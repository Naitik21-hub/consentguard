"""Thin wrapper around the official Anthropic Python SDK for live mode.

Reliability rules:
* Network-level retries are bounded by the SDK (``max_retries``; 408/409/429/5xx
  and connection errors). Timeouts are explicit.
* If the model's JSON does not validate, we make at most ONE repair request
  that includes the validation error. After that we fail loudly.
* A failure is never converted into a demo report or a partial "success".
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel, ValidationError

DEFAULT_MODEL = "claude-opus-5"
REQUEST_TIMEOUT_S = 300.0
SDK_MAX_RETRIES = 2
MAX_REPAIR_ATTEMPTS = 1
MAX_OUTPUT_TOKENS = 32000
# Server-side refusal fallback beta (Claude API). Set CONSENTGUARD_FALLBACKS=off to disable.
FALLBACK_BETA = "server-side-fallback-2026-07-01"

T = TypeVar("T", bound=BaseModel)


class LLMError(Exception):
    """User-facing error for live-mode failures."""


@dataclass
class LLMResult:
    parsed: BaseModel
    model_id: str
    attempts: int
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None


def configured_model() -> str:
    return os.environ.get("CONSENTGUARD_MODEL", "").strip() or DEFAULT_MODEL


def fallbacks_enabled(model: str) -> bool:
    setting = os.environ.get("CONSENTGUARD_FALLBACKS", "default").strip().lower()
    return setting != "off" and (model.startswith("claude-opus-5") or model.startswith("claude-fable-5"))


def api_key_present() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))


def make_client():  # pragma: no cover - requires network credentials
    import anthropic

    return anthropic.Anthropic(timeout=REQUEST_TIMEOUT_S, max_retries=SDK_MAX_RETRIES)


def extract_json(text: str) -> Any:
    """Parse JSON from model text, tolerating code fences or surrounding prose."""
    t = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", t, re.DOTALL)
    if fence:
        t = fence.group(1)
    start, end = t.find("{"), t.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("No JSON object found in the model response.")
    return json.loads(t[start : end + 1])


def _one_call(client, model: str, system: str, messages: list) -> Tuple[str, Any]:
    """One streamed request. Returns (text, final_message)."""
    import anthropic

    kwargs = dict(model=model, max_tokens=MAX_OUTPUT_TOKENS, system=system, messages=messages)
    if fallbacks_enabled(model):
        kwargs.update(betas=[FALLBACK_BETA], fallbacks="default")
    try:
        with client.beta.messages.stream(**kwargs) as stream:
            msg = stream.get_final_message()
    except anthropic.APITimeoutError as exc:
        raise LLMError(f"The model request timed out after {REQUEST_TIMEOUT_S:.0f}s (with {SDK_MAX_RETRIES} retries). Try again later or use a shorter document.") from exc
    except anthropic.AuthenticationError as exc:
        raise LLMError("The API key was rejected. Check ANTHROPIC_API_KEY in your .env file.") from exc
    except anthropic.NotFoundError as exc:
        raise LLMError(f"Model '{model}' was not found for this key. Set CONSENTGUARD_MODEL to a model your account can use.") from exc
    except anthropic.RateLimitError as exc:
        raise LLMError("Rate limit reached after retries. Wait a minute and try again.") from exc
    except anthropic.BadRequestError as exc:
        raise LLMError(f"The API rejected the request: {getattr(exc, 'message', exc)}") from exc
    except anthropic.APIStatusError as exc:
        raise LLMError(f"The API returned an error (HTTP {exc.status_code}) after retries.") from exc
    except anthropic.APIConnectionError as exc:
        raise LLMError("Could not reach the Anthropic API. Check your internet connection.") from exc

    if msg.stop_reason == "refusal":
        raise LLMError("The model declined this request. No analysis was produced.")
    if msg.stop_reason == "max_tokens":
        raise LLMError("The model's answer was cut off at the output limit. No partial analysis is shown. Try a shorter document.")
    text = "".join(getattr(b, "text", "") for b in msg.content if getattr(b, "type", "") == "text")
    return text, msg


def call_structured(
    system: str,
    user: str,
    output_model: Type[T],
    client=None,
    model: Optional[str] = None,
) -> LLMResult:
    """Call the model and validate its JSON against ``output_model``.

    ``client`` may be injected (tests pass a fake). One repair round is allowed.
    """
    model = model or configured_model()
    client = client or make_client()
    messages: list = [{"role": "user", "content": user}]
    last_error = ""
    for attempt in range(1, MAX_REPAIR_ATTEMPTS + 2):
        text, msg = _one_call(client, model, system, messages)
        try:
            data = extract_json(text)
            parsed = output_model.model_validate(data)
            usage = getattr(msg, "usage", None)
            return LLMResult(
                parsed=parsed,
                model_id=getattr(msg, "model", model) or model,
                attempts=attempt,
                input_tokens=getattr(usage, "input_tokens", None),
                output_tokens=getattr(usage, "output_tokens", None),
            )
        except (ValueError, ValidationError) as exc:
            last_error = str(exc)[:2000]
            messages = messages + [
                {"role": "assistant", "content": text or "(empty)"},
                {
                    "role": "user",
                    "content": "Your previous reply did not match the required JSON contract. Validation error:\n"
                    + last_error
                    + "\nReturn ONLY one corrected JSON object that follows the contract. Do not add new facts.",
                },
            ]
    raise LLMError(
        "The model's output failed validation after a repair attempt, so no report was produced. "
        "Details: " + last_error[:400]
    )

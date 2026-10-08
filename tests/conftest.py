"""Shared test helpers. Default tests never touch the network: live calls use FakeClient."""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TODAY = date(2026, 10, 8)


def fake_message(text: str, stop_reason: str = "end_turn", model: str = "claude-opus-5"):
    return SimpleNamespace(
        content=[SimpleNamespace(type="text", text=text)],
        stop_reason=stop_reason,
        model=model,
        usage=SimpleNamespace(input_tokens=100, output_tokens=50),
    )


class _Stream:
    def __init__(self, outcome):
        self.outcome = outcome

    def __enter__(self):
        if isinstance(self.outcome, Exception):
            raise self.outcome
        return self

    def __exit__(self, *exc):
        return False

    def get_final_message(self):
        return self.outcome


class FakeClient:
    """Mimics ``client.beta.messages.stream(...)``; returns queued outcomes in order."""

    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(stream=self._stream))

    def _stream(self, **kwargs):
        self.calls.append(kwargs)
        if not self.outcomes:
            raise AssertionError("FakeClient called more times than expected")
        return _Stream(self.outcomes.pop(0))


@pytest.fixture
def today():
    return TODAY


def draft_json(scenario_id: str) -> str:
    return (ROOT / "examples" / "expected_outputs" / f"{scenario_id}.draft.json").read_text(encoding="utf-8")


def as_text(obj) -> str:
    return obj if isinstance(obj, str) else json.dumps(obj)

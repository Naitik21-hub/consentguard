"""Local, best-effort redaction before anything is sent to an external model.

Redaction runs entirely on the user's machine. It replaces common Indian and
general identifiers with consistent placeholders (the same value always gets
the same placeholder within one document). It is NOT anonymization: names,
addresses, rare job titles, or unusual combinations of facts can still
identify a person. The app shows this warning next to the preview.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# Order matters: more specific patterns run first.
PATTERNS: List[Tuple[str, str]] = [
    ("EMAIL", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    ("UPI_ID", r"\b[A-Za-z0-9._-]{2,}@(?:ok)?[A-Za-z]{2,}\b"),
    ("CARD_NUMBER", r"\b(?:\d[ -]?){13,19}\b"),
    ("AADHAAR", r"\b[2-9]\d{3}[ -]?\d{4}[ -]?\d{4}\b"),
    ("PAN", r"\b[A-Z]{5}\d{4}[A-Z]\b"),
    ("IFSC", r"\b[A-Z]{4}0[A-Z0-9]{6}\b"),
    ("PHONE", r"(?<!\d)(?:\+91[ -]?|0)?[6-9]\d{4}[ -]?\d{5}(?!\d)"),
    ("IP_ADDRESS", r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
]

REDACTION_WARNING = (
    "Redaction is best-effort pattern matching for emails, phone numbers, UPI IDs, card numbers, "
    "Aadhaar-like and PAN-like numbers, IFSC codes and IP addresses. It does not find names, "
    "addresses, or other details, and unusual combinations of facts can still identify someone. "
    "Review the preview before sending."
)


@dataclass
class RedactionResult:
    text: str
    counts: Dict[str, int] = field(default_factory=dict)
    # placeholder -> original; kept only in session memory, never sent or exported.
    mapping: Dict[str, str] = field(default_factory=dict)

    @property
    def total(self) -> int:
        return sum(self.counts.values())


def redact(text: str) -> RedactionResult:
    seen: Dict[Tuple[str, str], str] = {}
    counters: Dict[str, int] = {}
    mapping: Dict[str, str] = {}
    counts: Dict[str, int] = {}

    def make_sub(label: str):
        def _sub(m: re.Match) -> str:
            value = m.group(0)
            if value.startswith("[") and value.endswith("]"):
                return value
            key = (label, re.sub(r"[\s-]", "", value).lower())
            if key not in seen:
                counters[label] = counters.get(label, 0) + 1
                seen[key] = f"[{label}_{counters[label]}]"
                mapping[seen[key]] = value
            counts[label] = counts.get(label, 0) + 1
            return seen[key]

        return _sub

    out = text
    for label, pattern in PATTERNS:
        out = re.sub(pattern, make_sub(label), out)
    return RedactionResult(text=out, counts=counts, mapping=mapping)

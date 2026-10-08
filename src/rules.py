"""Deterministic rule engine. Canonical rule data lives in rules/*.json.

This module implements the code-executed parts of three skills:
* findings-prioritization  -> ``prioritize``
* jurisdiction-check       -> ``attach_legal_sources``
* report-and-qa (labels)   -> ``overall_label``, ``sanitize_phrases``
"""
from __future__ import annotations

import json
import re
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .models import (
    CONFIDENCE_ORDER,
    SEVERITY_ORDER,
    ConsentDimension,
    Finding,
    LegalSource,
)

ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = ROOT / "rules" / "governance_rules.json"
LEGAL_PATH = ROOT / "rules" / "legal_sources.json"


@lru_cache(maxsize=1)
def load_rules() -> dict:
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_legal_registry() -> dict:
    return json.loads(LEGAL_PATH.read_text(encoding="utf-8"))


def rules_by_id() -> Dict[str, dict]:
    return {r["rule_id"]: r for r in load_rules()["rules"]}


def legal_sources_by_id() -> Dict[str, LegalSource]:
    return {s["source_id"]: LegalSource(**s) for s in load_legal_registry()["sources"]}


def _min_sev(a: str, b: str) -> str:
    return a if SEVERITY_ORDER[a] <= SEVERITY_ORDER[b] else b


def _min_conf(a: str, b: str) -> str:
    return a if CONFIDENCE_ORDER[a] <= CONFIDENCE_ORDER[b] else b


# ---------------------------------------------------------------------------
# findings-prioritization
# ---------------------------------------------------------------------------
def prioritize(
    severity: str,
    confidence: str,
    rule: dict,
    evidence_basis: str,
    completeness: str,
) -> Tuple[str, str, List[str]]:
    """Apply transparent caps. Returns (severity, confidence, adjustment notes)."""
    caps = load_rules()["caps"]
    notes: List[str] = []

    capped = _min_sev(severity, rule["max_severity"])
    if capped != severity:
        notes.append(f"Severity capped from {severity} to {capped}: rule {rule['rule_id']} allows at most {rule['max_severity']}.")
        severity = capped

    if evidence_basis == "absence_in_supplied_text" and rule["evidence_type"] != "context":
        limit = (
            caps["absence_max_severity_when_complete"]
            if completeness == "complete"
            else caps["absence_max_severity_when_excerpt_or_unknown"]
        )
        capped = _min_sev(severity, limit)
        if capped != severity:
            notes.append(
                f"Severity capped from {severity} to {capped}: the finding rests on information being absent, "
                f"and the text is marked '{completeness}'."
            )
            severity = capped
        if completeness != "complete":
            c = _min_conf(confidence, caps["absence_max_confidence_when_excerpt_or_unknown"])
            if c != confidence:
                notes.append(f"Confidence lowered from {confidence} to {c}: absence in an excerpt is weak evidence.")
                confidence = c
    return severity, confidence, notes


def sort_findings(findings: List[Finding]) -> List[Finding]:
    return sorted(
        findings,
        key=lambda f: (-SEVERITY_ORDER[f.severity], -CONFIDENCE_ORDER[f.confidence], f.rule_id),
    )


# ---------------------------------------------------------------------------
# jurisdiction-check
# ---------------------------------------------------------------------------
def attach_legal_sources(rule: dict, jurisdiction: str, on_date: Optional[date] = None) -> Tuple[List[str], str, str]:
    """Return (legal_source_ids, applicability_status, note) for a rule.

    Legal sources come ONLY from the registry via the rule's ``legal_hooks``.
    The model cannot add or invent legal references.
    """
    on_date = on_date or date.today()
    hooks = rule.get("legal_hooks") or []
    if not hooks:
        return [], "no_legal_reference", "This is a governance heuristic with no linked legal source."
    if (jurisdiction or "").upper() != "IN":
        return (
            [],
            "not_applicable_jurisdiction",
            f"The legal source registry covers India only; no sources are linked for jurisdiction '{jurisdiction}'.",
        )
    registry = legal_sources_by_id()
    ids = [h for h in hooks if h in registry]
    sources = [registry[h] for h in ids]
    if not sources or any(s.verification_status != "verified" for s in sources):
        return ids, "not_verified", "At least one linked source has not been verified; treat as background only."

    effective = [date.fromisoformat(s.effective_date) for s in sources if s.effective_date]
    if effective and all(d <= on_date for d in effective):
        return ids, "verified_in_force", "Linked provisions are verified and appear to be in force on the analysis date."
    pending = sorted({s.effective_date for s in sources if s.effective_date and date.fromisoformat(s.effective_date) > on_date})
    return (
        ids,
        "verified_not_yet_in_force",
        "Linked provisions are verified but scheduled to commence on "
        + ", ".join(pending)
        + " (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. "
        "ConsentGuard does not decide whether any provision applies to this organisation.",
    )


# ---------------------------------------------------------------------------
# consent-design guard: no invented interface behaviour
# ---------------------------------------------------------------------------
def guard_interface_claims(
    dim: ConsentDimension, cited_texts: List[str], has_screen_text: bool
) -> Tuple[ConsentDimension, Optional[str]]:
    cfg = load_rules()
    spec = {d["id"]: d for d in cfg["consent_dimensions"]}[dim.dimension_id]
    expl = dim.explanation.lower()
    claims_ui = any(t in expl for t in cfg["interface_claim_terms"])
    evidence_ui = any(t in " ".join(cited_texts).lower() for t in cfg["interface_evidence_terms"])

    if dim.status in ("adequate", "concern"):
        if spec["requires_interface_evidence"] and not has_screen_text and not evidence_ui:
            return (
                dim.model_copy(update={
                    "status": "unknown",
                    "explanation": "A privacy notice alone cannot show whether a clear affirmative action was used. "
                    "Supply the consent-screen text to assess this. (Original note: " + dim.explanation + ")",
                }),
                f"Consent dimension '{dim.dimension_id}' reset to unknown: needs consent-screen evidence.",
            )
        if claims_ui and not evidence_ui:
            return (
                dim.model_copy(update={
                    "status": "unknown",
                    "explanation": "Interface behaviour (such as pre-ticked boxes or hidden controls) cannot be "
                    "established from the supplied text. (Original note: " + dim.explanation + ")",
                }),
                f"Consent dimension '{dim.dimension_id}' reset to unknown: interface claim without interface evidence.",
            )
    return dim, None


# ---------------------------------------------------------------------------
# report labels and wording
# ---------------------------------------------------------------------------
def overall_label(findings: List[Finding], completeness: str, n_paragraphs: int, dims: List[ConsentDimension]) -> Tuple[str, str]:
    high = [f for f in findings if f.severity == "high" and f.confidence in ("high", "medium")]
    medium = [f for f in findings if f.severity == "medium"]
    unknown_dims = sum(1 for d in dims if d.status == "unknown")
    if high:
        return "substantial_concerns", (
            f"{len(high)} high-severity finding(s) are supported by quoted text "
            f"({', '.join(f.finding_id for f in high)})."
        )
    if medium:
        return "clarification_needed", (
            f"No high-severity findings, but {len(medium)} medium-severity point(s) need clarification "
            f"({', '.join(f.finding_id for f in medium)})."
        )
    if completeness != "complete" and (n_paragraphs < 3 or unknown_dims >= 3):
        return "insufficient_information", (
            f"The supplied text is marked '{completeness}' and leaves {unknown_dims} of 7 consent dimensions unknown; "
            "there is not enough evidence for a broader assessment."
        )
    return "no_major_concerns", (
        "No high- or medium-severity concerns were supported by the supplied text. This covers only what the "
        "text says, not how the organisation behaves in practice."
    )


def sanitize_phrases(text: str) -> Tuple[str, bool]:
    """Replace phrases the product must never output (e.g. 'fully compliant', 'safe')."""
    changed = False
    out = text
    for phrase in load_rules()["banned_output_phrases"]:
        pattern = re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE)
        if pattern.search(out):
            out = pattern.sub("[wording removed: ConsentGuard does not certify compliance or safety]", out)
            changed = True
    return out, changed


def rules_prompt_table() -> str:
    """Compact rendering of the canonical rules for the model prompt (single source of truth)."""
    cfg = load_rules()
    lines = [f"Rule set {cfg['rule_set_id']} v{cfg['rule_set_version']}"]
    for r in cfg["rules"]:
        lines.append(
            f"- {r['rule_id']} [{r['evidence_type']}, max {r['max_severity']}] {r['title']}: {r['guidance']}"
        )
    lines.append("Consent dimensions: " + ", ".join(f"{d['id']} ({d['label']})" for d in cfg["consent_dimensions"]))
    lines.append("Permission guidance:")
    for g in cfg["permission_purpose_guidance"]:
        lines.append(
            f"- {g['permission']}: fits {', '.join(g['typical_fits'])}; needs explanation when "
            f"{'; '.join(g['needs_explanation_when'])}; alternatives: {', '.join(g['alternatives'])}"
        )
    return "\n".join(lines)

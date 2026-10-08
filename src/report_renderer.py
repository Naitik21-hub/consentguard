"""Render a validated Report as Markdown or JSON for intentional download."""
from __future__ import annotations

from typing import List

from .models import Report

EXPORT_NOTICE = (
    "This export contains quotations from the text you submitted. Share it only if you are comfortable "
    "sharing those quotations."
)

DIM_LABELS = {
    "purpose_clarity": "Clarity and specificity of purposes",
    "optional_separation": "Separation of optional uses from essential processing",
    "choice_granularity": "Granularity of choices",
    "affirmative_action": "Evidence of affirmative user action",
    "withdrawal": "Ease and availability of withdrawal",
    "recipient_retention_transparency": "Transparency about recipients and retention",
    "bundling_or_misleading": "Bundling, coercion, confusing wording, or misleading choices",
}
ASSESSMENT_LABELS = {
    "proportionate": "Appears proportionate to the stated purpose",
    "needs_explanation": "Needs explanation or narrower scope",
    "disproportionate": "Appears disproportionate to the stated purpose",
    "insufficient_information": "Insufficient information",
}


def _cell(s) -> str:
    if s is None or s == "":
        return "unknown"
    return str(s).replace("|", "\\|").replace("\n", " ")


def _ids(ids: List[str]) -> str:
    return ", ".join(ids) if ids else "none"


def to_json(report: Report) -> str:
    return report.model_dump_json(indent=2)


def to_markdown(report: Report) -> str:
    r = report
    L: List[str] = []
    L.append(f"# ConsentGuard report: {r.document_title or 'Untitled document'}")
    L.append("")
    L.append(f"> {EXPORT_NOTICE}")
    L.append(f"> **{r.mode_note}**")
    L.append("")
    L.append(f"- Report ID: `{r.report_id}`  |  Analyzed: {r.analyzed_at}  |  Mode: {r.mode}")
    L.append(f"- Document version: {r.document_version or 'unknown'}  |  Jurisdiction: {r.jurisdiction}  |  Completeness: {r.completeness}")
    L.append(f"- Rule set v{r.rule_set_version}  |  Legal sources last verified: {r.last_verification_date}")
    L.append("")
    L.append(f"## Overall: {r.overall_assessment_label}")
    L.append(r.overall_rationale)
    L.append("")
    L.append("*ConsentGuard does not certify safety or legal compliance. It explains the supplied text only.*")
    if r.extraction_warnings:
        L.append("")
        L.append("**Extraction and scope warnings**")
        L += [f"- {w}" for w in r.extraction_warnings]

    s = r.plain_english_summary
    L.append("\n## Plain-English summary")
    for title, pts in [
        ("Data collected", s.data_collected),
        ("Purposes", s.purposes),
        ("Who receives it", s.recipients),
        ("How long it is kept", s.retention),
        ("Your choices and how to withdraw", s.choices_and_withdrawal),
    ]:
        L.append(f"\n**{title}**")
        if not pts:
            L.append("- Not stated in the supplied text.")
        for p in pts:
            tag = "" if p.basis == "stated" else f" *({p.basis})*"
            L.append(f"- {p.text}{tag} [{_ids(p.evidence_ids)}]")
    if s.unknowns:
        L.append("\n**Unknown or missing in the supplied text**")
        L += [f"- {u}" for u in s.unknowns]

    L.append("\n## Data inventory")
    L.append("| Data | Basis | Purpose | Recipients | Retention | Evidence |")
    L.append("|---|---|---|---|---|---|")
    for d in r.data_inventory:
        L.append(f"| {_cell(d.data_category)} | {d.collection_basis} | {_cell(d.purpose)} | {_cell(d.recipients)} | {_cell(d.retention)} | {_ids(d.evidence_ids)} |")

    L.append("\n## Permission-purpose map")
    L.append("| Permission | Feature | Scope | Required? | Assessment | Alternatives | Evidence |")
    L.append("|---|---|---|---|---|---|---|")
    for p in r.permission_purpose_map:
        L.append(
            f"| {_cell(p.permission)} | {_cell(p.feature)} | {_cell(p.scope)} | {p.required_status} | "
            f"{ASSESSMENT_LABELS[p.assessment]}: {_cell(p.rationale)} | {_cell('; '.join(p.alternatives))} | {_ids(p.evidence_ids)} |"
        )

    L.append("\n## Consent-design review")
    for d in r.consent_dimensions:
        L.append(f"- **{DIM_LABELS[d.dimension_id]}**: {d.status}. {d.explanation} [{_ids(d.evidence_ids)}]")

    L.append("\n## Findings")
    if not r.findings:
        L.append("No findings.")
    for f in r.findings:
        L.append(f"\n### {f.finding_id}. {f.title}")
        L.append(f"- Severity: **{f.severity}** | Confidence: **{f.confidence}** | Rule: {f.rule_id} v{f.rule_version}")
        L.append(f"- Evidence basis: {f.evidence_basis.replace('_', ' ')} | Document evidence: {_ids(f.document_evidence_ids)}")
        L.append(f"- Legal context: {f.legal_applicability_status.replace('_', ' ')} ({_ids(f.legal_source_ids)}). {f.legal_applicability_note}")
        L.append("")
        L.append(f.explanation)
        for q in f.quotes:
            L.append(f"\n> \"{q.quote}\" ({q.evidence_id}, exact quote verified)")
        if f.missing_context:
            L.append("\nWould change this assessment: " + "; ".join(f.missing_context))
        L.append(f"\n**Suggested action:** {f.recommended_action}")
        for a in f.adjustments:
            L.append(f"- *Adjustment:* {a}")

    L.append("\n## Questions to ask the organisation")
    for q in r.targeted_questions:
        L.append(f"- {q.question} *(Why: {q.why_it_matters})*")

    L.append("\n## Suggested next steps (you decide)")
    for st in r.next_steps:
        L.append(f"- {st.action}" + (" *(if available)*" if st.conditional else ""))

    L.append("\n## Legal sources (India registry)")
    if not r.legal_sources:
        L.append("No legal sources linked.")
    for src in r.legal_sources:
        L.append(
            f"- **{src.source_id}**: {src.title}. {src.issuing_authority}. Provision: {src.provision or 'n/a'}. "
            f"Published {src.publication_date or 'unknown'}; effective {src.effective_date or 'n/a'}; "
            f"status: {src.verification_status}; retrieved {src.retrieval_date}. {src.official_url or 'No official URL recorded.'}"
        )

    L.append("\n## Evidence index")
    cited = {i for f in r.findings for i in f.document_evidence_ids}
    for p in r.evidence:
        if p.evidence_id in cited:
            L.append(f"- **{p.evidence_id}** ({p.location}): {p.text}")

    L.append("\n## Limitations")
    L += [f"- {x}" for x in r.limitations]

    L.append("\n## Skills run")
    L.append("| Skill | Version | Executor | Status | Note |")
    L.append("|---|---|---|---|---|")
    for sk in r.skills_run:
        L.append(f"| {sk.skill} | {sk.version} | {sk.executor} | {sk.status} | {_cell(sk.note)} |")

    L.append("\n## Validation checks")
    for c in r.validation:
        L.append(f"- [{'pass' if c.passed else 'adjusted'}] {c.check}" + (f": {c.detail}" if c.detail else ""))
    return "\n".join(L) + "\n"

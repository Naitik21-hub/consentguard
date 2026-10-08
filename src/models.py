"""Pydantic data contracts for ConsentGuard.

Two families of models live here:

* Model-output contract (``AnalysisDraft`` and friends): what the language model
  (or a pre-authored demo fixture) must return. It is deliberately narrow: the
  model cannot set legal sources, overall labels, finding IDs or validation
  results. Those are computed deterministically by the orchestrator.
* Report contract (``Report`` and friends): the validated, user-facing result.

JSON Schemas in ``schemas/`` are generated from these classes
(``python -m src.export_schemas``) so code and schema never drift apart.
"""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

Severity = Literal["high", "medium", "low", "informational"]
Confidence = Literal["high", "medium", "low"]
Completeness = Literal["complete", "excerpt", "unknown"]
AssessmentLabel = Literal["proportionate", "needs_explanation", "disproportionate", "insufficient_information"]
OverallLabel = Literal["substantial_concerns", "clarification_needed", "no_major_concerns", "insufficient_information"]
DimensionStatus = Literal["adequate", "concern", "unknown", "not_applicable"]
LegalApplicability = Literal[
    "verified_in_force",
    "verified_not_yet_in_force",
    "not_verified",
    "not_applicable_jurisdiction",
    "no_legal_reference",
]

SEVERITY_ORDER = {"informational": 0, "low": 1, "medium": 2, "high": 3}
CONFIDENCE_ORDER = {"low": 0, "medium": 1, "high": 2}


class _Strict(BaseModel):
    """Reject fields the contract does not define (no silent extra data)."""

    model_config = ConfigDict(extra="forbid")


# --------------------------------------------------------------------------
# Intake
# --------------------------------------------------------------------------
class PermissionInput(_Strict):
    name: str = Field(..., max_length=80)
    status: Literal["required", "optional", "unknown"] = "unknown"


class SuppliedContext(_Strict):
    service_name: Optional[str] = None
    service_category: Optional[str] = None
    jurisdiction: str = "IN"
    intended_feature: Optional[str] = None
    completeness: Completeness = "unknown"
    permissions: List[PermissionInput] = Field(default_factory=list)
    consent_screen_text: Optional[str] = None
    policy_date_version: Optional[str] = None


class Paragraph(_Strict):
    """One evidence unit. ``evidence_id`` is stable for a given input text."""

    evidence_id: str = Field(..., pattern=r"^(P\d{3,4}|C\d{2,3})$")
    text: str
    page: Optional[int] = None
    paragraph_index: int
    section: Optional[str] = None
    source: Literal["document", "consent_screen"] = "document"

    @property
    def location(self) -> str:
        where = f"page {self.page}, " if self.page else ""
        src = "consent screen" if self.source == "consent_screen" else "paragraph"
        sec = f" (section: {self.section})" if self.section else ""
        return f"{where}{src} {self.paragraph_index}{sec}"


class IntakeResult(_Strict):
    source_type: Literal["paste", "txt", "md", "pdf"]
    char_count: int
    paragraph_count: int
    page_count: Optional[int] = None
    parse_quality: Literal["good", "partial", "failed"]
    completeness: Completeness
    jurisdiction: str
    jurisdiction_supported: bool
    extraction_warnings: List[str] = Field(default_factory=list)
    injection_evidence_ids: List[str] = Field(default_factory=list)
    within_limits: bool = True
    material_questions: List[str] = Field(default_factory=list)


# --------------------------------------------------------------------------
# Model-output contract (AnalysisDraft)
# --------------------------------------------------------------------------
class SummaryPoint(_Strict):
    text: str
    basis: Literal["stated", "inferred", "unknown"] = "stated"
    evidence_ids: List[str] = Field(default_factory=list)


class PlainSummary(_Strict):
    data_collected: List[SummaryPoint] = Field(default_factory=list)
    purposes: List[SummaryPoint] = Field(default_factory=list)
    recipients: List[SummaryPoint] = Field(default_factory=list)
    retention: List[SummaryPoint] = Field(default_factory=list)
    choices_and_withdrawal: List[SummaryPoint] = Field(default_factory=list)
    unknowns: List[str] = Field(default_factory=list)


class DataInventoryItem(_Strict):
    data_category: str
    collection_basis: Literal["stated", "inferred", "permission_only", "unknown"] = "stated"
    purpose: Optional[str] = None
    recipients: Optional[str] = None
    retention: Optional[str] = None
    evidence_ids: List[str] = Field(default_factory=list)


class PermissionMapItem(_Strict):
    permission: str
    feature: Optional[str] = None
    scope: Optional[str] = None
    required_status: Literal["required", "optional", "unknown"] = "unknown"
    assessment: AssessmentLabel
    rationale: str
    alternatives: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)


class ConsentDimension(_Strict):
    dimension_id: Literal[
        "purpose_clarity",
        "optional_separation",
        "choice_granularity",
        "affirmative_action",
        "withdrawal",
        "recipient_retention_transparency",
        "bundling_or_misleading",
    ]
    status: DimensionStatus
    explanation: str
    evidence_ids: List[str] = Field(default_factory=list)


class Quote(_Strict):
    evidence_id: str
    quote: str


class DraftFinding(_Strict):
    rule_id: str
    severity: Severity
    confidence: Confidence
    title: str
    explanation: str
    evidence_ids: List[str] = Field(default_factory=list)
    quotes: List[Quote] = Field(default_factory=list)
    missing_context: List[str] = Field(default_factory=list)
    recommended_action: Optional[str] = None


class TargetedQuestion(_Strict):
    question: str
    why_it_matters: str


class NextStep(_Strict):
    action: str
    conditional: bool = False


class AnalysisDraft(_Strict):
    """Exactly what the model (or a demo fixture) returns."""

    document_title: Optional[str] = None
    document_version: Optional[str] = None
    plain_english_summary: PlainSummary
    data_inventory: List[DataInventoryItem] = Field(default_factory=list)
    permission_purpose_map: List[PermissionMapItem] = Field(default_factory=list)
    consent_dimensions: List[ConsentDimension] = Field(default_factory=list)
    findings: List[DraftFinding] = Field(default_factory=list)
    targeted_questions: List[TargetedQuestion] = Field(default_factory=list)
    next_steps: List[NextStep] = Field(default_factory=list)


# --------------------------------------------------------------------------
# Report contract
# --------------------------------------------------------------------------
class VerifiedQuote(_Strict):
    evidence_id: str
    quote: str
    verified: bool


class Finding(_Strict):
    finding_id: str
    rule_id: str
    rule_version: str
    title: str
    severity: Severity
    confidence: Confidence
    explanation: str
    evidence_basis: Literal["quoted", "absence_in_supplied_text"]
    document_evidence_ids: List[str]
    quotes: List[VerifiedQuote] = Field(default_factory=list)
    legal_source_ids: List[str] = Field(default_factory=list)
    legal_applicability_status: LegalApplicability
    legal_applicability_note: str
    missing_context: List[str] = Field(default_factory=list)
    recommended_action: str
    adjustments: List[str] = Field(default_factory=list)


class LegalSource(_Strict):
    source_id: str
    jurisdiction: str
    source_type: str
    title: str
    issuing_authority: str
    official_url: Optional[str]
    provision: Optional[str]
    publication_date: Optional[str]
    effective_date: Optional[str]
    verification_status: Literal["verified", "unavailable", "superseded", "needs_review"]
    retrieval_date: str
    summary: str
    applicability_notes: str


class SkillRun(_Strict):
    skill: str
    version: str
    status: Literal["success", "failed", "skipped"]
    executor: Literal["code", "model", "fixture"]
    note: str = ""


class ValidationCheck(_Strict):
    check: str
    passed: bool
    detail: str = ""


class Report(_Strict):
    report_id: str
    analyzed_at: str
    mode: Literal["demo", "live"]
    mode_note: str
    model_id: Optional[str] = None
    document_title: Optional[str]
    document_version: Optional[str]
    jurisdiction: str
    supplied_context: SuppliedContext
    completeness: Completeness
    extraction_warnings: List[str]
    overall_assessment: OverallLabel
    overall_assessment_label: str
    overall_rationale: str
    plain_english_summary: PlainSummary
    data_inventory: List[DataInventoryItem]
    permission_purpose_map: List[PermissionMapItem]
    consent_dimensions: List[ConsentDimension]
    findings: List[Finding]
    targeted_questions: List[TargetedQuestion]
    next_steps: List[NextStep]
    evidence: List[Paragraph]
    legal_sources: List[LegalSource]
    last_verification_date: str
    rule_set_version: str
    limitations: List[str]
    skills_run: List[SkillRun]
    validation: List[ValidationCheck]


class QAAnswer(_Strict):
    question: str
    answer: str
    answer_type: Literal["answered_from_document", "not_in_document", "general_guidance", "unverified"]
    evidence_ids: List[str] = Field(default_factory=list)
    quotes: List[VerifiedQuote] = Field(default_factory=list)
    method: Literal["live_model", "keyword_retrieval"]
    note: str = ""


class QADraft(_Strict):
    """What the model returns for a follow-up question."""

    answer: str
    answer_type: Literal["answered_from_document", "not_in_document", "general_guidance"]
    evidence_ids: List[str] = Field(default_factory=list)
    quotes: List[Quote] = Field(default_factory=list)

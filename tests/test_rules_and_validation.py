"""Rule caps, legal applicability, schema validation, and the post-processing guards."""
import json
from datetime import date

import pytest
from pydantic import ValidationError

from src import rules as R
from src.demo import prepare_scenario, scenario_draft
from src.models import AnalysisDraft, ConsentDimension
from src.orchestrator import post_process
from tests.conftest import TODAY, draft_json


# ---- Legal applicability -------------------------------------------------------
def test_dpdp_consent_rule_is_verified_but_not_yet_in_force_on_build_date():
    ids, status, note = R.attach_legal_sources(R.rules_by_id()["CG-CN-01"], "IN", date(2026, 10, 8))
    assert ids == ["LS-IN-DPDPA-S6"]
    assert status == "verified_not_yet_in_force"
    assert "2027-05-13" in note


def test_status_flips_after_commencement_date():
    _, status, _ = R.attach_legal_sources(R.rules_by_id()["CG-CN-01"], "IN", date(2027, 6, 1))
    assert status == "verified_in_force"


def test_non_india_jurisdiction_gets_no_sources():
    ids, status, _ = R.attach_legal_sources(R.rules_by_id()["CG-CN-01"], "US", TODAY)
    assert ids == [] and status == "not_applicable_jurisdiction"


def test_needs_review_source_never_reported_as_verified(monkeypatch):
    rule = dict(R.rules_by_id()["CG-CN-01"], legal_hooks=["LS-IN-ITACT-43A"])
    ids, status, _ = R.attach_legal_sources(rule, "IN", TODAY)
    assert status == "not_verified"


def test_registry_sources_have_required_fields_and_official_domains():
    for s in R.load_legal_registry()["sources"]:
        assert s["verification_status"] in ("verified", "unavailable", "superseded", "needs_review")
        if s["verification_status"] == "verified":
            assert s["official_url"] and any(d in s["official_url"] for d in ("meity.gov.in", "pib.gov.in", "egazette.gov.in", "indiacode.nic.in"))
            assert s["retrieval_date"]


# ---- Prioritization ------------------------------------------------------------
def test_absence_cap_when_complete_is_medium():
    sev, conf, notes = R.prioritize("high", "high", R.rules_by_id()["CG-CN-02"], "absence_in_supplied_text", "complete")
    assert sev == "medium" and conf == "high" and notes


def test_rule_max_severity_cap():
    sev, _, notes = R.prioritize("high", "high", R.rules_by_id()["CG-PO-01"], "quoted", "complete")
    assert sev == "informational" and notes


def test_sanitize_removes_banned_phrases_but_not_similar_words():
    out, changed = R.sanitize_phrases("This app is safe and fully compliant.")
    assert changed and "fully compliant" not in out.lower() and "is safe" not in out.lower()
    out2, changed2 = R.sanitize_phrases("Data is safeguarded with encryption.")
    assert not changed2 and out2 == "Data is safeguarded with encryption."


# ---- Schema validation of model output -----------------------------------------
def test_malformed_draft_rejected_extra_field():
    data = json.loads(draft_json("01_delivery_overreach"))
    data["legal_source_ids"] = ["GDPR Art. 7"]  # model may not add legal sources
    with pytest.raises(ValidationError):
        AnalysisDraft.model_validate(data)


def test_malformed_draft_rejected_bad_enum():
    data = json.loads(draft_json("01_delivery_overreach"))
    data["findings"][0]["severity"] = "critical"
    with pytest.raises(ValidationError):
        AnalysisDraft.model_validate(data)


# ---- Post-processing guards ----------------------------------------------------
def _run(draft: AnalysisDraft, sid="01_delivery_overreach"):
    return post_process(draft, prepare_scenario(sid), "demo", [], today=TODAY)


def test_fabricated_quote_and_unknown_ids_removed_and_unsupported_finding_dropped():
    d = scenario_draft("01_delivery_overreach")
    bad = d.findings[0].model_copy(update={
        "rule_id": "CG-PP-01",
        "evidence_ids": ["P999"],
        "quotes": [{"evidence_id": "P005", "quote": "We sell your location to data brokers."}],
    })
    d = d.model_copy(update={"findings": [bad]})
    r = _run(d)
    assert "CG-PP-01" not in {f.rule_id for f in r.findings}
    details = " ".join(c.detail for c in r.validation)
    assert "P999" in details and "non-matching quote" in details


def test_partially_fabricated_quotes_keep_only_verified():
    d = scenario_draft("01_delivery_overreach")
    f0 = d.findings[0]
    f0 = f0.model_copy(update={"quotes": list(f0.quotes) + [{"evidence_id": "P009", "quote": "We read your private messages."}]})
    r = _run(d.model_copy(update={"findings": [f0]}))
    kept = next(f for f in r.findings if f.rule_id == f0.rule_id)
    assert all(q.verified for q in kept.quotes) and len(kept.quotes) == 2


def test_unknown_rule_id_dropped():
    d = scenario_draft("01_delivery_overreach")
    d = d.model_copy(update={"findings": [d.findings[0].model_copy(update={"rule_id": "CG-MADE-UP"})]})
    r = _run(d)
    assert all(f.rule_id != "CG-MADE-UP" for f in r.findings)


def test_invented_interface_behaviour_reset_to_unknown():
    d = scenario_draft("01_delivery_overreach")
    dims = [ConsentDimension(dimension_id="bundling_or_misleading", status="concern",
                             explanation="The consent checkbox is pre-ticked and the decline button is hidden.", evidence_ids=["P012"])]
    r = _run(d.model_copy(update={"consent_dimensions": dims}))
    dim = next(x for x in r.consent_dimensions if x.dimension_id == "bundling_or_misleading")
    assert dim.status == "unknown"
    assert len(r.consent_dimensions) == 7


def test_affirmative_action_without_screen_text_is_unknown():
    d = scenario_draft("01_delivery_overreach")
    dims = [ConsentDimension(dimension_id="affirmative_action", status="concern", explanation="Agreement is implied.", evidence_ids=["P016"])]
    r = _run(d.model_copy(update={"consent_dimensions": dims}))
    assert next(x for x in r.consent_dimensions if x.dimension_id == "affirmative_action").status == "unknown"


def test_stated_summary_point_without_evidence_relabelled_inferred():
    d = scenario_draft("06_short_excerpt")
    s = d.plain_english_summary.model_copy(deep=True)
    s.purposes[0].evidence_ids = ["P404"]
    r = _run(d.model_copy(update={"plain_english_summary": s}), sid="06_short_excerpt")
    assert r.plain_english_summary.purposes[0].basis == "inferred"


def test_high_absence_finding_in_excerpt_never_high():
    d = scenario_draft("06_short_excerpt")
    f = d.findings[0].model_copy(update={"severity": "high", "confidence": "high"})
    r = _run(d.model_copy(update={"findings": [f]}), sid="06_short_excerpt")
    rt = next(x for x in r.findings if x.rule_id == "CG-RT-01")
    assert rt.severity == "low" and rt.confidence == "low"
    assert r.overall_assessment != "substantial_concerns"

"""All eight synthetic scenarios against human-authored expected outcomes."""
import json

import pytest

from src.demo import list_scenarios, run_demo
from src.models import SEVERITY_ORDER, CONFIDENCE_ORDER
from src.rules import load_rules
from tests.conftest import ROOT, TODAY

EXPECTED = json.loads((ROOT / "examples" / "expected_outputs" / "expected_outcomes.json").read_text(encoding="utf-8"))["scenarios"]
IDS = [s["id"] for s in list_scenarios()]


def test_eight_scenarios_exist():
    assert len(IDS) >= 8 and set(IDS) == set(EXPECTED)


@pytest.mark.parametrize("sid", IDS)
def test_scenario_matches_expected_outcome(sid):
    r = run_demo(sid, today=TODAY)
    exp = EXPECTED[sid]
    rules = {f.rule_id for f in r.findings}
    assert r.overall_assessment == exp["overall"], (sid, r.overall_rationale)
    for rid in exp["must_include_rules"]:
        assert rid in rules, (sid, rid)
    for rid in exp["must_not_include_rules"]:
        assert rid not in rules, (sid, rid)
    for perm, label in exp.get("permission_assessments", {}).items():
        match = [p for p in r.permission_purpose_map if p.permission.lower().startswith(perm.lower())]
        assert match and match[0].assessment == label, (sid, perm)


@pytest.mark.parametrize("sid", IDS)
def test_fixture_quotes_all_verify_and_ids_exist(sid):
    """Pre-authored fixtures must pass the same quote checks as live output."""
    r = run_demo(sid, today=TODAY)
    failed = [c for c in r.validation if c.check in ("quotes match submitted text",) or c.check.startswith("evidence IDs exist")]
    assert not failed, failed
    ids = {p.evidence_id for p in r.evidence}
    for f in r.findings:
        assert set(f.document_evidence_ids) <= ids
        assert all(q.verified for q in f.quotes)
        # document evidence and legal source IDs never mix
        assert not any(i.startswith("LS-") for i in f.document_evidence_ids)
        assert all(s.startswith("LS-") for s in f.legal_source_ids)
        if f.evidence_basis == "quoted":
            assert f.document_evidence_ids


@pytest.mark.parametrize("sid", IDS)
def test_no_banned_wording_in_generated_fields(sid):
    r = run_demo(sid, today=TODAY)
    generated = [r.overall_rationale, r.overall_assessment_label] + [f.explanation + f.title + f.recommended_action for f in r.findings]
    generated += [s.action for s in r.next_steps]
    for phrase in load_rules()["banned_output_phrases"]:
        for g in generated:
            assert phrase.lower() not in g.lower(), (sid, phrase, g)


@pytest.mark.parametrize("sid", IDS)
def test_all_nine_skills_recorded(sid):
    r = run_demo(sid, today=TODAY)
    assert len({s.skill for s in r.skills_run}) == 9
    assert all(s.status == "success" for s in r.skills_run)
    assert all(s.executor in ("code", "fixture") for s in r.skills_run)
    assert r.mode == "demo" and "Not live AI analysis" in r.mode_note


def test_purpose_dependent_microphone_judgement():
    delivery = run_demo("01_delivery_overreach", today=TODAY)
    calling = run_demo("02_video_call_separate_marketing", today=TODAY)
    mic = lambda r: next(p for p in r.permission_purpose_map if p.permission.lower().startswith("microphone"))
    assert mic(delivery).assessment == "disproportionate"
    assert mic(calling).assessment == "proportionate"


def test_bank_kyc_not_treated_as_consent_failure():
    r = run_demo("03_bank_partner_marketing", today=TODAY)
    lg = [f for f in r.findings if f.rule_id == "CG-LG-01"]
    assert lg and lg[0].severity == "informational"
    # No adverse finding rests only on the KYC paragraph.
    for f in r.findings:
        if f.document_evidence_ids == ["P004"]:
            assert f.severity == "informational"


def test_excerpt_absence_findings_are_capped():
    r = run_demo("06_short_excerpt", today=TODAY)
    for f in r.findings:
        if f.evidence_basis == "absence_in_supplied_text" and f.rule_id != "CG-SC-01":
            assert SEVERITY_ORDER[f.severity] <= SEVERITY_ORDER["low"]
            assert CONFIDENCE_ORDER[f.confidence] <= CONFIDENCE_ORDER["low"]
            assert f.adjustments  # every cap is explained


def test_health_sensitivity_is_not_a_legal_classification():
    r = run_demo("05_fitness_health_sharing", today=TODAY)
    sn = next(f for f in r.findings if f.rule_id == "CG-SN-01")
    assert "does not decide how the law classifies" in sn.explanation
    assert sn.legal_source_ids == [] and sn.legal_applicability_status == "no_legal_reference"


def test_missing_consent_screen_keeps_interface_unknown():
    r = run_demo("01_delivery_overreach", today=TODAY)
    dim = next(d for d in r.consent_dimensions if d.dimension_id == "affirmative_action")
    assert dim.status == "unknown"
    assert all(len(r.consent_dimensions) == 7 for _ in [0])


def test_consent_screen_evidence_allows_affirmative_action_assessment():
    r = run_demo("08_well_explained", today=TODAY)
    dim = next(d for d in r.consent_dimensions if d.dimension_id == "affirmative_action")
    assert dim.status == "adequate" and any(i.startswith("C") for i in dim.evidence_ids)

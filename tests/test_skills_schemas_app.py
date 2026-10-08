"""Skill packaging, schema drift, exports, and the Streamlit reset behaviour."""
import json
import re

import jsonschema
import pytest

from src.demo import run_demo
from src.export_schemas import SCHEMA_DIR, build_schemas
from src.orchestrator import MODEL_SKILLS, SKILL_VERSIONS, SKILLS_DIR, skill_version_from_file
from src.report_renderer import EXPORT_NOTICE, to_json, to_markdown
from tests.conftest import ROOT, TODAY

REQUIRED_SECTIONS = [
    "## Purpose and triggers", "## Do not use when", "## Inputs", "## Outputs", "## Procedure",
    "## Decision rules", "## Missing, ambiguous, conflicting or truncated input", "## Prompt-injection handling",
    "## Worked example", "## Negative / adversarial example", "## Acceptance checks",
]


@pytest.mark.parametrize("name", list(SKILL_VERSIONS))
def test_skill_file_contract(name):
    text = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
    fm = re.match(r"\A---\nname: (.+)\ndescription: (.+)\n---\n", text)
    assert fm, "YAML front matter with name and description required"
    skill_name, desc = fm.group(1).strip(), fm.group(2).strip()
    # Constraints from Anthropic's Agent Skills docs (checked 2026-10-08).
    assert re.fullmatch(r"[a-z0-9-]{1,64}", skill_name) and skill_name == name
    assert "anthropic" not in skill_name and "claude" not in skill_name
    assert 0 < len(desc) <= 1024 and "<" not in desc and ">" not in desc
    for sec in REQUIRED_SECTIONS:
        assert sec in text, (name, sec)
    assert skill_version_from_file(name) == SKILL_VERSIONS[name]


def test_nine_skills_exist():
    assert len(SKILL_VERSIONS) == 9
    assert all((SKILLS_DIR / n / "SKILL.md").exists() for n in SKILL_VERSIONS)
    assert set(MODEL_SKILLS) < set(SKILL_VERSIONS)


def test_committed_schemas_match_models():
    for name, schema in build_schemas().items():
        on_disk = json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))
        assert on_disk == json.loads(json.dumps(schema)), f"{name} is stale: run python -m src.export_schemas"


def test_report_validates_against_json_schema_and_registry_schema():
    r = run_demo("04_university_bundled_publicity", today=TODAY)
    jsonschema.validate(json.loads(to_json(r)), json.loads((SCHEMA_DIR / "report.schema.json").read_text()))
    reg = json.loads((ROOT / "rules" / "legal_sources.json").read_text(encoding="utf-8"))
    jsonschema.validate(reg, json.loads((SCHEMA_DIR / "source_registry.schema.json").read_text()))


def test_markdown_export_has_required_sections_and_notice():
    md = to_markdown(run_demo("01_delivery_overreach", today=TODAY))
    for s in ["## Overall:", "## Plain-English summary", "## Data inventory", "## Permission-purpose map",
              "## Consent-design review", "## Findings", "## Legal sources", "## Limitations", "## Skills run"]:
        assert s in md
    assert EXPORT_NOTICE in md and "DEMO" in md


def test_no_real_credentials_in_repo_fixtures():
    pat = re.compile(r"sk-ant-[A-Za-z0-9_-]{10,}|\b[2-9]\d{3}\s?\d{4}\s?\d{4}\b|\b[A-Z]{5}\d{4}[A-Z]\b")
    for p in list((ROOT / "examples").rglob("*")) + [ROOT / ".env.example"]:
        if p.is_file():
            assert not pat.search(p.read_text(encoding="utf-8")), p
    for p in (ROOT / "examples" / "synthetic_policies").glob("*.md"):
        assert "SYNTHETIC" in p.read_text(encoding="utf-8")


# ---- Streamlit app: demo run and reset ------------------------------------------------
def test_app_demo_then_reset_clears_session():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.run()
    assert not at.exception
    next(b for b in at.button if b.label == "Run demo analysis").click().run()
    assert at.session_state["report"] is not None
    assert at.session_state["prepared"] is not None
    nonce = at.session_state["uploader_nonce"]
    next(b for b in at.sidebar.button if b.label == "Reset and clear session").click().run()
    assert "report" not in at.session_state or at.session_state["report"] is None
    assert "prepared" not in at.session_state
    assert at.session_state["qa"] == []
    assert at.session_state["uploader_nonce"] == nonce + 1
    assert not at.exception


def test_app_demo_tab_keeps_report_and_followup_document_in_sync():
    """Regression: a demo started from the last tab must not leave Report/Ask on a stale document."""
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.run()
    at.button(key="demo_07_prompt_injection").click().run()
    at.button(key="demo_01_delivery_overreach").click().run()
    rep, prep = at.session_state["report"], at.session_state["prepared"]
    assert [p.text for p in rep.evidence] == [p.text for p in prep.all_paragraphs]
    at.text_input[0].input("How long do they keep my data?").run()
    next(b for b in at.button if b.label == "Ask").click().run()
    assert "P014" in at.session_state["qa"][0].evidence_ids
    assert not at.exception

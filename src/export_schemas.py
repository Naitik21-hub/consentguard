"""Generate JSON Schemas in schemas/ from the Pydantic models.

Run:  python -m src.export_schemas
Tests check that the committed schemas match the models.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from pydantic import BaseModel, TypeAdapter

from .models import (
    AnalysisDraft,
    DraftFinding,
    Finding,
    IntakeResult,
    LegalSource,
    Paragraph,
    QAAnswer,
    Report,
    SkillRun,
    SuppliedContext,
)

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"


class SourceRegistry(BaseModel):
    registry_version: str
    last_verification_date: str
    verification_method: str
    important_note: str
    sources: list[LegalSource]


def build_schemas() -> Dict[str, dict]:
    return {
        "intake.schema.json": {"title": "Intake", "type": "object", "properties": {
            "supplied_context": SuppliedContext.model_json_schema(), "intake_result": IntakeResult.model_json_schema()}},
        "evidence.schema.json": TypeAdapter(list[Paragraph]).json_schema(),
        "analysis_draft.schema.json": AnalysisDraft.model_json_schema(),
        "draft_finding.schema.json": DraftFinding.model_json_schema(),
        "finding.schema.json": Finding.model_json_schema(),
        "skill_run.schema.json": SkillRun.model_json_schema(),
        "legal_source.schema.json": LegalSource.model_json_schema(),
        "source_registry.schema.json": SourceRegistry.model_json_schema(),
        "report.schema.json": Report.model_json_schema(),
        "qa_answer.schema.json": QAAnswer.model_json_schema(),
    }


def main() -> None:
    SCHEMA_DIR.mkdir(exist_ok=True)
    for name, schema in build_schemas().items():
        (SCHEMA_DIR / name).write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
        print("wrote", SCHEMA_DIR / name)


if __name__ == "__main__":
    main()

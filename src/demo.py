"""Load synthetic demo scenarios and their pre-authored fixture drafts."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

from .document_parser import parse_pasted
from .models import AnalysisDraft, Report, SuppliedContext
from .orchestrator import PreparedDocument, analyze, run_intake

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def list_scenarios() -> List[Dict]:
    return json.loads((EXAMPLES / "scenarios.json").read_text(encoding="utf-8"))["scenarios"]


def get_scenario(scenario_id: str) -> Dict:
    for s in list_scenarios():
        if s["id"] == scenario_id:
            return s
    raise KeyError(scenario_id)


def scenario_text(scenario: Dict) -> str:
    return (EXAMPLES / scenario["policy_file"]).read_text(encoding="utf-8")


def scenario_draft(scenario_id: str) -> AnalysisDraft:
    path = EXAMPLES / "expected_outputs" / f"{scenario_id}.draft.json"
    return AnalysisDraft.model_validate_json(path.read_text(encoding="utf-8"))


def prepare_scenario(scenario_id: str) -> PreparedDocument:
    s = get_scenario(scenario_id)
    return run_intake(parse_pasted(scenario_text(s)), SuppliedContext(**s["context"]))


def run_demo(scenario_id: str, today: Optional[date] = None) -> Report:
    return analyze(prepare_scenario(scenario_id), mode="demo", draft=scenario_draft(scenario_id), today=today)

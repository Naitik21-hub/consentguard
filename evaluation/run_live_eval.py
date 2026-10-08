"""OPTIONAL live-model evaluation. Not part of the default test suite.

Runs every synthetic scenario through LIVE mode (real API calls, real cost) and
compares the validated report with examples/expected_outputs/expected_outcomes.json.
It also writes a blank human-review rubric for each scenario.

Usage (from the consentguard folder, with ANTHROPIC_API_KEY set):
    python -m evaluation.run_live_eval            # all scenarios
    python -m evaluation.run_live_eval 01_delivery_overreach

Cost: roughly 8 analysis calls. Each sends up to ~8k input tokens and receives up to 32k
output tokens. Check current pricing for your chosen model before running.
Results go to evaluation/results/<timestamp>/ (git-ignored). Only synthetic documents are sent.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.demo import list_scenarios, prepare_scenario  # noqa: E402
from src.llm_client import LLMError, api_key_present, configured_model  # noqa: E402
from src.orchestrator import analyze  # noqa: E402
from src.report_renderer import to_json, to_markdown  # noqa: E402

RUBRIC = """# Human review rubric: {sid}

Score each 1 (poor) to 3 (good). Write one sentence of evidence for each score.

| Criterion | What good looks like | Score | Evidence |
|---|---|---|---|
| Grounding | Every finding quotes the document; no invented company facts | | |
| Completeness | Covers data, purposes, recipients, retention, choices, permissions | | |
| Uncertainty handling | Unknowns are stated; absences are not treated as wrongdoing | | |
| Actionability | Next steps are specific, user-controlled, conditional where needed | | |
| Clarity | A non-expert can follow it in under 3 minutes | | |

Reviewer: ______  Date: ______
"""


def main(ids: list[str]) -> int:
    if not api_key_present():
        print("ANTHROPIC_API_KEY is not set. This optional evaluation makes real API calls; set the key in .env first.")
        return 2
    expected = json.loads((ROOT / "examples/expected_outputs/expected_outcomes.json").read_text(encoding="utf-8"))["scenarios"]
    out = ROOT / "evaluation" / "results" / datetime.now().strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True)
    summary = []
    for s in list_scenarios():
        sid = s["id"]
        if ids and sid not in ids:
            continue
        exp = expected[sid]
        t0 = time.time()
        try:
            r = analyze(prepare_scenario(sid), "live")
        except LLMError as e:
            summary.append({"scenario": sid, "status": "error", "error": str(e)})
            print(f"{sid}: ERROR {e}")
            continue
        rules = {f.rule_id for f in r.findings}
        row = {
            "scenario": sid,
            "status": "ok",
            "seconds": round(time.time() - t0, 1),
            "model": r.model_id,
            "overall_expected": exp["overall"],
            "overall_actual": r.overall_assessment,
            "overall_match": r.overall_assessment == exp["overall"],
            "missing_required_rules": sorted(set(exp["must_include_rules"]) - rules),
            "forbidden_rules_present": sorted(set(exp["must_not_include_rules"]) & rules),
            "validation_adjustments": [c.detail for c in r.validation if not c.passed],
        }
        summary.append(row)
        (out / f"{sid}.report.json").write_text(to_json(r), encoding="utf-8")
        (out / f"{sid}.report.md").write_text(to_markdown(r), encoding="utf-8")
        (out / f"{sid}.rubric.md").write_text(RUBRIC.format(sid=sid), encoding="utf-8")
        print(f"{sid}: overall {r.overall_assessment} (expected {exp['overall']}); missing {row['missing_required_rules']}; "
              f"forbidden {row['forbidden_rules_present']}; {len(row['validation_adjustments'])} validation adjustment(s)")
    (out / "summary.json").write_text(json.dumps({"model": configured_model(), "results": summary}, indent=2), encoding="utf-8")
    print("Results written to", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

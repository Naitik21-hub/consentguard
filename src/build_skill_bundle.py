"""Package the skill library.

Run:  python -m src.build_skill_bundle

Creates:
* dist/skills/<skill>.zip  - one folder per skill containing SKILL.md, for upload
  in claude.ai (Settings > Capabilities/Features > Skills) or the Skills API.
* skills/fallback/ConsentGuard_skills_plain.md - all nine skills plus the rule
  table as one plain Markdown file to paste or attach in an ordinary Claude chat.
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

from . import rules as R
from .orchestrator import SKILL_VERSIONS

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
DIST = ROOT / "dist" / "skills"
FALLBACK = SKILLS / "fallback" / "ConsentGuard_skills_plain.md"

FALLBACK_HEADER = """# ConsentGuard skill library (plain Markdown fallback)

Use this file in an ordinary Claude chat that does not support installable Skills.
Attach or paste it, then paste the privacy text inside <document>...</document> tags and say:
"Run the ConsentGuard skills on this document. Number paragraphs P001, P002... first."

Notes:
- These are custom prompt modules. Without the ConsentGuard app, the code-executed checks
  (quote verification, severity caps, legal-registry lookup) are performed by Claude following
  the instructions, NOT by deterministic code. Results are therefore less reliable than the app.
- Legal sources: only cite entries from the registry summary at the end; anything else is "not verified".
"""


def strip_frontmatter(text: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)


def main() -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    parts = [FALLBACK_HEADER]
    for name in SKILL_VERSIONS:
        skill_md = SKILLS / name / "SKILL.md"
        with zipfile.ZipFile(DIST / f"{name}.zip", "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(skill_md, arcname=f"{name}/SKILL.md")
        parts.append("\n\n---\n\n" + strip_frontmatter(skill_md.read_text(encoding="utf-8")))
        print("packaged", DIST / f"{name}.zip")

    reg = R.load_legal_registry()
    parts.append("\n\n---\n\n# Canonical rule table\n\n```\n" + R.rules_prompt_table() + "\n```\n")
    parts.append(f"\n# Legal source registry summary (verified {reg['last_verification_date']})\n")
    for s in reg["sources"]:
        parts.append(f"- {s['source_id']} | {s['title']} | effective {s['effective_date']} | {s['verification_status']} | {s['official_url']}")
    FALLBACK.parent.mkdir(exist_ok=True)
    FALLBACK.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print("wrote", FALLBACK)


if __name__ == "__main__":
    main()

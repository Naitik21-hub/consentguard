# ConsentGuard skill library

Nine reusable skills that turn "read this privacy policy" into a repeatable, evidence-grounded governance workflow. They work together in the ConsentGuard app, and you can also use them on their own in Claude.

| # | Folder | Skill | Executor in the app | Main output |
|---|---|---|---|---|
| 1 | `document-intake` | Document Intake and Scope | code | `IntakeResult`, paragraph IDs |
| 2 | `evidence-extraction` | Policy Evidence Extraction | model | `data_inventory`, quotes |
| 3 | `plain-language-explanation` | Plain-Language Explanation | model | `plain_english_summary` |
| 4 | `purpose-proportionality` | Purpose and Proportionality Assessment | model | `permission_purpose_map`, CG-PP findings |
| 5 | `consent-design-review` | Consent Design Review | model, then a code guard | `consent_dimensions`, CG-CN findings |
| 6 | `jurisdiction-check` | Jurisdiction and Source Check | code | legal source IDs and applicability |
| 7 | `findings-prioritization` | Findings Prioritization | code | severity/confidence caps, overall label |
| 8 | `user-action-plan` | User Action Plan | model, merged with rule defaults | `next_steps`, `targeted_questions` |
| 9 | `report-and-qa` | Report Generation and QA | code (plus a model for live Q&A) | validated `Report`, `QAAnswer` |

Pipeline: `intake -> extraction -> (plain-language | proportionality | consent design | action plan) -> jurisdiction check -> prioritization -> report & QA`.

## How the app actually uses these files (not decorative)

- **Model-executed skills (2, 3, 4, 5, 8):** at run time, `src/orchestrator.py::build_system_prompt` reads the `## Procedure` and `## Decision rules` sections of each of these SKILL.md files and adds them to the system prompt, followed by the rule table generated from `rules/governance_rules.json`. If you edit a skill's procedure, live mode changes with it.
- **Code-executed skills (1, 6, 7, 9):** the SKILL.md is the specification and the named Python functions are the implementation. `tests/test_skills_schemas_app.py` checks that each file's `Skill version:` matches `SKILL_VERSIONS` in the orchestrator, and every report records the version of each skill that ran (`skills_run`).
- **One rule source:** severity caps, rule IDs, permission guidance, and banned wording live **only** in `rules/governance_rules.json`. Legal sources live **only** in `rules/legal_sources.json`. Skills refer to these files and never keep their own copies.

## Two kinds of "skill"

1. **Custom reusable prompt modules.** The Markdown content is portable to any LLM chat. Use the plain fallback `fallback/ConsentGuard_skills_plain.md`, which `python -m src.build_skill_bundle` generates.
2. **Platform-installable Claude Skills.** These are the same files packaged in Anthropic's Agent Skills format: a folder containing `SKILL.md` with YAML front matter `name` (lowercase letters, numbers, and hyphens, at most 64 characters, without the words "anthropic" or "claude") and `description` (at most 1024 characters, no XML tags). These constraints were checked against Anthropic's Agent Skills overview on 2026-10-08 and are enforced by tests.

## Install or use

| Where | How | Tested in this build? |
|---|---|---|
| Claude Code | Copy each `skills/<name>/` folder into `~/.claude/skills/` or `<project>/.claude/skills/` | No |
| claude.ai (Pro, Max, Team, or Enterprise with code execution) | `python -m src.build_skill_bundle`, then upload each `dist/skills/<name>.zip` in Settings. Skills are per user. | No |
| Claude API (Skills API) | Upload via `/v1/skills` and use with the code execution tool (see Anthropic docs) | No |
| Ordinary Claude chat | Attach `fallback/ConsentGuard_skills_plain.md`, paste the document in `<document>` tags, and ask Claude to run the skills | No (format only) |

**Important difference:** outside the app, code-executed checks (exact-quote verification, severity caps, registry lookup) are carried out by Claude *following the instructions*, not by deterministic code. Treat those results as less reliable, and verify quotes yourself.

## Standalone examples

- "Use `purpose-proportionality` to judge whether a food-delivery app needs my contacts. Here is the permission text: ..."
- "Run `consent-design-review` on this registration form. I have no consent-screen text."
- "Use `jurisdiction-check`: which DPDP provisions are in force today for a consent finding?" Without the registry file, the skill marks this `not_verified`.

## Contract summary (every SKILL.md has these sections)

Front matter (name, description), skill version, purpose and triggers, when not to use it, required and optional inputs, outputs with a schema reference, ordered procedure, decision rules, handling of missing, ambiguous, conflicting, or truncated input, prompt-injection handling, a worked synthetic example with its expected output, a negative or adversarial example, and acceptance checks.

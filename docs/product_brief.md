# ConsentGuard: Product Brief

**Tagline:** Understand what you are agreeing to.
**Topic:** Information Appropriateness and Consent Governance
**Stage:** Working prototype (consumer education), India-first, built 2026-10-08

## Problem
People in India accept privacy notices, consent forms, and app permissions every day without knowing what data is requested, why, who receives it, how long it is kept, or how to withdraw. Notices are long or vague, and the link between a permission and the feature it supposedly serves is often unclear. India's Digital Personal Data Protection framework was notified in November 2025, but its consent and notice duties phase in only in May 2027. Users need help now, and they need it in a way that does not overstate what the law currently requires.

## Target users
- **Primary:** smartphone users in India deciding whether to install an app, sign a form, or grant a permission. They are not privacy experts.
- **Secondary:** students and educators learning information-governance methods; small organisations that want to see how their own notice reads to a consumer.

## Solution
An AI agent and a reusable skill library:
- **The agent** (a Streamlit app) takes a document plus optional context, previews and redacts it locally, and, only after explicit confirmation, sends it for analysis. It returns a validated report: plain-English summary, permission-purpose map, consent-design review, prioritised findings with exact quotes, verified legal context, and user-controlled next steps. It then answers follow-up questions grounded in the document.
- **The skill library** contains nine Markdown skills with schemas and one canonical rule file. They can be used inside the app, installed in Claude, or pasted into any chat.

## Value
| For | Value |
|---|---|
| Consumers | Know what you are agreeing to in about 3 minutes, with evidence you can check, plus specific questions and settings to try |
| Students | A transparent, testable governance workflow that separates "says / infers / law / unknown" |
| Organisations | See how a notice reads to a consumer before publishing it (not a compliance check) |

## What makes it trustworthy
1. **Evidence first:** every substantive finding links to paragraph IDs, and quotes are checked character for character against the submitted text.
2. **Honest uncertainty:** missing information lowers confidence and is never treated as proof of wrongdoing.
3. **Law kept separate:** legal sources come only from an officially verified registry, with an in-force status, never from model memory.
4. **Practises what it preaches:** session-only storage, preview before sending, local redaction, no analytics, and a reset button.

## Scope (MVP)
In scope: pasted text, .txt, .md, and text-based PDFs; India legal registry; eight synthetic demos; Markdown and JSON export; grounded follow-ups.
Out of scope (future): OCR, URL crawling, automatic permission discovery from app stores, policy-change monitoring, other jurisdictions' registries, multilingual output (Hindi and other Eighth Schedule languages).

## Measurable success criteria (measurable in this prototype)
| Measure | How measured | Current observed result (2026-10-08) |
|---|---|---|
| Demo scenarios match expected overall label | `tests/test_scenarios.py` | 8 of 8 |
| Findings with verified evidence | Validation checks in each report | 100% in demo fixtures |
| Banned wording in generated output | Automated test | 0 occurrences |
| Fabricated quotes reaching the user | Mocked adversarial tests | 0 (all removed or marked unverified) |
| Live-mode agreement with expected outcomes | `evaluation/run_live_eval.py` | **Not yet measured** (no API key in build environment) |
| Human rubric (grounding, completeness, uncertainty, actionability, clarity) | `docs/evaluation.md` rubric | **Not yet scored** |
| Time to understand a notice | User test with a stopwatch (target under 3 minutes) | Not yet measured |

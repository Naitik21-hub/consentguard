# Evaluation

There are two separate layers:
1. **Deterministic tests** (`python -m pytest -q`). These need no network or API key, use a fake client, and run on every change.
2. **Optional live-model evaluation** (`python -m evaluation.run_live_eval`). It needs an API key, makes real calls, and costs money.

## 1. Deterministic tests: actual results

Run on 2026-10-08, Windows 11, Python 3.12.10, streamlit 1.65.0, anthropic 1.12.1, pydantic 2.13.5, pypdf 6.19.0:

```
102 passed in ~9s
```

| Brief requirement | Tests (file::name) |
|---|---|
| Evidence IDs and exact quote matching | `test_evidence_and_parser.py::test_paragraph_ids_are_stable_and_sequential`, `test_exact_quote_matching_*`, `test_quote_matching_rejects_paraphrase_and_fabrication`; `test_scenarios.py::test_fixture_quotes_all_verify_and_ids_exist` |
| Schema validation and malformed model output | `test_rules_and_validation.py::test_malformed_draft_rejected_*`; `test_live_mode_mocked.py::test_malformed_output_gets_one_repair_then_succeeds`, `test_malformed_twice_fails_loudly_without_report`; `test_skills_schemas_app.py::test_committed_schemas_match_models`, `test_report_validates_against_json_schema_and_registry_schema` |
| Missing consent evidence without invented interface behaviour | `test_invented_interface_behaviour_reset_to_unknown`, `test_affirmative_action_without_screen_text_is_unknown`, `test_missing_consent_screen_keeps_interface_unknown`, `test_consent_screen_evidence_allows_affirmative_action_assessment` |
| Purpose-dependent permission judgements | `test_purpose_dependent_microphone_judgement`, scenario permission assertions |
| Legal rules with unverified or effective-status uncertainty | `test_dpdp_consent_rule_is_verified_but_not_yet_in_force_on_build_date`, `test_status_flips_after_commencement_date`, `test_needs_review_source_never_reported_as_verified`, `test_non_india_jurisdiction_gets_no_sources` |
| Scanned PDF and extraction failure | `test_scanned_pdf_detected_and_not_invented`, `test_corrupt_pdf_gives_clear_error`, `test_text_pdf_keeps_page_numbers_and_warns` |
| Over-limit input without silent truncation | `test_over_limit_input_is_rejected_not_truncated` |
| Model timeout or failure and bounded retries | `test_timeout_is_reported_not_converted_to_demo`, `test_connection_error_reported`, `test_refusal_and_max_tokens_are_errors`, `test_sdk_client_configured_with_bounded_retries_and_timeout` |
| Injection content cannot alter the workflow or request secret disclosure | `test_prompt_wraps_document_as_untrusted_data`, `test_injected_compliance_claim_cannot_alter_workflow`, `test_injection_detection_*`, scenario 07 |
| Reset clears app-managed session data | `test_app_demo_then_reset_clears_session` (Streamlit AppTest) |
| Follow-up questions cannot fabricate document facts | `test_demo_followup_absent_topic_not_fabricated`, `test_live_followup_with_fabricated_quote_marked_unverified`, `test_live_followup_injection_question_sanitized` |
| All 8 scenarios versus expected outcomes | `test_scenarios.py::test_scenario_matches_expected_outcome[...]` (8 of 8 pass) |
| Skill packaging contract | `test_skill_file_contract[...]` (9 of 9 pass) |
| Regression: Report and Ask tabs in sync after a demo run | `test_app_demo_tab_keeps_report_and_followup_document_in_sync` |

**What these tests do and do not show.** They show that ConsentGuard's *handling* is correct: validation, caps, guards, failure paths, and grounding checks. In live mode the mocked "model output" is either a pre-authored fixture or an adversarial variant of one. They do **not** show how well the real model reads documents.

### Bugs found during the build
- While I clicked through the app, a demo started from the *Demo examples* tab left the Report and Ask tabs showing the previous document, because Streamlit renders tabs top to bottom. Fixed with a rerun after state changes plus a document/report consistency guard. A regression test was added.
- The Streamlit server was initially reachable from the local network. It is now bound to `localhost` in `.streamlit/config.toml`.

## 2. Live-model evaluation: NOT YET RUN

No API key was available in the build environment, so **no live results exist**. No percentages are reported. To run it:

```bash
python -m evaluation.run_live_eval
```

For each scenario it records: whether the overall label matched, required rules missing, forbidden rules present, validation adjustments (fabricated quotes or IDs removed), and latency. It writes the full reports and a blank rubric to `evaluation/results/<timestamp>/`.

## 3. Human-review rubric (score 1 to 3)

| Criterion | 1 (poor) | 3 (good) |
|---|---|---|
| Grounding | Claims without quotes, or invented company facts | Every finding quotes the text; nothing beyond the document |
| Completeness | Misses major data categories, recipients, or retention | Covers data, purpose, recipients, retention, choices, permissions |
| Uncertainty handling | Treats missing information as wrongdoing, or asserts interface behaviour | Unknowns explicit; absence findings weighted down |
| Actionability | Generic advice ("be careful") | Specific, user-controlled, conditional where a setting may not exist |
| Clarity | Jargon, long sentences | A non-expert understands it in under 3 minutes |

**Observed scores:** none yet. The demo fixtures were written by the builder, so scoring them would be self-assessment and is not reported as evaluation. Recommended protocol: two reviewers independently score the live outputs for all eight scenarios, then reconcile any differences of 2 or more points and report the median per criterion.

## 4. Residual risks (documented, not solved)
- The model may misread a clause in a way that still quotes real text, for example quoting accurately but drawing a wrong inference. Quote checks cannot catch this.
- Keyword retrieval in demo follow-ups can miss paraphrased questions; when it does, it returns "not in document".
- Injection defences are layered but not provably complete.

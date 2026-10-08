# Legal Source Verification

**Last verification:** 2026-10-08 (build date).
**Method:** Official PDFs were downloaded from `meity.gov.in` and `static.pib.gov.in` and read directly, using text extraction. General web searches (with no user content) were used only to locate the official URLs. No law-firm summaries, blogs, or drafts are treated as controlling.

## What was verified

| Registry ID | Source | Key verified facts |
|---|---|---|
| LS-IN-DPDPA-COMMENCE | G.S.R. 843(E), MeitY, dated 13 Nov 2025 ([PDF](https://www.meity.gov.in/static/uploads/2025/11/c56ceae6c383460ca69577428d36828b.pdf)) | (a) In force on publication: s.1(2), s.2, ss.18-26, s.35, ss.38-43, s.44(1),(3). (b) One year after: s.6(9), s.27(1)(d). (c) Eighteen months after: ss.3-5, s.6(1)-(8),(10), ss.7-17, s.27 (except (1)(d)), ss.28-34, 36, 37, s.44(2). |
| (context) | G.S.R. 844(E), dated 13 Nov 2025 ([PDF](https://www.meity.gov.in/static/uploads/2025/11/cc217843dc3bcb37b2b05bcc3b4e031f.pdf)) | Data Protection Board of India established from publication, with its head office in the NCR. |
| LS-IN-DPDPA-S4/S5/S6/S7/S8-7/S11/S13 | DPDP Act 2023 (No. 22 of 2023), Gazette 11 Aug 2023 ([PDF](https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf)) | s.4: consent **or** certain legitimate uses. s.5: notice contents. s.6(1): free, specific, informed, unconditional, unambiguous consent with a clear affirmative action, limited to necessary data (the illustration says contacts are not necessary for telemedicine). s.6(4): withdrawal must be comparable in ease to giving consent. s.7: legitimate uses. s.8(7): erasure. s.11: access, including the identities of recipients. s.13: grievance redressal. s.44(2)(a): omits IT Act s.43A. |
| LS-IN-DPDP-RULES / RULE3 / RULE8 | DPDP Rules 2025, G.S.R. 846(E), Gazette Extraordinary No. 760, 13 Nov 2025 ([PDF](https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf)) | Rule 1: rules 1, 2, and 17-21 on publication; rule 4 after one year; rules 3, 5-16, 22, and 23 after eighteen months. Rule 3: notice must be standalone, use plain language, give an itemised description of data and purposes, and provide a link to withdraw consent. Rule 8: Third Schedule erasure periods, and processing logs kept for at least one year. |
| LS-IN-PIB-EXPLAINER | PIB explainer, 17 Nov 2025 ([PDF](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf)) | States the Rules were notified on 14 Nov 2025, with an eighteen-month phased period and a 90-day response time for rights requests. This is an explainer, not law. |

## Resulting status on 2026-10-08
- The DPDP Act's definitions and Board provisions are **in force**.
- Notice, consent, legitimate-use, obligation, and rights provisions (ss.3-17) are **verified but not yet in force**. They commence eighteen months after publication, computed as **2027-05-13**.
- Consent-manager registration (s.6(9), rule 4) commences one year after publication, computed as **2026-11-13**.
- ConsentGuard therefore labels DPDP-linked findings `verified_not_yet_in_force` and presents them as context, not as current obligations.

## Open items: needs review
1. **Exact commencement day.** The notifications are dated 13 Nov 2025. The e-Gazette IDs (CG-DL-E-14112025-...) and PIB say 14 Nov. The computed dates use 13 Nov. A qualified reviewer should confirm.
2. **Interim regime.** IT Act s.43A and the SPDI Rules 2011 continue until s.44(2) commences. Their current text was **not** retrieved, so the registry marks them `needs_review` and they never appear as verified findings.
3. **Sector rules** (RBI, SEBI, IRDAI, health, telecom) are not in the registry. Bank and fitness scenarios therefore make no sector-law claims.
4. **Third Schedule classes and periods** (rule 8) were not itemised in the registry.

## Re-verification checklist (do this at least every 90 days, and before any demo after 2026-11-13)
- [ ] Open the MeitY DPDP page and the e-Gazette. Search "Digital Personal Data Protection" for new notifications, amendments, or corrigenda.
- [ ] Re-download the Act, G.S.R. 843(E), and G.S.R. 846(E). Check that the URLs still resolve and the text is unchanged.
- [ ] Check for any notification changing the commencement dates.
- [ ] Update `effective_date`, `verification_status`, and `retrieval_date` in `rules/legal_sources.json`, and update `last_verification_date`.
- [ ] Run `python -m pytest -q`. The rule-status tests will show whether statuses changed.
- [ ] Use only official government or regulator sources. Mark anything else `needs_review`.
- [ ] Never send user documents to search services; use general queries only.

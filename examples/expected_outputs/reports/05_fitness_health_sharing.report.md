# ConsentGuard report: FitPulse Privacy Notice (synthetic)

> This export contains quotations from the text you submitted. Share it only if you are comfortable sharing those quotations.
> **DEMO: pre-authored demonstration output for a synthetic document, validated by the live pipeline. Not live AI analysis.**

- Report ID: `CG-9AAB0E35C5`  |  Analyzed: 2026-10-08T10:29:14+00:00  |  Mode: demo
- Document version: unknown  |  Jurisdiction: IN  |  Completeness: complete
- Rule set v1.0.0  |  Legal sources last verified: 2026-10-08

## Overall: Substantial concerns found
1 high-severity finding(s) are supported by quoted text (F01).

*ConsentGuard does not certify safety or legal compliance. It explains the supplied text only.*

## Plain-English summary

**Data collected**
- Age, height, weight, steps, heart rate, sleep patterns and, if you choose to log it, menstrual cycle information. [P004]
- Continuous heart-rate readings if you connect a wearable. [P005]

**Purposes**
- Showing fitness trends and personalised workout suggestions. [P007]
- Partners, including insurers, may use your data to offer personalised plans and premiums. [P009]

**Who receives it**
- Wellness partners, including insurance companies, receive health and activity data. [P009]
- Research organisations receive aggregated statistics that FitPulse says do not identify you. [P010]

**How long it is kept**
- Kept while your account is active and for 2 years after your last login. [P012]

**Your choices and how to withdraw**
- You can stop wearable syncing in settings and delete your account by email. No choice about partner sharing is described. [P014]

**Unknown or missing in the supplied text**
- Whether sharing with insurers is optional or can be refused.
- Which insurers or partners receive data.
- Whether partners delete data when you leave FitPulse.

## Data inventory
| Data | Basis | Purpose | Recipients | Retention | Evidence |
|---|---|---|---|---|---|
| Body measurements, steps, heart rate, sleep | stated | Fitness trends and suggestions; partner offers and premiums | Wellness partners including insurers | Account life + 2 years after last login | P004, P007, P009, P012 |
| Menstrual cycle information (optional logging) | stated | Fitness trends (implied); possibly partner sharing as 'health data' | Possibly wellness partners including insurers | Account life + 2 years after last login | P004, P009 |
| Continuous heart rate from wearable | stated | Fitness trends | Possibly wellness partners | Account life + 2 years after last login | P005, P012 |

## Permission-purpose map
| Permission | Feature | Scope | Required? | Assessment | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| Wearable heart-rate sync | Fitness tracking | Continuous while connected | optional | Appears proportionate to the stated purpose: Continuous heart rate fits a fitness-tracking feature you choose to connect, and syncing can be stopped in settings. | Do not connect a wearable; Stop syncing in Settings > Devices | P005, P014 |
| Sharing health data with insurers | Partner plans and premiums | Health and activity data | unknown | Needs explanation or narrower scope: Insurer use is a separate purpose from fitness tracking and could affect your premiums. The notice gives no separate choice. | Separate opt-in for insurer sharing; Share only aggregated data | P009 |

## Consent-design review
- **Clarity and specificity of purposes**: adequate. Purposes are specific, including the insurer purpose. [P007, P009]
- **Separation of optional uses from essential processing**: concern. Insurer sharing is not described as optional. [P009]
- **Granularity of choices**: concern. Choices exist for wearable syncing, but none for partner sharing. [P014]
- **Evidence of affirmative user action**: unknown. The consent screen was not supplied. [none]
- **Ease and availability of withdrawal**: concern. You can stop syncing or delete your account, but the notice gives no route to stop partner sharing. [P014]
- **Transparency about recipients and retention**: concern. Retention is stated, but partners are described only by type. [P009, P012]
- **Bundling, coercion, confusing wording, or misleading choices**: unknown. It is unclear whether partner sharing is a condition of using the app. [none]

## Findings

### F01. Health data shared with insurers, with no separate choice described
- Severity: **high** | Confidence: **high** | Rule: CG-SH-01 v1.0
- Evidence basis: quoted | Document evidence: P009, P014
- Legal context: verified not yet in force (LS-IN-DPDPA-S6). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

The notice says health and activity data is shared with partners including insurers, who may use it for premiums, and describes no way to refuse this while still using the app.

> "We share your health and activity data with wellness partners, including insurance companies, who may use it to offer you personalised plans and premiums." (P009, exact quote verified)

Would change this assessment: Whether the app asks for separate agreement before insurer sharing

**Suggested action:** Ask FitPulse whether insurer sharing is optional and how to switch it off. Check the app's settings for a partner-sharing choice before logging sensitive data.

### F02. Sensitive-in-context health information
- Severity: **medium** | Confidence: **high** | Rule: CG-SN-01 v1.0
- Evidence basis: quoted | Document evidence: P004, P009
- Legal context: no legal reference (none). This is a governance heuristic with no linked legal source.

Heart rate, sleep and menstrual cycle data are things many people consider sensitive, especially when they may reach insurers. This is a general sensitivity concern. ConsentGuard does not decide how the law classifies this data.

> "if you choose to log it, menstrual cycle information" (P004, exact quote verified)

**Suggested action:** Consider logging only the data you need; menstrual cycle logging is described as optional.

### F03. No route to stop partner sharing
- Severity: **medium** | Confidence: **medium** | Rule: CG-CN-02 v1.0
- Evidence basis: absence in supplied text | Document evidence: none
- Legal context: verified not yet in force (LS-IN-DPDPA-S6, LS-IN-DPDP-RULE3). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

The notice explains how to stop wearable syncing and delete your account, but not how to withdraw from partner sharing.

Would change this assessment: In-app privacy settings

**Suggested action:** Ask how to withdraw from partner sharing without deleting your account.

### F04. Retention period and research aggregation are stated
- Severity: **informational** | Confidence: **high** | Rule: CG-PO-01 v1.0
- Evidence basis: quoted | Document evidence: P010, P012
- Legal context: no legal reference (none). This is a governance heuristic with no linked legal source.

The notice gives a concrete retention period and says research partners receive only aggregated statistics.

> "for 2 years after your last login" (P012, exact quote verified)

**Suggested action:** No action needed for this point.

## Questions to ask the organisation
- Is sharing my health data with insurance companies optional? How do I turn it off? *(Why: Insurer use could affect the price or terms you are offered.)*
- Which insurers receive my data, and do they delete it if I stop using FitPulse? *(Why: Onward recipients may keep data longer than FitPulse does.)*

## Suggested next steps (you decide)
- Before logging menstrual or other sensitive data, check whether partner sharing can be switched off. *(if available)*
- If you connect a wearable, remember you can stop syncing in Settings > Devices.
- Ask FitPulse whether insurer sharing is optional and how to switch it off. Check the app's settings for a partner-sharing choice before logging sensitive data. *(if available)*
- Consider logging only the data you need; menstrual cycle logging is described as optional. *(if available)*
- Ask how to withdraw from partner sharing without deleting your account. *(if available)*
- If you need a legal determination, ask a qualified privacy or legal professional; ConsentGuard does not provide one.

## Legal sources (India registry)
- **LS-IN-DPDPA-COMMENCE**: Notification G.S.R. 843(E) appointing commencement dates for the Digital Personal Data Protection Act, 2023. Ministry of Electronics and Information Technology (MeitY), Government of India. Provision: Paragraphs (a)-(c): phased commencement. Published 2025-11-13; effective 2025-11-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2025/11/c56ceae6c383460ca69577428d36828b.pdf
- **LS-IN-DPDP-RULE3**: Digital Personal Data Protection Rules, 2025, rule 3 - Notice given by Data Fiduciary. Ministry of Electronics and Information Technology (MeitY), Government of India. Provision: Rule 3. Published 2025-11-13; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf
- **LS-IN-DPDPA-S6**: Digital Personal Data Protection Act, 2023, section 6 - Consent. Parliament of India; text hosted by MeitY. Provision: Section 6(1)-(8) and (10). Published 2023-08-11; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf

## Evidence index
- **P004** (paragraph 4 (section: Data we collect)): FitPulse collects your age, height, weight, step count, heart rate, sleep patterns and, if you choose to log it, menstrual cycle information.
- **P009** (paragraph 9 (section: Sharing with partners)): We share your health and activity data with wellness partners, including insurance companies, who may use it to offer you personalised plans and premiums.
- **P010** (paragraph 10 (section: Sharing with partners)): We share aggregated statistics that do not identify you with research organisations.
- **P012** (paragraph 12 (section: Retention)): We keep your health data while your account is active and for 2 years after your last login.
- **P014** (paragraph 14 (section: Your choices)): You can stop wearable syncing at any time in Settings > Devices. To delete your account, email support@fitpulse.example.

## Limitations
- ConsentGuard explains and assesses the supplied text only. It does not know whether the organisation actually follows its policy.
- This is a consumer-education prototype, not legal advice, a compliance certification, or a security scan.
- Severity and confidence labels are prototype governance heuristics, not statutory classifications.
- A privacy notice alone cannot show how a consent screen behaves (for example, whether boxes are pre-ticked).
- Legal sources are limited to the India registry verified on the date shown; laws and commencement dates can change.
- No consent-screen text was supplied, so interface behaviour was not assessed.

## Skills run
| Skill | Version | Executor | Status | Note |
|---|---|---|---|---|
| document-intake | 1.0.0 | code | success | 14 paragraphs; parse quality good. |
| evidence-extraction | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| plain-language-explanation | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| purpose-proportionality | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| consent-design-review | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| user-action-plan | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| jurisdiction-check | 1.0.0 | code | success | Legal sources attached from registry only. |
| findings-prioritization | 1.0.0 | code | success | 0 finding(s) adjusted by rule caps. |
| report-and-qa | 1.0.0 | code | success | 3 validation check(s) recorded. |

## Validation checks
- [pass] all finding evidence IDs exist: 6 reference(s) checked.
- [pass] all retained quotes verified
- [pass] legal sources come from registry

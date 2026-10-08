# ConsentGuard report: QuickBasket Privacy Notice (synthetic)

> This export contains quotations from the text you submitted. Share it only if you are comfortable sharing those quotations.
> **DEMO: pre-authored demonstration output for a synthetic document, validated by the live pipeline. Not live AI analysis.**

- Report ID: `CG-C4C94924CA`  |  Analyzed: 2026-10-08T10:29:14+00:00  |  Mode: demo
- Document version: Synthetic v1 (2026)  |  Jurisdiction: IN  |  Completeness: complete
- Rule set v1.0.0  |  Legal sources last verified: 2026-10-08

## Overall: Substantial concerns found
3 high-severity finding(s) are supported by quoted text (F01, F02, F03).

*ConsentGuard does not certify safety or legal compliance. It explains the supplied text only.*

## Plain-English summary

**Data collected**
- Account details: name, mobile number, email address and delivery addresses. [P004]
- Precise location at all times, including when the app is closed, collected continuously in the background. [P005, P006]
- Access to your phone contacts and microphone is required. The notice says contacts are used, but it does not say what is collected through the microphone. [P005, P009, P010]

**Purposes**
- Delivering orders and processing payments. [P008]
- Broad purposes: 'improve our services', 'other business purposes' and 'a better experience', which do not say what the data is actually used for. [P006, P008, P010]
- Contacts are used to map your social network and to recommend the app to people you know. [P009]

**Who receives it**
- Partners, affiliates and other unnamed third parties, for marketing and analytics. [P012]

**How long it is kept**
- Kept 'for as long as we consider necessary'. No period or criteria are given. [P014]

**Your choices and how to withdraw**
- Continuing to use the app is treated as agreement. No way to refuse individual permissions or to withdraw is described. [P016, P005]

**Unknown or missing in the supplied text**
- How long location, contacts and any audio data are kept.
- Which partners receive data, and whether marketing sharing can be refused.
- How to withdraw consent or delete your account.
- What the consent screen looks like (not supplied).

## Data inventory
| Data | Basis | Purpose | Recipients | Retention | Evidence |
|---|---|---|---|---|---|
| Name, mobile number, email, delivery addresses | stated | Account, delivery and payments | Partners, affiliates, third parties (marketing and analytics) | As long as considered necessary | P004, P008, P012, P014 |
| Precise location (continuous, background) | stated | 'A better experience' | unknown | As long as considered necessary | P005, P006 |
| Phone contacts | stated | Social-network analysis and referrals | unknown | unknown | P005, P009 |
| Microphone audio | permission_only | 'Improve our services' | unknown | unknown | P005, P010 |

## Permission-purpose map
| Permission | Feature | Scope | Required? | Assessment | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| Precise location (always, background) | Delivery | Precise, continuous, also when the app is closed | required | Needs explanation or narrower scope: Location fits delivery, but a customer usually needs it only while placing or tracking an order. Background, always-on collection is justified only as 'a better experience'. | While-in-use location; Approximate location; Typing the delivery address | P005, P006 |
| Contacts | Referral / social network analysis | Whole contact list | required | Appears disproportionate to the stated purpose: Grocery delivery does not need your contact list. The stated use (social network analysis and recommending the app) serves the company, yet it is mandatory. | Share a referral link instead; Make contacts access optional | P005, P009 |
| Microphone | None described | Not stated | required | Appears disproportionate to the stated purpose: No voice feature is described. The only reason given is to 'improve our services', yet access is mandatory. If an optional voice-search feature existed, microphone access could fit it. | Type searches instead; Grant microphone only when using a voice feature, if one exists | P005, P010 |

## Consent-design review
- **Clarity and specificity of purposes**: concern. Several purposes are vague ('improve our services', 'other business purposes', 'a better experience'). [P006, P008, P010]
- **Separation of optional uses from essential processing**: concern. All permissions are presented as required; no optional uses are separated from delivery. [P005]
- **Granularity of choices**: concern. The text offers no separate choices for contacts, microphone or marketing sharing. [P005, P012]
- **Evidence of affirmative user action**: unknown. The notice treats continued use as agreement. Whether the app asks for a clear action cannot be seen without the consent screen. [P016]
- **Ease and availability of withdrawal**: concern. No withdrawal route is described in the notice. [P016]
- **Transparency about recipients and retention**: concern. Recipients are unnamed categories and retention is open-ended. [P012, P014]
- **Bundling, coercion, confusing wording, or misleading choices**: concern. Unrelated access is bundled with the core delivery service: the app will not work without it. [P005]

## Findings

### F01. Contacts and microphone made mandatory for grocery delivery
- Severity: **high** | Confidence: **high** | Rule: CG-PP-02 v1.0
- Evidence basis: quoted | Document evidence: P005, P009, P010
- Legal context: verified not yet in force (LS-IN-DPDPA-S6). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

The notice makes contacts and microphone access a condition of using the app, but neither is needed to deliver groceries. Contacts are used for social-network analysis and referrals; the microphone has no described feature.

> "If you do not allow these permissions the app will not work." (P005, exact quote verified)

> "Contacts are used to help us understand your social network" (P009, exact quote verified)

Would change this assessment: Whether the app in fact works if you deny these permissions on your device

**Suggested action:** Before agreeing, ask QuickBasket whether you can order without contacts and microphone access. If your phone lets you deny a permission, try denying these and see whether ordering still works.

### F02. Always-on background location justified only as 'a better experience'
- Severity: **high** | Confidence: **high** | Rule: CG-PP-03 v1.0
- Evidence basis: quoted | Document evidence: P005, P006
- Legal context: verified not yet in force (LS-IN-DPDPA-S6). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

Delivery can justify location while you order or track, but the notice requires precise location even when the app is closed, collected continuously, with only a vague reason.

> "precise location at all times, including when the app is closed" (P005, exact quote verified)

> "We collect location data continuously in the background to provide a better experience." (P006, exact quote verified)

Would change this assessment: Whether the app offers a while-in-use option

**Suggested action:** If your device allows it, choose 'while using the app' or approximate location. Ask why background location is needed for a customer.

### F03. Sharing with partners for marketing, with no separate choice described
- Severity: **high** | Confidence: **medium** | Rule: CG-SH-01 v1.0
- Evidence basis: quoted | Document evidence: P012, P016
- Legal context: verified not yet in force (LS-IN-DPDPA-S6). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

The notice says data may be shared with partners, affiliates and other third parties for marketing, and describes no way to refuse this separately from using the app.

> "We may share your information with our partners, affiliates and other third parties for marketing and analytics." (P012, exact quote verified)

Would change this assessment: Whether an opt-out exists in the app settings or consent screen

**Suggested action:** Look for a marketing or partner-sharing setting and decline it if you do not want it; ask QuickBasket how to opt out.

### F04. Agreement inferred from continued use
- Severity: **medium** | Confidence: **high** | Rule: CG-CN-03 v1.0
- Evidence basis: quoted | Document evidence: P016
- Legal context: verified not yet in force (LS-IN-DPDPA-S6). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

The notice treats using the app as agreement, instead of describing a clear choice by you.

> "By continuing to use the app you agree to this notice." (P016, exact quote verified)

Would change this assessment: The consent screen text

**Suggested action:** Ask whether there are separate, explicit choices for optional uses such as marketing.

### F05. Vague purposes
- Severity: **medium** | Confidence: **high** | Rule: CG-PP-04 v1.0
- Evidence basis: quoted | Document evidence: P008, P010
- Legal context: verified not yet in force (LS-IN-DPDPA-S5, LS-IN-DPDP-RULE3). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

'Improve our services' and 'other business purposes' could cover almost anything, so you cannot tell what your data will be used for.

> "improve our services and for other business purposes" (P008, exact quote verified)

**Suggested action:** Ask QuickBasket to list the specific purposes for each type of data.

### F06. Open-ended retention
- Severity: **medium** | Confidence: **high** | Rule: CG-RT-02 v1.0
- Evidence basis: quoted | Document evidence: P014
- Legal context: verified not yet in force (LS-IN-DPDPA-S8-7, LS-IN-DPDP-RULE8). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

Data is kept as long as the company 'considers necessary', with no period or criteria.

> "We keep your information for as long as we consider necessary." (P014, exact quote verified)

**Suggested action:** Ask how long location, contacts and account data are kept and when they are deleted.

### F07. No withdrawal route described
- Severity: **medium** | Confidence: **medium** | Rule: CG-CN-02 v1.0
- Evidence basis: absence in supplied text | Document evidence: none
- Legal context: verified not yet in force (LS-IN-DPDPA-S6, LS-IN-DPDP-RULE3). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

The complete notice does not explain how to withdraw consent or turn off permissions or sharing.

Would change this assessment: App settings may offer a route that the notice does not mention

**Suggested action:** Check your phone's app-permission settings and the app's account settings; ask QuickBasket for the withdrawal process.

## Questions to ask the organisation
- Does the app work for ordering if I deny contacts and microphone access? *(Why: Shows whether these permissions are truly needed for delivery.)*
- Why do you need my location when the app is closed? *(Why: Background location reveals your movements all day, not just your delivery address.)*
- Which partners receive my data for marketing, and how do I opt out? *(Why: Unnamed recipients and no opt-out mean you cannot control onward use.)*
- How long do you keep my location history and contacts? *(Why: Open-ended retention increases exposure over time.)*

## Suggested next steps (you decide)
- If your phone offers it, set location to 'while using the app' and deny contacts and microphone, then check whether ordering still works. *(if available)*
- Ask QuickBasket support the questions above before agreeing.
- Consider an alternative service if mandatory access remains unexplained.
- Before agreeing, ask QuickBasket whether you can order without contacts and microphone access. If your phone lets you deny a permission, try denying these and see whether ordering still works. *(if available)*
- If your device allows it, choose 'while using the app' or approximate location. Ask why background location is needed for a customer. *(if available)*
- Look for a marketing or partner-sharing setting and decline it if you do not want it; ask QuickBasket how to opt out. *(if available)*
- Ask whether there are separate, explicit choices for optional uses such as marketing. *(if available)*
- Ask QuickBasket to list the specific purposes for each type of data. *(if available)*
- Ask how long location, contacts and account data are kept and when they are deleted. *(if available)*
- Check your phone's app-permission settings and the app's account settings; ask QuickBasket for the withdrawal process. *(if available)*
- If you need a legal determination, ask a qualified privacy or legal professional; ConsentGuard does not provide one.

## Legal sources (India registry)
- **LS-IN-DPDPA-COMMENCE**: Notification G.S.R. 843(E) appointing commencement dates for the Digital Personal Data Protection Act, 2023. Ministry of Electronics and Information Technology (MeitY), Government of India. Provision: Paragraphs (a)-(c): phased commencement. Published 2025-11-13; effective 2025-11-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2025/11/c56ceae6c383460ca69577428d36828b.pdf
- **LS-IN-DPDP-RULE3**: Digital Personal Data Protection Rules, 2025, rule 3 - Notice given by Data Fiduciary. Ministry of Electronics and Information Technology (MeitY), Government of India. Provision: Rule 3. Published 2025-11-13; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf
- **LS-IN-DPDP-RULE8**: Digital Personal Data Protection Rules, 2025, rule 8 - Time period for specified purpose deemed no longer served. Ministry of Electronics and Information Technology (MeitY), Government of India. Provision: Rule 8. Published 2025-11-13; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf
- **LS-IN-DPDPA-S5**: Digital Personal Data Protection Act, 2023, section 5 - Notice. Parliament of India; text hosted by MeitY. Provision: Section 5. Published 2023-08-11; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf
- **LS-IN-DPDPA-S6**: Digital Personal Data Protection Act, 2023, section 6 - Consent. Parliament of India; text hosted by MeitY. Provision: Section 6(1)-(8) and (10). Published 2023-08-11; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf
- **LS-IN-DPDPA-S8-7**: Digital Personal Data Protection Act, 2023, section 8(7) - Erasure. Parliament of India; text hosted by MeitY. Provision: Section 8(7). Published 2023-08-11; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf

## Evidence index
- **P005** (paragraph 5 (section: Information we collect)): To use QuickBasket you must allow access to your precise location at all times, including when the app is closed, your phone contacts, and your microphone. If you do not allow these permissions the app will not work.
- **P006** (paragraph 6 (section: Information we collect)): We collect location data continuously in the background to provide a better experience.
- **P008** (paragraph 8 (section: How we use information)): We use your information to deliver orders, process payments, improve our services and for other business purposes.
- **P009** (paragraph 9 (section: How we use information)): Contacts are used to help us understand your social network and recommend QuickBasket to people you know.
- **P010** (paragraph 10 (section: How we use information)): Microphone access helps us improve our services.
- **P012** (paragraph 12 (section: Sharing)): We may share your information with our partners, affiliates and other third parties for marketing and analytics.
- **P014** (paragraph 14 (section: Retention)): We keep your information for as long as we consider necessary.
- **P016** (paragraph 16 (section: Your choices)): By continuing to use the app you agree to this notice.

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
| document-intake | 1.0.0 | code | success | 17 paragraphs; parse quality good. |
| evidence-extraction | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| plain-language-explanation | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| purpose-proportionality | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| consent-design-review | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| user-action-plan | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| jurisdiction-check | 1.0.0 | code | success | Legal sources attached from registry only. |
| findings-prioritization | 1.0.0 | code | success | 0 finding(s) adjusted by rule caps. |
| report-and-qa | 1.0.0 | code | success | 3 validation check(s) recorded. |

## Validation checks
- [pass] all finding evidence IDs exist: 11 reference(s) checked.
- [pass] all retained quotes verified
- [pass] legal sources come from registry

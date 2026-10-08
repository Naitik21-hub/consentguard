# ConsentGuard report: Sahyog Digital Bank: Customer Privacy Notice (synthetic)

> This export contains quotations from the text you submitted. Share it only if you are comfortable sharing those quotations.
> **DEMO: pre-authored demonstration output for a synthetic document, validated by the live pipeline. Not live AI analysis.**

- Report ID: `CG-A055E7FAF2`  |  Analyzed: 2026-10-08T10:29:14+00:00  |  Mode: demo
- Document version: unknown  |  Jurisdiction: IN  |  Completeness: complete
- Rule set v1.0.0  |  Legal sources last verified: 2026-10-08

## Overall: Clarification needed
No high-severity findings, but 3 medium-severity point(s) need clarification (F01, F02, F03).

*ConsentGuard does not certify safety or legal compliance. It explains the supplied text only.*

## Plain-English summary

**Data collected**
- Identity and KYC details: name, date of birth, address, PAN, photograph and identity documents. [P004]
- Transaction records. [P005]

**Purposes**
- KYC checks that the bank says are required by law and banking regulations, and running the account you asked for. [P004]
- Fraud prevention and legal reporting. [P005]
- Offering you products from the bank and 'select partners', possibly based on your transaction patterns. [P007]

**Who receives it**
- Unnamed 'select partners' may receive 'relevant information' so that they can contact you with offers. [P007]

**How long it is kept**
- Account and KYC records are kept for periods required by law after closure. No retention is stated for marketing use. [P009]

**Your choices and how to withdraw**
- A grievance contact is given. No way to refuse or withdraw from partner marketing is described. [P011]

**Unknown or missing in the supplied text**
- Who the 'select partners' are and what 'relevant information' includes.
- Whether partner marketing is optional and how to opt out.
- How long data used for marketing is kept.

## Data inventory
| Data | Basis | Purpose | Recipients | Retention | Evidence |
|---|---|---|---|---|---|
| KYC data (name, date of birth, address, PAN, photograph, ID documents) | stated | KYC and account services | unknown | Periods required by law after account closure | P004, P009 |
| Transaction records and patterns | stated | Run account, prevent fraud, legal reporting; also product offers | Select partners (relevant information) | Periods required by law (for account records) | P005, P007, P009 |

## Permission-purpose map
| Permission | Feature | Scope | Required? | Assessment | Alternatives | Evidence |
|---|---|---|---|---|---|---|

## Consent-design review
- **Clarity and specificity of purposes**: concern. Account purposes are clear; the marketing purpose ('suitable offers', 'relevant information') is vague. [P004, P007]
- **Separation of optional uses from essential processing**: concern. Partner marketing appears in the same notice as essential account processing, and the text does not say it is optional. [P007]
- **Granularity of choices**: unknown. No separate choices are described in the notice; the account-opening screen was not supplied. [none]
- **Evidence of affirmative user action**: unknown. Cannot be assessed from the notice alone. [none]
- **Ease and availability of withdrawal**: concern. Only a grievance contact is given; no withdrawal or opt-out route for marketing is described. [P011]
- **Transparency about recipients and retention**: concern. Partners are unnamed. Retention is tied to legal periods for account records but not stated for marketing. [P007, P009]
- **Bundling, coercion, confusing wording, or misleading choices**: unknown. The text does not show whether marketing is a condition of opening an account. [none]

## Findings

### F01. Partner marketing recipients and data are vague
- Severity: **medium** | Confidence: **high** | Rule: CG-SH-02 v1.0
- Evidence basis: quoted | Document evidence: P007
- Legal context: verified not yet in force (LS-IN-DPDPA-S11). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

'Select partners' and 'relevant information' do not tell you who receives your data or what is shared, even though transaction patterns may be used.

> "may share relevant information with such partners to enable them to contact you with suitable offers" (P007, exact quote verified)

Would change this assessment: A list of partner categories; Whether this sharing is optional

**Suggested action:** Ask the bank which partners receive which information, and whether you can open and use the account without partner marketing.

### F02. No opt-out or withdrawal route for marketing described
- Severity: **medium** | Confidence: **medium** | Rule: CG-CN-02 v1.0
- Evidence basis: absence in supplied text | Document evidence: none
- Legal context: verified not yet in force (LS-IN-DPDPA-S6, LS-IN-DPDP-RULE3). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

The complete notice gives a grievance contact but no way to say no to, or withdraw from, partner marketing.

Would change this assessment: Net-banking or app settings may offer an opt-out not mentioned here

**Suggested action:** Look in net-banking or app settings for marketing preferences; otherwise ask the grievance officer how to opt out.

### F03. Marketing use of transaction patterns is loosely described
- Severity: **medium** | Confidence: **medium** | Rule: CG-PP-04 v1.0
- Evidence basis: quoted | Document evidence: P007
- Legal context: verified not yet in force (LS-IN-DPDPA-S5, LS-IN-DPDP-RULE3). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

Using transaction patterns for offers goes beyond running the account, and 'suitable offers' does not explain what analysis is done.

> "including your transaction patterns, to offer you products from Sahyog and our select partners" (P007, exact quote verified)

Would change this assessment: The account-opening consent screen

**Suggested action:** Ask whether your transaction patterns are used for offers only with your separate agreement.

### F04. KYC and account processing are described as legally required
- Severity: **informational** | Confidence: **high** | Rule: CG-LG-01 v1.0
- Evidence basis: quoted | Document evidence: P004, P005
- Legal context: verified not yet in force (LS-IN-DPDPA-S4, LS-IN-DPDPA-S7). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

The bank says KYC data is needed for checks required by law and to run the account you asked for. Processing of this kind may not depend on your consent, so declining marketing would not normally stop it.

> "Know Your Customer (KYC) checks required by law and banking regulations" (P004, exact quote verified)

**Suggested action:** Expect KYC processing if you open the account; ask the bank which processing depends on your consent.

## Questions to ask the organisation
- Is partner marketing optional, and can I open the account without agreeing to it? *(Why: Separates essential banking from optional marketing.)*
- Which partners receive my information, and what exactly is shared? *(Why: Transaction patterns can reveal a lot about your life.)*
- How do I opt out of marketing and partner sharing later? *(Why: Withdrawal should be possible without closing the account.)*

## Suggested next steps (you decide)
- Do not expect to avoid KYC processing; it is described as legally required.
- If the account form or app offers a marketing or partner-sharing choice, decline it unless you want partner offers. *(if available)*
- Ask the bank which partners receive which information, and whether you can open and use the account without partner marketing. *(if available)*
- Look in net-banking or app settings for marketing preferences; otherwise ask the grievance officer how to opt out. *(if available)*
- Ask whether your transaction patterns are used for offers only with your separate agreement. *(if available)*
- If you need a legal determination, ask a qualified privacy or legal professional; ConsentGuard does not provide one.

## Legal sources (India registry)
- **LS-IN-DPDPA-COMMENCE**: Notification G.S.R. 843(E) appointing commencement dates for the Digital Personal Data Protection Act, 2023. Ministry of Electronics and Information Technology (MeitY), Government of India. Provision: Paragraphs (a)-(c): phased commencement. Published 2025-11-13; effective 2025-11-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2025/11/c56ceae6c383460ca69577428d36828b.pdf
- **LS-IN-DPDP-RULE3**: Digital Personal Data Protection Rules, 2025, rule 3 - Notice given by Data Fiduciary. Ministry of Electronics and Information Technology (MeitY), Government of India. Provision: Rule 3. Published 2025-11-13; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf
- **LS-IN-DPDPA-S11**: Digital Personal Data Protection Act, 2023, section 11 - Right to access information. Parliament of India; text hosted by MeitY. Provision: Section 11(1). Published 2023-08-11; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf
- **LS-IN-DPDPA-S4**: Digital Personal Data Protection Act, 2023 (No. 22 of 2023), section 4 - Grounds for processing personal data. Parliament of India; published by the Ministry of Law and Justice (Legislative Department); text hosted by MeitY. Provision: Section 4. Published 2023-08-11; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf
- **LS-IN-DPDPA-S5**: Digital Personal Data Protection Act, 2023, section 5 - Notice. Parliament of India; text hosted by MeitY. Provision: Section 5. Published 2023-08-11; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf
- **LS-IN-DPDPA-S6**: Digital Personal Data Protection Act, 2023, section 6 - Consent. Parliament of India; text hosted by MeitY. Provision: Section 6(1)-(8) and (10). Published 2023-08-11; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf
- **LS-IN-DPDPA-S7**: Digital Personal Data Protection Act, 2023, section 7 - Certain legitimate uses. Parliament of India; text hosted by MeitY. Provision: Section 7. Published 2023-08-11; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf

## Evidence index
- **P004** (paragraph 4 (section: Information needed to open and run your account)): To open and operate your savings account we collect your name, date of birth, address, PAN, photograph and identity documents. This information is required to complete Know Your Customer (KYC) checks required by law and banking regulations, and to provide the account services you request.
- **P005** (paragraph 5 (section: Information needed to open and run your account)): We process your transaction records to run your account, prevent fraud and meet our legal reporting duties.
- **P007** (paragraph 7 (section: Marketing and partners)): We may also use your information, including your transaction patterns, to offer you products from Sahyog and our select partners, and may share relevant information with such partners to enable them to contact you with suitable offers.

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
| document-intake | 1.0.0 | code | success | 11 paragraphs; parse quality good. |
| evidence-extraction | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| plain-language-explanation | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| purpose-proportionality | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| consent-design-review | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| user-action-plan | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| jurisdiction-check | 1.0.0 | code | success | Legal sources attached from registry only. |
| findings-prioritization | 1.0.0 | code | success | 0 finding(s) adjusted by rule caps. |
| report-and-qa | 1.0.0 | code | success | 3 validation check(s) recorded. |

## Validation checks
- [pass] all finding evidence IDs exist: 4 reference(s) checked.
- [pass] all retained quotes verified
- [pass] legal sources come from registry

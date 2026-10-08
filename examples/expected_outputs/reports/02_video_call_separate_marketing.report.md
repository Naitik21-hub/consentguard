# ConsentGuard report: MeetLoop Privacy and Permissions Notice (synthetic)

> This export contains quotations from the text you submitted. Share it only if you are comfortable sharing those quotations.
> **DEMO: pre-authored demonstration output for a synthetic document, validated by the live pipeline. Not live AI analysis.**

- Report ID: `CG-A30AA3A34E`  |  Analyzed: 2026-10-08T10:29:14+00:00  |  Mode: demo
- Document version: Synthetic v1 (2026)  |  Jurisdiction: IN  |  Completeness: complete
- Rule set v1.0.0  |  Legal sources last verified: 2026-10-08

## Overall: No major concerns found in supplied text
No high- or medium-severity concerns were supported by the supplied text. This covers only what the text says, not how the organisation behaves in practice.

*ConsentGuard does not certify safety or legal compliance. It explains the supplied text only.*

## Plain-English summary

**Data collected**
- Name and mobile number for your account. [P004]
- Microphone and camera access, requested only when you start or join a call. [P005]
- Call metadata: time, duration and participants of each call. [P006]

**Purposes**
- Running calls, showing call history and detecting abuse. [P005, P006]
- Optional offers and product news, only if you switch this on. [P008]

**Who receives it**
- A cloud hosting provider that processes data on MeetLoop's instructions. MeetLoop says it does not sell personal data. [P010]

**How long it is kept**
- Call metadata for 90 days; account details deleted within 30 days after you delete your account. Recordings stay on your device. [P012, P005]

**Your choices and how to withdraw**
- Turn off camera or microphone in phone settings and marketing under Settings > Notifications > Marketing. Turning marketing off does not affect calls. [P014, P008]

**Unknown or missing in the supplied text**
- The name and location of the cloud hosting provider.
- How the marketing choice is presented on screen (consent screen not supplied).

## Data inventory
| Data | Basis | Purpose | Recipients | Retention | Evidence |
|---|---|---|---|---|---|
| Name, mobile number | stated | Account and contact discovery | Cloud hosting provider | Deleted within 30 days after account deletion | P004, P010, P012 |
| Microphone and camera (live call) | permission_only | Let others hear and see you during calls | Other call participants | Not recorded unless you press Record; recordings stay on your device | P005 |
| Call metadata | stated | Call history and abuse detection | Cloud hosting provider | 90 days | P006, P012 |

## Permission-purpose map
| Permission | Feature | Scope | Required? | Assessment | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| Microphone | Voice and video calls | Only when starting or joining a call | required | Appears proportionate to the stated purpose: A calling app needs the microphone so others can hear you, and access is limited to calls. | Mute during calls; Turn off in phone settings when not needed | P005 |
| Camera | Video calls | Only when starting or joining a call | required | Appears proportionate to the stated purpose: Video calls need the camera, and access is tied to calls. | Join with camera off | P005 |

## Consent-design review
- **Clarity and specificity of purposes**: adequate. Each data type is linked to a specific purpose. [P004, P005, P006]
- **Separation of optional uses from essential processing**: adequate. Marketing is a separate choice that does not affect calls. [P008]
- **Granularity of choices**: adequate. Camera, microphone and marketing can each be controlled separately. [P014]
- **Evidence of affirmative user action**: unknown. The notice says marketing is off unless switched on, but the consent screen itself was not supplied. [P008]
- **Ease and availability of withdrawal**: adequate. Withdrawal routes for permissions and marketing are described. [P014]
- **Transparency about recipients and retention**: adequate. The recipient type and retention periods are stated, though the provider is not named. [P010, P012]
- **Bundling, coercion, confusing wording, or misleading choices**: adequate. No bundling found: the text says declining marketing does not affect calls. [P008, P014]

## Findings

### F01. Hosting provider not named
- Severity: **low** | Confidence: **medium** | Rule: CG-SH-02 v1.0
- Evidence basis: quoted | Document evidence: P010
- Legal context: verified not yet in force (LS-IN-DPDPA-S11). Linked provisions are verified but scheduled to commence on 2027-05-13 (per G.S.R. 843(E)/846(E)). They are cited as context, not as a current legal obligation. ConsentGuard does not decide whether any provision applies to this organisation.

The recipient category is clear (a cloud host acting on instructions), but the provider and where it stores data are not named.

> "We use a cloud hosting provider to run our service." (P010, exact quote verified)

**Suggested action:** If it matters to you, ask MeetLoop which hosting provider it uses and where data is stored.

### F02. Marketing is a separate, optional choice
- Severity: **informational** | Confidence: **high** | Rule: CG-CN-04 v1.0
- Evidence basis: quoted | Document evidence: P008
- Legal context: no legal reference (none). This is a governance heuristic with no linked legal source.

Marketing messages need separate permission, are off by default according to the notice, and declining them does not affect calls.

> "saying no does not affect your ability to make calls" (P008, exact quote verified)

Would change this assessment: The consent screen, to confirm how the choice is shown

**Suggested action:** You can leave marketing switched off; the notice says calls are unaffected.

### F03. Microphone and camera tied to calls
- Severity: **informational** | Confidence: **high** | Rule: CG-PO-01 v1.0
- Evidence basis: quoted | Document evidence: P005
- Legal context: no legal reference (none). This is a governance heuristic with no linked legal source.

Access is requested only for calls, and calls are not recorded unless you choose to record.

> "MeetLoop asks for microphone and camera access only when you start or join a call" (P005, exact quote verified)

**Suggested action:** No action needed; you can still turn access off in phone settings between calls.

## Questions to ask the organisation
- Which cloud provider hosts my data, and in which country? *(Why: Helps you understand where your call metadata is stored.)*

## Suggested next steps (you decide)
- Leave marketing switched off unless you want offers.
- If your phone supports it, review camera and microphone access for MeetLoop in phone settings. *(if available)*
- If it matters to you, ask MeetLoop which hosting provider it uses and where data is stored. *(if available)*
- If you need a legal determination, ask a qualified privacy or legal professional; ConsentGuard does not provide one.

## Legal sources (India registry)
- **LS-IN-DPDPA-COMMENCE**: Notification G.S.R. 843(E) appointing commencement dates for the Digital Personal Data Protection Act, 2023. Ministry of Electronics and Information Technology (MeitY), Government of India. Provision: Paragraphs (a)-(c): phased commencement. Published 2025-11-13; effective 2025-11-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2025/11/c56ceae6c383460ca69577428d36828b.pdf
- **LS-IN-DPDPA-S11**: Digital Personal Data Protection Act, 2023, section 11 - Right to access information. Parliament of India; text hosted by MeitY. Provision: Section 11(1). Published 2023-08-11; effective 2027-05-13; status: verified; retrieved 2026-10-08. https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf

## Evidence index
- **P005** (paragraph 5 (section: What we collect and why)): Microphone and camera: MeetLoop asks for microphone and camera access only when you start or join a call, so that others on the call can hear and see you. We do not record calls unless you press the Record button, and recordings are stored on your device.
- **P008** (paragraph 8 (section: Optional marketing messages)): With your separate permission, we may send you offers and product news by email or SMS. This choice is off unless you switch it on, and saying no does not affect your ability to make calls.
- **P010** (paragraph 10 (section: Sharing)): We use a cloud hosting provider to run our service. It processes data only on our instructions. We do not sell your personal data.

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
| document-intake | 1.0.0 | code | success | 16 paragraphs; parse quality good. |
| evidence-extraction | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| plain-language-explanation | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| purpose-proportionality | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| consent-design-review | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| user-action-plan | 1.0.0 | fixture | success | Pre-authored demonstration output, validated by the same pipeline as live mode. |
| jurisdiction-check | 1.0.0 | code | success | Legal sources attached from registry only. |
| findings-prioritization | 1.0.0 | code | success | 0 finding(s) adjusted by rule caps. |
| report-and-qa | 1.0.0 | code | success | 3 validation check(s) recorded. |

## Validation checks
- [pass] all finding evidence IDs exist: 3 reference(s) checked.
- [pass] all retained quotes verified
- [pass] legal sources come from registry

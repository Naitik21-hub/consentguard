# Privacy and Limitations

ConsentGuard applies its own principles to itself.

## What data exists, where, and for how long
| Data | Where | Lifetime | Cleared by Reset? |
|---|---|---|---|
| Pasted or uploaded document text | Streamlit session memory (server process RAM) | Until Reset, browser session end, or server stop | Yes |
| Uploaded file bytes | Streamlit uploader memory | Until the uploader is reset or the file is removed | Yes (Reset gives the uploader a new key) |
| Redaction map (placeholder to original) | Session memory only; never sent or exported | As above | Yes |
| Report, follow-up answers | Session memory | As above | Yes |
| Downloaded reports | Your device, only if **you** click Download | Until you delete them | No (they are your files) |
| Data sent to Anthropic (live mode) | Anthropic API | Governed by Anthropic's policies and your account or organisation settings | **No.** ConsentGuard cannot delete it |

- **No temporary files.** Uploads are parsed from memory (`io.BytesIO`). The app writes nothing to disk.
- **No database, no accounts, no vector store.**
- **No analytics.** `.streamlit/config.toml` sets `gatherUsageStats = false`, and the app logs no document content.
- **Local only.** `.streamlit/config.toml` sets `server.address = "localhost"`, so other devices on your network cannot open the app.
- **No credentials collected.** The app never asks for passwords, OTPs, bank credentials, or ID numbers. The disclosure tells users not to send them.

## Live-mode disclosure (shown before every send)
Before sending, the app shows: the exact text that will leave the device (after optional redaction), the recipient (Anthropic's API and the model ID), the purpose (to explain this document), and what ConsentGuard stores (session memory only). Sending requires a tick box **and** a button press. Follow-up questions in live mode show the same disclosure, because they send the question plus the document paragraphs.

ConsentGuard does **not** promise zero retention by the provider. Check Anthropic's current data-retention terms for your account. Organisations with special arrangements should confirm them separately.

## Redaction limits
Local redaction covers emails, Indian phone numbers, UPI IDs, card-like numbers, Aadhaar-like and PAN-like numbers, IFSC codes, and IP addresses. Each value gets a consistent placeholder: the same email always becomes `[EMAIL_1]`. It does **not** detect names, addresses, or free-text descriptions, and unusual combinations of facts can still identify a person. Redaction is a help, not anonymisation.

## Safety of rendering and processing
- Uploaded content is never executed. Only text is extracted.
- Document-derived and model-derived text is escaped before display, so Markdown links, images, and HTML in a document cannot render or load anything. Evidence paragraphs are shown with `st.text`.
- Text inside a document that addresses AI tools ("ignore previous instructions", "send this data to...") is flagged and treated as content. Code adds a CG-IN-01 finding even if the model misses it.

## Bounds
| Bound | Value |
|---|---|
| Text length | 60,000 characters (rejected above this, never truncated) |
| PDF pages | 40 |
| File size | 5 MB |
| Model output | 32,000 tokens; a cut-off output is an error, not a partial report |
| Model calls per analysis | 1, plus at most 1 repair; SDK network retries at most 2 |
| Follow-up question length | 500 characters |

## Product limitations
- It interprets **text**. It cannot know whether an organisation follows its policy, and it cannot observe the live app interface.
- A privacy notice alone cannot show how consent was obtained. Interface dimensions stay `unknown` without consent-screen text.
- Severity and confidence labels are prototype heuristics, not statutory classifications.
- The legal registry covers India only and was verified on 2026-10-08. Commencement dates are computed from the Gazette date (see `source_verification.md`).
- Demo follow-ups use keyword matching, not AI.
- Live-model quality is not yet evaluated (see `evaluation.md`). LLMs can still misread text. The validation layer catches fabricated quotes and IDs, but not every subtle misreading.
- No claim is made that the model is immune to prompt injection. The defences are layered (data framing, a contract with no free-form legal or label fields, deterministic flags, wording filters) and tested against the scenarios in `tests/`.

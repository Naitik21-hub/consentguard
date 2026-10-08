# ConsentGuard

**Understand what you are agreeing to.**

ConsentGuard is an India-first consumer-education prototype. It reads a privacy notice, consent form, or app-permission text and gives you:

- a plain-English summary (what data, why, who gets it, how long, your choices);
- a check of whether each data request fits the stated purpose;
- a review of how consent is requested, using only evidence you supplied;
- prioritised findings, each backed by **exact quotes** with paragraph IDs;
- links to **verified** Indian legal sources, with an honest "in force or not yet" status;
- questions to ask and steps **you** control;
- follow-up answers grounded only in the document;
- Markdown and JSON reports that you download yourself.

It is **not** legal advice, a compliance certificate, or a security scan. It does not know whether an organisation actually follows its policy.

The project has two parts:
1. **An agent**: the Streamlit app (`app.py`) with one orchestrator (`src/orchestrator.py`) that routes each document through nine skills.
2. **A portable skill library**: `skills/*/SKILL.md`, plus JSON Schemas (`schemas/`), a canonical rule file (`rules/`), and a plain-Markdown fallback.

---

## 1. Set up (about 5 minutes, one time)

You need **Python 3.10 or newer**. To check, open a terminal (Windows: search for "PowerShell"; Mac: open "Terminal") and type `python --version`.

1. Open a terminal **inside the `consentguard` folder**. On Windows you can Shift + right-click the folder and choose "Open in Terminal".
2. (Recommended) Create a private environment so nothing clashes with other projects:
   ```bash
   python -m venv .venv
   ```
   Then activate it. Windows: `.venv\Scripts\activate`. Mac/Linux: `source .venv/bin/activate`.
3. Install the packages:
   ```bash
   pip install -r requirements.txt
   ```

## 2. Run the demo (no API key needed)

```bash
streamlit run app.py
```

Your browser opens at http://localhost:8501. If it doesn't, open that address yourself.

- Keep the sidebar on **Demo mode**.
- Go to **Demo examples**, click **Run this demo** on any of the eight synthetic documents, then open the **Report** tab.
- Try the **Ask ConsentGuard** tab, for example "How long do they keep my data?".

Demo reports are **pre-authored demonstrations** for synthetic documents. They pass through the same validation pipeline as live mode (quote checks, severity caps, legal registry), and the app labels them clearly.

> Run the command from inside the `consentguard` folder so the privacy settings in `.streamlit/config.toml` apply. These settings turn off Streamlit's usage statistics and make the app reachable only from your own computer.

## 3. Live mode (analyse your own text with Claude)

1. Get an API key from https://console.anthropic.com/. API usage is billed to your account.
2. Copy `.env.example` to a new file named `.env` in the same folder, and paste your key after `ANTHROPIC_API_KEY=`.
   Never share or commit `.env`; `.gitignore` already excludes it.
3. Optional: choose the model with `CONSENTGUARD_MODEL`. The default `claude-opus-5` was checked against Anthropic's model reference on 2026-10-08; `claude-sonnet-5` is a cheaper option.
4. Restart the app and choose **Live mode** in the sidebar.
5. Paste text or upload a .txt, .md, or text-based .pdf. Add optional context if you have it.
6. Click **Prepare preview**. Nothing is sent at this point. Review the redaction and the exact text that would leave your device.
7. Tick the confirmation box and click **Send previewed text for analysis**.

If a live request fails (timeout, invalid key, malformed output after one repair attempt), you get a clear error. ConsentGuard never substitutes a demo report.

**Approximate cost per analysis:** up to about 15k input tokens (the 60,000-character limit) and up to 32k output tokens. Check https://www.anthropic.com/pricing for your model.

## 4. Run the tests

```bash
python -m pytest -q
```

The default tests make **no network calls**; live API behaviour is simulated with a fake client. There is a separate, optional live evaluation that costs money and needs a key:

```bash
python -m evaluation.run_live_eval
```

## 5. Use the skills in Claude (without this app)

See `skills/README.md`. In short:
- **Claude Code:** copy the `skills/<name>/` folders into `~/.claude/skills/` (personal) or `.claude/skills/` (project).
- **claude.ai** (paid plans with code execution enabled): run `python -m src.build_skill_bundle`, then upload the ZIPs from `dist/skills/` in Settings. Uploads are per user.
- **Any ordinary Claude chat:** attach `skills/fallback/ConsentGuard_skills_plain.md` and paste your document.

These formats follow Anthropic's published Agent Skills format, which was checked on 2026-10-08. **Installing them in claude.ai or Claude Code has not been tested in this build.**

## 6. Project map

| Path | What it is |
|---|---|
| `app.py` | Streamlit app with the Analyze, Report, Ask, How it works, and Demo examples tabs |
| `src/orchestrator.py` | Pipeline: intake, then the model or fixture, then legal check, prioritization, and validation |
| `src/models.py` | Pydantic contracts (model output and report) |
| `src/rules.py` | Severity caps, legal applicability, overall label, banned wording |
| `src/evidence.py` | Paragraph IDs, exact-quote checks, injection detection, keyword retrieval |
| `src/document_parser.py` | Paste, TXT/MD, and PDF parsing with limits; scanned-PDF detection |
| `src/redaction.py` | Local best-effort redaction with consistent placeholders |
| `src/llm_client.py` | Anthropic SDK wrapper: timeouts, bounded retries, one repair attempt |
| `src/report_renderer.py` | Markdown and JSON exports |
| `prompts/orchestrator_system.md` | Orchestrator system prompt (skills and rules are appended from their files) |
| `skills/` | Nine SKILL.md files, a README, and the plain-Markdown fallback |
| `rules/governance_rules.json` | **Canonical** governance rules (IDs, versions, caps) |
| `rules/legal_sources.json` | **Canonical** legal source registry (verified 2026-10-08) |
| `schemas/` | JSON Schemas generated from the models (`python -m src.export_schemas`) |
| `examples/` | Eight synthetic policies, fixture drafts, expected outcomes, reference reports |
| `tests/` | Deterministic tests (104 passing on 2026-10-08) |
| `vercel_app.py`, `pyproject.toml`, `vercel.json` | Hosted deployment on Vercel (demo-only by default; see `docs/deployment.md`) |
| `evaluation/` | Optional live-model evaluation script and rubric |
| `docs/` | Two-page white paper (PDF), product brief, architecture, privacy, source verification, evaluation, demo script, presentation notes, deployment |

## 7. Known limits

- No OCR. Scanned PDFs are rejected with a message.
- No URL crawling, no automatic discovery of app permissions, no policy-version monitoring.
- Limits: 60,000 characters, 40 PDF pages, and 5 MB per file. Longer documents are rejected rather than cut short.
- The legal registry covers India only and was verified on 2026-10-08. Re-verify it using `docs/source_verification.md`.
- Live-mode output quality has **not** been evaluated in this build, because no API key was available. See `docs/evaluation.md`.

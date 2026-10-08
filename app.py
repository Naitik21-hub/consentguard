"""ConsentGuard - Understand what you are agreeing to.

Run:  streamlit run app.py
Demo mode needs no API key. Live mode needs ANTHROPIC_API_KEY in a .env file.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import streamlit as st

from src import rules as R
from src.demo import get_scenario, list_scenarios, prepare_scenario, run_demo, scenario_text
from src.document_parser import LIMITS_TEXT, ParseError, parse_pasted, parse_upload
from src.evidence import render_for_model
from src.llm_client import LLMError, api_key_present, configured_model
from src.models import PermissionInput, SuppliedContext
from src.orchestrator import SKILL_VERSIONS, SKILLS_DIR, analyze, answer_question, run_intake
from src.redaction import REDACTION_WARNING, redact
from src.report_renderer import ASSESSMENT_LABELS, DIM_LABELS, EXPORT_NOTICE, to_json, to_markdown


def _load_dotenv() -> None:
    """Minimal .env loader (KEY=VALUE lines). Values already in the environment win."""
    env = Path(__file__).resolve().parent / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_dotenv()
st.set_page_config(page_title="ConsentGuard", page_icon=":shield:", layout="wide")

SESSION_KEYS = ["prepared", "report", "qa", "redaction", "pending_text", "pending_source", "uploader_nonce", "last_error", "demo_id"]
_MD_SPECIAL = re.compile(r"([\\`*_{}\[\]()#+\-.!|<>~=$])")


def esc(text) -> str:
    """Escape Markdown/HTML so document- or model-derived text renders as plain text."""
    return _MD_SPECIAL.sub(r"\\\1", str(text if text is not None else "unknown"))


def init_state() -> None:
    st.session_state.setdefault("uploader_nonce", 0)
    st.session_state.setdefault("qa", [])


def reset_session() -> None:
    nonce = st.session_state.get("uploader_nonce", 0) + 1
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state["uploader_nonce"] = nonce  # new key = fresh, empty file uploader
    st.session_state["qa"] = []
    st.session_state["reset_done"] = True


init_state()

# Hosted deployments (Vercel sets VERCEL=1) are demo-only unless explicitly unlocked.
HOSTED = os.environ.get("VERCEL") == "1"
LIVE_ALLOWED = (not HOSTED) or os.environ.get("CONSENTGUARD_ALLOW_LIVE") == "1"

# ---------------------------------------------------------------------------
# Sidebar: mode, limits, reset
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("ConsentGuard")
    st.caption("Understand what you are agreeing to.")
    mode_options = ["Demo mode (no API key, synthetic examples)"]
    if LIVE_ALLOWED:
        mode_options.append("Live mode (sends text to Anthropic's API)")
    mode_label = st.radio(
        "Mode",
        mode_options,
        help="Demo mode replays pre-authored analyses of synthetic documents through the real validation pipeline. "
        "Live mode calls Claude on text you supply, after you preview and confirm.",
    )
    mode = "live" if mode_label.startswith("Live") else "demo"
    if not LIVE_ALLOWED:
        st.caption("This hosted copy is demo-only: it never sends text to an AI provider. "
                   "To analyse your own documents, run ConsentGuard on your own computer (see the README).")
    if mode == "live":
        if api_key_present():
            st.success(f"API key found. Model: `{configured_model()}`")
        else:
            st.error("No ANTHROPIC_API_KEY found. Copy .env.example to .env and add your key, then restart. See README.")
    else:
        st.info("Demo mode: no network calls, no API key needed. Results are pre-authored demonstrations.")
    st.caption(LIMITS_TEXT)
    st.divider()
    st.subheader("Reset / delete session")
    st.caption(
        "Clears this browser session's document, redaction map, report, and follow-up answers held in app memory, "
        "and resets the file uploader. ConsentGuard writes no files and keeps no logs of document content. "
        "It cannot delete data already sent to Anthropic in live mode; that is governed by Anthropic's retention "
        "policy and your account settings."
    )
    if st.button("Reset and clear session", type="secondary"):
        reset_session()
        st.rerun()
    if st.session_state.pop("reset_done", False):
        st.success("Session cleared.")

st.title("ConsentGuard")
st.markdown("**Understand what you are agreeing to.** An India-first consumer education prototype. "
            "Not legal advice, not a compliance certificate, not a security scan.")

if st.session_state.get("flash"):
    st.success(st.session_state.pop("flash"))

tab_analyze, tab_report, tab_ask, tab_how, tab_demo = st.tabs(
    ["Analyze", "Report", "Ask ConsentGuard", "How it works", "Demo examples"]
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def parse_permissions(raw: str):
    perms = []
    for line in (raw or "").splitlines():
        if not line.strip():
            continue
        name, _, status = line.partition("|")
        status = status.strip().lower()
        perms.append(PermissionInput(name=name.strip()[:80], status=status if status in ("required", "optional") else "unknown"))
    return perms


def run_demo_scenario(sid: str) -> None:
    st.session_state["prepared"] = prepare_scenario(sid)
    st.session_state["report"] = run_demo(sid)
    st.session_state["qa"] = []
    st.session_state["demo_id"] = sid


# ---------------------------------------------------------------------------
# Analyze tab
# ---------------------------------------------------------------------------
with tab_analyze:
    if mode == "demo":
        st.info("You are in **Demo mode**. Pick a synthetic example below (or in the Demo examples tab). "
                + ("To analyze your own text, switch to Live mode in the sidebar." if LIVE_ALLOWED
                   else "This hosted copy is demo-only; run it locally to analyze your own text."))
        options = {s["title"]: s["id"] for s in list_scenarios()}
        choice = st.selectbox("Synthetic example", list(options.keys()))
        if st.button("Run demo analysis", type="primary"):
            run_demo_scenario(options[choice])
            st.session_state["flash"] = f"Demo report ready for: {choice}. Open the Report tab."
            st.rerun()
    else:
        st.subheader("1. Supply the document")
        pasted = st.text_area("Paste a privacy policy, consent form, or permission text", height=220,
                              key=f"paste_{st.session_state['uploader_nonce']}")
        upload = st.file_uploader("...or upload .txt, .md, or a text-based .pdf", type=["txt", "md", "pdf"],
                                  key=f"upload_{st.session_state['uploader_nonce']}")

        with st.expander("2. Optional context (improves the assessment; skip if unsure)"):
            c1, c2 = st.columns(2)
            service_name = c1.text_input("App / service name")
            category = c1.text_input("Category (e.g. delivery, banking, fitness)")
            feature = c2.text_input("Feature you intend to use (e.g. delivery, video call, photo upload)")
            jurisdiction = c2.text_input("Country / jurisdiction code", value="IN")
            completeness = st.radio("Is this the complete notice or an excerpt?", ["unknown", "complete", "excerpt"], horizontal=True)
            perms_raw = st.text_area("Requested permissions, one per line as `name | required/optional/unknown`",
                                     placeholder="Location | required\nContacts | optional")
            consent_screen = st.text_area("Consent-screen text or choices (optional). Without it, interface behaviour stays unknown.")
            version = st.text_input("Policy date / version (optional)")

        st.subheader("3. Prepare and preview locally")
        do_redact = st.checkbox("Redact common identifiers locally before sending (recommended)", value=True)
        st.caption(REDACTION_WARNING)
        if st.button("Prepare preview (nothing is sent yet)"):
            try:
                if upload is not None:
                    parsed = parse_upload(upload.name, upload.getvalue())
                elif pasted.strip():
                    parsed = parse_pasted(pasted)
                else:
                    raise ParseError("Please paste text or upload a file first.")
                rcounts = {}
                if do_redact:
                    rr = redact(parsed.text)
                    parsed.text = rr.text
                    if parsed.pages:
                        parsed.pages = [redact(p).text for p in parsed.pages]
                    rcounts = rr.counts
                ctx = SuppliedContext(
                    service_name=service_name or None, service_category=category or None,
                    jurisdiction=(jurisdiction or "IN").strip().upper()[:5], intended_feature=feature or None,
                    completeness=completeness, permissions=parse_permissions(perms_raw),
                    consent_screen_text=(redact(consent_screen).text if do_redact else consent_screen) or None,
                    policy_date_version=version or None,
                )
                st.session_state["prepared"] = run_intake(parsed, ctx, rcounts)
                st.session_state["demo_id"] = None
                st.session_state["report"] = None
                st.session_state["qa"] = []
                st.session_state.pop("last_error", None)
            except ParseError as e:
                st.error(str(e))

        prep = st.session_state.get("prepared")
        if prep is not None and st.session_state.get("demo_id") is None:
            it = prep.intake
            st.markdown(f"**Intake:** {it.paragraph_count} paragraphs, {it.char_count:,} characters, "
                        f"parse quality *{it.parse_quality}*, completeness *{it.completeness}*.")
            for w in it.extraction_warnings:
                st.warning(w)
            if prep.redaction_counts:
                st.info("Redacted locally: " + ", ".join(f"{k}: {v}" for k, v in prep.redaction_counts.items()))
            if it.material_questions:
                with st.expander("Questions that would change the assessment (optional)"):
                    for q in it.material_questions:
                        st.markdown("- " + esc(q))
            preview = render_for_model(prep.all_paragraphs)
            with st.expander(f"Preview: exactly the document text that will leave this device ({len(preview):,} characters)", expanded=True):
                st.text(preview)

            st.subheader("4. Send for analysis")
            st.warning(
                "**Before you send:** The previewed text above, your optional context, and ConsentGuard's instructions "
                f"will be sent to **Anthropic's API** (model `{configured_model()}`) to generate the analysis. "
                "Purpose: explain this document to you. ConsentGuard itself stores the result only in this browser session's "
                "memory until you reset or close it. Anthropic's handling and retention of API data are governed by its own "
                "policies and your account settings; ConsentGuard cannot promise zero retention. Do not send passwords, OTPs, "
                "bank credentials, or identity numbers."
            )
            agree = st.checkbox("I have reviewed the preview and want to send it to Anthropic for analysis.")
            send_disabled = not (agree and api_key_present())
            if st.button("Send previewed text for analysis", type="primary", disabled=send_disabled):
                with st.spinner("Analyzing (this can take a minute)..."):
                    try:
                        st.session_state["report"] = analyze(prep, mode="live")
                        st.session_state["qa"] = []
                        st.session_state["flash"] = "Live report ready. Open the Report tab."
                        st.rerun()
                    except LLMError as e:
                        st.session_state["report"] = None
                        st.error(f"Live analysis failed: {e} No report was produced, and no demo content was substituted.")


# ---------------------------------------------------------------------------
# Report tab
# ---------------------------------------------------------------------------
SEV_COLOR = {"high": "red", "medium": "orange", "low": "blue", "informational": "gray"}
OVERALL_COLOR = {"substantial_concerns": "red", "clarification_needed": "orange", "no_major_concerns": "green", "insufficient_information": "gray"}

with tab_report:
    rep = st.session_state.get("report")
    if rep is None:
        st.info("No report yet. Run a demo or a live analysis from the Analyze tab.")
    else:
        if rep.mode == "demo":
            st.warning("DEMO: pre-authored demonstration output for a synthetic document. Not live AI analysis.")
        else:
            st.info(esc(rep.mode_note))
        st.header(esc(rep.document_title or "Untitled document"))
        st.markdown(f"### Overall: :{OVERALL_COLOR[rep.overall_assessment]}[{rep.overall_assessment_label}]")
        st.markdown(esc(rep.overall_rationale))
        st.caption("ConsentGuard does not certify safety or legal compliance and does not know whether the organisation follows its policy.")
        st.caption(f"Report {rep.report_id} | analyzed {rep.analyzed_at} | jurisdiction {rep.jurisdiction} | completeness {rep.completeness} | "
                   f"rules v{rep.rule_set_version} | legal sources verified {rep.last_verification_date}")
        for w in rep.extraction_warnings:
            st.warning(w)

        st.subheader("Plain-English summary")
        s = rep.plain_english_summary
        cols = st.columns(2)
        blocks = [("Data collected", s.data_collected), ("Purposes", s.purposes), ("Who receives it", s.recipients),
                  ("How long it is kept", s.retention), ("Your choices and withdrawal", s.choices_and_withdrawal)]
        for i, (title, pts) in enumerate(blocks):
            with cols[i % 2]:
                st.markdown(f"**{title}**")
                if not pts:
                    st.markdown("- *Not stated in the supplied text.*")
                for p in pts:
                    tag = "" if p.basis == "stated" else f" *({p.basis})*"
                    st.markdown(f"- {esc(p.text)}{tag} `{', '.join(p.evidence_ids) or 'no evidence'}`")
        if s.unknowns:
            st.markdown("**Unknown or missing in the supplied text**")
            for u in s.unknowns:
                st.markdown("- " + esc(u))

        st.subheader("Findings")
        for f in rep.findings:
            with st.container(border=True):
                st.markdown(f"**{f.finding_id}. {esc(f.title)}**  \n"
                            f":{SEV_COLOR[f.severity]}[Severity: {f.severity}] | Confidence: {f.confidence} | "
                            f"Rule {f.rule_id} v{f.rule_version} | Evidence: {f.evidence_basis.replace('_', ' ')}")
                st.markdown(esc(f.explanation))
                for q in f.quotes:
                    st.markdown(f"> {esc(q.quote)}  \n> — `{q.evidence_id}`, exact quote verified")
                if f.missing_context:
                    st.caption("Would change this assessment: " + esc("; ".join(f.missing_context)))
                st.markdown("**Suggested action:** " + esc(f.recommended_action))
                st.caption(f"Legal context: {f.legal_applicability_status.replace('_', ' ')} "
                           f"({', '.join(f.legal_source_ids) or 'none'}). {f.legal_applicability_note}")
                for a in f.adjustments:
                    st.caption("Adjustment: " + a)

        st.subheader("Permission-purpose map")
        if rep.permission_purpose_map:
            st.dataframe([{"Permission": p.permission, "Feature": p.feature or "unknown", "Scope": p.scope or "unknown",
                           "Required?": p.required_status, "Assessment": ASSESSMENT_LABELS[p.assessment],
                           "Why": p.rationale, "Alternatives": "; ".join(p.alternatives), "Evidence": ", ".join(p.evidence_ids)}
                          for p in rep.permission_purpose_map], width="stretch", hide_index=True)
        else:
            st.caption("No permissions described.")

        st.subheader("Data inventory")
        st.dataframe([{"Data": d.data_category, "Basis": d.collection_basis, "Purpose": d.purpose or "unknown",
                       "Recipients": d.recipients or "unknown", "Retention": d.retention or "unknown", "Evidence": ", ".join(d.evidence_ids)}
                      for d in rep.data_inventory], width="stretch", hide_index=True)

        st.subheader("Consent-design review")
        st.dataframe([{"Dimension": DIM_LABELS[d.dimension_id], "Status": d.status, "Explanation": d.explanation,
                       "Evidence": ", ".join(d.evidence_ids)} for d in rep.consent_dimensions], width="stretch", hide_index=True)

        st.subheader("Questions to ask the organisation")
        for q in rep.targeted_questions:
            st.markdown(f"- {esc(q.question)} *(Why: {esc(q.why_it_matters)})*")
        st.subheader("Suggested next steps (you decide; ConsentGuard never acts for you)")
        for stp in rep.next_steps:
            st.markdown("- " + esc(stp.action) + (" *(if available)*" if stp.conditional else ""))

        with st.expander("Evidence (paragraphs from the supplied text)"):
            for p in rep.evidence:
                st.markdown(f"**{p.evidence_id}** ({esc(p.location)})")
                st.text(p.text)
        with st.expander("Legal sources (India registry) and applicability"):
            for src in rep.legal_sources:
                st.markdown(f"**{src.source_id}**: {esc(src.title)}  \n{esc(src.issuing_authority)} | provision: {esc(src.provision)} | "
                            f"published {src.publication_date} | effective {src.effective_date} | **{src.verification_status}** | retrieved {src.retrieval_date}")
                if src.official_url:
                    st.caption(src.official_url)
                st.caption(src.summary)
        with st.expander("Limitations"):
            for l_ in rep.limitations:
                st.markdown("- " + esc(l_))
        with st.expander("Skills run and validation checks"):
            st.dataframe([sk.model_dump() for sk in rep.skills_run], width="stretch", hide_index=True)
            st.dataframe([c.model_dump() for c in rep.validation], width="stretch", hide_index=True)

        st.subheader("Download")
        st.caption(EXPORT_NOTICE)
        d1, d2 = st.columns(2)
        d1.download_button("Download Markdown report", to_markdown(rep), file_name=f"{rep.report_id}.md", mime="text/markdown")
        d2.download_button("Download JSON report", to_json(rep), file_name=f"{rep.report_id}.json", mime="application/json")


# ---------------------------------------------------------------------------
# Ask tab
# ---------------------------------------------------------------------------
with tab_ask:
    prep = st.session_state.get("prepared")
    rep = st.session_state.get("report")
    if prep is None or rep is None:
        st.info("Analyze a document (or run a demo) first. Answers are grounded only in that document.")
    elif [p.text for p in rep.evidence] != [p.text for p in prep.all_paragraphs]:
        st.warning("The current report was made from a different document than the one now loaded. "
                   "Run the analysis again before asking follow-up questions.")
    else:
        qa_mode = "live" if rep.mode == "live" else "demo"
        if qa_mode == "live":
            st.warning("Sending a question shares your question and the previewed document paragraphs with Anthropic's API, "
                       "under the same terms as the analysis. ConsentGuard keeps answers only in this session.")
        else:
            st.info("Demo mode answers by keyword matching: it shows the most related passages, not an AI interpretation.")
        question = st.text_input("Ask about this document (e.g. 'How long do they keep my data?')", max_chars=500)
        if st.button("Ask", disabled=not question.strip() or (qa_mode == "live" and not api_key_present())):
            try:
                st.session_state["qa"].insert(0, answer_question(question, prep, rep, qa_mode))
            except LLMError as e:
                st.error(f"Could not answer: {e}")
        for a in st.session_state.get("qa", []):
            with st.container(border=True):
                st.markdown(f"**Q:** {esc(a.question)}")
                label = {"answered_from_document": "From the document", "not_in_document": "Not found in the document",
                         "general_guidance": "General guidance (not from the document)", "unverified": "Unverified"}[a.answer_type]
                st.markdown(f"*{label}* | method: {a.method.replace('_', ' ')}")
                st.markdown(esc(a.answer))
                for q in a.quotes:
                    st.markdown(f"> {esc(q.quote)}  \n> — `{q.evidence_id}`")
                if a.note:
                    st.caption(a.note)


# ---------------------------------------------------------------------------
# How it works
# ---------------------------------------------------------------------------
def _skill_description(name: str) -> str:
    text = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


with tab_how:
    st.subheader("What ConsentGuard does")
    st.markdown(
        "- Explains a privacy notice, consent form, or permission text in plain English.\n"
        "- Checks whether each data request fits the stated purpose (proportionality).\n"
        "- Reviews consent design using only the evidence supplied.\n"
        "- Links concerns to **verified** Indian legal sources and states whether each is in force today.\n"
        "- Suggests questions and steps that **you** control.\n\n"
        "It keeps four things separate: **what the document says** (quoted, with paragraph IDs), **what ConsentGuard infers or "
        "recommends**, **what verified law establishes**, and **what remains unknown**."
    )
    st.subheader("What it does not do")
    st.markdown(
        "- It does not certify compliance or safety, and it is not legal advice.\n"
        "- It does not know whether an organisation follows its own policy.\n"
        "- It does not accept terms, change permissions, contact companies, or file complaints.\n"
        "- It does not run OCR on scanned PDFs, crawl URLs, or monitor policy versions (future work)."
    )
    st.subheader("Pipeline: one agent, nine reusable skills")
    st.code(
        "document-intake (code)\n"
        "  -> [one model call or demo fixture] evidence-extraction, plain-language-explanation,\n"
        "     purpose-proportionality, consent-design-review, user-action-plan\n"
        "  -> jurisdiction-check (code; legal registry only)\n"
        "  -> findings-prioritization (code; rule caps)\n"
        "  -> report-and-qa (code; ID + exact-quote validation, labels, exports)",
        language="text",
    )
    st.dataframe([{"Skill": n, "Version": v, "Description": _skill_description(n)} for n, v in SKILL_VERSIONS.items()],
                  width="stretch", hide_index=True)
    st.subheader("Rules and severity")
    cfg = R.load_rules()
    st.markdown(f"Canonical rules: `rules/governance_rules.json` v{cfg['rule_set_version']}. {cfg['status_note']}")
    for k, v in cfg["severity_definitions"].items():
        st.markdown(f"- **{k}**: {v}")
    st.markdown("Confidence describes how well the text supports a finding, not how likely harm is. Missing evidence lowers confidence; it never raises severity.")
    st.subheader("Legal status (verified 2026-10-08 from official Gazette PDFs)")
    reg = R.load_legal_registry()
    st.markdown(
        "- The DPDP Act, 2023 commences in phases under **G.S.R. 843(E)** (13 Nov 2025). Notice, consent, legitimate-use, "
        "erasure and rights provisions (ss.3-17) start **eighteen months** after publication (about 13 May 2027).\n"
        "- The DPDP Rules, 2025 (**G.S.R. 846(E)**) follow the same phasing; consent-manager registration starts after one year.\n"
        "- So today ConsentGuard cites these provisions as **verified but not yet in force**, which means context rather than current obligations.\n"
        "- Consent is not the only ground: s.4 also allows processing for 'certain legitimate uses' (s.7)."
    )
    st.caption(reg["important_note"])
    st.subheader("How ConsentGuard handles your data")
    st.markdown(
        f"- Session-only: documents, reports and answers live in this browser session's memory. No database, no files written, "
        f"no analytics (Streamlit usage statistics are disabled in `.streamlit/config.toml`).\n"
        f"- Uploaded files are read in memory and never executed. Text is shown as plain text, not HTML.\n"
        f"- Live mode sends only the previewed text, after you confirm. Redaction is optional and best-effort.\n"
        f"- Limits: {LIMITS_TEXT}\n"
        "- Reset clears app-managed state. Data already sent to Anthropic is subject to Anthropic's retention policy."
    )


# ---------------------------------------------------------------------------
# Demo examples
# ---------------------------------------------------------------------------
with tab_demo:
    st.markdown("Eight **synthetic** documents (fictional organisations, invented details). Each demo replays a **pre-authored** "
                "analysis through the same validation pipeline used in live mode: quote checks, severity caps, legal registry. "
                "No API key or network is needed.")
    for s in list_scenarios():
        with st.container(border=True):
            st.markdown(f"**{esc(s['title'])}**")
            c1, c2 = st.columns([1, 3])
            if c1.button("Run this demo", key=f"demo_{s['id']}"):
                run_demo_scenario(s["id"])
                st.session_state["flash"] = f"Demo report ready for: {s['title']}. Open the Report tab."
                st.rerun()
            with c2.expander("View synthetic document"):
                st.text(scenario_text(get_scenario(s["id"])))

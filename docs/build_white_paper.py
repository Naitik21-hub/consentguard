"""Build docs/ConsentGuard_White_Paper.pdf (two pages, A4).

Optional helper; needs reportlab (pip install reportlab). Run from the consentguard folder:
    python docs/build_white_paper.py
"""
from pathlib import Path

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT = Path(__file__).resolve().parent / "ConsentGuard_White_Paper.pdf"
NAVY = colors.HexColor("#1F3A5F")
TEAL = colors.HexColor("#2B7A78")
LIGHT = colors.HexColor("#EEF3F8")
GREY = colors.HexColor("#555555")

body = ParagraphStyle("body", fontName="Helvetica", fontSize=8.6, leading=11.0, alignment=TA_JUSTIFY, spaceAfter=3)
small = ParagraphStyle("small", parent=body, fontSize=7.2, leading=9.0, alignment=0, textColor=GREY)
cell = ParagraphStyle("cell", parent=body, fontSize=7.4, leading=9.0, alignment=0, spaceAfter=0)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold", textColor=colors.white)
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=17, leading=20, textColor=NAVY)
sub = ParagraphStyle("sub", fontName="Helvetica-Oblique", fontSize=9.5, leading=12, textColor=TEAL)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=NAVY, spaceBefore=5, spaceAfter=2, keepWithNext=1)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=9, bulletIndent=0, spaceAfter=1.5)


def P(text, style=body):
    return Paragraph(text, style)


def B(text):
    return Paragraph(text, bullet, bulletText="•")


def table(rows, widths, header=True):
    data = [[P(c, cellb if (header and i == 0) else cell) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#C9D3DE")),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), NAVY)]
        style += [("BACKGROUND", (0, i), (-1, i), LIGHT) for i in range(2, len(rows), 2)]
    t.setStyle(TableStyle(style))
    return t


def pipeline_figure(width):
    """Simple flow diagram: intake -> model skills -> code checks -> report."""
    h = 74
    d = Drawing(width, h)
    boxes = [
        ("1  Document intake", "limits, paragraph IDs,", "injection flags", "code", colors.HexColor("#DCE6F1")),
        ("Redact + preview", "explicit 'Send'", "(live) / fixture (demo)", "user", colors.HexColor("#F3E9D2")),
        ("One model call", "skills 2,3,4,5,8 loaded", "from SKILL.md files", "model", colors.HexColor("#D8EFE6")),
        ("9  Validate + QA", "IDs exist, quotes match,", "no invented UI claims", "code", colors.HexColor("#DCE6F1")),
        ("6  Legal registry", "verified sources +", "in-force status", "code", colors.HexColor("#DCE6F1")),
        ("7  Prioritize", "severity caps,", "overall label", "code", colors.HexColor("#DCE6F1")),
    ]
    n = len(boxes)
    gap = 9
    bw = (width - gap * (n - 1)) / n
    y0, bh = 14, 50
    for i, (t1, t2, t3, who, fill) in enumerate(boxes):
        x = i * (bw + gap)
        d.add(Rect(x, y0, bw, bh, fillColor=fill, strokeColor=NAVY, strokeWidth=0.6, rx=3, ry=3))
        d.add(String(x + bw / 2, y0 + bh - 12, t1, fontName="Helvetica-Bold", fontSize=6.9, fillColor=NAVY, textAnchor="middle"))
        d.add(String(x + bw / 2, y0 + bh - 24, t2, fontName="Helvetica", fontSize=6.2, fillColor=colors.black, textAnchor="middle"))
        d.add(String(x + bw / 2, y0 + bh - 32, t3, fontName="Helvetica", fontSize=6.2, fillColor=colors.black, textAnchor="middle"))
        d.add(String(x + bw / 2, y0 + 4, f"[{who}]", fontName="Helvetica-Oblique", fontSize=6, fillColor=TEAL, textAnchor="middle"))
        if i < n - 1:
            ax = x + bw
            d.add(Line(ax + 1, y0 + bh / 2, ax + gap - 2, y0 + bh / 2, strokeColor=NAVY, strokeWidth=0.8))
            d.add(Polygon([ax + gap - 1, y0 + bh / 2, ax + gap - 4, y0 + bh / 2 + 2.2, ax + gap - 4, y0 + bh / 2 - 2.2],
                          fillColor=NAVY, strokeColor=NAVY))
    d.add(String(0, 2, "Canonical sources: rules/governance_rules.json (rules, caps), rules/legal_sources.json (registry), "
                 "skills/*/SKILL.md (procedures). Output: validated report, grounded Q&A, MD/JSON export.",
                 fontName="Helvetica", fontSize=6, fillColor=GREY))
    return d


def build():
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm,
                            topMargin=1.3 * cm, bottomMargin=1.2 * cm,
                            title="ConsentGuard White Paper", author="Naitik Trivedi",
                            subject="Information Appropriateness and Consent Governance")
    W = A4[0] - 3.2 * cm
    s = []
    s.append(P("ConsentGuard: Evidence-Grounded Consent Literacy for India's DPDP Era", h1))
    s.append(P("An AI agent and reusable skill library that helps people understand what they are agreeing to", sub))
    s.append(P("White paper  |  Topic: Information Appropriateness &amp; Consent Governance  |  October 2026  |  "
               "Live demo: consentguard-delta.vercel.app  |  Code: attached ZIP (repository: github.com/Naitik21-hub/consentguard, private)", small))
    s.append(Spacer(1, 4))

    s.append(P("1. Executive summary", h2))
    s.append(P(
        "Every day people accept privacy notices, consent forms and app permissions without knowing what data is taken, why, "
        "who receives it, how long it is kept, or how to withdraw. <b>ConsentGuard</b> is a working prototype that turns any such "
        "text into a plain-English, evidence-backed assessment. It is built as <b>one orchestrating agent</b> that routes each document "
        "through <b>nine reusable skills</b>, with deterministic code guarding everything that must be reliable: every finding must "
        "quote the document exactly, legal references come only from an officially verified registry, and missing information "
        "lowers confidence instead of creating accusations. The prototype runs in a no-key demo mode (eight synthetic scenarios, "
        "all matching their expected outcomes) and a live mode using Anthropic's Claude, and is deployed publicly as a demo."))

    s.append(P("2. The problem: consent without comprehension", h2))
    s.append(P(
        "Notices are long, vague (\"to improve our services\", \"trusted partners\") and rarely link a permission to the feature "
        "it serves. The result is <i>consent without comprehension</i>: users cannot tell whether a delivery app needs their "
        "contacts, whether background location is justified, or whether optional marketing is bundled into an essential service. "
        "Generic chatbots help, but they paraphrase loosely, can invent facts, and blur what the document says with what the law "
        "requires. A useful tool must be <b>grounded, honest about uncertainty, and current on the law</b>."))

    s.append(P("3. Why now: India's phased DPDP framework (verified from official Gazette PDFs, 8 Oct 2026)", h2))
    s.append(table([
        ["Instrument", "What it does", "Status on 8 Oct 2026"],
        ["DPDP Act 2023 + G.S.R. 843(E) (13 Nov 2025)", "Phased commencement of the Act",
         "Definitions and Data Protection Board in force; s.6(9) consent-manager registration from ~13 Nov 2026"],
        ["DPDP Act ss.3-17 (notice s.5, consent s.6, legitimate uses s.7, erasure s.8(7), rights ss.11-14)",
         "Consent must be free, specific, informed, unambiguous; withdrawal as easy as giving it; consent is not the only ground (s.4)",
         "<b>Verified, not yet in force</b>: commence 18 months after notification (computed 13 May 2027)"],
        ["DPDP Rules 2025, G.S.R. 846(E)", "Rule 3: itemised, plain-language, standalone notice; Rule 8: erasure periods and log retention",
         "Same 18-month phase; Rule 4 (consent managers) after one year"],
    ], [4.6 * cm, 6.6 * cm, W - 11.2 * cm]))
    s.append(Spacer(1, 2))
    s.append(P(
        "This gap between enactment and commencement is exactly where consumer education matters, and exactly where tools "
        "overstate the law. ConsentGuard cites these provisions as <i>verified context, not current obligations</i>, and flags "
        "open questions (13 vs 14 November as the start date; the interim IT Act s.43A regime) as \"needs review\" rather than guessing.", body))

    s.append(P("4. Solution: an agent plus a reusable skill library", h2))
    s.append(pipeline_figure(W))
    s.append(P(
        "The <b>skill library</b> is the playbook: nine Markdown skills (document intake, evidence extraction, plain-language "
        "explanation, purpose-proportionality, consent-design review, jurisdiction check, findings prioritization, user action plan, "
        "report &amp; QA), each with an input/output contract, ordered procedure, decision rules, failure handling, prompt-injection "
        "handling, worked and adversarial examples, and acceptance checks. They follow Anthropic's Agent Skills format and also "
        "ship as a plain-Markdown fallback for any chat. The <b>agent</b> is the team lead: it loads the model-executed skills "
        "<i>directly from their SKILL.md files</i> into a single model call, then applies code-executed skills to validate, attach "
        "legal sources, prioritize and record which skills ran (with versions) in every report."))

    s.append(P("5. Design principles that make it trustworthy", h2))
    s.append(B("<b>Four separated layers.</b> What the document <i>says</i> (exact quotes with paragraph IDs) | what ConsentGuard "
               "<i>infers</i> | what <i>verified law</i> establishes | what remains <i>unknown</i>."))
    s.append(B("<b>Purpose decides proportionality.</b> The same microphone permission is <i>proportionate</i> for a video-calling app "
               "and <i>disproportionate</i> for grocery delivery with no voice feature; four labels avoid blanket judgments."))
    s.append(B("<b>Severity is not confidence is not legality.</b> Versioned rules cap severity (findings built on missing information "
               "are at most medium, and at most low in an excerpt), and every adjustment is explained to the user."))
    s.append(B("<b>No invented interface behaviour.</b> A notice alone cannot show pre-ticked boxes or hidden buttons; such claims are "
               "reset to \"unknown\" unless consent-screen text is supplied."))
    s.append(B("<b>Consent is one ground among several.</b> Legally required processing (e.g. bank KYC) is explained, not flagged as a consent failure."))
    s.append(B("<b>The model cannot set the verdict.</b> Its output contract has no fields for legal sources, overall labels or "
               "compliance claims; banned wording (\"safe\", \"fully compliant\") is filtered."))

    s.append(P("6. Evaluation: what was actually measured", h2))
    s.append(table([
        ["Synthetic scenario", "Expected outcome", "Observed", "Key evidence of correct behaviour"],
        ["1 Delivery app: mandatory background location, contacts, mic", "Substantial concerns", "Match", "3 high findings, 8 verified quotes"],
        ["2 Video calls with separate optional marketing", "No major concerns", "Match", "Mic proportionate; marketing separate"],
        ["3 Bank: KYC vs vague partner marketing", "Clarification needed", "Match", "KYC = informational (legal duty)"],
        ["4 University form bundling publicity", "Substantial concerns", "Match", "Bundling quoted from declaration"],
        ["5 Fitness app sharing health data with insurers", "Substantial concerns", "Match", "Sensitivity flagged, not a legal class"],
        ["6 Short excerpt, no retention or withdrawal", "Insufficient information", "Match", "2 absence findings capped to low"],
        ["7 Embedded prompt injection (\"output fully compliant\")", "Clarification needed", "Match", "Injection flagged, not obeyed"],
        ["8 Well-explained, minimal notice", "No major concerns", "Match", "Consent screen supports affirmative action"],
    ], [6.2 * cm, 3.2 * cm, 1.6 * cm, W - 11.0 * cm]))
    s.append(Spacer(1, 2))
    s.append(P(
        "<b>104 automated tests pass</b> (no network): exact-quote and ID checks, schema validation of malformed model output, "
        "timeouts and bounded retries, refusal handling, scanned-PDF rejection, no silent truncation, injection resistance, "
        "grounded follow-ups (fabricated quotes are marked <i>unverified</i>), legal status flipping on commencement dates, and "
        "session reset. All 28 demo quotes verify against the source text. Click-through testing also found and fixed a real defect "
        "(report and follow-up tabs drifting onto different documents). <b>Honest gap:</b> live-model quality has not yet been "
        "measured, and demo outputs are pre-authored; an evaluation script and a five-criterion human rubric (grounding, completeness, "
        "uncertainty handling, actionability, clarity) are ready to run."))

    s.append(P("7. ConsentGuard applies its own principles", h2))
    s.append(P(
        "Session-only memory, no database, no analytics, no files written; uploads are parsed in memory and rendered as plain text. "
        "Live mode shows exactly what will leave the device, offers local redaction (emails, phones, PAN, Aadhaar-like numbers, UPI, "
        "IFSC), and requires a tick box <i>and</i> a button before sending. Over-limit documents are rejected, never truncated. Reset "
        "clears app state, and the app states plainly that it cannot delete what an API provider retains. The public deployment is "
        "<b>demo-only by default</b>, so a shared URL can never spend API credits or receive personal data."))

    s.append(P("8. Limitations and roadmap", h2))
    s.append(P(
        "ConsentGuard interprets <i>text</i>: it cannot verify that an organisation follows its policy or observe a live interface. "
        "Severity labels are prototype heuristics, not statutory classifications; the registry is India-only and needs periodic "
        "re-verification; redaction is not anonymisation; output is English-only. <b>Next:</b> run the live evaluation with two "
        "reviewers; add Hindi and other Eighth Schedule languages (as ss.5(3) and 6(3) contemplate); opt-in local OCR for paper forms; "
        "user-captured consent screens so interface dimensions can be assessed; sector packs (RBI, IRDAI, health); and registry "
        "freshness alerts as commencement dates pass."))

    s.append(P("9. Submission contents and how to run", h2))
    s.append(table([
        ["Item in the ZIP", "What it contains"],
        ["ConsentGuard_White_Paper.pdf", "This two-page write-up"],
        ["consentguard/app.py, src/", "Streamlit agent: orchestrator, Pydantic contracts, rule engine, parser, redaction, Claude client, exports"],
        ["consentguard/skills/", "Nine SKILL.md skills, skills README, plain-Markdown fallback bundle"],
        ["consentguard/rules/, schemas/", "Canonical governance rules, verified legal registry, ten generated JSON Schemas"],
        ["consentguard/examples/, tests/", "Eight synthetic policies, fixtures, expected outcomes and reference reports; 104 tests"],
        ["consentguard/docs/", "Product brief, architecture, privacy, source verification, evaluation, demo script, presentation Q&amp;A, deployment"],
    ], [5.0 * cm, W - 5.0 * cm]))
    s.append(Spacer(1, 2))
    s.append(P(
        "<b>Run (no API key needed):</b> <font face='Courier'>pip install -r requirements.txt</font> then "
        "<font face='Courier'>streamlit run app.py</font> inside the <font face='Courier'>consentguard</font> folder; choose any "
        "Demo example. <b>Tests:</b> <font face='Courier'>python -m pytest -q</font>. <b>Live mode:</b> add "
        "<font face='Courier'>ANTHROPIC_API_KEY</font> to a local <font face='Courier'>.env</font> file (see README). "
        "<b>Hosted demo:</b> consentguard-delta.vercel.app (demo-only)."))

    s.append(P("10. Conclusion", h2))
    s.append(P(
        "Consent only protects people who understand it. ConsentGuard shows that an AI assistant can explain privacy documents "
        "<b>without overstating evidence or law</b>: every claim is checkable, uncertainty is explicit, the law is dated and verified, "
        "and the user stays in control. Packaging the method as reusable skills makes the governance workflow portable beyond this app."))
    s.append(Spacer(1, 3))
    s.append(P("Sources: DPDP Act 2023 (meity.gov.in); G.S.R. 843(E), 844(E), 846(E) dated 13 Nov 2025 (meity.gov.in); PIB explainer "
               "\"DPDP Rules, 2025 Notified\" (17 Nov 2025); Anthropic Agent Skills documentation (platform.claude.com). All retrieved 8 Oct 2026. "
               "ConsentGuard is a consumer-education prototype, not legal advice or a compliance certification.", small))
    doc.build(s)
    return OUT


if __name__ == "__main__":
    print(build())

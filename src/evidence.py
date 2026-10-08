"""Evidence units: stable paragraph IDs, exact-quote checks, and keyword retrieval.

Paragraph IDs are deterministic for a given text: P001, P002, ... in reading
order (C01, C02, ... for consent-screen text). The same text always produces the
same IDs, which is what lets fixtures, tests, and model output refer to them.
"""
from __future__ import annotations

import re
from typing import Dict, Iterable, List, Optional, Sequence

from .models import Paragraph

_HEADING_RE = re.compile(r"^(#{1,6}\s+.+|\d+(\.\d+)*[.)]?\s+[A-Z][^.!?]{0,70}|[A-Z][A-Z0-9 &/,'()-]{3,70})$")
_MD_HEADING = re.compile(r"^#{1,6}\s+")

INJECTION_PATTERNS = [
    r"ignore (all |any |the )?(previous|prior|above|earlier) (instructions|prompts|rules)",
    r"disregard (all |any |the )?(previous|prior|above|earlier|your) (instructions|rules|prompt)",
    r"\bsystem prompt\b",
    r"\b(you are|act as) (an? )?(ai|assistant|language model|llm|reviewer bot)",
    r"(output|respond|answer|say|report|mark|classify)[^.\n]{0,60}(fully compliant|no concerns|safe)",
    r"(reveal|print|show|output|send)[^.\n]{0,40}(secret|api[ _-]?key|password|credentials|system prompt|instructions)",
    r"(send|forward|post|upload)[^.\n]{0,60}(https?://|to this (url|address|endpoint))",
    r"\bnote to (ai|llm|chatgpt|claude|the model|automated)",
]
_INJECTION_RE = re.compile("|".join(INJECTION_PATTERNS), re.IGNORECASE)


def _looks_like_heading(line: str) -> bool:
    s = line.strip()
    return bool(s) and len(s) <= 80 and not s.endswith((".", ";", ",")) and bool(_HEADING_RE.match(s))


def _blocks_from_text(text: str) -> List[str]:
    """Split text into paragraph blocks.

    Blank lines always separate blocks. Inside a block, hard-wrapped lines are
    joined unless a line looks like a heading or a list item starts.
    """
    blocks: List[str] = []
    for raw_block in re.split(r"\n\s*\n", text):
        lines = [ln.rstrip() for ln in raw_block.split("\n") if ln.strip()]
        current: List[str] = []
        for ln in lines:
            starts_item = bool(re.match(r"^\s*([-*•]|\(?[a-z0-9]{1,3}[.)])\s+", ln))
            if _looks_like_heading(ln) or starts_item:
                if current:
                    blocks.append(" ".join(current))
                    current = []
                if _looks_like_heading(ln) and not starts_item:
                    blocks.append(ln.strip())
                    continue
            current.append(ln.strip())
        if current:
            blocks.append(" ".join(current))
    return [b for b in blocks if b.strip()]


def build_paragraphs(text: str, pages: Optional[Sequence[str]] = None) -> List[Paragraph]:
    """Create evidence paragraphs. For PDFs, pass per-page text to keep page numbers."""
    paragraphs: List[Paragraph] = []
    section: Optional[str] = None
    page_texts = list(pages) if pages else [text]
    idx = 0
    for page_no, page_text in enumerate(page_texts, start=1):
        for block in _blocks_from_text(page_text):
            idx += 1
            clean = _MD_HEADING.sub("", block).strip()
            if _looks_like_heading(block):
                section = clean[:80]
            paragraphs.append(
                Paragraph(
                    evidence_id=f"P{idx:03d}",
                    text=clean,
                    page=page_no if pages else None,
                    paragraph_index=idx,
                    section=section if clean != section else None,
                )
            )
    return paragraphs


def build_consent_screen_paragraphs(text: Optional[str]) -> List[Paragraph]:
    if not text or not text.strip():
        return []
    out = []
    for i, block in enumerate(_blocks_from_text(text.replace("\r\n", "\n")), start=1):
        out.append(Paragraph(evidence_id=f"C{i:02d}", text=block, paragraph_index=i, source="consent_screen"))
    return out


# ---- Quote verification ----------------------------------------------------
_QUOTE_MAP = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", " ": " "})


def normalize(s: str) -> str:
    """Normalize only whitespace, curly quotes, and dashes. Case and words must match."""
    return re.sub(r"\s+", " ", (s or "").translate(_QUOTE_MAP)).strip()


def quote_matches(quote: str, paragraph_text: str) -> bool:
    q = normalize(quote).strip(" .\"'")
    return len(q) >= 3 and q in normalize(paragraph_text)


def index_by_id(paragraphs: Iterable[Paragraph]) -> Dict[str, Paragraph]:
    return {p.evidence_id: p for p in paragraphs}


# ---- Prompt-injection detection (flags only; never alters the workflow) -----
def detect_injection(paragraphs: Iterable[Paragraph]) -> List[str]:
    return [p.evidence_id for p in paragraphs if _INJECTION_RE.search(p.text)]


# ---- Rendering for the model ------------------------------------------------
def render_for_model(paragraphs: Iterable[Paragraph]) -> str:
    """Numbered rendering used inside <document> tags in prompts."""
    lines = []
    for p in paragraphs:
        loc = f" page={p.page}" if p.page else ""
        lines.append(f"[{p.evidence_id}{loc}] {p.text}")
    return "\n".join(lines)


# ---- Keyword retrieval (demo-mode follow-up questions) ---------------------
_STOP = set(
    "a an the and or of to in on for with by is are was were be been it this that these those what which who whom "
    "how why when where do does did can could will would should may might my me i you your we our they their them "
    "about from as at if not no yes any all there here have has had app service data policy".split()
)
_SYNONYMS = {
    "keep": ["retain", "retention", "store", "stored", "delete", "deletion", "period"],
    "delete": ["deletion", "erase", "erasure", "retain", "retention"],
    "share": ["sharing", "shared", "disclose", "disclosure", "partners", "third", "recipients", "sell"],
    "sell": ["sale", "sold", "partners", "advertisers", "share"],
    "withdraw": ["withdrawal", "withdrawing", "revoke", "opt", "unsubscribe", "settings"],
    "stop": ["withdraw", "opt", "unsubscribe", "revoke"],
    "location": ["gps", "location", "background", "address"],
    "marketing": ["promotional", "offers", "advertising", "newsletter"],
    "contact": ["grievance", "officer", "email", "complaint"],
    "complain": ["grievance", "complaint", "board", "officer"],
    "microphone": ["audio", "voice", "microphone"],
}


def _terms(s: str) -> List[str]:
    words = [w for w in re.findall(r"[a-z]+", s.lower()) if w not in _STOP and len(w) > 2]
    expanded = list(words)
    for w in words:
        for key, syns in _SYNONYMS.items():
            if w.startswith(key) or key.startswith(w):
                expanded.extend(syns)
    return expanded


def keyword_retrieve(question: str, paragraphs: Sequence[Paragraph], k: int = 3) -> List[Paragraph]:
    q_terms = set(_terms(question))
    if not q_terms:
        return []
    scored = []
    for p in paragraphs:
        if len(p.text.split()) < 4:  # skip bare headings; they are not answers
            continue
        p_words = set(re.findall(r"[a-z]+", p.text.lower()))
        score = sum(1 for t in q_terms if any(w.startswith(t) for w in p_words))
        if score > 0:
            scored.append((score, p.paragraph_index, p))
    scored.sort(key=lambda x: (-x[0], x[1]))
    if not scored:
        return []
    best = scored[0][0]
    # Require a minimally meaningful overlap to avoid presenting noise as an answer:
    # short questions need one matching term, longer ones need two.
    core = {w for w in re.findall(r"[a-z]+", question.lower()) if w not in _STOP and len(w) > 2}
    if best < (1 if len(core) <= 3 else 2):
        return []
    return [p for s, _, p in scored[:k] if s >= max(1, best - 1)]

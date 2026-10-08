"""Turn pasted text, .txt/.md files, or text-based PDFs into plain text.

Design rules (see docs/privacy_and_limitations.md):
* Uploaded files are read from memory; nothing is written to disk.
* Uploaded content is never executed or rendered as HTML.
* Over-limit input is rejected with a clear message, never silently truncated.
* Image-only (scanned) PDFs are detected and rejected; no text is invented.
"""
from __future__ import annotations

import io
from dataclasses import dataclass, field
from typing import List, Optional

# ---- Limits (shown to the user in the app) ---------------------------------
MAX_FILE_BYTES = 5 * 1024 * 1024  # 5 MB upload
MAX_PDF_PAGES = 40
MAX_CHARS = 60_000  # roughly 15k tokens; bounds API cost per analysis
MIN_CHARS = 80
SUPPORTED_EXTENSIONS = (".txt", ".md", ".pdf")

LIMITS_TEXT = (
    f"Limits: up to {MAX_CHARS:,} characters of text, {MAX_PDF_PAGES} PDF pages, "
    f"{MAX_FILE_BYTES // (1024 * 1024)} MB per file. Longer documents are rejected, "
    "not cut short: split them and analyze each part, marking each as an excerpt."
)


class ParseError(Exception):
    """Raised when a document cannot be used. The message is user-facing."""


@dataclass
class ParsedDocument:
    text: str
    source_type: str  # paste | txt | md | pdf
    pages: Optional[List[str]] = None  # PDF only: text per page
    warnings: List[str] = field(default_factory=list)
    parse_quality: str = "good"


def _check_length(text: str) -> None:
    n = len(text)
    if n > MAX_CHARS:
        raise ParseError(
            f"This document has {n:,} characters, above the {MAX_CHARS:,}-character limit. "
            "ConsentGuard does not silently cut documents short. Please split it into parts "
            "(for example by section), analyze each part separately, and mark each as an excerpt."
        )
    if n < MIN_CHARS:
        raise ParseError(
            f"Only {n} characters were found. Please supply at least {MIN_CHARS} characters of "
            "policy, consent-form, or permission text."
        )


def parse_pasted(text: str) -> ParsedDocument:
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    _check_length(text)
    return ParsedDocument(text=text, source_type="paste")


def parse_upload(filename: str, data: bytes) -> ParsedDocument:
    name = (filename or "").lower()
    if len(data) > MAX_FILE_BYTES:
        raise ParseError(
            f"The file is {len(data) / 1_048_576:.1f} MB, above the "
            f"{MAX_FILE_BYTES // 1_048_576} MB limit."
        )
    if name.endswith((".txt", ".md")):
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = data.decode("latin-1")
            warn = "File was not valid UTF-8; decoded as Latin-1. Check that special characters look right."
        else:
            warn = None
        doc = parse_pasted(text)
        doc.source_type = "md" if name.endswith(".md") else "txt"
        if warn:
            doc.warnings.append(warn)
            doc.parse_quality = "partial"
        return doc
    if name.endswith(".pdf"):
        return parse_pdf(data)
    raise ParseError(
        "Unsupported file type. Please upload .txt, .md, or a text-based .pdf, or paste the text."
    )


def parse_pdf(data: bytes) -> ParsedDocument:
    try:
        from pypdf import PdfReader
        from pypdf.errors import PdfReadError
    except ImportError as exc:  # pragma: no cover - dependency missing
        raise ParseError("PDF support needs the 'pypdf' package (pip install -r requirements.txt).") from exc

    try:
        reader = PdfReader(io.BytesIO(data))
        if reader.is_encrypted:
            raise ParseError("This PDF is password-protected. ConsentGuard does not ask for or use passwords.")
        n_pages = len(reader.pages)
    except ParseError:
        raise
    except (PdfReadError, ValueError, OSError, Exception) as exc:  # noqa: BLE001 - any parser failure
        raise ParseError(f"The PDF could not be read ({type(exc).__name__}). It may be damaged.") from exc

    if n_pages > MAX_PDF_PAGES:
        raise ParseError(
            f"This PDF has {n_pages} pages, above the {MAX_PDF_PAGES}-page limit. "
            "Please split it and analyze each part as an excerpt."
        )

    pages: List[str] = []
    empty_pages: List[int] = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            t = page.extract_text() or ""
        except Exception:  # noqa: BLE001 - pypdf can raise many types on odd pages
            t = ""
        t = t.replace("\r\n", "\n").replace("\r", "\n").strip()
        if len(t) < 20:
            empty_pages.append(i)
        pages.append(t)

    total = sum(len(p) for p in pages)
    if total < MIN_CHARS or len(empty_pages) == n_pages:
        raise ParseError(
            "No usable text layer was found in this PDF. It looks like a scanned or image-only "
            "document. ConsentGuard does not run OCR in this prototype and will not guess the "
            "content. Please paste the text or upload a text-based PDF."
        )

    warnings: List[str] = []
    quality = "good"
    if empty_pages:
        quality = "partial"
        warnings.append(
            "No text could be extracted from page(s) "
            + ", ".join(map(str, empty_pages))
            + ". They may be images. Findings do not cover those pages."
        )
    warnings.append(
        "PDF text extraction can merge columns, split words, or drop tables. Check quoted "
        "evidence against the original PDF."
    )
    text = "\n\n".join(pages)
    _check_length(text)
    return ParsedDocument(text=text, source_type="pdf", pages=pages, warnings=warnings, parse_quality=quality)

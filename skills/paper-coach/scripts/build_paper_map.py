#!/usr/bin/env python3
"""Build a structural and PDF-page text map for Paper Coach.

Optional dependencies:
- Miyo CLI for PDF -> Markdown/JSON structure.
- Poppler pdftotext for 1-indexed PDF page boundaries.

The script itself uses only Python's standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path


CAPTION_RE = re.compile(
    r"^(?:\*\*)?\s*(?:"
    r"figure|fig\.?|table|"
    r"图|表|圖|"
    r"figura|figur|abbildung|tabelle|tableau|"
    r"図|그림|표"
    r")\s*[\w.\-]+",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def fail(message: str, code: int = 1) -> None:
    print(json.dumps({"ok": False, "error": message}, ensure_ascii=False))
    raise SystemExit(code)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[*_`<>#]", " ", text)
    text = re.sub(r"[^\w\s.\-]+", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip().casefold()


def find_page(text: str, pages: list[str]) -> int | None:
    needle = normalize(text)
    if not needle:
        return None

    candidates: list[str] = []
    for limit in (180, 120, 80, 50, 30):
        if len(needle) >= limit:
            candidates.append(needle[:limit].rstrip())
    words = needle.split()
    if words:
        candidates.append(" ".join(words[: min(10, len(words))]))
    candidates.append(needle)

    seen: set[str] = set()
    unique = []
    for candidate in candidates:
        if candidate and candidate not in seen:
            unique.append(candidate)
            seen.add(candidate)

    normalized_pages = [normalize(page) for page in pages]
    for candidate in unique:
        hits = [i for i, page in enumerate(normalized_pages, 1) if candidate in page]
        if hits:
            return hits[0]
    return None


def find_miyo() -> str | None:
    candidates = [Path.home() / ".miyo" / "bin" / "miyo"]
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        candidates.append(Path(local_app_data) / "Miyo" / "bin" / "miyo" / "miyo.exe")
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return shutil.which("miyo") or shutil.which("miyo.exe")


def run_miyo(pdf: Path) -> dict:
    miyo = find_miyo()
    if not miyo:
        fail(
            "Miyo was not found. Use your harness-native PDF reader, or install Miyo "
            "and retry. The Paper Coach workflow does not require this helper.",
            2,
        )
    proc = subprocess.run(
        [miyo, "parse", str(pdf), "--json"],
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    if proc.returncode != 0:
        fail(f"miyo parse failed (exit {proc.returncode}): {proc.stderr.strip()}", 3)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        fail(f"miyo returned invalid JSON: {exc}", 3)


def run_pdftotext(pdf: Path) -> tuple[list[str], str | None]:
    executable = shutil.which("pdftotext") or shutil.which("pdftotext.exe")
    if not executable:
        return [], "pdftotext not found; page mapping unavailable"
    proc = subprocess.run(
        [executable, "-layout", str(pdf), "-"],
        capture_output=True,
        timeout=300,
        check=False,
    )
    if proc.returncode != 0:
        error = proc.stderr.decode("utf-8", errors="replace").strip()
        return [], f"pdftotext failed (exit {proc.returncode}): {error}"
    text = proc.stdout.decode("utf-8", errors="replace")
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages, None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build Markdown structure and 1-indexed PDF page text for Paper Coach."
    )
    parser.add_argument("pdf", help="Local PDF path")
    parser.add_argument("--out-dir", required=True, help="Output directory")
    args = parser.parse_args()

    pdf = Path(args.pdf).expanduser().resolve()
    if not pdf.exists() or not pdf.is_file():
        fail(f"PDF not found: {pdf}", 2)
    if pdf.suffix.casefold() != ".pdf":
        fail(f"Expected a .pdf file: {pdf}", 2)

    out_dir = Path(args.out_dir).expanduser().resolve()
    pages_dir = out_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    parsed = run_miyo(pdf)
    markdown = parsed.get("text") or ""
    markdown_path = out_dir / "paper.md"
    markdown_path.write_text(markdown, encoding="utf-8")

    pages, page_error = run_pdftotext(pdf)
    for number, page_text in enumerate(pages, 1):
        (pages_dir / f"page-{number:03d}.txt").write_text(page_text, encoding="utf-8")

    headings = []
    captions = []
    for line_number, line in enumerate(markdown.splitlines(), 1):
        heading_match = HEADING_RE.match(line)
        if heading_match:
            heading_text = heading_match.group(2).strip()
            headings.append(
                {
                    "level": len(heading_match.group(1)),
                    "text": heading_text,
                    "markdown_line": line_number,
                    "pdf_page": find_page(heading_text, pages) if pages else None,
                }
            )
        stripped = line.strip()
        if CAPTION_RE.match(stripped):
            captions.append(
                {
                    "text": stripped,
                    "markdown_line": line_number,
                    "pdf_page": find_page(stripped, pages) if pages else None,
                }
            )

    title = parsed.get("title")
    if not title and headings:
        title = headings[0]["text"]

    map_path = out_dir / "map.json"
    result = {
        "ok": True,
        "source_pdf": str(pdf),
        "title": title,
        "metadata": {
            "page_count_reported": parsed.get("page_count"),
            "page_count_mapped": len(pages),
            "failed_page_count": parsed.get("failed_page_count"),
            "pdf_type": parsed.get("pdf_type"),
            "pages_needing_ocr": parsed.get("pages_needing_ocr") or [],
            "page_mapping_available": bool(pages),
            "page_mapping_error": page_error,
        },
        "artifacts": {
            "markdown": str(markdown_path),
            "map": str(map_path),
            "pages_dir": str(pages_dir) if pages else None,
        },
        "headings": headings,
        "captions": captions,
    }
    map_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "ok": True,
        "title": title,
        "page_count_reported": parsed.get("page_count"),
        "page_count_mapped": len(pages),
        "failed_page_count": parsed.get("failed_page_count"),
        "pages_needing_ocr": parsed.get("pages_needing_ocr") or [],
        "heading_count": len(headings),
        "caption_count": len(captions),
        "map": str(map_path),
        "markdown": str(markdown_path),
        "page_mapping_error": page_error,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

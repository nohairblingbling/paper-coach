#!/usr/bin/env python3
"""Validate the public Paper Coach repository without third-party packages."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "paper-coach"
SKILL_MD = SKILL_DIR / "SKILL.md"
README = ROOT / "README.md"
VIDEO_URL = "https://www.youtube.com/watch?v=733m6qBH-jI"


def frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    marker = "\n---\n"
    index = text.find(marker, 4)
    if index < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    return text[4:index], text[index + len(marker) :]


def scalar(field: str, block: str) -> str | None:
    match = re.search(rf"^{re.escape(field)}:\s*(.+?)\s*$", block, re.MULTILINE)
    return match.group(1).strip().strip('"\'') if match else None


def referenced_files(text: str) -> set[str]:
    found = set()
    for pattern in (
        r"\((references/[^)#\s]+|examples/[^)#\s]+|scripts/[^)#\s]+)\)",
        r"`(references/[^`]+|examples/[^`]+|scripts/[^`]+)`",
    ):
        found.update(re.findall(pattern, text))
    return found


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    required = [
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / "CITATION.cff",
        ROOT / "CHANGELOG.md",
        ROOT / "CONTRIBUTING.md",
        SKILL_MD,
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")

    if not SKILL_MD.is_file():
        print(json.dumps({"ok": False, "errors": errors}, indent=2))
        return 1

    text = SKILL_MD.read_text(encoding="utf-8")
    try:
        fm, body = frontmatter(text)
    except ValueError as exc:
        errors.append(str(exc))
        fm, body = "", ""

    name = scalar("name", fm)
    description = scalar("description", fm)
    compatibility = scalar("compatibility", fm)
    license_name = scalar("license", fm)

    if name != SKILL_DIR.name:
        errors.append(f"name must match parent directory: {name!r} != {SKILL_DIR.name!r}")
    if not name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("name must use lowercase letters, numbers, and single hyphens")
    if not description or not 1 <= len(description) <= 1024:
        errors.append("description must contain 1-1024 characters")
    if compatibility and len(compatibility) > 500:
        errors.append("compatibility must not exceed 500 characters")
    if license_name != "MIT":
        errors.append("frontmatter license must be MIT")
    if not body.strip():
        errors.append("SKILL.md body is empty")

    references = sorted(referenced_files(text))
    for relative in references:
        if not (SKILL_DIR / relative).is_file():
            errors.append(f"dangling skill reference: {relative}")

    expected_refs = {
        "references/andrew-ng-method.md",
        "references/modes-and-state-machine.md",
        "references/extraction-and-grounding.md",
        "examples/quick-session.md",
        "examples/deep-session.md",
        "scripts/build_paper_map.py",
    }
    missing_mentions = sorted(expected_refs - set(references))
    if missing_mentions:
        errors.append(f"SKILL.md does not reference packaged support files: {missing_mentions}")

    public_text_files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in {".md", ".py", ".yml", ".yaml", ".cff", ".txt"}
    ]
    home_prefixes = {str(Path.home().resolve()) + "/"}
    for path in public_text_files:
        content = path.read_text(encoding="utf-8")
        if any(prefix in content for prefix in home_prefixes):
            errors.append(f"machine-local absolute path in {path.relative_to(ROOT)}")

    if README.is_file():
        readme = README.read_text(encoding="utf-8")
        for required_text in ("# English", "# 简体中文", VIDEO_URL, "npx skills@latest", "hermes skills install"):
            if required_text not in readme:
                errors.append(f"README missing required content: {required_text}")
        if "not affiliated" not in readme.lower() or "不存在隶属" not in readme:
            warnings.append("README disclaimer may be incomplete")

    helper = SKILL_DIR / "scripts" / "build_paper_map.py"
    if helper.is_file():
        compile_result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(helper)],
            capture_output=True,
            text=True,
            check=False,
        )
        if compile_result.returncode:
            errors.append(f"helper syntax error: {compile_result.stderr.strip()}")

    result = {
        "ok": not errors,
        "skill": name,
        "description_chars": len(description or ""),
        "support_files_referenced": len(references),
        "public_text_files_checked": len(public_text_files),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

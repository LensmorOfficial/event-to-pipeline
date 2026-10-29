#!/usr/bin/env python3
"""Check the local candidate's bundle, worked artifacts, links and public scope."""

import re
import sys
from pathlib import Path

from render_examples import render_all
from validate_mcp_bundle import ROOT, validate
from validate_metadata import validate_repository


EXCLUDED = {".git", ".qa-deps", ".venv", "__pycache__", "dist", "test-results"}


def public_files(root=ROOT):
    for path in sorted(Path(root).rglob("*")):
        relative = path.relative_to(root)
        if any(part in EXCLUDED for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError("A public release cannot contain symlinks.")
        if path.is_file():
            if path.name.startswith(".env"):
                raise ValueError("Environment files do not belong in the public candidate.")
            yield path


def check(root=ROOT):
    root = Path(root)
    paths, errors = validate_repository(root)
    if len(paths) != 15:
        errors.append("The 15 legacy root Skill directories must remain intact.")
    validate(root)
    for name, text in render_all(root).items():
        path = root / "examples" / name
        if not path.exists() or path.read_bytes() != text.encode("utf-8"):
            errors.append(f"Stale worked-example artifact: {name}")
    for path in public_files(root):
        relative = path.relative_to(root).as_posix()
        if path.suffix == ".html":
            errors.append(f"Unexpected HTML application: {relative}")
        if path.suffix in {".md", ".json", ".toml", ".yaml", ".yml", ".txt"}:
            text = path.read_text(encoding="utf-8-sig")
            if re.search(r"[A-Za-z]:[\\/](?:Users|project)[\\/]", text):
                errors.append(f"Absolute maintainer path in {relative}")
            if re.search(r"https?://(?:git|gitlab|scm)\.(?!github\.com)", text):
                errors.append(f"Private repository address in {relative}")
            if re.search(r"\b(?:lmh_[A-Za-z0-9_-]{20,}|sk_[A-Za-z0-9]{24,})\b", text):
                errors.append(f"Possible live handle/token in {relative}")
    if errors:
        raise ValueError("\n".join(errors))
    return len(paths)


if __name__ == "__main__":
    try:
        count = check()
    except (ValueError, KeyError, OSError) as exc:
        sys.exit(f"Candidate validation failed:\n{exc}")
    print(f"PASS: {count} legacy Skills, generated research bundle, reproducible examples, links and public file checks.")

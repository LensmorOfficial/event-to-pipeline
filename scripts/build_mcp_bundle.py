#!/usr/bin/env python3
"""Generate the public research bundle from a maintainer-supplied canonical source."""

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
ISC = """ISC License

Copyright (c) 2026 Lensmor

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED \"AS IS\" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

EXPORT_NOTE = """
## Optional local CSV export

When the user asks for an event directory CSV and has a REST API key, use the
bundled `scripts/export_exhibitors.py` (Python 3.11+, standard library only).
This is a separate REST path; MCP login does not supply `LENSMOR_API_KEY`.
First resolve the exact event edition using the connected tools. Run the script
relative to this Skill directory, with the confirmed ID and explicit filters:

```bash
python scripts/export_exhibitors.py --event-id EVENT_ID --max-pages 1 --output exhibitors.csv
```

`--country`, `--keyword`, repeated `--category` / `--industry`, and `--page-size`
preserve a bounded query. Raise `--max-pages` only for a user-requested larger
export. Inspect the accompanying `.metadata.json`; report previews, page limits,
and `complete_for_query` with the CSV. It is a directory query, not a model-ranked
shortlist or a confirmed-attendance list. Without a REST key, continue the MCP
workflow; do not substitute credentials or claim a file was created.
"""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def prepare(source, root=ROOT):
    # Non-strict resolution avoids Windows directory-handle ACL checks; required
    # source files are still opened explicitly and missing files fail below.
    source = Path(os.path.abspath(source)).resolve()
    root = Path(root).resolve()
    if source == root or root in source.parents or source in root.parents:
        raise ValueError("Canonical source and public checkout must be separate directories.")
    plan = json.loads((root / "integrations/mcp/bundle-plan.json").read_text(encoding="utf-8"))
    catalog_path = source / "skill-catalog.json"
    catalog_bytes = catalog_path.read_bytes()
    catalog = json.loads(catalog_bytes)
    if catalog["version"] != plan["canonical_version"]:
        raise ValueError("Canonical version changed; review the bundle plan before regenerating.")
    indexed = {skill["name"]: skill for skill in catalog["skills"]}
    names = plan["skills"]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate selected Skill.")
    files = {}
    records = []
    tools = set()
    for name in names:
        if not name or any(char not in "abcdefghijklmnopqrstuvwxyz0123456789-" for char in name):
            raise ValueError("Unsafe Skill name.")
        entry = indexed[name]
        if entry.get("requiredCapabilities"):
            raise ValueError(f"{name}: gated actions cannot enter the research-only bundle.")
        if any(not tool.startswith(("get_", "list_", "search_", "research_", "resolve_", "discover_")) for tool in entry["requiredTools"]):
            raise ValueError(f"{name}: non-research tool dependency.")
        tools.update(entry["requiredTools"])
        skill_root = source / "skills" / name
        if skill_root.is_symlink():
            raise ValueError("Canonical Skill directories cannot be symlinks.")
        source_files = sorted(path for path in skill_root.rglob("*") if path.is_file())
        if {path.relative_to(skill_root).as_posix() for path in source_files} != {"SKILL.md", "agents/openai.yaml"}:
            raise ValueError(f"{name}: new resources require explicit review in the public generator.")
        for path in source_files:
            if path.is_symlink():
                raise ValueError("Canonical resources cannot be symlinks.")
            original = path.read_bytes()
            content = original.decode("utf-8").replace("\r\n", "\n")
            if path.name == "SKILL.md":
                lines = content.splitlines(keepends=True)
                if not lines or lines[0].strip() != "---":
                    raise ValueError("Missing Skill frontmatter.")
                end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
                lines.insert(end + 1, "\n> Public research bundle: " + plan["public_scope_note"] + "\n")
                content = "".join(lines)
                if name == "research-exhibitors":
                    content = content.rstrip() + "\n" + EXPORT_NOTE
            if re.search(r"[A-Za-z]:[\\/](?:Users|project)[\\/]", content):
                raise ValueError(f"{name}: absolute maintainer path in canonical source.")
            for url in re.findall(r'https?://[^\s<>\"\)]+', content):
                if urlsplit(url).hostname not in {"platform.lensmor.com", "lensmor.com", "www.lensmor.com"}:
                    raise ValueError(f"{name}: a new source URL needs public-distribution review.")
            relative = f"{name}/{path.relative_to(skill_root).as_posix()}"
            generated = content.encode("utf-8")
            files[relative] = generated
            records.append({"path": relative, "source_sha256": digest(original), "sha256": digest(generated)})
        files[f"{name}/LICENSE"] = ISC.encode("utf-8")
        records.append({"path": f"{name}/LICENSE", "source_sha256": None, "sha256": digest(files[f"{name}/LICENSE"])})
    for resource, origin in (("export_exhibitors.py", root / "scripts/export_exhibitors.py"), ("LICENSE", root / "LICENSE")):
        relative = "research-exhibitors/scripts/" + resource
        files[relative] = origin.read_bytes()
        records.append({"path": relative, "source_path": origin.relative_to(root).as_posix(),
                        "source_sha256": digest(files[relative]), "sha256": digest(files[relative])})
    manifest = {
        "schema_version": 1,
        "version": plan["version"],
        "status": plan["status"],
        "generated_from": "Lensmor canonical Agent Skills",
        "canonical_version": catalog["version"],
        "catalog_sha256": digest(catalog_bytes),
        "transformation": "Normalize LF and add the public-research scope note; append local REST export guidance to research-exhibitors and bundle the MIT helper. Preserve canonical business instructions and UI metadata.",
        "mode": plan["mode"],
        "endpoint": plan["endpoint"],
        "license": "ISC; bundled public export helper: MIT",
        "skills": [{"name": name, "kind": indexed[name]["kind"], "required_tools": indexed[name]["requiredTools"]} for name in names],
        "required_tools": sorted(tools),
        "files": sorted(records, key=lambda item: item["path"]),
    }
    return files, manifest


def build(source, root=ROOT, check=False):
    root = Path(root).resolve()
    files, manifest = prepare(source, root)
    target = root / "skills"
    if target.is_symlink():
        raise ValueError("Output cannot be a symlink.")
    expected = files
    manifest_path = root / "integrations/mcp/bundle-manifest.json"
    manifest_bytes = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    existing = {path.relative_to(target).as_posix() for skill in manifest["skills"]
                for path in (target / skill["name"]).rglob("*") if path.is_file()}
    if existing - set(expected):
        raise ValueError("Unexpected files in generated bundle; review before regenerating.")
    for destination in [manifest_path, *(target / name for name in expected)]:
        if any(parent.is_symlink() for parent in [destination, *destination.parents] if parent != root.parent):
            raise ValueError("Output path cannot traverse a symlink.")
    if check:
        if (existing != set(expected) or not manifest_path.is_file()
                or manifest_path.read_bytes() != manifest_bytes
                or any((target / name).read_bytes() != content for name, content in expected.items())):
            raise ValueError("Generated bundle differs from the canonical source.")
    else:
        for name, content in expected.items():
            destination = target / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
        manifest_path.write_bytes(manifest_bytes)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Canonical plugin root; no credentials are needed")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        manifest = build(args.source, check=args.check)
    except (ValueError, KeyError, OSError, StopIteration) as exc:
        parser.exit(1, f"Bundle generation failed: {exc}\n")
    print(f"{'Checked' if args.check else 'Generated'} {len(manifest['skills'])} research Skills from {manifest['canonical_version']}.")


if __name__ == "__main__":
    main()

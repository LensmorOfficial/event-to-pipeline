#!/usr/bin/env python3
"""Verify public bundle integrity, its Skill metadata and research-only tool config."""

import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT, check_metadata=True):
    # End-user installation needs only the standard library; CI parses YAML too.
    if check_metadata:
        import yaml
    root = Path(root)
    folder = root / "skills"
    manifest = json.loads((root / "integrations/mcp/bundle-manifest.json").read_text(encoding="utf-8"))
    plan = json.loads((root / "integrations/mcp/bundle-plan.json").read_text(encoding="utf-8"))
    if manifest["mode"] != "read_only_research" or manifest["status"] != "preview":
        raise ValueError("Unexpected bundle scope or release status.")
    if [skill["name"] for skill in manifest["skills"]] != plan["skills"]:
        raise ValueError("Bundle selection differs from the reviewed plan.")
    if manifest["version"] != plan["version"]:
        raise ValueError("Bundle version differs from the reviewed plan.")
    actual = {path.relative_to(folder).as_posix() for name in plan["skills"]
              for path in (folder / name).rglob("*") if path.is_file()}
    expected = {entry["path"] for entry in manifest["files"]}
    required = {f"{name}/{resource}" for name in plan["skills"] for resource in ("SKILL.md", "agents/openai.yaml", "LICENSE")}
    required |= {"research-exhibitors/scripts/export_exhibitors.py", "research-exhibitors/scripts/LICENSE"}
    if expected != required:
        raise ValueError("Every selected Skill must include its instructions, agent metadata and license.")
    if actual != expected or len(expected) != len(manifest["files"]):
        raise ValueError("Unexpected, missing or duplicate bundle files.")
    for entry in manifest["files"]:
        relative = Path(entry["path"])
        if relative.is_absolute() or ".." in relative.parts or "\\" in entry["path"]:
            raise ValueError("Unsafe manifest path.")
        path = folder / relative
        if any(parent.is_symlink() for parent in [path, *path.parents] if parent != root.parent):
            raise ValueError("Symlinks are not allowed in the release.")
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            raise ValueError(f"Checksum mismatch: {entry['path']}")
        if path.name == "LICENSE" and path.parent.name != "scripts" and not raw.startswith(b"ISC License\n"):
            raise ValueError("Generated Skills must preserve their ISC license.")
        if entry["path"].startswith("research-exhibitors/scripts/"):
            original = root / ("LICENSE" if path.name == "LICENSE" else "scripts/export_exhibitors.py")
            if original.exists() and raw != original.read_bytes():
                raise ValueError("Bundled export helper differs from its public source.")
        if path.name == "SKILL.md":
            match = re.match(r"\A---\n(.*?)\n---\n", raw.decode("utf-8"), re.S)
            if not match:
                raise ValueError(f"Invalid frontmatter: {entry['path']}")
            if check_metadata:
                data = yaml.safe_load(match.group(1))
                if data["name"] != path.parent.name or not data.get("description"):
                    raise ValueError("Invalid Skill identity.")
            if "Public research bundle:" not in raw.decode("utf-8"):
                raise ValueError("Missing public-scope adaptation.")
    config = tomllib.loads((root / "integrations/mcp/codex.config.example.toml").read_text(encoding="utf-8"))
    server = config["mcp_servers"]["lensmor"]
    if server["url"] != manifest["endpoint"] or set(server["enabled_tools"]) != set(manifest["required_tools"]):
        raise ValueError("MCP example does not match the research bundle.")
    if any(not tool.startswith(("get_", "list_", "search_", "research_", "resolve_", "discover_")) for tool in server["enabled_tools"]):
        raise ValueError("Action tools are not enabled by the research template.")
    return manifest


if __name__ == "__main__":
    try:
        result = validate()
    except (ValueError, KeyError, OSError) as exc:
        sys.exit(f"MCP bundle validation failed: {exc}")
    print(f"PASS: {len(result['skills'])} generated Skills; checksums, metadata, licensing files and research-only config.")

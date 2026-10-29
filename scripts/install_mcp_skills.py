#!/usr/bin/env python3
"""Install six research Skills and the invitation writer into a chosen directory."""

import argparse
import json
import os
from pathlib import Path

from validate_mcp_bundle import ROOT, validate


def install(destination, root=ROOT, dry_run=False):
    root = Path(root).resolve()
    manifest = validate(root, check_metadata=False)
    requested = Path(os.path.abspath(destination))
    if any(part.is_symlink() for part in [requested, *requested.parents]):
        raise ValueError("Choose a destination without symlink components.")
    target = requested.resolve()
    bundle = root / "mcp-skills"
    if target == root or root in target.parents or target == bundle or target in bundle.parents:
        raise ValueError("Install into a separate project, not into this source checkout.")
    names = [skill["name"] for skill in manifest["skills"]] + ["booth-invitation-writer"]
    files = {entry["path"]: bundle / entry["path"] for entry in manifest["files"]}
    writer = root / "booth-invitation-writer"
    for path in sorted(writer.rglob("*")):
        if path.is_symlink():
            raise ValueError("Drafting Skill resources cannot be symlinks.")
        if path.is_file():
            files["booth-invitation-writer/" + path.relative_to(writer).as_posix()] = path
    files["booth-invitation-writer/LICENSE"] = root / "LICENSE"
    if "booth-invitation-writer/SKILL.md" not in files:
        raise ValueError("The drafting Skill is missing from this checkout.")
    # Read every source before creating the destination; missing files fail early.
    content = {name: path.read_bytes() for name, path in files.items()}
    conflicts = [name for name in names if (target / name).exists() or (target / name).is_symlink()]
    if conflicts:
        raise ValueError("Existing Skills were not changed: " + ", ".join(conflicts))
    receipt = {"mode": "dry_run" if dry_run else "installed", "destination": str(target), "skills": names, "version": manifest["version"], "mcp_configured": False}
    if dry_run:
        return receipt
    # Preflight all conflicts above; exclusive creation never overwrites an existing file.
    # A filesystem failure can leave a partial installation, which is reported as failure.
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        (target / name).mkdir(exist_ok=False)
        for path, data in content.items():
            relative = Path(path)
            if relative.parts[0] != name:
                continue
            output = target / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open("xb") as stream:
                stream.write(data)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.destination, dry_run=args.dry_run), ensure_ascii=False, indent=2))
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Installation did not complete: {exc}\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Package the validated local checkout, excluding Git, dependencies and local QA."""

import hashlib
import json
import zipfile
from pathlib import Path

from validate_repository import ROOT, check, public_files


def package(root=ROOT):
    root = Path(root).resolve()
    check(root)
    project = json.loads((root / "project.json").read_text(encoding="utf-8"))
    version = project["version"]
    if any(char not in "0123456789abcdefghijklmnopqrstuvwxyz.-" for char in version):
        raise ValueError("Unsafe candidate version.")
    files = list(public_files(root))
    output = root / "dist"
    if output.is_symlink():
        raise ValueError("Archive output cannot be a symlink.")
    output.mkdir(exist_ok=True)
    archive = output / f"event-to-pipeline-{version}.zip"
    if archive.is_symlink():
        raise ValueError("Archive path cannot be a symlink.")
    records = []
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as package_file:
        for path in files:
            relative = path.relative_to(root).as_posix()
            content = path.read_bytes()
            records.append({"path": relative, "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)})
            info = zipfile.ZipInfo(f"event-to-pipeline/{relative}", date_time=(2026, 10, 29, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            package_file.writestr(info, content)
    receipt = {"project": project["name"], "version": version, "status": "local_archive", "archive": archive.name, "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(), "files": records}
    (output / "release-files.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return archive, receipt


if __name__ == "__main__":
    archive, receipt = package()
    print(f"Packaged {len(receipt['files'])} public project files: {archive.name}")
    print("SHA256: " + receipt["sha256"])

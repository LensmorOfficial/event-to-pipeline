"""Exercise the self-contained distribution and its installation boundary."""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from package_release import package
from validate_repository import ROOT, check, public_files


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        for path in public_files(ROOT):
            target = self.root / path.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())

    def test_extra_skill_outside_the_catalogue_is_rejected(self):
        extra = self.root / "skills/unrelated-workflow/SKILL.md"
        extra.parent.mkdir()
        extra.write_text("---\nname: unrelated-workflow\ndescription: An unrelated workflow.\n---\n")
        with self.assertRaisesRegex(ValueError, "Skill directories differ"):
            check(self.root)

    def test_root_level_skill_is_rejected(self):
        extra = self.root / "retired-workflow/SKILL.md"
        extra.parent.mkdir()
        extra.write_text("A workflow left at the root.\n")
        with self.assertRaisesRegex(ValueError, "belong under skills"):
            check(self.root)

    def test_archive_installs_and_exports_without_the_source_checkout(self):
        for folder in (".git", ".qa-deps", "dist", "test-results"):
            path = self.root / folder / "excluded.txt"
            path.parent.mkdir()
            path.write_text("Local-only material.")
        archive, receipt = package(self.root)
        self.assertEqual(archive.name, "event-to-pipeline-0.6.0.zip")
        with zipfile.ZipFile(archive) as zipped:
            names = zipped.namelist()
            self.assertTrue(all(name.startswith("event-to-pipeline/") for name in names))
            self.assertEqual(sum(name.endswith("/SKILL.md") for name in names), 7)
            self.assertFalse(any(name.endswith("/excluded.txt") for name in names))
            for entry in receipt["files"]:
                self.assertEqual(hashlib.sha256(zipped.read("event-to-pipeline/" + entry["path"])).hexdigest(), entry["sha256"])
            extracted = Path(self.temp.name) / "extracted"
            zipped.extractall(extracted)
        checkout = extracted / "event-to-pipeline"
        check(checkout)
        target = Path(self.temp.name) / "client/skills"
        environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
        result = subprocess.run([sys.executable, "-S", str(checkout / "scripts/install_skills.py"),
                                 "--destination", str(target)], capture_output=True, text=True, env=environment)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["skills"]), 7)
        self.assertTrue((target / "booth-invitation-writer/LICENSE").is_file())
        result = subprocess.run([sys.executable, "-S", str(target / "research-exhibitors/scripts/export_exhibitors.py"),
                                 "--sample", str(checkout / "examples/exhibitor-export/sample.json"),
                                 "--max-pages", "2", "--output", str(Path(self.temp.name) / "export.csv")],
                                capture_output=True, text=True, env=environment)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["rows"], 3)

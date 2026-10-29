import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from build_mcp_bundle import build, prepare
from install_skills import install
from validate_mcp_bundle import ROOT, validate


class PublicBundleTests(unittest.TestCase):
    def test_checked_in_bundle_is_complete_and_uses_read_tools(self):
        manifest = validate()
        self.assertEqual(len(manifest["skills"]), 6)
        self.assertEqual(manifest["canonical_version"], "0.7.3")
        self.assertFalse(any(name.startswith(("quote_", "create_", "prepare_")) for name in manifest["required_tools"]))

    def test_dry_run_does_not_modify_a_target(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "project/.agents/skills"
            receipt = install(target, dry_run=True)
            self.assertEqual(receipt["mode"], "dry_run")
            self.assertFalse(target.exists())

    def test_installer_copies_complete_packages_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "project/.agents/skills"
            receipt = install(target)
            self.assertFalse(receipt["mcp_configured"])
            self.assertEqual(len(receipt["skills"]), 7)
            for name in receipt["skills"]:
                if name == "booth-invitation-writer":
                    self.assertEqual((target / name / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())
                    self.assertTrue((target / name / "examples/medica-cold-prospect.md").is_file())
                    continue
                self.assertTrue((target / name / "agents/openai.yaml").is_file())
                self.assertIn("ISC License", (target / name / "LICENSE").read_text(encoding="utf-8"))
            old = (target / "research-events/SKILL.md").read_bytes()
            with self.assertRaisesRegex(ValueError, "Existing Skills"):
                install(target)
            self.assertEqual((target / "research-events/SKILL.md").read_bytes(), old)

    def test_installed_helper_runs_without_third_party_dependencies(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "skills"
            # -S disables site packages, including PyYAML, for real CLI installation.
            environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
            result = subprocess.run([sys.executable, "-S", str(ROOT / "scripts/install_skills.py"),
                                     "--destination", str(target)], capture_output=True, text=True, env=environment)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = Path(directory) / "sample.csv"
            result = subprocess.run([sys.executable, "-S", str(target / "research-exhibitors/scripts/export_exhibitors.py"),
                                     "--sample", str(ROOT / "examples/exhibitor-export/sample.json"),
                                     "--max-pages", "2", "--output", str(output)], capture_output=True, text=True, env=environment)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["rows"], 3)

    def test_relative_sibling_install_path_is_normalized(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "skills"
            relative = os.path.relpath(target, Path.cwd())
            receipt = install(relative, dry_run=True)
            self.assertEqual(Path(receipt["destination"]), target.resolve())

    def test_drafting_conflict_prevents_research_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "skills"
            (target / "booth-invitation-writer").mkdir(parents=True)
            with self.assertRaisesRegex(ValueError, "Existing Skills"):
                install(target)
            self.assertEqual([p.name for p in target.iterdir()], ["booth-invitation-writer"])

    def test_a_single_conflict_prevents_all_skill_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "skills"
            (target / "research-events").mkdir(parents=True)
            with self.assertRaises(ValueError):
                install(target)
            self.assertEqual([path.name for path in target.iterdir()], ["research-events"])

    def test_source_checkout_is_not_an_installation_target(self):
        with self.assertRaises(ValueError):
            install(ROOT / ".agents/skills", dry_run=True)

    def test_tampered_bundle_is_rejected_before_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "candidate"
            root.mkdir()
            shutil.copytree(ROOT / "skills", root / "skills")
            shutil.copytree(ROOT / "integrations", root / "integrations")
            path = root / "skills/research-events/SKILL.md"
            path.write_text(path.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
            target = Path(directory) / "client/skills"
            with self.assertRaisesRegex(ValueError, "Checksum mismatch"):
                install(target, root=root)
            self.assertFalse(target.exists())

    def make_canonical(self, directory):
        source = Path(directory) / "canonical"
        source.mkdir()
        plan = json.loads((ROOT / "integrations/mcp/bundle-plan.json").read_text(encoding="utf-8"))
        skills = []
        for name in plan["skills"]:
            folder = source / "skills" / name
            (folder / "agents").mkdir(parents=True)
            (folder / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Research a bounded sample.\n---\n\n# Research\nPreserve unknown fields.\n", encoding="utf-8")
            (folder / "agents/openai.yaml").write_text("interface:\n  display_name: Research\n", encoding="utf-8")
            skills.append({"name": name, "kind": "scenario", "requiredTools": ["get_event"], "requiredCapabilities": []})
        catalog = {"version": plan["canonical_version"], "skills": skills}
        (source / "skill-catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
        return source, catalog

    def test_generation_is_deterministic_and_preserves_source_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            source, _ = self.make_canonical(directory)
            first_files, first_manifest = prepare(source)
            second_files, second_manifest = prepare(source)
            self.assertEqual(first_files, second_files)
            self.assertEqual(first_manifest, second_manifest)
            self.assertTrue(all(row["source_sha256"] for row in first_manifest["files"] if row["path"].endswith("SKILL.md")))
            self.assertIn("Public research bundle:", first_files["research-events/SKILL.md"].decode())

    def test_generation_accepts_a_relative_sibling_source(self):
        with tempfile.TemporaryDirectory() as directory:
            source, _ = self.make_canonical(directory)
            _, manifest = prepare(os.path.relpath(source, Path.cwd()))
            self.assertEqual(len(manifest["skills"]), 6)

    def test_generation_rejects_new_action_dependencies_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            source, catalog = self.make_canonical(directory)
            catalog["skills"][0]["requiredTools"].append("create_contact_unlock_confirmation")
            (source / "skill-catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "non-research"):
                prepare(source)

    def test_new_source_resources_require_review(self):
        with tempfile.TemporaryDirectory() as directory:
            source, _ = self.make_canonical(directory)
            (source / "skills/research-events/new-resource.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "new resources"):
                prepare(source)

    def test_generation_preserves_the_seventh_independent_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            source, _ = self.make_canonical(directory)
            checkout = Path(directory) / "checkout"
            shutil.copytree(ROOT / "integrations", checkout / "integrations")
            (checkout / "scripts").mkdir()
            shutil.copyfile(ROOT / "scripts/export_exhibitors.py", checkout / "scripts/export_exhibitors.py")
            shutil.copyfile(ROOT / "LICENSE", checkout / "LICENSE")
            writer = checkout / "skills/booth-invitation-writer/SKILL.md"
            writer.parent.mkdir(parents=True)
            writer.write_bytes(b"Keep the independent drafting workflow intact.\n")
            before = writer.read_bytes()
            build(source, root=checkout)
            build(source, root=checkout, check=True)
            self.assertEqual(writer.read_bytes(), before)
            self.assertEqual(len(list((checkout / "skills").glob("*/SKILL.md"))), 7)


if __name__ == "__main__":
    unittest.main()

"""Portable Skill frontmatter and local-reference validation."""

import tempfile
import unittest
from pathlib import Path

from validate_metadata import local_link_errors, parse_frontmatter, validate_skill

VALID = """---
name: sample-skill
description: Evaluate trade show fit using supplied evidence.
license: MIT
metadata:
  version: "1.0.0"
  homepage: https://github.com/LensmorOfficial/event-to-pipeline/tree/main/skills/sample-skill
---
# Sample Skill
"""


class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "sample-skill" / "SKILL.md"
        self.path.parent.mkdir()

    def check_invalid(self, text):
        self.path.write_text(text)
        with self.assertRaises(ValueError):
            validate_skill(self.path)

    def test_valid_metadata(self):
        self.path.write_text(VALID)
        self.assertEqual(validate_skill(self.path)["name"], "sample-skill")

    def test_field_in_body_cannot_replace_frontmatter(self):
        self.check_invalid(VALID.replace('name: sample-skill\n', '') + 'name: sample-skill\n')

    def test_duplicate_key_is_rejected(self):
        self.check_invalid(VALID.replace("name: sample-skill", "name: ignored\nname: sample-skill"))

    def test_invalid_yaml_is_rejected(self):
        self.check_invalid(VALID.replace("metadata:", "metadata: ["))

    def test_metadata_must_have_string_values(self):
        self.check_invalid(VALID.replace('version: "1.0.0"', "version: 1"))
        self.check_invalid(VALID.replace('version: "1.0.0"', 'version: {nested: value}'))

    def test_runtime_specific_top_level_fields_are_rejected(self):
        self.check_invalid(VALID.replace("license: MIT", "license: MIT\nuser-invocable: true"))
        self.check_invalid(VALID.replace("license: MIT", "license: MIT\nversion: 1.0.0"))

    def test_wrong_name_and_homepage(self):
        self.check_invalid(VALID.replace("name: sample-skill", "name: other-skill"))
        self.check_invalid(VALID.replace("skills/sample-skill", "skills/missing"))

    def test_invalid_version(self):
        self.check_invalid(VALID.replace('version: "1.0.0"', 'version: "latest"'))

    def test_invalid_compatibility(self):
        self.check_invalid(VALID.replace("license: MIT", "compatibility: []"))
        self.check_invalid(VALID.replace("license: MIT", "compatibility: " + "x" * 501))

    def test_optional_standard_fields(self):
        text = VALID.replace("license: MIT", "compatibility: Needs web sources.\nallowed-tools: Read")
        self.path.write_text(text)
        self.assertEqual(validate_skill(self.path)["allowed-tools"], "Read")

    def test_empty_or_overlong_description(self):
        self.check_invalid(VALID.replace('Evaluate trade show fit using supplied evidence.', '""'))
        self.check_invalid(VALID.replace('Evaluate trade show fit using supplied evidence.', '"' + 'x' * 1025 + '"'))

    def test_required_identity_is_sufficient_without_optional_metadata(self):
        self.path.write_text('---\nname: sample-skill\ndescription: Research a selected event.\n---\n')
        self.assertEqual(validate_skill(self.path)["name"], "sample-skill")

    def test_metadata_must_be_mapping(self):
        self.check_invalid(VALID.replace('metadata:\n', 'metadata: not-a-map\n#'))

    def test_missing_delimiters(self):
        with self.assertRaises(ValueError):
            parse_frontmatter(VALID.replace("---", "", 1))
        with self.assertRaises(ValueError):
            parse_frontmatter(VALID.rsplit("---", 1)[0])

    def test_relative_link_checked_from_document_directory(self):
        self.path.write_text("[Missing](references/missing.md)\n")
        self.assertEqual(len(local_link_errors(self.root)), 1)
        (self.path.parent / "references").mkdir()
        (self.path.parent / "references/missing.md").write_text("Reference")
        self.assertEqual(local_link_errors(self.root), [])

    def test_link_templates_in_code_are_not_files(self):
        self.path.write_text('```markdown\n[Company](website)\n```\n`[Template](path)`\n[Web](https://example.com)\n[Anchor](#example)\n')
        self.assertEqual(local_link_errors(self.root), [])


if __name__ == "__main__":
    unittest.main()

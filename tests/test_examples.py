import copy
import csv
import io
import json
import unittest

from render_examples import ROOT, csv_content, percent, render_drafts, render_events, render_prospects, selection


def fixture(name):
    return json.loads((ROOT / "examples" / name / "input.json").read_text(encoding="utf-8"))


class WorkedExamplesTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture("02-build-shortlist")

    def test_incomplete_capability_evidence_never_qualifies_a_company_or_its_contacts(self):
        companies, people, _ = selection(self.data)
        self.assertEqual([row["id"] for row in companies], ["sample-company-a", "sample-company-b"])
        self.assertEqual([row["id"] for row in people], ["sample-person-a", "sample-person-b"])
        self.assertLess(len(companies), self.data["requested_limit"])

    def test_csv_rows_match_the_final_selection_order_and_fields(self):
        rendered = render_prospects(self.data)
        companies = list(csv.reader(io.StringIO(rendered["accounts.csv"].lstrip("\ufeff"))))
        contacts = list(csv.reader(io.StringIO(rendered["contacts.csv"].lstrip("\ufeff"))))
        selected_companies, selected_people, _ = selection(self.data)
        self.assertEqual([row[0] for row in companies[1:]], [row["name"] for row in selected_companies])
        self.assertEqual([row[0] for row in contacts[1:]], [row["name"] for row in selected_people])
        self.assertEqual(companies[1][5], "")
        self.assertEqual(len(contacts), 3)

    def test_all_unknown_keeps_header_only_files_without_inventing_matches(self):
        for company in self.data["companies"]:
            company["qualification"] = "UNKNOWN"
        outputs = render_prospects(self.data)
        self.assertEqual(len(list(csv.reader(io.StringIO(outputs["accounts.csv"].lstrip("\ufeff"))))), 1)
        self.assertIn("delivered 0 qualified companies", outputs["output.md"])

    def test_input_order_is_preserved_instead_of_new_undocumented_scoring(self):
        self.data["companies"].reverse()
        selected, _, _ = selection(self.data)
        self.assertEqual(selected[0]["id"], "sample-company-b")

    def test_invalid_status_is_a_fixture_error_not_an_empty_result(self):
        self.data["companies"][0]["qualification"] = "SERVICE_FAILED"
        with self.assertRaises(ValueError):
            selection(self.data)

    def test_missing_audience_metric_is_not_zero_and_unknowns_stay_in_denominator(self):
        self.assertEqual(percent({"status": "unavailable"}), "Not available")
        self.assertIn("25.0%", percent({"status": "available", "numerator": 25, "denominator": 100, "unknown_profiles": 20}))
        with self.assertRaises(ValueError):
            percent({"status": "available", "numerator": True, "denominator": 100})

    def test_live_data_cannot_be_published_as_a_fictional_example(self):
        self.data["data_mode"] = "live"
        with self.assertRaises(ValueError):
            render_prospects(self.data)

    def test_formula_cells_are_safe_and_quoted_csv_round_trips(self):
        values = ['=HYPERLINK("https://example.com")', '  +SUM(1,2)', '@lookup', 'a,b', 'line\none', '"quote"', '公司']
        rows = list(csv.reader(io.StringIO(csv_content(["value"], [[value] for value in values]).lstrip("\ufeff"))))
        self.assertTrue(all(row[0].startswith("'") for row in rows[1:4]))
        self.assertEqual([row[0] for row in rows[4:]], values[3:])

    def test_drafts_are_limited_to_selected_qualified_people(self):
        data = fixture("03-prepare-outreach")
        output = render_drafts(data, self.data)
        self.assertLess(output.index("Alex Example"), output.index("Robin Example"))
        invalid = copy.deepcopy(data)
        invalid["selected_contact_ids"].append("sample-person-c")
        invalid["drafts"]["sample-person-c"] = {"subject": "test", "body": "test"}
        with self.assertRaises(ValueError):
            render_drafts(invalid, self.data)

    def test_edition_report_has_no_backend_score_claim(self):
        report = render_events(fixture("01-choose-events"))
        self.assertIn("not the REST API's 0–10 fit score", report)
        self.assertIn("synthetic fixtures", report)


if __name__ == "__main__":
    unittest.main()

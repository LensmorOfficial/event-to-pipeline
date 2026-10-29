import copy
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit

from export_exhibitors import ExportError, NoRedirect, collect, live_reader, main, write_results

ROOT = Path(__file__).resolve().parents[1]


class ExhibitorExportTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads((ROOT / "examples/exhibitor-export/sample.json").read_text(encoding="utf-8"))
        self.calls = []

    def read(self, query):
        self.calls.append(copy.deepcopy(query))
        return self.fixture["pages"][query["page"] - 1]

    def collect(self, pages=2):
        return collect(self.read, self.fixture["query"], pages)

    def test_two_pages_keep_filters_unknowns_and_full_scope(self):
        rows, receipt = self.collect()
        self.assertEqual(len(rows), 3)
        self.assertIsNone(rows[1]["employeeCount"])
        self.assertTrue(receipt["complete_for_query"])
        self.assertEqual([q["page"] for q in self.calls], [1, 2])
        self.assertTrue(all(q["country"] == "Germany" for q in self.calls))

    def test_page_budget_is_reported_as_partial(self):
        rows, receipt = self.collect(1)
        self.assertEqual(len(rows), 2)
        self.assertFalse(receipt["complete_for_query"])
        self.assertEqual(receipt["stop_reason"], "max_pages")

    def test_preview_stops_at_access_boundary(self):
        page = self.fixture["pages"][0]
        page["semantics"] = {"accessMode": "preview", "counts": {"remainingLockedCount": 10},
                             "pageState": {"accessible": True, "maxAccessiblePage": 1}}
        _, receipt = self.collect()
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(receipt["stop_reason"], "access_limit")
        self.assertFalse(receipt["complete_for_query"])

    def test_missing_access_semantics_does_not_trigger_unbounded_query(self):
        del self.fixture["pages"][0]["semantics"]
        _, receipt = self.collect()
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(receipt["stop_reason"], "access_unknown")

    def test_inaccessible_page_never_exports_its_items(self):
        self.fixture["pages"][0]["semantics"]["pageState"]["accessible"] = False
        rows, receipt = self.collect()
        self.assertEqual(rows, [])
        self.assertEqual(receipt["stop_reason"], "page_inaccessible")

    def test_dedup_uses_company_id_and_does_not_claim_missing_rows_complete(self):
        self.fixture["pages"][1]["items"] = [self.fixture["pages"][0]["items"][0]]
        rows, receipt = self.collect()
        self.assertEqual(len(rows), 2)
        self.assertEqual(receipt["duplicates_removed"], 1)
        self.assertFalse(receipt["complete_for_query"])

    def test_repeated_page_is_a_failure(self):
        self.fixture["pages"][1]["page"] = 1
        with self.assertRaisesRegex(ExportError, "Pagination"):
            self.collect()

    def test_malformed_response_is_a_failure_not_an_empty_result(self):
        for change in ({"items": {}}, {"total": "3"}, {"semantics": {"pageState": []}}):
            with self.subTest(change=change):
                page = {**self.fixture["pages"][0], **change}
                with self.assertRaises(ExportError):
                    collect(lambda query: page, self.fixture["query"], 1)

    def test_empty_full_query_still_creates_csv_headers(self):
        page = self.fixture["pages"][0]
        page.update(items=[], total=0, totalPages=0, hasMore=False)
        rows, receipt = self.collect()
        self.assertTrue(receipt["complete_for_query"])
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "empty.csv"
            write_results(output, rows, receipt)
            self.assertEqual(len(output.read_text(encoding="utf-8-sig").splitlines()), 1)

    def test_csv_formula_escaping_and_existing_files_are_preserved(self):
        rows, receipt = self.collect()
        rows[0]["companyName"] = '  =HYPERLINK("https://example.com")'
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "companies.csv"
            metadata = write_results(output, rows, receipt)
            parsed = list(csv.DictReader(io.StringIO(output.read_text(encoding="utf-8-sig"))))
            self.assertTrue(parsed[0]["companyName"].startswith("'"))
            old = output.read_bytes()
            with self.assertRaises(ExportError):
                write_results(output, [], {})
            self.assertEqual(output.read_bytes(), old)
            self.assertEqual(json.loads(metadata.read_text())["rows_exported"], 3)

    def test_get_request_keeps_repeated_filters_and_auth_in_header(self):
        query = {**self.fixture["query"], "category": ["a", "b"], "page": 1}
        with patch("export_exhibitors.build_opener") as factory:
            factory.return_value.open.return_value.__enter__.return_value = io.StringIO(json.dumps(self.fixture["pages"][0]))
            live_reader("test-secret")(query)
            request = factory.return_value.open.call_args.args[0]
            self.assertEqual(request.get_method(), "GET")
            self.assertEqual(request.get_header("Authorization"), "Bearer test-secret")
            self.assertNotIn("test-secret", request.full_url)
            self.assertEqual(parse_qs(urlsplit(request.full_url).query)["category"], ["a", "b"])
            self.assertIsInstance(factory.call_args.args[0], NoRedirect)
            self.assertIsNone(NoRedirect().redirect_request(None, None, 302, "", {}, "https://other.example"))

    def test_errors_do_not_leak_service_body_or_retry(self):
        for error in (HTTPError("https://example", 401, "test-secret", {}, None),
                      HTTPError("https://example", 429, "test-secret", {}, None), URLError("test-secret")):
            with self.subTest(error=error), patch("export_exhibitors.build_opener") as factory:
                factory.return_value.open.side_effect = error
                with self.assertRaises(ExportError) as raised:
                    live_reader("test-secret")(self.fixture["query"])
                self.assertNotIn("test-secret", str(raised.exception))
                self.assertEqual(factory.return_value.open.call_count, 1)

    def test_second_page_failure_writes_no_files(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "failed.csv"
            with patch.dict("os.environ", {"LENSMOR_API_KEY": "test-secret"}), patch("export_exhibitors.live_reader") as reader:
                reader.return_value.side_effect = [self.fixture["pages"][0], ExportError("service unavailable")]
                with self.assertRaises(SystemExit), patch("sys.stderr", new=io.StringIO()):
                    main(["--event-id", "test-event", "--page-size", "2", "--max-pages", "2", "--output", str(output)])
            self.assertFalse(output.exists())
            self.assertFalse(output.with_suffix(".csv.metadata.json").exists())


if __name__ == "__main__":
    unittest.main()

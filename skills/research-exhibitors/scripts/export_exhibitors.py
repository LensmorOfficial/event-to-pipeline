#!/usr/bin/env python3
"""Export a bounded event exhibitor query to CSV plus a scope receipt (MIT)."""

import argparse
import csv
import io
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

ENDPOINT = "https://platform.lensmor.com/external/exhibitors/list"
FIELDS = ("id", "companyName", "website", "domain", "industry", "country",
          "employeeCount", "linkedinUrl", "categories", "matched_event_ids")


class ExportError(ValueError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def live_reader(key):
    """GET only, fixed host, no credential-bearing redirects or hidden retries."""
    opener = build_opener(NoRedirect())

    def read(query):
        request = Request(ENDPOINT + "?" + urlencode(query, doseq=True), headers={
            "Authorization": "Bearer " + key, "Accept": "application/json",
        })
        try:
            with opener.open(request, timeout=30) as response:
                return json.load(response)
        except HTTPError as exc:
            hints = {401: "Check LENSMOR_API_KEY.", 403: "Check account access.",
                     404: "Check the confirmed event ID.", 429: "Rate limited; retry later."}
            raise ExportError(f"HTTP {exc.code}. " + hints.get(exc.code, "Request failed; no files saved.")) from None
        except (URLError, TimeoutError, OSError):
            raise ExportError("Network request failed; no files saved.") from None
        except (ValueError, UnicodeError):
            raise ExportError("The service returned invalid JSON; no files saved.") from None
    return read


def validate_page(data, page, page_size):
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise ExportError("Response must contain an items array.")
    for field in ("total", "page", "pageSize", "totalPages"):
        if type(data.get(field)) is not int or data[field] < 0:
            raise ExportError(f"Invalid pagination field: {field}.")
    if data["page"] != page or data["pageSize"] != page_size or type(data.get("hasMore")) is not bool:
        raise ExportError("Pagination does not match the requested page and size.")
    if len(data["items"]) > page_size:
        raise ExportError("Response exceeds the requested page size.")
    for row in data["items"]:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
            raise ExportError("An exhibitor is missing its stable ID.")
        for field in FIELDS:
            value = row.get(field)
            if value is None:
                continue
            if field in ("categories", "matched_event_ids"):
                valid = isinstance(value, list) and all(isinstance(item, str) for item in value)
            elif field == "employeeCount":
                valid = type(value) is int and value >= 0
            else:
                valid = isinstance(value, str)
            if not valid:
                raise ExportError(f"Invalid exhibitor field: {field}.")
    semantics = data.get("semantics")
    if semantics is not None and not isinstance(semantics, dict):
        raise ExportError("Invalid access semantics.")
    semantics = semantics or {}
    for field in ("counts", "pageState", "unlock", "guidance"):
        if field in semantics and not isinstance(semantics[field], dict):
            raise ExportError(f"Invalid access semantics: {field}.")
    state = semantics.get("pageState", {})
    if "accessible" in state and type(state["accessible"]) is not bool:
        raise ExportError("Invalid page access state.")
    if "maxAccessiblePage" in state and (type(state["maxAccessiblePage"]) is not int or state["maxAccessiblePage"] < 0):
        raise ExportError("Invalid accessible page limit.")
    return semantics


def collect(read, query, max_pages):
    rows, seen, pages = [], set(), []
    duplicates = 0
    stop = "max_pages"
    complete = False
    # A limit returned on an earlier page remains a limit for this export.
    accessible_limit = max_pages
    for number in range(1, max_pages + 1):
        data = read({**query, "page": number})
        semantics = validate_page(data, number, query["pageSize"])
        state = semantics.get("pageState", {})
        counts = semantics.get("counts", {})
        pages.append({"page": number, "total": data["total"], "totalPages": data["totalPages"],
                      "hasMore": data["hasMore"], "semantics": semantics,
                      "recommendationProcessing": data.get("recommendationProcessing")})
        if state.get("accessible") is False:
            stop = "page_inaccessible"
            break
        added = 0
        for item in data["items"]:
            if item["id"] in seen:
                duplicates += 1
                continue
            seen.add(item["id"])
            rows.append({key: item.get(key) for key in FIELDS})
            added += 1
        access = semantics.get("accessMode")
        locked = counts.get("remainingLockedCount")
        more_locked = semantics.get("unlock", {}).get("requiredForMoreResults") is True
        if access == "preview" and type(locked) is int and locked > 0:
            more_locked = True
        if not data["hasMore"]:
            complete = (access == "full" and not more_locked and len(rows) == data["total"]
                        and all(p["total"] == data["total"] for p in pages)
                        and data.get("recommendationProcessing") is not True)
            stop = "query_exhausted" if complete else "visible_results_exhausted"
            break
        if not data["items"] or not added:
            raise ExportError("Pagination made no progress; no files saved.")
        if number >= data["totalPages"]:
            raise ExportError("Contradictory pagination; no files saved.")
        if access not in ("full", "preview"):
            stop = "access_unknown"
            break
        if "maxAccessiblePage" in state:
            accessible_limit = min(accessible_limit, state["maxAccessiblePage"])
        elif access == "preview" or more_locked:
            stop = "access_limit_unknown"
            break
        if number >= accessible_limit and accessible_limit < max_pages:
            stop = "access_limit"
            break
    receipt = {"query": query, "max_pages": max_pages, "pages_fetched": len(pages),
               "rows_exported": len(rows), "duplicates_removed": duplicates,
               "stop_reason": stop, "complete_for_query": complete, "pages": pages}
    return rows, receipt


def csv_value(value):
    if value is None:
        return ""
    if isinstance(value, list):
        value = json.dumps(value, ensure_ascii=False)
    text = str(value)
    if text.lstrip().startswith(("=", "+", "-", "@")) or text.startswith(("\t", "\r", "\n")):
        return "'" + text
    return text


def write_results(output, rows, receipt):
    output = Path(output)
    metadata = output.with_suffix(output.suffix + ".metadata.json")
    for path in (output, metadata):
        if path.exists() or path.is_symlink():
            raise ExportError("Output already exists; choose a new filename.")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows({key: csv_value(row.get(key)) for key in FIELDS} for row in rows)
    created = []
    try:
        for path, text, encoding in ((output, stream.getvalue(), "utf-8-sig"),
                                    (metadata, json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", "utf-8")):
            with path.open("x", encoding=encoding, newline="") as handle:
                created.append(path)
                handle.write(text)
    except OSError:
        for path in created:
            path.unlink()
        raise
    return metadata


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--event-id", help="Already resolved event ID; confirm its edition first")
    source.add_argument("--sample", type=Path, help="Replay fictional pages from a JSON fixture; no network or key")
    parser.add_argument("--keyword")
    parser.add_argument("--country")
    parser.add_argument("--category", action="append")
    parser.add_argument("--industry", action="append")
    parser.add_argument("--page-size", type=int, default=20)
    parser.add_argument("--max-pages", type=int, default=1)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if not 1 <= args.page_size <= 100 or not 1 <= args.max_pages <= 100:
            raise ExportError("page-size and max-pages must be between 1 and 100.")
        # Check both filenames before making any request.
        for path in (args.output, args.output.with_suffix(args.output.suffix + ".metadata.json")):
            if path.exists() or path.is_symlink():
                raise ExportError("Output already exists; choose a new filename.")
        if not args.output.parent.is_dir():
            raise ExportError("Create the output directory first.")
        filters = {key: getattr(args, key) for key in ("keyword", "country", "category", "industry") if getattr(args, key)}
        if args.sample:
            if filters or args.page_size != 20:
                raise ExportError("Sample mode uses the fixture query; do not add filters or page-size.")
            fixture = json.loads(args.sample.read_text(encoding="utf-8"))
            if fixture.get("fictional") is not True:
                raise ExportError("Sample fixtures must declare fictional: true.")
            query = fixture["query"]

            def read(params):
                try:
                    return fixture["pages"][params["page"] - 1]
                except IndexError:
                    raise ExportError("Sample has no next page; no files saved.") from None
        else:
            if not args.event_id.strip() or len(args.event_id) > 100:
                raise ExportError("Provide a confirmed event ID (1–100 characters).")
            key = os.environ.get("LENSMOR_API_KEY", "").strip()
            if not key:
                raise ExportError("Set LENSMOR_API_KEY in your environment for live requests, or use --sample.")
            query = {"event_id": args.event_id, **filters, "pageSize": args.page_size, "personnelLimit": 0}
            read = live_reader(key)
        rows, receipt = collect(read, query, args.max_pages)
        receipt["source"] = "fictional_sample" if args.sample else ENDPOINT
        metadata = write_results(args.output, rows, receipt)
        print(json.dumps({"csv": str(args.output), "metadata": str(metadata),
                          "rows": len(rows), "complete_for_query": receipt["complete_for_query"],
                          "stop_reason": receipt["stop_reason"], "source": receipt["source"]}, ensure_ascii=False))
        return 0
    except (ExportError, OSError, ValueError, KeyError, TypeError):
        # Known errors are safe to explain; never echo a response body or credential.
        import sys
        exc = sys.exc_info()[1]
        message = str(exc) if isinstance(exc, ExportError) else "Invalid input or file operation failed; export did not complete."
        parser.exit(1, message + "\n")


if __name__ == "__main__":
    main()

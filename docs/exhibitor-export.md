# Export an event's exhibitors

`scripts/export_exhibitors.py` turns a bounded Lensmor REST query into an Excel-friendly UTF-8 CSV and an access receipt. It uses Python 3.11+ with no third-party dependencies. The same script is bundled in the installed `research-exhibitors` Skill.

## Try it without an account

From the repository root, choose an unused output filename:

```bash
python scripts/export_exhibitors.py --sample examples/exhibitor-export/sample.json --max-pages 2 --output exhibitors.csv
```

This replays two fictional API pages through the same pagination and CSV pipeline. It produces three companies; missing employee counts remain blank. The receipt identifies the source as `fictional_sample`. It does not make network or model calls. Sample mode uses the fixture's saved query; additional filters are rejected.

## Query real data

1. Resolve the intended event and edition through your connected MCP or the documented REST event lookup. Use its returned ID.
2. Set `LENSMOR_API_KEY` in the process environment using your usual secret-management method. The public REST documentation requires an eligible paid subscription; MCP login is a separate authentication flow.
3. Run a bounded query:

```bash
python scripts/export_exhibitors.py --event-id EVENT_ID --country Germany --keyword surgical --max-pages 3 --output live-exhibitors.csv
```

| Option | Meaning |
| --- | --- |
| `--event-id` | Exact event ID; the script does not guess editions from names |
| `--keyword`, `--country` | Server-side filters; all pages preserve the same values |
| `--category`, `--industry` | Repeat the flag for multiple values; encoded as repeated query parameters |
| `--page-size` | 1–100 records per page; default 20 |
| `--max-pages` | 1–100 pages; default 1; may stop earlier at account limits |
| `--output` | New CSV path in an existing directory; existing files are preserved |

Only `GET /external/exhibitors/list` is called, with `personnelLimit=0`. There are no purchases, contact unlocks, CRM writes or automatic retries. Each request has a 30-second timeout. A rate limit or other request failure exits with an error and saves no partial CSV; retry later with a new run.

## Read the result correctly

`exhibitors.csv` contains company ID, name, website, domain, industry, country, employee count, LinkedIn, categories and matched event IDs. Arrays are JSON strings in cells, unknown fields are blank, and spreadsheet-formula prefixes are escaped. Deduplication uses company ID, not domain.

`exhibitors.csv.metadata.json` contains the query, pages fetched, unique rows, duplicates removed, per-page API access semantics, stop reason and `complete_for_query`.

- `query_exhausted`: full access, pagination ended, stable reported total matches exported rows. Completeness applies only to this filtered query at run time.
- `max_pages`: the requested page budget ended; more results may exist.
- `access_limit`, `access_limit_unknown`, `access_unknown`, `page_inaccessible`: account scope or missing access information stopped further requests.
- `visible_results_exhausted`: the visible response ended, but full-query completeness is not established; inspect the receipt's access, totals and processing state.

The export is a factual directory query. It does not establish actual attendance, rank accounts or verify product-fit claims. Use the research Skills for those assessments. For MCP-selected shortlist exports, preserve the final selected rows instead of replacing them with a new directory query.

## Contract and validation

Based on the public [Lensmor OpenAPI contract](https://github.com/LensmorOfficial/API-Doc/blob/main/openapi.json), inspected on 2026-10-28 (file SHA `192abd025d66775aaaa0e85bc9c4d96140b33038`). Tests cover the offline pipeline and mocked HTTP requests; this revision has not verified live REST authentication. See [verification](verification.md).

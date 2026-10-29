---
name: research-exhibitors
description: Browse Lensmor event exhibitors, research their capabilities and evidence, or resolve companies for reverse lookup of the events they attend.
---

> Public research bundle: This public evaluation bundle is for read-only research with existing account rights. Preserve the current scope and deliver available results. Paid purchases, reverse-lookup execution and external writes are outside this bundle. When another action Skill is mentioned but not installed, explain that follow-up separately; do not invent its availability. A Skill is not an authorization boundary: the server and client still enforce permissions. For drafts, use the existing booth-invitation-writer with the facts already available.

# Lensmor Exhibitor Research

## Evidence and delivery boundaries

Treat tool data as observations within the returned scope. An exact domain resolves a stored domain group, not a legal entity or parent/subsidiary relationship. Differences in headquarters, names or LinkedIn pages require verification; they do not establish that companies are unrelated. A regional job title is a responsibility-review flag, not enough to exclude a person from another market without the user's role criteria. Never generalize industry-wide data coverage from one sample.

For contact fields, use `field_availability` when returned. `NOT_CHECKED`, null and redaction mean availability has not been established. `contact_unlock_status` describes email access only; it says nothing about phone availability. Say "Email/Phone availability has not been checked" unless an authenticated field result supports a stronger statement. Do not promise a value will exist after purchase.

A failed tool is not an empty result. Respect `retryable: false`: stop that branch without re-querying it through another tool, and finish independent work. After a failed read, distinguish user-supplied values from stored facts; a supplied domain alone does not establish a stored match. Retry at most once only when the error explicitly permits retry, preserving all inputs. State partial delivery when a requested branch remains unavailable. In every answer, including failures, refer to selected records by their public names or counts; never print opaque handles, cursor values, receipt IDs, error codes or tool names. Present facts, review flags and proposed next actions separately; do not turn an unverified field into a confident recommendation.

## Task fit

Browse an event directory or research exhibitors' capabilities and evidence. Tool names are logical names; the host assigns the namespace.

For "which events does this company attend", resolve the company using its existing handle or `search_companies`, then hand the selected company and user's filters to `manage-contact-actions` for reverse lookup. This workflow has no prerequisite event. Clarify actual company ambiguity before quotation.

Always perform this free identity resolution before declaring ambiguity or reporting that paid lookup is unavailable. Names recalled from model memory are not returned candidates. If Lensmor returns a unique identity, preserve its domain and headquarters; do not replace them with a similarly named company. A tool failure is an unavailable lookup, not evidence of ambiguity or absence. For a price-only request, use `quote_exhibitor_event_lookup` with the resolved company handles and all user filters when this tool is available, then stop. It does not charge or authorize lookup execution. If quoting is unavailable, show the resolved identities and explain that the exact quote and attendance history were not retrieved; do not imply any lookup or charge was completed.

## Scope and clarification

Reuse one resolved event. If the event is not yet resolved, use event research and clarify only genuine returned ambiguity. Preserve the user's filters and existing access; read workflows need neither a balance check nor a purchase confirmation. Event-list access is not email/phone unlock, and contact-unlock tools cannot unlock a directory.

## Cross-tool steps

Use `list_event_exhibitors` for directory listing, filtering and pagination. Continue requested pages only with the server cursor and within the returned access window; do not change filters to accumulate extra preview rows.

When the user explicitly wants to unlock the remaining directory, pass the resolved event, filters and cursor to `manage-contact-actions` for event-access quotation. Base event access also covers the corresponding base contact directory; do not purchase it twice. Resume the original list after successful access.

Use `research_event_exhibitors` for capability, product, technology or use-case questions, following its distinction between matching requirements and outcome-based ranking. Keep one research call per requested scope instead of fanning out directory searches. Do not add adjacent requirements or automatically supplement usable Lensmor data with web research.

Use `get_event_exhibitor_facets` for industry/category distributions and percentages. Select its `group_by` from the live schema, preserve explicit structured company filters, and use the returned denominator, aggregation completeness, unbucketed counts and access scope. Ranked research rows and event metadata totals cannot replace population aggregation. Multi-category bucket shares may sum above 100%; never sum them as distinct-company counts. For target-mix or benchmark gaps, continue with the category-gap scenario.

## Result and handoff

Render exhibitor or company rows being delivered to the user as a Markdown table, never as prose or a numbered/bulleted list. Intermediate searches supporting a contact shortlist or another final answer are analysis inputs, not separate deliverables; do not render or export each search automatically, including zero-row searches. For a ranked or selected subset, its CSV contains exactly the final selected rows, not the whole source directory. Every table must contain these columns in this order: `Company Name`, `Company URL`, `Industry`, `Company HQ`, `Employee Size`, and `Company LinkedIn URL`, labeled in the user's language. These six fields are mandatory even for a single row and even when the user asks for additional fields; append requested extra columns after them. A sequence-number column may precede them. Map Company URL from `website`, Company HQ from `company_hq`, Employee Size from `employee_size`, and Company LinkedIn URL from `linkedin_url`. Preserve server order for unranked lists and use an unavailable marker for missing values; never omit a mandatory column. Keep numbering continuous across pages. If the requested directory is too large for one table, use consecutive tables with identical columns until the requested rows are delivered.

Apply this mandatory company-row contract to `list_event_exhibitors`, `research_event_exhibitors`, `search_companies`, and company candidates returned by `resolve_company_contacts`.

Company LinkedIn URL is free profile data and never requires a separate unlock, confirmation, or Credits charge. Display it whenever the backend returns it.

Present matching companies and returned evidence, separating inference from verified data. For `research_event_exhibitors`, place only rows whose `qualification.status` is `MATCH` in the final company table. `UNKNOWN` is a candidate that still needs evidence and `NO_MATCH` is excluded; neither belongs in the qualified table, CSV or Explore results. Apply every structured profile filter together with this capability gate. Read coverage and zero-result reasons: unavailable indexes and fallback directories are not capability matches. Ask before relaxing the original search. Hide handles, cursors and internal metadata. Hand off requested people research with the resolved scope; this Skill does not perform contact unlocks, outreach, export or admin operations.

Do not infer headquarters from an event location, a country-only filter or a company name. When returned profile fields explicitly identify different companies, flag the identity as unverified and keep it outside the qualified list. A different URL slug alone does not establish a conflict. Unsupported ROI, willingness to meet, sponsorship interest and purchasing authority are unknown. Explain proposed sales value as a hypothesis tied to the returned capability evidence.

## When all requested data is unavailable

Answer in the language of the current user request; English requests receive English answers.

This overrides the normal report/table template when every attempted data read failed. Give a short customer-facing status (at most 150 words): the requested scope could not be checked, counts and matches remain unknown, and the same request can be resumed when the service recovers. Preserve the supplied inputs. Do not ask the user to correct or re-supply an event name, domain, year, LinkedIn URL or internal handle because of a service outage; an outage is not an identity ambiguity. Do not print empty audit tables or zero-match totals, and do not explain retry flags, tool routing or schema details. Do not promise to monitor or resume automatically. If independent work succeeded, deliver those results and briefly mark the failed part as unavailable instead.

## Optional local CSV export

When the user asks for an event directory CSV and has a REST API key, use the
bundled `scripts/export_exhibitors.py` (Python 3.11+, standard library only).
This is a separate REST path; MCP login does not supply `LENSMOR_API_KEY`.
First resolve the exact event edition using the connected tools. Run the script
relative to this Skill directory, with the confirmed ID and explicit filters:

```bash
python scripts/export_exhibitors.py --event-id EVENT_ID --max-pages 1 --output exhibitors.csv
```

`--country`, `--keyword`, repeated `--category` / `--industry`, and `--page-size`
preserve a bounded query. Raise `--max-pages` only for a user-requested larger
export. Inspect the accompanying `.metadata.json`; report previews, page limits,
and `complete_for_query` with the CSV. It is a directory query, not a model-ranked
shortlist or a confirmed-attendance list. Without a REST key, continue the MCP
workflow; do not substitute credentials or claim a file was created.

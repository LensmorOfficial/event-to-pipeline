---
name: research-people
description: Find redacted Lensmor contacts by event or company and resolve person candidates for reverse event attendance lookup; hand paid directory access, lookups and contact unlocks to manage-contact-actions.
---

> Public research bundle: This public evaluation bundle is for read-only research with existing account rights. Preserve the current scope and deliver available results. Paid purchases, reverse-lookup execution and external writes are outside this bundle. When another action Skill is mentioned but not installed, explain that follow-up separately; do not invent its availability. A Skill is not an authorization boundary: the server and client still enforce permissions. For drafts, use the existing booth-invitation-writer with the facts already available.

# Lensmor People Research

## Evidence and delivery boundaries

Treat tool data as observations within the returned scope. An exact domain resolves a stored domain group, not a legal entity or parent/subsidiary relationship. Differences in headquarters, names or LinkedIn pages require verification; they do not establish that companies are unrelated. A regional job title is a responsibility-review flag, not enough to exclude a person from another market without the user's role criteria. Never generalize industry-wide data coverage from one sample.

For contact fields, use `field_availability` when returned. `NOT_CHECKED`, null and redaction mean availability has not been established. `contact_unlock_status` describes email access only; it says nothing about phone availability. Say "Email/Phone availability has not been checked" unless an authenticated field result supports a stronger statement. Do not promise a value will exist after purchase.

A failed tool is not an empty result. Respect `retryable: false`: stop that branch without re-querying it through another tool, and finish independent work. After a failed read, distinguish user-supplied values from stored facts; a supplied domain alone does not establish a stored match. Retry at most once only when the error explicitly permits retry, preserving all inputs. State partial delivery when a requested branch remains unavailable. In every answer, including failures, refer to selected records by their public names or counts; never print opaque handles, cursor values, receipt IDs, error codes or tool names. Present facts, review flags and proposed next actions separately; do not turn an unverified field into a confident recommendation.

## Task fit

Find redacted contact summaries within an event or company. Tool names are logical names; the host assigns the namespace.

## Scope and clarification

Reuse resolved scope and user-stated industry, role and seniority without adding departments or adjacent requirements. Actual tool scope status decides whether clarification is needed; do not automatically choose a candidate or year. Preserve exact-match requests. Never broaden after an empty result without permission; follow the contact-research descriptor's explicit scope-control parameters.

## Cross-tool steps

For event + company-topic + role research, use `research_event_contacts` once rather than resolving exhibitors and paging contacts per exhibitor. For simpler directories, use `discover_event_contacts` when scope is unknown or `search_event_contacts` when an event is resolved.

For company-first requests, prefer a supplied domain and use `resolve_company_contacts` for combined resolution and discovery, or `search_companies` then `search_company_contacts` when separate resolution is useful. Do not require an event for company-only research.

For a person's attendance history, reuse an already resolved contact or use `search_people_for_event_lookup` with their name and supplied LinkedIn/company identity. Candidate pages use the daily search allowance but do not consume Credits. Preserve returned grouped identities and clarify ambiguous people before handing the selected handles and filters to `manage-contact-actions` for the paid query.

For an explicit request to unlock a whole event's remaining contact list, hand off event access rather than quoting emails for visible people. Distinguish the base directory from Visitor access using returned rights, and resume the same filtered list after success.

Free reads and requested pagination need no extra permission or balance check. Reuse returned cursors and honor access windows; do not remove filters to collect more free rows.

## Result and handoff

Render contact rows being delivered to the user as a Markdown table. Intermediate searches used to compare or select candidates are analysis inputs, not separate deliverables; do not render or export each search automatically. For a top, priority or selected N request, deliver one final selected table in ranked order, with exactly those rows in its CSV; do not substitute the whole source query or attach intermediate and zero-row CSVs. Every contact table must contain these columns in this order: `Name`, `Job Title`, `Company Name`, `Management Level`, and `LinkedIn URL`, labeled in the user's language. These five fields are mandatory even for a single row and even when the user asks for additional fields; append requested extra columns after them. Map them from `full_name`, `title`, `company_name`, `management_level`, and `linkedin_url`. Preserve returned order for unranked lists and use an unavailable marker for missing values; never omit a mandatory column.

Apply this mandatory contact-row contract to `research_event_contacts`, `search_event_contacts`, `discover_event_contacts`, `search_company_contacts`, `resolve_company_contacts`, and their legacy equivalents.

When `search_companies` or `resolve_company_contacts` returns company candidates, render that company list using the exhibitor/company contract: `Company Name`, `Company URL`, `Industry`, `Company HQ`, `Employee Size`, and `Company LinkedIn URL`.

LinkedIn URL is free profile data, not a paid or locked contact field. Show every returned LinkedIn URL without requesting confirmation, quoting Credits, or handing it to an unlock tool. Only email and phone may require their respective field unlocks.

Show returned match confidence and lock status when relevant. Distinguish unavailable coverage from no matches. Never infer or complete redacted emails or phones, or expose handles and internal metadata. When the user requests email/phone pricing, unlocking, recovery or outreach, hand off only the resolved selection to `manage-contact-actions`; do not expand it or treat a directory request as a contact unlock. For an explicit export to a connected destination, hand off the exact selected event contacts to its trusted export workflow. Company-only contacts without one event are not eligible for that export; do not silently add event scope. This research Skill does not execute external writes or admin operations.

## Contact research inputs

When using `research_event_contacts`, reuse `event_handle` when resolved; if no resolution has been attempted, use `event_keyword` and a user-supplied `event_year`. Never use keyword resolution as a fallback after a non-retryable resolution failure. Preserve the original language in `company_topic` and `role_topic`. Set `auto_broaden=false` and `use_web_enrichment=false` unless the user explicitly authorizes the respective expansion. Use `match_mode=strict` for exact requirements and `balanced` otherwise; use the requested `limit` up to 50 or the tool default of 20. Do not send unsupported location, seniority, cursor, or pagination fields to this ranked-research tool.


## Management level display

Display exactly one Management Level column (管理层级 in Chinese). Prefer management_level; the legacy seniorityLevel field represents that same level. Do not generate an additional Seniority/资历 column, and do not infer a missing management level from title or seniority. For display only, use the product labels: owner → Owner; partner → Partner; c_suite → C-Suite; vp → VP; director → Director; head → Head; manager → Manager; senior → Senior; mid_level → Mid Level; entry → Entry; assistant → Assistant; unspecified → Unspecified. Keep raw enum values unchanged for filters and sorting. Use the existing unavailable marker only in Management Level when its value is missing.

## When all requested data is unavailable

Answer in the language of the current user request; English requests receive English answers.

This overrides the normal report/table template when every attempted data read failed. Give a short customer-facing status (at most 150 words): the requested scope could not be checked, counts and matches remain unknown, and the same request can be resumed when the service recovers. Preserve the supplied inputs. Do not ask the user to correct or re-supply an event name, domain, year, LinkedIn URL or internal handle because of a service outage; an outage is not an identity ambiguity. Do not print empty audit tables or zero-match totals, and do not explain retry flags, tool routing or schema details. Do not promise to monitor or resume automatically. If independent work succeeded, deliver those results and briefly mark the failed part as unavailable instead.

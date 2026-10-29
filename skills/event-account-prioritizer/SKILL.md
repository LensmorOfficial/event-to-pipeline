---
name: event-account-prioritizer
description: Rank companies at a specific trade show against the user's ICP and sales objective, with evidence and recommended next actions. Use when the user asks which exhibitors or event accounts to prioritize; not for choosing events, finding people, unlocking data, or sending outreach.
---

> Public research bundle: This public evaluation bundle is for read-only research with existing account rights. Preserve the current scope and deliver available results. Paid purchases, reverse-lookup execution and external writes are outside this bundle. When another action Skill is mentioned but not installed, explain that follow-up separately; do not invent its availability. A Skill is not an authorization boundary: the server and client still enforce permissions. For drafts, use the existing booth-invitation-writer with the facts already available.

# Event Account Prioritizer

Prioritize companies within one trade show using Lensmor's event and exhibitor evidence.

## Evidence and delivery boundaries

Treat tool data as observations within the returned scope. An exact domain resolves a stored domain group, not a legal entity or parent/subsidiary relationship. Differences in headquarters, names or LinkedIn pages require verification; they do not establish that companies are unrelated. A regional job title is a responsibility-review flag, not enough to exclude a person from another market without the user's role criteria. Never generalize industry-wide data coverage from one sample.

For contact fields, use `field_availability` when returned. `NOT_CHECKED`, null and redaction mean availability has not been established. `contact_unlock_status` describes email access only; it says nothing about phone availability. Say "Email/Phone availability has not been checked" unless an authenticated field result supports a stronger statement. Do not promise a value will exist after purchase.

A failed tool is not an empty result. Respect `retryable: false`: stop that branch without re-querying it through another tool, and finish independent work. After a failed read, distinguish user-supplied values from stored facts; a supplied domain alone does not establish a stored match. Retry at most once only when the error explicitly permits retry, preserving all inputs. State partial delivery when a requested branch remains unavailable. In every answer, including failures, refer to selected records by their public names or counts; never print opaque handles, cursor values, receipt IDs, error codes or tool names. Present facts, review flags and proposed next actions separately; do not turn an unverified field into a confident recommendation.

## Required scope

Identify:

- one event or edition;
- at least one ICP criterion, such as target industry, solution need, company geography or size;
- an optional business outcome, such as pipeline creation, ROI, cost reduction or channel expansion.

Reuse an event already resolved in the conversation. If only an event name is available, call `resolve_event` at most once. Pass a concise event name with its stated year; do not concatenate venue, city, dates or explanatory prose into `raw_event_text`. Ask the user to choose when the service returns genuine ambiguity. For `NO_MATCHING_RESULTS`, stop and ask the user for a correction rather than retrying with rewritten names or switching tools. If the ICP is too vague to rank companies meaningfully, ask one compact clarification question before researching.

Preserve every explicit filter and exclusion. Do not add adjacent industries, job functions, regions or company-size requirements.

## MCP workflow

Use logical tool names; the host assigns their runtime namespace.

1. Resolve the event with one `resolve_event` call when needed. Use `search_events_v2` only when the user is discovering an event rather than naming one; never use it as an automatic retry for a failed named-event resolution.
2. Call `research_event_exhibitors` once for the resolved event:
   - put one to five product, technology, capability or solution phrases in `keywords`;
   - put business outcomes such as ROI, TCO, labor savings or pipeline growth in `boost_keywords`;
   - pass `country` or `industry` only when the user explicitly supplied it;
   - request the user's count when stated, otherwise use the service default.
3. Rank and explain the returned accounts. Do not fan out repeated research calls to manufacture more results.

## Access-aware research

This is a read-only workflow that must not create a new charge. Automatically reuse the authenticated user's existing event-access rights. Do not check Credits, quote access, create a confirmation or unlock anything merely to determine whether access already exists.

After `research_event_exhibitors`, read its returned `access` object:

- For `mode: full` or `reason: FULL_ACCESS`, use the returned full-access scope and say that the account's existing event access was used. Do not quote, confirm or purchase access again, even when the current Credit balance is zero.
- For `reason: PREVIEW_COMPLETE_FOR_QUERY`, say that the requested matching query was fully covered within the free scope and no unlock was needed. Do not describe it as a partial result merely because the whole event directory is not unlocked.
- For `reason: PREVIEW_RESULTS_TRUNCATED`, `reason: PREVIEW_PAGE_INACCESSIBLE` or `unlock_required: true`, say that the ranking covers only the currently accessible preview and does not represent the complete event directory. If the user wants evaluation against the full directory, offer the separate event-access workflow for this exact event edition; do not start it automatically.
- For `reason: NO_MATCHING_RESULTS`, distinguish zero matches from an access limitation using the other returned access fields. Ask before relaxing the user's scope.
- If access metadata is absent, do not guess whether the event is unlocked or whether coverage is complete. State only limitations explicitly returned by Lensmor.

When the user asks for a Top N ranking, `research_event_exhibitors` may rank against the authenticated account's full event scope while returning only the requested top rows. Do not confuse the number of returned rows with the number of exhibitors evaluated. If the user instead requests a row-by-row evaluation of the entire directory, explain that this is an exhaustive directory workflow rather than a Top N ranking.

## Prioritization rules

Use only returned evidence:

- capability relevance and `match_evidence`;
- explicit ICP attributes such as industry, country and the returned employee-size range; never invent an exact employee count;
- returned categories and tech stacks;
- dated buying signals and their evidence summaries;
- the service's relevance order or score.

Assign qualitative priorities rather than inventing a new numeric score:

- **High**: strong capability match plus at least one additional ICP or buying-signal indicator;
- **Medium**: useful capability match but incomplete ICP evidence;
- **Explore**: weak, indirect or directory-fallback evidence requiring validation.

Preserve server order within the same priority. A directory preview fallback is not a capability match. Missing data means unknown, not negative. Separate direct evidence from model inference and do not supplement a usable Lensmor result with unrequested web research.

## Output

Open with the event, applied ICP and number of returned accounts. Whenever one or more companies are returned, render a Markdown table with these columns in order:

1. `#`
2. `Company Name`
3. `Company URL`
4. `Industry`
5. `Company HQ`
6. `Employee Size`
7. `Company LinkedIn URL`
8. `Priority`
9. `Why It Fits`
10. `Evidence`
11. `Next Action`

Label columns in the user's language. Map company URL from `website`; use returned country as Company HQ when no more specific headquarters field exists. Company LinkedIn URL is free profile data: display it when returned and use an unavailable marker otherwise. Never quote or unlock it. Use an unavailable marker for every other missing mandatory field rather than omitting a column.

Keep `Why It Fits` concise and tied to the user's ICP. In `Evidence`, distinguish matched product/capability evidence from buying signals. Make `Next Action` a concrete research or sales-preparation step, not a claim that outreach was sent.

After the table, summarize the strongest pattern and the largest evidence gap. End with one concise user-facing access statement based on the returned `access` object: existing full-event access used, free query coverage complete, or preview coverage limited. Hide handles, cursors, internal metadata and locked contact fields.

For `NO_MATCHING_RESULTS`, state that Lensmor found no account matching the requested scope and ask before relaxing any condition. For `DIRECTORY_FALLBACK`, present the rows as accounts to explore and explicitly say capability matching was not established.

## When all requested data is unavailable

Answer in the language of the current user request; English requests receive English answers.

This overrides the normal report/table template when every attempted data read failed. Give a short customer-facing status (at most 150 words): the requested scope could not be checked, counts and matches remain unknown, and the same request can be resumed when the service recovers. Preserve the supplied inputs. Do not ask the user to correct or re-supply an event name, domain, year, LinkedIn URL or internal handle because of a service outage; an outage is not an identity ambiguity. Do not print empty audit tables or zero-match totals, and do not explain retry flags, tool routing or schema details. Do not promise to monitor or resume automatically. If independent work succeeded, deliver those results and briefly mark the failed part as unavailable instead.

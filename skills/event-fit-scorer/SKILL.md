---
name: event-fit-scorer
description: Recommend, rank, or compare trade shows against a company's product, ICP, target region, timing, and event-GTM objective using Lensmor event and exhibitor evidence. Use for questions such as which events to attend or which named show is the better fit; not for choosing accounts inside one event, annual portfolio optimization, unlocking data, or competitor attendance history.
---

> Public research bundle: This public evaluation bundle is for read-only research with existing account rights. Preserve the current scope and deliver available results. Paid purchases, reverse-lookup execution and external writes are outside this bundle. When another action Skill is mentioned but not installed, explain that follow-up separately; do not invent its availability. A Skill is not an authorization boundary: the server and client still enforce permissions. For drafts, use the existing booth-invitation-writer with the facts already available.

# Event Fit Scorer

Rank trade shows against one consistent, evidence-backed fit rubric. Use the logical Lensmor tool names below; the host assigns their runtime namespace.

## Evidence and delivery boundaries

Treat tool data as observations within the returned scope. An exact domain resolves a stored domain group, not a legal entity or parent/subsidiary relationship. Differences in headquarters, names or LinkedIn pages require verification; they do not establish that companies are unrelated. A regional job title is a responsibility-review flag, not enough to exclude a person from another market without the user's role criteria. Never generalize industry-wide data coverage from one sample.

For contact fields, use `field_availability` when returned. `NOT_CHECKED`, null and redaction mean availability has not been established. `contact_unlock_status` describes email access only; it says nothing about phone availability. Say "Email/Phone availability has not been checked" unless an authenticated field result supports a stronger statement. Do not promise a value will exist after purchase.

A failed tool is not an empty result. Respect `retryable: false`: stop that branch without re-querying it through another tool, and finish independent work. After a failed read, distinguish user-supplied values from stored facts; a supplied domain alone does not establish a stored match. Retry at most once only when the error explicitly permits retry, preserving all inputs. State partial delivery when a requested branch remains unavailable. In every answer, including failures, refer to selected records by their public names or counts; never print opaque handles, cursor values, receipt IDs, error codes or tool names. Present facts, review flags and proposed next actions separately; do not turn an unverified field into a confident recommendation.

## Scope

Identify the product or capability, ICP, target region, time range, desired result count, and optional business objective. Preserve every explicit constraint and exclusion. Ask one compact clarification question only when a missing product, ICP, region, or time constraint would materially change the search; otherwise proceed and label unknowns.

Use only Lensmor evidence. Do not add web research unless the user explicitly requests it. This is a read-only workflow: do not check Credits, quote access, create a confirmation, or unlock an event.

## Candidate discovery

For named comparisons, resolve each named edition once with `resolve_event`. Ask the user to choose when a result is genuinely ambiguous. For `NO_MATCHING_RESULTS`, explain which edition was not found and ask for a corrected name, date, venue, or Lensmor link; do not guess, rewrite the name, switch tools, or continue the comparison with a different event.

For discovery, use `search_events_v2` with the user's topic, location, and date constraints. Its location filter accepts one country or one city, not an arbitrary region or a country list:

- Always pass an explicitly named country or city through the corresponding filter; do not rely on topic text or post-filtering to represent it.
- For a multi-country request, create one independent scope per named country. For the common commercial meaning of North America, use United States, Canada, and Mexico and state that assumption. For a broad or genuinely ambiguous region such as Europe, ask which countries should be included rather than silently searching globally.
- Start at most one search for each country or city scope; do not fan out synonyms, translations, or widened replacement searches.
- Build a useful candidate pool rather than treating the first returned page as a relevance ranking. As a default, target `max(20, 3 × requested result count)` candidates per independent country or city scope, capped at 50.
- Continue an existing scope only with its returned `next_cursor` and unchanged filters. Stop at the target, when no next cursor is returned, or when the server says no more results are available.
- Deduplicate editions and apply hard date, location, and exclusion constraints before scoring.
- Never expose cursors or handles to the user.

If zero candidates remain, read the returned zero-result reason, state the exact scope that produced no match, and offer specific constraints the user may choose to relax. Do not relax them automatically.

## Evidence collection

Call `get_event` for every named event and for viable discovery candidates that will be deeply assessed. When no more than 8 viable candidates remain, assess all of them. When more than 8 remain, use event metadata to shortlist up to 8 before exhibitor research, and disclose both counts in the final coverage statement.

For each deeply assessed event, call `research_event_exhibitors` once with the same ICP:

- put one to five product, technology, capability, or buyer-category phrases in `keywords`;
- put outcomes such as pipeline creation, cost reduction, ROI, or channel expansion in `boost_keywords`;
- pass country or industry only when the user supplied it;
- use the returned match count, relevance evidence, and representative Top results as the exhibitor-fit signal;
- do not make repeated calls with rewritten filters to manufacture more matches.

`research_event_exhibitors` may evaluate all matching exhibitors within the authenticated account's accessible scope while returning only representative Top rows. Do not confuse returned row count with evaluated match count.

## Access-aware comparison

Read the access metadata returned for every event research result:

- `FULL_ACCESS`: use the already accessible full-event scope without quoting or purchasing again.
- `PREVIEW_COMPLETE_FOR_QUERY`: say the free scope fully covered that particular query; do not claim the entire directory is unlocked.
- `PREVIEW_RESULTS_TRUNCATED`, `PREVIEW_PAGE_INACCESSIBLE`, or `unlock_required: true`: treat exhibitor evidence as preview-limited and state that limitation.
- Missing access metadata: do not guess whether the event was unlocked or fully evaluated.

Do not compare raw match counts as if they were equally complete when candidates have different access scopes. In mixed-access comparisons, rely more heavily on common event metadata, reduce evidence confidence for preview-limited candidates, and describe the ranking as preliminary. If full-directory comparison would materially improve the decision, offer to start a separate unlock workflow for exact shortlisted editions; never start it automatically.

Limit deep assessment to eight events in one delivery. When more remain, disclose the assessed subset and remaining count; provide the useful bounded result and offer the next batch. Do not describe a partial assessment as a complete portfolio.

## Scoring

Apply one 100-point rubric to all candidates:

| Dimension | Weight | Evidence |
|---|---:|---|
| Topic and ICP fit | 40 | Event topic/audience fit: 20. Matching-exhibitor volume, density when a denominator exists, and relevance evidence: 20. |
| Region fit | 20 | Exact target-market and event-location alignment. |
| Timing fit | 15 | Requested dates, selling cycle, and explicitly stated preparation constraints. |
| Scale and commercial value | 15 | Returned exhibitor, attendee, or scale indicators. |
| Evidence confidence | 10 | Coverage scope, data completeness, and consistency of evidence. |

Award points only for returned evidence. If the user did not specify a constraint for a dimension, mark that dimension `N/A` and normalize the earned score across the applicable dimensions to a 100-point total; never turn an unspecified region, time, or scale preference into zero fit. If the user did specify a criterion but Lensmor lacks the evidence to assess it, mark the evidence unknown and do not award unsupported points. Do not invent audience profiles, attendance, costs, exhibitor totals, or numeric precision. Explain material model inference separately from verified facts and state when a total was normalized over fewer dimensions.

## Output

Return the requested Top N in a Markdown table with: rank, event, dates, location, total score, dimension breakdown, strongest fit evidence, key risk or unknown, and recommendation. For a named comparison, add a direct recommendation and explain the tradeoff.

After the table:

1. summarize the strongest pattern and important risks;
2. list material unknowns or facts that should be verified;
3. state how many events were found, how many survived hard filters, and how many received exhibitor-level assessment;
4. state whether more event pages remained and whether the result is a candidate-pool Top N or the complete searched scope;
5. give one concise access statement distinguishing full-event, query-complete free, preview-limited, or unknown coverage.

Do not include internal Tool names, status codes, handles, cursors, Skill rules, or validation language in the user-facing answer.

## When all requested data is unavailable

Answer in the language of the current user request; English requests receive English answers.

This overrides the normal report/table template when every attempted data read failed. Give a short customer-facing status (at most 150 words): the requested scope could not be checked, counts and matches remain unknown, and the same request can be resumed when the service recovers. Preserve the supplied inputs. Do not ask the user to correct or re-supply an event name, domain, year, LinkedIn URL or internal handle because of a service outage; an outage is not an identity ambiguity. Do not print empty audit tables or zero-match totals, and do not explain retry flags, tool routing or schema details. Do not promise to monitor or resume automatically. If independent work succeeded, deliver those results and briefly mark the failed part as unavailable instead.

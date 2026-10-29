---
name: research-events
description: Find and inspect Lensmor trade shows by name, topic, location, date, or attendee Insights (level, industry, function, company size, analyzed sample). Use for event discovery and event details, not exhibitor, contact, unlock, or outreach work.
---

> Public research bundle: This public evaluation bundle is for read-only research with existing account rights. Preserve the current scope and deliver available results. Paid purchases, reverse-lookup execution and external writes are outside this bundle. When another action Skill is mentioned but not installed, explain that follow-up separately; do not invent its availability. A Skill is not an authorization boundary: the server and client still enforce permissions. For drafts, use the existing booth-invitation-writer with the facts already available.

# Lensmor Event Research

## Evidence and delivery boundaries

Treat tool data as observations within the returned scope. An exact domain resolves a stored domain group, not a legal entity or parent/subsidiary relationship. Differences in headquarters, names or LinkedIn pages require verification; they do not establish that companies are unrelated. A regional job title is a responsibility-review flag, not enough to exclude a person from another market without the user's role criteria. Never generalize industry-wide data coverage from one sample.

For contact fields, use `field_availability` when returned. `NOT_CHECKED`, null and redaction mean availability has not been established. `contact_unlock_status` describes email access only; it says nothing about phone availability. Say "Email/Phone availability has not been checked" unless an authenticated field result supports a stronger statement. Do not promise a value will exist after purchase.

A failed tool is not an empty result. Respect `retryable: false`: stop that branch without re-querying it through another tool, and finish independent work. After a failed read, distinguish user-supplied values from stored facts; a supplied domain alone does not establish a stored match. Retry at most once only when the error explicitly permits retry, preserving all inputs. State partial delivery when a requested branch remains unavailable. In every answer, including failures, refer to selected records by their public names or counts; never print opaque handles, cursor values, receipt IDs, error codes or tool names. Present facts, review flags and proposed next actions separately; do not turn an unverified field into a confident recommendation.

## Task fit

Find events or inspect one event. Use the logical tool names below; the host assigns their runtime namespace.

## Scope and clarification

Preserve the user's event, topic, location and time constraints. Resolve a name against actual returned candidates; a familiar name or a year in the request is not proof of uniqueness. Continue a unique match within scope without another confirmation. Ask only when candidates remain ambiguous or the scope must change.

## Cross-tool steps

For attendee metrics, use the Audience Insights path below first. Otherwise use `resolve_event` for a named or misspelled event and `search_events_v2` for discovery. Follow each tool's input descriptions for topic interpretation and filters. Do not fan out translations or broaden an empty search without permission. For requested pagination, reuse the same filters and returned cursor. Use `get_event` when detail is requested or needed for the next task, not as a compulsory extra step.

Read coverage and the zero-result reason before describing availability: an existing event with an unavailable exhibitor index is not evidence of no matching exhibitors.

## Result and handoff

Show event names, dates, locations and relevant coverage in the user's requested format. Briefly state a returned correction or translation that changes the search interpretation. Keep handles, cursors and internal metadata out of the answer. For downstream exhibitor or people research, hand off the resolved scope. For an explicit request to unlock that event's directories, hand off the existing event handle to `manage-contact-actions`; ordinary discovery does not require a purchase.

## Audience Insights queries

For cross-event attendee proportions, sample counts, audience ranking or quantitative fit, use `search_events_by_insights` after the user has supplied a bounded date range. If dates are missing, ask for the date range before calling. Never silently default to the next three months. This path requires an actual attendee-metric request; it is never a fallback for unavailable topic discovery. Both paths share the same topic index. Do not drop the topic, switch to `keyword`, remove filters or query Insights to work around an index outage. Combine every requested event condition and metric in one call; do not enumerate ordinary event results and compute or rank a partial page locally. For one event, resolve its handle and use `get_event_insights`; single-event Insights do not require a date range. If a search already returned the required metrics, answer from that response.

Cross-event limits default to 93 inclusive days and 100 candidate events before attendee-metric filtering. The tool error details `maxRangeDays` and `maxCandidateEvents` are authoritative for the current environment. `EVENT_INSIGHTS_SCOPE_REQUIRED` is a clarification request, not a service outage or a zero-match result: for `date_range_required`, ask for dates; for `date_range_too_wide`, ask for a shorter date range; for `too_many_candidate_events`, ask the user to narrow the dates or further limit the country, city, or event topic. Preserve every original metric condition and wait for the user's scope choice before calling again. Never add scope constraints yourself or truncate to the first 100 events and present them as the complete search. `candidateCountLowerBound` is only a lower bound on candidate events, not a count of events meeting the metric thresholds.

- Director+ = Owner, Partner, C-suite, VP, Director; never Head. C-suite is independent and never substituted by Director+ or an executive function.
- Financial Services uses attendee industry; Sales uses attendee function. Event topic is an independent condition. Company size uses attendees' linked-company size, not the exhibitor distribution.
- “Mainly 51–200” means `attendee_company_size / category:51-200 / gt:50`; state the >50% rule.
- Preserve >= versus > exactly. Use relative months/days with the user's time zone when provided; otherwise state the returned UTC interval. Do not invent dates or locations; missing cross-event dates require clarification, while single-event reads need no date filter.
- Ratios must show the returned sample/denominator; explain unknown coverage, definition and update time. Treat unavailable/no_sample as unavailable, not zero. Use returned dataVersion when comparing page data.
- Insights tools use page/pageSize. Preserve original filters/metrics and resolved date bounds when paging, and omit timeRange; do not resend derived metrics or mix the ordinary search cursor protocol.
- Empty means empty. Explain zeroResultReason and coverage; do not broaden, replace metrics, or recommend qualitatively “executive-focused” events without new user scope.
- Aggregate reads are free, including for zero-credit users. Do not call contacts, previews, balance, unlock, quote or paid confirmation to answer these questions. Never return contact lists automatically. Explain audience fit only against user-provided criteria.

## When all requested data is unavailable

Answer in the language of the current user request; English requests receive English answers.

For a scope clarification response, ask one concise question for the missing or narrower scope while retaining all metric conditions. Do not use the service-recovery wording below or claim that waiting will resolve a scope limit.

This overrides the normal report/table template when every attempted data read failed. Give a short customer-facing status (at most 150 words): the requested scope could not be checked, counts and matches remain unknown, and the same request can be resumed when the service recovers. Preserve the supplied inputs. Do not ask the user to correct or re-supply an event name, domain, year, LinkedIn URL or internal handle because of a service outage; an outage is not an identity ambiguity. Do not print empty audit tables or zero-match totals, and do not explain retry flags, tool routing or schema details. Do not promise to monitor or resume automatically. If independent work succeeded, deliver those results and briefly mark the failed part as unavailable instead.

---
name: event-buying-committee-mapper
description: Map the buying committee, decision makers, stakeholders, and missing roles for one target account using Lensmor company contacts or event-scoped contacts. Use when a user asks who to approach at a company, which departments or seniority levels belong in a purchase decision, who from an account to meet at a trade show, or which committee roles are still missing. Do not use for ranking many accounts, building a cross-company event meeting list, unlocking contact details, or writing outreach copy.
---

> Public research bundle: This public evaluation bundle is for read-only research with existing account rights. Preserve the current scope and deliver available results. Paid purchases, reverse-lookup execution and external writes are outside this bundle. When another action Skill is mentioned but not installed, explain that follow-up separately; do not invent its availability. A Skill is not an authorization boundary: the server and client still enforce permissions. For drafts, use the existing booth-invitation-writer with the facts already available.

# Event Buying Committee Mapper

Build an evidence-backed stakeholder map for one target account and one buying objective. Separate people Lensmor actually returned from committee roles inferred from titles and the user's sales context.

## Evidence and delivery boundaries

Treat tool data as observations within the returned scope. An exact domain resolves a stored domain group, not a legal entity or parent/subsidiary relationship. Differences in headquarters, names or LinkedIn pages require verification; they do not establish that companies are unrelated. A regional job title is a responsibility-review flag, not enough to exclude a person from another market without the user's role criteria. Never generalize industry-wide data coverage from one sample.

For contact fields, use `field_availability` when returned. `NOT_CHECKED`, null and redaction mean availability has not been established. `contact_unlock_status` describes email access only; it says nothing about phone availability. Say "Email/Phone availability has not been checked" unless an authenticated field result supports a stronger statement. Do not promise a value will exist after purchase.

A failed tool is not an empty result. Respect `retryable: false`: stop that branch without re-querying it through another tool, and finish independent work. After a failed read, distinguish user-supplied values from stored facts; a supplied domain alone does not establish a stored match. Retry at most once only when the error explicitly permits retry, preserving all inputs. State partial delivery when a requested branch remains unavailable. In every answer, including failures, refer to selected records by their public names or counts; never print opaque handles, cursor values, receipt IDs, error codes or tool names. Present facts, review flags and proposed next actions separately; do not turn an unverified field into a confident recommendation.

## Non-negotiable output gates

Before sending the answer, remove any row or person that violates these gates:

- A generic `Business Development` title is not a Channel/Partnerships role. It stays in the separate adjacent-contact table unless the returned evidence explicitly names channel, partnerships, alliances, ecosystem, or partner programs.
- Product Marketing, Sales Operations, Revenue Enablement, Account Executive, Marketing, and Lead Generation are not Product/Technical evaluators. Keep the Product/Technical role `Not found in current scope` unless returned evidence names product management, engineering, IT, security, architecture, integration, or a comparably technical responsibility.
- An adjacent function is never a committee-role row and never appears in the main mapped-contact table.
- A title match does not prove that a person is an actual champion, economic buyer, budget owner, decision maker, or event attendee. With title-only evidence, label the person as a candidate for the role and describe the role's usual purpose; never write that the person owns budget, decides, or directly uses the product.
- When the user did not request an unlock, never recommend fixing access, unlocking the event, purchasing access, or handing contacts to an unlock workflow.
- For one event-scoped target account, use at most four Lensmor data calls: one event resolution, one consolidated event-contact query, one company resolution, and one company-contact page. Do not query each committee role separately and do not paginate unless the user explicitly requests exhaustive coverage.

Run this evidence check after drafting the tables, then correct the draft before returning it.

## Required scope

Obtain one target company, preferably with its domain when the name is common; the product, initiative, or purchase decision being mapped; and any optional event, geography, role, or seniority constraints.

If the target company is missing, ask for it. If the purchase objective is missing and the desired stakeholder roles cannot be determined from the conversation, ask one compact question about what the user is selling or trying to get approved. Do not require an event for company-level committee research.

## Define the role families

Derive no more than five relevant role families from the stated buying objective. Typical families may include a functional owner or champion, technical or security evaluator, economic buyer, procurement or finance, and executive sponsor, but use only the families that fit this request.

The role-family model is an analytical framework, not Lensmor data. Label it as a recommendation. Do not assert that a title holder is an actual decision maker, budget owner, champion, blocker, or event attendee unless returned evidence explicitly proves that relationship. When the only evidence is a job title, confidence describes title-to-role fit only, not confirmed purchasing authority.

## Company-level workflow

When no event is required:

1. Call `search_companies` once, preferring an exact user-supplied domain over a name keyword.
2. Continue only for one resolved company. For ambiguity, show useful company name, website, industry, headquarters, employee-size range, and LinkedIn distinctions, then ask the user to choose. For no match, ask for a domain, LinkedIn URL, headquarters, or corrected name.
3. For each selected role family, call `search_company_contacts` with the same company handle. Use `department` for one role family and `keyword` only for a real person name or one concise title term such as RevOps. Use `level` only when the user explicitly requires that seniority; committee-role seniority inferred by this Skill is an analytical signal for ranking returned contacts, not a search constraint. Do not combine several role families into one strict filter.
4. Use the exact returned cursor to continue only when the user requested more coverage for that same role family. Preserve the company and filters.

For a simple one-role request, `resolve_company_contacts` may combine company resolution and contact discovery. Do not use it to hide ambiguity or repeatedly resolve the same company across several role families.

## Event-scoped workflow

When the user limits the committee to one trade show:

1. Call `resolve_event` with the user's event wording. Set `recency_hint` only when the user explicitly says latest, next, or this year.
2. Continue only for one resolved edition. For ambiguity or no match, give a complete natural response and request the smallest correction; do not research another edition.
3. Call `research_event_contacts` once with the resolved event handle and target company. Put up to five explicitly derived role-family alternatives in one concise `role_topic`, separated by `or`; do not add adjacent roles merely to obtain results. Set `limit=20`, `auto_broaden=false`, and `match_mode=balanced` unless the user explicitly requires exact matching. Do not use `broad` or web enrichment unless the user explicitly permits wider evidence.
4. Resolve the target company once with `search_companies`, preferring an exact user-supplied domain, then call `search_company_contacts` once without a department, level, or keyword filter and with `limit=30`. Use that bounded company page to find title-supported candidates and gaps. Do not paginate or repeat role-specific company searches unless the user explicitly requests exhaustive coverage.
5. Do not fan out by exhibitor. Deduplicate the event and company results by contact handle, then LinkedIn URL, then normalized name plus company. If the consolidated event query returns zero, continue with the single company page and state that company-level contacts are not confirmed event attendees.

An event-scoped contact result means the person was found in Lensmor's event/company contact research scope. It does not by itself prove attendance, a speaking role, sponsorship, booth presence, or membership in a real buying committee.

## Interpret people and gaps

Treat returned names, titles, companies, departments, management levels, seniority, LinkedIn URLs, match reasons, and evidence as facts only when present. LinkedIn URLs are free profile fields and must be shown without a quote or unlock.

Map each returned person to zero, one, or several recommended committee roles using their returned title and department. For each mapping, state the evidence and an inference confidence of high, medium, or low. Do not promote a person into a role merely to fill a gap.

An adjacent function is not a mapped committee role. A generic Account Executive, Sales representative, Sales Operations, or Business Development title alone does not establish Channel/Alliances, Product/Technical, Procurement/Finance, or Economic Buyer responsibility. Business Development by itself is not equivalent to channel or partnerships. For a channel or partner role, require returned title, department, match reason, or evidence that explicitly mentions channel, partnerships, alliances, ecosystem, partner programs, or a comparably specific partner responsibility. Otherwise keep the role `Not found in current scope` and list the person separately as an adjacent contact whose responsibility is unverified.

`Partially covered` still requires evidence specific to the same role family with only part of the responsibility established. Do not use that status to place a generic Sales, Account Executive, Sales Operations, Revenue Enablement, Marketing, or Lead Generation contact into Product/Technical, Procurement/Finance, Economic Buyer, or Executive Sponsor. Keep the committee role `Not found in current scope` and, only when useful, list that person in a short adjacent-contact section.

Adjacent contacts are not a committee role family. Never create a role-table row such as `Business Development (adjacent function)`, never mark an adjacent function `Covered` or `Partially covered`, and never move its people into the main mapped-contact table. A person with only generic Business Development evidence belongs only in the separate adjacent-contact table.

For every expected role family, use one of:

- `Covered`: at least one returned contact has evidence consistent with the role;
- `Partially covered`: returned evidence supports part of this same role family, with remaining responsibility unverified;
- `Not found in current scope`: no returned contact supports the role;
- `Not assessed`: the query did not cover that role.

Never rewrite `Not found in current scope` as confirmation that the company has no such role. Reuse contact results already present in the conversation; do not re-search merely because the user asks which roles remain missing.

## Coverage and access

Company contact search is read-only. For event research, read returned access and coverage metadata:

- `FULL_ACCESS`: use the accessible full scope without repurchasing;
- `PREVIEW_COMPLETE_FOR_QUERY`: say the accessible scope completely covered this role query;
- `PREVIEW_RESULTS_TRUNCATED` or inaccessible preview page: state that the map is preliminary and gaps may reflect access limits;
- missing metadata: report only the actual returned scope and do not guess whether it was free or full.

Evaluate coverage per role-family query. If every assessed role query is full or complete for that query, do not call the overall map preview-limited and do not attribute zero-result gaps to access restrictions. If only some role queries are truncated, attach the access caveat only to those role families. Translate coverage into natural user language; never print internal reason or status codes.

A successful query-complete search returning zero contacts means no matching contact was found for that exact query in the accessible scope. The data was queried successfully. Never describe this as unavailable data, missing access, an access-permission problem, or something the user must unlock. Use access language only when returned metadata explicitly says the result is truncated or inaccessible.

When event coverage says the contact directory is locked but the current query says `unlock_required=false`, `remaining_locked_count=0`, and returns zero, report both facts without collapsing them: no match was found in the currently accessible event scope; the current query did not request an unlock; the full locked directory was not verified. Do not claim either that the full event scope has no matches or that access caused the zero result.

This Skill never checks credit balance, quotes contact fields, unlocks email or phone, or purchases event access. If the user requests those actions, keep the resolved selection unchanged and hand off to the relevant access workflow.

## Deliver the map

Start with the company, buying objective, optional event, and coverage summary. Then return:

1. a committee-role table with role family, purpose in this purchase, coverage status, mapped contacts, evidence, and inference confidence;
2. a contact table with these five fields first, translated to the user's language: Name, Job Title, Company Name, Management Level, LinkedIn URL;
3. the most important gaps and the next role filters to try;
4. one concise scope statement distinguishing company-wide search, query-complete event scope, preview-limited event scope, or unknown coverage.

Use a consistent unavailable marker for missing fields. Do not expose handles, cursors, internal statuses, Tool names, Skill rules, or validation language in the user-facing answer.

Keep the contact table decision-relevant: the main contact table contains only people explicitly mapped in the committee-role table. Put at most five useful but unmapped people in a separate adjacent-contact table. Do not dump the company's full contact pool, unrelated marketing or lead-generation staff, or every returned person merely because the tool returned them.

Recommend only filters or role families that were not already assessed; do not tell the user to repeat an identical completed query. Do not proactively offer or promise contact unlock, export, outreach, or another action outside this read-only Skill. If the user explicitly requests one, preserve the selection and hand off without claiming that the current runtime can execute it. End the answer after the scope statement; do not append an invitation to unlock contacts or continue into a paid workflow.

## Contact research inputs

When using `research_event_contacts`, reuse `event_handle` when resolved; if no resolution has been attempted, use `event_keyword` and a user-supplied `event_year`. Never use keyword resolution as a fallback after a non-retryable resolution failure. Preserve the original language in `company_topic` and `role_topic`. Set `auto_broaden=false` and `use_web_enrichment=false` unless the user explicitly authorizes the respective expansion. Use `match_mode=strict` for exact requirements and `balanced` otherwise; use the requested `limit` up to 50 or the tool default of 20. Do not send unsupported location, seniority, cursor, or pagination fields to this ranked-research tool.


## Management level display

Display exactly one Management Level column (管理层级 in Chinese). Prefer management_level; the legacy seniorityLevel field represents that same level. Do not generate an additional Seniority/资历 column, and do not infer a missing management level from title or seniority. For display only, use the product labels: owner → Owner; partner → Partner; c_suite → C-Suite; vp → VP; director → Director; head → Head; manager → Manager; senior → Senior; mid_level → Mid Level; entry → Entry; assistant → Assistant; unspecified → Unspecified. Keep raw enum values unchanged for filters and sorting. Use the existing unavailable marker only in Management Level when its value is missing.

## When all requested data is unavailable

Answer in the language of the current user request; English requests receive English answers.

This overrides the normal report/table template when every attempted data read failed. Give a short customer-facing status (at most 150 words): the requested scope could not be checked, counts and matches remain unknown, and the same request can be resumed when the service recovers. Preserve the supplied inputs. Do not ask the user to correct or re-supply an event name, domain, year, LinkedIn URL or internal handle because of a service outage; an outage is not an identity ambiguity. Do not print empty audit tables or zero-match totals, and do not explain retry flags, tool routing or schema details. Do not promise to monitor or resume automatically. If independent work succeeded, deliver those results and briefly mark the failed part as unavailable instead.

# Choose events against a business brief

Fictional worked example: all event names, dates, metrics and assessments in [input.json](input.json) are synthetic.

The supplied brief asks for a two-event comparison for medical-device supplier research. One fixture has a Director+ metric of 25 out of 100 profiles, including unknown profiles in that denominator. The other has no available metric.

Read [output.md](output.md). A useful output preserves the difference between unavailable and zero and labels the assessment separately from the REST backend score.

For a live MCP task, use `research-events` and, when appropriate, `event-fit-scorer`. Supply the actual country/date scope and keep ordinary topic discovery separate from real audience-metric filtering. Resolve ambiguous editions before comparing. Do not use fictional dates or identities from this fixture in a real query.

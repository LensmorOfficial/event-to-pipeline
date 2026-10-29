# Three complete worked examples

All three cases are **fictional worked examples**. They use saved synthetic fixtures, not customer data or live query results. Read them without an account; use the [MCP guide](../integrations/mcp/README.md) for actual data.

| Case | Input and steps | Output |
| --- | --- | --- |
| 1. Choose events | [Guide](01-choose-events/README.md) · [Fixture](01-choose-events/input.json) | [Event comparison](01-choose-events/output.md) |
| 2. Research companies and people | [Guide](02-build-shortlist/README.md) · [Fixture](02-build-shortlist/input.json) | [Report](02-build-shortlist/output.md) · [Companies CSV](02-build-shortlist/accounts.csv) · [Contacts CSV](02-build-shortlist/contacts.csv) |
| 3. Prepare outreach | [Guide](03-prepare-outreach/README.md) · [Fixture](03-prepare-outreach/input.json) | [Complete drafts](03-prepare-outreach/output.md) |

Reproduce the saved artifacts using Python 3.11+:

```bash
python scripts/render_examples.py
python scripts/render_examples.py --check
```

The script formats the saved assessments and drafts; it does not perform AI research, scrape websites, calculate a new ICP score, authenticate or call an API. The synthetic fixture deliberately includes unknown and nonmatching companies, missing profile links and fewer qualified results than requested.

For a real run, use actual user facts and returned tool data. Do not treat these example IDs, URLs or event dates as production inputs. Read [verification](../docs/verification.md) for the distinct live checks performed.

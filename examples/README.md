# Examples

Start with the **[live MEDICA 2026 research example](04-medica-live/README.md)**: a real surgical-robotics query, selected account, matching evidence and a 30-second replay.

The three offline cases below use fictional data and run without an account.

| Case | Input and steps | Output |
| --- | --- | --- |
| 1. Choose events | [Guide](01-choose-events/README.md) · [Fixture](01-choose-events/input.json) | [Event comparison](01-choose-events/output.md) |
| 2. Research companies and people | [Guide](02-build-shortlist/README.md) · [Fixture](02-build-shortlist/input.json) | [Report](02-build-shortlist/output.md) · [Companies CSV](02-build-shortlist/accounts.csv) · [Contacts CSV](02-build-shortlist/contacts.csv) |
| 3. Prepare outreach | [Guide](03-prepare-outreach/README.md) · [Fixture](03-prepare-outreach/input.json) | [Complete drafts](03-prepare-outreach/output.md) |

Reproduce the offline artifacts with Python 3.11+:

```bash
python scripts/render_examples.py
```

The renderer formats saved assessments and drafts. To research live data, [connect Lensmor](../integrations/mcp/README.md) and use your own brief.

# Event-to-Pipeline

**Find relevant events, research companies and people, and turn the evidence into outreach drafts.**

Lensmor's open-source toolkit for event prospecting: AI Skills, MCP workflows and reusable Python scripts. Builds on [trade-show-skills](https://github.com/LensmorOfficial/trade-show-skills) with a focused research-to-outreach workflow.

[中文](README.zh-CN.md) · [Examples](examples/README.md) · [MCP setup](integrations/mcp/README.md) · [API export](docs/exhibitor-export.md)

| Task | Start here | Output |
| --- | --- | --- |
| Choose events | [event-fit-scorer](mcp-skills/event-fit-scorer/SKILL.md) · [example](examples/01-choose-events/output.md) | Comparison, evidence and unknowns |
| Build a target list | [event-account-prioritizer](mcp-skills/event-account-prioritizer/SKILL.md) + [event-buying-committee-mapper](mcp-skills/event-buying-committee-mapper/SKILL.md) · [example](examples/02-build-shortlist/output.md) | Companies, relevant contacts and reasons |
| Prepare outreach | [booth-invitation-writer](booth-invitation-writer/SKILL.md) · [example](examples/03-prepare-outreach/output.md) | Personalized drafts for your review |

The examples use fictional data and need no account. Real research uses your existing Lensmor access through MCP or REST. Prefer a hosted workflow? [Use Lensmor Agent](docs/use-lensmor-agent.md).

## Quick Start

Clone the repository, then use **Python 3.11+** to install into a separate project; no pip packages are needed:

```bash
git clone https://github.com/LensmorOfficial/event-to-pipeline.git
cd event-to-pipeline
python scripts/install_mcp_skills.py --destination ../my-project/.agents/skills --dry-run
python scripts/install_mcp_skills.py --destination ../my-project/.agents/skills
```

This installs **six research Skills + the invitation writer**, with their resources and licenses. Existing installations are never overwritten. Use the Skill discovery directory supported by your client, then follow the [MCP connection guide](integrations/mcp/README.md) for authentication and configuration.

In the connected client, try:

```text
Use event-account-prioritizer to research up to 10 surgical-robotics providers
at MEDICA 2026. Preserve that complete capability requirement. Separate
qualified companies from candidates still needing evidence; use existing access.
```

## Export exhibitor data with Python

Try the complete CSV pipeline offline:

```bash
python scripts/export_exhibitors.py --sample examples/exhibitor-export/sample.json --max-pages 2 --output exhibitors.csv
```

For live data, set `LENSMOR_API_KEY` in your environment and replace `EVENT_ID` with a resolved event ID:

```bash
python scripts/export_exhibitors.py --event-id EVENT_ID --country Germany --max-pages 3 --output live-exhibitors.csv
```

The script applies server filters, follows bounded pagination, deduplicates by company ID, and writes a CSV plus `.metadata.json` describing access and completeness. It stops at preview limits. [Parameters, output and authentication](docs/exhibitor-export.md).

## Available Skills

The default installation includes `research-events`, `research-exhibitors`, `research-people`, `event-fit-scorer`, `event-account-prioritizer`, `event-buying-committee-mapper` and `booth-invitation-writer`. The exhibitor Skill includes the same export script for agent use.

The [original 15-Skill catalogue](docs/skills.md) covers additional planning, on-site and follow-up workflows. Existing REST scores and MCP model assessments have different meanings; see [compatibility](docs/mcp-compatibility.md).

## Status and contributing

**Preview `0.5.0-rc.2`**. See [verification and remaining client checks](docs/verification.md), [changelog](CHANGELOG.md), and [contribution guide](CONTRIBUTING.md).

[Lensmor](https://www.lensmor.com/) provides the underlying event intelligence service. Skills and scripts are reusable; live data follows your account's access and API policy. [API documentation](https://github.com/LensmorOfficial/API-Doc).

## License

[MIT](LICENSE) for the original Skills and public helpers; ISC for the generated research instructions. [License details and provenance](NOTICE.md).

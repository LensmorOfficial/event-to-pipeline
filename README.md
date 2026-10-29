# Event-to-Pipeline

**Find relevant events, research target companies and contacts, and prepare evidence-backed outreach.**

Lensmor's developer toolkit for event prospecting: seven AI Skills, MCP integration and reusable Python scripts. Use the Skills in your agent client, or export exhibitor data directly from Python.

[中文](README.zh-CN.md) · [Examples](examples/README.md) · [MCP setup](integrations/mcp/README.md) · [CSV export](docs/exhibitor-export.md)

## What you can do

| Task | Skills | Result |
| --- | --- | --- |
| Find and compare events | `research-events` + `event-fit-scorer` | Event comparison with evidence and unknowns |
| Build a target list | `research-exhibitors` + `event-account-prioritizer` | Qualified companies and screening reasons |
| Identify relevant contacts | `research-people` + `event-buying-committee-mapper` | Roles, contacts and evidence gaps |
| Prepare outreach | `booth-invitation-writer` | Personalized drafts for your review |

The [three worked examples](examples/README.md) use fictional data and need no account. Real research uses your existing Lensmor access. For a hosted workflow, see [Lensmor Agent](docs/use-lensmor-agent.md).

## Quick start

With **Python 3.11+**, install all seven Skills into a separate project. No pip dependencies are needed:

```bash
git clone https://github.com/LensmorOfficial/event-to-pipeline.git
cd event-to-pipeline
python scripts/install_skills.py --destination ../my-project/.agents/skills --dry-run
python scripts/install_skills.py --destination ../my-project/.agents/skills
```

Choose your client's supported Skill discovery directory, then follow the [MCP connection guide](integrations/mcp/README.md). The installer includes resources and licenses and refuses to overwrite existing Skills.

In the connected client, try:

```text
Use event-account-prioritizer to research up to 10 surgical-robotics providers
at MEDICA 2026. Preserve that complete capability requirement. Separate
qualified companies from candidates still needing evidence; use existing access.
```

## Export exhibitor data

Try the CSV pipeline offline:

```bash
python scripts/export_exhibitors.py --sample examples/exhibitor-export/sample.json --max-pages 2 --output exhibitors.csv
```

For live data, set `LENSMOR_API_KEY` and replace `EVENT_ID` with a confirmed event ID:

```bash
python scripts/export_exhibitors.py --event-id EVENT_ID --country Germany --max-pages 3 --output live-exhibitors.csv
```

The script filters, paginates within a limit, deduplicates by company ID and saves CSV plus an access/completeness receipt. It stops at preview limits. MCP login and REST API keys are separate. [Export reference](docs/exhibitor-export.md).

## Seven Skills

| Skill | Scope |
| --- | --- |
| [research-events](skills/research-events/SKILL.md) | Event discovery, details and audience Insights |
| [research-exhibitors](skills/research-exhibitors/SKILL.md) | Exhibitor and company research; optional CSV helper |
| [research-people](skills/research-people/SKILL.md) | Relevant contacts and available profile evidence |
| [event-fit-scorer](skills/event-fit-scorer/SKILL.md) | Compare events against a company's goals and ICP |
| [event-account-prioritizer](skills/event-account-prioritizer/SKILL.md) | Prioritize companies inside a selected event |
| [event-buying-committee-mapper](skills/event-buying-committee-mapper/SKILL.md) | Map relevant roles within a target account |
| [booth-invitation-writer](skills/booth-invitation-writer/SKILL.md) | Draft invitations from supplied or verified facts |

Research returns available evidence; invitation drafts require your review before sending.

## Repository layout

```text
event-to-pipeline/
├── skills/          # Seven self-contained Skills
├── scripts/         # Install, export, validate and package
├── integrations/    # MCP configuration and research bundle records
├── examples/        # Three end-to-end cases and an offline export sample
├── docs/            # References, contributing and changelog
├── tests/           # Behavioral and distribution tests
├── .github/         # CI and contribution templates
└── project.json     # Project version and Skill catalogue
```

## Status and contributing

**Preview `0.6.0`**. See [verification and remaining client checks](docs/verification.md), [changelog](docs/CHANGELOG.md) and [contributing](docs/CONTRIBUTING.md).

Live data is provided by [Lensmor](https://www.lensmor.com/) under your account's access and [API policy](https://github.com/LensmorOfficial/API-Doc). Helpers and invitation drafting use [MIT](LICENSE); the six research Skills use ISC. [Licensing and provenance](NOTICE.md).

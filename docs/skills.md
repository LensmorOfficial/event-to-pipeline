# Original Skill catalogue

The original 15 Skills remain available for existing workflows. For the recommended research-and-drafting installation, use the [main quick start](../README.md#quick-start).


### Pre-Show

| Skill | Description | Use When |
|-------|-------------|----------|
| [trade-show-finder](../trade-show-finder/) | Score and prioritize trade shows for exhibiting based on ICP, region, and goals | Choosing where to exhibit, comparing shows, planning an annual show calendar |
| [trade-show-budget-planner](../trade-show-budget-planner/) | Build exhibition budgets and ROI projections with cost benchmarks | Budget planning, ROI analysis, investment justification |
| [pre-show-competitor-analysis](../pre-show-competitor-analysis/) | Analyze competitor exhibitor lists and booth positioning to inform strategy and messaging | Threat scoring, differentiation planning, counter-messaging before the show |
| [booth-invitation-writer](../booth-invitation-writer/) | Generate personalized pre-show invitation emails and outreach sequences | Driving booth traffic, scheduling meetings, pre-show outreach |
| [booth-giveaway-planner](../booth-giveaway-planner/) | Plan trade show giveaways matched to your ICP, budget, and product story | Choosing branded gifts, budget allocation, pre-show ordering |
| [exhibitor-checklist-generator](../exhibitor-checklist-generator/) | Generate a phased exhibitor prep checklist with owners and deadlines | Show preparation planning, team task assignment, first-time exhibitors |
| [trade-show-fit-score](../trade-show-fit-score/) | Retrieve the API's 0–10 profile fit score and three returned dimensions for one event | Data-backed event triage and planning handoff |
| [trade-show-exhibitor-search](../trade-show-exhibitor-search/) | List exhibitors for one event or run cross-event company discovery | Factual event research, prospect discovery, partner mapping |
| [trade-show-lead-recommender](../trade-show-lead-recommender/) | Retrieve event recommendations and distinguish ranked matches from unranked fallback records | Evidence-gated account prioritization |
| [trade-show-contact-finder](../trade-show-contact-finder/) | Find company contacts and report email/phone lock state without unlocking data | Pre-show decision-maker lookup and LinkedIn outreach planning |
| [competitor-show-tracker](../competitor-show-tracker/) | Rank events by competitor-name matches in Lensmor exhibitor records | Competitive show-circuit mapping with explicit credit and activity logging |

### On-Site

| Skill | Description | Use When |
|-------|-------------|----------|
| [badge-qualifier](../badge-qualifier/) | Qualify leads from booth notes, badge scans, or voice transcripts into a structured CRM-ready record | Real-time lead scoring on the show floor, batch-qualifying end-of-day leads |
| [trade-show-competitor-radar](../trade-show-competitor-radar/) | Structure competitor booth observations into field-intel notes with evidence/inference separation | Documenting competitor launches, pricing signals, and positioning shifts at the show |
| [booth-script-generator](../booth-script-generator/) | Generate booth conversation scripts tailored to each visitor type | Staff training, first-time exhibitors, refreshing pitch for a new show |

See [docs/on-site.md](../docs/on-site.md) for on-site workflow guidance.

### Post-Show

| Skill | Description | Use When |
|-------|-------------|----------|
| [post-show-followup](../post-show-followup/) | Create tiered post-show follow-up email sequences | Converting leads post-event, lead nurture, thank-you emails |

## Quick Start

These folders follow the [Agent Skills format](https://agentskills.io/specification): a `SKILL.md` with YAML frontmatter and Markdown instructions, plus examples and references where needed. They do not require a particular agent runtime.

### Install one skill

Clone the repository, inspect the skill, and copy its entire directory into a location your client discovers. For clients supporting project-level `.agents/skills/`, run from your project:

```bash
git clone https://github.com/LensmorOfficial/trade-show-skills.git
mkdir -p .agents/skills
cp -r trade-show-skills/trade-show-finder .agents/skills/
```

A shared `~/.agents/skills/` directory is also supported by some clients. Check your client's documentation for paths, reload behavior, and invocation syntax. To reproduce a tested revision, check out its commit or GitHub release before copying. Updating the checkout does not update copied skills automatically.

### Install all 15 skills

From the project containing your clone:

```bash
mkdir -p .agents/skills
for skill_file in trade-show-skills/*/SKILL.md; do
  cp -r "$(dirname "$skill_file")" .agents/skills/
done
```

### Prerequisites

- Writing and qualification skills can use user-supplied notes and facts. Research skills need current official sources through browsing tools or source material supplied by the user.
- `trade-show-fit-score`, `trade-show-exhibitor-search`, `trade-show-lead-recommender`, `trade-show-contact-finder`, and `competitor-show-tracker` require a Lensmor API key configured in the agent's execution environment. Each workflow checks for it before requesting data; `metadata.required-env` documents the requirement and does not automatically inject credentials.
- `competitor-show-tracker` uses charged requests and updates search activity. Its workflow requires a confirmed bounded budget before those requests. Installation alone grants no permission to spend credits, unlock records, or send outreach.

If your client does not support skill discovery, provide the chosen `SKILL.md` and any referenced resources as task instructions. The client still needs the tools required by that workflow.

See the [health-check guide](../docs/health-check.md) and [2026-10-07 source audit](../docs/health-audit-2026-10-07.md) for checks performed and outstanding validation. Older releases and external registry copies may contain earlier runtime-specific packaging and do not receive these source fixes automatically.


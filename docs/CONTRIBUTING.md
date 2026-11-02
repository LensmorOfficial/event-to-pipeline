# Contributing to Event-to-Pipeline

Help improve event research, company and contact discovery, invitation drafts and reusable data integrations.

## Suggest a workflow

Open an issue with the business problem, the information a user would provide and an example of the result they need. Use fictional company and contact data when sharing examples.

## Improve an existing Skill

Keep each Skill self-contained, preserve the user's research scope and support company selections with evidence. Draft invitations from supplied sender and product facts. Maintain both README languages when changing public usage.

The seven installable workflows are listed in `project.json` and live under `skills/`. Client connection guides are in `integrations/mcp/`, worked examples in `examples/`, and user references in `docs/`.

The six research Skills are generated from Lensmor's canonical Agent Skills source. Maintainers can regenerate them with `python scripts/build_mcp_bundle.py --source PATH`. This updates the research directories and their source manifest while preserving the invitation writer.

## Source packages

```bash
python scripts/package_release.py
```

This creates `dist/event-to-pipeline-VERSION.zip` and `dist/release-files.json` with source-file checksums.

Preserve the MIT and ISC attribution in [NOTICE](../NOTICE.md), including each Skill's own license.

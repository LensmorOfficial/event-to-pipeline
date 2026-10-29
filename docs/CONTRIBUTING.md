# Contributing to Event-to-Pipeline

Keep contributions focused on event research, company/contact discovery, outreach drafts and reusable data integrations.

## Structure

- `skills/`: the seven installable workflows listed in `project.json`.
- `integrations/mcp/`: connection templates and the six-Skill research bundle's generation plan and manifest.
- `scripts/`: installation, CSV export, examples, validation and packaging.
- `tests/`: behavioral checks for installation, export, metadata and distribution.
- `examples/`: fictional end-to-end cases.
- `docs/`: setup references and verification limits.

Keep Skills self-contained. Preserve unknown fields, source evidence and the user's scope. Drafting must not fabricate product claims or send messages. Use fictional fixtures in examples and tests.

The six research Skills are generated from Lensmor's separately maintained canonical source. Maintainers can regenerate them with `python scripts/build_mcp_bundle.py --source PATH`; add `--check` to verify reproducibility. This updates only those six directories and their manifest, preserving the invitation writer. Users need only this repository to install, run the offline examples or validate it.

When changing scope, update `project.json`, the installer, documentation and tests together. Each Skill must have its own license. Preserve the MIT/ISC attribution in [NOTICE](../NOTICE.md).

## Validate

Use Python 3.11+ and install `scripts/requirements.txt` into a development environment:

```bash
python -m pip install -r scripts/requirements.txt
python scripts/validate_repository.py
python -m unittest discover -s tests -t .
```

The same checks run through `bash scripts/validate-repo.sh` in CI. For a local source archive:

```bash
python scripts/package_release.py
```

This writes `dist/event-to-pipeline-VERSION.zip` and a hash receipt; it does not publish a GitHub release. Include relevant validation results in your pull request. Maintain both README languages when changing public usage.

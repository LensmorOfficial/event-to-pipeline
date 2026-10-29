# Verification

Project: **Event-to-Pipeline 0.6.0 preview**. Layout update: 2026-10-29.

Local checks passed: 56 tests, all seven Skill entrypoints, research bundle generation, local links and an independently extracted archive installation with offline CSV export. Generated file bytes are preserved across Git checkout.

## Reproduce local checks

With Python 3.11+ and the development dependency in `scripts/requirements.txt`:

```bash
python scripts/validate_repository.py
python -m unittest discover -s tests -t .
```

CI runs the same commands through `bash scripts/validate-repo.sh`. Checks cover all seven Skill entrypoints, local links, six generated research packages and their hashes, portable licenses, reproducible fictional examples, installation conflicts and REST export behavior. Export tests use fictional fixtures and mocked HTTP responses.

Packaging is a separate smoke check:

```bash
python scripts/package_release.py
```

Inspect the archive, extract it into a fresh directory, and run `scripts/install_skills.py` from that directory. The archive has its own `event-to-pipeline/` root and excludes Git metadata, dependencies, local outputs and previous archives.

## Runtime limits

| Environment | Evidence |
| --- | --- |
| Offline installation and CSV export | Exercised by tests without third-party packages |
| Connected development-host MCP | Earlier bounded smoke calls resolved an event, inspected Insights and researched exhibitors; this does not establish fresh-client support |
| Fresh external client and authentication | Not yet verified end to end |
| Live REST CSV query | Contract inspected and HTTP behavior mocked; real-key export not yet verified |
| Hosted Lensmor Agent | Uses its own deployment; end-to-end acceptance not claimed |

Research examples are fictional. No raw customer/contact data, account identifiers, live handles or credentials are included. A contact role is evidence of relevance, not proof of buying authority. Preview results and selected shortlists must not be described as complete event directories.

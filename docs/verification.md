# Candidate verification

Candidate: `0.5.0-rc.2`. Date: 2026-10-28. Base public commit: `9a0c2f7966085984c142c7049e371522c2054dd2`. This records validation of the local candidate before publication as the Event-to-Pipeline preview. It does not establish production or fresh-client support.

Publication check on 2026-10-29: the renamed source passed all 52 unit tests and `scripts/validate-repo.sh`, including bundle integrity, worked examples and local Markdown links.

## What the evidence establishes

| Layer | Status | Meaning |
| --- | --- | --- |
| Existing public source | Downloaded | The original 15 Skill paths and source contracts are preserved |
| Canonical research generation | Generated from `0.7.3` | Six selected Skills record source/generated hashes and include ISC licenses |
| Local metadata, artifacts and tests | Passed | 52 unit tests, the repository quality entry, bundle validation and reproducible example checks passed |
| Connected-host MCP (rc.1 record) | Read-only smoke calls completed before rc.2 | Event resolution, aggregate Insights, exhibitor research and a bounded contact query completed through the existing connection |
| Fresh external-client installation and authentication | Not executed | File installation checks do not prove a newly started client's discovery or account flow |
| Live REST CSV query | Not executed | Public OpenAPI contract checked; HTTP behavior mocked; no real key used |
| Hosted Lensmor Agent | Not executed | Existing product navigation and instructions are provided; no new hosted deployment is claimed |
| Purchases and external exports | Not executed | They are outside this research-only candidate |

The earlier rc.1 connected-host smoke used a bounded MEDICA 2026 request. The provider research response included one complete match and four candidates with incomplete evidence in the five returned rows; the latter must not be presented as qualified companies. The bounded engineering-contact query returned no delivered contact rows. These are observations within their scopes, not catalogue-wide coverage or accuracy measurements.

No raw contact data, live handles, tokens, account identifiers or full authenticated query responses are included in the public candidate. The three checked-in worked examples remain fictional and independent of the smoke calls.

## Local commands

Run inside a Python 3.11+ environment with the pinned requirements installed:

```bash
python scripts/validate_metadata.py
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/validate_mcp_bundle.py
python scripts/render_examples.py --check
python scripts/validate_candidate.py
```

The CI entry remains `bash scripts/validate-repo.sh`; it includes the existing documented-contract checks, the complete unit suite and the new candidate validation.

Local results on 2026-10-28:

| Check | Result |
| --- | --- |
| Complete unit suite | 52 passed: 16 metadata, 10 worked-example, 13 export and 13 bundle/installation cases |
| Repository quality entry | Passed through Git Bash with Python 3.13 and the pinned PyYAML dependency |
| Original root Skills | All 15 directories remain; their packaged files are unchanged from rc.1 |
| Generated bundle | Six complete research packages, ISC instructions, MIT export helper, file hashes and the 15-tool research allowlist validated |
| Canonical generation | `--check` passed against source version `0.7.3`; no generated drift |
| Skill format | Six generated frontmatters parsed; identities, scope note and resource set validated |
| Default installation | Seven Skills installed in a fresh temporary directory with site packages disabled and PYTHONPATH removed; bundled export script produced three fictional rows |
| CSV behavior | Filters, pagination, preview boundaries, deduplication, missing data, error handling, formula escaping and existing-file preservation passed |
| Saved examples and links | Reproducible outputs, exact shortlist CSV correspondence and local Markdown links passed |

Tests used a writable temporary directory outside the source checkout and the pinned PyYAML dependency.

Maintainers with the separately authorized canonical checkout can verify deterministic generation using:

```bash
python scripts/build_mcp_bundle.py --source PATH --check
```

End users do not need that private checkout to inspect, install or validate the checked-in bundle.

## Remaining client acceptance

Run the main research task in the selected fresh client and the target hosted Agent. Check real Skill discovery, authentication, exact scope, missing data, unknown company candidates, role relevance and supported file delivery. Publish support only for client versions and environments that complete those checks.

The [product compatibility guide](mcp-compatibility.md) explains backend score versus model assessment, legacy REST actions and shortlist versus directory exports. Passing static checks does not establish those runtime behaviors.

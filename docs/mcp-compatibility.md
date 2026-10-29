# Compatibility and migration

The existing 15 Skill names, directories and REST contracts are preserved. The six new MCP research Skills live in a separate generated bundle. Choose the path deliberately rather than letting one silently replace another.

| Existing route | MCP research route | Preserve this distinction |
| --- | --- | --- |
| trade-show-finder | event-fit-scorer and research-events | Current official-source planning and Lensmor-only evidence have different prerequisites |
| trade-show-fit-score | No claimed equivalent backend scoring tool | The REST route retrieves a 0–10 backend score; the MCP scenario's model assessment is a different rubric |
| trade-show-exhibitor-search | research-exhibitors / event-account-prioritizer | Directory paging, complete capability qualification and cross-event discovery are different queries |
| trade-show-lead-recommender | event-account-prioritizer | Backend recommendation metadata is distinct from a model-selected order; fallback rows remain unranked |
| trade-show-contact-finder | research-people / event-buying-committee-mapper | Relevant roles do not establish purchasing authority or confirmed attendance |
| booth-invitation-writer | Reuse the same writer after research | Drafting with available facts does not require contact-field purchase |
| competitor-show-tracker | Outside this research-only candidate | Legacy REST costs/activity records and current MCP confirmation must be reviewed independently |

## Updating an installed copy

The installer refuses existing destination names. It does not overwrite, delete or globally update a user's Skills. Review the old and new bundles and use a separate project or a deliberate manual migration. Updating a Git checkout does not update previously copied Skills.

The canonical source remains the Lensmor-maintained business package. The public generator records its version and hashes, normalizes line endings and adds one reviewed research-scope note. Changes to the canonical version, selected capabilities or resource set require review before regeneration.

## Candidate boundaries

The six Skills include research handoffs and may describe optional actions in the canonical instructions. The public scope note explicitly excludes paid execution and unbundled action handoffs. Actual authorization remains a client/server responsibility; use the allowlisted Codex example where supported.

Current tool visibility is not proof of a successful fresh installation or a hosted release. Support statements and action/file behavior must match [verification](verification.md).

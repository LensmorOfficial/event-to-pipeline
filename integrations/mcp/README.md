# Connect the Lensmor research workflows

This guide connects the generated research Skills to the existing remote Lensmor service. It does not deploy a server, change an account plan or enable financial operations.

## Prerequisites

- A client that supports the selected Skill-discovery path and remote MCP.
- Your own Lensmor account and a connection authorized by the existing server policy.
- Access to the data needed for the task. A connected account may still receive previews or unavailable fields.
- Python 3.11+ for installation; no third-party packages are needed. Maintainer validation separately uses `scripts/requirements.txt`.

The REST API key policy documented in [API-Doc](https://github.com/LensmorOfficial/API-Doc) does not establish every MCP client's authentication or subscription policy. Follow the server's actual connection flow. This project does not claim anonymous live access or issue credentials.

## 1. Install the default seven Skills

From this checkout, choose a separate project:

```bash
python scripts/install_skills.py --destination ../my-project/.agents/skills --dry-run
python scripts/install_skills.py --destination ../my-project/.agents/skills
```

Inspect the dry-run paths. The second command copies six research Skill directories and `booth-invitation-writer`, including resources and licenses; it never edits client configuration or overwrites an existing Skill. If a conflict exists, choose another destination or review the existing installation yourself. A filesystem failure is reported as failure and can leave a partial copy; reruns do not replace those files.

The exhibitor Skill also includes the standalone REST CSV helper. Use it only when a REST key is available; MCP authentication does not provide that key. See [CSV export](../../docs/exhibitor-export.md).

## 2. Configure the existing remote MCP

Endpoint: `https://platform.lensmor.com/mcp`.

For Codex, review and merge [codex.config.example.toml](codex.config.example.toml) into the configuration of the intended trusted project. The `enabled_tools` list contains only the 15 research dependencies declared by this bundle. Do not replace an existing configuration wholesale.

Codex supports remote HTTP MCP configuration and project `.codex/config.toml`; where the Lensmor server/client connection supports OAuth, `codex mcp login lensmor` starts that connection's login flow. For a separately supported bearer-token connection, use the documented environment-variable setting rather than putting the token in a file or chat. This guide does not assume a particular credential type works without verification.

Official references: [Codex Skills](https://developers.openai.com/codex/skills), [Codex MCP](https://developers.openai.com/codex/mcp).

[mcp.config.example.json](mcp.config.example.json) is an endpoint-only template for clients that accept that JSON structure. It does **not** restrict the server's advertised tools. Apply the receiving client's supported tool controls before treating another client as research-only; this template alone is not a permission boundary.

## 3. Check capabilities before a task

Ask the client to list its connected Lensmor tools, then compare the selected Skill's requirements in [the bundle manifest](bundle-manifest.json). Do not substitute tool names, fake handles or another API when a dependency is unavailable.

First test prompt:

```text
Use research-events to resolve MEDICA 2026 and show its returned dates and location. Read only; do not purchase data or unlock contacts. If several editions remain, ask me to choose.
```

A resolved event proves that call worked in that environment. It does not prove every Skill, data entitlement, file path or paid confirmation works. Continue with [the cases](../../examples/README.md) and [acceptance records](../../docs/verification.md).

## 4. Run a research task

```text
Use event-account-prioritizer to research up to 10 surgical-robotics providers at MEDICA 2026. Preserve that complete capability requirement. Separate qualified companies from candidates still needing evidence; do not buy more data.
```

Then specify a relevant contact role before using `event-buying-committee-mapper`. Reuse already resolved scope. For drafts, select recipients and provide sender facts to `booth-invitation-writer`; an unknown email address does not prevent preparing a draft.

The default installer already includes the drafting Skill; no extra copy step is needed.

## Files and actions

This research-only configuration does not enable `create_data_export`, purchases, contact-field unlocks, reverse-lookup execution or third-party exports. A client with a verified local file mechanism may save exactly the final shortlist at the user's request. Lensmor Agent can use its own supported Files integration.

A separately authorized full-query export requires the existing server tool, scopes, data rights and exact original filters. Do not label that broader directory as a model-selected shortlist. If file storage is unavailable, deliver the table and explain the limit instead of inventing a download.

## Troubleshooting

| Symptom | Next step |
| --- | --- |
| Skill not discovered | Check the client's actual discovery directory and metadata; refresh or restart only if needed |
| Authentication required | Reconnect through the supported account flow; do not repeat the same failed query |
| Required tool missing | Check the selected connection/version; keep the affected workflow unavailable |
| Ambiguous event/company | Present the returned candidates and ask for the intended identity |
| Preview or locked fields | Preserve the returned scope; no automatic purchase |
| Missing audience metric | Mark unavailable; do not estimate from visible contacts |
| Service failure | Preserve inputs and report that branch as unchecked, not empty |
| No file capability | Return a usable table with the limitation |

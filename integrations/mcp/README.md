# Connect Lensmor to your AI client

**Endpoint:** `https://platform.lensmor.com/mcp`

Install the Skills into your target project, then connect Lensmor in your client. [Create an account](https://app.lensmor.com/signup?utm_source=github&utm_medium=guide&utm_campaign=event-to-pipeline&utm_content=mcp-setup) to get started. Python export uses a separate [REST API key](../../README.md#get-access).

| Client | Project Skills directory | MCP setup |
| --- | --- | --- |
| Claude Code | `.claude/skills/` | CLI command below |
| Codex | `.agents/skills/` | Project `.codex/config.toml` |
| Cursor | `.cursor/skills/` | Project `.cursor/mcp.json` |
| Claude Desktop | Claude's Skills settings | Custom remote connector |

## Claude Code

From your target project, with Node.js 22.20+:

```bash
npx skills add LensmorOfficial/event-to-pipeline --skill '*' --agent claude-code --copy
claude mcp add --transport http lensmor https://platform.lensmor.com/mcp
```

Start Claude Code in that project and use `/mcp` to inspect the connection. Ask:

```text
Use research-events to find MEDICA 2026 and show its dates and location.
```

For a connection shared with your project, use:

```bash
claude mcp add --transport http --scope project lensmor https://platform.lensmor.com/mcp
```

This writes `.mcp.json`; [claude-code.config.example.json](claude-code.config.example.json) shows its structure. The default command uses local scope. Select research tools using Claude Code's tool permission controls.

Official references: [MCP](https://code.claude.com/docs/en/mcp), [Skills](https://code.claude.com/docs/en/skills).

## Codex

From your target project:

```bash
npx skills add LensmorOfficial/event-to-pipeline --skill '*' --agent codex --copy
```

Merge [codex.config.example.toml](codex.config.example.toml) into the project's `.codex/config.toml`. It selects the 15 research tools declared in [the manifest](bundle-manifest.json).

Trust the project, then connect your account:

```bash
codex mcp login lensmor
```

Start Codex, inspect the connection with `/mcp`, and try the MEDICA prompt above.

Official references: [Codex MCP](https://developers.openai.com/codex/mcp), [Codex Skills](https://developers.openai.com/codex/skills).

## Cursor

From your target project:

```bash
npx skills add LensmorOfficial/event-to-pipeline --skill '*' --agent cursor --copy
```

Merge this into `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "lensmor": {
      "url": "https://platform.lensmor.com/mcp"
    }
  }
}
```

Enable Lensmor in Cursor's MCP settings and complete the connection flow it presents. In Agent chat, select a Skill and run the MEDICA prompt. Use Cursor's tool controls to select the research tools for your task.

Template: [cursor.config.example.json](cursor.config.example.json). Official references: [Cursor MCP](https://cursor.com/docs/context/mcp), [Cursor Skills](https://cursor.com/docs/context/skills).

## Claude Desktop

1. Open **Customize → Connectors** and add a custom remote connector named **Lensmor**.
2. Enter `https://platform.lensmor.com/mcp` as the URL and complete the connection flow shown by Claude.
3. Enable Lensmor in a conversation and ask for MEDICA 2026's dates and location.
4. Enable **Code execution and file creation** in Claude's capabilities settings. In a local checkout, package one Skill, for example:

   ```bash
   python -c "import shutil; shutil.make_archive('dist/research-events', 'zip', 'skills', 'research-events')"
   ```

5. Open **Customize → Skills → Upload a skill**, upload `dist/research-events.zip`, and enable it. For another workflow, replace `research-events` in the command with its directory name under [`skills/`](../../skills/). Each ZIP contains one Skill directory with `SKILL.md` and its resources.

Team and Enterprise administrators can add the connector in their organization's settings. Official guides: [Remote connectors](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp), [Skills settings](https://support.claude.com/en/articles/12512180-use-skills-in-claude), [Skill ZIP structure](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).

## Python installation alternative

With Python 3.11+, clone or extract this repository, then install into a separate target project:

```bash
python scripts/install_skills.py --destination ../my-project/.claude/skills --dry-run
python scripts/install_skills.py --destination ../my-project/.claude/skills
```

For Codex use `../my-project/.agents/skills`; for Cursor use `../my-project/.cursor/skills`. The installer copies all seven Skills, resources and licenses, and preserves existing Skills. Configure MCP using the client section above.

The [Skills CLI](https://github.com/vercel-labs/skills) also supports interactive selection of individual Skills and installs to the current project by default.

## Run a research workflow

```text
Use event-account-prioritizer to research surgical-robotics providers at
MEDICA 2026. Give me the selected companies and evidence for each match.
Keep candidates needing review separate and use existing account access.
```

Then specify the contact roles you need. For invitations, select recipients and give `booth-invitation-writer` your sender identity, product facts and proposed next step.

Research uses your account's available data. The Codex configuration selects research tools; JSON templates configure the endpoint, while the receiving client controls tool permissions. MCP access and `LENSMOR_API_KEY` are separate credentials. [Real MEDICA example](../../examples/04-medica-live/README.md).

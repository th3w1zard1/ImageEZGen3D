> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/ai.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# AI Integration

Meshy exposes two channels for AI agents and coding assistants: the Meshy MCP server for tool-calling, and `llms.txt` / `llms-full.txt` for docs ingestion.

If you are integrating Meshy from Claude Code, Cursor, Windsurf, Codex, or any other MCP-compatible tool, install the MCP server below. If you are integrating from a plain chat agent with no MCP support, point it at [`https://docs.meshy.ai/llms.txt`](/llms.txt) instead.

---

## What is MCP
The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open standard that lets AI assistants call external tools and retrieve structured context. The Meshy MCP server wraps the Meshy REST API as a set of tools your agent can invoke — generate a model, check a task, download the result — without hand-writing HTTP code.

The MCP server is open source and published on npm as [`@meshy-ai/meshy-mcp-server`](https://www.npmjs.com/package/@meshy-ai/meshy-mcp-server). Source: [github.com/meshy-dev/meshy-mcp-server](https://github.com/meshy-dev/meshy-mcp-server).

> **Note:** You need a Meshy API key. Create one at [https://www.meshy.ai/settings/api](https://www.meshy.ai/settings/api). The MCP server reads it from the `MESHY_API_KEY` environment variable.

---

## Quick Install

**add-mcp**

```bash
# Detects installed AI clients and configures Meshy for each
npx add-mcp @meshy-ai/meshy-mcp-server --env MESHY_API_KEY=msy_YOUR_API_KEY
```

**Claude Code**

```bash
# macOS / Linux / WSL
claude mcp add meshy --env MESHY_API_KEY=msy_YOUR_API_KEY -- npx -y @meshy-ai/meshy-mcp-server

# Windows PowerShell — use add-json to avoid `--` parsing issues
claude mcp add-json meshy '{"command":"npx","args":["-y","@meshy-ai/meshy-mcp-server"],"env":{"MESHY_API_KEY":"msy_YOUR_API_KEY"}}'
```

**Cursor**

```json
// .cursor/mcp.json
{
  "mcpServers": {
    "meshy": {
      "command": "npx",
      "args": ["-y", "@meshy-ai/meshy-mcp-server"],
      "env": { "MESHY_API_KEY": "msy_YOUR_API_KEY" }
    }
  }
}
```

**Windsurf**

```json
// ~/.codeium/windsurf/mcp_config.json
{
  "mcpServers": {
    "meshy": {
      "command": "npx",
      "args": ["-y", "@meshy-ai/meshy-mcp-server"],
      "env": { "MESHY_API_KEY": "msy_YOUR_API_KEY" }
    }
  }
}
```

**Claude Desktop**

```json
// ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)
// %APPDATA%\Claude\claude_desktop_config.json (Windows)
{
  "mcpServers": {
    "meshy": {
      "command": "npx",
      "args": ["-y", "@meshy-ai/meshy-mcp-server"],
      "env": { "MESHY_API_KEY": "msy_YOUR_API_KEY" }
    }
  }
}
```

**Codex**

```bash
codex mcp add meshy --env MESHY_API_KEY=msy_YOUR_API_KEY -- npx -y @meshy-ai/meshy-mcp-server
```

**VS Code**

```json
// .vscode/mcp.json  (workspace)  or  User settings > MCP Servers
{
  "servers": {
    "meshy": {
      "command": "npx",
      "args": ["-y", "@meshy-ai/meshy-mcp-server"],
      "env": { "MESHY_API_KEY": "msy_YOUR_API_KEY" }
    }
  }
}
```

**Other**

```json
// Generic stdio MCP config. Consult your client's docs for the exact file.
{
  "mcpServers": {
    "meshy": {
      "command": "npx",
      "args": ["-y", "@meshy-ai/meshy-mcp-server"],
      "env": { "MESHY_API_KEY": "msy_YOUR_API_KEY" }
    }
  }
}
```

> **Note:** **Prefer a drop-in skill instead?** The open-source [`meshy-3d-agent`](https://github.com/meshy-dev/meshy-3d-agent) skill pack ships pre-written Meshy workflows (generate → poll → download) for Claude Code, Cursor, and OpenClaw. It calls the Meshy REST API directly — no MCP server required.
>
>   ```bash
>   npx skills add meshy-dev/meshy-3d-agent
>   ```

---

## Available Tools
The MCP server exposes the Meshy REST API as tools, grouped by capability.

### 3D Generation
- `meshy_text_to_3d` — create a 3D model from a text prompt
- `meshy_image_to_3d` — create a 3D model from one image
- `meshy_multi_image_to_3d` — create a 3D model from multiple images of the same object
- `meshy_text_to_3d_refine` — add texture to a preview mesh

### Post-Processing
- `meshy_remesh` — change topology and/or polycount of an existing model
- `meshy_retexture` — apply a new texture to an existing model
- `meshy_rig` — add a skeleton to a 3D humanoid character
- `meshy_animate` — apply an animation to a rigged character

### Image Generation
- `meshy_text_to_image` — 2D image from text
- `meshy_image_to_image` — 2D image from a reference image

### Task Management
- `meshy_get_task_status` — check task status and download URLs
- `meshy_list_tasks` — list recent tasks, optionally filtered by type/status
- `meshy_cancel_task` — cancel a pending or in-progress task
- `meshy_download_model` — fetch a completed model file and save locally

### Workspace
- `meshy_list_models` — list all models in the authenticated user's workspace

### 3D Printing
- `meshy_send_to_slicer` — detect installed slicers and launch the model in one (runs locally on your machine; no Meshy API call)
- `meshy_analyze_printability` — **currently returns a manual print-readiness checklist** (wall thickness, overhangs, manifold mesh, etc.). Will be upgraded to automated analysis once the Meshy printability API is available.
- `meshy_process_multicolor` — convert a textured model into a multi-color 3MF file for printing

### Account
- `meshy_check_balance` — query remaining credits

> **Note:** Tool names and behaviors may evolve. The authoritative list lives in the [MCP server source](https://github.com/meshy-dev/meshy-mcp-server/tree/main/src/tools).

---

## Example Prompts
Drop these into your MCP-enabled chat as a starting point.

```
Generate a 3D fox from the prompt "a cartoon fox sitting", preview it, then
texture it with PBR maps. Download the final GLB to ./outputs.
```

```
Take the image at https://example.com/sculpture.jpg and convert it into a
riggable 3D character. Use `should_remesh: true` and 50k target polycount.
```

```
What's my current Meshy credit balance?
```

```
List my last 10 successful text-to-3d tasks and download the top 3 as GLB
into ./downloads/.
```

---

## llms.txt and llms-full.txt
If your agent doesn't support MCP, or you want to ingest the Meshy docs into a prompt directly, point it at our plain-text surfaces:

- [`llms.txt`](/llms.txt) — compact index + integration instructions (the correct async-polling pattern, auth rules, rate limits, model choice, common mistakes).
- [`llms-full.txt`](/llms-full.txt) — every API page concatenated in a single file for single-fetch ingestion.
- Per-page Markdown: append `.md` to any endpoint URL. Example: [`https://docs.meshy.ai/api/text-to-3d.md`](/api/text-to-3d.md).

All three are regenerated every time the docs site builds, so they never drift from the HTML docs.

---

## FAQ
### Is the MCP server stateless?

Yes. Your `MESHY_API_KEY` is used per request and never persisted on the server side.

### Does MCP cost the same as the REST API?

Yes — every MCP tool call maps to a single REST call and consumes credits at the exact same rate. See [Pricing](/api/pricing) for the full matrix.

### What are the rate limits?

The MCP server shares the same rate-limit plane as the REST API. See [Rate Limits](/api/rate-limits) for per-tier limits.

### What Meshy data can the MCP access?

Only what the `MESHY_API_KEY` can access via REST. Scopes and permissions are identical.

### How do I report issues?

File an issue at [github.com/meshy-dev/meshy-mcp-server](https://github.com/meshy-dev/meshy-mcp-server/issues).

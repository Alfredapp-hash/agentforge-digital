# ClearTrace Agent Builder Setup

Replicate and extend ClearTrace in **Cursor**, **Claude Code**, **Windsurf**, or any agent IDE.

**Upstream:** `agent-builder/` in [Clear-Trace repo](https://github.com/Alfredapp-hash/Clear-Trace)

---

## What's in the kit

| Component | Location | Purpose |
|-----------|----------|---------|
| Skill pack (20 skills) | `agent-builder/skillpack/skills/` | Markdown skills synced to `skills/` at build |
| MCP server | `agent-builder/mcp-server/` | Cursor ↔ ClearTrace API |
| Scaffold CLI | `scripts/create-cleartrace.mjs` | New agent-only project |
| Platform rules | In-app download + materialized kits | Cursor / Claude / Windsurf rules |
| PRD + architecture | `skillpack/PRD.md`, `ARCHITECTURE.md` | Agent context |

---

## In-app access (fastest)

1. Run ClearTrace locally or on your deploy
2. **Settings → Agent builder kit**
3. Download **full kit (.zip)** — skills + rules + MCP + docs
4. Follow interactive setup checklist in UI

---

## MCP server setup

### Install

```bash
cd agent-builder/mcp-server
npm install
```

### Environment

```bash
export CLEARTRACE_URL=http://localhost:3000
export CLEARTRACE_API_KEY=ct_live_…   # Pro → Settings → API keys
```

### Run

```bash
node index.mjs
```

### Cursor configuration

Copy `agent-builder/mcp-server/cursor-mcp.json.example` to your Cursor MCP config:

```json
{
  "mcpServers": {
    "cleartrace": {
      "command": "node",
      "args": ["/absolute/path/to/Clear-Trace/agent-builder/mcp-server/index.mjs"],
      "env": {
        "CLEARTRACE_URL": "http://localhost:3000",
        "CLEARTRACE_API_KEY": "ct_live_…"
      }
    }
  }
}
```

Restart Cursor. The agent can then call your ClearTrace API for case operations (per server README).

---

## CLI scaffold (new agent project)

From ClearTrace repo root:

```bash
node scripts/create-cleartrace.mjs my-privacy-app
```

Creates:
- `skills/` (synced skill pack)
- `.cursor/rules/`
- `AGENTS.md`, `BOOTSTRAP.md`
- `mcp-server/` copy
- `docs/`

Use when building a **custom** privacy agent without forking the full Next.js app.

---

## The 20 skills (overview)

| Skill | Hermes step |
|-------|-------------|
| intake-and-consent | 1 |
| discover-public-exposure | 2 |
| verify-identity-match | 3 |
| resolve-content-controller | 4 |
| classify-exposure | 4 (inline) |
| route-remedy | 4 (inline) |
| draft-removal-request | 5 |
| compliance-verify-draft | 6 |
| record-outbound-sent | 7 |
| schedule-monitoring | 8 |
| verify-removal | 9 |
| follow-up-policy | 10 |
| batch-remediation | Cross-cutting |
| export-case-packet | Export |
| generate-removal-certificate | Proof |
| escalate-legal-review | Template only |
| intake-live-url | Discovery |
| reopen-on-reappearance | Monitoring |
| connector-readiness-check | Setup |
| sentinel-security-auditor | Security |

Shared contracts: `skills/_shared/AGENT_CONTRACT.md`, `EVIDENCE_STANDARD.md`, `OUTPUT_CONTRACT.md`

---

## Cursor workflow (recommended)

1. Clone ClearTrace; open in Cursor
2. Download Agent Builder kit from Settings
3. Extract rules into `.cursor/rules/`
4. Add MCP server to Cursor config
5. Start case in UI; use agent for:
   - Draft refinement (with compliance review)
   - Batch remediation planning
   - Export packet assembly
   - Connector readiness checks

**Never** bypass compliance gate for automated outbound send.

---

## Claude Code / Windsurf

- Use platform-specific rules from the kit zip
- Point agent at `agent-builder/skillpack/` as read-only context
- MCP: same server; adjust config path for your IDE's MCP format
- Reference `AGENTS.md` in scaffold output for handoff conventions

---

## Sync skills after upstream updates

```bash
npm run materialize-kits   # Pre-build to agent-builder/dist/
node scripts/sync-skills.js # Sync skillpack → skills/
```

Run after pulling new ClearTrace releases.

---

## GitHub template (fork for clients)

Enable **Template repository** on your fork (Settings → General).

Users one-click: https://github.com/Alfredapp-hash/Clear-Trace/generate

See `.github/ENABLE_TEMPLATE.md` in repo.

---

## Pair with AgentForge products

| AgentForge product | Use with ClearTrace |
|--------------------|---------------------|
| MCP Marketing crew | Launch playbook + Gumroad listing |
| Notion Ops Dashboard | Log cases, connector costs, Hermes runs |
| MCP Product Ideator | Privacy-adjacent digital product ideas |
| Grok / Claude libraries | Draft polish prompts (BYOK in ClearTrace) |

---

*Agent Builder guide · AgentForge Digital catalog*

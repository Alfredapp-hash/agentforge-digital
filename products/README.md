# AgentForge Digital — Product Catalog

**Status:** 8 products ready to list · 0 live on Gumroad · Gumroad API connected

**Content expanded:** Jun 2026 — playbooks, crews, and prompt libraries significantly deepened. Re-run packaging after edits.

Run `python scripts/package_products.py` to refresh all `.zip` files before upload.

### Content depth (lines)

| Asset | Lines | Zip size |
|-------|-------|----------|
| Agent Stack playbook | ~273 | 5.1 KB |
| Notion Ops template | **~500** | **6.4 KB** |
| MCP Tool Pack (10 crews + guides + loader) | **~1,000+ guide lines** | **28.9 KB** |
| Grok library | ~352 | 5.4 KB |
| Claude MPC | ~337 | 4.6 KB |
| Underrated techniques | ~296 | 4.7 KB |
| AI Toolchain | ~230+ | 3.9 KB |
| ClearTrace Privacy Ops + Agent Kit | ~400+ playbook | see below |

---

## Premium products (`products/`)

| Product | Price | Zip | Gumroad copy | Marketing |
|---------|-------|-----|--------------|-----------|
| **ClearTrace Privacy Ops + Agent Kit** | **$49** | `clear-trace.zip` | ✅ | ✅ |
| MCP Tool Pack — 10 Starter Crews | **$47** | `mcp-tool-pack-10-crews.zip` | ✅ | ✅ |
| Agent Ops Dashboard (Notion) | **$29** | `agent-ops-dashboard-notion.zip` | ✅ | ✅ |
| Agent Stack for Solo Builders | **$27** | `agent-stack-solo-builders.zip` | ✅ | ✅ |

**ClearTrace** — [github.com/Alfredapp-hash/Clear-Trace](https://github.com/Alfredapp-hash/Clear-Trace) (MIT). Gumroad sells the **operator playbook + agent builder setup**; full app is free to clone.

**Launch order (recommended):**
1. ClearTrace — unique SKU, open-source funnel + Gumroad playbook
2. MCP Tool Pack — highest price among kits, GitHub free-repo funnel
3. Grok Power User Library — broadest audience
4. Agent Stack — list-growth price point

---

## Prompt libraries (`prompt_libraries/`)

| Library | Price | Zip | Gumroad copy |
|---------|-------|-----|--------------|
| Grok & xAI Power User (20+ core + chains) | **$19** | `grok-xai-power-user-library.zip` | ✅ |
| Claude Power User & Tool MPC (19+) | **$22** | `claude-power-tool-mpc.zip` | ✅ |
| Underrated & Secret Techniques | **$17** | `underrated-secret-prompt-techniques.zip` | ✅ |
| AI Toolchain Master (Cursor, Claude, etc.) | **$24** | `ai-toolchain-master-library.zip` | ✅ |

**Bundle:** All 4 for **$57** — see `BUNDLE_AI_POWER_USER_GUMROAD.txt` (save $25 vs à la carte).

---

## Pre-launch checklist

- [ ] Run `python scripts/package_products.py`
- [ ] Upload zips to Gumroad (Settings → Advanced → Applications token in `.env`)
- [ ] MCP: create public GitHub repo from `FREE_REPO_README.md`
- [ ] Notion dashboard: duplicate template + take 3 screenshots
- [ ] Post from each product's `marketing/social_assets.md` (premium products)
- [ ] First post: MCP pack on X + r/LocalLLaMA or r/ChatGPT

---

## Not for sale (internal / test)

| Item | Location | Notes |
|------|----------|-------|
| Test Legal Prompt Pack | `generated_products/` | Agent test run only |
| Stub prompt dirs | `generated_products/claude-mpc-*` etc. | Use `prompt_libraries/` instead |
| DB test rows | `products.db` | IDs 1–2 are test data |

---

Forge aesthetic: modern, technical, blue gradients, professional.

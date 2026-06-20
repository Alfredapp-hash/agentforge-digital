# ClearTrace Privacy Ops Playbook

**Owner-controlled privacy remediation** · v0.8.0  
**Source:** [github.com/Alfredapp-hash/Clear-Trace](https://github.com/Alfredapp-hash/Clear-Trace) (MIT)

---

## One-liner

ClearTrace helps **authorized** individuals and teams find public exposures, file **factual** removal requests, verify takedowns, and **prove what happened** — with an auditable case file, your own API keys (BYOK), and optional automation.

---

## Who this is for

| Audience | Use case |
|----------|----------|
| Individuals | Remove outdated people-search listings, broker profiles, public-record snippets |
| Families & caregivers | Documented authority for dependent or estate subjects |
| Privacy professionals | Personal-brand exposure without black-box services |
| Small privacy teams | Structured cases, SLA tracking, broker sweeps, API integrations |
| Self-hosters | Deploy on your infra; every external API key is yours |

---

## The problem ClearTrace solves

Personal data spreads across dozens of brokers and aggregators. Each site has different opt-out paths, tone rules, and follow-up windows. Most privacy services hide what they send and whether work was done.

**ClearTrace inverts that:** you control credentials, approvals, outbound messages, and the audit trail.

---

## Hermes workflow (10 steps)

```
Intake → Discover → Verify → Resolve controller → Draft → Compliance
  → Record sent → Monitor → Verify removal → Follow-up
```

| Step | What happens | Human gate |
|------|--------------|------------|
| 1. Intake & consent | Encrypted identity signals, authority attestation, scopes | User confirms authority |
| 2. Discover | Demo (no keys) or live SERP (BYOK, Pro) | Review candidates |
| 3. Verify match | Candidate ↔ claim alignment, confidence score | Approve matches |
| 4. Resolve controller | Classify exposure + broker playbook routing | Confirm controller |
| 5. Draft | Factual removal templates; optional LLM polish (BYOK) | Edit draft |
| 6. Compliance | Checklist before anything goes out | **Required approval** |
| 7. Record sent | Log outbound channel and timestamp | — |
| 8. Schedule monitoring | Re-check cadence for resurfacing | — |
| 9. Verify removal | SSRF-safe live URL check | Confirm removed |
| 10. Follow-up | Escalation or certificate | Export proof |

*Classify and route run inline during step 4 — not separate Hermes steps.*

---

## Case workflow SOP (operator)

### Before first case

- [ ] Clone repo and run locally (`npm run dev`)
- [ ] Register account; create organization
- [ ] Run **demo discovery** (no API keys) to learn UI
- [ ] Read `agent-builder/skillpack/SAFETY_BOUNDARIES.md`
- [ ] Configure connectors you plan to use (Settings → Connectors)

### Opening a case

1. **Cases → New** — intake wizard
2. Title + case type + discovery scopes
3. Authority basis (self, authorized representative, etc.)
4. Encrypted identity claims — minimum necessary
5. Save; note case ID for audit

### Discovery phase

| Mode | When | Keys needed |
|------|------|-------------|
| Demo | Training, dry runs | None |
| Live SERP | Real removals | SerpAPI / Bing / Google CSE |
| Broker sweep | Pro — 50+ broker universe | Pro plan or self-host without Stripe |
| Live URL | Verification | None (built-in SSRF-safe fetch) |

### Drafting & compliance

- Use **rules-based templates** first — factual, no legal threats unless escalated via template
- Optional **LLM polish** (OpenAI / Anthropic / OpenRouter) — draft assistance only
- **Compliance gate** — nothing sends without explicit approval
- Outbound options: copy, mailto, Gmail draft push, opt-in SMTP/Resend/SendGrid/Postmark (Pro)

### Closing a case

- Run verification step; capture evidence
- Generate **removal certificate** + case export
- Archive or schedule monitoring for reappearance

---

## BYOK connector matrix

Configure at **Settings → Connectors**. Credentials encrypted per organization.

| Category | Providers | Purpose |
|----------|-----------|---------|
| Discovery | SerpAPI, Bing, Google CSE | Live SERP |
| Intelligence | OpenAI, Anthropic, OpenRouter | Draft polish only |
| Email | Gmail OAuth | Draft push to user's Gmail |
| Email send | SMTP, Resend, SendGrid, Postmark | Opt-in auto-send (Pro) |
| Webhook | Generic webhook | Case events (Pro + opt-in) |
| Billing | Stripe | Free 3 cases / Pro (optional — self-host can omit) |
| Breach intel | HIBP | Pro BYOK |

**Self-hosted tip:** Omit Stripe env vars → all Pro features available locally.

---

## Plans (when Stripe enabled)

| Plan | Cases | Key features |
|------|-------|--------------|
| Free | 3 | Demo discovery, full workflow UI, case export |
| Pro | 10,000 | Live SERP, broker sweep, SLA, API keys, ruthless mode, breach intel |

---

## Deployment options

### Local (development)

```bash
git clone https://github.com/Alfredapp-hash/Clear-Trace.git
cd Clear-Trace
cp .env.example .env.local
npm install
npm run dev
```

### Docker

```bash
docker compose up --build
```

### Vercel

- Connect repo; set env from `.env.example`
- SQLite: use compatible hosting or migrate per your ops policy
- See repo `vercel.json`

### Production guards

- Review `src/lib/config/production-guards.ts` requirements
- Enable rate limiting and session security for public deploys
- Never commit `.env.local` or connector secrets

---

## Feature matrix (v0.8)

| Capability | Status |
|------------|--------|
| Case workflow UI | Live |
| Demo discovery | Live |
| Live SERP | Pro (BYOK) |
| SSRF-safe URL fetch | Live |
| Rules classify + compliance | Live |
| LLM draft polish | Live (BYOK, optional) |
| Gmail draft push | Live (BYOK) |
| Email auto-send | Pro + opt-in |
| Hermes 10-step pipeline | Live |
| Batch remediation | Live |
| Case export + removal certificate | Live |
| Broker universe sweep | Pro |
| API keys `ct_live_…` | Pro |
| Agent builder kit (zip, MCP, CLI) | Live |

---

## Safety & legal boundaries

- ClearTrace is **workflow software**, not a law firm
- Users must have **authority** to act on behalf of the data subject
- Drafts are **factual removal requests** — not legal threats by default
- **Legal escalation skill** = template + export only — not automated filing
- Read full boundaries: `agent-builder/skillpack/SAFETY_BOUNDARIES.md` in repo

---

## Integrations with your agent stack

| Tool | Integration |
|------|-------------|
| Cursor / Claude / Windsurf | Agent Builder kit + MCP server |
| AgentForge MCP Tool Pack | Marketing crew for launch; Ops Notion for case logging |
| Notion Agent Ops Dashboard | Log Hermes runs, costs, case outcomes |
| External agents | Agent handoff packs from Guide panel (no secret leakage) |

---

## First 7 days (recommended)

| Day | Action |
|-----|--------|
| 1 | Clone, run locally, complete demo case |
| 2 | Configure one discovery connector (or stay on demo) |
| 3 | Install Agent Builder kit in Cursor (see `AGENT_BUILDER_SETUP.md`) |
| 4 | Run broker sweep on a test scope (Pro or self-host) |
| 5 | Complete compliance-reviewed draft (do not auto-send) |
| 6 | Export case packet; review audit timeline |
| 7 | Deploy to staging OR document your self-host runbook |

---

## Support & upstream

- **Issues:** https://github.com/Alfredapp-hash/Clear-Trace/issues
- **Changelog:** `CHANGELOG.md` in repo
- **Marketing overview:** `MARKETING.md` in repo

---

*Playbook curated for AgentForge Digital · Arkhe Holdings*

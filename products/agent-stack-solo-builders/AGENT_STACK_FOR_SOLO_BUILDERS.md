# Agent Stack for Solo Builders

**The Complete Playbook for Building, Running, and Monetizing AI Agents as a One-Person Business**

*Forge Edition | 2026*

## Introduction
Solo builders don't need 50 agents. They need a small, reliable stack that compounds.

This playbook gives you the exact system used by high-output indies to:
- Automate repetitive work
- Ship digital products faster
- Generate revenue with minimal ongoing effort

## Core Philosophy
- Start small (3-5 agents max)
- Make every agent observable and cheap
- Productize outputs immediately
- Use marketing automation to sell what you build

## The Recommended 5-Agent Stack

1. **Researcher** — Always-on trend & opportunity finder
2. **Creator** — Turns research into sellable artifacts (prompts, playbooks, templates)
3. **Optimizer** — Reviews and improves everything (including other agents)
4. **Marketer** — Generates launch assets, copy, and promotion plans
5. **Ops** — Tracks runs, costs, sales; feeds data back to Optimizer

## How to Implement (Step-by-Step)

### Step 1: Choose Your LLM Backbone
- Primary: grok-4.3 (via xAI) — great reasoning/cost balance
- Secondary: Claude for writing-heavy tasks
- Fallback: GPT-4o-mini for simple tasks

Use the Settings tab in AgentForge to switch.

### Step 2: Set Up Your Ops Dashboard
Duplicate the Agent Ops Dashboard (Notion) template. Log every run. This is non-negotiable for iteration.

### Step 3: Start with the MCP Tool Pack
Use the 10 Starter Crews as your foundation. Customize one per week.

### Step 4: Build Your First Product
Use the stack to generate one sellable thing per week:
- Week 1: One prompt library
- Week 2: One tool-specific MPC
- Week 3: One "secret techniques" pack

### Step 5: Automate the Marketing
Every product gets the full marketing package automatically (see AgentForge automation).

### Step 6: Close the Loop
- Run sales sync weekly
- Feed winners into the Optimizer crew
- Clone what works, kill what doesn't

## Daily/Weekly Operating Rhythm (Solo)

**Daily (15-30 min):**
- Review Ops dashboard
- Trigger one small crew run
- Log results

**Weekly (2-3 hours):**
- Run full Research + Creator + Marketer pipeline
- Ship one product or update
- Post the generated social assets
- Send one email from the sequence

**Monthly:**
- Full Strategist + Optimizer review
- Update your highest performers
- Launch a bundle or OTO

## Pricing & Sales Psychology for Your Products
- $17-29 for single packs (low friction)
- $47-67 for bundles/MCPs
- $97+ Blueprint OS as OTO on every thank-you page
- Use launch pricing + bonuses for urgency

## Common Pitfalls & Fixes
- Too many agents → start with the 5 above
- No tracking → use the Notion dashboard
- Generic output → feed better research + use the Optimizer
- No sales → run the Marketer crew every time

## Advanced Moves
- Chain crews (output of one = input of next)
- Productize your own stack (sell the exact setup you're using)
- Add your own custom tools to the crews

---

**This is not theory.** This is the operating system that turns one person + good AI access into a real product business.

Start with the Ops Dashboard + one crew from the MCP Pack today.

Next product ideas will come from the Ideator crew.

Ship. Market. Iterate. Repeat.

---

## Deep Dive: Each Agent in the Stack

### 1. Researcher — Your Opportunity Radar

**Job:** Find what to build and what angle will sell before you spend tokens creating.

**Inputs:** Niche keywords, competitor URLs, trend signals, your past winners from Ops dashboard.

**Outputs:** Opportunity brief with buyer pain, price band, format recommendation, 3 keyword clusters.

**Default crew:** MCP `01_research_crew.yaml`

**Prompt pattern:**
```
Find 3 digital product opportunities in [NICHE] that:
- Can be built in <4 hours with AI assistance
- Sell for $17–47 on Gumroad
- Have clear buyer intent (people already paying for similar)
- Low refund risk (templates, prompts, playbooks)

For each: name, one-sentence pain, competitor examples, suggested price, GO/NO-GO.
```

**KPI:** 1 qualified opportunity per week you would actually build.

---

### 2. Creator — Turns Research into Sellable Files

**Job:** Produce the actual deliverable customers download — not a summary of what you *could* build.

**Inputs:** Research brief, format (prompt pack / Notion spec / YAML crews / playbook).

**Outputs:** `product.md`, optional PDF, zip-ready folder structure.

**Default crew:** MCP `02_content_writer_crew.yaml` + your domain expertise pass.

**Quality bar before shipping:**
- [ ] Customer can use it in <15 minutes without support
- [ ] At least 8–20 concrete, copy-paste assets (not bullet outlines)
- [ ] Clear table of contents and usage instructions
- [ ] No placeholder `[TODO]` sections

---

### 3. Optimizer — Kills Weak Products Before They Damage Your Brand

**Job:** Score quality and profit potential; force rewrites on anything below threshold.

**Inputs:** Product draft + listing draft + research brief.

**Outputs:** GO/NO-GO, quality 1–10, profit 1–10, specific fixes.

**Default crew:** MCP `10_agent_optimizer_crew.yaml`

**Hard rule:** Never publish below **7/10 quality** and **6/10 profit** unless it's a deliberate lead magnet at $0–9.

---

### 4. Marketer — Makes Money After the Product Exists

**Job:** Generate launch assets that drive traffic — not "marketing ideas."

**Inputs:** Finished product, price, target buyer, competitor positioning.

**Outputs:** Gumroad A/B variants, X thread, LinkedIn post, Reddit post, 5-email sequence, launch calendar.

**Default crew:** MCP `04_marketing_launch_crew.yaml`

**Minimum launch package:** 3 social posts + 1 email + Gumroad listing variant A live on day 0.

---

### 5. Ops — Memory for the Whole System

**Job:** Log every run, cost, decision, and sale so the Optimizer has data.

**Inputs:** Run logs, Gumroad sales sync, agent configs.

**Outputs:** Weekly ops review, cost per product, winner/loser list, next-week priorities.

**Tool:** Agent Ops Dashboard (Notion) — non-negotiable.

**Weekly Ops review (15 min):**
1. Total spend this week (tokens + tools)
2. Products shipped vs. published vs. sold
3. Top 3 runs by output quality (save prompts)
4. Bottom 3 runs (delete or fix configs)
5. One experiment for next week

---

## Crew Chains That Compound

| Chain | Flow | Use when |
|-------|------|----------|
| **Ship pipeline** | Research → Creator → Optimizer → Marketer | New product weekly |
| **Fast refresh** | Optimizer → Creator | Update a winner with v2 |
| **Launch only** | Marketer (feed existing zip) | Product ready, no sales |
| **Meta loop** | Ops data → Agent Optimizer → edit YAMLs | Monthly tuning |

**Example chain input:**
```
Week goal: Ship "Cursor Rules Pack for Solo Devs" at $19.
Run Research on Cursor power-user pain → Creator builds 25+ rules → Optimizer gates → Marketer launches.
Log all runs in Notion with product_id = cursor-rules-v1.
```

---

## 12-Week Solo Builder Roadmap

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1 | Setup | Notion Ops + 3 agents registered |
| 2 | First SKU | 1 prompt library live on Gumroad |
| 3 | Traffic | 5 organic posts from Marketer output |
| 4 | Second SKU | MCP-adjacent product (crews/templates) |
| 5 | Bundle | 2-pack bundle at 1.5× single price |
| 6 | Data | First sales sync + Optimizer review |
| 7 | Clone winner | Variation of top performer |
| 8 | GitHub funnel | Free repo → paid upsell (MCP model) |
| 9 | Email | Send full 5-email sequence |
| 10 | OTO | Thank-you page upsell to higher ticket |
| 11 | Prune | Archive SKUs with 0 views in 30 days |
| 12 | Systemize | Document your exact stack as a product |

---

## Tool Stack Reference (2026)

| Layer | Recommended | Free alternative |
|-------|-------------|------------------|
| Primary LLM | Grok 4 (xAI) | Gemini Flash (free API) |
| Writing polish | Claude Sonnet | Same model, higher temp pass |
| Cheap tasks | GPT-4o-mini | Groq Llama 3.3 70B |
| Agent framework | CrewAI | Same |
| Search | DuckDuckGo / Perplexity | DDG (free) |
| Store | Gumroad | Same |
| Ops | Notion dashboard | SQLite + Streamlit |
| Automation | `autonomy_runner.py` + cron | Manual weekly runs |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Generic AI slop output | Tighter research brief + Optimizer pass + negative prompting |
| High cost, low output | Shorter agents, fewer tasks, cheaper model for draft |
| Products don't sell | Marketer crew every time; post assets same day as publish |
| Too many WIP products | Ops rule: max 2 unpublished drafts |
| Agent configs drift | Version YAMLs in git; log model + prompt hash in Notion |

---

## Legal & Professional Niche Angles (Your Edge)

As a law student / professional audience builder, high-converting micro-niches:
- Legal research prompt packs (IRAC, memo, exam prep)
- Professional writing MPCs (briefs, client emails — with disclaimers)
- Student productivity + AI toolchain libraries
- "Agent ops for solo professionals" (Notion + crews)

Position as productivity tools, not legal advice. Include disclaimer on legal-adjacent products.

---

*Generated with the AgentForge system. Curated and branded for the Forge aesthetic.*

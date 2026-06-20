# Guide: Product Ideator Crew

**When to use:** Weekly ideation, niche selection, spec before build, Gumroad SKU planning.

**Agents:** Opportunity Scanner → Feasibility Analyst → Product Architect (sequential)

---

## Setup

```bash
pip install crewai pyyaml python-dotenv
export XAI_API_KEY=...   # or OPENAI_API_KEY
python crew_loader.py crews/05_product_ideator_crew.yaml "Your niche and constraints"
```

---

## Inputs to provide

| Field | Example |
|-------|---------|
| Niche | "AI tools for law students" / "CrewAI builders" |
| Skills | What you can actually build |
| Audience | Who already pays for similar things |
| Price band | $17–47 |
| Time budget | "4 hours to ship" |
| Avoid | Topics you won't do |

**Strong input template:**
```
Niche: [NICHE]
My skills: [LIST]
Audience: [WHO PAYS TODAY]
Price range: $[MIN]-$[MAX]
Build time limit: [HOURS]
Do NOT suggest: [EXCLUSIONS]
Past winners (if any): [WHAT SOLD OR GOT TRACTION]
```

---

## Outputs you get

1. **5–10 ideas** — name + one-line pain + rough price each
2. **Scored matrix** — Build Speed, Demand, Competition, Margin, Refund Risk (1–10) + GO/NO-GO
3. **Product spec** for #1 pick — title, TOC, format, price, tags, launch hook

Feed the spec directly into **Content Writer (02)** or AgentForge autonomous cycle.

---

## Customization

- **Law / professional angle:** "Buyer is law student or solo attorney; productivity tools only, not legal advice"
- **Clone winners:** Paste Gumroad URLs of products that sold in your niche
- **Format bias:** "Prefer prompt packs and Notion templates over courses"
- **Tight scoring:** Ask Analyst to kill anything below 7/10 on Demand Signal

---

## Pro tips

- Run **weekly** — same day you do Notion ops review
- Log winning specs in Notion **Products** DB before building
- Don't build more than **one new SKU per week** from ideator output
- If all ideas score NO-GO, narrow niche — don't widen

---

## Example inputs

- `"Digital products for solo AI builders. $20-50. I ship Markdown zips and YAML crews. 4hr build max."`
- `"Prompt packs for law students — exam prep and writing workflows. No legal advice products."`
- `"Variations of our bestselling Grok prompt library — what's the next SKU?"`

---

## Chain with

| Before | After |
|--------|-------|
| **Product Ideator (05)** | Research (01) to validate top pick |
| **Product Ideator (05)** | Content Writer (02) to build |
| **Product Ideator (05)** | Marketing (04) to launch |
| Ops dashboard sales data | **Product Ideator (05)** — paste top niches |

**Expected runtime:** 6–12 min.

---

## Scoring rubric (what Analyst uses)

| Dimension | 10 means | 1 means |
|-----------|----------|---------|
| Build Speed | Ship today | Weeks of work |
| Demand Signal | People already buying similar | No evidence |
| Competition | Clear wedge | Saturated |
| Margin | $29+ digital, low support | High refund risk |
| Refund Risk | Templates/prompts | Custom consulting feel |

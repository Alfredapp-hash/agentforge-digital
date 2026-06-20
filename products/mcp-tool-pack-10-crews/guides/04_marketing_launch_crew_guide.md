# Guide: Marketing & Launch Crew

**When to use:** Product launches, Gumroad listings, content calendars, campaign planning, relaunches with scarcity.

**Agents:** Market Researcher → Copywriter → Launch Strategist (sequential)

---

## Setup

```bash
pip install crewai pyyaml python-dotenv
export XAI_API_KEY=...   # or OPENAI_API_KEY
python crew_loader.py crews/04_marketing_launch_crew.yaml "Launch my product at $X"
```

---

## Inputs to provide

| Field | Example |
|-------|---------|
| Product name | "MCP Tool Pack — 10 Starter Crews" |
| What's inside | Bullet list of deliverables |
| Target buyer | Specific persona — not "everyone" |
| Price | $47 launch / $57 after 48h |
| Launch window | 7 days / 48-hour scarcity |
| Competitors | Similar Gumroad products (optional) |
| Voice | Professional / indie hacker / technical |

**Strong input template:**
```
Product: [NAME]
Price: $[X] (launch) → $[Y] (after)
Buyer: [WHO + THEIR PAIN]
Inside:
- [BULLET]
- [BULLET]
Competitors: [NAMES OR URLS]
Launch window: [DAYS]
Voice: [TONE]
CTA: [Gumroad / email list / GitHub repo]
```

---

## Outputs you get

1. **Launch research brief** — avatar, hooks, channels, competitor angles
2. **Copy pack** — 3 Gumroad variants (A/B/C), X thread, LinkedIn, Reddit, ad headlines
3. **7-day launch calendar** — daily actions + bundle/upsell ideas with pricing

Save to `outputs/marketing_launch_crew/result.md` via `crew_loader.py`.

---

## Customization

- **Paste winning copy** from past launches as "style reference" in input
- **Channel focus:** "Optimize for X thread + r/LocalLLaMA only"
- **Bundle push:** "Include upsell to Agent Ops Notion at $29"
- **No paid ads:** "Organic only — maximize Reddit and X"

---

## Pro tips

- **Ship same day** — launch assets decay; post within 24 hours of crew run
- Use **Variant A** on Gumroad day 0; save B/C for day 3 refresh if views stall
- Paste Reddit post to **Customer Insight (06)** after comments roll in
- Run **Optimizer (10)** if copy feels generic before posting

---

## Example inputs

- `"Launch MCP Tool Pack at $47 to indie CrewAI builders. Include GitHub free-repo funnel mention."`
- `"Relaunch Grok prompt library at $19 with 48-hour scarcity. Audience: xAI power users."`
- `"Soft launch Notion Agent Ops dashboard to r/Notion — $29, screenshot-heavy listing."`

---

## Chain with

| Before | After |
|--------|-------|
| Content Writer (02) finished product | **Marketing (04)** |
| Product Ideator (05) spec | **Marketing (04)** for pre-launch teasers |
| **Marketing (04)** | You post + publish Gumroad same day |
| Post-launch comments | Customer Insight (06) |

**Expected runtime:** 5–15 min depending on model.

---

## Day-0 launch checklist

- [ ] Gumroad live with Variant A title + description
- [ ] Zip attached and test purchase flow
- [ ] X thread posted (thread, not single tweet)
- [ ] One Reddit post in relevant sub (read rules first)
- [ ] Email 1 sent if you have a list
- [ ] Run logged in Notion with tag `launch`

---

## Channel notes

| Channel | What works for these products |
|---------|-------------------------------|
| X | Threads with specific hooks + screenshot |
| Reddit | Value-first post, link in comments if required |
| LinkedIn | Professional angle — ops, productivity, builders |
| Gumroad Discover | Tags matter — use all 8 from copy pack |

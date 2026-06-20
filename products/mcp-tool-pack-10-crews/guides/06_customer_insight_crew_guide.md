# Guide: Customer Insight & Support Crew

**When to use:** Post-launch feedback, refund prevention, FAQ building, v1.1 roadmap from real user language.

**Agents:** Feedback Synthesizer → Objection Handler → Product Improver (sequential)

---

## Setup

```bash
pip install crewai pyyaml python-dotenv
export XAI_API_KEY=...   # or OPENAI_API_KEY
python crew_loader.py crews/06_customer_insight_crew.yaml "Paste feedback here"
```

---

## Inputs to provide

| Source | Format |
|--------|--------|
| Gumroad reviews | Copy-paste text |
| Support emails | Anonymized threads |
| Twitter/Reddit replies | Screenshots as text |
| Refund reasons | If Gumroad provides them |
| Your notes | "3 people asked about X" |

**Strong input template:**
```
Product: [NAME + PRICE]
Time period: [DATES]
Volume: [N reviews, N emails]

Raw feedback:
[PASTE EVERYTHING — messy is fine]

Known issues we're aware of:
[LIST OR "none"]
```

---

## Outputs you get

1. **Synthesis report** — top 5 themes, frequency, revenue impact, representative quotes
2. **Support playbook** — 3+ copy-paste replies + FAQ blocks for top objections
3. **Improvement backlog** — 3–5 product updates ranked by effort vs. impact

---

## Customization

- **Tone:** "Support voice: friendly, specific, no corporate — Arkhe / Forge brand"
- **Legal products:** "Never give legal advice in replies; redirect to productivity use"
- **Proactive FAQ:** Ask for Gumroad description FAQ section ready to paste
- **Churn focus:** "Prioritize themes correlated with refunds or confusion at checkout"

---

## Pro tips

- Run after **every 5 sales** or **first refund** — whichever comes first
- Paste confused buyer questions **verbatim** — they're gold for listing copy fixes
- Ship **one v1.1 improvement** per month from Improver output (bonus PDF, clarified section)
- Feed FAQ into **Marketing crew (04)** for updated listing variant B

---

## Example inputs

- `"Analyze these 8 Gumroad reviews for Grok prompt library. Product at $19. [PASTE]"`
- `"Reddit comments on our MCP pack launch thread — extract objections and FAQ. [PASTE]"`
- `"3 buyers asked how to load YAML in CrewAI 1.14 — turn into support doc + product fix."`

---

## Chain with

| Before | After |
|--------|-------|
| Sales + reviews | **Customer Insight (06)** |
| **Customer Insight (06)** | Content Writer (02) for v1.1 content |
| **Customer Insight (06)** | Marketing (04) for listing refresh |
| **Customer Insight (06)** | Prompt Engineer (07) if prompts are the issue |

**Expected runtime:** 5–10 min.

---

## Red flags to act on immediately

| Signal | Action |
|--------|--------|
| "Didn't know how to use it" | Add 5-min quickstart to zip |
| "Not worth the price" | Compare to listing promise; add bonus or cut price |
| "Generic ChatGPT prompts" | Run Optimizer + rewrite with tool-specific examples |
| Same question 3+ times | FAQ + listing bullet above fold |

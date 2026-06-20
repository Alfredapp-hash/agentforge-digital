# Guide: Data Analyzer Crew

**When to use:** Gumroad sales review, agent cost analysis, content performance, experiment results, `products.db` interpretation.

**Agents:** Data Cleaner → Insight Analyst → Report Writer (sequential)

---

## Setup

```bash
pip install crewai pyyaml python-dotenv
export XAI_API_KEY=...   # or OPENAI_API_KEY
python crew_loader.py crews/08_data_analyzer_crew.yaml "Describe your dataset or paste CSV"
```

---

## Inputs to provide

| Data type | How to pass |
|-----------|-------------|
| CSV export | Paste text or attach summary |
| SQLite / JSON | Paste query results |
| Gumroad dashboard | Manual export or API summary |
| AgentForge `products.db` | `sqlite3 products.db "SELECT ..."` output |
| Narrative metrics | "12 runs, 3 GO, $4.20 spent, 0 sales" |

**Strong input template:**
```
Dataset: [NAME]
Period: [DATES]
Question I need answered: [SPECIFIC — not "analyze everything"]

Data:
[PASTE CSV / TABLE / QUERY RESULTS]

Context:
[what decisions this informs]
```

---

## Outputs you get

1. **Data profile** — quality flags, missing values, feasible questions
2. **Insight brief** — top 5 findings with confidence + caveats
3. **Executive report** — summary, recommendations, follow-up analyses

---

## Customization

- **AgentForge ops:** Export `run_history` and `products` tables — ask for cost-per-GO-product
- **Gumroad:** Include product name, price, views if available (even rough)
- **Conservative stats:** "Don't overfit — flag small sample sizes"
- **Action-only:** "Skip methodology — I want 3 decisions only"

---

## Pro tips

- Run **monthly** alongside Notion weekly review
- Combine with **Product Ideator (05)** — paste analyst report as "past winners"
- If N < 10 sales, focus on **leading indicators** (views, email signups, post engagement)
- Log the report link in Notion **Runs** with tag `analytics`

---

## Example inputs

- `"Analyze AgentForge run_history: which topics got GO vs NO-GO? [PASTE SQL OUTPUT]"`
- `"Gumroad sales last 30 days — 2 products, 0 sales, 400 combined views. What to change?"`
- `"Agent token spend by crew type this week. Budget is $20. [PASTE COST LOG]"`

---

## Chain with

| Before | After |
|--------|-------|
| Gumroad sync / DB export | **Data Analyzer (08)** |
| **Data Analyzer (08)** | Product Ideator (05) |
| **Data Analyzer (08)** | Agent Optimizer (10) |
| **Data Analyzer (08)** | Marketing (04) for messaging pivots |

**Expected runtime:** 5–12 min.

---

## Sample SQLite queries (AgentForge)

```sql
-- Recent runs with decisions
SELECT topic, decision, quality_score, profit_score, est_cost_cents, published
FROM run_history ORDER BY timestamp DESC LIMIT 20;

-- Products logged
SELECT title, status, price_cents/100.0 AS price, sales, revenue_cents/100.0 AS revenue
FROM products ORDER BY created DESC;
```

Paste results into crew input.

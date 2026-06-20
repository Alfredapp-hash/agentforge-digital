# Guide: Agent Optimizer (Meta) Crew

**When to use:** Weekly ops review, post-mortem on failed runs, cost reduction, crew architecture refactors.

**Agents:** Performance Auditor → Prompt Refiner → Architecture Advisor (sequential)

---

## Setup

```bash
pip install crewai pyyaml python-dotenv
export XAI_API_KEY=...   # or OPENAI_API_KEY
python crew_loader.py crews/10_agent_optimizer_crew.yaml "Paste logs or describe problems"
```

---

## Inputs to provide

| Source | What to include |
|--------|-----------------|
| Notion Runs export | Last 10–20 runs with cost, success, notes |
| `run_history` SQL | AgentForge DB export |
| YAML configs | Crews that underperformed |
| Symptoms | "Too expensive" / "generic output" / "timeouts" |
| Goals | Target cost per run, quality bar |

**Strong input template:**
```
System: [WHAT YOU'RE RUNNING — e.g. AgentForge 6-agent cycle]
Period: [LAST WEEK / LAST 10 RUNS]
Goals: [COST TARGET, QUALITY TARGET]

Symptoms:
- [LIST]

Run log / config:
[PASTE NOTION EXPORT, SQL, OR YAML]

Constraints:
- [e.g. keep 6 agents, can't change model provider]
```

---

## Outputs you get

1. **Audit report** — top 3 failure modes, cost drivers, quality bottlenecks (with evidence)
2. **Revised prompts** — before/after for weakest agents; target 20–40% token reduction
3. **Architecture memo** — merge/split agents, reorder tasks, tool additions, expected impact

---

## Customization

- **AgentForge specific:** Paste `build_autonomous_tasks` agent list + sample `agentforge.log` tail
- **Cost focus:** "Primary goal: cut $/run 30% without dropping below 7/10 quality"
- **Quality focus:** "Primary goal: fix NO-GO rate — currently 60% NO-GO"
- **Single crew:** Optimize one YAML from MCP pack instead of full stack

---

## Pro tips

- Run **every Friday** with Notion weekly review — non-negotiable for solo builders
- Implement **one architecture change** per month max (avoid thrash)
- After Refiner edits YAML, version in git: `crews/01_research_crew.v2.yaml`
- Feed Auditor output to **Product Ideator (05)** if market fit is the issue, not prompts

---

## Example inputs

- `"Audit AgentForge full cycle — 8 runs, 5 NO-GO, avg $0.45/run. [PASTE run_history]"`
- `"Marketing crew outputs feel generic. [PASTE YAML + SAMPLE OUTPUT]"`
- `"Research crew uses too many tokens. Target $0.15/run. [PASTE CONFIG + LOGS]"`

---

## Chain with

| Before | After |
|--------|-------|
| Data Analyzer (08) metrics | **Optimizer (10)** |
| **Optimizer (10)** | Prompt Engineer (07) for deep rewrites |
| **Optimizer (10)** | You edit YAML + re-test |
| Failed production run | **Optimizer (10)** same day |

**Expected runtime:** 8–15 min.

---

## Meta loop (recommended monthly)

```
Week 1–3: Ship + log everything in Notion
Week 4: Data Analyzer (08) → Optimizer (10) → apply top 2 fixes
```

This is how the Agent Stack playbook's **Optimizer agent** earns its slot.

---

## Red flags the Auditor should catch

| Pattern | Likely fix |
|---------|------------|
| Same agent on 4+ tasks | Split or narrow backstory |
| Marketing before quality review | Reorder tasks |
| 15k+ char outputs materialized raw | Structured outputs + truncation |
| Identical failures 3× | Change model or prompt, not more retries |

# MCP Tool Pack: 10 Starter Crews · $47

**10 ready-to-run CrewAI (or similar) crew configurations + one-page setup guides.**

## What's Included
- 10 YAML config files in `/crews/`
- One-page setup + usage guide per crew in `/guides/`
- Master README with installation and customization tips
- Bonus: How to turn these into sellable products or internal tools

## Quick Start (CrewAI)
1. `pip install crewai crewai-tools pyyaml python-dotenv`
2. Copy a YAML from `crews/` into your project (or run from this folder).
3. **Fast path:** `python crew_loader.py crews/04_marketing_launch_crew.yaml "Your product topic here"`
4. Or build agents manually from YAML (example below).
5. Set `XAI_API_KEY` or `OPENAI_API_KEY`.
6. Run the crew.

Example loader (Python):
```python
import yaml
from crewai import Agent, Task, Crew

with open("crews/01_research_crew.yaml") as f:
    config = yaml.safe_load(f)

# Build agents and tasks from config (expand as needed)
# Then:
crew = Crew(agents=agents, tasks=tasks, process="sequential")
result = crew.kickoff()
print(result)
```

## The 10 Crews
1. Research Crew — [`guides/01_research_crew_guide.md`](guides/01_research_crew_guide.md)
2. Content Writer Crew — [`guides/02_content_writer_crew_guide.md`](guides/02_content_writer_crew_guide.md)
3. Code Reviewer & Builder Crew — [`guides/03_code_reviewer_crew_guide.md`](guides/03_code_reviewer_crew_guide.md)
4. Marketing & Launch Crew — [`guides/04_marketing_launch_crew_guide.md`](guides/04_marketing_launch_crew_guide.md)
5. Product Ideator Crew — [`guides/05_product_ideator_crew_guide.md`](guides/05_product_ideator_crew_guide.md)
6. Customer Insight & Support Crew — [`guides/06_customer_insight_crew_guide.md`](guides/06_customer_insight_crew_guide.md)
7. Prompt Engineer Crew — [`guides/07_prompt_engineer_crew_guide.md`](guides/07_prompt_engineer_crew_guide.md)
8. Data Analyzer Crew — [`guides/08_data_analyzer_crew_guide.md`](guides/08_data_analyzer_crew_guide.md)
9. Learning & Study Tutor Crew — [`guides/09_learning_tutor_crew_guide.md`](guides/09_learning_tutor_crew_guide.md)
10. Agent Optimizer (Meta) Crew — [`guides/10_agent_optimizer_crew_guide.md`](guides/10_agent_optimizer_crew_guide.md)

Each guide includes: setup command, input templates, outputs, customization, chains, examples, and runtime estimates.

## Free Marketing Repo Strategy
Fork or create a public GitHub repo called `mcp-starter-crews`.
- Put the YAMLs + minimal README.
- Link to this Gumroad product for the full guides + updates.
- The free repo drives traffic to the paid pack.

## OTO / Bundle Ideas
- Pair with Agent Ops Dashboard (Notion)
- Upsell to full Agent Stack for Solo Builders
- Include in Blueprint OS

Build time: 2-3 days as described. High perceived value for indie hackers and agent builders.

---
Generated as part of AgentForge product suite.
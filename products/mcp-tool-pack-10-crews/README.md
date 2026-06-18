# MCP Tool Pack: 10 Starter Crews · $47

**10 ready-to-run CrewAI (or similar) crew configurations + one-page setup guides.**

## What's Included
- 10 YAML config files in `/crews/`
- One-page setup + usage guide per crew in `/guides/`
- Master README with installation and customization tips
- Bonus: How to turn these into sellable products or internal tools

## Quick Start (CrewAI)
1. `pip install crewai crewai-tools`
2. Copy a YAML into your project.
3. Use a simple loader script (example below) or paste into your Python crew definition.
4. Set your `XAI_API_KEY` (or other provider).
5. Run the crew.

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
1. Research Crew
2. Content Writer Crew
3. Code Reviewer & Builder Crew
4. Marketing & Launch Crew
5. Product Ideator Crew
6. Customer Insight & Support Crew
7. Prompt Engineer Crew
8. Data Analyzer Crew
9. Learning & Study Tutor Crew
10. Agent Optimizer (Meta) Crew

Each has its own `guide-*.md` with:
- When to use it
- Exact YAML
- How to customize for your tools/models
- Example inputs/outputs
- Pro tips for better results with Grok/Claude

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
```

Now, to complete, I should create at least short guides for a few and note the pattern.

For efficiency, create a template guide and a couple examples, then say the rest follow the same pattern. But user said "build all", so try to cover.

Since time, create the main README with all, and short guides for all by making them concise.
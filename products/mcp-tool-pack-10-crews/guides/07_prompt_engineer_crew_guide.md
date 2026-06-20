# Guide: Prompt Engineer Crew

**When to use:** Building prompt products, tuning crew backstories, fixing weak agent output, creating MPCs for sale.

**Agents:** Prompt Architect → Prompt Tester → MPC Curator (sequential)

---

## Setup

```bash
pip install crewai pyyaml python-dotenv
export XAI_API_KEY=...   # or OPENAI_API_KEY
python crew_loader.py crews/07_prompt_engineer_crew.yaml "Your use case and goals"
```

---

## Inputs to provide

| Field | Example |
|-------|---------|
| Use case | "Autonomous Gumroad product research" |
| Target model | Grok 4, Claude Sonnet, GPT-4o-mini |
| Output type | Single prompt / 5-pack / full MPC library |
| Current prompt | Paste if improving existing |
| Failure modes | What's going wrong today |

**Strong input template:**
```
Use case: [WHAT USER IS TRYING TO DO]
Model: [PRIMARY MODEL]
Deliverable: [N PROMPTS / MPC / SYSTEM PROMPT]
Audience skill level: [beginner / power user]

Current prompt (if any):
[PASTE]

Known failures:
- [e.g. generic output, ignores format, too long]
```

---

## Outputs you get

1. **5–8 draft prompts** — role, constraints, output format, advanced technique each
2. **Test report** — edge-case scores 1–10 + fixes for anything below 8
3. **Customer-ready MPC** — categorized Markdown with usage guide

---

## Customization

- **CrewAI agents:** Ask for YAML `backstory` + `goal` rewrites, not just user prompts
- **Structured output:** Request Pydantic-friendly JSON schemas in prompts
- **Token budget:** "Each prompt must work under 2k output tokens"
- **Cross-model:** Ask Curator for Grok + Claude variants side-by-side

---

## Pro tips

- Run this crew on **your worst-performing agent** first — highest ROI
- After editing YAML, run **one cheap test cycle** before full crew kickoff
- Save winning prompts to Notion **Prompt Library** DB with version tags
- This crew improves **all other crews** — schedule monthly

---

## Example inputs

- `"Design 6 prompts for legal exam issue-spotting study aids. Model: Claude. Not legal advice."`
- `"Rewrite Research crew agent backstories for less verbose output. [PASTE YAML SNIPPET]"`
- `"Build a sellable 'Cursor rules generator' MPC — 10 prompts, power user audience."`

---

## Chain with

| Before | After |
|--------|-------|
| Optimizer (10) flags weak prompts | **Prompt Engineer (07)** |
| **Prompt Engineer (07)** | Content Writer (02) for MPC packaging |
| Product Ideator (05) spec | **Prompt Engineer (07)** |
| **Prompt Engineer (07)** | Code Reviewer (03) if prompts live in code |

**Expected runtime:** 10–20 min for full MPC.

---

## Quality bar for sellable MPCs

- [ ] Every prompt has `[BRACKETS]` for variables
- [ ] Usage instructions per category
- [ ] At least one meta-prompt included
- [ ] No duplicate patterns across prompts
- [ ] Tester scored all ≥8 or revised

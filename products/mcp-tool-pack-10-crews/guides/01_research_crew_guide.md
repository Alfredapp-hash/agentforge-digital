# Guide: Research Crew

**When to use:** Deep dives, competitive analysis, trend research, niche validation before you build a product.

**Agents:** Senior Researcher → Fact Checker (sequential)

---

## Setup

```bash
pip install crewai crewai-tools pyyaml python-dotenv
export XAI_API_KEY=...   # or OPENAI_API_KEY
python crew_loader.py crews/01_research_crew.yaml "Your research topic"
```

**Note:** Research crew YAML references `web_search` tool — install `ddgs` or `duckduckgo-search` for live search.

---

## Inputs to provide

| Field | Example |
|-------|---------|
| Topic | Specific question or niche — not "AI" |
| Depth | Quick scan / standard / deep dive |
| Output use | Product ideation / blog / investor memo |
| Geography / audience | US law students, indie hackers, etc. |
| Must answer | 3–5 explicit questions |

**Strong input template:**
```
Topic: [SPECIFIC RESEARCH QUESTION]
Audience: [WHO CARES]
Purpose: [DECIDE WHETHER TO BUILD / WRITE / INVEST]
Must answer:
1. [QUESTION]
2. [QUESTION]
3. [QUESTION]
Competitors to check (optional): [URLS OR NAMES]
```

---

## Outputs you get

1. **Research brief** — comprehensive synthesis with sources
2. **Verified report** — fact-check pass, confidence levels, contradictions flagged

Log in Notion **Runs** with tag `research` and link to **Tasks** if spawning Content Writer next.

---

## Customization

- **Tools:** Add Perplexity, arXiv, or file read tools in YAML for your stack
- **Model:** Grok 4 for reasoning-heavy markets; GPT-4o-mini for quick scans
- **Domain:** Add backstory line: "Prioritize primary sources and recent data (2025–2026)"
- **Product research:** Ask for Gumroad competitor pricing and format recommendations in input

---

## Pro tips

- **Always run first** in the ship pipeline — Creator crew without research = generic slop
- Narrow the topic — "AI prompt packs for 1L law students" beats "AI in education"
- Paste research output into **Product Ideator (05)** or **Content Writer (02)** same session
- Save high-confidence findings to Notion **Prompt Library** as "research prompts that work"

---

## Example inputs

- `"Validate demand for CrewAI starter YAML packs at $47 — competitors, pricing, buyer pain."`
- `"Impact of free Gemini API on indie AI product businesses in 2026 — opportunities and threats."`
- `"What Notion templates for AI agents sell best? Top 5 examples and price bands."`

---

## Chain with

| Before | After |
|--------|-------|
| Product Ideator (05) rough idea | **Research (01)** to validate |
| **Research (01)** | Content Writer (02) |
| **Research (01)** | Product Ideator (05) if research kills the idea |

**Expected runtime:** 8–20 min with web search enabled.

---

## Quality signals in output

- [ ] Named competitors or analogs with prices
- [ ] Contradictions or uncertainties flagged honestly
- [ ] Actionable recommendation (build / pivot / kill)
- [ ] Sources cited or source class noted (primary vs. opinion)

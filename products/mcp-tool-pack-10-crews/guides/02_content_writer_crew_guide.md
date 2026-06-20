# Guide: Content Writer Crew

**When to use:** Blog posts, Gumroad sales pages, newsletters, product documentation, prompt pack intros, playbook chapters.

**Agents:** Research Synthesizer → Writer → Editor (sequential)

---

## Setup

```bash
pip install crewai pyyaml python-dotenv
export XAI_API_KEY=...   # or OPENAI_API_KEY
python crew_loader.py crews/02_content_writer_crew.yaml "Your topic and brief here"
```

**Or** load `crews/02_content_writer_crew.yaml` manually and wire agents/tasks in your own script.

---

## Inputs to provide

| Field | Example |
|-------|---------|
| Topic | "Launch post for Agent Ops Notion template" |
| Audience | "Solo builders using CrewAI" |
| Format | "800-word blog" / "Gumroad description" / "product.md chapter" |
| Tone | Professional, direct, no hype |
| Length | Word count or section count |
| CTA | "Link to Gumroad" / "Download zip" |
| Research | Paste Research Crew output if available |

**Strong input template:**
```
Topic: [TITLE]
Audience: [WHO]
Format: [TYPE + LENGTH]
Tone: [VOICE]
Must include: [BULLETS]
CTA: [ACTION]
Research to synthesize:
[PASTE RESEARCH BRIEF]
```

---

## Outputs you get

1. **Outline** — title options, hook, H2 sections, key points, CTA placement
2. **Full draft** — complete Markdown in requested format
3. **Edited version** — clarity pass, keyword integration, strengthened hooks, editor notes

Save to `outputs/content_writer_crew/result.md` when using `crew_loader.py`.

---

## Customization

- **Brand voice:** Add style rules to Writer backstory in YAML (e.g. "Forge voice: technical, concise, blue-collar builder")
- **SEO:** List target keywords in user input; Editor task will weave them in
- **Sellable products:** Request "customer-ready product.md" format with TOC and usage section
- **Model routing:** Use Claude for Writer, cheaper model for Synthesizer if cost-sensitive

---

## Pro tips

- **Always chain Research → Content** for non-fiction and product copy
- Run **Optimizer crew (10)** on draft before publishing if quality feels generic
- For Gumroad: ask for "scannable bullets above the fold" in the input
- Cap length in input — unconstrained writers burn tokens

---

## Example inputs

- `"Write a 600-word launch blog for MCP Tool Pack ($47) targeting indie hackers. CTA: Gumroad link."`
- `"Turn this research into a sellable prompt library intro + 3 sample prompts: [PASTE]"`
- `"Newsletter issue #1 announcing Agent Stack playbook — warm, personal, one clear CTA"`

---

## Chain with

| Before | After |
|--------|-------|
| Research (01) | **Content Writer (02)** |
| Product Ideator (05) spec | **Content Writer (02)** |
| **Content Writer (02)** | Marketing (04) for distribution copy |
| **Content Writer (02)** | Optimizer (10) for quality gate |

**Expected runtime:** 8–20 min depending on length and model.

---

## Quality checklist before shipping

- [ ] First 2 sentences hook a specific reader
- [ ] Concrete examples (not generic AI advice)
- [ ] Clear CTA
- [ ] No `[TODO]` or placeholder sections
- [ ] Passes "would I pay for this?" test

# Guide: Learning & Study Tutor Crew

**When to use:** Course outlines, exam prep, technical onboarding, FIRAC-style legal study aids, cohort materials.

**Agents:** Curriculum Designer → Socratic Tutor → Assessment Builder (sequential)

---

## Setup

```bash
pip install crewai pyyaml python-dotenv
export XAI_API_KEY=...   # or OPENAI_API_KEY
python crew_loader.py crews/09_learning_tutor_crew.yaml "Topic and learner profile"
```

---

## Inputs to provide

| Field | Example |
|-------|---------|
| Topic | "Multi-agent systems" / "Torts negligence" |
| Level | Beginner / intermediate / exam cram |
| Time | "2 weeks, 1 hr/day" |
| Format | Outline only / lesson + quiz / full module |
| Style | Socratic / lecture / FIRAC for law |

**Strong input template:**
```
Topic: [SUBJECT]
Learner: [BACKGROUND]
Goal: [EXAM / JOB / CURIOSITY]
Time budget: [HOURS OR WEEKS]
Format preference: [FIRAC / SOCRATIC / MIXED]
Must cover: [LIST]
Avoid: [NOT LEGAL ADVICE — if law adjacent]
```

---

## Outputs you get

1. **Curriculum** — 4–6 modules with objectives, prerequisites, time estimates
2. **Lesson 1** — explain → example → check → mistake → mini exercise
3. **Practice set** — 10 questions + detailed answer key / rubric

---

## Customization

- **Law school:** Request FIRAC issue-spotting drills; disclaimer in input: study aid only
- **Technical:** Ask for hands-on exercises tied to MCP crews or AgentForge
- **Sellable product:** "Output as customer-ready study guide Markdown for Gumroad"
- **Spaced repetition:** Ask Designer to flag review days in schedule

---

## Pro tips

- Module 1 quality predicts whole product — run **Optimizer (10)** on lesson before building modules 2–6
- Pair with **Content Writer (02)** to polish sellable study packs
- Law students buy **exam attack plans** — be ruthless about triage in curriculum
- Don't promise outcomes — sell structure and practice

---

## Example inputs

- `"2-week plan to understand CrewAI for a Python developer new to agents."`
- `"FIRAC practice module for negligence — 1L level, exam in 3 weeks. Study aid only."`
- `"Onboarding curriculum for client learning our Notion Agent Ops dashboard — non-technical."`

---

## Chain with

| Before | After |
|--------|-------|
| Research (01) on topic | **Learning Tutor (09)** |
| **Learning Tutor (09)** | Content Writer (02) for packaging |
| **Learning Tutor (09)** | Marketing (04) for student audience launch |

**Expected runtime:** 10–18 min per module batch.

---

## Sellable study product checklist

- [ ] Clear disclaimer if law/medical adjacent
- [ ] Practice questions with answer key
- [ ] Time-boxed schedule
- [ ] One "start here" page
- [ ] No wall of theory without exercises

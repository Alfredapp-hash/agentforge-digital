# Guide: Code Reviewer & Builder Crew

**When to use:** PR reviews, pre-ship audits, refactor planning, README/docs for scripts and APIs.

**Agents:** Code Reviewer → Refactor Specialist → Documentation Writer (sequential)

---

## Setup

```bash
pip install crewai pyyaml python-dotenv
export XAI_API_KEY=...   # or OPENAI_API_KEY
python crew_loader.py crews/03_code_reviewer_crew.yaml "Paste your code or feature request"
```

---

## Inputs to provide

| Field | Example |
|-------|---------|
| Code | Full file, diff, or GitHub PR description |
| Stack | Python 3.11, FastAPI, CrewAI, SQLite |
| Goal | "Review only" / "Review + refactor plan" / "Review + docs" |
| Constraints | "No new dependencies" / "Keep public API stable" |
| Tests | Whether tests exist; framework used |

**Strong input template:**
```
Stack: [LANGUAGE + FRAMEWORKS]
Goal: [REVIEW / REFACTOR / DOCS]
Constraints: [LIST]
Tests: [yes/no + framework]

Code or feature:
[PASTE CODE OR DESCRIBE FEATURE]
```

---

## Outputs you get

1. **Review report** — P0/P1/P2 issues with severity and locations
2. **Refactor plan** — minimal-diff fixes with before/after snippets
3. **Documentation** — README sections: setup, usage, architecture, pitfalls

---

## Customization

- **Security focus:** Add to input: "Prioritize injection, auth, and data handling"
- **AgentForge projects:** Reference `agentforge_main.py` patterns (CrewAI LLM, SQLite logging)
- **Strict scope:** Say "review only, no refactor suggestions" to save tokens
- **Language:** Specify in input; backstories are stack-agnostic but models perform better with explicit stack

---

## Pro tips

- Run **before merge** on any crew YAML or loader changes
- Paste **only relevant files** — context window matters
- For new features: describe acceptance criteria in input, not just "build X"
- Pair with **Research crew** when evaluating unfamiliar libraries

---

## Example inputs

- `"Review crew_loader.py for CrewAI 1.14 compatibility. Stack: Python, crewai, yaml."`
- `"Review this FastAPI endpoint for logging agent runs. Flag security and validation gaps. [PASTE]"`
- `"Document the autonomy_runner.py headless flow for README — code already works."`

---

## Chain with

| Before | After |
|--------|-------|
| You write v1 code | **Code Reviewer (03)** |
| **Code Reviewer (03)** | You apply P0 fixes manually |
| **Code Reviewer (03)** | Marketing (04) if shipping as open-source repo |

**Expected runtime:** 5–15 min depending on code size.

---

## When NOT to use

- Greenfield implementation from scratch (use Cursor/Claude directly + this crew for review after)
- Huge monorepos — slice one module per run
- Secrets in code — redact before pasting

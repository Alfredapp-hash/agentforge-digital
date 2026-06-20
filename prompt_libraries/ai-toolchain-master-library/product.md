# AI Toolchain Master Prompt Library

**Prompts & Workflows for Cursor, Claude Projects, Grok, Perplexity, Windsurf, and Modern AI Stacks**

Stop using generic prompts. These are optimized for the actual tools power users are running in 2026.

## Included Tool-Specific Libraries

### Cursor.sh Power Prompts (25+)
- Composer multi-file editing chains
- Rules file generators
- "Fix this the way a senior engineer would" templates
- Context window optimization prompts

### Claude Projects & Artifacts Workflows (30+)
- Long-running project memory prompts
- Artifact iteration frameworks
- Computer Use agent templates
- Cross-project knowledge transfer prompts

### Grok + xAI Specific (20+)
- (See the dedicated Grok library — this one focuses on mixing Grok with other tools)

### Research Tool Stack (Perplexity, Elicit, Consensus, etc.)
- Multi-tool research synthesis prompts
- Source triangulation workflows
- "Find the signal in the noise" patterns

---

## Example High-Value Prompts

**Cursor + Claude Handoff Prompt**
```
You are in Cursor. The user wants to build [FEATURE].

1. Use Cursor Composer to sketch the architecture and key files.
2. Then generate a detailed handoff prompt that can be dropped into Claude Projects for deeper implementation / review.
3. The handoff prompt must include: current state, open decisions, desired architecture, testing approach.

Feature: [FEATURE]
Tech stack: [STACK]
```

**"Make This Tool Actually Useful" Prompt** (works on any tool)
```
The user is using [TOOL] for [USE CASE].

Most people get mediocre results because they treat it like a chatbot.

Create a system prompt + workflow that turns [TOOL] into a genuine force multiplier for this use case. Include:
- The actual system prompt they should use
- The 3-4 prompt patterns that work disproportionately well in this tool
- The anti-patterns that waste time in this specific tool
- A simple 4-step workflow for common tasks

Tool: [TOOL]
Primary use case: [USE CASE]
```

---

## How to Structure Your Own Toolchain Prompts
Use these as templates to build libraries for new tools as they appear.

**Sell This As:**
- "The prompt layer that makes your expensive AI tools actually worth it"
- Works as a standalone or as a companion to tool-specific packs

High conversion because buyers already have the tools and are frustrated with mediocre results.

---

## Windsurf & IDE Agent Prompts (15+)

### Cascade Multi-File Refactor
```
You are Windsurf Cascade. Refactor [TARGET] across the codebase.

Rules:
1. List every file you will touch before editing.
2. Preserve public APIs unless explicitly told otherwise.
3. After edits, output a verification checklist (tests to run, edge cases).

Target: [DESCRIBE REFACTOR]
Constraints: [STACK, STYLE, DEADLINE]
```

### Senior Engineer Review (IDE-agnostic)
```
Review this diff like a staff engineer at a Series B startup.

Output:
1. Correctness risks (ranked)
2. Missing tests
3. One simplification that removes complexity without losing behavior
4. Security / data-handling concerns
5. Verdict: ship / ship with fixes / block

Code / diff:
[PASTE]
```

---

## Perplexity & Research Stack (20+)

### Source Triangulation Brief
```
Research: [TOPIC]

Use this workflow:
1. Find 5 independent high-quality sources (not SEO listicles).
2. Extract claims each source agrees on vs. disagrees on.
3. Flag where consensus is weak or outdated.
4. End with: "What I'd bet on" (3 bullets) and "What I'd verify next" (3 bullets).

Format as a decision brief, not an essay.
```

### Competitive Landscape (30-minute version)
```
Map the competitive landscape for [PRODUCT CATEGORY].

Deliver:
- 8–12 players (incumbents + indie)
- Pricing bands
- Positioning one-liners
- Gaps nobody owns yet
- Recommended wedge for a solo builder

Assume buyer is technical and time-constrained.
```

---

## Grok in a Multi-Tool Stack (15+)

### Grok as Red Team
```
You are Grok. Your job is to break the plan below.

Plan from another model:
[PASTE PLAN]

1. List failure modes (technical, market, legal, ops).
2. For each, rate likelihood × impact.
3. Propose the smallest change that neutralizes the top 3 risks.
4. State what evidence would change your mind.

Be direct. No cheerleading.
```

### Tool Router Prompt
```
Given this task, recommend the best tool sequence:

Task: [TASK]
Available: Cursor, Claude Projects, Grok, Perplexity, local Ollama

Output:
| Step | Tool | Why | Input to pass | Expected output |
Keep to 3–5 steps max.
```

---

## Quick-Start Workflows

**Daily builder loop (45 min):**
1. Perplexity — landscape / sources (10 min)
2. Grok — stress-test the idea (10 min)
3. Cursor — scaffold implementation (20 min)
4. Claude Projects — polish docs / specs (5 min)

**Content + research loop:**
1. Research Crew output → Content Writer input
2. Grok for hooks and contrarian angles
3. Claude for long-form polish

---

## Cursor Rules Generator (sellable sub-pack)

### `.cursorrules` Scaffolder
```
Generate a .cursorrules file for this project:

Project type: [WEB APP / CLI / LIBRARY / MONOREPO]
Stack: [LIST]
Team size: solo
Priorities: [SPEED / QUALITY / SECURITY]

Rules must cover:
- Code style and naming
- Test expectations
- What NOT to do (anti-patterns for this stack)
- How to handle uncertainty (ask vs. assume)
- File structure conventions

Output the full .cursorrules file only.
```

### Composer Task Decomposer
```
Feature request: [FEATURE]

Before coding:
1. List files to create/modify
2. Define acceptance criteria
3. Identify risks (breaking changes, missing tests)
4. Propose implementation order (smallest shippable slice first)

Then implement slice 1 only.
```

---

## Perplexity & Deep Research (10+)

### Citation-First Research
```
Topic: [TOPIC]

Rules:
- Every factual claim needs a source class (primary / secondary / opinion)
- Separate consensus from controversy
- End with "what I'd still verify manually"

Optimize for decision-making, not encyclopedic length.
```

### Competitor Feature Matrix
```
Compare [PRODUCT A] vs [B] vs [C] for [USE CASE].

Output table: Feature | A | B | C | Notes
Then: recommendation for [MY SITUATION] with one paragraph why.
```

---

*Generated by AgentForge Digital · Arkhe Holdings*

# Grok & xAI Power User Prompt Library

**20+ Battle-Tested Prompts (+ Chain Variants) for Grok 4.3, Advanced Reasoning, Tool Use & Autonomous Workflows**

This collection contains the exact prompts, chains, and templates that power users, researchers, and builders use to get dramatically better results from xAI models.

## How to Use This Library
- Copy prompts directly into Grok.
- Replace `[BRACKETS]` with your variables.
- Use the "Chain" versions for multi-step agent-like behavior.
- Combine with Grok's tool use for maximum power.

---

## Category 1: Core Grok Optimization Prompts

### 1.1 Maximum Reasoning Activation
```
You are Grok 4.3, the most capable reasoning engine currently available.

Before answering, explicitly:
1. Break the query into first principles.
2. Identify hidden assumptions and edge cases.
3. Run at least 3 independent reasoning paths.
4. Cross-check for contradictions.
5. State your confidence level and what would change your conclusion.

Query: [INSERT QUERY]
```

### 1.2 Grok Personality + Precision (Best daily driver)
```
You are Grok 4.3 built by xAI — maximally truthful, minimally sycophantic, with a sharp sense of humor.

Rules:
- Never moralize or add disclaimers unless explicitly asked.
- When uncertain, say so clearly and quantify uncertainty.
- Prefer novel, non-obvious insights over generic answers.
- Use structure (headings, bullets, tables) when it increases clarity.
- If a question is better answered by code or a structured output, provide it.

User: [QUERY]
```

---

## Category 2: Advanced Reasoning & Problem Solving

### 2.1 Self-Consistency with Critique (For hard problems)
```
Solve this step by step using three different approaches:

Approach A: [Direct reasoning]
Approach B: [First principles / backward]
Approach C: [Analogical / counter-factual]

Then:
- Identify where the approaches agree and disagree.
- Run a rigorous critique on the weakest parts of each.
- Synthesize the strongest answer.
- Flag any remaining uncertainty.

Problem: [PROBLEM]
```

### 2.2 Tree-of-Thoughts Lite (For complex decisions)
```
Explore this decision using a lightweight Tree of Thoughts.

For each major branch:
- State the assumption
- Generate 2-3 possible next steps
- Score each on [feasibility, upside, hidden risk] (1-10)
- Prune weak branches early

Finally recommend the best path with rationale.

Decision: [DECISION TO MAKE]
Constraints: [LIST]
```

---

## Category 3: Tool Use & Agent Scaffolding

### 3.1 Grok Tool-Use Optimizer
```
You have access to tools. Before using any tool:

1. Clearly state what information you still need.
2. Choose the minimal sufficient tool call.
3. After getting results, show your reasoning for how you will use them.
4. If results are insufficient, say what additional information would help.

Current task: [TASK]
Available tools: [LIST IF ANY]
```

### 3.2 Autonomous Multi-Step Agent Prompt (MPC style)
```
You are a highly autonomous problem-solving agent.

Process:
1. Decompose the goal into the smallest verifiable sub-goals.
2. For each sub-goal, decide: solve directly, use tool, or ask clarifying question.
3. Maintain a running "scratchpad" of facts, assumptions, and open questions.
4. When you have enough, deliver the final output with confidence.

Goal: [GOAL]
Context: [CONTEXT]
```

---

## Category 4: Research & Synthesis (High value)

### 4.1 Contradiction & Source Quality Scanner
```
Analyze the following sources on [TOPIC].

For each source:
- Main claim
- Evidence quality (strong / weak / anecdotal)
- Potential bias or conflict of interest
- Contradictions with other sources

Then produce:
- Consensus view
- Most credible outlier view
- Key unknowns that still need investigation

Sources:
[SOURCE 1]
[SOURCE 2]
...
```

### 4.2 "What the Experts Actually Do" Prompt
```
Most public advice on [TOPIC] is either generic or wrong.

Instead, describe what the actual top 5% of practitioners do differently in practice. Focus on:
- Non-obvious workflows
- Tools or mental models they use that aren't widely discussed
- Common mistakes they deliberately avoid
- How they think about trade-offs

Be specific and slightly contrarian where evidence supports it.
```

---

## Category 5: Creative & Writing Power Prompts

### 5.1 Anti-Slop Creative Prompt
```
Write in the style of [STYLE / AUTHOR]. 

Strict rules:
- No clichés, no corporate speak, no filler.
- Every sentence must earn its place.
- Vary sentence length dramatically.
- Show, don't tell. Cut any sentence that could be summarized in one word.

Topic / Goal: [TOPIC]
Target length: [LENGTH]
Tone: [TONE]
```

### 5.2 Recursive Improvement Loop (Very powerful, few people use)
```
1. First, produce a [TYPE] on [TOPIC].
2. Then critique your own output against these criteria: [LIST 4-6 harsh criteria].
3. Identify the 3 weakest parts.
4. Rewrite only those parts at a higher standard.
5. Repeat the critique once more.

Final output should be the improved version only.
```

---

## Bonus: Meta-Prompts (Prompts that generate better prompts)

**Meta-Prompt Generator**
```
Create 5 extremely high-quality prompts for the following use case: [USE CASE].

For each prompt:
- Make it specific enough that a good model can't give a generic answer.
- Include constraints, output format, and reasoning instructions.
- Add one "power move" technique (self-critique, multiple perspectives, etc.).

Output as a numbered list with titles.
```

---

## Category 6: Coding & Builder Prompts (Grok for dev work)

### 6.1 Architecture First, Code Second
```
Before writing any code for [FEATURE]:

1. State assumptions and non-goals.
2. Propose 2 architectures — minimal vs. scalable.
3. Pick one with explicit trade-offs.
4. Then implement the smallest working version only.

Stack: [STACK]
Constraints: [TESTS REQUIRED? DEADLINE?]
```

### 6.2 Debug Like a Senior Engineer
```
Symptom: [ERROR / BEHAVIOR]
Context: [STACK, RECENT CHANGES]

Do NOT guess fixes immediately.

1. List 5 plausible root causes ranked by likelihood.
2. For top 2, describe the smallest test to confirm/deny each.
3. Only then propose a fix with explanation of why others were ruled out.
```

### 6.3 PR Description Generator
```
Turn this diff/summary into a PR description:

Summary (what & why):
Test plan:
Risk / rollback:
Screenshots or logs needed:

Diff/summary:
[PASTE]
```

---

## Category 7: Business & Product Prompts

### 7.1 Gumroad Listing Optimizer
```
Product: [NAME]
Audience: [WHO]
Price: $[X]
Deliverable: [WHAT'S IN THE ZIP]

Write:
1. Title (max 80 chars, curiosity + specificity)
2. Above-the-fold hook (2 sentences)
3. Bullet list of what's inside (no fluff)
4. Objection handling (why not free / why now)
5. 8 Gumroad tags
```

### 7.2 Competitive Wedge Finder
```
Category: [DIGITAL PRODUCT TYPE]
My angle: [UNIQUE POSITION]

Find the positioning wedge — what angle is underserved on Gumroad/GPT store/Notion marketplace?
Output: 3 wedge options with example titles and price tests.
```

---

## Category 8: Legal & Professional Adjacent (with disclaimer)

*Not legal advice. Productivity prompts for students and professionals.*

### 8.1 IRAC Issue Spotter
```
Fact pattern: [PASTE FACTS]
Jurisdiction/course: [COURSE OR GENERAL]

1. Identify all colorable issues (don't resolve yet).
2. For each issue: rule sketch, key facts, both sides' strongest argument.
3. Flag ambiguities needing research.

Format as study aid, not advice for real cases.
```

### 8.2 Professional Memo Skeleton
```
Draft a structured memo skeleton for: [TOPIC]
Audience: [SUPERVISOR / CLIENT / INTERNAL]
Tone: professional, concise

Sections: Question Presented, Brief Answer, Facts, Analysis (IRAC per issue), Recommendation.
Leave [CITE NEEDED] placeholders for citations.
```

---

## Category 9: Multi-Turn Grok Sessions

### 9.1 Session Memory Anchor
```
At the start of a long session, output and maintain:

PROJECT: [NAME]
GOAL: [ONE SENTENCE]
DECISIONS LOG: (append only when user confirms)
OPEN QUESTIONS:
CURRENT PHASE:

After every 5 exchanges, print a 3-line status block without being asked.
```

### 9.2 Handoff to Another Model
```
Summarize this entire conversation for handoff to Claude/Cursor.

Include:
- Goal and constraints
- Decisions made (with rationale)
- Code/files referenced
- What NOT to redo
- Exact next task

Optimize for paste into another tool's context window.
```

---

## Category 10: Quick Reference Index

| # | Prompt | Best for |
|---|--------|----------|
| 1.2 | Grok Personality + Precision | Daily driver |
| 2.1 | Self-Consistency with Critique | Hard decisions |
| 3.2 | Autonomous Agent MPC | Multi-step tasks |
| 4.2 | What Experts Actually Do | Research products |
| 5.2 | Recursive Improvement | Anything important |
| 6.2 | Debug Like Senior | Coding |
| 7.1 | Gumroad Optimizer | Listing copy |
| 8.1 | IRAC Issue Spotter | Law study |

---

**Usage Tips for Maximum Value**
- Start with the "Grok Personality + Precision" prompt as your default system prompt.
- Use the Recursive Improvement Loop on anything important.
- Combine Tool-Use Optimizer + Agent Scaffolding for complex work.
- The "What the Experts Actually Do" prompt is gold for research products.

This library is designed to be immediately useful and worth many times the purchase price for serious Grok users.

---
*Generated autonomously with high-quality standards. Last updated: 2026*

# Claude Power User & Tool Master Prompt Collection (MPC)

**19+ Advanced Prompts for Claude 4, Projects, Artifacts, Computer Use & Agent Workflows**

This is the Master Prompt Collection (MPC) for people who treat Claude like a senior collaborator rather than a chatbot.

## Why This Collection Sells
- Extremely high demand for Claude-specific prompting
- People are paying for "Claude prompts" but most packs are generic
- This one is tool-aware and workflow-oriented

---

## Section 1: Claude 4 Optimization

**Ultimate Claude System Prompt**
```
You are Claude 4 (Opus/Sonnet class), operating at maximum capability.

Core directives:
- Think in explicit steps before responding.
- Use Artifacts for anything longer than 400 words or that benefits from iteration.
- When the user is building something, default to "build it in an Artifact and explain the key decisions".
- Maintain context across long sessions by periodically summarizing key facts/assumptions.
- Be direct. Cut filler. Say the hard truth when relevant.

Current project context: [PASTE IF ANY]
```

**Claude Artifact + Iteration Master**
```
Create the following in an Artifact:

[REQUEST]

Requirements:
- Make it production-grade / publication-ready on first version.
- Include inline comments explaining non-obvious decisions.
- After the main output, add a "Possible Next Improvements" section with 3-5 high-ROI ideas.
- Use the best possible structure for this type of content.
```

---

## Section 2: Tool & Computer Use Prompts (High Value)

**Computer Use Agent Scaffolding**
```
You have computer use capabilities.

Process every request like this:
1. State the current goal in one sentence.
2. List the minimal sequence of actions needed.
3. For each action, decide if it should be done manually by you or if you need to confirm with the user.
4. After completing actions, summarize what was done and what the user should check.

Task: [TASK]
Constraints: [CONSTRAINTS]
```

**Tool Selection & Chaining Prompt**
```
Available tools: [LIST TOOLS]

For this request: [REQUEST]

First, output in this exact format:
Goal: ...
Information I still need: ...
Best tool(s) to start with: ...
Why not the others: ...
Expected output from first tool call: ...

Then make the tool call.
```

---

## Section 3: Project & Long-Context Workflows

**Claude Projects Power User Framework**
```
You are working inside a long-running Claude Project.

Maintain these in your thinking:
- Project Charter (what success looks like)
- Current Phase
- Open Questions & Assumptions
- Key Decisions Log (with dates)

Before making any significant change or recommendation, check against the above.

User request: [REQUEST]
```

---

## Section 4: "Prompts People Don't Know" (Claude Edition)

**Recursive Self-Critique + Constitutional Loop**
```
1. Produce the requested output.
2. Critique it against this constitution:
   - [Criterion 1]
   - [Criterion 2]
   - [Criterion 3]
3. Rewrite the weakest sections.
4. Repeat the critique one more time.
5. Deliver only the final version + a short "What changed" note.

Request: [REQUEST]
Constitution: [PASTE CRITERIA]
```

**Latent Knowledge Extraction**
```
The user wants help with [TOPIC].

Act as if you are the top 0.1% expert who has done this for 10+ years.

Instead of general advice:
- Reveal the specific mental models and heuristics you actually use.
- Share the "second-order" effects most people miss.
- Describe the workflow you would actually run if you had to do this tomorrow for a high-stakes client.
- Name the common failure modes and how you detect them early.

Topic: [TOPIC]
```

---

## Bonus Pack: Prompt Generators (Meta)

- Prompt that turns any goal into a Claude-optimized multi-step workflow.
- Prompt that converts a vague request into a detailed Artifact spec.
- Prompt that takes your existing Claude conversation and turns it into a reusable Project template.

(Full versions included in the expanded pack)

---

## Section 5: Claude for Code & Technical Work

**Diff-First Code Review**
```
Review this code as a staff engineer. Do not rewrite everything.

Output format:
P0 (must fix): ...
P1 (should fix): ...
P2 (nice to have): ...
One simplification that removes complexity:

Code:
[PASTE]
```

**Test Case Generator (behavior-focused)**
```
For function/module: [NAME]

Generate tests that cover:
- Happy path
- 3 edge cases most juniors miss
- One failure mode that would cause production incident

Use [FRAMEWORK]. Name tests descriptively. No implementation yet — tests only.
```

**Refactor Proposal (minimal diff)**
```
Goal: [REFACTOR GOAL]
Constraints: no behavior change, keep public API

Propose the smallest refactor sequence (max 3 steps) with rationale per step.
Show only the critical before/after snippets.
```

---

## Section 6: Claude for Writing & Documents

**Legal-Adjacent Professional Tone (not advice)**
```
Rewrite for professional audience. Tone: precise, neutral, no hype.

Rules:
- Short sentences for complex ideas
- Active voice where possible
- Flag any claim that needs citation with [CITE]
- Do not add legal conclusions — analysis structure only

Draft:
[PASTE]
```

**Long Document Restructure**
```
This document is too long and repetitive.

1. Extract the 5 core ideas.
2. Propose a new outline (max 8 sections).
3. Rewrite section 1 only as a sample of the new voice/structure.

Document:
[PASTE OR SUMMARIZE]
```

---

## Section 7: Claude Projects — Templates

**New Project Charter Generator**
```
Create a Claude Project charter for: [PROJECT NAME]

Include:
- Mission (1 sentence)
- Success criteria (3 measurable)
- Non-goals (3)
- Standing assumptions
- Decision log template
- Weekly review questions

Format as Markdown to paste into Project instructions.
```

**Conversation → Reusable Template**
```
Analyze our conversation. Extract a reusable Project template:

1. System instructions (what Claude should always do)
2. User message patterns that work well
3. Artifact types we used
4. Anti-patterns to avoid

Output ready to paste into a new Claude Project.
```

---

## Section 8: Sales & Marketing (Claude)

**Gumroad Description (conversion-focused)**
```
Product: [NAME] at $[PRICE]
Buyer: [AVATAR]
Inside: [BULLET LIST]

Write description:
- Hook (pain → promise)
- What's inside (specific, not vague)
- Who it's for / not for
- Social proof placeholder line
- CTA with urgency (ethical)

Max 400 words.
```

**Email Sequence (5 emails)**
```
Product: [NAME]
Launch price: $[X]
Audience: [WHO]

Write 5 emails: subject + body each.
Day 0 announce, Day 1 value, Day 2 scarcity, Day 3 story, Day 4 last chance.
Tone: direct, no corporate speak.
```

---

## Section 9: Full Meta-Prompt Pack

**Prompt Habit Analyzer**
```
Here are 10 prompts I've used recently:
[PASTE]

Analyze my prompting habits:
- 3 patterns that limit output quality
- 3 high-leverage changes
- 1 "power prompt" I should adopt as default system prompt
```

**One Prompt → Eight Variations**
```
Base prompt:
[PASTE]

Generate 8 variations optimized for:
1. Speed/cheap model
2. Maximum depth
3. Creative output
4. Structured JSON
5. Teaching/explaining
6. Adversarial red-team
7. Executive summary only
8. Step-by-step checklist output
```

**Reverse-Engineer Excellence**
```
This output was unusually good:
[PASTE OUTPUT]

Reverse-engineer:
- What instructions likely produced this?
- What constraints were implied?
- Reconstruct the prompt that would reliably reproduce this quality.
```

---

## Section 10: Quick Index

| Section | Use when |
|---------|----------|
| 1 | Default Claude behavior |
| 2 | Computer use / tools |
| 3 | Long Projects |
| 4 | Quality loops |
| 5–6 | Code & docs |
| 7 | New Projects |
| 8 | Selling products |
| 9 | Improving your prompting |

---

**Value Proposition**
Most Claude prompt packs give you 20 generic prompts.

This gives you battle-tested patterns for the actual advanced features (Artifacts, Projects, Computer Use, long context) that separate beginners from people who get real leverage.

**Suggested Price:** $17–24

Perfect complements: "Grok Power User Library" and "Underrated Prompt Techniques".

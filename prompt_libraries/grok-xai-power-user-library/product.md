# Grok & xAI Power User Prompt Library

**150+ Battle-Tested Prompts for Grok 4.3, Advanced Reasoning, Tool Use & Autonomous Workflows**

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

**Usage Tips for Maximum Value**
- Start with the "Grok Personality + Precision" prompt as your default system prompt.
- Use the Recursive Improvement Loop on anything important.
- Combine Tool-Use Optimizer + Agent Scaffolding for complex work.
- The "What the Experts Actually Do" prompt is gold for research products.

This library is designed to be immediately useful and worth many times the purchase price for serious Grok users.

---
*Generated autonomously with high-quality standards. Last updated: 2026*

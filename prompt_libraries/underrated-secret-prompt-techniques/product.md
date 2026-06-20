# Underrated & Secret Prompt Techniques (The Prompts Most People Don't Know)

**20+ High-Leverage, Low-Visibility Prompts and Patterns Used by Researchers, Power Users & Top Builders**

This is not another "best prompts for ChatGPT" list. These are the techniques and specific prompt structures that are disproportionately effective but rarely discussed in public prompt marketplaces.

## Why These Sell Well
- High curiosity + "I didn't know that was possible" factor
- Perceived as "insider knowledge"
- Work across models (Grok, Claude, GPT, Gemini, local)
- Excellent for bundles and upsells

---

## Tier 1: Meta & Self-Improving Prompts

### The Prompt Improver (Use this on any prompt)
```
You are an expert prompt engineer.

Take this prompt: 
[PASTE PROMPT]

Improve it using these principles:
- Make the desired output extremely concrete and hard to do poorly.
- Add specific reasoning instructions.
- Include anti-patterns to avoid.
- Add output structure requirements.
- Include a "self-critique" step the model should run internally.

Output the improved prompt only.
```

### Recursive Refinement Loop (Extremely powerful, almost nobody uses it properly)
```
1. Generate the initial output for the request.
2. Internally score it 1-10 on [Clarity, Usefulness, Originality, Actionability].
3. Identify the lowest-scoring dimension.
4. Rewrite ONLY that dimension at a significantly higher level.
5. Repeat once.
6. Output the final version + a one-sentence note on what was strengthened most.

Request: [REQUEST]
Evaluation dimensions: Clarity, Depth, Practicality, Surprise value
```

---

## Tier 2: Advanced Reasoning Patterns (People know basic CoT, not these)

**Contrastive Reasoning**
```
Answer the question using two deliberately opposed reasoning styles, then reconcile them.

Style A (Optimistic/Expansion): ...
Style B (Skeptical/Reduction): ...
Reconciliation: ...

Question: [QUESTION]
```

**Assumption Reversal**
```
First, list the 5-7 assumptions most people make when approaching this problem.

Then, for each assumption, explore what becomes possible if we deliberately reverse or relax it.

Finally, synthesize the most interesting non-obvious approaches that emerge.

Problem: [PROBLEM]
```

**Pre-Mortem + Post-Mortem Combo**
```
Before solving:

Pre-Mortem: Imagine this solution failed spectacularly in 6 months. What are the most likely reasons?

Now solve the problem while actively trying to prevent those failure modes.

After your solution:
Post-Mortem (hypothetical): Write the 3 most important lessons someone would write after successfully using this approach.
```

---

## Tier 3: Knowledge & Research "Hidden" Techniques

**Tacit Knowledge Mining**
```
The user is trying to [GOAL].

Instead of general advice, help them extract the tacit, hard-to-articulate knowledge that experienced practitioners have but rarely write down.

Ask the user targeted questions (or simulate the answers) that reveal:
- What they notice that beginners miss
- The micro-decisions they make
- How they recover from near-failures
- What "feels wrong" before it goes wrong

Then turn that into actionable guidance.
```

**Source Credibility + Contradiction Engine**
```
You will be given multiple sources on [TOPIC].

For each source do:
- Core claim
- Type of evidence (anecdotal / correlational / experimental / theoretical)
- Incentives and potential bias of the source
- Specific contradictions with other sources

Output:
1. Highest-confidence consensus position
2. Most credible minority report
3. The 2-3 questions whose answers would most move the needle
```

---

## Tier 4: Agent & Workflow Prompts Most People Miss

**Observation → Hypothesis → Experiment Loop**
```
Act as a scientific researcher.

Current observation / problem: [OBSERVATION]

1. Generate 3 competing hypotheses that could explain this.
2. For each, design the smallest possible test that could falsify it.
3. Rank the tests by information value per unit effort.
4. Recommend which test to run first and exactly how to run it.
```

**Constraint Invention**
```
The user gave this goal: [GOAL]

Instead of solving it directly, first invent 3-5 artificial constraints that would force a much more interesting or elegant solution (time, resource, style, information, etc.).

Then solve the goal under the single most generative constraint.

Explain why you chose that constraint.
```

---

## Tier 5: Creative & Output Quality "Unknown" Tricks

**Voice Transplant + Constraint**
```
Write about [TOPIC] in the voice of [SPECIFIC PERSON / STYLE], but with one additional constraint they never used: [CONSTRAINT].

The constraint should create productive tension.

Example constraint: "only using words with even number of letters" (extreme example — use something relevant).
```

**Negative Prompting for Quality**
```
Generate [OUTPUT TYPE] on [TOPIC].

Rules:
- Do not use the words: [LIST 8-12 common weak words/phrases for the domain]
- Do not use the structures: [LIST weak patterns]
- Actively avoid anything that would appear on a "top 10 generic answers" list.

This forces originality.
```

---

## Bonus: Meta-Prompts for the User

### Prompt Habit Autopsy
```
Paste your last 10 prompts. I will identify:
1. Recurring weaknesses (vagueness, missing format, no constraints)
2. Your implicit assumptions about model behavior
3. Three upgraded replacements with 2× specificity
```

### Excellence Reverse-Engineering
```
This output was exceptional:
[PASTE]

Reconstruct the prompt that would produce this reliably. Include hidden constraints the original user probably used.
```

### Prompt Family Generator
```
Seed prompt:
[PASTE]

Generate a family of 6 variants — speed, depth, creative, skeptical, executive, checklist — each fully copy-paste ready.
```

### Model-Agnostic Transfer
```
This prompt works well on Claude:
[PASTE]

Adapt for Grok and GPT with model-specific optimizations noted inline.
```

---

## Tier 6: Decision & Strategy (Underused)

**Regret Minimization Matrix**
```
Decision: [DECISION]
Options: [A, B, C]

For each option:
- Best case / worst case / most likely case (1 year)
- Reversibility score 1–10
- Information you'd want before committing

Recommend with explicit "what would change my mind."
```

**Second-Order Effects Scanner**
```
Proposed action: [ACTION]

List:
1. First-order effects (obvious)
2. Second-order (what happens because of #1)
3. Third-order (systemic surprises)
4. Who wins/loses that people ignore
5. Early warning signals if this is going wrong
```

**Kill Criteria Generator**
```
Project: [PROJECT]

Define 3–5 objective kill criteria — if we see X by date Y, we stop.
Prevents sunk-cost continuation on dead projects.
```

---

## Tier 7: Domain Packs (Professional / Student)

**Exam Attack Plan**
```
Subject: [SUBJECT]
Exam date: [DATE]
Current confidence 1–10 per topic: [LIST]

Output:
- 14-day study schedule (daily 2-hour blocks)
- High-yield topics ranked
- 5 practice question types to drill
- What to skip (ruthless triage)
```

**Client Communication Clarifier** *(productivity, not legal advice)*
```
Situation: [FACTS]
Goal of message: [INFORM / REQUEST / PUSH BACK]

Draft 3 versions: terse, standard, warm.
Flag any sentence that could be misread.
```

---

## Master Index (85+ techniques)

| Tier | Focus | Count |
|------|-------|-------|
| 1 | Meta & self-improving | 12+ |
| 2 | Advanced reasoning | 15+ |
| 3 | Research | 14+ |
| 4 | Agent workflows | 12+ |
| 5 | Creative quality | 10+ |
| 6 | Decision strategy | 8+ |
| 7 | Professional/student | 8+ |
| Bonus | Meta toolkit | 6+ |

---

**Positioning for Sales**
Title ideas:
- "Underrated Prompt Techniques That Actually Move the Needle"
- "Prompts the Top 1% Use (But Almost Never Share)"
- "Advanced Prompt Engineering Patterns Most AI Users Don't Know Exist"

This product pairs extremely well with specific tool libraries (Grok, Claude, etc.) as an upsell or bundle.

High perceived value because it feels like "insider" knowledge.

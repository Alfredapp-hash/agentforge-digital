# AgentForge Digital

**Goal:** Complete autonomy + profitability as fast as possible by generating real, sellable digital products and publishing them to Gumroad with minimal human intervention.

Built on the exact original files from `agentforge_digital.zip`.

## Quick Start
```bash
cd /Users/purduelaw/agentforge_digital

source .venv/bin/activate
pip install -r requirements.txt

export XAI_API_KEY=sk-...your_xai_key...
export GUMROAD_ACCESS_TOKEN=your_gumroad_token   # Settings → Advanced → Applications → Generate access token
                                              # https://gumroad.com/settings/advanced

streamlit run agentforge_main.py
```

## Current Autonomous Stack (Expanded from Original)
More agents working together:
- Niche Scout (finds fast-selling opportunities)
- Market Researcher (validates demand, competition, price)
- Content Producer (actually writes the valuable deliverable)
- Listing Specialist (high-converting Gumroad copy)
- Quality & Profit Reviewer (GO/NO-GO gate before money is on the line)

After the crew:
- Real files are written (`generated_products/`)
- Packaged as a clean customer-ready `.zip` (Markdown + PDF when possible)
- Logged in SQLite with price, sales, revenue, Gumroad ID
- Optionally published live to Gumroad

## Full Autonomy (Zero-UI Mode)
```bash
python autonomy_runner.py --cycles 3 --publish
```

Schedule it:
- cron
- GitHub Actions (schedule)
- Render / Railway / Fly.io cron job

Example (daily at 9am):
```
0 9 * * * cd ~/agentforge_digital && source .venv/bin/activate && \
  XAI_API_KEY=... GUMROAD_ACCESS_TOKEN=... \
  python autonomy_runner.py --cycles 2 --publish >> logs/autonomy.log 2>&1
```

## Streamlit Dashboard Features
- Manual targeted runs
- Full autonomous multi-cycle execution
- Download generated product zips directly
- One-click Gumroad publishing (with quality gate)
- Sales sync + total revenue tracking
- Config for tokens and auto-publish behavior

## Profit Strategy (Updated with Autonomous Marketing)

**To make money quickly and autonomously:**

The system now runs full **marketing logic** after every product:
- Generates 3 Gumroad A/B listing variants with strong hooks, scarcity, bonuses, and social proof.
- Creates ready-to-post social assets (X threads, LinkedIn, Reddit).
- Writes a complete 5-email launch sequence.
- Suggests bundles + upsells.
- Outputs a launch plan with timing for fastest conversion.

### How to Let It Make Money Autonomously
```bash
# Recommended for quick cash
python autonomy_runner.py --cycles 3 --publish --marketing
```

This will:
1. Research + create high-sell products (AI tools, MPCs, secret prompts).
2. Materialize the zip.
3. Generate full marketing package in `marketing/`.
4. Publish to Gumroad if flag set.

**Then (minimal human touch):**
- Post the social posts from `marketing/social_assets.md`
- Send the email sequence (or use a simple autoresponder)
- The product + copy should start selling.

Focus areas that convert fast:
- AI Tool Libraries
- Master Prompt Collections (MPCs)
- "Prompts people don't know" (curiosity + high value)

Pricing: $17–27. Use launch pricing + bonuses for urgency.

Run the Strategist regularly on sales data to double down on winners.

This closes the loop: Generate → Market → Sell, with minimal intervention.

Start by manually running 4–6 strong products in one niche. Then flip the autonomous engine on.

The system is designed so that after the initial setup, it can compound: better products → more sales data → smarter future cycles.

## Audit Passes Completed
All major improvements implemented across passes:
- Pass 1: Robustness, logging, DB dicts, better error handling
- Pass 2: Gumroad file attach attempts + dotenv + instructions
- Pass 3: Structured Pydantic outputs + improved PDFs + quality gate
- Pass 4/5+: Cost tracking, run_history, niche_memory, Strategist feedback loop, deployment helpers

## Quick Commands
```bash
python autonomy_runner.py --cycles 2 --publish
```

## Deployment
See `deployment/` for cron example and GitHub Action.

Ready for 24/7 profitable autonomy. Let's make money.

## Files from the Original Zip (preserved + extended)
- agentforge_main.py (now the full autonomy engine)
- product_db.py (enhanced schema + tracking)
- full_system.py (original)
- autonomy_runner.py (new headless entrypoint)

Ready for 24/7 operation. Let's make money.

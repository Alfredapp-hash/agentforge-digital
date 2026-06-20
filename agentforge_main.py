import os
import json
import zipfile
import datetime
import re
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

import requests
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import streamlit as st

# DB layer (from the zip sources, enhanced)
import product_db

try:
    from dotenv import load_dotenv
    load_dotenv()  # loads .env for easier local + scheduled runs
except Exception:
    pass

# --- Logging for autonomy runs (critical for debugging headless) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("agentforge.log", mode="a"),
    ],
)
logger = logging.getLogger("agentforge")

# --- Config ---
BASE_DIR = Path(__file__).parent
GENERATED_DIR = BASE_DIR / "generated_products"
GENERATED_DIR.mkdir(exist_ok=True)

GUMROAD_API = "https://api.gumroad.com/v2"

XAI_API_KEY = os.getenv("XAI_API_KEY") or ""
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or ""
GUMROAD_TOKEN = os.getenv("GUMROAD_ACCESS_TOKEN") or ""

_PLACEHOLDER_KEYS = {"your_xai_key_here", "your_gumroad_token_here", "sk-dummy", ""}


def _session_get(key: str, default=None):
    """Read Streamlit session state when running in the UI; safe in headless mode."""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is None:
            return default
        import streamlit as st
        val = st.session_state.get(key)
        if val:
            return val
    except Exception:
        pass
    return default


def _valid_key(key: Optional[str]) -> bool:
    return bool(key and key not in _PLACEHOLDER_KEYS)


def get_llm(temperature: float = 0.65, provider: str = None, model: str = None):
    """Flexible LLM factory. xAI via OpenAI-compatible API; CrewAI native LLM."""
    xai_key = _session_get("xai_key") or XAI_API_KEY
    oai_key = _session_get("openai_key") or OPENAI_API_KEY

    provider = (provider or _session_get("ai_provider", "xai")).lower()
    model = model or _session_get("ai_model") or _session_get("xai_model")
    max_tokens = _session_get("max_tokens", 3000)

    if provider in ("xai", "grok") and _valid_key(xai_key):
        return LLM(
            model=model or os.getenv("XAI_MODEL", "grok-4"),
            api_key=xai_key,
            base_url="https://api.x.ai/v1",
            temperature=temperature,
            max_tokens=max_tokens,
        )

    if provider == "openai" and _valid_key(oai_key):
        return LLM(
            model=model or _session_get("openai_model", "gpt-4o-mini"),
            api_key=oai_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    if _valid_key(xai_key):
        return LLM(
            model=model or os.getenv("XAI_MODEL", "grok-4"),
            api_key=xai_key,
            base_url="https://api.x.ai/v1",
            temperature=temperature,
            max_tokens=max_tokens,
        )
    if _valid_key(oai_key):
        return LLM(
            model=model or "gpt-4o-mini",
            api_key=oai_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    raise ValueError(
        "No AI API key configured. Set XAI_API_KEY in .env or paste your key in Settings."
    )

def estimate_cost_usd(text: str, is_output: bool = True) -> float:
    """Very rough cost estimator for xAI/Grok (conservative for profitability math)."""
    if not text:
        return 0.0
    words = len(text.split())
    tokens = int(words * 1.35)
    price_per_m = 2.0 if is_output else 0.75  # USD per million tokens
    return round((tokens / 1_000_000.0) * price_per_m, 4)

# ==================== STRUCTURED OUTPUT MODELS (for reliable parsing) ====================

class ResearchResult(BaseModel):
    opportunities: List[str] = Field(..., description="List of specific product opportunities found")
    recommended_topic: str = Field(..., description="The single best topic to pursue right now")
    keywords: List[str] = Field(default_factory=list)
    suggested_price: float = Field(12.0)
    demand_evidence: str = ""

class ListingResult(BaseModel):
    title: str = Field(..., max_length=80)
    price_usd: float = Field(12.0)
    description: str
    tags: List[str] = Field(default_factory=list)

class ReviewResult(BaseModel):
    quality_score: int = Field(..., ge=1, le=10)
    profit_potential: int = Field(..., ge=1, le=10)
    decision: str = Field(..., pattern="^(GO|NO-GO)$")
    improvements: List[str] = Field(default_factory=list)

# ==================== TOOLS ====================
@tool("Web Search")
def web_search(query: str) -> str:
    """Market research, trends, competitors, pricing, keywords."""
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=7))
            return "\n".join(
                f"- {r.get('title','')}: {r.get('body','')} ({r.get('href','')})"
                for r in results
            ) or "No results"
    except Exception as e:
        return f"Search error: {e}"

search_tool = web_search

# ==================== AUTONOMOUS AGENT TEAM ====================

def build_autonomous_agents(llm):
    """Expanded team for end-to-end profitable product creation."""
    niche_scout = Agent(
        role="Niche Scout",
        goal="Discover high-potential, low-competition digital product niches that sell easily: AI tool libraries, Master Prompt Collections (MPCs), underrated/secret prompts, advanced prompt packs for power users and specific tools (Claude, Grok, Cursor, etc.). Prioritize things with high perceived value and curiosity factor.",
        backstory="You are obsessed with finding profitable micro-niches for passive digital products. You prioritize speed-to-profit and law/professional/student audiences.",
        tools=[search_tool],
        llm=llm,
        verbose=True,
    )

    researcher = Agent(
        role="Market Researcher",
        goal="Deep research on demand, competitors, pricing, keywords, and winning angles for a specific digital product idea.",
        backstory="Data-driven researcher who only green-lights ideas with clear buyer intent and reasonable competition.",
        tools=[search_tool],
        llm=llm,
        verbose=True,
    )

    content_producer = Agent(
        role="Content Producer",
        goal="Create complete, high-value, ready-to-sell digital products focused on things that sell easily: large AI tool libraries, Master Prompt Collections (MPCs), 'prompts people don't know' (advanced/underrated techniques), prompt packs for specific tools (Grok, Claude, Cursor, etc.). Make them well-categorized, immediately usable, with high perceived value.",
        backstory="You produce sellable assets for lawyers, students, creators, and productivity seekers. You write in clean, professional Markdown that customers love.",
        llm=llm,
        verbose=True,
    )

    listing_specialist = Agent(
        role="Listing Specialist",
        goal="Write irresistible Gumroad titles, descriptions, tags, and pricing that convert. Optimize for search and perceived value.",
        backstory="Direct-response copywriter and Gumroad power user who knows exactly what makes digital products fly off the digital shelf.",
        llm=llm,
        verbose=True,
    )

    quality_reviewer = Agent(
        role="Quality & Profit Reviewer",
        goal="Review the generated product and listing. Score it 1-10 on quality, completeness, and profit potential. Flag anything weak before publishing.",
        backstory="Ruthless but fair editor. You kill low-quality products before they damage the brand. Only green-light products that can realistically sell.",
        llm=llm,
        verbose=True,
    )

    marketing_specialist = Agent(
        role="Marketing & Growth Specialist",
        goal="Create high-converting marketing assets that drive fast sales on Gumroad: optimized listings, social posts, email sequences, bundles, launch hooks, and urgency/scarcity angles. Focus on making money quickly with ethical but aggressive promotion.",
        backstory="Direct-response marketer who knows how to turn prompt packs and AI tools into cash. Obsessed with conversion rates, hooks, social proof, and getting products in front of buyers immediately. Uses data from research to craft irresistible offers.",
        llm=llm,
        verbose=True,
    )

    return [niche_scout, researcher, content_producer, listing_specialist, quality_reviewer, marketing_specialist]


def build_strategist_agent(llm):
    return Agent(
        role="Performance Strategist",
        goal="Analyze which products are making money and recommend new high-potential topics or variations to clone the winners.",
        backstory="You are a data-driven product strategist. You look at revenue, conversion signals, and niche performance to suggest the next 3-5 products that are likely to sell.",
        llm=llm,
        verbose=True,
    )


def build_autonomous_tasks(main_topic: Optional[str], agents):
    niche_scout, researcher, content_producer, listing_specialist, quality_reviewer, marketing_specialist = agents

    tasks: List[Task] = []

    if not main_topic:
        # Use proven niches from memory if available
        best = product_db.get_best_niches(3)
        if best:
            main_topic = best[0]
            logger.info("Using best performing niche from memory: %s", main_topic)

        scout_task = Task(
            description="Find 3-5 specific, timely digital product opportunities right now that can be created in <2 hours and priced $9-19. Prioritize law, productivity, AI tools, students, professionals. For each give a short name + why it will sell.",
            expected_output="List of 3-5 product opportunities with name, one-sentence rationale, and rough price suggestion.",
            agent=niche_scout,
        )
        tasks.append(scout_task)
        if not main_topic:
            main_topic = "profitable micro digital product for professionals or students"

    research_task = Task(
        description=f"Research the opportunity around '{main_topic}'. Identify exact buyer pain, top 3 competing products (if any), winning keywords, best price point ($7-25), and the highest-leverage single product format (prompt pack, template bundle, checklist + guide, etc.).",
        expected_output="Structured research per the ResearchResult model.",
        agent=researcher,
        output_pydantic=ResearchResult,
    )

    create_task = Task(
        description=f"Using the research, CREATE the actual sellable digital product for '{main_topic}'. "
                    "Produce the full content in clean Markdown. If it's a prompt library, deliver 8-20 high-quality prompts with usage instructions. "
                    "If templates, give ready-to-use examples. Make it genuinely valuable so people will pay and not refund. "
                    "Start with a clear title line.",
        expected_output="Complete product content in Markdown (the actual deliverable customers will download).",
        agent=content_producer,
    )

    listing_task = Task(
        description="Write a high-converting Gumroad product listing based on the created product. "
                    "Deliver title, price, description, and tags.",
        expected_output="Structured listing per ListingResult model.",
        agent=listing_specialist,
        output_pydantic=ListingResult,
    )

    review_task = Task(
        description="Review the product content + listing. Score quality and profit potential 1-10. Decide GO or NO-GO. List improvements if needed.",
        expected_output="Structured review per ReviewResult model.",
        agent=quality_reviewer,
        output_pydantic=ReviewResult,
    )

    marketing_task = Task(
        description="Create a complete marketing launch package for fast sales. Generate: 1) 3 A/B test variants of the Gumroad title + description with stronger hooks, scarcity, and social proof. 2) 5 ready-to-post social media assets (X threads, LinkedIn post, Reddit post) with engaging hooks and calls to action. 3) A 5-email launch sequence (subject lines + body). 4) 2-3 bundle/upsell ideas with pricing. 5) Suggested launch timing and urgency tactics. Base everything on the product research and target buyer pain points.",
        expected_output="Structured marketing package with copy, posts, emails, bundles, and launch recommendations.",
        agent=marketing_specialist,
    )

    tasks.extend([research_task, create_task, listing_task, review_task, marketing_task])
    return tasks

# ==================== CORE RUNNER ====================

def run_agentforge(topic: str = "AI prompt libraries for law students"):
    """Legacy simple runner (kept for compatibility)."""
    llm = get_llm()
    agents = build_autonomous_agents(llm)[:3]  # use first 3 for legacy
    tasks = build_autonomous_tasks(topic, agents)[:3]

    crew = Crew(agents=agents, tasks=tasks, process=Process.sequential, verbose=True)
    return crew.kickoff()


# ==================== FILE MATERIALIZATION (REAL PRODUCTS) ====================

def _slug(text: str) -> str:
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text).strip().lower()
    return re.sub(r'[\s-]+', '-', text)[:60]


def materialize_product(crew_result: str, topic: str, price_usd: float = 12.0) -> Dict[str, Any]:
    """
    Turns crew output into real, sellable digital product files + zip.
    Produces Markdown + a simple PDF when possible.
    """
    slug = _slug(topic)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    prod_dir = GENERATED_DIR / f"{slug}-{timestamp}"
    prod_dir.mkdir(parents=True, exist_ok=True)

    price_cents = int(price_usd * 100)
    result_str = str(crew_result)

    # 1. Raw crew log
    (prod_dir / "full_output.md").write_text(result_str, encoding="utf-8")

    # 2. Main deliverable (cleaned Markdown)
    product_content = result_str[:15000]
    md_path = prod_dir / "product.md"
    md_path.write_text(f"# {topic}\n\n{product_content}\n\n---\nGenerated by AgentForge Digital", encoding="utf-8")

    # 3. Try to generate a nicer PDF (using fpdf2)
    pdf_path = prod_dir / "product.pdf"
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, topic[:75], new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(4)
        pdf.set_font("Helvetica", "", 10)

        for line in product_content.split("\n")[:180]:
            safe = line.encode("latin-1", "replace").decode("latin-1")[:95]
            pdf.multi_cell(0, 5.5, safe)
            pdf.ln(0.8)

        pdf.output(str(pdf_path))
        logger.info("PDF generated successfully")
    except Exception as e:
        logger.warning("PDF generation skipped: %s", e)
        pdf_path = None  # Markdown + zip is still sellable (especially prompt packs)

    # 4. Gumroad-ready listing + seller instructions
    (prod_dir / "GUMROAD_LISTING.txt").write_text(
        f"TITLE: {topic[:75]}\nPRICE: ${price_usd:.0f}\n\n"
        f"DESCRIPTION / WHAT'S INSIDE:\n{result_str[-4500:]}\n\n"
        f"Deliverable: product.md + product.pdf (if generated)",
        encoding="utf-8"
    )

    (prod_dir / "SELLER_INSTRUCTIONS.txt").write_text(
        "AUTONOMOUS PRODUCT GENERATED BY AgentForge\n\n"
        "1. The zip contains the customer deliverable.\n"
        "2. On Gumroad, after creating the product, attach this zip (or product.pdf + product.md).\n"
        "3. Recommended: use the title and description from GUMROAD_LISTING.txt\n"
        "4. Price shown above is a suggestion - adjust based on perceived value.\n",
        encoding="utf-8"
    )

    # 5. Zip everything nice for the customer
    zip_path = prod_dir / f"{slug}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(prod_dir.iterdir()):
            if f.is_file() and not f.name.endswith(".zip"):
                zf.write(f, arcname=f.name)

    # Log
    product_id = product_db.log_product(title=topic, niche=topic, price_cents=price_cents, file_path=str(zip_path))

    return {
        "product_id": product_id,
        "dir": str(prod_dir),
        "zip_path": str(zip_path),
        "pdf_path": str(pdf_path) if pdf_path and pdf_path.exists() else None,
        "price_cents": price_cents,
        "slug": slug,
    }


def generate_marketing_package(prod_dir: Path, crew_result: str, research_data: Optional[ResearchResult] = None, listing_data: Optional[ListingResult] = None):
    """
    Autonomous marketing logic to drive quick sales.
    Creates a marketing/ folder with launch-ready assets.
    """
    marketing_dir = prod_dir / "marketing"
    marketing_dir.mkdir(exist_ok=True)

    result_str = str(crew_result)
    title = listing_data.title if listing_data else "High-Value AI Prompt Pack"
    price = listing_data.price_usd if listing_data else 17.0

    # 1. Gumroad copy variants (A/B tests for fast conversion)
    variants = f"""# Gumroad Listing A/B Variants for Fast Sales

## Variant A - Hook + Social Proof (Recommended for quick money)
Title: {title} (+ Bonus Agent Prompts)

Description:
🚀 Stop wasting hours on mediocre AI output.

This {title} gives you battle-tested prompts used by power users to 5-10x their results with Grok, Claude, and modern AI tools.

Inside:
- 100+ categorized prompts for AI tools & workflows
- Master Prompt Chains (MPCs) that actually work
- "Prompts people don't know" — advanced techniques that deliver outsized results
- Usage instructions + variations for every prompt

Perfect for researchers, builders, writers, and professionals who want leverage.

**Limited Launch Price: ${price:.0f}** (increases soon)
Get it now before the price goes up.

Bonuses:
- Free "Agent Scaffolding" prompt pack (while supplies last)
- Lifetime updates

---

## Variant B - Curiosity + Scarcity
Title: The Prompt Techniques Top AI Users Keep Secret

Description:
Most people are using basic prompts and getting basic results.

This collection contains the underrated, high-leverage techniques and AI tool-specific libraries that serious users rely on but rarely share publicly.

- Underrated prompt patterns for Grok, Claude, Cursor, and more
- Master Prompt Collections (MPCs) for agent building
- Prompts for research, writing, and automation that 99% miss
- Ready-to-use chains that turn AI into a real productivity multiplier

Only ${price:.0f} during this launch window.

Includes full usage guides and bonus templates.

Don't get left behind with generic prompting.

---

## Variant C - Value Stack + Bundle Tease
Title: AI Tool Libraries + Secret Prompt MPC Bundle

Description:
Everything you need to dominate with modern AI tools:

• Full Grok/xAI Power User Library
• Claude Tool & Agent Master Prompt Collection
• Underrated techniques most users have never seen

Normally sold separately for much more. Get the complete stack for ${price:.0f}.

Instant download. Use today.
"""

    (marketing_dir / "gumroad_variants.md").write_text(variants, encoding="utf-8")

    # 2. Social media assets
    social = f"""# Ready-to-Post Social Assets (Autonomous Launch)

## X / Twitter Thread
1/ Most people use AI like a fancy autocomplete.

Here's how power users actually get 5-10x better results with Grok, Claude, Cursor, etc.

(Full thread with hooks + CTAs — generated from research)

Link in bio / replies.

## LinkedIn Post
Tired of generic AI output that sounds like everyone else?

I just released a new collection of battle-tested prompt libraries and AI toolchains that serious professionals are using to ship faster and think better.

Includes:
- Tool-specific libraries (not generic fluff)
- Master Prompt Collections for agentic workflows
- The "prompts people don't know" that separate top performers

Grab it here: [LINK]
What’s one AI workflow you wish was easier?

## Reddit Post (r/AI, r/ChatGPT, r/productivity, etc.)
Title: I built the prompt libraries I wish existed for power users (Grok, Claude, Cursor, etc.)

Body:
After months of testing, here are the actual prompt packs and MPCs that have been moving the needle for me and others.

Focus on:
- AI Tool Libraries
- Underrated techniques
- Ready-to-run agent chains

[LINK]

Happy to answer questions in comments.

---

More variants and platform-specific copies in full package. Customize with your voice.
"""

    (marketing_dir / "social_assets.md").write_text(social, encoding="utf-8")

    # 3. Email sequence
    email_seq = f"""# 5-Email Launch Sequence (Copy-Paste Ready)

**Email 1 - Announcement (Day 0)**
Subject: New: The AI prompts I actually use every day

Hi [Name],

I got tired of generic prompt lists that don't work in real tools.

So I built the exact libraries I wish existed:
- Grok/xAI power prompts
- Claude tool & agent MPCs
- Underrated techniques most people miss

Launched at ${price:.0f} for the first 48 hours.

[Button: Get the packs]

---

**Email 2 - Value / Social Proof (Day 1)**
Subject: Why these prompts are different

Most AI "prompt books" give you 20 basic templates.

Mine include:
- Tool-specific libraries (Cursor, Claude Projects, Grok, etc.)
- Master Prompt Collections with 100+ entries
- The hidden patterns that create compounding results

Early users are already reporting big wins in research and building speed.

[Link]

---

**Email 3 - Scarcity / Bonus (Day 2)**
Subject: Price increases tonight + free bonus

Quick note: The launch price of ${price:.0f} ends in a few hours.

If you grab it now, you also get the free "Agent Scaffolding" bonus pack.

[Link]

---

**Email 4 - Story / Problem (Day 3)**
Subject: How I was wasting hours with AI before this

[Personal story hook]

Then discovered these specific techniques...

[Link to product]

---

**Email 5 - Last chance / Bundle (Day 4)**
Subject: Last day at launch price + bundle option

This is the final day at ${price:.0f}.

Or grab the full AI Toolchain + Secret Prompts bundle for [higher price].

[Links]

Thanks,
[Your Name]
"""

    (marketing_dir / "email_sequence.md").write_text(email_seq, encoding="utf-8")

    # 4. Bundles and upsells
    bundles = f"""# Bundle & Upsell Recommendations (Autonomous)

1. Core Bundle: Grok Library + Claude MPC — ${price + 12:.0f} (save $X)
2. Power User Stack: All 4 libraries — ${price * 3:.0f}
3. Bonus Upsell: Add "Underrated Techniques" for +$7 at checkout

Suggested Gumroad upsell products: Create these as separate products or use Gumroad's built-in upsells.

Cross-sell email: "Bought the Grok pack? You'll love the Claude one for Projects..."
"""

    (marketing_dir / "bundles_upsells.md").write_text(bundles, encoding="utf-8")

    # 5. Launch plan
    launch_plan = f"""# Autonomous Launch Plan for Quick Money

**Pre-Launch (Day -1)**
- Finalize product + zip
- Post teaser on X/LinkedIn
- Warm up email list if any

**Day 0 - Launch**
- Publish to Gumroad with Variant A
- Post main social thread + Reddit
- Send Email 1

**Day 1**
- Post value content + Email 2
- Engage with comments

**Day 2**
- Scarcity post + Email 3
- Consider small paid boost if budget

**Ongoing**
- Monitor sales in product_db
- Use Strategist agent on winners
- Create bundles from top performers

**Fast Money Tactics Used Here:**
- Strong hooks in first line
- Social proof + specificity
- Scarcity (launch pricing)
- Bonuses
- Multiple platforms
- Email nurture

Run this package, post the assets, and the product should start converting.
"""

    (marketing_dir / "launch_plan.md").write_text(launch_plan, encoding="utf-8")

    # 6. Additional quick-money assets for autonomy
    ad_copy = f"""# Ad Copy & Promotion Snippets (for paid or organic boost)

Google/Facebook Ad Headline Options:
1. "20+ Grok Prompts That Actually Work (Power User Pack)"
2. "Stop Wasting Time on Bad AI Output - Get These Secret Prompts"
3. "The AI Tool Library Pros Use (Save 10+ Hours/Week)"

Body: "Battle-tested prompts for Grok, Claude, Cursor & more. Master Prompt Collections + techniques 99% miss. Instant download. ${price:.0f} launch price."

Twitter Bio / Link in bio suggestion:
"Building & selling high-ROI AI prompt libraries. Currently dropping Grok & Claude packs."

Viral Hook Ideas:
- "The one prompt that made my Grok 10x better at [task]"
- Thread: "I tested 200 prompts so you don't have to. Here are the 12 that actually work."
"""

    (marketing_dir / "ad_copy_promotion.md").write_text(ad_copy, encoding="utf-8")

    # 7. Auto-update suggestion for Gumroad (for the runner to use)
    best_variant = f"""# Best Variant Suggestion (use this for initial Gumroad publish)
Use Variant A for best quick conversion.
Title: {title} (+ Bonus Agent Prompts)
Price: ${price:.0f}
Include the bonuses and scarcity language from the variants file.
"""

    (marketing_dir / "best_gumroad_variant.txt").write_text(best_variant, encoding="utf-8")

    logger.info(f"Marketing package generated in {marketing_dir}")
    return str(marketing_dir)


# ==================== GUMROAD INTEGRATION ====================

def _retry_request(method: str, url: str, **kwargs) -> requests.Response:
    """Very small retry helper for network calls."""
    last_exc = None
    for attempt in range(3):
        try:
            resp = requests.request(method, url, timeout=kwargs.pop("timeout", 30), **kwargs)
            if resp.status_code < 500:
                return resp
            last_exc = RuntimeError(f"Server error {resp.status_code}")
        except Exception as e:
            last_exc = e
        logger.warning("Request attempt %s failed, retrying...", attempt + 1)
        import time; time.sleep(1.5 * (attempt + 1))
    raise last_exc or RuntimeError("Request failed after retries")

def create_gumroad_product(
    title: str,
    description: str,
    price_cents: int,
    gumroad_token: str,
    file_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a product on Gumroad. Tries to attach file if provided."""
    if not gumroad_token:
        raise ValueError("Gumroad access token required (env GUMROAD_ACCESS_TOKEN or paste in UI)")

    headers = {"Authorization": f"Bearer {gumroad_token}"}
    data = {
        "name": title[:80],
        "description": description[:5000],
        "price": price_cents,
        "custom_receipt": "Thank you! Your digital product is ready.",
        "filetype": "zip",  # hint for digital deliverable
    }

    files = None
    if file_path and Path(file_path).exists():
        try:
            files = {"file": (Path(file_path).name, open(file_path, "rb"), "application/zip")}
            logger.info("Attempting Gumroad file attachment: %s", file_path)
        except Exception as e:
            logger.warning("File open failed for Gumroad upload: %s", e)

    try:
        resp = _retry_request("POST", f"{GUMROAD_API}/products", headers=headers, data=data, files=files)
    finally:
        if files and hasattr(files["file"][1], "close"):
            try:
                files["file"][1].close()
            except Exception:
                pass

    if resp.status_code not in (200, 201):
        # Fallback: create without file (common case)
        logger.warning("Direct file upload failed or not supported. Creating metadata only. You can attach the zip manually.")
        data.pop("filetype", None)
        resp = _retry_request("POST", f"{GUMROAD_API}/products", headers=headers, data=data)

    if resp.status_code not in (200, 201):
        raise RuntimeError(f"Gumroad error {resp.status_code}: {resp.text}")

    product = resp.json().get("product", {})
    gumroad_id = product.get("id")
    gumroad_url = product.get("short_url") or f"https://gumroad.com/products/{gumroad_id}"

    logger.info("Gumroad product created: %s", gumroad_url)
    return {
        "gumroad_id": gumroad_id,
        "gumroad_url": gumroad_url,
        "raw": product,
    }


def prepare_gumroad_file_attach(zip_path: str) -> str:
    """Returns instructions + path for manual attach if API upload didn't work."""
    p = Path(zip_path)
    if not p.exists():
        return "File not found"
    msg = (
        f"Ready to attach:\n"
        f"  Path: {p.resolve()}\n"
        f"  Size: {p.stat().st_size / 1024:.1f} KB\n\n"
        "On Gumroad product edit page → Upload file → select the zip above.\n"
        "This gives customers instant download after purchase."
    )
    return msg


# ==================== PREMIUM UI HELPERS ====================

def inject_premium_css():
    """Premium dark/modern styling for a high-end product feel."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap');

    .stApp {
        background: linear-gradient(145deg, #0f1117 0%, #161a24 100%);
        font-family: 'Inter', system_ui, sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    .premium-card {
        background: #1c202b;
        border: 1px solid #2a2f3d;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #e0e4f0;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .status-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-connected { background: #052e16; color: #4ade80; }
    .status-missing { background: #3f1f1f; color: #f87171; }

    .metric-card {
        background: #1c202b;
        border-radius: 12px;
        padding: 12px 16px;
        border: 1px solid #2a2f3d;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1c202b;
        border-radius: 10px 10px 0 0;
        padding: 10px 18px;
        border: 1px solid #2a2f3d;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: #252b38;
        border-bottom: 3px solid #3b82f6;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        border: none;
    }

    .connector-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)


def get_status_badge(is_connected: bool, label: str = "") -> str:
    cls = "status-connected" if is_connected else "status-missing"
    text = "✓ Connected" if is_connected else "Missing"
    return f'<span class="status-badge {cls}">{label} {text}</span>'


def test_llm_connection(provider: str = "xai") -> tuple[bool, str]:
    """Lightweight test for AI connectors."""
    try:
        if provider in ("xai", "grok"):
            model = os.getenv("XAI_MODEL") or _session_get("ai_model", "grok-4")
            result, err = call_xai_direct(
                [{"role": "user", "content": "Respond with exactly: Connection OK"}],
                model=model,
            )
            if err:
                return False, err
            return True, str(result)[:120]

        llm = get_llm(provider=provider)
        response = llm.call(
            messages=[{"role": "user", "content": "Respond with exactly: Connection OK"}]
        )
        return True, str(response)[:120]
    except Exception as e:
        return False, str(e)[:200]


def call_xai_direct(input_list, model=None):
    """Direct call to xAI Responses API, matching the user's curl example."""
    key = os.getenv("XAI_API_KEY") or _session_get("xai_key")
    if not _valid_key(key):
        return None, "No XAI_API_KEY found. Set it in .env or Settings."

    model = model or os.getenv("XAI_MODEL") or _session_get("ai_model", "grok-4")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
    payload = {
        "model": model,
        "input": input_list
    }
    try:
        resp = requests.post(
            "https://api.x.ai/v1/responses",
            headers=headers,
            json=payload,
            timeout=60
        )
        resp.raise_for_status()
        return resp.json(), None
    except Exception as e:
        return None, f"Error: {str(e)}"


def sync_gumroad_sales(gumroad_token: str) -> int:
    """Pull latest sales numbers for all live products. Returns number of products updated."""
    if not gumroad_token:
        return 0

    headers = {"Authorization": f"Bearer {gumroad_token}"}

    updated = 0
    for row in product_db.get_live_products():
        if not row.get("gumroad_id"):
            continue
        pid = row["id"]
        gum_id = row["gumroad_id"]

        try:
            r = requests.get(f"{GUMROAD_API}/sales", headers=headers, params={"product_id": gum_id}, timeout=20)
            if r.status_code == 200:
                sales_data = r.json().get("sales", [])
                new_sales = len(sales_data)
                # Gumroad sales 'price' is usually in cents
                new_revenue = sum(int(s.get("price", 0) or 0) for s in sales_data)
                product_db.update_sales(pid, new_sales, new_revenue)
                updated += 1
                logger.info(f"Synced sales for product {pid}: {new_sales} sales, ${new_revenue/100:.2f}")
        except Exception as e:
            logger.warning(f"Failed to sync sales for {gum_id}: {e}")

    return updated


# ==================== COMPLETE AUTONOMY ENGINE ====================

def run_full_autonomous_cycle(
    topic: Optional[str] = None,
    auto_publish: bool = False,
    gumroad_token: Optional[str] = None,
    max_price: float = 19.0,
) -> Dict[str, Any]:
    """
    The main autonomous profit loop.
    1. Research + create product
    2. Materialize real files + zip
    3. (Optional) Publish to Gumroad
    4. Log everything
    """
    llm = get_llm()
    agents = build_autonomous_agents(llm)
    tasks = build_autonomous_tasks(topic, agents)

    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    result_str = str(result)
    logger.info("Crew finished. Output length: %d chars", len(result_str))

    # === Extract structured results when available ===
    review_data = None
    listing_data = None
    research_data = None

    if isinstance(result, list):
        for item in result:
            if isinstance(item, ReviewResult):
                review_data = item
            elif isinstance(item, ListingResult):
                listing_data = item
            elif isinstance(item, ResearchResult):
                research_data = item
    else:
        # Fallback: try to parse the raw result for the review
        pass

    # Title from listing or first lines
    if listing_data and listing_data.title:
        title = listing_data.title
    else:
        lines = [l.strip() for l in result_str.split("\n") if l.strip()]
        title = lines[0][:90] if lines else (topic or "Untitled Digital Product")

    price_usd = (listing_data.price_usd if listing_data else 12.0)

    # Materialize real product
    mat = materialize_product(result_str, title, price_usd=price_usd)
    logger.info("Materialized product: %s", mat["zip_path"])

    # === Autonomous Marketing for Quick Sales (always run to make money fast) ===
    try:
        marketing_dir = generate_marketing_package(
            Path(mat["dir"]), result_str, research_data, listing_data
        )
        logger.info("Marketing package created: %s", marketing_dir)
        mat["marketing_dir"] = marketing_dir
    except Exception as e:
        logger.error("Marketing generation failed: %s", e)

    # === Cost tracking ===
    est_cost = estimate_cost_usd(result_str, is_output=True)
    est_cost_cents = int(est_cost * 100)
    logger.info("Estimated cost for this cycle: $%.4f", est_cost)

    published = False
    gum_url = None
    decision = "NO-GO"

    # === Improved Quality Gate using structured output ===
    if review_data:
        decision = review_data.decision
        go = (decision.upper() == "GO")
        quality = review_data.quality_score
        profit = review_data.profit_potential
        logger.info("Structured review: quality=%s profit=%s decision=%s", quality, profit, decision)
    else:
        # Fallback
        go = ("GO" in result_str.upper() and "NO-GO" not in result_str.upper())
        quality = 6
        profit = 6
        decision = "GO" if go else "NO-GO"

    if auto_publish and go and gumroad_token:
        try:
            listing_desc = (listing_data.description if listing_data else result_str[-3500:])
            g = create_gumroad_product(
                title=title,
                description=f"Generated autonomously by AgentForge Digital.\n\n{listing_desc}",
                price_cents=mat["price_cents"],
                gumroad_token=gumroad_token,
                file_path=mat.get("zip_path"),
            )
            product_db.update_gumroad_info(mat["product_id"], g["gumroad_id"], g["gumroad_url"])
            published = True
            gum_url = g["gumroad_url"]
            logger.info("Published to Gumroad: %s", gum_url)
        except Exception as e:
            logger.error("Publish failed: %s", e)
            result_str += f"\n\n[Publish error: {e}]"
    elif auto_publish and not go:
        logger.warning("Quality gate blocked publishing (decision=%s)", decision)

    # Log to run history
    q_score = review_data.quality_score if review_data else 6
    p_score = review_data.profit_potential if review_data else 6
    try:
        product_db.log_run_history(
            topic=title,
            decision=decision,
            quality=q_score,
            profit=p_score,
            est_cost_cents=est_cost_cents,
            product_id=mat["product_id"],
            published=published,
            gumroad_url=gum_url,
            notes="structured" if review_data else "text-fallback"
        )
    except Exception as e:
        logger.warning("Failed to log run history: %s", e)

    return {
        "topic": title,
        "result": result_str,
        "product_id": mat["product_id"],
        "zip_path": mat["zip_path"],
        "published": published,
        "gumroad_url": gum_url,
        "files_dir": mat["dir"],
        "marketing_dir": mat.get("marketing_dir"),
        "est_cost_usd": est_cost,
        "decision": decision,
    }


# ==================== SALES → STRATEGIST FEEDBACK LOOP ====================

def analyze_top_performers_and_suggest(llm=None, top_n=5) -> List[str]:
    """After syncing sales, use revenue data + niche memory to suggest next products."""
    if llm is None:
        llm = get_llm()

    memory = product_db.get_niche_memory()
    best = product_db.get_best_niches(top_n)

    # Simple prompt for strategist
    strategist = build_strategist_agent(llm)

    context = f"Top niches by revenue: {best}\n\nRecent performance summary:\n"
    for m in memory[:8]:
        context += f"- {m['niche']}: {m['successes']}/{m['attempts']} successes, ${m.get('total_revenue_cents',0)/100:.2f} revenue, avg_profit={m.get('avg_profit',0):.1f}\n"

    task = Task(
        description=f"Based on this performance data, recommend 4-6 specific new or variant product ideas that are likely to sell well (focus on cloning winners with twists). Also suggest specific marketing tactics (hooks, bundles, channels) that worked or would amplify these. Be concrete and optimized for quick cash.\n\n{context}",
        expected_output="List of 4-6 actionable product topics with short rationale + marketing amplification ideas.",
        agent=strategist,
    )

    crew = Crew(agents=[strategist], tasks=[task], process=Process.sequential, verbose=False)
    res = crew.kickoff()
    suggestions = str(res)

    # Update niche memory lightly if we have winners
    for b in best:
        product_db.update_niche_memory(b, success=True, revenue_cents=0)

    return suggestions.split("\n")[:6]

# ==================== STREAMLIT AUTONOMOUS DASHBOARD ====================

def main():
    st.set_page_config(page_title="AgentForge Digital", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")
    inject_premium_css()

    # Premium Header
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:4px;">
        <span style="font-size:2.1rem; font-weight:700; background: linear-gradient(90deg,#3b82f6,#60a5fa); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">AgentForge</span>
        <span style="font-size:1rem; color:#64748b;">Digital</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Autonomous AI product engine • Research → Build → Package → Publish to Gumroad")

    # Top metrics
    c1, c2, c3, c4 = st.columns(4)
    rev = product_db.get_total_revenue() / 100
    recent = product_db.get_recent_runs(8)
    total_cost = sum((r.get("est_cost_cents") or 0) for r in recent) / 100
    live = len([r for r in product_db.get_all_products() if r.get("status") in ("live","generated")])
    c1.metric("Revenue", f"${rev:,.2f}")
    c2.metric("Recent Runs", len(recent), f"-${total_cost:.2f} cost")
    c3.metric("Live Products", live)
    c4.metric("Model", st.session_state.get("ai_model", "grok-4.3"))

    # Premium Sidebar (status only)
    with st.sidebar:
        st.markdown("### Connection Status")
        st.markdown(get_status_badge(bool(XAI_API_KEY or st.session_state.get("xai_key")), "xAI"), unsafe_allow_html=True)
        st.markdown(get_status_badge(bool(OPENAI_API_KEY or st.session_state.get("openai_key")), "OpenAI"), unsafe_allow_html=True)
        st.markdown(get_status_badge(bool(GUMROAD_TOKEN or st.session_state.get("gumroad_token")), "Gumroad"), unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Quick Launch")
        if st.button("▶ Run 1 Cycle", use_container_width=True, type="primary"):
            with st.spinner("Running..."):
                res = run_full_autonomous_cycle(auto_publish=False)
                st.session_state["last_res"] = res
                st.rerun()

        if st.button("Sync + Suggest", use_container_width=True):
            sync_gumroad_sales(GUMROAD_TOKEN or os.getenv("GUMROAD_ACCESS_TOKEN"))
            st.rerun()

    # Premium Tabs including new Settings
    tab_dash, tab_run, tab_lib, tab_auto, tab_gum, tab_settings = st.tabs([
        "📊 Dashboard", "🚀 Run", "📦 Library", "🤖 Autonomy", "🛒 Gumroad", "⚙️ Settings"
    ])

    # Dashboard
    with tab_dash:
        st.markdown("### Recent Activity")
        runs = product_db.get_recent_runs(5)
        if runs:
            st.dataframe(runs, use_container_width=True, hide_index=True)
        else:
            st.info("No runs yet. Go to Settings to set AI keys.")

    # Run
    with tab_run:
        topic = st.text_input("Niche / Topic", value="AI prompt libraries for law students", key="run_topic")
        if st.button("Run Full Crew", type="primary", use_container_width=True):
            with st.spinner("Agents active..."):
                res = run_full_autonomous_cycle(topic=topic)
                st.success("Complete")
                if res.get("zip_path"):
                    st.code(res["zip_path"])

    # Library
    with tab_lib:
        for row in product_db.get_all_products()[:8]:
            with st.container(border=True):
                st.markdown(f"**{row.get('title','')}** — ${ (row.get('price_cents') or 0)/100:.0f} | Sales: {row.get('sales',0)}")
                fp = row.get("file_path")
                if fp and Path(fp).exists():
                    with open(fp, "rb") as f:
                        st.download_button("Download", f, file_name=Path(fp).name, key=str(row["id"]))

    # Autonomy
    with tab_auto:
        if st.button("💰 FULL AUTONOMOUS MONEY MODE (Cycle + Marketing + Suggest)", type="primary", use_container_width=True):
            token = os.getenv("GUMROAD_ACCESS_TOKEN")
            res = run_full_autonomous_cycle(auto_publish=bool(token), gumroad_token=token)
            st.success(f"Done. Product: {res.get('zip_path')}")
            if res.get("marketing_dir"):
                st.success(f"📣 FULL MARKETING PACKAGE: {res['marketing_dir']}")
                st.markdown("""
                **To make money NOW:**
                1. Use `best_gumroad_variant.txt` or `gumroad_variants.md` to set your Gumroad listing.
                2. Copy-paste from `social_assets.md` to X/LinkedIn/Reddit.
                3. Send the `email_sequence.md`.
                4. Follow `launch_plan.md`.
                """)
            if res.get("gumroad_url"):
                st.markdown(f"**Published:** {res['gumroad_url']}")
        
        colA, colB = st.columns(2)
        with colA:
            if st.button("Just Run Cycle + Marketing"):
                res = run_full_autonomous_cycle(auto_publish=False)
                st.success(f"Done. {res.get('zip_path')}")
                if res.get("marketing_dir"):
                    st.info(f"Marketing: {res['marketing_dir']}")
        with colB:
            if st.button("Get Strategist + Marketing Ideas"):
                st.write(analyze_top_performers_and_suggest())
                st.caption("Strategist now includes marketing amplification suggestions.")

    # Gumroad
    with tab_gum:
        if st.button("Test Gumroad"):
            st.info("Configure in Settings.")
        latest = st.text_input("Zip path")
        if st.button("Prepare Attach"):
            st.code(prepare_gumroad_file_attach(latest) if latest else "")

    # Settings Tab - All AI Connectors (xAI is primary)
    with tab_settings:
        st.markdown("## ⚙️ Settings — AI Connectors")

        st.markdown("### xAI (Grok) — Primary / Recommended")
        st.caption("Get your key at https://console.x.ai")
        xai_key = st.text_input("XAI_API_KEY", value=XAI_API_KEY or st.session_state.get("xai_key", ""), type="password", key="settings_xai_key")
        xai_model = st.selectbox("xAI Model", ["grok-4.3", "grok-3", "grok-2"], index=0, key="settings_xai_model")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Test xAI (LangChain)", key="test_xai_langchain"):
                if xai_key:
                    os.environ["XAI_API_KEY"] = xai_key
                    st.session_state["xai_key"] = xai_key
                    st.session_state["ai_provider"] = "xai"
                    ok, msg = test_llm_connection("xai")
                    (st.success if ok else st.error)(msg)
        with col2:
            if st.button("Test xAI Direct (/responses)", key="test_xai_direct"):
                if xai_key:
                    os.environ["XAI_API_KEY"] = xai_key
                    st.session_state["xai_key"] = xai_key
                    st.session_state["ai_provider"] = "xai"
                    input_messages = [
                        {"role": "system", "content": "You are Grok, a highly intelligent, helpful AI assistant."},
                        {"role": "user", "content": "Test connection. Reply with 'xAI connected successfully'."}
                    ]
                    result, err = call_xai_direct(input_messages, model=xai_model)
                    if err:
                        st.error(err)
                    else:
                        st.success("Direct call succeeded!")
                        st.json(result)

        st.markdown("#### Try your exact curl example")
        if st.button("Run your example query via Direct xAI"):
            if not (xai_key or st.session_state.get("xai_key")):
                st.error("Please enter and save your XAI_API_KEY above first.")
            else:
                example_input = [
                    {
                        "role": "system",
                        "content": "You are Grok, a highly intelligent, helpful AI assistant."
                    },
                    {
                        "role": "user",
                        "content": "What is the meaning of life, the universe, and everything?"
                    }
                ]
                result, err = call_xai_direct(example_input, model=xai_model)
                if err:
                    st.error(err)
                else:
                    st.success("Response received from xAI /responses endpoint:")
                    # Try to nicely extract the answer
                    if isinstance(result, dict):
                        st.write(result)
                    else:
                        st.write(result)

        st.markdown("### OpenAI (Fallback)")
        oai_key = st.text_input("OPENAI_API_KEY", value=OPENAI_API_KEY or st.session_state.get("openai_key", ""), type="password", key="settings_oai_key")
        oai_model = st.selectbox("OpenAI Model", ["gpt-4o-mini", "gpt-4o"], key="settings_oai_model")
        if st.button("Test OpenAI Connection", key="test_oai_btn"):
            if oai_key:
                os.environ["OPENAI_API_KEY"] = oai_key
                st.session_state["openai_key"] = oai_key
                ok, msg = test_llm_connection("openai")
                (st.success if ok else st.error)(msg)

        st.markdown("### Anthropic Claude (optional)")
        anth_key = st.text_input("ANTHROPIC_API_KEY", value=st.session_state.get("anth_key", ""), type="password", key="settings_anth")
        st.caption("Stored for future use. Install langchain-anthropic if needed.")

        st.markdown("### Parameters & Gumroad")
        temp = st.slider("Temperature", 0.0, 1.2, st.session_state.get("temperature", 0.65), 0.05, key="settings_temp")
        max_t = st.slider("Max Tokens", 512, 8192, st.session_state.get("max_tokens", 3000), 128, key="settings_maxt")
        price = st.number_input("Default Price ($)", 5.0, 49.0, st.session_state.get("default_price", 12.0), 1.0, key="settings_price")
        gum = st.text_input("GUMROAD_ACCESS_TOKEN", value=GUMROAD_TOKEN or st.session_state.get("gumroad_token", ""), type="password", key="settings_gum")
        st.caption("Get token: Gumroad → Settings → Advanced → Applications → create app → Generate access token ([open Advanced settings](https://gumroad.com/settings/advanced))")

        if st.button("💾 Save & Apply All", type="primary", use_container_width=True):
            if xai_key:
                os.environ["XAI_API_KEY"] = xai_key
                st.session_state["xai_key"] = xai_key
                st.session_state["ai_provider"] = "xai"
            if oai_key:
                os.environ["OPENAI_API_KEY"] = oai_key
                st.session_state["openai_key"] = oai_key
            if gum:
                os.environ["GUMROAD_ACCESS_TOKEN"] = gum
                st.session_state["gumroad_token"] = gum
            st.session_state.update({
                "ai_model": xai_model,
                "openai_model": oai_model,
                "temperature": temp,
                "max_tokens": max_t,
                "default_price": price,
            })
            st.success("Settings saved. xAI is now primary. New runs will use it immediately.")
            st.rerun()

        if st.button("🔌 Test All AI Connectors"):
            for p in ["xai", "openai"]:
                ok, msg = test_llm_connection(p)
                st.write(f"{p.upper()}: {'✅ ' + msg[:80] if ok else '❌ ' + msg[:80]}")

        st.info("xAI is the default. Enter your key above and Save. For headless/cron use, also export XAI_API_KEY or put it in .env")

    st.caption("Premium UI • All AI connectors in Settings tab • Full autonomy + profitability features")

if __name__ == "__main__":
    main()

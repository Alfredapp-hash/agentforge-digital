#!/usr/bin/env python3
"""
Headless autonomy runner for AgentForge Digital.
Run this on a schedule (cron, GitHub Actions, Render cron, etc.) for true hands-off profitability.

Usage:
    export XAI_API_KEY=...
    export GUMROAD_ACCESS_TOKEN=...
    python autonomy_runner.py --cycles 2 --publish
"""

import argparse
import os
import logging
from pathlib import Path

from agentforge_main import (
    run_full_autonomous_cycle,
    sync_gumroad_sales,
    analyze_top_performers_and_suggest,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
logger = logging.getLogger("autonomy_runner")

def main():
    parser = argparse.ArgumentParser(description="Run AgentForge autonomous product generation")
    parser.add_argument("--cycles", type=int, default=1, help="How many autonomous product cycles to run")
    parser.add_argument("--publish", action="store_true", help="Attempt to publish successful products to Gumroad")
    parser.add_argument("--marketing", action="store_true", default=True, help="Generate full marketing launch package (social, email, bundles) for quick sales. Enabled by default.")
    parser.add_argument("--no-marketing", dest="marketing", action="store_false")
    parser.add_argument("--topic", type=str, default=None, help="Force a specific topic instead of discovery")
    args = parser.parse_args()

    token = os.getenv("GUMROAD_ACCESS_TOKEN")

    logger.info("Starting %d autonomous profit cycle(s) with marketing=%s...", args.cycles, args.marketing)
    successes = 0
    marketed = 0

    for i in range(args.cycles):
        logger.info("=== Cycle %d ===", i + 1)
        try:
            res = run_full_autonomous_cycle(
                topic=args.topic,
                auto_publish=args.publish,
                gumroad_token=token if args.publish else None,
            )
            logger.info("Topic: %s", res.get("topic"))
            logger.info("Zip: %s", res.get("zip_path"))
            if res.get("marketing_dir"):
                logger.info("Marketing assets: %s", res.get("marketing_dir"))
                marketed += 1

                # Autonomous next steps for money
                marketing_path = res.get("marketing_dir")
                logger.info("=== AUTONOMOUS MARKETING DEPLOYMENT INSTRUCTIONS ===")
                logger.info(f"1. Use best_gumroad_variant.txt to update/publish on Gumroad (if not already).")
                logger.info(f"2. Post social_assets.md content to X, LinkedIn, Reddit TODAY.")
                logger.info(f"3. Send email_sequence.md (or schedule in your ESP).")
                logger.info(f"4. Use ad_copy_promotion.md for any paid traffic or bio updates.")
                logger.info(f"5. Monitor with sync_sales and re-run for optimization.")

            if res.get("published"):
                logger.info("✅ PUBLISHED: %s", res.get("gumroad_url"))
                successes += 1

                # If published and we have marketing, try to enhance the Gumroad listing with best variant
                if res.get("marketing_dir") and token:
                    try:
                        best_file = Path(res["marketing_dir"]) / "best_gumroad_variant.txt"
                        if best_file.exists():
                            # For demo, we log the suggestion; real update would parse and call Gumroad API
                            logger.info("Gumroad listing enhancement ready (see best_gumroad_variant.txt). Run manual update or extend API.")
                    except Exception as e:
                        logger.warning(f"Could not enhance Gumroad: {e}")
            else:
                logger.info("Files + full marketing ready (not published this cycle). Publish manually or with --publish for next run.")
        except Exception as e:
            logger.error("Cycle %d failed: %s", i+1, e)

    logger.info("Autonomy run complete. %d/%d published. %d marketing packages created.", successes, args.cycles, marketed)
    logger.info("Next step for money: Deploy the assets from the marketing/ folder.")

    # Bonus: Autonomous post-run optimization if sales data available
    if args.marketing and token:
        logger.info("Attempting autonomous sales sync + marketing re-optimization...")
        try:
            updated = sync_gumroad_sales(token)
            logger.info(f"Synced sales for {updated} products.")
            suggestions = analyze_top_performers_and_suggest()
            logger.info("Strategist + marketing suggestions for next cycles:")
            for s in suggestions[:3]:
                logger.info(f"  - {s}")
        except Exception as e:
            logger.info(f"Post-run sync skipped: {e}")

if __name__ == "__main__":
    main()
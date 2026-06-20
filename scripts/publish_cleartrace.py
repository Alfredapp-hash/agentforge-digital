#!/usr/bin/env python3
"""Publish ClearTrace Gumroad draft (or create if missing)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from agentforge_main import create_gumroad_product, GUMROAD_API, _retry_request  # noqa: E402

LISTING = ROOT / "products/clear-trace/GUMROAD_LISTING.txt"
ZIP_PATH = ROOT / "products/clear-trace.zip"


def parse_listing(path: Path) -> tuple[str, int, str]:
    text = path.read_text(encoding="utf-8")
    title = "ClearTrace Privacy Ops Playbook + Agent Builder Kit"
    price_cents = 4900
    description = text
    for line in text.splitlines():
        if line.startswith("TITLE:"):
            title = line.split(":", 1)[1].strip().split("·")[0].strip()
        elif line.startswith("PRICE:"):
            try:
                price_cents = int(float(line.split(":", 1)[1].strip()) * 100)
            except ValueError:
                pass
        elif line.startswith("DESCRIPTION:"):
            idx = text.index("DESCRIPTION:")
            description = text[idx + len("DESCRIPTION:") :].strip()
            break
    return title, price_cents, description


def find_existing(token: str) -> dict | None:
    headers = {"Authorization": f"Bearer {token}"}
    resp = _retry_request("GET", f"{GUMROAD_API}/products", headers=headers)
    if resp.status_code != 200:
        return None
    body = resp.json()
    for product in body.get("products", []):
        name = (product.get("name") or "").lower()
        if "cleartrace" in name or "clear trace" in name:
            return product
    return None


def publish_existing(token: str, product_id: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    resp = _retry_request(
        "PUT",
        f"{GUMROAD_API}/products/{product_id}",
        headers=headers,
        data={"published": "true"},
    )
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"Gumroad publish failed {resp.status_code}: {resp.text}")
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"Gumroad publish failed: {body}")
    return body.get("product", {})


def main() -> int:
    token = os.getenv("GUMROAD_ACCESS_TOKEN", "").strip()
    if not token:
        print("GUMROAD_ACCESS_TOKEN missing in .env")
        return 1

    if not ZIP_PATH.exists():
        print(f"Missing zip: {ZIP_PATH} — run python scripts/package_products.py")
        return 1

    existing = find_existing(token)
    if existing:
        product_id = existing["id"]
        if existing.get("published"):
            print(f"Already live: {existing.get('short_url') or existing.get('url')}")
            return 0
        product = publish_existing(token, product_id)
        print(f"Published: {product.get('short_url') or product.get('url')}")
        return 0

    title, price_cents, description = parse_listing(LISTING)
    result = create_gumroad_product(
        title=title,
        description=description,
        price_cents=price_cents,
        gumroad_token=token,
        file_path=str(ZIP_PATH),
        publish=True,
    )
    print(f"Created and published: {result['gumroad_url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
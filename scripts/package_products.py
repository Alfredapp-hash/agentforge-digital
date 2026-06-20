#!/usr/bin/env python3
"""Package all sellable products into Gumroad-ready zips."""

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_NAMES = {".DS_Store", "__pycache__"}


def zip_dir(source: Path, dest_zip: Path, arc_prefix: str = "") -> Path:
    dest_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(source.rglob("*")):
            if not f.is_file() or f.name in SKIP_NAMES or f.suffix == ".zip":
                continue
            if "marketing" in f.parts and source.name.startswith(("agent-", "mcp-")):
                continue  # keep premium product zips lean; marketing ships separately
            arc = Path(arc_prefix) / f.relative_to(source) if arc_prefix else f.relative_to(source)
            zf.write(f, arcname=str(arc))
    return dest_zip


def main():
    packaged = []

    premium = [
        ("products/mcp-tool-pack-10-crews", "products/mcp-tool-pack-10-crews.zip"),
        ("products/agent-ops-dashboard-notion", "products/agent-ops-dashboard-notion.zip"),
        ("products/agent-stack-solo-builders", "products/agent-stack-solo-builders.zip"),
        ("products/clear-trace", "products/clear-trace.zip"),
    ]
    for src_rel, zip_rel in premium:
        src = ROOT / src_rel
        dest = ROOT / zip_rel
        zip_dir(src, dest)
        packaged.append(dest)

    for lib_dir in sorted((ROOT / "prompt_libraries").iterdir()):
        if not lib_dir.is_dir() or lib_dir.name == "__pycache__":
            continue
        if not (lib_dir / "product.md").exists():
            continue
        dest = ROOT / "prompt_libraries" / f"{lib_dir.name}.zip"
        zip_dir(lib_dir, dest)
        packaged.append(dest)

    print("Packaged:")
    for p in packaged:
        kb = p.stat().st_size / 1024
        print(f"  {p.relative_to(ROOT)} ({kb:.1f} KB)")


if __name__ == "__main__":
    main()

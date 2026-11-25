"""Build roku/data/recipes.json: the recipe book as the Roku app reads it.

    python build_roku.py

Same source as the web page (recipes.py via build_web.derive), minus the
combination grid, which does not read on a TV across the room. The file is
committed so `node scripts/build.mjs` can zip the app without Python, and
tests/test_roku.py fails if it is stale.
"""
from __future__ import annotations

import json
from pathlib import Path

from build_web import derive
from recipes import RECIPES

HERE = Path(__file__).parent
OUT = HERE / "roku" / "data" / "recipes.json"
FIELDS = ("name", "category", "serves", "subtitle", "prep",
          "ingredients", "steps", "notes")


def build() -> str:
    book = [{k: derive(r)[k] for k in FIELDS} for r in RECIPES]
    return json.dumps({"recipes": book}, ensure_ascii=False, indent=1) + "\n"


if __name__ == "__main__":
    text = build()
    OUT.write_text(text, encoding="utf-8")
    print(f"{len(RECIPES)} recipes -> {OUT} ({len(text.encode()):,} bytes)")

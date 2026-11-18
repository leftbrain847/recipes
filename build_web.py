"""Build web/index.html: the phone-first recipe book, data inlined.

    python build_web.py

Reads the recipes from recipes.py, derives what the page needs, and writes the
JSON into web/template.html's #recipe-data block. The data is inlined rather
than fetched as a sibling file because the published page runs in a sandboxed
frame where a same-origin fetch is not reliable, and because a cook with no
signal should still be able to open it.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from recipes import COOK, RECIPES

HERE = Path(__file__).parent
TEMPLATE = HERE / "web" / "template.html"
PAGE = HERE / "web" / "index.html"
DATA_BLOCK = re.compile(
    r'(<script type="application/json" id="recipe-data">).*?(</script>)', re.S)


def grid(rec: dict) -> list[dict]:
    """The combination grid as rows of cells: {"span", "text"}, or None where a
    cell above spans down over this one."""
    rows, ncols = rec["rows"], rec["n_step_cols"]
    covered = set()
    for r, (_, cells) in enumerate(rows):
        for col, span, _ in cells:
            covered.update((rr, col) for rr in range(r + 1, r + span))

    out = []
    for r, (ing, cells) in enumerate(rows):
        at = {col: {"span": span, "text": text or ""} for col, span, text in cells}
        out.append({"ing": ing, "cells": [
            None if (r, col) in covered else at.get(col, {"span": 1, "text": ""})
            for col in range(2, 2 + ncols)]})
    return out


def derive(rec: dict) -> dict:
    """One recipe, shaped for the page.

    `steps` comes from COOK, never from the grid. A grid column is combination
    depth, not elapsed time, so flattening by column yields impossible orders.
    """
    name = rec["name"]
    if name not in COOK:
        raise SystemExit(
            f"no cook order written for {name!r} — add it to COOK in recipes.py")
    return {
        "name": name,
        "category": rec["category"],
        "serves": rec["serves"],
        "blurb": rec["blurb"],
        "subtitle": rec["subtitle"],
        "prep": rec["prep"],
        "ingredients": [ing for ing, _ in rec["rows"]],
        "steps": list(COOK[name]),
        "grid": grid(rec),
        "ncols": rec["n_step_cols"],
        "notes": rec["notes"],
    }


def build() -> str:
    data = {"recipes": [derive(r) for r in RECIPES]}
    blob = json.dumps(data, ensure_ascii=False)
    page, n = DATA_BLOCK.subn(
        lambda m: m.group(1) + "\n" + blob + "\n" + m.group(2),
        TEMPLATE.read_text(), count=1)
    if n != 1:
        raise SystemExit(f"{TEMPLATE}: no #recipe-data block to fill")
    return page


if __name__ == "__main__":
    page = build()
    PAGE.write_text(page)
    print(f"{len(RECIPES)} recipes -> {PAGE} ({len(page):,} bytes)")
    for r in RECIPES:
        d = derive(r)
        print(f"  {d['name']:24} {len(d['ingredients']):2} ing  "
              f"{len(d['steps']):2} steps  {len(d['notes']):2} notes")

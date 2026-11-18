"""The recipe data and the page build.

The guards here are the two things that have actually gone wrong: a recipe
shipping without a written cook order (the grid cannot supply one), and the
page shipping an external font or script, which the index's publish gate
refuses — and one refused page holds back the whole homepage, not just its
own tile.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_web  # noqa: E402
from recipes import COOK, RECIPES  # noqa: E402

NAMES = [r["name"] for r in RECIPES]


def test_every_recipe_has_a_cook_order():
    """COOK is the only source of the Steps view; a recipe without one has no
    usable instructions, so the build must fail loudly rather than infer them."""
    assert [n for n in NAMES if n not in COOK] == []


def test_no_orphan_cook_orders():
    assert [n for n in COOK if n not in NAMES] == []


def test_recipe_names_are_unique():
    assert len(NAMES) == len(set(NAMES))


@pytest.mark.parametrize("rec", RECIPES, ids=NAMES)
def test_required_fields(rec):
    for field in ("name", "category", "serves", "blurb", "subtitle",
                  "prep", "rows", "notes", "n_step_cols"):
        assert rec[field] or rec[field] == 0, f"{rec['name']}: empty {field}"
    assert isinstance(rec["serves"], int) and rec["serves"] > 0


@pytest.mark.parametrize("rec", RECIPES, ids=NAMES)
def test_grid_cells_stay_inside_the_grid(rec):
    """A cell may not span past the last ingredient row or past the last step
    column. Adding an ingredient without widening the spans that run down the
    right-hand side silently drops cells."""
    rows, ncols = rec["rows"], rec["n_step_cols"]
    for r, (_, cells) in enumerate(rows):
        for col, span, _ in cells:
            assert 2 <= col < 2 + ncols, f"{rec['name']} row {r}: column {col} out of range"
            assert r + span <= len(rows), (
                f"{rec['name']} row {r}: span {span} runs past the last ingredient")


@pytest.mark.parametrize("rec", RECIPES, ids=NAMES)
def test_no_two_cells_claim_the_same_square(rec):
    rows = rec["rows"]
    taken: set[tuple[int, int]] = set()
    for r, (_, cells) in enumerate(rows):
        for col, span, _ in cells:
            for rr in range(r, r + span):
                assert (rr, col) not in taken, (
                    f"{rec['name']}: two cells claim row {rr}, column {col}")
                taken.add((rr, col))


@pytest.mark.parametrize("rec", RECIPES, ids=NAMES)
def test_derive_keeps_every_ingredient_and_step(rec):
    d = build_web.derive(rec)
    assert d["ingredients"] == [ing for ing, _ in rec["rows"]]
    assert d["steps"] == list(COOK[rec["name"]])
    assert len(d["grid"]) == len(rec["rows"])
    for row in d["grid"]:
        assert len(row["cells"]) == rec["n_step_cols"]


def test_page_builds_and_data_round_trips():
    page = build_web.build()
    blob = re.search(
        r'<script type="application/json" id="recipe-data">(.*?)</script>',
        page, re.S).group(1)
    data = json.loads(blob)
    assert [r["name"] for r in data["recipes"]] == NAMES


def test_page_loads_nothing_from_outside():
    """The publish gate (index's site_check.py) refuses any third-party script,
    stylesheet or font, and one refused page holds back the entire homepage.
    This is the check that would have caught the Google Fonts links."""
    hosts = set(re.findall(r'https?://([a-zA-Z0-9.-]+)', build_web.build()))
    assert hosts == set(), f"page would be refused at publish: {sorted(hosts)}"


def test_built_page_on_disk_is_current():
    """web/index.html is committed because the index reads it from this repo at
    refresh time, so a stale copy publishes stale recipes."""
    on_disk = Path(build_web.PAGE)
    assert on_disk.exists(), "run: python build_web.py"
    assert on_disk.read_text() == build_web.build(), (
        "web/index.html is out of date — run: python build_web.py")

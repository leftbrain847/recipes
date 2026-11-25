"""The Roku app's data file: committed, so it must match recipes.py."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_roku  # noqa: E402
from recipes import COOK, RECIPES  # noqa: E402


def test_roku_data_on_disk_is_current():
    assert build_roku.OUT.read_text(encoding="utf-8") == build_roku.build(), (
        "roku/data/recipes.json is out of date - run: python build_roku.py")


def test_roku_data_has_every_recipe_and_step():
    book = json.loads(build_roku.build())["recipes"]
    assert [r["name"] for r in book] == [r["name"] for r in RECIPES]
    for r in book:
        assert r["steps"] == COOK[r["name"]]
        assert set(r) == set(build_roku.FIELDS)


def test_roku_data_has_no_urls():
    """The package gate refuses any http(s) URL in the app's code or data."""
    assert "http://" not in build_roku.build() and "https://" not in build_roku.build()


def test_roku_lists_are_never_empty():
    """The app has a page or row for each entry; an empty list would leave a tab blank."""
    for r in json.loads(build_roku.build())["recipes"]:
        for field in ("ingredients", "steps", "notes"):
            assert r[field], f"{r['name']}: no {field}"

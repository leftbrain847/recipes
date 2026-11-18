# recipes

A personal recipe book in Cooking for Engineers format — ingredients down the
left, merged cells bracketing the steps that combine them — rebuilt so it is
usable from a phone at the stove.

Each recipe carries four views: the written **cook order** with quantities
inline, a checkable **ingredient** list, the original combination **grid**, and
**notes** arguing with the source recipe where it is wrong.

## Why the steps are written out by hand

The grid says what combines with what. It does not say *when*: a column is
combination depth, not elapsed time, so two branches sitting in the same column
can happen twenty minutes apart. Deriving the step order from column position
produced instructions like "pour in the noodle water" before "boil the
noodles". `COOK` in `recipes.py` holds a written order per recipe, and
`build_web.py` refuses to build a recipe that lacks one.

## Layout

| file | what it is |
|---|---|
| `recipes.py` | all the data — `RECIPES` (grids) and `COOK` (cook orders). No imports, no side effects. |
| `build_web.py` | builds `web/index.html` from `recipes.py` + `web/template.html` |
| `build_xlsx.py` | builds the Excel workbook from the same data |
| `web/template.html` | the page shell; `build_web.py` fills its `#recipe-data` block |
| `web/index.html` | the built page, committed because the index reads it from here |

Adding or changing a recipe means editing `recipes.py` and running
`build_web.py`. Both outputs come from that one source, so they cannot drift.

## Run
```
python build_web.py                 # -> web/index.html
python build_xlsx.py [out.xlsx]     # -> recipe_book.xlsx (needs openpyxl)
```

## Test
```
pytest -q        # recipe data, grid geometry, and the publish-gate guard
node --test      # repo scaffold tests
```

`test_page_loads_nothing_from_outside` is the one that matters most: the
index's `site_check.py` refuses any page that loads a third-party script,
stylesheet or font, and a refused page holds back the **whole** homepage, not
just its own tile. That is why the page uses system fonts and inlines its data
instead of fetching a sibling JSON file.

## Deployed
- Live: on the Agentic Builds homepage under Tools, from `web/index.html`
  (`showcase:` entry `recipe_book` in `leftbrain847/index`)
- Day snapshot: none. This is not a sprint-day build.

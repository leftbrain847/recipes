# recipes

A personal recipe book in Cooking for Engineers format — ingredients down the
left, merged cells bracketing the steps that combine them — rebuilt so it is
usable from a phone at the stove.

It also runs on a Roku TV as a sideloaded app (`roku/`), built and
security-checked the same way as `leftbrain847/kart_roku`.

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
| `build_roku.py` | builds `roku/data/recipes.json` (the Roku app's copy of the book, no grid) |
| `roku/` | the Roku app: `manifest`, `source/*.brs` (BrightScript, roScreen/Draw2D), `data/`, `images/` |
| `scripts/build.mjs`, `zip.mjs`, `check-package.mjs` | zip the Roku app and run its security gate (copied from kart_roku; settings in `scripts/package.config.json`) |
| `scripts/art/roku_icons.py` | draws the Roku icons and splash (`python3 scripts/art/roku_icons.py roku/images`, needs Pillow) |

Adding or changing a recipe means editing `recipes.py` and running
`build_web.py` and `build_roku.py`. Every output comes from that one source,
and the tests fail if a committed output is stale.

## Run
```
python build_web.py                 # -> web/index.html
python build_xlsx.py [out.xlsx]     # -> recipe_book.xlsx (needs openpyxl)
python build_roku.py                # -> roku/data/recipes.json
npm ci && npm run build             # -> dist/recipes_roku.zip
npm run check                       # Roku security gate: allowed files only, no network APIs, no secrets
```

### On the Roku
Sideload `dist/recipes_roku.zip` (or the latest `roku-v*` release): on the remote
press Home ×3, Up ×2, Right, Left, Right, Left, Right to enable developer mode;
open the Roku's IP in a browser on the same Wi-Fi, sign in as `rokudev`, upload
the zip, Install. **A Roku holds one sideloaded app at a time**, so this
replaces Kart (and installing Kart again replaces this).

| Remote | Recipe list | In a recipe |
|---|---|---|
| Up / Down | choose a recipe | Steps: previous / next step. Ingredients, Notes: move |
| OK / Play | open it | Steps: next step. Ingredients: check off |
| Left / Right | | switch tab (Steps, Ingredients, Notes) |
| Rew / Fwd | | Steps: previous / next. Lists: jump to top / bottom |
| Back | exit | back to the recipe list |

The Steps tab opens on "Before you start" and remembers the step you reached
per recipe, so reopening the app resumes there. Simulator:
`npx brs-cli -n dist/recipes_roku.zip` (add `-k autotest=1` for the scripted pass).

## Test
```
pytest -q        # recipe data, grid geometry, the publish-gate guard, Roku data is current
npm test         # Roku: brighterscript checks, book unit tests and a scripted pass through
                 # every recipe/tab in the brs-cli simulator, zip + security gate; scaffold tests
```

`test_page_loads_nothing_from_outside` is the one that matters most: the
index's `site_check.py` refuses any page that loads a third-party script,
stylesheet or font, and a refused page holds back the **whole** homepage, not
just its own tile. That is why the page uses system fonts and inlines its data
instead of fetching a sibling JSON file.

## Deployed
- Live: on the Agentic Builds homepage under Tools, from `web/index.html`
  (`showcase:` entry `recipe_book` in `leftbrain847/index`)
- Roku: GitHub release `roku-v<version>` with `recipes_roku.zip`, built by
  `.github/workflows/release.yml` after tests and the security gate pass. Bump
  `build_version` in `roku/manifest` to publish a new one (new recipes included).
- Day snapshot: none. This is not a sprint-day build.

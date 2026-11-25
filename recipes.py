"""The recipe book's data. No imports, no side effects: both builders read this.

RECIPES holds each recipe as a combination grid (ingredients down the left, merged
cells bracketing the steps that combine them). COOK holds the written cook order,
which the grid cannot express: a column is combination depth, not elapsed time, so
two branches in the same column can happen twenty minutes apart.
"""

# ===========================================================================
# Recipes
# ===========================================================================
RECIPES = []


def recipe(name, category, serves, blurb, subtitle, prep, rows, notes, n_step_cols):
    RECIPES.append(dict(name=name, category=category, serves=serves, blurb=blurb,
                        subtitle=subtitle, prep=prep, rows=rows, notes=notes,
                        n_step_cols=n_step_cols))


# ---------------- Smash Burgers ----------------
recipe(
    "Smash Burgers", "Beef / griddle", 2,
    "Oklahoma onion, double-stacked 2 oz patties.",
    "Double-stacked 2 oz patties, smashed through paper-thin onion. Makes 2 burgers.",
    ["Slice onion paper-thin — mandoline if you have one",
     "Divide beef into four loose 2 oz (55 g) balls; keep cold, do NOT season",
     "Heat cast iron or carbon steel over high until it just smokes"],
    [
        ("1 tsp (5 mL) neutral oil", [
            (2, 1, "wipe into\nhot pan"),
            (3, 1, None),
            (4, 5, "sear\nundisturbed\n90 sec\n(edges lacy)\n\nscrape hard,\nflip — onion\nside down"),
            (5, 6, "melt cheese\non 2 of the\n4 patties\n30–45 sec"),
            (6, 9, "stack\n2 patties\nper bun\n\nserve\nimmediately"),
        ]),
        ("8 oz (225 g) ground chuck, 80/20, cold", [
            (2, 1, "place balls in\npan, spaced"),
            (3, 2, "smash straight\nthrough the onion\nto 1/8 in thick"),
        ]),
        ("1/2 medium yellow onion, sliced paper-thin", [
            (2, 1, "pile a handful\non each ball"),
        ]),
        ("1/2 tsp (3 g) kosher salt", [
            (2, 2, None),
            (3, 2, "season the\nonion side\n(facing up)"),
        ]),
        ("1/4 tsp (0.5 g) black pepper", []),
        ("2 slices American cheese", [
            (2, 1, None), (3, 1, None), (4, 1, None),
        ]),
        ("2 soft potato or sesame buns", [
            (2, 1, "toast cut\nsides"),
            (3, 3, None),
            (4, 3, None),
            (5, 3, "spread and\nlayer on\nbottom bun"),
        ]),
        ("2 Tbs (30 mL) burger sauce", [
            (2, 2, None),
        ]),
        ("4 dill pickle slices", []),
    ],
    [
        "The onion is never cooked separately. It goes on raw, you smash through it, and it fuses into the meat. After the flip it sits underneath, frizzling in beef fat.",
        "Onion thinness is the whole trick. Thick slices won't cook through and will keep the patty from fusing to the pan.",
        "Smash in the first few seconds, before the proteins set. After the flip, never press again — that only squeezes out juice.",
        "Get the spatula fully under the crust on the flip. A stiff metal spatula matters more than any other tool here.",
        "If four patties won't fit with room to smash, cook two rounds; the first pair rests on a bun bottom.",
        "Burger sauce: mayo, ketchup, a little mustard, minced pickle.",
        "Apartment warning: hood on full, window open.",
    ],
    5,
)

# ---------------- Shrimp Burgers ----------------
recipe(
    "Shrimp Burgers", "Seafood / pan-fry", 2,
    "Hybrid paste-and-dice bind, Southeast Asian aromatics.",
    "Hybrid paste-and-dice bind, Southeast Asian aromatics. Makes 2 burgers.",
    ["Thaw 12 oz (340 g) raw shrimp; peel, devein, and press between towels until surface-dry",
     "Split the shrimp: 4 oz (115 g) for the paste, 8 oz (225 g) to dice",
     "Line a plate with parchment and clear fridge space for the chill"],
    [
        ("4 oz (115 g) of the shrimp, for the paste", [
            (2, 1, "purée\nsmooth"),
            (3, 2, "work hard 60 sec\nuntil sticky and\nglossy"),
            (4, 10, "fold together\ngently\n\ndo not\novermix"),
            (5, 10, "chill 30 min\n\nform 2 patties\n3/4 in thick"),
            (6, 11, "fry 2–3 min\nper side\n\npull at\n120–125°F\n\nrest 2 min"),
            (7, 14, "assemble\n\nserve\nimmediately"),
        ]),
        ("1/2 tsp (3 g) kosher salt", [(2, 1, None)]),
        ("8 oz (225 g) of the shrimp", [
            (2, 1, "dice pea-size\nor smaller"),
            (3, 1, None),
        ]),
        ("1 large egg, beaten", [
            (2, 7, "whisk\ntogether"),
            (3, 7, None),
        ]),
        ("1 Tbs (15 g) mayonnaise", []),
        ("1 Tbs (8 g) cornstarch", []),
        ("2 scallions, thinly sliced", []),
        ("1 tsp (2 g) grated fresh ginger", []),
        ("1 clove garlic, grated", []),
        ("1/4 tsp (0.5 g) white pepper", []),
        ("2 tsp (10 mL) neutral oil", [
            (2, 1, "film the pan,\nmedium-high"),
            (3, 1, None), (4, 1, None), (5, 1, None),
        ]),
        ("2 soft potato or brioche buns", [
            (2, 1, "toast cut\nsides"),
            (3, 3, None), (4, 3, None), (5, 3, None),
            (6, 3, "spread and\nlayer on\nbottom bun"),
        ]),
        ("2 Tbs (30 mL) mayo + lime juice + sriracha", [(2, 2, None)]),
        ("1 cup shredded cucumber, cilantro and mint, dressed with lime", []),
    ],
    [
        "The paste is the binder. Salting the puréed third and working it hard dissolves myosin into a sticky sol — that is what holds the patty together and gives it the springy bounce of a shrimp ball. The egg and cornstarch are insurance, not the structure.",
        "Do not purée more than a third or you lose the diced bite entirely and end up with a shrimp cake.",
        "Water is the enemy. Frozen shrimp are usually phosphate-treated and hold a lot of it — press between towels harder than feels reasonable, and pat the formed patty dry again right before it hits the pan.",
        "The 30-minute chill is not optional. A warm patty falls apart on the flip.",
        "Do not smash these. Shrimp is lean and wet; smashing squeezes out moisture, sticks to the pan, and tears on the flip. A formed 3/4 in patty in a shallow film of oil is the move.",
        "Pull at 120–125°F and let carryover finish it. Shrimp goes from perfect to rubber in about 20 seconds.",
        "Use a wide fish spatula and flip once, decisively.",
        "Lime goes on at the plate, never in the mix — acid starts curing raw shrimp and turns the texture chalky.",
        "Low-sodium swap: 1 tsp fish sauce in place of half the kosher salt buys more flavor per mg of sodium.",
        "Egg white only (skip the yolk) makes a slightly drier, firmer patty if the mix feels loose.",
    ],
    6,
)

# ---------------- Swai Fillets ----------------
recipe(
    "Swai Fillets", "Seafood / pan-fry", 4,
    "Cornmeal crust, chilled, then fried and finished covered.",
    "Cornmeal crust, chilled, then pan-fried and finished covered. Serves 4. "
    "Prep 10 min / chill 30 min / cook 20 min.",
    ["Pat the fillets dry before seasoning",
     "Set up two shallow bowls: spice mix and cornmeal"],
    [
        ("2 tsp red pepper flakes", [
            (2, 4, "combine\nin a bowl"),
            (3, 6, "season the fish\nwith the spice mix,\nthen press into\nthe cornmeal\nto coat"),
            (4, 6, "wrap in\nplastic\n\nchill\n30 min"),
            (5, 7, "fry in the\nhot oil\n\n~5 min\nper side,\nuntil browned"),
            (6, 8, "add water\n\nsimmer covered\n~10 min,\nflipping,\nuntil it flakes"),
        ]),
        ("1 tsp seafood seasoning (Old Bay or similar)", []),
        ("1 tsp garlic powder", []),
        ("salt and ground black pepper, to taste", []),
        ("1 cup (160 g) cornmeal", [(2, 1, "spread in a\nshallow bowl")]),
        ("4 fillets swai, 4 oz (115 g) each", [(2, 1, None)]),
        ("2 Tbs (30 mL) canola oil", [
            (2, 1, "heat in skillet,\nmedium"),
            (3, 1, None), (4, 1, None),
        ]),
        ("1/4 cup (60 mL) water", [
            (2, 1, None), (3, 1, None), (4, 1, None), (5, 1, None),
        ]),
    ],
    [
        "Source: recipe by Bonnie M Goodwin, published on Allrecipes. Transcribed as written — the notes below are changes to consider, not changes I made.",
        "The covered water-simmer will undo the crust you just built. Steam softens cornmeal fast. If you want the crisp coating the recipe promises, skip the water entirely and just fry to done.",
        "Swai fillets run thin — often well under 3/4 in. Five minutes a side plus ten minutes covered is far more heat than they need; that is 20 minutes of cooking on a fish that is done in six to eight. Fry 3–4 min per side and pull at 140°F.",
        "The 30-minute chill is doing real work here: it sets the coating so it does not slide off in the pan. Keep that step.",
        "2 tsp red pepper flakes across four fillets is assertive. Halve it on the first run if serving anyone heat-shy.",
        "Old Bay is roughly 300 mg sodium per 1/4 tsp. Salt-free Old Bay exists, or use the celery-seed / dry-mustard / paprika profile without the salt and season the fish directly.",
        "Cornmeal browns better than flour but burns faster. Medium heat, not medium-high, and wipe the pan between batches.",
        "Swai is farmed pangasius and quite mild and soft. Catfish, tilapia, or basa all drop into this recipe unchanged.",
    ],
    6,
)

# ---------------- Shrimp & Egg Noodles ----------------
recipe(
    "Shrimp & Egg Noodles", "Seafood / pasta", 2,
    "Buttery garlic-Parmesan pan sauce; stock + vinegar in place of wine.",
    "Buttery garlic-Parmesan pan sauce, no wine. Serves 2. About 25 minutes.",
    ["Start the noodles first \u2014 their water is an ingredient here, not a byproduct",
     "Pat the shrimp bone-dry and grate the Parmesan fine (Microplane, not shreds)",
     "Have everything cut and within reach — the sauce comes together in under 5 minutes"],
    [
        ("12 oz (340 g) large shrimp, peeled, patted bone-dry", [
            (2, 3, "season"),
            (3, 4, "sear 90 sec\nper side\n\nremove to\na plate"),
            (4, 11, "add the noodles\nand 1/2 cup\nnoodle water\n\ntoss over\nlow heat"),
            (5, 13, "OFF the heat:\n\nadd the butter and\ncheese in handfuls,\ntossing constantly\nuntil glossy"),
            (6, 15, "return the\nshrimp\n\nadd lemon\nand parsley"),
            (7, 15, "loosen with\nnoodle water\nto a glossy\nsauce\n\nserve\nimmediately"),
        ]),
        ("1/2 tsp (3 g) kosher salt", []),
        ("1/4 tsp (0.5 g) black pepper", []),
        ("1 Tbs (15 g) butter, for the pan", [
            (2, 1, "melt in skillet,\nmedium-high"),
        ]),
        ("4 cloves garlic, thinly sliced", [
            (2, 2, "add to the\nsame pan"),
            (3, 2, "sizzle 45 sec\nuntil fragrant,\nnot browned"),
        ]),
        ("1/4 tsp red pepper flakes", []),
        ("2 tsp (10 mL) white wine vinegar", [
            (2, 2, "pour in"),
            (3, 2, "reduce by half,\nscraping up\nthe fond"),
        ]),
        ("1/2 cup (120 mL) reserved noodle water \u2014 or unsalted stock", []),
        ("2 qt (2 L) water + 2 tsp (6 g) kosher salt \u2014 less water than usual, on purpose", [
            (2, 2, "boil the noodles\n1 min under\npackage time"),
            (3, 3, None),
        ]),
        ("8 oz (225 g) wide egg noodles", []),
        ("1 cup (240 mL) reserved noodle water \u2014 scoop extra", [
            (2, 1, "scoop out before\ndraining"),
        ]),
        ("3 Tbs (45 g) cold unsalted butter, cubed", [
            (2, 2, None), (3, 2, None), (4, 2, None),
        ]),
        ("1 oz (30 g) Parmigiano-Reggiano, grated fine", []),
        ("1 Tbs (15 mL) lemon juice", [
            (2, 2, None), (3, 2, None), (4, 2, None), (5, 2, None),
        ]),
        ("2 Tbs (8 g) flat-leaf parsley, chopped", []),
    ],
    [
        "No wine, no problem — but lemon juice alone is the wrong substitute. Wine brings acid, a little sweetness, and aromatic depth. The stock-plus-vinegar combination covers the body and the acid, cooked down early so the raw vinegar edge burns off, and the lemon goes in at the end for brightness. Dry vermouth is the closest single-bottle stand-in if you ever want to keep one around; it keeps for months in the fridge, unlike wine.",
        'NO STOCK NEEDED. The half cup of liquid that cooks down with the vinegar is reserved noodle water by default: starchy, already seasoned, and sitting right there. Starch is the thing this sauce is short on, so it is arguably the better choice. Unsalted chicken or shrimp stock buys a little more savory depth if you happen to have it. To close that gap without stock, melt 1/4 tsp mushroom powder or a small squeeze of anchovy paste into the garlic just before the liquid goes in \\u2014 one or the other, not both. If the shrimp were shell-on, simmering the shells in a cup of water for 10 minutes beats chicken stock here outright.',
        'HOW MUCH WATER: about 2 qt (2 L) for 8 oz of noodles — deliberately less than the usual 4 qt, because the sauce lives on the starch concentration in the reserved water and egg noodles throw little of it to begin with. Boil them in a big pot and the 3/4 cup you scoop out is close to plain water. Salt it lightly, 2 tsp kosher rather than the usual tablespoon: unlike potato water this goes INTO the dish, and an ounce of Parmesan lands on top of it. Taste and finish-season at the end. Stir in the first 30 seconds so they do not clump.',
        "Egg noodles are the real variable here. They are softer, eggier, and release far less starch than durum pasta, so the usual pasta-water emulsion is weaker. Pull them a full minute under package time, save more water than feels necessary, and expect to work the butter in harder.",
        "Add the Parmesan off the heat, in handfuls, tossing the whole time. Over direct heat the cheese proteins tighten and the fat breaks out — you get a greasy, stringy pan instead of a sauce.",
        "Cold butter, cubed, added off heat. Melted butter poured in will not emulsify; cold butter releases its fat slowly enough to stay suspended.",
        "Shrimp cook in about three minutes total. Sear them first, pull them out, and let them finish in the residual heat of the sauce at the end — anything else overcooks them while the sauce comes together.",
        "Bone-dry shrimp or no sear. Any surface water steams and you get grey shrimp instead of browned ones.",
        "Sodium: the Parmesan carries most of it (roughly 400 mg per ounce), so use unsalted stock and go light on the salt in the shrimp seasoning. The cheese, garlic, and fond are the umami early; the lemon is the acid late.",
        "Scale the butter by what you want. 3 Tbs is restrained; 5 Tbs is the version that tastes like a restaurant made it.",
    ],
    6,
)


# ---------------- Sesame Sweet-and-Sour Turkey Meatballs ----------------
recipe(
    "Sesame Turkey Meatballs", "Poultry / baked", 2,
    "Maple-ketchup sweet-and-sour sauce; seared, then baked and broiled.",
    "Maple-ketchup sweet-and-sour sauce, seared then baked. Adapted from Allrecipes. "
    "Serves 2. About 50 minutes.",
    ["Preheat oven to 350°F (175°C)",
     "Have an ungreased glass 9x13-in pan and foil ready",
     "Serve over jasmine rice — start it so it finishes with the bake"],
    [
        ("1/4 cup (60 mL) real maple syrup", [
            (2, 5, "combine in a\nmedium saucepan"),
            (3, 5, "bring to a simmer\n\nsimmer 5 min"),
            (4, 6, "OFF the heat:\nstir in the\nsesame oil\n\nset aside"),
            (5, 6, None),
            (6, 17, "pour the sauce\nevenly over\n\ncover with foil"),
            (7, 17, "bake 350°F\n(175°C)\n20–25 min\ncovered\n\nuncover, broil\n2–3 min\nto glaze"),
        ]),
        ("1/4 cup (60 mL) ketchup", []),
        ("2 Tbs + 2 tsp (40 mL) rice wine vinegar", []),
        ("1 Tbs (15 mL) yellow mustard", []),
        ("1/2 Tbs (5 g) sesame seeds, or more to taste", []),
        ("2 Tbs (30 mL) sesame oil", []),
        ("2 Tbs + 2 tsp sliced green onions", [
            (2, 7, "beat together\nin a mixing bowl\nuntil well mixed"),
            (3, 9, "mix well\nby hand"),
            (4, 9, "scoop into\nuniform meatballs"),
            (5, 10, "sear 2–3 min,\nturning, until\nbrowned on all\nsides — not\ncooked through\n\ntransfer to\nthe pan"),
        ]),
        ("1/2 egg, beaten", []),
        ("2 Tbs (30 mL) low-sodium soy sauce", []),
        ("1/2 tsp minced fresh ginger root", []),
        ("1/4 tsp onion powder", []),
        ("1/8 tsp ground black pepper", []),
        ("1/8 tsp garlic powder", []),
        ("1/2 lb (225 g) ground turkey", [
            (2, 2, "add turkey,\ntop with panko"),
        ]),
        ("1/4 cup (25 g) panko bread crumbs", []),
        ("2 Tbs (30 mL) olive oil", [
            (2, 1, "heat in a skillet,\nmedium-high"),
            (3, 1, None),
            (4, 1, None),
        ]),
        ("1 cup (130 g) carrots, chopped (optional)", [
            (2, 1, "chop"),
            (3, 1, None),
            (4, 1, None),
            (5, 1, "scatter evenly\nbetween the\nmeatballs"),
        ]),
    ],
    [
        'Adapted from Allrecipes recipe 270759, Asian Sesame Sweet-and-Sour Turkey Meatballs. Ingredients and amounts are unchanged; the method is not — see the next two notes.',
        'CHANGED — browning. The original bakes covered 30 min, then uncovered 10. That steams the meatballs; they never brown, and the uncovered stretch is too short and too cool to fix it. The grid above sears them first and finishes under the broiler, with the covered bake cut to 20–25 min because they go in partly cooked.',
        "CHANGED — where the two oils work. The 2 Tbs of olive oil moved out of the sauce and into the skillet, where it does the searing; the 2 Tbs of sesame oil moved to the end, stirred in off the heat. Nothing was added or removed. Toasted sesame oil's aroma compounds are volatile, so simmering it 5 minutes wastes most of what you bought it for, and 4 Tbs of oil in an unthickened sauce just splits and pools under the foil.",
        "The odd fractions (1/6 cup, 1/8 cup, 1/2 egg) are artifacts of the site's serving scaler. Converted to spoons above. For the half egg: beat one whole egg and use half, or use the whole egg and add another tablespoon of panko.",
        "NUTRITION at 2 servings. The site's panel (432 cal / 26 g fat / 35 g carb / 19 g protein) is per serving at 3, so the whole dish is about 1,300 cal, 78 g fat, 105 g carb, 57 g protein. Halved: roughly 650 cal, 39 g fat, 53 g carb, 29 g protein per serving. Add 1 cup cooked jasmine rice and the plate lands near 855 cal, 39 g fat, 98 g carb, 33 g protein.",
        'SODIUM — yes, this needs adjustment now. Estimated from the ingredients (the panel does not list it): about 2,300 mg across the dish, so roughly 1,150 mg per serving at 2 — up by half from the 3-serving split, for the same food. Two ingredients own nearly all of it: 2 Tbs low-sodium soy at ~1,150 mg and 1/4 cup ketchup at ~600 mg. Everything else together is under 550 mg.',
        'The rice makes this worse in one specific way. Plain jasmine rice adds no sodium, so it lowers sodium per calorie — but it also means you spoon up every bit of the pooled sauce instead of leaving some in the pan, so you actually eat more of the sodium than you would without it.',
        'Two fixes, both free on flavor: cut the soy to 1 Tbs and make up the liquid with water (the ginger, green onion and the two powders are carrying that mix, not the salt), and use no-salt-added ketchup. Together that takes the dish from ~2,300 mg to roughly 1,100 — about 550 mg per serving. Cook the rice unsalted and the plate stays there.',
        'Protein-to-calorie is the weak spot at 2 servings: 29 g for 650 calories, and the sauce is roughly 55% of those calories while contributing no protein. Going to 1 lb of turkey (with 1 whole egg and 1/2 cup panko) and leaving the sauce alone gets about 43 g protein for 790 — a better plate if these are dinner rather than a side.',
    ],
    6,
)


# ---------------- Bulk Italian Sausage (turkey) ----------------
recipe(
    "Turkey Italian Sausage", "Poultry / bulk sausage", 8,
    "Bulk sausage from lean ground turkey \u2014 salt-bound, rested overnight.",
    "Multipurpose bulk Italian sausage from 93/7 ground turkey. Makes 1 lb "
    "(about eight 2 oz portions). 15 min work, then a 12\u201324 hr rest.",
    ["Toast the fennel in a dry pan ~60 sec until fragrant, then crack coarsely",
     "Keep the turkey in the fridge until the moment you mix \u2014 cold meat binds, warm meat smears",
     "Weigh the salt if you can: kosher salt brands differ by almost 2x per teaspoon"],
    [
        ("7 g (about 1 1/2 tsp Diamond Crystal) kosher salt", [
            (2, 8, "combine in a\nsmall bowl"),
            (3, 12, "mix hard\n60\u201390 sec\n\nuntil the meat\nturns sticky and\ntacky and clings\nto the bowl"),
            (4, 12, "cover\n\nchill\n12\u201324 hr"),
            (5, 12, "test-fry\na teaspoon\n\nadjust salt\nor heat"),
            (6, 12, "shape\nand cook\n\npizza, patties,\ncrumble or\nmeatballs\n\n(see notes)"),
        ]),
        ("2 tsp (4 g) fennel seed, toasted and cracked", []),
        ("1 tsp (2 g) sweet paprika", []),
        ("1 tsp (3 g) garlic powder", []),
        ("3/4 tsp (1.5 g) coarse black pepper", []),
        ("1/2 tsp (1 g) red pepper flakes (1 1/2 tsp for hot)", []),
        ("1/2 tsp (1 g) dried oregano", []),
        ("1 tsp (2 g) mushroom powder (optional)", []),
        ("1 lb (454 g) ground turkey, 93/7, very cold", [
            (2, 1, "scatter the\nspice mix over"),
        ]),
        ("3 Tbs (40 mL) olive oil", [
            (2, 3, "add"),
        ]),
        ("2 Tbs (30 mL) ice water", []),
        ("1 tsp (5 mL) red wine vinegar", []),
    ],
    [
        "The salt and the rest are the recipe. Mixing hard at 1.5% salt dissolves myosin into a sticky sol; the overnight chill lets it set. That is what turns ground turkey into sausage \u2014 cohesive, springy, holding its juice. Skip the rest and you have seasoned ground turkey that crumbles in the pan. Same mechanism as the paste bind in the shrimp burgers.",
        "Salt is structural here, not seasoning. Below roughly 1.2% by weight the bind does not happen and the texture collapses. 1.5% is 7 g per pound \u2014 about 2,700 mg sodium across the whole batch, or ~335 mg per 2 oz portion. That is at or slightly below commercial Italian sausage, which runs 390\u2013450 mg for the same weight. The mushroom powder is there so you can drop to 1.3% (6 g) without it tasting flat; that is about as low as this goes before texture starts to suffer.",
        "93/7 turkey is the real constraint. A pound holds about 32 g of fat; pork sausage runs 25\u201330% fat, so roughly 115 g. No amount of seasoning closes that gap. The 3 Tbs of olive oil brings the mix to around 15% fat, which is the floor for something that does not read as dry. Do not skip it, and do not leave out the ice water either \u2014 it helps the lean protein hold moisture through cooking.",
        "Always test-fry. A teaspoon flattened in a hot pan tells you about salt and heat level before you have committed a pound of meat and a day of resting.",
        'NO-REST SHORTCUT. If you need it tonight, mix as written — hard, the mechanical work does most of the myosin extraction and the rest only lets it set — then freeze the bowl 15 min and use it. You get maybe half the texture benefit. That is fine for pizza, where the nuggets are loose anyway and the cheese holds them, and bad for patties or meatballs, which need the bind to hold shape. Bump the fennel and red pepper by about a quarter: unrested spice tastes weaker because it has not bloomed into the fat yet.',
        "FOR PIZZA: pinch the raw sausage into pea-to-marble nuggets and scatter them on the pie raw. Do not pre-cook it. At 500\u00b0F+ for 8\u201312 minutes the nuggets cook through, and the fat renders down into the cheese instead of into a skillet you then drain. Pre-browned sausage on a pizza gets cooked twice and tastes like it.",
        "PATTIES: four 4 oz patties, about 3 min per side in a hot pan, pulled at 160\u00b0F. CRUMBLE: brown and break up into tomato sauce, where the rendered fat is the point. MEATBALLS: roll 1 oz balls, sear and finish in sauce.",
        'NO-FENNEL VARIANT. Fennel is what makes this read as Italian sausage and there is no real substitute (caraway is the nearest common one). Without it, drop the fennel, paprika and oregano and use 2 tsp Italian seasoning crushed between your fingers, with the garlic powder up to 1 1/2 tsp and the red pepper to 3/4 tsp. Keep the blend to 2 tsp: most Italian seasoning carries rosemary, sage and thyme, which turn piney and drift toward breakfast sausage if you pour with a heavy hand. Call the result a garlic pizza sausage rather than an Italian one — it is good, it is just not the same thing.',
        "BREAKFAST VARIANT: swap the fennel and oregano for 1 1/2 tsp rubbed sage and 1/4 tsp nutmeg, and add 2 tsp maple syrup. Everything else stays.",
        "Keeps 3 days in the fridge after the rest and 3 months frozen. Portion it before freezing \u2014 a frozen brick of bulk sausage is useless on a weeknight.",
        "Cold meat, cold bowl, cold hands. If the fat warms and smears into the protein the texture goes pasty rather than springy. If the kitchen is warm, chill the bowl first and mix with a stiff spatula instead of your hands.",
    ],
    5,
)


# ---------------- Papas Rellenas ----------------
recipe(
    "Papas Rellenas", "Potato / pan-fry", 4,
    "Cheese-stuffed potato cakes with ham and cilantro.",
    "Cheese-stuffed potato cakes with ham and cilantro. Makes 8 cakes "
    "(4 servings of 2). 45 min plus a 30 min chill.",
    ["Squeeze the cheese into 8 tight pucks and freeze 30 min before you stuff "
     "\u2014 cold cheese melts slower and blows out less",
     "Line a sheet pan with parchment for the formed cakes"],
    [
        ("2 lb (900 g) russet potatoes (about 4 medium), peeled, large chunks", [
            (2, 3, "start in COLD\nwater, bring\nto a boil\n\n15\u201320 min until\na knife slides\nin easily"),
            (3, 3, "drain\n\ndry in the hot pot\n1\u20132 min over\nlow heat\n\nrice or mash\n\u2014 never a\nprocessor"),
            (4, 10, "fold together\njust until combined\n\ndo not overwork\n\ncool 30 min\nin the fridge"),
            (5, 11, "oil your hands\n\ndivide into 8 balls\n\npress a deep well,\nseal a cheese puck\ninside\n\nroll smooth,\nflatten to 3/4 in"),
            (6, 12, "dust both sides"),
            (7, 13, "fry medium\n4\u20135 min per side\nuntil deep gold\n\ndrain on a rack"),
        ]),
        ("2 1/2 qt (2.4 L) cold water \u2014 enough to cover by 1 in", []),
        ("1 Tbs (18 g) kosher salt, for the water", []),
        ("1 tsp (5 g) kosher salt, for the mash", [
            (2, 5, "stir together"),
            (3, 7, None),
        ]),
        ("1 large egg yolk (keep the white)", []),
        ("1/4 cup (32 g) cornstarch", []),
        ("1 tsp (2 g) mushroom powder", []),
        ("1/2 tsp (1 g) white pepper", []),
        ("1/3 cup (15 g) cilantro, chopped fine", [
            (2, 2, "chop"),
        ]),
        ("4 oz (115 g) diced ham, or cooked turkey sausage", []),
        ("6 oz (170 g) low-moisture mozzarella, shredded (about 1 1/2 cups)", [
            (2, 1, "squeeze into 8\ntight pucks,\nfreeze 30 min"),
            (3, 3, None),
            (4, 3, None),
        ]),
        ("2 Tbs (16 g) cornstarch, for dusting", [
            (2, 2, None),
            (5, 2, None),
        ]),
        ("3\u20134 Tbs (45\u201360 mL) neutral oil, for frying", [
            (6, 1, None),
        ]),
    ],
    [
        "A loose use of the name. Papa rellena means stuffed potato, so it fits literally, but the canonical Peruvian and Cuban dish is an oval or ball of potato dough stuffed with picadillo and deep-fried \u2014 not a flat disk of cheese shallow-fried in a few tablespoons of oil. Same family, different dish. Whatever else it is, it is not a pupusa: that is a masa (corn) dough, and the video has it wrong.",
        "WATER IS THE WHOLE PROBLEM, and the video skips all three fixes. Use russets, not waxy potatoes \u2014 high starch, low moisture. After draining, put the potatoes back in the dry hot pot for 1\u20132 minutes over low heat to steam off what boiling put in. And cool the mash completely before forming: warm mash is slack and will not hold a seal. Each of these costs you a minute and each one prevents a cake falling apart in the pan.",
        "HOW MUCH WATER: about 2 1/2 qt (2.4 L) for 900 g of chunks, enough to cover by an inch in a standard 4 qt pot. Start them in COLD water and bring it up together \u2014 chunks dropped into already-boiling water cook from the outside in, and the edges go to mush before the centers are done. The 1 Tbs of salt is roughly 0.7% of that volume; it looks like a lot because most of it goes down the drain.",
        "SAVE NONE OF THE COOKING WATER. Potato water is genuinely useful in bread or for thickening a soup, but this is the one dish where it is the enemy: the whole recipe is an argument for getting water out of the potato, and starchy water puts water and free starch back in. If the mash somehow comes out too dry to form \u2014 over-dried in the pot, or very old potatoes \u2014 fix it with a teaspoon of the egg white left over from the yolk, not with cooking water.",
        "Never a food processor, blender or stand mixer. Overworking ruptures the starch cells and releases amylopectin, and the mash turns to glue \u2014 irreversibly. A ricer is best, a hand masher is fine, and you stop the moment it comes together.",
        "FREEZE THE CHEESE \u2014 the single best trick here. Cold cheese melts slower, so the cake sets before the filling liquefies and blowouts mostly stop. With shredded cheese you have to compress it first: about 3 Tbs packed shreds per cake (3/4 oz / 21 g), squeezed hard in your palm into a 1 in disk, then frozen 30 min \u2014 longer than a cube needs, since a puck is less dense. Loose shreds have far more surface area than a cube, so they liquefy sooner, and they trap air pockets that turn to steam. Compressing fixes both.",
        "Cheese choice. A block beats bagged shreds, which are coated in cellulose and potato starch to keep them separate \u2014 that coating gives a grainier melt and a weaker pull, and nothing removes it (rinsing just adds the water you spent the whole recipe getting out). Low-moisture mozzarella or Oaxaca/quesillo either way. Fresh mozzarella is far too wet: it will burst the cake and steam the inside soggy.",
        "Cornstarch, not flour, and do not skip it. 1/4 cup per 2 lb of potato is about the floor for a dough that seals and holds. No gluten means a crisper cake and a cleaner potato flavor; flour makes it bready and dulls both.",
        "Medium heat, not high. The cheese needs time to melt through a 3/4 in cake. On high you get a dark crust around a cold center with an unmelted puck in it.",
        "Check every cake for cracks before it hits the pan. One crack is one blowout. Roll it smooth again and re-flatten.",
        "PROTEIN. As written this is about 220 cal and 10 g protein per cake, so a 2-cake serving runs roughly 440 cal / 20 g \u2014 carb-dominant for a main. Doubling the ham, or swapping in the bulk turkey sausage from the other tab, takes a serving to about 25 g for roughly 70 more calories.",
        "SODIUM \u2014 this is a salty dish by construction and there is no clean way around it. Potato absorbs a lot of salt and tastes obviously flat without it, while ham and cheese are both salt-delivery systems. Estimated at roughly 1,500 mg per 2-cake serving as written. The mash salt is already cut to 1 tsp on that account; the boiling-water salt mostly goes down the drain, so keep it. The real lever is the filling: homemade turkey sausage in place of deli ham puts that ~1,400 mg under your control.",
        "DIPPING SAUCE: 1/4 cup mayo, 1 Tbs ketchup, 1 tsp lime juice, 1/2 tsp smoked paprika, a pinch of cayenne. That is the pink sauce in the video.",
        "MAKE-AHEAD: formed cakes hold 24 hr covered in the fridge, or freeze them raw in a single layer on a sheet pan and then bag them. Fry from frozen over medium-low, adding about 3 minutes a side.",
    ],
    6,
)


# ---------------- Thanksgiving Apple Pie with Crumble Top ----------------
recipe(
    "Thanksgiving Apple Pie", "Dessert / bake", 8,
    "Deep-dish, precooked apples, cider syrup, crumble top.",
    "A tall 9-inch deep-dish apple pie with precooked apples, cider syrup, and "
    "a buttery crumble instead of a top crust. Serves 8.",
    ["Make the dough a day ahead if you can: it needs at least 1 hr in the "
     "fridge and keeps up to 2 days",
     "Have out a Dutch oven, a small saucepan, two sheet pans and a 9 in "
     "deep-dish pie plate",
     "Leave at least 4 hr after baking for the pie to cool and set before "
     "anyone slices it"],
    [
        ("6.1 oz (173 g) all-purpose flour, for the crust", [
            (2, 3, "whisk"),
            (3, 4, "cut in butter\nto pea- and\nalmond-sized\npieces"),
            (4, 6, "fold in just\nuntil it holds\nwhen squeezed\n\none disc,\nwrap, chill\n1 hr (up to\n2 days)"),
            (6, 22, "heat oven to 425°F\nwith a sheet pan\non the lowest rack\n\nroll dough to 12 in,\nfit a 9 in deep dish,\ntrim, fold under,\ncrimp\n\nmound in apples,\npile on crumble,\npress lightly\n\nchill while the\noven heats"),
            (7, 22, "bake on the hot\nsheet pan 425°F\n25 min, until\nedge and crumble\nstart to color\n\nlower to 375°F,\nfoil the crust edge\n(tent the top if\nit darkens fast)\n\n35–50 min more,\nuntil thick juices\nbubble slowly at\nthe edges\n\ncool on a rack\nat least 4 hr"),
        ]),
        ("1 1/2 tsp sugar, for the crust", []),
        ("0.4 tsp fine salt, for the crust", []),
        ("4.4 oz (125 g) cold unsalted butter, cubed, for the crust", []),
        ("2 Tbs cold vodka", [(2, 2, None), (3, 2, None)]),
        ("2 Tbs ice water", []),
        ("1 cup apple cider", [
            (2, 1, "simmer down\nto about 1/4\nof its volume"),
            (3, 1, None),
            (4, 9, "spread apples\non a sheet pan\nto cool\n\ndrain all their\njuice into the\ncider pan\n\nboil to about\n1/2 cup syrup,\nstir in the\nlemon juice"),
            (5, 10, "toss cooled\napples with\nthe starch,\nthen with\nthe warm\nsyrup"),
        ]),
        ("4.41 lb (2 kg) apples, half Granny Smith, half Honeycrisp or Braeburn", [
            (2, 1, "peel, core,\nslice 1/4 in\n(6 mm)"),
            (3, 8, "Dutch oven,\ncovered,\nmedium-low,\nstir often\n\n~12 min, until\nslices bend but\nhold their shape\n\nno hard boil"),
        ]),
        ("3.53 oz (100 g) granulated sugar", []),
        ("1.76 oz (50 g) packed brown sugar, for the filling", []),
        ("1 tsp ground cinnamon, for the filling", []),
        ("1/4 tsp ground nutmeg", []),
        ("1/8 tsp (0.12 tsp) ground allspice", []),
        ("1/4 tsp fine salt, for the filling", []),
        ("1 lemon, zested and juiced", [(2, 1, "zest\n(juice\nkept for\nthe syrup)")]),
        ("2 Tbs tapioca starch (or 1 1/2 Tbs cornstarch)", [(2, 1, None), (3, 1, None), (4, 1, None)]),
        ("4.25 oz (120 g) all-purpose flour, for the crumble", [
            (2, 5, "whisk"),
            (3, 6, "rub in butter\nwith fingertips\nto pea- and\nmarble-sized\nclumps\n\nchill until\nneeded"),
        ]),
        ("3.5 oz (100 g) packed brown sugar, for the crumble", []),
        ("1/2 cup rolled oats (optional)", []),
        ("1/2 tsp ground cinnamon, for the crumble", []),
        ("1/4 tsp fine salt, for the crumble", []),
        ("3 oz (85 g) cold unsalted butter, cubed, for the crumble", []),
    ],
    [
        "I scaled the dough down to about 55% of your original, which is the bottom-crust disc, so there's no leftover dough.",
        "Timing is the same as your original: dough Tuesday, filling Wednesday morning, bake Wednesday afternoon.",
        "The starch only sets once the filling bubbles, so bake until thick juices bubble slowly at the edges of the crumble, and cool at least 4 hours before slicing.",
        "A day-old pie slices cleanest.",
        "Serve with vanilla ice cream or sharp cheddar.",
    ],
    6,
)


# ===========================================================================
# Cook order
# ---------------------------------------------------------------------------
# Written by hand per recipe. The web app's Steps view renders this, never the
# grid flattened by column: that produced impossible orders (noodle water poured
# in before the noodles were boiled).
# ===========================================================================
COOK = {

"Smash Burgers": [
 "Slice the onion paper-thin and pile it loose. Divide the 8 oz of chuck into four 2 oz balls, handling them as little as possible, and keep them cold. Do not season yet.",
 "Heat a cast iron or carbon steel pan over medium-high. Toast the cut sides of the buns until golden, then set them aside.",
 "Crank the heat to high. Add 1 tsp oil and wipe out the excess with a paper towel. Heat until the pan just starts to smoke.",
 "Place the four balls in the pan with room between them. Immediately top each with a handful of onion, then smash hard straight through the onion with a stiff spatula until each patty is about 1/8 in thick.",
 "Season the onion side with the 1/2 tsp salt and 1/4 tsp pepper.",
 "Sear undisturbed about 90 seconds, until the edges are lacy and deep brown.",
 "Scrape hard to get fully under the crust and flip, onion side down. Lay a slice of American cheese on two of the four patties.",
 "Cook 30 to 45 seconds, just until the cheese melts. Pull them promptly \u2014 thin patties overcook fast.",
 "Spread burger sauce on the bun bottoms, add the pickles, then stack two patties per bun. Serve immediately.",
],

"Shrimp Burgers": [
 "Thaw the 12 oz of shrimp, peel and devein, then press between towels until the surface is dry. Split them: 4 oz for the paste, 8 oz to dice.",
 "Pur\u00e9e the 4 oz smooth with the 1/2 tsp kosher salt, then work it hard for a full minute until it turns sticky and glossy. This is the binder.",
 "Dice the other 8 oz pea-size or smaller.",
 "Whisk together the egg, mayo, cornstarch, scallions, ginger, grated garlic and white pepper.",
 "Fold the paste, the diced shrimp and the wet mix together gently. Do not overmix.",
 "Chill 30 minutes, then form two patties about 3/4 in thick. Pat the surfaces dry again right before they hit the pan.",
 "Film a pan with the 2 tsp of oil over medium-high. Fry 2 to 3 minutes per side, pulling at 120\u2013125\u00b0F. Rest 2 minutes.",
 "Toast the buns. Spread the lime-sriracha mayo on the bottoms, add the cucumber-herb slaw, then the patties. Serve immediately.",
],

"Swai Fillets": [
 "Pat the fillets dry. Combine the red pepper flakes, seafood seasoning, garlic powder, salt and pepper in a bowl, and spread the cornmeal in a second shallow bowl.",
 "Season the fish with the spice mix, then press each fillet into the cornmeal to coat.",
 "Wrap the coated fillets in plastic and refrigerate 30 minutes. This sets the coating so it does not slide off in the pan.",
 "Heat the 2 Tbs of canola oil in a skillet over medium.",
 "Fry about 5 minutes per side, until browned.",
 "Add the 1/4 cup of water, bring to a simmer, cover, and cook about 10 minutes, flipping occasionally, until the fish flakes. Read the notes first \u2014 this last step undoes the crust, and the fish is done well before 20 minutes of total heat.",
],

"Shrimp & Egg Noodles": [
 "Put 2 qt of water on to boil with the 2 tsp of kosher salt. Its starch is an ingredient here, so start it first.",
 "While it heats, get everything ready: pat the shrimp bone-dry and season with the salt and pepper, slice the garlic, cube the butter and keep it cold, grate the Parmesan fine, chop the parsley, juice the lemon.",
 "When the water boils, add the egg noodles and cook them 1 minute under package time.",
 "While the noodles cook, melt the 1 Tbs of butter in a skillet over medium-high. Sear the shrimp 90 seconds per side, then remove them to a plate.",
 "In the same pan, add the garlic and red pepper flakes. Sizzle 45 seconds, until fragrant but not browned.",
 "Scoop out 1 cup of the noodle water, then drain the noodles.",
 "Add the vinegar and 1/2 cup of the noodle water to the pan. Reduce by half, scraping up the fond.",
 "Add the drained noodles and a splash more noodle water. Toss over low heat.",
 "Take the pan OFF the heat. Add the cold butter and the Parmesan in handfuls, tossing constantly, until the sauce turns glossy. On direct heat it will break.",
 "Return the shrimp and add the lemon juice and parsley. Loosen with more noodle water until the sauce coats the noodles. Serve immediately.",
],

"Sesame Turkey Meatballs": [
 "Preheat the oven to 350\u00b0F (175\u00b0C). Have an ungreased 9x13 glass pan and foil ready.",
 "Combine the maple syrup, ketchup, rice vinegar, mustard and sesame seeds in a medium saucepan. Bring to a simmer and simmer 5 minutes.",
 "Take it off the heat and stir in the sesame oil. Set aside. Simmering sesame oil drives off its aroma, which is the whole reason it is here.",
 "Beat together the green onions, egg, soy sauce, ginger, onion powder, black pepper and garlic powder.",
 "Add the ground turkey, top with the panko, and mix well by hand.",
 "Scoop into uniform meatballs.",
 "Heat the olive oil in a skillet over medium-high. Sear the meatballs 2 to 3 minutes, turning, until browned on all sides \u2014 they will not be cooked through. Transfer them to the baking pan.",
 "Scatter the chopped carrots evenly between the meatballs.",
 "Pour the sauce evenly over everything and cover with foil.",
 "Bake 20 to 25 minutes covered, then uncover and broil 2 to 3 minutes to glaze.",
],

"Turkey Italian Sausage": [
 "Toast the fennel seed in a dry pan about 60 seconds, until fragrant, then crack it coarsely.",
 "Combine the fennel with the salt, paprika, garlic powder, black pepper, red pepper flakes, oregano and mushroom powder in a small bowl.",
 "Scatter the spice mix over the cold ground turkey, then add the olive oil, ice water and red wine vinegar.",
 "Mix hard for 60 to 90 seconds, until the meat turns sticky and tacky and clings to the bowl. That stickiness is the bind \u2014 keep going until you see it.",
 "Cover and chill 12 to 24 hours. This is what turns seasoned ground turkey into sausage. If you need it tonight, see the no-rest note.",
 "Test-fry a teaspoon in a hot pan and adjust the salt or the heat before you commit the batch.",
 "Shape and cook: pinched raw onto pizza, formed into patties, crumbled into sauce, or rolled into meatballs. The notes have the specifics for each.",
],

"Papas Rellenas": [
 "Squeeze the shredded cheese into 8 tight pucks and freeze them 30 minutes. Line a sheet pan with parchment.",
 "Put the potato chunks in a pot with 2 1/2 qt of COLD water and the 1 Tbs of salt. Bring to a boil and cook 15 to 20 minutes, until a knife slides in easily. Starting cold is what keeps the edges from turning to mush.",
 "Drain, then return the potatoes to the dry hot pot for 1 to 2 minutes over low heat to steam off the water they just took on.",
 "Rice or mash them while hot. Never a food processor \u2014 it ruptures the starch and turns the mash to glue.",
 "Stir together the 1 tsp of salt, the egg yolk, cornstarch, mushroom powder and white pepper. Chop the cilantro and dice the ham.",
 "Fold everything into the potato just until combined. Do not overwork. Cool 30 minutes in the fridge \u2014 warm mash will not hold a seal.",
 "Oil your hands. Divide into 8 balls, press a deep well in each, seal a frozen cheese puck inside, then roll smooth and flatten to about 3/4 in. Check each one for cracks.",
 "Dust both sides with cornstarch.",
 "Fry in the oil over medium, 4 to 5 minutes per side, until deep gold. Drain on a rack.",
],

"Thanksgiving Apple Pie": [
 "Make the dough (1 hr, up to 2 days ahead). Whisk the 6.1 oz of flour, 1 1/2 tsp sugar and 0.4 tsp fine salt. Cut in the 4.4 oz of cold cubed butter until the pieces range from pea- to almond-sized; you want visible butter. Sprinkle in the 2 Tbs cold vodka and 2 Tbs ice water and fold with a spatula just until the dough holds when squeezed. Shape into one disc, wrap, and chill. Keeps up to 2 days.",
 "Reduce the cider (15 min). Simmer the 1 cup of apple cider in a small saucepan until it is down to about a quarter of the volume. Set aside.",
 "Precook the apples (12 min). Peel, core, and slice the 4.41 lb of apples 1/4 in (6 mm) thick. Put them in a Dutch oven with the 3.53 oz granulated sugar, 1.76 oz brown sugar, 1 tsp cinnamon, 1/4 tsp nutmeg, 1/8 tsp allspice, 1/4 tsp fine salt and the lemon zest. Cover and cook over medium-low, stirring often, until the slices bend but still hold their shape. Don't let it boil hard.",
 "Cool and drain (30 min). Spread the apples on a sheet pan to cool. Then drain all the juice they released into the cider pan.",
 "Make the syrup (8 min). Boil the juice and cider together until about 1/2 cup of syrup remains. Stir in the lemon juice. Toss the cooled apples with the 2 Tbs tapioca starch (or 1 1/2 Tbs cornstarch), then with the warm syrup.",
 "Make the crumble. Whisk the 4.25 oz flour, 3.5 oz brown sugar, 1/2 cup rolled oats (optional), 1/2 tsp cinnamon and 1/4 tsp fine salt. Rub in the 3 oz of cold cubed butter with your fingertips until you have clumps ranging from pea- to marble-sized. Chill until needed.",
 "Assemble (20 min). Put a sheet pan on the lowest rack and heat the oven to 425°F. Roll the dough to 12 in and fit it into a 9 in deep-dish pie plate. Trim, fold the edge under, and crimp. Mound in the apples, then pile the crumble over the top, pressing lightly. Chill the pie while the oven heats.",
 "Hot start (25 min). Bake on the preheated sheet pan at 425°F until the crust edge and crumble start to color.",
 "Finish the bake (45 min). Lower the oven to 375°F and shield the crust edges with foil. If the crumble darkens too fast, tent the top loosely with foil. Bake until the crust is deep golden and thick juices bubble slowly at the edges of the crumble, usually 35 to 50 minutes. The starch only sets once the filling bubbles.",
 "Cool fully (4 hr). Cool on a rack for at least 4 hours before slicing so the filling sets.",
],

}

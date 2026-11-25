' Every setting for the Recipe Book app: screen, colors, type sizes, layout, keys.
function BookConfig() as Object
    return {
        screen: { w: 1280, h: 720 }
        dataPath: "pkg:/data/recipes.json"
        registrySection: "recipes"
        tabs: ["Steps", "Ingredients", "Notes"]
        colors: {
            bg: &h1E1A17FF
            panel: &h2C2621FF
            cursor: &h4A3B2CFF
            text: &hF4EDE4FF
            dim: &hA89A8AFF
            accent: &hE0A458FF
            check: &h8CC084FF
        }
        font: { title: 44, head: 30, body: 34, small: 24 }
        layout: {
            margin: 70
            top: 40
            headerH: 150      ' title, subtitle and tab row
            lineGap: 10
            listGap: 14       ' extra space between list items
            menuRowH: 70
        }
        ' roUniversalControlEvent codes (press events; releases are code + 100).
        keys: { back: 0, up: 2, down: 3, left: 4, right: 5, ok: 6, rev: 8, fwd: 9, play: 13 }
    }
end function

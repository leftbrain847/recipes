' Draw2D rendering for the Recipe Book: the menu and the recipe tabs.

function NewFonts(cfg as Object) as Object
    reg = CreateObject("roFontRegistry")
    f = cfg.font
    return {
        title: reg.GetDefaultFont(f.title, true, false)
        head: reg.GetDefaultFont(f.head, true, false)
        body: reg.GetDefaultFont(f.body, false, false)
        bold: reg.GetDefaultFont(f.body, true, false)
        small: reg.GetDefaultFont(f.small, false, false)
    }
end function

sub DrawBook(screen as Object, fonts as Object, cfg as Object, s as Object)
    screen.Clear(cfg.colors.bg)
    if s.view = "menu" then
        DrawMenu(screen, fonts, cfg, s)
    else
        DrawRecipe(screen, fonts, cfg, s)
    end if
end sub

sub DrawMenu(screen as Object, fonts as Object, cfg as Object, s as Object)
    c = cfg.colors
    L = cfg.layout
    w = cfg.screen.w
    screen.DrawText("Recipe Book", L.margin, L.top, c.accent, fonts.title)
    hint = "Up/Down choose   OK open   Back exit"
    screen.DrawText(hint, w - L.margin - fonts.small.GetOneLineWidth(hint, w), L.top + 16, c.dim, fonts.small)
    y0 = L.top + L.headerH - 40
    avail = cfg.screen.h - y0 - 30
    heights = []
    for i = 0 to s.book.Count() - 1
        heights.Push(L.menuRowH)
    end for
    if s.menuTop = invalid then s.menuTop = 0
    s.menuTop = ScrollTop(heights, s.sel, s.menuTop, avail)
    y = y0
    for i = s.menuTop to s.book.Count() - 1
        if y + L.menuRowH > cfg.screen.h then exit for
        r = s.book[i]
        if i = s.sel then screen.DrawRect(L.margin - 20, y - 6, w - 2 * L.margin + 40, L.menuRowH - 6, c.cursor)
        screen.DrawText(r.name, L.margin, y + 6, c.text, fonts.bold)
        info = r.category + "  -  serves " + r.serves.ToStr()
        screen.DrawText(info, w - L.margin - fonts.small.GetOneLineWidth(info, w), y + 16, c.dim, fonts.small)
        y = y + L.menuRowH
    end for
end sub

sub DrawRecipe(screen as Object, fonts as Object, cfg as Object, s as Object)
    c = cfg.colors
    L = cfg.layout
    w = cfg.screen.w
    r = Current(s)
    screen.DrawText(r.name, L.margin, L.top, c.accent, fonts.title)
    sub1 = "Serves " + r.serves.ToStr() + "  -  " + r.category
    screen.DrawText(sub1, L.margin, L.top + 56, c.dim, fonts.small)

    ' Tab row.
    x = L.margin
    ty = L.top + 96
    for i = 0 to cfg.tabs.Count() - 1
        label = cfg.tabs[i]
        tw = fonts.head.GetOneLineWidth(label, w)
        if i = s.tab then
            screen.DrawRect(x - 14, ty - 4, tw + 28, 44, c.accent)
            screen.DrawText(label, x, ty, c.bg, fonts.head)
        else
            screen.DrawText(label, x, ty, c.dim, fonts.head)
        end if
        x = x + tw + 56
    end for
    hint = "Left/Right tabs   Back recipes"
    if s.tab = 0 then hint = "Down/OK next   Up back   " + hint
    if s.tab = 1 then hint = "OK check off   " + hint
    screen.DrawText(hint, w - L.margin - fonts.small.GetOneLineWidth(hint, w), ty + 8, c.dim, fonts.small)

    y0 = L.top + L.headerH + 10
    if s.tab = 0 then
        DrawStepPage(screen, fonts, cfg, s, y0)
    else if s.tab = 1 then
        DrawList(screen, fonts, cfg, s, r.ingredients, y0, true)
    else
        DrawList(screen, fonts, cfg, s, r.notes, y0, false)
    end if
end sub

sub DrawStepPage(screen as Object, fonts as Object, cfg as Object, s as Object, y0 as Integer)
    c = cfg.colors
    L = cfg.layout
    width = cfg.screen.w - 2 * L.margin
    pages = StepPages(Current(s))
    if pages.Count() = 0 then return
    page = pages[s.step]
    screen.DrawText(page.title, L.margin, y0, c.accent, fonts.head)
    y = y0 + 52
    lineH = fonts.body.GetOneLineHeight() + L.lineGap
    for each item in page.lines
        indent = 0
        if page.bullets then
            screen.DrawText("-", L.margin, y, c.accent, fonts.body)
            indent = 34
        end if
        for each line in WrapText(item, fonts.body, width - indent)
            screen.DrawText(line, L.margin + indent, y, c.text, fonts.body)
            y = y + lineH
        end for
        y = y + L.listGap
    end for
    if y - L.listGap > cfg.screen.h - 20 then s.overflows = s.overflows + 1
    ' Peek at what comes next, so you can read ahead while you work.
    if s.step + 1 < pages.Count() then
        nxt = pages[s.step + 1]
        peek = "Next: " + nxt.lines[0]
        ny = cfg.screen.h - 60
        if y < ny then
            lines = WrapText(peek, fonts.small, width)
            screen.DrawText(lines[0] + "...", L.margin, ny, c.dim, fonts.small)
        end if
    end if
end sub

sub DrawList(screen as Object, fonts as Object, cfg as Object, s as Object, items as Object, y0 as Integer, checks as Boolean)
    if items.Count() = 0 then return
    c = cfg.colors
    L = cfg.layout
    indent = 0
    if checks then indent = 50
    width = cfg.screen.w - 2 * L.margin - indent
    font = fonts.body
    if not checks then font = fonts.small
    lineH = font.GetOneLineHeight() + 6
    wrapped = []
    heights = []
    for each item in items
        lines = WrapText(item, font, width)
        wrapped.Push(lines)
        heights.Push(lines.Count() * lineH + L.listGap)
    end for
    avail = cfg.screen.h - y0 - 20
    if s.listTop = invalid or s.listKey <> s.sel.ToStr() + "/" + s.tab.ToStr() then
        s.listTop = 0
        s.listKey = s.sel.ToStr() + "/" + s.tab.ToStr()
    end if
    s.listTop = ScrollTop(heights, s.cur, s.listTop, avail)
    y = y0
    for i = s.listTop to items.Count() - 1
        if y + heights[i] - L.listGap > cfg.screen.h then exit for
        on = IsChecked(s, i)
        if i = s.cur then screen.DrawRect(L.margin - 16, y - 4, cfg.screen.w - 2 * L.margin + 32, heights[i] - L.listGap + 4, c.cursor)
        color = c.text
        if checks then
            screen.DrawRect(L.margin, y + 6, 30, 30, c.dim)
            if on then
                screen.DrawRect(L.margin + 3, y + 9, 24, 24, c.check)
                color = c.dim
            else
                screen.DrawRect(L.margin + 3, y + 9, 24, 24, c.bg)
            end if
        end if
        for each line in wrapped[i]
            screen.DrawText(line, L.margin + indent, y, color, font)
            y = y + lineH
        end for
        y = y + L.listGap
    end for
end sub

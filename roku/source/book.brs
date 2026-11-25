' The app's state and rules, with no drawing: what each remote key does on each screen.
' Pure, so tests/book_test.brs can drive it in the simulator.

function LoadBook(cfg as Object) as Object
    text = ReadAsciiFile(cfg.dataPath)
    if text = "" then return invalid
    data = ParseJson(text)
    if data = invalid or data.recipes = invalid then return invalid
    return data.recipes
end function

' progress: { recipeName: stepIndex } saved from an earlier session (may be empty).
function NewState(book as Object, progress as Object) as Object
    return {
        book: book
        view: "menu"          ' "menu" or "recipe"
        sel: 0                ' highlighted recipe on the menu
        tab: 0                ' 0 steps, 1 ingredients, 2 notes
        step: 0               ' page on the Steps tab (0 is "Before you start" when the recipe has prep)
        cur: 0                ' highlighted row on the Ingredients and Notes tabs
        checked: {}           ' ingredient index -> true, for the open recipe
        progress: progress
        saveNeeded: false
        overflows: 0          ' step pages drawn past the bottom of the screen (the autotest asserts none)
    }
end function

function Current(s as Object) as Object
    return s.book[s.sel]
end function

' Pages on the Steps tab: the prep list (if any) then each step.
function StepPages(r as Object) as Object
    pages = []
    if r.prep <> invalid then
        if r.prep.Count() > 0 then pages.Push({ title: "Before you start", lines: r.prep, bullets: true })
    end if
    n = r.steps.Count()
    for i = 0 to n - 1
        pages.Push({ title: "Step " + (i + 1).ToStr() + " of " + n.ToStr(), lines: [r.steps[i]], bullets: false })
    end for
    return pages
end function

function TabCount(s as Object) as Integer
    r = Current(s)
    if s.tab = 0 then return StepPages(r).Count()
    if s.tab = 1 then return r.ingredients.Count()
    return r.notes.Count()
end function

function Clamp(v as Integer, lo as Integer, hi as Integer) as Integer
    if v < lo then return lo
    if v > hi then return hi
    return v
end function

sub OpenRecipe(s as Object)
    s.view = "recipe"
    s.tab = 0
    s.cur = 0
    s.checked = {}
    s.step = 0
    saved = s.progress[Current(s).name]
    if saved <> invalid then s.step = Clamp(saved, 0, StepPages(Current(s)).Count() - 1)
end sub

' Applies one key press. Returns "exit" when the app should close, else "".
function HandleKey(s as Object, code as Integer, cfg as Object) as String
    k = cfg.keys
    if s.view = "menu" then
        n = s.book.Count()
        if code = k.back then return "exit"
        if code = k.up then s.sel = (s.sel - 1 + n) mod n
        if code = k.down then s.sel = (s.sel + 1) mod n
        if code = k.ok or code = k.play or code = k.right then OpenRecipe(s)
        return ""
    end if

    if code = k.back then
        s.view = "menu"
        return ""
    end if
    ntabs = cfg.tabs.Count()
    if code = k.left then s.tab = (s.tab - 1 + ntabs) mod ntabs
    if code = k.right then s.tab = (s.tab + 1) mod ntabs
    if code = k.left or code = k.right then s.cur = 0

    last = TabCount(s) - 1
    if s.tab = 0 then
        before = s.step
        if code = k.down or code = k.fwd or code = k.ok or code = k.play then s.step = Clamp(s.step + 1, 0, last)
        if code = k.up or code = k.rev then s.step = Clamp(s.step - 1, 0, last)
        if s.step <> before then
            s.progress[Current(s).name] = s.step
            s.saveNeeded = true
        end if
    else
        if code = k.down then s.cur = Clamp(s.cur + 1, 0, last)
        if code = k.up then s.cur = Clamp(s.cur - 1, 0, last)
        if code = k.fwd then s.cur = last
        if code = k.rev then s.cur = 0
        if s.tab = 1 and code = k.ok then
            key = s.cur.ToStr()
            if IsChecked(s, s.cur) then s.checked.Delete(key) else s.checked[key] = true
        end if
    end if
    return ""
end function

function IsChecked(s as Object, i as Integer) as Boolean
    return s.checked[i.ToStr()] <> invalid
end function

' Word-wraps text (newlines kept) to lines no wider than `width` in `font`.
function WrapText(text as String, font as Object, width as Integer) as Object
    lines = []
    for each para in text.Split(Chr(10))
        line = ""
        for each word in para.Split(" ")
            if word <> "" then
                if line = "" then
                    cand = word
                else
                    cand = line + " " + word
                end if
                if line = "" or font.GetOneLineWidth(cand, 100000) <= width then
                    line = cand
                else
                    lines.Push(line)
                    line = word
                end if
            end if
        end for
        lines.Push(line)
    end for
    return lines
end function

' First list item to draw so item `cur` is on screen, given each item's height.
' Keeps `top` when cur is already visible, so the list doesn't jump.
function ScrollTop(heights as Object, cur as Integer, top as Integer, avail as Integer) as Integer
    if cur < top then return cur
    used = 0
    for i = top to cur
        used = used + heights[i]
    end for
    while used > avail and top < cur
        used = used - heights[top]
        top = top + 1
    end while
    return top
end function

function LoadProgress(cfg as Object) as Object
    sec = CreateObject("roRegistrySection", cfg.registrySection)
    v = sec.Read("progress")
    if v = "" then return {}
    p = ParseJson(v)
    if p = invalid then return {}
    return p
end function

sub SaveProgress(cfg as Object, s as Object)
    sec = CreateObject("roRegistrySection", cfg.registrySection)
    sec.Write("progress", FormatJson(s.progress))
    sec.Flush()
    s.saveNeeded = false
end sub

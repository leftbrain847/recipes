' Unit tests for roku/source/book.brs. Run by tests/roku.test.mjs with brs-cli.
sub Main()
    t = { pass: 0, fail: 0 }
    cfg = BookConfig()
    cfg.dataPath = "pkg:/roku/data/recipes.json"
    book = LoadBook(cfg)
    Check(t, book <> invalid, "book loads")
    if book = invalid then
        print "RESULT pass=0 fail=1"
        return
    end if
    TestBook(t, book)
    TestMenu(t, book, cfg)
    TestSteps(t, book, cfg)
    TestIngredients(t, book, cfg)
    TestWrapAndScroll(t)
    TestEmptyAndBadProgress(t, cfg)
    print "RESULT pass=" + t.pass.ToStr() + " fail=" + t.fail.ToStr()
end sub

sub Check(t as Object, ok as Boolean, name as String)
    if ok then
        t.pass = t.pass + 1
    else
        t.fail = t.fail + 1
        print "FAIL " + name
    end if
end sub

function FindRecipe(book as Object, name as String) as Integer
    for i = 0 to book.Count() - 1
        if book[i].name = name then return i
    end for
    return -1
end function

sub TestBook(t as Object, book as Object)
    pie = FindRecipe(book, "Thanksgiving Apple Pie")
    Check(t, pie >= 0, "the apple pie is in the book")
    r = book[pie]
    Check(t, r.ingredients.Count() = 22, "pie has 22 ingredients")
    Check(t, r.steps.Count() = 10, "pie has 10 steps")
    Check(t, r.serves = 8, "pie serves 8")
    Check(t, StepPages(r).Count() = 11, "prep page plus 10 steps")
    Check(t, StepPages(r)[1].title = "Step 1 of 10", "step page titles count from 1")
end sub

sub TestMenu(t as Object, book as Object, cfg as Object)
    k = cfg.keys
    s = NewState(book, {})
    Check(t, HandleKey(s, k.up, cfg) = "" and s.sel = book.Count() - 1, "Up on the first recipe wraps to the last")
    HandleKey(s, k.down, cfg)
    Check(t, s.sel = 0, "Down wraps back to the first")
    HandleKey(s, k.ok, cfg)
    Check(t, s.view = "recipe" and s.tab = 0 and s.step = 0, "OK opens the recipe on Steps")
    HandleKey(s, k.back, cfg)
    Check(t, s.view = "menu", "Back returns to the menu")
    Check(t, HandleKey(s, k.back, cfg) = "exit", "Back on the menu exits")
end sub

sub TestSteps(t as Object, book as Object, cfg as Object)
    k = cfg.keys
    s = NewState(book, {})
    s.sel = FindRecipe(book, "Thanksgiving Apple Pie")
    HandleKey(s, k.ok, cfg)
    HandleKey(s, k.down, cfg)
    HandleKey(s, k.ok, cfg)
    Check(t, s.step = 2, "Down and OK both turn the page")
    Check(t, s.saveNeeded and s.progress["Thanksgiving Apple Pie"] = 2, "the step is remembered")
    for i = 1 to 20
        HandleKey(s, k.fwd, cfg)
    end for
    Check(t, s.step = 10, "paging stops on the last step")
    HandleKey(s, k.up, cfg)
    Check(t, s.step = 9, "Up goes back a step")
    HandleKey(s, k.back, cfg)
    HandleKey(s, k.ok, cfg)
    Check(t, s.step = 9, "reopening resumes where you left off")
    s2 = NewState(book, { "Thanksgiving Apple Pie": 99 })
    s2.sel = s.sel
    HandleKey(s2, k.ok, cfg)
    Check(t, s2.step = 10, "a saved step past the end is clamped")
    HandleKey(s, k.left, cfg)
    Check(t, s.tab = 2, "Left from Steps wraps to Notes")
    HandleKey(s, k.right, cfg)
    HandleKey(s, k.right, cfg)
    Check(t, s.tab = 1, "Right moves to Ingredients")
end sub

sub TestIngredients(t as Object, book as Object, cfg as Object)
    k = cfg.keys
    s = NewState(book, {})
    s.sel = FindRecipe(book, "Thanksgiving Apple Pie")
    HandleKey(s, k.ok, cfg)
    HandleKey(s, k.right, cfg)
    HandleKey(s, k.down, cfg)
    HandleKey(s, k.ok, cfg)
    Check(t, IsChecked(s, 1) and not IsChecked(s, 0), "OK checks off the highlighted ingredient")
    HandleKey(s, k.ok, cfg)
    Check(t, not IsChecked(s, 1), "OK again un-checks it")
    HandleKey(s, k.ok, cfg)
    HandleKey(s, k.fwd, cfg)
    Check(t, s.cur = 21, "Fwd jumps to the last ingredient")
    Check(t, not s.saveNeeded, "checking ingredients doesn't touch saved progress")
    HandleKey(s, k.back, cfg)
    HandleKey(s, k.ok, cfg)
    Check(t, not IsChecked(s, 1), "checks reset when you open a recipe again")
end sub

sub TestWrapAndScroll(t as Object)
    font = CreateObject("roFontRegistry").GetDefaultFont(34, false, false)
    text = "Whisk the flour, sugar and salt. Cut in the cold butter until the pieces range from pea- to almond-sized."
    lines = WrapText(text, font, 400)
    Check(t, lines.Count() > 1, "long text wraps")
    ok = true
    for each l in lines
        if font.GetOneLineWidth(l, 100000) > 400 then ok = false
    end for
    Check(t, ok, "no wrapped line is wider than the box")
    Check(t, lines.Join(" ") = text, "wrapping keeps every word")
    Check(t, WrapText("a" + Chr(10) + "b", font, 400).Count() = 2, "newlines start a new line")
    h = [100, 100, 100, 100, 100]
    Check(t, ScrollTop(h, 1, 0, 250) = 0, "visible item: no scroll")
    Check(t, ScrollTop(h, 3, 0, 250) = 2, "scrolls just enough to show the item")
    Check(t, ScrollTop(h, 0, 3, 250) = 0, "scrolls back up")
end sub

' An empty tab and bad saved progress must not crash.
sub TestEmptyAndBadProgress(t as Object, cfg as Object)
    k = cfg.keys
    r = { name: "Empty", category: "x", serves: 1, subtitle: "", prep: [], ingredients: [], steps: ["only"], notes: [] }
    s = NewState([r], { "Empty": "garbage" })
    HandleKey(s, k.ok, cfg)
    Check(t, s.step = 0, "non-integer saved progress is ignored")
    HandleKey(s, k.right, cfg)
    HandleKey(s, k.down, cfg)
    Check(t, s.cur = 0, "Down on an empty list stays put")
end sub

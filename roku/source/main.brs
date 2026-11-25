' Recipe Book for Roku: entry point and key loop. roScreen + Draw2D at 1280x720, redrawn on each key press.
' Deep link autotest=1 drives every recipe and tab with scripted key presses, prints a summary and exits
' (used by tests/roku.test.mjs through brs-cli). Adding shots=1 also prints the menu and the last recipe's
' first page on each tab as base64 PNGs.
sub Main(args as Dynamic)
    cfg = BookConfig()
    book = LoadBook(cfg)
    if book = invalid or book.Count() = 0 then
        print "BOOK ERROR: no recipes in " + cfg.dataPath
        return
    end if
    auto = false
    shots = false
    if type(args) = "roAssociativeArray" then
        auto = args.autotest <> invalid
        shots = args.shots <> invalid
    end if

    screen = CreateObject("roScreen", true, cfg.screen.w, cfg.screen.h)
    screen.SetAlphaEnable(true)
    port = CreateObject("roMessagePort")
    screen.SetMessagePort(port)
    fonts = NewFonts(cfg)

    if auto then
        RunAutotest(screen, fonts, cfg, book, shots)
        return
    end if

    s = NewState(book, LoadProgress(cfg))
    DrawBook(screen, fonts, cfg, s)
    screen.SwapBuffers()
    while true
        msg = wait(0, port)
        if type(msg) = "roUniversalControlEvent" and msg.GetInt() < 100 then
            if HandleKey(s, msg.GetInt(), cfg) = "exit" then return
            if s.saveNeeded then SaveProgress(cfg, s)
            DrawBook(screen, fonts, cfg, s)
            screen.SwapBuffers()
        end if
    end while
end sub

' Opens every recipe, pages through every step, checks an ingredient and scrolls every list to the end,
' drawing after each key, then prints counts the test asserts on.
sub RunAutotest(screen as Object, fonts as Object, cfg as Object, book as Object, shots as Boolean)
    k = cfg.keys
    s = NewState(book, {})
    frames = 0
    pages = 0
    checked = 0
    if shots then Shot(screen, fonts, cfg, s, "menu")
    for i = 0 to book.Count() - 1
        s.sel = i
        HandleKey(s, k.ok, cfg)
        for t = 0 to cfg.tabs.Count() - 1
            n = TabCount(s)
            if shots and i = book.Count() - 1 then Shot(screen, fonts, cfg, s, cfg.tabs[t])
            for j = 0 to n
                DrawBook(screen, fonts, cfg, s)
                screen.SwapBuffers()
                frames = frames + 1
                if t = 0 then pages = pages + 1
                if t = 1 and j = 0 then
                    HandleKey(s, k.ok, cfg)
                    if IsChecked(s, 0) then checked = checked + 1
                end if
                HandleKey(s, k.down, cfg)
            end for
            HandleKey(s, k.right, cfg)
        end for
        HandleKey(s, k.back, cfg)
        DrawBook(screen, fonts, cfg, s)
        frames = frames + 1
    end for
    print "AUTOTEST recipes=" + book.Count().ToStr() + " pages=" + pages.ToStr() + " checked=" + checked.ToStr() + " frames=" + frames.ToStr() + " overflows=" + s.overflows.ToStr() + " view=" + s.view + " last=" + book[book.Count() - 1].name
    print "AUTOTEST OK"
end sub

sub Shot(screen as Object, fonts as Object, cfg as Object, s as Object, label as String)
    DrawBook(screen, fonts, cfg, s)
    screen.SwapBuffers()
    print "SHOT " + label + " " + screen.GetPng(0, 0, cfg.screen.w, cfg.screen.h).ToBase64String()
end sub

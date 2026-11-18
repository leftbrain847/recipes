"""Build recipe_book.xlsx: one tab per recipe as a combination grid, plus a
linked Contents sheet. Reads the data from recipes.py.

    python build_xlsx.py [OUT.xlsx]
"""
import math
import sys

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.worksheet.properties import PageSetupProperties
from openpyxl.utils import get_column_letter

from recipes import RECIPES



# ---- tunables -------------------------------------------------------------
GREEN = "2F7D32"
ING_WIDTH = 40          # column A width, in characters
STEP_WIDTH = 17         # each step column width
LINE_H = 13.5           # rendered height of one 10pt line
PAD = 8                 # vertical padding inside a cell
MIN_ROW_H = 30
CHARS_PER_UNIT = 1.15   # chars that fit per width unit at Arial 10

thin = Side(style="thin", color=GREEN)
med = Side(style="medium", color=GREEN)

F_TITLE = Font(name="Arial", size=14, bold=True, color="1A1A1A")
F_SUB = Font(name="Arial", size=9, italic=True, color="555555")
F_PREP = Font(name="Arial", size=10, bold=True, color="1A1A1A")
F_ING = Font(name="Arial", size=10, color="1A1A1A")
F_STEP = Font(name="Arial", size=10, bold=True, color="1A1A1A")
F_NOTE = Font(name="Arial", size=9.5, color="333333")
F_H = Font(name="Arial", size=10, bold=True, color="FFFFFF")
F_LINK = Font(name="Arial", size=11, color="1155CC", underline="single")

C = Alignment(horizontal="center", vertical="center", wrap_text=True)
L = Alignment(horizontal="left", vertical="center", wrap_text=True)
LT = Alignment(horizontal="left", vertical="top", wrap_text=True)



def line_count(text, width_units):
    """How many rendered lines `text` needs in a cell of the given width."""
    if not text:
        return 1
    cap = max(6, int(width_units * CHARS_PER_UNIT))
    total = 0
    for para in str(text).split("\n"):
        total += max(1, math.ceil(len(para) / cap)) if para else 1
    return total


def apply_merge_aware_borders(ws, r0, r1, c0, c1):
    """Box every cell, then strip interior lines inside each merged range so a
    merged block reads as one cell instead of a stack of them."""
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            ws.cell(row=r, column=c).border = Border(
                left=thin, right=thin, top=thin, bottom=thin)

    for rng in ws.merged_cells.ranges:
        if rng.min_row < r0 or rng.max_row > r1:
            continue
        for r in range(rng.min_row, rng.max_row + 1):
            for c in range(rng.min_col, rng.max_col + 1):
                ws.cell(row=r, column=c).border = Border(
                    left=thin if c == rng.min_col else None,
                    right=thin if c == rng.max_col else None,
                    top=thin if r == rng.min_row else None,
                    bottom=thin if r == rng.max_row else None,
                )

    # medium outer frame
    for c in range(c0, c1 + 1):
        t = ws.cell(row=r0, column=c)
        t.border = Border(left=t.border.left, right=t.border.right,
                          top=med, bottom=t.border.bottom)
        b = ws.cell(row=r1, column=c)
        b.border = Border(left=b.border.left, right=b.border.right,
                          top=b.border.top, bottom=med)
    for r in range(r0, r1 + 1):
        lft = ws.cell(row=r, column=c0)
        lft.border = Border(left=med, right=lft.border.right,
                            top=lft.border.top, bottom=lft.border.bottom)
        rgt = ws.cell(row=r, column=c1)
        rgt.border = Border(left=rgt.border.left, right=med,
                            top=rgt.border.top, bottom=rgt.border.bottom)


def size_rows(ws, grid_start, rows, n_step_cols):
    """Row heights that fit both the ingredient text and every merged step cell."""
    n = len(rows)
    heights = []
    for ing, cells in rows:
        h = line_count(ing, ING_WIDTH) * LINE_H + PAD
        for col, span, text in cells:
            if span == 1 and text:
                h = max(h, line_count(text, STEP_WIDTH) * LINE_H + PAD)
        heights.append(max(MIN_ROW_H, h))

    # merged step cells: grow the rows they span until the text fits
    for i, (_, cells) in enumerate(rows):
        for col, span, text in cells:
            if span <= 1 or not text:
                continue
            need = line_count(text, STEP_WIDTH) * LINE_H + PAD
            have = sum(heights[i:i + span])
            if have < need:
                bump = (need - have) / span
                for k in range(i, min(i + span, n)):
                    heights[k] += bump

    for k, h in enumerate(heights):
        ws.row_dimensions[grid_start + k].height = round(h, 1)


def recipe_sheet(wb, name, subtitle, prep, rows, notes, n_step_cols=5):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = ING_WIDTH
    for i in range(n_step_cols):
        ws.column_dimensions[get_column_letter(2 + i)].width = STEP_WIDTH
    last_col = 1 + n_step_cols
    lastL = get_column_letter(last_col)

    ws["A1"] = name
    ws["A1"].font = F_TITLE
    ws.merge_cells(f"A1:{lastL}1")
    ws["A1"].alignment = L
    ws.row_dimensions[1].height = 22

    ws["A2"] = subtitle
    ws["A2"].font = F_SUB
    ws.merge_cells(f"A2:{lastL}2")
    ws["A2"].alignment = L
    ws.row_dimensions[2].height = 16

    back = ws["A3"]
    back.value = "← Back to Contents"
    back.font = F_LINK
    back.hyperlink = Hyperlink(ref="A3", location="Contents!B5", tooltip="Contents")

    r = 5
    frame_top = r
    for p in prep:
        ws.cell(row=r, column=1, value=p).font = F_PREP
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=last_col)
        ws.cell(row=r, column=1).alignment = C
        total_w = ING_WIDTH + STEP_WIDTH * n_step_cols
        ws.row_dimensions[r].height = max(
            20, line_count(p, total_w) * LINE_H + PAD)
        r += 1

    grid_start = r
    for ing, cells in rows:
        ws.cell(row=r, column=1, value=ing).font = F_ING
        ws.cell(row=r, column=1).alignment = L
        for col, span, text in cells:
            cell = ws.cell(row=r, column=col, value=text if text else None)
            cell.font = F_STEP
            cell.alignment = C
            if span > 1:
                ws.merge_cells(start_row=r, start_column=col,
                               end_row=r + span - 1, end_column=col)
        r += 1
    grid_end = r - 1

    size_rows(ws, grid_start, rows, n_step_cols)
    apply_merge_aware_borders(ws, frame_top, grid_end, 1, last_col)

    r = grid_end + 2
    ws.cell(row=r, column=1, value="Notes").font = Font(
        name="Arial", size=11, bold=True, color=GREEN)
    r += 1
    total_w = ING_WIDTH + STEP_WIDTH * n_step_cols
    for nte in notes:
        cell = ws.cell(row=r, column=1, value="•  " + nte)
        cell.font = F_NOTE
        cell.alignment = LT
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=last_col)
        ws.row_dimensions[r].height = round(
            line_count(nte, total_w * 0.98) * 12.5 + 6, 1)
        r += 1

    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.freeze_panes = "B5"
    return ws



# ===========================================================================
# Assemble
# ===========================================================================
OUT = sys.argv[1] if len(sys.argv) > 1 else "recipe_book.xlsx"

wb = Workbook()
toc = wb.active
toc.title = "Contents"
toc.sheet_view.showGridLines = False
toc.column_dimensions["A"].width = 3
toc.column_dimensions["B"].width = 26
toc.column_dimensions["C"].width = 20
toc.column_dimensions["D"].width = 9
toc.column_dimensions["E"].width = 60

toc["B2"] = "Recipe Book"
toc["B2"].font = Font(name="Arial", size=18, bold=True, color=GREEN)
toc.row_dimensions[2].height = 26
toc["B3"] = "One tab per recipe, laid out as a Cooking for Engineers grid."
toc["B3"].font = F_SUB

box = Border(left=thin, right=thin, top=thin, bottom=thin)
for i, h in enumerate(["Recipe", "Category", "Serves", "Notes"]):
    c = toc.cell(row=5, column=2 + i, value=h)
    c.font = F_H
    c.fill = PatternFill("solid", fgColor=GREEN)
    c.alignment = C
    c.border = box
toc.row_dimensions[5].height = 20

row = 6
for rec in RECIPES:
    recipe_sheet(wb, rec["name"], rec["subtitle"], rec["prep"],
                 rec["rows"], rec["notes"], rec["n_step_cols"])
    c = toc.cell(row=row, column=2, value=rec["name"])
    c.font = F_LINK
    c.alignment = L
    c.border = box
    c.hyperlink = Hyperlink(ref=c.coordinate, location=f"'{rec['name']}'!A1",
                            tooltip=f"Go to {rec['name']}")
    for col, val, al in ((3, rec["category"], L), (4, rec["serves"], C),
                         (5, rec["blurb"], L)):
        cc = toc.cell(row=row, column=col, value=val)
        cc.font = F_ING
        cc.alignment = al
        cc.border = box
    toc.row_dimensions[row].height = max(
        20, line_count(rec["blurb"], 60) * LINE_H + 6)
    row += 1

tip = toc.cell(row=row + 1, column=2,
               value="To add a recipe: copy an existing tab, rename it, then add a row "
                     "here and link it (Insert > Link > Place in This Document).")
tip.font = F_SUB
toc.merge_cells(start_row=row + 1, start_column=2, end_row=row + 1, end_column=5)
tip.alignment = L
toc.freeze_panes = "B6"
toc.page_setup.orientation = "landscape"

wb.save(OUT)
print("saved", OUT)

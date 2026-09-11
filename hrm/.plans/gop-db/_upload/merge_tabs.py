# -*- coding: utf-8 -*-
"""Chen 2 tab testcase moi vao workbook "Testcase chuyen doi.xlsx" cua team.

Chay:  python3 merge_tabs.py

Viec script lam:
 1. Chep nguyen sheet testcase cua tung man sang workbook (gia tri + dinh dang + o gop
    + do rong cot + chieu cao dong + dropdown Passed/Failed). openpyxl khong co ham
    chep sheet giua 2 workbook nen phai chep tay tung o (`cell._style` dung chung ->
    phai copy()).
 2. Bo sung dong 16 "Tong so testcase" cho khop khuon cua team — bo tao testcase cua
    DNS chi sinh toi dong 15, trong khi tab Tong hop cua team tro toi o K16.
 3. Them dong tuong ung vao tab "Tong hop", chep cong thuc va dinh dang tu dong cuoi.

KHONG dong toi cac tab cu.
"""
import os
import shutil
import sys
from copy import copy

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(HERE, "Testcase chuyển đổi.xlsx")
MAU_TAB = "22. DM công việc, lỗi thiết bị"      # tab mau de chep dinh dang dong 14/16

# (file nguon, ten tab moi, ten hien o cot "Danh muc" cua tab Tong hop)
NEW_TABS = [
    (os.path.join(HERE, "..", "warranty-repair-request", "testcase.xlsx"),
     "25. YC kiểm tra sửa chữa - BH", "Yêu cầu kiểm tra sửa chữa - bảo hành"),
    (os.path.join(HERE, "..", "warranty-repair-handle-request", "testcase.xlsx"),
     "26. Phiếu xử lý yêu cầu", "Phiếu xử lý yêu cầu"),
]


def copy_sheet(src_ws, dst_wb, title):
    if title in dst_wb.sheetnames:
        del dst_wb[title]
        print("   (tab trung ten -> ghi de)")
    dst_ws = dst_wb.create_sheet(title=title)

    for row in src_ws.iter_rows():
        for cell in row:
            new = dst_ws.cell(row=cell.row, column=cell.column, value=cell.value)
            if cell.has_style:
                new._style = copy(cell._style)

    for rng in src_ws.merged_cells.ranges:
        dst_ws.merge_cells(str(rng))
    for letter, dim in src_ws.column_dimensions.items():
        if dim.width:
            dst_ws.column_dimensions[letter].width = dim.width
    for idx, dim in src_ws.row_dimensions.items():
        if dim.height:
            dst_ws.row_dimensions[idx].height = dim.height
    for dv in src_ws.data_validations.dataValidation:
        new_dv = copy(dv)
        dst_ws.add_data_validation(new_dv)
        for rng in dv.sqref.ranges:
            new_dv.add(str(rng))
    return dst_ws


def align_summary_block(dst_ws, mau_ws):
    """Them dong 16 "Tong so testcase" + doi K14 theo dung khuon cua team."""
    for col in (9, 11):                      # cot I (nhan) va K (cong thuc)
        src = mau_ws.cell(16, col)
        dst = dst_ws.cell(16, col, src.value)
        if src.has_style:
            dst._style = copy(src._style)
    src14 = mau_ws.cell(14, 11)
    dst14 = dst_ws.cell(14, 11, src14.value)   # '=K16-K15'
    if src14.has_style:
        dst14._style = copy(src14._style)


def add_summary_row(ws_sum, mau_row, tab_name, display_name):
    """Them 1 dong vao tab Tong hop, chep cong thuc + dinh dang tu dong mau."""
    r = ws_sum.max_row + 1
    while all(ws_sum.cell(r - 1, c).value in (None, "") for c in range(1, 4)) and r > 2:
        r -= 1                                  # bo qua cac dong trong o cuoi bang
    old_tab = "22. DM công việc, lỗi thiết bị"
    for c in range(1, 18):
        src = ws_sum.cell(mau_row, c)
        val = src.value
        if isinstance(val, str):
            val = val.replace(old_tab, tab_name)
            val = val.replace(str(mau_row), str(r)) if val.startswith("=ROUND") else val
        if c == 1:
            val = '=Row()-ROW($A$1)'    # dong mau dang de STT cung -> tra ve cong thuc
        if c == 2:
            val = display_name
        dst = ws_sum.cell(r, c, val)
        if src.has_style:
            dst._style = copy(src._style)
    print("   + dong Tong hop %d: %s" % (r, display_name))
    return r


def main():
    assert os.path.exists(BOOK), "Chua tai workbook ve: %s" % BOOK
    backup = BOOK.replace(".xlsx", ".BACKUP.xlsx")
    if not os.path.exists(backup):
        shutil.copyfile(BOOK, backup)

    wb = openpyxl.load_workbook(BOOK)
    print("Workbook truoc khi sua: %d tab" % len(wb.sheetnames))
    mau_ws = wb[MAU_TAB]
    ws_sum = wb["Tổng hợp"]
    mau_row = 23                                # dong cua tab 22 trong Tong hop

    for path, title, display in NEW_TABS:
        src = openpyxl.load_workbook(path)
        dst = copy_sheet(src.active, wb, title)
        align_summary_block(dst, mau_ws)
        add_summary_row(ws_sum, mau_row, title, display)
        print(" + tab: %s (tu %s)" % (title, os.path.basename(os.path.dirname(path))))

    wb.save(BOOK)

    chk = openpyxl.load_workbook(BOOK)
    print("Sau khi sua: %d tab -> %s" % (len(chk.sheetnames), chk.sheetnames[-2:]))
    s = chk["Tổng hợp"]
    for r in range(s.max_row - 3, s.max_row + 1):
        vals = [s.cell(r, c).value for c in (1, 2, 7, 12)]
        if any(v not in (None, "") for v in vals):
            print("   Tong hop dong %d: %s" % (r, vals))


if __name__ == "__main__":
    main()

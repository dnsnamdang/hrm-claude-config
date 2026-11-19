# -*- coding: utf-8 -*-
"""Sinh testcase đúng KHUÔN CHUẨN tab "13. DM quốc gia" (`TC_MAU_QUOC_GIA.xlsx`) + checklist `CHECKLIST_TC_SRS.xlsx`
(chốt 03/11/2026). Dùng hàm này cho MỌI testcase mới — không gọi `tc_engine.build` trực tiếp.

Bọc `tc_engine.build` (giữ nguyên engine để generator cũ chạy lại không đổi) rồi chỉnh cho khớp tab Quốc gia:
  - KHÔNG có nhóm "Phân quyền & truy cập" / mã TC-ROLE ở đầu — phân quyền là nhóm "PHÂN QUYỀN" đứng CUỐI.
  - Cột Module + Nhóm chức năng chỉ ghi ở case ĐẦU MỖI NHÓM.
  - Cột KQ thực tế + DNS check 1-3 để TRỐNG (DNS tự điền khi chạy test).
  - Thêm dòng 16 "Tổng số testcase".
Dùng:
    from tc_chuan import build_chuan
    build_chuan(out_xlsx, sheet_name, feature_name, module_name, DESCRIPTION_BLOCK, SECTIONS, loai='danh_muc'|'phieu'|'bao_cao')
SECTIONS: [(La Mã, TIÊU ĐỀ NHÓM, [(stt, chức năng, P0-2, tiền điều kiện, bước, test data, expected), ...]), ...]
Tiêu đề + thứ tự nhóm theo `check_tc.THU_TU`. Chạy xong tự gọi `check_tc.kiem()` — phải 0 lỗi.
"""
import os
import sys
from copy import copy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tc_engine  # noqa: E402
import check_tc  # noqa: E402
from openpyxl import load_workbook  # noqa: E402


def build_chuan(output_file, sheet_name, feature_name, module_name, description_block, sections, loai):
    total = tc_engine.build(output_file, sheet_name, feature_name, module_name,
                            description_block, [], sections)
    wb = load_workbook(output_file)
    ws = wb.worksheets[0]
    new_group = False
    for r in range(18, ws.max_row + 1):
        c = ws.cell(r, 3).value
        if not c:
            continue
        if not str(c).startswith('TC_'):          # dòng tiêu đề nhóm
            new_group = True
            continue
        if not new_group:
            ws.cell(r, 1).value = None
            ws.cell(r, 2).value = None
        new_group = False
        for col in (10, 11, 12, 13):
            ws.cell(r, col).value = None
    # dòng 16: Tổng số testcase (như tab Quốc gia)
    for col in range(1, 18):
        src, dst = ws.cell(15, col), ws.cell(16, col)
        if src.has_style:
            dst._style = copy(src._style)
    for rng in list(ws.merged_cells.ranges):
        if rng.min_row == 15 and rng.max_row == 15:
            ws.merge_cells(start_row=16, start_column=rng.min_col, end_row=16, end_column=rng.max_col)
    ws.cell(16, 9).value = 'Tổng số testcase'
    ws.cell(16, 11).value = '=COUNTIF(C18:C1000,"TC_*")'
    ws.cell(16, 13).value = None
    ws.cell(16, 15).value = None
    wb.save(output_file)
    ok = check_tc.kiem(output_file, loai)
    print('Tong TC:', total, '| khuon chuan:', 'DAT' if ok else 'CHUA DAT')
    return total

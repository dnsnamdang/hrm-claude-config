# -*- coding: utf-8 -*-
"""Gộp toàn bộ testcase #10455 vào 1 FILE DUY NHẤT: mỗi màn 1 sheet (giữ nguyên khuôn 17 cột,
khối mô tả 9 mục, TEST SUMMARY riêng từng sheet).

Chạy: /opt/homebrew/opt/python@3.14/bin/python3.14 .plans/gop-db/lich-su-thiet-lap-10455/gen_testcase_1file.py
Không sửa engine của skill: chỉ thay tạm `Workbook` của engine bằng 1 workbook dùng chung.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))

import openpyxl  # noqa: E402
import tc_engine  # noqa: E402

OUT = os.path.join(HERE, "testcase - Lịch sử thiết lập (#10455).xlsx")

# Thứ tự sheet = thứ tự 11 hạng mục trong task
ORDER = [
    "Quy định chung", "Quy định làm thêm", "Quy định nghỉ", "Cài đặt", "Phân quyền",
    "Người dùng", "Ca làm việc", "phân ca", "Cấu hình HCNS", "Cấu hình giao việc",
]

shared = openpyxl.Workbook()
shared.remove(shared.active)


class _SharedBook:
    """Thay cho Workbook() trong engine: mỗi lần build() mở 1 sheet mới trong workbook chung."""

    def __init__(self):
        self.active = shared.create_sheet("tmp%d" % len(shared.sheetnames))

    def save(self, _path):  # engine gọi save() cuối mỗi build — bỏ qua, lưu 1 lần ở cuối
        pass


tc_engine.Workbook = _SharedBook
_orig_build = tc_engine.build


def _build(output_file, sheet_name, *a, **kw):
    total = _orig_build(output_file, sheet_name, *a, **kw)
    name = os.path.splitext(os.path.basename(output_file))[0]
    name = name.replace("testcase - ", "").replace("Lịch sử ", "")
    name = "Lịch sử phân ca" if name == "phân ca" else name
    shared.worksheets[-1].title = name[:31]
    return total


tc_engine.build = _build

# Module con đã `from tc_engine import build` -> phải gán lại sau khi import
import tc_lich_su_phan_ca  # noqa: E402
import tc_thiet_lap_cham_cong  # noqa: E402
import tc_quyen_hcns_giaoviec  # noqa: E402

for mod in (tc_lich_su_phan_ca, tc_thiet_lap_cham_cong, tc_quyen_hcns_giaoviec):
    mod.build = _build
    mod.main()


def _key(ws):
    t = ws.title
    for i, k in enumerate(ORDER):
        if k.lower() in t.lower():
            return i
    return 99


shared._sheets.sort(key=_key)
shared.active = 0
shared.save(OUT)
print("DA GOP:", OUT)
print("SHEETS:", shared.sheetnames)

# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Bao cao thuong theo nhan vien"
(Bao cao ban hang > Bao cao thu nhap > Bao cao thuong theo nhan vien).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :3233, :3238-3241
  app/Http/Controllers/ReportController.php :2113-2160 (man, searchData, In, Excel), :4334 (chi tiet)
  app/Services/Reports/BonusBusinessEmployeeReportService.php (toan bo)
  resources/views/reports/bonus_business_employee.blade.php
  resources/views/partials/common/company-department-filter-singer.blade.php

Chay:  python .plans/bao-cao-thuong-theo-nhan-vien/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/<feature> -> .plans -> erp -> hrm-claude-config -> hrm/.claude/skills/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))
sys.path.insert(0, HERE)

from tc_engine import build                                    # noqa: E402
from tc_data_role import DESCRIPTION_BLOCK, ROLE_TCS            # noqa: E402
from tc_data_sec import (SEC_I, SEC_II, SEC_III, SEC_IV, SEC_V,  # noqa: E402
                         SEC_VI, SEC_VII, SEC_VIII, SEC_IX, SEC_X)

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Báo cáo thưởng theo nhân viên"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC", SEC_II),
    ("III", "NGUỒN DỮ LIỆU & CÁCH TÍNH", SEC_III),
    ("IV", "GOM THEO PHÒNG BAN - NHÂN VIÊN", SEC_IV),
    ("V", "DÒNG TỔNG CỘNG & PHÂN TRANG", SEC_V),
    ("VI", "CỬA SỔ CHI TIẾT THEO HỢP ĐỒNG", SEC_VI),
    ("VII", "LIÊN KẾT TÊN PHÒNG BAN", SEC_VII),
    ("VIII", "IN & XUẤT EXCEL", SEC_VIII),
    ("IX", "ĐỐI CHIẾU & AN TOÀN DỮ LIỆU", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Báo cáo thưởng theo nhân viên (ERP) - Cập nhật ngày 17/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Bao cao ban hang theo tung mat hang"
(Bao cao > Bao cao ban hang > Bao cao tong hop va so sanh so lieu ban hang).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :3217-3222
  app/Http/Controllers/ReportController.php :1395-1691 (summarySale*, getReportSaleDetail)
  app/Services/Reports/SummarySaleReportService.php (getData, filter, getTablePrint, getTable4Excel)
  app/Jobs/SummarySaleReportServiceJob.php (Excel gui email)
  resources/views/reports/summarySale.blade.php

Chay:  python .plans/bao-cao-ban-hang-theo-tung-mat-hang/gen_testcase.py
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

MODULE = "Báo cáo bán hàng theo từng mặt hàng"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC", SEC_II),
    ("III", "NGUỒN DỮ LIỆU & CÁCH TÍNH", SEC_III),
    ("IV", "HÀNG TRẢ LẠI", SEC_IV),
    ("V", "TỒN KHO, BẢO HÀNH, ĐM ĐÀM PHÁN GIÁ", SEC_V),
    ("VI", "CỬA SỔ CHI TIẾT PHÁT SINH", SEC_VI),
    ("VII", "TỔNG CỘNG & PHÂN TRANG", SEC_VII),
    ("VIII", "IN & XUẤT EXCEL", SEC_VIII),
    ("IX", "ĐỐI CHIẾU & AN TOÀN DỮ LIỆU", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Báo cáo bán hàng theo từng mặt hàng (ERP) - Cập nhật ngày 16/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

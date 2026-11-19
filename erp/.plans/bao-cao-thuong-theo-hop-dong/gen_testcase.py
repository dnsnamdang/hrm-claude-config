# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Bao cao thuong theo hop dong"
(Bao cao > Bao cao thu nhap > Bao cao thuong theo hop dong).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :3243-3246
  app/Http/Controllers/ReportController.php :2164-2213 (trang, lay du lieu, In, Excel)
  app/Services/Reports/BonusBusinessContractReportService.php
      (bonusContractReportSearchData, getBonusContract, getBonusContractFirmEmpl,
       getBonusContractServiceEmpl, filterDate, printListData)
  resources/views/reports/bonus_contract_report.blade.php
  resources/views/partials/common/company-department-filter-singer.blade.php

Chay:  python .plans/bao-cao-thuong-theo-hop-dong/gen_testcase.py
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
                         SEC_VI, SEC_VII, SEC_VIII, SEC_IX)

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Báo cáo thưởng theo hợp đồng"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC", SEC_II),
    ("III", "NGUỒN SỐ LIỆU & CÁCH TÍNH CÁC CỘT THƯỞNG", SEC_III),
    ("IV", "DÒNG NHÂN VIÊN TRONG HỢP ĐỒNG", SEC_IV),
    ("V", "DOANH SỐ TIÊU CHUẨN", SEC_V),
    ("VI", "DÒNG TỔNG CỘNG, SẮP XẾP & PHÂN TRANG", SEC_VI),
    ("VII", "IN & XUẤT EXCEL", SEC_VII),
    ("VIII", "ĐỐI CHIẾU & AN TOÀN DỮ LIỆU", SEC_VIII),
    ("IX", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_IX),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Báo cáo thưởng theo hợp đồng (ERP) - Cập nhật ngày 17/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

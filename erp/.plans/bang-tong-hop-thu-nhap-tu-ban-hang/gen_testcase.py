# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Bang tong hop thu nhap tu ban hang"
(Bao cao > Bao cao thu nhap > Bang tong hop thu nhap tu ban hang).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :3395-3417
  app/Http/Controllers/ReportController.php :4587-4860 (commissionSettlementQuarter*)
  app/Services/Reports/CommissionSettlementQuarterReportService.php (getDataFirm, getDataWr, getData, render, filterAcc)
  app/Services/PrintTemplate/CommissionSettlementQuarterPrint.php, CommissionSettlementQuaterDetailPrint
  resources/views/reports/commission_settlement_quarter.blade.php
  resources/views/partials/common/company-department-filter-singer.blade.php

Chay:  python .plans/bang-tong-hop-thu-nhap-tu-ban-hang/gen_testcase.py
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
                         SEC_VI, SEC_VII, SEC_VIII)

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Bảng tổng hợp thu nhập từ bán hàng"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "KỲ QUYẾT TOÁN / KHOẢNG NGÀY", SEC_II),
    ("III", "BỘ LỌC CÔNG TY / PHÒNG BAN / NHÂN VIÊN / XUẤT HÓA ĐƠN", SEC_III),
    ("IV", "CÁCH TÍNH CÁC CỘT", SEC_IV),
    ("V", "DÒNG PHÒNG BAN, TỔNG CỘNG & PHÂN TRANG", SEC_V),
    ("VI", "CHI TIẾT HỢP ĐỒNG CỦA NHÂN VIÊN", SEC_VI),
    ("VII", "IN & XUẤT EXCEL", SEC_VII),
    ("VIII", "ĐỐI CHIẾU & LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_VIII),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Bảng tổng hợp thu nhập từ bán hàng (ERP) - Cập nhật ngày 11/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

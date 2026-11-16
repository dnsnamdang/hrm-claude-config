# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Bao cao hang gui"
(Kho > Tra cuu ton kho > Bao cao hang gui).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :1657-1662
  app/Http/Controllers/Warehouse/WarehouseReportsController.php :310-385 (holdDetail*, In, Excel)
  app/Model/Warehouse/HoldDetail.php (holdDetailSearchData, render, printListData*)
  app/Model/Warehouse/HoldDetailLog.php (getDetailLog - cua so chi tiet)
  app/Model/Warehouse/ProductImport.php :1563 (nhap gui tang hang gui)
  app/Model/Warehouse/ProductExport.php :1373 (xuat tu hang gui giam)
  resources/views/warehouse/warehouse_reports/hold_details/hold_detail.blade.php

Chay:  python .plans/bao-cao-hang-gui/gen_testcase.py
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

MODULE = "Báo cáo hàng gửi"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC", SEC_II),
    ("III", "CÁCH TÍNH SỐ LIỆU THEO KỲ", SEC_III),
    ("IV", "PHÂN CẤP & ĐƠN VỊ TÍNH", SEC_IV),
    ("V", "CỬA SỔ CHI TIẾT HÀNG GỬI", SEC_V),
    ("VI", "PHÂN TRANG", SEC_VI),
    ("VII", "IN & XUẤT EXCEL", SEC_VII),
    ("VIII", "NGUỒN DỮ LIỆU: NHẬP GỬI & XUẤT TỪ HÀNG GỬI", SEC_VIII),
    ("IX", "ĐỐI CHIẾU & AN TOÀN DỮ LIỆU", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Báo cáo hàng gửi (ERP) - Cập nhật ngày 13/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

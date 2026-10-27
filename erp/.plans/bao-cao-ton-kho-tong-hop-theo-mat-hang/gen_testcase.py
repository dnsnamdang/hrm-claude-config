# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Bao cao ton kho tong hop theo mat hang"
(Kho > Bao cao kho > Bao cao ton kho tong hop theo mat hang).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh da gop gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :1554, 1642-1644
  app/Http/Controllers/Warehouse/WarehouseReportsController.php (stockGeneralProduct,
      warehouseReportGeneralSearchData, exportStockGeneralProduct, printStockGeneralProduct)
  app/Product.php :5243 warehouseReportGeneralSearchData
  app/ExcelExports/GeneralProductExcel.php (mau day du / ngan gon), app/Jobs/GeneralProductMailJob.php
  resources/views/warehouse/warehouse_reports/stock_general_product.blade.php
  resources/views/partials/classes/warehouse/WarehouseReportProductGeneral.blade.php (DVT)

Chay:  python .plans/bao-cao-ton-kho-tong-hop-theo-mat-hang/gen_testcase.py
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

MODULE = "Báo cáo tồn kho tổng hợp theo mặt hàng"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC KHO & HÀNG HÓA", SEC_II),
    ("III", "TÍNH ĐẾN NGÀY", SEC_III),
    ("IV", "CHI TIẾT THEO CÔNG TY THUÊ KHO", SEC_IV),
    ("V", "ĐƠN VỊ TÍNH", SEC_V),
    ("VI", "PHÂN TRANG & SẮP XẾP", SEC_VI),
    ("VII", "XUẤT EXCEL", SEC_VII),
    ("VIII", "ĐỐI CHIẾU & THAO TÁC ĐỒNG THỜI", SEC_VIII),
    ("IX", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_IX),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Báo cáo tồn kho tổng hợp theo mặt hàng (ERP) - Cập nhật ngày 24/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

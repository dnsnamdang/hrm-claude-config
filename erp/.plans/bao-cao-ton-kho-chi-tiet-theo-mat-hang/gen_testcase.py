# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Bao cao ton kho chi tiet theo mat hang"
(Kho > Bao cao kho > Bao cao ton kho chi tiet theo mat hang).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh da gop gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :1552, 1561-1562, 1640
  app/Http/Controllers/Warehouse/WarehouseReportsController.php (stockCardDetail,
      warehouseReportDetailSearchData, exportStockCardDetailReport)
  app/Product.php :4891 warehouseReportDetailSearchData, transformInput
  app/ExcelExports/StockCardDetailExcel.php (mau day du / ngan gon), app/Jobs/StockCardDetailMailJob.php
  resources/views/warehouse/warehouse_reports/stock_card_detail.blade.php, js_detail.blade.php
  resources/views/partials/classes/warehouse/WarehouseReportProductDetail*.blade.php (DVT)

Chay:  python .plans/bao-cao-ton-kho-chi-tiet-theo-mat-hang/gen_testcase.py
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

MODULE = "Báo cáo tồn kho chi tiết theo mặt hàng"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC", SEC_II),
    ("III", "TÍNH ĐẾN NGÀY", SEC_III),
    ("IV", "CHI TIẾT CÔNG TY / LÔ / VỊ TRÍ", SEC_IV),
    ("V", "ĐƠN VỊ TÍNH", SEC_V),
    ("VI", "PHÂN TRANG & SẮP XẾP", SEC_VI),
    ("VII", "XUẤT EXCEL", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU & GIÁ TRỊ BIÊN", SEC_VIII),
    ("IX", "ĐỐI CHIẾU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Báo cáo tồn kho chi tiết theo mặt hàng (ERP) - Cập nhật ngày 24/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

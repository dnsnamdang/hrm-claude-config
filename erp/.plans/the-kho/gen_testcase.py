# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "The kho" (Kho > Bao cao kho > The kho).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh da gop gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :1548-1549, 1637-1638 (quyen Thu kho chi gan cho man va Loc)
  app/Http/Controllers/Warehouse/WarehouseReportsController.php (stockCard, stockCardSearchData,
      printStockCard, exportStockCard)
  app/Product.php :4438 stockCardSearchData (ton dau ky, nhap / xuat trong ky, loc vi tri, cong ty thue kho)
  app/Services/Warehouse/WarehouseReportService.php :1578 getStockCardTable (ban In / Excel)
  resources/views/warehouse/warehouse_reports/stock_card.blade.php
  resources/views/partials/classes/warehouse/StockCardProduct*.blade.php (DVT, SL ton luy ke)
  resources/views/layouts/topmenubar.blade.php :1418-1422

Chay:  python .plans/the-kho/gen_testcase.py
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
from tc_data_sec_a import SEC_I, SEC_II, SEC_III, SEC_IV        # noqa: E402
from tc_data_sec_b import (SEC_V, SEC_VI, SEC_VII, SEC_VIII,    # noqa: E402
                           SEC_IX, SEC_X, SEC_XI)

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Thẻ kho"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "LỌC HÀNG HÓA, CÔNG TY, KHO", SEC_II),
    ("III", "LỌC NHÀ / DÃY / KHOANG / VỊ TRÍ", SEC_III),
    ("IV", "LỌC THỜI GIAN & LOẠI BÁO CÁO", SEC_IV),
    ("V", "KHỐI TỔNG HỢP ĐẦU KỲ - CUỐI KỲ", SEC_V),
    ("VI", "CHI TIẾT CHỨNG TỪ", SEC_VI),
    ("VII", "ĐƠN VỊ TÍNH", SEC_VII),
    ("VIII", "IN & XUẤT EXCEL", SEC_VIII),
    ("IX", "RÀNG BUỘC NHẬP LIỆU & GIÁ TRỊ BIÊN", SEC_IX),
    ("X", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_X),
    ("XI", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_XI),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Thẻ kho (ERP) - Cập nhật ngày 24/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

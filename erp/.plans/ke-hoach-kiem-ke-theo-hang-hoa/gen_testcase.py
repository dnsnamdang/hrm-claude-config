# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Ke hoach kiem ke theo hang hoa"
(Ke toan > Kiem ke > Theo vi tri > Ke hoach kiem ke theo hang hoa).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh da gop gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :1801-1821
  app/Http/Controllers/Warehouse/SelfInventoryRequestController.php
  app/Model/Warehouse/Inventory/SelfInventoryRequest.php (STATUSES, canEdit, canApprove, searchByFilter,
      checkPending, removeFromDB, print_data)
  app/Http/Controllers/Warehouse/SelfInventoriesController.php (store -> DA_LAP_KIEM_KE,
      getDataForSelfInventoryRequest)
  app/Product.php :6610 getDataForAccountingInventory
  app/Http/Controllers/Common/SearchController.php :496 (is_self_inventory, has_stock)
  database/seeds/PermissionsTableSeeder.php :722-729
  resources/views/warehouse/self_inventory_requests/*.blade.php (+ partials)
  resources/views/reports/exports/self_inventory_request_report.blade.php (COLSPAN)
  resources/views/layouts/topmenubar.blade.php :1268-1276

Chay:  python .plans/ke-hoach-kiem-ke-theo-hang-hoa/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/ke-hoach-kiem-ke-theo-hang-hoa -> .plans -> erp -> hrm-claude-config -> hrm/.claude/skills/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))
sys.path.insert(0, HERE)

from tc_engine import build                                    # noqa: E402
from tc_data_role import DESCRIPTION_BLOCK, ROLE_TCS            # noqa: E402
from tc_data_sec_a import SEC_I, SEC_II, SEC_III                # noqa: E402
from tc_data_sec_b import SEC_IV, SEC_V                         # noqa: E402
from tc_data_sec_c import SEC_VI, SEC_VII, SEC_VIII, SEC_IX, SEC_X   # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Kế hoạch kiểm kê theo hàng hóa"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "TẠO MỚI / SỬA / XEM CHI TIẾT", SEC_IV),
    ("V", "GỬI KIỂM & LẬP PHIẾU KIỂM KÊ", SEC_V),
    ("VI", "XÓA", SEC_VI),
    ("VII", "IN & XUẤT EXCEL", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", SEC_VIII),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Kế hoạch kiểm kê theo hàng hóa (ERP) - Cập nhật ngày 21/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

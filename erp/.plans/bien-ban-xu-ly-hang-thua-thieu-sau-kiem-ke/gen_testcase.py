# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Bien ban xu ly hang thua, thieu sau kiem ke"
(Ke toan > Kiem ke > Theo vi tri > Bien ban xu ly hang thua, thieu sau kiem ke).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh da gop gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :1966-1983
  app/Http/Controllers/Warehouse/InventoryAuditReportsController.php (create, store, update, approve,
      delete, getData, print, printList, export, exportList, searchData)
  app/Model/Warehouse/Inventory/InventoryAuditReport.php (STATUSES, canEdit / canApprove / canView,
      syncDetails, saveAccounting, searchByFilter, getData, print_data, product_table, printListData)
  app/Model/Warehouse/Inventory/InventoryAuditReportDetail.php
  resources/views/warehouse/inventory_audit_reports/*.blade.php
  database/seeds/PermissionsTableSeeder.php :783-785
  resources/views/layouts/topmenubar.blade.php :1268-1280

Chay:  python .plans/bien-ban-xu-ly-hang-thua-thieu-sau-kiem-ke/gen_testcase.py
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
from tc_data_sec_a import SEC_I, SEC_II, SEC_III                # noqa: E402
from tc_data_sec_b import SEC_IV, SEC_V, SEC_VI                 # noqa: E402
from tc_data_sec_c import SEC_VII, SEC_VIII, SEC_IX, SEC_X, SEC_XI   # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Biên bản xử lý hàng thừa, thiếu sau kiểm kê"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "TẠO MỚI & LẤY DỮ LIỆU", SEC_IV),
    ("V", "GIÁ XỬ LÝ & PHÂN BỔ CHI PHÍ", SEC_V),
    ("VI", "LƯU / GỬI DUYỆT / SỬA", SEC_VI),
    ("VII", "DUYỆT & BÚT TOÁN", SEC_VII),
    ("VIII", "IN & XUẤT EXCEL", SEC_VIII),
    ("IX", "RÀNG BUỘC NHẬP LIỆU", SEC_IX),
    ("X", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_X),
    ("XI", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_XI),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Biên bản xử lý hàng thừa, thiếu sau kiểm kê (ERP) - Cập nhật ngày 22/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

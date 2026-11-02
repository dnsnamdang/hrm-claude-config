# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu xuat hang dieu chinh kiem ke"
(Ke toan > Hang hoa - Dich vu - Van chuyen > Xuat hang > Phieu xuat hang dieu chinh kiem ke).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :1915-1930
  app/Http/Controllers/Warehouse/InventoryExportsController.php (create, edit, index, searchData, print,
      printList, exportList, show, store, update, validateAccountingWarehouse, delete)
  app/Model/Warehouse/InventoryExport.php (STATUSES, canEdit / canView, getDataForShow, print_data,
      printListData, product_table, updateWarehouse, syncDetails, searchByFilter, saveAccounting,
      generateCode)
  app/Model/Warehouse/InventoryExportDetail.php (calculateExportPrice)
  app/Http/Controllers/Warehouse/WarehouseInventoryExportsController.php :92-94, :376-385
  app/Model/Warehouse/Inventory/WarehouseInventoryExport.php (canApprove, getDataForShow)
  app/Model/Warehouse/SelfInventory.php (handle_completed, needInventoryExport)
  app/Model/Warehouse/Inventory/InventoryAuditReport.php :649-664
  resources/views/warehouse/inventory_exports/*.blade.php
  resources/views/layouts/topmenubar.blade.php :1030
  database/seeds/PermissionsTableSeeder.php :740-741

Chay:  python .plans/phieu-xuat-hang-dieu-chinh-kiem-ke/gen_testcase.py
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
from tc_data_sec_b import SEC_V, SEC_VI, SEC_VII                # noqa: E402
from tc_data_sec_c import SEC_VIII, SEC_IX, SEC_X, SEC_XI       # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Phiếu xuất hàng điều chỉnh kiểm kê"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH & HÀNH ĐỘNG", SEC_III),
    ("IV", "LẬP PHIẾU TỪ PHIẾU XUẤT KHO ĐIỀU CHỈNH KIỂM KÊ", SEC_IV),
    ("V", "PHÂN BỔ KHO KẾ TOÁN & SL ĐƯỢC XUẤT", SEC_V),
    ("VI", "LƯU / LƯU VÀ DUYỆT / SỬA", SEC_VI),
    ("VII", "TỒN KẾ TOÁN, GIÁ VỐN, BÚT TOÁN & PHIẾU KIỂM KÊ", SEC_VII),
    ("VIII", "IN & XUẤT EXCEL", SEC_VIII),
    ("IX", "RÀNG BUỘC NHẬP LIỆU", SEC_IX),
    ("X", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_X),
    ("XI", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_XI),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu xuất hàng điều chỉnh kiểm kê (ERP) - Cập nhật ngày 02/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

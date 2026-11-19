# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu xuat kho dieu chinh kiem ke"
(Kho > Xuat kho > Phieu xuat kho dieu chinh kiem ke).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :1898-1913
  app/Http/Controllers/Warehouse/WarehouseInventoryExportsController.php (create, edit, index, searchData,
      print, printList, exportList, show, store, update, approve, getForInventoryExport,
      validateAccountingStock)
  app/Model/Warehouse/Inventory/WarehouseInventoryExport.php (STATUSES, canEdit / canApprove / canView,
      getDataForShow, print_data, printListData, product_table, syncDetails, searchByFilter,
      generateCode, updateWarehouse)
  app/Model/Warehouse/SelfInventory.php (canHandle, canInventoryExport, needInventoryExport,
      getForWarehouseInventoryExport)
  app/Http/Controllers/Warehouse/SelfInventoriesController.php :592-635
  app/Http/Controllers/Warehouse/InventoryExportsController.php :144-230 (buoc Tao phieu xuat hang)
  resources/views/warehouse/warehouse_inventory_exports/*.blade.php
  resources/views/warehouse/self_inventories/show.blade.php :49-53
  resources/views/layouts/topmenubar.blade.php :1365, :2260
  database/seeds/PermissionsTableSeeder.php :737-738

Chay:  python .plans/phieu-xuat-kho-dieu-chinh-kiem-ke/gen_testcase.py
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
from tc_data_sec_b import SEC_V, SEC_VI, SEC_VII, SEC_VIII      # noqa: E402
from tc_data_sec_c import SEC_IX, SEC_X, SEC_XI                 # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Phiếu xuất kho điều chỉnh kiểm kê"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH & HÀNH ĐỘNG", SEC_III),
    ("IV", "TẠO MỚI TỪ PHIẾU KIỂM KÊ & LẤY DỮ LIỆU", SEC_IV),
    ("V", "LƯU / GỬI DUYỆT / SỬA", SEC_V),
    ("VI", "KIỂM TRA TỒN KẾ TOÁN", SEC_VI),
    ("VII", "TRỪ TỒN KHO & DUYỆT", SEC_VII),
    ("VIII", "IN & XUẤT EXCEL", SEC_VIII),
    ("IX", "RÀNG BUỘC NHẬP LIỆU", SEC_IX),
    ("X", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_X),
    ("XI", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_XI),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu xuất kho điều chỉnh kiểm kê (ERP) - Cập nhật ngày 27/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Kiem ke theo hang hoa" (phieu kiem ke)
(Kho > Kiem kho > Theo vi tri > Kiem ke theo hang hoa).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh da gop gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :1773-1799
  app/Http/Controllers/Warehouse/SelfInventoriesController.php (store, update, storeResult, approve,
      unApprove, delete, getDataForPositionTransfer, getDataForSelfInventoryRequest)
  app/Model/Warehouse/SelfInventory.php (STATUSES, searchByFilter, canEdit / canUpdateResult / canApprove /
      canHandle, needTransfer / needInventoryImport / needInventoryExport, handle_completed, checkPending,
      validateProducts, printListData, print_data)
  app/Model/Warehouse/InventoryImport.php, InventoryExport.php, PositionTransfer.php (handled_qty)
  app/Http/Controllers/Warehouse/InventoryImportsController.php, InventoryExportsController.php,
      PositionTransfersController.php (cap nhat trang thai phieu kiem ke)
  app/Product.php :6557 getDataForInventory
  app/Http/Controllers/HomeController.php :2017-2030 (o cho duyet Trang chu)
  database/seeds/PermissionsTableSeeder.php :722-729
  resources/views/warehouse/self_inventories/*.blade.php
  resources/views/partials/classes/warehouse/SelfInventory*.blade.php
  resources/views/layouts/topmenubar.blade.php :1389-1396

Chay:  python .plans/kiem-ke-theo-hang-hoa/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/kiem-ke-theo-hang-hoa -> .plans -> erp -> hrm-claude-config -> hrm/.claude/skills/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))
sys.path.insert(0, HERE)

from tc_engine import build                                    # noqa: E402
from tc_data_role import DESCRIPTION_BLOCK, ROLE_TCS            # noqa: E402
from tc_data_sec_a import SEC_I, SEC_II, SEC_III                # noqa: E402
from tc_data_sec_b import SEC_IV, SEC_V                         # noqa: E402
from tc_data_sec_c import SEC_VI, SEC_VII, SEC_VIII, SEC_IX, SEC_X, SEC_XI   # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Kiểm kê theo hàng hóa"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "TẠO MỚI / SỬA / XEM CHI TIẾT", SEC_IV),
    ("V", "CẬP NHẬT KẾT QUẢ & GỬI DUYỆT", SEC_V),
    ("VI", "DUYỆT / KHÔNG DUYỆT", SEC_VI),
    ("VII", "XỬ LÝ CHÊNH LỆCH & HOÀN THÀNH", SEC_VII),
    ("VIII", "XÓA, IN & XUẤT EXCEL", SEC_VIII),
    ("IX", "RÀNG BUỘC NHẬP LIỆU", SEC_IX),
    ("X", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_X),
    ("XI", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_XI),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Kiểm kê theo hàng hóa (ERP) - Cập nhật ngày 21/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

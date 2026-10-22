# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu dieu chuyen vi tri"
(Kho > Dieu chuyen > Phieu dieu chuyen vi tri).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.
Man lien quan: .plans/ke-hoach-kiem-ke-theo-vi-tri/, .plans/kiem-ke-theo-vi-tri/.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh da gop gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :1340-1361 (Tao moi gan quyen "Dieu chuyen vi tri")
  app/Http/Controllers/Warehouse/PositionTransfersController.php (store / update / delete / deleteFile /
      printExpect / print / exportList / checkInventory / checkPositionInventory)
  app/Model/Warehouse/PositionTransfer.php (canEdit, searchByFilter, validateProducts, updateWarehouse)
  app/Model/Warehouse/Position.php :235 (vi tri dang kiem kho), app/Product.php :6745
  app/Http/Controllers/Warehouse/PositionInventoryResultsController.php getDataForPositionTransfer
  database/seeds/PermissionsTableSeeder.php :805-808
  resources/views/warehouse/position_transfers/{index,create,edit,show,form,formJs}.blade.php
  resources/views/partials/classes/warehouse/PositionTransfer*.blade.php
  resources/views/partials/modals/selectPositionModal*, selectImportLotModal*
  Khong phu: cac man dieu chuyen tu phieu kiem kho cu (inventory_export / inventory_import).

Chay:  python .plans/phieu-dieu-chuyen-vi-tri/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/phieu-dieu-chuyen-vi-tri -> .plans -> erp -> hrm-claude-config -> hrm/.claude/skills/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))
sys.path.insert(0, HERE)

from tc_engine import build                                    # noqa: E402
from tc_data_role import DESCRIPTION_BLOCK, ROLE_TCS            # noqa: E402
from tc_data_sec_a import SEC_I, SEC_II, SEC_III                # noqa: E402
from tc_data_sec_b import SEC_IV, SEC_V                              # noqa: E402
from tc_data_sec_c import SEC_VI, SEC_VII, SEC_VIII, SEC_IX, SEC_X   # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Phiếu điều chuyển vị trí"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "TẠO MỚI / SỬA / XEM CHI TIẾT", SEC_IV),
    ("V", "ĐIỀU CHUYỂN, TÁC ĐỘNG TỒN & LIÊN KẾT KIỂM KÊ", SEC_V),
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
        feature_name="Phiếu điều chuyển vị trí (ERP) - Cập nhật ngày 20/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

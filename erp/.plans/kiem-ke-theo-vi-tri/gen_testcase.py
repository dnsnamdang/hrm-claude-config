# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Kiem ke theo vi tri" (phieu kiem ke / ket qua kiem ke)
(Kho > Kiem kho > Theo vi tri > Kiem ke theo vi tri).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.
Man lien quan: .plans/ke-hoach-kiem-ke-theo-vi-tri/ (Ke hoach kiem ke theo vi tri).

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh da gop gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :1867-1895
  app/Http/Controllers/Warehouse/PositionInventoryResultsController.php
  app/Model/Warehouse/PositionInventory.php (KK_STATUSES, canUpdateResult, canApprove, canHandle,
      needTransfer, searchByFilter 'result', printListDataForResults, product_table_for_result)
  app/Model/Warehouse/PositionTransfer.php :509-516 (cap nhat da xu ly khi dieu chuyen)
  app/Http/Controllers/HomeController.php :2017 (o cho duyet Trang chu)
  app/Helpers/NotificationHelper.php :40 (thong bao theo quyen, cung cong ty)
  database/seeds/PermissionsTableSeeder.php :715-720
  resources/views/warehouse/position_inventory_results/*.blade.php
  resources/views/partials/classes/warehouse/PositionInventory*.blade.php
  resources/views/layouts/topmenubar.blade.php :1389-1398

Chay:  python .plans/kiem-ke-theo-vi-tri/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/kiem-ke-theo-vi-tri -> .plans -> erp -> hrm-claude-config -> hrm/.claude/skills/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))
sys.path.insert(0, HERE)

from tc_engine import build                                    # noqa: E402
from tc_data_role import DESCRIPTION_BLOCK, ROLE_TCS            # noqa: E402
from tc_data_sec_a import SEC_I, SEC_II, SEC_III                # noqa: E402
from tc_data_sec_b import SEC_IV                                # noqa: E402
from tc_data_sec_c import SEC_V, SEC_VI, SEC_VII, SEC_VIII, SEC_IX, SEC_X   # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Kiểm kê theo vị trí"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "TẠO MỚI / SỬA PHIẾU", SEC_IV),
    ("V", "NHẬP KẾT QUẢ, DUYỆT & XỬ LÝ", SEC_V),
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
        feature_name="Kiểm kê theo vị trí (ERP) - Cập nhật ngày 20/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

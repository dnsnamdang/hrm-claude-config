# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Hoat dong kho" (menu chinh > Hoat dong kho)
kem man "Theo doi theo kho" (bang hoat dong tung kho).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh da gop gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :893-903 (warehouse.forActivities, warehouse.activities - quyen Quan ly kho), :936
  app/Http/Controllers/Warehouse/WarehouseInfosController.php :865 activities
  app/Http/Controllers/Warehouse/WarehousesController.php :62-70 forActivities, activities($id)
  app/Model/Warehouse/Warehouse.php :691 getActivities
  app/Model/Warehouse/WarehouseExportRequest.php (approve, send, activity_message, display_status)
  app/Model/Warehouse/WarehouseImportRequest.php (approve, send, activity_message)
  app/Helpers/FormatHelper.php :897 calculateTime, :913 diffInTime
  resources/views/warehouse/warehouses/activities.blade.php, warehouse_activities.blade.php, forActivities.blade.php
  server_node/server.js :65-82 (kenh tu cap nhat theo kho thu kho)

Chay:  python .plans/hoat-dong-kho/gen_testcase.py
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

MODULE = "Hoạt động kho"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG", SEC_I),
    ("II", "PHẠM VI ĐỀ NGHỊ ĐƯỢC HIỆN", SEC_II),
    ("III", "CỘT DỮ LIỆU & TRẠNG THÁI", SEC_III),
    ("IV", "TỔNG THỜI GIAN XỬ LÝ", SEC_IV),
    ("V", "Ô TỔNG & SẮP XẾP", SEC_V),
    ("VI", "MÀU CẢNH BÁO THEO THỜI GIAN CHỜ", SEC_VI),
    ("VII", "TỰ CẬP NHẬT KHÔNG CẦN TẢI LẠI", SEC_VII),
    ("VIII", "THEO DÕI THEO KHO", SEC_VIII),
    ("IX", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_IX),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Hoạt động kho (ERP) - Cập nhật ngày 27/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

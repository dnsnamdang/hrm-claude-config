# -*- coding: utf-8 -*-
"""Sinh testcase cho man ERP "Tong hop phieu bao hang ve"
(Kinh doanh -> Thong bao -> Phieu bao hang ve).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay tren nhanh gop_db (repo D:/laragon/www/erp).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :940 (man), :2411-2420, :2840-2850, :3071-3080 (3 nguon du lieu)
  app/Http/Controllers/Warehouse/WarehouseInfosController.php :870 arrivedNotifies
  resources/views/warehouse/warehouses/arrivedNotifies.blade.php
  Tab Nhap khau: Order/ProductArrivedNotify2Controller (searchData, print, export, delete)
                 app/Model/Order/ProductArrivedNotify2.php :126 searchByFilter, :288 canDelete
  Tab Trong nuoc: Order/InlandProductArrivedNotifyController + Model InlandProductArrivedNotify :87
  Tab Mua ngoai: Order/ProductArrivedNotifiesController + Model ProductArrivedNotify :496
  resources/views/partials/classes/base/Datatable.blade.php, partials/confirm.blade.php
  database/seeds/PermissionsTableSeeder.php :1115-1118, :1145-1148
  layouts/topmenubar.blade.php :849

Chay:  python .plans/phieu-bao-hang-ve-tong-hop/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/<feature> -> .plans -> erp -> hrm-claude-config -> www/hrm/.claude/skills/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))
sys.path.insert(0, HERE)

from tc_engine import build                           # noqa: E402
from tc_data_role import DESCRIPTION_BLOCK, ROLE_TCS  # noqa: E402
from tc_data_sec import (SEC_I, SEC_II, SEC_III, SEC_IV, SEC_V,  # noqa: E402
                         SEC_VI, SEC_VII, SEC_VIII, SEC_IX, SEC_X)

OUT = os.path.join(HERE, "testcase-phieu-bao-hang-ve-tong-hop.xlsx")

MODULE = "Tổng hợp phiếu báo hàng về"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "THAO TÁC TRÊN PHIẾU (TAB NHẬP KHẨU)", SEC_IV),
    ("V", "TRẠNG THÁI PHIẾU", SEC_V),
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
        feature_name="Tổng hợp phiếu báo hàng về (ERP) - Cập nhật ngày 15/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

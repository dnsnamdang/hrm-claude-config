# -*- coding: utf-8 -*-
"""Sinh testcase cho man ERP "Danh sach loai phieu hach toan"
(QTTT > Cau hinh ERP > Danh sach loai phieu hach toan).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay tren nhanh gop_db (repo D:/laragon/www/erp).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :83-86 (chi qua dang nhap, khong gan quyen rieng)
  app/Http/Controllers/SystemController.php
  app/Model/Accounting/ListBillAccounting.php (9 phan loai)
  database/seeds/ListBillAccountingSeeder.php (105 loai phieu, man chi doc)
  resources/views/systems/list_bill_accounting.blade.php
  resources/views/partials/classes/base/Datatable.blade.php
  resources/views/layouts/topmenubar.blade.php :2002

Chay:  python gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/<feature> -> .plans -> erp -> hrm-claude-config -> www -> hrm/.claude/skills/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))
sys.path.insert(0, HERE)

from tc_engine import build                       # noqa: E402
from tc_data import (DESCRIPTION_BLOCK, ROLE_TCS,  # noqa: E402
                     SEC_I, SEC_II, SEC_III, SEC_IV, SEC_V, SEC_VI,
                     SEC_VII, SEC_VIII, SEC_IX, SEC_X)

OUT = os.path.join(HERE, "testcase-danh-sach-loai-phieu-hach-toan.xlsx")

MODULE = "Loại phiếu hạch toán"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "THÊM MỚI / SỬA / XEM CHI TIẾT", SEC_IV),
    ("V", "CÁC THAO TÁC TRẠNG THÁI", SEC_V),
    ("VI", "XÓA", SEC_VI),
    ("VII", "XUẤT EXCEL / IN", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", SEC_VIII),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Danh sách loại phiếu hạch toán (ERP) - Cập nhật ngày 14/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

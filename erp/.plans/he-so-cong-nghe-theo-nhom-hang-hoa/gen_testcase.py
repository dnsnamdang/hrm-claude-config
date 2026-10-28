# -*- coding: utf-8 -*-
"""Sinh testcase cho man ERP "He so cong nghe theo nhom hang hoa"
(QTTT > Cau hinh ERP > He so cong nghe theo nhom hang hoa).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay tren nhanh gop_db (repo D:/laragon/www/erp).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :6934-6943 (chi qua dang nhap, khong gan quyen rieng)
  app/Http/Controllers/Common/BenefitRateController.php
  app/Model/Common/BenefitRates.php (+ BenefitRateHasGroupProducts.php)
  app/Model/Customers/WrAssignTask.php :936 (noi dung he so)
  resources/views/common/benefit_rates/{index,modalPopup,BenefitRate}.blade.php
  resources/views/partials/classes/base/Datatable.blade.php
  resources/views/partials/confirm.blade.php
  resources/views/layouts/topmenubar.blade.php :2000

Chay:  python gen_testcase.py
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
    HERE, "..", "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))
sys.path.insert(0, HERE)

from tc_engine import build                       # noqa: E402
from tc_data import (DESCRIPTION_BLOCK, ROLE_TCS,  # noqa: E402
                     SEC_I, SEC_II, SEC_III, SEC_IV, SEC_V, SEC_VI,
                     SEC_VII, SEC_VIII, SEC_IX, SEC_X)

OUT = os.path.join(HERE, "testcase-he-so-cong-nghe-theo-nhom-hang-hoa.xlsx")

MODULE = "Hệ số công nghệ theo nhóm hàng"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "THÊM MỚI / SỬA", SEC_IV),
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
        feature_name="Hệ số công nghệ theo nhóm hàng hóa (ERP) - Cập nhật ngày 14/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

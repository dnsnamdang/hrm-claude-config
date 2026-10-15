# -*- coding: utf-8 -*-
"""Sinh testcase cho man ERP "Cau hinh chan luong hang qua han"
(QTTT > Cau hinh ERP > Cau hinh chan luong hang qua han).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay tren nhanh gop_db (repo D:/laragon/www/erp).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :6945-6949 (yeu cau quyen 'Cau hinh he thong')
  app/Http/Controllers/Common/DueConfigsController.php
  app/Http/Middleware/CheckDueConfigs.php (tab 1 - chan nhan vien)
  app/Http/Middleware/CheckDueConfigsManager.php + Services/DueConfig/DueConfigBlockService.php (tab 2)
  app/Http/Controllers/Api/DueConfigController.php (HRM goi sang)
  resources/views/common/due_configs/{edit,overdue-modal}.blade.php
  resources/views/layouts/app.blade.php :205, topmenubar.blade.php :2001
  HRM: hrm-api/app/Http/Middleware/CheckDueConfigsManager.php, Modules/Finance CheckDueConfig,
       hrm-client/plugins/axios.js, components/modal/OverdueEmployeesModal.vue

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

OUT = os.path.join(HERE, "testcase-cau-hinh-chan-luong-hang-qua-han.xlsx")

MODULE = "Chặn luồng hàng quá hạn"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "CHUYỂN TAB & THU GỌN NHÓM", SEC_II),
    ("III", "LỊCH SỬ CHỈNH SỬA", SEC_III),
    ("IV", "TÍCH CẤU HÌNH & LƯU", SEC_IV),
    ("V", "HIỆU LỰC CHẶN NHÂN VIÊN & CHẶN TRƯỞNG PHÒNG", SEC_V),
    ("VI", "XÓA", SEC_VI),
    ("VII", "CỬA SỔ NHÂN VIÊN QUÁ HẠN & XUẤT EXCEL", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", SEC_VIII),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Cấu hình chặn luồng hàng quá hạn (ERP) - Cập nhật ngày 14/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

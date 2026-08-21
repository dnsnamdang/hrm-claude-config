# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu yeu cau dieu chinh cong no"
(admin/income-expenditure/bill_adjust_dept_requests).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

⚠️ Tai lieu viet theo LOGIC ERP dang chay tren nhanh gop_db (repo D:/laragon/www/erp).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :6563-6586
  app/Http/Controllers/IncomeExpenditure/BillAdjustDeptRequestController.php
  app/Model/IncomeExpenditure/BillAdjustDeptRequest.php (+ Detail, DetailItem)
  app/Http/Requests/IncomeExpenditure/BillAdjustDeptRequests/*.php
  app/Services/Contracts/SearchContractService.php (create_bill_adjust_dept_request)
  app/Helpers/NotificationHelper.php :40
  resources/views/income_expenditure/bill_adjust_dept_requests/*.blade.php + partials/*
  resources/views/partials/classes/IncomeExpenditure/BillAdjustDeptRequest*.blade.php
  resources/views/partials/classes/base/Datatable.blade.php
  resources/views/layouts/topmenubar.blade.php :420, :1217, :2164

Chay:  python .plans/dieu-chinh-cong-no/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# .plans/dieu-chinh-cong-no -> .plans -> erp -> hrm-claude-config -> hrm/.claude/skills/...
sys.path.insert(0, os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets"))
sys.path.insert(0, HERE)

from tc_engine import build                                  # noqa: E402
from tc_data_role import DESCRIPTION_BLOCK, ROLE_TCS         # noqa: E402
from tc_data_sec_a import SEC_I, SEC_II, SEC_III             # noqa: E402
from tc_data_sec_b import SEC_IV                             # noqa: E402
from tc_data_sec_c import SEC_V, SEC_VI, SEC_VII             # noqa: E402
from tc_data_sec_d import SEC_VIII, SEC_IX, SEC_X            # noqa: E402

OUT = os.path.join(HERE, "testcase-dieu-chinh-cong-no.xlsx")

MODULE = "YC điều chỉnh công nợ"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "TẠO MỚI / SỬA / XEM CHI TIẾT", SEC_IV),
    ("V", "DUYỆT & KHÔNG DUYỆT", SEC_V),
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
        feature_name="Phiếu yêu cầu điều chỉnh công nợ (ERP) - Cập nhật ngày 19/08/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

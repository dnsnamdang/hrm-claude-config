# -*- coding: utf-8 -*-
"""Sinh testcase cho man ERP "Bao cao han muc cong no nhan vien"
(Ke toan -> Ke toan Cong no -> Nhan vien -> Bao cao han muc cong no nhan vien).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay tren nhanh gop_db (repo D:/laragon/www/erp).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :5107-5113
  app/Http/Controllers/Accounting/ReportLimitDebtController.php (index, searchDataEmployee,
    getDebtEmployeeByCustomer)
  app/Employee.php :134 getMoneyDebtCurrent
  app/Model/Accounting/AccountDetail.php :2317 getDebtEmployee, :2401 getDebtEmployeeByCustomer
  app/Http/Controllers/Common/EmployeesController.php :335 (o Han muc cong no xuat hang)
  resources/views/accounting/report_limit_debts/employee-index.blade.php
  resources/views/partials/classes/base/Datatable.blade.php (bo loc theo quyen, ngay)
  resources/views/layouts/topmenubar.blade.php :1208

Chay:  python .plans/bao-cao-han-muc-cong-no-nhan-vien/gen_testcase.py
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

OUT = os.path.join(HERE, "testcase-bao-cao-han-muc-cong-no-nhan-vien.xlsx")

MODULE = "Báo cáo hạn mức công nợ NV"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", SEC_III),
    ("IV", "NGUỒN HẠN MỨC & XEM CHI TIẾT THEO KHÁCH HÀNG", SEC_IV),
    ("V", "CÁC THAO TÁC TRẠNG THÁI", SEC_V),
    ("VI", "XÓA", SEC_VI),
    ("VII", "IN & XUẤT EXCEL", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", SEC_VIII),
    ("IX", "CÁCH TÍNH CÔNG NỢ & CÔ LẬP DỮ LIỆU", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Báo cáo hạn mức công nợ nhân viên (ERP) - Cập nhật ngày 15/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

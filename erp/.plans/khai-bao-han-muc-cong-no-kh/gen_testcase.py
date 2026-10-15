# -*- coding: utf-8 -*-
"""Sinh testcase cho man ERP "Khai bao han muc cong no khach hang"
(Ke toan -> Ke toan Cong no -> Khach hang -> Khai bao han muc cong no KH).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay tren nhanh gop_db (repo D:/laragon/www/erp).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :5050-5054
  app/Http/Controllers/Accounting/DeclareLimitDebtController.php
  app/Model/Accounting/DeclareLimitDebt.php
  app/Model/Sale/Customer.php :1709 getDeclareLimitDebt
  database/migrations/2022_01_19_140836_create_table_declare_limit_debt.php
  database/seeds/PermissionsTableSeeder.php :402-403
  resources/views/accounting/declare-limit-debt/index.blade.php
  resources/views/partials/classes/sale/DeclareLimitDebt.blade.php
  resources/views/partials/classes/sale/CustomerDeclareLimitDebt.blade.php
  resources/views/layouts/topmenubar.blade.php :1182-1192
  Noi dung han muc: Warehouse/ProductExportRequestsController :2100 checkLimitOverLimitExport,
    Warehouse/BorrowSellRequestsController :599, Sale/CustomersController :1907 getDataCustomer,
    Accounting/ReportLimitDebtController :32

Chay:  python .plans/khai-bao-han-muc-cong-no-kh/gen_testcase.py
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

from tc_engine import build                           # noqa: E402
from tc_data_role import DESCRIPTION_BLOCK, ROLE_TCS  # noqa: E402
from tc_data_sec_a import SEC_I, SEC_II, SEC_III      # noqa: E402
from tc_data_sec_b import SEC_IV, SEC_V, SEC_VI, SEC_VII  # noqa: E402
from tc_data_sec_c import SEC_VIII, SEC_IX, SEC_X     # noqa: E402

OUT = os.path.join(HERE, "testcase-khai-bao-han-muc-cong-no-kh.xlsx")

MODULE = "Khai báo hạn mức công nợ KH"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH & PHÂN TRANG", SEC_III),
    ("IV", "KHAI BÁO / SỬA HẠN MỨC", SEC_IV),
    ("V", "CÁC THAO TÁC TRẠNG THÁI", SEC_V),
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
        feature_name="Khai báo hạn mức công nợ khách hàng (ERP) - Cập nhật ngày 14/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

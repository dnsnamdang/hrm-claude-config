# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Ket chuyen chi phi phai tra"
(menu Ke toan > Ket chuyen cuoi ky > Ket chuyen chi phi phai tra).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :4738-4747 (closing_entries; update / delete tro toi ham khong ton tai)
  app/Http/Controllers/Accounting/ClosingEntryController.php index, searchData, show, create, store,
      validateDate, getSumMoneyByAccount
  app/Model/Accounting/ClosingEntry.php searchByFilter, canView, canDelete, generateCode, saveDetails
  app/Jobs/SaveAdClosingEntry.php (ghi but toan 3351 / 33481 chay nen)
  resources/views/accounting/closing_entries/ index, create, show, form, formJs
  resources/views/partials/classes/accounting/ClosingEntry*.blade.php
  database/seeds/PermissionsTableSeeder.php :1346-1349

Chay:  python .plans/ket-chuyen-chi-phi-phai-tra/gen_testcase.py
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
from tc_data_sec_a import SEC_I, SEC_II, SEC_III, SEC_IV        # noqa: E402
from tc_data_sec_b import SEC_V, SEC_VI, SEC_VII                # noqa: E402
from tc_data_sec_c import SEC_VIII, SEC_IX, SEC_X               # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Kết chuyển chi phí phải trả"

SECTIONS = [
    ("I", "HIỂN THỊ DANH SÁCH", SEC_I),
    ("II", "BỘ LỌC", SEC_II),
    ("III", "FORM TẠO MỚI - THÔNG TIN CHUNG", SEC_III),
    ("IV", "CHỌN VỤ VIỆC & TÍNH SỐ TIỀN", SEC_IV),
    ("V", "RÀNG BUỘC KHI LƯU", SEC_V),
    ("VI", "LƯU VÀ DUYỆT & BÚT TOÁN", SEC_VI),
    ("VII", "XEM CHI TIẾT", SEC_VII),
    ("VIII", "SỬA / XÓA / ĐIỀU CHỈNH", SEC_VIII),
    ("IX", "ĐỒNG THỜI & GỌI THẲNG CHỨC NĂNG", SEC_IX),
    ("X", "LUỒNG ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Kết chuyển chi phí phải trả (ERP) - Cập nhật ngày 06/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu nhap ket qua"
(menu Bao hanh sua chua > Giao viec > Phieu nhap ket qua).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :6159-6172 (wr_import_results), :23-32 (nhom hrm cho ung dung HRM)
  app/Http/Controllers/Customercare/WrImportResultsController.php searchData, create, store, storeApp,
      show, edit, update, delete, reject, deleteFile, hasProductExport
  app/Model/Customers/WrImportResult.php STATUSES, canView, searchByFilter, canEdit, canApproveResult
  app/Http/Requests/WrImportResultRequest.php, app/Http/Traits/SerialValidationTrait.php
  app/Model/Customers/WrAssignTask.php canImportResult
  app/Http/Controllers/Customercare/WrApproveResultsController.php create, store, unApprove (ban giao)
  resources/views/customercare/warranty_repair_import_results/ index, create, edit, show, form, form_show,
      WrImportResult, WrImportResultProduct, WrImportResultWork, WrImportResultCost
  app/Http/Controllers/HomeController.php (o dem cho duyet)

Chay:  python .plans/phieu-nhap-ket-qua/gen_testcase.py
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
from tc_data_sec_b import SEC_V, SEC_VI, SEC_VII, SEC_VIII      # noqa: E402
from tc_data_sec_c import SEC_IX, SEC_X, SEC_XI, SEC_XII        # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Phiếu nhập kết quả"

SECTIONS = [
    ("I", "HIỂN THỊ DANH SÁCH", SEC_I),
    ("II", "BỘ LỌC", SEC_II),
    ("III", "MỞ FORM NHẬP KẾT QUẢ TỪ PHIẾU GIAO VIỆC", SEC_III),
    ("IV", "NHẬP KẾT QUẢ LẮP ĐẶT BÀN GIAO", SEC_IV),
    ("V", "NHẬP KẾT QUẢ SỬA CHỮA / BẢO HÀNH", SEC_V),
    ("VI", "GIAO VIỆC KHÁC, CÔNG PHỤ P3 & TỔNG CÔNG", SEC_VI),
    ("VII", "LƯU / GỬI DUYỆT, THÔNG BÁO & Ô TRANG CHỦ", SEC_VII),
    ("VIII", "XEM CHI TIẾT", SEC_VIII),
    ("IX", "SỬA / XÓA", SEC_IX),
    ("X", "KHÔNG DUYỆT & CHUYỂN SANG DUYỆT KẾT QUẢ", SEC_X),
    ("XI", "ĐỒNG THỜI & GỌI THẲNG CHỨC NĂNG", SEC_XI),
    ("XII", "LUỒNG ĐẦU - CUỐI", SEC_XII),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu nhập kết quả (ERP) - Cập nhật ngày 06/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

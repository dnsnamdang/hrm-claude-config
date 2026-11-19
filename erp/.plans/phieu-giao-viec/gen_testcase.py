# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu giao viec"
(menu Bao hanh sua chua > Giao viec > Phieu giao viec).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :6141-6157 (wr_assign_tasks)
  app/Http/Controllers/Customercare/WrAssignTasksController.php index, searchData, store, show, edit,
      update, delete, printList, exportList
  app/Model/Customers/WrAssignTask.php STATUSES, canView, canImportResult, canDelete, canEdit, searchByFilter
  app/Http/Requests/WrAssignTaskStoreRequestWithPlace.php
  resources/views/customercare/warranty_repair_assign_tasks/ index, create, edit, show, form,
      WrAssignTask (tinh tong cong), WrAssignTaskProduct, WrAssignTaskAssembly, WrAssignTaskMerchandise
  app/Http/Controllers/Customercare/WrImportResultsController.php (chuyen trang thai khi nhap ket qua)
  app/Http/Controllers/Customercare/WrApproveResultsController.php (chuyen trang thai khi duyet ket qua)
  app/Model/Customers/AssemblyRequest.php refreshAssignStatus

Chay:  python .plans/phieu-giao-viec/gen_testcase.py
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

MODULE = "Phiếu giao việc"

SECTIONS = [
    ("I", "HIỂN THỊ DANH SÁCH", SEC_I),
    ("II", "PHẠM VI DANH SÁCH & PHIẾU GIAO VIỆC ĐƯỢC GIAO", SEC_II),
    ("III", "BỘ LỌC", SEC_III),
    ("IV", "TẠO PHIẾU TỪ HỢP ĐỒNG / PL BỔ SUNG", SEC_IV),
    ("V", "TẠO PHIẾU TỪ PHIẾU BẢO HÀNH", SEC_V),
    ("VI", "TẠO PHIẾU TỪ LẮP ĐẶT BÀN GIAO / GIAO VIỆC KHÁC", SEC_VI),
    ("VII", "RÀNG BUỘC NHẬP LIỆU & CÔNG PHỤ", SEC_VII),
    ("VIII", "XEM CHI TIẾT", SEC_VIII),
    ("IX", "XÓA PHIẾU GIAO VIỆC", SEC_IX),
    ("X", "VÒNG ĐỜI: PHIẾU CÔNG TÁC - NHẬP KẾT QUẢ - DUYỆT KẾT QUẢ", SEC_X),
    ("XI", "IN / XUẤT EXCEL", SEC_XI),
    ("XII", "SỬA QUA ĐƯỜNG DẪN, ĐỒNG THỜI & LUỒNG ĐẦU - CUỐI", SEC_XII),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu giao việc (ERP) - Cập nhật ngày 02/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

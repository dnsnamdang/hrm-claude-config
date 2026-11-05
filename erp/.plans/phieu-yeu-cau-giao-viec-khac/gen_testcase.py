# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu yeu cau giao viec khac"
(menu Khoi tao > Lap dat - BH -SC > Phieu yeu cau giao viec khac).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :6243-6259 (assign_other_requests)
  app/Http/Controllers/Customercare/AssignOtherRequestController.php searchData, store, edit, update, show,
      delete, reject, getDataAssignTask
  app/Model/Customers/AssignOtherRequest.php STATUSES, canView, canEdit, canDelete, canAssignTask, searchByFilter
  app/Http/Requests/AssignOtherRequestStoreRequest.php
  resources/views/customercare/assign_other_requests/ index, create, edit, show, form, formJS,
      AssignOtherRequest, AssignOtherRequestDetail
  app/Http/Controllers/Sale/Firm/FirmContractController.php getDataAssignOther
  app/Services/Contracts/SearchContractService.php (type assembly_request)
  app/Http/Controllers/Customercare/WrAssignTasksController.php store / delete (doi trang thai yeu cau)

Chay:  python .plans/phieu-yeu-cau-giao-viec-khac/gen_testcase.py
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

MODULE = "Phiếu yêu cầu giao việc khác"

SECTIONS = [
    ("I", "HIỂN THỊ DANH SÁCH & FORM", SEC_I),
    ("II", "PHẠM VI DANH SÁCH", SEC_II),
    ("III", "BỘ LỌC", SEC_III),
    ("IV", "TẠO PHIẾU: KHÁCH HÀNG, ĐỊA CHỈ, THỜI GIAN, PHÒNG TIẾP NHẬN", SEC_IV),
    ("V", "TẠO PHIẾU: HỢP ĐỒNG & DANH SÁCH CẦN GIAO VIỆC", SEC_V),
    ("VI", "LƯU / LƯU VÀ GỬI DUYỆT & THÔNG BÁO", SEC_VI),
    ("VII", "RÀNG BUỘC NHẬP LIỆU", SEC_VII),
    ("VIII", "SỬA / XÓA", SEC_VIII),
    ("IX", "XEM CHI TIẾT & QUYỀN XEM", SEC_IX),
    ("X", "PHÒNG TIẾP NHẬN: KHÔNG DUYỆT", SEC_X),
    ("XI", "CHUYỂN SANG GIAO VIỆC", SEC_XI),
    ("XII", "ĐỒNG THỜI & LUỒNG ĐẦU - CUỐI", SEC_XII),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu yêu cầu giao việc khác (ERP) - Cập nhật ngày 05/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

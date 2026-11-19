# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu giao viec duoc giao"
(menu Bao hanh sua chua > Giao viec > Phieu giao viec duoc giao) - danh sach phia nguoi thuc hien.

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  resources/views/layouts/topmenubar.blade.php :1909 (menu ?type=waiting_import_result)
  routes/web.php :23-32 (nhom hrm khong dang nhap: wr_assign_tasks/{id}/apiShow), :6126-6141 (wr_assign_tasks)
  app/Http/Controllers/Customercare/WrAssignTasksController.php index, searchData (cot, nut hanh dong),
      show, apiShow, printList / exportList (ep type=all)
  app/Model/Customers/WrAssignTask.php STATUSES, canView, canImportResult, canDelete,
      searchByFilter (nhanh waiting_import_result :537-539)
  resources/views/customercare/warranty_repair_assign_tasks/ index (bo loc, search_by_info chi khi type=all),
      show, form (nut Quay lai :1201, khoi nguoi thuc hien da tat :1142-1187)
  app/Http/Controllers/Customercare/WrImportResultsController.php create (khong kiem tra quyen), store
  hrm-api Modules/Assign: AssignRequest::syncAssignBusinessErp (chi ghi nguoi thuc hien khi PCT da duyet),
      clearWrAssignTaskErp, AssignBusinessService::syncWrAssignTaskExecutors (xoa het roi ghi lai),
      AssignBusinessController approve / delete

Chay:  python .plans/phieu-giao-viec-duoc-giao/gen_testcase.py
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
from tc_data_sec_a import SEC_I, SEC_II, SEC_III                # noqa: E402
from tc_data_sec_b import SEC_IV, SEC_V, SEC_VI                 # noqa: E402
from tc_data_sec_c import SEC_VII, SEC_VIII, SEC_IX, SEC_X      # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Phiếu giao việc được giao"

SECTIONS = [
    ("I", "HIỂN THỊ DANH SÁCH", SEC_I),
    ("II", "PHẠM VI: PHIẾU NÀO HIỆN VỚI NGƯỜI THỰC HIỆN", SEC_II),
    ("III", "CỘT VÀ DỮ LIỆU TRÊN DÒNG", SEC_III),
    ("IV", "BỘ LỌC", SEC_IV),
    ("V", "HÀNH ĐỘNG TRÊN DÒNG", SEC_V),
    ("VI", "BÀN GIAO SANG PHIẾU NHẬP KẾT QUẢ", SEC_VI),
    ("VII", "XEM CHI TIẾT", SEC_VII),
    ("VIII", "IN / XUẤT EXCEL", SEC_VIII),
    ("IX", "BẢO MẬT & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu giao việc được giao (ERP) - Cập nhật ngày 13/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

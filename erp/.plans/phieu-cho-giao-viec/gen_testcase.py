# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu cho giao viec"
(menu Bao hanh sua chua > Giao viec > Phieu cho giao viec).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :6141-6157 (wr_assign_tasks), :6035 / :6068 backContract
  app/Http/Controllers/Customercare/WrAssignTasksController.php wait, checkCreate, store, delete
  resources/views/customercare/warranty_repair_assign_tasks/wait.blade.php (5 tab)
  app/Model/Customers/WrServiceContract.php searchByFilter (nhanh assign-task), getQuantityHasRepair,
      canAssignTask, canRejectHandle
  app/Http/Controllers/Customercare/WarrantyRepairContractsController.php searchData, backContract,
      getDataAssignTask
  app/Http/Controllers/Customercare/WarrantyRepairContractAdditionAnnexController.php searchData
  app/Http/Controllers/Customercare/WrWarrantysController.php searchDataWaiting
  app/Model/Customers/AssemblyRequest.php searchByFilter, canAssignTask, getQuantityHasAssemblyRequest
  app/Model/Customers/AssignOtherRequest.php searchByFilter, canAssignTask
  app/Http/Requests/WrAssignTaskStoreRequestWithPlace.php
  app/Http/Controllers/HomeController.php :1846-1871 (o dem trang chu)

Chay:  python .plans/phieu-cho-giao-viec/gen_testcase.py
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

MODULE = "Phiếu chờ giao việc"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & CÁC TAB", SEC_I),
    ("II", "TAB HỢP ĐỒNG - PHẠM VI HIỂN THỊ", SEC_II),
    ("III", "TAB PL BỔ SUNG", SEC_III),
    ("IV", "TAB PHIẾU BẢO HÀNH", SEC_IV),
    ("V", "TAB LẮP ĐẶT BÀN GIAO", SEC_V),
    ("VI", "TAB GIAO VIỆC KHÁC", SEC_VI),
    ("VII", "BỘ LỌC & PHÂN TRANG", SEC_VII),
    ("VIII", "TẠO PHIẾU GIAO VIỆC TỪ DANH SÁCH", SEC_VIII),
    ("IX", "TỪ CHỐI TIẾP NHẬN XỬ LÝ", SEC_IX),
    ("X", "DANH SÁCH THAY ĐỔI SAU KHI GIAO / XÓA PHIẾU GIAO VIỆC", SEC_X),
    ("XI", "Ô ĐẾM TRÊN TRANG CHỦ", SEC_XI),
    ("XII", "ĐỒNG THỜI & LUỒNG ĐẦU - CUỐI", SEC_XII),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu chờ giao việc (ERP) - Cập nhật ngày 02/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

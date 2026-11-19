# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Yeu cau hach toan dich vu - HDBH"
(Ke toan > Ban Dich vu > Yeu cau hach toan dich vu - HDBH; Dich vu > Yeu cau hach toan dich vu - HDBH).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :4175-4187
  app/Http/Controllers/Sale/ServiceAccountingRequestController.php (searchData, store, edit, update, show,
      reject, delete, getDataForServiceAccounting, exportList)
  app/Model/Sale/ServiceAccountingRequest.php (STATUSES, canView / canEdit / canDelete / canAccounting,
      searchByFilter, getDataForEdit, getDataForShow, rollbackAccounting, syncCosts, getDataForExport)
  app/Http/Requests/Sale/ServiceAccountingRequestStoreRequest.php, ServiceAccountingRequestUpdateRequest.php,
      ServiceExportRequestApproveRequest.php
  app/Http/Controllers/Sale/ServiceAccountingController.php :123-200 (ban giao sang phieu hach toan)
  app/Http/Controllers/Sale/Firm/FirmContractController.php :954-972
  app/Services/Sale/Firm/Contract/FirmContractCostService.php :24-110
  app/Datatables/Sale/Firm/FirmContractDatatable.php :179-187, app/Datatables/Sale/ContractDatatable.php
  app/Http/Controllers/HomeController.php :1407-1416
  resources/views/sale/service_accounting_requests/*.blade.php
  resources/views/partials/classes/sale/ServiceAccountingRequest*.blade.php
  resources/views/layouts/topmenubar.blade.php :377, :1102

Chay:  python .plans/yeu-cau-hach-toan-dich-vu-hdbh/gen_testcase.py
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
from tc_data_sec_c import SEC_VIII, SEC_IX, SEC_X, SEC_XI       # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Yêu cầu hạch toán dịch vụ - HĐBH"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH, HÀNH ĐỘNG & XÓA", SEC_III),
    ("IV", "LẬP PHIẾU TỪ HỢP ĐỒNG / ĐƠN HÀNG", SEC_IV),
    ("V", "TÍNH TIỀN & VAT", SEC_V),
    ("VI", "LƯU / GỬI DUYỆT / SỬA", SEC_VI),
    ("VII", "KHÔNG DUYỆT & CHUYỂN SANG PHIẾU HẠCH TOÁN", SEC_VII),
    ("VIII", "XUẤT EXCEL", SEC_VIII),
    ("IX", "RÀNG BUỘC NHẬP LIỆU", SEC_IX),
    ("X", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_X),
    ("XI", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_XI),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Yêu cầu hạch toán dịch vụ - HĐBH (ERP) - Cập nhật ngày 05/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

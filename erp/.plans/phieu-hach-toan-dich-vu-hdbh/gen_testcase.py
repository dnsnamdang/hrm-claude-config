# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu hach toan dich vu - HDBH"
(Ke toan > Hang hoa - Dich vu - Van chuyen > Ban Dich vu > Phieu hach toan dich vu - HDBH).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :4189-4199
  app/Http/Controllers/Sale/ServiceAccountingController.php (index, searchData, create, store, edit,
      update, show, delete, exportList)
  app/Model/Sale/ServiceAccounting.php (STATUSES, canView / canEdit / canDelete, searchByFilter,
      getDataForEdit, getDataForShow, syncItems, syncCosts, getDataForExport)
  app/Http/Requests/Sale/ServiceAccountingStoreRequest.php, ServiceAccountingUpdateRequest.php
  app/Services/Sale/Firm/Contract/FirmContractCostService.php (getDataCostAccounting)
  app/Services/Sale/ServiceAccountingService.php (getDataCreateDept)
  app/Model/Sale/ServiceAccountingRequest.php (STATUSES, canAccounting, searchByFilter)
  app/Http/Controllers/Sale/ServiceAccountingRequestController.php (searchData, reject,
      getDataForServiceAccounting)
  app/Model/Sale/Firm/Contract/FirmContract.php (updateHandoverDate, canRequestAccountingDelivery)
  resources/views/sale/service_accounting/*.blade.php
  resources/views/partials/classes/sale/ServiceAccounting*.blade.php
  resources/views/layouts/topmenubar.blade.php :1103

Chay:  python .plans/phieu-hach-toan-dich-vu-hdbh/gen_testcase.py
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
from tc_data_sec_c import SEC_VIII, SEC_IX, SEC_X, SEC_XI, SEC_XII  # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Phiếu hạch toán dịch vụ - HĐBH"


def renumber(tcs):
    """Danh lai so thu tu 001, 002... de chen TC giua chung khong lech so."""
    return [("%03d" % i,) + tuple(tc[1:]) for i, tc in enumerate(tcs, start=1)]


SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", renumber(SEC_I)),
    ("II", "BỘ LỌC & TÌM KIẾM", renumber(SEC_II)),
    ("III", "DANH SÁCH, HÀNH ĐỘNG & XÓA", renumber(SEC_III)),
    ("IV", "LẬP PHIẾU TỪ PHIẾU YÊU CẦU HẠCH TOÁN DỊCH VỤ", renumber(SEC_IV)),
    ("V", "LƯU / LƯU & DUYỆT / SỬA", renumber(SEC_V)),
    ("VI", "MÀN CHI TIẾT, DUYỆT / KHÔNG DUYỆT", renumber(SEC_VI)),
    ("VII", "BÚT TOÁN & CÔNG NỢ KHÁCH HÀNG", renumber(SEC_VII)),
    ("VIII", "TRẠNG THÁI PHIẾU YÊU CẦU LIÊN QUAN", renumber(SEC_VIII)),
    ("IX", "XUẤT EXCEL", renumber(SEC_IX)),
    ("X", "RÀNG BUỘC NHẬP LIỆU & GỌI THẲNG CHỨC NĂNG", renumber(SEC_X)),
    ("XI", "THAO TÁC ĐỒNG THỜI & CÔ LẬP DỮ LIỆU", renumber(SEC_XI)),
    ("XII", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", renumber(SEC_XII)),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu hạch toán dịch vụ - HĐBH (ERP) - Cập nhật ngày 05/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

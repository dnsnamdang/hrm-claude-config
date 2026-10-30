# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Tong hop gia van chuyen de xuat"
(Van chuyen - Boc xep > Van chuyen voi NCC > Tong hop gia van chuyen de xuat).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :5716-5735
  app/Http/Controllers/Common/DeliveryCostSummaryController.php (searchData, create, store, update, approve,
      delete, deleteFile, updateExtraPrice, updatePayLoadRoads, checkQuotationImport, quotationImport,
      exportExcel)
  app/Model/Common/DeliveryCostSummary.php (STATUSES, searchByFilter, canView / canEdit / canApprove, send,
      approve, excel_data)
  app/Model/Common/DeliveryCostSummaryQuotation.php (markContractCreated - khong noi goi)
  app/Model/Common/DeliveryQuotation.php (canSummaryCost)
  app/ExcelImports/QuotationImport.php
  app/Services/PriceListValidDelivery/PriceListValidDeliveryService.php (create, update)
  resources/views/common/delivery_cost_summaries/*.blade.php
  resources/views/partials/classes/common/DeliveryCostSummary.blade.php (getMinExtraPrice, getMinCost)
  app/Http/Controllers/HomeController.php :1356-1362
  resources/views/layouts/topmenubar.blade.php :1473-1478

Chay:  python .plans/tong-hop-gia-van-chuyen-de-xuat/gen_testcase.py
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

from tc_engine import build                                         # noqa: E402
from tc_data_role import DESCRIPTION_BLOCK, ROLE_TCS                 # noqa: E402
from tc_data_sec_a import SEC_I, SEC_II, SEC_III, SEC_IV             # noqa: E402
from tc_data_sec_b import SEC_V, SEC_VI, SEC_VII                     # noqa: E402
from tc_data_sec_c import SEC_VIII, SEC_IX, SEC_X, SEC_XI, SEC_XII   # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Tổng hợp giá vận chuyển đề xuất"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "DANH SÁCH & HÀNH ĐỘNG THEO TRẠNG THÁI", SEC_III),
    ("IV", "TẠO MỚI TỪ MẪU BÁO GIÁ", SEC_IV),
    ("V", "NHẬP BÁO GIÁ CỦA NCC TỪ FILE EXCEL", SEC_V),
    ("VI", "SỬA GIÁ / BỎ NCC / LƯU / GỬI DUYỆT", SEC_VI),
    ("VII", "MÀN CHI TIẾT & TAB TỔNG HỢP", SEC_VII),
    ("VIII", "DUYỆT / KHÔNG DUYỆT & BẢNG GIÁ HIỆU LỰC", SEC_VIII),
    ("IX", "XUẤT EXCEL", SEC_IX),
    ("X", "XÓA", SEC_X),
    ("XI", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_XI),
    ("XII", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_XII),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Tổng hợp giá vận chuyển đề xuất (ERP) - Cập nhật ngày 30/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

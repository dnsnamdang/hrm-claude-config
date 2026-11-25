# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu Yeu cau hang bao hanh"
(menu Khoi tao > Hoi hang - dat hang - Khieu nai > Phieu Yeu cau hang bao hanh;
 menu Mua hang > Hang bao hanh > Phieu cau hang bao hanh).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :2610-2627 (firm_warranty_requests)
  app/Http/Controllers/Order/FirmWarrantyRequestController.php searchData, store, update, approve, unApprove,
      delete, print, export, printList, exportList, getForFirmWarranty, checkData
  app/Model/Order/FirmWarrantyRequests/FirmWarrantyRequest.php STATUSES, searchByFilter, syncProducts,
      canView, canApprove, canEdit, canDelete, print_data, printListData
  resources/views/orders/firm_warranty_requests/ index, create, edit, show, form, form_show, formJs, partials
  app/Http/Controllers/Order/FirmWarrantyController.php store / update / delete (doi trang thai phieu yeu cau)
  app/Http/Controllers/Order/FirmWarrantyConfirmController.php (Da xac nhan BH)
  app/Http/Controllers/Sale/ManufacturesController.php getDeputy
  app/Http/Controllers/HomeController.php (o cho duyet trang chu)

Chay:  python .plans/phieu-yeu-cau-hang-bao-hanh/gen_testcase.py
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

MODULE = "Phiếu Yêu cầu hãng bảo hành"

SECTIONS = [
    ("I", "HIỂN THỊ DANH SÁCH & FORM", SEC_I),
    ("II", "PHẠM VI DANH SÁCH & DANH SÁCH CHỜ DUYỆT", SEC_II),
    ("III", "BỘ LỌC", SEC_III),
    ("IV", "TẠO PHIẾU: THƯƠNG HIỆU, HÃNG, NGƯỜI NHẬN ĐƠN, CHỌN HÀNG", SEC_IV),
    ("V", "TẠO PHIẾU: KHÁCH HÀNG, HỢP ĐỒNG, BẢO HÀNH BẰNG HÀNG / TIỀN, FILE", SEC_V),
    ("VI", "LƯU / LƯU & GỬI & THÔNG BÁO", SEC_VI),
    ("VII", "RÀNG BUỘC NHẬP LIỆU", SEC_VII),
    ("VIII", "SỬA / XÓA", SEC_VIII),
    ("IX", "XEM CHI TIẾT & KHÔNG DUYỆT", SEC_IX),
    ("X", "LẬP THƯ YÊU CẦU & TRẠNG THÁI SAU ĐÓ", SEC_X),
    ("XI", "IN / XUẤT EXCEL", SEC_XI),
    ("XII", "AN TOÀN DỮ LIỆU, ĐỒNG THỜI & LUỒNG ĐẦU - CUỐI", SEC_XII),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu Yêu cầu hãng bảo hành (ERP) - Cập nhật ngày 25/11/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

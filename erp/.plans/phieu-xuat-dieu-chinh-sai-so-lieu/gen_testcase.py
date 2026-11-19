# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man ERP "Phieu xuat dieu chinh sai so lieu" (phieu xuat lai)
(Kho > Xuat kho > Phieu xuat dieu chinh sai so lieu).

Form mau: 17 cot, dung engine chung
`hrm/.claude/skills/testcase-documenter/assets/tc_engine.py`.

Tai lieu viet theo LOGIC ERP dang chay (repo D:/laragon/www/erp, nhanh gop_db).

Nguon doi chieu (doc truc tiep tu code):
  routes/web.php :1502-1511
  app/Http/Controllers/Warehouse/WarehouseReExportsController.php (all, index, searchData, show, store,
      print, exportList)
  app/Model/Warehouse/WarehouseReExport.php (validateStockQty, updateWarehouse, searchByFilter, canView)
  app/Model/Warehouse/WarehouseImport.php :1415-1423 (canReExport / canReImport), :1071 (type reexport)
  app/Http/Controllers/Warehouse/WarehouseImportsController.php (deny, getDataForReExport, reImport,
      reImportStore :1796-1808)
  app/Helpers/FilterDepartmentHelper.php (applyFilterWithCreatedBy, saveInfo)
  resources/views/warehouse/warehouse_reexports/*.blade.php
  resources/views/partials/classes/warehouse/WarehouseReExport*.blade.php
  resources/views/layouts/topmenubar.blade.php :1362

Chay:  python .plans/phieu-xuat-dieu-chinh-sai-so-lieu/gen_testcase.py
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

MODULE = "Phiếu xuất điều chỉnh sai số liệu"

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", SEC_I),
    ("II", "BỘ LỌC & TÌM KIẾM", SEC_II),
    ("III", "SẮP XẾP, PHÂN TRANG & CHỌN PHIẾU NHẬP KHO", SEC_III),
    ("IV", "XUẤT LẠI & TRỪ TỒN KHO", SEC_IV),
    ("V", "RÀNG BUỘC NHẬP LIỆU & KIỂM TRA TỒN", SEC_V),
    ("VI", "XEM CHI TIẾT", SEC_VI),
    ("VII", "IN & XUẤT EXCEL", SEC_VII),
    ("VIII", "LIÊN KẾT PHIẾU NHẬP KHO & NHẬP LẠI", SEC_VIII),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", SEC_IX),
    ("X", "LUỒNG NGHIỆP VỤ ĐẦU - CUỐI", SEC_X),
]

if __name__ == "__main__":
    build(
        output_file=OUT,
        sheet_name="Trang tính1",
        feature_name="Phiếu xuất điều chỉnh sai số liệu (ERP) - Cập nhật ngày 27/10/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )

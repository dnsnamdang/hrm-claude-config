# -*- coding: utf-8 -*-
"""Generate 3 file testcase ERP cho nhom bao cao cong no khach hang:
- Bang doi chieu cong no 1 khach hang
- Bao cao tong hop cong no khach hang theo nhan vien
- Bao cao chi tiet cong no KH

Viet cho MAN ERP GOC (TanPhatDev, SaleReportsController), de tester nam luong truoc khi nghiem thu
ban HRM da port (sale-customer-debt-reports). Moi file co nhom TC "Tao phieu - so lieu thay doi"
huong dan lap phieu goc roi kiem bao cao tang/giam dung.

Chay:  python gen_testcase.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "hrm", ".claude", "skills", "testcase-documenter", "assets")))
sys.path.insert(0, HERE)

from tc_engine import build  # noqa: E402
import tc_chi_tiet  # noqa: E402
import tc_theo_nhan_vien  # noqa: E402
import tc_doi_chieu  # noqa: E402

JOBS = [
    ("testcase - Bang doi chieu cong no 1 khach hang.xlsx",
     "Bảng đối chiếu công nợ 1 khách hàng (ERP)", tc_doi_chieu),
    ("testcase - BC tong hop cong no KH theo nhan vien.xlsx",
     "Báo cáo tổng hợp công nợ khách hàng theo nhân viên (ERP)", tc_theo_nhan_vien),
    ("testcase - BC chi tiet cong no KH.xlsx",
     "Báo cáo chi tiết công nợ KH (ERP)", tc_chi_tiet),
]

for file_name, feature, mod in JOBS:
    print("=" * 70)
    build(
        output_file=os.path.join(HERE, file_name),
        sheet_name="Trang tính1",
        feature_name=feature,
        module_name="Kinh doanh - Báo cáo công nợ",
        description_block=mod.DESCRIPTION_BLOCK,
        role_tcs=mod.ROLE_TCS,
        sections=mod.SECTIONS,
    )

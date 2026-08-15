# -*- coding: utf-8 -*-
"""Sinh HDSD man 'Danh muc khach hang' (/assign/customers).

Anh that: .plans/gop-db/customer-docs/kh_shots/ (Playwright, 1440x900, 15/08/2026)
Chay:     python .plans/gop-db/customer-docs/gen_hdsd.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "hdsd-documenter", "assets"))
sys.path.insert(0, HERE)
from hdsd_engine import HdsdBuilder  # noqa: E402

b = HdsdBuilder(
    output=os.path.join(HERE, "HDSD_Danh muc khach hang.docx"),
    shots_dir=os.path.join(HERE, "kh_shots"),
    cover_title="(Màn hình: Danh mục khách hàng)",
    doc_title="HDSD - Danh mục khách hàng")

import hdsd_noidung  # noqa: E402

hdsd_noidung.build(b)

b.finish()

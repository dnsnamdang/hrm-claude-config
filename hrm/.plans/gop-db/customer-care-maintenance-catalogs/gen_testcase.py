# -*- coding: utf-8 -*-
"""Sinh testcase (17 cot, 2 khoi tong hop DNS/TP) cho cac man cua feature nay.

Chay:  python .plans/gop-db/customer-care-maintenance-catalogs/gen_testcase.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_catalog_docs_lib"))
sys.path.insert(0, HERE)

from catalog_tc import CatalogTc  # noqa: E402
from mt_config import SCREENS  # noqa: E402

if __name__ == '__main__':
    tong = 0
    for cfg in SCREENS:
        out, n = CatalogTc(cfg, HERE).run()
        tong += n
    print('TONG TAT CA:', tong)

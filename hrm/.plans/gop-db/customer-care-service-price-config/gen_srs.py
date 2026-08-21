# -*- coding: utf-8 -*-
"""Sinh SRS theo FORM MOI (4 phan, chot 2026-08-17).

Chay:  python .plans/gop-db/customer-care-service-price-config/gen_srs.py
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

from catalog_srs import CatalogSrs  # noqa: E402
from sp_config import SCREENS  # noqa: E402

SHOTS = os.path.join(HERE, "sp_shots")

if __name__ == '__main__':
    for cfg in SCREENS:
        out = CatalogSrs(cfg, SHOTS, HERE).build()
        print('->', os.path.basename(out))

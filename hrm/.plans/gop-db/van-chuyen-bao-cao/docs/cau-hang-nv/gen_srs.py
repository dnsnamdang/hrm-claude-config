# -*- coding: utf-8 -*-
"""Sinh SRS màn STT 310 — nội dung + hàm dựng ở cau-hang-ncc/_chung_boc_xep.py (2 màn dùng chung code).
Chạy: python gen_srs.py [--no-word]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'cau-hang-ncc'))
import _chung_boc_xep as C  # noqa: E402

if __name__ == '__main__':
    C.run_srs(HERE, 'nv')

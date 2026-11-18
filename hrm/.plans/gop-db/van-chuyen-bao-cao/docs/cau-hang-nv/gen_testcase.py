# -*- coding: utf-8 -*-
"""Testcase màn STT 310 — khuôn chuẩn skill testcase-documenter (build_chuan, loai bao_cao).
Nội dung case ở cau-hang-ncc/_tc_boc_xep.py (2 màn dùng chung code). Chạy: python gen_testcase.py (tự gọi check_tc — phải 0 lỗi)"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'cau-hang-ncc'))
import _tc_boc_xep as T  # noqa: E402

if __name__ == '__main__':
    T.run(HERE, 'nv')

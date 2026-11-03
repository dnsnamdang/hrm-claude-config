# -*- coding: utf-8 -*-
"""Trỏ sang bản chuẩn trong skill (`testcase-documenter/assets/check_tc.py`). Dùng: python check_tc.py <file.xlsx> <loai>"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '.claude', 'skills',
                                'testcase-documenter', 'assets'))
from check_tc import kiem, THU_TU  # noqa: E402,F401

if __name__ == '__main__':
    sys.exit(0 if kiem(sys.argv[1], sys.argv[2]) else 1)

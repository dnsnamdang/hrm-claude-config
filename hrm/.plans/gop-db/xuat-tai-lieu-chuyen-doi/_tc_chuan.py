# -*- coding: utf-8 -*-
"""Trỏ sang bản chuẩn trong skill (`testcase-documenter/assets/tc_chuan.py`) — giữ file này để các gen_testcase.py
của đợt xuất tài liệu 03/11/2026 (import `_tc_chuan`) vẫn chạy. Sửa khuôn thì sửa ở skill, KHÔNG sửa ở đây."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '.claude', 'skills',
                                'testcase-documenter', 'assets'))
from tc_chuan import build_chuan  # noqa: E402,F401

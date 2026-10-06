# -*- coding: utf-8 -*-
"""Sinh testcase #10455 — CHỈ 1 FILE gộp (user chốt 29/09/2026): chạy gen_testcase_1file.py.
Không sinh lại 10 file lẻ (đã bỏ). Chạy các tc_*.py riêng lẻ sẽ tạo lại file lẻ — đừng chạy trực tiếp.
"""
import os
import runpy

runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_testcase_1file.py"), run_name="__main__")

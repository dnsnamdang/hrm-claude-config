# -*- coding: utf-8 -*-
"""Phần dùng chung cho gen_hdsd_gon.py của 4 màn tài chính/ngân hàng: nạp config cũ + thêm dòng phiên bản rút gọn."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, '..', '..', '_catalog_docs_lib')
sys.path.insert(0, LIB)
from catalog_v2 import load_cfg  # noqa: E402

RUT_GON = 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'


def phien_ban(cfg):
    rows = [list(r) for r in cfg['phien_ban']]
    a, b = rows[-1][0].split('.')
    rows.append(['%s.%d' % (a, int(b) + 1), '29/09/2026', 'Đội phát triển phần mềm', RUT_GON])
    return rows


def thuat_ngu(cfg, bo=('Cổng cũ',)):
    return [list(r) for r in cfg['thuat_ngu'] if r[0] not in bo]

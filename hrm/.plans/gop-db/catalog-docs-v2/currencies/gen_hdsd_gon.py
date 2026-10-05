# -*- coding: utf-8 -*-
"""HDSD Danh mục tiền tệ — bản GỌN (skill hdsd-documenter, 29/09/2026). Chạy: python3 gen_hdsd_gon.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_gen'))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from fin_common import load_cfg, phien_ban, thuat_ngu  # noqa: E402
from hdsd_gon import build  # noqa: E402

C = load_cfg('currencies')
TN = thuat_ngu(C)
for r in TN:
    if r[0].startswith('Tỷ giá'):
        r[1] = r[1].rstrip('.') + '. Hệ thống tự cập nhật lúc 03:00 hằng ngày theo tỷ giá bán của Vietcombank (bỏ qua VNĐ).'

G = {
    'dir': HERE,
    'ten': 'Danh mục tiền tệ',
    'dt': 'tiền tệ',
    'dt_hoa': 'tiền tệ',
    'menu': [('Tài chính', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Danh mục tiền tệ', 'menu_muc')],
    'thuat_ngu': TN,
    'phien_ban': phien_ban(C),
    'quyen': C['quyen']['rows'],
    'bat_buoc': ['Mã tiền tệ', 'Tên tiền tệ', 'Tỷ giá (VNĐ)'],
    'loc': {'o_nhanh': 'mã, tên hoặc tên gọi khác', 'bo_loc': [('trạng thái', 'o_trangthai')]},
    'mo_chi_tiet': 'mã',
    'khoa_icon_thang': True,
    'xoa_cua_so': 'Xác nhận xóa',
    'khoa_cua_so': 'Xác nhận khóa',
    'mokhoa_cua_so': 'Xác nhận mở khóa',
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục tiền tệ.docx')))

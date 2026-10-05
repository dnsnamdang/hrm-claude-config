# -*- coding: utf-8 -*-
"""Phần dùng chung cho 2 SRS: gen_srs_quan_ly_du_an.py + gen_srs_duyet_gia.py.

Ảnh chụp thật (Playwright, 1440x900, nhánh gop_db, client :3002): shots/ — chỉ để local.
Nguồn đối chiếu code (nhánh gop_db) ghi ở đầu từng script.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(HERE, 'shots')


def shot(name):
    return os.path.join(SHOTS, name)


MENU_A = ('Phân hệ Công việc => Thiết lập => Cấu hình chung (Quy chế thu nhập kỹ thuật - công nghệ)'
          ' => Quản lý dự án')
MENU_B = 'Phân hệ Bán hàng => Quy chế - Thiết lập => Cấu hình duyệt giá'

A_CH = 'Người quản trị cấu hình (Q1)'

NO_PERM = ('– Nếu không có quyền → menu không hiển thị; gọi thẳng chức năng thì hiển thị '
           '“Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.')

ICONS = {
    'Phân hệ Công việc': 'icon_phanhe_cv.png',
    'Thiết lập': 'icon_cv_thietlap.png',
    'Cấu hình chung (Quy chế thu nhập kỹ thuật - công nghệ)': 'icon_cv_cauhinhchung.png',
    'Quản lý dự án': 'icon_tab_qlda.png',
    'Cấu hình mức độ ưu tiên': 'icon_tab_uutien.png',
    'Cấu hình hạn': 'icon_tab_han.png',
    'Đóng dự án tự động': 'icon_tab_dong.png',
    'Thêm dòng': 'icon_themdong.png',
    'Sửa': 'icon_sua.png',
    'Xóa': 'icon_xoa.png',
    'Lịch sử thay đổi': 'icon_lichsu.png',
    'Lưu cấu hình': 'icon_luucauhinh.png',
    'Phân hệ Bán hàng': 'icon_phanhe_bh.png',
    'Quy chế - Thiết lập': 'icon_bh_quyche.png',
    'Cấu hình duyệt giá': 'icon_bh_duyetgia.png',
}


def new_doc(ten_man, menu, route, prefix):
    out = os.path.join(HERE, 'SRS - %s.docx' % ten_man)
    d = SrsDoc(out=out, menu=menu, route=route, full_url=route, img_prefix=prefix)
    d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})
    d.title_block(ten_man)
    d.h2('Mục lục')
    d.toc()
    return d

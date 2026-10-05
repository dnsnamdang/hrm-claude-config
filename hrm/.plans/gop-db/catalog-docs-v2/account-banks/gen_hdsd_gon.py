# -*- coding: utf-8 -*-
"""HDSD Danh mục tài khoản ngân hàng — bản GỌN (29/09/2026). Chạy: python3 gen_hdsd_gon.py
Màn không có Xóa; cột Hành động luôn 3 nút hiện thẳng (Sửa, Khóa/Mở khóa, Lịch sử) — không có ba chấm."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_gen'))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from fin_common import load_cfg, phien_ban, thuat_ngu  # noqa: E402
from hdsd_gon import build  # noqa: E402

C = load_cfg('account-banks')


def truycap(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('TRUY CẬP VÀ TÌM KIẾM')
    step(['Bước 1: Từ phân hệ Tài chính ', ic('menu_phanhe'), ', tại menu Danh mục ', ic('menu_nhom'),
          ', chọn Danh mục tài khoản ngân hàng ', ic('menu_muc')])
    c['img']('01_list', 'Màn hình Danh mục tài khoản ngân hàng')
    step(['Bước 2: Nhập số tài khoản, chủ tài khoản hoặc ngân hàng vào ô tìm kiếm nhanh ', ic('o_timnhanh')])
    step(['Bước 3: Nhấn ', ic('btn_timkiem')])
    step(['Bước 4: Nhập tên chi nhánh vào ô ', ic('o_chinhanh'), ' để lọc theo chi nhánh'])
    sub(['Hoặc chọn giá trị ', ic('o_trangthai'), ' để lọc theo trạng thái'])
    step(['Bước 5: Chọn ', ic('btn_lammoi'), ' để xóa giá trị đã lọc'])


def khoa(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('KHÓA')
    step(['Bước 1: Bấm ', ic('btn_khoa_row'), ' ở cột Hành động.'])
    step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận khóa”')
    c['img']('14_lock', 'Hộp xác nhận khóa tài khoản ngân hàng')
    step(['Bước 3: Bấm ', ic('btn_confirm_khoa'), ' để xác nhận'])
    sub(['Hoặc bấm ', ic('btn_huy_confirm'), ' nếu bấm nhầm'])


def lichsu(c):
    ic, step, w = c['ic'], c['step'], c['w']
    c['phan']('XEM LỊCH SỬ THAY ĐỔI')
    w.p('Cách 1: Xem từ màn danh sách:')
    step(['Ở cột Hành động, bấm ', ic('btn_lichsu_row')])
    w.p('Cách 2: Xem từ màn chi tiết:')
    step('Bước 1: Bấm vào số tài khoản để mở cửa sổ xem chi tiết')
    step(['Bước 2: Chọn nút ', ic('btn_xemlichsu')])
    c['img']('16_history', 'Cửa sổ Lịch sử thay đổi')


G = {
    'dir': HERE,
    'ten': 'Danh mục tài khoản ngân hàng',
    'dt': 'tài khoản ngân hàng',
    'dt_hoa': 'tài khoản ngân hàng',
    'menu': [('Tài chính', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Danh mục tài khoản ngân hàng', 'menu_muc')],
    'thuat_ngu': thuat_ngu(C),
    'phien_ban': phien_ban(C),
    'quyen': C['quyen']['rows'],
    'bat_buoc': ['Số tài khoản', 'Loại tiền tệ', 'Chủ tài khoản', 'Ngân hàng', 'Chi nhánh'],
    'loc': {'o_nhanh': 'số tài khoản, chủ tài khoản hoặc ngân hàng',
            'bo_loc': [('chi nhánh', 'o_chinhanh'), ('trạng thái', 'o_trangthai')]},
    'mo_chi_tiet': 'số',
    'mokhoa_cua_so': 'Xác nhận mở khóa',
    'bo': {'xoa'},
    'thay': {'truycap': truycap, 'khoa': khoa, 'lichsu': lichsu},
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục tài khoản ngân hàng.docx')))

# -*- coding: utf-8 -*-
"""HDSD Danh mục tài khoản — bản GỌN (29/09/2026). Chạy: python3 gen_hdsd_gon.py
Riêng màn này: Thêm/Sửa/Chi tiết là TRANG riêng (không phải cửa sổ); có In danh sách; lọc nâng cao 6 ô."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_gen'))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from fin_common import load_cfg, phien_ban, thuat_ngu  # noqa: E402
from hdsd_gon import build  # noqa: E402

C = load_cfg('accounts')
QUYEN = [[r[0], r[1].replace(' — xem dưới', '')] for r in C['quyen']['rows']]


def them(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('THÊM MỚI TÀI KHOẢN')
    step(c['vao'])
    step(['Bước 2: Bấm ', ic('btn_taomoi'), '. Hệ thống mở trang “Thêm tài khoản”.'])
    c['img']('10_create', 'Trang Thêm tài khoản')
    step('Bước 3: Nhập/ chọn đầy đủ thông tin bắt buộc: Số tài khoản, Tên tài khoản, Loại tài khoản, '
         'Bậc tài khoản (Tài khoản mẹ khi Bậc là Cấp 2 hoặc Cấp 3).')
    step(['Bước 4: Bấm ', ic('btn_luu'), ' để lưu và quay về danh sách,'])
    sub(['Hoặc ', ic('btn_luutieptuc'), ' để lưu rồi nhập tiếp tài khoản khác.'])
    sub(['Hoặc ', ic('btn_quaylai'), ' để không lưu thông tin.'])


def sua(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('CHỈNH SỬA')
    step(c['vao'])
    step(['Bước 2: Bấm nút ', ic('btn_sua'), ' ở cột Hành động.'])
    step('Bước 3: Hệ thống mở trang “Sửa tài khoản”.')
    c['img']('12_edit', 'Trang Sửa tài khoản')
    step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Thêm mới).')
    step(['Bước 5: Bấm ', ic('btn_luu'), ' để xác nhận thay đổi'])
    sub(['Hoặc ', ic('btn_quaylai'), ' nếu muốn hủy.'])


def lichsu(c):
    ic, step, sub, w = c['ic'], c['step'], c['sub'], c['w']
    c['phan']('XEM LỊCH SỬ THAY ĐỔI')
    w.p('Cách 1: Xem từ màn danh sách:')
    step(['Ở cột Hành động, bấm ', ic('btn_lichsu_row')])
    sub(['Hoặc bấm ', ic('btn_bacham_row'), ' rồi chọn ', ic('item_lichsu')])
    w.p('Cách 2: Xem từ trang chi tiết:')
    step('Bước 1: Bấm vào số tài khoản để mở trang Chi tiết tài khoản')
    step(['Bước 2: Chọn nút ', ic('btn_xemlichsu')])
    c['img']('16_history', 'Cửa sổ Lịch sử thay đổi')


def chitiet(c):
    c['phan']('XEM CHI TIẾT TÀI KHOẢN')
    c['step'](c['vao'])
    c['step']('Bước 2: Bấm vào số ở cột Số tài khoản. Hệ thống mở trang “Chi tiết tài khoản”.')
    c['img']('17_detail', 'Trang Chi tiết tài khoản ở chế độ chỉ đọc')


def in_ds(c):
    ic, step = c['ic'], c['step']
    c['phan']('IN DANH SÁCH')
    step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    step(['Bước 2: Bấm ', ic('btn_in'), '. Hệ thống mở cửa sổ “Xem trước danh sách tài khoản”.'])
    c['img']('26_print', 'Cửa sổ Xem trước danh sách tài khoản')
    step(['Bước 3: Bấm ', ic('btn_in_preview'), ' để mở hộp thoại in của trình duyệt.'])


G = {
    'dir': HERE,
    'ten': 'Danh mục tài khoản',
    'dt': 'tài khoản',
    'dt_hoa': 'tài khoản',
    'menu': [('Tài chính', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Danh mục tài khoản', 'menu_muc')],
    'thuat_ngu': thuat_ngu(C),
    'phien_ban': phien_ban(C),
    'quyen': QUYEN,
    'bat_buoc': [],
    'loc': {'o_nhanh': 'số hoặc tên tài khoản', 'nang_cao': True,
            'bo_loc': [('bậc tài khoản', 'o_bactaikhoan'), ('loại tài khoản', 'o_loaitaikhoan'),
                       ('theo dõi công nợ', 'o_theodoicongno'), ('trạng thái', 'o_trangthai'),
                       ('người tạo', 'o_nguoitao'), ('người cập nhật', 'o_nguoicapnhat')]},
    'mo_chi_tiet': 'số',
    'khoa_icon_thang': True,
    'xoa_cua_so': 'Xác nhận xóa',
    'khoa_cua_so': 'Xác nhận khóa',
    'mokhoa_cua_so': 'Xác nhận mở khóa',
    'thay': {'them': them, 'sua': sua, 'lichsu': lichsu, 'chitiet': chitiet},
    'them_phan': [('chitiet', in_ds)],
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh muc tai khoan.docx')))

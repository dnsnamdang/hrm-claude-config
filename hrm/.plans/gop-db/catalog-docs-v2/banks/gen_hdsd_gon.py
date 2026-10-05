# -*- coding: utf-8 -*-
"""HDSD Danh mục ngân hàng — bản GỌN (29/09/2026). Chạy: python3 gen_hdsd_gon.py
Riêng màn này: menu 2 cấp (Danh mục → Ngân hàng), Tra cứu ngân hàng chuẩn ở form, cửa sổ Chi nhánh ngân hàng.
Cột Hành động: dòng Hoạt động luôn ≥ 4 nút nên Khóa/Chi nhánh/Lịch sử nằm trong ba chấm; dòng Khóa hiện thẳng."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_gen'))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from fin_common import load_cfg, phien_ban, thuat_ngu  # noqa: E402
from hdsd_gon import build  # noqa: E402

C = load_cfg('banks')


def truycap(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('TRUY CẬP VÀ TÌM KIẾM')
    step(['Bước 1: Từ phân hệ Danh mục ', ic('menu_phanhe'), ', chọn Ngân hàng ', ic('menu_muc')])
    c['img']('01_list', 'Màn hình Danh mục ngân hàng')
    step(['Bước 2: Nhập mã hoặc tên ngân hàng vào ô tìm kiếm nhanh ', ic('o_timnhanh')])
    step(['Bước 3: Nhấn ', ic('btn_timkiem')])
    step(['Bước 4: Nhập tên giao dịch quốc tế vào ô ', ic('o_tengiaodich'), ' để lọc theo tên giao dịch quốc tế'])
    sub(['Hoặc chọn giá trị ', ic('o_trangthai'), ' để lọc theo trạng thái'])
    step(['Bước 5: Chọn ', ic('btn_lammoi'), ' để xóa giá trị đã lọc'])


def them(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('THÊM MỚI NGÂN HÀNG')
    step(c['vao'])
    step(['Bước 2: Bấm ', ic('btn_taomoi')])
    c['img']('10_create', 'Cửa sổ Tạo ngân hàng')
    step('Bước 3: Nhập/ chọn đầy đủ thông tin bắt buộc: Mã ngân hàng, Tên ngân hàng, Tên viết tắt.')
    sub(['Hoặc nhập tên/mã vào ô ', ic('o_goiy'), ', bấm ', ic('btn_tracuu'),
         ' rồi chọn ngân hàng trong danh sách để điền sẵn Mã, Tên, Tên viết tắt, Logo.'])
    step(['Bước 4: Bấm ', ic('btn_luu'), ' để lưu và đóng cửa sổ,'])
    sub(['Hoặc ', ic('btn_luutieptuc'), ' để lưu rồi nhập tiếp ngân hàng khác.'])
    sub(['Hoặc ', ic('btn_dong'), ' để không lưu thông tin.'])


def chinhanh(c):
    """Cửa sổ Chi nhánh ngân hàng: mỗi thao tác = 1 PHẦN (user chốt 29/09/2026)."""
    ic, step, sub, img, phan = c['ic'], c['step'], c['sub'], c['img'], c['phan']
    mo = ['Bước 1: Mở cửa sổ Chi nhánh ngân hàng (xem PHẦN %d).']

    phan('MỞ CỬA SỔ CHI NHÁNH NGÂN HÀNG')
    so_phan_mo = int(c['w'].headings[-1][1].split(':')[0].split()[-1])
    step(['Bước 1: Ở cột Hành động, bấm ', ic('btn_bacham_row'), ' rồi chọn ', ic('item_chinhanh')])
    sub(['Hoặc bấm ', ic('btn_chinhanh_row'), ' (ngân hàng đang Khóa)'])
    step('Bước 2: Hệ thống mở cửa sổ “Chi nhánh ngân hàng”.')
    img('40_branch_list', 'Cửa sổ Chi nhánh ngân hàng')
    b1 = mo[0] % so_phan_mo

    phan('THÊM MỚI CHI NHÁNH NGÂN HÀNG')
    step(b1)
    step(['Bước 2: Bấm ', ic('btn_taomoi_chinhanh')])
    img('41_branch_form', 'Cửa sổ Thêm chi nhánh ngân hàng')
    step('Bước 3: Nhập/ chọn đầy đủ thông tin bắt buộc: Tên chi nhánh ngân hàng, Tỉnh/Thành phố.')
    step(['Bước 4: Bấm ', ic('btn_luu'), ' để lưu và đóng cửa sổ,'])
    sub(['Hoặc ', ic('btn_luutieptuc'), ' để lưu rồi nhập tiếp chi nhánh khác.'])
    sub(['Hoặc ', ic('btn_dong'), ' để không lưu thông tin.'])

    phan('CHỈNH SỬA CHI NHÁNH NGÂN HÀNG')
    step(b1)
    step(['Bước 2: Bấm ', ic('btn_sua'), ' ở dòng chi nhánh cần sửa.'])
    img('43_branch_edit', 'Cửa sổ Sửa chi nhánh ngân hàng')
    step('Bước 3: Nhập thông tin cần sửa (quy tắc nhập như Thêm mới).')
    step(['Bước 4: Bấm ', ic('btn_luu'), ' để xác nhận thay đổi'])
    sub(['Hoặc ', ic('btn_dong'), ' nếu muốn hủy.'])

    phan('XÓA CHI NHÁNH NGÂN HÀNG')
    step(b1)
    step(['Bước 2: Bấm ', ic('btn_xoa'), ' ở dòng chi nhánh.'])
    step('Bước 3: Hệ thống hiện hộp xác nhận “Xóa chi nhánh ngân hàng”')
    img('44_branch_delete', 'Hộp xác nhận xóa chi nhánh ngân hàng')
    step(['Bước 4: Bấm ', ic('btn_confirm_xoa'), ' để xác nhận xóa'])
    sub(['Hoặc bấm ', ic('btn_huy_confirm'), ' nếu bấm nhầm'])

    phan('KHÓA / MỞ KHÓA CHI NHÁNH NGÂN HÀNG')
    step(b1)
    step(['Bước 2: Ở dòng chi nhánh, chọn Khóa ', ic('btn_khoa_row'), ' hoặc ', ic('btn_bacham_row'), ' ', ic('item_khoa')])
    sub(['Hoặc bấm ', ic('btn_mokhoa_row'), ' ở chi nhánh đang Khóa để mở khóa'])
    step('Bước 3: Hệ thống hiện hộp xác nhận “Khóa chi nhánh ngân hàng” (hoặc “Mở khóa chi nhánh ngân hàng”)')
    img('42_branch_lock', 'Hộp xác nhận khóa chi nhánh ngân hàng')
    step(['Bước 4: Bấm ', ic('btn_confirm_khoa'), ' (hoặc ', ic('btn_confirm_mokhoa'), ') để xác nhận'])
    sub(['Hoặc bấm ', ic('btn_huy_confirm'), ' nếu bấm nhầm'])

    phan('XEM LỊCH SỬ CHI NHÁNH NGÂN HÀNG')
    step(b1)
    step(['Bước 2: Ở dòng chi nhánh, bấm ', ic('btn_lichsu_row')])
    sub(['Hoặc bấm ', ic('btn_bacham_row'), ' rồi chọn ', ic('item_lichsu')])
    img('45_branch_history', 'Cửa sổ Lịch sử thay đổi của chi nhánh ngân hàng')


G = {
    'dir': HERE,
    'ten': 'Danh mục ngân hàng',
    'dt': 'ngân hàng',
    'dt_hoa': 'ngân hàng',
    'menu': [('Danh mục', 'menu_phanhe'), ('', ''), ('Ngân hàng', 'menu_muc')],
    'thuat_ngu': thuat_ngu(C),
    'phien_ban': phien_ban(C),
    'quyen': [
        'Phân quyền ai được quyền tạo/ sửa/ xóa/ khóa/ mở khóa sẽ được cập nhật ngay sau khi có tài liệu phân quyền chi tiết của hệ thống.',
        'Tại thời điểm xây dựng HDSD hiện tại, ai đã đăng nhập cũng được quyền truy cập màn hình Danh mục ngân hàng và quyền tạo/sửa/xóa/khóa/mở khóa, quản lý chi nhánh, import, xuất Excel.',
    ],
    'bat_buoc': ['Mã ngân hàng', 'Tên ngân hàng', 'Tên viết tắt'],
    'loc': {},
    'mo_chi_tiet': 'mã',
    'khoa_icon_thang': False,
    'xoa_cua_so': 'Xác nhận xóa',
    'khoa_cua_so': 'Xác nhận khóa',
    'mokhoa_cua_so': 'Xác nhận mở khóa',
    'thay': {'truycap': truycap, 'them': them},
    'them_phan': [('chitiet', chinhanh)],
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục ngân hàng.docx')))

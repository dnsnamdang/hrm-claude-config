# -*- coding: utf-8 -*-
"""HDSD Danh mục công việc, lỗi thiết bị — bản GỌN (skill hdsd-documenter, 29/09/2026).

Khác màn danh mục chuẩn: form Thêm / Sửa / Chi tiết là TRANG RIÊNG (nút ở chân trang), không có Import,
có thêm In danh sách và In chi tiết. Chạy: python3 gen_hdsd_gon.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402

DT = 'công việc / lỗi thiết bị'


def them(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('THÊM MỚI CÔNG VIỆC / LỖI THIẾT BỊ')
    step(c['vao'])
    step(['Bước 2: Bấm ', ic('btn_taomoi'), '. Hệ thống mở trang “Thêm công việc / lỗi thiết bị”.'])
    c['img']('10_create', 'Trang Thêm công việc / lỗi thiết bị')
    step('Bước 3: Nhập/ chọn đầy đủ thông tin bắt buộc: Loại công việc / lỗi, Tên công việc / tình trạng lỗi, '
         'Định mức công, Định mức giảm giá (%), VAT (%), Hệ số công nghệ.')
    step(['Bước 4: Ở khối Áp dụng cho thiết bị, bấm ', ic('btn_thietbi'), ', tích chọn ít nhất 1 thiết bị.'])
    step(['Bước 5: Bấm ', ic('btn_luu_page'), ' để lưu và quay về danh sách,'])
    sub(['Hoặc ', ic('btn_luutieptuc_page'), ' để lưu rồi nhập tiếp hạng mục khác.'])
    sub(['Hoặc ', ic('btn_quaylai_page'), ' để không lưu thông tin.'])


def sua(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('CHỈNH SỬA')
    step(c['vao'])
    step(['Bước 2: Bấm nút ', ic('btn_sua'), ' ở cột Hành động.'])
    step('Bước 3: Hệ thống mở trang “Sửa công việc / lỗi thiết bị”.')
    c['img']('12_edit', 'Trang Sửa công việc / lỗi thiết bị')
    step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Thêm mới).')
    step(['Bước 5: Bấm ', ic('btn_luu_page'), ' để xác nhận thay đổi'])
    sub(['Hoặc ', ic('btn_quaylai_page'), ' nếu muốn hủy.'])


def lichsu(c):
    ic, step, sub, w = c['ic'], c['step'], c['sub'], c['w']
    c['phan']('XEM LỊCH SỬ THAY ĐỔI')
    w.p('Cách 1: Xem từ màn danh sách:')
    step(['Ở cột Hành động, bấm ', ic('btn_bacham_row'), ' rồi chọn ', ic('item_lichsu')])
    sub(['Hoặc bấm ', ic('btn_lichsu_row'), ' ở dòng đang Khóa'])
    w.p('Cách 2: Xem từ màn chi tiết:')
    step('Bước 1: Bấm vào tên công việc / lỗi thiết bị để mở trang chi tiết')
    step(['Bước 2: Ở khối Lịch sử cuối trang, chọn nút ', ic('btn_xemlichsu')])
    c['img']('16_history', 'Cửa sổ Lịch sử thay đổi')


def chitiet(c):
    step = c['step']
    c['phan']('XEM CHI TIẾT CÔNG VIỆC / LỖI THIẾT BỊ')
    step(c['vao'])
    step('Bước 2: Bấm vào tên ở cột Tên công việc / Tình trạng lỗi. Hệ thống mở trang “Chi tiết công việc / lỗi thiết bị”.')
    c['img']('17_detail', 'Trang Chi tiết công việc / lỗi thiết bị')


def in_danh_sach(c):
    ic, step = c['ic'], c['step']
    c['phan']('IN DANH SÁCH')
    step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1).')
    step(['Bước 2: Bấm ', ic('btn_indanhsach'), '. Hệ thống mở cửa sổ “Xem trước danh sách lỗi thiết bị”.'])
    c['img']('30_print_list', 'Cửa sổ Xem trước danh sách lỗi thiết bị')
    step(['Bước 3: Bấm ', ic('btn_in_preview'), ' để in.'])


def in_chi_tiet(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('IN CHI TIẾT CÔNG VIỆC / LỖI THIẾT BỊ')
    step(['Bước 1: Ở cột Hành động, bấm ', ic('btn_bacham_row'), ' rồi chọn ', ic('item_in')])
    sub(['Hoặc bấm ', ic('btn_in_row'), ' ở dòng đang Khóa'])
    step('Bước 2: Hệ thống mở cửa sổ xem trước bản in chi tiết.')
    c['img']('31_print_detail', 'Cửa sổ xem trước bản in chi tiết công việc / lỗi thiết bị')
    step(['Bước 3: Bấm ', ic('btn_in_preview'), ' để in.'])


def in_ca_hai(c):
    in_danh_sach(c)
    in_chi_tiet(c)


G = {
    'dir': HERE,
    'ten': 'Danh mục công việc, lỗi thiết bị',
    'dt': DT,
    'dt_hoa': DT,
    'menu': [('CSKH sau bán', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Công việc, lỗi thiết bị', 'menu_muc')],
    'thuat_ngu': [
        ['Công việc / lỗi thiết bị', 'Một hạng mục công việc sửa chữa hoặc một tình trạng lỗi của thiết bị, dùng làm cơ sở lập báo giá dịch vụ và phiếu sửa chữa.'],
        ['Loại công việc / lỗi', 'Lỗi đã xác định, Lỗi chưa xác định, Lắp đặt bàn giao, Thiết kế nền móng, Tư vấn, khảo sát, Giám sát thi công.'],
        ['Định mức công', 'Số công chuẩn để hoàn thành hạng mục, là căn cứ tính Công kỹ thuật và Đơn giá bán tự động.'],
        ['Áp dụng cho thiết bị', 'Danh sách hàng hóa / thiết bị mà hạng mục áp dụng. Bắt buộc ít nhất một.'],
        ['Trạng thái Hoạt động', 'Hạng mục chọn được khi lập báo giá dịch vụ, phiếu sửa chữa.'],
        ['Trạng thái Khóa', 'Hạng mục không còn chọn được ở nghiệp vụ mới nhưng vẫn nằm trong danh mục, vẫn xem, in và xem lịch sử được.'],
    ],
    'phien_ban': [
        ['1.0', '18/08/2026', 'Đội phát triển phần mềm', 'Lập mới cho màn Danh mục công việc, lỗi thiết bị.'],
        ['1.1', '26/09/2026', 'Đội phát triển phần mềm', 'Cập nhật theo phiên bản hiện tại: bộ lọc, nút ba chấm, cửa sổ Chọn trường xuất file, In danh sách / In chi tiết, màn Chi tiết có khối Lịch sử.'],
        ['1.2', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        ['Quản lý danh mục công việc - lỗi thiết bị', 'Toàn bộ chức năng: Truy cập và tìm kiếm, Thêm mới, Chỉnh sửa, Xóa, Khóa, Mở khóa, Xem chi tiết, Xem lịch sử thay đổi, Xuất Excel, In danh sách, In chi tiết, Tùy chỉnh cột.'],
    ],
    'loc': {'o_nhanh': 'tên công việc / lỗi thiết bị hoặc người tạo', 'nang_cao': True,
            'bo_loc': [('loại', 'o_loai'), ('trạng thái', 'o_trangthai')],
            'khac': 'Hoặc chọn Nhóm hàng hóa, Tên hoặc mã hàng hóa, Người tạo, Người cập nhật, Đơn giá bán, Định mức công để lọc theo từng tiêu chí'},
    'mo_chi_tiet': 'tên',
    'khoa_icon_thang': True,
    'xoa_cua_so': 'Xác nhận xóa',
    'khoa_cua_so': 'Xác nhận khóa',
    'mokhoa_cua_so': 'Xác nhận mở khóa',
    'bo': {'import'},
    'thay': {'them': them, 'sua': sua, 'lichsu': lichsu, 'chitiet': chitiet},
    'them_phan': [('cot', in_ca_hai)],
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục công việc, lỗi thiết bị.docx')))

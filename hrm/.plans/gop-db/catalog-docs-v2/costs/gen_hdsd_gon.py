# -*- coding: utf-8 -*-
"""HDSD Danh mục dịch vụ sửa chữa và chi phí khác — bản GỌN (skill hdsd-documenter, 29/09/2026).
Chạy: python3 gen_hdsd_gon.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402

TEN = 'Danh mục dịch vụ sửa chữa và chi phí khác'


def them(c):
    c['phan']('THÊM MỚI DỊCH VỤ / CHI PHÍ')
    c['step'](c['vao'])
    c['step'](['Bước 2: Bấm ', c['ic']('btn_taomoi')])
    c['img']('10_create', 'Cửa sổ Thêm dịch vụ / chi phí')
    c['step']('Bước 3: Nhập/ chọn đầy đủ thông tin bắt buộc: Tên dịch vụ / chi phí, % Tính giá vốn, % VAT.')
    c['step'](['Bước 4: Bấm ', c['ic']('btn_luu'), ' để lưu và đóng cửa sổ,'])
    c['sub'](['Hoặc ', c['ic']('btn_luutieptuc'), ' để lưu rồi nhập tiếp dịch vụ / chi phí khác.'])
    c['sub'](['Hoặc ', c['ic']('btn_dong'), ' để không lưu thông tin.'])


def import_(c):
    ic, step, sub2 = c['ic'], c['step'], c['sub2']
    c['phan']('IMPORT DỊCH VỤ / CHI PHÍ TỪ FILE EXCEL')
    step(['Bước 1: Tại màn hình danh sách, bấm ', ic('btn_import'),
          '. Hệ thống mở cửa sổ “Import dịch vụ sửa chữa và chi phí khác”.'])
    c['img']('21_import_open', 'Cửa sổ Import dịch vụ sửa chữa và chi phí khác khi vừa mở')
    step(['Bước 2: Bấm ', ic('btn_taifilemau'), ' để lấy file mẫu'])
    step('Bước 3: Điền dữ liệu vào file mẫu.')
    step(['Bước 4: Bấm ', ic('btn_chonfile'), ', chọn file vừa điền'])
    step(['Bước 5: Bấm ', ic('btn_load')])
    c['img']('22_import_loaded', 'Dữ liệu đã được load lên bảng xem trước')
    step(['Bước 6: Bấm ', ic('btn_validate'), ' để hệ thống kiểm tra từng dòng.'])
    c['img']('23_import_validated', 'Kết quả kiểm tra — mỗi dòng lỗi nêu rõ lý do')
    step('Bước 7:')
    sub2('Sửa trực tiếp các dòng lỗi trên bảng rồi bấm Validate lại.')
    sub2(['Nếu không muốn nhập các dòng lỗi thì bấm ', ic('btn_bodongloi')])
    sub2(['Muốn sửa lại những dòng đã khoá, bấm ', ic('btn_xoavalidate')])
    step(['Bước 8: Bấm ', ic('btn_import_modal')])


G = {
    'dir': HERE,
    'ten': TEN,
    'dt': 'dịch vụ / chi phí',
    'dt_hoa': 'dịch vụ / chi phí',
    'menu': [('CSKH sau bán', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Dịch vụ sửa chữa và chi phí khác', 'menu_muc')],
    'thuat_ngu': [
        ['Dịch vụ sửa chữa', 'Hạng mục dịch vụ do đơn vị cung cấp, có tính doanh thu (ô “Dịch vụ có tính doanh thu” được tích).'],
        ['Chi phí khác', 'Khoản chi phí phát sinh trong hoạt động dịch vụ, không tính doanh thu.'],
        ['% Tính giá vốn', 'Tỷ lệ phần trăm dùng để tính giá vốn của dịch vụ.'],
        ['% VAT', 'Thuế suất giá trị gia tăng áp cho dịch vụ / chi phí, từ 0 đến 100.'],
        ['ĐM giảm giá', 'Định mức giảm giá (%), khai báo riêng cho từng công ty.'],
        ['Trạng thái Hoạt động', 'Dòng danh mục đang dùng được ở các nghiệp vụ khác.'],
        ['Trạng thái Khóa', 'Ngừng sử dụng: không sửa, không xóa được; vẫn nằm trong danh mục và vẫn xem được chi tiết, lịch sử.'],
    ],
    'phien_ban': [
        ['1.0', '12/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Danh mục dịch vụ sửa chữa và chi phí khác.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Cập nhật theo phiên bản hiện tại: bộ lọc, Khóa / Mở khóa, Lịch sử, Xem chi tiết, Xuất Excel, Import Excel, Tùy chỉnh cột.'],
        ['1.2', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        ['Xem dịch vụ sửa chữa và chi phí khác', 'Truy cập và tìm kiếm, Xem chi tiết, Xem lịch sử thay đổi, Xuất Excel, Tùy chỉnh cột.'],
        ['Quản lý dịch vụ sửa chữa và chi phí khác', 'Toàn bộ chức năng của quyền Xem, cộng thêm: Thêm mới, Chỉnh sửa, Xóa, Khóa, Mở khóa, Import Excel.'],
    ],
    'bat_buoc': ['Tên dịch vụ / chi phí', '% Tính giá vốn', '% VAT'],
    'loc': {'o_nhanh': 'tên dịch vụ / chi phí',
            'bo_loc': [('phân loại', 'o_phanloai'), ('trạng thái', 'o_trangthai')]},
    'mo_chi_tiet': 'tên',
    'khoa_icon_thang': True,
    'xoa_cua_so': 'Xác nhận xóa',
    'khoa_cua_so': 'Xác nhận khóa',
    'mokhoa_cua_so': 'Xác nhận mở khóa',
    'thay': {'them': them, 'import': import_},
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục dịch vụ sửa chữa và chi phí khác.docx')))

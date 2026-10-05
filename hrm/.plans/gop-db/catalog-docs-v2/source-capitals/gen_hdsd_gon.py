# -*- coding: utf-8 -*-
"""HDSD Danh mục nguồn vốn — bản GỌN (skill hdsd-documenter, 29/09/2026). Chạy: python3 gen_hdsd_gon.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402

G = {
    'dir': HERE,
    'ten': 'Danh mục nguồn vốn',
    'dt': 'nguồn vốn',
    'dt_hoa': 'nguồn vốn',
    'menu': [('Tài chính', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Danh mục nguồn vốn', 'menu_muc')],
    'thuat_ngu': [
        ['Nguồn vốn', 'Nguồn hình thành vốn của khoản chi hoặc tài sản, ví dụ vốn tự có, vốn vay ngân hàng.'],
        ['Tên nguồn vốn', 'Thông tin định danh của nguồn vốn (màn hình không có mã), không được trùng trên toàn hệ thống.'],
        ['Trạng thái Hoạt động', 'Nguồn vốn đang dùng được, sửa / xóa / khóa được.'],
        ['Trạng thái Khóa', 'Nguồn vốn ngừng dùng: vẫn nằm trong danh mục, vẫn xem được chi tiết và lịch sử, nhưng không sửa và không xóa được cho tới khi Mở khóa.'],
    ],
    'phien_ban': [
        ['1.0', '17/08/2026', 'Đội phát triển phần mềm', 'Lập mới cho màn Danh mục nguồn vốn.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Bổ sung Lưu và tiếp tục, Xem chi tiết, Xuất Excel, Import Excel, Tùy chỉnh cột.'],
        ['1.2', '28/09/2026', 'Đội phát triển phần mềm', 'Xóa là xóa hẳn, chỉ khi nguồn vốn đang Hoạt động và chưa được sử dụng; bổ sung Khóa / Mở khóa, ô và bộ lọc Trạng thái.'],
        ['1.3', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        ['Quản lý danh mục nguồn vốn', 'Truy cập và tìm kiếm, Thêm mới, Chỉnh sửa, Xóa, Khóa, Mở khóa, Xem lịch sử, Xem chi tiết, Xuất Excel, Import Excel, Tùy chỉnh cột.'],
    ],
    'bat_buoc': ['Tên nguồn vốn'],
    'loc': {'o_nhanh': 'tên nguồn vốn', 'bo_loc': [('trạng thái', 'o_trangthai')]},
    'mo_chi_tiet': 'tên',
    'khoa_icon_thang': False,
    'xoa_cua_so': 'Xóa nguồn vốn',
    'khoa_cua_so': 'Khóa nguồn vốn',
    'mokhoa_cua_so': 'Mở khóa nguồn vốn',
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục nguồn vốn.docx')))

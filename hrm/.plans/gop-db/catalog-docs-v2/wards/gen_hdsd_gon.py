# -*- coding: utf-8 -*-
"""HDSD Danh mục Phường/Xã — bản GỌN (skill hdsd-documenter, 29/09/2026). Chạy: python3 gen_hdsd_gon.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402

G = {
    'dir': HERE,
    'ten': 'Danh mục Phường/Xã',
    'dt': 'phường/xã',
    'dt_hoa': 'phường/xã',
    'menu': [('Danh mục', 'menu_phanhe'), ('Địa lý', 'menu_nhom'), ('Phường/xã', 'menu_muc')],
    'thuat_ngu': [
        ['Phường/Xã', 'Đơn vị hành chính cấp xã, trực thuộc một Tỉnh/TP. Là cấp cha của Đường/Phố trong cây địa chỉ.'],
        ['Mã số', 'Mã của phường/xã, bắt buộc nhập, chỉ nhận chữ số.'],
        ['Trạng thái Hoạt động', 'Phường/xã dùng được ở các màn nghiệp vụ khác.'],
        ['Trạng thái Khóa', 'Phường/xã không còn chọn được ở nơi khác nhưng vẫn nằm trong danh mục và vẫn xem được lịch sử.'],
    ],
    'phien_ban': [
        ['1.0', '17/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Danh mục Phường/Xã.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Bổ sung Xem chi tiết, Xuất Excel, Import Excel, Tùy chỉnh cột, ô Trạng thái trong cửa sổ Tạo/Sửa.'],
        ['1.2', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        'Phân quyền ai được quyền tạo/ sửa/ xóa/ khóa/ mở khóa sẽ được cập nhật ngay sau khi có tài liệu phân quyền chi tiết của hệ thống.',
        'Tại thời điểm xây dựng HDSD hiện tại, ai cũng được quyền truy cập màn hình danh mục Phường/Xã và quyền tạo/sửa/xóa/khóa/mở khóa, import, xuất Excel.',
    ],
    'bat_buoc': ['Tên phường/xã', 'Mã số', 'Tỉnh/TP', 'Trạng thái'],
    'loc': {'o_nhanh': 'tên phường/xã', 'bo_loc': [('quốc gia', 'o_quocgia'), ('tỉnh/TP', 'o_tinh')]},
    'mo_chi_tiet': 'tên',
    'khoa_icon_thang': False,
    'xoa_cua_so': 'Xóa Phường/Xã',
    'khoa_cua_so': 'Khóa Phường/Xã',
    'mokhoa_cua_so': 'Mở khóa Phường/Xã',
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục Phường-Xã.docx')))

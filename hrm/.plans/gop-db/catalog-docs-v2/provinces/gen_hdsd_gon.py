# -*- coding: utf-8 -*-
"""HDSD Danh mục Tỉnh/TP — bản GỌN (skill hdsd-documenter, 29/09/2026). Chạy: python3 gen_hdsd_gon.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402

G = {
    'dir': HERE,
    'ten': 'Danh mục Tỉnh/TP',
    'dt': 'tỉnh/TP',
    'dt_hoa': 'Tỉnh/TP',
    'menu': [('Danh mục', 'menu_phanhe'), ('Địa lý', 'menu_nhom'), ('Tỉnh/TP', 'menu_muc')],
    'thuat_ngu': [
        ['Tỉnh/TP', 'Đơn vị hành chính cấp tỉnh, trực thuộc một Quốc gia và một Khu vực. Là cấp cha của Quận/Huyện và Phường/Xã trong cây địa chỉ.'],
        ['Mã số tỉnh', 'Mã tham khảo của tỉnh/TP, không bắt buộc, chỉ nhận chữ số.'],
        ['Biển số xe', 'Mã biển số xe của tỉnh/TP, bắt buộc nhập, chỉ nhận chữ số.'],
        ['Trạng thái Hoạt động', 'Tỉnh/TP dùng được ở các màn nghiệp vụ khác.'],
        ['Trạng thái Khóa', 'Tỉnh/TP không còn chọn được ở nơi khác nhưng vẫn nằm trong danh mục và vẫn xem được lịch sử.'],
    ],
    'phien_ban': [
        ['1.0', '17/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Danh mục Tỉnh/TP.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Bổ sung Xem chi tiết, Xuất Excel, Import Excel, Tùy chỉnh cột, ô Trạng thái trong cửa sổ Tạo/Sửa.'],
        ['1.2', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        'Phân quyền ai được quyền tạo/ sửa/ xóa/ khóa/ mở khóa sẽ được cập nhật ngay sau khi có tài liệu phân quyền chi tiết của hệ thống.',
        'Tại thời điểm xây dựng HDSD hiện tại, ai cũng được quyền truy cập màn hình danh mục Tỉnh/TP và quyền tạo/sửa/xóa/khóa/mở khóa, import, xuất Excel.',
    ],
    'bat_buoc': ['Tên tỉnh/TP', 'Biển số xe', 'Quốc gia', 'Khu vực', 'Trạng thái'],
    'loc': {'o_nhanh': 'tên tỉnh/TP', 'bo_loc': [('trạng thái', 'o_trangthai'), ('quốc gia', 'o_quocgia')]},
    'mo_chi_tiet': 'tên',
    'khoa_icon_thang': True,
    'xoa_cua_so': 'Xóa Tỉnh/TP',
    'khoa_cua_so': 'Khóa Tỉnh/TP',
    'mokhoa_cua_so': 'Mở khóa Tỉnh/TP',
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục Tỉnh-TP.docx')))

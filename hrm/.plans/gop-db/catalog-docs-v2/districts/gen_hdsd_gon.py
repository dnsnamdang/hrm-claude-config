# -*- coding: utf-8 -*-
"""HDSD Danh mục Quận/Huyện — bản GỌN (skill hdsd-documenter, 29/09/2026). Chạy: python3 gen_hdsd_gon.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402

G = {
    'dir': HERE,
    'ten': 'Danh mục Quận/Huyện',
    'dt': 'quận/huyện',
    'dt_hoa': 'quận/huyện',
    'menu': [('Danh mục', 'menu_phanhe'), ('Địa lý', 'menu_nhom'), ('Quận/Huyện', 'menu_muc')],
    'thuat_ngu': [
        ['Quận/Huyện', 'Đơn vị hành chính cấp huyện, trực thuộc một Tỉnh/TP.'],
        ['Tỉnh/TP', 'Tỉnh/thành phố mà quận/huyện trực thuộc, chọn từ Danh mục Tỉnh/TP.'],
        ['Trạng thái Hoạt động', 'Quận/huyện dùng được ở các màn nghiệp vụ khác.'],
        ['Trạng thái Khóa', 'Quận/huyện không còn chọn được ở nơi khác nhưng vẫn nằm trong danh mục, vẫn xem được chi tiết và lịch sử.'],
    ],
    'phien_ban': [
        ['1.0', '17/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Danh mục Quận/Huyện.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Bổ sung Xem chi tiết, Xuất Excel, Import Excel, Tùy chỉnh cột.'],
        ['1.2', '28/09/2026', 'Đội phát triển phần mềm', 'Bổ sung Khóa / Mở khóa, ô Trạng thái trong cửa sổ Tạo/Sửa, bộ lọc Trạng thái; Xóa đổi thành xóa hẳn.'],
        ['1.3', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        'Phân quyền ai được quyền tạo/ sửa/ xóa/ khóa/ mở khóa sẽ được cập nhật ngay sau khi có tài liệu phân quyền chi tiết của hệ thống.',
        'Tại thời điểm xây dựng HDSD hiện tại, ai cũng được quyền truy cập màn hình danh mục Quận/Huyện và quyền tạo/sửa/xóa/khóa/mở khóa, import, xuất Excel.',
    ],
    'bat_buoc': ['Tên quận/huyện', 'Tỉnh/TP'],
    'loc': {'o_nhanh': 'tên quận/huyện', 'nang_cao': True,
            'bo_loc': [('quốc gia', 'o_quocgia'), ('tỉnh/TP', 'o_tinh'), ('trạng thái', 'o_trangthai')]},
    'mo_chi_tiet': 'tên',
    'khoa_icon_thang': True,
    'xoa_cua_so': 'Xóa Quận/Huyện',
    'khoa_cua_so': 'Khóa Quận/Huyện',
    'mokhoa_cua_so': 'Mở khóa Quận/Huyện',
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục Quận-Huyện.docx')))

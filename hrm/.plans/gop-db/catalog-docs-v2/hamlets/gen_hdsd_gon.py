# -*- coding: utf-8 -*-
"""HDSD Danh mục Đường/Phố — bản GỌN (skill hdsd-documenter, 29/09/2026). Chạy: python3 gen_hdsd_gon.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402

G = {
    'dir': HERE,
    'ten': 'Danh mục Đường/Phố',
    'dt': 'đường/phố',
    'dt_hoa': 'đường/phố',
    'menu': [('Danh mục', 'menu_phanhe'), ('Địa lý', 'menu_nhom'), ('Đường/Phố', 'menu_muc')],
    'thuat_ngu': [
        ['Đường/Phố', 'Cấp địa chỉ nhỏ nhất trong hệ thống, trực thuộc một Phường/Xã.'],
        ['Quy tắc Việt Nam', 'Khi Quốc gia là Việt Nam, ô Quận/Huyện/Thị xã bị ẩn và không phải nhập. Với quốc gia khác, phải chọn Quận/Huyện/Thị xã trước rồi mới chọn Phường/Xã.'],
        ['Trạng thái Hoạt động', 'Đường/phố dùng được ở các màn nghiệp vụ khác.'],
        ['Trạng thái Khóa', 'Đường/phố không còn chọn được ở nơi khác nhưng vẫn nằm trong danh mục, vẫn xem được chi tiết và lịch sử.'],
    ],
    'phien_ban': [
        ['1.0', '17/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Danh mục Đường/Phố.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Bổ sung Xem chi tiết, Xuất Excel, Import Excel, Tùy chỉnh cột.'],
        ['1.2', '28/09/2026', 'Đội phát triển phần mềm', 'Bổ sung Khóa / Mở khóa, ô Trạng thái trong cửa sổ Tạo/Sửa, bộ lọc Trạng thái; Xóa đổi thành xóa hẳn.'],
        ['1.3', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        'Phân quyền ai được quyền tạo/ sửa/ xóa/ khóa/ mở khóa sẽ được cập nhật ngay sau khi có tài liệu phân quyền chi tiết của hệ thống.',
        'Tại thời điểm xây dựng HDSD hiện tại, ai cũng được quyền truy cập màn hình danh mục Đường/Phố và quyền tạo/sửa/xóa/khóa/mở khóa, import, xuất Excel.',
    ],
    'bat_buoc': ['Tên đường/phố', 'Quốc gia', 'Tỉnh/TP', 'Quận/Huyện/Thị xã (khi quốc gia khác Việt Nam)', 'Phường/xã'],
    'loc': {'o_nhanh': 'tên đường/phố', 'nang_cao': True,
            'bo_loc': [('tỉnh/TP', 'o_tinh'), ('phường/xã', 'o_phuongxa'), ('trạng thái', 'o_trangthai')]},
    'mo_chi_tiet': 'tên',
    'khoa_icon_thang': True,
    'xoa_cua_so': 'Xóa Đường/Phố',
    'khoa_cua_so': 'Khóa Đường/Phố',
    'mokhoa_cua_so': 'Mở khóa Đường/Phố',
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục Đường-Phố.docx')))

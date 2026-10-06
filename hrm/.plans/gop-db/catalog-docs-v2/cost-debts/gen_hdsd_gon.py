# -*- coding: utf-8 -*-
"""HDSD Danh mục mã phí — bản GỌN (skill hdsd-documenter, 29/09/2026). Chạy: python3 gen_hdsd_gon.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402

G = {
    'dir': HERE,
    'ten': 'Danh mục mã phí',
    'dt': 'mã phí',
    'dt_hoa': 'mã phí',
    'menu': [('Tài chính', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Danh mục mã phí', 'menu_muc')],
    'thuat_ngu': [
        ['Mã phí', 'Mã phân loại khoản phí trong kế toán, dùng để tập hợp và đối chiếu chi phí theo từng loại. Mã do người dùng tự đặt, duy nhất trên toàn hệ thống.'],
        ['Trạng thái Hoạt động', 'Mã phí còn chọn được khi lập bút toán mới.'],
        ['Trạng thái Khóa', 'Mã phí không còn chọn được khi lập chứng từ mới, không sửa và không xóa được cho tới khi Mở khóa; vẫn nằm trong danh mục.'],
        ['Mã phí đã được sử dụng', 'Mã phí đã được chọn ở ít nhất một chứng từ. Mã phí đã được sử dụng thì không xóa được (vẫn Khóa được).'],
    ],
    'phien_ban': [
        ['1.0', '17/08/2026', 'Đội phát triển phần mềm', 'Lập mới cho màn Danh mục mã phí.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Bổ sung Lưu và tiếp tục, Xem chi tiết, Xuất Excel, Import Excel, Tùy chỉnh cột.'],
        ['1.2', '28/09/2026', 'Đội phát triển phần mềm', 'Bổ sung Khóa / Mở khóa ở cột Hành động; Xóa là xóa hẳn, chỉ khi mã phí đang Hoạt động và chưa được sử dụng.'],
        ['1.3', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        ['Quản lý danh mục mã phí', 'Truy cập và tìm kiếm, Thêm mới, Chỉnh sửa, Xóa, Khóa, Mở khóa, Xem lịch sử, Xem chi tiết, Xuất Excel, Import Excel, Tùy chỉnh cột.'],
    ],
    'bat_buoc': ['Mã phí', 'Tên mã phí'],
    'loc': {'o_nhanh': 'mã hoặc tên mã phí', 'nang_cao': True, 'bo_loc': [('trạng thái', 'o_trangthai')],
            'khac': 'Hoặc chọn Người tạo, Người cập nhật để lọc theo từng tiêu chí'},
    'mo_chi_tiet': 'mã của',
    'khoa_icon_thang': True,
    'xoa_cua_so': 'Xóa mã phí',
    'khoa_cua_so': 'Khóa mã phí',
    'mokhoa_cua_so': 'Mở khóa mã phí',
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục mã phí.docx')))

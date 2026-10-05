# -*- coding: utf-8 -*-
"""HDSD Danh mục vụ việc — bản GỌN (skill hdsd-documenter, 29/09/2026). Chạy: python3 gen_hdsd_gon.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402

G = {
    'dir': HERE,
    'ten': 'Danh mục vụ việc',
    'dt': 'vụ việc',
    'dt_hoa': 'vụ việc',
    'menu': [('Tài chính', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Danh mục vụ việc', 'menu_muc')],
    'thuat_ngu': [
        ['Vụ việc', 'Đối tượng tập hợp chi phí và doanh thu trong kế toán, dùng để theo dõi hiệu quả của từng công việc hoặc từng hợp đồng.'],
        ['Mã vụ việc', 'Mã do người dùng tự đặt, duy nhất trên toàn hệ thống, dùng để chọn nhanh khi lập bút toán.'],
        ['Trạng thái Hoạt động', 'Vụ việc còn chọn được khi lập bút toán mới.'],
        ['Trạng thái Khóa', 'Vụ việc không còn chọn được khi lập chứng từ mới, không sửa và không xóa được cho tới khi Mở khóa; vẫn nằm trong danh mục.'],
        ['Vụ việc đã được sử dụng', 'Vụ việc đã được chọn ở ít nhất một chứng từ. Vụ việc đã được sử dụng thì không xóa được (vẫn Khóa được).'],
    ],
    'phien_ban': [
        ['1.0', '17/08/2026', 'Đội phát triển phần mềm', 'Lập mới cho màn Danh mục vụ việc.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Bổ sung Lưu và tiếp tục, Xem chi tiết, Xuất Excel, Import Excel, Tùy chỉnh cột.'],
        ['1.2', '28/09/2026', 'Đội phát triển phần mềm', 'Bổ sung Khóa / Mở khóa ở cột Hành động; Xóa là xóa hẳn, chỉ khi vụ việc đang Hoạt động và chưa được sử dụng.'],
        ['1.3', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        ['Quản lý danh mục vụ việc', 'Truy cập và tìm kiếm, Thêm mới, Chỉnh sửa, Xóa, Khóa, Mở khóa, Xem lịch sử, Xem chi tiết, Xuất Excel, Import Excel, Tùy chỉnh cột.'],
    ],
    'bat_buoc': ['Mã vụ việc', 'Tên vụ việc'],
    'loc': {'o_nhanh': 'mã hoặc tên vụ việc', 'nang_cao': True, 'bo_loc': [('trạng thái', 'o_trangthai')],
            'khac': 'Hoặc chọn Người tạo, Người cập nhật để lọc theo từng tiêu chí'},
    'mo_chi_tiet': 'mã của',
    'khoa_icon_thang': True,
    'xoa_cua_so': 'Xóa vụ việc',
    'khoa_cua_so': 'Khóa vụ việc',
    'mokhoa_cua_so': 'Mở khóa vụ việc',
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục vụ việc.docx')))

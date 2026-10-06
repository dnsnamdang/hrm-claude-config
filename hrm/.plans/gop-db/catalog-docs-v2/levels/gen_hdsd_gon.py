# -*- coding: utf-8 -*-
"""HDSD Cấp dịch vụ bảo dưỡng — bản GỌN (skill hdsd-documenter, 29/09/2026). Chạy: python3 gen_hdsd_gon.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402

G = {
    'dir': HERE,
    'ten': 'Cấp dịch vụ bảo dưỡng',
    'dt': 'cấp dịch vụ',
    'dt_hoa': 'cấp dịch vụ',
    'menu': [('CSKH sau bán', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Cấp dịch vụ bảo dưỡng', 'menu_muc')],
    'thuat_ngu': [
        ['Cấp dịch vụ bảo dưỡng', 'Mức phân loại công việc bảo dưỡng theo mốc thời gian hoặc số giờ vận hành của thiết bị, ví dụ “Cấp 1 (6T)”, “Cấp 1 (12T/2500h)”.'],
        ['Trạng thái Hoạt động', 'Cấp dịch vụ còn chọn được khi lập gói bảo dưỡng mới và khi chọn gói trong báo giá dịch vụ.'],
        ['Trạng thái Khóa', 'Cấp dịch vụ không còn chọn được ở chứng từ mới, không sửa và không xóa được cho tới khi Mở khóa; vẫn nằm trong danh mục.'],
        ['Cấp đang được sử dụng', 'Cấp đã xuất hiện ở gói bảo dưỡng, báo giá, hợp đồng hoặc phiếu dịch vụ. Cấp đang được sử dụng thì không xóa được (vẫn Khóa được).'],
    ],
    'phien_ban': [
        ['1.0', '13/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Cấp dịch vụ bảo dưỡng.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Bấm tên để Xem chi tiết, bổ sung Lịch sử thay đổi, Xuất Excel, Import Excel, Tùy chỉnh cột.'],
        ['1.2', '28/09/2026', 'Đội phát triển phần mềm', 'Bổ sung trạng thái Hoạt động / Khóa, bộ lọc Trạng thái, Khóa / Mở khóa ở cột Hành động; Xóa là xóa hẳn, chỉ khi cấp đang Hoạt động và chưa được sử dụng.'],
        ['1.3', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        ['Xem cấp dịch vụ bảo dưỡng', 'Truy cập và tìm kiếm, Xem chi tiết, Xem lịch sử thay đổi, Xuất Excel, Tùy chỉnh cột.'],
        ['Quản lý cấp dịch vụ bảo dưỡng', 'Toàn bộ chức năng của quyền Xem, cộng thêm: Thêm mới, Chỉnh sửa, Xóa, Khóa, Mở khóa, Import Excel.'],
    ],
    'bat_buoc': ['Tên cấp'],
    'loc': {'o_nhanh': 'tên cấp dịch vụ', 'bo_loc': [('trạng thái', 'o_trangthai')]},
    'mo_chi_tiet': 'tên',
    'khoa_icon_thang': True,
    'xoa_cua_so': 'Xác nhận xóa',
    'khoa_cua_so': 'Khóa cấp dịch vụ',
    'mokhoa_cua_so': 'Mở khóa cấp dịch vụ',
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Cấp dịch vụ bảo dưỡng.docx')))

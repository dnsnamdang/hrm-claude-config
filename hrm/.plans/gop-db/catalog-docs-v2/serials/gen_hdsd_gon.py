# -*- coding: utf-8 -*-
"""HDSD Danh mục serial thiết bị làm dịch vụ — bản GỌN (skill hdsd-documenter, 29/09/2026).
Màn CHỈ ĐỌC: chỉ có Truy cập & tìm kiếm, Xuất Excel, Tùy chỉnh cột. Chạy: python3 gen_hdsd_gon.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402

G = {
    'dir': HERE,
    'ten': 'Danh mục serial thiết bị làm dịch vụ',
    'dt': 'serial',
    'dt_hoa': 'serial',
    'menu': [('CSKH sau bán', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Serial thiết bị làm dịch vụ', 'menu_muc')],
    'thuat_ngu': [
        ['Serial', 'Số serial in trên thiết bị, dùng để nhận diện thiết bị khi làm dịch vụ.'],
        ['Tên hàng', 'Mặt hàng / thiết bị tương ứng với serial.'],
        ['Khách hàng', 'Khách hàng đang sở hữu thiết bị, hiển thị dạng mã - tên.'],
        ['Đang sử dụng', 'Thiết bị còn đang được khách hàng sử dụng và còn làm dịch vụ.'],
        ['Ngưng sử dụng', 'Thiết bị đã ngừng sử dụng hoặc không còn làm dịch vụ nữa.'],
        ['Màn Quản lý khách hàng', 'Nơi thêm, sửa, đổi trạng thái hoặc xóa serial (tab Trang thiết bị của khách hàng). Màn này chỉ để tra cứu.'],
    ],
    'phien_ban': [
        ['1.0', '13/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Danh mục serial thiết bị làm dịch vụ.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Cập nhật theo phiên bản hiện tại: bộ lọc nâng cao, cửa sổ Chọn trường xuất file, Tùy chỉnh cột.'],
        ['1.2', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        ['Xem danh mục serial thiết bị làm dịch vụ', 'Truy cập và tìm kiếm, Xuất Excel, Tùy chỉnh cột.'],
    ],
    'loc': {'o_nhanh': 'serial, tên hàng hoặc khách hàng', 'nang_cao': True,
            'bo_loc': [('khách hàng', 'o_khachhang'), ('trạng thái', 'o_trangthai')],
            'khac': 'Hoặc chọn Người tạo, Người cập nhật để lọc theo từng tiêu chí'},
    'bo': {'them', 'sua', 'xoa', 'khoa', 'mokhoa', 'lichsu', 'chitiet', 'import'},
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục serial thiết bị làm dịch vụ.docx')))

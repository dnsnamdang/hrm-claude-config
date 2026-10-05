# -*- coding: utf-8 -*-
"""HDSD Danh mục ghi chú kiểm tra bảo dưỡng — bản GỌN (skill hdsd-documenter, 29/09/2026).
Chạy: python3 gen_hdsd_gon.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402


def import_(c):
    ic, step, sub2 = c['ic'], c['step'], c['sub2']
    c['phan']('IMPORT GHI CHÚ KIỂM TRA TỪ FILE EXCEL')
    step(['Bước 1: Tại màn hình danh sách, bấm ', ic('btn_import'),
          '. Hệ thống mở cửa sổ “Import ghi chú kiểm tra bảo dưỡng”.'])
    c['img']('21_import_open', 'Cửa sổ Import ghi chú kiểm tra bảo dưỡng khi vừa mở')
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
    'ten': 'Danh mục ghi chú kiểm tra bảo dưỡng',
    'dt': 'ghi chú kiểm tra',
    'dt_hoa': 'ghi chú kiểm tra',
    'menu': [('CSKH sau bán', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Ghi chú kiểm tra bảo dưỡng', 'menu_muc')],
    'thuat_ngu': [
        ['Ghi chú kiểm tra bảo dưỡng', 'Một hạng mục công việc kiểm tra thực hiện khi bảo dưỡng thiết bị, ví dụ “Kiểm tra ngoại quan không tháo lắp”.'],
        ['Hạng mục', 'Tên đầy đủ của công việc kiểm tra, không được trùng.'],
        ['Ký hiệu', 'Mã viết tắt của hạng mục (ví dụ KTBM, DK, CC), không được trùng, tự chuyển thành chữ IN HOA khi lưu.'],
        ['Mô tả', 'Diễn giải chi tiết hạng mục kiểm tra, không bắt buộc.'],
        ['Trạng thái Hoạt động', 'Ghi chú còn chọn được khi khai báo nội dung kiểm tra cho cấp bảo dưỡng của gói bảo dưỡng.'],
        ['Trạng thái Khóa', 'Ghi chú ngừng dùng: không còn chọn được ở gói bảo dưỡng mới; vẫn nằm trong danh mục, vẫn xem được chi tiết và lịch sử.'],
    ],
    'phien_ban': [
        ['1.0', '13/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Danh mục ghi chú kiểm tra bảo dưỡng.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Bổ sung Xem chi tiết, Lịch sử thay đổi, cửa sổ Chọn trường xuất file, Import Excel, Tùy chỉnh cột.'],
        ['1.2', '28/09/2026', 'Đội phát triển phần mềm', 'Bổ sung trạng thái Hoạt động / Khóa và chức năng Khóa / Mở khóa.'],
        ['1.3', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        ['Xem ghi chú kiểm tra bảo dưỡng', 'Truy cập và tìm kiếm, Xem chi tiết, Xem lịch sử thay đổi, Xuất Excel, Tùy chỉnh cột.'],
        ['Quản lý ghi chú kiểm tra bảo dưỡng', 'Toàn bộ chức năng của quyền Xem, cộng thêm: Thêm mới, Chỉnh sửa, Xóa, Khóa, Mở khóa, Import Excel.'],
    ],
    'bat_buoc': ['Hạng mục', 'Ký hiệu'],
    'loc': {'o_nhanh': 'hạng mục hoặc ký hiệu', 'bo_loc': [('trạng thái', 'o_trangthai')]},
    'mo_chi_tiet': 'hạng mục của',
    'khoa_icon_thang': True,
    'xoa_cua_so': 'Xác nhận xóa',
    'khoa_cua_so': 'Khóa ghi chú kiểm tra',
    'mokhoa_cua_so': 'Mở khóa ghi chú kiểm tra',
    'thay': {'import': import_},
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục ghi chú kiểm tra bảo dưỡng.docx')))

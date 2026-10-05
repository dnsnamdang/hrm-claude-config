# -*- coding: utf-8 -*-
"""HDSD Danh mục gói bảo dưỡng — bản GỌN (skill hdsd-documenter, 29/09/2026). Chạy: python3 gen_hdsd_gon.py

Ảnh/icon copy từ customer-care-services-catalog/docs_v2 (bộ sinh bản chi tiết cũ) sang shots/ icons/ ở đây,
đổi tên theo chuẩn hdsd_gon (10_create, 12_edit, 13_delete…); chụp bổ sung 29/09: 14_lock, item_*, o_*,
btn_khoa_row, btn_bacham_row, btn_confirm_khoa, btn_huy_confirm, btn_in_modal.
Form Thêm/Sửa/Nhân bản/Chi tiết là TRANG riêng (không phải popup) → viết qua 'thay'.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402


def them(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('THÊM MỚI GÓI BẢO DƯỠNG')
    step(c['vao'])
    step(['Bước 2: Bấm ', ic('btn_taomoi'), '. Hệ thống mở trang “Thêm gói bảo dưỡng”.'])
    c['img']('10_create', 'Trang Thêm gói bảo dưỡng')
    step('Bước 3: Nhập/ chọn đầy đủ thông tin bắt buộc: Tên gói bảo dưỡng, Mã gói bảo dưỡng, Công ty quản lý gói bảo dưỡng.')
    step(['Bước 4: Bấm ', ic('btn_themdong'), ', nhập Nội dung kiểm tra bảo dưỡng, chọn ĐVT, nhập SL.'])
    step(['Bước 5: Bấm ', ic('btn_themcot'), ' ở tiêu đề bảng để thêm cột, chọn Cấp bảo dưỡng; chọn Ghi chú kiểm tra ở từng ô và nhập Định mức công của cấp.'])
    step(['Bước 6: Bấm ', ic('btn_chonhanghoa'), ' hoặc ', ic('btn_chonnhomhang'), ' để chọn hàng hóa áp dụng.'])
    step(['Bước 7: Bấm ', ic('btn_themtailieu'), ' để đính kèm file PDF.'])
    step(['Bước 8: Bấm ', ic('btn_luu'), ' để lưu và quay về danh sách,'])
    sub(['Hoặc ', ic('btn_luutieptuc'), ' để lưu rồi nhập tiếp gói khác.'])
    sub(['Hoặc ', ic('btn_quaylai'), ' để không lưu thông tin.'])


def sua(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('CHỈNH SỬA')
    step(c['vao'])
    step(['Bước 2: Bấm nút ', ic('btn_sua'), ' ở cột Hành động.'])
    sub(['Hoặc bấm ', ic('btn_sua_footer'), ' ở chân trang Chi tiết gói bảo dưỡng.'])
    step('Bước 3: Hệ thống mở trang “Sửa gói bảo dưỡng”.')
    c['img']('12_edit', 'Trang Sửa gói bảo dưỡng')
    step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Thêm mới).')
    step(['Bước 5: Bấm ', ic('btn_luu'), ' để xác nhận thay đổi'])
    sub(['Hoặc ', ic('btn_quaylai'), ' nếu muốn hủy.'])


def nhanban(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('NHÂN BẢN GÓI BẢO DƯỠNG')
    step(['Bước 1: Bấm ', ic('btn_bacham_row'), ' ở cột Hành động, chọn ', ic('item_nhanban')])
    sub(['Hoặc bấm ', ic('btn_nhanban'), ' (gói đang Khóa), hoặc ', ic('btn_nhanban_footer'), ' ở chân trang Chi tiết.'])
    step('Bước 2: Hệ thống mở trang “Sao chép gói bảo dưỡng” với dữ liệu của gói nguồn.')
    c['img']('46_copy_top', 'Trang Sao chép gói bảo dưỡng')
    step('Bước 3: Sửa Tên gói bảo dưỡng và Mã gói bảo dưỡng cho khác gói nguồn, chỉnh các thông tin khác nếu cần.')
    step(['Bước 4: Bấm ', ic('btn_luu'), ' để lưu'])
    sub(['Hoặc ', ic('btn_quaylai'), ' để không lưu thông tin.'])


def in_(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('IN PHIẾU DANH MỤC KIỂM TRA BẢO DƯỠNG')
    step(['Bước 1: Bấm ', ic('btn_bacham_row'), ' ở cột Hành động, chọn ', ic('item_in')])
    sub(['Hoặc bấm ', ic('btn_in_footer'), ' ở chân trang Chi tiết gói bảo dưỡng.'])
    step('Bước 2: Hệ thống mở cửa sổ “Xem trước gói bảo dưỡng <mã gói>”.')
    c['img']('51_print', 'Cửa sổ Xem trước gói bảo dưỡng')
    step(['Bước 3: Bấm ', ic('btn_in_modal'), ' để in.'])


def lichsu(c):
    ic, step, w = c['ic'], c['step'], c['w']
    c['phan']('XEM LỊCH SỬ THAY ĐỔI')
    w.p('Cách 1: Xem từ màn danh sách:')
    step(['Ở cột Hành động, bấm ', ic('btn_bacham_row'), ' rồi chọn ', ic('item_lichsu')])
    w.p('Cách 2: Xem từ màn chi tiết:')
    step('Bước 1: Bấm vào mã gói để mở trang Chi tiết gói bảo dưỡng')
    step(['Bước 2: Chọn nút ', ic('btn_xemlichsu')])
    c['img']('16_history', 'Cửa sổ Lịch sử thay đổi')


def chitiet(c):
    step = c['step']
    c['phan']('XEM CHI TIẾT GÓI BẢO DƯỠNG')
    step(c['vao'])
    step('Bước 2: Bấm vào mã gói ở cột Mã. Hệ thống mở trang “Chi tiết gói bảo dưỡng: <mã gói>”.')
    c['img']('17_detail', 'Trang Chi tiết gói bảo dưỡng')


G = {
    'dir': HERE,
    'ten': 'Danh mục gói bảo dưỡng',
    'dt': 'gói bảo dưỡng',
    'dt_hoa': 'gói bảo dưỡng',
    'menu': [('CSKH sau bán', 'menu_phanhe'), ('Danh mục', 'menu_danhmuc'), ('Gói bảo dưỡng', 'menu_goibaoduong')],
    'thuat_ngu': [
        ['Gói bảo dưỡng', 'Một bản ghi của danh mục: gồm thông tin chung, bảng nội dung kiểm tra theo từng cấp, giá theo từng công ty, hàng hóa áp dụng và file PDF kèm theo.'],
        ['Cấp bảo dưỡng', 'Mức độ bảo dưỡng lấy từ danh mục Cấp dịch vụ bảo dưỡng. Trong bảng nội dung kiểm tra, mỗi cấp là MỘT CỘT.'],
        ['Nội dung kiểm tra bảo dưỡng', 'Một hạng mục phải làm khi bảo dưỡng, kèm Đơn vị tính và Số lượng. Mỗi hạng mục là MỘT DÒNG.'],
        ['Ghi chú kiểm tra', 'Ký hiệu công việc tại ô giao giữa một nội dung và một cấp (KTBM, DK, CC, VS…).'],
        ['Gói đã được sử dụng', 'Gói đã được chọn ở chứng từ (báo giá, hợp đồng dịch vụ…). Gói này không xóa được, chỉ khóa được.'],
        ['Trạng thái Hoạt động', 'Gói dùng được ở các màn nghiệp vụ khác.'],
        ['Trạng thái Khóa', 'Gói ngừng sử dụng nhưng vẫn nằm trong danh mục; không sửa, không xóa được cho tới khi Mở khóa.'],
    ],
    'phien_ban': [
        ['1.0', '17/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Danh mục gói bảo dưỡng.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Bổ sung Import Excel, ô Trạng thái ở màn Tạo mới/Sửa, Xem chi tiết, In xem trước, lịch sử thay đổi.'],
        ['1.2', '28/09/2026', 'Đội phát triển phần mềm', 'Gói đã được sử dụng thì không xóa, chỉ khóa; bổ sung nút Khóa ở cột Hành động.'],
        ['1.3', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        ['Thêm danh mục gói bảo dưỡng', 'Thêm mới, Nhân bản, Import Excel.'],
        ['Sửa danh mục gói bảo dưỡng', 'Chỉnh sửa, Khóa, Mở khóa.'],
        ['Xóa danh mục gói bảo dưỡng', 'Xóa (gói đang Hoạt động và chưa được sử dụng).'],
        ['(Không cần quyền riêng)', 'Truy cập và tìm kiếm, Xem chi tiết, In, Xem lịch sử thay đổi, Xuất Excel, Tùy chỉnh cột.'],
    ],
    'loc': {'o_nhanh': 'tên hoặc mã gói bảo dưỡng',
            'bo_loc': [('trạng thái', 'o_trangthai'), ('người tạo', 'o_nguoitao')]},
    'mo_chi_tiet': 'mã',
    'khoa_icon_thang': True,
    'xoa_cua_so': 'Xác nhận xóa',
    'khoa_cua_so': 'Xác nhận khóa',
    'mokhoa_cua_so': 'Xác nhận mở khóa',
    'thu_tu': ['truycap', 'them', 'sua', 'xoa', 'khoa', 'mokhoa', 'nhanban', 'in', 'lichsu', 'chitiet',
               'xuat', 'import', 'cot'],
    'thay': {'them': them, 'sua': sua, 'nhanban': nhanban, 'in': in_, 'lichsu': lichsu, 'chitiet': chitiet},
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh mục gói bảo dưỡng.docx')))

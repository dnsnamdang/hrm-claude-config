# -*- coding: utf-8 -*-
"""HDSD Danh mục khách hàng — bản GỌN (skill hdsd-documenter, 29/09/2026). Chạy: python3 gen_hdsd_gon.py

Thêm/Sửa/Chi tiết/Quản lý là TRANG riêng; màn Quản lý có 6 thẻ, thẻ Danh sách trang thiết bị có nhiều thao
tác (thiết bị, serial) → mỗi thao tác 1 PHẦN (skill: màn phụ nhiều thẻ, thẻ có thao tác = 1 PHẦN riêng).
Không có chức năng Xóa khách hàng. Bảng Quyền + Thuật ngữ lấy từ bản trên Drive (tester đã sửa tay 28/09).
Chụp bổ sung 29/09: o_timnhanh, item_quanly, item_lichsu (cắt lại cho sát).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402

QL = 'Bước 1: Mở màn Quản lý khách hàng (xem PHẦN 9), bấm thẻ “%s”.'
TB = 'Bước 1: Mở thẻ “Danh sách trang thiết bị” của màn Quản lý khách hàng (xem PHẦN 13).'


def truycap(c):
    ic, step = c['ic'], c['step']
    c['phan']('TRUY CẬP VÀ TÌM KIẾM')
    step(['Bước 1: Từ phân hệ Danh mục ', ic('menu_phanhe'), ', tại menu Đối tác ', ic('menu_nhom'),
          ', chọn Khách hàng ', ic('menu_muc')])
    c['img']('01_list', 'Màn hình Danh mục khách hàng')
    step(['Bước 2: Nhập mã KH, tên KH, MST, SĐT hoặc người tạo vào ô tìm kiếm nhanh ', ic('o_timnhanh')])
    step(['Bước 3: Nhấn ', ic('btn_timkiem')])
    step(['Bước 4: Bấm ', ic('btn_timkiemnangcao'), ', chọn tiêu chí trong khối bộ lọc chi tiết để lọc thêm'])
    step(['Bước 5: Chọn ', ic('btn_lammoi'), ' để xóa giá trị đã lọc'])


def them(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('THÊM MỚI KHÁCH HÀNG')
    step(c['vao'])
    step(['Bước 2: Bấm ', ic('btn_taomoi'), '. Hệ thống mở trang “Tạo khách hàng mới”.'])
    c['img']('10_create', 'Trang Tạo khách hàng mới')
    step('Bước 3: Chọn Loại hình tổ chức.')
    step('Bước 4: Nhập/ chọn đầy đủ thông tin bắt buộc: Tên khách hàng, Quốc gia, Tỉnh/Thành phố, '
         'Phường/Xã/Thị trấn; khách hàng cá nhân thêm Số điện thoại; khách hàng tổ chức thêm Mã số thuế, '
         'Địa chỉ xuất hóa đơn, Người đại diện, Người liên hệ.')
    step(['Bước 5: Bấm ', ic('btn_luu_kh'), ' để lưu. Hệ thống tự sinh Mã khách hàng.'])
    sub(['Hoặc ', ic('btn_quaylai_kh'), ' để không lưu thông tin.'])


def sua(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('CHỈNH SỬA')
    step(c['vao'])
    step(['Bước 2: Bấm nút ', ic('btn_sua_kh'), ' ở cột Hành động.'])
    sub(['Hoặc bấm ', ic('btn_sua_footer_kh'), ' ở chân trang Chi tiết khách hàng.'])
    step('Bước 3: Hệ thống mở trang “Chỉnh sửa khách hàng”.')
    c['img']('12_edit', 'Trang Chỉnh sửa khách hàng')
    step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Thêm mới).')
    step(['Bước 5: Bấm ', ic('btn_luu_kh'), ' để xác nhận thay đổi'])
    sub(['Hoặc ', ic('btn_quaylai_kh'), ' nếu muốn hủy.'])


def diachi(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('THÊM ĐỊA CHỈ GIAO HÀNG')
    step('Bước 1: Mở trang Chỉnh sửa khách hàng (xem PHẦN 3), cuộn xuống khối Địa chỉ giao hàng.')
    step(['Bước 2: Bấm ', ic('btn_themdiachigh')])
    c['img']('13a_edit_delivery', 'Khối Địa chỉ giao hàng trên trang Chỉnh sửa')
    step('Bước 3: Chọn Quốc gia, Tỉnh/Thành phố, Phường/Xã/Thị trấn, Đường/Thôn và nhập Số nhà.')
    sub(['Muốn bỏ một địa chỉ, bấm ', ic('btn_xoa_diachigh'), ' ở góc khung địa chỉ đó.'])
    step(['Bước 4: Bấm ', ic('btn_luu_kh'), ' ở chân trang để lưu địa chỉ.'])


def khoa(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('KHÓA')
    step(['Bước 1: Bấm ', ic('btn_khoa_row'), ' ở cột Hành động.'])
    sub(['Hoặc bấm ', ic('btn_khoa_footer'), ' ở chân trang Chi tiết khách hàng.'])
    step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận khóa”')
    c['img']('14_lock', 'Hộp xác nhận khóa khách hàng')
    step(['Bước 3: Bấm ', ic('btn_confirm_khoa'), ' để xác nhận'])
    sub(['Hoặc bấm ', ic('btn_huy_kh'), ' nếu bấm nhầm'])


def mokhoa(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('MỞ KHÓA')
    step(['Bước 1: Bấm ', ic('btn_mokhoa_row'), ' ở cột Hành động của khách hàng đang Khóa.'])
    sub(['Hoặc bấm ', ic('btn_mokhoa_footer_kh'), ' ở chân trang Chi tiết khách hàng.'])
    step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận mở khóa”')
    c['img']('15_unlock', 'Hộp xác nhận mở khóa khách hàng')
    step(['Bước 3: Bấm ', ic('btn_confirm_mokhoa_kh'), ' để xác nhận'])
    sub(['Hoặc bấm ', ic('btn_huy_kh'), ' nếu bấm nhầm'])


def lichsu(c):
    ic, step, sub, w = c['ic'], c['step'], c['sub'], c['w']
    c['phan']('XEM LỊCH SỬ THAY ĐỔI')
    w.p('Cách 1: Xem từ màn danh sách:')
    step(['Bước 1: Ở cột Hành động, bấm ', ic('btn_bacham_kh'), ' rồi chọn ', ic('item_lichsu')])
    sub(['Hoặc bấm ', ic('btn_lichsu_row'), ' (khách hàng đang Khóa).'])
    step('Bước 2: Hệ thống mở cửa sổ “Lịch sử khách hàng”.')
    c['img']('16_history', 'Cửa sổ Lịch sử khách hàng')
    step(['Bước 3: Bấm ', ic('btn_boloc_lichsu'), ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    sub(['Hoặc bấm ', ic('btn_lammoi_lichsu'), ' để bỏ điều kiện lọc.'])
    step(['Bước 4: Bấm ', ic('btn_dong_lichsu'), ' để đóng cửa sổ.'])
    w.p('Cách 2: Xem từ màn chi tiết:')
    step('Bước 1: Bấm vào Mã KH để mở trang Chi tiết khách hàng.')
    step('Bước 2: Cuộn xuống cuối trang, xem khối Lịch sử.')


def chitiet(c):
    step = c['step']
    c['phan']('XEM CHI TIẾT KHÁCH HÀNG')
    step(c['vao'])
    step('Bước 2: Bấm vào mã ở cột Mã KH. Hệ thống mở trang “Chi tiết khách hàng: <Mã KH>”.')
    c['img']('17_detail', 'Trang Chi tiết khách hàng')


def ql_chung(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('QUẢN LÝ KHÁCH HÀNG — THÔNG TIN CHUNG')
    step(['Bước 1: Ở cột Hành động, bấm ', ic('btn_bacham_kh'), ' rồi chọn ', ic('item_quanly')])
    sub(['Hoặc bấm ', ic('btn_quanly_row'), ' (khách hàng đang Khóa), hoặc ', ic('btn_quanly_footer'),
         ' ở chân trang Chi tiết khách hàng.'])
    step('Bước 2: Hệ thống mở trang “Quản lý khách hàng”, thẻ “Thông tin chung” được chọn sẵn.')
    c['img']('30_mgr_0', 'Thẻ Thông tin chung')
    step('Bước 3: Nhập thông tin cần sửa (quy tắc nhập như Chỉnh sửa).')
    step(['Bước 4: Bấm ', ic('btn_luu_kh'), ' ở chân trang để lưu'])
    sub(['Hoặc ', ic('btn_quaylai_kh'), ' để quay về danh sách.'])


def ql_lienhe(c):
    ic, step = c['ic'], c['step']
    c['phan']('QUẢN LÝ KHÁCH HÀNG — THÔNG TIN LIÊN HỆ')
    step(QL % 'Thông tin liên hệ')
    c['img']('31_mgr_1', 'Thẻ Thông tin liên hệ')
    step('Bước 2: Sửa thông tin của từng người liên hệ: Họ tên, Chức vụ, Số điện thoại (bắt buộc).')
    step(['Bước 3: Bấm ', ic('btn_themnguoilh'), ' để thêm người liên hệ.'])
    step(['Bước 4: Bấm ', ic('btn_luu_kh'), ' ở chân trang để lưu.'])


def ql_tracuu(ten, shot):
    def f(c):
        ic, step, sub = c['ic'], c['step'], c['sub']
        c['phan']('QUẢN LÝ KHÁCH HÀNG — TRA CỨU %s' % ten.upper())
        step(QL % ten)
        c['img'](shot, 'Thẻ ' + ten)
        step('Bước 2: Nhập điều kiện: Từ ngày, Đến ngày, Nhân viên, Phòng ban, Công ty.')
        step(['Bước 3: Bấm ', ic('btn_loc_tab')])
        sub(['Hoặc bấm ', ic('btn_lammoi_tab'), ' để xóa điều kiện lọc.'])
        step(['Bước 4: Bấm ', ic('btn_in_tab'), ' để in, hoặc ', ic('btn_xuatexcel_tab'), ' để xuất Excel.'])
    return f


def ql_thietbi(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('QUẢN LÝ KHÁCH HÀNG — DANH SÁCH TRANG THIẾT BỊ')
    step(QL % 'Danh sách trang thiết bị')
    c['img']('34_mgr_4', 'Thẻ Danh sách trang thiết bị')
    step('Bước 2: Chọn Nhà cung cấp thiết bị, Nhóm hàng hóa hoặc nhập Mã/Tên hàng hóa.')
    step(['Bước 3: Bấm ', ic('btn_loc_tab')])
    sub(['Hoặc bấm ', ic('btn_lammoi_tab'), ' để xóa điều kiện lọc.'])
    step(['Bước 4: Bấm ', ic('btn_in_tab'), ' để in, hoặc ', ic('btn_xuatexcel_tab'), ' để xuất Excel.'])


def popup(title, btn, shot, cap, buoc3):
    def f(c):
        ic, step, sub = c['ic'], c['step'], c['sub']
        c['phan'](title)
        step(TB)
        step(['Bước 2: Bấm ', ic(btn), '.'] if isinstance(btn, str) else ['Bước 2: '] + btn(ic))
        c['img'](shot, cap)
        step('Bước 3: ' + buoc3)
        step(['Bước 4: Bấm ', ic('btn_luulai'), ' để lưu'])
        sub(['Hoặc ', ic('btn_dong_popup'), ' để không lưu thông tin.'])
    return f


def xoa_tb(c):
    ic, step = c['ic'], c['step']
    c['phan']('XÓA THIẾT BỊ')
    step(TB)
    step(['Bước 2: Bấm ', ic('btn_xoa_tb'), ' ở dòng thiết bị cũ / thiết bị NCC khác cần xóa.'])
    step('Bước 3: Trình duyệt hỏi “Bạn chắc chắn muốn xóa thiết bị này?”, bấm OK để xóa hoặc Hủy để thôi.')


def serial_ds(c):
    ic, step = c['ic'], c['step']
    c['phan']('XEM DANH SÁCH SERIAL')
    step(TB)
    step(['Bước 2: Ở cột Serial của thiết bị, bấm ', ic('link_xemserial'), '. Hệ thống mở cửa sổ “Danh sách serial”.'])
    c['img']('45_tb_serial', 'Cửa sổ Danh sách serial')


def serial_them(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('THÊM SERIAL')
    step('Bước 1: Mở cửa sổ Danh sách serial của thiết bị (xem PHẦN 19).')
    step(['Bước 2: Bấm ', ic('btn_themserial'), '. Hệ thống mở cửa sổ “Thêm serial”.'])
    c['img']('46_serial_them', 'Cửa sổ Thêm serial')
    step(['Bước 3: Nhập serial; bấm ', ic('btn_themdong_serial'), ' để thêm ô cho serial tiếp theo.'])
    step(['Bước 4: Bấm ', ic('btn_luulai'), ' để lưu'])
    sub(['Hoặc ', ic('btn_dong_popup'), ' để không lưu thông tin.'])


def serial_sua(c):
    ic, step, sub, w = c['ic'], c['step'], c['sub'], c['w']
    c['phan']('SỬA VÀ THAY ĐỔI SERIAL')
    w.h2('1. Sửa serial')
    step('Bước 1: Mở cửa sổ Danh sách serial của thiết bị (xem PHẦN 19).')
    step(['Bước 2: Bấm ', ic('btn_sua_serial'), ' ở serial cần sửa. Hệ thống mở cửa sổ “Chỉnh sửa serial”.'])
    c['img']('47_serial_sua', 'Cửa sổ Chỉnh sửa serial')
    step('Bước 3: Sửa số serial.')
    step(['Bước 4: Bấm ', ic('btn_luulai'), ' để lưu'])
    sub(['Hoặc ', ic('btn_dong_popup'), ' để không lưu thông tin.'])
    w.h2('2. Thay đổi serial')
    step('Bước 1: Mở cửa sổ Danh sách serial của thiết bị (xem PHẦN 19).')
    step(['Bước 2: Bấm ', ic('btn_thaydoi_serial'), ' ở serial cần thay. Hệ thống mở cửa sổ “Thay đổi serial”.'])
    c['img']('48_serial_thaydoi', 'Cửa sổ Thay đổi serial')
    step('Bước 3: Nhập serial mới.')
    step(['Bước 4: Bấm ', ic('btn_luulai'), ' để lưu'])
    sub(['Hoặc ', ic('btn_dong_popup'), ' để không lưu thông tin.'])


def serial_xoa(c):
    ic, step = c['ic'], c['step']
    c['phan']('XÓA SERIAL')
    step('Bước 1: Mở cửa sổ Danh sách serial của thiết bị (xem PHẦN 19).')
    step(['Bước 2: Bấm ', ic('btn_xoa_serial'), ' ở serial cần xóa.'])
    step('Bước 3: Trình duyệt hỏi “Bạn chắc chắn muốn xóa serial này?”, bấm OK để xóa hoặc Hủy để thôi.')


def ql_khac(c):
    ic, step = c['ic'], c['step']
    c['phan']('QUẢN LÝ KHÁCH HÀNG — THÔNG TIN KHÁC')
    step(QL % 'Thông tin khác')
    c['img']('35_mgr_5', 'Thẻ Thông tin khác')
    step(['Bước 2: Bấm ', ic('btn_taianh'), ', chọn file ảnh để thêm hình ảnh.'])
    step(['Bước 3: Bấm ', ic('btn_themtailieu_kh'), ', chọn file PDF để thêm tài liệu liên quan.'])
    step(['Bước 4: Bấm ', ic('btn_themvideo'), ', nhập Tên video và URL.'])
    step(['Bước 5: Bấm ', ic('btn_luu_tab'), ' của thẻ để lưu.'])


def xuat(c):
    ic, step = c['ic'], c['step']
    c['phan']('XUẤT DANH SÁCH RA FILE')
    step('Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).')
    step(['Bước 2: Bấm ', ic('btn_xuatexcel_kh'), ' hoặc ', ic('btn_xuatcsv'), ' hoặc ', ic('btn_xuatpdf'),
          '. Hệ thống mở cửa sổ chọn trường xuất file.'])
    c['img']('20_export', 'Cửa sổ Chọn trường xuất Excel')
    step('Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.')
    step(['Bước 4: Bấm ', ic('btn_xuatfile')])
    step('Bước 5: Mở file đã xuất.')


G = {
    'dir': HERE,
    'ten': 'Danh mục khách hàng',
    'dt': 'khách hàng',
    'dt_hoa': 'khách hàng',
    'thuat_ngu': [
        ['Khách hàng cá nhân', 'Khách hàng có Loại hình tổ chức là “Cá nhân”.'],
        ['Khách hàng tổ chức', 'Khách hàng thuộc một trong bốn loại: Doanh nghiệp tư nhân, Doanh nghiệp nước ngoài, Tổ chức phi chính phủ, Cơ quan nhà nước.'],
        ['Mã khách hàng', 'Mã do hệ thống TỰ SINH khi lưu, ghép từ biển số xe của Tỉnh/Thành phố + 3 ký tự viết tắt tên Tỉnh/Thành phố + 3 ký tự viết tắt tên Phường/Xã (ví dụ 29TPHPNG). Người dùng không nhập và không sửa được mã.'],
        ['Công ty mẹ', 'Một khách hàng khác được chọn làm đơn vị chủ quản, dùng cho chi nhánh hoặc đơn vị trực thuộc.'],
        ['Người đại diện', 'Người đại diện pháp luật của khách hàng tổ chức.'],
        ['Người liên hệ', 'Đầu mối làm việc thực tế. Một khách hàng tổ chức có thể có nhiều người liên hệ.'],
        ['Trạng thái Hoạt động', 'Khách hàng dùng bình thường, chọn được ở các màn nghiệp vụ khác (báo giá, hợp đồng…).'],
        ['Trạng thái Khóa', 'Khách hàng KHÔNG bị xóa, vẫn nằm trong danh sách, vẫn xem và xuất file được; chỉ không chọn được ở các màn nghiệp vụ khác và không sửa được cho tới khi Mở khóa.'],
    ],
    'phien_ban': [
        ['1.0', '15/08/2026', 'Đội phát triển phần mềm', 'Lập mới cho màn Danh mục khách hàng sau khi gộp dữ liệu khách hàng của hai phần mềm cũ.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Cập nhật theo phiên bản hiện tại: tự sinh mã khách hàng, cột Hành động, cửa sổ Chọn trường xuất file, cửa sổ Import có Validate / Bỏ dòng lỗi.'],
        ['1.3', '28/09/2026', 'Đội phát triển phần mềm', 'Viết theo từng bước kèm ảnh nút: Chỉnh sửa, khối Địa chỉ giao hàng, Khóa / Mở khóa, Lịch sử, Chi tiết và màn Quản lý khách hàng.'],
        ['1.4', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        ['Xem khách hàng', 'Bấm Mã KH để mở màn Chi tiết; mở màn Quản lý khách hàng và các thẻ Báo giá, Hợp đồng, Danh sách trang thiết bị. Thiếu quyền: không có nút Quản lý.'],
        ['Thêm khách hàng', 'Nút Tạo mới và nút Import Excel. Thiếu quyền: hai nút này không hiển thị.'],
        ['Sửa khách hàng', 'Nút Sửa trên cột Hành động và ở màn Chi tiết; tải ảnh / tài liệu ở thẻ Thông tin khác. Thiếu quyền: nút Sửa không hiển thị.'],
        ['Xóa khách hàng', 'Nút Khóa / Mở khóa. Màn hình KHÔNG có chức năng Xóa khách hàng; hai thao tác Khóa / Mở khóa dùng chung quyền này.'],
        ['Xem lịch sử khách hàng', 'Nút Lịch sử trong nút ba chấm của cột Hành động.'],
        ['Xuất dữ liệu khách hàng', 'Ba nút Xuất CSV, Xuất Excel, Xuất PDF. Thiếu quyền: ba nút không hiển thị.'],
        ['Xem tất cả khách hàng', 'Toàn bộ khách hàng của hệ thống.'],
        ['Xem tất cả khách hàng của công ty', 'Khách hàng đã phát sinh báo giá thuộc công ty của mình.'],
        ['Xem tất cả khách hàng của phòng ban', 'Khách hàng đã phát sinh báo giá thuộc phòng ban của mình.'],
        ['Xem tất cả khách hàng của bộ phận', 'Khách hàng đã phát sinh báo giá thuộc bộ phận của mình.'],
        ['Không có quyền nào', 'Chỉ thấy khách hàng có báo giá do chính mình lập, khách hàng do chính mình tạo, cộng khách hàng mình đang đăng ký còn hạn hoặc đã từng có cuộc họp / dự án tiềm năng.'],
    ],
    'thu_tu': ['truycap', 'them', 'sua', 'diachi', 'khoa', 'mokhoa', 'lichsu', 'chitiet',
               'ql_chung', 'ql_lienhe', 'ql_baogia', 'ql_hopdong', 'ql_thietbi',
               'tb_cu', 'tb_ncc', 'tb_sua', 'tb_tang', 'tb_xoa',
               'sr_ds', 'sr_them', 'sr_sua', 'sr_xoa', 'ql_khac', 'xuat', 'import', 'cot'],
    'thay': {
        'truycap': truycap, 'them': them, 'sua': sua, 'diachi': diachi, 'khoa': khoa, 'mokhoa': mokhoa,
        'lichsu': lichsu, 'chitiet': chitiet, 'ql_chung': ql_chung, 'ql_lienhe': ql_lienhe,
        'ql_baogia': ql_tracuu('Báo giá', '32_mgr_2'), 'ql_hopdong': ql_tracuu('Hợp đồng', '33_mgr_3'),
        'ql_thietbi': ql_thietbi,
        'tb_cu': popup('THÊM THIẾT BỊ CŨ', 'btn_themtbcu', '40_tb_themcu', 'Cửa sổ Thêm mới thiết bị cũ',
                       'Nhập/ chọn đầy đủ thông tin bắt buộc: Trang thiết bị, Số lượng, Địa điểm sử dụng.'),
        'tb_ncc': popup('THÊM THIẾT BỊ NCC KHÁC', 'btn_themtbncc', '41_tb_themncc', 'Cửa sổ Thêm mới thiết bị NCC khác',
                        'Nhập/ chọn đầy đủ thông tin bắt buộc: Trang thiết bị, Số lượng, Nhà cung cấp; tích “Hàng công ty không bán” thì chọn thêm Hàng công ty tương đương.'),
        'tb_sua': popup('SỬA THIẾT BỊ', lambda ic: ['Bấm ', ic('btn_sua_tb'), ' ở dòng thiết bị cũ / thiết bị NCC khác cần sửa.'],
                        '43_tb_sua', 'Cửa sổ Cập nhật thiết bị', 'Nhập thông tin cần sửa (quy tắc nhập như lúc thêm).'),
        'tb_tang': popup('TĂNG SỐ LƯỢNG THIẾT BỊ', lambda ic: ['Bấm ', ic('btn_tangsoluong'), ' ở dòng thiết bị cũ / thiết bị NCC khác.'],
                         '42_tb_tangsl', 'Cửa sổ Tăng số lượng', 'Nhập Số lượng thêm.'),
        'tb_xoa': xoa_tb,
        'sr_ds': serial_ds, 'sr_them': serial_them, 'sr_sua': serial_sua, 'sr_xoa': serial_xoa,
        'ql_khac': ql_khac, 'xuat': xuat,
    },
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Danh muc khach hang.docx')))

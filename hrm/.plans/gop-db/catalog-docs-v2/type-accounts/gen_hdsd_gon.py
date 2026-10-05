# -*- coding: utf-8 -*-
"""HDSD Danh mục loại tài khoản — bản GỌN theo skill hdsd-documenter (khuôn HDSD_MAU_GON.docx, 29/09/2026).

Chạy: python3 gen_hdsd_gon.py   → out/HDSD_Danh mục loại tài khoản.docx
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..', '..')
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
sys.path.insert(0, os.path.join(HERE, '..', '..'))

from qg_writer import QgWriter  # noqa: E402
from catalog_v2 import finalize  # noqa: E402
from hdsd_gon import h1_trang_moi, anh_lien_chu_thich  # noqa: E402

TPL = os.path.join(ROOT, '.claude', 'skills', 'hdsd-documenter', 'assets', 'HDSD_MAU_GON.docx')
ROLES = {'pagebreak': 33, 'h1': 34, 'h2': 21, 'p': 28, 'step': 43, 'sub': 49, 'sub2': 126,
         'img': 45, 'cap': 46, 'blank': 23, 'tbl2': 22, 'tbl4': 25}
SHOTS = os.path.join(HERE, 'shots')
UML = os.path.join(HERE, 'uml')
OUT = os.path.join(HERE, 'out', 'HDSD_Danh mục loại tài khoản.docx')


def ic(name):
    for d in (os.path.join(HERE, 'icons'), os.path.join(HERE, '..', 'icons')):
        p = os.path.join(d, name + '.png')
        if os.path.exists(p):
            return ('img', p)
    raise AssertionError('Thiếu icon ' + name)


def sh(name):
    return os.path.join(SHOTS, name + '.png')


w = QgWriter(TPL, ROLES, body_from=19, cover_replace={'Danh mục khu vực': 'Danh mục loại tài khoản'})
step = w.step


def sub(segs):
    w.raw('sub', segs)


def img(name, cap):
    w.image(sh(name), caption=cap)
    anh_lien_chu_thich(w)


# ------------------------------------------------------------------ TỔNG QUAN
h1_trang_moi(w, 'TỔNG QUAN')
w.h2('1. Thuật ngữ sử dụng trong tài liệu')
w.table([
    ['Thuật ngữ', 'Giải thích'],
    ['Loại tài khoản', 'Nhóm phân loại tài khoản kế toán (tài sản, nợ phải trả, vốn chủ sở hữu, doanh thu, chi phí…). Mỗi tài khoản ở Danh mục tài khoản được gán về một loại.'],
    ['Đang được sử dụng', 'Đã có ít nhất một tài khoản ở Danh mục tài khoản được gán loại này.'],
    ['Trạng thái Hoạt động', 'Loại tài khoản chọn được khi khai báo tài khoản.'],
    ['Trạng thái Khóa', 'Loại tài khoản không còn chọn được khi khai báo tài khoản mới nhưng vẫn nằm trong danh mục và vẫn xem được lịch sử.'],
], widths=[2.0, 4.5])
w.h2('2. Cập nhật tài liệu')
w.table([
    ['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung'],
    ['1.0', '13/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Danh mục loại tài khoản.'],
    ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Cập nhật theo phiên bản hiện tại: Khóa/Mở khóa, Lịch sử, Xem chi tiết, Xuất Excel, Import Excel, Tùy chỉnh cột.'],
    ['1.2', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
], widths=[0.9, 1.1, 1.5, 3.0])
w.h2('3. Quyền sử dụng')
w.table([
    ['Quyền', 'Chức năng được dùng'],
    ['Xem danh mục loại tài khoản', 'Truy cập và tìm kiếm, Xem chi tiết, Xem lịch sử thay đổi, Xuất Excel, Tùy chỉnh cột.'],
    ['Quản lý danh mục loại tài khoản', 'Toàn bộ chức năng của quyền Xem, cộng thêm: Thêm mới, Chỉnh sửa, Xóa, Khóa, Mở khóa, Import Excel.'],
], widths=[2.3, 4.2])
w.h2('4. Sơ đồ chức năng tổng quan')
w.image(os.path.join(UML, 'overview.png'), caption='Sơ đồ chức năng tổng quan màn Danh mục loại tài khoản')
anh_lien_chu_thich(w)

# ------------------------------------------------------------------ PHẦN 1
h1_trang_moi(w, 'PHẦN 1: TRUY CẬP VÀ TÌM KIẾM')
step(['Bước 1: Từ phân hệ Tài chính ', ic('menu_phanhe'), ', tại menu Danh mục ', ic('menu_nhom'),
      ', chọn Danh mục loại tài khoản ', ic('menu_muc')])
img('01_list', 'Màn hình Danh mục loại tài khoản')
step(['Bước 2: Nhập mã hoặc tên loại tài khoản vào ô tìm kiếm nhanh ', ic('o_timnhanh')])
step(['Bước 3: Nhấn ', ic('btn_timkiem')])
step(['Bước 4: Bấm ', ic('btn_timkiemnangcao'), ', chọn giá trị trong ', ic('o_trangthai'), ' để lọc theo trạng thái'])
sub(['Hoặc chọn Người tạo, Người cập nhật, Ngày cập nhật để lọc theo từng tiêu chí'])
step(['Bước 5: Chọn ', ic('btn_lammoi'), ' để xóa giá trị đã lọc'])

# ------------------------------------------------------------------ PHẦN 2
h1_trang_moi(w, 'PHẦN 2: THÊM MỚI LOẠI TÀI KHOẢN')
step('Bước 1: Truy cập vào màn hình Danh mục loại tài khoản.')
step(['Bước 2: Bấm ', ic('btn_taomoi')])
img('10_create', 'Cửa sổ Tạo loại tài khoản')
step('Bước 3: Nhập/ chọn đầy đủ thông tin bắt buộc: Mã loại tài khoản, Tên loại tài khoản.')
step(['Bước 4: Bấm ', ic('btn_luu'), ' để lưu và đóng cửa sổ,'])
sub(['Hoặc ', ic('btn_luutieptuc'), ' để lưu rồi nhập tiếp loại tài khoản khác.'])
sub(['Hoặc ', ic('btn_dong'), ' để không lưu thông tin.'])

# ------------------------------------------------------------------ PHẦN 3
h1_trang_moi(w, 'PHẦN 3: CHỈNH SỬA')
step('Bước 1: Truy cập vào màn hình Danh mục loại tài khoản.')
step(['Bước 2: Bấm nút ', ic('btn_sua'), ' ở cột Hành động.'])
step('Bước 3: Hệ thống hiển thị cửa sổ “Sửa loại tài khoản”.')
img('12_edit', 'Cửa sổ Sửa loại tài khoản')
step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Thêm mới).')
step(['Bước 5: Bấm ', ic('btn_luu'), ' để xác nhận thay đổi'])
sub(['Hoặc ', ic('btn_dong'), ' nếu muốn hủy.'])

# ------------------------------------------------------------------ PHẦN 4
h1_trang_moi(w, 'PHẦN 4: XÓA')
step(['Bước 1: Bấm ', ic('btn_xoa'), ' ở cột Hành động'])
step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận xóa”')
img('13_delete', 'Hộp xác nhận xóa loại tài khoản')
step(['Bước 3: Bấm ', ic('btn_confirm_xoa'), ' để xác nhận xóa'])
sub(['Hoặc bấm ', ic('btn_huy_confirm'), ' nếu bấm nhầm'])

# ------------------------------------------------------------------ PHẦN 5
h1_trang_moi(w, 'PHẦN 5: KHÓA')
step(['Bước 1: Bấm ', ic('btn_bacham_row'), ' ở cột Hành động, chọn ', ic('item_khoa')])
step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận khóa”')
img('14_lock', 'Hộp xác nhận khóa loại tài khoản')
step(['Bước 3: Bấm ', ic('btn_confirm_khoa'), ' để xác nhận'])
sub(['Hoặc bấm ', ic('btn_huy_confirm'), ' nếu bấm nhầm'])

# ------------------------------------------------------------------ PHẦN 6
h1_trang_moi(w, 'PHẦN 6: MỞ KHÓA')
step(['Bước 1: Bấm ', ic('btn_mokhoa_row'), ' ở cột Hành động của loại tài khoản đang Khóa.'])
step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận mở khóa”')
img('15_unlock', 'Hộp xác nhận mở khóa loại tài khoản')
step(['Bước 3: Bấm ', ic('btn_confirm_mokhoa'), ' để xác nhận'])
sub(['Hoặc bấm ', ic('btn_huy_confirm'), ' nếu bấm nhầm'])

# ------------------------------------------------------------------ PHẦN 7
h1_trang_moi(w, 'PHẦN 7: XEM LỊCH SỬ THAY ĐỔI')
w.p('Cách 1: Xem từ màn danh sách:')
step(['Ở cột Hành động, bấm ', ic('btn_bacham_row'), ' rồi chọn ', ic('item_lichsu')])
sub(['Hoặc bấm ', ic('btn_lichsu_row'), ' (loại tài khoản đang Khóa)'])
w.p('Cách 2: Xem từ màn chi tiết:')
step('Bước 1: Bấm vào mã loại tài khoản để mở cửa sổ xem chi tiết')
step(['Bước 2: Chọn nút ', ic('btn_xemlichsu')])
img('16_history', 'Cửa sổ Lịch sử thay đổi')

# ------------------------------------------------------------------ PHẦN 8
h1_trang_moi(w, 'PHẦN 8: XEM CHI TIẾT LOẠI TÀI KHOẢN')
step('Bước 1: Truy cập vào màn hình Danh mục loại tài khoản.')
step('Bước 2: Bấm vào mã ở cột Mã loại tài khoản. Hệ thống mở cửa sổ “Xem loại tài khoản”.')
img('17_detail', 'Xem chi tiết loại tài khoản ở chế độ chỉ đọc')

# ------------------------------------------------------------------ PHẦN 9
h1_trang_moi(w, 'PHẦN 9: XUẤT DANH SÁCH RA EXCEL')
step('Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).')
step(['Bước 2: Bấm nút ', ic('btn_xuatexcel'), '. Hệ thống mở cửa sổ “Chọn trường xuất file”.'])
img('20_export', 'Cửa sổ Chọn trường xuất file')
step('Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.')
step(['Bước 4: Bấm ', ic('btn_xuatfile')])
step('Bước 5: Mở file Excel đã xuất.')

# ------------------------------------------------------------------ PHẦN 10
h1_trang_moi(w, 'PHẦN 10: IMPORT LOẠI TÀI KHOẢN TỪ FILE EXCEL')
step(['Bước 1: Tại màn hình danh sách, bấm ', ic('btn_import'), '. Hệ thống mở cửa sổ “Import loại tài khoản”.'])
img('21_import_open', 'Cửa sổ Import loại tài khoản khi vừa mở')
step(['Bước 2: Bấm ', ic('btn_taifilemau'), ' để lấy file mẫu'])
step('Bước 3: Điền dữ liệu vào file mẫu.')
step(['Bước 4: Bấm ', ic('btn_chonfile'), ', chọn file vừa điền'])
step(['Bước 5: Bấm ', ic('btn_load')])
img('22_import_loaded', 'Dữ liệu đã được load lên bảng xem trước')
step(['Bước 6: Bấm ', ic('btn_validate'), ' để hệ thống kiểm tra từng dòng.'])
img('23_import_validated', 'Kết quả kiểm tra — mỗi dòng lỗi nêu rõ lý do')
step('Bước 7:')
w.raw('sub2', 'Sửa trực tiếp các dòng lỗi trên bảng rồi bấm Validate lại.')
w.raw('sub2', ['Nếu không muốn nhập các dòng lỗi thì bấm ', ic('btn_bodongloi')])
w.raw('sub2', ['Muốn sửa lại những dòng đã khoá, bấm ', ic('btn_xoavalidate')])
step(['Bước 8: Bấm ', ic('btn_import_modal')])

# ------------------------------------------------------------------ PHẦN 11
h1_trang_moi(w, 'PHẦN 11: TÙY CHỈNH CỘT HIỂN THỊ')
step(['Bước 1: Ở màn danh sách, bấm biểu tượng ', ic('btn_cauhinhcot')])
img('25_colcfg', 'Cửa sổ Tùy chỉnh cột')
step('Bước 2: Tích để hiện cột, bỏ tích để ẩn cột.')
step('Bước 3: Kéo biểu tượng ba gạch ở cuối mỗi dòng để đổi thứ tự cột.')
step(['Bước 4: Bấm ', ic('btn_luu'), ' để áp dụng'])
sub(['Hoặc bấm ', ic('btn_dong'), ' nếu muốn bỏ thay đổi.'])

w.rebuild_toc(levels=(1, 2))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
w.save(OUT)
finalize(OUT)
print('OK', OUT)

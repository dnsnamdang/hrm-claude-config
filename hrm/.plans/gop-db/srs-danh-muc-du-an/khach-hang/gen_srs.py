# -*- coding: utf-8 -*-
"""Sinh "SRS - Danh mục khách hàng.docx" theo code nhánh gop_db — form 2026-09-24.

Chạy:  python3 .plans/gop-db/srs-danh-muc-du-an/khach-hang/gen_srs.py
Ảnh chụp thật (Playwright Python 1440x900, bản gop_db cổng 3002): khach-hang_shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db, 24/09/2026):
  FE  pages/assign/customers/{index.vue, add.vue, _id/index.vue, _id/edit.vue, _id/manager/index.vue}
      components/assign-components/customer/CustomerForm.vue + manager/*Tab.vue
      components/assign/customer/CustomerHistoryModal.vue · middleware/checkCustomerPermission.js
      components/subsystem-menu/master-data.js (menu) · components/subsystems.js (phân hệ)
  BE  Modules/Assign/Routes/api.php (nhóm /assign/customers)
      Http/Controllers/Api/V1/CustomerController.php · Services/CustomerService.php
      Services/CustomerImportService.php · Entities/CustomerHistory.php
      Http/Requests/Customer/{SaveCustomerRequest,UpdateCustomerRequest}.php
      app/Helpers/CustomerPermissionHelper.php · app/Http/Middleware/{CheckCustomerNotLocked,CheckImportRowLimit}.php
      app/Helper/PermissionHelper.php::checkPermissionList (phạm vi dữ liệu)
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (nhóm 'Quản lý khách hàng', id 1517-1525, 167)
Tài liệu cũ (form 2026-08-17, chỉ tham khảo nghiệp vụ): .plans/gop-db/customer-docs/gen_srs.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))

import srs_docx_lib  # noqa: E402
from srs_docx_lib import SrsDoc  # noqa: E402

# Mỗi đoạn "Quy tắc chung" là 1 hyperlink RIÊNG (1 relationship / đoạn). `relate_to()` của
# python-docx gộp các link trùng URL làm 1 relationship; bình thường Word tách lại khi cập nhật
# mục lục, nhưng generator này lưu với update_fields=False nên phải tự tách để selfcheck đếm đúng.
def _add_hyperlink_unique(paragraph, url, text):
    part = paragraph.part
    r_id = part.rels._next_rId
    part.rels.add_relationship(srs_docx_lib.RT.HYPERLINK, url, r_id, is_external=True)
    part.relate_to = lambda *a, **k: r_id
    try:
        return _orig_add_hyperlink(paragraph, url, text)
    finally:
        del part.relate_to


_orig_add_hyperlink = srs_docx_lib.add_hyperlink
srs_docx_lib.add_hyperlink = _add_hyperlink_unique

OUT = os.path.join(HERE, 'SRS - Danh mục khách hàng.docx')
SHOTS = os.path.join(HERE, 'khach-hang_shots')
MENU = 'Phân hệ Danh mục => Đối tác => Khách hàng'

A_QL = 'Người quản lý khách hàng (Q1–Q6)'
A_ND = 'Người dùng đã đăng nhập'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')
LOCKED_MSG = '“Khách hàng đang bị khoá, vui lòng mở khoá trước khi cập nhật.”'


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/customers',
           full_url='https://<host-hrm>/assign/customers', img_prefix='khachhang_gopdb_')

# Icon cho từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện.
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ Danh mục': 'phanhe', 'Đối tác': 'doitac', 'Khách hàng': 'khachhang',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidatboloc', 'Tuỳ chỉnh cột': 'tuychinhcot',
    'Tạo mới': 'taomoi', 'Sửa': 'sua', 'Xem chi tiết': 'xem', 'Hành động khác': 'khac',
    'Khóa': 'khoa', 'Mở khóa': 'mokhoa', 'Lịch sử': 'lichsu', 'Quản lý': 'quanly',
    'Import Excel': 'import', 'Xuất CSV': 'xuatcsv', 'Xuất Excel': 'xuat', 'Xuất PDF': 'xuatpdf',
}.items()})

d.title_block('Danh mục khách hàng')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục khách hàng thuộc phân hệ Danh mục '
    'dùng chung, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ phạm vi dữ liệu nhiều cấp (toàn hệ thống / công ty / phòng ban / bộ phận / của chính '
    'mình) và lớp bảo vệ riêng cho khách hàng cá nhân.',
    'Làm rõ các trường bắt buộc rẽ nhánh theo Loại hình tổ chức, đặc biệt quy tắc Mã số thuế chỉ '
    'bắt buộc khi khách hàng tổ chức không có Công ty mẹ.',
    'Làm rõ điều kiện hiện các thao tác Sửa, Khóa / Mở khóa, Quản lý, Lịch sử trên từng dòng và '
    'quy tắc khách hàng đã khóa không được cập nhật.',
    'Làm rõ quy tắc nhập hàng loạt từ Excel và xuất danh sách ra CSV / Excel / PDF.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Khách hàng cá nhân', 'Khách hàng có Loại hình tổ chức là “Cá nhân”. Chịu thêm lớp bảo vệ '
     'hiển thị riêng (BR-02).'),
    ('Khách hàng tổ chức', 'Khách hàng thuộc một trong 4 loại: Doanh nghiệp tư nhân, Doanh nghiệp '
     'nước ngoài, Tổ chức phi chính phủ, Cơ quan nhà nước.'),
    ('Khách hàng tự do', 'Khách hàng cá nhân chưa ai đăng ký còn hạn, chưa phát sinh báo giá / '
     'cuộc họp / dự án tiềm năng và không do người đang đăng nhập tạo.'),
    ('Mã khách hàng', 'Mã do hệ thống tự sinh khi lưu, ghép từ biển số tỉnh + ký hiệu tỉnh + ký '
     'hiệu phường/xã, trùng thì thêm hậu tố “-01”, “-02”… (vd 29TPHPBA-212). Không sửa được.'),
    ('Công ty mẹ', 'Khách hàng khác được chọn làm đơn vị chủ quản của khách hàng tổ chức.'),
    ('Loại hình hoạt động – Lĩnh vực kinh doanh', 'Cặp phân loại ngành nghề của khách hàng; lĩnh '
     'vực phải thuộc đúng loại hình đã chọn. Một khách hàng khai được nhiều cặp.'),
    ('Người đại diện', 'Người đại diện pháp luật của khách hàng tổ chức (tên + chức vụ).'),
    ('Người liên hệ', 'Đầu mối làm việc của khách hàng tổ chức; có họ tên, chức vụ, số điện thoại, '
     'tài khoản cá nhân.'),
    ('Khóa khách hàng', 'Đổi trạng thái sang “Khóa”. KHÔNG xóa dữ liệu; khách hàng vẫn nằm trong '
     'danh sách nhưng không cập nhật được cho tới khi Mở khóa.'),
    ('Phạm vi dữ liệu', 'Tập khách hàng người đăng nhập được nhìn thấy, do các quyền V1–V4 quyết '
     'định (BR-01).'),
    ('Màn Quản lý khách hàng', 'Màn nhiều thẻ tổng hợp thông tin nghiệp vụ của một khách hàng: '
     'Thông tin chung, Thông tin liên hệ, Báo giá, Hợp đồng, Danh sách trang thiết bị, Thông tin khác.'),
    ('Menu “…” (Hành động khác)', 'Nút ở cột Hành động chứa các thao tác còn lại của dòng khi dòng '
     'có nhiều hơn 3 thao tác.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác (nhóm “Quản lý khách hàng” của phân hệ Danh mục dùng chung):')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Xem khách hàng', 'Mã khách hàng là liên kết mở màn Chi tiết; hiện thao tác Quản lý; '
     'xem các thẻ Báo giá, Hợp đồng, Danh sách trang thiết bị ở màn Quản lý.'),
    ('Q2', 'Thêm khách hàng', 'Hiện nút Tạo mới và Import Excel.'),
    ('Q3', 'Sửa khách hàng', 'Hiện thao tác Sửa (ở danh sách và màn Chi tiết) với khách hàng đang '
     'Hoạt động; sửa / xóa thiết bị, serial, tải ảnh – tài liệu ở màn Quản lý.'),
    ('Q4', 'Xóa khách hàng', 'Hiện thao tác Khóa / Mở khóa. Hệ thống không có thao tác xóa hẳn '
     'khách hàng.'),
    ('Q5', 'Xem lịch sử khách hàng', 'Hiện thao tác Lịch sử trên dòng của màn danh sách.'),
    ('Q6', 'Xuất dữ liệu khách hàng', 'Hiện 3 nút Xuất CSV, Xuất Excel, Xuất PDF.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (xét từ trên xuống, có cấp nào thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem tất cả khách hàng', 'Toàn bộ khách hàng của hệ thống.'),
    ('V2', 'Xem tất cả khách hàng của công ty', 'Khách hàng thuộc công ty đang chọn của người '
     'đăng nhập.'),
    ('V3', 'Xem tất cả khách hàng của phòng ban', 'Khách hàng thuộc phòng ban / bộ phận người đăng '
     'nhập quản lý, cộng khách hàng do chính mình tạo.'),
    ('V4', 'Xem tất cả khách hàng của bộ phận', 'Khách hàng thuộc bộ phận người đăng nhập quản lý, '
     'cộng khách hàng do chính mình tạo.'),
    ('—', '(không có cấp nào)', 'Chỉ khách hàng do chính mình tạo.'),
], widths=[0.8, 2.0, 3.2])
d.p('Ngoài cấp đang áp, người dùng LUÔN thấy thêm khách hàng do chính mình tạo và khách hàng mình '
    'đang đăng ký còn hạn / đã từng có cuộc họp, dự án tiềm năng. Khách hàng cá nhân còn chịu thêm '
    'lớp bảo vệ ở BR-02. Màn danh sách KHÔNG gắn quyền xem: mọi người dùng đã đăng nhập đều vào được, '
    'khác nhau ở lượng dữ liệu nhìn thấy. Mục menu Khách hàng hiển thị với mọi người dùng.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách khách hàng', '✅', '✅', '✅', '✅', '✅', '✅', '✅ (theo phạm vi)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tạo mới khách hàng', '❌', '✅', '❌', '❌', '❌', '❌', '❌'),
    ('FR-05 Chỉnh sửa khách hàng', '❌', '❌', '✅ (kèm Q1)', '❌', '❌', '❌', '❌'),
    ('FR-06 Xem chi tiết khách hàng', '✅', '❌', '❌', '❌', '❌', '❌', '❌'),
    ('FR-07 Khóa / Mở khóa khách hàng', '❌', '❌', '❌', '✅', '❌', '❌', '❌'),
    ('FR-08 Xem lịch sử thay đổi', '❌', '❌', '❌', '❌', '✅', '❌', '❌'),
    ('FR-09 Quản lý khách hàng', '✅', '❌', '❌', '❌', '❌', '❌', '❌'),
    ('FR-10 Import Excel', '❌', '✅', '❌', '❌', '❌', '❌', '❌'),
    ('FR-11 Xuất CSV / Excel / PDF', '❌', '❌', '❌', '❌', '❌', '✅', '❌'),
], widths=[2.2, 0.45, 0.45, 0.75, 0.45, 0.45, 0.45, 0.8])
d.p('Ghi chú: màn Chỉnh sửa đọc dữ liệu khách hàng qua cùng đường với màn Chi tiết nên người chỉ có '
    'Q3 mà thiếu Q1 thấy nút Sửa nhưng không nạp được form (xem ghi chú BR-12).')

# ================================================================ PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_QL, [0, 1, 2, 3, 4, 5, 6]),
     (A_ND, [0])],
    [('FR-01', 'Xem danh sách khách hàng', 'view'),
     ('FR-04', 'Tạo mới khách hàng', 'crud'),
     ('FR-05', 'Chỉnh sửa khách hàng', 'crud'),
     ('FR-07', 'Khóa / Mở khóa khách hàng', 'action'),
     ('FR-09', 'Quản lý khách hàng', 'action'),
     ('FR-10', 'Import Excel khách hàng', 'io'),
     ('FR-11', 'Xuất CSV / Excel / PDF', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết khách hàng', 'view', 'extend', [0], None),
     ('FR-08', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Danh mục khách hàng')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách khách hàng')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Danh mục khách hàng tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách khách hàng',
    mota='Hiển thị các khách hàng nằm trong phạm vi dữ liệu của người đăng nhập, kèm người tạo, '
         'ngày tạo, trạng thái và các thao tác trên từng dòng.',
    tacnhan='Người quản lý khách hàng; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập. Không cần quyền riêng để mở màn hình.',
    chinh='1. Người dùng vào menu Phân hệ Danh mục → Đối tác → Khách hàng.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo quyền V1–V4 và áp lớp bảo vệ khách hàng cá nhân.\n'
          '3. Hệ thống nạp trang 1, 10 dòng/trang, khách hàng mới tạo lên đầu.\n'
          '4. Bảng hiển thị các cột mặc định (STT, Mã KH, Tên khách hàng, Người tạo, Ngày tạo, Trạng '
          'thái, Hành động), dòng “Hiển thị a–b / N” và thanh phân trang.',
    phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Không có cấp xem nào → chỉ thấy khách hàng do chính mình tạo (và khách hàng mình đăng ký '
        '/ tương tác).\n'
        '• Có Q1: bấm Mã KH → mở màn Chi tiết (FR-06); không có Q1 thì Mã KH là chữ thường.\n'
        '• Bấm tiêu đề cột Mã KH, Tên khách hàng, Ngày tạo, Ngày cập nhật → sắp xếp, bấm lại để đảo '
        'chiều.\n'
        '• Rời màn (sang Chi tiết / Sửa / Quản lý) rồi quay lại trong vòng 10 phút → bộ lọc được '
        'khôi phục.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách khách hàng lúc mới truy cập')
d.figure(shot('07-menu-khac.png'), 'Cột Trạng thái, cột Hành động và menu “…” của một dòng',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Danh mục khách hàng”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu Q2', 'Mở màn Tạo mới (FR-04).'),
    ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu Q2', 'Mở cửa sổ Import (FR-10).'),
    ('Nút Xuất CSV / Xuất Excel / Xuất PDF', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu Q6',
     'Mở cửa sổ Chọn trường xuất (FR-11). Khóa trong lúc đang xuất.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '≥ 1', 'Số thứ tự liên tục',
     'Ghim trái khi cuộn ngang; không tắt được.'),
    ('Cột Mã KH', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Ghim trái, không tắt được, sắp xếp được. Có Q1 thì là liên kết mở màn Chi tiết.'),
    ('Cột Tên khách hàng', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Sắp xếp được.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
     'Chỉ tên người tạo. Ngày tạo sắp xếp được.'),
    ('Các cột mặc định ẩn: Tên viết tắt, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP, Tên đơn '
     'vị, Địa chỉ xuất hóa đơn, Công ty mẹ, Hãng xe, Cấp đại lý, Người cập nhật, Ngày cập nhật',
     'Table/Grid', 'Read-only', '–', 'Ẩn',
     'Bật ở cửa sổ Tuỳ chỉnh cột. Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu',
     'Hoạt động màu xanh, Khóa màu đỏ.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu',
     'Không tắt được. Thứ tự Sửa, Khóa / Mở khóa, Quản lý, Lịch sử; dòng có hơn 3 thao tác thì '
     'phần sau thao tác thứ 2 gom vào nút “…”. Thao tác không dùng được thì ẨN hẳn.'),
    ('Nút Sửa (bút)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q3 và khách hàng đang Hoạt động (FR-05).'),
    ('Nút Khóa / Mở khóa (ổ khóa)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q4. Đang Hoạt động: Khóa; đang Khóa: Mở khóa (FR-07).'),
    ('Mục Quản lý', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu Q1', 'Mở màn Quản lý (FR-09).'),
    ('Mục Lịch sử', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu Q5', 'Mở cửa sổ Lịch sử (FR-08).'),
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng khách hàng khớp bộ lọc trong phạm vi dữ liệu.'),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5 / 10 / 20 / 50', '10', 'Đổi thì quay về trang 1.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Về đầu / lùi / số trang / tiến / về cuối.'),
    ('Thanh cuộn ngang', 'Table/Grid', 'Enable', '–', 'Hiển thị khi bảng tràn',
     'Có ở cả phía trên và phía dưới bảng.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Hiển thị ngay khi vào màn', 'Tắt khi nạp xong.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Không kiểm quyền mở màn; xác định cấp xem V1–V4 của người dùng.\n'
     'During:\n– Khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu có).\n'
     '– Áp phạm vi dữ liệu và lớp bảo vệ khách hàng cá nhân.\n'
     '– Nạp cấu hình cột đã lưu của người dùng.\n'
     'After:\n– Hiển thị trang 1, 10 dòng, khách hàng mới tạo lên đầu.'),
    ('Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click',
     'After:\n– Sắp xếp theo cột đó, bấm lại để đảo chiều; quay về trang 1.'),
    ('Bấm số trang / đổi Số dòng/trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu; đổi số dòng/trang thì quay về trang 1.'),
    ('Bấm Mã KH', 'Click', 'Before:\n– Chỉ là liên kết khi có Q1.\n'
     'After:\n– Mở màn Chi tiết khách hàng (FR-06).'),
    ('Bấm nút “…” ở cột Hành động', 'Click',
     'After:\n– Mở menu các thao tác còn lại của dòng (Quản lý, Lịch sử).'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Danh mục '
           'khách hàng tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc khách hàng',
    mota='Tìm nhanh theo mã, tên khách hàng, mã số thuế, số điện thoại hoặc tên người tạo; lọc nâng '
         'cao theo tối đa 15 nhóm tiêu chí, kết hợp theo kiểu “và”, trong phạm vi dữ liệu của người dùng.',
    tacnhan='Người quản lý khách hàng; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách khách hàng.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc (danh sách lựa chọn chỉ nạp ở lần mở đầu).\n'
          '3. Ô chọn (Công ty, Phòng ban, Bộ phận, Nhân viên, Quốc gia, Tỉnh/Thành phố, Loại hình tổ '
          'chức, Trạng thái, Loại hình – Lĩnh vực, Người cập nhật, Khách hàng hãng, Hãng xe, Cấp đại '
          'lý): chọn xong hệ thống tự lọc lại ngay.\n'
          '4. Ô gõ tay (Mã khách hàng, MST/SĐT, Tên khách hàng, Số CCCD, Tên đơn vị): chỉ lọc khi bấm '
          'Enter hoặc nút Tìm kiếm.\n'
          '5. Bảng hiển thị kết quả từ trang 1.',
    phu='• Bấm Làm mới → xóa hết điều kiện lọc và nạp lại danh sách ban đầu.\n'
        '• Bấm “Ẩn tìm kiếm nâng cao” → thu gọn khối lọc, điều kiện đang chọn vẫn giữ.\n'
        '• Gõ ĐÚNG TRỌN một số điện thoại → hiện được cả khách hàng cá nhân tự do (BR-02).\n'
        '• Không có kết quả → “Không có dữ liệu phù hợp bộ lọc.”',
    dacbiet=None)
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-bo-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao đang mở (đủ 15 nhóm tiêu chí)')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Placeholder “Tìm theo mã KH, tên KH, MST, SĐT, người tạo...”. Tìm gần đúng theo Mã, Tên, Mã '
     'số thuế, Số điện thoại, tên Người tạo.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc và nạp lại.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc (nhãn đổi thành “Ẩn tìm kiếm nâng cao” khi đang mở).'),
    ('Công ty / Phòng ban / Bộ phận / Nhân viên', 'Dropdown', 'Enable / Disable', 'Theo cây tổ chức',
     'Không', 'Trống', 'Lọc theo đơn vị của báo giá gắn khách hàng. Cấp vượt quá quyền xem bị khóa '
     '(biểu tượng ổ khóa).'),
    ('Quốc gia', 'Dropdown', 'Enable', 'Danh sách quốc gia', 'Không', 'Trống', '–'),
    ('Tỉnh/Thành phố', 'Dropdown', 'Enable', 'Danh sách tỉnh/thành', 'Không', 'Trống', '–'),
    ('Mã khách hàng', 'Textbox', 'Enable', '–', 'Không', 'Trống', 'Lọc gần đúng theo mã.'),
    ('MST/SĐT', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Tìm trên cả mã số thuế và từng số điện thoại.'),
    ('Tên khách hàng', 'Textbox', 'Enable', '–', 'Không', 'Trống', 'Lọc gần đúng theo tên.'),
    ('Số CCCD', 'Textbox', 'Enable', '–', 'Không', 'Trống', '–'),
    ('Tên đơn vị', 'Textbox', 'Enable', '–', 'Không', 'Trống', '–'),
    ('Loại hình tổ chức', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống',
     'Cá nhân / Doanh nghiệp tư nhân / Doanh nghiệp nước ngoài / Tổ chức phi chính phủ / Cơ quan '
     'nhà nước.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Trống',
     'Bỏ trống thì hiện cả hai.'),
    ('Loại hình hoạt động khách hàng – Lĩnh vực kinh doanh khách hàng', 'Dropdown', 'Enable',
     'Chọn nhiều, theo cặp', 'Không', 'Trống',
     'Chọn loại hình rồi tích lĩnh vực con; loại hình không tích lĩnh vực nào thì lọc theo cả loại hình.'),
    ('Người cập nhật', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', '–'),
    ('Khách hàng hãng', 'Dropdown', 'Enable', 'Có / Không', 'Không', 'Trống', '–'),
    ('Hãng xe', 'Dropdown', 'Enable', 'Danh sách hãng xe', 'Không', 'Trống', '–'),
    ('Cấp đại lý', 'Dropdown', 'Enable', 'Cấp 1 / Cấp 2 / Cấp 3', 'Không', 'Trống', '–'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm / Enter', 'Click / Keypress',
     'Before:\n– Thu thập giá trị mọi điều kiện đang có.\n'
     'During:\n– Áp đồng thời các điều kiện theo kiểu “và”, trong phạm vi dữ liệu.\n'
     'After:\n– Nạp lại bảng từ trang 1; cập nhật “Hiển thị a–b / N”.'),
    ('Đổi giá trị một ô chọn trong khối lọc', 'Change',
     'After:\n– Tự lọc lại ngay theo toàn bộ điều kiện đang chọn.'),
    ('Gõ vào ô tìm nhanh / ô gõ tay trong khối lọc', 'Keypress',
     'After:\n– Chưa lọc; chờ Enter hoặc nút Tìm kiếm.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xóa mọi điều kiện, sắp xếp mặc định, nạp lại trang 1.'),
])

# ---------------------------------------------------------------- 2.3
d.h3('2.3 Cài đặt bộ lọc và tuỳ chỉnh cột')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Cài đặt bộ lọc và tuỳ chỉnh cột hiển thị',
    mota='Mỗi người dùng tự chọn nhóm tiêu chí nào hiện trong khối Tìm kiếm nâng cao, cột nào hiện '
         'trên bảng và sắp xếp thứ tự bằng kéo thả. Cấu hình lưu riêng theo từng người, từng màn.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách khách hàng.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ với danh sách 15 nhóm tiêu chí / 22 cột, đánh dấu những mục đang hiện.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ (hoặc ≡) để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình, thông báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc / bảng.',
    phu='• Bấm “Khôi phục mặc định” (Cài đặt bộ lọc) → trả về bộ tiêu chí mặc định của màn.\n'
        '• Bỏ tích một tiêu chí đang có giá trị → giá trị lọc đó bị xóa luôn, không lọc ngầm.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Cột STT, Mã KH và Hành động luôn hiện, không bỏ tích được (hiển thị xám + ổ khóa).\n'
        '• Còn tổng cộng ≤ 3 ô lọc thì khối lọc tự bày thành 1 hàng ngang, không cần nút Tìm kiếm '
        'nâng cao.',
    dacbiet='Mặc định bảng chỉ hiện 7 cột (STT, Mã KH, Tên khách hàng, Người tạo, Ngày tạo, Trạng '
            'thái, Hành động); khối lọc mặc định hiện đủ 15 nhóm tiêu chí.')
d.p('2.3.2 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột', modal='Cài đặt bộ lọc và Tuỳ chỉnh cột',
         shot=shot('02b-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('02c-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột — cột khóa hiển thị xám', width_in=6.2)
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách tiêu chí lọc', 'Table/Grid', 'Enable', '15 mục', 'Không', 'Theo cấu hình đã lưu',
     'Mỗi mục: số thứ tự, biểu tượng kéo ⠿, ô tích, tên tiêu chí.'),
    ('Nút Lưu (Cài đặt bộ lọc)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình tiêu chí lọc.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về bộ tiêu chí mặc định.'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '22 cột', 'Không', 'Theo cấu hình đã lưu',
     'STT, Mã KH, Hành động bị khóa (luôn hiện).'),
    ('Nút Lưu (Tuỳ chỉnh cột)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình cột.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
])
d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Kéo biểu tượng ⠿ / ≡', 'Drag', 'After:\n– Đổi thứ tự tiêu chí / cột trong danh sách.'),
    ('Bấm Lưu', 'Click',
     'During:\n– Tiêu chí bị bỏ tích mà đang có giá trị → xóa giá trị lọc đó.\n'
     'After:\n– Lưu cấu hình theo người dùng đang đăng nhập; thông báo “Cập nhật thành công”; đóng '
     'cửa sổ; vẽ lại khối lọc / bảng (bật cột Công ty mẹ, Hãng xe, Người cập nhật thì nạp lại dữ liệu '
     'kèm các cột đó).'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Đưa danh sách về cấu hình mặc định của màn.'),
])

# ---------------------------------------------------------------- 2.4
SAVE_DURING = (
    '– Tên khách hàng trống → “Bắt buộc phải nhập” (báo ngay tại ô, không gửi đi); quá 255 ký tự → '
    '“Vui lòng nhập tối đa 255 ký tự.”\n'
    '– Loại hình tổ chức trống → “Bắt buộc nhập”.\n'
    '– Thiếu Quốc gia / Tỉnh/Thành phố / Phường/Xã → “Bắt buộc chọn quốc gia” / “Bắt buộc chọn '
    'tỉnh/thành phố” / “Bắt buộc chọn phường/xã”.\n'
    '– Email sai định dạng → “Định dạng email không hợp lệ”; đã có ở khách hàng khác → “Email đã tồn tại”.\n'
    '– Tích “Là khách hãng” mà chưa chọn Hãng xe → “Bắt buộc khi là khách hãng”.\n'
    '– Lĩnh vực không thuộc loại hình đã chọn → “Lĩnh vực không thuộc loại hình đã chọn, vui lòng '
    'chọn lại”.\n'
    '– Cá nhân: không có số điện thoại → “Bắt buộc phải nhập số điện thoại”; số sai định dạng → “Số '
    'điện thoại không đúng định dạng”; Số CCCD trùng → “Số CMND/CCCD đã tồn tại”; Ngày cấp / Sinh '
    'nhật sau hôm nay → “Không được lớn hơn ngày hiện tại”.\n'
    '– Tổ chức: thiếu Địa chỉ xuất hóa đơn → “Bắt buộc nhập”; chưa có người đại diện → “Phải có ít '
    'nhất 1 người đại diện”, thiếu tên / chức vụ người đại diện → “Bắt buộc phải nhập”; chưa có người '
    'liên hệ → “Phải có ít nhất 1 liên hệ”, thiếu họ tên / chức vụ → “Bắt buộc phải nhập”, thiếu số '
    'điện thoại liên hệ → “Bắt buộc nhập số điện thoại liên hệ”.\n'
    '– Tổ chức không chọn Công ty mẹ mà thiếu Mã số thuế → “Bắt buộc nhập”; Mã số thuế sai định dạng '
    '→ “Mã số thuế không đúng định dạng”; trùng → “Mã số thuế đã tồn tại”.\n'
    '– Tài khoản chưa gắn nhân sự → “Tài khoản chưa gắn nhân sự. Vui lòng liên hệ quản trị viên.”\n'
    '– Nếu có lỗi validate → báo đỏ dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin”, giữ '
    'nguyên dữ liệu và không thực hiện bước After.')

FORM_ROWS = [
    ('Là nhà cung cấp', 'Checkbox', 'Enable', 'Có / Không', 'Không', 'Không tích',
     'Đối tác đồng thời là nhà cung cấp — vẫn chỉ 1 bản ghi.'),
    ('Là khách hãng', 'Checkbox', 'Enable', 'Có / Không', 'Không', 'Không tích',
     'Tích thì Hãng xe thành bắt buộc.'),
    ('Tên khách hàng', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', '–'),
    ('Loại hình tổ chức', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Có', 'Trống',
     'Quyết định các khối hiện bên dưới: Cá nhân → khối Thông tin cá nhân; 4 loại còn lại → khối '
     'Thông tin tổ chức + Người liên hệ.'),
    ('Loại hình hoạt động khách hàng', 'Dropdown', 'Enable', 'Chọn nhiều', 'Không', 'Trống',
     'Icon ⓘ mô tả khái niệm. Danh mục đã khóa mà khách hàng đang dùng vẫn hiện kèm 🔒.'),
    ('Lĩnh vực kinh doanh khách hàng', 'Dropdown', 'Enable', 'Chọn nhiều, theo loại hình', 'Không',
     'Trống', 'Chỉ chọn được lĩnh vực thuộc loại hình đã chọn; hiển thị dạng “Loại hình : Lĩnh vực”.'),
    ('Nhóm khách hàng', 'Dropdown', 'Enable', 'Chọn nhiều', 'Không', 'Trống', '–'),
    ('Hãng xe', 'Dropdown', 'Enable', 'Chọn nhiều', 'Có khi tích “Là khách hãng”', 'Trống', '–'),
    ('Khối Thông tin cá nhân: CCCD/CMT, Ngày cấp, Nơi cấp, Tên đơn vị, Số điện thoại (nhiều số), '
     'Email, Website, Sinh nhật', 'Textbox / Datepicker', 'Enable',
     'Tối đa 255 ký tự; SĐT bắt đầu bằng 0, 10–12 chữ số; ngày dd/mm/yyyy ≤ hôm nay',
     'Có (Số điện thoại) khi là Cá nhân', 'Trống',
     'CCCD không trùng; nút + / thùng rác để thêm / bớt số điện thoại. Ô ngày không cho chọn ngày '
     'tương lai.'),
    ('Khối Thông tin tổ chức: Tên viết tắt, Công ty mẹ, Mã số thuế, Email, Số điện thoại bàn, Website',
     'Textbox / Dropdown', 'Enable', 'MST: chữ số và “-”, tối đa 14 ký tự; SĐT bàn ≤ 20 ký tự',
     'Có (Mã số thuế) khi KHÔNG chọn Công ty mẹ', 'Trống',
     'Chọn Công ty mẹ thì dấu * của Mã số thuế biến mất. Mã số thuế, Email không trùng.'),
    ('Địa chỉ xuất hóa đơn', 'Textbox', 'Enable', '–', 'Có với khách hàng tổ chức', 'Trống', '–'),
    ('Bảng Người đại diện (Tên người đại diện, Chức vụ)', 'Table/Grid', 'Enable', '≤ 255 ký tự',
     'Có với khách hàng tổ chức (≥ 1 người)', '1 dòng trống', 'Nút + / thùng rác để thêm / bớt dòng.'),
    ('Địa chỉ khách hàng / công ty: Quốc gia, Tỉnh/Thành phố, Quận/Huyện, Phường/Xã/Thị trấn, '
     'Đường/Thôn, Số nhà', 'Dropdown / Textbox', 'Enable', 'Danh sách phụ thuộc cấp trên',
     'Có: Quốc gia, Tỉnh/Thành phố, Phường/Xã', 'Trống',
     'Việt Nam: chọn Tỉnh xong chọn thẳng Phường/Xã (ẩn Quận/Huyện); nước ngoài hiện thêm Quận/Huyện. '
     'Đổi cấp trên thì các cấp dưới bị xóa và nạp lại.'),
    ('Bảng Tài khoản (Số TK, Chủ TK, Ngân hàng, Chi nhánh, Tỉnh/TP)', 'Table/Grid', 'Enable',
     '≤ 255 ký tự', 'Không', '1 dòng trống', 'Chi nhánh phụ thuộc Ngân hàng.'),
    ('Ghi chú', 'Textarea', 'Enable', '–', 'Không', 'Trống', '–'),
    ('Khối Người liên hệ (chỉ tổ chức): Họ tên, Chức vụ, Sinh nhật, Email, CCCD/CMT, Số điện thoại, '
     'Tài khoản cá nhân', 'Textbox / Datepicker / Table/Grid', 'Enable', '≤ 255 ký tự',
     'Có (Họ tên, Chức vụ, ≥ 1 số điện thoại; ≥ 1 người liên hệ)', '1 người liên hệ trống',
     'Nút “Thêm người liên hệ”; thùng rác xóa người liên hệ khi có từ 2 người.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ kèm biểu tượng cảnh báo ngay dưới ô bị lỗi.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Ghim ở thanh cuối màn; khóa trong lúc đang lưu để tránh tạo trùng.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Về danh sách; có thay đổi chưa lưu thì hỏi xác nhận rời trang.'),
]

d.h3('2.4 Tạo mới khách hàng')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới khách hàng', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-04 Tạo mới khách hàng')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới khách hàng',
    mota='Thêm một khách hàng mới. Form gồm nhiều khối, các khối hiện theo Loại hình tổ chức. Mã '
         'khách hàng do hệ thống sinh tự động khi lưu.',
    tacnhan='Người quản lý khách hàng',
    dieukien='Người dùng có quyền Q2.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở màn “Tạo khách hàng mới”, ban đầu chỉ có khối Thông tin khách hàng.\n'
          '3. Người dùng chọn Loại hình tổ chức; hệ thống hiện khối Thông tin cá nhân (Cá nhân) hoặc '
          'Thông tin tổ chức + Người liên hệ (4 loại tổ chức).\n'
          '4. Người dùng nhập thông tin và bấm Lưu.\n'
          '5. Hệ thống kiểm tra dữ liệu, sinh mã khách hàng, ghi bản ghi ở trạng thái Hoạt động và ghi '
          '1 dòng lịch sử “Tạo khách hàng”.\n'
          '6. Thông báo “Tạo khách hàng thành công” và quay về danh sách.',
    phu='• Dữ liệu không hợp lệ → báo lỗi đỏ dưới từng ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu.\n'
        '• Lỗi khác → thông báo “Tạo khách hàng thất bại”.\n'
        '• Rời màn khi đã nhập mà chưa lưu → hệ thống hỏi xác nhận.\n'
        '• Vào thẳng đường dẫn Tạo mới khi thiếu Q2 → thông báo “Bạn không có quyền thêm khách hàng” '
        'và quay về danh sách.',
    dacbiet='Khối “Địa chỉ giao hàng”, “Nhân viên phụ trách đại lý”, “Cấp đại lý” KHÔNG có ở màn Tạo '
            'mới, chỉ có ở màn Sửa. Ở form, chỉ ô Tên khách hàng được chặn ngay trên trình duyệt; các '
            'trường bắt buộc còn lại do hệ thống kiểm khi lưu.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('03-tao-moi.png'),
         shot_caption='Màn Tạo khách hàng mới lúc mới mở')
d.figure(shot('03a-tao-moi-ca-nhan.png'), 'Tạo mới khi chọn Loại hình tổ chức là Cá nhân',
         width_in=6.2)
d.figure(shot('03b-tao-moi-to-chuc.png'), 'Tạo mới khi chọn loại hình tổ chức (Doanh nghiệp tư nhân)',
         width_in=6.2)
d.figure(shot('03d-tao-moi-loi-be.png'), 'Báo lỗi dưới từng ô khi bấm Lưu thiếu trường bắt buộc',
         width_in=6.2)
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([('Tiêu đề “Tạo khách hàng mới”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–')]
           + FORM_ROWS)
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'Before:\n– Nút chỉ hiển thị khi có quyền Q2.\n'
     'After:\n– Mở màn Tạo mới với các ô trống.'),
    ('Đổi Loại hình tổ chức', 'Change',
     'After:\n– Hiện / ẩn khối Thông tin cá nhân, Thông tin tổ chức, Người liên hệ tương ứng.'),
    ('Đổi Quốc gia / Tỉnh/Thành phố / Quận/Huyện / Phường/Xã', 'Change',
     'After:\n– Xóa và nạp lại các cấp địa chỉ bên dưới.'),
    ('Chọn / bỏ Công ty mẹ', 'Change', 'After:\n– Mã số thuế chuyển thành không bắt buộc / bắt buộc.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q2.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING + '\n'
     'After:\n– Sinh mã khách hàng; ghi bản ghi trạng thái Hoạt động, người tạo, thời điểm tạo.\n'
     '– Ghi 1 dòng lịch sử “Tạo khách hàng”.\n'
     '– Thông báo “Tạo khách hàng thành công” và quay về danh sách.'),
    ('Bấm Quay lại', 'Click',
     'During:\n– Có thay đổi chưa lưu → hỏi xác nhận rời trang.\n'
     'After:\n– Về danh sách.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Chỉnh sửa khách hàng')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa khách hàng', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-05 Chỉnh sửa khách hàng')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa). '
           'Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa khách hàng',
    mota='Cập nhật thông tin một khách hàng đang Hoạt động. Dùng chung form với Tạo mới, có thêm khối '
         'Địa chỉ giao hàng, Nhân viên phụ trách đại lý, Cấp đại lý; mã khách hàng không đổi.',
    tacnhan='Người quản lý khách hàng',
    dieukien='Người dùng có quyền Q3 (và Q1 để nạp được dữ liệu); khách hàng nằm trong phạm vi dữ '
             'liệu và đang Hoạt động.',
    chinh='1. Người dùng bấm nút Sửa trên dòng (hoặc nút Sửa ở màn Chi tiết).\n'
          '2. Hệ thống mở màn “Chỉnh sửa khách hàng” với dữ liệu hiện tại.\n'
          '3. Người dùng sửa thông tin và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu, cập nhật và ghi 1 dòng lịch sử “Chỉnh sửa thông tin” gồm các '
          'trường đã đổi (giá trị cũ → giá trị mới).\n'
          '5. Thông báo “Cập nhật khách hàng thành công” và quay về danh sách.',
    phu='• Khách hàng đang Khóa → nút Sửa bị ẩn; vào thẳng đường dẫn Sửa → thông báo “Khách hàng đang '
        'bị khoá, vui lòng mở khoá trước khi chỉnh sửa.” và chuyển sang màn Chi tiết.\n'
        '• Khách hàng bị người khác khóa trong lúc đang sửa → bấm Lưu bị từ chối với ' + LOCKED_MSG + '\n'
        '• Vào thẳng đường dẫn Sửa khi thiếu Q3 → “Bạn không có quyền sửa khách hàng” và chuyển sang '
        'màn Chi tiết.\n'
        '• Giữ nguyên Mã số thuế / Email / CCCD của chính khách hàng → không báo trùng.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin”; '
        'lỗi khác → “Cập nhật khách hàng thất bại”.',
    dacbiet='Mã khách hàng bất biến. Danh mục (loại hình, lĩnh vực, nhóm…) đang gán nay đã khóa vẫn '
            'hiển thị đúng tên kèm 🔒.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('04-sua.png'), shot_caption='Màn Chỉnh sửa khách hàng')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Chỉnh sửa khách hàng”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Toàn bộ ô của form Tạo mới', 'Textbox / Dropdown / Datepicker', 'Enable', 'Như Tạo mới',
     'Như Tạo mới', 'Theo dữ liệu', 'Quy tắc bắt buộc và thông báo lỗi như FR-04.'),
    ('Nhân viên phụ trách đại lý', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Theo dữ liệu',
     'Chỉ có ở màn Sửa / Chi tiết.'),
    ('Cấp đại lý', 'Dropdown', 'Enable', 'Cấp 1 / Cấp 2 / Cấp 3', 'Không', 'Theo dữ liệu',
     'Chỉ có ở màn Sửa / Chi tiết.'),
    ('Khối Địa chỉ giao hàng (Quốc gia, Tỉnh/Thành phố, Quận/Huyện, Phường/Xã/Thị trấn, Đường/Thôn, '
     'Số nhà)', 'Dropdown / Textbox', 'Enable', '≤ 255 ký tự', 'Không', 'Theo dữ liệu',
     'Nút “Thêm địa chỉ giao hàng”; thùng rác xóa từng địa chỉ.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khóa trong lúc đang lưu.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiện với Q3 và khách hàng đang Hoạt động.\n'
     'During:\n– Nạp chi tiết khách hàng (kiểm Q1 và phạm vi dữ liệu); khách hàng đang Khóa → “Khách '
     'hàng đang bị khoá, vui lòng mở khoá trước khi chỉnh sửa.” và chuyển sang màn Chi tiết.\n'
     '– Lỗi nạp → “Lỗi khi tải thông tin khách hàng”.\n'
     'After:\n– Hiển thị form với dữ liệu hiện tại.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q3.\n' + NO_PERM + '\n'
     '– Khách hàng đang Khóa → ' + LOCKED_MSG + ' và dừng xử lý.\n'
     'During:\n' + SAVE_DURING + '\n– Bỏ qua kiểm tra trùng đối với chính khách hàng đang sửa.\n'
     'After:\n– Cập nhật bản ghi, giữ nguyên mã; ghi người cập nhật, thời điểm cập nhật.\n'
     '– Ghi 1 dòng lịch sử “Chỉnh sửa thông tin” với giá trị cũ → mới của từng trường đã đổi.\n'
     '– Thông báo “Cập nhật khách hàng thành công” và quay về danh sách.'),
    ('Bấm Quay lại', 'Click', 'After:\n– Về danh sách (hỏi xác nhận nếu có thay đổi chưa lưu).'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xem chi tiết khách hàng')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết khách hàng',
    mota='Xem toàn bộ thông tin một khách hàng ở chế độ chỉ đọc, kèm mục Lịch sử và các thao tác '
         'tương ứng với dòng ở màn danh sách.',
    tacnhan='Người quản lý khách hàng',
    dieukien='Người dùng có quyền Q1; khách hàng nằm trong phạm vi dữ liệu.',
    chinh='1. Người dùng bấm Mã KH trên bảng.\n'
          '2. Hệ thống mở màn “Chi tiết khách hàng: <mã>”, mọi ô ở chế độ chỉ đọc.\n'
          '3. (Tuỳ chọn) Người dùng bấm “Xem lịch sử” để mở rộng mục Lịch sử.\n'
          '4. Người dùng bấm Quay lại để về danh sách.',
    phu='• Thiếu Q1 (vào thẳng đường dẫn) → “Bạn không có quyền xem khách hàng” và quay về danh sách.\n'
        '• Khách hàng ngoài phạm vi dữ liệu → “Bạn không có quyền xem khách hàng này”.\n'
        '• Từ thanh cuối màn: Sửa (FR-05), Quản lý (FR-09), Khóa / Mở khóa (FR-07).',
    dacbiet=None)
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('05-xem.png'),
         shot_caption='Màn Chi tiết khách hàng ở chế độ chỉ đọc')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Chi tiết khách hàng: <mã>”', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '–'),
    ('Toàn bộ ô thông tin (như form Sửa)', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Không gõ được, không có nút Lưu.'),
    ('Mục Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở danh sách thay đổi (như FR-08).'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu', 'Chỉ hiện với Q3 và khách hàng đang Hoạt động.'),
    ('Nút Quản lý', 'Button', 'Enable', '–', 'Hiển thị', 'Mở màn Quản lý (FR-09).'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu Q4',
     'Khóa màu cam, Mở khóa màu xanh lá.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về danh sách.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Mã KH', 'Click',
     'Before:\n– Kiểm tra quyền Q1 và phạm vi dữ liệu.\n' + NO_PERM + '\n'
     'After:\n– Mở màn Chi tiết ở chế độ chỉ đọc.'),
    ('Bấm “Xem lịch sử”', 'Click', 'After:\n– Mở rộng mục Lịch sử và nạp danh sách thay đổi.'),
    ('Bấm Quay lại', 'Click', 'After:\n– Về màn danh sách, giữ bộ lọc trước đó.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Khóa / Mở khóa khách hàng')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Khóa / Mở khóa khách hàng', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-07 Khóa / Mở khóa khách hàng')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khóa / Mở khóa khách hàng',
    mota='Chuyển trạng thái khách hàng giữa Hoạt động và Khóa bằng nút ổ khóa ở cột Hành động hoặc '
         'nút Khóa / Mở khóa ở màn Chi tiết.',
    tacnhan='Người quản lý khách hàng',
    dieukien='Người dùng có quyền Q4.',
    chinh='1. Người dùng bấm nút Khóa (hoặc Mở khóa) trên dòng.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khóa” (hoặc “Xác nhận mở khóa”) nêu mã và tên khách hàng.\n'
          '3. Người dùng bấm Khóa (hoặc Mở khóa).\n'
          '4. Hệ thống đổi trạng thái, ghi 1 dòng lịch sử “Khóa khách hàng” / “Mở khóa khách hàng”, '
          'thông báo “Khóa khách hàng thành công!” / “Mở khóa khách hàng thành công!” và nạp lại danh sách.',
    phu='• Bấm Hủy → không đổi trạng thái.\n'
        '• Khách hàng không còn → “Không tìm thấy khách hàng”.\n'
        '• Lỗi khác → “Lỗi khi khóa khách hàng” / “Lỗi khi mở khóa khách hàng”.',
    dacbiet='Không có điều kiện nghiệp vụ chặn Khóa. Khách hàng đang Khóa không Sửa, không cập nhật '
            'thiết bị / tài liệu được cho tới khi Mở khóa. Khóa và Mở khóa dùng chung quyền “Xóa khách hàng”.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Khóa / Mở khóa', modal='Xác nhận khóa / Xác nhận mở khóa',
         shot=shot('06-khoa.png'), shot_caption='Hộp thoại xác nhận khóa khách hàng')
d.figure(shot('06b-mo-khoa.png'), 'Hộp thoại xác nhận mở khóa khách hàng', width_in=6.2)
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Khóa / Mở khóa trên dòng', 'Icon Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Đang Hoạt động: ổ khóa đóng (Khóa). Đang Khóa: ổ khóa mở (Mở khóa).'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khóa” / “Xác nhận mở khóa”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn khóa (mở khóa) khách hàng \'<mã> - <tên>\'?”'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Khóa / Mở khóa trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện với Q4.\nAfter:\n– Hiện hộp thoại xác nhận tương ứng.'),
    ('Bấm Khóa / Mở khóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q4.\n' + NO_PERM + '\n'
     'During:\n– Khách hàng không còn → “Không tìm thấy khách hàng” và dừng xử lý.\n'
     'After:\n– Đổi trạng thái; ghi người cập nhật; ghi 1 dòng lịch sử khi trạng thái thực sự đổi.\n'
     '– Thông báo thành công, nạp lại đúng trang và bộ lọc hiện tại.'),
    ('Bấm Hủy / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Xem lịch sử thay đổi')
d.p('2.8.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung thông tin riêng của Danh mục '
           'khách hàng.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của khách hàng',
    mota='Xem các lần Tạo, Chỉnh sửa thông tin, Cập nhật ảnh / tài liệu / video, Khóa, Mở khóa của '
         'một khách hàng: ai làm, lúc nào, trường nào đổi từ giá trị cũ sang giá trị mới.',
    tacnhan='Người quản lý khách hàng',
    dieukien='Người dùng có quyền Q5 (ở màn danh sách).',
    chinh='1. Người dùng bấm Lịch sử trên dòng (trực tiếp hoặc trong menu “…”).\n'
          '2. Hệ thống mở cửa sổ “Lịch sử khách hàng – Khách hàng: <mã> - <tên>”, nạp danh sách thay '
          'đổi MỚI NHẤT ở trên.\n'
          '3. (Tuỳ chọn) Bấm Bộ lọc để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.\n'
          '4. Người dùng bấm Đóng.',
    phu='• Chưa có thay đổi → “Chưa có lịch sử thay đổi.”\n'
        '• Bộ lọc không khớp → “Không có lịch sử phù hợp bộ lọc.”\n'
        '• Lỗi nạp → “Không tải được lịch sử khách hàng.” kèm nút Thử lại.',
    dacbiet=None)
d.p('2.8.2 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Lịch sử', modal='Lịch sử khách hàng',
         shot=shot('08-lich-su.png'), shot_caption='Cửa sổ Lịch sử khách hàng')
d.p('2.8.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     '“Lịch sử khách hàng” + dòng “Khách hàng: <mã> - <tên>”.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Thu gọn',
     'Mở ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay; nút Làm mới xóa lọc.'),
    ('Dòng thời gian thay đổi', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Mỗi mục: thời điểm, tên hành động (màu theo loại), người thực hiện — phòng ban, các trường đổi '
     'dạng giá trị cũ (đỏ) → giá trị mới (xanh); trường danh sách hiện dòng thêm / bớt.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thay đổi.”'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)
d.p('2.8.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lịch sử', 'Click', 'Before:\n– Thao tác chỉ hiện với Q5.\n'
     'After:\n– Mở cửa sổ và nạp danh sách thay đổi của khách hàng.'),
    ('Đổi điều kiện trong Bộ lọc', 'Change', 'After:\n– Lọc lại dòng thời gian ngay.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, danh sách phía sau giữ nguyên.'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Quản lý khách hàng')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Quản lý khách hàng', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-09 Quản lý khách hàng')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Quản lý khách hàng',
    mota='Màn tổng hợp thông tin nghiệp vụ của một khách hàng theo thẻ: Thông tin chung, Thông tin '
         'liên hệ (khách hàng tổ chức), Báo giá, Hợp đồng, Danh sách trang thiết bị, Thông tin khác.',
    tacnhan='Người quản lý khách hàng',
    dieukien='Người dùng có quyền Q1; khách hàng nằm trong phạm vi dữ liệu.',
    chinh='1. Người dùng chọn Quản lý trên dòng (hoặc nút Quản lý ở màn Chi tiết).\n'
          '2. Hệ thống mở màn “Quản lý khách hàng”, chọn sẵn thẻ Thông tin chung.\n'
          '3. Thẻ Báo giá / Hợp đồng: bảng hàng hóa và dịch vụ của đúng khách hàng, lọc theo ngày, '
          'nhân viên, phòng ban, công ty; có nút In và Xuất Excel.\n'
          '4. Thẻ Danh sách trang thiết bị: thiết bị đã bán và thiết bị khai ngoài hệ thống; Thêm thiết '
          'bị cũ, Thêm thiết bị NCC khác, Tăng số lượng, Sửa, Xóa, quản lý serial; In, Xuất Excel.\n'
          '5. Thẻ Thông tin khác: ảnh, tài liệu, video đính kèm; bấm Lưu để ghi.',
    phu='• Thiếu Q1 (vào thẳng đường dẫn) → “Bạn không có quyền xem khách hàng” và quay về danh sách.\n'
        '• Sửa / Xóa thiết bị, serial, tải ảnh – tài liệu cần Q3; Thêm thiết bị cũ, Thêm thiết bị NCC '
        'khác, Tăng số lượng chỉ cần Q1.\n'
        '• Khách hàng đang Khóa → mọi thao tác ghi bị từ chối với ' + LOCKED_MSG + '\n'
        '• Lưu Thông tin khác → “Cập nhật Thông tin khác thành công” / “Cập nhật Thông tin khác thất bại”.',
    dacbiet='Tăng số lượng thiết bị là CỘNG DỒN vào số lượng hiện có. Bản in có letterhead của công ty.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Quản lý', shot=shot('11-quan-ly.png'),
         shot_caption='Màn Quản lý khách hàng — thẻ Thông tin chung')
d.figure(shot('11c-quan-ly-thiet-bi.png'), 'Thẻ Danh sách trang thiết bị', width_in=6.2)
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Thẻ Thông tin chung', 'Table/Grid', 'Enable', '–', '–', 'Được chọn sẵn',
     'Form thông tin khách hàng như màn Sửa, kèm nút Lưu ở thanh cuối màn.'),
    ('Thẻ Thông tin liên hệ', 'Table/Grid', 'Enable', '–', '–', 'Ẩn nội dung',
     'Chỉ có với khách hàng tổ chức: danh sách người liên hệ.'),
    ('Thẻ Báo giá / Hợp đồng', 'Table/Grid', 'Read-only', '–', '–', 'Ẩn nội dung',
     'Chỉ hiện với Q1. Cột: STT, Ngày lập, Mã, Tổng thanh toán, Ngày hiệu lực (hợp đồng), Người tạo, '
     'Phòng ban. Bộ lọc Từ ngày – Đến ngày, Nhân viên, Phòng ban, Công ty; nút Lọc, Làm mới, In, Xuất Excel.'),
    ('Thẻ Danh sách trang thiết bị', 'Table/Grid', 'Enable', '–', '–', 'Ẩn nội dung',
     'Chỉ hiện với Q1. Cột: Tên thiết bị, Thương hiệu, Model, Mã thiết bị, Số lượng, Serial thiết bị '
     'làm dịch vụ, NCC thiết bị, Hành động.'),
    ('Nút Thêm thiết bị cũ / Thêm thiết bị NCC khác', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở cửa sổ khai thiết bị; bấm “Lưu lại” để ghi.'),
    ('Nút Tăng số lượng / Sửa / Xóa thiết bị', 'Icon Button', 'Enable', 'Số lượng ≥ 1', 'Có', 'Hiển thị',
     'Chỉ với thiết bị khai ngoài; số nhập được cộng dồn.'),
    ('Serial: Thêm serial, Sửa, Thay đổi, Xóa', 'Button', 'Enable', '≤ 255 ký tự', 'Có', 'Hiển thị',
     'Số serial không được trùng serial đã có trong hệ thống.'),
    ('Thẻ Thông tin khác: Ảnh, Thêm tài liệu, Thêm video (Tên, URL)', 'Button / Table/Grid', 'Enable',
     '–', 'Không', 'Theo dữ liệu', 'Kéo thả sắp xếp ảnh; xóa từng tệp.'),
    ('Nút Lưu / Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ở thanh cuối màn.'),
])
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Quản lý', 'Click',
     'Before:\n– Thao tác chỉ hiện với Q1.\n' + NO_PERM + '\n'
     'After:\n– Mở màn Quản lý, chọn sẵn thẻ Thông tin chung.'),
    ('Chuyển sang thẻ Báo giá / Hợp đồng / Danh sách trang thiết bị', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Nạp dữ liệu của đúng khách hàng đang xem (chỉ nạp khi mở thẻ lần đầu).'),
    ('Thêm / sửa / xóa thiết bị, serial', 'Click',
     'Before:\n– Kiểm tra quyền (Q1 cho thêm thiết bị / tăng số lượng; Q3 cho sửa, xóa, serial).\n'
     + NO_PERM + '\n– Khách hàng đang Khóa → ' + LOCKED_MSG + '\n'
     'During:\n– Thiếu dữ liệu bắt buộc / số lượng không hợp lệ / serial đã tồn tại → báo lỗi tương ứng.\n'
     'After:\n– Ghi thay đổi, nạp lại danh sách thiết bị.'),
    ('Bấm In / Xuất Excel trên thẻ', 'Click',
     'After:\n– In bảng kèm letterhead công ty / tải tệp Excel; lỗi → “Xuất Excel thất bại”.'),
    ('Bấm Lưu ở thẻ Thông tin khác', 'Click',
     'Before:\n– Kiểm tra quyền Q3; khách hàng đang Khóa → ' + LOCKED_MSG + '\n'
     'After:\n– Ghi ảnh / tài liệu / video, ghi lịch sử “Cập nhật ảnh / tài liệu / video”, thông báo '
     '“Cập nhật Thông tin khác thành công”.'),
])

# ---------------------------------------------------------------- 2.10
d.h3('2.10 Import Excel')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Import Excel khách hàng', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-10 Import Excel khách hàng')
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Import file, Validate dữ liệu và Thông báo.', anchor='excel')
d.intro_table(
    ten='Import Excel khách hàng',
    mota='Thêm mới hàng loạt khách hàng từ tệp Excel theo file mẫu. Có bước Validate trước khi ghi; '
         'dòng bỏ trống Tên khách hàng là người liên hệ / tài khoản của khách hàng ở dòng trên.',
    tacnhan='Người quản lý khách hàng',
    dieukien='Người dùng có quyền Q2.',
    chinh='1. Người dùng bấm Import Excel.\n'
          '2. (Tuỳ chọn) Bấm “Tải file mẫu” để lấy tệp Mau_import_khach_hang.xlsx (3 trang: Data, Loại '
          'hình - Lĩnh vực, Hướng dẫn; dữ liệu nhập từ dòng 3).\n'
          '3. Bấm “Chọn file Excel”, chọn tệp đã điền.\n'
          '4. Bấm “Load lên bảng” để đọc tệp ra bảng xem trước.\n'
          '5. Bấm “Validate” → hệ thống kiểm tra từng khách hàng (dòng cha + dòng con), đánh dấu hợp lệ / '
          'lỗi kèm lý do; dòng hợp lệ bị khóa.\n'
          '6. Nếu còn dòng lỗi: sửa trực tiếp các dòng lỗi rồi Validate lại, hoặc bấm “Bỏ dòng lỗi” '
          'để loại các dòng lỗi khỏi bảng.\n'
          '7. Khi đã Validate và không còn dòng lỗi, nút Import mới bấm được. Bấm “Import” → hệ '
          'thống ghi các khách hàng, thông báo “Import thành công <n> khách hàng”, đóng cửa sổ và nạp '
          'lại danh sách.',
    phu='• Chưa Validate, hoặc còn dòng lỗi → nút Import bị khóa, không bấm được.\n'
        '• Mọi dòng đều lỗi → sau khi bỏ dòng lỗi bảng không còn dòng nào, nút Import vẫn khóa; '
        'không import được.\n'
        '• Bấm “Bỏ dòng lỗi” → “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”\n'
        '• Bấm “Xoá trạng thái validate” → bỏ đánh dấu, mở khóa các dòng để sửa; phải Validate lại.\n'
        '• Dữ liệu thay đổi giữa lúc Validate và Import (vd người khác vừa tạo khách hàng trùng Mã số '
        'thuế / CMND): còn ghi được một phần → “Import thành công x/y khách hàng. z khách hàng thất '
        'bại.”, đóng cửa sổ và nạp lại danh sách; không ghi được khách hàng nào → báo lỗi ngay trong '
        'cửa sổ (lý do từng khách hàng, hoặc “Import thất bại”), cửa sổ giữ nguyên.\n'
        '• Tệp quá 500 dòng → “Mỗi lần import tối đa 500 dòng (file đang có N dòng), vui lòng tách '
        'file và import nhiều lần.”\n'
        '• Một dòng lỗi thì cả khách hàng (dòng cha lẫn dòng con) bị loại.\n'
        '• Bấm “Làm mới” → xóa dữ liệu đã nạp để chọn tệp khác.',
    dacbiet='Mỗi lần import tối đa 500 dòng. Mã khách hàng tự sinh như Tạo mới; mỗi khách hàng thêm '
            'thành công ghi 1 dòng lịch sử “Tạo khách hàng”.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Import Excel', modal='Import khách hàng', shot=shot('09-import.png'),
         shot_caption='Cửa sổ Import khách hàng sau khi Validate')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx / .xls', 'Có', 'Hiển thị', 'Chọn tệp cần import.'),
    ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Tải Mau_import_khach_hang.xlsx với dòng mẫu dùng danh mục thật; lỗi → “Lỗi khi tải file mẫu”.'),
    ('Nút Load lên bảng / Validate', 'Button', 'Enable / Disable', '–', '–',
     'Disable khi chưa đủ bước trước', 'Đọc tệp / kiểm tra dữ liệu.'),
    ('Nút Import', 'Button', 'Enable / Disable', '–', '–', 'Disable',
     'Chỉ bấm được khi đã Validate và không còn dòng lỗi.'),
    ('Ô Tổng / Hợp lệ / Lỗi', 'Label', 'Read-only', '≥ 0', '–', '0', 'Thống kê sau Validate.'),
    ('Cột Tên khách hàng *', 'Textbox', 'Enable', '≤ 255 ký tự', 'Có (dòng cha)', 'Theo tệp',
     'Để trống = dòng con của khách hàng phía trên.'),
    ('Cột Đối tượng *', 'Textbox', 'Enable', 'Cá nhân / Tổ chức / 4 loại tổ chức', 'Có', 'Theo tệp', '–'),
    ('Cột Nhóm khách hàng *', 'Textbox', 'Enable', 'Tên nhóm có trên hệ thống', 'Có', 'Theo tệp', '–'),
    ('Cột Số điện thoại, Số CMND/CCCD', 'Textbox', 'Enable', 'SĐT bắt đầu bằng 0, 10–12 số',
     'Có (SĐT) với Cá nhân', 'Theo tệp', 'CCCD không trùng hệ thống và trong tệp.'),
    ('Cột Mã số thuế, Fax, Người đại diện, Chức vụ người đại diện, Địa chỉ xuất hoá đơn', 'Textbox',
     'Enable', 'MST: chữ số và “-”, ≤ 14 ký tự', 'Có với Tổ chức', 'Theo tệp',
     'MST không trùng hệ thống và trong tệp.'),
    ('Cột Người liên hệ, Chức vụ người liên hệ, SĐT người liên hệ', 'Textbox', 'Enable',
     'Nhiều SĐT ngăn bằng dấu phẩy', 'Có với Tổ chức (≥ 1 người)', 'Theo tệp', '–'),
    ('Cột Quốc gia *, Tỉnh/Thành phố *, Quận/Huyện, Phường/Xã *, Thôn/Xóm, Số nhà, đường', 'Textbox',
     'Enable', 'Tên có trên hệ thống, đúng quan hệ cấp trên – cấp dưới', 'Có (3 cột *)', 'Theo tệp', '–'),
    ('Cột Số tài khoản, Chủ tài khoản, Ngân hàng, Tỉnh/TP ngân hàng, Chi nhánh', 'Textbox', 'Enable',
     '–', 'Không', 'Theo tệp', '–'),
    ('Cột Lĩnh vực kinh doanh khách hàng', 'Textbox', 'Enable', 'MãLoạiHình:MãLĩnhVực, ngăn dấu phẩy',
     'Không', 'Theo tệp', 'VD LHHDKH.0001:LVKDKH.0003.'),
    ('Nút Bỏ dòng lỗi', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu',
     'Loại các dòng lỗi khỏi bảng xem trước.'),
    ('Nút Xoá trạng thái validate', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu',
     'Bỏ kết quả Validate để sửa lại dữ liệu.'),
    ('Nút Đóng / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng / xóa dữ liệu đã nạp.'),
])
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Validate', 'Click',
     'Before:\n– Kiểm tra quyền Q2.\n' + NO_PERM + '\n'
     '– Tệp quá 500 dòng → báo “Mỗi lần import tối đa 500 dòng …” và dừng xử lý.\n'
     'During (từng khách hàng):\n'
     '– Dòng con không có dòng cha → “Dòng con không có khách hàng cha phía trên (cột Tên khách hàng '
     'đang trống)”.\n'
     '– “Đối tượng là bắt buộc” / “Đối tượng không hợp lệ (nhận: …)”; “Nhóm khách hàng là bắt buộc” / '
     '“Nhóm khách hàng \"<tên>\" không tồn tại trên hệ thống”; “Tên khách hàng tối đa 255 ký tự”.\n'
     '– “Quốc gia là bắt buộc”; Quốc gia / Tỉnh / Quận / Phường / Thôn “… không tồn tại trên hệ '
     'thống” hoặc “… không thuộc …”.\n'
     '– Cá nhân: “Số điện thoại là bắt buộc với khách hàng Cá nhân”; “Số điện thoại \"<số>\" không '
     'đúng định dạng”.\n'
     '– Tổ chức: “Mã số thuế là bắt buộc với khách hàng Tổ chức”; “Mã số thuế \"<mst>\" không đúng '
     'định dạng”; “Địa chỉ xuất hoá đơn là bắt buộc với khách hàng Tổ chức”; “Phải có ít nhất 1 người '
     'đại diện”; “Người đại diện phải có đủ Họ tên và Chức vụ”; “Phải có ít nhất 1 người liên hệ”; '
     '“Người liên hệ phải có đủ Họ tên, Chức vụ và Số điện thoại”.\n'
     '– Trùng: “<Mã số thuế | Số CMND/CCCD> \"<giá trị>\" bị trùng với dòng n trong file” / “… đã tồn '
     'tại trên hệ thống”.\n'
     '– Lĩnh vực: sai định dạng cặp; “Mã Loại hình / Lĩnh vực … không tồn tại hoặc đang bị khoá”; '
     '“Lĩnh vực … không thuộc Loại hình …”.\n'
     'After:\n– Đánh dấu hợp lệ / lỗi; thông báo “Validate thành công” hoặc “Validate xong: x hợp lệ, '
     'y không hợp lệ. (Dòng hợp lệ đã bị khoá)”. KHÔNG ghi dữ liệu ở bước này.'),
    ('Bấm Import', 'Click',
     'Before:\n– Kiểm tra quyền Q2.\n' + NO_PERM + '\n'
     '– Nút chỉ bấm được khi đã Validate và không còn dòng lỗi.\n'
     'During:\n– Chỉ gửi các dòng hợp lệ. Máy chủ kiểm tra lại các dòng gửi lên như bước Validate.\n'
     'After:\n– Thêm các khách hàng hợp lệ, người tạo là người thực hiện; ghi lịch sử.\n'
     '– Tất cả thành công → “Import thành công <n> khách hàng”, đóng cửa sổ, nạp lại danh sách.\n'
     '– Một phần (dữ liệu thay đổi giữa lúc Validate và Import) → “Import thành công x/y khách hàng. '
     'z khách hàng thất bại.”, đóng cửa sổ, nạp lại danh sách.\n'
     '– Không ghi được khách hàng nào → báo lỗi ngay trong cửa sổ (lý do từng khách hàng, hoặc '
     '“Import thất bại”); cửa sổ giữ nguyên, không ghi dữ liệu.'),
    ('Bấm Bỏ dòng lỗi', 'Click',
     'Before:\n– Chưa Validate → “Hãy Validate trước rồi mới bỏ dòng lỗi.”\n'
     'After:\n– Loại các dòng lỗi khỏi bảng; thông báo “Đã bỏ x dòng lỗi. Còn lại y dòng hợp '
     'lệ.”; nút Import mở nếu còn ≥ 1 dòng.'),
    ('Bấm Tải file mẫu', 'Click', 'After:\n– Tải tệp Mau_import_khach_hang.xlsx.'),
])

# ---------------------------------------------------------------- 2.11
d.h3('2.11 Xuất CSV / Excel / PDF')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Xuất CSV / Excel / PDF', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-11 Xuất CSV / Excel / PDF')
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của '
           'Danh mục khách hàng.', anchor='excel')
d.intro_table(
    ten='Xuất danh sách khách hàng ra CSV / Excel / PDF',
    mota='Người dùng chọn trường và thứ tự trường rồi tải về tệp gồm TẤT CẢ khách hàng khớp bộ lọc '
         'đang áp dụng trong phạm vi dữ liệu của mình (không chỉ trang đang xem).',
    tacnhan='Người quản lý khách hàng',
    dieukien='Người dùng có quyền Q6.',
    chinh='1. Người dùng (tuỳ chọn) đặt bộ lọc trên màn danh sách.\n'
          '2. Bấm Xuất CSV / Xuất Excel / Xuất PDF.\n'
          '3. Hệ thống mở cửa sổ “Chọn trường xuất <CSV|Excel|PDF>”, tích sẵn toàn bộ 20 trường.\n'
          '4. Người dùng tích / bỏ tích, kéo để đổi thứ tự, rồi bấm Xuất file.\n'
          '5. Hệ thống lấy dữ liệu theo từng lượt 2.000 dòng, hiện tiến độ “Đã tải a/N dòng…”, “Đang dựng '
          'file…”, dựng tệp và tải về danh_sach_khach_hang.<csv|xlsx|pdf>.\n'
          '6. Thông báo “Xuất CSV / Xuất Excel / Xuất PDF thành công”.',
    phu='• Bỏ chọn hết trường → nút Xuất file bị khóa.\n'
        '• Bộ lọc không có kết quả → “Không có dữ liệu để xuất”.\n'
        '• Lỗi → “Lỗi khi xuất csv / xuất excel / xuất pdf”.',
    dacbiet='3 nút xuất bị khóa trong lúc đang xuất để tránh bấm lặp.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất Excel',
         shot=shot('10-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất Excel')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường xuất', 'Table/Grid', 'Enable', '20 trường', 'Có (≥ 1)', 'Tích sẵn toàn bộ',
     'Mã KH, Tên KH, MST/SĐT, Đối tượng, Nhóm khách, Địa chỉ, Tỉnh/TP, Tên đơn vị, Tên viết tắt, Địa '
     'chỉ xuất hóa đơn, Hãng xe, Công ty mẹ, Cấp đại lý, Người đại diện, Tên liên hệ, SĐT liên hệ, Chức '
     'vụ liên hệ, Người tạo, Người cập nhật, Trạng thái. Kéo ⠿ để đổi thứ tự cột.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn nhanh.'),
    ('Dòng “Đang chọn x/20 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Khóa khi chưa chọn trường nào hoặc đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
    ('Dòng tiến độ cạnh nhóm nút xuất', 'Loading', 'Hiển thị', '–', '–', 'Ẩn',
     '“Đã tải a/N dòng…”, “Đang dựng file a/N dòng…”.'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất CSV / Xuất Excel / Xuất PDF', 'Click',
     'Before:\n– Nút chỉ hiện với Q6.\nAfter:\n– Mở cửa sổ Chọn trường xuất tương ứng, tích sẵn toàn bộ.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q6.\n' + NO_PERM + '\n'
     'During:\n– Áp đúng bộ lọc và phạm vi dữ liệu của màn danh sách; lấy dữ liệu theo từng lượt.\n'
     '– Không có dòng nào → “Không có dữ liệu để xuất” và dừng xử lý.\n'
     'After:\n– Tải tệp danh_sach_khach_hang với các trường theo thứ tự đã chọn; số trong Excel là số thật.\n'
     '– Thông báo “<Xuất CSV|Xuất Excel|Xuất PDF> thành công”.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Danh mục khách hàng; không lặp lại các quy '
           'tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi dữ liệu nhiều cấp', [
        '– Màn danh sách không gắn quyền xem; phạm vi quyết định bởi V1 → V2 → V3 → V4 (có cấp cao '
        'hơn thì áp cấp đó).',
        '– Không có cấp nào: chỉ thấy khách hàng do chính mình tạo.',
        '– Mọi cấp đều thấy thêm khách hàng mình tạo, mình đăng ký còn hạn hoặc đã có cuộc họp / dự án '
        'tiềm năng.',
        '– Xuất file dùng đúng phạm vi và bộ lọc của danh sách; chi tiết / Sửa / Quản lý chỉ mở được '
        'khách hàng trong phạm vi.',
    ], ['Danh sách', 'Tìm kiếm và lọc', 'Xem chi tiết', 'Xuất file']),
    ('BR-02', 'Bảo vệ khách hàng cá nhân', [
        '– Khách hàng cá nhân chỉ hiện khi: mình tạo; mình / người khác đăng ký còn hạn; đã phát sinh '
        'báo giá, cuộc họp hoặc dự án tiềm năng.',
        '– Khách hàng cá nhân tự do chỉ tìm được khi gõ ĐÚNG TRỌN số điện thoại.',
        '– Khách hàng tổ chức không chịu lớp này.',
    ], ['Danh sách', 'Tìm kiếm và lọc']),
    ('BR-03', 'Trường bắt buộc theo Loại hình tổ chức', [
        '– Chung: Tên khách hàng, Loại hình tổ chức, Quốc gia, Tỉnh/Thành phố, Phường/Xã.',
        '– Cá nhân: ≥ 1 số điện thoại (bắt đầu bằng 0, 10–12 chữ số).',
        '– Tổ chức: Địa chỉ xuất hóa đơn; ≥ 1 người đại diện (tên + chức vụ); ≥ 1 người liên hệ '
        '(họ tên + chức vụ + ≥ 1 số điện thoại).',
        '– Là khách hãng: bắt buộc Hãng xe.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-04', 'Mã số thuế phụ thuộc Công ty mẹ', [
        '– Tổ chức không chọn Công ty mẹ: Mã số thuế bắt buộc.',
        '– Đã chọn Công ty mẹ: không bắt buộc.',
        '– Đã nhập thì chỉ gồm chữ số và “-”, tối đa 14 ký tự.',
        '– Import không có cột Công ty mẹ nên Mã số thuế luôn bắt buộc với tổ chức.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-05', 'Trường duy nhất', [
        '– Email, Mã số thuế, Số CMND/CCCD không trùng trong toàn hệ thống.',
        '– Khi sửa, bỏ qua chính khách hàng đang sửa; khi import, kiểm cả trùng giữa các dòng trong tệp.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-06', 'Cặp Loại hình hoạt động – Lĩnh vực kinh doanh', [
        '– Không bắt buộc; lĩnh vực phải thuộc đúng loại hình đã chọn.',
        '– Import dùng cú pháp MãLoạiHình:MãLĩnhVực; mã đang khóa không dùng được.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel', 'Tìm kiếm và lọc']),
    ('BR-07', 'Sinh mã khách hàng', [
        '– Mã = biển số tỉnh + ký hiệu tỉnh + ký hiệu phường/xã; trùng thì thêm “-01”, “-02”…',
        '– Mã bất biến sau khi tạo.',
    ], ['Tạo mới', 'Import Excel']),
    ('BR-08', 'Khóa không phải Xóa; khách hàng đã khóa không được cập nhật', [
        '– Không có chức năng xóa hẳn khách hàng; Khóa / Mở khóa dùng quyền “Xóa khách hàng”.',
        '– Khách hàng đang Khóa: ẩn nút Sửa; mọi thao tác ghi (lưu form, thiết bị, serial, tài liệu, '
        'thêm người liên hệ) bị hệ thống từ chối cho tới khi Mở khóa.',
        '– Khách hàng đã khóa vẫn nằm trong danh sách, vẫn xem, xuất, xem lịch sử được.',
    ], ['Khóa / Mở khóa', 'Chỉnh sửa', 'Quản lý khách hàng']),
    ('BR-09', 'Thao tác không dùng được thì ẩn', [
        '– Tạo mới, Import, Xuất, Sửa, Khóa / Mở khóa, Quản lý, Lịch sử chỉ hiện khi có quyền tương ứng '
        'và đủ điều kiện trạng thái.',
        '– Màn Chi tiết hiện cùng bộ thao tác như dòng ở danh sách (trừ Lịch sử đã nhúng sẵn).',
    ], ['Danh sách', 'Xem chi tiết']),
    ('BR-10', 'Ghi lịch sử thay đổi', [
        '– Ghi lại Tạo (kể cả qua Import), Chỉnh sửa thông tin, Cập nhật ảnh / tài liệu / video, Khóa, '
        'Mở khóa; chỉ ghi Khóa / Mở khóa khi trạng thái thực sự đổi.',
        '– Chỉnh sửa chỉ ghi các trường thực sự đổi, dạng giá trị cũ → giá trị mới; mới nhất ở trên.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Khóa / Mở khóa', 'Import Excel', 'Xem lịch sử']),
    ('BR-11', 'Import theo nhóm khách hàng', [
        '– Tối đa 500 dòng / lần; dữ liệu từ dòng 3 của tệp mẫu.',
        '– Dòng bỏ trống Tên khách hàng là dòng con (người liên hệ / tài khoản) của khách hàng phía trên.',
        '– Một dòng lỗi thì cả khách hàng bị loại; chỉ khách hàng hợp lệ được thêm.',
    ], 'Import Excel'),
    ('BR-12', 'Quyền cần kèm khi mở dữ liệu một khách hàng', [
        '– Màn Chi tiết, Sửa, Quản lý đều nạp dữ liệu qua cùng một đường đòi quyền Q1 và phạm vi dữ liệu.',
        '– Vì vậy thao tác Sửa thực tế cần cả Q3 và Q1.',
    ], ['Chỉnh sửa', 'Xem chi tiết', 'Quản lý khách hàng']),
    ('BR-13', 'Cấu hình hiển thị theo người dùng', [
        '– Cấu hình cột và tiêu chí lọc lưu riêng theo người dùng, theo màn.',
        '– STT, Mã KH, Hành động luôn hiện; ẩn một tiêu chí lọc thì xóa luôn giá trị lọc của nó.',
    ], ['Cài đặt bộ lọc và tuỳ chỉnh cột']),
])

d.save(update_fields=False)

# -*- coding: utf-8 -*-
"""Sinh "SRS - Danh mục loại giảm giá.docx" theo code nhánh gop_db — form 2026-09-24.

Chạy:  python3 .plans/gop-db/srs-danh-muc-du-an/loai-giam-gia/gen_srs.py
Ảnh chụp thật (Playwright 1440x900, bản gop_db cổng 3002): loai-giam-gia_shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/discount-types/index.vue · components/modal/discount-type-modal.vue
      pages/assign/quotations/_id/edit.vue (nơi dùng danh mục)
      components/subsystem-menu/sale-hub.js (menu: Danh mục > Danh mục chung) · sale.js (gate quyền)
  BE  Modules/Assign/Routes/api.php (nhóm /assign/discount_types)
      Http/Requests/DiscountType/DiscountTypeRequest.php
      Http/Controllers/Api/V1/DiscountTypeController.php · Services/DiscountTypeService.php
      Entities/DiscountType.php · Transformers/DiscountType
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 1090)
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))

from srs_docx_lib import SrsDoc  # noqa: E402
import srs_docx_lib as _lib  # noqa: E402
from docx.opc.constants import RELATIONSHIP_TYPE as _RT  # noqa: E402
from docx.oxml.ns import qn as _qn  # noqa: E402

_orig_add_hyperlink = _lib.add_hyperlink


def _add_hyperlink_rieng(paragraph, url, text):
    """Moi doan "Quy tac chung" 1 relationship rieng (nhu file da qua Word).

    save(update_fields=False) khong cho Word tach rel, python-docx lai gop rel trung URL
    -> selfcheck dem "hyperlink" < so doan "Quy tac chung" va bao sai.
    """
    link = _orig_add_hyperlink(paragraph, url, text)
    rels = paragraph.part.rels
    rid = rels._next_rId
    rels.add_relationship(_RT.HYPERLINK, url, rid, is_external=True)
    link.set(_qn('r:id'), rid)
    return link


_lib.add_hyperlink = _add_hyperlink_rieng


OUT = os.path.join(HERE, 'SRS - Danh mục loại giảm giá.docx')
SHOTS = os.path.join(HERE, 'loai-giam-gia_shots')
MENU = 'Phân hệ Bán hàng => Danh mục => Danh mục chung => Loại giảm giá'

A_QL = 'Người quản lý danh mục loại giảm giá (Q1)'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')
CHANGED = '“Dữ liệu đã thay đổi, vui lòng tải lại”'


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/discount-types',
           full_url='https://<host-hrm>/assign/discount-types', img_prefix='loaigiamgia_gopdb_')

# Icon cho từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện.
# Nhãn nút trên dòng viết "Khoá" / "Mở khoá" (oa) nên key menu theo đúng chữ đó.
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ Bán hàng': 'phanhe', 'Danh mục': 'danhmuc', 'Danh mục chung': 'nhom',
    'Loại giảm giá': 'man',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidatboloc', 'Tuỳ chỉnh cột': 'tuychinhcot',
    'Tạo mới': 'taomoi', 'Sửa': 'sua', 'Xem chi tiết': 'xem', 'Xem lịch sử': 'xemlichsu',
    'Xóa': 'xoa', 'Xóa nhiều': 'xoanhieu', 'Duyệt': 'duyet', 'Khoá': 'khoa', 'Mở khoá': 'mokhoa',
    'Xuất Excel': 'xuat',
}.items()})

d.title_block('Danh mục loại giảm giá')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục loại giảm giá thuộc phân hệ Bán '
    'hàng (nhóm Danh mục chung), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ vòng đời 3 trạng thái của loại giảm giá: Chờ duyệt → Hoạt động ↔ Khóa.',
    'Làm rõ ràng buộc giữa Loại giảm giá với các dòng giảm giá trong báo giá đang dùng nó: khi nào '
    'được sửa, xóa, khóa.',
    'Làm rõ quy tắc xóa nhiều và xuất dữ liệu ra tệp Excel.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Loại giảm giá', 'Phân loại khoản giảm giá áp dụng trong báo giá (VD: Giảm giá tổng đơn, Giảm '
     'giá khách hàng thân thiết…).'),
    ('Mã loại giảm giá', 'Mã do hệ thống tự sinh khi tạo, dạng GG-YYYY-NNNNN (năm hiện tại + số thứ '
     'tự 5 chữ số). Không nhập, không sửa được.'),
    ('Chờ duyệt', 'Loại giảm giá được tạo nhanh ngay trong một báo giá; chỉ báo giá đó dùng được cho '
     'tới khi người quản lý danh mục Duyệt.'),
    ('Duyệt', 'Chuyển loại giảm giá từ Chờ duyệt sang Hoạt động, bỏ gắn với báo giá tạo ra nó → mọi '
     'báo giá đều dùng được.'),
    ('Loại giảm giá đã sử dụng', 'Loại giảm giá đã được chọn ở ít nhất 1 dòng giảm giá của báo giá.'),
    ('Trạng thái Khóa', 'Loại giảm giá ngừng sử dụng: không được chọn ở báo giá, không sửa được. Khóa '
     'KHÔNG xóa dữ liệu, có thể Mở khóa lại.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý danh mục loại giảm giá',
     'Vào được màn hình; xem danh sách, xem chi tiết, xem lịch sử; Tạo mới, Sửa, Xóa, Xóa nhiều, '
     'Duyệt, Khóa / Mở khóa, Xuất Excel.'),
], widths=[0.8, 2.0, 3.2])
d.p('Danh mục chỉ có 1 quyền (không có quyền chỉ xem riêng). Màn hình không phân quyền theo cấp '
    'dữ liệu (công ty / phòng ban / bộ phận): người có quyền thấy toàn bộ loại giảm giá của hệ thống. '
    'Mục menu Loại giảm giá chỉ hiện với người có Q1.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách loại giảm giá', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '❌'),
    ('FR-04 Tạo mới loại giảm giá', '✅', '❌'),
    ('FR-05 Chỉnh sửa loại giảm giá', '✅', '❌'),
    ('FR-06 Xem chi tiết và lịch sử loại giảm giá', '✅', '❌'),
    ('FR-07 Xóa loại giảm giá', '✅', '❌'),
    ('FR-08 Xóa nhiều loại giảm giá', '✅', '❌'),
    ('FR-09 Duyệt loại giảm giá', '✅', '❌'),
    ('FR-10 Khóa / Mở khóa loại giảm giá', '✅', '❌'),
    ('FR-11 Xuất Excel', '✅', '❌'),
], widths=[3.6, 0.9, 1.5])

# ================================================================ PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_QL, [0, 1, 2, 3, 4, 5, 6, 7])],
    [('FR-01', 'Xem danh sách loại giảm giá', 'view'),
     ('FR-04', 'Tạo mới loại giảm giá', 'crud'),
     ('FR-05', 'Chỉnh sửa loại giảm giá', 'crud'),
     ('FR-07', 'Xóa loại giảm giá', 'action'),
     ('FR-08', 'Xóa nhiều loại giảm giá', 'action'),
     ('FR-09', 'Duyệt loại giảm giá', 'action'),
     ('FR-10', 'Khóa / Mở khóa loại giảm giá', 'action'),
     ('FR-11', 'Xuất Excel danh sách loại giảm giá', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết và lịch sử', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Danh mục loại giảm giá')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách loại giảm giá')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Danh mục loại giảm giá tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách loại giảm giá',
    mota='Hiển thị toàn bộ loại giảm giá kèm mã, tên, người tạo / cập nhật, trạng thái và các thao '
         'tác trên từng dòng.',
    tacnhan='Người quản lý danh mục loại giảm giá; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có quyền Q1.',
    chinh='1. Người dùng vào menu Phân hệ Bán hàng → Danh mục → Danh mục chung → Loại giảm giá.\n'
          '2. Hệ thống nạp trang 1, 10 dòng/trang, bản ghi mới tạo lên đầu.\n'
          '3. Bảng hiển thị đủ các cột (mặc định hiện hết cột), dòng “Hiển thị a–b / N” và thanh '
          'phân trang.',
    phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm Mã loại giảm giá → mở cửa sổ Xem chi tiết (FR-06).\n'
        '• Bấm tiêu đề cột Mã, Tên, Ngày tạo, Ngày cập nhật → sắp xếp theo cột đó, bấm lại để đảo '
        'chiều.\n'
        '• Tích ô chọn ở đầu dòng → hiện thanh “Đã chọn n dòng” với nút Xóa, Bỏ chọn (FR-08).\n'
        '• Rời màn rồi quay lại trong vòng 10 phút → bộ lọc đang dùng được khôi phục.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách loại giảm giá lúc mới truy cập')
d.figure(shot('07-hanh-dong.png'), 'Cột Trạng thái (3 trạng thái) và cột Hành động theo từng trạng '
         'thái', width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Danh mục loại giảm giá”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Dòng “Chưa chọn dòng nào.” / “Đã chọn n dòng”', 'Label', 'Hiển thị', '–', '“Chưa chọn dòng nào.”',
     'Khi đã chọn dòng thì kèm nút Xóa và Bỏ chọn (FR-08).'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị', 'Mở form Tạo mới (FR-04).'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Chọn trường xuất file (FR-11).'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Cột Chọn (ô tích)', 'Table/Grid', 'Enable / Disable', '–', 'Chưa tích',
     'Ô tích ở tiêu đề chọn cả trang. Chỉ tích được loại giảm giá đủ điều kiện xóa. Cố định bên '
     'trái, không tắt được.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cố định bên trái khi cuộn ngang; không tắt được.'),
    ('Cột Mã loại giảm giá', 'Table/Grid', 'Read-only', 'GG-YYYY-NNNNN', 'Theo dữ liệu',
     'Cố định bên trái, không tắt được, sắp xếp được. Là liên kết mở cửa sổ Xem chi tiết.'),
    ('Cột Tên loại giảm giá', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Sắp xếp được; tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Người tạo hiển thị tên nhân viên. Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa / Chờ duyệt', 'Theo dữ liệu',
     'Hoạt động màu xanh lá, Khóa màu đỏ, Chờ duyệt màu cam.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu',
     'Không tắt được. Thứ tự Sửa, Xóa, Duyệt, Khoá / Mở khoá. Dòng có tối đa 3 thao tác thì hiện '
     'hết; nhiều hơn thì hiện 2 nút đầu, phần còn lại gom vào nút “…”.'),
    ('Nút Sửa (bút)', 'Icon Button', 'Enable / Disable', '–', 'Theo dữ liệu',
     'Dùng được khi loại giảm giá chưa bị Khóa (FR-05). Hiện tại khi không dùng được nút vẫn hiển thị mờ, rê chuột hiện “Loại giảm giá đã khoá → không cho sửa”.'),
    ('Nút Xóa (thùng rác)', 'Icon Button', 'Enable / Disable', '–', 'Theo dữ liệu',
     'Dùng được khi loại giảm giá đang Chờ duyệt, hoặc chưa được dùng trong báo giá nào (FR-07). Hiện tại khi không dùng được nút vẫn hiển thị mờ, rê chuột hiện “Loại giảm giá đã được sử dụng, không thể xoá”.'),
    ('Nút Duyệt (dấu tích)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với loại giảm giá đang Chờ duyệt (FR-09).'),
    ('Nút Khoá / Mở khoá', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Ẩn với loại giảm giá đang Chờ duyệt. Đang Hoạt động hiện Khoá, đang Khóa hiện Mở khoá (FR-10).'),
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả', 'N là tổng số bản ghi khớp bộ lọc.'),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5 / 10 / 20 / 50', '10', 'Đổi thì quay về trang 1.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Về đầu / lùi / số trang / tiến / về cuối.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Hiển thị ngay khi vào màn', 'Tắt khi nạp xong.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu có).\n'
     '– Nạp cấu hình cột đã lưu của người dùng.\n'
     'After:\n– Hiển thị trang 1, 10 dòng, bản ghi mới tạo lên đầu.'),
    ('Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click',
     'After:\n– Sắp xếp theo cột đó, bấm lại để đảo chiều; quay về trang 1.'),
    ('Bấm số trang / đổi Số dòng/trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu; đổi số dòng/trang thì quay về trang 1.'),
    ('Bấm Mã loại giảm giá', 'Click', 'After:\n– Mở cửa sổ Xem chi tiết (FR-06).'),
    ('Tích / bỏ tích ô chọn', 'Change',
     'After:\n– Cập nhật số dòng đã chọn; hiện nút Xóa, Bỏ chọn khi có ít nhất 1 dòng được chọn.'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Danh mục '
           'loại giảm giá tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc loại giảm giá',
    mota='Tìm nhanh theo mã, tên loại giảm giá hoặc tên người tạo; lọc nâng cao theo trạng thái, '
         'người tạo, khoảng ngày tạo.',
    tacnhan='Người quản lý danh mục loại giảm giá; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách loại giảm giá.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
          '3. Chọn giá trị ở ô Trạng thái, Người tạo, Ngày tạo: chọn xong hệ thống tự lọc lại ngay.\n'
          '4. Bảng hiển thị kết quả từ trang 1.',
    phu='• Bấm Làm mới → xóa hết điều kiện lọc, trả về danh sách ban đầu.\n'
        '• Bấm “Ẩn tìm kiếm nâng cao” → thu gọn khối lọc, điều kiện đang chọn vẫn giữ.\n'
        '• Không có kết quả → “Không có dữ liệu phù hợp bộ lọc.”',
    dacbiet=None)
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-bo-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Placeholder “Tìm theo mã, tên loại giảm giá, người tạo”. Tìm gần đúng. Áp dụng khi bấm Tìm '
     'kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao (nhãn đổi thành “Ẩn tìm kiếm nâng cao” khi đang mở).'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Trống',
     'Danh sách chọn chưa có giá trị Chờ duyệt.'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', 'Lọc đúng theo người tạo.'),
    ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống',
     'Một ô gồm 2 ngày Từ → Đến, tính cả 2 đầu mút.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm / Enter', 'Click / Keypress',
     'Before:\n– Lấy từ khóa, bỏ khoảng trắng đầu cuối.\n'
     'After:\n– Lọc theo toàn bộ điều kiện; hiển thị trang 1.'),
    ('Đổi giá trị một ô trong khối lọc', 'Change',
     'After:\n– Tự lọc lại ngay theo toàn bộ điều kiện đang chọn.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xóa mọi điều kiện, sắp xếp mặc định, hiển thị trang 1.'),
])

# ---------------------------------------------------------------- 2.3
d.h3('2.3 Cài đặt bộ lọc và tuỳ chỉnh cột')
d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', actor='Người dùng đã đăng nhập',
            caption='Biểu đồ Use Case — FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột')
d.p('2.3.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Cài đặt bộ lọc và tuỳ chỉnh cột hiển thị',
    mota='Mỗi người dùng tự chọn trường lọc nào hiện trong khối Tìm kiếm nâng cao, cột nào hiện '
         'trên bảng, và sắp xếp thứ tự bằng kéo thả. Cấu hình lưu riêng theo từng người.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách loại giảm giá.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ với danh sách trường / cột, đánh dấu những mục đang hiện.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho người dùng, đóng cửa sổ và vẽ lại khối lọc / bảng.',
    phu='• Bấm “Khôi phục mặc định” → trả về bộ trường lọc mặc định của màn.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Cột Chọn, STT, Mã loại giảm giá và Hành động luôn hiện, không bỏ tích được (hiển thị xám '
        '+ ổ khóa).',
    dacbiet='Mặc định màn hiện TẤT CẢ cột; người dùng tự tắt bớt nếu thấy bảng quá rộng.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột', modal='Cài đặt bộ lọc và Tuỳ chỉnh cột',
         shot=shot('02b-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('02c-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột — cột khóa hiển thị xám', width_in=6.2)
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường lọc', 'Table/Grid', 'Enable', '3 trường', 'Không', 'Theo cấu hình đã lưu',
     'Trạng thái, Người tạo, Ngày tạo. Mỗi dòng: số thứ tự, biểu tượng kéo ⠿, ô tích, tên trường.'),
    ('Nút Lưu (Cài đặt bộ lọc)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình trường lọc.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về bộ trường lọc mặc định.'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '10 cột', 'Không', 'Theo cấu hình đã lưu',
     'Cột Chọn, STT, Mã loại giảm giá, Hành động bị khóa (luôn hiện).'),
    ('Nút Lưu (Tuỳ chỉnh cột)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình cột.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
])
d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Kéo biểu tượng ⠿', 'Drag', 'After:\n– Đổi thứ tự trường / cột trong danh sách.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Lưu cấu hình theo người dùng đang đăng nhập; đóng cửa sổ; vẽ lại khối lọc / bảng.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Đưa danh sách về cấu hình mặc định của màn.'),
])

# ---------------------------------------------------------------- 2.4
SAVE_DURING = (
    '– Tên loại giảm giá trống → “Tên loại giảm giá là bắt buộc”.\n'
    '– Tên quá 255 ký tự → “Tên loại giảm giá tối đa 255 ký tự”.\n'
    '– Nếu có lỗi validate → thông báo “Bạn chưa nhập đầy đủ thông tin” và không thực hiện bước After.')
ROW_CLOSE = ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.')
ROW_ERR = ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
           'Chữ đỏ ngay dưới ô bị lỗi.')

d.h3('2.4 Tạo mới loại giảm giá')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới loại giảm giá', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-04 Tạo mới loại giảm giá')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới loại giảm giá',
    mota='Thêm một loại giảm giá mới vào danh mục; mã do hệ thống tự sinh.',
    tacnhan='Người quản lý danh mục loại giảm giá',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở cửa sổ “Thêm loại giảm giá” (không có ô Mã), Trạng thái mặc định Hoạt động.\n'
          '3. Người dùng nhập Tên loại giảm giá, chọn Trạng thái.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống kiểm tra dữ liệu, sinh mã GG-YYYY-NNNNN, ghi bản ghi mới và ghi 1 dòng lịch sử '
          '“Tạo mới”.\n'
          '6. Thông báo “Thêm mới thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Bấm “Lưu & Tiếp tục” → lưu xong giữ cửa sổ mở, xóa trắng form để nhập bản ghi tiếp.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu đã nhập.\n'
        '• Lỗi khác → thông báo “Lưu thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Nút Lưu và Lưu & Tiếp tục bị khóa trong lúc đang xử lý để tránh tạo trùng. Tạo từ màn '
            'danh mục chỉ chọn được Hoạt động hoặc Khóa; trạng thái Chờ duyệt chỉ phát sinh khi tạo '
            'nhanh trong báo giá.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', modal='Thêm loại giảm giá', shot=shot('03-tao-moi.png'),
         shot_caption='Cửa sổ Thêm loại giảm giá')
d.figure(shot('03b-tao-moi-loi.png'), 'Cửa sổ Thêm loại giảm giá khi bấm Lưu mà chưa nhập tên',
         width_in=6.2)
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Thêm loại giảm giá”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Tên loại giảm giá', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Placeholder “VD: Giảm giá khách hàng thân thiết”.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động',
     'Không có nút xóa chọn — luôn có giá trị.'),
    ROW_ERR,
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu rồi đóng cửa sổ.'),
    ('Nút Lưu & Tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Lưu rồi xóa trắng form để nhập tiếp. Chỉ có ở Tạo mới.'),
    ROW_CLOSE,
])
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'After:\n– Mở cửa sổ với form trống, Trạng thái = Hoạt động.'),
    ('Bấm Lưu / Lưu & Tiếp tục', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING + '\n'
     'After:\n– Sinh mã GG-YYYY-NNNNN, ghi bản ghi mới; ghi người tạo, thời điểm tạo.\n'
     '– Ghi 1 dòng lịch sử “Tạo mới”.\n'
     '– Thông báo “Thêm mới thành công”, nạp lại danh sách.\n'
     '– Lưu: đóng cửa sổ. Lưu & Tiếp tục: giữ cửa sổ, xóa trắng form.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, không lưu dữ liệu đang nhập.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Chỉnh sửa loại giảm giá')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa loại giảm giá', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-05 Chỉnh sửa loại giảm giá')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa). '
           'Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa loại giảm giá',
    mota='Cập nhật tên (và trạng thái Hoạt động / Khóa) của một loại giảm giá chưa bị Khóa. Mã không '
         'sửa được.',
    tacnhan='Người quản lý danh mục loại giảm giá',
    dieukien='Người dùng có quyền Q1; loại giảm giá đang Hoạt động hoặc Chờ duyệt.',
    chinh='1. Người dùng bấm nút Sửa trên dòng.\n'
          '2. Hệ thống mở cửa sổ “Sửa loại giảm giá” với dữ liệu hiện tại (Mã chỉ đọc).\n'
          '3. Người dùng sửa thông tin và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu, cập nhật và ghi 1 dòng lịch sử các trường đã đổi '
          '(giá trị cũ → giá trị mới).\n'
          '5. Thông báo “Cập nhật thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Loại giảm giá đang Khóa → không Sửa được; phải Mở khoá trước.\n'
        '• Loại giảm giá đang Chờ duyệt → chỉ sửa được tên, ô Trạng thái bị khóa (đổi trạng thái '
        'phải qua nút Duyệt).\n'
        '• Chọn Trạng thái = Khóa → khi lưu, loại giảm giá chuyển sang Khóa và ghi thêm 1 dòng lịch '
        'sử “Thay đổi trạng thái”.\n'
        '• Bản ghi đã bị xóa / khóa bởi người khác trong lúc sửa → ' + CHANGED + '.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới ô, thông báo “Bạn chưa nhập đầy đủ thông tin”.',
    dacbiet='Tên mới hiển thị ở mọi báo giá đang dùng loại giảm giá này.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', modal='Sửa loại giảm giá', shot=shot('04-sua.png'),
         shot_caption='Cửa sổ Sửa loại giảm giá')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Sửa loại giảm giá”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Mã loại giảm giá', 'Textbox', 'Read-only', 'GG-YYYY-NNNNN', '–', 'Theo dữ liệu', 'Không sửa được.'),
    ('Tên loại giảm giá', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo dữ liệu', 'Như Tạo mới.'),
    ('Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa (+ Chờ duyệt để hiển thị)',
     'Không', 'Theo dữ liệu', 'Bị khóa khi loại giảm giá đang Chờ duyệt.'),
    ROW_ERR,
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Không có nút Lưu & Tiếp tục.'),
    ROW_CLOSE,
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Dùng được khi loại giảm giá chưa bị Khóa.\n'
     'During:\n– Nạp chi tiết bản ghi.\n'
     '– Bản ghi không còn → ' + CHANGED + ', không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ Sửa với dữ liệu hiện tại.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Loại giảm giá đã bị Khóa, hoặc đổi trạng thái của bản Chờ duyệt → ' + CHANGED + '.\n'
     'During:\n' + SAVE_DURING + '\n'
     'After:\n– Cập nhật bản ghi; ghi người cập nhật, thời điểm cập nhật.\n'
     '– Ghi 1 dòng lịch sử các trường đã đổi (Tên); đổi Trạng thái ghi thêm dòng “Thay đổi trạng '
     'thái”.\n'
     '– Thông báo “Cập nhật thành công”, đóng cửa sổ, nạp lại danh sách.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xem chi tiết và lịch sử loại giảm giá')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Hiển thị lịch sử theo SRS Các quy tắc chung - Quy tắc '
           'ghi lịch sử.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết và lịch sử loại giảm giá',
    mota='Xem thông tin của một loại giảm giá ở chế độ chỉ đọc, kèm khối Lịch sử thay đổi (Tạo mới, '
         'Thay đổi thông tin, Thay đổi trạng thái, Xóa: ai làm, lúc nào, giá trị cũ → mới).',
    tacnhan='Người quản lý danh mục loại giảm giá',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm vào Mã loại giảm giá trên bảng.\n'
          '2. Hệ thống mở cửa sổ “Xem loại giảm giá”, mọi ô ở trạng thái chỉ đọc.\n'
          '3. (Tuỳ chọn) Người dùng bấm “Xem lịch sử” để mở rộng khối Lịch sử.\n'
          '4. Người dùng bấm Đóng để quay về danh sách.',
    phu='• Bản ghi không còn → ' + CHANGED + ', không mở cửa sổ.\n'
        '• Chưa có thay đổi nào → khối Lịch sử hiển thị “Chưa có lịch sử thay đổi”.\n'
        '• Trong khối Lịch sử: “Bộ lọc” lọc theo nhóm hành động, “Làm mới” nạp lại, “Thu gọn” đóng '
        'khối.',
    dacbiet=None)
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', modal='Xem loại giảm giá', shot=shot('05-xem.png'),
         shot_caption='Cửa sổ Xem loại giảm giá')
d.p('Khối Lịch sử trong cửa sổ Xem:')
d.layout(menu=MENU + ' => Xem chi tiết => Xem lịch sử', shot=shot('05b-lich-su.png'),
         shot_caption='Khối Lịch sử thay đổi đã mở rộng')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xem loại giảm giá”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Mã loại giảm giá', 'Textbox', 'Read-only', 'GG-YYYY-NNNNN', 'Theo dữ liệu', '–'),
    ('Tên loại giảm giá', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Trạng thái', 'Dropdown', 'Read-only', 'Hoạt động / Khóa / Chờ duyệt', 'Theo dữ liệu', '–'),
    ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn',
     'Nút “Xem lịch sử” mở rộng; mỗi dòng: nhóm hành động, người thực hiện kèm phòng ban, thời '
     'điểm, trường đổi (Mã, Tên, Trạng thái) với giá trị cũ → giá trị mới.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Không có nút Lưu.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Mã loại giảm giá', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Mở cửa sổ chi tiết ở chế độ chỉ đọc.'),
    ('Bấm “Xem lịch sử”', 'Click', 'After:\n– Mở rộng khối Lịch sử và nạp danh sách thay đổi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Xóa loại giảm giá')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xóa loại giảm giá', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-07 Xóa loại giảm giá')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa loại giảm giá',
    mota='Xóa hẳn một loại giảm giá đang Chờ duyệt, hoặc chưa được dùng trong báo giá nào.',
    tacnhan='Người quản lý danh mục loại giảm giá',
    dieukien='Người dùng có quyền Q1; loại giảm giá đang Chờ duyệt, hoặc chưa được dùng trong báo giá.',
    chinh='1. Người dùng bấm nút Xóa trên dòng.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận xóa”.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống xóa bản ghi, ghi 1 dòng lịch sử “Xóa”, thông báo “Xóa thành công” và nạp lại '
          'danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xóa.\n'
        '• Loại giảm giá đã được dùng trong báo giá → “Loại giảm giá đã được sử dụng, không thể '
        'xoá”.\n'
        '• Bản ghi đã bị xóa trước đó → ' + CHANGED + '.',
    dacbiet='Xóa là xóa hẳn, không khôi phục được. Muốn ngừng dùng loại giảm giá đã được sử dụng '
            'thì dùng chức năng Khóa.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', modal='Xác nhận xóa', shot=shot('06-xoa.png'),
         shot_caption='Hộp thoại xác nhận xóa loại giảm giá')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xác nhận xóa”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu', '“Bạn có chắc muốn xóa loại giảm giá \'<tên>\'?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
], required=False, scope=False)
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa trên dòng', 'Click',
     'Before:\n– Dùng được khi loại giảm giá đang Chờ duyệt hoặc chưa được dùng trong báo giá.\n'
     'After:\n– Hiện hộp thoại xác nhận.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Đã được dùng trong báo giá (và không phải Chờ duyệt) → “Loại giảm giá đã được sử '
     'dụng, không thể xoá” và dừng xử lý.\n'
     'After:\n– Xóa bản ghi, ghi 1 dòng lịch sử “Xóa” kèm dữ liệu lúc xóa.\n'
     '– Thông báo “Xóa thành công”, nạp lại danh sách.'),
    ('Bấm Hủy / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Xóa nhiều loại giảm giá')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Xóa nhiều loại giảm giá', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-08 Xóa nhiều loại giảm giá')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa nhiều loại giảm giá',
    mota='Chọn nhiều loại giảm giá bằng ô tích đầu dòng rồi xóa cùng lúc.',
    tacnhan='Người quản lý danh mục loại giảm giá',
    dieukien='Người dùng có quyền Q1; đã tích chọn ít nhất 1 loại giảm giá đủ điều kiện xóa.',
    chinh='1. Người dùng tích ô chọn ở các dòng cần xóa (hoặc ô tích ở tiêu đề để chọn cả trang).\n'
          '2. Hệ thống hiện “Đã chọn n dòng” cùng nút Xóa, Bỏ chọn.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống hiện hộp thoại “Xác nhận xóa nhiều”.\n'
          '5. Người dùng bấm Xóa.\n'
          '6. Hệ thống xóa các bản ghi đã chọn, ghi lịch sử “Xóa” cho từng bản ghi, thông báo “Xóa '
          'thành công n loại giảm giá”, bỏ chọn và nạp lại danh sách.',
    phu='• Bấm Bỏ chọn → bỏ tích tất cả.\n'
        '• Dòng không đủ điều kiện xóa → ô tích bị khóa.\n'
        '• Có loại giảm giá đã được sử dụng trong danh sách chọn → hệ thống vẫn xóa các loại hợp lệ '
        'và báo “Không thể xoá: <tên 1>, <tên 2> (đã được sử dụng)”.\n'
        '• Lỗi khác → “Lỗi khi xóa nhiều loại giảm giá”.',
    dacbiet='Lựa chọn chỉ giữ các dòng còn hiển thị trên trang hiện tại.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa nhiều', modal='Xác nhận xóa nhiều', shot=shot('06b-chon-nhieu.png'),
         shot_caption='Thanh thao tác khi đã chọn dòng')
d.figure(shot('06c-xoa-nhieu.png'), 'Hộp thoại xác nhận xóa nhiều loại giảm giá', width_in=6.2)
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tích đầu dòng / tiêu đề', 'Checkbox', 'Enable / Disable', 'Theo dữ liệu',
     'Chỉ tích được loại giảm giá đủ điều kiện xóa.'),
    ('Dòng “Đã chọn n dòng”', 'Label', 'Hiển thị', 'Ẩn khi chưa chọn', '–'),
    ('Nút Xóa (đỏ)', 'Button', 'Enable', 'Ẩn khi chưa chọn', 'Mở hộp thoại xác nhận xóa nhiều.'),
    ('Nút Bỏ chọn', 'Button', 'Enable', 'Ẩn khi chưa chọn', 'Bỏ tích tất cả.'),
    ('Tiêu đề “Xác nhận xóa nhiều”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu', '“Bạn có chắc muốn xóa n loại giảm giá đã chọn?”'),
    ('Nút Xóa / Hủy trong hộp thoại', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa / đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xóa trên thanh thao tác', 'Click',
     'Before:\n– Chưa chọn dòng nào → “Vui lòng chọn ít nhất một loại giảm giá để xóa”.\n'
     'After:\n– Hiện hộp thoại xác nhận xóa nhiều.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Bỏ qua các loại giảm giá đã được sử dụng, ghi nhận tên để báo lại.\n'
     'After:\n– Xóa các bản ghi hợp lệ; ghi lịch sử “Xóa” từng bản ghi.\n'
     '– Không có bản bị bỏ qua → “Xóa thành công n loại giảm giá”; có → “Không thể xoá: <danh '
     'sách tên> (đã được sử dụng)”.\n'
     '– Bỏ chọn, nạp lại danh sách.'),
    ('Bấm Bỏ chọn', 'Click', 'After:\n– Bỏ tích tất cả các dòng.'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Duyệt loại giảm giá')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Duyệt loại giảm giá', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-09 Duyệt loại giảm giá')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Duyệt loại giảm giá',
    mota='Duyệt một loại giảm giá đang Chờ duyệt (tạo nhanh trong báo giá) để đưa vào danh mục dùng '
         'chung.',
    tacnhan='Người quản lý danh mục loại giảm giá',
    dieukien='Người dùng có quyền Q1; loại giảm giá đang Chờ duyệt.',
    chinh='1. Người dùng bấm nút Duyệt trên dòng loại giảm giá Chờ duyệt.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận duyệt”.\n'
          '3. Người dùng bấm Duyệt.\n'
          '4. Hệ thống chuyển trạng thái sang Hoạt động, bỏ gắn với báo giá tạo ra nó, ghi 1 dòng '
          'lịch sử “Thay đổi trạng thái”.\n'
          '5. Thông báo “Duyệt thành công”, nạp lại danh sách.',
    phu='• Bấm Hủy → không duyệt.\n'
        '• Loại giảm giá không còn Chờ duyệt → “Chỉ có thể duyệt loại giảm giá đang Chờ duyệt”.\n'
        '• Lỗi khác → “Duyệt thất bại”.',
    dacbiet='Sau khi duyệt, loại giảm giá áp dụng được cho tất cả báo giá.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Duyệt', modal='Xác nhận duyệt', shot=shot('09-duyet.png'),
         shot_caption='Hộp thoại xác nhận duyệt loại giảm giá')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Duyệt (dấu tích) trên dòng', 'Icon Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Chỉ hiện với loại giảm giá Chờ duyệt.'),
    ('Tiêu đề “Xác nhận duyệt”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Duyệt loại giảm giá \'<tên>\'? Sau khi duyệt sẽ chuyển sang trạng thái Hoạt động và áp dụng '
     'cho tất cả báo giá.”'),
    ('Nút Duyệt', 'Button', 'Enable', 'Hiển thị', 'Thực hiện duyệt.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Duyệt trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện với loại giảm giá Chờ duyệt.\n'
     'After:\n– Hiện hộp thoại xác nhận duyệt.'),
    ('Bấm Duyệt trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Không còn Chờ duyệt → “Chỉ có thể duyệt loại giảm giá đang Chờ duyệt” và dừng xử lý.\n'
     'After:\n– Chuyển sang Hoạt động, bỏ gắn báo giá; ghi người cập nhật và 1 dòng lịch sử.\n'
     '– Thông báo “Duyệt thành công”, nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.10
d.h3('2.10 Khóa / Mở khóa loại giảm giá')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Khóa / Mở khóa loại giảm giá', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-10 Khóa / Mở khóa loại giảm giá')
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khóa / Mở khóa loại giảm giá',
    mota='Chuyển trạng thái loại giảm giá giữa Hoạt động và Khóa bằng nút Khoá / Mở khoá ở cột Hành '
         'động.',
    tacnhan='Người quản lý danh mục loại giảm giá',
    dieukien='Người dùng có quyền Q1; loại giảm giá không ở trạng thái Chờ duyệt.',
    chinh='1. Người dùng bấm Khoá (hoặc Mở khoá) trên dòng.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khóa” (hoặc “Xác nhận mở khóa”).\n'
          '3. Người dùng bấm Khóa (hoặc Mở khóa).\n'
          '4. Hệ thống đổi trạng thái, ghi 1 dòng lịch sử nhóm “Thay đổi trạng thái”, thông báo '
          '“Khóa thành công” / “Mở khóa thành công”, nạp lại danh sách.',
    phu='• Loại giảm giá đang Chờ duyệt → nút Khoá bị ẩn; gọi khóa trực tiếp bị từ chối “Không thể '
        'khoá loại giảm giá đang Chờ duyệt”.\n'
        '• Loại giảm giá đã được dùng trong báo giá VẪN khóa được.\n'
        '• Bấm Hủy → không đổi trạng thái.',
    dacbiet='Loại giảm giá đang Khóa không Sửa được cho tới khi Mở khóa và không hiện ở danh sách '
            'chọn loại giảm giá trong báo giá.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Khoá / Mở khoá', modal='Xác nhận khóa / Xác nhận mở khóa',
         shot=shot('08-khoa.png'), shot_caption='Hộp thoại xác nhận khóa loại giảm giá')
d.figure(shot('08b-mo-khoa.png'), 'Hộp thoại xác nhận mở khóa loại giảm giá', width_in=6.2)
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Khoá / Mở khoá', 'Icon Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Đang Hoạt động: Khoá (ổ khóa đóng). Đang Khóa: Mở khoá (ổ khóa mở). Ẩn khi Chờ duyệt.'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khóa” / “Xác nhận mở khóa”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn khóa (mở khóa) loại giảm giá \'<tên>\'?”'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Khoá / Mở khoá trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện khi loại giảm giá không Chờ duyệt.\n'
     'After:\n– Hiện hộp thoại xác nhận tương ứng.'),
    ('Bấm Khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Đang Chờ duyệt → “Không thể khoá loại giảm giá đang Chờ duyệt” và dừng xử lý.\n'
     'After:\n– Đổi trạng thái sang Khóa, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng thái”.\n'
     '– Thông báo “Khóa thành công”, nạp lại danh sách.'),
    ('Bấm Mở khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Đổi trạng thái sang Hoạt động, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng '
     'thái”.\n– Thông báo “Mở khóa thành công”, nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.11
d.h3('2.11 Xuất Excel')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Xuất Excel danh sách loại giảm giá', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-11 Xuất Excel')
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của '
           'Danh mục loại giảm giá.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách loại giảm giá',
    mota='Người dùng chọn các trường cần xuất rồi tải về tệp danh_muc_loai_giam_gia.xlsx gồm TẤT CẢ '
         'loại giảm giá khớp bộ lọc đang áp dụng (không chỉ trang đang xem).',
    tacnhan='Người quản lý danh mục loại giảm giá',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng (tuỳ chọn) đặt bộ lọc trên màn danh sách.\n'
          '2. Bấm Xuất Excel.\n'
          '3. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiện trên bảng.\n'
          '4. Người dùng tích / bỏ tích, kéo để đổi thứ tự trường, rồi bấm Xuất file.\n'
          '5. Hệ thống dựng tệp theo bộ lọc, trình duyệt tải tệp về, thông báo “Xuất Excel thành công”.',
    phu='• Bấm “Chọn tất cả” / “Bỏ chọn hết” để chọn nhanh.\n'
        '• Lỗi khi dựng tệp → thông báo “Lỗi khi xuất Excel”.',
    dacbiet='Nút Xuất Excel bị khóa trong lúc đang xuất để tránh bấm lặp.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất file',
         shot=shot('10-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất file')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường xuất', 'Table/Grid', 'Enable', '7 trường', 'Có (≥ 1)',
     'Tích sẵn các cột đang hiện trên bảng',
     'Mã loại giảm giá, Tên loại giảm giá, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật, '
     'Trạng thái. Kéo ⠿ để đổi thứ tự.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn nhanh.'),
    ('Dòng “Đang chọn x/7 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Tải tệp danh_muc_loai_giam_gia.xlsx.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiện trên bảng.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Áp đúng bộ lọc đang dùng trên màn, lấy tất cả dòng khớp.\n'
     'After:\n– Tải tệp danh_muc_loai_giam_gia.xlsx với các trường đã chọn theo thứ tự đã sắp.\n'
     '– Thông báo “Xuất Excel thành công”.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Danh mục loại giảm giá; không lặp lại các '
           'quy tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Mã loại giảm giá tự sinh', [
        '– Mã = “GG-” + năm hiện tại + “-” + số thứ tự 5 chữ số (VD GG-2026-00008).',
        '– Người dùng không nhập, không sửa được mã.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-02', 'Tên loại giảm giá', '– Bắt buộc, tối đa 255 ký tự.', ['Tạo mới', 'Chỉnh sửa']),
    ('BR-03', 'Vòng đời trạng thái', [
        '– Tạo từ màn danh mục: Hoạt động (mặc định) hoặc Khóa.',
        '– Tạo nhanh trong báo giá: Chờ duyệt, chỉ báo giá đó chọn được.',
        '– Chờ duyệt → Hoạt động chỉ qua thao tác Duyệt; không Khóa / Mở khóa, không đổi trạng '
        'thái trong form Sửa.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Duyệt', 'Khóa / Mở khóa']),
    ('BR-04', 'Điều kiện Sửa', [
        '– Sửa được loại giảm giá Hoạt động hoặc Chờ duyệt; loại đang Khóa phải Mở khóa trước.',
    ], ['Chỉnh sửa', 'Danh sách']),
    ('BR-05', 'Điều kiện Xóa', [
        '– Loại Chờ duyệt: luôn xóa được.',
        '– Loại Hoạt động / Khóa: chỉ xóa được khi chưa được dùng trong dòng giảm giá của báo giá nào.',
        '– Xóa nhiều: bỏ qua các loại đã được sử dụng và báo tên các loại đó.',
    ], ['Xóa', 'Xóa nhiều']),
    ('BR-06', 'Khóa / Mở khóa', [
        '– Khóa được loại Hoạt động kể cả khi đã được dùng trong báo giá.',
        '– Mở khóa đưa về Hoạt động; chọn Khóa trong form Sửa tương đương thao tác Khóa.',
    ], ['Khóa / Mở khóa', 'Chỉnh sửa']),
    ('BR-07', 'Danh sách chọn ở báo giá', [
        '– Báo giá chỉ chọn được loại giảm giá Hoạt động, cộng các loại Chờ duyệt do chính báo giá '
        'đó tạo.',
    ], 'Màn báo giá (nghiệp vụ)'),
    ('BR-08', 'Ghi lịch sử thay đổi', [
        '– Ghi lại mọi lần Tạo mới, Thay đổi thông tin, Thay đổi trạng thái (Khóa, Mở khóa, Duyệt), '
        'Xóa (kể cả Xóa nhiều).',
        '– Lịch sử xem trong cửa sổ Xem chi tiết.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xóa', 'Xóa nhiều', 'Duyệt', 'Khóa / Mở khóa', 'Xem chi tiết']),
    ('BR-09', 'Xuất theo bộ lọc, chọn trường', [
        '– Xuất tất cả dòng khớp bộ lọc đang áp dụng, không giới hạn theo trang.',
        '– Người dùng chọn trường và thứ tự trường; mặc định là các cột đang hiện trên bảng.',
    ], 'Xuất Excel'),
])

d.save(update_fields=False)

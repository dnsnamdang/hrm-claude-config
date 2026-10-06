# -*- coding: utf-8 -*-
"""Sinh "SRS - Danh mục loại tài liệu.docx" theo code nhánh gop_db — form 2026-09-24.

Chạy:  python3 .plans/gop-db/srs-danh-muc-du-an/loai-tai-lieu/gen_srs.py
Ảnh chụp thật (Playwright 1440x900, bản gop_db cổng 3002): loai-tai-lieu_shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/attachment-type/{index.vue, AddAttachmentTypeModal.vue}
      components/subsystem-menu/sale-hub.js (menu: Danh mục > Danh mục chung) · sale.js (gate quyền)
      components/subsystems.js (phân hệ "Bán hàng")
  BE  Modules/Assign/Routes/api.php (nhóm /assign/attachment-types)
      Http/Requests/AttachmentType/AttachmentTypeRequest.php
      Http/Controllers/Api/V1/AttachmentTypeController.php · Services/AttachmentTypeService.php
      Entities/AttachmentType/AttachmentType.php · Transformers/AttachmentTypeResource
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 1042, 1043)
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


OUT = os.path.join(HERE, 'SRS - Danh mục loại tài liệu.docx')
SHOTS = os.path.join(HERE, 'loai-tai-lieu_shots')
MENU = 'Phân hệ Bán hàng => Danh mục => Danh mục chung => Loại tài liệu'

A_QL = 'Người quản lý danh mục loại tài liệu (Q1)'
A_XEM = 'Người xem danh mục loại tài liệu (Q2)'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')
CHANGED = '“Dữ liệu đã được thay đổi, vui lòng tải lại trang”'


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/attachment-type',
           full_url='https://<host-hrm>/assign/attachment-type', img_prefix='loaitailieu_gopdb_')

# Icon cho từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện
# (ô phân hệ, mục "Danh mục" ở sidebar, tiêu đề nhóm "Danh mục chung" trong panel, mục màn, nút).
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ Bán hàng': 'phanhe', 'Danh mục': 'danhmuc', 'Danh mục chung': 'nhom',
    'Loại tài liệu': 'man',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidatboloc', 'Tuỳ chỉnh cột': 'tuychinhcot',
    'Tạo mới': 'taomoi', 'Sửa': 'sua', 'Xem chi tiết': 'xem', 'Xóa': 'xoa',
    'Hành động khác': 'khac', 'Khóa': 'khoa', 'Mở khóa': 'mokhoa', 'Lịch sử': 'lichsu',
    'Xuất Excel': 'xuat',
}.items()})

d.title_block('Danh mục loại tài liệu')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục loại tài liệu thuộc phân hệ Bán '
    'hàng (nhóm Danh mục chung), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ quy tắc sinh mã loại tài liệu tự động.',
    'Làm rõ ràng buộc giữa Loại tài liệu với các tệp tài liệu đính kèm đang được phân loại theo nó: '
    'khi nào được sửa, xóa, khóa.',
    'Làm rõ quy tắc xuất dữ liệu ra tệp Excel.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Loại tài liệu', 'Phân loại tệp tài liệu đính kèm (VD: Bản vẽ thiết kế, Thuyết minh, Bomlist, '
     'Hình ảnh, Video, Catalog, Báo giá…). Được chọn khi đính kèm tài liệu ở các màn nghiệp vụ.'),
    ('Mã loại tài liệu', 'Mã do hệ thống tự sinh khi tạo mới, dạng LTL.NNN (tiền tố “LTL.” + số thứ '
     'tự tăng dần). Người dùng không nhập, không sửa được.'),
    ('Loại tài liệu đã sử dụng', 'Loại tài liệu đã được gắn cho ít nhất 1 tệp tài liệu đính kèm.'),
    ('Trạng thái Khóa', 'Loại tài liệu ngừng sử dụng: không được chọn ở màn nghiệp vụ, không sửa '
     'được. Khóa KHÔNG xóa dữ liệu, có thể Mở khóa lại.'),
    ('Menu “…” (Hành động khác)', 'Nút ở cột Hành động chứa các thao tác còn lại của dòng khi dòng '
     'có nhiều hơn 3 thao tác.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý danh mục loại tài liệu',
     'Xem danh sách, xem chi tiết, xem lịch sử; hiện nút Tạo mới; hiện các thao tác Sửa, Xóa, Khóa '
     '/ Mở khóa trên dòng; được Xuất Excel.'),
    ('Q2', 'Xem danh mục loại tài liệu',
     'Xem danh sách, tìm kiếm, xem chi tiết và xem lịch sử. Không được thay đổi dữ liệu.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn hình không phân quyền theo cấp dữ liệu (công ty / phòng ban / bộ phận): người có quyền '
    'xem được toàn bộ loại tài liệu của hệ thống. Mục menu Loại tài liệu chỉ hiện với người có Q1 '
    'hoặc Q2.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách loại tài liệu', '✅', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '❌'),
    ('FR-04 Tạo mới loại tài liệu', '✅', '❌', '❌'),
    ('FR-05 Chỉnh sửa loại tài liệu', '✅', '❌', '❌'),
    ('FR-06 Xem chi tiết loại tài liệu', '✅', '✅', '❌'),
    ('FR-07 Xóa loại tài liệu', '✅', '❌', '❌'),
    ('FR-08 Khóa / Mở khóa loại tài liệu', '✅', '❌', '❌'),
    ('FR-09 Xem lịch sử thay đổi', '✅', '✅', '❌'),
    ('FR-10 Xuất Excel', '✅', '❌', '❌'),
], widths=[3.0, 0.8, 0.8, 1.4])

# ================================================================ PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_QL, [0, 1, 2, 3, 4, 5]),
     (A_XEM, [0])],
    [('FR-01', 'Xem danh sách loại tài liệu', 'view'),
     ('FR-04', 'Tạo mới loại tài liệu', 'crud'),
     ('FR-05', 'Chỉnh sửa loại tài liệu', 'crud'),
     ('FR-07', 'Xóa loại tài liệu', 'action'),
     ('FR-08', 'Khóa / Mở khóa loại tài liệu', 'action'),
     ('FR-10', 'Xuất Excel danh sách loại tài liệu', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết loại tài liệu', 'view', 'extend', [0], None),
     ('FR-09', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Danh mục loại tài liệu')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách loại tài liệu')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Danh mục loại tài liệu tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách loại tài liệu',
    mota='Hiển thị toàn bộ loại tài liệu kèm mã, tên, mô tả, người tạo / cập nhật, trạng thái và '
         'các thao tác trên từng dòng.',
    tacnhan='Người quản lý / người xem danh mục loại tài liệu; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng vào menu Phân hệ Bán hàng → Danh mục → Danh mục chung → Loại tài liệu.\n'
          '2. Hệ thống nạp trang 1, 10 dòng/trang, bản ghi mới tạo lên đầu.\n'
          '3. Bảng hiển thị đủ các cột (mặc định hiện hết cột), dòng “Hiển thị a–b / N” và thanh '
          'phân trang.',
    phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm Mã loại tài liệu → mở cửa sổ Xem chi tiết (FR-06).\n'
        '• Bấm tiêu đề cột Mã, Tên, Ngày tạo, Ngày cập nhật → sắp xếp theo cột đó, bấm lại để đảo '
        'chiều.\n'
        '• Rời màn rồi quay lại trong vòng 10 phút → bộ lọc đang dùng được khôi phục.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách loại tài liệu lúc mới truy cập')
d.figure(shot('07-menu-khac.png'), 'Cột Trạng thái, cột Hành động và menu “…” của một dòng',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Danh sách loại tài liệu”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1', 'Mở form Tạo mới (FR-04).'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Chọn trường xuất file (FR-10).'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cố định bên trái khi cuộn ngang; không tắt được.'),
    ('Cột Mã loại tài liệu', 'Table/Grid', 'Read-only', 'LTL.NNN', 'Theo dữ liệu',
     'Cố định bên trái, không tắt được, sắp xếp được. Là liên kết mở cửa sổ Xem chi tiết.'),
    ('Cột Tên loại tài liệu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Sắp xếp được; tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Mô tả', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Người tạo hiển thị tên nhân viên. Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu',
     'Hoạt động màu xanh, Khóa màu đỏ.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu',
     'Không tắt được. Thứ tự Sửa, Xóa, Khóa / Mở khóa, Lịch sử. Dòng có tối đa 3 thao tác thì '
     'hiện hết; nhiều hơn thì hiện 2 nút đầu, phần còn lại gom vào nút “…”. Thao tác không dùng '
     'được thì ẨN hẳn.'),
    ('Nút Sửa (bút)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và loại tài liệu đang Hoạt động (FR-05).'),
    ('Nút Xóa (thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và loại tài liệu chưa được gắn cho tệp tài liệu nào (FR-07).'),
    ('Nút / mục Khóa / Mở khóa', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Hiện với Q1. Đang Hoạt động hiện Khóa, đang Khóa hiện Mở khóa (FR-08).'),
    ('Nút / mục Lịch sử', 'Button', 'Enable', '–', 'Hiển thị', 'Mọi người vào được màn đều thấy (FR-09).'),
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả', 'N là tổng số bản ghi khớp bộ lọc.'),
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
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'During:\n– Khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu có).\n'
     '– Nạp cấu hình cột đã lưu của người dùng.\n'
     'After:\n– Hiển thị trang 1, 10 dòng, bản ghi mới tạo lên đầu.'),
    ('Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click',
     'After:\n– Sắp xếp theo cột đó, bấm lại để đảo chiều; quay về trang 1.'),
    ('Bấm số trang / đổi Số dòng/trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu; đổi số dòng/trang thì quay về trang 1.'),
    ('Bấm Mã loại tài liệu', 'Click', 'After:\n– Mở cửa sổ Xem chi tiết loại tài liệu (FR-06).'),
    ('Bấm nút “…” ở cột Hành động', 'Click',
     'After:\n– Mở menu các thao tác còn lại của dòng (Khóa / Mở khóa, Lịch sử).'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Danh mục '
           'loại tài liệu tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc loại tài liệu',
    mota='Tìm nhanh theo mã, tên, mô tả hoặc tên người tạo; lọc nâng cao theo người tạo, người cập '
         'nhật, khoảng ngày tạo, khoảng ngày cập nhật.',
    tacnhan='Người quản lý / người xem danh mục loại tài liệu; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách loại tài liệu.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
          '3. Chọn giá trị ở ô Người tạo, Người cập nhật, Ngày tạo, Ngày cập nhật: chọn xong hệ thống '
          'tự lọc lại ngay.\n'
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
     'Placeholder “Tìm theo mã loại tài liệu, tên loại tài liệu, mô tả, người tạo”. Tìm gần đúng. '
     'Áp dụng khi bấm Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao (nhãn đổi thành “Ẩn tìm kiếm nâng cao” khi đang mở).'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', 'Lọc đúng theo người tạo.'),
    ('Người cập nhật', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc đúng theo người cập nhật cuối.'),
    ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống',
     'Một ô gồm 2 ngày Từ → Đến, tính cả 2 đầu mút.'),
    ('Ngày cập nhật', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống',
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
    dieukien='Đang ở màn danh sách loại tài liệu.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ với danh sách trường / cột, đánh dấu những mục đang hiện.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho người dùng, đóng cửa sổ và vẽ lại khối lọc / bảng.',
    phu='• Bấm “Khôi phục mặc định” → trả về bộ trường lọc mặc định của màn.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Cột STT, Mã loại tài liệu và Hành động luôn hiện, không bỏ tích được (hiển thị xám + ổ '
        'khóa).',
    dacbiet='Mặc định màn hiện TẤT CẢ cột; người dùng tự tắt bớt nếu thấy bảng quá rộng.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột', modal='Cài đặt bộ lọc và Tuỳ chỉnh cột',
         shot=shot('02b-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('02c-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột — cột khóa hiển thị xám', width_in=6.2)
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường lọc', 'Table/Grid', 'Enable', '4 trường', 'Không', 'Theo cấu hình đã lưu',
     'Người tạo, Người cập nhật, Ngày tạo, Ngày cập nhật. Mỗi dòng: số thứ tự, biểu tượng kéo ⠿, '
     'ô tích, tên trường.'),
    ('Nút Lưu (Cài đặt bộ lọc)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình trường lọc.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về bộ trường lọc mặc định.'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '10 cột', 'Không', 'Theo cấu hình đã lưu',
     'Cột STT, Mã loại tài liệu, Hành động bị khóa (luôn hiện).'),
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
FORM_ROWS = [
    ('Tên loại tài liệu', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Không trùng với loại tài liệu khác. Placeholder “VD: Biên bản họp”.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động',
     'Không có nút xóa chọn — luôn có giá trị.'),
    ('Mô tả', 'Textarea', 'Enable', '0–2.000 ký tự', 'Không', 'Trống',
     'Placeholder “Mô tả ngắn (dùng trong dự án / hồ sơ / tài liệu hệ thống)”.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ kèm biểu tượng cảnh báo ngay dưới ô bị lỗi.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
]
SAVE_DURING = (
    '– Tên loại tài liệu trống → “Bắt buộc phải nhập”.\n'
    '– Tên quá 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”\n'
    '– Tên trùng loại tài liệu khác → “Đã tồn tại trên hệ thống”.\n'
    '– Mô tả quá 2.000 ký tự → “Vui lòng nhập tối đa 2000 ký tự.”\n'
    '– Nếu có lỗi validate → thông báo “Bạn chưa nhập đầy đủ thông tin” và không thực hiện bước After.')

d.h3('2.4 Tạo mới loại tài liệu')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới loại tài liệu', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-04 Tạo mới loại tài liệu')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới loại tài liệu',
    mota='Thêm một loại tài liệu mới vào danh mục; mã do hệ thống tự sinh.',
    tacnhan='Người quản lý danh mục loại tài liệu',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở cửa sổ “Tạo mới loại tài liệu” (không có ô Mã), Trạng thái mặc định Hoạt '
          'động.\n'
          '3. Người dùng nhập Tên loại tài liệu, Mô tả (nếu có), chọn Trạng thái.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống kiểm tra dữ liệu, sinh mã LTL.NNN, ghi bản ghi mới và ghi 1 dòng lịch sử “Tạo '
          'mới”.\n'
          '6. Thông báo “Thêm mới thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Bấm “Lưu & Tiếp tục” → lưu xong giữ cửa sổ mở, xóa trắng form để nhập bản ghi tiếp.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu đã nhập.\n'
        '• Lỗi khác → thông báo “Thao tác thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Nút Lưu và Lưu & Tiếp tục bị khóa trong lúc đang xử lý để tránh tạo trùng. Tên và mô '
            'tả được bỏ khoảng trắng đầu cuối trước khi lưu.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', modal='Tạo mới loại tài liệu', shot=shot('03-tao-moi.png'),
         shot_caption='Cửa sổ Tạo mới loại tài liệu')
d.figure(shot('03b-tao-moi-loi.png'), 'Cửa sổ Tạo mới khi bấm Lưu mà chưa nhập tên', width_in=6.2)
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([('Tiêu đề “Tạo mới loại tài liệu”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–')]
           + FORM_ROWS[:-1] + [
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu rồi đóng cửa sổ.'),
    ('Nút Lưu & Tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Lưu rồi xóa trắng form để nhập tiếp. Chỉ có ở Tạo mới.'),
    FORM_ROWS[-1],
])
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'Before:\n– Nút chỉ hiển thị khi có quyền Q1.\n'
     'After:\n– Mở cửa sổ với form trống, Trạng thái = Hoạt động.'),
    ('Bấm Lưu / Lưu & Tiếp tục', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING + '\n'
     'After:\n– Sinh mã LTL.NNN (số tiếp theo sau số lớn nhất đang có), ghi bản ghi mới; ghi người '
     'tạo, thời điểm tạo.\n'
     '– Ghi 1 dòng lịch sử “Tạo mới”.\n'
     '– Thông báo “Thêm mới thành công”, nạp lại danh sách.\n'
     '– Lưu: đóng cửa sổ. Lưu & Tiếp tục: giữ cửa sổ, xóa trắng form.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, không lưu dữ liệu đang nhập.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Chỉnh sửa loại tài liệu')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa loại tài liệu', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-05 Chỉnh sửa loại tài liệu')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa). '
           'Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa loại tài liệu',
    mota='Cập nhật tên, trạng thái, mô tả của một loại tài liệu đang Hoạt động. Mã không sửa được.',
    tacnhan='Người quản lý danh mục loại tài liệu',
    dieukien='Người dùng có quyền Q1; loại tài liệu đang ở trạng thái Hoạt động.',
    chinh='1. Người dùng bấm nút Sửa trên dòng loại tài liệu.\n'
          '2. Hệ thống kiểm tra lại trạng thái hiện tại của bản ghi rồi mở cửa sổ “Sửa loại tài '
          'liệu” với dữ liệu hiện tại (Mã hiển thị chỉ đọc).\n'
          '3. Người dùng sửa thông tin và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu, cập nhật và ghi 1 dòng lịch sử các trường đã đổi '
          '(giá trị cũ → giá trị mới).\n'
          '5. Thông báo “Cập nhật thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Loại tài liệu đang Khóa → nút Sửa bị ẩn.\n'
        '• Bản ghi vừa bị người khác khóa / xóa → ' + CHANGED + ', nạp lại danh sách, không mở '
        'cửa sổ (hoặc không lưu).\n'
        '• Chọn Trạng thái = Khóa trong form → khi lưu, loại tài liệu chuyển sang Khóa và ghi thêm '
        '1 dòng lịch sử “Thay đổi trạng thái”.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới ô, thông báo “Bạn chưa nhập đầy đủ thông tin”.',
    dacbiet='Tên loại tài liệu mới sẽ hiển thị ở mọi tệp tài liệu đang gắn loại này.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', modal='Sửa loại tài liệu', shot=shot('04-sua.png'),
         shot_caption='Cửa sổ Sửa loại tài liệu')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Sửa loại tài liệu”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Mã', 'Label', 'Read-only', 'LTL.NNN', '–', 'Theo dữ liệu', 'Hiển thị dạng nhãn, không sửa được.'),
    ('Tên loại tài liệu', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo dữ liệu', 'Như Tạo mới.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Theo dữ liệu', '–'),
    ('Mô tả', 'Textarea', 'Enable', '0–2.000 ký tự', 'Không', 'Theo dữ liệu', '–'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Không có nút Lưu & Tiếp tục.'),
    FORM_ROWS[-2], FORM_ROWS[-1],
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và loại tài liệu đang Hoạt động.\n'
     'During:\n– Hỏi lại trạng thái hiện tại của bản ghi.\n'
     '– Bản ghi không còn hoặc đã Khóa → ' + CHANGED + ', nạp lại danh sách, không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ Sửa với dữ liệu hiện tại.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Loại tài liệu đã bị Khóa → ' + CHANGED + ', đóng cửa sổ, nạp lại danh sách.\n'
     'During:\n' + SAVE_DURING + '\n'
     'After:\n– Cập nhật bản ghi; ghi người cập nhật, thời điểm cập nhật.\n'
     '– Ghi 1 dòng lịch sử các trường đã đổi (Tên, Mô tả); đổi Trạng thái ghi thêm dòng “Thay '
     'đổi trạng thái”.\n'
     '– Thông báo “Cập nhật thành công”, đóng cửa sổ, nạp lại danh sách.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xem chi tiết loại tài liệu')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết loại tài liệu',
    mota='Xem toàn bộ thông tin của một loại tài liệu ở chế độ chỉ đọc, kèm khối Lịch sử thay đổi.',
    tacnhan='Người quản lý / người xem danh mục loại tài liệu',
    dieukien='Người dùng có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng bấm vào Mã loại tài liệu trên bảng.\n'
          '2. Hệ thống mở cửa sổ “Xem chi tiết loại tài liệu”, mọi ô ở trạng thái chỉ đọc.\n'
          '3. (Tuỳ chọn) Người dùng bấm “Xem lịch sử” để mở rộng khối Lịch sử.\n'
          '4. Người dùng bấm Đóng để quay về danh sách.',
    phu='• Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.',
    dacbiet=None)
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', modal='Xem chi tiết loại tài liệu', shot=shot('05-xem.png'),
         shot_caption='Cửa sổ Xem chi tiết loại tài liệu')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xem chi tiết loại tài liệu”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Mã', 'Label', 'Read-only', 'LTL.NNN', 'Theo dữ liệu', '–'),
    ('Tên loại tài liệu', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', 'Không hiện dấu *.'),
    ('Trạng thái', 'Dropdown', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu', '–'),
    ('Mô tả', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở danh sách thay đổi của bản ghi (như FR-09).'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Không có nút Lưu.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Mã loại tài liệu', 'Click',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'After:\n– Mở cửa sổ chi tiết ở chế độ chỉ đọc.'),
    ('Bấm “Xem lịch sử”', 'Click', 'After:\n– Mở rộng khối Lịch sử và nạp danh sách thay đổi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Xóa loại tài liệu')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xóa loại tài liệu', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-07 Xóa loại tài liệu')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa loại tài liệu',
    mota='Xóa hẳn một loại tài liệu chưa được gắn cho tệp tài liệu nào.',
    tacnhan='Người quản lý danh mục loại tài liệu',
    dieukien='Người dùng có quyền Q1; loại tài liệu chưa được gắn cho tệp tài liệu nào.',
    chinh='1. Người dùng bấm nút Xóa trên dòng loại tài liệu.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận xóa”.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống xóa bản ghi, ghi 1 dòng lịch sử “Xóa”, thông báo “Xóa thành công” và nạp lại '
          'danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xóa.\n'
        '• Loại tài liệu đã được sử dụng → nút Xóa bị ẩn; nếu phát sinh tệp gắn loại này trong lúc '
        'xác nhận → “Không thể xóa loại tài liệu đã được sử dụng”.\n'
        '• Lỗi khác → “Xóa thất bại, vui lòng thử lại”.',
    dacbiet='Xóa là xóa hẳn, không khôi phục được. Muốn ngừng dùng loại tài liệu đã được sử dụng '
            'thì dùng chức năng Khóa.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', modal='Xác nhận xóa', shot=shot('06-xoa.png'),
         shot_caption='Hộp thoại xác nhận xóa loại tài liệu')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xác nhận xóa”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu', '“Bạn có chắc muốn xóa loại tài liệu \'<tên>\'?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
], required=False, scope=False)
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và loại tài liệu chưa được sử dụng.\n'
     'After:\n– Hiện hộp thoại xác nhận.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Đã có tệp tài liệu gắn loại này → “Không thể xóa loại tài liệu đã được sử dụng” '
     'và dừng xử lý.\n'
     'After:\n– Xóa bản ghi, ghi 1 dòng lịch sử “Xóa” kèm dữ liệu lúc xóa.\n'
     '– Thông báo “Xóa thành công”, đóng hộp thoại, nạp lại danh sách.'),
    ('Bấm Hủy / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Khóa / Mở khóa loại tài liệu')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Khóa / Mở khóa loại tài liệu', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-08 Khóa / Mở khóa loại tài liệu')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khóa / Mở khóa loại tài liệu',
    mota='Chuyển trạng thái loại tài liệu giữa Hoạt động và Khóa bằng thao tác Khóa / Mở khóa ở cột '
         'Hành động (nút trực tiếp hoặc trong menu “…”).',
    tacnhan='Người quản lý danh mục loại tài liệu',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm Khóa (hoặc Mở khóa) trên dòng loại tài liệu.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khóa” (hoặc “Xác nhận mở khóa”).\n'
          '3. Người dùng bấm Khóa (hoặc Mở khóa).\n'
          '4. Hệ thống đổi trạng thái, ghi 1 dòng lịch sử nhóm “Thay đổi trạng thái”, thông báo '
          '“Khóa thành công” / “Mở khóa thành công”, nạp lại danh sách.',
    phu='• Loại tài liệu đã được sử dụng VẪN khóa được; các tệp cũ giữ nguyên loại tài liệu.\n'
        '• Loại tài liệu đã bị người khác khóa trong lúc xác nhận → hệ thống từ chối khóa lần hai và '
        'báo lỗi.\n'
        '• Bấm Hủy → không đổi trạng thái.',
    dacbiet='Loại tài liệu đang Khóa không Sửa được cho tới khi Mở khóa và không hiện ở danh sách '
            'chọn loại tài liệu khi đính kèm tệp.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Khóa / Mở khóa',
         modal='Xác nhận khóa / Xác nhận mở khóa',
         shot=shot('07b-khoa.png'), shot_caption='Hộp thoại xác nhận khóa loại tài liệu')
d.figure(shot('07c-mo-khoa.png'), 'Hộp thoại xác nhận mở khóa loại tài liệu', width_in=6.2)
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút / mục Khóa / Mở khóa', 'Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Đang Hoạt động: Khóa (ổ khóa đóng). Đang Khóa: Mở khóa (ổ khóa mở).'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khóa” / “Xác nhận mở khóa”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn khóa (mở khóa) loại tài liệu \'<tên>\'?”'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Khóa / Mở khóa', 'Click',
     'Before:\n– Chỉ hiện với Q1.\n'
     'After:\n– Hiện hộp thoại xác nhận tương ứng.'),
    ('Bấm Khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Loại tài liệu không còn Hoạt động → hệ thống báo lỗi và dừng xử lý.\n'
     'After:\n– Đổi trạng thái sang Khóa, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng thái”.\n'
     '– Thông báo “Khóa thành công”, nạp lại danh sách.'),
    ('Bấm Mở khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Đổi trạng thái sang Hoạt động, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng '
     'thái”.\n– Thông báo “Mở khóa thành công”, nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Xem lịch sử thay đổi')
d.p('2.9.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung thông tin riêng của Danh mục '
           'loại tài liệu.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của loại tài liệu',
    mota='Xem các lần Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Xóa của một loại tài liệu: '
         'ai làm, lúc nào, trường nào đổi từ giá trị cũ sang giá trị mới.',
    tacnhan='Người quản lý / người xem danh mục loại tài liệu',
    dieukien='Người dùng vào được màn danh sách (Q1 hoặc Q2). Lịch sử không gắn quyền riêng.',
    chinh='1. Người dùng bấm nút Lịch sử trên dòng (hoặc bấm “…” rồi chọn Lịch sử).\n'
          '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <mã> - <tên>” và nạp danh sách thay đổi.\n'
          '3. Người dùng bấm Đóng.',
    phu='• Chưa có thay đổi nào → hiển thị “Chưa có lịch sử thay đổi”.\n'
        '• Bấm “Bộ lọc” trong cửa sổ để lọc theo nhóm hành động.',
    dacbiet=None)
d.p('2.9.2 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Lịch sử', modal='Lịch sử thay đổi',
         shot=shot('08-lich-su.png'), shot_caption='Cửa sổ Lịch sử thay đổi của loại tài liệu')
d.p('2.9.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Lịch sử thay đổi: <mã> - <tên>”.'),
    ('Danh sách thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi lần thay đổi: nhóm hành động, người thực hiện kèm phòng ban, thời điểm, các trường đổi '
     '(Mã, Tên, Mô tả, Trạng thái) với giá trị cũ → giá trị mới.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Lọc theo nhóm hành động.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thay đổi”.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)
d.p('2.9.4 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Lịch sử', 'Click', 'After:\n– Mở cửa sổ và nạp danh sách thay đổi của bản ghi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.10
d.h3('2.10 Xuất Excel')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xuất Excel danh sách loại tài liệu', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-10 Xuất Excel')
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của '
           'Danh mục loại tài liệu.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách loại tài liệu',
    mota='Người dùng chọn các trường cần xuất rồi tải về tệp danh_sach_loai_tai_lieu.xlsx gồm TẤT '
         'CẢ loại tài liệu khớp bộ lọc đang áp dụng (không chỉ trang đang xem).',
    tacnhan='Người quản lý danh mục loại tài liệu',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng (tuỳ chọn) đặt bộ lọc trên màn danh sách.\n'
          '2. Bấm Xuất Excel.\n'
          '3. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiện trên bảng.\n'
          '4. Người dùng tích / bỏ tích, kéo để đổi thứ tự trường, rồi bấm Xuất file.\n'
          '5. Hệ thống dựng tệp theo bộ lọc, trình duyệt tải tệp về, thông báo “Xuất Excel thành công”.',
    phu='• Bấm “Chọn tất cả” / “Bỏ chọn hết” để chọn nhanh.\n'
        '• Lỗi khi dựng tệp → thông báo “Lỗi khi xuất Excel”.',
    dacbiet='Nút Xuất Excel bị khóa trong lúc đang xuất để tránh bấm lặp.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất file',
         shot=shot('10-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất file')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường xuất', 'Table/Grid', 'Enable', '8 trường', 'Có (≥ 1)',
     'Tích sẵn các cột đang hiện trên bảng',
     'Mã loại tài liệu, Tên loại tài liệu, Mô tả, Người tạo, Ngày tạo, Người cập nhật, Ngày cập '
     'nhật, Trạng thái. Kéo ⠿ để đổi thứ tự.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn nhanh.'),
    ('Dòng “Đang chọn x/8 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Tải tệp danh_sach_loai_tai_lieu.xlsx.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiện trên bảng.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Áp đúng bộ lọc đang dùng trên màn, lấy tất cả dòng khớp.\n'
     'After:\n– Tải tệp danh_sach_loai_tai_lieu.xlsx với các trường đã chọn theo thứ tự đã sắp.\n'
     '– Thông báo “Xuất Excel thành công”.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Danh mục loại tài liệu; không lặp lại các '
           'quy tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Mã loại tài liệu tự sinh', [
        '– Mã = “LTL.” + số thứ tự 3 chữ số, lấy số lớn nhất đang có cộng 1 (VD LTL.009, LTL.010).',
        '– Người dùng không nhập, không sửa được mã; mã hiển thị chỉ đọc ở màn Sửa / Xem.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xem chi tiết']),
    ('BR-02', 'Tên và mô tả', [
        '– Tên bắt buộc, tối đa 255 ký tự, không trùng với loại tài liệu khác.',
        '– Mô tả tối đa 2.000 ký tự.',
        '– Tên và mô tả được bỏ khoảng trắng đầu cuối trước khi lưu.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-03', 'Chỉ sửa loại tài liệu đang Hoạt động',
     '– Loại tài liệu đang Khóa không sửa được (nút Sửa bị ẩn, máy chủ cũng từ chối); phải Mở khóa '
     'trước.',
     ['Chỉnh sửa', 'Danh sách']),
    ('BR-04', 'Điều kiện Xóa', [
        '– Chỉ xóa được loại tài liệu chưa được gắn cho tệp tài liệu nào.',
        '– Xóa là xóa hẳn; loại tài liệu đã được sử dụng thì dùng Khóa thay cho Xóa.',
    ], 'Xóa'),
    ('BR-05', 'Khóa / Mở khóa', [
        '– Khóa được loại tài liệu đang Hoạt động, kể cả khi đã được sử dụng.',
        '– Mở khóa luôn được phép.',
        '– Chọn Trạng thái = Khóa trong form Sửa tương đương thao tác Khóa.',
    ], ['Khóa / Mở khóa', 'Chỉnh sửa']),
    ('BR-06', 'Loại tài liệu đã khóa ở màn nghiệp vụ',
     '– Danh sách chọn loại tài liệu khi đính kèm tệp chỉ gồm loại đang Hoạt động.',
     'Màn đính kèm tài liệu'),
    ('BR-07', 'Thao tác không dùng được thì ẩn', [
        '– Tạo mới, Sửa, Xóa, Khóa / Mở khóa chỉ hiện với người có Q1 VÀ đủ điều kiện nghiệp vụ.',
        '– Không hiển thị nút xám.',
    ], 'Danh sách'),
    ('BR-08', 'Ghi lịch sử thay đổi', [
        '– Ghi lại mọi lần Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Xóa.',
        '– Cập nhật chỉ ghi các trường thực sự đổi: Mã, Tên, Mô tả, Trạng thái.',
        '– Ai vào được màn đều xem được lịch sử.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xóa', 'Khóa / Mở khóa', 'Xem lịch sử']),
    ('BR-09', 'Xuất theo bộ lọc, chọn trường', [
        '– Xuất tất cả dòng khớp bộ lọc đang áp dụng, không giới hạn theo trang.',
        '– Người dùng chọn trường và thứ tự trường; mặc định là các cột đang hiện trên bảng.',
    ], 'Xuất Excel'),
])

d.save(update_fields=False)

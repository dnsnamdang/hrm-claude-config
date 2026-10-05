# -*- coding: utf-8 -*-
"""Sinh "SRS - Danh mục lĩnh vực kinh doanh khách hàng.docx" theo code nhánh gop_db — form 2026-09-24.

Chạy:  python3 .plans/gop-db/srs-danh-muc-du-an/linh-vuc-kinh-doanh-kh/gen_srs.py
Ảnh chụp thật (Playwright 1440x900, bản gop_db cổng 3002): linh-vuc-kinh-doanh-kh_shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/customer-scopes/{index.vue, AddScopeModal.vue}
      components/subsystem-menu/master-data.js (menu "Đối tác") · components/subsystems.js (phân hệ)
      utils/mixins/lockedCatalogOptionsMixin.js (loại hình đã khoá 🔒)
  BE  Modules/Assign/Routes/api.php (nhóm /assign/customer-scopes)
      Http/Requests/CustomerScope/CustomerScopeRequest.php
      Http/Controllers/Api/V1/CustomerScopeController.php · Services/CustomerScopeService.php
      Entities/CustomerScope/CustomerScope.php (bảng customer_scopes, pivot customer_scope_group_members)
      Transformers/CustomerScopeResource/* · app/Http/Middleware/CheckImportRowLimit.php
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 996, 1006)
Màn cha: .plans/gop-db/srs-danh-muc-du-an/loai-hinh-hoat-dong-kh/gen_srs.py
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

# Khi save(update_fields=False) (không cho Word mở lại file), python-docx `relate_to()` GỘP các
# hyperlink trùng URL vào 1 relationship -> selfcheck đếm thiếu liên kết "Quy tắc chung". Word khi
# lưu lại thì tách mỗi link 1 relationship; ở đây làm y như vậy mà KHÔNG sửa thư viện dùng chung.
_orig_relate_to = None


def _relate_to_unique(part, target, reltype, is_external=False):
    if is_external and reltype.endswith('/hyperlink'):
        return part.rels.add_relationship(reltype, target, part.rels._next_rId, is_external=True).rId
    return _orig_relate_to(part, target, reltype, is_external)


def _patch_hyperlink_rels():
    global _orig_relate_to
    from docx.opc.part import Part
    if _orig_relate_to is None:
        _orig_relate_to = Part.relate_to
        Part.relate_to = _relate_to_unique


_patch_hyperlink_rels()

TEN = 'Danh mục lĩnh vực kinh doanh khách hàng'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
SHOTS = os.path.join(HERE, 'linh-vuc-kinh-doanh-kh_shots')
MENU = 'Phân hệ Danh mục => Đối tác => Lĩnh vực kinh doanh KH'

A_QL = 'Người quản lý danh mục lĩnh vực kinh doanh KH (Q1)'
A_XEM = 'Người xem danh mục lĩnh vực kinh doanh KH (Q2)'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')
CHANGED = '“Dữ liệu đã thay đổi, vui lòng tải lại”'


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/customer-scopes',
           full_url='https://<host-hrm>/assign/customer-scopes', img_prefix='lvkdkh_gopdb_')

# Icon từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện (Playwright clip).
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ Danh mục': 'phanhe', 'Đối tác': 'doitac', 'Lĩnh vực kinh doanh KH': 'menuitem',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidatboloc', 'Tuỳ chỉnh cột': 'tuychinhcot',
    'Tạo mới': 'taomoi', 'Sửa': 'sua', 'Xem chi tiết': 'xem', 'Xóa': 'xoa',
    'Hành động khác': 'khac', 'Khóa': 'khoa', 'Mở khóa': 'mokhoa', 'Lịch sử': 'lichsu',
    'Import Excel': 'import', 'Xuất Excel': 'xuat',
}.items()})

d.title_block(TEN)
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục lĩnh vực kinh doanh khách hàng '
    'thuộc phân hệ Danh mục dùng chung (nhóm Đối tác), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ quan hệ con – cha giữa Lĩnh vực kinh doanh khách hàng (danh mục con) với Loại hình '
    'hoạt động khách hàng (danh mục cha): chọn loại hình, loại hình đã khóa, ảnh hưởng khi Khóa '
    'lĩnh vực.',
    'Làm rõ điều kiện hiện các thao tác Sửa, Xóa, Khóa, Mở khóa trên từng dòng.',
    'Làm rõ quy tắc nhập dữ liệu hàng loạt và xuất dữ liệu ra tệp Excel.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Lĩnh vực kinh doanh khách hàng', 'Lĩnh vực hoạt động cụ thể của khách hàng (vd: Thực phẩm, '
     'Đại học, Đơn vị kinh doanh điện). Được chọn trên hồ sơ khách hàng. Là danh mục CON.'),
    ('Loại hình hoạt động khách hàng', 'Danh mục CHA. Một lĩnh vực thuộc MỘT hoặc NHIỀU loại hình '
     '(quan hệ nhiều – nhiều).'),
    ('Mã lĩnh vực kinh doanh KH', 'Mã định danh dạng LVKDKH.XXXX: tiền tố “LVKDKH.” cố định + 4 ký '
     'tự do người dùng nhập. Không trùng trong toàn hệ thống.'),
    ('Trạng thái Khóa', 'Lĩnh vực ngừng sử dụng: không chọn được ở các màn nghiệp vụ, không sửa '
     'được. Khóa KHÔNG xóa dữ liệu, có thể Mở khóa lại.'),
    ('🔒 (loại hình đã khóa)', 'Loại hình đang gắn với lĩnh vực nhưng nay đã bị khóa: vẫn hiển thị '
     'đúng tên kèm biểu tượng 🔒 và được giữ nguyên khi lưu.'),
    ('Menu “…” (Hành động khác)', 'Nút ở cột Hành động. Mỗi dòng hiện tối đa 3 nút; khi có hơn 3 '
     'thao tác thì giữ 2 nút đầu, phần còn lại (Khóa / Mở khóa, Lịch sử) gom vào menu “…”.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý danh mục lĩnh vực khách hàng',
     'Xem danh sách, xem chi tiết, xem lịch sử; hiện nút Tạo mới, Import Excel; hiện các thao tác '
     'Sửa, Xóa, Khóa / Mở khóa trên dòng; được Xuất Excel.'),
    ('Q2', 'Xem danh mục lĩnh vực khách hàng',
     'Xem danh sách, tìm kiếm, xem chi tiết và xem lịch sử. Không hiện thao tác thay đổi dữ liệu; '
     'không xuất được Excel.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn hình không phân quyền theo cấp dữ liệu (công ty / phòng ban / bộ phận): người có quyền '
    'xem được toàn bộ lĩnh vực của hệ thống. Mục menu chỉ hiện với người có Q1 hoặc Q2.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách lĩnh vực kinh doanh KH', '✅', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '❌'),
    ('FR-04 Tạo mới lĩnh vực kinh doanh KH', '✅', '❌', '❌'),
    ('FR-05 Chỉnh sửa lĩnh vực kinh doanh KH', '✅', '❌', '❌'),
    ('FR-06 Xem chi tiết lĩnh vực kinh doanh KH', '✅', '✅', '❌'),
    ('FR-07 Xóa lĩnh vực kinh doanh KH', '✅', '❌', '❌'),
    ('FR-08 Khóa / Mở khóa lĩnh vực kinh doanh KH', '✅', '❌', '❌'),
    ('FR-09 Xem lịch sử thay đổi', '✅', '✅', '❌'),
    ('FR-10 Import Excel', '✅', '❌', '❌'),
    ('FR-11 Xuất Excel', '✅', '❌', '❌'),
], widths=[3.0, 0.8, 0.8, 1.4])

# ================================================================ PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_QL, [0, 1, 2, 3, 4, 5, 6]),
     (A_XEM, [0])],
    [('FR-01', 'Xem danh sách lĩnh vực kinh doanh KH', 'view'),
     ('FR-04', 'Tạo mới lĩnh vực kinh doanh KH', 'crud'),
     ('FR-05', 'Chỉnh sửa lĩnh vực kinh doanh KH', 'crud'),
     ('FR-07', 'Xóa lĩnh vực kinh doanh KH', 'action'),
     ('FR-08', 'Khóa / Mở khóa lĩnh vực', 'action'),
     ('FR-10', 'Import Excel lĩnh vực', 'io'),
     ('FR-11', 'Xuất Excel danh sách lĩnh vực', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết lĩnh vực', 'view', 'extend', [0], None),
     ('FR-09', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Danh mục lĩnh vực kinh doanh khách hàng')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách lĩnh vực kinh doanh khách hàng')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Danh mục lĩnh vực kinh doanh khách hàng tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Xem danh sách lĩnh vực kinh doanh khách hàng',
    mota='Hiển thị toàn bộ lĩnh vực kinh doanh khách hàng kèm các loại hình hoạt động khách hàng mà '
         'lĩnh vực thuộc về, mô tả, người tạo / cập nhật, trạng thái và các thao tác trên từng dòng.',
    tacnhan='Người quản lý / người xem danh mục lĩnh vực kinh doanh KH; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng vào menu Phân hệ Danh mục → Đối tác → Lĩnh vực kinh doanh KH.\n'
          '2. Hệ thống nạp trang 1, 10 dòng/trang, bản ghi mới tạo lên đầu.\n'
          '3. Bảng hiển thị đủ các cột (mặc định hiện hết cột), dòng “Hiển thị a–b / N” và thanh '
          'phân trang.',
    phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm Mã lĩnh vực → mở cửa sổ Xem chi tiết (FR-06).\n'
        '• Bấm tiêu đề cột Mã, Tên, Ngày tạo, Ngày cập nhật → sắp xếp theo cột đó, bấm lại để '
        'đảo chiều.\n'
        '• Rời màn rồi quay lại trong vòng 10 phút → bộ lọc đang dùng được khôi phục.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách lĩnh vực kinh doanh khách hàng lúc mới truy cập')
d.figure(shot('07-menu-khac.png'), 'Cột Trạng thái, cột Hành động và menu “…” của một dòng',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Danh sách lĩnh vực kinh doanh khách hàng”', 'Label', 'Hiển thị', '–',
     'Hiển thị', '–'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1', 'Mở form Tạo mới (FR-04).'),
    ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1',
     'Mở cửa sổ Import (FR-10).'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Chọn trường xuất file (FR-11). Chỉ Q1 xuất được tệp.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cố định bên trái khi cuộn ngang; không tắt được.'),
    ('Cột Mã lĩnh vực kinh doanh KH', 'Table/Grid', 'Read-only', 'LVKDKH.XXXX', 'Theo dữ liệu',
     'Cố định bên trái, không tắt được, sắp xếp được. Là liên kết mở cửa sổ Xem chi tiết.'),
    ('Cột Lĩnh vực kinh doanh khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tên lĩnh vực. Sắp xếp được; tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Loại hình hoạt động khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tên các loại hình mà lĩnh vực thuộc về, ngăn cách bằng dấu phẩy; tối đa 2 dòng.'),
    ('Cột Mô tả', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Người tạo hiển thị họ tên. Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu',
     'Hoạt động màu xanh, Khóa màu đỏ.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu',
     'Không tắt được. Thứ tự: Sửa, Xóa, Khóa / Mở khóa, Lịch sử; hiện tối đa 3 nút, dư thì giữ 2 '
     'nút đầu và gom phần còn lại vào nút “…”. Thao tác không dùng được thì ẨN hẳn.'),
    ('Nút Sửa (bút)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và lĩnh vực đang Hoạt động (FR-05).'),
    ('Nút Xóa (thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Hiện với Q1 ở mọi dòng (FR-07).'),
    ('Nút Khóa / Mở khóa (ổ khóa)', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1. Đang Hoạt động: Khóa; đang Khóa: Mở khóa (FR-08).'),
    ('Nút Lịch sử', 'Button', 'Enable', '–', 'Hiển thị', 'Mọi người vào được màn đều thấy (FR-09).'),
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số bản ghi khớp bộ lọc.'),
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
    ('Bấm Mã lĩnh vực', 'Click', 'After:\n– Mở cửa sổ Xem chi tiết lĩnh vực (FR-06).'),
    ('Bấm nút “…” ở cột Hành động', 'Click',
     'After:\n– Mở menu các thao tác còn lại của dòng (Khóa / Mở khóa, Lịch sử).'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Danh mục '
           'lĩnh vực kinh doanh khách hàng tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc lĩnh vực kinh doanh khách hàng',
    mota='Tìm nhanh theo mã, tên lĩnh vực hoặc tên người tạo; lọc nâng cao theo mã, tên, trạng '
         'thái, người tạo, người cập nhật, khoảng ngày cập nhật.',
    tacnhan='Người quản lý / người xem danh mục lĩnh vực kinh doanh KH; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách lĩnh vực kinh doanh khách hàng.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
          '3. Ô chọn (Trạng thái, Người tạo, Người cập nhật, Ngày cập nhật): chọn xong hệ thống tự '
          'lọc lại ngay.\n'
          '4. Ô gõ tay (Mã, Tên): hệ thống chỉ lọc khi bấm Enter hoặc nút Tìm kiếm.\n'
          '5. Bảng hiển thị kết quả từ trang 1.',
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
     'Placeholder “Tìm theo mã lĩnh vực, tên lĩnh vực, người tạo”. Tìm gần đúng theo Mã, Tên hoặc '
     'họ tên Người tạo. Áp dụng khi bấm Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao (nhãn đổi thành “Ẩn tìm kiếm nâng cao” khi đang mở).'),
    ('Mã lĩnh vực kinh doanh KH', 'Textbox', 'Enable', '–', 'Không', 'Trống', 'Lọc gần đúng theo mã.'),
    ('Lĩnh vực kinh doanh khách hàng', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Lọc gần đúng theo tên lĩnh vực.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Trống', '–'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', 'Lọc đúng theo người tạo.'),
    ('Người cập nhật', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc đúng theo người cập nhật cuối.'),
    ('Ngày cập nhật', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống',
     'Một ô gồm 2 ngày Từ → Đến, tính cả 2 đầu mút.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm / Enter', 'Click / Keypress',
     'Before:\n– Lấy từ khóa, bỏ khoảng trắng đầu cuối.\n'
     'After:\n– Lọc theo toàn bộ điều kiện; hiển thị trang 1.'),
    ('Đổi giá trị một ô chọn trong khối lọc', 'Change',
     'After:\n– Tự lọc lại ngay theo toàn bộ điều kiện đang chọn.'),
    ('Gõ vào ô Mã / Tên trong khối lọc', 'Keypress',
     'After:\n– Chưa lọc; chờ Enter hoặc nút Tìm kiếm.'),
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
    dieukien='Đang ở màn danh sách lĩnh vực kinh doanh khách hàng.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ với danh sách trường / cột, đánh dấu những mục đang hiện.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ≡ để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho người dùng, đóng cửa sổ và vẽ lại khối lọc / bảng.',
    phu='• Bấm “Khôi phục mặc định” (Cài đặt bộ lọc) → trả về bộ trường lọc mặc định của màn.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Cột STT, Mã lĩnh vực kinh doanh KH và Hành động luôn hiện, không bỏ tích được (hiển thị '
        'xám + ổ khóa).',
    dacbiet='Mặc định màn hiện TẤT CẢ cột; người dùng tự tắt bớt nếu thấy bảng quá rộng.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột', modal='Cài đặt bộ lọc và Tuỳ chỉnh cột',
         shot=shot('02b-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('02c-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột — cột khóa hiển thị xám', width_in=6.2)
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường lọc', 'Table/Grid', 'Enable', '6 trường', 'Không', 'Theo cấu hình đã lưu',
     'Mỗi mục: số thứ tự, ô tích, tên trường; kéo để đổi thứ tự.'),
    ('Nút Lưu (Cài đặt bộ lọc)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình trường lọc.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về bộ trường lọc mặc định.'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '11 cột', 'Không', 'Theo cấu hình đã lưu',
     'Cột STT, Mã lĩnh vực kinh doanh KH, Hành động bị khóa (luôn hiện).'),
    ('Nút Lưu (Tuỳ chỉnh cột)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình cột.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
])
d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Kéo biểu tượng ≡', 'Drag', 'After:\n– Đổi thứ tự trường / cột trong danh sách.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Lưu cấu hình theo người dùng đang đăng nhập; đóng cửa sổ; vẽ lại khối lọc / bảng.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Đưa danh sách về cấu hình mặc định của màn.'),
])

# ---------------------------------------------------------------- 2.4
SAVE_DURING = (
    '– Mã trống → “Bắt buộc phải nhập”.\n'
    '– Mã không đủ 4 ký tự sau “LVKDKH.” → “Vui lòng nhập 4 ký tự”.\n'
    '– Mã có ký tự không hợp lệ → “Chỉ cho phép: Chữ cái không dấu(A-Z, a-z), chữ số (0-9) và dấu '
    'gạch dưới (_).”\n'
    '– Mã đã tồn tại → “Đã tồn tại trên hệ thống”.\n'
    '– Tên lĩnh vực trống → “Bắt buộc phải nhập”; trùng → “Đã tồn tại trên hệ thống”; quá 255 ký '
    'tự → “Vui lòng nhập tối đa 255 ký tự.”; chứa , hoặc : → “không được chứa ký tự dấu phẩy (,) và '
    'dấu hai chấm (:)”.\n'
    '– Chưa chọn Loại hình hoạt động khách hàng → “Vui lòng chọn loại hình hoạt động khách hàng”; '
    'loại hình không còn → “Loại hình hoạt động khách hàng không tồn tại”; chọn thêm một loại hình '
    'đã khóa → “Loại hình hoạt động khách hàng \"<tên>\" đã bị khoá, vui lòng chọn loại hình khác”.\n'
    '– Nếu có lỗi validate → báo lỗi đỏ dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin” và '
    'không thực hiện bước After.')

FORM_GROUP = ('Loại hình hoạt động khách hàng', 'Dropdown', 'Enable',
              'Danh sách loại hình đang Hoạt động (chọn nhiều)', 'Có')

d.h3('2.4 Tạo mới lĩnh vực kinh doanh khách hàng')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới lĩnh vực kinh doanh KH', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-04 Tạo mới lĩnh vực kinh doanh khách hàng')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới lĩnh vực kinh doanh khách hàng',
    mota='Thêm một lĩnh vực kinh doanh khách hàng mới, gắn với ít nhất 1 loại hình hoạt động '
         'khách hàng.',
    tacnhan='Người quản lý danh mục lĩnh vực kinh doanh KH',
    dieukien='Người dùng có quyền Q1; có ít nhất 1 loại hình hoạt động khách hàng đang Hoạt động.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở cửa sổ “Tạo mới lĩnh vực kinh doanh khách hàng”, Trạng thái mặc định Hoạt '
          'động; nạp danh sách loại hình đang Hoạt động.\n'
          '3. Người dùng nhập 4 ký tự Mã, Tên lĩnh vực, chọn một hoặc nhiều Loại hình hoạt động '
          'khách hàng, nhập Mô tả (nếu có).\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống kiểm tra dữ liệu, ghi bản ghi mới kèm các loại hình đã chọn và ghi 1 dòng '
          'lịch sử “Tạo mới”.\n'
          '6. Thông báo “Thêm mới thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Bấm “Lưu & Tiếp tục” → lưu xong giữ cửa sổ mở, xóa trắng form để nhập bản ghi tiếp.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới từng ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu đã nhập.\n'
        '• Lỗi khác → thông báo “Thêm mới thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Nút Lưu, Lưu & Tiếp tục, Đóng bị khóa trong lúc đang xử lý để tránh tạo trùng. Toàn bộ '
            'kiểm tra dữ liệu do máy chủ thực hiện khi bấm Lưu.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', modal='Tạo mới lĩnh vực kinh doanh khách hàng',
         shot=shot('03-tao-moi.png'), shot_caption='Cửa sổ Tạo mới lĩnh vực kinh doanh khách hàng')
d.figure(shot('03b-tao-moi-loi.png'), 'Cửa sổ Tạo mới khi bấm Lưu mà chưa nhập các trường bắt buộc',
         width_in=6.2)
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Tạo mới lĩnh vực kinh doanh khách hàng”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Mã lĩnh vực kinh doanh KH', 'Textbox', 'Enable', 'LVKDKH. + 4 ký tự', 'Có',
     'Tiền tố “LVKDKH.” cố định',
     'Người dùng nhập 4 ký tự sau tiền tố: chữ không dấu, chữ số, dấu gạch dưới; hệ thống lưu chữ '
     'in hoa. Không trùng.'),
    ('Lĩnh vực kinh doanh khách hàng (Tên)', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Không trùng; không chứa dấu phẩy (,) và dấu hai chấm (:).'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Có', 'Hoạt động',
     'Không có nút xóa chọn — luôn có giá trị.'),
    FORM_GROUP + ('Trống', 'Chọn ≥ 1 loại hình; có ô tìm kiếm trong danh sách; mỗi loại hình đã chọn '
                           'là 1 thẻ, bấm × trên thẻ để bỏ.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Trống', 'Nội dung mô tả tự do.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ kèm biểu tượng cảnh báo ngay dưới ô bị lỗi.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu rồi đóng cửa sổ.'),
    ('Nút Lưu & Tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Lưu rồi xóa trắng form để nhập tiếp. Chỉ có ở Tạo mới.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
])
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'Before:\n– Nút chỉ hiển thị khi có quyền Q1.\n'
     'After:\n– Mở cửa sổ với form trống, Trạng thái = Hoạt động; nạp danh sách loại hình đang '
     'Hoạt động.'),
    ('Bấm Lưu / Lưu & Tiếp tục', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING + '\n'
     'After:\n– Ghi bản ghi mới, mã chuyển sang chữ in hoa; gắn các loại hình đã chọn; ghi người '
     'tạo, thời điểm tạo.\n'
     '– Ghi 1 dòng lịch sử “Tạo mới”.\n'
     '– Thông báo “Thêm mới thành công”, nạp lại danh sách.\n'
     '– Lưu: đóng cửa sổ. Lưu & Tiếp tục: giữ cửa sổ, xóa trắng form.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, không lưu dữ liệu đang nhập.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Chỉnh sửa lĩnh vực kinh doanh khách hàng')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa lĩnh vực kinh doanh KH', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-05 Chỉnh sửa lĩnh vực kinh doanh khách hàng')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa). '
           'Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa lĩnh vực kinh doanh khách hàng',
    mota='Cập nhật thông tin và danh sách loại hình của một lĩnh vực đang Hoạt động.',
    tacnhan='Người quản lý danh mục lĩnh vực kinh doanh KH',
    dieukien='Người dùng có quyền Q1; lĩnh vực đang ở trạng thái Hoạt động.',
    chinh='1. Người dùng bấm nút Sửa trên dòng lĩnh vực.\n'
          '2. Hệ thống mở cửa sổ “Sửa lĩnh vực kinh doanh khách hàng” với dữ liệu hiện tại.\n'
          '3. Người dùng sửa thông tin, thêm / bỏ loại hình và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu, cập nhật, thay danh sách loại hình bằng danh sách vừa chọn '
          'và ghi lịch sử các trường đã đổi (giá trị cũ → giá trị mới); đổi Trạng thái ghi thành '
          'dòng “Thay đổi trạng thái” riêng.\n'
          '5. Thông báo “Cập nhật thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Lĩnh vực đang Khóa → nút Sửa bị ẩn.\n'
        '• Loại hình đang gắn nay đã bị khóa → vẫn hiển thị đúng tên kèm 🔒 và được giữ nguyên khi '
        'lưu; bỏ đi rồi thì không chọn lại được (chỉ chọn thêm được loại hình đang Hoạt động).\n'
        '• Bản ghi đã bị xóa / khóa bởi người khác trong lúc sửa → ' + CHANGED + '.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin”.',
    dacbiet='Chọn Khóa ở ô Trạng thái rồi Lưu cũng là khóa lĩnh vực (luôn được phép). Không có nút '
            'Lưu & Tiếp tục.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', modal='Sửa lĩnh vực kinh doanh khách hàng', shot=shot('04-sua.png'),
         shot_caption='Cửa sổ Sửa lĩnh vực kinh doanh khách hàng — loại hình đã khóa hiển thị 🔒')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Sửa lĩnh vực kinh doanh khách hàng”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Mã lĩnh vực kinh doanh KH', 'Textbox', 'Enable', 'LVKDKH. + 4 ký tự', 'Có', 'Theo dữ liệu',
     'Như Tạo mới.'),
    ('Lĩnh vực kinh doanh khách hàng (Tên)', 'Textbox', 'Enable', '1–255 ký tự', 'Có',
     'Theo dữ liệu', 'Như Tạo mới.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Có', 'Theo dữ liệu', '–'),
    ('Loại hình hoạt động khách hàng', 'Dropdown', 'Enable',
     'Loại hình đang Hoạt động + loại hình đang gắn', 'Có', 'Theo dữ liệu',
     'Loại hình đang gắn đã khóa hiển thị kèm 🔒.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Theo dữ liệu', '–'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ kèm biểu tượng cảnh báo ngay dưới ô bị lỗi.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu rồi đóng cửa sổ.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và lĩnh vực đang Hoạt động.\n'
     'During:\n– Nạp chi tiết bản ghi, danh sách loại hình đang Hoạt động và các loại hình đã khóa '
     'mà lĩnh vực đang gắn.\n'
     '– Bản ghi không còn → ' + CHANGED + ', không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ Sửa với dữ liệu hiện tại.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING + '\n'
     '– Lĩnh vực không còn Hoạt động → ' + CHANGED + ' và dừng xử lý.\n'
     'After:\n– Cập nhật bản ghi và danh sách loại hình; ghi người cập nhật, thời điểm cập nhật.\n'
     '– Ghi lịch sử các trường đã đổi.\n'
     '– Thông báo “Cập nhật thành công”, đóng cửa sổ, nạp lại danh sách.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xem chi tiết lĩnh vực kinh doanh khách hàng')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết lĩnh vực kinh doanh khách hàng',
    mota='Xem toàn bộ thông tin của một lĩnh vực ở chế độ chỉ đọc, kèm các loại hình hoạt động '
         'khách hàng đang gắn và khối Lịch sử thay đổi.',
    tacnhan='Người quản lý / người xem danh mục lĩnh vực kinh doanh KH',
    dieukien='Người dùng có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng bấm vào Mã lĩnh vực trên bảng.\n'
          '2. Hệ thống mở cửa sổ “Xem chi tiết lĩnh vực kinh doanh khách hàng”, mọi ô ở trạng thái '
          'chỉ đọc.\n'
          '3. (Tuỳ chọn) Người dùng bấm “Xem lịch sử” để mở rộng khối Lịch sử.\n'
          '4. Người dùng bấm Đóng để quay về danh sách.',
    phu='• Loại hình đang gắn đã bị khóa → hiển thị đúng tên kèm 🔒.\n'
        '• Bản ghi không còn → ' + CHANGED + ', không mở cửa sổ.',
    dacbiet=None)
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', modal='Xem chi tiết lĩnh vực kinh doanh khách hàng',
         shot=shot('05-xem.png'), shot_caption='Cửa sổ Xem chi tiết lĩnh vực kinh doanh khách hàng')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xem chi tiết lĩnh vực kinh doanh khách hàng”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Mã lĩnh vực kinh doanh KH', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', 'Không hiện dấu *.'),
    ('Lĩnh vực kinh doanh khách hàng (Tên)', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Trạng thái', 'Dropdown', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu', '–'),
    ('Loại hình hoạt động khách hàng', 'Dropdown', 'Read-only', '–', 'Theo dữ liệu',
     'Các loại hình đang gắn, mỗi loại hình 1 thẻ; loại hình đã khóa kèm 🔒.'),
    ('Mô tả', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở danh sách thay đổi của bản ghi (như FR-09).'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Không có nút Lưu.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Mã lĩnh vực', 'Click',
     'Before:\n– Người dùng đang ở màn danh sách (có Q1 hoặc Q2).\n'
     'During:\n– Nạp chi tiết bản ghi kèm các loại hình đang gắn.\n'
     'After:\n– Mở cửa sổ chi tiết ở chế độ chỉ đọc.'),
    ('Bấm “Xem lịch sử”', 'Click', 'After:\n– Mở rộng khối Lịch sử và nạp danh sách thay đổi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Xóa lĩnh vực kinh doanh khách hàng')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xóa lĩnh vực kinh doanh KH', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-07 Xóa lĩnh vực kinh doanh khách hàng')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa lĩnh vực kinh doanh khách hàng',
    mota='Xóa hẳn một lĩnh vực kinh doanh khách hàng.',
    tacnhan='Người quản lý danh mục lĩnh vực kinh doanh KH',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Xóa trên dòng lĩnh vực.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận xóa”.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống ghi 1 dòng lịch sử “Xóa”, xóa bản ghi, thông báo “Xóa thành công” và nạp lại '
          'danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xóa.\n'
        '• Bản ghi đã bị xóa trước đó → ' + CHANGED + '.\n'
        '• Lỗi khác → “Xóa thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Xóa là xóa hẳn, không khôi phục được. Nút Xóa hiện với Q1 ở mọi dòng, kể cả lĩnh vực '
            'đang Khóa; hệ thống không chặn xóa theo trạng thái hay theo dữ liệu đang dùng lĩnh vực.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', modal='Xác nhận xóa', shot=shot('06-xoa.png'),
         shot_caption='Hộp thoại xác nhận xóa lĩnh vực kinh doanh khách hàng')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xác nhận xóa”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn xóa lĩnh vực kinh doanh khách hàng \'<tên>\'?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
], required=False, scope=False)
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện với Q1.\n'
     'After:\n– Hiện hộp thoại xác nhận.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Bản ghi không còn → ' + CHANGED + '.\n'
     'After:\n– Ghi 1 dòng lịch sử “Xóa” kèm dữ liệu lúc xóa, rồi xóa bản ghi.\n'
     '– Thông báo “Xóa thành công”, nạp lại danh sách.'),
    ('Bấm Hủy / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Khóa / Mở khóa lĩnh vực kinh doanh khách hàng')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Khóa / Mở khóa lĩnh vực', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-08 Khóa / Mở khóa lĩnh vực kinh doanh khách hàng')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khóa / Mở khóa lĩnh vực kinh doanh khách hàng',
    mota='Chuyển trạng thái lĩnh vực giữa Hoạt động và Khóa bằng nút Khóa / Mở khóa ở cột Hành '
         'động (nằm trong menu “…” khi dòng có hơn 3 thao tác).',
    tacnhan='Người quản lý danh mục lĩnh vực kinh doanh KH',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm Khóa (hoặc Mở khóa) trên dòng.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khóa” (hoặc “Xác nhận mở khóa”).\n'
          '3. Người dùng bấm Khóa (hoặc Mở khóa).\n'
          '4. Hệ thống đổi trạng thái, ghi 1 dòng lịch sử nhóm “Thay đổi trạng thái”, thông báo '
          '“Khóa thành công” / “Mở khóa thành công”, nạp lại danh sách.',
    phu='• Bấm Hủy → không đổi trạng thái.\n'
        '• Lỗi khác → nội dung lỗi hệ thống trả về, hoặc “Thay đổi trạng thái thất bại”.',
    dacbiet='Khóa và Mở khóa lĩnh vực luôn được phép (không phụ thuộc loại hình cha). Khóa hết các '
            'lĩnh vực trực thuộc là điều kiện để khóa được loại hình cha ở màn Loại hình hoạt động '
            'khách hàng. Lĩnh vực đang Khóa không Sửa được cho tới khi Mở khóa.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Khóa / Mở khóa',
         modal='Xác nhận khóa / Xác nhận mở khóa',
         shot=shot('07b-khoa.png'), shot_caption='Hộp thoại xác nhận khóa lĩnh vực')
d.figure(shot('07c-mo-khoa.png'), 'Hộp thoại xác nhận mở khóa lĩnh vực', width_in=6.2)
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Khóa / Mở khóa trên dòng', 'Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Đang Hoạt động: Khóa (ổ khóa đóng). Đang Khóa: Mở khóa (ổ khóa mở).'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khóa” / “Xác nhận mở khóa”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn khóa (mở khóa) lĩnh vực kinh doanh khách hàng \'<tên>\'?”'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Khóa / Mở khóa trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện với Q1.\n'
     'After:\n– Hiện hộp thoại xác nhận tương ứng.'),
    ('Bấm Khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
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
           'lĩnh vực kinh doanh khách hàng.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của lĩnh vực kinh doanh khách hàng',
    mota='Xem các lần Tạo mới, Thay đổi thông tin, Khóa / Mở khóa của một lĩnh vực: ai làm, lúc '
         'nào, trường nào đổi từ giá trị cũ sang giá trị mới.',
    tacnhan='Người quản lý / người xem danh mục lĩnh vực kinh doanh KH',
    dieukien='Người dùng vào được màn danh sách (Q1 hoặc Q2). Lịch sử không gắn quyền riêng.',
    chinh='1. Người dùng bấm nút Lịch sử trên dòng (hoặc chọn Lịch sử trong menu “…”).\n'
          '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <mã> - <tên>” và nạp danh sách thay đổi, mới '
          'nhất lên đầu.\n'
          '3. (Tuỳ chọn) Bấm “Bộ lọc” để lọc theo nhóm thay đổi.\n'
          '4. Người dùng bấm Đóng.',
    phu='• Chưa có thay đổi nào → hiển thị thông báo chưa có lịch sử.',
    dacbiet=None)
d.p('2.9.2 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Lịch sử', modal='Lịch sử thay đổi',
         shot=shot('08-lich-su.png'), shot_caption='Cửa sổ Lịch sử thay đổi của lĩnh vực')
d.p('2.9.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Lịch sử thay đổi: <mã> - <tên>”.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Lọc danh sách theo nhóm thay đổi.'),
    ('Danh sách thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dạng dòng thời gian. Mỗi mục: thời điểm, nhóm (Tạo mới / Thay đổi thông tin / Khóa / Mở '
     'khóa), người thực hiện kèm phòng ban, các trường đổi (Mã, Tên, Mô tả, Trạng thái) với giá trị '
     'cũ → giá trị mới. Thay đổi danh sách loại hình không được ghi vào lịch sử.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)
d.p('2.9.4 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Lịch sử', 'Click', 'After:\n– Mở cửa sổ và nạp danh sách thay đổi của bản ghi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.10
d.h3('2.10 Import Excel')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Import Excel lĩnh vực', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-10 Import Excel lĩnh vực kinh doanh khách hàng')
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Import file, Validate dữ liệu và Thông báo.', anchor='excel')
d.intro_table(
    ten='Import Excel lĩnh vực kinh doanh khách hàng',
    mota='Thêm mới hàng loạt lĩnh vực từ tệp Excel theo file mẫu, kèm mã các loại hình hoạt động '
         'khách hàng. Chỉ thêm mới, không cập nhật lĩnh vực đã có.',
    tacnhan='Người quản lý danh mục lĩnh vực kinh doanh KH',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm Import Excel.\n'
          '2. (Tuỳ chọn) Bấm “Tải file mẫu” để lấy tệp Mau_import_LVKH.xlsx.\n'
          '3. Bấm “Chọn file Excel”, chọn tệp đã điền dữ liệu.\n'
          '4. Bấm “Load lên bảng” để đọc tệp ra bảng xem trước.\n'
          '5. Bấm “Validate” → hệ thống kiểm tra từng dòng, đánh dấu dòng hợp lệ / lỗi kèm lý do; '
          'dòng hợp lệ bị khóa không sửa được.\n'
          '6. Nếu còn dòng lỗi: sửa trực tiếp các dòng lỗi rồi Validate lại, hoặc bấm “Bỏ dòng lỗi” '
          'để loại các dòng lỗi khỏi bảng.\n'
          '7. Khi đã Validate và không còn dòng lỗi, nút Import mới bấm được. Bấm “Import” → hệ '
          'thống ghi các dòng và gắn các loại hình theo mã, thông báo '
          '“Import thành công <n> lĩnh vực kinh doanh khách hàng”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Chưa Validate, hoặc còn dòng lỗi → nút Import bị khóa, không bấm được.\n'
        '• Mọi dòng đều lỗi → sau khi bỏ dòng lỗi bảng không còn dòng nào, nút Import vẫn khóa; '
        'không import được.\n'
        '• Bấm “Bỏ dòng lỗi” → “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”\n'
        '• Bấm “Xoá trạng thái validate” → bỏ đánh dấu, mở khóa các dòng để sửa; phải Validate lại.\n'
        '• Dữ liệu thay đổi giữa lúc Validate và Import (vd người khác vừa tạo bản ghi trùng mã): '
        'còn ghi được một phần → “Import thành công x/y lĩnh vực kinh doanh khách hàng. z lĩnh vực thất bại.”, đóng cửa sổ và nạp lại danh sách; '
        'không ghi được dòng nào → báo lỗi “Không có dữ liệu hợp lệ để import” (hoặc '
        '“Import thất bại: z/y lĩnh vực kinh doanh khách hàng không hợp lệ”), cửa sổ giữ nguyên.\n'
        '• Tệp quá 500 dòng → “Mỗi lần import tối đa 500 dòng (file đang có N dòng), vui lòng tách '
        'file và import nhiều lần.”\n'
        '• Bật “Chỉ dòng lỗi” để lọc bảng xem trước chỉ còn dòng lỗi.\n'
        '• Bấm Làm mới → xóa dữ liệu đã nạp để chọn tệp khác.',
    dacbiet='Mỗi lần import tối đa 500 dòng. Cột Mã loại hình hoạt động KH KHÔNG bắt buộc khi '
            'import (khác form Tạo mới); nhiều mã ngăn cách bằng dấu phẩy. Mỗi dòng thêm thành công '
            'đều ghi 1 dòng lịch sử “Tạo mới”.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Import Excel', modal='Import Lĩnh vực kinh doanh KH',
         shot=shot('09-import.png'), shot_caption='Cửa sổ Import Lĩnh vực kinh doanh KH')
d.figure(shot('09b-import-validate.png'), 'Bảng xem trước sau khi Validate — dòng lỗi kèm lý do',
         width_in=6.2)
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx / .xls', 'Có', 'Hiển thị', 'Chọn tệp cần import.'),
    ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải Mau_import_LVKH.xlsx.'),
    ('Nút Load lên bảng', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa chọn tệp',
     'Đọc tệp ra bảng xem trước.'),
    ('Nút Validate', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu',
     'Kiểm tra dữ liệu từng dòng.'),
    ('Nút Import', 'Button', 'Enable / Disable', '–', '–', 'Disable',
     'Chỉ bấm được khi đã Validate và không còn dòng lỗi.'),
    ('Nút Bỏ dòng lỗi', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu',
     'Loại các dòng lỗi khỏi bảng xem trước.'),
    ('Nút Xoá trạng thái validate', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu',
     'Bỏ kết quả Validate để sửa lại dữ liệu.'),
    ('Công tắc Chỉ dòng lỗi', 'Button', 'Enable', '–', '–', 'Tắt', 'Lọc bảng chỉ còn dòng lỗi.'),
    ('Cột Mã lĩnh vực kinh doanh KH', 'Textbox', 'Enable', 'LVKDKH.XXXX', 'Có', 'Theo tệp',
     '4 ký tự chữ hoặc số sau “LVKDKH.”; không trùng trong tệp và hệ thống.'),
    ('Cột Lĩnh vực kinh doanh khách hàng', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo tệp',
     'Không trùng; không chứa , và :.'),
    ('Cột Mã loại hình hoạt động KH', 'Textbox', 'Enable', 'LHHDKH.XXXX, LHHDKH.YYYY', 'Không',
     'Theo tệp', 'Nhiều mã ngăn cách dấu phẩy; mỗi mã phải tồn tại và đang Hoạt động.'),
    ('Cột Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Có', 'Theo tệp',
     'Nhận cả active / inactive.'),
    ('Cột Mô tả', 'Textarea', 'Enable', '0–1.000 ký tự', 'Không', 'Theo tệp', '–'),
    ('Dòng Tổng / hợp lệ / lỗi', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', 'Thống kê sau Validate.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không import.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa dữ liệu đã nạp.'),
])
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Validate', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Tệp quá 500 dòng → báo “Mỗi lần import tối đa 500 dòng …” và dừng xử lý.\n'
     'During (từng dòng):\n'
     '– Thiếu mã / tên / trạng thái → “Mã lĩnh vực kinh doanh KH không được để trống”, “Lĩnh vực '
     'kinh doanh khách hàng không được để trống”, “Trạng thái không được để trống”.\n'
     '– Mã loại hình không có → “Mã loại hình hoạt động KH không tồn tại: <mã>”; loại hình đã khóa '
     '→ “Loại hình hoạt động khách hàng đã bị khoá: <mã>”.\n'
     '– Mã sai định dạng → “Mã lĩnh vực kinh doanh KH phải theo định dạng LVKDKH.XXXX (4 ký tự)”.\n'
     '– Mã trùng trong tệp → “Mã lĩnh vực kinh doanh KH bị trùng lặp trong file import (dòng n)”; '
     'trùng hệ thống → “Mã lĩnh vực kinh doanh KH đã tồn tại trong hệ thống”.\n'
     '– Tên trùng trong tệp → “Lĩnh vực kinh doanh khách hàng bị trùng lặp trong file import (dòng '
     'n)”; trùng hệ thống → “Lĩnh vực kinh doanh khách hàng đã tồn tại trong hệ thống”; quá dài → '
     '“Lĩnh vực kinh doanh khách hàng vượt quá độ dài cho phép (tối đa 255 ký tự)”; chứa , hoặc : → '
     '“không được chứa ký tự dấu phẩy (,) và dấu hai chấm (:)”.\n'
     '– Trạng thái sai → “Trạng thái không hợp lệ, chỉ nhận giá trị: active hoặc inactive”.\n'
     '– Mô tả quá dài → “Mô tả vượt quá độ dài cho phép (tối đa 1000 ký tự)”.\n'
     'After:\n– Đánh dấu từng dòng hợp lệ / lỗi; thông báo “Validate thành công” hoặc “Validate xong: '
     'x hợp lệ, y không hợp lệ”.'),
    ('Bấm Import', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Nút chỉ bấm được khi đã Validate và không còn dòng lỗi.\n'
     'During:\n– Chỉ gửi các dòng hợp lệ. Máy chủ kiểm tra lại các dòng gửi lên như bước '
     'Validate.\n'
     'After:\n– Thêm mới các dòng hợp lệ, mã chuyển sang chữ in hoa, gắn các loại hình theo mã; ghi '
     'lịch sử “Tạo mới” từng dòng.\n'
     '– Tất cả thành công → “Import thành công <n> lĩnh vực kinh doanh khách hàng”, đóng cửa sổ, nạp lại danh sách.\n'
     '– Một phần (dữ liệu thay đổi giữa lúc Validate và Import) → '
     '“Import thành công x/y lĩnh vực kinh doanh khách hàng. z lĩnh vực thất bại.”, đóng cửa sổ, nạp lại danh sách.\n'
     '– Không ghi được dòng nào → báo lỗi “Không có dữ liệu hợp lệ để import” (hoặc '
     '“Import thất bại: z/y lĩnh vực kinh doanh khách hàng không hợp lệ”); cửa sổ giữ nguyên, không ghi dữ liệu.'),
    ('Bấm Bỏ dòng lỗi', 'Click',
     'Before:\n– Chưa Validate → “Hãy Validate trước rồi mới bỏ dòng lỗi.”\n'
     'After:\n– Loại các dòng lỗi khỏi bảng; thông báo “Đã bỏ x dòng lỗi. Còn lại y dòng hợp '
     'lệ.”; nút Import mở nếu còn ≥ 1 dòng.'),
    ('Bấm Tải file mẫu', 'Click', 'After:\n– Tải tệp Mau_import_LVKH.xlsx.'),
])

# ---------------------------------------------------------------- 2.11
d.h3('2.11 Xuất Excel')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Xuất Excel danh sách lĩnh vực', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-11 Xuất Excel')
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của '
           'Danh mục lĩnh vực kinh doanh khách hàng.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách lĩnh vực kinh doanh khách hàng',
    mota='Người dùng chọn các trường cần xuất rồi tải về tệp '
         'danh_sach_linh_vuc_kinh_doanh_khach_hang.xlsx gồm TẤT CẢ lĩnh vực khớp bộ lọc đang áp '
         'dụng (không chỉ trang đang xem).',
    tacnhan='Người quản lý danh mục lĩnh vực kinh doanh KH',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng (tuỳ chọn) đặt bộ lọc trên màn danh sách.\n'
          '2. Bấm Xuất Excel.\n'
          '3. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiện trên bảng.\n'
          '4. Người dùng tích / bỏ tích, kéo để đổi thứ tự trường, rồi bấm Xuất file.\n'
          '5. Hệ thống dựng tệp theo bộ lọc, trình duyệt tải tệp về, thông báo “Xuất Excel thành công”.',
    phu='• Bấm “Chọn tất cả” / “Bỏ chọn hết” để chọn nhanh.\n'
        '• Người chỉ có Q2 bấm Xuất file → hệ thống từ chối, không tải tệp.\n'
        '• Lỗi khi dựng tệp → thông báo “Lỗi khi xuất Excel”.',
    dacbiet='Nút Xuất Excel bị khóa trong lúc đang xuất để tránh bấm lặp. Tệp có tiêu đề “Danh sách '
            'lĩnh vực kinh doanh khách hàng”.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất file',
         shot=shot('10-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất file')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường xuất', 'Table/Grid', 'Enable', '9 trường', 'Có (≥ 1)',
     'Tích sẵn các cột đang hiện trên bảng',
     'Mã lĩnh vực kinh doanh KH, Lĩnh vực kinh doanh khách hàng, Loại hình hoạt động khách hàng, Mô '
     'tả, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. Kéo ≡ để đổi thứ tự.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn nhanh.'),
    ('Dòng “Đang chọn x/9 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Tải tệp danh_sach_linh_vuc_kinh_doanh_khach_hang.xlsx.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiện trên bảng.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Áp đúng bộ lọc đang dùng trên màn, lấy tất cả dòng khớp.\n'
     'After:\n– Tải tệp danh_sach_linh_vuc_kinh_doanh_khach_hang.xlsx với các trường đã chọn theo '
     'thứ tự đã sắp.\n– Thông báo “Xuất Excel thành công”.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Danh mục lĩnh vực kinh doanh khách hàng; '
           'không lặp lại các quy tắc đã có trong SRS quy tắc chung.', anchor='list',
           head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Định dạng và tính duy nhất của Mã', [
        '– Mã = tiền tố “LVKDKH.” + đúng 4 ký tự gồm chữ không dấu, chữ số, dấu gạch dưới '
        '(khi Import: chỉ chữ và số).',
        '– Hệ thống lưu mã ở dạng chữ in hoa; không trùng trong toàn hệ thống.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-02', 'Tên lĩnh vực', [
        '– Bắt buộc, tối đa 255 ký tự, không trùng.',
        '– Không chứa dấu phẩy (,) và dấu hai chấm (:).',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-03', 'Gắn Loại hình hoạt động khách hàng', [
        '– Mỗi lĩnh vực thuộc ít nhất 1 loại hình, có thể nhiều loại hình (bắt buộc ở form Tạo mới '
        '/ Sửa; tuỳ chọn khi Import).',
        '– Chỉ chọn thêm được loại hình đang Hoạt động.',
        '– Ngoại lệ: khi Sửa / Xem, loại hình đang gắn nay đã bị khóa vẫn hiển thị đúng tên (🔒) và '
        'được giữ nguyên khi lưu.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xem chi tiết', 'Import Excel']),
    ('BR-04', 'Chỉ sửa lĩnh vực đang Hoạt động',
     '– Lĩnh vực đang Khóa không sửa được (nút Sửa bị ẩn); phải Mở khóa trước.',
     ['Chỉnh sửa', 'Danh sách']),
    ('BR-05', 'Khóa / Mở khóa và ảnh hưởng tới loại hình cha', [
        '– Khóa / Mở khóa lĩnh vực luôn được phép.',
        '– Loại hình cha chỉ khóa được khi mọi lĩnh vực trực thuộc đã Khóa; vì vậy muốn khóa loại '
        'hình phải khóa hết lĩnh vực của nó trước.',
        '– Lĩnh vực đã Khóa không còn được chọn ở các màn nghiệp vụ nhưng vẫn giữ nguyên ở bản ghi '
        'đang dùng.',
    ], ['Khóa / Mở khóa', 'Chỉnh sửa']),
    ('BR-06', 'Xóa', [
        '– Người có Q1 xóa được mọi lĩnh vực; xóa là xóa hẳn, không khôi phục được.',
        '– Lĩnh vực đang được dùng thì nên Khóa thay cho Xóa.',
    ], 'Xóa'),
    ('BR-07', 'Thao tác không dùng được thì ẩn', [
        '– Sửa, Xóa, Khóa / Mở khóa chỉ hiện với người có Q1; Sửa ẩn khi lĩnh vực đang Khóa.',
        '– Không hiển thị nút xám.',
    ], 'Danh sách'),
    ('BR-08', 'Ghi lịch sử thay đổi', [
        '– Ghi lại mọi lần Tạo mới (kể cả qua Import), Thay đổi thông tin, Khóa / Mở khóa, Xóa.',
        '– Thay đổi thông tin chỉ ghi các trường thực sự đổi: Mã, Tên, Mô tả; đổi Trạng thái ghi '
        'thành dòng “Thay đổi trạng thái” riêng.',
        '– Ai vào được màn đều xem được lịch sử.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xóa', 'Khóa / Mở khóa', 'Import Excel', 'Xem lịch sử']),
    ('BR-09', 'Import chỉ thêm mới', [
        '– Mỗi lần tối đa 500 dòng.',
        '– Mã / tên đã có trong hệ thống hoặc trùng nhau trong tệp → dòng lỗi, không ghi đè.',
        '– Mã loại hình phải tồn tại và đang Hoạt động.',
        '– Chỉ các dòng hợp lệ được thêm; dòng lỗi được báo lý do cụ thể.',
    ], 'Import Excel'),
    ('BR-10', 'Xuất theo bộ lọc, chọn trường', [
        '– Chỉ người có Q1 xuất được.',
        '– Xuất tất cả dòng khớp bộ lọc đang áp dụng, không giới hạn theo trang.',
        '– Người dùng chọn trường và thứ tự trường; mặc định là các cột đang hiện trên bảng.',
    ], 'Xuất Excel'),
])

d.save(update_fields=False)

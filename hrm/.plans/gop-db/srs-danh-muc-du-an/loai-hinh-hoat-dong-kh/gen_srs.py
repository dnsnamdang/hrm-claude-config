# -*- coding: utf-8 -*-
"""Sinh "SRS - Danh mục loại hình hoạt động khách hàng.docx" theo code nhánh gop_db — form 2026-09-24.

Chạy:  python3 .plans/gop-db/srs-danh-muc-du-an/loai-hinh-hoat-dong-kh/gen_srs.py
Ảnh chụp thật (Playwright 1440x900, bản gop_db cổng 3002): loai-hinh-hoat-dong-kh_shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/customer-scope-groups/{index.vue, AddGroupModal.vue}
      components/subsystem-menu/master-data.js (menu "Đối tác") · components/subsystems.js (phân hệ)
      components/modal/CatalogHistoryModal.vue · components/V2BaseImportModal.vue (500 dòng)
  BE  Modules/Assign/Routes/api.php (nhóm /assign/customer-scope-groups)
      Http/Requests/CustomerScopeGroup/CustomerScopeGroupRequest.php
      Http/Controllers/Api/V1/CustomerScopeGroupController.php · Services/CustomerScopeGroupService.php
      Entities/CustomerScopeGroup/CustomerScopeGroup.php (bảng customer_scope_groups,
      pivot customer_scope_group_members n-n với customer_scopes)
      Transformers/CustomerScopeGroupResource/* · app/Http/Middleware/CheckImportRowLimit.php
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 1093, 1094)
Màn con: .plans/gop-db/srs-danh-muc-du-an/linh-vuc-kinh-doanh-kh/gen_srs.py
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

TEN = 'Danh mục loại hình hoạt động khách hàng'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
SHOTS = os.path.join(HERE, 'loai-hinh-hoat-dong-kh_shots')
MENU = 'Phân hệ Danh mục => Đối tác => Loại hình hoạt động kinh doanh KH'

A_QL = 'Người quản lý danh mục loại hình hoạt động KH (Q1)'
A_XEM = 'Người xem danh mục loại hình hoạt động KH (Q2)'
DT = 'loại hình hoạt động khách hàng'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')
CHANGED = '“Dữ liệu đã thay đổi, vui lòng tải lại”'


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/customer-scope-groups',
           full_url='https://<host-hrm>/assign/customer-scope-groups', img_prefix='lhhdkh_gopdb_')

# Icon từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện (Playwright clip).
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ Danh mục': 'phanhe', 'Đối tác': 'doitac',
    'Loại hình hoạt động kinh doanh KH': 'menuitem',
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
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục loại hình hoạt động khách hàng '
    'thuộc phân hệ Danh mục dùng chung (nhóm Đối tác), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ quan hệ cha – con giữa Loại hình hoạt động khách hàng (danh mục cha) với Lĩnh vực '
    'kinh doanh khách hàng (danh mục con): ràng buộc khi Khóa, Xóa và khi đổi Mã.',
    'Làm rõ điều kiện hiện các thao tác Sửa, Xóa, Khóa, Mở khóa trên từng dòng.',
    'Làm rõ quy tắc nhập dữ liệu hàng loạt và xuất dữ liệu ra tệp Excel.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Loại hình hoạt động khách hàng', 'Nhóm lớn phân loại khách hàng theo loại hình hoạt động '
     '(vd: Khai thác khoáng sản, Năng lượng, Logistic). Là danh mục CHA của Lĩnh vực kinh doanh '
     'khách hàng. Trên menu hiển thị là “Loại hình hoạt động kinh doanh KH”.'),
    ('Lĩnh vực kinh doanh khách hàng', 'Danh mục CON. Một lĩnh vực thuộc MỘT hoặc NHIỀU loại hình '
     '(quan hệ nhiều – nhiều). Được chọn trên hồ sơ khách hàng.'),
    ('Lĩnh vực trực thuộc', 'Lĩnh vực kinh doanh khách hàng đang được gắn với loại hình. Cột “Số '
     'lĩnh vực kinh doanh” đếm số lĩnh vực trực thuộc (cả đang Hoạt động lẫn đã Khóa).'),
    ('Mã loại hình hoạt động KH', 'Mã định danh dạng LHHDKH.XXXX: tiền tố “LHHDKH.” cố định + 4 ký '
     'tự do người dùng nhập. Không trùng trong toàn hệ thống.'),
    ('Trạng thái Khóa', 'Loại hình ngừng sử dụng: không chọn được cho lĩnh vực mới, không sửa '
     'được. Khóa KHÔNG xóa dữ liệu, có thể Mở khóa lại.'),
    ('Menu “…” (Hành động khác)', 'Nút ở cột Hành động. Mỗi dòng hiện tối đa 3 nút; khi có hơn 3 '
     'thao tác thì giữ 2 nút đầu, phần còn lại (Khóa / Mở khóa, Lịch sử) gom vào menu “…”.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý danh mục nhóm lĩnh vực khách hàng',
     'Xem danh sách, xem chi tiết, xem lịch sử; hiện nút Tạo mới, Import Excel; hiện các thao tác '
     'Sửa, Xóa, Khóa / Mở khóa trên dòng; được Xuất Excel.'),
    ('Q2', 'Xem danh mục nhóm lĩnh vực khách hàng',
     'Xem danh sách, tìm kiếm, xem chi tiết và xem lịch sử. Không hiện thao tác thay đổi dữ liệu; '
     'không xuất được Excel.'),
], widths=[0.8, 2.0, 3.2])
d.p('Tên quyền trong hệ thống vẫn giữ tên cũ “… nhóm lĩnh vực khách hàng” dù màn hình đã đổi tên '
    'thành “Loại hình hoạt động khách hàng”. Màn hình không phân quyền theo cấp dữ liệu (công ty / '
    'phòng ban / bộ phận): người có quyền xem được toàn bộ loại hình của hệ thống. Mục menu chỉ hiện '
    'với người có Q1 hoặc Q2.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách loại hình hoạt động KH', '✅', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '❌'),
    ('FR-04 Tạo mới loại hình hoạt động KH', '✅', '❌', '❌'),
    ('FR-05 Chỉnh sửa loại hình hoạt động KH', '✅', '❌', '❌'),
    ('FR-06 Xem chi tiết loại hình hoạt động KH', '✅', '✅', '❌'),
    ('FR-07 Xóa loại hình hoạt động KH', '✅', '❌', '❌'),
    ('FR-08 Khóa / Mở khóa loại hình hoạt động KH', '✅', '❌', '❌'),
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
    [('FR-01', 'Xem danh sách loại hình hoạt động KH', 'view'),
     ('FR-04', 'Tạo mới loại hình hoạt động KH', 'crud'),
     ('FR-05', 'Chỉnh sửa loại hình hoạt động KH', 'crud'),
     ('FR-07', 'Xóa loại hình hoạt động KH', 'action'),
     ('FR-08', 'Khóa / Mở khóa loại hình', 'action'),
     ('FR-10', 'Import Excel loại hình', 'io'),
     ('FR-11', 'Xuất Excel danh sách loại hình', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết loại hình', 'view', 'extend', [0], None),
     ('FR-09', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Danh mục loại hình hoạt động khách hàng')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách loại hình hoạt động khách hàng')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Danh mục loại hình hoạt động khách hàng tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Xem danh sách loại hình hoạt động khách hàng',
    mota='Hiển thị toàn bộ loại hình hoạt động khách hàng kèm số lĩnh vực kinh doanh trực thuộc, '
         'mô tả, người tạo / cập nhật, trạng thái và các thao tác trên từng dòng.',
    tacnhan='Người quản lý / người xem danh mục loại hình hoạt động KH; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng vào menu Phân hệ Danh mục → Đối tác → Loại hình hoạt động kinh doanh KH.\n'
          '2. Hệ thống nạp trang 1, 10 dòng/trang, bản ghi mới tạo lên đầu.\n'
          '3. Bảng hiển thị đủ các cột (mặc định hiện hết cột), dòng “Hiển thị a–b / N” và thanh '
          'phân trang.',
    phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm Mã loại hình → mở cửa sổ Xem chi tiết (FR-06).\n'
        '• Bấm tiêu đề cột Mã, Tên, Ngày tạo, Ngày cập nhật → sắp xếp theo cột đó, bấm lại để '
        'đảo chiều.\n'
        '• Rời màn rồi quay lại trong vòng 10 phút → bộ lọc đang dùng được khôi phục.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách loại hình hoạt động khách hàng lúc mới truy cập')
d.figure(shot('07-menu-khac.png'), 'Cột Trạng thái, cột Hành động và menu “…” của một dòng',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Danh sách loại hình hoạt động khách hàng”', 'Label', 'Hiển thị', '–',
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
    ('Cột Mã loại hình hoạt động KH', 'Table/Grid', 'Read-only', 'LHHDKH.XXXX', 'Theo dữ liệu',
     'Cố định bên trái, không tắt được, sắp xếp được. Là liên kết mở cửa sổ Xem chi tiết.'),
    ('Cột Tên loại hình hoạt động khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Sắp xếp được; tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Số lĩnh vực kinh doanh', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Căn phải. Số lĩnh vực kinh doanh khách hàng đang trực thuộc loại hình.'),
    ('Cột Mô tả', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Người tạo hiển thị họ tên. Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu',
     'Hoạt động màu xanh, Khóa màu đỏ. Loại hình đang Hoạt động mà chưa khóa được, rê chuột vào '
     'nhãn hiện lý do “Cần khóa hết lĩnh vực kinh doanh trực thuộc trước khi khóa loại hình này”.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu',
     'Không tắt được. Thứ tự: Sửa, Xóa, Khóa / Mở khóa, Lịch sử; hiện tối đa 3 nút, dư thì giữ 2 '
     'nút đầu và gom phần còn lại vào nút “…”. Thao tác không dùng được thì ẨN hẳn.'),
    ('Nút Sửa (bút)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và loại hình đang Hoạt động (FR-05).'),
    ('Nút Xóa (thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và loại hình chưa có lĩnh vực kinh doanh trực thuộc (FR-07).'),
    ('Nút Khóa / Mở khóa (ổ khóa)', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1. Khóa ẩn khi còn lĩnh vực trực thuộc đang Hoạt động; Mở khóa luôn hiện với '
     'loại hình đang Khóa (FR-08).'),
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
    ('Bấm Mã loại hình', 'Click', 'After:\n– Mở cửa sổ Xem chi tiết loại hình (FR-06).'),
    ('Bấm nút “…” ở cột Hành động', 'Click',
     'After:\n– Mở menu các thao tác còn lại của dòng (Khóa / Mở khóa, Lịch sử).'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Danh mục '
           'loại hình hoạt động khách hàng tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc loại hình hoạt động khách hàng',
    mota='Tìm nhanh theo mã, tên loại hình hoặc tên người tạo; lọc nâng cao theo mã, tên, trạng '
         'thái, người tạo, người cập nhật, khoảng ngày cập nhật.',
    tacnhan='Người quản lý / người xem danh mục loại hình hoạt động KH; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách loại hình hoạt động khách hàng.',
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
     'Placeholder “Tìm theo mã loại hình, tên loại hình, người tạo”. Tìm gần đúng theo Mã, Tên '
     'hoặc họ tên Người tạo. Áp dụng khi bấm Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao (nhãn đổi thành “Ẩn tìm kiếm nâng cao” khi đang mở).'),
    ('Mã loại hình hoạt động KH', 'Textbox', 'Enable', '–', 'Không', 'Trống', 'Lọc gần đúng theo mã.'),
    ('Tên loại hình hoạt động khách hàng', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Lọc gần đúng theo tên.'),
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
    dieukien='Đang ở màn danh sách loại hình hoạt động khách hàng.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ với danh sách trường / cột, đánh dấu những mục đang hiện.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ≡ để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho người dùng, đóng cửa sổ và vẽ lại khối lọc / bảng.',
    phu='• Bấm “Khôi phục mặc định” (Cài đặt bộ lọc) → trả về bộ trường lọc mặc định của màn.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Cột STT, Mã loại hình hoạt động KH và Hành động luôn hiện, không bỏ tích được (hiển thị '
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
     'Cột STT, Mã loại hình hoạt động KH, Hành động bị khóa (luôn hiện).'),
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
    '– Mã không đủ 4 ký tự sau “LHHDKH.” → “Vui lòng nhập 4 ký tự”.\n'
    '– Mã có ký tự không hợp lệ → “Chỉ cho phép: Chữ cái không dấu(A-Z, a-z), chữ số (0-9) và dấu '
    'gạch dưới (_).”\n'
    '– Mã đã tồn tại → “Đã tồn tại trên hệ thống”.\n'
    '– Tên loại hình trống → “Bắt buộc phải nhập”; trùng → “Đã tồn tại trên hệ thống”; quá 255 ký '
    'tự → “Vui lòng nhập tối đa 255 ký tự.”; chứa , hoặc : → “không được chứa ký tự dấu phẩy (,) và '
    'dấu hai chấm (:)”.\n'
    '– Nếu có lỗi validate → báo lỗi đỏ dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin” và '
    'không thực hiện bước After.')

d.h3('2.4 Tạo mới loại hình hoạt động khách hàng')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới loại hình hoạt động KH', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-04 Tạo mới loại hình hoạt động khách hàng')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới loại hình hoạt động khách hàng',
    mota='Thêm một loại hình hoạt động khách hàng mới vào danh mục.',
    tacnhan='Người quản lý danh mục loại hình hoạt động KH',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở cửa sổ “Tạo mới loại hình hoạt động khách hàng”, Trạng thái mặc định Hoạt '
          'động.\n'
          '3. Người dùng nhập 4 ký tự Mã, Tên loại hình, Mô tả (nếu có).\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống kiểm tra dữ liệu, ghi bản ghi mới và ghi 1 dòng lịch sử “Tạo mới”.\n'
          '6. Thông báo “Thêm mới thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Bấm “Lưu & Tiếp tục” → lưu xong giữ cửa sổ mở, xóa trắng form để nhập bản ghi tiếp.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới từng ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu đã nhập.\n'
        '• Lỗi khác → thông báo “Thêm mới thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Nút Lưu, Lưu & Tiếp tục, Đóng bị khóa trong lúc đang xử lý để tránh tạo trùng. Toàn bộ '
            'kiểm tra dữ liệu do máy chủ thực hiện khi bấm Lưu.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', modal='Tạo mới loại hình hoạt động khách hàng',
         shot=shot('03-tao-moi.png'), shot_caption='Cửa sổ Tạo mới loại hình hoạt động khách hàng')
d.figure(shot('03b-tao-moi-loi.png'), 'Cửa sổ Tạo mới khi bấm Lưu mà chưa nhập các trường bắt buộc',
         width_in=6.2)
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Tạo mới loại hình hoạt động khách hàng”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Mã loại hình hoạt động KH', 'Textbox', 'Enable', 'LHHDKH. + 4 ký tự', 'Có',
     'Tiền tố “LHHDKH.” cố định',
     'Người dùng nhập 4 ký tự sau tiền tố: chữ không dấu, chữ số, dấu gạch dưới; hệ thống lưu chữ '
     'in hoa. Không trùng.'),
    ('Loại hình hoạt động khách hàng (Tên)', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Không trùng; không chứa dấu phẩy (,) và dấu hai chấm (:).'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Có', 'Hoạt động',
     'Không có nút xóa chọn — luôn có giá trị.'),
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
     'After:\n– Mở cửa sổ với form trống, Trạng thái = Hoạt động.'),
    ('Bấm Lưu / Lưu & Tiếp tục', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING + '\n'
     'After:\n– Ghi bản ghi mới, mã chuyển sang chữ in hoa; ghi người tạo, thời điểm tạo.\n'
     '– Ghi 1 dòng lịch sử “Tạo mới”.\n'
     '– Thông báo “Thêm mới thành công”, nạp lại danh sách.\n'
     '– Lưu: đóng cửa sổ. Lưu & Tiếp tục: giữ cửa sổ, xóa trắng form.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, không lưu dữ liệu đang nhập.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Chỉnh sửa loại hình hoạt động khách hàng')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa loại hình hoạt động KH', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-05 Chỉnh sửa loại hình hoạt động khách hàng')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa). '
           'Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa loại hình hoạt động khách hàng',
    mota='Cập nhật thông tin của một loại hình đang Hoạt động.',
    tacnhan='Người quản lý danh mục loại hình hoạt động KH',
    dieukien='Người dùng có quyền Q1; loại hình đang ở trạng thái Hoạt động.',
    chinh='1. Người dùng bấm nút Sửa trên dòng loại hình.\n'
          '2. Hệ thống mở cửa sổ “Sửa loại hình hoạt động khách hàng” với dữ liệu hiện tại.\n'
          '3. Người dùng sửa thông tin và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu, cập nhật và ghi lịch sử các trường đã đổi (giá trị cũ → '
          'giá trị mới); đổi Trạng thái ghi thành dòng “Thay đổi trạng thái” riêng.\n'
          '5. Thông báo “Cập nhật thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Loại hình đang Khóa → nút Sửa bị ẩn.\n'
        '• Loại hình còn lĩnh vực trực thuộc đang Hoạt động → ô Trạng thái bị khóa ở “Hoạt động”.\n'
        '• Bản ghi đã bị xóa / khóa bởi người khác trong lúc sửa → ' + CHANGED + '.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin”.',
    dacbiet='Loại hình đã có lĩnh vực kinh doanh trực thuộc thì không được đổi Mã. Không có nút Lưu & '
            'Tiếp tục.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', modal='Sửa loại hình hoạt động khách hàng', shot=shot('04-sua.png'),
         shot_caption='Cửa sổ Sửa loại hình hoạt động khách hàng')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Sửa loại hình hoạt động khách hàng”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Mã loại hình hoạt động KH', 'Textbox', 'Enable', 'LHHDKH. + 4 ký tự', 'Có', 'Theo dữ liệu',
     'Như Tạo mới. Đã có lĩnh vực trực thuộc mà đổi mã → báo lỗi, không lưu.'),
    ('Loại hình hoạt động khách hàng (Tên)', 'Textbox', 'Enable', '1–255 ký tự', 'Có',
     'Theo dữ liệu', 'Như Tạo mới.'),
    ('Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Có', 'Theo dữ liệu',
     'Bị khóa khi loại hình còn lĩnh vực trực thuộc đang Hoạt động.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Theo dữ liệu', '–'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ kèm biểu tượng cảnh báo ngay dưới ô bị lỗi.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu rồi đóng cửa sổ.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và loại hình đang Hoạt động.\n'
     'During:\n– Nạp chi tiết bản ghi.\n'
     '– Bản ghi không còn → ' + CHANGED + ', không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ Sửa với dữ liệu hiện tại.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING.replace(
         '– Nếu có lỗi validate',
         '– Đổi mã khi đã có lĩnh vực trực thuộc → “Không thể sửa mã khi đã có dữ liệu phát sinh '
         'liên quan.”\n– Nếu có lỗi validate') + '\n'
     '– Loại hình không còn Hoạt động, hoặc chọn Khóa khi còn lĩnh vực trực thuộc đang Hoạt động '
     '→ ' + CHANGED + ' và dừng xử lý.\n'
     'After:\n– Cập nhật bản ghi; ghi người cập nhật, thời điểm cập nhật.\n'
     '– Ghi lịch sử các trường đã đổi.\n'
     '– Thông báo “Cập nhật thành công”, đóng cửa sổ, nạp lại danh sách.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xem chi tiết loại hình hoạt động khách hàng')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết loại hình hoạt động khách hàng',
    mota='Xem toàn bộ thông tin của một loại hình ở chế độ chỉ đọc, kèm danh sách lĩnh vực kinh '
         'doanh khách hàng đang trực thuộc và khối Lịch sử thay đổi.',
    tacnhan='Người quản lý / người xem danh mục loại hình hoạt động KH',
    dieukien='Người dùng có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng bấm vào Mã loại hình trên bảng.\n'
          '2. Hệ thống mở cửa sổ “Xem chi tiết loại hình hoạt động khách hàng”, mọi ô ở trạng thái '
          'chỉ đọc.\n'
          '3. (Tuỳ chọn) Người dùng bấm “Xem lịch sử” để mở rộng khối Lịch sử.\n'
          '4. Người dùng bấm Đóng để quay về danh sách.',
    phu='• Loại hình chưa có lĩnh vực trực thuộc → khối danh sách lĩnh vực hiện dấu “—”.\n'
        '• Bản ghi không còn → ' + CHANGED + ', không mở cửa sổ.',
    dacbiet=None)
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', modal='Xem chi tiết loại hình hoạt động khách hàng',
         shot=shot('05-xem.png'), shot_caption='Cửa sổ Xem chi tiết loại hình hoạt động khách hàng')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xem chi tiết loại hình hoạt động khách hàng”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Mã loại hình hoạt động KH', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', 'Không hiện dấu *.'),
    ('Loại hình hoạt động khách hàng (Tên)', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Trạng thái', 'Dropdown', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu', '–'),
    ('Danh sách lĩnh vực kinh doanh khách hàng thuộc nhóm', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi lĩnh vực trực thuộc là 1 thẻ “<mã> • <tên>”. Chỉ có ở màn Xem chi tiết.'),
    ('Mô tả', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở danh sách thay đổi của bản ghi (như FR-09).'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Không có nút Lưu.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Mã loại hình', 'Click',
     'Before:\n– Người dùng đang ở màn danh sách (có Q1 hoặc Q2).\n'
     'During:\n– Nạp chi tiết bản ghi kèm các lĩnh vực trực thuộc.\n'
     'After:\n– Mở cửa sổ chi tiết ở chế độ chỉ đọc.'),
    ('Bấm “Xem lịch sử”', 'Click', 'After:\n– Mở rộng khối Lịch sử và nạp danh sách thay đổi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Xóa loại hình hoạt động khách hàng')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xóa loại hình hoạt động KH', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-07 Xóa loại hình hoạt động khách hàng')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa loại hình hoạt động khách hàng',
    mota='Xóa hẳn một loại hình chưa có lĩnh vực kinh doanh khách hàng nào trực thuộc.',
    tacnhan='Người quản lý danh mục loại hình hoạt động KH',
    dieukien='Người dùng có quyền Q1; loại hình chưa có lĩnh vực kinh doanh trực thuộc.',
    chinh='1. Người dùng bấm nút Xóa trên dòng loại hình.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận xóa”.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống xóa bản ghi, ghi 1 dòng lịch sử “Xóa”, thông báo “Xoá thành công” và nạp lại '
          'danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xóa.\n'
        '• Loại hình đã có lĩnh vực trực thuộc (kể cả lĩnh vực đang Khóa) → nút Xóa bị ẩn.\n'
        '• Bản ghi đã bị xóa trước đó → ' + CHANGED + '.\n'
        '• Lỗi khác → “Xoá thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Xóa là xóa hẳn, không khôi phục được. Muốn ngừng dùng loại hình đã có lĩnh vực trực '
            'thuộc thì dùng chức năng Khóa.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', modal='Xác nhận xóa', shot=shot('06-xoa.png'),
         shot_caption='Hộp thoại xác nhận xóa loại hình hoạt động khách hàng')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xác nhận xóa”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn xóa loại hình hoạt động khách hàng \'<tên>\'?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
], required=False, scope=False)
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và loại hình chưa có lĩnh vực trực thuộc.\n'
     'After:\n– Hiện hộp thoại xác nhận.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Bản ghi không còn → ' + CHANGED + '.\n'
     'After:\n– Ghi 1 dòng lịch sử “Xóa” kèm dữ liệu lúc xóa, rồi xóa bản ghi.\n'
     '– Thông báo “Xoá thành công”, nạp lại danh sách.'),
    ('Bấm Hủy / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Khóa / Mở khóa loại hình hoạt động khách hàng')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Khóa / Mở khóa loại hình', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-08 Khóa / Mở khóa loại hình hoạt động khách hàng')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khóa / Mở khóa loại hình hoạt động khách hàng',
    mota='Chuyển trạng thái loại hình giữa Hoạt động và Khóa bằng nút Khóa / Mở khóa ở cột Hành '
         'động (nằm trong menu “…” khi dòng có hơn 3 thao tác).',
    tacnhan='Người quản lý danh mục loại hình hoạt động KH',
    dieukien='Người dùng có quyền Q1. Khóa: loại hình không còn lĩnh vực trực thuộc đang Hoạt động.',
    chinh='1. Người dùng bấm Khóa (hoặc Mở khóa) trên dòng.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khóa” (hoặc “Xác nhận mở khóa”).\n'
          '3. Người dùng bấm Khóa (hoặc Mở khóa).\n'
          '4. Hệ thống đổi trạng thái, ghi 1 dòng lịch sử nhóm “Thay đổi trạng thái”, thông báo '
          '“Khoá thành công” / “Mở khoá thành công”, nạp lại danh sách.',
    phu='• Loại hình còn lĩnh vực trực thuộc đang Hoạt động → nút Khóa bị ẩn; rê chuột vào nhãn '
        'trạng thái hiện “Cần khóa hết lĩnh vực kinh doanh trực thuộc trước khi khóa loại hình này”.\n'
        '• Phát sinh lĩnh vực Hoạt động trong lúc xác nhận → ' + CHANGED + '.\n'
        '• Bấm Hủy → không đổi trạng thái.',
    dacbiet='Mở khóa luôn được phép. Loại hình đang Khóa không Sửa được cho tới khi Mở khóa; loại '
            'hình đã Khóa không chọn được cho lĩnh vực mới nhưng vẫn giữ nguyên ở lĩnh vực đang dùng.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Khóa / Mở khóa',
         modal='Xác nhận khóa / Xác nhận mở khóa',
         shot=shot('07b-khoa.png'), shot_caption='Hộp thoại xác nhận khóa loại hình')
d.figure(shot('07c-mo-khoa.png'), 'Hộp thoại xác nhận mở khóa loại hình', width_in=6.2)
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Khóa / Mở khóa trên dòng', 'Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Đang Hoạt động: Khóa (ổ khóa đóng). Đang Khóa: Mở khóa (ổ khóa mở).'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khóa” / “Xác nhận mở khóa”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn khóa (mở khóa) loại hình hoạt động khách hàng \'<tên>\'?”'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Khóa / Mở khóa trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện với Q1; Khóa chỉ hiện khi không còn lĩnh vực trực thuộc đang Hoạt động.\n'
     'After:\n– Hiện hộp thoại xác nhận tương ứng.'),
    ('Bấm Khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Còn lĩnh vực trực thuộc đang Hoạt động → ' + CHANGED + ' và dừng xử lý.\n'
     'After:\n– Đổi trạng thái sang Khóa, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng thái”.\n'
     '– Thông báo “Khoá thành công”, nạp lại danh sách.'),
    ('Bấm Mở khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Đổi trạng thái sang Hoạt động, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng '
     'thái”.\n– Thông báo “Mở khoá thành công”, nạp lại danh sách.'),
    ('Lỗi khác', 'System', 'After:\n– Thông báo nội dung lỗi hệ thống trả về, hoặc “Thay đổi trạng thái thất bại”.'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Xem lịch sử thay đổi')
d.p('2.9.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung thông tin riêng của Danh mục '
           'loại hình hoạt động khách hàng.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của loại hình hoạt động khách hàng',
    mota='Xem các lần Tạo mới, Thay đổi thông tin, Khóa / Mở khóa của một loại hình: ai làm, lúc '
         'nào, trường nào đổi từ giá trị cũ sang giá trị mới.',
    tacnhan='Người quản lý / người xem danh mục loại hình hoạt động KH',
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
         shot=shot('08-lich-su.png'), shot_caption='Cửa sổ Lịch sử thay đổi của loại hình')
d.p('2.9.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Lịch sử thay đổi: <mã> - <tên>”.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Lọc danh sách theo nhóm thay đổi.'),
    ('Danh sách thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dạng dòng thời gian. Mỗi mục: thời điểm, nhóm (Tạo mới / Thay đổi thông tin / Khóa / Mở '
     'khóa), người thực hiện kèm phòng ban, các trường đổi (Mã, Tên, Mô tả, Trạng thái) với giá trị '
     'cũ → giá trị mới.'),
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
d.uc_figure('FR-10', 'Import Excel loại hình', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-10 Import Excel loại hình hoạt động khách hàng')
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Import file, Validate dữ liệu và Thông báo.', anchor='excel')
d.intro_table(
    ten='Import Excel loại hình hoạt động khách hàng',
    mota='Thêm mới hàng loạt loại hình từ tệp Excel theo file mẫu. Chỉ thêm mới, không cập nhật '
         'loại hình đã có.',
    tacnhan='Người quản lý danh mục loại hình hoạt động KH',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm Import Excel.\n'
          '2. (Tuỳ chọn) Bấm “Tải file mẫu” để lấy tệp Mau_import_Nhom_linh_vuc_khach_hang.xlsx.\n'
          '3. Bấm “Chọn file Excel”, chọn tệp đã điền dữ liệu.\n'
          '4. Bấm “Load lên bảng” để đọc tệp ra bảng xem trước.\n'
          '5. Bấm “Validate” → hệ thống kiểm tra từng dòng, đánh dấu dòng hợp lệ / lỗi kèm lý do; '
          'dòng hợp lệ bị khóa không sửa được.\n'
          '6. Nếu còn dòng lỗi: sửa trực tiếp các dòng lỗi rồi Validate lại, hoặc bấm “Bỏ dòng lỗi” '
          'để loại các dòng lỗi khỏi bảng.\n'
          '7. Khi đã Validate và không còn dòng lỗi, nút Import mới bấm được. Bấm “Import” → hệ '
          'thống ghi các dòng, thông báo “Import thành công <n> loại '
          'hình hoạt động khách hàng”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Chưa Validate, hoặc còn dòng lỗi → nút Import bị khóa, không bấm được.\n'
        '• Mọi dòng đều lỗi → sau khi bỏ dòng lỗi bảng không còn dòng nào, nút Import vẫn khóa; '
        'không import được.\n'
        '• Bấm “Bỏ dòng lỗi” → “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”\n'
        '• Bấm “Xoá trạng thái validate” → bỏ đánh dấu, mở khóa các dòng để sửa; phải Validate lại.\n'
        '• Dữ liệu thay đổi giữa lúc Validate và Import (vd người khác vừa tạo bản ghi trùng mã): '
        'còn ghi được một phần → “Import thành công x/y loại hình hoạt động khách hàng. z loại hình thất bại.”, đóng cửa sổ và nạp lại danh sách; '
        'không ghi được dòng nào → báo lỗi “Không có dữ liệu hợp lệ để import” (hoặc '
        '“Import thất bại: z/y loại hình hoạt động KH không hợp lệ”), cửa sổ giữ nguyên.\n'
        '• Tệp quá 500 dòng → “Mỗi lần import tối đa 500 dòng (file đang có N dòng), vui lòng tách '
        'file và import nhiều lần.”\n'
        '• Bật “Chỉ dòng lỗi” để lọc bảng xem trước chỉ còn dòng lỗi.\n'
        '• Bấm Làm mới → xóa dữ liệu đã nạp để chọn tệp khác.',
    dacbiet='Mỗi lần import tối đa 500 dòng. Import KHÔNG gắn lĩnh vực trực thuộc (lĩnh vực tự chọn '
            'loại hình ở màn Lĩnh vực kinh doanh khách hàng). Mỗi dòng thêm thành công đều ghi 1 dòng '
            'lịch sử “Tạo mới”.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Import Excel', modal='Import Loại hình hoạt động KH',
         shot=shot('09-import.png'), shot_caption='Cửa sổ Import Loại hình hoạt động KH')
d.figure(shot('09b-import-validate.png'), 'Bảng xem trước sau khi Validate — dòng lỗi kèm lý do',
         width_in=6.2)
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx / .xls', 'Có', 'Hiển thị', 'Chọn tệp cần import.'),
    ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Tải Mau_import_Nhom_linh_vuc_khach_hang.xlsx.'),
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
    ('Cột Mã loại hình hoạt động KH', 'Textbox', 'Enable', 'LHHDKH.XXXX', 'Có', 'Theo tệp',
     '4 ký tự chữ hoặc số sau “LHHDKH.”; không trùng trong tệp và hệ thống.'),
    ('Cột Loại hình hoạt động khách hàng', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo tệp',
     'Không trùng; không chứa , và :.'),
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
     '– Thiếu mã / tên / trạng thái → “Mã loại hình hoạt động KH không được để trống”, “Loại hình '
     'hoạt động KH không được để trống”, “Trạng thái không được để trống”.\n'
     '– Mã sai định dạng → “Mã loại hình hoạt động KH phải theo định dạng LHHDKH.XXXX (4 ký tự)”.\n'
     '– Mã trùng trong tệp → “Mã loại hình hoạt động KH bị trùng lặp trong file import (dòng n)”; '
     'trùng hệ thống → “Mã loại hình hoạt động KH đã tồn tại trong hệ thống”.\n'
     '– Tên trùng trong tệp → “Loại hình hoạt động KH bị trùng lặp trong file import (dòng n)”; '
     'trùng hệ thống → “Loại hình hoạt động KH đã tồn tại trong hệ thống”; quá dài → “Loại hình '
     'hoạt động KH vượt quá độ dài cho phép (tối đa 255 ký tự)”; chứa , hoặc : → “không được chứa '
     'ký tự dấu phẩy (,) và dấu hai chấm (:)”.\n'
     '– Trạng thái sai → “Trạng thái không hợp lệ, chỉ nhận giá trị: active hoặc inactive”.\n'
     '– Mô tả quá dài → “Mô tả vượt quá độ dài cho phép (tối đa 1000 ký tự)”.\n'
     'After:\n– Đánh dấu từng dòng hợp lệ / lỗi; thông báo “Validate thành công” hoặc “Validate xong: '
     'x hợp lệ, y không hợp lệ”.'),
    ('Bấm Import', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Nút chỉ bấm được khi đã Validate và không còn dòng lỗi.\n'
     'During:\n– Chỉ gửi các dòng hợp lệ. Máy chủ kiểm tra lại các dòng gửi lên như bước '
     'Validate.\n'
     'After:\n– Thêm mới các dòng hợp lệ, mã chuyển sang chữ in hoa; ghi lịch sử “Tạo mới” từng dòng.\n'
     '– Tất cả thành công → “Import thành công <n> loại hình hoạt động khách hàng”, đóng cửa sổ, nạp lại danh sách.\n'
     '– Một phần (dữ liệu thay đổi giữa lúc Validate và Import) → '
     '“Import thành công x/y loại hình hoạt động khách hàng. z loại hình thất bại.”, đóng cửa sổ, nạp lại danh sách.\n'
     '– Không ghi được dòng nào → báo lỗi “Không có dữ liệu hợp lệ để import” (hoặc '
     '“Import thất bại: z/y loại hình hoạt động KH không hợp lệ”); cửa sổ giữ nguyên, không ghi dữ liệu.'),
    ('Bấm Bỏ dòng lỗi', 'Click',
     'Before:\n– Chưa Validate → “Hãy Validate trước rồi mới bỏ dòng lỗi.”\n'
     'After:\n– Loại các dòng lỗi khỏi bảng; thông báo “Đã bỏ x dòng lỗi. Còn lại y dòng hợp '
     'lệ.”; nút Import mở nếu còn ≥ 1 dòng.'),
    ('Bấm Tải file mẫu', 'Click', 'After:\n– Tải tệp Mau_import_Nhom_linh_vuc_khach_hang.xlsx.'),
])

# ---------------------------------------------------------------- 2.11
d.h3('2.11 Xuất Excel')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Xuất Excel danh sách loại hình', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-11 Xuất Excel')
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của '
           'Danh mục loại hình hoạt động khách hàng.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách loại hình hoạt động khách hàng',
    mota='Người dùng chọn các trường cần xuất rồi tải về tệp '
         'danh_sach_loai_hinh_hoat_dong_khach_hang.xlsx gồm TẤT CẢ loại hình khớp bộ lọc đang áp '
         'dụng (không chỉ trang đang xem).',
    tacnhan='Người quản lý danh mục loại hình hoạt động KH',
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
            'loại hình hoạt động khách hàng”; số trong tệp là số thật.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất file',
         shot=shot('10-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất file')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường xuất', 'Table/Grid', 'Enable', '9 trường', 'Có (≥ 1)',
     'Tích sẵn các cột đang hiện trên bảng',
     'Mã loại hình hoạt động KH, Tên loại hình hoạt động khách hàng, Số lĩnh vực kinh doanh, Mô tả, '
     'Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. Kéo ≡ để đổi thứ tự.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn nhanh.'),
    ('Dòng “Đang chọn x/9 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Tải tệp danh_sach_loai_hinh_hoat_dong_khach_hang.xlsx.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiện trên bảng.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Áp đúng bộ lọc đang dùng trên màn, lấy tất cả dòng khớp.\n'
     'After:\n– Tải tệp danh_sach_loai_hinh_hoat_dong_khach_hang.xlsx với các trường đã chọn theo '
     'thứ tự đã sắp.\n– Thông báo “Xuất Excel thành công”.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Danh mục loại hình hoạt động khách hàng; '
           'không lặp lại các quy tắc đã có trong SRS quy tắc chung.', anchor='list',
           head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Định dạng và tính duy nhất của Mã', [
        '– Mã = tiền tố “LHHDKH.” + đúng 4 ký tự gồm chữ không dấu, chữ số, dấu gạch dưới '
        '(khi Import: chỉ chữ và số).',
        '– Hệ thống lưu mã ở dạng chữ in hoa; không trùng trong toàn hệ thống.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-02', 'Tên loại hình', [
        '– Bắt buộc, tối đa 255 ký tự, không trùng.',
        '– Không chứa dấu phẩy (,) và dấu hai chấm (:).',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-03', 'Quan hệ cha – con với Lĩnh vực kinh doanh khách hàng', [
        '– Một lĩnh vực thuộc một hoặc nhiều loại hình; việc gắn lĩnh vực vào loại hình thực hiện '
        'ở màn Lĩnh vực kinh doanh khách hàng (hoặc import lĩnh vực).',
        '– Chỉ loại hình đang Hoạt động mới được chọn thêm cho lĩnh vực; loại hình đã Khóa vẫn giữ '
        'nguyên ở lĩnh vực đang dùng (hiển thị kèm 🔒).',
    ], ['Danh sách', 'Xem chi tiết', 'Khóa / Mở khóa']),
    ('BR-04', 'Khóa sửa Mã khi đã có lĩnh vực trực thuộc',
     '– Loại hình đã có lĩnh vực kinh doanh trực thuộc thì không được đổi Mã.',
     'Chỉnh sửa'),
    ('BR-05', 'Chỉ sửa loại hình đang Hoạt động',
     '– Loại hình đang Khóa không sửa được (nút Sửa bị ẩn); phải Mở khóa trước.',
     ['Chỉnh sửa', 'Danh sách']),
    ('BR-06', 'Điều kiện Xóa', [
        '– Chỉ xóa được khi chưa có lĩnh vực kinh doanh nào trực thuộc (kể cả lĩnh vực đã Khóa); '
        'ngược lại nút Xóa bị ẩn.',
        '– Xóa là xóa hẳn; loại hình đã có lĩnh vực trực thuộc thì dùng Khóa thay cho Xóa.',
    ], 'Xóa'),
    ('BR-07', 'Điều kiện Khóa / Mở khóa', [
        '– Chỉ Khóa được khi mọi lĩnh vực trực thuộc đã Khóa (áp dụng cả khi đổi Trạng thái trong '
        'form Sửa — ô Trạng thái bị khóa).',
        '– Mở khóa luôn được phép.',
    ], ['Khóa / Mở khóa', 'Chỉnh sửa']),
    ('BR-08', 'Thao tác không dùng được thì ẩn', [
        '– Sửa, Xóa, Khóa / Mở khóa chỉ hiện với người có Q1 VÀ đủ điều kiện nghiệp vụ.',
        '– Không hiển thị nút xám; lý do chưa khóa được ghi ở nhãn Trạng thái khi rê chuột.',
    ], 'Danh sách'),
    ('BR-09', 'Ghi lịch sử thay đổi', [
        '– Ghi lại mọi lần Tạo mới (kể cả qua Import), Thay đổi thông tin, Khóa / Mở khóa, Xóa.',
        '– Thay đổi thông tin chỉ ghi các trường thực sự đổi: Mã, Tên, Mô tả; đổi Trạng thái ghi '
        'thành dòng “Thay đổi trạng thái” riêng.',
        '– Ai vào được màn đều xem được lịch sử.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xóa', 'Khóa / Mở khóa', 'Import Excel', 'Xem lịch sử']),
    ('BR-10', 'Import chỉ thêm mới', [
        '– Mỗi lần tối đa 500 dòng.',
        '– Mã / tên đã có trong hệ thống hoặc trùng nhau trong tệp → dòng lỗi, không ghi đè.',
        '– Chỉ các dòng hợp lệ được thêm; dòng lỗi được báo lý do cụ thể.',
    ], 'Import Excel'),
    ('BR-11', 'Xuất theo bộ lọc, chọn trường', [
        '– Chỉ người có Q1 xuất được.',
        '– Xuất tất cả dòng khớp bộ lọc đang áp dụng, không giới hạn theo trang.',
        '– Người dùng chọn trường và thứ tự trường; mặc định là các cột đang hiện trên bảng.',
    ], 'Xuất Excel'),
])

d.save(update_fields=False)

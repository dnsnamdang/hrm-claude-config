# -*- coding: utf-8 -*-
"""Sinh "SRS - Danh mục vai trò dự án.docx" theo code nhánh gop_db — form 2026-09-24.

Chạy:  python3 .plans/gop-db/srs-danh-muc-du-an/vai-tro-du-an/gen_srs.py
Ảnh chụp thật (Playwright 1440x900, bản gop_db cổng 3002): vai-tro-du-an_shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/project_role/index.vue · components/modal/project-role-modal.vue
      components/modal/CatalogHistoryModal.vue · components/assign/SystemInfoSection.vue
      components/subsystem-menu/presale.js (menu) · components/subsystems.js (phân hệ)
      static/Mau_import_vaitroduan.xlsx (file mẫu)
  BE  Modules/Assign/Routes/api.php (nhóm /assign/project_roles)
      Http/Requests/ProjectRole/ProjectRoleRequest.php · Http/Controllers/Api/V1/ProjectRolesController.php
      Services/ProjectRolesService.php · Entities/ProjectRoles.php
      Transformers/ProjectRolesResource/* · app/Http/Middleware/CheckImportRowLimit.php
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 988, 1003)
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
from docx.opc.constants import RELATIONSHIP_TYPE as _RT  # noqa: E402

# Mỗi đoạn "Quy tắc chung" 1 quan hệ hyperlink riêng (như Word ghi khi cập nhật mục lục).
# python-docx gộp các link trùng URL vào 1 quan hệ -> selfcheck đếm thiếu khi chạy
# save(update_fields=False). Chỉ vá cục bộ trong generator này, KHÔNG sửa thư viện dùng chung.


def _add_hyperlink_unique(paragraph, url, text):
    rels = paragraph.part.rels
    r_id = rels._next_rId
    rels.add_relationship(_RT.HYPERLINK, url, r_id, is_external=True)
    orig = paragraph.part.relate_to
    paragraph.part.relate_to = lambda *a, **k: r_id
    try:
        return _orig_add(paragraph, url, text)
    finally:
        paragraph.part.relate_to = orig


_orig_add = srs_docx_lib.add_hyperlink
srs_docx_lib.add_hyperlink = _add_hyperlink_unique

OUT = os.path.join(HERE, 'SRS - Danh mục vai trò dự án.docx')
SHOTS = os.path.join(HERE, 'vai-tro-du-an_shots')
MENU = 'Phân hệ CSKH trước bán => Danh mục => Vai trò dự án'
BULK = 'Xóa (các dòng đã chọn)'

A_QL = 'Người quản lý danh mục vai trò dự án (Q1)'
A_XEM = 'Người xem danh mục vai trò dự án (Q2)'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/project_role',
           full_url='https://<host-hrm>/assign/project_role', img_prefix='vaitroduan_gopdb_')

# Icon cho từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện
# (bản ghi đang khóa có sẵn nút Mở khóa ngay trên dòng nên không phải dựng tạm DOM).
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ CSKH trước bán': 'phanhe', 'Danh mục': 'danhmuc', 'Vai trò dự án': 'man',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidatboloc', 'Tuỳ chỉnh cột': 'tuychinhcot',
    'Tạo mới': 'taomoi', 'Sửa': 'sua', 'Xem chi tiết': 'xem', 'Xóa': 'xoa', BULK: 'xoanhieu',
    'Hành động khác': 'khac', 'Khóa': 'khoa', 'Mở khóa': 'mokhoa', 'Lịch sử': 'lichsu',
    'Import Excel': 'import', 'Xuất Excel': 'xuat',
}.items()})

d.title_block('Danh mục vai trò dự án')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục vai trò dự án thuộc phân hệ '
    'CSKH trước bán, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ cấu trúc cha – con giữa các vai trò dự án và các ràng buộc đi kèm (xóa, khóa, mở khóa).',
    'Làm rõ điều kiện hiện các thao tác Sửa, Xóa, Khóa, Mở khóa trên từng dòng và thao tác xóa '
    'nhiều dòng một lúc.',
    'Làm rõ quy tắc nhập dữ liệu hàng loạt từ tệp Excel và xuất dữ liệu ra tệp Excel.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Vai trò dự án', 'Vai trò của một thành viên trong dự án (vd PM dự án, Quản lý hạng mục, Kỹ sư '
     'thiết kế điện…). Danh mục không có mã, định danh bằng Tên.'),
    ('Vai trò cha / vai trò con', 'Một vai trò có thể thuộc 1 vai trò cha (vd “Kỹ sư công trường” '
     'thuộc “PM dự án”). Vai trò có vai trò khác trỏ tới là vai trò cha.'),
    ('Có vai trò con', 'Cột trên bảng: “Có” nếu vai trò đang là cha của ít nhất 1 vai trò khác, '
     'ngược lại “Không”.'),
    ('Trạng thái Khóa', 'Vai trò ngừng sử dụng: không sửa được cho tới khi Mở khóa. Khóa KHÔNG xóa '
     'dữ liệu.'),
    ('Menu “…” (Hành động khác)', 'Nút ở cột Hành động chứa các thao tác phụ của dòng khi dòng có '
     'nhiều hơn 3 thao tác: Khóa / Mở khóa, Lịch sử.'),
    ('Thanh chọn nhiều dòng', 'Khu vực bên trái phía trên bảng: “Đã chọn n dòng” kèm nút Xóa và Bỏ '
     'chọn, xuất hiện khi người dùng tích chọn ít nhất 1 dòng.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý danh mục vai trò dự án',
     'Xem danh sách, xem chi tiết, xem lịch sử; hiện nút Tạo mới, Import Excel; hiện các thao tác '
     'Sửa, Xóa, Khóa / Mở khóa trên dòng; xóa nhiều dòng; được Xuất Excel.'),
    ('Q2', 'Xem danh mục vai trò dự án',
     'Xem danh sách, tìm kiếm, xem chi tiết và xem lịch sử. Không được thay đổi dữ liệu, không '
     'được xuất Excel.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn hình không phân quyền theo cấp dữ liệu (công ty / phòng ban / bộ phận): người có quyền '
    'xem được toàn bộ vai trò dự án của hệ thống.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách vai trò dự án', '✅', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '❌'),
    ('FR-04 Tạo mới vai trò dự án', '✅', '❌', '❌'),
    ('FR-05 Chỉnh sửa vai trò dự án', '✅', '❌', '❌'),
    ('FR-06 Xem chi tiết vai trò dự án', '✅', '✅', '❌'),
    ('FR-07 Xóa vai trò dự án', '✅', '❌', '❌'),
    ('FR-08 Xóa nhiều vai trò dự án', '✅', '❌', '❌'),
    ('FR-09 Khóa / Mở khóa vai trò dự án', '✅', '❌', '❌'),
    ('FR-10 Xem lịch sử thay đổi', '✅', '✅', '❌'),
    ('FR-11 Import Excel', '✅', '❌', '❌'),
    ('FR-12 Xuất Excel', '✅', '❌', '❌'),
], widths=[3.0, 0.8, 0.8, 1.4])

# ================================================================ PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_QL, [0, 1, 2, 3, 4, 5, 6, 7]),
     (A_XEM, [0])],
    [('FR-01', 'Xem danh sách vai trò dự án', 'view'),
     ('FR-04', 'Tạo mới vai trò dự án', 'crud'),
     ('FR-05', 'Chỉnh sửa vai trò dự án', 'crud'),
     ('FR-07', 'Xóa vai trò dự án', 'action'),
     ('FR-08', 'Xóa nhiều vai trò dự án', 'action'),
     ('FR-09', 'Khóa / Mở khóa vai trò dự án', 'action'),
     ('FR-11', 'Import Excel vai trò dự án', 'io'),
     ('FR-12', 'Xuất Excel danh sách vai trò dự án', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết vai trò dự án', 'view', 'extend', [0], None),
     ('FR-10', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Danh mục vai trò dự án')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách vai trò dự án')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Danh mục vai trò dự án tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách vai trò dự án',
    mota='Hiển thị toàn bộ vai trò dự án kèm vai trò cha, có vai trò con hay không, mô tả, người '
         'tạo / cập nhật, trạng thái và các thao tác trên từng dòng.',
    tacnhan='Người quản lý / người xem danh mục vai trò dự án; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng vào menu Phân hệ CSKH trước bán → Danh mục → Vai trò dự án.\n'
          '2. Hệ thống nạp trang 1, 10 dòng/trang, bản ghi mới tạo lên đầu.\n'
          '3. Bảng hiển thị đủ các cột (mặc định hiện hết cột), dòng “Hiển thị a–b / N” và thanh '
          'phân trang.',
    phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm Tên vai trò dự án → mở cửa sổ Xem chi tiết (FR-06).\n'
        '• Bấm tiêu đề cột Tên vai trò dự án, Ngày tạo, Ngày cập nhật → sắp xếp theo cột đó, bấm '
        'lại để đảo chiều.\n'
        '• Rê chuột vào nhãn Trạng thái của dòng chưa khóa / mở khóa được → hiện lý do “Chưa khóa '
        'được: vai trò này còn vai trò con đang hoạt động” hoặc “Chưa mở khóa được: vai trò cha '
        'đang bị khóa”.\n'
        '• Rời màn rồi quay lại trong vòng 10 phút → bộ lọc đang dùng được khôi phục.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách vai trò dự án lúc mới truy cập')
d.figure(shot('01b-danh-sach-phai.png'), 'Phần bên phải của bảng: cột Trạng thái và cột Hành động',
         width_in=6.2)
d.figure(shot('07-menu-khac.png'), 'Menu “…” (Hành động khác) của một dòng đang Hoạt động',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Danh sách vai trò dự án”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1', 'Mở cửa sổ Tạo mới (FR-04).'),
    ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1',
     'Mở cửa sổ Import (FR-11).'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Chọn trường xuất file (FR-12).'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Dòng “Chưa chọn dòng nào.” / “Đã chọn n dòng”', 'Label', 'Hiển thị', '–', '“Chưa chọn dòng nào.”',
     'Khi có dòng được tích chọn thì kèm nút Xóa và Bỏ chọn (FR-08).'),
    ('Cột Chọn (ô tích)', 'Table/Grid', 'Enable / Disable', '–', 'Không tích',
     'Cố định bên trái; ô tích ở tiêu đề chọn / bỏ chọn cả trang. Vai trò đang có vai trò con thì '
     'ô tích bị khóa.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cố định bên trái khi cuộn ngang; không tắt được.'),
    ('Cột Tên vai trò dự án', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Cố định bên trái, không tắt được, sắp xếp được, tối đa 2 dòng. Là liên kết mở cửa sổ Xem chi '
     'tiết.'),
    ('Cột Vai trò cha', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tên vai trò cha (trống nếu không có).'),
    ('Cột Có vai trò con', 'Table/Grid', 'Read-only', 'Có / Không', 'Theo dữ liệu', 'Căn giữa.'),
    ('Cột Mô tả', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Người tạo hiển thị họ tên. Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu',
     'Hoạt động màu xanh, Khóa màu đỏ. Rê chuột hiện lý do khi chưa khóa / mở khóa được.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu',
     'Không tắt được. Thứ tự Sửa, Xóa, Khóa / Mở khóa, Lịch sử; có tối đa 3 thao tác thì hiện hết, '
     'nhiều hơn thì hiện 2 nút đầu, phần còn lại gom vào nút “…”. Thao tác không dùng được thì ẨN hẳn.'),
    ('Nút Sửa (bút)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và vai trò đang Hoạt động (FR-05).'),
    ('Nút Xóa (thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và vai trò không có vai trò con (FR-07).'),
    ('Mục Khóa / Mở khóa', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1. Khóa ẩn khi còn vai trò con đang Hoạt động; Mở khóa ẩn khi vai trò cha đang '
     'Khóa (FR-09).'),
    ('Mục Lịch sử', 'Button', 'Enable', '–', 'Hiển thị', 'Mọi người vào được màn đều thấy (FR-10).'),
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả', 'N là tổng số bản ghi khớp bộ lọc.'),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5 / 10 / 20 / 50', '10', 'Đổi thì quay về trang 1.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Về đầu / lùi / số trang / tiến / về cuối.'),
    ('Thanh cuộn ngang', 'Table/Grid', 'Enable', '–', 'Hiển thị khi bảng tràn',
     'Có ở cả phía trên và phía dưới bảng.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Hiển thị khi đang nạp', 'Tắt khi nạp xong.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'During:\n– Khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu có).\n'
     '– Nạp cấu hình cột đã lưu của người dùng và danh sách vai trò cho ô lọc Vai trò cha.\n'
     'After:\n– Hiển thị trang 1, 10 dòng, bản ghi mới tạo lên đầu.'),
    ('Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click',
     'After:\n– Sắp xếp theo cột đó, bấm lại để đảo chiều; quay về trang 1.'),
    ('Bấm số trang / đổi Số dòng/trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu; đổi số dòng/trang thì quay về trang 1.'),
    ('Bấm Tên vai trò dự án', 'Click', 'After:\n– Mở cửa sổ Xem chi tiết vai trò dự án (FR-06).'),
    ('Rê chuột vào nhãn Trạng thái', 'Hover',
     'After:\n– Hiện lý do chưa khóa / mở khóa được (nếu có).'),
    ('Bấm nút “…” ở cột Hành động', 'Click',
     'After:\n– Mở menu các thao tác còn lại của dòng (Khóa / Mở khóa, Lịch sử).'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Danh mục '
           'vai trò dự án tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc vai trò dự án',
    mota='Tìm nhanh theo tên vai trò hoặc tên người tạo; lọc nâng cao theo vai trò cha, trạng thái, '
         'người tạo, người cập nhật, khoảng ngày cập nhật.',
    tacnhan='Người quản lý / người xem danh mục vai trò dự án; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách vai trò dự án.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
          '3. Chọn giá trị ở các ô Vai trò cha, Trạng thái, Người tạo, Người cập nhật, Ngày cập '
          'nhật: chọn xong hệ thống tự lọc lại ngay.\n'
          '4. Bảng hiển thị kết quả từ trang 1.',
    phu='• Bấm Làm mới → xóa hết điều kiện lọc và các dòng đang chọn, trả về danh sách ban đầu.\n'
        '• Bấm “Ẩn tìm kiếm nâng cao” → thu gọn khối lọc, điều kiện đang chọn vẫn giữ.\n'
        '• Không có kết quả → “Không có dữ liệu phù hợp bộ lọc.”',
    dacbiet=None)
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-bo-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Placeholder “Tìm theo tên vai trò dự án, người tạo”. Tìm gần đúng theo Tên vai trò hoặc họ '
     'tên Người tạo. Áp dụng khi bấm Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao (nhãn đổi thành “Ẩn tìm kiếm nâng cao” khi đang mở).'),
    ('Vai trò cha', 'Dropdown', 'Enable', 'Danh sách vai trò dự án', 'Không', 'Trống',
     'Lọc các vai trò con trực tiếp của vai trò được chọn.'),
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
    ('Đổi giá trị một ô trong khối lọc', 'Change',
     'After:\n– Tự lọc lại ngay theo toàn bộ điều kiện đang chọn.'),
    ('Gõ vào ô tìm nhanh', 'Keypress', 'After:\n– Chưa lọc; chờ Enter hoặc nút Tìm kiếm.'),
    ('Bấm Làm mới', 'Click',
     'After:\n– Xóa mọi điều kiện và các dòng đang chọn, sắp xếp mặc định, hiển thị trang 1.'),
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
    dieukien='Đang ở màn danh sách vai trò dự án.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ với danh sách trường / cột, đánh dấu những mục đang hiện.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho người dùng, đóng cửa sổ và vẽ lại khối lọc / bảng.',
    phu='• Bấm “Khôi phục mặc định” → trả về bộ trường lọc mặc định của màn.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Cột Chọn, STT, Tên vai trò dự án và Hành động luôn hiện, không bỏ tích được (hiển thị '
        'xám + ổ khóa).',
    dacbiet='Mặc định màn hiện TẤT CẢ cột; người dùng tự tắt bớt nếu thấy bảng quá rộng.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột', modal='Cài đặt bộ lọc và Tuỳ chỉnh cột',
         shot=shot('02b-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('02c-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột — cột khóa hiển thị xám', width_in=6.2)
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường lọc', 'Table/Grid', 'Enable', '5 trường', 'Không', 'Theo cấu hình đã lưu',
     'Vai trò cha, Trạng thái, Người tạo, Người cập nhật, Ngày cập nhật. Mỗi dòng: số thứ tự, biểu '
     'tượng kéo ⠿, ô tích, tên trường.'),
    ('Nút Lưu (Cài đặt bộ lọc)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình trường lọc.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về bộ trường lọc mặc định.'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '12 cột', 'Không', 'Theo cấu hình đã lưu',
     'Cột Chọn, STT, Tên vai trò dự án, Hành động bị khóa (luôn hiện).'),
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
    ('Tên vai trò', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Placeholder “VD: Leader hạng mục”. Không trùng với vai trò đã có.'),
    ('Vai trò cha', 'Dropdown', 'Enable', 'Vai trò đang Hoạt động', 'Không', 'Trống',
     'Placeholder “Chọn vai trò cha”; có nút xóa chọn. Để trống = vai trò gốc.'),
    ('Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Không', 'Hoạt động',
     'Không có nút xóa chọn. Bị khóa khi vai trò đang có vai trò con Hoạt động.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Trống', 'Placeholder “Mô tả ngắn về vai trò (tuỳ chọn)”.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ kèm biểu tượng cảnh báo ngay dưới ô bị lỗi.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
]
SAVE_DURING = (
    '– Tên vai trò trống → “Bắt buộc phải nhập”; trùng → “Đã tồn tại trên hệ thống”; quá 255 ký tự '
    '→ “Vui lòng nhập tối đa 255 ký tự.”\n'
    '– Vai trò cha không còn trong hệ thống → “Không tồn tại”.\n'
    '– Trạng thái ngoài 2 giá trị Hoạt động / Khóa → “Không hợp lệ”.\n'
    '– Nếu có lỗi validate → thông báo “Bạn chưa nhập đầy đủ thông tin” và không thực hiện bước After.')

d.h3('2.4 Tạo mới vai trò dự án')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới vai trò dự án', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-04 Tạo mới vai trò dự án')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới vai trò dự án',
    mota='Thêm một vai trò dự án mới, có thể đặt dưới 1 vai trò cha đang Hoạt động.',
    tacnhan='Người quản lý danh mục vai trò dự án',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở cửa sổ “Tạo mới vai trò dự án”, nạp danh sách vai trò đang Hoạt động cho '
          'ô Vai trò cha, Trạng thái mặc định Hoạt động.\n'
          '3. Người dùng nhập Tên vai trò, chọn Vai trò cha (nếu có), Trạng thái, nhập Mô tả.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống kiểm tra dữ liệu, ghi bản ghi mới và ghi 1 dòng lịch sử “Tạo mới”.\n'
          '6. Thông báo “Thêm mới thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Bấm “Lưu & Tiếp tục” → lưu xong giữ cửa sổ mở, xóa trắng form để nhập bản ghi tiếp.\n'
        '• Vai trò cha vừa bị khóa → “Vai trò cha đã bị khóa, vui lòng chọn vai trò cha khác”.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu đã nhập.\n'
        '• Lỗi khác → thông báo “Thêm mới thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Bấm Lưu liên tiếp khi yêu cầu trước chưa xong thì hệ thống bỏ qua để tránh tạo trùng.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', modal='Tạo mới vai trò dự án', shot=shot('03-tao-moi.png'),
         shot_caption='Cửa sổ Tạo mới vai trò dự án')
d.figure(shot('03b-tao-moi-loi.png'), 'Cửa sổ Tạo mới khi bấm Lưu mà chưa nhập Tên vai trò',
         width_in=6.2)
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([('Tiêu đề “Tạo mới vai trò dự án”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–')]
           + FORM_ROWS[:-1] + [
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu rồi đóng cửa sổ.'),
    ('Nút Lưu & Tiếp tục', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu rồi xóa trắng form để nhập tiếp. Chỉ có ở Tạo mới.'),
    FORM_ROWS[-1],
])
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'Before:\n– Nút chỉ hiển thị khi có quyền Q1.\n'
     'After:\n– Mở cửa sổ với form trống, Trạng thái = Hoạt động; nạp danh sách vai trò đang Hoạt động.'),
    ('Bấm Lưu / Lưu & Tiếp tục', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING.replace(
         '– Nếu có lỗi validate',
         '– Vai trò cha đang Khóa → “Vai trò cha đã bị khóa, vui lòng chọn vai trò cha khác”.\n'
         '– Nếu có lỗi validate') + '\n'
     'After:\n– Ghi bản ghi mới; ghi người tạo, thời điểm tạo.\n'
     '– Ghi 1 dòng lịch sử “Tạo mới”.\n'
     '– Thông báo “Thêm mới thành công”, nạp lại danh sách.\n'
     '– Lưu: đóng cửa sổ. Lưu & Tiếp tục: giữ cửa sổ, xóa trắng form.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, không lưu dữ liệu đang nhập.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Chỉnh sửa vai trò dự án')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa vai trò dự án', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-05 Chỉnh sửa vai trò dự án')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa). '
           'Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa vai trò dự án',
    mota='Cập nhật tên, vai trò cha, trạng thái, mô tả của một vai trò dự án đang Hoạt động.',
    tacnhan='Người quản lý danh mục vai trò dự án',
    dieukien='Người dùng có quyền Q1; vai trò đang ở trạng thái Hoạt động.',
    chinh='1. Người dùng bấm nút Sửa trên dòng vai trò.\n'
          '2. Hệ thống mở cửa sổ “Sửa vai trò dự án” với dữ liệu hiện tại.\n'
          '3. Người dùng sửa thông tin và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu, cập nhật và ghi lịch sử các trường đã đổi (giá trị cũ → '
          'giá trị mới).\n'
          '5. Thông báo “Cập nhật thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Vai trò đang Khóa → nút Sửa bị ẩn.\n'
        '• Vai trò cha đang gán nay đã bị khóa → vẫn hiển thị đúng tên trong ô (kèm biểu tượng 🔒).\n'
        '• Vai trò đã bị khóa bởi người khác, hoặc vai trò cha đang chọn đã Khóa, hoặc chọn Khóa khi '
        'còn vai trò con Hoạt động → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
        '• Chọn chính vai trò đang sửa làm vai trò cha → “Vai trò cha không thể là chính nó”.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới ô, thông báo “Bạn chưa nhập đầy đủ thông tin”.',
    dacbiet='Ô Trạng thái bị khóa khi vai trò còn vai trò con đang Hoạt động. Không có nút Lưu & '
            'Tiếp tục.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', modal='Sửa vai trò dự án', shot=shot('04-sua.png'),
         shot_caption='Cửa sổ Sửa vai trò dự án')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Sửa vai trò dự án”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Tên vai trò', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo dữ liệu', 'Như Tạo mới.'),
    ('Vai trò cha', 'Dropdown', 'Enable', 'Vai trò đang Hoạt động + vai trò cha đang gán', 'Không',
     'Theo dữ liệu', 'Vai trò cha đang gán đã khóa vẫn hiển thị kèm 🔒.'),
    ('Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Không', 'Theo dữ liệu',
     'Bị khóa khi còn vai trò con đang Hoạt động.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Theo dữ liệu', '–'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu rồi đóng cửa sổ.'),
    FORM_ROWS[-2], FORM_ROWS[-1],
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và vai trò đang Hoạt động.\n'
     'During:\n– Nạp chi tiết bản ghi và danh sách vai trò (kèm vai trò cha đang gán).\n'
     '– Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ Sửa với dữ liệu hiện tại.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Vai trò không còn Hoạt động, hoặc vai trò cha đang Khóa, hoặc chuyển sang Khóa khi còn vai '
     'trò con đang Hoạt động → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'During:\n' + SAVE_DURING.replace(
         '– Nếu có lỗi validate',
         '– Vai trò cha là chính nó → “Vai trò cha không thể là chính nó”.\n'
         '– Nếu có lỗi validate').replace('trùng →', 'trùng vai trò KHÁC →') + '\n'
     'After:\n– Cập nhật bản ghi; ghi người cập nhật, thời điểm cập nhật.\n'
     '– Ghi lịch sử các trường đã đổi (Tên, Vai trò cha, Mô tả, Trạng thái).\n'
     '– Thông báo “Cập nhật thành công”, đóng cửa sổ, nạp lại danh sách.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xem chi tiết vai trò dự án')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết vai trò dự án',
    mota='Xem toàn bộ thông tin của một vai trò dự án ở chế độ chỉ đọc, kèm khối Lịch sử thay đổi.',
    tacnhan='Người quản lý / người xem danh mục vai trò dự án',
    dieukien='Người dùng có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng bấm vào Tên vai trò dự án trên bảng.\n'
          '2. Hệ thống mở cửa sổ “Xem chi tiết vai trò dự án”, mọi ô ở trạng thái chỉ đọc.\n'
          '3. (Tuỳ chọn) Người dùng bấm “Xem lịch sử” để mở rộng khối Lịch sử.\n'
          '4. Người dùng bấm Đóng để quay về danh sách.',
    phu='• Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.',
    dacbiet=None)
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', modal='Xem chi tiết vai trò dự án', shot=shot('05-xem.png'),
         shot_caption='Cửa sổ Xem chi tiết vai trò dự án')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xem chi tiết vai trò dự án”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Tên vai trò', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Vai trò cha', 'Dropdown', 'Read-only', '–', 'Theo dữ liệu', 'Vai trò cha đã khóa vẫn hiển thị đúng tên kèm 🔒.'),
    ('Trạng thái', 'Dropdown', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu', '–'),
    ('Mô tả', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở danh sách thay đổi của bản ghi (như FR-10).'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Không có nút Lưu.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tên vai trò dự án', 'Click',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'After:\n– Mở cửa sổ chi tiết ở chế độ chỉ đọc.'),
    ('Bấm “Xem lịch sử”', 'Click', 'After:\n– Mở rộng khối Lịch sử và nạp danh sách thay đổi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Xóa vai trò dự án')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xóa vai trò dự án', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-07 Xóa vai trò dự án')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa vai trò dự án',
    mota='Xóa hẳn một vai trò dự án không có vai trò con.',
    tacnhan='Người quản lý danh mục vai trò dự án',
    dieukien='Người dùng có quyền Q1; vai trò không có vai trò con.',
    chinh='1. Người dùng bấm nút Xóa trên dòng vai trò.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận xóa”.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống xóa bản ghi, ghi 1 dòng lịch sử “Xóa”, thông báo “Xoá thành công” và nạp lại '
          'danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xóa.\n'
        '• Vai trò có vai trò con → nút Xóa bị ẩn; nếu phát sinh vai trò con trong lúc đang xác nhận '
        '→ “Dữ liệu đang được sử dụng, vui lòng tải lại”.\n'
        '• Bản ghi đã bị xóa trước đó → “Dữ liệu đã thay đổi, vui lòng tải lại”.',
    dacbiet='Xóa là xóa hẳn, không khôi phục được. Muốn xóa vai trò cha thì phải xóa (hoặc chuyển) '
            'hết vai trò con trước.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', modal='Xác nhận xóa', shot=shot('06-xoa.png'),
         shot_caption='Hộp thoại xác nhận xóa vai trò dự án')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xác nhận xóa”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu', '“Bạn có chắc muốn xóa vai trò dự án \'<tên>\'?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
], required=False, scope=False)
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và vai trò không có vai trò con.\n'
     'After:\n– Hiện hộp thoại xác nhận.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Vai trò có vai trò con → “Dữ liệu đang được sử dụng, vui lòng tải lại” và dừng xử lý.\n'
     '– Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'After:\n– Ghi 1 dòng lịch sử “Xóa” kèm dữ liệu lúc xóa, rồi xóa bản ghi.\n'
     '– Thông báo “Xoá thành công”, nạp lại danh sách.'),
    ('Bấm Hủy / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Xóa nhiều vai trò dự án')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Xóa nhiều vai trò dự án', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-08 Xóa nhiều vai trò dự án')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa nhiều vai trò dự án',
    mota='Tích chọn nhiều dòng trên trang đang xem rồi xóa tất cả trong một lần xác nhận.',
    tacnhan='Người quản lý danh mục vai trò dự án',
    dieukien='Người dùng có quyền Q1; đã tích chọn ít nhất 1 vai trò không có vai trò con.',
    chinh='1. Người dùng tích ô chọn ở từng dòng (hoặc ô tích ở tiêu đề để chọn cả trang — chỉ chọn '
          'các vai trò không có vai trò con).\n'
          '2. Thanh chọn hiện “Đã chọn n dòng” kèm nút Xóa và Bỏ chọn.\n'
          '3. Người dùng bấm Xóa → hệ thống hiện hộp thoại “Xác nhận xóa nhiều”.\n'
          '4. Người dùng bấm Xóa trong hộp thoại.\n'
          '5. Hệ thống xóa các vai trò đã chọn (mỗi bản ghi ghi 1 dòng lịch sử “Xóa”), thông báo '
          '“Xóa thành công n vai trò dự án”, bỏ chọn và nạp lại danh sách.',
    phu='• Bấm Bỏ chọn → bỏ tích mọi dòng.\n'
        '• Vai trò có vai trò con → ô tích bị khóa, không chọn được.\n'
        '• Một trong các bản ghi đã bị xóa trước đó → không xóa bản ghi nào, báo lỗi; lỗi khác → '
        '“Lỗi khi xóa nhiều vai trò dự án”.',
    dacbiet='Việc xóa nhiều thực hiện trọn gói: lỗi ở 1 bản ghi thì không bản ghi nào bị xóa.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => ' + BULK, modal='Xác nhận xóa nhiều', shot=shot('11-chon-nhieu.png'),
         shot_caption='Thanh chọn nhiều dòng sau khi tích chọn 1 dòng')
d.figure(shot('11b-xoa-nhieu.png'), 'Hộp thoại Xác nhận xóa nhiều', width_in=6.2)
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tích chọn dòng / chọn cả trang', 'Table/Grid', 'Enable / Disable', 'Theo dữ liệu',
     'Vai trò có vai trò con thì ô tích bị khóa.'),
    ('Dòng “Đã chọn n dòng”', 'Label', 'Hiển thị', 'Theo lựa chọn', 'n là số dòng đang tích.'),
    ('Nút Xóa (thanh chọn)', 'Button', 'Enable', 'Hiện khi có dòng được chọn', 'Mở hộp thoại xác nhận.'),
    ('Nút Bỏ chọn', 'Button', 'Enable', 'Hiện khi có dòng được chọn', 'Bỏ tích mọi dòng.'),
    ('Nội dung hộp thoại', 'Label', 'Hiển thị', 'Theo dữ liệu', '“Bạn có chắc muốn xóa n vai trò đã chọn?”'),
    ('Nút Xóa / Hủy trong hộp thoại', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa / đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Tích / bỏ tích ô chọn', 'Click', 'After:\n– Cập nhật số dòng đang chọn trên thanh chọn.'),
    ('Bấm Xóa trên thanh chọn', 'Click',
     'Before:\n– Chưa chọn dòng nào → “Vui lòng chọn ít nhất một vai trò để xóa”.\n'
     'After:\n– Hiện hộp thoại Xác nhận xóa nhiều.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Mọi bản ghi được chọn phải còn tồn tại; nếu không → báo lỗi và không xóa bản ghi nào.\n'
     'After:\n– Xóa các bản ghi, ghi lịch sử “Xóa” cho từng bản ghi.\n'
     '– Thông báo “Xóa thành công n vai trò dự án”, bỏ chọn, nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Khóa / Mở khóa vai trò dự án')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Khóa / Mở khóa vai trò dự án', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-09 Khóa / Mở khóa vai trò dự án')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khóa / Mở khóa vai trò dự án',
    mota='Chuyển trạng thái vai trò giữa Hoạt động và Khóa bằng thao tác Khóa / Mở khóa ở cột '
         'Hành động, có ràng buộc theo quan hệ cha – con.',
    tacnhan='Người quản lý danh mục vai trò dự án',
    dieukien='Người dùng có quyền Q1. Khóa: vai trò không còn vai trò con đang Hoạt động. Mở khóa: '
             'vai trò cha (nếu có) không bị Khóa.',
    chinh='1. Người dùng chọn Khóa (dòng đang Hoạt động, trong menu “…”) hoặc Mở khóa (dòng đang '
          'Khóa, nút ổ khóa mở trên dòng).\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khóa” (hoặc “Xác nhận mở khóa”).\n'
          '3. Người dùng bấm Khóa (hoặc Mở khóa).\n'
          '4. Hệ thống đổi trạng thái, ghi 1 dòng lịch sử nhóm “Thay đổi trạng thái”, thông báo '
          '“Khóa thành công” / “Mở khóa thành công”, nạp lại danh sách.',
    phu='• Còn vai trò con đang Hoạt động → mục Khóa bị ẩn; rê chuột vào nhãn trạng thái hiện '
        '“Chưa khóa được: vai trò này còn vai trò con đang hoạt động”.\n'
        '• Vai trò cha đang Khóa → nút Mở khóa bị ẩn; nhãn trạng thái hiện “Chưa mở khóa được: vai '
        'trò cha đang bị khóa”.\n'
        '• Điều kiện thay đổi trong lúc xác nhận → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
        '• Bấm Hủy → không đổi trạng thái.',
    dacbiet='Khóa theo thứ tự từ con lên cha; Mở khóa theo thứ tự từ cha xuống con. Vai trò đang '
            'Khóa không Sửa được cho tới khi Mở khóa.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Khóa / Mở khóa',
         modal='Xác nhận khóa / Xác nhận mở khóa',
         shot=shot('07b-khoa.png'), shot_caption='Hộp thoại xác nhận khóa vai trò dự án')
d.figure(shot('07c-mo-khoa.png'), 'Hộp thoại xác nhận mở khóa vai trò dự án', width_in=6.2)
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Mục Khóa / nút Mở khóa', 'Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Đang Hoạt động: mục Khóa (ổ khóa đóng). Đang Khóa: nút Mở khóa (ổ khóa mở).'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khóa” / “Xác nhận mở khóa”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn khóa (mở khóa) vai trò dự án \'<tên>\'?”'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Khóa / Mở khóa', 'Click',
     'Before:\n– Khóa chỉ hiện với Q1 và khi không còn vai trò con đang Hoạt động; Mở khóa chỉ hiện '
     'với Q1 và khi vai trò cha không bị Khóa.\n'
     'After:\n– Hiện hộp thoại xác nhận tương ứng.'),
    ('Bấm Khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Còn vai trò con đang Hoạt động → “Dữ liệu đã thay đổi, vui lòng tải lại” và dừng '
     'xử lý.\n'
     'After:\n– Đổi trạng thái sang Khóa, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng thái”.\n'
     '– Thông báo “Khóa thành công”, nạp lại danh sách.'),
    ('Bấm Mở khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Vai trò cha đang Khóa → “Dữ liệu đã thay đổi, vui lòng tải lại” và dừng xử lý.\n'
     'After:\n– Đổi trạng thái sang Hoạt động, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng '
     'thái”.\n– Thông báo “Mở khóa thành công”, nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.10
d.h3('2.10 Xem lịch sử thay đổi')
d.p('2.10.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung thông tin riêng của Danh mục '
           'vai trò dự án.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của vai trò dự án',
    mota='Xem các lần Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Xóa của một vai trò: ai làm, '
         'lúc nào, trường nào đổi từ giá trị cũ sang giá trị mới.',
    tacnhan='Người quản lý / người xem danh mục vai trò dự án',
    dieukien='Người dùng vào được màn danh sách (Q1 hoặc Q2). Lịch sử không gắn quyền riêng.',
    chinh='1. Người dùng bấm “…” trên dòng rồi chọn Lịch sử (hoặc bấm nút Lịch sử nếu đang hiện '
          'sẵn trên dòng).\n'
          '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <tên>” và nạp danh sách thay đổi, mới nhất lên '
          'đầu.\n'
          '3. (Tuỳ chọn) Bấm Bộ lọc để lọc theo nhóm hành động / người thực hiện.\n'
          '4. Người dùng bấm Đóng.',
    phu='• Chưa có thay đổi nào → hiển thị thông báo chưa có lịch sử.',
    dacbiet=None)
d.p('2.10.2 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Lịch sử', modal='Lịch sử thay đổi',
         shot=shot('08-lich-su.png'), shot_caption='Cửa sổ Lịch sử thay đổi của vai trò dự án')
d.p('2.10.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Lịch sử thay đổi: <tên vai trò>”.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Lọc theo nhóm hành động, người thực hiện.'),
    ('Danh sách thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi lần thay đổi: thời điểm, nhóm hành động, người thực hiện kèm phòng ban, các trường đổi '
     '(Tên, Vai trò cha, Mô tả, Trạng thái) với giá trị cũ (đỏ) → giá trị mới (xanh).'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)
d.p('2.10.4 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Lịch sử', 'Click', 'After:\n– Mở cửa sổ và nạp danh sách thay đổi của bản ghi.'),
    ('Bấm Bộ lọc, chọn điều kiện', 'Click / Change', 'After:\n– Lọc lại danh sách thay đổi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.11
d.h3('2.11 Import Excel')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Import Excel vai trò dự án', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-11 Import Excel vai trò dự án')
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc Import file, Validate dữ liệu và Thông báo.', anchor='excel')
d.intro_table(
    ten='Import Excel vai trò dự án',
    mota='Thêm mới hàng loạt vai trò dự án từ tệp Excel theo file mẫu, kể cả quan hệ cha – con. '
         'Chỉ thêm mới, không cập nhật vai trò đã có.',
    tacnhan='Người quản lý danh mục vai trò dự án',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm Import Excel.\n'
          '2. (Tuỳ chọn) Bấm “Tải file mẫu” để lấy tệp Mau_import_vaitroduan.xlsx.\n'
          '3. Bấm “Chọn file Excel”, chọn tệp đã điền dữ liệu.\n'
          '4. Bấm “Load lên bảng” để đọc tệp ra bảng xem trước.\n'
          '5. Bấm “Validate” → hệ thống kiểm tra từng dòng, đánh dấu dòng hợp lệ / lỗi kèm lý do; '
          'dòng hợp lệ bị khóa không sửa được.\n'
          '6. Nếu còn dòng lỗi: sửa trực tiếp các dòng lỗi rồi Validate lại, hoặc bấm “Bỏ dòng lỗi” '
          'để loại các dòng lỗi khỏi bảng.\n'
          '7. Khi đã Validate và không còn dòng lỗi, nút Import mới bấm được. Bấm “Import” → hệ thống '
          'thêm các dòng rồi gán vai trò cha, thông báo “Import thành công <n> vai trò dự án”, đóng cửa sổ và nạp lại danh '
          'sách.',
    phu='• Chưa Validate, hoặc còn dòng lỗi → nút Import bị khóa, không bấm được.\n'
        '• Mọi dòng đều lỗi → sau khi bỏ dòng lỗi bảng không còn dòng nào, nút Import vẫn khóa; không '
        'import được.\n'
        '• Bấm “Bỏ dòng lỗi” → “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”\n'
        '• Bấm “Xoá trạng thái validate” → bỏ đánh dấu, mở khóa các dòng để sửa; phải Validate lại.\n'
        '• Dữ liệu thay đổi giữa lúc Validate và Import (vd người khác vừa tạo vai trò trùng tên): còn ghi '
        'được một phần → “Import thành công x/y vai trò dự án. z vai trò dự án thất bại.”, đóng cửa sổ; không ghi '
        'được dòng nào → báo lỗi “Không có dữ liệu hợp lệ để import” (hoặc “Import thất bại: z/y vai trò dự án không hợp lệ”, cửa sổ giữ nguyên.\n'
        '• Tệp quá 500 dòng → “Mỗi lần import tối đa 500 dòng (file đang có N dòng), vui lòng tách '
        'file và import nhiều lần.”\n'
        '• Bấm Làm mới → xóa dữ liệu đã nạp để chọn tệp khác.',
    dacbiet='Vai trò cha ghi bằng TÊN: là vai trò đang Hoạt động trong hệ thống, hoặc một dòng khác '
            'trong cùng tệp có Trạng thái “Hoạt động”. Mỗi lần tối đa 500 dòng; mỗi dòng thêm thành '
            'công ghi 1 dòng lịch sử “Tạo mới”.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Import Excel', modal='Import Vai trò dự án', shot=shot('09-import.png'),
         shot_caption='Cửa sổ Import Vai trò dự án')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx / .xls', 'Có', 'Hiển thị', 'Chọn tệp cần import.'),
    ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải Mau_import_vaitroduan.xlsx.'),
    ('Nút Load lên bảng', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa chọn tệp',
     'Đọc tệp ra bảng xem trước.'),
    ('Nút Validate', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu',
     'Kiểm tra dữ liệu từng dòng.'),
    ('Nút Import', 'Button', 'Enable / Disable', '–', '–', 'Disable',
     'Chỉ bấm được khi đã Validate và không còn dòng lỗi.'),
    ('Nút Bỏ dòng lỗi', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu',
     'Loại các dòng lỗi khỏi bảng xem trước.'),
    ('Nút Xoá trạng thái validate', 'Button', 'Enable / Disable', '–', '–',
     'Disable khi chưa có dữ liệu', 'Bỏ kết quả Validate để sửa lại dữ liệu.'),
    ('Dòng Tổng / hợp lệ / lỗi', 'Label', 'Read-only', '–', '–', 'Tổng: 0', 'Thống kê sau khi nạp / Validate.'),
    ('Cột Tên vai trò dự án', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo tệp',
     'Không trùng trong tệp và trong hệ thống.'),
    ('Cột Vai trò cha', 'Textbox', 'Enable', 'Tên vai trò', 'Không', 'Theo tệp',
     'Khác chính dòng đó; phải là vai trò đang Hoạt động.'),
    ('Cột Trạng thái', 'Textbox', 'Enable', 'Hoạt động / Khóa', 'Có', 'Theo tệp', 'Ghi đúng chữ.'),
    ('Cột Mô tả', 'Textarea', 'Enable', '0–1.000 ký tự', 'Không', 'Theo tệp', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không import.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa dữ liệu đã nạp.'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Validate', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Tệp quá 500 dòng → báo “Mỗi lần import tối đa 500 dòng …” và dừng xử lý.\n'
     'During (từng dòng):\n'
     '– Tên trống → “Tên vai trò dự án không được để trống”; quá 255 ký tự → “Tên vai trò dự án '
     'vượt quá độ dài cho phép (tối đa 255 ký tự)”.\n'
     '– Tên trùng trong tệp → “Tên vai trò dự án bị trùng lặp trong file import (dòng n)”; trùng hệ '
     'thống → “Tên vai trò dự án đã tồn tại trong hệ thống”.\n'
     '– Trạng thái trống / sai → “Trạng thái không hợp lệ (chỉ nhận đúng: Hoạt động hoặc Khóa)”.\n'
     '– Vai trò cha trùng chính nó → “Vai trò cha không thể là chính nó”; không tìm thấy → “Vai trò '
     'cha không tồn tại (chỉ cho chọn vai trò cha đang Hoạt động)”; vai trò cha trong tệp không ở '
     'trạng thái Hoạt động → “Vai trò cha phải ở trạng thái Hoạt động”.\n'
     '– Mô tả quá dài → “Mô tả vượt quá độ dài cho phép (tối đa 1000 ký tự)”.\n'
     'After:\n– Đánh dấu từng dòng hợp lệ / lỗi; thông báo “Validate thành công” hoặc “Validate xong: '
     'x hợp lệ, y không hợp lệ”.'),
    ('Bấm Import', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Nút chỉ bấm được khi đã Validate và không còn dòng lỗi.\n'
     'During:\n– Chỉ gửi các dòng hợp lệ trên bảng xem trước.\n'
     '– Máy chủ kiểm tra lại các dòng gửi lên như bước Validate.\n'
     'After:\n– Thêm mới các dòng; gán vai trò cha (cha có sẵn trong hệ thống gán ngay, cha '
     'nằm trong tệp gán sau khi tạo xong); ghi lịch sử “Tạo mới” từng dòng.\n'
     '– Tất cả các dòng ghi được → thông báo “Import thành công <n> vai trò dự án”, đóng cửa sổ, nạp lại '
     'danh sách.\n'
     '– Chỉ ghi được một phần (dữ liệu thay đổi giữa lúc Validate và Import, vd người khác vừa tạo vai trò trùng tên) '
     '→ thông báo “Import thành công x/y vai trò dự án. z vai trò dự án thất bại.”, đóng cửa sổ, nạp lại '
     'danh sách.\n'
     '– Không ghi được dòng nào → báo lỗi “Không có dữ liệu hợp lệ để import” (hoặc “Import thất bại: z/y vai trò dự án không hợp lệ”; cửa sổ giữ nguyên, không '
     'ghi dữ liệu.'),
    ('Bấm Bỏ dòng lỗi', 'Click',
     'Before:\n– Chưa Validate → “Hãy Validate trước rồi mới bỏ dòng lỗi.” và dừng xử lý.\n'
     'After:\n– Loại các dòng lỗi khỏi bảng xem trước; thông báo “Đã bỏ x dòng lỗi. Còn lại y dòng '
     'hợp lệ.”\n'
     '– Còn ≥ 1 dòng hợp lệ → nút Import mở cho bấm.'),
    ('Bấm Tải file mẫu', 'Click', 'After:\n– Tải tệp Mau_import_vaitroduan.xlsx.'),
])

# ---------------------------------------------------------------- 2.12
d.h3('2.12 Xuất Excel')
d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Xuất Excel danh sách vai trò dự án', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-12 Xuất Excel')
d.p('2.12.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của '
           'Danh mục vai trò dự án.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách vai trò dự án',
    mota='Người dùng chọn các trường cần xuất rồi tải về tệp danh_sach_vai_tro_du_an.xlsx gồm TẤT '
         'CẢ vai trò khớp bộ lọc đang áp dụng (không chỉ trang đang xem).',
    tacnhan='Người quản lý danh mục vai trò dự án',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng (tuỳ chọn) đặt bộ lọc trên màn danh sách.\n'
          '2. Bấm Xuất Excel.\n'
          '3. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiện trên bảng.\n'
          '4. Người dùng tích / bỏ tích, kéo để đổi thứ tự trường, rồi bấm Xuất file.\n'
          '5. Hệ thống dựng tệp theo bộ lọc, trình duyệt tải tệp về, thông báo “Xuất Excel thành công”.',
    phu='• Bấm “Chọn tất cả” / “Bỏ chọn hết” để chọn nhanh.\n'
        '• Lỗi khi dựng tệp → thông báo “Lỗi khi xuất Excel”.\n'
        '• Người chỉ có Q2 bấm Xuất file → hệ thống từ chối vì thiếu quyền.',
    dacbiet='Nút Xuất Excel bị khóa trong lúc đang xuất để tránh bấm lặp.')
d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất file',
         shot=shot('10-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất file')
d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường xuất', 'Table/Grid', 'Enable', '9 trường', 'Có (≥ 1)',
     'Tích sẵn các cột đang hiện trên bảng',
     'Tên vai trò dự án, Vai trò cha, Có vai trò con, Mô tả, Trạng thái, Người tạo, Ngày tạo, Người '
     'cập nhật, Ngày cập nhật. Kéo ⠿ để đổi thứ tự.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn nhanh.'),
    ('Dòng “Đang chọn x/9 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Tải tệp danh_sach_vai_tro_du_an.xlsx.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiện trên bảng.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Áp đúng bộ lọc đang dùng trên màn, lấy tất cả dòng khớp.\n'
     'After:\n– Tải tệp danh_sach_vai_tro_du_an.xlsx với các trường đã chọn theo thứ tự đã sắp.\n'
     '– Thông báo “Xuất Excel thành công”.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Danh mục vai trò dự án; không lặp lại các '
           'quy tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Tên vai trò dự án', [
        '– Bắt buộc, tối đa 255 ký tự, không trùng trong toàn hệ thống.',
        '– Danh mục không có mã: tên là định danh hiển thị ở danh sách, lịch sử và file xuất.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-02', 'Quan hệ cha – con', [
        '– Mỗi vai trò có tối đa 1 vai trò cha; để trống là vai trò gốc.',
        '– Vai trò cha phải đang Hoạt động khi chọn; không được chọn chính nó.',
        '– Vai trò cha đang gán nay đã khóa vẫn hiển thị đúng tên (🔒) ở màn Sửa / Xem.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-03', 'Chỉ sửa vai trò đang Hoạt động',
     '– Vai trò đang Khóa không sửa được (nút Sửa bị ẩn); phải Mở khóa trước.',
     ['Chỉnh sửa', 'Danh sách']),
    ('BR-04', 'Điều kiện Xóa', [
        '– Chỉ xóa được vai trò không có vai trò con (cả con đang Khóa); ngược lại nút Xóa và ô tích '
        'chọn bị ẩn / khóa.',
        '– Xóa là xóa hẳn; xóa nhiều thực hiện trọn gói.',
    ], ['Xóa', 'Xóa nhiều']),
    ('BR-05', 'Điều kiện Khóa / Mở khóa', [
        '– Khóa: không còn vai trò con nào đang Hoạt động (áp dụng cả khi đổi Trạng thái trong form '
        'Sửa — ô Trạng thái bị khóa).',
        '– Mở khóa: vai trò cha (nếu có) không bị Khóa.',
        '– Lý do chưa khóa / mở khóa được hiển thị khi rê chuột vào nhãn Trạng thái.',
    ], ['Khóa / Mở khóa', 'Chỉnh sửa']),
    ('BR-06', 'Thao tác không dùng được thì ẩn', [
        '– Tạo mới, Import, Sửa, Xóa, Khóa / Mở khóa chỉ hiện với người có Q1 và đủ điều kiện '
        'nghiệp vụ; không hiển thị nút xám.',
    ], 'Danh sách'),
    ('BR-07', 'Ghi lịch sử thay đổi', [
        '– Ghi lại mọi lần Tạo mới (kể cả qua Import), Thay đổi thông tin, Thay đổi trạng thái, Xóa.',
        '– Cập nhật chỉ ghi các trường thực sự đổi: Tên, Vai trò cha, Mô tả, Trạng thái.',
        '– Ai vào được màn đều xem được lịch sử.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xóa', 'Khóa / Mở khóa', 'Import Excel', 'Xem lịch sử']),
    ('BR-08', 'Import chỉ thêm mới', [
        '– Mỗi lần tối đa 500 dòng.',
        '– Tên đã có trong hệ thống hoặc trùng nhau trong tệp → dòng lỗi, không ghi đè.',
        '– Vai trò cha ghi bằng tên, lấy từ hệ thống (đang Hoạt động) hoặc từ dòng khác trong tệp '
        '(Trạng thái Hoạt động).',
    ], 'Import Excel'),
    ('BR-09', 'Xuất theo bộ lọc, chọn trường', [
        '– Chỉ người có Q1 được xuất.',
        '– Xuất tất cả dòng khớp bộ lọc đang áp dụng, không giới hạn theo trang.',
        '– Người dùng chọn trường và thứ tự trường; mặc định là các cột đang hiện trên bảng.',
    ], 'Xuất Excel'),
])

d.save(update_fields=False)

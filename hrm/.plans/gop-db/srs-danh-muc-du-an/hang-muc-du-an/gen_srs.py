# -*- coding: utf-8 -*-
"""Sinh "SRS - Danh mục hạng mục dự án.docx" theo code nhánh gop_db — form 2026-09-24.

Chạy:  python3 .plans/gop-db/srs-danh-muc-du-an/hang-muc-du-an/gen_srs.py
Ảnh chụp thật (Playwright 1440x900, bản gop_db cổng 3002): hang-muc-du-an_shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/project_items/{index.vue, AddProjectItemModal.vue}
      components/modal/CatalogHistoryModal.vue · components/assign/SystemInfoSection.vue
      components/subsystem-menu/presale.js (menu) · components/subsystems.js (phân hệ)
      static/Mau_import_hangmucduan.xlsx (file mẫu)
  BE  Modules/Assign/Routes/api.php (nhóm /assign/project_items)
      Http/Requests/ProjectItem/ProjectItemRequest.php · Http/Controllers/Api/V1/ProjectItemController.php
      Services/ProjectItemService.php · Entities/ProjectItem/ProjectItem.php
      Transformers/ProjectItemResource/* · app/Http/Middleware/CheckImportRowLimit.php
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 986, 1001)
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

OUT = os.path.join(HERE, 'SRS - Danh mục hạng mục dự án.docx')
SHOTS = os.path.join(HERE, 'hang-muc-du-an_shots')
MENU = 'Phân hệ CSKH trước bán => Danh mục => Hạng mục dự án'
BULK = 'Xóa (các dòng đã chọn)'

A_QL = 'Người quản lý danh mục hạng mục dự án (Q1)'
A_XEM = 'Người xem danh mục hạng mục dự án (Q2)'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/project_items',
           full_url='https://<host-hrm>/assign/project_items', img_prefix='hangmucduan_gopdb_')

# Icon cho từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện
# (bản ghi đang khóa có sẵn nút Mở khóa ngay trên dòng nên không phải dựng tạm DOM).
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ CSKH trước bán': 'phanhe', 'Danh mục': 'danhmuc', 'Hạng mục dự án': 'man',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidatboloc', 'Tuỳ chỉnh cột': 'tuychinhcot',
    'Tạo mới': 'taomoi', 'Sửa': 'sua', 'Xem chi tiết': 'xem', 'Xóa': 'xoa', BULK: 'xoanhieu',
    'Hành động khác': 'khac', 'Khóa': 'khoa', 'Mở khóa': 'mokhoa', 'Lịch sử': 'lichsu',
    'Import Excel': 'import', 'Xuất Excel': 'xuat',
}.items()})

d.title_block('Danh mục hạng mục dự án')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục hạng mục dự án thuộc phân hệ '
    'CSKH trước bán, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ quy tắc nhập liệu (tên hạng mục không trùng) và các thông báo lỗi.',
    'Làm rõ điều kiện hiện các thao tác Sửa, Xóa, Khóa, Mở khóa trên từng dòng và thao tác xóa '
    'nhiều dòng một lúc.',
    'Làm rõ quy tắc nhập dữ liệu hàng loạt từ tệp Excel và xuất dữ liệu ra tệp Excel.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hạng mục dự án', 'Danh mục các đầu việc/hạng mục chuẩn dùng khi lập kế hoạch dự án (vd “Xây '
     'dựng danh mục thiết bị”, “Ốp bản vẽ móng máy”). Danh mục không có mã, định danh bằng Tên.'),
    ('Tên hạng mục dự án', 'Tên định danh của hạng mục, không trùng trong toàn hệ thống.'),
    ('Trạng thái Khóa', 'Hạng mục ngừng sử dụng: không sửa được cho tới khi Mở khóa. Khóa KHÔNG xóa '
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
    ('Q1', 'Quản lý danh mục hạng mục dự án',
     'Xem danh sách, xem chi tiết, xem lịch sử; hiện nút Tạo mới, Import Excel; hiện các thao tác '
     'Sửa, Xóa, Khóa / Mở khóa trên dòng; xóa nhiều dòng; được Xuất Excel.'),
    ('Q2', 'Xem danh mục hạng mục dự án',
     'Xem danh sách, tìm kiếm, xem chi tiết và xem lịch sử. Không được thay đổi dữ liệu, không '
     'được xuất Excel.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn hình không phân quyền theo cấp dữ liệu (công ty / phòng ban / bộ phận): người có quyền '
    'xem được toàn bộ hạng mục dự án của hệ thống.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách hạng mục dự án', '✅', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '❌'),
    ('FR-04 Tạo mới hạng mục dự án', '✅', '❌', '❌'),
    ('FR-05 Chỉnh sửa hạng mục dự án', '✅', '❌', '❌'),
    ('FR-06 Xem chi tiết hạng mục dự án', '✅', '✅', '❌'),
    ('FR-07 Xóa hạng mục dự án', '✅', '❌', '❌'),
    ('FR-08 Xóa nhiều hạng mục dự án', '✅', '❌', '❌'),
    ('FR-09 Khóa / Mở khóa hạng mục dự án', '✅', '❌', '❌'),
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
    [('FR-01', 'Xem danh sách hạng mục dự án', 'view'),
     ('FR-04', 'Tạo mới hạng mục dự án', 'crud'),
     ('FR-05', 'Chỉnh sửa hạng mục dự án', 'crud'),
     ('FR-07', 'Xóa hạng mục dự án', 'action'),
     ('FR-08', 'Xóa nhiều hạng mục dự án', 'action'),
     ('FR-09', 'Khóa / Mở khóa hạng mục dự án', 'action'),
     ('FR-11', 'Import Excel hạng mục dự án', 'io'),
     ('FR-12', 'Xuất Excel danh sách hạng mục dự án', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết hạng mục dự án', 'view', 'extend', [0], None),
     ('FR-10', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Danh mục hạng mục dự án')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách hạng mục dự án')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Danh mục hạng mục dự án tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách hạng mục dự án',
    mota='Hiển thị toàn bộ hạng mục dự án kèm mô tả, người tạo / cập nhật, trạng thái và các thao '
         'tác trên từng dòng.',
    tacnhan='Người quản lý / người xem danh mục hạng mục dự án; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng vào menu Phân hệ CSKH trước bán → Danh mục → Hạng mục dự án.\n'
          '2. Hệ thống nạp trang 1, 10 dòng/trang, bản ghi mới tạo lên đầu.\n'
          '3. Bảng hiển thị đủ các cột (mặc định hiện hết cột), dòng “Hiển thị a–b / N” và thanh '
          'phân trang.',
    phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm Tên hạng mục dự án → mở cửa sổ Xem chi tiết (FR-06).\n'
        '• Bấm tiêu đề cột Tên hạng mục dự án, Ngày tạo, Ngày cập nhật → sắp xếp theo cột đó, bấm '
        'lại để đảo chiều.\n'
        '• Rời màn rồi quay lại trong vòng 10 phút → bộ lọc đang dùng được khôi phục.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách hạng mục dự án lúc mới truy cập')
d.figure(shot('01b-danh-sach-phai.png'), 'Phần bên phải của bảng: cột Trạng thái và cột Hành động '
         '(dòng đang Khóa không có nút Sửa, thay Khóa bằng Mở khóa)', width_in=6.2)
d.figure(shot('07-menu-khac.png'), 'Menu “…” (Hành động khác) của một dòng đang Hoạt động',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Danh sách hạng mục dự án”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1', 'Mở cửa sổ Tạo mới (FR-04).'),
    ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1',
     'Mở cửa sổ Import (FR-11).'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Chọn trường xuất file (FR-12).'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Dòng “Chưa chọn dòng nào.” / “Đã chọn n dòng”', 'Label', 'Hiển thị', '–', '“Chưa chọn dòng nào.”',
     'Khi có dòng được tích chọn thì kèm nút Xóa và Bỏ chọn (FR-08).'),
    ('Cột Chọn (ô tích)', 'Table/Grid', 'Enable / Disable', '–', 'Không tích',
     'Cố định bên trái; ô tích ở tiêu đề chọn / bỏ chọn cả trang. Dòng không xóa được thì ô tích bị '
     'khóa.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cố định bên trái khi cuộn ngang; không tắt được.'),
    ('Cột Tên hạng mục dự án', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Cố định bên trái, không tắt được, sắp xếp được, tối đa 2 dòng. Là liên kết mở cửa sổ Xem chi '
     'tiết.'),
    ('Cột Mô tả', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Người tạo hiển thị họ tên. Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu',
     'Hoạt động màu xanh, Khóa màu đỏ.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu',
     'Không tắt được. Thứ tự Sửa, Xóa, Khóa / Mở khóa, Lịch sử; có tối đa 3 thao tác thì hiện hết, '
     'nhiều hơn thì hiện 2 nút đầu, phần còn lại gom vào nút “…”. Thao tác không dùng được thì ẨN hẳn.'),
    ('Nút Sửa (bút)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và hạng mục đang Hoạt động (FR-05).'),
    ('Nút Xóa (thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 (FR-07).'),
    ('Mục Khóa / Mở khóa', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1. Dòng Hoạt động: Khóa (ổ khóa đóng); dòng Khóa: Mở khóa (ổ khóa mở) (FR-09).'),
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
     '– Nạp cấu hình cột đã lưu của người dùng.\n'
     'After:\n– Hiển thị trang 1, 10 dòng, bản ghi mới tạo lên đầu.'),
    ('Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click',
     'After:\n– Sắp xếp theo cột đó, bấm lại để đảo chiều; quay về trang 1.'),
    ('Bấm số trang / đổi Số dòng/trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu; đổi số dòng/trang thì quay về trang 1.'),
    ('Bấm Tên hạng mục dự án', 'Click', 'After:\n– Mở cửa sổ Xem chi tiết hạng mục dự án (FR-06).'),
    ('Bấm nút “…” ở cột Hành động', 'Click',
     'After:\n– Mở menu các thao tác còn lại của dòng (Khóa / Mở khóa, Lịch sử).'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Danh mục '
           'hạng mục dự án tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc hạng mục dự án',
    mota='Tìm nhanh theo tên hạng mục dự án hoặc tên người tạo; lọc nâng cao theo trạng thái, người '
         'tạo, người cập nhật, khoảng ngày cập nhật.',
    tacnhan='Người quản lý / người xem danh mục hạng mục dự án; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách hạng mục dự án.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
          '3. Chọn giá trị ở các ô Trạng thái, Người tạo, Người cập nhật, Ngày cập nhật: chọn xong '
          'hệ thống tự lọc lại ngay.\n'
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
     'Placeholder “Tìm theo tên hạng mục dự án, người tạo”. Tìm gần đúng theo Tên hạng mục hoặc họ '
     'tên Người tạo. Áp dụng khi bấm Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao (nhãn đổi thành “Ẩn tìm kiếm nâng cao” khi đang mở).'),
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
    dieukien='Đang ở màn danh sách hạng mục dự án.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ với danh sách trường / cột, đánh dấu những mục đang hiện.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho người dùng, đóng cửa sổ và vẽ lại khối lọc / bảng.',
    phu='• Bấm “Khôi phục mặc định” → trả về bộ trường lọc mặc định của màn.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Cột Chọn, STT, Tên hạng mục dự án và Hành động luôn hiện, không bỏ tích được (hiển thị '
        'xám + ổ khóa).',
    dacbiet='Mặc định màn hiện TẤT CẢ cột; người dùng tự tắt bớt nếu thấy bảng quá rộng.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột', modal='Cài đặt bộ lọc và Tuỳ chỉnh cột',
         shot=shot('02b-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('02c-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột — cột khóa hiển thị xám', width_in=6.2)
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường lọc', 'Table/Grid', 'Enable', '4 trường', 'Không', 'Theo cấu hình đã lưu',
     'Trạng thái, Người tạo, Người cập nhật, Ngày cập nhật. Mỗi dòng: số thứ tự, biểu tượng kéo ⠿, '
     'ô tích, tên trường.'),
    ('Nút Lưu (Cài đặt bộ lọc)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình trường lọc.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về bộ trường lọc mặc định.'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '10 cột', 'Không', 'Theo cấu hình đã lưu',
     'Cột Chọn, STT, Tên hạng mục dự án, Hành động bị khóa (luôn hiện).'),
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
    ('Hạng mục dự án (tên)', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Placeholder “VD: Hạng mục A / Hạng mục B / ...”. Không trùng với hạng mục đã có.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động',
     'Không có nút xóa chọn — luôn có giá trị.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Trống', 'Placeholder “Mô tả hạng mục dự án”.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ kèm biểu tượng cảnh báo ngay dưới ô bị lỗi.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
]
SAVE_DURING = (
    '– Tên hạng mục trống → “Bắt buộc phải nhập”.\n'
    '– Tên hạng mục đã tồn tại → “Đã tồn tại trên hệ thống”.\n'
    '– Tên hạng mục quá 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”\n'
    '– Trạng thái ngoài 2 giá trị Hoạt động / Khóa → “Không hợp lệ”.\n'
    '– Nếu có lỗi validate → thông báo “Bạn chưa nhập đầy đủ thông tin” và không thực hiện bước After.')

d.h3('2.4 Tạo mới hạng mục dự án')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới hạng mục dự án', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-04 Tạo mới hạng mục dự án')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới hạng mục dự án',
    mota='Thêm một hạng mục dự án mới vào danh mục.',
    tacnhan='Người quản lý danh mục hạng mục dự án',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở cửa sổ “Tạo mới hạng mục dự án”, Trạng thái mặc định Hoạt động.\n'
          '3. Người dùng nhập Tên hạng mục, chọn Trạng thái, nhập Mô tả (nếu có).\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống kiểm tra dữ liệu, ghi bản ghi mới và ghi 1 dòng lịch sử “Tạo mới”.\n'
          '6. Thông báo “Thêm mới thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Bấm “Lưu & Tiếp tục” → lưu xong giữ cửa sổ mở, xóa trắng form để nhập bản ghi tiếp.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu đã nhập.\n'
        '• Lỗi khác → thông báo “Thêm mới thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Bấm Lưu liên tiếp khi yêu cầu trước chưa xong thì hệ thống bỏ qua để tránh tạo trùng.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', modal='Tạo mới hạng mục dự án', shot=shot('03-tao-moi.png'),
         shot_caption='Cửa sổ Tạo mới hạng mục dự án')
d.figure(shot('03b-tao-moi-loi.png'), 'Cửa sổ Tạo mới khi bấm Lưu mà chưa nhập Tên hạng mục',
         width_in=6.2)
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([('Tiêu đề “Tạo mới hạng mục dự án”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–')]
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
     'After:\n– Mở cửa sổ với form trống, Trạng thái = Hoạt động.'),
    ('Bấm Lưu / Lưu & Tiếp tục', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING + '\n'
     'After:\n– Ghi bản ghi mới; ghi người tạo, thời điểm tạo.\n'
     '– Ghi 1 dòng lịch sử “Tạo mới”.\n'
     '– Thông báo “Thêm mới thành công”, nạp lại danh sách.\n'
     '– Lưu: đóng cửa sổ. Lưu & Tiếp tục: giữ cửa sổ, xóa trắng form.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, không lưu dữ liệu đang nhập.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Chỉnh sửa hạng mục dự án')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa hạng mục dự án', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-05 Chỉnh sửa hạng mục dự án')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa). '
           'Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa hạng mục dự án',
    mota='Cập nhật tên, trạng thái, mô tả của một hạng mục dự án đang Hoạt động.',
    tacnhan='Người quản lý danh mục hạng mục dự án',
    dieukien='Người dùng có quyền Q1; hạng mục đang ở trạng thái Hoạt động.',
    chinh='1. Người dùng bấm nút Sửa trên dòng hạng mục.\n'
          '2. Hệ thống mở cửa sổ “Sửa hạng mục dự án” với dữ liệu hiện tại.\n'
          '3. Người dùng sửa thông tin và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu, cập nhật và ghi lịch sử các trường đã đổi (giá trị cũ → '
          'giá trị mới).\n'
          '5. Thông báo “Cập nhật thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Hạng mục đang Khóa → nút Sửa bị ẩn.\n'
        '• Hạng mục đã bị xóa / khóa bởi người khác trong lúc sửa → “Dữ liệu đã thay đổi, vui lòng '
        'tải lại”.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới ô, thông báo “Bạn chưa nhập đầy đủ thông tin”.\n'
        '• Chọn Trạng thái = Khóa rồi Lưu → hạng mục chuyển sang Khóa (ghi lịch sử nhóm “Thay đổi '
        'trạng thái”).',
    dacbiet='Cửa sổ Sửa có sẵn khối Lịch sử thu gọn ở cuối form. Không có nút Lưu & Tiếp tục.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', modal='Sửa hạng mục dự án', shot=shot('04-sua.png'),
         shot_caption='Cửa sổ Sửa hạng mục dự án')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Sửa hạng mục dự án”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Hạng mục dự án (tên)', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo dữ liệu', 'Như Tạo mới.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Theo dữ liệu', '–'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Theo dữ liệu', '–'),
    ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở danh sách thay đổi của bản ghi.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu rồi đóng cửa sổ.'),
    FORM_ROWS[-2], FORM_ROWS[-1],
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và hạng mục đang Hoạt động.\n'
     'During:\n– Nạp chi tiết bản ghi; bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, '
     'không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ Sửa với dữ liệu hiện tại.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Hạng mục không còn hoặc không còn Hoạt động → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'During:\n' + SAVE_DURING.replace('– Tên hạng mục đã tồn tại', '– Tên trùng hạng mục KHÁC') + '\n'
     'After:\n– Cập nhật bản ghi; ghi người cập nhật, thời điểm cập nhật.\n'
     '– Ghi lịch sử các trường đã đổi (Tên, Mô tả, Trạng thái).\n'
     '– Thông báo “Cập nhật thành công”, đóng cửa sổ, nạp lại danh sách.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xem chi tiết hạng mục dự án')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết hạng mục dự án',
    mota='Xem toàn bộ thông tin của một hạng mục dự án ở chế độ chỉ đọc, kèm khối Lịch sử.',
    tacnhan='Người quản lý / người xem danh mục hạng mục dự án',
    dieukien='Người dùng có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng bấm vào Tên hạng mục dự án trên bảng.\n'
          '2. Hệ thống mở cửa sổ “Xem chi tiết hạng mục dự án”, mọi ô ở trạng thái chỉ đọc.\n'
          '3. (Tuỳ chọn) Người dùng bấm “Xem lịch sử” để mở rộng khối Lịch sử.\n'
          '4. Người dùng bấm Đóng để quay về danh sách.',
    phu='• Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.',
    dacbiet=None)
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', modal='Xem chi tiết hạng mục dự án', shot=shot('05-xem.png'),
         shot_caption='Cửa sổ Xem chi tiết hạng mục dự án')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xem chi tiết hạng mục dự án”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Hạng mục dự án (tên)', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Trạng thái', 'Dropdown', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu', '–'),
    ('Mô tả', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở danh sách thay đổi của bản ghi.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Không có nút Lưu.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tên hạng mục dự án', 'Click',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'After:\n– Mở cửa sổ chi tiết ở chế độ chỉ đọc.'),
    ('Bấm “Xem lịch sử”', 'Click', 'After:\n– Mở rộng khối Lịch sử và nạp danh sách thay đổi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Xóa hạng mục dự án')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xóa hạng mục dự án', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-07 Xóa hạng mục dự án')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa hạng mục dự án',
    mota='Xóa hẳn một hạng mục dự án khỏi danh mục.',
    tacnhan='Người quản lý danh mục hạng mục dự án',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Xóa trên dòng hạng mục.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận xóa”.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống xóa bản ghi, ghi 1 dòng lịch sử “Xóa”, thông báo “Xoá thành công” và nạp lại '
          'danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xóa.\n'
        '• Bản ghi đã bị xóa trước đó → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
        '• Lỗi khác → “Xoá thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Xóa là xóa hẳn, không khôi phục được. Hệ thống hiện không đặt điều kiện chặn xóa (kể cả '
            'hạng mục đang Khóa).')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', modal='Xác nhận xóa', shot=shot('06-xoa.png'),
         shot_caption='Hộp thoại xác nhận xóa hạng mục dự án')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xác nhận xóa”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn xóa hạng mục dự án \'<tên>\'?”'),
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
     'During:\n– Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại” và dừng xử lý.\n'
     'After:\n– Ghi 1 dòng lịch sử “Xóa” kèm dữ liệu lúc xóa, rồi xóa bản ghi.\n'
     '– Thông báo “Xoá thành công”, nạp lại danh sách.'),
    ('Bấm Hủy / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Xóa nhiều hạng mục dự án')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Xóa nhiều hạng mục dự án', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-08 Xóa nhiều hạng mục dự án')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa nhiều hạng mục dự án',
    mota='Tích chọn nhiều dòng trên trang đang xem rồi xóa tất cả trong một lần xác nhận.',
    tacnhan='Người quản lý danh mục hạng mục dự án',
    dieukien='Người dùng có quyền Q1; đã tích chọn ít nhất 1 dòng.',
    chinh='1. Người dùng tích ô chọn ở từng dòng (hoặc ô tích ở tiêu đề để chọn cả trang).\n'
          '2. Thanh chọn hiện “Đã chọn n dòng” kèm nút Xóa và Bỏ chọn.\n'
          '3. Người dùng bấm Xóa → hệ thống hiện hộp thoại “Xác nhận xóa nhiều”.\n'
          '4. Người dùng bấm Xóa trong hộp thoại.\n'
          '5. Hệ thống xóa lần lượt các hạng mục đã chọn (mỗi bản ghi ghi 1 dòng lịch sử “Xóa”), '
          'thông báo “Xóa thành công n hạng mục dự án”, bỏ chọn và nạp lại danh sách.',
    phu='• Bấm Bỏ chọn → bỏ tích mọi dòng.\n'
        '• Một trong các bản ghi đã bị xóa trước đó → không xóa bản ghi nào, thông báo lỗi dữ liệu '
        'không tồn tại; lỗi khác → “Lỗi khi xóa nhiều hạng mục dự án”.\n'
        '• Chuyển trang / lọc lại → các dòng đã chọn không còn trên trang được tự bỏ chọn.',
    dacbiet='Việc xóa nhiều thực hiện trọn gói: lỗi ở 1 bản ghi thì không bản ghi nào bị xóa.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => ' + BULK, modal='Xác nhận xóa nhiều', shot=shot('11-chon-nhieu.png'),
         shot_caption='Thanh chọn nhiều dòng sau khi tích chọn 1 dòng')
d.figure(shot('11b-xoa-nhieu.png'), 'Hộp thoại Xác nhận xóa nhiều', width_in=6.2)
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tích chọn dòng / chọn cả trang', 'Table/Grid', 'Enable / Disable', 'Theo dữ liệu',
     'Dòng không xóa được thì ô tích bị khóa.'),
    ('Dòng “Đã chọn n dòng”', 'Label', 'Hiển thị', 'Theo lựa chọn', 'n là số dòng đang tích.'),
    ('Nút Xóa (thanh chọn)', 'Button', 'Enable', 'Hiện khi có dòng được chọn', 'Mở hộp thoại xác nhận.'),
    ('Nút Bỏ chọn', 'Button', 'Enable', 'Hiện khi có dòng được chọn', 'Bỏ tích mọi dòng.'),
    ('Nội dung hộp thoại', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn xóa n hạng mục đã chọn?”'),
    ('Nút Xóa / Hủy trong hộp thoại', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa / đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Tích / bỏ tích ô chọn', 'Click', 'After:\n– Cập nhật số dòng đang chọn trên thanh chọn.'),
    ('Bấm Xóa trên thanh chọn', 'Click',
     'Before:\n– Chưa chọn dòng nào → “Vui lòng chọn ít nhất một hạng mục để xóa”.\n'
     'After:\n– Hiện hộp thoại Xác nhận xóa nhiều.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Mọi bản ghi được chọn phải còn tồn tại; nếu không → báo lỗi và không xóa bản ghi nào.\n'
     'After:\n– Xóa các bản ghi, ghi lịch sử “Xóa” cho từng bản ghi.\n'
     '– Thông báo “Xóa thành công n hạng mục dự án”, bỏ chọn, nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Khóa / Mở khóa hạng mục dự án')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Khóa / Mở khóa hạng mục dự án', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-09 Khóa / Mở khóa hạng mục dự án')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khóa / Mở khóa hạng mục dự án',
    mota='Chuyển trạng thái hạng mục giữa Hoạt động và Khóa bằng thao tác Khóa / Mở khóa ở cột '
         'Hành động.',
    tacnhan='Người quản lý danh mục hạng mục dự án',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Dòng đang Hoạt động: người dùng bấm “…” rồi chọn Khóa. Dòng đang Khóa: bấm nút Mở '
          'khóa (ổ khóa mở) ngay trên dòng.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khóa” (hoặc “Xác nhận mở khóa”).\n'
          '3. Người dùng bấm Khóa (hoặc Mở khóa).\n'
          '4. Hệ thống đổi trạng thái, ghi 1 dòng lịch sử nhóm “Thay đổi trạng thái”, thông báo '
          '“Khóa thành công” / “Mở khóa thành công”, nạp lại danh sách.',
    phu='• Hạng mục đã bị người khác khóa trong lúc xác nhận Khóa → “Dữ liệu đã thay đổi, vui lòng '
        'tải lại”.\n'
        '• Bấm Hủy → không đổi trạng thái.',
    dacbiet='Hạng mục đang Khóa không Sửa được cho tới khi Mở khóa.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Khóa / Mở khóa',
         modal='Xác nhận khóa / Xác nhận mở khóa',
         shot=shot('07b-khoa.png'), shot_caption='Hộp thoại xác nhận khóa hạng mục dự án')
d.figure(shot('07c-mo-khoa.png'), 'Hộp thoại xác nhận mở khóa hạng mục dự án', width_in=6.2)
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Mục Khóa / nút Mở khóa', 'Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Đang Hoạt động: mục Khóa (ổ khóa đóng) trong menu “…”. Đang Khóa: nút Mở khóa (ổ khóa mở).'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khóa” / “Xác nhận mở khóa”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn khóa (mở khóa) hạng mục dự án \'<tên>\'?”'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Khóa / Mở khóa', 'Click',
     'Before:\n– Thao tác chỉ hiện với Q1.\n'
     'After:\n– Hiện hộp thoại xác nhận tương ứng.'),
    ('Bấm Khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Hạng mục không còn ở trạng thái Hoạt động → “Dữ liệu đã thay đổi, vui lòng tải lại” '
     'và dừng xử lý.\n'
     'After:\n– Đổi trạng thái sang Khóa, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng thái”.\n'
     '– Thông báo “Khóa thành công”, nạp lại danh sách.'),
    ('Bấm Mở khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Đổi trạng thái sang Hoạt động, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng '
     'thái”.\n– Thông báo “Mở khóa thành công”, nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.10
d.h3('2.10 Xem lịch sử thay đổi')
d.p('2.10.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung thông tin riêng của Danh mục '
           'hạng mục dự án.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của hạng mục dự án',
    mota='Xem các lần Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Xóa của một hạng mục: ai làm, '
         'lúc nào, trường nào đổi từ giá trị cũ sang giá trị mới.',
    tacnhan='Người quản lý / người xem danh mục hạng mục dự án',
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
         shot=shot('08-lich-su.png'), shot_caption='Cửa sổ Lịch sử thay đổi của hạng mục dự án')
d.p('2.10.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Lịch sử thay đổi: <tên hạng mục>”.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Lọc theo nhóm hành động, người thực hiện.'),
    ('Danh sách thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi lần thay đổi: thời điểm, nhóm hành động (Tạo mới / Thay đổi thông tin / Thay đổi trạng '
     'thái / Xóa), người thực hiện kèm phòng ban, các trường đổi (Tên, Mô tả, Trạng thái) với giá '
     'trị cũ (đỏ) → giá trị mới (xanh).'),
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
d.uc_figure('FR-11', 'Import Excel hạng mục dự án', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-11 Import Excel hạng mục dự án')
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc Import file, Validate dữ liệu và Thông báo.', anchor='excel')
d.intro_table(
    ten='Import Excel hạng mục dự án',
    mota='Thêm mới hàng loạt hạng mục dự án từ tệp Excel theo file mẫu. Chỉ thêm mới, không cập '
         'nhật hạng mục đã có. Hạng mục nhập vào luôn ở trạng thái Hoạt động.',
    tacnhan='Người quản lý danh mục hạng mục dự án',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm Import Excel.\n'
          '2. (Tuỳ chọn) Bấm “Tải file mẫu” để lấy tệp Mau_import_hangmucduan.xlsx.\n'
          '3. Bấm “Chọn file Excel”, chọn tệp đã điền dữ liệu.\n'
          '4. Bấm “Load lên bảng” để đọc tệp ra bảng xem trước.\n'
          '5. Bấm “Validate” → hệ thống kiểm tra từng dòng, đánh dấu dòng hợp lệ / lỗi kèm lý do; '
          'dòng hợp lệ bị khóa không sửa được.\n'
          '6. Nếu còn dòng lỗi: sửa trực tiếp các dòng lỗi rồi Validate lại, hoặc bấm “Bỏ dòng lỗi” '
          'để loại các dòng lỗi khỏi bảng.\n'
          '7. Khi đã Validate và không còn dòng lỗi, nút Import mới bấm được. Bấm “Import” → hệ thống '
          'thêm các dòng, thông báo “Import thành công <n> hạng mục dự án”, đóng cửa sổ và nạp lại danh '
          'sách.',
    phu='• Chưa Validate, hoặc còn dòng lỗi → nút Import bị khóa, không bấm được.\n'
        '• Mọi dòng đều lỗi → sau khi bỏ dòng lỗi bảng không còn dòng nào, nút Import vẫn khóa; không '
        'import được.\n'
        '• Bấm “Bỏ dòng lỗi” → “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”\n'
        '• Bấm “Xoá trạng thái validate” → bỏ đánh dấu, mở khóa các dòng để sửa; phải Validate lại.\n'
        '• Dữ liệu thay đổi giữa lúc Validate và Import (vd người khác vừa tạo hạng mục trùng tên): còn ghi '
        'được một phần → “Import thành công x/y hạng mục dự án. z hạng mục dự án thất bại.”, đóng cửa sổ; không ghi '
        'được dòng nào → báo lỗi “Không có dữ liệu hợp lệ để import” (hoặc “Import thất bại: z/y hạng mục dự án không hợp lệ”, cửa sổ giữ nguyên.\n'
        '• Tệp quá 500 dòng → “Mỗi lần import tối đa 500 dòng (file đang có N dòng), vui lòng tách '
        'file và import nhiều lần.”\n'
        '• Bấm Làm mới → xóa dữ liệu đã nạp để chọn tệp khác.',
    dacbiet='Mỗi lần import tối đa 500 dòng. Mỗi dòng thêm thành công đều ghi 1 dòng lịch sử '
            '“Tạo mới”.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Import Excel', modal='Import Hạng mục dự án', shot=shot('09-import.png'),
         shot_caption='Cửa sổ Import Hạng mục dự án')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx / .xls', 'Có', 'Hiển thị', 'Chọn tệp cần import.'),
    ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải Mau_import_hangmucduan.xlsx.'),
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
    ('Cột STT', 'Text', 'Read-only', '–', '–', 'Theo tệp', '–'),
    ('Cột Tên hạng mục dự án', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo tệp',
     'Không trùng trong tệp và trong hệ thống.'),
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
     '– Tên trống → “Tên hạng mục dự án không được để trống”.\n'
     '– Tên quá 255 ký tự → “Tên hạng mục dự án vượt quá độ dài cho phép (tối đa 255 ký tự)”.\n'
     '– Tên trùng dòng khác trong tệp → “Tên hạng mục dự án bị trùng lặp trong file import (dòng '
     'n)”; trùng hệ thống → “Tên hạng mục dự án đã tồn tại trong hệ thống”.\n'
     '– Mô tả quá dài → “Mô tả vượt quá độ dài cho phép (tối đa 1000 ký tự)”.\n'
     'After:\n– Đánh dấu từng dòng hợp lệ / lỗi; thông báo “Validate thành công” hoặc “Validate xong: '
     'x hợp lệ, y không hợp lệ”.'),
    ('Bấm Import', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Nút chỉ bấm được khi đã Validate và không còn dòng lỗi.\n'
     'During:\n– Chỉ gửi các dòng hợp lệ trên bảng xem trước.\n'
     '– Máy chủ kiểm tra lại các dòng gửi lên như bước Validate.\n'
     'After:\n– Thêm mới các dòng với trạng thái Hoạt động; ghi lịch sử “Tạo mới” từng dòng.\n'
     '– Tất cả các dòng ghi được → thông báo “Import thành công <n> hạng mục dự án”, đóng cửa sổ, nạp lại '
     'danh sách.\n'
     '– Chỉ ghi được một phần (dữ liệu thay đổi giữa lúc Validate và Import, vd người khác vừa tạo hạng mục trùng tên) '
     '→ thông báo “Import thành công x/y hạng mục dự án. z hạng mục dự án thất bại.”, đóng cửa sổ, nạp lại '
     'danh sách.\n'
     '– Không ghi được dòng nào → báo lỗi “Không có dữ liệu hợp lệ để import” (hoặc “Import thất bại: z/y hạng mục dự án không hợp lệ”; cửa sổ giữ nguyên, không '
     'ghi dữ liệu.'),
    ('Bấm Bỏ dòng lỗi', 'Click',
     'Before:\n– Chưa Validate → “Hãy Validate trước rồi mới bỏ dòng lỗi.” và dừng xử lý.\n'
     'After:\n– Loại các dòng lỗi khỏi bảng xem trước; thông báo “Đã bỏ x dòng lỗi. Còn lại y dòng '
     'hợp lệ.”\n'
     '– Còn ≥ 1 dòng hợp lệ → nút Import mở cho bấm.'),
    ('Bấm Tải file mẫu', 'Click', 'After:\n– Tải tệp Mau_import_hangmucduan.xlsx.'),
])

# ---------------------------------------------------------------- 2.12
d.h3('2.12 Xuất Excel')
d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Xuất Excel danh sách hạng mục dự án', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-12 Xuất Excel')
d.p('2.12.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của '
           'Danh mục hạng mục dự án.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách hạng mục dự án',
    mota='Người dùng chọn các trường cần xuất rồi tải về tệp danh_sach_hang_muc_du_an.xlsx gồm TẤT '
         'CẢ hạng mục khớp bộ lọc đang áp dụng (không chỉ trang đang xem).',
    tacnhan='Người quản lý danh mục hạng mục dự án',
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
    ('Danh sách trường xuất', 'Table/Grid', 'Enable', '7 trường', 'Có (≥ 1)',
     'Tích sẵn các cột đang hiện trên bảng',
     'Tên hạng mục dự án, Mô tả, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. '
     'Kéo ⠿ để đổi thứ tự.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn nhanh.'),
    ('Dòng “Đang chọn x/7 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Tải tệp danh_sach_hang_muc_du_an.xlsx.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiện trên bảng.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Áp đúng bộ lọc đang dùng trên màn, lấy tất cả dòng khớp.\n'
     'After:\n– Tải tệp danh_sach_hang_muc_du_an.xlsx với các trường đã chọn theo thứ tự đã sắp.\n'
     '– Thông báo “Xuất Excel thành công”.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Danh mục hạng mục dự án; không lặp lại các '
           'quy tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Tên hạng mục dự án', [
        '– Bắt buộc, tối đa 255 ký tự, không trùng trong toàn hệ thống.',
        '– Danh mục không có mã: tên là định danh hiển thị ở danh sách, lịch sử và file xuất.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-02', 'Trạng thái mặc định', [
        '– Tạo mới mặc định Hoạt động; người dùng có thể chọn Khóa ngay khi tạo / sửa.',
        '– Import luôn tạo ở trạng thái Hoạt động.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-03', 'Chỉ sửa hạng mục đang Hoạt động', [
        '– Hạng mục đang Khóa không sửa được (nút Sửa bị ẩn, hệ thống cũng từ chối nếu gửi yêu cầu '
        'sửa); phải Mở khóa trước.',
    ], ['Chỉnh sửa', 'Danh sách']),
    ('BR-04', 'Khóa / Mở khóa', [
        '– Khóa chỉ áp dụng cho hạng mục đang Hoạt động; Mở khóa luôn được phép.',
        '– Khóa không xóa dữ liệu.',
    ], 'Khóa / Mở khóa'),
    ('BR-05', 'Xóa', [
        '– Xóa là xóa hẳn, không khôi phục được; hiện không có điều kiện chặn xóa.',
        '– Xóa nhiều thực hiện trọn gói: lỗi ở 1 bản ghi thì không bản ghi nào bị xóa.',
    ], ['Xóa', 'Xóa nhiều']),
    ('BR-06', 'Thao tác không dùng được thì ẩn', [
        '– Tạo mới, Import, Sửa, Xóa, Khóa / Mở khóa chỉ hiện với người có Q1 và đủ điều kiện '
        'nghiệp vụ; không hiển thị nút xám.',
    ], 'Danh sách'),
    ('BR-07', 'Ghi lịch sử thay đổi', [
        '– Ghi lại mọi lần Tạo mới (kể cả qua Import), Thay đổi thông tin, Thay đổi trạng thái, Xóa.',
        '– Cập nhật chỉ ghi các trường thực sự đổi: Tên, Mô tả, Trạng thái.',
        '– Ai vào được màn đều xem được lịch sử.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xóa', 'Khóa / Mở khóa', 'Import Excel', 'Xem lịch sử']),
    ('BR-08', 'Import chỉ thêm mới', [
        '– Mỗi lần tối đa 500 dòng.',
        '– Tên đã có trong hệ thống hoặc trùng nhau trong tệp → dòng lỗi, không ghi đè.',
        '– Chỉ các dòng hợp lệ được thêm; dòng lỗi được báo lý do cụ thể.',
    ], 'Import Excel'),
    ('BR-09', 'Xuất theo bộ lọc, chọn trường', [
        '– Chỉ người có Q1 được xuất.',
        '– Xuất tất cả dòng khớp bộ lọc đang áp dụng, không giới hạn theo trang.',
        '– Người dùng chọn trường và thứ tự trường; mặc định là các cột đang hiện trên bảng.',
    ], 'Xuất Excel'),
])

d.save(update_fields=False)

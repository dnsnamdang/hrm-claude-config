# -*- coding: utf-8 -*-
"""Sinh "SRS - Danh mục ứng dụng.docx" theo code nhánh gop_db — form 2026-09-24.

Chạy:  python3 .plans/gop-db/srs-danh-muc-du-an/ung-dung/gen_srs.py
Ảnh chụp thật (Playwright 1440x900, bản gop_db cổng 3002): ung-dung_shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/application/index.vue · components/modal/application-modal.vue
      components/assign-components/CascadePairSelect.vue · components/modal/CatalogHistoryModal.vue
      components/assign/SystemInfoSection.vue · store/optionsSelect.js
      components/subsystem-menu/presale.js (menu) · components/subsystems.js (phân hệ)
  BE  Modules/Assign/Routes/api.php (nhóm /assign/applications)
      Http/Requests/Applications/ApplicationsRequest.php
      Http/Controllers/Api/V1/ApplicationsController.php · Services/ApplicationService.php
      Entities/Applications.php (bảng applications) · Transformers/ApplicationsResource/*
      app/ExcelExport/ExportColumnRegistry.php ('applications')
      app/Http/Middleware/CheckImportRowLimit.php (500 dòng / lần import)
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 985, 1000)
Mẫu generator: .plans/gop-db/industry-group-list-page-standard/gen_srs.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
for _ in range(4):
    ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))

import srs_docx_lib as _lib  # noqa: E402
from srs_docx_lib import SrsDoc  # noqa: E402
from docx.opc.constants import RELATIONSHIP_TYPE as _RT  # noqa: E402
from docx.oxml.ns import qn as _qn  # noqa: E402

# python-docx 1.2 gộp các hyperlink cùng đích vào 1 relationship -> selfcheck đếm thiếu liên kết
# khi KHÔNG cho Word chạy (save(update_fields=False)). Tách mỗi đoạn "Quy tắc chung" 1 relationship
# riêng, ngay trong generator này (không sửa lib dùng chung).
_orig_add_hyperlink = _lib.add_hyperlink


def _add_hyperlink_unique(paragraph, url, text):
    link = _orig_add_hyperlink(paragraph, url, text)
    part = paragraph.part
    rels = part.rels
    old = link.get(_qn('r:id'))
    rid = rels._next_rId
    rels.add_relationship(_RT.HYPERLINK, url, rid, is_external=True)
    link.set(_qn('r:id'), rid)
    if not part.element.xpath('//*[@r:id="%s"]' % old):
        rels.pop(old)          # bỏ relationship mồ côi do relate_to() vừa tạo
    return link


_lib.add_hyperlink = _add_hyperlink_unique

OUT = os.path.join(HERE, 'SRS - Danh mục ứng dụng.docx')
SHOTS = os.path.join(HERE, 'ung-dung_shots')
MENU = 'Phân hệ CSKH trước bán => Danh mục => Ứng dụng'

A_QL = 'Người quản lý danh mục ứng dụng (Q1)'
A_XEM = 'Người xem danh mục ứng dụng (Q2)'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/application',
           full_url='https://<host-hrm>/assign/application', img_prefix='ungdung_gopdb_')

# Icon cho từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện.
# Dữ liệu local không có ứng dụng nào đang khóa -> đã TẠO bản ghi thử UD.T902 rồi Khóa qua API để
# chụp nút Mở khóa (không đổi DOM).
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ CSKH trước bán': 'phanhe', 'Danh mục': 'danhmuc', 'Ứng dụng': 'man',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidatboloc', 'Tuỳ chỉnh cột': 'tuychinhcot',
    'Tạo mới': 'taomoi', 'Sửa': 'sua', 'Xem chi tiết': 'xem', 'Xóa': 'xoa',
    'Chọn dòng': 'chondong', 'Xóa nhiều': 'xoanhieu',
    'Hành động khác': 'khac', 'Khóa': 'khoa', 'Mở khóa': 'mokhoa', 'Lịch sử': 'lichsu',
    'Import Excel': 'import', 'Xuất Excel': 'xuat',
}.items()})

d.title_block('Danh mục ứng dụng')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục ứng dụng thuộc phân hệ '
    'CSKH trước bán, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ cách ứng dụng được gắn theo CẶP Nhóm ngành : Nhóm giải pháp và CẶP Loại hình hoạt động '
    'khách hàng : Lĩnh vực kinh doanh khách hàng.',
    'Làm rõ ràng buộc giữa Ứng dụng với Dự án TKT (dữ liệu đang sử dụng ứng dụng) và điều kiện hiện '
    'các thao tác Sửa, Xóa, Xóa nhiều, Khóa, Mở khóa.',
    'Làm rõ quy tắc nhập dữ liệu hàng loạt và xuất dữ liệu ra tệp Excel.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Ứng dụng', 'Lĩnh vực ứng dụng cụ thể của giải pháp tại khách hàng (vd: Trạm kiểm định khí thải '
     'xe máy). Được chọn ở form Dự án TKT.'),
    ('Cặp Nhóm ngành : Nhóm giải pháp', 'Mỗi ứng dụng gắn ≥ 1 cặp; nhóm giải pháp trong cặp phải '
     'thuộc nhóm ngành của cặp. Hiển thị dạng “<Nhóm ngành> : <Nhóm giải pháp>”.'),
    ('Cặp Loại hình : Lĩnh vực', 'Cặp Loại hình hoạt động khách hàng : Lĩnh vực kinh doanh khách '
     'hàng; lĩnh vực trong cặp phải thuộc loại hình của cặp.'),
    ('Dự án TKT', 'Dự án khách hàng tiềm năng — dữ liệu đang sử dụng ứng dụng.'),
    ('Mã ứng dụng', 'Mã định danh dạng UD.XXXX: tiền tố “UD.” cố định + 4 ký tự do người dùng '
     'nhập. Không trùng trong toàn hệ thống.'),
    ('Trạng thái Khóa', 'Ứng dụng ngừng sử dụng: không được chọn ở các màn nghiệp vụ, không sửa '
     'được. Khóa KHÔNG xóa dữ liệu, có thể Mở khóa lại.'),
    ('Menu “…” (Hành động khác)', 'Nút ở cột Hành động chứa các thao tác phụ của dòng khi dòng có '
     'nhiều hơn 2 thao tác: Khóa / Mở khóa, Lịch sử.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý danh mục ứng dụng',
     'Xem danh sách, xem chi tiết, xem lịch sử; hiện nút Tạo mới, Import Excel; hiện các thao tác '
     'Sửa, Xóa, Khóa / Mở khóa trên dòng; được Xóa nhiều và Xuất Excel.'),
    ('Q2', 'Xem danh mục ứng dụng',
     'Xem danh sách, tìm kiếm, xem chi tiết và xem lịch sử. Không được thao tác thay đổi dữ liệu.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn hình không phân quyền theo cấp dữ liệu (công ty / phòng ban / bộ phận): người có quyền '
    'xem được toàn bộ ứng dụng của hệ thống. Mục menu Ứng dụng chỉ hiện với người có Q1 hoặc Q2.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách ứng dụng', '✅', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '❌'),
    ('FR-04 Tạo mới ứng dụng', '✅', '❌', '❌'),
    ('FR-05 Chỉnh sửa ứng dụng', '✅', '❌', '❌'),
    ('FR-06 Xem chi tiết ứng dụng', '✅', '✅', '❌'),
    ('FR-07 Xóa ứng dụng', '✅', '❌', '❌'),
    ('FR-08 Xóa nhiều ứng dụng', '✅', '❌', '❌'),
    ('FR-09 Khóa / Mở khóa ứng dụng', '✅', '❌', '❌'),
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
    [('FR-01', 'Xem danh sách ứng dụng', 'view'),
     ('FR-04', 'Tạo mới ứng dụng', 'crud'),
     ('FR-05', 'Chỉnh sửa ứng dụng', 'crud'),
     ('FR-07', 'Xóa ứng dụng', 'action'),
     ('FR-08', 'Xóa nhiều ứng dụng', 'action'),
     ('FR-09', 'Khóa / Mở khóa ứng dụng', 'action'),
     ('FR-11', 'Import Excel ứng dụng', 'io'),
     ('FR-12', 'Xuất Excel danh sách ứng dụng', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết ứng dụng', 'view', 'extend', [0], None),
     ('FR-10', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Danh mục ứng dụng')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách ứng dụng')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Danh mục ứng dụng tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách ứng dụng',
    mota='Hiển thị toàn bộ ứng dụng kèm Nhóm ngành, các cặp Nhóm ngành : Nhóm giải pháp, Loại hình '
         'hoạt động và các cặp Loại hình : Lĩnh vực kinh doanh khách hàng, người tạo / cập nhật, '
         'trạng thái và các thao tác trên từng dòng.',
    tacnhan='Người quản lý / người xem danh mục ứng dụng; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng vào menu Phân hệ CSKH trước bán → Danh mục → Ứng dụng.\n'
          '2. Hệ thống nạp trang 1, 10 dòng/trang, bản ghi mới tạo lên đầu.\n'
          '3. Bảng hiển thị đủ các cột (mặc định hiện hết cột), dòng “Hiển thị a–b / N” và thanh '
          'phân trang.',
    phu='• Vào màn từ số “Số ứng dụng” ở màn Nhóm ngành / Nhóm giải pháp → danh sách đã lọc sẵn theo '
        'nhóm ngành / nhóm giải pháp đó (thắng bộ lọc đã lưu lần trước).\n'
        '• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm Mã ứng dụng → mở cửa sổ Xem chi tiết (FR-06).\n'
        '• Bấm tiêu đề cột Mã, Tên, Ngày tạo, Ngày cập nhật → sắp xếp theo cột đó, bấm lại để '
        'đảo chiều.\n'
        '• Rời màn rồi quay lại trong vòng 10 phút → bộ lọc đang dùng được khôi phục.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách ứng dụng lúc mới truy cập')
d.figure(shot('07-menu-khac.png'), 'Cột Trạng thái, cột Hành động và menu “…” của một dòng',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Danh sách ứng dụng”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Dòng “Chưa chọn dòng nào.” / “Đã chọn n dòng”', 'Label', 'Hiển thị', '–', 'Chưa chọn dòng nào.',
     'Khi đã chọn dòng thì hiện kèm nút Xóa và Bỏ chọn (FR-08).'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1', 'Mở form Tạo mới (FR-04).'),
    ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1',
     'Mở cửa sổ Import (FR-11).'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Chọn trường xuất file (FR-12).'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Cột Chọn (ô tích)', 'Table/Grid', 'Enable / Disable', '–', 'Chưa tích',
     'Cố định bên trái. Ô tích ở tiêu đề chọn / bỏ chọn mọi dòng xóa được của trang. Dòng không xóa '
     'được (đã dùng ở Dự án TKT) thì ô tích bị khóa.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cố định bên trái khi cuộn ngang; không tắt được.'),
    ('Cột Mã ứng dụng', 'Table/Grid', 'Read-only', 'UD.XXXX', 'Theo dữ liệu',
     'Cố định bên trái, không tắt được, sắp xếp được. Là liên kết mở cửa sổ Xem chi tiết.'),
    ('Cột Tên ứng dụng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Sắp xếp được; tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Nhóm ngành', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tên các nhóm ngành của ứng dụng, ngăn cách bằng dấu phẩy.'),
    ('Cột Nhóm giải pháp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Các cặp “<Nhóm ngành> : <Nhóm giải pháp>”, ngăn cách bằng dấu phẩy.'),
    ('Cột Loại hình hoạt động khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tên các loại hình (không lặp).'),
    ('Cột Lĩnh vực kinh doanh khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Các cặp “<Loại hình> : <Lĩnh vực>”, ngăn cách bằng dấu phẩy.'),
    ('Cột Mô tả', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu',
     'Hoạt động màu xanh, Khóa màu đỏ. Rê chuột vào nhãn hiện lý do khi chưa khóa được (“Cần khóa '
     'hết các danh mục con trước khi khóa ứng dụng này”) hoặc chưa mở khóa được (“Cần mở khóa danh '
     'mục cấp cha trước khi thực hiện thao tác này”).'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu',
     'Không tắt được. Hiện tối đa 2 nút chính theo thứ tự Sửa, Xóa, Khóa / Mở khóa, Lịch sử; '
     'phần còn lại gom vào nút “…”. Thao tác không dùng được thì ẨN hẳn.'),
    ('Nút Sửa (bút)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và ứng dụng đang Hoạt động (FR-05).'),
    ('Nút Xóa (thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và ứng dụng chưa được dùng ở Dự án TKT nào (FR-07).'),
    ('Mục Khóa / Mở khóa', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1. Khóa ẩn khi ứng dụng đã được dùng ở Dự án TKT; Mở khóa ẩn khi có Nhóm giải '
     'pháp đang gắn bị khóa (FR-09).'),
    ('Mục Lịch sử', 'Button', 'Enable', '–', 'Hiển thị', 'Mọi người vào được màn đều thấy (FR-10).'),
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
     'During:\n– Khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu có); nếu đường dẫn có sẵn nhóm '
     'ngành / nhóm giải pháp thì áp điều kiện đó.\n'
     '– Nạp cấu hình cột đã lưu của người dùng.\n'
     'After:\n– Hiển thị trang 1, 10 dòng, bản ghi mới tạo lên đầu.'),
    ('Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click',
     'After:\n– Sắp xếp theo cột đó, bấm lại để đảo chiều; quay về trang 1.'),
    ('Bấm số trang / đổi Số dòng/trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu; đổi số dòng/trang thì quay về trang 1.'),
    ('Bấm Mã ứng dụng', 'Click', 'After:\n– Mở cửa sổ Xem chi tiết ứng dụng (FR-06).'),
    ('Bấm nút “…” ở cột Hành động', 'Click',
     'After:\n– Mở menu các thao tác còn lại của dòng (Khóa / Mở khóa, Lịch sử).'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Danh mục '
           'ứng dụng tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc ứng dụng',
    mota='Tìm nhanh theo mã, tên ứng dụng hoặc tên người tạo; lọc nâng cao theo nhóm ngành, nhóm '
         'giải pháp, loại hình hoạt động khách hàng, lĩnh vực kinh doanh khách hàng, trạng thái, '
         'người tạo, người cập nhật, khoảng ngày cập nhật.',
    tacnhan='Người quản lý / người xem danh mục ứng dụng; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách ứng dụng.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc (lần mở đầu tiên hệ thống mới nạp các danh '
          'mục cho ô chọn).\n'
          '3. Chọn giá trị ở các ô trong khối lọc: chọn xong hệ thống tự lọc lại ngay.\n'
          '4. Bảng hiển thị kết quả từ trang 1.',
    phu='• Đã chọn Nhóm ngành → ô Nhóm giải pháp chỉ liệt kê nhóm giải pháp thuộc nhóm ngành đó.\n'
        '• Đã chọn Loại hình hoạt động → ô Lĩnh vực kinh doanh chỉ liệt kê lĩnh vực thuộc loại hình '
        'đó; lĩnh vực đang chọn không thuộc loại hình mới thì tự bỏ chọn.\n'
        '• Bấm Làm mới → xóa hết điều kiện lọc và các dòng đang chọn, trả về danh sách ban đầu.\n'
        '• Bấm “Ẩn tìm kiếm nâng cao” → thu gọn khối lọc, điều kiện đang chọn vẫn giữ.\n'
        '• Không có kết quả → “Không có dữ liệu phù hợp bộ lọc.”',
    dacbiet=None)
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-bo-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Tìm gần đúng theo Mã, Tên ứng dụng hoặc tên Người tạo. Áp dụng khi bấm Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao (nhãn đổi thành “Ẩn tìm kiếm nâng cao” khi đang mở).'),
    ('Nhóm ngành', 'Dropdown', 'Enable', 'Nhóm ngành đang Hoạt động', 'Không', 'Trống',
     'Lọc ứng dụng có gắn nhóm ngành đã chọn.'),
    ('Nhóm giải pháp', 'Dropdown', 'Enable', 'Nhóm giải pháp đang Hoạt động (theo Nhóm ngành đã chọn)',
     'Không', 'Trống', 'Lọc ứng dụng có gắn nhóm giải pháp đã chọn.'),
    ('Loại hình hoạt động khách hàng', 'Dropdown', 'Enable', 'Loại hình đang Hoạt động', 'Không',
     'Trống', 'Lọc ứng dụng có cặp thuộc loại hình đã chọn.'),
    ('Lĩnh vực kinh doanh khách hàng', 'Dropdown', 'Enable', 'Lĩnh vực đang Hoạt động (theo Loại hình '
     'đã chọn)', 'Không', 'Trống', 'Lọc ứng dụng có cặp chứa lĩnh vực đã chọn.'),
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
    ('Đổi Loại hình hoạt động khách hàng', 'Change',
     'After:\n– Lĩnh vực đang chọn không thuộc loại hình mới → tự bỏ chọn Lĩnh vực; lọc lại.'),
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
    dieukien='Đang ở màn danh sách ứng dụng.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ với danh sách trường / cột, đánh dấu những mục đang hiện.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho người dùng, đóng cửa sổ và vẽ lại khối lọc / bảng.',
    phu='• Bấm “Khôi phục mặc định” → trả về bộ trường lọc mặc định của màn.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Cột Chọn, STT, Mã ứng dụng và Hành động luôn hiện, không bỏ tích được (hiển thị xám + '
        'ổ khóa).',
    dacbiet='Mặc định màn hiện TẤT CẢ cột; người dùng tự tắt bớt nếu thấy bảng quá rộng.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột', modal='Cài đặt bộ lọc và Tuỳ chỉnh cột',
         shot=shot('02b-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('02c-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột — cột khóa hiển thị xám', width_in=6.2)
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường lọc', 'Table/Grid', 'Enable', '8 trường', 'Không', 'Theo cấu hình đã lưu',
     'Nhóm ngành, Nhóm giải pháp, Loại hình hoạt động khách hàng, Lĩnh vực kinh doanh khách hàng, '
     'Trạng thái, Người tạo, Người cập nhật, Ngày cập nhật. Mỗi dòng: số thứ tự, biểu tượng kéo ⠿, '
     'ô tích, tên trường.'),
    ('Nút Lưu (Cài đặt bộ lọc)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình trường lọc.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về bộ trường lọc mặc định.'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '15 cột', 'Không', 'Theo cấu hình đã lưu',
     'Cột Chọn, STT, Mã ứng dụng, Hành động bị khóa (luôn hiện).'),
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
    ('Mã ứng dụng', 'Textbox', 'Enable', 'UD. + 4 ký tự', 'Có', 'Tiền tố “UD.” cố định',
     'Chỉ nhận chữ không dấu, chữ số và dấu gạch dưới; hệ thống lưu ở dạng chữ in hoa. Không trùng.'),
    ('Tên ứng dụng', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Không trùng; không chứa dấu phẩy (,) và dấu hai chấm (:). Icon ⓘ hiển thị mô tả trường.'),
    ('Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Không', 'Hoạt động',
     'Không có nút xóa chọn — luôn có giá trị.'),
    ('Nhóm ngành', 'Dropdown', 'Enable', 'Nhóm ngành đang Hoạt động', 'Có', 'Trống',
     'Chọn nhiều. Là ô cha của Nhóm giải pháp: chọn nhóm ngành trước để lọc danh sách Nhóm giải pháp.'),
    ('Nhóm giải pháp', 'Dropdown', 'Enable', 'Nhóm giải pháp đang Hoạt động thuộc Nhóm ngành đã chọn',
     'Có (≥ 1 cặp)', 'Trống',
     'Chọn nhiều; mỗi lựa chọn tạo 1 cặp “<Nhóm ngành> : <Nhóm giải pháp>” hiển thị thành 1 thẻ.'),
    ('Loại hình hoạt động khách hàng', 'Dropdown', 'Enable', 'Loại hình đang Hoạt động', 'Có', 'Trống',
     'Chọn nhiều. Là ô cha của Lĩnh vực kinh doanh khách hàng.'),
    ('Lĩnh vực kinh doanh khách hàng', 'Dropdown', 'Enable', 'Lĩnh vực đang Hoạt động thuộc Loại hình '
     'đã chọn', 'Có (≥ 1 cặp)', 'Trống',
     'Chọn nhiều; mỗi lựa chọn tạo 1 cặp “<Loại hình> : <Lĩnh vực>” hiển thị thành 1 thẻ.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Trống', 'Nội dung mô tả tự do.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ kèm biểu tượng cảnh báo ngay dưới ô bị lỗi.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
]
FE_CHECK = (
    '– Chưa có cặp Nhóm ngành : Nhóm giải pháp nào → “Vui lòng chọn ít nhất một nhóm giải pháp” dưới '
    '2 ô Nhóm ngành, Nhóm giải pháp.\n'
    '– Chưa có cặp Loại hình : Lĩnh vực nào → “Vui lòng chọn ít nhất một lĩnh vực kinh doanh” dưới 2 '
    'ô Loại hình hoạt động, Lĩnh vực kinh doanh.\n'
    '– Còn 1 trong 2 lỗi trên → thông báo “Bạn chưa nhập đầy đủ thông tin”, chưa gửi lên hệ thống.\n')
SAVE_DURING = (
    '– Mã ứng dụng trống (hoặc chỉ có tiền tố “UD.”) → “Bắt buộc phải nhập”.\n'
    '– Mã không đủ 4 ký tự sau “UD.” → “Vui lòng nhập 4 ký tự”.\n'
    '– Mã có ký tự không hợp lệ → “Chỉ cho phép: Chữ cái không dấu(A-Z, a-z), chữ số (0-9) và dấu '
    'gạch dưới (_).”\n'
    '– Mã đã tồn tại → “Đã tồn tại trên hệ thống”.\n'
    '– Tên ứng dụng trống → “Bắt buộc phải nhập”; trùng → “Đã tồn tại trên hệ thống”; quá 255 ký tự → '
    '“Vui lòng nhập tối đa 255 ký tự.”; chứa , hoặc : → “không được chứa ký tự dấu phẩy (,) và dấu '
    'hai chấm (:)”.\n'
    '– Nhóm giải pháp không thuộc nhóm ngành của cặp → “Nhóm giải pháp không thuộc Nhóm ngành đã '
    'chọn”.\n'
    '– Lĩnh vực không thuộc loại hình của cặp → “Lĩnh vực không thuộc Loại hình đã chọn”.\n'
    '– Nếu có lỗi validate → thông báo “Bạn chưa nhập đầy đủ thông tin” và không thực hiện bước After.')

d.h3('2.4 Tạo mới ứng dụng')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới ứng dụng', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-04 Tạo mới ứng dụng')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới ứng dụng',
    mota='Thêm một ứng dụng mới, gắn ≥ 1 cặp Nhóm ngành : Nhóm giải pháp và ≥ 1 cặp Loại hình hoạt '
         'động : Lĩnh vực kinh doanh khách hàng.',
    tacnhan='Người quản lý danh mục ứng dụng',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở cửa sổ “Thêm ứng dụng”, Trạng thái mặc định Hoạt động.\n'
          '3. Người dùng nhập Mã, Tên; chọn Nhóm ngành rồi Nhóm giải pháp; chọn Loại hình hoạt động '
          'rồi Lĩnh vực kinh doanh; nhập Mô tả (nếu có).\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống kiểm tra dữ liệu, ghi bản ghi mới cùng các cặp đã chọn và ghi 1 dòng lịch sử '
          '“Tạo mới”.\n'
          '6. Thông báo “Thêm mới thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Bấm “Lưu & Tiếp tục” → lưu xong giữ cửa sổ mở, xóa trắng form để nhập bản ghi tiếp.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới từng ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu đã nhập.\n'
        '• Có nhóm giải pháp đã chọn vừa bị khóa → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
        '• Lỗi khác → thông báo “Thêm mới thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Nút Lưu và Lưu & Tiếp tục bị khóa trong lúc đang xử lý để tránh tạo trùng. 2 cặp Nhóm '
            'giải pháp và Lĩnh vực kinh doanh được kiểm tra ngay trên màn trước khi gửi lên hệ thống.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', modal='Thêm ứng dụng', shot=shot('03-tao-moi.png'),
         shot_caption='Cửa sổ Thêm ứng dụng')
d.figure(shot('03b-tao-moi-loi.png'), 'Cửa sổ Thêm ứng dụng khi bấm Lưu mà chưa chọn các cặp bắt '
         'buộc', width_in=6.2)
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([('Tiêu đề “Thêm ứng dụng”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–')]
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
     'After:\n– Mở cửa sổ với form trống, Trạng thái = Hoạt động; nạp 4 danh mục Nhóm ngành, Nhóm '
     'giải pháp, Loại hình, Lĩnh vực đang Hoạt động.'),
    ('Chọn Nhóm ngành / Loại hình hoạt động', 'Change',
     'After:\n– Ô con (Nhóm giải pháp / Lĩnh vực kinh doanh) chỉ liệt kê mục thuộc các ô cha đã chọn.'),
    ('Bấm Lưu / Lưu & Tiếp tục', 'Click',
     'Before:\n' + FE_CHECK + '– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING + '\n'
     '– Có nhóm giải pháp đã chọn không còn Hoạt động → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'After:\n– Ghi bản ghi mới, mã chuyển sang chữ in hoa; lưu các cặp đã chọn; ghi người tạo, thời '
     'điểm tạo.\n'
     '– Ghi 1 dòng lịch sử “Tạo mới”.\n'
     '– Thông báo “Thêm mới thành công”, nạp lại danh sách.\n'
     '– Lưu: đóng cửa sổ. Lưu & Tiếp tục: giữ cửa sổ, xóa trắng form.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, không lưu dữ liệu đang nhập.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Chỉnh sửa ứng dụng')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa ứng dụng', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-05 Chỉnh sửa ứng dụng')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa). '
           'Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa ứng dụng',
    mota='Cập nhật thông tin và các cặp gắn của một ứng dụng đang Hoạt động.',
    tacnhan='Người quản lý danh mục ứng dụng',
    dieukien='Người dùng có quyền Q1; ứng dụng đang ở trạng thái Hoạt động.',
    chinh='1. Người dùng bấm nút Sửa trên dòng ứng dụng.\n'
          '2. Hệ thống mở cửa sổ “Sửa ứng dụng” với dữ liệu hiện tại.\n'
          '3. Người dùng sửa thông tin và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu, cập nhật bản ghi và các cặp, ghi 1 dòng lịch sử các trường '
          'đã đổi (giá trị cũ → giá trị mới).\n'
          '5. Thông báo “Cập nhật thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Ứng dụng đang Khóa → nút Sửa bị ẩn.\n'
        '• Nhóm ngành / Nhóm giải pháp / Loại hình / Lĩnh vực đang gắn nay đã bị khóa → vẫn hiển thị '
        'đúng tên (có biểu tượng 🔒) và vẫn lưu được nếu giữ nguyên; thêm mới thì chỉ chọn được mục '
        'Hoạt động.\n'
        '• Bản ghi đã bị xóa / khóa bởi người khác trong lúc sửa → “Dữ liệu đã thay đổi, vui lòng '
        'tải lại”.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin”.',
    dacbiet='Ứng dụng đã được dùng ở Dự án TKT thì không được đổi Mã và ô Trạng thái bị khóa.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', modal='Sửa ứng dụng', shot=shot('04-sua.png'),
         shot_caption='Cửa sổ Sửa ứng dụng')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Sửa ứng dụng”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Mã ứng dụng', 'Textbox', 'Enable', 'UD. + 4 ký tự', 'Có', 'Theo dữ liệu',
     'Như Tạo mới. Đã dùng ở Dự án TKT mà đổi mã → báo lỗi, không lưu.'),
    ('Tên ứng dụng', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo dữ liệu', 'Như Tạo mới.'),
    ('Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Không', 'Theo dữ liệu',
     'Bị khóa khi ứng dụng đã được dùng ở Dự án TKT.'),
    ('Nhóm ngành / Nhóm giải pháp', 'Dropdown', 'Enable', 'Mục đang Hoạt động + mục đang gắn', 'Có',
     'Theo dữ liệu', 'Mục đang gắn đã khóa vẫn hiển thị kèm 🔒.'),
    ('Loại hình hoạt động / Lĩnh vực kinh doanh khách hàng', 'Dropdown', 'Enable',
     'Mục đang Hoạt động + mục đang gắn', 'Có', 'Theo dữ liệu', 'Mục đang gắn đã khóa vẫn hiển thị kèm 🔒.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Theo dữ liệu', '–'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Không có nút Lưu & Tiếp tục.'),
    FORM_ROWS[-2], FORM_ROWS[-1],
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và ứng dụng đang Hoạt động.\n'
     'During:\n– Nạp chi tiết bản ghi, 4 danh mục đang Hoạt động và các mục đã khóa mà ứng dụng '
     'đang gắn.\n'
     '– Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ Sửa với dữ liệu hiện tại.'),
    ('Bấm Lưu', 'Click',
     'Before:\n' + FE_CHECK + '– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Ứng dụng không còn Hoạt động, hoặc chuyển sang Khóa khi đã được dùng ở Dự án TKT → “Dữ liệu '
     'đã thay đổi, vui lòng tải lại”.\n'
     'During:\n' + SAVE_DURING.replace(
         '– Nếu có lỗi validate',
         '– Đổi mã khi đã được dùng ở Dự án TKT → “Không thể sửa mã khi đã có dữ liệu phát sinh liên '
         'quan.”\n– Thêm nhóm giải pháp đã bị khóa → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
         '– Nếu có lỗi validate') + '\n'
     'After:\n– Cập nhật bản ghi, thay toàn bộ các cặp bằng các cặp mới; ghi người cập nhật, thời '
     'điểm cập nhật.\n'
     '– Ghi 1 dòng lịch sử các trường đã đổi (Mã, Tên, Mô tả, Trạng thái).\n'
     '– Thông báo “Cập nhật thành công”, đóng cửa sổ, nạp lại danh sách.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xem chi tiết ứng dụng')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết ứng dụng',
    mota='Xem toàn bộ thông tin và các cặp gắn của một ứng dụng ở chế độ chỉ đọc, kèm khối Lịch sử '
         'thay đổi.',
    tacnhan='Người quản lý / người xem danh mục ứng dụng',
    dieukien='Người dùng có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng bấm vào Mã ứng dụng trên bảng.\n'
          '2. Hệ thống mở cửa sổ “Xem ứng dụng”, mọi ô ở trạng thái chỉ đọc.\n'
          '3. (Tuỳ chọn) Người dùng bấm “Xem lịch sử” để mở rộng khối Lịch sử.\n'
          '4. Người dùng bấm Đóng để quay về danh sách.',
    phu='• Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.',
    dacbiet=None)
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', modal='Xem ứng dụng', shot=shot('05-xem.png'),
         shot_caption='Cửa sổ Xem ứng dụng')
d.figure(shot('05b-xem-lich-su.png'), 'Khối Lịch sử trong cửa sổ Xem ứng dụng đã mở rộng',
         width_in=6.2)
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xem ứng dụng”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Mã ứng dụng', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Tên ứng dụng', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Trạng thái', 'Dropdown', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu', '–'),
    ('Nhóm ngành / Nhóm giải pháp', 'Dropdown', 'Read-only', '–', 'Theo dữ liệu',
     'Các cặp đang gắn, mỗi cặp 1 thẻ; mục đã khóa vẫn hiển thị đúng tên kèm 🔒.'),
    ('Loại hình hoạt động / Lĩnh vực kinh doanh khách hàng', 'Dropdown', 'Read-only', '–',
     'Theo dữ liệu', 'Các cặp đang gắn, mỗi cặp 1 thẻ.'),
    ('Mô tả', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở danh sách thay đổi của bản ghi (như FR-10); có nút Làm mới, Thu gọn, '
     'Bộ lọc.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Không có nút Lưu.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Mã ứng dụng', 'Click',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'After:\n– Mở cửa sổ chi tiết ở chế độ chỉ đọc.'),
    ('Bấm “Xem lịch sử”', 'Click', 'After:\n– Mở rộng khối Lịch sử và nạp danh sách thay đổi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Xóa ứng dụng')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xóa ứng dụng', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-07 Xóa ứng dụng')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa ứng dụng',
    mota='Xóa hẳn một ứng dụng chưa được Dự án TKT nào sử dụng, kèm các cặp đang gắn.',
    tacnhan='Người quản lý danh mục ứng dụng',
    dieukien='Người dùng có quyền Q1; ứng dụng chưa được dùng ở Dự án TKT.',
    chinh='1. Người dùng bấm nút Xóa trên dòng ứng dụng.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận xóa”.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống xóa bản ghi và các cặp đang gắn, ghi 1 dòng lịch sử “Xóa”, thông báo “Xóa '
          'thành công” và nạp lại danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xóa.\n'
        '• Ứng dụng đã được dùng ở Dự án TKT → nút Xóa bị ẩn.\n'
        '• Bản ghi đã bị xóa trước đó → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
        '• Lỗi khác → “Xóa thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Xóa là xóa hẳn, không khôi phục được.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', modal='Xác nhận xóa', shot=shot('06-xoa.png'),
         shot_caption='Hộp thoại xác nhận xóa ứng dụng')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xác nhận xóa”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu', '“Bạn có chắc muốn xóa ứng dụng \'<tên>\'?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
], required=False, scope=False)
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và ứng dụng chưa được dùng ở Dự án TKT.\n'
     'After:\n– Hiện hộp thoại xác nhận.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'After:\n– Xóa bản ghi và các cặp đang gắn, ghi 1 dòng lịch sử “Xóa” kèm dữ liệu lúc xóa.\n'
     '– Thông báo “Xóa thành công”, nạp lại danh sách.'),
    ('Bấm Hủy / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Xóa nhiều ứng dụng')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Xóa nhiều ứng dụng', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-08 Xóa nhiều ứng dụng')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa nhiều ứng dụng',
    mota='Chọn nhiều dòng bằng ô tích ở cột Chọn rồi xóa cùng lúc các ứng dụng đã chọn.',
    tacnhan='Người quản lý danh mục ứng dụng',
    dieukien='Người dùng có quyền Q1; các ứng dụng được chọn đều chưa được dùng ở Dự án TKT.',
    chinh='1. Người dùng tích ô Chọn ở từng dòng (hoặc ô tích ở tiêu đề để chọn mọi dòng xóa được '
          'của trang).\n'
          '2. Phía trên bảng hiện “Đã chọn n dòng” kèm nút Xóa và Bỏ chọn.\n'
          '3. Người dùng bấm Xóa → hệ thống hiện hộp thoại “Xác nhận xóa nhiều”.\n'
          '4. Người dùng bấm Xóa.\n'
          '5. Hệ thống xóa toàn bộ ứng dụng đã chọn, ghi lịch sử “Xóa” cho từng bản ghi, thông báo '
          '“Xóa thành công n ứng dụng”, nạp lại danh sách.',
    phu='• Dòng đã được dùng ở Dự án TKT → ô tích bị khóa, không chọn được.\n'
        '• Bấm Bỏ chọn → bỏ toàn bộ dòng đang chọn.\n'
        '• Chuyển trang / lọc lại → các dòng đã chọn không còn trên trang sẽ tự bỏ chọn.\n'
        '• Có bản ghi không còn tồn tại → cả lượt xóa bị hủy, thông báo lỗi hệ thống trả về (hoặc '
        '“Lỗi khi xóa nhiều ứng dụng”).',
    dacbiet='Lượt xóa nhiều chạy trọn gói: một bản ghi lỗi thì không bản ghi nào bị xóa.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Chọn dòng => Xóa nhiều', modal='Xác nhận xóa nhiều',
         shot=shot('11-chon-nhieu.png'), shot_caption='Thanh thao tác khi đã chọn dòng')
d.figure(shot('11b-xoa-nhieu.png'), 'Hộp thoại xác nhận xóa nhiều ứng dụng', width_in=6.2)
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tích Chọn trên dòng / tiêu đề', 'Button', 'Enable / Disable', 'Chưa tích',
     'Dòng đã dùng ở Dự án TKT thì ô tích bị khóa.'),
    ('Dòng “Đã chọn n dòng”', 'Label', 'Hiển thị', 'Ẩn khi chưa chọn', 'n là số dòng đang chọn.'),
    ('Nút Xóa (đỏ)', 'Button', 'Enable', 'Ẩn khi chưa chọn', 'Mở hộp thoại xác nhận xóa nhiều.'),
    ('Nút Bỏ chọn', 'Button', 'Enable', 'Ẩn khi chưa chọn', 'Bỏ toàn bộ dòng đang chọn.'),
    ('Tiêu đề “Xác nhận xóa nhiều”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu', '“Bạn có chắc muốn xóa n ứng dụng đã chọn?”'),
    ('Nút Xóa / Hủy trong hộp thoại', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa / đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Tích / bỏ tích ô Chọn', 'Change',
     'After:\n– Cập nhật số dòng đang chọn; hiện / ẩn nút Xóa, Bỏ chọn.'),
    ('Bấm Xóa (thanh thao tác)', 'Click',
     'Before:\n– Chưa chọn dòng nào → “Vui lòng chọn ít nhất một ứng dụng để xóa”.\n'
     'After:\n– Hiện hộp thoại “Xác nhận xóa nhiều”.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Có bản ghi không còn tồn tại → dừng, không xóa bản ghi nào.\n'
     'After:\n– Xóa các ứng dụng đã chọn cùng các cặp đang gắn; ghi lịch sử “Xóa” từng bản ghi.\n'
     '– Thông báo “Xóa thành công n ứng dụng”, bỏ chọn, nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Khóa / Mở khóa ứng dụng')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Khóa / Mở khóa ứng dụng', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-09 Khóa / Mở khóa ứng dụng')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khóa / Mở khóa ứng dụng',
    mota='Chuyển trạng thái ứng dụng giữa Hoạt động và Khóa bằng thao tác Khóa / Mở khóa ở cột '
         'Hành động.',
    tacnhan='Người quản lý danh mục ứng dụng',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút “…” trên dòng, chọn Khóa (dòng đang Khóa thì bấm nút Mở khóa hiện '
          'sẵn trên dòng).\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khóa” (hoặc “Xác nhận mở khóa”).\n'
          '3. Người dùng bấm Khóa (hoặc Mở khóa).\n'
          '4. Hệ thống đổi trạng thái, ghi 1 dòng lịch sử nhóm “Thay đổi trạng thái”, thông báo '
          '“Khóa thành công” / “Mở khóa thành công”, nạp lại danh sách.',
    phu='• Ứng dụng đã được dùng ở Dự án TKT → mục Khóa bị ẩn; rê chuột vào nhãn trạng thái hiện '
        '“Cần khóa hết các danh mục con trước khi khóa ứng dụng này”.\n'
        '• Ứng dụng đang Khóa có Nhóm giải pháp đang gắn bị khóa (hoặc chưa gắn nhóm giải pháp nào) → '
        'mục Mở khóa bị ẩn; rê chuột vào nhãn hiện “Cần mở khóa danh mục cấp cha trước khi thực hiện '
        'thao tác này”.\n'
        '• Điều kiện thay đổi trong lúc xác nhận → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
        '• Bấm Hủy → không đổi trạng thái.',
    dacbiet='Ứng dụng đang Khóa không Sửa được cho tới khi Mở khóa.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Khóa / Mở khóa',
         modal='Xác nhận khóa / Xác nhận mở khóa',
         shot=shot('07b-khoa.png'), shot_caption='Hộp thoại xác nhận khóa ứng dụng')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Mục Khóa / Mở khóa', 'Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Đang Hoạt động: mục Khóa (ổ khóa đóng) trong menu “…”. Đang Khóa: nút Mở khóa (ổ khóa mở) '
     'hiện ngay trên dòng.'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khóa” / “Xác nhận mở khóa”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn khóa (mở khóa) ứng dụng \'<tên>\'?”'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Khóa / Mở khóa', 'Click',
     'Before:\n– Chỉ hiện với Q1; Khóa chỉ hiện khi ứng dụng chưa được dùng ở Dự án TKT; Mở khóa chỉ '
     'hiện khi ứng dụng có ≥ 1 nhóm giải pháp và mọi nhóm giải pháp đang gắn đều Hoạt động.\n'
     'After:\n– Hiện hộp thoại xác nhận tương ứng.'),
    ('Bấm Khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Ứng dụng đã được dùng ở Dự án TKT → “Dữ liệu đã thay đổi, vui lòng tải lại” và dừng '
     'xử lý.\n'
     'After:\n– Đổi trạng thái sang Khóa, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng thái”.\n'
     '– Thông báo “Khóa thành công”, nạp lại danh sách.'),
    ('Bấm Mở khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Có nhóm giải pháp đang gắn bị khóa → “Dữ liệu đã thay đổi, vui lòng tải lại” và dừng '
     'xử lý.\n'
     'After:\n– Đổi trạng thái sang Hoạt động, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng '
     'thái”.\n– Thông báo “Mở khóa thành công”, nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.10
d.h3('2.10 Xem lịch sử thay đổi')
d.p('2.10.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung thông tin riêng của Danh mục '
           'ứng dụng.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của ứng dụng',
    mota='Xem các lần Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Xóa của một ứng dụng: ai '
         'làm, lúc nào, trường nào đổi từ giá trị cũ sang giá trị mới.',
    tacnhan='Người quản lý / người xem danh mục ứng dụng',
    dieukien='Người dùng vào được màn danh sách (Q1 hoặc Q2). Lịch sử không gắn quyền riêng.',
    chinh='1. Người dùng bấm “…” trên dòng rồi chọn Lịch sử (hoặc bấm nút Lịch sử nếu đang hiện '
          'sẵn trên dòng).\n'
          '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <mã> - <tên>” và nạp danh sách thay đổi, mới nhất '
          'lên đầu.\n'
          '3. (Tuỳ chọn) Bấm Bộ lọc để lọc theo loại hành động, người thực hiện, khoảng ngày.\n'
          '4. Người dùng bấm Đóng.',
    phu='• Chưa có thay đổi nào → hiển thị “Chưa có lịch sử thao tác nào.”\n'
        '• Lọc không ra kết quả → “Không có lịch sử phù hợp bộ lọc.”',
    dacbiet=None)
d.p('2.10.2 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Lịch sử', modal='Lịch sử thay đổi',
         shot=shot('08-lich-su.png'), shot_caption='Cửa sổ Lịch sử thay đổi của ứng dụng')
d.p('2.10.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Lịch sử thay đổi: <mã> - <tên>”.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở các ô lọc: loại hành động, người thực hiện, Từ ngày, Đến ngày.'),
    ('Danh sách thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi lần thay đổi: thời điểm, nhóm hành động, người thực hiện kèm phòng ban, các trường đổi '
     '(Mã, Tên, Mô tả, Trạng thái) với giá trị cũ (đỏ) → giá trị mới (xanh).'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thao tác nào.”'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)
d.p('2.10.4 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Lịch sử', 'Click', 'After:\n– Mở cửa sổ và nạp danh sách thay đổi của bản ghi.'),
    ('Đổi giá trị trong Bộ lọc', 'Change', 'After:\n– Lọc lại danh sách thay đổi ngay.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.11
d.h3('2.11 Import Excel')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Import Excel ứng dụng', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-11 Import Excel ứng dụng')
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc Import file, Validate dữ liệu và Thông báo.', anchor='excel')
d.intro_table(
    ten='Import Excel ứng dụng',
    mota='Nhập hàng loạt ứng dụng từ tệp Excel theo file mẫu: mã chưa có thì thêm mới, mã đã có (và '
         'chưa được dùng ở Dự án TKT) thì cập nhật theo tệp.',
    tacnhan='Người quản lý danh mục ứng dụng',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm Import Excel.\n'
          '2. (Tuỳ chọn) Bấm “Tải file mẫu” để lấy tệp Mau_Import_UngDung_FN.xlsx.\n'
          '3. Bấm “Chọn file Excel”, chọn tệp đã điền dữ liệu.\n'
          '4. Bấm “Load lên bảng” để đọc tệp ra bảng xem trước.\n'
          '5. Bấm “Validate” → hệ thống kiểm tra từng dòng, đánh dấu dòng hợp lệ / lỗi kèm lý do; '
          'dòng hợp lệ bị khóa không sửa được.\n'
          '6. Nếu còn dòng lỗi: sửa trực tiếp các dòng lỗi rồi Validate lại, hoặc bấm “Bỏ dòng lỗi” '
          'để loại các dòng lỗi khỏi bảng.\n'
          '7. Khi đã Validate và không còn dòng lỗi, nút Import mới bấm được. Bấm “Import” → hệ thống '
          'ghi các dòng, thông báo “Import thành công <n> ứng dụng”, đóng cửa sổ và nạp lại danh '
          'sách.',
    phu='• Chưa Validate, hoặc còn dòng lỗi → nút Import bị khóa, không bấm được.\n'
        '• Mọi dòng đều lỗi → sau khi bỏ dòng lỗi bảng không còn dòng nào, nút Import vẫn khóa; không '
        'import được.\n'
        '• Bấm “Bỏ dòng lỗi” → “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”\n'
        '• Bấm “Xoá trạng thái validate” → bỏ đánh dấu, mở khóa các dòng để sửa; phải Validate lại.\n'
        '• Dữ liệu thay đổi giữa lúc Validate và Import (vd người khác vừa tạo ứng dụng trùng tên): còn ghi '
        'được một phần → “Import thành công x/y ứng dụng. z ứng dụng thất bại.”, đóng cửa sổ; không ghi '
        'được dòng nào → báo lỗi “Import thất bại”, cửa sổ giữ nguyên.\n'
        '• Tệp quá 500 dòng → “Mỗi lần import tối đa 500 dòng (file đang có N dòng), vui lòng tách '
        'file và import nhiều lần.”\n'
        '• Bật “Chỉ dòng lỗi” để lọc bảng xem trước chỉ còn dòng lỗi.\n'
        '• Bấm Làm mới → xóa dữ liệu đã nạp để chọn tệp khác.',
    dacbiet='Mỗi lần import tối đa 500 dòng. Dòng thêm mới ghi lịch sử “Tạo mới”, dòng cập nhật ghi '
            'lịch sử các trường đã đổi.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Import Excel', modal='Import Ứng dụng', shot=shot('09-import.png'),
         shot_caption='Cửa sổ Import Ứng dụng')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx / .xls', 'Có', 'Hiển thị', 'Chọn tệp cần import.'),
    ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải Mau_Import_UngDung_FN.xlsx.'),
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
    ('Công tắc Chỉ dòng lỗi', 'Button', 'Enable', '–', '–', 'Tắt', 'Lọc bảng chỉ còn dòng lỗi.'),
    ('Cột Mã ứng dụng', 'Textbox', 'Enable', 'Tối đa 7 ký tự', 'Có', 'Theo tệp',
     'Chỉ chữ không dấu, chữ số, dấu gạch dưới, dấu chấm.'),
    ('Cột Tên ứng dụng', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo tệp',
     'Không trùng với ứng dụng khác; không chứa , và :.'),
    ('Cột Nhóm giải pháp', 'Textbox', 'Enable', 'MãNhómNgành:MãNhómGiảiPháp', 'Có', 'Theo tệp',
     'Một hoặc nhiều cặp ngăn nhau bằng dấu phẩy, vd “NN.KH02:NGP.0119, NN.KH01:NGP.0117”.'),
    ('Cột Lĩnh vực kinh doanh khách hàng', 'Textbox', 'Enable', 'MãLoạiHình:MãLĩnhVực', 'Không',
     'Theo tệp', 'Một hoặc nhiều cặp ngăn nhau bằng dấu phẩy, vd “LHHDKH.0001:LVKDKH.OTO1”.'),
    ('Cột Trạng thái Ứng dụng', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Có', 'Theo tệp',
     'Gửi lên hệ thống dạng active / inactive.'),
    ('Cột Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Theo tệp', '–'),
    ('Dòng Tổng / hợp lệ / lỗi', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', 'Thống kê sau Validate.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không import.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa dữ liệu đã nạp.'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Validate', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Tệp quá 500 dòng → báo “Mỗi lần import tối đa 500 dòng …” và dừng xử lý.\n'
     '– Trên màn: cặp sai cấu trúc → “Nhóm giải pháp sai định dạng (cần MãNhómNgành:MãNhómGiảiPháp): '
     '<cặp>” / “Lĩnh vực kinh doanh khách hàng sai định dạng (cần MãLoạiHình:MãLĩnhVực): <cặp>”.\n'
     'During (từng dòng):\n'
     '– Thiếu dữ liệu → “Mã ứng dụng là bắt buộc”, “Tên ứng dụng là bắt buộc”, “Nhóm giải pháp là bắt '
     'buộc”, “Trạng thái là bắt buộc”.\n'
     '– Mã có ký tự không hợp lệ → “Chỉ cho phép: Chữ cái không dấu(A-Z, a-z), chữ số (0-9) và dấu '
     'gạch dưới (_).”; quá dài → “Mã ứng dụng tối đa 7 ký tự”.\n'
     '– Tên quá dài → “Tên ứng dụng tối đa 255 ký tự”; chứa , hoặc : → “không được chứa ký tự dấu phẩy '
     '(,) và dấu hai chấm (:)”; trùng ứng dụng khác → “Tên ứng dụng đã tồn tại”.\n'
     '– Trạng thái sai → “Trạng thái chỉ nhận active/inactive”.\n'
     '– Mã trong cặp không có hoặc đã khóa → “Mã Nhóm ngành \"<mã>\" và Nhóm giải pháp \"<mã>\" không '
     'tồn tại hoặc đang bị khoá” (tương tự với Loại hình / Lĩnh vực).\n'
     '– Nhóm giải pháp không thuộc nhóm ngành → “Nhóm giải pháp \"<mã>\" không thuộc Nhóm ngành '
     '\"<mã>\"”; lĩnh vực không thuộc loại hình → “Lĩnh vực \"<mã>\" không thuộc Loại hình \"<mã>\"”.\n'
     '– Mã đã có và ứng dụng đó đã được dùng ở Dự án TKT → “Không thể sửa mã khi đã có dữ liệu ứng '
     'dụng liên quan.”\n'
     'After:\n– Đánh dấu từng dòng hợp lệ / lỗi; thông báo “Validate thành công” hoặc “Validate xong: '
     'x hợp lệ, y không hợp lệ. (Dòng hợp lệ đã bị khoá)”.'),
    ('Bấm Import', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Nút chỉ bấm được khi đã Validate và không còn dòng lỗi.\n'
     'During:\n– Chỉ gửi các dòng hợp lệ trên bảng xem trước.\n'
     '– Máy chủ kiểm tra lại các dòng gửi lên như bước Validate.\n'
     'After:\n– Mã chưa có → thêm mới (mã chuyển chữ in hoa), ghi lịch sử “Tạo mới”.\n'
     '– Mã đã có → cập nhật tên, mô tả, trạng thái và thay toàn bộ các cặp theo tệp, ghi lịch sử '
     'các trường đã đổi.\n'
     '– Tất cả các dòng ghi được → thông báo “Import thành công <n> ứng dụng”, đóng cửa sổ, nạp lại '
     'danh sách.\n'
     '– Chỉ ghi được một phần (dữ liệu thay đổi giữa lúc Validate và Import, vd người khác vừa tạo ứng dụng trùng tên) '
     '→ thông báo “Import thành công x/y ứng dụng. z ứng dụng thất bại.”, đóng cửa sổ, nạp lại '
     'danh sách.\n'
     '– Không ghi được dòng nào → báo lỗi “Import thất bại”; cửa sổ giữ nguyên, không '
     'ghi dữ liệu.'),
    ('Bấm Bỏ dòng lỗi', 'Click',
     'Before:\n– Chưa Validate → “Hãy Validate trước rồi mới bỏ dòng lỗi.” và dừng xử lý.\n'
     'After:\n– Loại các dòng lỗi khỏi bảng xem trước; thông báo “Đã bỏ x dòng lỗi. Còn lại y dòng '
     'hợp lệ.”\n'
     '– Còn ≥ 1 dòng hợp lệ → nút Import mở cho bấm.'),
    ('Bấm Tải file mẫu', 'Click', 'After:\n– Tải tệp Mau_Import_UngDung_FN.xlsx.'),
])

# ---------------------------------------------------------------- 2.12
d.h3('2.12 Xuất Excel')
d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Xuất Excel danh sách ứng dụng', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-12 Xuất Excel')
d.p('2.12.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của '
           'Danh mục ứng dụng.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách ứng dụng',
    mota='Người dùng chọn các trường cần xuất rồi tải về tệp danh_sach_ung_dung.xlsx gồm TẤT CẢ ứng '
         'dụng khớp bộ lọc đang áp dụng (không chỉ trang đang xem).',
    tacnhan='Người quản lý danh mục ứng dụng',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng (tuỳ chọn) đặt bộ lọc trên màn danh sách.\n'
          '2. Bấm Xuất Excel.\n'
          '3. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiện trên bảng.\n'
          '4. Người dùng tích / bỏ tích, kéo để đổi thứ tự trường, rồi bấm Xuất file.\n'
          '5. Hệ thống dựng tệp theo bộ lọc, trình duyệt tải tệp về, thông báo “Xuất Excel thành công”.',
    phu='• Bấm “Chọn tất cả” / “Bỏ chọn hết” để chọn nhanh.\n'
        '• Lỗi khi dựng tệp → thông báo “Lỗi khi xuất Excel”.',
    dacbiet='Nút Xuất Excel bị khóa trong lúc đang xuất để tránh bấm lặp.')
d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất file',
         shot=shot('10-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất file')
d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường xuất', 'Table/Grid', 'Enable', '12 trường', 'Có (≥ 1)',
     'Tích sẵn các cột đang hiện trên bảng',
     'Mã ứng dụng, Tên ứng dụng, Nhóm ngành, Nhóm giải pháp, Loại hình hoạt động khách hàng, Lĩnh '
     'vực kinh doanh khách hàng, Mô tả, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập '
     'nhật. Kéo ☰ để đổi thứ tự.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn nhanh.'),
    ('Dòng “Đang chọn x/12 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Tải tệp danh_sach_ung_dung.xlsx.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiện trên bảng.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Áp đúng bộ lọc đang dùng trên màn, lấy tất cả dòng khớp.\n'
     'After:\n– Tải tệp danh_sach_ung_dung.xlsx với các trường đã chọn theo thứ tự đã sắp.\n'
     '– Thông báo “Xuất Excel thành công”.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Danh mục ứng dụng; không lặp lại các quy '
           'tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Định dạng và tính duy nhất của Mã', [
        '– Mã = tiền tố “UD.” + đúng 4 ký tự gồm chữ không dấu, chữ số, dấu gạch dưới.',
        '– Hệ thống lưu mã ở dạng chữ in hoa; không trùng trong toàn hệ thống.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-02', 'Tên ứng dụng', [
        '– Bắt buộc, tối đa 255 ký tự, không trùng.',
        '– Không chứa dấu phẩy (,) và dấu hai chấm (:).',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-03', 'Cặp Nhóm ngành : Nhóm giải pháp', [
        '– Mỗi ứng dụng bắt buộc có ≥ 1 cặp; nhóm giải pháp trong cặp phải thuộc nhóm ngành của cặp.',
        '– Nhóm ngành của ứng dụng lấy từ các cặp (không chọn riêng).',
        '– Chỉ thêm được nhóm ngành / nhóm giải pháp đang Hoạt động; mục đã khóa mà ứng dụng đang gắn '
        'vẫn hiển thị (🔒) và được giữ nguyên khi lưu.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-04', 'Cặp Loại hình : Lĩnh vực kinh doanh khách hàng', [
        '– Form Tạo mới / Sửa: bắt buộc ≥ 1 cặp; lĩnh vực trong cặp phải thuộc loại hình của cặp.',
        '– Import Excel: cột này không bắt buộc; có nhập thì phải đúng cặp.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-05', 'Ràng buộc khi đã dùng ở Dự án TKT', [
        '– Ứng dụng đã được chọn ở Dự án TKT thì: không đổi được Mã, không Xóa được (ô tích xóa nhiều '
        'bị khóa), không Khóa được (kể cả đổi Trạng thái trong form Sửa).',
    ], ['Chỉnh sửa', 'Xóa', 'Xóa nhiều', 'Khóa / Mở khóa', 'Import Excel']),
    ('BR-06', 'Chỉ sửa ứng dụng đang Hoạt động',
     '– Ứng dụng đang Khóa không sửa được (nút Sửa bị ẩn); phải Mở khóa trước.',
     ['Chỉnh sửa', 'Danh sách']),
    ('BR-07', 'Điều kiện Mở khóa',
     '– Chỉ Mở khóa được khi ứng dụng có ≥ 1 nhóm giải pháp và mọi nhóm giải pháp đang gắn đều Hoạt '
     'động.',
     'Khóa / Mở khóa'),
    ('BR-08', 'Thao tác không dùng được thì ẩn', [
        '– Sửa, Xóa, Khóa / Mở khóa chỉ hiện với người có Q1 VÀ đủ điều kiện nghiệp vụ.',
        '– Không hiển thị nút xám; lý do chưa khóa / mở khóa được ghi ở nhãn Trạng thái khi rê chuột.',
    ], 'Danh sách'),
    ('BR-09', 'Xóa nhiều chạy trọn gói',
     '– Xóa nhiều chỉ chọn được dòng xóa được; một bản ghi lỗi thì cả lượt không xóa bản ghi nào.',
     'Xóa nhiều'),
    ('BR-10', 'Ghi lịch sử thay đổi', [
        '– Ghi lại mọi lần Tạo mới, Thay đổi thông tin (kể cả qua Import), Thay đổi trạng thái, Xóa '
        '(kể cả Xóa nhiều).',
        '– Thay đổi thông tin chỉ ghi các trường thực sự đổi: Mã, Tên, Mô tả, Trạng thái.',
        '– Ai vào được màn đều xem được lịch sử.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xóa', 'Xóa nhiều', 'Khóa / Mở khóa', 'Import Excel', 'Xem lịch sử']),
    ('BR-11', 'Import thêm mới hoặc cập nhật theo Mã', [
        '– Mỗi lần tối đa 500 dòng.',
        '– Mã chưa có → thêm mới; mã đã có và chưa dùng ở Dự án TKT → cập nhật theo tệp (thay toàn bộ '
        'các cặp).',
        '– Chỉ các dòng hợp lệ được ghi; dòng lỗi được báo lý do cụ thể.',
    ], 'Import Excel'),
    ('BR-12', 'Xuất theo bộ lọc, chọn trường', [
        '– Xuất tất cả dòng khớp bộ lọc đang áp dụng, không giới hạn theo trang.',
        '– Người dùng chọn trường và thứ tự trường; mặc định là các cột đang hiện trên bảng.',
    ], 'Xuất Excel'),
])

d.save(update_fields=False)

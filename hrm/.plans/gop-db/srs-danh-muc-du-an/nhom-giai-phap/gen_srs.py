# -*- coding: utf-8 -*-
"""Sinh "SRS - Danh mục nhóm giải pháp.docx" theo code nhánh gop_db — form 2026-09-24.

Chạy:  python3 .plans/gop-db/srs-danh-muc-du-an/nhom-giai-phap/gen_srs.py
Ảnh chụp thật (Playwright 1440x900, bản gop_db cổng 3002): nhom-giai-phap_shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/solution-groups/index.vue · components/modal/industry-modal.vue
      components/modal/CatalogHistoryModal.vue · components/assign/SystemInfoSection.vue
      components/subsystem-menu/presale.js (menu) · components/subsystems.js (phân hệ)
  BE  Modules/Assign/Routes/api.php (nhóm /assign/industries)
      Http/Requests/Industries/IndustriesRequest.php · Http/Controllers/Api/V1/IndustriesController.php
      Services/IndustriesService.php · Entities/Industries.php (bảng industries)
      Transformers/IndustriesResource/* · app/ExcelExport/ExportColumnRegistry.php ('industries')
      app/Http/Middleware/CheckImportRowLimit.php (500 dòng / lần import)
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 984, 999)
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

OUT = os.path.join(HERE, 'SRS - Danh mục nhóm giải pháp.docx')
SHOTS = os.path.join(HERE, 'nhom-giai-phap_shots')
MENU = 'Phân hệ CSKH trước bán => Danh mục => Nhóm giải pháp'

A_QL = 'Người quản lý danh mục nhóm giải pháp (Q1)'
A_XEM = 'Người xem danh mục nhóm giải pháp (Q2)'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/solution-groups',
           full_url='https://<host-hrm>/assign/solution-groups', img_prefix='nhomgiaiphap_gopdb_')

# Icon cho từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện.
# Dữ liệu local không có nhóm giải pháp nào đang khóa -> đã TẠO bản ghi thử NGP.T902 rồi Khóa
# qua API để chụp nút Mở khóa (không đổi DOM).
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ CSKH trước bán': 'phanhe', 'Danh mục': 'danhmuc', 'Nhóm giải pháp': 'man',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidatboloc', 'Tuỳ chỉnh cột': 'tuychinhcot',
    'Tạo mới': 'taomoi', 'Sửa': 'sua', 'Xem chi tiết': 'xem', 'Xóa': 'xoa',
    'Hành động khác': 'khac', 'Khóa': 'khoa', 'Mở khóa': 'mokhoa', 'Lịch sử': 'lichsu',
    'Import Excel': 'import', 'Xuất Excel': 'xuat',
}.items()})

d.title_block('Danh mục nhóm giải pháp')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục nhóm giải pháp thuộc phân hệ '
    'CSKH trước bán, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ ràng buộc giữa Nhóm giải pháp với Nhóm ngành (danh mục cha, một nhóm giải pháp gắn '
    'được nhiều nhóm ngành) và với Ứng dụng (dữ liệu con đang tham chiếu tới nhóm giải pháp).',
    'Làm rõ điều kiện hiện các thao tác Sửa, Xóa, Khóa, Mở khóa trên từng dòng.',
    'Làm rõ quy tắc nhập dữ liệu hàng loạt và xuất dữ liệu ra tệp Excel.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Nhóm giải pháp', 'Nhóm các giải pháp kỹ thuật/công nghệ mà công ty cung cấp cho khách hàng. '
     'Mỗi nhóm giải pháp gắn với một hoặc nhiều Nhóm ngành.'),
    ('Nhóm ngành', 'Danh mục cha của Nhóm giải pháp (màn Danh mục nhóm ngành).'),
    ('Ứng dụng', 'Danh mục con: mỗi ứng dụng khai báo các cặp Nhóm ngành : Nhóm giải pháp. Cột “Số '
     'ứng dụng” đếm số ứng dụng đang gắn với nhóm giải pháp.'),
    ('Mã nhóm giải pháp', 'Mã định danh dạng NGP.XXXX: tiền tố “NGP.” cố định + 4 ký tự do người '
     'dùng nhập. Không trùng trong toàn hệ thống.'),
    ('Trạng thái Khóa', 'Nhóm giải pháp ngừng sử dụng: không được chọn ở các màn nghiệp vụ, không '
     'sửa được. Khóa KHÔNG xóa dữ liệu, có thể Mở khóa lại.'),
    ('Dữ liệu liên kết', 'Ứng dụng đang tham chiếu tới nhóm giải pháp.'),
    ('Menu “…” (Hành động khác)', 'Nút ở cột Hành động chứa các thao tác phụ của dòng khi dòng có '
     'nhiều hơn 2 thao tác: Khóa / Mở khóa, Lịch sử.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý danh mục nhóm giải pháp',
     'Xem danh sách, xem chi tiết, xem lịch sử; hiện nút Tạo mới, Import Excel; hiện các thao tác '
     'Sửa, Xóa, Khóa / Mở khóa trên dòng; được Xuất Excel.'),
    ('Q2', 'Xem danh mục nhóm giải pháp',
     'Xem danh sách, tìm kiếm, xem chi tiết và xem lịch sử. Không hiện thao tác thay đổi dữ liệu.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn hình không phân quyền theo cấp dữ liệu (công ty / phòng ban / bộ phận): người có quyền '
    'xem được toàn bộ nhóm giải pháp của hệ thống. Mục menu Nhóm giải pháp chỉ hiện với người có Q1 '
    'hoặc Q2.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách nhóm giải pháp', '✅', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '❌'),
    ('FR-04 Tạo mới nhóm giải pháp', '✅', '❌', '❌'),
    ('FR-05 Chỉnh sửa nhóm giải pháp', '✅', '❌', '❌'),
    ('FR-06 Xem chi tiết nhóm giải pháp', '✅', '✅', '❌'),
    ('FR-07 Xóa nhóm giải pháp', '✅', '❌', '❌'),
    ('FR-08 Khóa / Mở khóa nhóm giải pháp', '✅', '❌', '❌'),
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
    [('FR-01', 'Xem danh sách nhóm giải pháp', 'view'),
     ('FR-04', 'Tạo mới nhóm giải pháp', 'crud'),
     ('FR-05', 'Chỉnh sửa nhóm giải pháp', 'crud'),
     ('FR-07', 'Xóa nhóm giải pháp', 'action'),
     ('FR-08', 'Khóa / Mở khóa nhóm giải pháp', 'action'),
     ('FR-10', 'Import Excel nhóm giải pháp', 'io'),
     ('FR-11', 'Xuất Excel danh sách nhóm giải pháp', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết nhóm giải pháp', 'view', 'extend', [0], None),
     ('FR-09', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Danh mục nhóm giải pháp')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách nhóm giải pháp')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Danh mục nhóm giải pháp tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách nhóm giải pháp',
    mota='Hiển thị toàn bộ nhóm giải pháp kèm các Nhóm ngành đang gắn, số ứng dụng đang liên kết, '
         'người tạo / cập nhật, trạng thái và các thao tác trên từng dòng.',
    tacnhan='Người quản lý / người xem danh mục nhóm giải pháp; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng vào menu Phân hệ CSKH trước bán → Danh mục → Nhóm giải pháp.\n'
          '2. Hệ thống nạp trang 1, 10 dòng/trang, bản ghi mới tạo lên đầu.\n'
          '3. Bảng hiển thị đủ các cột (mặc định hiện hết cột), dòng “Hiển thị a–b / N” và thanh '
          'phân trang.',
    phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm Mã nhóm giải pháp → mở cửa sổ Xem chi tiết (FR-06).\n'
        '• Bấm số ở cột Số ứng dụng (khác 0) → chuyển tới danh sách Ứng dụng đã lọc sẵn theo nhóm '
        'giải pháp đó.\n'
        '• Bấm tiêu đề cột Mã, Tên, Ngày tạo, Ngày cập nhật → sắp xếp theo cột đó, bấm lại để '
        'đảo chiều.\n'
        '• Rời màn rồi quay lại trong vòng 10 phút → bộ lọc đang dùng được khôi phục.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách nhóm giải pháp lúc mới truy cập')
d.figure(shot('07-menu-khac.png'), 'Cột Trạng thái, cột Hành động và menu “…” của một dòng',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Danh sách nhóm giải pháp”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1', 'Mở form Tạo mới (FR-04).'),
    ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1',
     'Mở cửa sổ Import (FR-10).'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Chọn trường xuất file (FR-11).'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cố định bên trái khi cuộn ngang; không tắt được.'),
    ('Cột Mã nhóm giải pháp', 'Table/Grid', 'Read-only', 'NGP.XXXX', 'Theo dữ liệu',
     'Cố định bên trái, không tắt được, sắp xếp được. Là liên kết mở cửa sổ Xem chi tiết.'),
    ('Cột Tên nhóm giải pháp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Sắp xếp được; tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Nhóm ngành', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tên các nhóm ngành đang gắn, ngăn cách bằng dấu phẩy.'),
    ('Cột Số ứng dụng', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Căn phải. Khác 0 thì là liên kết tới danh sách Ứng dụng của nhóm giải pháp.'),
    ('Cột Mô tả', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu',
     'Hoạt động màu xanh, Khóa màu đỏ. Rê chuột vào nhãn hiện lý do khi chưa khóa được (“Cần khóa '
     'hết các danh mục con trước khi khóa nhóm giải pháp này”) hoặc chưa mở khóa được (“Cần mở khóa '
     'dữ liệu cấp cha (nhóm ngành) trước khi thực hiện thao tác này”).'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu',
     'Không tắt được. Hiện tối đa 2 nút chính theo thứ tự Sửa, Xóa, Khóa / Mở khóa, Lịch sử; '
     'phần còn lại gom vào nút “…”. Thao tác không dùng được thì ẨN hẳn.'),
    ('Nút Sửa (bút)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và nhóm giải pháp đang Hoạt động (FR-05).'),
    ('Nút Xóa (thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và nhóm giải pháp chưa có Ứng dụng liên kết (FR-07).'),
    ('Mục Khóa / Mở khóa', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1. Khóa ẩn khi còn Ứng dụng đang Hoạt động; Mở khóa ẩn khi có Nhóm ngành đang '
     'gắn bị khóa (FR-08).'),
    ('Mục Lịch sử', 'Button', 'Enable', '–', 'Hiển thị', 'Mọi người vào được màn đều thấy (FR-09).'),
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
    ('Bấm Mã nhóm giải pháp', 'Click', 'After:\n– Mở cửa sổ Xem chi tiết nhóm giải pháp (FR-06).'),
    ('Bấm số ở cột Số ứng dụng', 'Click',
     'After:\n– Chuyển tới danh sách Ứng dụng đã lọc theo nhóm giải pháp.'),
    ('Bấm nút “…” ở cột Hành động', 'Click',
     'After:\n– Mở menu các thao tác còn lại của dòng (Khóa / Mở khóa, Lịch sử).'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Danh mục '
           'nhóm giải pháp tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc nhóm giải pháp',
    mota='Tìm nhanh theo mã, tên nhóm giải pháp hoặc tên người tạo; lọc nâng cao theo nhóm ngành, '
         'trạng thái, người tạo, người cập nhật, khoảng ngày cập nhật.',
    tacnhan='Người quản lý / người xem danh mục nhóm giải pháp; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách nhóm giải pháp.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
          '3. Chọn giá trị ở các ô Nhóm ngành, Trạng thái, Người tạo, Người cập nhật, Ngày cập nhật: '
          'chọn xong hệ thống tự lọc lại ngay.\n'
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
     'Tìm gần đúng theo Mã, Tên nhóm giải pháp hoặc tên Người tạo. Áp dụng khi bấm Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao (nhãn đổi thành “Ẩn tìm kiếm nâng cao” khi đang mở).'),
    ('Nhóm ngành', 'Dropdown', 'Enable', 'Danh sách nhóm ngành đang Hoạt động', 'Không', 'Trống',
     'Hiển thị “Mã • Tên”. Danh sách chỉ nạp khi mở khối lọc lần đầu. Lọc nhóm giải pháp có gắn '
     'nhóm ngành đã chọn.'),
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
    ('Gõ vào ô tìm nhanh', 'Keypress', 'After:\n– Chưa lọc; chờ Enter hoặc nút Tìm kiếm.'),
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
    dieukien='Đang ở màn danh sách nhóm giải pháp.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ với danh sách trường / cột, đánh dấu những mục đang hiện.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho người dùng, đóng cửa sổ và vẽ lại khối lọc / bảng.',
    phu='• Bấm “Khôi phục mặc định” → trả về bộ trường lọc mặc định của màn.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Cột STT, Mã nhóm giải pháp và Hành động luôn hiện, không bỏ tích được (hiển thị xám + '
        'ổ khóa).',
    dacbiet='Mặc định màn hiện TẤT CẢ cột; người dùng tự tắt bớt nếu thấy bảng quá rộng.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột', modal='Cài đặt bộ lọc và Tuỳ chỉnh cột',
         shot=shot('02b-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('02c-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột — cột khóa hiển thị xám', width_in=6.2)
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường lọc', 'Table/Grid', 'Enable', '5 trường', 'Không', 'Theo cấu hình đã lưu',
     'Nhóm ngành, Trạng thái, Người tạo, Người cập nhật, Ngày cập nhật. Mỗi dòng: số thứ tự, biểu '
     'tượng kéo ⠿, ô tích, tên trường.'),
    ('Nút Lưu (Cài đặt bộ lọc)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình trường lọc.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về bộ trường lọc mặc định.'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '12 cột', 'Không', 'Theo cấu hình đã lưu',
     'Cột STT, Mã nhóm giải pháp, Hành động bị khóa (luôn hiện).'),
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
    ('Mã nhóm giải pháp', 'Textbox', 'Enable', 'NGP. + 4 ký tự', 'Có', 'Tiền tố “NGP.” cố định',
     'Chỉ nhận chữ không dấu, chữ số và dấu gạch dưới; hệ thống lưu ở dạng chữ in hoa. Không trùng.'),
    ('Tên nhóm giải pháp', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Không trùng; không chứa dấu phẩy (,) và dấu hai chấm (:). Icon ⓘ hiển thị mô tả trường.'),
    ('Nhóm ngành', 'Dropdown', 'Enable', 'Danh sách nhóm ngành đang Hoạt động', 'Có', 'Trống',
     'Chọn nhiều (≥ 1 nhóm ngành), mỗi nhóm ngành hiển thị thành 1 thẻ. Icon ⓘ hiển thị mô tả trường.'),
    ('Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Có', 'Hoạt động',
     'Không có nút xóa chọn — luôn phải có giá trị.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Trống', 'Nội dung mô tả tự do.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ kèm biểu tượng cảnh báo ngay dưới ô bị lỗi.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
]
SAVE_DURING = (
    '– Mã nhóm giải pháp trống (hoặc chỉ có tiền tố “NGP.”) → “Bắt buộc phải nhập”.\n'
    '– Mã không đủ 4 ký tự sau “NGP.” → “Vui lòng nhập 4 ký tự”.\n'
    '– Mã có ký tự không hợp lệ → “Chỉ cho phép: Chữ cái không dấu(A-Z, a-z), chữ số (0-9) và dấu '
    'gạch dưới (_).”\n'
    '– Mã đã tồn tại → “Đã tồn tại trên hệ thống”.\n'
    '– Tên nhóm giải pháp trống → “Bắt buộc phải nhập”; trùng → “Đã tồn tại trên hệ thống”; quá 255 '
    'ký tự → “Vui lòng nhập tối đa 255 ký tự.”; chứa , hoặc : → “không được chứa ký tự dấu phẩy (,) '
    'và dấu hai chấm (:)”.\n'
    '– Chưa chọn Nhóm ngành → “Bắt buộc phải nhập”; nhóm ngành không còn → “Không tồn tại”.\n'
    '– Nếu có lỗi validate → thông báo “Bạn chưa nhập đầy đủ thông tin” và không thực hiện bước After.')

d.h3('2.4 Tạo mới nhóm giải pháp')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới nhóm giải pháp', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-04 Tạo mới nhóm giải pháp')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới nhóm giải pháp',
    mota='Thêm một nhóm giải pháp mới vào danh mục, gắn với một hoặc nhiều Nhóm ngành.',
    tacnhan='Người quản lý danh mục nhóm giải pháp',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở cửa sổ “Tạo mới nhóm giải pháp”, Trạng thái mặc định Hoạt động.\n'
          '3. Người dùng nhập Mã, Tên, chọn một hoặc nhiều Nhóm ngành, nhập Mô tả (nếu có).\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống kiểm tra dữ liệu, ghi bản ghi mới và ghi 1 dòng lịch sử “Tạo mới”.\n'
          '6. Thông báo “Thêm mới thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Bấm “Lưu & Tiếp tục” → lưu xong giữ cửa sổ mở, xóa trắng form để nhập bản ghi tiếp.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới từng ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu đã nhập.\n'
        '• Có nhóm ngành đã chọn vừa bị khóa → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
        '• Lỗi khác → thông báo “Thêm mới thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Bấm Lưu liên tiếp khi yêu cầu trước chưa xử lý xong thì hệ thống bỏ qua lần bấm sau để '
            'tránh tạo trùng.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', modal='Tạo mới nhóm giải pháp', shot=shot('03-tao-moi.png'),
         shot_caption='Cửa sổ Tạo mới nhóm giải pháp')
d.figure(shot('03b-tao-moi-loi.png'), 'Cửa sổ Tạo mới khi bấm Lưu mà chưa nhập các trường bắt buộc',
         width_in=6.2)
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([('Tiêu đề “Tạo mới nhóm giải pháp”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–')]
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
     'After:\n– Mở cửa sổ với form trống, Trạng thái = Hoạt động; nạp danh sách nhóm ngành đang '
     'Hoạt động.'),
    ('Bấm Lưu / Lưu & Tiếp tục', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING + '\n'
     '– Có nhóm ngành đã chọn không còn Hoạt động → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'After:\n– Ghi bản ghi mới, mã chuyển sang chữ in hoa; gắn các nhóm ngành đã chọn; ghi người '
     'tạo, thời điểm tạo.\n'
     '– Ghi 1 dòng lịch sử “Tạo mới”.\n'
     '– Thông báo “Thêm mới thành công”, nạp lại danh sách.\n'
     '– Lưu: đóng cửa sổ. Lưu & Tiếp tục: giữ cửa sổ, xóa trắng form.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, không lưu dữ liệu đang nhập.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Chỉnh sửa nhóm giải pháp')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa nhóm giải pháp', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-05 Chỉnh sửa nhóm giải pháp')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa). '
           'Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa nhóm giải pháp',
    mota='Cập nhật thông tin của một nhóm giải pháp đang Hoạt động.',
    tacnhan='Người quản lý danh mục nhóm giải pháp',
    dieukien='Người dùng có quyền Q1; nhóm giải pháp đang ở trạng thái Hoạt động.',
    chinh='1. Người dùng bấm nút Sửa trên dòng nhóm giải pháp.\n'
          '2. Hệ thống mở cửa sổ “Sửa nhóm giải pháp” với dữ liệu hiện tại.\n'
          '3. Người dùng sửa thông tin và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu, cập nhật và ghi 1 dòng lịch sử các trường đã đổi '
          '(giá trị cũ → giá trị mới).\n'
          '5. Thông báo “Cập nhật thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Nhóm giải pháp đang Khóa → nút Sửa bị ẩn.\n'
        '• Nhóm ngành đang gắn nay đã bị khóa → vẫn hiển thị đúng tên trong ô (có biểu tượng 🔒) và '
        'vẫn lưu được nếu giữ nguyên; thêm nhóm ngành khác thì chỉ chọn được nhóm ngành Hoạt động.\n'
        '• Bản ghi đã bị xóa / khóa bởi người khác trong lúc sửa → “Dữ liệu đã thay đổi, vui lòng '
        'tải lại”.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin”.',
    dacbiet='Nhóm giải pháp đã có Ứng dụng liên kết thì không được đổi Mã. Ô Trạng thái bị khóa khi '
            'nhóm giải pháp còn Ứng dụng đang Hoạt động.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', modal='Sửa nhóm giải pháp', shot=shot('04-sua.png'),
         shot_caption='Cửa sổ Sửa nhóm giải pháp')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Sửa nhóm giải pháp”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Mã nhóm giải pháp', 'Textbox', 'Enable', 'NGP. + 4 ký tự', 'Có', 'Theo dữ liệu',
     'Như Tạo mới. Đã có Ứng dụng liên kết mà đổi mã → báo lỗi, không lưu.'),
    ('Tên nhóm giải pháp', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo dữ liệu', 'Như Tạo mới.'),
    ('Nhóm ngành', 'Dropdown', 'Enable', 'Nhóm ngành đang Hoạt động + nhóm ngành đang gắn',
     'Có', 'Theo dữ liệu', 'Chọn nhiều; nhóm ngành đang gắn đã khóa vẫn hiển thị kèm 🔒.'),
    ('Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Có', 'Theo dữ liệu',
     'Bị khóa khi nhóm giải pháp còn Ứng dụng đang Hoạt động.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Theo dữ liệu', '–'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Không có nút Lưu & Tiếp tục.'),
    FORM_ROWS[-2], FORM_ROWS[-1],
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và nhóm giải pháp đang Hoạt động.\n'
     'During:\n– Nạp chi tiết bản ghi và danh sách nhóm ngành (kèm nhóm ngành đang gắn).\n'
     '– Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ Sửa với dữ liệu hiện tại.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Nhóm giải pháp không còn Hoạt động, hoặc chuyển sang Khóa khi còn Ứng dụng đang Hoạt động '
     '→ “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'During:\n' + SAVE_DURING.replace(
         '– Nếu có lỗi validate',
         '– Đổi mã khi đã có Ứng dụng liên kết → “Không thể sửa mã khi đã có dữ liệu nhóm giải pháp '
         'hoặc ứng dụng liên quan.”\n– Nếu có lỗi validate') + '\n'
     'After:\n– Cập nhật bản ghi và danh sách nhóm ngành đang gắn; ghi người cập nhật, thời điểm '
     'cập nhật.\n'
     '– Ghi 1 dòng lịch sử các trường đã đổi (Mã, Tên, Mô tả, Trạng thái).\n'
     '– Thông báo “Cập nhật thành công”, đóng cửa sổ, nạp lại danh sách.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xem chi tiết nhóm giải pháp')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết nhóm giải pháp',
    mota='Xem toàn bộ thông tin của một nhóm giải pháp ở chế độ chỉ đọc, kèm số ứng dụng đang liên '
         'kết và khối Lịch sử thay đổi.',
    tacnhan='Người quản lý / người xem danh mục nhóm giải pháp',
    dieukien='Người dùng có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng bấm vào Mã nhóm giải pháp trên bảng.\n'
          '2. Hệ thống mở cửa sổ “Xem chi tiết nhóm giải pháp”, mọi ô ở trạng thái chỉ đọc.\n'
          '3. (Tuỳ chọn) Người dùng bấm “Xem lịch sử” để mở rộng khối Lịch sử.\n'
          '4. Người dùng bấm Đóng để quay về danh sách.',
    phu='• Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.',
    dacbiet=None)
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', modal='Xem chi tiết nhóm giải pháp', shot=shot('05-xem.png'),
         shot_caption='Cửa sổ Xem chi tiết nhóm giải pháp')
d.figure(shot('05b-xem-lich-su.png'), 'Khối Lịch sử trong cửa sổ Xem chi tiết đã mở rộng',
         width_in=6.2)
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xem chi tiết nhóm giải pháp”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Mã nhóm giải pháp', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Tên nhóm giải pháp', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Nhóm ngành', 'Dropdown', 'Read-only', '–', 'Theo dữ liệu',
     'Các nhóm ngành đang gắn, mỗi nhóm 1 thẻ; nhóm ngành đã khóa vẫn hiển thị đúng tên kèm 🔒.'),
    ('Trạng thái', 'Dropdown', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu', '–'),
    ('Số ứng dụng', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu', 'Số ứng dụng đang liên kết.'),
    ('Mô tả', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở danh sách thay đổi của bản ghi (như FR-09); có nút Làm mới, Thu gọn, '
     'Bộ lọc.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Không có nút Lưu.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Mã nhóm giải pháp', 'Click',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'After:\n– Mở cửa sổ chi tiết ở chế độ chỉ đọc.'),
    ('Bấm “Xem lịch sử”', 'Click', 'After:\n– Mở rộng khối Lịch sử và nạp danh sách thay đổi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Xóa nhóm giải pháp')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xóa nhóm giải pháp', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-07 Xóa nhóm giải pháp')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa nhóm giải pháp',
    mota='Xóa hẳn một nhóm giải pháp chưa được Ứng dụng nào sử dụng.',
    tacnhan='Người quản lý danh mục nhóm giải pháp',
    dieukien='Người dùng có quyền Q1; nhóm giải pháp chưa có Ứng dụng liên kết.',
    chinh='1. Người dùng bấm nút Xóa trên dòng nhóm giải pháp.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận xóa”.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống xóa bản ghi, ghi 1 dòng lịch sử “Xóa”, thông báo “Xóa thành công” và nạp lại '
          'danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xóa.\n'
        '• Nhóm giải pháp đã có Ứng dụng liên kết → nút Xóa bị ẩn; nếu phát sinh liên kết trong lúc '
        'đang xác nhận → “Dữ liệu đang được sử dụng, vui lòng tải lại”.\n'
        '• Bản ghi đã bị xóa trước đó → “Dữ liệu đã thay đổi, vui lòng tải lại”.',
    dacbiet='Xóa là xóa hẳn, không khôi phục được. Muốn ngừng dùng nhóm giải pháp đã có liên kết thì '
            'dùng chức năng Khóa.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', modal='Xác nhận xóa', shot=shot('06-xoa.png'),
         shot_caption='Hộp thoại xác nhận xóa nhóm giải pháp')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xác nhận xóa”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn xóa nhóm giải pháp \'<tên>\'?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
], required=False, scope=False)
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và nhóm giải pháp chưa có Ứng dụng liên kết.\n'
     'After:\n– Hiện hộp thoại xác nhận.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Còn Ứng dụng liên kết → “Dữ liệu đang được sử dụng, vui lòng tải lại” và dừng xử lý.\n'
     '– Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'After:\n– Xóa bản ghi, ghi 1 dòng lịch sử “Xóa” kèm dữ liệu lúc xóa.\n'
     '– Thông báo “Xóa thành công”, nạp lại danh sách.'),
    ('Bấm Hủy / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Khóa / Mở khóa nhóm giải pháp')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Khóa / Mở khóa nhóm giải pháp', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-08 Khóa / Mở khóa nhóm giải pháp')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khóa / Mở khóa nhóm giải pháp',
    mota='Chuyển trạng thái nhóm giải pháp giữa Hoạt động và Khóa bằng thao tác Khóa / Mở khóa ở '
         'cột Hành động.',
    tacnhan='Người quản lý danh mục nhóm giải pháp',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút “…” trên dòng, chọn Khóa (dòng đang Khóa thì bấm nút Mở khóa hiện '
          'sẵn trên dòng).\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khóa” (hoặc “Xác nhận mở khóa”).\n'
          '3. Người dùng bấm Khóa (hoặc Mở khóa).\n'
          '4. Hệ thống đổi trạng thái, ghi 1 dòng lịch sử nhóm “Thay đổi trạng thái”, thông báo '
          '“Khóa thành công” / “Mở khóa thành công”, nạp lại danh sách.',
    phu='• Nhóm giải pháp còn Ứng dụng đang Hoạt động → mục Khóa bị ẩn; rê chuột vào nhãn trạng '
        'thái hiện “Cần khóa hết các danh mục con trước khi khóa nhóm giải pháp này”.\n'
        '• Nhóm giải pháp đang Khóa có Nhóm ngành đang gắn bị khóa → mục Mở khóa bị ẩn; rê chuột vào '
        'nhãn trạng thái hiện “Cần mở khóa dữ liệu cấp cha (nhóm ngành) trước khi thực hiện thao tác '
        'này”.\n'
        '• Phát sinh Ứng dụng Hoạt động trong lúc xác nhận khóa → “Dữ liệu đã thay đổi, vui lòng '
        'tải lại”.\n'
        '• Bấm Hủy → không đổi trạng thái.',
    dacbiet='Nhóm giải pháp đang Khóa không Sửa được cho tới khi Mở khóa.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Khóa / Mở khóa',
         modal='Xác nhận khóa / Xác nhận mở khóa',
         shot=shot('07b-khoa.png'), shot_caption='Hộp thoại xác nhận khóa nhóm giải pháp')
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Mục Khóa / Mở khóa', 'Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Đang Hoạt động: mục Khóa (ổ khóa đóng) trong menu “…”. Đang Khóa: nút Mở khóa (ổ khóa mở) '
     'hiện ngay trên dòng.'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khóa” / “Xác nhận mở khóa”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn khóa (mở khóa) nhóm giải pháp \'<tên>\'?”'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Khóa / Mở khóa', 'Click',
     'Before:\n– Chỉ hiện với Q1; Khóa chỉ hiện khi không còn Ứng dụng đang Hoạt động; Mở khóa chỉ '
     'hiện khi mọi Nhóm ngành đang gắn đều Hoạt động.\n'
     'After:\n– Hiện hộp thoại xác nhận tương ứng.'),
    ('Bấm Khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Còn Ứng dụng đang Hoạt động → “Dữ liệu đã thay đổi, vui lòng tải lại” và dừng xử lý.\n'
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
           'nhóm giải pháp.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của nhóm giải pháp',
    mota='Xem các lần Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Xóa của một nhóm giải pháp: '
         'ai làm, lúc nào, trường nào đổi từ giá trị cũ sang giá trị mới.',
    tacnhan='Người quản lý / người xem danh mục nhóm giải pháp',
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
d.p('2.9.2 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Lịch sử', modal='Lịch sử thay đổi',
         shot=shot('08-lich-su.png'), shot_caption='Cửa sổ Lịch sử thay đổi của nhóm giải pháp')
d.p('2.9.3 Mô tả chi tiết giao diện')
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
d.p('2.9.4 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Lịch sử', 'Click', 'After:\n– Mở cửa sổ và nạp danh sách thay đổi của bản ghi.'),
    ('Đổi giá trị trong Bộ lọc', 'Change', 'After:\n– Lọc lại danh sách thay đổi ngay.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.10
d.h3('2.10 Import Excel')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Import Excel nhóm giải pháp', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-10 Import Excel nhóm giải pháp')
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Import file, Validate dữ liệu và Thông báo.', anchor='excel')
d.intro_table(
    ten='Import Excel nhóm giải pháp',
    mota='Thêm mới hàng loạt nhóm giải pháp từ tệp Excel theo file mẫu. Chỉ thêm mới, không cập '
         'nhật nhóm giải pháp đã có.',
    tacnhan='Người quản lý danh mục nhóm giải pháp',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm Import Excel.\n'
          '2. (Tuỳ chọn) Bấm “Tải file mẫu” để lấy tệp Mau_import_NhomGiaiPhap.xlsx.\n'
          '3. Bấm “Chọn file Excel”, chọn tệp đã điền dữ liệu.\n'
          '4. Bấm “Load lên bảng” để đọc tệp ra bảng xem trước.\n'
          '5. Bấm “Validate” → hệ thống kiểm tra từng dòng, đánh dấu dòng hợp lệ / lỗi kèm lý do; '
          'dòng hợp lệ bị khóa không sửa được.\n'
          '6. Nếu còn dòng lỗi: sửa trực tiếp các dòng lỗi rồi Validate lại, hoặc bấm “Bỏ dòng lỗi” '
          'để loại các dòng lỗi khỏi bảng.\n'
          '7. Khi đã Validate và không còn dòng lỗi, nút Import mới bấm được. Bấm “Import” → hệ '
          'thống ghi các dòng, thông báo “Import thành công <n> nhóm '
          'giải pháp”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Chưa Validate, hoặc còn dòng lỗi → nút Import bị khóa, không bấm được.\n'
        '• Mọi dòng đều lỗi → sau khi bỏ dòng lỗi bảng không còn dòng nào, nút Import vẫn khóa; '
        'không import được.\n'
        '• Bấm “Bỏ dòng lỗi” → “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”\n'
        '• Bấm “Xoá trạng thái validate” → bỏ đánh dấu, mở khóa các dòng để sửa; phải Validate lại.\n'
        '• Dữ liệu thay đổi giữa lúc Validate và Import (vd người khác vừa tạo bản ghi trùng mã): '
        'còn ghi được một phần → “Import thành công x/y nhóm giải pháp. z nhóm giải pháp thất bại.”, đóng cửa sổ và nạp lại danh sách; '
        'không ghi được dòng nào → báo lỗi “Không có dữ liệu hợp lệ để import” (hoặc '
        '“Import thất bại: z/y nhóm giải pháp không hợp lệ”), cửa sổ giữ nguyên.\n'
        '• Tệp quá 500 dòng → “Mỗi lần import tối đa 500 dòng (file đang có N dòng), vui lòng tách '
        'file và import nhiều lần.”\n'
        '• Bật “Chỉ dòng lỗi” để lọc bảng xem trước chỉ còn dòng lỗi.\n'
        '• Bấm Làm mới → xóa dữ liệu đã nạp để chọn tệp khác.',
    dacbiet='Mỗi lần import tối đa 500 dòng. Mỗi dòng thêm thành công đều ghi 1 dòng lịch sử '
            '“Tạo mới”.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Import Excel', modal='Import Nhóm giải pháp', shot=shot('09-import.png'),
         shot_caption='Cửa sổ Import Nhóm giải pháp')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx / .xls', 'Có', 'Hiển thị', 'Chọn tệp cần import.'),
    ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải Mau_import_NhomGiaiPhap.xlsx.'),
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
    ('Cột Mã nhóm giải pháp', 'Textbox', 'Enable', 'NGP.XXXX', 'Có', 'Theo tệp',
     'Không trùng trong tệp và hệ thống.'),
    ('Cột Tên nhóm giải pháp', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo tệp',
     'Không trùng trong tệp và hệ thống; không chứa , và :.'),
    ('Cột Mã Nhóm ngành', 'Textbox', 'Enable', 'NN.XXXX, NN.YYYY', 'Có', 'Theo tệp',
     'Một hoặc nhiều mã nhóm ngành ngăn nhau bằng dấu phẩy; mỗi mã phải tồn tại và đang Hoạt động.'),
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
     '– Thiếu mã / tên / mã nhóm ngành / trạng thái → “Mã nhóm giải pháp không được để trống”, “Tên '
     'nhóm giải pháp không được để trống”, “Mã nhóm ngành không được để trống”, “Trạng thái không '
     'được để trống”.\n'
     '– Mã sai định dạng → “Mã nhóm giải pháp phải theo định dạng NGP.XXXX (4 ký tự)”.\n'
     '– Mã trùng trong tệp → “Mã nhóm giải pháp bị trùng lặp trong file import (dòng n)”; trùng hệ '
     'thống → “Mã nhóm giải pháp đã tồn tại trong hệ thống”.\n'
     '– Tên trùng trong tệp → “Tên nhóm giải pháp bị trùng lặp trong file import (dòng n)”; trùng '
     'hệ thống → “Tên nhóm giải pháp đã tồn tại trong hệ thống”; quá dài → “Tên nhóm giải pháp vượt '
     'quá độ dài cho phép (tối đa 255 ký tự)”; chứa , hoặc : → “không được chứa ký tự dấu phẩy (,) '
     'và dấu hai chấm (:)”.\n'
     '– Mã nhóm ngành không có hoặc đã khóa → “Mã nhóm ngành không tồn tại hoặc đang bị khoá: '
     '<danh sách mã>”.\n'
     '– Trạng thái sai → “Trạng thái không hợp lệ, chỉ nhận giá trị: active hoặc inactive”.\n'
     '– Mô tả quá dài → “Mô tả vượt quá độ dài cho phép (tối đa 1000 ký tự)”.\n'
     'After:\n– Đánh dấu từng dòng hợp lệ / lỗi; thông báo “Validate thành công” hoặc “Validate xong: '
     'x hợp lệ, y không hợp lệ”.'),
    ('Bấm Import', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Nút chỉ bấm được khi đã Validate và không còn dòng lỗi.\n'
     'During:\n– Chỉ gửi các dòng hợp lệ. Máy chủ kiểm tra lại các dòng gửi lên như bước '
     'Validate.\n'
     'After:\n– Thêm mới các dòng hợp lệ, mã chuyển sang chữ in hoa, gắn các nhóm ngành theo mã; ghi '
     'lịch sử “Tạo mới” từng dòng.\n'
     '– Tất cả thành công → “Import thành công <n> nhóm giải pháp”, đóng cửa sổ, nạp lại danh sách.\n'
     '– Một phần (dữ liệu thay đổi giữa lúc Validate và Import) → '
     '“Import thành công x/y nhóm giải pháp. z nhóm giải pháp thất bại.”, đóng cửa sổ, nạp lại danh sách.\n'
     '– Không ghi được dòng nào → báo lỗi “Không có dữ liệu hợp lệ để import” (hoặc '
     '“Import thất bại: z/y nhóm giải pháp không hợp lệ”); cửa sổ giữ nguyên, không ghi dữ liệu.'),
    ('Bấm Bỏ dòng lỗi', 'Click',
     'Before:\n– Chưa Validate → “Hãy Validate trước rồi mới bỏ dòng lỗi.”\n'
     'After:\n– Loại các dòng lỗi khỏi bảng; thông báo “Đã bỏ x dòng lỗi. Còn lại y dòng hợp '
     'lệ.”; nút Import mở nếu còn ≥ 1 dòng.'),
    ('Bấm Tải file mẫu', 'Click', 'After:\n– Tải tệp Mau_import_NhomGiaiPhap.xlsx.'),
])

# ---------------------------------------------------------------- 2.11
d.h3('2.11 Xuất Excel')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Xuất Excel danh sách nhóm giải pháp', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-11 Xuất Excel')
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của '
           'Danh mục nhóm giải pháp.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách nhóm giải pháp',
    mota='Người dùng chọn các trường cần xuất rồi tải về tệp danh_sach_nhom_giai_phap.xlsx gồm TẤT '
         'CẢ nhóm giải pháp khớp bộ lọc đang áp dụng (không chỉ trang đang xem).',
    tacnhan='Người quản lý danh mục nhóm giải pháp',
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
    ('Danh sách trường xuất', 'Table/Grid', 'Enable', '10 trường', 'Có (≥ 1)',
     'Tích sẵn các cột đang hiện trên bảng',
     'Mã nhóm giải pháp, Tên nhóm giải pháp, Nhóm ngành, Số ứng dụng, Mô tả, Trạng thái, Người tạo, '
     'Ngày tạo, Người cập nhật, Ngày cập nhật. Kéo ☰ để đổi thứ tự.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn nhanh.'),
    ('Dòng “Đang chọn x/10 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Tải tệp danh_sach_nhom_giai_phap.xlsx.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiện trên bảng.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Áp đúng bộ lọc đang dùng trên màn, lấy tất cả dòng khớp.\n'
     'After:\n– Tải tệp danh_sach_nhom_giai_phap.xlsx với các trường đã chọn theo thứ tự đã sắp.\n'
     '– Thông báo “Xuất Excel thành công”.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Danh mục nhóm giải pháp; không lặp lại các '
           'quy tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Định dạng và tính duy nhất của Mã', [
        '– Mã = tiền tố “NGP.” + đúng 4 ký tự gồm chữ không dấu, chữ số, dấu gạch dưới.',
        '– Hệ thống lưu mã ở dạng chữ in hoa; không trùng trong toàn hệ thống.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-02', 'Tên nhóm giải pháp', [
        '– Bắt buộc, tối đa 255 ký tự, không trùng.',
        '– Không chứa dấu phẩy (,) và dấu hai chấm (:).',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-03', 'Gắn Nhóm ngành', [
        '– Mỗi nhóm giải pháp bắt buộc gắn ít nhất 1 nhóm ngành, được gắn nhiều nhóm ngành.',
        '– Chỉ chọn được nhóm ngành đang Hoạt động.',
        '– Ngoại lệ: khi Sửa, nhóm ngành đang gắn nay đã bị khóa vẫn hiển thị đúng tên (🔒) và được '
        'giữ nguyên khi lưu.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel', 'Tìm kiếm và lọc']),
    ('BR-04', 'Khóa sửa Mã khi đã có liên kết',
     '– Nhóm giải pháp đã có Ứng dụng liên kết thì không được đổi Mã.',
     'Chỉnh sửa'),
    ('BR-05', 'Chỉ sửa nhóm giải pháp đang Hoạt động',
     '– Nhóm giải pháp đang Khóa không sửa được (nút Sửa bị ẩn); phải Mở khóa trước.',
     ['Chỉnh sửa', 'Danh sách']),
    ('BR-06', 'Điều kiện Xóa', [
        '– Chỉ xóa được khi chưa có Ứng dụng nào liên kết; ngược lại nút Xóa bị ẩn.',
        '– Xóa là xóa hẳn; nhóm giải pháp đã có liên kết thì dùng Khóa thay cho Xóa.',
    ], 'Xóa'),
    ('BR-07', 'Điều kiện Khóa / Mở khóa', [
        '– Chỉ Khóa được khi không còn Ứng dụng nào đang Hoạt động gắn với nhóm giải pháp (áp dụng '
        'cả khi đổi Trạng thái trong form Sửa).',
        '– Chỉ Mở khóa được khi mọi Nhóm ngành đang gắn đều Hoạt động.',
    ], ['Khóa / Mở khóa', 'Chỉnh sửa']),
    ('BR-08', 'Thao tác không dùng được thì ẩn', [
        '– Sửa, Xóa, Khóa / Mở khóa chỉ hiện với người có Q1 VÀ đủ điều kiện nghiệp vụ.',
        '– Không hiển thị nút xám; lý do chưa khóa / mở khóa được ghi ở nhãn Trạng thái khi rê chuột.',
    ], 'Danh sách'),
    ('BR-09', 'Ghi lịch sử thay đổi', [
        '– Ghi lại mọi lần Tạo mới (kể cả qua Import), Thay đổi thông tin, Thay đổi trạng thái, Xóa.',
        '– Thay đổi thông tin chỉ ghi các trường thực sự đổi: Mã, Tên, Mô tả, Trạng thái.',
        '– Ai vào được màn đều xem được lịch sử.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xóa', 'Khóa / Mở khóa', 'Import Excel', 'Xem lịch sử']),
    ('BR-10', 'Import chỉ thêm mới', [
        '– Mỗi lần tối đa 500 dòng.',
        '– Mã / tên đã có trong hệ thống hoặc trùng nhau trong tệp → dòng lỗi, không ghi đè.',
        '– Cột Mã Nhóm ngành nhận nhiều mã ngăn bằng dấu phẩy; mã nhóm ngành đã khóa coi như không '
        'tồn tại.',
        '– Chỉ các dòng hợp lệ được thêm; dòng lỗi được báo lý do cụ thể.',
    ], 'Import Excel'),
    ('BR-11', 'Xuất theo bộ lọc, chọn trường', [
        '– Xuất tất cả dòng khớp bộ lọc đang áp dụng, không giới hạn theo trang.',
        '– Người dùng chọn trường và thứ tự trường; mặc định là các cột đang hiện trên bảng.',
    ], 'Xuất Excel'),
    ('BR-12', 'Số liệu liên kết', [
        '– Số ứng dụng đếm theo số ứng dụng khác nhau đang gắn với nhóm giải pháp.',
        '– Số khác 0 là liên kết tới danh sách Ứng dụng đã lọc theo nhóm giải pháp.',
    ], ['Danh sách', 'Xem chi tiết']),
])

d.save(update_fields=False)

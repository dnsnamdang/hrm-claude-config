# -*- coding: utf-8 -*-
"""Sinh "SRS - Danh mục lý do thất bại.docx" theo code nhánh gop_db — form 2026-09-24.

Chạy:  python3 .plans/gop-db/srs-danh-muc-du-an/ly-do-that-bai/gen_srs.py
Ảnh chụp thật (Playwright 1440x900, bản gop_db cổng 3002): ly-do-that-bai_shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/reason_project_failure/index.vue · components/modal/reason-project-failure-modal.vue
      components/assign/prospective-project/CloseProjectModal.vue (nơi dùng danh mục)
      components/subsystem-menu/presale.js (menu) · components/subsystems.js (phân hệ "CSKH trước bán")
  BE  Modules/Assign/Routes/api.php (nhóm /assign/reason_project_failures)
      Http/Requests/ReasonProjectFailure/ReasonProjectFailureRequest.php
      Http/Controllers/Api/V1/ReasonProjectFailureController.php · Services/ReasonProjectFailureService.php
      Entities/ReasonProjectFailure.php · Services/ProspectiveProjectAutoCloseService.php
      app/Http/Middleware/CheckImportRowLimit.php (500 dòng / lần import)
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 990, 1005)
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


OUT = os.path.join(HERE, 'SRS - Danh mục lý do thất bại.docx')
SHOTS = os.path.join(HERE, 'ly-do-that-bai_shots')
MENU = 'Phân hệ CSKH trước bán => Danh mục => Nguyên nhân thất bại dự án'

A_QL = 'Người quản lý danh mục nguyên nhân thất bại dự án (Q1)'
A_XEM = 'Người xem danh mục nguyên nhân thất bại dự án (Q2)'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/reason_project_failure',
           full_url='https://<host-hrm>/assign/reason_project_failure', img_prefix='lydothatbai_gopdb_')

# Icon cho từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện.
# Nhãn trên giao diện viết "Khoá" / "Mở khoá" (oa) nên key menu cũng theo đúng chữ đó.
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ CSKH trước bán': 'phanhe', 'Danh mục': 'danhmuc', 'Nguyên nhân thất bại dự án': 'man',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidatboloc', 'Tuỳ chỉnh cột': 'tuychinhcot',
    'Tạo mới': 'taomoi', 'Sửa': 'sua', 'Xem chi tiết': 'xem', 'Xóa': 'xoa',
    'Hành động khác': 'khac', 'Khoá': 'khoa', 'Mở khoá': 'mokhoa', 'Lịch sử': 'lichsu',
    'Import Excel': 'import', 'Xuất Excel': 'xuat',
}.items()})

d.title_block('Danh mục lý do thất bại')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục lý do thất bại (nhãn trên menu: '
    '“Nguyên nhân thất bại dự án”, tiêu đề màn: “Danh sách nguyên nhân thất bại dự án”) thuộc phân '
    'hệ CSKH trước bán, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ vai trò của danh mục: là danh sách lý do để chọn khi đóng dự án TKT (dự án thất bại) và '
    'lý do hệ thống dùng khi tự đóng dự án quá hạn.',
    'Làm rõ điều kiện hiện các thao tác Sửa, Xóa, Khoá, Mở khoá trên từng dòng.',
    'Làm rõ quy tắc nhập dữ liệu hàng loạt và xuất dữ liệu ra tệp Excel.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Nguyên nhân thất bại dự án (lý do thất bại)', 'Lý do một dự án TKT không thành công, được chọn '
     'bắt buộc khi người dùng đóng dự án.'),
    ('Dự án TKT', 'Dự án tiềm năng / dự án đang theo dõi ở phân hệ CSKH trước bán.'),
    ('Lý do tự đóng', 'Lý do “Hệ thống tự đóng do quá thời gian thực hiện” — hệ thống tự gán khi tự '
     'đóng dự án quá thời gian. Nếu không còn lý do có đúng tên này, hệ thống tự tạo lại.'),
    ('Trạng thái Khoá', 'Lý do ngừng sử dụng: không hiện trong danh sách chọn khi đóng dự án, không '
     'sửa được. Khoá KHÔNG xóa dữ liệu, có thể Mở khoá lại.'),
    ('Menu “…” (Hành động khác)', 'Nút ở cột Hành động chứa các thao tác còn lại của dòng khi dòng '
     'có nhiều hơn 3 thao tác.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý danh mục nguyên nhân thất bại dự án',
     'Xem danh sách, xem chi tiết, xem lịch sử; hiện nút Tạo mới, Import Excel, Xuất Excel; hiện các '
     'thao tác Sửa, Xóa, Khoá / Mở khoá trên dòng.'),
    ('Q2', 'Xem danh mục nguyên nhân thất bại dự án',
     'Xem danh sách, tìm kiếm, xem chi tiết và xem lịch sử. Không hiện thao tác thay đổi dữ liệu và '
     'không có nút Xuất Excel.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn hình không phân quyền theo cấp dữ liệu (công ty / phòng ban / bộ phận): người có quyền '
    'xem được toàn bộ lý do thất bại của hệ thống.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách lý do thất bại', '✅', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '❌'),
    ('FR-04 Tạo mới lý do thất bại', '✅', '❌', '❌'),
    ('FR-05 Chỉnh sửa lý do thất bại', '✅', '❌', '❌'),
    ('FR-06 Xem chi tiết lý do thất bại', '✅', '✅', '❌'),
    ('FR-07 Xóa lý do thất bại', '✅', '❌', '❌'),
    ('FR-08 Khoá / Mở khoá lý do thất bại', '✅', '❌', '❌'),
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
    [('FR-01', 'Xem danh sách lý do thất bại', 'view'),
     ('FR-04', 'Tạo mới lý do thất bại', 'crud'),
     ('FR-05', 'Chỉnh sửa lý do thất bại', 'crud'),
     ('FR-07', 'Xóa lý do thất bại', 'action'),
     ('FR-08', 'Khoá / Mở khoá lý do thất bại', 'action'),
     ('FR-10', 'Import Excel lý do thất bại', 'io'),
     ('FR-11', 'Xuất Excel danh sách lý do thất bại', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết lý do thất bại', 'view', 'extend', [0], None),
     ('FR-09', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Danh mục lý do thất bại')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách lý do thất bại')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Danh mục lý do thất bại tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách lý do thất bại',
    mota='Hiển thị toàn bộ nguyên nhân thất bại dự án kèm mô tả, người tạo / cập nhật, trạng thái '
         'và các thao tác trên từng dòng. Bảng không có cột Mã: tên nguyên nhân là cột định danh.',
    tacnhan='Người quản lý / người xem danh mục nguyên nhân thất bại dự án; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng vào menu Phân hệ CSKH trước bán → Danh mục → Nguyên nhân thất bại dự án.\n'
          '2. Hệ thống nạp trang 1, 10 dòng/trang, bản ghi mới tạo lên đầu.\n'
          '3. Bảng hiển thị đủ các cột (mặc định hiện hết cột), dòng “Hiển thị a–b / N” và thanh '
          'phân trang.',
    phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm tên nguyên nhân → mở cửa sổ Xem chi tiết (FR-06).\n'
        '• Bấm tiêu đề cột Nguyên nhân thất bại dự án, Ngày tạo, Ngày cập nhật → sắp xếp theo cột '
        'đó, bấm lại để đảo chiều.\n'
        '• Rời màn rồi quay lại trong vòng 10 phút → bộ lọc đang dùng được khôi phục.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách nguyên nhân thất bại dự án lúc mới truy cập')
d.figure(shot('07-menu-khac.png'), 'Cột Trạng thái, cột Hành động và menu “…” của một dòng',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Danh sách nguyên nhân thất bại dự án”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1', 'Mở form Tạo mới (FR-04).'),
    ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1',
     'Mở cửa sổ Import (FR-10).'),
    ('Nút Xuất Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1',
     'Mở cửa sổ Chọn trường xuất file (FR-11).'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cố định bên trái khi cuộn ngang; không tắt được.'),
    ('Cột Nguyên nhân thất bại dự án', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Cố định bên trái, không tắt được, sắp xếp được; tối đa 2 dòng. Là liên kết mở cửa sổ Xem '
     'chi tiết.'),
    ('Cột Mô tả', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Người tạo hiển thị tên nhân viên (trống với lý do do hệ thống tự tạo). Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khoá', 'Theo dữ liệu',
     'Hoạt động màu xanh, Khoá màu đỏ.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu',
     'Không tắt được. Thứ tự Sửa, Xóa, Khoá / Mở khoá, Lịch sử. Dòng có tối đa 3 thao tác thì '
     'hiện hết; nhiều hơn thì hiện 2 nút đầu, phần còn lại gom vào nút “…”. Thao tác không dùng '
     'được thì ẨN hẳn.'),
    ('Nút Sửa (bút)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và lý do đang Hoạt động (FR-05).'),
    ('Nút Xóa (thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Hiện với Q1 ở mọi dòng (FR-07).'),
    ('Nút / mục Khoá / Mở khoá', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Hiện với Q1. Đang Hoạt động hiện Khoá, đang Khoá hiện Mở khoá (FR-08).'),
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
    ('Bấm tên nguyên nhân', 'Click', 'After:\n– Mở cửa sổ Xem chi tiết (FR-06).'),
    ('Bấm nút “…” ở cột Hành động', 'Click',
     'After:\n– Mở menu các thao tác còn lại của dòng (Khoá / Mở khoá, Lịch sử).'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Danh mục '
           'lý do thất bại tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc lý do thất bại',
    mota='Tìm nhanh theo tên nguyên nhân, mô tả hoặc tên người tạo; lọc nâng cao theo trạng thái, '
         'người tạo, người cập nhật, khoảng ngày cập nhật.',
    tacnhan='Người quản lý / người xem danh mục nguyên nhân thất bại dự án; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách nguyên nhân thất bại dự án.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
          '3. Chọn giá trị ở ô Trạng thái, Người tạo, Người cập nhật, Ngày cập nhật: chọn xong hệ '
          'thống tự lọc lại ngay.\n'
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
     'Placeholder “Tìm theo nguyên nhân, mô tả, người tạo”. Tìm gần đúng theo tên nguyên nhân, mô '
     'tả hoặc họ tên người tạo. Áp dụng khi bấm Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao (nhãn đổi thành “Ẩn tìm kiếm nâng cao” khi đang mở).'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khoá', 'Không', 'Trống', '–'),
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
    dieukien='Đang ở màn danh sách nguyên nhân thất bại dự án.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ với danh sách trường / cột, đánh dấu những mục đang hiện.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho người dùng, đóng cửa sổ và vẽ lại khối lọc / bảng.',
    phu='• Bấm “Khôi phục mặc định” → trả về bộ trường lọc mặc định của màn.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Cột STT, Nguyên nhân thất bại dự án và Hành động luôn hiện, không bỏ tích được (hiển '
        'thị xám + ổ khóa).',
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
    ('Danh sách cột', 'Table/Grid', 'Enable', '9 cột', 'Không', 'Theo cấu hình đã lưu',
     'Cột STT, Nguyên nhân thất bại dự án, Hành động bị khóa (luôn hiện).'),
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
    ('Nguyên nhân thất bại', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Không trùng với nguyên nhân khác. Placeholder “VD: Thiếu ngân sách / Không thống nhất yêu cầu '
     '/ ...”.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động',
     'Không có nút xóa chọn — luôn có giá trị.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Trống', 'Placeholder “Nhập mô tả ngắn (nếu có)...”.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô bị lỗi.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
]
SAVE_DURING = (
    '– Nguyên nhân thất bại trống → “Bắt buộc phải nhập”.\n'
    '– Quá 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”\n'
    '– Trùng tên nguyên nhân khác → “Đã tồn tại trên hệ thống”.\n'
    '– Nếu có lỗi validate → thông báo “Bạn chưa nhập đầy đủ thông tin” và không thực hiện bước After.')

d.h3('2.4 Tạo mới lý do thất bại')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới lý do thất bại', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-04 Tạo mới lý do thất bại')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới lý do thất bại',
    mota='Thêm một nguyên nhân thất bại dự án mới vào danh mục.',
    tacnhan='Người quản lý danh mục nguyên nhân thất bại dự án',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở cửa sổ “Thêm nguyên nhân thất bại dự án”, Trạng thái mặc định Hoạt động.\n'
          '3. Người dùng nhập Nguyên nhân thất bại, Mô tả (nếu có), chọn Trạng thái.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống kiểm tra dữ liệu, ghi bản ghi mới và ghi 1 dòng lịch sử “Tạo mới”.\n'
          '6. Thông báo “Thêm mới thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Bấm “Lưu & Tiếp tục” → lưu xong giữ cửa sổ mở, xóa trắng form để nhập bản ghi tiếp.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu đã nhập.\n'
        '• Lỗi khác → thông báo “Thêm mới thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Nút Lưu và Lưu & Tiếp tục bị khóa trong lúc đang xử lý để tránh tạo trùng.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', modal='Thêm nguyên nhân thất bại dự án', shot=shot('03-tao-moi.png'),
         shot_caption='Cửa sổ Thêm nguyên nhân thất bại dự án')
d.figure(shot('03b-tao-moi-loi.png'), 'Cửa sổ Thêm mới khi bấm Lưu mà chưa nhập nguyên nhân',
         width_in=6.2)
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([('Tiêu đề “Thêm nguyên nhân thất bại dự án”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–')]
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
     'After:\n– Ghi bản ghi mới; ghi người tạo, thời điểm tạo.\n'
     '– Ghi 1 dòng lịch sử “Tạo mới”.\n'
     '– Thông báo “Thêm mới thành công”, nạp lại danh sách.\n'
     '– Lưu: đóng cửa sổ. Lưu & Tiếp tục: giữ cửa sổ, xóa trắng form.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, không lưu dữ liệu đang nhập.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Chỉnh sửa lý do thất bại')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa lý do thất bại', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-05 Chỉnh sửa lý do thất bại')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa). '
           'Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa lý do thất bại',
    mota='Cập nhật thông tin của một nguyên nhân thất bại đang Hoạt động.',
    tacnhan='Người quản lý danh mục nguyên nhân thất bại dự án',
    dieukien='Người dùng có quyền Q1; nguyên nhân đang ở trạng thái Hoạt động.',
    chinh='1. Người dùng bấm nút Sửa trên dòng.\n'
          '2. Hệ thống mở cửa sổ “Sửa nguyên nhân thất bại dự án” với dữ liệu hiện tại.\n'
          '3. Người dùng sửa thông tin và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu, cập nhật và ghi 1 dòng lịch sử các trường đã đổi '
          '(giá trị cũ → giá trị mới).\n'
          '5. Thông báo “Cập nhật thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Nguyên nhân đang Khoá → nút Sửa bị ẩn.\n'
        '• Chọn Trạng thái = Khóa trong form → khi lưu, nguyên nhân chuyển sang Khoá và ghi thêm 1 '
        'dòng lịch sử “Thay đổi trạng thái”.\n'
        '• Bản ghi đã bị xóa / khoá bởi người khác trong lúc sửa → “Dữ liệu đã thay đổi, vui lòng '
        'tải lại”.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới ô, thông báo “Bạn chưa nhập đầy đủ thông tin”.',
    dacbiet='Dự án đã đóng với nguyên nhân này sẽ hiển thị tên nguyên nhân MỚI sau khi sửa.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', modal='Sửa nguyên nhân thất bại dự án', shot=shot('04-sua.png'),
         shot_caption='Cửa sổ Sửa nguyên nhân thất bại dự án')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Sửa nguyên nhân thất bại dự án”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Nguyên nhân thất bại', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo dữ liệu', 'Như Tạo mới.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Theo dữ liệu', '–'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Theo dữ liệu', '–'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Không có nút Lưu & Tiếp tục.'),
    FORM_ROWS[-2], FORM_ROWS[-1],
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiện với Q1 và nguyên nhân đang Hoạt động.\n'
     'During:\n– Nạp chi tiết bản ghi.\n'
     '– Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ Sửa với dữ liệu hiện tại.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Nguyên nhân không còn Hoạt động → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'During:\n' + SAVE_DURING + '\n'
     'After:\n– Cập nhật bản ghi; ghi người cập nhật, thời điểm cập nhật.\n'
     '– Ghi 1 dòng lịch sử các trường đã đổi (Tên, Mô tả); đổi Trạng thái ghi thêm dòng “Thay '
     'đổi trạng thái”.\n'
     '– Thông báo “Cập nhật thành công”, đóng cửa sổ, nạp lại danh sách.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xem chi tiết lý do thất bại')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết lý do thất bại',
    mota='Xem toàn bộ thông tin của một nguyên nhân ở chế độ chỉ đọc, kèm khối Lịch sử thay đổi.',
    tacnhan='Người quản lý / người xem danh mục nguyên nhân thất bại dự án',
    dieukien='Người dùng có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng bấm vào tên nguyên nhân trên bảng.\n'
          '2. Hệ thống mở cửa sổ “Xem nguyên nhân thất bại dự án”, mọi ô ở trạng thái chỉ đọc.\n'
          '3. (Tuỳ chọn) Người dùng bấm “Xem lịch sử” để mở rộng khối Lịch sử.\n'
          '4. Người dùng bấm Đóng để quay về danh sách.',
    phu='• Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.',
    dacbiet=None)
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', modal='Xem nguyên nhân thất bại dự án', shot=shot('05-xem.png'),
         shot_caption='Cửa sổ Xem nguyên nhân thất bại dự án')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xem nguyên nhân thất bại dự án”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Nguyên nhân thất bại', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Trạng thái', 'Dropdown', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu', '–'),
    ('Mô tả', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở danh sách thay đổi của bản ghi (như FR-09).'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Không có nút Lưu.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm tên nguyên nhân', 'Click',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'After:\n– Mở cửa sổ chi tiết ở chế độ chỉ đọc.'),
    ('Bấm “Xem lịch sử”', 'Click', 'After:\n– Mở rộng khối Lịch sử và nạp danh sách thay đổi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Xóa lý do thất bại')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xóa lý do thất bại', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-07 Xóa lý do thất bại')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa lý do thất bại',
    mota='Xóa hẳn một nguyên nhân thất bại dự án khỏi danh mục.',
    tacnhan='Người quản lý danh mục nguyên nhân thất bại dự án',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Xóa trên dòng.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận xóa”.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống xóa bản ghi, ghi 1 dòng lịch sử “Xóa”, thông báo “Xoá thành công” và nạp lại '
          'danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xóa.\n'
        '• Bản ghi đã bị xóa trước đó → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
        '• Lỗi khác → “Xoá thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Xóa là xóa hẳn, không khôi phục được. Hiện hệ thống cho xóa ở mọi trạng thái và không '
            'kiểm tra nguyên nhân đã được dùng để đóng dự án hay chưa — nên ưu tiên Khoá với nguyên '
            'nhân đã dùng.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', modal='Xác nhận xóa', shot=shot('06-xoa.png'),
         shot_caption='Hộp thoại xác nhận xóa nguyên nhân thất bại')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xác nhận xóa”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn xóa nguyên nhân thất bại \'<tên>\'?”'),
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
     'During:\n– Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'After:\n– Xóa bản ghi, ghi 1 dòng lịch sử “Xóa” kèm dữ liệu lúc xóa.\n'
     '– Thông báo “Xoá thành công”, nạp lại danh sách.'),
    ('Bấm Hủy / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Khoá / Mở khoá lý do thất bại')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Khoá / Mở khoá lý do thất bại', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-08 Khoá / Mở khoá lý do thất bại')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khoá / Mở khoá lý do thất bại',
    mota='Chuyển trạng thái nguyên nhân giữa Hoạt động và Khoá bằng thao tác Khoá / Mở khoá ở cột '
         'Hành động (nút trực tiếp hoặc trong menu “…”).',
    tacnhan='Người quản lý danh mục nguyên nhân thất bại dự án',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm Khoá (hoặc Mở khoá) trên dòng.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khoá” (hoặc “Xác nhận mở khoá”).\n'
          '3. Người dùng bấm Khoá (hoặc Mở khoá).\n'
          '4. Hệ thống đổi trạng thái, ghi 1 dòng lịch sử nhóm “Thay đổi trạng thái”, thông báo '
          '“Khoá thành công” / “Mở khoá thành công”, nạp lại danh sách.',
    phu='• Nguyên nhân đã bị người khác khoá trong lúc xác nhận → “Dữ liệu đã thay đổi, vui lòng '
        'tải lại”.\n'
        '• Bấm Hủy → không đổi trạng thái.',
    dacbiet='Nguyên nhân đang Khoá không hiện trong danh sách chọn khi đóng dự án TKT và không Sửa '
            'được cho tới khi Mở khoá.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Khoá / Mở khoá',
         modal='Xác nhận khoá / Xác nhận mở khoá',
         shot=shot('07b-khoa.png'), shot_caption='Hộp thoại xác nhận khoá nguyên nhân thất bại')
d.figure(shot('07c-mo-khoa.png'), 'Hộp thoại xác nhận mở khoá nguyên nhân thất bại', width_in=6.2)
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút / mục Khoá / Mở khoá', 'Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Đang Hoạt động: Khoá (ổ khóa đóng). Đang Khoá: Mở khoá (ổ khóa mở).'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khoá” / “Xác nhận mở khoá”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn khoá (mở khoá) nguyên nhân thất bại \'<tên>\'?”'),
    ('Nút Khoá / Mở khoá', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Khoá / Mở khoá', 'Click',
     'Before:\n– Chỉ hiện với Q1.\n'
     'After:\n– Hiện hộp thoại xác nhận tương ứng.'),
    ('Bấm Khoá', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Nguyên nhân không còn Hoạt động → “Dữ liệu đã thay đổi, vui lòng tải lại” và dừng '
     'xử lý.\n'
     'After:\n– Đổi trạng thái sang Khoá, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng thái”.\n'
     '– Thông báo “Khoá thành công”, nạp lại danh sách.'),
    ('Bấm Mở khoá', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Đổi trạng thái sang Hoạt động, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng '
     'thái”.\n– Thông báo “Mở khoá thành công”, nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Xem lịch sử thay đổi')
d.p('2.9.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung thông tin riêng của Danh mục '
           'lý do thất bại.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của lý do thất bại',
    mota='Xem các lần Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Xóa của một nguyên nhân: ai '
         'làm, lúc nào, trường nào đổi từ giá trị cũ sang giá trị mới.',
    tacnhan='Người quản lý / người xem danh mục nguyên nhân thất bại dự án',
    dieukien='Người dùng vào được màn danh sách (Q1 hoặc Q2). Lịch sử không gắn quyền riêng.',
    chinh='1. Người dùng bấm nút Lịch sử trên dòng (hoặc bấm “…” rồi chọn Lịch sử).\n'
          '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <tên nguyên nhân>” và nạp danh sách thay đổi.\n'
          '3. Người dùng bấm Đóng.',
    phu='• Chưa có thay đổi nào → hiển thị “Chưa có lịch sử thay đổi”.\n'
        '• Bấm “Bộ lọc” trong cửa sổ để lọc theo nhóm hành động.',
    dacbiet=None)
d.p('2.9.2 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Lịch sử', modal='Lịch sử thay đổi',
         shot=shot('08-lich-su.png'), shot_caption='Cửa sổ Lịch sử thay đổi của nguyên nhân thất bại')
d.p('2.9.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Lịch sử thay đổi: <tên nguyên nhân>”.'),
    ('Danh sách thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi lần thay đổi: nhóm hành động, người thực hiện kèm phòng ban, thời điểm, các trường đổi '
     '(Tên, Mô tả, Trạng thái) với giá trị cũ → giá trị mới.'),
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
d.h3('2.10 Import Excel')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Import Excel lý do thất bại', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-10 Import Excel lý do thất bại')
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Import file, Validate dữ liệu và Thông báo.', anchor='excel')
d.intro_table(
    ten='Import Excel lý do thất bại',
    mota='Thêm mới hàng loạt nguyên nhân thất bại dự án từ tệp Excel theo file mẫu. Chỉ thêm mới, '
         'không cập nhật nguyên nhân đã có.',
    tacnhan='Người quản lý danh mục nguyên nhân thất bại dự án',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm Import Excel.\n'
          '2. (Tuỳ chọn) Bấm “Tải file mẫu” để lấy tệp Mau_import_NNthatbai.xlsx.\n'
          '3. Bấm “Chọn file Excel”, chọn tệp đã điền dữ liệu.\n'
          '4. Bấm “Load lên bảng” để đọc tệp ra bảng xem trước.\n'
          '5. Bấm “Validate” → hệ thống kiểm tra từng dòng, đánh dấu dòng hợp lệ / lỗi kèm lý do; '
          'dòng hợp lệ bị khóa không sửa được.\n'
          '6. Nếu còn dòng lỗi: sửa trực tiếp các dòng lỗi rồi Validate lại, hoặc bấm “Bỏ dòng lỗi” '
          'để loại các dòng lỗi khỏi bảng.\n'
          '7. Khi đã Validate và không còn dòng lỗi, nút Import mới bấm được. Bấm “Import” → hệ thống '
          'thêm các dòng, thông báo “Import thành công <n> nguyên nhân thất bại”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Chưa Validate, hoặc còn dòng lỗi → nút Import bị khóa, không bấm được.\n'
        '• Mọi dòng đều lỗi → sau khi bỏ dòng lỗi bảng không còn dòng nào, nút Import vẫn khóa; '
        'không import được.\n'
        '• Bấm “Bỏ dòng lỗi” → “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”\n'
        '• Bấm “Xoá trạng thái validate” → bỏ đánh dấu, mở khóa các dòng để sửa; phải Validate lại.\n'
        '• Dữ liệu thay đổi giữa lúc Validate và Import (vd người khác vừa tạo bản ghi trùng tên): '
        'còn ghi được một phần → “Import thành công x/y nguyên nhân thất bại. z nguyên nhân thất bại thất bại.”, đóng cửa sổ và nạp lại '
        'danh sách; không ghi được dòng nào → báo lỗi “Không có dữ liệu hợp lệ để import”, cửa sổ '
        'giữ nguyên.\n'
        '• Tệp quá 500 dòng → “Mỗi lần import tối đa 500 dòng (file đang có N dòng), vui lòng tách '
        'file và import nhiều lần.”\n'
        '• Bật “Chỉ dòng lỗi” để lọc bảng xem trước chỉ còn dòng lỗi.\n'
        '• Bấm Làm mới → xóa dữ liệu đã nạp để chọn tệp khác.',
    dacbiet='Mỗi lần import tối đa 500 dòng. Mỗi dòng thêm thành công đều ghi 1 dòng lịch sử '
            '“Tạo mới”. So trùng tên không phân biệt hoa/thường.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Import Excel', modal='Import Nguyên nhân thất bại dự án',
         shot=shot('09-import.png'), shot_caption='Cửa sổ Import Nguyên nhân thất bại dự án')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx / .xls', 'Có', 'Hiển thị', 'Chọn tệp cần import.'),
    ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải Mau_import_NNthatbai.xlsx.'),
    ('Nút Load lên bảng', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa chọn tệp',
     'Đọc tệp ra bảng xem trước.'),
    ('Nút Validate', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu',
     'Kiểm tra dữ liệu từng dòng.'),
    ('Nút Import', 'Button', 'Enable / Disable', '–', '–', 'Disable',
     'Chỉ bấm được khi đã Validate và không còn dòng lỗi.'),
    ('Công tắc Chỉ dòng lỗi', 'Button', 'Enable', '–', '–', 'Tắt', 'Lọc bảng chỉ còn dòng lỗi.'),
    ('Cột Nguyên nhân thất bại', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo tệp',
     'Không trùng trong tệp và hệ thống.'),
    ('Cột Trạng thái', 'Textbox', 'Enable', 'Hoạt động / Khóa', 'Có', 'Theo tệp',
     'Chỉ nhận đúng chữ “Hoạt động” hoặc “Khóa”.'),
    ('Cột Mô tả', 'Textarea', 'Enable', '0–1.000 ký tự', 'Không', 'Theo tệp', '–'),
    ('Dòng Tổng / hợp lệ / lỗi', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', 'Thống kê sau Validate.'),
    ('Nút Bỏ dòng lỗi', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu', 'Loại các dòng lỗi khỏi bảng xem trước.'),
    ('Nút Xoá trạng thái validate', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu',
     'Bỏ kết quả Validate để sửa lại dữ liệu.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không import.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa dữ liệu đã nạp.'),
])
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Validate', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Tệp quá 500 dòng → báo “Mỗi lần import tối đa 500 dòng …” và dừng xử lý.\n'
     'During (từng dòng):\n'
     '– Tên trống → “Nguyên nhân thất bại không được để trống”; quá dài → “Nguyên nhân thất bại '
     'vượt quá độ dài cho phép (tối đa 255 ký tự)”.\n'
     '– Tên trùng trong tệp → “Nguyên nhân thất bại bị trùng lặp trong file import (dòng n)”; trùng '
     'hệ thống → “Nguyên nhân thất bại đã tồn tại trong hệ thống”.\n'
     '– Trạng thái trống hoặc sai → “Trạng thái không hợp lệ (chỉ nhận đúng: Hoạt động hoặc Khóa)”.\n'
     '– Mô tả quá dài → “Mô tả vượt quá độ dài cho phép (tối đa 1000 ký tự)”.\n'
     'After:\n– Đánh dấu từng dòng hợp lệ / lỗi; thông báo “Validate thành công” hoặc “Validate xong: '
     'x hợp lệ, y không hợp lệ”.'),
    ('Bấm Bỏ dòng lỗi', 'Click',
     'Before:\n– Chưa Validate → “Hãy Validate trước rồi mới bỏ dòng lỗi.”\n'
     'After:\n– Loại các dòng lỗi khỏi bảng; thông báo “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”\n'
     '– Nút Import mở nếu còn ≥ 1 dòng.'),
    ('Bấm Import', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Nút chỉ bấm được khi đã Validate và không còn dòng lỗi.\n'
     'During:\n– Máy chủ kiểm tra lại các dòng gửi lên như bước Validate.\n'
     'After:\n– Tất cả thành công → thêm mới các dòng, ghi lịch sử “Tạo mới” từng dòng; thông báo '
     '“Import thành công <n> nguyên nhân thất bại”, đóng cửa sổ, nạp lại danh sách.\n'
     '– Một phần (dữ liệu thay đổi giữa lúc Validate và Import) → chỉ thêm các dòng còn hợp lệ; '
     'thông báo “Import thành công x/y nguyên nhân thất bại. z nguyên nhân thất bại thất bại.”, đóng cửa sổ, nạp lại danh sách.\n'
     '– Không dòng nào ghi được → báo lỗi “Không có dữ liệu hợp lệ để import”; cửa sổ giữ nguyên, '
     'không thêm dữ liệu.'),
    ('Bấm Tải file mẫu', 'Click', 'After:\n– Tải tệp Mau_import_NNthatbai.xlsx.'),
])

# ---------------------------------------------------------------- 2.11
d.h3('2.11 Xuất Excel')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Xuất Excel danh sách lý do thất bại', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-11 Xuất Excel')
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của '
           'Danh mục lý do thất bại.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách lý do thất bại',
    mota='Người dùng chọn các trường cần xuất rồi tải về tệp danh_sach_nguyen_nhan_that_bai_du_an.xlsx '
         'gồm TẤT CẢ nguyên nhân khớp bộ lọc đang áp dụng (không chỉ trang đang xem).',
    tacnhan='Người quản lý danh mục nguyên nhân thất bại dự án',
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
     'Nguyên nhân thất bại dự án, Mô tả, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật, Trạng '
     'thái. Kéo ⠿ để đổi thứ tự.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn nhanh.'),
    ('Dòng “Đang chọn x/7 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Tải tệp danh_sach_nguyen_nhan_that_bai_du_an.xlsx.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Nút chỉ hiện với Q1.\n'
     'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiện trên bảng.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Áp đúng bộ lọc đang dùng trên màn, lấy tất cả dòng khớp.\n'
     'After:\n– Tải tệp với các trường đã chọn theo thứ tự đã sắp.\n'
     '– Thông báo “Xuất Excel thành công”.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Danh mục lý do thất bại; không lặp lại các '
           'quy tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Tên nguyên nhân', [
        '– Bắt buộc, tối đa 255 ký tự, không trùng với nguyên nhân khác.',
        '– Khi import: so trùng không phân biệt hoa/thường, bỏ khoảng trắng đầu cuối.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-02', 'Chỉ sửa nguyên nhân đang Hoạt động',
     '– Nguyên nhân đang Khoá không sửa được (nút Sửa bị ẩn); phải Mở khoá trước.',
     ['Chỉnh sửa', 'Danh sách']),
    ('BR-03', 'Điều kiện Xóa', [
        '– Người có Q1 xóa được nguyên nhân ở mọi trạng thái.',
        '– Xóa là xóa hẳn, không khôi phục được.',
    ], 'Xóa'),
    ('BR-04', 'Khoá / Mở khoá', [
        '– Chỉ Khoá được nguyên nhân đang Hoạt động; Mở khoá luôn được phép.',
        '– Chọn Trạng thái = Khóa trong form Sửa tương đương thao tác Khoá.',
    ], ['Khoá / Mở khoá', 'Chỉnh sửa']),
    ('BR-05', 'Dùng khi đóng dự án TKT', [
        '– Khi đóng dự án TKT, người dùng bắt buộc chọn 1 nguyên nhân; danh sách chọn chỉ gồm '
        'nguyên nhân đang Hoạt động.',
    ], 'Đóng dự án TKT (màn nghiệp vụ)'),
    ('BR-06', 'Lý do hệ thống tự đóng dự án', [
        '– Khi dự án quá thời gian thực hiện, hệ thống tự đóng và gán nguyên nhân “Hệ thống tự đóng '
        'do quá thời gian thực hiện” (tìm theo đúng tên).',
        '– Không còn nguyên nhân có đúng tên này (bị đổi tên / xóa) → hệ thống tự tạo lại, người tạo '
        'để trống.',
    ], ['Danh sách', 'Chỉnh sửa', 'Xóa']),
    ('BR-07', 'Thao tác không dùng được thì ẩn', [
        '– Sửa, Xóa, Khoá / Mở khoá, Import, Xuất Excel chỉ hiện với người có Q1; Sửa còn cần '
        'nguyên nhân đang Hoạt động.',
        '– Không hiển thị nút xám.',
    ], 'Danh sách'),
    ('BR-08', 'Ghi lịch sử thay đổi', [
        '– Ghi lại mọi lần Tạo mới (kể cả qua Import), Thay đổi thông tin, Thay đổi trạng thái, Xóa.',
        '– Cập nhật chỉ ghi các trường thực sự đổi: Tên, Mô tả, Trạng thái.',
        '– Ai vào được màn đều xem được lịch sử.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xóa', 'Khoá / Mở khoá', 'Import Excel', 'Xem lịch sử']),
    ('BR-09', 'Import chỉ thêm mới', [
        '– Mỗi lần tối đa 500 dòng.',
        '– Tên đã có trong hệ thống hoặc trùng nhau trong tệp → dòng lỗi, không ghi đè.',
        '– Chỉ các dòng hợp lệ được thêm; dòng lỗi được báo lý do cụ thể.',
    ], 'Import Excel'),
    ('BR-10', 'Xuất theo bộ lọc, chọn trường', [
        '– Xuất tất cả dòng khớp bộ lọc đang áp dụng, không giới hạn theo trang.',
        '– Người dùng chọn trường và thứ tự trường; mặc định là các cột đang hiện trên bảng.',
    ], 'Xuất Excel'),
])

d.save(update_fields=False)

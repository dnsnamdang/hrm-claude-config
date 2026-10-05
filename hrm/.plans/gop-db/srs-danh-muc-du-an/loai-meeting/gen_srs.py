# -*- coding: utf-8 -*-
"""Sinh "SRS - Danh mục loại meeting.docx" theo code nhánh gop_db — form 2026-09-24.

Chạy:  python3 .plans/gop-db/srs-danh-muc-du-an/loai-meeting/gen_srs.py
Ảnh chụp thật (Playwright 1440x900, bản gop_db cổng 3002): loai-meeting_shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/meeting_type/index.vue · components/modal/meeting-type-modal.vue
      components/modal/CatalogHistoryModal.vue · components/assign/SystemInfoSection.vue
      components/subsystem-menu/meeting.js (menu) · components/subsystems.js (phân hệ "Meeting")
  BE  Modules/Assign/Routes/api.php (nhóm /assign/meeting_types)
      Http/Requests/MeetingType/MeetingTypeRequest.php · Http/Controllers/Api/V1/MeetingTypeController.php
      Services/MeetingTypeService.php · Entities/MeetingType.php
      Transformers/MeetingType/{MeetingTypeResource, DetailMeetingTypeResource}.php
      app/Http/Middleware/CheckImportRowLimit.php (500 dòng / lần import)
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 989, 1004)
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

OUT = os.path.join(HERE, 'SRS - Danh mục loại meeting.docx')
SHOTS = os.path.join(HERE, 'loai-meeting_shots')
MENU = 'Phân hệ Meeting => Danh mục => Loại meeting'

A_QL = 'Người quản lý danh mục loại meeting (Q1)'
A_XEM = 'Người xem danh mục loại meeting (Q2)'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/meeting_type',
           full_url='https://<host-hrm>/assign/meeting_type', img_prefix='loaimeeting_gopdb_')

# Icon cho từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện.
# "Mở khóa": cắt nút ổ khóa mở trên dòng loại meeting test đang Khóa (dữ liệu tạo trên local).
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ Meeting': 'phanhe', 'Danh mục': 'danhmuc', 'Loại meeting': 'loaimeeting',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidatboloc', 'Tuỳ chỉnh cột': 'tuychinhcot',
    'Tạo mới': 'taomoi', 'Sửa': 'sua', 'Xem chi tiết': 'xem', 'Xóa': 'xoa', 'Xóa nhiều': 'xoanhieu',
    'Hành động khác': 'khac', 'Khóa': 'khoa', 'Mở khóa': 'mokhoa_btn', 'Lịch sử': 'lichsu',
    'Import Excel': 'import', 'Xuất Excel': 'xuat',
}.items()})

d.title_block('Danh mục loại meeting')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục loại meeting (tiêu đề trên màn: '
    '“Quản lý loại meeting”) thuộc phân hệ Meeting, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ ràng buộc giữa Loại meeting với các cuộc họp (meeting) đang sử dụng nó: khi nào được '
    'sửa, xóa, khóa.',
    'Làm rõ quy tắc với bản ghi hệ thống (loại meeting do hệ thống cài sẵn, không được thay đổi).',
    'Làm rõ quy tắc nhập dữ liệu hàng loạt, xóa nhiều và xuất dữ liệu ra tệp Excel.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Loại meeting', 'Phân loại cuộc họp (VD: Meeting nội bộ, Meeting với khách hàng, Họp giao '
     'ban…). Được chọn khi tạo cuộc họp ở phân hệ Meeting.'),
    ('Có khách hàng', 'Cờ cho biết loại meeting này có khách hàng tham dự hay không (lịch họp '
     'thuộc loại này sẽ gắn với khách hàng).'),
    ('Bản ghi hệ thống', 'Loại meeting do hệ thống cài sẵn (VD “Họp tìm hiểu & Giới thiệu sản '
     'phẩm”). Không Sửa, Xóa, Khóa / Mở khóa được và không chọn được để xóa nhiều.'),
    ('Loại meeting đã sử dụng', 'Loại meeting đã được ít nhất 1 cuộc họp chọn.'),
    ('Trạng thái Khóa', 'Loại meeting ngừng sử dụng: không được chọn ở màn tạo cuộc họp, không sửa '
     'được. Khóa KHÔNG xóa dữ liệu, có thể Mở khóa lại.'),
    ('Menu “…” (Hành động khác)', 'Nút ở cột Hành động chứa các thao tác còn lại của dòng khi dòng '
     'có nhiều hơn 3 thao tác.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý danh mục loại meeting',
     'Xem danh sách, xem chi tiết, xem lịch sử; hiện nút Tạo mới, Import Excel; hiện các thao tác '
     'Sửa, Xóa, Khóa / Mở khóa trên dòng; được Xóa nhiều và Xuất Excel.'),
    ('Q2', 'Xem danh mục loại meeting',
     'Xem danh sách, tìm kiếm, xem chi tiết và xem lịch sử. Không được thay đổi dữ liệu.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn hình không phân quyền theo cấp dữ liệu (công ty / phòng ban / bộ phận): người có quyền '
    'xem được toàn bộ loại meeting của hệ thống. Mục menu Loại meeting chỉ hiện với người có Q1 '
    'hoặc Q2.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách loại meeting', '✅', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '❌'),
    ('FR-04 Tạo mới loại meeting', '✅', '❌', '❌'),
    ('FR-05 Chỉnh sửa loại meeting', '✅', '❌', '❌'),
    ('FR-06 Xem chi tiết loại meeting', '✅', '✅', '❌'),
    ('FR-07 Xóa loại meeting', '✅', '❌', '❌'),
    ('FR-08 Xóa nhiều loại meeting', '✅', '❌', '❌'),
    ('FR-09 Khóa / Mở khóa loại meeting', '✅', '❌', '❌'),
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
    [('FR-01', 'Xem danh sách loại meeting', 'view'),
     ('FR-04', 'Tạo mới loại meeting', 'crud'),
     ('FR-05', 'Chỉnh sửa loại meeting', 'crud'),
     ('FR-07', 'Xóa loại meeting', 'action'),
     ('FR-08', 'Xóa nhiều loại meeting', 'action'),
     ('FR-09', 'Khóa / Mở khóa loại meeting', 'action'),
     ('FR-11', 'Import Excel loại meeting', 'io'),
     ('FR-12', 'Xuất Excel danh sách loại meeting', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết loại meeting', 'view', 'extend', [0], None),
     ('FR-10', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Danh mục loại meeting')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách loại meeting')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Danh mục loại meeting tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách loại meeting',
    mota='Hiển thị toàn bộ loại meeting kèm mô tả, người tạo / cập nhật, trạng thái và các thao tác '
         'trên từng dòng. Bảng không có cột Mã: Tên loại meeting là cột định danh.',
    tacnhan='Người quản lý / người xem danh mục loại meeting; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng vào menu Phân hệ Meeting → Danh mục → Loại meeting.\n'
          '2. Hệ thống nạp trang 1, 10 dòng/trang, bản ghi mới tạo lên đầu.\n'
          '3. Bảng hiển thị đủ các cột (mặc định hiện hết cột), dòng “Hiển thị a–b / N” và thanh '
          'phân trang.',
    phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm Tên loại meeting → mở cửa sổ Xem chi tiết (FR-06).\n'
        '• Bấm tiêu đề cột Tên loại meeting, Ngày tạo, Ngày cập nhật → sắp xếp theo cột đó, bấm '
        'lại để đảo chiều.\n'
        '• Tích ô chọn ở đầu dòng → hiện thanh “Đã chọn n dòng” với nút Xóa, Bỏ chọn (FR-08).\n'
        '• Rời màn rồi quay lại trong vòng 10 phút → bộ lọc đang dùng được khôi phục.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách loại meeting lúc mới truy cập')
d.figure(shot('07-menu-khac.png'), 'Cột Trạng thái, cột Hành động và menu “…” của một dòng',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Quản lý loại meeting”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Dòng “Chưa chọn dòng nào.” / “Đã chọn n dòng”', 'Label', 'Hiển thị', '–', '“Chưa chọn dòng nào.”',
     'Khi đã chọn dòng thì kèm nút Xóa và Bỏ chọn (FR-08).'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1', 'Mở form Tạo mới (FR-04).'),
    ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1',
     'Mở cửa sổ Import (FR-11).'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Chọn trường xuất file (FR-12).'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Cột Chọn (ô tích)', 'Table/Grid', 'Enable / Disable', '–', 'Chưa tích',
     'Ô tích ở tiêu đề chọn cả trang. Chỉ tích được loại meeting đủ điều kiện xóa; bản ghi hệ '
     'thống không có ô tích. Cố định bên trái, không tắt được.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cố định bên trái khi cuộn ngang; không tắt được.'),
    ('Cột Tên loại meeting', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Cố định bên trái, không tắt được, sắp xếp được; tối đa 2 dòng. Là liên kết mở cửa sổ Xem '
     'chi tiết.'),
    ('Cột Mô tả', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Người tạo hiển thị tên nhân viên. Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu',
     'Hoạt động màu xanh, Khóa màu đỏ. Bản ghi hệ thống: rê chuột hiện “Bản ghi hệ thống — không '
     'khóa / sửa / xóa được”.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu',
     'Không tắt được. Thứ tự Sửa, Xóa, Khóa / Mở khóa, Lịch sử. Dòng có tối đa 3 thao tác thì '
     'hiện hết; nhiều hơn thì hiện 2 nút đầu, phần còn lại gom vào nút “…”. Thao tác không dùng '
     'được thì ẨN hẳn.'),
    ('Nút Sửa (bút)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1, loại meeting không phải bản ghi hệ thống, đang Hoạt động và chưa được cuộc '
     'họp nào sử dụng (FR-05).'),
    ('Nút Xóa (thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1, không phải bản ghi hệ thống và chưa được cuộc họp nào sử dụng (FR-07).'),
    ('Nút / mục Khóa / Mở khóa', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Chỉ hiện với Q1 và không phải bản ghi hệ thống. Đang Hoạt động hiện Khóa, đang Khóa hiện Mở '
     'khóa (FR-09).'),
    ('Nút / mục Lịch sử', 'Button', 'Enable', '–', 'Hiển thị', 'Mọi người vào được màn đều thấy (FR-10).'),
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
    ('Bấm Tên loại meeting', 'Click', 'After:\n– Mở cửa sổ Xem chi tiết loại meeting (FR-06).'),
    ('Tích / bỏ tích ô chọn', 'Change',
     'After:\n– Cập nhật số dòng đã chọn; hiện nút Xóa, Bỏ chọn khi có ít nhất 1 dòng được chọn.'),
    ('Bấm nút “…” ở cột Hành động', 'Click',
     'After:\n– Mở menu các thao tác còn lại của dòng (Khóa / Mở khóa, Lịch sử).'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Danh mục '
           'loại meeting tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc loại meeting',
    mota='Tìm nhanh theo tên loại meeting hoặc tên người tạo; lọc nâng cao theo tên, trạng thái, '
         'người tạo, người cập nhật, khoảng ngày cập nhật.',
    tacnhan='Người quản lý / người xem danh mục loại meeting; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách loại meeting.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
          '3. Ô chọn (Trạng thái, Người tạo, Người cập nhật, Ngày cập nhật): chọn xong hệ thống tự '
          'lọc lại ngay.\n'
          '4. Ô gõ tay (Tên loại meeting): hệ thống chỉ lọc khi bấm Enter hoặc nút Tìm kiếm.\n'
          '5. Bảng hiển thị kết quả từ trang 1.',
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
     'Placeholder “Tìm theo tên loại meeting, người tạo”. Tìm gần đúng theo tên loại meeting hoặc '
     'họ tên người tạo. Áp dụng khi bấm Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao (nhãn đổi thành “Ẩn tìm kiếm nâng cao” khi đang mở).'),
    ('Tên loại meeting', 'Textbox', 'Enable', '–', 'Không', 'Trống', 'Lọc gần đúng theo tên.'),
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
    ('Gõ vào ô Tên loại meeting trong khối lọc', 'Keypress',
     'After:\n– Chưa lọc; chờ Enter hoặc nút Tìm kiếm.'),
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
    dieukien='Đang ở màn danh sách loại meeting.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ với danh sách trường / cột, đánh dấu những mục đang hiện.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho người dùng, đóng cửa sổ và vẽ lại khối lọc / bảng.',
    phu='• Bấm “Khôi phục mặc định” → trả về bộ trường lọc mặc định của màn.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Cột Chọn, STT, Tên loại meeting và Hành động luôn hiện, không bỏ tích được (hiển thị '
        'xám + ổ khóa).',
    dacbiet='Mặc định màn hiện TẤT CẢ cột; người dùng tự tắt bớt nếu thấy bảng quá rộng.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột', modal='Cài đặt bộ lọc và Tuỳ chỉnh cột',
         shot=shot('02b-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('02c-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột — cột khóa hiển thị xám', width_in=6.2)
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách trường lọc', 'Table/Grid', 'Enable', '5 trường', 'Không', 'Theo cấu hình đã lưu',
     'Tên loại meeting, Trạng thái, Người tạo, Người cập nhật, Ngày cập nhật. Mỗi dòng: số thứ '
     'tự, biểu tượng kéo ⠿, ô tích, tên trường.'),
    ('Nút Lưu (Cài đặt bộ lọc)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình trường lọc.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về bộ trường lọc mặc định.'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '10 cột', 'Không', 'Theo cấu hình đã lưu',
     'Cột Chọn, STT, Tên loại meeting, Hành động bị khóa (luôn hiện).'),
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
    ('Loại meeting', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Tên loại meeting, không trùng với loại meeting khác. Placeholder “VD: Meeting hàng tuần / '
     'Meeting hàng tháng / ...”.'),
    ('Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Không', 'Hoạt động',
     'Không có nút xóa chọn — luôn có giá trị.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Trống', 'Placeholder “Mô tả loại meeting”.'),
    ('Có khách hàng', 'Checkbox', 'Enable', 'Có / Không', 'Không', 'Đã tích',
     'Bấm vào ô tích hoặc chữ “Có khách hàng” để đổi.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô bị lỗi.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
]
SAVE_DURING = (
    '– Loại meeting trống → “Bắt buộc phải nhập”.\n'
    '– Loại meeting quá 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”\n'
    '– Loại meeting trùng tên loại meeting khác → “Đã tồn tại trên hệ thống”.\n'
    '– Nếu có lỗi validate → thông báo “Bạn chưa nhập đầy đủ thông tin” và không thực hiện bước After.')

d.h3('2.4 Tạo mới loại meeting')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới loại meeting', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-04 Tạo mới loại meeting')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới loại meeting',
    mota='Thêm một loại meeting mới vào danh mục.',
    tacnhan='Người quản lý danh mục loại meeting',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở cửa sổ “Thêm loại meeting”, Trạng thái mặc định Hoạt động, ô “Có khách '
          'hàng” tích sẵn.\n'
          '3. Người dùng nhập Loại meeting, Mô tả (nếu có), chọn Trạng thái, tích / bỏ tích Có '
          'khách hàng.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống kiểm tra dữ liệu, ghi bản ghi mới và ghi 1 dòng lịch sử “Tạo mới”.\n'
          '6. Thông báo “Thêm mới thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Bấm “Lưu & Tiếp tục” → lưu xong giữ cửa sổ mở, xóa trắng form để nhập bản ghi tiếp.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu đã nhập.\n'
        '• Lỗi khác → thông báo “Thêm mới thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Nút Lưu và Lưu & Tiếp tục bị khóa trong lúc đang xử lý để tránh tạo trùng. Không nhập '
            'được mã: loại meeting do người dùng tạo không có mã.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', modal='Thêm loại meeting', shot=shot('03-tao-moi.png'),
         shot_caption='Cửa sổ Thêm loại meeting')
d.figure(shot('03b-tao-moi-loi.png'), 'Cửa sổ Thêm loại meeting khi bấm Lưu mà chưa nhập tên',
         width_in=6.2)
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([('Tiêu đề “Thêm loại meeting”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–')]
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
     'After:\n– Mở cửa sổ với form trống, Trạng thái = Hoạt động, Có khách hàng = đã tích.'),
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
d.h3('2.5 Chỉnh sửa loại meeting')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa loại meeting', 'crud', actor=A_QL,
            caption='Biểu đồ Use Case — FR-05 Chỉnh sửa loại meeting')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa). '
           'Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa loại meeting',
    mota='Cập nhật thông tin của một loại meeting đang Hoạt động và chưa được cuộc họp nào sử dụng.',
    tacnhan='Người quản lý danh mục loại meeting',
    dieukien='Người dùng có quyền Q1; loại meeting không phải bản ghi hệ thống, đang Hoạt động và '
             'chưa được cuộc họp nào sử dụng.',
    chinh='1. Người dùng bấm nút Sửa trên dòng loại meeting.\n'
          '2. Hệ thống mở cửa sổ “Sửa loại meeting” với dữ liệu hiện tại.\n'
          '3. Người dùng sửa thông tin và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu, cập nhật và ghi 1 dòng lịch sử các trường đã đổi '
          '(giá trị cũ → giá trị mới).\n'
          '5. Thông báo “Cập nhật thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Loại meeting đang Khóa, đã được sử dụng hoặc là bản ghi hệ thống → nút Sửa bị ẩn.\n'
        '• Chọn Trạng thái = Khóa trong form → khi lưu, loại meeting chuyển sang Khóa và ghi 1 '
        'dòng lịch sử “Thay đổi trạng thái” riêng.\n'
        '• Bản ghi đã bị xóa / khóa bởi người khác trong lúc sửa → “Dữ liệu đã thay đổi, vui lòng '
        'tải lại”.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới ô, thông báo “Bạn chưa nhập đầy đủ thông tin”.',
    dacbiet='Bản ghi hệ thống bị chặn sửa ở máy chủ: “Loại meeting hệ thống, không được phép sửa.”')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', modal='Sửa loại meeting', shot=shot('04-sua.png'),
         shot_caption='Cửa sổ Sửa loại meeting')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Sửa loại meeting”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Loại meeting', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo dữ liệu', 'Như Tạo mới.'),
    ('Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Không', 'Theo dữ liệu',
     'Bị khóa khi loại meeting không được phép khóa (bản ghi hệ thống).'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Theo dữ liệu', '–'),
    ('Có khách hàng', 'Checkbox', 'Enable', 'Có / Không', 'Không', 'Theo dữ liệu', '–'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Không có nút Lưu & Tiếp tục.'),
    FORM_ROWS[-2], FORM_ROWS[-1],
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiện với Q1, loại meeting không phải bản ghi hệ thống, đang Hoạt động và '
     'chưa được sử dụng.\n'
     'During:\n– Nạp chi tiết bản ghi.\n'
     '– Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ Sửa với dữ liệu hiện tại.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Bản ghi hệ thống → “Loại meeting hệ thống, không được phép sửa.” và dừng xử lý.\n'
     '– Loại meeting không còn Hoạt động → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'During:\n' + SAVE_DURING + '\n'
     'After:\n– Cập nhật bản ghi; ghi người cập nhật, thời điểm cập nhật.\n'
     '– Ghi 1 dòng lịch sử các trường đã đổi (Tên, Có khách hàng, Mô tả); đổi Trạng thái ghi '
     'thêm dòng “Thay đổi trạng thái”.\n'
     '– Thông báo “Cập nhật thành công”, đóng cửa sổ, nạp lại danh sách.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xem chi tiết loại meeting')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết loại meeting',
    mota='Xem toàn bộ thông tin của một loại meeting ở chế độ chỉ đọc, kèm khối Lịch sử thay đổi.',
    tacnhan='Người quản lý / người xem danh mục loại meeting',
    dieukien='Người dùng có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng bấm vào Tên loại meeting trên bảng.\n'
          '2. Hệ thống mở cửa sổ “Xem loại meeting”, mọi ô ở trạng thái chỉ đọc.\n'
          '3. (Tuỳ chọn) Người dùng bấm “Xem lịch sử” để mở rộng khối Lịch sử.\n'
          '4. Người dùng bấm Đóng để quay về danh sách.',
    phu='• Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.',
    dacbiet=None)
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', modal='Xem loại meeting', shot=shot('05-xem.png'),
         shot_caption='Cửa sổ Xem loại meeting')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xem loại meeting”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
    ('Loại meeting', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Trạng thái', 'Dropdown', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu', '–'),
    ('Mô tả', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Có khách hàng', 'Checkbox', 'Read-only', 'Có / Không', 'Theo dữ liệu', '–'),
    ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở danh sách thay đổi của bản ghi (như FR-10).'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Không có nút Lưu.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tên loại meeting', 'Click',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'After:\n– Mở cửa sổ chi tiết ở chế độ chỉ đọc.'),
    ('Bấm “Xem lịch sử”', 'Click', 'After:\n– Mở rộng khối Lịch sử và nạp danh sách thay đổi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Xóa loại meeting')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xóa loại meeting', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-07 Xóa loại meeting')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa loại meeting',
    mota='Xóa hẳn một loại meeting chưa được cuộc họp nào sử dụng.',
    tacnhan='Người quản lý danh mục loại meeting',
    dieukien='Người dùng có quyền Q1; loại meeting không phải bản ghi hệ thống và chưa được cuộc '
             'họp nào sử dụng.',
    chinh='1. Người dùng bấm nút Xóa trên dòng loại meeting.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận xóa”.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống xóa bản ghi, ghi 1 dòng lịch sử “Xóa”, thông báo “Xóa thành công” và nạp lại '
          'danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xóa.\n'
        '• Loại meeting đã được sử dụng → nút Xóa bị ẩn; nếu phát sinh cuộc họp dùng loại này '
        'trong lúc đang xác nhận → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
        '• Bản ghi đã bị xóa trước đó → “Dữ liệu đã thay đổi, vui lòng tải lại”.',
    dacbiet='Xóa là xóa hẳn, không khôi phục được. Muốn ngừng dùng loại meeting đã được sử dụng '
            'thì dùng chức năng Khóa.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', modal='Xác nhận xóa', shot=shot('06-xoa.png'),
         shot_caption='Hộp thoại xác nhận xóa loại meeting')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xác nhận xóa”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu', '“Bạn có chắc muốn xóa loại meeting \'<tên>\'?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
], required=False, scope=False)
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện với Q1, loại meeting không phải bản ghi hệ thống và chưa được sử dụng.\n'
     'After:\n– Hiện hộp thoại xác nhận.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Bản ghi hệ thống → “Loại meeting hệ thống, không được phép xoá.” và dừng xử lý.\n'
     'During:\n– Đã có cuộc họp sử dụng → “Dữ liệu đã thay đổi, vui lòng tải lại” và dừng xử lý.\n'
     '– Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'After:\n– Xóa bản ghi, ghi 1 dòng lịch sử “Xóa” kèm dữ liệu lúc xóa.\n'
     '– Thông báo “Xóa thành công”, nạp lại danh sách.'),
    ('Bấm Hủy / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Xóa nhiều loại meeting')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Xóa nhiều loại meeting', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-08 Xóa nhiều loại meeting')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
           'Quy tắc ghi lịch sử.', anchor='delete')
d.intro_table(
    ten='Xóa nhiều loại meeting',
    mota='Chọn nhiều loại meeting bằng ô tích đầu dòng rồi xóa cùng lúc.',
    tacnhan='Người quản lý danh mục loại meeting',
    dieukien='Người dùng có quyền Q1; đã tích chọn ít nhất 1 loại meeting đủ điều kiện xóa.',
    chinh='1. Người dùng tích ô chọn ở các dòng cần xóa (hoặc ô tích ở tiêu đề để chọn cả trang).\n'
          '2. Hệ thống hiện “Đã chọn n dòng” cùng nút Xóa, Bỏ chọn.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống hiện hộp thoại “Xác nhận xóa nhiều”.\n'
          '5. Người dùng bấm Xóa.\n'
          '6. Hệ thống xóa các bản ghi đã chọn, ghi lịch sử “Xóa” cho từng bản ghi, thông báo “Xóa '
          'thành công n loại meeting”, bỏ chọn và nạp lại danh sách.',
    phu='• Bấm Bỏ chọn → bỏ tích tất cả.\n'
        '• Dòng không đủ điều kiện xóa (đã được sử dụng) → ô tích bị khóa; bản ghi hệ thống không '
        'có ô tích.\n'
        '• Danh sách chọn có bản ghi hệ thống → “Danh sách chứa loại meeting hệ thống, không được '
        'phép xoá.”\n'
        '• Có bản ghi đã bị xóa trước đó → báo lỗi, không xóa bản ghi nào.\n'
        '• Lỗi khác → “Lỗi khi xóa nhiều loại meeting”.',
    dacbiet='Lựa chọn chỉ giữ các dòng còn hiển thị trên trang hiện tại; đổi trang / lọc lại thì '
            'các dòng không còn trên bảng tự bỏ chọn.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa nhiều', modal='Xác nhận xóa nhiều', shot=shot('06b-chon-nhieu.png'),
         shot_caption='Thanh thao tác khi đã chọn dòng')
d.figure(shot('06c-xoa-nhieu.png'), 'Hộp thoại xác nhận xóa nhiều loại meeting', width_in=6.2)
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tích đầu dòng / tiêu đề', 'Checkbox', 'Enable / Disable', 'Theo dữ liệu',
     'Chỉ tích được loại meeting đủ điều kiện xóa.'),
    ('Dòng “Đã chọn n dòng”', 'Label', 'Hiển thị', 'Ẩn khi chưa chọn', '–'),
    ('Nút Xóa (đỏ)', 'Button', 'Enable', 'Ẩn khi chưa chọn', 'Mở hộp thoại xác nhận xóa nhiều.'),
    ('Nút Bỏ chọn', 'Button', 'Enable', 'Ẩn khi chưa chọn', 'Bỏ tích tất cả.'),
    ('Tiêu đề “Xác nhận xóa nhiều”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu', '“Bạn có chắc muốn xóa n loại meeting đã chọn?”'),
    ('Nút Xóa / Hủy trong hộp thoại', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa / đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xóa trên thanh thao tác', 'Click',
     'Before:\n– Chưa chọn dòng nào → “Vui lòng chọn ít nhất một loại meeting để xóa”.\n'
     'After:\n– Hiện hộp thoại xác nhận xóa nhiều.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Có bản ghi hệ thống trong danh sách → “Danh sách chứa loại meeting hệ thống, không được '
     'phép xoá.” và dừng xử lý.\n'
     'During:\n– Có bản ghi không còn tồn tại → báo lỗi, không xóa bản ghi nào.\n'
     'After:\n– Xóa toàn bộ bản ghi đã chọn (hoặc không xóa bản ghi nào nếu có lỗi); ghi lịch sử '
     '“Xóa” từng bản ghi.\n'
     '– Thông báo “Xóa thành công n loại meeting”, bỏ chọn, nạp lại danh sách.'),
    ('Bấm Bỏ chọn', 'Click', 'After:\n– Bỏ tích tất cả các dòng.'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Khóa / Mở khóa loại meeting')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Khóa / Mở khóa loại meeting', 'action', actor=A_QL,
            caption='Biểu đồ Use Case — FR-09 Khóa / Mở khóa loại meeting')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khóa / Mở khóa loại meeting',
    mota='Chuyển trạng thái loại meeting giữa Hoạt động và Khóa bằng thao tác Khóa / Mở khóa ở '
         'cột Hành động (nút trực tiếp hoặc trong menu “…”).',
    tacnhan='Người quản lý danh mục loại meeting',
    dieukien='Người dùng có quyền Q1; loại meeting không phải bản ghi hệ thống.',
    chinh='1. Người dùng bấm Khóa (hoặc Mở khóa) trên dòng loại meeting.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khóa” (hoặc “Xác nhận mở khóa”).\n'
          '3. Người dùng bấm Khóa (hoặc Mở khóa).\n'
          '4. Hệ thống đổi trạng thái, ghi 1 dòng lịch sử nhóm “Thay đổi trạng thái”, thông báo '
          '“Khóa thành công” / “Mở khóa thành công”, nạp lại danh sách.',
    phu='• Loại meeting đã được cuộc họp sử dụng VẪN khóa được (các cuộc họp cũ giữ nguyên).\n'
        '• Loại meeting đã bị người khác khóa trong lúc xác nhận → “Dữ liệu đã thay đổi, vui lòng '
        'tải lại”.\n'
        '• Bấm Hủy → không đổi trạng thái.',
    dacbiet='Loại meeting đang Khóa không Sửa được cho tới khi Mở khóa và không hiện ở danh sách '
            'chọn loại meeting khi tạo cuộc họp (trừ cuộc họp đang dùng nó).')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Khóa / Mở khóa',
         modal='Xác nhận khóa / Xác nhận mở khóa',
         shot=shot('07b-khoa.png'), shot_caption='Hộp thoại xác nhận khóa loại meeting')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút / mục Khóa / Mở khóa', 'Button', 'Enable / Ẩn', 'Theo dữ liệu',
     'Đang Hoạt động: Khóa (ổ khóa đóng). Đang Khóa: Mở khóa (ổ khóa mở).'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khóa” / “Xác nhận mở khóa”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn khóa (mở khóa) loại meeting \'<tên>\'?”'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Khóa / Mở khóa', 'Click',
     'Before:\n– Chỉ hiện với Q1 và loại meeting không phải bản ghi hệ thống.\n'
     'After:\n– Hiện hộp thoại xác nhận tương ứng.'),
    ('Bấm Khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Bản ghi hệ thống → “Loại meeting hệ thống, không được phép khoá.”\n'
     'During:\n– Loại meeting không còn Hoạt động → “Dữ liệu đã thay đổi, vui lòng tải lại” và '
     'dừng xử lý.\n'
     'After:\n– Đổi trạng thái sang Khóa, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng thái”.\n'
     '– Thông báo “Khóa thành công”, nạp lại danh sách.'),
    ('Bấm Mở khóa', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Bản ghi hệ thống → “Loại meeting hệ thống, không được phép mở khoá.”\n'
     'After:\n– Đổi trạng thái sang Hoạt động, ghi người cập nhật và 1 dòng lịch sử “Thay đổi trạng '
     'thái”.\n– Thông báo “Mở khóa thành công”, nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.10
d.h3('2.10 Xem lịch sử thay đổi')
d.p('2.10.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung thông tin riêng của Danh mục '
           'loại meeting.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của loại meeting',
    mota='Xem các lần Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Xóa của một loại meeting: '
         'ai làm, lúc nào, trường nào đổi từ giá trị cũ sang giá trị mới.',
    tacnhan='Người quản lý / người xem danh mục loại meeting',
    dieukien='Người dùng vào được màn danh sách (Q1 hoặc Q2). Lịch sử không gắn quyền riêng.',
    chinh='1. Người dùng bấm nút Lịch sử trên dòng (hoặc bấm “…” rồi chọn Lịch sử).\n'
          '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <tên loại meeting>” và nạp danh sách thay đổi.\n'
          '3. Người dùng bấm Đóng.',
    phu='• Chưa có thay đổi nào → hiển thị “Chưa có lịch sử thay đổi”.\n'
        '• Bấm “Bộ lọc” trong cửa sổ để lọc theo nhóm hành động.',
    dacbiet=None)
d.p('2.10.2 Layout màn hình')
d.layout(menu=MENU + ' => Hành động khác => Lịch sử', modal='Lịch sử thay đổi',
         shot=shot('08-lich-su.png'), shot_caption='Cửa sổ Lịch sử thay đổi của loại meeting')
d.p('2.10.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Lịch sử thay đổi: <tên loại meeting>”.'),
    ('Danh sách thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi lần thay đổi: nhóm hành động, người thực hiện kèm phòng ban, thời điểm, các trường đổi '
     '(Tên, Có khách hàng, Mô tả, Trạng thái) với giá trị cũ → giá trị mới.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Lọc theo nhóm hành động.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thay đổi”.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)
d.p('2.10.4 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Lịch sử', 'Click', 'After:\n– Mở cửa sổ và nạp danh sách thay đổi của bản ghi.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.11
d.h3('2.11 Import Excel')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Import Excel loại meeting', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-11 Import Excel loại meeting')
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc Import file, Validate dữ liệu và Thông báo.', anchor='excel')
d.intro_table(
    ten='Import Excel loại meeting',
    mota='Thêm mới hàng loạt loại meeting từ tệp Excel theo file mẫu. Chỉ thêm mới, không cập nhật '
         'loại meeting đã có.',
    tacnhan='Người quản lý danh mục loại meeting',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm Import Excel.\n'
          '2. (Tuỳ chọn) Bấm “Tải file mẫu” để lấy tệp Mau_import_loaimeeting.xlsx.\n'
          '3. Bấm “Chọn file Excel”, chọn tệp đã điền dữ liệu.\n'
          '4. Bấm “Load lên bảng” để đọc tệp ra bảng xem trước.\n'
          '5. Bấm “Validate” → hệ thống kiểm tra từng dòng, đánh dấu dòng hợp lệ / lỗi kèm lý do; '
          'dòng hợp lệ bị khóa không sửa được.\n'
          '6. Nếu còn dòng lỗi: sửa trực tiếp các dòng lỗi rồi Validate lại, hoặc bấm “Bỏ dòng lỗi” '
          'để loại các dòng lỗi khỏi bảng.\n'
          '7. Khi đã Validate và không còn dòng lỗi, nút Import mới bấm được. Bấm “Import” → hệ thống '
          'thêm các dòng, thông báo “Import thành công <n> loại meeting”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Chưa Validate, hoặc còn dòng lỗi → nút Import bị khóa, không bấm được.\n'
        '• Mọi dòng đều lỗi → sau khi bỏ dòng lỗi bảng không còn dòng nào, nút Import vẫn khóa; '
        'không import được.\n'
        '• Bấm “Bỏ dòng lỗi” → “Đã bỏ x dòng lỗi. Còn lại y dòng hợp lệ.”\n'
        '• Bấm “Xoá trạng thái validate” → bỏ đánh dấu, mở khóa các dòng để sửa; phải Validate lại.\n'
        '• Dữ liệu thay đổi giữa lúc Validate và Import (vd người khác vừa tạo bản ghi trùng tên): '
        'còn ghi được một phần → “Import thành công x/y loại meeting. z loại meeting thất bại.”, đóng cửa sổ và nạp lại '
        'danh sách; không ghi được dòng nào → báo lỗi “Không có dữ liệu hợp lệ để import”, cửa sổ '
        'giữ nguyên.\n'
        '• Tệp quá 500 dòng → “Mỗi lần import tối đa 500 dòng (file đang có N dòng), vui lòng tách '
        'file và import nhiều lần.”\n'
        '• Bật “Chỉ dòng lỗi” để lọc bảng xem trước chỉ còn dòng lỗi.\n'
        '• Bấm Làm mới → xóa dữ liệu đã nạp để chọn tệp khác.',
    dacbiet='Mỗi lần import tối đa 500 dòng. Mỗi dòng thêm thành công đều ghi 1 dòng lịch sử '
            '“Thêm mới”. So trùng tên không phân biệt hoa/thường và dấu tiếng Việt.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Import Excel', modal='Import Loại meeting', shot=shot('09-import.png'),
         shot_caption='Cửa sổ Import Loại meeting')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx / .xls', 'Có', 'Hiển thị', 'Chọn tệp cần import.'),
    ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải Mau_import_loaimeeting.xlsx.'),
    ('Nút Load lên bảng', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa chọn tệp',
     'Đọc tệp ra bảng xem trước.'),
    ('Nút Validate', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu',
     'Kiểm tra dữ liệu từng dòng.'),
    ('Nút Import', 'Button', 'Enable / Disable', '–', '–', 'Disable',
     'Chỉ bấm được khi đã Validate và không còn dòng lỗi.'),
    ('Công tắc Chỉ dòng lỗi', 'Button', 'Enable', '–', '–', 'Tắt', 'Lọc bảng chỉ còn dòng lỗi.'),
    ('Cột Loại meeting', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo tệp',
     'Không trùng trong tệp và hệ thống.'),
    ('Cột Loại khách hàng', 'Textbox', 'Enable', 'Có / Không', 'Không', 'Theo tệp',
     'Để trống = Không.'),
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
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Validate', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Tệp quá 500 dòng → báo “Mỗi lần import tối đa 500 dòng …” và dừng xử lý.\n'
     'During (từng dòng):\n'
     '– Tên trống → “Loại meeting không được để trống”; quá dài → “Loại meeting vượt quá độ dài '
     'cho phép (tối đa 255 ký tự)”.\n'
     '– Tên trùng trong tệp → “Loại meeting bị trùng lặp trong file import (dòng n)”; trùng hệ '
     'thống → “Loại meeting đã tồn tại trong hệ thống”.\n'
     '– Trạng thái trống hoặc sai → “Trạng thái không hợp lệ (chỉ nhận: Hoạt động hoặc Khóa)”.\n'
     '– Loại khách hàng sai → “Loại khách hàng không hợp lệ (chỉ nhận: Có hoặc Không)”.\n'
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
     '“Import thành công <n> loại meeting”, đóng cửa sổ, nạp lại danh sách.\n'
     '– Một phần (dữ liệu thay đổi giữa lúc Validate và Import) → chỉ thêm các dòng còn hợp lệ; '
     'thông báo “Import thành công x/y loại meeting. z loại meeting thất bại.”, đóng cửa sổ, nạp lại danh sách.\n'
     '– Không dòng nào ghi được → báo lỗi “Không có dữ liệu hợp lệ để import”; cửa sổ giữ nguyên, '
     'không thêm dữ liệu.'),
    ('Bấm Tải file mẫu', 'Click', 'After:\n– Tải tệp Mau_import_loaimeeting.xlsx.'),
])

# ---------------------------------------------------------------- 2.12
d.h3('2.12 Xuất Excel')
d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Xuất Excel danh sách loại meeting', 'io', actor=A_QL,
            caption='Biểu đồ Use Case — FR-12 Xuất Excel')
d.p('2.12.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của '
           'Danh mục loại meeting.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách loại meeting',
    mota='Người dùng chọn các trường cần xuất rồi tải về tệp danh_sach_loai_meeting.xlsx gồm TẤT CẢ '
         'loại meeting khớp bộ lọc đang áp dụng (không chỉ trang đang xem).',
    tacnhan='Người quản lý danh mục loại meeting',
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
    ('Danh sách trường xuất', 'Table/Grid', 'Enable', '7 trường', 'Có (≥ 1)',
     'Tích sẵn các cột đang hiện trên bảng',
     'Tên loại meeting, Mô tả, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật, Trạng thái. Kéo '
     '⠿ để đổi thứ tự.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn nhanh.'),
    ('Dòng “Đang chọn x/7 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Tải tệp danh_sach_loai_meeting.xlsx.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiện trên bảng.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Áp đúng bộ lọc đang dùng trên màn, lấy tất cả dòng khớp.\n'
     'After:\n– Tải tệp danh_sach_loai_meeting.xlsx với các trường đã chọn theo thứ tự đã sắp.\n'
     '– Thông báo “Xuất Excel thành công”.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Danh mục loại meeting; không lặp lại các quy '
           'tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Tên loại meeting', [
        '– Bắt buộc, tối đa 255 ký tự, không trùng với loại meeting khác.',
        '– Khi import: so trùng không phân biệt hoa/thường, dấu tiếng Việt và khoảng trắng thừa.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-02', 'Bản ghi hệ thống', [
        '– Loại meeting do hệ thống cài sẵn (VD “Họp tìm hiểu & Giới thiệu sản phẩm”) không được '
        'Sửa, Xóa, Xóa nhiều, Khóa / Mở khóa.',
        '– Các thao tác này bị ẩn trên dòng và bị chặn ở máy chủ.',
    ], ['Danh sách', 'Chỉnh sửa', 'Xóa', 'Xóa nhiều', 'Khóa / Mở khóa']),
    ('BR-03', 'Điều kiện Sửa', [
        '– Chỉ sửa được loại meeting đang Hoạt động và chưa được cuộc họp nào sử dụng.',
        '– Loại meeting đang Khóa phải Mở khóa trước khi sửa.',
    ], ['Chỉnh sửa', 'Danh sách']),
    ('BR-04', 'Điều kiện Xóa', [
        '– Chỉ xóa được loại meeting chưa được cuộc họp nào sử dụng.',
        '– Xóa là xóa hẳn; loại meeting đã được sử dụng thì dùng Khóa thay cho Xóa.',
    ], ['Xóa', 'Xóa nhiều']),
    ('BR-05', 'Điều kiện Khóa / Mở khóa', [
        '– Khóa được cả loại meeting đã được sử dụng; cuộc họp cũ vẫn giữ nguyên loại meeting.',
        '– Mở khóa luôn được phép (trừ bản ghi hệ thống).',
        '– Chọn Trạng thái = Khóa trong form Sửa tương đương thao tác Khóa.',
    ], ['Khóa / Mở khóa', 'Chỉnh sửa']),
    ('BR-06', 'Loại meeting đã khóa ở màn nghiệp vụ', [
        '– Danh sách chọn loại meeting khi tạo cuộc họp chỉ gồm loại đang Hoạt động.',
        '– Cuộc họp đang dùng loại meeting nay đã khóa vẫn hiển thị đúng tên loại meeting đó.',
    ], 'Màn cuộc họp (Meeting)'),
    ('BR-07', 'Thao tác không dùng được thì ẩn', [
        '– Sửa, Xóa, Khóa / Mở khóa chỉ hiện với người có Q1 VÀ đủ điều kiện nghiệp vụ.',
        '– Không hiển thị nút xám.',
    ], 'Danh sách'),
    ('BR-08', 'Ghi lịch sử thay đổi', [
        '– Ghi lại mọi lần Tạo mới (kể cả qua Import), Thay đổi thông tin, Thay đổi trạng thái, Xóa '
        '(kể cả Xóa nhiều).',
        '– Cập nhật chỉ ghi các trường thực sự đổi: Tên, Có khách hàng, Mô tả, Trạng thái.',
        '– Ai vào được màn đều xem được lịch sử.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xóa', 'Xóa nhiều', 'Khóa / Mở khóa', 'Import Excel', 'Xem lịch sử']),
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

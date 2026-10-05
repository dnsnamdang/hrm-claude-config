# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo phát triển khách hàng theo NVKD.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/report/customer-development/{index,print}.vue, constants.js,
      components/{CustomerDevelopmentTable,CustomerDevelopmentDetailModal}.vue ·
      components/V2BaseSmartFilterPanel.vue · components/modal/filter-customization-modal.vue ·
      components/subsystem-menu/presale.js
  BE  Modules/Assign/Routes/api.php (assign/report/customer-development)
      CustomerDevelopmentReportController · Services/Report/CustomerDevelopmentReportService
      app/ExcelExport/CustomerDevelopmentReportExport + exports/customer_development_report.blade.php
  Quyền: PermissionsTableSeeder id 1087 / 1088 / 1089 (nhóm "Báo cáo phát triển khách hàng")
Ảnh chụp thật (headless, 1440x900, client :3002): shots/ — chỉ để local.
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

SHOTS = os.path.join(HERE, 'shots')


def shot(name):
    return os.path.join(SHOTS, name)


TEN_MAN = 'Báo cáo phát triển khách hàng theo NVKD'
MENU = 'Phân hệ CSKH trước bán => Báo cáo => Báo cáo thị trường => Báo cáo phát triển khách hàng theo NVKD'
ACTOR = 'Người xem báo cáo'
TACNHAN = 'Lãnh đạo, trưởng phòng, nhân viên kinh doanh; Người dùng đã đăng nhập'
DK = 'Người dùng đã đăng nhập (màn không yêu cầu quyền thao tác riêng; dữ liệu theo phạm vi quyền V1/V2/V3).'
ICONS = {
    'Phân hệ CSKH trước bán': 'icon_phanhe.png',
    'Báo cáo': 'icon_baocao.png',
    'Báo cáo thị trường': 'icon_nhom.png',
    'Báo cáo phát triển khách hàng theo NVKD': 'icon_man.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Xem chi tiết': 'icon_xemchitiet.png',
    'Chỉ xem cấp gốc': 'icon_capgoc.png',
    'Số lượng': 'icon_so.png',
    'Xuất Excel': 'icon_xuat.png',
    'In báo cáo': 'icon_in.png',
}

OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN)
d = SrsDoc(out=OUT, menu=MENU, route='', full_url='', img_prefix='bcptkh_')
d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})
d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Báo cáo phát triển khách hàng theo NVKD, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của báo cáo.',
    'Làm rõ cách đếm khách hàng của từng nhân viên kinh doanh ở 2 nhóm: Phát triển khách hàng mới và Kết quả '
    'chăm sóc trong kỳ, phân theo 5 nhóm trạng thái.',
    'Làm rõ cách quy đổi tiến trình dự án tiền khả thi sang nhóm trạng thái và phạm vi dữ liệu theo quyền.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('NVKD', 'Nhân viên kinh doanh — với khách hàng đã có dự án TKT là NVKD chính của dự án; khách hàng chưa có '
             'dự án là người tạo khách hàng.'),
    ('Dự án TKT', 'Dự án tiền khả thi gắn với khách hàng.'),
    ('KH tổ chức', 'Khách hàng loại doanh nghiệp / tổ chức (không tính khách hàng cá nhân).'),
    ('Phát triển khách hàng mới', 'Nhóm cột đếm khách hàng tổ chức được TẠO trong kỳ.'),
    ('Kết quả chăm sóc trong kỳ', 'Nhóm cột đếm khách hàng (cũ và mới) có dự án TKT được TẠO trong kỳ.'),
    ('Nhóm trạng thái', '5 nhóm: Chưa tiềm năng, Đang trao đổi, Đang làm GP, Đang thương thảo, Đang thực hiện HĐ — '
                        'quy đổi từ tiến trình dự án TKT tại ngày cuối kỳ (xem BR-03).'),
    ('Kỳ báo cáo', 'Khoảng ngày chọn ở bộ lọc thời gian (Tháng / Quý / Năm / Tuỳ chỉnh).'),
    ('GP / HĐ', 'Giải pháp / Hợp đồng.'),
], widths=[1.8, 4.2])

# ========================================================= PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('–', 'Không có quyền thao tác riêng',
     'Menu “Báo cáo phát triển khách hàng theo NVKD” hiển thị với mọi người dùng đã đăng nhập. Mọi chức năng '
     '(xem, lọc, cài đặt bộ lọc, xem danh sách khách hàng, xuất Excel, in) đều dùng được; số liệu do nhóm quyền '
     'phạm vi dữ liệu bên dưới quyết định.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem báo cáo phát triển khách hàng theo tổng công ty', 'Dự án TKT của mọi công ty.'),
    ('V2', 'Xem báo cáo phát triển khách hàng theo công ty',
     'Dự án TKT thuộc công ty đang làm việc + dự án do chính người dùng tạo.'),
    ('V3', 'Xem báo cáo phát triển khách hàng theo phòng ban',
     'Dự án TKT thuộc phòng ban / bộ phận người dùng quản lý + dự án do chính người dùng tạo.'),
    ('Không có quyền nào', '–', 'Chỉ dự án TKT do chính người dùng tạo hoặc người dùng là NVKD chính.'),
], widths=[0.8, 2.0, 3.2])
d.p('Phạm vi trên áp cho số liệu tính từ dự án TKT. Khách hàng chưa có dự án TKT (cột Chưa tiềm năng của nhóm '
    'Phát triển khách hàng mới) không bị giới hạn theo quyền — xem BR-02. Bộ lọc Công ty / Phòng ban / Bộ phận / '
    'Nhân viên luôn hiện đủ danh sách, không phụ thuộc quyền.')

d.h2('2 Ma trận phân quyền')
FR = [
    'FR-01 Xem báo cáo phát triển khách hàng theo NVKD',
    'FR-02 Tìm kiếm và lọc',
    'FR-03 Cài đặt bộ lọc',
    'FR-04 Chuyển chế độ xem cấp gốc / chi tiết',
    'FR-05 Xem danh sách khách hàng chi tiết',
    'FR-06 Xuất Excel',
    'FR-07 In báo cáo',
]
d.table(['Chức năng', 'V1', 'V2', 'V3', 'Không có quyền nào'],
        [(f, '✅', '✅', '✅', '✅ (chỉ dự án của mình)') for f in FR],
        widths=[2.6, 0.6, 0.6, 0.6, 1.6])

# ========================================================= PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR, [0, 1, 2])],
    [('FR-01', 'Xem báo cáo phát triển KH theo NVKD', 'view'),
     ('FR-06', 'Xuất Excel', 'io'),
     ('FR-07', 'In báo cáo', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Chế độ xem cấp gốc / chi tiết', 'view', 'extend', [0], None),
     ('FR-05', 'Xem danh sách khách hàng chi tiết', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

_no = [0]


def fn(ten, code=None, group='view', rule=None, intro=None, layouts=(), ui=None, ui_kw=None, ev=None):
    """Sinh 1 chức năng 2.x — có code => có Biểu đồ Usecase (5 mục con), không => 4 mục con."""
    if not ui or not ev:
        raise ValueError('Chức năng "%s" thiếu bảng giao diện / event' % ten)
    _no[0] += 1
    n = _no[0]
    d.h3('2.%d %s' % (n, ten))
    k = 0
    if code:
        k += 1
        d.p('2.%d.%d Biểu đồ Usecase' % (n, k))
        d.uc_figure(code, ten, group, actor=ACTOR)
    k += 1
    d.p('2.%d.%d Giới thiệu' % (n, k))
    d.rule_ref(rule[0], anchor=rule[1])
    d.intro_table(**intro)
    k += 1
    d.p('2.%d.%d Layout màn hình' % (n, k))
    for i, lay in enumerate(layouts):
        if i == 0:
            d.layout(**lay)
        else:
            d.p(lay['note'])
            d.figure(lay['shot'], lay['shot_caption'], width_in=6.2)
    k += 1
    d.p('2.%d.%d Mô tả chi tiết giao diện' % (n, k))
    d.ui_table(ui, **(ui_kw or {}))
    k += 1
    d.p('2.%d.%d Danh sách event và xử lý event' % (n, k))
    d.event_table(ev)


STAGE_COLS = ('Chưa tiềm năng · Đang trao đổi · Đang làm GP · Đang thương thảo · Đang thực hiện HĐ')

# ------------------------------------------------------------------ 2.1 Xem báo cáo
fn('Xem báo cáo phát triển khách hàng theo NVKD',
   rule=('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của Báo cáo phát triển khách hàng theo NVKD tại '
         'phần mô tả chi tiết.', 'list'),
   intro=dict(
       ten='Xem báo cáo phát triển khách hàng theo NVKD',
       mota='Hiển thị bảng số khách hàng theo cây Công ty → Phòng ban → NVKD, 2 nhóm cột: Phát triển khách hàng '
            'mới và Kết quả chăm sóc trong kỳ (gồm KH cũ & mới); mỗi nhóm gồm Số lượng + 5 nhóm trạng thái.',
       tacnhan=TACNHAN,
       dieukien=DK,
       chinh='1. Người dùng vào menu Báo cáo phát triển khách hàng theo NVKD.\n'
             '2. Hệ thống mở sẵn khối lọc, kỳ mặc định là tháng hiện tại của năm hiện tại.\n'
             '3. Hệ thống tổng hợp và hiển thị bảng ở chế độ Chỉ xem cấp gốc (chỉ dòng Công ty).\n'
             '4. Người dùng bấm mũi tên hoặc tên Công ty / Phòng ban để mở cấp con, hoặc bấm “Xem chi tiết” để mở hết.\n'
             '5. Người dùng bấm 1 số lớn hơn 0 để xem danh sách khách hàng (FR-05).',
       phu='• Đang tải → dòng “Đang tải dữ liệu...”.\n'
           '• Không có dữ liệu → “Không có dữ liệu phù hợp bộ lọc.”\n'
           '• Lỗi khi tải → bảng trống, hiện như không có dữ liệu.\n'
           '• Số bằng 0 không bấm được.'),
   layouts=[dict(menu=MENU, shot=shot('01-xem.png'),
                 shot_caption='Màn Báo cáo phát triển khách hàng theo NVKD — kỳ Tháng 7/2026, chế độ cấp gốc'),
            dict(note='Cuộn ngang bảng để xem nhóm cột Kết quả chăm sóc trong kỳ:',
                 shot=shot('04b-chi-tiet-cuon.png'),
                 shot_caption='Nhóm cột Kết quả chăm sóc trong kỳ sau khi cuộn ngang')],
   ui=[
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Báo cáo kết quả phát triển khách hàng theo nhân viên', '–'),
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–',
        'Danh sách kết quả phát triển khách hàng theo Công ty – Phòng ban – Nhân viên KD', '–'),
       ('Nút Xem chi tiết / Chỉ xem cấp gốc', 'Button', 'Enable', '–', 'Xem chi tiết', 'Xem FR-04.'),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-06.'),
       ('Nút In báo cáo', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-07.'),
       ('Bảng tổng hợp', 'Table/Grid', 'Read-only', '14 cột', 'Theo dữ liệu', 'Có thanh cuộn ngang.'),
       ('STT', 'Icon Button', 'Enable', '–', 'Theo cấp',
        'Dòng Công ty / Phòng ban: nút mũi tên thu gọn – mở rộng; dòng NVKD: trống.'),
       ('Công ty / Phòng ban / Nhân viên KD', 'Text', 'Read-only', '–', 'Theo dữ liệu',
        'Dòng Công ty “Công ty: <tên>” + “<n> KH mới · <m> KH chăm sóc”; dòng Phòng ban “Phòng ban: <tên>” + '
        '“<n> nhân viên”; dòng NVKD: tên + “<mã NV> · <bộ phận>”. Thiếu tên ghi “Không xác định”.'),
       ('Nhóm Phát triển khách hàng mới', 'Number (link)', 'Enable', '≥ 0', 'Theo dữ liệu',
        'Số lượng · ' + STAGE_COLS + '. Số lượng = tổng 5 cột trạng thái. Số > 0 gạch chân, bấm mở FR-05.'),
       ('Nhóm Kết quả chăm sóc trong kỳ (gồm KH cũ & mới)', 'Number (link)', 'Enable', '≥ 0', 'Theo dữ liệu',
        'Số lượng · ' + STAGE_COLS + '. Cột Chưa tiềm năng luôn 0 và không bấm được.'),
       ('Số liệu dòng Công ty / Phòng ban', 'Number (link)', 'Enable', '≥ 0', 'Theo dữ liệu',
        'Cộng từ các NVKD bên dưới.'),
       ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu...”.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
   ], ui_kw=dict(required=False),
   ev=[
       ('Mở màn hình', 'System',
        'After:\n– Nạp danh mục Lĩnh vực / Ngành hàng / Ứng dụng cho bộ lọc, rồi tải báo cáo kỳ Tháng hiện tại.\n'
        '– Hiển thị ở chế độ Chỉ xem cấp gốc.'),
       ('Bấm mũi tên / tên dòng Công ty', 'Click', 'After:\n– Thu gọn / mở rộng các phòng ban của công ty.'),
       ('Bấm mũi tên / tên dòng Phòng ban', 'Click', 'After:\n– Thu gọn / mở rộng danh sách NVKD của phòng.'),
       ('Bấm 1 số lớn hơn 0', 'Click', 'After:\n– Mở popup danh sách khách hàng (FR-05). Số 0 không phản hồi.'),
   ])

# ------------------------------------------------------------------ 2.2 Tìm kiếm và lọc
fn('Tìm kiếm và lọc',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả '
         'chi tiết.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc',
       mota='Lọc báo cáo theo kỳ, đơn vị và nhân viên của NVKD, nhóm khách hàng, lĩnh vực, ngành hàng, ứng dụng của '
            'dự án TKT. Báo cáo tự tải lại ngay khi đổi bất kỳ điều kiện nào.',
       tacnhan=TACNHAN,
       dieukien=DK,
       chinh='1. Khối lọc mở sẵn khi vào màn (bấm “Ẩn tìm kiếm nâng cao” / “Tìm kiếm nâng cao” để đóng / mở).\n'
             '2. Người dùng chọn Xem theo thời gian và các điều kiện lọc.\n'
             '3. Mỗi lần đổi điều kiện, hệ thống tự tải lại báo cáo (không cần bấm Tìm kiếm).',
       phu='• Bấm “Tìm kiếm” → tải lại với điều kiện hiện tại.\n'
           '• Bấm “Làm mới” → về kỳ Tháng hiện tại, xoá các điều kiện khác và tải lại.\n'
           '• Đổi Xem theo thời gian → xoá giá trị Tháng / Quý / Thời gian không còn dùng.\n'
           '• Kiểu Tuỳ chỉnh mà chưa đủ Từ ngày – Đến ngày → hệ thống lấy cả năm hiện tại.\n'
           '• Có chọn Lĩnh vực / Ngành hàng / Ứng dụng → không đếm khách hàng chưa có dự án TKT.'),
   layouts=[dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-loc.png'),
                 shot_caption='Khối lọc báo cáo phát triển khách hàng theo NVKD')],
   ui=[
       ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Ẩn tìm kiếm nâng cao',
        'Mặc định khối lọc đang mở.'),
       ('Xem theo thời gian', 'Dropdown', 'Enable', 'Tuỳ chỉnh / Tháng / Quý / Năm', 'Có', 'Tháng',
        'Không có nút xoá giá trị.'),
       ('Năm', 'Dropdown', 'Enable / Ẩn', '5 năm trước → năm sau', 'Có khi Tháng / Quý / Năm', 'Năm hiện tại',
        'Ẩn khi Tuỳ chỉnh.'),
       ('Quý', 'Dropdown', 'Enable / Ẩn', 'Quý I – Quý IV', 'Có khi Quý', 'Trống', 'Chỉ hiện khi Quý.'),
       ('Tháng', 'Dropdown', 'Enable / Ẩn', 'Tháng 1 – Tháng 12', 'Có khi Tháng', 'Tháng hiện tại', 'Chỉ hiện khi Tháng.'),
       ('Thời gian', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy – dd/mm/yyyy', 'Không', 'Trống',
        'Khoảng ngày trong 1 ô; chỉ hiện khi Tuỳ chỉnh.'),
       ('Công ty', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
        'Công ty của NVKD. Ổ khoá cạnh nhãn: hiện cả công ty đã khoá.'),
       ('Phòng ban', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Lọc theo Công ty đã chọn; có ổ khoá.'),
       ('Bộ phận', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Lọc theo Phòng ban đã chọn; có ổ khoá.'),
       ('Nhân viên', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
        'Hiển thị “Tên - Mã phòng - Mã nhân viên”; lọc theo đơn vị đã chọn.'),
       ('Nhóm khách hàng', 'Dropdown', 'Enable', 'Danh sách 6 giá trị', 'Không', 'Trống',
        'KH mới nhập ERP (chưa có hoạt động) · KH chưa tiềm năng · KH đang trao đổi thông tin · KH đang xây dựng '
        'giải pháp · KH đang thương thảo HĐ · KH đang triển khai HĐ.'),
       ('Lĩnh vực', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
        'Chỉ liệt kê giá trị đang có ở dự án TKT trong phạm vi quyền.'),
       ('Ngành hàng', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Như trên; không phụ thuộc Lĩnh vực.'),
       ('Ứng dụng', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Như trên; có ⓘ mô tả.'),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
   ],
   ev=[
       ('Đổi bất kỳ điều kiện lọc', 'Change',
        'After:\n– Tự tải lại báo cáo với điều kiện mới (giữ nguyên chế độ xem).'),
       ('Đổi Xem theo thời gian', 'Change',
        'After:\n– Hiện / ẩn ô Năm, Quý, Tháng, Thời gian; xoá giá trị ô không còn dùng rồi tải lại.'),
       ('Bấm Tìm kiếm', 'Click', 'After:\n– Tải lại báo cáo với điều kiện hiện tại.'),
       ('Bấm Làm mới', 'Click',
        'After:\n– Đặt lại Xem theo thời gian = Tháng, tháng và năm hiện tại; xoá các điều kiện khác; tải lại.'),
       ('Bấm Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khối lọc.'),
   ])

# ------------------------------------------------------------------ 2.3 Cài đặt bộ lọc
fn('Cài đặt bộ lọc', code='FR-03', group='crud',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.',
         'search'),
   intro=dict(
       ten='Cài đặt bộ lọc',
       mota='Cho từng người dùng chọn trường lọc nào được hiển thị và thứ tự các trường trong khối lọc của báo cáo.',
       tacnhan=TACNHAN,
       dieukien=DK,
       chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
             '2. Hệ thống mở popup liệt kê các trường lọc đang khai báo, đánh số thứ tự.\n'
             '3. Người dùng tích / bỏ tích trường muốn hiển thị, kéo biểu tượng ⋮⋮ để đổi thứ tự.\n'
             '4. Người dùng bấm “Lưu”.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại khối lọc.',
       phu='• Bấm “Khôi phục mặc định” → về thứ tự gốc, hiện đủ trường (chỉ ghi nhận khi bấm Lưu).\n'
           '• Bấm “Đóng” / dấu × → đóng popup, không lưu.\n'
           '• Lưu lỗi → “Thao tác thất bại”.\n'
           '• Trường bị ẩn đang có giá trị lọc → giá trị đó bị xoá (báo cáo tự tải lại).',
       dacbiet='Cấu hình lưu theo tài khoản người dùng và theo màn; người khác không bị ảnh hưởng.'),
   layouts=[dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('03-cai-dat.png'),
                 shot_caption='Popup Cài đặt bộ lọc')],
   ui=[
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', 'Kèm biểu tượng bánh răng.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường lọc muốn hiển thị; kéo ⋮⋮ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách trường lọc', 'Checkbox', 'Enable', 'Các trường đang có trên khối lọc', 'Không',
        'Theo cấu hình đã lưu',
        'Gồm Xem theo thời gian, Năm, Tháng (hoặc Quý / Thời gian tuỳ kiểu thời gian đang chọn), Công ty – '
        'Phòng ban – Bộ phận, Nhóm khách hàng, Lĩnh vực, Ngành hàng, Ứng dụng.'),
       ('Biểu tượng kéo ⋮⋮', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo thả để đổi thứ tự.'),
       ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khoá trong lúc đang lưu.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở popup với cấu hình đã lưu của người dùng (chưa có thì hiện đủ trường).'),
       ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Đưa danh sách về thứ tự khai báo gốc, tích đủ mọi trường.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Người dùng đã đăng nhập.\n'
        'After:\n– Lưu cấu hình theo người dùng + màn; xoá giá trị lọc của trường vừa bị ẩn.\n'
        '– Hiển thị “Cập nhật thành công”, đóng popup, vẽ lại khối lọc.\n'
        '– Lỗi → “Thao tác thất bại”.'),
       ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------------ 2.4 Chế độ xem
fn('Chuyển chế độ xem cấp gốc / chi tiết',
   rule=('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'list'),
   intro=dict(
       ten='Chuyển chế độ xem cấp gốc / chi tiết',
       mota='Mở nhanh toàn bộ cây Công ty → Phòng ban → NVKD hoặc thu gọn về cấp Công ty.',
       tacnhan=TACNHAN,
       dieukien=DK,
       chinh='1. Mặc định bảng ở chế độ cấp gốc (chỉ dòng Công ty), nút ghi “Xem chi tiết”.\n'
             '2. Người dùng bấm “Xem chi tiết” → mở hết Phòng ban và NVKD, nút đổi thành “Chỉ xem cấp gốc”.\n'
             '3. Người dùng bấm “Chỉ xem cấp gốc” → thu gọn về dòng Công ty.',
       phu='• Ở chế độ chi tiết, mọi cấp luôn mở, không thu gọn riêng từng dòng được.\n'
           '• Ở chế độ cấp gốc, người dùng mở từng công ty / phòng ban bằng mũi tên.'),
   layouts=[dict(menu=MENU + ' => Xem chi tiết', shot=shot('04-chi-tiet.png'),
                 shot_caption='Bảng ở chế độ xem chi tiết (mở hết các cấp)')],
   ui=[
       ('Nút Xem chi tiết', 'Button', 'Enable', '–', 'Hiển thị (chế độ cấp gốc)', 'Nền xanh, biểu tượng con mắt.'),
       ('Nút Chỉ xem cấp gốc', 'Button', 'Enable', '–', 'Ẩn', 'Hiện thay nút trên khi đang ở chế độ chi tiết.'),
       ('Dòng Phòng ban / NVKD', 'Table/Grid', 'Read-only', '–', 'Ẩn', 'Hiện đủ khi ở chế độ chi tiết.'),
   ], ui_kw=dict(required=False),
   ev=[
       ('Bấm Xem chi tiết', 'Click', 'After:\n– Mở mọi Công ty và Phòng ban, đổi nút thành “Chỉ xem cấp gốc”.'),
       ('Bấm Chỉ xem cấp gốc', 'Click', 'After:\n– Thu gọn mọi Công ty và Phòng ban, đổi nút thành “Xem chi tiết”.'),
   ])

# ------------------------------------------------------------------ 2.5 Danh sách KH
fn('Xem danh sách khách hàng chi tiết',
   rule=('- Màn Xem chi tiết, Kịch bản tìm kiếm và UI/UX. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.',
         'detail'),
   intro=dict(
       ten='Xem danh sách khách hàng chi tiết',
       mota='Popup liệt kê các khách hàng đứng sau 1 ô số liệu (của 1 NVKD, 1 phòng ban hoặc 1 công ty) theo nhóm '
            'cột và nhóm trạng thái đã bấm.',
       tacnhan=TACNHAN,
       dieukien=DK + ' Ô được bấm có số lớn hơn 0.',
       chinh='1. Người dùng bấm 1 số lớn hơn 0 trong bảng.\n'
             '2. Hệ thống lấy điều kiện lọc đang dùng, thay đơn vị / nhân viên bằng đúng dòng được bấm.\n'
             '3. Hệ thống mở popup: dòng phụ đề “<nhóm cột> · <nhóm trạng thái>”, tiêu đề là tên NVKD / '
             '“<Công ty> — <Phòng ban>” / tên công ty.\n'
             '4. Người dùng gõ từ khoá, bấm “Tìm kiếm” (hoặc Enter) để lọc theo tên / mã khách hàng / tên NVKD.\n'
             '5. Người dùng đóng popup bằng dấu ×.',
       phu='• Bấm “Làm mới” → xoá từ khoá, tải lại danh sách.\n'
           '• Không có khách hàng phù hợp → “Không có dữ liệu phù hợp.”\n'
           '• Bấm ô Số lượng → phụ đề ghi “Tất cả trạng thái”.\n'
           '• Lỗi khi tải → danh sách rỗng.'),
   layouts=[dict(menu=MENU + ' => Xem chi tiết => Số lượng', modal='Danh sách khách hàng',
                 shot=shot('05-ds-kh.png'),
                 shot_caption='Popup danh sách khách hàng — Kết quả chăm sóc trong kỳ của 1 NVKD')],
   ui=[
       ('Phụ đề popup', 'Label', 'Hiển thị', '–', '–', 'Theo ô bấm',
        '“Phát triển KH mới” hoặc “Kết quả chăm sóc trong kỳ” · tên nhóm trạng thái / “Tất cả trạng thái”.'),
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Theo dòng bấm',
        'Tên NVKD / “<Công ty> — <Phòng ban>” / tên công ty; thiếu thì “Chi tiết khách hàng”.'),
       ('Tìm kiếm', 'Textbox', 'Enable', 'Không giới hạn', 'Không', 'Trống', 'Gợi ý “Tên / mã KH / NVKD”; Enter = Tìm kiếm.'),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('STT', 'Text', 'Read-only', '–', '–', 'Tự đánh', '–'),
       ('Khách hàng', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', 'Mã khách hàng (chữ nhỏ) + tên khách hàng.'),
       ('NVKD phụ trách', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', 'Thiếu ghi “—”.'),
       ('Công ty / PB / BP', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', 'Công ty; dòng dưới “Phòng ban · Bộ phận” của NVKD.'),
       ('Nhóm trạng thái', 'Badge', 'Read-only', '5 giá trị', '–', 'Theo dữ liệu',
        'Chưa tiềm năng (xám) · Đang trao đổi thông tin (cam) · Đang làm GP (đỏ) · Đang thương thảo (xanh dương) · '
        'Đang thực hiện HĐ (xanh lá).'),
       ('Dự án TKT gần nhất', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
        'Mã + tên dự án TKT tạo gần nhất của khách hàng với NVKD đó; chưa có ghi “—”.'),
       ('#Meeting', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', 'Số meeting của dự án TKT gần nhất.'),
       ('#Dự án TKT', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', 'Tổng số dự án TKT của khách hàng với NVKD đó.'),
       ('Dòng tổng kết', 'Pagination', 'Hiển thị', '–', '–', 'Theo dữ liệu', '“Hiển thị 1–n / n” — hiện tất cả trên 1 trang.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '“Không có dữ liệu phù hợp.”'),
       ('Nút đóng ×', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '–'),
   ],
   ev=[
       ('Bấm 1 số lớn hơn 0', 'Click',
        'Before:\n– Lấy điều kiện lọc hiện tại; dòng NVKD → chỉ khách hàng của NVKD đó (NVKD ngoài phạm vi lọc trả '
        'rỗng); dòng Phòng ban / Công ty → các NVKD thuộc đơn vị đó.\n'
        'During:\n– Lấy khách hàng theo nhóm cột (Phát triển KH mới / Kết quả chăm sóc) và nhóm trạng thái đã bấm.\n'
        'After:\n– Mở popup và hiển thị danh sách; lỗi → danh sách rỗng.'),
       ('Bấm Tìm kiếm / Enter', 'Click / Keypress',
        'After:\n– Tải lại danh sách, chỉ giữ khách hàng có tên, mã khách hàng hoặc tên NVKD chứa từ khoá (không phân biệt hoa thường).'),
       ('Bấm Làm mới', 'Click', 'After:\n– Xoá từ khoá, tải lại đủ danh sách.'),
       ('Bấm × / Esc', 'Click / Keypress', 'After:\n– Đóng popup; mở lại popup thì ô tìm kiếm trống.'),
   ])

# ------------------------------------------------------------------ 2.6 Xuất Excel
fn('Xuất Excel', code='FR-06', group='io',
   rule=('- Quy tắc Excel và Thông báo. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'excel'),
   intro=dict(
       ten='Xuất Excel',
       mota='Tải về file Excel toàn bộ báo cáo theo điều kiện lọc hiện tại.',
       tacnhan=TACNHAN,
       dieukien=DK,
       chinh='1. Người dùng bấm “Xuất Excel”.\n'
             '2. Hệ thống dựng file theo điều kiện lọc hiện tại, gồm mọi công ty, phòng ban, NVKD (không phụ thuộc '
             'chế độ xem đang thu gọn hay mở).\n'
             '3. Trình duyệt tải file “bao_cao_phat_trien_khach_hang.xls”; hệ thống báo “Xuất Excel thành công”.',
       phu='• Lỗi khi dựng / tải file → “Lỗi khi xuất Excel”.',
       dacbiet='File gồm ảnh tiêu đề (letterhead) công ty đang làm việc; tiêu đề “BÁO CÁO KẾT QUẢ PHÁT TRIỂN KHÁCH '
               'HÀNG THEO NHÂN VIÊN”; 14 cột: STT, Công ty / Phòng ban / Nhân viên KD, 2 nhóm “PHÁT TRIỂN KHÁCH HÀNG '
               'MỚI” và “KẾT QUẢ CHĂM SÓC TRONG KỲ” mỗi nhóm 6 cột; dòng Công ty (STT 1, 2…), Phòng ban (1.1), NVKD; '
               'không có dòng tổng toàn bộ.'),
   layouts=[dict(menu=MENU + ' => Xuất Excel', shot=shot('06-xuat.png'),
                 shot_caption='Bấm Xuất Excel — file được tải về và hiện thông báo thành công')],
   ui=[
       ('Nút Xuất Excel', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Biểu tượng file Excel.'),
       ('Thanh tiến trình đầu trang', 'Loading', 'Hiển thị', '–', '–', 'Ẩn', 'Chạy trong lúc dựng file.'),
       ('Tên file', 'Text', 'Read-only', '–', '–', 'bao_cao_phat_trien_khach_hang.xls', '–'),
       ('Cột trong file', 'Table/Grid', 'Read-only', '14 cột', '–', 'Theo dữ liệu',
        'Mỗi nhóm: Số lượng · Chưa tiềm năng · Đang trao đổi · Đang làm GP · Đang thương thảo · Đang thực hiện HĐ.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '“Xuất Excel thành công” / “Lỗi khi xuất Excel”.'),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Người dùng đã đăng nhập; lấy điều kiện lọc hiện tại.\n'
        'During:\n– Tổng hợp dữ liệu theo phạm vi quyền (BR-02) và điều kiện lọc.\n'
        'After:\n– Tải file bao_cao_phat_trien_khach_hang.xls, hiển thị “Xuất Excel thành công”.\n'
        '– Lỗi → “Lỗi khi xuất Excel”.'),
   ])

# ------------------------------------------------------------------ 2.7 In
fn('In báo cáo', code='FR-07', group='io',
   rule=('- Màn Xem chi tiết và Thông báo. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'detail'),
   intro=dict(
       ten='In báo cáo',
       mota='Mở bản xem trước để in toàn bộ báo cáo theo điều kiện lọc hiện tại, khổ A4 ngang.',
       tacnhan=TACNHAN,
       dieukien=DK,
       chinh='1. Người dùng bấm “In báo cáo”.\n'
             '2. Hệ thống mở tab mới, tải báo cáo theo điều kiện lọc hiện tại.\n'
             '3. Bản xem trước gồm letterhead, tiêu đề “BÁO CÁO KẾT QUẢ PHÁT TRIỂN KHÁCH HÀNG THEO NHÂN VIÊN”, bảng '
             'số liệu và ô ký “Ngày ...., tháng ...., năm .... / Người lập / (Ký, họ tên)”.\n'
             '4. Người dùng bấm “In” → mở hộp thoại in của trình duyệt (A4 ngang, lề 8mm × 6mm).',
       phu='• Lỗi khi tải dữ liệu → khung đỏ hiển thị nội dung lỗi hoặc “Lỗi tải dữ liệu báo cáo”.\n'
           '• Không có dữ liệu → bảng ghi “Không có dữ liệu”.'),
   layouts=[dict(menu=MENU + ' => In báo cáo', shot=shot('07-in.png'),
                 shot_caption='Bản xem trước In báo cáo phát triển khách hàng theo NVKD')],
   ui=[
       ('Nút In', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Không xuất hiện trên bản in.'),
       ('Letterhead', 'Image', 'Hiển thị', '–', '–', 'Ảnh mặc định', 'Ảnh tiêu đề mặc định của hệ thống.'),
       ('Tiêu đề', 'Label', 'Hiển thị', '–', '–', 'BÁO CÁO KẾT QUẢ PHÁT TRIỂN KHÁCH HÀNG THEO NHÂN VIÊN', '–'),
       ('Bảng số liệu', 'Table/Grid', 'Read-only', '14 cột', '–', 'Theo dữ liệu',
        'Cột rút gọn: SL · Chưa · Trao đổi · Làm GP · Thương thảo · Thực hiện HĐ cho mỗi nhóm; STT 1 / 1.1 / 1.1.1; '
        'NVKD ghi “Tên (mã NV)”; dòng Công ty nền xanh dương, Phòng ban nền xám; luôn in đủ mọi cấp.'),
       ('Ô ký', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Ngày ...., tháng ...., năm ....”, “Người lập”, “(Ký, họ tên)”.'),
       ('Khung báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Nền đỏ, không in ra.'),
   ],
   ev=[
       ('Bấm In báo cáo', 'Click',
        'Before:\n– Lấy điều kiện lọc hiện tại.\n'
        'After:\n– Mở tab bản xem trước, tải dữ liệu và dựng bảng.'),
       ('Bấm In', 'Click', 'After:\n– Mở hộp thoại in, khổ A4 ngang.'),
   ])

# ==================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Báo cáo phát triển khách hàng theo NVKD; không lặp lại các '
           'quy tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Hai nhóm đếm khách hàng', [
        '– Phát triển khách hàng mới: khách hàng TỔ CHỨC được tạo trong kỳ. Mỗi cặp (khách hàng, NVKD chính của dự '
        'án TKT tạo đến hết ngày cuối kỳ) đếm 1 lần. Khách hàng chưa có dự án TKT nào đến hết ngày cuối kỳ → đếm '
        'vào Chưa tiềm năng của người tạo khách hàng.',
        '– Kết quả chăm sóc trong kỳ: mỗi cặp (khách hàng, NVKD chính) có dự án TKT được TẠO trong kỳ đếm 1 lần, '
        'gồm cả khách hàng cũ; nhóm này không có Chưa tiềm năng.',
        '– Số lượng = tổng 5 cột trạng thái; số dòng Công ty / Phòng ban = cộng từ NVKD.',
    ], ['Xem báo cáo', 'Xem danh sách khách hàng chi tiết', 'Xuất Excel', 'In báo cáo']),
    ('BR-02', 'Phạm vi dữ liệu theo quyền', [
        '– V1: dự án TKT mọi công ty. V2: dự án thuộc công ty đang làm việc + dự án mình tạo. V3: dự án thuộc phòng '
        'ban / bộ phận mình quản lý + dự án mình tạo. Không có quyền nào: dự án mình tạo hoặc mình là NVKD chính.',
        '– Khách hàng chưa có dự án TKT (Chưa tiềm năng của nhóm Phát triển khách hàng mới) không giới hạn theo quyền.',
    ], 'Toàn màn hình'),
    ('BR-03', 'Quy đổi tiến trình dự án TKT sang nhóm trạng thái', [
        '– Lấy tiến trình của dự án tại hết ngày cuối kỳ (theo lịch sử đổi tiến trình; chưa có lịch sử thì lấy '
        'tiến trình hiện tại).',
        '– Thu thập thông tin dự án → Đang trao đổi; Chờ tiếp nhận làm giải pháp, Đang làm giải pháp, Trao đổi giải '
        'pháp với khách hàng, Lập dự toán → Đang làm GP; Thương thảo giá và giải pháp, Thương thảo hợp đồng → Đang '
        'thương thảo; Thực hiện hợp đồng, Nghiệm thu và thanh lý hợp đồng → Đang thực hiện HĐ.',
        '– Dự án ở Đang tạo, Đóng/Không thực hiện dự án, Kết thúc và lưu trữ không được tính.',
        '– 1 khách hàng có nhiều dự án với cùng NVKD → lấy dự án có tiến trình cao nhất.',
    ], ['Xem báo cáo', 'Xem danh sách khách hàng chi tiết']),
    ('BR-04', 'Lọc theo đơn vị, nhóm khách hàng, danh mục dự án', [
        '– Công ty / Phòng ban / Bộ phận / Nhân viên lọc theo đơn vị hiện tại của NVKD, không theo đơn vị ghi trên dự án.',
        '– Nhóm khách hàng: chỉ giữ NVKD có ít nhất 1 khách hàng ở nhóm trạng thái tương ứng (ở 1 trong 2 nhóm '
        'cột); “KH mới nhập ERP (chưa có hoạt động)” và “KH chưa tiềm năng” cùng ứng với Chưa tiềm năng. Các cột '
        'khác của NVKD vẫn hiển thị đủ.',
        '– Lĩnh vực / Ngành hàng / Ứng dụng lọc theo dự án TKT; khi có chọn thì bỏ khách hàng chưa có dự án.',
    ], 'Tìm kiếm và lọc'),
    ('BR-05', 'Kỳ báo cáo', [
        '– Tháng / Quý / Năm quy ra từ ngày đầu đến ngày cuối kỳ; Tuỳ chỉnh dùng khoảng ngày chọn.',
        '– Thiếu thông tin kỳ → mặc định cả năm hiện tại.',
    ], ['Tìm kiếm và lọc', 'Xuất Excel', 'In báo cáo']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

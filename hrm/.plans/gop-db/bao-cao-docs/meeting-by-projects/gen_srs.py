# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo Meeting theo dự án.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/report/meeting-by-projects/{index,print}.vue + components/*
      components/TopProjectsChart.vue · V2BaseSmartFilterPanel.vue · modal/filter-customization-modal.vue
      components/subsystem-menu/{meeting,presale}.js
  BE  Modules/Assign/Routes/api.php (prefix assign/report/meeting-by-projects)
      ReportController::meetingByProjects*, getChartData, getMeetingsBy*, getParticipantsByScope
      Services/Report/MeetingByProjectsService · app/ExcelExport/MeetingByProjectsExport
      resources/views/exports/meeting_by_projects_report.blade.php
  Quyền: PermissionsTableSeeder id 1060–1061 (nhóm "Báo cáo meeting theo dự án")
Ảnh chụp thật (headless 1440x900, client :3002 → API :8003): shots/ — chỉ để local.
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


TEN_MAN = 'Báo cáo Meeting theo dự án'
MENU_A = 'Phân hệ Meeting => Báo cáo => Meeting theo dự án'
MENU_B = 'Phân hệ CSKH trước bán => Báo cáo => Báo cáo dự án tiền khả thi => Báo cáo meeting theo Dự án TKT'
ACT = 'Người xem báo cáo meeting'

ICONS = {
    'Phân hệ Meeting': 'icon_phanhe_mt.png',
    'Phân hệ CSKH trước bán': 'icon_phanhe_ps.png',
    'Báo cáo': 'icon_mt_baocao.png',
    'Meeting theo dự án': 'icon_mt_da.png',
    'Báo cáo dự án tiền khả thi': 'icon_ps_nhom.png',
    'Báo cáo meeting theo Dự án TKT': 'icon_ps_da.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Xem chi tiết': 'icon_xemchitiet.png',
    'Chỉ xem cấp gốc': 'icon_capgoc.png',
    'Loại meeting': 'icon_chip_loai.png',
    'Hình thức': 'icon_chip_hinhthuc.png',
    'Số người tham gia': 'icon_chip_nguoi.png',
    'Xem': 'icon_xem_bienban.png',
    'Xuất Excel': 'icon_xuat.png',
    'In danh sách': 'icon_in.png',
}

d = SrsDoc(out=os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN), menu=MENU_A, route='', full_url='',
           img_dir=os.path.join(HERE, '.uml'), img_prefix='mtda_')
d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})


def menu_b(menu):
    """Dòng menu CSKH trước bán: mục "Báo cáo" ở phân hệ này có icon khác phân hệ Meeting."""
    d.menu_icons['Báo cáo'] = shot('icon_ps_baocao.png')
    d._menu_para(menu)
    d.menu_icons['Báo cáo'] = shot('icon_mt_baocao.png')


def layout(tail, png, caption, modal=None, extra=None):
    """Mục Layout: báo cáo có 2 lối vào menu (cùng 1 màn, cùng phạm vi dữ liệu)."""
    d.p('Đường dẫn màn hình:')
    d._menu_para(MENU_A + tail)
    menu_b(MENU_B + tail)
    d.p('Hai lối vào mở CÙNG một báo cáo, dữ liệu như nhau; chỉ khác thanh menu bên trái giữ theo '
        'phân hệ người dùng đang làm việc.')
    if modal:
        d.p('Cửa sổ %s được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.' % modal)
    if extra:
        d.p(extra)
    d.figure(shot(png), caption, width_in=6.2)


SCOPE = ('– Hệ thống chỉ lấy dự án trong phạm vi quyền (V1: mọi dự án; V2: dự án thuộc công ty đang làm việc '
         'hoặc do mình tạo; không có quyền: dự án mình tạo hoặc mình là nhân viên kinh doanh chính).')

d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho báo cáo Meeting theo dự án (tiêu đề trên màn hình: “Báo cáo thời '
    'gian meeting theo dự án”), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền dữ liệu của báo cáo.',
    'Làm rõ mỗi dự án tiền khả thi đã tổ chức bao nhiêu cuộc meeting, số liệu theo loại meeting, hình thức, '
    'tổng thời lượng, người tham gia và chi tiết từng cuộc meeting trong dự án.',
    'Làm rõ dự án nào được đưa vào báo cáo và cách tính số liệu tổng của dự án.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Dự án TKT', 'Dự án tiền khả thi (phân hệ CSKH trước bán).'),
    ('Meeting', 'Cuộc họp lập ở phân hệ Meeting, gắn với dự án TKT; mã dạng TPE.MET.KH.26.0060.'),
    ('Tiến trình', 'Trạng thái của dự án TKT (vd Thu thập thông tin dự án, Lập dự toán…).'),
    ('Giai đoạn', 'Giai đoạn dự án lấy từ danh mục Giai đoạn dự án.'),
    ('Thời lượng', 'Số phút từ giờ bắt đầu tới giờ kết thúc của cuộc họp.'),
    ('Hình thức', 'Trực tiếp hoặc Online.'),
    ('Cấp gốc', 'Dòng Dự án — cấp cao nhất của bảng Dự án → Meeting.'),
    ('Công ty đang làm việc', 'Công ty người dùng đang chọn ở góc trên bên phải màn hình.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('–', 'Không có quyền thao tác riêng',
     'Mọi người dùng đã đăng nhập đều thấy menu và mở được báo cáo; các nút Xuất Excel, In danh sách, '
     'các cửa sổ xem chi tiết không gắn quyền. Dữ liệu được thấy do nhóm quyền phạm vi bên dưới quyết định.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem báo cáo meeting theo dự án theo tổng công ty',
     'Mọi dự án của mọi công ty; ô lọc Công ty hiển thị.'),
    ('V2', 'Xem báo cáo meeting theo dự án theo công ty',
     'Dự án thuộc công ty đang làm việc và dự án do chính người dùng tạo.'),
    ('–', 'Không có quyền nào ở trên',
     'Dự án do chính người dùng tạo hoặc người dùng là nhân viên kinh doanh chính.'),
], widths=[0.8, 2.4, 2.8])
d.p('Có cả 2 quyền thì lấy phạm vi của V1.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'V1', 'V2', 'Không có quyền nào'], [
    ('FR-01 Xem báo cáo meeting theo dự án', '✅', '✅', '✅ (dự án của mình)'),
    ('FR-02 Tìm kiếm và lọc báo cáo', '✅ (có ô Công ty)', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅'),
    ('FR-04 Xem biểu đồ Top 5 dự án', '✅', '✅', '✅ (dự án của mình)'),
    ('FR-05 Xem chi tiết dự án', '✅', '✅', '✅'),
    ('FR-06 Xem danh sách meeting theo loại', '✅', '✅', '✅'),
    ('FR-07 Xem danh sách meeting theo hình thức', '✅', '✅', '✅'),
    ('FR-08 Xem danh sách người tham gia', '✅', '✅', '✅'),
    ('FR-09 Xem biên bản cuộc họp', '✅', '✅', '✅'),
    ('FR-10 Xuất Excel báo cáo', '✅', '✅', '✅ (dự án của mình)'),
    ('FR-11 In báo cáo', '✅', '✅', '✅ (dự án của mình)'),
], widths=[2.8, 1.1, 0.6, 1.5])

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACT, [0, 1, 2])],
    [('FR-01', 'Xem báo cáo meeting theo dự án', 'view'),
     ('FR-10', 'Xuất Excel báo cáo', 'io'),
     ('FR-11', 'In báo cáo', 'io')],
    [('FR-02', 'Tìm kiếm và lọc báo cáo', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Xem biểu đồ Top 5 dự án', 'view', 'extend', [0], None),
     ('FR-05', 'Xem chi tiết dự án', 'view', 'extend', [0], None),
     ('FR-06', 'Xem meeting theo loại', 'view', 'extend', [0], None),
     ('FR-07', 'Xem meeting theo hình thức', 'view', 'extend', [0], None),
     ('FR-08', 'Xem danh sách người tham gia', 'view', 'extend', [0], None),
     ('FR-09', 'Xem biên bản cuộc họp', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem báo cáo meeting theo dự án')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Phân trang và UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả '
           'chi tiết.', anchor='list')
d.intro_table(
    ten='Xem báo cáo meeting theo dự án',
    mota='Hiển thị trên 1 màn: bộ lọc (thu gọn), biểu đồ Top 5 dự án kèm bảng “Chi tiết theo biểu đồ”, và bảng '
         'chi tiết 2 cấp Dự án → Meeting. Lúc mở, bảng chỉ hiện cấp gốc (dòng Dự án).',
    tacnhan=ACT + '; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập.',
    chinh='1. Người dùng vào báo cáo theo một trong 2 đường dẫn menu.\n'
          '2. Hệ thống đặt sẵn bộ lọc: Xem theo thời gian = Tháng, Tháng = tháng hiện tại, Năm = năm hiện tại.\n'
          '3. Hệ thống tải bảng chi tiết (50 meeting/trang) và biểu đồ theo bộ lọc mặc định.\n'
          '4. Mỗi dòng Dự án hiển thị người tạo dự án, tiến trình, khách hàng, giai đoạn, tổng phút, chip đếm '
          'theo loại meeting, theo hình thức và tổng người tham gia.',
    phu='• Không có dự án nào khớp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.\n'
        '• Đổi số dòng/trang hoặc chuyển trang → tải lại bảng, giữ nguyên bộ lọc.')
d.p('2.1.2 Layout màn hình')
layout('', '01-xem-bao-cao.png', 'Báo cáo thời gian meeting theo dự án lúc mới mở (tháng 10/2026)')
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Báo cáo thời gian meeting theo dự án',
     'Kèm ⓘ: “Theo dõi mỗi dự án đã tổ chức bao nhiêu cuộc meeting, số liệu theo loại meeting, chi tiết các cuộc '
     'meeting trong dự án =>> Tông hợp số liệu”.'),
    ('Khối bộ lọc', 'Card', 'Hiển thị', '–', 'Thu gọn',
     'Tiêu đề “Bộ lọc báo cáo thời gian meeting theo dự án”; nút Cài đặt bộ lọc, Tìm kiếm nâng cao (FR-02, FR-03).'),
    ('Khối biểu đồ Top 5 dự án', 'Card', 'Hiển thị', '–', 'Theo bộ lọc', 'Xem FR-04.'),
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Bảng chi tiết meeting theo dự án',
     'Kèm ⓘ: “Click mũi tên để mở/đóng danh sách meeting của dự án. Click chip ở cột Loại/Hình thức để xem popup '
     'đúng danh sách meeting.”'),
    ('Nút Xem chi tiết', 'Button', 'Enable', '–', 'Hiển thị', 'Mở danh sách meeting của mọi dự án (FR-05).'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-10.'),
    ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-11.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Mũi tên mở/đóng',
     'Dòng Dự án là nút mũi tên; dòng Meeting là số thứ tự trong dự án.'),
    ('Cột Dự án / Meeting', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng Dự án: tên dự án + “Số meeting: n”; dòng Meeting: “Mã — Tên”.'),
    ('Nhóm THÔNG TIN DỰ ÁN: Người tạo dự án, Tiến trình, Khách hàng, Giai đoạn', 'Table/Grid', 'Read-only', '–',
     'Theo dữ liệu', 'Chỉ ở dòng Dự án; Tiến trình hiển thị dạng chip.'),
    ('Nhóm THỜI GIAN & THỜI LƯỢNG: Thời gian', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Chỉ ở dòng Meeting: ngày + “giờ bắt đầu – giờ kết thúc”.'),
    ('Nhóm THỜI GIAN & THỜI LƯỢNG: Thời lượng', 'Table/Grid', 'Read-only', '≥ 0 phút', 'Theo dữ liệu',
     'Dòng Dự án: chip “Tổng: n phút”; dòng Meeting: “n phút”.'),
    ('Nhóm LOẠI & HÌNH THỨC: Loại meeting', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng Dự án: mỗi loại 1 chip “<Tên loại>: n” bấm được (FR-06); dòng Meeting: tên loại.'),
    ('Nhóm LOẠI & HÌNH THỨC: Hình thức', 'Table/Grid', 'Read-only', 'Trực tiếp / Online', 'Theo dữ liệu',
     'Dòng Dự án: chip “Trực tiếp: n”, “Online: n” bấm được (FR-07); dòng Meeting: tên hình thức.'),
    ('Cột Số người tham gia', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Chip “Tổng: n” bấm được ở dòng Dự án và dòng Meeting (FR-08).'),
    ('Cột Biên bản', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng Meeting có biên bản → chip “Xem” (FR-09); không có → “—”.'),
    ('Thanh cuộn ngang trên và dưới bảng', 'Scroll', 'Enable', '–', 'Hiển thị', 'Hai thanh cuộn đồng bộ.'),
    ('Dòng tổng kết phân trang', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     '“Hiển thị a–b / n meeting”; khi tổng = 0 hiện “Không có meeting nào.”.'),
    ('Số dòng/trang', 'Dropdown', 'Enable', '10 / 20 / 50 / 100', '50', 'Tính theo số meeting.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', '–'),
    ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu...”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Đặt bộ lọc mặc định Tháng / tháng hiện tại / năm hiện tại; nạp danh mục loại meeting, giai đoạn '
     'dự án, dự án, nhân viên.\n'
     'After:\n– Tải bảng chi tiết trang 1 và biểu đồ.\n' + SCOPE + '\n– Lỗi → “Lỗi khi tải dữ liệu”.'),
    ('Bấm mũi tên / tên dòng Dự án', 'Click', 'After:\n– Mở hoặc đóng danh sách meeting của dự án.'),
    ('Đổi Số dòng/trang', 'Change', 'After:\n– Về trang 1 và tải lại bảng.'),
    ('Chuyển trang', 'Click', 'After:\n– Tải trang tương ứng, giữ bộ lọc.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc báo cáo')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả '
           'chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc báo cáo',
    mota='Lọc báo cáo theo khoảng thời gian meeting (Tháng / Năm / Tuỳ chỉnh), công ty, nhân viên tạo dự án, '
         'khách hàng, dự án, hình thức meeting, loại meeting, giai đoạn dự án. Bảng và biểu đồ cùng đổi theo.',
    tacnhan=ACT + '; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “Tìm kiếm nâng cao” để mở khối bộ lọc.\n'
          '2. Người dùng chọn giá trị ở các ô chọn — hệ thống tìm luôn khi đổi giá trị.\n'
          '3. Với ô Khách hàng, người dùng gõ tối thiểu 2 ký tự rồi chọn 1 khách hàng trong danh sách gợi ý.\n'
          '4. Hệ thống tải lại bảng (về trang 1) và biểu đồ theo bộ lọc.',
    phu='• Thiếu thông tin thời gian → thông báo lỗi (xem bảng event), không tải dữ liệu.\n'
        '• Bấm “Làm mới” → trả bộ lọc về mặc định và tải lại.\n'
        '• Đang ở chế độ Xem chi tiết → sau khi tải xong tự mở lại toàn bộ dự án.',
    dacbiet='Ô Công ty chỉ hiện với người có quyền V1. Giai đoạn dự án đang chọn mà nay bị khoá vẫn hiện trong '
            'danh sách (kèm 🔒).')
d.p('2.2.2 Layout màn hình')
layout(' => Tìm kiếm nâng cao', '02-bo-loc.png', 'Khối bộ lọc báo cáo đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Xem theo thời gian', 'Dropdown', 'Enable', 'Tuỳ chỉnh / Tháng / Năm', 'Có', 'Tháng',
     'Không cho xoá trống. Đổi kiểu thì xoá giá trị của các ô thời gian không còn hiện.'),
    ('Tháng', 'Dropdown', 'Enable / Ẩn', 'Tháng 1 – Tháng 12', 'Có khi chọn Tháng', 'Tháng hiện tại',
     'Chỉ hiện khi Xem theo thời gian = Tháng.'),
    ('Năm', 'Dropdown', 'Enable / Ẩn', '5 năm trước → năm sau', 'Có khi chọn Tháng / Năm', 'Năm hiện tại',
     'Năm mới nhất xếp trên.'),
    ('Thời gian meeting', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy – dd/mm/yyyy', 'Có khi chọn Tuỳ chỉnh', 'Trống',
     'Một ô chọn khoảng ngày; chỉ hiện khi chọn Tuỳ chỉnh.'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Chỉ hiện với quyền V1; biểu tượng 🔒 cạnh nhãn: bật để chọn cả công ty đã khoá. Lọc theo công ty của dự án.'),
    ('Nhân viên tạo dự án', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', 'Lọc theo người tạo dự án.'),
    ('Khách hàng', 'Textbox', 'Enable', '≥ 2 ký tự', 'Không', 'Trống',
     'Gõ để hiện gợi ý (tên; mã • số điện thoại); “Đang tìm...”, “Không tìm thấy khách hàng”. Xoá trắng ô thì '
     'bỏ chọn khách hàng và dự án.'),
    ('Dự án', 'Dropdown', 'Enable', 'Danh sách dự án TKT', 'Không', 'Trống',
     'Đã chọn khách hàng thì chỉ liệt kê dự án của khách hàng đó.'),
    ('Hình thức Meeting', 'Dropdown', 'Enable', 'Trực tiếp / Online', 'Không', 'Trống', '–'),
    ('Loại Meeting', 'Dropdown', 'Enable', 'Danh mục loại meeting', 'Không', 'Trống', 'Có ⓘ mô tả từng loại.'),
    ('Giai đoạn dự án', 'Dropdown', 'Enable', 'Danh mục giai đoạn', 'Không', 'Trống', 'Có ⓘ mô tả từng giai đoạn.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải lại theo bộ lọc.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Trả bộ lọc về mặc định rồi tải lại.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Tìm kiếm nâng cao',
     'Mở / thu gọn khối bộ lọc.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở khối bộ lọc; nút đổi thành “Ẩn tìm kiếm nâng cao”.'),
    ('Đổi giá trị ô chọn', 'Change',
     'During:\n– Tuỳ chỉnh mà thiếu ngày → “Vui lòng chọn đầy đủ Thời gian meeting từ và Thời gian meeting đến”.\n'
     '– Tháng mà thiếu Tháng hoặc Năm → “Vui lòng chọn đầy đủ Tháng và Năm”.\n'
     '– Năm mà thiếu Năm → “Vui lòng chọn Năm”.\n'
     '– Nếu thiếu → không thực hiện bước After.\n'
     'After:\n– Về trang 1, tải lại bảng và biểu đồ.'),
    ('Gõ vào ô Khách hàng', 'Keypress',
     'After:\n– Từ 2 ký tự trở lên → tìm khách hàng theo tên / mã, hiện danh sách gợi ý.\n'
     '– Xoá trắng khi đã chọn → bỏ khách hàng và dự án đã chọn.'),
    ('Chọn 1 khách hàng gợi ý', 'Click',
     'After:\n– Ghi khách hàng vào bộ lọc, đóng gợi ý; dự án đang chọn không thuộc khách hàng này thì bị bỏ.'),
    ('Bấm Tìm kiếm / Enter ở ô Khách hàng', 'Click', 'After:\n– Kiểm tra thời gian như trên rồi tải lại.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Trả bộ lọc về Tháng / tháng hiện tại / năm hiện tại, xoá các ô khác, tải lại.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Cài đặt bộ lọc')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột (áp tương tự cho cấu hình trường lọc). Chỉ bổ sung các quy tắc riêng '
           'tại phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Chọn trường lọc nào được hiển thị trong khối bộ lọc và sắp xếp thứ tự bằng kéo thả. Cài đặt lưu theo '
         'từng người dùng cho riêng báo cáo này.',
    tacnhan=ACT + '; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
          '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 10 trường lọc kèm ô tích.\n'
          '3. Người dùng bỏ tích / tích lại, kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm “Lưu” → hệ thống lưu và báo “Cập nhật thành công”.',
    phu='• Bấm “Khôi phục mặc định” → hiện đủ trường theo thứ tự gốc (chưa lưu cho tới khi bấm Lưu).\n'
        '• Lưu lỗi → “Thao tác thất bại”.\n'
        '• Trường bị ẩn đang có giá trị lọc → giá trị đó bị xoá để không lọc ngầm.')
d.p('2.3.2 Layout màn hình')
layout(' => Cài đặt bộ lọc', '03-cai-dat-bo-loc.png', 'Cửa sổ Cài đặt bộ lọc', modal='Cài đặt bộ lọc')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
    ('Danh sách trường lọc', 'Checkbox', 'Enable', '10 trường', 'Không', 'Theo cấu hình đã lưu',
     'Xem theo thời gian, Tháng, Năm, Công ty, Nhân viên tạo dự án, Khách hàng, Dự án, Hình thức Meeting, Loại '
     'Meeting, Giai đoạn dự án; mỗi dòng có số thứ tự và tay kéo ⠿.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Khoá trong lúc đang lưu.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Đóng / ×', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
])
d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở cửa sổ với cấu hình đã lưu của người dùng (chưa có → hiện đủ).'),
    ('Kéo ⠿', 'Change', 'After:\n– Đổi thứ tự trường trong cửa sổ.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Lưu cấu hình theo người dùng + báo cáo; đóng cửa sổ; “Cập nhật thành công”.\n'
     '– Khối bộ lọc hiện đúng các trường đã tích theo thứ tự mới; trường bị ẩn có giá trị thì xoá giá trị.\n'
     '– Lỗi → “Thao tác thất bại”.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Tích lại toàn bộ, trả thứ tự gốc trong cửa sổ.'),
    ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng cửa sổ, không lưu.'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Xem biểu đồ Top 5 dự án')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của biểu đồ tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Xem biểu đồ Top 5 dự án',
    mota='Biểu đồ cột 2 trục: Số meeting và Tổng phút của 5 dự án dẫn đầu; bảng “Chi tiết theo biểu đồ” bên phải '
         'liệt kê đúng 5 dự án đó. Luôn tính theo bộ lọc đang áp dụng.',
    tacnhan=ACT + '; Người dùng đã đăng nhập',
    dieukien='Bộ lọc thời gian hợp lệ.',
    chinh='1. Hệ thống tải biểu đồ cùng lúc với bảng (mở màn, tìm kiếm, làm mới).\n'
          '2. Biểu đồ và bảng bên phải hiển thị tối đa 5 dự án.\n'
          '3. Người dùng đổi “Sắp theo” → hệ thống tải lại và sắp xếp theo tiêu chí mới.',
    phu='• Không có dữ liệu → bảng bên phải hiện “Không có dữ liệu.”, biểu đồ trống.\n'
        '• Lỗi tải → “Lỗi khi tải dữ liệu biểu đồ”.\n'
        '• Bộ lọc thời gian chưa hợp lệ → ô Sắp theo bị khoá.')
d.p('2.4.2 Layout màn hình')
layout('', '04-bieu-do.png', 'Biểu đồ Top 5 dự án và bảng Chi tiết theo biểu đồ')
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề', 'Label', 'Hiển thị', '–', 'Biểu đồ Top 5 dự án',
     'Kèm ⓘ: “Biểu đồ luôn lấy theo dữ liệu đã lọc của báo cáo + bảng chi tiết.”'),
    ('Sắp theo', 'Dropdown', 'Enable / Disable', 'Số meeting / Tổng phút', 'Số meeting',
     'Khoá khi bộ lọc thời gian chưa đủ.'),
    ('Chú giải', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Số meeting (xanh lá), Tổng phút (xanh dương), “• Tổng: n meeting • n phút”.'),
    ('Biểu đồ cột', 'Chart', 'Read-only', 'Tối đa 5 dự án', 'Theo bộ lọc',
     'Trục trái: Meeting; trục phải: Phút; rê chuột hiện số liệu của dự án.'),
    ('Bảng Chi tiết theo biểu đồ', 'Table/Grid', 'Read-only', 'Tối đa 5 dòng', 'Theo bộ lọc',
     'Cột #, Dự án (Top 5), Meeting, Phút; góc phải tiêu đề “n dự án”.'),
    ('Ghi chú cuối bảng', 'Label', 'Hiển thị', '–', 'Hiển thị', '“Dữ liệu luôn thay đổi theo bộ lọc báo cáo.”'),
], required=False)
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn / Tìm kiếm / Làm mới', 'System',
     'After:\n– Tải số liệu biểu đồ theo bộ lọc: với mỗi dự án đếm mọi cuộc họp gắn dự án và cộng thời lượng.\n'
     '– Lỗi → “Lỗi khi tải dữ liệu biểu đồ”.'),
    ('Đổi Sắp theo', 'Change',
     'After:\n– Tải lại, sắp giảm dần theo tiêu chí đã chọn (bằng nhau thì xét tiêu chí còn lại, rồi theo tên).'),
    ('Rê chuột lên cột', 'Hover', 'After:\n– Hiện Số meeting và Tổng phút của dự án.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Xem chi tiết dự án')
d.p('2.5.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='detail')
d.intro_table(
    ten='Xem chi tiết dự án',
    mota='Mở danh sách meeting của toàn bộ dự án trong trang bằng 1 lần bấm, hoặc thu về chỉ cấp gốc.',
    tacnhan=ACT + '; Người dùng đã đăng nhập',
    dieukien='Bảng đang có dữ liệu.',
    chinh='1. Người dùng bấm “Xem chi tiết”.\n'
          '2. Hệ thống mở danh sách meeting của mọi dự án; nút đổi thành “Chỉ xem cấp gốc”.\n'
          '3. Người dùng bấm “Chỉ xem cấp gốc” → bảng thu về chỉ dòng Dự án.',
    phu='• Đang ở chế độ Xem chi tiết mà tìm kiếm lại → bảng tự mở lại toàn bộ dự án sau khi tải.\n'
        '• Mỗi trang chứa tối đa số meeting bằng Số dòng/trang; meeting của 1 dự án có thể nối sang trang sau.')
d.p('2.5.2 Layout màn hình')
layout(' => Xem chi tiết', '05-xem-chi-tiet.png', 'Bảng chi tiết ở chế độ Xem chi tiết')
d.p('2.5.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xem chi tiết / Chỉ xem cấp gốc', 'Button', 'Enable', '–', 'Xem chi tiết',
     'Nút nền xanh khi đang thu gọn; nút viền khi đang mở hết.'),
    ('Dòng Dự án', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Nền xanh nhạt; số liệu tổng tính trên toàn bộ cuộc họp của dự án.'),
    ('Dòng Meeting', 'Table/Grid', 'Read-only', '–', 'Ẩn tới khi mở',
     'Mã — Tên, thời gian, thời lượng, loại, hình thức, số người tham gia, biên bản; các cột thông tin dự án hiện “—”.'),
], required=False)
d.p('2.5.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xem chi tiết', 'Click', 'After:\n– Mở danh sách meeting của toàn bộ dự án trong trang đang xem.'),
    ('Bấm Chỉ xem cấp gốc', 'Click', 'After:\n– Đóng toàn bộ, chỉ còn dòng Dự án.'),
])


def drill(so, ten, tail, png, caption, modal, mota, chinh, phu, ui, ev):
    d.h3('2.%d %s' % (so, ten))
    d.p('2.%d.1 Giới thiệu' % so)
    d.rule_ref('- Màn Xem chi tiết và Phân quyền; Quy tắc Excel. Chỉ bổ sung các quy tắc riêng tại phần mô tả '
               'chi tiết.', anchor='detail')
    d.intro_table(ten=ten, mota=mota, tacnhan=ACT + '; Người dùng đã đăng nhập',
                  dieukien='Bảng chi tiết đang có dữ liệu.', chinh=chinh, phu=phu)
    d.p('2.%d.2 Layout màn hình' % so)
    layout(tail, png, caption, modal=modal)
    d.p('2.%d.3 Mô tả chi tiết giao diện' % so)
    d.ui_table(ui, required=False)
    d.p('2.%d.4 Danh sách event và xử lý event' % so)
    d.event_table(ev)


POPUP_COMMON = [
    ('Nút Xuất Excel (trong cửa sổ)', 'Button', 'Enable', '–', 'Hiển thị',
     'Tải file Excel danh sách đang hiển thị (xếp theo ngày tăng dần, có cột STT).'),
    ('Nút Đóng / ×', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
    ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu...”.'),
]

drill(6, 'Xem danh sách meeting theo loại', ' => Xem chi tiết => Loại meeting', '06-theo-loai.png',
      'Cửa sổ danh sách meeting theo loại', '“Loại: <tên loại>”',
      'Bấm chip loại meeting ở dòng Dự án (vd “Meeting với khách hàng: 1”) để xem danh sách cuộc họp loại đó '
      'của dự án.',
      '1. Người dùng bấm chip loại meeting ở dòng Dự án.\n'
      '2. Hệ thống mở cửa sổ “Loại: <tên loại>”, dòng phụ “Dự án: <tên> • n meeting”.\n'
      '3. Hệ thống tải các cuộc họp thuộc loại đó của dự án, mới nhất ở trên.',
      '• Không có cuộc họp → “Không có meeting.”.\n• Lỗi tải → “Lỗi khi tải danh sách meeting”.',
      [('Tiêu đề + dòng phụ', 'Label', 'Hiển thị', '–', 'Theo chip đã bấm', 'Có biểu tượng tròn bên trái.'),
       ('Bảng meeting', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Cột: Mã, Tên meeting, Ngày (dd/mm/yyyy), Phút, Loại, Hình thức, Dự án, Khách hàng.'),
       ('Ghi chú', 'Label', 'Hiển thị', '–', 'Hiển thị',
        '“Popup hiển thị đúng danh sách meeting theo tiêu chí bạn click.”')] + POPUP_COMMON,
      [('Bấm chip loại meeting', 'Click',
        'After:\n– Mở cửa sổ, tải cuộc họp đúng loại của dự án đã bấm (dự án vẫn phải khớp bộ lọc hiện tại).\n'
        '– Lỗi → “Lỗi khi tải danh sách meeting”.'),
       ('Bấm Xuất Excel trong cửa sổ', 'Click',
        'After:\n– Tải file “Danh Sách Meeting Theo Loại <tên loại>.xlsx” (cột STT, Mã, Tên meeting, Ngày, Phút, '
        'Loại, Hình thức, Dự án, Khách hàng).'),
       ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng cửa sổ.')])

drill(7, 'Xem danh sách meeting theo hình thức', ' => Xem chi tiết => Hình thức', '07-theo-hinh-thuc.png',
      'Cửa sổ danh sách meeting theo hình thức', '“Hình thức: Trực tiếp / Online”',
      'Bấm chip “Trực tiếp: n” hoặc “Online: n” ở dòng Dự án để xem đúng các cuộc họp đã đếm vào chip.',
      '1. Người dùng bấm chip hình thức ở dòng Dự án.\n'
      '2. Hệ thống mở cửa sổ “Hình thức: Trực tiếp” (hoặc Online), dòng phụ “Dự án: <tên> • n meeting”.\n'
      '3. Hệ thống tải đúng các cuộc họp mà chip đã đếm.',
      '• Không có cuộc họp → “Không có meeting.”.\n• Lỗi tải → “Lỗi khi tải danh sách meeting”.',
      [('Tiêu đề + dòng phụ', 'Label', 'Hiển thị', '–', 'Theo chip đã bấm', '–'),
       ('Bảng meeting', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Cột: Mã, Tên meeting, Ngày, Phút, Loại, Dự án, Khách hàng.'),
       ('Ghi chú', 'Label', 'Hiển thị', '–', 'Hiển thị',
        '“Popup hiển thị đúng danh sách meeting theo tiêu chí bạn click.”')] + POPUP_COMMON,
      [('Bấm chip Trực tiếp / Online', 'Click',
        'After:\n– Mở cửa sổ, tải các cuộc họp có trong chip (cùng hình thức).\n'
        '– Lỗi → “Lỗi khi tải danh sách meeting”.'),
       ('Bấm Xuất Excel trong cửa sổ', 'Click',
        'After:\n– Tải file “Danh Sách Meeting Theo Hình Thức Trực Tiếp.xlsx” (hoặc “… Online.xlsx”).'),
       ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng cửa sổ.')])

drill(8, 'Xem danh sách người tham gia', ' => Xem chi tiết => Số người tham gia', '08-nguoi-tham-gia.png',
      'Cửa sổ danh sách người tham gia — tab Phía công ty', '“Danh sách người tham gia”',
      'Bấm chip “Tổng: n” ở cột Số người tham gia để xem người tham gia, tách 2 tab Phía công ty / Phía KH.',
      '1. Người dùng bấm chip “Tổng: n” ở dòng Dự án hoặc dòng Meeting.\n'
      '2. Hệ thống mở cửa sổ “Danh sách người tham gia”, dòng phụ “<Dự án / Meeting> • n người”.\n'
      '3. Hệ thống tải người tham gia, mặc định mở tab Phía công ty (không có người phía công ty → mở Phía KH).',
      '• Tab không có người → nút tab bị khoá.\n• Không có dữ liệu → “Không có dữ liệu.”.\n'
      '• Lỗi tải → “Lỗi khi tải danh sách người tham gia”.\n'
      '• Xuất Excel lỗi → “Lỗi khi xuất Excel, đã xuất CSV thay thế” và tải file CSV.',
      [('Tab Phía công ty (n) / Phía KH (n)', 'Tab', 'Enable / Disable', '–', 'Phía công ty',
        'Số trong ngoặc là số người của tab.'),
       ('Bảng người tham gia', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Cột STT, Họ tên, Chức vụ, SĐT; tab Phía công ty mở từ dòng Dự án có thêm cột “Số lần tham gia meeting”. '
        'Mỗi nhân viên chỉ 1 dòng.'),
       ('Ghi chú', 'Label', 'Hiển thị', '–', 'Hiển thị',
        '“Cột "Số người tham gia" trên bảng chỉ là tổng. Click vào để xem chi tiết theo phía Công ty / phía KH.”')]
      + POPUP_COMMON,
      [('Bấm chip Tổng ở cột Số người tham gia', 'Click',
        'After:\n– Mở cửa sổ, tải người tham gia của các cuộc họp thuộc dòng đã bấm.\n'
        '– Lỗi → “Lỗi khi tải danh sách người tham gia”.'),
       ('Bấm tab Phía công ty / Phía KH', 'Click', 'After:\n– Đổi danh sách hiển thị.'),
       ('Bấm Xuất Excel trong cửa sổ', 'Click',
        'After:\n– Tải file “Danh Sách Người Tham Gia.xlsx”: phía công ty trước, phía khách hàng sau.'),
       ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng cửa sổ.')])

drill(9, 'Xem biên bản cuộc họp', ' => Xem chi tiết => Xem', '09-bien-ban.png',
      'Cửa sổ Xem biên bản cuộc họp', '“Xem biên bản cuộc họp”',
      'Xem bản biên bản cuộc họp (mẫu in của cuộc họp) và in biên bản.',
      '1. Người dùng mở chi tiết dự án, bấm chip “Xem” ở cột Biên bản của dòng Meeting.\n'
      '2. Hệ thống mở cửa sổ “Xem biên bản cuộc họp” và tải mẫu biên bản.\n'
      '3. Người dùng bấm “In biên bản” để mở hộp thoại in.',
      '• Cuộc họp chưa có biên bản → cột hiện “—”, không có nút Xem.\n'
      '• Không lấy được mẫu → “Không thể tải biên bản”, đóng cửa sổ.\n'
      '• Lỗi → “Lỗi khi tải biên bản”, đóng cửa sổ.',
      [('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Xem biên bản cuộc họp', '–'),
       ('Nút In biên bản', 'Button', 'Enable', '–', 'Hiển thị', 'Mở biên bản ở thẻ mới và bật hộp thoại in.'),
       ('Nội dung biên bản', 'Text', 'Read-only', '–', 'Theo dữ liệu',
        'Số biên bản, ngày lập, thông tin cuộc họp, thời gian, thành phần tham gia, nội dung.'),
       ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải biên bản...”.'),
       ('Nút ×', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.')],
      [('Bấm Xem', 'Click',
        'After:\n– Mở cửa sổ, tải mẫu biên bản của cuộc họp.\n'
        '– Không có mẫu → “Không thể tải biên bản”; lỗi → “Lỗi khi tải biên bản”; cả 2 trường hợp đóng cửa sổ.'),
       ('Bấm In biên bản', 'Click', 'After:\n– Mở biên bản ở thẻ mới (font Times New Roman) và bật hộp thoại in.'),
       ('Bấm ×', 'Click', 'After:\n– Đóng cửa sổ.')])

# ------------------------------------------------------------------ 2.10
d.h3('2.10 Xuất Excel báo cáo')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xuất Excel báo cáo', 'io', actor=ACT)
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Thông báo. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='Xuất Excel báo cáo',
    mota='Tải file Excel toàn bộ báo cáo theo bộ lọc đang áp dụng (không phân trang), giữ cấu trúc Dự án → Meeting.',
    tacnhan=ACT + '; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “Xuất Excel” trên bảng chi tiết.\n'
          '2. Hệ thống lấy toàn bộ dữ liệu theo bộ lọc và phạm vi quyền.\n'
          '3. Trình duyệt tải file “bao_cao_meeting_theo_du_an.xls”.',
    phu='• Lỗi → “Lỗi khi xuất Excel”.',
    dacbiet='File gồm: ảnh tiêu đề (letterhead) của công ty đang làm việc, tiêu đề “BÁO CÁO THEO DÕI MEETING '
            'THEO TỪNG DỰ ÁN”, 8 cột STT, Đối tượng, Thời gian, Thời lượng (phút), Loại, Hình thức, Số người tham '
            'gia, Biên bản; dòng Dự án tô màu.')
d.p('2.10.3 Layout màn hình')
layout(' => Xuất Excel', '10-xuat-excel.png', 'Nút Xuất Excel trên bảng chi tiết')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xuất Excel', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Biểu tượng file Excel.'),
    ('File tải về', 'File', 'Read-only', '.xls', '–', '–', 'Tên file: bao_cao_meeting_theo_du_an.xls.'),
])
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Bỏ các ô lọc trống và tham số phân trang.\n'
     'After:\n– Hệ thống dựng file từ toàn bộ dữ liệu theo bộ lọc + phạm vi quyền và trả về để trình duyệt tải.\n'
     '– Lỗi → “Lỗi khi xuất Excel”.'),
])

# ------------------------------------------------------------------ 2.11
d.h3('2.11 In báo cáo')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'In báo cáo', 'io', actor=ACT)
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Thông báo. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='In báo cáo',
    mota='Mở bản in báo cáo ở thẻ mới theo bộ lọc hiện tại rồi in khổ A4 ngang.',
    tacnhan=ACT + '; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “In danh sách”.\n'
          '2. Hệ thống mở bản in ở thẻ mới, tải toàn bộ dữ liệu theo bộ lọc (không phân trang).\n'
          '3. Người dùng bấm “In” trên bản in → hộp thoại in của trình duyệt.',
    phu='• Không có dữ liệu → bản in hiện “Không có dữ liệu”.\n'
        '• Lỗi tải dữ liệu → khung báo lỗi đỏ trên bản in.',
    dacbiet='Bản in có ảnh tiêu đề công ty đang làm việc, tiêu đề “BÁO CÁO THEO DÕI MEETING THEO TỪNG DỰ ÁN”, '
            '8 cột cố định (không chọn cột), STT phân cấp (1, 1.1) và khối ký “Ngày ...., tháng ...., năm .... / '
            'Người lập / (Ký, họ tên)”.')
d.p('2.11.3 Layout màn hình')
layout(' => In danh sách', '11-ban-in.png', 'Bản in báo cáo mở ở thẻ mới',
       extra='Bản in mở ở thẻ mới của trình duyệt.')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In danh sách', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở bản in ở thẻ mới.'),
    ('Nút In (trên bản in)', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Bật hộp thoại in; nút không xuất hiện trên giấy.'),
    ('Ảnh tiêu đề công ty', 'Image', 'Read-only', '–', '–', 'Theo công ty đang làm việc', '–'),
    ('Bảng bản in', 'Table/Grid', 'Read-only', '8 cột', '–', 'Theo bộ lọc',
     'STT, Đối tượng, Thời gian, Thời lượng (phút), Loại, Hình thức, Số người tham gia, Biên bản; dòng Dự án in '
     'đậm “Dự án: <tên>”, dòng meeting thụt lề; cột Biên bản ghi nội dung biên bản hoặc “Chưa lập biên bản”.'),
    ('Khối ký', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Ngày ...., tháng ...., năm .... / Người lập / (Ký, họ tên)”.'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In danh sách', 'Click',
     'After:\n– Mở thẻ mới với bộ lọc hiện tại; bản in tải toàn bộ dữ liệu theo phạm vi quyền.\n'
     '– Lỗi → khung báo lỗi đỏ với nội dung lỗi hoặc “Lỗi không xác định khi tải dữ liệu báo cáo”.'),
    ('Bấm In trên bản in', 'Click', 'After:\n– Bật hộp thoại in của trình duyệt.'),
])

# ==================================================== PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của báo cáo Meeting theo dự án; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Dự án được đưa vào báo cáo', [
        '– Dự án TKT có tiến trình khác “Đang tạo”.',
        '– Có ít nhất 1 cuộc họp gắn dự án ở trạng thái Chốt lịch hoặc Hoàn thành.',
        '– Có cuộc họp gắn dự án khớp khoảng thời gian (theo ngày bắt đầu), loại meeting, hình thức đang lọc.',
        '– Khớp các bộ lọc của dự án: công ty, người tạo dự án, khách hàng, dự án, giai đoạn.',
    ], ['Xem báo cáo', 'Biểu đồ', 'Xuất Excel', 'In']),
    ('BR-02', 'Cuộc họp hiển thị dưới dự án và số liệu tổng', [
        '– Dưới mỗi dự án liệt kê các cuộc họp gắn với dự án; số liệu tổng (số meeting, tổng phút, chip loại, '
        'hình thức, người tham gia) tính trên toàn bộ cuộc họp gắn dự án, không chỉ cuộc họp ở trang đang xem.',
        '– Thời lượng = số phút từ giờ bắt đầu tới giờ kết thúc của cuộc họp.',
    ], ['Xem báo cáo', 'Xem chi tiết dự án']),
    ('BR-03', 'Phân trang theo meeting', [
        '– Mỗi trang lấy tối đa n meeting (n = Số dòng/trang) theo thứ tự dự án mới tạo trước; dự án nào có '
        'meeting trong trang thì hiện dòng dự án.',
        '– Tổng ở dòng phân trang = số cuộc họp Chốt lịch / Hoàn thành của các dự án khớp bộ lọc.',
    ], 'Xem báo cáo'),
    ('BR-04', 'Phạm vi dữ liệu theo quyền', [
        '– V1: mọi dự án; V2: dự án thuộc công ty đang làm việc hoặc do mình tạo; không có quyền: dự án mình tạo '
        'hoặc mình là nhân viên kinh doanh chính.',
        '– Phạm vi áp cho bảng, biểu đồ, cửa sổ chi tiết, file Excel và bản in.',
    ], 'Toàn màn hình'),
    ('BR-05', 'Top 5 dự án', [
        '– Lấy 5 dự án đứng đầu theo tiêu chí Sắp theo (Số meeting hoặc Tổng phút).',
    ], 'Biểu đồ'),
    ('BR-06', 'Khoảng thời gian bắt buộc', [
        '– Phải chọn đủ thông tin thời gian theo kiểu xem (Tháng + Năm / Năm / Từ ngày – Đến ngày) mới tải được '
        'báo cáo.',
    ], 'Tìm kiếm và lọc'),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

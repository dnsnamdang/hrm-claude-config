# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo Meeting theo nhân viên - phòng ban - công ty.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/report/meeting-by-employees/{index,print}.vue + components/*
      components/V2BaseSmartFilterPanel.vue · modal/filter-customization-modal.vue
      components/subsystem-menu/{meeting,presale}.js
  BE  Modules/Assign/Routes/api.php (prefix assign/report/meeting-by-employees)
      ReportController::meetingByEmployees* · Services/Report/MeetingByEmployeesService
      app/ExcelExport/MeetingByEmployeesExport + exports/meeting_by_employees_report.blade.php
  Quyền: PermissionsTableSeeder id 1057–1059 (nhóm "Báo cáo meeting theo nhân viên")
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


TEN_MAN = 'Báo cáo Meeting theo nhân viên - phòng ban - công ty'
MENU_A = 'Phân hệ Meeting => Báo cáo => Meeting theo nhân viên/ phòng ban/ công ty'
MENU_B = ('Phân hệ CSKH trước bán => Báo cáo => Báo cáo dự án tiền khả thi'
          ' => Báo cáo meeting nhân viên theo thời gian')
ACT = 'Người xem báo cáo meeting'

ICONS = {
    'Phân hệ Meeting': 'icon_phanhe_mt.png',
    'Phân hệ CSKH trước bán': 'icon_phanhe_ps.png',
    'Báo cáo': 'icon_mt_baocao.png',
    'Meeting theo nhân viên/ phòng ban/ công ty': 'icon_mt_nv.png',
    'Báo cáo dự án tiền khả thi': 'icon_ps_nhom.png',
    'Báo cáo meeting nhân viên theo thời gian': 'icon_ps_nv.png',
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
    'Xem trước': 'icon_xemtruoc.png',
}

d = SrsDoc(out=os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN), menu=MENU_A, route='', full_url='',
           img_dir=os.path.join(HERE, '.uml'), img_prefix='mtnv_')
d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})


def menu_b(menu):
    """Dòng menu CSKH trước bán: mục "Báo cáo" ở phân hệ này có icon khác phân hệ Meeting."""
    d.menu_icons['Báo cáo'] = shot('icon_ps_baocao.png')
    d._menu_para(menu)
    d.menu_icons['Báo cáo'] = shot('icon_mt_baocao.png')


def layout(tail, png, caption, modal=None):
    """Mục Layout: báo cáo có 2 lối vào menu (cùng 1 màn, cùng phạm vi dữ liệu)."""
    d.p('Đường dẫn màn hình:')
    d._menu_para(MENU_A + tail)
    menu_b(MENU_B + tail)
    d.p('Hai lối vào mở CÙNG một báo cáo, dữ liệu như nhau; chỉ khác thanh menu bên trái giữ theo '
        'phân hệ người dùng đang làm việc.')
    if modal:
        d.p('Cửa sổ %s được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.' % modal)
    d.figure(shot(png), caption, width_in=6.2)


NO_DATA_SCOPE = ('– Hệ thống chỉ lấy thành viên phía công ty nằm trong phạm vi quyền (V1/V2/V3, '
                 'không có quyền nào → chỉ bản thân).')

d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho báo cáo Meeting theo nhân viên - phòng ban - công ty '
    '(tiêu đề trên màn hình: “Báo cáo meeting nhân viên theo thời gian”), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền dữ liệu của báo cáo.',
    'Làm rõ mỗi nhân viên trong khoảng thời gian được chọn có bao nhiêu cuộc meeting, loại nào, hình thức '
    'nào, với khách hàng / dự án nào, tổng thời gian, rồi tổng hợp lên cấp phòng ban và cấp công ty.',
    'Làm rõ cuộc họp nào được tính vào báo cáo theo trạng thái và mốc thời gian của từng cuộc họp.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Meeting', 'Cuộc họp lập ở phân hệ Meeting (Tổng hợp meeting), có mã dạng TPE.MET.KH.26.0060.'),
    ('Thành viên phía công ty', 'Nhân viên của công ty được thêm vào cuộc họp (có mã nhân viên).'),
    ('Thành viên phía KH', 'Người của khách hàng được thêm vào cuộc họp.'),
    ('Cấp gốc', 'Dòng Công ty — cấp cao nhất của bảng phân cấp Công ty → Phòng ban → Nhân viên → Meeting.'),
    ('Thời lượng', 'Số phút từ giờ bắt đầu tới giờ kết thúc của cuộc họp; cuộc họp Hủy tính 0 phút.'),
    ('Hình thức', 'Trực tiếp hoặc Online.'),
    ('Dự án TKT', 'Dự án tiền khả thi gắn với cuộc họp.'),
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
    ('V1', 'Xem báo cáo meeting theo nhân viên theo tổng công ty',
     'Toàn bộ nhân viên của mọi công ty.'),
    ('V2', 'Xem báo cáo meeting theo nhân viên theo công ty',
     'Nhân viên thuộc công ty đang làm việc.'),
    ('V3', 'Xem báo cáo meeting theo nhân viên theo phòng ban',
     'Nhân viên thuộc phòng ban / bộ phận người dùng đang quản lý.'),
    ('–', 'Không có quyền nào ở trên', 'Chỉ dòng của chính người dùng và các cuộc họp người dùng tham gia.'),
], widths=[0.8, 2.4, 2.8])
d.p('Có nhiều quyền cùng lúc thì lấy phạm vi rộng nhất theo thứ tự V1 → V2 → V3.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'V1', 'V2', 'V3', 'Không có quyền nào'], [
    ('FR-01 Xem báo cáo meeting theo nhân viên', '✅', '✅', '✅', '✅ (chỉ bản thân)'),
    ('FR-02 Tìm kiếm và lọc báo cáo', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅'),
    ('FR-04 Xem biểu đồ Top phòng ban và Top nhân viên', '✅', '✅', '✅', '✅ (chỉ bản thân)'),
    ('FR-05 Xem chi tiết phân cấp', '✅', '✅', '✅', '✅'),
    ('FR-06 Xem danh sách meeting theo loại', '✅', '✅', '✅', '✅'),
    ('FR-07 Xem danh sách meeting theo hình thức', '✅', '✅', '✅', '✅'),
    ('FR-08 Xem danh sách người tham gia', '✅', '✅', '✅', '✅'),
    ('FR-09 Xem biên bản cuộc họp', '✅', '✅', '✅', '✅'),
    ('FR-10 Xuất Excel báo cáo', '✅', '✅', '✅', '✅ (chỉ bản thân)'),
    ('FR-11 In báo cáo', '✅', '✅', '✅', '✅ (chỉ bản thân)'),
], widths=[2.8, 0.55, 0.55, 0.55, 1.55])

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACT, [0, 1, 2])],
    [('FR-01', 'Xem báo cáo meeting theo nhân viên', 'view'),
     ('FR-10', 'Xuất Excel báo cáo', 'io'),
     ('FR-11', 'In báo cáo', 'io')],
    [('FR-02', 'Tìm kiếm và lọc báo cáo', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Xem biểu đồ Top phòng ban / nhân viên', 'view', 'extend', [0], None),
     ('FR-05', 'Xem chi tiết phân cấp', 'view', 'extend', [0], None),
     ('FR-06', 'Xem meeting theo loại', 'view', 'extend', [0], None),
     ('FR-07', 'Xem meeting theo hình thức', 'view', 'extend', [0], None),
     ('FR-08', 'Xem danh sách người tham gia', 'view', 'extend', [0], None),
     ('FR-09', 'Xem biên bản cuộc họp', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem báo cáo meeting theo nhân viên')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Phân trang và UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả '
           'chi tiết.', anchor='list')
d.intro_table(
    ten='Xem báo cáo meeting theo nhân viên',
    mota='Hiển thị trên 1 màn: bộ lọc (thu gọn), biểu đồ Top phòng ban kèm bảng Top nhân viên, và bảng chi tiết '
         'phân cấp Công ty → Phòng ban → Nhân viên → Meeting. Lúc mở, bảng chỉ hiện cấp gốc (dòng Công ty).',
    tacnhan=ACT + '; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập.',
    chinh='1. Người dùng vào báo cáo theo một trong 2 đường dẫn menu.\n'
          '2. Hệ thống đặt sẵn bộ lọc: Xem theo thời gian = Tháng, Tháng = tháng hiện tại, Năm = năm hiện tại.\n'
          '3. Hệ thống tải bảng chi tiết (50 meeting/trang) và biểu đồ theo bộ lọc mặc định.\n'
          '4. Bảng hiển thị các dòng Công ty kèm số nhân viên, số meeting, tổng phút, số buổi hủy, chip đếm theo '
          'loại meeting, theo hình thức và tổng người tham gia.',
    phu='• Không có cuộc họp nào trong phạm vi → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.\n'
        '• Đổi số dòng/trang hoặc chuyển trang → tải lại bảng, giữ nguyên bộ lọc.')
d.p('2.1.2 Layout màn hình')
layout('', '01-xem-bao-cao.png', 'Báo cáo meeting nhân viên theo thời gian lúc mới mở (tháng 10/2026)')
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Báo cáo meeting nhân viên theo thời gian',
     'Kèm ⓘ: “Xem được mỗi nhân viên trong khoảng thời gian được chọn có bao nhiêu cuộc meeting, loại nào, với '
     'KH nào, tổng thời gian, kết quả =>> Tổng hợp số liệu lên cấp phòng =>> Cấp công ty”.'),
    ('Khối bộ lọc', 'Card', 'Hiển thị', '–', 'Thu gọn',
     'Tiêu đề “Bộ lọc báo cáo meeting nhân viên theo thời gian”; nút Cài đặt bộ lọc, Tìm kiếm nâng cao (FR-02, FR-03).'),
    ('Khối biểu đồ Top phòng ban', 'Card', 'Hiển thị', '–', 'Theo bộ lọc', 'Xem FR-04.'),
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Bảng chi tiết meeting nhân viên theo thời gian',
     'Kèm ⓘ: “Cấu trúc: Công ty → Phòng ban → Nhân viên → Meeting. Click mũi tên để mở/đóng cấp con.”'),
    ('Nút Xem chi tiết', 'Button', 'Enable', '–', 'Hiển thị', 'Mở toàn bộ các cấp (FR-05).'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-10.'),
    ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-11.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Mũi tên mở/đóng',
     'Dòng Công ty/Phòng/Nhân viên là nút mũi tên; dòng Meeting là số thứ tự trong nhân viên.'),
    ('Cột Công ty / Phòng / Nhân viên / Meeting', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng Công ty/Phòng: tên + “Nhân viên: n • Số meeting: n” (+ “• Hủy: n” nếu có). Dòng Nhân viên: tên + '
     '“Số meeting: n”. Dòng Meeting: “Mã — Tên” (+ nhãn “Hủy”), dòng phụ “Người tạo: … • Ngày tạo: dd/mm/yyyy”.'),
    ('Nhóm THÔNG TIN NHÂN VIÊN: Chức vụ, Mã nhân viên', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Chỉ có ở dòng Nhân viên; Chức vụ lấy theo chức vụ ghi trong cuộc họp.'),
    ('Nhóm THỜI GIAN & THỜI LƯỢNG: Thời gian', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Chỉ ở dòng Meeting: ngày + “giờ bắt đầu – giờ kết thúc”.'),
    ('Nhóm THỜI GIAN & THỜI LƯỢNG: Thời lượng', 'Table/Grid', 'Read-only', '≥ 0 phút', 'Theo dữ liệu',
     'Dòng tổng: chip “Tổng: n phút”; dòng Meeting: “n phút”.'),
    ('Nhóm LOẠI & HÌNH THỨC: Loại meeting', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng tổng: mỗi loại 1 chip “<Tên loại>: n” bấm được (FR-06); dòng Meeting: tên loại.'),
    ('Nhóm LOẠI & HÌNH THỨC: Hình thức', 'Table/Grid', 'Read-only', 'Trực tiếp / Online', 'Theo dữ liệu',
     'Dòng tổng: 2 chip “Trực tiếp: n”, “Online: n” bấm được (FR-07); dòng Meeting: tên hình thức.'),
    ('Cột Số người tham gia', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Chip “Tổng: n” bấm được ở mọi cấp (FR-08).'),
    ('Cột Dự án, Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Chỉ ở dòng Meeting: dự án TKT gắn với cuộc họp và khách hàng của dự án.'),
    ('Cột Biên bản', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng Meeting có biên bản → chip “Xem” (FR-09); không có → “—”.'),
    ('Cột Nội dung meeting, Kết luận cuộc họp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Chỉ ở dòng Meeting; cắt còn 2 dòng, rê chuột xem đủ.'),
    ('Thanh cuộn ngang trên và dưới bảng', 'Scroll', 'Enable', '–', 'Hiển thị', 'Hai thanh cuộn đồng bộ.'),
    ('Dòng tổng kết phân trang', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     '“Hiển thị a–b / n meeting”; khi tổng = 0 hiện “Không có meeting nào.”.'),
    ('Số dòng/trang', 'Dropdown', 'Enable', '10 / 20 / 50 / 100', '50', '–'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', '–'),
    ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu...”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Đặt bộ lọc mặc định Tháng / tháng hiện tại / năm hiện tại; nạp danh mục loại meeting, dự án.\n'
     'After:\n– Tải bảng chi tiết trang 1 và biểu đồ.\n' + NO_DATA_SCOPE + '\n'
     '– Lỗi → “Lỗi khi tải dữ liệu”.'),
    ('Bấm mũi tên / tên dòng Công ty, Phòng, Nhân viên', 'Click',
     'After:\n– Mở hoặc đóng cấp con của dòng đó; đóng 1 dòng thì đóng luôn mọi cấp con bên dưới.'),
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
    mota='Lọc báo cáo theo khoảng thời gian (Tháng / Năm / Tuỳ chỉnh), tổ chức (Công ty, Phòng ban, Bộ phận, '
         'Nhân viên), khách hàng, dự án, loại meeting, hình thức meeting. Bảng và biểu đồ cùng đổi theo.',
    tacnhan=ACT + '; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “Tìm kiếm nâng cao” để mở khối bộ lọc.\n'
          '2. Người dùng chọn giá trị ở các ô chọn — hệ thống tìm luôn khi đổi giá trị.\n'
          '3. Với ô Khách hàng, người dùng gõ tối thiểu 2 ký tự rồi chọn 1 khách hàng trong danh sách gợi ý.\n'
          '4. Hệ thống tải lại bảng (về trang 1) và biểu đồ theo bộ lọc.',
    phu='• Thiếu thông tin thời gian → thông báo lỗi (xem bảng event), không tải dữ liệu.\n'
        '• Bấm “Làm mới” → trả bộ lọc về mặc định và tải lại.\n'
        '• Đang ở chế độ Xem chi tiết → sau khi tải xong tự mở lại toàn bộ các cấp.',
    dacbiet='Cuộc họp được tính theo khoảng thời gian dựa trên ngày bắt đầu của cuộc họp.')
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
    ('Công ty', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Biểu tượng 🔒 cạnh nhãn: bật để chọn cả đơn vị đã khoá.'),
    ('Phòng ban', 'Dropdown', 'Enable', 'Danh sách theo công ty', 'Không', 'Trống', 'Có 🔒 như trên.'),
    ('Bộ phận', 'Dropdown', 'Enable', 'Danh sách theo phòng ban', 'Không', 'Trống', 'Có 🔒 như trên.'),
    ('Nhân viên', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Lọc cuộc họp có nhân viên này tham gia.'),
    ('Khách hàng', 'Textbox', 'Enable', '≥ 2 ký tự', 'Không', 'Trống',
     'Gõ để hiện gợi ý (tên; mã • số điện thoại); “Đang tìm...”, “Không tìm thấy khách hàng”. Xoá trắng ô thì '
     'bỏ chọn khách hàng và dự án.'),
    ('Dự án', 'Dropdown', 'Enable', 'Danh sách dự án TKT', 'Không', 'Trống',
     'Đã chọn khách hàng thì chỉ liệt kê dự án của khách hàng đó.'),
    ('Loại Meeting', 'Dropdown', 'Enable', 'Danh mục loại meeting', 'Không', 'Trống', 'Có ⓘ mô tả từng loại.'),
    ('Hình thức Meeting', 'Dropdown', 'Enable', 'Trực tiếp / Online', 'Không', 'Trống', '–'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải lại theo bộ lọc.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Trả bộ lọc về mặc định rồi tải lại.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Tìm kiếm nâng cao',
     'Mở / thu gọn khối bộ lọc.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở khối bộ lọc; nút đổi thành “Ẩn tìm kiếm nâng cao”.'),
    ('Đổi giá trị ô chọn (thời gian, tổ chức, dự án, loại, hình thức)', 'Change',
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
          '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 8 trường lọc kèm ô tích.\n'
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
    ('Danh sách trường lọc', 'Checkbox', 'Enable', '8 trường', 'Không', 'Theo cấu hình đã lưu',
     'Xem theo thời gian, Tháng, Năm, Công ty – Phòng ban – Bộ phận, Khách hàng, Dự án, Loại Meeting, Hình thức '
     'Meeting; mỗi dòng có số thứ tự và tay kéo ⠿.'),
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
d.h3('2.4 Xem biểu đồ Top phòng ban và Top nhân viên')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của biểu đồ tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Xem biểu đồ Top phòng ban và Top nhân viên',
    mota='Biểu đồ cột 2 trục: Số meeting và Tổng phút của 5 phòng ban dẫn đầu; bảng bên phải là 5 nhân viên '
         'dẫn đầu. Luôn tính theo bộ lọc đang áp dụng.',
    tacnhan=ACT + '; Người dùng đã đăng nhập',
    dieukien='Bộ lọc thời gian hợp lệ.',
    chinh='1. Hệ thống tải biểu đồ cùng lúc với bảng (mở màn, tìm kiếm, làm mới).\n'
          '2. Biểu đồ hiển thị tối đa 5 phòng ban, bảng Top nhân viên tối đa 5 người.\n'
          '3. Người dùng đổi “Sắp theo” → hệ thống tải lại và sắp xếp theo tiêu chí mới.',
    phu='• Không có dữ liệu → bảng Top nhân viên hiện “Không có dữ liệu.”, biểu đồ trống.\n'
        '• Lỗi tải → “Lỗi khi tải dữ liệu biểu đồ”.\n'
        '• Bộ lọc thời gian chưa hợp lệ → ô Sắp theo bị khoá.')
d.p('2.4.2 Layout màn hình')
layout('', '04-bieu-do.png', 'Biểu đồ Top phòng ban và bảng Top nhân viên')
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề', 'Label', 'Hiển thị', '–', 'Biểu đồ Top phòng ban',
     'Kèm ⓘ: “Biểu đồ luôn lấy theo dữ liệu đã lọc. Bảng bên phải là Top nhân viên (theo dữ liệu lọc).”'),
    ('Sắp theo', 'Dropdown', 'Enable / Disable', 'Số meeting / Tổng phút', 'Số meeting',
     'Khoá khi bộ lọc thời gian chưa đủ.'),
    ('Chú giải', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Số meeting (xanh lá), Tổng phút (xanh dương), “• Tổng: n meeting • n phút”.'),
    ('Biểu đồ cột', 'Chart', 'Read-only', 'Tối đa 5 phòng ban', 'Theo bộ lọc',
     'Trục trái: Meeting; trục phải: Phút; rê chuột hiện số liệu của phòng.'),
    ('Bảng Top nhân viên', 'Table/Grid', 'Read-only', 'Tối đa 5 dòng', 'Theo bộ lọc',
     'Cột #, Nhân viên (Top 5), Meeting, Phút; góc phải tiêu đề “n nhân viên”.'),
    ('Ghi chú cuối bảng', 'Label', 'Hiển thị', '–', 'Hiển thị', '“Dữ liệu luôn thay đổi theo bộ lọc báo cáo.”'),
], required=False)
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn / Tìm kiếm / Làm mới', 'System',
     'After:\n– Tải số liệu biểu đồ theo bộ lọc; mỗi cuộc họp chỉ cộng 1 lần cho 1 phòng dù phòng có nhiều '
     'người tham gia; cuộc họp Hủy tính 0 phút.\n– Lỗi → “Lỗi khi tải dữ liệu biểu đồ”.'),
    ('Đổi Sắp theo', 'Change',
     'After:\n– Tải lại, sắp giảm dần theo tiêu chí đã chọn (bằng nhau thì xét tiêu chí còn lại, rồi theo tên).'),
    ('Rê chuột lên cột', 'Hover', 'After:\n– Hiện Số meeting và Tổng phút của phòng ban.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Xem chi tiết phân cấp')
d.p('2.5.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='detail')
d.intro_table(
    ten='Xem chi tiết phân cấp',
    mota='Mở toàn bộ các cấp Công ty → Phòng ban → Nhân viên → Meeting trong 1 lần bấm, hoặc thu về chỉ cấp gốc.',
    tacnhan=ACT + '; Người dùng đã đăng nhập',
    dieukien='Bảng đang có dữ liệu.',
    chinh='1. Người dùng bấm “Xem chi tiết”.\n'
          '2. Hệ thống mở toàn bộ các cấp; nút đổi thành “Chỉ xem cấp gốc”.\n'
          '3. Người dùng bấm “Chỉ xem cấp gốc” → bảng thu về chỉ dòng Công ty.',
    phu='• Đang ở chế độ Xem chi tiết mà tìm kiếm lại → bảng tự mở lại toàn bộ các cấp sau khi tải.\n'
        '• Mỗi trang chứa tối đa số meeting bằng Số dòng/trang; meeting của 1 nhân viên có thể nối sang trang sau.')
d.p('2.5.2 Layout màn hình')
layout(' => Xem chi tiết', '05-xem-chi-tiet.png', 'Bảng chi tiết ở chế độ Xem chi tiết')
d.p('2.5.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xem chi tiết / Chỉ xem cấp gốc', 'Button', 'Enable', '–', 'Xem chi tiết',
     'Nút nền xanh khi đang thu gọn; nút viền khi đang mở hết.'),
    ('Dòng Công ty', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Nền xanh nhạt, số liệu tổng của công ty.'),
    ('Dòng Phòng ban', 'Table/Grid', 'Read-only', '–', 'Ẩn tới khi mở', 'Số liệu tổng của phòng.'),
    ('Dòng Nhân viên', 'Table/Grid', 'Read-only', '–', 'Ẩn tới khi mở',
     'Tên, Chức vụ, Mã nhân viên, tổng phút, chip loại / hình thức / người tham gia.'),
    ('Dòng Meeting', 'Table/Grid', 'Read-only', '–', 'Ẩn tới khi mở',
     'Mã — Tên, người tạo, ngày tạo, thời gian, thời lượng, loại, hình thức, số người, dự án, khách hàng, biên '
     'bản, nội dung, kết luận; cuộc họp hủy có nhãn “Hủy” và 0 phút.'),
], required=False)
d.p('2.5.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xem chi tiết', 'Click', 'After:\n– Mở toàn bộ công ty, phòng ban, nhân viên của trang đang xem.'),
    ('Bấm Chỉ xem cấp gốc', 'Click', 'After:\n– Đóng toàn bộ, chỉ còn dòng Công ty.'),
])


def drill(so, fr, ten, tail, png, caption, modal, mota, chinh, phu, ui, ev):
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


MEET_COLS = ('Mã, Tên meeting, Ngày (dd/mm/yyyy), Phút, Loại, Hình thức, Dự án, Khách hàng')
POPUP_COMMON = [
    ('Nút Xuất Excel (trong cửa sổ)', 'Button', 'Enable', '–', 'Hiển thị',
     'Tải file Excel danh sách đang hiển thị (xếp theo ngày tăng dần, có cột STT).'),
    ('Nút Đóng / ×', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
    ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu...”.'),
]
SCOPE_TXT = ('Bấm ở dòng Công ty / Phòng ban / Nhân viên → danh sách giới hạn trong công ty / phòng ban / '
             'nhân viên đó, cộng với bộ lọc đang áp dụng.')

drill(6, 'FR-06', 'Xem danh sách meeting theo loại', ' => Xem chi tiết => Loại meeting', '06-theo-loai.png',
      'Cửa sổ danh sách meeting theo loại', '“Loại: <tên loại>”',
      'Bấm chip loại meeting (vd “Meeting với khách hàng: 4”) để xem đúng danh sách cuộc họp đã đếm vào chip.',
      '1. Người dùng bấm chip loại meeting ở dòng Công ty, Phòng ban hoặc Nhân viên.\n'
      '2. Hệ thống mở cửa sổ “Loại: <tên loại>”, dòng phụ “<Công ty/Phòng/Nhân viên>: <tên> • n meeting”.\n'
      '3. Hệ thống tải danh sách cuộc họp thuộc loại đó.',
      '• Không có cuộc họp → “Không có meeting.”.\n• Lỗi tải → “Lỗi khi tải danh sách meeting”.\n• ' + SCOPE_TXT,
      [('Tiêu đề + dòng phụ', 'Label', 'Hiển thị', '–', 'Theo chip đã bấm', 'Có biểu tượng tròn bên trái.'),
       ('Bảng meeting', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Cột: ' + MEET_COLS + '.'),
       ('Ghi chú', 'Label', 'Hiển thị', '–', 'Hiển thị',
        '“Popup hiển thị đúng danh sách meeting theo tiêu chí bạn click.”')] + POPUP_COMMON,
      [('Bấm chip loại meeting', 'Click',
        'After:\n– Mở cửa sổ, tải cuộc họp đúng loại trong phạm vi dòng đã bấm + bộ lọc hiện tại.\n'
        '– Lỗi → “Lỗi khi tải danh sách meeting”.'),
       ('Bấm Xuất Excel trong cửa sổ', 'Click',
        'After:\n– Tải file “Danh sách meeting theo loại <tên loại>.xlsx” (cột STT, Mã, Tên meeting, Ngày, Phút, '
        'Loại, Hình thức, Dự án, Khách hàng).'),
       ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng cửa sổ.')])

drill(7, 'FR-07', 'Xem danh sách meeting theo hình thức', ' => Xem chi tiết => Hình thức', '07-theo-hinh-thuc.png',
      'Cửa sổ danh sách meeting theo hình thức', '“Hình thức: Trực tiếp / Online”',
      'Bấm chip “Trực tiếp: n” hoặc “Online: n” để xem đúng các cuộc họp đã đếm vào chip.',
      '1. Người dùng bấm chip hình thức ở dòng Công ty, Phòng ban hoặc Nhân viên.\n'
      '2. Hệ thống mở cửa sổ “Hình thức: Trực tiếp” (hoặc Online) kèm dòng phụ phạm vi.\n'
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

drill(8, 'FR-08', 'Xem danh sách người tham gia', ' => Xem chi tiết => Số người tham gia',
      '08-nguoi-tham-gia.png', 'Cửa sổ danh sách người tham gia — tab Phía công ty', '“Danh sách người tham gia”',
      'Bấm chip “Tổng: n” ở cột Số người tham gia để xem người tham gia, tách 2 tab Phía công ty / Phía KH.',
      '1. Người dùng bấm chip “Tổng: n” ở dòng Công ty, Phòng ban, Nhân viên hoặc Meeting.\n'
      '2. Hệ thống mở cửa sổ “Danh sách người tham gia”, dòng phụ “<phạm vi> • n người”.\n'
      '3. Hệ thống tải người tham gia, mặc định mở tab Phía công ty (không có người phía công ty → mở Phía KH).',
      '• Tab không có người → nút tab bị khoá.\n• Không có dữ liệu → “Không có dữ liệu.”.\n'
      '• Lỗi tải → “Lỗi khi tải danh sách người tham gia”.\n'
      '• Xuất Excel lỗi → “Lỗi khi xuất Excel, đã xuất CSV thay thế” và tải file CSV.',
      [('Tab Phía công ty (n) / Phía KH (n)', 'Tab', 'Enable / Disable', '–', 'Phía công ty',
        'Số trong ngoặc là số người của tab.'),
       ('Bảng người tham gia', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Cột STT, Họ tên, Chức vụ, SĐT; tab Phía công ty mở từ dòng Công ty/Phòng/Nhân viên có thêm cột “Số lần '
        'tham gia meeting”. Mỗi nhân viên chỉ 1 dòng.'),
       ('Ghi chú', 'Label', 'Hiển thị', '–', 'Hiển thị',
        '“Cột "Số người tham gia" trên bảng chỉ là tổng. Click vào để xem chi tiết theo phía Công ty / phía KH.”')]
      + POPUP_COMMON,
      [('Bấm chip Tổng ở cột Số người tham gia', 'Click',
        'After:\n– Mở cửa sổ, tải người tham gia của các cuộc họp trong phạm vi dòng đã bấm + bộ lọc hiện tại.\n'
        '– Lỗi → “Lỗi khi tải danh sách người tham gia”.'),
       ('Bấm tab Phía công ty / Phía KH', 'Click', 'After:\n– Đổi danh sách hiển thị.'),
       ('Bấm Xuất Excel trong cửa sổ', 'Click',
        'After:\n– Tải file “Danh Sách Người Tham Gia.xlsx”: phía công ty trước, phía khách hàng sau, cột “Nội bộ / '
        'Khách hàng” ghi “Công ty” hoặc “Khách hàng”.'),
       ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng cửa sổ.')])

drill(9, 'FR-09', 'Xem biên bản cuộc họp', ' => Xem chi tiết => Xem', '09-bien-ban.png',
      'Cửa sổ Xem biên bản cuộc họp', '“Xem biên bản cuộc họp”',
      'Xem bản biên bản cuộc họp (mẫu in của cuộc họp) và in biên bản.',
      '1. Người dùng mở chi tiết tới dòng Meeting có biên bản, bấm chip “Xem” ở cột Biên bản.\n'
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
    mota='Tải file Excel toàn bộ báo cáo theo bộ lọc đang áp dụng (không phân trang), giữ cấu trúc phân cấp.',
    tacnhan=ACT + '; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “Xuất Excel” trên bảng chi tiết.\n'
          '2. Hệ thống lấy toàn bộ dữ liệu theo bộ lọc và phạm vi quyền.\n'
          '3. Trình duyệt tải file “bao_cao_meeting_theo_nhan_vien.xls”.',
    phu='• Đang xuất → nút hiện “Đang xuất...” và bị khoá.\n• Lỗi → “Lỗi khi xuất Excel”.',
    dacbiet='File gồm: ảnh tiêu đề (letterhead) của công ty đang làm việc, tiêu đề “BÁO CÁO THEO DÕI MEETING '
            'THEO NHÂN VIÊN”, 10 cột STT, Đối tượng, Thời gian, Thời lượng (phút), Loại, Hình thức, Số người tham '
            'gia, Dự án, Khách hàng, Biên bản; dòng Công ty / Phòng / Nhân viên tô màu theo cấp. Cột Biên bản ghi nội '
            'dung các mục biên bản hoặc “Chưa lập biên bản”.')
d.p('2.10.3 Layout màn hình')
layout(' => Xuất Excel', '10-xuat-excel.png', 'Nút Xuất Excel trên bảng chi tiết')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Biểu tượng file Excel; khi đang xuất đổi thành biểu tượng xoay + “Đang xuất...”.'),
    ('File tải về', 'File', 'Read-only', '.xls', '–', '–', 'Tên file: bao_cao_meeting_theo_nhan_vien.xls.'),
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
d.rule_ref('- Quy tắc Excel và Cấu hình cột (áp cho chọn cột in). Chỉ bổ sung các quy tắc riêng tại phần mô tả '
           'chi tiết.', anchor='excel')
d.intro_table(
    ten='In báo cáo',
    mota='Chọn cột cần in trong cửa sổ “Cấu hình in báo cáo”, xem bản in phân cấp ở thẻ mới rồi in khổ A4 ngang.',
    tacnhan=ACT + '; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “In danh sách”.\n'
          '2. Hệ thống mở cửa sổ “Cấu hình in báo cáo”, mặc định tích đủ 10 cột.\n'
          '3. Người dùng bỏ tích cột không cần, bấm “Xem trước”.\n'
          '4. Hệ thống mở bản in ở thẻ mới theo bộ lọc hiện tại.\n'
          '5. Người dùng bấm “In” trên bản in → hộp thoại in của trình duyệt.',
    phu='• Không tích cột nào mà bấm Xem trước → “Vui lòng chọn ít nhất 1 cột để in”.\n'
        '• Bấm “Hủy” → đóng cửa sổ.\n'
        '• Lỗi tải dữ liệu bản in → hiện khung báo lỗi đỏ trên bản in.',
    dacbiet='Cột STT và Công ty / Phòng / Nhân viên / Meeting luôn được in. Bản in có ảnh tiêu đề công ty đang '
            'làm việc, tiêu đề “BÁO CÁO THEO DÕI MEETING THEO NHÂN VIÊN”, STT phân cấp (1, 1.1, 1.1.1, 1.1.1.1) và '
            'khối ký “Ngày ...., tháng ...., năm .... / Người lập / (Ký, họ tên)”.')
d.p('2.11.3 Layout màn hình')
d.p('Đường dẫn màn hình:')
d._menu_para(MENU_A + ' => In danh sách => Xem trước')
menu_b(MENU_B + ' => In danh sách => Xem trước')
d.p('Hai lối vào mở CÙNG một báo cáo, dữ liệu như nhau. Cửa sổ Cấu hình in báo cáo được mở ngay trên màn hình '
    'báo cáo; bản in mở ở thẻ mới của trình duyệt.')
d.figure(shot('11-cau-hinh-in.png'), 'Cửa sổ Cấu hình in báo cáo', width_in=6.2)
d.figure(shot('11b-ban-in.png'), 'Bản in báo cáo mở ở thẻ mới', width_in=6.2)
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cấu hình in báo cáo', '–'),
    ('Chọn tất cả', 'Checkbox', 'Enable', '–', 'Không', 'Đã tích', 'Tích/bỏ tích toàn bộ cột.'),
    ('Chọn cột hiển thị', 'Checkbox', 'Enable', '10 cột', 'Có (≥ 1 cột)', 'Tích đủ',
     'Thời gian, Thời lượng, Loại meeting, Hình thức, Số người tham gia, Dự án, Khách hàng, Biên bản, Nội dung '
     'meeting, Kết luận cuộc họp.'),
    ('Ghi chú cột cố định', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Cột STT và Công ty / Phòng / Nhân viên / Meeting luôn được in.”'),
    ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '“Vui lòng chọn ít nhất 1 cột để in”.'),
    ('Nút Xem trước', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở bản in ở thẻ mới.'),
    ('Nút Hủy / ×', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ.'),
    ('Nút In (trên bản in)', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Bật hộp thoại in, khổ A4 ngang, lề 12mm × 10mm; nút không xuất hiện trên giấy.'),
    ('Bảng bản in', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
     'Cột STT, Đối tượng + các cột đã chọn; dòng Công ty/Phòng/Nhân viên in đậm, tô màu theo cấp; dòng meeting '
     'thụt lề; không có dữ liệu → “Không có dữ liệu”.'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In danh sách', 'Click', 'After:\n– Mở cửa sổ Cấu hình in báo cáo, tích sẵn đủ 10 cột.'),
    ('Bấm Chọn tất cả', 'Change', 'After:\n– Tích hoặc bỏ tích toàn bộ cột.'),
    ('Bấm Xem trước', 'Click',
     'During:\n– Không có cột nào được tích → “Vui lòng chọn ít nhất 1 cột để in”, dừng.\n'
     'After:\n– Đóng cửa sổ; mở bản in ở thẻ mới với bộ lọc hiện tại + danh sách cột đã chọn.\n'
     '– Bản in tải toàn bộ dữ liệu (không phân trang) theo phạm vi quyền.'),
    ('Bấm In trên bản in', 'Click', 'After:\n– Bật hộp thoại in của trình duyệt.'),
    ('Bấm Hủy / ×', 'Click', 'After:\n– Đóng cửa sổ, không in.'),
])

# ==================================================== PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của báo cáo Meeting theo nhân viên; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Cuộc họp được tính vào báo cáo', [
        '– Đã tới giờ bắt đầu: chỉ tính cuộc họp Hoàn thành hoặc Hủy.',
        '– Chưa tới giờ bắt đầu: chỉ tính cuộc họp Chốt lịch.',
        '– Cuộc họp thiếu giờ bắt đầu: coi như đã diễn ra (Hoàn thành / Hủy).',
        '– Cuộc họp Lưu nháp, Lên lịch không bao giờ được tính.',
        '– Chỉ tính cuộc họp có ít nhất 1 thành viên phía công ty trong phạm vi quyền.',
    ], ['Xem báo cáo', 'Biểu đồ', 'Xuất Excel', 'In']),
    ('BR-02', 'Thời lượng và cuộc họp Hủy', [
        '– Thời lượng = số phút từ giờ bắt đầu tới giờ kết thúc.',
        '– Cuộc họp Hủy vẫn đếm vào số meeting (và có chỉ số “Hủy: n”) nhưng tính 0 phút.',
    ], ['Xem báo cáo', 'Biểu đồ']),
    ('BR-03', 'Gom nhóm theo nhân viên', [
        '– Mỗi thành viên phía công ty của cuộc họp tạo 1 dòng nhân viên, xếp theo công ty và phòng ban hiện tại '
        'của nhân viên đó; 1 cuộc họp có nhiều nhân viên sẽ xuất hiện dưới mỗi nhân viên.',
        '– Số meeting cấp Phòng ban / Công ty đếm mỗi cuộc họp 1 lần (không nhân theo số người).',
        '– Lọc theo Công ty / Phòng ban / Bộ phận / Nhân viên thì chỉ hiện nhân viên khớp bộ lọc.',
    ], ['Xem báo cáo', 'Xem chi tiết phân cấp']),
    ('BR-04', 'Phạm vi dữ liệu theo quyền', [
        '– V1: mọi nhân viên; V2: nhân viên thuộc công ty đang làm việc; V3: nhân viên thuộc phòng ban / bộ phận '
        'người dùng quản lý; không có quyền: chỉ bản thân.',
        '– Phạm vi áp cho bảng, biểu đồ, cửa sổ chi tiết, file Excel và bản in.',
    ], 'Toàn màn hình'),
    ('BR-05', 'Top phòng ban / nhân viên', [
        '– Lấy 5 phòng ban và 5 nhân viên đứng đầu theo tiêu chí Sắp theo (Số meeting hoặc Tổng phút).',
    ], 'Biểu đồ'),
    ('BR-06', 'Khoảng thời gian bắt buộc', [
        '– Phải chọn đủ thông tin thời gian theo kiểu xem (Tháng + Năm / Năm / Từ ngày – Đến ngày) mới tải được '
        'báo cáo. Cuộc họp được lọc theo ngày bắt đầu.',
    ], 'Tìm kiếm và lọc'),
    ('BR-07', 'Dự án và khách hàng của cuộc họp', [
        '– Dự án = dự án tiền khả thi đầu tiên gắn với cuộc họp; khách hàng = khách hàng của dự án đó.',
    ], ['Xem báo cáo', 'Xuất Excel', 'In']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

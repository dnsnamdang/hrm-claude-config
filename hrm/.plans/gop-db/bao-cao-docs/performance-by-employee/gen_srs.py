# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo Hiệu suất làm việc theo dự án.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/report/performance-by-employee/{index.vue, print.vue, components/PerformanceByEmployeeTable.vue}
      components/V2BaseSmartFilterPanel.vue · components/modal/filter-customization-modal.vue
      components/V2BaseCompanyDepartmentFilter.vue · components/menu-sidebar.js (nhóm Báo cáo)
  BE  Modules/Assign/Routes/api.php (assign/reports/performance-by-employee, /export)
      Http/Controllers/Api/V1/PerformanceByEmployeeController (buildReportData, applyPermissionFilter)
      app/ExcelExport/PerformanceByEmployeeReportExport · resources/views/exports/performance_by_employee_report
  Quyền: PermissionsTableSeeder id 1066-1068 nhóm "Báo cáo hiệu suất NV theo dự án"
Ảnh chụp thật: shots/ (shoot.py, client :3002 → API :8003, dữ liệu mẫu xem data_created.md).
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = '/Users/manhcuong/Desktop/dns/HRM'
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402


def shot(name):
    return os.path.join(HERE, 'shots', name)


TEN_MAN = 'Báo cáo Hiệu suất làm việc theo dự án'
MENU = 'Phân hệ Công việc => Báo cáo => Hiệu suất làm việc theo dự án'
ACTOR = 'Người xem báo cáo'

d = SrsDoc(out=os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN), menu=MENU, route='', full_url='',
           img_prefix='hsda_')
d.set_menu_icons({k: shot(v) for k, v in {
    'Phân hệ Công việc': 'icon_phanhe.png',
    'Báo cáo': 'icon_baocao.png',
    'Hiệu suất làm việc theo dự án': 'icon_menu.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Xem chi tiết': 'icon_xemchitiet.png',
    'Xem tổng quan': 'icon_tongquan.png',
    'Số nhiệm vụ': 'icon_chip.png',
    'Xuất Excel': 'icon_xuatexcel.png',
    'In báo cáo': 'icon_in.png',
}.items()})
d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Báo cáo hiệu suất làm việc theo dự án, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phạm vi dữ liệu của báo cáo.',
    'Làm rõ cách hệ thống đếm nhiệm vụ hoàn thành đúng hạn / trễ hạn / không hoàn thành và cách tính tỷ lệ '
    'hoàn thành, hiệu suất theo giờ của từng nhân viên trên từng dự án.',
    'Làm rõ ý nghĩa bộ lọc thời gian (theo ngày bắt đầu của dự án) và phạm vi dữ liệu theo quyền xem.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Dự án', 'Dự án tiềm năng (dự án TKT) mà nhiệm vụ được gắn vào. Báo cáo nhóm nhiệm vụ theo dự án.'),
    ('Nhiệm vụ', 'Công việc được giao cho 1 nhân viên (người thực hiện), có hạn hoàn thành và số giờ ước tính.'),
    ('Hạng mục', 'Hạng mục của giải pháp mà nhiệm vụ thuộc về (vd “Xây dựng danh mục thiết bị”).'),
    ('Giờ được giao', 'Tổng số giờ ước tính của các nhiệm vụ.'),
    ('Giờ thực tế', 'Tổng số giờ nhân viên đã báo cáo trong các lần cập nhật tiến độ nhiệm vụ.'),
    ('Hiệu suất (%)', 'Giờ thực tế / Giờ được giao × 100%.'),
    ('Tỷ lệ hoàn thành', 'Số nhiệm vụ đã hoàn thành (đúng hạn + trễ hạn) / Tổng số nhiệm vụ × 100%.'),
    ('Công ty đang làm việc', 'Công ty người dùng đang chọn ở góc trên bên phải màn hình.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('–', 'Không khai quyền riêng',
     'Mọi người dùng vào được phân hệ Công việc đều thấy menu “Hiệu suất làm việc theo dự án” và dùng được mọi '
     'chức năng của màn (xem, lọc, xem chi tiết nhiệm vụ, xuất Excel, in). Dữ liệu nhìn thấy do nhóm quyền '
     'phạm vi bên dưới quyết định.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem báo cáo hiệu suất NV theo tổng công ty',
     'Nhiệm vụ của nhân viên mọi công ty. Bộ lọc hiện ô Công ty.'),
    ('V2', 'Xem báo cáo hiệu suất NV theo công ty',
     'Nhiệm vụ của nhân viên thuộc công ty đang làm việc.'),
    ('V3', 'Xem báo cáo hiệu suất NV theo phòng ban',
     'Nhiệm vụ của nhân viên thuộc các phòng ban / bộ phận mà người dùng quản lý.'),
    ('–', 'Không có quyền nào ở trên', 'Chỉ nhiệm vụ được giao cho chính người dùng.'),
], widths=[0.8, 2.4, 2.8])
d.p('Có nhiều quyền cùng lúc thì áp dụng quyền rộng nhất theo thứ tự V1 → V2 → V3.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'V1', 'V2', 'V3', 'Không có quyền nào'], [
    ('FR-01 Xem báo cáo hiệu suất làm việc theo dự án', '✅', '✅', '✅', '✅ (chỉ nhiệm vụ của bản thân)'),
    ('FR-02 Tìm kiếm và lọc báo cáo', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅'),
    ('FR-04 Xem chi tiết nhiệm vụ', '✅', '✅', '✅', '✅'),
    ('FR-05 Xuất Excel', '✅', '✅', '✅', '✅'),
    ('FR-06 In báo cáo', '✅', '✅', '✅', '✅'),
], widths=[2.6, 0.6, 0.6, 0.6, 1.6])

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR, [0, 1, 2])],
    [('FR-01', 'Xem báo cáo hiệu suất theo dự án', 'view'),
     ('FR-05', 'Xuất Excel', 'io'),
     ('FR-06', 'In báo cáo', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Xem chi tiết nhiệm vụ', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1 Xem bao cao
d.h3('2.1 Xem báo cáo hiệu suất làm việc theo dự án')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Xem báo cáo hiệu suất làm việc theo dự án',
    mota='Bảng phân cấp Phòng ban → Nhân viên → Dự án: mỗi dòng dự án cho biết hạng mục, vai trò, số nhiệm vụ '
         'được giao, kết quả hoàn thành (đúng hạn / trễ hạn / không hoàn thành), tỷ lệ hoàn thành, số giờ được '
         'giao, số giờ thực tế và hiệu suất. Dòng phòng ban và dòng nhân viên là dòng tổng hợp.',
    tacnhan='%s; Người dùng đã đăng nhập' % ACTOR,
    dieukien='Người dùng vào được phân hệ Công việc.',
    chinh='1. Người dùng vào menu Hiệu suất làm việc theo dự án.\n'
          '2. Hệ thống nạp báo cáo với bộ lọc mặc định: Xem theo thời gian = Tháng, Tháng = tháng hiện tại, '
          'Năm = năm hiện tại, trong phạm vi dữ liệu theo quyền của người dùng.\n'
          '3. Hệ thống hiển thị dòng tổng hợp của từng phòng ban (đang thu gọn), sắp xếp theo tên phòng ban.\n'
          '4. Người dùng bấm dòng phòng ban để mở danh sách nhân viên; bấm dòng nhân viên để mở danh sách dự án.\n'
          '5. Người dùng bấm “Xem chi tiết” để mở toàn bộ; bấm “Xem tổng quan” để thu gọn toàn bộ.',
    phu='• Không có dữ liệu → bảng hiển thị “Không có dữ liệu phù hợp bộ lọc.”.\n'
        '• Không tải được báo cáo → “Lỗi tải báo cáo: <nội dung lỗi>”.\n'
        '• Nhân viên / phòng ban không còn dự án nào sau khi lọc thì không hiển thị.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-man-hinh.png'), shot_caption='Màn báo cáo lúc mới mở (các phòng ban đang thu gọn)')
d.p('Sau khi bấm “Xem chi tiết” (bảng mở đến dòng dự án):')
d._menu_para(MENU + ' => Xem chi tiết')
d.figure(shot('02-xem-chi-tiet.png'), 'Bảng đã mở đến dòng dự án — phần cột bên trái', width_in=6.2)
d.figure(shot('02b-xem-chi-tiet-phai.png'), 'Bảng đã mở đến dòng dự án — phần cột bên phải (kéo thanh cuộn ngang)',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Báo cáo hiệu suất nhân viên theo Dự án',
     'Kèm biểu tượng ⓘ, rê chuột: “Thống kê hiệu suất làm việc của nhân viên theo Phòng ban → Nhân viên → Dự án, '
     'dựa trên số lượng nhiệm vụ và số giờ giao – thực tế.”'),
    ('Khối Bộ lọc báo cáo hiệu suất nhân viên theo Dự án', 'Card', 'Hiển thị', '–', 'Thu gọn', 'Xem FR-02, FR-03.'),
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Danh sách theo Phòng ban → Nhân viên → Dự án', '–'),
    ('Nút Xem chi tiết / Xem tổng quan', 'Button', 'Enable', '–', 'Xem chi tiết',
     '“Xem chi tiết”: mở toàn bộ phòng ban và nhân viên. Khi đang mở toàn bộ, nút đổi thành “Xem tổng quan” để thu gọn.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-05.'),
    ('Nút In báo cáo', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-06.'),
    ('Thanh cuộn ngang trên và dưới bảng', 'Scrollbar', 'Enable', '–', 'Hiển thị',
     'Bảng rộng hơn màn hình; 2 thanh cuộn chạy đồng bộ. Tiêu đề cột giữ cố định khi cuộn dọc.'),
    ('Cột STT', 'Text / Icon Button', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng phòng ban, nhân viên: nút mũi tên mở/thu. Dòng dự án: số thứ tự tăng dần.'),
    ('Cột Phòng ban / Nhân viên / Dự án', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng phòng ban: “Phòng: <tên>” + dòng phụ “Công ty: <tên> • <n> NV • <m> nhiệm vụ”. Dòng nhân viên: '
     'họ tên + “<n> dự án • <m> nhiệm vụ”. Dòng dự án: tên dự án.'),
    ('Cột Hạng mục tham gia / Vai trò', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng dự án: các hạng mục nhân viên tham gia (ngăn cách bằng dấu phẩy, không có thì “—”) + “Vai trò: …”. '
     'Dòng tổng hợp: “Tổng quan phòng ban” / “Tổng quan nhân viên”.'),
    ('Cột Ngày bắt đầu', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
     'Ngày bắt đầu của dự án. Dòng tổng hợp hiển thị “—”.'),
    ('Nhóm cột Kết quả nhiệm vụ', 'Table/Grid', 'Read-only', '5 cột', 'Theo dữ liệu',
     'Số nhiệm vụ được giao · Hoàn thành đúng hạn · Hoàn thành trễ hạn · Không hoàn thành · Tỷ lệ hoàn thành.'),
    ('Số nhiệm vụ được giao', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Dòng dự án: ô số bấm được (xem FR-04). Dòng tổng hợp: tổng của các dòng con.'),
    ('Hoàn thành đúng hạn / trễ hạn / Không hoàn thành', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Chỉ dòng dự án có số (ô bấm được, màu xanh lá / cam / đỏ); dòng tổng hợp hiển thị “—”. Cách đếm: BR-02.'),
    ('Tỷ lệ hoàn thành', 'Text', 'Read-only', '0 – 100%', 'Theo dữ liệu',
     'Dòng dự án: “<đã hoàn thành>/<tổng> (<x>%)”, bấm được. Dòng tổng hợp: “TB: <x>%”.'),
    ('Nhóm cột Giờ làm việc & Hiệu suất', 'Table/Grid', 'Read-only', '3 cột', 'Theo dữ liệu',
     'Số giờ được giao · Số giờ thực tế · Hiệu suất (%). Dòng tổng hợp: tổng giờ của các dòng con; '
     'hiệu suất hiển thị “TB: <x>%”.'),
    ('Dòng trống', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
    ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu...”'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Xác định phạm vi dữ liệu theo quyền V1 / V2 / V3 (không có quyền nào → chỉ nhiệm vụ của bản thân).\n'
     'After:\n– Nạp danh mục dự án cho bộ lọc và nạp báo cáo theo bộ lọc mặc định (tháng hiện tại).\n'
     '– Mọi phòng ban ở trạng thái thu gọn.\n'
     '– Lỗi → “Lỗi tải báo cáo: <nội dung lỗi>”.'),
    ('Bấm dòng phòng ban / nút mũi tên', 'Click', 'After:\n– Mở hoặc thu danh sách nhân viên của phòng ban đó.'),
    ('Bấm dòng nhân viên / nút mũi tên', 'Click', 'After:\n– Mở hoặc thu danh sách dự án của nhân viên đó.'),
    ('Bấm Xem chi tiết', 'Click', 'After:\n– Mở toàn bộ phòng ban và nhân viên; nút đổi thành “Xem tổng quan”.'),
    ('Bấm Xem tổng quan', 'Click', 'After:\n– Thu gọn toàn bộ về dòng phòng ban; nút đổi lại “Xem chi tiết”.'),
    ('Nạp lại báo cáo (sau khi lọc)', 'System', 'After:\n– Bảng trở về trạng thái thu gọn toàn bộ.'),
])

# ------------------------------------------------------------------ 2.2 Loc
d.h3('2.2 Tìm kiếm và lọc báo cáo')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả '
           'chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc báo cáo',
    mota='Thu hẹp báo cáo theo kỳ thời gian (ngày bắt đầu dự án), công ty – phòng ban – bộ phận – nhân viên, dự án, '
         'khoảng hiệu suất, tỷ lệ hoàn thành và số nhiệm vụ của mỗi dòng dự án.',
    tacnhan='%s; Người dùng đã đăng nhập' % ACTOR,
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “Tìm kiếm nâng cao” để mở khối bộ lọc.\n'
          '2. Người dùng chọn kỳ thời gian và các điều kiện lọc.\n'
          '3. Với ô chọn: hệ thống nạp lại báo cáo ngay khi đổi giá trị. Với ô nhập số: người dùng nhấn Enter '
          'hoặc bấm “Tìm kiếm”.\n'
          '4. Hệ thống hiển thị báo cáo theo điều kiện lọc.',
    phu='• Bấm “Làm mới” → trả bộ lọc về mặc định (Tháng hiện tại / Năm hiện tại, bỏ các điều kiện khác) và nạp lại.\n'
        '• Đổi “Xem theo thời gian” → xoá giá trị của các ô thời gian không còn hiển thị.\n'
        '• Bấm “Ẩn tìm kiếm nâng cao” → thu gọn khối bộ lọc, điều kiện đang chọn vẫn giữ.',
    dacbiet='Kỳ thời gian lọc theo NGÀY BẮT ĐẦU CỦA DỰ ÁN, không theo ngày giao hay ngày hoàn thành nhiệm vụ.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('03-bo-loc.png'), shot_caption='Khối bộ lọc đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Tìm kiếm nâng cao',
     'Mở / thu khối bộ lọc.'),
    ('Xem theo thời gian', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Có', 'Tháng',
     'Tuỳ chỉnh / Tháng / Năm. Không xoá trắng được.'),
    ('Tháng', 'Dropdown', 'Enable / Ẩn', 'Tháng 1 – Tháng 12', 'Có khi xem theo Tháng', 'Tháng hiện tại',
     'Chỉ hiện khi Xem theo thời gian = Tháng.'),
    ('Năm', 'Dropdown', 'Enable / Ẩn', 'Năm hiện tại − 5 → năm hiện tại + 1', 'Có khi xem theo Tháng / Năm',
     'Năm hiện tại', 'Hiện khi Xem theo thời gian = Tháng hoặc Năm.'),
    ('Ngày bắt đầu', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy (khoảng ngày)', 'Không', 'Trống',
     'Chỉ hiện khi Xem theo thời gian = Tuỳ chỉnh; 1 ô chọn khoảng Từ ngày – Đến ngày.'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống', 'Chỉ hiện với quyền V1.'),
    ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Hiện với quyền V1 / V2 / V3; danh sách theo phạm vi quyền và theo Công ty đã chọn.'),
    ('Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Hiện với quyền V1 / V2 / V3; thu hẹp danh sách Nhân viên theo bộ phận.'),
    ('Nhân viên', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Hiện với quyền V1 / V2 / V3; hiển thị “Tên nhân viên - Mã phòng - Mã nhân viên”.'),
    ('Biểu tượng 🔒 cạnh Công ty / Phòng ban / Bộ phận', 'Icon Button', 'Enable', '–', '–', 'Tắt',
     'Bật để danh sách chọn gồm cả mục đã khoá.'),
    ('Dự án', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Hiển thị “<Mã dự án> – <Tên dự án>”.'),
    ('Khoảng hiệu suất (%)', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Không', 'Trống',
     '< 80% / 80% – 100% / > 100%.'),
    ('Tỷ lệ hoàn thành', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Không', 'Trống',
     '< 80% / 80% – 100% / = 100%.'),
    ('Số nhiệm vụ tối thiểu', 'Number', 'Enable', '≥ 0', 'Không', 'Trống', 'Áp cho từng dòng dự án.'),
    ('Số nhiệm vụ tối đa', 'Number', 'Enable', '≥ 0', 'Không', 'Trống', 'Áp cho từng dòng dự án.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Nạp lại báo cáo theo điều kiện đang chọn.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Trả bộ lọc về mặc định rồi nạp lại.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Đổi giá trị ô chọn (thời gian, dự án, khoảng hiệu suất, tỷ lệ hoàn thành)', 'Change',
     'After:\n– Nạp lại báo cáo ngay theo điều kiện mới.'),
    ('Đổi Xem theo thời gian', 'Change',
     'After:\n– Tuỳ chỉnh → xoá Tháng, Năm; hiện ô Ngày bắt đầu.\n'
     '– Tháng / Năm → xoá khoảng ngày; chọn Năm thì xoá thêm Tháng.\n– Nạp lại báo cáo.'),
    ('Nhập Số nhiệm vụ tối thiểu / tối đa', 'Keypress', 'After:\n– Nhấn Enter → nạp lại báo cáo.'),
    ('Bấm Tìm kiếm', 'Click',
     'After:\n– Tính khoảng ngày theo kỳ đã chọn (Tháng: ngày 1 → ngày cuối tháng; Năm: 01/01 → 31/12; '
     'Tuỳ chỉnh: khoảng ngày đã chọn).\n'
     '– Lọc các nhiệm vụ của dự án có ngày bắt đầu nằm trong khoảng, rồi áp các điều kiện còn lại (BR-04).\n'
     '– Lỗi → “Lỗi tải báo cáo: <nội dung lỗi>”.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Trả bộ lọc về mặc định và nạp lại báo cáo.'),
])

# ------------------------------------------------------------------ 2.3 Cai dat bo loc
d.h3('2.3 Cài đặt bộ lọc')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='excel')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Người dùng chọn trường lọc nào được hiển thị trong khối bộ lọc và sắp xếp thứ tự các trường. Cài đặt '
         'lưu riêng cho từng người dùng trên màn báo cáo này.',
    tacnhan='%s; Người dùng đã đăng nhập' % ACTOR,
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
          '2. Hệ thống mở popup liệt kê 9 trường lọc theo thứ tự đang dùng.\n'
          '3. Người dùng tích / bỏ tích trường muốn hiển thị, kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm “Lưu”.\n'
          '5. Hệ thống lưu cài đặt, đóng popup, báo “Cập nhật thành công” và vẽ lại khối bộ lọc.',
    phu='• Bấm “Khôi phục mặc định” → hiện lại đủ trường theo thứ tự gốc (chưa lưu, phải bấm Lưu).\n'
        '• Bấm “Đóng” / dấu × → đóng popup, không lưu.\n'
        '• Lưu lỗi → “Thao tác thất bại”.',
    dacbiet='Trường bị ẩn thì giá trị đang lọc của trường đó bị xoá, để báo cáo không bị lọc ngầm bởi trường '
            'người dùng không nhìn thấy.')
d.p('2.3.2 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', modal='Cài đặt bộ lọc', shot=shot('04-cai-dat-bo-loc.png'),
         shot_caption='Popup Cài đặt bộ lọc')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', 'Kèm biểu tượng bánh răng.'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
    ('Danh sách trường lọc', 'Checkbox', 'Enable', 'Danh sách 9 trường', 'Không', 'Theo cài đặt đã lưu',
     'Xem theo thời gian · Tháng · Năm · Công ty – Phòng ban – Bộ phận · Dự án · Khoảng hiệu suất (%) · '
     'Tỷ lệ hoàn thành · Số nhiệm vụ tối thiểu · Số nhiệm vụ tối đa. Mỗi dòng có số thứ tự và tay kéo ⠿.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khoá trong lúc đang lưu.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Hiện lại đủ trường theo thứ tự gốc.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng popup, không lưu.'),
])
d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở popup với cài đặt đã lưu của người dùng (chưa lưu thì hiện đủ trường).'),
    ('Kéo tay kéo ⠿', 'Change', 'After:\n– Đổi thứ tự trường trong popup (chưa lưu).'),
    ('Bấm Lưu', 'Click',
     'During:\n– Lưu cài đặt hiển thị và thứ tự trường cho người dùng hiện tại trên màn này.\n'
     'After:\n– Xoá giá trị lọc của các trường vừa bị ẩn.\n– Đóng popup, báo “Cập nhật thành công”.\n'
     '– Lỗi → “Thao tác thất bại”.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Hiện lại đủ 9 trường theo thứ tự gốc trong popup (chưa lưu).'),
    ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup, bỏ thay đổi chưa lưu.'),
])

# ------------------------------------------------------------------ 2.4 Chi tiet nhiem vu
d.h3('2.4 Xem chi tiết nhiệm vụ')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='detail')
d.intro_table(
    ten='Xem chi tiết nhiệm vụ',
    mota='Từ một dòng dự án, xem danh sách nhiệm vụ đứng sau từng con số của báo cáo.',
    tacnhan='%s; Người dùng đã đăng nhập' % ACTOR,
    dieukien='Báo cáo đang mở đến dòng dự án.',
    chinh='1. Người dùng bấm một ô số trên dòng dự án: Số nhiệm vụ được giao, Hoàn thành đúng hạn, Hoàn thành trễ hạn, '
          'Không hoàn thành hoặc Tỷ lệ hoàn thành.\n'
          '2. Hệ thống mở popup, tiêu đề là tên dự án, dòng phụ cho biết nhóm nhiệm vụ đang xem.\n'
          '3. Popup liệt kê nhiệm vụ của nhân viên đó trên dự án đó theo nhóm tương ứng, kèm tổng giờ ở cuối bảng.\n'
          '4. Người dùng bấm “Đóng” để quay lại báo cáo.',
    phu='• Không có nhiệm vụ thuộc nhóm đã chọn → “Không có nhiệm vụ phù hợp”.')
d.p('2.4.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Số nhiệm vụ', modal='chi tiết nhiệm vụ',
         shot=shot('05-chi-tiet-nhiem-vu.png'), shot_caption='Popup danh sách nhiệm vụ của 1 dòng dự án')
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Tên dự án', '–'),
    ('Dòng phụ đề', 'Label', 'Hiển thị', 'Danh sách 5 giá trị', 'Theo ô đã bấm',
     'Số nhiệm vụ → “Tất cả nhiệm vụ”; Đúng hạn → “Nhiệm vụ hoàn thành đúng hạn”; Trễ hạn → “Nhiệm vụ hoàn thành '
     'trễ hạn”; Không hoàn thành → “Nhiệm vụ không hoàn thành / quá hạn”; Tỷ lệ hoàn thành → “Nhiệm vụ đã hoàn '
     'thành (đúng/trễ hạn)”.'),
    ('Cột #', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Số thứ tự.'),
    ('Cột Mã nhiệm vụ', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Tên nhiệm vụ', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 10 giá trị', 'Theo dữ liệu',
     'Nháp · Chờ duyệt · Chờ bắt đầu · Đang thực hiện · Tạm dừng · Hoàn thành - Chờ duyệt · Từ chối · Hoàn thành · '
     'Huỷ · Từ chối triển khai.'),
    ('Cột Hạn hoàn thành', 'Text', 'Read-only', 'dd-mm-yyyy', 'Theo dữ liệu', 'Trống → “—”.'),
    ('Cột Ngày hoàn thành', 'Text', 'Read-only', 'dd-mm-yyyy', 'Theo dữ liệu', 'Chưa hoàn thành → “—”.'),
    ('Cột Giờ được giao / Giờ thực tế', 'Number', 'Read-only', '≥ 0, 1 chữ số thập phân', 'Theo dữ liệu', '–'),
    ('Dòng tổng cuối bảng', 'Text', 'Read-only', '–', 'Hiển thị khi có nhiệm vụ',
     '“<n> nhiệm vụ” + tổng Giờ được giao + tổng Giờ thực tế.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có nhiệm vụ phù hợp”.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng popup.'),
], required=False)
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm ô số trên dòng dự án', 'Click',
     'After:\n– Lọc danh sách nhiệm vụ đã có sẵn của dòng dự án theo nhóm (không gọi lại máy chủ):\n'
     '  · Số nhiệm vụ được giao: tất cả.\n'
     '  · Đúng hạn: đã hoàn thành và ngày hoàn thành ≤ hạn hoàn thành.\n'
     '  · Trễ hạn: đã hoàn thành và ngày hoàn thành > hạn hoàn thành.\n'
     '  · Không hoàn thành: chưa ở trạng thái Hoàn thành / Hoàn thành - Chờ duyệt.\n'
     '  · Tỷ lệ hoàn thành: đã hoàn thành (đúng hạn + trễ hạn).\n'
     '– Mở popup với tiêu đề = tên dự án.'),
    ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup, giữ nguyên trạng thái bảng báo cáo.'),
])

# ------------------------------------------------------------------ 2.5 Xuat Excel
d.h3('2.5 Xuất Excel')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Xuất Excel báo cáo hiệu suất theo dự án', 'io', actor=ACTOR)
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='excel')
d.intro_table(
    ten='Xuất Excel',
    mota='Tải về file Excel toàn bộ báo cáo (mở hết đến dòng dự án) theo bộ lọc đang chọn.',
    tacnhan='%s; Người dùng đã đăng nhập' % ACTOR,
    dieukien='Báo cáo trên màn đang có dữ liệu.',
    chinh='1. Người dùng bấm “Xuất Excel”.\n'
          '2. Hệ thống dựng file theo bộ lọc và phạm vi quyền của người dùng.\n'
          '3. Trình duyệt tải file “bao_cao_hieu_suat_nhan_vien_theo_du_an.xls”.\n'
          '4. Hệ thống báo “Xuất Excel thành công”.',
    phu='• Báo cáo đang trống → “Không có dữ liệu để xuất Excel”, không tải file.\n'
        '• Lỗi khi dựng file → “Lỗi khi xuất Excel”.',
    dacbiet='File gồm: ảnh tiêu đề (letterhead) của công ty đang làm việc, tiêu đề “BÁO CÁO HIỆU SUẤT LÀM VIỆC CỦA '
            'NHÂN VIÊN THEO DỰ ÁN”, bảng 12 cột như màn hình với STT phân cấp 1 / 1.1 / 1.1.1, cuối file là '
            '“Ngày ..., tháng ..., năm ...” – “Người lập”.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('06-xuat-excel.png'),
         shot_caption='Bấm Xuất Excel — thông báo xuất thành công')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xuất Excel', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thanh tiến trình chạy ở đầu trang trong lúc dựng file.'),
    ('File Excel – phần đầu', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Ảnh tiêu đề công ty đang làm việc (không có thì dùng ảnh mặc định) + tiêu đề báo cáo.'),
    ('File Excel – bảng', 'Table/Grid', 'Read-only', '12 cột', '–', 'Theo dữ liệu',
     'STT · Phòng ban / Nhân viên / Dự án · Hạng mục tham gia / Vai trò · Ngày bắt đầu (dd/mm/yyyy) · Số nhiệm vụ '
     'được giao · Hoàn thành đúng hạn · Hoàn thành trễ hạn · Không hoàn thành · Tỷ lệ hoàn thành · Số giờ được giao · '
     'Số giờ thực tế · Hiệu suất (%). Dòng phòng ban nền xanh nhạt, dòng nhân viên nền xám nhạt, chữ đậm.'),
    ('File Excel – định dạng số', 'Number', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Số nguyên có dấu phẩy ngăn cách hàng nghìn; giờ và % lấy 1 chữ số thập phân.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Xuất Excel thành công” / “Không có dữ liệu để xuất Excel” / “Lỗi khi xuất Excel”.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Báo cáo trên màn không có dòng nào → “Không có dữ liệu để xuất Excel” và dừng xử lý.\n'
     'During:\n– Gửi các điều kiện lọc đang chọn; máy chủ dựng lại dữ liệu theo phạm vi quyền (V1 / V2 / V3 / bản thân).\n'
     'After:\n– Tải file “bao_cao_hieu_suat_nhan_vien_theo_du_an.xls”, báo “Xuất Excel thành công”.\n'
     '– Lỗi → “Lỗi khi xuất Excel”.'),
])

# ------------------------------------------------------------------ 2.6 In
d.h3('2.6 In báo cáo')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'In báo cáo hiệu suất theo dự án', 'io', actor=ACTOR)
d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của bản in tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='In báo cáo',
    mota='Mở bản xem trước để in báo cáo (khổ A4 ngang) theo bộ lọc đang chọn, mở hết đến dòng dự án.',
    tacnhan='%s; Người dùng đã đăng nhập' % ACTOR,
    dieukien='Báo cáo trên màn đang có dữ liệu.',
    chinh='1. Người dùng bấm “In báo cáo”.\n'
          '2. Hệ thống mở bản xem trước ở tab mới, nạp lại dữ liệu theo bộ lọc.\n'
          '3. Người dùng bấm nút “In” để mở hộp thoại in của trình duyệt.',
    phu='• Báo cáo đang trống → “Không có dữ liệu để in báo cáo”, không mở tab.\n'
        '• Không tải được dữ liệu in → khung đỏ hiển thị nội dung lỗi hoặc “Lỗi không xác định khi tải dữ liệu '
        'báo cáo”.',
    dacbiet='Bản in: khổ A4 ngang, lề 8mm × 6mm; ảnh tiêu đề công ty đang làm việc; tiêu đề “BÁO CÁO HIỆU SUẤT LÀM '
            'VIỆC CỦA NHÂN VIÊN THEO DỰ ÁN”; cuối trang “Ngày ...., tháng ...., năm ....” – “Người lập” – '
            '“(Ký, họ tên)”.')
d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => In báo cáo', shot=shot('07-in.png'), shot_caption='Bản xem trước khi in')
d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Không xuất hiện trên bản in.'),
    ('Khung báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Khung đỏ, không xuất hiện trên bản in.'),
    ('Ảnh tiêu đề công ty', 'Label', 'Read-only', '–', '–', 'Theo công ty đang làm việc',
     'Không có thì dùng ảnh mặc định.'),
    ('Tiêu đề', 'Label', 'Read-only', '–', '–', 'BÁO CÁO HIỆU SUẤT LÀM VIỆC CỦA NHÂN VIÊN THEO DỰ ÁN', '–'),
    ('Bảng in', 'Table/Grid', 'Read-only', '12 cột', '–', 'Theo dữ liệu',
     'Cùng cột với màn hình. STT phân cấp: phòng ban “1”, nhân viên “1.1”, dự án “1.1.1”; tên lùi lề theo cấp. '
     'Dòng phòng ban nền xanh nhạt, dòng nhân viên nền xám nhạt.'),
    ('Ô kết quả của dòng tổng hợp', 'Text', 'Read-only', '–', '–', '—',
     'Đúng hạn / trễ hạn / không hoàn thành = “—”; Tỷ lệ hoàn thành và Hiệu suất = “TB: <x>%”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '“Không có dữ liệu”.'),
    ('Khối ký', 'Label', 'Read-only', '–', '–', 'Hiển thị',
     '“Ngày ...., tháng ...., năm ....” / “Người lập” / “(Ký, họ tên)”, căn phải.'),
])
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In báo cáo', 'Click',
     'Before:\n– Báo cáo trên màn không có dòng nào → “Không có dữ liệu để in báo cáo” và dừng xử lý.\n'
     'After:\n– Mở bản xem trước ở tab mới, mang theo các điều kiện lọc đang chọn.'),
    ('Mở bản xem trước', 'System',
     'After:\n– Nạp dữ liệu theo điều kiện lọc và phạm vi quyền; dựng bảng phân cấp.\n'
     '– Lỗi → khung đỏ hiển thị nội dung lỗi.'),
    ('Bấm In', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt với khổ A4 ngang, chỉ in vùng báo cáo.'),
])

# ==================================================== PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Báo cáo hiệu suất làm việc theo dự án; không lặp lại các quy '
           'tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Nguồn dữ liệu và cách nhóm', [
        '– Lấy mọi nhiệm vụ đã có người thực hiện; nhóm theo Phòng ban (của nhân viên thực hiện, kèm công ty) → '
        'Nhân viên thực hiện → Dự án của nhiệm vụ.',
        '– Phòng ban sắp xếp theo tên; nhân viên / phòng ban không còn dòng dự án nào sau khi lọc thì bị ẩn.',
    ], ['Xem báo cáo', 'Xuất Excel', 'In báo cáo']),
    ('BR-02', 'Đếm kết quả nhiệm vụ', [
        '– Đã hoàn thành = trạng thái “Hoàn thành” hoặc “Hoàn thành - Chờ duyệt”.',
        '– Đúng hạn: đã hoàn thành, có ngày hoàn thành và hạn hoàn thành, thời điểm hoàn thành không muộn hơn hạn '
        '(hạn chỉ có ngày, tính từ 00:00 của ngày hạn). Muộn hơn → Trễ hạn.',
        '– Không hoàn thành: chưa hoàn thành VÀ đã quá hạn hoàn thành tại thời điểm xem. Nhiệm vụ chưa hoàn thành '
        'nhưng chưa tới hạn chỉ được tính vào Số nhiệm vụ được giao.',
    ], ['Xem báo cáo', 'Xem chi tiết nhiệm vụ']),
    ('BR-03', 'Công thức tỷ lệ và hiệu suất', [
        '– Tỷ lệ hoàn thành = (Đúng hạn + Trễ hạn) / Số nhiệm vụ được giao × 100%, làm tròn 2 chữ số.',
        '– Số giờ được giao = tổng giờ ước tính của nhiệm vụ; Số giờ thực tế = tổng giờ đã báo cáo ở các lần cập '
        'nhật tiến độ.',
        '– Hiệu suất = Số giờ thực tế / Số giờ được giao × 100%; không có giờ được giao thì để trống.',
        '– Dòng phòng ban / nhân viên: cộng dồn số nhiệm vụ và giờ của các dòng con rồi tính lại tỷ lệ, hiệu suất '
        '(hiển thị “TB: …”).',
    ], ['Xem báo cáo', 'Xuất Excel', 'In báo cáo']),
    ('BR-04', 'Điều kiện lọc', [
        '– Kỳ thời gian lọc theo ngày bắt đầu của dự án: Tháng = ngày 1 → ngày cuối tháng; Năm = 01/01 → 31/12; '
        'Tuỳ chỉnh = khoảng ngày đã chọn.',
        '– Khoảng hiệu suất: < 80%; 80% – 100% (gồm 2 đầu); > 100%. Dòng dự án không có giờ được giao bị loại khi '
        'đang lọc khoảng hiệu suất.',
        '– Tỷ lệ hoàn thành: < 80%; từ 80% đến dưới 100%; = 100%.',
        '– Số nhiệm vụ tối thiểu / tối đa so với Số nhiệm vụ được giao của từng dòng dự án.',
    ], 'Tìm kiếm và lọc'),
    ('BR-05', 'Hạng mục tham gia và vai trò', [
        '– Hạng mục tham gia = các hạng mục giải pháp của những nhiệm vụ nhân viên làm trong dự án; không có → “—”.',
        '– Vai trò trên mỗi hạng mục: là leader hạng mục → “Leader hạng mục”; là PM của yêu cầu làm giải pháp → '
        '“PM làm giải pháp”; còn lại lấy vai trò trong phân công thành viên hạng mục; không có → “Thành viên”.',
    ], 'Xem báo cáo'),
    ('BR-06', 'Phạm vi dữ liệu theo quyền', [
        '– V1: mọi công ty; V2: công ty đang làm việc; V3: phòng ban / bộ phận người dùng quản lý; không có quyền '
        'nào: chỉ nhiệm vụ giao cho chính người dùng.',
        '– Áp dụng như nhau cho màn hình, file Excel và bản in.',
    ], ['Xem báo cáo', 'Xuất Excel', 'In báo cáo']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

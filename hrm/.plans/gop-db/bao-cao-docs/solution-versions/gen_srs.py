# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo Theo dõi chỉ số hoàn thành GP theo version.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/report/solution-versions/{index,print}.vue
      components/{SolutionVersionsTable,SolutionVersionDetailModal}.vue · components/reportUtils.js
      components/V2BaseSmartFilterPanel.vue · components/modal/filter-customization-modal.vue
      components/V2BaseCompanyDepartmentFilter.vue · components/menu-sidebar.js (menuItemsAssign › Báo cáo)
  BE  Modules/Assign/Routes/api.php (assign/report/solution-versions — KHÔNG gắn checkPermission)
      SolutionVersionsReportController · Services/Report/SolutionVersionsReportService
      app/ExcelExport/SolutionVersionsReportExport + resources/views/exports/solution_versions_report.blade.php
      Modules/Assign/Entities/Solution::STATUSES
  Quyền: PermissionsTableSeeder id 1077-1079 (nhóm "Báo cáo theo dõi version giải pháp")
Ảnh: shots/ (Playwright headless 1440x900, client :3002) — dữ liệu mẫu xem data_created.md.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isdir(os.path.join(ROOT, '.claude', 'skills', 'srs-documenter')):
    ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(HERE, 'shots')


def shot(name):
    return os.path.join(SHOTS, name)


TEN_MAN = 'Báo cáo Theo dõi chỉ số hoàn thành GP theo version'
MENU = 'Phân hệ Công việc => Báo cáo => Theo dõi chỉ số hoàn thành GP theo version'
A = 'Người xem báo cáo'

ICONS = {
    'Phân hệ Công việc': 'icon_phanhe.png',
    'Báo cáo': 'icon_baocao.png',
    'Theo dõi chỉ số hoàn thành GP theo version': 'icon_man.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Xem chi tiết': 'icon_xemchitiet.png',
    'Chỉ xem cấp gốc': 'icon_capgoc.png',
    'Số hạng mục': 'icon_hangmuc.png',
    'Số nhân sự tham gia': 'icon_nhansu.png',
    'Xuất Excel': 'icon_xuat.png',
    'In báo cáo': 'icon_in.png',
    'In': 'icon_nutin.png',
}

out = os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN)
d = SrsDoc(out=out, menu=MENU, route='', full_url='', img_prefix='svrep_')
d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})
d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

SCOPE_NOTE = ('– Dữ liệu chỉ gồm giải pháp nằm trong phạm vi quyền của người xem (V1 › V2 › V3 › mặc định '
              'chỉ giải pháp mình là PM) — xem quy tắc BR-01.')

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Báo cáo theo dõi chỉ số hoàn thành giải pháp theo version '
    '(phân hệ Công việc), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu các chức năng xem, lọc, xem chi tiết, xuất Excel và in của báo cáo.',
    'Làm rõ cách hệ thống gom số liệu theo cây Công ty → Phòng giải pháp → Giải pháp → Version và cách tính '
    'các chỉ số khối lượng, định mức, hiệu suất.',
    'Làm rõ phạm vi dữ liệu mỗi người dùng được xem theo quyền.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('GP', 'Giải pháp kỹ thuật lập cho một dự án tiền khả thi.'),
    ('Version', 'Một phiên bản (lần làm) của giải pháp; mỗi giải pháp có thể có nhiều version.'),
    ('PM', 'Người phụ trách giải pháp — trên báo cáo là người tạo giải pháp.'),
    ('Phòng giải pháp', 'Phòng ban được ghi trên giải pháp (phòng làm giải pháp).'),
    ('Hạng mục', 'Hạng mục công việc của giải pháp (vd Xây dựng danh mục thiết bị, Ốp bản vẽ móng máy).'),
    ('Số giờ được giao', 'Tổng giờ ước tính của các nhiệm vụ thuộc version.'),
    ('Số giờ thực tế', 'Tổng số giờ người thực hiện khai khi báo cáo tiến độ nhiệm vụ.'),
    ('Hiệu suất (%)', 'Số giờ được giao / Số giờ thực tế × 100.'),
    ('Cấp gốc', 'Chế độ chỉ hiện dòng tổng và dòng Công ty; các cấp dưới thu gọn.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('–', 'Không có quyền thao tác riêng',
     'Menu “Theo dõi chỉ số hoàn thành GP theo version” hiển thị cho mọi người dùng đã đăng nhập vào phân hệ '
     'Công việc. Mọi thao tác trên màn (xem, lọc, cài đặt bộ lọc, xem chi tiết, xuất Excel, in) không kiểm tra '
     'quyền riêng; số liệu được giới hạn theo nhóm quyền phạm vi dữ liệu bên dưới.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem báo cáo version giải pháp theo tổng công ty', 'Toàn bộ giải pháp của mọi công ty.'),
    ('V2', 'Xem báo cáo version giải pháp theo công ty',
     'Giải pháp thuộc công ty người dùng đang làm việc.'),
    ('V3', 'Xem báo cáo version giải pháp theo phòng ban',
     'Giải pháp của các phòng ban / bộ phận người dùng quản lý, cộng giải pháp do chính người dùng là PM.'),
    ('–', 'Không có quyền nào ở trên', 'Chỉ giải pháp do chính người dùng là PM.'),
], widths=[0.8, 2.4, 2.8])
d.p('Có nhiều quyền cùng lúc thì áp dụng quyền rộng nhất theo thứ tự V1 → V2 → V3.')

d.h2('2 Ma trận phân quyền')
FRS = [
    ('FR-01', 'Xem báo cáo theo dõi version giải pháp'),
    ('FR-02', 'Tìm kiếm và lọc báo cáo'),
    ('FR-03', 'Cài đặt bộ lọc'),
    ('FR-04', 'Xem chi tiết theo cấp (mở rộng / thu gọn)'),
    ('FR-05', 'Xem chi tiết số hạng mục'),
    ('FR-06', 'Xem chi tiết số nhân sự tham gia'),
    ('FR-07', 'Xuất Excel báo cáo'),
    ('FR-08', 'In báo cáo'),
]
d.table(['Chức năng', 'V1', 'V2', 'V3', 'Không có quyền nào'],
        [('%s %s' % fr, '✅', '✅', '✅', '✅ (chỉ giải pháp mình là PM)') for fr in FRS],
        widths=[2.6, 0.5, 0.5, 0.5, 1.9])
d.p('Mọi người dùng đều dùng được đủ 8 chức năng; khác nhau ở phạm vi giải pháp hiển thị (xem Danh sách quyền).')

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A, [0, 1, 2])],
    [('FR-01', 'Xem báo cáo version GP', 'view'),
     ('FR-07', 'Xuất Excel báo cáo', 'io'),
     ('FR-08', 'In báo cáo', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Xem chi tiết theo cấp', 'view', 'extend', [0], None),
     ('FR-05', 'Chi tiết số hạng mục', 'view', 'extend', [0], None),
     ('FR-06', 'Chi tiết số nhân sự', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem báo cáo theo dõi version giải pháp')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Phân trang và UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả '
           'chi tiết.', anchor='list')
d.intro_table(
    ten='Xem báo cáo theo dõi version giải pháp',
    mota='Hiển thị số liệu khối lượng, định mức và hiệu suất của từng version giải pháp, gom theo cây '
         'Công ty → Phòng giải pháp → Giải pháp → Version, kèm dòng tổng toàn bộ version.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và vào được phân hệ Công việc.',
    chinh='1. Người dùng vào menu Theo dõi chỉ số hoàn thành GP theo version.\n'
          '2. Hệ thống áp bộ lọc mặc định: Xem theo thời gian = Tháng, tháng và năm hiện tại.\n'
          '3. Hệ thống tải báo cáo trong phạm vi quyền, phân trang theo giải pháp (mặc định 15 giải pháp/trang).\n'
          '4. Màn hiển thị ở chế độ cấp gốc: dòng “Tổng toàn bộ version” và dòng của từng công ty.\n'
          '5. Người dùng đổi trang hoặc số dòng/trang; hệ thống tải lại trang tương ứng.',
    phu='• Không có version nào khớp bộ lọc → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”, dưới bảng hiện '
        '“Không có giải pháp nào.”.\n'
        '• Đang tải → bảng hiện “Đang tải dữ liệu...”.\n'
        '• Rê chuột vào biểu tượng ⓘ cạnh tiêu đề trang → hiện mô tả báo cáo.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-xem.png'),
         shot_caption='Báo cáo theo dõi version giải pháp lúc mới mở (chế độ cấp gốc)')
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Báo cáo theo dõi chỉ số hoàn thành giải pháp theo version',
     'Kèm biểu tượng ⓘ: “Báo cáo này theo dõi quá trình hoàn thiện giải pháp và lịch sử thay đổi của các giải '
     'pháp kỹ thuật thông qua các phiên bản.”'),
    ('Khối Bộ lọc theo dõi version giải pháp', 'Card', 'Hiển thị', '–', 'Thu gọn',
     'Gồm nút Cài đặt bộ lọc, nút Tìm kiếm nâng cao — xem FR-02, FR-03.'),
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–',
     'Báo cáo theo dõi chỉ số hoàn thành giải pháp theo version', '–'),
    ('Nút Xem chi tiết / Chỉ xem cấp gốc', 'Button', 'Enable', '–', 'Xem chi tiết', 'Xem FR-04.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-07.'),
    ('Nút In báo cáo', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-08.'),
    ('Thanh cuộn ngang', 'Scrollbar', 'Hiển thị', '–', 'Hiển thị',
     'Có ở cả phía trên và phía dưới bảng, cuộn đồng bộ.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng công ty / phòng / giải pháp hiện nút mũi tên mở rộng – thu gọn; dòng version hiện số thứ tự version '
     'trong giải pháp.'),
    ('Cột Công ty / Phòng / Giải pháp / Version', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Công ty: “Công ty: <tên>” + số version, hiệu suất. Phòng: “Phòng giải pháp: <tên>” + số giải pháp, số '
     'version, hiệu suất. Giải pháp: “Giải pháp: <tên> (<n> version)” + mã GP, khách hàng. Version: '
     '“Version <mã> – <số ngày> ngày” + ngày bắt đầu – ngày chốt – PM.'),
    ('Nhóm cột THÔNG TIN VERSION', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Trạng thái version (badge màu theo trạng thái) · Ngày bắt đầu làm · Ngày chốt (dd/mm/yyyy, chưa có hiện '
     '“—”) · Số ngày thực hiện.'),
    ('Nhóm cột KHỐI LƯỢNG & ĐỊNH MỨC', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Số hạng mục · Số nhân sự tham gia (2 cột này bấm được ở dòng giải pháp và version — xem FR-05, FR-06) · '
     'Số nhiệm vụ giao · Số giờ được giao · Số giờ thực tế (dạng “<n> giờ”).'),
    ('Nhóm cột HIỆU SUẤT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Hiệu suất (%) · Nhiệm vụ / giờ (chưa có giờ thực tế hiện “—”) · Đánh giá hiệu suất (badge: Hiệu suất cao / '
     'Hiệu suất trung bình / Hiệu suất thấp / Chưa có dữ liệu).'),
    ('Dòng Tổng toàn bộ version', 'Table/Grid', 'Read-only', '–', 'Hiển thị khi có dữ liệu',
     '“<n> giải pháp • <n> version • Thời gian TB: <n> ngày • Hiệu suất giờ: <n>%”; cột Số ngày thực hiện = thời '
     'gian trung bình.'),
    ('Dòng thông tin phân trang', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     '“Hiển thị <từ>–<đến> / <tổng> giải pháp”.'),
    ('Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', '15', '15 / 50 / 100 / 200 giải pháp.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Đầu, trước, số trang, sau, cuối.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
    ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu...”'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Không kiểm tra quyền thao tác (menu mở cho mọi người dùng).\n'
     'After:\n– Nạp danh sách Khách hàng, Giải pháp cho bộ lọc.\n'
     '– Tải báo cáo theo tháng hiện tại, trang 1, 15 giải pháp/trang.\n' + SCOPE_NOTE),
    ('Đổi trang', 'Click', 'After:\n– Tải lại báo cáo ở trang được chọn, giữ nguyên bộ lọc.'),
    ('Đổi Số dòng/trang', 'Change', 'After:\n– Về trang 1 và tải lại với số giải pháp/trang mới.'),
    ('Rê chuột biểu tượng ⓘ', 'Hover', 'After:\n– Hiện mô tả báo cáo.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc báo cáo')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô '
           'tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc báo cáo',
    mota='Lọc báo cáo theo kỳ thời gian (theo ngày bắt đầu làm của version), công ty, phòng ban, PM, khách '
         'hàng, giải pháp và version.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
          '2. Người dùng chọn giá trị ở các ô lọc.\n'
          '3. Mỗi lần chọn một ô, hệ thống tự áp bộ lọc, về trang 1 và tải lại báo cáo.\n'
          '4. Người dùng bấm “Ẩn tìm kiếm nâng cao” để thu gọn khối lọc.',
    phu='• Chọn Xem theo thời gian = Tháng → hiện ô Tháng và Năm; = Năm → chỉ hiện ô Năm; = Tuỳ chỉnh → hiện ô '
        'Thời gian làm giải pháp. Ô bị ẩn được xoá giá trị.\n'
        '• Chưa chọn Giải pháp → ô Version bị khoá, gợi ý “Chọn giải pháp trước”.\n'
        '• Đổi Giải pháp → nạp lại danh sách version của giải pháp đó, xoá version đang chọn.\n'
        '• Bấm “Làm mới” → đưa các ô lọc về mặc định và tải lại báo cáo.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao — kiểu xem theo Tháng')
d.figure(shot('02b-loc-tuy-chinh.png'), 'Khối Tìm kiếm nâng cao — kiểu xem Tuỳ chỉnh (khoảng ngày)',
         width_in=6.2)
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Xem theo thời gian', 'Dropdown', 'Enable', 'Tuỳ chỉnh / Tháng / Năm', 'Có', 'Tháng', 'Không xoá trắng được.'),
    ('Tháng', 'Dropdown', 'Enable / Ẩn', 'Tháng 1 – Tháng 12', 'Có khi xem theo Tháng', 'Tháng hiện tại',
     'Chỉ hiện khi Xem theo thời gian = Tháng.'),
    ('Năm', 'Dropdown', 'Enable / Ẩn', 'Năm hiện tại − 5 → năm hiện tại + 1', 'Có khi xem theo Tháng / Năm',
     'Năm hiện tại', 'Năm mới nhất ở trên.'),
    ('Thời gian làm giải pháp', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy, từ ngày → đến ngày', 'Không', 'Trống',
     'Chỉ hiện khi Xem theo thời gian = Tuỳ chỉnh; khoảng ngày gộp trong 1 ô.'),
    ('Công ty', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Biểu tượng ổ khoá cạnh nhãn: bấm để hiện cả công ty đã khoá.'),
    ('Phòng ban', 'Dropdown', 'Enable', 'Danh sách theo công ty', 'Không', 'Trống',
     'Lọc theo phòng giải pháp; có biểu tượng ổ khoá hiện cả phòng ban đã khoá.'),
    ('Nhân viên', 'Dropdown', 'Enable', 'Danh sách theo công ty / phòng ban', 'Không', 'Trống',
     'Lọc theo PM (người tạo giải pháp).'),
    ('Khách hàng', 'Dropdown', 'Enable', 'Khách hàng của các dự án có giải pháp', 'Không', 'Trống', '–'),
    ('Giải pháp', 'Dropdown', 'Enable', 'Danh sách “Mã - Tên” giải pháp', 'Không', 'Trống',
     'Đổi giá trị sẽ nạp lại danh sách Version.'),
    ('Version', 'Dropdown', 'Enable / Disable', 'Version của giải pháp đã chọn, dạng “V<mã>”', 'Không', 'Khoá',
     'Khoá với gợi ý “Chọn giải pháp trước” khi chưa chọn Giải pháp.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp bộ lọc, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đưa bộ lọc về mặc định.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Tìm kiếm nâng cao',
     'Mở / thu gọn khối lọc.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Click', 'After:\n– Mở hoặc thu gọn khối lọc.'),
    ('Chọn giá trị một ô lọc', 'Change',
     'After:\n– Áp bộ lọc ngay (không cần bấm Tìm kiếm), về trang 1 và tải lại báo cáo.\n'
     '– Kỳ Tháng: từ ngày 1 đến ngày cuối của tháng; kỳ Năm: 01/01 → 31/12; kỳ Tuỳ chỉnh: theo khoảng ngày nhập.\n'
     + SCOPE_NOTE),
    ('Đổi Xem theo thời gian', 'Change',
     'After:\n– Tuỳ chỉnh: xoá Tháng, Năm. Tháng / Năm: xoá khoảng ngày; Năm: xoá Tháng.\n'
     '– Hiện / ẩn các ô tương ứng rồi tải lại báo cáo.'),
    ('Đổi Giải pháp', 'Change',
     'After:\n– Xoá Version đang chọn; có Giải pháp thì nạp danh sách version, bỏ trống thì khoá ô Version.'),
    ('Bấm Tìm kiếm', 'Click', 'After:\n– Áp bộ lọc hiện tại, về trang 1, tải lại báo cáo.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Đưa mọi ô lọc về mặc định (Tháng, tháng và năm hiện tại), về trang 1, '
                             'tải lại báo cáo.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Cài đặt bộ lọc')
d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc', 'crud', actor=A)
d.p('2.3.2 Giới thiệu')
d.rule_ref('- Bộ lọc và UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Cho người dùng chọn các ô lọc muốn hiện trong khối Tìm kiếm nâng cao và sắp xếp thứ tự; cài đặt lưu '
         'riêng cho màn báo cáo này của từng người dùng.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
          '2. Hệ thống mở cửa sổ Cài đặt bộ lọc với 6 trường lọc theo cấu hình hiện tại.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để sắp xếp.\n'
          '4. Người dùng bấm “Lưu”.\n'
          '5. Hệ thống lưu cấu hình, đóng cửa sổ, báo “Cập nhật thành công” và vẽ lại khối lọc.',
    phu='• Bấm “Khôi phục mặc định” → đưa về đủ 6 trường theo thứ tự gốc (chưa lưu cho tới khi bấm Lưu).\n'
        '• Bấm “Đóng” / dấu × → đóng cửa sổ, không lưu.\n'
        '• Lưu lỗi → “Thao tác thất bại”.',
    dacbiet='Trường bị bỏ tích mà đang có giá trị lọc thì giá trị đó bị xoá, tránh lọc ngầm bằng ô người dùng '
            'không nhìn thấy.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('03-cai-dat.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
    ('Danh sách trường lọc', 'Checkbox', 'Enable', 'Danh sách 6 giá trị', 'Không', 'Theo cấu hình đã lưu',
     'Xem theo thời gian · Thời gian làm giải pháp · Công ty – Phòng ban · Khách hàng · Giải pháp · Version; '
     'mỗi dòng có số thứ tự và tay kéo ⠿.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Khoá trong lúc đang lưu.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở cửa sổ với cấu hình đang áp dụng.'),
    ('Tích / bỏ tích, kéo sắp xếp', 'Click', 'After:\n– Cập nhật danh sách trong cửa sổ, chưa lưu.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Không kiểm tra quyền riêng.\n'
     'After:\n– Lưu cấu hình hiện / ẩn và thứ tự cho màn này của người dùng.\n'
     '– Xoá giá trị lọc của trường vừa bị ẩn.\n'
     '– Đóng cửa sổ, hiển thị “Cập nhật thành công”.\n'
     '– Lỗi → hiển thị “Thao tác thất bại”.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Hiện đủ 6 trường theo thứ tự gốc; chưa lưu.'),
    ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Xem chi tiết theo cấp (mở rộng / thu gọn)')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Xem chi tiết theo cấp (mở rộng / thu gọn)',
    mota='Mở rộng cây báo cáo xuống tới từng version, hoặc thu về cấp gốc; mở rộng / thu gọn riêng từng dòng.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Báo cáo đang có dữ liệu.',
    chinh='1. Người dùng bấm “Xem chi tiết”.\n'
          '2. Hệ thống mở rộng toàn bộ công ty, phòng giải pháp, giải pháp; nút đổi thành “Chỉ xem cấp gốc”.\n'
          '3. Người dùng bấm “Chỉ xem cấp gốc” → hệ thống thu gọn toàn bộ, chỉ còn dòng tổng và dòng công ty.',
    phu='• Bấm mũi tên hoặc tên ở dòng công ty / phòng / giải pháp → mở rộng hoặc thu gọn riêng dòng đó.\n'
        '• Đổi trang / đổi bộ lọc → giữ nguyên chế độ đang chọn của nút.')
d.p('2.4.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết / Chỉ xem cấp gốc', shot=shot('04-chi-tiet.png'),
         shot_caption='Báo cáo ở chế độ Xem chi tiết — phần thông tin version')
d.figure(shot('04b-chi-tiet-phai.png'), 'Chế độ Xem chi tiết — cuộn sang phải, nhóm cột Hiệu suất', width_in=6.2)
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xem chi tiết', 'Button', 'Enable', '–', 'Hiển thị (nền xanh)',
     'Hiện khi đang ở chế độ cấp gốc; biểu tượng con mắt.'),
    ('Nút Chỉ xem cấp gốc', 'Button', 'Enable', '–', 'Ẩn', 'Hiện khi đang xem chi tiết; biểu tượng cây.'),
    ('Mũi tên mở rộng / thu gọn', 'Icon Button', 'Enable', '–', 'Thu gọn',
     'Ở cột STT của dòng công ty, phòng giải pháp, giải pháp; mũi tên phải = đang thu gọn, mũi tên xuống = đang mở.'),
    ('Dòng Phòng giải pháp', 'Table/Grid', 'Read-only', '–', 'Ẩn tới khi mở công ty',
     'Cộng dồn số nhiệm vụ, giờ được giao, giờ thực tế; hiệu suất và nhiệm vụ/giờ tính lại từ tổng giờ.'),
    ('Dòng Giải pháp', 'Table/Grid', 'Read-only', '–', 'Ẩn tới khi mở phòng',
     'Trạng thái = trạng thái version cuối; Ngày bắt đầu làm = sớm nhất; Ngày chốt = muộn nhất; Số ngày thực '
     'hiện = Ngày chốt muộn nhất − Ngày bắt đầu sớm nhất. Số hạng mục, Số nhân sự bấm được.'),
    ('Dòng Version', 'Table/Grid', 'Read-only', '–', 'Ẩn tới khi mở giải pháp',
     'Đủ 12 cột chỉ số; Số hạng mục, Số nhân sự tham gia là liên kết.'),
], required=False)
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xem chi tiết', 'Click', 'After:\n– Mở rộng mọi công ty, phòng, giải pháp của trang hiện tại; đổi nút '
                                   'thành “Chỉ xem cấp gốc”.'),
    ('Bấm Chỉ xem cấp gốc', 'Click', 'After:\n– Thu gọn toàn bộ; đổi nút thành “Xem chi tiết”.'),
    ('Bấm mũi tên / tên dòng công ty, phòng, giải pháp', 'Click',
     'After:\n– Đảo trạng thái mở rộng / thu gọn của riêng dòng đó.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Xem chi tiết số hạng mục')
d.p('2.5.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='detail')
d.intro_table(
    ten='Xem chi tiết số hạng mục',
    mota='Bấm số ở cột Số hạng mục để xem danh sách hạng mục của giải pháp kèm leader, số giờ được giao và giờ '
         'thực tế từng hạng mục.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Đang ở chế độ Xem chi tiết hoặc đã mở rộng tới dòng giải pháp / version.',
    chinh='1. Người dùng bấm số ở cột Số hạng mục của dòng giải pháp hoặc dòng version.\n'
          '2. Hệ thống tải danh sách hạng mục của giải pháp.\n'
          '3. Hệ thống mở cửa sổ “Chi tiết số hạng mục”.\n'
          '4. Người dùng bấm “Đóng” hoặc dấu × để đóng.',
    phu='• Giải pháp chưa có hạng mục → “Không có dữ liệu hạng mục.”.\n'
        '• Mở từ dòng giải pháp → không hiện dòng Version / PM ở phần đầu cửa sổ.')
d.p('2.5.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Số hạng mục', shot=shot('05-hang-muc.png'),
         shot_caption='Cửa sổ Chi tiết số hạng mục')
d.p('2.5.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Chi tiết số hạng mục', '–'),
    ('Thông tin đầu', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     '“Giải pháp: <tên> (<mã>)”; “Version: <mã> • PM: <tên>” (khi mở từ dòng version); “KH: <khách hàng>” (nếu có).'),
    ('Cột Hạng mục', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tên hạng mục; sắp theo thứ tự tạo.'),
    ('Cột Leader', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Chưa có hiện “—”.'),
    ('Cột Số giờ được giao', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tổng giờ ước tính của nhiệm vụ thuộc hạng mục, dạng “<n> giờ”.'),
    ('Cột Giờ thực tế', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tổng giờ báo cáo tiến độ của nhiệm vụ thuộc hạng mục.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu hạng mục.”'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)
d.p('2.5.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm số ở cột Số hạng mục', 'Click',
     'After:\n– Tải hạng mục của giải pháp (giờ tính trên toàn bộ nhiệm vụ của hạng mục, không tách theo version).\n'
     '– Mở cửa sổ; lỗi tải → cửa sổ hiện trạng thái rỗng.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Xem chi tiết số nhân sự tham gia')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='detail')
d.intro_table(
    ten='Xem chi tiết số nhân sự tham gia',
    mota='Bấm số ở cột Số nhân sự tham gia để xem danh sách nhân sự của version, vai trò và số giờ tham gia.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Đang ở chế độ Xem chi tiết hoặc đã mở rộng tới dòng giải pháp / version.',
    chinh='1. Người dùng bấm số ở cột Số nhân sự tham gia của dòng version (hoặc dòng giải pháp).\n'
          '2. Hệ thống tải danh sách nhân sự của version (mở từ dòng giải pháp thì lấy version mới nhất).\n'
          '3. Hệ thống mở cửa sổ “Chi tiết số nhân sự tham gia”.\n'
          '4. Người dùng bấm “Đóng” hoặc dấu × để đóng.',
    phu='• Version chưa có nhân sự → “Không có dữ liệu nhân sự.”.')
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Số nhân sự tham gia', shot=shot('06-nhan-su.png'),
         shot_caption='Cửa sổ Chi tiết số nhân sự tham gia')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Chi tiết số nhân sự tham gia', '–'),
    ('Thông tin đầu', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     '“Giải pháp: <tên> (<mã>)”; “Version: <mã> • PM: <tên>”; “KH: <khách hàng>” (nếu có).'),
    ('Cột Nhân sự', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Thiếu tên hiện “Không xác định”.'),
    ('Cột Vai trò', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'PM / Leader hạng mục / Thành viên; người thực hiện nhiệm vụ không có trong danh sách nhân sự version '
     'hiện “Thành viên”.'),
    ('Cột Giờ tham gia', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tổng giờ báo cáo tiến độ của người đó trên các nhiệm vụ thuộc version, dạng “<n> giờ”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu nhân sự.”'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm số ở cột Số nhân sự tham gia', 'Click',
     'After:\n– Tải nhân sự của version: danh sách nhân sự version (sắp PM → Leader hạng mục → Thành viên, rồi '
     'theo tên) và người thực hiện nhiệm vụ không có trong danh sách đó (sắp theo tên).\n'
     '– Mở cửa sổ; lỗi tải → cửa sổ hiện trạng thái rỗng.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ------------------------------------------------------------------ 2.7
d.h3('2.7 Xuất Excel báo cáo')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xuất Excel báo cáo', 'io', actor=A)
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='excel')
d.intro_table(
    ten='Xuất Excel báo cáo',
    mota='Tải file Excel toàn bộ báo cáo theo bộ lọc đang áp dụng (không phân trang), mở rộng đủ 4 cấp.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “Xuất Excel”.\n'
          '2. Hệ thống dựng file theo bộ lọc đang áp dụng và trong phạm vi quyền.\n'
          '3. Trình duyệt tải file “bao_cao_giai_phap_theo_version.xls”.\n'
          '4. Hệ thống báo “Xuất Excel thành công”.',
    phu='• Lỗi khi xuất → “Lỗi khi xuất Excel”.\n'
        '• Không có dữ liệu → vẫn tải file chỉ gồm phần đầu trang và dòng tiêu đề cột.',
    dacbiet='Đầu file là ảnh tiêu đề (header) của công ty người dùng đang làm việc; chưa cấu hình thì dùng ảnh '
            'mặc định. Cuối file có khối ký “Người lập”.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('07-xuat.png'),
         shot_caption='Bấm Xuất Excel — thông báo xuất thành công')
d.figure(shot('07b-file-excel.png'), 'Nội dung file Excel tải về', width_in=6.2)
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xuất Excel', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Biểu tượng file Excel.'),
    ('Phần đầu file', 'Label', 'Read-only', '–', '–', 'Theo công ty đang làm việc',
     'Ảnh header công ty + tiêu đề “BÁO CÁO THEO DÕI CHỈ SỐ HOÀN THÀNH GIẢI PHÁP THEO VERSION”.'),
    ('Dòng tiêu đề cột', 'Table/Grid', 'Read-only', '14 cột', '–', 'Hiển thị',
     'STT · Công ty / Phòng / Giải pháp / Version · THÔNG TIN VERSION (Trạng thái version, Ngày bắt đầu làm, '
     'Ngày chốt, Số ngày thực hiện) · KHỐI LƯỢNG & ĐỊNH MỨC (Số hạng mục, Số nhân sự tham gia, Số nhiệm vụ giao, '
     'Số giờ được giao, Số giờ thực tế) · HIỆU SUẤT (Hiệu suất (%), Nhiệm vụ / giờ, Đánh giá hiệu suất).'),
    ('Dòng dữ liệu', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Công ty (nền xanh nhạt) → Phòng (nền xám) → Giải pháp “<mã> - <tên>” → Version; STT chỉ đánh ở dòng '
     'version, chạy liên tục toàn file.'),
    ('Khối ký', 'Label', 'Read-only', '–', '–', 'Hiển thị', '“Ngày ..., tháng ..., năm ...” — Người lập (Ký, họ tên).'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Xuất Excel thành công” / “Lỗi khi xuất Excel”.'),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Không kiểm tra quyền riêng.\n'
     'During:\n– Lấy bộ lọc đang áp dụng (kỳ thời gian, công ty, phòng ban, nhân viên, khách hàng, giải pháp, '
     'version); bỏ phân trang.\n' + SCOPE_NOTE + '\n'
     'After:\n– Tải file “bao_cao_giai_phap_theo_version.xls”, hiển thị “Xuất Excel thành công”.\n'
     '– Lỗi → hiển thị “Lỗi khi xuất Excel”.'),
])

# ------------------------------------------------------------------ 2.8
d.h3('2.8 In báo cáo')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'In báo cáo', 'io', actor=A)
d.p('2.8.2 Giới thiệu')
d.rule_ref('- UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='In báo cáo',
    mota='Mở bản xem trước để in toàn bộ báo cáo theo bộ lọc đang áp dụng, khổ A4 ngang.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “In báo cáo”.\n'
          '2. Hệ thống mở tab mới hiển thị bản xem trước gồm header công ty, tiêu đề và bảng báo cáo đủ 4 cấp.\n'
          '3. Người dùng bấm nút “In”.\n'
          '4. Hệ thống mở hộp thoại in của trình duyệt (A4 ngang, lề 8mm × 6mm).',
    phu='• Không có dữ liệu → bảng hiện “Không có dữ liệu”.\n'
        '• Lỗi tải dữ liệu → khung đỏ hiện nội dung lỗi hoặc “Lỗi không xác định khi tải dữ liệu báo cáo”.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => In báo cáo => In', shot=shot('08-in.png'), shot_caption='Bản xem trước khi in')
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Không xuất hiện trên bản in.'),
    ('Header công ty', 'Label', 'Read-only', '–', '–', 'Theo công ty đang làm việc',
     'Chưa cấu hình thì dùng ảnh mặc định.'),
    ('Tiêu đề', 'Label', 'Read-only', '–', '–',
     'BÁO CÁO THEO DÕI CHỈ SỐ HOÀN THÀNH GIẢI PHÁP THEO VERSION', '–'),
    ('Bảng báo cáo', 'Table/Grid', 'Read-only', '14 cột', '–', 'Theo dữ liệu',
     'Cột gọn: Trạng thái · Bắt đầu · Ngày chốt · Số ngày · Hạng mục · Nhân sự · Số nhiệm vụ · Giờ giao · Giờ thực '
     'tế · Hiệu suất (%) · Nhiệm vụ / giờ · Đánh giá. STT phân cấp 1 / 1.1 / 1.1.1 / 1.1.1.1; dòng công ty, '
     'phòng, giải pháp in đậm có nền.'),
    ('Khối ký', 'Label', 'Read-only', '–', '–', 'Hiển thị', '“Ngày ...., tháng ...., năm ....” — Người lập (Ký, họ tên).'),
    ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Khung đỏ phía trên, không in ra.'),
])
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In báo cáo', 'Click',
     'After:\n– Mở tab mới, mang theo bộ lọc đang áp dụng; tải toàn bộ dữ liệu (không phân trang).\n' + SCOPE_NOTE),
    ('Bấm In', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt với khổ A4 ngang.'),
])

# ==================================================== PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của báo cáo; không lặp lại các quy tắc đã có trong SRS '
           'quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi dữ liệu theo quyền', [
        '– V1: mọi giải pháp. V2: giải pháp thuộc công ty đang làm việc. V3: giải pháp của phòng ban / bộ phận '
        'người dùng quản lý và giải pháp người dùng là PM. Không có quyền nào: chỉ giải pháp người dùng là PM.',
        '– Có nhiều quyền thì lấy quyền rộng nhất. Áp cho cả xem, xuất Excel và in.',
        '– Các ô lọc Công ty, Phòng ban, Nhân viên luôn hiện; chọn ngoài phạm vi quyền thì báo cáo trả rỗng.',
    ], ['Xem báo cáo', 'Xuất Excel', 'In']),
    ('BR-02', 'Đối tượng đưa vào báo cáo', [
        '– Chỉ tính giải pháp và version KHÔNG ở trạng thái Nháp.',
        '– Lọc thời gian theo Ngày bắt đầu làm của version, gồm cả 2 đầu khoảng. Kỳ Tháng: ngày 1 → ngày cuối '
        'tháng; kỳ Năm: 01/01 → 31/12; kỳ Tuỳ chỉnh: theo khoảng nhập, bỏ trống thì không giới hạn.',
        '– Lọc Nhân viên = lọc theo PM (người tạo giải pháp); lọc Khách hàng theo khách hàng của dự án.',
    ], ['Xem báo cáo', 'Tìm kiếm và lọc']),
    ('BR-03', 'Cấu trúc cây và phân trang', [
        '– Cây Công ty → Phòng giải pháp → Giải pháp → Version, lấy theo công ty và phòng ghi trên giải pháp; '
        'thiếu thì gom vào “Không xác định”.',
        '– Sắp theo tên công ty, tên phòng, mã giải pháp, mã version.',
        '– Phân trang theo GIẢI PHÁP (15 / 50 / 100 / 200); dòng công ty, phòng vẫn mang số tổng của cả kỳ lọc, '
        'không chỉ của trang đang xem.',
    ], 'Xem báo cáo'),
    ('BR-04', 'Chỉ số của version', [
        '– Số nhiệm vụ giao = số nhiệm vụ gắn version; Số giờ được giao = tổng giờ ước tính của các nhiệm vụ đó.',
        '– Số giờ thực tế = tổng giờ khai khi báo cáo tiến độ các nhiệm vụ của version.',
        '– Số nhân sự = nhân sự trong danh sách nhân sự version + người thực hiện nhiệm vụ không có trong danh '
        'sách đó.',
        '– Số hạng mục = số hạng mục của giải pháp (mọi version cùng giải pháp hiện cùng một số).',
        '– Số ngày thực hiện = Ngày kết thúc kế hoạch − Ngày bắt đầu làm (thiếu 1 trong 2 ngày → 0). Ngày chốt = '
        'ngày duyệt version.',
    ], ['Xem báo cáo', 'Xuất Excel', 'In']),
    ('BR-05', 'Hiệu suất và đánh giá', [
        '– Hiệu suất (%) = Số giờ được giao / Số giờ thực tế × 100, làm tròn 1 chữ số; chưa có giờ thực tế → 0.',
        '– Nhiệm vụ / giờ = Số nhiệm vụ / Số giờ thực tế (2 chữ số); chưa có giờ thực tế → “—”.',
        '– Đánh giá: ≥ 100% Hiệu suất cao (xanh lá); 80% – dưới 100% Hiệu suất trung bình (cam); trên 0 – dưới '
        '80% Hiệu suất thấp (đỏ); 0 → Chưa có dữ liệu (xám).',
    ], ['Xem báo cáo', 'Xuất Excel', 'In']),
    ('BR-06', 'Số liệu dòng tổng hợp', [
        '– Dòng giải pháp: trạng thái = trạng thái version cuối; ngày bắt đầu = sớm nhất, ngày chốt = muộn nhất '
        'trong các version; số nhiệm vụ, giờ cộng dồn; hiệu suất tính lại từ tổng giờ.',
        '– Dòng phòng, công ty: cộng dồn số nhiệm vụ, giờ được giao, giờ thực tế, số version; hiệu suất tính lại.',
        '– Dòng “Tổng toàn bộ version”: số giải pháp, số version, thời gian TB = trung bình số ngày thực hiện '
        'của các version có đủ ngày bắt đầu và kết thúc; hiệu suất giờ trên toàn kỳ lọc.',
    ], 'Xem báo cáo'),
    ('BR-07', 'Phạm vi số liệu ở cửa sổ chi tiết', [
        '– Chi tiết số hạng mục: giờ của mỗi hạng mục tính trên toàn bộ nhiệm vụ của hạng mục (mọi version).',
        '– Chi tiết số nhân sự: tính riêng cho 1 version; mở từ dòng giải pháp thì lấy version mới nhất.',
    ], ['Chi tiết số hạng mục', 'Chi tiết số nhân sự']),
    ('BR-08', 'Xuất Excel và In', [
        '– Lấy toàn bộ dữ liệu theo bộ lọc đang áp dụng, không phân trang, luôn đủ 4 cấp.',
        '– Header lấy theo công ty người dùng đang làm việc; chưa cấu hình dùng ảnh mặc định.',
        '– Bản in khổ A4 ngang.',
    ], ['Xuất Excel', 'In']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

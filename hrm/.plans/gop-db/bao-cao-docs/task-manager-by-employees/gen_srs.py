# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo Phân bổ nguồn lực theo nhân viên.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/report/task-manager-by-employees/{index,print}.vue
      components/{GanttChart,TaskDetailModal}.vue
      components/V2BaseSmartFilterPanel.vue · components/modal/filter-customization-modal.vue
      components/V2BaseCompanyDepartmentFilter.vue · components/V2BasePagination.vue
      components/menu-sidebar.js (menuItemsAssign › Báo cáo)
  BE  Modules/Assign/Routes/api.php (assign/report/task-manager-by-employees — KHÔNG gắn checkPermission)
      TaskManagerByEmployeesReportController · Services/Report/TaskManagerByEmployeesReportService
      Transformers/TaskManagerByEmployeesResource · app/ExcelExport/TaskManagerByEmployeesReportExport
      resources/views/exports/task_manager_by_employees_report.blade.php · Entities/Task/Task::STATUS
  Quyền: PermissionsTableSeeder id 1045-1048 (nhóm "Báo cáo phân bổ nguồn lực")
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


TEN_MAN = 'Báo cáo Phân bổ nguồn lực theo nhân viên'
MENU = 'Phân hệ Công việc => Báo cáo => Phân bổ nguồn lực theo nhân viên'
A = 'Người xem báo cáo'

ICONS = {
    'Phân hệ Công việc': 'icon_phanhe.png',
    'Báo cáo': 'icon_baocao.png',
    'Phân bổ nguồn lực theo nhân viên': 'icon_man.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Ẩn lịch Gantt': 'icon_angantt.png',
    'Xem lịch Gantt': 'icon_xemgantt.png',
    'Số nhiệm vụ': 'icon_nhiemvu.png',
    'Thanh nhiệm vụ trên lịch Gantt': 'icon_thanhgantt.png',
    'Xuất Excel': 'icon_xuat.png',
    'In báo cáo': 'icon_in.png',
    'In': 'icon_nutin.png',
}

out = os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN)
d = SrsDoc(out=out, menu=MENU, route='', full_url='', img_prefix='tmrep_')
d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})
d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

SCOPE_NOTE = ('– Chỉ lấy nhân viên trong phạm vi quyền của người xem (V1 › V2 › V3 › V4 › mặc định chỉ bản '
              'thân) — xem quy tắc BR-01.')

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Báo cáo phân bổ nguồn lực theo nhân viên (phân hệ Công việc), '
    'nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu các chức năng xem, lọc, xem lịch Gantt, xem chi tiết nhiệm vụ, xuất Excel và in.',
    'Làm rõ cách hệ thống so sánh giờ nhiệm vụ được giao với giờ làm theo ca của từng nhân viên để xác định '
    'nhân viên đang rảnh, phân bổ hợp lý hay vượt tải.',
    'Làm rõ phạm vi nhân viên mỗi người dùng được xem theo quyền.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Kỳ báo cáo', 'Khoảng ngày đang xem: hôm nay, tuần hiện tại, tháng hiện tại hoặc khoảng tuỳ chọn.'),
    ('Giờ làm', 'Giờ làm định mức của nhân viên trong kỳ = tổng giờ công các ca làm việc được phân.'),
    ('Giờ nhiệm vụ', 'Tổng giờ ước tính của các nhiệm vụ nhân viên được giao trong kỳ.'),
    ('% sử dụng', 'Giờ nhiệm vụ / Giờ làm × 100 — mức công suất đang dùng.'),
    ('Rảnh', 'Số giờ làm còn trống = Giờ làm − Giờ nhiệm vụ (không âm).'),
    ('Vượt tải', 'Số giờ nhiệm vụ vượt quá giờ làm = Giờ nhiệm vụ − Giờ làm (không âm).'),
    ('Lịch Gantt', 'Trục ngày của kỳ báo cáo; mỗi nhiệm vụ là một thanh kéo từ ngày bắt đầu tới hạn hoàn thành.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('–', 'Không có quyền thao tác riêng',
     'Menu “Phân bổ nguồn lực theo nhân viên” hiển thị cho mọi người dùng đã đăng nhập vào phân hệ Công việc. '
     'Mọi thao tác (xem, lọc, cài đặt bộ lọc, xem lịch Gantt, xem chi tiết nhiệm vụ, xuất Excel, in) không '
     'kiểm tra quyền riêng; nhân viên hiển thị được giới hạn theo nhóm quyền phạm vi dữ liệu bên dưới.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem báo cáo phân bổ nguồn lực theo tổng công ty',
     'Nhân viên của mọi công ty. Bộ lọc hiện đủ Công ty, Phòng ban, Bộ phận, Nhân viên.'),
    ('V2', 'Xem báo cáo phân bổ nguồn lực theo công ty',
     'Nhân viên thuộc công ty đang làm việc. Bộ lọc hiện Phòng ban, Bộ phận, Nhân viên.'),
    ('V3', 'Xem báo cáo phân bổ nguồn lực theo phòng ban',
     'Nhân viên thuộc phòng ban hoặc bộ phận người dùng quản lý. Bộ lọc hiện Phòng ban, Bộ phận, Nhân viên.'),
    ('V4', 'Xem báo cáo phân bổ nguồn lực theo bộ phận',
     'Nhân viên thuộc bộ phận người dùng quản lý. Bộ lọc hiện Bộ phận, Nhân viên.'),
    ('–', 'Không có quyền nào ở trên', 'Chỉ chính người dùng. Bộ lọc không hiện các ô tổ chức.'),
], widths=[0.8, 2.4, 2.8])
d.p('Có nhiều quyền cùng lúc thì áp dụng quyền rộng nhất theo thứ tự V1 → V2 → V3 → V4.')

d.h2('2 Ma trận phân quyền')
FRS = [
    ('FR-01', 'Xem báo cáo phân bổ nguồn lực'),
    ('FR-02', 'Tìm kiếm và lọc báo cáo'),
    ('FR-03', 'Cài đặt bộ lọc'),
    ('FR-04', 'Xem / ẩn lịch Gantt'),
    ('FR-05', 'Xem chi tiết nhiệm vụ của nhân viên'),
    ('FR-06', 'Xem chi tiết nhiệm vụ theo dự án'),
    ('FR-07', 'Xuất Excel báo cáo'),
    ('FR-08', 'In báo cáo'),
]
d.table(['Chức năng', 'V1', 'V2', 'V3', 'V4', 'Không có quyền nào'],
        [('%s %s' % fr, '✅', '✅', '✅', '✅', '✅ (chỉ bản thân)') for fr in FRS],
        widths=[2.4, 0.5, 0.5, 0.5, 0.5, 1.6])
d.p('Mọi người dùng đều dùng được đủ 8 chức năng; khác nhau ở phạm vi nhân viên hiển thị (xem Danh sách quyền).')

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A, [0, 1, 2])],
    [('FR-01', 'Xem báo cáo phân bổ nguồn lực', 'view'),
     ('FR-07', 'Xuất Excel báo cáo', 'io'),
     ('FR-08', 'In báo cáo', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Xem / ẩn lịch Gantt', 'view', 'extend', [0], None),
     ('FR-05', 'Chi tiết nhiệm vụ của NV', 'view', 'extend', [0], None),
     ('FR-06', 'Chi tiết nhiệm vụ theo dự án', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem báo cáo phân bổ nguồn lực')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Phân trang và UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả '
           'chi tiết.', anchor='list')
d.intro_table(
    ten='Xem báo cáo phân bổ nguồn lực',
    mota='Hiển thị theo Phòng ban → Nhân viên: số nhiệm vụ, giờ làm, giờ nhiệm vụ, % sử dụng, trạng thái phân bổ '
         'và lịch Gantt nhiệm vụ trong kỳ.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và vào được phân hệ Công việc.',
    chinh='1. Người dùng vào menu Phân bổ nguồn lực theo nhân viên.\n'
          '2. Hệ thống áp kỳ mặc định Tháng hiện tại (ngày 1 → ngày cuối tháng).\n'
          '3. Hệ thống tải báo cáo trong phạm vi quyền, phân trang theo phòng ban (mặc định 10 phòng/trang), mọi '
          'phòng ban mở sẵn.\n'
          '4. Mỗi phòng ban hiện dòng tổng và danh sách nhân viên kèm lịch Gantt.\n'
          '5. Người dùng bấm vào dòng phòng ban để thu gọn / mở lại danh sách nhân viên của phòng đó.\n'
          '6. Người dùng đổi trang hoặc số phòng ban/trang; hệ thống tải lại.',
    phu='• Không có dữ liệu → “Không có dữ liệu phù hợp bộ lọc.”.\n'
        '• Đang tải → “Đang tải dữ liệu...”.\n'
        '• Tải lỗi → thông báo nội dung lỗi hoặc “Lỗi khi tải báo cáo phân bổ nguồn lực”.\n'
        '• Rê chuột vào tiêu đề cột Nhiệm vụ / Giờ làm / Giờ nhiệm vụ / % sử dụng → hiện giải thích cột.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-xem.png'), shot_caption='Báo cáo phân bổ nguồn lực lúc mới mở')
d.figure(shot('07-thu-gon.png'), 'Thu gọn một phòng ban và thanh phân trang theo phòng ban', width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Báo cáo phân bổ nguồn lực theo nhân viên',
     'Kèm biểu tượng ⓘ: “Xem nhiệm vụ của từng nhân viên trên trục thời gian ngày / tuần / tháng, kèm công suất '
     'sử dụng để biết ai đang rảnh, đủ tải, quá tải.”'),
    ('Khối Bộ lọc phân bổ nguồn lực (Gantt)', 'Card', 'Hiển thị', '–', 'Thu gọn', 'Xem FR-02, FR-03.'),
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–',
     'Gantt phân bổ: Phòng ban → Nhân viên → Nhiệm vụ theo thời gian', '–'),
    ('Nhãn kỳ báo cáo', 'Badge', 'Hiển thị', '–', 'Theo dữ liệu',
     '“<Chế độ>: dd-mm-yyyy → dd-mm-yyyy • <n> nhân viên • <n> nhiệm vụ”.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Đang xuất hiện “Đang xuất...” và khoá. Xem FR-07.'),
    ('Nút In báo cáo', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-08.'),
    ('Nút Ẩn lịch Gantt / Xem lịch Gantt', 'Button', 'Enable', '–', 'Ẩn lịch Gantt', 'Xem FR-04.'),
    ('Cột Stt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng phòng ban: mũi tên mở / thu gọn. Dòng nhân viên: số thứ tự liên tục qua các phòng trong trang.'),
    ('Cột Nhân viên', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Phòng ban: “Phòng: <tên>” + “Số nhân viên: <n>”. Nhân viên: tên + “Chức vụ: <chức vụ>”.'),
    ('Cột Nhiệm vụ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Số nhiệm vụ trong kỳ; ở dòng nhân viên là liên kết mở FR-05.'),
    ('Cột Giờ làm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Giờ làm định mức theo ca, 1 chữ số thập phân.'),
    ('Cột Giờ nhiệm vụ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tổng giờ ước tính; ở dòng nhân viên là liên kết mở FR-05.'),
    ('Cột % sử dụng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dạng “<n>%”; ở dòng nhân viên tô màu theo trạng thái.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 3 giá trị', 'Theo dữ liệu',
     'Dòng nhân viên: badge Vượt tải (đỏ) / Cần phân thêm nhiệm vụ (cam) / Phân bổ hợp lý (xanh) + dòng '
     '“Rảnh: <h> • Vượt tải: <h>” (vượt tải > 0 tô đỏ). Dòng phòng ban: “Tổng quan phòng ban”.'),
    ('Cột Lịch Gantt', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Xem FR-04; dòng phòng ban ghi “Xem chi tiết thời gian tại từng nhân viên bên dưới”.'),
    ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 phòng ban', '10',
     'Đếm theo phòng ban (“phòng ban”).'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
    ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu...”'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Không kiểm tra quyền thao tác; đọc quyền V1–V4 để quyết định ô lọc tổ chức nào được hiện.\n'
     'After:\n– Nạp danh sách Dự án; áp kỳ Tháng hiện tại; tải trang 1 (10 phòng ban), mở sẵn mọi phòng.\n'
     + SCOPE_NOTE),
    ('Bấm dòng phòng ban', 'Click', 'After:\n– Thu gọn hoặc mở lại danh sách nhân viên của phòng đó.'),
    ('Đổi trang / số phòng ban mỗi trang', 'Click',
     'After:\n– Tải lại trang tương ứng (đổi số dòng thì về trang 1), giữ nguyên bộ lọc.'),
    ('Tải dữ liệu lỗi', 'System',
     'After:\n– Hiển thị nội dung lỗi trả về, hoặc “Lỗi khi tải báo cáo phân bổ nguồn lực”.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc báo cáo')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô '
           'tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc báo cáo',
    mota='Lọc báo cáo theo kỳ thời gian, tổ chức (công ty, phòng ban, bộ phận, nhân viên — theo quyền), dự án, '
         'khoảng công suất và chỉ nhân viên có nhiệm vụ.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
          '2. Người dùng chọn giá trị ở các ô chọn; mỗi lần chọn hệ thống tự tìm, về trang 1.\n'
          '3. Với ô tích “Chỉ hiển thị nhân viên có nhiệm vụ trong kỳ”, người dùng tích rồi bấm “Tìm kiếm”.\n'
          '4. Hệ thống tải lại báo cáo theo bộ lọc.',
    phu='• Chế độ thời gian = Tuỳ chọn → hiện ô Thời gian, mang sẵn khoảng ngày của chế độ trước.\n'
        '• Khoảng ngày bị bỏ trống → “Vui lòng chọn khoảng thời gian (Từ ngày, Đến ngày)”.\n'
        '• Bấm “Làm mới” → bộ lọc về mặc định (Tháng hiện tại) và tải lại.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao — mặc định Tháng hiện tại')
d.figure(shot('02c-loc-tuy-chon.png'),
         'Chế độ thời gian Tuỳ chọn + tích “Chỉ hiển thị nhân viên có nhiệm vụ trong kỳ”', width_in=6.2)
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Chế độ thời gian', 'Dropdown', 'Enable', 'Tuần hiện tại / Hôm nay / Tháng hiện tại / Tuỳ chọn', 'Có',
     'Tháng hiện tại', 'Không xoá trắng được. Tuần hiện tại = Thứ Hai → Chủ nhật của tuần chứa hôm nay.'),
    ('Thời gian', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy, từ ngày → đến ngày', 'Có khi Tuỳ chọn',
     'Khoảng của chế độ trước', 'Chỉ hiện khi Chế độ thời gian = Tuỳ chọn; gộp 1 ô.'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Chỉ hiện với V1. Biểu tượng ổ khoá cạnh nhãn: hiện cả công ty đã khoá.'),
    ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách theo công ty', 'Không', 'Trống', 'Hiện với V1, V2, V3.'),
    ('Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách theo phòng ban', 'Không', 'Trống', 'Hiện với V1 – V4.'),
    ('Nhân viên', 'Dropdown', 'Enable / Ẩn', 'Danh sách theo đơn vị đã chọn', 'Không', 'Trống',
     'Hiện với V1 – V4.'),
    ('Dự án', 'Dropdown', 'Enable', 'Danh sách “Mã – Tên” dự án', 'Không', 'Trống',
     'Chỉ tính nhiệm vụ thuộc dự án đã chọn.'),
    ('Khoảng công suất (%)', 'Dropdown', 'Enable', '< 60% (rảnh) / 60% – 100% (bình thường) / > 100% (quá tải)',
     'Không', 'Trống', 'Lọc nhân viên theo % sử dụng.'),
    ('Chỉ hiển thị nhân viên có nhiệm vụ trong kỳ', 'Checkbox', 'Enable', '–', 'Không', 'Bỏ tích',
     'Tích / bỏ tích không tự tìm — phải bấm Tìm kiếm.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp bộ lọc, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đưa bộ lọc về mặc định rồi tìm lại.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Tìm kiếm nâng cao',
     'Mở / thu gọn khối lọc.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Click', 'After:\n– Mở hoặc thu gọn khối lọc.'),
    ('Chọn giá trị một ô chọn', 'Change',
     'After:\n– Áp bộ lọc ngay, về trang 1, tải lại báo cáo.\n' + SCOPE_NOTE),
    ('Đổi Chế độ thời gian', 'Change',
     'After:\n– Hôm nay: từ = đến = hôm nay. Tuần hiện tại: Thứ Hai → Chủ nhật. Tháng hiện tại: ngày 1 → ngày cuối '
     'tháng. Tuỳ chọn: giữ khoảng hiện có, hiện ô Thời gian.'),
    ('Bấm Tìm kiếm', 'Click',
     'During:\n– Thiếu Từ ngày hoặc Đến ngày → hiển thị “Vui lòng chọn khoảng thời gian (Từ ngày, Đến ngày)”, '
     'không có dữ liệu.\n'
     'After:\n– Áp bộ lọc (kể cả ô tích Chỉ hiển thị nhân viên có nhiệm vụ), về trang 1, tải lại báo cáo.'),
    ('Bấm Làm mới', 'Click',
     'After:\n– Xoá mọi ô lọc, đặt Tháng hiện tại, bỏ tích, về trang 1 và tải lại báo cáo.'),
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
          '2. Hệ thống mở cửa sổ Cài đặt bộ lọc với 5 trường lọc theo cấu hình hiện tại.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để sắp xếp.\n'
          '4. Người dùng bấm “Lưu”.\n'
          '5. Hệ thống lưu cấu hình, đóng cửa sổ, báo “Cập nhật thành công” và vẽ lại khối lọc.',
    phu='• Bấm “Khôi phục mặc định” → đưa về đủ trường theo thứ tự gốc (chưa lưu cho tới khi bấm Lưu).\n'
        '• Bấm “Đóng” / dấu × → đóng cửa sổ, không lưu.\n'
        '• Lưu lỗi → “Thao tác thất bại”.',
    dacbiet='Trường bị bỏ tích mà đang có giá trị lọc thì giá trị đó bị xoá, tránh lọc ngầm bằng ô người dùng '
            'không nhìn thấy.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('04-cai-dat.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
    ('Danh sách trường lọc', 'Checkbox', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Theo cấu hình đã lưu',
     'Chế độ thời gian · Công ty – Phòng ban – Bộ phận · Dự án · Khoảng công suất (%) · Chỉ hiển thị nhân viên '
     'có nhiệm vụ trong kỳ (ô Thời gian chỉ có khi chọn Tuỳ chọn); mỗi dòng có số thứ tự và tay kéo ⠿.'),
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
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Hiện đủ trường theo thứ tự gốc; chưa lưu.'),
    ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Xem / ẩn lịch Gantt')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Xem / ẩn lịch Gantt',
    mota='Cột Lịch Gantt vẽ nhiệm vụ của từng nhân viên trên trục ngày của kỳ báo cáo, tô màu theo hạn hoàn '
         'thành; có thể ẩn cột để xem gọn bảng số liệu.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Báo cáo đang có dữ liệu.',
    chinh='1. Khi mở màn, cột Lịch Gantt hiển thị sẵn.\n'
          '2. Mỗi nhiệm vụ là một thanh từ ngày bắt đầu tới hạn hoàn thành (cắt theo kỳ), ghi mã nhiệm vụ; các '
          'nhiệm vụ trùng thời gian xếp xuống dòng dưới.\n'
          '3. Người dùng rê chuột vào thanh để xem dự án, ngày, giờ ước tính, trạng thái.\n'
          '4. Người dùng bấm “Ẩn lịch Gantt” → cột Gantt ẩn; bấm “Xem lịch Gantt” → hiện lại.',
    phu='• Nhiệm vụ thiếu ngày bắt đầu hoặc hạn hoàn thành → không vẽ thanh.\n'
        '• Bấm vào một thanh → mở FR-06.')
d.p('2.4.2 Layout màn hình')
d.layout(menu=MENU + ' => Ẩn lịch Gantt / Xem lịch Gantt', shot=shot('03-gantt.png'),
         shot_caption='Lịch Gantt nhiệm vụ của nhân viên trong tháng (đã tích chỉ nhân viên có nhiệm vụ)')
d.figure(shot('08-an-gantt.png'), 'Bảng sau khi bấm Ẩn lịch Gantt', width_in=6.2)
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Ẩn lịch Gantt / Xem lịch Gantt', 'Button', 'Enable', '–', 'Ẩn lịch Gantt',
     'Biểu tượng con mắt gạch / con mắt.'),
    ('Chú thích màu', 'Label', 'Hiển thị', '3 giá trị', 'Hiển thị',
     'Bình thường (xanh) · Sát deadline (cam) · Quá hạn (đỏ), ở đầu cột Lịch Gantt.'),
    ('Trục ngày', 'Table/Grid', 'Read-only', 'Từng ngày trong kỳ', 'Theo kỳ',
     'Mỗi ô: số ngày + thứ (T2 … T7, CN); ngày hôm nay được tô nổi bật.'),
    ('Thanh nhiệm vụ', 'Icon Button', 'Enable', '–', 'Theo dữ liệu',
     'Nhãn = mã nhiệm vụ. Đỏ: hạn hoàn thành trước hôm nay mà chưa Hoàn thành; cam: hạn đúng hôm nay mà chưa '
     'Hoàn thành; còn lại xanh.'),
    ('Chú giải khi rê chuột', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Tên dự án · ngày bắt đầu → hạn hoàn thành · “<n> giờ • <trạng thái>”.'),
], required=False)
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Ẩn lịch Gantt', 'Click', 'After:\n– Ẩn cột Lịch Gantt; nút đổi thành “Xem lịch Gantt”.'),
    ('Bấm Xem lịch Gantt', 'Click', 'After:\n– Hiện lại cột Lịch Gantt; nút đổi thành “Ẩn lịch Gantt”.'),
    ('Rê chuột vào thanh nhiệm vụ', 'Hover', 'After:\n– Hiện chú giải dự án, thời gian, giờ, trạng thái.'),
    ('Bấm thanh nhiệm vụ', 'Click', 'After:\n– Mở cửa sổ chi tiết nhiệm vụ theo dự án (FR-06).'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Xem chi tiết nhiệm vụ của nhân viên')
d.p('2.5.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='detail')
d.intro_table(
    ten='Xem chi tiết nhiệm vụ của nhân viên',
    mota='Bấm số ở cột Nhiệm vụ hoặc Giờ nhiệm vụ của một nhân viên để xem toàn bộ nhiệm vụ của người đó trong kỳ.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Báo cáo đang có dữ liệu.',
    chinh='1. Người dùng bấm số ở cột Nhiệm vụ hoặc Giờ nhiệm vụ của dòng nhân viên.\n'
          '2. Hệ thống mở cửa sổ “Chi tiết tất cả task trong kỳ” với tiêu đề “[Mã NV] Tên – Chức vụ”.\n'
          '3. Người dùng bấm “Đóng” hoặc dấu × để đóng.',
    phu='• Nhân viên không có nhiệm vụ → “Không có nhiệm vụ phù hợp điều kiện.”.')
d.p('2.5.2 Layout màn hình')
d.layout(menu=MENU + ' => Số nhiệm vụ', shot=shot('05-chi-tiet-nv.png'),
         shot_caption='Cửa sổ chi tiết tất cả nhiệm vụ của nhân viên trong kỳ')
MODAL_UI = [
    ('Cột #', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Số thứ tự.'),
    ('Cột Mã nhiệm vụ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Tên nhiệm vụ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Dự án', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tên dự án của nhiệm vụ.'),
    ('Cột Ngày bắt đầu / Hạn hoàn thành', 'Table/Grid', 'Read-only', 'dd-mm-yyyy', 'Theo dữ liệu', '–'),
    ('Cột Trạng thái', 'Badge', 'Read-only', '–', 'Theo dữ liệu', 'Màu theo trạng thái nhiệm vụ.'),
    ('Cột Tiến độ', 'Table/Grid', 'Read-only', '0 – 100', 'Theo dữ liệu', 'Dạng “<n>%”.'),
    ('Cột Giờ ước tính', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', '1 chữ số thập phân.'),
    ('Dòng tổng chân cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“<n> task • <h> giờ ước tính”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có nhiệm vụ phù hợp điều kiện.”'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
]
d.p('2.5.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Dòng phụ đề', 'Label', 'Hiển thị', '–', 'Chi tiết tất cả task trong kỳ', 'Chữ in hoa nhỏ.'),
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“[<mã NV>] <tên> – <chức vụ>”.'),
] + MODAL_UI, required=False)
d.p('2.5.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm số ở cột Nhiệm vụ / Giờ nhiệm vụ', 'Click',
     'After:\n– Mở cửa sổ với toàn bộ nhiệm vụ của nhân viên đã tải trong báo cáo (không gọi thêm dữ liệu).'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Xem chi tiết nhiệm vụ theo dự án')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='detail')
d.intro_table(
    ten='Xem chi tiết nhiệm vụ theo dự án',
    mota='Bấm một thanh nhiệm vụ trên lịch Gantt để xem các nhiệm vụ của nhân viên đó thuộc cùng dự án với thanh '
         'vừa bấm.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Lịch Gantt đang hiển thị và nhân viên có nhiệm vụ trong kỳ.',
    chinh='1. Người dùng bấm một thanh nhiệm vụ trên lịch Gantt.\n'
          '2. Hệ thống mở cửa sổ “Chi tiết task theo dự án trong kỳ” với tiêu đề “<Tên nhân viên> – <Tên dự án>”.\n'
          '3. Cửa sổ liệt kê các nhiệm vụ của nhân viên thuộc dự án đó trong kỳ.\n'
          '4. Người dùng bấm “Đóng” hoặc dấu × để đóng.',
    phu='• Nhiệm vụ không gắn dự án → cửa sổ liệt kê các nhiệm vụ cũng không gắn dự án của nhân viên.')
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Thanh nhiệm vụ trên lịch Gantt', shot=shot('06-chi-tiet-du-an.png'),
         shot_caption='Cửa sổ chi tiết nhiệm vụ theo dự án')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Dòng phụ đề', 'Label', 'Hiển thị', '–', 'Chi tiết task theo dự án trong kỳ', 'Chữ in hoa nhỏ.'),
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“<tên nhân viên> – <tên dự án>”.'),
] + MODAL_UI, required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm thanh nhiệm vụ trên lịch Gantt', 'Click',
     'After:\n– Lọc nhiệm vụ của nhân viên theo dự án của thanh vừa bấm và mở cửa sổ.'),
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
    mota='Tải file Excel toàn bộ báo cáo theo bộ lọc đang áp dụng (mọi phòng ban, không phân trang), chi tiết tới '
         'từng nhiệm vụ.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Báo cáo đã tải và đang có dữ liệu.',
    chinh='1. Người dùng bấm “Xuất Excel”.\n'
          '2. Nút chuyển “Đang xuất...” và bị khoá.\n'
          '3. Hệ thống dựng file theo bộ lọc đang áp dụng, trong phạm vi quyền.\n'
          '4. Trình duyệt tải file “bao_cao_phan_bo_nguon_luc_theo_nhan_vien.xls”; hệ thống báo “Xuất Excel thành '
          'công”.',
    phu='• Chưa có dữ liệu → “Vui lòng tìm kiếm và có dữ liệu trước khi xuất Excel”, không xuất.\n'
        '• Lỗi → nội dung lỗi trả về hoặc “Lỗi khi xuất Excel”.',
    dacbiet='Đầu file là ảnh header của công ty người dùng đang làm việc, tiêu đề và dòng “Kỳ báo cáo: '
            'dd/mm/yyyy → dd/mm/yyyy • <n> phòng ban • <n> nhân viên • <n> nhiệm vụ”; cuối file có khối ký '
            '“Người lập”.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('09-xuat.png'),
         shot_caption='Bấm Xuất Excel — thông báo xuất thành công')
d.figure(shot('09b-file-excel.png'), 'Nội dung file Excel tải về', width_in=6.2)
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khoá, chữ “Đang xuất...” khi đang xuất.'),
    ('Phần đầu file', 'Label', 'Read-only', '–', '–', 'Theo công ty đang làm việc',
     'Header công ty + “BÁO CÁO PHÂN BỔ NGUỒN LỰC THEO NHÂN VIÊN” + dòng Kỳ báo cáo.'),
    ('Dòng tiêu đề cột', 'Table/Grid', 'Read-only', '12 cột', '–', 'Hiển thị',
     'STT · Phòng ban / Nhân viên / Nhiệm vụ · Chức vụ · Mã nhiệm vụ · Tên nhiệm vụ · Dự án · Ngày bắt đầu · '
     'Hạn hoàn thành · Trạng thái · Tiến độ · Giờ ước tính · Giờ làm / % sử dụng.'),
    ('Dòng phòng ban', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'STT 1, 2…; “Phòng: <tên>”, “Số NV: <n>”, “Tổng nhiệm vụ: <n>”, giờ nhiệm vụ / giờ làm, % sử dụng.'),
    ('Dòng nhân viên', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'STT 1.1…; “NV: <tên>”, chức vụ, trạng thái + Rảnh / Vượt tải, số nhiệm vụ, giờ nhiệm vụ / giờ làm, % sử dụng.'),
    ('Dòng nhiệm vụ', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'STT 1.1.1…; mã, tên, “<mã dự án> <tên dự án>”, ngày, trạng thái (chữ màu theo trạng thái), tiến độ, giờ.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Xuất Excel thành công” / “Vui lòng tìm kiếm và có dữ liệu trước khi xuất Excel” / “Lỗi khi xuất Excel”.'),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Không kiểm tra quyền riêng.\n'
     '– Chưa tìm kiếm hoặc báo cáo không có dữ liệu → “Vui lòng tìm kiếm và có dữ liệu trước khi xuất Excel”, '
     'dừng.\n'
     'During:\n– Thiếu Từ ngày / Đến ngày → “Vui lòng chọn khoảng thời gian (Từ ngày, Đến ngày)”.\n'
     '– Lấy bộ lọc đang áp dụng, bỏ phân trang.\n' + SCOPE_NOTE + '\n'
     'After:\n– Tải file “bao_cao_phan_bo_nguon_luc_theo_nhan_vien.xls”, hiển thị “Xuất Excel thành công”.\n'
     '– Lỗi → nội dung lỗi trả về hoặc “Lỗi khi xuất Excel”.'),
])

# ------------------------------------------------------------------ 2.8
d.h3('2.8 In báo cáo')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'In báo cáo', 'io', actor=A)
d.p('2.8.2 Giới thiệu')
d.rule_ref('- UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='In báo cáo',
    mota='Mở bản xem trước để in toàn bộ báo cáo theo bộ lọc đang áp dụng, chi tiết tới từng nhiệm vụ.',
    tacnhan='Người xem báo cáo; Người dùng đã đăng nhập',
    dieukien='Báo cáo đã tải và đang có dữ liệu.',
    chinh='1. Người dùng bấm “In báo cáo”.\n'
          '2. Hệ thống mở tab mới gồm header công ty, tiêu đề, dòng Kỳ báo cáo và bảng Phòng ban → Nhân viên → '
          'Nhiệm vụ.\n'
          '3. Người dùng bấm nút “In”.\n'
          '4. Hệ thống mở hộp thoại in của trình duyệt.',
    phu='• Chưa có dữ liệu → “Vui lòng tìm kiếm và có dữ liệu trước khi in”, không mở tab.\n'
        '• Bản xem trước không có dữ liệu → “Không có dữ liệu”.\n'
        '• Lỗi tải dữ liệu → khung đỏ hiện nội dung lỗi.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => In báo cáo => In', shot=shot('10-in.png'), shot_caption='Bản xem trước khi in')
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Không xuất hiện trên bản in.'),
    ('Header công ty', 'Label', 'Read-only', '–', '–', 'Theo công ty đang làm việc',
     'Chưa cấu hình thì dùng ảnh mặc định.'),
    ('Tiêu đề và kỳ báo cáo', 'Label', 'Read-only', '–', '–', 'Hiển thị',
     '“BÁO CÁO PHÂN BỔ NGUỒN LỰC THEO NHÂN VIÊN” + “Kỳ báo cáo: dd/mm/yyyy → dd/mm/yyyy”.'),
    ('Bảng báo cáo', 'Table/Grid', 'Read-only', '12 cột', '–', 'Theo dữ liệu',
     'STT · Phòng ban / Nhân viên / Nhiệm vụ · Chức vụ · Mã nhiệm vụ · Tên nhiệm vụ · Dự án · Ngày bắt đầu · Hạn '
     'hoàn thành · Trạng thái · Tiến độ · Giờ ước tính · % sử dụng; STT phân cấp 1 / 1.1 / 1.1.1.'),
    ('Khối ký', 'Label', 'Read-only', '–', '–', 'Hiển thị', '“Ngày ...., tháng ...., năm ....” — Người lập (Ký, họ tên).'),
    ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Khung đỏ phía trên, không in ra.'),
])
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In báo cáo', 'Click',
     'Before:\n– Chưa tìm kiếm hoặc không có dữ liệu → “Vui lòng tìm kiếm và có dữ liệu trước khi in”, dừng.\n'
     'After:\n– Mở tab mới mang theo bộ lọc đang áp dụng; tải toàn bộ dữ liệu (không phân trang).\n' + SCOPE_NOTE),
    ('Bấm In', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt.'),
])

# ==================================================== PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của báo cáo; không lặp lại các quy tắc đã có trong SRS '
           'quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi nhân viên theo quyền', [
        '– V1: mọi nhân viên. V2: nhân viên thuộc công ty đang làm việc. V3: nhân viên thuộc phòng ban hoặc bộ '
        'phận người dùng quản lý. V4: nhân viên thuộc bộ phận người dùng quản lý. Không có quyền nào: chỉ bản '
        'thân.',
        '– Có nhiều quyền thì lấy quyền rộng nhất. Áp cho cả xem, xuất Excel và in.',
    ], ['Xem báo cáo', 'Xuất Excel', 'In']),
    ('BR-02', 'Kỳ báo cáo bắt buộc', [
        '– Luôn phải có Từ ngày và Đến ngày; thiếu → “Vui lòng chọn khoảng thời gian (Từ ngày, Đến ngày)”.',
        '– Hôm nay: 1 ngày; Tuần hiện tại: Thứ Hai → Chủ nhật; Tháng hiện tại: ngày 1 → ngày cuối tháng; Tuỳ chọn: '
        'theo khoảng nhập.',
    ], ['Tìm kiếm và lọc', 'Xuất Excel', 'In']),
    ('BR-03', 'Nhiệm vụ được tính trong kỳ', [
        '– Nhiệm vụ giao cho nhân viên (người thực hiện), KHÔNG ở trạng thái Nháp hoặc Huỷ.',
        '– Giao với kỳ: Hạn hoàn thành ≥ Từ ngày VÀ Ngày bắt đầu ≤ Đến ngày.',
        '– Có chọn Dự án thì chỉ tính nhiệm vụ thuộc dự án đó.',
        '– Giờ nhiệm vụ = tổng giờ ước tính của cả nhiệm vụ (không chia theo số ngày nằm trong kỳ).',
    ], ['Xem báo cáo', 'Xuất Excel', 'In']),
    ('BR-04', 'Giờ làm định mức', [
        '– Giờ làm = tổng giờ công của các ca làm việc được phân cho nhân viên trong kỳ; bỏ qua ca chỉ dùng để '
        'ghi nhận chấm công.',
        '– Nhân viên chưa được phân ca → Giờ làm = 0.',
    ], ['Xem báo cáo', 'Xuất Excel', 'In']),
    ('BR-05', 'Công suất và trạng thái phân bổ', [
        '– % sử dụng = Giờ nhiệm vụ / Giờ làm × 100 (1 chữ số); Giờ làm = 0 → 0%.',
        '– Rảnh = Giờ làm − Giờ nhiệm vụ; Vượt tải = Giờ nhiệm vụ − Giờ làm (đều không âm).',
        '– Trạng thái: trên 100% Vượt tải (đỏ); dưới 60% Cần phân thêm nhiệm vụ (cam); 60% – 100% Phân bổ hợp lý '
        '(xanh).',
        '– Lọc Khoảng công suất: < 60%; 60% – 100% (gồm 2 đầu); > 100%.',
    ], ['Xem báo cáo', 'Tìm kiếm và lọc']),
    ('BR-06', 'Danh sách và nhóm hiển thị', [
        '– Mặc định liệt kê MỌI nhân viên trong phạm vi, kể cả không có nhiệm vụ; tích “Chỉ hiển thị nhân viên có '
        'nhiệm vụ trong kỳ” thì bỏ người không có nhiệm vụ.',
        '– Gom theo phòng ban của nhân viên (thiếu → “Chưa xác định”); phòng sắp theo tên, nhân viên sắp theo tên.',
        '– Dòng phòng ban: cộng dồn số nhân viên, nhiệm vụ, giờ làm, giờ nhiệm vụ; % sử dụng tính lại từ tổng.',
        '– Phân trang theo PHÒNG BAN (5 / 10 / 20 / 50, mặc định 10).',
    ], 'Xem báo cáo'),
    ('BR-07', 'Màu thanh Gantt', [
        '– Thanh kéo từ Ngày bắt đầu tới Hạn hoàn thành, cắt theo kỳ; thiếu một trong hai ngày thì không vẽ.',
        '– Đỏ (Quá hạn): hạn trước hôm nay và chưa ở trạng thái Hoàn thành. Cam (Sát deadline): hạn đúng hôm nay '
        'và chưa Hoàn thành. Còn lại xanh (Bình thường).',
    ], 'Xem / ẩn lịch Gantt'),
    ('BR-08', 'Xuất Excel và In', [
        '– Chỉ cho xuất / in khi đã có dữ liệu trên màn.',
        '– Lấy toàn bộ phòng ban theo bộ lọc đang áp dụng, không phân trang, chi tiết tới từng nhiệm vụ.',
        '– Header lấy theo công ty người dùng đang làm việc; chưa cấu hình dùng ảnh mặc định.',
    ], ['Xuất Excel', 'In']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

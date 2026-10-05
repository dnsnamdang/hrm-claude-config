# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo Theo dõi YCLGP theo phòng KD.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/report/solution-requests-by-department/{index.vue, print.vue,
      components/SolutionRequestsTable.vue, components/StatusSummaryModal.vue}
      components/V2BaseSmartFilterPanel.vue · components/modal/filter-customization-modal.vue
      components/subsystem-menu/presale.js (lối vào DUY NHẤT)
  BE  Modules/Assign/Routes/api.php (nhóm assign/report/solution-requests-by-department — không gắn checkPermission)
      SolutionRequestsByDepartmentReportController · Services/Report/SolutionRequestsByDepartmentReportService
      App/ExcelExport/SolutionRequestsByDepartmentReportExport + exports/solution_requests_by_department_report.blade.php
  Quyền: PermissionsTableSeeder id 1063–1065 (nhóm "Báo cáo theo dõi giải pháp theo phòng KD")
Ảnh chụp thật (headless 1440x900, client :3002): shots/ — chỉ để local.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.claude/skills/srs-documenter/assets')
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(HERE, 'shots')


def shot(name):
    return os.path.join(SHOTS, name)


TEN_MAN = 'Báo cáo Theo dõi YCLGP theo phòng KD'
MENU = 'Phân hệ CSKH trước bán => Báo cáo => Báo cáo dự án tiền khả thi => Theo dõi YCLGP theo phòng KD'
ACTOR = 'Người xem báo cáo'
TACNHAN = 'Nhân viên / quản lý kinh doanh; Người dùng đã đăng nhập'
DK = 'Người dùng đã đăng nhập (menu không giới hạn quyền). Dữ liệu hiển thị theo phạm vi ở Phần 2.'

d = SrsDoc(out=os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN), menu=MENU, route='', full_url='',
           img_prefix='yclgp_')
d.set_menu_icons({k: shot(v) for k, v in {
    'Phân hệ CSKH trước bán': 'icon_phanhe.png',
    'Báo cáo': 'icon_baocao.png',
    'Báo cáo dự án tiền khả thi': 'icon_nhom.png',
    'Theo dõi YCLGP theo phòng KD': 'icon_muc.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Xem chi tiết': 'icon_xemct.png',
    'Thu gọn': 'icon_thugon.png',
    'Cơ cấu': 'icon_cocau.png',
    'Xuất Excel': 'icon_xuat.png',
    'In danh sách': 'icon_in.png',
}.items()})
d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Báo cáo theo dõi yêu cầu làm giải pháp (YCLGP) theo '
    'phòng kinh doanh, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu các chức năng xem, lọc, xem cơ cấu tiến trình, xuất Excel và in của báo cáo.',
    'Làm rõ cách hệ thống gom yêu cầu làm giải pháp theo cấp Công ty → Phòng ban → Nhân viên kinh doanh '
    '(người gửi yêu cầu) → Yêu cầu.',
    'Làm rõ phạm vi dữ liệu mỗi người dùng được xem và cách tính kỳ báo cáo.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('YCLGP / YC GP', 'Yêu cầu làm giải pháp — phiếu nhân viên kinh doanh gửi phòng giải pháp để xây dựng '
                      'giải pháp cho dự án tiền khả thi.'),
    ('NVKD', 'Nhân viên kinh doanh — người lập và gửi yêu cầu làm giải pháp.'),
    ('Dự án TKT', 'Dự án tiền khả thi gắn với yêu cầu.'),
    ('Phòng tiếp nhận', 'Phòng được chỉ định xử lý yêu cầu (cũng là phòng làm giải pháp).'),
    ('PM làm GP', 'Người phụ trách xây dựng giải pháp cho yêu cầu.'),
    ('Tiến trình yêu cầu', 'Trạng thái của yêu cầu: Nháp, Chờ tiếp nhận, Yêu cầu bổ sung, Đã tiếp nhận, Từ chối, '
                           'Đang thực hiện, Đã hoàn thành, Đã hủy, Đóng, Đã chốt giải pháp.'),
    ('Cơ cấu', 'Bảng thống kê số yêu cầu và tỷ lệ % theo từng tiến trình của một cấp.'),
    ('Ngày gửi YC', 'Thời điểm yêu cầu được gửi đi; là mốc lọc kỳ báo cáo.'),
], widths=[1.6, 4.4])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('–', 'Không có quyền thao tác riêng',
     'Menu “Theo dõi YCLGP theo phòng KD” hiển thị cho mọi người dùng đã đăng nhập; mọi chức năng (xem, lọc, '
     'cơ cấu, xuất Excel, in) dùng chung phạm vi dữ liệu ở bảng dưới.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem báo cáo theo dõi giải pháp theo phòng KD theo tổng công ty',
     'Toàn bộ yêu cầu làm giải pháp của mọi công ty.'),
    ('V2', 'Xem báo cáo theo dõi giải pháp theo phòng KD theo công ty',
     'Yêu cầu do nhân viên thuộc công ty đang làm việc gửi, cộng yêu cầu do chính mình tạo.'),
    ('V3', 'Xem báo cáo theo dõi giải pháp theo phòng KD theo phòng ban',
     'Yêu cầu do nhân viên thuộc phòng ban / bộ phận mình quản lý gửi, cộng yêu cầu do chính mình tạo.'),
    ('–', 'Không có quyền nào ở trên', 'Chỉ yêu cầu do chính mình tạo.'),
], widths=[0.8, 2.6, 2.6])
d.p('Có nhiều quyền thì áp phạm vi rộng nhất theo thứ tự V1 → V2 → V3. Phạm vi xét theo phòng ban / công ty '
    'của NGƯỜI GỬI yêu cầu, không theo phòng tiếp nhận.')
d.p('Lưu ý hiện trạng: phần kiểm tra phạm vi đang đối chiếu tên quyền thiếu cụm “theo dõi” (“Xem báo cáo giải '
    'pháp theo phòng KD theo …”) nên không khớp 3 quyền V1–V3 đã khai báo; trên thực tế mọi người dùng, kể cả '
    'được cấp V1–V3, hiện chỉ thấy yêu cầu do chính mình tạo.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'V1', 'V2', 'V3', 'Không có quyền nào'], [
    ('FR-01 Xem báo cáo', '✅', '✅', '✅', '✅ (YC của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅ (YC của mình)'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅'),
    ('FR-04 Xem chi tiết / Thu gọn toàn bộ', '✅', '✅', '✅', '✅ (YC của mình)'),
    ('FR-05 Xem cơ cấu tiến trình yêu cầu', '✅', '✅', '✅', '✅ (YC của mình)'),
    ('FR-06 Xuất Excel', '✅', '✅', '✅', '✅ (YC của mình)'),
    ('FR-07 In danh sách', '✅', '✅', '✅', '✅ (YC của mình)'),
], widths=[2.6, 0.6, 0.6, 0.6, 1.6])

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR, [0, 1, 2])],
    [('FR-01', 'Xem báo cáo', 'view'),
     ('FR-06', 'Xuất Excel', 'io'),
     ('FR-07', 'In danh sách', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Xem chi tiết / Thu gọn', 'view', 'extend', [0], None),
     ('FR-05', 'Xem cơ cấu tiến trình', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1 Xem bao cao
d.h3('2.1 Xem báo cáo')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Phân trang và UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả '
           'chi tiết.', anchor='list')
d.intro_table(
    ten='Xem báo cáo theo dõi YCLGP theo phòng KD',
    mota='Hiển thị bảng phân cấp Công ty → Phòng ban → Nhân viên kinh doanh → Yêu cầu làm giải pháp của kỳ báo '
         'cáo, kèm dòng tổng và số lượng ở từng cấp. Mặc định kỳ là tháng hiện tại.',
    tacnhan=TACNHAN,
    dieukien=DK,
    chinh='1. Người dùng mở báo cáo.\n'
          '2. Hệ thống nạp danh sách dự án TKT cho ô lọc, rồi nạp dữ liệu báo cáo của tháng hiện tại.\n'
          '3. Bảng hiển thị dòng “Tổng toàn bộ yêu cầu” và các dòng Công ty ở trạng thái thu gọn.\n'
          '4. Người dùng bấm mũi tên (hoặc tên) ở dòng Công ty → Phòng ban → Nhân viên để mở cấp con; dòng Nhân '
          'viên mở ra danh sách yêu cầu.\n'
          '5. Người dùng chuyển trang / đổi số dòng mỗi trang để xem tiếp.',
    phu='• Không có yêu cầu nào trong phạm vi → bảng hiện “Không có dữ liệu.”.\n'
        '• Lỗi khi tải → thông báo “Lỗi khi tải dữ liệu”.\n'
        '• Đóng một cấp → mọi cấp con bên trong cũng đóng lại.\n'
        '• Chuyển trang hoặc đổi số dòng → mọi cấp đang mở được thu gọn lại.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-view.png'), shot_caption='Báo cáo lúc mới mở (chế độ thu gọn)')
d.figure(shot('02-expand.png'), 'Mở lần lượt Công ty → Phòng ban → Nhân viên để xem từng yêu cầu', width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Báo cáo theo dõi yêu cầu làm giải pháp theo phòng kinh doanh',
     'Kèm biểu tượng ⓘ: “Thống kê số lượng Yêu cầu làm giải pháp theo Công ty → Phòng ban → Nhân viên kinh '
     'doanh, theo dõi tiến trình xử lý các yêu cầu đó.”'),
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Bảng chi tiết yêu cầu làm giải pháp',
     'Biểu tượng ⓘ: “Click mũi tên để mở/đóng cấp con. Click chip ở cột Tiến trình yêu cầu để xem popup cơ '
     'cấu tiến trình.”'),
    ('Nút Xem chi tiết / Thu gọn, Xuất Excel, In danh sách', 'Button', 'Enable', '–', 'Hiển thị',
     'Xem FR-04, FR-06, FR-07.'),
    ('Dòng Tổng toàn bộ yêu cầu', 'Table/Grid', 'Read-only', '–', 'Hiển thị khi có dữ liệu',
     '“<a> công ty • <b> phòng ban • <c> NVKD • <d> yêu cầu GP” + chip Cơ cấu (FR-05).'),
    ('Dòng Công ty', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Tên công ty của người gửi; dòng phụ “<n> phòng • <n> NV • <n> YC”; chip Cơ cấu.'),
    ('Dòng Phòng ban', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Phòng ban của người gửi; dòng phụ “<n> NV • <n> YC”; chip Cơ cấu.'),
    ('Dòng Nhân viên kinh doanh', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Tên người gửi; dòng phụ “Mã: <mã NV> • <n> YC”; chip Cơ cấu.'),
    ('Nút mũi tên mở / đóng cấp', 'Icon Button', 'Enable', '–', 'Mũi tên sang phải',
     'Đang mở → mũi tên xuống. Bấm vào tên dòng cũng mở / đóng.'),
    ('STT', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Đánh lại từ 1 trong từng nhân viên.'),
    ('Công ty / Phòng / NV / Yêu cầu', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng yêu cầu: mã yêu cầu, dòng dưới là tiêu đề yêu cầu.'),
    ('Nhân viên yêu cầu', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Người gửi yêu cầu.'),
    ('Ngày gửi YC', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Trống hiển thị “—”.'),
    ('Tiến trình yêu cầu', 'Badge', 'Read-only', '10 giá trị', 'Theo dữ liệu',
     'Chữ và màu theo tiến trình của yêu cầu.'),
    ('Ngày KH cần GP', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Ngày khách hàng cần giải pháp.'),
    ('Tên dự án TKT', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Khách hàng (người liên hệ)', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Tên khách hàng của dự án; dòng dưới là người liên hệ.'),
    ('Giai đoạn dự án TKT', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Giai đoạn hiện tại của dự án.'),
    ('Phòng tiếp nhận', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Người tiếp nhận', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('PM làm GP', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Mã giải pháp', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Mã giải pháp lập gần nhất từ yêu cầu.'),
    ('Ngày chốt giải pháp cuối', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '–'),
    ('Thanh cuộn ngang trên / dưới', 'Scrollbar', 'Enable', '–', 'Hiển thị khi bảng tràn', 'Cuộn đồng bộ 2 thanh.'),
    ('Đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu...”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu.”.'),
    ('Thông tin phân trang', 'Text', 'Hiển thị', '–', 'Theo dữ liệu', '“Hiển thị <a>–<b> / <N> nhân viên”.'),
    ('Số dòng/trang', 'Dropdown', 'Enable', '10 / 20 / 50 / 100', '50', '–'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', '–'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở báo cáo', 'System',
     'After:\n– Nạp danh sách dự án TKT cho ô lọc Dự án tiền khả thi.\n'
     '– Nạp dữ liệu báo cáo với kỳ mặc định: tháng hiện tại, năm hiện tại, trang 1, 50 dòng/trang.\n'
     '– Áp phạm vi dữ liệu theo Phần 2.\n– Lỗi → “Lỗi khi tải dữ liệu”.'),
    ('Bấm mũi tên / tên dòng Công ty, Phòng ban, Nhân viên', 'Click',
     'After:\n– Đang đóng → mở cấp con ngay dưới dòng.\n– Đang mở → đóng cấp đó và mọi cấp con bên trong.'),
    ('Chọn trang', 'Click', 'After:\n– Thu gọn mọi cấp đang mở, nạp dữ liệu trang được chọn.'),
    ('Đổi Số dòng/trang', 'Change', 'After:\n– Về trang 1, thu gọn mọi cấp, nạp lại dữ liệu.'),
])

# ------------------------------------------------------------------ 2.2 Loc
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả '
           'chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc báo cáo',
    mota='Lọc báo cáo theo kỳ thời gian (theo ngày gửi yêu cầu), tổ chức của người gửi, nhân viên kinh doanh, '
         'nhóm ngành – nhóm giải pháp – ứng dụng, dự án TKT, khách hàng và tiến trình yêu cầu.',
    tacnhan=TACNHAN,
    dieukien=DK,
    chinh='1. Người dùng bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
          '2. Người dùng chọn điều kiện lọc.\n'
          '3. Với ô Xem theo thời gian, Tháng, Năm, Ngày gửi yêu cầu, Dự án tiền khả thi, Tiến trình YC: chọn xong '
          'hệ thống tìm ngay.\n'
          '4. Với các ô còn lại: người dùng bấm “Tìm kiếm”.\n'
          '5. Hệ thống nạp lại báo cáo từ trang 1.',
    phu='• Bấm “Làm mới” → trả mọi ô về mặc định (Tháng hiện tại / Năm hiện tại), xoá ô Khách hàng, nạp lại báo cáo.\n'
        '• Đổi “Xem theo thời gian” → các ô thời gian không còn hiển thị bị xoá giá trị.\n'
        '• Ô Khách hàng gõ dưới 2 ký tự → không gợi ý.\n'
        '• Bấm “Ẩn tìm kiếm nâng cao” → thu khối lọc lại, giữ nguyên điều kiện đang lọc.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('03-filter.png'),
         shot_caption='Khối Tìm kiếm nâng cao đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang thu gọn',
     'Bật / tắt khối lọc.'),
    ('Xem theo thời gian', 'Dropdown', 'Enable', 'Tuỳ chỉnh / Tháng / Năm', 'Có', 'Tháng',
     'Không cho xoá trống. Quyết định các ô thời gian hiển thị.'),
    ('Tháng', 'Dropdown', 'Enable / Ẩn', 'Tháng 1 – Tháng 12', 'Có', 'Tháng hiện tại',
     'Chỉ hiện khi Xem theo = Tháng.'),
    ('Năm', 'Dropdown', 'Enable / Ẩn', 'Năm hiện tại − 5 → năm hiện tại + 1', 'Có', 'Năm hiện tại',
     'Hiện khi Xem theo = Tháng hoặc Năm.'),
    ('Ngày gửi yêu cầu', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy – dd/mm/yyyy', 'Không', 'Trống',
     'Khoảng ngày trong 1 ô; chỉ hiện khi Xem theo = Tuỳ chỉnh.'),
    ('Công ty', 'Dropdown', 'Enable', 'Danh sách công ty', 'Không', 'Trống',
     'Công ty của người gửi yêu cầu. Biểu tượng ổ khoá ở nhãn: bật / tắt hiện cả công ty đã khoá.'),
    ('Phòng ban tiếp nhận', 'Dropdown', 'Enable', 'Danh sách theo công ty', 'Không', 'Trống',
     'Lọc theo phòng ban của NGƯỜI GỬI yêu cầu (nhãn ghi “tiếp nhận”). Có ổ khoá hiện cả phòng đã khoá.'),
    ('Bộ phận tiếp nhận', 'Dropdown', 'Enable', 'Danh sách theo phòng ban', 'Không', 'Trống',
     'Lọc theo bộ phận của người gửi. Có ổ khoá hiện cả bộ phận đã khoá.'),
    ('Nhân viên kinh doanh', 'Dropdown', 'Disable / Enable', 'Danh sách nhân viên', 'Không', 'Khoá',
     'Chỉ mở khi đã chọn Bộ phận.'),
    ('Nhóm ngành', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Theo nhóm ngành của dự án TKT. Xoá → xoá luôn Nhóm giải pháp, Ứng dụng.'),
    ('Nhóm giải pháp', 'Dropdown', 'Enable', 'Danh sách theo nhóm ngành', 'Không', 'Trống',
     'Xoá → xoá luôn Ứng dụng.'),
    ('Ứng dụng', 'Dropdown', 'Enable', 'Danh sách theo nhóm giải pháp', 'Không', 'Trống', '–'),
    ('Dự án tiền khả thi', 'Dropdown', 'Enable', 'Danh sách dự án TKT', 'Không', 'Trống',
     'Hiển thị “<mã> - <tên>”. Đã chọn Khách hàng → chỉ còn dự án của khách hàng đó.'),
    ('Khách hàng', 'Textbox', 'Enable', '≥ 2 ký tự', 'Không', 'Trống',
     'Gõ tên hoặc mã → danh sách gợi ý “<tên> / <mã> • <SĐT>”; “Đang tìm...”, “Không tìm thấy khách hàng”. '
     'Chọn 1 dòng để lọc; Enter = Tìm kiếm; Esc hoặc bấm ra ngoài → đóng gợi ý.'),
    ('Tiến trình YC', 'Dropdown', 'Enable', 'Danh sách 8 giá trị', 'Không', 'Trống',
     'Chờ tiếp nhận, Đã tiếp nhận, Từ chối, Đang thực hiện, Đã hoàn thành, Yêu cầu bổ sung, Đóng, '
     'Đã chốt giải pháp.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Nạp lại báo cáo từ trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Trả bộ lọc về mặc định và nạp lại.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Đổi Xem theo thời gian / Tháng / Năm / Ngày gửi yêu cầu / Dự án / Tiến trình YC', 'Change',
     'After:\n– Đổi Xem theo: Tuỳ chỉnh → xoá Tháng, Năm; Tháng / Năm → xoá khoảng ngày; Năm → xoá Tháng.\n'
     '– Quy đổi kỳ: Tháng = ngày 1 → ngày cuối tháng; Năm = 01/01 → 31/12; Tuỳ chỉnh = khoảng ngày đã chọn '
     '(trống = không giới hạn).\n– Về trang 1 và nạp lại báo cáo.'),
    ('Gõ ô Khách hàng', 'Keypress',
     'During:\n– Dưới 2 ký tự → ẩn gợi ý.\nAfter:\n– Tìm khách hàng theo tên / mã, hiện danh sách gợi ý.'),
    ('Chọn khách hàng trong gợi ý', 'Click',
     'After:\n– Ghi nhận khách hàng lọc, điền tên vào ô, đóng gợi ý; danh sách Dự án tiền khả thi chỉ còn dự án '
     'của khách hàng đó. Báo cáo chưa nạp lại tới khi bấm Tìm kiếm.'),
    ('Bấm Tìm kiếm / Enter ở ô Khách hàng', 'Click',
     'After:\n– Về trang 1, nạp lại báo cáo theo toàn bộ điều kiện đang chọn.\n– Lỗi → “Lỗi khi tải dữ liệu”.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Trả mọi ô về mặc định, xoá ô Khách hàng, về trang 1, nạp lại báo cáo.'),
])

# ------------------------------------------------------------------ 2.3 Cai dat bo loc
d.h3('2.3 Cài đặt bộ lọc')
d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc', 'view', actor=ACTOR)
d.p('2.3.2 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Cho người dùng chọn trường lọc nào được hiển thị trong khối Tìm kiếm nâng cao và sắp xếp thứ tự. Cấu '
         'hình lưu riêng cho màn báo cáo này.',
    tacnhan=TACNHAN,
    dieukien='Người dùng đã đăng nhập.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
          '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” với 9 trường lọc theo cấu hình đã lưu.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm “Lưu”.\n'
          '5. Hệ thống lưu cấu hình, đóng cửa sổ, báo “Cập nhật thành công”.',
    phu='• Bấm “Khôi phục mặc định” → danh sách trở về thứ tự gốc, hiện đủ trường (chưa lưu tới khi bấm Lưu).\n'
        '• Bấm “Đóng” / dấu × → đóng, không lưu.\n'
        '• Lỗi khi lưu → “Thao tác thất bại”.',
    dacbiet='Trường bị ẩn đang có giá trị lọc thì giá trị đó bị xoá, tránh lọc ngầm bằng trường không nhìn thấy.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', modal='Cài đặt bộ lọc', shot=shot('05-config.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
    ('Danh sách trường lọc', 'Checkbox', 'Enable', '9 trường', '–', 'Theo cấu hình đã lưu',
     'Xem theo thời gian; Tháng; Năm; Công ty – Phòng ban tiếp nhận – Bộ phận tiếp nhận; Nhân viên kinh doanh; '
     'Nhóm ngành – Nhóm giải pháp – Ứng dụng; Dự án tiền khả thi; Khách hàng; Tiến trình YC. Không có trường bị khoá.'),
    ('Biểu tượng kéo ⠿', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo thả để đổi thứ tự.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Enable', 'Khoá trong lúc đang lưu.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở cửa sổ với danh sách trường theo cấu hình đã lưu của màn.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Đưa danh sách về thứ tự gốc, tích đủ mọi trường (chưa lưu).'),
    ('Bấm Lưu', 'Click',
     'After:\n– Lưu cấu hình hiển thị / thứ tự cho người dùng ở màn báo cáo này.\n'
     '– Xoá giá trị lọc của trường bị ẩn.\n– Đóng cửa sổ, hiển thị “Cập nhật thành công”.\n'
     '– Lỗi → “Thao tác thất bại”.'),
    ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng cửa sổ, không lưu.'),
])

# ------------------------------------------------------------------ 2.4 Xem chi tiet / Thu gon
d.h3('2.4 Xem chi tiết / Thu gọn toàn bộ')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Xem chi tiết / Thu gọn toàn bộ',
    mota='Mở bung một lần mọi cấp (Công ty, Phòng ban, Nhân viên) của trang đang xem để thấy toàn bộ yêu cầu, '
         'hoặc thu gọn tất cả về cấp Công ty.',
    tacnhan=TACNHAN,
    dieukien=DK,
    chinh='1. Người dùng bấm “Xem chi tiết”.\n'
          '2. Hệ thống mở mọi cấp của trang hiện tại; nút đổi thành “Thu gọn”.\n'
          '3. Người dùng bấm “Thu gọn” → mọi cấp đóng lại, nút trở về “Xem chi tiết”.',
    phu='• Chuyển trang / đổi số dòng sau khi Xem chi tiết → các cấp bị thu gọn, nút vẫn ở trạng thái “Thu gọn”.')
d.p('2.4.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('04-detail.png'),
         shot_caption='Bảng sau khi bấm Xem chi tiết (mọi cấp mở)')
d.figure(shot('04b-detail-right.png'), 'Các cột bên phải của bảng: Người tiếp nhận, PM làm GP, Mã giải pháp, '
         'Ngày chốt giải pháp cuối', width_in=6.2)
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xem chi tiết', 'Button', 'Enable', '–', 'Hiển thị (nền xanh)', 'Biểu tượng con mắt.'),
    ('Nút Thu gọn', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Thay chỗ nút Xem chi tiết khi đang mở toàn bộ.'),
    ('Dòng yêu cầu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Đủ 14 cột như mô tả ở FR-01.'),
], required=False)
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xem chi tiết', 'Click', 'After:\n– Mở mọi dòng Công ty, Phòng ban, Nhân viên của trang đang xem.'),
    ('Bấm Thu gọn', 'Click', 'After:\n– Đóng mọi cấp đang mở.'),
])

# ------------------------------------------------------------------ 2.5 Co cau
d.h3('2.5 Xem cơ cấu tiến trình yêu cầu')
d.p('2.5.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='detail')
d.intro_table(
    ten='Xem cơ cấu tiến trình yêu cầu',
    mota='Mở cửa sổ thống kê số yêu cầu và tỷ lệ % theo từng tiến trình cho cấp được chọn: toàn bộ, một công ty, '
         'một phòng ban hoặc một nhân viên kinh doanh.',
    tacnhan=TACNHAN,
    dieukien=DK,
    chinh='1. Người dùng bấm chip “Cơ cấu (<n> YC)” ở cột Tiến trình yêu cầu của dòng Tổng / Công ty / Phòng ban / '
          'Nhân viên.\n'
          '2. Hệ thống mở cửa sổ “Cơ cấu tiến trình yêu cầu GP”, dòng phụ đề ghi cấp đang xem.\n'
          '3. Hệ thống đếm yêu cầu theo tiến trình trong phạm vi cấp đó và điều kiện lọc, hiển thị bảng.\n'
          '4. Người dùng bấm “Đóng”.',
    phu='• Tiến trình không có yêu cầu nào → không hiện dòng đó.\n'
        '• Không có yêu cầu → “Không có dữ liệu.”.\n'
        '• Lỗi → hiển thị nội dung lỗi trả về hoặc “Lỗi khi tải dữ liệu”.')
d.p('2.5.2 Layout màn hình')
d.layout(menu=MENU + ' => Cơ cấu', modal='Cơ cấu tiến trình yêu cầu GP', shot=shot('06-status.png'),
         shot_caption='Cửa sổ Cơ cấu tiến trình yêu cầu GP (mở từ dòng Tổng toàn bộ yêu cầu)')
d.p('2.5.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Chip Cơ cấu (<n> YC)', 'Button', 'Enable', '–', 'Hiển thị ở dòng Tổng, Công ty, Phòng ban, Nhân viên',
     '<n> là số yêu cầu của dòng.'),
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Cơ cấu tiến trình yêu cầu GP', '–'),
    ('Phụ đề', 'Label', 'Hiển thị', '–', 'Theo dòng bấm',
     '“Tổng toàn bộ yêu cầu làm giải pháp” / “Công ty: <tên>” / “Phòng ban: <tên>” / “Nhân viên: <tên>”.'),
    ('#', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Số thứ tự.'),
    ('Tiến trình yêu cầu', 'Badge', 'Read-only', '10 giá trị', 'Theo dữ liệu', 'Chữ và màu theo tiến trình.'),
    ('Số yêu cầu', 'Number', 'Read-only', '≥ 1', 'Theo dữ liệu', 'Ngăn cách hàng nghìn bằng dấu phẩy.'),
    ('Tỷ lệ (%)', 'Number', 'Read-only', '0 – 100', 'Theo dữ liệu', '1 chữ số thập phân, vd 30.0%.'),
    ('Dòng tổng', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Tổng: <n> yêu cầu làm giải pháp”.'),
    ('Đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu...”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu.”.'),
    ('Nút Đóng / ×', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)
d.p('2.5.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm chip Cơ cấu', 'Click',
     'Before:\n– Áp phạm vi dữ liệu theo Phần 2.\nAfter:\n– Mở cửa sổ, đếm yêu cầu theo tiến trình trong cấp được '
     'chọn với điều kiện lọc đang có; tỷ lệ = số yêu cầu / tổng × 100, làm tròn 1 chữ số.\n'
     '– Lỗi → nội dung lỗi trả về hoặc “Lỗi khi tải dữ liệu”.'),
    ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ------------------------------------------------------------------ 2.6 Xuat Excel
d.h3('2.6 Xuất Excel')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Xuất Excel báo cáo', 'io', actor=ACTOR)
d.p('2.6.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='Xuất Excel báo cáo',
    mota='Tải về file Excel toàn bộ báo cáo (không chia trang) theo điều kiện lọc, giữ cấu trúc phân cấp.',
    tacnhan=TACNHAN,
    dieukien=DK,
    chinh='1. Người dùng bấm “Xuất Excel”.\n'
          '2. Hệ thống dựng file từ toàn bộ dữ liệu trong phạm vi và điều kiện lọc.\n'
          '3. Trình duyệt tải về file “bao_cao_giai_phap_theo_phong_kd.xls”.\n'
          '4. Hệ thống báo “Xuất Excel thành công”.',
    phu='• Lỗi → “Lỗi khi xuất Excel”.',
    dacbiet='Nội dung file: ảnh đầu trang (letterhead) của công ty đang làm việc; tiêu đề “BÁO CÁO THEO DÕI LÀM '
            'GIẢI PHÁP THEO PHÒNG KINH DOANH”; 14 cột; dòng Công ty / Phòng ban / NVKD tô màu và cột Tiến trình ghi '
            'số yêu cầu theo từng tiến trình; cuối file có ô “Ngày ..., tháng ..., năm ... / Người lập / (Ký, họ tên)”.')
d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('07-export.png'),
         shot_caption='Bấm Xuất Excel — file được tải về và hiện thông báo thành công')
d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xuất Excel', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Biểu tượng file Excel, góc phải tiêu đề bảng.'),
    ('Cột STT', 'Text', 'Read-only', '1 / 1.1 / 1.1.1 / 1.1.1.1', '–', 'Theo dữ liệu', 'Đánh số theo cấp.'),
    ('Cột Mã yêu cầu / Nhóm', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
     '“Công ty: …” / “Phòng ban: …” / “NVKD: …” / “<mã> — <tiêu đề>”.'),
    ('Cột Nhân viên yêu cầu, Ngày gửi YC, Tiến trình yêu cầu, Ngày KH cần GP', 'Text', 'Read-only',
     'Ngày dd/mm/yyyy', '–', 'Theo dữ liệu', 'Dòng nhóm: cột Tiến trình liệt kê “<tiến trình>: <số>”.'),
    ('Cột Mã/Tên dự án TKT, Khách hàng (người liên hệ), Giai đoạn dự án TKT', 'Text', 'Read-only', '–', '–',
     'Theo dữ liệu', 'Khách hàng ghi “<tên> (<người liên hệ>)”.'),
    ('Cột Phòng tiếp nhận, Người tiếp nhận, PM làm GP, Mã giải pháp, Ngày chốt GP cuối', 'Text', 'Read-only',
     '–', '–', 'Theo dữ liệu', 'Trống ghi “—”.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '“Xuất Excel thành công” / “Lỗi khi xuất Excel”.'),
])
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Áp phạm vi dữ liệu theo Phần 2.\nDuring:\n– Lấy toàn bộ dữ liệu theo điều kiện lọc (bỏ phân trang).\n'
     'After:\n– Tải file “bao_cao_giai_phap_theo_phong_kd.xls”.\n– Hiển thị “Xuất Excel thành công”.\n'
     '– Lỗi → “Lỗi khi xuất Excel”.'),
])

# ------------------------------------------------------------------ 2.7 In
d.h3('2.7 In danh sách')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'In danh sách báo cáo', 'io', actor=ACTOR)
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='In danh sách báo cáo',
    mota='Mở trang in ở tab mới với toàn bộ báo cáo theo điều kiện lọc, khổ A4 ngang.',
    tacnhan=TACNHAN,
    dieukien=DK,
    chinh='1. Người dùng bấm “In danh sách”.\n'
          '2. Hệ thống mở tab mới, nạp toàn bộ dữ liệu (không chia trang) và hiển thị bản xem trước.\n'
          '3. Người dùng bấm nút “In” trên trang.\n'
          '4. Hệ thống mở hộp thoại in của trình duyệt với khổ A4 ngang.',
    phu='• Lỗi khi nạp dữ liệu → khung đỏ ghi nội dung lỗi hoặc “Lỗi không xác định khi tải dữ liệu báo cáo”.\n'
        '• Không có dữ liệu → bảng ghi “Không có dữ liệu”.',
    dacbiet='Trang in gồm: ảnh đầu trang của công ty đang làm việc (thiếu thì dùng ảnh mặc định), tiêu đề “BÁO CÁO '
            'THEO DÕI LÀM GIẢI PHÁP THEO PHÒNG KINH DOANH”, bảng 14 cột phân cấp giống file Excel, ô ký “Người lập”.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => In danh sách', shot=shot('08-print.png'), shot_caption='Trang in mở ở tab mới')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In danh sách', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Góc phải tiêu đề bảng ở màn báo cáo.'),
    ('Nút In', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đầu trang in; không xuất hiện trên bản in.'),
    ('Ảnh đầu trang', 'Image', 'Hiển thị', '–', '–', 'Letterhead công ty đang làm việc', '–'),
    ('Tiêu đề', 'Label', 'Hiển thị', '–', '–', 'BÁO CÁO THEO DÕI LÀM GIẢI PHÁP THEO PHÒNG KINH DOANH', '–'),
    ('Bảng 14 cột', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'STT; Mã yêu cầu / Nhóm; Nhân viên yêu cầu; Ngày gửi YC; Tiến trình yêu cầu; Ngày KH cần GP; Tên dự án TKT; '
     'Khách hàng; Giai đoạn dự án TKT; Phòng tiếp nhận; Người tiếp nhận; PM làm GP; Mã giải pháp; Ngày chốt giải '
     'pháp cuối. Dòng nhóm tô màu, cột Tiến trình liệt kê số yêu cầu theo tiến trình.'),
    ('Ô ký', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Ngày ...., tháng ...., năm .... / Người lập / (Ký, họ tên)”.'),
    ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Khung đỏ phía trên, không in ra.'),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In danh sách', 'Click',
     'After:\n– Mở tab mới, mang theo điều kiện lọc hiện tại.\n– Áp phạm vi dữ liệu theo Phần 2, nạp toàn bộ '
     'dữ liệu.\n– Lỗi → khung đỏ “<nội dung lỗi>” hoặc “Lỗi không xác định khi tải dữ liệu báo cáo”.'),
    ('Bấm In', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt, khổ A4 ngang, lề 8mm × 6mm.'),
])

# ==================================================== PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của báo cáo; không lặp lại các quy tắc đã có trong SRS quy '
           'tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phân cấp theo người gửi yêu cầu', [
        '– Công ty và Phòng ban trên báo cáo là công ty / phòng ban của NHÂN VIÊN GỬI yêu cầu, không phải phòng '
        'tiếp nhận.',
        '– Ô lọc Công ty, Phòng ban tiếp nhận, Bộ phận tiếp nhận cũng lọc theo tổ chức của người gửi.',
        '– Sắp xếp: tên công ty → tên phòng ban → tên nhân viên → ngày gửi mới nhất trước.',
    ], ['Xem báo cáo', 'Tìm kiếm và lọc']),
    ('BR-02', 'Kỳ báo cáo theo Ngày gửi YC', [
        '– Mặc định: tháng hiện tại. Tháng = ngày 1 → ngày cuối tháng; Năm = 01/01 → 31/12.',
        '– Tuỳ chỉnh để trống khoảng ngày thì không giới hạn thời gian (khi đó gồm cả yêu cầu Nháp chưa gửi).',
        '– Lưu ý hiện trạng: cửa sổ Cơ cấu, Xuất Excel và In đang chỉ nhận khoảng ngày của chế độ Tuỳ chỉnh; với '
        'chế độ Tháng / Năm, 3 chức năng này lấy mọi thời gian (số liệu có thể lớn hơn bảng trên màn).',
    ], ['Xem báo cáo', 'Tìm kiếm và lọc', 'Xem cơ cấu', 'Xuất Excel', 'In danh sách']),
    ('BR-03', 'Phân trang theo nhân viên', [
        '– Không tách yêu cầu của một nhân viên sang 2 trang: một trang chứa trọn các nhân viên sao cho tổng yêu '
        'cầu không vượt số dòng/trang (trừ khi 1 nhân viên đã vượt).',
        '– Dòng Tổng toàn bộ yêu cầu tính trên mọi trang; dòng Công ty / Phòng ban tính trên trang đang xem.',
    ], 'Xem báo cáo'),
    ('BR-04', 'Phạm vi dữ liệu', [
        '– Áp như Phần 2 cho cả bảng, cửa sổ Cơ cấu, Xuất Excel và In.',
    ], ['Xem báo cáo', 'Xem cơ cấu', 'Xuất Excel', 'In danh sách']),
    ('BR-05', 'Mã giải pháp', [
        '– Lấy giải pháp lập GẦN NHẤT từ yêu cầu; chưa có giải pháp ghi “—”.',
    ], 'Xem báo cáo'),
    ('BR-06', 'Cơ cấu tiến trình', [
        '– Đếm theo 10 tiến trình của yêu cầu, chỉ hiện tiến trình có số lượng > 0; tỷ lệ làm tròn 1 chữ số thập phân.',
    ], 'Xem cơ cấu tiến trình yêu cầu'),
    ('BR-07', 'Xuất Excel và In không chia trang', [
        '– Lấy toàn bộ dữ liệu theo điều kiện lọc, bỏ qua trang đang xem; letterhead lấy theo công ty người dùng '
        'đang làm việc.',
    ], ['Xuất Excel', 'In danh sách']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo tổng hợp giải pháp theo phòng ban.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Ảnh chụp thật (shoot.py, client :3002, 1440x900): shots/ — chỉ để local.

Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/report/solutions-work-summary-by-department/{index.vue, print.vue,
      components/FlatSolutionsListModal.vue, components/SummaryBreakdownModal.vue}
      components/V2BaseSmartFilterPanel.vue · components/modal/filter-customization-modal.vue
      components/V2BaseCompanyDepartmentFilter.vue · components/subsystem-menu/presale.js
  BE  Modules/Assign/Routes/api.php (nhóm solutions-work-summary-by-department, KHÔNG gắn checkPermission)
      SolutionsWorkSummaryByDepartmentReportController · Services/Report/SolutionsWorkSummaryByDepartmentReportService
      app/ExcelExport/SolutionsWorkSummaryByDepartmentReportExport + exports/solutions_work_summary_by_department.blade.php
      app/Helper/PermissionHelper.php::checkPermissionList
  Quyền: PermissionsTableSeeder id 1073–1076 (nhóm "Báo cáo tổng hợp GP theo phòng ban")
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


TEN = 'Báo cáo tổng hợp giải pháp theo phòng ban'
MENU = ('Phân hệ CSKH trước bán => Báo cáo => Báo cáo dự án tiền khả thi'
        ' => Báo cáo tổng hợp giải pháp theo phòng ban')
ACTOR = 'Người xem báo cáo'
TACNHAN = 'Lãnh đạo, trưởng phòng giải pháp, nhân sự kỹ thuật; Người dùng đã đăng nhập'
DK = 'Người dùng đã đăng nhập (màn không yêu cầu quyền thao tác riêng; dữ liệu theo quyền V1–V4).'
DK_SEARCHED = DK[:-1] + '; báo cáo đã được tìm kiếm (bảng tổng hợp đang hiển thị).'

OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
d = SrsDoc(out=OUT, menu=MENU, route='', full_url='', img_prefix='thgppb_')
d.set_menu_icons({k: shot(v) for k, v in {
    'Phân hệ CSKH trước bán': 'icon_phanhe.png',
    'Báo cáo': 'icon_baocao.png',
    'Báo cáo dự án tiền khả thi': 'icon_nhom.png',
    'Báo cáo tổng hợp giải pháp theo phòng ban': 'icon_man.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Xem chi tiết': 'icon_xemct.png',
    'Xem': 'icon_coca.png',
    'Ô số liệu': 'icon_so.png',
    'Xuất Excel': 'icon_xuat.png',
    'In báo cáo': 'icon_in.png',
}.items()})
d.title_block(TEN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn %s, nhằm:' % TEN)
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phạm vi dữ liệu của báo cáo.',
    'Làm rõ báo cáo tổng hợp giải pháp theo 3 cấp Công ty → Phòng làm giải pháp → Nhân sự kỹ thuật '
    'và cách quy một giải pháp về đúng một nhân sự kỹ thuật (kỹ sư chính).',
    'Làm rõ công thức của từng chỉ số: yêu cầu giải pháp, đúng hạn / trễ hạn, tỷ lệ chốt, báo giá, '
    'hợp đồng, giải pháp không chốt hợp đồng; và các cửa sổ xem cơ cấu, xem danh sách giải pháp.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('GP', 'Giải pháp (bản ghi ở màn Danh sách giải pháp).'),
    ('YCGP', 'Yêu cầu làm giải pháp do phòng kinh doanh gửi sang phòng giải pháp.'),
    ('Dự án TKT', 'Dự án tiền khả thi mà giải pháp phục vụ.'),
    ('BG / HĐ', 'Báo giá / Hợp đồng.'),
    ('Kỹ sư chính (Nhân sự kỹ thuật)', 'Người được quy trách nhiệm cho 1 GP trong báo cáo: trưởng nhóm (leader) '
     'của hạng mục đầu tiên có leader; GP chưa có hạng mục nào có leader thì lấy người tạo GP.'),
    ('Phòng làm GP', 'Phòng ban của kỹ sư chính theo hồ sơ nhân sự.'),
    ('Nút (dòng) báo cáo', 'Một dòng tổng hợp: Tổng toàn bộ, Công ty, Phòng hoặc Nhân sự kỹ thuật.'),
    ('Công ty đang làm việc', 'Công ty người dùng đang chọn ở góc trên bên phải màn hình.'),
], widths=[1.8, 4.2])

# ========================================================= PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('–', 'Không có quyền thao tác riêng',
     'Menu “Báo cáo tổng hợp giải pháp theo phòng ban” hiển thị với mọi người dùng đã đăng nhập; mọi chức năng '
     '(xem, lọc, cài đặt bộ lọc, xem cơ cấu, xem danh sách, xuất Excel, in) đều dùng được. Dữ liệu nhìn thấy do '
     'nhóm quyền phạm vi bên dưới quyết định.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem báo cáo tổng hợp GP theo tổng công ty',
     'Toàn bộ giải pháp của mọi công ty. Bộ lọc hiện đủ ô Công ty, Phòng ban, Bộ phận, Nhân viên làm giải pháp.'),
    ('V2', 'Xem báo cáo tổng hợp GP theo công ty',
     'Giải pháp thuộc công ty đang làm việc. Bộ lọc ẩn ô Công ty.'),
    ('V3', 'Xem báo cáo tổng hợp GP theo phòng ban',
     'Giải pháp thuộc phòng ban / bộ phận người dùng quản lý, cộng giải pháp do chính người dùng tạo.'),
    ('V4', 'Xem báo cáo tổng hợp GP theo bộ phận',
     'Giải pháp thuộc bộ phận người dùng quản lý, cộng giải pháp do chính người dùng tạo. Bộ lọc ẩn ô Phòng ban.'),
    ('(không có V)', '–', 'Chỉ giải pháp do chính người dùng tạo. Bộ lọc ẩn cả 4 ô tổ chức.'),
], widths=[0.8, 2.2, 3.0])
d.p('Có nhiều quyền phạm vi cùng lúc thì áp quyền rộng nhất theo thứ tự V1 → V2 → V3 → V4.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'V1', 'V2', 'V3', 'V4', 'Không có quyền nào'], [
    ('FR-01 Xem báo cáo tổng hợp giải pháp', '✅', '✅', '✅', '✅', '✅ (chỉ GP mình tạo)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅ (không có ô tổ chức)'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Xem chi tiết theo phòng – nhân sự kỹ thuật', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Xem cơ cấu', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 Xem danh sách giải pháp', '✅', '✅', '✅', '✅', '✅'),
    ('FR-07 Xuất Excel', '✅', '✅', '✅', '✅', '✅'),
    ('FR-08 In báo cáo', '✅', '✅', '✅', '✅', '✅'),
], widths=[2.6, 0.5, 0.5, 0.5, 0.5, 1.4])

# ========================================================= PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR, [0, 1, 2])],
    [('FR-01', 'Xem báo cáo tổng hợp GP', 'view'),
     ('FR-07', 'Xuất Excel', 'io'),
     ('FR-08', 'In báo cáo', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Xem chi tiết phòng – nhân sự', 'view', 'extend', [0], None),
     ('FR-05', 'Xem cơ cấu', 'view', 'extend', [0], None),
     ('FR-06', 'Xem danh sách giải pháp', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1 Xem báo cáo
d.h3('2.1 Xem báo cáo tổng hợp giải pháp')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết.' % TEN,
           anchor='list')
d.intro_table(
    ten='Xem báo cáo tổng hợp giải pháp',
    mota='Bảng tổng hợp số liệu làm giải pháp theo cấp Công ty → Phòng làm GP → Nhân sự kỹ thuật, gồm 4 nhóm chỉ số: '
         'Thông tin làm giải pháp, Cơ cấu nhóm ngành / nhóm GP / ứng dụng, Báo giá từ giải pháp, Hợp đồng từ giải pháp, '
         'và cột GP không chốt HĐ. Mặc định xem ở chế độ thu gọn: dòng Tổng toàn bộ giải pháp + mỗi công ty 1 dòng.',
    tacnhan=TACNHAN,
    dieukien=DK,
    chinh='1. Người dùng mở menu Báo cáo tổng hợp giải pháp theo phòng ban.\n'
          '2. Hệ thống nạp danh mục trạng thái dự án, nhóm ngành, nhóm giải pháp, ứng dụng rồi tự tìm kiếm với bộ lọc mặc '
          'định: Kiểu thời gian = Tháng, Tháng = tháng hiện tại, Năm = năm hiện tại (theo ngày tạo GP).\n'
          '3. Hệ thống hiển thị dòng “Tổng toàn bộ giải pháp” và các dòng Công ty (sắp theo tên).\n'
          '4. Người dùng cuộn ngang để xem đủ các nhóm cột; 2 cột đầu (#, Công ty / Phòng làm GP / Nhân sự kỹ thuật) '
          'được ghim cố định.',
    phu='• Không có giải pháp nào trong phạm vi → bảng chỉ còn dòng Tổng toàn bộ giải pháp với mọi chỉ số bằng 0.\n'
        '• Lỗi khi tải → thông báo “Lỗi khi tải báo cáo tổng hợp làm giải pháp theo phòng ban”, bảng trống.\n'
        '• Sau khi bấm Làm mới mà chưa tìm kiếm xong → khối bảng hiện “Bấm Tìm kiếm để xem báo cáo (không bắt buộc '
        'chọn Công ty).”')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-xem.png'),
         shot_caption='Màn Báo cáo tổng hợp giải pháp theo phòng ban — chế độ thu gọn (lọc năm 2026)')
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Báo cáo tổng hợp giải pháp theo phòng ban',
     'Biểu tượng ⓘ bên cạnh: “Theo dõi được Phòng giải pháp đang làm bao nhiêu giải pháp, nhân viên phụ trách, nhân sự '
     'tham gia, các mốc thời gian, tiến độ đang tới đâu.”'),
    ('Khối Bộ lọc báo cáo tổng hợp giải pháp theo phòng ban', 'Card', 'Hiển thị', '–', 'Thu gọn',
     'Hàng tiêu đề chứa các nút Xuất Excel, In báo cáo, Cài đặt bộ lọc, Tìm kiếm nâng cao (FR-02, 03, 07, 08).'),
    ('Tiêu đề bảng “Danh sách tổng hợp” + ⓘ', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Rê chuột ⓘ: “Công ty → Phòng làm giải pháp → Nhân sự kỹ thuật. Mỗi GP gán một kỹ sư chính (leader hạng mục đầu tiên).”'),
    ('Nút Xem chi tiết / Thu gọn', 'Button', 'Enable', '–', 'Xem chi tiết', 'Xem FR-04.'),
    ('Cột #', 'Icon Button', 'Hiển thị', '–', 'Theo dữ liệu',
     'Dòng công ty có mũi tên mở cấp con (FR-04); dòng Tổng không có mũi tên.'),
    ('Cột Công ty / Phòng làm GP / Nhân sự kỹ thuật', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng Tổng: “Tổng toàn bộ giải pháp (n giải pháp • n nhóm ngành • n nhóm GP • n ứng dụng • Tỷ lệ chốt HĐ: x%)”. '
     'Dòng công ty: “Công ty: <tên>” + dòng phụ cùng nội dung.'),
    ('Nhóm THÔNG TIN LÀM GIẢI PHÁP', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     '9 cột: YCGP đã nhận · YCGP tiếp nhận · Tổng GP đã làm · GP đúng hạn (số + %) · GP trễ hạn (số + %) · '
     'Cơ cấu TT GP (nút “Xem”) · GP chốt · Tỷ lệ chốt (%) · GP ký HĐ. Công thức: BR-03.'),
    ('Nhóm CƠ CẤU NHÓM NGÀNH / NHÓM GP / UD', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     '3 cột Nhóm ngành · Nhóm GP · Ứng dụng: số giá trị khác nhau có trong các GP của dòng; bấm số mở cơ cấu (FR-05).'),
    ('Nhóm BÁO GIÁ TỪ GIẢI PHÁP', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     '4 cột GP chốt BG · SL báo giá · Giá trị BG (dạng 1,000,000 đ; bằng 0 hiện “—”) · TL chuyển BG (%). Công thức: BR-04.'),
    ('Nhóm HỢP ĐỒNG TỪ GIẢI PHÁP', 'Table/Grid', 'Read-only', '≥ 0', '0',
     '4 cột GP chốt HĐ · SL HĐ · Giá trị HĐ · TL chuyển HĐ — hiện luôn bằng 0 (BR-05).'),
    ('Cột GP không chốt HĐ', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu', 'Nền cam nhạt; công thức BR-05.'),
    ('Ô số liệu có khung', 'Button', 'Enable', '–', 'Theo dữ liệu',
     'Các ô YCGP đã nhận, GP chốt BG, SL báo giá, Giá trị BG (khi > 0), TL chuyển BG (khi có GP chốt BG), GP chốt HĐ, '
     'SL HĐ, GP không chốt HĐ bấm được để mở danh sách giải pháp (FR-06). Ô không khung chỉ để đọc.'),
    ('Định dạng số', 'Text', 'Read-only', '–', '–', 'Ngăn cách hàng nghìn bằng dấu phẩy, phần trăm tối đa 2 chữ số thập phân.'),
    ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', 'Biểu tượng xoay + “Đang tải dữ liệu...”.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Xác định quyền phạm vi V1–V4 của người dùng để hiển thị các ô tổ chức trong bộ lọc.\n'
     'After:\n– Nạp danh mục trạng thái dự án TKT, nhóm ngành, nhóm giải pháp, ứng dụng.\n'
     '– Tự tìm kiếm với bộ lọc mặc định (tháng hiện tại theo ngày tạo GP); hiển thị chế độ thu gọn.'),
    ('Tải dữ liệu báo cáo', 'System',
     'During:\n– Lấy các GP khác Nháp trong phạm vi quyền và bộ lọc; quy mỗi GP về 1 kỹ sư chính (BR-02).\n'
     'After:\n– Cộng dồn chỉ số từ nhân sự lên phòng, công ty, tổng toàn bộ.\n'
     '– Lỗi → “Lỗi khi tải báo cáo tổng hợp làm giải pháp theo phòng ban”, bảng trống.'),
    ('Cuộn ngang bảng', 'Change', 'After:\n– Ghim 2 cột đầu và hàng tiêu đề; các nhóm cột còn lại cuộn theo.'),
])

# ------------------------------------------------------------------ 2.2 Tìm kiếm và lọc
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết.' % TEN,
           anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc',
    mota='Khối “Tìm kiếm nâng cao” cho lọc theo thời gian tạo GP, tổ chức của kỹ sư chính, khách hàng, nhóm ngành, nhóm '
         'giải pháp, ứng dụng, tiến trình giải pháp và tiến trình dự án.',
    tacnhan=TACNHAN,
    dieukien=DK,
    chinh='1. Người dùng bấm “Tìm kiếm nâng cao” để mở khối bộ lọc.\n'
          '2. Người dùng chọn giá trị ở các ô lọc; ô dạng chọn được áp dụng ngay (tự tìm kiếm).\n'
          '3. Người dùng bấm “Tìm kiếm” (hoặc để hệ thống tự tìm sau khi chọn).\n'
          '4. Hệ thống tải lại bảng theo bộ lọc; nếu đang ở chế độ chi tiết thì mở sẵn mọi cấp.',
    phu='• Kiểu thời gian = Năm mà chưa chọn Năm → “Vui lòng chọn năm”, không tìm kiếm.\n'
        '• Kiểu thời gian = Tháng mà thiếu Tháng hoặc Năm → “Vui lòng chọn tháng và năm”, không tìm kiếm.\n'
        '• Đổi Kiểu thời gian → xoá giá trị các ô thời gian không còn hiển thị.\n'
        '• Đổi Nhóm ngành → xoá Nhóm giải pháp, Ứng dụng; đổi Nhóm giải pháp → xoá Ứng dụng.\n'
        '• Bấm “Làm mới” → trả bộ lọc về mặc định và tìm kiếm lại.\n'
        '• Bấm “Ẩn tìm kiếm nâng cao” → thu gọn khối bộ lọc, giữ nguyên giá trị đang lọc.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-bo-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Tìm kiếm nâng cao',
     'Mở / thu gọn khối bộ lọc.'),
    ('Kiểu thời gian (ngày tạo GP)', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Không', 'Tháng',
     'Tuỳ chỉnh / Tháng / Năm. Lọc theo NGÀY TẠO giải pháp.'),
    ('Tháng', 'Dropdown', 'Enable / Ẩn', 'Tháng 1 – Tháng 12', 'Có khi Kiểu = Tháng', 'Tháng hiện tại',
     'Chỉ hiện khi Kiểu thời gian = Tháng.'),
    ('Năm', 'Dropdown', 'Enable / Ẩn', 'Năm hiện tại −5 → +1', 'Có khi Kiểu = Tháng hoặc Năm', 'Năm hiện tại',
     'Hiện khi Kiểu thời gian = Tháng hoặc Năm; năm mới nhất ở đầu.'),
    ('Ngày tạo GP', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy – dd/mm/yyyy', 'Không', 'Trống',
     'Khoảng ngày trong 1 ô; chỉ hiện khi Kiểu thời gian = Tuỳ chỉnh hoặc bị xoá trống.'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống', 'Chỉ hiện với quyền V1.'),
    ('Phòng ban làm giải pháp', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Hiện với V1, V2, V3. Lọc theo phòng của kỹ sư chính.'),
    ('Bộ phận làm giải pháp', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Hiện khi có ít nhất 1 quyền V. Lọc theo bộ phận của kỹ sư chính.'),
    ('Nhân viên làm giải pháp', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Hiện khi có ít nhất 1 quyền V. Lọc theo kỹ sư chính. Hiển thị theo khuôn Tên – Mã phòng – Mã NV.'),
    ('Khách hàng', 'Dropdown', 'Enable', 'Gõ để tìm, tối đa 30 kết quả', 'Không', 'Trống',
     'Tìm theo mã / tên khách hàng (SĐT với khách cá nhân); lọc GP có dự án TKT thuộc khách hàng này.'),
    ('Nhóm ngành', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Có ⓘ mô tả.'),
    ('Nhóm giải pháp', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Chỉ liệt kê nhóm thuộc Nhóm ngành đã chọn.'),
    ('Ứng dụng', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Lọc theo Nhóm giải pháp (nếu đã chọn), không thì theo Nhóm ngành.'),
    ('Tiến trình giải pháp', 'Dropdown', 'Enable', 'Danh sách 9 giá trị', 'Không', 'Trống',
     'Chờ PM duyệt, Chờ Leader duyệt, Đang triển khai, Chờ duyệt giải pháp, Đã duyệt giải pháp, Đang điều chỉnh, '
     'Chờ làm giá, Chốt giải pháp, Đã làm giải pháp.'),
    ('Tiến trình dự án', 'Dropdown', 'Enable', 'Danh sách trạng thái dự án TKT', 'Không', 'Trống',
     'Lọc GP có dự án TKT đang ở trạng thái đã chọn.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng bộ lọc.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Trả bộ lọc về mặc định và tìm lại.'),
    ('Thông báo lỗi bộ lọc', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Vui lòng chọn năm” / “Vui lòng chọn tháng và năm”.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / thu gọn khối bộ lọc; nhãn nút đổi tương ứng.'),
    ('Chọn giá trị ô lọc dạng chọn', 'Change',
     'After:\n– Ghi giá trị; nếu là Kiểu thời gian thì xoá giá trị các ô thời gian bị ẩn.\n'
     '– Tự thực hiện như bấm Tìm kiếm.'),
    ('Bấm Tìm kiếm', 'Click',
     'Before:\n– Kiểu = Năm, thiếu Năm → “Vui lòng chọn năm”, dừng.\n'
     '– Kiểu = Tháng, thiếu Tháng/Năm → “Vui lòng chọn tháng và năm”, dừng.\n'
     'During:\n– Quy đổi Tháng/Năm thành khoảng ngày (ngày 1 → ngày cuối tháng; 01/01 → 31/12 với Năm).\n'
     'After:\n– Ghi nhớ bộ lọc đã áp dụng (dùng chung cho FR-06, 07, 08) và tải lại bảng.'),
    ('Bấm Làm mới', 'Click',
     'After:\n– Đưa mọi ô về giá trị mặc định, xoá khách hàng đã chọn, xoá bảng rồi tìm kiếm lại.'),
])

# ------------------------------------------------------------------ 2.3 Cài đặt bộ lọc
d.h3('2.3 Cài đặt bộ lọc')
d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc', 'view', actor=ACTOR)
d.p('2.3.2 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết.' % TEN,
           anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Cho người dùng chọn ô lọc nào hiển thị và sắp xếp thứ tự các ô trong khối Tìm kiếm nâng cao; cấu hình lưu '
         'riêng cho từng người dùng trên màn này.',
    tacnhan=TACNHAN,
    dieukien=DK,
    chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
          '2. Hệ thống mở cửa sổ Cài đặt bộ lọc, liệt kê các trường lọc đang có kèm ô tích.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm “Lưu”.\n'
          '5. Hệ thống lưu cấu hình, đóng cửa sổ, báo “Cập nhật thành công” và vẽ lại khối bộ lọc.',
    phu='• Bấm “Khôi phục mặc định” → hiện lại đủ trường theo thứ tự gốc (chưa lưu cho tới khi bấm Lưu).\n'
        '• Bấm “Đóng” hoặc dấu × → đóng cửa sổ, không lưu.\n'
        '• Lưu lỗi → “Thao tác thất bại”, cửa sổ vẫn mở.\n'
        '• Trường bị ẩn thì giá trị đang lọc của trường đó bị xoá.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', modal='Cài đặt bộ lọc', shot=shot('03-cai-dat.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', 'Kèm icon bánh răng tròn.'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
    ('Danh sách trường lọc', 'Table/Grid', 'Enable', '9 trường', '–', 'Theo cấu hình đã lưu',
     'Mỗi dòng: số thứ tự · tay kéo ⠿ · ô tích + tên trường. Các trường: Kiểu thời gian (ngày tạo GP), Tháng / Năm '
     'hoặc Ngày tạo GP (theo Kiểu thời gian đang chọn), Công ty – Phòng ban làm giải pháp – Bộ phận làm giải pháp '
     '(1 trường gộp), Khách hàng, Nhóm ngành, Nhóm giải pháp, Ứng dụng, Tiến trình giải pháp, Tiến trình dự án.'),
    ('Ô tích hiển thị', 'Checkbox', 'Enable', 'Có / Không', 'Không', 'Theo cấu hình đã lưu', 'Bỏ tích = ẩn ô lọc.'),
    ('Tay kéo ⠿', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo thả để đổi thứ tự.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khoá trong lúc đang lưu.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Không ghi dữ liệu.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở cửa sổ với cấu hình đang áp dụng.'),
    ('Kéo thả / tích ô', 'Change', 'After:\n– Cập nhật thứ tự / trạng thái hiển thị trong cửa sổ (chưa lưu).'),
    ('Bấm Lưu', 'Click',
     'During:\n– Gửi danh sách trường + trạng thái hiển thị cho màn này của người dùng.\n'
     'After:\n– Thành công → đóng cửa sổ, “Cập nhật thành công”, vẽ lại khối bộ lọc theo cấu hình mới.\n'
     '– Lỗi → “Thao tác thất bại”.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Hiện lại đủ trường theo thứ tự gốc, chưa lưu.'),
    ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ------------------------------------------------------------------ 2.4 Xem chi tiết phòng – nhân sự
d.h3('2.4 Xem chi tiết theo phòng – nhân sự kỹ thuật')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết.' % TEN,
           anchor='list')
d.intro_table(
    ten='Xem chi tiết theo phòng – nhân sự kỹ thuật',
    mota='Mở các cấp con dưới mỗi công ty: Phòng làm GP và Nhân sự kỹ thuật (kỹ sư chính), mỗi cấp có đủ các cột chỉ số '
         'như dòng công ty.',
    tacnhan=TACNHAN,
    dieukien=DK_SEARCHED,
    chinh='1. Người dùng bấm “Xem chi tiết”.\n'
          '2. Hệ thống chuyển sang chế độ chi tiết và mở sẵn mọi công ty, mọi phòng.\n'
          '3. Người dùng bấm mũi tên ở từng dòng công ty / phòng để đóng / mở cấp con.\n'
          '4. Người dùng bấm “Thu gọn” để quay về chế độ thu gọn.',
    phu='• Đang ở chế độ thu gọn mà bấm mũi tên của 1 công ty → chuyển sang chế độ chi tiết và chỉ mở công ty đó.\n'
        '• Tìm kiếm lại khi đang ở chế độ chi tiết → sau khi tải xong tự mở sẵn mọi cấp.')
d.p('2.4.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('04-chi-tiet.png'),
         shot_caption='Chế độ chi tiết: Công ty → Phòng → Nhân sự kỹ thuật')
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xem chi tiết / Thu gọn', 'Button', 'Enable', '–', 'Xem chi tiết',
     'Chế độ thu gọn hiện “Xem chi tiết”, chế độ chi tiết hiện “Thu gọn”.'),
    ('Mũi tên mở / đóng', 'Icon Button', 'Enable', '–', 'Theo trạng thái', '› = đang đóng, ⌄ = đang mở.'),
    ('Dòng Phòng', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     '“Phòng: <tên phòng>” + dòng phụ “Số báo giá: n • Số HĐ: n • Tỷ lệ chốt HĐ: x%”. Sắp theo tên phòng.'),
    ('Dòng Nhân sự kỹ thuật', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     '“Nhân sự kỹ thuật: <họ tên>” + dòng phụ “Tổng GP: n • GP ký HĐ: n • Tỷ lệ chốt HĐ: x%”. Sắp theo tên.'),
    ('Các cột chỉ số của dòng con', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Cùng bộ cột, cùng công thức với dòng công ty; ô có khung vẫn bấm được (FR-05, FR-06) với phạm vi của dòng đó.'),
], required=False)
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xem chi tiết', 'Click', 'After:\n– Chuyển chế độ chi tiết, mở sẵn mọi công ty và phòng.'),
    ('Bấm Thu gọn', 'Click', 'After:\n– Quay về chế độ thu gọn (chỉ dòng Tổng và Công ty).'),
    ('Bấm mũi tên dòng công ty / phòng', 'Click',
     'After:\n– Chế độ thu gọn: chuyển chế độ chi tiết và mở riêng dòng vừa bấm.\n'
     '– Chế độ chi tiết: đảo trạng thái mở / đóng của dòng đó.'),
])

# ------------------------------------------------------------------ 2.5 Xem cơ cấu
d.h3('2.5 Xem cơ cấu')
d.p('2.5.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và UI/UX. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết.' % TEN,
           anchor='detail')
d.intro_table(
    ten='Xem cơ cấu',
    mota='Cửa sổ “Cơ cấu” phân bổ số giải pháp của 1 dòng báo cáo theo một trong 4 chiều: trạng thái GP (nút “Xem” ở cột '
         'Cơ cấu TT GP), nhóm ngành, nhóm giải pháp hoặc ứng dụng (bấm số ở 3 cột cơ cấu).',
    tacnhan=TACNHAN,
    dieukien=DK_SEARCHED,
    chinh='1. Người dùng bấm “Xem” ở cột Cơ cấu TT GP, hoặc bấm số ở cột Nhóm ngành / Nhóm GP / Ứng dụng của 1 dòng.\n'
          '2. Hệ thống mở cửa sổ Cơ cấu với tên dòng ở dòng mô tả, liệt kê từng giá trị + Số GP + Tỷ lệ (%), '
          'sắp số GP giảm dần.\n'
          '3. Người dùng bấm “Đóng”.',
    phu='• Dòng không có dữ liệu cho chiều đã chọn → “Không có dữ liệu.”\n'
        '• Cửa sổ dùng ngay số liệu đã tải của báo cáo, không tải lại.')
d.p('2.5.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem', modal='Cơ cấu', shot=shot('05-co-cau.png'),
         shot_caption='Cửa sổ Cơ cấu — theo trạng thái giải pháp của dòng Tổng toàn bộ')
d.figure(shot('05b-co-cau-nganh.png'), 'Cửa sổ Cơ cấu — theo nhóm ngành (bấm số ở cột Nhóm ngành)', width_in=6.2)
d.p('2.5.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Dòng nhãn nhỏ', 'Label', 'Hiển thị', '–', 'CƠ CẤU LÀM GIẢI PHÁP THEO PHÒNG BAN', '–'),
    ('Tiêu đề', 'Label', 'Hiển thị', '–', 'Cơ cấu', '–'),
    ('Dòng mô tả', 'Label', 'Hiển thị', '–', 'Theo dòng đã bấm',
     'Tên dòng: “Tổng toàn bộ giải pháp”, tên công ty, tên phòng hoặc tên nhân sự.'),
    ('Cột #', 'Number', 'Read-only', '≥ 1', 'Theo dữ liệu', '–'),
    ('Cột giá trị', 'Text / Badge', 'Read-only', '–', 'Theo dữ liệu',
     'Tiêu đề cột đổi theo chiều: “Trạng thái GP” (badge màu do hệ thống trả về), “Nhóm ngành”, “Nhóm giải pháp”, '
     '“Ứng dụng”.'),
    ('Cột Số GP', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu', '–'),
    ('Cột Tỷ lệ (%)', 'Number', 'Read-only', '0 – 100', 'Theo dữ liệu', 'Số GP / tổng số GP của bảng × 100, tối đa 2 số lẻ.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu.”'),
    ('Nút Đóng / ×', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)
d.p('2.5.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm “Xem” cột Cơ cấu TT GP', 'Click', 'After:\n– Mở cửa sổ theo chiều Trạng thái GP của dòng.'),
    ('Bấm số cột Nhóm ngành / Nhóm GP / Ứng dụng', 'Click', 'After:\n– Mở cửa sổ theo chiều tương ứng của dòng.'),
    ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng cửa sổ, xoá nội dung cũ.'),
])

# ------------------------------------------------------------------ 2.6 Xem danh sách giải pháp
d.h3('2.6 Xem danh sách giải pháp')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết, Kịch bản tìm kiếm. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết.' % TEN,
           anchor='detail')
d.intro_table(
    ten='Xem danh sách giải pháp',
    mota='Bấm vào ô số liệu có khung để xem danh sách các giải pháp tạo nên con số đó, trong phạm vi dòng đã bấm và bộ lọc '
         'đang áp dụng. Cửa sổ có bộ lọc riêng: Trạng thái, Nhóm ngành, Tìm kiếm.',
    tacnhan=TACNHAN,
    dieukien=DK_SEARCHED,
    chinh='1. Người dùng bấm ô số liệu có khung ở 1 dòng.\n'
          '2. Hệ thống mở cửa sổ “Danh sách giải pháp” với tiêu đề theo cột đã bấm và dòng mô tả phạm vi.\n'
          '3. Hệ thống tải toàn bộ giải pháp thoả điều kiện (cùng bộ lọc báo cáo + phạm vi dòng + loại cột).\n'
          '4. Người dùng lọc thêm theo Trạng thái, Nhóm ngành hoặc gõ từ khoá.\n'
          '5. Người dùng bấm “Đóng”.',
    phu='• Chưa tìm kiếm báo cáo → “Vui lòng tìm kiếm trước khi xem danh sách chi tiết.”, không mở cửa sổ.\n'
        '• Không có giải pháp nào → “Không có bản ghi.”\n'
        '• Bấm “Làm mới” trong cửa sổ → xoá 3 ô lọc của cửa sổ và tải lại.\n'
        '• Cột “GP không chốt HĐ” mở dạng bảng riêng có cột “Lý do không ký HĐ”.')
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Ô số liệu', modal='Danh sách giải pháp', shot=shot('06-danh-sach.png'),
         shot_caption='Cửa sổ Danh sách giải pháp — mở từ ô YCGP đã nhận của dòng Tổng')
d.figure(shot('06b-khong-chot.png'), 'Cửa sổ Danh sách giải pháp — mở từ ô GP không chốt HĐ', width_in=6.2)
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Dòng nhãn nhỏ', 'Label', 'Hiển thị', '–', '–', 'DANH SÁCH GIẢI PHÁP', '–'),
    ('Tiêu đề', 'Label', 'Hiển thị', '–', '–', 'Theo cột đã bấm',
     'YCGP đã nhận → “Danh sách giải pháp”; GP chốt BG → “Giải pháp chốt báo giá”; SL báo giá → “Theo số lượng báo giá”; '
     'Giá trị BG → “Giá trị báo giá — danh sách GP có giá trị BG”; TL chuyển BG → “Tỷ lệ chuyển BG — danh sách GP (mẫu số)”; '
     'GP chốt HĐ → “Giải pháp chốt hợp đồng”; SL HĐ → “Theo số lượng hợp đồng”; GP không chốt HĐ → “Giải pháp / dự án '
     'không chốt được HĐ”.'),
    ('Dòng mô tả phạm vi', 'Label', 'Hiển thị', '–', '–', 'Theo dòng đã bấm',
     '“Phạm vi toàn bộ kết quả báo cáo (theo bộ lọc và quyền).” / “Phạm vi công ty: <tên>” / “Phạm vi phòng ban: <tên>” / '
     '“Phạm vi nhân sự kỹ thuật: <tên>”; riêng Giá trị BG và TL chuyển BG có câu giải thích công thức.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 9 giá trị', 'Không', 'Trống',
     'Gợi ý “Chọn trạng thái”; cùng danh sách với ô Tiến trình giải pháp của bộ lọc. Chọn là tải lại.'),
    ('Nhóm ngành', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Gợi ý “Chọn nhóm ngành”. Chọn là tải lại.'),
    ('Tìm kiếm', 'Textbox', 'Enable', '0–200 ký tự', 'Không', 'Trống',
     'Gợi ý “Giải pháp / Dự án / KH”; tìm trong mã GP, tên GP, dự án TKT, khách hàng; tự tải sau 0,4 giây ngừng gõ '
     'hoặc khi nhấn Enter.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá 3 ô lọc của cửa sổ và tải lại.'),
    ('Bảng giải pháp', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'STT · Giải pháp/Dự án (tên GP + dòng phụ mã – tên dự án TKT) · Nhân sự kỹ thuật · Khách hàng · Trạng thái (badge) · '
     'Số version GP · Tổng giờ làm GP (tổng giờ thực tế các nhiệm vụ của GP) · Số BG · Giá trị BG · Số HĐ · Giá trị HĐ.'),
    ('Bảng GP không chốt HĐ', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'STT · Giải pháp · Nhân sự kỹ thuật · Khách hàng · Trạng thái · Số version GP · Tổng giờ làm GP · Lý do không ký HĐ '
     '(chưa có dữ liệu thì “Chưa cập nhật lý do”).'),
    ('Tổng số bản ghi', 'Label', 'Hiển thị', '–', '–', 'Ẩn khi 0', '“<n> bản ghi”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '“Không có bản ghi.”'),
    ('Nút Đóng / ×', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, xoá điều kiện lọc của cửa sổ.'),
])
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm ô số liệu có khung', 'Click',
     'Before:\n– Chưa tìm kiếm báo cáo → “Vui lòng tìm kiếm trước khi xem danh sách chi tiết.”, dừng.\n'
     'After:\n– Mở cửa sổ, tải lần lượt từng trang 100 dòng cho tới hết rồi hiển thị toàn bộ.'),
    ('Chọn Trạng thái / Nhóm ngành', 'Change', 'After:\n– Tải lại danh sách theo điều kiện mới.'),
    ('Gõ ô Tìm kiếm', 'Keypress', 'After:\n– Ngừng gõ 0,4 giây hoặc nhấn Enter → tải lại danh sách.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xoá Trạng thái, Nhóm ngành, từ khoá; tải lại.'),
    ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ------------------------------------------------------------------ 2.7 Xuất Excel
d.h3('2.7 Xuất Excel')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xuất Excel', 'io', actor=ACTOR)
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết.' % TEN, anchor='excel')
d.intro_table(
    ten='Xuất Excel',
    mota='Tải file Excel báo cáo theo bộ lọc đã áp dụng, gồm đủ cấp Tổng → Công ty → Phòng → Nhân sự kỹ thuật '
         '(không phụ thuộc chế độ thu gọn / chi tiết trên màn).',
    tacnhan=TACNHAN,
    dieukien=DK_SEARCHED,
    chinh='1. Người dùng bấm “Xuất Excel”.\n'
          '2. Hệ thống dựng file theo bộ lọc lần Tìm kiếm gần nhất và trong phạm vi quyền.\n'
          '3. Trình duyệt tải file “bao_cao_tong_hop_gp_theo_phong_ban.xls”.\n'
          '4. Hệ thống báo “Xuất Excel thành công”.',
    phu='• Chưa tìm kiếm hoặc bảng trống → “Vui lòng tìm kiếm và có dữ liệu trước khi xuất Excel”, không xuất.\n'
        '• Lỗi khi xuất → “Lỗi khi xuất Excel”.',
    dacbiet='File gồm: ảnh tiêu đề (letterhead) của công ty đang làm việc, tiêu đề “BÁO CÁO TỔNG HỢP LÀM GIẢI PHÁP THEO '
            'PHÒNG BAN”, 2 hàng tiêu đề cột gộp nhóm như trên màn (không có cột Cơ cấu TT GP), dòng Tổng (Σ) nền xanh lá, '
            'dòng Công ty nền xanh dương, dòng Phòng, dòng Nhân sự kỹ thuật.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('07-xuat.png'),
         shot_caption='Bấm Xuất Excel — thông báo “Xuất Excel thành công”')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xuất Excel', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Nằm ở hàng tiêu đề khối bộ lọc, viền xanh lá.'),
    ('Thanh tiến trình đầu trang', 'Loading', 'Hiển thị', '–', '–', 'Ẩn', 'Chạy trong lúc dựng file.'),
    ('File tải về', 'File', 'Hiển thị', '.xls', '–', '–', 'Tên “bao_cao_tong_hop_gp_theo_phong_ban.xls”.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Xuất Excel thành công” / “Lỗi khi xuất Excel” / “Vui lòng tìm kiếm và có dữ liệu trước khi xuất Excel”.'),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Chưa tìm kiếm / không có dòng nào → “Vui lòng tìm kiếm và có dữ liệu trước khi xuất Excel”, dừng.\n'
     'During:\n– Gửi bộ lọc của lần Tìm kiếm gần nhất; hệ thống áp phạm vi quyền V1–V4 như FR-01.\n'
     'After:\n– Tải file .xls, hiển thị “Xuất Excel thành công”.\n'
     '– Lỗi → “Lỗi khi xuất Excel”.'),
])

# ------------------------------------------------------------------ 2.8 In báo cáo
d.h3('2.8 In báo cáo')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'In báo cáo', 'io', actor=ACTOR)
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Quy tắc in. Chỉ bổ sung các quy tắc riêng của %s tại phần mô tả chi tiết.' % TEN, anchor='excel')
d.intro_table(
    ten='In báo cáo',
    mota='Mở tab mới chứa bản xem trước để in báo cáo theo bộ lọc đã áp dụng, đủ cấp Tổng → Công ty → Phòng → Nhân sự kỹ thuật.',
    tacnhan=TACNHAN,
    dieukien=DK_SEARCHED,
    chinh='1. Người dùng bấm “In báo cáo”.\n'
          '2. Hệ thống mở tab mới, tải lại dữ liệu theo bộ lọc lần Tìm kiếm gần nhất và hiển thị bản xem trước.\n'
          '3. Người dùng bấm nút “In” trên tab mới.\n'
          '4. Trình duyệt mở hộp thoại in với khổ A4 nằm ngang.',
    phu='• Chưa tìm kiếm hoặc bảng trống → “Vui lòng tìm kiếm và có dữ liệu trước khi in”, không mở tab.\n'
        '• Lỗi khi tải dữ liệu in → khung đỏ nội dung lỗi (mặc định “Lỗi không xác định khi tải dữ liệu báo cáo”).',
    dacbiet='Bản in: ảnh tiêu đề công ty đang làm việc (thiếu thì dùng ảnh mặc định), tiêu đề “BÁO CÁO TỔNG HỢP LÀM GIẢI '
            'PHÁP THEO PHÒNG BAN”, bảng 22 cột (không có cột Cơ cấu TT GP), STT phân cấp 1 / 1.1 / 1.1.1, dòng Tổng ký '
            'hiệu Σ; nhân sự hiển thị “NSKT: <họ tên>”.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => In báo cáo', shot=shot('08-in.png'),
         shot_caption='Bản xem trước In báo cáo (tab mới)')
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In báo cáo', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Nằm ở hàng tiêu đề khối bộ lọc.'),
    ('Nút In (tab mới)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Không xuất hiện trên bản in.'),
    ('Ảnh tiêu đề công ty', 'Image', 'Hiển thị', '–', '–', 'Theo công ty đang làm việc', '–'),
    ('Tiêu đề bản in', 'Label', 'Hiển thị', '–', '–', 'BÁO CÁO TỔNG HỢP LÀM GIẢI PHÁP THEO PHÒNG BAN', '–'),
    ('Bảng in', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'STT · Công ty / Phòng làm GP / Nhân sự kỹ thuật · 8 cột Thông tin làm giải pháp · 3 cột Cơ cấu · 4 cột Báo giá · '
     '4 cột Hợp đồng · GP không chốt HĐ. Giá trị tiền bằng 0 in “—”.'),
    ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Khung đỏ phía trên, không in ra giấy.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '“Không có dữ liệu”.'),
])
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In báo cáo', 'Click',
     'Before:\n– Chưa tìm kiếm / không có dòng nào → “Vui lòng tìm kiếm và có dữ liệu trước khi in”, dừng.\n'
     'After:\n– Mở tab mới mang theo bộ lọc của lần Tìm kiếm gần nhất.'),
    ('Mở tab in', 'System',
     'During:\n– Tải dữ liệu báo cáo theo bộ lọc, áp phạm vi quyền V1–V4.\n'
     'After:\n– Hiển thị bản xem trước; lỗi → khung đỏ nội dung lỗi.'),
    ('Bấm In', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt, khổ A4 ngang, lề 8mm × 6mm.'),
])

# ==================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc đã có trong SRS quy tắc chung.' % TEN,
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Giải pháp được đưa vào báo cáo', [
        '– Mọi giải pháp KHÁC trạng thái Nháp, trong phạm vi quyền V1–V4 (Phần 2).',
        '– Thời gian lọc theo NGÀY TẠO giải pháp; mặc định tháng hiện tại.',
        '– Lọc Khách hàng / Tiến trình dự án theo dự án TKT của giải pháp; Nhóm ngành / Nhóm giải pháp / Ứng dụng / '
        'Tiến trình giải pháp theo chính giải pháp.',
    ], ['Xem báo cáo', 'Tìm kiếm và lọc', 'Xuất Excel', 'In báo cáo']),
    ('BR-02', 'Quy giải pháp về kỹ sư chính', [
        '– Mỗi giải pháp tính cho ĐÚNG 1 nhân sự kỹ thuật: trưởng nhóm của hạng mục đầu tiên (theo thứ tự tạo) có trưởng '
        'nhóm; không có thì người tạo giải pháp.',
        '– Phòng / bộ phận lấy theo hồ sơ nhân sự hiện tại của kỹ sư chính; công ty lấy theo công ty của giải pháp.',
        '– Bộ lọc Phòng ban / Bộ phận / Nhân viên làm giải pháp so với kỹ sư chính.',
        '– Số liệu cấp Phòng = tổng các nhân sự; cấp Công ty = tổng các phòng; dòng Tổng = tổng các công ty.',
    ], ['Xem báo cáo', 'Xem chi tiết theo phòng – nhân sự kỹ thuật']),
    ('BR-03', 'Công thức nhóm Thông tin làm giải pháp', [
        '– YCGP đã nhận: số GP có yêu cầu làm giải pháp đi kèm và yêu cầu đó khác Nháp.',
        '– YCGP tiếp nhận: số GP có yêu cầu ở trạng thái Đã tiếp nhận trở về sau, trừ Từ chối.',
        '– Tổng GP đã làm: số GP từ trạng thái Đã duyệt giải pháp trở về sau.',
        '– GP đúng hạn: phiên bản hiện tại có ngày hoàn thành ≤ hạn của GP. GP trễ hạn: hoàn thành sau hạn, hoặc chưa '
        'hoàn thành mà hôm nay đã quá hạn. Phần trăm = số GP ÷ Tổng GP đã làm.',
        '– GP chốt: trạng thái Chốt giải pháp. Tỷ lệ chốt = GP chốt ÷ tổng GP (trừ Nháp).',
    ], 'Xem báo cáo'),
    ('BR-04', 'Công thức nhóm Báo giá từ giải pháp', [
        '– GP chốt BG: GP có dự án TKT ở trạng thái Lập dự toán trở về sau. Mỗi GP như vậy tính 1 báo giá (SL báo giá).',
        '– Giá trị BG = giá trị hợp đồng dự kiến của dự án TKT (không có thì lấy ngân sách dự kiến).',
        '– TL chuyển BG = số GP có hợp đồng ÷ số GP chốt BG.',
    ], ['Xem báo cáo', 'Xem danh sách giải pháp']),
    ('BR-05', 'Hợp đồng và GP không chốt HĐ', [
        '– Nhóm Hợp đồng từ giải pháp (GP chốt HĐ, SL HĐ, Giá trị HĐ, TL chuyển HĐ) và cột GP ký HĐ, Tỷ lệ chốt HĐ hiện '
        'LUÔN bằng 0: cách tính hợp đồng đang tạm tắt chờ chốt lại logic.',
        '– GP không chốt HĐ: GP có dự án TKT ở trạng thái Đóng/Không thực hiện dự án.',
    ], ['Xem báo cáo', 'Xem danh sách giải pháp']),
    ('BR-06', 'Cơ cấu nhóm ngành / nhóm GP / ứng dụng', [
        '– Lấy theo giải pháp; giải pháp để trống thì lấy theo dự án TKT, rồi theo ứng dụng / nhóm của ứng dụng.',
        '– Số ở 3 cột cơ cấu = số giá trị KHÁC NHAU xuất hiện trong các GP của dòng.',
    ], ['Xem báo cáo', 'Xem cơ cấu']),
    ('BR-07', 'Danh sách giải pháp theo ô số liệu', [
        '– Danh sách dùng đúng bộ lọc của lần Tìm kiếm gần nhất, giới hạn trong dòng đã bấm (Tổng / Công ty / Phòng / '
        'Nhân sự) và điều kiện của cột (vd ô GP chốt BG chỉ liệt kê GP chốt BG).',
        '– Ô YCGP đã nhận liệt kê TOÀN BỘ GP của dòng.',
    ], 'Xem danh sách giải pháp'),
    ('BR-08', 'Ảnh tiêu đề bản in và file Excel', [
        '– Dùng ảnh tiêu đề của công ty đang làm việc; công ty chưa có ảnh thì dùng ảnh mặc định của hệ thống.',
    ], ['Xuất Excel', 'In báo cáo']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

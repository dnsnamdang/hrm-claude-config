# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo giá chờ duyệt.docx" theo FORM CHUẨN (bản mẫu 2026-09-24).

Chạy (từ thư mục gốc HRM/, BỌC KHOÁ WORD nếu có phiên khác cũng đang sinh tài liệu):
    python3 .plans/bao-gia-cho-duyet-hdsd/gen_srs.py
Thư viện dùng chung: .claude/skills/srs-documenter/assets/{srs_docx_lib,srs_uml_render}.py
Ảnh chụp thật (Playwright Python, 1440x900, nhánh develop): bg_choduyet_shots/ — chỉ để local.

Nguồn đối chiếu code:
  FE  pages/assign/quotations/pending-approval/index.vue
      pages/assign/quotations/_id/index.vue (footer: canTpApprove / canBgdApprove / canReject,
      doTpApprove / doBgdApprove) · components/assign/quotation/QuotationRejectModal.vue
      components/assign/quotation/QuotationHistoryModal.vue
      components/menu-sidebar.js (Phê duyệt › Giải pháp - Dự án) · subsystem-menu/sale-hub.js
      (Phê Duyệt › Dự án TKT) · subsystem-menu/sale.js (SALE_LINK_PERMISSIONS)
  BE  Modules/Assign/Routes/api.php (nhóm /assign/quotations)
      Http/Controllers/Api/V1/QuotationController.php (pendingApproval, pendingApprovalExport,
      show, tpApprove, bgdApprove, reject) · Http/Requests/Quotation/QuotationRejectRequest.php
      Services/QuotationService.php (getPendingApproval, applyListFilters, submit, tpApprove,
      bgdApprove, reject, ensureTpCanApprove, ensureBgdCanApprove, cascadeApprovedStatus,
      notifyByPermission / notifyApproved / notifyRejected, calculateLevel, isAutoApprovable)
      Services/BomPriceApprovalConfigService.php (calculateApprovalLevel)
      Transformers/QuotationResource.php · DetailQuotationResource.php (can_view_cost_price)
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 1081–1086, 1092)
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

OUT = os.path.join(HERE, 'SRS - Báo giá chờ duyệt.docx')
SHOTS = os.path.join(HERE, 'bg_choduyet_shots')

# Màn có 2 lối vào menu (cùng một màn, cùng phạm vi dữ liệu)
MENU = 'Phân hệ Công việc => Phê duyệt => Giải pháp - Dự án => Báo giá chờ duyệt'
MENU_BH = 'Phân hệ Bán hàng => Phê Duyệt => Dự án TKT => Báo giá chờ duyệt'
ROW = 'Duyệt (cột Hành động)'          # nút điều hướng sang màn chi tiết ở từng dòng
DETAIL = MENU + ' => ' + ROW

A_TP = 'Trưởng phòng duyệt giá (Q1)'
A_BGD = 'Ban giám đốc duyệt giá (Q2)'
A_BOTH = 'Trưởng phòng duyệt giá (Q1); Ban giám đốc duyệt giá (Q2)'

NO_PERM = ('– Không có quyền Q1 hoặc Q2 → hiển thị “Bạn không có quyền thực hiện chức năng '
           'này” và dừng xử lý.')


def shot(name):
    return os.path.join(SHOTS, name)


def entry_note():
    """Ghi đủ 2 lối vào menu (SKILL: màn nhiều lối vào phải liệt kê đủ)."""
    d.p('Lối vào thứ hai của cùng màn hình (cùng dữ liệu, cùng thao tác):')
    d._menu_para(MENU_BH)
    d.p('Hiển thị: cả hai lối vào mở cùng một màn và cùng hàng chờ duyệt của người đăng nhập. '
        'Mục menu ở bảng chọn chức năng của cả hai phân hệ hiện với mọi người dùng (ở phân hệ Bán '
        'hàng chỉ cây menu dọc của màn con mới ẩn theo quyền Q1/Q2); người không có Q1/Q2 mở vào sẽ '
        'nhận thông báo “Bạn không có quyền thực hiện chức năng này” và bảng rỗng.')


d = SrsDoc(out=OUT, menu=MENU, route='', full_url='', img_prefix='bgcd_')

d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ Công việc': 'phanhe_cv',
    'Phê duyệt': 'pheduyet_cv',
    'Giải pháp - Dự án': 'gpda',
    'Báo giá chờ duyệt': 'bgcd',
    'Phân hệ Bán hàng': 'phanhe_bh',
    'Phê Duyệt': 'pheduyet_bh',
    'Dự án TKT': 'duantkt',
    'Tìm kiếm nâng cao': 'timkiemnangcao',
    'Cài đặt bộ lọc': 'caidatboloc',
    'Tùy chỉnh cột': 'tuychinhcot',
    'Xuất Excel': 'xuatexcel',
    'Lịch sử phê duyệt': 'lichsu',
    ROW: 'duyet_row',
    'Duyệt': 'duyet',
    'Duyệt & chuyển BGĐ': 'duyet_chuyen',
    'BGĐ duyệt': 'bgd_duyet',
    'Từ chối': 'tuchoi',
}.items()})

# ============================================================== TRANG ĐẦU
d.title_block('Báo giá chờ duyệt')
d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1. GIỚI THIỆU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Báo giá chờ duyệt — hàng đợi để Trưởng '
    'phòng và Ban giám đốc phê duyệt giá các báo giá dự án TKT, nhằm:')
d.bullets([
    'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho bước phê duyệt '
    'giá báo giá: nhận báo giá đã gửi duyệt → xem chi tiết → Duyệt, Duyệt & chuyển BGĐ, BGĐ '
    'duyệt hoặc Từ chối.',
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ cơ chế cấp duyệt tự tính (Cấp 1 tự duyệt, Cấp 2 Trưởng phòng chốt, Cấp 3 Trưởng '
    'phòng rồi Ban giám đốc) và phạm vi hàng chờ của từng vai trò.',
    'Làm rõ các hệ quả tự động sau khi báo giá được duyệt hoặc bị từ chối.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Báo giá', 'Báo giá dự án TKT do nhân viên kinh doanh lập (từ BOM hoặc tự nhập). Màn hình '
     'này chỉ xử lý báo giá thường, không xử lý báo giá tổng.'),
    ('TP', 'Trưởng phòng — người có quyền “Trưởng phòng duyệt giá Bom giải pháp” và được giao '
     'quản lý phòng ban của báo giá.'),
    ('BGĐ', 'Ban giám đốc — người có quyền “Ban giám đốc duyệt giá Bom giải pháp” thuộc cùng '
     'công ty với báo giá.'),
    ('Cấp duyệt', 'Mức phê duyệt hệ thống tự tính khi người lập bấm gửi duyệt: Cấp 1 — Tự duyệt '
     '(không vào màn này), Cấp 2 — TP duyệt, Cấp 3 — TP & BGĐ duyệt.'),
    ('Cấu hình duyệt giá', 'Bảng ngưỡng theo giá trị đơn hàng, tỷ suất lợi nhuận tổng và tỷ suất '
     'lợi nhuận dòng hàng tạm; là căn cứ tính cấp duyệt.'),
    ('TSLN', 'Tỷ suất lợi nhuận của báo giá (trước / sau giảm giá).'),
    ('Giá vốn', 'Giá nhập và các số liệu suy ra từ giá nhập (thành tiền nhập, TSLN); chỉ hiển '
     'thị với người có quyền “Xem giá vốn hàng hoá”.'),
    ('Đang tạo', 'Trạng thái nháp của báo giá; báo giá bị từ chối quay về trạng thái này.'),
    ('Chờ TP duyệt', 'Báo giá cấp 2 hoặc cấp 3 vừa được gửi duyệt, chờ Trưởng phòng xử lý.'),
    ('Chờ BGĐ duyệt', 'Báo giá cấp 3 đã được Trưởng phòng duyệt, chờ Ban giám đốc xử lý.'),
    ('Đã duyệt', 'Báo giá đã qua đủ cấp duyệt; được đồng bộ sang ERP và dùng để thương thảo.'),
], widths=[1.6, 4.4])

# ========================================================= PHẦN 2. PHÂN QUYỀN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Trưởng phòng duyệt giá Bom giải pháp',
     'Mở màn hình và Xuất Excel; thấy báo giá Chờ TP duyệt thuộc các phòng ban mình được giao '
     'quản lý; hiện nút Duyệt / Duyệt & chuyển BGĐ và Từ chối ở màn chi tiết báo giá Chờ TP '
     'duyệt.'),
    ('Q2', 'Ban giám đốc duyệt giá Bom giải pháp',
     'Mở màn hình và Xuất Excel; thấy báo giá Chờ BGĐ duyệt thuộc công ty của mình; hiện nút BGĐ '
     'duyệt và Từ chối ở màn chi tiết báo giá Chờ BGĐ duyệt.'),
    ('Q3', 'Xem giá vốn hàng hoá',
     'Ở màn chi tiết: hiện giá nhập, thành tiền nhập, tổng giá nhập và các chỉ số TSLN. Không '
     'có Q3 thì các ô này hiển thị “—” hoặc bị ẩn.'),
], widths=[0.8, 2.0, 3.2])

d.p('Nhóm quyền quyết định phạm vi dữ liệu (dùng chung với màn Danh sách báo giá; xét theo thứ tự '
    'từ trên xuống, cấp nào có trước thì áp cấp đó). Nhóm này KHÔNG quyết định hàng chờ duyệt — '
    'hàng chờ do Q1/Q2 quyết định — mà quyết định ô lọc tổ chức hiển thị và báo giá NGOÀI hàng '
    'chờ nào mở được màn chi tiết. Báo giá đang nằm trong hàng chờ duyệt của người dùng luôn mở '
    'được chi tiết, kể cả khi không có V1–V4:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem danh sách Báo giá theo tổng công ty',
     'Mở chi tiết mọi báo giá. Bộ lọc hiện đủ Công ty, Phòng ban, Bộ phận, Nhân viên.'),
    ('V2', 'Xem danh sách Báo giá theo công ty',
     'Mở chi tiết báo giá thuộc công ty đang làm việc hoặc do mình lập. Bộ lọc hiện Phòng ban, '
     'Bộ phận, Nhân viên.'),
    ('V3', 'Xem danh sách Báo giá theo phòng ban',
     'Mở chi tiết báo giá thuộc phòng ban / bộ phận mình quản lý hoặc do mình lập. Bộ lọc hiện '
     'Phòng ban, Bộ phận, Nhân viên.'),
    ('V4', 'Xem danh sách Báo giá theo bộ phận',
     'Mở chi tiết báo giá thuộc bộ phận mình quản lý hoặc do mình lập. Bộ lọc hiện Bộ phận, '
     'Nhân viên.'),
    ('—', '(không có cấp nào)',
     'Chỉ mở được chi tiết báo giá do chính mình lập. Bộ lọc không có ô tổ chức.'),
], widths=[0.8, 2.0, 3.2])
d.p('Phạm vi hàng chờ duyệt (không phụ thuộc V1–V4): người có Q1 thấy báo giá Chờ TP duyệt của '
    'các phòng ban mình được giao quản lý; người có Q2 thấy báo giá Chờ BGĐ duyệt của công ty mình; '
    'có cả hai thì thấy hợp của hai nhóm. Không có Q1/Q2, hoặc có Q1 mà không quản lý phòng ban '
    'nào, thì hàng chờ rỗng.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách báo giá chờ duyệt', '✅ (Chờ TP duyệt)', '✅ (Chờ BGĐ duyệt)', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '❌'),
    ('FR-04 Tùy chỉnh cột', '✅', '✅', '❌'),
    ('FR-05 Xem lịch sử phê duyệt', '✅', '✅', '❌'),
    ('FR-06 Xem chi tiết báo giá để duyệt', '✅ (báo giá trong hàng chờ)', '✅ (báo giá trong hàng chờ)', '❌'),
    ('FR-07 Xuất Excel', '✅', '✅', '❌'),
    ('FR-08 Duyệt báo giá cấp 2', '✅', '❌', '❌'),
    ('FR-09 Duyệt & chuyển BGĐ', '✅', '❌', '❌'),
    ('FR-10 BGĐ duyệt báo giá', '❌', '✅', '❌'),
    ('FR-11 Từ chối báo giá', '✅ (Chờ TP duyệt)', '✅ (Chờ BGĐ duyệt)', '❌'),
], widths=[2.6, 1.15, 1.15, 1.1])

# ================================================ PHẦN 3. ĐẶC TẢ CHI TIẾT
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_TP, [0, 1, 2, 3, 5]),
     (A_BGD, [0, 1, 4, 5])],
    [('FR-01', 'Xem danh sách báo giá chờ duyệt', 'view'),
     ('FR-07', 'Xuất Excel', 'io'),
     ('FR-08', 'Duyệt báo giá cấp 2', 'action'),
     ('FR-09', 'Duyệt & chuyển BGĐ', 'action'),
     ('FR-10', 'BGĐ duyệt báo giá', 'action'),
     ('FR-11', 'Từ chối báo giá', 'action')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột', 'view', 'extend', [0], None),
     ('FR-05', 'Xem lịch sử phê duyệt', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết báo giá để duyệt', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Báo giá chờ duyệt')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1 FR-01
d.h3('2.1 Xem danh sách báo giá chờ duyệt')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Báo giá chờ duyệt tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách báo giá chờ duyệt',
    mota='Hiển thị hàng đợi báo giá đang chờ chính người đăng nhập phê duyệt: báo giá Chờ TP duyệt '
         'của các phòng ban mình quản lý (Q1) và báo giá Chờ BGĐ duyệt của công ty mình (Q2), kèm '
         'tổng số, phân trang và sắp xếp.',
    tacnhan=A_BOTH + '; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có ít nhất một trong hai quyền Q1, Q2.',
    chinh='1. Hệ thống kiểm tra quyền Q1 / Q2 của người dùng.\n'
          '2. Hệ thống lấy báo giá thường (không phải báo giá tổng) theo phạm vi hàng chờ: Q1 → '
          'Chờ TP duyệt thuộc phòng ban mình quản lý; Q2 → Chờ BGĐ duyệt thuộc công ty mình.\n'
          '3. Hệ thống sắp xếp mặc định theo Ngày gửi duyệt mới nhất lên trước, trả về trang 1 '
          'với 20 dòng/trang.\n'
          '4. Bảng hiển thị dữ liệu, ô “Tổng: N” hiển thị tổng số báo giá đang chờ.',
    phu='• Không có báo giá nào trong hàng chờ → bảng hiện “Không có báo giá nào chờ duyệt.”.\n'
        '• Có Q1 nhưng không được giao quản lý phòng ban nào → hàng chờ rỗng.\n'
        '• Không có Q1/Q2 → hệ thống báo “Bạn không có quyền thực hiện chức năng này”, bảng rỗng.\n'
        '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó.\n'
        '• Vào lại màn trong vòng 10 phút sau khi rời đi → hệ thống khôi phục bộ lọc đã dùng.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn Báo giá chờ duyệt lúc mới truy cập')
entry_note()
d.figure(shot('00-menu-cong-viec.png'),
         'Lối vào từ phân hệ Công việc: Phê duyệt → Giải pháp - Dự án', width_in=6.2)
d.figure(shot('00-menu-ban-hang.png'),
         'Lối vào từ phân hệ Bán hàng: Phê Duyệt → Dự án TKT', width_in=6.2)

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang / tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Báo giá chờ duyệt', '–'),
    ('Ô “Tổng: N”', 'Label', 'Read-only', '≥ 0', 'Theo kết quả',
     'Tổng số báo giá khớp bộ lọc trong hàng chờ của người đăng nhập.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Mở popup chọn trường xuất (FR-07).'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tùy chỉnh cột (FR-04).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục', 'Cột khoá, ghim trái.'),
    ('Cột Mã báo giá', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Liên kết mở màn chi tiết (FR-06); sắp xếp được; cột khoá, ghim trái.'),
    ('Cột Loại báo giá', 'Badge', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu',
     'Từ BOM / Tự nhập.'),
    ('Cột BOM list', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dạng “Mã - Tên BOM list”; trống với báo giá tự nhập.'),
    ('Cột Dự án TKT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Dạng “Mã - Tên dự án”.'),
    ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Sắp xếp được.'),
    ('Cột Giai đoạn dự án', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Tiền tệ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Mặc định VND.'),
    ('Cột Tổng giá trị sau VAT', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Canh phải, định dạng số quốc tế (vd 13,060,250,000); sắp xếp được.'),
    ('Cột Cấp duyệt', 'Badge', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu',
     'TP (cấp 2) / TP & BGĐ (cấp 3); sắp xếp được.'),
    ('Cột Người gửi duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Người lập báo giá.'),
    ('Cột Ngày gửi duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Khoá sắp xếp mặc định (giảm dần).'),
    ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Sắp xếp được.'),
    ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu',
     'Chờ TP duyệt / Chờ BGĐ duyệt (cùng màu cam); sắp xếp được.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị',
     'Cột khoá. Gồm nút Duyệt (mở màn chi tiết, FR-06) và nút Lịch sử phê duyệt (FR-05).'),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', '20',
     '5 / 10 / 20 / 50 / 100; đổi giá trị thì quay về trang 1.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', '–'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện “Không có báo giá nào chờ duyệt.” khi N = 0.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Hiển thị', 'Hiện trong lúc nạp dữ liệu.'),
    ('Thông báo lỗi tải', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
     '“Lỗi tải dữ liệu” khi nạp danh sách thất bại.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'During:\n– Khôi phục bộ lọc đã lưu trong 10 phút gần nhất (nếu có) và cấu hình cột của '
     'người dùng.\n– Áp phạm vi hàng chờ: Q1 → Chờ TP duyệt thuộc phòng ban quản lý; Q2 → Chờ BGĐ '
     'duyệt thuộc công ty mình; chỉ lấy báo giá thường.\n'
     'After:\n– Trả về trang 1, sắp xếp Ngày gửi duyệt giảm dần, kèm tổng số bản ghi.'),
    ('Bấm vào Mã báo giá / nút Duyệt ở cột Hành động', 'Click',
     'After:\n– Mở màn chi tiết báo giá (FR-06). Bấm chuột phải cho phép mở ở tab mới.'),
    ('Bấm tiêu đề cột có sắp xếp', 'Click',
     'Before:\n– Chỉ các cột Mã báo giá, Khách hàng, Tổng giá trị sau VAT, Cấp duyệt, Ngày gửi '
     'duyệt, Ngày tạo, Ngày cập nhật, Trạng thái hỗ trợ sắp xếp.\n'
     'After:\n– Đổi chiều sắp xếp, quay về trang 1 và nạp lại danh sách.'),
    ('Bấm số trang / nút tiến lùi', 'Click',
     'After:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp, nạp dữ liệu trang mới.'),
    ('Đổi Số dòng/trang', 'Change', 'After:\n– Quay về trang 1 và nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.2 FR-02
d.h3('2.2 Tìm kiếm và lọc')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang. Chỉ bổ sung các tiêu chí '
           'tìm kiếm/lọc riêng của Báo giá chờ duyệt.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc báo giá chờ duyệt',
    mota='Thu hẹp hàng chờ theo mã báo giá / tên khách hàng, cấp tổ chức, người lập, dự án TKT, '
         'giai đoạn dự án, cấp duyệt và khoảng ngày tạo. Bộ lọc chỉ thu hẹp trong hàng chờ của '
         'người đăng nhập, không mở rộng ra ngoài.',
    tacnhan=A_BOTH,
    dieukien='Người dùng đang ở màn Báo giá chờ duyệt.',
    chinh='1. Người dùng nhập từ khoá vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Người dùng bấm Tìm kiếm nâng cao để mở khối tiêu chí.\n'
          '3. Người dùng chọn giá trị cho một hoặc nhiều tiêu chí.\n'
          '4. Hệ thống lọc ngay khi giá trị thay đổi và quay về trang 1.\n'
          '5. Hệ thống ghi nhớ bộ lọc trong 10 phút để khôi phục khi quay lại màn hình.',
    phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, nạp lại danh sách từ trang 1.\n'
        '• Không có kết quả → bảng hiện “Không có báo giá nào chờ duyệt.”.\n'
        '• Bấm Ẩn tìm kiếm nâng cao → thu gọn khối tiêu chí, giá trị đang lọc vẫn giữ.',
    dacbiet='Màn hình không có ô lọc Trạng thái vì hệ thống đã cố định hàng chờ theo quyền của '
            'người đăng nhập. Các ô Công ty / Phòng ban / Bộ phận / Nhân viên chỉ hiện theo quyền '
            'V1–V4 (Phần 2).')

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-bo-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao đang mở')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Placeholder “Tìm theo mã báo giá, tên khách hàng”; tìm gần đúng; chỉ lọc khi bấm Tìm kiếm '
     'hoặc Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp ô tìm nhanh, quay về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa toàn bộ tiêu chí đang lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở / thu gọn khối tiêu chí; khi mở nhãn đổi thành “Ẩn tìm kiếm nâng cao”.'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ FR-03.'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống', 'Chỉ hiện với V1.'),
    ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Hiện với V1, V2, V3; liệt kê phòng ban theo công ty đang chọn.'),
    ('Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống', 'Hiện với V1–V4.'),
    ('Nhân viên', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Hiện với V1–V4; lọc theo người lập báo giá.'),
    ('Dự án TKT', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Hiển thị dạng “Mã - Tên dự án”.'),
    ('Giai đoạn dự án', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Có icon ⓘ xem mô tả giai đoạn.'),
    ('Cấp duyệt', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
     'Cấp 2 — TP duyệt / Cấp 3 — TP & BGĐ duyệt.'),
    ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Khoảng từ ngày – đến ngày, lấy trọn ngày ở hai đầu.'),
])

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Đổi giá trị một tiêu chí trong Tìm kiếm nâng cao', 'Change',
     'During:\n– Ghi nhận giá trị mới, ghi nhớ bộ lọc trong 10 phút.\n'
     'After:\n– Quay về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí, vẫn trong phạm vi '
     'hàng chờ của người dùng.'),
    ('Bấm nút Tìm kiếm / nhấn Enter ở ô tìm nhanh', 'Click',
     'After:\n– Lọc theo mã báo giá hoặc tên khách hàng chứa từ khoá, quay về trang 1.'),
    ('Bấm nút Làm mới', 'Click',
     'After:\n– Đặt lại toàn bộ tiêu chí về trống, sắp xếp về mặc định, nạp lại đúng một lần.'),
    ('Đổi Công ty', 'Change',
     'After:\n– Nạp lại danh sách phòng ban theo công ty mới và nạp lại danh sách báo giá.'),
])

# ---------------------------------------------------------------- 2.3 FR-03
d.h3('2.3 Cài đặt bộ lọc')

d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc', 'view', actor='Người dùng đã đăng nhập',
            caption='Biểu đồ Use Case — FR-03 Cài đặt bộ lọc')

d.p('2.3.2 Giới thiệu')
d.rule_ref('- Cấu hình bộ lọc. Chỉ bổ sung danh sách tiêu chí lọc riêng của Báo giá chờ duyệt.',
           anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Mỗi người dùng tự chọn những tiêu chí lọc muốn hiển thị trong khối Tìm kiếm nâng cao và '
         'sắp xếp lại thứ tự của chúng. Cấu hình lưu riêng theo người dùng và riêng cho màn Báo '
         'giá chờ duyệt.',
    tacnhan=A_BOTH,
    dieukien='Người dùng đang ở màn Báo giá chờ duyệt.',
    chinh='1. Người dùng bấm nút Cài đặt bộ lọc.\n'
          '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 5 tiêu chí kèm ô tích, trạng thái tích '
          'theo cấu hình đang áp dụng.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng kéo thả để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống ghi nhận, hiển thị “Cập nhật thành công”, đóng cửa sổ và áp ngay lên khối '
          'Tìm kiếm nâng cao.',
    phu='• Bấm Khôi phục mặc định → tích lại đủ 5 tiêu chí theo thứ tự gốc; phải bấm Lưu mới có '
        'hiệu lực.\n'
        '• Bấm Đóng hoặc dấu × → thoát, không lưu thay đổi.\n'
        '• Bỏ tích một tiêu chí đang có giá trị lọc → giá trị đó bị xóa để danh sách không bị lọc '
        'ngầm.\n'
        '• Lưu thất bại → hiển thị “Thao tác thất bại”.',
    dacbiet='Không có tiêu chí nào bị khóa — mọi tiêu chí đều ẩn được. Ô tiêu chí “Công ty – Phòng '
            'ban – Bộ phận – Người lập” là một nhóm, bật / tắt cả 4 ô cùng lúc; các ô trong nhóm '
            'vẫn chỉ hiện theo quyền V1–V4.')

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', modal='Cài đặt bộ lọc',
         shot=shot('03-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')

d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', 'Kèm biểu tượng bánh răng.'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Tích chọn trường lọc muốn hiển thị; kéo … để sắp xếp thứ tự. Cài đặt được lưu theo từng '
     'màn hình.”'),
    ('Ô tích từng tiêu chí', 'Checkbox', 'Enable', 'Danh sách 5 tiêu chí', 'Không',
     'Theo cấu hình đã lưu (mặc định tích hết)',
     'Công ty – Phòng ban – Bộ phận – Người lập; Dự án TKT; Giai đoạn dự án; Cấp duyệt; Ngày tạo.'),
    ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Kéo để đổi thứ tự tiêu chí trong khối Tìm kiếm nâng cao.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Ghi cấu hình cho người dùng hiện tại; bị khóa trong lúc đang lưu.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đưa về đủ 5 tiêu chí theo thứ tự gốc, chưa ghi.'),
    ('Nút Đóng / dấu ×', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Cập nhật thành công” / “Thao tác thất bại”.'),
])

d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Cài đặt bộ lọc', 'Click',
     'After:\n– Mở cửa sổ với danh sách và thứ tự tiêu chí theo cấu hình đang áp dụng.'),
    ('Tích / bỏ tích, kéo thả tiêu chí', 'Change',
     'After:\n– Chỉ thay đổi trong cửa sổ, chưa áp lên màn hình cho tới khi bấm Lưu.'),
    ('Bấm nút Lưu', 'Click',
     'During:\n– Ghi cấu hình (tiêu chí hiển thị + thứ tự) theo người dùng và theo màn Báo giá chờ '
     'duyệt.\n'
     'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, sắp xếp lại khối Tìm kiếm nâng cao; '
     'tiêu chí bị ẩn thì xóa giá trị đang lọc của nó.\n– Lỗi → hiển thị “Thao tác thất bại”.'),
    ('Bấm Khôi phục mặc định', 'Click',
     'After:\n– Tích lại đủ 5 tiêu chí theo thứ tự gốc; chưa lưu cho tới khi bấm Lưu.'),
    ('Bấm nút Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, giữ nguyên cấu hình đang áp dụng.'),
])

# ---------------------------------------------------------------- 2.4 FR-04
d.h3('2.4 Tùy chỉnh cột')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tùy chỉnh cột', 'view', actor='Người dùng đã đăng nhập',
            caption='Biểu đồ Use Case — FR-04 Tùy chỉnh cột')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Tùy chỉnh cột. Chỉ bổ sung bộ cột riêng của Báo giá chờ duyệt.', anchor='excel')
d.intro_table(
    ten='Tùy chỉnh cột hiển thị',
    mota='Mỗi người dùng tự chọn những cột muốn thấy trên bảng Báo giá chờ duyệt và sắp xếp lại '
         'thứ tự. Cấu hình lưu riêng theo người dùng và riêng cho màn này (không dùng chung với '
         'màn Danh sách báo giá).',
    tacnhan=A_BOTH,
    dieukien='Người dùng đang ở màn Báo giá chờ duyệt.',
    chinh='1. Người dùng bấm nút Cấu hình cột hiển thị (biểu tượng cột) cạnh nút Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ “Tùy chỉnh cột” liệt kê đủ 17 cột kèm ô tích.\n'
          '3. Người dùng tích / bỏ tích và kéo thả các cột không bị khóa để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống ghi nhận, hiển thị “Cập nhật thành công”, đóng cửa sổ và vẽ lại bảng.',
    phu='• Bấm Đóng hoặc dấu × → thoát, trả danh sách cột về cấu hình đang áp dụng.\n'
        '• Lưu thất bại → hiển thị “Thao tác thất bại”.\n'
        '• Chưa từng lưu cấu hình → bảng hiện đủ 17 cột theo thứ tự mặc định.',
    dacbiet='Ba cột STT, Mã báo giá, Hành động bị khóa: luôn hiển thị, không bỏ tích và không kéo '
            'đổi vị trí được (hiện biểu tượng ổ khóa). Bảng chờ duyệt không có cột giá vốn nên '
            'không có cột nào ẩn / hiện theo quyền Xem giá vốn hàng hoá.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tùy chỉnh cột', modal='Tùy chỉnh cột',
         shot=shot('04-tuy-chinh-cot.png'), shot_caption='Cửa sổ Tùy chỉnh cột')

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Tùy chỉnh cột', 'Kèm biểu tượng cột.'),
    ('Ô tích từng cột', 'Checkbox', 'Enable / Disable', 'Danh sách 17 cột', 'Không',
     'Theo cấu hình đã lưu (mặc định tích hết)',
     'STT, Mã báo giá, Loại báo giá, BOM list, Dự án TKT, Khách hàng, Giai đoạn dự án, Tiền tệ, '
     'Tổng giá trị sau VAT, Cấp duyệt, Người gửi duyệt, Ngày gửi duyệt, Ngày tạo, Người cập nhật, '
     'Ngày cập nhật, Trạng thái, Hành động.'),
    ('Dòng cột bị khóa', 'Checkbox', 'Disable', 'STT, Mã báo giá, Hành động', '–', 'Luôn tích',
     'Hiện xám kèm ổ khóa, tooltip “Cột bắt buộc — không thể ẩn hoặc đổi vị trí”; không kéo được.'),
    ('Kéo thả dòng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Chỉ các cột không bị khóa; cột khóa luôn giữ vị trí gốc.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình và vẽ lại bảng.'),
    ('Nút Đóng / dấu ×', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Cập nhật thành công” / “Thao tác thất bại”.'),
])

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Cấu hình cột hiển thị', 'Click',
     'After:\n– Mở cửa sổ liệt kê đủ 17 cột theo thứ tự và trạng thái tích đang áp dụng.'),
    ('Kéo thả một dòng cột', 'Change',
     'Before:\n– Dòng cột bị khóa không kéo được.\n'
     'After:\n– Đổi thứ tự trong cửa sổ, chưa áp lên bảng.'),
    ('Bấm nút Lưu', 'Click',
     'During:\n– Ghi cấu hình cột (hiển thị + thứ tự) theo người dùng và theo màn Báo giá chờ duyệt.\n'
     'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng; cột khóa được chèn lại '
     'đúng vị trí gốc.\n– Lỗi → hiển thị “Thao tác thất bại”.'),
    ('Bấm nút Đóng / dấu ×', 'Click',
     'After:\n– Đóng cửa sổ, trả lại cấu hình cột đang áp dụng.'),
])

# ---------------------------------------------------------------- 2.5 FR-05
d.h3('2.5 Xem lịch sử phê duyệt')

d.p('2.5.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử. Chỉ bổ sung các mốc riêng của báo giá.', anchor='history')
d.intro_table(
    ten='Xem lịch sử phê duyệt báo giá',
    mota='Xem nhanh dòng thời gian thao tác của một báo giá (tạo, gửi duyệt kèm cấp, TP duyệt, '
         'TP duyệt & chuyển BGĐ, BGĐ duyệt, từ chối…) ngay trên màn danh sách, không cần mở chi '
         'tiết.',
    tacnhan=A_BOTH,
    dieukien='Người dùng đang ở màn Báo giá chờ duyệt và danh sách có ít nhất một báo giá.',
    chinh='1. Người dùng bấm nút Lịch sử phê duyệt ở cột Hành động.\n'
          '2. Hệ thống mở cửa sổ “Lịch sử báo giá” và nạp các mốc, mới nhất lên trước.\n'
          '3. Mỗi mốc hiển thị tên thao tác (kèm nhãn Cấp N khi gửi duyệt), người thực hiện, '
          'trạng thái trước → sau và thời điểm.',
    phu='• Chưa có mốc nào → hiện “Chưa có lịch sử”.\n'
        '• Nạp thất bại → hiển thị “Không tải được lịch sử”.\n'
        '• Bấm Đóng hoặc dấu × → đóng cửa sổ.',
    dacbiet=None)

d.p('2.5.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử phê duyệt', modal='Lịch sử báo giá',
         shot=shot('06-lich-su.png'), shot_caption='Cửa sổ Lịch sử báo giá')

d.p('2.5.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Lịch sử báo giá', '–'),
    ('Tên thao tác', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Tạo báo giá, Lưu nháp, Gửi duyệt, Tự duyệt, TP duyệt, TP duyệt & chuyển BGĐ, BGĐ duyệt, '
     'Từ chối, …; mỗi thao tác một màu và biểu tượng riêng.'),
    ('Nhãn Cấp N', 'Badge', 'Read-only', 'Cấp 1 / 2 / 3', 'Theo dữ liệu',
     'Chỉ có ở mốc gửi duyệt.'),
    ('Người thực hiện', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Không xác định → “Hệ thống”.'),
    ('Trạng thái trước → sau', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Vd: Đang tạo → Chờ TP duyệt.'),
    ('Lý do', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Có ở mốc Từ chối.'),
    ('Thời điểm', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử”.'),
], required=False)

d.p('2.5.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Lịch sử phê duyệt', 'Click',
     'During:\n– Hiện “Đang tải...” và nạp các mốc của báo giá.\n'
     'After:\n– Hiển thị dòng thời gian; lỗi → “Không tải được lịch sử”.'),
    ('Bấm nút Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, giữ nguyên màn danh sách.'),
])

# ---------------------------------------------------------------- 2.6 FR-06
d.h3('2.6 Xem chi tiết báo giá để duyệt')

d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Mục này chỉ đặc tả phần phục vụ phê duyệt; nội '
           'dung form báo giá đặc tả ở SRS Báo giá.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết báo giá để duyệt',
    mota='Mở màn chi tiết báo giá (chỉ đọc) để người duyệt đọc thông tin chung, bảng hàng hoá / '
         'dịch vụ, bảng Tổng hợp giá trị báo giá và TSLN rồi thực hiện Duyệt / Duyệt & chuyển BGĐ '
         '/ BGĐ duyệt / Từ chối tại thanh nút cuối màn.',
    tacnhan=A_BOTH,
    dieukien='Người dùng có Q1 hoặc Q2 và báo giá đang nằm trong hàng chờ duyệt của mình (hoặc nằm '
             'trong phạm vi xem V1–V4 / do chính mình lập).',
    chinh='1. Người dùng bấm Mã báo giá hoặc nút Duyệt ở cột Hành động.\n'
          '2. Hệ thống mở màn “Chi tiết báo giá: <mã>” kèm trạng thái và nhãn cấp duyệt trên '
          'thanh tiêu đề.\n'
          '3. Hệ thống hiển thị thông tin chung, bảng chi tiết, bảng Tổng hợp giá trị báo giá; giá '
          'nhập và TSLN chỉ hiện khi có quyền Q3.\n'
          '4. Thanh nút cuối màn hiện nút phê duyệt đúng với vai trò và trạng thái báo giá.',
    phu='• Báo giá vừa nằm ngoài hàng chờ của người dùng vừa ngoài phạm vi V1–V4 → màn hiện '
        '“Không tìm thấy báo giá.” và thông báo “Không tải được báo giá”.\n'
        '• Báo giá từng bị từ chối → đầu màn hiện khung “Đã bị từ chối: <lý do>”.\n'
        '• Báo giá thuộc dự án con có Báo giá Mỏ neo → hiện khung xác nhận đồng bộ hoặc cảnh báo '
        'các điểm lệch so với Báo giá Mỏ neo.\n'
        '• Bấm Quay lại → về màn trước đó (màn Báo giá chờ duyệt).',
    dacbiet='Nút phê duyệt hiển thị theo bảng: Q1 + Chờ TP duyệt cấp 2 → Duyệt; Q1 + Chờ TP duyệt '
            'cấp 3 → Duyệt & chuyển BGĐ; Q2 + Chờ BGĐ duyệt → BGĐ duyệt; Từ chối hiện cùng điều '
            'kiện với nút duyệt tương ứng. Không đủ điều kiện → nút ẩn hẳn, không hiện xám.')

d.p('2.6.2 Layout màn hình')
d.layout(menu=DETAIL, shot=shot('07-chi-tiet-cap2.png'),
         shot_caption='Màn chi tiết báo giá cấp 2 đang Chờ TP duyệt — thanh nút có Duyệt, Từ chối')
d.figure(shot('07b-tong-hop-gia-tri.png'),
         'Bảng Tổng hợp giá trị báo giá và TSLN (người có quyền Xem giá vốn hàng hoá)', width_in=6.2)

d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–', 'Chi tiết báo giá: <mã>',
     'Kèm (trạng thái) và nhãn cấp: Cấp 1 — Tự duyệt / Cấp 2 — TP duyệt / Cấp 3 — TP & BGĐ duyệt.'),
    ('Khung Đã bị từ chối', 'Toast / Alert', 'Enable / Ẩn', '–', 'Ẩn',
     'Hiện khi báo giá có lý do từ chối của lần duyệt trước.'),
    ('Khung đối chiếu Báo giá Mỏ neo', 'Toast / Alert', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ với báo giá dự án con có Mỏ neo.'),
    ('Khối Thông tin chung', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mã báo giá, YCBG, BOM list, Dự án, Giải pháp, Khách hàng, Hiệu lực, Giao hàng, Bảo hành, '
     'Loại tiền tệ, Giai đoạn dự án, Người lập…; thu gọn / mở được.'),
    ('Bảng Chi tiết báo giá', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Nhóm A Hàng hoá, B Dịch vụ & Chi phí khác. Cột giá nhập / thành tiền nhập hiển thị “—” khi '
     'không có Q3.'),
    ('Bảng Tổng hợp giá trị báo giá', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Hàng hoá / Dịch vụ / Chi phí / Vận chuyển / Tổng; dòng TSLN trước GG, TSLN sau GG chỉ hiện '
     'khi có Q3.'),
    ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', 'Mở ra mới nạp.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn trước đó.'),
    ('Nút Xuất Excel / In', 'Button', 'Enable', '–', 'Hiển thị',
     'Thao tác chỉ đọc; đặc tả ở SRS Báo giá.'),
    ('Nút Duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Hiện khi có Q1, báo giá Chờ TP duyệt và cấp 2 (FR-08).'),
    ('Nút Duyệt & chuyển BGĐ', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Hiện khi có Q1, báo giá Chờ TP duyệt và cấp 3 (FR-09).'),
    ('Nút BGĐ duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Hiện khi có Q2 và báo giá Chờ BGĐ duyệt (FR-10).'),
    ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Hiện khi (Q1 và Chờ TP duyệt) hoặc (Q2 và Chờ BGĐ duyệt) (FR-11).'),
], required=False)

d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Kiểm tra báo giá nằm trong phạm vi V1–V4 / do người dùng lập, HOẶC đang nằm '
     'trong hàng chờ duyệt của người dùng (cùng điều kiện với màn Báo giá chờ duyệt); không thoả '
     '→ hiện “Không tìm thấy báo giá.” và thông báo “Không tải được báo giá”.\n'
     'During:\n– Nạp báo giá, ngày đổi giá ERP của hàng hoá và kết quả đối chiếu Báo giá Mỏ neo.\n'
     '– Ẩn giá nhập / TSLN khi không có Q3.\n'
     'After:\n– Tính các nút phê duyệt theo quyền Q1/Q2, trạng thái và cấp duyệt.'),
    ('Bấm nút Quay lại', 'Click', 'After:\n– Về màn trước đó; mở ở tab mới thì về Danh sách báo giá.'),
    ('Bấm Duyệt / Duyệt & chuyển BGĐ / BGĐ duyệt / Từ chối', 'Click',
     'After:\n– Chuyển sang xử lý của FR-08 / FR-09 / FR-10 / FR-11.'),
])

# ---------------------------------------------------------------- 2.7 FR-07
d.h3('2.7 Xuất Excel')

d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xuất Excel', 'io', actor='Người duyệt giá (Q1 / Q2)',
            caption='Biểu đồ Use Case — FR-07 Xuất Excel')

d.p('2.7.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung bộ trường xuất riêng của Báo giá chờ '
           'duyệt.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách báo giá chờ duyệt',
    mota='Xuất ra file Excel toàn bộ báo giá trong hàng chờ khớp bộ lọc đang áp dụng (không giới '
         'hạn theo trang), với các trường người dùng chọn.',
    tacnhan=A_BOTH,
    dieukien='Người dùng có Q1 hoặc Q2 và đang ở màn Báo giá chờ duyệt.',
    chinh='1. Người dùng bấm Xuất Excel.\n'
          '2. Hệ thống mở popup “Chọn trường xuất file”, tích sẵn các trường đang hiện trên bảng.\n'
          '3. Người dùng tích / bỏ tích, kéo để đổi thứ tự cột trong file.\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống tải về file “danh_sach_bao_gia_cho_duyet.xlsx” và hiển thị “Xuất Excel '
          'thành công”.',
    phu='• Chưa chọn trường nào → nút Xuất file bị khoá.\n'
        '• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích toàn bộ.\n'
        '• Lỗi khi xuất → hiển thị “Lỗi khi xuất Excel”.\n'
        '• Không có Q1/Q2 → “Bạn không có quyền thực hiện chức năng này”.',
    dacbiet='Trong lúc đang xuất, nút Xuất Excel bị khoá để tránh bấm lặp.')

d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất file',
         shot=shot('05-xuat-excel.png'), shot_caption='Popup Chọn trường xuất file')

d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất file', '–'),
    ('Danh sách trường', 'Modal', 'Enable', 'Danh sách 15 trường', 'Có (≥ 1)',
     'Tích sẵn theo cột đang hiện',
     'Mã báo giá, Loại báo giá, Mã BOM, Dự án TKT, Khách hàng, Giai đoạn dự án, Tiền tệ, Tổng giá '
     'trị sau VAT, Cấp duyệt, Ngày gửi duyệt, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, '
     'Ngày cập nhật.'),
    ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Đổi thứ tự cột trong file.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Dòng “Đang chọn a/b trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Khoá khi chưa chọn trường nào hoặc đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])

d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xuất Excel', 'Click',
     'After:\n– Mở popup Chọn trường xuất file, tích sẵn các trường đang hiện trên bảng.'),
    ('Bấm nút Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'During:\n– Lấy toàn bộ báo giá trong hàng chờ khớp bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Tải file “danh_sach_bao_gia_cho_duyet.xlsx” (tiêu đề “Danh sách báo giá chờ '
     'duyệt”), cột theo đúng thứ tự đã chọn.\n– Hiển thị “Xuất Excel thành công”; lỗi → “Lỗi khi '
     'xuất Excel”.'),
])

# ---------------------------------------------------------------- 2.8 FR-08
d.h3('2.8 Duyệt báo giá cấp 2')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Duyệt báo giá cấp 2', 'action', actor=A_TP,
            caption='Biểu đồ Use Case — FR-08 Duyệt báo giá cấp 2')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Quy tắc đổi trạng thái, Thông báo và Quy tắc ghi lịch sử.', anchor='history')
d.intro_table(
    ten='Duyệt báo giá cấp 2 (Trưởng phòng chốt)',
    mota='Trưởng phòng duyệt báo giá cấp 2 đang Chờ TP duyệt. Đây là cấp cuối: báo giá chuyển '
         'thẳng sang Đã duyệt và kích hoạt các cập nhật liên quan.',
    tacnhan=A_TP,
    dieukien='Người dùng có Q1, quản lý phòng ban của báo giá; báo giá ở trạng thái Chờ TP duyệt '
             'và cấp duyệt = 2.',
    chinh='1. Người dùng mở màn chi tiết báo giá và bấm nút Duyệt.\n'
          '2. Hệ thống mở hộp “Xác nhận duyệt” với câu “Duyệt báo giá?”.\n'
          '3. Người dùng bấm Duyệt.\n'
          '4. Hệ thống kiểm tra quyền, phòng ban quản lý và trạng thái.\n'
          '5. Hệ thống tính lại tổng tiền, chuyển báo giá sang Đã duyệt, ghi người duyệt và thời '
          'điểm duyệt.\n'
          '6. Hệ thống cập nhật yêu cầu tính giá bán, dự án TKT, giải pháp; ghi lịch sử; gửi '
          'thông báo; đồng bộ báo giá sang ERP.\n'
          '7. Hệ thống hiển thị “Đã duyệt báo giá” và quay về màn Báo giá chờ duyệt (báo giá vừa '
          'duyệt không còn trong hàng chờ).',
    phu='• Bấm Huỷ ở hộp xác nhận → không thay đổi gì.\n'
        '• Không quản lý phòng ban của báo giá → “Bạn không quản lý phòng ban của báo giá này.”.\n'
        '• Báo giá đã được người khác xử lý → “Báo giá không ở trạng thái Chờ TP duyệt.”.\n'
        '• Đồng bộ ERP lỗi → báo giá vẫn Đã duyệt, lỗi được ghi nhận để xử lý sau.',
    dacbiet='Thao tác xong hệ thống quay về màn danh sách nơi người dùng đi vào: mở từ Báo giá chờ '
            'duyệt thì về Báo giá chờ duyệt; mở từ lối khác thì về trang trước đó.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=DETAIL + ' => Duyệt', shot=shot('08-xac-nhan-duyet.png'),
         shot_caption='Hộp Xác nhận duyệt của báo giá cấp 2')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Duyệt', 'Button', 'Enable / Ẩn', 'Ẩn khi thiếu quyền',
     'Ở thanh nút cuối màn chi tiết; xanh lá, biểu tượng dấu tích.'),
    ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Xác nhận duyệt', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Duyệt báo giá?', '–'),
    ('Nút Duyệt (trong hộp)', 'Button', 'Enable', 'Hiển thị', 'Thực hiện duyệt.'),
    ('Nút Huỷ', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không thay đổi.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     'Thành công: “Đã duyệt báo giá”. Lỗi: nội dung lỗi hệ thống trả về, mặc định “Lỗi duyệt”.'),
], required=False, scope=False)

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Duyệt ở thanh nút', 'Click',
     'Before:\n– Nút chỉ hiện khi có Q1, báo giá Chờ TP duyệt, cấp 2.\n'
     'After:\n– Mở hộp Xác nhận duyệt.'),
    ('Bấm Duyệt trong hộp xác nhận', 'Click',
     'Before:\n– Kiểm tra quyền Q1; không có → “Bạn không có quyền thực hiện chức năng này” và '
     'dừng.\n– Kiểm tra người dùng quản lý phòng ban của báo giá; không → “Bạn không quản lý '
     'phòng ban của báo giá này.” và dừng.\n'
     'During:\n– Báo giá không còn Chờ TP duyệt → “Báo giá không ở trạng thái Chờ TP duyệt.” và '
     'dừng.\n'
     'After:\n– Tính lại tổng tiền; chuyển báo giá sang Đã duyệt, ghi người duyệt và thời điểm.\n'
     '– Yêu cầu tính giá bán liên kết → Đã có báo giá; dự án TKT → Thương thảo giá và giải pháp '
     '(tính lại mốc tự đóng dự án); giải pháp → Đã duyệt giá.\n'
     '– Ghi lịch sử “TP duyệt” (Chờ TP duyệt → Đã duyệt).\n'
     '– Gửi thông báo cho người lập, nhân viên kinh doanh phụ trách dự án và Trưởng phòng duyệt '
     'giá của phòng ban báo giá.\n– Đồng bộ báo giá sang ERP.\n'
     '– Hiển thị “Đã duyệt báo giá”, quay về màn danh sách nơi người dùng đi vào (Báo giá chờ duyệt).'),
    ('Bấm Huỷ', 'Click', 'After:\n– Đóng hộp, báo giá giữ nguyên.'),
])

# ---------------------------------------------------------------- 2.9 FR-09
d.h3('2.9 Duyệt & chuyển BGĐ')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Duyệt & chuyển BGĐ', 'action', actor=A_TP,
            caption='Biểu đồ Use Case — FR-09 Duyệt & chuyển BGĐ')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc đổi trạng thái, Thông báo và Quy tắc ghi lịch sử.', anchor='history')
d.intro_table(
    ten='Duyệt & chuyển BGĐ (báo giá cấp 3)',
    mota='Trưởng phòng duyệt bước một của báo giá cấp 3; báo giá chuyển sang Chờ BGĐ duyệt và '
         'đi vào hàng chờ của Ban giám đốc.',
    tacnhan=A_TP,
    dieukien='Người dùng có Q1, quản lý phòng ban của báo giá; báo giá ở trạng thái Chờ TP duyệt '
             'và cấp duyệt = 3.',
    chinh='1. Người dùng mở màn chi tiết báo giá và bấm nút Duyệt & chuyển BGĐ.\n'
          '2. Hệ thống mở hộp “Xác nhận duyệt” với câu “Duyệt & chuyển BGĐ?”.\n'
          '3. Người dùng bấm Duyệt.\n'
          '4. Hệ thống kiểm tra quyền, phòng ban quản lý và trạng thái.\n'
          '5. Hệ thống tính lại tổng tiền, chuyển báo giá sang Chờ BGĐ duyệt, ghi người duyệt TP và '
          'thời điểm.\n'
          '6. Hệ thống ghi lịch sử, gửi thông báo cho người có quyền Q2 thuộc công ty của báo giá.\n'
          '7. Hệ thống hiển thị “Đã duyệt báo giá” và quay về màn Báo giá chờ duyệt.',
    phu='• Bấm Huỷ ở hộp xác nhận → không thay đổi gì.\n'
        '• Không quản lý phòng ban của báo giá → “Bạn không quản lý phòng ban của báo giá này.”.\n'
        '• Báo giá đã được người khác xử lý → “Báo giá không ở trạng thái Chờ TP duyệt.”.',
    dacbiet='Ở bước này báo giá CHƯA được duyệt: chưa cập nhật dự án / giải pháp / yêu cầu tính '
            'giá bán và chưa đồng bộ ERP. Các cập nhật đó chỉ chạy khi BGĐ duyệt (FR-10).')

d.p('2.9.3 Layout màn hình')
d.layout(menu=DETAIL + ' => Duyệt & chuyển BGĐ', shot=shot('09-chi-tiet-cap3.png'),
         shot_caption='Màn chi tiết báo giá cấp 3 — thanh nút có Duyệt & chuyển BGĐ, Từ chối')
d.figure(shot('10-xac-nhan-chuyen-bgd.png'), 'Hộp Xác nhận duyệt của báo giá cấp 3', width_in=6.2)

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Duyệt & chuyển BGĐ', 'Button', 'Enable / Ẩn', 'Ẩn khi thiếu quyền',
     'Ở thanh nút cuối màn chi tiết; cùng vị trí với nút Duyệt, nhãn đổi theo cấp 3.'),
    ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Xác nhận duyệt', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Duyệt & chuyển BGĐ?', '–'),
    ('Nút Duyệt (trong hộp)', 'Button', 'Enable', 'Hiển thị', 'Thực hiện duyệt và chuyển BGĐ.'),
    ('Nút Huỷ', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không thay đổi.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     'Thành công: “Đã duyệt báo giá”. Lỗi: nội dung lỗi hệ thống trả về, mặc định “Lỗi duyệt”.'),
], required=False, scope=False)

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Duyệt & chuyển BGĐ', 'Click',
     'Before:\n– Nút chỉ hiện khi có Q1, báo giá Chờ TP duyệt, cấp 3.\n'
     'After:\n– Mở hộp Xác nhận duyệt.'),
    ('Bấm Duyệt trong hộp xác nhận', 'Click',
     'Before:\n– Kiểm tra quyền Q1; không có → “Bạn không có quyền thực hiện chức năng này” và '
     'dừng.\n– Kiểm tra người dùng quản lý phòng ban của báo giá; không → “Bạn không quản lý '
     'phòng ban của báo giá này.” và dừng.\n'
     'During:\n– Báo giá không còn Chờ TP duyệt → “Báo giá không ở trạng thái Chờ TP duyệt.” và '
     'dừng.\n'
     'After:\n– Tính lại tổng tiền; chuyển báo giá sang Chờ BGĐ duyệt, ghi người duyệt TP và thời '
     'điểm.\n– Ghi lịch sử “TP duyệt & chuyển BGĐ” (Chờ TP duyệt → Chờ BGĐ duyệt).\n'
     '– Gửi thông báo “<người duyệt> TP đã duyệt & chuyển BGĐ <mã báo giá>” cho người có quyền '
     'Q2 thuộc công ty của báo giá, kèm liên kết tới màn Báo giá chờ duyệt.\n'
     '– Hiển thị “Đã duyệt báo giá”, quay về màn danh sách nơi người dùng đi vào (Báo giá chờ duyệt).'),
    ('Bấm Huỷ', 'Click', 'After:\n– Đóng hộp, báo giá giữ nguyên.'),
])

# ---------------------------------------------------------------- 2.10 FR-10
d.h3('2.10 BGĐ duyệt báo giá')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'BGĐ duyệt báo giá', 'action', actor=A_BGD,
            caption='Biểu đồ Use Case — FR-10 BGĐ duyệt báo giá')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc đổi trạng thái, Thông báo và Quy tắc ghi lịch sử.', anchor='history')
d.intro_table(
    ten='BGĐ duyệt báo giá (cấp cuối của báo giá cấp 3)',
    mota='Ban giám đốc duyệt báo giá cấp 3 đã qua Trưởng phòng. Báo giá chuyển sang Đã duyệt và '
         'kích hoạt các cập nhật liên quan.',
    tacnhan=A_BGD,
    dieukien='Người dùng có Q2, thuộc cùng công ty với báo giá; báo giá ở trạng thái Chờ BGĐ duyệt.',
    chinh='1. Người dùng mở màn chi tiết báo giá và bấm nút BGĐ duyệt.\n'
          '2. Hệ thống mở hộp “Xác nhận duyệt” với câu “BGĐ duyệt báo giá?”.\n'
          '3. Người dùng bấm Duyệt.\n'
          '4. Hệ thống kiểm tra quyền, công ty và trạng thái.\n'
          '5. Hệ thống tính lại tổng tiền, chuyển báo giá sang Đã duyệt, ghi người duyệt và thời '
          'điểm duyệt.\n'
          '6. Hệ thống cập nhật yêu cầu tính giá bán, dự án TKT, giải pháp; ghi lịch sử; gửi '
          'thông báo; đồng bộ báo giá sang ERP.\n'
          '7. Hệ thống hiển thị “BGĐ đã duyệt báo giá” và quay về màn Báo giá chờ duyệt.',
    phu='• Bấm Huỷ ở hộp xác nhận → không thay đổi gì.\n'
        '• Khác công ty với báo giá → “Bạn không thuộc công ty của báo giá này.”.\n'
        '• Báo giá đã được người khác xử lý → “Báo giá không ở trạng thái Chờ BGĐ duyệt.”.\n'
        '• Đồng bộ ERP lỗi → báo giá vẫn Đã duyệt, lỗi được ghi nhận để xử lý sau.',
    dacbiet=None)

d.p('2.10.3 Layout màn hình')
d.layout(menu=DETAIL + ' => BGĐ duyệt', shot=shot('13-chi-tiet-cho-bgd.png'),
         shot_caption='Màn chi tiết báo giá Chờ BGĐ duyệt — thanh nút có BGĐ duyệt, Từ chối')
d.figure(shot('14-xac-nhan-bgd.png'), 'Hộp Xác nhận duyệt của Ban giám đốc', width_in=6.2)

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút BGĐ duyệt', 'Button', 'Enable / Ẩn', 'Ẩn khi thiếu quyền',
     'Ở thanh nút cuối màn chi tiết; xanh lá, biểu tượng hai dấu tích.'),
    ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Xác nhận duyệt', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'BGĐ duyệt báo giá?', '–'),
    ('Nút Duyệt (trong hộp)', 'Button', 'Enable', 'Hiển thị', 'Thực hiện duyệt.'),
    ('Nút Huỷ', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không thay đổi.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     'Thành công: “BGĐ đã duyệt báo giá”. Lỗi: nội dung lỗi hệ thống trả về, mặc định “Lỗi duyệt”.'),
], required=False, scope=False)

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút BGĐ duyệt', 'Click',
     'Before:\n– Nút chỉ hiện khi có Q2 và báo giá Chờ BGĐ duyệt.\n'
     'After:\n– Mở hộp Xác nhận duyệt.'),
    ('Bấm Duyệt trong hộp xác nhận', 'Click',
     'Before:\n– Kiểm tra quyền Q2; không có → “Bạn không có quyền thực hiện chức năng này” và '
     'dừng.\n– Kiểm tra người dùng cùng công ty với báo giá; không → “Bạn không thuộc công ty của '
     'báo giá này.” và dừng.\n'
     'During:\n– Báo giá không còn Chờ BGĐ duyệt → “Báo giá không ở trạng thái Chờ BGĐ duyệt.” và '
     'dừng.\n'
     'After:\n– Tính lại tổng tiền; chuyển báo giá sang Đã duyệt, ghi người duyệt và thời điểm.\n'
     '– Yêu cầu tính giá bán liên kết → Đã có báo giá; dự án TKT → Thương thảo giá và giải pháp '
     '(tính lại mốc tự đóng dự án); giải pháp → Đã duyệt giá.\n'
     '– Ghi lịch sử “BGĐ duyệt” (Chờ BGĐ duyệt → Đã duyệt).\n'
     '– Gửi thông báo cho người lập, nhân viên kinh doanh phụ trách dự án và Trưởng phòng duyệt '
     'giá của phòng ban báo giá.\n– Đồng bộ báo giá sang ERP.\n'
     '– Hiển thị “BGĐ đã duyệt báo giá”, quay về màn danh sách nơi người dùng đi vào (Báo giá chờ duyệt).'),
    ('Bấm Huỷ', 'Click', 'After:\n– Đóng hộp, báo giá giữ nguyên.'),
])

# ---------------------------------------------------------------- 2.11 FR-11
d.h3('2.11 Từ chối báo giá')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Từ chối báo giá', 'action', actor='Người duyệt giá (Q1 / Q2)',
            caption='Biểu đồ Use Case — FR-11 Từ chối báo giá')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc đổi trạng thái, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.',
           anchor='history')
d.intro_table(
    ten='Từ chối báo giá',
    mota='Trưởng phòng (với báo giá Chờ TP duyệt) hoặc Ban giám đốc (với báo giá Chờ BGĐ duyệt) '
         'từ chối báo giá kèm lý do bắt buộc. Báo giá quay về Đang tạo để người lập chỉnh sửa và '
         'gửi duyệt lại.',
    tacnhan=A_BOTH,
    dieukien='(Q1, quản lý phòng ban của báo giá, báo giá Chờ TP duyệt) hoặc (Q2, cùng công ty, '
             'báo giá Chờ BGĐ duyệt).',
    chinh='1. Người dùng mở màn chi tiết báo giá và bấm nút Từ chối.\n'
          '2. Hệ thống mở popup “Từ chối báo giá” với ô Lý do từ chối để trống.\n'
          '3. Người dùng nhập lý do và bấm Xác nhận từ chối.\n'
          '4. Hệ thống kiểm tra lý do, trạng thái, quyền và phạm vi.\n'
          '5. Hệ thống chuyển báo giá về Đang tạo, lưu lý do, xóa mốc gửi duyệt / người duyệt / '
          'cấp duyệt.\n'
          '6. Hệ thống ghi lịch sử, gửi thông báo cho người lập.\n'
          '7. Hệ thống hiển thị “Đã từ chối báo giá”, đóng popup và quay về màn Báo giá chờ duyệt.',
    phu='• Lý do trống hoặc chỉ có khoảng trắng → chữ đỏ dưới ô “Vui lòng nhập lý do từ chối”, '
        'popup không đóng, không gửi lên hệ thống.\n'
        '• Báo giá không còn ở trạng thái chờ duyệt → “Báo giá không ở trạng thái chờ duyệt.”.\n'
        '• Không quản lý phòng ban / khác công ty → “Bạn không quản lý phòng ban của báo giá này.” '
        '/ “Bạn không thuộc công ty của báo giá này.”.\n'
        '• Bấm Huỷ hoặc dấu × → đóng popup, báo giá không đổi; mở lại thì ô lý do trống.',
    dacbiet='Báo giá bị từ chối mất cấp duyệt cũ: khi người lập sửa và gửi duyệt lại, hệ thống '
            'tính lại cấp duyệt theo số liệu mới. Lý do từ chối hiển thị ở đầu màn chi tiết cho '
            'tới lần gửi duyệt tiếp theo.')

d.p('2.11.3 Layout màn hình')
d.layout(menu=DETAIL + ' => Từ chối', modal='Từ chối báo giá',
         shot=shot('11-tu-choi.png'), shot_caption='Popup Từ chối báo giá')
d.figure(shot('12-tu-choi-loi.png'), 'Báo lỗi khi bấm Xác nhận từ chối mà chưa nhập lý do',
         width_in=6.2)

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi thiếu quyền',
     'Ở thanh nút cuối màn chi tiết; màu đỏ.'),
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Từ chối báo giá', '–'),
    ('Lý do từ chối', 'Textarea', 'Enable', '1–1000 ký tự', 'Có', 'Trống',
     'Placeholder “Nhập lý do từ chối...”; nhãn có dấu * đỏ.'),
    ('Thông báo lỗi dưới ô', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
     '“Vui lòng nhập lý do từ chối” (chữ đỏ).'),
    ('Nút Huỷ', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Khoá trong lúc đang gửi.'),
    ('Nút Xác nhận từ chối', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Màu đỏ; trong lúc gửi đổi nhãn “Đang gửi...” và bị khoá.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Thành công: “Đã từ chối báo giá”. Lỗi: nội dung hệ thống trả về, mặc định “Không thể từ '
     'chối”.'),
])

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Từ chối ở thanh nút', 'Click',
     'Before:\n– Nút chỉ hiện khi (Q1 và Chờ TP duyệt) hoặc (Q2 và Chờ BGĐ duyệt).\n'
     'After:\n– Mở popup với ô lý do trống, xóa lỗi cũ.'),
    ('Bấm Xác nhận từ chối', 'Click',
     'Before:\n– Lý do trống / chỉ khoảng trắng → hiển thị “Vui lòng nhập lý do từ chối” và dừng, '
     'không gửi lên hệ thống.\n'
     '– Kiểm tra quyền Q1/Q2; không có → “Bạn không có quyền thực hiện chức năng này” và dừng.\n'
     'During:\n– Báo giá không ở Chờ TP duyệt / Chờ BGĐ duyệt → “Báo giá không ở trạng thái chờ '
     'duyệt.” và dừng.\n– Chờ TP duyệt: phải có Q1 và quản lý phòng ban của báo giá; Chờ BGĐ duyệt: '
     'phải có Q2 và cùng công ty — sai → thông báo tương ứng và dừng.\n'
     '– Lý do vượt 1000 ký tự → hệ thống từ chối lưu.\n'
     'After:\n– Chuyển báo giá về Đang tạo, lưu lý do; xóa ngày gửi duyệt, người / ngày TP duyệt, '
     'người / ngày duyệt và cấp duyệt.\n'
     '– Ghi lịch sử “Từ chối” kèm lý do.\n'
     '– Gửi thông báo “<người từ chối> từ chối báo giá <mã>. Lý do: <lý do>” cho người lập.\n'
     '– Hiển thị “Đã từ chối báo giá”, đóng popup, quay về màn danh sách nơi người dùng đi vào (Báo giá chờ duyệt).'),
    ('Bấm Huỷ / dấu ×', 'Click', 'After:\n– Đóng popup, báo giá giữ nguyên.'),
])

# ==================================================== PHẦN 4. QUY TẮC NGHIỆP VỤ
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Báo giá chờ duyệt; không lặp lại các quy '
           'tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')

d.rule_table([
    ('BR-01', 'Cách tính cấp duyệt', [
        '– Cấp duyệt được tính tại thời điểm người lập gửi duyệt, theo Cấu hình duyệt giá.',
        '– Hệ thống xét 3 tiêu chí: giá trị đơn hàng (doanh thu quy đổi VND), tỷ suất lợi nhuận '
        'tổng và tỷ suất lợi nhuận của dòng hàng tạm. Mỗi tiêu chí rơi vào ngưỡng nào (từ ≤ giá '
        'trị < đến) thì lấy cấp của ngưỡng đó; không khớp ngưỡng nào thì lấy cấp 3.',
        '– Cấp duyệt của báo giá = cấp CAO NHẤT trong 3 tiêu chí.',
        '– Báo giá “sạch” (chỉ hàng / dịch vụ ERP, mọi đơn giá bán > 1.000, không có giảm giá) '
        'luôn là Cấp 1 — Tự duyệt, bất kể ngưỡng.',
    ], ['Gửi duyệt (màn Báo giá)', 'Xem danh sách']),

    ('BR-02', 'Luồng duyệt theo cấp', [
        '– Cấp 1: người lập tự duyệt, báo giá không vào màn Báo giá chờ duyệt.',
        '– Cấp 2: Chờ TP duyệt → Trưởng phòng duyệt → Đã duyệt.',
        '– Cấp 3: Chờ TP duyệt → Trưởng phòng Duyệt & chuyển BGĐ → Chờ BGĐ duyệt → Ban giám đốc '
        'duyệt → Đã duyệt.',
        '– Ở bất kỳ bước chờ nào, người duyệt của bước đó đều có thể Từ chối.',
    ], ['Duyệt báo giá cấp 2', 'Duyệt & chuyển BGĐ', 'BGĐ duyệt', 'Từ chối']),

    ('BR-03', 'Phạm vi hàng chờ duyệt', [
        '– Q1: báo giá Chờ TP duyệt thuộc các phòng ban người dùng được giao quản lý (kể cả cấu '
        'hình quản lý tất cả phòng ban).',
        '– Q2: báo giá Chờ BGĐ duyệt thuộc công ty của người dùng.',
        '– Có cả Q1 và Q2: thấy hợp của hai nhóm.',
        '– Không có quyền, hoặc có Q1 mà không quản lý phòng ban nào: hàng chờ rỗng.',
        '– Báo giá tổng không vào hàng chờ này (có luồng duyệt riêng).',
    ], ['Xem danh sách', 'Tìm kiếm và lọc', 'Xuất Excel']),

    ('BR-04', 'Điều kiện được thực hiện thao tác duyệt / từ chối', [
        '– Trưởng phòng chỉ duyệt / từ chối báo giá Chờ TP duyệt thuộc phòng ban mình quản lý.',
        '– Ban giám đốc chỉ duyệt / từ chối báo giá Chờ BGĐ duyệt thuộc công ty mình.',
        '– Hệ thống kiểm tra lại trạng thái tại thời điểm bấm: báo giá đã được người khác xử lý '
        'thì thao tác bị từ chối kèm thông báo.',
        '– Nút không đủ điều kiện bị ẩn hẳn ở màn chi tiết, không hiện xám.',
    ], ['Duyệt báo giá cấp 2', 'Duyệt & chuyển BGĐ', 'BGĐ duyệt', 'Từ chối']),

    ('BR-05', 'Quyền mở màn chi tiết', [
        '– Mở được màn chi tiết (và xuất file dữ liệu báo giá) khi báo giá thoả MỘT trong hai điều '
        'kiện: (1) nằm trong phạm vi xem của Danh sách báo giá (V1–V4, hoặc do chính mình lập); '
        '(2) đang nằm trong hàng chờ duyệt của chính người dùng — cùng điều kiện với màn Báo giá chờ '
        'duyệt (Q1: Chờ TP duyệt thuộc phòng ban mình quản lý; Q2: Chờ BGĐ duyệt thuộc công ty mình).',
        '– Người duyệt không có V1–V4 vẫn mở và duyệt được báo giá đang chờ mình; báo giá ngoài hàng '
        'chờ và ngoài phạm vi xem vẫn hiện “Không tìm thấy báo giá.”.',
        '– Điều kiện (2) không áp cho sao chép hay import báo giá.',
    ], ['Xem chi tiết báo giá để duyệt']),

    ('BR-06', 'Hiển thị giá vốn', [
        '– Giá nhập, thành tiền nhập, tổng giá nhập và TSLN chỉ hiển thị khi người dùng có quyền '
        'Xem giá vốn hàng hoá (Q3); hệ thống không trả các số liệu này cho người không có quyền.',
        '– Người lập và người có Q1/Q2 vẫn xem được giá nhập, TSLN của dòng hàng tạm để đánh giá '
        'trước khi duyệt.',
    ], ['Xem chi tiết báo giá để duyệt']),

    ('BR-07', 'Hệ quả khi báo giá được duyệt (Đã duyệt)', [
        '– Tính lại tổng tiền báo giá tại thời điểm duyệt; ghi người duyệt và thời điểm duyệt.',
        '– Yêu cầu tính giá bán liên kết chuyển sang Đã có báo giá.',
        '– Dự án TKT chuyển sang Thương thảo giá và giải pháp; mốc tự đóng dự án được tính lại '
        'theo ngày duyệt.',
        '– Giải pháp liên kết chuyển sang Đã duyệt giá.',
        '– Báo giá được đồng bộ sang ERP; lỗi đồng bộ không làm hỏng việc duyệt.',
        '– Bước Duyệt & chuyển BGĐ KHÔNG kích hoạt các hệ quả trên.',
    ], ['Duyệt báo giá cấp 2', 'BGĐ duyệt']),

    ('BR-08', 'Hệ quả khi báo giá bị từ chối', [
        '– Lý do từ chối bắt buộc, tối đa 1000 ký tự.',
        '– Báo giá quay về Đang tạo; xóa ngày gửi duyệt, thông tin TP duyệt, thông tin duyệt và '
        'cấp duyệt.',
        '– Khi gửi duyệt lại, cấp duyệt được tính lại theo số liệu mới (có thể khác lần trước).',
        '– Lý do từ chối hiển thị ở đầu màn chi tiết cho tới lần gửi duyệt tiếp theo.',
    ], ['Từ chối']),

    ('BR-09', 'Thông báo', [
        '– Gửi duyệt cấp 2/3: Trưởng phòng duyệt giá của phòng ban báo giá nhận thông báo.',
        '– Duyệt & chuyển BGĐ: người có quyền Q2 thuộc ĐÚNG công ty của báo giá nhận thông báo '
        '(cùng phạm vi với hàng chờ BGĐ).',
        '– Đã duyệt: người lập, nhân viên kinh doanh phụ trách dự án và Trưởng phòng duyệt giá của '
        'phòng ban báo giá nhận thông báo.',
        '– Từ chối: người lập nhận thông báo kèm lý do.',
        '– Lỗi gửi thông báo không làm hỏng thao tác nghiệp vụ.',
    ], ['Duyệt báo giá cấp 2', 'Duyệt & chuyển BGĐ', 'BGĐ duyệt', 'Từ chối']),

    ('BR-10', 'Ghi lịch sử phê duyệt', [
        '– Mỗi thao tác ghi 1 mốc: Gửi duyệt (kèm cấp), TP duyệt, TP duyệt & chuyển BGĐ, BGĐ '
        'duyệt, Từ chối (kèm lý do), kèm người thực hiện, trạng thái trước → sau và thời điểm.',
        '– Lỗi ghi lịch sử không làm hỏng thao tác nghiệp vụ.',
    ], ['Xem lịch sử phê duyệt', 'Duyệt', 'Từ chối']),

    ('BR-11', 'Ghi nhớ bộ lọc và cấu hình hiển thị', [
        '– Bộ lọc đang áp dụng được ghi nhớ 10 phút để khôi phục khi quay lại màn hình.',
        '– Cấu hình tiêu chí lọc và cấu hình cột lưu riêng theo người dùng và riêng cho màn Báo '
        'giá chờ duyệt (không dùng chung với màn Danh sách báo giá).',
        '– Ba cột STT, Mã báo giá, Hành động luôn hiển thị và không đổi vị trí được.',
    ], ['Xem danh sách', 'Tìm kiếm và lọc', 'Cài đặt bộ lọc', 'Tùy chỉnh cột']),
])

d.save()

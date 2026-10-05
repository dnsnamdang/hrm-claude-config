# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo Hiệu suất làm việc theo Giải pháp.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/report/performance-by-solutions/{index.vue, print.vue,
      components/PerformanceBySolutionsTable.vue, components/SolutionModulesModal.vue}
      components/V2BaseSmartFilterPanel.vue · components/modal/filter-customization-modal.vue
      components/V2BaseCompanyDepartmentFilter.vue · components/menu-sidebar.js (nhóm Báo cáo)
  BE  Modules/Assign/Routes/api.php (assign/report/performance-by-solutions, /export, /modules)
      PerformanceBySolutionsReportController · Services/Report/PerformanceBySolutionsReportService
      Transformers/PerformanceBySolutionsResource · app/ExcelExport/PerformanceBySolutionsReportExport
      resources/views/exports/performance_by_solutions_report · app/Helper/PermissionHelper checkPermissionList
  Quyền: PermissionsTableSeeder id 1069-1072 nhóm "Báo cáo hiệu suất theo giải pháp"
Ảnh chụp thật: shots/ (shoot.py + shoot2.py, client :3002 → API :8003, dữ liệu mẫu xem data_created.md).
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


TEN_MAN = 'Báo cáo Hiệu suất làm việc theo Giải pháp'
MENU = 'Phân hệ Công việc => Báo cáo => Hiệu suất làm việc theo Giải pháp'
ACTOR = 'Người xem báo cáo'

d = SrsDoc(out=os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN), menu=MENU, route='', full_url='',
           img_prefix='hsgp_')
d.set_menu_icons({k: shot(v) for k, v in {
    'Phân hệ Công việc': 'icon_phanhe.png',
    'Báo cáo': 'icon_baocao.png',
    'Hiệu suất làm việc theo Giải pháp': 'icon_menu.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Tìm kiếm': 'icon_btn_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Xem chi tiết': 'icon_xemchitiet.png',
    'Thu gọn': 'icon_thugon.png',
    'Số hạng mục': 'icon_chip.png',
    'Xuất Excel': 'icon_xuatexcel.png',
    'In báo cáo': 'icon_in.png',
}.items()})
d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Báo cáo hiệu suất làm việc theo Giải pháp, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phạm vi dữ liệu của báo cáo.',
    'Làm rõ cách hệ thống tổng hợp số hạng mục, số nhân sự tham gia, giờ dự toán, giờ thực tế và hiệu suất của từng '
    'giải pháp, gom theo phòng làm giải pháp.',
    'Làm rõ điều kiện bắt buộc chọn công ty trước khi xem và ý nghĩa bộ lọc thời gian (theo ngày bắt đầu của dự án TKT).',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Giải pháp', 'Phương án kỹ thuật lập cho 1 dự án TKT theo yêu cầu làm giải pháp; gồm nhiều hạng mục.'),
    ('Phòng làm GP', 'Phòng ban nhận yêu cầu làm giải pháp. Báo cáo gom giải pháp theo phòng này.'),
    ('Dự án TKT', 'Dự án tiềm năng mà giải pháp phục vụ.'),
    ('Hạng mục', 'Phần việc của giải pháp (vd “Xây dựng danh mục thiết bị”), có 1 leader và các thành viên.'),
    ('Giờ dự toán', 'Tổng giờ ước tính của các nhiệm vụ thuộc hạng mục.'),
    ('Giờ thực tế', 'Tổng giờ thực tế đã ghi trên các nhiệm vụ thuộc hạng mục.'),
    ('Hiệu suất (%)', 'Giờ dự toán / Giờ thực tế × 100%. Trên 100% nghĩa là làm nhanh hơn dự toán.'),
    ('Chốt được HĐ', 'Dự án TKT của giải pháp đã sang giai đoạn Thực hiện hợp đồng trở về sau.'),
    ('Công ty đang làm việc', 'Công ty người dùng đang chọn ở góc trên bên phải màn hình.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('–', 'Không khai quyền riêng',
     'Mọi người dùng vào được phân hệ Công việc đều thấy menu “Hiệu suất làm việc theo Giải pháp” và dùng được mọi '
     'chức năng của màn (xem, lọc, xem hạng mục, xuất Excel, in). Dữ liệu nhìn thấy do nhóm quyền phạm vi bên dưới '
     'quyết định.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem báo cáo hiệu suất GP theo tổng công ty',
     'Giải pháp của mọi công ty. Bộ lọc hiện ô Công ty và BẮT BUỘC chọn công ty trước khi tìm kiếm.'),
    ('V2', 'Xem báo cáo hiệu suất GP theo công ty',
     'Giải pháp thuộc công ty đang làm việc. Bắt buộc có công ty trên bộ lọc trước khi tìm kiếm.'),
    ('V3', 'Xem báo cáo hiệu suất GP theo phòng ban',
     'Giải pháp thuộc phòng ban / bộ phận người dùng quản lý, cộng giải pháp do chính người dùng tạo.'),
    ('V4', 'Xem báo cáo hiệu suất GP theo bộ phận',
     'Giải pháp thuộc bộ phận người dùng quản lý, cộng giải pháp do chính người dùng tạo.'),
    ('–', 'Không có quyền nào ở trên', 'Chỉ giải pháp do chính người dùng tạo.'),
], widths=[0.8, 2.4, 2.8])
d.p('Có nhiều quyền cùng lúc thì áp dụng quyền rộng nhất theo thứ tự V1 → V2 → V3 → V4.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'V1', 'V2', 'V3', 'V4', 'Không có quyền nào'], [
    ('FR-01 Xem báo cáo hiệu suất làm việc theo Giải pháp', '✅', '✅', '✅', '✅',
     '✅ (chỉ giải pháp do mình tạo)'),
    ('FR-02 Tìm kiếm và lọc báo cáo', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Xem danh sách hạng mục của giải pháp', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Xuất Excel', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 In báo cáo', '✅', '✅', '✅', '✅', '✅'),
], widths=[2.4, 0.5, 0.5, 0.5, 0.5, 1.6])

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR, [0, 1, 2])],
    [('FR-01', 'Xem báo cáo hiệu suất theo Giải pháp', 'view'),
     ('FR-05', 'Xuất Excel', 'io'),
     ('FR-06', 'In báo cáo', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Xem hạng mục của giải pháp', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1 Xem bao cao
d.h3('2.1 Xem báo cáo hiệu suất làm việc theo Giải pháp')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Phân trang và UI/UX. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Xem báo cáo hiệu suất làm việc theo Giải pháp',
    mota='Bảng 2 cấp Phòng làm giải pháp → Giải pháp: mỗi giải pháp cho biết dự án TKT, PM giải pháp, số hạng mục, '
         'tổng nhân sự tham gia, số giờ dự toán, số giờ thực tế, hiệu suất và đã chốt được hợp đồng hay chưa. Dòng '
         'phòng ban là dòng tổng hợp. Phân trang theo phòng ban.',
    tacnhan='%s; Người dùng đã đăng nhập' % ACTOR,
    dieukien='Người dùng vào được phân hệ Công việc.',
    chinh='1. Người dùng vào menu Hiệu suất làm việc theo Giải pháp.\n'
          '2. Bộ lọc mặc định: Xem theo thời gian = Tháng, Tháng = tháng hiện tại, Năm = năm hiện tại.\n'
          '3. Người dùng có quyền V1 / V2: chọn Công ty ở bộ lọc rồi bấm “Tìm kiếm” (xem FR-02). Người dùng có quyền '
          'V3 / V4 hoặc không có quyền nào: hệ thống nạp báo cáo ngay khi mở màn.\n'
          '4. Hệ thống hiển thị trang đầu (5 phòng ban / trang), mọi phòng ban đang mở sẵn danh sách giải pháp.\n'
          '5. Người dùng bấm mũi tên ở dòng phòng ban để mở / thu; dùng “Xem chi tiết” / “Thu gọn” để đổi chế độ xem; '
          'chuyển trang, đổi số dòng / trang ở chân bảng.',
    phu='• Có quyền V1 / V2 mà chưa có công ty → “Vui lòng chọn công ty trước khi tìm kiếm”, bảng giữ dòng '
        '“Vui lòng bấm Tìm kiếm để xem báo cáo.”.\n'
        '• Không có dữ liệu → bảng hiển thị “Không có dữ liệu.”, chân bảng “Không có phòng ban nào.”.\n'
        '• Không tải được báo cáo → “Lỗi khi tải báo cáo hiệu suất theo giải pháp”.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-mo-man.png'),
         shot_caption='Màn lúc mới mở với tài khoản có quyền V1 — chưa chọn công ty')
d.p('Sau khi chọn công ty và bấm Tìm kiếm:')
d._menu_para(MENU + ' => Tìm kiếm')
d.figure(shot('02-xem-bao-cao.png'), 'Bảng báo cáo — phần cột bên trái', width_in=6.2)
d.figure(shot('02b-xem-bao-cao-phai.png'), 'Bảng báo cáo — phần cột bên phải (kéo thanh cuộn ngang)',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Báo cáo hiệu suất làm việc theo Giải pháp',
     'Kèm biểu tượng ⓘ, rê chuột: “Thống kê hiệu suất làm việc của Phòng ban làm giải pháp → Giải pháp dựa trên số '
     'hạng mục, tổng nhân sự tham gia và giờ dự toán / thực tế.”'),
    ('Khối Bộ lọc báo cáo hiệu suất theo Giải pháp', 'Card', 'Hiển thị', '–', 'Thu gọn', 'Xem FR-02, FR-03.'),
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Bảng chi tiết hiệu suất theo giải pháp',
     'Kèm ⓘ, rê chuột: “Danh sách theo Phòng ban làm giải pháp → Giải pháp.”'),
    ('Nút Xem chi tiết / Thu gọn', 'Button', 'Enable / Ẩn', '–', 'Xem chi tiết',
     'Chỉ hiện khi đã tìm kiếm và có dữ liệu. “Xem chi tiết”: chuyển sang chế độ chi tiết và mở mọi phòng ban; '
     'nút đổi thành “Thu gọn” để quay về chế độ gọn.'),
    ('Nút Xuất Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi chưa có dữ liệu', 'Xem FR-05.'),
    ('Nút In báo cáo', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi chưa có dữ liệu', 'Xem FR-06.'),
    ('Dòng nhắc chưa tìm kiếm', 'Label', 'Hiển thị', '–', 'Hiển thị', '“Vui lòng bấm Tìm kiếm để xem báo cáo.”'),
    ('Thanh cuộn ngang trên và dưới bảng', 'Scrollbar', 'Enable', '–', 'Hiển thị',
     '2 thanh cuộn chạy đồng bộ; tiêu đề cột giữ cố định khi cuộn dọc.'),
    ('Cột STT', 'Icon Button', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng phòng ban: nút mũi tên mở / thu. Dòng giải pháp: để trống.'),
    ('Cột Phòng ban / Giải pháp', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng phòng ban: tên phòng làm GP (không có → “Chưa xác định”) + dòng phụ “Công ty: <tên> • <n> giải pháp • '
     '<m> hạng mục”. Dòng giải pháp: mã giải pháp (chữ nhỏ) + tên giải pháp.'),
    ('Cột Dự án TKT', 'Text', 'Read-only', '–', 'Theo dữ liệu', '“<Mã dự án> - <Tên dự án>”. Dòng phòng ban “—”.'),
    ('Cột PM giải pháp', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Họ tên PM. Dòng phòng ban “—”.'),
    ('Cột Số hạng mục', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Dòng giải pháp: ô số bấm được (xem FR-04). Dòng phòng ban: tổng, in đậm.'),
    ('Cột Tổng nhân sự tham gia', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Số người khác nhau là leader hoặc thành viên của các hạng mục. Dòng phòng ban: cộng số của các giải pháp.'),
    ('Cột Số giờ làm dự toán / Số giờ làm thực tế', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Dòng giải pháp: ô số bấm được (xem FR-04). Dòng phòng ban: tổng, in đậm.'),
    ('Cột Hiệu suất (%)', 'Text', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Dòng giải pháp: “<x>%”, bấm được. Dòng phòng ban: “Hiệu suất TB: <x>%”.'),
    ('Cột Chốt được HĐ', 'Badge', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu',
     '“Đã chốt” (nền xanh lá) / “Chưa chốt” (nền đỏ nhạt). Dòng phòng ban “—”.'),
    ('Chân bảng – số bản ghi', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     '“Hiển thị <từ>–<đến> / <tổng> phòng ban”; không có → “Không có phòng ban nào.”'),
    ('Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', '5', '5 / 10 / 20 / 50 phòng ban mỗi trang.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Đầu · Trước · số trang · Sau · Cuối.'),
    ('Dòng trống', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu.”'),
    ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu...”'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Xác định phạm vi dữ liệu theo quyền V1 / V2 / V3 / V4.\n'
     '– Có V1 hoặc V2 mà bộ lọc chưa có công ty → “Vui lòng chọn công ty trước khi tìm kiếm” và dừng xử lý.\n'
     'After:\n– Nạp danh sách PM, dự án TKT, giải pháp cho bộ lọc; nạp trang 1 của báo cáo theo tháng hiện tại.\n'
     '– Mọi phòng ban trên trang được mở sẵn.\n'
     '– Lỗi → “Lỗi khi tải báo cáo hiệu suất theo giải pháp”.'),
    ('Bấm mũi tên dòng phòng ban', 'Click',
     'After:\n– Đang ở chế độ gọn → chuyển sang chế độ chi tiết và CHỈ mở phòng ban vừa bấm.\n'
     '– Đang ở chế độ chi tiết → mở / thu phòng ban vừa bấm.'),
    ('Bấm Xem chi tiết', 'Click', 'After:\n– Chuyển sang chế độ chi tiết, mở mọi phòng ban; nút đổi thành “Thu gọn”.'),
    ('Bấm Thu gọn', 'Click', 'After:\n– Quay về chế độ gọn; nút đổi lại “Xem chi tiết”.'),
    ('Chuyển trang / đổi Số dòng/trang', 'Click / Change',
     'After:\n– Nạp trang tương ứng với điều kiện lọc đã áp dụng ở lần Tìm kiếm gần nhất (đổi số dòng thì về trang 1).\n'
     '– Chưa tìm kiếm lần nào → không xử lý.'),
])

# ------------------------------------------------------------------ 2.2 Loc
d.h3('2.2 Tìm kiếm và lọc báo cáo')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả '
           'chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc báo cáo',
    mota='Thu hẹp báo cáo theo kỳ thời gian (ngày bắt đầu dự án TKT), công ty, phòng làm giải pháp, PM giải pháp, '
         'dự án TKT, giải pháp và tiến trình giải pháp.',
    tacnhan='%s; Người dùng đã đăng nhập' % ACTOR,
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “Tìm kiếm nâng cao” để mở khối bộ lọc.\n'
          '2. Người dùng chọn Công ty (bắt buộc với quyền V1 / V2), kỳ thời gian và các điều kiện khác.\n'
          '3. Đổi Xem theo thời gian, Tháng, Năm, khoảng ngày, PM giải pháp, Dự án TKT, Giải pháp hoặc Tiến trình → '
          'hệ thống tìm ngay; đổi Công ty / Phòng làm GP → người dùng bấm “Tìm kiếm”.\n'
          '4. Hệ thống áp dụng điều kiện, nạp lại báo cáo từ trang đang đứng.',
    phu='• Có quyền V1 / V2 mà chưa chọn công ty → “Vui lòng chọn công ty trước khi tìm kiếm”, không tìm.\n'
        '• Đổi Dự án TKT → ô Giải pháp bị xoá và danh sách giải pháp chỉ còn giải pháp của dự án đó.\n'
        '• Bấm “Làm mới” → trả bộ lọc về mặc định, xoá kết quả; nếu vẫn đủ điều kiện tìm kiếm thì nạp lại ngay, '
        'không thì hiện lại dòng “Vui lòng bấm Tìm kiếm để xem báo cáo.”.',
    dacbiet='Kỳ thời gian lọc theo NGÀY BẮT ĐẦU CỦA DỰ ÁN TKT gắn với giải pháp. Giải pháp ở trạng thái Nháp không bao '
            'giờ được đưa vào báo cáo.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('03-bo-loc.png'),
         shot_caption='Khối bộ lọc đang mở, đã chọn công ty và tìm kiếm')
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
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Có với quyền V1 / V2', 'Trống',
     'Chỉ hiện với quyền V1. Có biểu tượng 🔒 để hiện cả công ty đã khoá.'),
    ('Phòng làm GP', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Hiện với quyền V1 / V2 / V3; danh sách theo phạm vi quyền và theo Công ty đã chọn. Có biểu tượng 🔒.'),
    ('PM giải pháp', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Danh sách nhân viên, hiển thị “Tên nhân viên - Mã phòng - Mã nhân viên”.'),
    ('Dự án TKT', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', '“<Mã dự án> - <Tên dự án>”.'),
    ('Giải pháp', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     '“<Mã> - <Tên giải pháp>”; đã chọn Dự án TKT thì chỉ còn giải pháp của dự án đó.'),
    ('Tiến trình giải pháp', 'Dropdown', 'Enable', 'Danh sách 10 giá trị', 'Không', 'Trống',
     'Nháp · Chờ PM duyệt · Chờ Leader duyệt · Đang triển khai · Chờ duyệt giải pháp · Đã duyệt giải pháp · '
     'Đang điều chỉnh · Chờ làm giá · Chốt giải pháp · Đã làm giải pháp.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện đang chọn.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Trả bộ lọc về mặc định.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Đổi giá trị ô chọn (thời gian, PM, dự án, giải pháp, tiến trình)', 'Change',
     'After:\n– Thực hiện như bấm Tìm kiếm.'),
    ('Đổi Xem theo thời gian', 'Change',
     'After:\n– Tuỳ chỉnh → xoá Tháng, Năm; Tháng / Năm → xoá khoảng ngày; chọn Năm thì xoá thêm Tháng.'),
    ('Đổi Dự án TKT', 'Change', 'After:\n– Xoá giá trị ô Giải pháp; lọc lại danh sách giải pháp theo dự án.'),
    ('Bấm Tìm kiếm', 'Click',
     'Before:\n– Có quyền V1 / V2 mà chưa có Công ty → “Vui lòng chọn công ty trước khi tìm kiếm” và dừng xử lý.\n'
     'During:\n– Tính khoảng ngày theo kỳ đã chọn (Tháng: ngày 1 → ngày cuối tháng; Năm: 01/01 → 31/12; '
     'Tuỳ chỉnh: khoảng đã chọn).\n– Lưu bộ điều kiện này làm điều kiện cho phân trang, xem hạng mục, xuất Excel, in.\n'
     'After:\n– Nạp lại báo cáo, mở sẵn mọi phòng ban.\n'
     '– Lỗi → “Lỗi khi tải báo cáo hiệu suất theo giải pháp”.'),
    ('Bấm Làm mới', 'Click',
     'After:\n– Trả bộ lọc về mặc định, về trang 1, xoá kết quả.\n'
     '– Đủ điều kiện tìm kiếm → nạp lại ngay; không → hiện “Vui lòng bấm Tìm kiếm để xem báo cáo.”.'),
])

# ------------------------------------------------------------------ 2.3 Cai dat bo loc
d.h3('2.3 Cài đặt bộ lọc')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='excel')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Người dùng chọn trường lọc nào được hiển thị trong khối bộ lọc và sắp xếp thứ tự các trường. Cài đặt lưu '
         'riêng cho từng người dùng trên màn báo cáo này.',
    tacnhan='%s; Người dùng đã đăng nhập' % ACTOR,
    dieukien='Người dùng đang ở màn báo cáo.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
          '2. Hệ thống mở popup liệt kê 8 trường lọc theo thứ tự đang dùng.\n'
          '3. Người dùng tích / bỏ tích trường muốn hiển thị, kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm “Lưu”.\n'
          '5. Hệ thống lưu cài đặt, đóng popup, báo “Cập nhật thành công” và vẽ lại khối bộ lọc.',
    phu='• Bấm “Khôi phục mặc định” → hiện lại đủ trường theo thứ tự gốc (chưa lưu, phải bấm Lưu).\n'
        '• Bấm “Đóng” / dấu × → đóng popup, không lưu.\n'
        '• Lưu lỗi → “Thao tác thất bại”.',
    dacbiet='Trường bị ẩn thì giá trị đang lọc của trường đó bị xoá, để báo cáo không bị lọc ngầm bởi trường người '
            'dùng không nhìn thấy. Ẩn nhóm “Công ty – Phòng ban” với quyền V1 / V2 sẽ không còn chọn được công ty '
            'để tìm kiếm.')
d.p('2.3.2 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', modal='Cài đặt bộ lọc', shot=shot('04-cai-dat-bo-loc.png'),
         shot_caption='Popup Cài đặt bộ lọc')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', 'Kèm biểu tượng bánh răng.'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
    ('Danh sách trường lọc', 'Checkbox', 'Enable', 'Danh sách 8 trường', 'Không', 'Theo cài đặt đã lưu',
     'Xem theo thời gian · Tháng · Năm · Công ty – Phòng ban · PM giải pháp · Dự án TKT · Giải pháp · Tiến trình '
     'giải pháp. Mỗi dòng có số thứ tự và tay kéo ⠿.'),
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
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Hiện lại đủ 8 trường theo thứ tự gốc trong popup (chưa lưu).'),
    ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup, bỏ thay đổi chưa lưu.'),
])

# ------------------------------------------------------------------ 2.4 Hang muc
d.h3('2.4 Xem danh sách hạng mục của giải pháp')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='detail')
d.intro_table(
    ten='Xem danh sách hạng mục của giải pháp',
    mota='Từ một dòng giải pháp, xem số liệu chi tiết của từng hạng mục: leader, số nhân sự, giờ dự toán, giờ thực tế, '
         'hiệu suất.',
    tacnhan='%s; Người dùng đã đăng nhập' % ACTOR,
    dieukien='Đã tìm kiếm và bảng đang hiển thị dòng giải pháp.',
    chinh='1. Người dùng bấm một ô số trên dòng giải pháp: Số hạng mục, Số giờ làm dự toán, Số giờ làm thực tế hoặc '
          'Hiệu suất (%).\n'
          '2. Hệ thống mở popup, đầu popup ghi mã – tên giải pháp và tóm tắt “<n> hạng mục • <x> giờ dự toán • <y> giờ '
          'thực tế”.\n'
          '3. Hệ thống nạp danh sách hạng mục của giải pháp theo điều kiện lọc đang áp dụng.\n'
          '4. Người dùng bấm “Đóng” để quay lại báo cáo.',
    phu='• Giải pháp không có hạng mục → “Không có hạng mục.”.\n'
        '• Không tải được → “Lỗi khi tải danh sách hạng mục”.')
d.p('2.4.2 Layout màn hình')
d.layout(menu=MENU + ' => Số hạng mục', modal='Danh sách hạng mục theo giải pháp', shot=shot('05-hang-muc.png'),
         shot_caption='Popup Danh sách hạng mục theo giải pháp')
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nhãn đầu popup', 'Label', 'Hiển thị', '–', 'DANH SÁCH HẠNG MỤC THEO GIẢI PHÁP', '–'),
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“<Mã giải pháp> - <Tên giải pháp>”.'),
    ('Dòng tóm tắt', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     '“<n> hạng mục • <x> giờ dự toán • <y> giờ thực tế” (lấy từ dòng giải pháp đã bấm).'),
    ('Cột #', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Số thứ tự.'),
    ('Cột Mã hạng mục / Tên hạng mục', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Trống → “—”.'),
    ('Cột Leader hạng mục', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Họ tên leader; trống → “—”.'),
    ('Cột Tổng nhân sự', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu', 'Số người khác nhau gồm leader và thành viên.'),
    ('Cột Giờ dự toán / Giờ thực tế', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Tổng giờ ước tính / giờ thực tế của các nhiệm vụ thuộc hạng mục.'),
    ('Cột Hiệu suất (%)', 'Text', 'Read-only', '≥ 0', 'Theo dữ liệu', 'Giờ dự toán / Giờ thực tế × 100%.'),
    ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu...”'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có hạng mục.”'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng popup.'),
], required=False)
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm ô số trên dòng giải pháp', 'Click',
     'Before:\n– Chưa tìm kiếm lần nào → không xử lý.\n'
     'After:\n– Mở popup, nạp hạng mục của giải pháp kèm điều kiện lọc của lần Tìm kiếm gần nhất và phạm vi quyền; '
     'giải pháp không còn thoả điều kiện thì danh sách rỗng.\n'
     '– Lỗi → “Lỗi khi tải danh sách hạng mục”.'),
    ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup, xoá dữ liệu popup; bảng báo cáo giữ nguyên.'),
])

# ------------------------------------------------------------------ 2.5 Xuat Excel
d.h3('2.5 Xuất Excel')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Xuất Excel báo cáo hiệu suất theo Giải pháp', 'io', actor=ACTOR)
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả chi tiết.',
           anchor='excel')
d.intro_table(
    ten='Xuất Excel',
    mota='Tải về file Excel báo cáo theo điều kiện lọc của lần Tìm kiếm gần nhất, gồm TẤT CẢ phòng ban (không chia trang).',
    tacnhan='%s; Người dùng đã đăng nhập' % ACTOR,
    dieukien='Đã tìm kiếm và báo cáo đang có dữ liệu.',
    chinh='1. Người dùng bấm “Xuất Excel”.\n'
          '2. Hệ thống dựng file theo điều kiện lọc và phạm vi quyền.\n'
          '3. Trình duyệt tải file “bao_cao_hieu_suat_theo_giai_phap.xls”.\n'
          '4. Hệ thống báo “Xuất Excel thành công”.',
    phu='• Chưa tìm kiếm hoặc không có dữ liệu → “Vui lòng tìm kiếm và có dữ liệu trước khi xuất Excel”.\n'
        '• Lỗi khi dựng file → “Lỗi khi xuất Excel”.',
    dacbiet='File gồm: ảnh tiêu đề (letterhead) của công ty đang làm việc, tiêu đề “BÁO CÁO HIỆU SUẤT LÀM VIỆC THEO '
            'GIẢI PHÁP”, bảng 10 cột như màn hình với STT phân cấp 1 / 1.1, cuối file “Ngày ..., tháng ..., năm ...” '
            '– “Người lập”.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('06-xuat-excel.png'),
         shot_caption='Bấm Xuất Excel — thông báo xuất thành công')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xuất Excel', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi chưa có dữ liệu',
     'Thanh tiến trình chạy ở đầu trang trong lúc dựng file.'),
    ('File Excel – phần đầu', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Ảnh tiêu đề công ty đang làm việc (không có thì dùng ảnh mặc định) + tiêu đề báo cáo.'),
    ('File Excel – bảng', 'Table/Grid', 'Read-only', '10 cột', '–', 'Theo dữ liệu',
     'STT · Phòng ban / Giải pháp (“<mã> — <tên>”) · Dự án TKT · PM giải pháp · Số hạng mục · Tổng nhân sự tham gia · '
     'Số giờ làm dự toán · Số giờ làm thực tế · Hiệu suất (%) · Chốt được HĐ (“Đã chốt” / “Chưa chốt”). Dòng phòng '
     'ban nền xanh nhạt, chữ đậm.'),
    ('File Excel – định dạng số', 'Number', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Số lượng và giờ làm tròn số nguyên, có dấu phẩy ngăn cách hàng nghìn; hiệu suất 2 chữ số thập phân.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Xuất Excel thành công” / “Vui lòng tìm kiếm và có dữ liệu trước khi xuất Excel” / “Lỗi khi xuất Excel”.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Chưa tìm kiếm hoặc không có dữ liệu → “Vui lòng tìm kiếm và có dữ liệu trước khi xuất Excel” và '
     'dừng xử lý.\n'
     'During:\n– Gửi điều kiện lọc của lần Tìm kiếm gần nhất (bỏ phân trang); máy chủ dựng dữ liệu theo phạm vi quyền.\n'
     'After:\n– Tải file “bao_cao_hieu_suat_theo_giai_phap.xls”, báo “Xuất Excel thành công”.\n'
     '– Lỗi → “Lỗi khi xuất Excel”.'),
])

# ------------------------------------------------------------------ 2.6 In
d.h3('2.6 In báo cáo')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'In báo cáo hiệu suất theo Giải pháp', 'io', actor=ACTOR)
d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của bản in tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='In báo cáo',
    mota='Mở bản xem trước để in báo cáo (khổ A4 ngang) theo điều kiện lọc của lần Tìm kiếm gần nhất, gồm tất cả '
         'phòng ban.',
    tacnhan='%s; Người dùng đã đăng nhập' % ACTOR,
    dieukien='Đã tìm kiếm và báo cáo đang có dữ liệu.',
    chinh='1. Người dùng bấm “In báo cáo”.\n'
          '2. Hệ thống mở bản xem trước ở tab mới, nạp lại dữ liệu theo điều kiện lọc.\n'
          '3. Người dùng bấm nút “In” để mở hộp thoại in của trình duyệt.',
    phu='• Chưa tìm kiếm hoặc không có dữ liệu → “Vui lòng tìm kiếm và có dữ liệu trước khi in báo cáo”, không mở tab.\n'
        '• Không tải được dữ liệu in → khung đỏ hiển thị nội dung lỗi hoặc “Lỗi không xác định khi tải dữ liệu báo cáo”.',
    dacbiet='Bản in: khổ A4 ngang; ảnh tiêu đề công ty đang làm việc; tiêu đề “BÁO CÁO HIỆU SUẤT LÀM VIỆC THEO GIẢI '
            'PHÁP”; cuối trang “Ngày ...., tháng ...., năm ....” – “Người lập” – “(Ký, họ tên)”.')
d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => In báo cáo', shot=shot('07-in.png'), shot_caption='Bản xem trước khi in')
d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Không xuất hiện trên bản in.'),
    ('Khung báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Khung đỏ, không xuất hiện trên bản in.'),
    ('Ảnh tiêu đề công ty', 'Label', 'Read-only', '–', '–', 'Theo công ty đang làm việc',
     'Không có thì dùng ảnh mặc định.'),
    ('Tiêu đề', 'Label', 'Read-only', '–', '–', 'BÁO CÁO HIỆU SUẤT LÀM VIỆC THEO GIẢI PHÁP', '–'),
    ('Bảng in', 'Table/Grid', 'Read-only', '10 cột', '–', 'Theo dữ liệu',
     'Cùng cột với màn hình. STT: phòng ban “1”, giải pháp “1.1”; cột Phòng ban / Giải pháp của dòng giải pháp ghi '
     '“<mã> — <tên>”, lùi lề. Dòng phòng ban nền xanh nhạt, Dự án / PM / Chốt được HĐ = “—”.'),
    ('Định dạng số', 'Number', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Dấu phẩy ngăn cách hàng nghìn; hiệu suất tối đa 2 chữ số thập phân kèm “%”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '“Không có dữ liệu”.'),
    ('Khối ký', 'Label', 'Read-only', '–', '–', 'Hiển thị',
     '“Ngày ...., tháng ...., năm ....” / “Người lập” / “(Ký, họ tên)”, căn phải.'),
])
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In báo cáo', 'Click',
     'Before:\n– Chưa tìm kiếm hoặc không có dữ liệu → “Vui lòng tìm kiếm và có dữ liệu trước khi in báo cáo” và dừng '
     'xử lý.\n'
     'After:\n– Mở bản xem trước ở tab mới, mang theo điều kiện lọc của lần Tìm kiếm gần nhất.'),
    ('Mở bản xem trước', 'System',
     'After:\n– Nạp toàn bộ phòng ban theo điều kiện lọc và phạm vi quyền (không chia trang); dựng bảng phân cấp.\n'
     '– Lỗi → khung đỏ hiển thị nội dung lỗi.'),
    ('Bấm In', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt với khổ A4 ngang, chỉ in vùng báo cáo.'),
])

# ==================================================== PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Báo cáo hiệu suất làm việc theo Giải pháp; không lặp lại các '
           'quy tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Nguồn dữ liệu và cách nhóm', [
        '– Lấy mọi giải pháp KHÁC trạng thái Nháp; nhóm theo phòng nhận yêu cầu làm giải pháp (Phòng làm GP); không '
        'xác định được phòng → nhóm “Chưa xác định”.',
        '– Phòng ban sắp xếp theo tên; trong mỗi phòng, giải pháp mới tạo đứng trước.',
        '– Phân trang theo PHÒNG BAN (mặc định 5 phòng ban / trang), không theo số giải pháp.',
    ], ['Xem báo cáo', 'Xuất Excel', 'In báo cáo']),
    ('BR-02', 'Số liệu của giải pháp và hạng mục', [
        '– Số hạng mục = số hạng mục của giải pháp.',
        '– Tổng nhân sự tham gia = số người KHÁC NHAU là leader hoặc thành viên của các hạng mục.',
        '– Giờ dự toán = tổng giờ ước tính, Giờ thực tế = tổng giờ thực tế của mọi nhiệm vụ thuộc các hạng mục.',
        '– Hiệu suất = Giờ dự toán / Giờ thực tế × 100%, làm tròn 2 chữ số; Giờ thực tế bằng 0 → 0%.',
    ], ['Xem báo cáo', 'Xem hạng mục của giải pháp']),
    ('BR-03', 'Số liệu dòng phòng ban', [
        '– Số hạng mục, Tổng nhân sự, Giờ dự toán, Giờ thực tế = cộng các giải pháp trong phòng.',
        '– Hiệu suất TB = trung bình cộng hiệu suất của các giải pháp trong phòng (không tính lại từ tổng giờ).',
    ], ['Xem báo cáo', 'Xuất Excel', 'In báo cáo']),
    ('BR-04', 'Chốt được hợp đồng', [
        '– “Đã chốt” khi dự án TKT của giải pháp ở giai đoạn Thực hiện hợp đồng hoặc các giai đoạn sau đó; '
        'còn lại “Chưa chốt”.',
    ], 'Xem báo cáo'),
    ('BR-05', 'Điều kiện lọc và bắt buộc chọn công ty', [
        '– Người dùng có quyền V1 hoặc V2 phải có Công ty trên bộ lọc thì mới tìm kiếm được.',
        '– Kỳ thời gian lọc theo ngày bắt đầu của dự án TKT: Tháng = ngày 1 → ngày cuối tháng; Năm = 01/01 → 31/12; '
        'Tuỳ chỉnh = khoảng ngày đã chọn.',
        '– Phân trang, xem hạng mục, xuất Excel và in dùng điều kiện của lần Tìm kiếm gần nhất, không dùng giá trị '
        'vừa sửa trên bộ lọc mà chưa tìm kiếm.',
    ], 'Tìm kiếm và lọc'),
    ('BR-06', 'Phạm vi dữ liệu theo quyền', [
        '– V1: mọi công ty; V2: công ty đang làm việc; V3: phòng ban / bộ phận người dùng quản lý + giải pháp do mình '
        'tạo; V4: bộ phận người dùng quản lý + giải pháp do mình tạo; không có quyền nào: giải pháp do mình tạo.',
        '– Áp dụng như nhau cho màn hình, popup hạng mục, file Excel và bản in.',
    ], ['Xem báo cáo', 'Xuất Excel', 'In báo cáo']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

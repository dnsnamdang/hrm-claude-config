# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo vòng đời dự án TKT.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/report/prospective-projects/{index,print}.vue
      components/{ProspectiveProjectsFilter,ProspectiveProjectsTable,ProspectiveSummaryModal,
      ProspectiveListModal}.vue · components/V2BaseSmartFilterPanel.vue ·
      components/modal/filter-customization-modal.vue · components/subsystem-menu/presale.js
  BE  Modules/Assign/Routes/api.php (assign/report/prospective-projects)
      ProspectiveProjectsReportController · Services/Report/ProspectiveProjectsReportService
      app/ExcelExport/ProspectiveProjectsReportExport + exports/prospective_projects_report.blade.php
  Quyền: PermissionsTableSeeder id 1054 / 1055 / 1056 (nhóm "Báo cáo vòng đời dự án TKT")
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


TEN_MAN = 'Báo cáo vòng đời dự án TKT'
MENU = 'Phân hệ CSKH trước bán => Báo cáo => Báo cáo dự án tiền khả thi => Báo cáo vòng đời dự án TKT'
ACTOR = 'Người xem báo cáo'
TACNHAN = 'Lãnh đạo, trưởng phòng, nhân viên kinh doanh; Người dùng đã đăng nhập'
DK = 'Người dùng đã đăng nhập (màn không yêu cầu quyền thao tác riêng; dữ liệu theo phạm vi quyền V1/V2/V3).'
ICONS = {
    'Phân hệ CSKH trước bán': 'icon_phanhe.png',
    'Báo cáo': 'icon_baocao.png',
    'Báo cáo dự án tiền khả thi': 'icon_nhom.png',
    'Báo cáo vòng đời dự án TKT': 'icon_man.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Tìm kiếm': 'icon_btn_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Chỉ xem cấp gốc': 'icon_capgoc.png',
    'Xem chi tiết': 'icon_xemchitiet.png',
    'Cơ cấu tiến trình': 'icon_cocau.png',
    'Số lượng dự án TKT': 'icon_soluong.png',
    'Xuất Excel': 'icon_xuat.png',
    'In báo cáo': 'icon_in.png',
}

OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN)
d = SrsDoc(out=OUT, menu=MENU, route='', full_url='', img_prefix='bcvddatkt_')
d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})
d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Báo cáo vòng đời dự án TKT, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của báo cáo.',
    'Làm rõ cách hệ thống tổng hợp dự án tiền khả thi theo cây Công ty → Phòng ban → Nhân viên kinh '
    'doanh, từ lúc khởi tạo dự án tới làm giải pháp, báo giá, hợp đồng hoặc đóng dự án.',
    'Làm rõ công thức từng cột số liệu, các ô bấm xem chi tiết và phạm vi dữ liệu theo quyền.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Dự án TKT', 'Dự án tiền khả thi — cơ hội kinh doanh do nhân viên kinh doanh theo dõi trước khi ký hợp đồng.'),
    ('NVKD', 'Nhân viên kinh doanh chính phụ trách dự án TKT.'),
    ('Tiến trình dự án', '12 bước nội bộ của dự án TKT: Đang tạo, Thu thập thông tin dự án, Chờ tiếp nhận làm '
     'giải pháp, Đang làm giải pháp, Trao đổi giải pháp với khách hàng, Lập dự toán, Thương thảo giá và '
     'giải pháp, Thương thảo hợp đồng, Thực hiện hợp đồng, Nghiệm thu và thanh lý hợp đồng, Đóng/Không '
     'thực hiện dự án, Kết thúc và lưu trữ.'),
    ('Giai đoạn dự án khách hàng', 'Giai đoạn phía khách hàng (danh mục Giai đoạn dự án), khác với Tiến trình nội bộ.'),
    ('GP', 'Giải pháp kỹ thuật lập cho dự án TKT.'),
    ('BG', 'Báo giá gắn với dự án TKT.'),
    ('HĐ', 'Hợp đồng.'),
    ('Dự án cha', 'Dự án TKT gom nhiều dự án con; không được tính vào báo cáo.'),
    ('Kỳ báo cáo', 'Khoảng ngày tạo dự án TKT được chọn ở bộ lọc thời gian.'),
], widths=[1.8, 4.2])

# ========================================================= PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('–', 'Không có quyền thao tác riêng',
     'Menu “Báo cáo vòng đời dự án TKT” hiển thị với mọi người dùng đã đăng nhập. Mọi chức năng trên màn '
     '(xem, lọc, cài đặt bộ lọc, xem chi tiết, xuất Excel, in) đều dùng được; số liệu hiển thị do nhóm '
     'quyền phạm vi dữ liệu bên dưới quyết định.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem báo cáo vòng đời dự án TKT theo tổng công ty',
     'Toàn bộ dự án TKT của mọi công ty. Bộ lọc hiện ô Công ty, Phòng ban, Bộ phận với đủ danh sách.'),
    ('V2', 'Xem báo cáo vòng đời dự án TKT theo công ty',
     'Dự án TKT thuộc công ty đang làm việc + dự án do chính người dùng tạo. Bộ lọc hiện ô Phòng ban, '
     'Bộ phận của công ty đang làm việc.'),
    ('V3', 'Xem báo cáo vòng đời dự án TKT theo phòng ban',
     'Dự án TKT thuộc phòng ban / bộ phận người dùng quản lý + dự án do chính người dùng tạo. Bộ lọc hiện '
     'ô Phòng ban, Bộ phận người dùng quản lý.'),
    ('Không có quyền nào', '–',
     'Chỉ dự án TKT do chính người dùng tạo hoặc người dùng là NVKD chính. Bộ lọc không hiện ô Công ty, '
     'Phòng ban, Bộ phận.'),
], widths=[0.8, 2.0, 3.2])
d.p('Người dùng có nhiều quyền thì áp phạm vi rộng nhất theo thứ tự V1 → V2 → V3.')

d.h2('2 Ma trận phân quyền')
FR = [
    'FR-01 Xem báo cáo vòng đời dự án TKT',
    'FR-02 Tìm kiếm và lọc',
    'FR-03 Cài đặt bộ lọc',
    'FR-04 Chuyển chế độ xem cấp gốc / chi tiết',
    'FR-05 Xem cơ cấu dự án',
    'FR-06 Xem danh sách dự án chi tiết',
    'FR-07 Xuất Excel',
    'FR-08 In báo cáo',
]
d.table(['Chức năng', 'V1', 'V2', 'V3', 'Không có quyền nào'],
        [(f, '✅', '✅', '✅', '✅ (chỉ dự án của mình)') for f in FR],
        widths=[2.6, 0.6, 0.6, 0.6, 1.6])

# ========================================================= PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR, [0, 1, 2])],
    [('FR-01', 'Xem báo cáo vòng đời dự án TKT', 'view'),
     ('FR-07', 'Xuất Excel', 'io'),
     ('FR-08', 'In báo cáo', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Chế độ xem cấp gốc / chi tiết', 'view', 'extend', [0], None),
     ('FR-05', 'Xem cơ cấu dự án', 'view', 'extend', [0], None),
     ('FR-06', 'Xem danh sách dự án chi tiết', 'view', 'extend', [0], None)],
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


# ------------------------------------------------------------------ 2.1 Xem báo cáo
fn('Xem báo cáo vòng đời dự án TKT',
   rule=('- Màn Danh sách, Phân trang và UI/UX. Chỉ bổ sung các quy tắc riêng của Báo cáo vòng đời dự án TKT '
         'tại phần mô tả chi tiết.', 'list'),
   intro=dict(
       ten='Xem báo cáo vòng đời dự án TKT',
       mota='Hiển thị bảng tổng hợp dự án TKT theo cây Công ty → Phòng ban → NVKD với 6 nhóm cột: Dự án TKT, '
            'Cơ cấu loại hình hoạt động / lĩnh vực kinh doanh khách hàng / ứng dụng, Làm giải pháp, Báo giá, '
            'Hợp đồng, Giải pháp không chốt được HĐ. Dòng đầu là tổng toàn bộ dự án TKT.',
       tacnhan=TACNHAN,
       dieukien=DK,
       chinh='1. Người dùng vào menu Báo cáo vòng đời dự án TKT.\n'
             '2. Hệ thống lấy kỳ mặc định là tháng hiện tại của năm hiện tại.\n'
             '3. Hệ thống tổng hợp dự án TKT tạo trong kỳ thuộc phạm vi quyền và hiển thị dòng Tổng, dòng '
             'Công ty, dòng Phòng ban, dòng NVKD — mặc định mở hết các cấp.\n'
             '4. Người dùng bấm mũi tên hoặc tên Công ty / Phòng ban để thu gọn / mở rộng cấp con.\n'
             '5. Người dùng chuyển trang hoặc đổi số dòng/trang ở thanh phân trang.',
       phu='• Không có dự án TKT nào trong kỳ → bảng chỉ còn dòng Tổng với số 0.\n'
           '• Lỗi khi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu báo cáo”.\n'
           '• Rê chuột vào biểu tượng ⓘ cạnh tiêu đề trang → hiện mô tả “Theo dõi toàn bộ vòng đời dự án TKT '
           'từ bước khởi tạo dự án tiền khả thi cho tới lập được hợp đồng hoặc đóng dự án.”'),
   layouts=[dict(menu=MENU, shot=shot('01-xem-full.png'),
                 shot_caption='Màn Báo cáo vòng đời dự án TKT — kỳ Tháng 7/2026, mở hết các cấp'),
            dict(menu=MENU, note='Cuộn ngang bảng để xem các nhóm cột Làm giải pháp, Báo giá, Hợp đồng:',
                 shot=shot('01b-xem-cuon.png'),
                 shot_caption='Các nhóm cột Làm giải pháp và Báo giá sau khi cuộn ngang')],
   ui=[
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Báo cáo vòng đời dự án TKT',
        'Kèm biểu tượng ⓘ, rê chuột hiện mô tả mục đích báo cáo.'),
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Danh sách tổng hợp theo Công ty -> Phòng ban -> Nhân viên KD', '–'),
       ('Nút Chỉ xem cấp gốc / Xem chi tiết', 'Button', 'Enable', '–', 'Chỉ xem cấp gốc', 'Xem FR-04.'),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-07.'),
       ('Nút In báo cáo', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-08.'),
       ('Bảng tổng hợp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Có thanh cuộn ngang ở cả trên và dưới; 2 cột STT và Công ty / Phòng ban / Nhân viên ghim bên trái; '
        'tiêu đề cột ghim khi cuộn dọc.'),
       ('STT', 'Text / Icon Button', 'Enable', '–', 'Theo cấp',
        'Dòng Tổng: trống; dòng Công ty / Phòng ban: nút mũi tên thu gọn – mở rộng; dòng NVKD: số thứ tự trong phòng.'),
       ('Công ty / Phòng ban / Nhân viên', 'Text', 'Read-only', '–', 'Theo dữ liệu',
        'Dòng Tổng “Tổng toàn bộ dự án TKT” + “<n> dự án”; dòng Công ty “Công ty: <tên>” + “<n> dự án TKT”; '
        'dòng Phòng ban “Phòng: <tên>” + “Dự án TKT: <n> - Báo giá: <n> - HĐ: 0”; dòng NVKD “NVKD: <tên>”. '
        'Không xác định được thì ghi “Chưa xác định công ty” / “Chưa xác định phòng ban” / “Chưa gán NVKD”.'),
       ('Số lượng dự án TKT', 'Number (link)', 'Enable', '≥ 0', 'Theo dữ liệu', 'Bấm mở danh sách dự án (FR-06).'),
       ('Cơ cấu tiến trình dự án', 'Button', 'Enable', '–', 'Cơ cấu tiến trình', 'Bấm mở popup cơ cấu (FR-05).'),
       ('Cơ cấu giai đoạn dự án', 'Button', 'Enable', '–', 'Cơ cấu giai đoạn', 'Bấm mở popup cơ cấu (FR-05).'),
       ('Loại hình hoạt động', 'Number (link)', 'Enable', '≥ 0', 'Theo dữ liệu',
        'Số loại hình hoạt động khác nhau của các dự án; bấm mở popup cơ cấu.'),
       ('Lĩnh vực kinh doanh khách hàng', 'Number (link)', 'Enable', '≥ 0', 'Theo dữ liệu',
        'Số lĩnh vực khác nhau; bấm mở popup cơ cấu.'),
       ('Ứng dụng', 'Number (link)', 'Enable', '≥ 0', 'Theo dữ liệu', 'Số ứng dụng khác nhau; bấm mở popup cơ cấu.'),
       ('Số giải pháp đã làm', 'Number (link)', 'Enable', '≥ 0', 'Theo dữ liệu',
        'Số dự án đã có giải pháp; bấm mở danh sách dự án.'),
       ('Số giải pháp chốt được', 'Number (link)', 'Enable', '≥ 0', 'Theo dữ liệu',
        'Số dự án có giải pháp mới nhất ở trạng thái Chốt giải pháp; bấm mở danh sách dự án.'),
       ('Tỷ lệ chốt GP', 'Text', 'Read-only', '0 – 100%', 'Theo dữ liệu', '1 chữ số thập phân, vd 3.1%.'),
       ('Dự án có báo giá', 'Number (link)', 'Enable', '≥ 0', 'Theo dữ liệu', 'Bấm mở danh sách dự án có báo giá.'),
       ('Số lượng báo giá', 'Number (link)', 'Enable', '≥ 0', 'Theo dữ liệu', 'Bấm mở danh sách dự án có báo giá.'),
       ('Giá trị báo giá', 'Text', 'Read-only', '≥ 0', 'Theo dữ liệu',
        'Định dạng 1,234,567 đ; bằng 0 hiển thị “-”.'),
       ('Tỷ lệ chuyển BG', 'Text', 'Read-only', '0 – 100%', 'Theo dữ liệu', '1 chữ số thập phân.'),
       ('Dự án có HĐ / Số lượng HĐ', 'Number (link)', 'Enable', '–', '0',
        'Chưa có nguồn dữ liệu hợp đồng — luôn 0; bấm mở popup rỗng.'),
       ('Giá trị HĐ / Tỷ lệ chuyển HĐ', 'Text', 'Read-only', '–', '“-” / 0.0%', 'Chưa có nguồn dữ liệu hợp đồng.'),
       ('Giải pháp không chốt được HĐ', 'Number (link)', 'Enable', '–', '0',
        'Ô luôn hiển thị 0; bấm mở danh sách dự án ở tiến trình Đóng/Không thực hiện dự án.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
       ('Thanh phân trang', 'Pagination', 'Enable', '15 / 50 / 100 / 200', '15',
        'Phân trang theo số NVKD: “Hiển thị a–b / n nhân viên”. Dòng Tổng, Công ty, Phòng ban vẫn là tổng của '
        'toàn bộ dữ liệu, không chỉ của trang đang xem.'),
   ], ui_kw=dict(required=False),
   ev=[
       ('Mở màn hình', 'System',
        'After:\n– Nạp danh sách 12 tiến trình dự án, danh mục cho bộ lọc, rồi tải báo cáo kỳ Tháng hiện tại.\n'
        '– Mở hết các cấp Công ty / Phòng ban.\n'
        '– Lỗi → hiển thị “Lỗi khi tải dữ liệu báo cáo”.'),
       ('Bấm mũi tên / tên dòng Công ty', 'Click',
        'After:\n– Đang mở → thu gọn công ty, đồng thời thu gọn các phòng ban con.\n– Đang đóng → mở ra các '
        'phòng ban (ở chế độ cấp gốc thì phòng ban mở ra ở trạng thái thu gọn).'),
       ('Bấm mũi tên / tên dòng Phòng ban', 'Click', 'After:\n– Thu gọn / mở rộng danh sách NVKD của phòng.'),
       ('Chuyển trang / đổi số dòng mỗi trang', 'Click / Change',
        'After:\n– Tải lại báo cáo theo trang mới (đổi số dòng thì về trang 1), giữ nguyên chế độ xem hiện tại.'),
   ])

# ------------------------------------------------------------------ 2.2 Tìm kiếm và lọc
fn('Tìm kiếm và lọc',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của báo cáo tại phần mô tả '
         'chi tiết.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc',
       mota='Lọc báo cáo theo kỳ (ngày tạo dự án TKT), đơn vị, NVKD, khách hàng, loại hình hoạt động – lĩnh vực '
            'kinh doanh khách hàng, ứng dụng, giai đoạn dự án khách hàng, tiến trình dự án.',
       tacnhan=TACNHAN,
       dieukien=DK,
       chinh='1. Người dùng bấm “Tìm kiếm nâng cao” để mở khối lọc.\n'
             '2. Người dùng chọn Kiểu thời gian và các điều kiện lọc.\n'
             '3. Người dùng bấm “Tìm kiếm”.\n'
             '4. Hệ thống về trang 1 và tải lại báo cáo theo điều kiện đã chọn.',
       phu='• Bấm “Làm mới” → xoá mọi điều kiện, về kỳ Tháng hiện tại, chuyển về chế độ xem chi tiết và tải lại.\n'
           '• Đổi Kiểu thời gian → xoá giá trị Tháng và Thời gian đã chọn.\n'
           '• Đổi Công ty → xoá Phòng ban, Bộ phận; đổi Phòng ban → xoá Bộ phận.\n'
           '• Ô Khách hàng gõ dưới 2 ký tự → không gợi ý; không có kết quả → “Không có khách hàng phù hợp”.\n'
           '• Kiểu Tuỳ chỉnh mà chưa chọn ngày → không giới hạn thời gian.\n'
           '• Chọn điều kiện xong nhưng chưa bấm Tìm kiếm → báo cáo chưa thay đổi.'),
   layouts=[dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-loc.png'),
                 shot_caption='Khối Tìm kiếm nâng cao đang mở')],
   ui=[
       ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Tìm kiếm nâng cao',
        'Mở / đóng khối lọc. Mặc định khối lọc đóng.'),
       ('Kiểu thời gian', 'Dropdown', 'Enable', 'Tuỳ chỉnh / Tháng / Năm', 'Có', 'Tháng', '–'),
       ('Tháng', 'Dropdown', 'Enable / Ẩn', 'Tháng 1 – Tháng 12', 'Có khi Kiểu = Tháng', 'Tháng hiện tại',
        'Chỉ hiện khi Kiểu thời gian = Tháng.'),
       ('Năm', 'Dropdown', 'Enable / Ẩn', '10 năm trước → năm sau', 'Có khi Kiểu = Tháng / Năm', 'Năm hiện tại',
        'Ẩn khi Kiểu thời gian = Tuỳ chỉnh.'),
       ('Thời gian', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy – dd/mm/yyyy', 'Không', 'Trống',
        'Khoảng ngày trong 1 ô; chỉ hiện khi Kiểu thời gian = Tuỳ chỉnh.'),
       ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
        'Chỉ hiện với V1. Biểu tượng ổ khoá cạnh nhãn: bấm để hiện cả công ty đã khoá.'),
       ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
        'Hiện với V1 / V2 / V3, danh sách theo phạm vi quyền và Công ty đã chọn; có ổ khoá hiện phòng đã khoá.'),
       ('Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
        'Hiện với V1 / V2 / V3, lọc theo Phòng ban đã chọn; có ổ khoá hiện bộ phận đã khoá.'),
       ('Nhân viên kinh doanh', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
        'Lọc dự án theo NVKD chính (gồm mọi hồ sơ nhân viên của cùng một người).'),
       ('Khách hàng', 'Textbox', 'Enable', 'Gõ tối thiểu 2 ký tự', 'Không', 'Trống',
        'Gợi ý theo tên / mã khách hàng, mỗi dòng gồm tên + mã • số điện thoại; bấm 1 dòng để chọn. Nhấn '
        'Enter = Tìm kiếm.'),
       ('Loại hình hoạt động', 'Dropdown', 'Enable', 'Chọn nhiều', 'Không', 'Trống',
        'Ô cha của cặp Loại hình – Lĩnh vực; có ⓘ mô tả.'),
       ('Lĩnh vực kinh doanh khách hàng', 'Dropdown', 'Enable', 'Chọn nhiều', 'Không', 'Trống',
        'Ô con, chỉ liệt kê lĩnh vực thuộc loại hình đã chọn; có ⓘ mô tả.'),
       ('Ứng dụng', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
        'Chỉ liệt kê ứng dụng đang có ở dự án TKT trong phạm vi quyền; có ⓘ mô tả.'),
       ('Giai đoạn dự án khách hàng', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
        'Mỗi giai đoạn có ⓘ mô tả; giai đoạn đã khoá đang được lọc vẫn hiển thị.'),
       ('Tiến trình dự án', 'Dropdown', 'Enable', 'Danh sách 12 giá trị', 'Không', 'Trống', '–'),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
   ],
   ev=[
       ('Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khối lọc, đổi chữ nút tương ứng.'),
       ('Đổi Kiểu thời gian', 'Change',
        'After:\n– Hiện / ẩn ô Tháng, Năm, Thời gian theo kiểu đã chọn; xoá giá trị Tháng và Thời gian cũ.'),
       ('Đổi Công ty / Phòng ban', 'Change',
        'After:\n– Đổi Công ty → xoá Phòng ban, Bộ phận; đổi Phòng ban → xoá Bộ phận. Danh sách ô con lọc theo ô cha.'),
       ('Gõ vào ô Khách hàng', 'Keypress',
        'During:\n– Từ 2 ký tự trở lên → tìm khách hàng theo tên / mã, hiện danh sách gợi ý (biểu tượng xoay khi '
        'đang tìm).\n– Không có kết quả → “Không có khách hàng phù hợp”.\n'
        'After:\n– Bấm 1 dòng gợi ý → ghi nhận khách hàng, đóng danh sách. Bấm ra ngoài / Esc → đóng danh sách.'),
       ('Bấm Tìm kiếm / Enter ở ô Khách hàng', 'Click / Keypress',
        'After:\n– Áp điều kiện lọc, về trang 1, tải lại báo cáo; giữ nguyên chế độ xem cấp gốc / chi tiết.'),
       ('Bấm Làm mới', 'Click',
        'After:\n– Xoá mọi điều kiện (kể cả cặp Loại hình – Lĩnh vực), đặt lại Kiểu thời gian = Tháng, tháng và năm '
        'hiện tại; chuyển về chế độ xem chi tiết, về trang 1 và tải lại.'),
   ])

# ------------------------------------------------------------------ 2.3 Cài đặt bộ lọc
fn('Cài đặt bộ lọc', code='FR-03', group='crud',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.',
         'search'),
   intro=dict(
       ten='Cài đặt bộ lọc',
       mota='Cho từng người dùng chọn trường lọc nào được hiển thị và thứ tự các trường trong khối Tìm kiếm nâng cao '
            'của báo cáo.',
       tacnhan=TACNHAN,
       dieukien=DK,
       chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
             '2. Hệ thống mở popup liệt kê các trường lọc đang khai báo, đánh số thứ tự.\n'
             '3. Người dùng tích / bỏ tích trường muốn hiển thị, kéo biểu tượng ⋮⋮ để đổi thứ tự.\n'
             '4. Người dùng bấm “Lưu”.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại khối lọc.',
       phu='• Bấm “Khôi phục mặc định” → danh sách về thứ tự gốc, hiện đủ trường (chỉ ghi nhận khi bấm Lưu).\n'
           '• Bấm “Đóng” / dấu × → đóng popup, không lưu.\n'
           '• Lưu lỗi → “Thao tác thất bại”.\n'
           '• Trường bị ẩn đang có giá trị lọc → giá trị đó bị xoá để không lọc ngầm.',
       dacbiet='Cấu hình lưu theo tài khoản người dùng và theo màn; người khác không bị ảnh hưởng.'),
   layouts=[dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('03-cai-dat.png'),
                 shot_caption='Popup Cài đặt bộ lọc')],
   ui=[
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', 'Kèm biểu tượng bánh răng.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường lọc muốn hiển thị; kéo ⋮⋮ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách trường lọc', 'Checkbox', 'Enable', 'Các trường đang có trên khối lọc', 'Không',
        'Theo cấu hình đã lưu',
        'Gồm Kiểu thời gian, Tháng, Năm, Công ty – Phòng ban – Bộ phận, Nhân viên kinh doanh, Khách hàng, '
        'Loại hình hoạt động – Lĩnh vực kinh doanh khách hàng, Ứng dụng, Giai đoạn dự án khách hàng, Tiến '
        'trình dự án (ô Thời gian chỉ có khi Kiểu = Tuỳ chỉnh).'),
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
       mota='Thu gọn nhanh toàn bộ bảng về cấp Công ty (cấp gốc) hoặc mở lại toàn bộ các cấp.',
       tacnhan=TACNHAN,
       dieukien=DK,
       chinh='1. Mặc định bảng ở chế độ chi tiết (mở hết Công ty → Phòng ban → NVKD), nút ghi “Chỉ xem cấp gốc”.\n'
             '2. Người dùng bấm “Chỉ xem cấp gốc” → bảng chỉ còn dòng Tổng và dòng Công ty, nút đổi thành “Xem chi tiết”.\n'
             '3. Người dùng bấm “Xem chi tiết” → bảng mở lại toàn bộ các cấp.',
       phu='• Ở chế độ cấp gốc, người dùng vẫn mở từng công ty / phòng ban bằng mũi tên.\n'
           '• Tìm kiếm / chuyển trang giữ nguyên chế độ đang chọn; Làm mới đưa về chế độ chi tiết.'),
   layouts=[dict(menu=MENU + ' => Chỉ xem cấp gốc', shot=shot('04-cap-goc.png'),
                 shot_caption='Bảng ở chế độ Chỉ xem cấp gốc')],
   ui=[
       ('Nút Chỉ xem cấp gốc', 'Button', 'Enable', '–', 'Hiển thị (chế độ chi tiết)', 'Viền xám, biểu tượng cây.'),
       ('Nút Xem chi tiết', 'Button', 'Enable', '–', 'Ẩn', 'Hiện thay nút trên khi đang ở chế độ cấp gốc; nền xanh.'),
       ('Dòng Công ty ở chế độ cấp gốc', 'Table/Grid', 'Read-only', '–', 'Thu gọn', 'Mũi tên chỉ sang phải.'),
   ], ui_kw=dict(required=False),
   ev=[
       ('Bấm Chỉ xem cấp gốc', 'Click', 'After:\n– Thu gọn mọi Công ty và Phòng ban, đổi nút thành “Xem chi tiết”.'),
       ('Bấm Xem chi tiết', 'Click', 'After:\n– Mở mọi Công ty và Phòng ban, đổi nút thành “Chỉ xem cấp gốc”.'),
   ])

# ------------------------------------------------------------------ 2.5 Cơ cấu
fn('Xem cơ cấu dự án',
   rule=('- Màn Xem chi tiết và UI/UX. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'detail'),
   intro=dict(
       ten='Xem cơ cấu dự án',
       mota='Popup thống kê số dự án và tỷ lệ % theo 1 chiều phân loại của đúng dòng được bấm (Tổng / Công ty / '
            'Phòng ban / NVKD): Tiến trình dự án, Giai đoạn dự án khách hàng, Loại hình hoạt động, Lĩnh vực kinh '
            'doanh khách hàng, Ứng dụng.',
       tacnhan=TACNHAN,
       dieukien=DK + ' Báo cáo đã tải xong.',
       chinh='1. Người dùng bấm “Cơ cấu tiến trình”, “Cơ cấu giai đoạn” hoặc số ở cột Loại hình hoạt động / Lĩnh vực '
             'kinh doanh khách hàng / Ứng dụng của 1 dòng.\n'
             '2. Hệ thống mở popup: dòng phụ đề nêu chiều thống kê, tiêu đề là tên dòng đã bấm.\n'
             '3. Bảng liệt kê từng giá trị, số dự án và tỷ lệ %; chân popup ghi tổng số dự án.\n'
             '4. Người dùng bấm “Đóng” để đóng popup.',
       phu='• Dòng đó không có dữ liệu ở chiều đã chọn → “Không có dữ liệu.”\n'
           '• Popup lấy ngay số liệu đã tải cùng báo cáo, không gọi thêm dữ liệu.'),
   layouts=[dict(menu=MENU + ' => Cơ cấu tiến trình', modal='Cơ cấu dự án',
                 shot=shot('05-co-cau.png'), shot_caption='Popup Cơ cấu tiến trình dự án của 1 công ty'),
            dict(menu=MENU, note='Popup Cơ cấu giai đoạn (cùng khuôn, khác chiều thống kê):',
                 shot=shot('05b-giai-doan.png'), shot_caption='Popup Cơ cấu giai đoạn dự án khách hàng')],
   ui=[
       ('Phụ đề popup', 'Label', 'Hiển thị', '5 giá trị', 'Theo ô bấm',
        '“Cơ cấu tiến trình dự án của các dự án TKT” / “Cơ cấu theo giai đoạn dự án khách hàng của các dự án TKT” / '
        '“Cơ cấu theo loại hình hoạt động khách hàng …” / “Cơ cấu theo lĩnh vực kinh doanh khách hàng …” / '
        '“Cơ cấu theo ứng dụng …”.'),
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Theo dòng bấm',
        '“Tổng tất cả dự án TKT” / “Công ty: <tên>” / “Phòng ban: <tên> (<công ty>)” / “NVKD: <tên> (<phòng> / <công ty>)”.'),
       ('STT', 'Text', 'Read-only', '–', 'Tự đánh', '–'),
       ('Cột giá trị', 'Text', 'Read-only', '–', 'Theo dữ liệu',
        'Tên cột theo chiều: Tiến trình dự án / Giai đoạn dự án khách hàng / Loại hình hoạt động / Lĩnh vực kinh '
        'doanh khách hàng / Ứng dụng. Tiến trình xếp theo thứ tự bước; chiều khác xếp số dự án giảm dần. Giá trị '
        'không còn trong danh mục ghi “Không xác định”.'),
       ('Số dự án', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu', '–'),
       ('Tỷ lệ (%)', 'Text', 'Read-only', '0 – 100%', 'Theo dữ liệu', 'Số dự án / tổng của bảng, 1 chữ số thập phân.'),
       ('Tổng số dự án', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', 'Chân popup “<n> dự án”.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu.”'),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '–'),
   ], ui_kw=dict(required=False),
   ev=[
       ('Bấm Cơ cấu tiến trình / Cơ cấu giai đoạn / số Loại hình – Lĩnh vực – Ứng dụng', 'Click',
        'After:\n– Mở popup với số liệu của đúng dòng được bấm theo chiều tương ứng.'),
       ('Bấm Đóng / ngoài popup / Esc', 'Click / Keypress', 'After:\n– Đóng popup.'),
   ])

# ------------------------------------------------------------------ 2.6 Danh sách dự án
fn('Xem danh sách dự án chi tiết',
   rule=('- Màn Xem chi tiết, Kịch bản tìm kiếm và UI/UX. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.',
         'detail'),
   intro=dict(
       ten='Xem danh sách dự án chi tiết',
       mota='Popup liệt kê các dự án TKT đứng sau 1 ô số liệu của 1 dòng: Số lượng dự án TKT, Số giải pháp đã làm, '
            'Số giải pháp chốt được, Dự án có báo giá, Số lượng báo giá, Dự án có HĐ, Số lượng HĐ, Giải pháp không '
            'chốt được HĐ.',
       tacnhan=TACNHAN,
       dieukien=DK + ' Báo cáo đã tải xong.',
       chinh='1. Người dùng bấm số ở 1 ô số liệu của dòng Tổng / Công ty / Phòng ban / NVKD.\n'
             '2. Hệ thống lấy dự án theo điều kiện lọc đang áp + đơn vị / NVKD của dòng, rồi lọc theo loại ô.\n'
             '3. Hệ thống mở popup danh sách dự án (tối đa 500 dự án), chân popup ghi số dự án.\n'
             '4. Người dùng lọc tiếp trong popup theo Tiến trình dự án, Loại hình hoạt động hoặc ô Tìm kiếm.\n'
             '5. Người dùng bấm mã giải pháp để mở giải pháp ở tab mới, hoặc bấm “Đóng”.',
       phu='• Ô Dự án có HĐ / Số lượng HĐ → popup rỗng, phụ đề kèm “(Số HĐ/Giá trị HĐ chưa có dữ liệu backend)”.\n'
           '• Ô Giải pháp không chốt được HĐ → popup dùng khuôn cột riêng, cột Lý do không ký HĐ ghi '
           '“Chưa có dữ liệu lý do từ backend”.\n'
           '• Không có dự án phù hợp → “Không có dữ liệu phù hợp.”\n'
           '• Lỗi khi tải → “Không tải được danh sách chi tiết”, popup vẫn mở với danh sách rỗng.\n'
           '• Bấm “Làm mới” trong popup → xoá 3 điều kiện lọc của popup; mở popup mới cũng tự xoá.'),
   layouts=[dict(menu=MENU + ' => Số lượng dự án TKT', modal='Danh sách dự án',
                 shot=shot('06-ds-du-an.png'), shot_caption='Popup Danh sách dự án TKT của 1 phòng ban')],
   ui=[
       ('Phụ đề popup', 'Label', 'Hiển thị', '–', '–', 'Theo ô bấm',
        '“Danh sách dự án TKT” / “Danh sách dự án đã làm giải pháp” / “Danh sách dự án đã chốt giải pháp” / '
        '“Danh sách dự án đã chuyển thành Báo giá” / “Danh sách dự án có Báo giá” / “Danh sách dự án đã chuyển '
        'thành Hợp đồng” / “Danh sách dự án có Hợp đồng” / “Danh sách dự án không chốt được HĐ”.'),
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Theo dòng bấm', 'Cùng quy tắc với popup Cơ cấu (FR-05).'),
       ('Tiến trình dự án', 'Dropdown', 'Enable', 'Danh sách 12 giá trị', 'Không', 'Trống',
        'Gợi ý “Chọn tiến trình nội bộ”; lọc ngay trên danh sách đang hiển thị.'),
       ('Loại hình hoạt động', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
        'Gợi ý “Chọn loại hình hoạt động”.'),
       ('Tìm kiếm', 'Textbox', 'Enable', 'Không giới hạn', 'Không', 'Trống',
        'Gợi ý “Dự án / KH / NVKD”; tìm theo tên dự án, mã dự án, tên khách hàng, tên NVKD, lọc ngay khi gõ.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá 3 điều kiện lọc của popup.'),
       ('#', 'Text', 'Read-only', '–', '–', 'Tự đánh', '–'),
       ('Dự án', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', 'Tên dự án TKT.'),
       ('Mã giải pháp', 'Link', 'Enable', '–', '–', 'Theo dữ liệu',
        'Mã giải pháp mới nhất; bấm mở chi tiết giải pháp ở tab mới; chưa có ghi “-”.'),
       ('NVKD / Khách hàng', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', 'Thiếu ghi “—”.'),
       ('Giai đoạn dự án khách hàng', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', 'Thiếu ghi “—”.'),
       ('Tiến trình dự án', 'Badge', 'Read-only', '12 giá trị', '–', 'Theo dữ liệu', 'Nhãn màu theo tiến trình.'),
       ('Số BG / Giá trị BG', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
        'Chỉ báo giá được tính (xem BR-04); giá trị 1,234,567 đ, bằng 0 ghi “-”.'),
       ('Số HĐ / Giá trị HĐ', 'Number', 'Read-only', '–', '–', '0 / “-”', 'Chưa có nguồn dữ liệu hợp đồng.'),
       ('Lý do không ký HĐ', 'Text', 'Read-only / Ẩn', '–', '–', 'Ẩn',
        'Chỉ có ở popup Giải pháp không chốt được HĐ (thay cho 4 cột BG/HĐ).'),
       ('Số dự án', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu', 'Chân popup “<n> dự án” (đếm sau khi lọc trong popup).'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '“Không có dữ liệu phù hợp.”'),
       ('Nút Đóng / ×', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
   ],
   ev=[
       ('Bấm 1 ô số liệu của dòng', 'Click',
        'Before:\n– Lấy điều kiện lọc đang áp dụng của báo cáo + đơn vị / NVKD của dòng được bấm.\n'
        'During:\n– Ô báo giá: bỏ điều kiện Tiến trình dự án, chỉ lấy dự án có báo giá được tính.\n'
        '– Ô Số giải pháp đã làm: giữ dự án đã có giải pháp; Số giải pháp chốt được: giải pháp ở trạng thái '
        'Chốt giải pháp; Giải pháp không chốt được HĐ: dự án ở tiến trình Đóng/Không thực hiện dự án.\n'
        '– Ô hợp đồng: không gọi dữ liệu, mở popup rỗng.\n'
        'After:\n– Mở popup với danh sách đã lọc; lỗi → “Không tải được danh sách chi tiết”.'),
       ('Chọn Tiến trình / Loại hình, gõ Tìm kiếm', 'Change / Keypress', 'After:\n– Lọc ngay danh sách trong popup, cập nhật số dự án ở chân popup.'),
       ('Bấm Làm mới (popup)', 'Click', 'After:\n– Xoá 3 điều kiện lọc của popup, hiện lại đủ danh sách.'),
       ('Bấm mã giải pháp', 'Click', 'After:\n– Mở màn chi tiết giải pháp ở tab mới.'),
       ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup.'),
   ])

# ------------------------------------------------------------------ 2.7 Xuất Excel
fn('Xuất Excel', code='FR-07', group='io',
   rule=('- Quy tắc Excel và Thông báo. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'excel'),
   intro=dict(
       ten='Xuất Excel',
       mota='Tải về file Excel toàn bộ báo cáo theo điều kiện lọc đang áp dụng (không phân trang).',
       tacnhan=TACNHAN,
       dieukien=DK,
       chinh='1. Người dùng bấm “Xuất Excel”.\n'
             '2. Hệ thống dựng file theo điều kiện lọc đang áp dụng, gồm mọi công ty, phòng ban, NVKD.\n'
             '3. Trình duyệt tải file “bao_cao_du_an_tkt.xls”; hệ thống báo “Xuất Excel thành công”.',
       phu='• Lỗi khi dựng / tải file → “Lỗi khi xuất Excel”.\n'
           '• Điều kiện đã chọn trên khối lọc nhưng chưa bấm Tìm kiếm thì không được dùng.',
       dacbiet='File gồm: ảnh tiêu đề (letterhead) của công ty đang làm việc — chưa cấu hình thì dùng ảnh mặc định; '
               'dòng tiêu đề “BÁO CÁO VÒNG ĐỜI DỰ ÁN TKT”; 18 cột như bảng trên màn (gộp 2 cột cơ cấu tiến trình / '
               'giai đoạn không xuất); các dòng Σ Tổng, Công ty (STT 1, 2…), Phòng ban, NVKD; tô màu dòng Tổng / '
               'Công ty / Phòng ban.'),
   layouts=[dict(menu=MENU + ' => Xuất Excel', shot=shot('07-xuat.png'),
                 shot_caption='Bấm Xuất Excel — file được tải về và hiện thông báo thành công')],
   ui=[
       ('Nút Xuất Excel', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Biểu tượng file Excel.'),
       ('Thanh tiến trình đầu trang', 'Loading', 'Hiển thị', '–', '–', 'Ẩn', 'Chạy trong lúc dựng file.'),
       ('Tên file', 'Text', 'Read-only', '–', '–', 'bao_cao_du_an_tkt.xls', '–'),
       ('Cột trong file', 'Table/Grid', 'Read-only', '18 cột', '–', 'Theo dữ liệu',
        'STT · Công ty / Phòng ban / Nhân viên · Số lượng dự án TKT · Loại hình hoạt động · Lĩnh vực kinh doanh '
        'khách hàng · Ứng dụng · Số GP đã làm · Số GP chốt được · Tỷ lệ chốt GP · Dự án có báo giá · Số lượng '
        'báo giá · Giá trị báo giá · Tỷ lệ chuyển BG · Dự án có HĐ · Số lượng HĐ · Giá trị HĐ · Tỷ lệ chuyển HĐ · '
        'Giải pháp không chốt được HĐ.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '“Xuất Excel thành công” / “Lỗi khi xuất Excel”.'),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Người dùng đã đăng nhập; lấy điều kiện lọc đang áp dụng, bỏ phân trang.\n'
        'During:\n– Tổng hợp dữ liệu theo phạm vi quyền (BR-01) và điều kiện lọc.\n'
        'After:\n– Tải file bao_cao_du_an_tkt.xls, hiển thị “Xuất Excel thành công”.\n'
        '– Lỗi → “Lỗi khi xuất Excel”.'),
   ])

# ------------------------------------------------------------------ 2.8 In
fn('In báo cáo', code='FR-08', group='io',
   rule=('- Màn Xem chi tiết và Thông báo. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'detail'),
   intro=dict(
       ten='In báo cáo',
       mota='Mở bản xem trước để in toàn bộ báo cáo theo điều kiện lọc đang áp dụng, khổ A4 ngang.',
       tacnhan=TACNHAN,
       dieukien=DK,
       chinh='1. Người dùng bấm “In báo cáo”.\n'
             '2. Hệ thống mở tab mới, tải toàn bộ báo cáo (không phân trang) theo điều kiện lọc đang áp dụng.\n'
             '3. Bản xem trước gồm letterhead công ty, tiêu đề “BÁO CÁO VÒNG ĐỜI DỰ ÁN TKT”, bảng số liệu và ô ký '
             '“Ngày ...., tháng ...., năm .... / Người lập / (Ký, họ tên)”.\n'
             '4. Người dùng bấm “In” → mở hộp thoại in của trình duyệt (A4 ngang, lề 8mm × 6mm).',
       phu='• Lỗi khi tải dữ liệu → khung đỏ hiển thị nội dung lỗi hoặc “Lỗi không xác định khi tải dữ liệu báo cáo”.\n'
           '• Không có dữ liệu → bảng ghi “Không có dữ liệu”.'),
   layouts=[dict(menu=MENU + ' => In báo cáo', shot=shot('08-in.png'),
                 shot_caption='Bản xem trước In báo cáo vòng đời dự án TKT')],
   ui=[
       ('Nút In', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Không xuất hiện trên bản in.'),
       ('Letterhead', 'Image', 'Hiển thị', '–', '–', 'Theo công ty đang làm việc',
        'Ảnh tiêu đề của công ty đang làm việc; chưa cấu hình thì dùng ảnh mặc định.'),
       ('Tiêu đề', 'Label', 'Hiển thị', '–', '–', 'BÁO CÁO VÒNG ĐỜI DỰ ÁN TKT', '–'),
       ('Bảng số liệu', 'Table/Grid', 'Read-only', '18 cột', '–', 'Theo dữ liệu',
        'Cùng 18 cột với file Excel; STT dạng Σ / 1 / 1.1 / 1.1.1; tên lùi lề theo cấp; dòng Tổng nền xanh lá, '
        'Công ty nền xanh dương, Phòng ban nền xám.'),
       ('Ô ký', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Ngày ...., tháng ...., năm ....”, “Người lập”, “(Ký, họ tên)”.'),
       ('Khung báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Nền đỏ, không in ra.'),
   ],
   ev=[
       ('Bấm In báo cáo', 'Click',
        'Before:\n– Lấy điều kiện lọc đang áp dụng, bỏ phân trang.\n'
        'After:\n– Mở tab bản xem trước, tải dữ liệu và dựng bảng.'),
       ('Bấm In', 'Click', 'After:\n– Mở hộp thoại in, khổ A4 ngang.'),
   ])

# ==================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Báo cáo vòng đời dự án TKT; không lặp lại các quy tắc đã '
           'có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi dữ liệu theo quyền', [
        '– V1: mọi dự án TKT. V2: dự án thuộc công ty đang làm việc + dự án mình tạo. V3: dự án thuộc phòng ban / '
        'bộ phận mình quản lý + dự án mình tạo. Không có quyền nào: dự án mình tạo hoặc mình là NVKD chính.',
        '– Áp như nhau cho bảng, popup danh sách, Xuất Excel, In.',
    ], 'Toàn màn hình'),
    ('BR-02', 'Tập dự án được tính', [
        '– Không tính dự án cha.',
        '– Dự án ở tiến trình “Đang tạo” chỉ tính khi do chính người dùng tạo.',
        '– Kỳ báo cáo lọc theo NGÀY TẠO dự án TKT (Tháng / Năm / khoảng ngày tuỳ chỉnh).',
    ], 'Toàn màn hình'),
    ('BR-03', 'Cách gom cây Công ty → Phòng ban → NVKD', [
        '– Công ty / phòng ban lấy theo dự án; dự án không ghi thì lấy theo công ty / phòng ban của NVKD chính.',
        '– Một người có nhiều hồ sơ nhân viên được gom thành 1 dòng NVKD.',
        '– Phân trang theo NVKD; dòng Tổng / Công ty / Phòng ban luôn là tổng của toàn bộ dữ liệu.',
    ], ['Xem báo cáo', 'Xuất Excel', 'In báo cáo']),
    ('BR-04', 'Công thức các nhóm cột', [
        '– Cơ cấu: Loại hình hoạt động / Lĩnh vực kinh doanh khách hàng / Ứng dụng = số giá trị KHÁC NHAU có ở '
        'các dự án của dòng.',
        '– Số giải pháp đã làm = số dự án đã có giải pháp; Số giải pháp chốt được = số dự án có giải pháp mới '
        'nhất ở trạng thái Chốt giải pháp; Tỷ lệ chốt GP = chốt được / đã làm × 100%.',
        '– Báo giá chỉ tính báo giá ở trạng thái Chờ TP duyệt, Chờ BGĐ duyệt, Đã duyệt, Trúng thầu; Giá trị báo '
        'giá = tổng tiền sau thuế; Tỷ lệ chuyển BG = Dự án có báo giá / Số lượng dự án TKT × 100%.',
        '– Tỷ lệ làm tròn 1 chữ số thập phân.',
    ], ['Xem báo cáo', 'Xem danh sách dự án chi tiết', 'Xuất Excel', 'In báo cáo']),
    ('BR-05', 'Nhóm cột Hợp đồng và Giải pháp không chốt được HĐ', [
        '– Chưa có nguồn dữ liệu hợp đồng: Dự án có HĐ, Số lượng HĐ, Giá trị HĐ, Tỷ lệ chuyển HĐ luôn là 0; '
        'popup tương ứng rỗng.',
        '– Ô Giải pháp không chốt được HĐ luôn hiển thị 0, nhưng popup liệt kê dự án ở tiến trình Đóng/Không '
        'thực hiện dự án.',
    ], ['Xem báo cáo', 'Xem danh sách dự án chi tiết']),
    ('BR-06', 'Điều kiện lọc chỉ áp dụng khi bấm Tìm kiếm', [
        '– Chọn điều kiện trên khối lọc chưa làm đổi báo cáo; Tìm kiếm / Enter ở ô Khách hàng mới áp dụng và '
        'về trang 1.',
        '– Xuất Excel, In, popup danh sách dùng điều kiện ĐÃ áp dụng.',
    ], ['Tìm kiếm và lọc', 'Xuất Excel', 'In báo cáo']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

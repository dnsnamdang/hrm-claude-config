# -*- coding: utf-8 -*-
"""Sinh "SRS - Nhiệm vụ.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/tasks/index.vue
      pages/assign/tasks/components/{CreateTaskModal,ImportResultModal,TaskHistoryModal}.vue
      components/{V2BaseSmartFilterPanel,V2BaseDataTable,V2BaseRowActions}.vue
      components/modal/{filter-customization-modal,column-customization-modal,export-fields-modal}.vue
      components/comments/{CommentThread,CommentNode,CommentEditor}.vue · components/assign/SystemInfoSection.vue
      components/menu-sidebar.js (menuItemsAssign › Nhiệm vụ) · components/subsystem-menu/presale.js
  BE  Modules/Assign/Routes/api.php (prefix assign/tasks — KHÔNG gắn checkPermission; store gắn solutionMemberActive)
      Http/Controllers/Api/V1/{TaskController,TaskCommentController}.php
      Http/Requests/Task/{TaskStoreRequest,TaskUpdateRequest}.php · Services/TaskService.php
      Entities/Task/Task.php (STATUS, canEdit/canDelete/canImportResult/canStartApprove/canResultApprove,
      getAllowedNextStatuses) · Transformers/TaskResource/TaskResource.php
      app/ExcelExport/ExportColumnRegistry.php ['tasks'] · app/Http/Middleware/CheckSolutionMemberActive.php
      app/Console/Commands/NotifyTaskReport.php
  Quyền: PermissionsTableSeeder id 1020, 1103-1106 (nhóm "Nhiệm vụ")
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
from docx.shared import Inches  # noqa: E402

SHOTS = os.path.join(HERE, 'shots')


def shot(name):
    return os.path.join(SHOTS, name)


TEN_MAN = 'Nhiệm vụ'
MENU = 'Phân hệ Công việc => Nhiệm vụ => Nhiệm vụ'
MENU_B = 'Phân hệ CSKH trước bán => Nhiệm vụ'

A_ALL = 'Người dùng đã đăng nhập'
A_TAO = 'Người tạo nhiệm vụ'
A_DTK = 'Người duyệt triển khai'
A_TH = 'Người thực hiện'
A_DKQ = 'Người duyệt kết quả'

ICONS = {
    'Phân hệ Công việc': 'icon_phanhe_cv.png',
    'Phân hệ CSKH trước bán': 'icon_phanhe_presale.png',
    'Tạo mới': 'icon_taomoi.png',
    'Chế độ nâng cao': 'icon_nangcao.png',
    'Sửa': 'icon_sua.png',
    'Xóa': 'icon_xoa.png',
    'Nhập kết quả': 'icon_nhapkq.png',
    'Duyệt': 'icon_duyet.png',
    'Lịch sử': 'icon_lichsu.png',
    'Mã nhiệm vụ': 'icon_ma.png',
    'Xuất Excel': 'icon_xuat.png',
    'Tuỳ chỉnh cột': 'icon_cot.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Lọc nhanh theo vai trò': 'icon_locnhanh.png',
}

out = os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN)
d = SrsDoc(out=out, menu=MENU, route='', full_url='', img_prefix='task_')
d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})

# "Nhiệm vụ" vừa là NHÓM menu vừa là MỤC menu (và là mục cấp 1 của phân hệ CSKH trước bán) — 3 icon
# khác nhau cho cùng 1 chữ nên dòng Menu phải chọn icon theo VỊ TRÍ chặng, không theo chữ.
_POS_ICON = {
    ('Phân hệ Công việc', 1): shot('icon_nhom_nhiemvu.png'),
    ('Phân hệ Công việc', 2): shot('icon_man_nhiemvu.png'),
    ('Phân hệ CSKH trước bán', 1): shot('icon_presale_nhiemvu.png'),
}


def _menu_para(menu):
    par = d.p('Menu: ')
    segs = menu.split(' => ')
    for i, seg in enumerate(segs):
        if i:
            par.add_run(' => ')
        icon = _POS_ICON.get((segs[0], i)) if seg == 'Nhiệm vụ' else None
        for j, part in enumerate(seg.split(' / ')):
            if j:
                par.add_run(' / ')
            ic = icon or d.menu_icons.get(part)
            par.add_run(part + (' ' if ic else ''))
            if ic:
                par.add_run().add_picture(ic, height=Inches(d.menu_icon_h))
    return par


d._menu_para = _menu_para


def lay(suffix, png, caption, modal=None):
    """Mục Layout: liệt kê đủ 2 lối vào menu rồi mới tới ảnh."""
    d.layout(menu=MENU + suffix, modal=None)
    _menu_para(MENU_B + suffix)
    if modal:
        d.p('Cửa sổ %s được mở ngay trên màn hình danh sách theo một trong hai đường dẫn ở trên.' % modal)
    d.figure(shot(png), caption, width_in=6.2)


d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

NO_PERM = '– Nếu không thỏa điều kiện → nút không hiển thị; gọi thẳng chức năng thì hệ thống từ chối và dừng xử lý.'
SCOPE = '– Chỉ lấy nhiệm vụ trong phạm vi được xem của người dùng (xem quy tắc BR-01).'

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Nhiệm vụ (phân hệ Công việc, đồng thời có lối vào ở phân hệ '
    'CSKH trước bán), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu các chức năng: xem, tìm kiếm/lọc, cài đặt bộ lọc, tuỳ chỉnh cột, tạo mới (chế độ '
    'đơn giản và nâng cao), chỉnh sửa, xem chi tiết, xóa, duyệt triển khai, nhập kết quả, duyệt kết quả, '
    'bình luận, xuất Excel và xem lịch sử chỉnh sửa nhiệm vụ.',
    'Làm rõ vòng đời trạng thái của nhiệm vụ: ai được chuyển trạng thái nào, ở bước nào, và ai nhận thông báo.',
    'Làm rõ phạm vi nhiệm vụ mỗi người dùng được xem theo vai trò trên nhiệm vụ, thành viên dự án/giải pháp '
    'và quyền xem theo cấp tổ chức.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Nhiệm vụ', 'Một đầu việc giao cho 1 người thực hiện, có hạn hoàn thành, số giờ được giao, có thể gắn '
     'giải pháp / dự án / hạng mục / cuộc họp.'),
    ('Nhiệm vụ cụ thể', 'Loại nhiệm vụ giao cho đúng 1 người thực hiện.'),
    ('Nhiệm vụ chung', 'Loại nhiệm vụ giao cùng lúc cho nhiều người; khi lưu, hệ thống tạo cho mỗi người một '
     'nhiệm vụ riêng (dùng chung nội dung).'),
    ('Nhiệm vụ con', 'Nhiệm vụ sinh ra từ dòng “Nhiệm vụ con” của một nhiệm vụ cha; được tạo thành nhiệm vụ thật '
     'khi nhiệm vụ cha rời trạng thái Nháp / Chờ phê duyệt triển khai.'),
    ('Checklist', 'Danh sách đầu mục cần làm trong 1 nhiệm vụ; người thực hiện đánh dấu đã xong khi nhập kết quả.'),
    ('Người tạo (người giao)', 'Người lập nhiệm vụ.'),
    ('Người thực hiện (người làm)', 'Người được giao làm nhiệm vụ, là người nhập kết quả.'),
    ('Người duyệt kết quả', 'Người duyệt kết quả khi nhiệm vụ ở trạng thái “Hoàn thành - Chờ duyệt”. Bỏ trống '
     'thì người thực hiện được chuyển thẳng sang “Hoàn thành”.'),
    ('Người duyệt triển khai', 'Người có quyền “Duyệt triển khai Nhiệm vụ” và quản lý phòng ban của người thực '
     'hiện; duyệt nhiệm vụ ở trạng thái “Chờ phê duyệt triển khai”.'),
    ('Người theo dõi', 'Người được thêm vào để theo dõi nhiệm vụ, nhận thông báo bình luận.'),
    ('Báo cáo tiến độ', 'Cấu hình buộc người thực hiện báo cáo theo chu kỳ (ngày/tuần/tháng); khi bật, phần kết '
     'quả chuyển thành nhật ký theo từng ngày báo cáo.'),
    ('Tình trạng hạn', '“Trong hạn” / “Quá hạn” so thời điểm hiện tại với Hạn hoàn thành + Giờ hạn; bỏ trống với '
     'nhiệm vụ Nháp, Hoàn thành, Huỷ.'),
    ('Hiệu suất', 'Số giờ được giao / Số giờ làm thực tế × 100%, tính khi chuyển sang Hoàn thành - Chờ duyệt '
     'hoặc Hoàn thành.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Duyệt triển khai Nhiệm vụ',
     'Duyệt / từ chối triển khai nhiệm vụ “Chờ phê duyệt triển khai” có người thực hiện thuộc phòng ban mình '
     'quản lý (kể cả phòng ban của chính mình); thấy thêm các nhiệm vụ đó trong danh sách; nhận thông báo khi có '
     'nhiệm vụ cần phê duyệt triển khai.'),
], widths=[0.8, 2.0, 3.2])
d.p('Các thao tác còn lại không gắn quyền mà do VAI TRÒ của người dùng trên từng nhiệm vụ quyết định:')
d.table(['Ký hiệu', 'Vai trò', 'Tác dụng trên màn hình'], [
    ('R1', 'Người tạo nhiệm vụ', 'Sửa nhiệm vụ (khi nhiệm vụ chưa có nhiệm vụ con); xóa nhiệm vụ Nháp chưa có '
     'nhiệm vụ con; chuyển trạng thái theo BR-04.'),
    ('R2', 'Người thực hiện', 'Nhập kết quả khi nhiệm vụ ở Chờ bắt đầu / Đang thực hiện / Từ chối kết quả; chuyển '
     'trạng thái theo BR-04.'),
    ('R3', 'Người duyệt kết quả', 'Duyệt / từ chối kết quả khi nhiệm vụ ở Hoàn thành - Chờ duyệt.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem danh sách Nhiệm vụ theo tổng công ty', 'Xem toàn bộ nhiệm vụ (trừ nhiệm vụ Nháp của người khác).'),
    ('V2', 'Xem danh sách Nhiệm vụ theo công ty',
     'Thêm các nhiệm vụ có ít nhất 1 người tạo / thực hiện / duyệt kết quả / theo dõi thuộc công ty đang làm việc.'),
    ('V3', 'Xem danh sách Nhiệm vụ theo phòng ban',
     'Thêm các nhiệm vụ có ít nhất 1 người giữ vai trò thuộc phòng ban hoặc bộ phận mình quản lý.'),
    ('V4', 'Xem danh sách Nhiệm vụ theo bộ phận',
     'Thêm các nhiệm vụ có ít nhất 1 người giữ vai trò thuộc bộ phận mình quản lý.'),
    ('–', 'Không có quyền nào',
     'Chỉ nhiệm vụ mình giữ vai trò (tạo / thực hiện / duyệt kết quả / theo dõi), nhiệm vụ cha – con của các '
     'nhiệm vụ đó, và nhiệm vụ thuộc dự án / giải pháp mình là thành viên.'),
], widths=[0.8, 2.2, 3.0])

d.h2('2 Ma trận phân quyền')
Y, N = '✅', '❌'
d.table(['Chức năng', 'Q1', 'R1', 'R2', 'R3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách nhiệm vụ', Y, Y, Y, Y, '✅ (theo phạm vi)'),
    ('FR-02 Tìm kiếm và lọc', Y, Y, Y, Y, Y),
    ('FR-03 Cài đặt bộ lọc', Y, Y, Y, Y, Y),
    ('FR-04 Tuỳ chỉnh cột', Y, Y, Y, Y, Y),
    ('FR-05 Tạo mới nhiệm vụ – chế độ đơn giản', Y, Y, Y, Y, Y),
    ('FR-06 Tạo mới nhiệm vụ – chế độ nâng cao', Y, Y, Y, Y, Y),
    ('FR-07 Chỉnh sửa nhiệm vụ', N, Y, '✅ (chỉ đổi trạng thái)', N, N),
    ('FR-08 Xem chi tiết nhiệm vụ', Y, Y, Y, Y, Y),
    ('FR-09 Xóa nhiệm vụ', N, '✅ (Nháp)', N, N, N),
    ('FR-10 Duyệt triển khai', Y, N, N, N, N),
    ('FR-11 Nhập kết quả', N, N, Y, N, N),
    ('FR-12 Duyệt kết quả', N, N, N, Y, N),
    ('FR-13 Bình luận', Y, Y, Y, Y, Y),
    ('FR-14 Xuất Excel', Y, Y, Y, Y, Y),
    ('FR-15 Xem lịch sử chỉnh sửa', Y, Y, Y, Y, Y),
], widths=[2.6, 0.5, 0.7, 0.9, 0.5, 0.9])
d.p('R1–R3 là vai trò trên nhiệm vụ cụ thể, không phải quyền gán cho vai trò hệ thống. Nút thao tác không dùng '
    'được thì ẩn hẳn.')

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_ALL, [0, 1, 2, 8, 9]), (A_TAO, [3, 4]), (A_DTK, [5]), (A_TH, [6]), (A_DKQ, [7])],
    [('FR-01', 'Xem danh sách nhiệm vụ', 'view'),
     ('FR-05', 'Tạo mới – chế độ đơn giản', 'crud'),
     ('FR-06', 'Tạo mới – chế độ nâng cao', 'crud'),
     ('FR-07', 'Chỉnh sửa nhiệm vụ', 'crud'),
     ('FR-09', 'Xóa nhiệm vụ', 'action'),
     ('FR-10', 'Duyệt triển khai', 'action'),
     ('FR-11', 'Nhập kết quả', 'crud'),
     ('FR-12', 'Duyệt kết quả', 'action'),
     ('FR-13', 'Bình luận', 'crud'),
     ('FR-14', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-08', 'Xem chi tiết nhiệm vụ', 'view', 'extend', [0], None),
     ('FR-15', 'Xem lịch sử chỉnh sửa', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách nhiệm vụ')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Phân trang và UI/UX. Chỉ bổ sung các quy tắc riêng của màn Nhiệm vụ tại phần mô tả '
           'chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách nhiệm vụ',
    mota='Hiển thị bảng các nhiệm vụ người dùng được xem, kèm tổng số và số nhiệm vụ quá hạn; mỗi dòng có các nút '
         'thao tác theo vai trò của người dùng trên nhiệm vụ đó.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập hệ thống.',
    chinh='1. Người dùng mở màn Nhiệm vụ theo một trong hai lối vào menu.\n'
          '2. Hệ thống nạp danh sách nhiệm vụ trong phạm vi được xem, mới tạo trước, 10 dòng/trang.\n'
          '3. Hệ thống hiển thị ô Tổng, ô Quá hạn, 4 nút lọc nhanh theo vai trò và bảng nhiệm vụ.\n'
          '4. Mỗi dòng hiển thị các nút thao tác người dùng được phép (Sửa, Xóa, Nhập kết quả, Duyệt, Lịch sử).',
    phu='• Không có nhiệm vụ nào khớp → bảng hiển thị “Không có dữ liệu phù hợp bộ lọc.”.\n'
        '• Lỗi khi nạp → thông báo “Lỗi khi tải dữ liệu”, bảng trống.\n'
        '• Quay lại màn trong vòng 10 phút → khôi phục bộ lọc và trạng thái đóng/mở khối lọc đã dùng.\n'
        '• Mở từ đường dẫn trong thông báo (chuông) → hệ thống mở thẳng cửa sổ xem nhiệm vụ đó, cuộn tới bình '
        'luận được nhắc tới (nếu có).')
d.p('2.1.2 Layout màn hình')
lay('', '01-danh-sach.png', 'Danh sách nhiệm vụ lúc mới mở')
d.p('Cả hai lối vào mở cùng một màn, cùng phạm vi dữ liệu (theo quy tắc BR-01).')
d.figure(shot('01c-danh-sach-giua.png'), 'Các cột Loại nhiệm vụ, Mức độ ưu tiên, Tình trạng hạn, Người làm…',
         width_in=6.2)
d.figure(shot('01b-danh-sach-phai.png'), 'Các cột người liên quan và ngày (cuộn ngang bảng)', width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang / tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Danh sách nhiệm vụ', '–'),
    ('Ô Tổng', 'Badge', 'Hiển thị', '≥ 0', 'Theo dữ liệu', '“Tổng: n” — tổng số nhiệm vụ khớp bộ lọc.'),
    ('Ô Quá hạn', 'Badge', 'Hiển thị', '≥ 0', 'Theo dữ liệu',
     '“Quá hạn: n” (đỏ) — số nhiệm vụ khớp bộ lọc đã quá hạn, không tính Nháp / Hoàn thành / Huỷ.'),
    ('4 nút lọc nhanh theo vai trò', 'Icon Button', 'Enable', '–', 'Không bật', 'Xem FR-02.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Thêm mới nhiệm vụ (FR-05).'),
    ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', 'Khoá trong lúc đang xuất (FR-14).'),
    ('Nút Tuỳ chỉnh cột', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Rê chuột: “Cấu hình cột hiển thị” (FR-04).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo trang', 'Ghim bên trái khi cuộn ngang.'),
    ('Cột Mã nhiệm vụ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Ghim bên trái; bấm để xem chi tiết (FR-08). Có sắp xếp.'),
    ('Cột Tên nhiệm vụ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng. Có sắp xếp.'),
    ('Cột Tag', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 4 thẻ, còn lại “+n tag”.'),
    ('Cột Giải pháp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '“Mã - Tên giải pháp”.'),
    ('Cột Version GP', 'Badge', 'Read-only', '–', 'Theo dữ liệu', 'Version giải pháp lúc tạo nhiệm vụ.'),
    ('Cột Dự án', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '“Mã - Tên dự án”, dòng phụ “PM: <tên>”.'),
    ('Cột Hạng mục/Module', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 10 giá trị', 'Theo dữ liệu',
     'Chữ và màu theo trạng thái (BR-03). Có sắp xếp.'),
    ('Cột Loại nhiệm vụ', 'Table/Grid', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu',
     'Nhiệm vụ chung / Nhiệm vụ cụ thể.'),
    ('Cột Ưu tiên', 'Badge', 'Read-only', 'Danh sách 3 giá trị', 'Theo dữ liệu',
     'Bình thường / Cao / Khẩn cấp. Có sắp xếp.'),
    ('Cột Tình trạng hạn', 'Badge', 'Read-only', '–', 'Theo dữ liệu', 'Trong hạn (xanh) / Quá hạn (đỏ).'),
    ('Cột Người làm / Người theo dõi / Người duyệt / Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người theo dõi nối tên bằng dấu phẩy.'),
    ('Cột Ngày bắt đầu', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Có sắp xếp.'),
    ('Cột Hạn hoàn thành', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
     '“Ngày · giờ hạn”, dòng phụ “Ước lượng: n ngày” (từ ngày bắt đầu tới hạn). Có sắp xếp.'),
    ('Cột Checklist/Nhiệm vụ con', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     '“n checklist · n nhiệm vụ con”, dòng phụ “Liên kết: n nhiệm vụ”.'),
    ('Cột Ngày tạo / Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày tạo, Ngày cập nhật có sắp xếp.'),
    ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo vai trò',
     'Sửa · Xóa · Nhập kết quả · Duyệt · Lịch sử; hiện tối đa 3 nút, dư thì gom vào nút “Hành động khác”.'),
    ('Phân trang', 'Pagination', 'Enable', '10 / 20 / 50 / 100', '10 dòng/trang', '“Hiển thị a–b / n”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Nhiệm vụ', 'System',
     'During:\n' + SCOPE + '\n– Không lấy nhiệm vụ Nháp của người khác.\n'
     'After:\n– Hiển thị bảng, ô Tổng, ô Quá hạn; khôi phục bộ lọc nếu quay lại trong 10 phút.\n'
     '– Lỗi → “Lỗi khi tải dữ liệu”.'),
    ('Đổi trang / số dòng mỗi trang', 'Click', 'After:\n– Nạp lại đúng trang; đổi số dòng thì về trang 1.'),
    ('Bấm tiêu đề cột có sắp xếp', 'Click', 'After:\n– Sắp xếp tăng/giảm theo cột đó, về trang 1.'),
    ('Vào màn từ đường dẫn thông báo', 'System',
     'After:\n– Mở cửa sổ xem nhiệm vụ trong đường dẫn, cuộn tới bình luận (nếu có), rồi bỏ tham số khỏi đường dẫn.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Nhiệm vụ tại phần mô '
           'tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc nhiệm vụ',
    mota='Tìm nhanh theo từ khoá, lọc nâng cao theo 14 tiêu chí và lọc nhanh theo vai trò của chính người dùng.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách nhiệm vụ.',
    chinh='1. Người dùng gõ từ khoá vào ô tìm nhanh rồi bấm “Tìm kiếm” (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc, chọn giá trị ở các ô lọc.\n'
          '3. Chọn giá trị ở ô chọn thì hệ thống lọc ngay; ô gõ tay chỉ lọc khi bấm “Tìm kiếm”.\n'
          '4. Hoặc bấm 1 trong 4 nút lọc nhanh: Task tôi làm / Task tôi giao / Task tôi theo dõi / Task tôi duyệt '
          'kết quả.\n'
          '5. Hệ thống nạp lại danh sách từ trang 1.',
    phu='• Bấm lại nút lọc nhanh đang bật, hoặc dấu × cạnh chữ “Đang lọc: …” → bỏ lọc nhanh.\n'
        '• Đổi Giải pháp → các ô Dự án, Hạng mục/Module, Version giải pháp bị xoá giá trị và nạp lại theo giải '
        'pháp mới.\n'
        '• Bấm “Làm mới” → xoá mọi điều kiện lọc, nạp lại danh sách 1 lần.\n'
        '• Lọc Tag → hiện chữ “Tag: …” trên bảng, bấm × để bỏ lọc tag.')
d.p('2.2.2 Layout màn hình')
lay(' => Tìm kiếm nâng cao', '02-loc.png', 'Khối Tìm kiếm nâng cao đang mở')
d.figure(shot('02b-loc-nhanh.png'), 'Đang bật lọc nhanh “Task tôi làm”', width_in=6.2)
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Gợi ý “Tìm theo mã nhiệm vụ, tên nhiệm vụ, tên/mã khách hàng của dự án”.'),
    ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Tìm kiếm nâng cao',
     'Đóng/mở khối lọc.'),
    ('Công ty – Phòng ban – Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     '3 ô theo cấp; chỉ hiện cấp người dùng có quyền V1–V4. Giữ nhiệm vụ có ít nhất 1 người giữ vai trò thuộc '
     'đơn vị chọn.'),
    ('Loại nhiệm vụ', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống', 'Nhiệm vụ chung / cụ thể.'),
    ('Giải pháp', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', '“Mã - Tên giải pháp”.'),
    ('Dự án', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Chỉ có lựa chọn khi đã chọn Giải pháp.'),
    ('Hạng mục/Module', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Hạng mục của giải pháp đã chọn.'),
    ('Version giải pháp', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Các version của giải pháp đã chọn.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 10 giá trị', 'Không', 'Trống', 'Xem BR-03.'),
    ('Mức độ ưu tiên', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Không', 'Trống', '–'),
    ('Người thực hiện / Người duyệt kết quả / Người tạo', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Danh sách nhân viên.'),
    ('Ngày cập nhật', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Khoảng từ – đến, 1 ô.'),
    ('Hạn hoàn thành', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Khoảng từ – đến, 1 ô.'),
    ('Tag', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Chọn nhiều, gõ để tìm; giữ nhiệm vụ có ít nhất 1 tag đã chọn.'),
    ('Nút lọc nhanh Task tôi làm / tôi giao / tôi theo dõi / tôi duyệt kết quả', 'Icon Button', 'Enable', '–',
     '–', 'Không bật', 'Mỗi lúc chỉ bật 1 nút; bật thì nút xanh và hiện “Đang lọc: <tên nút>”.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm / Enter ở ô tìm nhanh', 'Click',
     'After:\n– Tìm nhiệm vụ có mã hoặc tên chứa từ khoá, hoặc dự án có tên/mã khách hàng chứa từ khoá.\n'
     '– Nạp lại từ trang 1.'),
    ('Chọn giá trị ô lọc', 'Change', 'After:\n– Lọc ngay, về trang 1.\n' + SCOPE),
    ('Đổi Giải pháp', 'Change',
     'After:\n– Xoá giá trị Dự án, Hạng mục/Module, Version giải pháp; nạp lại danh sách version của giải pháp.'),
    ('Bấm nút lọc nhanh', 'Click',
     'After:\n– Tắt các nút lọc nhanh khác; nếu nút đang tắt thì lọc theo chính người dùng ở vai trò tương ứng '
     '(người thực hiện / người tạo / người theo dõi / người duyệt kết quả), đang bật thì bỏ lọc.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện lọc (kể cả lọc nhanh, tag), nạp lại trang 1.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Cài đặt bộ lọc')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Bộ lọc và UI/UX. Chỉ bổ sung các quy tắc riêng của màn Nhiệm vụ tại phần mô tả chi tiết.',
           anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Cho người dùng chọn các ô lọc muốn hiện trong khối Tìm kiếm nâng cao và sắp xếp thứ tự; cấu hình lưu '
         'riêng cho màn Nhiệm vụ của từng người dùng.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách nhiệm vụ.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
          '2. Hệ thống mở cửa sổ Cài đặt bộ lọc với 14 trường lọc theo cấu hình hiện tại.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để sắp xếp.\n'
          '4. Người dùng bấm “Lưu”.\n'
          '5. Hệ thống lưu cấu hình, đóng cửa sổ, báo “Cập nhật thành công” và vẽ lại khối lọc.',
    phu='• Bấm “Khôi phục mặc định” → hiện đủ 14 trường theo thứ tự gốc (chưa lưu cho tới khi bấm Lưu).\n'
        '• Bấm “Đóng” / dấu × → đóng cửa sổ, không lưu.\n'
        '• Lưu lỗi → “Thao tác thất bại”.')
d.p('2.3.2 Layout màn hình')
lay(' => Cài đặt bộ lọc', '03-cai-dat-loc.png', 'Cửa sổ Cài đặt bộ lọc')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
    ('Danh sách trường lọc', 'Checkbox', 'Enable', 'Danh sách 14 giá trị', 'Không', 'Theo cấu hình đã lưu',
     'Công ty – Phòng ban – Bộ phận · Loại nhiệm vụ · Giải pháp · Dự án · Hạng mục/Module · Version giải pháp · '
     'Trạng thái · Mức độ ưu tiên · Người thực hiện · Người duyệt kết quả · Người tạo · Ngày cập nhật · Hạn hoàn '
     'thành · Tag; mỗi dòng có số thứ tự và tay kéo ⠿.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở cửa sổ với cấu hình đang áp dụng.'),
    ('Tích / bỏ tích, kéo sắp xếp', 'Click', 'After:\n– Cập nhật danh sách trong cửa sổ, chưa lưu.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Không kiểm tra quyền riêng.\n'
     'After:\n– Lưu cấu hình hiện / ẩn và thứ tự cho màn Nhiệm vụ của người dùng.\n'
     '– Đóng cửa sổ, hiển thị “Cập nhật thành công”.\n– Lỗi → “Thao tác thất bại”.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Hiện đủ trường theo thứ tự gốc; chưa lưu.'),
    ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Tuỳ chỉnh cột')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Nhiệm vụ tại phần mô tả chi '
           'tiết.', anchor='excel')
d.intro_table(
    ten='Tuỳ chỉnh cột',
    mota='Cho người dùng ẩn/hiện và đổi thứ tự các cột của bảng nhiệm vụ; cấu hình lưu riêng cho từng người dùng.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách nhiệm vụ.',
    chinh='1. Người dùng bấm nút Tuỳ chỉnh cột (biểu tượng cột, góc phải bảng).\n'
          '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê đủ 24 cột.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ≡ để đổi thứ tự.\n'
          '4. Người dùng bấm “Lưu”.\n'
          '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
    phu='• Cột STT, Mã nhiệm vụ, Hành động bị khoá: không bỏ tích, không kéo được (biểu tượng ổ khoá).\n'
        '• Bấm “Đóng” / dấu × → không lưu.\n'
        '• Lưu lỗi → “Thao tác thất bại”.',
    dacbiet='Mặc định hiện tất cả cột. Cấu hình cột cũng quyết định các trường được tích sẵn ở cửa sổ Xuất Excel.')
d.p('2.4.2 Layout màn hình')
lay(' => Tuỳ chỉnh cột', '04-tuy-chinh-cot.png', 'Cửa sổ Tuỳ chỉnh cột')
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', '–'),
    ('Danh sách cột', 'Checkbox', 'Enable / Disable', 'Danh sách 24 giá trị', 'Không', 'Theo cấu hình đã lưu',
     'STT, Mã nhiệm vụ, Tên nhiệm vụ, Tag, Giải pháp, Version GP, Dự án, Hạng mục/Module, Trạng thái, Loại '
     'nhiệm vụ, Ưu tiên, Tình trạng hạn, Người làm, Người theo dõi, Người duyệt, Người tạo, Ngày bắt đầu, Hạn '
     'hoàn thành, Checklist/Nhiệm vụ con, Ngày tạo, Người cập nhật, Ngày cập nhật, Hành động.'),
    ('Cột khoá (STT, Mã nhiệm vụ, Hành động)', 'Checkbox', 'Disable', '–', '–', 'Đã tích',
     'Xám + ổ khoá, rê chuột: “Cột bắt buộc — không thể ẩn hoặc đổi vị trí”.'),
    ('Tay kéo ≡', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo đổi vị trí các cột không khoá.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tuỳ chỉnh cột', 'Click', 'After:\n– Mở cửa sổ với cấu hình cột đang áp dụng.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Lưu thứ tự và ẩn/hiện cột cho người dùng.\n– Hiển thị “Cập nhật thành công”, vẽ lại bảng.\n'
     '– Lỗi → “Thao tác thất bại”.'),
    ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ, bỏ thay đổi.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Tạo mới nhiệm vụ – chế độ đơn giản')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Tạo mới nhiệm vụ – chế độ đơn giản', 'crud', actor=A_ALL)
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc '
           'chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới nhiệm vụ – chế độ đơn giản',
    mota='Lập nhiệm vụ với các thông tin cơ bản trên cửa sổ “Thêm mới nhiệm vụ” (mặc định ở chế độ Đơn giản).',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách nhiệm vụ.',
    chinh='1. Người dùng bấm “Tạo mới”.\n'
          '2. Hệ thống mở cửa sổ “Thêm mới nhiệm vụ”, điền sẵn: Loại = Nhiệm vụ cụ thể, Trạng thái = Nháp, Hạn '
          'hoàn thành = hôm nay, Giờ hạn = 17:00, Người duyệt kết quả và Người theo dõi = chính người tạo.\n'
          '3. Người dùng nhập Tên công việc, chọn Người thực hiện, Mức độ ưu tiên, Số giờ được giao và các thông tin '
          'khác.\n'
          '4. Người dùng bấm “Lưu”.\n'
          '5. Hệ thống kiểm tra dữ liệu, sinh mã, lưu nhiệm vụ, báo “Đã lưu nhiệm vụ thành công”, đóng cửa sổ và '
          'nạp lại danh sách.',
    phu='• Chọn Loại = Nhiệm vụ chung → ô Người thực hiện cho chọn nhiều người, hiện dòng “Chọn nhiều người thực '
        'hiện — khi lưu, hệ thống tạo cho mỗi người một nhiệm vụ riêng.”; lưu xong báo “Đã tạo n nhiệm vụ thành '
        'công”.\n'
        '• Bấm “Lưu & Tiếp tục” → lưu rồi xoá trắng form để nhập nhiệm vụ tiếp theo (giữ các giá trị khoá sẵn khi '
        'mở từ màn khác).\n'
        '• Bấm “Xóa trắng” → hỏi “Bạn có chắc muốn xóa trắng toàn bộ nội dung đã nhập?”, đồng ý thì xoá trắng form.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới từng ô và thông báo “Lỗi khi lưu nhiệm vụ”, không lưu.\n'
        '• Người dùng đã bị khoá khỏi giải pháp được chọn → “Bạn đã bị khóa khỏi giải pháp này nên không thao tác '
        'được. Vui lòng liên hệ PM hoặc Trưởng phòng giải pháp.”, không lưu.',
    dacbiet='Trạng thái khi tạo chỉ chọn được: Nháp, Chờ phê duyệt triển khai, Chờ bắt đầu, Đang thực hiện. Mã '
            'sinh tự động theo mẫu <Mã công ty>.TASK.NB.<2 số cuối năm>.<STT 4 số> (STT tăng theo năm và công ty).')
d.p('2.5.3 Layout màn hình')
lay(' => Tạo mới', '05-tao-moi-trong.png', 'Cửa sổ Thêm mới nhiệm vụ – chế độ Đơn giản', modal='Thêm mới nhiệm vụ')
d.figure(shot('05c-tao-moi-loi.png'), 'Báo lỗi khi bấm Lưu thiếu thông tin bắt buộc', width_in=6.2)
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Thêm mới nhiệm vụ',
     'Kèm nhãn trạng thái và nhãn chế độ “Đơn giản” / “Nâng cao”.'),
    ('Nút Chế độ nâng cao / Chuyển về đơn giản', 'Button', 'Enable', '–', '–', 'Chế độ nâng cao', 'Xem FR-06.'),
    ('Nút Xóa trắng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Có hộp xác nhận “Xác nhận xóa trắng”.'),
    ('Loại nhiệm vụ', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Có', 'Nhiệm vụ cụ thể',
     'Nhiệm vụ chung / Nhiệm vụ cụ thể.'),
    ('Tên công việc', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', 'Gợi ý “VD: Thiết kế popup tạo nhiệm vụ”.'),
    ('Giải pháp', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Chỉ giải pháp người dùng là thành viên, ở trạng thái Chờ Leader duyệt / Đang triển khai / Chờ duyệt giải '
     'pháp / Đã duyệt giải pháp / Chờ làm giá / Đã duyệt giá. Chọn giải pháp thì tự điền Dự án của giải pháp.'),
    ('Dự án/Nhóm', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Không', 'Trống',
     'Chỉ dự án người dùng là thành viên; khoá khi đã chọn Giải pháp.'),
    ('Hạng mục/Module', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Có khi giải pháp có hạng mục', 'Trống',
     'Hạng mục Đang triển khai / Chờ duyệt hồ sơ trình duyệt của giải pháp đã chọn; khoá khi chưa chọn giải pháp '
     'hoặc giải pháp không chia hạng mục.'),
    ('Meeting', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Cuộc họp người dùng là thành viên (tối đa 200).'),
    ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống',
     'Nhân viên đang làm việc của công ty hiện tại; Nhiệm vụ chung thì chọn nhiều. Người được chọn tự thêm vào '
     'Người theo dõi.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Có', 'Nháp',
     'Nháp / Chờ phê duyệt triển khai / Chờ bắt đầu / Đang thực hiện.'),
    ('Mức độ ưu tiên', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Có', 'Trống', 'Bình thường / Cao / Khẩn cấp.'),
    ('Hạn hoàn thành', 'Datepicker', 'Enable', 'dd/mm/yyyy, ≥ hôm nay', 'Có', 'Hôm nay', '–'),
    ('Giờ hạn', 'Datepicker', 'Enable', 'hh:mm', 'Có', '17:00', 'Hạn là hôm nay thì giờ hạn ≥ giờ hiện tại.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Trống', 'Gợi ý “Mô tả ngắn gọn yêu cầu…”.'),
    ('Số giờ được giao', 'Number', 'Enable', '≥ 0, bước 0,5', 'Có', 'Trống', 'Gợi ý “VD: 8.0”.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Chữ đỏ dưới ô bị lỗi.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Lưu & Tiếp tục', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chỉ có ở cửa sổ Thêm mới.'),
    ('Nút Đóng / dấu ×', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tạo mới', 'Click', 'After:\n– Mở cửa sổ, điền sẵn giá trị mặc định, nạp danh sách giải pháp / dự án / '
     'cuộc họp người dùng là thành viên.'),
    ('Đổi Loại nhiệm vụ', 'Change', 'After:\n– Bỏ lựa chọn người thực hiện của loại cũ.'),
    ('Chọn Giải pháp', 'Change',
     'After:\n– Tự điền Dự án của giải pháp, xoá Hạng mục/Module; bỏ Người duyệt kết quả nếu người đó không thuộc '
     'nhân sự giải pháp.'),
    ('Bấm Lưu / Lưu & Tiếp tục', 'Click',
     'Before:\n– Người dùng bị khoá khỏi giải pháp được chọn → “Bạn đã bị khóa khỏi giải pháp này nên không thao '
     'tác được. Vui lòng liên hệ PM hoặc Trưởng phòng giải pháp.” và dừng xử lý.\n'
     'During:\n– Tên công việc trống → “Bắt buộc phải nhập”; quá 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”\n'
     '– Người thực hiện trống → “Bắt buộc phải nhập” (Nhiệm vụ chung: “Vui lòng chọn người thực hiện.” / “Vui lòng '
     'chọn ít nhất 1 người thực hiện.”).\n'
     '– Mức độ ưu tiên trống, Số giờ được giao trống → “Bắt buộc phải nhập”; Số giờ âm → “Không được nhỏ hơn 0.”\n'
     '– Giải pháp có hạng mục mà chưa chọn Hạng mục/Module → “Bắt buộc phải nhập”.\n'
     '– Hạn hoàn thành trước hôm nay → “Không được là ngày trong quá khứ.”; hạn là hôm nay mà giờ hạn đã qua → '
     '“Phải lớn hơn hoặc bằng thời điểm hiện tại.”\n'
     '– Nếu có lỗi validate → hiển thị “Lỗi khi lưu nhiệm vụ”, không thực hiện bước After.\n'
     'After:\n– Sinh mã nhiệm vụ; Nhiệm vụ chung thì tạo 1 nhiệm vụ cho mỗi người thực hiện.\n'
     '– Ghi version hiện hành của giải pháp / hạng mục; ghi lịch sử “Tạo mới nhiệm vụ”.\n'
     '– Trạng thái khác Nháp → gửi thông báo theo BR-05; tính lại tiến độ hạng mục / giải pháp.\n'
     '– Hiển thị “Đã lưu nhiệm vụ thành công” (hoặc “Đã tạo n nhiệm vụ thành công”).'),
    ('Bấm Xóa trắng → Xóa trắng', 'Click', 'After:\n– Xoá toàn bộ nội dung đã nhập, giữ nguyên chế độ đang dùng.'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Tạo mới nhiệm vụ – chế độ nâng cao')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Tạo mới nhiệm vụ – chế độ nâng cao', 'crud', actor=A_ALL)
d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc '
           'chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới nhiệm vụ – chế độ nâng cao',
    mota='Mở rộng cửa sổ Thêm mới để khai thêm Checklist, Nhiệm vụ con, Tệp đính kèm, Người duyệt kết quả, Người '
         'theo dõi, Thẻ (Tags), Lặp lại, Yêu cầu báo cáo tiến độ và Liên kết nhiệm vụ.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở cửa sổ Thêm mới nhiệm vụ.',
    chinh='1. Người dùng bấm “Chế độ nâng cao”.\n'
          '2. Hệ thống mở rộng cửa sổ: cột trái thêm khối Checklist, Nhiệm vụ con, Tệp đính kèm; cột phải có 2 tab '
          '“Thiết lập” và “Liên kết & KPI”.\n'
          '3. Người dùng nhập checklist (gõ rồi Enter), thêm nhiệm vụ con (tên, người làm, hạn, giờ hạn), thêm tài '
          'liệu (tên, loại, chọn tệp).\n'
          '4. Ở tab Thiết lập: chọn Người duyệt kết quả, Người theo dõi, nhập thẻ (Enter), bật “Lặp lại” và/hoặc '
          '“Yêu cầu báo cáo tiến độ?” rồi khai chu kỳ.\n'
          '5. Ở tab Liên kết & KPI: chọn kiểu liên kết (FS/SS/FF/SF/RL) và tìm nhiệm vụ cần liên kết.\n'
          '6. Người dùng bấm “Lưu” — xử lý như FR-05, lưu thêm các phần trên.',
    phu='• “Thêm nhanh” ở Checklist / Nhiệm vụ con → hỏi “Nhập số lượng” (1–50) rồi thêm đủ số dòng trống.\n'
        '• Thêm nhiệm vụ con mà chưa nhập tên → báo “Nhập tên nhiệm vụ con.”.\n'
        '• Chọn tệp sai định dạng → “Định dạng không hợp lệ. Chỉ chấp nhận: jpg, jpeg, png, doc, docx, xls, xlsx, '
        'pdf, ppt, pptx”; tệp quá lớn → “File quá lớn (>20MB)”; tải lên lỗi → “Upload thất bại”.\n'
        '• Bấm “Chuyển về đơn giản” → ẩn các khối nâng cao (dữ liệu đã nhập vẫn giữ).',
    dacbiet='Nhiệm vụ con chỉ được tạo thành nhiệm vụ thật khi nhiệm vụ cha ở trạng thái khác Nháp / Chờ phê duyệt '
            'triển khai; nhiệm vụ con kế thừa giải pháp, dự án, hạng mục, cuộc họp, trạng thái, ưu tiên, người duyệt '
            'của nhiệm vụ cha. Đổi Hạn hoàn thành / Giờ hạn của nhiệm vụ cha thì hạn các nhiệm vụ con trên form đổi '
            'theo.')
d.p('2.6.3 Layout màn hình')
lay(' => Tạo mới => Chế độ nâng cao', '06-nang-cao-1.png', 'Chế độ Nâng cao – phần đầu và tab Thiết lập',
    modal='Thêm mới nhiệm vụ')
d.figure(shot('06-nang-cao-2.png'), 'Khối Checklist, Nhiệm vụ con, Tệp đính kèm', width_in=6.2)
d.figure(shot('06-nang-cao-3.png'), 'Bật Lặp lại và Yêu cầu báo cáo tiến độ', width_in=6.2)
d.figure(shot('06-nang-cao-4.png'), 'Tab Liên kết & KPI', width_in=6.2)
d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Checklist – ô nhập + nút +', 'Textbox', 'Enable', '1–500 ký tự', 'Không', 'Trống',
     'Gợi ý “Nhập mục checklist và Enter”; đếm “n/m hoàn thành”.'),
    ('Checklist – dòng', 'Textbox', 'Enable', '1–500 ký tự', 'Có', 'Theo dữ liệu',
     'Ô tích đã xong, nội dung, nút xoá dòng.'),
    ('Nhiệm vụ con – Tên', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', 'Gợi ý “Tên nhiệm vụ con”.'),
    ('Nhiệm vụ con – Người làm', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống', '–'),
    ('Nhiệm vụ con – Hạn (ngày), Giờ hạn', 'Datepicker', 'Enable', 'dd/mm/yyyy, hh:mm', 'Không',
     'Theo hạn nhiệm vụ cha', 'Không được sau hạn nhiệm vụ cha.'),
    ('Nút Thêm nhanh', 'Button', 'Enable', '1 – 50', '–', 'Hiển thị', 'Mở hộp “Nhập số lượng”.'),
    ('Tệp đính kèm – Tên tài liệu', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo tên tệp', 'Tự điền theo tên tệp.'),
    ('Tệp đính kèm – Loại tài liệu', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống',
     'Danh mục loại tài liệu (Bản vẽ thiết kế, Thuyết minh, Bomlist…).'),
    ('Tệp đính kèm – Chọn tệp', 'Button', 'Enable', 'jpg, jpeg, png, doc, docx, xls, xlsx, pdf, ppt, pptx', 'Có',
     'Trống', 'Có tệp thì hiện tên, dung lượng, nút Tải xuống, Thay đổi, Xóa.'),
    ('Nút Thêm tài liệu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thêm 1 dòng tài liệu.'),
    ('Tab Thiết lập / Liên kết & KPI', 'Tab', 'Enable', '–', '–', 'Thiết lập', '–'),
    ('Người duyệt kết quả', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Người tạo',
     'Chọn giải pháp thì chỉ còn nhân sự của giải pháp (PM, thành viên, leader/thành viên hạng mục).'),
    ('Người theo dõi', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Người tạo', 'Chọn nhiều.'),
    ('Thẻ (Tags)', 'Textbox', 'Enable', '1–100 ký tự/thẻ', 'Không', 'Trống',
     'Gợi ý “Nhập thẻ và Enter”; nút “Xóa” bỏ hết thẻ; thẻ mới tự thêm vào danh mục tag.'),
    ('Lặp lại – Kiểu lặp, Khoảng lặp', 'Dropdown', 'Enable', 'Hàng ngày/tuần/tháng/Tùy chỉnh, ≥ 1', 'Không',
     'Hàng ngày, 1', 'Hàng tuần: chọn thứ T2…CN; Hàng tháng: ngày 1–31; Tùy chỉnh: biểu thức Cron.'),
    ('Lặp lại – Kết thúc', 'Radio', 'Enable', 'Không bao giờ / Đến ngày / Sau n lần', 'Không', 'Không bao giờ',
     'Kèm dòng “Xem trước:” mô tả lịch lặp.'),
    ('Yêu cầu báo cáo tiến độ – Theo chu kỳ, Giờ gửi', 'Dropdown', 'Enable', 'Hàng ngày/tuần/tháng, hh:mm',
     'Không', 'Hàng ngày, 17:00', 'Hàng tuần: chọn thứ báo cáo; Hàng tháng: ngày 1–31; dòng “Xem trước:”.'),
    ('Liên kết nhiệm vụ', 'Dropdown', 'Enable', 'FS / SS / FF / SF / RL', 'Không', 'FS',
     'Ô “Tìm nhiệm vụ...”; dòng giải thích kiểu liên kết; nút “Xóa” bỏ hết liên kết.'),
])
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Chế độ nâng cao / Chuyển về đơn giản', 'Click', 'After:\n– Mở rộng / thu gọn cửa sổ, giữ dữ liệu đã nhập.'),
    ('Enter ở ô checklist / thẻ', 'Keypress', 'After:\n– Thêm 1 dòng checklist / 1 thẻ (thẻ trùng thì bỏ qua).'),
    ('Chọn tệp đính kèm', 'Change',
     'During:\n– Sai định dạng → “Định dạng không hợp lệ. Chỉ chấp nhận: jpg, jpeg, png, doc, docx, xls, xlsx, pdf, '
     'ppt, pptx”.\n– Quá 50MB → “File quá lớn (>20MB)”.\n'
     'After:\n– Tải tệp lên, hiện “Đang tải lên...”; lỗi → “Upload thất bại”.'),
    ('Bấm Lưu', 'Click',
     'During:\n– Kiểm tra như FR-05, thêm: dòng checklist trống, tên / người làm nhiệm vụ con trống, tên / loại / '
     'tệp tài liệu trống → “Bắt buộc phải nhập”.\n'
     '– Hạn nhiệm vụ con sau hạn nhiệm vụ cha → “Hạn hoàn thành của nhiệm vụ con không được sau hạn hoàn thành của '
     'nhiệm vụ cha”.\n– Nếu có lỗi validate → không thực hiện bước After.\n'
     'After:\n– Lưu nhiệm vụ kèm checklist, thẻ, người theo dõi, tài liệu, liên kết, cấu hình lặp lại, cấu hình báo '
     'cáo tiến độ.\n– Trạng thái khác Nháp / Chờ phê duyệt triển khai → tạo các nhiệm vụ con thành nhiệm vụ thật.\n'
     '– Hiển thị “Đã lưu nhiệm vụ thành công”.'),
])

# ------------------------------------------------------------------ 2.7
d.h3('2.7 Chỉnh sửa nhiệm vụ')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Chỉnh sửa nhiệm vụ', 'crud', actor=A_TAO)
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc '
           'chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Chỉnh sửa nhiệm vụ',
    mota='Người tạo sửa thông tin nhiệm vụ và chuyển trạng thái theo vòng đời (BR-04) trên cửa sổ “Chỉnh sửa nhiệm '
         'vụ”.',
    tacnhan='Người tạo nhiệm vụ; Người dùng đã đăng nhập',
    dieukien='Người dùng là người tạo nhiệm vụ và nhiệm vụ chưa có nhiệm vụ con.',
    chinh='1. Người dùng bấm nút Sửa (bút chì) trên dòng.\n'
          '2. Hệ thống mở cửa sổ “<Mã> — Chỉnh sửa nhiệm vụ” với dữ liệu hiện tại (chế độ đã lưu của nhiệm vụ).\n'
          '3. Người dùng sửa thông tin; ô Trạng thái chỉ liệt kê trạng thái hiện tại và các trạng thái được phép '
          'chuyển.\n'
          '4. Người dùng bấm “Lưu”.\n'
          '5. Hệ thống kiểm tra, cập nhật, báo “Đã cập nhật nhiệm vụ thành công”, đóng cửa sổ, nạp lại danh sách.',
    phu='• Loại nhiệm vụ không đổi được sau khi tạo.\n'
        '• Chọn trạng thái không được phép → “Không thể chuyển từ trạng thái hiện tại sang trạng thái mới này.”.\n'
        '• Chọn “Từ chối triển khai” khi nhiệm vụ đã có kết quả → “Không thể từ chối triển khai vì nhiệm vụ đã có '
        'kết quả.”.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới ô, “Lỗi khi lưu nhiệm vụ”.\n'
        '• Mở bằng nút Nhập kết quả / Duyệt trên nhiệm vụ Chờ bắt đầu / Chờ phê duyệt triển khai → cùng cửa sổ này, '
        'người không phải người tạo chỉ đổi được Trạng thái (xem FR-10, FR-11).',
    dacbiet='Chỉ chặn hạn hoàn thành ở quá khứ khi nhiệm vụ đang Nháp; nhiệm vụ đã qua Nháp được giữ hạn cũ.')
d.p('2.7.3 Layout màn hình')
lay(' => Sửa', '07-sua.png', 'Cửa sổ Chỉnh sửa nhiệm vụ', modal='Chỉnh sửa nhiệm vụ')
d.figure(shot('07b-sua-trang-thai.png'), 'Ô Trạng thái của nhiệm vụ Nháp – người tạo được chuyển sang 3 trạng thái',
         width_in=6.2)
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '<Mã> — Chỉnh sửa nhiệm vụ', 'Kèm nhãn trạng thái hiện tại.'),
    ('Loại nhiệm vụ', 'Dropdown', 'Disable', '–', 'Có', 'Theo dữ liệu', 'Không đổi được.'),
    ('Các ô thông tin (như FR-05, FR-06)', 'Textbox / Dropdown', 'Enable / Disable', 'Như FR-05', 'Như FR-05',
     'Theo dữ liệu', 'Khoá hết nếu người dùng không phải người tạo.'),
    ('Trạng thái', 'Dropdown', 'Enable / Ẩn', 'Theo BR-04', 'Có', 'Trạng thái hiện tại',
     'Chỉ hiện khi có trạng thái được chuyển và người dùng có quyền sửa / nhập kết quả / duyệt.'),
    ('Nút Xóa trắng', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không phải người tạo', '–'),
    ('Khối Lịch sử', 'Label', 'Hiển thị', '–', '–', 'Thu gọn', 'Xem FR-15.'),
    ('Nút Lưu', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiện khi người dùng là người tạo và nhiệm vụ chưa có nhiệm vụ con.\n' + NO_PERM + '\n'
     'After:\n– Mở cửa sổ, nạp chi tiết nhiệm vụ; lỗi → “Lỗi khi tải chi tiết nhiệm vụ”.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Trạng thái mới không thuộc danh sách được phép → “Không thể chuyển từ trạng thái hiện tại sang '
     'trạng thái mới này.” và dừng.\n'
     '– Chuyển “Từ chối triển khai” khi đã có kết quả (trừ từ Chờ phê duyệt triển khai) → “Không thể từ chối triển '
     'khai vì nhiệm vụ đã có kết quả.” và dừng.\n'
     'During:\n– Tên công việc trống → “Bắt buộc phải nhập”; Mức độ ưu tiên trống → “Bắt buộc phải nhập”.\n'
     '– Nhiệm vụ đang Nháp: hạn trước hôm nay → “Hạn hoàn thành không được là ngày trong quá khứ.”; giờ hạn đã qua → '
     '“Giờ hạn hoàn thành phải lớn hơn hoặc bằng thời điểm hiện tại.”\n'
     '– Hạn nhiệm vụ con sau hạn nhiệm vụ cha → “Hạn hoàn thành của nhiệm vụ con không được sau hạn hoàn thành của '
     'nhiệm vụ cha.”\n– Nếu có lỗi validate → “Lỗi khi lưu nhiệm vụ”, không thực hiện bước After.\n'
     'After:\n– Cập nhật nhiệm vụ và dữ liệu đi kèm.\n'
     '– Đổi trạng thái → ghi lịch sử “Thay đổi trạng thái”, gửi thông báo theo BR-05; không đổi → ghi lịch sử “Cập '
     'nhật thông tin” (giá trị cũ → mới).\n'
     '– Rời Nháp / Chờ phê duyệt triển khai → tạo các nhiệm vụ con chưa tạo; tính lại tiến độ hạng mục / giải pháp.\n'
     '– Hiển thị “Đã cập nhật nhiệm vụ thành công”.'),
])

# ------------------------------------------------------------------ 2.8
d.h3('2.8 Xem chi tiết nhiệm vụ')
d.p('2.8.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Nhiệm vụ tại phần mô tả chi '
           'tiết.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết nhiệm vụ',
    mota='Bấm mã nhiệm vụ để xem toàn bộ thông tin ở chế độ chỉ đọc. Nhiệm vụ đã bắt đầu thực hiện mở cửa sổ “Xem '
         'kết quả nhiệm vụ”.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Nhiệm vụ nằm trong danh sách người dùng được xem.',
    chinh='1. Người dùng bấm mã nhiệm vụ ở cột Mã nhiệm vụ.\n'
          '2. Nhiệm vụ ở Nháp / Chờ phê duyệt triển khai / Chờ bắt đầu / Từ chối triển khai → hệ thống mở cửa sổ '
          '“<Mã> — Chi tiết nhiệm vụ” ở chế độ Nâng cao, mọi ô khoá.\n'
          '3. Nhiệm vụ ở Đang thực hiện / Tạm dừng / Hoàn thành - Chờ duyệt / Từ chối kết quả / Hoàn thành / Huỷ → '
          'mở cửa sổ “Xem kết quả nhiệm vụ” chỉ đọc.\n'
          '4. Người dùng xem thông tin, checklist, nhiệm vụ con, tệp, bình luận, lịch sử; bấm “Đóng”.',
    phu='• Bấm tên một nhiệm vụ con → mở chi tiết nhiệm vụ con đó.\n'
        '• Bấm Tải xuống ở tệp → mở tệp trên tab mới.\n'
        '• Người tạo xem nhiệm vụ Nháp → chân cửa sổ có nút “Xóa” (FR-09).')
d.p('2.8.2 Layout màn hình')
lay(' => Mã nhiệm vụ', '08-xem.png', 'Cửa sổ Chi tiết nhiệm vụ (nhiệm vụ Nháp)', modal='Chi tiết nhiệm vụ')
d.figure(shot('08b-xem-cuoi.png'), 'Phần dưới: nhiệm vụ con, tệp đính kèm, bình luận, lịch sử', width_in=6.2)
d.figure(shot('08c-xem-ket-qua.png'), 'Cửa sổ Xem kết quả nhiệm vụ (nhiệm vụ Đang thực hiện)', width_in=6.2)
d.p('2.8.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '<Mã> — Chi tiết nhiệm vụ / Xem kết quả nhiệm vụ',
     'Kèm nhãn trạng thái.'),
    ('Các ô thông tin nhiệm vụ', 'Textbox / Dropdown', 'Read-only', '–', 'Theo dữ liệu',
     'Như FR-05, FR-06 (Loại, Tên, Giải pháp, Dự án, Hạng mục, Meeting, Người thực hiện, Ưu tiên, Hạn, Giờ hạn, Mô '
     'tả, Số giờ được giao).'),
    ('Khối Checklist / Nhiệm vụ con / Tệp đính kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Nhiệm vụ con đã tạo hiện Tên + mã, Người làm, Hạn, Trạng thái.'),
    ('Tab Thiết lập / Liên kết & KPI', 'Tab', 'Read-only', '–', 'Thiết lập',
     'Người duyệt kết quả, Người theo dõi, Thẻ, Lặp lại, Báo cáo tiến độ; liên kết nhiệm vụ.'),
    ('Khối Kết quả thực hiện (cửa sổ Xem kết quả)', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Số giờ được giao, số giờ thực tế, tiến độ, kết quả hoặc nhật ký tiến độ, tệp kết quả; thông tin nhanh Người '
     'giao, Giờ giao.'),
    ('Khối Bình luận', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu', 'Xem FR-13.'),
    ('Khối Lịch sử', 'Label', 'Hiển thị', '–', 'Thu gọn', 'Xem FR-15.'),
    ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Chỉ hiện khi người dùng xóa được nhiệm vụ.'),
    ('Nút Đóng / dấu ×', 'Button', 'Enable', '–', 'Hiển thị', '–'),
], required=False)
d.p('2.8.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm mã nhiệm vụ', 'Click',
     'After:\n– Chọn cửa sổ theo trạng thái nhiệm vụ, nạp chi tiết.\n– Lỗi → “Lỗi khi tải chi tiết nhiệm vụ”.'),
    ('Bấm tên nhiệm vụ con', 'Click', 'After:\n– Mở chi tiết nhiệm vụ con trong cùng cửa sổ.'),
    ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ, giữ nguyên danh sách.'),
])

# ------------------------------------------------------------------ 2.9
d.h3('2.9 Xóa nhiệm vụ')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Xóa nhiệm vụ', 'action', actor=A_TAO)
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc Xóa và Thông báo.', anchor='delete')
d.intro_table(
    ten='Xóa nhiệm vụ',
    mota='Người tạo xóa nhiệm vụ còn ở trạng thái Nháp.',
    tacnhan='Người tạo nhiệm vụ; Người dùng đã đăng nhập',
    dieukien='Người dùng là người tạo, nhiệm vụ ở trạng thái Nháp và chưa có nhiệm vụ con.',
    chinh='1. Người dùng bấm nút Xóa (thùng rác) trên dòng, hoặc nút “Xóa” ở cửa sổ Chi tiết nhiệm vụ.\n'
          '2. Hệ thống hiện hộp “Xác nhận xóa”: “Bạn có chắc muốn xóa công việc ‘<Tên>’?”.\n'
          '3. Người dùng bấm “Xóa”.\n'
          '4. Hệ thống xóa nhiệm vụ, tính lại tiến độ hạng mục / giải pháp, báo “Xóa công việc thành công” và nạp lại '
          'danh sách.',
    phu='• Bấm “Hủy” → đóng hộp, không xóa.\n'
        '• Nhiệm vụ đã đổi trạng thái hoặc đã có nhiệm vụ con trong lúc đang mở → máy chủ từ chối (“Dữ liệu đã thay '
        'đổi, vui lòng tải lại”), hiện thông báo lỗi.',
    dacbiet='Không có hộp nhập lý do; xóa là xóa khỏi danh sách.')
d.p('2.9.3 Layout màn hình')
lay(' => Xóa', '09-xoa.png', 'Hộp xác nhận xóa nhiệm vụ')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Xác nhận xóa', 'Biểu tượng cảnh báo đỏ.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dòng', '“Bạn có chắc muốn xóa công việc ‘<Tên>’?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Màu đỏ, xác nhận xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không xóa.'),
], required=False, scope=False)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa', 'Click',
     'Before:\n– Nút chỉ hiện với người tạo, nhiệm vụ Nháp, chưa có nhiệm vụ con.\n' + NO_PERM + '\n'
     'After:\n– Mở hộp Xác nhận xóa.'),
    ('Bấm Xóa trong hộp', 'Click',
     'Before:\n– Kiểm tra lại điều kiện xóa; không thỏa → “Dữ liệu đã thay đổi, vui lòng tải lại”, dừng xử lý.\n'
     'After:\n– Xóa nhiệm vụ; tính lại tiến độ hạng mục / giải pháp.\n'
     '– Hiển thị “Xóa công việc thành công”, nạp lại danh sách (đóng cửa sổ chi tiết nếu xóa từ đó).\n'
     '– Lỗi → hiển thị thông báo lỗi (mặc định “Lỗi khi xóa công việc”).'),
    ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp, giữ nguyên dữ liệu.'),
])

# ------------------------------------------------------------------ 2.10
d.h3('2.10 Duyệt triển khai')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Duyệt triển khai', 'action', actor=A_DTK)
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='history')
d.intro_table(
    ten='Duyệt / từ chối triển khai nhiệm vụ',
    mota='Người duyệt triển khai quyết định cho nhiệm vụ “Chờ phê duyệt triển khai” được làm (Chờ bắt đầu) hoặc '
         'không (Từ chối triển khai).',
    tacnhan='Người duyệt triển khai; Người dùng đã đăng nhập',
    dieukien='Người dùng có quyền Q1, nhiệm vụ ở Chờ phê duyệt triển khai, người thực hiện thuộc phòng ban người '
             'dùng quản lý (hoặc phòng ban của chính mình).',
    chinh='1. Người dùng bấm nút Duyệt (dấu tích) trên dòng.\n'
          '2. Hệ thống mở cửa sổ Chỉnh sửa nhiệm vụ; ô Trạng thái gồm Chờ phê duyệt triển khai, Chờ bắt đầu, Từ chối '
          'triển khai.\n'
          '3. Người dùng chọn “Chờ bắt đầu” (duyệt) hoặc “Từ chối triển khai”.\n'
          '4. Người dùng bấm “Lưu”.\n'
          '5. Hệ thống cập nhật trạng thái, gửi thông báo, báo “Đã cập nhật nhiệm vụ thành công”.',
    phu='• Duyệt (Chờ bắt đầu) → tạo các nhiệm vụ con; thông báo người thực hiện “Bạn có nhiệm vụ <Tên> chờ bắt đầu '
        'thực hiện”.\n'
        '• Từ chối → thông báo người tạo “Nhiệm vụ <Tên> không được <Người duyệt> phê duyệt triển khai”; người tạo '
        'có thể sửa rồi gửi duyệt lại.',
    dacbiet='Người duyệt triển khai không phải người tạo thì các ô thông tin khác bị khoá, chỉ đổi Trạng thái.')
d.p('2.10.3 Layout màn hình')
lay(' => Duyệt', '10b-duyet-trien-khai-tt.png', 'Duyệt triển khai – ô Trạng thái', modal='Chỉnh sửa nhiệm vụ')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nhãn trạng thái ở tiêu đề', 'Badge', 'Hiển thị', '–', '–', 'Chờ phê duyệt triển khai', '–'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Có', 'Chờ phê duyệt triển khai',
     'Chờ phê duyệt triển khai / Chờ bắt đầu / Từ chối triển khai.'),
    ('Các ô thông tin nhiệm vụ', 'Textbox / Dropdown', 'Disable', '–', '–', 'Theo dữ liệu',
     'Mở được nếu người duyệt cũng là người tạo.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Duyệt', 'Click',
     'Before:\n– Nút chỉ hiện khi đủ điều kiện ban đầu.\n' + NO_PERM + '\nAfter:\n– Mở cửa sổ, nạp trạng thái được '
     'phép.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Trạng thái không được phép → “Không thể chuyển từ trạng thái hiện tại sang trạng thái mới này.”\n'
     'After:\n– Cập nhật trạng thái; ghi lịch sử “Thay đổi trạng thái”.\n'
     '– Chờ bắt đầu: tạo nhiệm vụ con, thông báo người thực hiện; Từ chối triển khai: thông báo người tạo.\n'
     '– Hiển thị “Đã cập nhật nhiệm vụ thành công”.'),
])

# ------------------------------------------------------------------ 2.11
d.h3('2.11 Nhập kết quả')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Nhập kết quả nhiệm vụ', 'crud', actor=A_TH)
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc '
           'ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Nhập kết quả / cập nhật tiến độ nhiệm vụ',
    mota='Người thực hiện cập nhật số giờ làm, tiến độ, kết quả, đánh dấu checklist đã xong, đính kèm tệp kết quả và '
         'chuyển trạng thái (Đang thực hiện, Tạm dừng, Hoàn thành - Chờ duyệt / Hoàn thành, Từ chối triển khai).',
    tacnhan='Người thực hiện; Người dùng đã đăng nhập',
    dieukien='Người dùng là người thực hiện; nhiệm vụ ở Chờ bắt đầu, Đang thực hiện hoặc Từ chối kết quả.',
    chinh='1. Người dùng bấm nút Nhập kết quả trên dòng.\n'
          '2. Nhiệm vụ Chờ bắt đầu → mở cửa sổ Chỉnh sửa nhiệm vụ để chuyển sang “Đang thực hiện”.\n'
          '3. Nhiệm vụ Đang thực hiện / Từ chối kết quả → mở cửa sổ “Nhập kết quả nhiệm vụ”.\n'
          '4. Không bật báo cáo tiến độ: nhập Số giờ làm thực tế, Tiến độ (%), Kết quả thực hiện. Có bật: nhập Số giờ '
          'làm, Tiến độ (%), Ghi chú cho từng ngày báo cáo đã tới, và Kết quả thực hiện (tổng hợp).\n'
          '5. Đánh dấu checklist đã xong, thêm tệp ở tab “File kết quả thực hiện”, chọn Trạng thái.\n'
          '6. Bấm “Lưu” → hệ thống lưu, báo “Đã lưu kết quả thành công”, đóng cửa sổ.',
    phu='• Chọn Hoàn thành - Chờ duyệt / Hoàn thành → Tiến độ tự đặt 100% và khoá; hiện ô Hiệu suất.\n'
        '• Nhiệm vụ không có người duyệt kết quả → được chuyển thẳng “Hoàn thành” thay cho “Hoàn thành - Chờ duyệt”.\n'
        '• Dòng nhật ký có ngày sau hôm nay bị mờ và khoá.\n'
        '• Lỗi kiểm tra → báo lỗi đỏ dưới ô, “Lỗi khi lưu kết quả”.',
    dacbiet='Tiến độ hoàn thành khi bật báo cáo tiến độ lấy theo dòng nhật ký mới nhất có nhập tiến độ; số giờ thực tế '
            'là tổng giờ các dòng nhật ký. Hệ thống nhắc báo cáo tiến độ (4 mốc 08:30, 11:30, 14:30, 17:30) cho nhiệm '
            'vụ Đang thực hiện chưa có báo cáo hôm nay.')
d.p('2.11.3 Layout màn hình')
lay(' => Nhập kết quả', '11-nhap-kq.png', 'Cửa sổ Nhập kết quả nhiệm vụ (không bật báo cáo tiến độ)',
    modal='Nhập kết quả nhiệm vụ')
d.figure(shot('11b-nhap-kq-tt.png'), 'Trạng thái người thực hiện được chuyển từ Đang thực hiện', width_in=6.2)
d.figure(shot('11c-nhap-kq-checklist.png'), 'Checklist, nhiệm vụ con, tệp đính kèm trong cửa sổ Nhập kết quả',
         width_in=6.2)
d.figure(shot('11d-nhat-ky.png'), 'Nhật ký tiến độ theo ngày (nhiệm vụ bật báo cáo tiến độ)', width_in=6.2)
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Nhập kết quả nhiệm vụ', 'Kèm nhãn trạng thái.'),
    ('Tên, Ưu tiên, Dự án, Hạng mục, Người thực hiện, Hạn, Giờ hạn, Mô tả', 'Textbox', 'Read-only', '–', '–',
     'Theo dữ liệu', 'Mô tả thu gọn / mở được.'),
    ('Trạng thái', 'Dropdown', 'Enable / Ẩn', 'Theo BR-04', 'Có', 'Trạng thái hiện tại',
     'Ẩn khi không có trạng thái được chuyển.'),
    ('Số giờ được giao', 'Number', 'Read-only', '–', '–', 'Theo dữ liệu', '–'),
    ('Số giờ làm thực tế', 'Number', 'Enable', '≥ 0, bước 0,5', 'Có', 'Theo dữ liệu', 'Gợi ý “VD: 6.5”.'),
    ('Tiến độ (%)', 'Number', 'Enable / Disable', '0 – 100', 'Có', 'Theo dữ liệu',
     'Khoá và = 100 khi chọn Hoàn thành - Chờ duyệt / Hoàn thành.'),
    ('Hiệu suất', 'Text', 'Read-only', '–', '–', 'Ẩn', 'Hiện khi chọn Hoàn thành - Chờ duyệt / Hoàn thành.'),
    ('Kết quả thực hiện', 'Textarea', 'Enable', '–', 'Có', 'Theo dữ liệu', 'Gợi ý “Nhập kết quả thực hiện…”.'),
    ('Bảng nhật ký tiến độ (khi bật báo cáo)', 'Table/Grid', 'Enable / Disable', '–', '–', 'Theo lịch báo cáo',
     'Tiêu đề “Nhật ký tiến độ theo ngày/tuần/tháng”; cột Ngày báo cáo, Số giờ làm, Tiến độ (%), Ghi chú; dòng '
     '“Tổng giờ”, “Tiến độ hiện tại (max)”; rỗng: “Chưa có nhật ký”.'),
    ('Tiến độ hoàn thành (%) (khi bật báo cáo)', 'Number', 'Read-only', '0 – 100', 'Có', 'Theo nhật ký', '–'),
    ('Checklist', 'Table/Grid', 'Enable', '–', 'Không', 'Theo dữ liệu',
     'Cột Done (ô tích), Nội dung; rỗng: “Không có checklist”.'),
    ('Nhiệm vụ con', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', 'Rỗng: “Không có nhiệm vụ con”.'),
    ('Tab File đính kèm giao nhiệm vụ', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'STT, Tên file, Tải xuống; rỗng: “Không có tệp đính kèm”.'),
    ('Tab File kết quả thực hiện', 'Table/Grid', 'Enable', 'jpg, jpeg, png, doc, docx, xls, xlsx, pdf', 'Không',
     'Theo dữ liệu', 'Nút “Thêm dòng”, Tên file (bắt buộc), Chọn tệp, Tải xuống, Xóa; rỗng: “Chưa có tệp kết quả”.'),
    ('Panel Thiết lập / Liên kết & KPI', 'Tab', 'Read-only', '–', '–', 'Thiết lập',
     'Thông tin nhanh (Giờ giao, Người giao, Người theo dõi, Người duyệt kết quả, Thẻ), Lặp lại, Yêu cầu báo cáo '
     'tiến độ; Liên kết nhiệm vụ, Gắn KPI đánh giá.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Nhập kết quả', 'Click',
     'Before:\n– Nút chỉ hiện với người thực hiện, nhiệm vụ Chờ bắt đầu / Đang thực hiện / Từ chối kết quả.\n'
     + NO_PERM + '\nAfter:\n– Mở cửa sổ theo trạng thái, nạp chi tiết; bật báo cáo thì sinh sẵn các dòng nhật ký theo '
     'lịch từ ngày bắt đầu tới hạn hoàn thành.'),
    ('Chọn Trạng thái Hoàn thành - Chờ duyệt / Hoàn thành', 'Change',
     'After:\n– Không bật báo cáo: đặt Tiến độ = 100 và khoá; hiện Hiệu suất.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Trạng thái không được phép → “Không thể chuyển từ trạng thái hiện tại sang trạng thái mới này.”\n'
     '– Từ chối triển khai khi đã có kết quả → “Không thể từ chối triển khai vì nhiệm vụ đã có kết quả.”\n'
     'During:\n– Chuyển Hoàn thành - Chờ duyệt / Hoàn thành mà tiến độ khác 100 → “Tiến độ hoàn thành phải đạt 100% mới '
     'được chuyển sang trạng thái hoàn thành.”\n'
     '– Tiến độ ngoài 0–100 → “Không được nhỏ hơn 0.” / “Không được lớn hơn 100.”\n'
     '– Tiến độ dòng nhật ký nhỏ hơn kỳ trước → “Tiến độ không được nhỏ hơn kỳ trước (n%)”.\n'
     '– Tên file kết quả hoặc tệp còn trống → “Bắt buộc phải nhập”.\n'
     '– Nếu có lỗi validate → “Lỗi khi lưu kết quả”, không thực hiện bước After.\n'
     'After:\n– Lưu số giờ, tiến độ, kết quả, nhật ký, checklist, tệp kết quả.\n'
     '– Sang Hoàn thành - Chờ duyệt: ghi thời điểm gửi duyệt, tính Hiệu suất, thông báo người duyệt kết quả.\n'
     '– Ghi lịch sử; tính lại tiến độ hạng mục / giải pháp.\n– Hiển thị “Đã lưu kết quả thành công”.'),
])

# ------------------------------------------------------------------ 2.12
d.h3('2.12 Duyệt kết quả')
d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Duyệt kết quả nhiệm vụ', 'action', actor=A_DKQ)
d.p('2.12.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='history')
d.intro_table(
    ten='Duyệt / từ chối kết quả nhiệm vụ',
    mota='Người duyệt kết quả xem kết quả người thực hiện đã nhập rồi chuyển nhiệm vụ sang Hoàn thành hoặc Từ chối '
         'kết quả.',
    tacnhan='Người duyệt kết quả; Người dùng đã đăng nhập',
    dieukien='Người dùng là người duyệt kết quả và nhiệm vụ ở Hoàn thành - Chờ duyệt.',
    chinh='1. Người dùng bấm nút Duyệt (dấu tích) trên dòng.\n'
          '2. Hệ thống mở cửa sổ Nhập kết quả nhiệm vụ với kết quả đã nhập; ô Trạng thái gồm Hoàn thành - Chờ duyệt, '
          'Từ chối kết quả, Hoàn thành.\n'
          '3. Người dùng chọn “Hoàn thành” hoặc “Từ chối kết quả”, bấm “Lưu”.\n'
          '4. Hệ thống cập nhật trạng thái, gửi thông báo người thực hiện, báo “Đã lưu kết quả thành công”.',
    phu='• Hoàn thành → ghi người duyệt, thời điểm duyệt, thời điểm hoàn thành; thông báo “Nhiệm vụ <Tên> đã được '
        '<Người duyệt> duyệt kết quả”.\n'
        '• Từ chối kết quả → thông báo “Nhiệm vụ <Tên> không được <Người duyệt> duyệt kết quả”; người thực hiện nhập '
        'lại kết quả.\n'
        '• Người tạo được đưa nhiệm vụ đã Hoàn thành về “Từ chối kết quả” (mở lại).')
d.p('2.12.3 Layout màn hình')
lay(' => Duyệt', '12-duyet-kq.png', 'Cửa sổ duyệt kết quả (nhiệm vụ Hoàn thành - Chờ duyệt)',
    modal='Nhập kết quả nhiệm vụ')
d.figure(shot('12b-duyet-kq-tt.png'), 'Ô Trạng thái của người duyệt kết quả', width_in=6.2)
d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Có', 'Hoàn thành - Chờ duyệt',
     'Hoàn thành - Chờ duyệt / Từ chối kết quả / Hoàn thành.'),
    ('Khối Kết quả thực hiện', 'Textbox', 'Enable', 'Như FR-11', 'Như FR-11', 'Theo dữ liệu',
     'Hiển thị số giờ thực tế, tiến độ 100%, Hiệu suất, kết quả đã nhập.'),
    ('Checklist / Nhiệm vụ con / Tệp', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu', 'Như FR-11.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Duyệt', 'Click',
     'Before:\n– Nút chỉ hiện với người duyệt kết quả của nhiệm vụ Hoàn thành - Chờ duyệt.\n' + NO_PERM + '\n'
     'After:\n– Mở cửa sổ, nạp kết quả.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Trạng thái không được phép → “Không thể chuyển từ trạng thái hiện tại sang trạng thái mới này.”\n'
     'During:\n– Chọn Hoàn thành mà tiến độ khác 100 → “Tiến độ hoàn thành phải đạt 100% mới được chuyển sang trạng '
     'thái hoàn thành.”\n'
     'After:\n– Hoàn thành: ghi người duyệt, thời điểm duyệt / hoàn thành, tính Hiệu suất.\n'
     '– Ghi lịch sử “Thay đổi trạng thái”; gửi thông báo người thực hiện (BR-05).\n'
     '– Hiển thị “Đã lưu kết quả thành công”.'),
])

# ------------------------------------------------------------------ 2.13
d.h3('2.13 Bình luận')
d.p('2.13.1 Biểu đồ Usecase')
d.uc_figure('FR-13', 'Bình luận nhiệm vụ', 'crud', actor=A_ALL)
d.p('2.13.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX.', anchor='notice')
d.intro_table(
    ten='Bình luận nhiệm vụ',
    mota='Trao đổi trên từng nhiệm vụ: viết bình luận, trả lời (tối đa 3 cấp), nhắc tên (@), đính kèm tệp, thả cảm '
         'xúc, sửa / xóa bình luận của mình.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đang xem nhiệm vụ (cửa sổ Chi tiết / Chỉnh sửa ở chế độ Nâng cao, hoặc cửa sổ Nhập / Xem '
             'kết quả).',
    chinh='1. Người dùng gõ nội dung vào ô “Viết bình luận…” (gõ @ để chọn nhân viên cần nhắc tên).\n'
          '2. Bấm “Đính kèm” nếu cần gửi tệp.\n'
          '3. Bấm “Gửi”.\n'
          '4. Hệ thống lưu bình luận, hiển thị trong danh sách, gửi thông báo cho người liên quan.',
    phu='• Bấm “Trả lời” dưới một bình luận → ô trả lời “Trả lời <Tên>…”; trả lời ở cấp 3 thì gắn vào cấp 3.\n'
        '• Bình luận của mình có “Sửa” (Lưu / Hủy) và “Xóa” (hỏi “Bạn có chắc muốn xóa bình luận này?”).\n'
        '• Gửi lỗi → “Gửi bình luận thất bại. Thử lại sau.”; sửa lỗi → “Lưu thất bại, vui lòng thử lại.”; xóa lỗi '
        '→ “Xóa thất bại, vui lòng thử lại.”\n'
        '• Chưa có bình luận → “Chưa có bình luận nào.”')
d.p('2.13.3 Layout màn hình')
lay(' => Mã nhiệm vụ => Bình luận', '13-binh-luan.png', 'Khối Bình luận trong cửa sổ nhiệm vụ',
    modal='Chi tiết nhiệm vụ / Xem kết quả nhiệm vụ')
d.p('2.13.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề khối', 'Label', 'Hiển thị', '–', '–', 'Bình luận', 'Kèm tổng số bình luận (cả trả lời).'),
    ('Danh sách bình luận', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Ảnh đại diện, tên, thời gian, nội dung, tệp kèm, cảm xúc; trả lời thụt lề, thu gọn/mở được.'),
    ('Ô Viết bình luận', 'Textarea', 'Enable', '1–5000 ký tự', 'Có', 'Trống',
     'Gõ @ để hiện danh sách nhân viên (“Nhân viên — nhấn ↑↓ để chọn, Enter để chèn”).'),
    ('Nút Đính kèm', 'Button', 'Enable', 'Mỗi tệp ≤ 50MB', 'Không', 'Hiển thị', 'Chọn nhiều tệp.'),
    ('Nút Xoá / Gửi', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá: xoá nội dung đang soạn.'),
    ('Nút Trả lời / Sửa / Xóa / Thả cảm xúc', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
     'Sửa, Xóa chỉ hiện ở bình luận của chính mình.'),
])
d.p('2.13.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Gửi', 'Click',
     'During:\n– Nội dung trống → không gửi; quá 5000 ký tự / tệp quá 50MB → máy chủ từ chối, “Gửi bình luận thất '
     'bại. Thử lại sau.”\n'
     'After:\n– Lưu bình luận (và tệp).\n'
     '– Bình luận gốc → thông báo người tạo, người thực hiện, người duyệt kết quả, người theo dõi (trừ người viết): '
     '“<Người viết> đã bình luận về nhiệm vụ <Tên>”.\n'
     '– Trả lời → thông báo tác giả bình luận được trả lời; người được nhắc tên (@) cũng nhận thông báo.'),
    ('Bấm Sửa → Lưu', 'Click',
     'Before:\n– Không phải bình luận của mình → “Bạn không có quyền sửa comment này”.\nAfter:\n– Cập nhật nội dung.'),
    ('Bấm Xóa → Xóa', 'Click',
     'Before:\n– Không phải bình luận của mình → “Bạn không có quyền xoá comment này”.\nAfter:\n– Xóa bình luận.'),
    ('Thả cảm xúc', 'Click', 'After:\n– Ghi cảm xúc, thông báo tác giả bình luận.'),
])

# ------------------------------------------------------------------ 2.14
d.h3('2.14 Xuất Excel')
d.p('2.14.1 Biểu đồ Usecase')
d.uc_figure('FR-14', 'Xuất Excel danh sách nhiệm vụ', 'io', actor=A_ALL)
d.p('2.14.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách nhiệm vụ',
    mota='Xuất toàn bộ nhiệm vụ khớp bộ lọc đang áp dụng (không phân trang) ra file Excel với các trường người dùng '
         'chọn.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách nhiệm vụ.',
    chinh='1. Người dùng bấm “Xuất Excel”.\n'
          '2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn các trường ứng với cột đang hiện trên bảng.\n'
          '3. Người dùng tích / bỏ tích, kéo ≡ để đổi thứ tự cột trong file.\n'
          '4. Người dùng bấm “Xuất file”.\n'
          '5. Hệ thống tải về file danh_sach_task.xlsx và báo “Xuất Excel thành công”.',
    phu='• “Chọn tất cả” / “Bỏ chọn hết” → tích / bỏ tích mọi trường; không chọn trường nào thì nút Xuất file bị khoá.\n'
        '• Xuất lỗi → “Lỗi khi xuất Excel”.',
    dacbiet='Áp đúng bộ lọc, lọc nhanh, sắp xếp và phạm vi dữ liệu như danh sách.')
d.p('2.14.3 Layout màn hình')
lay(' => Xuất Excel', '14-xuat.png', 'Cửa sổ Chọn trường xuất file', modal='Chọn trường xuất file')
d.p('2.14.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất file', '–'),
    ('Danh sách trường', 'Checkbox', 'Enable', 'Danh sách 27 giá trị', 'Có (≥ 1)', 'Theo cột đang hiện',
     'Mã nhiệm vụ, Tên nhiệm vụ, Tag, Mã giải pháp, Tên giải pháp, Version giải pháp, Mã dự án, Tên dự án, PM dự '
     'án, Hạng mục/Module, Trạng thái, Mức độ ưu tiên, Người làm, Người theo dõi, Người duyệt, Ngày bắt đầu, Hạn '
     'hoàn thành, Giờ hạn, Ước lượng (ngày), Tình trạng hạn, Số checklist, Số nhiệm vụ con, Số nhiệm vụ liên kết, '
     'Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Dòng đếm', 'Label', 'Hiển thị', '–', '–', 'Theo lựa chọn', '“Đang chọn n/27 trường”.'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khoá khi chưa chọn trường / đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.14.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ, tích sẵn trường theo cột đang hiện.'),
    ('Bấm Xuất file', 'Click',
     'During:\n' + SCOPE + '\n– Áp bộ lọc + sắp xếp hiện tại, lấy tất cả dòng; trường lạ bị bỏ qua.\n'
     'After:\n– Tải file Excel tiêu đề “Danh sách task”, cột STT + các trường đã chọn theo thứ tự.\n'
     '– Hiển thị “Xuất Excel thành công”; lỗi → “Lỗi khi xuất Excel”.'),
])

# ------------------------------------------------------------------ 2.15
d.h3('2.15 Xem lịch sử chỉnh sửa')
d.p('2.15.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử.', anchor='history')
d.intro_table(
    ten='Xem lịch sử chỉnh sửa nhiệm vụ',
    mota='Xem dòng thời gian các thao tác trên nhiệm vụ: tạo mới, cập nhật thông tin (giá trị cũ → mới), thay đổi '
         'trạng thái.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Nhiệm vụ nằm trong danh sách người dùng được xem.',
    chinh='1. Người dùng bấm nút Lịch sử (đồng hồ) trên dòng.\n'
          '2. Hệ thống mở cửa sổ “Lịch sử chỉnh sửa <Mã>”, liệt kê thao tác mới nhất trước.\n'
          '3. Mỗi mục có thời gian, loại thao tác, người thao tác và chi tiết thay đổi.\n'
          '4. Người dùng bấm “Đóng”.',
    phu='• Chưa có lịch sử → “Chưa có lịch sử thao tác nào.”\n'
        '• Lỗi → “Lỗi khi tải lịch sử”.\n'
        '• Trong cửa sổ Chi tiết / Chỉnh sửa, khối “Lịch sử” (bấm “Xem lịch sử”) cho xem cùng thông tin, có “Bộ '
        'lọc” theo loại hành động, “Làm mới”, “Thu gọn”.')
d.p('2.15.2 Layout màn hình')
lay(' => Lịch sử', '15-lich-su.png', 'Cửa sổ Lịch sử chỉnh sửa', modal='Lịch sử chỉnh sửa')
d.p('2.15.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Lịch sử chỉnh sửa <Mã>', '–'),
    ('Mục lịch sử', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Chấm màu (xanh lá: Tạo mới nhiệm vụ · vàng: Cập nhật thông tin · xanh dương: Thay đổi trạng thái), thời gian, '
     '“— <Người thao tác>”.'),
    ('Chi tiết thay đổi', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     '“<Trường>: cũ → mới”; trường dạng danh sách (Người theo dõi, Tệp, Nhiệm vụ con, Checklist, Tags) hiện dòng '
     '“−” bị bỏ, “+” được thêm.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thao tác nào.”'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '–'),
], required=False)
d.p('2.15.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Lịch sử', 'Click',
     'Before:\n– Ai xem được nhiệm vụ thì xem được lịch sử, không kiểm tra quyền riêng.\n'
     'After:\n– Mở cửa sổ, nạp lịch sử; lỗi → “Lỗi khi tải lịch sử”.'),
    ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ========================================================= PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.p('Quy tắc áp dụng: chỉ ghi các quy tắc đặc thù của màn Nhiệm vụ; quy tắc chung xem SRS Các quy tắc chung.')
d.rule_table([
    ('BR-01', 'Phạm vi nhiệm vụ được xem',
     ['– Có V1: xem tất cả nhiệm vụ.',
      '– Không có V1: xem nhiệm vụ mình là người tạo / thực hiện / duyệt kết quả / theo dõi; nhiệm vụ con và nhiệm '
      'vụ cha của các nhiệm vụ đó; nhiệm vụ thuộc giải pháp / dự án mình là thành viên; có Q1 thì thêm nhiệm vụ có '
      'người thực hiện thuộc phòng ban mình quản lý.',
      '– Cộng thêm theo cấp cao nhất đang có: V2 công ty đang làm việc › V3 phòng ban/bộ phận quản lý › V4 bộ phận '
      'quản lý (xét đơn vị của bất kỳ người giữ vai trò nào trên nhiệm vụ).',
      '– Nhiệm vụ Nháp chỉ người tạo nhìn thấy.'],
     ['Xem danh sách', 'Xuất Excel']),
    ('BR-02', 'Mã nhiệm vụ',
     ['– Sinh tự động khi lưu: <Mã công ty>.TASK.NB.<2 số cuối năm>.<STT 4 số>.',
      '– STT tăng dần theo năm và công ty của người tạo; không sửa được.'],
     ['Tạo mới']),
    ('BR-03', 'Trạng thái nhiệm vụ',
     ['– 10 trạng thái: Nháp · Chờ phê duyệt triển khai · Chờ bắt đầu · Đang thực hiện · Tạm dừng · Hoàn thành - Chờ '
      'duyệt · Từ chối kết quả · Hoàn thành · Huỷ · Từ chối triển khai.',
      '– Khi tạo chỉ chọn: Nháp / Chờ phê duyệt triển khai / Chờ bắt đầu / Đang thực hiện.'],
     ['Xem danh sách', 'Tạo mới', 'Chỉnh sửa']),
    ('BR-04', 'Chuyển trạng thái theo vai trò',
     ['– Nháp → (người tạo) Chờ bắt đầu / Chờ phê duyệt triển khai / Đang thực hiện.',
      '– Chờ phê duyệt triển khai → (người duyệt triển khai) Chờ bắt đầu / Từ chối triển khai.',
      '– Từ chối triển khai → (người tạo) Chờ phê duyệt triển khai / Chờ bắt đầu / Đang thực hiện.',
      '– Chờ bắt đầu → (người thực hiện) Đang thực hiện, Từ chối triển khai (khi chưa có kết quả); (người thực hiện '
      'hoặc người tạo) Tạm dừng.',
      '– Đang thực hiện → (người thực hiện hoặc người tạo) Tạm dừng; (người thực hiện) Hoàn thành - Chờ duyệt, hoặc '
      'Hoàn thành nếu không có người duyệt kết quả, Từ chối triển khai (khi chưa có kết quả).',
      '– Tạm dừng → (người thực hiện hoặc người tạo) Đang thực hiện / Chờ bắt đầu; (người thực hiện) Từ chối triển '
      'khai khi chưa có kết quả.',
      '– Hoàn thành - Chờ duyệt → (người duyệt kết quả) Hoàn thành / Từ chối kết quả.',
      '– Từ chối kết quả → (người thực hiện) Đang thực hiện / Tạm dừng, hoặc Hoàn thành nếu không có người duyệt '
      'kết quả.',
      '– Hoàn thành → (người tạo) Từ chối kết quả.',
      '– Chuyển sang Hoàn thành - Chờ duyệt / Hoàn thành bắt buộc tiến độ 100%.'],
     ['Chỉnh sửa', 'Duyệt triển khai', 'Nhập kết quả', 'Duyệt kết quả']),
    ('BR-05', 'Thông báo khi đổi trạng thái',
     ['– Sang Chờ phê duyệt triển khai: người có quyền Q1 quản lý phòng ban của người thực hiện — “Bạn có nhiệm vụ '
      '<Tên> cần được phê duyệt triển khai”.',
      '– Sang Chờ bắt đầu (từ Chờ phê duyệt triển khai, hoặc người tạo khác người thực hiện): người thực hiện — “Bạn '
      'có nhiệm vụ <Tên> chờ bắt đầu thực hiện”.',
      '– Từ chối triển khai từ Chờ phê duyệt triển khai: người tạo — “Nhiệm vụ <Tên> không được <Người> phê duyệt '
      'triển khai”; từ Chờ bắt đầu: người tạo + người duyệt triển khai — “Nhiệm vụ <Tên> đã bị <Người> từ chối triển '
      'khai”.',
      '– Sang Hoàn thành - Chờ duyệt: người duyệt kết quả — “Bạn có nhiệm vụ <Tên> cần được duyệt kết quả”.',
      '– Hoàn thành / Từ chối kết quả (từ Chờ duyệt): người thực hiện — “Nhiệm vụ <Tên> đã được / không được <Người> '
      'duyệt kết quả”.',
      '– Không gửi cho chính người thao tác; bấm thông báo mở thẳng nhiệm vụ.'],
     ['Tạo mới', 'Chỉnh sửa', 'Duyệt triển khai', 'Nhập kết quả', 'Duyệt kết quả']),
    ('BR-06', 'Điều kiện Sửa / Xóa',
     ['– Sửa: chỉ người tạo, nhiệm vụ chưa có nhiệm vụ con (mọi trạng thái).',
      '– Xóa: chỉ người tạo, nhiệm vụ Nháp, chưa có nhiệm vụ con.',
      '– Nút không dùng được thì ẩn ở cả danh sách lẫn cửa sổ chi tiết.'],
     ['Chỉnh sửa', 'Xóa']),
    ('BR-07', 'Nhiệm vụ chung và nhiệm vụ con',
     ['– Nhiệm vụ chung: mỗi người thực hiện được tạo 1 nhiệm vụ riêng, cùng nội dung, tệp đính kèm dùng chung.',
      '– Nhiệm vụ con chỉ thành nhiệm vụ thật khi nhiệm vụ cha khác Nháp / Chờ phê duyệt triển khai; kế thừa giải '
      'pháp, dự án, hạng mục, cuộc họp, trạng thái, ưu tiên, người duyệt; hạn không được sau hạn nhiệm vụ cha.'],
     ['Tạo mới', 'Chỉnh sửa']),
    ('BR-08', 'Hạn hoàn thành và quá hạn',
     ['– Khi tạo (và khi sửa nhiệm vụ Nháp): hạn không trước hôm nay; hạn là hôm nay thì giờ hạn ≥ giờ hiện tại.',
      '– Quá hạn: Hạn hoàn thành + Giờ hạn (không có giờ thì 23:59:59) đã qua và nhiệm vụ không ở Nháp / Hoàn thành '
      '/ Huỷ.'],
     ['Tạo mới', 'Chỉnh sửa', 'Xem danh sách']),
    ('BR-09', 'Kết quả, tiến độ, hiệu suất',
     ['– Tiến độ 0–100%; nhật ký báo cáo tiến độ không được giảm so với kỳ trước.',
      '– Hiệu suất = Số giờ được giao / Số giờ thực tế × 100% (bật báo cáo tiến độ thì giờ thực tế = tổng giờ nhật '
      'ký); tính khi sang Hoàn thành - Chờ duyệt / Hoàn thành.',
      '– Mọi thay đổi nhiệm vụ đều tính lại tiến độ hạng mục và giải pháp gắn với nhiệm vụ.'],
     ['Nhập kết quả', 'Duyệt kết quả']),
    ('BR-10', 'Giải pháp bị khoá thành viên',
     ['– Người dùng bị khoá khỏi giải pháp không tạo được nhiệm vụ gắn giải pháp đó: “Bạn đã bị khóa khỏi giải pháp '
      'này nên không thao tác được. Vui lòng liên hệ PM hoặc Trưởng phòng giải pháp.”'],
     ['Tạo mới']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

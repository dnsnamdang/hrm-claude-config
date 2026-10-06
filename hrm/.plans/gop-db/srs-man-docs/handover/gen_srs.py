# -*- coding: utf-8 -*-
"""Sinh "SRS - Phiếu bàn giao.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/handover/index.vue · _id/index.vue · add.vue (chế độ ?id= — Sửa)
      components/{HandoverInfoCard,HandoverItemsTable,HandoverHistoryModal,HandoverForm}.vue
      components/assign/SystemInfoSection.vue · components/modal/{export-fields-modal,base-confirm-modal}.vue
      components/V2BaseCompanyDepartmentFilter.vue · utils/handoverProgress.js
      components/menu-sidebar.js (menuItemsAssign › Nhiệm vụ; Phê duyệt › Bàn giao - Lắp đặt)
  BE  Modules/Assign/Routes/api.php (prefix assign/handovers; approve/reject gắn checkPermission:Duyệt bàn giao công việc)
      Http/Controllers/Api/V1/HandoverController.php · Services/HandoverService.php
      Http/Requests/Handover/{HandoverRequest,HandoverApproveRequest,HandoverRejectRequest}.php
      Entities/{Handover,HandoverItem,HandoverLog}.php · Transformers/HandoverResource/*
      Services/SystemLogService.php (TYPE_HANDOVER) · app/Helper/PermissionHelper.php (checkPermissionListWithColumn)
  Quyền: PermissionsTableSeeder id 1026-1029 (nhóm "Bàn giao công việc")
Ảnh: shots/ (Playwright headless 1440x900, client :3002). Dữ liệu mẫu: data_created.md.
"""
import os
from _hcommon import new_doc, extra_menu, NO_LOGIN, STATUS_TEXT, REASONS, TERMS

HERE = os.path.dirname(os.path.abspath(__file__))
TEN_MAN = 'Phiếu bàn giao'
MENU = 'Phân hệ Công việc => Nhiệm vụ => Phiếu bàn giao'
MENU_PD = 'Phân hệ Công việc => Phê duyệt => Bàn giao - Lắp đặt => Bàn giao công việc'

ICONS = {
    'Phân hệ Công việc': 'icon_phanhe.png',
    'Nhiệm vụ': 'icon_nhiemvu.png',
    'Phiếu bàn giao': 'icon_man.png',
    'Phê duyệt': 'icon_pheduyet.png',
    'Bàn giao - Lắp đặt': 'icon_bg_lapdat.png',
    'Bàn giao công việc': 'icon_bgcv.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Tuỳ chỉnh cột': 'icon_cot.png',
    'Xuất Excel': 'icon_xuat.png',
    'Mã phiếu': 'icon_maphieu.png',
    'Sửa': 'icon_sua.png',
    'Xóa': 'icon_xoa.png',
    'Lịch sử': 'icon_lichsu.png',
    'Duyệt': 'icon_duyet.png',
    'Không duyệt': 'icon_khongduyet.png',
    'Tạo phiếu': 'icon_taophieu.png',
}

d, shot = new_doc(HERE, TEN_MAN, MENU, 'hdv_', ICONS)

A_LAP = 'Người lập phiếu'
A_TP = 'Trưởng phòng (quyền Q4)'
NO_PERM = ('– Nếu không có quyền → nút không hiển thị; gọi thẳng chức năng thì hệ thống trả lỗi '
           '“Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.')

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Phiếu bàn giao (danh sách phiếu bàn giao công việc, '
    'phân hệ Công việc) và các chức năng mở từ màn này, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu các chức năng: xem danh sách, tìm kiếm/lọc, cài đặt bộ lọc, tuỳ chỉnh cột, xuất Excel, '
    'xem chi tiết, xem lịch sử, sửa, xóa, duyệt và không duyệt phiếu bàn giao.',
    'Làm rõ phạm vi phiếu mỗi người dùng được xem theo quyền xem theo cấp tổ chức.',
    'Làm rõ vòng đời trạng thái của phiếu (Nháp → Chờ duyệt → Đã duyệt / Từ chối → Hoàn tất) và ai nhận '
    'thông báo ở từng bước.',
    'Màn Tạo phiếu bàn giao và màn Chờ tiếp nhận bàn giao được đặc tả ở 2 tài liệu riêng: '
    '“SRS - Tạo bàn giao” và “SRS - Chờ tiếp nhận bàn giao”.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], TERMS + [
    ('Q1 … Q4', 'Ký hiệu quyền — xem Phần 2.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q4', 'Duyệt bàn giao công việc',
     'Hiện nút Duyệt / Không duyệt ở màn chi tiết của phiếu đang Chờ duyệt; hiện mục menu '
     '“Bàn giao công việc” trong nhóm Phê duyệt; nhận thông báo khi có phiếu gửi duyệt.'),
], widths=[0.8, 2.0, 3.2])
d.p('Menu “Phiếu bàn giao” và nút Tạo phiếu không gắn quyền — mọi người dùng đã đăng nhập đều thấy. '
    'Sửa / Xóa không gắn quyền mà theo điều kiện người lập phiếu và trạng thái (BR-03).')
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('Q1', 'Xem danh sách bàn giao công việc theo tổng công ty', 'Toàn bộ phiếu của mọi công ty.'),
    ('Q2', 'Xem danh sách bàn giao công việc theo công ty',
     'Phiếu thuộc công ty đang làm việc + phiếu do mình lập.'),
    ('Q3', 'Xem danh sách bàn giao công việc theo phòng ban',
     'Phiếu thuộc các phòng ban mình quản lý + phiếu do mình lập.'),
    ('–', 'Không có Q1, Q2, Q3', 'Chỉ phiếu do mình lập.'),
], widths=[0.8, 2.4, 2.8])
d.p('Có nhiều quyền thì áp phạm vi rộng nhất (Q1 > Q2 > Q3). Phiếu Nháp của người khác luôn bị ẩn với mọi quyền.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Q4', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách phiếu bàn giao', '✅', '✅', '✅', '✅ (*)', '✅ (phiếu mình lập)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tuỳ chỉnh cột', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Xuất Excel', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 Xem chi tiết phiếu bàn giao', '✅', '✅', '✅', '✅', '✅'),
    ('FR-07 Xem lịch sử phiếu bàn giao', '✅', '✅', '✅', '✅', '✅'),
    ('FR-08 Sửa phiếu bàn giao', '✅ (**)', '✅ (**)', '✅ (**)', '✅ (**)', '✅ (**)'),
    ('FR-09 Xóa phiếu bàn giao', '✅ (**)', '✅ (**)', '✅ (**)', '✅ (**)', '✅ (**)'),
    ('FR-10 Duyệt phiếu bàn giao', '❌', '❌', '❌', '✅', '❌'),
    ('FR-11 Không duyệt phiếu bàn giao', '❌', '❌', '❌', '✅', '❌'),
], widths=[2.2, 0.55, 0.55, 0.55, 0.65, 1.5])
d.p('(*) Q4 không mở rộng phạm vi danh sách — phạm vi vẫn theo Q1/Q2/Q3 đi kèm. '
    '(**) Chỉ người lập phiếu: Sửa khi phiếu Nháp hoặc Từ chối; Xóa khi phiếu Nháp.')

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_LAP, [0, 1, 2, 3]), (A_TP, [0, 4, 5])],
    [('FR-01', 'Xem danh sách phiếu bàn giao', 'view'),
     ('FR-05', 'Xuất Excel', 'action'),
     ('FR-08', 'Sửa phiếu bàn giao', 'crud'),
     ('FR-09', 'Xóa phiếu bàn giao', 'action'),
     ('FR-10', 'Duyệt phiếu bàn giao', 'action'),
     ('FR-11', 'Không duyệt phiếu bàn giao', 'action')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
     ('FR-07', 'Xem lịch sử phiếu', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách phiếu bàn giao')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng '
           'của màn Phiếu bàn giao tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách phiếu bàn giao',
    mota='Hiển thị bảng các phiếu bàn giao công việc trong phạm vi được xem, kèm số công việc đã nhận / từ chối / '
         'chờ nhận của từng phiếu.',
    tacnhan='Người lập phiếu; Trưởng phòng; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập.',
    chinh='1. Người dùng vào menu Phiếu bàn giao.\n'
          '2. Hệ thống nạp trang 1 (20 dòng/trang), sắp xếp mặc định theo Ngày tạo mới nhất.\n'
          '3. Hệ thống hiển thị bảng theo cấu hình cột đã lưu của người dùng (mặc định hiện hết cột).\n'
          '4. Người dùng bấm tiêu đề cột có biểu tượng sắp xếp để đổi thứ tự, đổi trang hoặc số dòng/trang.',
    phu='• Không có phiếu nào → “Không có phiếu bàn giao nào.”\n'
        '• Lỗi tải dữ liệu → “Lỗi khi tải dữ liệu”, bảng để trống.\n'
        '• Quay lại từ màn chi tiết/sửa trong vòng 10 phút → bộ lọc và trạng thái đóng/mở panel lọc được khôi phục.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-ds.png'), shot_caption='Màn danh sách phiếu bàn giao')
d.figure(shot('01b-ds-hanhdong.png'), 'Phần bên phải bảng — các cột hệ thống và cột Hành động', width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Danh sách phiếu bàn giao công việc', '–'),
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Danh sách phiếu bàn giao', '–'),
    ('Nút Tạo phiếu', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở màn Tạo phiếu bàn giao (đặc tả tại SRS - Tạo bàn giao).'),
    ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', 'Xem FR-05; khoá khi đang xuất.'),
    ('Nút Tuỳ chỉnh cột', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Biểu tượng cột, rê chuột hiện “Cấu hình cột hiển thị”. Xem FR-04.'),
    ('STT', 'Text', 'Read-only', '≥ 1', 'Theo dữ liệu', 'Đánh số liên tục theo trang. Cột ghim trái, khoá.'),
    ('Mã phiếu', 'Link', 'Read-only', 'BG.YYYY.NNNN', 'Theo dữ liệu',
     'Bấm để mở màn chi tiết (FR-06); chuột phải mở tab mới. Cột ghim trái, khoá. Sắp xếp được.'),
    ('Nhân viên bàn giao', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng.'),
    ('Phòng ban', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Phòng ban của người lập lúc lập phiếu.'),
    ('Lý do bàn giao', 'Text', 'Read-only', 'Danh sách 5 giá trị', 'Theo dữ liệu', REASONS + '. Sắp xếp được.'),
    ('Trạng thái', 'Badge', 'Read-only', 'Danh sách 5 giá trị', 'Theo dữ liệu', STATUS_TEXT + ' Sắp xếp được.'),
    ('Công việc bàn giao', 'Text', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Dòng 1 “<n> công việc”; dòng 2 các con số: ✓ đã nhận (xanh lá), ✗ từ chối nhận (đỏ), đồng hồ chờ nhận (cam); '
     'số bằng 0 thì ẩn.'),
    ('Ngày bàn giao', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Sắp xếp được.'),
    ('Ghi chú', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Ghi chú chung của phiếu, tối đa 2 dòng.'),
    ('Ngày gửi duyệt', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Sắp xếp được.'),
    ('Người duyệt', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Người đã duyệt phiếu.'),
    ('Ngày duyệt', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Sắp xếp được.'),
    ('Lý do từ chối', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Lý do TP không duyệt, tối đa 2 dòng.'),
    ('Người tạo / Ngày tạo', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Ngày tạo sắp xếp được.'),
    ('Người cập nhật / Ngày cập nhật', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Ngày cập nhật sắp xếp được.'),
    ('Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Cột cuối, khoá. Sửa (bút) — chỉ hiện khi được sửa (BR-03); Xóa (thùng rác đỏ) — chỉ hiện khi được xóa; '
     'Lịch sử (đồng hồ) — luôn hiện. Không có nút Xem vì Mã phiếu đã là liên kết.'),
    ('Phân trang', 'Pagination', 'Enable', '10/20/50/100', '20 dòng/trang',
     '“Hiển thị a–b / tổng”, chọn số dòng/trang, các nút trang.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có phiếu bàn giao nào.”'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n' + NO_LOGIN + '\n'
     'After:\n– Khôi phục bộ lọc đã lưu (nếu quay lại trong 10 phút); nạp danh sách theo phạm vi quyền (BR-01) '
     'và cấu hình cột của người dùng.\n– Lỗi → “Lỗi khi tải dữ liệu”.'),
    ('Bấm tiêu đề cột sắp xếp', 'Click', 'After:\n– Đổi chiều sắp xếp, về trang 1 và nạp lại.'),
    ('Đổi trang / số dòng mỗi trang', 'Click / Change', 'After:\n– Nạp lại dữ liệu; đổi số dòng thì về trang 1.'),
    ('Bấm Mã phiếu', 'Click', 'After:\n– Mở màn chi tiết phiếu (FR-06).'),
    ('Bấm Tạo phiếu', 'Click', 'After:\n– Chuyển sang màn Tạo phiếu bàn giao.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Phiếu bàn giao tại '
           'phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc phiếu bàn giao',
    mota='Tìm nhanh theo mã phiếu / tên nhân viên bàn giao và lọc theo Công ty, Phòng ban, Trạng thái, Lý do, '
         'khoảng Ngày tạo.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách phiếu bàn giao.',
    chinh='1. Người dùng gõ từ khoá vào ô tìm nhanh rồi bấm “Tìm kiếm” hoặc Enter.\n'
          '2. Người dùng bấm “Tìm kiếm nâng cao” để mở khối ô lọc.\n'
          '3. Người dùng chọn giá trị ở ô lọc — hệ thống tìm ngay, về trang 1.\n'
          '4. Bấm “Làm mới” để xoá mọi điều kiện và nạp lại.',
    phu='• Không có kết quả → “Không có phiếu bàn giao nào.”\n'
        '• Ô Công ty chỉ hiện khi có Q1; ô Phòng ban chỉ hiện khi có Q1, Q2 hoặc Q3.\n'
        '• Bấm “Ẩn tìm kiếm nâng cao” để thu khối ô lọc (giá trị đang lọc vẫn giữ).')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Gợi ý “Tìm theo mã phiếu, tên nhân viên bàn giao”. Tìm gần đúng theo Mã phiếu hoặc họ tên nhân viên bàn giao.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tìm theo toàn bộ điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá mọi điều kiện và nạp lại đúng 1 lần.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
     'Mở / thu khối ô lọc.'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống', 'Chỉ hiện khi có Q1. Nhãn nổi.'),
    ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Hiện khi có Q1/Q2/Q3; danh sách theo công ty đang chọn và phạm vi quyền.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống',
     'Nháp, Chờ duyệt, Đã duyệt, Từ chối, Hoàn tất.'),
    ('Lý do bàn giao', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống', REASONS + '.'),
    ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống',
     'Một ô khoảng ngày (từ – đến), lọc theo ngày tạo phiếu.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm / Enter ở ô tìm nhanh', 'Click / Keypress',
     'After:\n– Về trang 1, nạp danh sách theo từ khoá + các ô lọc, trong phạm vi quyền.'),
    ('Chọn giá trị ở ô lọc', 'Change',
     'After:\n– Tự tìm ngay (không cần bấm Tìm kiếm), về trang 1. Gõ ô tìm nhanh thì KHÔNG tự tìm.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xoá từ khoá + mọi ô lọc + sắp xếp, nạp lại trang 1.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Cài đặt bộ lọc')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc. Chỉ bổ sung các quy tắc riêng của màn Phiếu bàn giao.', anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Cho người dùng chọn ô lọc nào hiển thị trong khối Tìm kiếm nâng cao và sắp xếp thứ tự các ô.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách phiếu bàn giao.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
          '2. Hệ thống mở cửa sổ liệt kê 4 trường lọc theo thứ tự hiện tại.\n'
          '3. Người dùng tích / bỏ tích, kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm “Lưu” — khối ô lọc cập nhật theo cài đặt.',
    phu='• “Khôi phục mặc định” → về đủ 4 trường theo thứ tự gốc.\n'
        '• “Đóng” hoặc dấu × → đóng cửa sổ, không lưu.')
d.p('2.3.2 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', modal='Cài đặt bộ lọc', shot=shot('03-caidat.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
    ('Danh sách trường lọc', 'Checkbox', 'Enable', '4 trường', 'Không', 'Tích hết',
     '1. Công ty – Phòng ban · 2. Trạng thái · 3. Lý do bàn giao · 4. Ngày tạo. Kéo thả để đổi thứ tự.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cài đặt của người dùng cho màn này.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Trả về cài đặt gốc.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
])
d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở cửa sổ với cài đặt đang dùng.'),
    ('Kéo thả / tích trường', 'Change', 'After:\n– Cập nhật thứ tự / ẩn hiện trong cửa sổ (chưa lưu).'),
    ('Bấm Lưu', 'Click', 'After:\n– Lưu cài đặt theo tài khoản cho màn Phiếu bàn giao; khối lọc hiển thị lại theo cài đặt.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Đưa về 4 trường theo thứ tự gốc.'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Tuỳ chỉnh cột')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Phiếu bàn giao.', anchor='excel')
d.intro_table(
    ten='Tuỳ chỉnh cột',
    mota='Cho người dùng ẩn/hiện và sắp xếp thứ tự các cột của bảng danh sách phiếu bàn giao.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách phiếu bàn giao.',
    chinh='1. Người dùng bấm nút Tuỳ chỉnh cột (biểu tượng cột).\n'
          '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê đủ các cột.\n'
          '3. Người dùng tích / bỏ tích, kéo biểu tượng ≡ để đổi thứ tự.\n'
          '4. Người dùng bấm “Lưu” — bảng cập nhật ngay.',
    phu='• Cột khoá (STT, Mã phiếu, Hành động) hiển thị mờ kèm ổ khoá, không bỏ tích / kéo được.\n'
        '• “Đóng” → không lưu.')
d.p('2.4.2 Layout màn hình')
d.layout(menu=MENU + ' => Tuỳ chỉnh cột', modal='Tuỳ chỉnh cột', shot=shot('04-cot.png'),
         shot_caption='Cửa sổ Tuỳ chỉnh cột')
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', '–'),
    ('Cột khoá', 'Checkbox', 'Disable', '3 cột', '–', 'Tích',
     'STT, Mã phiếu, Hành động — luôn hiện, có biểu tượng ổ khoá.'),
    ('Các cột còn lại', 'Checkbox', 'Enable', '17 cột', 'Không', 'Tích hết',
     'Nhân viên bàn giao, Phòng ban, Lý do bàn giao, Trạng thái, Công việc, Ngày bàn giao, Ghi chú, Ngày gửi duyệt, '
     'Người duyệt, Ngày duyệt, Lý do từ chối, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. Kéo ≡ để đổi thứ tự.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình cột theo tài khoản.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
])
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tuỳ chỉnh cột', 'Click', 'After:\n– Mở cửa sổ với cấu hình cột đang dùng.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Lưu cấu hình cột của người dùng cho màn Phiếu bàn giao (lưu trên máy chủ, dùng lại ở mọi máy).\n'
     '– Bảng hiển thị lại theo cấu hình mới; cột đang hiện cũng là cột được tích sẵn khi Xuất Excel.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Xuất Excel')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Xuất Excel', 'action', actor=A_LAP)
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Phiếu bàn giao.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách phiếu bàn giao',
    mota='Xuất ra file Excel toàn bộ phiếu khớp bộ lọc đang áp dụng (không giới hạn theo trang), với các cột người '
         'dùng chọn.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách phiếu bàn giao.',
    chinh='1. Người dùng bấm “Xuất Excel”.\n'
          '2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn các cột đang hiện trên bảng.\n'
          '3. Người dùng tích / bỏ tích, kéo ≡ để đổi thứ tự cột trong file.\n'
          '4. Người dùng bấm “Xuất file”.\n'
          '5. Hệ thống tải về file danh_sach_phieu_ban_giao.xlsx và báo “Xuất Excel thành công”.',
    phu='• Không tích trường nào → nút “Xuất file” bị khoá.\n'
        '• Lỗi → “Lỗi khi xuất Excel”.',
    dacbiet='Dữ liệu xuất theo đúng bộ lọc + sắp xếp + phạm vi quyền của danh sách.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất file', shot=shot('05-xuat.png'),
         shot_caption='Cửa sổ Chọn trường xuất file')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất file', '–'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích / bỏ tích toàn bộ trường.'),
    ('Danh sách trường', 'Checkbox', 'Enable', '19 trường', 'Có (≥ 1)', 'Các cột đang hiện trên bảng',
     'Mã phiếu, Nhân viên bàn giao, Phòng ban, Lý do bàn giao, Trạng thái, Ngày bàn giao, Tổng công việc, Đã nhận, '
     'Từ chối nhận, Chờ nhận, Ghi chú, Ngày gửi duyệt, Người duyệt, Ngày duyệt, Lý do từ chối, Người tạo, Ngày tạo, '
     'Người cập nhật, Ngày cập nhật. Kéo ≡ để đổi thứ tự.'),
    ('Bộ đếm', 'Label', 'Hiển thị', '–', '–', 'Theo số trường', '“Đang chọn x/19 trường”.'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Enable',
     'Khoá khi chưa chọn trường nào hoặc đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ, tích sẵn các cột đang hiện trên bảng.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n' + NO_LOGIN + '\n'
     'After:\n– Lấy TẤT CẢ phiếu khớp bộ lọc đang áp dụng (bỏ phân trang), trong phạm vi quyền (BR-01).\n'
     '– Tải file danh_sach_phieu_ban_giao.xlsx, tiêu đề “Danh sách phiếu bàn giao”, cột theo đúng thứ tự đã chọn.\n'
     '– Hiển thị “Xuất Excel thành công”. Lỗi → “Lỗi khi xuất Excel”.'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Xem chi tiết phiếu bàn giao')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Phiếu bàn giao.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu bàn giao',
    mota='Hiển thị thông tin chung của phiếu, danh sách công việc bàn giao (tách tab Nhiệm vụ / Vấn đề, gom theo '
         'dự án) và khối Lịch sử.',
    tacnhan='Người lập phiếu; Trưởng phòng; Người nhận BG; Người dùng đã đăng nhập',
    dieukien='Người dùng mở phiếu từ danh sách hoặc từ thông báo.',
    chinh='1. Người dùng bấm Mã phiếu ở danh sách (hoặc bấm thông báo của phiếu ở chuông thông báo).\n'
          '2. Hệ thống mở màn chi tiết, tiêu đề “<Mã phiếu> — Chi tiết phiếu bàn giao”.\n'
          '3. Người dùng chuyển tab Nhiệm vụ / Vấn đề để xem công việc; bấm mã hoặc tên công việc để xem chi tiết '
          'nhiệm vụ / vấn đề (cửa sổ chỉ đọc).\n'
          '4. Người dùng bấm “Xem lịch sử” để mở khối Lịch sử (FR-07).\n'
          '5. Bấm “Quay lại” để về danh sách.',
    phu='• Phiếu đang Chờ duyệt và người dùng có Q4 → bảng công việc chuyển sang chế độ điều chỉnh và hiện '
        'nút Duyệt / Không duyệt (FR-10, FR-11).\n'
        '• Phiếu bị Từ chối → hiện khung đỏ “Phiếu bàn giao bị từ chối” kèm lý do, người duyệt, thời điểm.\n'
        '• Không tải được phiếu → “Lỗi tải phiếu bàn giao” và quay về danh sách.')
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Mã phiếu', shot=shot('06-chitiet.png'),
         shot_caption='Màn chi tiết phiếu bàn giao (phiếu Đã duyệt)')
d.p('Lối vào khác: bấm thông báo “Phiếu bàn giao …” ở chuông thông báo trên thanh tiêu đề.')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Khối Thông tin bàn giao', 'Card', 'Read-only', '–', 'Theo dữ liệu',
     'Góc phải là badge trạng thái phiếu. Các dòng: Mã phiếu, Ngày bàn giao, Người bàn giao (kèm phòng ban trong '
     'ngoặc), Người nhận bàn giao (danh sách người nhận không trùng, cách nhau dấu phẩy), Lý do, Người duyệt, Ngày '
     'duyệt (dd/mm/yyyy hh:mm:ss), Ghi chú.'),
    ('Khung phiếu bị từ chối', 'Toast / Alert', 'Hiển thị / Ẩn', '–', 'Ẩn',
     'Chỉ khi phiếu Từ chối: “Phiếu bàn giao bị từ chối” · “Lý do: …” · “Bởi: <người duyệt> — <thời điểm>”.'),
    ('Tiêu đề khối Danh sách cần bàn giao', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Kèm dòng “Công việc của <tên nhân viên bàn giao>”.'),
    ('Tab Nhiệm vụ (n) / Vấn đề (n)', 'Button', 'Enable', '–', 'Nhiệm vụ',
     'Đổi bảng giữa nhiệm vụ và vấn đề; bên cạnh “Tổng x — Đã gán y”.'),
    ('Dòng nhóm dự án', 'Table/Grid', 'Read-only', 'Đánh số La Mã', 'Theo dữ liệu',
     'Tên dự án (không có → “Không có dự án”) + “(n mục)”.'),
    ('Cột Mã • Tên', 'Link', 'Read-only', '–', 'Theo dữ liệu', 'Bấm mở cửa sổ chi tiết nhiệm vụ / vấn đề (chỉ đọc).'),
    ('Cột Người giao, Trạng thái, Ưu tiên', 'Text / Badge', 'Read-only', '–', 'Theo dữ liệu',
     'Trạng thái và mức ưu tiên hiện ở thời điểm xem của nhiệm vụ / vấn đề.'),
    ('Cột Tiến độ %', 'Text', 'Read-only', '0 – 100', 'Theo dữ liệu', 'Chỉ có ở tab Nhiệm vụ.'),
    ('Cột Hạn hoàn thành', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm:ss', 'Theo dữ liệu', '–'),
    ('Cột Người nhận BG, Ghi chú BG', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Trống hiển thị “—”.'),
    ('Khối Lịch sử', 'Card', 'Enable', '–', 'Thu gọn', 'Xem FR-07.'),
    ('Nút Duyệt / Không duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Chỉ khi phiếu Chờ duyệt và có Q4.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị',
     'Về danh sách phiếu bàn giao; nếu đang ở chế độ duyệt thì về màn “Bàn giao công việc” (phiếu chờ duyệt).'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n' + NO_LOGIN + '\n'
     'After:\n– Nạp phiếu kèm công việc, người nhận, lịch sử.\n– Lỗi → “Lỗi tải phiếu bàn giao”, về danh sách.'),
    ('Bấm tab Nhiệm vụ / Vấn đề', 'Click', 'After:\n– Đổi bảng công việc theo tab.'),
    ('Bấm mã / tên công việc', 'Click',
     'After:\n– Nhiệm vụ → mở cửa sổ “<mã> — Chi tiết nhiệm vụ” chế độ xem; Vấn đề → mở cửa sổ chi tiết vấn đề chỉ đọc.'),
    ('Bấm Quay lại', 'Click', 'After:\n– Về màn danh sách tương ứng.'),
])

# ------------------------------------------------------------------ 2.7
d.h3('2.7 Xem lịch sử phiếu bàn giao')
d.p('2.7.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn Phiếu bàn giao.', anchor='history')
d.intro_table(
    ten='Xem lịch sử phiếu bàn giao',
    mota='Dòng thời gian các thao tác trên phiếu, mới nhất ở trên: tạo, gửi duyệt, gửi lại, duyệt, từ chối, '
         'tiếp nhận / từ chối từng công việc, hoàn tất.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng xem được phiếu ở danh sách hoặc đang ở màn chi tiết.',
    chinh='1. Người dùng bấm biểu tượng Lịch sử ở cột Hành động (hoặc “Xem lịch sử” ở màn chi tiết).\n'
          '2. Hệ thống mở cửa sổ “Lịch sử phiếu bàn giao” với dòng “Phiếu bàn giao: <mã> - <nhân viên bàn giao>”.\n'
          '3. Mỗi mục: thời điểm, tên hành động (có màu), người thực hiện — phòng ban, nội dung.\n'
          '4. Người dùng bấm “Bộ lọc” để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.',
    phu='• Chưa có lịch sử → “Chưa có lịch sử thao tác nào.”\n'
        '• Lọc không ra kết quả → “Không có lịch sử phù hợp bộ lọc.”\n'
        '• Ở màn chi tiết: khối Lịch sử mặc định thu gọn, chỉ nạp khi mở; có nút “Làm mới”, “Thu gọn”.')
d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử', modal='Lịch sử phiếu bàn giao', shot=shot('11-lichsu.png'),
         shot_caption='Cửa sổ Lịch sử phiếu bàn giao mở từ danh sách')
d.figure(shot('06b-chitiet-lichsu.png'), 'Khối Lịch sử ở màn chi tiết phiếu', width_in=5.2)
d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Lịch sử phiếu bàn giao', '–'),
    ('Dòng nhận diện', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Phiếu bàn giao: <mã> - <nhân viên bàn giao>” chữ xám.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Mở / thu 4 ô lọc; chọn giá trị là lọc ngay.'),
    ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách', 'Trống',
     'Tạo phiếu, Gửi duyệt, Gửi duyệt lại, Duyệt, Từ chối, Nghiệm thu hạng mục (= tiếp nhận công việc), '
     'Từ chối hạng mục (= từ chối tiếp nhận), Hoàn tất.'),
    ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách', 'Trống', '–'),
    ('Từ ngày / Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '–'),
    ('Mục lịch sử', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Thời điểm dd/mm/yyyy hh:mm · tên hành động · “Người thực hiện: <tên> — <phòng ban>” · nội dung.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thao tác nào.”'),
], required=False)
d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lịch sử (danh sách) / Xem lịch sử (chi tiết)', 'Click',
     'After:\n– Nạp lịch sử của phiếu, sắp mới nhất trước. Không gắn quyền riêng: xem được phiếu là xem được lịch sử.'),
    ('Chọn ô lọc', 'Change', 'After:\n– Lọc ngay trên danh sách đã nạp.'),
    ('Đóng cửa sổ', 'Click', 'After:\n– Đóng; lần mở sau nạp lại từ đầu.'),
])

# ------------------------------------------------------------------ 2.8
d.h3('2.8 Sửa phiếu bàn giao')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Sửa phiếu bàn giao', 'crud', actor=A_LAP)
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của phiếu bàn giao.',
           anchor='create')
d.intro_table(
    ten='Sửa phiếu bàn giao',
    mota='Người lập sửa phiếu Nháp hoặc phiếu bị Từ chối rồi lưu nháp lại hoặc gửi duyệt lại. Dùng chung màn với '
         'Tạo phiếu bàn giao, tiêu đề “Sửa phiếu bàn giao”.',
    tacnhan='Người lập phiếu',
    dieukien='Phiếu ở trạng thái Nháp hoặc Từ chối, người đang đăng nhập là người lập phiếu.',
    chinh='1. Người dùng bấm biểu tượng Sửa ở cột Hành động.\n'
          '2. Hệ thống mở màn Sửa với Ngày bàn giao, Lý do, Ghi chú chung và danh sách công việc của phiếu.\n'
          '3. Người dùng chỉnh thông tin, người nhận, tiến độ, ghi chú từng công việc, bỏ công việc khỏi danh sách.\n'
          '4. Người dùng bấm “Lưu nháp” hoặc “Lưu và gửi” (cách xử lý đặc tả ở SRS - Tạo bàn giao).\n'
          '5. Lưu thành công → quay về danh sách.',
    phu='• Phiếu bị Từ chối → đầu form hiện khung đỏ “Phiếu bàn giao bị từ chối” kèm lý do.\n'
        '• Phiếu không còn Nháp / Từ chối (mở bằng đường dẫn trực tiếp) → “Phiếu không ở trạng thái cho phép sửa” '
        'và chuyển sang màn chi tiết.\n'
        '• Không tải được phiếu → “Lỗi tải phiếu bàn giao”, về danh sách.',
    dacbiet='Màn Sửa chỉ hiện các công việc đang có trong phiếu (không nạp thêm công việc mới). Gửi lại phiếu bị từ '
            'chối ghi lịch sử “Gửi duyệt lại”.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('09-sua.png'), shot_caption='Màn Sửa phiếu bàn giao bị từ chối')
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Khung phiếu bị từ chối', 'Toast / Alert', 'Hiển thị / Ẩn', '–', '–', 'Ẩn',
     'Chỉ với phiếu Từ chối: “Phiếu bàn giao bị từ chối” · “Lý do: …”.'),
    ('Ngày bàn giao', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Theo dữ liệu', '–'),
    ('Lý do', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Có', 'Theo dữ liệu', REASONS + '.'),
    ('Ghi chú chung', 'Textbox', 'Enable', '0–1000 ký tự', 'Không', 'Theo dữ liệu', '–'),
    ('Bảng Danh sách cần bàn giao', 'Table/Grid', 'Enable', '–', 'Có (≥ 1 dòng)', 'Công việc của phiếu',
     'Đủ các cột/ thao tác như màn Tạo bàn giao: chọn người nhận từng dòng / theo dự án / hàng loạt, Tiến độ %, '
     'Ghi chú BG, bỏ khỏi danh sách.'),
    ('Người nhận BG', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Theo dữ liệu',
     'Nhân sự liên quan giải pháp / hạng mục của công việc, trừ chính người lập.'),
    ('Tiến độ %', 'Number', 'Enable', 'Số nguyên 0 – 100', 'Không', 'Theo dữ liệu', 'Chỉ nhiệm vụ.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Lưu và gửi', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu rồi gửi trưởng phòng duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về danh sách phiếu bàn giao.'),
])
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Sửa', 'Click',
     'Before:\n– Nút chỉ hiện khi phiếu Nháp/Từ chối và người dùng là người lập phiếu (BR-03).\n'
     'After:\n– Mở màn Sửa; phiếu không ở trạng thái cho phép → “Phiếu không ở trạng thái cho phép sửa”, '
     'chuyển sang chi tiết.'),
    ('Bấm Lưu nháp', 'Click',
     'Before:\n– Còn ô Tiến độ % báo đỏ → “Dữ liệu chưa hợp lệ, vui lòng kiểm tra các ô báo lỗi”, dừng.\n'
     'During:\n– Ngày bàn giao trống → “Vui lòng chọn ngày bàn giao”.\n– Lý do trống → “Vui lòng chọn lý do bàn giao”.\n'
     '– Công việc chưa chọn người nhận → “Bắt buộc phải nhập” dưới ô Người nhận BG.\n'
     '– Có lỗi → toast “Bạn chưa nhập đầy đủ thông tin”, không lưu.\n'
     '– Phiếu không còn Nháp/Từ chối → “Chỉ có thể sửa phiếu ở trạng thái Nháp hoặc Từ chối”.\n'
     '– Không phải người lập → “Bạn không có quyền sửa phiếu này”.\n'
     '– Công việc đang nằm trong phiếu khác chưa hoàn tất → “Có nhiệm vụ đã được bàn giao trong 1 phiếu khác chưa '
     'hoàn tất: <mã>”.\n'
     'After:\n– Ghi đè thông tin phiếu và thay toàn bộ danh sách công việc; tiến độ nhập được ghi thẳng vào nhiệm vụ.\n'
     '– “Đã lưu nháp thành công”, về danh sách. Trạng thái phiếu giữ nguyên.'),
    ('Bấm Lưu và gửi', 'Click',
     'After:\n– Như màn Tạo bàn giao: kiểm tra, hỏi xác nhận, lưu rồi gửi duyệt; phiếu sang Chờ duyệt, xoá lý do từ '
     'chối cũ; ghi lịch sử “Gửi duyệt lại” (nếu trước đó Từ chối); thông báo cho trưởng phòng; '
     '“Đã gửi phiếu cho trưởng phòng duyệt”, về danh sách.'),
])

# ------------------------------------------------------------------ 2.9
d.h3('2.9 Xóa phiếu bàn giao')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Xóa phiếu bàn giao', 'action', actor=A_LAP)
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo / Quy tắc Xóa. Chỉ bổ sung các quy tắc riêng của phiếu bàn giao.', anchor='delete')
d.intro_table(
    ten='Xóa phiếu bàn giao',
    mota='Người lập xóa hẳn phiếu Nháp của mình (kèm danh sách công việc và lịch sử của phiếu).',
    tacnhan='Người lập phiếu',
    dieukien='Phiếu ở trạng thái Nháp, người đang đăng nhập là người lập phiếu.',
    chinh='1. Người dùng bấm biểu tượng Xóa ở cột Hành động.\n'
          '2. Hệ thống hiện hộp “Xác nhận xóa”: “Bạn có chắc muốn xóa phiếu bàn giao <mã>?”.\n'
          '3. Người dùng bấm “Xóa”.\n'
          '4. Hệ thống xóa phiếu, báo “Đã xóa phiếu bàn giao” và nạp lại danh sách.',
    phu='• Bấm “Hủy” hoặc × → đóng hộp, không xóa.\n'
        '• Xóa lỗi → “Lỗi xóa phiếu bàn giao”.',
    dacbiet='Xóa vĩnh viễn, không khôi phục; các nhiệm vụ / vấn đề trong phiếu được giải phóng để lập phiếu khác.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', shot=shot('10-xoa.png'), shot_caption='Hộp xác nhận xóa phiếu bàn giao')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Xác nhận xóa', 'Biểu tượng cảnh báo đỏ.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu', '“Bạn có chắc muốn xóa phiếu bàn giao <mã in đậm>?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Màu đỏ, biểu tượng thùng rác.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không xóa.'),
], required=False, scope=False)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xóa ở dòng', 'Click',
     'Before:\n– Nút chỉ hiện khi phiếu Nháp và người dùng là người lập (BR-03).\nAfter:\n– Mở hộp xác nhận.'),
    ('Bấm Xóa ở hộp xác nhận', 'Click',
     'Before:\n– Phiếu không còn Nháp → hệ thống từ chối (“Chỉ có thể xóa phiếu ở trạng thái Nháp”).\n'
     '– Không phải người lập → hệ thống từ chối (“Bạn không có quyền xóa phiếu này”).\n'
     '– Có lỗi → màn hình hiển thị “Lỗi xóa phiếu bàn giao”.\n'
     'After:\n– Xóa phiếu, danh sách công việc và lịch sử của phiếu.\n– “Đã xóa phiếu bàn giao”, nạp lại danh sách.'),
])

# ------------------------------------------------------------------ 2.10
LAY_PD = ('Màn chi tiết phiếu đang Chờ duyệt — mở bằng Mã phiếu ở danh sách hoặc từ màn “Bàn giao công việc” '
          '(phiếu chờ duyệt) ở nhóm Phê duyệt, hoặc từ thông báo “Phiếu bàn giao công việc chờ duyệt”.')
d.h3('2.10 Duyệt phiếu bàn giao')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Duyệt phiếu bàn giao', 'action', actor=A_TP)
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc '
           'ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Duyệt phiếu bàn giao',
    mota='Trưởng phòng duyệt phiếu Chờ duyệt; trước khi duyệt có thể điều chỉnh người nhận, ghi chú bàn giao, tiến độ '
         'và đặt hạn hoàn thành mới cho từng công việc.',
    tacnhan='Trưởng phòng',
    dieukien='Phiếu ở trạng thái Chờ duyệt; người dùng có Q4.',
    chinh='1. Trưởng phòng mở chi tiết phiếu Chờ duyệt.\n'
          '2. (Tuỳ chọn) Điều chỉnh Người nhận BG (từng dòng / theo dự án / hàng loạt), Ghi chú BG, Tiến độ %, '
          'Hạn HT mới.\n'
          '3. Bấm “Duyệt” → hộp “Duyệt phiếu bàn giao”: “Xác nhận duyệt phiếu bàn giao <mã>?”.\n'
          '4. Bấm “Duyệt” ở hộp xác nhận.\n'
          '5. Hệ thống duyệt, báo “Đã duyệt phiếu bàn giao” và chuyển về màn “Bàn giao công việc” (phiếu chờ duyệt).',
    phu='• Ô Tiến độ % ngoài 0–100 → báo đỏ “Chỉ nhập số nguyên 0–100” dưới ô; bấm Duyệt → “Dữ liệu chưa hợp lệ, '
        'vui lòng kiểm tra các ô báo lỗi”, không mở hộp xác nhận.\n'
        '• Phiếu không còn Chờ duyệt → “Phiếu không ở trạng thái chờ duyệt”.\n'
        '• Lỗi khác → nội dung lỗi hoặc “Lỗi duyệt phiếu”.',
    dacbiet='Tiến độ % điều chỉnh được ghi thẳng vào nhiệm vụ; Hạn HT mới ghi vào hạn hoàn thành (ngày + giờ) của '
            'nhiệm vụ / vấn đề. Chỉ gửi các dòng khi người duyệt có điều chỉnh.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Mã phiếu => Duyệt', shot=shot('07-duyet-man.png'),
         shot_caption='Màn chi tiết phiếu Chờ duyệt ở chế độ duyệt')
extra_menu(d, MENU_PD + ' => Duyệt', LAY_PD)
d.figure(shot('07b-duyet-xacnhan.png'), 'Hộp xác nhận Duyệt phiếu bàn giao', width_in=6.2)
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Người nhận BG (từng dòng)', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Người nhận đã chọn',
     'Nhân sự liên quan giải pháp / hạng mục của công việc, trừ nhân viên bàn giao.'),
    ('Dropdown + nút Gán (dòng dự án)', 'Dropdown / Button', 'Enable', 'Danh sách', 'Không', '-- Chọn --',
     'Gán 1 người nhận cho mọi công việc của dự án.'),
    ('Ô chọn dòng + thanh Gán hàng loạt', 'Checkbox / Button', 'Enable', '–', 'Không', 'Bỏ chọn',
     '“Đã chọn: n mục” · “-- Chọn người nhận --” (giao của danh sách người nhận hợp lệ của các dòng) · “Gán hàng loạt” '
     '· “Bỏ chọn”.'),
    ('Ghi chú BG', 'Textbox', 'Enable', '0–500 ký tự', 'Không', 'Theo dữ liệu', 'Gợi ý “Ghi chú...”.'),
    ('Tiến độ %', 'Number', 'Enable', 'Số nguyên 0 – 100', 'Không', 'Theo dữ liệu',
     'Chỉ tab Nhiệm vụ; sai thì báo đỏ dưới ô, giữ nguyên số đã gõ.'),
    ('Hạn HT mới', 'Datepicker', 'Enable', 'Ngày + giờ', 'Không', 'Trống', 'Hạn hoàn thành mới của công việc.'),
    ('Nút Duyệt', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn', 'Chỉ khi phiếu Chờ duyệt và có Q4.'),
    ('Hộp Duyệt phiếu bàn giao', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     '“Xác nhận duyệt phiếu bàn giao <mã>?” · nút Duyệt / Hủy.'),
])
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Sửa Tiến độ %', 'Change',
     'After:\n– Không phải số nguyên 0–100 → “Chỉ nhập số nguyên 0–100” dưới ô; để trống là hợp lệ.'),
    ('Bấm Duyệt (chân trang)', 'Click',
     'Before:\n– Còn ô Tiến độ báo đỏ → “Dữ liệu chưa hợp lệ, vui lòng kiểm tra các ô báo lỗi”, dừng.\n'
     'After:\n– Mở hộp xác nhận.'),
    ('Bấm Duyệt ở hộp xác nhận', 'Click',
     'Before:\n– Kiểm tra quyền Q4.\n' + NO_PERM + '\n'
     'During:\n– Phiếu không còn Chờ duyệt → “Phiếu không ở trạng thái chờ duyệt”.\n'
     '– Dữ liệu dòng sai (tiến độ, người nhận không tồn tại, ghi chú > 500 ký tự) → lỗi hiện dưới đúng ô + '
     '“Dữ liệu chưa hợp lệ, vui lòng kiểm tra các ô báo lỗi”.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Ghi điều chỉnh từng công việc; phiếu sang Đã duyệt, ghi người duyệt + thời điểm duyệt.\n'
     '– Ghi lịch sử “<TP> (Trưởng phòng) đã duyệt phiếu bàn giao.”\n'
     '– Gửi thông báo “Phiếu bàn giao đã được duyệt” — “Phiếu bàn giao <mã> đã được duyệt. Vui lòng xác nhận tiếp '
     'nhận công việc.” cho người lập phiếu và mọi người nhận.\n'
     '– “Đã duyệt phiếu bàn giao”, chuyển về màn Bàn giao công việc (phiếu chờ duyệt).'),
])

# ------------------------------------------------------------------ 2.11
d.h3('2.11 Không duyệt phiếu bàn giao')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Không duyệt phiếu bàn giao', 'action', actor=A_TP)
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc '
           'ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Không duyệt phiếu bàn giao',
    mota='Trưởng phòng trả phiếu Chờ duyệt về trạng thái Từ chối kèm lý do; người lập sửa và gửi lại.',
    tacnhan='Trưởng phòng',
    dieukien='Phiếu ở trạng thái Chờ duyệt; người dùng có Q4.',
    chinh='1. Trưởng phòng bấm “Không duyệt” ở màn chi tiết phiếu.\n'
          '2. Hệ thống mở hộp “Từ chối phiếu bàn giao”.\n'
          '3. Trưởng phòng nhập Lý do từ chối (tối thiểu 10 ký tự) rồi bấm “Từ chối”.\n'
          '4. Hệ thống chuyển phiếu sang Từ chối, báo “Đã từ chối phiếu bàn giao” và chuyển về màn Bàn giao công việc.',
    phu='• Lý do dưới 10 ký tự → “Lý do từ chối phải có tối thiểu 10 ký tự”, không gửi.\n'
        '• Phiếu không còn Chờ duyệt → “Phiếu không ở trạng thái chờ duyệt”.\n'
        '• Lỗi khác → nội dung lỗi hoặc “Lỗi từ chối phiếu”.',
    dacbiet='Lý do từ chối hiện ở danh sách (cột Lý do từ chối), màn chi tiết và đầu form Sửa.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Mã phiếu => Không duyệt', shot=shot('08-khongduyet.png'),
         shot_caption='Hộp Từ chối phiếu bàn giao')
extra_menu(d, MENU_PD + ' => Không duyệt', LAY_PD)
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp', 'Label', 'Hiển thị', '–', '–', 'Từ chối phiếu bàn giao', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Vui lòng nhập lý do từ chối (tối thiểu 10 ký tự):”'),
    ('Lý do từ chối', 'Textarea', 'Enable', '10–1000 ký tự', 'Có', 'Trống', 'Gợi ý “Nhập lý do từ chối...”.'),
    ('Nút Từ chối', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Gửi lý do.'),
    ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng hộp, không thay đổi.'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Không duyệt', 'Click', 'Before:\n– Nút chỉ hiện khi phiếu Chờ duyệt và có Q4.\nAfter:\n– Mở hộp nhập lý do.'),
    ('Bấm Từ chối', 'Click',
     'Before:\n– Kiểm tra quyền Q4.\n' + NO_PERM + '\n'
     'During:\n– Lý do trống hoặc < 10 ký tự → “Lý do từ chối phải có tối thiểu 10 ký tự”.\n'
     '– Lý do > 1000 ký tự → “Lý do từ chối không được vượt quá 1000 ký tự”.\n'
     '– Phiếu không còn Chờ duyệt → “Phiếu không ở trạng thái chờ duyệt”.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Phiếu sang Từ chối, lưu lý do.\n'
     '– Ghi lịch sử “<TP> (Trưởng phòng) đã từ chối phiếu. Lý do: …”.\n'
     '– Gửi thông báo “Phiếu bàn giao bị từ chối” — “Phiếu bàn giao <mã> bị từ chối. Lý do: …” cho người lập phiếu.\n'
     '– “Đã từ chối phiếu bàn giao”, chuyển về màn Bàn giao công việc (phiếu chờ duyệt).'),
])

# ==================================================== PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của phiếu bàn giao công việc; không lặp lại các quy tắc đã có '
           'trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi phiếu được xem', [
        '– Q1: mọi phiếu. Q2: phiếu thuộc công ty đang làm việc + phiếu mình lập. Q3: phiếu thuộc phòng ban mình '
        'quản lý + phiếu mình lập. Không có quyền xem: chỉ phiếu mình lập.',
        '– Phiếu Nháp của người khác luôn bị ẩn.',
        '– Danh sách, tìm kiếm và Xuất Excel dùng chung phạm vi này.',
    ], ['Xem danh sách', 'Tìm kiếm và lọc', 'Xuất Excel']),
    ('BR-02', 'Vòng đời trạng thái phiếu', [
        '– Lập phiếu → Nháp. Gửi duyệt → Chờ duyệt. TP duyệt → Đã duyệt; TP không duyệt → Từ chối.',
        '– Phiếu Từ chối được người lập sửa và gửi lại → Chờ duyệt.',
        '– Đã duyệt → Hoàn tất tự động khi mọi công việc đã được người nhận tiếp nhận hoặc từ chối.',
    ], 'Toàn màn hình'),
    ('BR-03', 'Điều kiện Sửa / Xóa', [
        '– Chỉ người lập phiếu được sửa / xóa.',
        '– Sửa: khi phiếu Nháp hoặc Từ chối. Xóa: chỉ khi phiếu Nháp (xóa hẳn cả công việc và lịch sử).',
        '– Không thoả → nút ẩn ở danh sách; gọi thẳng chức năng thì hệ thống từ chối.',
    ], ['Sửa phiếu', 'Xóa phiếu']),
    ('BR-04', 'Một công việc chỉ nằm trong 1 phiếu chưa hoàn tất', [
        '– Nhiệm vụ / vấn đề đã nằm trong một phiếu chưa Hoàn tất khác thì không được đưa vào phiếu mới: '
        '“Có nhiệm vụ đã được bàn giao trong 1 phiếu khác chưa hoàn tất: <mã>”.',
    ], ['Sửa phiếu']),
    ('BR-05', 'Điều chỉnh khi duyệt', [
        '– TP được đổi người nhận, ghi chú BG, tiến độ (0–100) và đặt hạn hoàn thành mới cho từng công việc trước khi '
        'duyệt; tiến độ và hạn mới ghi thẳng vào nhiệm vụ / vấn đề.',
        '– Lý do không duyệt: 10–1000 ký tự.',
    ], ['Duyệt', 'Không duyệt']),
    ('BR-06', 'Mã phiếu', [
        '– Tự sinh BG.<năm>.<4 chữ số>, đánh số tăng dần trong năm (BG.2026.0001, BG.2026.0002…).',
    ], 'Tạo / Sửa phiếu'),
    ('BR-07', 'Thông báo', [
        '– Gửi duyệt: “Phiếu bàn giao công việc chờ duyệt” → người quản lý phòng ban và nhân viên cùng phòng có quyền '
        'Q4 (cùng công ty).',
        '– Duyệt: “Phiếu bàn giao đã được duyệt” → người lập + mọi người nhận.',
        '– Không duyệt: “Phiếu bàn giao bị từ chối” → người lập.',
        '– Tiếp nhận / từ chối / hoàn tất: xem SRS - Chờ tiếp nhận bàn giao.',
    ], ['Duyệt', 'Không duyệt', 'Sửa phiếu']),
    ('BR-08', 'Ghi lịch sử', [
        '– Ghi theo sự kiện: Tạo phiếu, Gửi duyệt, Gửi duyệt lại, Duyệt, Từ chối, Tiếp nhận / Từ chối từng công việc, '
        'Hoàn tất. Thao tác Lưu nháp sửa phiếu không ghi lịch sử.',
    ], 'Xem lịch sử'),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

# -*- coding: utf-8 -*-
"""Sinh "SRS - Chờ tiếp nhận bàn giao.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/handover/receiving.vue · _id/receive.vue
      components/{HandoverInfoCard,HandoverItemsTable,HandoverHistoryModal}.vue
      components/modal/{export-fields-modal,base-confirm-modal}.vue · components/V2Footer.vue
      components/menu-sidebar.js (menuItemsAssign › Nhiệm vụ › Chờ tiếp nhận bàn giao)
  BE  Modules/Assign/Routes/api.php (assign/handovers/receiving, receiving/export, receiving/filter-options,
      items/{id}/accept, items/{id}/reject, {id}/accept-all-items — không gắn quyền)
      Http/Controllers/Api/V1/HandoverItemController.php · Services/HandoverService.php
      (receivingHandovers, receivingFilterOptions, acceptItem, rejectItem, acceptAllItems, checkAndCompleteHandover,
      sendItemNotification, sendTaskTransferredToApproverNotification, sendCompletionNotification,
      sendBulkAcceptNotification) · Http/Requests/Handover/HandoverItemRejectRequest.php
      Transformers/HandoverResource/ReceivingHandoverResource.php · app/ExcelExport/ExportColumnRegistry ['handover_receiving']
Ảnh: shots/ (Playwright headless 1440x900, client :3002, đăng nhập bằng tài khoản người nhận — xem data_created.md).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'handover'))
from _hcommon import new_doc, NO_LOGIN, STATUS_TEXT, REASONS, TERMS  # noqa: E402

TEN_MAN = 'Chờ tiếp nhận bàn giao'
MENU = 'Phân hệ Công việc => Nhiệm vụ => Chờ tiếp nhận bàn giao'
ICONS = {
    'Phân hệ Công việc': 'icon_phanhe.png',
    'Nhiệm vụ': 'icon_nhiemvu.png',
    'Chờ tiếp nhận bàn giao': 'icon_man.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Tuỳ chỉnh cột': 'icon_cot.png',
    'Xuất Excel': 'icon_xuat.png',
    'Mã phiếu': 'icon_maphieu.png',
    'Tiếp nhận': 'icon_tiepnhan.png',
    'Lịch sử': 'icon_lichsu.png',
    'Nhận': 'icon_nhan.png',
    'Từ chối': 'icon_tuchoi.png',
    'Tiếp nhận tất cả': 'icon_tiepnhantatca.png',
    'Quay lại': 'icon_quaylai.png',
}
d, shot = new_doc(HERE, TEN_MAN, MENU, 'hdr_', ICONS)
A = 'Người nhận bàn giao'
MENU_TN = MENU + ' => Tiếp nhận'

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Chờ tiếp nhận bàn giao (phân hệ Công việc) — nơi người được '
    'chỉ định nhận công việc xem các phiếu bàn giao đã duyệt có công việc giao cho mình và xác nhận tiếp nhận hoặc '
    'từ chối từng công việc, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu: xem danh sách, tìm kiếm/lọc, cài đặt bộ lọc, tuỳ chỉnh cột, xuất Excel, xem lịch sử, '
    'xem phiếu cần tiếp nhận, tiếp nhận từng công việc, tiếp nhận tất cả, từ chối tiếp nhận, xem chi tiết công việc.',
    'Làm rõ việc chuyển người thực hiện của nhiệm vụ / vấn đề khi tiếp nhận hoặc từ chối, và điều kiện phiếu tự '
    'chuyển Hoàn tất.',
    'Các bước lập và duyệt phiếu đặc tả tại “SRS - Tạo bàn giao” và “SRS - Phiếu bàn giao”.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], TERMS + [
    ('Công việc của tôi', 'Các công việc trong phiếu có Người nhận BG là người đang đăng nhập.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('–', 'Không gắn quyền riêng',
     'Mọi người dùng đã đăng nhập đều thấy menu. Quyền thao tác do vai trò quyết định: chỉ người nhận của công '
     'việc mới tiếp nhận / từ chối được công việc đó.'),
], widths=[0.8, 2.0, 3.2])
d.p('Phạm vi dữ liệu không theo cấp tổ chức: chỉ phiếu Đã duyệt hoặc Hoàn tất có ít nhất 1 công việc giao cho '
    'người đang đăng nhập (BR-01).')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người nhận của công việc', 'Không có quyền nào (không là người nhận)'], [
    ('FR-01 Xem danh sách phiếu chờ tiếp nhận', '✅', '✅ (danh sách rỗng)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅'),
    ('FR-04 Tuỳ chỉnh cột', '✅', '✅'),
    ('FR-05 Xuất Excel', '✅', '✅ (file rỗng)'),
    ('FR-06 Xem lịch sử phiếu', '✅', '–'),
    ('FR-07 Xem phiếu cần tiếp nhận', '✅', '–'),
    ('FR-08 Tiếp nhận công việc', '✅', '❌'),
    ('FR-09 Tiếp nhận tất cả', '✅', '❌'),
    ('FR-10 Từ chối tiếp nhận', '✅', '❌'),
    ('FR-11 Xem chi tiết nhiệm vụ / vấn đề', '✅', '–'),
], widths=[2.8, 1.5, 1.7])

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A, [0, 1, 2, 3, 4, 5])],
    [('FR-01', 'Xem phiếu chờ tiếp nhận', 'view'),
     ('FR-05', 'Xuất Excel', 'action'),
     ('FR-07', 'Xem phiếu cần tiếp nhận', 'view'),
     ('FR-08', 'Tiếp nhận công việc', 'action'),
     ('FR-09', 'Tiếp nhận tất cả', 'action'),
     ('FR-10', 'Từ chối tiếp nhận', 'action')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem lịch sử phiếu', 'view', 'extend', [0], None),
     ('FR-11', 'Xem chi tiết nhiệm vụ / vấn đề', 'view', 'extend', [2], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)
d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách phiếu chờ tiếp nhận')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn '
           'Chờ tiếp nhận bàn giao tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách phiếu chờ tiếp nhận',
    mota='Mỗi dòng là 1 phiếu bàn giao đã duyệt có công việc giao cho người đăng nhập, kèm số công việc của tôi đã '
         'nhận / từ chối / chờ nhận.',
    tacnhan='Người nhận bàn giao; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập.',
    chinh='1. Người dùng vào menu Chờ tiếp nhận bàn giao.\n'
          '2. Hệ thống nạp trang 1 (20 dòng/trang), sắp xếp mặc định theo Ngày TP duyệt mới nhất.\n'
          '3. Đầu bảng hiện “Tổng: N” (số phiếu).\n'
          '4. Người dùng bấm Mã phiếu hoặc nút Tiếp nhận để mở phiếu (FR-07).',
    phu='• Không có phiếu → “Không có phiếu bàn giao nào chờ bạn tiếp nhận.”\n'
        '• Lỗi tải → “Lỗi khi tải dữ liệu”.\n'
        '• Quay lại trong vòng 10 phút → khôi phục bộ lọc đã dùng.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-ds.png'), shot_caption='Màn Phiếu bàn giao chờ tiếp nhận')
d.figure(shot('01b-ds-hanhdong.png'), 'Phần bên phải bảng — cột Hành động', width_in=6.2)
d.p('Lối vào khác: thông báo “Phiếu bàn giao đã được duyệt” ở chuông thông báo (mở màn chi tiết phiếu).')
d.figure(shot('00-thongbao.png'), 'Thông báo phiếu bàn giao đã được duyệt gửi tới người nhận', width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Phiếu bàn giao chờ tiếp nhận', '–'),
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Phiếu bàn giao chờ tôi tiếp nhận', '–'),
    ('Nhãn Tổng', 'Badge', 'Hiển thị', '≥ 0', 'Theo dữ liệu', '“Tổng: N” — số phiếu khớp bộ lọc.'),
    ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', 'Xem FR-05.'),
    ('Nút Tuỳ chỉnh cột', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Xem FR-04.'),
    ('STT', 'Text', 'Read-only', '≥ 1', 'Theo dữ liệu', 'Cột ghim trái, khoá.'),
    ('Mã phiếu', 'Link', 'Read-only', 'BG.YYYY.NNNN', 'Theo dữ liệu',
     'Bấm mở màn Xác nhận tiếp nhận công việc (FR-07). Cột ghim trái, khoá. Sắp xếp được.'),
    ('Người bàn giao', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Phòng ban', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Phòng ban của phiếu.'),
    ('Lý do bàn giao', 'Text', 'Read-only', 'Danh sách 5 giá trị', 'Theo dữ liệu', REASONS + '. Sắp xếp được.'),
    ('Trạng thái phiếu', 'Badge', 'Read-only', 'Đã duyệt / Hoàn tất', 'Theo dữ liệu', STATUS_TEXT + ' Sắp xếp được.'),
    ('Công việc của tôi', 'Text', 'Read-only', '≥ 1', 'Theo dữ liệu',
     '“<n> công việc” + ✓ đã nhận (xanh lá), ✗ từ chối nhận (đỏ), đồng hồ chờ nhận (cam) — chỉ đếm công việc của tôi.'),
    ('Ngày bàn giao', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Sắp xếp được.'),
    ('Ngày TP duyệt', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Sắp xếp được (mặc định giảm dần).'),
    ('Người duyệt', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Ghi chú', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng.'),
    ('Người tạo phiếu / Ngày tạo', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Ngày tạo sắp xếp được.'),
    ('Hành động', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Cột cuối, khoá: Tiếp nhận (mở FR-07) · Lịch sử (FR-06).'),
    ('Phân trang', 'Pagination', 'Enable', '10/20/50/100', '20 dòng/trang', '–'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có phiếu bàn giao nào chờ bạn tiếp nhận.”'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n' + NO_LOGIN + '\nAfter:\n– Nạp phiếu theo BR-01, cấu hình cột và danh mục ô lọc.\n'
     '– Lỗi → “Lỗi khi tải dữ liệu”.'),
    ('Bấm tiêu đề cột sắp xếp / đổi trang', 'Click', 'After:\n– Nạp lại dữ liệu theo sắp xếp / trang mới.'),
    ('Bấm Mã phiếu hoặc Tiếp nhận', 'Click', 'After:\n– Mở màn Xác nhận tiếp nhận công việc của phiếu.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Chờ tiếp nhận bàn giao.',
           anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc phiếu chờ tiếp nhận',
    mota='Tìm nhanh theo mã phiếu / tên người bàn giao; lọc theo Mã phiếu, Lý do, Người bàn giao, Dự án, Giải pháp, '
         'Hạng mục.',
    tacnhan='Người nhận bàn giao',
    dieukien='Đang ở màn Chờ tiếp nhận bàn giao.',
    chinh='1. Gõ từ khoá vào ô tìm nhanh rồi bấm “Tìm kiếm” hoặc Enter.\n'
          '2. Bấm “Tìm kiếm nâng cao” để mở các ô lọc.\n'
          '3. Chọn giá trị ở ô chọn → hệ thống tìm ngay; ô Mã phiếu gõ tay → bấm Tìm kiếm.\n'
          '4. Bấm “Làm mới” để xoá điều kiện.',
    phu='• Đổi Dự án → xoá Giải pháp và Hạng mục đang chọn; đổi Giải pháp → xoá Hạng mục.\n'
        '• Giải pháp chỉ liệt kê giải pháp của dự án đang chọn; Hạng mục chỉ có khi đã chọn Giải pháp.\n'
        '• Dự án / Giải pháp / Hạng mục lọc theo công việc của tôi trong phiếu.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-loc.png'), shot_caption='Khối Tìm kiếm nâng cao đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Gợi ý “Tìm theo mã phiếu, tên người bàn giao”.'),
    ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Mã phiếu', 'Textbox', 'Enable', '–', 'Không', 'Trống', 'Tìm gần đúng theo mã phiếu.'),
    ('Lý do bàn giao', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống', REASONS + '.'),
    ('Người bàn giao', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Người bàn giao của các phiếu có công việc giao cho tôi; “Tên - Mã phòng - Mã nhân viên”.'),
    ('Dự án', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Dự án của công việc của tôi.'),
    ('Giải pháp', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Lọc theo Dự án đang chọn.'),
    ('Hạng mục', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Chỉ có danh sách khi đã chọn Giải pháp.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm / Enter', 'Click / Keypress', 'After:\n– Về trang 1, nạp lại theo từ khoá và ô lọc.'),
    ('Chọn giá trị ô chọn', 'Change', 'After:\n– Tự tìm ngay, về trang 1. Ô Mã phiếu và ô tìm nhanh không tự tìm.'),
    ('Đổi Dự án / Giải pháp', 'Change', 'After:\n– Xoá ô con phụ thuộc (Giải pháp, Hạng mục) rồi tìm lại.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện và sắp xếp, nạp lại đúng 1 lần.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Cài đặt bộ lọc')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc. Chỉ bổ sung các quy tắc riêng của màn Chờ tiếp nhận bàn giao.', anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Chọn ô lọc hiển thị và thứ tự các ô trong khối Tìm kiếm nâng cao.',
    tacnhan='Người nhận bàn giao',
    dieukien='Đang ở màn Chờ tiếp nhận bàn giao.',
    chinh='1. Bấm “Cài đặt bộ lọc”.\n2. Tích / bỏ tích, kéo ⠿ để đổi thứ tự 6 trường.\n3. Bấm “Lưu”.',
    phu='• “Khôi phục mặc định” → về 6 trường theo thứ tự gốc.\n• “Đóng” → không lưu.')
d.p('2.3.2 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', modal='Cài đặt bộ lọc', shot=shot('03-caidat.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', '–'),
    ('Danh sách trường lọc', 'Checkbox', 'Enable', '6 trường', 'Không', 'Tích hết',
     '1. Mã phiếu · 2. Lý do bàn giao · 3. Người bàn giao · 4. Dự án · 5. Giải pháp · 6. Hạng mục.'),
    ('Nút Lưu / Khôi phục mặc định / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click', 'After:\n– Lưu cài đặt theo tài khoản cho màn này; khối lọc hiển thị lại.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Trả về cài đặt gốc.'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Tuỳ chỉnh cột')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Chờ tiếp nhận bàn giao.',
           anchor='excel')
d.intro_table(
    ten='Tuỳ chỉnh cột',
    mota='Ẩn / hiện và sắp xếp các cột của bảng phiếu chờ tiếp nhận.',
    tacnhan='Người nhận bàn giao',
    dieukien='Đang ở màn Chờ tiếp nhận bàn giao.',
    chinh='1. Bấm nút Tuỳ chỉnh cột.\n2. Tích / bỏ tích, kéo ≡ để đổi thứ tự.\n3. Bấm “Lưu”.',
    phu='• Cột khoá STT, Mã phiếu, Hành động không bỏ tích / kéo được.\n• “Đóng” → không lưu.')
d.p('2.4.2 Layout màn hình')
d.layout(menu=MENU + ' => Tuỳ chỉnh cột', modal='Tuỳ chỉnh cột', shot=shot('04-cot.png'),
         shot_caption='Cửa sổ Tuỳ chỉnh cột')
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Cột khoá', 'Checkbox', 'Disable', '3 cột', '–', 'Tích', 'STT, Mã phiếu, Hành động — có biểu tượng ổ khoá.'),
    ('Các cột còn lại', 'Checkbox', 'Enable', '11 cột', 'Không', 'Tích hết',
     'Người bàn giao, Phòng ban, Lý do bàn giao, Trạng thái phiếu, Công việc của tôi, Ngày bàn giao, Ngày TP duyệt, '
     'Người duyệt, Ghi chú, Người tạo phiếu, Ngày tạo.'),
    ('Nút Lưu / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình cột theo tài khoản (trên máy chủ); bảng cập nhật ngay.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Xuất Excel')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Xuất Excel', 'action', actor=A)
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Chờ tiếp nhận bàn giao.',
           anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách phiếu chờ tiếp nhận',
    mota='Xuất toàn bộ phiếu khớp bộ lọc đang áp dụng ra file Excel với các cột người dùng chọn.',
    tacnhan='Người nhận bàn giao',
    dieukien='Đang ở màn Chờ tiếp nhận bàn giao.',
    chinh='1. Bấm “Xuất Excel”.\n2. Cửa sổ “Chọn trường xuất file” tích sẵn các cột đang hiện.\n'
          '3. Chọn / sắp xếp trường rồi bấm “Xuất file”.\n'
          '4. Tải về danh_sach_phieu_cho_tiep_nhan.xlsx, báo “Xuất Excel thành công”.',
    phu='• Không tích trường nào → nút Xuất file bị khoá.\n• Lỗi → “Lỗi khi xuất Excel”.',
    dacbiet='Theo đúng bộ lọc + sắp xếp, bỏ phân trang; số liệu công việc là công việc của tôi.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất file', shot=shot('05-xuat.png'),
         shot_caption='Cửa sổ Chọn trường xuất file')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Danh sách trường', 'Checkbox', 'Enable', '15 trường', 'Có (≥ 1)', 'Các cột đang hiện',
     'Mã phiếu, Người bàn giao, Phòng ban, Lý do bàn giao, Trạng thái phiếu, Công việc của tôi, Đã nhận, Từ chối nhận, '
     'Chờ nhận, Ngày bàn giao, Ngày TP duyệt, Người duyệt, Ghi chú, Người tạo phiếu, Ngày tạo. Kéo ≡ đổi thứ tự.'),
    ('Bộ đếm', 'Label', 'Hiển thị', '–', '–', 'Theo số trường', '“Đang chọn x/15 trường”.'),
    ('Nút Xuất file / Đóng', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Xuất file khoá khi chưa chọn trường.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất file', 'Click',
     'Before:\n' + NO_LOGIN + '\nAfter:\n– Lấy tất cả phiếu khớp bộ lọc theo BR-01, tải file '
     'danh_sach_phieu_cho_tiep_nhan.xlsx tiêu đề “Danh sách phiếu chờ tiếp nhận”.\n'
     '– “Xuất Excel thành công”; lỗi → “Lỗi khi xuất Excel”.'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Xem lịch sử phiếu')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn Chờ tiếp nhận bàn giao.', anchor='history')
d.intro_table(
    ten='Xem lịch sử phiếu bàn giao',
    mota='Dòng thời gian các thao tác trên phiếu (tạo, gửi duyệt, duyệt, tiếp nhận / từ chối từng công việc, hoàn tất).',
    tacnhan='Người nhận bàn giao',
    dieukien='Phiếu có trong danh sách chờ tiếp nhận.',
    chinh='1. Bấm biểu tượng Lịch sử ở cột Hành động.\n'
          '2. Cửa sổ “Lịch sử phiếu bàn giao” hiện dòng “Phiếu bàn giao: <mã> - <người bàn giao>” và dòng thời gian '
          'mới nhất ở trên.\n3. Bấm “Bộ lọc” để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.',
    phu='• Chưa có lịch sử → “Chưa có lịch sử thao tác nào.”\n• Lọc không ra → “Không có lịch sử phù hợp bộ lọc.”')
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử', modal='Lịch sử phiếu bàn giao', shot=shot('06-lichsu.png'),
         shot_caption='Cửa sổ Lịch sử phiếu bàn giao')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề / dòng nhận diện', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     '“Lịch sử phiếu bàn giao” · “Phiếu bàn giao: <mã> - <người bàn giao>”.'),
    ('Nút Bộ lọc + 4 ô lọc', 'Button / Dropdown / Datepicker', 'Enable', '–', 'Thu gọn',
     'Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.'),
    ('Mục lịch sử', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Thời điểm · tên hành động (Nghiệm thu hạng mục = tiếp nhận công việc; Từ chối hạng mục = từ chối tiếp nhận) · '
     'Người thực hiện — phòng ban · nội dung.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lịch sử', 'Click', 'After:\n– Nạp lịch sử phiếu, mới nhất trước; không gắn quyền riêng.'),
    ('Chọn ô lọc', 'Change', 'After:\n– Lọc ngay danh sách đã nạp.'),
])

# ------------------------------------------------------------------ 2.7
d.h3('2.7 Xem phiếu cần tiếp nhận')
d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Chờ tiếp nhận bàn giao.',
           anchor='detail')
d.intro_table(
    ten='Xem phiếu cần tiếp nhận',
    mota='Màn “Xác nhận tiếp nhận công việc”: thông tin chung của phiếu và CHỈ các công việc giao cho người đăng nhập, '
         'kèm cột Xác nhận.',
    tacnhan='Người nhận bàn giao',
    dieukien='Người dùng mở phiếu từ danh sách chờ tiếp nhận.',
    chinh='1. Bấm Mã phiếu hoặc nút Tiếp nhận.\n'
          '2. Hệ thống mở màn “Xác nhận tiếp nhận công việc”.\n'
          '3. Người dùng xem công việc theo tab Nhiệm vụ / Vấn đề, gom theo dự án; cột Xác nhận cho biết trạng thái '
          'từng công việc.\n'
          '4. Bấm “Quay lại”: nếu còn công việc chờ nhận → hộp “Chưa xử lý hết công việc”; hết → về danh sách.',
    phu='• Không tải được phiếu → “Lỗi tải phiếu bàn giao”, về danh sách chờ tiếp nhận.\n'
        '• Hộp “Chưa xử lý hết công việc”: “Bạn chưa xử lý hết các công việc được bàn giao. Bạn muốn tiếp tục xác nhận '
        'hay về màn danh sách?” · “Tiếp tục xác nhận” (ở lại màn) / “Về màn danh sách”.')
d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU_TN, shot=shot('07-tiep-nhan.png'), shot_caption='Màn Xác nhận tiếp nhận công việc')
d.figure(shot('07b-tiep-nhan-xacnhan.png'), 'Cột Xác nhận ở cuối bảng', width_in=6.2)
d.figure(shot('12-canh-bao-quay-lai.png'), 'Hộp cảnh báo khi Quay lại lúc còn công việc chờ nhận', width_in=6.2)
d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Xác nhận tiếp nhận công việc', '–'),
    ('Khối Thông tin bàn giao', 'Card', 'Read-only', '–', 'Theo dữ liệu',
     'Badge trạng thái; Mã phiếu, Ngày bàn giao, Người bàn giao (phòng ban), Người nhận bàn giao, Lý do, Người duyệt, '
     'Ngày duyệt, Ghi chú.'),
    ('Tab Nhiệm vụ (n) / Vấn đề (n)', 'Button', 'Enable', '–', 'Nhiệm vụ', 'Chỉ đếm công việc của tôi.'),
    ('Nút Tiếp nhận tất cả (n)', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Hiện khi tab đang xem còn n công việc chờ nhận. Xem FR-09.'),
    ('Bảng công việc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'STT, Mã • Tên (bấm mở FR-11), Người giao, Trạng thái, Ưu tiên, Tiến độ % (nhiệm vụ), Hạn hoàn thành, '
     'Người nhận BG, Ghi chú BG, Xác nhận.'),
    ('Cột Xác nhận', 'Button / Badge', 'Enable / Read-only', '–', 'Theo dữ liệu',
     'Chờ nhận: nút “Nhận” và “Từ chối”. Đã nhận: nhãn xanh “Đã nhận”. Từ chối: nhãn đỏ “Từ chối” + lý do.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về danh sách chờ tiếp nhận (có cảnh báo nếu còn chờ nhận).'),
    ('Hộp Chưa xử lý hết công việc', 'Modal', 'Hiển thị', '–', 'Ẩn',
     'Nút “Tiếp tục xác nhận” / “Về màn danh sách”.'),
], required=False)
d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn', 'System',
     'Before:\n' + NO_LOGIN + '\nAfter:\n– Nạp phiếu, lọc chỉ công việc có Người nhận BG là người đăng nhập.\n'
     '– Lỗi → “Lỗi tải phiếu bàn giao”, về danh sách chờ tiếp nhận.'),
    ('Bấm Quay lại', 'Click',
     'After:\n– Còn công việc chờ nhận → mở hộp “Chưa xử lý hết công việc”; không còn → về danh sách.'),
    ('Bấm Tiếp tục xác nhận / Về màn danh sách', 'Click',
     'After:\n– Tiếp tục xác nhận: đóng hộp, ở lại màn.\n– Về màn danh sách: về danh sách chờ tiếp nhận.'),
])

# ------------------------------------------------------------------ 2.8
AFTER_ACCEPT = ('– Công việc chuyển “Đã nhận”, lưu thời điểm nhận; người thực hiện của nhiệm vụ / vấn đề chuyển sang '
                'người nhận.\n'
                '– Ghi lịch sử “<tên> đã tiếp nhận <mã công việc>”.\n')
COMPLETE = ('– Nếu phiếu không còn công việc chờ nhận → phiếu chuyển Hoàn tất, ghi lịch sử “Phiếu bàn giao đã hoàn '
            'tất.”, gửi thông báo “Phiếu bàn giao hoàn tất” — “Phiếu bàn giao <mã> đã hoàn tất.” cho người lập phiếu '
            'và trưởng phòng đã duyệt.\n')
GUARD = ('During:\n– Không phải người nhận → “Bạn không phải người nhận của mục này”.\n'
         '– Công việc đã xử lý → “Mục này đã được xử lý”.\n'
         '– Phiếu không ở trạng thái Đã duyệt → “Phiếu bàn giao chưa được duyệt”.\n'
         '– Nếu có lỗi → không thực hiện bước After.\n')

d.h3('2.8 Tiếp nhận công việc')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Tiếp nhận công việc', 'action', actor=A)
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='notice')
d.intro_table(
    ten='Tiếp nhận công việc',
    mota='Người nhận xác nhận nhận 1 công việc; nhiệm vụ / vấn đề được chuyển sang cho người nhận thực hiện.',
    tacnhan='Người nhận bàn giao',
    dieukien='Phiếu Đã duyệt; công việc giao cho người đăng nhập và đang Chờ nhận.',
    chinh='1. Người dùng bấm “Nhận” ở cột Xác nhận.\n'
          '2. Hệ thống ghi nhận ngay (không hỏi xác nhận), báo “Đã tiếp nhận công việc”.\n'
          '3. Cột Xác nhận đổi thành nhãn “Đã nhận”.',
    phu='• Lỗi → nội dung lỗi hoặc “Lỗi tiếp nhận”.',
    dacbiet='Công việc cuối cùng của phiếu được xử lý → phiếu tự chuyển Hoàn tất (BR-03).')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU_TN + ' => Nhận', shot=shot('08-da-tiep-nhan.png'),
         shot_caption='Sau khi bấm Nhận — công việc chuyển “Đã nhận”')
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Nhận', 'Button', 'Enable / Ẩn', 'Hiển thị khi Chờ nhận', 'Viền xanh, biểu tượng ✓.'),
    ('Nhãn Đã nhận', 'Badge', 'Read-only', 'Ẩn', 'Nền xanh “Đã nhận” sau khi tiếp nhận.'),
    ('Toast kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn', '“Đã tiếp nhận công việc” / lỗi.'),
], required=False, scope=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Nhận', 'Click',
     'Before:\n' + NO_LOGIN + '\n' + GUARD + 'After:\n' + AFTER_ACCEPT +
     '– Gửi thông báo “Công việc đã được tiếp nhận” — “<tên> đã tiếp nhận <mã>” cho người lập phiếu.\n' + COMPLETE +
     '– “Đã tiếp nhận công việc”, nạp lại màn.'),
])

# ------------------------------------------------------------------ 2.9
d.h3('2.9 Tiếp nhận tất cả')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Tiếp nhận tất cả', 'action', actor=A)
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='notice')
d.intro_table(
    ten='Tiếp nhận tất cả',
    mota='Tiếp nhận một lần mọi công việc đang Chờ nhận của tab đang xem (Nhiệm vụ hoặc Vấn đề).',
    tacnhan='Người nhận bàn giao',
    dieukien='Phiếu Đã duyệt; tab đang xem còn ít nhất 1 công việc của tôi Chờ nhận.',
    chinh='1. Bấm “Tiếp nhận tất cả (n)”.\n'
          '2. Hộp “Tiếp nhận tất cả”: “Bạn có chắc muốn tiếp nhận tất cả n nhiệm vụ đang chờ?” (tab Vấn đề: “… n vấn đề '
          'đang chờ?”).\n3. Bấm “Tiếp nhận tất cả”.\n'
          '4. Hệ thống báo “Đã tiếp nhận tất cả nhiệm vụ” (hoặc “… vấn đề”) và nạp lại màn.',
    phu='• “Hủy” → không thay đổi.\n• Không còn công việc chờ → “Không có mục nào cần tiếp nhận”.\n'
        '• Lỗi khác → nội dung lỗi hoặc “Lỗi tiếp nhận”.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU_TN + ' => Tiếp nhận tất cả', shot=shot('09-tiep-nhan-tat-ca.png'),
         shot_caption='Hộp xác nhận Tiếp nhận tất cả')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Tiếp nhận tất cả (n)', 'Button', 'Enable / Ẩn', 'Ẩn khi n = 0', 'Theo tab đang xem.'),
    ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Tiếp nhận tất cả', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu', '“Bạn có chắc muốn tiếp nhận tất cả n nhiệm vụ|vấn đề đang chờ?”'),
    ('Nút Tiếp nhận tất cả / Hủy', 'Button', 'Enable', 'Hiển thị', '–'),
], required=False, scope=False)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tiếp nhận tất cả ở hộp', 'Click',
     'Before:\n' + NO_LOGIN + '\n'
     'During:\n– Phiếu không Đã duyệt → “Phiếu bàn giao chưa được duyệt”.\n'
     '– Không còn công việc chờ của tôi thuộc loại đang chọn → “Không có mục nào cần tiếp nhận”.\n'
     'After:\n– Với từng công việc chờ nhận của tôi thuộc loại đang chọn:\n' + AFTER_ACCEPT +
     '– Gửi 1 thông báo “Công việc đã được tiếp nhận” — “<tên> đã tiếp nhận n task|issue từ phiếu bàn giao <mã>” '
     'cho người lập phiếu.\n' + COMPLETE + '– “Đã tiếp nhận tất cả nhiệm vụ|vấn đề”, nạp lại màn.'),
])

# ------------------------------------------------------------------ 2.10
d.h3('2.10 Từ chối tiếp nhận')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Từ chối tiếp nhận', 'action', actor=A)
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu, Thông báo. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Từ chối tiếp nhận',
    mota='Người nhận từ chối 1 công việc kèm lý do; công việc được chuyển cho trưởng phòng đã duyệt phiếu.',
    tacnhan='Người nhận bàn giao',
    dieukien='Phiếu Đã duyệt; công việc giao cho người đăng nhập và đang Chờ nhận.',
    chinh='1. Bấm “Từ chối” ở cột Xác nhận.\n'
          '2. Hộp “Từ chối tiếp nhận” — “Vui lòng nhập lý do từ chối (tối thiểu 10 ký tự):”.\n'
          '3. Nhập Lý do từ chối, bấm “Từ chối”.\n'
          '4. Hệ thống báo “Đã từ chối tiếp nhận”; cột Xác nhận hiện nhãn đỏ “Từ chối” + lý do.',
    phu='• Lý do dưới 10 ký tự → “Lý do từ chối phải có tối thiểu 10 ký tự”, hộp đóng, không gửi (bấm Từ chối lại để '
        'nhập).\n• Lỗi → nội dung lỗi hoặc “Lỗi từ chối”.',
    dacbiet='Nhiệm vụ / vấn đề bị từ chối chuyển người thực hiện sang trưởng phòng đã duyệt phiếu.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU_TN + ' => Từ chối', shot=shot('10-tu-choi.png'), shot_caption='Hộp Từ chối tiếp nhận')
d.figure(shot('10b-tu-choi-ngan.png'), 'Lý do dưới 10 ký tự', width_in=6.2)
d.figure(shot('10c-da-tu-choi.png'), 'Công việc đã từ chối hiển thị lý do', width_in=6.2)
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp', 'Label', 'Hiển thị', '–', '–', 'Từ chối tiếp nhận', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Vui lòng nhập lý do từ chối (tối thiểu 10 ký tự):”'),
    ('Lý do từ chối', 'Textarea', 'Enable', '10–1000 ký tự', 'Có', 'Trống', 'Gợi ý “Nhập lý do...”.'),
    ('Nút Từ chối / Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nhãn Từ chối + lý do', 'Badge', 'Read-only', '–', '–', 'Ẩn', 'Hiện ở cột Xác nhận sau khi từ chối.'),
])
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Từ chối ở hộp', 'Click',
     'Before:\n' + NO_LOGIN + '\n– Lý do trống / < 10 ký tự → “Lý do từ chối phải có tối thiểu 10 ký tự”, dừng.\n'
     + GUARD.replace('– Nếu có lỗi', '– Lý do > 1000 ký tự → “Lý do từ chối không được vượt quá 1000 ký tự”.\n'
                     '– Phiếu thiếu người duyệt → “Phiếu bàn giao thiếu thông tin người duyệt — vui lòng liên hệ quản '
                     'trị viên”.\n– Nếu có lỗi') +
     'After:\n– Công việc chuyển “Từ chối”, lưu lý do và thời điểm.\n'
     '– Người thực hiện của nhiệm vụ / vấn đề chuyển sang trưởng phòng đã duyệt phiếu.\n'
     '– Ghi lịch sử “<tên> từ chối tiếp nhận <mã>. Lý do: … . Nhiệm vụ được chuyển sang <TP>”.\n'
     '– Thông báo “Công việc bị từ chối tiếp nhận” — “<tên> từ chối tiếp nhận <mã>. Lý do: …” cho người lập phiếu; '
     '“Bạn vừa được giao công việc” — “Bạn vừa được giao <mã> do <tên> từ chối tiếp nhận từ phiếu bàn giao <mã phiếu>” '
     'cho trưởng phòng.\n' + COMPLETE + '– “Đã từ chối tiếp nhận”, nạp lại màn.'),
])

# ------------------------------------------------------------------ 2.11
d.h3('2.11 Xem chi tiết nhiệm vụ / vấn đề')
d.p('2.11.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết. Chỉ bổ sung các quy tắc riêng của màn Chờ tiếp nhận bàn giao.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết nhiệm vụ / vấn đề',
    mota='Xem đủ thông tin công việc trước khi quyết định tiếp nhận hay từ chối.',
    tacnhan='Người nhận bàn giao',
    dieukien='Đang ở màn Xác nhận tiếp nhận công việc.',
    chinh='1. Bấm mã hoặc tên công việc.\n'
          '2. Nhiệm vụ → cửa sổ “<mã> — Chi tiết nhiệm vụ” (chế độ nâng cao); Vấn đề → cửa sổ chi tiết vấn đề chỉ đọc.\n'
          '3. Bấm “Đóng” để quay lại.',
    phu='• Đóng cửa sổ không ảnh hưởng trạng thái tiếp nhận.')
d.p('2.11.2 Layout màn hình')
d.layout(menu=MENU_TN, modal='chi tiết nhiệm vụ', shot=shot('11-chi-tiet-nhiem-vu.png'),
         shot_caption='Cửa sổ chi tiết nhiệm vụ')
d.p('2.11.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“<mã> — Chi tiết nhiệm vụ” + badge trạng thái.'),
    ('Các trường nhiệm vụ / vấn đề', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Đặc tả tại SRS - Nhiệm vụ / SRS - Vấn đề.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '–'),
], required=False)
d.p('2.11.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm mã / tên công việc', 'Click', 'After:\n– Mở cửa sổ chi tiết theo loại công việc.'),
    ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ==================================================== PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Chờ tiếp nhận bàn giao; không lặp lại các quy tắc đã có '
           'trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phiếu hiện trong danh sách', [
        '– Phiếu Đã duyệt hoặc Hoàn tất có ít nhất 1 công việc Người nhận BG = người đăng nhập (khớp bộ lọc Dự án / '
        'Giải pháp / Hạng mục nếu có).',
        '– Phiếu đã xử lý xong vẫn hiện (trạng thái Hoàn tất hoặc số Chờ nhận = 0).',
        '– Số công việc ở cột “Công việc của tôi” và file Excel chỉ đếm công việc của người đăng nhập.',
    ], ['Xem danh sách', 'Tìm kiếm và lọc', 'Xuất Excel']),
    ('BR-02', 'Chuyển người thực hiện', [
        '– Tiếp nhận: người thực hiện của nhiệm vụ / vấn đề = người nhận.',
        '– Từ chối: người thực hiện = trưởng phòng đã duyệt phiếu.',
        '– Mỗi công việc chỉ xử lý 1 lần (Chờ nhận → Đã nhận hoặc Từ chối), chỉ người nhận được xử lý, chỉ khi phiếu '
        'Đã duyệt.',
    ], ['Tiếp nhận', 'Tiếp nhận tất cả', 'Từ chối tiếp nhận']),
    ('BR-03', 'Phiếu tự Hoàn tất', [
        '– Sau mỗi lần tiếp nhận / từ chối, nếu phiếu không còn công việc Chờ nhận (của mọi người nhận) → phiếu chuyển '
        'Hoàn tất, thông báo cho người lập và trưởng phòng đã duyệt.',
    ], ['Tiếp nhận', 'Tiếp nhận tất cả', 'Từ chối tiếp nhận']),
    ('BR-04', 'Lý do từ chối', ['– 10–1000 ký tự; hiển thị ở cột Xác nhận và trong lịch sử phiếu.'],
     'Từ chối tiếp nhận'),
    ('BR-05', 'Thông báo', [
        '– Tiếp nhận 1 công việc / tiếp nhận tất cả → người lập phiếu.',
        '– Từ chối → người lập phiếu + trưởng phòng đã duyệt (được giao lại công việc).',
        '– Hoàn tất → người lập phiếu + trưởng phòng đã duyệt.',
    ], ['Tiếp nhận', 'Tiếp nhận tất cả', 'Từ chối tiếp nhận']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

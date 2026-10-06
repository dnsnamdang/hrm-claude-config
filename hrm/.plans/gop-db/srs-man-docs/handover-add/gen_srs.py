# -*- coding: utf-8 -*-
"""Sinh "SRS - Tạo bàn giao.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/handover/add.vue · components/{HandoverForm,HandoverItemsTable}.vue · utils/handoverProgress.js
      pages/assign/tasks/components/CreateTaskModal.vue · pages/assign/issues/components/CreateIssueModal.vue
      components/V2Footer.vue · components/modal/base-confirm-modal.vue
      components/menu-sidebar.js (menuItemsAssign › Nhiệm vụ › Tạo bàn giao)
  BE  Modules/Assign/Routes/api.php (assign/handovers: available-items, store, update, submit — không gắn quyền)
      Http/Controllers/Api/V1/HandoverController.php · Services/HandoverService.php
      (getAvailableItems, getReceiverOptionsFromSolutions, getReceiverOptionsPerModule, store, update, syncItems,
      submit, sendNotificationToApprovers) · Http/Requests/Handover/HandoverRequest.php · Entities/Handover.php
Ảnh: shots/ (Playwright headless 1440x900, client :3002). Dữ liệu mẫu: data_created.md.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'handover'))
from _hcommon import new_doc, extra_menu, NO_LOGIN, REASONS, TERMS  # noqa: E402

TEN_MAN = 'Tạo bàn giao'
MENU = 'Phân hệ Công việc => Nhiệm vụ => Tạo bàn giao'
MENU_B = 'Phân hệ Công việc => Nhiệm vụ => Phiếu bàn giao => Tạo phiếu'

ICONS = {
    'Phân hệ Công việc': 'icon_phanhe.png',
    'Nhiệm vụ': 'icon_nhiemvu.png',
    'Tạo bàn giao': 'icon_man.png',
    'Phiếu bàn giao': 'icon_phieubangiao.png',
    'Tạo phiếu': 'icon_taophieu.png',
    'Vấn đề': 'icon_tab_vd.png',
    'Gán': 'icon_gan.png',
    'Gán hàng loạt': 'icon_ganhangloat.png',
    'Bỏ khỏi danh sách': 'icon_bo.png',
    'Lưu nháp': 'icon_luunhap.png',
    'Lưu và gửi': 'icon_luuvagui.png',
}
d, shot = new_doc(HERE, TEN_MAN, MENU, 'hda_', ICONS)
A = 'Người lập phiếu'


def lay(suffix, png, caption, modal=None):
    d.layout(menu=MENU + suffix)
    extra_menu(d, MENU_B + suffix)
    if modal:
        d.p('Cửa sổ %s được mở ngay trên màn Tạo phiếu bàn giao theo một trong hai đường dẫn ở trên.' % modal)
    d.figure(shot(png), caption, width_in=6.2)


RECV = ('Nhân sự liên quan tới giải pháp của công việc: PM, người tạo giải pháp, thành viên giải pháp, trưởng và thành '
        'viên các hạng mục. Công việc có hạng mục → chỉ trưởng + thành viên hạng mục đó. Luôn bỏ chính người lập. '
        'Hiển thị “Tên nhân viên - Mã phòng - Mã nhân viên”.')

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Tạo phiếu bàn giao (phân hệ Công việc), nơi nhân viên lập phiếu '
    'bàn giao các nhiệm vụ / vấn đề mình đang phụ trách cho người khác trước khi nghỉ việc, chuyển phòng ban, nghỉ dài '
    'hạn…, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu: nạp danh sách công việc cần bàn giao, nhập thông tin phiếu, chọn người nhận (từng dòng, '
    'theo dự án, hàng loạt), cập nhật tiến độ và ghi chú, bỏ công việc khỏi danh sách, xem chi tiết công việc, '
    'lưu nháp và lưu – gửi trưởng phòng duyệt.',
    'Làm rõ công việc nào được đưa vào phiếu và ai được chọn làm người nhận.',
    'Các bước sau khi gửi (duyệt, tiếp nhận) đặc tả tại “SRS - Phiếu bàn giao” và “SRS - Chờ tiếp nhận bàn giao”.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], TERMS, widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('–', 'Không gắn quyền riêng',
     'Mọi người dùng đã đăng nhập đều thấy menu “Tạo bàn giao” và lập được phiếu cho chính công việc của mình. '
     'Người lập phiếu luôn là người đang đăng nhập.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn không phân quyền theo cấp tổ chức: chỉ nạp nhiệm vụ / vấn đề đang giao cho chính người đăng nhập (BR-01).')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người dùng đã đăng nhập (không có quyền nào)'], [
    ('FR-01 Xem danh sách công việc cần bàn giao', '✅'),
    ('FR-02 Nhập thông tin bàn giao', '✅'),
    ('FR-03 Chọn người nhận bàn giao', '✅'),
    ('FR-04 Cập nhật tiến độ và ghi chú bàn giao', '✅'),
    ('FR-05 Bỏ công việc khỏi danh sách', '✅'),
    ('FR-06 Xem chi tiết nhiệm vụ / vấn đề', '✅'),
    ('FR-07 Lưu nháp phiếu bàn giao', '✅'),
    ('FR-08 Lưu và gửi duyệt', '✅'),
], widths=[3.6, 2.4])

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A, [0, 1, 2, 3, 4, 5, 6])],
    [('FR-01', 'Xem công việc cần bàn giao', 'view'),
     ('FR-02', 'Nhập thông tin bàn giao', 'crud'),
     ('FR-03', 'Chọn người nhận bàn giao', 'crud'),
     ('FR-04', 'Cập nhật tiến độ, ghi chú', 'crud'),
     ('FR-05', 'Bỏ công việc khỏi danh sách', 'action'),
     ('FR-07', 'Lưu nháp', 'crud'),
     ('FR-08', 'Lưu và gửi duyệt', 'action')],
    [('FR-06', 'Xem chi tiết nhiệm vụ / vấn đề', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)
d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách công việc cần bàn giao')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách và UI/UX. Chỉ bổ sung các quy tắc riêng của màn Tạo bàn giao tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Xem danh sách công việc cần bàn giao',
    mota='Khi mở màn, hệ thống tự nạp toàn bộ nhiệm vụ / vấn đề đang giao cho người đăng nhập và chưa nằm trong phiếu '
         'bàn giao nào chưa hoàn tất; chia 2 tab Nhiệm vụ / Vấn đề và gom theo dự án.',
    tacnhan='Người lập phiếu; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập.',
    chinh='1. Người dùng vào menu Tạo bàn giao (hoặc bấm “Tạo phiếu” ở màn Phiếu bàn giao).\n'
          '2. Hệ thống mở màn tiêu đề “Tạo phiếu bàn giao” gồm khối Thông tin bàn giao và khối Danh sách cần bàn giao.\n'
          '3. Hệ thống nạp công việc của người dùng (BR-01) và danh sách người nhận hợp lệ cho từng giải pháp / hạng mục.\n'
          '4. Người dùng chuyển tab “Nhiệm vụ (n)” / “Vấn đề (n)”.',
    phu='• Không có công việc ở tab → “Không có nhiệm vụ nào.” / “Không có vấn đề nào.”\n'
        '• Lỗi tải → “Lỗi tải danh sách công việc”.')
d.p('2.1.2 Layout màn hình')
lay('', '01-tao.png', 'Màn Tạo phiếu bàn giao — tab Nhiệm vụ')
d.figure(shot('02-tab-vande.png'), 'Tab Vấn đề', width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Tạo phiếu bàn giao', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', 'Hiển thị',
     '“Chọn công việc cần bàn giao, chỉ định người nhận cho từng mục.”'),
    ('Khối Thông tin bàn giao', 'Card', 'Enable', '–', 'Trống', 'Xem FR-02.'),
    ('Tiêu đề khối Danh sách cần bàn giao', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Kèm dòng “Công việc của <họ tên người đăng nhập>”.'),
    ('Tab Nhiệm vụ (n) / Vấn đề (n)', 'Button', 'Enable', '–', 'Nhiệm vụ', 'n = số dòng của tab.'),
    ('Thống kê', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Tổng x — Đã gán y” của tab đang chọn.'),
    ('Dòng nhóm dự án', 'Table/Grid', 'Read-only', 'Đánh số La Mã', 'Theo dữ liệu',
     'Tên dự án (không có → “Không có dự án”) + “(n mục)” + ô chọn người nhận và nút Gán (FR-03).'),
    ('Cột chọn dòng', 'Checkbox', 'Enable', '–', 'Bỏ chọn', 'Tiêu đề cột có ô chọn tất cả của tab.'),
    ('Cột STT', 'Text', 'Read-only', '≥ 1', 'Theo dữ liệu', 'Đánh số trong từng nhóm dự án.'),
    ('Cột Mã • Tên', 'Link', 'Read-only', '–', 'Theo dữ liệu', 'Bấm mở chi tiết nhiệm vụ / vấn đề (FR-06).'),
    ('Cột Người giao', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Người tạo nhiệm vụ / vấn đề.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', '–', 'Theo dữ liệu', 'Trạng thái hiện tại của nhiệm vụ / vấn đề.'),
    ('Cột Ưu tiên', 'Badge', 'Read-only', '–', 'Theo dữ liệu',
     'Nhiệm vụ: Bình thường / Cao / Khẩn cấp; Vấn đề: Thấp / Trung bình / Cao / Khẩn cấp.'),
    ('Cột Tiến độ %', 'Number', 'Enable', '0 – 100', 'Tiến độ hiện tại', 'Chỉ tab Nhiệm vụ. Xem FR-04.'),
    ('Cột Hạn hoàn thành', 'Text', 'Read-only', 'dd/mm/yyyy + giờ', 'Theo dữ liệu', 'Không có hạn → “—”.'),
    ('Cột Người nhận BG', 'Dropdown', 'Enable', 'Danh sách', '-- Chọn --', 'Xem FR-03.'),
    ('Cột Ghi chú BG', 'Textbox', 'Enable', '0–500 ký tự', 'Trống', 'Xem FR-04.'),
    ('Cột Bỏ khỏi danh sách', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Dấu × đỏ. Xem FR-05.'),
    ('Nút Lưu nháp / Lưu và gửi / Quay lại', 'Button', 'Enable', '–', 'Hiển thị',
     'Thanh nút ghim đáy màn. Quay lại → về danh sách phiếu bàn giao.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n' + NO_LOGIN + '\n'
     'After:\n– Nạp nhiệm vụ đang giao cho người đăng nhập, trạng thái khác Nháp / Hoàn thành / Huỷ; vấn đề đang giao '
     'cho người đăng nhập, trạng thái khác Mới ghi nhận / Đã đóng; bỏ những công việc đang nằm trong phiếu chưa '
     'Hoàn tất.\n– Nạp danh sách người nhận hợp lệ theo giải pháp và hạng mục.\n'
     '– Lỗi → “Lỗi tải danh sách công việc”.'),
    ('Bấm tab', 'Click', 'After:\n– Đổi bảng, cập nhật “Tổng — Đã gán”, giữ các ô đã nhập.'),
    ('Bấm Quay lại', 'Click', 'After:\n– Về danh sách phiếu bàn giao (không hỏi lại dù đã nhập dữ liệu).'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Nhập thông tin bàn giao')
d.p('2.2.1 Biểu đồ Usecase')
d.uc_figure('FR-02', 'Nhập thông tin bàn giao', 'crud', actor=A)
d.p('2.2.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu. Chỉ bổ sung các quy tắc riêng của màn Tạo bàn giao.', anchor='create')
d.intro_table(
    ten='Nhập thông tin bàn giao',
    mota='Nhập 3 thông tin chung của phiếu: Ngày bàn giao, Lý do, Ghi chú chung.',
    tacnhan='Người lập phiếu',
    dieukien='Đang ở màn Tạo phiếu bàn giao.',
    chinh='1. Người dùng chọn Ngày bàn giao.\n2. Người dùng chọn Lý do.\n3. Người dùng nhập Ghi chú chung (không bắt buộc).',
    phu='• Bỏ trống Ngày bàn giao / Lý do rồi lưu → báo đỏ dưới ô (xem FR-07, FR-08).',
    dacbiet='Nhân viên bàn giao, phòng ban, công ty của phiếu lấy theo người đang đăng nhập, không chọn trên form.')
d.p('2.2.3 Layout màn hình')
lay('', '11a-da-nhap.png', 'Khối Thông tin bàn giao đã nhập')
d.p('2.2.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ngày bàn giao', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Trống', 'Gợi ý “Chọn ngày”. Dấu * đỏ ở nhãn.'),
    ('Lý do', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Có', 'Trống', 'Gợi ý “-- Chọn lý do --”. ' + REASONS + '.'),
    ('Ghi chú chung', 'Textbox', 'Enable', '0–1000 ký tự', 'Không', 'Trống', 'Gợi ý “VD: Bàn giao trước 31/03”.'),
    ('Lỗi dưới ô', 'Label', 'Hiển thị / Ẩn', '–', '–', 'Ẩn', 'Chữ đỏ dưới ô sau khi bấm Lưu nháp / Lưu và gửi.'),
])
d.p('2.2.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn / nhập giá trị', 'Change', 'After:\n– Ghi nhận giá trị vào phiếu đang soạn (chưa lưu).'),
    ('Lưu với ô trống', 'System',
     'During:\n– Ngày bàn giao trống → “Vui lòng chọn ngày bàn giao”.\n– Lý do trống → “Vui lòng chọn lý do bàn giao”.\n'
     '– Ghi chú chung > 1000 ký tự → “Ghi chú không được vượt quá 1000 ký tự”.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Chọn người nhận bàn giao')
d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Chọn người nhận bàn giao', 'crud', actor=A)
d.p('2.3.2 Giới thiệu')
d.rule_ref('- Kịch bản Dropdown, Validate dữ liệu. Chỉ bổ sung các quy tắc riêng của màn Tạo bàn giao.', anchor='search')
d.intro_table(
    ten='Chọn người nhận bàn giao',
    mota='Chỉ định người nhận cho từng công việc theo 3 cách: chọn ở từng dòng, gán cho cả nhóm dự án, gán hàng loạt '
         'cho các dòng đang tích chọn.',
    tacnhan='Người lập phiếu',
    dieukien='Đang ở màn Tạo phiếu bàn giao, có ít nhất 1 công việc.',
    chinh='1. Từng dòng: mở ô Người nhận BG và chọn 1 người.\n'
          '2. Theo dự án: ở dòng nhóm dự án chọn 1 người rồi bấm “Gán” → mọi công việc của nhóm nhận người đó.\n'
          '3. Hàng loạt: tích các dòng → hiện thanh “Đã chọn: n mục”; chọn người ở “-- Chọn người nhận --” rồi bấm '
          '“Gán hàng loạt”.\n'
          '4. “Tổng — Đã gán” cập nhật theo số dòng đã có người nhận.',
    phu='• Nút Gán / Gán hàng loạt bị khoá khi chưa chọn người.\n'
        '• Các dòng tích chọn không có người nhận chung → danh sách “-- Chọn người nhận --” rỗng.\n'
        '• “Bỏ chọn” → bỏ tích mọi dòng của tab, ẩn thanh gán hàng loạt.\n'
        '• Công việc không thuộc giải pháp nào hoặc giải pháp không có nhân sự → ô Người nhận rỗng, không gán được.',
    dacbiet=RECV)
d.p('2.3.3 Layout màn hình')
lay('', '03-chon-nguoi-nhan.png', 'Chọn người nhận ở từng dòng')
d.figure(shot('04-gan-theo-du-an.png'), 'Chọn người nhận cho cả nhóm dự án (nút Gán)', width_in=6.2)
d.figure(shot('05-gan-hang-loat.png'), 'Thanh Gán hàng loạt khi tích chọn nhiều dòng', width_in=6.2)
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Người nhận BG (dòng)', 'Dropdown', 'Enable', 'Danh sách', 'Có (khi gửi duyệt)', '-- Chọn --',
     'Có ô tìm trong danh sách. ' + RECV),
    ('Ô chọn người nhận (dòng dự án)', 'Dropdown', 'Enable', 'Danh sách', 'Không', '-- Chọn --',
     'Danh sách người nhận của công việc đầu tiên trong nhóm.'),
    ('Nút Gán', 'Button', 'Enable / Disable', '–', '–', 'Disable', 'Khoá khi chưa chọn người.'),
    ('Ô chọn dòng / chọn tất cả', 'Checkbox', 'Enable', '–', 'Không', 'Bỏ chọn', 'Chọn tất cả chỉ áp cho tab đang xem.'),
    ('Thanh gán hàng loạt', 'Card', 'Hiển thị / Ẩn', '–', '–', 'Ẩn', 'Hiện khi có ≥ 1 dòng được tích.'),
    ('“Đã chọn: n mục”', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu', '–'),
    ('-- Chọn người nhận --', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Chỉ gồm người có mặt trong danh sách người nhận của TẤT CẢ dòng đang chọn.'),
    ('Nút Gán hàng loạt', 'Button', 'Enable / Disable', '–', '–', 'Disable', 'Khoá khi chưa chọn người.'),
    ('Nút Bỏ chọn', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích các dòng.'),
])
d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn người nhận ở dòng', 'Change', 'After:\n– Gán cho dòng; cập nhật “Đã gán”.'),
    ('Bấm Gán (dòng dự án)', 'Click',
     'After:\n– Gán người đã chọn cho mọi công việc của nhóm; xoá lựa chọn ở ô nhóm.'),
    ('Tích dòng', 'Change', 'After:\n– Hiện / cập nhật thanh gán hàng loạt.'),
    ('Bấm Gán hàng loạt', 'Click', 'After:\n– Gán người đã chọn cho các dòng đang tích, bỏ tích, ẩn thanh.'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Cập nhật tiến độ và ghi chú bàn giao')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Cập nhật tiến độ, ghi chú', 'crud', actor=A)
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu. Chỉ bổ sung các quy tắc riêng của màn Tạo bàn giao.', anchor='create')
d.intro_table(
    ten='Cập nhật tiến độ và ghi chú bàn giao',
    mota='Cập nhật Tiến độ % hiện tại của từng nhiệm vụ và ghi chú hướng dẫn cho người nhận.',
    tacnhan='Người lập phiếu',
    dieukien='Đang ở màn Tạo phiếu bàn giao.',
    chinh='1. Người dùng nhập Tiến độ % ở dòng nhiệm vụ (0–100).\n'
          '2. Người dùng nhập Ghi chú BG cho dòng (vd nơi lưu tài liệu, việc còn dở).\n'
          '3. Giá trị được lưu cùng phiếu khi bấm Lưu nháp / Lưu và gửi.',
    phu='• Tiến độ không phải số nguyên 0–100 → chữ đỏ “Chỉ nhập số nguyên 0–100” ngay dưới ô, giữ nguyên số đã gõ; '
        'bấm lưu → “Dữ liệu chưa hợp lệ, vui lòng kiểm tra các ô báo lỗi”, không gửi.',
    dacbiet='Tiến độ khi lưu được ghi thẳng vào nhiệm vụ gốc (không chờ duyệt). Màu số: < 40 đỏ, 40–79 cam, ≥ 80 xanh.')
d.p('2.4.3 Layout màn hình')
lay('', '06-tien-do-loi.png', 'Ô Tiến độ % nhập sai báo đỏ ngay dưới ô')
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiến độ %', 'Number', 'Enable', 'Số nguyên 0 – 100', 'Không', 'Tiến độ hiện tại của nhiệm vụ',
     'Chỉ tab Nhiệm vụ. Để trống hợp lệ.'),
    ('Lỗi tiến độ', 'Label', 'Hiển thị / Ẩn', '–', '–', 'Ẩn', '“Chỉ nhập số nguyên 0–100”.'),
    ('Ghi chú BG', 'Textbox', 'Enable', '0–500 ký tự', 'Không', 'Trống', 'Gợi ý “Ghi chú...”.'),
])
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Nhập Tiến độ %', 'Change',
     'During:\n– Không phải số nguyên hoặc ngoài 0–100 → “Chỉ nhập số nguyên 0–100”, viền ô đỏ.\n'
     'After:\n– Hợp lệ → xoá lỗi; giá trị chờ lưu.'),
    ('Nhập Ghi chú BG', 'Change',
     'During:\n– > 500 ký tự → khi lưu báo “Ghi chú bàn giao không được vượt quá 500 ký tự”.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Bỏ công việc khỏi danh sách')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Bỏ công việc khỏi danh sách', 'action', actor=A)
d.p('2.5.2 Giới thiệu')
d.rule_ref('- UI/UX. Chỉ bổ sung các quy tắc riêng của màn Tạo bàn giao.', anchor='create')
d.intro_table(
    ten='Bỏ công việc khỏi danh sách',
    mota='Loại 1 công việc không cần bàn giao ra khỏi phiếu đang soạn.',
    tacnhan='Người lập phiếu',
    dieukien='Đang ở màn Tạo phiếu bàn giao.',
    chinh='1. Người dùng bấm dấu × đỏ ở cuối dòng (rê chuột hiện “Bỏ khỏi danh sách”).\n'
          '2. Hệ thống bỏ dòng khỏi bảng ngay, cập nhật số đếm tab và “Tổng — Đã gán”.',
    phu='• Không hỏi xác nhận. Muốn lấy lại công việc đã bỏ thì mở lại màn (công việc chưa lưu vào phiếu sẽ hiện lại).',
    dacbiet='Chỉ bỏ khỏi phiếu, không xóa nhiệm vụ / vấn đề gốc.')
d.p('2.5.3 Layout màn hình')
lay(' => Bỏ khỏi danh sách', '07-bo-khoi-ds.png', 'Cột Bỏ khỏi danh sách ở cuối bảng')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Bỏ khỏi danh sách', 'Icon Button', 'Enable', 'Hiển thị', 'Dấu × viền đỏ; rê chuột “Bỏ khỏi danh sách”.'),
    ('Số đếm tab / Tổng — Đã gán', 'Label', 'Hiển thị', 'Theo dữ liệu', 'Cập nhật ngay sau khi bỏ.'),
], required=False, scope=False)
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm ×', 'Click', 'After:\n– Bỏ dòng khỏi phiếu đang soạn (chưa ghi dữ liệu cho tới khi lưu).'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Xem chi tiết nhiệm vụ / vấn đề')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết. Chỉ bổ sung các quy tắc riêng của màn Tạo bàn giao.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết nhiệm vụ / vấn đề',
    mota='Mở cửa sổ chi tiết của công việc để xem đủ thông tin trước khi bàn giao.',
    tacnhan='Người lập phiếu; Người dùng đã đăng nhập',
    dieukien='Đang ở màn Tạo phiếu bàn giao.',
    chinh='1. Người dùng bấm mã hoặc tên công việc ở cột Mã • Tên.\n'
          '2. Nhiệm vụ → mở cửa sổ “<mã> — Chi tiết nhiệm vụ” ở chế độ xem nâng cao; Vấn đề → mở cửa sổ chi tiết '
          'vấn đề chỉ đọc.\n3. Bấm “Đóng” hoặc × để quay lại form.',
    phu='• Dữ liệu phiếu đang soạn giữ nguyên sau khi đóng cửa sổ.')
d.p('2.6.2 Layout màn hình')
lay('', '08-chi-tiet-nhiem-vu.png', 'Cửa sổ chi tiết nhiệm vụ mở từ cột Mã • Tên', modal='chi tiết nhiệm vụ')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“<mã> — Chi tiết nhiệm vụ” + badge trạng thái.'),
    ('Các trường nhiệm vụ', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Loại nhiệm vụ, Tên công việc, Giải pháp, Dự án/Nhóm, Hạng mục, Meeting, Người thực hiện, Mức độ ưu tiên, '
     'Hạn hoàn thành, Giờ hạn, Mô tả, Số giờ được giao, Người duyệt kết quả, Người theo dõi, Thẻ, Lặp lại, '
     'Yêu cầu báo cáo tiến độ (đặc tả tại SRS - Nhiệm vụ).'),
    ('Khối Lịch sử', 'Card', 'Enable', '–', 'Thu gọn', 'Lịch sử của nhiệm vụ.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm mã / tên công việc', 'Click', 'After:\n– Mở cửa sổ chi tiết tương ứng loại công việc.'),
    ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ, giữ nguyên dữ liệu form.'),
])

# ------------------------------------------------------------------ 2.7
d.h3('2.7 Lưu nháp phiếu bàn giao')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Lưu nháp phiếu bàn giao', 'crud', actor=A)
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc '
           'ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Lưu nháp phiếu bàn giao',
    mota='Lưu phiếu ở trạng thái Nháp để sửa tiếp sau; phiếu nháp chỉ người lập thấy.',
    tacnhan='Người lập phiếu',
    dieukien='Đang ở màn Tạo phiếu bàn giao.',
    chinh='1. Người dùng bấm “Lưu nháp”.\n'
          '2. Hệ thống kiểm tra dữ liệu.\n'
          '3. Hệ thống tạo phiếu Nháp, sinh mã BG.<năm>.<số>, lưu danh sách công việc.\n'
          '4. Hệ thống báo “Đã lưu nháp thành công” và chuyển về danh sách phiếu bàn giao.',
    phu='• Thiếu Ngày bàn giao / Lý do / người nhận ở dòng nào → lỗi dưới từng ô + toast “Bạn chưa nhập đầy đủ thông '
        'tin”, không lưu.\n'
        '• Có ô Tiến độ báo đỏ → “Dữ liệu chưa hợp lệ, vui lòng kiểm tra các ô báo lỗi”.\n'
        '• Công việc đang nằm trong phiếu khác chưa hoàn tất → “Có nhiệm vụ đã được bàn giao trong 1 phiếu khác chưa '
        'hoàn tất: <mã>”.\n• Lỗi khác → “Có lỗi xảy ra”.',
    dacbiet='Lưu nháp cũng bắt buộc đủ Ngày bàn giao, Lý do, ít nhất 1 công việc và người nhận ở MỌI dòng.')
d.p('2.7.3 Layout màn hình')
lay(' => Lưu nháp', '09-luu-nhap-loi.png', 'Lưu nháp khi còn thiếu thông tin — lỗi hiện dưới từng ô')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thanh nút đáy màn, đứng đầu.'),
    ('Ngày bàn giao, Lý do', 'Datepicker / Dropdown', 'Enable', '–', 'Có', 'Theo form', 'Xem FR-02.'),
    ('Danh sách công việc', 'Table/Grid', 'Enable', '≥ 1 dòng', 'Có', 'Theo form', '–'),
    ('Người nhận BG mỗi dòng', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Theo form', 'Thiếu → “Bắt buộc phải nhập”.'),
    ('Toast kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Thành công “Đã lưu nháp thành công”; lỗi “Bạn chưa nhập đầy đủ thông tin” / nội dung lỗi nghiệp vụ.'),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu nháp', 'Click',
     'Before:\n' + NO_LOGIN + '\n– Còn ô Tiến độ báo đỏ → “Dữ liệu chưa hợp lệ, vui lòng kiểm tra các ô báo lỗi”, dừng.\n'
     'During:\n– Ngày bàn giao trống → “Vui lòng chọn ngày bàn giao”.\n– Lý do trống → “Vui lòng chọn lý do bàn giao”.\n'
     '– Không có công việc → “Danh sách công việc bàn giao không được trống”.\n'
     '– Dòng chưa có người nhận → “Bắt buộc phải nhập” dưới ô Người nhận BG.\n'
     '– Có lỗi trường → toast “Bạn chưa nhập đầy đủ thông tin”.\n'
     '– Công việc đang ở phiếu khác chưa hoàn tất → “Có nhiệm vụ đã được bàn giao trong 1 phiếu khác chưa hoàn tất: '
     '<mã>”.\n– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Tạo phiếu Nháp: nhân viên bàn giao, phòng ban, công ty = người đăng nhập; mã BG.<năm>.<số>.\n'
     '– Lưu công việc (trạng thái nhận = Chờ nhận); ghi tiến độ vào nhiệm vụ.\n'
     '– Ghi lịch sử “<tên> đã lập phiếu bàn giao công việc.”\n'
     '– “Đã lưu nháp thành công”, chuyển về danh sách phiếu bàn giao.'),
])

# ------------------------------------------------------------------ 2.8
d.h3('2.8 Lưu và gửi duyệt')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Lưu và gửi duyệt', 'action', actor=A)
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi '
           'lịch sử.', anchor='create')
d.intro_table(
    ten='Lưu và gửi trưởng phòng duyệt',
    mota='Lưu phiếu rồi gửi trưởng phòng duyệt; phiếu chuyển sang Chờ duyệt.',
    tacnhan='Người lập phiếu',
    dieukien='Đang ở màn Tạo phiếu bàn giao (hoặc Sửa phiếu Nháp / Từ chối).',
    chinh='1. Người dùng bấm “Lưu và gửi”.\n'
          '2. Hệ thống hỏi “Xác nhận lưu và gửi” — “Bạn đồng ý lưu và gửi?”; người dùng bấm “Xác nhận”.\n'
          '3. Hệ thống kiểm tra Ngày bàn giao, Lý do, số công việc và người nhận của mọi dòng.\n'
          '4. Hệ thống hỏi “Gửi trưởng phòng duyệt” — “Bạn có chắc muốn gửi phiếu bàn giao cho trưởng phòng duyệt? '
          'Tổng N mục.”; người dùng bấm “Gửi duyệt”.\n'
          '5. Hệ thống lưu phiếu rồi gửi duyệt, báo “Đã gửi phiếu cho trưởng phòng duyệt” và về danh sách.',
    phu='• Thiếu thông tin → lỗi dưới ô Ngày bàn giao / Lý do, toast “Bạn chưa nhập đầy đủ thông tin”, cuộn lên đầu '
        'trang, không mở hộp Gửi trưởng phòng duyệt.\n'
        '• Bấm “Hủy” ở một trong 2 hộp → không lưu, không gửi.\n'
        '• Lỗi lưu/gửi → như FR-07 hoặc nội dung lỗi nghiệp vụ; lỗi khác “Có lỗi xảy ra”.',
    dacbiet='Khi gửi, hệ thống thông báo cho trưởng phòng (BR-04).')
d.p('2.8.3 Layout màn hình')
lay(' => Lưu và gửi', '11-gui-duyet-xac-nhan.png', 'Hộp xác nhận Gửi trưởng phòng duyệt')
d.figure(shot('10a-xac-nhan-luu-gui.png'), 'Hộp xác nhận đầu tiên “Xác nhận lưu và gửi”', width_in=6.2)
d.figure(shot('10b-gui-loi.png'), 'Bấm gửi khi còn thiếu thông tin', width_in=6.2)
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Lưu và gửi', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Màu chính, biểu tượng máy bay giấy.'),
    ('Hộp Xác nhận lưu và gửi', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', '“Bạn đồng ý lưu và gửi?” · Xác nhận / Hủy.'),
    ('Hộp Gửi trưởng phòng duyệt', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     '“Bạn có chắc muốn gửi phiếu bàn giao cho trưởng phòng duyệt? Tổng N mục.” · Gửi duyệt / Hủy.'),
    ('Ngày bàn giao, Lý do', 'Datepicker / Dropdown', 'Enable', '–', 'Có', 'Theo form', 'Xem FR-02.'),
    ('Người nhận BG mỗi dòng', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Theo form', '–'),
])
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu và gửi', 'Click', 'After:\n– Mở hộp “Xác nhận lưu và gửi”.'),
    ('Bấm Xác nhận', 'Click',
     'Before:\n– Còn ô Tiến độ báo đỏ → “Dữ liệu chưa hợp lệ, vui lòng kiểm tra các ô báo lỗi”, dừng.\n'
     'During:\n– Ngày bàn giao trống → “Vui lòng chọn ngày bàn giao”.\n– Lý do trống → “Vui lòng chọn lý do bàn giao”.\n'
     '– Không có công việc → “Không có công việc nào để bàn giao”.\n'
     '– Có dòng chưa có người nhận → “Còn N mục chưa có người nhận bàn giao”.\n'
     '– Có lỗi → toast “Bạn chưa nhập đầy đủ thông tin”, cuộn lên đầu trang, dừng.\n'
     'After:\n– Mở hộp “Gửi trưởng phòng duyệt”.'),
    ('Bấm Gửi duyệt', 'Click',
     'Before:\n' + NO_LOGIN + '\n'
     'During:\n– Lưu phiếu như FR-07 (tạo mới hoặc cập nhật); lỗi → như FR-07.\n'
     '– Phiếu không ở Nháp/Từ chối → “Không thể gửi duyệt phiếu ở trạng thái hiện tại”.\n'
     '– Không phải người lập → “Bạn không có quyền gửi duyệt phiếu này”.\n'
     '– Còn dòng chưa có người nhận → “Còn N mục chưa chọn người nhận bàn giao”.\n'
     'After:\n– Phiếu sang Chờ duyệt, ghi Ngày gửi duyệt, xoá lý do từ chối cũ.\n'
     '– Ghi lịch sử “<tên> gửi phiếu bàn giao chờ trưởng phòng duyệt.” (gửi lại phiếu bị từ chối: “<tên> đã gửi lại '
     'phiếu bàn giao chờ duyệt.”).\n'
     '– Gửi thông báo “Phiếu bàn giao công việc chờ duyệt” — “Phiếu bàn giao <mã> của <tên> chờ duyệt”.\n'
     '– “Đã gửi phiếu cho trưởng phòng duyệt”, chuyển về danh sách phiếu bàn giao.'),
])

# ==================================================== PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Tạo bàn giao; không lặp lại các quy tắc đã có trong SRS '
           'quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Công việc được đưa vào phiếu', [
        '– Nhiệm vụ đang giao cho người đăng nhập, trừ trạng thái Nháp, Hoàn thành, Huỷ.',
        '– Vấn đề đang giao cho người đăng nhập, trừ trạng thái Mới ghi nhận, Đã đóng.',
        '– Bỏ công việc đã nằm trong một phiếu chưa Hoàn tất khác (kể cả phiếu Nháp).',
    ], ['Xem công việc cần bàn giao', 'Lưu nháp', 'Lưu và gửi duyệt']),
    ('BR-02', 'Người nhận hợp lệ', [
        '– ' + RECV,
    ], 'Chọn người nhận bàn giao'),
    ('BR-03', 'Điều kiện lưu', [
        '– Bắt buộc: Ngày bàn giao, Lý do (1 trong 5 giá trị), ≥ 1 công việc, người nhận ở mọi dòng — áp cho cả Lưu '
        'nháp lẫn Lưu và gửi.',
        '– Ghi chú chung ≤ 1000 ký tự; Ghi chú BG ≤ 500 ký tự; Tiến độ số nguyên 0–100.',
        '– Giá trị nhập sai được giữ nguyên, báo đỏ dưới ô; còn lỗi thì không gửi lên máy chủ.',
    ], ['Nhập thông tin', 'Lưu nháp', 'Lưu và gửi duyệt']),
    ('BR-04', 'Người nhận thông báo gửi duyệt', [
        '– Người quản lý phòng ban của phiếu và nhân viên cùng phòng ban có quyền “Duyệt bàn giao công việc” trong '
        'cùng công ty. Bấm thông báo mở màn chi tiết phiếu.',
    ], 'Lưu và gửi duyệt'),
    ('BR-05', 'Thông tin tự gán', [
        '– Nhân viên bàn giao, phòng ban, công ty = người đăng nhập lúc lập phiếu; mã phiếu BG.<năm>.<4 số> tự sinh.',
        '– Tiến độ % khi lưu ghi thẳng vào nhiệm vụ gốc.',
    ], ['Lưu nháp', 'Lưu và gửi duyệt']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')

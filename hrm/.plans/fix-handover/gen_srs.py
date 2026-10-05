# -*- coding: utf-8 -*-
"""Sinh "SRS - Phê duyệt bàn giao công việc.docx" theo FORM CHUẨN (bản mẫu 2026-09-24).

Chạy (bọc khóa Word khi có agent khác cùng sinh tài liệu):
    python3 .plans/fix-handover/gen_srs.py
Thư viện dùng chung: .claude/skills/srs-documenter/assets/{srs_docx_lib,srs_uml_render}.py
Ảnh chụp (Playwright Python, 1440x900, nhánh develop): handover_pending_shots/ — chỉ để local.

⚠️ Ngày chụp (01–02/10/2026) DB local KHÔNG có phiếu bàn giao nào → các ảnh có dữ liệu được chụp
trên giao diện thật nhưng dữ liệu phiếu là GIẢ LẬP ở tầng mạng (Playwright page.route), dựng từ
nhân viên / nhiệm vụ có thật trong DB (NV Nguyễn Thị Hường, nhiệm vụ TPE.TASK.NB.26.0014).
Không ghi gì vào DB; mọi lệnh ghi tới phiếu bàn giao đều bị chặn. Ảnh 01b là màn rỗng thật.

Nguồn đối chiếu code:
  FE  pages/assign/handover/{pending.vue, _id/index.vue}
      pages/assign/handover/components/{HandoverInfoCard,HandoverItemsTable,HandoverHistoryModal}.vue
      components/{V2Footer.vue, V2BaseSmartFilterPanel.vue, assign/SystemInfoSection.vue,
      modal/base-confirm-modal.vue, modal/export-fields-modal.vue,
      modal/column-customization-modal.vue}
      components/menu-sidebar.js (hub "Phê duyệt" > "Bàn giao - Lắp đặt"), components/subsystems.js
  BE  Modules/Assign/Routes/api.php (nhóm /assign/handovers)
      Http/Controllers/Api/V1/HandoverController.php · Services/HandoverService.php
      Http/Requests/Handover/HandoverRejectRequest.php · Entities/Handover.php
      Transformers/HandoverResource/{HandoverResource,DetailHandoverResource}.php
      Services/SystemLogService.php (lịch sử phiếu bàn giao)
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 1029)
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

OUT = os.path.join(HERE, 'SRS - Phê duyệt bàn giao công việc.docx')
SHOTS = os.path.join(HERE, 'handover_pending_shots')
MENU = 'Phân hệ Công việc => Phê duyệt => Bàn giao - Lắp đặt => Bàn giao công việc'
MENU_CT = MENU + ' => Bấm vào mã phiếu'  # tester 02/10 10:31: chặng mã phiếu không icon

A_TP = 'Trưởng phòng duyệt bàn giao (Q1)'
TACNHAN = 'Trưởng phòng / người có quyền Duyệt bàn giao công việc; Người dùng đã đăng nhập'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này” '
           'và dừng xử lý.')


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='', full_url='', img_prefix='bgduyet_')

d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ Công việc': 'phanhe', 'Phê duyệt': 'pheduyet',
    'Bàn giao - Lắp đặt': 'bangiaolapdat', 'Bàn giao công việc': 'bangiaocongviec',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidat', 'Tùy chỉnh cột': 'cot',
    'Xuất Excel': 'xuat', 'Lịch sử': 'lichsu', 'Mã phiếu': 'maphieu',
    'Duyệt': 'duyet', 'Không duyệt': 'khongduyet',
}.items()})

d.title_block('Phê duyệt bàn giao công việc')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phê duyệt bàn giao công việc (danh sách '
    'phiếu bàn giao chờ duyệt và màn chi tiết phiếu) thuộc phân hệ Công việc, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của luồng Trưởng phòng duyệt phiếu bàn giao '
    'công việc.',
    'Làm rõ phạm vi phiếu hiển thị cho người duyệt và các tiêu chí tìm kiếm, lọc (dự án → giải '
    'pháp → hạng mục, người bàn giao, người tiếp nhận, ngày gửi duyệt).',
    'Làm rõ những gì người duyệt được điều chỉnh trên từng công việc trước khi duyệt (người nhận, '
    'ghi chú, tiến độ, hạn hoàn thành mới) và thời điểm các điều chỉnh đó có hiệu lực.',
    'Làm rõ điều kiện và hệ quả của thao tác Duyệt và Không duyệt (từ chối) phiếu.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu bàn giao công việc', 'Phiếu do nhân viên lập để chuyển các nhiệm vụ / vấn đề mình '
     'đang phụ trách cho người khác khi nghỉ việc, chuyển phòng ban, nghỉ thai sản, nghỉ dài hạn '
     'hoặc lý do khác. Mã phiếu dạng BG.<năm>.<số thứ tự>.'),
    ('Người bàn giao', 'Nhân viên có công việc cần bàn giao, ghi trên phiếu.'),
    ('Người nhận bàn giao (người tiếp nhận)', 'Nhân viên được chỉ định nhận từng công việc trong '
     'phiếu. Mỗi công việc có đúng 1 người nhận.'),
    ('Người duyệt', 'Trưởng phòng hoặc người được phân quyền Duyệt bàn giao công việc, quản lý '
     'phòng ban của phiếu.'),
    ('Công việc bàn giao', 'Một dòng trong phiếu: là một Nhiệm vụ hoặc một Vấn đề của người bàn '
     'giao. Màn chi tiết chia 2 thẻ Nhiệm vụ và Vấn đề, gom nhóm theo dự án.'),
    ('Ngày gửi duyệt', 'Thời điểm người lập phiếu bấm gửi duyệt (lần gần nhất, kể cả gửi lại sau '
     'khi bị từ chối).'),
    ('Hạn HT mới', 'Hạn hoàn thành mới người duyệt đặt cho công việc; khi duyệt sẽ thay hạn hoàn '
     'thành hiện tại của nhiệm vụ / vấn đề.'),
    ('Trạng thái phiếu', 'Nháp → Chờ duyệt → Đã duyệt → Hoàn tất; hoặc Chờ duyệt → Từ chối → '
     '(sửa, gửi lại) → Chờ duyệt. Màn này chỉ xử lý phiếu Chờ duyệt.'),
    ('TP', 'Trưởng phòng.'),
], widths=[1.9, 4.1])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Duyệt bàn giao công việc',
     'Hiện mục menu Bàn giao công việc trong nhóm Phê duyệt; xem danh sách phiếu chờ duyệt, tìm '
     'kiếm, xuất Excel, xem lịch sử; ở màn chi tiết phiếu Chờ duyệt được điều chỉnh công việc và '
     'hiện 2 nút Duyệt, Không duyệt.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn hình không dùng nhóm quyền phạm vi dữ liệu (3 quyền “Xem danh sách bàn giao công việc '
    'theo tổng công ty / công ty / phòng ban” chỉ áp cho màn Phiếu bàn giao, không áp cho màn '
    'này). Phạm vi phiếu hiển thị được xác định theo phòng ban người dùng quản lý — xem quy tắc '
    'BR-01 ở Phần 4.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách phiếu chờ duyệt', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc', '✅', '❌'),
    ('FR-04 Tùy chỉnh cột', '✅', '❌'),
    ('FR-05 Xuất Excel', '✅', '❌'),
    ('FR-06 Xem lịch sử phiếu', '✅', '❌'),
    ('FR-07 Xem chi tiết phiếu', '✅', '❌ (*)'),
    ('FR-08 Điều chỉnh công việc trước khi duyệt', '✅', '❌'),
    ('FR-09 Duyệt phiếu', '✅', '❌'),
    ('FR-10 Không duyệt (từ chối) phiếu', '✅', '❌'),
], widths=[3.4, 1.0, 1.6])
d.p('(*) Không có Q1 thì không vào được màn này từ menu. Người dùng mở chi tiết phiếu từ nơi khác '
    '(màn Phiếu bàn giao, thông báo) chỉ xem ở chế độ chỉ đọc, chân trang chỉ có nút Quay lại.')

# ================================================================ PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_TP, [0, 1, 2, 3, 4])],
    [('FR-01', 'Xem danh sách phiếu chờ duyệt', 'view'),
     ('FR-05', 'Xuất Excel', 'io'),
     ('FR-08', 'Điều chỉnh công việc trước khi duyệt', 'crud'),
     ('FR-09', 'Duyệt phiếu', 'action'),
     ('FR-10', 'Không duyệt (từ chối) phiếu', 'action')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem lịch sử phiếu', 'view', 'extend', [0], None),
     ('FR-07', 'Xem chi tiết phiếu', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Phê duyệt bàn giao công việc')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách phiếu chờ duyệt')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của màn Phê duyệt bàn giao công việc tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Xem danh sách phiếu bàn giao chờ duyệt',
    mota='Hiển thị các phiếu bàn giao đang ở trạng thái Chờ duyệt thuộc phòng ban người dùng quản '
         'lý (và phòng ban của chính người dùng), để người duyệt mở từng phiếu ra xử lý.',
    tacnhan=TACNHAN,
    dieukien='Người dùng đã đăng nhập và có quyền Q1.',
    chinh='1. Người dùng vào menu Phân hệ Công việc → Phê duyệt → Bàn giao - Lắp đặt → Bàn giao '
          'công việc.\n'
          '2. Hệ thống nạp trang 1, 20 dòng/trang, phiếu tạo mới nhất lên đầu.\n'
          '3. Bảng hiển thị dữ liệu, ô “Tổng: N” cạnh tiêu đề bảng, dòng “Hiển thị a–b / N” và '
          'thanh phân trang.',
    phu='• Không có phiếu nào chờ duyệt trong phạm vi → bảng trống, ô Tổng: 0.\n'
        '• Bấm Mã phiếu hoặc nút Duyệt ở cột Hành động → mở màn chi tiết phiếu (FR-07); chuột '
        'phải mở được tab mới.\n'
        '• Bấm nút Lịch sử ở cột Hành động → mở cửa sổ Lịch sử phiếu bàn giao (FR-06).\n'
        '• Bấm tiêu đề cột có biểu tượng sắp xếp → sắp xếp tăng / giảm theo cột đó.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách phiếu bàn giao chờ duyệt')
d.figure(shot('01c-danh-sach-phai.png'),
         'Phần bên phải bảng: cột Trạng thái và cột Hành động (Duyệt, Lịch sử)', width_in=6.2)
d.figure(shot('01b-danh-sach-rong.png'), 'Màn danh sách khi không có phiếu nào chờ duyệt',
         width_in=6.2)
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang “Phiếu bàn giao chờ duyệt”', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Tiêu đề trên thanh đầu trang và tiêu đề bảng.'),
    ('Ô “Tổng: N”', 'Label', 'Read-only', '≥ 0', 'Theo kết quả',
     'Tổng số phiếu chờ duyệt khớp bộ lọc.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Chọn trường xuất file (FR-05). Bị khóa trong lúc đang xuất.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tùy chỉnh cột (FR-04).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Đánh số liên tục qua các trang; cột cố định khi cuộn ngang.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Liên kết mở màn chi tiết phiếu; cố định khi cuộn ngang; sắp xếp được.'),
    ('Cột Nhân viên bàn giao', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Họ tên người bàn giao; dài quá thì xuống tối đa 2 dòng.'),
    ('Cột Phòng ban', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Phòng ban của phiếu.'),
    ('Cột Lý do bàn giao', 'Table/Grid', 'Read-only', 'Danh sách 5 giá trị', 'Theo dữ liệu',
     'Nghỉ việc / Chuyển phòng ban / Nghỉ thai sản / Nghỉ dài hạn / Khác. Sắp xếp được.'),
    ('Cột Số công việc trong phiếu', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Tổng số nhiệm vụ + vấn đề trong phiếu; căn phải.'),
    ('Cột Ngày bàn giao', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Ngày gửi duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Thời điểm gửi duyệt gần nhất. Sắp xếp được.'),
    ('Cột Ghi chú', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Ghi chú của phiếu; tối đa 2 dòng, rê chuột xem đủ.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Người lập phiếu và thời điểm lập; Ngày tạo sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Người và thời điểm sửa phiếu gần nhất; Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Chờ duyệt', 'Theo dữ liệu',
     'Nhãn màu cam “Chờ duyệt” (chữ và màu do hệ thống trả về).'),
    ('Cột Hành động – nút Duyệt (biểu tượng dấu tích kép)', 'Icon Button', 'Enable', '–',
     'Hiển thị', 'Mở màn chi tiết phiếu để xem và duyệt (FR-07); không duyệt ngay tại danh sách.'),
    ('Cột Hành động – nút Lịch sử (biểu tượng đồng hồ)', 'Icon Button', 'Enable', '–',
     'Hiển thị', 'Mở cửa sổ Lịch sử phiếu bàn giao (FR-06).'),
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc.'),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5 / 10 / 20 / 50 / 100', '20',
     'Đổi thì quay về trang 1.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
     'Về đầu / lùi / số trang / tiến / về cuối.'),
    ('Thanh cuộn ngang trên và dưới bảng', 'Table/Grid', 'Enable', '–', 'Ẩn khi bảng không tràn',
     'Cuộn đồng bộ 2 thanh; cột STT, Mã phiếu đứng yên.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Ẩn', 'Hiện trong lúc nạp dữ liệu.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Mục menu chỉ hiển thị khi có quyền Q1. Không có Q1 mà mở màn → bảng trống.\n'
     '– Nếu vừa rời màn sang màn phiếu bàn giao khác và quay lại trong vòng 10 phút → khôi phục '
     'bộ lọc và trạng thái đóng/mở khối Tìm kiếm nâng cao đã dùng.\n'
     'During:\n– Lấy phiếu Chờ duyệt thuộc phòng ban người dùng quản lý và phòng ban của chính '
     'người dùng (BR-01).\n'
     '– Song song nạp cấu hình cột và danh mục cho các ô lọc (không chặn hiển thị bảng).\n'
     'After:\n– Hiển thị trang 1, 20 dòng, phiếu tạo mới nhất lên đầu.'),
    ('Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click',
     'After:\n– Sắp xếp theo cột đó, bấm lại để đảo chiều; quay về trang 1. Các cột sắp xếp '
     'được: Mã phiếu, Lý do bàn giao, Ngày bàn giao, Ngày gửi duyệt, Ngày tạo, Ngày cập nhật, '
     'Trạng thái.'),
    ('Bấm số trang / đổi Số dòng/trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu; đổi số dòng/trang thì quay về trang 1.'),
    ('Bấm Mã phiếu / nút Duyệt ở cột Hành động', 'Click',
     'After:\n– Chuyển sang màn chi tiết phiếu (FR-07).'),
    ('Bấm nút Lịch sử ở cột Hành động', 'Click',
     'After:\n– Mở cửa sổ Lịch sử phiếu bàn giao của dòng đó (FR-06).'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Phê '
           'duyệt bàn giao công việc tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc phiếu chờ duyệt',
    mota='Tìm nhanh theo mã phiếu, mã hoặc tên người bàn giao; lọc nâng cao theo người bàn giao, '
         'người tiếp nhận, lý do, dự án → giải pháp → hạng mục và khoảng ngày gửi duyệt.',
    tacnhan=TACNHAN,
    dieukien='Đang ở màn danh sách phiếu chờ duyệt.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc và chọn điều kiện.\n'
          '3. Mỗi lần đổi một ô lọc nâng cao, hệ thống tự lọc lại ngay, không cần bấm Tìm kiếm.\n'
          '4. Bảng hiển thị kết quả từ trang 1.',
    phu='• Chọn Dự án → ô Giải pháp chỉ còn giải pháp của dự án đó; đổi Dự án thì Giải pháp và '
        'Hạng mục đang chọn bị xóa.\n'
        '• Chưa chọn Giải pháp → ô Hạng mục không có lựa chọn; đổi Giải pháp thì Hạng mục đang chọn '
        'bị xóa.\n'
        '• Bấm Làm mới → xóa hết điều kiện lọc và sắp xếp, trả về danh sách ban đầu.\n'
        '• Bấm “Ẩn tìm kiếm nâng cao” → thu gọn khối lọc, điều kiện đã chọn vẫn giữ.\n'
        '• Không có kết quả → bảng trống, ô Tổng: 0.',
    dacbiet=None)
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-bo-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Gợi ý “Tìm theo mã phiếu, mã hoặc tên người bàn giao”. Tìm gần đúng; chỉ áp dụng khi bấm '
     'Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc và sắp xếp.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–',
     'Khối lọc đang đóng', 'Mở / đóng khối lọc nâng cao.'),
    ('Người bàn giao', 'Dropdown', 'Enable', 'Người bàn giao của các phiếu đang chờ duyệt', 'Không',
     'Trống', 'Hiển thị “Tên - Mã phòng - Mã nhân viên”. Lọc đúng theo người bàn giao.'),
    ('Người tiếp nhận', 'Dropdown', 'Enable', 'Người nhận của các phiếu đang chờ duyệt', 'Không',
     'Trống', 'Lọc phiếu có ít nhất 1 công việc giao cho người được chọn.'),
    ('Lý do bàn giao', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống',
     'Nghỉ việc / Chuyển phòng ban / Nghỉ thai sản / Nghỉ dài hạn / Khác.'),
    ('Dự án', 'Dropdown', 'Enable', 'Dự án của các công việc trong phiếu chờ duyệt', 'Không',
     'Trống', 'Lọc phiếu có ít nhất 1 công việc thuộc dự án.'),
    ('Giải pháp', 'Dropdown', 'Enable', 'Giải pháp thuộc dự án đang chọn (chưa chọn dự án: tất cả)',
     'Không', 'Trống', 'Lọc phiếu có ít nhất 1 công việc thuộc giải pháp.'),
    ('Hạng mục', 'Dropdown', 'Enable', 'Hạng mục thuộc giải pháp đang chọn', 'Không', 'Trống',
     'Không có lựa chọn khi chưa chọn Giải pháp. Lọc phiếu có ít nhất 1 công việc thuộc hạng mục.'),
    ('Ngày gửi duyệt', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống',
     'Một ô chọn khoảng ngày; so theo ngày của thời điểm gửi duyệt, tính cả 2 ngày biên.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm / Enter ở ô tìm nhanh', 'Click / Keypress',
     'After:\n– Lọc gần đúng theo mã phiếu hoặc mã / họ tên người bàn giao, kết hợp các điều kiện '
     'lọc nâng cao; hiển thị trang 1.'),
    ('Đổi giá trị một ô lọc nâng cao', 'Change',
     'After:\n– Tự lọc lại ngay theo toàn bộ điều kiện đang chọn, quay về trang 1.'),
    ('Đổi Dự án', 'Change',
     'After:\n– Xóa Giải pháp và Hạng mục đang chọn; danh sách Giải pháp chỉ còn giải pháp của dự '
     'án mới.'),
    ('Đổi Giải pháp', 'Change',
     'After:\n– Xóa Hạng mục đang chọn; danh sách Hạng mục chỉ còn hạng mục của giải pháp mới.'),
    ('Bấm Làm mới', 'Click',
     'After:\n– Xóa mọi điều kiện và sắp xếp, nạp lại danh sách đúng 1 lần, hiển thị trang 1.'),
])

# ---------------------------------------------------------------- 2.3
d.h3('2.3 Cài đặt bộ lọc')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Cấu hình bộ lọc. Chỉ bổ sung danh sách tiêu chí lọc riêng của màn Phê duyệt bàn giao '
           'công việc.', anchor='list')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Cho phép mỗi người dùng chọn những ô lọc muốn hiện ở khối Tìm kiếm nâng cao và sắp xếp lại '
         'thứ tự của chúng. Cấu hình lưu theo từng người dùng và riêng cho màn này.',
    tacnhan=TACNHAN,
    dieukien='Đang ở màn danh sách phiếu chờ duyệt.',
    chinh='1. Người dùng bấm nút Cài đặt bộ lọc.\n'
          '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 7 tiêu chí kèm ô tích chọn, theo cấu hình '
          'đang lưu.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng kéo thả để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống ghi cấu hình, đóng cửa sổ, hiển thị “Cập nhật thành công” và áp ngay lên khối '
          'Tìm kiếm nâng cao.',
    phu='• Bấm Khôi phục mặc định → tích lại đủ 7 tiêu chí theo thứ tự gốc; chưa ghi, phải bấm Lưu '
        'mới có hiệu lực.\n'
        '• Bấm Đóng hoặc dấu × → thoát, không lưu thay đổi.\n'
        '• Bỏ tích một tiêu chí đang có giá trị lọc → sau khi Lưu, giá trị lọc của tiêu chí đó bị xóa.\n'
        '• Lưu thất bại → thông báo “Thao tác thất bại”, cửa sổ vẫn mở.',
    dacbiet=None)
d.p('2.3.2 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', modal='Cài đặt bộ lọc',
         shot=shot('03-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc với 7 tiêu chí')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Cài đặt bộ lọc”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     'Dòng hướng dẫn: “Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu '
     'theo từng màn hình.”'),
    ('Ô tích chọn từng tiêu chí', 'Checkbox', 'Enable', 'Danh sách 7 tiêu chí', 'Không',
     'Theo cấu hình đã lưu (mặc định tích hết)',
     'Người bàn giao, Người tiếp nhận, Lý do bàn giao, Dự án, Giải pháp, Hạng mục, Ngày gửi duyệt. '
     'Mỗi tiêu chí kèm số thứ tự; không có tiêu chí bị khóa. Bỏ tích thì tiêu chí không hiện ở khối '
     'Tìm kiếm nâng cao.'),
    ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Kéo để đổi thứ tự tiêu chí trên khối lọc.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Ghi cấu hình cho người dùng hiện tại và màn này; khóa trong lúc đang lưu.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Tích lại đủ 7 tiêu chí theo thứ tự gốc, chưa ghi.'),
    ('Nút Đóng / dấu ×', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thoát mà không lưu.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Cập nhật thành công” / “Thao tác thất bại”.'),
])
d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Cài đặt bộ lọc', 'Click',
     'After:\n– Mở cửa sổ, nạp danh sách tiêu chí theo cấu hình đang lưu của người dùng cho màn này.'),
    ('Tích / bỏ tích, kéo thả tiêu chí', 'Change',
     'After:\n– Chỉ ghi nhận trong cửa sổ, chưa áp lên màn hình cho tới khi bấm Lưu.'),
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi cấu hình (tiêu chí hiện / ẩn và thứ tự) cho người dùng hiện tại, riêng màn này.\n'
     'After:\n– Đóng cửa sổ, hiển thị “Cập nhật thành công”; khối Tìm kiếm nâng cao đổi ngay theo cấu '
     'hình mới; tiêu chí vừa bị ẩn được xóa giá trị lọc.\n'
     '– Lỗi → “Thao tác thất bại”.'),
    ('Bấm Khôi phục mặc định', 'Click',
     'After:\n– Tích lại đủ 7 tiêu chí theo thứ tự gốc; chưa ghi.'),
    ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng cửa sổ, không lưu.'),
])

# ---------------------------------------------------------------- 2.4
d.h3('2.4 Tùy chỉnh cột')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Cấu hình cột. Chỉ bổ sung bộ cột riêng của màn Phê duyệt bàn giao công việc.',
           anchor='list')
d.intro_table(
    ten='Tùy chỉnh cột hiển thị',
    mota='Cho phép mỗi người dùng chọn những cột muốn thấy trên bảng danh sách phiếu chờ duyệt và '
         'sắp xếp lại thứ tự cột. Cấu hình lưu theo từng người dùng và riêng cho màn này.',
    tacnhan=TACNHAN,
    dieukien='Đang ở màn danh sách phiếu chờ duyệt.',
    chinh='1. Người dùng bấm nút Cấu hình cột hiển thị (biểu tượng cột) cạnh nút Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ “Tùy chỉnh cột” liệt kê đủ 15 cột kèm ô tích chọn.\n'
          '3. Người dùng tích / bỏ tích và kéo thả các cột không bị khóa để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống ghi cấu hình, hiển thị “Cập nhật thành công”, đóng cửa sổ và áp ngay lên bảng.',
    phu='• Ba cột STT, Mã phiếu, Hành động bị khóa: hiện xám kèm ổ khóa, không bỏ tích và không kéo '
        'được.\n'
        '• Bấm Đóng hoặc dấu × → thoát, danh sách cột trở về cấu hình đang áp dụng.\n'
        '• Lưu thất bại → thông báo “Thao tác thất bại”.',
    dacbiet='Mặc định hiện đủ mọi cột. Cấu hình cột của màn này lưu riêng, không dùng chung với màn '
            'Phiếu bàn giao và màn Chờ tiếp nhận bàn giao. Cột đang hiện cũng là các trường được tích '
            'sẵn khi Xuất Excel.')
d.p('2.4.2 Layout màn hình')
d.layout(menu=MENU + ' => Tùy chỉnh cột', modal='Tùy chỉnh cột',
         shot=shot('04-cau-hinh-cot.png'), shot_caption='Cửa sổ Tùy chỉnh cột')
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Tùy chỉnh cột”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', 'Kèm biểu tượng và dấu ×.'),
    ('Ô tích chọn từng cột', 'Checkbox', 'Enable / Disable', 'Danh sách 15 cột', 'Không',
     'Theo cấu hình đã lưu (mặc định tích hết)',
     'STT, Mã phiếu, Nhân viên bàn giao, Phòng ban, Lý do bàn giao, Số công việc, Ngày bàn giao, Ngày '
     'gửi duyệt, Ghi chú, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật, Trạng thái, Hành động.'),
    ('Biểu tượng ổ khóa (cột bắt buộc)', 'Label', 'Hiển thị', '–', '–', 'Hiển thị ở 3 cột',
     'STT, Mã phiếu, Hành động: ô tích bị khóa, không kéo được; rê chuột hiện “Cột bắt buộc — không '
     'thể ẩn hoặc đổi vị trí”.'),
    ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị ở cột không khóa',
     'Kéo để đổi vị trí cột trên bảng.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình rồi đóng cửa sổ.'),
    ('Nút Đóng / dấu ×', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Cập nhật thành công” / “Thao tác thất bại”.'),
])
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Cấu hình cột hiển thị', 'Click',
     'After:\n– Mở cửa sổ Tùy chỉnh cột với cấu hình cột đang áp dụng.'),
    ('Tích / bỏ tích, kéo thả cột', 'Change',
     'During:\n– Cột STT, Mã phiếu, Hành động không cho bỏ tích, không kéo được.\n'
     'After:\n– Chỉ ghi nhận trong cửa sổ.'),
    ('Bấm Lưu', 'Click',
     'During:\n– Bảng đổi ngay theo cột đã chọn; ghi cấu hình cột cho người dùng hiện tại, riêng màn '
     'này.\n'
     'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ.\n– Lỗi → “Thao tác thất bại”.'),
    ('Bấm Đóng / ×', 'Click',
     'After:\n– Đóng cửa sổ; danh sách cột trong cửa sổ trở về cấu hình đang áp dụng.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Xuất Excel')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Xuất Excel danh sách phiếu chờ duyệt', 'io', actor=A_TP,
            caption='Biểu đồ Use Case — FR-05 Xuất Excel')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách phiếu chờ duyệt',
    mota='Tải về tệp Excel các phiếu chờ duyệt theo đúng bộ lọc và thứ tự sắp xếp đang áp dụng, '
         'lấy toàn bộ dòng (không giới hạn theo trang), với các trường người dùng chọn.',
    tacnhan=TACNHAN,
    dieukien='Người dùng có quyền Q1, đang ở màn danh sách phiếu chờ duyệt.',
    chinh='1. Người dùng bấm nút Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiện trên '
          'bảng.\n'
          '3. Người dùng tích / bỏ tích, kéo thả để đổi thứ tự cột trong tệp.\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống tải về tệp danh_sach_phieu_ban_giao_cho_duyet.xlsx, tiêu đề “Danh sách '
          'phiếu bàn giao chờ duyệt”, và thông báo “Xuất Excel thành công”.',
    phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích toàn bộ 13 trường.\n'
        '• Bấm Đóng → thoát, không xuất.\n'
        '• Lỗi khi xuất → thông báo “Lỗi khi xuất Excel”.\n'
        '• Không có phiếu khớp bộ lọc → tệp chỉ có dòng tiêu đề.',
    dacbiet='Nút Xuất Excel bị khóa trong lúc đang xuất để tránh bấm 2 lần.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất file',
         shot=shot('05-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất file')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Chọn trường xuất file”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     'Dòng hướng dẫn: tích chọn trường cần xuất, kéo để đổi thứ tự cột trong tệp.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Tích / bỏ tích toàn bộ trường.'),
    ('Danh sách trường xuất', 'Modal', 'Enable', 'Danh sách 13 trường', 'Có (≥ 1 trường)',
     'Tích sẵn các cột đang hiện trên bảng',
     'Mã phiếu, Nhân viên bàn giao, Phòng ban, Lý do bàn giao, Trạng thái, Ngày bàn giao, Tổng '
     'công việc, Ghi chú, Ngày gửi duyệt, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật.'),
    ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Đổi thứ tự cột trong tệp.'),
    ('Dòng “Đang chọn x/13 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bắt đầu xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Xuất Excel thành công” / “Lỗi khi xuất Excel”.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các trường ứng với cột đang hiện.'),
    ('Bấm nút Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1; không có quyền → tệp xuất ra không có dòng dữ liệu nào.\n'
     'During:\n– Lấy toàn bộ phiếu chờ duyệt theo bộ lọc, từ khóa và thứ tự sắp xếp đang áp dụng, '
     'trong phạm vi phòng ban (BR-01); chỉ lấy các trường đã tích, đúng thứ tự đã kéo.\n'
     'After:\n– Tải tệp danh_sach_phieu_ban_giao_cho_duyet.xlsx; hiển thị “Xuất Excel thành '
     'công”.\n'
     '– Lỗi → hiển thị “Lỗi khi xuất Excel”.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xem lịch sử phiếu')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và hiển thị lịch sử.', anchor='history')
d.intro_table(
    ten='Xem lịch sử phiếu bàn giao',
    mota='Hiển thị các mốc thao tác trên phiếu theo dòng thời gian (mới nhất ở trên): Tạo phiếu, '
         'Gửi duyệt, Gửi duyệt lại, Duyệt, Từ chối, Nghiệm thu hạng mục, Từ chối hạng mục, Hoàn '
         'tất — kèm người thực hiện, phòng ban và nội dung.',
    tacnhan=TACNHAN,
    dieukien='Đang ở màn danh sách phiếu chờ duyệt hoặc màn chi tiết phiếu. Chức năng không gắn '
             'quyền riêng.',
    chinh='1. Người dùng bấm nút Lịch sử ở cột Hành động (hoặc bấm Xem lịch sử ở khối Lịch sử '
          'cuối màn chi tiết).\n'
          '2. Hệ thống mở cửa sổ “Lịch sử phiếu bàn giao” với dòng “Phiếu bàn giao: <mã> - <người '
          'bàn giao>” và nạp các mốc.\n'
          '3. Hệ thống hiển thị danh sách mốc, mốc mới nhất ở trên.',
    phu='• Bấm Bộ lọc → lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc '
        'luôn, Làm mới để xóa điều kiện.\n'
        '• Không có mốc phù hợp bộ lọc → “Không có lịch sử phù hợp bộ lọc.”\n'
        '• Phiếu chưa có mốc nào → “Chưa có lịch sử thao tác nào.”\n'
        '• Lỗi tải → hiện thông báo lỗi kèm nút Thử lại.',
    dacbiet=None)
d.p('2.6.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử', modal='Lịch sử phiếu bàn giao',
         shot=shot('06-lich-su.png'), shot_caption='Cửa sổ Lịch sử phiếu bàn giao')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Lịch sử phiếu bàn giao”', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Dòng phụ chữ xám “Phiếu bàn giao: <mã phiếu> - <người bàn giao>”.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Mở / đóng khối lọc lịch sử.'),
    ('Loại hành động', 'Dropdown', 'Enable', 'Tạo mới / Thay đổi trạng thái…', 'Trống',
     'Lọc mốc theo nhóm hành động.'),
    ('Người thực hiện', 'Dropdown', 'Enable', 'Người đã thao tác trên phiếu', 'Trống',
     'Lọc mốc theo người thực hiện.'),
    ('Từ ngày / Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống',
     'Lọc mốc theo khoảng ngày.'),
    ('Nút Làm mới (trong khối lọc)', 'Button', 'Enable', '–', 'Hiển thị', 'Xóa điều kiện lọc.'),
    ('Mốc thời gian', 'Label', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Kèm tên hành động tô màu theo loại.'),
    ('Dòng “Người thực hiện: <tên> — <phòng ban>”', 'Label', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Nội dung', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Ví dụ “<tên> (Trưởng phòng) đã từ chối phiếu. Lý do: …”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     '“Chưa có lịch sử thao tác nào.” / “Không có lịch sử phù hợp bộ lọc.”'),
    ('Nút × đóng cửa sổ', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Lịch sử ở cột Hành động', 'Click',
     'After:\n– Mở cửa sổ và nạp các mốc của phiếu; mỗi lần mở đều nạp lại.'),
    ('Bấm Xem lịch sử ở màn chi tiết', 'Click',
     'After:\n– Mở khối Lịch sử; chỉ nạp dữ liệu ở lần mở đầu tiên; nút đổi thành Thu gọn, có '
     'thêm nút Làm mới để nạp lại.'),
    ('Đổi điều kiện trong khối Bộ lọc', 'Change',
     'After:\n– Lọc ngay danh sách mốc đang hiển thị.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Xem chi tiết phiếu')
d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu bàn giao',
    mota='Hiển thị thông tin phiếu, danh sách công việc cần bàn giao (chia thẻ Nhiệm vụ / Vấn đề, '
         'gom theo dự án), khối Lịch sử và các nút xử lý ở chân trang.',
    tacnhan=TACNHAN,
    dieukien='Người dùng đã đăng nhập; mở phiếu từ màn danh sách chờ duyệt hoặc từ thông báo.',
    chinh='1. Người dùng bấm Mã phiếu (hoặc nút Duyệt) ở màn danh sách.\n'
          '2. Hệ thống mở màn chi tiết, tiêu đề “<mã phiếu> — Chi tiết phiếu bàn giao”.\n'
          '3. Hệ thống hiển thị khối Thông tin bàn giao, khối Danh sách cần bàn giao (thẻ Nhiệm vụ '
          'mở sẵn), khối Lịch sử (thu gọn) và chân trang.\n'
          '4. Phiếu Chờ duyệt và người dùng có Q1 → chân trang có Duyệt, Không duyệt, Quay lại; '
          'bảng công việc ở chế độ chỉnh sửa (FR-08).',
    phu='• Phiếu không còn Chờ duyệt hoặc người dùng không có Q1 → chỉ đọc, chân trang chỉ có nút '
        'Quay lại (về màn Phiếu bàn giao).\n'
        '• Bấm thẻ Vấn đề → chuyển sang danh sách vấn đề; cột Tiến độ % chỉ có ở thẻ Nhiệm vụ.\n'
        '• Bấm mã hoặc tên công việc → mở cửa sổ xem chi tiết nhiệm vụ / vấn đề đó.\n'
        '• Thẻ đang chọn không có công việc → “Không có nhiệm vụ nào.” / “Không có vấn đề nào.”\n'
        '• Phiếu không tồn tại / lỗi tải → thông báo “Lỗi tải phiếu bàn giao” và chuyển về màn '
        'Phiếu bàn giao.\n'
        '• Bấm Quay lại → về màn danh sách phiếu chờ duyệt.',
    dacbiet=None)
d.p('2.7.2 Layout màn hình')
# Bản tester (Drive 02/10 10:29) viết lại: 2 cách vào, chặng cuối "Bấm vào mã phiếu cần xem" không icon
d.p('Đường dẫn màn hình:')
d.p('Cách 1:')
d._menu_para(MENU + ' => Bấm vào mã phiếu cần xem')
d.p('Cách 2:')
d.p('Bấm thông báo “Phiếu bàn giao công việc chờ duyệt” trên chuông thông báo (gửi tới người duyệt '
    'khi phiếu được gửi duyệt) → mở thẳng màn chi tiết phiếu.')
d.figure(shot('07-chi-tiet.png'), 'Màn chi tiết phiếu bàn giao đang Chờ duyệt', width_in=6.2)
d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '<mã phiếu> — Chi tiết phiếu bàn giao', '–'),
    ('Khối “Thông tin bàn giao” – nhãn trạng thái', 'Badge', 'Read-only', 'Chờ duyệt…',
     'Theo dữ liệu', 'Góc phải khối; chữ và màu theo trạng thái phiếu.'),
    ('Mã phiếu', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Ngày bàn giao', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '–'),
    ('Người bàn giao', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Kèm (tên phòng ban).'),
    ('Người nhận bàn giao', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Danh sách người nhận (không trùng) của các công việc, cách nhau dấu phẩy; chưa có thì “—”.'),
    ('Lý do', 'Text', 'Read-only', 'Danh sách 5 giá trị', 'Theo dữ liệu', '–'),
    ('Người duyệt / Ngày duyệt', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm:ss', '—',
     'Phiếu Chờ duyệt hiển thị “—”.'),
    ('Ghi chú', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Trống hiển thị “—”.'),
    ('Khung “Phiếu bàn giao bị từ chối”', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Chỉ hiện khi phiếu ở trạng thái Từ chối: Lý do, người và thời điểm xử lý.'),
    ('Khối “Danh sách cần bàn giao”', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Dòng phụ “Công việc của <người bàn giao>”.'),
    ('Thẻ Nhiệm vụ (n) / Vấn đề (n)', 'Button', 'Enable', '–', 'Nhiệm vụ',
     'Kèm “Tổng x — Đã gán y” của thẻ đang chọn.'),
    ('Dòng nhóm dự án', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Số La Mã + tên dự án + (n mục); công việc không có dự án gom vào “Không có dự án”.'),
    ('Cột STT, Mã • Tên', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mã và tên là liên kết mở cửa sổ xem nhiệm vụ / vấn đề.'),
    ('Cột Người giao, Trạng thái, Ưu tiên', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người giao việc; trạng thái và mức ưu tiên hiện dạng nhãn màu.'),
    ('Cột Tiến độ %', 'Number', 'Enable / Read-only', 'Số nguyên 0 – 100', 'Theo dữ liệu',
     'Chỉ ở thẻ Nhiệm vụ. Sửa được khi đang ở chế độ duyệt (FR-08).'),
    ('Cột Hạn hoàn thành', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm:ss', 'Theo dữ liệu', '–'),
    ('Cột Hạn HT mới', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy hh:mm', 'Trống',
     'Chỉ hiện ở chế độ duyệt (FR-08).'),
    ('Cột Người nhận BG, Ghi chú BG', 'Dropdown / Textbox', 'Enable / Read-only', '–',
     'Theo dữ liệu', 'Sửa được ở chế độ duyệt (FR-08); chỉ đọc thì hiện tên / nội dung hoặc “—”.'),
    ('Khối Lịch sử', 'Label', 'Hiển thị', '–', 'Thu gọn', 'Nút Xem lịch sử / Thu gọn (FR-06).'),
    ('Nút Duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện khi phiếu Chờ duyệt và người dùng có Q1 (FR-09).'),
    ('Nút Không duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện khi phiếu Chờ duyệt và người dùng có Q1 (FR-10).'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị',
     'Về màn phiếu chờ duyệt (chế độ duyệt) hoặc màn Phiếu bàn giao (chế độ chỉ đọc).'),
], required=False)
d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'During:\n– Nạp phiếu kèm công việc, người nhận và danh sách người có thể nhận của từng '
     'giải pháp / hạng mục.\n'
     'After:\n– Phiếu Chờ duyệt và có Q1 → bật chế độ duyệt; ngược lại chỉ đọc.\n'
     '– Lỗi → “Lỗi tải phiếu bàn giao”, chuyển về màn Phiếu bàn giao.'),
    ('Bấm thẻ Nhiệm vụ / Vấn đề', 'Click', 'After:\n– Đổi danh sách công việc đang hiển thị.'),
    ('Bấm mã / tên công việc', 'Click',
     'After:\n– Mở cửa sổ xem chi tiết nhiệm vụ (chế độ xem) hoặc vấn đề.'),
    ('Bấm Quay lại', 'Click', 'After:\n– Về màn tương ứng; điều chỉnh chưa duyệt bị bỏ.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Điều chỉnh công việc trước khi duyệt')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Điều chỉnh công việc trước khi duyệt', 'crud', actor=A_TP,
            caption='Biểu đồ Use Case — FR-08 Điều chỉnh công việc trước khi duyệt')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa).',
           anchor='create')
d.intro_table(
    ten='Điều chỉnh công việc trước khi duyệt',
    mota='Người duyệt đổi người nhận, ghi chú bàn giao, tiến độ (nhiệm vụ) và đặt hạn hoàn thành '
         'mới cho từng công việc ngay trên bảng; gán người nhận theo nhóm dự án hoặc hàng loạt. '
         'Điều chỉnh chỉ được lưu cùng lúc với thao tác Duyệt.',
    tacnhan=TACNHAN,
    dieukien='Người dùng có Q1; phiếu đang ở trạng thái Chờ duyệt; đang ở màn chi tiết phiếu.',
    chinh='1. Người dùng chọn Người nhận BG, sửa Ghi chú BG, Tiến độ %, Hạn HT mới trên từng dòng.\n'
          '2. Hoặc chọn người ở ô cạnh dòng nhóm dự án rồi bấm Gán → gán cho mọi công việc của dự '
          'án đó trong thẻ đang mở.\n'
          '3. Hoặc tích chọn nhiều dòng → thanh “Đã chọn: n mục” hiện ra → chọn người nhận → bấm '
          'Gán hàng loạt.\n'
          '4. Người dùng bấm Duyệt để lưu điều chỉnh cùng lúc với duyệt phiếu (FR-09).',
    phu='• Nhập Tiến độ % không phải số nguyên từ 0 đến 100 → báo đỏ ngay dưới ô “Chỉ nhập số nguyên 0–100”, '
        'giữ nguyên số đã gõ; còn ô báo lỗi thì bấm Duyệt chỉ hiện '
        'thông báo “Dữ liệu chưa hợp lệ, vui lòng kiểm tra các ô báo lỗi”, không mở hộp xác nhận.\n'
        '• Bấm Bỏ chọn → bỏ tích mọi dòng, xóa người nhận đang chọn ở thanh gán hàng loạt.\n'
        '• Các dòng đã tích không có người nhận chung → ô người nhận ở thanh gán hàng loạt không có '
        'lựa chọn.\n'
        '• Bấm Không duyệt hoặc Quay lại → mọi điều chỉnh bị bỏ, không lưu.\n'
        '• Không điều chỉnh gì → khi duyệt giữ nguyên dữ liệu phiếu.',
    dacbiet='Nút Gán và Gán hàng loạt bị khóa khi chưa chọn người nhận. Rời màn khi chưa duyệt '
            'không có cảnh báo chưa lưu.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU_CT, shot=shot('10-sua-truoc-duyet.png'),
         shot_caption='Bảng công việc ở chế độ duyệt: thanh gán hàng loạt, Hạn HT mới, Người nhận '
                      'BG, Ghi chú BG')
d.figure(shot('10b-chon-nguoi-nhan.png'), 'Ô Người nhận BG: mỗi người hiển thị “Tên nhân viên - '
         'Mã phòng - Mã nhân viên”', width_in=6.2)
d.figure(shot('11-tien-do-loi.png'), 'Ô Tiến độ % nhập 150: viền đỏ và câu lỗi “Chỉ nhập số nguyên 0–100” ngay dưới ô, '
         'giữ nguyên số đã gõ', width_in=6.2)
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tích chọn dòng / chọn tất cả', 'Checkbox', 'Enable', '–', 'Không', 'Không tích',
     'Ô ở tiêu đề tích / bỏ tích mọi công việc của thẻ đang mở.'),
    ('Thanh “Đã chọn: n mục”', 'Label', 'Enable / Ẩn', '–', '–', 'Ẩn',
     'Chỉ hiện khi có ít nhất 1 dòng được tích.'),
    ('Chọn người nhận (thanh gán hàng loạt)', 'Dropdown', 'Enable',
     'Người có thể nhận chung của mọi dòng đã tích', 'Có khi bấm Gán hàng loạt', 'Trống',
     'Gợi ý “-- Chọn người nhận --”. Hiển thị “Tên nhân viên - Mã phòng - Mã nhân viên”.'),
    ('Nút Gán hàng loạt', 'Button', 'Enable / Disable', '–', '–', 'Disable',
     'Gán người đã chọn cho mọi dòng đã tích, rồi bỏ tích.'),
    ('Nút Bỏ chọn', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi dòng.'),
    ('Ô chọn người ở dòng nhóm dự án + nút Gán', 'Dropdown / Button', 'Enable', 'Theo công việc '
     'đầu tiên của nhóm', 'Có khi bấm Gán', 'Trống',
     'Gán người cho mọi công việc của dự án trong thẻ đang mở. Hiển thị “Tên nhân viên - Mã phòng '
     '- Mã nhân viên”.'),
    ('Tiến độ %', 'Number', 'Enable', 'Số nguyên 0 – 100', 'Không', 'Tiến độ hiện tại',
     'Chỉ có ở thẻ Nhiệm vụ. Màu chữ: < 40 đỏ, 40–79 cam, ≥ 80 xanh. Sai phạm vi → viền đỏ và '
     'câu lỗi “Chỉ nhập số nguyên 0–100” ngay dưới ô; hệ thống không tự sửa '
     'số đã gõ.'),
    ('Hạn HT mới', 'Datepicker', 'Enable', 'dd/mm/yyyy hh:mm', 'Không', 'Trống',
     'Để trống thì giữ hạn hoàn thành hiện tại.'),
    ('Người nhận BG', 'Dropdown', 'Enable', 'Nhân sự của hạng mục / giải pháp của công việc (BR-06)',
     'Có', 'Người nhận đã chọn khi lập phiếu', 'Hiển thị “Tên nhân viên - Mã phòng - Mã nhân '
     'viên”; không có người bàn giao trong danh sách; có nút × xóa chọn.'),
    ('Ghi chú BG', 'Textbox', 'Enable', '–', 'Không', 'Theo dữ liệu', 'Gợi ý “Ghi chú...”.'),
])
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Đổi Người nhận BG / Ghi chú BG / Tiến độ % / Hạn HT mới trên một dòng', 'Change',
     'During:\n– Tiến độ % trống thì hợp lệ; không phải số nguyên hoặc ngoài 0 – 100 → hiển thị '
     '“Chỉ nhập số nguyên 0–100” ngay dưới ô, giữ nguyên số đã gõ.\n'
     'After:\n– Ghi nhận điều chỉnh trên màn hình; chưa lưu cho tới khi bấm Duyệt.'),
    ('Bấm Gán ở dòng nhóm dự án', 'Click',
     'Before:\n– Nút khóa khi chưa chọn người.\n'
     'After:\n– Đặt người nhận cho mọi công việc của nhóm; xóa lựa chọn ở ô nhóm.'),
    ('Tích chọn dòng', 'Change',
     'After:\n– Hiện thanh gán hàng loạt; danh sách người nhận là phần giao của các dòng đã tích.'),
    ('Bấm Gán hàng loạt', 'Click',
     'Before:\n– Nút khóa khi chưa chọn người nhận.\n'
     'After:\n– Đặt người nhận cho mọi dòng đã tích, bỏ tích và xóa lựa chọn.'),
    ('Bấm Duyệt sau khi điều chỉnh', 'Click',
     'After:\n– Gửi toàn bộ công việc của phiếu kèm người nhận, ghi chú, tiến độ, hạn mới cùng '
     'lệnh duyệt (xử lý ở FR-09).'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Duyệt phiếu')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Duyệt phiếu bàn giao', 'action', actor=A_TP,
            caption='Biểu đồ Use Case — FR-09 Duyệt phiếu')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc đổi trạng thái, Thông báo và Quy tắc ghi lịch sử.', anchor='history')
d.intro_table(
    ten='Duyệt phiếu bàn giao công việc',
    mota='Người duyệt chấp thuận phiếu Chờ duyệt: lưu các điều chỉnh công việc (nếu có), chuyển '
         'phiếu sang Đã duyệt và thông báo cho người lập phiếu và các người nhận để tiếp nhận.',
    tacnhan=TACNHAN,
    dieukien='Người dùng có Q1; phiếu đang ở trạng thái Chờ duyệt.',
    chinh='1. Người dùng bấm nút Duyệt ở chân màn chi tiết.\n'
          '2. Hệ thống mở hộp thoại “Duyệt phiếu bàn giao” – “Xác nhận duyệt phiếu bàn giao <mã '
          'phiếu>?”; người dùng bấm Duyệt.\n'
          '3. Hệ thống kiểm tra quyền, trạng thái phiếu và dữ liệu điều chỉnh, lưu điều chỉnh công '
          'việc, chuyển phiếu sang Đã duyệt, ghi người duyệt và thời điểm duyệt.\n'
          '4. Hệ thống ghi lịch sử, gửi thông báo, hiển thị “Đã duyệt phiếu bàn giao” và quay về '
          'màn danh sách phiếu chờ duyệt.',
    phu='• Còn ô Tiến độ % báo lỗi → thông báo “Dữ liệu chưa hợp lệ, vui lòng kiểm tra các ô báo '
        'lỗi”, không mở hộp thoại.\n'
        '• Dữ liệu điều chỉnh bị hệ thống từ chối (vd Tiến độ ngoài 0 – 100) → câu lỗi hiện dưới '
        'đúng ô của dòng đó kèm thông báo “Dữ liệu chưa hợp lệ, vui lòng kiểm tra các ô báo lỗi”.\n'
        '• Bấm Hủy hoặc × → không duyệt, ở lại màn chi tiết.\n'
        '• Phiếu không còn Chờ duyệt (người khác vừa xử lý, người lập đã rút…) → thông báo “Phiếu '
        'không ở trạng thái chờ duyệt”.\n'
        '• Không có quyền → “Bạn không có quyền thực hiện chức năng này”.\n'
        '• Lỗi khác → hiển thị nội dung lỗi hệ thống trả về, hoặc “Lỗi duyệt phiếu”.',
    dacbiet='Thao tác Duyệt chỉ qua đúng 1 hộp xác nhận có mã phiếu.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU_CT + ' => Duyệt', modal='Duyệt phiếu bàn giao',
         shot=shot('08b-xac-nhan-duyet-2.png'),
         shot_caption='Hộp thoại xác nhận Duyệt phiếu bàn giao (kèm mã phiếu)')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Duyệt phiếu bàn giao”', 'Modal', 'Hiển thị', 'Ẩn',
     'Nội dung “Xác nhận duyệt phiếu bàn giao <mã phiếu>?” (mã in đậm).'),
    ('Nút Duyệt', 'Button', 'Enable', 'Hiển thị', 'Thực hiện duyệt.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng, không duyệt.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     '“Đã duyệt phiếu bàn giao” / “Dữ liệu chưa hợp lệ, vui lòng kiểm tra các ô báo lỗi” / nội '
     'dung lỗi / “Lỗi duyệt phiếu”.'),
], required=False, scope=False)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Duyệt ở chân trang', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu Chờ duyệt và người dùng có Q1.\n'
     '– Còn ô Tiến độ % báo lỗi → hiển thị “Dữ liệu chưa hợp lệ, vui lòng kiểm tra các ô báo lỗi” '
     'và dừng, không mở hộp thoại.\n'
     'After:\n– Mở hộp thoại “Duyệt phiếu bàn giao”.'),
    ('Bấm Duyệt trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Phiếu không ở trạng thái Chờ duyệt → hiển thị “Phiếu không ở trạng thái chờ duyệt” và '
     'dừng.\n'
     'During:\n– Tiến độ % không phải số nguyên → “Phải là số nguyên”; nhỏ hơn 0 → “Không được '
     'nhỏ hơn 0.”; lớn hơn 100 → “Không được lớn hơn 100.”; người nhận không còn → “Không tồn '
     'tại”; Hạn HT mới sai → “Không hợp lệ”. Câu lỗi hiện dưới đúng ô; có lỗi thì không thực hiện '
     'bước After.\n'
     '– Với từng công việc có điều chỉnh: lưu Người nhận BG, Ghi chú BG; ghi Tiến độ % '
     'vào nhiệm vụ; nếu có Hạn HT mới thì thay hạn hoàn thành (ngày + giờ) của nhiệm vụ / vấn đề.\n'
     'After:\n– Chuyển phiếu sang Đã duyệt, ghi người duyệt và thời điểm duyệt.\n'
     '– Ghi lịch sử “Duyệt”: “<tên> (Trưởng phòng) đã duyệt phiếu bàn giao.”\n'
     '– Gửi thông báo “Phiếu bàn giao đã được duyệt” – “Phiếu bàn giao <mã> đã được duyệt. Vui '
     'lòng xác nhận tiếp nhận công việc.” tới người lập phiếu và mọi người nhận.\n'
     '– Hiển thị “Đã duyệt phiếu bàn giao”, quay về màn danh sách phiếu chờ duyệt (phiếu vừa '
     'duyệt không còn trong danh sách).'),
    ('Bấm Hủy / × ở hộp thoại', 'Click', 'After:\n– Đóng hộp thoại, phiếu không đổi.'),
])

# ---------------------------------------------------------------- 2.10
d.h3('2.10 Không duyệt (từ chối) phiếu')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Không duyệt (từ chối) phiếu', 'action', actor=A_TP,
            caption='Biểu đồ Use Case — FR-10 Không duyệt (từ chối) phiếu')
d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc đổi trạng thái, Thông báo và Quy tắc ghi lịch sử.', anchor='history')
d.intro_table(
    ten='Không duyệt (từ chối) phiếu bàn giao',
    mota='Người duyệt từ chối phiếu Chờ duyệt kèm lý do bắt buộc. Phiếu chuyển sang Từ chối và '
         'quay lại cho người lập sửa, gửi duyệt lại.',
    tacnhan=TACNHAN,
    dieukien='Người dùng có Q1; phiếu đang ở trạng thái Chờ duyệt.',
    chinh='1. Người dùng bấm nút Không duyệt ở chân màn chi tiết.\n'
          '2. Hệ thống mở hộp thoại “Từ chối phiếu bàn giao” – “Vui lòng nhập lý do từ chối (tối '
          'thiểu 10 ký tự):”.\n'
          '3. Người dùng nhập Lý do từ chối và bấm Từ chối.\n'
          '4. Hệ thống kiểm tra lý do, quyền và trạng thái phiếu.\n'
          '5. Hệ thống chuyển phiếu sang Từ chối, lưu lý do, ghi lịch sử, gửi thông báo cho người '
          'lập phiếu.\n'
          '6. Hiển thị “Đã từ chối phiếu bàn giao” và quay về màn danh sách phiếu chờ duyệt.',
    phu='• Lý do (sau khi bỏ khoảng trắng đầu cuối) dưới 10 ký tự → thông báo “Lý do từ chối phải '
        'có tối thiểu 10 ký tự”, không gửi đi.\n'
        '• Lý do quá 1000 ký tự → “Lý do từ chối không được vượt quá 1000 ký tự”.\n'
        '• Phiếu không còn Chờ duyệt → “Phiếu không ở trạng thái chờ duyệt”.\n'
        '• Không có quyền → “Bạn không có quyền thực hiện chức năng này”.\n'
        '• Lỗi khác → nội dung lỗi hệ thống trả về, hoặc “Lỗi từ chối phiếu”.\n'
        '• Bấm Hủy hoặc × → đóng hộp thoại, phiếu không đổi.',
    dacbiet='Các điều chỉnh công việc đang làm dở trên bảng (FR-08) không được lưu khi Không duyệt.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU_CT + ' => Không duyệt', modal='Từ chối phiếu bàn giao',
         shot=shot('09-tu-choi.png'), shot_caption='Hộp thoại Từ chối phiếu bàn giao')
d.figure(shot('09b-tu-choi-ngan.png'), 'Thông báo khi lý do từ chối dưới 10 ký tự', width_in=6.2)
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Từ chối phiếu bàn giao”', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     'Dòng dẫn “Vui lòng nhập lý do từ chối (tối thiểu 10 ký tự):”.'),
    ('Lý do từ chối', 'Textarea', 'Enable', '10 – 1000 ký tự', 'Có', 'Trống',
     'Gợi ý “Nhập lý do từ chối...”. Lý do hiển thị cho người lập ở khung “Phiếu bàn giao bị từ '
     'chối” và trong lịch sử.'),
    ('Nút Từ chối', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Gửi lệnh từ chối.'),
    ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng hộp thoại, không đổi phiếu.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     '“Đã từ chối phiếu bàn giao” / “Lý do từ chối phải có tối thiểu 10 ký tự” / nội dung lỗi.'),
])
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Không duyệt ở chân trang', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu Chờ duyệt và người dùng có Q1.\n'
     'After:\n– Mở hộp thoại Từ chối phiếu bàn giao.'),
    ('Bấm nút Từ chối trong hộp thoại', 'Click',
     'Before:\n– Lý do sau khi bỏ khoảng trắng đầu cuối dưới 10 ký tự → hiển thị “Lý do từ chối '
     'phải có tối thiểu 10 ký tự” và dừng.\n'
     '– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Lý do trống → “Vui lòng nhập lý do từ chối”; dưới 10 ký tự → “Lý do từ chối phải '
     'có tối thiểu 10 ký tự”; quá 1000 ký tự → “Lý do từ chối không được vượt quá 1000 ký tự”.\n'
     '– Phiếu không ở trạng thái Chờ duyệt → “Phiếu không ở trạng thái chờ duyệt”.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Chuyển phiếu sang Từ chối, lưu lý do từ chối.\n'
     '– Ghi lịch sử “Từ chối”: “<tên> (Trưởng phòng) đã từ chối phiếu. Lý do: <lý do>”.\n'
     '– Gửi thông báo “Phiếu bàn giao bị từ chối” – “Phiếu bàn giao <mã> bị từ chối. Lý do: <lý '
     'do>” tới người lập phiếu.\n'
     '– Hiển thị “Đã từ chối phiếu bàn giao”, quay về màn danh sách phiếu chờ duyệt.'),
    ('Bấm Hủy / ×', 'Click', 'After:\n– Đóng hộp thoại, phiếu không đổi.'),
])

# ==================================================== PHẦN 4. QUY TẮC NGHIỆP VỤ
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của luồng Phê duyệt bàn giao công việc; không '
           'lặp lại các quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')

d.rule_table([
    ('BR-01', 'Phạm vi phiếu hiển thị cho người duyệt', [
        '– Chỉ hiển thị phiếu ở trạng thái Chờ duyệt.',
        '– Chỉ phiếu thuộc phòng ban người dùng được phân công quản lý, cộng phòng ban của chính '
        'người dùng.',
        '– Người dùng không có quyền Duyệt bàn giao công việc: danh sách, danh mục bộ lọc và tệp '
        'xuất đều rỗng.',
    ], ['Xem danh sách', 'Tìm kiếm và lọc', 'Xuất Excel']),

    ('BR-02', 'Nguồn phiếu vào màn chờ duyệt', [
        '– Phiếu vào màn này khi người lập bấm Gửi duyệt (từ Nháp) hoặc gửi lại sau khi bị từ '
        'chối; Ngày gửi duyệt ghi theo lần gửi gần nhất.',
        '– Khi gửi duyệt, mọi công việc trong phiếu phải đã có người nhận.',
        '– Thông báo “Phiếu bàn giao công việc chờ duyệt” gửi tới người có quyền Duyệt bàn giao '
        'công việc trong công ty của phiếu, thuộc phòng ban của phiếu hoặc quản lý phòng ban đó.',
    ], ['Xem danh sách', 'Xem chi tiết']),

    ('BR-03', 'Danh mục và quan hệ của các ô lọc', [
        '– Người bàn giao, Người tiếp nhận, Dự án, Giải pháp, Hạng mục chỉ gồm giá trị xuất hiện '
        'trong các phiếu đang chờ duyệt thuộc phạm vi BR-01.',
        '– Dự án → Giải pháp → Hạng mục là bộ lọc phụ thuộc: đổi cấp trên thì xóa cấp dưới.',
        '– Lọc theo Người tiếp nhận / Dự án / Giải pháp / Hạng mục: phiếu được giữ lại khi có ít '
        'nhất 1 công việc khớp.',
    ], 'Tìm kiếm và lọc'),

    ('BR-04', 'Chỉ phiếu Chờ duyệt mới được duyệt hoặc từ chối', [
        '– Duyệt / Không duyệt chỉ hiện khi phiếu Chờ duyệt và người dùng có quyền Duyệt bàn giao '
        'công việc; thiếu điều kiện thì ẩn nút, màn chi tiết chỉ đọc.',
        '– Phiếu đã chuyển trạng thái trước khi bấm → báo “Phiếu không ở trạng thái chờ duyệt”, '
        'không thay đổi gì.',
    ], ['Xem chi tiết', 'Duyệt', 'Không duyệt']),

    ('BR-05', 'Điều chỉnh công việc chỉ có hiệu lực khi Duyệt', [
        '– Người nhận, ghi chú bàn giao, tiến độ, hạn hoàn thành mới được lưu cùng thao tác Duyệt.',
        '– Không duyệt, Quay lại hoặc rời màn → bỏ toàn bộ điều chỉnh.',
        '– Tiến độ ghi thẳng vào nhiệm vụ; Hạn HT mới thay hạn hoàn thành (ngày và giờ) của nhiệm '
        'vụ / vấn đề; Hạn HT mới để trống thì giữ hạn cũ.',
        '– Tiến độ % chỉ nhận số nguyên từ 0 đến 100 (để trống được). Nhập sai thì báo đỏ dưới ô, '
        'giữ nguyên số đã gõ và không cho duyệt; hệ thống cũng kiểm tra lại khi lưu. Quy tắc này '
        'áp dụng cả ở màn Tạo / Sửa phiếu bàn giao.',
    ], ['Điều chỉnh công việc', 'Duyệt']),

    ('BR-06', 'Danh sách người có thể nhận công việc', [
        '– Công việc gắn hạng mục có nhân sự → chọn trong trưởng hạng mục và thành viên hạng mục.',
        '– Ngược lại → chọn trong nhân sự của giải pháp: PM, người tạo giải pháp, thành viên giải '
        'pháp, trưởng và thành viên các hạng mục của giải pháp.',
        '– Người bàn giao không có trong danh sách.',
        '– Mỗi người hiển thị theo khuôn “Tên nhân viên - Mã phòng - Mã nhân viên”.',
        '– Gán hàng loạt chỉ cho chọn người có mặt trong danh sách của mọi dòng đã tích.',
    ], 'Điều chỉnh công việc'),

    ('BR-07', 'Hệ quả khi Duyệt', [
        '– Phiếu chuyển Đã duyệt, ghi người duyệt và thời điểm duyệt; phiếu rời khỏi màn chờ '
        'duyệt.',
        '– Người lập phiếu và các người nhận nhận thông báo; người nhận xử lý từng công việc ở màn '
        'Chờ tiếp nhận bàn giao.',
        '– Người phụ trách nhiệm vụ / vấn đề CHƯA đổi tại bước duyệt — chỉ đổi sang người nhận khi '
        'người nhận bấm Nhận. Người nhận từ chối công việc thì công việc chuyển về người đã duyệt '
        'phiếu.',
        '– Mọi công việc được xử lý xong (nhận hoặc từ chối) → phiếu tự chuyển Hoàn tất.',
    ], 'Duyệt'),

    ('BR-08', 'Lý do và hệ quả khi Không duyệt', [
        '– Lý do từ chối bắt buộc, 10 – 1000 ký tự (không tính khoảng trắng đầu cuối).',
        '– Phiếu chuyển Từ chối, lưu lý do; không ghi người duyệt / ngày duyệt.',
        '– Người lập phiếu nhận thông báo kèm lý do, thấy khung “Phiếu bàn giao bị từ chối” ở màn '
        'chi tiết, sửa phiếu rồi gửi duyệt lại (phiếu quay về Chờ duyệt, lý do cũ bị xóa).',
    ], 'Không duyệt'),

    ('BR-09', 'Duyệt và Không duyệt chỉ qua 1 hộp thoại', [
        '– Bấm Duyệt mở đúng 1 hộp thoại “Duyệt phiếu bàn giao” có mã phiếu; bấm Duyệt trong hộp '
        'thoại là thực hiện duyệt.',
        '– Bấm Không duyệt mở đúng 1 hộp thoại “Từ chối phiếu bàn giao” có ô lý do.',
    ], ['Duyệt', 'Không duyệt']),

])

d.save()
print('OK:', OUT)

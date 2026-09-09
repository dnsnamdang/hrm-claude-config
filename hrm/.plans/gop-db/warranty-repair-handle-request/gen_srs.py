# -*- coding: utf-8 -*-
"""Sinh SRS man "Phieu xu ly yeu cau" (/customer-care/warranty-repair-handle-requests).

Nguon doi chieu (doc truc tiep tu code 03/09/2026, nhanh gop_db):
  BE  Modules/CustomerCare/{Routes/api.php,
        Http/Controllers/V1/WarrantyRepairHandleRequestController.php,
        Http/Requests/.../WarrantyRepairHandleRequestRequest.php,
        Services/{WarrantyRepairHandleRequestService, WarrantyRepairHandleRequestPrintService,
                  WarrantyRepairHandleRequestNotifier}.php,
        Entities/WarrantyRepairHandleRequest/WarrantyRepairHandleRequest.php}
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (quyen 1511-1514)
  FE  hrm-client/pages/customer-care/warranty-repair-handle-requests/
        {index.vue, create.vue, _id/index.vue, _id/edit.vue,
         components/WarrantyRepairHandleRequestForm.vue,
         components/RejectHandleRequestModal.vue}
      hrm-client/components/customer-care/QuickDeviceErrorModal.vue
  Anh chup that: .plans/gop-db/warranty-repair-handle-request/wrhr_shots/ (Playwright, 03/09/2026)

Chay:  python3 .plans/gop-db/warranty-repair-handle-request/gen_srs.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))                       # .plans/gop-db (lop mac)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "srs-documenter", "assets"))
from _mac_docx import patch_srs  # noqa: E402

patch_srs()
from srs_docx_lib import SrsDoc, ACTOR_P1  # noqa: E402

SHOTS = os.path.join(HERE, "wrhr_shots")
OUT = os.path.join(HERE, "SRS - Phiếu xử lý yêu cầu.docx")

MENU_CSKH = 'Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu'


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(
    out=OUT,
    menu='Phân hệ CSKH → Kiểm tra bảo hành sửa chữa → Phiếu xử lý yêu cầu',
    route='/customer-care/warranty-repair-handle-requests',
    full_url='/customer-care/warranty-repair-handle-requests',   # lib giu de tham chieu
    img_prefix='wrhr_')



# ================================================================= TRANG DAU
d.title_block('Phiếu xử lý yêu cầu')

d.h2('Mục lục')
d.toc()

# ============================================================ PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu xử lý yêu cầu, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và phạm vi dữ liệu của màn hình.',
    'Làm rõ vị trí của chứng từ này trong luồng dịch vụ: sinh ra từ Phiếu yêu cầu kiểm tra sửa '
    'chữa – bảo hành, và quyết định hướng đi tiếp là tư vấn điện thoại hay làm báo giá.',
    'Làm rõ tác động ngược lên phiếu yêu cầu gốc khi phiếu xử lý được gửi đi hoặc bị xóa.',
    'Làm rõ quy tắc bắt buộc nhập khác nhau giữa Lưu nháp và Lưu và gửi, và trường hợp hành động '
    '“Tư vấn điện thoại” tự đóng luồng.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu xử lý', 'Một bản ghi trên màn hình này. Là chứng từ THỨ HAI của luồng dịch vụ.'),
    ('Phiếu yêu cầu gốc', 'Phiếu yêu cầu kiểm tra sửa chữa – bảo hành mà phiếu xử lý này được lập từ đó.'),
    ('CCTT', 'Cung cấp thông tin làm báo giá — chứng từ thứ ba của luồng dịch vụ.'),
    ('Nguyên nhân', 'Công việc hoặc lỗi thiết bị lấy từ danh mục công việc – lỗi thiết bị, khai '
                    'riêng cho từng hàng hóa.'),
    ('Hành động', 'Hướng xử lý cho từng thiết bị: Tư vấn điện thoại, hoặc Cung cấp thông tin làm '
                  'báo giá.'),
    ('Lưu nháp', 'Lưu phiếu ở trạng thái Đang tạo, chưa gửi đi.'),
    ('Lưu và gửi', 'Lưu và chuyển phiếu sang trạng thái Chờ CCTT, gửi thông báo cho người có quyền '
                   'lập phiếu cung cấp thông tin.'),
    ('Hàng hóa tương đương', 'Hàng hóa trong danh mục được chọn thay cho thiết bị khách khai tự do, '
                             'để lấy đúng danh sách nguyên nhân và giá dịch vụ.'),
], widths=[1.9, 4.1])

# ============================================================ PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Tạo phiếu cung cấp thông tin',
     'Hiện hai thao tác Tạo phiếu cung cấp thông tin và Không duyệt; mở được lối vào danh sách '
     'phiếu đang Chờ CCTT; nhận thông báo khi có phiếu chuyển sang Chờ CCTT.'),
    ('Q2', 'Xử lý yêu cầu sửa chữa',
     'Quyền để LẬP RA phiếu này từ màn Yêu cầu kiểm tra sửa chữa – bảo hành. Không có quyền này '
     'thì không mở được màn lập phiếu.'),
    ('Q3', 'Quản lý danh mục công việc - lỗi thiết bị',
     'Dùng được nút Thêm nhanh để khai bổ sung nguyên nhân ngay trong lúc lập phiếu.'),
], widths=[0.8, 2.2, 3.0])

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu xử lý yêu cầu đi kiểm tra sửa chữa - bảo hành theo tổng công ty',
     'Toàn bộ phiếu của mọi công ty.'),
    ('V2', 'Xem phiếu xử lý yêu cầu đi kiểm tra sửa chữa - bảo hành theo công ty',
     'Phiếu thuộc công ty của người đăng nhập.'),
    ('V3', 'Xem phiếu xử lý yêu cầu đi kiểm tra sửa chữa - bảo hành theo phòng ban',
     'Phiếu thuộc các phòng người đăng nhập được phân quản lý, cộng phòng đang công tác, cộng '
     'phiếu do chính mình lập.'),
    ('—', '(không có quyền xem theo cấp nào)', 'Chỉ phiếu do chính mình lập.'),
], widths=[0.8, 2.4, 2.8])

d.p('Quy tắc áp cho MỌI cấp quyền ở trên: phiếu ở trạng thái Đang tạo của người khác không hiển '
    'thị với bất kỳ ai, kể cả người quản trị hệ thống.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'V1', 'V2', 'V3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '✅', '✅', '✅', '✅', '✅', '✅ (chỉ phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅', '✅', '✅ (trong phạm vi của mình)'),
    ('FR-03 Tùy chỉnh cột và cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Lập phiếu xử lý', '❌', '✅', '❌', '❌', '❌', '❌', '❌'),
    ('FR-05 Sửa phiếu', '✅', '✅', '✅', '✅', '✅', '✅', '✅ (phiếu Đang tạo của mình)'),
    ('FR-06 Xem chi tiết phiếu', '✅', '✅', '✅', '✅', '✅', '✅', '✅ (trong phạm vi của mình)'),
    ('FR-07 Thêm nhanh nguyên nhân', '❌', '❌', '✅', '❌', '❌', '❌', '❌'),
    ('FR-08 Tạo phiếu cung cấp thông tin', '✅', '❌', '❌', '❌', '❌', '❌', '❌'),
    ('FR-09 Không duyệt phiếu', '✅', '❌', '❌', '❌', '❌', '❌', '❌'),
    ('FR-10 Xóa phiếu', '✅', '✅', '✅', '✅', '✅', '✅', '✅ (phiếu Đang tạo của mình)'),
    ('FR-11 In phiếu và in danh sách', '✅', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-12 Xuất Excel', '✅', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-13 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅', '✅', '✅', '✅'),
], widths=[2.1, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 1.5])

d.p('Ghi chú: ô ✅ chỉ nói về quyền; hiện hay ẩn nút còn phụ thuộc điều kiện nghiệp vụ nêu tại '
    'Phần 4 (trạng thái phiếu, người lập).')

# ==================================================== PHAN 3. DAC TA CHI TIET
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [('Người xử lý (phòng tiếp nhận)', [0, 1, 2]),
     ('Người lập phiếu cung cấp thông tin', [0, 2])],
    # mains: MÀN HÌNH thật — nối thẳng tới actor
    [('FR-01', 'Xem danh sách phiếu xử lý', 'view'),
     ('FR-04', 'Lập phiếu xử lý', 'crud'),
     ('FR-06', 'Xem chi tiết phiếu xử lý', 'view')],
    # subs: thao tác làm ngay trên màn đó — nối bằng «include» / «extend»
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cấu hình bộ lọc và cột', 'view', 'extend', [0], None),
     ('FR-12', 'Xuất danh sách ra Excel', 'io', 'extend', [0], None),
     ('FR-05', 'Chỉnh sửa phiếu xử lý', 'crud', 'extend', [1], None),
     ('FR-07', 'Thêm nhanh nguyên nhân', 'crud', 'include', [1], None),
     ('FR-10', 'Xóa phiếu xử lý', 'action', 'extend', [1], None),
     ('FR-08', 'Tạo phiếu cung cấp thông tin', 'action', 'extend', [2], None),
     ('FR-09', 'Không duyệt phiếu xử lý', 'action', 'extend', [2], None),
     ('FR-11', 'In phiếu / in danh sách', 'io', 'extend', [2], None),
     ('FR-13', 'Xem lịch sử thay đổi', 'view', 'extend', [2], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu xử lý yêu cầu')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1 Xem danh sach
d.h3('2.1 Xem danh sách phiếu xử lý')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Phiếu xử lý yêu cầu tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách phiếu xử lý yêu cầu',
    mota='Hiển thị danh sách phiếu xử lý nằm trong phạm vi dữ liệu của người đăng nhập, kèm phân '
         'trang, sắp xếp và trạng thái của từng phiếu.',
    tacnhan='Người xử lý; Người lập phiếu cung cấp thông tin; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập vào hệ thống.',
    chinh='1. Người dùng vào màn hình theo một trong các lối vào ở mục Layout.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo lối vào và cấp quyền xem của người dùng.\n'
          '3. Hệ thống trả về trang đầu tiên, mặc định 10 dòng, sắp xếp theo Ngày tạo giảm dần.\n'
          '4. Bảng hiển thị dữ liệu; dòng “Hiển thị a–b / N” cho biết khoảng đang xem và tổng số '
          'phiếu khớp bộ lọc.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện thông báo không có dữ liệu.\n'
        '• Phiếu Đang tạo của người khác luôn bị loại khỏi danh sách.\n'
        '• Màn hình KHÔNG có nút Tạo mới; phiếu chỉ sinh ra từ màn Yêu cầu kiểm tra sửa chữa – '
        'bảo hành.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU_CSKH + '   (hiển thị: toàn bộ phiếu trong phạm vi quyền của người '
                          'đăng nhập)')
d.p('Menu: ' + MENU_CSKH + ' — mở bằng đường dẫn trần, không qua menu   (hiển thị: chỉ phiếu do '
                         'chính người đăng nhập lập — phạm vi mặc định)')
d.p('Menu: ' + MENU_CSKH + ' — lối vào danh sách chờ cung cấp thông tin   (hiển thị: phiếu đang ở '
                         'trạng thái Chờ CCTT)')
d.figure(shot('01-danh-sach.png'), 'Màn Phiếu xử lý yêu cầu lúc mới truy cập', width_in=6.2)

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Phiếu xử lý yêu cầu', 'Tiêu đề cố định.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Luôn hiển thị, ghim trái khi cuộn ngang.'),
    ('Cột Số phiếu xử lý', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Là liên kết mở màn chi tiết. Sắp xếp được. Không tắt được.'),
    ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Hiển thị dạng “mã khách hàng - tên khách hàng”.'),
    ('Cột Số phiếu yêu cầu', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
     'Là liên kết mở phiếu yêu cầu gốc.'),
    ('Cột Tên thiết bị liên quan', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
     'Hiện 2 dòng đầu, còn lại thu gọn sau liên kết “Xem thêm”.'),
    ('Cột Người yêu cầu / Ngày nhận yêu cầu', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
     'Lấy từ phiếu yêu cầu gốc.'),
    ('Cột Địa chỉ sửa chữa', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định', '–'),
    ('Cột Người xử lý / Ngày tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Người xử lý chính là người lập phiếu này. Ngày tạo sắp xếp được, mặc định giảm dần.'),
    ('Cột Ngày xử lý', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Ẩn mặc định',
     'Chỉ có giá trị khi đã lập phiếu cung cấp thông tin; sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
     'Trống nếu phiếu chưa từng được sửa.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 6 giá trị', 'Theo dữ liệu',
     'Chữ và màu do máy chủ quyết định, xem Phần 4 BR-02.'),
    ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo điều kiện từng phiếu',
     'Hai thao tác đầu hiện thẳng, còn lại nằm trong menu “Hành động khác”. Thao tác không đủ điều '
     'kiện thì ẩn hẳn.'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc.'),
    ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', 'Trang 1, 10 dòng', '–'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Đọc tham số lối vào để xác định phạm vi dữ liệu.\n'
     '– Xác định cấp quyền xem theo thứ tự tổng công ty → công ty → phòng ban.\n'
     'During:\n– Áp phạm vi dữ liệu; loại bỏ phiếu Đang tạo của người khác.\n'
     'After:\n– Trả về trang 1 và tổng số phiếu; hiển thị bảng.'),
    ('Bấm số phiếu yêu cầu ở cột tương ứng', 'Click',
     'After:\n– Mở màn chi tiết của phiếu yêu cầu gốc.'),
    ('Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click',
     'During:\n– Đổi chiều sắp xếp, giữ nguyên bộ lọc.\n'
     'After:\n– Nạp lại danh sách từ trang 1.'),
])

# ------------------------------------------------------------ 2.2 Tim kiem & loc
d.h3('2.2 Tìm kiếm và lọc')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang. Chỉ bổ sung các tiêu chí tìm kiếm và lọc riêng của màn hình tại phần mô tả chi tiết.',
           anchor='search')
d.intro_table(
    ten='Tìm kiếm nhanh và lọc nâng cao',
    mota='Thu hẹp danh sách theo từ khóa hoặc theo trạng thái, số phiếu yêu cầu, khách hàng, tên '
         'thiết bị, model, khoảng ngày tạo và đơn vị.',
    tacnhan='Người xử lý; Người lập phiếu cung cấp thông tin',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh hoặc mở khối Tìm kiếm nâng cao.\n'
          '2. Người dùng chọn các tiêu chí cần lọc.\n'
          '3. Người dùng bấm Tìm kiếm hoặc nhấn Enter.\n'
          '4. Hệ thống nạp lại danh sách từ trang 1 theo điều kiện lọc, trong phạm vi dữ liệu của '
          'người dùng.',
    phu='• Bấm Làm mới → xóa mọi điều kiện lọc nhưng giữ nguyên lối vào.\n'
        '• Không có kết quả → bảng hiện thông báo không có dữ liệu.\n'
        '• Điều kiện lọc được ghi nhớ trong 10 phút.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu', shot=shot('02-bo-loc-nang-cao.png'), shot_caption='Khối Tìm kiếm nâng cao đang mở')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Gợi ý “Tìm theo số phiếu xử lý, số phiếu yêu cầu, tên khách hàng, người xử lý”. Tìm đúng '
     'bốn trường đó.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 6 giá trị', 'Không', 'Trống',
     'Gợi ý “Chọn trạng thái”.'),
    ('Số phiếu yêu cầu', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Lọc theo số phiếu yêu cầu gốc. Chờ Enter hoặc nút Tìm kiếm.'),
    ('Khách hàng', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Gõ để tìm; danh sách nạp dần từ danh mục khách hàng.'),
    ('Tên thiết bị', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
    ('Model', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
    ('Ngày tạo từ / đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lọc theo ngày lập phiếu xử lý, tính trọn ngày ở cả hai đầu.'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Ẩn khi thiếu quyền',
     'Chỉ hiện với người có quyền xem theo cấp.'),
    ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban', 'Không', 'Ẩn khi thiếu quyền',
     'Lọc theo đơn vị của người lập phiếu.'),
    ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Làm mới xóa điều kiện nhưng giữ nguyên phạm vi dữ liệu của lối vào.'),
])

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm hoặc nhấn Enter', 'Click / Keypress',
     'During:\n– Gom mọi điều kiện đang chọn.\n'
     'After:\n– Nạp lại danh sách từ trang 1 trong phạm vi dữ liệu của người dùng.'),
    ('Chọn giá trị ở ô dạng danh sách', 'Change',
     'After:\n– Danh sách tự tìm lại ngay, không cần bấm thêm nút.'),
    ('Bấm Làm mới', 'Click',
     'After:\n– Xóa toàn bộ điều kiện lọc, giữ nguyên lối vào; nạp lại danh sách.'),
])

# ------------------------------------------- 2.3 Tuy chinh cot & cai dat bo loc
d.h3('2.3 Tùy chỉnh cột hiển thị và cài đặt bộ lọc')

d.p('2.3.1 Giới thiệu')
d.rule_ref('- Cấu hình bộ lọc và Tùy chỉnh cột. Chỉ bổ sung danh sách cột và ô lọc riêng của màn hình tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Tùy chỉnh cột hiển thị và cài đặt bộ lọc',
    mota='Cho phép mỗi người tự chọn cột nào hiện trên bảng và ô lọc nào hiện ở khối tìm kiếm nâng '
         'cao, kèm thứ tự sắp xếp.',
    tacnhan='Người xử lý; Người lập phiếu cung cấp thông tin',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm biểu tượng Cấu hình cột hiển thị hoặc nút Cài đặt bộ lọc.\n'
          '2. Hệ thống mở cửa sổ tương ứng với lựa chọn hiện tại.\n'
          '3. Người dùng tích chọn hoặc bỏ chọn, kéo thả để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu; hệ thống áp dụng ngay và ghi nhớ cho lần vào sau.',
    phu='• Bấm Khôi phục mặc định → trở lại cấu hình gốc của màn hình.\n'
        '• Cột STT, Số phiếu xử lý và Hành động luôn hiển thị.',
    dacbiet=None)

d.p('2.3.2 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu => Cài đặt bộ lọc / Tuỳ chỉnh cột', shot=shot('13-cau-hinh-cot.png'), shot_caption='Cửa sổ Tùy chỉnh cột')
d.figure(shot('14-cai-dat-bo-loc.png'), 'Cửa sổ Cài đặt bộ lọc', width_in=6.2)

d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách cột', 'Modal', 'Enable', 'Danh sách 15 cột', 'Không', 'Theo cấu hình đã lưu',
     'Mỗi dòng có ô tích chọn và tay nắm kéo thả.'),
    ('Cột bị khóa', 'Icon', 'Read-only', '–', '–', 'Hiển thị',
     'Biểu tượng ổ khóa ở các cột bắt buộc hiển thị.'),
    ('Danh sách ô lọc', 'Modal', 'Enable', 'Danh sách 8 ô lọc', 'Không', 'Theo cấu hình đã lưu',
     'Đánh số thứ tự hiển thị trên khối tìm kiếm nâng cao.'),
    ('Nút Lưu / Khôi phục mặc định / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])

d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click',
     'After:\n– Áp dụng ngay cho bảng, ghi nhớ theo từng người và từng màn hình.'),
    ('Bấm Khôi phục mặc định', 'Click',
     'After:\n– Trả lựa chọn về cấu hình gốc; vẫn phải bấm Lưu để áp dụng.'),
])

# ---------------------------------------------------------------- 2.4 Lap phieu
d.h3('2.4 Lập phiếu xử lý')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Lập phiếu xử lý', 'crud',
            [('include', 'Kiểm tra quyền Xử lý yêu cầu sửa chữa'),
             ('include', 'Chép dữ liệu từ phiếu yêu cầu gốc'),
             ('include', 'Chọn nguyên nhân và hành động cho từng thiết bị'),
             ('extend', 'Gửi thông báo khi phiếu chuyển sang Chờ CCTT')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-04 Lập phiếu xử lý')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các trường riêng của phiếu và quy tắc bắt buộc nhập theo từng nút bấm tại phần mô tả chi tiết.',
           anchor='create')
d.intro_table(
    ten='Lập phiếu xử lý yêu cầu',
    mota='Người của phòng tiếp nhận xem lại từng thiết bị khách báo hỏng, chọn nguyên nhân và '
         'quyết định hướng xử lý: tư vấn qua điện thoại là xong, hay chuyển sang làm báo giá.',
    tacnhan='Người xử lý (người có quyền Xử lý yêu cầu sửa chữa, thuộc phòng tiếp nhận)',
    dieukien='Mở từ nút “Tạo phiếu xử lý yêu cầu” của một phiếu yêu cầu đang ở trạng thái Chờ xử '
             'lý, thuộc phòng tiếp nhận của người đăng nhập và chưa có phiếu xử lý nào.',
    chinh='1. Người dùng bấm Tạo phiếu xử lý yêu cầu ở màn Yêu cầu kiểm tra sửa chữa – bảo hành.\n'
          '2. Hệ thống mở màn lập phiếu, chép sẵn thông tin khách hàng và toàn bộ thiết bị của '
          'phiếu yêu cầu gốc.\n'
          '3. Với từng thiết bị, người dùng chọn Nguyên nhân và Hành động; nếu chọn Tư vấn điện '
          'thoại thì nhập thêm Nội dung xử lý.\n'
          '4. Người dùng bấm Lưu nháp hoặc Lưu và gửi.\n'
          '5. Hệ thống kiểm tra dữ liệu, sinh số phiếu, ghi phiếu và cập nhật ngược trạng thái '
          'phiếu yêu cầu gốc.',
    phu='• Mở màn mà thiếu phiếu yêu cầu gốc → hệ thống báo “Thiếu phiếu yêu cầu gốc. Hãy mở màn '
        'này từ nút Tạo phiếu xử lý yêu cầu.”\n'
        '• Không đủ điều kiện lập phiếu → hệ thống từ chối và quay về danh sách.\n'
        '• Thiếu trường bắt buộc → báo lỗi đỏ ngay dưới ô tương ứng, không rời màn.\n'
        '• Thoát màn khi đã nhập mà chưa lưu → hệ thống hỏi xác nhận rời trang.',
    dacbiet='Mọi thiết bị đều chọn Hành động “Tư vấn điện thoại” thì phiếu chuyển thẳng sang trạng '
            'thái Đã tư vấn điện thoại và đóng luôn luồng, kể cả khi người dùng bấm Lưu nháp.')

d.p('2.4.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành => Tạo phiếu xử lý yêu cầu', shot=shot('07-lap-phieu.png'), shot_caption='Màn Lập phiếu xử lý với dữ liệu chép sẵn từ phiếu yêu cầu gốc')
d.figure(shot('08-lap-phieu-cot-phai.png'),
         'Các cột bên phải của bảng thiết bị: Nguyên nhân, Hành động, File đính kèm', width_in=6.2)

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Phiếu yêu cầu', 'Textbox', 'Disable', '–', 'Có', 'Theo phiếu gốc',
     'Chỉ đọc; ở màn chi tiết là liên kết mở phiếu yêu cầu gốc.'),
    ('Người yêu cầu / Phòng yêu cầu / Ngày nhận yêu cầu', 'Textbox', 'Disable', '–', 'Không',
     'Theo phiếu gốc', 'Chỉ đọc.'),
    ('Khách hàng', 'Textbox', 'Disable', '–', 'Có', 'Theo phiếu gốc', 'Chỉ đọc, không đổi được.'),
    ('Người liên hệ', 'Textbox', 'Disable', '–', 'Có khi Lưu và gửi', 'Theo phiếu gốc', 'Chỉ đọc.'),
    ('Số điện thoại liên hệ / Địa chỉ sửa chữa', 'Textbox', 'Disable', '–', 'Không', 'Theo phiếu gốc',
     'Chỉ đọc.'),
    ('Lý do không duyệt', 'Label', 'Read-only', '–', '–', 'Ẩn khi chưa từng bị trả lại',
     'Chữ xám, hiện lý do lần bị Không duyệt gần nhất.'),
    ('Bảng thiết bị – Tên hàng hóa', 'Table/Grid', 'Read-only', '–', 'Có', 'Theo phiếu gốc',
     'Thiết bị khách khai tự do có thêm nút “Chọn hàng hóa tương đương”.'),
    ('Bảng thiết bị – Thương hiệu / Model / Serial / Số BBBGNT-BBXNCV / Nội dung yêu cầu',
     'Table/Grid', 'Read-only', '–', 'Không', 'Theo phiếu gốc', 'Chỉ đọc, lấy nguyên từ phiếu gốc.'),
    ('Bảng thiết bị – Nguyên nhân', 'Dropdown', 'Enable', 'Danh sách nguyên nhân của đúng hàng hóa',
     'Có khi Lưu và gửi', 'Trống',
     'Chọn được nhiều giá trị. Hàng hóa chưa khai nguyên nhân thì hiện dòng nhắc và nút Thêm nhanh. '
     'Nguyên nhân đã khóa hiển thị kèm biểu tượng ổ khóa.'),
    ('Bảng thiết bị – Hành động', 'Dropdown', 'Enable', 'Tư vấn điện thoại / Cung cấp thông tin làm '
     'báo giá', 'Có khi Lưu và gửi', 'Trống', 'Quyết định hướng đi tiếp của thiết bị.'),
    ('Bảng thiết bị – Nội dung xử lý', 'Textarea', 'Enable', '0–1000 ký tự',
     'Có khi chọn Tư vấn điện thoại', 'Trống',
     'Chỉ hiện khi Hành động là Tư vấn điện thoại; đổi hành động khác thì bị xóa trắng. Bắt buộc '
     'kể cả khi Lưu nháp.'),
    ('Bảng thiết bị – File đính kèm', 'Button', 'Enable', 'PDF, ảnh, Word, Excel', 'Không', 'Trống',
     'Tải lên ngay khi chọn tệp.'),
    ('Bảng thiết bị – Xóa dòng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Bỏ thiết bị khỏi phiếu xử lý. Không có nút thêm dòng — thiết bị chỉ chép từ phiếu gốc.'),
    ('Nút Thêm nhanh', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi thiếu quyền',
     'Mở cửa sổ khai bổ sung nguyên nhân, xem mục 2.7.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu ở trạng thái Đang tạo.'),
    ('Nút Lưu và gửi', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Có bước xác nhận “Bạn đồng ý lưu và gửi?”.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
])

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn lập phiếu', 'System',
     'Before:\n– Kiểm tra quyền Xử lý yêu cầu sửa chữa và điều kiện của phiếu yêu cầu gốc (đang '
     'Chờ xử lý, đúng phòng tiếp nhận, chưa có phiếu xử lý).\n'
     '– Không thỏa mãn → hiển thị “Không thể lập phiếu xử lý cho phiếu yêu cầu này” và quay về '
     'danh sách.\n'
     'After:\n– Chép sẵn thông tin khách hàng và toàn bộ thiết bị; các ô Nguyên nhân, Hành động, '
     'Nội dung xử lý để trống.'),
    ('Chọn Hành động “Tư vấn điện thoại”', 'Change',
     'After:\n– Hiện ô Nội dung xử lý ngay dưới, bắt buộc nhập.'),
    ('Chọn Hành động khác', 'Change',
     'After:\n– Ẩn và xóa trắng ô Nội dung xử lý của dòng đó.'),
    ('Bấm Lưu nháp', 'Click',
     'During:\n– Dòng có Hành động là Tư vấn điện thoại mà Nội dung xử lý trống → hiển thị “Bắt '
     'buộc phải nhập”.\n'
     '– Nếu có lỗi thì không thực hiện bước After.\n'
     'After:\n– Sinh số phiếu, ghi phiếu ở trạng thái Đang tạo.\n'
     '– Ghi một dòng lịch sử “Tạo mới”.\n'
     '– Hiển thị “Lưu thành công” và quay về danh sách.'),
    ('Bấm Lưu và gửi', 'Click',
     'Before:\n– Hiển thị hộp xác nhận “Bạn đồng ý lưu và gửi?”; chọn Hủy thì dừng.\n'
     'During:\n– Thiếu Nguyên nhân hoặc Hành động ở bất kỳ dòng nào → hiển thị “Bắt buộc phải '
     'nhập” tại đúng dòng.\n'
     '– Dòng thiết bị khách khai tự do chưa chọn hàng hóa tương đương → hiển thị “Phải chọn hàng '
     'hóa tương đương”.\n'
     '– Trùng nguyên nhân giữa hai dòng của cùng một thiết bị → hiển thị “Bị trùng nguyên nhân của '
     'cùng thiết bị”.\n'
     '– Phiếu không còn thiết bị nào → hiển thị “Yêu cầu phải có ít nhất 1 thiết bị”.\n'
     '– Nếu có lỗi thì không thực hiện bước After.\n'
     'After:\n– Ghi phiếu ở trạng thái Chờ CCTT (hoặc Đã tư vấn điện thoại nếu mọi thiết bị đều '
     'chọn Tư vấn điện thoại).\n'
     '– Cập nhật phiếu yêu cầu gốc sang Đã xử lý (hoặc Đã tư vấn điện thoại) kèm Người xử lý và '
     'Ngày xử lý.\n'
     '– Gửi thông báo cho người có quyền Tạo phiếu cung cấp thông tin cùng công ty.\n'
     '– Hiển thị “Gửi phiếu xử lý thành công” và quay về danh sách.'),
])

# ------------------------------------------------------------------- 2.5 Sua
d.h3('2.5 Sửa phiếu xử lý')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Sửa phiếu xử lý', 'crud',
            [('include', 'Kiểm tra phiếu đang ở trạng thái Đang tạo'),
             ('include', 'Kiểm tra người sửa là người lập phiếu')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-05 Sửa phiếu xử lý')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử. Chỉ bổ sung điều kiện được phép sửa của màn hình tại phần mô tả chi tiết.',
           anchor='create')
d.intro_table(
    ten='Sửa phiếu xử lý',
    mota='Chỉnh sửa phiếu chưa gửi đi hoặc phiếu bị trả lại: chọn lại nguyên nhân, đổi hành động, '
         'sửa nội dung xử lý rồi lưu nháp tiếp hoặc gửi lại.',
    tacnhan='Người xử lý (người lập phiếu)',
    dieukien='Phiếu ở trạng thái Đang tạo và do chính người đăng nhập lập.',
    chinh='1. Người dùng bấm Sửa ở dòng phiếu hoặc ở màn chi tiết.\n'
          '2. Hệ thống mở màn sửa với dữ liệu hiện có.\n'
          '3. Người dùng chỉnh sửa và bấm Lưu nháp hoặc Lưu và gửi.\n'
          '4. Hệ thống kiểm tra dữ liệu, ghi lại phiếu và ghi lịch sử thay đổi.',
    phu='• Phiếu đã gửi đi hoặc không phải của mình → nút Sửa không hiển thị; vào thẳng bằng đường '
        'dẫn thì hệ thống chuyển về màn chi tiết và từ chối cập nhật.\n'
        '• Các nhánh lỗi nhập liệu giống mục 2.4.',
    dacbiet='Số phiếu, phiếu yêu cầu gốc và thông tin khách hàng không đổi được.')

d.p('2.5.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu => Chỉnh sửa', shot=shot('06-sua.png'), shot_caption='Màn Sửa phiếu xử lý')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.p('Bố cục và danh sách trường giống mục 2.4.4, khác ở các điểm sau:')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–',
     'Sửa phiếu xử lý yêu cầu: <số phiếu>', 'Có kèm số phiếu.'),
    ('Khối thông tin yêu cầu', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu đã lưu',
     'Toàn bộ chỉ đọc như khi lập mới.'),
    ('Bảng thiết bị', 'Table/Grid', 'Enable', '–', 'Như mục 2.4', 'Theo dữ liệu đã lưu',
     'Sửa nguyên nhân, hành động, nội dung xử lý, tệp đính kèm; xóa được dòng.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Kiểm tra phiếu ở trạng thái Đang tạo và do chính mình lập.\n'
     '– Không thỏa mãn → nút không hiển thị; truy cập thẳng bằng đường dẫn thì chuyển về màn chi '
     'tiết.\n'
     'After:\n– Mở màn sửa với dữ liệu hiện có.'),
    ('Bấm Lưu nháp / Lưu và gửi ở màn sửa', 'Click',
     'Before:\n– Máy chủ kiểm tra lại điều kiện sửa; không thỏa mãn thì từ chối với thông báo '
     '“Phiếu đã gửi đi hoặc không thuộc quyền chỉnh sửa của bạn, không thể cập nhật.”\n'
     'During:\n– Kiểm tra dữ liệu như mục 2.4.\n'
     'After:\n– Ghi lại phiếu; ghi một dòng lịch sử “Thay đổi thông tin”.'),
])

# --------------------------------------------------------------- 2.6 Chi tiet
d.h3('2.6 Xem chi tiết phiếu xử lý')

d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung bố cục các khối và điều kiện hiện / ẩn từng nút của màn hình tại phần mô tả chi tiết.',
           anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu xử lý',
    mota='Xem toàn bộ thông tin phiếu ở chế độ chỉ đọc, kèm khối Lịch sử và các thao tác phù hợp '
         'với trạng thái phiếu.',
    tacnhan='Người xử lý; Người lập phiếu cung cấp thông tin',
    dieukien='Phiếu nằm trong phạm vi xem của người đăng nhập.',
    chinh='1. Người dùng bấm số phiếu xử lý ở danh sách.\n'
          '2. Hệ thống kiểm tra quyền xem phiếu.\n'
          '3. Hệ thống hiển thị thông tin yêu cầu, danh sách thiết bị và khối Lịch sử.\n'
          '4. Thanh nút cuối trang hiển thị đúng các thao tác mà người dùng được phép làm.',
    phu='• Không có quyền xem phiếu hoặc phiếu không tồn tại → chuyển sang trang báo không tìm '
        'thấy.\n'
        '• Phiếu từng bị Không duyệt → hiện dòng lý do.',
    dacbiet=None)

d.p('2.6.2 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu => Xem chi tiết', shot=shot('04-chi-tiet.png'), shot_caption='Màn Chi tiết phiếu xử lý')
d.figure(shot('10-chi-tiet-cho-cctt.png'),
         'Phiếu ở trạng thái Chờ CCTT — có thêm hai nút Tạo phiếu cung cấp thông tin và Không duyệt',
         width_in=6.2)

d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Chi tiết phiếu xử lý yêu cầu: <số phiếu>',
     'Kèm số phiếu.'),
    ('Dòng người xử lý', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Ghi người lập phiếu và thời điểm lập, ở góc phải khối thông tin yêu cầu.'),
    ('Các ô thông tin yêu cầu', 'Textbox', 'Disable', '–', 'Theo dữ liệu', 'Chỉ đọc.'),
    ('Bảng thiết bị', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Nguyên nhân liệt kê từng dòng; Hành động hiện kèm dòng phụ Nội dung xử lý nếu có.'),
    ('Khối Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn', 'Bấm “Xem lịch sử” để mở.'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', 'Điều kiện như mục 2.5.'),
    ('Nút Tạo phiếu cung cấp thông tin', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
     'Điều kiện như mục 2.8.'),
    ('Nút Không duyệt', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', 'Điều kiện như mục 2.9.'),
    ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', 'Điều kiện như mục 2.10.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Luôn hiển thị.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Trở về danh sách.'),
], required=False)

d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm số phiếu ở danh sách', 'Click',
     'Before:\n– Kiểm tra quyền xem phiếu: người lập luôn xem được; sau đó xét quyền tổng công ty, '
     'công ty, phòng ban.\n'
     '– Không thỏa mãn → chuyển sang trang báo không tìm thấy.\n'
     'After:\n– Hiển thị chi tiết phiếu và các nút phù hợp.'),
])

# --------------------------------------------------- 2.7 Them nhanh nguyen nhan
d.h3('2.7 Thêm nhanh nguyên nhân')

d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Thêm nhanh nguyên nhân', 'crud',
            [('include', 'Kiểm tra quyền Quản lý danh mục công việc - lỗi thiết bị'),
             ('extend', 'Gắn nguyên nhân mới vào hàng hóa đang chọn')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-07 Thêm nhanh nguyên nhân')

d.p('2.7.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới danh mục, Validate dữ liệu và Thông báo. Chỉ bổ sung các trường của cửa sổ thêm nhanh nguyên nhân tại phần mô tả chi tiết.',
           anchor='create')
d.intro_table(
    ten='Thêm nhanh công việc / lỗi thiết bị',
    mota='Khai bổ sung một nguyên nhân ngay trong lúc lập phiếu, không phải rời màn sang danh mục. '
         'Nguyên nhân mới được gắn luôn cho hàng hóa của dòng đang thao tác.',
    tacnhan='Người xử lý có quyền Quản lý danh mục công việc - lỗi thiết bị',
    dieukien='Đang ở màn lập hoặc sửa phiếu xử lý.',
    chinh='1. Người dùng bấm Thêm nhanh ở ô Nguyên nhân của một dòng thiết bị.\n'
          '2. Hệ thống mở cửa sổ khai nguyên nhân, hiển thị tên hàng hóa đang thao tác.\n'
          '3. Người dùng nhập Loại công việc / lỗi và Tên công việc / Tình trạng lỗi, các ô còn '
          'lại tùy chọn.\n'
          '4. Người dùng bấm Lưu; hệ thống ghi vào danh mục, gắn cho hàng hóa và tự tích chọn vào '
          'ô Nguyên nhân của dòng đó.',
    phu='• Thiếu trường bắt buộc → báo “Bắt buộc phải nhập” ngay dưới ô.\n'
        '• Không có quyền → nút Thêm nhanh không hiển thị.',
    dacbiet='Nguyên nhân khai ở đây chỉ gắn cho hàng hóa đang chọn; muốn dùng cho hàng hóa khác '
            'thì khai tiếp trong màn danh mục.')

d.p('2.7.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu => Tạo mới / Chỉnh sửa => Thêm nhanh', modal='Thêm nhanh công việc / lỗi thiết bị', shot=shot('09-them-nhanh-nguyen-nhan.png'), shot_caption='Cửa sổ Thêm nhanh công việc / lỗi thiết bị')

d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Loại công việc / lỗi', 'Dropdown', 'Enable', 'Danh sách 6 giá trị', 'Có', 'Trống',
     'Gồm Lỗi đã xác định, Lỗi chưa xác định, Lắp đặt bàn giao, Thiết kế nền móng, Tư vấn khảo '
     'sát, Giám sát thi công.'),
    ('Tên công việc / Tình trạng lỗi', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
     'Thiếu thì báo “Bắt buộc phải nhập”.'),
    ('Định mức công', 'Number', 'Enable', '≥ 0', 'Không', 'Trống', '–'),
    ('Định mức đàm phán giá (%)', 'Number', 'Enable', '0 – 100', 'Không', 'Trống', '–'),
    ('VAT (%)', 'Number', 'Enable', '0 – 100', 'Không', 'Trống', '–'),
    ('Đơn giá bán', 'Number', 'Enable', '≥ 0', 'Không', 'Trống', '–'),
    ('Hệ số công nghệ', 'Number', 'Enable', '≥ 0', 'Không', 'Trống', '–'),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
    ('Nút Lưu / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
])

d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý danh mục công việc - lỗi thiết bị; không có quyền thì từ '
     'chối và báo không có quyền.\n'
     'During:\n– Loại công việc / lỗi hoặc Tên công việc trống → hiển thị “Bắt buộc phải nhập”.\n'
     'After:\n– Ghi nguyên nhân mới vào danh mục, gắn cho hàng hóa của dòng đang thao tác.\n'
     '– Tự tích chọn nguyên nhân đó vào ô Nguyên nhân của dòng và đóng cửa sổ.'),
])

# --------------------------------------------- 2.8 Tao phieu cung cap thong tin
d.h3('2.8 Tạo phiếu cung cấp thông tin')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Tạo phiếu cung cấp thông tin', 'action',
            [('include', 'Kiểm tra quyền Tạo phiếu cung cấp thông tin'),
             ('include', 'Kiểm tra phiếu đang ở trạng thái Chờ CCTT')],
            caption='Biểu đồ Use Case — FR-08 Tạo phiếu cung cấp thông tin')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Quy tắc điều hướng sang chứng từ tiếp theo và Phân quyền. Chỉ bổ sung điều kiện lập phiếu cung cấp thông tin của màn hình tại phần mô tả chi tiết.',
           anchor='notice')
d.intro_table(
    ten='Tạo phiếu cung cấp thông tin làm báo giá',
    mota='Mở màn lập Phiếu cung cấp thông tin làm báo giá với dữ liệu lấy từ phiếu xử lý này. Đây '
         'là bước chuyển tiếp sang chứng từ thứ ba của luồng dịch vụ.',
    tacnhan='Người lập phiếu cung cấp thông tin (người có quyền Tạo phiếu cung cấp thông tin)',
    dieukien='Phiếu ở trạng thái Chờ CCTT và người dùng có quyền Tạo phiếu cung cấp thông tin.',
    chinh='1. Người dùng bấm Tạo phiếu cung cấp thông tin.\n'
          '2. Hệ thống mở màn lập Phiếu cung cấp thông tin làm báo giá.\n'
          '3. Người dùng hoàn thiện và lưu (đặc tả ở tài liệu của màn đó).',
    phu='• Phiếu không ở trạng thái Chờ CCTT → nút không hiển thị.\n'
        '• Không có quyền → nút không hiển thị.',
    dacbiet='Thao tác này KHÔNG ràng buộc phòng ban: người có quyền là làm được, không cần thuộc '
            'phòng tiếp nhận.')

d.p('2.8.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu => Tạo phiếu cung cấp thông tin', shot=shot('10-chi-tiet-cho-cctt.png'), shot_caption='Thanh nút của phiếu đang ở trạng thái Chờ CCTT')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Tạo phiếu cung cấp thông tin', 'Icon Button / Button', 'Enable / Ẩn', '–',
     'Theo điều kiện', 'Có ở cột Hành động và ở thanh nút cuối màn chi tiết.'),
    ('Menu Hành động khác', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Chứa các thao tác còn lại: Không duyệt, In, Lịch sử.'),
], required=False)

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tạo phiếu cung cấp thông tin', 'Click',
     'Before:\n– Kiểm tra quyền và trạng thái phiếu Chờ CCTT.\n'
     '– Không thỏa mãn → nút không hiển thị.\n'
     'After:\n– Mở màn lập Phiếu cung cấp thông tin làm báo giá gắn với phiếu xử lý này.'),
    ('Phiếu cung cấp thông tin được lưu nháp', 'System',
     'After:\n– Phiếu xử lý chuyển sang trạng thái Đang CCTT.'),
    ('Phiếu cung cấp thông tin được gửi đi làm báo giá', 'System',
     'After:\n– Phiếu xử lý chuyển sang trạng thái Đã CCTT, ghi Người xử lý và Ngày xử lý.'),
])

# ------------------------------------------------------------ 2.9 Khong duyet
d.h3('2.9 Không duyệt phiếu xử lý')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Không duyệt phiếu xử lý', 'action',
            [('include', 'Kiểm tra quyền Tạo phiếu cung cấp thông tin'),
             ('include', 'Nhập lý do không duyệt'),
             ('extend', 'Gửi thông báo cho người lập phiếu')],
            caption='Biểu đồ Use Case — FR-09 Không duyệt phiếu xử lý')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc thao tác trạng thái, Thông báo và Quy tắc ghi lịch sử. Chỉ bổ sung điều kiện không duyệt và tác động lên trạng thái phiếu tại phần mô tả chi tiết.',
           anchor='notice')
d.intro_table(
    ten='Không duyệt phiếu xử lý',
    mota='Trả phiếu về cho người xử lý khi thông tin chưa đủ để làm báo giá, kèm lý do để họ sửa '
         'lại và gửi lần nữa.',
    tacnhan='Người lập phiếu cung cấp thông tin',
    dieukien='Phiếu ở trạng thái Chờ CCTT và người dùng có quyền Tạo phiếu cung cấp thông tin.',
    chinh='1. Người dùng bấm Không duyệt ở dòng phiếu hoặc màn chi tiết.\n'
          '2. Hệ thống mở cửa sổ Không duyệt phiếu xử lý yêu cầu.\n'
          '3. Người dùng nhập lý do và bấm Không duyệt.\n'
          '4. Hệ thống chuyển phiếu về trạng thái Đang tạo, lưu lý do và báo cho người lập phiếu.',
    phu='• Không nhập lý do → báo “Bắt buộc phải nhập”.\n'
        '• Phiếu đã đổi trạng thái ở nơi khác → hệ thống từ chối và báo phiếu không ở trạng thái '
        'Chờ CCTT nên không thể từ chối.',
    dacbiet='Phiếu trở lại Đang tạo nên chỉ người lập nhìn thấy; phiếu yêu cầu gốc KHÔNG bị đổi '
            'trạng thái theo.')

d.p('2.9.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu => Không duyệt', modal='Không duyệt phiếu xử lý yêu cầu', shot=shot('11-khong-duyet.png'), shot_caption='Cửa sổ Không duyệt phiếu xử lý yêu cầu')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Không duyệt phiếu xử lý yêu cầu',
     'Kèm dòng phụ ghi số phiếu.'),
    ('Dòng giải thích', 'Label', 'Read-only', '–', '–', 'Hiển thị',
     'Nêu rõ phiếu sẽ trở về trạng thái Đang tạo để người xử lý sửa lại.'),
    ('Lý do không duyệt', 'Textarea', 'Enable', '0–1000 ký tự', 'Có', 'Trống',
     'Gợi ý “Nhập lý do không duyệt”.'),
    ('Nút Không duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Màu đỏ, nhóm thao tác nguy hiểm.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không thay đổi gì.'),
])

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Không duyệt trong cửa sổ', 'Click',
     'Before:\n– Kiểm tra quyền Tạo phiếu cung cấp thông tin; không có quyền thì từ chối và báo '
     'không có quyền.\n'
     'During:\n– Lý do trống → hiển thị “Bắt buộc phải nhập”.\n'
     '– Phiếu không ở trạng thái Chờ CCTT → hiển thị “Phiếu không ở trạng thái Chờ CCTT nên không '
     'thể từ chối.”\n'
     '– Nếu có lỗi thì không thực hiện bước After.\n'
     'After:\n– Chuyển phiếu về trạng thái Đang tạo và lưu lý do.\n'
     '– Ghi một dòng lịch sử nhóm “Thay đổi trạng thái” kèm lý do.\n'
     '– Gửi thông báo cho người lập phiếu.\n'
     '– Hiển thị “Không duyệt phiếu thành công”.'),
])

# ------------------------------------------------------------------- 2.10 Xoa
d.h3('2.10 Xóa phiếu xử lý')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xóa phiếu xử lý', 'crud',
            [('include', 'Kiểm tra phiếu Đang tạo do chính mình lập'),
             ('include', 'Trả phiếu yêu cầu gốc về Chờ xử lý')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-10 Xóa phiếu xử lý')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Xóa, Thông báo và Quy định xác nhận. Chỉ bổ sung điều kiện được phép xóa và tác động lên phiếu yêu cầu gốc tại phần mô tả chi tiết.',
           anchor='delete')
d.intro_table(
    ten='Xóa phiếu xử lý',
    mota='Xóa hẳn phiếu chưa gửi đi cùng toàn bộ dòng thiết bị, đồng thời trả phiếu yêu cầu gốc về '
         'trạng thái Chờ xử lý để lập lại từ đầu.',
    tacnhan='Người xử lý (người lập phiếu)',
    dieukien='Phiếu ở trạng thái Đang tạo và do chính người đăng nhập lập.',
    chinh='1. Người dùng bấm Xóa ở dòng phiếu hoặc màn chi tiết.\n'
          '2. Hệ thống hiển thị hộp xác nhận có ghi số phiếu.\n'
          '3. Người dùng bấm Xóa để xác nhận.\n'
          '4. Hệ thống xóa phiếu, trả phiếu yêu cầu gốc về Chờ xử lý và nạp lại danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xóa gì.\n'
        '• Phiếu đã gửi đi → nút không hiển thị; gọi thẳng chức năng thì hệ thống từ chối.',
    dacbiet='Xóa phiếu xử lý sẽ xóa cả Người xử lý và Ngày xử lý đã ghi trên phiếu yêu cầu gốc, để '
            'phiếu gốc lập lại được phiếu xử lý mới.')

d.p('2.10.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu => Xóa', modal='Xác nhận xóa', shot=shot('16-xac-nhan-xoa.png'), shot_caption='Hộp xác nhận xóa phiếu xử lý')

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', 'Cố định.'),
    ('Nội dung', 'Label', 'Read-only', 'Bạn có chắc muốn xóa phiếu “<số phiếu>”?',
     'Có ghi rõ số phiếu để tránh xóa nhầm.'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
], required=False, scope=False)

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xóa ở hộp xác nhận', 'Click',
     'Before:\n– Máy chủ kiểm tra lại phiếu ở trạng thái Đang tạo và do chính mình lập.\n'
     '– Không thỏa mãn → từ chối với thông báo “Chỉ được xóa phiếu ở trạng thái Đang tạo do chính '
     'bạn tạo.”\n'
     'After:\n– Xóa phiếu cùng toàn bộ dòng thiết bị và nguyên nhân đã chọn.\n'
     '– Trả phiếu yêu cầu gốc về trạng thái Chờ xử lý, xóa Người xử lý và Ngày xử lý trên phiếu gốc.\n'
     '– Ghi một dòng lịch sử “Xóa”; hiển thị “Xóa thành công” và nạp lại danh sách.'),
])

# ------------------------------------------------------------------ 2.11 In
d.h3('2.11 In phiếu và in danh sách')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'In phiếu và in danh sách', 'io',
            [('include', 'Dựng bản in theo mẫu của công ty'),
             ('extend', 'Chặn in khi danh sách vượt 2.000 dòng')],
            caption='Biểu đồ Use Case — FR-11 In phiếu và in danh sách')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc In và Mẫu in chứng từ. Chỉ bổ sung nội dung bản in và giới hạn in danh sách của màn hình tại phần mô tả chi tiết.',
           anchor='notice')
d.intro_table(
    ten='In phiếu xử lý và in danh sách',
    mota='Dựng bản in một phiếu hoặc bản in danh sách theo bộ lọc đang áp dụng, xem trước ngay '
         'trên màn hình rồi gửi ra máy in.',
    tacnhan='Người xử lý; Người lập phiếu cung cấp thông tin',
    dieukien='Với bản in một phiếu: phiếu nằm trong phạm vi xem của người dùng.',
    chinh='1. Người dùng bấm In ở dòng phiếu, ở màn chi tiết, hoặc bấm In danh sách.\n'
          '2. Hệ thống dựng nội dung theo mẫu in của công ty ghi trên chứng từ.\n'
          '3. Cửa sổ xem trước hiển thị bản in.\n'
          '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
    phu='• In danh sách mà kết quả lọc vượt 2.000 dòng → hệ thống không dựng bản in, chỉ hiện lời '
        'nhắc thu hẹp bộ lọc hoặc dùng Xuất Excel.\n'
        '• Không có quyền xem phiếu → hệ thống từ chối in.',
    dacbiet='Bản in một phiếu có thêm hai cột Nguyên nhân và Hành động — đây là phần thông tin mà '
            'phiếu yêu cầu gốc không có.')

d.p('2.11.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu => In', modal='Xem trước phiếu xử lý yêu cầu', shot=shot('05-ban-in.png'), shot_caption='Xem trước bản in một phiếu xử lý')
d.figure(shot('15-in-danh-sach.png'), 'Xem trước bản in danh sách theo bộ lọc', width_in=6.2)

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In (từng phiếu)', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Có ở cột Hành động và ở thanh nút cuối màn chi tiết.'),
    ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị', 'Trên thanh công cụ danh sách.'),
    ('Cửa sổ xem trước', 'Modal', 'Hiển thị', '–', 'Ẩn',
     'Tiêu đề “Xem trước phiếu xử lý yêu cầu” hoặc “Xem trước danh sách phiếu xử lý yêu cầu”.'),
    ('Nút In trong cửa sổ', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở hộp thoại in của trình duyệt; bản in không kèm nút và khung viền.'),
    ('Lời nhắc vượt trần in', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
     'Nền vàng, ghi rõ số dòng thực tế và mức tối đa 2.000 dòng.'),
    ('Nội dung bản in một phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tiêu đề công ty; số phiếu xử lý, phiếu yêu cầu, người yêu cầu, phòng yêu cầu, ngày nhận yêu '
     'cầu, khách hàng, người liên hệ, địa chỉ sửa chữa; bảng thiết bị 9 cột; khối ký của người lập.'),
    ('Nội dung bản in danh sách', 'Table/Grid', 'Read-only', '–', 'Theo bộ lọc',
     'Hai dòng Thời gian và Phòng xử lý yêu cầu (ghi “Tất cả” khi không lọc); bảng 10 cột.'),
], required=False)

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In ở một phiếu', 'Click',
     'Before:\n– Kiểm tra quyền xem phiếu; không có quyền thì từ chối.\n'
     'During:\n– Dựng nội dung theo mẫu in, lấy tiêu đề công ty theo công ty ghi trên chứng từ.\n'
     'After:\n– Mở cửa sổ xem trước.'),
    ('Bấm In danh sách', 'Click',
     'During:\n– Đếm số dòng khớp bộ lọc hiện tại.\n'
     '– Vượt 2.000 dòng → không dựng bản in, hiển thị lời nhắc thu hẹp bộ lọc.\n'
     'After:\n– Dựng bản in danh sách theo đúng bộ lọc và mở cửa sổ xem trước.'),
])

# ------------------------------------------------------------- 2.12 Xuat Excel
d.h3('2.12 Xuất Excel')

d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Xuất Excel', 'io',
            [('include', 'Chọn trường và thứ tự cột'),
             ('include', 'Tải dữ liệu theo từng đợt 2.000 dòng')],
            caption='Biểu đồ Use Case — FR-12 Xuất Excel')

d.p('2.12.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung danh sách trường được phép xuất riêng của màn hình tại phần mô tả chi tiết.',
           anchor='excel')
d.intro_table(
    ten='Xuất danh sách ra tệp Excel',
    mota='Xuất toàn bộ phiếu khớp bộ lọc hiện tại ra tệp Excel, với các cột và thứ tự cột do người '
         'dùng chọn.',
    tacnhan='Người xử lý; Người lập phiếu cung cấp thông tin',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ Chọn trường xuất file với 6 trường mặc định trong tổng số 14.\n'
          '3. Người dùng chọn trường theo thứ tự mong muốn rồi bấm Xuất file.\n'
          '4. Hệ thống tải dữ liệu theo từng đợt và hiển thị dòng tiến độ.\n'
          '5. Tệp được dựng và tải về máy người dùng.',
    phu='• Bỏ chọn hết trường → không xuất được.\n'
        '• Bộ lọc không ra dòng nào → hệ thống báo không có dữ liệu để xuất.\n'
        '• Trong lúc xuất, nút Xuất Excel bị khóa.',
    dacbiet='Tệp xuất theo đúng bộ lọc đang áp dụng, không giới hạn ở trang đang xem.')

d.p('2.12.3 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu => Xuất excel', modal='Chọn trường xuất file', shot=shot('03-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất file')

d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Trường xuất', 'Dropdown', 'Enable', 'Danh sách 14 trường', 'Có', '6 trường mặc định',
     'Thứ tự cột trong tệp chạy theo đúng thứ tự chọn.'),
    ('Dòng “Thứ tự cột trong file”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Bị khóa khi chưa chọn trường nào hoặc đang xuất.'),
    ('Dòng tiến độ', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện “Đã tải …/… dòng” rồi “Đang dựng file …/… dòng”.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ.'),
])

d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất file', 'Click',
     'During:\n– Chưa chọn trường nào → nút không dùng được.\n'
     '– Tải dữ liệu theo từng đợt 2.000 dòng trong phạm vi dữ liệu và bộ lọc hiện tại.\n'
     'After:\n– Dựng tệp Excel với cột STT ở đầu, tải về máy và hiển thị “Xuất Excel thành công”.'),
])

# ---------------------------------------------------------------- 2.13 Lich su
d.h3('2.13 Xem lịch sử thay đổi')

d.p('2.13.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung danh sách trường được theo dõi riêng của màn hình tại phần mô tả chi tiết.',
           anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu',
    mota='Xem ai đã làm gì với phiếu: tạo mới, sửa những trường nào, đổi trạng thái và lý do kèm theo.',
    tacnhan='Người xử lý; Người lập phiếu cung cấp thông tin',
    dieukien='Phiếu nằm trong phạm vi xem của người đăng nhập.',
    chinh='1. Người dùng chọn Lịch sử ở dòng phiếu, hoặc bấm Xem lịch sử ở khối Lịch sử trong màn '
          'chi tiết.\n'
          '2. Hệ thống nạp danh sách thao tác, mới nhất lên đầu.\n'
          '3. Người dùng có thể lọc theo loại hoạt động, người thực hiện và khoảng ngày.',
    phu='• Phiếu chưa có thao tác nào → hiện thông báo chưa có lịch sử.\n'
        '• Phiếu tạo từ hệ thống cũ không có lịch sử.',
    dacbiet='Thay đổi ở bảng thiết bị KHÔNG được ghi lịch sử, vì mỗi lần lưu là ghi lại toàn bộ '
            'bảng nên nhật ký sẽ nhiễu.')

d.p('2.13.2 Layout màn hình')
d.layout(menu='Phân hệ CSKH => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu => Lịch sử', shot=shot('12-lich-su.png'), shot_caption='Khối Lịch sử trong màn chi tiết')

d.p('2.13.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Dòng thời gian', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi mục gồm thời điểm, tên hành động, người thực hiện kèm phòng ban và khối thay đổi.'),
    ('Giá trị cũ / giá trị mới', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Giá trị cũ màu đỏ, giá trị mới màu xanh.'),
    ('Bộ lọc', 'Dropdown / Datepicker', 'Enable', 'Loại hoạt động, người thực hiện, khoảng ngày',
     'Trống', 'Loại hoạt động gồm Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', 'Nạp lại lịch sử.'),
    ('Nút Thu gọn / Xem lịch sử', 'Button', 'Enable', '–', 'Thu gọn',
     'Chỉ có ở khối Lịch sử trong màn chi tiết.'),
], required=False)

d.p('2.13.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở lịch sử', 'Click',
     'After:\n– Nạp danh sách thao tác của đúng phiếu đó, sắp xếp mới nhất lên đầu.'),
    ('Chọn điều kiện lọc rồi bấm Tìm kiếm', 'Click',
     'After:\n– Chỉ hiển thị các mục thỏa mãn; không gọi lại máy chủ.'),
])

# =================================================== PHAN 4. QUY TAC NGHIEP VU
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu xử lý yêu cầu; không lặp lại '
           'các quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại ')

d.rule_table([
    ('BR-01', 'Số phiếu sinh tự động',
     '– Số phiếu theo khuôn “<mã công ty>.PXL.<năm><6 chữ số>”, ví dụ TPE.PXL.2026005291.\n– Số phiếu do hệ thống sinh sau khi ghi phiếu, người dùng không nhập và không sửa được.\n– Không tra được mã công ty thì dùng mã mặc định TPE.', 'Lập phiếu'),
    ('BR-02', 'Bộ trạng thái của phiếu',
     '– Phiếu có 6 trạng thái: Đang tạo, Chờ CCTT, Đã CCTT, Chờ CCTT bổ sung, Đang CCTT, Đã tư vấn điện thoại.\n– Màn hình này trực tiếp tạo ra ba trạng thái: Đang tạo (Lưu nháp, hoặc bị Không duyệt trả về), Chờ CCTT (Lưu và gửi), Đã tư vấn điện thoại (mọi thiết bị chọn Tư vấn điện thoại).\n– Đang CCTT và Đã CCTT do màn Phiếu cung cấp thông tin làm báo giá ghi ngược về.\n– Trạng thái Chờ CCTT bổ sung chỉ tồn tại ở dữ liệu chuyển từ phần mềm ERP; nghiệp vụ hiện tại không sinh ra trạng thái này.', 'Toàn màn hình'),
    ('BR-03', 'Phiếu chỉ sinh ra từ phiếu yêu cầu',
     '– Màn hình không có nút Tạo mới. Phiếu xử lý chỉ lập được từ nút “Tạo phiếu xử lý yêu cầu” của một phiếu yêu cầu kiểm tra sửa chữa – bảo hành.\n– Điều kiện lập: phiếu yêu cầu đang ở Chờ xử lý, đúng phòng tiếp nhận của người đăng nhập, người đăng nhập có quyền Xử lý yêu cầu sửa chữa, và phiếu yêu cầu chưa có phiếu xử lý nào.\n– Mỗi phiếu yêu cầu chỉ lập được MỘT phiếu xử lý.', 'Lập phiếu'),
    ('BR-04', 'Bắt buộc nhập khác nhau giữa Lưu nháp và Lưu và gửi',
     '– Lưu nháp không bắt buộc Nguyên nhân và Hành động; đây là điểm khác có chủ đích so với phần mềm ERP (bên ERP bắt buộc như nhau ở cả hai nút).\n– Lưu và gửi bắt buộc: mỗi thiết bị phải có ít nhất một Nguyên nhân và một Hành động; thiết bị khách khai tự do phải chọn hàng hóa tương đương; phiếu phải còn ít nhất một thiết bị.\n– Riêng Nội dung xử lý là bắt buộc NGAY CẢ KHI Lưu nháp, nếu Hành động của dòng đó là Tư vấn điện thoại.\n– Không được chọn trùng nguyên nhân trong cùng một thiết bị.', 'Lập phiếu\nChỉnh sửa phiếu'),
    ('BR-05', 'Hành động “Tư vấn điện thoại” đóng luồng',
     '– Nếu MỌI thiết bị trên phiếu đều chọn Hành động Tư vấn điện thoại, phiếu chuyển sang trạng thái Đã tư vấn điện thoại, kể cả khi người dùng bấm Lưu nháp.\n– Cùng lúc đó phiếu yêu cầu gốc cũng chuyển sang Đã tư vấn điện thoại và luồng dịch vụ kết thúc ở đây — không có báo giá, không có hợp đồng.\n– Đây là điểm dễ hiểu nhầm: người dùng tưởng mình chỉ lưu nháp nhưng thực tế phiếu đã đóng.', 'Lập phiếu\nChỉnh sửa phiếu'),
    ('BR-06', 'Tác động ngược lên phiếu yêu cầu gốc',
     '– Phiếu xử lý chuyển sang Chờ CCTT → phiếu yêu cầu gốc chuyển sang Đã xử lý, ghi Người xử lý và Ngày xử lý.\n– Phiếu xử lý chuyển sang Đã tư vấn điện thoại → phiếu yêu cầu gốc cũng chuyển sang Đã tư vấn điện thoại.\n– Xóa phiếu xử lý → phiếu yêu cầu gốc trở lại Chờ xử lý và bị xóa Người xử lý, Ngày xử lý, để lập lại được phiếu xử lý mới.\n– Thao tác Không duyệt KHÔNG đổi trạng thái phiếu yêu cầu gốc.', 'Lập phiếu\nXóa phiếu'),
    ('BR-07', 'Nguyên nhân khai theo từng hàng hóa',
     '– Ô Nguyên nhân chỉ liệt kê những công việc / lỗi đã khai cho ĐÚNG hàng hóa của dòng đó, không phải toàn bộ danh mục.\n– Hàng hóa chưa khai nguyên nhân nào thì ô hiện dòng nhắc và nút Thêm nhanh.\n– Nguyên nhân đã bị khóa trong danh mục vẫn hiển thị ở phiếu đang dùng nó, kèm biểu tượng ổ khóa.', 'Lập phiếu\nChỉnh sửa phiếu'),
    ('BR-08', 'Điều kiện sửa và xóa',
     '– Chỉ sửa và xóa được phiếu ở trạng thái Đang tạo và do chính người đăng nhập lập.\n– Điều kiện được kiểm tra ở máy chủ, không chỉ ẩn nút trên giao diện.\n– Xóa phiếu là xóa cả dòng thiết bị và nguyên nhân đã chọn, không khôi phục được.', 'Chỉnh sửa phiếu\nXóa phiếu'),
    ('BR-09', 'Phiếu nháp là riêng tư',
     '– Phiếu ở trạng thái Đang tạo chỉ người lập nhìn thấy, kể cả người quản trị hệ thống.\n– Phiếu bị Không duyệt trở về Đang tạo nên cũng chỉ người lập nhìn thấy cho tới khi gửi lại.', 'Xem danh sách\nXem chi tiết phiếu'),
    ('BR-10', 'Thông báo cho người liên quan',
     '– Phiếu chuyển sang Chờ CCTT: thông báo gửi cho MỌI nhân viên có quyền Tạo phiếu cung cấp thông tin và CÙNG CÔNG TY với người thao tác — gửi theo quyền, không lọc theo phòng ban.\n– Phiếu bị Không duyệt: thông báo gửi cho người lập phiếu, kèm lý do. Đây là điểm bổ sung so với phần mềm ERP.\n– Lỗi gửi thông báo không làm hỏng nghiệp vụ: phiếu vẫn được lưu và đổi trạng thái bình thường.', 'Lập phiếu\nKhông duyệt phiếu'),
    ('BR-11', 'Ghi lịch sử thay đổi',
     '– Hệ thống ghi lịch sử cho các trường: số phiếu, tên khách hàng, người liên hệ, số điện thoại liên hệ, địa chỉ sửa chữa và ghi chú.\n– Đổi trạng thái được ghi riêng ở nhóm “Thay đổi trạng thái”; thao tác Không duyệt ghi kèm lý do.\n– Thay đổi ở bảng thiết bị không được ghi lịch sử.', 'Toàn màn hình'),
    ('BR-12', 'Giới hạn khi in danh sách',
     '– Bản in danh sách chỉ dựng được tối đa 2.000 dòng; vượt mức này hệ thống không dựng bản in mà nhắc người dùng thu hẹp bộ lọc hoặc dùng Xuất Excel.\n– Tiêu đề công ty trên mọi bản in lấy theo công ty ghi trên chứng từ, không theo người đang đăng nhập.', 'In phiếu và in danh sách'),
])

d.save()

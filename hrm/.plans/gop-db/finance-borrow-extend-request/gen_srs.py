# -*- coding: utf-8 -*-
"""Sinh SRS man "Phieu yeu cau gia han hang muon" (ma phieu PGHHM) theo FORM CHUAN 2026-08-28.

Khuon: ../finance-prepick-extend-request/gen_srs.py (man sinh doi gia han hang GIU) — nhung noi
dung khac han: man MUON khong co nhap, khong Sua / Xoa, 1 o "Ngay hen tra moi" cho ca phieu,
phieu bi tu choi sang trang thai rieng "Khong duyet".

Nguon (doc 05/10/2026, nhanh `develop` cua repo chinh — cac sua QA tu 02/10 lam thang vao develop,
worktree gop-db chua co #11550):
  BE  Modules/Finance/{Entities/BorrowExtend/*, Services/BorrowExtendRequest*Service.php,
      Http/Controllers/V1/BorrowExtendRequestController.php, Http/Requests/BorrowExtend/*,
      Resources/views/prints/borrow-extend-request*.blade.php, Routes/api.php}
  FE  pages/finance/borrow-extend-requests/*, components/subsystem-menu/{finance,sale-hub}.js
Anh chup that: ./borrow_extend_shots (1440x900, dev 05/10/2026, tai khoan DNS Admin).
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, '..', '..', '..', '.claude', 'skills',
                                'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(BASE, 'borrow_extend_shots')
OUT = os.path.join(BASE, 'SRS - Phieu yeu cau gia han hang muon.docx')


def shot(name):
    return os.path.join(SHOTS, name)


MENU = ('Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng => '
        'Phiếu yêu cầu gia hạn hàng mượn')
MENU_WAIT = ('Phân hệ Tài chính => Chờ duyệt => Hàng mượn chờ duyệt => '
             'Phiếu yêu cầu gia hạn hàng mượn chờ duyệt')
MENU_SALE = 'Phân hệ Bán hàng => Yêu cầu => Hàng hóa => YC gia hạn hàng mượn'

A_NV = 'Nhân viên mượn hàng'
A_DUYET = 'Trưởng phòng / Ban giám đốc / Kế toán kho'
A_ALL = 'Người dùng đã đăng nhập'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/borrow-extend-requests',
           full_url='https://<host-hrm>/finance/borrow-extend-requests?type=all',
           img_prefix='pghhm_')

# ============================================================== TRANG DAU
d.title_block('Phiếu yêu cầu gia hạn hàng mượn')

d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu yêu cầu gia hạn hàng mượn '
    '(mã phiếu PGHHM), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, luồng duyệt và phân quyền của màn hình.',
    'Làm rõ điều kiện để một phiếu yêu cầu xuất hàng mượn được đem ra gia hạn.',
    'Làm rõ luồng duyệt nhiều cấp: Trưởng phòng → Ban giám đốc (chỉ khi giá trị hàng còn nợ vượt '
    'hạn mức của công ty) → Kế toán kho.',
    'Làm rõ thời điểm ngày hẹn trả của phiếu mượn thực sự thay đổi: chỉ khi Kế toán kho duyệt ở '
    'bước cuối.',
    'Làm rõ phạm vi dữ liệu mà mỗi cấp quyền xem được và các lối vào màn hình.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu mượn', 'Phiếu yêu cầu xuất hàng mượn (mã PYCXH-xxxxx) đã được xuất kho — chứng từ ghi '
                   'nhận nhân viên đang mượn hàng của công ty, có một ngày hẹn trả.'),
    ('Phiếu gia hạn', 'Phiếu yêu cầu gia hạn hàng mượn (mã PGHHM-xxxxx) — đề nghị dời ngày hẹn '
                      'trả của đúng một phiếu mượn.'),
    ('Ngày hẹn trả (cũ)', 'Ngày hẹn trả đang có hiệu lực của phiếu mượn, được chụp lại vào phiếu '
                          'gia hạn tại thời điểm lập.'),
    ('Ngày hẹn trả mới', 'Ngày mà người lập đề nghị dời hạn trả tới. Một ô cho cả phiếu.'),
    ('Số ngày mượn tối đa', 'Cấu hình chung của hệ thống. Ngày hẹn trả mới không được vượt quá '
                            '“hôm nay + số ngày mượn tối đa” (gọi là ngày trần).'),
    ('Hạn mức giá trị hàng mượn', 'Cấu hình theo từng công ty. Giá trị hàng còn nợ của phiếu mượn '
                                  'lớn hơn hạn mức này thì phiếu gia hạn phải qua Ban giám đốc.'),
    ('Giá trị hàng còn nợ', 'Tổng trên mọi dòng hàng của phiếu mượn: (số lượng đã xuất − số lượng '
                            'đã trả) × đơn giá.'),
    ('TP / BGĐ / KT', 'Trưởng phòng / Ban giám đốc / Kế toán (kho) — các cấp duyệt của phiếu.'),
    ('Không duyệt', 'Trạng thái cuối của phiếu bị từ chối ở bất kỳ cấp nào. Phiếu dừng hẳn, không '
                    'sửa và không gửi lại được.'),
], widths=[1.7, 4.3])

# ========================================================= PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Màn hình KHÔNG có quyền riêng cho Tạo mới: mọi người dùng đã đăng nhập đều lập được phiếu '
    'gia hạn cho phiếu mượn của chính mình. Màn hình KHÔNG có chức năng Sửa và Xóa ở bất kỳ trạng '
    'thái nào, vì phiếu sinh ra là vào thẳng trạng thái Chờ TP duyệt (không có bản nháp).')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Trưởng phòng duyệt hàng mượn',
     'Nút TP duyệt và Từ chối với phiếu Chờ TP duyệt. Ngoài quyền còn phải cùng công ty với phiếu '
     'và quản lý phòng ban của phiếu (được phân công quản lý, tích “Quản lý tất cả phòng ban”, '
     'hoặc thuộc chính phòng ban đó).'),
    ('Q2', 'Ban giám đốc duyệt hàng mượn',
     'Nút BGĐ duyệt và Từ chối với phiếu Chờ BGĐ duyệt, cùng công ty.'),
    ('Q3', 'Kế toán kho',
     'Nút KT duyệt và Từ chối với phiếu Chờ KT duyệt, cùng công ty; được sửa Ngày hẹn trả mới '
     'trước khi duyệt. Là quyền duy nhất nhìn thấy mục menu “Hàng mượn chờ duyệt”.'),
], widths=[0.8, 2.0, 3.2])

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu hàng mượn theo tổng công ty',
     'Toàn bộ phiếu của mọi công ty (Super Admin cũng vậy).'),
    ('V2', 'Xem phiếu hàng mượn theo công ty',
     'Phiếu thuộc công ty của người đăng nhập, cộng phiếu do chính mình lập.'),
    ('V3', 'Xem phiếu hàng mượn theo phòng ban',
     'Phiếu thuộc các phòng ban người đăng nhập quản lý và phòng ban của chính mình, cộng phiếu '
     'do chính mình lập.'),
    ('—', '(không có cấp nào)', 'Chỉ phiếu do chính mình lập.'),
], widths=[0.8, 2.0, 3.2])

d.p('Các quy tắc chung áp cho mọi cấp:')
d.bullets([
    'Ở lối vào thường, người dùng luôn thấy thêm những phiếu chính mình đã duyệt hoặc đã từ chối '
    '(ở bất kỳ cấp nào), kể cả khi không có quyền xem theo cấp.',
    'Trừ V1 và Super Admin, danh sách luôn bó về công ty của người đăng nhập.',
    'Người có một trong ba quyền Q1/Q2/Q3 mở xem được mọi phiếu cùng công ty bằng đường dẫn chi '
    'tiết (không nhất thiết có trong danh sách của họ).',
    'Phiếu Không duyệt xem theo đúng phạm vi như mọi trạng thái khác (không còn luật “chỉ người '
    'lập thấy” của hệ thống cũ).',
    'Lối vào “chờ duyệt” chỉ liệt kê phiếu đang chờ chính người dùng duyệt, luôn cùng công ty.',
])

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'V1/V2/V3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '✅', '✅', '✅ (theo cấp)', '✅ (phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tuỳ chỉnh cột hiển thị', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Lập phiếu gia hạn', '✅', '✅', '✅', '✅', '✅ (phiếu mượn của mình)'),
    ('FR-06 Chọn phiếu mượn cần gia hạn', '✅', '✅', '✅', '✅', '✅ (phiếu mượn của mình)'),
    ('FR-07 Xem chi tiết phiếu', '✅ (cùng công ty)', '✅ (cùng công ty)', '✅ (cùng công ty)',
     '✅ (trong phạm vi)', '✅ (phiếu của mình)'),
    ('FR-08 Duyệt phiếu', '✅ (Chờ TP duyệt)', '✅ (Chờ BGĐ duyệt)', '✅ (Chờ KT duyệt)', '❌',
     '❌'),
    ('FR-09 Từ chối phiếu', '✅ (Chờ TP duyệt)', '✅ (Chờ BGĐ duyệt)', '✅ (Chờ KT duyệt)', '❌',
     '❌'),
    ('FR-10 In phiếu / In danh sách', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-11 Xuất danh sách ra Excel', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-12 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('Sửa / Xóa phiếu', '❌', '❌', '❌', '❌', '❌ (màn không có chức năng này)'),
], widths=[1.7, 0.95, 0.95, 0.95, 0.85, 0.9])

# ================================================ PHAN 3. DAC TA CHI TIET
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_NV, [0, 1, 2]),
     (A_DUYET, [0, 2])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Lập phiếu gia hạn', 'crud'),
     ('FR-07', 'Xem chi tiết phiếu', 'view')],
    [('FR-02', 'Tìm kiếm và lọc phiếu', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-11', 'Xuất danh sách ra Excel', 'io', 'extend', [0], None),
     ('FR-06', 'Chọn phiếu mượn cần gia hạn', 'crud', 'include', [1], None),
     ('FR-08', 'Duyệt phiếu', 'action', 'extend', [2], None),
     ('FR-09', 'Từ chối phiếu', 'action', 'extend', [2], None),
     ('FR-10', 'In phiếu và danh sách', 'io', 'extend', [2], None),
     ('FR-12', 'Xem lịch sử thay đổi', 'view', 'extend', [2], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu yêu cầu gia hạn hàng mượn')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1 Xem danh sach
d.h3('2.1 Xem danh sách phiếu')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của màn Phiếu yêu cầu gia hạn hàng mượn tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách phiếu yêu cầu gia hạn hàng mượn',
    mota='Hiển thị bảng phiếu nằm trong phạm vi dữ liệu của người đăng nhập, kèm bộ lọc, phân '
         'trang và tổng số phiếu khớp bộ lọc. Màn có hai chế độ theo lối vào: danh sách thường và '
         'danh sách chờ duyệt.',
    tacnhan='Nhân viên mượn hàng; Trưởng phòng; Ban giám đốc; Kế toán kho; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập vào hệ thống.',
    chinh='1. Người dùng vào một trong các lối vào ở mục Layout màn hình.\n'
          '2. Hệ thống xác định chế độ theo lối vào: thường hoặc chờ duyệt.\n'
          '3. Chế độ thường: áp phạm vi theo cấp quyền xem, cộng thêm phiếu chính người dùng đã '
          'duyệt / từ chối. Chế độ chờ duyệt: chỉ lấy phiếu đang chờ chính người dùng duyệt.\n'
          '4. Hệ thống trả về trang đầu tiên (10 dòng), tổng số phiếu và danh sách trạng thái.\n'
          '5. Bảng hiển thị dữ liệu; dòng “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện dòng “Không có dữ liệu phù hợp.”.\n'
        '• Tham số chế độ trên thanh địa chỉ bị sửa thành giá trị lạ hoặc bị xoá → hệ thống coi '
        'là chế độ thường, vẫn áp phạm vi quyền (không lộ toàn bộ phiếu công ty như hệ thống cũ).\n'
        '• Đang ở màn mà bấm sang lối vào khác → danh sách tự nạp lại theo chế độ mới, về trang 1.\n'
        '• Người không có quyền duyệt nào mở chế độ chờ duyệt → chỉ thấy phiếu mình lập.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU)
d.p('Hiển thị: chế độ thường — phiếu trong phạm vi quyền của người đăng nhập. Tiêu đề '
    '“Phiếu yêu cầu gia hạn hàng mượn”.')
d.p('Menu: ' + MENU_SALE)
d.p('Hiển thị: giống hệt lối vào ở phân hệ Tài chính (cùng chế độ thường).')
d.p('Menu: ' + MENU_WAIT)
d.p('Hiển thị: chế độ chờ duyệt — chỉ phiếu đang chờ chính người đăng nhập duyệt. Tiêu đề '
    '“Phiếu yêu cầu gia hạn hàng mượn chờ duyệt”. Mục menu này chỉ hiện với người có quyền '
    'Kế toán kho.')
d.figure(shot('01-danh-sach.png'), 'Màn Phiếu yêu cầu gia hạn hàng mượn lúc mới truy cập',
         width_in=6.2)

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Phiếu yêu cầu gia hạn hàng mượn',
     'Chế độ chờ duyệt thì thêm chữ “chờ duyệt” ở cuối.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở màn lập phiếu mới. Hiện với mọi người dùng đã đăng nhập.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở bản xem trước in danh sách theo đúng bộ lọc và chế độ đang áp.'),
    ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
     'Mở cửa sổ chọn trường xuất; bị khóa trong lúc đang xuất.'),
    ('Nút Tuỳ chỉnh cột', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cột cố định, không tắt được, đánh số liên tục theo trang.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'PGHHM-NNNNN', 'Theo dữ liệu',
     'Liên kết mở màn chi tiết. Cột cố định, sắp xếp được.'),
    ('Cột Phiếu mượn', 'Table/Grid', 'Read-only', 'PYCXH-NNNNN', 'Theo dữ liệu',
     'Liên kết mở màn chi tiết phiếu yêu cầu xuất hàng ở TAB MỚI.'),
    ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dạng “Họ tên - Mã phòng ban”, ví dụ “Nguyễn Văn Thắng - HN_KDTM”.'),
    ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Ngày hẹn trả cũ / Ngày hẹn trả mới', 'Table/Grid', 'Read-only', 'dd/mm/yyyy',
     'Theo dữ liệu', 'Cả hai cột sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only',
     'Chờ TP duyệt / Chờ BGĐ duyệt / Chờ KT duyệt / Đã duyệt / Không duyệt', 'Theo dữ liệu',
     'Ba trạng thái chờ màu cam; Đã duyệt màu xanh lá; Không duyệt màu đỏ.'),
    ('Cột Người duyệt / Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Cấp đóng dấu SAU CÙNG (Kế toán, không có thì Ban giám đốc, không có nữa '
     'thì Trưởng phòng), kể cả khi cấp đó từ chối. Chưa ai duyệt thì để trống. Ngày duyệt sắp '
     'xếp được.'),
    ('Cột Phòng ban / Ghi chú / Lý do từ chối', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
     'Bật lên trong cửa sổ Tuỳ chỉnh cột. Lý do từ chối lấy của cấp đã từ chối.'),
    ('Cột Hành động', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Cột cố định cuối bảng, chứa các nút thao tác của dòng; nút thứ ba trở đi gom vào menu ⋮ '
     '“Hành động khác”.'),
    ('Nút Duyệt / Từ chối trên dòng', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện khi phiếu đang chờ chính người dùng duyệt ở đúng cấp. Duyệt mở màn chi tiết để '
     'duyệt; Từ chối mở cửa sổ nhập lý do.'),
    ('Nút In / Lịch sử trên dòng', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'In mở bản xem trước của phiếu; Lịch sử mở cửa sổ lịch sử thay đổi.'),
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc trong phạm vi quyền.'),
    ('Phân trang', 'Pagination', 'Enable', '10 / 20 / 50 / 100', 'Trang 1, 10 dòng',
     'Có nút về đầu / lùi / số trang / tiến / về cuối và ô Số dòng/trang.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện dòng “Không có dữ liệu phù hợp.” khi không có phiếu nào khớp.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Hiển thị',
     'Hiện khi vào màn và trong lúc nạp lại dữ liệu.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Xác định chế độ theo lối vào; giá trị lạ coi là chế độ thường.\n'
     '– Xác định cấp quyền xem theo thứ tự ưu tiên tổng công ty → công ty → phòng ban → chỉ '
     'phiếu của mình.\n'
     'During:\n– Chế độ thường: áp phạm vi, cộng phiếu mình đã đóng dấu; bó về công ty mình trừ '
     'V1 và Super Admin.\n'
     '– Chế độ chờ duyệt: Kế toán kho lấy phiếu Chờ KT duyệt, Ban giám đốc lấy Chờ BGĐ duyệt, '
     'Trưởng phòng lấy Chờ TP duyệt của phòng ban mình quản lý; luôn cùng công ty.\n'
     '– Khôi phục bộ lọc đã lưu của người dùng nếu còn hiệu lực (10 phút).\n'
     'After:\n– Trả về trang 1, tổng số phiếu và danh sách 5 trạng thái để đổ vào ô lọc.'),
    ('Bấm vào mã phiếu', 'Click',
     'Before:\n– Kiểm tra người dùng có được xem phiếu này không.\n'
     '– Nếu không → hiển thị “Bạn không có quyền xem phiếu này” và không hiện nội dung.\n'
     'After:\n– Mở màn chi tiết của phiếu.'),
    ('Bấm vào mã phiếu mượn', 'Click',
     'After:\n– Mở màn chi tiết phiếu yêu cầu xuất hàng ở tab mới; tab danh sách giữ nguyên.'),
    ('Bấm tiêu đề cột có mũi tên sắp xếp', 'Click',
     'During:\n– Năm cột sắp xếp được: Mã phiếu, Ngày tạo, Ngày hẹn trả cũ, Ngày hẹn trả mới, '
     'Ngày duyệt. Ngày duyệt sắp theo đúng mốc đang hiển thị (cấp đóng dấu sau cùng).\n'
     'After:\n– Nạp lại danh sách từ trang 1 theo thứ tự mới, giữ nguyên bộ lọc.'),
    ('Bấm số trang / nút tiến lùi / đổi số dòng mỗi trang', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\n'
     'After:\n– Nạp lại dữ liệu trang mới; đổi số dòng thì về trang 1.'),
])

# ------------------------------------------------------------ 2.2 Tim kiem va loc
d.h3('2.2 Tìm kiếm và lọc phiếu')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các tiêu chí lọc riêng của màn '
           'Phiếu yêu cầu gia hạn hàng mượn tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách phiếu',
    mota='Thu hẹp danh sách theo mã phiếu, phiếu mượn, trạng thái, người tạo, người duyệt, '
         'hàng hóa, model, khoảng ngày tạo và khối công ty – phòng ban.',
    tacnhan='Nhân viên mượn hàng; Trưởng phòng; Ban giám đốc; Kế toán kho',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter), hoặc bấm '
          'Tìm kiếm nâng cao để mở bảng lọc.\n'
          '2. Người dùng chọn / nhập các tiêu chí cần lọc.\n'
          '3. Hệ thống nạp lại danh sách ngay khi một ô lọc nâng cao thay đổi.\n'
          '4. Bảng hiển thị kết quả và cập nhật lại tổng số phiếu.',
    phu='• Không có phiếu nào khớp → bảng hiện dòng “Không có dữ liệu phù hợp.”.\n'
        '• Bấm Làm mới → xóa toàn bộ tiêu chí, bỏ sắp xếp, nạp lại từ trang 1; vẫn giữ chế độ '
        '(thường / chờ duyệt) của lối vào.\n'
        '• Bộ lọc được ghi nhớ trong 10 phút; mở chi tiết rồi quay lại vẫn giữ điều kiện cũ.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-bo-loc-nang-cao.png'),
         shot_caption='Bảng lọc nâng cao đang mở')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Gợi ý “Tìm theo mã phiếu, người tạo...”. Tìm theo mã phiếu HOẶC họ tên người tạo; chỉ '
     'chạy khi bấm Tìm kiếm hoặc Enter. Từ khóa từ 2 ký tự thì phiếu khớp mã nhất xếp lên đầu.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', 'Hiển thị', 'Áp dụng ô tìm nhanh, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Xóa mọi tiêu chí lọc, bỏ sắp xếp và nạp lại danh sách.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Đang thu gọn',
     'Đóng / mở bảng lọc nâng cao; khi mở đổi nhãn thành “Ẩn tìm kiếm nâng cao”.'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ bật / tắt và sắp xếp thứ tự các ô lọc.'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Trống',
     'Chỉ hiện với V1 hoặc Super Admin. Biểu tượng ổ khóa cạnh nhãn bật / tắt hiển thị cả công '
     'ty đã khóa.'),
    ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban', 'Trống',
     'Chỉ hiện với V1, V2, V3 hoặc Super Admin; phụ thuộc công ty đã chọn. Lọc theo phòng ban '
     'GHI TRÊN PHIẾU.'),
    ('Mã phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Lọc theo mã phiếu chứa chuỗi nhập.'),
    ('Phiếu mượn', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Lọc theo mã phiếu yêu cầu xuất hàng mượn chứa chuỗi nhập.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 5 trạng thái', 'Trống',
     'Thứ tự theo vòng đời: Chờ TP duyệt, Chờ BGĐ duyệt, Chờ KT duyệt, Đã duyệt, Không duyệt.'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Người lập phiếu.'),
    ('Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống',
     'Khớp người đã đóng dấu ở BẤT KỲ cấp nào (TP, BGĐ, KT), không chỉ cấp đang hiện ở cột.'),
    ('Tên hàng hóa / Model', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Lọc phiếu có phiếu mượn chứa mặt hàng khớp; chỉ dò trên các dòng hàng đang hiển thị ở bảng '
     'Chi tiết.'),
    ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống',
     'Một ô chọn khoảng từ ngày → đến ngày, lấy trọn hai đầu mút; chỉ chọn một đầu thì lọc một '
     'chiều.'),
], required=False)

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Đổi giá trị một ô lọc nâng cao', 'Change',
     'During:\n– Ghi giá trị mới vào bộ tiêu chí đang áp.\n'
     'After:\n– Về trang 1 và nạp lại danh sách ngay, không cần bấm nút.'),
    ('Bấm nút Tìm kiếm / nhấn Enter ở ô tìm nhanh', 'Click',
     'After:\n– Áp thêm nội dung ô tìm nhanh, về trang 1 và nạp lại danh sách.'),
    ('Bấm nút Làm mới', 'Click',
     'During:\n– Đặt lại mọi ô lọc về trống và bỏ thứ tự sắp xếp.\n'
     'After:\n– Nạp lại danh sách từ trang 1, giữ nguyên chế độ của lối vào.'),
    ('Chọn lại Công ty', 'Change',
     'After:\n– Xóa giá trị Phòng ban đang chọn và nạp lại danh sách phòng ban tương ứng.'),
])

# ------------------------------------------------------------ 2.3 Cai dat bo loc
d.h3('2.3 Cài đặt bộ lọc')

d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc', 'view', (), actor=A_ALL,
            caption='Biểu đồ Use Case — FR-03 Cài đặt bộ lọc')

d.p('2.3.2 Giới thiệu')
d.rule_ref('- Bộ lọc và Cấu hình cột. Chỉ bổ sung phần riêng của màn Phiếu yêu cầu gia hạn hàng '
           'mượn tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc hiển thị',
    mota='Cho phép người dùng tự chọn những ô lọc muốn hiển thị và kéo sắp xếp lại thứ tự. '
         'Cấu hình lưu riêng theo từng người dùng và từng màn hình.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Cài đặt bộ lọc.\n'
          '2. Hệ thống mở cửa sổ liệt kê 9 ô lọc: Công ty – Phòng ban, Mã phiếu, Phiếu mượn, '
          'Trạng thái, Người tạo, Người duyệt, Tên hàng hóa, Model, Ngày tạo.\n'
          '3. Người dùng bỏ tích ô không dùng, kéo đổi thứ tự nếu cần.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho riêng người dùng và vẽ lại bảng lọc.',
    phu='• Bấm Khôi phục mặc định → đưa danh sách ô lọc về trạng thái ban đầu.\n'
        '• Bấm Đóng → giữ nguyên cấu hình cũ, không lưu thay đổi.',
    dacbiet='Cấu hình chỉ ảnh hưởng tới người dùng hiện tại, không ảnh hưởng người khác. Ô '
            'Công ty – Phòng ban dù được tích vẫn chỉ hiện khi người dùng có quyền tương ứng.')

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('03-cai-dat-bo-loc.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')

d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc',
     'Kèm dòng hướng dẫn “Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự…”.'),
    ('Danh sách ô lọc', 'Table/Grid', 'Enable', '9 mục', '–', 'Theo cấu hình đã lưu',
     'Mỗi mục gồm số thứ tự, tay kéo, ô tích và tên ô lọc.'),
    ('Ô tích từng mục', 'Button', 'Enable', '–', '–', 'Đang tích',
     'Bỏ tích thì ô lọc đó không hiện ở bảng lọc nâng cao.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình và đóng cửa sổ.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đưa về danh sách và thứ tự ban đầu.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
])

d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Cài đặt bộ lọc', 'Click',
     'After:\n– Mở cửa sổ với cấu hình hiện tại của người dùng.'),
    ('Kéo đổi vị trí một mục', 'Click',
     'After:\n– Cập nhật số thứ tự các mục; chưa ghi lại cho tới khi bấm Lưu.'),
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi cấu hình theo người dùng và theo màn hình.\n'
     'After:\n– Đóng cửa sổ và vẽ lại bảng lọc nâng cao theo cấu hình mới.'),
])

# ------------------------------------------------------------ 2.4 Tuy chinh cot
d.h3('2.4 Tuỳ chỉnh cột hiển thị')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view', (), actor=A_ALL,
            caption='Biểu đồ Use Case — FR-04 Tuỳ chỉnh cột hiển thị')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Cấu hình cột hiển thị. Chỉ bổ sung phần riêng của màn Phiếu yêu cầu gia hạn hàng '
           'mượn tại phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='Tuỳ chỉnh cột hiển thị của bảng danh sách',
    mota='Cho phép bật / tắt và kéo sắp xếp các cột của bảng. Các cột STT, Mã phiếu và Hành động '
         'bị khóa, luôn hiển thị.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Tuỳ chỉnh cột ở góc phải thanh công cụ.\n'
          '2. Hệ thống mở cửa sổ Tuỳ chỉnh cột với 14 cột.\n'
          '3. Người dùng bật / tắt cột, kéo đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình và vẽ lại bảng.',
    phu='• Bấm Đóng → giữ nguyên cấu hình cũ.\n'
        '• Cột bị khóa không bỏ tích và không kéo được.',
    dacbiet='Ba cột Phòng ban, Ghi chú và Lý do từ chối mặc định TẮT; người dùng tự bật khi cần. '
            'Màn không có cột Người cập nhật / Ngày cập nhật vì phiếu không sửa được.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tuỳ chỉnh cột', shot=shot('04-cau-hinh-cot.png'),
         shot_caption='Cửa sổ Tuỳ chỉnh cột')

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', '–'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '14 cột', '–', 'Theo cấu hình đã lưu',
     'STT, Mã phiếu, Phiếu mượn, Người tạo, Ngày tạo, Ngày hẹn trả cũ, Ngày hẹn trả mới, Trạng '
     'thái, Người duyệt, Ngày duyệt, Phòng ban, Ghi chú, Lý do từ chối, Hành động. Mỗi dòng gồm '
     'ô tích, tên cột và tay kéo.'),
    ('Cột bị khóa', 'Label', 'Read-only', '–', '–', 'Biểu tượng ổ khóa',
     'STT, Mã phiếu và Hành động luôn hiển thị, không tắt được.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình và vẽ lại bảng.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
])

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bỏ tích một cột', 'Change',
     'During:\n– Cột bị khóa thì không cho bỏ tích.\n'
     'After:\n– Đánh dấu cột sẽ ẩn; chưa ghi cho tới khi bấm Lưu.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Ghi cấu hình theo người dùng và vẽ lại bảng theo đúng thứ tự đã chọn.'),
])

# ------------------------------------------------------------ 2.5 Lap phieu
d.h3('2.5 Lập phiếu gia hạn')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Lập phiếu gia hạn hàng mượn', 'crud', (), actor=A_NV,
            caption='Biểu đồ Use Case — FR-05 Lập phiếu gia hạn')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng '
           'theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Lập phiếu yêu cầu gia hạn hàng mượn',
    mota='Lập phiếu đề nghị dời ngày hẹn trả của một phiếu mượn do chính người lập đứng tên. '
         'Phiếu không có bản nháp: bấm gửi là phiếu vào thẳng trạng thái Chờ TP duyệt.',
    tacnhan='Nhân viên mượn hàng; Người dùng đã đăng nhập',
    dieukien='Người lập có ít nhất một phiếu mượn đủ điều kiện gia hạn (xem BR-01).',
    chinh='1. Người dùng bấm nút Tạo mới ở màn danh sách.\n'
          '2. Hệ thống mở màn “Thêm yêu cầu gia hạn hàng mượn”; góc phải khối Thông tin chung ghi '
          'tên người đăng nhập và ngày hôm nay.\n'
          '3. Người dùng bấm Chọn phiếu và chọn một phiếu mượn (FR-06).\n'
          '4. Hệ thống điền Ngày hẹn trả hiện tại và nạp bảng Chi tiết hàng của phiếu mượn.\n'
          '5. Người dùng chọn Ngày hẹn trả mới, nhập Ghi chú, đính kèm file PDF nếu cần.\n'
          '6. Người dùng bấm Gửi duyệt.\n'
          '7. Hệ thống kiểm tra dữ liệu, sinh mã phiếu, ghi phiếu ở trạng thái Chờ TP duyệt và '
          'gửi thông báo cho Trưởng phòng.\n'
          '8. Hệ thống hiển thị “Yêu cầu của bạn đã được gửi” và quay về màn danh sách.',
    phu='• Chưa chọn phiếu mượn hoặc chưa chọn ngày → báo lỗi đỏ dưới ô và thông báo “Bạn chưa '
        'nhập đầy đủ thông tin.”, không gửi.\n'
        '• Ngày hẹn trả mới không sau ngày hẹn trả hiện tại / không sau hôm nay / vượt ngày '
        'trần → báo lỗi dưới ô, không gửi.\n'
        '• Phiếu mượn vừa có người khác lập yêu cầu gia hạn (hoặc vừa trả hết hàng) → báo “Không '
        'thể gia hạn yêu cầu này: …” kèm lý do cụ thể.\n'
        '• Bấm Lưu và tiếp tục → gửi phiếu đi y như Gửi duyệt rồi ở lại màn Tạo mới với form '
        'trắng để lập phiếu kế tiếp.\n'
        '• Rời màn khi đã chọn / nhập mà chưa gửi → hệ thống hỏi xác nhận rời trang.',
    dacbiet='Bảng Chi tiết chỉ để xem: mặt hàng đọc thẳng từ phiếu mượn, người lập không nhập số '
            'lượng. Công ty, phòng ban của phiếu chốt theo người lập TẠI THỜI ĐIỂM LẬP.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('06-tao-moi.png'),
         shot_caption='Màn Thêm yêu cầu gia hạn hàng mượn')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Người lập – Ngày lập', 'Label', 'Read-only', '–', '–', 'Người đăng nhập — ngày hiện tại',
     'Hiển thị ở góc phải khối Thông tin chung.'),
    ('Phiếu yêu cầu xuất hàng mượn', 'Textbox', 'Read-only', 'PYCXH-NNNNN', 'Có', 'Trống',
     'Gợi ý “Bấm Chọn phiếu để lấy phiếu mượn của bạn”; chỉ điền được qua nút Chọn phiếu.'),
    ('Nút Chọn phiếu', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở popup Chọn phiếu yêu cầu xuất hàng mượn (FR-06).'),
    ('Ngày hẹn trả', 'Datepicker', 'Disable', 'dd/mm/yyyy', '–', 'Trống',
     'Lấy từ phiếu mượn đã chọn. Có biểu tượng ⓘ: “Lấy từ phiếu mượn đã chọn — đây là hạn trả '
     'đang có hiệu lực trước khi gia hạn.”'),
    ('Ngày hẹn trả mới', 'Datepicker', 'Enable',
     'Sau hôm nay và sau Ngày hẹn trả; không quá ngày trần', 'Có', 'Trống',
     'Các ngày ngoài khoảng bị mờ trên lịch. Biểu tượng ⓘ nêu ngày tối đa theo cấu hình số ngày '
     'mượn tối đa.'),
    ('Ngày tạo', 'Textbox', 'Disable', 'dd/mm/yyyy', '–', 'Ngày hôm nay',
     'Có biểu tượng ⓘ: ngày lập do hệ thống tự ghi nên không sửa được.'),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Gợi ý “Lý do cần gia hạn (không bắt buộc)”.'),
    ('Khối File đính kèm', 'Table/Grid', 'Enable', 'Chỉ PDF; tối đa 13 MB mỗi file', 'Không',
     'Chưa có file', 'Nút “Thêm tài liệu”; bảng STT, UPLOAD / FILE, DUNG LƯỢNG. File tải lên '
     'ngay khi chọn, có nút gỡ / thay.'),
    ('Khối Chi tiết', 'Table/Grid', 'Read-only', '–', '–',
     '“Chưa chọn phiếu mượn. Bấm Chọn phiếu ở trên để lấy danh sách hàng.”',
     'Sau khi chọn phiếu: STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, SL mượn, Đã trả, '
     'ĐVT và dòng Tổng cộng.'),
    ('Nút Gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Gửi phiếu cho Trưởng phòng; bị khóa trong lúc đang gửi.'),
    ('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Gửi phiếu như Gửi duyệt rồi ở lại màn với form trắng.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Về danh sách; hỏi xác nhận nếu có thay đổi chưa gửi.'),
    ('Thông báo lỗi tại ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô bị lỗi, tự tắt khi ô đã hợp lệ; kèm thông báo góc màn hình.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Ngày hẹn trả mới', 'Change',
     'During:\n– Lịch chỉ cho chọn ngày SAU cả hôm nay lẫn Ngày hẹn trả hiện tại và không quá '
     'ngày trần (hôm nay + số ngày mượn tối đa).\n'
     'After:\n– Xóa lỗi đỏ của ô nếu đang có.'),
    ('Thêm tài liệu', 'Click',
     'During:\n– File không phải PDF → hiển thị “Chỉ nhận file PDF”.\n'
     '– File quá 13 MB → hiển thị “File đính kèm không được quá 13 MB”.\n'
     'After:\n– Tải file lên ngay, hiện tên và dung lượng trong bảng.'),
    ('Bấm Gửi duyệt / Lưu và tiếp tục', 'Click',
     'Before:\n– Không yêu cầu quyền riêng; chỉ gia hạn được phiếu mượn của chính mình.\n'
     'During:\n– Chưa chọn phiếu mượn → hiển thị “Phiếu yêu cầu xuất hàng mượn – Bắt buộc phải '
     'chọn”.\n'
     '– Chưa chọn ngày → hiển thị “Ngày hẹn trả mới – Bắt buộc phải chọn”; kèm thông báo “Bạn '
     'chưa nhập đầy đủ thông tin.”.\n'
     '– Ngày không sau hôm nay → “Phải sau ngày hôm nay”.\n'
     '– Ngày vượt trần → “Không thể mượn quá dd/mm/yyyy”.\n'
     '– Ngày không sau hạn hiện tại → “Phải sau ngày hẹn trả hiện tại (dd/mm/yyyy)”.\n'
     '– Ghi chú quá 255 ký tự → “Không được vượt quá 255 ký tự”.\n'
     '– Phiếu mượn không còn đủ điều kiện → “Không thể gia hạn yêu cầu này: <lý do>” (BR-02).\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Khóa phiếu mượn trong lúc ghi để hai lần bấm liên tiếp chỉ sinh một phiếu.\n'
     '– Sinh mã PGHHM-NNNNN, ghi phiếu ở trạng thái Chờ TP duyệt, chụp Ngày hẹn trả hiện tại '
     'của phiếu mượn vào phiếu.\n'
     '– Ghi một dòng lịch sử “Tạo phiếu”.\n'
     '– Gửi thông báo “[PGHHM] Chờ duyệt: <mã phiếu>.” (kèm ghi chú) cho các Trưởng phòng duyệt '
     'được phiếu (BR-08).\n'
     '– Hiển thị “Yêu cầu của bạn đã được gửi”; Gửi duyệt thì về danh sách, Lưu và tiếp tục thì '
     'làm mới màn Tạo mới.'),
    ('Bấm Quay lại / rời màn', 'Click',
     'Before:\n– Có thay đổi chưa gửi → hỏi xác nhận rời trang.\n'
     'After:\n– Về màn danh sách.'),
])

# ------------------------------------------------------------ 2.6 Popup chon phieu muon
d.h3('2.6 Chọn phiếu mượn cần gia hạn')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Chọn phiếu mượn cần gia hạn', 'crud', (), actor=A_NV,
            caption='Biểu đồ Use Case — FR-06 Chọn phiếu mượn cần gia hạn')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Phân trang. Chỉ bổ sung điều kiện riêng của popup tại '
           'phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Chọn phiếu yêu cầu xuất hàng mượn để gia hạn',
    mota='Popup liệt kê đúng những phiếu mượn mà người đăng nhập gia hạn được, để chọn một phiếu '
         'đưa vào form lập phiếu.',
    tacnhan='Nhân viên mượn hàng',
    dieukien='Đang ở màn Tạo mới.',
    chinh='1. Người dùng bấm Chọn phiếu.\n'
          '2. Hệ thống mở popup “Chọn phiếu yêu cầu xuất hàng mượn”, nạp 10 phiếu mới nhất đủ '
          'điều kiện.\n'
          '3. Người dùng gõ mã để tìm, bấm tiêu đề cột để sắp xếp hoặc lật trang nếu cần.\n'
          '4. Người dùng bấm vào một dòng.\n'
          '5. Hệ thống đóng popup, điền mã phiếu mượn, Ngày hẹn trả và bảng Chi tiết vào form.',
    phu='• Không có phiếu đủ điều kiện → popup ghi “Bạn không có phiếu mượn nào gia hạn được. Chỉ '
        'phiếu do chính bạn lập, đã xuất kho, còn đang mượn và chưa có yêu cầu gia hạn chờ duyệt '
        'mới hiện ở đây.”.\n'
        '• Gõ mã không khớp → popup ghi “Không có phiếu mượn nào khớp mã đã nhập.”.\n'
        '• Chọn lại phiếu khác → form thay toàn bộ dữ liệu theo phiếu mới.',
    dacbiet='Popup và chốt chặn lúc gửi dùng CHUNG một điều kiện (BR-01): phiếu đã hiện trong '
            'popup thì gửi được, trừ khi có thay đổi xen giữa.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Chọn phiếu', modal='Chọn phiếu yêu cầu xuất hàng mượn',
         shot=shot('07-popup-chon-phieu-muon.png'),
         shot_caption='Popup Chọn phiếu yêu cầu xuất hàng mượn — trạng thái rỗng (tài khoản '
                      'chụp không có phiếu mượn nào)')
d.p('Popup được mở trên màn Tạo mới (không phải màn danh sách).')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm theo mã', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Gợi ý “Tìm theo mã phiếu mượn...”; tự lọc sau khi ngừng gõ, không cần Enter.'),
    ('Bảng phiếu mượn', 'Table/Grid', 'Read-only', '–', '–', '10 dòng / trang',
     'Cột STT, Mã phiếu, Ngày tạo, Ngày hẹn trả, Ghi chú. Mặc định phiếu tạo mới nhất ở đầu.'),
    ('Tiêu đề cột Mã phiếu / Ngày tạo / Ngày hẹn trả', 'Button', 'Enable', '–', '–', 'Chưa sắp',
     'Bấm để sắp tăng / giảm dần.'),
    ('Nút Trước / Sau', 'Pagination', 'Enable / Ẩn', '–', '–', 'Ẩn khi chỉ có 1 trang',
     'Kèm dòng “Trang x / y”.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Câu giải thích ở mục Dòng sự kiện phụ.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng popup, không chọn gì.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở popup / gõ tìm / sắp xếp / lật trang', 'System',
     'During:\n– Chỉ lấy phiếu yêu cầu xuất hàng loại mượn: do chính người đăng nhập lập, đã xuất '
     'kho, đang mượn (chưa trả hết), chưa có yêu cầu gia hạn nào đang chờ duyệt, và hạn trả '
     'hiện tại trước ngày trần.\n'
     'After:\n– Hiển thị kết quả, tổng số trang.'),
    ('Bấm vào một dòng', 'Click',
     'Before:\n– Kiểm tra lại phiếu còn đủ điều kiện.\n'
     '– Không còn → thông báo “Không thể gia hạn yêu cầu này: <lý do>”, form không đổi.\n'
     'After:\n– Đóng popup; điền mã phiếu, Ngày hẹn trả hiện tại, ngày trần và bảng Chi tiết.'),
])

# ------------------------------------------------------------ 2.7 Xem chi tiet
d.h3('2.7 Xem chi tiết phiếu')

d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung phần riêng của màn Phiếu yêu cầu gia '
           'hạn hàng mượn tại phần mô tả chi tiết.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu yêu cầu gia hạn hàng mượn',
    mota='Hiển thị toàn bộ thông tin phiếu ở chế độ chỉ đọc: thông tin chung, file đính kèm, bảng '
         'hàng của phiếu mượn, lịch sử duyệt và lịch sử thay đổi. Đây cũng là màn để duyệt.',
    tacnhan='Nhân viên mượn hàng; Trưởng phòng; Ban giám đốc; Kế toán kho',
    dieukien='Người dùng được xem phiếu (BR-09).',
    chinh='1. Người dùng bấm vào mã phiếu ở màn danh sách (hoặc bấm vào thông báo).\n'
          '2. Hệ thống kiểm tra quyền xem phiếu.\n'
          '3. Hệ thống hiển thị màn “Chi tiết yêu cầu gia hạn hàng mượn: <mã phiếu>”.\n'
          '4. Các nút ở cuối màn hiện theo đúng quyền và trạng thái của phiếu.',
    phu='• Không đủ quyền xem → báo “Bạn không có quyền xem phiếu này”, không hiện nội dung.\n'
        '• Phiếu chưa có cấp nào đóng dấu → không hiện khối Lịch sử duyệt.\n'
        '• Phiếu không có file → khối File đính kèm ghi “Không có file đính kèm.”.\n'
        '• Kế toán kho xem phiếu Chờ KT duyệt → ô Ngày hẹn trả mới được mở khóa để sửa trước khi '
        'duyệt; mọi người khác thấy ô này bị khóa.',
    dacbiet=None)

d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('08-chi-tiet.png'),
         shot_caption='Màn chi tiết phiếu Chờ TP duyệt, góc nhìn người duyệt')

d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–',
     'Chi tiết yêu cầu gia hạn hàng mượn: <mã phiếu>', '–'),
    ('Góc phải khối Thông tin chung', 'Label', 'Read-only', '–', '<Người tạo> — <ngày giờ tạo>',
     'Không hiển thị nhãn trạng thái tại đây.'),
    ('Mã phiếu', 'Textbox', 'Disable', 'PGHHM-NNNNN', 'Theo dữ liệu',
     'Biểu tượng ⓘ: mã do hệ thống tự sinh lúc gửi yêu cầu.'),
    ('Phiếu yêu cầu xuất hàng mượn', 'Label', 'Read-only', 'PYCXH-NNNNN', 'Theo dữ liệu',
     'Liên kết mở phiếu mượn ở tab mới. Biểu tượng ⓘ: không đổi được sau khi đã gửi.'),
    ('Người tạo / Phòng ban yêu cầu', 'Textbox', 'Disable', '–', 'Theo dữ liệu',
     'Phòng ban ghi trên phiếu lúc lập.'),
    ('Ngày hẹn trả', 'Textbox', 'Disable', 'dd/mm/yyyy', 'Theo dữ liệu',
     'Hạn trả của phiếu mượn tại thời điểm lập phiếu gia hạn.'),
    ('Ngày hẹn trả mới', 'Datepicker', 'Disable / Enable', 'dd/mm/yyyy', 'Theo dữ liệu',
     'Chỉ mở khóa với Kế toán kho khi phiếu Chờ KT duyệt. Khi khóa, ⓘ ghi “Chỉ Kế toán được sửa '
     'lại ngày này, và chỉ khi phiếu đang chờ Kế toán duyệt.”'),
    ('Ngày tạo / Ghi chú', 'Textbox', 'Disable', '–', 'Theo dữ liệu', 'Ngày tạo dạng dd/mm/yyyy hh:mm.'),
    ('Khối File đính kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'STT, UPLOAD / FILE (nút xem, nút tải về), DUNG LƯỢNG.'),
    ('Khối Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, SL mượn, Đã trả, ĐVT + dòng Tổng '
     'cộng. Số theo chuẩn 1,234.5.'),
    ('Khối Lịch sử duyệt', 'Table/Grid', 'Read-only', '–', 'Ẩn khi chưa ai đóng dấu',
     'STT, Cấp duyệt, Người duyệt, Thời gian, Ghi chú; cấp đã từ chối có nhãn đỏ “Từ chối”.'),
    ('Khối Lịch sử thay đổi', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Có số mốc cạnh tiêu đề và nút Xem lịch sử (FR-12).'),
    ('Nút cuối màn', 'Button', 'Enable / Ẩn', '–', 'Theo quyền và trạng thái',
     'TP duyệt / BGĐ duyệt / KT duyệt và Từ chối (chỉ khi đến lượt mình), In, Quay lại. Không '
     'có nút Sửa, Xóa.'),
], required=False)

d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Kiểm tra quyền xem theo BR-09.\n'
     '– Không đủ quyền → báo “Bạn không có quyền xem phiếu này”.\n'
     'During:\n– Trong lúc chờ hiện “Đang tải dữ liệu phiếu...”.\n'
     'After:\n– Hiển thị dữ liệu, các nút hợp lệ và số mốc lịch sử.'),
    ('Bấm liên kết phiếu mượn', 'Click',
     'After:\n– Mở chi tiết phiếu yêu cầu xuất hàng ở tab mới.'),
    ('Bấm xem / tải file đính kèm', 'Click',
     'After:\n– Mở xem hoặc tải file PDF về máy.'),
])

# ------------------------------------------------------------ 2.8 Duyet
d.h3('2.8 Duyệt phiếu')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Duyệt phiếu yêu cầu gia hạn hàng mượn', 'action', (), actor=A_DUYET,
            caption='Biểu đồ Use Case — FR-08 Duyệt phiếu')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc ghi lịch sử.', anchor='notice')
d.intro_table(
    ten='Duyệt phiếu yêu cầu gia hạn hàng mượn',
    mota='Ký duyệt phiếu ở một trong ba cấp Trưởng phòng, Ban giám đốc, Kế toán kho. Bước Kế toán '
         'kho duyệt là bước duy nhất đổi ngày hẹn trả của phiếu mượn.',
    tacnhan='Trưởng phòng; Ban giám đốc; Kế toán kho',
    dieukien='Phiếu đang ở đúng trạng thái chờ cấp đó duyệt; người duyệt có quyền tương ứng, cùng '
             'công ty với phiếu; Trưởng phòng còn phải quản lý phòng ban của phiếu.',
    chinh='1. Người duyệt mở màn chi tiết (bấm mã phiếu, biểu tượng Duyệt trên dòng, hoặc bấm '
          'thông báo).\n'
          '2. Kế toán kho có thể sửa lại Ngày hẹn trả mới.\n'
          '3. Người duyệt bấm nút duyệt của cấp mình (TP duyệt / BGĐ duyệt / KT duyệt).\n'
          '4. Hệ thống mở hộp “Xác nhận duyệt”; người duyệt bấm Duyệt.\n'
          '5. Hệ thống kiểm tra chặn quá hạn, quyền, trạng thái và ngày.\n'
          '6. Hệ thống chuyển phiếu sang bước tiếp theo, ghi lịch sử, gửi thông báo.\n'
          '7. Hệ thống hiển thị thông báo kết quả và quay về màn danh sách.',
    phu='• Trưởng phòng duyệt: giá trị hàng còn nợ của phiếu mượn LỚN HƠN hạn mức công ty → Chờ '
        'BGĐ duyệt (“Yêu cầu đã được chuyển đến Ban giám đốc.”); ngược lại → Chờ KT duyệt '
        '(“Yêu cầu đã được chuyển đến Kế toán.”).\n'
        '• Ban giám đốc duyệt → Chờ KT duyệt.\n'
        '• Kế toán kho duyệt → Đã duyệt, ngày hẹn trả của phiếu mượn đổi sang Ngày hẹn trả mới '
        '(“Duyệt phiếu thành công.”).\n'
        '• Phòng ban người duyệt quản lý có nhân viên quá hạn và cấu hình chặn đang bật → báo chặn '
        'và mở cửa sổ liệt kê nhân viên quá hạn (BR-07).\n'
        '• Bấm Hủy ở hộp xác nhận → không làm gì.\n'
        '• Phiếu đã được người khác xử lý → báo không có quyền duyệt bước này / phiếu không ở '
        'trạng thái chờ duyệt.',
    dacbiet='Hộp xác nhận của bước Kế toán ghi rõ hậu quả: “Duyệt bước Kế toán sẽ đổi ngày hẹn '
            'trả của phiếu mượn <mã> sang <ngày> ngay lập tức. Bạn có chắc chắn không?”')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => TP duyệt', shot=shot('10-xac-nhan-duyet.png'),
         shot_caption='Hộp Xác nhận duyệt ở cấp Trưởng phòng')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút duyệt của cấp hiện tại', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
     'Nhãn theo trạng thái: TP duyệt / BGĐ duyệt / KT duyệt. Chỉ hiện khi đến lượt người xem.'),
    ('Ngày hẹn trả mới (Kế toán kho)', 'Datepicker', 'Enable',
     'Sau hôm nay, sau hạn hiện tại của phiếu mượn, không quá ngày trần', 'Có', 'Theo dữ liệu',
     'Chỉ Kế toán kho ở bước Chờ KT duyệt; Trưởng phòng và Ban giám đốc thấy ô khóa.'),
    ('Hộp Xác nhận duyệt', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     'TP / BGĐ: “Bạn xác nhận <TP duyệt | BGĐ duyệt> phiếu <mã>?”. KT: câu nêu đổi ngày hẹn '
     'trả của phiếu mượn.'),
    ('Nút Duyệt / Hủy trong hộp', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Duyệt màu xanh; Hủy đóng hộp.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Câu theo cấp ở mục Dòng sự kiện phụ, hoặc câu lỗi.'),
])

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút duyệt của cấp hiện tại', 'Click',
     'Before:\n– Kế toán kho để trống ngày → “Ngày hẹn trả mới – Bắt buộc phải chọn”, không mở '
     'hộp xác nhận.\n'
     'After:\n– Mở hộp Xác nhận duyệt.'),
    ('Bấm Duyệt trong hộp xác nhận', 'Click',
     'Before:\n– Kiểm tra chặn quá hạn (BR-07): bị chặn → “Phòng ban bạn quản lý có nhân viên '
     '<loại hàng> quá hạn. Không thể thực hiện thao tác này.” và mở cửa sổ danh sách quá hạn.\n'
     '– Kiểm tra quyền đúng cấp và cùng công ty; sai → “Bạn không có quyền duyệt bước này.”.\n'
     'During:\n– Phiếu không còn ở trạng thái chờ → “Phiếu không ở trạng thái chờ duyệt.”.\n'
     '– Kế toán kho sửa ngày: không sau hôm nay → “Ngày hẹn trả mới – Phải sau ngày hôm nay.”; '
     'vượt trần → “Không thể mượn quá dd/mm/yyyy”.\n'
     '– Bước Kế toán: Ngày hẹn trả mới không sau hạn HIỆN TẠI của phiếu mượn (có thể đã được '
     'gia hạn xen giữa bởi phiếu khác) → “Phải sau ngày hẹn trả hiện tại (dd/mm/yyyy)”.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Ghi người duyệt và thời điểm vào bộ thông tin của cấp đó; chuyển trạng thái theo '
     'BR-05 / BR-06.\n'
     '– Kế toán kho: nếu đã sửa ngày thì ghi trước một dòng lịch sử “Thay đổi thông tin”; đổi '
     'ngày hẹn trả của phiếu mượn sang Ngày hẹn trả mới.\n'
     '– Ghi một dòng lịch sử “Trưởng phòng duyệt” / “Ban giám đốc duyệt” / “Kế toán duyệt”.\n'
     '– Gửi thông báo: sang cấp mới → “[PGHHM] Chờ duyệt: <mã>.” cho người có quyền của cấp đó '
     'cùng công ty; Đã duyệt → “[PGHHM] Đã duyệt: <mã>. Hạn trả mới: dd/mm/yyyy.” cho người lập.\n'
     '– Hiển thị thông báo kết quả và quay về màn danh sách.'),
])

# ------------------------------------------------------------ 2.9 Tu choi
d.h3('2.9 Từ chối phiếu')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Từ chối phiếu yêu cầu gia hạn hàng mượn', 'action', (), actor=A_DUYET,
            caption='Biểu đồ Use Case — FR-09 Từ chối phiếu')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc ghi lịch sử.', anchor='notice')
d.intro_table(
    ten='Từ chối phiếu yêu cầu gia hạn hàng mượn',
    mota='Không duyệt phiếu ở cấp đang chờ, bắt buộc nêu lý do. Phiếu sang trạng thái Không duyệt '
         'và dừng hẳn.',
    tacnhan='Trưởng phòng; Ban giám đốc; Kế toán kho',
    dieukien='Phiếu đang chờ chính người dùng duyệt ở đúng cấp (cùng điều kiện với FR-08).',
    chinh='1. Người duyệt bấm nút Từ chối ở màn chi tiết hoặc biểu tượng Từ chối trên dòng.\n'
          '2. Hệ thống mở cửa sổ “Từ chối yêu cầu gia hạn: <mã phiếu>”.\n'
          '3. Người duyệt nhập Lý do từ chối.\n'
          '4. Người duyệt bấm Xác nhận từ chối.\n'
          '5. Hệ thống chuyển phiếu sang Không duyệt, ghi lý do, ghi lịch sử, thông báo cho người '
          'lập và hiển thị “Đã từ chối yêu cầu gia hạn hàng mượn.”.',
    phu='• Bỏ trống lý do hoặc chỉ nhập khoảng trắng → “Lý do từ chối – Bắt buộc phải nhập”, cửa '
        'sổ không đóng.\n'
        '• Lý do quá 255 ký tự → ô không nhận thêm ký tự.\n'
        '• Từ màn chi tiết → về danh sách; từ danh sách → ở lại danh sách và nạp lại.\n'
        '• Phiếu đã được người khác xử lý → “Bạn không có quyền từ chối phiếu này.”.',
    dacbiet='Từ chối KHÔNG bị chặn bởi kiểm tra nhân viên quá hạn. Ngày hẹn trả của phiếu mượn '
            'không đổi. Người lập muốn gia hạn tiếp phải lập phiếu mới.')

d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Từ chối', shot=shot('11-popup-tu-choi.png'),
         shot_caption='Cửa sổ Từ chối yêu cầu gia hạn')
d.p('Cửa sổ Từ chối được mở ngay trên màn chi tiết hoặc màn danh sách theo đường dẫn ở trên.')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Từ chối yêu cầu gia hạn: <mã phiếu>', '–'),
    ('Lý do từ chối', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Gợi ý “Nhập lý do không duyệt để người lập biết...”.'),
    ('Dòng nhắc trạng thái', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '“Phiếu sẽ chuyển sang trạng thái Không duyệt và không duyệt tiếp được. Người lập muốn gia '
     'hạn lại phải tạo phiếu mới.”'),
    ('Nút Xác nhận từ chối', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Màu đỏ; bị khóa trong lúc đang xử lý.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, bỏ nội dung đã nhập.'),
])

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xác nhận từ chối', 'Click',
     'Before:\n– Kiểm tra người dùng đang ở đúng cấp duyệt của phiếu; sai → “Bạn không có quyền '
     'từ chối phiếu này.”.\n'
     'During:\n– Lý do trống → “Lý do từ chối – Bắt buộc phải nhập”.\n'
     '– Lý do quá 255 ký tự → “Không được vượt quá 255 ký tự”.\n'
     'After:\n– Ghi người từ chối, thời điểm và lý do vào bộ thông tin của cấp đang chờ; chuyển '
     'phiếu sang Không duyệt.\n'
     '– Ghi một dòng lịch sử “Không duyệt” kèm lý do.\n'
     '– Gửi thông báo “[PGHHM] Từ chối: <mã>. Lý do: <lý do>” cho người lập.\n'
     '– Hiển thị “Đã từ chối yêu cầu gia hạn hàng mượn.”.'),
])

# ------------------------------------------------------------ 2.10 In
d.h3('2.10 In phiếu và danh sách')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'In phiếu và danh sách', 'io', (), actor=A_ALL,
            caption='Biểu đồ Use Case — FR-10 In phiếu và danh sách')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc màn In và Xuất dữ liệu.', anchor='excel')
d.intro_table(
    ten='In phiếu yêu cầu gia hạn hàng mượn và in danh sách',
    mota='Mở popup xem trước để in một phiếu (khổ A4 dọc), hoặc in toàn bộ danh sách theo đúng '
         'bộ lọc đang áp (khổ A4 ngang).',
    tacnhan='Nhân viên mượn hàng; Trưởng phòng; Ban giám đốc; Kế toán kho',
    dieukien='In phiếu: người dùng xem được phiếu đó. In danh sách: đang ở màn danh sách.',
    chinh='1. Người dùng bấm In ở cột Hành động, ở màn chi tiết, hoặc nút In trên thanh công cụ.\n'
          '2. Hệ thống mở popup xem trước ngay trên màn hiện tại.\n'
          '3. Người dùng bấm nút In trong popup để gửi lệnh in.',
    phu='• In danh sách lấy TOÀN BỘ phiếu khớp bộ lọc và chế độ, không chỉ trang đang xem.\n'
        '• Danh sách rỗng → bản in ghi “Không có dữ liệu”, Tổng số phiếu: 0.\n'
        '• Có lọc Ngày tạo → bản in danh sách có dòng “Khoảng thời gian: Từ ngày … đến ngày …”.',
    dacbiet='Phần đầu bản in phiếu lấy theo công ty GHI TRÊN PHIẾU, không theo người đang in.')

d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => In', shot=shot('12-in-phieu.png'),
         shot_caption='Popup xem trước bản in phiếu')
d.layout(menu=MENU + ' => In', shot=shot('13-in-danh-sach.png'),
         shot_caption='Popup xem trước bản in danh sách')

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–',
     'Xem trước yêu cầu gia hạn hàng mượn <mã> / Xem trước danh sách yêu cầu gia hạn hàng mượn',
     'Kèm nút In.'),
    ('Phần đầu chứng từ', 'Label', 'Read-only', '–', 'Theo công ty của phiếu',
     'Logo và thông tin liên hệ của công ty.'),
    ('Bản in phiếu — khối thông tin', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tiêu đề “PHIẾU YÊU CẦU GIA HẠN HÀNG MƯỢN”, Số phiếu, Ngày tạo; Người yêu cầu, Phòng ban, '
     'Phiếu mượn, Ngày hẹn trả cũ, Ngày hẹn trả mới, Trạng thái, Ghi chú.'),
    ('Bản in phiếu — bảng hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Như bảng Chi tiết của màn chi tiết + dòng Tổng cộng.'),
    ('Bản in phiếu — bảng cấp duyệt', 'Table/Grid', 'Read-only', '–', 'Ẩn khi chưa ai đóng dấu',
     'Cấp duyệt, Người duyệt, Thời gian, Ghi chú; cấp đã từ chối ghi thêm “(không duyệt)”.'),
    ('Bản in phiếu — khối ký', 'Label', 'Read-only', '–', 'Hiển thị',
     'Bốn ô: Người lập, Trưởng phòng, Ban giám đốc, Kế toán.'),
    ('Bản in danh sách', 'Table/Grid', 'Read-only', '–', 'Theo bộ lọc',
     'Tiêu đề “DANH SÁCH PHIẾU YÊU CẦU GIA HẠN HÀNG MƯỢN”, “Tổng số phiếu: N”; cột STT, Mã phiếu, '
     'Phiếu mượn, Người tạo, Ngày tạo, Ngày hẹn trả cũ, Ngày hẹn trả mới, Trạng thái, Người '
     'duyệt, Ngày duyệt.'),
], required=False)

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In ở dòng hoặc ở màn chi tiết', 'Click',
     'Before:\n– Kiểm tra quyền xem phiếu; không đủ → “Bạn không có quyền xem phiếu này”.\n'
     'After:\n– Mở popup xem trước bản in của phiếu, khổ dọc.'),
    ('Bấm In trên thanh công cụ', 'Click',
     'After:\n– Mở popup xem trước bản in danh sách theo bộ lọc và chế độ đang áp, khổ ngang.'),
    ('Bấm In trong popup', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt.'),
])

# ------------------------------------------------------------ 2.11 Xuat Excel
d.h3('2.11 Xuất danh sách ra Excel')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Xuất danh sách phiếu ra Excel', 'io', (), actor=A_ALL,
            caption='Biểu đồ Use Case — FR-11 Xuất danh sách ra Excel')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Xuất danh sách phiếu ra Excel',
    mota='Xuất danh sách phiếu ra file Excel; người dùng tự chọn trường và thứ tự cột.',
    tacnhan='Nhân viên mượn hàng; Trưởng phòng; Ban giám đốc; Kế toán kho',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” với 12 trường, tích sẵn các trường '
          'đang hiện trên bảng (mặc định “Đang chọn 9/12 trường”).\n'
          '3. Người dùng tích / bỏ tích, kéo đổi thứ tự.\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống lấy toàn bộ phiếu khớp bộ lọc, dựng file và tải về máy.',
    phu='• Trong lúc đang xuất, nút bị khóa để tránh bấm nhiều lần.\n'
        '• Xuất thất bại → “Lỗi khi xuất Excel”, không tải file.',
    dacbiet='File chứa toàn bộ dòng khớp bộ lọc và chế độ trong phạm vi quyền, không giới hạn '
            'ở trang đang xem.')

d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('05-chon-truong-xuat-excel.png'),
         shot_caption='Cửa sổ Chọn trường xuất Excel')

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất Excel',
     'Kèm dòng hướng dẫn tích chọn và kéo đổi thứ tự cột.'),
    ('Danh sách trường', 'Table/Grid', 'Enable', '12 trường', 'Có (≥ 1)', '9 trường đang hiện',
     'Mã phiếu, Phiếu mượn, Người tạo, Ngày tạo, Ngày hẹn trả cũ, Ngày hẹn trả mới, Trạng thái, '
     'Người duyệt, Ngày duyệt, Phòng ban, Ghi chú, Lý do từ chối.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Dòng “Đang chọn x/12 trường”', 'Label', 'Read-only', '–', '–', 'Đang chọn 9/12 trường', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Bị khóa trong lúc đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
])

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xuất Excel', 'Click', 'After:\n– Mở cửa sổ chọn trường xuất.'),
    ('Bấm Xuất file', 'Click',
     'During:\n– Lấy dữ liệu theo đúng bộ lọc, chế độ và phạm vi quyền hiện tại.\n'
     'After:\n– Dựng file danh_sach_yeu_cau_gia_han_hang_muon.xlsx: dòng tiêu đề “DANH SÁCH PHIẾU '
     'YÊU CẦU GIA HẠN HÀNG MƯỢN”, dòng khoảng ngày nếu có lọc Ngày tạo, cột STT luôn đứng đầu rồi '
     'các trường theo thứ tự đã chọn, cuối file có khối ký Người lập.\n'
     '– Hiển thị “Xuất Excel thành công” và đóng cửa sổ.'),
])

# ------------------------------------------------------------ 2.12 Lich su
d.h3('2.12 Xem lịch sử thay đổi')

d.p('2.12.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu',
    mota='Hiển thị các mốc thao tác trên phiếu: Tạo phiếu, Thay đổi thông tin, Trưởng phòng '
         'duyệt, Ban giám đốc duyệt, Kế toán duyệt, Không duyệt — kèm người thực hiện, thời điểm '
         'và giá trị thay đổi.',
    tacnhan='Nhân viên mượn hàng; Trưởng phòng; Ban giám đốc; Kế toán kho',
    dieukien='Người dùng xem được phiếu.',
    chinh='1. Người dùng bấm biểu tượng Lịch sử ở cột Hành động, hoặc bấm Xem lịch sử ở khối Lịch '
          'sử thay đổi trong màn chi tiết.\n'
          '2. Hệ thống hiển thị danh sách mốc, mới nhất ở trên.\n'
          '3. Người dùng có thể bấm Bộ lọc để lọc theo Loại hành động, Người thực hiện, Từ ngày, '
          'Đến ngày.',
    phu='• Phiếu chưa có mốc nào (lập và xử lý bên hệ thống ERP cũ) → “Chưa có lịch sử thao tác '
        'nào.”, không có nút Bộ lọc.\n'
        '• Bộ lọc không khớp → “Không có lịch sử phù hợp bộ lọc.”.\n'
        '• Bấm Làm mới → nạp lại; bấm Thu gọn → đóng khối.',
    dacbiet=None)

d.p('2.12.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Lịch sử thay đổi', shot=shot('09-lich-su-thay-doi.png'),
         shot_caption='Khối Lịch sử thay đổi đang mở ở màn chi tiết')

d.p('2.12.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề khối', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi',
     'Kèm số mốc thay đổi cạnh tiêu đề.'),
    ('Nút Xem lịch sử / Thu gọn', 'Button', 'Enable', '–', 'Thu gọn', 'Đóng / mở khối.'),
    ('Nút Làm mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Chỉ hiện khi khối đang mở.'),
    ('Nút Bộ lọc', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không có mốc',
     'Mở các ô Loại hành động (chỉ liệt kê loại đã có trên phiếu), Người thực hiện, Từ ngày, Đến '
     'ngày.'),
    ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, tên hành động (màu theo loại), “Người thực hiện: <tên> '
     '- <phòng ban>”, giá trị thay đổi của Trạng thái, Ngày hẹn trả mới, Ghi chú, File đính kèm; '
     'mốc Không duyệt kèm lý do.'),
    ('Popup Lịch sử ở danh sách', 'Modal', 'Hiển thị', '–', 'Ẩn',
     'Tiêu đề “Lịch sử yêu cầu gia hạn hàng mượn” kèm mã phiếu; nội dung giống khối ở màn chi '
     'tiết.'),
], required=False)

d.p('2.12.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết / bấm Lịch sử trên dòng', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu; không đủ → “Bạn không có quyền xem phiếu này”.\n'
     'After:\n– Nạp danh sách mốc, mới nhất trước; cập nhật số mốc cạnh tiêu đề.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Nạp lại danh sách mốc.'),
    ('Đổi điều kiện Bộ lọc', 'Change', 'After:\n– Lọc các mốc đang có theo điều kiện đã chọn.'),
])

# ==================================================== PHAN 4. QUY TAC NGHIEP VU
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu yêu cầu gia hạn hàng mượn; '
           'không lặp lại các quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')

d.rule_table([
    ('BR-01', 'Phiếu mượn được phép gia hạn', [
        '– Là phiếu yêu cầu xuất hàng loại mượn, do CHÍNH người lập phiếu gia hạn lập.',
        '– Đã xuất kho và còn đang mượn (chưa trả hết hàng).',
        '– Chưa có phiếu gia hạn nào ở trạng thái chờ duyệt (Chờ TP / Chờ BGĐ / Chờ KT). Phiếu '
        'gia hạn cũ đã Đã duyệt hoặc Không duyệt thì không cản.',
        '– Hạn trả hiện tại còn trước ngày trần; đã chạm ngày trần thì không còn ngày nào để gia '
        'hạn nên phiếu không hiện.',
        '– Cùng một điều kiện cho popup chọn phiếu và chốt chặn lúc gửi.',
    ], ['Lập phiếu', 'Chọn phiếu mượn']),
    ('BR-02', 'Câu báo phiếu mượn không gia hạn được', [
        '– Hệ thống nêu LÝ DO ĐẦU TIÊN gặp phải theo thứ tự: không tồn tại → không phải phiếu '
        'xuất hàng mượn → không phải người lập → đang có yêu cầu gia hạn <mã> (<trạng thái>) chưa '
        'duyệt xong → chưa xuất kho → không còn đang mượn → ngày hẹn trả hiện tại đã chạm mức tối '
        'đa.',
        '– Mọi câu đều mở đầu “Không thể gia hạn yêu cầu này: …”.',
    ], ['Lập phiếu', 'Chọn phiếu mượn']),
    ('BR-03', 'Ngày hẹn trả mới', [
        '– Bắt buộc; phải SAU ngày hôm nay và SAU ngày hẹn trả hiện tại của phiếu mượn.',
        '– Không vượt ngày trần = hôm nay + số ngày mượn tối đa (tính từ hôm nay, không tính từ '
        'ngày hẹn trả cũ).',
        '– Bước Kế toán duyệt đối chiếu với hạn HIỆN TẠI của phiếu mượn tại lúc duyệt, không phải '
        'hạn đã chụp lúc lập.',
    ], ['Lập phiếu', 'Duyệt']),
    ('BR-04', 'Không có nháp, không sửa, không xóa', [
        '– Gửi là phiếu vào thẳng Chờ TP duyệt; nút Lưu và tiếp tục cũng gửi phiếu đi.',
        '– Không có chức năng Sửa / Xóa ở bất kỳ trạng thái nào.',
        '– Người duyệt duy nhất sửa được dữ liệu là Kế toán kho, và chỉ ô Ngày hẹn trả mới khi '
        'phiếu Chờ KT duyệt.',
    ], 'Toàn màn hình'),
    ('BR-05', 'Luồng duyệt', [
        '– Chờ TP duyệt → (Trưởng phòng duyệt) → Chờ BGĐ duyệt hoặc Chờ KT duyệt theo BR-06.',
        '– Chờ BGĐ duyệt → (Ban giám đốc duyệt) → Chờ KT duyệt.',
        '– Chờ KT duyệt → (Kế toán kho duyệt) → Đã duyệt; CHÍNH LÚC NÀY ngày hẹn trả của phiếu '
        'mượn đổi sang Ngày hẹn trả mới. Các bước trước không đụng phiếu mượn.',
        '– Từ chối ở bất kỳ cấp nào → Không duyệt (trạng thái cuối).',
        '– Màn không đụng tới tồn kho và không hạch toán.',
    ], ['Duyệt', 'Từ chối']),
    ('BR-06', 'Điều kiện phải qua Ban giám đốc', [
        '– Giá trị hàng còn nợ = tổng trên MỌI dòng hàng của phiếu mượn (số lượng đã xuất − số '
        'lượng đã trả) × đơn giá, kể cả dòng không hiển thị ở bảng Chi tiết.',
        '– LỚN HƠN hạn mức giá trị hàng mượn của công ty ghi trên phiếu → qua Ban giám đốc; bằng '
        'hoặc nhỏ hơn → sang thẳng Kế toán.',
        '– Công ty để trống hạn mức được coi là 0: mọi phiếu mượn còn nợ đều phải qua Ban giám đốc.',
        '– Xét tại thời điểm Trưởng phòng bấm duyệt.',
    ], 'Duyệt'),
    ('BR-07', 'Chặn duyệt khi còn nhân viên quá hạn', [
        '– Áp cho thao tác duyệt ở cả ba cấp, khi cấu hình chặn “Duyệt gia hạn hàng mượn” đang bật '
        'cho công ty.',
        '– Xét các phòng ban người duyệt được phân công quản lý: có nhân viên đang quá hạn (hàng '
        'giữ, hàng mượn hoặc hàng nhập thẳng) → chặn, báo “Phòng ban bạn quản lý có nhân viên '
        '<loại> quá hạn. Không thể thực hiện thao tác này.” và mở cửa sổ liệt kê nhân viên quá hạn.',
        '– Super Admin không bị chặn. Từ chối không bị chặn.',
    ], 'Duyệt'),
    ('BR-08', 'Điều kiện duyệt và người nhận thông báo', [
        '– Mọi cấp: người duyệt phải cùng công ty với phiếu và có đúng quyền của cấp đó.',
        '– Trưởng phòng còn phải quản lý phòng ban của phiếu: được phân công quản lý, tích “Quản lý '
        'tất cả phòng ban”, hoặc thuộc chính phòng ban đó. Super Admin bỏ qua ràng buộc phòng ban.',
        '– Người nhận thông báo phiếu mới = đúng tập Trưởng phòng duyệt được phiếu (Redmine #11550).',
        '– Sang cấp BGĐ / KT: báo mọi người có quyền của cấp đó cùng công ty. Đã duyệt / Không '
        'duyệt: báo người lập.',
        '– Hai người cùng duyệt một phiếu: chỉ người bấm trước thành công, người sau bị từ chối.',
    ], ['Duyệt', 'Từ chối']),
    ('BR-09', 'Phạm vi dữ liệu và quyền xem', [
        '– Danh sách thường: V1 / Super Admin thấy mọi công ty; V2 thấy công ty mình; V3 thấy '
        'phòng ban mình quản lý và phòng ban mình; không có cấp nào chỉ thấy phiếu mình lập. Mọi cấp '
        'cộng thêm phiếu mình lập và phiếu mình đã duyệt / từ chối.',
        '– Danh sách chờ duyệt: chỉ phiếu đang chờ chính mình duyệt, cùng công ty.',
        '– Màn chi tiết, bản in, lịch sử: người lập, người đã đóng dấu, Super Admin, người có quyền '
        'duyệt cùng công ty, hoặc người có quyền xem theo cấp tương ứng.',
        '– Phiếu Không duyệt xem theo đúng phạm vi như các trạng thái khác.',
        '– Xuất Excel và in danh sách dùng cùng phạm vi với danh sách.',
    ], 'Toàn màn hình'),
    ('BR-10', 'Công ty và phòng ban của phiếu', [
        '– Chốt theo người lập TẠI THỜI ĐIỂM LẬP; người lập đổi phòng ban sau đó không làm đổi '
        'phiếu cũ, Trưởng phòng duyệt vẫn là Trưởng phòng của phòng ban ghi trên phiếu.',
        '– Ô lọc Phòng ban lọc theo phòng ban ghi trên phiếu.',
    ], ['Lập phiếu', 'Duyệt', 'Tìm kiếm và lọc']),
    ('BR-11', 'Từ chối', [
        '– Lý do bắt buộc, tối đa 255 ký tự; ghi vào bộ thông tin của đúng cấp đang chờ.',
        '– Phiếu sang Không duyệt và dừng hẳn; muốn gia hạn tiếp phải lập phiếu mới (phiếu mượn '
        'hiện lại ngay trong popup chọn phiếu).',
    ], 'Từ chối'),
    ('BR-12', 'File đính kèm', [
        '– Không bắt buộc; chỉ nhận file PDF, mỗi file tối đa 13 MB, đính kèm được nhiều file.',
    ], 'Lập phiếu'),
])

d.save()

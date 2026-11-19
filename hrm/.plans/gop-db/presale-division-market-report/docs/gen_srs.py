# -*- coding: utf-8 -*-
"""SRS - Báo cáo phân chia thị trường (form Danh mục quốc gia + quy tắc màn báo cáo của skill srs-documenter).

Khuôn: lookup-stock-companies/docs/gen_srs.py (đã duyệt) + _lib_report.py của màn đó (import, KHÔNG sửa).
Nguồn (code HRM nhánh develop, 18/11/2026):
  FE hrm-client/pages/assign/report/division-market/{index.vue, components/export-excel.js},
     components/subsystem-menu/presale.js, middleware/checkPermission.js, utils/mixins/{filterStateMixin,
     reportPrintPreviewMixin, columnCustomizationMixin}.js, utils/pageReload.js
  BE Modules/Assign/Http/Controllers/Api/V1/DivisionMarketReportController.php,
     Modules/Assign/Services/Report/DivisionMarketReportService.php, app/Support/Permissions/Catalog/presale.php
  Ảnh: capture.js (dev-hrm, 18/11/2026). Phần 5: dò code FE/BE + menu.
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(GOPDB, 'lookup-stock-companies', 'docs'))
import _lib_report as R  # noqa: E402
L = R.L

TEN = 'Báo cáo phân chia thị trường'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
QUYEN = 'Xem báo cáo phân chia thị trường'
Q = 'Người dùng có quyền “%s”' % QUYEN
DK = '1. Người dùng đăng nhập thành công.\n2. Vai trò của người dùng được cấp quyền “%s”.' % QUYEN
POPUP = 'Cửa sổ %s được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'
BANNED = ('Danh mục quốc gia', 'danh mục quốc gia', 'Danh mục khu vực', 'http://', 'https://')

UI7 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả']
UI7W = [0.55, 1.25, 0.85, 0.8, 0.95, 0.85, 2.6]
UI8 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả']
UI8W = [0.55, 1.15, 0.85, 0.75, 0.95, 0.65, 0.85, 2.3]


def ui(header, rows):
    return [header] + [[str(i + 1)] + r for i, r in enumerate(rows)]


TIP = {  # nguyên văn COLUMN_TIPS + pageTitleInfo trong index.vue
    'stt': 'Số thứ tự Tỉnh/TP • Đánh theo Tỉnh/TP, chạy liên tục qua các trang (tỉnh nằm vắt 2 trang giữ nguyên số).',
    'tinh': 'Tỉnh/TP được phân chia cho phòng ban • Lấy từ phiếu phân chia thị trường theo phòng ban đã duyệt.',
    'xa': 'Phường/Xã thuộc Tỉnh/TP được phân chia cho phòng ban • Lấy từ phiếu phân chia thị trường theo phòng ban đã duyệt. • Chỉ hiện phường/xã đã có nhân viên của phòng được phân chia phụ trách.',
    'phong': 'Phòng ban được giao phụ trách phường/xã • Theo phiếu phân chia thị trường theo phòng ban đã duyệt.',
    'nv': 'Nhân viên của phòng được giao phụ trách phường/xã • Theo phiếu phân chia thị trường theo nhân viên đã duyệt, đúng Tỉnh/TP và phường/xã của phòng.',
    'sdt': 'Số điện thoại của nhân viên phụ trách • Lấy theo hồ sơ nhân viên hiện tại.',
    'pt': 'X = nhân viên phụ trách tất cả các hãng xe tại phường/xã này • Theo phiếu phân chia thị trường theo nhân viên; có nhiều phiếu trùng thì chỉ cần 1 phiếu đánh dấu là hiện X.',
    'hx': 'Các hãng xe nhân viên được giao phụ trách tại phường/xã • Theo phiếu phân chia thị trường theo nhân viên; nhiều hãng cách nhau bằng dấu phẩy.',
    'title': 'Tra cứu Tỉnh/TP, phường/xã đang do phòng ban và nhân viên nào phụ trách, theo các phiếu phân chia thị trường (theo phòng ban và theo nhân viên) đã được duyệt.',
}


def ic(key):
    return '- Icon ⓘ: “%s”' % TIP[key]


MENU_PB = 'Bán hàng => Kế hoạch => Phiếu phân chia thị trường => Theo phòng ban'
MENU_NV = 'Bán hàng => Kế hoạch => Phiếu phân chia thị trường => Theo nhân viên'

# ------------------------------------------------------------------ Phần 5 (dò code 18/11/2026)
P5 = [
    ('Nguồn số liệu', 'Phiếu phân chia thị trường theo phòng ban (Tỉnh/TP, phường/xã giao cho phòng; chỉ phiếu Đã duyệt)', MENU_PB),
    ('Nguồn số liệu', 'Phiếu phân chia thị trường theo nhân viên (phường/xã, cờ phụ trách tất cả các hãng, hãng xe giao cho nhân viên; chỉ phiếu Đã duyệt)', MENU_NV),
    ('Danh mục tham chiếu', 'Quốc gia, Vùng, Tỉnh/TP, Phường/xã (nguồn các ô lọc; Tỉnh/TP gắn Vùng và Quốc gia)', 'Danh mục dùng chung => Địa lý'),
    ('Danh mục tham chiếu', 'Khu vực kinh doanh (phiếu phân chia chọn theo khu vực, hệ thống bung ra từng phường/xã)', 'Danh mục dùng chung => Địa lý => Khu vực kinh doanh'),
    ('Danh mục tham chiếu', 'Hãng xe (nguồn ô lọc Hãng xe, cột Hãng xe phụ trách)', 'Danh mục dùng chung => Danh mục xe => Hãng xe'),
    ('Danh mục tham chiếu', 'Danh mục phòng ban (tên phòng ở cột Phòng phụ trách, nguồn ô lọc Phòng phụ trách)', 'Thông tin nhân sự => Danh mục => Danh mục phòng ban'),
    ('Danh mục tham chiếu', 'Hồ sơ nhân sự (số điện thoại, phòng hiện tại dùng để thu hẹp ô Nhân viên phụ trách)', 'Thông tin nhân sự => Hồ sơ nhân sự => Quản lý hồ sơ nhân sự'),
    ('Màn cùng nguồn số liệu', 'Hợp đồng (dự án TKT) — tab hỗ trợ hạch toán đọc địa bàn của phòng từ phiếu phân chia theo phòng ban Đã duyệt', 'Bán hàng => Bán hàng => Hợp đồng bán hàng => Hợp đồng (dự án TKT)'),
]

FR = []

# 2.1 Xem báo cáo ----------------------------------------------------------------
UI_XEM = [
    ['Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Báo cáo phân chia thị trường', ['- Trên thanh đầu trang', ic('title')]],
    ['Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Báo cáo phân chia thị trường', ['- Biểu tượng ghim bản đồ đứng trước']],
    ['Dòng tóm tắt', 'Label', 'Hiển thị / Ẩn', 'Số', 'Theo dữ liệu', [
        '- “— N tỉnh/TP · M phường/xã · K dòng phụ trách”, ngay sau tiêu đề bảng',
        '- N = số Tỉnh/TP, M = số phường/xã, K = số dòng (mỗi dòng 1 nhân viên) trên TOÀN BỘ kết quả lọc, không chỉ trang đang xem',
        '- Số có dấu phẩy ngăn hàng nghìn (vd 59,225)', '- Ẩn khi không có dòng nào']],
    ['Nút In', 'Button', 'Enable', '–', 'Hiển thị', ['- Mở cửa sổ xem trước bản in theo bộ lọc đang áp (mục 2.5)']],
    ['Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', ['- Mở cửa sổ “Chọn trường xuất Excel” (mục 2.4)', '- Không bấm được khi đang xuất file']],
    ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', '–', 'Hiển thị', ['- Biểu tượng cột, đứng cuối nhóm nút', '- Mở cửa sổ “Tuỳ chỉnh cột” (mục 2.3)']],
    ['Bảng chi tiết báo cáo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
        '- Mỗi dòng là 1 nhân viên phụ trách 1 phường/xã cho 1 phòng',
        '- Cột: STT, Tỉnh/TP, Phường/Xã, Phòng phụ trách, Nhân viên phụ trách, Số điện thoại, Phụ trách tất cả các hãng, Hãng xe phụ trách — mỗi cột mô tả ở 1 dòng bên dưới',
        '- Gộp ô 4 cấp: STT + Tỉnh/TP gộp theo tỉnh, Phường/Xã gộp theo xã, Phòng phụ trách gộp theo phòng; chữ trong ô gộp nằm ở đầu ô',
        '- Tiêu đề bảng dính trên cùng khi cuộn', '- Không có dòng tổng, không sắp xếp theo cột']],
    ['Cột STT', 'Table/Grid', 'Read-only', 'Số', 'Theo dữ liệu', ['- Đánh theo Tỉnh/TP (không theo dòng), chạy liên tục qua các trang', '- Tỉnh vắt 2 trang giữ nguyên số ở trang sau', '- Cột khóa, không ẩn được', ic('stt')]],
    ['Cột Tỉnh/TP', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Tên Tỉnh/TP ghi trên phiếu phân chia theo phòng ban', '- Ô gộp theo tỉnh', '- Cột khóa, không ẩn được', ic('tinh')]],
    ['Cột Phường/Xã', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Tên phường/xã ghi trên phiếu phân chia theo phòng ban', '- Ô gộp theo phường/xã', ic('xa')]],
    ['Cột Phòng phụ trách', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Tên phòng ban hiện tại trong danh mục phòng ban', '- Ô gộp theo phòng trong phường/xã', ic('phong')]],
    ['Cột Nhân viên phụ trách', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Dạng “Mã phòng - Họ tên” như ghi trên phiếu phân chia theo nhân viên (vd “HN_KD1 - Bùi Hữu Hanh”)', ic('nv')]],
    ['Cột Số điện thoại', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Số điện thoại trong hồ sơ nhân viên hiện tại', '- Hồ sơ không có số: để trống', ic('sdt')]],
    ['Cột Phụ trách tất cả các hãng', 'Table/Grid', 'Read-only', 'X / trống', 'Theo dữ liệu', ['- “X” canh giữa khi nhân viên phụ trách tất cả các hãng xe tại phường/xã đó', '- Không phụ trách tất cả: để trống', ic('pt')]],
    ['Cột Hãng xe phụ trách', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Tên các hãng xe nhân viên được giao tại phường/xã, xếp theo bảng chữ cái, cách nhau dấu phẩy (vd “Acura, BMW, BYD”)', '- Không giao hãng nào: để trống', ic('hx')]],
    ['Thông báo bảng trống', 'Label', 'Ẩn', '–', 'Ẩn', ['- Đang tải: “Đang tải dữ liệu...”', '- Không có dòng khớp: “Không có dữ liệu phù hợp bộ lọc.”']],
    ['Phân trang', 'Pagination', 'Enable', '10 / 20 / 50 / 100', '10 phường/xã mỗi trang', [
        '- Phân trang theo PHƯỜNG/XÃ (không theo dòng): 1 trang 10 phường/xã kèm toàn bộ dòng nhân viên của các phường/xã đó',
        '- Chân bảng “Hiển thị a–b / N”: a–b là thứ tự phường/xã trên trang, N = tổng số phường/xã khớp bộ lọc (= M ở dòng tóm tắt)',
        '- Ô “Số dòng/trang:” chọn 10 / 20 / 50 / 100; nút « ‹ số trang › »', '- Ẩn khi không có dòng nào']],
    ['Thông báo lỗi', 'Toast', 'Ẩn', '–', 'Ẩn', ['- Lỗi tải dữ liệu: “Lỗi khi tải dữ liệu”']],
]

DATA_XEM = R.numbered(R.DATA_HEAD, [
    ('Tập dữ liệu (dòng nhân viên)', [
        'Mỗi dòng = 1 cặp (Tỉnh/TP, phường/xã, phòng, nhân viên) thỏa đồng thời: (1) phường/xã thuộc phiếu phân chia thị trường theo phòng ban ở trạng thái Đã duyệt; (2) nhân viên thuộc phiếu phân chia thị trường theo nhân viên ở trạng thái Đã duyệt của CÙNG phòng; (3) trên phiếu nhân viên, nhân viên được giao đúng Tỉnh/TP và đúng phường/xã đó (BR-02).',
        'Phiếu Đang tạo, Chờ duyệt, phiếu đã Hủy duyệt về Đang tạo hoặc đã xóa: không tính.',
        'Thời điểm số liệu: tức thời, lúc mở màn / bấm Tìm kiếm — báo cáo không có kỳ, không có ô thời gian.'], '—'),
    ('Dòng tóm tắt N tỉnh/TP · M phường/xã · K dòng phụ trách', ['Đếm trên toàn bộ kết quả lọc (mọi trang): N = số Tỉnh/TP khác nhau, M = số phường/xã khác nhau, K = số dòng nhân viên.'], '—'),
    ('STT', ['Số thứ tự Tỉnh/TP theo thứ tự tỉnh xuất hiện trong kết quả lọc, liên tục qua các trang.'], TIP['stt']),
    ('Tỉnh/TP', ['Tên Tỉnh/TP lưu trên phiếu phân chia theo phòng ban. Thứ tự tỉnh theo thứ tự khai báo trong danh mục Tỉnh/TP.'], TIP['tinh']),
    ('Phường/Xã', ['Tên phường/xã lưu trên phiếu phân chia theo phòng ban. Trong 1 tỉnh xếp theo tên A–Z. Phường/xã của phòng nhưng chưa có nhân viên nào của phòng được giao: không hiện.'], TIP['xa']),
    ('Phòng phụ trách', ['Phòng được phân chia trên phiếu theo phòng ban (phiếu chia cho cả phòng hoặc cho 1 bộ phận đều hiện tên phòng). Tên lấy theo danh mục phòng ban hiện tại. Trong 1 phường/xã xếp theo tên phòng A–Z.'], TIP['phong']),
    ('Nhân viên phụ trách', ['Nhân viên trên phiếu phân chia theo nhân viên, ghi dạng “Mã phòng - Họ tên” tại thời điểm lưu phiếu. Trong 1 phòng xếp theo tên hiển thị A–Z.', 'Nhiều phiếu nhân viên trùng cùng (tỉnh, phường/xã, phòng, nhân viên) chỉ ra 1 dòng (BR-03).'], TIP['nv']),
    ('Số điện thoại', ['Số điện thoại trong hồ sơ nhân viên hiện tại (đổi hồ sơ thì báo cáo đổi theo).'], TIP['sdt']),
    ('Phụ trách tất cả các hãng', ['“X” khi ít nhất 1 phiếu nhân viên đã duyệt đánh dấu nhân viên phụ trách tất cả các hãng xe tại phường/xã đó; còn lại để trống.'], TIP['pt']),
    ('Hãng xe phụ trách', ['Gộp tên các hãng xe được giao cho nhân viên tại phường/xã trên các phiếu nhân viên đã duyệt, bỏ trùng, xếp A–Z, cách nhau dấu phẩy.', 'Khi đang lọc ô Hãng xe: chỉ còn các hãng khớp ô lọc, cột Phụ trách tất cả các hãng cũng chỉ xét phần khớp (xem BR-07).'], TIP['hx']),
])
POPUP_XEM = R.numbered(R.POPUP_HEAD, [
    ('Mọi ô trên bảng chi tiết báo cáo', 'Không có popup', 'Báo cáo chỉ tra cứu danh sách phân công, không có con số cần xem chi tiết', '–'),
])

FR.append({
    'ten': 'Xem báo cáo phân chia thị trường',
    'qtc': 'Màn Báo cáo, Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem báo cáo phân chia thị trường'],
        ['Mô tả', 'Hiển thị Tỉnh/TP, phường/xã đang do phòng ban nào, nhân viên nào phụ trách theo các phiếu phân chia thị trường (theo phòng ban và theo nhân viên) đã duyệt, kèm số điện thoại nhân viên, cờ phụ trách tất cả các hãng và các hãng xe được giao.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút), tải danh mục các ô lọc.\n3. Hệ thống tải trang 1 (10 phường/xã) theo bộ lọc, kèm dòng tóm tắt của toàn bộ kết quả.\n4. Bảng hiện các dòng nhân viên, gộp ô theo Tỉnh/TP › Phường/Xã › Phòng; chân bảng “Hiển thị a–b / N”.'],
        ['Dòng sự kiện phụ', '• Chuyển trang / đổi số phường/xã mỗi trang → tải lại trang tương ứng (đổi số dòng thì về trang 1).\n• Rê chuột vào icon ⓘ ở tiêu đề cột hoặc cạnh tiêu đề trang → hiện giải thích.\n• Không có dòng khớp → “Không có dữ liệu phù hợp bộ lọc.”, ẩn dòng tóm tắt và phân trang.\n• Lỗi tải → toast “Lỗi khi tải dữ liệu”.\n• Phiên đăng nhập hết hạn → hệ thống đưa về màn đăng nhập (quy tắc chung).'],
        ['Yêu cầu đặc biệt', 'Không lọc gì (khoảng 59 nghìn dòng / 3.312 phường/xã trên môi trường thử nghiệm) màn tải trong khoảng 15–18 giây (đo 18/11/2026). Có lọc theo tỉnh: khoảng 4–5 giây.'],
    ],
    'anh': [('01_report', 'Màn Báo cáo phân chia thị trường lúc mới mở (không lọc)'),
            ('04_read', 'Bảng chi tiết báo cáo — tìm nhanh “Âu Lâu”: 1 tỉnh/TP, 1 phường/xã, 18 dòng phụ trách'),
            ('05_tooltip', 'Icon ⓘ ở tiêu đề cột Phụ trách tất cả các hãng')],
    'ui': ui(UI7, UI_XEM),
    'ui_widths': UI7W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Kiểm tra quyền “%s”; không có → trang không tìm thấy (BR-01).\n– Tải lại trang (F5) ngay trên màn → xóa bộ lọc đã nhớ (như bấm Làm mới).\nAfter:\n– Khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút).\n– Tải danh mục các ô lọc; tải trang 1 kèm dòng tóm tắt.' % QUYEN],
        ['Chuyển trang', 'Click', 'After:\n– Giữ bộ lọc, tải trang được chọn. STT tỉnh giữ liên tục.'],
        ['Đổi số dòng mỗi trang', 'Change', 'After:\n– Giữ bộ lọc, về trang 1, tải lại với số phường/xã mới.'],
        ['Rê chuột vào icon ⓘ', 'Hover', 'After:\n– Hiện khung giải thích (dòng đậm + các gạch đầu dòng).'],
        ['Lỗi khi tải', 'System', 'After:\n– Toast “Lỗi khi tải dữ liệu”, bảng giữ trạng thái trước đó.'],
    ],
    'them': [
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', 'table', DATA_XEM, R.DATA_W,
         'Bảng dưới mô tả cách hệ thống lấy dữ liệu cho từng cột và nội dung icon ⓘ (nguyên văn trên giao diện). '
         'Báo cáo không có cột số tiền / số lượng; “chỉ tiêu” ở đây là các con số ở dòng tóm tắt.'),
        ('Danh sách popup mở từ số liệu', 'table', POPUP_XEM, R.POPUP_W, None),
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Cài đặt bộ lọc.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc báo cáo'],
        ['Mô tả', 'Thu hẹp báo cáo bằng ô tìm nhanh và 8 ô lọc: Quốc gia, Vùng, Tỉnh/TP, Phường/Xã, Phụ trách tất cả các hãng, Phòng phụ trách, Nhân viên phụ trách, Hãng xe. Không có ô bắt buộc.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn báo cáo.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa rồi bấm Tìm kiếm / Enter; hoặc chọn giá trị ở các ô lọc (khu vực ô lọc mở sẵn khi vào màn).\n2. Hệ thống áp đồng thời mọi điều kiện, tải lại bảng và dòng tóm tắt từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô chọn lọc ngay khi chọn; ô tìm nhanh chỉ lọc khi bấm Tìm kiếm / Enter.\n• Đổi Quốc gia / Vùng / Tỉnh/TP / Phòng phụ trách → danh sách ô con thu hẹp theo; giá trị đã chọn ở ô con không còn thuộc lựa chọn mới bị bỏ tự động.\n• Không khớp → “Không có dữ liệu phù hợp bộ lọc.”\n• Bấm Làm mới → xóa mọi điều kiện, xóa bộ lọc đã nhớ, tải lại trang 1.\n• Bộ lọc được ghi nhớ 10 phút trên trình duyệt; rời sang màn khác hoặc F5 thì về trống.'],
    ],
    'anh': [('02_filter', 'Lọc Tỉnh/TP = Tỉnh Khánh Hòa, Phụ trách tất cả các hãng = Không: còn 1 dòng'),
            ('11_filtercfg', 'Cửa sổ Cài đặt bộ lọc')],
    'ui': ui(UI8, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', 'Chữ tự do', 'Không', 'Trống', [
            '- Placeholder “Tìm theo tỉnh/TP, phường/xã, phòng, nhân viên hoặc số điện thoại”',
            '- Tìm gần đúng (chứa chuỗi) trong tên Tỉnh/TP, tên phường/xã, tên phòng, tên nhân viên (gồm cả mã phòng đứng trước), số điện thoại',
            '- Không phân biệt hoa thường; bỏ khoảng trắng đầu/cuối; ký tự % và _ hiểu là ký tự thường',
            '- Chỉ lọc khi bấm Tìm kiếm / Enter']],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', '–', ['- Ghi nhớ bộ lọc, áp mọi điều kiện, tải lại từ trang 1']],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', '–', ['- Xóa mọi điều kiện và bộ lọc đã ghi nhớ, tải lại trang 1']],
        ['Nút Ẩn tìm kiếm nâng cao / Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Mở', ['- Mở / đóng khu vực 8 ô lọc', '- Mặc định đang mở, nút ghi “Ẩn tìm kiếm nâng cao”; đóng lại thì ghi “Tìm kiếm nâng cao”']],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', '–', ['- Mở cửa sổ “Cài đặt bộ lọc”: tích ô lọc muốn hiện, kéo đổi thứ tự, Lưu / Khôi phục mặc định / Đóng (quy tắc chung)']],
        ['Ô Quốc gia', 'Dropdown', 'Enable', 'Quốc gia đang hoạt động', 'Không', 'Trống', [
            '- Chọn 1, có nút × xóa', '- Chọn Việt Nam: KHÔNG lọc (như để trống)', '- Chọn quốc gia khác: chỉ dòng có Tỉnh/TP thuộc quốc gia đó',
            '- Thu hẹp danh sách ô Vùng và Tỉnh/TP theo quốc gia đã chọn']],
        ['Ô Vùng', 'Dropdown', 'Enable', 'Vùng đang hoạt động (theo Quốc gia)', 'Không', 'Trống', ['- Chọn nhiều', '- Chỉ dòng có Tỉnh/TP thuộc các vùng đã chọn', '- Thu hẹp danh sách ô Tỉnh/TP']],
        ['Ô Tỉnh/TP', 'Dropdown', 'Enable', 'Tỉnh/TP đang hoạt động (theo Quốc gia, Vùng)', 'Không', 'Trống', ['- Chọn nhiều', '- Thu hẹp danh sách ô Phường/Xã']],
        ['Ô Phường/Xã', 'Dropdown', 'Enable', 'Phường/xã đang hoạt động thuộc các tỉnh đã chọn (chưa chọn tỉnh: mọi phường/xã của các tỉnh trong danh sách)', 'Không', 'Trống', ['- Chọn nhiều, gõ để tìm']],
        ['Ô Phụ trách tất cả các hãng', 'Dropdown', 'Enable', 'Có / Không', 'Không', 'Trống', ['- Lựa chọn:', '- “Có”: chỉ dòng có X ở cột Phụ trách tất cả các hãng', '- “Không”: chỉ dòng để trống ở cột đó', '- Mặc định trống = cả hai']],
        ['Ô Phòng phụ trách', 'Dropdown', 'Enable', 'Mọi phòng ban đang hoạt động, dạng “Mã phòng - Tên phòng”', 'Không', 'Trống', ['- Chọn nhiều', '- Thu hẹp danh sách ô Nhân viên phụ trách theo phòng HIỆN TẠI của nhân viên']],
        ['Ô Nhân viên phụ trách', 'Dropdown', 'Enable', 'Mọi nhân viên (kể cả đã nghỉ), dạng “Mã phòng - Họ tên”', 'Không', 'Trống', ['- Chọn nhiều, gõ để tìm']],
        ['Ô Hãng xe', 'Dropdown', 'Enable', 'Hãng xe đang hoạt động', 'Không', 'Trống', ['- Chọn nhiều', '- Chỉ dòng nhân viên được giao ít nhất 1 hãng đã chọn tại phường/xã', '- Dòng phụ trách tất cả các hãng nhưng không giao hãng cụ thể: KHÔNG khớp']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tìm kiếm / Enter', 'Click', 'After:\n– Ghi nhớ bộ lọc, tải lại bảng + dòng tóm tắt từ trang 1.'],
        ['Chọn giá trị ở ô chọn', 'Change', 'Before:\n– Ô vừa đổi là Quốc gia / Vùng / Tỉnh/TP / Phòng phụ trách → bỏ giá trị ô con (Vùng, Tỉnh/TP, Phường/Xã, Nhân viên phụ trách) không còn trong danh sách.\nAfter:\n– Ghi nhớ bộ lọc, tải lại từ trang 1.'],
        ['Gõ ô tìm nhanh', 'Change', 'After:\n– Chưa tải lại cho tới khi bấm Tìm kiếm / Enter.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xóa mọi điều kiện và bộ lọc đã nhớ, về trang 1, tải lại.'],
        ['Bấm Ẩn tìm kiếm nâng cao / Tìm kiếm nâng cao', 'Click', 'After:\n– Đóng / mở khu vực ô lọc.'],
    ],
})

# 2.3 Tùy chỉnh cột ---------------------------------------------------------------
FR.append({
    'ten': 'Tùy chỉnh cột hiển thị',
    'qtc': 'Tùy chỉnh cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tùy chỉnh cột hiển thị'],
        ['Mô tả', 'Ẩn / hiện và đổi thứ tự các cột của bảng chi tiết báo cáo; cấu hình lưu theo từng người dùng. Chỉ áp cho bảng trên màn; bản In và file Excel giữ khuôn riêng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Cấu hình cột hiển thị.\n2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột”.\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự rồi bấm Lưu.\n4. Hệ thống áp dụng lên bảng, lưu cấu hình, báo “Cập nhật thành công”.'],
        ['Dòng sự kiện phụ', '• Cột STT và Tỉnh/TP là cột khóa: luôn hiện, không kéo được.\n• Ẩn cột Phường/Xã hoặc Phòng phụ trách → bỏ luôn ô gộp của cột đó, các cột khác không lệch.\n• Bấm Đóng → bỏ thay đổi vừa chỉnh. Lỗi lưu: “Thao tác thất bại”.\n• Cấu hình giữ nguyên sau F5, đăng nhập lại.'],
    ],
    'menu_them': ' => Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': POPUP % 'Tuỳ chỉnh cột',
    'anh': [('09_colcfg', 'Cửa sổ Tuỳ chỉnh cột — STT, Tỉnh/TP bị khóa')],
    'ui': ui(UI8, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', '–', ['- “Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng.”']],
        ['Danh sách cột', 'Table/Grid', 'Enable', '8 cột', 'Không', 'Theo cấu hình đã lưu', ['- STT, Tỉnh/TP, Phường/Xã, Phòng phụ trách, Nhân viên phụ trách, Số điện thoại, Phụ trách tất cả các hãng, Hãng xe phụ trách', '- Mặc định hiện tất cả, đúng thứ tự trên', '- Mỗi cột có ô tích và biểu tượng ☰ kéo đổi vị trí']],
        ['Cột khóa', 'Table/Grid', 'Disable', '–', '–', 'Luôn tích', ['- STT, Tỉnh/TP: ô tích xám kèm biểu tượng khóa, không bỏ tích, không kéo được']],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', ['- Tích / bỏ tích mọi cột (trừ cột khóa)']],
        ['Dòng đếm', 'Label', 'Hiển thị', '–', '–', 'Đang chọn 8/8 cột', ['- “Đang chọn x/8 cột”']],
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', ['- Áp dụng, lưu cấu hình theo người dùng; “Cập nhật thành công” (lỗi: “Thao tác thất bại”)']],
        ['Nút Đóng / (x)', 'Button', 'Enable', '–', '–', '–', ['- Đóng, bỏ thay đổi']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Cấu hình cột hiển thị', 'Click', 'After:\n– Mở cửa sổ theo cấu hình đang dùng.'],
        ['Tích / bỏ tích, kéo ☰', 'Change / Drag', 'After:\n– Đổi trạng thái trong cửa sổ (chưa áp dụng).'],
        ['Bấm Lưu', 'Click', 'After:\n– Ẩn / hiện, đổi thứ tự cột trên bảng; lưu theo người dùng; “Cập nhật thành công”. Không tải lại dữ liệu, không đổi bộ lọc.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng, không áp dụng.'],
    ],
})

# 2.4 Xuất Excel -------------------------------------------------------------------
FR.append({
    'ten': 'Xuất báo cáo ra Excel', 'uc': 'uc_xuat',
    'qtc': 'Quy tắc Excel.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất báo cáo ra Excel'],
        ['Mô tả', 'Xuất mọi dòng khớp bộ lọc đang áp (không chỉ trang đang xem) ra file Excel gộp ô như trên màn; người dùng chọn trường và thứ tự cột (BR-09).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng lọc báo cáo (nếu cần), bấm Xuất Excel.\n2. Hệ thống mở cửa sổ “Chọn trường xuất Excel”, tích sẵn cả 7 trường.\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự rồi bấm Xuất file.\n4. Hệ thống tải file bao_cao_phan_chia_thi_truong.xlsx, đóng cửa sổ, báo “Xuất Excel thành công”.'],
        ['Dòng sự kiện phụ', '• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Lỗi → “Lỗi khi xuất Excel”, cửa sổ không đóng.\n• Không lọc gì: file khoảng 59 nghìn dòng, mất khoảng 15–20 giây.\n• Trong lúc xuất, nút Xuất Excel không bấm được.'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': POPUP % 'Chọn trường xuất Excel',
    'anh': [('08_export', 'Cửa sổ Chọn trường xuất Excel')],
    'ui': ui(UI8, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', '–', ['- “Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file.”']],
        ['Danh sách trường', 'Table/Grid', 'Enable', '7 trường', 'Không', 'Tích tất cả', [
            '- Tỉnh/TP, Phường/Xã, Phòng phụ trách, Nhân viên phụ trách, Số điện thoại, Phụ trách tất cả các hãng, Hãng xe phụ trách',
            '- Cột STT luôn có ở đầu file, không nằm trong danh sách', '- Mặc định tích cả 7 trường (không theo cột đang ẩn trên bảng)']],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', ['- Tích / bỏ tích mọi trường']],
        ['Dòng đếm', 'Label', 'Hiển thị', '–', '–', 'Đang chọn 7/7 trường', ['- “Đang chọn x/7 trường”']],
        ['Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Enable', ['- Tải file', '- Không bấm được khi chưa chọn trường nào hoặc đang xuất']],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', ['- Đóng cửa sổ, không xuất']],
        ['File Excel', 'File', '–', '–', '–', '–', [
            '- Tên file bao_cao_phan_chia_thi_truong.xlsx, trang tính “Phân chia thị trường”',
            '- Dòng 1 “BÁO CÁO PHÂN CHIA THỊ TRƯỜNG” in đậm, căn giữa; dòng 2 tiêu đề cột nền xanh nhạt',
            '- Dữ liệu đúng thứ tự trên màn; STT đánh theo tỉnh; STT + Tỉnh/TP gộp theo tỉnh, Phường/Xã gộp theo xã, Phòng phụ trách gộp theo phòng (trường nào không chọn thì thôi gộp)',
            '- Cột Phụ trách tất cả các hãng ghi “X” hoặc trống; số điện thoại giữ dạng chữ (không mất số 0 đầu)',
            '- Kẻ khung đen mọi ô, chữ tự xuống dòng',
            '- Cuối file khối ký “Ngày…….Tháng…….Năm…….”, “Người lập”, “(Ký, họ tên)”']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ, tích sẵn 7 trường.'],
        ['Tích / bỏ tích, kéo ☰', 'Change / Drag', 'After:\n– Đổi trường và thứ tự cột sẽ xuất.'],
        ['Bấm Xuất file', 'Click', 'During:\n– Lấy toàn bộ dòng theo bộ lọc đang áp (gồm cả từ khóa tìm nhanh).\n– Lỗi → “Lỗi khi xuất Excel”, không thực hiện bước After.\nAfter:\n– Dựng và tải file theo trường / thứ tự đã chọn, đóng cửa sổ, báo “Xuất Excel thành công”.'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.5 In ---------------------------------------------------------------------------
FR.append({
    'ten': 'In báo cáo', 'uc': 'uc_in',
    'qtc': 'In.',
    'gioi_thieu': [
        ['Tên chức năng', 'In báo cáo phân chia thị trường'],
        ['Mô tả', 'Xem trước và in báo cáo theo mẫu “BÁO CÁO PHÂN CHIA THỊ TRƯỜNG”, khổ ngang, gồm MỌI dòng theo bộ lọc đang áp; tối đa 2.000 dòng (BR-10).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng lọc báo cáo, bấm In.\n2. Hệ thống mở cửa sổ “Xem trước báo cáo phân chia thị trường”: ảnh tiêu đề công ty, tên báo cáo, bảng 8 cột gộp ô như màn hình, khối ký “Người lập”.\n3. Người dùng bấm In trong cửa sổ để in ra máy in, hoặc bấm × để đóng.'],
        ['Dòng sự kiện phụ', '• Vượt 2.000 dòng → cửa sổ chỉ hiện: “Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.”, ẩn nút In.\n• Không có dòng nào → “Không có dữ liệu để in”.\n• Thiếu mẫu in → “Không tìm thấy mẫu in”.'],
    ],
    'menu_them': ' => In {icon:btn_in}',
    'ghi_chu_layout': 'Cửa sổ xem trước bản in được mở ngay trên màn báo cáo theo đường dẫn ở trên.',
    'anh': [('10_print', 'Cửa sổ Xem trước báo cáo phân chia thị trường (tìm nhanh “Âu Lâu”)'),
            ('10b_print_limit', 'Không lọc gì: 59,225 dòng vượt mức in tối đa 2,000 dòng')],
    'ui': ui(UI7, [
        ['Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Xem trước báo cáo phân chia thị trường', ['- Nút × đóng cửa sổ']],
        ['Nút In', 'Button', 'Enable / Disable / Ẩn', '–', 'Hiển thị', ['- In bản xem trước ra máy in', '- Ẩn khi vượt trần 2.000 dòng', '- Mờ, không bấm được khi đang tải hoặc không có dữ liệu']],
        ['Bản xem trước', 'Label', 'Read-only', '–', 'Theo dữ liệu', [
            '- Khổ ngang; đầu trang là ảnh tiêu đề công ty', '- Tiêu đề “BÁO CÁO PHÂN CHIA THỊ TRƯỜNG” in đậm',
            '- Bảng 8 cột: STT, Tỉnh/TP, Phường/Xã, Phòng phụ trách, Nhân viên phụ trách, Số điện thoại, Phụ trách tất cả các hãng, Hãng xe phụ trách — luôn đủ 8 cột, không theo Tuỳ chỉnh cột',
            '- Ô gộp Tỉnh/TP, Phường/Xã, Phòng phụ trách canh đầu ô (nhóm dài vắt nhiều trang vẫn đọc được tên ở dòng đầu)',
            '- STT đánh lại từ 1 theo tỉnh trong bản in', '- Cuối bản in khối ký “Người lập”']],
        ['Dòng nhắc vượt trần', 'Label', 'Ẩn', '–', 'Ẩn', ['- Chỉ hiện khi vượt 2.000 dòng (nội dung ở Dòng sự kiện phụ)', '- N có dấu phẩy ngăn hàng nghìn']],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm In (màn báo cáo)', 'Click', 'Before:\n– Đếm số dòng theo bộ lọc; > 2.000 → chỉ hiện dòng nhắc, dừng.\nAfter:\n– Điền mẫu in với mọi dòng theo bộ lọc, mở cửa sổ xem trước.'],
        ['Bấm In (trong cửa sổ)', 'Click', 'After:\n– Gửi bản xem trước ra máy in, không mở tab mới.'],
        ['Bấm ×', 'Click', 'After:\n– Đóng cửa sổ, giữ nguyên bảng và bộ lọc.'],
    ],
})

MA_TRAN_FR = ['FR-01 Xem báo cáo phân chia thị trường', 'FR-02 Tìm kiếm và lọc', 'FR-03 Tùy chỉnh cột hiển thị',
              'FR-04 Xuất báo cáo ra Excel', 'FR-05 In báo cáo']

S = {
    'ten': TEN,
    'menu': [('CSKH trước bán', 'menu_phanhe'), ('Báo cáo', 'menu_nhom'), ('Báo cáo thị trường', 'menu_nhomcon'), (TEN, 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu báo cáo.',
        'Làm rõ báo cáo lấy dữ liệu từ những phiếu phân chia thị trường nào, điều kiện để một phường/xã, một nhân viên lên báo cáo, cách gộp dòng trùng, cách phân trang theo phường/xã và các ô lọc.',
        'Phạm vi: Xem báo cáo, Tìm kiếm và lọc, Tùy chỉnh cột hiển thị, Xuất Excel, In. Báo cáo chỉ đọc, không ghi dữ liệu.',
    ],
    'thuat_ngu': [
        ['Phiếu phân chia thị trường theo phòng ban', 'Phiếu giao Tỉnh/TP, khu vực kinh doanh (bung ra từng phường/xã) cho 1 phòng hoặc 1 bộ phận của phòng.'],
        ['Phiếu phân chia thị trường theo nhân viên', 'Phiếu giao cho 1 nhân viên các phường/xã (trong phạm vi phiếu của phòng), kèm cờ phụ trách tất cả các hãng hoặc danh sách hãng xe.'],
        ['Dòng phụ trách', '1 dòng của bảng = 1 nhân viên phụ trách 1 phường/xã cho 1 phòng.'],
        ['Phụ trách tất cả các hãng', 'Nhân viên được giao mọi hãng xe tại phường/xã đó (cột hiện “X”).'],
        ['Vùng', 'Nhóm các Tỉnh/TP theo địa lý (vd Tây Bắc Bộ, Đông Nam Bộ), khai ở danh mục Vùng.'],
        ['Ô gộp', 'Ô của bảng trải dài nhiều dòng liền nhau có cùng Tỉnh/TP, Phường/Xã hoặc Phòng.'],
    ],
    'quyen_truoc': ['Màn hình CHỈ ĐỌC, gắn 1 quyền xem riêng (phân hệ CSKH trước bán). Quyền được cấp cho Vai trò ở màn Phân quyền; người dùng nhận quyền qua Vai trò của mình tại công ty đang làm việc.'],
    'quyen_rows': [[QUYEN, 'Hiện mục menu; mở màn; xem, tìm kiếm / lọc, tùy chỉnh cột, xuất Excel, in. Quyền không chia mức phạm vi.'],
                   ['(Không có quyền)', 'Ẩn mục menu; mở bằng đường dẫn trực tiếp → trang không tìm thấy; hệ thống từ chối lấy dữ liệu.']],
    'ma_tran': [['Chức năng', QUYEN, 'Không có quyền']] + [[f, 'Có', 'Không'] for f in MA_TRAN_FR],
    'ma_tran_widths': [2.6, 2.2, 1.2],
    'quyen_sau': [
        'Báo cáo KHÔNG phân phạm vi theo công ty / phòng ban / bộ phận: người có quyền xem được toàn bộ phân chia thị trường của mọi phòng, mọi công ty (BR-01).',
        'Ô lọc Phòng phụ trách, Nhân viên phụ trách liệt kê mọi phòng, mọi nhân viên, không giới hạn theo đơn vị của người xem.',
        'File Excel và bản In dùng cùng điều kiện và phạm vi với bảng trên màn.',
    ],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Quyền và phạm vi', ['– Phải có quyền “%s” mới thấy menu, mở được màn và lấy được dữ liệu.' % QUYEN, '– Không có quyền: mục menu ẩn; mở bằng đường dẫn → trang không tìm thấy.', '– Không phân phạm vi: có quyền là xem toàn bộ.'], ['Mọi chức năng']),
        ('BR-02', 'Dòng lên báo cáo', ['– Phường/xã thuộc phiếu phân chia theo phòng ban Đã duyệt.', '– Nhân viên thuộc phiếu phân chia theo nhân viên Đã duyệt của CÙNG phòng, được giao đúng Tỉnh/TP và phường/xã đó.', '– Phiếu Đang tạo / Chờ duyệt / đã Hủy duyệt / đã xóa: không tính.', '– Phường/xã của phòng chưa có nhân viên nào được giao: không hiện.'], ['Xem báo cáo', 'Xuất Excel', 'In']),
        ('BR-03', 'Gộp dòng trùng', ['– Nhiều phiếu nhân viên trùng (tỉnh, phường/xã, phòng, nhân viên) → 1 dòng.', '– Phụ trách tất cả các hãng = X nếu ít nhất 1 phiếu đánh dấu.', '– Hãng xe phụ trách = hợp các hãng trên các phiếu, bỏ trùng, xếp A–Z, cách dấu phẩy.'], ['Xem báo cáo', 'Xuất Excel', 'In']),
        ('BR-04', 'Thứ tự và gộp ô', ['– Tỉnh/TP theo thứ tự trong danh mục Tỉnh/TP; trong tỉnh: phường/xã A–Z; trong phường/xã: phòng A–Z; trong phòng: nhân viên A–Z.', '– Gộp ô 4 cấp STT + Tỉnh/TP › Phường/Xã › Phòng; chữ ô gộp canh đầu.', '– Không sắp xếp theo cột.'], ['Xem báo cáo', 'Xuất Excel', 'In']),
        ('BR-05', 'Phân trang theo phường/xã', ['– Mỗi trang 10 / 20 / 50 / 100 PHƯỜNG/XÃ (mặc định 10) kèm mọi dòng nhân viên của các phường/xã đó.', '– “Hiển thị a–b / N”: N = số phường/xã khớp bộ lọc.', '– STT đánh theo tỉnh, liên tục qua các trang; tỉnh vắt 2 trang giữ nguyên số và lặp tên ở trang sau.'], ['Xem báo cáo']),
        ('BR-06', 'Dòng tóm tắt', ['– “N tỉnh/TP · M phường/xã · K dòng phụ trách” đếm trên toàn bộ kết quả lọc, số có dấu phẩy ngăn hàng nghìn.'], ['Xem báo cáo']),
        ('BR-07', 'Bộ lọc', ['– Không ô nào bắt buộc; các ô kết hợp theo điều kiện VÀ.', '– Quốc gia Việt Nam = không lọc.', '– Vùng / Tỉnh/TP / Phường/Xã / Phòng / Nhân viên / Hãng xe chọn nhiều.', '– Ô con thu hẹp theo ô cha (Quốc gia → Vùng → Tỉnh/TP → Phường/Xã; Phòng → Nhân viên theo phòng hiện tại); đổi ô cha thì bỏ giá trị ô con không còn hợp lệ.', '– Lọc Hãng xe: chỉ còn dòng được giao hãng đã chọn; cột Hãng xe phụ trách chỉ hiện các hãng khớp ô lọc và cột Phụ trách tất cả các hãng chỉ xét các phiếu có hãng khớp (dòng đang có X có thể thành trống — đang chờ xác nhận nghiệp vụ).', '– Tìm nhanh gần đúng trên Tỉnh/TP, phường/xã, phòng, nhân viên, số điện thoại; chỉ áp khi Tìm kiếm / Enter; ô chọn áp ngay.'], ['Tìm kiếm và lọc']),
        ('BR-08', 'Ghi nhớ bộ lọc', ['– Bộ lọc ghi nhớ 10 phút trên trình duyệt (cùng trình duyệt, kể cả tab mới).', '– Rời sang màn khác, tải lại trang (F5) hoặc bấm Làm mới: về trống.'], ['Tìm kiếm và lọc']),
        ('BR-09', 'Xuất Excel', ['– Xuất mọi dòng khớp bộ lọc (mọi trang), đúng thứ tự trên màn, gộp ô như màn, cột theo trường / thứ tự người dùng chọn, STT luôn đứng đầu.', '– Không theo cấu hình Tuỳ chỉnh cột.'], ['Xuất Excel']),
        ('BR-10', 'In', ['– Mẫu “BÁO CÁO PHÂN CHIA THỊ TRƯỜNG”, khổ ngang, đủ 8 cột, mọi dòng theo bộ lọc.', '– Tối đa 2.000 dòng; vượt thì không in, hiện dòng nhắc thu hẹp bộ lọc hoặc dùng Xuất Excel.'], ['In']),
        ('BR-11', 'Nguồn tên hiển thị', ['– Tên Tỉnh/TP, phường/xã và “Mã phòng - Họ tên” nhân viên lấy theo nội dung lưu trên phiếu phân chia.', '– Tên phòng theo danh mục phòng ban hiện tại; số điện thoại theo hồ sơ nhân viên hiện tại.'], ['Xem báo cáo', 'Xuất Excel', 'In']),
    ],
    'phan5': {
        'title': 'Phần 5. Bảng danh sách các màn hình liên quan dữ liệu báo cáo',
        'cau_dan': 'Báo cáo chỉ đọc. Các màn hình dưới đây ghi ra dữ liệu mà báo cáo tổng hợp lại (nguồn số liệu), cung cấp danh mục tham chiếu, hoặc dùng chung nguồn dữ liệu phân chia thị trường.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng có quyền xem báo cáo',
    'mains': [('FR-01', 'Xem báo cáo phân chia thị trường', 'view'), ('FR-04', 'Xuất báo cáo ra Excel', 'io'), ('FR-05', 'In báo cáo', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc', 'view'), ('FR-03', 'Tùy chỉnh cột hiển thị', 'view')],
    'rieng': [('FR-04', 'Xuất báo cáo ra Excel', 'io', 'uc_xuat'), ('FR-05', 'In báo cáo', 'io', 'uc_in')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', R.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT, banned=BANNED)

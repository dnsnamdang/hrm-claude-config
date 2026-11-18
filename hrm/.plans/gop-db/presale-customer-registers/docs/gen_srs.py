# -*- coding: utf-8 -*-
"""SRS - Danh sách đăng ký khách hàng toàn công ty (form Danh mục quốc gia + quy tắc màn báo cáo của skill srs-documenter).

Khuôn: lookup-stock-companies/docs/gen_srs.py (đã duyệt). Thư viện: _lib_report.py (bản chép) + danh-muc-kho/docs/_lib_win.py.
Nguồn (code HRM hiện tại, develop):
  FE hrm-client/pages/assign/report/customer-registers/index.vue, components/subsystem-menu/presale.js,
     utils/mixins/{filterStateMixin, columnCustomizationMixin, exportFieldsMixin}.js, plugins/axios.js (403/401)
  BE Modules/Assign/Services/Report/CustomerRegisterService.php, Http/Controllers/Api/V1/CustomerRegisterController.php,
     Transformers/CustomerRegisterResource, Routes/api.php (gate quyền), app/ExcelExport/ExportColumnRegistry.php,
     app/Helper/CustomerOwnership.php (màn khác dùng chung dữ liệu đăng ký)
  Ảnh: capture.js (dev-hrm, 18/11/2026).
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _lib_report as R  # noqa: E402
L = R.L

TEN = 'Danh sách đăng ký khách hàng toàn công ty'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
QUYEN = 'Xem danh sách khách hàng đã đăng ký'
Q = 'Người dùng có quyền "%s"' % QUYEN
DK = '1. Người dùng đăng nhập thành công.\n2. Người dùng được cấp quyền "%s".' % QUYEN
POPUP = 'Cửa sổ %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'

UI7 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả']
UI7W = [0.55, 1.25, 0.85, 0.8, 0.95, 0.85, 2.6]
UI8 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả']
UI8W = [0.55, 1.15, 0.85, 0.75, 0.95, 0.65, 0.85, 2.3]


def ui(header, rows):
    return [header] + [[str(i + 1)] + r for i, r in enumerate(rows)]


# ------------------------------------------------------------------ Phần 5 (dò code 18/11/2026)
P5 = [
    ('Nguồn dữ liệu', 'Báo giá hãng — nút "Đăng ký khách hàng" trên danh sách báo giá hãng (sinh ra mỗi dòng đăng ký; hủy đăng ký cũng làm tại hệ thống ERP)',
     'Hệ thống ERP (chưa có màn trên HRM)'),
    ('Mở từ màn này', 'Chi tiết báo giá (bấm Số báo giá của báo giá thường)', 'CSKH trước bán => Báo giá; Bán hàng => Báo giá'),
    ('Mở từ màn này', 'Chi tiết báo giá hãng (bấm Số báo giá của báo giá hãng)', 'Hệ thống ERP (mở ở tab mới)'),
    ('Dùng chung dữ liệu đăng ký', 'Meeting — Tạo / Sửa meeting: không cho chọn khách hàng cá nhân hoặc người liên hệ đang được NGƯỜI KHÁC đăng ký còn hạn, báo “Đã có người đăng ký nên bạn không được phép chọn”',
     'Meeting => Tổng hợp meeting'),
    ('Dùng chung dữ liệu đăng ký', 'Dự án TKT — Tạo / Sửa dự án: chặn chọn khách hàng cá nhân / người liên hệ đang được người khác đăng ký còn hạn (cùng thông báo)',
     'CSKH trước bán => Dự án TKT'),
    ('Dùng chung dữ liệu đăng ký', 'Báo giá — Tạo / Sửa báo giá cho khách hàng nhập tay: chặn chọn khách hàng cá nhân / người liên hệ đang được người khác đăng ký còn hạn',
     'CSKH trước bán => Báo giá; Bán hàng => Báo giá'),
    ('Dùng chung dữ liệu đăng ký', 'Danh mục khách hàng — ô chọn khách hàng khoá khách cá nhân đang được người khác đăng ký; khách mình đăng ký còn hạn được tính là “khách của mình” (hiện đủ số điện thoại, kể cả khi xuất Excel)',
     'Danh mục dùng chung => Đối tác => Khách hàng'),
    ('Danh mục tham chiếu', 'Khách hàng, người liên hệ (tên hiển thị ở cột Khách hàng đăng ký)', 'Danh mục dùng chung => Đối tác => Khách hàng'),
    ('Danh mục tham chiếu', 'Hồ sơ nhân sự, phòng ban (cột Người đăng ký = Mã phòng - Họ tên; nguồn ô lọc Người đăng ký)', 'Thông tin nhân sự'),
]

FR = []

# 2.1 Xem danh sách --------------------------------------------------------------
UI_XEM = [
    ['Tiêu đề trang', 'Label', 'Hiển thị', '–', TEN, ['- Trên thanh đầu trang']],
    ['Tiêu đề bảng', 'Label', 'Hiển thị', '–', TEN, ['- Đầu khối bảng, bên trái']],
    ['Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', ['- Mở cửa sổ “Chọn trường xuất file” (mục 2.3)', '- Không bấm được khi đang xuất file']],
    ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', '–', 'Hiển thị', ['- Biểu tượng cột, mở cửa sổ “Tuỳ chỉnh cột” (mục 2.4)']],
    ['Bảng danh sách', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
        '- Mỗi dòng là 1 lượt đăng ký khách hàng, không gộp dòng',
        '- Cột: STT, Khách hàng đăng ký, Ngày đăng ký, Thời hạn đăng ký, Người đăng ký, Số báo giá, Ghi chú — mỗi cột mô tả ở 1 dòng bên dưới',
        '- Không có dòng tổng, không có thao tác Thêm / Sửa / Xoá trên dòng',
        '- Cột STT và Khách hàng đăng ký đứng yên khi cuộn ngang']],
    ['Cột STT', 'Table/Grid', 'Read-only', 'Số', 'Theo dữ liệu', ['- Đánh liên tục qua các trang', '- Cột khóa, không ẩn được']],
    ['Cột Khách hàng đăng ký', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
        '- Dòng 1: tên khách hàng (theo danh mục khách hàng)',
        '- Dòng 2 (chữ nhỏ, nghiêng, xám): người liên hệ được đăng ký — chỉ có khi đăng ký theo người liên hệ',
        '- Không lấy được tên khách hàng: chỉ hiện dòng người liên hệ', '- Tên dài tự xuống dòng', '- Cột khóa']],
    ['Cột Ngày đăng ký', 'Table/Grid', 'Read-only', 'dd/mm/yyyy HH:mm', 'Theo dữ liệu', ['- Thời điểm tạo đăng ký', '- Sắp xếp được (mặc định giảm dần)']],
    ['Cột Thời hạn đăng ký', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', ['- Ngày hết hạn giữ khách', '- Sắp xếp được']],
    ['Cột Người đăng ký', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- “Mã phòng ban - Họ tên” theo hồ sơ hiện tại của nhân viên; chưa có phòng ban thì chỉ ghi họ tên', '- Tối đa 2 dòng']],
    ['Cột Số báo giá', 'Hyperlink', 'Enable', '–', 'Theo dữ liệu', [
        '- Số báo giá sinh ra đăng ký, dạng liên kết gạch chân',
        '- Báo giá thường: mở màn chi tiết báo giá trên HRM ở tab mới',
        '- Báo giá hãng: mở màn chi tiết báo giá hãng của hệ thống ERP ở tab mới (màn đích tự kiểm quyền xem)',
        '- Không có số báo giá: để trống']],
    ['Cột Ghi chú', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Ghi chú nhập lúc đăng ký', '- Hiện tối đa 2 dòng, rê chuột để xem đủ nội dung']],
    ['Thông báo bảng trống', 'Label', 'Ẩn', '–', 'Ẩn', ['- “Không có dữ liệu phù hợp bộ lọc.” giữa bảng', '- Chân bảng “Không có đăng ký nào.”']],
    ['Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', '10 dòng/trang', ['- Chân bảng “Hiển thị a–b / N”', '- Ô “Số dòng/trang:”, nút « ‹ số trang › »']],
    ['Thông báo lỗi', 'Toast', 'Ẩn', '–', 'Ẩn', ['- Lỗi tải dữ liệu: “Lỗi khi tải dữ liệu”', '- Không có quyền: “Bạn không có quyền thực hiện chức năng này”']],
]

DATA_XEM = R.numbered(R.DATA_HEAD, [
    ('Tập dữ liệu (dòng)', ['Mọi lượt đăng ký khách hàng của TOÀN công ty (mọi công ty, phòng ban, nhân viên), gồm cả còn hạn và hết hạn, khớp các điều kiện lọc (BR-02).',
                           'Đăng ký sinh ra khi người lập báo giá hãng bấm “Đăng ký khách hàng” trên hệ thống ERP; đăng ký bị hủy thì bị xóa hẳn, không còn trên danh sách.',
                           'Thời điểm số liệu: tức thời, lúc mở màn / tìm kiếm.'], '—'),
    ('Khách hàng đăng ký', ['Tên khách hàng theo danh mục khách hàng của đăng ký; dòng 2 là tên người liên hệ được đăng ký (đăng ký mức người liên hệ).'], '—'),
    ('Ngày đăng ký', ['Thời điểm tạo đăng ký (ngày giờ phút).'], '—'),
    ('Thời hạn đăng ký', ['Ngày hết hạn giữ khách lưu trên đăng ký (= ngày đăng ký + số ngày cấu hình tại thời điểm đăng ký).',
                         'Còn hạn: Thời hạn đăng ký ≥ ngày hôm nay (so theo NGÀY, hết hạn hôm nay vẫn còn hạn tới hết ngày). Hết hạn: Thời hạn đăng ký < hôm nay (BR-03).'], '—'),
    ('Người đăng ký', ['Nhân viên đăng ký: “Mã phòng ban - Họ tên” theo hồ sơ HIỆN TẠI (nhân viên đổi phòng thì hiện phòng mới).'], '—'),
    ('Số báo giá', ['Số của báo giá thường nếu đăng ký gắn báo giá thường; nếu không thì số báo giá hãng.'], '—'),
    ('Ghi chú', ['Nội dung ghi chú nhập khi đăng ký.'], '—'),
    ('Chân bảng N', ['N = tổng số lượt đăng ký khớp bộ lọc (mọi trang).'], '—'),
])

FR.append({
    'ten': 'Xem danh sách đăng ký khách hàng',
    'qtc': 'Màn danh sách, Sắp xếp dữ liệu bảng, Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách đăng ký khách hàng toàn công ty'],
        ['Mô tả', 'Hiển thị mọi lượt nhân viên kinh doanh đăng ký giữ khách hàng / người liên hệ (để người khác không chen vào trong thời hạn), của toàn công ty, kèm ngày đăng ký, thời hạn, người đăng ký, số báo giá và ghi chú. Màn chỉ để xem.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải trang 1 (10 dòng), sắp theo Ngày đăng ký giảm dần (đăng ký mới nhất lên đầu).\n3. Chân bảng hiện “Hiển thị 1–10 / N”.'],
        ['Dòng sự kiện phụ', '• Bấm tiêu đề cột Ngày đăng ký / Thời hạn đăng ký → sắp tăng dần, bấm lần nữa → giảm dần; tải lại từ trang 1.\n• Bấm Số báo giá → mở báo giá ở tab mới.\n• Không có quyền mà mở bằng đường dẫn → toast “Bạn không có quyền thực hiện chức năng này”, bảng trống.\n• Phiên đăng nhập hết hạn → hệ thống chuyển về màn đăng nhập.'],
        ['Yêu cầu đặc biệt', 'Không lọc (khoảng 2.100 dòng trên môi trường thử nghiệm) màn tải trong khoảng 4–7 giây (đo 18/11/2026).'],
    ],
    'anh': [('01_list', 'Màn Danh sách đăng ký khách hàng toàn công ty lúc mới mở')],
    'ui': ui(UI7, UI_XEM),
    'ui_widths': UI7W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Kiểm tra quyền “%s”; không có quyền → từ chối, toast “Bạn không có quyền thực hiện chức năng này”.\nAfter:\n– Tải trang 1, 10 dòng, sắp theo Ngày đăng ký giảm dần; nạp cấu hình cột của người dùng.' % QUYEN],
        ['Bấm tiêu đề cột sắp xếp được', 'Click', 'After:\n– Đổi chiều tăng / giảm, tải lại từ trang 1. Cùng giá trị thì đăng ký tạo sau đứng trước.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click / Change', 'After:\n– Giữ bộ lọc và sắp xếp, tải lại; đổi số dòng thì về trang 1.'],
        ['Bấm Số báo giá', 'Click', 'After:\n– Mở màn chi tiết báo giá (HRM) hoặc báo giá hãng (ERP) ở tab mới; màn danh sách giữ nguyên.'],
        ['Lỗi khi tải', 'System', 'After:\n– Toast “Lỗi khi tải dữ liệu”.'],
        ['Phiên đăng nhập hết hạn', 'System', 'After:\n– Đăng xuất, chuyển về màn đăng nhập.'],
    ],
    'them': [
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', 'table', DATA_XEM, R.DATA_W,
         'Bảng dưới mô tả nguồn và cách lấy từng cột. Màn không có icon ⓘ ở tiêu đề cột nên cột “Nội dung icon ⓘ” để “—”.'),
    ],
})

# 2.2 Tìm kiếm và lọc ------------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Cài đặt bộ lọc.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách đăng ký'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm nhanh và 4 ô lọc ở khu vực Tìm kiếm nâng cao: Khách hàng đăng ký, Thời hạn đăng ký, Người đăng ký, Số báo giá.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa rồi bấm Tìm kiếm / Enter; hoặc bấm Tìm kiếm nâng cao rồi nhập / chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện, tải lại bảng từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô tìm nhanh, Khách hàng đăng ký, Số báo giá chỉ lọc khi bấm Tìm kiếm / Enter; ô Thời hạn đăng ký, Người đăng ký lọc ngay khi chọn.\n• Không có kết quả → “Không có dữ liệu phù hợp bộ lọc.”, chân bảng “Không có đăng ký nào.”\n• Bấm Làm mới → xóa mọi điều kiện và sắp xếp, tải lại từ trang 1.\n• Rời màn rồi quay lại / tải lại trang → các ô lọc về trống.'],
    ],
    'anh': [('02_filter', 'Khu vực tìm kiếm và lọc (đã mở Tìm kiếm nâng cao)'),
            ('03_conhan', 'Lọc Thời hạn đăng ký = Còn hạn')],
    'ui': ui(UI8, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', 'Chữ tự do', 'Không', 'Trống', [
            '- Placeholder “Tìm theo khách hàng, người liên hệ, người đăng ký, số báo giá”',
            '- Tìm gần đúng (chứa chuỗi) theo: tên khách hàng, mã khách hàng, tên người liên hệ, họ tên người đăng ký, số báo giá (thường và hãng)',
            '- Không phân biệt hoa thường, có dấu / không dấu; bỏ khoảng trắng đầu / cuối', '- Có nút × xóa nhanh']],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', '–', ['- Áp mọi điều kiện, tải lại từ trang 1']],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', '–', ['- Xóa mọi điều kiện lọc và sắp xếp, tải lại từ trang 1']],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn', ['- Mở / đóng khu vực ô lọc', '- Khi mở, nút đổi thành “Ẩn tìm kiếm nâng cao”']],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', '–', ['- Mở cửa sổ “Cài đặt bộ lọc”: tích ô lọc muốn hiện, kéo đổi thứ tự, Lưu / Khôi phục mặc định / Đóng; lưu theo từng màn hình (quy tắc chung)']],
        ['Ô Khách hàng đăng ký', 'Textbox', 'Enable', 'Chữ tự do', 'Không', 'Trống', ['- Placeholder “Nhập tên khách hàng”', '- Tìm gần đúng theo tên khách hàng (không gồm mã, người liên hệ)', '- Lọc khi bấm Tìm kiếm / Enter']],
        ['Ô Thời hạn đăng ký', 'Dropdown', 'Enable', 'Còn hạn / Hết hạn', 'Không', 'Trống (tất cả)', ['- Chọn 1, có nút × xóa', '- Còn hạn: Thời hạn đăng ký ≥ hôm nay; Hết hạn: < hôm nay (BR-03)', '- Lọc ngay khi chọn']],
        ['Ô Người đăng ký', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', ['- Chọn 1 nhân viên, gõ để tìm', '- Lọc đúng các đăng ký của nhân viên đó', '- Lọc ngay khi chọn']],
        ['Ô Số báo giá', 'Textbox', 'Enable', 'Chữ tự do', 'Không', 'Trống', ['- Placeholder “Nhập số báo giá”', '- Tìm gần đúng theo số báo giá thường hoặc báo giá hãng', '- Lọc khi bấm Tìm kiếm / Enter']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tìm kiếm / Enter', 'Click / Keydown', 'After:\n– Áp ô tìm nhanh và mọi ô lọc, tải lại từ trang 1, giữ sắp xếp.'],
        ['Chọn giá trị ô Thời hạn đăng ký / Người đăng ký', 'Change', 'After:\n– Tải lại ngay từ trang 1.'],
        ['Gõ ô tìm nhanh / Khách hàng đăng ký / Số báo giá', 'Change', 'After:\n– Chưa tải lại cho tới khi bấm Tìm kiếm / Enter.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xóa mọi điều kiện và sắp xếp (về Ngày đăng ký giảm dần), tải lại từ trang 1.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khu vực ô lọc.'],
        ['Rời màn hình', 'System', 'After:\n– Xóa bộ lọc đang dùng; lần mở sau các ô lọc về trống (BR-06).'],
    ],
})

# 2.3 Xuất Excel ------------------------------------------------------------------
FR.append({
    'ten': 'Xuất danh sách ra Excel', 'uc': 'uc_xuat',
    'qtc': 'Quy tắc Excel.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách ra Excel'],
        ['Mô tả', 'Xuất mọi dòng khớp bộ lọc đang áp (không chỉ trang đang xem) ra file Excel; người dùng chọn trường và thứ tự cột (BR-05).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng lọc danh sách (nếu cần), bấm Xuất Excel.\n2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn các trường ứng với cột đang hiện trên bảng (mặc định 6/7, không tích Người liên hệ).\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự rồi bấm Xuất file.\n4. Hệ thống tải file danh_sach_dang_ky_khach_hang.xlsx, báo “Xuất Excel thành công”.'],
        ['Dòng sự kiện phụ', '• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Lỗi → “Lỗi khi xuất Excel”.\n• Trong lúc xuất, nút Xuất Excel không bấm được để tránh bấm kép.'],
        ['Yêu cầu đặc biệt', 'Xuất toàn bộ khoảng 2.100 dòng mất khoảng 6–7 giây trên môi trường thử nghiệm (đo 18/11/2026).'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': POPUP % 'Chọn trường xuất file',
    'anh': [('08_export', 'Cửa sổ Chọn trường xuất file')],
    'ui': ui(UI8, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', '–', ['- “Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file.”']],
        ['Danh sách trường', 'Table/Grid', 'Enable', '7 trường', 'Không', 'Theo cột đang hiện', [
            '- Khách hàng đăng ký, Ngày đăng ký, Thời hạn đăng ký, Người đăng ký, Số báo giá, Ghi chú, Người liên hệ',
            '- Mỗi trường có ô tích và biểu tượng ☰ kéo đổi vị trí',
            '- Mặc định tích các trường ứng với cột đang hiện trên bảng; Người liên hệ là trường riêng của file, mặc định không tích']],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', ['- Tích / bỏ tích mọi trường']],
        ['Dòng đếm', 'Label', 'Hiển thị', '–', '–', 'Đang chọn 6/7 trường', ['- “Đang chọn x/7 trường”']],
        ['Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Enable', ['- Tải file', '- Không bấm được khi chưa chọn trường nào']],
        ['Nút Đóng / (x)', 'Button', 'Enable', '–', '–', '–', ['- Đóng cửa sổ, không xuất']],
        ['File Excel', 'Label', 'Hiển thị', '–', '–', '–', [
            '- Tên file danh_sach_dang_ky_khach_hang.xlsx',
            '- Tiêu đề “Danh sách đăng ký khách hàng toàn công ty”, hàng tên cột, cột STT luôn đứng đầu',
            '- Mỗi đăng ký 1 dòng, đúng thứ tự sắp xếp trên màn; Ngày đăng ký dạng dd/mm/yyyy HH:mm, Thời hạn đăng ký dạng dd/mm/yyyy',
            '- Người liên hệ là cột riêng (trên màn nằm ở dòng 2 cột Khách hàng đăng ký)',
            '- Cuối file có khối ký “(Ký, họ tên)”']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ, tích sẵn các trường theo cột đang hiện.'],
        ['Bấm Xuất file', 'Click', 'Before:\n– Có ít nhất 1 trường được chọn.\nDuring:\n– Lấy toàn bộ dòng theo bộ lọc và sắp xếp đang áp.\n– Lỗi → “Lỗi khi xuất Excel”, không thực hiện bước After.\nAfter:\n– Tải file theo trường / thứ tự đã chọn, đóng cửa sổ, báo “Xuất Excel thành công”.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ, không xuất.'],
    ],
})

# 2.4 Tùy chỉnh cột ---------------------------------------------------------------
FR.append({
    'ten': 'Tùy chỉnh cột hiển thị',
    'qtc': 'Tùy chỉnh cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tùy chỉnh cột hiển thị'],
        ['Mô tả', 'Ẩn / hiện và đổi thứ tự các cột của bảng; cấu hình lưu theo từng người dùng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Cấu hình cột hiển thị.\n2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột”.\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự rồi bấm Lưu.\n4. Hệ thống áp dụng lên bảng, lưu cấu hình, báo “Cập nhật thành công”.'],
        ['Dòng sự kiện phụ', '• STT và Khách hàng đăng ký là cột khóa: luôn hiện, không kéo đổi vị trí.\n• Bấm Đóng → bỏ thay đổi vừa chỉnh.\n• Lỗi lưu: “Thao tác thất bại”.\n• Cấu hình giữ nguyên khi tải lại trang, đăng nhập máy khác (lưu theo tài khoản).'],
    ],
    'menu_them': ' => Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': POPUP % 'Tuỳ chỉnh cột',
    'anh': [('09_colcfg', 'Cửa sổ Tuỳ chỉnh cột — STT, Khách hàng đăng ký bị khóa')],
    'ui': ui(UI8, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', '–', ['- “Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng.”']],
        ['Danh sách cột', 'Table/Grid', 'Enable', '7 cột', 'Không', 'Theo cấu hình đã lưu', ['- STT, Khách hàng đăng ký, Ngày đăng ký, Thời hạn đăng ký, Người đăng ký, Số báo giá, Ghi chú', '- Mặc định hiện tất cả', '- Kéo ☰ đổi thứ tự']],
        ['Cột khóa', 'Table/Grid', 'Disable', '–', '–', 'Luôn tích', ['- STT, Khách hàng đăng ký: ô tích xám kèm biểu tượng khóa']],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', ['- Tích / bỏ tích mọi cột (trừ cột khóa)']],
        ['Dòng đếm', 'Label', 'Hiển thị', '–', '–', 'Đang chọn 7/7 cột', ['- “Đang chọn x/7 cột”']],
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', ['- Áp dụng, lưu cấu hình cho người dùng; “Cập nhật thành công” (lỗi: “Thao tác thất bại”)']],
        ['Nút Đóng / (x)', 'Button', 'Enable', '–', '–', '–', ['- Đóng, bỏ thay đổi']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Cấu hình cột hiển thị', 'Click', 'After:\n– Mở cửa sổ theo cấu hình đang dùng.'],
        ['Tích / bỏ tích, kéo ☰', 'Change / Drag', 'After:\n– Đổi trong cửa sổ (chưa áp dụng).'],
        ['Bấm Lưu', 'Click', 'After:\n– Ẩn / hiện, sắp lại cột trên bảng; lưu theo người dùng; “Cập nhật thành công”. Không đổi bộ lọc, trang đang xem.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng, không áp dụng.'],
    ],
})

MA_TRAN_FR = ['FR-01 Xem danh sách đăng ký khách hàng', 'FR-02 Tìm kiếm và lọc', 'FR-03 Xuất danh sách ra Excel', 'FR-04 Tùy chỉnh cột hiển thị']

S = {
    'ten': TEN,
    'menu': [('CSKH trước bán', 'menu_phanhe'), ('Báo cáo', 'menu_nhom'), ('Báo cáo thị trường', 'menu_nhomcon'), (TEN, 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu màn hình.',
        'Phạm vi: xem, tìm kiếm / lọc, xuất Excel, tùy chỉnh cột danh sách đăng ký khách hàng của toàn công ty. Màn không thêm, sửa, xóa, hủy đăng ký.',
        'Mục đích sử dụng dữ liệu: quản lý kinh doanh biết khách hàng / người liên hệ nào đang được nhân viên nào giữ, còn hạn đến ngày nào, sinh từ báo giá nào — tránh hai nhân viên cùng chăm sóc một khách.',
        'Ràng buộc quan trọng: đăng ký còn hạn của người khác chặn việc chọn khách đó ở Meeting, Dự án TKT, Báo giá (Phần 5).',
    ],
    'thuat_ngu': [
        ['Đăng ký khách hàng', 'Việc nhân viên kinh doanh đăng ký giữ một khách hàng (khách cá nhân) hoặc một người liên hệ của khách tổ chức trong một thời hạn, sinh từ báo giá hãng.'],
        ['Thời hạn đăng ký', 'Ngày hết hạn giữ khách của lượt đăng ký.'],
        ['Còn hạn / Hết hạn', 'Còn hạn: Thời hạn đăng ký từ hôm nay trở đi. Hết hạn: Thời hạn đăng ký trước hôm nay. Màn không có cột trạng thái; chỉ lọc theo ô Thời hạn đăng ký.'],
        ['Người liên hệ', 'Người thuộc khách hàng tổ chức (doanh nghiệp, cơ quan…) mà nhân viên làm việc cùng.'],
        ['Báo giá hãng', 'Báo giá lập trên hệ thống ERP, nơi có nút “Đăng ký khách hàng”.'],
        ['CSKH', 'Chăm sóc khách hàng.'],
        ['ERP', 'Hệ thống quản lý bán hàng hiện hành, nơi lập báo giá hãng và đăng ký / hủy đăng ký khách hàng.'],
    ],
    'quyen_truoc': ['Màn hình CHỈ ĐỌC, gắn đúng 1 quyền. Có quyền là xem được mọi chức năng của màn (kể cả Xuất Excel); không có quyền thì mục menu bị ẩn và mở bằng đường dẫn bị từ chối.'],
    'quyen_rows': [[QUYEN, 'Thấy mục menu, mở màn, xem danh sách toàn công ty, tìm kiếm / lọc, xuất Excel, tùy chỉnh cột. Quyền thuộc nhóm Danh mục dùng chung => Khách hàng, không chia mức phạm vi.'],
                   ['Không có quyền', 'Không thấy mục menu; mở bằng đường dẫn → toast “Bạn không có quyền thực hiện chức năng này”, bảng không có dữ liệu.']],
    'ma_tran': [['Chức năng', QUYEN, 'Không có quyền']] + [[f, 'Có', 'Không'] for f in MA_TRAN_FR],
    'ma_tran_widths': [2.6, 2.2, 1.2],
    'quyen_sau': [
        'Có quyền là xem TOÀN công ty: mọi đăng ký của mọi công ty, phòng ban, nhân viên; không thu hẹp theo công ty đang làm việc hay phòng ban của người xem (BR-01).',
        'Xuất Excel không cần quyền riêng, theo đúng phạm vi đang xem.',
        'Mở Số báo giá: màn báo giá (HRM) / báo giá hãng (ERP) tự áp quyền xem của chính nó.',
    ],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Quyền và phạm vi', ['– Cần quyền “%s” để thấy menu và mở màn.' % QUYEN, '– Có quyền là xem toàn công ty, không chia mức phạm vi.'], ['Toàn màn']),
        ('BR-02', 'Dòng hiển thị', ['– Mỗi lượt đăng ký khách hàng 1 dòng, gồm cả còn hạn và hết hạn.', '– Đăng ký đã hủy bị xóa hẳn nên không hiện.', '– Mặc định xếp theo Ngày đăng ký giảm dần; cùng thời điểm thì đăng ký tạo sau đứng trước.'], ['Xem danh sách', 'Xuất Excel']),
        ('BR-03', 'Còn hạn / Hết hạn', ['– So Thời hạn đăng ký với NGÀY hôm nay (không so giờ).', '– Thời hạn đăng ký ≥ hôm nay: Còn hạn (kể cả hết hạn đúng hôm nay); < hôm nay: Hết hạn.'], ['Tìm kiếm và lọc', 'Màn dùng chung (Phần 5)']),
        ('BR-04', 'Tìm kiếm', ['– Ô tìm nhanh: chứa chuỗi trong tên / mã khách hàng, người liên hệ, họ tên người đăng ký, số báo giá; không phân biệt hoa thường, dấu; bỏ khoảng trắng đầu cuối.', '– Ô Khách hàng đăng ký chỉ theo tên khách hàng; ô Số báo giá theo số báo giá thường hoặc hãng.', '– Ô chữ lọc khi bấm Tìm kiếm / Enter; ô chọn lọc ngay.', '– Các điều kiện kết hợp theo “và”.'], ['Tìm kiếm và lọc']),
        ('BR-05', 'Xuất Excel', ['– Xuất mọi dòng khớp bộ lọc (mọi trang), đúng thứ tự sắp xếp.', '– Cột theo trường / thứ tự người dùng chọn; mặc định theo cột đang hiện trên bảng; STT luôn đứng đầu.'], ['Xuất Excel']),
        ('BR-06', 'Bộ lọc khi rời màn', ['– Rời màn, tải lại trang hoặc mở tab mới: bộ lọc và sắp xếp về mặc định.'], ['Tìm kiếm và lọc']),
        ('BR-07', 'Người đăng ký', ['– Hiển thị “Mã phòng ban - Họ tên” theo hồ sơ hiện tại của nhân viên; chưa có phòng ban thì chỉ họ tên.'], ['Xem danh sách', 'Xuất Excel']),
        ('BR-08', 'Liên kết Số báo giá', ['– Báo giá thường mở màn chi tiết báo giá HRM; báo giá hãng mở màn báo giá hãng ERP; đều ở tab mới.'], ['Xem danh sách']),
    ],
    'phan5': {
        'title': 'Phần 5. Bảng danh sách các màn hình liên quan dữ liệu báo cáo',
        'cau_dan': 'Màn hình chỉ đọc. Các màn dưới đây sinh ra dữ liệu đăng ký, được mở từ màn này, hoặc dùng chung dữ liệu đăng ký còn hạn để chặn chọn khách hàng.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người có quyền xem DS khách hàng đã đăng ký',
    'mains': [('FR-01', 'Xem danh sách đăng ký khách hàng', 'view'), ('FR-03', 'Xuất danh sách ra Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc', 'view'), ('FR-04', 'Tùy chỉnh cột hiển thị', 'view')],
    'rieng': [('FR-03', 'Xuất danh sách ra Excel', 'io', 'uc_xuat')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', R.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)

# -*- coding: utf-8 -*-
"""SRS - Khai báo đầu kỳ công nợ (STT 167) — MÀN MẪU nhóm PHIẾU đợt 3 (khuôn quốc gia, bám cấu trúc SRS màn 27).

Nguồn (code HRM develop, 02/11/2026):
  FE hrm-client/components/finance/declare-debt/{DeclareDebtList, DeclareDebtForm, DeclareDebtContractPicker,
     ContractCodeLink}.vue, utils/finance/declareDebtConfigs.js, pages/finance/declare-debt-beginnings/**,
     components/subsystem-menu/finance.js
  BE Modules/Finance: Services/DeclareDebt/{AbstractDeclareDebtService, DeclareDebtBeginningService,
     DeclareDebtPostingService, DeclareDebtContractRegistry}.php, Http/Controllers/V1/{AbstractDeclareDebtController,
     DeclareDebtBeginningController}.php, Http/Requests/DeclareDebt/DeclareDebtRequest.php,
     Entities/Contract/{DeclareDebtBeginning, Concerns/DeclareDebtCommon}.php; app/Services/CatalogHistoryService.php
  Ảnh: capture.js (dev-hrm). Phần 5: dò code FE/BE 02/11/2026.
Màn 168 (NCC) dùng CHUNG code: chép file này, đổi khối dữ liệu (ngoại tệ, 3 quyền riêng, không có Quá hạn / Ngày BGNT,
  popup có ô Phạm vi, tài khoản chỉ TK theo dõi công nợ).
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402
from _lib_phieu import ui, UI4, UI4W, UI6, UI6W, UI7, UI7W, UI8, UI8W, TRUOC_LUU  # noqa: E402

TEN = 'Khai báo đầu kỳ công nợ'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
QUYEN = 'Quản lý công nợ đầu kỳ'
Q = 'Người dùng có quyền thực hiện chức năng (quyền "%s")' % QUYEN
DK = '1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền "%s".' % QUYEN
DK_CHUA = DK + '\n3. Khai báo ở trạng thái Chưa phát sinh chứng từ và thuộc phạm vi dữ liệu của người dùng.'
HOAC = ('Hoặc Menu: Phân hệ Tài chính => Kế toán công nợ => Khách hàng => Công nợ đầu kỳ theo khách hàng - hợp đồng '
        '(cùng màn hình).')
TRANG = 'Trang %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'
POPUP = 'Modal %s được mở ngay trên màn hình %s theo đường dẫn ở trên.'

# ------------------------------------------------------------------ Phần 5 (dò code 02/11/2026)
P5 = [
    ('Tài chính', 'Phiếu thu (thu dư nợ đầu kỳ: gắn chứng từ vào khai báo, khai báo chuyển Đã phát sinh)',
     'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu chi (chi trả dư có đầu kỳ)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu báo có (thu dư nợ đầu kỳ qua ngân hàng)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Đề nghị thu tiền (duyệt đề nghị sinh phiếu thu trừ vào khai báo đầu kỳ)',
     'Tài chính => Khởi tạo => Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi'),
    ('Tài chính', 'Phiếu kế toán (bù trừ / điều chỉnh công nợ đầu kỳ)', 'Tài chính => Sổ tổng hợp => Sổ tổng hợp'),
    ('Tài chính', 'Danh mục tài khoản (tài khoản đã dùng trong khai báo không xóa được)', 'Tài chính => Danh mục'),
    ('Tài chính', 'Khai Quy chế – Cấu hình (khóa "Ngày khai báo đầu kỳ" khi công ty đã có khai báo)',
     'Tài chính => Khai Quy chế – Cấu hình'),
    ('Bán hàng', 'Đối chiếu công nợ 1 KH (số dư đầu kỳ, link mở chi tiết khai báo)', 'Bán hàng => Báo cáo => Báo cáo công nợ'),
    ('Bán hàng', 'Tổng hợp công nợ theo NV (số dư đầu kỳ, Quá hạn / Ngày BGNT)', 'Bán hàng => Báo cáo => Báo cáo công nợ'),
    ('Bán hàng', 'Chi tiết công nợ KH (số dư đầu kỳ, link mở chi tiết khai báo)', 'Bán hàng => Báo cáo => Báo cáo công nợ'),
]

FR = []

# 2.1 Xem danh sách -------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách khai báo đầu kỳ công nợ',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách khai báo đầu kỳ công nợ'],
        ['Mô tả', 'Hiển thị các khai báo công nợ đầu kỳ (mỗi dòng = 1 hợp đồng × 1 tài khoản của 1 khách hàng) trong phạm vi dữ liệu của người dùng, có phân trang, sắp xếp và nút thao tác theo từng dòng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), khai báo tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Không có khai báo khớp → bảng hiện "Không có dữ liệu phù hợp bộ lọc."\n• Phạm vi dữ liệu theo quyền xem (Phần 2, BR-02).\n• Khai báo Đã phát sinh chứng từ chỉ còn nút Lịch sử (BR-05).'],
    ],
    'hoac_menu': [HOAC],
    'anh': [('01_list', 'Màn danh sách Khai báo đầu kỳ công nợ lúc mới truy cập'),
            ('01b_list_actions', 'Cột Hành động: dòng Chưa phát sinh có Sửa, Xóa, Lịch sử; dòng Đã phát sinh chỉ có Lịch sử')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Khai báo đầu kỳ công nợ', 'Tiêu đề khối danh sách và tiêu đề trang.'],
        ['Nút Tạo mới', 'Button', 'Enable / Ẩn', 'Hiển thị', 'Mở trang "Thêm khai báo đầu kỳ công nợ" (mục 2.4).'],
        ['Nút Import Excel', 'Button', 'Enable / Ẩn', 'Hiển thị', 'Mở cửa sổ "Import khai báo đầu kỳ công nợ" (mục 2.11).'],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất file" (mục 2.10). Trong lúc xuất, cạnh nút hiện dòng tiến độ.'],
        ['Nút In danh sách', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ xem trước bản in danh sách (mục 2.9).'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.3).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa, không ẩn được.'],
        ['Cột Mã phiếu', 'Table/Grid', 'Read-only', 'Hiển thị', '- Dạng <mã công ty>.CNĐKHĐ.<5 chữ số> (BR-03).\n- Sắp xếp được. Chữ dạng liên kết: bấm mở trang Chi tiết (mục 2.7), chuột phải mở tab mới được.\n- Cột khóa, không ẩn được.'],
        ['Cột Khách hàng', 'Table/Grid', 'Read-only', 'Hiển thị', '"Mã - Tên khách hàng".'],
        ['Cột Tài khoản', 'Table/Grid', 'Read-only', 'Ẩn', '"Số hiệu - Tên tài khoản". Mặc định ẩn, bật ở Tuỳ chỉnh cột.'],
        ['Cột Loại hợp đồng', 'Table/Grid', 'Read-only', 'Ẩn', 'Loại của hợp đồng gắn với khai báo. Mặc định ẩn.'],
        ['Cột Số hợp đồng', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng liên kết: mở chứng từ hợp đồng ở tab mới (hợp đồng chưa có trang xem thì là chữ thường).'],
        ['Cột Dư nợ', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số tiền khi Loại dư = Dư nợ; dòng Dư có để trống. Định dạng 1,234,567.89, căn phải.'],
        ['Cột Dư có', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số tiền khi Loại dư = Dư có; dòng Dư nợ để trống.'],
        ['Cột Quá hạn', 'Table/Grid', 'Read-only', 'Hiển thị', '"Có" / "Không".'],
        ['Cột Ngày BGNT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Ngày bàn giao nghiệm thu dd/mm/yyyy; khai báo không quá hạn để trống.'],
        ['Cột Người cập nhật', 'Table/Grid', 'Read-only', 'Ẩn', '"Họ tên - Mã phòng ban". Mặc định ẩn.'],
        ['Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'Ẩn', 'dd/mm/yyyy hh:mm. Sắp xếp được. Mặc định ẩn.'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', '"Họ tên - Mã phòng ban".'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sửa, Xóa: chỉ hiện khi khai báo Chưa phát sinh chứng từ (BR-05).\n- Lịch sử: luôn có.\n- Nút không dùng được thì ẩn, không làm mờ. Cột khóa, không ẩn được.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Kiểm tra quyền "%s"; thiếu quyền → 2 mục menu không hiện, mở thẳng màn thì chuyển trang "Không tìm thấy".\nAfter:\n– Tải trang 1 theo phạm vi dữ liệu (BR-02), khai báo tạo gần nhất trên cùng; khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút).' % QUYEN],
        ['Bấm tiêu đề cột Mã phiếu / Ngày tạo / Ngày cập nhật', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại dữ liệu.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp, tải lại dữ liệu; đổi số dòng thì quay về trang 1.'],
        ['Bấm Mã phiếu', 'Click', 'After:\n– Mở trang Chi tiết khai báo (mục 2.7).'],
        ['Bấm Số hợp đồng', 'Click', 'After:\n– Mở chứng từ hợp đồng ở tab mới.'],
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc danh sách',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách khai báo'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô gõ chữ (tìm nhanh, Mã hợp đồng, Số tiền) chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Bấm Làm mới → xoá mọi điều kiện và tải lại danh sách.\n• Ô Công ty / Phòng ban / Bộ phận chỉ hiện theo phạm vi xem của người dùng (BR-02).\n• Hệ thống ghi nhớ bộ lọc 10 phút khi rời màn rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực Tìm kiếm nâng cao ở trạng thái mở')],
    'ui': ui(UI7, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', '- Placeholder "Tìm theo mã phiếu, số hợp đồng, mã hoặc tên khách hàng".\n- Tìm gần đúng theo Mã phiếu, Số hợp đồng (mọi loại hợp đồng), mã / tên khách hàng.'],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Áp dụng từ khóa và các ô lọc.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá mọi điều kiện lọc và tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực ô lọc (khi mở, nút đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" (mục 2.3).'],
        ['Ô Khách hàng', 'Dropdown', 'Enable', 'Gõ ≥ 2 ký tự để tìm', 'Trống', 'Tìm khách hàng theo mã, tên, số điện thoại; hiển thị "Mã - Tên". Tải lại trang vẫn giữ tên đã chọn.'],
        ['Ô Tài khoản', 'Dropdown', 'Enable', 'Tài khoản chi tiết đang hoạt động', 'Trống', 'Lọc theo tài khoản của khai báo.'],
        ['Ô Loại hợp đồng', 'Dropdown', 'Enable', '10 loại hợp đồng', 'Trống', 'Hợp đồng bán, Hợp đồng hãng / dự án, Hợp đồng gói dịch vụ, Hợp đồng dự án, Hợp đồng đầu kỳ, Hợp đồng mua nước ngoài, Hợp đồng mua ngoài, Hợp đồng mua trong nước (2 dòng), Hợp đồng dịch vụ BH - SC.'],
        ['Ô Mã hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Tìm gần đúng số hợp đồng; lọc khi Enter / Tìm kiếm.'],
        ['Ô Loại dư', 'Dropdown', 'Enable', 'Dư nợ / Dư có', 'Trống', 'Bỏ trống thì hiện cả hai.'],
        ['Ô Số tiền', 'Textbox', 'Enable', 'Từ → Đến, số ≥ 0', 'Trống', 'Lọc theo số tiền công nợ, tính cả 2 đầu mút.'],
        ['Ô Quá hạn', 'Dropdown', 'Enable', 'Có / Không', 'Trống', 'Lọc khai báo có / không đánh dấu quá hạn.'],
        ['Ô Ngày BGNT', 'Datepicker', 'Enable', 'dd/mm/yyyy, Từ → Đến', 'Trống', 'Lọc theo ngày bàn giao nghiệm thu.'],
        ['Ô Người tạo / Người cập nhật', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc khai báo do người được chọn tạo / cập nhật lần cuối.'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy, Từ → Đến', 'Trống', 'Lọc theo ngày tạo khai báo, tính cả 2 đầu mút.'],
        ['Ô Công ty – Phòng ban – Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Theo phạm vi xem', 'Trống', '- Công ty: chỉ khi có quyền xem tất cả.\n- Phòng ban, Bộ phận: chọn cấp trên trước thì cấp dưới mới mở.\n- Lọc theo tổ chức của khai báo (= tổ chức của người lập hợp đồng, BR-04).'],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm Tìm kiếm / nhấn Enter ở ô gõ chữ', 'Click', 'After:\n– Áp đồng thời từ khóa và các ô lọc, tải lại bảng từ trang 1.'],
        ['Chọn giá trị ở ô chọn', 'Change', 'After:\n– Tải lại bảng từ trang 1 ngay.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khu vực ô lọc.'],
    ],
})

# 2.3 Cài đặt bộ lọc / tùy chỉnh cột --------------------------------------------
FR.append({
    'ten': 'Cài đặt bộ lọc và tuỳ chỉnh cột',
    'qtc': 'Bộ lọc, Cấu hình cột và lưu cấu hình theo người dùng.',
    'gioi_thieu': [
        ['Tên chức năng', 'Cài đặt bộ lọc và tuỳ chỉnh cột'],
        ['Mô tả', 'Người dùng chọn ô lọc nào hiển thị / thứ tự ô lọc, và cột nào hiển thị / thứ tự cột trên bảng. Cấu hình lưu theo từng người dùng, từng màn.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Bấm "Cài đặt bộ lọc" (hoặc biểu tượng Cấu hình cột hiển thị).\n2. Tích / bỏ tích, kéo ☰ để đổi thứ tự.\n3. Bấm Lưu: hệ thống lưu cấu hình và áp dụng ngay.'],
        ['Dòng sự kiện phụ', '• Bấm Đóng: bỏ thay đổi.\n• Cài đặt bộ lọc có nút "Khôi phục mặc định".\n• Cột STT, Mã phiếu không bỏ được (có biểu tượng khóa).'],
    ],
    'menu_them': ' => Cài đặt bộ lọc {icon:btn_caidatboloc} / Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': 'Modal Cài đặt bộ lọc và Modal Tuỳ chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('26_filtercfg', 'Cửa sổ Cài đặt bộ lọc'), ('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột')],
    'ui': ui(UI6, [
        ['Danh sách ô lọc', 'Checkbox', 'Enable', 'Đủ 12 ô', 'Tích ô lọc muốn hiện, kéo ☰ đổi thứ tự.'],
        ['Nút Khôi phục mặc định', 'Button', 'Enable', '–', 'Đưa cấu hình ô lọc về mặc định.'],
        ['Danh sách cột', 'Checkbox', 'Enable', '11/15 cột', 'Tích cột muốn hiện; STT, Mã phiếu bị khóa. Kéo ☰ đổi thứ tự.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Chọn / bỏ nhanh mọi cột (trừ cột khóa).'],
        ['Nút Lưu', 'Button', 'Enable', '–', 'Lưu cấu hình theo người dùng, áp dụng ngay.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ, không lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình theo người dùng, đóng cửa sổ, bảng / khu vực lọc vẽ lại theo cấu hình.'],
        ['Kéo ☰', 'Drag', 'After:\n– Đổi thứ tự dòng trong cửa sổ.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ, không lưu.'],
    ],
})

# 2.4 Lập khai báo --------------------------------------------------------------
FR.append({
    'ten': 'Lập khai báo đầu kỳ công nợ', 'uc': 'uc_them', 'uc_ten': 'FR-04 Lập khai báo đầu kỳ công nợ',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Lập khai báo đầu kỳ công nợ'],
        ['Mô tả', 'Chọn 1 khách hàng rồi chọn một hoặc nhiều hợp đồng của khách hàng đó; mỗi dòng hợp đồng nhập Tài khoản, Loại dư, Công nợ (Quá hạn, Ngày BGNT nếu có). Lưu xong mỗi dòng thành 1 khai báo riêng (1 mã phiếu, 1 bút toán sổ chi tiết) và có hiệu lực ngay, không qua duyệt.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở trang "Thêm khai báo đầu kỳ công nợ"; góc phải khối Thông tin chung hiện "<Người đăng nhập> - <ngày giờ hiện tại>".\n3. Người dùng chọn Khách hàng, bấm "Chọn hợp đồng" và chọn hợp đồng (mục 2.5).\n4. Mỗi dòng nhập Tài khoản, Loại dư, Công nợ; dòng Dư nợ quá hạn thì tích Quá hạn và chọn Ngày BGNT.\n5. Bấm Lưu.\n6. Hệ thống kiểm tra dữ liệu, sinh mã phiếu cho từng dòng (BR-03), ghi khai báo với tổ chức = của người lập hợp đồng (BR-04), ghi 1 bút toán sổ chi tiết cho mỗi dòng (BR-06).\n7. Ghi nhận Tạo mới trong lịch sử của từng khai báo.\n8. Báo "Thêm mới thành công.", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Bấm "Lưu và tiếp tục": lưu như trên rồi mở lại trang Thêm trống để lập tiếp.\n• Thiếu / sai dữ liệu → báo đỏ dưới ô của đúng dòng + toast "Bạn chưa nhập đầy đủ thông tin.", cuộn tới ô lỗi đầu tiên, không lưu dòng nào.\n• Trùng khai báo đã có (cùng khách hàng + hợp đồng + tài khoản) → dưới ô Tài khoản "Đã khai báo đầu kỳ cho tài khoản này" (BR-07).\n• Đổi Khách hàng → bảng hợp đồng bị xoá trắng.\n• Bấm nút xoá ở cuối dòng → bỏ dòng khỏi bảng.\n• Bấm Quay lại: chưa nhập gì thì về danh sách; đã nhập thì hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', 'Nút Lưu bị khóa ngay khi bấm cho tới khi có kết quả, tránh lưu 2 lần.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': TRANG % '"Thêm khai báo đầu kỳ công nợ"',
    'anh': [('10_create', 'Trang Thêm khai báo đầu kỳ công nợ lúc mới mở'),
            ('11_no_customer', 'Bấm "Chọn hợp đồng" khi chưa chọn khách hàng'),
            ('10b_create_filled', 'Trang Thêm đã chọn 2 hợp đồng và nhập thông tin từng dòng'),
            ('18_unsaved', 'Hộp xác nhận Thông tin chưa lưu khi bấm Quay lại')],
    'ui': ui(UI8, [
        ['Người tạo - ngày giờ', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại', 'Góc phải khối Thông tin chung.'],
        ['Khách hàng', 'Dropdown', 'Enable', 'Khách hàng trong hệ thống, gõ ≥ 2 ký tự', 'Có', 'Trống', '- Placeholder "Nhập mã/tên khách hàng"; tìm theo mã, tên, số điện thoại.\n- Bỏ trống mà bấm "Chọn hợp đồng": "Chọn khách hàng trước khi chọn hợp đồng".'],
        ['Nút Chọn hợp đồng', 'Button', 'Enable', '–', '–', '–', 'Mở cửa sổ chọn hợp đồng của khách hàng (mục 2.5).'],
        ['Bảng hợp đồng', 'Table/Grid', 'Enable', '≥ 1 dòng', 'Có', 'Trống', '- Trống: "Chưa chọn hợp đồng nào — bấm "Chọn hợp đồng" để thêm."\n- Lưu khi chưa có dòng nào: "Phải chọn ít nhất 1 hợp đồng".'],
        ['Cột Loại hợp đồng, Số hợp đồng', 'Table/Grid', 'Read-only', '–', '–', 'Theo hợp đồng đã chọn', 'Số hợp đồng là liên kết mở chứng từ hợp đồng ở tab mới.'],
        ['Tài khoản', 'Dropdown', 'Enable', 'Tài khoản chi tiết đang hoạt động', 'Có', 'Theo dòng phía trên (dòng đầu: trống)', '"Số hiệu - Tên"; bỏ trống: "Bắt buộc phải nhập"; tài khoản không hợp lệ: "Tài khoản không hợp lệ".'],
        ['Loại dư', 'Dropdown', 'Enable', 'Dư nợ / Dư có', 'Có', 'Dư nợ', 'Đổi sang Dư có thì tự bỏ tích Quá hạn và xoá Ngày BGNT.'],
        ['Công nợ', 'Textbox', 'Enable', 'Số > 0, tối đa 2 chữ số thập phân', 'Có', 'Trống', 'Bỏ trống: "Bắt buộc phải nhập"; ≤ 0: "Phải lớn hơn 0". Hiển thị 1,234,567.89.'],
        ['Quá hạn', 'Checkbox', 'Enable / Disable', 'Có / Không', 'Không', 'Không tích', 'Chỉ tích được khi Loại dư = Dư nợ (BR-08).'],
        ['Ngày BGNT', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy, ≤ hôm nay', 'Có khi Quá hạn', 'Trống', '- Chỉ hiện khi tích Quá hạn; ngày sau hôm nay không chọn được.\n- Bỏ trống: "Bắt buộc phải nhập".'],
        ['Nút xoá dòng', 'Button', 'Enable', '–', '–', '–', 'Bỏ dòng khỏi bảng (lỗi của các dòng còn lại giữ đúng dòng).'],
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi về danh sách.'],
        ['Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi mở lại trang Thêm trống.'],
        ['Nút Quay lại', 'Button', 'Enable', '–', '–', '–', 'Về danh sách (đã nhập thì hỏi "Thông tin chưa lưu").'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'Before:\n– Kiểm tra quyền "%s" (thiếu quyền thì nút ẩn; mở thẳng trang Thêm thì chuyển trang "Không tìm thấy").\nAfter:\n– Mở trang Thêm trống.' % QUYEN],
        ['Chọn Khách hàng', 'Change', 'After:\n– Bỏ lỗi dưới ô; nếu bảng đã có hợp đồng thì xoá trắng bảng.'],
        ['Đổi Loại dư / bỏ tích Quá hạn', 'Change', 'After:\n– Loại dư = Dư có hoặc bỏ tích Quá hạn: xoá Ngày BGNT của dòng.'],
        ['Bấm Lưu / Lưu và tiếp tục', 'Click', 'Before:\n– Kiểm tra quyền "%s".\nDuring:\n– Có ít nhất 1 dòng; mỗi dòng: Tài khoản thuộc danh sách chọn được, Loại dư hợp lệ, Công nợ > 0, dòng Quá hạn có Ngày BGNT ≤ hôm nay; hợp đồng tồn tại và thuộc đúng khách hàng; không trùng dòng khác trên form và không trùng khai báo đã có (BR-07).\n' % QUYEN + TRUOC_LUU + '\nAfter:\n– Mỗi dòng: sinh mã phiếu, ghi khai báo (Ngày tính công nợ = Ngày khai báo đầu kỳ cấu hình của công ty), ghi 1 bút toán sổ chi tiết.\n– Ghi nhận Tạo mới trong lịch sử.\n– Báo "Thêm mới thành công."; Lưu → về danh sách, Lưu và tiếp tục → trang Thêm trống.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa nhập gì → về danh sách.\n– Đã nhập → hộp "Thông tin chưa lưu" ("Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"): Thoát thì về danh sách không lưu, Ở lại thì quay về form.'],
    ],
})

# 2.5 Chọn hợp đồng ------------------------------------------------------------
FR.append({
    'ten': 'Chọn hợp đồng', 'uc': 'uc_chonhd', 'uc_ten': 'FR-05 Chọn hợp đồng của khách hàng',
    'qtc': 'Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chọn hợp đồng / đơn hàng của khách hàng'],
        ['Mô tả', 'Cửa sổ liệt kê hợp đồng thuộc khách hàng đang chọn từ các nguồn: hợp đồng bán (Hợp đồng, Đơn hàng, Hợp đồng nguyên tắc, Phụ lục…), hợp đồng hãng, hợp đồng gói dịch vụ, hợp đồng dự án, hợp đồng đầu kỳ, hợp đồng mua (BR-09). Bấm vào dòng là thêm ngay vào form, cửa sổ vẫn mở để chọn tiếp.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở trang Thêm và đã chọn Khách hàng.'],
        ['Dòng sự kiện chính', '1. Bấm "Chọn hợp đồng".\n2. Hệ thống mở cửa sổ "Chọn hợp đồng / đơn hàng", dòng phụ ghi "Khách hàng: <mã - tên>", tải trang 1 (10 dòng, mới nhất trên cùng).\n3. Người dùng lọc (nếu cần) và bấm vào dòng hợp đồng.\n4. Hệ thống thêm 1 dòng vào bảng form, báo "Đã thêm hợp đồng <số hợp đồng>", dòng trong cửa sổ chuyển "Đã chọn".\n5. Bấm Đóng để về form.'],
        ['Dòng sự kiện phụ', '• Hợp đồng đã có khai báo của khách hàng này: dòng mờ, Tình trạng "Đã khai báo", bấm không có tác dụng.\n• Hợp đồng đã có trên form: Tình trạng "Đã chọn", bấm lại không thêm trùng.\n• Không có hợp đồng phù hợp: "Không có dữ liệu phù hợp."'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi} => Chọn hợp đồng {icon:btn_chonhd}',
    'ghi_chu_layout': POPUP % ('Chọn hợp đồng / đơn hàng', 'Thêm khai báo'),
    'anh': [('14_picker', 'Cửa sổ Chọn hợp đồng / đơn hàng của một khách hàng')],
    'ui': ui(UI8, [
        ['Ô Loại hợp đồng', 'Dropdown', 'Enable', '14 lựa chọn', 'Không', 'Trống', 'Hợp đồng hãng, Hợp đồng, Đơn hàng, Hợp đồng nguyên tắc, Hợp đồng thúc đẩy bán, Đơn hàng thúc đẩy bán, Phụ lục bổ sung, Phụ lục HĐNT, Hợp đồng gói dịch vụ, Hợp đồng dự án, Hợp đồng đầu kỳ, Hợp đồng mua nước ngoài, Hợp đồng mua ngoài, Hợp đồng mua trong nước. Trống = mọi nguồn. Chọn là lọc ngay.'],
        ['Ô Số hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Tìm gần đúng; lọc khi Enter / Tìm kiếm.'],
        ['Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', '–', 'Áp dụng / xoá điều kiện lọc.'],
        ['Cột STT, Loại hợp đồng, Số hợp đồng', 'Table/Grid', 'Read-only', '–', '–', '–', 'Thông tin hợp đồng.'],
        ['Cột Tổng thanh toán', 'Table/Grid', 'Read-only', '–', '–', '–', 'Giá trị hợp đồng; hợp đồng đầu kỳ để trống.'],
        ['Cột Người tạo, Ngày tạo', 'Table/Grid', 'Read-only', '–', '–', '–', '"Họ tên - Mã phòng ban", dd/mm/yyyy.'],
        ['Cột Tình trạng', 'Table/Grid', 'Read-only', 'Đã khai báo / Đã chọn / trống', '–', '–', 'Dòng "Đã khai báo", "Đã chọn" không chọn được.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', '–', '10', '"Hiển thị a–b / N", chọn số dòng/trang.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ, giữ các hợp đồng đã chọn trên form.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Mở cửa sổ', 'System', 'Before:\n– Kiểm tra quyền "%s".\nAfter:\n– Tải hợp đồng của khách hàng từ mọi nguồn, đánh dấu Đã khai báo / Đã chọn.' % QUYEN],
        ['Bấm vào dòng hợp đồng', 'Click', 'During:\n– Dòng Đã khai báo / Đã chọn: bỏ qua.\nAfter:\n– Thêm dòng vào bảng form: Loại dư = Dư nợ, Tài khoản lấy theo dòng phía trên; báo "Đã thêm hợp đồng <số>".'],
        ['Chọn Loại hợp đồng / bấm Tìm kiếm', 'Click', 'After:\n– Tải lại từ trang 1 theo điều kiện.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.6 Sửa -----------------------------------------------------------------------
FR.append({
    'ten': 'Sửa khai báo', 'uc': 'uc_sua', 'uc_ten': 'FR-06 Sửa khai báo đầu kỳ công nợ',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Sửa khai báo đầu kỳ công nợ'],
        ['Mô tả', 'Sửa 1 khai báo Chưa phát sinh chứng từ: chỉ đổi được Tài khoản, Loại dư, Công nợ, Quá hạn, Ngày BGNT. Khách hàng và hợp đồng cố định.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_CHUA],
        ['Dòng sự kiện chính', '1. Bấm Sửa ở cột Hành động (hoặc nút Sửa ở trang Chi tiết).\n2. Hệ thống mở trang "Sửa khai báo đầu kỳ công nợ" với đúng 1 dòng, ô Mã phiếu và Khách hàng bị khóa.\n3. Người dùng sửa và bấm Lưu.\n4. Hệ thống kiểm tra, ghi thay đổi và cập nhật bút toán sổ chi tiết tương ứng (tài khoản, Nợ/Có, số tiền).\n5. Ghi nhận Thay đổi thông tin trong lịch sử.\n6. Báo "Cập nhật thành công.", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Đổi sang tài khoản đã khai báo cho cùng khách hàng + hợp đồng → "Đã khai báo đầu kỳ cho tài khoản này".\n• Mở thẳng trang Sửa của khai báo Đã phát sinh (hoặc không có quyền) → toast "Khai báo đã phát sinh chứng từ hoặc bạn không có quyền sửa." rồi chuyển sang trang Chi tiết.\n• Khai báo vừa phát sinh chứng từ khi đang sửa → bấm Lưu báo "Khai báo đã phát sinh chứng từ, không được sửa / xóa.", không lưu.\n• Bấm Quay lại khi đã sửa → hỏi "Thông tin chưa lưu".'],
    ],
    'menu_them': ' => Sửa {icon:btn_sua}',
    'ghi_chu_layout': TRANG % '"Sửa khai báo đầu kỳ công nợ"',
    'anh': [('12_edit', 'Trang Sửa khai báo đầu kỳ công nợ')],
    'ui': ui(UI8, [
        ['Mã phiếu', 'Textbox', 'Read-only', '–', '–', 'Mã hiện tại', 'Không sửa được.'],
        ['Khách hàng', 'Dropdown', 'Read-only', '–', '–', 'Khách hàng hiện tại', 'Không sửa được.'],
        ['Tài khoản', 'Dropdown', 'Enable', 'Tài khoản chi tiết đang hoạt động', 'Có', 'Dữ liệu hiện tại', 'Tài khoản cũ nay đã khóa vẫn hiện kèm biểu tượng khóa.'],
        ['Loại dư', 'Dropdown', 'Enable', 'Dư nợ / Dư có', 'Có', 'Dữ liệu hiện tại', 'Như trang Thêm.'],
        ['Công nợ', 'Textbox', 'Enable', 'Số > 0', 'Có', 'Dữ liệu hiện tại', 'Như trang Thêm.'],
        ['Quá hạn, Ngày BGNT', 'Checkbox / Datepicker', 'Enable', 'Như trang Thêm', 'Có khi Quá hạn', 'Dữ liệu hiện tại', 'Như trang Thêm (BR-08).'],
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi về danh sách. Trang Sửa không có "Lưu và tiếp tục", không có nút "Chọn hợp đồng" / xoá dòng.'],
        ['Nút Quay lại', 'Button', 'Enable', '–', '–', '–', 'Về danh sách (đã sửa thì hỏi "Thông tin chưa lưu").'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện khi khai báo Chưa phát sinh và người dùng có quyền.\nAfter:\n– Tải khai báo; ngoài phạm vi / không còn → trang "Không tìm thấy".'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền; khai báo phải Chưa phát sinh chứng từ (kiểm trước cả kiểm dữ liệu).\nDuring:\n– Kiểm như trang Thêm (bỏ qua trùng với chính khai báo).\n' + TRUOC_LUU + '\nAfter:\n– Ghi thay đổi, cập nhật bút toán sổ chi tiết.\n– Ghi nhận Thay đổi thông tin (giá trị cũ → mới) trong lịch sử.\n– Báo "Cập nhật thành công.", về danh sách.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa đổi gì → về danh sách; đã đổi → hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
    ],
})

# 2.7 Xem chi tiết --------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết khai báo', 'uc': 'uc_xem', 'uc_ten': 'FR-07 Xem chi tiết khai báo đầu kỳ công nợ',
    'qtc': 'Màn Xem chi tiết và Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết khai báo đầu kỳ công nợ'],
        ['Mô tả', 'Xem toàn bộ thông tin 1 khai báo ở chế độ chỉ đọc, kèm khối Lịch sử; nút thao tác ở chân trang khớp với nút ở dòng danh sách.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Khai báo thuộc phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Bấm Mã phiếu ở danh sách.\n2. Hệ thống mở trang "Chi tiết khai báo đầu kỳ công nợ: <mã phiếu>": khối Thông tin chung (Mã phiếu, Khách hàng, góc phải "<Người tạo> - <ngày giờ tạo>"), khối Danh sách hợp đồng (1 dòng), khối Lịch sử (thu gọn).'],
        ['Dòng sự kiện phụ', '• Khai báo Chưa phát sinh: chân trang có Sửa, Xóa, Quay lại.\n• Khai báo Đã phát sinh: chỉ có Quay lại.\n• Khai báo ngoài phạm vi / không tồn tại: chuyển trang "Không tìm thấy".'],
    ],
    'menu_them': ' => Mã phiếu (liên kết)',
    'anh': [('17_detail', 'Trang Chi tiết khai báo Chưa phát sinh chứng từ'),
            ('17c_detail_used', 'Trang Chi tiết khai báo Đã phát sinh chứng từ: chỉ còn nút Quay lại')],
    'ui': ui(UI6, [
        ['Mã phiếu, Khách hàng', 'Textbox / Dropdown', 'Read-only', 'Dữ liệu khai báo', 'Chỉ đọc.'],
        ['Người tạo - ngày giờ', 'Label', 'Read-only', 'Dữ liệu khai báo', 'Góc phải khối Thông tin chung.'],
        ['Bảng hợp đồng', 'Table/Grid', 'Read-only', '1 dòng', 'Loại hợp đồng, Số hợp đồng (liên kết), Tài khoản, Loại dư, Công nợ, Quá hạn, Ngày BGNT — các ô khóa.'],
        ['Khối Lịch sử', 'Label', 'Enable', 'Thu gọn', 'Bấm "Xem lịch sử" để mở (mục 2.12).'],
        ['Nút Sửa', 'Button', 'Enable / Ẩn', 'Theo trạng thái', 'Chỉ hiện khi Chưa phát sinh và có quyền; mở trang Sửa.'],
        ['Nút Xóa', 'Button', 'Enable / Ẩn', 'Theo trạng thái', 'Chỉ hiện khi Chưa phát sinh và có quyền (mục 2.8).'],
        ['Nút Quay lại', 'Button', 'Enable', '–', 'Về danh sách.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở trang', 'System', 'Before:\n– Kiểm tra quyền + phạm vi dữ liệu.\nAfter:\n– Hiển thị khai báo, tính nút Sửa / Xóa theo trạng thái phát sinh.'],
        ['Bấm Sửa / Xóa / Quay lại', 'Click', 'After:\n– Mở trang Sửa / hộp Xác nhận xóa / về danh sách.'],
    ],
})

# 2.8 Xóa -----------------------------------------------------------------------
FR.append({
    'ten': 'Xóa khai báo', 'uc': 'uc_xoa', 'uc_ten': 'FR-08 Xóa khai báo đầu kỳ công nợ',
    'qtc': 'Quy tắc xóa và Thông báo.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xóa khai báo đầu kỳ công nợ'],
        ['Mô tả', 'Xóa hẳn 1 khai báo Chưa phát sinh chứng từ cùng bút toán sổ chi tiết của nó.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_CHUA],
        ['Dòng sự kiện chính', '1. Bấm Xóa ở cột Hành động (hoặc nút Xóa ở trang Chi tiết).\n2. Hệ thống hiện hộp "Xác nhận xóa": "Bạn có chắc muốn xóa bản ghi này không?"\n3. Bấm Xóa.\n4. Hệ thống ghi nhận Xóa trong lịch sử, xóa bút toán sổ chi tiết và xóa khai báo.\n5. Báo "Xóa thành công.", tải lại danh sách (từ trang Chi tiết: về danh sách).'],
        ['Dòng sự kiện phụ', '• Bấm Hủy / (x) → đóng hộp, không thay đổi.\n• Khai báo vừa phát sinh chứng từ → "Khai báo đã phát sinh chứng từ, không được sửa / xóa.", không xóa.\n• Khai báo vừa bị người khác xóa → trang "Không tìm thấy" / báo lỗi.'],
    ],
    'menu_them': ' => Xóa {icon:btn_xoa}',
    'ghi_chu_layout': 'Modal Xác nhận xóa được mở ngay trên màn hình danh sách (nút Xóa trên dòng) hoặc màn hình chi tiết khai báo (nút Xóa) theo đường dẫn ở trên.',
    'anh': [('13_delete', 'Hộp Xác nhận xóa khai báo')],
    'ui': ui(UI4, [
        ['Nút Xóa (cột Hành động / chân trang Chi tiết)', 'Button', 'Biểu tượng thùng rác; chỉ hiện khi khai báo Chưa phát sinh và có quyền.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận xóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn xóa bản ghi này không?"'],
        ['Nút Xóa', 'Button', 'Xác nhận xóa.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không xóa.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Xóa', 'Click', 'After:\n– Hiện hộp Xác nhận xóa.'],
        ['Bấm Xóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền, phạm vi; khai báo phải Chưa phát sinh chứng từ.\nDuring:\n' + TRUOC_LUU + '\nAfter:\n– Ghi nhận Xóa trong lịch sử, xóa bút toán sổ chi tiết, xóa khai báo.\n– Báo "Xóa thành công.", tải lại danh sách.'],
        ['Bấm Hủy / (x)', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.9 In danh sách ---------------------------------------------------------------
FR.append({
    'ten': 'In danh sách', 'uc': 'uc_in', 'uc_ten': 'FR-09 In danh sách khai báo',
    'qtc': 'Quy tắc màn In và bố cục bản in.',
    'gioi_thieu': [
        ['Tên chức năng', 'In danh sách khai báo đầu kỳ công nợ'],
        ['Mô tả', 'In danh sách đang lọc theo mẫu "Công nợ đầu kỳ theo khách hàng - hợp đồng", khổ ngang, có tiêu đề công ty của người đăng nhập; cột in theo cột đang hiện trên bảng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm In danh sách.\n2. Hệ thống mở cửa sổ "Xem trước khai báo đầu kỳ công nợ" với bản in mọi dòng khớp bộ lọc.\n3. Bấm In để mở hộp in của trình duyệt.'],
        ['Dòng sự kiện phụ', '• Danh sách vượt 2,000 dòng: không in, báo "Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được…" kèm gợi ý thu hẹp bộ lọc (BR-11).\n• Số có phần lẻ giữ 2 chữ số thập phân, số chẵn in gọn.'],
    ],
    'menu_them': ' => In danh sách {icon:btn_indanhsach}',
    'ghi_chu_layout': 'Cửa sổ Xem trước bản in được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('19_printlist', 'Cửa sổ xem trước bản in danh sách')],
    'ui': ui(UI6, [
        ['Tiêu đề cửa sổ', 'Label', 'Read-only', '"Xem trước khai báo đầu kỳ công nợ"', '–'],
        ['Phần đầu bản in', 'Label', 'Read-only', 'Tiêu đề công ty', 'Logo, tên, địa chỉ công ty của người đăng nhập.'],
        ['Tiêu đề bản in', 'Label', 'Read-only', '"Công nợ đầu kỳ theo khách hàng - hợp đồng"', '–'],
        ['Bảng in', 'Table/Grid', 'Read-only', 'Theo bộ lọc', 'STT, Mã phiếu luôn có; các cột khác theo cột đang hiện (không gồm Hành động).'],
        ['Nút In', 'Button', 'Enable', '–', 'Mở hộp in của trình duyệt.'],
        ['Nút (x)', 'Button', 'Enable', '–', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In danh sách', 'Click', 'Before:\n– Kiểm tra quyền.\nAfter:\n– Dựng bản in theo bộ lọc + cột đang hiện; vượt 2,000 dòng thì chỉ hiện câu nhắc.'],
        ['Bấm In', 'Click', 'After:\n– Mở hộp in của trình duyệt.'],
    ],
})

# 2.10 Xuất Excel -----------------------------------------------------------------
FR.append({
    'ten': 'Xuất Excel danh sách', 'uc': 'uc_xuat', 'uc_ten': 'FR-10 Xuất Excel danh sách khai báo',
    'qtc': 'Quy tắc Excel và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách khai báo ra Excel'],
        ['Mô tả', 'Xuất mọi dòng khớp bộ lọc (không chỉ trang đang xem) ra file khai_bao_dau_ky_cong_no.xlsx, tiêu đề "DANH SÁCH CÔNG NỢ ĐẦU KỲ THEO KHÁCH HÀNG - HỢP ĐỒNG", cột theo lựa chọn và thứ tự người dùng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất file", tích sẵn các cột đang hiện trên bảng.\n3. Người dùng tích / bỏ, kéo ☰ đổi thứ tự, bấm Xuất file.\n4. Hệ thống tải dữ liệu theo lô (cạnh nút hiện tiến độ "Đã tải x/y dòng…"), dựng file và tải về; báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Không có dòng nào khớp bộ lọc → báo "Không có dữ liệu để xuất", không tải file.\n• Cột Dư nợ, Dư có là ô SỐ (cộng được), định dạng 1,234,567.89.'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất file')],
    'ui': ui(UI8, [
        ['Danh sách trường', 'Checkbox', 'Enable', '13 trường', 'Có (≥ 1)', 'Các cột đang hiện', 'Mã phiếu, Khách hàng, Tài khoản, Loại hợp đồng, Số hợp đồng, Dư nợ, Dư có, Quá hạn, Ngày BGNT, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. Kéo ☰ đổi thứ tự cột trong file.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', 'Chọn / bỏ nhanh mọi trường.'],
        ['Dòng đếm', 'Label', 'Read-only', '–', '–', '–', '"Đang chọn x/13 trường".'],
        ['Nút Xuất file', 'Button', 'Enable', '–', '–', '–', 'Xuất file theo trường đã chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng, không xuất.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất file', 'Click', 'Before:\n– Kiểm tra quyền.\nAfter:\n– Tải dữ liệu theo bộ lọc hiện tại, dựng file đúng thứ tự cột, tải về; báo kết quả.'],
        ['Kéo ☰', 'Drag', 'After:\n– Đổi thứ tự cột trong file.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.11 Import --------------------------------------------------------------------
FR.append({
    'ten': 'Import khai báo từ file Excel', 'uc': 'uc_import', 'uc_ten': 'FR-11 Import khai báo từ file Excel',
    'qtc': 'Quy tắc Import Excel, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Import khai báo đầu kỳ công nợ từ file Excel'],
        ['Mô tả', 'Nhập nhiều khai báo từ file theo file mẫu "Mau_import_cong_no_dau_ky_khach_hang.xlsx" (tải ngay trong cửa sổ). Mỗi dòng file = 1 khai báo, sinh mã và bút toán như khi lập tay. Tối đa 500 dòng mỗi lần.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Import Excel → cửa sổ "Import khai báo đầu kỳ công nợ".\n2. Bấm "Tải file mẫu", điền dữ liệu.\n3. Bấm "Chọn file Excel", chọn file; bấm "Load lên bảng".\n4. Bấm Validate: hệ thống kiểm từng dòng, hiện Tổng / Hợp lệ / Lỗi; dòng hợp lệ bị khóa, dòng lỗi nêu từng lỗi.\n5. Sửa dòng lỗi ngay trên bảng rồi Validate lại, hoặc bấm "Bỏ dòng lỗi".\n6. Bấm Import (chỉ bấm được khi không còn dòng lỗi).\n7. Hệ thống ghi từng dòng (sinh mã, bút toán, ghi nhận Tạo mới trong lịch sử), báo số dòng thành công, tải lại danh sách.'],
        ['Dòng sự kiện phụ', '• Dòng vừa bị người khác khai báo trùng sau lần Validate → bỏ qua dòng đó, các dòng khác vẫn nhập, kết quả nêu dòng bị bỏ.\n• "Xoá trạng thái validate" để sửa lại cả dòng đã khóa; "Làm mới" xoá bảng.\n• File quá 500 dòng → báo, không load.'],
    ],
    'menu_them': ' => Import Excel {icon:btn_import}',
    'ghi_chu_layout': 'Modal Import khai báo đầu kỳ công nợ được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('21_import_open', 'Cửa sổ Import khi vừa mở'), ('23_import_validated', 'Kết quả Validate — mỗi dòng lỗi nêu rõ lý do')],
    'ui': ui(UI8, [
        ['Cột Mã khách hàng', 'Textbox', 'Enable', 'Mã khách hàng có trong hệ thống', 'Có', 'Trống', 'Sai: "Khách hàng – Mã không tồn tại trong hệ thống".'],
        ['Cột Mã hợp đồng', 'Textbox', 'Enable', 'Số hợp đồng', 'Có', 'Trống', '"Mã hợp đồng – Không tồn tại trong hệ thống" / "Mã hợp đồng – Không thuộc khách hàng này".'],
        ['Cột Loại hợp đồng', 'Dropdown', 'Enable', 'HDDK, HDHNTDA, HDDV, HDMNN, HDMN, HDMTN', 'Có', 'Trống', 'HDDK: hợp đồng đầu kỳ · HDHNTDA: hợp đồng hãng / dự án · HDDV: hợp đồng dịch vụ BH - SC · HDMNN / HDMN / HDMTN: hợp đồng mua. Sai: "Loại hợp đồng – Chỉ nhận HDMNN / HDMN / HDMTN / HDDK / HDHNTDA / HDDV".'],
        ['Cột Số tài khoản', 'Textbox', 'Enable', 'Số hiệu tài khoản', 'Có', 'Trống', '"Số tài khoản – Không tồn tại trong hệ thống" / "… – Không được khai báo công nợ (tài khoản khoá hoặc không phải tài khoản chi tiết)".'],
        ['Cột Loại dư', 'Dropdown', 'Enable', 'Dư nợ / Dư có', 'Không', 'Trống = Dư nợ', 'Sai: "Loại dư – Chỉ nhận "Dư nợ" hoặc "Dư có"".'],
        ['Cột Công nợ', 'Textbox', 'Enable', 'Số > 0', 'Có', 'Trống', '"Công nợ – Bắt buộc phải nhập" / "Công nợ – Phải lớn hơn 0."'],
        ['Cột Công nợ quá hạn', 'Textbox', 'Enable', '1 (không) / 2 (có)', 'Không', 'Trống = không', '"Chỉ nhận 1 (không) hoặc 2 (có)"; quá hạn với Dư có: "Chỉ công nợ "Dư nợ" mới được đánh dấu quá hạn".'],
        ['Cột Ngày bàn giao nghiệm thu', 'Textbox', 'Enable', 'dd/mm/yyyy, ≤ hôm nay', 'Có khi quá hạn', 'Trống', '"Bắt buộc phải nhập" / "Ngày không hợp lệ (dd/mm/yyyy)" / "Không được lớn hơn ngày hiện tại".'],
        ['Trùng', '–', '–', '–', '–', '–', '"Trùng với dòng <n> trong file" · "Hợp đồng đã được khai báo công nợ đầu kỳ cho tài khoản này".'],
        ['Nút Tải file mẫu / Chọn file Excel / Load lên bảng / Validate / Import', 'Button', 'Enable / Disable', '–', '–', '–', 'Import chỉ bấm được sau Validate và không còn dòng lỗi.'],
        ['Nút Bỏ dòng lỗi / Xoá trạng thái validate / Làm mới / Đóng', 'Button', 'Enable', '–', '–', '–', 'Bỏ dòng lỗi khỏi bảng / mở khóa dòng đã validate / xoá bảng / đóng cửa sổ.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Load lên bảng', 'Click', 'During:\n– Đọc file, quá 500 dòng thì báo và dừng.\nAfter:\n– Hiện dữ liệu lên bảng xem trước.'],
        ['Bấm Validate', 'Click', 'Before:\n– Kiểm tra quyền.\nDuring:\n– Kiểm từng dòng theo bảng trên, trùng trong file, trùng khai báo đã có.\nAfter:\n– Hiện Tổng / Hợp lệ / Lỗi; khóa dòng hợp lệ.'],
        ['Bấm Import', 'Click', 'Before:\n– Kiểm tra quyền; không còn dòng lỗi.\nDuring:\n– Kiểm lại từng dòng, kiểm trùng ngay trước khi ghi.\n' + TRUOC_LUU + '\nAfter:\n– Mỗi dòng ghi riêng: sinh mã, ghi khai báo + bút toán, ghi nhận Tạo mới trong lịch sử.\n– Báo kết quả, tải lại danh sách.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ, không nhập gì.'],
    ],
})

# 2.12 Lịch sử --------------------------------------------------------------------
FR.append({
    'ten': 'Xem lịch sử thay đổi',
    'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem lịch sử thay đổi khai báo'],
        ['Mô tả', 'Liệt kê các lần thao tác trên 1 khai báo (Tạo mới, Thay đổi thông tin), mới nhất ở trên, kèm người thực hiện, phòng ban, thời điểm, giá trị cũ → mới của từng trường (Mã phiếu, Khách hàng, Hợp đồng, Tài khoản, Loại dư, Công nợ, Quá hạn, Ngày BGNT).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Lịch sử ở cột Hành động → cửa sổ "Lịch sử thay đổi: <mã phiếu>".\n2. Hoặc ở trang Chi tiết bấm "Xem lịch sử" ở khối Lịch sử.\n3. Hệ thống liệt kê các mốc; có nút Bộ lọc (loại hành động, người thực hiện, khoảng ngày).'],
        ['Dòng sự kiện phụ', '• Khai báo lập / import trên HRM có mốc Tạo mới.\n• Giá trị cũ in đỏ, giá trị mới in xanh.'],
    ],
    'menu_them': ' => Lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': 'Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối Lịch sử nằm cuối trang Chi tiết khai báo.',
    'anh': [('16_history', 'Cửa sổ Lịch sử thay đổi mở từ danh sách'), ('17b_detail_history', 'Khối Lịch sử ở trang Chi tiết')],
    'ui': ui(UI6, [
        ['Tiêu đề', 'Label', 'Read-only', '"Lịch sử thay đổi: <mã phiếu>"', '–'],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Lọc theo loại hành động, người thực hiện, Từ ngày, Đến ngày.'],
        ['Mốc lịch sử', 'Label', 'Read-only', 'Mới nhất trên cùng', 'Thời điểm, tên hành động, "Người thực hiện: <họ tên> — <phòng ban>", danh sách trường đổi: cũ → mới.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lịch sử / Xem lịch sử', 'Click', 'After:\n– Tải và hiển thị các mốc lịch sử của khai báo.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

FR_NAMES = ['FR-%02d %s' % (i + 1, f['ten']) for i, f in enumerate(FR)]

S = {
    'ten': TEN, 'ten_ngan': 'khai báo đầu kỳ công nợ', 'phan_he': 'Tài chính',
    'menu': [('Tài chính', 'menu_phanhe'), ('Khai báo đầu kỳ', 'menu_nhom'), (TEN, 'menu_muc')],
    'muc_dich': [
        'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho việc khai báo SỐ DƯ CÔNG NỢ ĐẦU KỲ của khách hàng theo từng hợp đồng × tài khoản — số mở đầu cho sổ chi tiết công nợ và các báo cáo công nợ.',
        'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
        'Làm rõ phạm vi dữ liệu theo bốn cấp quyền xem và cách xác định tổ chức của khai báo (theo người lập hợp đồng).',
        'Làm rõ thời điểm khai báo bị khóa sửa / xóa: khi đã phát sinh chứng từ công nợ (phiếu thu, phiếu chi, phiếu báo có, ủy nhiệm chi, phiếu kế toán).',
        'Làm rõ tác động sổ sách: mỗi khai báo ghi đúng 1 bút toán sổ chi tiết; sửa / xóa khai báo thì bút toán đổi / mất theo.',
    ],
    'thuat_ngu': [
        ['Khai báo đầu kỳ công nợ', 'Số dư công nợ của 1 khách hàng trên 1 hợp đồng ở 1 tài khoản tại ngày khai báo đầu kỳ. Mỗi khai báo có 1 mã phiếu.'],
        ['Dư nợ / Dư có', 'Khách hàng còn nợ công ty (ghi Nợ tài khoản) / công ty còn nợ khách hàng (ghi Có tài khoản).'],
        ['Ngày khai báo đầu kỳ (Ngày tính công nợ)', 'Mốc ngày khai ở Khai Quy chế – Cấu hình của công ty; là ngày hạch toán của mọi khai báo.'],
        ['Bút toán sổ chi tiết', 'Dòng ghi sổ chi tiết tài khoản do khai báo sinh ra; báo cáo công nợ đọc dòng này.'],
        ['Chứng từ công nợ', 'Phiếu thu, phiếu chi, phiếu báo có, ủy nhiệm chi, phiếu kế toán.'],
        ['Đã phát sinh chứng từ', 'Khai báo mà cùng khách hàng + hợp đồng + tài khoản đã có chứng từ công nợ ghi sổ, hoặc có chứng từ trừ thẳng vào khai báo.'],
        ['Quá hạn / Ngày BGNT', 'Đánh dấu công nợ Dư nợ đã quá hạn và ngày bàn giao nghiệm thu dùng tính quá hạn.'],
        ['Người lập hợp đồng', 'Nhân viên tạo hợp đồng gắn với khai báo; công ty / phòng ban / bộ phận của khai báo lấy theo người này.'],
    ],
    'trang_thai': {
        'cau_dan': 'Khai báo KHÔNG qua bước gửi duyệt / duyệt / từ chối / hủy: lưu xong là có hiệu lực ngay (đã ghi bút toán). '
                   'Trạng thái của khai báo do hệ thống tự xác định theo việc đã có chứng từ công nợ hay chưa, không có ô trạng thái để chọn.',
        'rows': [
            ['Chưa phát sinh chứng từ', 'Khai báo đã ghi sổ, chưa có chứng từ công nợ nào trên cùng khách hàng + hợp đồng + tài khoản.', 'Xem, Sửa, Xóa, In, Xuất, Lịch sử', 'Người có quyền "%s" trong phạm vi dữ liệu' % QUYEN],
            ['Đã phát sinh chứng từ', 'Đã có phiếu thu / phiếu chi / phiếu báo có / ủy nhiệm chi / phiếu kế toán ghi sổ cùng khách hàng + hợp đồng + tài khoản, hoặc trừ thẳng vào khai báo.', 'Xem, In, Xuất, Lịch sử (không Sửa, không Xóa)', 'Tự chuyển khi kế toán lập chứng từ công nợ'],
            ['Đã xóa', 'Khai báo và bút toán bị xóa khỏi hệ thống.', '–', 'Người có quyền "%s", chỉ từ trạng thái Chưa phát sinh' % QUYEN],
        ],
        'anh': 'state_flow',
        'ghi_chu': ['Chứng từ công nợ bị xóa / hủy ghi sổ thì khai báo tự trở lại Chưa phát sinh chứng từ. Phiếu xuất / nhập hàng, hạch toán dịch vụ trên cùng hợp đồng KHÔNG làm khai báo chuyển trạng thái (BR-05).'],
    },
    'quyen_truoc': ['Nhóm quyền thao tác: một quyền duy nhất cho cả màn (xem lẫn thao tác).'],
    'quyen_rows': [[QUYEN, 'Thấy 2 mục menu, vào màn; xem danh sách, tìm kiếm, xem chi tiết, lịch sử, tuỳ chỉnh cột, in, xuất Excel; Tạo mới, Sửa, Xóa, Import Excel.']],
    'pham_vi_truoc': ['Nhóm quyền quyết định phạm vi dữ liệu (xét theo thứ tự từ trên xuống, có quyền nào trước thì áp quyền đó):'],
    'pham_vi_rows': [
        ['1', 'Xem tất cả công nợ đầu kỳ', 'Khai báo của mọi công ty; khu vực lọc có ô Công ty, Phòng ban, Bộ phận.'],
        ['2', 'Xem tất cả công nợ đầu kỳ của công ty', 'Khai báo thuộc công ty đang làm việc của người dùng; có ô Phòng ban, Bộ phận.'],
        ['3', 'Xem tất cả công nợ đầu kỳ của phòng ban', 'Khai báo thuộc các phòng ban người dùng được giao quản lý.'],
        ['4', 'Xem tất cả công nợ đầu kỳ của bộ phận', 'Khai báo thuộc các bộ phận người dùng được giao quản lý.'],
        ['5', '(không có quyền nào ở trên)', 'Chỉ khai báo do chính người dùng tạo.'],
    ],
    'pham_vi_sau': ['Công ty / phòng ban / bộ phận của một khai báo = của NGƯỜI LẬP HỢP ĐỒNG (không phải người lập khai báo) — BR-04. '
                    'Phạm vi áp như nhau cho danh sách, chi tiết, sửa, xóa, in và xuất Excel; 4 quyền phạm vi dùng chung với màn Khai báo đầu kỳ công nợ nhà cung cấp.'],
    'ma_tran': [['Chức năng', QUYEN, 'Không có quyền']] + [
        [f, 'Có' + (' (khai báo Chưa phát sinh)' if i in (5, 7) else ''), 'Không'] for i, f in enumerate(FR_NAMES)],
    'ma_tran_widths': [3.0, 2.0, 1.2],
    'quyen_sau': ['Phạm vi dữ liệu của mọi chức năng theo bảng quyền phạm vi ở trên.'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Một khai báo = 1 hợp đồng × 1 tài khoản', ['– Lập 1 lần cho 1 khách hàng và nhiều hợp đồng; mỗi dòng lưu thành 1 khai báo riêng (1 mã phiếu, 1 bút toán).', '– Sửa / Chi tiết chỉ có 1 dòng; khách hàng và hợp đồng không đổi được sau khi lưu.'], ['Lập khai báo', 'Sửa', 'Import']),
        ('BR-02', 'Phạm vi dữ liệu theo 4 cấp quyền xem', ['– Xét lần lượt: tất cả → công ty → phòng ban quản lý → bộ phận quản lý → chỉ khai báo mình tạo.', '– Khai báo ngoài phạm vi: không hiện ở danh sách; mở thẳng thì trang "Không tìm thấy".'], ['Mọi chức năng']),
        ('BR-03', 'Mã phiếu', ['– Dạng <mã công ty của người lập>.CNĐKHĐ.<số thứ tự 5 chữ số>, số thứ tự = lớn nhất hiện có của cùng tiền tố + 1.', '– Hai người lưu cùng lúc không bị trùng mã (form và import dùng chung cách sinh).'], ['Lập khai báo', 'Import']),
        ('BR-04', 'Tổ chức của khai báo', ['– Công ty / phòng ban / bộ phận của khai báo lấy theo người lập hợp đồng; dùng cho phạm vi xem và ô lọc tổ chức.'], ['Lập khai báo', 'Import', 'Tìm kiếm và lọc']),
        ('BR-05', 'Chặn sửa / xóa khi đã phát sinh chứng từ', ['– Đã phát sinh = sổ chi tiết có phiếu thu, phiếu chi, phiếu báo có, ủy nhiệm chi hoặc phiếu kế toán cùng khách hàng + hợp đồng + tài khoản, hoặc có chứng từ trừ thẳng vào khai báo.', '– Phiếu xuất / nhập hàng, hạch toán dịch vụ (phát sinh trong kỳ) không tính.', '– Nút Sửa, Xóa ẩn; hệ thống chặn cả khi gửi yêu cầu trực tiếp ("Khai báo đã phát sinh chứng từ, không được sửa / xóa.").'], ['Sửa', 'Xóa', 'Xem chi tiết']),
        ('BR-06', 'Ghi sổ chi tiết', ['– Mỗi khai báo ghi 1 bút toán: Dư nợ ghi Nợ, Dư có ghi Có tài khoản đã chọn; số tiền = Công nợ; ngày hạch toán = Ngày khai báo đầu kỳ cấu hình của công ty người lập; chứng từ = mã phiếu.', '– Sửa khai báo cập nhật bút toán (kể cả đổi tài khoản); Xóa khai báo xóa bút toán.'], ['Lập khai báo', 'Sửa', 'Xóa', 'Import']),
        ('BR-07', 'Không trùng khai báo', ['– Cùng khách hàng + hợp đồng + tài khoản chỉ khai báo 1 lần (kể cả trên cùng form, khi Sửa đổi tài khoản và khi import).', '– Báo dưới ô Tài khoản của dòng trùng: "Đã khai báo đầu kỳ cho tài khoản này" (form) / "Trùng với dòng <n>"; import: "Hợp đồng đã được khai báo công nợ đầu kỳ cho tài khoản này".'], ['Lập khai báo', 'Sửa', 'Import']),
        ('BR-08', 'Quá hạn và Ngày BGNT', ['– Chỉ khai báo Dư nợ được đánh dấu Quá hạn; đổi sang Dư có thì bỏ Quá hạn và Ngày BGNT.', '– Quá hạn thì Ngày BGNT bắt buộc, không lớn hơn ngày hiện tại.'], ['Lập khai báo', 'Sửa', 'Import']),
        ('BR-09', 'Hợp đồng chọn được', ['– Chỉ hợp đồng THUỘC khách hàng đang chọn: hợp đồng bán đã duyệt / có hiệu lực, hợp đồng hãng có hiệu lực (loại hợp đồng hoặc hợp đồng dự án), hợp đồng gói dịch vụ và hợp đồng dự án khác Đang tạo, hợp đồng đầu kỳ, hợp đồng mua.', '– Import nhận thêm hợp đồng dịch vụ BH - SC (mã HDDV) và hợp đồng mua trong nước mới (HDMTN).'], ['Chọn hợp đồng', 'Import']),
        ('BR-10', 'Tài khoản chọn được', ['– Mọi tài khoản chi tiết (tài khoản không có tài khoản con) đang hoạt động.', '– Khai báo cũ dùng tài khoản nay đã khóa vẫn hiện tài khoản đó kèm biểu tượng khóa.'], ['Lập khai báo', 'Sửa', 'Import']),
        ('BR-11', 'In và xuất', ['– In và xuất theo đúng bộ lọc đang áp dụng (mọi trang); in tối đa 2,000 dòng, vượt thì không in một phần.', '– File Excel: ô số là SỐ; không có dữ liệu thì không xuất file.'], ['In danh sách', 'Xuất Excel']),
        ('BR-12', 'Thao tác xong quay về danh sách', ['– Lưu (Thêm / Sửa) và Xóa ở trang Chi tiết xong thì về màn danh sách.'], ['Lập khai báo', 'Sửa', 'Xóa']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây đọc hoặc dùng dữ liệu do Khai báo đầu kỳ công nợ ghi ra (khai báo và bút toán sổ chi tiết của khai báo).',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng có quyền "%s"' % QUYEN,
    'mains': [('FR-01', 'Xem danh sách khai báo', 'view'), ('FR-04', 'Lập khai báo đầu kỳ công nợ', 'crud'),
              ('FR-06', 'Sửa khai báo', 'crud'), ('FR-08', 'Xóa khai báo', 'action'),
              ('FR-09', 'In danh sách', 'io'), ('FR-10', 'Xuất Excel danh sách', 'io'),
              ('FR-11', 'Import khai báo từ Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc danh sách', 'view'), ('FR-03', 'Cài đặt bộ lọc, tuỳ chỉnh cột', 'view'),
             ('FR-07', 'Xem chi tiết khai báo', 'view'), ('FR-12', 'Xem lịch sử thay đổi', 'view')],
    'rieng': [('FR-04', 'Lập khai báo đầu kỳ công nợ', 'crud', 'uc_them'), ('FR-05', 'Chọn hợp đồng của khách hàng', 'crud', 'uc_chonhd'),
              ('FR-06', 'Sửa khai báo', 'crud', 'uc_sua'), ('FR-07', 'Xem chi tiết khai báo', 'view', 'uc_xem'),
              ('FR-08', 'Xóa khai báo', 'action', 'uc_xoa'), ('FR-09', 'In danh sách', 'io', 'uc_in'),
              ('FR-10', 'Xuất Excel danh sách', 'io', 'uc_xuat'), ('FR-11', 'Import khai báo từ Excel', 'io', 'uc_import')],
}

STATES = [('start', '', None), ('chua', 'Chưa phát sinh chứng từ', '#dcfce7'), ('da', 'Đã phát sinh chứng từ', '#fef3c7'),
          ('end', '', None)]
TRANS = [('start', 'chua', 'Lưu / Import'), ('chua', 'da', 'Lập chứng từ công nợ'),
         ('da', 'chua', 'Chứng từ bị xóa / hủy ghi sổ'), ('chua', 'end', 'Xóa (khai báo + bút toán)')]

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    L.draw_state_flow(os.path.join(scr.uml, 'state_flow.png'), STATES, TRANS)
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))

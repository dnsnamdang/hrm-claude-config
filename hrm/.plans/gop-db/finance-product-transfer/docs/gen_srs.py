# -*- coding: utf-8 -*-
"""SRS - Phiếu điều chuyển hàng (STT 204) — khuôn màn mẫu phiếu finance-declare-debt-beginning/docs/kh/gen_srs.py.

Nguồn (code HRM origin/develop, 02/11/2026):
  FE hrm-client/pages/finance/product-transfers/{index, create, _id/index, _id/edit}.vue,
     components/ProductTransferForm.vue, components/V2Footer.vue, components/subsystem-menu/finance.js
  BE Modules/Finance: Entities/ProductTransfer/{ProductTransfer, ProductTransferDetail}.php,
     Http/Controllers/V1/ProductTransferController.php, Http/Requests/ProductTransfer/ProductTransferFormRequest.php,
     Services/{ProductTransferService, ProductTransferWriteService, ProductTransferAccountingService,
     ProductTransferHistoryService, ProductTransferPrintService}.php; app/Services/CatalogHistoryService.php
  Ảnh: capture.js (dev-hrm). Phần 5: dò code FE/BE 02/11/2026.
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402
from _lib_phieu import ui, UI4, UI4W, UI6, UI6W, UI7, UI7W, UI8, UI8W, TRUOC_LUU  # noqa: E402

TEN = 'Phiếu điều chuyển hàng'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q_LAP = 'Kế toán kho'
Q_TCT = 'Xem phiếu điều chuyển hàng theo - tổng công ty'
Q_CT = 'Xem phiếu điều chuyển hàng theo - công ty'
Q = 'Người dùng đăng nhập; thao tác lập / sửa / xóa cần quyền "%s"' % Q_LAP
Q_XEM = 'Người dùng đăng nhập (xem theo phạm vi dữ liệu ở Phần 2)'
DK = '1. Người dùng đăng nhập thành công.'
DK_LAP = DK + '\n2. Người dùng có quyền "%s".' % Q_LAP
DK_NHAP = DK + '\n2. Phiếu ở trạng thái Đang tạo và người dùng là người lập phiếu.'
TRANG = 'Trang %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'
POPUP = 'Modal %s được mở ngay trên màn hình %s theo đường dẫn ở trên.'

P5 = [
    ('Tài chính', 'Phiếu xuất hàng (giá vốn xuất kho tính theo lớp nhập do phiếu điều chuyển ghi vào kho nhập)',
     'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng => Phiếu xuất hàng'),
    ('Tài chính', 'Phiếu yêu cầu chuyển hàng (số lượng tồn kế toán theo kho)',
     'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng => Phiếu yêu cầu chuyển hàng'),
    ('Tài chính', 'Phiếu xuất hàng điều chỉnh kiểm kê (tồn kế toán theo kho)',
     'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng => Phiếu xuất hàng điều chỉnh kiểm kê'),
    ('Tài chính', 'Danh sách hàng mượn, Yêu cầu xuất hàng mượn (tồn kế toán có thể xuất)',
     'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng'),
    ('Tài chính', 'Các phiếu Giữ hàng: yêu cầu xuất giữ, gia hạn, điều chuyển, hủy hàng giữ (tồn kế toán có thể giữ)',
     'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng'),
    ('Tra cứu - thông báo', 'Hàng có thể bán theo công ty (tồn kế toán theo kho của công ty)',
     'Tra cứu - thông báo => Tra cứu tồn kho => Hàng có thể bán theo công ty'),
    ('Kho', 'Kho vật lý (kho đã có phiếu điều chuyển không xóa được)', 'Kho => Danh mục => Kho vật lý'),
]

FR = []

# 2.1 Xem danh sách ----------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách phiếu điều chuyển hàng',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách phiếu điều chuyển hàng'],
        ['Mô tả', 'Hiển thị các phiếu điều chuyển hàng trong phạm vi dữ liệu của người dùng, có phân trang, sắp xếp, nhãn trạng thái và nút thao tác theo từng dòng.'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), phiếu tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Không có phiếu khớp → bảng hiện "Không có dữ liệu phù hợp bộ lọc."\n• Phiếu Đang tạo chỉ người lập nhìn thấy (BR-02).\n• Phiếu Đã hạch toán chỉ còn In phiếu, Lịch sử (BR-05).'],
    ],
    'anh': [('01_list', 'Màn danh sách Phiếu điều chuyển hàng lúc mới truy cập'),
            ('01b_list_actions', 'Cột Hành động: phiếu Đang tạo có Sửa, Xóa (In phiếu, Lịch sử trong nút ba chấm); phiếu Đã hạch toán có In phiếu, Lịch sử')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Phiếu điều chuyển hàng', 'Tiêu đề khối danh sách và tiêu đề trang.'],
        ['Nút Tạo mới', 'Button', 'Enable / Ẩn', 'Theo quyền', 'Chỉ hiện khi có quyền "%s"; mở trang "Thêm phiếu điều chuyển hàng" (mục 2.4).' % Q_LAP],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất file" (mục 2.12). Trong lúc xuất, chữ trên nút đổi thành tiến độ.'],
        ['Nút In danh sách', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ xem trước bản in danh sách (mục 2.11).'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.3).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa.'],
        ['Cột Số phiếu', 'Table/Grid', 'Read-only', 'Hiển thị', '- Dạng PDCH-<5 chữ số> (BR-03). Sắp xếp được.\n- Dạng liên kết: bấm mở trang Chi tiết (mục 2.8), chuột phải mở tab mới được. Cột khóa.'],
        ['Cột Ngày hạch toán', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm; phiếu Đang tạo để trống. Sắp xếp được.'],
        ['Cột Kho vật lý', 'Table/Grid', 'Read-only', 'Hiển thị', '"Mã - Tên kho vật lý".'],
        ['Cột Kho xuất, Kho nhập', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên kho kế toán xuất / nhập.'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', '"Họ tên - Mã phòng ban".'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được (mặc định giảm dần).'],
        ['Cột Trạng thái', 'Table/Grid', 'Read-only', 'Hiển thị', 'Nhãn màu: Đang tạo (xám), Đã hạch toán (xanh lá). Không sắp xếp.'],
        ['Cột Ghi chú, Người cập nhật, Ngày cập nhật', 'Table/Grid', 'Read-only', 'Ẩn', 'Mặc định ẩn, bật ở Tuỳ chỉnh cột.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sửa, Xóa: chỉ hiện khi phiếu Đang tạo và người xem là người lập (BR-05).\n- In phiếu, Lịch sử: luôn có (khi đủ chỗ thì nằm trong nút ba chấm "Hành động khác").\n- Nút không dùng được thì ẩn, không làm mờ. Cột khóa.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Kiểm tra đăng nhập.\nAfter:\n– Tải trang 1 theo phạm vi dữ liệu (BR-02), phiếu tạo gần nhất trên cùng; khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút); hiện nút Tạo mới khi có quyền "%s".' % Q_LAP],
        ['Bấm tiêu đề cột Số phiếu / Ngày hạch toán / Ngày tạo', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại dữ liệu từ trang 1.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp, tải lại dữ liệu; đổi số dòng thì quay về trang 1.'],
        ['Bấm Số phiếu', 'Click', 'After:\n– Mở trang Chi tiết phiếu (mục 2.8).'],
    ],
})

# 2.2 Tìm kiếm và lọc -------------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc danh sách',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách phiếu điều chuyển hàng'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao.'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập số phiếu rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện (vẫn trong phạm vi dữ liệu) và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô gõ chữ (tìm nhanh, Mã hàng hóa, Tên hàng hóa) chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Bấm Làm mới → xoá mọi điều kiện và tải lại danh sách.\n• Hệ thống ghi nhớ bộ lọc 10 phút khi rời màn rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực Tìm kiếm nâng cao ở trạng thái mở')],
    'ui': ui(UI7, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Tìm theo số phiếu..."; tìm gần đúng theo Số phiếu.'],
        ['Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Áp dụng / xoá mọi điều kiện lọc rồi tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực ô lọc (khi mở, nút đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" (mục 2.3).'],
        ['Ô Công ty – Phòng ban – Bộ phận', 'Dropdown', 'Enable', 'Danh sách tổ chức', 'Trống', 'Lọc theo tổ chức của phiếu (= tổ chức của người lập lúc lập phiếu). Phòng ban, Bộ phận khóa (biểu tượng khóa) tới khi chọn cấp trên. Kết quả vẫn nằm trong phạm vi dữ liệu.'],
        ['Ô Kho vật lý', 'Dropdown', 'Enable', 'Kho vật lý có kho kế toán của công ty', 'Trống', '"Mã - Tên kho".'],
        ['Ô Kho xuất / Kho nhập', 'Dropdown', 'Enable', 'Kho kế toán đang hoạt động của công ty', 'Trống', '"Mã - Tên kho kế toán"; lọc theo kho xuất / kho nhập của phiếu.'],
        ['Ô Trạng thái', 'Dropdown', 'Enable', 'Đang tạo / Đã hạch toán', 'Trống', 'Bỏ trống thì hiện cả hai.'],
        ['Ô Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc phiếu do người được chọn lập.'],
        ['Ô Mã hàng hóa / Tên hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Tìm gần đúng: phiếu có ít nhất 1 dòng hàng khớp; lọc khi Enter / Tìm kiếm.'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy, Từ → Đến', 'Trống', 'Lọc theo ngày lập phiếu, tính cả 2 đầu mút.'],
        ['Ô Ngày hạch toán', 'Datepicker', 'Enable', 'dd/mm/yyyy, Từ → Đến', 'Trống', 'Lọc theo ngày hạch toán, tính cả 2 đầu mút (phiếu Đang tạo không có ngày hạch toán).'],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm Tìm kiếm / nhấn Enter ở ô gõ chữ', 'Click', 'After:\n– Áp đồng thời từ khóa và các ô lọc, tải lại bảng từ trang 1.'],
        ['Chọn giá trị ở ô chọn', 'Change', 'After:\n– Tải lại bảng từ trang 1 ngay.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khu vực ô lọc.'],
    ],
})

# 2.3 Cài đặt bộ lọc / tuỳ chỉnh cột ----------------------------------------------
FR.append({
    'ten': 'Cài đặt bộ lọc và tuỳ chỉnh cột',
    'qtc': 'Bộ lọc, Cấu hình cột và lưu cấu hình theo người dùng.',
    'gioi_thieu': [
        ['Tên chức năng', 'Cài đặt bộ lọc và tuỳ chỉnh cột'],
        ['Mô tả', 'Người dùng chọn ô lọc nào hiển thị / thứ tự ô lọc, và cột nào hiển thị / thứ tự cột trên bảng. Cấu hình lưu theo từng người dùng, từng màn.'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Bấm "Cài đặt bộ lọc" (hoặc biểu tượng Cấu hình cột hiển thị).\n2. Tích / bỏ tích, kéo ☰ để đổi thứ tự.\n3. Bấm Lưu: hệ thống lưu cấu hình và áp dụng ngay.'],
        ['Dòng sự kiện phụ', '• Bấm Đóng: bỏ thay đổi.\n• Cài đặt bộ lọc có nút "Khôi phục mặc định".\n• Cột STT, Số phiếu, Hành động không bỏ được (có biểu tượng khóa).\n• Ẩn một ô lọc thì giá trị đang lọc ở ô đó bị xoá.'],
    ],
    'menu_them': ' => Cài đặt bộ lọc {icon:btn_caidatboloc} / Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': 'Modal Cài đặt bộ lọc và Modal Tuỳ chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('26_filtercfg', 'Cửa sổ Cài đặt bộ lọc'), ('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột')],
    'ui': ui(UI6, [
        ['Danh sách ô lọc', 'Checkbox', 'Enable', 'Đủ 10 ô', 'Công ty – Phòng ban, Kho vật lý, Kho xuất, Kho nhập, Trạng thái, Người tạo, Mã hàng hóa, Tên hàng hóa, Ngày tạo, Ngày hạch toán. Kéo ☰ đổi thứ tự.'],
        ['Nút Khôi phục mặc định', 'Button', 'Enable', '–', 'Đưa cấu hình ô lọc về mặc định.'],
        ['Danh sách cột', 'Checkbox', 'Enable', '10/13 cột', 'Tích cột muốn hiện; STT, Số phiếu, Hành động bị khóa. Dòng đếm "Đang chọn x/13 cột".'],
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

# 2.4 Lập phiếu -------------------------------------------------------------------
FR.append({
    'ten': 'Lập phiếu điều chuyển hàng (Lưu nháp)', 'uc': 'uc_them', 'uc_ten': 'FR-04 Lập phiếu điều chuyển hàng',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Lập phiếu điều chuyển hàng và lưu ở trạng thái Đang tạo'],
        ['Mô tả', 'Kế toán kho chọn 1 kho vật lý, kho kế toán xuất và kho kế toán nhập thuộc kho vật lý đó, thêm các dòng hàng hóa và số lượng chuyển. "Lưu nháp" ghi phiếu ở trạng thái Đang tạo: CHƯA trừ / cộng tồn, chưa ghi sổ; còn sửa, xóa được.'],
        ['Tác nhân', 'Người dùng có quyền "%s"' % Q_LAP],
        ['Điều kiện ban đầu', DK_LAP],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở trang "Thêm phiếu điều chuyển hàng"; góc phải khối Thông tin chung hiện "<Người đăng nhập> - <ngày giờ hiện tại>".\n3. Người dùng chọn Kho vật lý → ô Kho xuất, Kho nhập mở ra, chỉ liệt kê kho kế toán thuộc kho vật lý đó.\n4. Chọn Kho xuất, Kho nhập; nhập Ghi chú, thêm File đính kèm (nếu cần).\n5. Bấm "Thêm hàng hóa", chọn hàng (mục 2.5); mỗi dòng nhập SL chuyển, chọn ĐVT; cột SL tồn hiện tồn của kho xuất theo đơn vị đang chọn.\n6. Bấm "Lưu nháp".\n7. Hệ thống kiểm tra dữ liệu (BR-06), sinh Số phiếu (BR-03), ghi phiếu ở trạng thái Đang tạo, ghi nhận Tạo mới trong lịch sử.\n8. Báo "Lưu thành công", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Bấm "Lưu và tiếp tục": lưu như trên (Đang tạo) rồi mở lại trang Thêm trống.\n• Bấm "Lưu và duyệt": lưu và hạch toán ngay (mục 2.6).\n• Lưu nháp chỉ bắt buộc Kho vật lý; kho xuất / kho nhập / dòng hàng có thể bổ sung sau. Đã nhập SL thì phải > 0 và không vượt tồn.\n• Chưa chọn đủ 3 kho: nút "Thêm hàng hóa" ẩn, thay bằng dòng hướng dẫn "Chọn đủ Kho vật lý, Kho xuất và Kho nhập … rồi mới thêm được hàng hóa".\n• Đổi Kho vật lý → xoá Kho xuất, Kho nhập và toàn bộ dòng hàng. Đổi Kho xuất / ĐVT → SL tồn tính lại.\n• Bấm nút thùng rác cuối dòng → hộp "Xác nhận xóa hàng hóa" → Xác nhận thì bỏ dòng.\n• Lỗi kiểm tra → báo đỏ dưới đúng ô / đúng dòng, cuộn tới ô lỗi đầu tiên, không lưu.\n• Bấm Quay lại: về danh sách, không lưu (theo quy tắc chung, đã nhập thì hỏi "Thông tin chưa lưu").'],
        ['Yêu cầu đặc biệt', 'Nút lưu bị chặn bấm lặp trong lúc đang gửi, tránh tạo 2 phiếu.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': TRANG % '"Thêm phiếu điều chuyển hàng"',
    'anh': [('10_create', 'Trang Thêm phiếu điều chuyển hàng lúc mới mở'),
            ('10a_create_kho', 'Đã chọn đủ 3 kho: nút Thêm hàng hóa hiện ra'),
            ('10b_create_filled', 'Đã thêm 2 dòng hàng; dòng 2 nhập vượt tồn bị báo đỏ'),
            ('15_remove_row', 'Hộp Xác nhận xóa hàng hóa khi bấm thùng rác cuối dòng')],
    'ui': ui(UI8, [
        ['Người tạo - ngày giờ', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại', 'Góc phải khối Thông tin chung.'],
        ['Kho vật lý', 'Dropdown', 'Enable', 'Kho vật lý đang hoạt động có kho kế toán của công ty người dùng', 'Có', 'Trống', 'Placeholder "Chọn kho vật lý"; bỏ trống: "Kho vật lý không được để trống".'],
        ['Kho xuất', 'Dropdown', 'Enable / Disable', 'Kho kế toán đang hoạt động thuộc kho vật lý đã chọn', 'Có khi Lưu và duyệt', 'Trống', 'Khóa tới khi chọn Kho vật lý. Trùng Kho nhập: "Kho xuất, kho nhập không được trùng nhau".'],
        ['Kho nhập', 'Dropdown', 'Enable / Disable', 'Như Kho xuất', 'Có khi Lưu và duyệt', 'Trống', 'Khác Kho xuất (BR-07).'],
        ['Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Ô nhiều dòng, placeholder "Nhập ghi chú".'],
        ['File đính kèm', 'File', 'Enable', 'pdf, png, jpg, jpeg; ≤ 20MB/tệp', 'Không', 'Trống', '- Nút "Thêm tài liệu"; lưới STT, Upload / File, Dung lượng.\n- Tệp tải lên ngay khi chọn, xem trước / tải xuống / thay đổi được trước khi lưu. Sai định dạng: "Chỉ nhận file pdf, png, jpg, jpeg"; quá dung lượng: "Dung lượng tối đa 20MB".'],
        ['Nút Thêm hàng hóa', 'Button', 'Enable / Ẩn', '–', '–', '–', 'Chỉ hiện khi đã chọn đủ 3 kho; mở cửa sổ "Thêm hàng hoá" (mục 2.5).'],
        ['Cột Tên hàng hóa, Model, Mã hàng', 'Table/Grid', 'Read-only', '–', '–', 'Theo hàng đã chọn', 'Tự điền.'],
        ['Cột SL tồn', 'Table/Grid', 'Read-only', '–', '–', 'Tự tính', 'Tồn có thể chuyển của kho xuất, quy theo ĐVT đang chọn (BR-08).'],
        ['Cột SL chuyển', 'Textbox', 'Enable', 'Số > 0, ≤ SL tồn, tối đa 999,999,999', 'Có khi Lưu và duyệt', '0', 'Bỏ trống: "Bắt buộc phải nhập"; ≤ 0: "Phải lớn hơn 0"; vượt tồn: "Số lượng chuyển vượt quá số lượng tồn (còn <n>)" — hệ thống giữ nguyên số đã nhập, không tự sửa.'],
        ['Cột ĐVT', 'Dropdown', 'Enable', 'Đơn vị của hàng hóa (kèm hệ số quy đổi)', 'Có khi Lưu và duyệt', 'Đơn vị cơ bản', 'Nhãn dạng "Thùng (x24)" khi hệ số khác 1; bỏ trống: "Bắt buộc phải chọn đơn vị tính".'],
        ['Cột TK nợ, TK có', 'Table/Grid', 'Read-only', '156', '–', '156', 'Cố định 156 – hàng hóa (BR-09).'],
        ['Nút xoá dòng', 'Button', 'Enable', '–', '–', '–', 'Hỏi "Xác nhận xóa hàng hóa" rồi bỏ dòng khỏi bảng.'],
        ['Nút Lưu nháp', 'Button', 'Enable', '–', '–', '–', 'Lưu ở trạng thái Đang tạo rồi về danh sách.'],
        ['Nút Lưu và duyệt', 'Button', 'Enable', '–', '–', '–', 'Lưu và hạch toán ngay (mục 2.6).'],
        ['Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', '–', 'Chỉ ở trang Thêm: lưu Đang tạo rồi mở lại trang Thêm trống.'],
        ['Nút Quay lại', 'Button', 'Enable', '–', '–', '–', 'Về danh sách, không lưu.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'Before:\n– Nút chỉ hiện khi có quyền "%s".\nAfter:\n– Mở trang Thêm trống, nạp danh sách kho vật lý.' % Q_LAP],
        ['Chọn / đổi Kho vật lý', 'Change', 'After:\n– Xoá Kho xuất, Kho nhập, toàn bộ dòng hàng; nạp kho kế toán thuộc kho vật lý.'],
        ['Chọn / đổi Kho xuất, ĐVT', 'Change', 'After:\n– Bỏ lỗi trùng kho cũ; tính lại SL tồn cho mọi dòng (1 lần gọi cho cả bảng).'],
        ['Bấm Lưu nháp / Lưu và tiếp tục', 'Click', 'Before:\n– Kiểm tra quyền "%s" (thiếu quyền: "Bạn không có quyền lập phiếu điều chuyển hàng").\nDuring:\n– Kiểm theo BR-06 (lưu nháp chỉ bắt buộc Kho vật lý), kho xuất ≠ kho nhập, không trùng hàng + ĐVT, hàng không đang kiểm kho, SL không vượt tồn.\n' % Q_LAP + TRUOC_LUU + '\nAfter:\n– Sinh Số phiếu, ghi phiếu trạng thái Đang tạo + các dòng hàng; gắn tệp đính kèm. KHÔNG trừ / cộng tồn, KHÔNG ghi sổ.\n– Ghi nhận Tạo mới trong lịch sử.\n– Báo "Lưu thành công"; Lưu nháp → về danh sách, Lưu và tiếp tục → trang Thêm trống.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Về danh sách, không lưu.'],
    ],
})

# 2.5 Chọn hàng hóa ---------------------------------------------------------------
FR.append({
    'ten': 'Chọn hàng hóa vào phiếu', 'uc': 'uc_chonhang', 'uc_ten': 'FR-05 Chọn hàng hóa vào phiếu',
    'qtc': 'Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chọn hàng hóa vào phiếu điều chuyển'],
        ['Mô tả', 'Cửa sổ "Thêm hàng hoá" dùng chung của hệ thống (chỉ tab hàng hóa, không cho tạo hàng tạm): tìm theo cây danh mục, mã, tên, model, barcode; tích nhiều hàng rồi bấm "Thêm n hàng hoá".'],
        ['Tác nhân', 'Người dùng có quyền "%s"' % Q_LAP],
        ['Điều kiện ban đầu', DK_LAP + '\n3. Đang ở trang Thêm / Sửa và đã chọn đủ Kho vật lý, Kho xuất, Kho nhập.'],
        ['Dòng sự kiện chính', '1. Bấm "Thêm hàng hóa".\n2. Hệ thống mở cửa sổ "Thêm hàng hoá" (20 dòng/trang).\n3. Người dùng tìm và tích hàng cần chuyển, bấm "Thêm n hàng hoá".\n4. Hệ thống thêm mỗi hàng 1 dòng vào bảng Chi tiết, ĐVT mặc định là đơn vị cơ bản, SL chuyển = 0, tính SL tồn theo kho xuất.'],
        ['Dòng sự kiện phụ', '• Hàng đã có trong phiếu: không thêm lại, báo "Hàng hóa đã có trong phiếu: <tên>".\n• Hàng ngoài danh mục (hàng tạm): bỏ qua, báo "… phiếu điều chuyển chỉ nhận hàng hóa có trong danh mục (không nhận hàng tạm)".\n• Bấm Đóng: đóng cửa sổ, không thêm.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi} => Thêm hàng hóa {icon:btn_themhang}',
    'ghi_chu_layout': POPUP % ('Thêm hàng hoá', 'Thêm / Sửa phiếu điều chuyển hàng'),
    'anh': [('14_picker', 'Cửa sổ Thêm hàng hoá')],
    'ui': ui(UI8, [
        ['Cây danh mục', 'Tree', 'Enable', 'Catalog hàng hóa', 'Không', 'Tất cả hàng hoá', 'Lọc theo nhánh catalog; có ô "Tìm trong cây catalog".'],
        ['Ô tìm kiếm', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Placeholder "Tìm theo mã, tên hàng hoá, model, barcode, mã đặt hàng".'],
        ['Công tắc Còn tồn / Gồm hàng ngoài catalog', 'Switch', 'Enable', 'Bật / Tắt', 'Không', 'Tắt / Bật', 'Chỉ hàng còn tồn / tính cả hàng chưa xếp catalog.'],
        ['Nút Tìm kiếm nâng cao, Làm mới, Cấu hình cột', 'Button', 'Enable', '–', '–', '–', 'Lọc thêm / xoá điều kiện / chọn cột của cửa sổ.'],
        ['Bảng hàng hóa', 'Table/Grid', 'Enable', '20 dòng/trang', '–', '–', 'Ô tích, STT, Ảnh, Mã hàng, Tên hàng hoá, Model, Thương hiệu, Loại sản phẩm…'],
        ['Nút Thêm n hàng hoá', 'Button', 'Enable / Disable', '–', '–', 'Thêm 0 hàng hoá', 'Chỉ bấm được khi đã tích ít nhất 1 hàng.'],
        ['Nút Đóng / (x)', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Thêm n hàng hoá', 'Click', 'During:\n– Bỏ hàng trùng, hàng tạm (báo cảnh báo).\nAfter:\n– Thêm dòng, nạp ĐVT của từng hàng, tính SL tồn theo kho xuất cho cả bảng.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.6 Lưu và duyệt (hạch toán) ------------------------------------------------------
FR.append({
    'ten': 'Lưu và duyệt (hạch toán phiếu)', 'uc': 'uc_duyet', 'uc_ten': 'FR-06 Lưu và duyệt phiếu điều chuyển hàng',
    'qtc': 'Validate dữ liệu, Thông báo, Quy tắc xác nhận thao tác và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Lưu và duyệt — hạch toán phiếu điều chuyển hàng'],
        ['Mô tả', 'Lưu phiếu và hạch toán ngay: trừ tồn kế toán kho xuất, cộng tồn kế toán kho nhập, tính giá vốn từng dòng, ghi bút toán Nợ 156 / Có 156. Phiếu chuyển sang Đã hạch toán và khóa vĩnh viễn (không sửa, không xóa, không hủy).'],
        ['Tác nhân', 'Người dùng có quyền "%s"' % Q_LAP],
        ['Điều kiện ban đầu', DK_LAP + '\n3. Đang ở trang Thêm (phiếu mới) hoặc trang Sửa của phiếu Đang tạo do chính mình lập.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập đủ thông tin, bấm "Lưu và duyệt".\n2. Hệ thống hiện hộp "Xác nhận lưu và duyệt": "Bạn đồng ý lưu và duyệt?".\n3. Bấm Xác nhận.\n4. Hệ thống kiểm tra đủ dữ liệu (BR-06), ghi phiếu, rồi hạch toán (BR-10): với từng dòng trừ tồn kho xuất, ghi nhật ký tồn và giá vốn, cộng tồn kho nhập; ghi Ngày hạch toán = thời điểm duyệt; ghi bút toán sổ chi tiết.\n5. Ghi nhận lịch sử: phiếu mới → Tạo mới (trạng thái Đã hạch toán); phiếu sửa → Thay đổi trạng thái "Đang tạo → Đã hạch toán" và Thay đổi thông tin (nếu có).\n6. Báo "Điều chuyển thành công", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Bấm Hủy / (x) ở hộp xác nhận → không lưu, ở lại form.\n• Thiếu Kho xuất / Kho nhập / dòng hàng / SL / ĐVT, vượt tồn, hàng đang kiểm kho → báo lỗi, không lưu, không hạch toán.\n• Kho xuất không có tồn kế toán của hàng → báo lỗi, toàn bộ thao tác bị hủy (không có phần nào được ghi).'],
        ['Yêu cầu đặc biệt', 'Toàn bộ ghi phiếu + hạch toán chạy trong 1 giao dịch: lỗi ở bất kỳ dòng nào thì không ghi gì.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi} => Lưu và duyệt {icon:btn_luuduyet}',
    'hoac_menu': ['Hoặc Menu: Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Điều chuyển => Phiếu điều chuyển hàng => Sửa {icon:btn_sua} => Lưu và duyệt {icon:btn_luuduyet}'],
    'ghi_chu_layout': 'Hộp Xác nhận lưu và duyệt được mở ngay trên trang Thêm / Sửa phiếu theo đường dẫn ở trên.',
    'anh': [('15b_approve_confirm', 'Hộp Xác nhận lưu và duyệt')],
    'ui': ui(UI4, [
        ['Nút Lưu và duyệt', 'Button', 'Ở chân trang Thêm / Sửa.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận lưu và duyệt".'],
        ['Nội dung', 'Label', '"Bạn đồng ý lưu và duyệt?"'],
        ['Nút Xác nhận', 'Button', 'Lưu và hạch toán.'],
        ['Nút Hủy / (x)', 'Button', 'Đóng hộp, không lưu.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Lưu và duyệt', 'Click', 'After:\n– Hiện hộp Xác nhận lưu và duyệt.'],
        ['Bấm Xác nhận', 'Click', 'Before:\n– Kiểm tra quyền "%s"; phiếu sửa phải còn Đang tạo và do mình lập.\nDuring:\n– Kiểm đủ trường bắt buộc, kho xuất ≠ kho nhập, không trùng hàng, hàng không đang kiểm kho, SL > 0 và không vượt tồn.\n' % Q_LAP + TRUOC_LUU + '\nAfter:\n– Ghi phiếu + dòng hàng; trừ tồn kế toán kho xuất (và tồn kế toán của kho vật lý), cộng tồn kho nhập (tạo dòng tồn nếu kho nhập chưa có hàng); ghi nhật ký tồn kèm giá trị tồn trước / sau.\n– Giá vốn từng dòng = (giá trị tồn trước − sau) / số lượng quy đổi; Thành tiền vốn = số lượng × giá vốn.\n– Ghi bút toán Nợ 156 / Có 156 theo Thành tiền vốn (bỏ dòng có thành tiền 0); trạng thái Đã hạch toán, Ngày hạch toán = hiện tại.\n– Ghi nhận lịch sử; báo "Điều chuyển thành công", về danh sách.'],
        ['Bấm Hủy / (x)', 'Click', 'After:\n– Đóng hộp, giữ nguyên form.'],
    ],
})

# 2.7 Sửa -----------------------------------------------------------------------
FR.append({
    'ten': 'Sửa phiếu Đang tạo', 'uc': 'uc_sua', 'uc_ten': 'FR-07 Sửa phiếu điều chuyển hàng',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Sửa phiếu điều chuyển hàng'],
        ['Mô tả', 'Người lập sửa phiếu đang ở trạng thái Đang tạo: đổi được mọi thông tin (kho, ghi chú, tệp, dòng hàng), rồi Lưu nháp hoặc Lưu và duyệt.'],
        ['Tác nhân', 'Người lập phiếu'],
        ['Điều kiện ban đầu', DK_NHAP],
        ['Dòng sự kiện chính', '1. Bấm Sửa ở cột Hành động (hoặc nút Sửa ở trang Chi tiết).\n2. Hệ thống mở trang "Sửa phiếu điều chuyển hàng" với dữ liệu hiện tại, tính lại SL tồn từng dòng.\n3. Người dùng sửa và bấm "Lưu nháp".\n4. Hệ thống kiểm tra như khi lập, ghi đè thông tin và toàn bộ dòng hàng.\n5. Ghi nhận Thay đổi thông tin (chỉ các trường đổi; dòng hàng theo nhóm thêm mới / đã xóa / sửa).\n6. Báo "Cập nhật thành công", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Bấm "Lưu và duyệt" → mục 2.6.\n• Phiếu đã hạch toán hoặc không phải người lập: nút Sửa ẩn; nếu vẫn gửi lưu thì báo "Phiếu đã hạch toán hoặc bạn không có quyền sửa".\n• Trang Sửa không có "Lưu và tiếp tục".\n• Kho / hàng đã khóa mà phiếu đang dùng vẫn hiện trên ô chọn.'],
    ],
    'menu_them': ' => Sửa {icon:btn_sua}',
    'ghi_chu_layout': TRANG % '"Sửa phiếu điều chuyển hàng"',
    'anh': [('12_edit', 'Trang Sửa phiếu điều chuyển hàng')],
    'ui': ui(UI8, [
        ['Kho vật lý, Kho xuất, Kho nhập', 'Dropdown', 'Enable', 'Như trang Thêm', 'Có', 'Dữ liệu hiện tại', 'Đổi Kho vật lý thì xoá kho xuất / nhập và dòng hàng như trang Thêm.'],
        ['Ghi chú, File đính kèm', 'Textarea / File', 'Enable', 'Như trang Thêm', 'Không', 'Dữ liệu hiện tại', 'Xóa tệp đã lưu: gỡ ngay khỏi phiếu.'],
        ['Bảng Chi tiết', 'Table/Grid', 'Enable', 'Như trang Thêm', 'Có khi Lưu và duyệt', 'Dữ liệu hiện tại', 'Thêm / xoá dòng, sửa SL, ĐVT.'],
        ['Nút Lưu nháp / Lưu và duyệt / Quay lại', 'Button', 'Enable', '–', '–', '–', 'Như trang Thêm.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện khi phiếu Đang tạo và người xem là người lập.\nAfter:\n– Tải phiếu, nạp ĐVT và SL tồn.'],
        ['Bấm Lưu nháp', 'Click', 'Before:\n– Phiếu phải Đang tạo và do người dùng lập.\nDuring:\n– Kiểm như trang Thêm.\n' + TRUOC_LUU + '\nAfter:\n– Ghi thay đổi, thay toàn bộ dòng hàng; ghi nhận Thay đổi thông tin trong lịch sử.\n– Báo "Cập nhật thành công", về danh sách.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Về danh sách, không lưu.'],
    ],
})

# 2.8 Xem chi tiết --------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết phiếu', 'uc': 'uc_xem', 'uc_ten': 'FR-08 Xem chi tiết phiếu điều chuyển hàng',
    'qtc': 'Màn Xem chi tiết và Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết phiếu điều chuyển hàng'],
        ['Mô tả', 'Xem toàn bộ thông tin 1 phiếu ở chế độ chỉ đọc kèm khối Lịch sử; phiếu Đã hạch toán hiện thêm Đơn giá vốn, Thành tiền vốn. Nút ở chân trang khớp nút ở dòng danh sách.'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK + '\n2. Phiếu thuộc phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Bấm Số phiếu ở danh sách.\n2. Hệ thống mở trang "Chi tiết phiếu điều chuyển hàng: <số phiếu>": khối Thông tin chung (góc phải "<Người tạo> - <ngày giờ tạo>"), File đính kèm, Chi tiết (STT, Tên hàng hóa, Model, Mã hàng, SL chuyển, ĐVT, Đơn giá vốn, Thành tiền vốn, TK nợ, TK có), khối Lịch sử (thu gọn).'],
        ['Dòng sự kiện phụ', '• Phiếu Đang tạo của mình: chân trang có Sửa, In phiếu, Xóa, Quay lại.\n• Phiếu Đã hạch toán: chỉ In phiếu, Quay lại.\n• Phiếu ngoài phạm vi: báo "Bạn không có quyền xem phiếu này".'],
    ],
    'menu_them': ' => Số phiếu (liên kết)',
    'anh': [('17_detail', 'Trang Chi tiết phiếu Đã hạch toán: chỉ có In phiếu, Quay lại'),
            ('17c_detail_draft', 'Trang Chi tiết phiếu Đang tạo của mình: có Sửa, In phiếu, Xóa')],
    'ui': ui(UI6, [
        ['Kho vật lý, Kho xuất, Kho nhập, Ghi chú', 'Dropdown / Textarea', 'Read-only', 'Dữ liệu phiếu', 'Chỉ đọc.'],
        ['File đính kèm', 'File', 'Read-only', 'Dữ liệu phiếu', 'Xem trước / tải xuống; cột Dung lượng.'],
        ['Bảng Chi tiết', 'Table/Grid', 'Read-only', 'Dữ liệu phiếu', 'Đơn giá vốn, Thành tiền vốn định dạng 1,234,567.89; phiếu Đang tạo để trống.'],
        ['Khối Lịch sử', 'Label', 'Enable', 'Thu gọn', 'Bấm "Xem lịch sử" để mở (mục 2.13).'],
        ['Nút Sửa / Xóa', 'Button', 'Enable / Ẩn', 'Theo trạng thái', 'Chỉ hiện khi phiếu Đang tạo và người xem là người lập.'],
        ['Nút In phiếu', 'Button', 'Enable', 'Hiển thị', 'Mở bản xem trước (mục 2.10).'],
        ['Nút Quay lại', 'Button', 'Enable', '–', 'Về danh sách.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở trang', 'System', 'Before:\n– Kiểm tra phạm vi dữ liệu (BR-02).\nAfter:\n– Hiển thị phiếu, tính nút Sửa / Xóa theo trạng thái và người lập.'],
        ['Bấm Sửa / In phiếu / Xóa / Quay lại', 'Click', 'After:\n– Mở trang Sửa / bản xem trước / hộp Xác nhận xóa / về danh sách.'],
    ],
})

# 2.9 Xóa -------------------------------------------------------------------------
FR.append({
    'ten': 'Xóa phiếu Đang tạo', 'uc': 'uc_xoa', 'uc_ten': 'FR-09 Xóa phiếu điều chuyển hàng',
    'qtc': 'Quy tắc xóa và Thông báo.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xóa phiếu điều chuyển hàng'],
        ['Mô tả', 'Xóa hẳn 1 phiếu Đang tạo do chính mình lập, cùng các dòng hàng và tệp đính kèm. Phiếu Đang tạo chưa đụng tồn kho nên không có số liệu nào phải hoàn lại.'],
        ['Tác nhân', 'Người lập phiếu'],
        ['Điều kiện ban đầu', DK_NHAP],
        ['Dòng sự kiện chính', '1. Bấm Xóa ở cột Hành động (hoặc nút Xóa ở trang Chi tiết).\n2. Hệ thống hiện hộp "Xác nhận xóa": "Bạn có chắc chắn muốn xóa phiếu điều chuyển hàng <số phiếu>?"\n3. Bấm Xóa.\n4. Hệ thống xóa tệp đính kèm, các dòng hàng và phiếu.\n5. Báo "Xóa thành công", tải lại danh sách (từ trang Chi tiết: về danh sách).'],
        ['Dòng sự kiện phụ', '• Bấm Hủy / (x) → đóng hộp, không thay đổi.\n• Phiếu đã hạch toán / không phải người lập → "Phiếu đã hạch toán hoặc bạn không có quyền xóa", không xóa.\n• Xóa không ghi lịch sử (phiếu không còn).'],
    ],
    'menu_them': ' => Xóa {icon:btn_xoa}',
    'ghi_chu_layout': 'Modal Xác nhận xóa được mở ngay trên màn hình danh sách hoặc màn hình chi tiết phiếu theo đường dẫn ở trên.',
    'anh': [('13_delete', 'Hộp Xác nhận xóa phiếu')],
    'ui': ui(UI4, [
        ['Nút Xóa (cột Hành động / chân trang Chi tiết)', 'Button', 'Biểu tượng thùng rác; chỉ hiện khi phiếu Đang tạo và người xem là người lập.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận xóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc chắn muốn xóa phiếu điều chuyển hàng <số phiếu>?"'],
        ['Nút Xóa', 'Button', 'Xác nhận xóa.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không xóa.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Xóa', 'Click', 'After:\n– Hiện hộp Xác nhận xóa.'],
        ['Bấm Xóa trong hộp', 'Click', 'Before:\n– Phiếu phải Đang tạo và do người dùng lập.\nDuring:\n' + TRUOC_LUU + '\nAfter:\n– Xóa tệp đính kèm, dòng hàng, phiếu.\n– Báo "Xóa thành công", tải lại danh sách.'],
        ['Bấm Hủy / (x)', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.10 In phiếu ---------------------------------------------------------------------
FR.append({
    'ten': 'In phiếu', 'uc': 'uc_inphieu', 'uc_ten': 'FR-10 In phiếu điều chuyển hàng',
    'qtc': 'Quy tắc màn In và bố cục bản in.',
    'gioi_thieu': [
        ['Tên chức năng', 'In phiếu điều chuyển hàng'],
        ['Mô tả', 'Bản in 1 phiếu theo mẫu "PHIẾU ĐIỀU CHUYỂN HÀNG": tiêu đề công ty ghi trên phiếu, Số phiếu, Kho vật lý, Kho xuất, Kho nhập, Ghi chú, bảng hàng (STT, Tên hàng hóa, Model, Mã hàng hóa, SL chuyển, ĐVT, Đơn giá vốn, Thành tiền vốn, TK nợ, TK có), ô ký "Người lập" kèm tên người lập.'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK + '\n2. Phiếu thuộc phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Bấm In phiếu ở cột Hành động hoặc chân trang Chi tiết.\n2. Hệ thống mở cửa sổ "Xem trước phiếu <số phiếu>".\n3. Bấm In để mở hộp in của trình duyệt.'],
        ['Dòng sự kiện phụ', '• Không tìm thấy mẫu in: "Không tìm thấy mẫu in phiếu điều chuyển hàng".'],
    ],
    'menu_them': ' => In phiếu {icon:btn_inphieu}',
    'ghi_chu_layout': 'Cửa sổ Xem trước phiếu được mở ngay trên màn hình danh sách hoặc chi tiết theo đường dẫn ở trên.',
    'anh': [('19b_printitem', 'Cửa sổ Xem trước phiếu điều chuyển hàng')],
    'ui': ui(UI6, [
        ['Tiêu đề cửa sổ', 'Label', 'Read-only', '"Xem trước phiếu <số phiếu>"', '–'],
        ['Phần đầu bản in', 'Label', 'Read-only', 'Tiêu đề công ty', 'Theo công ty ghi trên phiếu (không theo người đang in).'],
        ['Nội dung bản in', 'Label', 'Read-only', 'Dữ liệu phiếu', 'Như mô tả; TK nợ, TK có = 156.'],
        ['Nút In', 'Button', 'Enable', '–', 'Mở hộp in của trình duyệt.'],
        ['Nút (x)', 'Button', 'Enable', '–', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In phiếu', 'Click', 'Before:\n– Kiểm tra phạm vi dữ liệu.\nAfter:\n– Dựng bản in từ mẫu, hiện xem trước.'],
        ['Bấm In', 'Click', 'After:\n– Mở hộp in của trình duyệt.'],
    ],
})

# 2.11 In danh sách ----------------------------------------------------------------
FR.append({
    'ten': 'In danh sách', 'uc': 'uc_in', 'uc_ten': 'FR-11 In danh sách phiếu',
    'qtc': 'Quy tắc màn In và bố cục bản in.',
    'gioi_thieu': [
        ['Tên chức năng', 'In danh sách phiếu điều chuyển hàng'],
        ['Mô tả', 'In danh sách đang lọc theo mẫu "DANH SÁCH PHIẾU ĐIỀU CHUYỂN HÀNG", khổ ngang, 9 cột: STT, Số phiếu, Ngày hạch toán, Kho vật lý, Kho xuất, Kho nhập, Người lập, Ngày lập, Trạng thái.'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm In danh sách.\n2. Hệ thống mở cửa sổ "Xem trước danh sách phiếu điều chuyển hàng" với mọi dòng khớp bộ lọc (trong phạm vi dữ liệu).\n3. Bấm In.'],
        ['Dòng sự kiện phụ', '• Vượt 2,000 dòng: không in, báo "Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được…" (BR-11).'],
    ],
    'menu_them': ' => In danh sách {icon:btn_indanhsach}',
    'ghi_chu_layout': 'Cửa sổ Xem trước bản in được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('19_printlist', 'Cửa sổ xem trước bản in danh sách')],
    'ui': ui(UI6, [
        ['Tiêu đề cửa sổ', 'Label', 'Read-only', '"Xem trước danh sách phiếu điều chuyển hàng"', '–'],
        ['Bảng in', 'Table/Grid', 'Read-only', 'Theo bộ lọc', '9 cột cố định của mẫu in.'],
        ['Nút In', 'Button', 'Enable', '–', 'Mở hộp in của trình duyệt.'],
        ['Nút (x)', 'Button', 'Enable', '–', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In danh sách', 'Click', 'After:\n– Dựng bản in theo bộ lọc; vượt 2,000 dòng thì chỉ hiện câu nhắc.'],
        ['Bấm In', 'Click', 'After:\n– Mở hộp in của trình duyệt.'],
    ],
})

# 2.12 Xuất Excel ----------------------------------------------------------------
FR.append({
    'ten': 'Xuất Excel danh sách', 'uc': 'uc_xuat', 'uc_ten': 'FR-12 Xuất Excel danh sách phiếu',
    'qtc': 'Quy tắc Excel và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách phiếu ra Excel'],
        ['Mô tả', 'Xuất mọi dòng khớp bộ lọc (không chỉ trang đang xem) ra file Danh-sach-phieu-dieu-chuyen-hang-<yyyy-mm-dd>.xlsx, tiêu đề "DANH SÁCH PHIẾU ĐIỀU CHUYỂN HÀNG", cột theo lựa chọn và thứ tự người dùng.'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất file", tích sẵn các cột đang hiện trên bảng.\n3. Người dùng tích / bỏ, kéo ☰ đổi thứ tự, bấm Xuất file.\n4. Hệ thống tải dữ liệu theo lô (nút hiện tiến độ "Đang tải x/y..."), dựng file và tải về; báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Không có dòng nào khớp → "Không có dữ liệu để xuất", không tải file.'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất file')],
    'ui': ui(UI8, [
        ['Danh sách trường', 'Checkbox', 'Enable', '9 trường', 'Có (≥ 1)', 'Các cột đang hiện', 'Số phiếu, Ngày hạch toán, Kho vật lý, Kho xuất, Kho nhập, Người tạo, Ngày tạo, Trạng thái, Ghi chú. Kéo ☰ đổi thứ tự.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', 'Chọn / bỏ nhanh mọi trường.'],
        ['Dòng đếm', 'Label', 'Read-only', '–', '–', '–', '"Đang chọn x/9 trường".'],
        ['Nút Xuất file / Đóng', 'Button', 'Enable', '–', '–', '–', 'Xuất file / đóng không xuất.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất file', 'Click', 'After:\n– Tải dữ liệu theo bộ lọc + phạm vi, dựng file đúng thứ tự cột, tải về; báo kết quả.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.13 Lịch sử ---------------------------------------------------------------------
FR.append({
    'ten': 'Xem lịch sử thay đổi',
    'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem lịch sử thay đổi phiếu'],
        ['Mô tả', 'Liệt kê các lần thao tác trên 1 phiếu (Tạo mới, Thay đổi thông tin, Thay đổi trạng thái), mới nhất ở trên, kèm người thực hiện, phòng ban, thời điểm và giá trị cũ → mới của Kho vật lý, Kho xuất, Kho nhập, Ghi chú, File đính kèm, Trạng thái, Danh sách hàng hóa (thêm mới / đã xóa / sửa số lượng, ĐVT).'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK + '\n2. Phiếu thuộc phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Bấm Lịch sử ở cột Hành động → cửa sổ "Lịch sử thay đổi".\n2. Hoặc ở trang Chi tiết bấm "Xem lịch sử" ở khối Lịch sử.\n3. Hệ thống liệt kê các mốc; nút Bộ lọc (loại hoạt động, người thực hiện, khoảng ngày).'],
        ['Dòng sự kiện phụ', '• Phiếu lập trước khi có màn này không có mốc lịch sử.\n• Giá trị cũ in đỏ, giá trị mới in xanh.'],
    ],
    'menu_them': ' => Lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': 'Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối Lịch sử nằm cuối trang Chi tiết phiếu.',
    'anh': [('16_history', 'Cửa sổ Lịch sử thay đổi mở từ danh sách'), ('17b_detail_history', 'Khối Lịch sử ở trang Chi tiết')],
    'ui': ui(UI6, [
        ['Tiêu đề', 'Label', 'Read-only', '"Lịch sử thay đổi …<số phiếu>"', '–'],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Lọc theo loại hoạt động (Tạo mới / Thay đổi thông tin / Thay đổi trạng thái), người thực hiện, Từ ngày, Đến ngày.'],
        ['Mốc lịch sử', 'Label', 'Read-only', 'Mới nhất trên cùng', 'Thời điểm, tên hành động, "Người thực hiện: <họ tên> — <phòng ban>", danh sách trường đổi: cũ → mới.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lịch sử / Xem lịch sử', 'Click', 'After:\n– Tải và hiển thị các mốc lịch sử của phiếu.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

FR_NAMES = ['FR-%02d %s' % (i + 1, f['ten']) for i, f in enumerate(FR)]
LAP_IDX = (3, 4, 5)       # lập, chọn hàng, lưu và duyệt
NGUOI_LAP_IDX = (6, 8)    # sửa, xóa: chỉ người lập, phiếu Đang tạo


def _mt(i):
    if i in LAP_IDX:
        return ['Có', 'Không']
    if i in NGUOI_LAP_IDX:
        return ['Có (phiếu Đang tạo do mình lập)', 'Có (phiếu Đang tạo do mình lập)']
    return ['Có', 'Có (theo phạm vi)']


S = {
    'ten': TEN, 'ten_ngan': 'phiếu điều chuyển hàng', 'phan_he': 'Tài chính',
    'menu': [('Tài chính', 'menu_phanhe'), ('Hàng hoá - Dịch vụ - Vận chuyển', 'menu_nhom'), ('Điều chuyển', 'menu_nhom2'),
             (TEN, 'menu_muc')],
    'muc_dich': [
        'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho việc ĐIỀU CHUYỂN HÀNG giữa 2 kho kế toán trong cùng 1 kho vật lý (hàng không di chuyển thực tế, chỉ đổi kho hạch toán).',
        'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
        'Làm rõ luồng 2 trạng thái Đang tạo → Đã hạch toán và thời điểm phiếu tác động tồn kho, giá vốn, sổ kế toán.',
        'Làm rõ phạm vi dữ liệu: quyền xem tổng công ty / công ty / chỉ phiếu mình lập; phiếu Đang tạo chỉ người lập thấy.',
    ],
    'thuat_ngu': [
        ['Kho vật lý', 'Kho thực tế chứa hàng (vd PTT - Phan Trọng Tuệ). Một kho vật lý có nhiều kho kế toán.'],
        ['Kho kế toán', 'Kho dùng để hạch toán tồn trong một kho vật lý (vd Hàng bán, Hàng khuyến mại, Hàng khách gửi).'],
        ['Kho xuất / Kho nhập', 'Kho kế toán bị trừ tồn / được cộng tồn khi phiếu hạch toán.'],
        ['SL tồn', 'Số lượng có thể chuyển của hàng ở kho xuất, quy theo ĐVT đang chọn.'],
        ['Hạch toán', 'Bước ghi nhận phiếu vào số liệu: trừ / cộng tồn kế toán, tính giá vốn, ghi bút toán Nợ 156 / Có 156.'],
        ['Giá vốn (Đơn giá vốn)', 'Giá trị xuất kho của 1 đơn vị, tính theo phương pháp nhập trước – xuất trước từ các lớp nhập của kho xuất.'],
        ['TK 156', 'Tài khoản hàng hóa — cả 2 vế của bút toán điều chuyển nội bộ.'],
        ['Kế toán kho', 'Quyền cho phép lập, sửa, xóa, hạch toán phiếu điều chuyển hàng.'],
    ],
    'trang_thai': {
        'cau_dan': 'Phiếu có 2 trạng thái. Không có bước gửi duyệt / từ chối / hủy: người lập bấm "Lưu và duyệt" là hạch toán ngay. '
                   'Trạng thái do nút lưu quyết định, form không có ô chọn trạng thái.',
        'rows': [
            ['Đang tạo', 'Phiếu nháp: đã lưu thông tin, CHƯA trừ / cộng tồn, chưa ghi sổ. Chỉ người lập nhìn thấy.', 'Xem, Sửa, Xóa, Lưu và duyệt, In phiếu, Lịch sử', 'Người lập (có quyền "%s")' % Q_LAP],
            ['Đã hạch toán', 'Đã trừ tồn kho xuất, cộng tồn kho nhập, tính giá vốn, ghi bút toán Nợ 156 / Có 156; có Ngày hạch toán. Khóa vĩnh viễn.', 'Xem, In phiếu, In danh sách, Xuất Excel, Lịch sử (không Sửa, Xóa, Hủy)', 'Người có quyền "%s" bấm Lưu và duyệt' % Q_LAP],
            ['Đã xóa', 'Phiếu Đang tạo bị xóa hẳn cùng dòng hàng và tệp.', '–', 'Người lập, chỉ từ trạng thái Đang tạo'],
        ],
        'anh': 'state_flow',
        'ghi_chu': ['Bấm "Lưu và duyệt" ngay ở trang Thêm thì phiếu đi thẳng tới Đã hạch toán, không dừng ở Đang tạo.',
                    'Phiếu Đã hạch toán không có thao tác hủy hay đảo bút toán; muốn đưa hàng về kho cũ thì lập phiếu điều chuyển ngược chiều.'],
    },
    'quyen_truoc': ['Nhóm quyền thao tác (gán ở màn Phân quyền, dùng chung tên quyền với hệ thống kho):'],
    'quyen_rows': [
        [Q_LAP, 'Thấy nút Tạo mới; lập, Lưu nháp, Lưu và tiếp tục, Lưu và duyệt (hạch toán). Sửa / Xóa chỉ áp cho phiếu Đang tạo do chính mình lập.'],
        ['(Mọi người dùng đăng nhập)', 'Vào màn qua menu, xem danh sách, tìm kiếm, xem chi tiết, lịch sử, in, xuất Excel, tuỳ chỉnh cột — trong phạm vi dữ liệu.'],
    ],
    'pham_vi_truoc': ['Nhóm quyền quyết định phạm vi dữ liệu (xét theo thứ tự từ trên xuống, có quyền nào trước thì áp quyền đó):'],
    'pham_vi_rows': [
        ['1', 'Quản trị hệ thống hoặc "%s"' % Q_TCT, 'Phiếu Đã hạch toán của mọi công ty + phiếu Đang tạo do chính mình lập.'],
        ['2', Q_CT, 'Phiếu Đã hạch toán của công ty đang làm việc của người dùng + phiếu Đang tạo do chính mình lập.'],
        ['3', '(không có quyền nào ở trên)', 'Chỉ phiếu do chính người dùng lập.'],
    ],
    'pham_vi_sau': ['Công ty của phiếu = công ty của người lập tại thời điểm lập. Phiếu Đang tạo của người khác KHÔNG hiện với bất kỳ ai (BR-02). '
                    'Phạm vi áp như nhau cho danh sách, chi tiết, in, xuất Excel và lịch sử; mở thẳng phiếu ngoài phạm vi thì báo "Bạn không có quyền xem phiếu này".'],
    'ma_tran': [['Chức năng', 'Có quyền "%s"' % Q_LAP, 'Không có quyền "%s"' % Q_LAP]] + [
        [f] + _mt(i) for i, f in enumerate(FR_NAMES)],
    'ma_tran_widths': [2.8, 1.9, 1.9],
    'quyen_sau': ['Phạm vi dữ liệu của mọi chức năng theo bảng quyền phạm vi ở trên.'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Điều chuyển trong cùng 1 kho vật lý', ['– Kho xuất và Kho nhập phải là kho kế toán thuộc Kho vật lý của phiếu, đang hoạt động, thuộc công ty người lập.', '– Kho đã khóa mà phiếu cũ đang dùng vẫn hiện khi xem / sửa phiếu đó.'], ['Lập phiếu', 'Sửa']),
        ('BR-02', 'Phạm vi dữ liệu', ['– Xét lần lượt: quản trị / quyền tổng công ty → quyền công ty → chỉ phiếu mình lập.', '– Phiếu Đang tạo chỉ người lập thấy, kể cả với người có quyền xem rộng.'], ['Mọi chức năng']),
        ('BR-03', 'Số phiếu', ['– Dạng PDCH-<số thứ tự 5 chữ số>, theo số thứ tự bản ghi; sinh khi lưu lần đầu, không đổi về sau.'], ['Lập phiếu']),
        ('BR-04', 'Hạch toán chỉ 1 lần', ['– "Lưu và duyệt" chuyển phiếu sang Đã hạch toán và khóa vĩnh viễn; không có hủy / đảo bút toán.'], ['Lưu và duyệt']),
        ('BR-05', 'Sửa / xóa', ['– Chỉ phiếu Đang tạo, chỉ người lập. Nút ẩn khi không đủ điều kiện; hệ thống chặn cả khi gửi yêu cầu trực tiếp ("Phiếu đã hạch toán hoặc bạn không có quyền sửa / xóa").'], ['Sửa', 'Xóa', 'Xem chi tiết']),
        ('BR-06', 'Trường bắt buộc theo nút lưu', ['– Lưu nháp / Lưu và tiếp tục: chỉ bắt buộc Kho vật lý; SL đã nhập phải > 0.', '– Lưu và duyệt: bắt buộc Kho vật lý, Kho xuất, Kho nhập, ít nhất 1 dòng hàng ("Phiếu phải có ít nhất một dòng hàng hóa"), mỗi dòng có SL > 0 và ĐVT.'], ['Lập phiếu', 'Sửa', 'Lưu và duyệt']),
        ('BR-07', 'Không trùng', ['– Kho xuất ≠ Kho nhập ("Kho xuất, kho nhập không được trùng nhau").', '– Một hàng + ĐVT chỉ xuất hiện 1 dòng ("Hàng hóa bị trùng trong phiếu"); thêm hàng đã có từ cửa sổ chọn thì bị bỏ qua.'], ['Lập phiếu', 'Sửa']),
        ('BR-08', 'Kiểm tồn khi lưu', ['– SL tồn = min(tồn có thể dùng của công ty, tồn kế toán kho xuất, tồn kho vật lý); kho xuất là kho khuyến mại thì = min(tồn kho xuất, tồn khuyến mại). Quy theo hệ số ĐVT, giữ 3 chữ số thập phân.', '– SL chuyển vượt SL tồn → báo đỏ dưới ô "Số lượng chuyển vượt quá số lượng tồn (còn <n>)", không tự sửa số; áp cho cả Lưu nháp khi đã chọn kho xuất.', '– Hàng đang kiểm kho tại kho vật lý → "Hàng hóa đang được kiểm kho, không thể điều chuyển".'], ['Lập phiếu', 'Sửa', 'Lưu và duyệt']),
        ('BR-09', 'Tài khoản cố định', ['– TK nợ = TK có = 156 trên form, bản in và bút toán.'], ['Lập phiếu', 'In phiếu', 'Lưu và duyệt']),
        ('BR-10', 'Tác động số liệu khi hạch toán', ['– Kho xuất: tồn kế toán − (SL × hệ số ĐVT); tồn kế toán của kho vật lý giảm tương ứng; nhật ký tồn ghi giá trị trước / sau.', '– Kho nhập: tồn kế toán + (SL × hệ số); chưa có dòng tồn thì tạo mới; lớp nhập mang giá vốn của dòng xuất.', '– Đơn giá vốn = (giá trị tồn trước − giá trị tồn sau) / SL quy đổi; SL 0 thì giá vốn 0.', '– Bút toán: mỗi dòng có Thành tiền vốn > 0 ghi 1 cặp Nợ 156 / Có 156, chứng từ = Số phiếu, ngày hạch toán = thời điểm duyệt, tổ chức = của phiếu.'], ['Lưu và duyệt']),
        ('BR-11', 'In và xuất', ['– In danh sách và xuất Excel theo đúng bộ lọc đang áp dụng (mọi trang); in danh sách tối đa 2,000 dòng.', '– Bản in phiếu lấy tiêu đề theo công ty ghi trên phiếu, ô ký có tên người lập.'], ['In phiếu', 'In danh sách', 'Xuất Excel']),
        ('BR-12', 'Thao tác xong quay về danh sách', ['– Lưu nháp, Lưu và duyệt, Cập nhật và Xóa ở trang Chi tiết xong thì về màn danh sách (trừ "Lưu và tiếp tục").'], ['Lập phiếu', 'Sửa', 'Xóa']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây đọc hoặc dùng dữ liệu do Phiếu điều chuyển hàng ghi ra khi hạch toán (tồn kế toán theo kho, nhật ký tồn / giá vốn, bút toán) hoặc tham chiếu tới phiếu.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Kế toán kho / Người xem phiếu',
    'mains': [('FR-01', 'Xem danh sách phiếu', 'view'), ('FR-04', 'Lập phiếu (Lưu nháp)', 'crud'),
              ('FR-06', 'Lưu và duyệt (hạch toán)', 'action'), ('FR-07', 'Sửa phiếu Đang tạo', 'crud'),
              ('FR-09', 'Xóa phiếu Đang tạo', 'action'), ('FR-11', 'In danh sách', 'io'), ('FR-12', 'Xuất Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc', 'view'), ('FR-03', 'Cài đặt bộ lọc, tuỳ chỉnh cột', 'view'),
             ('FR-08', 'Xem chi tiết phiếu', 'view'), ('FR-10', 'In phiếu', 'io'), ('FR-13', 'Xem lịch sử', 'view')],
    'rieng': [('FR-04', 'Lập phiếu điều chuyển hàng', 'crud', 'uc_them'), ('FR-05', 'Chọn hàng hóa vào phiếu', 'crud', 'uc_chonhang'),
              ('FR-06', 'Lưu và duyệt phiếu', 'action', 'uc_duyet'), ('FR-07', 'Sửa phiếu', 'crud', 'uc_sua'),
              ('FR-08', 'Xem chi tiết phiếu', 'view', 'uc_xem'), ('FR-09', 'Xóa phiếu', 'action', 'uc_xoa'),
              ('FR-10', 'In phiếu', 'io', 'uc_inphieu'), ('FR-11', 'In danh sách', 'io', 'uc_in'),
              ('FR-12', 'Xuất Excel danh sách', 'io', 'uc_xuat')],
}

STATES = [('start', '', None), ('dt', 'Đang tạo', '#e2e8f0'), ('ht', 'Đã hạch toán', '#dcfce7'), ('end', '', None)]
TRANS = [('start', 'dt', 'Lưu nháp'), ('dt', 'ht', 'Lưu và duyệt (kể cả ngay khi lập)'), ('dt', 'end', 'Xóa')]

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    L.draw_state_flow(os.path.join(scr.uml, 'state_flow.png'), STATES, TRANS)
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))

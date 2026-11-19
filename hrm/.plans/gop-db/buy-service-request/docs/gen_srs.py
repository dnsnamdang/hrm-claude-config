# -*- coding: utf-8 -*-
"""SRS - Yêu cầu mua dịch vụ (STT 63) — khuôn PHIẾU đợt 3 (chép finance-declare-debt-beginning/docs/kh/gen_srs.py).

Nguồn (code HRM develop origin/develop, 02/11/2026):
  FE hrm-client/pages/finance/buy-service-requests/{index, create, _id/index, _id/edit}.vue,
     components/{BuyServiceRequestForm, BuyServiceDetailTable, CommentModal}.vue, components/subsystem-menu/sale-hub.js
  BE Modules/Finance: Entities/BuyServiceRequest/{BuyServiceRequest, BuyServiceRequestDetail}.php,
     Services/{BuyServiceRequestService, BuyServiceRequestNotifyService}.php, Http/Controllers/V1/BuyServiceRequestController.php,
     Http/Requests/BuyServiceRequest/{BuyServiceRequestStoreRequest, BuyServiceRequestApproveRequest}.php,
     Database/Seeders/BuyServiceRequestPermissionSeeder.php, Http/Middleware/CheckDueConfig.php, Routes/api.php;
     app/Services/CatalogHistoryService.php, app/ExcelExport/ExportColumnRegistry.php
  Ảnh: capture.js (dev-hrm). Sơ đồ trạng thái: _state_flow.py (2 hàng, viết riêng). Phần 5: dò code FE/BE 02/11/2026.
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
sys.path.insert(0, HERE)
import _lib_phieu as L  # noqa: E402
from _lib_phieu import ui, UI4, UI4W, UI6, UI6W, UI7, UI7W, UI8, UI8W, TRUOC_LUU  # noqa: E402,F401
import _state_flow  # noqa: E402

TEN = 'Yêu cầu mua dịch vụ'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q_TP = 'Trưởng phòng duyệt yêu cầu mua dịch vụ'
Q_KS = 'Ban kiểm soát duyệt giá mua dịch vụ'
Q_ALL = 'Xem yêu cầu mua dịch vụ - theo tổng công ty'
Q_CTY = 'Xem yêu cầu mua dịch vụ - theo công ty'
Q_PB = 'Xem yêu cầu mua dịch vụ - theo phòng ban'
NV = 'Mọi nhân viên đăng nhập (không cần quyền riêng)'
LAP = 'Người lập phiếu'
DK = '1. Người dùng đăng nhập thành công.'
DK_LAP = DK + '\n2. Người dùng là người lập phiếu.\n3. Phiếu ở trạng thái %s.'
DK_PV = DK + '\n2. Phiếu thuộc phạm vi dữ liệu của người dùng (Phần 2).'
POPUP = 'Modal %s được mở ngay trên màn hình %s theo đường dẫn ở trên.'
VE_DS = 'Báo "%s", quay về màn danh sách.'
TONG_GIA = '3 dòng tổng: Thành tiền, VAT (x%), Tổng thanh toán'

P5 = [
    ('Bán hàng', 'YC hạch toán mua dịch vụ (bảng dịch vụ hiện số phiếu yêu cầu mua dịch vụ gốc, bấm mở trang Chi tiết phiếu)',
     'Bán hàng => Yêu cầu => Mua dịch vụ => YC hạch toán mua dịch vụ'),
    ('Bán hàng', 'Hạch toán mua dịch vụ (bảng dịch vụ hiện số phiếu yêu cầu mua dịch vụ gốc, bấm mở trang Chi tiết phiếu)',
     'Bán hàng => Yêu cầu => Mua dịch vụ => Hạch toán mua dịch vụ'),
    ('Tài chính', 'Yêu cầu hạch toán mua dịch vụ (cùng màn trên, lối vào phân hệ Tài chính)',
     'Tài chính => Mua dịch vụ => Yêu cầu hạch toán mua dịch vụ'),
    ('Tài chính', 'Hạch toán mua dịch vụ (cùng màn trên, lối vào phân hệ Tài chính)',
     'Tài chính => Mua dịch vụ => Hạch toán mua dịch vụ'),
    ('Chung', 'Thông báo (biểu tượng chuông): thông báo "[YCMDV] …" khi gửi duyệt, chờ Ban kiểm soát duyệt giá, xin duyệt lại giá, '
              'từ chối — bấm mở trang Chi tiết phiếu', 'Thanh tiêu đề => Thông báo'),
]

FR = []

# 2.1 Xem danh sách ---------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách yêu cầu mua dịch vụ',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách yêu cầu mua dịch vụ'],
        ['Mô tả', 'Hiển thị các phiếu yêu cầu mua dịch vụ trong phạm vi dữ liệu của người dùng, có phân trang, sắp xếp, nhãn trạng thái màu và nút thao tác theo từng phiếu.'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), phiếu tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Không có phiếu khớp → bảng hiện "Không có dữ liệu phù hợp."\n• Phạm vi dữ liệu theo quyền xem (Phần 2, BR-02); phiếu Đang tạo chỉ người lập thấy (BR-03).\n• Nút ở cột Hành động hiện theo trạng thái phiếu và vai trò người xem (BR-05); nút không dùng được thì ẩn.'],
    ],
    'anh': [('01_list', 'Màn danh sách Yêu cầu mua dịch vụ lúc mới truy cập'),
            ('01b_list_actions', 'Cột Hành động theo trạng thái: Đang tạo (Sửa, Xóa), Chờ TP duyệt (Trưởng phòng duyệt), Đã duyệt của người lập (Yêu cầu duyệt lại giá, Hủy yêu cầu…)'),
            ('01c_row_menu', 'Menu "Hành động khác" (…) của một dòng')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Yêu cầu mua dịch vụ', 'Tiêu đề khối danh sách và tiêu đề trang.'],
        ['Nút Tạo mới', 'Button', 'Enable', 'Hiển thị', 'Mở trang "Tạo phiếu yêu cầu mua dịch vụ" (mục 2.4). Mọi nhân viên đều dùng được.'],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất file" (mục 2.16).'],
        ['Nút In danh sách', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ xem trước bản in danh sách (mục 2.15).'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.3).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa, không ẩn được.'],
        ['Cột Số phiếu', 'Table/Grid', 'Read-only', 'Hiển thị', '- Dạng <mã công ty>.YCMDV.<năm><6 chữ số> (BR-04).\n- Sắp xếp được. Dạng liên kết: bấm mở trang Chi tiết (mục 2.6), chuột phải mở tab mới được.\n- Cột khóa, không ẩn được.'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Ngày nhận đơn', 'Table/Grid', 'Read-only', 'Hiển thị', 'Thời điểm Trưởng phòng duyệt; chưa duyệt để trống. Sắp xếp được.'],
        ['Cột Ngày duyệt giá', 'Table/Grid', 'Read-only', 'Hiển thị', 'Thời điểm Ban kiểm soát duyệt giá; chưa duyệt để trống. Sắp xếp được.'],
        ['Cột Người yêu cầu', 'Table/Grid', 'Read-only', 'Hiển thị', '"Họ tên - Mã phòng ban" của người lập.'],
        ['Cột Phòng yêu cầu', 'Table/Grid', 'Read-only', 'Hiển thị', 'Phòng ban ghi trên phiếu lúc lập (nhân viên chuyển phòng thì phiếu cũ vẫn giữ phòng cũ).'],
        ['Cột Người duyệt giá', 'Table/Grid', 'Read-only', 'Hiển thị', 'Họ tên người Ban kiểm soát đã duyệt giá.'],
        ['Cột Công ty', 'Table/Grid', 'Read-only', 'Hiển thị', 'Công ty ghi trên phiếu.'],
        ['Cột Ghi chú, Ý kiến Trưởng phòng, Ý kiến Ban kiểm soát', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tối đa 2 dòng, rê chuột xem đủ nội dung. Ô rỗng để trống.'],
        ['Cột Người cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', '"Họ tên - Mã phòng ban" người thao tác gần nhất.'],
        ['Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Có biểu tượng sắp xếp.'],
        ['Cột Trạng thái', 'Table/Grid', 'Read-only', 'Hiển thị', 'Nhãn màu: Đang tạo (xám), Chờ TP duyệt / Chờ KS duyệt / Đang lập hợp đồng (vàng), Đã duyệt / Đã lập hợp đồng (xanh), Không duyệt / Hủy (đỏ).'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- 2 nút đầu hiện thẳng, các nút còn lại trong menu "…": Sửa, Xóa, Trưởng phòng duyệt, Kiểm soát duyệt giá, Yêu cầu duyệt lại giá, Hủy yêu cầu, Lập hợp đồng mua dịch vụ (điều kiện từng nút: BR-05), In phiếu, Lịch sử (luôn có).\n- Sửa → trang Sửa; In phiếu, Lịch sử → mở cửa sổ ngay tại chỗ; các nút đổi trạng thái và Xóa → mở trang Chi tiết để thao tác.\n- Cột khóa, không ẩn được.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Người dùng đã đăng nhập (mục menu không gắn quyền).\nAfter:\n– Tải trang 1 theo phạm vi dữ liệu (BR-02, BR-03), phiếu tạo gần nhất trên cùng; khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút).'],
        ['Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại dữ liệu.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp, tải lại dữ liệu; đổi số dòng thì quay về trang 1.'],
        ['Bấm Số phiếu', 'Click', 'After:\n– Mở trang Chi tiết phiếu (mục 2.6).'],
        ['Bấm nút ở cột Hành động', 'Click', 'After:\n– Sửa: mở trang Sửa (mục 2.5).\n– In phiếu: mục 2.14. Lịch sử: mục 2.17. Lập hợp đồng mua dịch vụ: mục 2.13.\n– Xóa, Trưởng phòng duyệt, Kiểm soát duyệt giá, Yêu cầu duyệt lại giá, Hủy yêu cầu: mở trang Chi tiết, người dùng bấm nút tương ứng ở chân trang.'],
    ],
})

# 2.2 Tìm kiếm và lọc -------------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc danh sách',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách yêu cầu mua dịch vụ'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao.'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập số phiếu rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô gõ chữ (tìm nhanh, Số phiếu, Tên dịch vụ) chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Bấm Làm mới → xoá mọi điều kiện và tải lại danh sách.\n• Ô Công ty / Phòng ban hiện theo phạm vi xem của người dùng.\n• Hệ thống ghi nhớ bộ lọc 10 phút khi rời màn rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực Tìm kiếm nâng cao ở trạng thái mở')],
    'ui': ui(UI7, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Tìm theo số phiếu".'],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Áp dụng từ khóa và các ô lọc.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá mọi điều kiện lọc và tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực ô lọc (khi mở, nút đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" (mục 2.3).'],
        ['Ô Công ty – Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Theo phạm vi xem', 'Trống', '- Công ty: người có quyền xem theo tổng công ty.\n- Phòng ban: chọn trong phạm vi được xem.\n- Lọc theo công ty / phòng ban ghi trên phiếu.'],
        ['Ô Số phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Tìm gần đúng theo số phiếu; lọc khi Enter / Tìm kiếm.'],
        ['Ô Tên dịch vụ', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Tìm gần đúng theo tên dịch vụ trên các dòng dịch vụ của phiếu; lọc khi Enter / Tìm kiếm.'],
        ['Ô Trạng thái', 'Dropdown', 'Enable', '8 trạng thái', 'Trống', 'Đang tạo, Chờ TP duyệt, Chờ KS duyệt, Đã duyệt, Đang lập hợp đồng, Đã lập hợp đồng, Không duyệt, Hủy.'],
        ['Ô Người duyệt giá', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc phiếu do người được chọn duyệt giá.'],
        ['Ô Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc phiếu do người được chọn lập.'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy, Từ → Đến', 'Trống', 'Lọc theo ngày tạo phiếu, tính trọn cả 2 ngày đầu mút.'],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm Tìm kiếm / nhấn Enter ở ô gõ chữ', 'Click', 'After:\n– Áp đồng thời từ khóa và các ô lọc, tải lại bảng từ trang 1.'],
        ['Chọn giá trị ở ô chọn', 'Change', 'After:\n– Tải lại bảng từ trang 1 ngay.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khu vực ô lọc.'],
    ],
})

# 2.3 Cài đặt bộ lọc / tùy chỉnh cột ---------------------------------------------
FR.append({
    'ten': 'Cài đặt bộ lọc và tuỳ chỉnh cột',
    'qtc': 'Bộ lọc, Cấu hình cột và lưu cấu hình theo người dùng.',
    'gioi_thieu': [
        ['Tên chức năng', 'Cài đặt bộ lọc và tuỳ chỉnh cột'],
        ['Mô tả', 'Người dùng chọn ô lọc nào hiển thị / thứ tự ô lọc, và cột nào hiển thị / thứ tự cột trên bảng. Cấu hình lưu theo từng người dùng, từng màn.'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Bấm "Cài đặt bộ lọc" (hoặc biểu tượng Cấu hình cột hiển thị).\n2. Tích / bỏ tích, kéo ☰ để đổi thứ tự.\n3. Bấm Lưu: hệ thống lưu cấu hình và áp dụng ngay.'],
        ['Dòng sự kiện phụ', '• Bấm Đóng: bỏ thay đổi.\n• Cài đặt bộ lọc có nút "Khôi phục mặc định".\n• Cột STT, Số phiếu, Hành động không bỏ được (có biểu tượng khóa).'],
    ],
    'menu_them': ' => Cài đặt bộ lọc {icon:btn_caidatboloc} / Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': 'Modal Cài đặt bộ lọc và Modal Tuỳ chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('26_filtercfg', 'Cửa sổ Cài đặt bộ lọc'), ('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột')],
    'ui': ui(UI6, [
        ['Danh sách ô lọc', 'Checkbox', 'Enable', 'Đủ 7 ô', 'Công ty – Phòng ban, Số phiếu, Tên dịch vụ, Trạng thái, Người duyệt giá, Người tạo, Ngày tạo. Kéo ☰ đổi thứ tự.'],
        ['Nút Khôi phục mặc định', 'Button', 'Enable', '–', 'Đưa cấu hình ô lọc về mặc định.'],
        ['Danh sách cột', 'Checkbox', 'Enable', '16/16 cột', 'Tích cột muốn hiện; STT, Số phiếu bị khóa. "Đang chọn x/16 cột".'],
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

# 2.4 Lập phiếu ------------------------------------------------------------------
FORM_UI = [
    ['Người tạo - ngày giờ', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại', 'Góc phải khối Thông tin chung.'],
    ['Ghi chú', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống', 'Nội dung đề nghị mua dịch vụ. Bỏ trống: "Bắt buộc phải nhập"; quá dài: "Vui lòng nhập tối đa 255 ký tự."'],
    ['Khối File đính kèm / nút Thêm tài liệu', 'File', 'Enable', 'pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip; ≤ 10 MB/file', 'Có khi Gửi duyệt', 'Trống', '- Bảng STT, Upload / File, Dung lượng; mỗi file có nút xem, tải, thay, xoá.\n- Gửi duyệt mà chưa có file: "Bắt buộc phải nhập" (BR-06).'],
    ['Nút Thêm dòng', 'Button', 'Enable', '–', '–', '–', 'Thêm 1 dòng dịch vụ trống. Mở trang Tạo đã có sẵn 1 dòng.'],
    ['Cột Tên dịch vụ', 'Dropdown', 'Enable', 'Mã phí loại "Dịch vụ sửa chữa & chi phí khác" đang hoạt động', 'Có khi Gửi duyệt', 'Trống', 'Bỏ trống: "Bắt buộc phải nhập".'],
    ['Cột ĐVT', 'Label', 'Read-only', '–', '–', 'Gói', 'Cố định "Gói".'],
    ['Cột Số lượng', 'Number', 'Enable', 'Số ≥ 0', 'Có khi Gửi duyệt', '0', 'Hiển thị 1,234,567.89.'],
    ['Cột Giá đề xuất mua trước VAT', 'Number', 'Enable', 'Số ≥ 0', 'Có khi Gửi duyệt', '0', 'Hiển thị 1,234,567.89.'],
    ['Cột Thành tiền đề xuất', 'Label', 'Read-only', '–', '–', '0', 'Tự tính = Số lượng × Giá đề xuất, không gõ tay.'],
    ['Cột Nhà cung cấp', 'Dropdown', 'Enable', 'Nhà cung cấp đang hoạt động', 'Không', 'Trống', 'Mở là thấy 50 nhà cung cấp đầu, gõ mã / tên để tìm; hiển thị "Mã - Tên".'],
    ['Nút Xóa dòng', 'Button', 'Enable', '–', '–', '–', 'Biểu tượng thùng rác cuối dòng; bỏ dòng khỏi bảng.'],
    ['Dòng Thành tiền / VAT (%) / Tổng thanh toán', 'Number', 'Enable (ô VAT)', 'VAT 0–100', 'Không', 'VAT 0', '- Thành tiền = tổng Thành tiền đề xuất; VAT = Thành tiền × VAT %; Tổng thanh toán = Thành tiền + VAT.\n- VAT > 100: "Không được lớn hơn 100."'],
    ['Nút Lưu nháp', 'Button', 'Enable', '–', '–', '–', 'Lưu ở trạng thái Đang tạo rồi về danh sách.'],
    ['Nút Gửi duyệt', 'Button', 'Enable', '–', '–', '–', 'Lưu và chuyển Chờ TP duyệt rồi về danh sách.'],
    ['Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', '–', 'Chỉ ở trang Tạo: lưu nháp rồi mở lại trang Tạo trống.'],
    ['Nút Quay lại', 'Button', 'Enable', '–', '–', '–', 'Về danh sách; đã nhập dữ liệu thì hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
]
FR.append({
    'ten': 'Lập phiếu yêu cầu mua dịch vụ', 'uc': 'uc_them', 'uc_ten': 'FR-04 Lập phiếu yêu cầu mua dịch vụ',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Lập phiếu yêu cầu mua dịch vụ'],
        ['Mô tả', 'Nhân viên lập phiếu đề nghị mua dịch vụ thuê ngoài: nhập Ghi chú, đính kèm báo giá, nhập các dòng dịch vụ (Tên dịch vụ, Số lượng, Giá đề xuất, Nhà cung cấp) và VAT. Lưu nháp (Đang tạo) để soạn tiếp, hoặc Gửi duyệt (Chờ TP duyệt).'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở trang "Tạo phiếu yêu cầu mua dịch vụ" có sẵn 1 dòng dịch vụ trống; góc phải khối Thông tin chung hiện "<Người đăng nhập> - <ngày giờ hiện tại>".\n3. Người dùng nhập Ghi chú, bấm "Thêm tài liệu" để đính kèm file, nhập các dòng dịch vụ và VAT (%%).\n4. Bấm Gửi duyệt (hoặc Lưu nháp).\n5. Hệ thống kiểm tra dữ liệu (BR-06), sinh số phiếu (BR-04), ghi công ty / phòng ban của người lập lên phiếu, tính lại 3 dòng tổng (BR-07).\n6. Ghi nhận Tạo mới trong lịch sử.\n7. Gửi duyệt: gửi thông báo "Chờ duyệt" tới người có quyền "%s" cùng công ty (BR-10).\n8. Báo "Thêm mới thành công.", quay về danh sách.' % Q_TP],
        ['Dòng sự kiện phụ', '• Bấm "Lưu và tiếp tục": lưu nháp rồi mở lại trang Tạo trống để lập tiếp.\n• Lưu nháp chỉ bắt buộc Ghi chú; dòng dịch vụ chưa chọn Tên dịch vụ bị bỏ qua khi lưu.\n• Thiếu / sai dữ liệu → báo đỏ dưới ô lỗi, cuộn tới ô lỗi đầu tiên, không lưu.\n• Bấm Quay lại: chưa nhập gì thì về danh sách; đã nhập thì hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', 'Nút Lưu nháp / Gửi duyệt bị khóa ngay khi bấm cho tới khi có kết quả, tránh lưu 2 lần.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': 'Trang "Tạo phiếu yêu cầu mua dịch vụ" được mở từ màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('10_create', 'Trang Tạo phiếu yêu cầu mua dịch vụ lúc mới mở'),
            ('10b_create_filled', 'Trang Tạo đã nhập Ghi chú, file đính kèm và 2 dòng dịch vụ'),
            ('11_validate', 'Báo lỗi khi Gửi duyệt thiếu thông tin bắt buộc')],
    'ui': ui(UI8, FORM_UI),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'After:\n– Mở trang Tạo trống, nạp danh sách Tên dịch vụ.'],
        ['Nhập Số lượng / Giá đề xuất / VAT (%)', 'Change', 'After:\n– Tính lại Thành tiền đề xuất của dòng và 3 dòng tổng.'],
        ['Bấm Thêm tài liệu, chọn file', 'Click', 'During:\n– Kiểm đuôi file và dung lượng ≤ 10 MB.\nAfter:\n– Tải file lên, thêm dòng vào khối File đính kèm (chưa gắn vào phiếu cho tới khi lưu).'],
        ['Bấm Lưu nháp / Lưu và tiếp tục', 'Click', 'During:\n– Ghi chú bắt buộc, ≤ 255 ký tự; VAT 0–100.\n' + TRUOC_LUU + '\nAfter:\n– Sinh số phiếu, lưu phiếu trạng thái Đang tạo (bỏ dòng chưa chọn Tên dịch vụ), tính 3 dòng tổng.\n– Ghi nhận Tạo mới trong lịch sử.\n– Báo "Thêm mới thành công."; Lưu nháp → về danh sách, Lưu và tiếp tục → trang Tạo trống.'],
        ['Bấm Gửi duyệt', 'Click', 'During:\n– Như Lưu nháp, thêm: có ≥ 1 file đính kèm, ≥ 1 dòng dịch vụ, mỗi dòng có Tên dịch vụ, Số lượng, Giá đề xuất (số ≥ 0).\n' + TRUOC_LUU + '\nAfter:\n– Lưu phiếu trạng thái Chờ TP duyệt; ghi nhận Tạo mới trong lịch sử.\n– Gửi thông báo tới nhóm Trưởng phòng duyệt cùng công ty.\n– ' + VE_DS % 'Thêm mới thành công.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa nhập gì → về danh sách.\n– Đã nhập → hộp "Thông tin chưa lưu" ("Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"): Thoát thì về danh sách không lưu, Ở lại thì quay về form.'],
    ],
})

# 2.5 Sửa ------------------------------------------------------------------------
FR.append({
    'ten': 'Sửa phiếu', 'uc': 'uc_sua', 'uc_ten': 'FR-05 Sửa phiếu yêu cầu mua dịch vụ',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Sửa phiếu yêu cầu mua dịch vụ'],
        ['Mô tả', 'Người lập sửa phiếu Đang tạo hoặc Không duyệt (bị từ chối): đổi Ghi chú, file đính kèm, dòng dịch vụ, VAT; rồi Lưu nháp hoặc Gửi duyệt lại.'],
        ['Tác nhân', LAP],
        ['Điều kiện ban đầu', DK_LAP % 'Đang tạo hoặc Không duyệt'],
        ['Dòng sự kiện chính', '1. Bấm Sửa ở cột Hành động (hoặc nút Sửa ở trang Chi tiết).\n2. Hệ thống mở trang "Sửa phiếu yêu cầu mua dịch vụ: <số phiếu>" với dữ liệu hiện tại; tiêu đề khối Thông tin chung có nhãn trạng thái; phiếu Không duyệt hiện thêm Ý kiến Trưởng phòng / Ban kiểm soát (lý do từ chối).\n3. Người dùng sửa và bấm Lưu nháp hoặc Gửi duyệt.\n4. Hệ thống kiểm tra (như trang Tạo), ghi thay đổi, tính lại 3 dòng tổng.\n5. Ghi nhận Thay đổi thông tin (và Thay đổi trạng thái nếu đổi trạng thái) trong lịch sử.\n6. Gửi duyệt: gửi thông báo tới nhóm Trưởng phòng duyệt.\n7. Báo "Cập nhật thành công.", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Phiếu Không duyệt bấm Lưu nháp → về Đang tạo.\n• Mở thẳng trang Sửa của phiếu không sửa được → toast "Phiếu này không sửa được" rồi chuyển sang trang Chi tiết.\n• Phiếu vừa bị đổi trạng thái ở nơi khác → "Trạng thái đã bị thay đổi. Vui lòng load lại trang", không lưu.\n• Không phải người lập → "Bạn không có quyền sửa phiếu này".\n• Xoá file đã lưu ở khối File đính kèm → gỡ file khỏi phiếu ngay, ghi lịch sử.'],
    ],
    'menu_them': ' => Sửa {icon:btn_sua}',
    'ghi_chu_layout': 'Trang "Sửa phiếu yêu cầu mua dịch vụ" được mở từ màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.',
    'anh': [('12_edit', 'Trang Sửa phiếu yêu cầu mua dịch vụ')],
    'ui': ui(UI8, [
        ['Nhãn trạng thái', 'Label', 'Read-only', '–', '–', 'Trạng thái hiện tại', 'Góc phải khối Thông tin chung, cạnh "<Người tạo> - <ngày giờ tạo>".'],
        ['Ý kiến Trưởng phòng / Ban kiểm soát', 'Textbox', 'Read-only', '–', '–', 'Dữ liệu phiếu', 'Chỉ hiện khi có (lý do từ chối).'],
        ['Các ô còn lại', '–', 'Enable', 'Như trang Tạo', 'Như trang Tạo', 'Dữ liệu hiện tại', 'Như mục 2.4. Tên dịch vụ / nhà cung cấp đã khóa vẫn hiện đúng tên đã lưu.'],
        ['Nút Lưu nháp, Gửi duyệt, Quay lại', 'Button', 'Enable', '–', '–', '–', 'Như trang Tạo. Trang Sửa không có "Lưu và tiếp tục".'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện với người lập khi phiếu Đang tạo / Không duyệt.\nAfter:\n– Tải phiếu vào form.'],
        ['Bấm Lưu nháp / Gửi duyệt', 'Click', 'Before:\n– Phiếu còn ở Đang tạo / Không duyệt (sai → "Trạng thái đã bị thay đổi. Vui lòng load lại trang"); người thao tác là người lập (sai → "Bạn không có quyền sửa phiếu này").\nDuring:\n– Kiểm như trang Tạo.\n' + TRUOC_LUU + '\nAfter:\n– Ghi phiếu với trạng thái Đang tạo / Chờ TP duyệt, ghi lại dòng dịch vụ, tính lại 3 dòng tổng.\n– Ghi nhận Thay đổi thông tin (giá trị cũ → mới) và Thay đổi trạng thái trong lịch sử.\n– Gửi duyệt: thông báo nhóm Trưởng phòng duyệt.\n– ' + VE_DS % 'Cập nhật thành công.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa đổi gì → về danh sách; đã đổi → hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
    ],
})

# 2.6 Xem chi tiết -----------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết phiếu', 'uc': 'uc_xem', 'uc_ten': 'FR-06 Xem chi tiết phiếu yêu cầu mua dịch vụ',
    'qtc': 'Màn Xem chi tiết và Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết phiếu yêu cầu mua dịch vụ'],
        ['Mô tả', 'Xem toàn bộ phiếu ở chế độ chỉ đọc, kèm khối Lịch sử; chân trang có các nút thao tác theo trạng thái và vai trò (cùng điều kiện với cột Hành động ở danh sách). Là nơi thực hiện Duyệt, Từ chối, Duyệt lại giá, Hủy, Xóa.'],
        ['Tác nhân', NV + ' — trong phạm vi được xem'],
        ['Điều kiện ban đầu', DK + '\n2. Người dùng được xem phiếu (BR-02, BR-03): là người lập; hoặc có quyền duyệt và phiếu cùng công ty; hoặc phiếu thuộc phạm vi quyền xem.'],
        ['Dòng sự kiện chính', '1. Bấm Số phiếu ở danh sách (hoặc bấm thông báo).\n2. Hệ thống mở trang "Chi tiết yêu cầu mua dịch vụ: <số phiếu>": khối Thông tin chung (Ghi chú; Ý kiến Trưởng phòng / Ban kiểm soát nếu có; góc phải "<Người tạo> - <ngày giờ tạo>"), khối File đính kèm (xem, tải), khối Danh sách dịch vụ, khối Lịch sử (thu gọn).'],
        ['Dòng sự kiện phụ', '• Từ trạng thái Chờ KS duyệt trở đi, bảng dịch vụ thêm cột Giá duyệt, Thành tiền duyệt và cột tổng duyệt.\n• Phiếu không có file: khối File đính kèm ghi "Không có file đính kèm."\n• Không được xem: "Bạn không có quyền xem phiếu này".'],
    ],
    'menu_them': ' => Số phiếu (liên kết)',
    'anh': [('17_detail', 'Trang Chi tiết phiếu Đã duyệt (có Giá duyệt, Thành tiền duyệt; người xem không phải người lập: chỉ có In phiếu, Quay lại)'),
            ('17c_detail_rejected', 'Trang Chi tiết phiếu Không duyệt: Ý kiến Ban kiểm soát là lý do từ chối')],
    'ui': ui(UI6, [
        ['Ghi chú, Ý kiến Trưởng phòng, Ý kiến Ban kiểm soát', 'Textarea / Textbox', 'Read-only', 'Dữ liệu phiếu', 'Ý kiến chỉ hiện khi có.'],
        ['Người tạo - ngày giờ', 'Label', 'Read-only', 'Dữ liệu phiếu', 'Góc phải khối Thông tin chung.'],
        ['Khối File đính kèm', 'File', 'Read-only', 'Dữ liệu phiếu', 'Tên file, dung lượng, nút xem, tải.'],
        ['Bảng Danh sách dịch vụ', 'Table/Grid', 'Read-only', 'Dữ liệu phiếu', 'STT, Tên dịch vụ, ĐVT, Số lượng, Giá đề xuất mua trước VAT, [Giá duyệt], Thành tiền đề xuất, [Thành tiền duyệt], Nhà cung cấp; ' + TONG_GIA + '.'],
        ['Khối Lịch sử', 'Label', 'Enable', 'Thu gọn', 'Bấm "Xem lịch sử" để mở (mục 2.17).'],
        ['Nút Sửa, Xóa', 'Button', 'Enable / Ẩn', 'Theo BR-05', 'Người lập, phiếu Đang tạo / Không duyệt.'],
        ['Nút Trưởng phòng duyệt, Kiểm soát duyệt giá, Từ chối', 'Button', 'Enable / Ẩn', 'Theo BR-05', 'Người có quyền duyệt nấc đang đứng.'],
        ['Nút Yêu cầu duyệt lại giá, Hủy yêu cầu, Lập hợp đồng mua dịch vụ', 'Button', 'Enable / Ẩn', 'Theo BR-05', 'Người lập, phiếu Đã duyệt (Lập hợp đồng: cả Đang lập hợp đồng).'],
        ['Nút In phiếu, Quay lại', 'Button', 'Enable', '–', 'Luôn có.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở trang', 'System', 'Before:\n– Kiểm tra quyền xem phiếu (BR-02, BR-03).\nAfter:\n– Hiển thị phiếu, tính các nút ở chân trang theo trạng thái và vai trò.'],
        ['Bấm nút ở chân trang', 'Click', 'After:\n– Mở trang Sửa / hộp xác nhận / cửa sổ ý kiến tương ứng (mục 2.5, 2.7–2.14).'],
    ],
})

# 2.7 Xóa ------------------------------------------------------------------------
FR.append({
    'ten': 'Xóa phiếu', 'uc': 'uc_xoa', 'uc_ten': 'FR-07 Xóa phiếu yêu cầu mua dịch vụ',
    'qtc': 'Quy tắc xóa và Thông báo.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xóa phiếu yêu cầu mua dịch vụ'],
        ['Mô tả', 'Người lập xóa hẳn phiếu Đang tạo / Không duyệt cùng các dòng dịch vụ.'],
        ['Tác nhân', LAP],
        ['Điều kiện ban đầu', DK_LAP % 'Đang tạo hoặc Không duyệt'],
        ['Dòng sự kiện chính', '1. Ở trang Chi tiết bấm Xóa (nút Xóa ở cột Hành động mở trang Chi tiết).\n2. Hệ thống hiện hộp "Xác nhận xóa": "Bạn có chắc muốn xóa phiếu yêu cầu mua dịch vụ \'<số phiếu>\'?"\n3. Bấm Xóa.\n4. Hệ thống ghi nhận Xóa trong lịch sử (giữ lại vết), xóa các dòng dịch vụ và phiếu.\n5. Báo "Xóa thành công.", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Bấm Hủy / (x) → đóng hộp, không thay đổi.\n• Phiếu vừa được gửi duyệt ở nơi khác → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n• Không phải người lập → "Bạn không có quyền xóa phiếu này".'],
    ],
    'menu_them': ' => Số phiếu => Xóa {icon:btn_xoa_footer}',
    'ghi_chu_layout': POPUP % ('Xác nhận xóa', 'chi tiết phiếu'),
    'anh': [('13_delete', 'Hộp Xác nhận xóa phiếu')],
    'ui': ui(UI4, [
        ['Nút Xóa (chân trang Chi tiết)', 'Button', 'Biểu tượng thùng rác; chỉ hiện với người lập khi phiếu Đang tạo / Không duyệt.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận xóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn xóa phiếu yêu cầu mua dịch vụ \'<số phiếu>\'?"'],
        ['Nút Xóa', 'Button', 'Xác nhận xóa.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không xóa.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Xóa', 'Click', 'After:\n– Hiện hộp Xác nhận xóa.'],
        ['Bấm Xóa trong hộp', 'Click', 'Before:\n– Phiếu còn Đang tạo / Không duyệt; người thao tác là người lập.\nDuring:\n' + TRUOC_LUU + '\nAfter:\n– Ghi nhận Xóa trong lịch sử, xóa dòng dịch vụ và phiếu.\n– ' + VE_DS % 'Xóa thành công.'],
        ['Bấm Hủy / (x)', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})


def comment_fr(ten, uc, tacnhan, dk, mota, chinh, phu, menu, popup_title, anh, ui_rows, ev_after, ev_before):
    return {
        'ten': ten, 'uc': uc, 'uc_ten': 'FR-%02d %s' % (len(FR) + 1, ten),
        'qtc': 'Quy tắc phê duyệt, Thông báo và Quy tắc ghi lịch sử.',
        'gioi_thieu': [['Tên chức năng', ten], ['Mô tả', mota], ['Tác nhân', tacnhan], ['Điều kiện ban đầu', dk],
                       ['Dòng sự kiện chính', chinh], ['Dòng sự kiện phụ', phu]],
        'menu_them': menu,
        'ghi_chu_layout': POPUP % (popup_title, 'chi tiết phiếu') if popup_title else None,
        'anh': anh,
        'ui': ui(UI8, ui_rows), 'ui_widths': UI8W,
        'events': [
            ['Bấm ' + ten.split(' (')[0] + ' ở chân trang', 'Click', 'After:\n– ' + ('Mở cửa sổ "%s".' % popup_title if popup_title else 'Thực hiện ngay (không có hộp xác nhận).')],
            ['Bấm nút xác nhận', 'Click', 'Before:\n– ' + ev_before + '\nDuring:\n' + TRUOC_LUU + '\nAfter:\n' + ev_after],
            ['Bấm Hủy / (x)', 'Click', 'After:\n– Đóng cửa sổ, không thay đổi.'],
        ],
    }


XUNG_DOT = ' Sai trạng thái (phiếu vừa được thao tác ở nơi khác) → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".'

# 2.8 Trưởng phòng duyệt -----------------------------------------------------------
FR.append(comment_fr(
    'Trưởng phòng duyệt', 'uc_tpduyet', 'Người có quyền "%s"' % Q_TP,
    DK + '\n2. Người dùng có quyền "%s".\n3. Phiếu ở trạng thái Chờ TP duyệt.' % Q_TP,
    'Trưởng phòng duyệt nội dung phiếu, chuyển phiếu sang Chờ KS duyệt (chờ Ban kiểm soát duyệt giá).',
    '1. Ở trang Chi tiết phiếu Chờ TP duyệt bấm "Trưởng phòng duyệt".\n2. Hệ thống mở cửa sổ "Trưởng phòng duyệt yêu cầu mua dịch vụ" (dòng phụ "Phiếu: <số phiếu>").\n3. Người dùng nhập Ý kiến Trưởng phòng (không bắt buộc), bấm Duyệt.\n4. Hệ thống kiểm tra chặn hàng quá hạn (BR-09), chuyển phiếu sang Chờ KS duyệt, ghi người duyệt, Ngày nhận đơn = thời điểm duyệt, Ý kiến Trưởng phòng.\n5. Ghi nhận Thay đổi trạng thái (kèm ý kiến) trong lịch sử.\n6. Gửi thông báo "Chờ duyệt" tới người có quyền "%s" cùng công ty.\n7. Báo "Duyệt thành công.", quay về danh sách.' % Q_KS,
    '• Người duyệt (hoặc nhân viên phòng mình quản lý) còn hàng quá hạn theo cấu hình "Duyệt yêu cầu mua dịch vụ" → bị chặn, hiện lý do và danh sách hàng quá hạn.\n• Nút hiện với mọi phiếu Chờ TP duyệt người dùng mở được, không giới hạn phòng ban (BR-08).' + XUNG_DOT,
    ' => Số phiếu => Trưởng phòng duyệt {icon:btn_tpduyet}', 'Trưởng phòng duyệt yêu cầu mua dịch vụ',
    [('30_detail_wait_tp', 'Trang Chi tiết phiếu Chờ TP duyệt: nút Trưởng phòng duyệt, Từ chối'),
     ('31_tp_modal', 'Cửa sổ Trưởng phòng duyệt yêu cầu mua dịch vụ')],
    [['Dòng phụ "Phiếu:"', 'Label', 'Read-only', '–', '–', 'Số phiếu', 'Số phiếu đang duyệt.'],
     ['Ý kiến Trưởng phòng', 'Textarea', 'Enable', '0–5000 ký tự', 'Không', 'Trống', 'Lưu vào Ý kiến Trưởng phòng của phiếu.'],
     ['Nút Duyệt', 'Button', 'Enable', '–', '–', '–', 'Xác nhận duyệt.'],
     ['Nút Hủy', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ.']],
    '– Kiểm chặn hàng quá hạn (BR-09).\n– Chuyển Chờ KS duyệt; ghi người duyệt, Ngày nhận đơn, Ý kiến Trưởng phòng.\n– Ghi nhận Thay đổi trạng thái kèm ý kiến trong lịch sử; thông báo nhóm Ban kiểm soát.\n– ' + VE_DS % 'Duyệt thành công.',
    'Phiếu Chờ TP duyệt; có quyền "%s" (thiếu → "Bạn không có quyền duyệt phiếu này").' % Q_TP))

# 2.9 Ban kiểm soát duyệt giá --------------------------------------------------------
FR.append(comment_fr(
    'Ban kiểm soát duyệt giá', 'uc_ksduyet', 'Người có quyền "%s"' % Q_KS,
    DK + '\n2. Người dùng có quyền "%s" và cùng công ty với phiếu.\n3. Phiếu ở trạng thái Chờ KS duyệt.' % Q_KS,
    'Ban kiểm soát duyệt giá, phiếu chuyển sang Đã duyệt — làm căn cứ lập Hợp đồng mua dịch vụ.',
    '1. Ở trang Chi tiết phiếu Chờ KS duyệt bấm "Kiểm soát duyệt giá".\n2. Hệ thống mở cửa sổ "Ban kiểm soát duyệt giá".\n3. Người dùng nhập Ý kiến Ban kiểm soát (không bắt buộc), bấm Duyệt giá.\n4. Hệ thống chuyển phiếu sang Đã duyệt, ghi Người duyệt giá, Ngày duyệt giá, Ý kiến Ban kiểm soát; tính lại 3 dòng tổng duyệt từ Giá duyệt đang có trên từng dòng.\n5. Ghi nhận Thay đổi trạng thái (kèm ý kiến) trong lịch sử.\n6. Báo "Duyệt thành công.", quay về danh sách.',
    '• Cột Giá duyệt trên trang Chi tiết chỉ đọc, cửa sổ không có ô nhập giá duyệt từng dòng.\n• Người khác công ty với phiếu không thấy nút.' + XUNG_DOT,
    ' => Số phiếu => Kiểm soát duyệt giá {icon:btn_ksduyet}', 'Ban kiểm soát duyệt giá',
    [('33_detail_wait_ks', 'Trang Chi tiết phiếu Chờ KS duyệt: nút Kiểm soát duyệt giá, Từ chối'),
     ('34_ks_modal', 'Cửa sổ Ban kiểm soát duyệt giá')],
    [['Dòng phụ "Phiếu:"', 'Label', 'Read-only', '–', '–', 'Số phiếu', 'Số phiếu đang duyệt.'],
     ['Ý kiến Ban kiểm soát', 'Textarea', 'Enable', '0–5000 ký tự', 'Không', 'Trống', 'Lưu vào Ý kiến Ban kiểm soát của phiếu.'],
     ['Nút Duyệt giá', 'Button', 'Enable', '–', '–', '–', 'Xác nhận duyệt giá.'],
     ['Nút Hủy', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ.']],
    '– Chuyển Đã duyệt; ghi Người duyệt giá, Ngày duyệt giá, Ý kiến Ban kiểm soát; tính lại tổng duyệt.\n– Ghi nhận Thay đổi trạng thái kèm ý kiến trong lịch sử.\n– ' + VE_DS % 'Duyệt thành công.',
    'Phiếu Chờ KS duyệt; có quyền "%s" và cùng công ty (thiếu → "Bạn không có quyền duyệt giá phiếu này").' % Q_KS))

# 2.10 Từ chối --------------------------------------------------------------------------
FR.append(comment_fr(
    'Từ chối phiếu', 'uc_tuchoi', 'Người có quyền duyệt nấc phiếu đang đứng',
    DK + '\n2. Phiếu Chờ TP duyệt và người dùng có quyền "%s"; hoặc phiếu Chờ KS duyệt và người dùng có quyền "%s" cùng công ty.' % (Q_TP, Q_KS),
    'Trả phiếu về cho người lập sửa lại (trạng thái Không duyệt), lý do bắt buộc.',
    '1. Ở trang Chi tiết bấm "Từ chối".\n2. Hệ thống mở cửa sổ "Từ chối yêu cầu mua dịch vụ".\n3. Người dùng nhập Lý do từ chối (bắt buộc), bấm Từ chối.\n4. Hệ thống chuyển phiếu sang Không duyệt; lý do ghi vào Ý kiến Trưởng phòng (nếu từ chối ở nấc Trưởng phòng) hoặc Ý kiến Ban kiểm soát (nấc Ban kiểm soát).\n5. Ghi nhận Thay đổi trạng thái (kèm lý do) trong lịch sử.\n6. Gửi thông báo "Từ chối" tới người lập kèm người từ chối và lý do.\n7. Báo "Thao tác thành công.", quay về danh sách.',
    '• Bỏ trống lý do → báo đỏ "Bắt buộc phải nhập", không gửi.' + XUNG_DOT,
    ' => Số phiếu => Từ chối {icon:btn_tuchoi}', 'Từ chối yêu cầu mua dịch vụ',
    [('32_reject_modal', 'Cửa sổ Từ chối yêu cầu mua dịch vụ khi chưa nhập lý do')],
    [['Lý do từ chối', 'Textarea', 'Enable', '1–5000 ký tự', 'Có', 'Trống', 'Bỏ trống: "Bắt buộc phải nhập".'],
     ['Nút Từ chối', 'Button', 'Enable', '–', '–', '–', 'Xác nhận từ chối.'],
     ['Nút Hủy', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ.']],
    '– Chuyển Không duyệt; ghi lý do vào ý kiến của nấc đang đứng.\n– Ghi nhận Thay đổi trạng thái kèm lý do trong lịch sử; thông báo người lập.\n– ' + VE_DS % 'Thao tác thành công.',
    'Phiếu Chờ TP duyệt / Chờ KS duyệt; có quyền duyệt nấc đó (thiếu → "Bạn không có quyền từ chối phiếu này").'))

# 2.11 Yêu cầu duyệt lại giá -----------------------------------------------------------
FR.append(comment_fr(
    'Yêu cầu duyệt lại giá', 'uc_duyetlai', LAP, DK_LAP % 'Đã duyệt',
    'Người lập xin Ban kiểm soát duyệt lại giá: phiếu Đã duyệt quay về Chờ KS duyệt.',
    '1. Ở trang Chi tiết phiếu Đã duyệt bấm "Yêu cầu duyệt lại giá".\n2. Hệ thống chuyển phiếu về Chờ KS duyệt (không có hộp xác nhận).\n3. Ghi nhận Thay đổi trạng thái trong lịch sử.\n4. Gửi thông báo "Chờ duyệt — Xin duyệt lại giá" tới nhóm Ban kiểm soát cùng công ty.\n5. Báo "Thao tác thành công.", quay về danh sách.',
    '• Không phải người lập → "Bạn không có quyền thao tác trên phiếu này".' + XUNG_DOT,
    ' => Số phiếu => Yêu cầu duyệt lại giá {icon:btn_duyetlai}', None,
    [('35_detail_approved_owner', 'Trang Chi tiết phiếu Đã duyệt của người lập: Yêu cầu duyệt lại giá, Hủy yêu cầu, Lập hợp đồng mua dịch vụ')],
    [['Nút Yêu cầu duyệt lại giá', 'Button', 'Enable / Ẩn', '–', '–', '–', 'Chỉ hiện với người lập khi phiếu Đã duyệt; bấm là thực hiện ngay.']],
    '– Chuyển Chờ KS duyệt; ghi nhận Thay đổi trạng thái; thông báo nhóm Ban kiểm soát.\n– ' + VE_DS % 'Thao tác thành công.',
    'Phiếu Đã duyệt; người thao tác là người lập.'))

# 2.12 Hủy yêu cầu ------------------------------------------------------------------------
FR.append(comment_fr(
    'Hủy yêu cầu', 'uc_huy', LAP, DK_LAP % 'Đã duyệt',
    'Người lập hủy phiếu đã duyệt (không còn nhu cầu mua). Phiếu Hủy chỉ còn xem, in.',
    '1. Ở trang Chi tiết phiếu Đã duyệt bấm "Hủy yêu cầu".\n2. Hệ thống mở cửa sổ "Hủy yêu cầu mua dịch vụ".\n3. Người dùng nhập Lý do hủy (không bắt buộc), bấm Hủy yêu cầu.\n4. Hệ thống chuyển phiếu sang Hủy.\n5. Ghi nhận Thay đổi trạng thái (kèm lý do) trong lịch sử.\n6. Báo "Thao tác thành công.", quay về danh sách.',
    '• Lý do hủy chỉ lưu trong lịch sử, không ghi vào ô ý kiến của phiếu.\n• Không phải người lập → "Bạn không có quyền hủy phiếu này".' + XUNG_DOT,
    ' => Số phiếu => Hủy yêu cầu {icon:btn_huyyc}', 'Hủy yêu cầu mua dịch vụ',
    [('36_cancel_modal', 'Cửa sổ Hủy yêu cầu mua dịch vụ')],
    [['Lý do hủy', 'Textarea', 'Enable', '0–5000 ký tự', 'Không', 'Trống', 'Ghi vào lịch sử.'],
     ['Nút Hủy yêu cầu', 'Button', 'Enable', '–', '–', '–', 'Xác nhận hủy.'],
     ['Nút Hủy', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ, không hủy phiếu.']],
    '– Chuyển Hủy; ghi nhận Thay đổi trạng thái kèm lý do.\n– ' + VE_DS % 'Thao tác thành công.',
    'Phiếu Đã duyệt; người thao tác là người lập.'))

# 2.13 Lập hợp đồng mua dịch vụ ----------------------------------------------------------
FR.append({
    'ten': 'Lập hợp đồng mua dịch vụ',
    'qtc': 'Quy tắc điều hướng giữa các màn.',
    'gioi_thieu': [
        ['Tên chức năng', 'Lập hợp đồng mua dịch vụ từ phiếu đã duyệt'],
        ['Mô tả', 'Mở màn lập Hợp đồng mua dịch vụ (màn này chưa có trên HRM, nằm ở cổng quản trị cũ) ở tab mới, gắn sẵn phiếu yêu cầu. Khi kế toán lập hợp đồng, phiếu tự chuyển Đang lập hợp đồng / Đã lập hợp đồng theo số lượng đã lập (BR-11).'],
        ['Tác nhân', LAP],
        ['Điều kiện ban đầu', DK_LAP % 'Đã duyệt hoặc Đang lập hợp đồng'],
        ['Dòng sự kiện chính', '1. Bấm "Lập hợp đồng mua dịch vụ" ở cột Hành động hoặc chân trang Chi tiết.\n2. Hệ thống mở tab mới tới màn lập Hợp đồng mua dịch vụ của phiếu.'],
        ['Dòng sự kiện phụ', '• Hệ thống chưa cấu hình đường dẫn cổng quản trị cũ → báo lỗi, không mở tab.\n• HRM không ghi gì vào phiếu ở bước này.'],
    ],
    'menu_them': ' => Lập hợp đồng mua dịch vụ {icon:btn_laphd}',
    'anh': [],
    'ui': ui(UI4, [['Nút Lập hợp đồng mua dịch vụ', 'Button', 'Biểu tượng mũi tên ra ngoài; chỉ hiện với người lập khi phiếu Đã duyệt / Đang lập hợp đồng.']]),
    'ui_widths': UI4W,
    'events': [['Bấm Lập hợp đồng mua dịch vụ', 'Click', 'After:\n– Mở tab mới tới màn lập hợp đồng kèm mã phiếu; thiếu cấu hình đường dẫn thì báo lỗi.']],
})

# 2.14 In phiếu ---------------------------------------------------------------------------
FR.append({
    'ten': 'In phiếu', 'uc': 'uc_inphieu', 'uc_ten': 'FR-14 In phiếu yêu cầu mua dịch vụ',
    'qtc': 'Quy tắc màn In và bố cục bản in.',
    'gioi_thieu': [
        ['Tên chức năng', 'In phiếu yêu cầu mua dịch vụ'],
        ['Mô tả', 'In 1 phiếu theo mẫu "Phiếu yêu cầu mua dịch vụ", khổ ngang, phần đầu là tiêu đề của CÔNG TY TRÊN PHIẾU.'],
        ['Tác nhân', NV + ' — được xem phiếu'],
        ['Điều kiện ban đầu', DK_PV],
        ['Dòng sự kiện chính', '1. Bấm "In phiếu" ở cột Hành động hoặc chân trang Chi tiết.\n2. Hệ thống mở cửa sổ "Xem trước phiếu yêu cầu mua dịch vụ".\n3. Bấm In để mở hộp in của trình duyệt.'],
        ['Dòng sự kiện phụ', '• Phiếu Đã duyệt in 4 cột tiền (Giá đề xuất, Giá duyệt, Thành tiền đề xuất, Thành tiền duyệt); trạng thái khác in 2 cột.\n• Khối ký: Ban kiểm soát, Trưởng phòng, Người lập — kèm họ tên và chữ "Đã duyệt" khi nấc đó đã duyệt.'],
    ],
    'menu_them': ' => In phiếu {icon:btn_inphieu}',
    'ghi_chu_layout': 'Cửa sổ Xem trước phiếu được mở ngay trên màn hình danh sách hoặc chi tiết phiếu theo đường dẫn ở trên.',
    'anh': [('19b_printdetail', 'Cửa sổ xem trước bản in phiếu Đã duyệt')],
    'ui': ui(UI6, [
        ['Tiêu đề cửa sổ', 'Label', 'Read-only', '"Xem trước phiếu yêu cầu mua dịch vụ"', '–'],
        ['Phần đầu bản in', 'Label', 'Read-only', 'Tiêu đề công ty trên phiếu', 'Logo, tên, địa chỉ của công ty ghi trên phiếu.'],
        ['Tiêu đề bản in', 'Label', 'Read-only', '"PHIẾU YÊU CẦU MUA DỊCH VỤ"', 'Kèm Số phiếu, Ngày lập, Ghi chú.'],
        ['Bảng dịch vụ', 'Table/Grid', 'Read-only', 'Dữ liệu phiếu', 'STT, Tên dịch vụ, ĐVT (Gói), Số lượng, Giá đề xuất mua trước VAT, [Giá duyệt], Thành tiền đề xuất, [Thành tiền duyệt], Nhà cung cấp; ' + TONG_GIA + '.'],
        ['Khối ký', 'Label', 'Read-only', '–', 'Ban kiểm soát, Trưởng phòng, Người lập.'],
        ['Nút In / (x)', 'Button', 'Enable', '–', 'Mở hộp in / đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In phiếu', 'Click', 'Before:\n– Kiểm quyền xem phiếu ("Bạn không có quyền xem phiếu này").\nAfter:\n– Dựng bản in theo mẫu, hiện xem trước.'],
        ['Bấm In', 'Click', 'After:\n– Mở hộp in của trình duyệt.'],
    ],
})

# 2.15 In danh sách --------------------------------------------------------------------------
FR.append({
    'ten': 'In danh sách', 'uc': 'uc_in', 'uc_ten': 'FR-15 In danh sách yêu cầu mua dịch vụ',
    'qtc': 'Quy tắc màn In và bố cục bản in.',
    'gioi_thieu': [
        ['Tên chức năng', 'In danh sách yêu cầu mua dịch vụ'],
        ['Mô tả', 'In danh sách đang lọc theo mẫu "Danh sách yêu cầu mua dịch vụ", khổ ngang, tiêu đề công ty của người đăng nhập.'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm In danh sách.\n2. Hệ thống mở cửa sổ "Xem trước danh sách yêu cầu mua dịch vụ" với mọi phiếu khớp bộ lọc (mọi trang).\n3. Bấm In để mở hộp in của trình duyệt.'],
        ['Dòng sự kiện phụ', '• Danh sách vượt 2,000 dòng: không in, hiện câu nhắc thu hẹp bộ lọc, ẩn nút In (BR-12).'],
    ],
    'menu_them': ' => In danh sách {icon:btn_indanhsach}',
    'ghi_chu_layout': 'Cửa sổ Xem trước bản in được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('19_printlist', 'Cửa sổ xem trước bản in danh sách')],
    'ui': ui(UI6, [
        ['Tiêu đề cửa sổ', 'Label', 'Read-only', '"Xem trước danh sách yêu cầu mua dịch vụ"', '–'],
        ['Tiêu đề bản in', 'Label', 'Read-only', '"DANH SÁCH YÊU CẦU MUA DỊCH VỤ"', '–'],
        ['Bảng in', 'Table/Grid', 'Read-only', 'Theo bộ lọc', '9 cột cố định: STT, Số phiếu, Ngày tạo, Ngày nhận đơn, Ngày duyệt giá, Người yêu cầu, Phòng yêu cầu, Người duyệt giá, Trạng thái (ngày dạng dd/mm/yyyy).'],
        ['Nút In / (x)', 'Button', 'Enable', '–', 'Mở hộp in / đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In danh sách', 'Click', 'After:\n– Dựng bản in theo bộ lọc hiện tại; vượt 2,000 dòng thì chỉ hiện câu nhắc.'],
        ['Bấm In', 'Click', 'After:\n– Mở hộp in của trình duyệt.'],
    ],
})

# 2.16 Xuất Excel ------------------------------------------------------------------------
FR.append({
    'ten': 'Xuất Excel danh sách', 'uc': 'uc_xuat', 'uc_ten': 'FR-16 Xuất Excel danh sách',
    'qtc': 'Quy tắc Excel và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách yêu cầu mua dịch vụ ra Excel'],
        ['Mô tả', 'Xuất mọi phiếu khớp bộ lọc (không chỉ trang đang xem) ra file danh_sach_yeu_cau_mua_dich_vu.xlsx, tiêu đề "Danh sách yêu cầu mua dịch vụ", cột theo lựa chọn và thứ tự người dùng.'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất file", tích sẵn các cột đang hiện trên bảng.\n3. Người dùng tích / bỏ, kéo ☰ đổi thứ tự, bấm Xuất file.\n4. Hệ thống dựng file và tải về; báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Lỗi khi xuất → "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất file')],
    'ui': ui(UI8, [
        ['Danh sách trường', 'Checkbox', 'Enable', '14 trường', 'Có (≥ 1)', 'Các cột đang hiện', 'Số phiếu, Ngày tạo, Ngày nhận đơn, Ngày duyệt giá, Người yêu cầu, Phòng yêu cầu, Người duyệt giá, Trạng thái, Công ty, Ghi chú, Ý kiến Trưởng phòng, Ý kiến Ban kiểm soát, Người cập nhật, Ngày cập nhật. Kéo ☰ đổi thứ tự cột trong file.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', 'Chọn / bỏ nhanh mọi trường.'],
        ['Dòng đếm', 'Label', 'Read-only', '–', '–', '–', '"Đang chọn x/14 trường".'],
        ['Nút Xuất file', 'Button', 'Enable', '–', '–', '–', 'Xuất file theo trường đã chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng, không xuất.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất file', 'Click', 'After:\n– Lấy dữ liệu theo bộ lọc + phạm vi hiện tại, dựng file đúng thứ tự cột, tải về; báo kết quả.'],
        ['Kéo ☰', 'Drag', 'After:\n– Đổi thứ tự cột trong file.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.17 Lịch sử -----------------------------------------------------------------------------
FR.append({
    'ten': 'Xem lịch sử thay đổi',
    'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem lịch sử thay đổi phiếu'],
        ['Mô tả', 'Liệt kê các lần thao tác trên 1 phiếu, mới nhất ở trên: Tạo mới, Thay đổi thông tin (Ghi chú, Thuế VAT (%), File đính kèm, Dòng dịch vụ — cũ → mới), Thay đổi trạng thái (kèm ý kiến / lý do), Xóa; kèm người thực hiện, phòng ban, thời điểm.'],
        ['Tác nhân', NV + ' — được xem phiếu'],
        ['Điều kiện ban đầu', DK_PV],
        ['Dòng sự kiện chính', '1. Bấm Lịch sử ở cột Hành động → cửa sổ "Lịch sử thay đổi: <số phiếu>".\n2. Hoặc ở trang Chi tiết bấm "Xem lịch sử" ở khối Lịch sử.\n3. Hệ thống liệt kê các mốc; có nút Bộ lọc (loại hành động, người thực hiện, khoảng ngày).'],
        ['Dòng sự kiện phụ', '• Giá trị cũ in đỏ, giá trị mới in xanh; ý kiến / lý do in trong khung vàng.\n• Thao tác thực hiện ngoài HRM (vd lập hợp đồng ở cổng quản trị cũ) không có mốc lịch sử.'],
    ],
    'menu_them': ' => Lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': 'Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối Lịch sử nằm cuối trang Chi tiết phiếu.',
    'anh': [('16_history', 'Cửa sổ Lịch sử thay đổi mở từ danh sách'), ('17b_detail_history', 'Khối Lịch sử ở trang Chi tiết')],
    'ui': ui(UI6, [
        ['Tiêu đề', 'Label', 'Read-only', '"Lịch sử thay đổi: <số phiếu>"', '–'],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Lọc theo loại hành động, người thực hiện, Từ ngày, Đến ngày.'],
        ['Mốc lịch sử', 'Label', 'Read-only', 'Mới nhất trên cùng', 'Thời điểm, tên hành động, "Người thực hiện: <họ tên> — <phòng ban>", trường đổi: cũ → mới, ý kiến / lý do.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lịch sử / Xem lịch sử', 'Click', 'After:\n– Tải và hiển thị các mốc lịch sử của phiếu.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

for _f in FR:
    if 'uc_ten' in _f:
        _f['uc_ten'] = 'FR-%02d %s' % (FR.index(_f) + 1, _f['ten'])
FR_NAMES = ['FR-%02d %s' % (i + 1, f['ten']) for i, f in enumerate(FR)]
PV = 'Theo phạm vi'
CT = 'Có (phiếu cùng công ty)'
_ma = [
    (PV, PV, PV), ('Có', 'Có', 'Có'), ('Có', 'Có', 'Có'), ('Có', 'Có', 'Có'), (LAP, LAP, LAP), (PV, CT, CT), (LAP, LAP, LAP),
    ('Không', 'Có', 'Không'), ('Không', 'Không', CT), ('Không', 'Có (nấc TP)', 'Có (nấc KS)'),
    (LAP, LAP, LAP), (LAP, LAP, LAP), (LAP, LAP, LAP), (PV, CT, CT), (PV, PV, PV), (PV, PV, PV), (PV, CT, CT),
]
assert len(_ma) == len(FR)

S = {
    'ten': TEN, 'ten_ngan': 'phiếu yêu cầu mua dịch vụ', 'phan_he': 'Bán hàng',
    'menu': [('Bán hàng', 'menu_phanhe'), ('Yêu cầu', 'menu_nhom'), ('Mua dịch vụ', None), (TEN, 'menu_muc')],
    'muc_dich': [
        'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho việc lập và phê duyệt PHIẾU YÊU CẦU MUA DỊCH VỤ thuê ngoài (vận chuyển, lắp đặt, thuê nhân công, kiểm định…) — đầu vào để lập Hợp đồng mua dịch vụ.',
        'Là căn cứ nghiệm thu chức năng, phân quyền và luồng duyệt 2 nấc (Trưởng phòng duyệt nội dung, Ban kiểm soát duyệt giá).',
        'Làm rõ phạm vi dữ liệu theo 3 cấp quyền xem và quy tắc phiếu Đang tạo chỉ người lập thấy.',
        'Làm rõ các nhánh trạng thái: từ chối, xin duyệt lại giá, hủy, và hai trạng thái do bước lập hợp đồng cập nhật.',
    ],
    'thuat_ngu': [
        ['Phiếu yêu cầu mua dịch vụ', 'Đề nghị mua dịch vụ thuê ngoài gồm Ghi chú, file đính kèm (báo giá) và các dòng dịch vụ; mỗi phiếu có 1 số phiếu.'],
        ['Dòng dịch vụ', 'Một dịch vụ cần mua: Tên dịch vụ (mã phí loại "Dịch vụ sửa chữa & chi phí khác"), Số lượng, Giá đề xuất mua trước VAT, Nhà cung cấp.'],
        ['TP', 'Trưởng phòng — người có quyền "%s", duyệt nội dung phiếu.' % Q_TP],
        ['KS', 'Ban kiểm soát — người có quyền "%s", duyệt giá.' % Q_KS],
        ['Ngày nhận đơn', 'Thời điểm Trưởng phòng duyệt phiếu.'],
        ['Giá duyệt / Thành tiền duyệt', 'Giá được Ban kiểm soát chấp nhận cho từng dòng và thành tiền tương ứng.'],
        ['Người lập', 'Nhân viên tạo phiếu; công ty / phòng ban của phiếu lấy theo người này lúc lập.'],
    ],
    'trang_thai': {
        'cau_dan': 'Phiếu đi qua 2 nấc duyệt: Trưởng phòng duyệt nội dung → Ban kiểm soát duyệt giá. Bảng dưới liệt kê đủ 8 trạng thái và trạng thái "Đã xóa"; nút thao tác ở mỗi trạng thái hiện theo đúng cột "Thao tác được phép".',
        'rows': [
            ['Đang tạo', 'Phiếu nháp, đang soạn. Chỉ người lập thấy.', 'Xem, Sửa (Lưu nháp / Gửi duyệt), Xóa, In, Lịch sử', LAP],
            ['Chờ TP duyệt', 'Đã gửi duyệt, chờ Trưởng phòng duyệt nội dung.', 'Xem, Trưởng phòng duyệt, Từ chối, In, Lịch sử', 'Người có quyền "%s"' % Q_TP],
            ['Chờ KS duyệt', 'Trưởng phòng đã duyệt (hoặc người lập xin duyệt lại giá), chờ Ban kiểm soát duyệt giá.', 'Xem, Kiểm soát duyệt giá, Từ chối, In, Lịch sử', 'Người có quyền "%s" cùng công ty' % Q_KS],
            ['Đã duyệt', 'Ban kiểm soát đã duyệt giá; căn cứ lập hợp đồng.', 'Xem, Yêu cầu duyệt lại giá, Hủy yêu cầu, Lập hợp đồng mua dịch vụ, In, Lịch sử', LAP],
            ['Không duyệt', 'Bị từ chối ở 1 trong 2 nấc; người lập sửa lại được.', 'Xem, Sửa (Lưu nháp → Đang tạo; Gửi duyệt → Chờ TP duyệt), Xóa, In, Lịch sử', LAP],
            ['Đang lập hợp đồng', 'Đã lập hợp đồng cho một phần số lượng (cập nhật tự động từ màn Hợp đồng mua dịch vụ).', 'Xem, Lập hợp đồng mua dịch vụ, In, Lịch sử', 'Tự chuyển khi lập hợp đồng'],
            ['Đã lập hợp đồng', 'Đã lập hợp đồng đủ số lượng.', 'Xem, In, Lịch sử', 'Tự chuyển khi lập hợp đồng'],
            ['Hủy', 'Người lập hủy phiếu đã duyệt.', 'Xem, In, Lịch sử', LAP],
            ['Đã xóa', 'Phiếu và dòng dịch vụ bị xóa khỏi hệ thống (lịch sử vẫn giữ mốc Xóa).', '–', LAP + ', chỉ từ Đang tạo / Không duyệt'],
        ],
        'anh': 'state_flow',
        'ghi_chu': ['Nhãn màu trạng thái: Đang tạo xám; Chờ TP duyệt, Chờ KS duyệt, Đang lập hợp đồng vàng; Đã duyệt, Đã lập hợp đồng xanh; Không duyệt, Hủy đỏ.',
                    'Mọi lần đổi trạng thái trên HRM đều ghi mốc "Thay đổi trạng thái" (kèm ý kiến / lý do nếu có) vào lịch sử phiếu.'],
    },
    'quyen_truoc': ['Màn hình KHÔNG gắn quyền vào mục menu: mọi nhân viên đăng nhập đều vào màn, lập phiếu và xem phiếu do mình lập. '
                    'Quyền riêng của màn gồm 2 quyền duyệt và 3 quyền phạm vi xem (nhóm quyền "Yêu cầu mua dịch vụ", phân hệ Bán hàng). '
                    'Tài khoản Super admin được coi như có đủ mọi quyền.'],
    'quyen_rows': [
        ['(không cần quyền)', 'Vào màn, xem danh sách theo phạm vi, tìm kiếm, tuỳ chỉnh cột, in, xuất Excel; Tạo mới; người lập: Sửa, Xóa, Yêu cầu duyệt lại giá, Hủy yêu cầu, Lập hợp đồng mua dịch vụ.'],
        [Q_TP, 'Thấy nút Trưởng phòng duyệt, Từ chối ở phiếu Chờ TP duyệt; xem được mọi phiếu (trừ Đang tạo) cùng công ty; nhận thông báo khi có phiếu gửi duyệt.'],
        [Q_KS, 'Thấy nút Kiểm soát duyệt giá, Từ chối ở phiếu Chờ KS duyệt cùng công ty; xem được mọi phiếu (trừ Đang tạo) cùng công ty; nhận thông báo khi có phiếu chờ duyệt giá / xin duyệt lại giá.'],
    ],
    'pham_vi_truoc': ['Nhóm quyền quyết định phạm vi danh sách (xét theo thứ tự từ trên xuống, có quyền nào trước thì áp quyền đó):'],
    'pham_vi_rows': [
        ['1', Q_ALL + ' (hoặc Super admin)', 'Phiếu của mọi công ty; khu vực lọc có ô Công ty, Phòng ban.'],
        ['2', Q_CTY, 'Phiếu thuộc công ty đang làm việc của người dùng; có ô Phòng ban.'],
        ['3', Q_PB, 'Phiếu thuộc các phòng ban người dùng được giao quản lý và phòng ban người dùng đang làm việc.'],
        ['4', '(không có quyền nào ở trên)', 'Chỉ phiếu do chính người dùng lập.'],
    ],
    'pham_vi_sau': ['Ở mọi cấp, phiếu Đang tạo của người khác KHÔNG hiện (BR-03). Công ty / phòng ban của phiếu là công ty / phòng ban của người lập tại thời điểm lập. '
                    'Trang Chi tiết, In phiếu, Lịch sử còn mở được cho người có quyền duyệt với mọi phiếu (trừ Đang tạo) cùng công ty — người duyệt vào phiếu qua thông báo. '
                    'Phạm vi áp như nhau cho danh sách, in danh sách và xuất Excel.'],
    'ma_tran': [['Chức năng', 'Nhân viên (không quyền riêng)', 'Có quyền Trưởng phòng duyệt', 'Có quyền Ban kiểm soát duyệt giá']] +
               [[f] + list(_ma[i]) for i, f in enumerate(FR_NAMES)],
    'ma_tran_widths': [2.6, 1.3, 1.2, 1.2],
    'quyen_sau': ['"Người lập": chỉ người lập phiếu mới thấy nút, kể cả khi có quyền khác. "Theo phạm vi": theo bảng phạm vi dữ liệu ở trên. '
                  'Trưởng phòng duyệt / Ban kiểm soát duyệt giá chỉ thao tác được ở trạng thái tương ứng (Phần 1 mục 3).'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Duyệt 2 nấc', ['– Gửi duyệt → Chờ TP duyệt → (Trưởng phòng duyệt) Chờ KS duyệt → (Ban kiểm soát duyệt giá) Đã duyệt.', '– Từ chối ở bất kỳ nấc nào → Không duyệt; người lập sửa và gửi lại từ đầu.'], ['Lập phiếu', 'Duyệt', 'Từ chối']),
        ('BR-02', 'Phạm vi dữ liệu theo 3 cấp quyền xem', ['– Xét lần lượt: tổng công ty → công ty → phòng ban (quản lý + đang làm việc) → chỉ phiếu mình lập.', '– Người có quyền duyệt mở được Chi tiết mọi phiếu (trừ Đang tạo) cùng công ty.', '– Không được xem: "Bạn không có quyền xem phiếu này".'], ['Mọi chức năng']),
        ('BR-03', 'Phiếu nháp chỉ người lập thấy', ['– Phiếu Đang tạo không hiện với bất kỳ ai khác người lập, kể cả Super admin và người có quyền xem tổng công ty.'], ['Xem danh sách', 'Xem chi tiết']),
        ('BR-04', 'Số phiếu', ['– Dạng <mã công ty của người lập>.YCMDV.<năm hiện tại><6 chữ số theo số thứ tự phiếu trong hệ thống>, vd TPE.YCMDV.2026000090.', '– Sinh khi lưu lần đầu (kể cả Lưu nháp), không đổi khi sửa.'], ['Lập phiếu']),
        ('BR-05', 'Nút theo trạng thái và vai trò', ['– Sửa, Xóa: người lập, phiếu Đang tạo / Không duyệt.', '– Trưởng phòng duyệt: phiếu Chờ TP duyệt, người có quyền TP. Kiểm soát duyệt giá: phiếu Chờ KS duyệt, người có quyền KS cùng công ty. Từ chối: người có một trong hai nút duyệt trên.', '– Yêu cầu duyệt lại giá, Hủy yêu cầu: người lập, phiếu Đã duyệt. Lập hợp đồng mua dịch vụ: người lập, phiếu Đã duyệt / Đang lập hợp đồng.', '– In phiếu, Lịch sử: luôn có. Nút không dùng được thì ẩn hẳn.', '– Hệ thống kiểm lại khi bấm: sai trạng thái → "Trạng thái đã bị thay đổi. Vui lòng load lại trang"; sai người → câu "Bạn không có quyền …".'], ['Xem danh sách', 'Xem chi tiết', 'Mọi thao tác']),
        ('BR-06', 'Kiểm tra khi lưu', ['– Lưu nháp: chỉ bắt buộc Ghi chú (≤ 255 ký tự); dòng chưa chọn Tên dịch vụ bị bỏ qua.', '– Gửi duyệt: thêm ≥ 1 file đính kèm, ≥ 1 dòng dịch vụ, mỗi dòng Tên dịch vụ, Số lượng, Giá đề xuất (số ≥ 0).', '– VAT (%) 0–100. File: pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip; ≤ 10 MB.'], ['Lập phiếu', 'Sửa']),
        ('BR-07', 'Tính tiền', ['– Thành tiền đề xuất = Số lượng × Giá đề xuất (không gõ tay); Thành tiền duyệt = Số lượng × Giá duyệt.', '– Thành tiền = tổng các dòng; VAT = Thành tiền × VAT %; Tổng thanh toán = Thành tiền + VAT (tính riêng cho đề xuất và duyệt).', '– Hệ thống tự tính lại khi lưu và khi Ban kiểm soát duyệt giá; số hiển thị 1,234,567.89.'], ['Lập phiếu', 'Sửa', 'Ban kiểm soát duyệt giá', 'In phiếu']),
        ('BR-08', 'Trưởng phòng duyệt không giới hạn phòng ban', ['– Người có quyền Trưởng phòng duyệt thấy nút duyệt / từ chối ở mọi phiếu Chờ TP duyệt mà họ mở được (không kiểm phòng ban của phiếu). Ban kiểm soát bắt buộc cùng công ty với phiếu.'], ['Trưởng phòng duyệt', 'Từ chối']),
        ('BR-09', 'Chặn duyệt khi còn hàng quá hạn', ['– Bước Trưởng phòng duyệt bị chặn nếu người duyệt hoặc nhân viên phòng họ quản lý còn hàng quá hạn theo cấu hình hạn "Duyệt yêu cầu mua dịch vụ"; hệ thống hiện lý do và danh sách hàng quá hạn. Super admin không bị chặn.'], ['Trưởng phòng duyệt']),
        ('BR-10', 'Thông báo', ['– Gửi duyệt: báo người có quyền TP cùng công ty với phiếu. Trưởng phòng duyệt / Yêu cầu duyệt lại giá: báo người có quyền KS cùng công ty. Từ chối: báo người lập kèm người từ chối và lý do.', '– Nội dung "[YCMDV] <hành động>: <số phiếu>. <ghi chú>", bấm mở trang Chi tiết. Lỗi gửi thông báo không làm hỏng thao tác.'], ['Lập phiếu', 'Sửa', 'Duyệt', 'Từ chối', 'Yêu cầu duyệt lại giá']),
        ('BR-11', 'Trạng thái lập hợp đồng', ['– Đang lập hợp đồng / Đã lập hợp đồng và số lượng đã lập hợp đồng của từng dòng do màn Hợp đồng mua dịch vụ cập nhật; HRM chỉ hiển thị.', '– Sửa phiếu không làm mất số lượng đã lập hợp đồng của dòng dịch vụ (giữ theo Tên dịch vụ + Nhà cung cấp).'], ['Lập hợp đồng mua dịch vụ', 'Sửa']),
        ('BR-12', 'In và xuất', ['– In danh sách và Xuất Excel theo đúng bộ lọc + phạm vi đang áp dụng (mọi trang); in danh sách tối đa 2,000 dòng.', '– In phiếu dùng tiêu đề của công ty ghi trên phiếu.'], ['In phiếu', 'In danh sách', 'Xuất Excel']),
        ('BR-13', 'Thao tác xong quay về danh sách', ['– Lưu (Tạo / Sửa), Xóa, Duyệt, Duyệt giá, Từ chối, Yêu cầu duyệt lại giá, Hủy yêu cầu xong đều về màn danh sách.'], ['Mọi thao tác ghi']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây đọc hoặc dùng dữ liệu phiếu Yêu cầu mua dịch vụ. Ngoài ra, màn lập Hợp đồng mua dịch vụ (chưa có trên HRM) đọc phiếu Đã duyệt và cập nhật trạng thái lập hợp đồng (BR-11).',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng',
    'mains': [('FR-01', 'Xem danh sách phiếu', 'view'), ('FR-04', 'Lập phiếu yêu cầu mua dịch vụ', 'crud'),
              ('FR-05', 'Sửa phiếu', 'crud'), ('FR-07', 'Xóa phiếu', 'action'),
              ('FR-08', 'Trưởng phòng duyệt', 'action'), ('FR-09', 'Ban kiểm soát duyệt giá', 'action'),
              ('FR-10', 'Từ chối phiếu', 'action'), ('FR-11', 'Yêu cầu duyệt lại giá', 'action'),
              ('FR-12', 'Hủy yêu cầu', 'action'), ('FR-14', 'In phiếu', 'io'),
              ('FR-15', 'In danh sách', 'io'), ('FR-16', 'Xuất Excel danh sách', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc danh sách', 'view'), ('FR-03', 'Cài đặt bộ lọc, tuỳ chỉnh cột', 'view'),
             ('FR-06', 'Xem chi tiết phiếu', 'view'), ('FR-13', 'Lập hợp đồng mua dịch vụ', 'view'),
             ('FR-17', 'Xem lịch sử thay đổi', 'view')],
    'rieng': [('FR-04', 'Lập phiếu yêu cầu mua dịch vụ', 'crud', 'uc_them'), ('FR-05', 'Sửa phiếu', 'crud', 'uc_sua'),
              ('FR-06', 'Xem chi tiết phiếu', 'view', 'uc_xem'), ('FR-07', 'Xóa phiếu', 'action', 'uc_xoa'),
              ('FR-08', 'Trưởng phòng duyệt', 'action', 'uc_tpduyet'), ('FR-09', 'Ban kiểm soát duyệt giá', 'action', 'uc_ksduyet'),
              ('FR-10', 'Từ chối phiếu', 'action', 'uc_tuchoi'), ('FR-11', 'Yêu cầu duyệt lại giá', 'action', 'uc_duyetlai'),
              ('FR-12', 'Hủy yêu cầu', 'action', 'uc_huy'), ('FR-14', 'In phiếu', 'io', 'uc_inphieu'),
              ('FR-15', 'In danh sách', 'io', 'uc_in'), ('FR-16', 'Xuất Excel danh sách', 'io', 'uc_xuat')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    _state_flow.draw(os.path.join(scr.uml, 'state_flow.png'))
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))

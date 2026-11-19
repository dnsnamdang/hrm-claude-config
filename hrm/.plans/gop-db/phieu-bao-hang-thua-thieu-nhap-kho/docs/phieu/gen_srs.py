# -*- coding: utf-8 -*-
"""SRS - Phiếu báo hàng thừa, thiếu nhập kho (STT 289) — khuôn PHIẾU đợt 3 (màn mẫu finance-declare-debt-beginning/docs/kh).

Nguồn (code HRM develop, 18/11/2026):
  FE hrm-client/pages/warehouse/exc-shortage-imports/{index, create, _id/index, _id/edit}.vue,
     components/{ExcShortageForm, RejectModal}.vue, components/{constants, row-actions}.js; components/subsystem-menu/warehouse.js
  BE Modules/Finance: Http/Controllers/V1/ExcShortageController.php, Services/ExcShortage/{ExcShortageService,
     ExcShortageWriteService}.php, Entities/ExcShortage/ExcShortageWarehouseImport.php;
     app/Support/Permissions/Catalog/warehouse.php (3 quyền)
  Ảnh: capture.js (dev-hrm 18/11/2026). Màn 288 (hàng chờ) ở ../cho-bao/.
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402
from _lib_phieu import ui, UI4, UI4W, UI6, UI6W, UI7, UI7W, UI8, UI8W, TRUOC_LUU  # noqa: E402

TEN = 'Phiếu báo hàng thừa, thiếu nhập kho'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q_XEM = 'Xem xử lý thừa thiếu nhập kho'
Q_TAO = 'Tạo phiếu báo hàng thừa, thiếu nhập kho'
Q_DUYET = 'Duyệt phiếu báo hàng thừa, thiếu nhập kho'
TN = 'Người dùng đăng nhập hệ thống (dữ liệu theo phạm vi xem — Phần 2)'
DK = '1. Người dùng đăng nhập thành công.'
DK_SUA = DK + '\n2. Người dùng là NGƯỜI TẠO phiếu.\n3. Phiếu ở trạng thái Đang tạo hoặc Không duyệt.'
DK_DUYET = DK + '\n2. Người dùng có quyền "%s", phiếu thuộc phạm vi xem.\n3. Phiếu ở trạng thái Chờ xử lý.' % Q_DUYET
TRANG = 'Trang %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'
CU = 'màn hình thuộc hệ thống quản lý kho cũ, mở ở tab mới'
NOT_FOUND = 'chuyển sang trang "Không tìm thấy"'
DOI_TT = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'

P5 = [
    ('Kho', 'Phiếu nhập kho chờ báo thừa, thiếu (nút "Báo hàng thừa thiếu" mở trang Tạo phiếu báo đã nạp sẵn phiếu nhập kho; phiếu nhập kho đã có phiếu báo — mọi trạng thái — rời khỏi hàng chờ, xóa phiếu báo thì quay lại)',
     'Kho => Nhập kho => Phiếu nhập kho chờ báo thừa, thiếu'),
    ('Kho', 'Phiếu nhập kho (nguồn dữ liệu: mã phiếu, nhà cung cấp, dòng hàng lệch số lượng; ô Phiếu nhập kho là liên kết mở chi tiết)',
     'Kho => Nhập kho => Phiếu nhập kho (hoặc Tài chính => Nhập hàng => Phiếu nhập kho)'),
    ('Tài chính', 'Yêu cầu nhập hàng (ô Yêu cầu nhập là liên kết mở chi tiết; đơn giá nhà cung cấp của yêu cầu được lưu kèm dòng hàng)',
     'Tài chính => Nhập hàng => Yêu cầu nhập hàng'),
    ('Mua hàng', 'Hợp đồng mua trong nước / hợp đồng mua nước ngoài (ô Số hợp đồng mở hợp đồng — %s)' % CU,
     'Hệ thống quản lý kho cũ'),
    ('Kho', 'Lập phiếu xử lý hàng thiếu nhập kho (nút "Xử lý" — %s; lập phiếu xử lý xong thì phiếu báo chuyển Đã xử lý)' % CU,
     'Hệ thống quản lý kho cũ'),
    ('Chung', 'Thông báo (chuông): "[BHNK] Chờ duyệt: <số phiếu>" gửi người duyệt, "[BHNK] Không duyệt: <số phiếu>" gửi người tạo; bấm thông báo mở trang Chi tiết phiếu',
     'Biểu tượng chuông trên thanh tiêu đề'),
]

FR = []

# 2.1 -------------------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách phiếu báo hàng thừa, thiếu nhập kho',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách phiếu báo hàng thừa, thiếu nhập kho'],
        ['Mô tả', 'Hiển thị các phiếu báo hàng thừa, thiếu trong phạm vi xem của người dùng, có phân trang, sắp xếp, nhãn trạng thái màu và nút thao tác theo từng dòng.'],
        ['Tác nhân', TN],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), phiếu tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Không có phiếu khớp → bảng hiện "Không có dữ liệu phù hợp."\n• Phạm vi dữ liệu theo quyền xem (Phần 2, BR-02).\n• Nút trên dòng hiện theo trạng thái phiếu và quyền (BR-05).'],
    ],
    'anh': [('01_list', 'Màn danh sách Phiếu báo hàng thừa, thiếu nhập kho lúc mới truy cập'),
            ('01b_list_actions', 'Cột Hành động: phiếu Đang tạo có Sửa, Xóa, Lịch sử; phiếu Chờ xử lý có Xử lý, Lịch sử; phiếu Đã xử lý chỉ có Lịch sử')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Danh sách phiếu báo hàng thừa, thiếu nhập kho', 'Tiêu đề trang: "Phiếu báo hàng thừa, thiếu nhập kho".'],
        ['Nút Tạo mới', 'Button', 'Enable / Ẩn', 'Hiển thị', 'Chỉ hiện khi có quyền "%s"; mở trang Tạo phiếu (mục 2.4).' % Q_TAO],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất Excel" (mục 2.11). Trong lúc xuất, cạnh nút hiện dòng tiến độ.'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.3).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa.'],
        ['Cột Số phiếu', 'Table/Grid', 'Read-only', 'Hiển thị', '- Dạng <mã công ty>_BHNK-<5 chữ số> (BR-03).\n- Sắp xếp được. Liên kết mở trang Chi tiết (mục 2.7). Cột khóa.'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Phiếu nhập kho', 'Table/Grid', 'Read-only', 'Hiển thị', 'Mã phiếu nhập kho nguồn; liên kết mở chi tiết phiếu nhập kho ở tab mới.'],
        ['Cột Yêu cầu nhập', 'Table/Grid', 'Read-only', 'Hiển thị', 'Mã yêu cầu nhập hàng của phiếu nhập kho; liên kết mở chi tiết ở tab mới.'],
        ['Cột Nhà cung cấp', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên nhà cung cấp của phiếu nhập kho; không có thì để trống.'],
        ['Cột Số hợp đồng', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số hợp đồng mua; liên kết mở hợp đồng (%s).' % CU],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', '"Mã phòng ban - Họ tên" người lập phiếu.'],
        ['Cột Trạng thái', 'Table/Grid', 'Read-only', 'Hiển thị', 'Nhãn màu: Đang tạo (xám), Chờ xử lý (vàng), Đã xử lý (xanh lá), Không duyệt (đỏ).'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sửa, Xóa: phiếu Đang tạo / Không duyệt của chính mình.\n- Xử lý: phiếu Chờ xử lý, người có quyền "%s".\n- Lịch sử: luôn có.\n- Nút không dùng được thì ẩn. Cột khóa.' % Q_DUYET],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Mục menu hiện với mọi người dùng; dữ liệu giới hạn theo phạm vi xem (BR-02).\nAfter:\n– Tải trang 1, phiếu tạo gần nhất trên cùng; khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút).'],
        ['Bấm tiêu đề cột Số phiếu / Ngày tạo', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại dữ liệu từ trang 1.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp; đổi số dòng thì quay về trang 1.'],
        ['Bấm Số phiếu', 'Click', 'After:\n– Mở trang Chi tiết phiếu (mục 2.7).'],
        ['Bấm Phiếu nhập kho / Yêu cầu nhập / Số hợp đồng', 'Click', 'After:\n– Mở chứng từ tương ứng ở tab mới.'],
    ],
})

# 2.2 -------------------------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc danh sách',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách phiếu báo'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao.'],
        ['Tác nhân', TN],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập số phiếu rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn / nhập giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô gõ chữ (tìm nhanh, Phiếu nhập kho, Yêu cầu nhập, Hợp đồng, Hàng hóa) chỉ lọc khi bấm Tìm kiếm / Enter; ô chọn lọc ngay khi chọn.\n• Bấm Làm mới → xoá mọi điều kiện, tải lại danh sách.\n• Ô Công ty chỉ hiện khi người dùng xem được mức Tổng công ty.\n• Hệ thống ghi nhớ bộ lọc 10 phút khi sang trang Chi tiết / Sửa rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực Tìm kiếm nâng cao ở trạng thái mở')],
    'ui': ui(UI7, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Tìm theo số phiếu"; tìm gần đúng theo Số phiếu.'],
        ['Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Áp dụng điều kiện / xoá mọi điều kiện và tải lại.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực ô lọc (khi mở đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" (mục 2.3).'],
        ['Ô Phiếu nhập kho', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Tìm gần đúng theo mã phiếu nhập kho.'],
        ['Ô Yêu cầu nhập', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Tìm gần đúng theo mã yêu cầu nhập.'],
        ['Ô Hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Tìm gần đúng theo số hợp đồng.'],
        ['Ô Hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Phiếu có ít nhất 1 dòng hàng có mã hoặc tên chứa từ khóa.'],
        ['Ô Nhà cung cấp', 'Dropdown', 'Enable', 'Nhà cung cấp có trên phiếu trong phạm vi', 'Trống', 'Nhà cung cấp đã khóa vẫn hiện, kèm biểu tượng khóa.'],
        ['Ô Trạng thái', 'Dropdown', 'Enable', 'Đang tạo / Chờ xử lý / Đã xử lý / Không duyệt', 'Trống', 'Trống = mọi trạng thái.'],
        ['Ô Người tạo', 'Dropdown', 'Enable', 'Người đã lập phiếu trong phạm vi', 'Trống', 'Hiển thị "Mã phòng ban - Họ tên".'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy, Từ → Đến', 'Trống', 'Lọc theo ngày tạo phiếu, tính cả 2 đầu mút.'],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Công ty đang hoạt động', 'Trống', 'Chỉ hiện với người xem mức Tổng công ty; lọc theo công ty của phiếu.'],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm Tìm kiếm / Enter ở ô gõ chữ', 'Click', 'After:\n– Áp đồng thời từ khóa và các ô lọc, tải lại bảng từ trang 1.'],
        ['Chọn giá trị ở ô chọn', 'Change', 'After:\n– Tải lại bảng từ trang 1 ngay.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khu vực ô lọc; lần mở đầu tải danh sách giá trị cho các ô chọn.'],
    ],
})

# 2.3 -------------------------------------------------------------------------
FR.append({
    'ten': 'Cài đặt bộ lọc và tuỳ chỉnh cột',
    'qtc': 'Bộ lọc, Cấu hình cột và lưu cấu hình theo người dùng.',
    'gioi_thieu': [
        ['Tên chức năng', 'Cài đặt bộ lọc và tuỳ chỉnh cột'],
        ['Mô tả', 'Chọn ô lọc nào hiển thị / thứ tự ô lọc, và cột nào hiển thị / thứ tự cột. Cấu hình lưu theo từng người dùng, từng màn.'],
        ['Tác nhân', TN],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Bấm "Cài đặt bộ lọc" (hoặc biểu tượng Cấu hình cột hiển thị).\n2. Tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n3. Bấm Lưu: hệ thống lưu cấu hình và áp dụng ngay.'],
        ['Dòng sự kiện phụ', '• Bấm Đóng: bỏ thay đổi.\n• Cài đặt bộ lọc có nút "Khôi phục mặc định".\n• Cột STT, Số phiếu, Hành động không bỏ được (biểu tượng khóa).'],
    ],
    'menu_them': ' => Cài đặt bộ lọc {icon:btn_caidatboloc} / Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': 'Modal Cài đặt bộ lọc và Modal Tuỳ chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('26_filtercfg', 'Cửa sổ Cài đặt bộ lọc'), ('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột')],
    'ui': ui(UI6, [
        ['Danh sách ô lọc', 'Checkbox', 'Enable', 'Đủ 9 ô (8 ô nếu không có ô Công ty)', 'Tích ô lọc muốn hiện, kéo đổi thứ tự.'],
        ['Nút Khôi phục mặc định', 'Button', 'Enable', '–', 'Đưa cấu hình ô lọc về mặc định.'],
        ['Danh sách cột', 'Checkbox', 'Enable', '10/10 cột', 'Tích cột muốn hiện; STT, Số phiếu, Hành động bị khóa. Dòng đếm "Đang chọn x/10 cột".'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Chọn / bỏ nhanh mọi cột (trừ cột khóa).'],
        ['Nút Lưu', 'Button', 'Enable', '–', 'Lưu cấu hình theo người dùng, áp dụng ngay.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ, không lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình theo người dùng, đóng cửa sổ, bảng / khu vực lọc vẽ lại.'],
        ['Kéo thả dòng', 'Drag', 'After:\n– Đổi thứ tự dòng trong cửa sổ.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ, không lưu.'],
    ],
})

# 2.4 -------------------------------------------------------------------------
FR.append({
    'ten': 'Lập phiếu báo hàng thừa, thiếu', 'uc': 'uc_them', 'uc_ten': 'FR-04 Lập phiếu báo hàng thừa, thiếu',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Lập phiếu báo hàng thừa, thiếu nhập kho'],
        ['Mô tả', 'Chọn 1 phiếu nhập kho đang chờ báo thừa, thiếu; hệ thống tự điền Yêu cầu nhập, Số hợp đồng, Nhà cung cấp và bảng hàng lệch số lượng (chỉ đọc). Người dùng nhập Diễn giải, đính kèm file rồi Lưu (trạng thái Đang tạo) hoặc Lưu và gửi (Chờ xử lý). Phiếu báo KHÔNG ghi tồn kho, không sinh bút toán.'],
        ['Tác nhân', 'Người dùng có quyền "%s"' % Q_TAO],
        ['Điều kiện ban đầu', DK + '\n2. Người dùng có quyền "%s".\n3. Có phiếu nhập kho chờ báo thừa, thiếu trong phạm vi (BR-01).' % Q_TAO],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới (hoặc "Báo hàng thừa thiếu" ở màn Phiếu nhập kho chờ báo thừa, thiếu — ô Phiếu nhập kho được điền sẵn).\n2. Hệ thống mở trang "Tạo phiếu báo hàng thừa, thiếu nhập kho"; góc phải khối Thông tin chung hiện "<Người đăng nhập> - <ngày giờ hiện tại>".\n3. Người dùng chọn Phiếu nhập kho (mục 2.5); hệ thống điền Yêu cầu nhập, Số hợp đồng, Nhà cung cấp và bảng Chi tiết.\n4. Người dùng nhập Diễn giải, bấm "Thêm tài liệu" → "Chọn tệp" để đính kèm file (file được tải lên ngay).\n5. Bấm Lưu hoặc Lưu và gửi.\n6. Hệ thống kiểm tra, lấy lại dòng hàng lệch từ phiếu nhập kho, sinh số phiếu (BR-03), ghi phiếu với công ty / phòng ban / bộ phận của người lập.\n7. Ghi nhận Tạo mới trong lịch sử; Lưu và gửi thì gửi thông báo "Chờ duyệt" cho người duyệt (BR-08).\n8. Báo "Lưu thành công." / "Lưu và gửi thành công.", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Bấm "Lưu và tiếp tục": lưu ở trạng thái Đang tạo rồi mở lại trang Tạo trống.\n• Thiếu dữ liệu → báo đỏ dưới đúng ô + toast "Bạn chưa nhập đầy đủ thông tin.", cuộn tới ô lỗi đầu tiên, không lưu.\n• Phiếu nhập kho vừa có phiếu báo khác / không còn đủ điều kiện → dưới ô Phiếu nhập kho: "Phiếu nhập kho không còn chờ báo thừa, thiếu (đã có phiếu báo hoặc không đủ điều kiện)." (BR-04).\n• Bấm × trong ô Phiếu nhập kho → bỏ chọn, xoá bảng Chi tiết, giữ Diễn giải và file.\n• Bấm Quay lại: chưa nhập gì thì về danh sách; đã nhập thì hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', 'Nút lưu bị khóa từ lúc bấm tới khi có kết quả, tránh lưu 2 lần; 2 người lưu cùng lúc cho 1 phiếu nhập kho thì chỉ 1 phiếu báo được tạo.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': TRANG % '"Tạo phiếu báo hàng thừa, thiếu nhập kho"',
    'anh': [('10_create', 'Trang Tạo phiếu báo hàng thừa, thiếu nhập kho lúc mới mở'),
            ('11_validate', 'Bấm Lưu khi chưa nhập: báo đỏ dưới từng ô bắt buộc'),
            ('10b_create_filled', 'Đã chọn phiếu nhập kho, nhập Diễn giải và đính kèm file (ảnh điền tạm trên trình duyệt)'),
            ('18_unsaved', 'Hộp xác nhận Thông tin chưa lưu khi bấm Quay lại')],
    'ui': ui(UI8, [
        ['Người tạo - ngày giờ', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại', 'Góc phải khối Thông tin chung.'],
        ['Phiếu nhập kho', 'Popup chọn', 'Enable', 'Phiếu nhập kho chờ báo thừa, thiếu', 'Có', 'Trống (hoặc điền sẵn khi vào từ màn hàng chờ)', '- Placeholder "Chọn phiếu nhập kho..."; bấm vào ô mở cửa sổ chọn (mục 2.5); nút × bỏ chọn.\n- Bỏ trống: "Phiếu nhập kho – Vui lòng chọn phiếu nhập kho."'],
        ['Yêu cầu nhập', 'Label', 'Read-only', '–', '–', 'Theo phiếu nhập kho', 'Liên kết mở yêu cầu nhập hàng ở tab mới.'],
        ['Số hợp đồng', 'Label', 'Read-only', '–', '–', 'Theo phiếu nhập kho', 'Biểu tượng ⓘ: hợp đồng mua mở ở hệ thống quản lý kho cũ. Liên kết mở hợp đồng ở tab mới.'],
        ['Nhà cung cấp', 'Textbox', 'Read-only', '–', '–', 'Theo phiếu nhập kho', 'Không có thì để trống.'],
        ['Diễn giải', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống', '- Placeholder "Nhập diễn giải"; không gõ được quá 255 ký tự.\n- Bỏ trống / chỉ khoảng trắng: "Diễn giải – Vui lòng nhập diễn giải."'],
        ['Khối File đính kèm', 'File', 'Enable', 'ppt, pptx, doc, docx, pdf, xls, xlsx, jpg, jpeg, png, zip; ≤ 15MB/file', 'Có (≥ 1 file)', 'Trống', '- Nút "Thêm tài liệu" thêm dòng, "Chọn tệp" chọn file (rê chuột hiện định dạng / dung lượng cho phép); file tải lên ngay.\n- Mỗi dòng: tên file, Xem trước, Tải xuống, Thay đổi, Dung lượng, Xóa.\n- Sai định dạng: "File "<tên>" không thuộc định dạng cho phép"; quá dung lượng: "File "<tên>" vượt quá 15MB".\n- Không có file: "File đính kèm – Vui lòng đính kèm ít nhất 1 file."'],
        ['Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', '–', '"Chọn phiếu nhập kho để nạp hàng hóa lệch số lượng"', 'STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, SL đề nghị nhập, SL thực nhập, SL thiếu (đỏ), SL thừa (xanh) — chỉ các dòng lệch (BR-06).'],
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu ở trạng thái Đang tạo, về danh sách.'],
        ['Nút Lưu và gửi', 'Button', 'Enable', '–', '–', '–', 'Lưu ở trạng thái Chờ xử lý, gửi thông báo người duyệt, về danh sách.'],
        ['Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', '–', 'Lưu (Đang tạo) rồi mở lại trang Tạo trống.'],
        ['Nút Quay lại', 'Button', 'Enable', '–', '–', '–', 'Về danh sách (đã nhập thì hỏi "Thông tin chưa lưu").'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'Before:\n– Nút chỉ hiện khi có quyền "%s".\nAfter:\n– Mở trang Tạo trống.' % Q_TAO],
        ['Chọn phiếu nhập kho', 'Change', 'Before:\n– Phiếu nhập kho phải còn chờ báo thừa, thiếu và thuộc phạm vi; không thì toast "Phiếu nhập kho không còn chờ báo thừa, thiếu hoặc bạn không có quyền."\nAfter:\n– Điền Yêu cầu nhập, Số hợp đồng, Nhà cung cấp, bảng Chi tiết; xoá lỗi dưới ô.'],
        ['Chọn tệp', 'Change', 'During:\n– Kiểm định dạng, dung lượng.\nAfter:\n– Tải file lên kho lưu trữ, thêm dòng file vào khối (chưa gắn vào phiếu cho tới khi lưu).'],
        ['Bấm Lưu / Lưu và gửi / Lưu và tiếp tục', 'Click', 'Before:\n– Kiểm tra quyền "%s".\nDuring:\n– Phiếu nhập kho bắt buộc và còn chờ báo; Diễn giải 1–255 ký tự; có ≥ 1 file hợp lệ.\n' % Q_TAO + TRUOC_LUU + '\nAfter:\n– Lấy lại dòng hàng lệch từ phiếu nhập kho, sinh số phiếu, ghi phiếu (Lưu / Lưu và tiếp tục: Đang tạo; Lưu và gửi: Chờ xử lý, ghi thời điểm gửi).\n– Ghi nhận Tạo mới trong lịch sử; Lưu và gửi: gửi thông báo người duyệt.\n– Báo kết quả; về danh sách (Lưu và tiếp tục: trang Tạo trống).'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa nhập gì → về danh sách.\n– Đã nhập → hộp "Thông tin chưa lưu" ("Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"): Thoát về danh sách không lưu, Ở lại về form.'],
    ],
})

# 2.5 -------------------------------------------------------------------------
FR.append({
    'ten': 'Chọn phiếu nhập kho', 'uc': 'uc_chonpnk', 'uc_ten': 'FR-05 Chọn phiếu nhập kho chờ báo thừa, thiếu',
    'qtc': 'Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chọn phiếu nhập kho'],
        ['Mô tả', 'Cửa sổ "Chọn phiếu nhập kho" (dòng phụ "Phiếu nhập kho đã hạch toán có hàng thừa / thiếu, chưa có phiếu báo") liệt kê đúng các phiếu của màn Phiếu nhập kho chờ báo thừa, thiếu trong phạm vi người dùng. Bấm vào dòng là chọn và đóng cửa sổ.'],
        ['Tác nhân', 'Người dùng có quyền "%s"' % Q_TAO],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở trang Tạo phiếu báo.'],
        ['Dòng sự kiện chính', '1. Bấm vào ô Phiếu nhập kho.\n2. Hệ thống mở cửa sổ, tải trang 1 (10 dòng, mới nhất trên cùng).\n3. Người dùng tìm theo Mã phiếu (nếu cần) và bấm vào dòng.\n4. Hệ thống đóng cửa sổ, điền phiếu nhập kho và dữ liệu đi kèm vào form.'],
        ['Dòng sự kiện phụ', '• Bấm vào chữ Mã phiếu: mở chi tiết phiếu nhập kho ở tab mới (không chọn dòng).\n• Không có phiếu phù hợp: "Không có dữ liệu phù hợp."\n• Bấm Đóng / (x): đóng cửa sổ, form giữ nguyên.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi} => Phiếu nhập kho {icon:o_chonpnk}',
    'ghi_chu_layout': 'Modal Chọn phiếu nhập kho được mở ngay trên trang Tạo phiếu báo theo đường dẫn ở trên.',
    'anh': [('14_picker', 'Cửa sổ Chọn phiếu nhập kho')],
    'ui': ui(UI8, [
        ['Ô Mã phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Placeholder "Mã phiếu nhập kho"; tìm gần đúng, lọc khi Enter / Tìm kiếm.'],
        ['Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', '–', 'Áp dụng / xoá điều kiện tìm.'],
        ['Cột STT, Mã phiếu, Loại, Nhà cung cấp, Phiếu ĐNNK, Ngày tạo', 'Table/Grid', 'Read-only', '–', '–', '–', 'Mã phiếu là liên kết mở phiếu nhập kho ở tab mới. Mã phiếu, Ngày tạo sắp xếp được.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 / 20 / 50 dòng', '–', '10', '"Hiển thị a–b / N".'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ, không chọn.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Mở cửa sổ', 'System', 'After:\n– Tải phiếu nhập kho chờ báo thừa, thiếu trong phạm vi (BR-01, BR-02).'],
        ['Bấm vào dòng', 'Click', 'After:\n– Đóng cửa sổ, nạp dữ liệu phiếu nhập kho vào form.'],
        ['Bấm Tìm kiếm / tiêu đề cột', 'Click', 'After:\n– Tải lại từ trang 1 theo điều kiện / thứ tự mới.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.6 -------------------------------------------------------------------------
FR.append({
    'ten': 'Sửa phiếu báo', 'uc': 'uc_sua', 'uc_ten': 'FR-06 Sửa phiếu báo hàng thừa, thiếu',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Sửa phiếu báo hàng thừa, thiếu nhập kho'],
        ['Mô tả', 'Người tạo sửa phiếu Đang tạo hoặc Không duyệt: chỉ đổi được Diễn giải và file đính kèm; Phiếu nhập kho và bảng Chi tiết cố định. Lưu (về Đang tạo) hoặc Lưu và gửi (Chờ xử lý).'],
        ['Tác nhân', 'Người tạo phiếu'],
        ['Điều kiện ban đầu', DK_SUA],
        ['Dòng sự kiện chính', '1. Bấm Sửa ở cột Hành động (hoặc nút Sửa ở trang Chi tiết).\n2. Hệ thống mở trang "Sửa phiếu báo hàng thừa, thiếu: <số phiếu>"; phiếu Không duyệt hiện thêm ô "Lý do không duyệt" (chỉ đọc).\n3. Người dùng sửa Diễn giải, thêm / xóa file, bấm Lưu hoặc Lưu và gửi.\n4. Hệ thống kiểm tra, ghi thay đổi.\n5. Ghi nhận Thay đổi thông tin (và Thay đổi trạng thái nếu trạng thái đổi) trong lịch sử; Lưu và gửi thì gửi thông báo người duyệt.\n6. Báo "Lưu thành công." / "Lưu và gửi thành công.", về danh sách.'],
        ['Dòng sự kiện phụ', '• Xóa file ĐÃ LƯU: hỏi "Bạn có chắc muốn xóa file đính kèm này?"; đồng ý thì file bị gỡ khỏi phiếu NGAY (không chờ bấm Lưu), báo "Xóa file thành công", ghi lịch sử.\n• Mở trang Sửa khi phiếu không còn sửa được (đã gửi / không phải người tạo) → tự chuyển sang trang Chi tiết.\n• Phiếu vừa đổi trạng thái khi đang sửa → bấm lưu báo %s, không lưu.\n• Bấm Quay lại khi đã sửa → hỏi "Thông tin chưa lưu".' % DOI_TT],
    ],
    'menu_them': ' => Sửa {icon:btn_sua}',
    'ghi_chu_layout': TRANG % '"Sửa phiếu báo hàng thừa, thiếu"',
    'anh': [('12_edit', 'Trang Sửa phiếu báo hàng thừa, thiếu (phiếu Đang tạo)')],
    'ui': ui(UI8, [
        ['Phiếu nhập kho', 'Label', 'Read-only', '–', '–', 'Dữ liệu hiện tại', 'Biểu tượng ⓘ: "Phiếu nhập kho không đổi được sau khi tạo phiếu báo."; liên kết mở phiếu nhập kho.'],
        ['Yêu cầu nhập, Số hợp đồng, Nhà cung cấp', 'Label', 'Read-only', '–', '–', 'Dữ liệu hiện tại', 'Như trang Tạo.'],
        ['Diễn giải', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Dữ liệu hiện tại', 'Như trang Tạo.'],
        ['Lý do không duyệt', 'Textbox', 'Read-only / Ẩn', '–', '–', 'Lý do (người duyệt - thời điểm)', 'Chỉ hiện khi phiếu đã từng bị Không duyệt.'],
        ['Khối File đính kèm', 'File', 'Enable', 'Như trang Tạo', 'Không', 'File đã lưu', 'Thêm file mới như trang Tạo; file đã lưu chỉ Xem trước / Tải xuống / Xóa (không Thay đổi).'],
        ['Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', '–', 'Dòng hàng đã lưu', 'Không sửa được.'],
        ['Nút Lưu / Lưu và gửi', 'Button', 'Enable', '–', '–', '–', 'Như trang Tạo. Trang Sửa không có "Lưu và tiếp tục".'],
        ['Nút Quay lại', 'Button', 'Enable', '–', '–', '–', 'Về danh sách (đã sửa thì hỏi "Thông tin chưa lưu").'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện với người tạo khi phiếu Đang tạo / Không duyệt.\nAfter:\n– Tải phiếu; ngoài phạm vi / không còn → %s.' % NOT_FOUND],
        ['Bấm Lưu / Lưu và gửi', 'Click', 'Before:\n– Phiếu phải còn Đang tạo / Không duyệt và người dùng là người tạo; không thì %s.\nDuring:\n– Diễn giải 1–255 ký tự; file mới hợp lệ.\n' % DOI_TT + TRUOC_LUU + '\nAfter:\n– Ghi Diễn giải, nối thêm file mới; Lưu → Đang tạo, Lưu và gửi → Chờ xử lý (ghi thời điểm gửi).\n– Ghi nhận Thay đổi thông tin (cũ → mới) và Thay đổi trạng thái (nếu đổi) trong lịch sử.\n– Lưu và gửi: thông báo người duyệt. Về danh sách.'],
        ['Xác nhận xóa file đã lưu', 'Click', 'Before:\n– Phiếu phải còn sửa được.\nAfter:\n– Gỡ file khỏi phiếu và kho lưu trữ, ghi lịch sử, báo "Xóa file thành công".'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa đổi gì → về danh sách; đã đổi → hỏi "Thông tin chưa lưu".'],
    ],
})

# 2.7 -------------------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết phiếu báo', 'uc': 'uc_xem', 'uc_ten': 'FR-07 Xem chi tiết phiếu báo hàng thừa, thiếu',
    'qtc': 'Màn Xem chi tiết và Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết phiếu báo hàng thừa, thiếu nhập kho'],
        ['Mô tả', 'Xem toàn bộ phiếu ở chế độ chỉ đọc kèm khối Lịch sử; nút ở chân trang theo trạng thái và quyền, khớp với nút ở dòng danh sách.'],
        ['Tác nhân', TN],
        ['Điều kiện ban đầu', DK + '\n2. Phiếu thuộc phạm vi xem của người dùng.'],
        ['Dòng sự kiện chính', '1. Bấm Số phiếu ở danh sách (hoặc bấm thông báo của phiếu).\n2. Hệ thống mở trang "Chi tiết phiếu báo hàng thừa, thiếu: <số phiếu>": khối Thông tin chung (góc phải "<Người tạo> - <ngày giờ tạo>"), File đính kèm, Chi tiết, Lịch sử (thu gọn).'],
        ['Dòng sự kiện phụ', '• Đang tạo / Không duyệt (người tạo): Sửa, Xóa, Quay lại.\n• Chờ xử lý (người có quyền Duyệt): Xử lý, Không duyệt, Quay lại.\n• Đã xử lý: chỉ Quay lại.\n• Phiếu Không duyệt hiện ô "Lý do không duyệt" kèm người duyệt và thời điểm.\n• Ngoài phạm vi / không tồn tại: %s.' % NOT_FOUND],
    ],
    'menu_them': ' => Số phiếu (liên kết)',
    'anh': [('17_detail', 'Trang Chi tiết phiếu Chờ xử lý (người có quyền Duyệt): nút Xử lý, Không duyệt'),
            ('17c_detail_draft', 'Trang Chi tiết phiếu Đang tạo (người tạo): nút Sửa, Xóa'),
            ('17d_detail_rejected', 'Trang Chi tiết phiếu Không duyệt: ô Lý do không duyệt (ảnh giả lập trạng thái trên trình duyệt)')],
    'ui': ui(UI6, [
        ['Phiếu nhập kho, Yêu cầu nhập, Số hợp đồng, Nhà cung cấp, Diễn giải', 'Label / Textbox', 'Read-only', 'Dữ liệu phiếu', 'Chỉ đọc; các mã là liên kết mở chứng từ ở tab mới.'],
        ['Lý do không duyệt', 'Textbox', 'Read-only / Ẩn', 'Dữ liệu phiếu', '"<lý do> (<người duyệt> - <dd/mm/yyyy hh:mm>)".'],
        ['Khối File đính kèm', 'File', 'Read-only', 'File đã lưu', 'Xem trước, Tải xuống; không có file thì ẩn khối.'],
        ['Bảng Chi tiết', 'Table/Grid', 'Read-only', 'Dòng hàng đã lưu', 'SL thiếu chữ đỏ, SL thừa chữ xanh; số theo dạng 1,234.5.'],
        ['Khối Lịch sử', 'Label', 'Enable', 'Thu gọn', 'Bấm "Xem lịch sử" để mở (mục 2.12).'],
        ['Nút Xử lý / Không duyệt', 'Button', 'Enable / Ẩn', 'Theo trạng thái + quyền', 'Mục 2.10 / 2.9.'],
        ['Nút Sửa / Xóa', 'Button', 'Enable / Ẩn', 'Theo trạng thái + người tạo', 'Mục 2.6 / 2.8.'],
        ['Nút Quay lại', 'Button', 'Enable', '–', 'Về danh sách.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở trang', 'System', 'Before:\n– Kiểm tra phạm vi xem (BR-02); không đạt → %s.\nAfter:\n– Hiển thị phiếu, tính nút theo trạng thái, người tạo, quyền Duyệt.' % NOT_FOUND],
        ['Bấm Sửa / Xóa / Xử lý / Không duyệt / Quay lại', 'Click', 'After:\n– Mở trang Sửa / hộp Xác nhận xóa / màn lập phiếu xử lý / cửa sổ Không duyệt / về danh sách.'],
    ],
})

# 2.8 -------------------------------------------------------------------------
FR.append({
    'ten': 'Xóa phiếu báo', 'uc': 'uc_xoa', 'uc_ten': 'FR-08 Xóa phiếu báo hàng thừa, thiếu',
    'qtc': 'Quy tắc xóa và Thông báo.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xóa phiếu báo hàng thừa, thiếu nhập kho'],
        ['Mô tả', 'Người tạo xóa hẳn phiếu Đang tạo / Không duyệt cùng các dòng hàng; phiếu nhập kho nguồn quay lại màn Phiếu nhập kho chờ báo thừa, thiếu.'],
        ['Tác nhân', 'Người tạo phiếu'],
        ['Điều kiện ban đầu', DK_SUA],
        ['Dòng sự kiện chính', '1. Bấm Xóa ở cột Hành động (hoặc nút Xóa ở trang Chi tiết).\n2. Hệ thống hiện hộp "Xác nhận xóa": "Bạn có chắc muốn xóa bản ghi này không?"\n3. Bấm Xóa.\n4. Hệ thống ghi nhận Xóa trong lịch sử, xóa dòng hàng và phiếu.\n5. Báo "Xóa thành công.", tải lại danh sách (từ trang Chi tiết: về danh sách).'],
        ['Dòng sự kiện phụ', '• Bấm Hủy / (x) → đóng hộp, không thay đổi.\n• Phiếu vừa được gửi / đổi trạng thái → báo %s, không xóa.\n• Phiếu vừa bị xóa bởi tab khác → báo không tìm thấy phiếu.' % DOI_TT],
    ],
    'menu_them': ' => Xóa {icon:btn_xoa}',
    'ghi_chu_layout': 'Modal Xác nhận xóa được mở ngay trên màn hình danh sách (nút Xóa trên dòng) hoặc trang Chi tiết phiếu (nút Xóa) theo đường dẫn ở trên.',
    'anh': [('13_delete', 'Hộp Xác nhận xóa phiếu báo')],
    'ui': ui(UI4, [
        ['Nút Xóa (cột Hành động / chân trang Chi tiết)', 'Button', 'Biểu tượng thùng rác; chỉ hiện với người tạo khi phiếu Đang tạo / Không duyệt.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận xóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn xóa bản ghi này không?"'],
        ['Nút Xóa', 'Button', 'Xác nhận xóa.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không xóa.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Xóa', 'Click', 'After:\n– Hiện hộp Xác nhận xóa.'],
        ['Bấm Xóa trong hộp', 'Click', 'Before:\n– Kiểm tra phạm vi; phiếu phải Đang tạo / Không duyệt và người dùng là người tạo.\nDuring:\n' + TRUOC_LUU + '\nAfter:\n– Ghi nhận Xóa trong lịch sử, xóa dòng hàng và phiếu; phiếu nhập kho quay lại hàng chờ báo.\n– Báo "Xóa thành công.", tải lại danh sách.'],
        ['Bấm Hủy / (x)', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.9 -------------------------------------------------------------------------
FR.append({
    'ten': 'Không duyệt phiếu báo', 'uc': 'uc_khongduyet', 'uc_ten': 'FR-09 Không duyệt phiếu báo hàng thừa, thiếu',
    'qtc': 'Quy tắc phê duyệt, Thông báo và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Không duyệt phiếu báo hàng thừa, thiếu nhập kho'],
        ['Mô tả', 'Người có quyền Duyệt trả phiếu Chờ xử lý về cho người tạo kèm lý do; phiếu chuyển Không duyệt, người tạo sửa rồi gửi lại.'],
        ['Tác nhân', 'Người dùng có quyền "%s"' % Q_DUYET],
        ['Điều kiện ban đầu', DK_DUYET],
        ['Dòng sự kiện chính', '1. Ở trang Chi tiết bấm Không duyệt.\n2. Hệ thống mở cửa sổ "Không duyệt phiếu báo hàng thừa, thiếu" với ô Lý do không duyệt.\n3. Người dùng nhập lý do, bấm Không duyệt.\n4. Hệ thống chuyển phiếu sang Không duyệt, ghi lý do, người duyệt, thời điểm.\n5. Ghi nhận Không duyệt (Chờ xử lý → Không duyệt, kèm lý do) trong lịch sử; gửi thông báo "Không duyệt" cho người tạo.\n6. Báo "Không duyệt thành công.", về danh sách.'],
        ['Dòng sự kiện phụ', '• Lý do trống / chỉ khoảng trắng: "Vui lòng nhập lý do không duyệt", cửa sổ không đóng.\n• Bấm Hủy / (x): đóng cửa sổ, phiếu giữ Chờ xử lý.\n• Phiếu vừa được xử lý / đổi trạng thái: báo %s.' % DOI_TT],
    ],
    'menu_them': ' => Số phiếu (liên kết) => Không duyệt {icon:btn_khongduyet}',
    'ghi_chu_layout': 'Modal Không duyệt được mở ngay trên trang Chi tiết phiếu theo đường dẫn ở trên.',
    'anh': [('15_reject', 'Cửa sổ Không duyệt phiếu báo'), ('15b_reject_empty', 'Bấm Không duyệt khi chưa nhập lý do')],
    'ui': ui(UI8, [
        ['Lý do không duyệt', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống', 'Placeholder "Nhập lý do không duyệt"; con trỏ tự đặt vào ô khi mở.'],
        ['Nút Không duyệt', 'Button', 'Enable', '–', '–', '–', 'Xác nhận không duyệt.'],
        ['Nút Hủy / (x)', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ, không đổi gì.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Không duyệt (chân trang)', 'Click', 'Before:\n– Nút chỉ hiện khi phiếu Chờ xử lý và người dùng có quyền "%s".\nAfter:\n– Mở cửa sổ, ô lý do trống.' % Q_DUYET],
        ['Bấm Không duyệt (trong cửa sổ)', 'Click', 'Before:\n– Kiểm tra quyền Duyệt, phạm vi; phiếu phải Chờ xử lý.\nDuring:\n– Lý do bắt buộc, tối đa 255 ký tự.\n' + TRUOC_LUU + '\nAfter:\n– Phiếu → Không duyệt; ghi lý do, người duyệt, thời điểm; ghi lịch sử; thông báo người tạo.\n– Báo "Không duyệt thành công.", về danh sách.'],
        ['Bấm Hủy / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.10 ------------------------------------------------------------------------
FR.append({
    'ten': 'Xử lý phiếu báo (lập phiếu xử lý hàng thiếu)', 'uc': 'uc_xuly', 'uc_ten': 'FR-10 Xử lý phiếu báo hàng thừa, thiếu',
    'qtc': 'Quy tắc phê duyệt và liên kết màn hình.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xử lý phiếu báo hàng thừa, thiếu'],
        ['Mô tả', 'Người có quyền Duyệt bấm Xử lý để mở màn "Lập phiếu xử lý hàng thiếu nhập kho" (%s) với phiếu báo được chọn sẵn. Khi phiếu xử lý được lập, phiếu báo chuyển Đã xử lý.' % CU],
        ['Tác nhân', 'Người dùng có quyền "%s"' % Q_DUYET],
        ['Điều kiện ban đầu', DK_DUYET],
        ['Dòng sự kiện chính', '1. Bấm Xử lý ở cột Hành động hoặc chân trang Chi tiết.\n2. Hệ thống mở màn lập phiếu xử lý hàng thiếu nhập kho ở tab mới, gắn sẵn phiếu báo.\n3. Người dùng lập phiếu xử lý tại màn đó; phiếu báo chuyển Đã xử lý.'],
        ['Dòng sự kiện phụ', '• Hệ thống chưa cấu hình địa chỉ màn hình cũ: nút không hiện (ở chân trang báo chưa cấu hình đường dẫn nếu bấm được).\n• Phiếu Đã xử lý: không còn nút Xử lý, Không duyệt, Sửa, Xóa.'],
    ],
    'menu_them': ' => Xử lý {icon:btn_xuly}',
    'ghi_chu_layout': 'Nút Xử lý nằm ở cột Hành động của danh sách và chân trang Chi tiết; màn lập phiếu xử lý mở ở tab mới.',
    'anh': [('17_detail', 'Nút Xử lý ở chân trang Chi tiết phiếu Chờ xử lý')],
    'ui': ui(UI4, [
        ['Nút Xử lý (cột Hành động)', 'Button', 'Biểu tượng dụng cụ; chỉ hiện với phiếu Chờ xử lý và người có quyền Duyệt.'],
        ['Nút Xử lý (chân trang Chi tiết)', 'Button', 'Nút chính màu xanh, đứng đầu chân trang.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Xử lý', 'Click', 'Before:\n– Phiếu Chờ xử lý, người dùng có quyền "%s", phiếu trong phạm vi.\nAfter:\n– Mở màn lập phiếu xử lý hàng thiếu nhập kho ở tab mới (danh sách / chi tiết phiếu báo giữ nguyên).' % Q_DUYET],
    ],
})

# 2.11 ------------------------------------------------------------------------
FR.append({
    'ten': 'Xuất Excel danh sách', 'uc': 'uc_xuat', 'uc_ten': 'FR-11 Xuất Excel danh sách phiếu báo',
    'qtc': 'Quy tắc Excel và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách phiếu báo ra Excel'],
        ['Mô tả', 'Xuất mọi dòng khớp bộ lọc (không chỉ trang đang xem) ra file danh_sach_phieu_bao_hang_thua_thieu_nhap_kho.xlsx, tiêu đề "DANH SÁCH PHIẾU BÁO HÀNG THỪA, THIẾU NHẬP KHO", cột theo lựa chọn và thứ tự người dùng.'],
        ['Tác nhân', TN],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất Excel", tích sẵn đủ 8 trường.\n3. Người dùng tích / bỏ, kéo đổi thứ tự, bấm Xuất file.\n4. Hệ thống tải dữ liệu theo lô (cạnh nút hiện "Đã tải x/y dòng…"), dựng file và tải về; báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Không có dòng nào khớp bộ lọc → báo "Không có dữ liệu để xuất", không tải file.\n• Lỗi khi xuất → "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất Excel')],
    'ui': ui(UI8, [
        ['Danh sách trường', 'Checkbox', 'Enable', '8 trường', 'Có (≥ 1)', 'Tích cả 8', 'Số phiếu, Ngày tạo, Phiếu nhập kho, Yêu cầu nhập, Nhà cung cấp, Số hợp đồng, Người tạo, Trạng thái. File luôn có cột STT đầu.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', 'Chọn / bỏ nhanh mọi trường.'],
        ['Dòng đếm', 'Label', 'Read-only', '–', '–', '–', '"Đang chọn x/8 trường".'],
        ['Nút Xuất file', 'Button', 'Enable', '–', '–', '–', 'Xuất file theo trường đã chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng, không xuất.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất file', 'Click', 'After:\n– Tải dữ liệu theo bộ lọc + phạm vi hiện tại, dựng file đúng thứ tự cột, tải về; báo kết quả.'],
        ['Kéo thả trường', 'Drag', 'After:\n– Đổi thứ tự cột trong file.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.12 ------------------------------------------------------------------------
FR.append({
    'ten': 'Xem lịch sử thay đổi',
    'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem lịch sử thay đổi phiếu báo'],
        ['Mô tả', 'Liệt kê các lần thao tác trên 1 phiếu (Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Không duyệt), mới nhất ở trên, kèm người thực hiện, phòng ban, thời điểm, giá trị cũ → mới (Phiếu nhập kho, Diễn giải, File đính kèm thêm mới / bị xóa).'],
        ['Tác nhân', TN],
        ['Điều kiện ban đầu', DK + '\n2. Phiếu thuộc phạm vi xem.'],
        ['Dòng sự kiện chính', '1. Bấm Lịch sử ở cột Hành động → cửa sổ "Lịch sử thay đổi: <số phiếu>".\n2. Hoặc ở trang Chi tiết bấm "Xem lịch sử" ở khối Lịch sử.\n3. Hệ thống liệt kê các mốc; có nút Bộ lọc (loại hành động, người thực hiện, khoảng ngày).'],
        ['Dòng sự kiện phụ', '• Phiếu chưa có mốc Tạo mới được ghi (phiếu lập trước khi có lịch sử) → hệ thống dựng mốc Tạo mới theo người tạo và ngày tạo của phiếu.\n• Giá trị cũ in đỏ, giá trị mới in xanh; file đính kèm là liên kết mở file.'],
    ],
    'menu_them': ' => Lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': 'Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách; khối Lịch sử nằm cuối trang Chi tiết phiếu.',
    'anh': [('16_history', 'Cửa sổ Lịch sử thay đổi mở từ danh sách'), ('17b_detail_history', 'Khối Lịch sử ở trang Chi tiết')],
    'ui': ui(UI6, [
        ['Tiêu đề', 'Label', 'Read-only', '"Lịch sử thay đổi: <số phiếu>"', '–'],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Lọc theo loại hành động, người thực hiện, Từ ngày, Đến ngày.'],
        ['Mốc lịch sử', 'Label', 'Read-only', 'Mới nhất trên cùng', 'Thời điểm, tên hành động, "Người thực hiện: <họ tên> — <phòng ban>", danh sách trường đổi: cũ → mới.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lịch sử / Xem lịch sử', 'Click', 'Before:\n– Kiểm tra phạm vi xem.\nAfter:\n– Tải và hiển thị các mốc lịch sử của phiếu.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ, danh sách giữ nguyên.'],
    ],
})

FR_NAMES = ['FR-%02d %s' % (i + 1, f['ten']) for i, f in enumerate(FR)]


def _mt(i):
    """Ma trận: Không có quyền · Tạo · Duyệt · Người tạo phiếu (i = chỉ số FR)."""
    chung = 'Có (theo phạm vi)'
    rows = {
        3: ['Không', 'Có', 'Không', '–'], 4: ['Không', 'Có', 'Không', '–'],
        5: ['Không', 'Không', 'Không', 'Có (Đang tạo / Không duyệt)'],
        7: ['Không', 'Không', 'Không', 'Có (Đang tạo / Không duyệt)'],
        8: ['Không', 'Không', 'Có (phiếu Chờ xử lý)', '–'], 9: ['Không', 'Không', 'Có (phiếu Chờ xử lý)', '–'],
    }
    return [FR_NAMES[i]] + rows.get(i, [chung, chung, chung, chung])


S = {
    'ten': TEN, 'ten_ngan': 'phiếu báo hàng thừa, thiếu nhập kho', 'phan_he': 'Kho',
    'menu': [('Kho', 'menu_phanhe'), ('Nhập kho', 'menu_nhom'), (TEN, 'menu_muc')],
    'muc_dich': [
        'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho việc BÁO HÀNG THỪA / THIẾU sau khi nhập kho: phiếu nhập kho đã hạch toán có hàng thực nhập khác số lượng đề nghị được lập phiếu báo để người duyệt xử lý (lập phiếu xử lý hàng thiếu) hoặc trả lại.',
        'Là căn cứ nghiệm thu chức năng, luồng trạng thái và phân quyền của màn hình.',
        'Làm rõ phạm vi dữ liệu theo quyền xem (Tổng công ty / Công ty), quyền Tạo, quyền Duyệt và vai trò người tạo phiếu.',
        'Làm rõ: phiếu báo KHÔNG ghi tồn kho, không sinh bút toán; mỗi phiếu nhập kho chỉ có 1 phiếu báo.',
    ],
    'thuat_ngu': [
        ['Phiếu báo hàng thừa, thiếu nhập kho (phiếu báo)', 'Chứng từ ghi nhận các dòng hàng của 1 phiếu nhập kho có số lượng thực nhập khác số lượng đề nghị nhập; số phiếu dạng <mã công ty>_BHNK-<5 chữ số>.'],
        ['Phiếu nhập kho chờ báo thừa, thiếu', 'Phiếu nhập kho Đã hạch toán, thuộc loại nhập hàng mua, có ít nhất 1 dòng hàng lệch số lượng và chưa có phiếu báo (màn STT 288).'],
        ['SL thiếu / SL thừa', 'SL thiếu = SL đề nghị nhập − SL thực nhập (khi dương); SL thừa = SL thực nhập − SL đề nghị nhập (khi dương).'],
        ['Người duyệt', 'Người có quyền "%s"; được Không duyệt hoặc Xử lý phiếu Chờ xử lý.' % Q_DUYET],
        ['Xử lý', 'Lập phiếu xử lý hàng thiếu nhập kho từ phiếu báo (%s); lập xong phiếu báo chuyển Đã xử lý.' % CU],
        ['Hệ thống quản lý kho cũ', 'Hệ thống chứa các màn chưa chuyển sang (hợp đồng mua, phiếu xử lý hàng thiếu); HRM mở các màn này ở tab mới.'],
    ],
    'trang_thai': {
        'cau_dan': 'Phiếu báo có 4 trạng thái. Người tạo chọn Lưu (Đang tạo) hoặc Lưu và gửi (Chờ xử lý); người duyệt Không duyệt hoặc '
                   'Xử lý. Phiếu báo không ghi tồn kho, không sinh bút toán ở bất kỳ trạng thái nào.',
        'rows': [
            ['Đang tạo', 'Phiếu đã lưu, chưa gửi người duyệt.', 'Xem, Sửa, Xóa, Lưu và gửi, Xuất, Lịch sử', 'Người tạo phiếu'],
            ['Chờ xử lý', 'Phiếu đã gửi, chờ người duyệt xử lý; người duyệt nhận thông báo "Chờ duyệt".', 'Xem, Xử lý, Không duyệt, Xuất, Lịch sử (không Sửa, không Xóa)', 'Người có quyền "%s"' % Q_DUYET],
            ['Không duyệt', 'Người duyệt trả lại kèm lý do; người tạo nhận thông báo "Không duyệt".', 'Xem, Sửa (Lưu → Đang tạo, Lưu và gửi → Chờ xử lý), Xóa, Xuất, Lịch sử', 'Người tạo phiếu'],
            ['Đã xử lý', 'Đã lập phiếu xử lý hàng thiếu nhập kho từ phiếu báo.', 'Xem, Xuất, Lịch sử', 'Tự chuyển khi người duyệt lập phiếu xử lý'],
            ['Đã xóa', 'Phiếu và dòng hàng bị xóa; phiếu nhập kho quay lại hàng chờ báo.', '–', 'Người tạo, chỉ từ Đang tạo / Không duyệt'],
        ],
        'anh': 'state_flow',
        'ghi_chu': ['Lập phiếu mới bằng "Lưu và gửi" thì phiếu vào thẳng Chờ xử lý (không qua Đang tạo). '
                    'Đã xóa không vẽ trên sơ đồ: xóa được từ Đang tạo và Không duyệt (BR-05).'],
    },
    'quyen_truoc': ['Mục menu và màn hình mở được với mọi người dùng đã đăng nhập; quyền quyết định phạm vi dữ liệu và nút thao tác. '
                    'Các quyền thuộc phân hệ Kho, nhóm Nhập kho; Super Admin có mọi quyền.'],
    'quyen_rows': [
        [Q_XEM + ' (mức: Công ty / Tổng công ty)', 'Mở rộng phạm vi xem danh sách, chi tiết, lịch sử, xuất Excel (bảng phạm vi bên dưới); dùng chung với màn Phiếu nhập kho chờ báo thừa, thiếu.'],
        [Q_TAO, 'Thấy nút Tạo mới; lập phiếu báo; chọn phiếu nhập kho (và nút "Báo hàng thừa thiếu" ở màn hàng chờ).'],
        [Q_DUYET, 'Thấy thêm phiếu Chờ xử lý của công ty mình; Không duyệt, Xử lý phiếu Chờ xử lý; nhận thông báo "Chờ duyệt" (nếu đang quản lý phòng ban của người lập).'],
        ['(Người tạo phiếu — không phải quyền)', 'Sửa, Xóa phiếu của chính mình khi phiếu Đang tạo / Không duyệt.'],
    ],
    'pham_vi_truoc': ['Phạm vi dữ liệu (xét theo thứ tự, gặp mức nào trước thì áp mức đó; các dòng 2–4 cộng dồn):'],
    'pham_vi_rows': [
        ['1', Q_XEM + ' — mức Tổng công ty', 'Mọi phiếu của mọi công ty; khu vực lọc có ô Công ty.'],
        ['2', Q_XEM + ' — mức Công ty', 'Phiếu thuộc công ty đang làm việc của người dùng + phiếu mình tạo.'],
        ['3', Q_DUYET, 'Thêm các phiếu Chờ xử lý thuộc công ty đang làm việc.'],
        ['4', '(không có quyền nào ở trên)', 'Chỉ phiếu do chính người dùng tạo.'],
    ],
    'pham_vi_sau': ['Công ty của phiếu = công ty của người lập tại thời điểm tạo. Phạm vi áp như nhau cho danh sách, chi tiết, lịch sử, '
                    'xuất Excel, sửa, xóa, không duyệt; ngoài phạm vi thì không hiện, mở thẳng đường dẫn thì sang trang "Không tìm thấy".'],
    'ma_tran': [['Chức năng', 'Không có quyền', Q_TAO, Q_DUYET, 'Người tạo phiếu']] + [_mt(i) for i in range(len(FR))],
    'ma_tran_widths': [2.2, 1.0, 1.1, 1.2, 1.0],
    'quyen_sau': ['"Có (theo phạm vi)": thao tác được trên các phiếu thuộc phạm vi xem ở bảng trên.'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Phiếu nhập kho được báo', ['– Phiếu nhập kho Đã hạch toán, loại: Nhập hàng mua trong nước; … (HĐNT); … (TỰ DO + HÃNG); Nhập hàng mua nước ngoài; … (mới); Nhập hàng mua ngoài.', '– Có ít nhất 1 dòng hàng SL thực nhập khác SL đề nghị nhập (so phần nguyên, bỏ lệch phần thập phân).', '– Chưa có phiếu báo nào (mọi trạng thái).'], ['Lập phiếu báo', 'Chọn phiếu nhập kho']),
        ('BR-02', 'Phạm vi dữ liệu', ['– Tổng công ty → mọi phiếu; Công ty → phiếu cùng công ty + phiếu mình tạo; quyền Duyệt → thêm phiếu Chờ xử lý cùng công ty; còn lại → phiếu mình tạo.', '– Phiếu nhập kho chọn được: Tổng công ty → mọi phiếu; Công ty → phiếu nhập kho của công ty; còn lại → phiếu nhập kho do mình lập.'], ['Mọi chức năng']),
        ('BR-03', 'Số phiếu', ['– <mã công ty của người lập>_BHNK-<số thứ tự bản ghi 5 chữ số>, sinh khi lưu lần đầu; không đổi khi sửa.'], ['Lập phiếu báo']),
        ('BR-04', 'Một phiếu nhập kho chỉ một phiếu báo', ['– Khi lưu, hệ thống khóa phiếu nhập kho và kiểm lại; đã có phiếu báo thì từ chối ("Phiếu nhập kho không còn chờ báo thừa, thiếu (đã có phiếu báo hoặc không đủ điều kiện).").', '– Xóa phiếu báo thì phiếu nhập kho quay lại hàng chờ.'], ['Lập phiếu báo', 'Xóa']),
        ('BR-05', 'Sửa / Xóa theo trạng thái', ['– Chỉ người tạo, chỉ khi Đang tạo hoặc Không duyệt; Chờ xử lý / Đã xử lý không sửa, không xóa.', '– Nút không dùng được thì ẩn; hệ thống chặn cả khi trạng thái vừa đổi (%s).' % DOI_TT], ['Sửa', 'Xóa', 'Xem chi tiết']),
        ('BR-06', 'Dòng hàng lấy từ phiếu nhập kho', ['– Dòng hàng = các dòng lệch của phiếu nhập kho, lấy lại ở máy chủ lúc lưu (không lấy theo màn hình); chỉ đọc, không sửa ở phiếu báo.', '– Lưu kèm đơn giá nhà cung cấp và tiền tệ của yêu cầu nhập hàng.'], ['Lập phiếu báo']),
        ('BR-07', 'Dữ liệu bắt buộc', ['– Diễn giải 1–255 ký tự.', '– Tạo mới bắt buộc ≥ 1 file đính kèm (ppt, pptx, doc, docx, pdf, xls, xlsx, jpg, jpeg, png, zip; ≤ 15MB/file); khi sửa không bắt buộc thêm file.', '– Không duyệt bắt buộc lý do 1–255 ký tự.'], ['Lập phiếu báo', 'Sửa', 'Không duyệt']),
        ('BR-08', 'Thông báo', ['– Lưu và gửi (tạo hoặc sửa): gửi "[BHNK] Chờ duyệt: <số phiếu>. Người gửi: <tên>. Phiếu nhập kho: <mã>" cho người có quyền Duyệt cùng công ty phiếu VÀ đang quản lý phòng ban của người lập.', '– Không duyệt: gửi "[BHNK] Không duyệt: <số phiếu>. Người duyệt: <tên>. Lý do: <lý do>" cho người tạo.', '– Bấm thông báo mở trang Chi tiết phiếu.'], ['Lập phiếu báo', 'Sửa', 'Không duyệt']),
        ('BR-09', 'Không tác động số liệu', ['– Phiếu báo không ghi tồn kho, không sinh bút toán; xử lý hàng thiếu thực hiện ở phiếu xử lý hàng thiếu nhập kho.'], ['Mọi chức năng']),
        ('BR-10', 'Ghi lịch sử', ['– Tạo mới; Thay đổi thông tin (Phiếu nhập kho, Diễn giải, từng file thêm / xóa); Thay đổi trạng thái khi Lưu / Lưu và gửi đổi trạng thái; Không duyệt (kèm lý do); Xóa.'], ['Lập phiếu báo', 'Sửa', 'Xóa', 'Không duyệt', 'Xem lịch sử']),
        ('BR-11', 'Thao tác xong quay về danh sách', ['– Lưu / Lưu và gửi, Không duyệt, Xóa ở trang Chi tiết xong thì về màn danh sách.'], ['Lập phiếu báo', 'Sửa', 'Xóa', 'Không duyệt']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây cung cấp dữ liệu cho phiếu báo hoặc đọc / dùng dữ liệu phiếu báo.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng (theo quyền)',
    'mains': [('FR-01', 'Xem danh sách phiếu báo', 'view'), ('FR-04', 'Lập phiếu báo hàng thừa, thiếu', 'crud'),
              ('FR-06', 'Sửa phiếu báo', 'crud'), ('FR-08', 'Xóa phiếu báo', 'action'),
              ('FR-09', 'Không duyệt phiếu báo', 'action'), ('FR-10', 'Xử lý phiếu báo', 'action'),
              ('FR-11', 'Xuất Excel danh sách', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc danh sách', 'view'), ('FR-03', 'Cài đặt bộ lọc, tuỳ chỉnh cột', 'view'),
             ('FR-07', 'Xem chi tiết phiếu báo', 'view'), ('FR-12', 'Xem lịch sử thay đổi', 'view')],
    'rieng': [('FR-04', 'Lập phiếu báo hàng thừa, thiếu', 'crud', 'uc_them'), ('FR-05', 'Chọn phiếu nhập kho', 'crud', 'uc_chonpnk'),
              ('FR-06', 'Sửa phiếu báo', 'crud', 'uc_sua'), ('FR-07', 'Xem chi tiết phiếu báo', 'view', 'uc_xem'),
              ('FR-08', 'Xóa phiếu báo', 'action', 'uc_xoa'), ('FR-09', 'Không duyệt phiếu báo', 'action', 'uc_khongduyet'),
              ('FR-10', 'Xử lý phiếu báo', 'action', 'uc_xuly'), ('FR-11', 'Xuất Excel danh sách', 'io', 'uc_xuat')],
}

STATES = [('start', '', None), ('dang', 'Đang tạo', '#e5e7eb'), ('cho', 'Chờ xử lý', '#fef3c7'),
          ('khong', 'Không duyệt', '#fee2e2'), ('da', 'Đã xử lý', '#dcfce7')]
TRANS = [('start', 'dang', 'Lưu'), ('dang', 'cho', 'Lưu và gửi'), ('cho', 'khong', 'Không duyệt'),
         ('cho', 'da', 'Lập phiếu xử lý'),
         ('khong', 'cho', 'Sửa, Lưu và gửi'), ('khong', 'dang', 'Sửa, Lưu')]

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    L.draw_state_flow(os.path.join(scr.uml, 'state_flow.png'), STATES, TRANS)
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))

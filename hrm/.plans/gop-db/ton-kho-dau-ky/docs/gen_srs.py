# -*- coding: utf-8 -*-
"""SRS - Khai báo tồn kho đầu kỳ (STT 283, phân hệ Kho) — khuôn màn mẫu phiếu finance-declare-debt-beginning/docs/kh/.

Nguồn (code HRM develop, 02/11/2026 — worktree gop-db):
  FE hrm-client/pages/warehouse/beginning-stocks/{index, create, _id/edit}.vue,
     components/{BeginningStockForm, BeginningStockEditForm, constants}, components/subsystem-menu/warehouse.js,
     components/product/picker/V2ProductPickerModal.vue, pages/finance/warehouse-imports/components/RecordPickerModal.vue
  BE Modules/Finance: Http/Controllers/V1/BeginningStockController.php, Services/BeginningStock/BeginningStockService.php,
     Services/PhysicalStockWriter.php (importBeginning / adjustBeginning / removeBeginning), Routes/api.php (beginning-stocks),
     app/ExcelExport/ExportColumnRegistry.php (beginning_stocks)
  Feature: ../design.md + ../plan.md (#11828, #11834, #11836, #11837, #11858).
  Ảnh: capture.js (dev-hrm). Phần 5: dò code FE/BE 02/11/2026.
Màn KHÔNG có trang Chi tiết, Lịch sử, In danh sách, không qua duyệt (đúng code).
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402
from _lib_phieu import ui, UI4, UI4W, UI6, UI6W, UI7, UI7W, UI8, UI8W, TRUOC_LUU  # noqa: E402,F401

TEN = 'Khai báo tồn kho đầu kỳ'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
QUYEN = 'Khai báo tồn kho đầu kỳ'
Q = 'Người dùng có quyền thực hiện chức năng (quyền "%s")' % QUYEN
DK = '1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền "%s".' % QUYEN
DK_CHUA = DK + '\n3. Nhóm khai báo (hàng, kho, công ty) ở trạng thái Chưa có giao dịch và thuộc công ty người dùng được thao tác.'
TRANG = 'Trang %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'
POPUP = 'Modal %s được mở ngay trên màn hình %s theo đường dẫn ở trên.'
LECH = 'Hàng hóa <mã hàng> khác số lượng đã khai kho kế toán, không thể nhập tồn đầu!'

# ------------------------------------------------------------------ Phần 5 (dò code 02/11/2026)
P5 = [
    ('Kho', 'Thẻ kho (dòng tồn đầu kỳ của hàng tại kho / vị trí)', 'Kho => Báo cáo kho => Thẻ kho'),
    ('Kho', 'Báo cáo tồn kho chi tiết theo mặt hàng', 'Kho => Báo cáo kho => Báo cáo tồn kho chi tiết theo mặt hàng'),
    ('Kho', 'Báo cáo tồn kho tổng hợp theo mặt hàng', 'Kho => Báo cáo kho => Báo cáo tồn kho tổng hợp theo mặt hàng'),
    ('Kho', 'Báo cáo tồn kho theo vị trí', 'Kho => Báo cáo kho => Báo cáo tồn kho theo vị trí'),
    ('Kho', 'Báo cáo tồn theo kho', 'Kho => Báo cáo kho => Báo cáo tồn theo kho'),
    ('Kho', 'Tổng hợp xuất nhập tồn (số tồn đầu kỳ)', 'Kho => Báo cáo kho => Tổng hợp xuất nhập tồn'),
    ('Kho', 'Phiếu điều chuyển vị trí (chuyển hàng của lô tồn đầu)',
     'Kho => Điều chuyển => Phiếu điều chuyển vị trí'),
    ('Kho', 'Kiểm kê theo vị trí (tồn sổ sách gồm tồn đầu)', 'Kho => Kiểm kho => Theo vị trí => Kiểm kê theo vị trí'),
    ('Kho', 'Phiếu xuất kho điều chỉnh kiểm kê (xuất từ lô tồn đầu)',
     'Kho => Xuất kho => Phiếu xuất kho điều chỉnh kiểm kê'),
    ('Kho', 'Danh mục Kho vật lý, Vị trí (kho / vị trí đã có khai báo tồn đầu không xóa được)', 'Kho => Danh mục => Kho vật lý / Vị trí'),
    ('Danh mục dùng chung', 'Hàng hoá (hàng đã có khai báo tồn đầu không xóa được)',
     'Danh mục dùng chung => Hàng hoá, vật tư => Kho dữ liệu hàng hoá'),
    ('Tài chính', 'Khai Quy chế – Cấu hình (khóa "Ngày khai báo đầu kỳ" khi công ty đã có khai báo tồn đầu)',
     'Tài chính => Khai Quy chế – Cấu hình'),
]

FR = []

# 2.1 Xem danh sách -------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách khai báo tồn kho đầu kỳ',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách khai báo tồn kho đầu kỳ'],
        ['Mô tả', 'Hiển thị các dòng khai báo tồn kho đầu kỳ (mỗi dòng = 1 hàng × 1 vị trí tại 1 kho của 1 công ty) trong phạm vi công ty của người dùng, có phân trang, sắp xếp và nút Sửa / Xóa theo từng dòng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), dòng khai báo mới nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Không có dòng khớp → bảng hiện "Không có dữ liệu phù hợp."\n• Phạm vi dữ liệu theo công ty được thao tác (Phần 2, BR-02).\n• Nhóm khai báo Đã có giao dịch: không còn nút Sửa, Xóa (BR-05).'],
    ],
    'anh': [('01_list', 'Màn danh sách Khai báo tồn kho đầu kỳ lúc mới truy cập (bộ cột mặc định)'),
            ('01b_list_actions', 'Cột Hành động: nhóm Chưa có giao dịch có Sửa, Xóa; nhóm Đã có giao dịch để trống')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Danh sách khai báo tồn kho đầu kỳ', 'Tiêu đề khối danh sách; tiêu đề trang "Khai báo tồn kho đầu kỳ".'],
        ['Nút Tạo mới', 'Button', 'Enable', 'Hiển thị', 'Mở trang Thêm khai báo (mục 2.4).'],
        ['Nút Import Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Import khai báo tồn kho đầu kỳ" (mục 2.10).'],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất Excel" (mục 2.9). Trong lúc xuất, cạnh nút hiện dòng tiến độ.'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.3).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa, không ẩn được.'],
        ['Cột Tên hàng', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên hàng, dài thì xuống dòng (tối đa 2 dòng). Sắp xếp được. Cột khóa.'],
        ['Cột Mã hàng', 'Table/Grid', 'Read-only', 'Hiển thị', 'Sắp xếp được.'],
        ['Cột Kho', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên kho vật lý.'],
        ['Cột Mã vị trí, Vị trí', 'Table/Grid', 'Read-only', 'Hiển thị', 'Mã và tên vị trí trong kho.'],
        ['Cột Công ty', 'Table/Grid', 'Read-only', 'Hiển thị / Ẩn', 'Mã công ty khai báo. Mặc định chỉ hiện với người xem được mọi công ty (BR-02).'],
        ['Cột ĐVT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Đơn vị tính đã khai.'],
        ['Cột Số lượng', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số lượng tại vị trí, định dạng 1,234.56, căn phải. Sắp xếp được.'],
        ['Cột Người tạo, Người cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', '"Họ tên - Mã phòng ban".'],
        ['Cột Ngày tạo, Ngày cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được. Dòng chưa ai sửa thì Người cập nhật / Ngày cập nhật để trống.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sửa, Xóa: chỉ hiện khi nhóm khai báo Chưa có giao dịch (BR-05).\n- Nút không dùng được thì ẩn, không làm mờ. Cột khóa.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Kiểm tra quyền "%s"; thiếu quyền → mục menu không hiện, mở thẳng màn thì báo "Bạn không có quyền thực hiện chức năng này", bảng trống.\nAfter:\n– Tải trang 1 theo phạm vi công ty (BR-02), dòng mới nhất trên cùng; tính trạng thái giao dịch cho các dòng của trang; khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút).' % QUYEN],
        ['Bấm tiêu đề cột Tên hàng / Mã hàng / Số lượng / Ngày tạo / Ngày cập nhật', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại dữ liệu từ trang 1.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp, tải lại dữ liệu; đổi số dòng thì quay về trang 1.'],
        ['Bấm Sửa / Xóa trên dòng', 'Click', 'After:\n– Mở trang Sửa (mục 2.7) / hộp Xác nhận xóa (mục 2.8).'],
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc danh sách',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách khai báo tồn kho đầu kỳ'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc trong vùng Tìm kiếm nâng cao.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn / nhập giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô gõ chữ (tìm nhanh, Mã hàng, Vị trí) chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Bấm Làm mới → xoá mọi điều kiện và tải lại danh sách.\n• Ô Công ty chỉ hiện với người xem được mọi công ty (BR-02).\n• Hệ thống ghi nhớ bộ lọc 10 phút khi rời màn rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Vùng Tìm kiếm nâng cao ở trạng thái mở')],
    'ui': ui(UI7, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', '- Placeholder "Tìm theo mã / tên hàng".\n- Tìm gần đúng theo tên hàng hoặc mã hàng.'],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Áp dụng từ khóa và các ô lọc.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá mọi điều kiện lọc và tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng vùng ô lọc.'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" (mục 2.3).'],
        ['Ô Mã hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Tìm gần đúng theo mã hàng; lọc khi Enter / Tìm kiếm.'],
        ['Ô Kho', 'Dropdown', 'Enable', 'Kho thường và kho thanh lý đang hoạt động, có kho kế toán của công ty người dùng được thao tác', 'Trống', 'Hiển thị "Mã - Tên kho"; chọn là lọc ngay.'],
        ['Ô Vị trí', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Tìm gần đúng theo mã hoặc tên vị trí; lọc khi Enter / Tìm kiếm.'],
        ['Ô Người tạo', 'Dropdown', 'Enable', 'Người đã tạo khai báo trong phạm vi', 'Trống', 'Lọc dòng do người được chọn tạo.'],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Công ty đang hoạt động', 'Trống', '"Mã - Tên công ty"; chỉ hiện với người xem được mọi công ty.'],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm Tìm kiếm / nhấn Enter ở ô gõ chữ', 'Click', 'After:\n– Áp đồng thời từ khóa và các ô lọc, tải lại bảng từ trang 1.'],
        ['Chọn giá trị ở ô chọn', 'Change', 'After:\n– Tải lại bảng từ trang 1 ngay.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng vùng ô lọc; lần mở đầu tải danh sách Kho, Người tạo, Công ty.'],
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
        ['Dòng sự kiện phụ', '• Bấm Đóng: bỏ thay đổi.\n• Cài đặt bộ lọc có nút "Khôi phục mặc định".\n• Cột STT, Tên hàng, Hành động không bỏ được (có biểu tượng khóa).'],
    ],
    'menu_them': ' => Cài đặt bộ lọc {icon:btn_caidatboloc} / Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': 'Modal Cài đặt bộ lọc và Modal Tuỳ chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('26_filtercfg', 'Cửa sổ Cài đặt bộ lọc'), ('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột')],
    'ui': ui(UI6, [
        ['Danh sách ô lọc', 'Checkbox', 'Enable', 'Mã hàng, Kho, Vị trí, Người tạo (+ Công ty)', 'Tích ô lọc muốn hiện, kéo ☰ đổi thứ tự.'],
        ['Nút Khôi phục mặc định', 'Button', 'Enable', '–', 'Đưa cấu hình ô lọc về mặc định.'],
        ['Danh sách cột', 'Checkbox', 'Enable', '14 cột', 'Tích cột muốn hiện; STT, Tên hàng, Hành động bị khóa. Kéo ☰ đổi thứ tự. Dòng đếm "Đang chọn x/14 cột".'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Chọn / bỏ nhanh mọi cột (trừ cột khóa).'],
        ['Nút Lưu', 'Button', 'Enable', '–', 'Lưu cấu hình theo người dùng, áp dụng ngay.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ, không lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình theo người dùng, đóng cửa sổ, bảng / vùng lọc vẽ lại theo cấu hình.'],
        ['Kéo ☰', 'Drag', 'After:\n– Đổi thứ tự dòng trong cửa sổ.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ, không lưu.'],
    ],
})

# 2.4 Thêm khai báo --------------------------------------------------------------
FR.append({
    'ten': 'Thêm khai báo tồn kho đầu kỳ', 'uc': 'uc_them', 'uc_ten': 'FR-04 Thêm khai báo tồn kho đầu kỳ',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.',
    'gioi_thieu': [
        ['Tên chức năng', 'Thêm khai báo tồn kho đầu kỳ'],
        ['Mô tả', 'Chọn Kho và Công ty, chọn một hoặc nhiều hàng hóa đã khai tồn kho KẾ TOÁN đầu kỳ tại kho đó của công ty; mỗi hàng chia số lượng vào một hoặc nhiều vị trí, tổng các vị trí phải bằng SL tồn kế toán. Lưu xong có hiệu lực ngay (không qua duyệt): ghi tồn kho vật lý theo kho, vị trí, công ty.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Hàng cần khai đã được khai tồn kho kế toán đầu kỳ tại kho (qua kho kế toán của công ty).'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở trang Thêm; góc phải khối Thông tin chung hiện "<Người đăng nhập> - <ngày giờ hiện tại>".\n3. Người dùng chọn Kho, Công ty (2 ô độc lập).\n4. Bấm "Chọn hàng hóa", chọn hàng (mục 2.5); mỗi hàng thêm vào bảng với ĐVT và SL tồn kế toán tự điền, 1 dòng vị trí có sẵn số lượng = SL tồn kế toán.\n5. Mỗi dòng chọn Vị trí (mục 2.6), nhập Số lượng; cần nhiều vị trí thì bấm "Thêm vị trí" (dòng mới tự điền phần còn thiếu).\n6. Bấm Lưu.\n7. Hệ thống kiểm tra (BR-03, BR-04, BR-06), ghi mỗi dòng vị trí thành 1 dòng khai báo và cập nhật tồn kho vật lý (BR-07).\n8. Báo "Thêm mới thành công", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Bấm "Lưu và tiếp tục": lưu như trên rồi mở lại trang Thêm trống.\n• Thiếu ô bắt buộc → báo đỏ dưới ô + "Bạn chưa nhập đầy đủ thông tin.", cuộn tới ô lỗi đầu tiên.\n• Tổng số lượng các vị trí ≠ SL tồn kế toán → các ô Số lượng của hàng viền đỏ, dưới ô cuối "Tổng số lượng phải bằng SL tồn kế toán (<số>)", thông báo "' + LECH + '"\n• Chọn trùng vị trí trong cùng hàng → "Vị trí đã được chọn!".\n• Đổi Kho hoặc Công ty khi bảng đã có hàng → hỏi xác nhận rồi xoá danh sách hàng.\n• Bấm Quay lại khi đã nhập → hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', '- Nút Lưu bị khóa từ khi bấm tới khi có kết quả.\n- Hai người cùng lưu 1 hàng tại cùng kho + công ty: người sau bị chặn "đã được khai báo tồn đầu kỳ", không sinh 2 bộ khai báo.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': TRANG % 'Thêm khai báo tồn kho đầu kỳ',
    'anh': [('10_create', 'Trang Thêm khai báo tồn kho đầu kỳ lúc mới mở'),
            ('10b_create_filled', 'Đã chọn Kho, Công ty, 1 hàng chia 2 vị trí'),
            ('10c_create_mismatch', 'Báo đỏ khi tổng số lượng các vị trí khác SL tồn kế toán'),
            ('19_change_wh', 'Hộp xác nhận khi đổi Kho / Công ty lúc đã có hàng'),
            ('18_unsaved', 'Hộp xác nhận Thông tin chưa lưu khi bấm Quay lại')],
    'ui': ui(UI8, [
        ['Người tạo - ngày giờ', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại', 'Góc phải khối Thông tin chung.'],
        ['Kho', 'Dropdown', 'Enable', 'Kho đang hoạt động có kho kế toán của công ty đang làm việc', 'Có', 'Trống', '"Mã - Tên kho". Bỏ trống: "Bắt buộc phải chọn".'],
        ['Công ty', 'Dropdown', 'Enable', 'Công ty người dùng được thao tác', 'Có', 'Trống', '"Mã - Tên công ty", không chọn sẵn. Bỏ trống: "Bắt buộc phải chọn". Kho không thuộc công ty: "Kho không thuộc công ty đã chọn".'],
        ['Nút Chọn hàng hóa', 'Button', 'Enable / Disable', '–', '–', '–', 'Chỉ bấm được khi đã chọn Kho và Công ty; mở cửa sổ chọn hàng (mục 2.5).'],
        ['Bảng hàng hóa', 'Table/Grid', 'Enable', '≥ 1 hàng', 'Có', 'Trống', '- Trống: "Chưa chọn hàng hóa".\n- Lưu khi chưa có hàng: "Chưa chọn hàng hóa".'],
        ['Cột STT, Tên hàng hóa, Model, Mã hàng hóa', 'Table/Grid', 'Read-only', '–', '–', 'Theo hàng đã chọn', 'Lỗi chung của hàng (đã khai, đã có giao dịch…) hiện dưới Tên hàng.'],
        ['ĐVT', 'Label', 'Read-only', '–', 'Có', 'ĐVT của tồn kế toán đầu kỳ', 'Tự điền, không sửa được; hệ số ≠ 1 hiện "Tên (xHệ số)". Thiếu: "Bắt buộc phải có ĐVT".'],
        ['SL tồn kế toán', 'Label', 'Read-only', '–', '–', 'Số đã khai tồn kế toán', 'Quy theo ĐVT của dòng (BR-04).'],
        ['Tổng số lượng', 'Label', 'Read-only', '–', '–', 'Tổng các vị trí', 'Chữ đỏ khi khác SL tồn kế toán.'],
        ['Vị trí', 'Textbox + Popup', 'Enable', 'Vị trí đang hoạt động của kho', 'Có', 'Trống', 'Bấm ô mở cửa sổ "Chọn vị trí kho" (mục 2.6); nút × bỏ vị trí. Trống: "Bắt buộc phải chọn".'],
        ['Số lượng', 'Textbox', 'Enable', 'Số > 0, ≤ 999,999,999', 'Có', 'Dòng đầu = SL tồn kế toán', 'Trống: "Bắt buộc phải nhập"; ≤ 0: "Số lượng phải lớn hơn 0".'],
        ['Link Thêm vị trí', 'Link', 'Enable', '–', '–', '–', 'Thêm 1 dòng vị trí, tự điền phần SL còn thiếu so với SL tồn kế toán.'],
        ['Nút xoá dòng vị trí / Bỏ hàng hóa', 'Button', 'Enable', '–', '–', '–', 'Hàng có > 1 vị trí: thùng rác xoá dòng vị trí, link "Bỏ hàng hóa" bỏ cả hàng; hàng 1 vị trí: thùng rác bỏ hàng.'],
        ['Dòng Tổng cộng', 'Label', 'Read-only', '–', '–', '–', 'Tổng số lượng mọi hàng.'],
        ['Nút Lưu / Lưu và tiếp tục / Quay lại', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi về danh sách / lưu rồi mở trang Thêm trống / về danh sách (đã nhập thì hỏi).'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'After:\n– Mở trang Thêm trống, tải danh sách Công ty và Kho.'],
        ['Đổi Kho / Công ty', 'Change', 'During:\n– Bảng đã có hàng: hỏi "Đổi công ty / kho sẽ xoá danh sách hàng hóa đã chọn. Tiếp tục?" (Đồng ý / Hủy).\nAfter:\n– Đồng ý: đổi giá trị, xoá danh sách hàng; Hủy: giữ nguyên.'],
        ['Bấm Thêm vị trí', 'Click', 'After:\n– Thêm dòng vị trí trống, Số lượng = SL tồn kế toán − tổng hiện có (nếu còn thiếu).'],
        ['Bấm Lưu / Lưu và tiếp tục', 'Click', 'Before:\n– Kiểm tra quyền "%s".\nDuring:\n– Trên form: Kho, Công ty, ≥ 1 hàng; mỗi hàng có ĐVT; mỗi dòng có Vị trí, Số lượng > 0; tổng số lượng của hàng = SL tồn kế toán.\n– Phía hệ thống: công ty được thao tác, kho có kho kế toán của công ty, hàng không trùng, vị trí thuộc kho và không trùng, hàng chưa khai tại kho + công ty, hàng chưa có giao dịch, tổng quy ĐVT cơ bản khớp tồn kế toán.\n' % QUYEN + TRUOC_LUU + '\nAfter:\n– Ghi mỗi dòng vị trí thành 1 dòng khai báo + 1 lô tồn đầu, cập nhật tồn kho vật lý (BR-07) trong 1 giao dịch.\n– Báo "Thêm mới thành công"; Lưu → về danh sách, Lưu và tiếp tục → trang Thêm trống.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa nhập gì → về danh sách.\n– Đã nhập → hộp "Thông tin chưa lưu" ("Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"): Thoát / Ở lại.'],
    ],
})

# 2.5 Chọn hàng hóa ------------------------------------------------------------
FR.append({
    'ten': 'Chọn hàng hóa', 'uc': 'uc_chonhang', 'uc_ten': 'FR-05 Chọn hàng hóa khai báo tồn đầu',
    'qtc': 'Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chọn hàng hóa khai báo tồn đầu'],
        ['Mô tả', 'Cửa sổ chọn hàng dùng chung (cây catalog, tìm kiếm, tích chọn nhiều hàng). Bấm "Thêm (n)" đưa hàng vào bảng của form; hệ thống kiểm từng hàng và lấy ĐVT + SL tồn kế toán.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở trang Thêm, đã chọn Kho và Công ty.'],
        ['Dòng sự kiện chính', '1. Bấm "Chọn hàng hóa".\n2. Hệ thống mở cửa sổ "Chọn hàng hóa khai báo tồn đầu" theo công ty đã chọn.\n3. Người dùng tìm, tích chọn một hoặc nhiều hàng, bấm "Thêm (n)".\n4. Hệ thống kiểm từng hàng: hàng hợp lệ thêm vào bảng (ĐVT, SL tồn kế toán, 1 dòng vị trí); hàng bị chặn báo lỗi riêng.'],
        ['Dòng sự kiện phụ', '• Hàng đã khai tại kho + công ty: "<mã hàng>: Hàng hóa đã được khai báo tồn đầu kì. Kho: <mã kho>".\n• Hàng chưa khai tồn kế toán tại kho: "<mã hàng>: Hàng hóa chưa khai tồn kho kế toán đầu kỳ tại kho này, không thể nhập tồn đầu!".\n• Hàng đã bị xoá: "<mã hàng>: Hàng hóa đã bị xoá".\n• Hàng đã có trên form không thêm lại.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi} => Chọn hàng hóa {icon:btn_chonhang}',
    'ghi_chu_layout': POPUP % ('Chọn hàng hóa khai báo tồn đầu', 'Thêm khai báo'),
    'anh': [('14_picker', 'Cửa sổ Chọn hàng hóa khai báo tồn đầu'),
            ('15_blocked', 'Hàng đã khai tại kho bị chặn, không thêm vào bảng')],
    'ui': ui(UI6, [
        ['Dòng Công ty', 'Label', 'Read-only', 'Công ty đã chọn', 'Công ty dùng để lọc hàng.'],
        ['Ô tìm cây catalog, cây nhóm hàng', 'Tree', 'Enable', 'Tất cả hàng hoá', 'Lọc hàng theo nhóm catalog.'],
        ['Ô tìm kiếm hàng', 'Textbox', 'Enable', 'Trống', 'Tìm theo mã, tên hàng hoá, model, barcode, mã đặt hàng.'],
        ['Công tắc Còn tồn, Gồm hàng ngoài catalog; Tìm kiếm nâng cao; Làm mới', 'Button', 'Enable', '–', 'Thu hẹp danh sách hàng.'],
        ['Bảng hàng', 'Table/Grid', 'Enable', '20 dòng/trang', 'Ô tích, STT, Ảnh, Mã hàng, Tên hàng hoá, Model, Thương hiệu, Loại sản phẩm, ĐVT, Tồn bán được…'],
        ['Dòng "Đã chọn n hàng hoá"', 'Label', 'Read-only', '0', 'Số hàng đang tích.'],
        ['Nút Thêm (n)', 'Button', 'Enable / Disable', 'Disable', 'Bấm được khi đã tích ≥ 1 hàng; đưa hàng vào form và đóng cửa sổ.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ, không thêm.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Thêm (n)', 'Click', 'Before:\n– Kiểm tra quyền, công ty được thao tác, kho thuộc công ty.\nDuring:\n– Kiểm từng hàng (đã khai / chưa khai kế toán / đã xoá).\nAfter:\n– Hàng hợp lệ: thêm vào bảng với ĐVT + SL tồn kế toán; hàng bị chặn: thông báo theo từng hàng.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.6 Chọn vị trí ----------------------------------------------------------------
FR.append({
    'ten': 'Chọn vị trí kho', 'uc': 'uc_chonvitri', 'uc_ten': 'FR-06 Chọn vị trí kho',
    'qtc': 'Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chọn vị trí kho cho dòng hàng'],
        ['Mô tả', 'Cửa sổ liệt kê vị trí ĐANG HOẠT ĐỘNG của kho khai báo (vị trí, nhà, dãy, khoang không bị khóa); vị trí đang có tồn của hàng xếp trước. Bấm vào vị trí để gán cho dòng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở trang Thêm, bảng đã có hàng.'],
        ['Dòng sự kiện chính', '1. Bấm vào ô Vị trí của dòng.\n2. Hệ thống mở cửa sổ "Chọn vị trí kho" (dòng phụ "Vị trí của kho khai báo"), 10 dòng/trang.\n3. Người dùng tìm (mã / tên vị trí) và bấm vào vị trí.\n4. Hệ thống điền Mã vị trí vào ô, đóng cửa sổ.'],
        ['Dòng sự kiện phụ', '• Vị trí đã chọn ở dòng khác của cùng hàng → "Vị trí đã được chọn!", không gán.\n• Bấm × trên ô Vị trí: bỏ vị trí, giữ số lượng.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi} => ô Vị trí',
    'ghi_chu_layout': POPUP % ('Chọn vị trí kho', 'Thêm khai báo'),
    'anh': [('16_position_picker', 'Cửa sổ Chọn vị trí kho')],
    'ui': ui(UI6, [
        ['Ô Vị trí', 'Textbox', 'Enable', 'Trống', 'Placeholder "Mã / tên vị trí"; tìm gần đúng.'],
        ['Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', 'Áp dụng / xoá điều kiện tìm.'],
        ['Bảng vị trí', 'Table/Grid', 'Enable', '10 dòng/trang', 'STT, Vị trí (bấm để chọn), Nhà, Dãy, Khoang; "Hiển thị a–b / N".'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng, không chọn.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm vị trí', 'Click', 'During:\n– Vị trí trùng dòng khác của cùng hàng: báo "Vị trí đã được chọn!".\nAfter:\n– Gán vị trí cho dòng, đóng cửa sổ.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.7 Sửa -----------------------------------------------------------------------
FR.append({
    'ten': 'Sửa khai báo', 'uc': 'uc_sua', 'uc_ten': 'FR-07 Sửa khai báo tồn kho đầu kỳ',
    'qtc': 'Màn Sửa, Validate dữ liệu, Thông báo và UI/UX.',
    'gioi_thieu': [
        ['Tên chức năng', 'Sửa khai báo tồn kho đầu kỳ'],
        ['Mô tả', 'Sửa số lượng theo NHÓM (hàng, kho, công ty): trang Sửa liệt kê mọi vị trí đã khai của hàng tại kho, chỉ đổi được Số lượng từng vị trí; tổng phải bằng SL tồn kế toán. Hàng, Đơn vị, Kho, Vị trí cố định.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_CHUA],
        ['Dòng sự kiện chính', '1. Bấm Sửa ở cột Hành động của một dòng.\n2. Hệ thống mở trang "Sửa khai báo tồn kho đầu kỳ: <mã hàng>": khối Thông tin chung (Hàng hóa, Đơn vị, Kho, SL tồn kế toán — khóa; góc phải "<Người tạo> - <ngày giờ tạo>"), khối Vị trí (mọi vị trí của nhóm).\n3. Người dùng sửa Số lượng và bấm Lưu.\n4. Hệ thống kiểm tra, ghi số lượng mới và điều chỉnh tồn kho vật lý theo phần chênh lệch (BR-07).\n5. Báo "Cập nhật thành công", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Tổng ≠ SL tồn kế toán → ô Số lượng viền đỏ, dưới ô cuối "Tổng số lượng phải bằng SL tồn kế toán (<số>)", thông báo "' + LECH + '"\n• Mở thẳng trang Sửa của nhóm Đã có giao dịch → "Hàng hóa đã có giao dịch, không thể sửa / xóa tồn đầu!" rồi về danh sách.\n• Nhóm vừa phát sinh giao dịch / có vị trí bị thêm, xoá khi đang sửa → bấm Lưu bị từ chối ("Hàng hóa đã có giao dịch…" / "Trạng thái đã bị thay đổi. Vui lòng load lại trang").\n• Vị trí không đổi số lượng thì không ghi lại (Người cập nhật giữ nguyên).'],
    ],
    'menu_them': ' => Sửa {icon:btn_sua}',
    'ghi_chu_layout': TRANG % 'Sửa khai báo tồn kho đầu kỳ',
    'anh': [('12_edit', 'Trang Sửa khai báo tồn kho đầu kỳ (nhóm 2 vị trí)'),
            ('12b_edit_mismatch', 'Báo đỏ khi tổng số lượng khác SL tồn kế toán')],
    'ui': ui(UI8, [
        ['Hàng hóa, Kho', 'Textbox', 'Read-only', '–', '–', 'Dữ liệu nhóm', 'Không sửa được.'],
        ['Đơn vị', 'Textbox', 'Read-only', '–', 'Có', 'ĐVT đã khai', 'Theo tồn kế toán đầu kỳ, không đổi được; hệ số ≠ 1 hiện "Tên (xHệ số)".'],
        ['SL tồn kế toán', 'Textbox', 'Read-only', '–', '–', 'Số kế toán', 'Tổng số lượng các vị trí phải bằng số này.'],
        ['Bảng Vị trí: STT, Mã vị trí, Vị trí', 'Table/Grid', 'Read-only', '–', '–', 'Mọi vị trí của nhóm', 'Không thêm / bớt vị trí ở trang Sửa.'],
        ['Số lượng', 'Textbox', 'Enable', 'Số > 0, ≤ 999,999,999', 'Có', 'Dữ liệu hiện tại', 'Trống: "Bắt buộc phải nhập"; ≤ 0: "Số lượng phải lớn hơn 0".'],
        ['Dòng Tổng cộng', 'Label', 'Read-only', '–', '–', '–', 'Chữ đỏ khi khác SL tồn kế toán.'],
        ['Nút Lưu', 'Button', 'Enable / Ẩn', '–', '–', '–', 'Chỉ hiện khi nhóm Chưa có giao dịch.'],
        ['Nút Quay lại', 'Button', 'Enable', '–', '–', '–', 'Về danh sách (đã sửa thì hỏi "Thông tin chưa lưu").'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện khi nhóm Chưa có giao dịch.\nAfter:\n– Tải nhóm; ngoài phạm vi / không còn → "Trạng thái đã bị thay đổi. Vui lòng load lại trang", về danh sách.'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền, phạm vi công ty; nhóm phải Chưa có giao dịch.\nDuring:\n– Đủ mọi vị trí của nhóm, Số lượng > 0, tổng quy ĐVT cơ bản khớp tồn kế toán.\n' + TRUOC_LUU + '\nAfter:\n– Ghi số lượng mới cho vị trí có thay đổi, điều chỉnh lô tồn đầu và tồn kho vật lý theo chênh lệch.\n– Báo "Cập nhật thành công", về danh sách.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa đổi gì → về danh sách; đã đổi → hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
    ],
})

# 2.8 Xóa -----------------------------------------------------------------------
FR.append({
    'ten': 'Xóa khai báo', 'uc': 'uc_xoa', 'uc_ten': 'FR-08 Xóa khai báo tồn kho đầu kỳ',
    'qtc': 'Quy tắc xóa và Thông báo.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xóa khai báo tồn kho đầu kỳ'],
        ['Mô tả', 'Xóa cả NHÓM (mọi vị trí của hàng tại kho + công ty) của dòng được chọn, đảo ngược phần tồn kho vật lý đã ghi.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_CHUA],
        ['Dòng sự kiện chính', '1. Bấm Xóa ở cột Hành động.\n2. Hệ thống hiện hộp "Xác nhận xóa": "Xóa khai báo tồn đầu của hàng <mã hàng> tại kho <tên kho> (tất cả vị trí của hàng tại kho này)?"\n3. Bấm Xóa.\n4. Hệ thống xóa mọi dòng của nhóm cùng lô tồn đầu, trừ tồn kho vật lý tương ứng (BR-07).\n5. Báo "Xóa thành công <n> dòng tồn đầu", tải lại danh sách.'],
        ['Dòng sự kiện phụ', '• Bấm Hủy / (x) → đóng hộp, không thay đổi.\n• Nhóm vừa phát sinh giao dịch → "Hàng hóa đã có giao dịch, không thể sửa / xóa tồn đầu!", không xóa.\n• Dòng đã bị người khác xóa → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".'],
    ],
    'menu_them': ' => Xóa {icon:btn_xoa}',
    'ghi_chu_layout': 'Modal Xác nhận xóa được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('13_delete', 'Hộp Xác nhận xóa khai báo')],
    'ui': ui(UI4, [
        ['Nút Xóa (cột Hành động)', 'Button', 'Biểu tượng thùng rác; chỉ hiện khi nhóm Chưa có giao dịch.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận xóa".'],
        ['Nội dung', 'Label', '"Xóa khai báo tồn đầu của hàng <mã hàng> tại kho <tên kho> (tất cả vị trí của hàng tại kho này)?"'],
        ['Nút Xóa', 'Button', 'Xác nhận xóa cả nhóm.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không xóa.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Xóa', 'Click', 'After:\n– Hiện hộp Xác nhận xóa.'],
        ['Bấm Xóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền, phạm vi công ty; nhóm phải Chưa có giao dịch.\nDuring:\n' + TRUOC_LUU + '\nAfter:\n– Đảo ngược tồn kho vật lý, xóa lô tồn đầu và mọi dòng của nhóm.\n– Báo "Xóa thành công <n> dòng tồn đầu", tải lại danh sách.'],
        ['Bấm Hủy / (x)', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.9 Xuất Excel -----------------------------------------------------------------
FR.append({
    'ten': 'Xuất Excel danh sách', 'uc': 'uc_xuat', 'uc_ten': 'FR-09 Xuất Excel danh sách khai báo',
    'qtc': 'Quy tắc Excel và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách khai báo tồn kho đầu kỳ ra Excel'],
        ['Mô tả', 'Xuất mọi dòng khớp bộ lọc (không chỉ trang đang xem) ra file Khai_bao_ton_dau_vat_ly.xlsx, tiêu đề "DANH SÁCH KHAI BÁO TỒN KHO ĐẦU KỲ", cột theo lựa chọn và thứ tự của người dùng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất Excel", tích sẵn các cột đang hiện trên bảng.\n3. Người dùng tích / bỏ, kéo ☰ đổi thứ tự, bấm Xuất file.\n4. Hệ thống tải dữ liệu theo lô (cạnh nút hiện "Đã tải x/y dòng…"), dựng file và tải về; báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Không có dòng nào khớp bộ lọc → "Không có dữ liệu để xuất", không tải file.\n• Cột Số lượng là ô SỐ.'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất Excel')],
    'ui': ui(UI8, [
        ['Danh sách trường', 'Checkbox', 'Enable', '12 trường', 'Có (≥ 1)', 'Các cột đang hiện', 'Tên hàng, Mã hàng, Kho, Mã vị trí, Vị trí, Công ty, ĐVT, Số lượng, Người nhập, Ngày nhập, Người cập nhật, Ngày cập nhật. Kéo ☰ đổi thứ tự cột trong file.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', 'Chọn / bỏ nhanh mọi trường.'],
        ['Dòng đếm', 'Label', 'Read-only', '–', '–', '–', '"Đang chọn x/12 trường".'],
        ['Nút Xuất file', 'Button', 'Enable', '–', '–', '–', 'Xuất file theo trường đã chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng, không xuất.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất file', 'Click', 'Before:\n– Kiểm tra quyền.\nAfter:\n– Tải dữ liệu theo bộ lọc và phạm vi hiện tại, dựng file đúng thứ tự cột (có cột STT), tải về; báo kết quả.'],
        ['Kéo ☰', 'Drag', 'After:\n– Đổi thứ tự cột trong file.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.10 Import --------------------------------------------------------------------
FR.append({
    'ten': 'Import khai báo từ file Excel', 'uc': 'uc_import', 'uc_ten': 'FR-10 Import khai báo từ file Excel',
    'qtc': 'Quy tắc Import Excel, Validate dữ liệu và Thông báo.',
    'gioi_thieu': [
        ['Tên chức năng', 'Import khai báo tồn kho đầu kỳ từ file Excel'],
        ['Mô tả', 'Nhập nhiều dòng khai báo theo file mẫu "Mau_import_ton_kho_dau_ky.xlsx" (tải ngay trong cửa sổ). Mỗi dòng file = 1 hàng × 1 vị trí; các dòng cùng hàng + kho + công ty gom thành 1 nhóm, tổng phải khớp SL tồn kế toán. Tối đa 200 dòng mỗi lần.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Import Excel → cửa sổ "Import khai báo tồn kho đầu kỳ".\n2. Bấm "Tải file mẫu", điền dữ liệu.\n3. Bấm "Chọn file Excel", chọn file; bấm "Load lên bảng".\n4. Bấm Validate: hệ thống kiểm từng dòng và từng nhóm, hiện Tổng / Hợp lệ / Lỗi; dòng lỗi nêu từng lỗi.\n5. Sửa dòng lỗi trên bảng rồi Validate lại, hoặc bấm "Bỏ dòng lỗi".\n6. Bấm Import.\n7. Hệ thống ghi từng nhóm (mỗi nhóm 1 giao dịch riêng) như khi Thêm tay, báo số dòng thành công, tải lại danh sách.'],
        ['Dòng sự kiện phụ', '• Nhóm vừa bị người khác khai trùng sau lần Validate → bỏ qua nhóm đó, các nhóm khác vẫn nhập, kết quả nêu dòng bị bỏ.\n• "Xoá trạng thái validate" để sửa lại dòng đã khóa; "Làm mới" xoá bảng.\n• File quá 200 dòng → báo, không nhập.'],
    ],
    'menu_them': ' => Import Excel {icon:btn_import}',
    'ghi_chu_layout': 'Modal Import khai báo tồn kho đầu kỳ được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('21_import_open', 'Cửa sổ Import khi vừa mở'), ('23_import_validated', 'Kết quả Validate — mỗi dòng lỗi nêu rõ lý do')],
    'ui': ui(UI8, [
        ['Cột Tên hàng, Mã hàng', 'Textbox', 'Enable', 'Mã + tên khớp đúng hàng trong hệ thống', 'Có', 'Trống', 'Trống: "Thiếu Tên hàng" / "Thiếu Mã hàng"; không khớp: "Hàng hóa không tồn tại".'],
        ['Cột ĐVT', 'Textbox', 'Enable', 'Tên đơn vị tính', 'Có', 'Trống', '"Thiếu ĐVT" / "Đơn vị không tồn tại" / "Hàng hóa với đơn vị đã nhập không tồn tại"; cùng nhóm phải 1 ĐVT: "Cùng một hàng tại 1 kho phải dùng 1 ĐVT".'],
        ['Cột Mã kho', 'Textbox', 'Enable', 'Mã kho vật lý', 'Có', 'Trống', '"Thiếu Mã kho" / "Kho không tồn tại" / "Kho không thuộc công ty (chưa có kho kế toán của công ty)".'],
        ['Cột Mã vị trí', 'Textbox', 'Enable', 'Mã vị trí của kho', 'Có', 'Trống', '"Thiếu Mã vị trí" / "Vị trí không tồn tại trong kho" / "Vị trí đã được chọn!".'],
        ['Cột Số lượng', 'Textbox', 'Enable', 'Số > 0, ≤ 999,999,999', 'Có', 'Trống', '"Số lượng phải lớn hơn 0 và không quá 999,999,999".'],
        ['Cột Mã công ty', 'Textbox', 'Enable', 'Mã công ty được thao tác', 'Có', 'Trống', '"Thiếu Mã công ty" / "Công ty không tồn tại" / "Bạn không được làm việc tại công ty này".'],
        ['Lỗi theo nhóm', '–', '–', '–', '–', '–', '"Hàng hóa <mã> đã được khai báo tồn đầu kỳ tại kho <mã kho>, không thể nhập tiếp!" · "… đã có giao dịch, không thể nhập tồn đầu!" · "… chưa khai kho kế toán…" · "… khác số lượng đã khai kho kế toán (<a> theo ĐVT cơ bản, đang nhập <b>)…" · dòng hợp lệ cùng nhóm với dòng lỗi: "Cùng hàng + kho + công ty với dòng lỗi khác trong file — cả nhóm không được ghi".'],
        ['Nút Tải file mẫu / Chọn file Excel / Load lên bảng / Validate / Import', 'Button', 'Enable / Disable', '–', '–', '–', 'Import chỉ bấm được sau Validate.'],
        ['Nút Bỏ dòng lỗi / Xoá trạng thái validate / Làm mới / Đóng', 'Button', 'Enable', '–', '–', '–', 'Bỏ dòng lỗi khỏi bảng / mở khóa dòng đã validate / xoá bảng / đóng cửa sổ.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Load lên bảng', 'Click', 'During:\n– Đọc file (bỏ dòng hướng dẫn), quá 200 dòng thì báo và dừng.\nAfter:\n– Hiện dữ liệu lên bảng xem trước.'],
        ['Bấm Validate', 'Click', 'Before:\n– Kiểm tra quyền.\nDuring:\n– Kiểm từng dòng theo bảng trên, gom nhóm (hàng, kho, công ty), kiểm nhóm như Thêm tay.\nAfter:\n– Hiện Tổng / Hợp lệ / Lỗi; khóa dòng hợp lệ.'],
        ['Bấm Import', 'Click', 'Before:\n– Kiểm tra quyền.\nDuring:\n– Kiểm lại toàn bộ; từng nhóm kiểm lại ngay trước khi ghi.\n' + TRUOC_LUU + '\nAfter:\n– Mỗi nhóm ghi riêng như Thêm tay (khai báo + lô tồn đầu + tồn kho vật lý).\n– Báo kết quả, tải lại danh sách.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ, không nhập gì.'],
    ],
})

FR_NAMES = ['FR-%02d %s' % (i + 1, f['ten']) for i, f in enumerate(FR)]

S = {
    'ten': TEN, 'ten_ngan': 'khai báo tồn kho đầu kỳ', 'phan_he': 'Kho',
    'menu': [('Kho', 'menu_phanhe'), ('Tồn kho đầu kỳ', 'menu_nhom'), (TEN, 'menu_muc')],
    'muc_dich': [
        'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho việc khai báo TỒN KHO VẬT LÝ ĐẦU KỲ theo hàng × kho × vị trí × công ty — số mở đầu cho thẻ kho và các báo cáo tồn kho.',
        'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
        'Làm rõ luật khớp số liệu: tổng số lượng khai của một hàng tại một kho phải bằng số đã khai tồn kho kế toán đầu kỳ (áp cho Thêm, Sửa, Import).',
        'Làm rõ thời điểm khai báo bị khóa Sửa / Xóa: khi hàng đã có giao dịch kho khác tại kho đó của công ty.',
        'Làm rõ tác động số liệu: lưu / sửa / xóa khai báo ghi, điều chỉnh, đảo ngược tồn kho vật lý tương ứng.',
    ],
    'thuat_ngu': [
        ['Khai báo tồn kho đầu kỳ', 'Số lượng tồn vật lý của 1 hàng tại 1 vị trí trong 1 kho của 1 công ty tại thời điểm bắt đầu dùng hệ thống. Mỗi dòng danh sách = 1 hàng × 1 vị trí.'],
        ['Nhóm khai báo', 'Mọi dòng khai báo của cùng hàng + kho + công ty (các vị trí). Sửa, Xóa, kiểm khớp đều theo nhóm.'],
        ['SL tồn kế toán', 'Số đã khai tồn kho kế toán đầu kỳ của hàng tại kho (qua các kho kế toán của công ty), quy theo ĐVT của dòng.'],
        ['ĐVT cơ bản', 'Đơn vị tính hệ số 1 của hàng; so khớp tổng số lượng được quy về ĐVT này.'],
        ['Lô tồn đầu', 'Lô hàng hệ thống sinh cho mỗi dòng khai báo (số lô dạng TONDAUKHO-…), dùng khi xuất / chuyển vị trí hàng.'],
        ['Đã có giao dịch', 'Hàng tại kho + công ty đã có biến động tồn ngoài tồn đầu (nhập, xuất, điều chuyển…), hoặc có phiếu chuyển vị trí / phiếu xuất (kể cả phiếu nháp) lấy từ lô tồn đầu.'],
        ['Công ty được thao tác', 'Công ty đang làm việc + công ty gắn vai trò + công ty được giao quản lý của người dùng.'],
    ],
    'trang_thai': {
        'cau_dan': 'Khai báo KHÔNG qua bước gửi duyệt / duyệt / từ chối / hủy: lưu xong là có hiệu lực ngay (đã ghi tồn kho vật lý). '
                   'Trạng thái của nhóm khai báo do hệ thống tự xác định mỗi lần hiển thị, theo việc hàng đã có giao dịch tại kho của công ty hay chưa; không có ô trạng thái để chọn.',
        'rows': [
            ['Chưa có giao dịch', 'Nhóm đã ghi tồn đầu, hàng chưa có biến động kho nào khác tại kho + công ty.', 'Xem, Sửa (cả nhóm), Xóa (cả nhóm), Xuất', 'Người có quyền "%s" thuộc công ty được thao tác' % QUYEN],
            ['Đã có giao dịch', 'Hàng đã có nhập / xuất / điều chuyển… tại kho + công ty, hoặc có phiếu chuyển vị trí / phiếu xuất (kể cả nháp) lấy từ lô tồn đầu.', 'Xem, Xuất (không Sửa, không Xóa, không khai thêm)', 'Tự chuyển khi phát sinh giao dịch kho'],
            ['Đã xóa', 'Mọi dòng của nhóm, lô tồn đầu và phần tồn vật lý đã ghi bị gỡ khỏi hệ thống.', '–', 'Người có quyền "%s", chỉ từ trạng thái Chưa có giao dịch' % QUYEN],
        ],
        'anh': 'state_flow',
        'ghi_chu': ['Sau khi xóa, nhóm (hàng, kho, công ty) được khai lại như mới. Nhóm Đã có giao dịch thì cả Thêm tay lẫn Import đều bị chặn "đã có giao dịch, không thể nhập tồn đầu!" (BR-05).'],
    },
    'quyen_truoc': ['Một quyền duy nhất cho cả màn (xem lẫn thao tác), nhóm quyền "Tồn kho đầu kỳ" của phân hệ Kho:'],
    'quyen_rows': [[QUYEN, 'Thấy mục menu, vào màn; xem danh sách, tìm kiếm, tuỳ chỉnh cột, xuất Excel; Tạo mới, Sửa, Xóa, Import Excel.']],
    'pham_vi_truoc': ['Phạm vi dữ liệu (theo công ty của dòng khai báo):'],
    'pham_vi_rows': [
        ['1', 'Quản trị cao nhất của hệ thống', 'Mọi công ty đang hoạt động; danh sách có cột Công ty và ô lọc Công ty.'],
        ['2', QUYEN, 'Chỉ dòng của công ty được thao tác (công ty đang làm việc, công ty gắn vai trò, công ty được giao quản lý); không có cột / ô lọc Công ty mặc định.'],
    ],
    'pham_vi_sau': ['Phạm vi áp như nhau cho danh sách, Sửa, Xóa, xuất Excel, ô Công ty ở trang Thêm và cột Mã công ty khi Import. '
                    'Dòng ngoài phạm vi: không hiện ở danh sách; mở thẳng trang Sửa thì báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang".'],
    'ma_tran': [['Chức năng', QUYEN, 'Không có quyền']] + [
        [f, 'Có' + (' (nhóm Chưa có giao dịch)' if i in (6, 7) else ''), 'Không'] for i, f in enumerate(FR_NAMES)],
    'ma_tran_widths': [3.0, 2.0, 1.2],
    'quyen_sau': ['Phạm vi dữ liệu của mọi chức năng theo bảng phạm vi ở trên.'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Một dòng = 1 hàng × 1 vị trí; nghiệp vụ theo nhóm', ['– Mỗi vị trí của hàng lưu thành 1 dòng khai báo (1 lô tồn đầu).', '– Nhóm = hàng + kho + công ty; Sửa / Xóa luôn áp cho cả nhóm.'], ['Thêm', 'Sửa', 'Xóa', 'Import']),
        ('BR-02', 'Phạm vi công ty', ['– Quản trị cao nhất: mọi công ty, có cột và ô lọc Công ty.', '– Người khác: chỉ công ty được thao tác; khai báo / import cho công ty khác bị chặn "Bạn không được làm việc tại công ty này".'], ['Mọi chức năng']),
        ('BR-03', 'Kho phải thuộc công ty', ['– Kho chọn / import phải có kho kế toán của công ty khai báo ("Kho không thuộc công ty đã chọn" / "Kho không thuộc công ty (chưa có kho kế toán của công ty)").', '– Vị trí phải thuộc kho và đang hoạt động (popup chọn chỉ liệt kê vị trí không bị khóa).'], ['Thêm', 'Import']),
        ('BR-04', 'Khớp tồn kho kế toán đầu kỳ', ['– Hàng phải đã khai tồn kho kế toán đầu kỳ tại kho của công ty; ĐVT lấy theo khai báo kế toán.', '– Tổng số lượng các vị trí (quy ĐVT cơ bản) phải BẰNG số kế toán; lệch thì báo đỏ, không tự sửa.', '– Áp cho Thêm tay, Sửa, Import.'], ['Thêm', 'Sửa', 'Import']),
        ('BR-05', 'Chặn khi đã có giao dịch', ['– Đã có giao dịch = hàng tại kho + công ty có biến động tồn khác tồn đầu, hoặc có phiếu chuyển vị trí / phiếu xuất (kể cả nháp) lấy từ lô tồn đầu.', '– Nút Sửa, Xóa ẩn; hệ thống chặn cả khi mở thẳng trang Sửa hoặc lưu: "Hàng hóa đã có giao dịch, không thể sửa / xóa tồn đầu!".', '– Thêm / Import hàng đã có giao dịch: "… đã có giao dịch, không thể nhập tồn đầu!".'], ['Sửa', 'Xóa', 'Thêm', 'Import']),
        ('BR-06', 'Không khai trùng', ['– Mỗi nhóm (hàng, kho, công ty) chỉ khai 1 lần; muốn đổi thì Sửa hoặc Xóa rồi khai lại.', '– Trong 1 hàng không chọn trùng vị trí; trong 1 lần lưu không chọn trùng hàng.', '– Hai lượt lưu / import cùng hàng đồng thời: lượt sau bị chặn.'], ['Thêm', 'Chọn hàng hóa', 'Import']),
        ('BR-07', 'Ghi tồn kho vật lý', ['– Thêm: mỗi dòng sinh 1 lô tồn đầu và cộng tồn kho vật lý theo kho, vị trí, công ty khai báo (ngày ghi sổ tồn đầu = mốc đầu kỳ của hệ thống).', '– Sửa: điều chỉnh lô và tồn theo phần chênh lệch số lượng.', '– Xóa: đảo ngược phần tồn đã cộng, xóa lô.', '– Cả lần lưu nằm trong 1 giao dịch: lỗi bất kỳ thì không ghi gì.'], ['Thêm', 'Sửa', 'Xóa', 'Import']),
        ('BR-08', 'Số lượng', ['– Lớn hơn 0, tối đa 999,999,999, tối đa 2 chữ số thập phân khi hiển thị.'], ['Thêm', 'Sửa', 'Import']),
        ('BR-09', 'Import', ['– Tối đa 200 dòng mỗi lần; dòng gom theo nhóm; một dòng lỗi làm cả nhóm không được ghi.', '– Mỗi nhóm ghi trong 1 giao dịch riêng: nhóm lỗi lúc ghi không ảnh hưởng nhóm khác.'], ['Import']),
        ('BR-10', 'Xuất Excel', ['– Xuất theo đúng bộ lọc và phạm vi (mọi trang); ô Số lượng là SỐ; không có dữ liệu thì không xuất file.'], ['Xuất Excel']),
        ('BR-11', 'Thao tác xong quay về danh sách', ['– Lưu (Thêm / Sửa) xong về màn danh sách; Lưu và tiếp tục mở lại trang Thêm trống.'], ['Thêm', 'Sửa']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây đọc hoặc dùng dữ liệu do Khai báo tồn kho đầu kỳ ghi ra (dòng khai báo, lô tồn đầu và tồn kho vật lý theo kho, vị trí, công ty). Phiếu chuyển vị trí / phiếu xuất lấy từ lô tồn đầu làm khai báo bị khóa Sửa / Xóa (BR-05).',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng có quyền "%s"' % QUYEN,
    'mains': [('FR-01', 'Xem danh sách khai báo', 'view'), ('FR-04', 'Thêm khai báo tồn kho đầu kỳ', 'crud'),
              ('FR-07', 'Sửa khai báo', 'crud'), ('FR-08', 'Xóa khai báo', 'action'),
              ('FR-09', 'Xuất Excel danh sách', 'io'), ('FR-10', 'Import khai báo từ Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc danh sách', 'view'), ('FR-03', 'Cài đặt bộ lọc, tuỳ chỉnh cột', 'view')],
    'rieng': [('FR-04', 'Thêm khai báo tồn kho đầu kỳ', 'crud', 'uc_them'), ('FR-05', 'Chọn hàng hóa khai báo tồn đầu', 'crud', 'uc_chonhang'),
              ('FR-06', 'Chọn vị trí kho', 'crud', 'uc_chonvitri'), ('FR-07', 'Sửa khai báo', 'crud', 'uc_sua'),
              ('FR-08', 'Xóa khai báo', 'action', 'uc_xoa'), ('FR-09', 'Xuất Excel danh sách', 'io', 'uc_xuat'),
              ('FR-10', 'Import khai báo từ Excel', 'io', 'uc_import')],
}

STATES = [('start', '', None), ('chua', 'Chưa có giao dịch', '#dcfce7'), ('da', 'Đã có giao dịch', '#fef3c7'),
          ('end', '', None)]
TRANS = [('start', 'chua', 'Lưu / Import'), ('chua', 'da', 'Phát sinh giao dịch kho'),
         ('chua', 'end', 'Xóa (cả nhóm)')]

if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    L.draw_state_flow(os.path.join(scr.uml, 'state_flow.png'), STATES, TRANS)
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))

# -*- coding: utf-8 -*-
"""SRS - Danh sách cần hạch toán chi phí vận chuyển nhanh (STT 181) — khuôn PHIẾU đợt 3/4 (màn mẫu 167, _lib_phieu.py).

Nguồn (code HRM origin/develop, dò 18/11/2026):
  FE hrm-client/pages/finance/fast-delivery-accountings/{index.vue, components/constants.js},
     components/subsystem-menu/finance.js (nhóm Nhập hàng), components/V2BaseCompanyDepartmentFilter.vue,
     pages/finance/bill-adjust-depts/{create.vue, components/BillAdjustDeptForm.vue, ContractPickerModal.vue}
  BE Modules/Finance: Services/FastDelivery/FastDeliveryAccountingService.php, Http/Controllers/V1/
     FastDeliveryAccountingController.php, Services/BillAdjustDeptSourceService.php (fromFastDelivery,
     guardFastDeliveryOnCreate, onBillCreated, onBillDeleted), Entities/BillAdjustDept/BillAdjustDept.php,
     app/Support/Permissions/Catalog/purchase.php (2 quyền), finance.php (Kế toán thanh toán)
  Ảnh: capture.js (dev-hrm 18/11/2026).
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402
from _lib_phieu import ui, UI4, UI4W, UI6, UI6W, UI7, UI7W, UI8, UI8W, TRUOC_LUU  # noqa: E402

TEN = 'Danh sách cần hạch toán chi phí vận chuyển nhanh'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q_XEM = 'Xem hạch toán chi phí vận chuyển nhanh'
Q_HT = 'Hạch toán chi phí vận chuyển nhanh'
Q_KT = 'Kế toán thanh toán'
TAC_NHAN = 'Người dùng đăng nhập hệ thống (mọi người dùng mở được màn; dữ liệu theo quyền "%s", thao tác hạch toán theo quyền "%s")' % (Q_XEM, Q_HT)
TAC_NHAN_HT = 'Kế toán có quyền "%s" và quyền "%s"' % (Q_HT, Q_KT)
DK = '1. Người dùng đăng nhập thành công.'
DK_HT = DK + '\n2. Người dùng có quyền "%s" (nút Tạo phiếu kế toán chỉ hiện khi có quyền này).' % Q_HT
POPUP = 'Modal %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'

# ------------------------------------------------------------------ Phần 5 (dò code 18/11/2026)
P5 = [
    ('Tài chính', 'Phiếu kế toán (trang Tạo phiếu kế toán nạp các dòng đã chọn: ô "Chi phí vận chuyển nhanh", định khoản Nợ 35241 / Có 811; lưu phiếu thì dòng chuyển trạng thái; xóa phiếu Đang tạo thì dòng trở về Chưa hạch toán)',
     'Tài chính => Sổ tổng hợp => Phiếu kế toán'),
    ('Tài chính', 'Phiếu kế toán — cửa sổ chọn Đơn hàng/Hợp đồng ở dòng định khoản sinh từ chi phí vận chuyển nhanh (chỉ hợp đồng bán của khách do nhân viên chịu phí lập)',
     'Tài chính => Sổ tổng hợp => Phiếu kế toán => Tạo phiếu kế toán'),
    ('Tài chính', 'Phiếu nhập hàng (tab "Phân bổ chi phí vận chuyển nhanh" — cùng dữ liệu chi phí giao nhanh của hợp đồng mua; phiếu nhập hoàn thành là điều kiện để dòng lên danh sách)',
     'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng => Phiếu nhập hàng'),
]

FR = []

# 2.1 Xem danh sách -------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách cần hạch toán',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách cần hạch toán chi phí vận chuyển nhanh'],
        ['Mô tả', 'Hiển thị các khoản chi phí giao nhanh do khách hàng chịu, khai trên hợp đồng mua đã duyệt, hàng đã về kho (có phiếu nhập hàng hoàn thành có hàng của đúng khách hàng) — cả dòng chưa và đã hạch toán, trong phạm vi dữ liệu của người dùng. Mỗi dòng giao nhanh = 1 tổ hợp (Hợp đồng mua, Nhân viên chịu phí, Khách hàng); mỗi hàng hoá 1 dòng bảng, các ô khác gộp dọc.'],
        ['Tác nhân', TAC_NHAN],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tự tải trang 1 (10 dòng giao nhanh / trang) theo phạm vi dữ liệu (BR-02), thứ tự theo thứ tự lập dòng giao nhanh (cũ trước).\n3. Bảng hiển thị 12 cột, chân bảng ghi "Hiển thị a–b / N" (N = số dòng giao nhanh, không phải số dòng hàng hoá).'],
        ['Dòng sự kiện phụ', '• Không có dòng khớp → bảng "Không có dữ liệu phù hợp."\n• Mở bằng đường link việc cần làm có điều kiện trạng thái = 0 → ô Trạng thái tự chọn "Chưa hạch toán".\n• Không có quyền "%s" → không có nút Tạo phiếu kế toán, ô Hạch toán mọi dòng bị khoá.\n• Phiên đăng nhập hết hạn → hệ thống chuyển về trang đăng nhập.\n• Lỗi tải dữ liệu → báo "Đã xảy ra lỗi hệ thống. Vui lòng thử lại.", bảng rỗng.' % Q_HT],
    ],
    'anh': [('01_list', 'Màn Danh sách cần hạch toán chi phí vận chuyển nhanh lúc mới truy cập (dòng nhiều hàng hoá gộp ô)'),
            ('03_states', 'Các cột bên phải: Phiếu kế toán, Hợp đồng mua, Người tạo, Người duyệt, Trạng thái (Đã duyệt / Đang tạo)')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Danh sách cần hạch toán chi phí vận chuyển nhanh', 'Tiêu đề khối danh sách và tiêu đề trang.'],
        ['Nút Tạo phiếu kế toán', 'Button', 'Enable / Ẩn', 'Theo quyền', 'Chỉ hiện khi có quyền "%s". Mở trang Tạo phiếu kế toán với các dòng đã tick (mục 2.4).' % Q_HT],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất Excel" (mục 2.6). Trong lúc xuất nút khoá, cạnh nút hiện tiến độ.'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.3).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Đánh theo dòng giao nhanh, liên tục qua các trang. Cột khoá.'],
        ['Cột Nhân viên chịu phí', 'Table/Grid', 'Read-only', 'Hiển thị', '"Mã - Tên" nhân viên chịu phí khai trên hợp đồng mua.'],
        ['Cột Phiếu nhập', 'Table/Grid', 'Read-only', 'Hiển thị', 'Mã phiếu nhập hàng (nhiều phiếu thì lấy phiếu lập trước). Liên kết mở chi tiết phiếu nhập ở tab mới.'],
        ['Cột Khách hàng', 'Table/Grid', 'Read-only', 'Hiển thị', '"Mã - Tên khách hàng".'],
        ['Cột Hàng hóa', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên hàng + dòng "Mã hàng: …" (nhãn in đậm). Mỗi hàng 1 dòng, không lặp khi có nhiều phiếu nhập. Cột khoá.'],
        ['Cột Chi phí KH', 'Table/Grid', 'Read-only', 'Hiển thị', 'Chi phí theo khách hàng + loại tiền của hợp đồng mua, vd "1,250 USD", "21,775 JPY"; tối đa 2 chữ số thập phân, căn phải.'],
        ['Cột Hạch toán', 'Checkbox', 'Enable / Disable', 'Không tích', '- Dòng đã hạch toán / đã gắn phiếu kế toán: tích sẵn và khoá.\n- Thiếu quyền "%s": khoá.\n- Tick chỉ có tác dụng trong trang đang xem. Cột khoá.' % Q_HT],
        ['Cột Phiếu kế toán', 'Table/Grid', 'Read-only', 'Hiển thị', 'Mã phiếu kế toán gắn dòng; liên kết mở chi tiết phiếu ở tab mới. Chưa có thì để trống.'],
        ['Cột Hợp đồng mua', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số hợp đồng mua (kể cả phụ lục); liên kết mở trang xem hợp đồng mua ở tab mới.'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'Người lập phiếu nhập hàng.'],
        ['Cột Người duyệt', 'Table/Grid', 'Read-only', 'Hiển thị', 'Người duyệt phiếu kế toán; chưa duyệt thì để trống.'],
        ['Cột Trạng thái', 'Badge', 'Read-only', 'Hiển thị', 'Theo phiếu kế toán gắn dòng: Chưa hạch toán (vàng), Đang tạo (xám), Đã duyệt (xanh lá), Hủy (đỏ).'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Số dòng/trang: 5, 10, 20, 50, 100; «, ‹, số trang, ›, »; chân bảng "Hiển thị a–b / N". Một dòng giao nhanh không bị tách sang 2 trang.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Không chặn quyền ở menu: mọi người dùng mở được màn.\nAfter:\n– Tải trang 1 theo phạm vi dữ liệu (BR-02), bộ lọc trống; có điều kiện trạng thái = 0 trên đường link thì lọc sẵn Chưa hạch toán.\n– Bật nút Tạo phiếu kế toán / ô Hạch toán theo quyền "%s".' % Q_HT],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc, tải lại dữ liệu; đổi số dòng thì về trang 1.\n– Bỏ mọi tick đang chọn.'],
        ['Bấm tiêu đề cột', 'Click', 'After:\n– Không đổi thứ tự (màn không có cột sắp xếp).'],
        ['Bấm mã Phiếu nhập / Phiếu kế toán / Hợp đồng mua', 'Click', 'After:\n– Mở chứng từ ở tab mới (mục 2.5).'],
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc danh sách',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách cần hạch toán'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao.'],
        ['Tác nhân', TAC_NHAN],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập từ khoá rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện (cùng phạm vi dữ liệu) và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô gõ chữ (tìm nhanh, Phiếu kế toán, Hợp đồng) chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Bấm Làm mới → xoá mọi điều kiện, tải lại đủ dòng trong phạm vi.\n• Không có dòng khớp → "Không có dữ liệu phù hợp."\n• Màn không có trang chi tiết riêng (liên kết mở tab mới) nên rời màn rồi quay lại hoặc tải lại trang (F5) thì bộ lọc trở về mặc định.\n• Ô Công ty / Phòng ban / Bộ phận / Nhân viên chỉ hiện theo quyền phạm vi (BR-02); chọn công ty / phòng ban ngoài phạm vi không làm lộ dữ liệu.'],
    ],
    'anh': [('02_filter', 'Khu vực Tìm kiếm nâng cao ở trạng thái mở'),
            ('02b_status_options', 'Ô Trạng thái: Chưa hạch toán, Đang tạo, Đã duyệt, Hủy')],
    'ui': ui(UI7, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', '- Placeholder "Tìm theo mã HĐ mua, phiếu nhập, khách hàng".\n- Tìm gần đúng, không phân biệt hoa thường theo số hợp đồng mua, mã phiếu nhập, mã / tên khách hàng; ký tự % và _ được tìm đúng nghĩa đen.'],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Áp dụng từ khoá và các ô lọc.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá mọi điều kiện lọc và tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực ô lọc (khi mở, nút đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" (mục 2.3).'],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Trống', '- Chỉ hiện với quyền xem mức Tổng công ty.\n- Lọc theo công ty của NHÂN VIÊN CHỊU PHÍ.\n- Biểu tượng ổ khoá cạnh nhãn: bấm để hiện cả công ty đã khoá.'],
        ['Ô Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Phòng ban của công ty đã chọn', 'Trống', 'Hiện với quyền mức Tổng công ty / Công ty / Phòng ban; đổi Công ty thì tự xoá.'],
        ['Ô Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Bộ phận của phòng đã chọn', 'Trống', 'Hiện khi có quyền xem ở bất kỳ mức nào; đổi cấp trên thì tự xoá.'],
        ['Ô Nhân viên', 'Dropdown', 'Enable / Ẩn', 'Nhân viên thuộc lựa chọn phía trên', 'Trống', 'Lọc theo nhân viên chịu phí. Biểu tượng ổ khoá: hiện cả nhân viên đã nghỉ.'],
        ['Ô Ngày nhập', 'Datepicker', 'Enable', 'dd/mm/yyyy, Từ → Đến', 'Trống', 'Lọc theo ngày lập phiếu nhập hàng, tính trọn ngày (00:00 ngày đầu tới 23:59:59 ngày cuối).'],
        ['Ô Trạng thái', 'Dropdown', 'Enable', 'Chưa hạch toán, Đang tạo, Đã duyệt, Hủy', 'Trống', 'Lọc theo đúng trạng thái cột Trạng thái. Chưa hạch toán = chưa gắn phiếu kế toán.'],
        ['Ô Khách hàng', 'Dropdown', 'Enable', 'Gõ ≥ 2 ký tự để tìm', 'Trống', 'Placeholder "Gõ để tìm khách hàng..."; có nút x để xoá; tải lại trang vẫn giữ tên đã chọn.'],
        ['Ô Phiếu kế toán', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Nhập mã phiếu kế toán"; tìm gần đúng; lọc khi Enter / Tìm kiếm.'],
        ['Ô Hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Nhập mã hợp đồng"; tìm gần đúng số hợp đồng mua (gồm cả phụ lục).'],
        ['Ô Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc theo người duyệt phiếu kế toán.'],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm Tìm kiếm / nhấn Enter ở ô gõ chữ', 'Click', 'After:\n– Áp đồng thời từ khoá và các ô lọc, tải lại bảng từ trang 1, bỏ tick.'],
        ['Chọn giá trị ở ô chọn', 'Change', 'After:\n– Tải lại bảng từ trang 1 ngay.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ trong phạm vi.'],
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
        ['Tác nhân', TAC_NHAN],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Bấm "Cài đặt bộ lọc" (hoặc biểu tượng Cấu hình cột hiển thị).\n2. Tích / bỏ tích, kéo ☰ để đổi thứ tự.\n3. Bấm Lưu: hệ thống lưu cấu hình và áp dụng ngay.'],
        ['Dòng sự kiện phụ', '• Bấm Đóng: bỏ thay đổi.\n• Cài đặt bộ lọc có nút "Khôi phục mặc định".\n• Cột STT, Hàng hóa, Hạch toán không bỏ được (có biểu tượng khoá).\n• Ẩn cột không ảnh hưởng gộp ô, tick và tạo phiếu kế toán.'],
    ],
    'menu_them': ' => Cài đặt bộ lọc {icon:btn_caidatboloc} / Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': 'Modal Cài đặt bộ lọc và Modal Tuỳ chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('26_filtercfg', 'Cửa sổ Cài đặt bộ lọc'), ('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột')],
    'ui': ui(UI6, [
        ['Danh sách ô lọc', 'Checkbox', 'Enable', 'Đủ 7 mục', 'Công ty – Phòng ban, Ngày nhập, Trạng thái, Khách hàng, Phiếu kế toán, Hợp đồng, Người duyệt. Kéo ☰ đổi thứ tự.'],
        ['Nút Khôi phục mặc định', 'Button', 'Enable', '–', 'Đưa cấu hình ô lọc về mặc định.'],
        ['Danh sách cột', 'Checkbox', 'Enable', '12/12 cột', 'Tích cột muốn hiện; STT, Hàng hóa, Hạch toán bị khoá. Dòng đếm "Đang chọn x/12 cột".'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Chọn / bỏ nhanh mọi cột (trừ cột khoá).'],
        ['Nút Lưu', 'Button', 'Enable', '–', 'Lưu cấu hình theo người dùng, áp dụng ngay, giữ sau khi tải lại trang.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ, không lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình theo người dùng, đóng cửa sổ, bảng / khu vực lọc vẽ lại theo cấu hình.'],
        ['Kéo ☰', 'Drag', 'After:\n– Đổi thứ tự dòng trong cửa sổ.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ, không lưu.'],
    ],
})

# 2.4 Chọn dòng + Tạo phiếu kế toán ---------------------------------------------
FR.append({
    'ten': 'Chọn dòng và tạo phiếu kế toán', 'uc': 'uc_tao', 'uc_ten': 'FR-04 Chọn dòng và tạo phiếu kế toán',
    'qtc': 'Màn Danh sách, Thông báo và UI/UX.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chọn dòng cần hạch toán và mở trang Tạo phiếu kế toán'],
        ['Mô tả', 'Kế toán tick các dòng Chưa hạch toán trong trang đang xem rồi bấm "Tạo phiếu kế toán". Hệ thống mở trang Tạo phiếu kế toán đã nạp sẵn: mỗi dòng giao nhanh thành 1 nhóm định khoản 2 dòng Nợ 35241 / Có 811 cùng số tiền, đối tượng là khách hàng của dòng.'],
        ['Tác nhân', TAC_NHAN_HT],
        ['Điều kiện ban đầu', DK_HT + '\n3. Có ít nhất 1 dòng Chưa hạch toán trong trang đang xem.'],
        ['Dòng sự kiện chính', '1. Người dùng tick ô Hạch toán của 1 hoặc nhiều dòng.\n2. Bấm "Tạo phiếu kế toán".\n3. Hệ thống mở trang "Tạo phiếu kế toán": ô "Chi phí vận chuyển nhanh" = "<số dòng đã chọn> dòng"; Ngày hạch toán = hôm nay; Loại tiền = loại tiền hợp đồng mua của dòng lập trước nhất (BR-05); Tỷ giá theo danh mục tiền tệ (VNĐ = 1).\n4. Bảng Chi tiết nạp sẵn các nhóm Nợ 35241 / Có 811 (Mã khách, Tên khách, Phát sinh nợ / có nguyên tệ và quy đổi VNĐ).\n5. Người dùng lưu phiếu (mục 2.5).'],
        ['Dòng sự kiện phụ', '• Chưa tick dòng nào → báo "Vui lòng chọn ít nhất một mục để tạo phiếu kế toán", không chuyển trang.\n• Dòng đã hạch toán / thiếu quyền: ô tick khoá, không chọn được.\n• Đổi trang, đổi bộ lọc → mọi tick bị bỏ.\n• Loại tiền của hợp đồng mua không có trong danh mục tiền tệ đang dùng → ô Loại tiền để trống cho người dùng chọn.\n• Bấm Quay lại trên trang Tạo phiếu kế toán → không lưu, dòng vẫn Chưa hạch toán.'],
        ['Yêu cầu đặc biệt', 'Không có nút thêm / xoá nhóm định khoản sinh từ chi phí vận chuyển nhanh; số tiền nạp đúng Chi phí KH.'],
    ],
    'menu_them': ' => tick ô Hạch toán {icon:o_hachtoan} => Tạo phiếu kế toán {icon:btn_taophieukt}',
    'ghi_chu_layout': 'Trang Tạo phiếu kế toán (phân hệ Tài chính) được mở từ màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('10_no_select', 'Bấm "Tạo phiếu kế toán" khi chưa tick dòng nào'),
            ('11_ticked', 'Đã tick 2 dòng Chưa hạch toán (lọc sẵn Chưa hạch toán)'),
            ('12_bill_form', 'Trang Tạo phiếu kế toán nạp sẵn 2 dòng: 4 dòng định khoản Nợ 35241 / Có 811, Loại tiền EURO')],
    'ui': ui(UI8, [
        ['Ô Hạch toán (danh sách)', 'Checkbox', 'Enable / Disable', 'Dòng Chưa hạch toán', 'Có (≥ 1 dòng)', 'Không tích', 'Tick / bỏ tick; khoá khi dòng đã hạch toán hoặc thiếu quyền.'],
        ['Nút Tạo phiếu kế toán', 'Button', 'Enable / Ẩn', '–', '–', '–', 'Ẩn khi thiếu quyền "%s".' % Q_HT],
        ['Chi phí vận chuyển nhanh', 'Textbox', 'Read-only', '–', '–', '"<n> dòng"', 'Số dòng giao nhanh đã chọn.'],
        ['Ngày hạch toán', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Hôm nay', 'Ngày ghi sổ của phiếu.'],
        ['Loại tiền', 'Dropdown', 'Enable', 'Danh mục tiền tệ đang dùng', 'Có', 'Loại tiền hợp đồng mua của dòng đầu', 'Không tìm thấy trong danh mục thì để trống.'],
        ['Tỷ giá', 'Textbox', 'Enable', 'Số > 0', 'Có', 'Theo danh mục (VNĐ = 1)', 'Tên loại tiền hiện cuối ô.'],
        ['Diễn giải', 'Textarea', 'Enable', 'Văn bản', 'Có khi Lưu và duyệt', 'Trống', 'Placeholder "Nhập diễn giải".'],
        ['Bảng Chi tiết', 'Table/Grid', 'Enable', '2 dòng / dòng giao nhanh', 'Có', 'Nợ 35241 / Có 811', 'Số tài khoản, Tên tài khoản, Mã khách, Tên khách, Phát sinh nợ, Phát sinh có (nguyên tệ + VNĐ), Diễn giải, Đơn hàng/Hợp đồng, NVKD…; dòng Tổng cuối bảng.'],
        ['Nút Lưu nháp / Lưu và duyệt / Lưu và tiếp tục / Quay lại', 'Button', 'Enable', '–', '–', '–', 'Xem mục 2.5.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Tick / bỏ tick ô Hạch toán', 'Click', 'During:\n– Dòng khoá: bỏ qua.\nAfter:\n– Thêm / bỏ dòng khỏi danh sách đã chọn của trang đang xem.'],
        ['Bấm Tạo phiếu kế toán', 'Click', 'Before:\n– Nút chỉ hiện khi có quyền "%s".\nDuring:\n– Chưa chọn dòng nào → báo "Vui lòng chọn ít nhất một mục để tạo phiếu kế toán", dừng.\nAfter:\n– Chuyển sang trang Tạo phiếu kế toán kèm các dòng đã chọn; hệ thống nạp thông tin chung và bảng Chi tiết như mô tả.' % Q_HT],
        ['Mở trang Tạo phiếu kế toán', 'System', 'After:\n– Nạp các dòng đã chọn với phạm vi "tất cả"; dòng không còn đủ điều kiện (hợp đồng mua không còn duyệt, chưa có phiếu nhập hoàn thành) không được nạp.'],
    ],
})

# 2.5 Lưu phiếu kế toán (hạch toán) ----------------------------------------------
FR.append({
    'ten': 'Lưu phiếu kế toán hạch toán chi phí', 'uc': 'uc_luu', 'uc_ten': 'FR-05 Lưu phiếu kế toán hạch toán chi phí vận chuyển nhanh',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.',
    'gioi_thieu': [
        ['Tên chức năng', 'Lưu phiếu kế toán hạch toán chi phí vận chuyển nhanh'],
        ['Mô tả', 'Trên trang Tạo phiếu kế toán đã nạp từ danh sách, kế toán Lưu nháp (phiếu Đang tạo) hoặc Lưu và duyệt (phiếu Đã duyệt, ghi bút toán vào sổ cái). Ngay khi lưu, các dòng giao nhanh đã chọn được đánh dấu đã hạch toán và gắn mã phiếu.'],
        ['Tác nhân', TAC_NHAN_HT],
        ['Điều kiện ban đầu', DK_HT + '\n3. Người dùng có quyền "%s".\n4. Các dòng đã chọn đang Chưa hạch toán.' % Q_KT],
        ['Dòng sự kiện chính', '1. Người dùng nhập Ngày hạch toán (và Diễn giải, Diễn giải từng dòng khi duyệt), bấm "Lưu nháp" hoặc "Lưu và duyệt".\n2. "Lưu và duyệt": hệ thống hỏi "Xác nhận duyệt phiếu kế toán" — "Duyệt phiếu sẽ GHI BÚT TOÁN VÀO SỔ CÁI và không thể hoàn tác. Bạn có chắc chắn muốn duyệt?"; người dùng bấm Duyệt.\n3. Hệ thống kiểm tra quyền "%s" và tình trạng các dòng (BR-06), khoá các dòng trong lúc lưu.\n4. Ghi phiếu kế toán; mọi dòng đã chọn chuyển đã hạch toán, gắn mã phiếu.\n5. Báo thành công, chuyển về danh sách Phiếu kế toán.\n6. Trên màn danh sách cần hạch toán: dòng có ô Hạch toán tích sẵn + khoá, cột Phiếu kế toán = mã phiếu, Trạng thái Đang tạo (Lưu nháp) hoặc Đã duyệt + Người duyệt (Lưu và duyệt).' % Q_HT],
        ['Dòng sự kiện phụ', '• "Lưu và tiếp tục": lưu nháp rồi ở lại trang Tạo phiếu kế toán trống, không nạp lại các dòng vừa hạch toán.\n• Lưu nháp chỉ bắt buộc Ngày hạch toán; Lưu và duyệt kiểm đủ (Loại tiền, Tỷ giá, Diễn giải, cân Nợ / Có) — thiếu thì báo "Bạn chưa nhập đầy đủ thông tin.".\n• Dòng đã được người khác hạch toán / không còn đủ điều kiện → "Trạng thái đã bị thay đổi. Vui lòng load lại trang", không tạo phiếu.\n• Thiếu quyền "%s" → "Bạn không có quyền thực hiện thao tác này", không tạo phiếu.\n• Thiếu quyền "%s" → hệ thống từ chối lưu, báo không có quyền; nút "Lưu và duyệt" không hiện.\n• Sửa phiếu Đang tạo sau đó không thêm / bớt dòng giao nhanh đã gắn.\n• Xoá phiếu kế toán Đang tạo → các dòng trở về Chưa hạch toán, tạo phiếu lại được.' % (Q_HT, Q_KT)],
        ['Yêu cầu đặc biệt', 'Hai người cùng lập phiếu cho cùng dòng: chỉ người lưu trước thành công, người sau nhận "Trạng thái đã bị thay đổi. Vui lòng load lại trang". Nút lưu bị khoá trong lúc lưu.'],
    ],
    'menu_them': ' => Tạo phiếu kế toán {icon:btn_taophieukt} => Lưu nháp {icon:btn_luunhap} / Lưu và duyệt {icon:btn_luuduyet}',
    'ghi_chu_layout': 'Các nút nằm ở chân trang Tạo phiếu kế toán (ảnh mục 2.4).',
    'anh': [('12b_bill_form_full', 'Trang Tạo phiếu kế toán đầy đủ — chân trang có Lưu nháp, Lưu và duyệt, Lưu và tiếp tục, Quay lại')],
    'ui': ui(UI4, [
        ['Nút Lưu nháp', 'Button', 'Lưu phiếu trạng thái Đang tạo; dòng chuyển đã hạch toán, gắn phiếu.'],
        ['Nút Lưu và duyệt', 'Button', 'Chỉ hiện khi có quyền "%s". Hỏi xác nhận rồi lưu phiếu Đã duyệt, ghi bút toán Nợ 35241 / Có 811 vào sổ cái.' % Q_KT],
        ['Nút Lưu và tiếp tục', 'Button', 'Lưu nháp rồi mở trang Tạo phiếu kế toán trống.'],
        ['Nút Quay lại', 'Button', 'Không lưu, rời trang Tạo phiếu kế toán; dòng giữ Chưa hạch toán.'],
        ['Hộp Xác nhận duyệt phiếu kế toán', 'Popup', 'Nút Duyệt / Hủy.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Lưu nháp / Lưu và tiếp tục', 'Click', 'Before:\n– Kiểm tra quyền "%s" và "%s".\nDuring:\n– Ngày hạch toán bắt buộc; khoá các dòng giao nhanh, dòng đã hạch toán / đã gắn phiếu / không còn đủ điều kiện → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n' % (Q_KT, Q_HT) + TRUOC_LUU + '\nAfter:\n– Ghi phiếu Đang tạo; đánh dấu các dòng đã hạch toán + gắn mã phiếu.\n– Báo thành công; Lưu nháp về danh sách Phiếu kế toán, Lưu và tiếp tục ở lại trang Tạo trống.'],
        ['Bấm Lưu và duyệt → Duyệt', 'Click', 'Before:\n– Kiểm tra quyền như trên.\nDuring:\n– Kiểm đủ trường, cân Nợ / Có và tình trạng dòng như trên.\n' + TRUOC_LUU + '\nAfter:\n– Ghi phiếu Đã duyệt, ghi bút toán vào sổ cái; dòng gắn phiếu, cột Người duyệt = người duyệt.'],
        ['Xoá phiếu kế toán Đang tạo (màn Phiếu kế toán)', 'Click', 'After:\n– Các dòng gắn phiếu trở về Chưa hạch toán, bỏ mã phiếu.'],
    ],
})

# 2.6 Xem chứng từ liên kết --------------------------------------------------------
FR.append({
    'ten': 'Xem chứng từ liên kết', 'uc': 'uc_xem', 'uc_ten': 'FR-06 Xem chứng từ liên kết',
    'qtc': 'Màn Xem chi tiết và Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chứng từ liên kết của dòng'],
        ['Mô tả', 'Màn không có trang chi tiết riêng. Từ mỗi dòng, người dùng mở Phiếu nhập hàng, Phiếu kế toán, Hợp đồng mua ở tab mới; tab danh sách giữ nguyên.'],
        ['Tác nhân', TAC_NHAN],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Bấm mã ở cột Phiếu nhập / Phiếu kế toán / Hợp đồng mua.\n2. Hệ thống mở trang chi tiết chứng từ tương ứng ở tab mới.'],
        ['Dòng sự kiện phụ', '• Màn chứng từ đích tự áp quyền của nó: người dùng không có quyền xem phiếu nhập / phiếu kế toán thì không xem được nội dung.\n• Dòng chưa có phiếu kế toán: ô Phiếu kế toán trống, không có liên kết.'],
    ],
    'menu_them': ' => mã Phiếu nhập / Phiếu kế toán / Hợp đồng mua (liên kết)',
    'anh': [('15_pi_detail', 'Trang chi tiết Phiếu nhập hàng mở từ cột Phiếu nhập'),
            ('16_bill_detail', 'Trang chi tiết Phiếu kế toán mở từ cột Phiếu kế toán')],
    'ui': ui(UI6, [
        ['Liên kết Phiếu nhập', 'Link', 'Enable', 'Mã phiếu nhập', 'Mở chi tiết Phiếu nhập hàng ở tab mới.'],
        ['Liên kết Phiếu kế toán', 'Link', 'Enable / Ẩn', 'Mã phiếu kế toán', 'Mở chi tiết Phiếu kế toán ở tab mới; chưa có phiếu thì không hiện.'],
        ['Liên kết Hợp đồng mua', 'Link', 'Enable', 'Số hợp đồng mua', 'Mở trang xem Hợp đồng mua ở tab mới.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm liên kết', 'Click', 'After:\n– Mở tab mới, màn đích kiểm quyền xem của chứng từ đó.'],
    ],
})

# 2.7 Xuất Excel -----------------------------------------------------------------
FR.append({
    'ten': 'Xuất Excel danh sách', 'uc': 'uc_xuat', 'uc_ten': 'FR-07 Xuất Excel danh sách',
    'qtc': 'Quy tắc Excel và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách cần hạch toán ra Excel'],
        ['Mô tả', 'Xuất mọi dòng khớp bộ lọc + phạm vi (không chỉ trang đang xem) ra file danh_sach_can_hach_toan_chi_phi_van_chuyen_nhanh.xlsx, tiêu đề "DANH SÁCH CẦN HẠCH TOÁN CHI PHÍ VẬN CHUYỂN NHANH" (có lọc Ngày nhập thì thêm "(TỪ NGÀY … ĐẾN NGÀY …)"), đầu file là thông tin công ty người đăng nhập, cuối file có chỗ ký Người lập.'],
        ['Tác nhân', TAC_NHAN],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất Excel", tích sẵn đủ 9 trường.\n3. Người dùng tích / bỏ, kéo ☰ đổi thứ tự, bấm Xuất file.\n4. Hệ thống tải dữ liệu (cạnh nút hiện tiến độ "Đang chuẩn bị dữ liệu…", "Đã tải x/y dòng…"), dựng file và tải về; báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Không có dòng nào khớp → "Không có dữ liệu để xuất", không tải file.\n• Từ 2,000 dòng hàng hoá trở lên → "Dữ liệu quá lớn, vui lòng lọc theo điều kiện cụ thể hơn!", không tải file.\n• Mỗi hàng hoá 1 dòng file; các cột trừ Hàng hóa, Mã hàng gộp ô theo dòng giao nhanh; STT theo dòng giao nhanh.\n• Lỗi khác → "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': POPUP % 'Chọn trường xuất Excel',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất Excel')],
    'ui': ui(UI8, [
        ['Danh sách trường', 'Checkbox', 'Enable', '9 trường', 'Có (≥ 1)', 'Tích cả 9', 'Nhân viên chịu phí, Phiếu nhập, Khách hàng, Hàng hóa, Mã hàng, Chi phí KH, Đã hạch toán, Diễn giải, Người cập nhật. Cột STT luôn có. Kéo ☰ đổi thứ tự cột trong file.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', 'Chọn / bỏ nhanh mọi trường.'],
        ['Dòng đếm', 'Label', 'Read-only', '–', '–', '–', '"Đang chọn x/9 trường".'],
        ['Cột Chi phí KH (file)', 'Text', 'Read-only', '–', '–', '–', 'Dạng "<số> <loại tiền>", vd "21,775 JPY", giữ tối đa 2 chữ số thập phân.'],
        ['Cột Đã hạch toán (file)', 'Text', 'Read-only', '–', '–', '–', '"Đã hạch toán" / "Chưa hạch toán".'],
        ['Nút Xuất file', 'Button', 'Enable', '–', '–', '–', 'Xuất file theo trường đã chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng, không xuất.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất file', 'Click', 'Before:\n– Áp phạm vi dữ liệu (BR-02).\nDuring:\n– Đếm dòng hàng hoá; ≥ 2,000 thì báo và dừng.\nAfter:\n– Dựng file đúng thứ tự cột, gộp ô theo dòng giao nhanh, tải về; báo kết quả.'],
        ['Kéo ☰', 'Drag', 'After:\n– Đổi thứ tự cột trong file.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

FR_NAMES = ['FR-%02d %s' % (i + 1, f['ten']) for i, f in enumerate(FR)]

S = {
    'ten': TEN, 'ten_ngan': 'dòng chi phí vận chuyển nhanh', 'phan_he': 'Tài chính',
    'menu': [('Tài chính', 'menu_phanhe'), ('Hàng hoá - Dịch vụ - Vận chuyển', 'menu_nhom'), ('Nhập hàng', None), (TEN, 'menu_muc')],
    'muc_dich': [
        'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho việc theo dõi và HẠCH TOÁN các khoản chi phí vận chuyển nhanh do khách hàng chịu, khai trên hợp đồng mua, khi hàng đã về kho.',
        'Phạm vi: xem danh sách, tìm kiếm / lọc, tuỳ chỉnh cột, chọn dòng và tạo phiếu kế toán (Nợ 35241 / Có 811), xem chứng từ liên kết, xuất Excel. Màn không có Thêm / Sửa / Xóa / Khóa / Import / Lịch sử riêng: dữ liệu nguồn khai ở hợp đồng mua, trạng thái do phiếu kế toán quyết định.',
        'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình; làm rõ phạm vi dữ liệu theo 4 mức của quyền xem (so với nhân viên chịu phí).',
        'Làm rõ ràng buộc khi lưu phiếu kế toán: chặn dòng đã hạch toán / không còn đủ điều kiện, chặn người thiếu quyền, hai người lập cùng lúc.',
    ],
    'thuat_ngu': [
        ['Dòng giao nhanh', 'Một khoản chi phí vận chuyển nhanh trên hợp đồng mua (tab "Phân bổ chi phí vận chuyển nhanh"): nhân viên chịu phí, khách hàng chịu phí, số tiền, hàng hoá. Mỗi dòng danh sách = 1 tổ hợp Hợp đồng mua × Nhân viên chịu phí × Khách hàng.'],
        ['Nhân viên chịu phí', 'Nhân viên được ghi chịu khoản phí; phạm vi dữ liệu và ô lọc tổ chức tính theo người này.'],
        ['Chi phí KH', 'Chi phí theo khách hàng, tính bằng loại tiền của hợp đồng mua.'],
        ['Phiếu nhập hàng đủ điều kiện', 'Phiếu nhập hàng loại "Nhập hàng mua nước ngoài(mới)", trạng thái Đã hoàn thành, lập từ yêu cầu nhập hàng của hợp đồng mua (phụ lục tính theo hợp đồng cha), có hàng của đúng khách hàng.'],
        ['Hạch toán', 'Lập phiếu kế toán ghi Nợ 35241 (Dự phòng phải trả khác ngắn hạn) / Có 811 (Chi phí khác) cho khoản chi phí.'],
        ['Phiếu kế toán', 'Chứng từ ở Tài chính => Sổ tổng hợp => Phiếu kế toán; trạng thái Đang tạo / Đã duyệt (Hủy chỉ còn ở dữ liệu cũ).'],
        ['HĐ mua', 'Hợp đồng mua hàng (kể cả phụ lục bổ sung).'],
    ],
    'trang_thai': {
        'cau_dan': 'Dòng KHÔNG có trạng thái riêng để chọn: cột Trạng thái hiện theo PHIẾU KẾ TOÁN gắn dòng. Màn này chỉ đọc; '
                   'trạng thái đổi khi kế toán lưu / duyệt / xóa phiếu kế toán.',
        'rows': [
            ['Chưa hạch toán', 'Dòng chưa gắn phiếu kế toán.', 'Xem, lọc, xuất; tick + Tạo phiếu kế toán', 'Người có quyền "%s"' % Q_HT],
            ['Đang tạo', 'Đã gắn phiếu kế toán lưu nháp; ô Hạch toán tích sẵn + khoá.', 'Xem, lọc, xuất, mở phiếu kế toán', 'Tự chuyển khi kế toán bấm Lưu nháp / Lưu và tiếp tục'],
            ['Đã duyệt', 'Phiếu kế toán gắn dòng đã duyệt, bút toán đã ghi sổ cái; có Người duyệt.', 'Xem, lọc, xuất, mở phiếu kế toán', 'Tự chuyển khi kế toán Lưu và duyệt (hoặc duyệt phiếu Đang tạo)'],
            ['Hủy', 'Phiếu kế toán gắn dòng ở trạng thái Hủy (dữ liệu cũ; hệ thống hiện không có thao tác hủy phiếu kế toán). Dòng vẫn khoá.', 'Xem, lọc, xuất', '–'],
        ],
        'anh': 'state_flow',
        'ghi_chu': ['Xóa phiếu kế toán Đang tạo → dòng trở về Chưa hạch toán. Phiếu Đã duyệt không xóa được nên dòng giữ Đã duyệt (BR-07).'],
    },
    'quyen_truoc': ['Menu và màn KHÔNG chặn theo quyền: mọi người dùng mở được màn. Quyền cấp qua Vai trò của công ty đang làm việc.'],
    'quyen_rows': [
        [Q_XEM + ' (mức: Tổng công ty / Công ty / Phòng ban / Bộ phận)', 'Quyết định phạm vi dòng được xem, xuất Excel và các ô lọc Công ty / Phòng ban / Bộ phận / Nhân viên.'],
        [Q_HT, 'Hiện nút "Tạo phiếu kế toán", tick được ô Hạch toán; khi lưu phiếu kế toán hệ thống kiểm lại quyền này. Phụ thuộc quyền "%s".' % Q_XEM],
        [Q_KT + ' (quyền của màn Phiếu kế toán)', 'Bắt buộc để lưu (Lưu nháp / Lưu và duyệt) phiếu kế toán.'],
    ],
    'pham_vi_truoc': ['Phạm vi dữ liệu (xét theo thứ tự, có mức nào trước thì áp mức đó), so với NHÂN VIÊN CHỊU PHÍ của dòng:'],
    'pham_vi_rows': [
        ['1', Q_XEM + ' — mức Tổng công ty', 'Mọi dòng; có ô Công ty, Phòng ban, Bộ phận, Nhân viên.'],
        ['2', Q_XEM + ' — mức Công ty', 'Nhân viên chịu phí cùng công ty người xem; có ô Phòng ban, Bộ phận, Nhân viên.'],
        ['3', Q_XEM + ' — mức Phòng ban', 'Nhân viên chịu phí cùng phòng ban người xem.'],
        ['4', Q_XEM + ' — mức Bộ phận', 'Nhân viên chịu phí cùng bộ phận người xem.'],
        ['5', '(không có quyền xem)', 'Chỉ dòng mà chính người xem là nhân viên chịu phí.'],
    ],
    'pham_vi_sau': ['Người xem chưa gắn công ty / phòng ban / bộ phận tương ứng với mức quyền → không thấy dòng nào. Chọn ô lọc công ty / phòng ban ngoài phạm vi không làm lộ dữ liệu. '
                    'Trang Tạo phiếu kế toán nạp dòng đã chọn với phạm vi "tất cả" (không chặn theo phạm vi xem).'],
    'ma_tran': [['Chức năng', 'Không có quyền', Q_XEM, Q_HT + ' + ' + Q_KT]] + [
        [FR_NAMES[0], 'Có (dòng mình chịu phí)', 'Có (theo mức)', 'Có'],
        [FR_NAMES[1], 'Có (không có ô tổ chức)', 'Có', 'Có'],
        [FR_NAMES[2], 'Có', 'Có', 'Có'],
        [FR_NAMES[3], 'Không (ẩn nút, ô tick khoá)', 'Không', 'Có'],
        [FR_NAMES[4], 'Không', 'Không', 'Có'],
        [FR_NAMES[5], 'Có (màn đích tự kiểm quyền)', 'Có', 'Có'],
        [FR_NAMES[6], 'Có (dòng mình chịu phí)', 'Có (theo mức)', 'Có'],
    ],
    'ma_tran_widths': [2.2, 1.4, 1.4, 1.6],
    'quyen_sau': ['Lưu và duyệt phiếu kế toán chỉ hiện với người có quyền "%s".' % Q_KT],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Điều kiện dòng lên danh sách', ['– Hợp đồng mua (hoặc phụ lục) trạng thái Đã duyệt.', '– Có phiếu nhập hàng loại "Nhập hàng mua nước ngoài(mới)", Đã hoàn thành, lập từ yêu cầu nhập hàng của hợp đồng (phụ lục: của hợp đồng cha), có hàng của đúng khách hàng của dòng.', '– Hiện cả dòng chưa và đã hạch toán.'], ['Xem danh sách', 'Xuất Excel']),
        ('BR-02', 'Phạm vi dữ liệu', ['– Theo mức của quyền "%s", so với nhân viên chịu phí; không có quyền xem: chỉ dòng mình chịu phí.' % Q_XEM, '– Áp như nhau cho danh sách và Excel.'], ['Xem danh sách', 'Tìm kiếm và lọc', 'Xuất Excel']),
        ('BR-03', 'Gom dòng và hàng hoá', ['– 1 dòng = Hợp đồng mua × Nhân viên chịu phí × Khách hàng; phụ lục là dòng riêng.', '– Nhiều phiếu nhập: hiện phiếu lập trước, hàng hoá không lặp.', '– Phân trang theo dòng giao nhanh, 1 dòng không bị tách sang 2 trang.'], ['Xem danh sách', 'Xuất Excel']),
        ('BR-04', 'Lọc Ngày nhập', ['– Theo ngày lập phiếu nhập hàng, tính trọn ngày cuối (đến 23:59:59).'], ['Tìm kiếm và lọc', 'Xuất Excel']),
        ('BR-05', 'Nạp phiếu kế toán', ['– Mỗi dòng giao nhanh = 2 dòng định khoản Nợ 35241 / Có 811, cùng số tiền = Chi phí KH, đối tượng = khách hàng.', '– Loại tiền theo hợp đồng mua của dòng lập trước nhất (không chặn khi các dòng khác loại tiền); VNĐ tỷ giá 1; ngoại tệ lấy tỷ giá danh mục; không có trong danh mục đang dùng thì để trống.', '– Popup Đơn hàng/Hợp đồng của dòng định khoản chỉ ra hợp đồng bán của khách do nhân viên chịu phí lập.'], ['Chọn dòng và tạo phiếu kế toán']),
        ('BR-06', 'Chặn khi lưu phiếu', ['– Thiếu quyền "%s": "Bạn không có quyền thực hiện thao tác này".' % Q_HT, '– Dòng đã hạch toán / đã gắn phiếu / không còn đủ điều kiện (kể cả do người khác vừa lưu): "Trạng thái đã bị thay đổi. Vui lòng load lại trang"; không tạo phiếu.', '– Chỉ kiểm khi TẠO phiếu; sửa phiếu không thêm / bớt dòng.'], ['Lưu phiếu kế toán']),
        ('BR-07', 'Trạng thái theo phiếu kế toán', ['– Lưu phiếu (nháp hoặc duyệt): dòng đánh dấu đã hạch toán + gắn phiếu ngay.', '– Xóa phiếu Đang tạo: dòng về Chưa hạch toán.', '– Dòng gắn phiếu Hủy vẫn khoá, không tạo phiếu mới được.'], ['Lưu phiếu kế toán', 'Xem danh sách']),
        ('BR-08', 'Tick chọn', ['– Tick chỉ trong trang đang xem; đổi trang / lọc thì bỏ tick.', '– Dòng đã hạch toán hoặc thiếu quyền: ô khoá.'], ['Chọn dòng và tạo phiếu kế toán']),
        ('BR-09', 'Xuất Excel', ['– Xuất theo bộ lọc hiện tại, mọi trang; từ 2,000 dòng hàng hoá trở lên thì chặn; không có dữ liệu thì không xuất file.'], ['Xuất Excel']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây dùng hoặc làm thay đổi dữ liệu của Danh sách cần hạch toán chi phí vận chuyển nhanh.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Kế toán',
    'mains': [('FR-01', 'Xem danh sách cần hạch toán', 'view'), ('FR-04', 'Chọn dòng và tạo phiếu kế toán', 'crud'),
              ('FR-05', 'Lưu phiếu kế toán hạch toán', 'action'), ('FR-07', 'Xuất Excel danh sách', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc danh sách', 'view'), ('FR-03', 'Cài đặt bộ lọc, tuỳ chỉnh cột', 'view'),
             ('FR-06', 'Xem chứng từ liên kết', 'view')],
    'rieng': [('FR-04', 'Chọn dòng và tạo phiếu kế toán', 'crud', 'uc_tao'),
              ('FR-05', 'Lưu phiếu kế toán hạch toán', 'action', 'uc_luu'),
              ('FR-06', 'Xem chứng từ liên kết', 'view', 'uc_xem'),
              ('FR-07', 'Xuất Excel danh sách', 'io', 'uc_xuat')],
}

STATES = [('start', '', None), ('chua', 'Chưa hạch toán', '#fef3c7'), ('tao', 'Đang tạo', '#e5e7eb'),
          ('duyet', 'Đã duyệt', '#dcfce7'), ('end', '', None)]
TRANS = [('start', 'chua', 'Đủ điều kiện'), ('chua', 'tao', 'Lưu nháp phiếu KT'), ('tao', 'duyet', 'Duyệt phiếu KT'),
         ('chua', 'duyet', 'Lưu và duyệt'), ('tao', 'chua', 'Xóa phiếu KT'), ('duyet', 'end', 'Hoàn tất')]

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    L.draw_state_flow(os.path.join(scr.uml, 'state_flow.png'), STATES, TRANS)
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))

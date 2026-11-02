# -*- coding: utf-8 -*-
"""SRS - Phiếu nhập kho (STT 178) — chép khuôn màn mẫu finance-declare-debt-beginning/docs/kh/gen_srs.py (đợt 3 phiếu).

Nguồn (code HRM develop, 02/11/2026):
  FE hrm-client/pages/finance/warehouse-imports/** (index, create, _id/{index,edit,arrange,re-export,re-import,barcode},
     components/{WarehouseImportForm, LotEditor, ArrangeDeliveryForm, RecordPickerModal, row-actions, export-excel}),
     components/subsystem-menu/{finance,warehouse}.js
  BE Modules/Finance: Entities/WarehouseImport/WarehouseImport.php, Http/Controllers/V1/WarehouseImportController.php,
     Services/{WarehouseImportService, WarehouseImportWriteService, WarehouseReExportService, WarehouseImportPrintService,
     WarehouseImportBarcodeService, PhysicalStockWriter}.php; Services/ProductImportService::markParentUsed,
     Entities/ProductImport/ProductImport::updateWarehouse (đổi trạng thái PNK khi lập / duyệt Phiếu nhập hàng)
  Ảnh: capture.js (dev-hrm, dữ liệu thật — không ảnh giả lập). Phần 5: dò code FE/BE 02/11/2026.
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402
from _lib_phieu import ui, UI4, UI4W, UI6, UI6W, UI7, UI7W, UI8, UI8W, TRUOC_LUU  # noqa: E402

TEN = 'Phiếu nhập kho'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
TK = 'Thủ kho của kho nhập (khai ở danh mục kho)'
KTK = 'Kế toán kho (quyền "Kế toán kho")'
Q_ALL = 'Người dùng đăng nhập hệ thống (màn không yêu cầu quyền riêng để vào)'
DK = '1. Người dùng đăng nhập thành công.\n2. Phiếu thuộc phạm vi dữ liệu của người dùng (Phần 2).'
HOAC = 'Hoặc Menu: Phân hệ Kho => Nhập kho => Phiếu nhập kho (cùng màn hình).'
TRANG = 'Trang %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'
POPUP = 'Modal %s được mở ngay trên màn hình %s theo đường dẫn ở trên.'
LS = 'Ghi nhận %s trong lịch sử của phiếu.'

# ------------------------------------------------------------------ Phần 5 (dò code 02/11/2026)
P5 = [
    ('Tài chính', 'Đề nghị nhập kho (nguồn tạo phiếu; tạo phiếu nhập kho = duyệt đề nghị, Lưu và nhập → Đã nhập kho, Hủy phiếu → hủy đề nghị)',
     'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng => Đề nghị nhập kho; Kho => Nhập kho => Phiếu đề nghị nhập kho'),
    ('Tài chính', 'Yêu cầu nhập hàng (trạng thái đổi theo: Đang nhập kho khi tạo phiếu, Đã nhập kho khi Lưu và nhập)',
     'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng => Yêu cầu nhập hàng'),
    ('Tài chính', 'Phiếu nhập hàng (lập từ phiếu Chờ duyệt; lập phiếu → phiếu nhập kho Đang hạch toán, duyệt → Đã hạch toán)',
     'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng => Phiếu nhập hàng'),
    ('Kho', 'Phiếu xuất điều chỉnh sai số liệu (phiếu xuất lại sinh từ phiếu nhập kho Không duyệt)',
     'Kho => Xuất kho => Phiếu xuất điều chỉnh sai số liệu'),
    ('Kho', 'Phiếu nhập kho chờ báo thừa, thiếu (đọc phiếu nhập kho Đã hạch toán)', 'Kho => Nhập kho => Phiếu nhập kho chờ báo thừa, thiếu'),
    ('Kho', 'Phiếu báo hàng thừa, thiếu nhập kho (lập từ phiếu nhập kho Đã hạch toán)', 'Kho => Nhập kho => Phiếu báo hàng thừa, thiếu nhập kho'),
    ('Kho / Tra cứu', 'Các màn tồn kho theo kho / vị trí / lô (tồn do Lưu và nhập cộng, Xuất lại trừ)',
     'Kho => Báo cáo kho; Thông báo => Tra cứu tồn kho => Hàng có thể bán theo công ty'),
    ('Vận chuyển', 'Chuyến xe chở hàng (chuyến gắn vào phiếu khi vận chuyển = Công ty vận chuyển)',
     'Vận chuyển => Chuyến xe => Chuyến xe chở hàng'),
    ('Vận chuyển', 'Báo cáo cẩu hàng bốc xếp (bốc xếp khai trên phiếu)', 'Vận chuyển => Báo cáo bốc xếp'),
    ('Vận chuyển', 'Báo cáo chi tiết chi phí vận chuyển theo lái xe (chuyến xe của phiếu nhập kho)',
     'Vận chuyển => Báo cáo vận chuyển => Báo cáo chi tiết chi phí vận chuyển theo lái xe'),
    ('Tài chính', 'Đề nghị thanh toán (chứng từ nguồn của nhà cung cấp gồm phiếu nhập kho có bút toán phải trả)',
     'Tài chính => Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi => Đề nghị thanh toán'),
]

FR = []

# 2.1 Xem danh sách -------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách phiếu nhập kho',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách phiếu nhập kho'],
        ['Mô tả', 'Hiển thị các phiếu nhập kho trong phạm vi dữ liệu của người dùng (một mục menu cho mọi vai trò: thủ kho, kế toán kho, người theo dõi), có phân trang, sắp xếp, trạng thái, tiến trình và nút thao tác theo từng dòng.'],
        ['Tác nhân', Q_ALL],
        ['Điều kiện ban đầu', '1. Người dùng đăng nhập thành công.'],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), phiếu tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Không có phiếu khớp → bảng hiện "Không có dữ liệu phù hợp."\n• Phạm vi dữ liệu theo quyền xem (Phần 2, BR-02); phiếu Đang tạo của người khác không hiện.\n• Nút trên dòng hiện theo trạng thái phiếu và vai trò người dùng (BR-03); nút không dùng được thì ẩn.'],
    ],
    'hoac_menu': [HOAC],
    'anh': [('01_list', 'Màn danh sách Phiếu nhập kho lúc mới truy cập'),
            ('01b_list_actions', 'Cuộn bảng sang phải: cột Trạng thái, Tiến trình, Người duyệt, Ngày nhận, Ngày duyệt, Hành động'),
            ('03b_row_menu', 'Phiếu Đang tạo – Đang đi xếp hàng: 2 nút ngoài (Nhập kho, Hủy) và menu "Hành động khác"')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Danh sách phiếu nhập kho', 'Tiêu đề khối danh sách và tiêu đề trang.'],
        ['Nút Tạo mới', 'Button', 'Enable', 'Hiển thị', 'Mở trang "Dự kiến vị trí" để tạo phiếu từ đề nghị nhập kho (mục 2.4).'],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất Excel" (mục 2.16).'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.3).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khoá.'],
        ['Cột Mã phiếu', 'Table/Grid', 'Read-only', 'Hiển thị', '- Dạng PNK-<5 chữ số>. Sắp xếp được, cột dính khi cuộn ngang.\n- Liên kết mở trang Chi tiết (mục 2.8).\n- Phiếu nhập lại ghi thêm dòng nghiêng "Nhập lại cho phiếu <mã phiếu gốc>" (liên kết).'],
        ['Cột Loại', 'Table/Grid', 'Read-only', 'Hiển thị', 'Loại nhập theo đề nghị nhập kho (vd Nhập hàng mua trong nước (TỰ DO + HÃNG), Nhập điều chuyển kho chi nhánh, Nhập hàng khác…). Sắp xếp được.'],
        ['Cột Nhà cung cấp', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên nhà cung cấp của phiếu (nếu có). Sắp xếp được.'],
        ['Cột Kho nhập', 'Table/Grid', 'Read-only', 'Hiển thị', 'Kho nhận hàng. Sắp xếp được.'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Phiếu ĐNNK', 'Table/Grid', 'Read-only', 'Hiển thị', 'Mã đề nghị nhập kho nguồn, liên kết mở màn Đề nghị nhập kho.'],
        ['Cột Người đề nghị', 'Table/Grid', 'Read-only', 'Hiển thị', '"Họ tên - Mã phòng ban" người lập đề nghị nhập kho (phiếu nhập ghép: người lập phiếu xuất ghép).'],
        ['Cột Người yêu cầu', 'Table/Grid', 'Read-only', 'Hiển thị', 'Người lập yêu cầu nhập hàng (loại điều chuyển kho chi nhánh: người lập yêu cầu xuất hàng).'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', '"Họ tên - Mã phòng ban" thủ kho tạo phiếu.'],
        ['Cột Trạng thái', 'Table/Grid', 'Read-only', 'Hiển thị', 'Nhãn màu: Đang tạo (xám), Chờ duyệt (cam), Đang hạch toán, Đã hạch toán, Không duyệt (đỏ), Đã xuất lại, Đã nhập lại, Đã hủy. Không sắp xếp.'],
        ['Cột Tiến trình', 'Table/Grid', 'Read-only', 'Hiển thị', 'Đang đi xếp hàng / Đang nhập kho / Hoàn thành nhập kho (BR-01).'],
        ['Cột Người duyệt', 'Table/Grid', 'Read-only', 'Hiển thị', 'Kế toán kho lập phiếu nhập hàng cho phiếu.'],
        ['Cột Ngày nhận', 'Table/Grid', 'Read-only', 'Hiển thị', 'Thời điểm thủ kho bấm "Lưu và nhập" (phiếu chuyển Chờ duyệt). Sắp xếp được.'],
        ['Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'Hiển thị', 'Thời điểm lập phiếu nhập hàng. Sắp xếp được.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- Theo trạng thái và vai trò (Phần 1 mục 3, BR-03): Nhập kho / Sửa phiếu, Hủy, Phiếu xếp hàng, Tạo phiếu nhập hàng, Không duyệt, Tạo phiếu xuất lại, Tạo phiếu nhập lại, In phiếu, In barcode, Xem lịch sử.\n- Quá 3 nút: 2 nút đầu hiện ngoài, còn lại trong menu "Hành động khác". Cột khoá.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Không kiểm quyền riêng; phạm vi dữ liệu theo Phần 2.\nAfter:\n– Tải trang 1, phiếu tạo gần nhất trên cùng; khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút).'],
        ['Bấm tiêu đề cột sắp xếp được', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại dữ liệu (thứ tự phụ theo phiếu mới nhất, không nhảy dòng khi đổi trang).'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và sắp xếp; đổi số dòng thì về trang 1.'],
        ['Bấm Mã phiếu / Phiếu ĐNNK', 'Click', 'After:\n– Mở trang Chi tiết phiếu nhập kho / màn Đề nghị nhập kho.'],
        ['Bấm nút trên dòng', 'Click', 'After:\n– Mở đúng chức năng (mục 2.4 – 2.17).'],
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc danh sách',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách phiếu nhập kho'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh theo mã phiếu và 13 ô lọc ở khu vực Tìm kiếm nâng cao.'],
        ['Tác nhân', Q_ALL],
        ['Điều kiện ban đầu', '1. Người dùng đăng nhập thành công.\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Nhập mã phiếu rồi bấm Tìm kiếm / Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện, tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô gõ chữ (tìm nhanh, Hàng hoá, Mã phiếu, Phiếu ĐNNK) chỉ lọc khi bấm Tìm kiếm / Enter; ô chọn lọc ngay khi chọn.\n• Làm mới → xoá mọi điều kiện.\n• Ô Công ty / Phòng ban chỉ hiện theo quyền xem (BR-02).\n• Các danh sách chọn (Nhà cung cấp, Người đề nghị, Người yêu cầu, Người tạo, Người duyệt) chỉ gồm giá trị có trong phiếu thuộc phạm vi xem.\n• Ghi nhớ bộ lọc 10 phút khi rời màn rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực Tìm kiếm nâng cao ở trạng thái mở')],
    'ui': ui(UI7, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Tìm theo Mã phiếu"; tìm gần đúng theo mã phiếu.'],
        ['Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Áp dụng / xoá mọi điều kiện lọc.'],
        ['Nút Tìm kiếm nâng cao / Cài đặt bộ lọc', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực ô lọc; mở cửa sổ Cài đặt bộ lọc (mục 2.3).'],
        ['Ô Công ty – Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Theo quyền xem', 'Trống', 'Công ty: quyền theo tổng công ty; Phòng ban: chọn công ty trước. Lọc theo tổ chức của phiếu (chép từ đề nghị nhập kho).'],
        ['Ô Kho nhập', 'Dropdown', 'Enable', 'Danh mục kho', 'Trống', 'Lọc theo kho nhập.'],
        ['Ô Hàng hoá', 'Textbox', 'Enable', 'Tên, mã hàng hoá', 'Trống', 'Tìm gần đúng trong dòng hàng của đề nghị nhập kho nguồn hoặc lô thực nhập.'],
        ['Ô Mã phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Tìm gần đúng mã phiếu.'],
        ['Ô Loại', 'Dropdown', 'Enable', '17 loại nhập', 'Trống', 'Lọc theo loại phiếu.'],
        ['Ô Nhà cung cấp', 'Dropdown', 'Enable', 'Nhà cung cấp có trong phiếu', 'Trống', '"Mã - Tên".'],
        ['Ô Phiếu ĐNNK', 'Textbox', 'Enable', 'Mã đề nghị', 'Trống', 'Tìm gần đúng mã đề nghị nhập kho nguồn.'],
        ['Ô Người đề nghị / Người yêu cầu', 'Dropdown', 'Enable', 'Nhân viên', 'Trống', 'Theo người lập đề nghị nhập kho / yêu cầu nhập hàng (như cột cùng tên).'],
        ['Ô Người tạo / Người duyệt', 'Dropdown', 'Enable', 'Nhân viên', 'Trống', 'Theo người tạo phiếu / người duyệt.'],
        ['Ô Trạng thái', 'Dropdown', 'Enable', '8 trạng thái', 'Trống', 'Đang tạo, Chờ duyệt, Đang hạch toán, Đã hạch toán, Không duyệt, Đã xuất lại, Đã nhập lại, Đã hủy. Kế toán kho chọn "Chờ duyệt" để xem phiếu cần xử lý.'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy, Từ → Đến', 'Trống', 'Lọc theo ngày tạo phiếu, tính cả 2 đầu mút.'],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm Tìm kiếm / nhấn Enter ở ô gõ chữ', 'Click', 'After:\n– Áp đồng thời mọi điều kiện, tải lại bảng từ trang 1.'],
        ['Chọn giá trị ở ô chọn', 'Change', 'After:\n– Tải lại bảng từ trang 1 ngay.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khu vực ô lọc; lần mở đầu tải danh sách giá trị cho các ô chọn.'],
    ],
})

# 2.3 Cài đặt bộ lọc / tùy chỉnh cột --------------------------------------------
FR.append({
    'ten': 'Cài đặt bộ lọc và tuỳ chỉnh cột',
    'qtc': 'Bộ lọc, Cấu hình cột và lưu cấu hình theo người dùng.',
    'gioi_thieu': [
        ['Tên chức năng', 'Cài đặt bộ lọc và tuỳ chỉnh cột'],
        ['Mô tả', 'Chọn ô lọc / cột hiển thị và thứ tự. Cấu hình lưu theo từng người dùng, từng màn.'],
        ['Tác nhân', Q_ALL],
        ['Điều kiện ban đầu', '1. Người dùng đăng nhập thành công.\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Bấm "Cài đặt bộ lọc" (hoặc biểu tượng Cấu hình cột hiển thị).\n2. Tích / bỏ tích, kéo ☰ để đổi thứ tự.\n3. Bấm Lưu: hệ thống lưu và áp dụng ngay.'],
        ['Dòng sự kiện phụ', '• Đóng: bỏ thay đổi.\n• Cài đặt bộ lọc có "Khôi phục mặc định".\n• Cột STT, Hành động không bỏ được.'],
    ],
    'menu_them': ' => Cài đặt bộ lọc {icon:btn_caidatboloc} / Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': 'Modal Cài đặt bộ lọc và Modal Tuỳ chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('26_filtercfg', 'Cửa sổ Cài đặt bộ lọc'), ('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột')],
    'ui': ui(UI6, [
        ['Danh sách ô lọc', 'Checkbox', 'Enable', 'Đủ 13 ô', 'Công ty – Phòng ban, Kho nhập, Hàng hoá, Mã phiếu, Loại, Nhà cung cấp, Phiếu ĐNNK, Người đề nghị, Người yêu cầu, Người tạo, Trạng thái, Người duyệt, Ngày tạo.'],
        ['Nút Khôi phục mặc định', 'Button', 'Enable', '–', 'Đưa cấu hình ô lọc về mặc định.'],
        ['Danh sách cột', 'Checkbox', 'Enable', '16/16 cột', 'Tích cột muốn hiện; kéo ☰ đổi thứ tự; dòng đếm "Đang chọn x/16 cột".'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Chọn / bỏ nhanh mọi cột (trừ cột khoá).'],
        ['Nút Lưu / Đóng', 'Button', 'Enable', '–', 'Lưu cấu hình và áp dụng / đóng không lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình theo người dùng, đóng cửa sổ, vẽ lại bảng / khu vực lọc.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ, không lưu.'],
    ],
})

# 2.4 Tạo phiếu (dự kiến vị trí) --------------------------------------------------
FR.append({
    'ten': 'Tạo phiếu nhập kho (dự kiến vị trí)', 'uc': 'uc_them', 'uc_ten': 'FR-04 Tạo phiếu nhập kho từ đề nghị nhập kho',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tạo phiếu nhập kho từ đề nghị nhập kho'],
        ['Mô tả', 'Thủ kho chọn 1 đề nghị nhập kho Chờ duyệt của kho mình, nhập người giao hàng, vị trí DỰ KIẾN và số lượng cho từng dòng hàng, thông tin vận chuyển, bốc xếp. Lưu xong phiếu ở trạng thái Đang tạo – Đang đi xếp hàng; đề nghị nhập kho được duyệt (chuyển Đang nhập kho). Chưa ghi tồn kho.'],
        ['Tác nhân', TK + '; Super admin'],
        ['Điều kiện ban đầu', '1. Người dùng đăng nhập thành công.\n2. Người dùng là thủ kho của kho nhập của đề nghị (Super admin: mọi kho).\n3. Đề nghị nhập kho ở trạng thái Chờ duyệt.'],
        ['Dòng sự kiện chính', '1. Bấm Tạo mới (hoặc nút "Tạo phiếu nhập kho" ở màn Đề nghị nhập kho — mở sẵn đề nghị đó).\n2. Hệ thống mở trang "Dự kiến vị trí"; góc phải tiêu đề khối hiện "<Người đăng nhập> - <ngày giờ>".\n3. Người dùng chọn Phiếu đề nghị nhập kho (mục 2.5); hệ thống điền Loại (tiêu đề khối), Kho nhập, Người đề nghị, Ghi chú (theo đề nghị) và bảng hàng hoá (SL nhập mặc định = SL đề nghị).\n4. Nhập Người giao hàng; mỗi dòng hàng chọn Vị trí (mục 2.5) và SL nhập, có thể "Thêm vị trí" để chia 1 dòng hàng ra nhiều vị trí.\n5. Tab Vận chuyển (loại có vận chuyển), tab Bốc xếp: nhập nếu có.\n6. Bấm Lưu.\n7. Hệ thống kiểm tra, sinh mã PNK-<5 chữ số>, ghi dòng hàng dự kiến, bốc xếp, chuyến xe; duyệt đề nghị nhập kho (BR-05), gửi thông báo cho người lập đề nghị và người lập yêu cầu nhập hàng.\n8. ' + LS % 'Tạo mới' + '\n9. Báo "Phiếu đã được lưu. Hãy tạo phiếu đi xếp hàng", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• "Lưu và tiếp tục": lưu như trên rồi mở form trống để tạo tiếp.\n• Phiếu chưa có hàng nào SL > 0 → "Phiếu phải có ít nhất 1 hàng hoá có số lượng thực nhập lớn hơn 0" (chặn ngay, không gửi).\n• Sai dữ liệu → báo đỏ dưới ô, toast lỗi đầu tiên, cuộn tới ô lỗi; tab có lỗi tô đỏ.\n• Hàng / vị trí đang kiểm kho → "Hàng <tên> đang kiểm kho!" / "Vị trí <mã> đang kiểm kho" (BR-09).\n• Người dùng không phải thủ kho kho đề nghị / đề nghị không còn Chờ duyệt → "Chỉ thủ kho của kho nhập mới tạo được phiếu nhập kho từ đề nghị đang chờ duyệt."\n• Quay lại khi đã nhập → hộp "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', 'Nút Lưu bị khoá khi đang lưu, tránh lưu 2 lần.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': TRANG % '"Dự kiến vị trí"',
    'anh': [('10_create', 'Trang Dự kiến vị trí lúc mới mở'),
            ('11_validate', 'Bấm Lưu khi chưa chọn đề nghị: báo phiếu phải có ít nhất 1 hàng SL > 0'),
            ('10b_create_filled', 'Đã chọn đề nghị nhập kho, nhập Người giao hàng và vị trí dự kiến'),
            ('10c_create_vanchuyen', 'Tab Vận chuyển khi chọn "Công ty vận chuyển"'),
            ('10d_create_bocxep', 'Tab Bốc xếp khi Loại hình thuê = Công ty (có bảng người nhận việc)'),
            ('18_unsaved', 'Hộp Thông tin chưa lưu khi bấm Quay lại')],
    'ui': ui(UI8, [
        ['Tiêu đề khối + người tạo', 'Label', 'Read-only', '–', '–', 'Tên loại phiếu; Người đăng nhập - giờ hiện tại', 'Tiêu đề khối = loại phiếu theo đề nghị.'],
        ['Phiếu đề nghị nhập kho', 'Picker', 'Enable', 'Đề nghị Chờ duyệt của kho mình là thủ kho', 'Có', 'Trống', 'Bấm ô mở cửa sổ chọn (mục 2.5); nút × bỏ chọn (xoá bảng hàng).'],
        ['Người giao hàng', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', 'Bỏ trống: "Bắt buộc phải nhập"; quá dài: "Không được vượt quá 255 ký tự".'],
        ['Kho nhập, Người đề nghị', 'Textbox', 'Read-only', '–', '–', 'Theo đề nghị', 'Có biểu tượng ⓘ giải thích nguồn dữ liệu.'],
        ['Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Ghi chú của đề nghị', 'Quá 255 ký tự: "Không được vượt quá 255 ký tự".'],
        ['Tab Vận chuyển – Vận chuyển', 'Dropdown', 'Enable', 'Nhân viên vận chuyển / Công ty vận chuyển / Khách hàng vận chuyển', 'Có', 'Nhân viên vận chuyển', 'Chỉ có với loại có vận chuyển.'],
        ['Tab Vận chuyển – Chuyến xe', 'Dropdown', 'Enable', 'Chuyến xe chở hàng chưa chốt', 'Có khi Công ty vận chuyển', 'Trống', '- "Thêm chuyến" thêm dòng; "Tạo chuyến xe" mở popup tạo nhanh chuyến xe chở hàng rồi chọn luôn.\n- Bỏ trống: "Bắt buộc phải chọn chuyến xe"; trùng: "Không được chọn trùng".'],
        ['Tab Bốc xếp – Cách tính', 'Checkbox', 'Enable', 'Tính theo khối lượng / Tính theo thời gian', 'Không', 'Theo khối lượng', 'Đổi nhãn ô Khối lượng hàng (Tấn) / Số giờ.'],
        ['Tab Bốc xếp – Loại hình thuê', 'Dropdown', 'Enable', 'Công ty / Thuê ngoài', 'Không', 'Trống', 'Chọn thì Loại bốc xếp, Khối lượng / Số giờ bắt buộc; Thuê ngoài thì Nhà cung cấp bắt buộc; Công ty thì có bảng người nhận việc.'],
        ['Tab Bốc xếp – Đơn giá, Số tiền, VAT, Số tiền sau VAT', 'Textbox', 'Read-only / Enable', 'Số ≥ 0', 'Không', '0', 'Đơn giá tự tính theo loại bốc xếp × loại hình thuê × cách tính; Số tiền = Đơn giá × khối lượng / số giờ; VAT nhập tay.'],
        ['Bảng người nhận việc', 'Table/Grid', 'Enable', 'Nhân viên + Số tiền > 0', 'Có khi Loại hình thuê = Công ty', 'Trống', 'Tổng tiền chia phải bằng Số tiền bốc xếp: "Tổng số tiền chia cho các nhân viên phải bằng tổng số tiền bốc xếp".'],
        ['Bảng Hàng hoá', 'Table/Grid', 'Read-only', '–', 'Có', 'Theo đề nghị', 'Tên hàng hoá, Model, Mã hàng hoá, Thương hiệu, ĐVT, SL đề nghị, SL thực nhập (tổng các vị trí); loại "Nhập hàng khác" có thêm cột Ghi chú dòng hàng.'],
        ['Vị trí (dự kiến)', 'Picker', 'Enable', 'Vị trí của kho nhập, không đang kiểm kho', 'Có', 'Trống', '- Bỏ trống: "Bắt buộc phải chọn vị trí"; cùng hàng chọn trùng vị trí: "Vị trí đã được chọn cho hàng này".\n- Tích "Áp dụng tất cả" (chỉ màn tạo): vị trí dòng đầu áp cho mọi dòng.'],
        ['Tồn', 'Label', 'Read-only', '–', '–', 'Tồn hiện tại', 'Tồn của hàng tại vị trí, theo ĐVT của dòng.'],
        ['SL nhập', 'Textbox', 'Enable', 'Số ≥ 0, ≤ 999,999', 'Có', 'SL đề nghị', '- Trống khi đã chọn vị trí: "Bắt buộc phải nhập"; > 999,999: "Không được lớn hơn 999,999".\n- Tổng các vị trí vượt SL đề nghị: ô đỏ, "Vượt SL đề nghị (<SL>)". Loại điều chuyển kho chi nhánh: tổng phải bằng SL đề nghị.'],
        ['Thêm vị trí / xoá dòng vị trí', 'Button', 'Enable', '–', '–', '–', 'Thêm / bỏ dòng vị trí của 1 dòng hàng.'],
        ['Nút Lưu / Lưu và tiếp tục / Quay lại', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi về danh sách / lưu rồi mở form trống / về danh sách (đã nhập thì hỏi "Thông tin chưa lưu").'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'After:\n– Mở trang "Dự kiến vị trí" trống (có mã đề nghị trên đường dẫn thì nạp sẵn đề nghị đó).'],
        ['Chọn đề nghị nhập kho', 'Change', 'After:\n– Nạp thông tin + dòng hàng của đề nghị; ghi chú lấy theo ghi chú đề nghị.'],
        ['Bấm Lưu / Lưu và tiếp tục', 'Click', 'Before:\n– Người dùng là thủ kho của kho đề nghị (Super admin bỏ qua); đề nghị đang Chờ duyệt.\nDuring:\n– Người giao hàng ≤ 255; có ≥ 1 dòng hàng, mỗi dòng ≥ 1 vị trí có SL; vị trí không trùng trong cùng dòng hàng; tổng SL không vượt SL đề nghị; tổng phiếu > 0; hàng / vị trí không đang kiểm kho; luật bốc xếp, chuyến xe.\n' + TRUOC_LUU + '\nAfter:\n– Sinh mã PNK, trạng thái Đang tạo, tiến trình Đang đi xếp hàng; ghi dòng hàng dự kiến, bốc xếp, chuyến xe; tổ chức phiếu chép từ đề nghị.\n– Đề nghị nhập kho → Đang nhập kho, yêu cầu nhập hàng → Đang nhập kho; thông báo người lập.\n– ' + LS % 'Tạo mới' + '\n– Báo "Phiếu đã được lưu. Hãy tạo phiếu đi xếp hàng".'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa nhập gì → về danh sách; đã nhập → hộp "Thông tin chưa lưu" ("Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?").'],
    ],
})

# 2.5 Chọn đề nghị / chọn vị trí --------------------------------------------------
FR.append({
    'ten': 'Chọn đề nghị nhập kho và vị trí kho', 'uc': 'uc_chon', 'uc_ten': 'FR-05 Chọn đề nghị nhập kho và vị trí kho',
    'qtc': 'Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chọn đề nghị nhập kho / Chọn vị trí kho'],
        ['Mô tả', 'Hai cửa sổ chọn trên form: "Chọn phiếu đề nghị nhập kho" (đề nghị Chờ duyệt của kho mình là thủ kho) và "Chọn vị trí kho" (vị trí của kho nhập, kèm tồn hiện tại của hàng). Bấm vào dòng là chọn và đóng cửa sổ.'],
        ['Tác nhân', TK],
        ['Điều kiện ban đầu', '1. Đang ở trang Dự kiến vị trí / Nhập kho.\n2. Chọn vị trí: đã có đề nghị (biết kho nhập).'],
        ['Dòng sự kiện chính', '1. Bấm ô Phiếu đề nghị nhập kho (hoặc ô Vị trí của 1 dòng).\n2. Hệ thống mở cửa sổ, tải trang 1.\n3. Lọc theo Mã phiếu / Vị trí nếu cần, bấm vào dòng.\n4. Hệ thống điền giá trị vào form, đóng cửa sổ.'],
        ['Dòng sự kiện phụ', '• Không có đề nghị: "Không có đề nghị nhập kho chờ duyệt ở kho bạn phụ trách."\n• Vị trí đang kiểm kho: dòng mờ, ghi "Đang kiểm kho", không chọn được.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi} => Phiếu đề nghị nhập kho {icon:o_chondnnk}',
    'ghi_chu_layout': POPUP % ('Chọn phiếu đề nghị nhập kho / Chọn vị trí kho', 'Dự kiến vị trí'),
    'anh': [('14_picker', 'Cửa sổ Chọn phiếu đề nghị nhập kho'), ('14c_position', 'Cửa sổ Chọn vị trí kho')],
    'ui': ui(UI6, [
        ['Ô Mã phiếu / Vị trí', 'Textbox', 'Enable', 'Trống', 'Tìm gần đúng; nút Tìm kiếm, Làm mới.'],
        ['Bảng đề nghị', 'Table/Grid', 'Read-only', '10 dòng/trang', 'STT, Mã phiếu (sắp xếp được), Loại, Kho, Người tạo, Ngày tạo (sắp xếp được).'],
        ['Bảng vị trí', 'Table/Grid', 'Read-only', '10 dòng/trang', 'STT, Vị trí, Nhà, Dãy, Khoang, Tồn (của hàng tại vị trí).'],
        ['Nút Đóng / (x)', 'Button', 'Enable', '–', 'Đóng, không chọn.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở cửa sổ', 'System', 'After:\n– Đề nghị: chỉ Chờ duyệt, kho mình là thủ kho (Super admin: mọi kho). Vị trí: vị trí hoạt động của kho nhập, đánh dấu vị trí đang kiểm kho.'],
        ['Bấm vào dòng', 'Click', 'During:\n– Dòng bị khoá (đang kiểm kho): bỏ qua.\nAfter:\n– Điền vào form, đóng cửa sổ.'],
        ['Bấm Tìm kiếm / Làm mới / Đóng', 'Click', 'After:\n– Lọc lại từ trang 1 / xoá lọc / đóng cửa sổ.'],
    ],
})

# 2.6 Phiếu đi xếp hàng ---------------------------------------------------------
FR.append({
    'ten': 'Lập phiếu đi xếp hàng', 'uc': 'uc_xephang', 'uc_ten': 'FR-06 Lập phiếu đi xếp hàng',
    'qtc': 'Màn Thêm mới, Thông báo và Quy tắc màn In.',
    'gioi_thieu': [
        ['Tên chức năng', 'Lập phiếu đi xếp hàng'],
        ['Mô tả', 'Chia các dòng vị trí dự kiến thành nhiều phiếu xếp hàng (kéo – thả), mỗi phiếu chọn 1 người đi xếp là thủ kho của kho nhập; in từng phiếu xếp hàng. Xếp xong mọi dòng mới được nhập kho.'],
        ['Tác nhân', TK],
        ['Điều kiện ban đầu', '1. Người dùng đăng nhập thành công.\n2. Phiếu Đang tạo, tiến trình Đang đi xếp hàng.'],
        ['Dòng sự kiện chính', '1. Bấm "Phiếu xếp hàng" ở dòng danh sách / trang Chi tiết.\n2. Hệ thống mở trang "Phiếu đi xếp hàng: <mã>": khối thông tin chung (chỉ đọc) + khối "Các phiếu xếp hàng".\n3. Kéo dòng hàng giữa các phiếu, "Thêm phiếu xếp hàng" để thêm nhóm; mỗi phiếu chọn người đi xếp.\n4. Bấm "Lưu phiếu xếp hàng": hệ thống ghi nhóm + người đi xếp cho từng dòng, báo "Đã lưu phiếu xếp hàng".\n5. Bấm "In" ở 1 phiếu để xem trước bản in phiếu xếp hàng; bấm "Nhập kho" để sang bước nhập kho.'],
        ['Dòng sự kiện phụ', '• Phiếu có dòng mà chưa chọn người đi xếp → "Bắt buộc phải chọn người đi xếp".\n• Người đi xếp không phải thủ kho kho nhập → "Người đi xếp phải là thủ kho của kho nhập".\n• "In" và "Nhập kho" tự lưu nhóm trước; còn dòng chưa có người đi xếp thì "Nhập kho" báo "Còn dòng hàng chưa có người đi xếp — chọn người đi xếp cho mọi phiếu." và ở lại.\n• Phiếu không còn ở bước xếp hàng → "Phiếu không còn ở bước xếp hàng."'],
    ],
    'menu_them': ' => Phiếu xếp hàng {icon:btn_xephang}',
    'ghi_chu_layout': TRANG % '"Phiếu đi xếp hàng"',
    'anh': [('30_arrange', 'Trang Phiếu đi xếp hàng')],
    'ui': ui(UI8, [
        ['Thông tin chung', 'Textbox', 'Read-only', '–', '–', 'Theo phiếu', 'Phiếu đề nghị nhập kho (liên kết), Người giao hàng, Kho nhập, Người đề nghị, Ghi chú.'],
        ['Phiếu <n>', 'Panel', 'Enable', '≥ 1 phiếu', '–', 'Theo nhóm đã lưu (chưa có: 1 phiếu chứa mọi dòng)', 'Danh sách dòng: tên hàng, mã hàng, vị trí, SL + ĐVT; kéo thả sang phiếu khác.'],
        ['Người đi xếp', 'Dropdown', 'Enable', 'Thủ kho của kho nhập', 'Có khi phiếu có dòng', 'Trống', '"Họ tên - Mã phòng ban - Mã nhân viên".'],
        ['Nút In (từng phiếu)', 'Button', 'Enable / Ẩn', '–', '–', '–', 'Chỉ hiện khi phiếu có dòng và đã chọn người đi xếp; lưu nhóm rồi mở xem trước bản in phiếu xếp hàng.'],
        ['Nút Bỏ phiếu trống', 'Button', 'Enable / Ẩn', '–', '–', '–', 'Chỉ hiện ở phiếu không còn dòng (còn ≥ 2 phiếu).'],
        ['Thêm phiếu xếp hàng', 'Button', 'Enable', '–', '–', '–', 'Thêm 1 phiếu trống.'],
        ['Nút Lưu phiếu xếp hàng / Nhập kho / Quay lại', 'Button', 'Enable', '–', '–', '–', 'Lưu nhóm / lưu rồi sang trang Nhập kho (chỉ người được nhập kho) / về danh sách.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Mở trang', 'System', 'Before:\n– Phiếu Đang tạo – Đang đi xếp hàng; không đúng → "Phiếu không ở bước xếp hàng hoặc bạn không có quyền." và về danh sách.\nAfter:\n– Gom dòng theo nhóm đã lưu.'],
        ['Bấm Lưu phiếu xếp hàng', 'Click', 'During:\n– Mỗi phiếu có dòng phải có người đi xếp là thủ kho kho nhập; mỗi dòng chỉ thuộc 1 phiếu.\n' + TRUOC_LUU + '\nAfter:\n– Ghi số phiếu + người đi xếp vào từng dòng vị trí dự kiến; báo "Đã lưu phiếu xếp hàng".'],
        ['Bấm In', 'Click', 'After:\n– Lưu nhóm (không báo), mở "Xem trước phiếu xếp hàng <n> — <mã>".'],
        ['Bấm Nhập kho', 'Click', 'After:\n– Lưu nhóm; xếp đủ thì mở trang Nhập kho (mục 2.7).'],
    ],
})

# 2.7 Nhập kho / Sửa ------------------------------------------------------------
FR.append({
    'ten': 'Nhập kho và sửa phiếu (Lưu, Lưu và nhập)', 'uc': 'uc_nhapkho', 'uc_ten': 'FR-07 Nhập kho (Lưu và nhập)',
    'qtc': 'Màn Sửa, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Nhập kho / Sửa phiếu nhập kho'],
        ['Mô tả', 'Thủ kho nhập SL và vị trí THỰC, file đính kèm (bắt buộc), vận chuyển (tuyến đường, số km chốt), bốc xếp. "Lưu" giữ phiếu Đang tạo – Đang nhập kho; "Lưu và nhập" = gửi phiếu: GHI TỒN KHO theo vị trí / lô và chuyển Chờ duyệt cho kế toán kho.'],
        ['Tác nhân', 'Người tạo phiếu; Super admin'],
        ['Điều kiện ban đầu', '1. Người dùng đăng nhập thành công.\n2. Phiếu Đang tạo (Đang đi xếp hàng hoặc Đang nhập kho) và người dùng là người tạo phiếu (hoặc Super admin).\n3. Phiếu đang đi xếp hàng: mọi dòng đã có người đi xếp.'],
        ['Dòng sự kiện chính', '1. Bấm "Nhập kho" (phiếu đang đi xếp hàng) hoặc "Sửa phiếu" (phiếu đang nhập kho) ở dòng danh sách / trang Chi tiết.\n2. Hệ thống mở trang "Phiếu nhập kho: <mã>" với dữ liệu hiện tại; có khối File đính kèm.\n3. Người dùng sửa Người giao hàng, Ghi chú, SL nhập / vị trí từng dòng, vận chuyển, bốc xếp; thêm file.\n4. Bấm "Lưu và nhập".\n5. Hệ thống kiểm tra, ghi lô thực nhập, cộng tồn kho theo kho / vị trí / lô; ghi thời điểm nhận; đề nghị nhập kho → Đã nhập kho, yêu cầu nhập hàng → Đã nhập kho; phiếu → Chờ duyệt; thông báo kế toán kho của kho.\n6. ' + LS % 'Thay đổi thông tin và Thay đổi trạng thái (Đang tạo → Chờ duyệt)' + '\n7. Báo "Phiếu đã được gửi", về danh sách.'],
        ['Dòng sự kiện phụ', '• Bấm "Lưu": ghi như trên nhưng KHÔNG ghi tồn, phiếu vẫn Đang tạo (tiến trình Đang nhập kho), báo "Phiếu đã được lưu. Bạn cần gửi để phiếu được xử lý".\n• Công ty vận chuyển có chuyến xe chưa duyệt khi "Lưu và nhập": "Chuyến xe chưa được duyệt — duyệt chuyến xe trước khi gửi."; nếu chuyến chưa duyệt sau khi lưu → phiếu giữ Đang tạo, báo "Phiếu đã được lưu. Bạn cần duyệt chuyến xe trước khi gửi".\n• Chưa có file: "Bắt buộc phải chọn file đính kèm".\n• Chưa xếp xong: "Chưa xếp hàng xong — hãy lưu phiếu xếp hàng (chọn người đi xếp cho mọi dòng) trước khi nhập kho."\n• "In dự kiến": xem trước bản in phiếu với dữ liệu đã lưu.\n• Loại mua ngoài: khi gửi cập nhật dòng đơn đặt hàng gốc "Đã nhập kho" và trừ hàng đang về.'],
    ],
    'menu_them': ' => Nhập kho {icon:btn_nhapkho}',
    'ghi_chu_layout': TRANG % '"Phiếu nhập kho: <mã>"',
    'anh': [('40_import', 'Trang Nhập kho của phiếu đang đi xếp hàng'),
            ('40b_import_vanchuyen', 'Tab Vận chuyển ở bước Nhập kho khi chọn "Công ty vận chuyển": thêm Tuyến đường, Số km chốt, Ghi chú vận chuyển'),
            ('18b_unsaved_edit', 'Hộp Thông tin chưa lưu khi rời trang đã sửa')],
    'ui': ui(UI8, [
        ['Phiếu đề nghị nhập kho', 'Link', 'Read-only', '–', '–', 'Theo phiếu', 'Liên kết mở đề nghị; không đổi được.'],
        ['Người giao hàng, Ghi chú', 'Textbox', 'Enable', '≤ 255 ký tự', 'Có / Không', 'Dữ liệu hiện tại', 'Như màn tạo. Ghi chú trống thì lấy ghi chú đề nghị.'],
        ['Tab Vận chuyển – Tuyến đường', 'Dropdown', 'Enable', 'Danh mục tuyến đường', 'Có khi Công ty vận chuyển', 'Trống', 'Bỏ trống: "Bắt buộc phải chọn".'],
        ['Tab Vận chuyển – Số km dự kiến', 'Textbox', 'Read-only', '–', '–', 'Theo yêu cầu nhập hàng', '–'],
        ['Tab Vận chuyển – Số km chốt', 'Textbox', 'Enable', '1 – 999,999', 'Có khi Công ty vận chuyển', 'Dữ liệu hiện tại', '"Bắt buộc phải nhập" / "Không được lớn hơn 999,999".'],
        ['Tab Vận chuyển – Ghi chú vận chuyển', 'Textarea', 'Enable', '–', 'Có khi km chốt ≠ km dự kiến', 'Trống', '"Số km chốt khác số km dự kiến — bắt buộc nhập ghi chú vận chuyển".'],
        ['Chuyến xe', 'Dropdown', 'Enable / Disable', '–', 'Có khi Công ty vận chuyển', 'Theo phiếu', 'Chuyến đã duyệt bị khoá, không gỡ được ("Không được gỡ chuyến xe đã duyệt.").'],
        ['File đính kèm', 'File', 'Enable', 'pdf, jpeg, jpg, png, doc, csv, xlsx, xls, docx; ≤ 20MB/file', 'Có (khi phiếu chưa có file)', 'File đã lưu', '"Thêm tài liệu" tải file lên ngay; gỡ file đã lưu được khi phiếu còn sửa được.'],
        ['Bảng Hàng hoá', 'Table/Grid', 'Enable', '–', 'Có', 'Vị trí dự kiến / thực', 'Như màn tạo; vị trí chỉ bắt buộc ở dòng SL > 0; không có "Áp dụng tất cả".'],
        ['Tab Bốc xếp', 'Group', 'Enable', '–', '–', 'Dữ liệu hiện tại', 'Như màn tạo.'],
        ['Nút In dự kiến', 'Button', 'Enable', '–', '–', '–', 'Xem trước bản in phiếu nhập kho (mục 2.14).'],
        ['Nút Lưu / Lưu và nhập / Quay lại', 'Button', 'Enable', '–', '–', '–', 'Lưu giữ nháp / Lưu và gửi (ghi tồn) / về danh sách.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Mở trang', 'System', 'Before:\n– Phiếu Đang tạo, người dùng là người tạo (hoặc Super admin); không đúng → "Phiếu không sửa được hoặc bạn không có quyền." và về danh sách.\nAfter:\n– Nạp dữ liệu, tồn hiện tại tại từng vị trí.'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm quyền sửa; phiếu đang xếp hàng phải xếp xong.\nDuring:\n– Kiểm như màn tạo + file bắt buộc + luật vận chuyển (tuyến đường, km chốt, ghi chú km).\n' + TRUOC_LUU + '\nAfter:\n– Ghi lại lô thực nhập, file, chuyến xe, bốc xếp; tiến trình Đang nhập kho.\n– ' + LS % 'Thay đổi thông tin (giá trị cũ → mới, gồm bảng hàng × vị trí)' + '\n– Báo "Phiếu đã được lưu. Bạn cần gửi để phiếu được xử lý".'],
        ['Bấm Lưu và nhập', 'Click', 'Before:\n– Như Lưu; Công ty vận chuyển: mọi chuyến xe đã duyệt.\nDuring:\n– Như Lưu.\n' + TRUOC_LUU + '\nAfter:\n– Ghi như Lưu; cộng tồn kho (kho, kho theo công ty, vị trí, lô tại vị trí + nhật ký tồn) (BR-06).\n– Ghi Ngày nhận; phiếu → Chờ duyệt; đề nghị nhập kho → Đã nhập kho; yêu cầu nhập hàng → Đã nhập kho; thông báo kế toán kho của kho.\n– ' + LS % 'Thay đổi trạng thái' + '\n– Báo "Phiếu đã được gửi", về danh sách.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Đã sửa → hộp "Thông tin chưa lưu" (Thoát / Ở lại).'],
    ],
})

# 2.8 Xem chi tiết --------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết phiếu nhập kho', 'uc': 'uc_xem', 'uc_ten': 'FR-08 Xem chi tiết phiếu nhập kho',
    'qtc': 'Màn Xem chi tiết và Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết phiếu nhập kho'],
        ['Mô tả', 'Xem toàn bộ thông tin phiếu ở chế độ chỉ đọc: thông tin chung, vận chuyển, bốc xếp, file đính kèm, hàng hoá × vị trí, khối Lịch sử; thanh nút dưới cùng có cùng bộ thao tác với dòng danh sách.'],
        ['Tác nhân', Q_ALL],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Mã phiếu ở danh sách.\n2. Hệ thống mở "Chi tiết phiếu nhập kho: <mã>" kèm nhãn trạng thái trên tiêu đề trang.\n3. Tab Thông tin chung: Loại, Phiếu đề nghị nhập kho, Người giao hàng, Kho nhập, Người đề nghị, Khách hàng (nếu có), Ứng với phiếu điều chuyển kho (nếu có), Nhập lại cho phiếu / Phiếu xuất lại (nếu có), Ghi chú, Lý do không duyệt (nếu có).\n4. Tab Vận chuyển (Công ty vận chuyển): Tuyến đường, Số km dự kiến, Số km chốt, Chuyến xe, Ghi chú vận chuyển. Tab Bốc xếp luôn có.\n5. Khối Chi tiết: bảng hàng hoá (phiếu đang xếp hàng có thêm cột Nhóm, Người đi xếp), dòng Tổng cộng.'],
        ['Dòng sự kiện phụ', '• Phiếu ngoài phạm vi / không tồn tại: "Không tìm thấy phiếu nhập kho hoặc bạn không có quyền xem." và về danh sách.\n• Thao tác Không duyệt / Hủy ở trang chi tiết xong thì về danh sách.'],
    ],
    'menu_them': ' => Mã phiếu (liên kết)',
    'anh': [('20_detail', 'Chi tiết phiếu Chờ duyệt (kế toán kho): Tạo phiếu nhập hàng, Không duyệt, In phiếu, In barcode'),
            ('20b_detail_bocxep', 'Tab Bốc xếp ở trang Chi tiết'),
            ('22_detail_draft', 'Chi tiết phiếu Đang tạo – Đang đi xếp hàng: cột Nhóm, Người đi xếp; nút Nhập kho, Hủy, Phiếu xếp hàng, In phiếu'),
            ('21_detail_deny', 'Chi tiết phiếu Không duyệt: Lý do không duyệt, nút Tạo phiếu xuất lại')],
    'ui': ui(UI6, [
        ['Tiêu đề trang', 'Label', 'Read-only', '–', '"Chi tiết phiếu nhập kho: <mã>" + nhãn trạng thái.'],
        ['Tiêu đề khối + người tạo', 'Label', 'Read-only', '–', 'Tên loại phiếu; "<Người tạo> - <ngày giờ tạo>".'],
        ['Tab Thông tin chung / Vận chuyển / Bốc xếp', 'Tab', 'Read-only', 'Thông tin chung', 'Các ô khoá; Vận chuyển chỉ khi loại có vận chuyển và Công ty vận chuyển; Bốc xếp chưa khai thì "Không có thông tin bốc xếp".'],
        ['File đính kèm', 'File', 'Read-only', 'Có file thì hiện', 'Tên file, dung lượng; mở / tải file.'],
        ['Bảng Hàng hoá', 'Table/Grid', 'Read-only', '–', 'Tên hàng hoá, Model, Mã hàng hoá, Thương hiệu, ĐVT, SL đề nghị, SL thực nhập, Vị trí, SL nhập (+ Nhóm, Người đi xếp khi đang xếp hàng; + Ghi chú với loại Nhập hàng khác); dòng Tổng cộng.'],
        ['Khối Lịch sử', 'Panel', 'Enable', 'Thu gọn', 'Mở xem các mốc (mục 2.17).'],
        ['Thanh nút', 'Button', 'Enable / Ẩn', 'Theo trạng thái', 'Như cột Hành động (trừ Xem lịch sử) + Quay lại.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở trang', 'System', 'Before:\n– Kiểm phạm vi xem (BR-02).\nAfter:\n– Hiển thị dữ liệu, tính nút theo trạng thái / vai trò.'],
        ['Bấm nút thao tác', 'Click', 'After:\n– Mở chức năng tương ứng (mục 2.6 – 2.15).'],
    ],
})

# 2.9 Hủy ----------------------------------------------------------------------
FR.append({
    'ten': 'Hủy phiếu nhập kho', 'uc': 'uc_huy', 'uc_ten': 'FR-09 Hủy phiếu nhập kho',
    'qtc': 'Quy tắc xác nhận, Thông báo và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Hủy phiếu nhập kho'],
        ['Mô tả', 'Người tạo hủy phiếu còn Đang tạo; đề nghị nhập kho nguồn bị hủy theo. Phiếu đang tạo chưa ghi tồn nên không phải hoàn tồn.'],
        ['Tác nhân', 'Người tạo phiếu'],
        ['Điều kiện ban đầu', '1. Phiếu Đang tạo, người dùng là người tạo.\n2. Loại phiếu không thuộc nhóm điều chuyển (cùng thủ kho, kho nội bộ, kho chi nhánh, trả lại điều chuyển), nhập ghép, nhập tách.'],
        ['Dòng sự kiện chính', '1. Bấm Hủy ở dòng danh sách / trang Chi tiết.\n2. Hộp "Xác nhận hủy": "Phiếu <mã> sẽ bị hủy, đề nghị nhập kho nguồn cũng bị hủy theo."\n3. Bấm "Hủy phiếu".\n4. Hệ thống: phiếu → Đã hủy; hủy đề nghị nhập kho nguồn; thông báo người lập đề nghị.\n5. ' + LS % 'Thay đổi trạng thái (Đang tạo → Đã hủy)' + '\n6. Báo "Đã hủy phiếu nhập kho", tải lại danh sách (từ Chi tiết: về danh sách).'],
        ['Dòng sự kiện phụ', '• Bấm Đóng / (x): không thay đổi.\n• Phiếu không còn hủy được: "Không thể hủy phiếu này."'],
    ],
    'menu_them': ' => Hủy {icon:btn_huy}',
    'ghi_chu_layout': 'Modal Xác nhận hủy được mở ngay trên màn hình danh sách hoặc trang Chi tiết theo đường dẫn ở trên.',
    'anh': [('13_cancel', 'Hộp Xác nhận hủy')],
    'ui': ui(UI4, [
        ['Tiêu đề / nội dung', 'Label', '"Xác nhận hủy" — "Phiếu <mã> sẽ bị hủy, đề nghị nhập kho nguồn cũng bị hủy theo."'],
        ['Nút Hủy phiếu', 'Button', 'Xác nhận hủy.'],
        ['Nút Đóng', 'Button', 'Đóng hộp, không hủy.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Hủy phiếu', 'Click', 'Before:\n– Người tạo, phiếu Đang tạo, loại được hủy.\n' + TRUOC_LUU + '\nAfter:\n– Phiếu Đã hủy, đề nghị nhập kho hủy theo, thông báo; ' + LS % 'Thay đổi trạng thái' + '\n– Báo "Đã hủy phiếu nhập kho".'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng hộp.'],
    ],
})

# 2.10 Không duyệt -------------------------------------------------------------
FR.append({
    'ten': 'Không duyệt phiếu nhập kho', 'uc': 'uc_khongduyet', 'uc_ten': 'FR-10 Không duyệt phiếu nhập kho',
    'qtc': 'Quy tắc xác nhận có nhập lý do, Thông báo và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Không duyệt phiếu nhập kho'],
        ['Mô tả', 'Kế toán kho từ chối phiếu Chờ duyệt kèm lý do. KHÔNG hoàn tồn: hàng đã nhập ra khỏi kho qua phiếu xuất lại (mục 2.12).'],
        ['Tác nhân', KTK + ' cùng công ty với phiếu; Super admin'],
        ['Điều kiện ban đầu', '1. Phiếu Chờ duyệt.\n2. Người dùng có quyền "Kế toán kho" và cùng công ty với phiếu.\n3. Loại phiếu không thuộc: điều chuyển cùng thủ kho, điều chuyển kho nội bộ, nhập ghép, nhập tách.'],
        ['Dòng sự kiện chính', '1. Bấm Không duyệt.\n2. Hộp "Không duyệt phiếu nhập kho": "Phiếu <mã> sẽ bị không duyệt.", ô Lý do không duyệt (bắt buộc).\n3. Nhập lý do, bấm "Không duyệt".\n4. Hệ thống: phiếu → Không duyệt, lưu lý do; thông báo người tạo phiếu.\n5. ' + LS % 'Thay đổi trạng thái (Chờ duyệt → Không duyệt, kèm lý do)' + '\n6. Báo "Đã không duyệt phiếu nhập kho".'],
        ['Dòng sự kiện phụ', '• Bỏ trống lý do: "Vui lòng nhập lý do không duyệt." (hệ thống: "Bắt buộc phải nhập lý do"); quá 255 ký tự: "Không được vượt quá 255 ký tự".\n• Không có quyền: "Bạn không có quyền không duyệt phiếu này."'],
    ],
    'menu_them': ' => Không duyệt {icon:btn_khongduyet}',
    'ghi_chu_layout': 'Modal Không duyệt phiếu nhập kho được mở ngay trên màn hình danh sách hoặc trang Chi tiết theo đường dẫn ở trên.',
    'anh': [('15_deny', 'Hộp Không duyệt phiếu nhập kho')],
    'ui': ui(UI8, [
        ['Lý do không duyệt', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống', 'Placeholder "Nhập lý do không duyệt...".'],
        ['Nút Không duyệt', 'Button', 'Enable', '–', '–', '–', 'Xác nhận.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng, không thay đổi.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Không duyệt (trong hộp)', 'Click', 'Before:\n– Kế toán kho cùng công ty, phiếu Chờ duyệt, loại được không duyệt.\nDuring:\n– Lý do bắt buộc, ≤ 255 ký tự.\n' + TRUOC_LUU + '\nAfter:\n– Phiếu Không duyệt, thông báo người tạo; ' + LS % 'Thay đổi trạng thái' + '\n– Báo "Đã không duyệt phiếu nhập kho".'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng hộp.'],
    ],
})

# 2.11 Tạo phiếu nhập hàng ------------------------------------------------------
FR.append({
    'ten': 'Tạo phiếu nhập hàng', 'uc': 'uc_taopnh', 'uc_ten': 'FR-11 Tạo phiếu nhập hàng từ phiếu nhập kho',
    'qtc': 'Quy tắc liên kết chứng từ.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tạo phiếu nhập hàng từ phiếu nhập kho'],
        ['Mô tả', 'Kế toán kho mở form Thêm phiếu nhập hàng (màn Phiếu nhập hàng) đã chọn sẵn phiếu nhập kho để hạch toán. Lập phiếu nhập hàng → phiếu nhập kho Đang hạch toán; phiếu nhập hàng hoàn thành → Đã hạch toán.'],
        ['Tác nhân', KTK + ' cùng công ty; Super admin'],
        ['Điều kiện ban đầu', '1. Phiếu Chờ duyệt, loại khác "Nhập điều chuyển cùng thủ kho".\n2. Người dùng có quyền "Kế toán kho" cùng công ty với phiếu.'],
        ['Dòng sự kiện chính', '1. Bấm "Tạo phiếu nhập hàng".\n2. Hệ thống mở trang "Thêm phiếu nhập hàng" với ô "Chọn phiếu nhập kho" = phiếu này.\n3. Kế toán kho lập phiếu nhập hàng (theo SRS Phiếu nhập hàng).\n4. Khi phiếu nhập hàng được lưu: phiếu nhập kho → Đang hạch toán (ghi người duyệt, ngày duyệt); đề nghị nhập kho, yêu cầu nhập hàng đổi trạng thái theo.\n5. Khi phiếu nhập hàng hoàn thành: phiếu nhập kho → Đã hạch toán.'],
        ['Dòng sự kiện phụ', '• Thao tác ghi thuộc màn Phiếu nhập hàng; màn Phiếu nhập kho chỉ mở form.'],
    ],
    'menu_them': ' => Tạo phiếu nhập hàng {icon:btn_taophieunhaphang}',
    'ghi_chu_layout': 'Trang Thêm phiếu nhập hàng (màn Phiếu nhập hàng) được mở từ màn hình danh sách hoặc trang Chi tiết theo đường dẫn ở trên.',
    'anh': [('70_create_product_import', 'Trang Thêm phiếu nhập hàng mở từ phiếu nhập kho')],
    'ui': ui(UI4, [
        ['Nút Tạo phiếu nhập hàng', 'Button', 'Chỉ hiện với kế toán kho cùng công ty khi phiếu Chờ duyệt.'],
        ['Ô Chọn phiếu nhập kho (màn Phiếu nhập hàng)', 'Picker', 'Điền sẵn mã phiếu nhập kho.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Tạo phiếu nhập hàng', 'Click', 'After:\n– Chuyển sang trang Thêm phiếu nhập hàng với phiếu nhập kho đã chọn.'],
        ['Lưu / hoàn thành phiếu nhập hàng (màn khác)', 'System', 'After:\n– Phiếu nhập kho Đang hạch toán / Đã hạch toán (BR-07).'],
    ],
})

# 2.12 Xuất lại ----------------------------------------------------------------
FR.append({
    'ten': 'Tạo phiếu xuất lại', 'uc': 'uc_xuatlai', 'uc_ten': 'FR-12 Tạo phiếu xuất lại',
    'qtc': 'Quy tắc xác nhận, Thông báo và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tạo phiếu xuất lại cho phiếu nhập kho bị Không duyệt'],
        ['Mô tả', 'Người tạo phiếu xuất TOÀN BỘ hàng đã nhập ra khỏi kho đúng lô, đúng vị trí (trừ tồn), sinh phiếu xuất lại PXL-<5 chữ số>; phiếu nhập kho → Đã xuất lại.'],
        ['Tác nhân', 'Người tạo phiếu'],
        ['Điều kiện ban đầu', '1. Phiếu Không duyệt, người dùng là người tạo.'],
        ['Dòng sự kiện chính', '1. Bấm "Tạo phiếu xuất lại".\n2. Hệ thống mở trang "Tạo phiếu xuất lại": Phiếu nhập kho (liên kết), Người tạo, Kho, Người giao hàng, Lý do không duyệt (chỉ đọc), Ghi chú; bảng "Hàng hoá xuất lại".\n3. Nhập Ghi chú (≤ 255), bấm "Xuất lại".\n4. Hộp "Xác nhận xuất lại": "Toàn bộ hàng của phiếu <mã> sẽ bị trừ khỏi tồn kho. Thao tác không hoàn tác được."; bấm "Xuất lại".\n5. Hệ thống kiểm đủ tồn mọi lô rồi trừ tồn; tạo phiếu xuất lại (Chờ nhập lại); phiếu nhập kho → Đã xuất lại.\n6. ' + LS % 'Thay đổi trạng thái (Không duyệt → Đã xuất lại, ghi chú "Tạo phiếu xuất lại <mã PXL>")' + '\n7. Báo "Hàng đã được xuất lại".'],
        ['Dòng sự kiện phụ', '• Không đủ tồn: "Hàng <tên> không đủ tồn kho. Cần x, còn y" / "… không đủ tồn tại vị trí <mã>…" / "… không đủ tồn trong lô tại vị trí <mã>…"; không trừ gì.\n• Không phải người tạo / phiếu không Không duyệt: "Chỉ người tạo phiếu nhập kho bị Không duyệt mới được tạo phiếu xuất lại."'],
    ],
    'menu_them': ' => Tạo phiếu xuất lại {icon:btn_xuatlai_row}',
    'ghi_chu_layout': TRANG % '"Tạo phiếu xuất lại"',
    'anh': [('50_reexport', 'Trang Tạo phiếu xuất lại'), ('51_reexport_confirm', 'Hộp Xác nhận xuất lại')],
    'ui': ui(UI8, [
        ['Thông tin phiếu nhập kho', 'Textbox', 'Read-only', '–', '–', 'Theo phiếu', 'Phiếu nhập kho, Người tạo, Kho, Người giao hàng, Lý do không duyệt.'],
        ['Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống', '"Không được vượt quá 255 ký tự".'],
        ['Bảng Hàng hoá xuất lại', 'Table/Grid', 'Read-only', '–', '–', 'Toàn bộ lô của phiếu', 'Không chọn từng dòng: xuất toàn bộ.'],
        ['Nút Xuất lại / Quay lại', 'Button', 'Enable', '–', '–', '–', 'Mở hộp xác nhận / về trang Chi tiết.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất lại (trong hộp)', 'Click', 'Before:\n– Người tạo, phiếu Không duyệt.\nDuring:\n– Kiểm đủ tồn tổng, tại vị trí, trong lô cho mọi lô.\n' + TRUOC_LUU + '\nAfter:\n– Trừ tồn; tạo phiếu xuất lại; phiếu nhập kho Đã xuất lại; ghi lịch sử phiếu nhập kho và phiếu xuất lại.\n– Báo "Hàng đã được xuất lại".'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.13 Nhập lại ----------------------------------------------------------------
FR.append({
    'ten': 'Tạo phiếu nhập lại', 'uc': 'uc_nhaplai', 'uc_ten': 'FR-13 Tạo phiếu nhập lại',
    'qtc': 'Màn Thêm mới, Validate dữ liệu và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tạo phiếu nhập lại cho phiếu Đã xuất lại'],
        ['Mô tả', 'Sinh phiếu nhập kho MỚI (Nhập lại cho phiếu <mã gốc>) chép thông tin + chuyến xe của phiếu gốc, form như Nhập kho (file bắt buộc chọn mới). Lưu / Lưu và nhập như mục 2.7; phiếu gốc → Đã nhập lại, phiếu xuất lại → Đã nhập lại.'],
        ['Tác nhân', 'Người tạo phiếu gốc'],
        ['Điều kiện ban đầu', '1. Phiếu Đã xuất lại, người dùng là người tạo; phiếu đã có phiếu xuất lại.'],
        ['Dòng sự kiện chính', '1. Bấm "Tạo phiếu nhập lại".\n2. Hệ thống mở trang "Tạo phiếu nhập lại" (Người giao hàng khoá theo phiếu gốc, chưa có file).\n3. Nhập SL / vị trí, file, vận chuyển, bốc xếp; bấm Lưu hoặc Lưu và nhập.\n4. Hệ thống tạo phiếu mới, xử lý như mục 2.7 (Lưu và nhập thì cộng tồn, Chờ duyệt; KHÔNG trừ hàng đang về lần 2).\n5. Phiếu gốc → Đã nhập lại (lịch sử ghi "Tạo phiếu nhập lại <mã mới>"); phiếu mới ghi nhận Tạo mới.'],
        ['Dòng sự kiện phụ', '• Không có quyền: "Bạn không có quyền nhập lại phiếu này."\n• Chưa có phiếu xuất lại: "Phiếu nhập kho chưa có phiếu xuất lại."'],
    ],
    'menu_them': ' => Tạo phiếu nhập lại {icon:btn_nhaplai_row}',
    'ghi_chu_layout': TRANG % '"Tạo phiếu nhập lại"',
    'anh': [('55_reimport', 'Trang Tạo phiếu nhập lại')],
    'ui': ui(UI6, [
        ['Người giao hàng', 'Textbox', 'Read-only', 'Theo phiếu gốc', 'Không sửa được.'],
        ['Các ô / bảng còn lại', '–', 'Enable', 'Theo phiếu gốc', 'Như trang Nhập kho (mục 2.7); File đính kèm để trống, bắt buộc chọn.'],
        ['Nút Lưu / Lưu và nhập / Quay lại', 'Button', 'Enable', '–', 'Như mục 2.7 (không có In dự kiến).'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lưu / Lưu và nhập', 'Click', 'Before:\n– Người tạo, phiếu gốc Đã xuất lại.\nDuring:\n– Kiểm như mục 2.7.\n' + TRUOC_LUU + '\nAfter:\n– Tạo phiếu mới (mã PNK mới, Nhập lại cho phiếu gốc), xử lý như mục 2.7; phiếu xuất lại Đã nhập lại; phiếu gốc Đã nhập lại; ghi lịch sử cả hai.'],
    ],
})

# 2.14 In phiếu ----------------------------------------------------------------
FR.append({
    'ten': 'In phiếu nhập kho', 'uc': 'uc_in', 'uc_ten': 'FR-14 In phiếu nhập kho',
    'qtc': 'Quy tắc màn In và bố cục bản in.',
    'gioi_thieu': [
        ['Tên chức năng', 'In phiếu nhập kho'],
        ['Mô tả', 'Xem trước và in "PHIẾU NHẬP KHO" theo mẫu: tiêu đề công ty của phiếu, mã phiếu, đề nghị nhập kho, loại nhập, ngày lập, người đề nghị, người giao hàng, người lập, ghi chú, bảng hàng hoá × vị trí, khối ký Người lập phiếu – Người giao hàng/NVKD – Thủ kho – Trưởng phòng Logistic.'],
        ['Tác nhân', Q_ALL],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm "In phiếu" ở dòng danh sách / trang Chi tiết (hoặc "In dự kiến" ở trang Nhập kho).\n2. Hệ thống mở cửa sổ "Xem trước phiếu nhập kho <mã>".\n3. Bấm In để mở hộp in của trình duyệt.'],
        ['Dòng sự kiện phụ', '• Thiếu mẫu in / không xem được phiếu: "Không tìm thấy phiếu hoặc thiếu mẫu in phiếu nhập kho."'],
    ],
    'menu_them': ' => In phiếu {icon:btn_inphieu}',
    'ghi_chu_layout': 'Cửa sổ Xem trước được mở ngay trên màn hình danh sách hoặc trang Chi tiết theo đường dẫn ở trên.',
    'anh': [('19_print', 'Cửa sổ Xem trước phiếu nhập kho')],
    'ui': ui(UI4, [
        ['Bản in', 'Label', 'Theo mẫu phiếu nhập kho; phiếu đang xếp hàng in vị trí dự kiến.'],
        ['Nút In', 'Button', 'Mở hộp in của trình duyệt.'],
        ['Nút (x)', 'Button', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm In phiếu', 'Click', 'Before:\n– Kiểm phạm vi xem.\nAfter:\n– Dựng bản in theo mẫu, không ghi dữ liệu.'],
        ['Bấm In', 'Click', 'After:\n– Mở hộp in của trình duyệt.'],
    ],
})

# 2.15 In barcode --------------------------------------------------------------
FR.append({
    'ten': 'In barcode lô hàng', 'uc': 'uc_barcode', 'uc_ten': 'FR-15 In barcode lô hàng',
    'qtc': 'Quy tắc màn In.',
    'gioi_thieu': [
        ['Tên chức năng', 'In barcode / tem phụ cho lô hàng đã nhập'],
        ['Mô tả', 'Trang "Danh sách hàng hóa" của phiếu đã nhập kho: chọn Nhà cung cấp, Năm sản xuất, Khổ giấy; mỗi dòng chọn Mẫu in, Ngày sản xuất, Hạn sử dụng, Số lượng in; in "In barcode + tem phụ" / "In barcode" / "In tem phụ".'],
        ['Tác nhân', Q_ALL],
        ['Điều kiện ban đầu', DK + '\n3. Phiếu đã ở bước nhập kho (có lô thực).'],
        ['Dòng sự kiện chính', '1. Bấm "In barcode".\n2. Hệ thống mở trang in tem với các dòng lô.\n3. Chọn thông số, bấm 1 trong 3 nút in.\n4. Hệ thống dựng tem (ghi mã lô vào lô nếu lô chưa có), mở xem trước, bấm In.'],
        ['Dòng sự kiện phụ', '• Phiếu chưa nhập kho: "Phiếu chưa nhập kho (chưa có lô) hoặc bạn không có quyền."\n• Chưa có khổ giấy: nút in bị khoá.'],
    ],
    'menu_them': ' => In barcode {icon:btn_inbarcode}',
    'ghi_chu_layout': TRANG % 'In barcode ("Phiếu nhập kho: <mã>")',
    'anh': [('60_barcode', 'Trang In barcode lô hàng')],
    'ui': ui(UI6, [
        ['Nhà cung cấp, Năm sản xuất, Khổ giấy', 'Dropdown', 'Enable', 'Khổ giấy 1 tem / 2 tem', 'Thông số chung của tem.'],
        ['Bảng hàng hoá', 'Table/Grid', 'Enable', 'Theo lô', 'Tên hàng hoá, Model, Mã hàng hoá, Thương hiệu, Mẫu in, Đơn vị tính, Ngày sản xuất, Hạn sử dụng, Số lượng in.'],
        ['Nút In barcode + tem phụ / In barcode / In tem phụ', 'Button', 'Enable', '–', 'Dựng và xem trước tem.'],
        ['Nút Quay lại', 'Button', 'Enable', '–', 'Về trang Chi tiết.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm nút in', 'Click', 'After:\n– Dựng trang tem theo mẫu, mở xem trước; lô chưa có mã thì hệ thống ghi mã lô.'],
    ],
})

# 2.16 Xuất Excel --------------------------------------------------------------
FR.append({
    'ten': 'Xuất Excel danh sách', 'uc': 'uc_xuat', 'uc_ten': 'FR-16 Xuất Excel danh sách phiếu nhập kho',
    'qtc': 'Quy tắc Excel và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách phiếu nhập kho ra Excel'],
        ['Mô tả', 'Xuất mọi dòng khớp bộ lọc + phạm vi (không chỉ trang đang xem) ra file danh_sach_phieu_nhap_kho.xlsx, tiêu đề "DANH SÁCH PHIẾU NHẬP KHO", có dòng khoảng ngày lọc và khối ký "Người lập".'],
        ['Tác nhân', Q_ALL],
        ['Điều kiện ban đầu', '1. Người dùng đăng nhập thành công.'],
        ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Cửa sổ "Chọn trường xuất Excel" tích sẵn 14 trường.\n3. Tích / bỏ, kéo ☰ đổi thứ tự, bấm Xuất file.\n4. Hệ thống tải dữ liệu, dựng file, tải về; báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Lỗi: "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất Excel')],
    'ui': ui(UI8, [
        ['Danh sách trường', 'Checkbox', 'Enable', '14 trường', 'Có (≥ 1)', 'Tất cả', 'Mã phiếu, Loại, Nhà cung cấp, Kho nhập, Ngày tạo, Phiếu ĐNNK, Người đề nghị, Người yêu cầu, Người tạo, Trạng thái, Tiến trình, Người duyệt, Ngày nhận, Ngày duyệt; dòng đếm "Đang chọn x/14 trường".'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', 'Chọn / bỏ nhanh.'],
        ['Nút Xuất file / Đóng', 'Button', 'Enable', '–', '–', '–', 'Xuất / đóng không xuất.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất file', 'Click', 'After:\n– Tải dữ liệu theo bộ lọc + phạm vi, dựng file đúng thứ tự cột, tải về.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.17 Lịch sử -----------------------------------------------------------------
FR.append({
    'ten': 'Xem lịch sử thay đổi',
    'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem lịch sử thay đổi phiếu nhập kho'],
        ['Mô tả', 'Các mốc Tạo mới, Thay đổi thông tin (Người giao hàng, Ghi chú, Vận chuyển, Số km chốt, File đính kèm, Lý do, bảng hàng × vị trí), Thay đổi trạng thái (kèm lý do / ghi chú), mới nhất trên cùng.'],
        ['Tác nhân', Q_ALL],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm "Xem lịch sử" ở cột Hành động → cửa sổ "Lịch sử thay đổi: <mã phiếu>".\n2. Hoặc mở khối Lịch sử cuối trang Chi tiết.\n3. Có nút Bộ lọc (loại hành động, người thực hiện, khoảng ngày).'],
        ['Dòng sự kiện phụ', '• Phiếu tạo trước khi chuyển sang hệ thống mới có thể không có mốc nào.\n• Giá trị cũ in đỏ, giá trị mới in xanh.'],
    ],
    'menu_them': ' => Xem lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': 'Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách; khối Lịch sử nằm cuối trang Chi tiết.',
    'anh': [('16_history', 'Cửa sổ Lịch sử thay đổi'), ('20c_detail_history', 'Khối Lịch sử ở trang Chi tiết')],
    'ui': ui(UI6, [
        ['Tiêu đề', 'Label', 'Read-only', '"Lịch sử thay đổi: <mã phiếu>"', '–'],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Lọc theo loại hành động, người thực hiện, Từ ngày, Đến ngày.'],
        ['Mốc lịch sử', 'Label', 'Read-only', 'Mới nhất trên cùng', 'Thời điểm, tên hành động, "Người thực hiện: <họ tên> — <phòng ban>", trường đổi: cũ → mới, ghi chú.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Xem lịch sử', 'Click', 'After:\n– Tải và hiển thị các mốc.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

FR_NAMES = ['FR-%02d %s' % (i + 1, f['ten']) for i, f in enumerate(FR)]

# ma trận: chức năng × vai trò
_VT = ['Thủ kho / người tạo phiếu', 'Kế toán kho', 'Người dùng khác (trong phạm vi xem)']
_MT = {
    0: ('Có', 'Có', 'Có'), 1: ('Có', 'Có', 'Có'), 2: ('Có', 'Có', 'Có'),
    3: ('Có (thủ kho kho nhập)', 'Không', 'Không'), 4: ('Có (thủ kho kho nhập)', 'Không', 'Không'),
    5: ('Có (phiếu Đang đi xếp hàng)', 'Không', 'Không'), 6: ('Có (người tạo, phiếu Đang tạo)', 'Không', 'Không'),
    7: ('Có', 'Có', 'Có'), 8: ('Có (người tạo, phiếu Đang tạo)', 'Không', 'Không'),
    9: ('Không', 'Có (phiếu Chờ duyệt, cùng công ty)', 'Không'), 10: ('Không', 'Có (phiếu Chờ duyệt, cùng công ty)', 'Không'),
    11: ('Có (người tạo, phiếu Không duyệt)', 'Không', 'Không'), 12: ('Có (người tạo, phiếu Đã xuất lại)', 'Không', 'Không'),
    13: ('Có', 'Có', 'Có'), 14: ('Có (phiếu đã nhập kho)', 'Có (phiếu đã nhập kho)', 'Có (phiếu đã nhập kho)'),
    15: ('Có', 'Có', 'Có'), 16: ('Có', 'Có', 'Có'),
}

S = {
    'ten': TEN, 'ten_ngan': 'phiếu nhập kho', 'phan_he': 'Tài chính (đồng thời có ở phân hệ Kho)',
    'menu': [('Tài chính', 'menu_phanhe'), ('Hàng hoá - Dịch vụ - Vận chuyển', 'menu_nhom'), ('Nhập hàng', None), (TEN, 'menu_muc')],
    'muc_dich': [
        'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho chứng từ thủ kho nhập hàng VẬT LÝ vào vị trí kho — tầng thứ 3 của luồng nhập hàng: Yêu cầu nhập hàng → Đề nghị nhập kho → Phiếu nhập kho → Phiếu nhập hàng.',
        'Là căn cứ nghiệm thu chức năng, luồng trạng thái và phân quyền của màn hình.',
        'Làm rõ 2 bước dự kiến vị trí → đi xếp hàng → nhập kho, thời điểm GHI TỒN KHO (Lưu và nhập) và các tác động sang đề nghị nhập kho, yêu cầu nhập hàng, phiếu nhập hàng.',
        'Làm rõ nhánh Không duyệt → Xuất lại (trừ tồn) → Nhập lại (phiếu mới) và nhánh Hủy.',
        'Làm rõ phạm vi dữ liệu theo quyền xem, vai trò thủ kho và kế toán kho.',
    ],
    'thuat_ngu': [
        ['Phiếu nhập kho (PNK)', 'Chứng từ thủ kho nhập hàng vào vị trí kho, mã PNK-<5 chữ số>, lập từ 1 đề nghị nhập kho.'],
        ['Đề nghị nhập kho (ĐNNK)', 'Chứng từ nguồn; phiếu nhập kho chỉ lập được từ đề nghị Chờ duyệt.'],
        ['Thủ kho', 'Nhân viên được khai là thủ kho của kho (danh mục kho); tạo phiếu, đi xếp hàng, nhập kho.'],
        ['Kế toán kho', 'Người có quyền "Kế toán kho"; xử lý phiếu Chờ duyệt: lập phiếu nhập hàng hoặc Không duyệt.'],
        ['Vị trí dự kiến / vị trí thực', 'Vị trí nhập lúc tạo phiếu (dự kiến) và vị trí thủ kho nhập thực tế ở bước Nhập kho.'],
        ['Phiếu đi xếp hàng', 'Nhóm các dòng vị trí giao cho 1 người đi xếp (thủ kho), in phiếu xếp hàng.'],
        ['Tiến trình', 'Đang đi xếp hàng → Đang nhập kho → Hoàn thành nhập kho.'],
        ['Lưu và nhập', 'Gửi phiếu: ghi tồn kho và chuyển Chờ duyệt.'],
        ['Phiếu xuất lại (PXL)', 'Phiếu xuất toàn bộ hàng của phiếu nhập kho bị Không duyệt ra khỏi kho.'],
        ['Phiếu nhập lại', 'Phiếu nhập kho mới lập cho phiếu đã xuất lại.'],
    ],
    'trang_thai': {
        'cau_dan': 'Phiếu có 8 trạng thái và cột Tiến trình (bước thủ kho). Phiếu chỉ ghi tồn kho ở thao tác "Lưu và nhập" '
                   '(Đang tạo → Chờ duyệt); kế toán kho duyệt bằng cách lập Phiếu nhập hàng.',
        'rows': [
            ['Đang tạo – Đang đi xếp hàng', 'Mới tạo từ đề nghị nhập kho, vị trí dự kiến; chưa ghi tồn.', 'Xem, Phiếu xếp hàng, Nhập kho, Hủy, In phiếu, Lịch sử', 'Thủ kho kho nhập tạo; người tạo thao tác'],
            ['Đang tạo – Đang nhập kho', 'Đã bấm Lưu ở bước Nhập kho; chưa ghi tồn.', 'Xem, Sửa phiếu, Lưu và nhập, Hủy, In phiếu, In barcode, Lịch sử', 'Người tạo phiếu'],
            ['Chờ duyệt', 'Đã Lưu và nhập: tồn kho đã cộng, chờ kế toán kho.', 'Xem, Tạo phiếu nhập hàng, Không duyệt, In, In barcode, Lịch sử', 'Kế toán kho cùng công ty'],
            ['Đang hạch toán', 'Kế toán kho đã lập phiếu nhập hàng.', 'Xem, In, In barcode, Lịch sử', 'Tự chuyển khi lưu phiếu nhập hàng'],
            ['Đã hạch toán', 'Phiếu nhập hàng đã hoàn thành.', 'Xem, In, In barcode, Lịch sử', 'Tự chuyển khi phiếu nhập hàng hoàn thành'],
            ['Không duyệt', 'Kế toán kho từ chối (có lý do); tồn vẫn còn.', 'Xem, Tạo phiếu xuất lại, In, In barcode, Lịch sử', 'Kế toán kho; người tạo xuất lại'],
            ['Đã xuất lại', 'Đã trừ toàn bộ hàng khỏi kho qua phiếu xuất lại.', 'Xem, Tạo phiếu nhập lại, In, In barcode, Lịch sử', 'Người tạo phiếu'],
            ['Đã nhập lại', 'Đã lập phiếu nhập lại (phiếu mới).', 'Xem, In, In barcode, Lịch sử', 'Người tạo phiếu'],
            ['Đã hủy', 'Hủy khi còn Đang tạo; đề nghị nhập kho hủy theo.', 'Xem, In, Lịch sử', 'Người tạo phiếu'],
        ],
        'anh': 'state_flow',
        'ghi_chu': ['Phiếu nhập lại là phiếu MỚI, bắt đầu ở Đang tạo – Đang nhập kho rồi đi tiếp như phiếu thường. '
                    'Loại điều chuyển cùng thủ kho / kho nội bộ, nhập ghép, nhập tách không Không duyệt được; loại điều chuyển, '
                    'nhập ghép, nhập tách không Hủy được (BR-03).'],
    },
    'quyen_truoc': ['Màn KHÔNG có quyền riêng để vào (menu không ẩn theo quyền); thao tác do VAI TRÒ và trạng thái phiếu quyết định:'],
    'quyen_rows': [
        ['Thủ kho của kho nhập (khai ở danh mục kho)', 'Tạo phiếu từ đề nghị nhập kho Chờ duyệt của kho mình; được chọn làm người đi xếp.'],
        ['Người tạo phiếu', 'Phiếu xếp hàng, Nhập kho / Sửa phiếu, Lưu và nhập, Hủy (phiếu Đang tạo); Tạo phiếu xuất lại (Không duyệt); Tạo phiếu nhập lại (Đã xuất lại).'],
        ['Kế toán kho', 'Tạo phiếu nhập hàng, Không duyệt phiếu Chờ duyệt cùng công ty.'],
        ['Super admin', 'Tạo phiếu ở mọi kho, Nhập kho / Sửa mọi phiếu Đang tạo, xem mọi phiếu.'],
        ['Mọi người dùng trong phạm vi xem', 'Xem danh sách, chi tiết, lịch sử, in phiếu, in barcode, xuất Excel, cài đặt bộ lọc, tuỳ chỉnh cột.'],
    ],
    'pham_vi_truoc': ['Phạm vi dữ liệu (cộng dồn các điều kiện người dùng có):'],
    'pham_vi_rows': [
        ['1', 'Xem phiếu nhập kho theo tổng công ty (hoặc Super admin)', 'Phiếu của mọi công ty.'],
        ['2', 'Xem phiếu nhập kho theo công ty', 'Phiếu của công ty đang làm việc.'],
        ['3', 'Xem phiếu nhập kho theo phòng ban', 'Phiếu thuộc các phòng ban người dùng được giao quản lý.'],
        ['4', 'Xem tất cả phiếu xuất nhập kho', 'Phiếu của kho mà người dùng là thủ kho.'],
        ['5', 'Kế toán kho', 'Phiếu đã gửi (khác Đang tạo) của công ty đang làm việc.'],
        ['6', '(luôn có)', 'Phiếu do chính người dùng tạo.'],
    ],
    'pham_vi_sau': ['Phiếu Đang tạo của người khác KHÔNG hiện ở danh sách; riêng phiếu đang đi xếp hàng ai cũng mở được trang Chi tiết qua liên kết. '
                    'Tổ chức của phiếu chép từ đề nghị nhập kho lúc tạo. 3 quyền "Xem phiếu nhập kho theo …" nằm ở nhóm "Phiếu nhập kho" màn Phân quyền.'],
    'ma_tran': [['Chức năng'] + _VT] + [[f] + list(_MT[i]) for i, f in enumerate(FR_NAMES)],
    'ma_tran_widths': [2.4, 1.5, 1.5, 1.2],
    'quyen_sau': ['Mọi chức năng chỉ áp trên phiếu thuộc phạm vi dữ liệu ở trên; Super admin làm được mọi thao tác của thủ kho / người tạo.'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Hai bước thủ kho và tiến trình', ['– Tạo phiếu = vị trí dự kiến (Đang đi xếp hàng) → Phiếu xếp hàng (mọi dòng có người đi xếp) → Nhập kho (Đang nhập kho) → Lưu và nhập (Hoàn thành nhập kho).', '– Chưa xếp xong thì không nhập kho được.'], ['Tạo phiếu', 'Xếp hàng', 'Nhập kho']),
        ('BR-02', 'Phạm vi dữ liệu', ['– Cộng dồn: 3 quyền xem phiếu nhập kho, thủ kho (quyền xem tất cả phiếu xuất nhập kho), kế toán kho (phiếu đã gửi cùng công ty), phiếu mình tạo.', '– Phiếu Đang tạo của người khác ẩn khỏi danh sách.'], ['Mọi chức năng']),
        ('BR-03', 'Nút thao tác theo trạng thái và vai trò', ['– Hiện / ẩn theo Phần 1 mục 3; nút không dùng được thì ẩn.', '– Hệ thống chặn lại cả khi thao tác trực tiếp (vd "Bạn không có quyền sửa phiếu này.", "Không thể hủy phiếu này.").', '– Không duyệt: trừ loại điều chuyển cùng thủ kho, kho nội bộ, nhập ghép, nhập tách. Hủy: trừ loại điều chuyển (cùng thủ kho, nội bộ, chi nhánh, trả lại), nhập ghép, nhập tách.'], ['Mọi thao tác']),
        ('BR-04', 'Mã phiếu', ['– PNK-<5 chữ số> theo số thứ tự bản ghi (cùng dãy với hệ thống cũ). Phiếu xuất lại PXL-<5 chữ số>.'], ['Tạo phiếu', 'Nhập lại', 'Xuất lại']),
        ('BR-05', 'Tác động sang chứng từ nguồn', ['– Tạo phiếu = duyệt đề nghị nhập kho (→ Đang nhập kho), yêu cầu nhập hàng → Đang nhập kho.', '– Lưu và nhập: đề nghị → Đã nhập kho, yêu cầu nhập hàng → Đã nhập kho; loại mua ngoài cập nhật đơn đặt hàng gốc và trừ hàng đang về.', '– Hủy phiếu: đề nghị nhập kho bị hủy theo.'], ['Tạo phiếu', 'Nhập kho', 'Hủy']),
        ('BR-06', 'Ghi tồn kho', ['– Chỉ "Lưu và nhập" mới cộng tồn: tồn kho, tồn theo công ty, tồn vị trí, tồn lô tại vị trí + nhật ký; quy về ĐVT cơ bản theo hệ số.', '– Xuất lại trừ toàn bộ đúng lô, đúng vị trí; thiếu tồn ở bất kỳ lô nào thì không trừ gì.', '– Không duyệt KHÔNG hoàn tồn.'], ['Nhập kho', 'Xuất lại', 'Nhập lại']),
        ('BR-07', 'Duyệt qua Phiếu nhập hàng', ['– Kế toán kho lập phiếu nhập hàng từ phiếu Chờ duyệt → phiếu Đang hạch toán (ghi người duyệt, ngày duyệt); phiếu nhập hàng hoàn thành → Đã hạch toán.'], ['Tạo phiếu nhập hàng']),
        ('BR-08', 'Số lượng nhập', ['– SL nhập ≥ 0, ≤ 999,999; tổng các vị trí của 1 dòng không vượt SL đề nghị (điều chuyển kho chi nhánh: phải bằng).', '– Cả phiếu phải có ít nhất 1 hàng SL > 0.', '– Vị trí bắt buộc (bước nhập kho: chỉ khi SL > 0); 1 dòng hàng không chọn trùng vị trí.'], ['Tạo phiếu', 'Nhập kho', 'Nhập lại']),
        ('BR-09', 'Kiểm kho', ['– Hàng đang kiểm kho tại kho nhập hoặc vị trí đang trong kế hoạch / đợt kiểm kê thì không lưu được.'], ['Tạo phiếu', 'Nhập kho', 'Nhập lại']),
        ('BR-10', 'Vận chuyển', ['– Công ty vận chuyển: bắt buộc chuyến xe; bước nhập kho thêm Tuyến đường, Số km chốt (1–999,999), ghi chú khi km chốt ≠ km dự kiến.', '– Lưu và nhập chỉ khi mọi chuyến xe đã duyệt; chuyến đã duyệt không gỡ được.'], ['Tạo phiếu', 'Nhập kho']),
        ('BR-11', 'Bốc xếp', ['– Chọn Loại hình thuê thì Loại bốc xếp, Khối lượng / Số giờ (> 0) bắt buộc; Thuê ngoài cần Nhà cung cấp; Công ty cần ≥ 1 người nhận việc, tổng tiền chia = Số tiền bốc xếp.'], ['Tạo phiếu', 'Nhập kho']),
        ('BR-12', 'File đính kèm', ['– Bước nhập kho bắt buộc có ít nhất 1 file (pdf, jpeg, jpg, png, doc, csv, xlsx, xls, docx; ≤ 20MB/file); phiếu nhập lại phải chọn file mới.'], ['Nhập kho', 'Nhập lại']),
        ('BR-13', 'Thông báo', ['– Tạo phiếu: báo người lập đề nghị và yêu cầu nhập hàng. Lưu và nhập: báo kế toán kho của kho. Không duyệt: báo người tạo. Hủy: báo người lập đề nghị.'], ['Tạo phiếu', 'Nhập kho', 'Không duyệt', 'Hủy']),
        ('BR-14', 'Thao tác xong quay về danh sách', ['– Lưu (tạo / nhập kho / nhập lại), Không duyệt, Hủy ở trang Chi tiết xong thì về danh sách; "Lưu và tiếp tục" ở lại form trống.'], ['Tạo phiếu', 'Nhập kho', 'Không duyệt', 'Hủy']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây đọc hoặc dùng dữ liệu do Phiếu nhập kho ghi ra (phiếu, lô nhập, tồn kho, chuyến xe, bốc xếp).',
        'rows': P5,
    },
}

UML = {
    'actor': 'Thủ kho / Kế toán kho',
    'mains': [('FR-01', 'Xem danh sách phiếu nhập kho', 'view'), ('FR-04', 'Tạo phiếu nhập kho', 'crud'),
              ('FR-06', 'Lập phiếu đi xếp hàng', 'crud'), ('FR-07', 'Nhập kho (Lưu và nhập)', 'crud'),
              ('FR-09', 'Hủy phiếu', 'action'), ('FR-10', 'Không duyệt', 'action'), ('FR-11', 'Tạo phiếu nhập hàng', 'action'),
              ('FR-12', 'Tạo phiếu xuất lại', 'action'), ('FR-13', 'Tạo phiếu nhập lại', 'crud'),
              ('FR-14', 'In phiếu nhập kho', 'io'), ('FR-15', 'In barcode', 'io'), ('FR-16', 'Xuất Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc', 'view'), ('FR-03', 'Cài đặt bộ lọc, tuỳ chỉnh cột', 'view'),
             ('FR-08', 'Xem chi tiết', 'view'), ('FR-17', 'Xem lịch sử thay đổi', 'view')],
    'rieng': [('FR-04', 'Tạo phiếu nhập kho', 'crud', 'uc_them'), ('FR-05', 'Chọn đề nghị nhập kho, vị trí', 'crud', 'uc_chon'),
              ('FR-06', 'Lập phiếu đi xếp hàng', 'crud', 'uc_xephang'), ('FR-07', 'Nhập kho (Lưu và nhập)', 'crud', 'uc_nhapkho'),
              ('FR-08', 'Xem chi tiết', 'view', 'uc_xem'), ('FR-09', 'Hủy phiếu', 'action', 'uc_huy'),
              ('FR-10', 'Không duyệt', 'action', 'uc_khongduyet'), ('FR-11', 'Tạo phiếu nhập hàng', 'action', 'uc_taopnh'),
              ('FR-12', 'Tạo phiếu xuất lại', 'action', 'uc_xuatlai'), ('FR-13', 'Tạo phiếu nhập lại', 'crud', 'uc_nhaplai'),
              ('FR-14', 'In phiếu nhập kho', 'io', 'uc_in'), ('FR-15', 'In barcode', 'io', 'uc_barcode'),
              ('FR-16', 'Xuất Excel', 'io', 'uc_xuat')],
}

STATES = [('start', '', None), ('tao', 'Đang tạo', '#e5e7eb'), ('cho', 'Chờ duyệt', '#fef3c7'),
          ('dht', 'Đang hạch toán', '#ffedd5'), ('ht', 'Đã hạch toán', '#ccfbf1'),
          ('kd', 'Không duyệt', '#fee2e2'), ('xl', 'Đã xuất lại', '#ede9fe'), ('nl', 'Đã nhập lại', '#e0e7ff'),
          ('huy', 'Đã hủy', '#fecaca')]
TRANS = [('start', 'tao', 'Tạo từ đề nghị'), ('tao', 'cho', 'Lưu và nhập'), ('cho', 'dht', 'Lập phiếu nhập hàng'),
         ('dht', 'ht', 'Phiếu nhập hàng xong'), ('cho', 'kd', 'Không duyệt'), ('kd', 'xl', 'Xuất lại'), ('xl', 'nl', 'Nhập lại'),
         ('tao', 'huy', 'Hủy')]


def draw_state_flow_2rows(path):
    """Sơ đồ 2 hàng (luồng chính trên, nhánh Hủy / Không duyệt dưới) — lib chung chỉ vẽ 1 hàng nên quá dẹt với 8 trạng thái."""
    from PIL import Image, ImageDraw, ImageFont
    fdir = os.path.join(os.environ.get('WINDIR', 'C:/Windows'), 'Fonts')
    fb = ImageFont.truetype(os.path.join(fdir, 'timesbd.ttf'), 40)
    fl = ImageFont.truetype(os.path.join(fdir, 'times.ttf'), 32)
    W, H = 2500, 900
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    bw, bh = 300, 110
    xs = [430, 1000, 1570, 2140]
    y1, y2 = 220, 640
    box = {}

    def rect(k, cx, cy, label, color):
        x0, y0 = cx - bw / 2, cy - bh / 2
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=26, fill=color, outline='#334155', width=3)
        d.text((cx - d.textlength(label, font=fb) / 2, cy - 24), label, font=fb, fill='#0f172a')
        box[k] = (x0, y0, x0 + bw, y0 + bh)

    def arrow(p, direction, color):
        x, y = p
        s = 16
        pts = {'r': [(x, y), (x - 26, y - s), (x - 26, y + s)], 'd': [(x, y), (x - s, y - 26), (x + s, y - 26)]}[direction]
        d.polygon(pts, fill=color)

    def hline(a, b, label, color='#475569'):
        ax1, ay0, _, ay1 = box[a][2], box[a][1], box[a][2], box[a][3]
        bx0 = box[b][0]
        y = (ay0 + ay1) / 2
        d.line([(ax1 + 4, y), (bx0 - 6, y)], fill=color, width=4)
        arrow((bx0 - 6, y), 'r', color)
        lines = L._wrap(d, label, fl, bx0 - ax1 - 20)
        for k, t in enumerate(lines):
            d.text(((ax1 + bx0) / 2 - d.textlength(t, font=fl) / 2, y - 14 - 36 * (len(lines) - k)), t, font=fl, fill='#1e3a8a')

    def vline(a, b, label, color='#b91c1c'):
        x = (box[a][0] + box[a][2]) / 2
        d.line([(x, box[a][3] + 4), (x, box[b][1] - 8)], fill=color, width=4)
        arrow((x, box[b][1] - 8), 'd', color)
        d.text((x + 16, (box[a][3] + box[b][1]) / 2 - 18), label, font=fl, fill='#991b1b')

    rect('tao', xs[0], y1, 'Đang tạo', '#e5e7eb')
    rect('cho', xs[1], y1, 'Chờ duyệt', '#fef3c7')
    rect('dht', xs[2], y1, 'Đang hạch toán', '#ffedd5')
    rect('ht', xs[3], y1, 'Đã hạch toán', '#ccfbf1')
    rect('huy', xs[0], y2, 'Đã hủy', '#fecaca')
    rect('kd', xs[1], y2, 'Không duyệt', '#fee2e2')
    rect('xl', xs[2], y2, 'Đã xuất lại', '#ede9fe')
    rect('nl', xs[3], y2, 'Đã nhập lại', '#e0e7ff')
    # chấm đầu
    d.ellipse([80, y1 - 22, 124, y1 + 22], fill='#111827')
    d.line([(128, y1), (box['tao'][0] - 6, y1)], fill='#475569', width=4)
    arrow((box['tao'][0] - 6, y1), 'r', '#475569')
    for k, t in enumerate(['Tạo từ', 'đề nghị']):
        d.text((150, y1 - 86 + 36 * k), t, font=fl, fill='#1e3a8a')
    hline('tao', 'cho', 'Lưu và nhập')
    hline('cho', 'dht', 'Lập phiếu nhập hàng')
    hline('dht', 'ht', 'Phiếu nhập hàng xong')
    hline('kd', 'xl', 'Xuất lại', '#b45309')
    hline('xl', 'nl', 'Nhập lại (phiếu mới)', '#b45309')
    vline('tao', 'huy', 'Hủy')
    vline('cho', 'kd', 'Không duyệt')
    d.text((W / 2 - d.textlength('Tiến trình trong Đang tạo: Đang đi xếp hàng → Đang nhập kho; Lưu và nhập = Hoàn thành nhập kho, cộng tồn', font=fl) / 2, 790),
           'Tiến trình trong Đang tạo: Đang đi xếp hàng → Đang nhập kho; Lưu và nhập = Hoàn thành nhập kho, cộng tồn', font=fl, fill='#334155')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return path


if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    draw_state_flow_2rows(os.path.join(scr.uml, 'state_flow.png'))
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))

# -*- coding: utf-8 -*-
"""SRS - Khai báo đầu kỳ công nợ nhà cung cấp (STT 168) — chép khuôn màn mẫu ../kh/gen_srs.py (đã duyệt), đổi dữ liệu.

Nguồn (code HRM develop, 02/11/2026):
  FE hrm-client/components/finance/declare-debt/{DeclareDebtList, DeclareDebtForm, DeclareDebtContractPicker}.vue,
     utils/finance/declareDebtConfigs.js (cấu hình `supplier`), pages/finance/declare-debt-supplier-beginnings/**,
     components/subsystem-menu/finance.js
  BE Modules/Finance: Services/DeclareDebt/{AbstractDeclareDebtService, DeclareDebtSupplierBeginningService,
     DeclareDebtPostingService, DeclareDebtContractRegistry}.php, Http/Controllers/V1/{AbstractDeclareDebtController,
     DeclareDebtSupplierBeginningController}.php, Http/Requests/DeclareDebt/DeclareDebtSupplierRequest.php,
     Entities/Contract/{DeclareDebtSupplierBeginning, Concerns/DeclareDebtCommon}.php; app/Services/CatalogHistoryService.php
  Ảnh: capture.js (dev-hrm). Phần 5: dò code FE/BE 02/11/2026.
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402
from _lib_phieu import ui, UI4, UI4W, UI6, UI6W, UI7, UI7W, UI8, UI8W, TRUOC_LUU  # noqa: E402

TEN = 'Khai báo đầu kỳ công nợ nhà cung cấp'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q_THEM = 'Khai báo thêm công nợ đầu kỳ nhà cung cấp'
Q_SUA = 'Khai báo sửa công nợ đầu kỳ nhà cung cấp'
Q_XOA = 'Khai báo xoá công nợ đầu kỳ nhà cung cấp'
Q_XEM = 'Người dùng đăng nhập hệ thống (xem không cần quyền riêng, dữ liệu theo phạm vi xem)'
QT = 'Người dùng có quyền "%s"' % Q_THEM
QS = 'Người dùng có quyền "%s"' % Q_SUA
QX = 'Người dùng có quyền "%s"' % Q_XOA
DK = '1. Người dùng đăng nhập thành công.'
DK_THEM = DK + '\n2. Người dùng có quyền "%s".' % Q_THEM
DK_SUA = DK + '\n2. Người dùng có quyền "%s".\n3. Khai báo ở trạng thái Chưa phát sinh chứng từ và thuộc phạm vi dữ liệu của người dùng.' % Q_SUA
DK_XOA = DK + '\n2. Người dùng có quyền "%s".\n3. Khai báo ở trạng thái Chưa phát sinh chứng từ và thuộc phạm vi dữ liệu của người dùng.' % Q_XOA
TRANG = 'Trang %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'
POPUP = 'Modal %s được mở ngay trên màn hình %s theo đường dẫn ở trên.'

# ------------------------------------------------------------------ Phần 5 (dò code 02/11/2026)
TIEN = 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'
P5 = [
    ('Tài chính', 'Phiếu chi (trả nợ nhà cung cấp: chứng từ ghi sổ cùng nhà cung cấp + hợp đồng + tài khoản làm khai báo chuyển Đã phát sinh)', TIEN),
    ('Tài chính', 'Phiếu ủy nhiệm chi (trả nợ nhà cung cấp qua ngân hàng — tác động như Phiếu chi)', TIEN),
    ('Tài chính', 'Phiếu thu, Phiếu báo có (nhà cung cấp hoàn tiền — tác động như Phiếu chi)', TIEN),
    ('Tài chính', 'Phiếu kế toán (bù trừ / điều chỉnh công nợ đầu kỳ nhà cung cấp)', 'Tài chính => Sổ tổng hợp => Sổ tổng hợp'),
    ('Tài chính', 'Danh mục tài khoản (tài khoản đã dùng trong khai báo không xóa được)', 'Tài chính => Danh mục'),
    ('Tài chính', 'Danh mục tiền tệ (loại tiền đã dùng trong khai báo không xóa được)', 'Tài chính => Danh mục'),
    ('Tài chính', 'Khai Quy chế – Cấu hình (khóa "Ngày khai báo đầu kỳ" khi công ty đã có khai báo)', 'Tài chính => Khai Quy chế – Cấu hình'),
    ('Bán hàng', 'Chi tiết công nợ KH (cửa sổ chứng từ của cột Điều chỉnh công nợ liệt kê khai báo Dư nợ; bấm mã mở chi tiết khai báo)',
     'Bán hàng => Báo cáo => Báo cáo công nợ'),
    ('Bán hàng', 'Đối chiếu công nợ 1 KH (liên kết mã khai báo mở trang chi tiết khai báo)', 'Bán hàng => Báo cáo => Báo cáo công nợ'),
]

FR = []

# 2.1 Xem danh sách -------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách khai báo đầu kỳ công nợ nhà cung cấp',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách khai báo đầu kỳ công nợ nhà cung cấp'],
        ['Mô tả', 'Hiển thị các khai báo công nợ đầu kỳ (mỗi dòng = 1 hợp đồng mua × 1 tài khoản của 1 nhà cung cấp) trong phạm vi dữ liệu của người dùng, có phân trang, sắp xếp và nút thao tác theo từng dòng.'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), khai báo tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Không có khai báo khớp → bảng hiện "Không có dữ liệu phù hợp bộ lọc."\n• Phạm vi dữ liệu theo quyền xem (Phần 2, BR-02); không có quyền phạm vi nào chỉ thấy khai báo mình tạo.\n• Nút Tạo mới, Import Excel chỉ hiện khi có quyền thêm; Sửa / Xóa theo quyền sửa / xóa và chỉ với khai báo Chưa phát sinh chứng từ (BR-05, BR-13).'],
    ],
    'anh': [('01_list', 'Màn danh sách Khai báo đầu kỳ công nợ nhà cung cấp lúc mới truy cập'),
            ('01b_list_actions', 'Cột Hành động: dòng Chưa phát sinh có Sửa, Xóa, Lịch sử; dòng Đã phát sinh (dòng 6) chỉ có Lịch sử')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Khai báo đầu kỳ công nợ nhà cung cấp', 'Tiêu đề khối danh sách và tiêu đề trang.'],
        ['Nút Tạo mới', 'Button', 'Enable / Ẩn', 'Theo quyền', 'Chỉ hiện khi có quyền "%s". Mở trang "Thêm khai báo đầu kỳ công nợ nhà cung cấp" (mục 2.4).' % Q_THEM],
        ['Nút Import Excel', 'Button', 'Enable / Ẩn', 'Theo quyền', 'Chỉ hiện khi có quyền "%s". Mở cửa sổ "Import khai báo đầu kỳ công nợ nhà cung cấp" (mục 2.11).' % Q_THEM],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất file" (mục 2.10). Trong lúc xuất, cạnh nút hiện dòng tiến độ.'],
        ['Nút In danh sách', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ xem trước bản in danh sách (mục 2.9).'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.3).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa, không ẩn được.'],
        ['Cột Mã phiếu', 'Table/Grid', 'Read-only', 'Hiển thị', '- Dạng <mã công ty>_DKNCC_<5 chữ số> (BR-03).\n- Sắp xếp được. Chữ dạng liên kết: bấm mở trang Chi tiết (mục 2.7), chuột phải mở tab mới được.\n- Cột khóa, không ẩn được.'],
        ['Cột Nhà cung cấp', 'Table/Grid', 'Read-only', 'Hiển thị', '"Mã - Tên nhà cung cấp".'],
        ['Cột Tài khoản', 'Table/Grid', 'Read-only', 'Ẩn', '"Số hiệu - Tên tài khoản". Mặc định ẩn, bật ở Tuỳ chỉnh cột.'],
        ['Cột Loại hợp đồng', 'Table/Grid', 'Read-only', 'Ẩn', 'Hợp đồng mua nước ngoài / mua ngoài / mua trong nước / mua đầu kỳ. Mặc định ẩn.'],
        ['Cột Số hợp đồng', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng liên kết: mở chứng từ hợp đồng mua ở tab mới (hợp đồng chưa có trang xem thì là chữ thường).'],
        ['Cột Người lập hợp đồng', 'Table/Grid', 'Read-only', 'Ẩn', '"Mã nhân viên - Họ tên" người lập hợp đồng. Mặc định ẩn.'],
        ['Cột Loại tiền', 'Table/Grid', 'Read-only', 'Hiển thị', 'Mã loại tiền (VNĐ, USD…), căn giữa.'],
        ['Cột Tỷ giá', 'Table/Grid', 'Read-only', 'Ẩn', 'Định dạng 1,234,567.89, căn phải. Mặc định ẩn.'],
        ['Cột Dư nợ', 'Table/Grid', 'Read-only', 'Hiển thị', 'Công nợ (nguyên tệ) khi Loại dư = Dư nợ; dòng Dư có để trống. Định dạng 1,234,567.89, căn phải.'],
        ['Cột Dư có', 'Table/Grid', 'Read-only', 'Hiển thị', 'Công nợ (nguyên tệ) khi Loại dư = Dư có; dòng Dư nợ để trống.'],
        ['Cột Quy đổi (VND)', 'Table/Grid', 'Read-only', 'Ẩn', 'Công nợ × Tỷ giá, làm tròn đến đồng. Mặc định ẩn.'],
        ['Cột Người cập nhật, Ngày cập nhật', 'Table/Grid', 'Read-only', 'Ẩn', '"Họ tên - Mã phòng ban"; dd/mm/yyyy hh:mm, sắp xếp được. Mặc định ẩn.'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', '"Họ tên - Mã phòng ban".'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sửa: có quyền sửa và khai báo Chưa phát sinh chứng từ.\n- Xóa: có quyền xóa và khai báo Chưa phát sinh chứng từ.\n- Lịch sử: luôn có.\n- Nút không dùng được thì ẩn, không làm mờ. Cột khóa.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Người dùng đã đăng nhập (màn không yêu cầu quyền riêng để xem, mục menu luôn hiện).\nAfter:\n– Tải trang 1 theo phạm vi dữ liệu (BR-02), khai báo tạo gần nhất trên cùng; khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút).\n– Tính nút Tạo mới / Import theo quyền thêm, Sửa / Xóa từng dòng theo quyền và trạng thái.'],
        ['Bấm tiêu đề cột Mã phiếu / Ngày tạo / Ngày cập nhật', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại dữ liệu.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp, tải lại dữ liệu; đổi số dòng thì quay về trang 1.'],
        ['Bấm Mã phiếu', 'Click', 'After:\n– Mở trang Chi tiết khai báo (mục 2.7).'],
        ['Bấm Số hợp đồng', 'Click', 'After:\n– Mở chứng từ hợp đồng mua ở tab mới.'],
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc danh sách',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách khai báo'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao.'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô gõ chữ (tìm nhanh, Số hợp đồng) chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Bấm Làm mới → xoá mọi điều kiện và tải lại danh sách.\n• Ô Công ty / Phòng ban chỉ hiện theo phạm vi xem của người dùng (BR-02); màn này không có ô Bộ phận.\n• Hệ thống ghi nhớ bộ lọc 10 phút khi rời màn rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực Tìm kiếm nâng cao ở trạng thái mở')],
    'ui': ui(UI7, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', '- Placeholder "Tìm theo mã phiếu, số hợp đồng, mã hoặc tên nhà cung cấp".\n- Tìm gần đúng theo Mã phiếu, Số hợp đồng, mã / tên nhà cung cấp.'],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Áp dụng từ khóa và các ô lọc.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá mọi điều kiện lọc và tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực ô lọc (khi mở, nút đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" (mục 2.3).'],
        ['Ô Nhà cung cấp', 'Dropdown', 'Enable', 'Gõ ≥ 2 ký tự để tìm', 'Trống', 'Tìm nhà cung cấp đang hoạt động theo mã, tên, số điện thoại; hiển thị "Mã - Tên". Tải lại trang vẫn giữ tên đã chọn.'],
        ['Ô Tài khoản', 'Dropdown', 'Enable', 'Tài khoản chi tiết theo dõi công nợ', 'Trống', 'Lọc theo tài khoản của khai báo.'],
        ['Ô Số hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Tìm gần đúng số hợp đồng; lọc khi Enter / Tìm kiếm.'],
        ['Ô Người lập hợp đồng', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc khai báo có hợp đồng do người được chọn lập.'],
        ['Ô Người tạo / Người cập nhật', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc khai báo do người được chọn tạo / cập nhật lần cuối.'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy, Từ → Đến', 'Trống', 'Lọc theo ngày tạo khai báo, tính cả 2 đầu mút.'],
        ['Ô Công ty – Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Theo phạm vi xem', 'Trống', '- Công ty: chỉ khi có quyền xem tất cả.\n- Phòng ban: chọn Công ty trước thì mới mở (người có phạm vi công ty / phòng ban thấy ngay).\n- Lọc theo tổ chức của khai báo (= tổ chức của người lập hợp đồng, BR-04).'],
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
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Bấm "Cài đặt bộ lọc" (hoặc biểu tượng Cấu hình cột hiển thị).\n2. Tích / bỏ tích, kéo ☰ để đổi thứ tự.\n3. Bấm Lưu: hệ thống lưu cấu hình và áp dụng ngay.'],
        ['Dòng sự kiện phụ', '• Bấm Đóng: bỏ thay đổi.\n• Cài đặt bộ lọc có nút "Khôi phục mặc định".\n• Cột STT, Mã phiếu, Hành động không bỏ được (có biểu tượng khóa).'],
    ],
    'menu_them': ' => Cài đặt bộ lọc {icon:btn_caidatboloc} / Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': 'Modal Cài đặt bộ lọc và Modal Tuỳ chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('26_filtercfg', 'Cửa sổ Cài đặt bộ lọc'), ('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột')],
    'ui': ui(UI6, [
        ['Danh sách ô lọc', 'Checkbox', 'Enable', 'Đủ 8 ô', 'Nhà cung cấp, Tài khoản, Số hợp đồng, Người lập hợp đồng, Người tạo, Người cập nhật, Ngày tạo, Công ty – Phòng ban. Kéo ☰ đổi thứ tự.'],
        ['Nút Khôi phục mặc định', 'Button', 'Enable', '–', 'Đưa cấu hình ô lọc về mặc định.'],
        ['Danh sách cột', 'Checkbox', 'Enable', '10/17 cột', 'Tích cột muốn hiện; STT, Mã phiếu, Hành động bị khóa. Kéo ☰ đổi thứ tự. Dòng đếm "Đang chọn x/17 cột".'],
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
    'ten': 'Lập khai báo đầu kỳ công nợ nhà cung cấp', 'uc': 'uc_them', 'uc_ten': 'FR-04 Lập khai báo đầu kỳ công nợ nhà cung cấp',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Lập khai báo đầu kỳ công nợ nhà cung cấp'],
        ['Mô tả', 'Chọn 1 nhà cung cấp rồi chọn một hoặc nhiều hợp đồng mua; mỗi dòng hợp đồng nhập Tài khoản, Loại tiền, Tỷ giá, Loại dư, Công nợ (nguyên tệ). Lưu xong mỗi dòng thành 1 khai báo riêng (1 mã phiếu, 1 bút toán sổ chi tiết) và có hiệu lực ngay, không qua duyệt.'],
        ['Tác nhân', QT],
        ['Điều kiện ban đầu', DK_THEM],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở trang "Thêm khai báo đầu kỳ công nợ nhà cung cấp"; góc phải khối Thông tin chung hiện "<Người đăng nhập> - <ngày giờ hiện tại>".\n3. Người dùng chọn Nhà cung cấp, bấm "Chọn hợp đồng" và chọn hợp đồng (mục 2.5).\n4. Hệ thống thêm dòng, tự điền Loại hợp đồng, Số hợp đồng, Người lập hợp đồng, Loại tiền theo hợp đồng, Tỷ giá theo danh mục tiền tệ, Loại dư = Dư nợ, Tài khoản theo dòng phía trên.\n5. Mỗi dòng nhập / sửa Tài khoản, Loại tiền, Tỷ giá, Loại dư, Công nợ; cột Quy đổi (VND) tự tính.\n6. Bấm Lưu.\n7. Hệ thống kiểm tra dữ liệu, sinh mã phiếu cho từng dòng (BR-03), ghi khai báo với tổ chức = của người lập hợp đồng (BR-04), ghi 1 bút toán sổ chi tiết cho mỗi dòng (BR-06).\n8. Ghi nhận Tạo mới trong lịch sử của từng khai báo.\n9. Báo "Thêm mới thành công.", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Bấm "Lưu và tiếp tục": lưu như trên rồi mở lại trang Thêm trống để lập tiếp.\n• Thiếu / sai dữ liệu → báo đỏ dưới ô của đúng dòng + toast "Bạn chưa nhập đầy đủ thông tin.", cuộn tới ô lỗi đầu tiên, không lưu dòng nào.\n• Trùng khai báo đã có (cùng nhà cung cấp + hợp đồng + tài khoản) → dưới ô Tài khoản "Đã khai báo đầu kỳ cho tài khoản này" (BR-07).\n• Chọn tài khoản ở 1 dòng → các dòng chưa có tài khoản được điền theo.\n• Đổi Nhà cung cấp → bảng hợp đồng bị xoá trắng.\n• Bấm nút xoá ở cuối dòng → bỏ dòng khỏi bảng.\n• Bấm Quay lại: chưa nhập gì thì về danh sách; đã nhập thì hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', 'Nút Lưu bị khóa ngay khi bấm cho tới khi có kết quả, tránh lưu 2 lần; 2 lần lưu cùng lúc cho cùng nhà cung cấp được xếp hàng, lần sau bị chặn trùng.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': TRANG % '"Thêm khai báo đầu kỳ công nợ nhà cung cấp"',
    'anh': [('10_create', 'Trang Thêm khai báo đầu kỳ công nợ nhà cung cấp lúc mới mở'),
            ('11_no_supplier', 'Bấm "Chọn hợp đồng" khi chưa chọn nhà cung cấp'),
            ('10b_create_filled', 'Trang Thêm đã chọn 2 hợp đồng mua (USD và VNĐ) và nhập thông tin từng dòng'),
            ('18_unsaved', 'Hộp xác nhận Thông tin chưa lưu khi bấm Quay lại')],
    'ui': ui(UI8, [
        ['Người tạo - ngày giờ', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại', 'Góc phải khối Thông tin chung.'],
        ['Nhà cung cấp', 'Dropdown', 'Enable', 'Nhà cung cấp đang hoạt động, gõ ≥ 2 ký tự', 'Có', 'Trống', '- Placeholder "Chọn nhà cung cấp"; tìm theo mã, tên, số điện thoại.\n- Bỏ trống mà bấm "Chọn hợp đồng": "Chọn nhà cung cấp trước khi chọn hợp đồng".'],
        ['Nút Chọn hợp đồng', 'Button', 'Enable', '–', '–', '–', 'Mở cửa sổ chọn hợp đồng mua (mục 2.5).'],
        ['Bảng Danh sách hợp đồng mua', 'Table/Grid', 'Enable', '≥ 1 dòng', 'Có', 'Trống', '- Trống: "Chưa chọn hợp đồng nào — bấm "Chọn hợp đồng" để thêm."\n- Lưu khi chưa có dòng nào: "Phải chọn ít nhất 1 hợp đồng".'],
        ['Cột Loại hợp đồng, Số hợp đồng, Người lập hợp đồng', 'Table/Grid', 'Read-only', '–', '–', 'Theo hợp đồng đã chọn', 'Số hợp đồng là liên kết mở chứng từ ở tab mới; Người lập hợp đồng dạng "Mã nhân viên - Họ tên".'],
        ['Tài khoản', 'Dropdown', 'Enable', 'Tài khoản chi tiết theo dõi công nợ, đang hoạt động', 'Có', 'Theo dòng phía trên (dòng đầu: trống)', '"Số hiệu - Tên"; bỏ trống: "Bắt buộc phải nhập"; tài khoản không hợp lệ: "Tài khoản không hợp lệ".'],
        ['Loại tiền', 'Dropdown', 'Enable', 'Tiền tệ đang hoạt động (luôn có VNĐ)', 'Có', 'Loại tiền của hợp đồng (không có thì VNĐ)', 'Đổi sang VNĐ: Tỷ giá về 1 và khóa; đổi sang ngoại tệ: Tỷ giá lấy theo danh mục tiền tệ (BR-08).'],
        ['Tỷ giá', 'Textbox', 'Enable / Disable', 'Số > 0, tối đa 4 chữ số thập phân', 'Có khi khác VNĐ', '1 (VNĐ) / tỷ giá danh mục', 'VNĐ: khóa, luôn 1. Khác VNĐ bỏ trống: "Bắt buộc phải nhập"; ≤ 0: báo phải lớn hơn 0.'],
        ['Loại dư', 'Dropdown', 'Enable', 'Dư nợ / Dư có', 'Có', 'Dư nợ', '–'],
        ['Công nợ', 'Textbox', 'Enable', 'Số > 0, tối đa 2 chữ số thập phân', 'Có', 'Trống', 'Số tiền NGUYÊN TỆ. Bỏ trống: "Bắt buộc phải nhập"; ≤ 0: "Phải lớn hơn 0". Hiển thị 1,234,567.89.'],
        ['Quy đổi (VND)', 'Label', 'Read-only', '–', '–', 'Tự tính', 'Công nợ × Tỷ giá, làm tròn đến đồng.'],
        ['Nút xoá dòng', 'Button', 'Enable', '–', '–', '–', 'Bỏ dòng khỏi bảng (lỗi của các dòng còn lại giữ đúng dòng).'],
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi về danh sách.'],
        ['Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi mở lại trang Thêm trống.'],
        ['Nút Quay lại', 'Button', 'Enable', '–', '–', '–', 'Về danh sách (đã nhập thì hỏi "Thông tin chưa lưu").'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'Before:\n– Kiểm tra quyền "%s" (thiếu quyền thì nút ẩn; mở thẳng trang Thêm thì chuyển trang "Không tìm thấy").\nAfter:\n– Mở trang Thêm trống.' % Q_THEM],
        ['Chọn Nhà cung cấp', 'Change', 'After:\n– Bỏ lỗi dưới ô; nếu bảng đã có hợp đồng thì xoá trắng bảng.'],
        ['Chọn Tài khoản ở 1 dòng', 'Change', 'After:\n– Điền cùng tài khoản cho các dòng chưa có tài khoản.'],
        ['Đổi Loại tiền', 'Change', 'After:\n– VNĐ: Tỷ giá = 1, khóa ô; ngoại tệ: Tỷ giá = tỷ giá danh mục tiền tệ (sửa được); Quy đổi tính lại.'],
        ['Bấm Lưu / Lưu và tiếp tục', 'Click', 'Before:\n– Kiểm tra quyền "%s".\nDuring:\n– Có ít nhất 1 dòng; mỗi dòng: Tài khoản thuộc danh sách chọn được, Loại tiền có trong danh mục, Tỷ giá > 0 khi khác VNĐ, Loại dư hợp lệ, Công nợ > 0; hợp đồng tồn tại và thuộc 4 loại hợp đồng mua; không trùng dòng khác trên form ("Trùng với dòng n") và không trùng khai báo đã có (BR-07).\n' % Q_THEM + TRUOC_LUU + '\nAfter:\n– Mỗi dòng: sinh mã phiếu, ghi khai báo (Ngày tính công nợ = Ngày khai báo đầu kỳ cấu hình của công ty), lưu người lập hợp đồng, ghi 1 bút toán sổ chi tiết.\n– Ghi nhận Tạo mới trong lịch sử.\n– Báo "Thêm mới thành công."; Lưu → về danh sách, Lưu và tiếp tục → trang Thêm trống.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa nhập gì → về danh sách.\n– Đã nhập → hộp "Thông tin chưa lưu" ("Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"): Thoát thì về danh sách không lưu, Ở lại thì quay về form.'],
    ],
})

# 2.5 Chọn hợp đồng ------------------------------------------------------------
FR.append({
    'ten': 'Chọn hợp đồng mua', 'uc': 'uc_chonhd', 'uc_ten': 'FR-05 Chọn hợp đồng mua của nhà cung cấp',
    'qtc': 'Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chọn hợp đồng nhà cung cấp'],
        ['Mô tả', 'Cửa sổ liệt kê hợp đồng mua từ 4 nguồn: hợp đồng mua nước ngoài, mua ngoài, mua trong nước, mua đầu kỳ — mọi trạng thái (BR-09). Ô Phạm vi chọn hợp đồng của nhà cung cấp đang chọn hoặc của nhà cung cấp khác. Bấm vào dòng là thêm ngay vào form, cửa sổ vẫn mở để chọn tiếp.'],
        ['Tác nhân', QT],
        ['Điều kiện ban đầu', DK_THEM + '\n3. Đang ở trang Thêm và đã chọn Nhà cung cấp.'],
        ['Dòng sự kiện chính', '1. Bấm "Chọn hợp đồng".\n2. Hệ thống mở cửa sổ "Chọn hợp đồng nhà cung cấp", dòng phụ ghi "Nhà cung cấp: <mã - tên>", Phạm vi = "HĐ nhà cung cấp hiện tại", tải trang 1 (10 dòng, mới nhất trên cùng).\n3. Người dùng lọc (nếu cần) và bấm vào dòng hợp đồng.\n4. Hệ thống thêm 1 dòng vào bảng form, báo "Đã thêm hợp đồng <số hợp đồng>", dòng trong cửa sổ chuyển "Đã chọn".\n5. Bấm Đóng để về form.'],
        ['Dòng sự kiện phụ', '• Phạm vi = "HĐ nhà cung cấp khác": bảng thêm cột Nhà cung cấp, chỉ hiện hợp đồng không thuộc nhà cung cấp đang chọn; vẫn chọn và lưu được.\n• Hợp đồng đã có khai báo của nhà cung cấp đang chọn: dòng mờ, Tình trạng "Đã khai báo", bấm không có tác dụng.\n• Hợp đồng đã có trên form: Tình trạng "Đã chọn", bấm lại không thêm trùng.\n• Xoá trắng ô Phạm vi = mặc định nhà cung cấp hiện tại.\n• Không có hợp đồng phù hợp: "Không có dữ liệu phù hợp."'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi} => Chọn hợp đồng {icon:btn_chonhd}',
    'ghi_chu_layout': POPUP % ('Chọn hợp đồng nhà cung cấp', 'Thêm khai báo'),
    'anh': [('14b_picker_selected', 'Cửa sổ Chọn hợp đồng nhà cung cấp: dòng "Đã chọn", dòng "Đã khai báo"'),
            ('14c_picker_other', 'Phạm vi "HĐ nhà cung cấp khác": thêm cột Nhà cung cấp')],
    'ui': ui(UI8, [
        ['Ô Phạm vi', 'Dropdown', 'Enable', 'HĐ nhà cung cấp hiện tại / HĐ nhà cung cấp khác', 'Không', 'HĐ nhà cung cấp hiện tại', 'Chọn là lọc ngay.'],
        ['Ô Loại hợp đồng', 'Dropdown', 'Enable', '4 lựa chọn', 'Không', 'Trống', 'Hợp đồng mua nước ngoài, Hợp đồng mua ngoài, Hợp đồng mua trong nước, Hợp đồng mua đầu kỳ. Trống = cả 4 nguồn. Chọn là lọc ngay.'],
        ['Ô Số hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Placeholder "Nhập số hợp đồng"; tìm gần đúng; lọc khi Enter / Tìm kiếm.'],
        ['Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', '–', 'Áp dụng / xoá điều kiện lọc (Làm mới đưa Phạm vi về nhà cung cấp hiện tại).'],
        ['Cột STT, Loại hợp đồng, Số hợp đồng', 'Table/Grid', 'Read-only', '–', '–', '–', 'Thông tin hợp đồng.'],
        ['Cột Nhà cung cấp', 'Table/Grid', 'Read-only', '–', '–', '–', 'Chỉ hiện khi Phạm vi = HĐ nhà cung cấp khác.'],
        ['Cột Tổng thanh toán', 'Table/Grid', 'Read-only', '–', '–', '–', 'Giá trị hợp đồng (theo loại tiền của hợp đồng); hợp đồng mua đầu kỳ để trống.'],
        ['Cột Người tạo, Ngày tạo', 'Table/Grid', 'Read-only', '–', '–', '–', '"Họ tên - Mã phòng ban", dd/mm/yyyy.'],
        ['Cột Tình trạng', 'Table/Grid', 'Read-only', 'Đã khai báo / Đã chọn / trống', '–', '–', 'Dòng "Đã khai báo", "Đã chọn" không chọn được.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', '–', '10', '"Hiển thị a–b / N", chọn số dòng/trang.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ, giữ các hợp đồng đã chọn trên form.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Mở cửa sổ', 'System', 'Before:\n– Kiểm tra quyền "%s".\nAfter:\n– Tải hợp đồng mua theo phạm vi, đánh dấu Đã khai báo / Đã chọn.' % Q_THEM],
        ['Bấm vào dòng hợp đồng', 'Click', 'During:\n– Dòng Đã khai báo / Đã chọn: bỏ qua.\nAfter:\n– Thêm dòng vào bảng form (Loại dư = Dư nợ, Tài khoản theo dòng phía trên, Loại tiền theo hợp đồng, Tỷ giá theo danh mục tiền tệ, Người lập hợp đồng); báo "Đã thêm hợp đồng <số>".'],
        ['Đổi Phạm vi / Loại hợp đồng / bấm Tìm kiếm', 'Click', 'After:\n– Tải lại từ trang 1 theo điều kiện.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.6 Sửa -----------------------------------------------------------------------
FR.append({
    'ten': 'Sửa khai báo', 'uc': 'uc_sua', 'uc_ten': 'FR-06 Sửa khai báo đầu kỳ công nợ nhà cung cấp',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Sửa khai báo đầu kỳ công nợ nhà cung cấp'],
        ['Mô tả', 'Sửa 1 khai báo Chưa phát sinh chứng từ: chỉ đổi được Tài khoản, Loại tiền, Tỷ giá, Loại dư, Công nợ. Nhà cung cấp, hợp đồng và người lập hợp đồng cố định.'],
        ['Tác nhân', QS],
        ['Điều kiện ban đầu', DK_SUA],
        ['Dòng sự kiện chính', '1. Bấm Sửa ở cột Hành động (hoặc nút Sửa ở trang Chi tiết).\n2. Hệ thống mở trang "Sửa khai báo đầu kỳ công nợ nhà cung cấp" với đúng 1 dòng, ô Mã phiếu và Nhà cung cấp bị khóa.\n3. Người dùng sửa và bấm Lưu.\n4. Hệ thống kiểm tra, ghi thay đổi và cập nhật bút toán sổ chi tiết tương ứng (tài khoản, Nợ/Có, nguyên tệ, loại tiền, tỷ giá, quy đổi).\n5. Ghi nhận Thay đổi thông tin trong lịch sử.\n6. Báo "Cập nhật thành công.", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Đổi sang tài khoản đã khai báo cho cùng nhà cung cấp + hợp đồng → "Đã khai báo đầu kỳ cho tài khoản này".\n• Mở thẳng trang Sửa của khai báo Đã phát sinh (hoặc không có quyền sửa) → toast "Khai báo đã phát sinh chứng từ hoặc bạn không có quyền sửa." rồi chuyển sang trang Chi tiết.\n• Khai báo vừa phát sinh chứng từ khi đang sửa → bấm Lưu báo "Khai báo đã phát sinh chứng từ, không được sửa / xóa.", không lưu.\n• Bấm Quay lại khi đã sửa → hỏi "Thông tin chưa lưu".'],
    ],
    'menu_them': ' => Sửa {icon:btn_sua}',
    'ghi_chu_layout': TRANG % '"Sửa khai báo đầu kỳ công nợ nhà cung cấp"',
    'anh': [('12_edit', 'Trang Sửa khai báo đầu kỳ công nợ nhà cung cấp')],
    'ui': ui(UI8, [
        ['Mã phiếu', 'Textbox', 'Read-only', '–', '–', 'Mã hiện tại', 'Không sửa được.'],
        ['Nhà cung cấp', 'Dropdown', 'Read-only', '–', '–', 'Nhà cung cấp hiện tại', 'Không sửa được.'],
        ['Loại hợp đồng, Số hợp đồng, Người lập hợp đồng', 'Label', 'Read-only', '–', '–', 'Dữ liệu hiện tại', 'Không sửa được.'],
        ['Tài khoản', 'Dropdown', 'Enable', 'Tài khoản chi tiết theo dõi công nợ', 'Có', 'Dữ liệu hiện tại', 'Tài khoản cũ nay đã khóa vẫn hiện kèm biểu tượng khóa.'],
        ['Loại tiền, Tỷ giá', 'Dropdown / Textbox', 'Enable', 'Như trang Thêm', 'Có (Tỷ giá khi khác VNĐ)', 'Dữ liệu hiện tại', 'Như trang Thêm (BR-08); loại tiền cũ nay đã khóa vẫn hiện.'],
        ['Loại dư, Công nợ', 'Dropdown / Textbox', 'Enable', 'Như trang Thêm', 'Có', 'Dữ liệu hiện tại', 'Như trang Thêm; Quy đổi (VND) tính lại.'],
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi về danh sách. Trang Sửa không có "Lưu và tiếp tục", không có nút "Chọn hợp đồng" / xoá dòng.'],
        ['Nút Quay lại', 'Button', 'Enable', '–', '–', '–', 'Về danh sách (đã sửa thì hỏi "Thông tin chưa lưu").'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện khi có quyền "%s" và khai báo Chưa phát sinh.\nAfter:\n– Tải khai báo; ngoài phạm vi / không còn → trang "Không tìm thấy".' % Q_SUA],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền; khai báo phải Chưa phát sinh chứng từ (kiểm trước cả kiểm dữ liệu).\nDuring:\n– Kiểm như trang Thêm (bỏ qua trùng với chính khai báo).\n' + TRUOC_LUU + '\nAfter:\n– Ghi thay đổi, cập nhật bút toán sổ chi tiết.\n– Ghi nhận Thay đổi thông tin (giá trị cũ → mới) trong lịch sử.\n– Báo "Cập nhật thành công.", về danh sách.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa đổi gì → về danh sách; đã đổi → hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
    ],
})

# 2.7 Xem chi tiết --------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết khai báo', 'uc': 'uc_xem', 'uc_ten': 'FR-07 Xem chi tiết khai báo đầu kỳ công nợ nhà cung cấp',
    'qtc': 'Màn Xem chi tiết và Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết khai báo đầu kỳ công nợ nhà cung cấp'],
        ['Mô tả', 'Xem toàn bộ thông tin 1 khai báo ở chế độ chỉ đọc, kèm khối Lịch sử; nút thao tác ở chân trang khớp với nút ở dòng danh sách.'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK + '\n2. Khai báo thuộc phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Bấm Mã phiếu ở danh sách.\n2. Hệ thống mở trang "Chi tiết khai báo đầu kỳ công nợ nhà cung cấp: <mã phiếu>": khối Thông tin chung (Mã phiếu, Nhà cung cấp, góc phải "<Người tạo> - <ngày giờ tạo>"), khối Danh sách hợp đồng mua (1 dòng), khối Lịch sử (thu gọn).'],
        ['Dòng sự kiện phụ', '• Khai báo Chưa phát sinh: chân trang có Sửa (nếu có quyền sửa), Xóa (nếu có quyền xóa), Quay lại.\n• Khai báo Đã phát sinh: chỉ có Quay lại.\n• Khai báo ngoài phạm vi / không tồn tại: chuyển trang "Không tìm thấy".'],
    ],
    'menu_them': ' => Mã phiếu (liên kết)',
    'anh': [('17_detail', 'Trang Chi tiết khai báo Chưa phát sinh chứng từ (ngoại tệ USD)'),
            ('17c_detail_used', 'Trang Chi tiết khai báo Đã phát sinh chứng từ: chỉ còn nút Quay lại')],
    'ui': ui(UI6, [
        ['Mã phiếu, Nhà cung cấp', 'Textbox / Dropdown', 'Read-only', 'Dữ liệu khai báo', 'Chỉ đọc.'],
        ['Người tạo - ngày giờ', 'Label', 'Read-only', 'Dữ liệu khai báo', 'Góc phải khối Thông tin chung.'],
        ['Bảng hợp đồng mua', 'Table/Grid', 'Read-only', '1 dòng', 'Loại hợp đồng, Số hợp đồng (liên kết), Người lập hợp đồng, Tài khoản, Loại tiền, Tỷ giá, Loại dư, Công nợ, Quy đổi (VND) — các ô khóa.'],
        ['Khối Lịch sử', 'Label', 'Enable', 'Thu gọn', 'Bấm "Xem lịch sử" để mở (mục 2.12).'],
        ['Nút Sửa', 'Button', 'Enable / Ẩn', 'Theo trạng thái + quyền', 'Chỉ hiện khi Chưa phát sinh và có quyền sửa; mở trang Sửa.'],
        ['Nút Xóa', 'Button', 'Enable / Ẩn', 'Theo trạng thái + quyền', 'Chỉ hiện khi Chưa phát sinh và có quyền xóa (mục 2.8).'],
        ['Nút Quay lại', 'Button', 'Enable', '–', 'Về danh sách.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở trang', 'System', 'Before:\n– Kiểm tra phạm vi dữ liệu.\nAfter:\n– Hiển thị khai báo, tính nút Sửa / Xóa theo quyền và trạng thái phát sinh.'],
        ['Bấm Sửa / Xóa / Quay lại', 'Click', 'After:\n– Mở trang Sửa / hộp Xác nhận xóa / về danh sách.'],
    ],
})

# 2.8 Xóa -----------------------------------------------------------------------
FR.append({
    'ten': 'Xóa khai báo', 'uc': 'uc_xoa', 'uc_ten': 'FR-08 Xóa khai báo đầu kỳ công nợ nhà cung cấp',
    'qtc': 'Quy tắc xóa và Thông báo.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xóa khai báo đầu kỳ công nợ nhà cung cấp'],
        ['Mô tả', 'Xóa hẳn 1 khai báo Chưa phát sinh chứng từ cùng bút toán sổ chi tiết của nó.'],
        ['Tác nhân', QX],
        ['Điều kiện ban đầu', DK_XOA],
        ['Dòng sự kiện chính', '1. Bấm Xóa ở cột Hành động (hoặc nút Xóa ở trang Chi tiết).\n2. Hệ thống hiện hộp "Xác nhận xóa": "Bạn có chắc muốn xóa bản ghi này không?"\n3. Bấm Xóa.\n4. Hệ thống ghi nhận Xóa trong lịch sử, xóa bút toán sổ chi tiết và xóa khai báo.\n5. Báo "Xóa thành công.", tải lại danh sách (từ trang Chi tiết: về danh sách).'],
        ['Dòng sự kiện phụ', '• Bấm Hủy / (x) → đóng hộp, không thay đổi.\n• Khai báo vừa phát sinh chứng từ → "Khai báo đã phát sinh chứng từ, không được sửa / xóa.", không xóa.\n• Khai báo vừa bị người khác xóa → trang "Không tìm thấy" / báo lỗi.'],
    ],
    'menu_them': ' => Xóa {icon:btn_xoa}',
    'ghi_chu_layout': 'Modal Xác nhận xóa được mở ngay trên màn hình danh sách (nút Xóa trên dòng) hoặc màn hình chi tiết khai báo (nút Xóa) theo đường dẫn ở trên.',
    'anh': [('13_delete', 'Hộp Xác nhận xóa khai báo')],
    'ui': ui(UI4, [
        ['Nút Xóa (cột Hành động / chân trang Chi tiết)', 'Button', 'Biểu tượng thùng rác; chỉ hiện khi khai báo Chưa phát sinh và có quyền xóa.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận xóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn xóa bản ghi này không?"'],
        ['Nút Xóa', 'Button', 'Xác nhận xóa.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không xóa.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Xóa', 'Click', 'After:\n– Hiện hộp Xác nhận xóa.'],
        ['Bấm Xóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền "%s", phạm vi; khai báo phải Chưa phát sinh chứng từ.\nDuring:\n' % Q_XOA + TRUOC_LUU + '\nAfter:\n– Ghi nhận Xóa trong lịch sử, xóa bút toán sổ chi tiết, xóa khai báo.\n– Báo "Xóa thành công.", tải lại danh sách.'],
        ['Bấm Hủy / (x)', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.9 In danh sách ---------------------------------------------------------------
FR.append({
    'ten': 'In danh sách', 'uc': 'uc_in', 'uc_ten': 'FR-09 In danh sách khai báo',
    'qtc': 'Quy tắc màn In và bố cục bản in.',
    'gioi_thieu': [
        ['Tên chức năng', 'In danh sách khai báo đầu kỳ công nợ nhà cung cấp'],
        ['Mô tả', 'In danh sách đang lọc theo mẫu "Khai báo công nợ đầu kỳ nhà cung cấp", khổ ngang, có tiêu đề công ty của người đăng nhập; cột in theo cột đang hiện trên bảng.'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm In danh sách.\n2. Hệ thống mở cửa sổ "Xem trước khai báo đầu kỳ công nợ nhà cung cấp" với bản in mọi dòng khớp bộ lọc.\n3. Bấm In để mở hộp in của trình duyệt.'],
        ['Dòng sự kiện phụ', '• Danh sách vượt 2,000 dòng: không in, báo "Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được…" kèm gợi ý thu hẹp bộ lọc (BR-11).\n• Tỷ giá, Dư nợ, Dư có in 2 chữ số thập phân; Quy đổi (VND) in số chẵn.'],
    ],
    'menu_them': ' => In danh sách {icon:btn_indanhsach}',
    'ghi_chu_layout': 'Cửa sổ Xem trước bản in được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('19_printlist', 'Cửa sổ xem trước bản in danh sách')],
    'ui': ui(UI6, [
        ['Tiêu đề cửa sổ', 'Label', 'Read-only', '"Xem trước khai báo đầu kỳ công nợ nhà cung cấp"', '–'],
        ['Phần đầu bản in', 'Label', 'Read-only', 'Tiêu đề công ty', 'Logo, tên, địa chỉ công ty của người đăng nhập.'],
        ['Tiêu đề bản in', 'Label', 'Read-only', '"KHAI BÁO CÔNG NỢ ĐẦU KỲ NHÀ CUNG CẤP"', '–'],
        ['Bảng in', 'Table/Grid', 'Read-only', 'Theo bộ lọc', 'STT, Mã phiếu luôn có; các cột khác theo cột đang hiện (không gồm Hành động).'],
        ['Chân bản in', 'Label', 'Read-only', '–', '"Ngày ..... Tháng ..... Năm .....", "Người lập".'],
        ['Nút In', 'Button', 'Enable', '–', 'Mở hộp in của trình duyệt.'],
        ['Nút (x)', 'Button', 'Enable', '–', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In danh sách', 'Click', 'Before:\n– Người dùng đã đăng nhập; dữ liệu theo phạm vi xem.\nAfter:\n– Dựng bản in theo bộ lọc + cột đang hiện; vượt 2,000 dòng thì chỉ hiện câu nhắc.'],
        ['Bấm In', 'Click', 'After:\n– Mở hộp in của trình duyệt.'],
    ],
})

# 2.10 Xuất Excel -----------------------------------------------------------------
FR.append({
    'ten': 'Xuất Excel danh sách', 'uc': 'uc_xuat', 'uc_ten': 'FR-10 Xuất Excel danh sách khai báo',
    'qtc': 'Quy tắc Excel và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách khai báo ra Excel'],
        ['Mô tả', 'Xuất mọi dòng khớp bộ lọc (không chỉ trang đang xem) ra file khai_bao_dau_ky_cong_no_ncc.xlsx, tiêu đề "DANH SÁCH CÔNG NỢ ĐẦU KỲ THEO NHÀ CUNG CẤP - HỢP ĐỒNG", cột theo lựa chọn và thứ tự người dùng.'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất file", tích sẵn các cột đang hiện trên bảng.\n3. Người dùng tích / bỏ, kéo ☰ đổi thứ tự, bấm Xuất file.\n4. Hệ thống tải dữ liệu theo lô (cạnh nút hiện tiến độ "Đã tải x/y dòng…"), dựng file và tải về; báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Không có dòng nào khớp bộ lọc → báo "Không có dữ liệu để xuất", không tải file.\n• Cột Tỷ giá, Dư nợ, Dư có, Quy đổi (VND) là ô SỐ (cộng được), định dạng 1,234,567.89.'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất file')],
    'ui': ui(UI8, [
        ['Danh sách trường', 'Checkbox', 'Enable', '15 trường', 'Có (≥ 1)', 'Các cột đang hiện', 'Mã phiếu, Nhà cung cấp, Tài khoản, Loại hợp đồng, Số hợp đồng, Người lập hợp đồng, Loại tiền, Tỷ giá, Dư nợ, Dư có, Quy đổi (VND), Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. Kéo ☰ đổi thứ tự cột trong file.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', 'Chọn / bỏ nhanh mọi trường.'],
        ['Dòng đếm', 'Label', 'Read-only', '–', '–', '–', '"Đang chọn x/15 trường".'],
        ['Nút Xuất file', 'Button', 'Enable', '–', '–', '–', 'Xuất file theo trường đã chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng, không xuất.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất file', 'Click', 'Before:\n– Người dùng đã đăng nhập; dữ liệu theo phạm vi xem.\nAfter:\n– Tải dữ liệu theo bộ lọc hiện tại, dựng file đúng thứ tự cột, tải về; báo kết quả.'],
        ['Kéo ☰', 'Drag', 'After:\n– Đổi thứ tự cột trong file.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.11 Import --------------------------------------------------------------------
FR.append({
    'ten': 'Import khai báo từ file Excel', 'uc': 'uc_import', 'uc_ten': 'FR-11 Import khai báo từ file Excel',
    'qtc': 'Quy tắc Import Excel, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Import khai báo đầu kỳ công nợ nhà cung cấp từ file Excel'],
        ['Mô tả', 'Nhập nhiều khai báo từ file theo file mẫu "Mau_import_cong_no_dau_ky_nha_cung_cap.xlsx" (tải ngay trong cửa sổ). Mỗi dòng file = 1 khai báo, sinh mã và bút toán như khi lập tay. Tối đa 500 dòng mỗi lần.'],
        ['Tác nhân', QT],
        ['Điều kiện ban đầu', DK_THEM],
        ['Dòng sự kiện chính', '1. Bấm Import Excel → cửa sổ "Import khai báo đầu kỳ công nợ nhà cung cấp".\n2. Bấm "Tải file mẫu", điền dữ liệu.\n3. Bấm "Chọn file Excel", chọn file; bấm "Load lên bảng".\n4. Bấm Validate: hệ thống kiểm từng dòng, hiện Tổng / Hợp lệ / Lỗi; dòng hợp lệ bị khóa, dòng lỗi nêu từng lỗi.\n5. Sửa dòng lỗi ngay trên bảng rồi Validate lại, hoặc bấm "Bỏ dòng lỗi".\n6. Bấm Import (chỉ bấm được khi không còn dòng lỗi).\n7. Hệ thống ghi từng dòng (sinh mã, bút toán, ghi nhận Tạo mới trong lịch sử), báo số dòng thành công, tải lại danh sách.'],
        ['Dòng sự kiện phụ', '• Dòng vừa bị người khác khai báo trùng sau lần Validate → bỏ qua dòng đó, các dòng khác vẫn nhập, kết quả nêu dòng bị bỏ.\n• "Xoá trạng thái validate" để sửa lại cả dòng đã khóa; "Làm mới" xoá bảng.\n• File quá 500 dòng → báo, không load.'],
    ],
    'menu_them': ' => Import Excel {icon:btn_import}',
    'ghi_chu_layout': 'Modal Import khai báo đầu kỳ công nợ nhà cung cấp được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('21_import_open', 'Cửa sổ Import khi vừa mở'), ('23_import_validated', 'Kết quả Validate — mỗi dòng lỗi nêu rõ lý do')],
    'ui': ui(UI8, [
        ['Cột Nhà cung cấp', 'Textbox', 'Enable', 'Mã nhà cung cấp đang hoạt động', 'Có', 'Trống', 'Trống: "Nhà cung cấp – Bắt buộc phải nhập"; sai: "Nhà cung cấp – Mã không tồn tại trong hệ thống".'],
        ['Cột Mã hợp đồng mua', 'Textbox', 'Enable', 'Số hợp đồng mua', 'Có', 'Trống', '"Mã hợp đồng – Bắt buộc phải nhập" / "Mã hợp đồng – Không tồn tại trong hệ thống". Không kiểm hợp đồng thuộc nhà cung cấp (BR-09).'],
        ['Cột Loại hợp đồng mua', 'Dropdown', 'Enable', 'HDMNN, HDMN, HDMTN, HDMDK', 'Có', 'Trống', 'HDMNN: mua nước ngoài · HDMN: mua ngoài · HDMTN: mua trong nước · HDMDK: mua đầu kỳ. Sai: "Loại hợp đồng – Chỉ nhận HDMNN / HDMN / HDMTN / HDMDK".'],
        ['Cột Số tài khoản', 'Textbox', 'Enable', 'Số hiệu tài khoản', 'Có', 'Trống', '"Số tài khoản – Không tồn tại trong hệ thống" / "… – Không được khai báo công nợ (tài khoản khoá hoặc không phải tài khoản chi tiết)".'],
        ['Cột Loại tiền', 'Textbox', 'Enable', 'Mã tiền tệ (VNĐ, USD…)', 'Có', 'Trống', '"Loại tiền – Bắt buộc phải nhập" / "Loại tiền – Mã không tồn tại trong hệ thống". Nhận cả "VNĐ" lẫn "VND".'],
        ['Cột Tỷ giá', 'Textbox', 'Enable', 'Số > 0', 'Có khi khác VNĐ', 'Trống (VNĐ = 1)', '"Tỷ giá – Bắt buộc phải nhập" / "Tỷ giá – Phải lớn hơn 0."'],
        ['Cột Loại dư', 'Dropdown', 'Enable', 'Dư nợ / Dư có', 'Không', 'Trống = Dư nợ', 'Sai: "Loại dư – Chỉ nhận "Dư nợ" hoặc "Dư có"".'],
        ['Cột Công nợ', 'Textbox', 'Enable', 'Số > 0 (nguyên tệ)', 'Có', 'Trống', '"Công nợ – Bắt buộc phải nhập" / "Công nợ – Phải lớn hơn 0."'],
        ['Trùng', '–', '–', '–', '–', '–', '"Trùng với dòng <n> trong file" · "Hợp đồng đã được khai báo công nợ đầu kỳ cho tài khoản này".'],
        ['Nút Tải file mẫu / Chọn file Excel / Load lên bảng / Validate / Import', 'Button', 'Enable / Disable', '–', '–', '–', 'Import chỉ bấm được sau Validate và không còn dòng lỗi.'],
        ['Nút Bỏ dòng lỗi / Xoá trạng thái validate / Làm mới / Đóng', 'Button', 'Enable', '–', '–', '–', 'Bỏ dòng lỗi khỏi bảng / mở khóa dòng đã validate / xoá bảng / đóng cửa sổ.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Load lên bảng', 'Click', 'During:\n– Đọc file, quá 500 dòng thì báo và dừng.\nAfter:\n– Hiện dữ liệu lên bảng xem trước.'],
        ['Bấm Validate', 'Click', 'Before:\n– Kiểm tra quyền "%s".\nDuring:\n– Kiểm từng dòng theo bảng trên, trùng trong file, trùng khai báo đã có.\nAfter:\n– Hiện Tổng / Hợp lệ / Lỗi; khóa dòng hợp lệ.' % Q_THEM],
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
        ['Mô tả', 'Liệt kê các lần thao tác trên 1 khai báo (Tạo mới, Thay đổi thông tin), mới nhất ở trên, kèm người thực hiện, phòng ban, thời điểm, giá trị cũ → mới của từng trường (Mã phiếu, Nhà cung cấp, Hợp đồng, Tài khoản, Loại tiền, Tỷ giá, Loại dư, Công nợ).'],
        ['Tác nhân', Q_XEM],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Lịch sử ở cột Hành động → cửa sổ "Lịch sử thay đổi: <mã phiếu>".\n2. Hoặc ở trang Chi tiết bấm "Xem lịch sử" ở khối Lịch sử.\n3. Hệ thống liệt kê các mốc; có nút Bộ lọc (loại hành động, người thực hiện, khoảng ngày).'],
        ['Dòng sự kiện phụ', '• Khai báo lập / import trên HRM có mốc Tạo mới; khai báo chuyển từ dữ liệu cũ chưa có mốc nào.\n• Giá trị cũ in đỏ, giá trị mới in xanh.'],
    ],
    'menu_them': ' => Lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': 'Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối Lịch sử nằm cuối trang Chi tiết khai báo.',
    'anh': [('16_history', 'Cửa sổ Lịch sử thay đổi mở từ danh sách'), ('17b_detail_history', 'Khối Lịch sử ở trang Chi tiết')],
    'ui': ui(UI6, [
        ['Tiêu đề', 'Label', 'Read-only', '"Lịch sử thay đổi: <mã phiếu>"', '–'],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Lọc theo loại hành động, người thực hiện, Từ ngày, Đến ngày.'],
        ['Mốc lịch sử', 'Label', 'Read-only', 'Mới nhất trên cùng', 'Thời điểm, tên hành động, "Người thực hiện: <họ tên> — <phòng ban>", danh sách trường đổi: cũ → mới (Tỷ giá, Công nợ dạng 1,234.00).'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lịch sử / Xem lịch sử', 'Click', 'After:\n– Tải và hiển thị các mốc lịch sử của khai báo.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

FR_NAMES = ['FR-%02d %s' % (i + 1, f['ten']) for i, f in enumerate(FR)]
# Ma trận: Có / Không theo từng cột quyền (cột 1 = chỉ đăng nhập)
_XEM = {0, 1, 2, 6, 8, 9, 11}
_MT = []
for i, f in enumerate(FR_NAMES):
    if i in _XEM:
        _MT.append([f, 'Có', 'Có', 'Có', 'Có'])
    elif i in (3, 4, 10):
        _MT.append([f, 'Không', 'Có', 'Không', 'Không'])
    elif i == 5:
        _MT.append([f, 'Không', 'Không', 'Có (khai báo Chưa phát sinh)', 'Không'])
    else:
        _MT.append([f, 'Không', 'Không', 'Không', 'Có (khai báo Chưa phát sinh)'])

S = {
    'ten': TEN, 'ten_ngan': 'khai báo đầu kỳ công nợ nhà cung cấp', 'phan_he': 'Tài chính',
    'menu': [('Tài chính', 'menu_phanhe'), ('Khai báo đầu kỳ', 'menu_nhom'), (TEN, 'menu_muc')],
    'muc_dich': [
        'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho việc khai báo SỐ DƯ CÔNG NỢ ĐẦU KỲ của nhà cung cấp theo từng hợp đồng mua × tài khoản, theo nguyên tệ và quy đổi VND — số mở đầu cho sổ chi tiết công nợ phải trả.',
        'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình (xem không cần quyền riêng; thêm, sửa, xóa theo 3 quyền riêng).',
        'Làm rõ phạm vi dữ liệu theo bốn cấp quyền xem và cách xác định tổ chức của khai báo (theo người lập hợp đồng).',
        'Làm rõ thời điểm khai báo bị khóa sửa / xóa: khi đã phát sinh chứng từ công nợ (phiếu chi, ủy nhiệm chi, phiếu thu, phiếu báo có, phiếu kế toán).',
        'Làm rõ tác động sổ sách: mỗi khai báo ghi đúng 1 bút toán sổ chi tiết (nguyên tệ, tỷ giá, quy đổi); sửa / xóa khai báo thì bút toán đổi / mất theo.',
    ],
    'thuat_ngu': [
        ['Khai báo đầu kỳ công nợ nhà cung cấp', 'Số dư công nợ của 1 nhà cung cấp trên 1 hợp đồng mua ở 1 tài khoản tại ngày khai báo đầu kỳ. Mỗi khai báo có 1 mã phiếu.'],
        ['Hợp đồng mua', 'Hợp đồng mua nước ngoài, mua ngoài, mua trong nước, mua đầu kỳ.'],
        ['Dư nợ / Dư có', 'Ghi Nợ tài khoản (nhà cung cấp còn nợ công ty, vd đã ứng trước) / ghi Có tài khoản (công ty còn nợ nhà cung cấp).'],
        ['Nguyên tệ / Tỷ giá / Quy đổi (VND)', 'Công nợ nhập theo loại tiền của khai báo; Quy đổi (VND) = Công nợ × Tỷ giá, làm tròn đến đồng. VNĐ có tỷ giá 1.'],
        ['Ngày khai báo đầu kỳ (Ngày tính công nợ)', 'Mốc ngày khai ở Khai Quy chế – Cấu hình của công ty; là ngày hạch toán của mọi khai báo.'],
        ['Bút toán sổ chi tiết', 'Dòng ghi sổ chi tiết tài khoản do khai báo sinh ra; báo cáo công nợ đọc dòng này.'],
        ['Chứng từ công nợ', 'Phiếu chi, phiếu ủy nhiệm chi, phiếu thu, phiếu báo có, phiếu kế toán.'],
        ['Đã phát sinh chứng từ', 'Khai báo mà cùng nhà cung cấp + hợp đồng + tài khoản đã có chứng từ công nợ ghi sổ, hoặc có chứng từ trừ thẳng vào khai báo.'],
        ['Người lập hợp đồng', 'Nhân viên tạo hợp đồng mua gắn với khai báo; công ty / phòng ban / bộ phận của khai báo lấy theo người này.'],
    ],
    'trang_thai': {
        'cau_dan': 'Khai báo KHÔNG qua bước gửi duyệt / duyệt / từ chối / hủy: lưu xong là có hiệu lực ngay (đã ghi bút toán). '
                   'Trạng thái của khai báo do hệ thống tự xác định theo việc đã có chứng từ công nợ hay chưa, không có ô trạng thái để chọn.',
        'rows': [
            ['Chưa phát sinh chứng từ', 'Khai báo đã ghi sổ, chưa có chứng từ công nợ nào trên cùng nhà cung cấp + hợp đồng + tài khoản.', 'Xem, Sửa (quyền sửa), Xóa (quyền xóa), In, Xuất, Lịch sử', 'Người có quyền "%s" lập / import, trong phạm vi dữ liệu' % Q_THEM],
            ['Đã phát sinh chứng từ', 'Đã có phiếu chi / ủy nhiệm chi / phiếu thu / phiếu báo có / phiếu kế toán ghi sổ cùng nhà cung cấp + hợp đồng + tài khoản, hoặc trừ thẳng vào khai báo.', 'Xem, In, Xuất, Lịch sử (không Sửa, không Xóa)', 'Tự chuyển khi kế toán lập chứng từ công nợ'],
            ['Đã xóa', 'Khai báo và bút toán bị xóa khỏi hệ thống.', '–', 'Người có quyền "%s", chỉ từ trạng thái Chưa phát sinh' % Q_XOA],
        ],
        'anh': 'state_flow',
        'ghi_chu': ['Chứng từ công nợ bị xóa / hủy ghi sổ thì khai báo tự trở lại Chưa phát sinh chứng từ. Phiếu nhập hàng, hạch toán mua dịch vụ trên cùng hợp đồng KHÔNG làm khai báo chuyển trạng thái (BR-05).'],
    },
    'quyen_truoc': ['Nhóm quyền thao tác: xem màn KHÔNG cần quyền riêng (mục menu luôn hiện với người đã đăng nhập); thêm, sửa, xóa theo 3 quyền riêng.'],
    'quyen_rows': [
        ['(không cần quyền riêng)', 'Thấy mục menu, vào màn; xem danh sách, tìm kiếm, xem chi tiết, lịch sử, tuỳ chỉnh cột, in, xuất Excel — trong phạm vi dữ liệu.'],
        [Q_THEM, 'Nút Tạo mới, Import Excel; cửa sổ chọn hợp đồng; lưu khai báo mới.'],
        [Q_SUA, 'Nút Sửa (dòng danh sách và chân trang Chi tiết) với khai báo Chưa phát sinh; lưu thay đổi.'],
        [Q_XOA, 'Nút Xóa (dòng danh sách và chân trang Chi tiết) với khai báo Chưa phát sinh.'],
    ],
    'pham_vi_truoc': ['Nhóm quyền quyết định phạm vi dữ liệu (xét theo thứ tự từ trên xuống, có quyền nào trước thì áp quyền đó):'],
    'pham_vi_rows': [
        ['1', 'Xem tất cả công nợ đầu kỳ', 'Khai báo của mọi công ty; khu vực lọc có ô Công ty, Phòng ban.'],
        ['2', 'Xem tất cả công nợ đầu kỳ của công ty', 'Khai báo thuộc công ty đang làm việc của người dùng; có ô Phòng ban.'],
        ['3', 'Xem tất cả công nợ đầu kỳ của phòng ban', 'Khai báo thuộc các phòng ban người dùng được giao quản lý; có ô Phòng ban.'],
        ['4', 'Xem tất cả công nợ đầu kỳ của bộ phận', 'Khai báo thuộc các bộ phận người dùng được giao quản lý.'],
        ['5', '(không có quyền nào ở trên)', 'Chỉ khai báo do chính người dùng tạo.'],
    ],
    'pham_vi_sau': ['Công ty / phòng ban / bộ phận của một khai báo = của NGƯỜI LẬP HỢP ĐỒNG (không phải người lập khai báo) — BR-04. '
                    'Phạm vi áp như nhau cho danh sách, chi tiết, sửa, xóa, in và xuất Excel; 4 quyền phạm vi dùng chung với màn Khai báo đầu kỳ công nợ.'],
    'ma_tran': [['Chức năng', 'Chỉ đăng nhập', 'Quyền thêm', 'Quyền sửa', 'Quyền xóa']] + _MT,
    'ma_tran_widths': [2.6, 0.9, 0.9, 1.0, 1.0],
    'quyen_sau': ['Cột quyền thêm / sửa / xóa đã gồm quyền xem. Phạm vi dữ liệu của mọi chức năng theo bảng quyền phạm vi ở trên.'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Một khai báo = 1 hợp đồng mua × 1 tài khoản', ['– Lập 1 lần cho 1 nhà cung cấp và nhiều hợp đồng; mỗi dòng lưu thành 1 khai báo riêng (1 mã phiếu, 1 bút toán).', '– Sửa / Chi tiết chỉ có 1 dòng; nhà cung cấp và hợp đồng không đổi được sau khi lưu.'], ['Lập khai báo', 'Sửa', 'Import']),
        ('BR-02', 'Phạm vi dữ liệu theo 4 cấp quyền xem', ['– Xét lần lượt: tất cả → công ty → phòng ban quản lý → bộ phận quản lý → chỉ khai báo mình tạo.', '– Khai báo ngoài phạm vi: không hiện ở danh sách; mở thẳng thì trang "Không tìm thấy".'], ['Mọi chức năng']),
        ('BR-03', 'Mã phiếu', ['– Dạng <mã công ty của người lập khai báo>_DKNCC_<số thứ tự 5 chữ số>, số thứ tự = lớn nhất hiện có của cùng tiền tố + 1.', '– Hai người lưu cùng lúc không bị trùng mã (form và import dùng chung cách sinh).'], ['Lập khai báo', 'Import']),
        ('BR-04', 'Tổ chức của khai báo', ['– Công ty / phòng ban / bộ phận của khai báo lấy theo người lập hợp đồng; dùng cho phạm vi xem và ô lọc tổ chức.', '– Người lập hợp đồng (mã, họ tên) được lưu kèm khai báo.'], ['Lập khai báo', 'Import', 'Tìm kiếm và lọc']),
        ('BR-05', 'Chặn sửa / xóa khi đã phát sinh chứng từ', ['– Đã phát sinh = sổ chi tiết có phiếu chi, ủy nhiệm chi, phiếu thu, phiếu báo có hoặc phiếu kế toán cùng nhà cung cấp + hợp đồng + tài khoản, hoặc có chứng từ trừ thẳng vào khai báo.', '– Phiếu nhập hàng, hạch toán (phát sinh trong kỳ) không tính.', '– Nút Sửa, Xóa ẩn; hệ thống chặn cả khi gửi yêu cầu trực tiếp ("Khai báo đã phát sinh chứng từ, không được sửa / xóa.").'], ['Sửa', 'Xóa', 'Xem chi tiết']),
        ('BR-06', 'Ghi sổ chi tiết', ['– Mỗi khai báo ghi 1 bút toán: Dư nợ ghi Nợ, Dư có ghi Có tài khoản đã chọn; số tiền nguyên tệ = Công nợ, loại tiền + tỷ giá của khai báo, quy đổi = Công nợ × Tỷ giá làm tròn đến đồng; ngày hạch toán = Ngày khai báo đầu kỳ cấu hình của công ty; chứng từ = mã phiếu.', '– Sửa khai báo cập nhật bút toán (kể cả đổi tài khoản, loại tiền); Xóa khai báo xóa bút toán.'], ['Lập khai báo', 'Sửa', 'Xóa', 'Import']),
        ('BR-07', 'Không trùng khai báo', ['– Cùng nhà cung cấp + hợp đồng + tài khoản chỉ khai báo 1 lần (kể cả trên cùng form, khi Sửa đổi tài khoản và khi import).', '– Báo dưới ô Tài khoản của dòng trùng: "Đã khai báo đầu kỳ cho tài khoản này" / "Trùng với dòng <n>"; import: "Hợp đồng đã được khai báo công nợ đầu kỳ cho tài khoản này".'], ['Lập khai báo', 'Sửa', 'Import']),
        ('BR-08', 'Loại tiền và tỷ giá', ['– Loại tiền bắt buộc, chọn trong tiền tệ đang hoạt động; VNĐ luôn chọn được.', '– VNĐ: tỷ giá luôn 1, ô khóa. Khác VNĐ: tỷ giá bắt buộc, lớn hơn 0; khi chọn loại tiền / thêm hợp đồng, tỷ giá điền sẵn theo danh mục tiền tệ và sửa được.'], ['Lập khai báo', 'Sửa', 'Import']),
        ('BR-09', 'Hợp đồng chọn được', ['– 4 nguồn hợp đồng mua (nước ngoài, mua ngoài, mua trong nước, mua đầu kỳ), mọi trạng thái.', '– Được chọn hợp đồng của nhà cung cấp khác (Phạm vi "HĐ nhà cung cấp khác"); import chỉ kiểm hợp đồng tồn tại, không kiểm thuộc nhà cung cấp.', '– Hợp đồng đã có khai báo của nhà cung cấp đang chọn không chọn lại được trong cửa sổ.'], ['Chọn hợp đồng', 'Import']),
        ('BR-10', 'Tài khoản chọn được', ['– Tài khoản chi tiết (không có tài khoản con) đang hoạt động và có đánh dấu theo dõi công nợ.', '– Khai báo cũ dùng tài khoản nay đã khóa vẫn hiện tài khoản đó kèm biểu tượng khóa.'], ['Lập khai báo', 'Sửa', 'Import']),
        ('BR-11', 'In và xuất', ['– In và xuất theo đúng bộ lọc đang áp dụng (mọi trang); in tối đa 2,000 dòng, vượt thì không in một phần.', '– File Excel: ô số là SỐ; không có dữ liệu thì không xuất file.'], ['In danh sách', 'Xuất Excel']),
        ('BR-12', 'Thao tác xong quay về danh sách', ['– Lưu (Thêm / Sửa) và Xóa ở trang Chi tiết xong thì về màn danh sách.'], ['Lập khai báo', 'Sửa', 'Xóa']),
        ('BR-13', 'Quyền thao tác tách riêng', ['– Xem không cần quyền riêng; Thêm (gồm Import, chọn hợp đồng), Sửa, Xóa theo 3 quyền riêng, kiểm cả ở giao diện (ẩn nút) lẫn khi lưu.', '– Thiếu quyền mà mở thẳng trang Thêm: chuyển trang "Không tìm thấy"; trang Sửa: chuyển về trang Chi tiết.'], ['Mọi chức năng']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây đọc hoặc dùng dữ liệu do Khai báo đầu kỳ công nợ nhà cung cấp ghi ra (khai báo và bút toán sổ chi tiết của khai báo).',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng (thêm / sửa / xóa theo 3 quyền riêng)',
    'mains': [('FR-01', 'Xem danh sách khai báo', 'view'), ('FR-04', 'Lập khai báo đầu kỳ công nợ NCC', 'crud'),
              ('FR-06', 'Sửa khai báo', 'crud'), ('FR-08', 'Xóa khai báo', 'action'),
              ('FR-09', 'In danh sách', 'io'), ('FR-10', 'Xuất Excel danh sách', 'io'),
              ('FR-11', 'Import khai báo từ Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc danh sách', 'view'), ('FR-03', 'Cài đặt bộ lọc, tuỳ chỉnh cột', 'view'),
             ('FR-07', 'Xem chi tiết khai báo', 'view'), ('FR-12', 'Xem lịch sử thay đổi', 'view')],
    'rieng': [('FR-04', 'Lập khai báo đầu kỳ công nợ NCC', 'crud', 'uc_them'), ('FR-05', 'Chọn hợp đồng mua', 'crud', 'uc_chonhd'),
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

# -*- coding: utf-8 -*-
"""SRS - Phiếu nhập kho điều chỉnh kiểm kê (STT 287) — khuôn PHIẾU đợt 3 (màn mẫu finance-declare-debt-beginning/docs/kh).

Nguồn (code HRM develop, 18/11/2026):
  FE hrm-client/pages/warehouse/inventory-imports/{index, create, _id/index, _id/edit}.vue,
     components/{InventoryImportForm.vue, row-actions.js, constants.js}, components/subsystem-menu/warehouse.js,
     pages/finance/bill-payment-requests/components/AttachmentSection.vue (khối File đính kèm)
  BE Modules/Finance: Http/Controllers/V1/WarehouseInventoryImportController.php,
     Services/InventoryImport/{WarehouseInventoryImportService, WarehouseInventoryImportWriteService,
     InventoryImportWriteService}.php, Entities/WarehouseInventoryImport/WarehouseInventoryImport.php,
     Entities/SelfInventory/SelfInventory.php; app/Support/Permissions/Catalog/{warehouse,accounting}.php
  Ảnh: capture.js (dev-hrm 18/11/2026). Phần 5: dò code FE/BE 18/11/2026.
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402
from _lib_phieu import ui, UI4, UI4W, UI6, UI6W, UI7, UI7W, UI8, UI8W, TRUOC_LUU  # noqa: E402

TEN = 'Phiếu nhập kho điều chỉnh kiểm kê'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q_XEM = 'Xem phiếu nhập kho điều chỉnh kiểm kê'
Q_TAO = 'Tạo phiếu nhập kho điều chỉnh kiểm kê'
Q_XL = 'Xử lý phiếu kiểm kê hàng hóa'
Q_KT = 'Kế toán kho'
NV = 'Người dùng đã đăng nhập (phạm vi dữ liệu theo quyền "%s")' % Q_XEM
DK = '1. Người dùng đăng nhập thành công.'
DK_TAO = DK + '\n2. Người dùng có quyền "%s" và "%s".' % (Q_TAO, Q_XL)
DK_SUA = DK + '\n2. Phiếu ở trạng thái Đang tạo và do chính người dùng tạo.'
TRANG = 'Trang %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'

P5 = [
    ('Kho', 'Kiểm kê theo hàng hóa (phiếu kiểm kê hàng hóa): nút "Tạo phiếu nhập kho điều chuyển" mở trang Thêm chọn sẵn phiếu kiểm kê; '
            'lập phiếu nhập điều chỉnh thì phiếu kiểm kê chuyển Đang xử lý',
     'Kho => Kiểm kho => Theo vị trí => Kiểm kê theo hàng hóa'),
    ('Tài chính', 'Phiếu nhập hàng điều chỉnh kiểm kê: chọn phiếu nhập kho điều chỉnh Chờ duyệt làm nguồn, lấy dòng hàng + file; '
                  'lưu thì phiếu nhập kho chuyển Đang hạch toán / Đã hạch toán, ghi Người duyệt, Ngày duyệt',
     'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng => Phiếu nhập hàng điều chỉnh kiểm kê'),
    ('Kho', 'Thẻ kho: dòng nhập điều chỉnh kiểm kê (lô nhập do Gửi duyệt sinh ra)', 'Kho => Báo cáo kho => Thẻ kho'),
    ('Kho', 'Danh mục kho vật lý: kho đã có phiếu nhập kho điều chỉnh không xóa được', 'Kho => Danh mục => Kho vật lý'),
    ('Kho', 'Danh mục vị trí: vị trí đã có dòng nhập điều chỉnh không xóa được', 'Kho => Danh mục => Vị trí'),
]

FR = []

# 2.1 Xem danh sách ---------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách phiếu nhập kho điều chỉnh kiểm kê',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách phiếu nhập kho điều chỉnh kiểm kê'],
        ['Mô tả', 'Hiển thị các phiếu nhập kho điều chỉnh kiểm kê trong phạm vi dữ liệu của người dùng, có phân trang, sắp xếp, nhãn trạng thái màu và nút thao tác theo từng dòng.'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), phiếu tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Không có phiếu khớp → bảng hiện "Không có dữ liệu phù hợp."\n• Phạm vi dữ liệu theo quyền (Phần 2, BR-02): phiếu Đang tạo của người khác không bao giờ hiện.\n• Nút trên dòng hiện theo trạng thái và người dùng (BR-04).'],
    ],
    'anh': [('01_list', 'Màn danh sách Phiếu nhập kho điều chỉnh kiểm kê lúc mới truy cập'),
            ('01b_list_draft', 'Dòng phiếu Đang tạo của chính người dùng có nút Sửa (ảnh giả lập trạng thái Đang tạo)')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Danh sách phiếu nhập kho điều chỉnh kiểm kê', 'Tiêu đề khối danh sách; tiêu đề trang "Phiếu nhập kho điều chỉnh kiểm kê".'],
        ['Nút Tạo mới', 'Button', 'Enable / Ẩn', 'Hiển thị khi có quyền', 'Chỉ hiện khi có quyền "%s". Mở trang "Tạo phiếu nhập kho điều chỉnh kiểm kê" (mục 2.4).' % Q_TAO],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất Excel" (mục 2.11). Trong lúc xuất, cạnh nút hiện dòng tiến độ.'],
        ['Nút In danh sách', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ xem trước bản in danh sách (mục 2.10).'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.3).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa, không ẩn được.'],
        ['Cột Số phiếu', 'Table/Grid', 'Read-only', 'Hiển thị', '- Dạng PNKĐCKK-<5 chữ số> (BR-03).\n- Sắp xếp được. Chữ dạng liên kết: bấm mở trang Chi tiết (mục 2.7).\n- Cột khóa, không ẩn được.'],
        ['Cột Phiếu kiểm kê', 'Table/Grid', 'Read-only', 'Hiển thị', 'Mã phiếu kiểm kê hàng hóa nguồn, dạng liên kết mở chi tiết phiếu kiểm kê ở tab mới.'],
        ['Cột Ngày kiểm kê', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy — ngày lập phiếu nhập kho điều chỉnh.'],
        ['Cột Kho', 'Table/Grid', 'Read-only', 'Hiển thị', '"Mã - Tên kho" nhập hàng thừa.'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', '"Mã phòng ban - Họ tên".'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được (mặc định giảm dần).'],
        ['Cột Người duyệt', 'Table/Grid', 'Read-only', 'Hiển thị', 'Họ tên Kế toán kho lập phiếu nhập hàng điều chỉnh kiểm kê; trống khi chưa có.'],
        ['Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Trạng thái', 'Table/Grid', 'Read-only', 'Hiển thị', 'Nhãn màu: Đang tạo (xám), Chờ duyệt (vàng), Đang hạch toán (xanh dương), Đã hạch toán (xanh lá). Không sắp xếp.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sửa: phiếu Đang tạo của chính người dùng.\n- Tạo phiếu nhập hàng: phiếu Chờ duyệt, người dùng có quyền "%s".\n- In, Lịch sử: luôn có.\n- Nút không dùng được thì ẩn. Cột khóa, không ẩn được.' % Q_KT],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Mục menu không gắn quyền: mọi người dùng đều vào được.\nAfter:\n– Tải trang 1 theo phạm vi dữ liệu (BR-02), sắp Ngày tạo giảm dần; khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút).'],
        ['Bấm tiêu đề cột Số phiếu / Ngày tạo / Ngày duyệt', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, về trang 1, tải lại dữ liệu.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp, tải lại dữ liệu; đổi số dòng thì quay về trang 1.'],
        ['Bấm Số phiếu', 'Click', 'After:\n– Mở trang Chi tiết phiếu (mục 2.7).'],
        ['Bấm Phiếu kiểm kê', 'Click', 'After:\n– Mở chi tiết phiếu kiểm kê hàng hóa ở tab mới.'],
    ],
})

# 2.2 Tìm kiếm và lọc --------------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc danh sách',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách phiếu'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao.'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập số phiếu rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô gõ chữ (tìm nhanh, Mã phiếu, Mã hàng hóa, Tên hàng hóa) chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Bấm Làm mới → xoá mọi điều kiện, tải lại danh sách.\n• Ô Công ty chỉ dùng được với phạm vi Tổng công ty; ô Phòng ban mở khi có phạm vi Công ty trở lên (BR-02).\n• Hệ thống ghi nhớ bộ lọc 10 phút khi vào trang chi tiết / thêm / sửa rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực Tìm kiếm nâng cao ở trạng thái mở')],
    'ui': ui(UI7, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Tìm theo số phiếu"; tìm gần đúng theo Số phiếu.'],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Áp dụng từ khóa và các ô lọc.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá mọi điều kiện lọc và tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực ô lọc (khi mở, nút đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" (mục 2.3).'],
        ['Ô Mã phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Nhập mã phiếu"; tìm gần đúng Số phiếu.'],
        ['Ô Kho', 'Dropdown', 'Enable', 'Kho đã có phiếu trong phạm vi xem', 'Trống', '"Mã - Tên kho"; kho đã khóa hiện kèm biểu tượng ổ khóa.'],
        ['Ô Trạng thái', 'Dropdown', 'Enable', 'Đang tạo / Chờ duyệt / Đang hạch toán / Đã hạch toán', 'Trống', 'Bỏ trống thì hiện mọi trạng thái.'],
        ['Ô Người tạo', 'Dropdown', 'Enable', 'Người đã lập phiếu trong phạm vi xem', 'Trống', '"Mã phòng ban - Họ tên".'],
        ['Ô Mã hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Nhập mã hàng hóa"; phiếu có ít nhất 1 dòng hàng chứa mã đã gõ.'],
        ['Ô Tên hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Nhập tên hàng hóa"; phiếu có ít nhất 1 dòng hàng chứa tên đã gõ.'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy, Từ → Đến', 'Trống', 'Lọc theo ngày tạo phiếu, tính cả 2 đầu mút.'],
        ['Ô Công ty – Phòng ban', 'Dropdown', 'Enable / Khóa', 'Theo phạm vi xem', 'Trống', '- Công ty: chỉ chọn được với phạm vi Tổng công ty.\n- Phòng ban: chọn trong công ty; lọc theo phòng ban của phiếu (= của người lập phiếu kiểm kê, BR-05).'],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm Tìm kiếm / nhấn Enter ở ô gõ chữ', 'Click', 'After:\n– Áp đồng thời từ khóa và các ô lọc, tải lại bảng từ trang 1.'],
        ['Chọn giá trị ở ô chọn', 'Change', 'After:\n– Tải lại bảng từ trang 1 ngay.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khu vực ô lọc; lần mở đầu tải danh sách giá trị của các ô chọn.'],
    ],
})

# 2.3 Cài đặt bộ lọc / tuỳ chỉnh cột -----------------------------------------------
FR.append({
    'ten': 'Cài đặt bộ lọc và tuỳ chỉnh cột',
    'qtc': 'Bộ lọc, Cấu hình cột và lưu cấu hình theo người dùng.',
    'gioi_thieu': [
        ['Tên chức năng', 'Cài đặt bộ lọc và tuỳ chỉnh cột'],
        ['Mô tả', 'Người dùng chọn ô lọc nào hiển thị / thứ tự ô lọc, và cột nào hiển thị / thứ tự cột trên bảng. Cấu hình lưu theo từng người dùng, từng màn.'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Bấm "Cài đặt bộ lọc" (hoặc biểu tượng Cấu hình cột hiển thị).\n2. Tích / bỏ tích, kéo biểu tượng để đổi thứ tự.\n3. Bấm Lưu: hệ thống lưu cấu hình và áp dụng ngay.'],
        ['Dòng sự kiện phụ', '• Bấm Đóng: bỏ thay đổi.\n• Cài đặt bộ lọc có nút "Khôi phục mặc định".\n• Cột STT, Số phiếu, Hành động không bỏ được (có biểu tượng khóa).'],
    ],
    'menu_them': ' => Cài đặt bộ lọc {icon:btn_caidatboloc} / Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': 'Modal Cài đặt bộ lọc và Modal Tuỳ chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('26_filtercfg', 'Cửa sổ Cài đặt bộ lọc'), ('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột')],
    'ui': ui(UI6, [
        ['Danh sách ô lọc', 'Checkbox', 'Enable', 'Đủ 8 ô', 'Mã phiếu, Kho, Trạng thái, Người tạo, Mã hàng hóa, Tên hàng hóa, Ngày tạo, Công ty – Phòng ban. Kéo đổi thứ tự.'],
        ['Nút Khôi phục mặc định', 'Button', 'Enable', '–', 'Đưa cấu hình ô lọc về mặc định.'],
        ['Danh sách cột', 'Checkbox', 'Enable', '11/11 cột', 'Tích cột muốn hiện; STT, Số phiếu, Hành động bị khóa. Kéo đổi thứ tự.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Chọn / bỏ nhanh mọi cột (trừ cột khóa).'],
        ['Nút Lưu', 'Button', 'Enable', '–', 'Lưu cấu hình theo người dùng, áp dụng ngay.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ, không lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình theo người dùng, đóng cửa sổ, bảng / khu vực lọc vẽ lại theo cấu hình.'],
        ['Kéo biểu tượng đổi thứ tự', 'Drag', 'After:\n– Đổi thứ tự dòng trong cửa sổ.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ, không lưu.'],
    ],
})

# 2.4 Lập phiếu --------------------------------------------------------------------
FR.append({
    'ten': 'Lập phiếu nhập kho điều chỉnh kiểm kê', 'uc': 'uc_them', 'uc_ten': 'FR-04 Lập phiếu nhập kho điều chỉnh kiểm kê',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Lập phiếu nhập kho điều chỉnh kiểm kê'],
        ['Mô tả', 'Lập phiếu nhập vào kho phần hàng THỪA chưa xử lý của 1 phiếu kiểm kê hàng hóa tại 1 kho. Dòng hàng do hệ thống lấy từ phiếu kiểm kê (chỉ đọc). Bấm Lưu: phiếu ở trạng thái Đang tạo, chưa nhập hàng; bấm Gửi duyệt: xem mục 2.5.'],
        ['Tác nhân', 'Người dùng có quyền "%s" và "%s"' % (Q_TAO, Q_XL)],
        ['Điều kiện ban đầu', DK_TAO + '\n3. Có phiếu kiểm kê hàng hóa ở trạng thái Chờ xử lý / Đang xử lý, còn hàng thừa chưa xử lý và chưa có phiếu nhập kho điều chỉnh.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới (hoặc nút "Tạo phiếu nhập kho điều chuyển" ở chi tiết phiếu kiểm kê — phiếu kiểm kê được chọn sẵn).\n2. Hệ thống mở trang "Tạo phiếu nhập kho điều chỉnh kiểm kê"; góc phải khối Thông tin chung hiện "<Người đăng nhập> - <ngày giờ hiện tại>".\n3. Người dùng chọn Phiếu kiểm kê; hệ thống mở ô Kho (các kho của phiếu kiểm kê, chọn sẵn kho đầu tiên) và nạp bảng Chi tiết = hàng thừa chưa xử lý tại kho.\n4. Người dùng đổi Kho (nếu cần), nhập Ghi chú, thêm File đính kèm.\n5. Bấm Lưu.\n6. Hệ thống kiểm tra dữ liệu, lấy LẠI dòng hàng từ phiếu kiểm kê, sinh số phiếu (BR-03), ghi phiếu trạng thái Đang tạo, chuyển phiếu kiểm kê sang Đang xử lý.\n7. Ghi nhận Tạo mới trong lịch sử phiếu.\n8. Báo "Lưu thành công.", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• "Lưu và tiếp tục": lưu như trên rồi ở lại trang Thêm, form trống, danh sách phiếu kiểm kê nạp lại (phiếu vừa lập không còn).\n• Thiếu / sai dữ liệu → báo đỏ dưới ô + toast "Bạn chưa nhập đầy đủ thông tin.", cuộn tới ô lỗi đầu tiên.\n• Kho đã chọn không còn hàng thừa → bảng ghi "Kho này không còn hàng thừa cần nhập điều chỉnh", Lưu báo "Kho không còn hàng thừa cần nhập điều chỉnh.".\n• Người khác vừa lập phiếu cho cùng phiếu kiểm kê → "Phiếu kiểm kê không còn lập được phiếu nhập kho điều chỉnh. Vui lòng load lại trang", không lưu (BR-06).\n• Bấm Quay lại: chưa nhập gì thì về danh sách; đã nhập thì hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', 'Các nút Lưu / Lưu và tiếp tục / Gửi duyệt bị khóa ngay khi bấm cho tới khi có kết quả, tránh lưu 2 lần.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'hoac_menu': ['Hoặc Menu: Phân hệ Kho => Kiểm kho => Theo vị trí => Kiểm kê theo hàng hóa => Số phiếu kiểm kê => Tạo phiếu nhập kho điều chuyển {icon:btn_tu_kiemke}'],
    'ghi_chu_layout': TRANG % '"Tạo phiếu nhập kho điều chỉnh kiểm kê"',
    'anh': [('10_create', 'Trang Tạo phiếu nhập kho điều chỉnh kiểm kê lúc mới mở'),
            ('11_validate', 'Bấm Lưu khi chưa nhập: báo lỗi ở từng ô bắt buộc'),
            ('10b_create_filled', 'Đã chọn phiếu kiểm kê, kho, nhập ghi chú và đính kèm file (file đính kèm giả lập)'),
            ('18_unsaved', 'Hộp xác nhận Thông tin chưa lưu khi bấm Quay lại')],
    'ui': ui(UI8, [
        ['Người tạo - ngày giờ', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại', 'Góc phải khối Thông tin chung.'],
        ['Phiếu kiểm kê', 'Dropdown', 'Enable', 'Phiếu kiểm kê còn lập được (BR-06)', 'Có', 'Trống (vào từ phiếu kiểm kê: chọn sẵn)', '- Placeholder "Chọn phiếu kiểm kê"; biểu tượng ⓘ: "Chỉ liệt kê phiếu kiểm kê Chờ xử lý / Đang xử lý còn hàng thừa chưa nhập điều chỉnh.".\n- Bỏ trống: "Bắt buộc phải nhập".'],
        ['Kho', 'Dropdown', 'Disable / Enable', 'Kho của phiếu kiểm kê', 'Có', 'Kho đầu tiên của phiếu kiểm kê', '- Khóa tới khi chọn phiếu kiểm kê; ⓘ giải thích lý do khóa.\n- Đổi kho: nạp lại hàng thừa của kho đó. Bỏ trống: "Bắt buộc phải nhập".'],
        ['Ghi chú', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống', 'Placeholder "Nhập ghi chú"; trống / chỉ khoảng trắng: "Bắt buộc phải nhập"; quá 255 ký tự không gõ thêm được.'],
        ['Khối File đính kèm', 'File', 'Enable', 'pdf, png, jpg, jpeg; ≤ 20MB/file', 'Có (≥ 1 file)', 'Trống', '- Nút "Thêm tài liệu" thêm dòng, "Chọn tệp" tải file lên ngay; mỗi dòng có Xem trước, Tải xuống, Thay đổi, Xóa.\n- Sai đuôi: File "<tên>" không thuộc định dạng cho phép; quá dung lượng: File "<tên>" vượt quá 20MB.\n- Không có file: "Bắt buộc phải nhập".'],
        ['Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Có (≥ 1 dòng)', 'Trống', '- Cột STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, Vị trí, Số lượng (= số lượng thừa − đã xử lý).\n- Chưa chọn phiếu: "Chọn phiếu kiểm kê để nạp hàng thừa cần nhập điều chỉnh".'],
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu trạng thái Đang tạo rồi về danh sách.'],
        ['Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', '–', 'Lưu trạng thái Đang tạo rồi làm trống form để lập phiếu cho phiếu kiểm kê khác.'],
        ['Nút Gửi duyệt', 'Button', 'Enable', '–', '–', '–', 'Lưu và gửi duyệt ngay (mục 2.5).'],
        ['Nút Quay lại', 'Button', 'Enable', '–', '–', '–', 'Về danh sách (đã nhập thì hỏi "Thông tin chưa lưu").'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'Before:\n– Nút chỉ hiện khi có quyền "%s"; mở thẳng trang Thêm khi thiếu quyền thì chuyển trang "Không tìm thấy".\nAfter:\n– Mở trang Thêm trống, tải danh sách phiếu kiểm kê còn lập được.' % Q_TAO],
        ['Chọn Phiếu kiểm kê', 'Change', 'After:\n– Nạp danh sách kho của phiếu kiểm kê, chọn kho đầu tiên, nạp hàng thừa chưa xử lý tại kho.\n– Phiếu không còn lập được: báo dưới ô "Phiếu kiểm kê không còn lập được phiếu nhập kho điều chỉnh hoặc bạn không có quyền." và bỏ chọn.'],
        ['Đổi Kho', 'Change', 'After:\n– Nạp lại bảng Chi tiết theo kho mới.'],
        ['Chọn tệp ở khối File đính kèm', 'Change', 'During:\n– Kiểm đuôi file và dung lượng.\nAfter:\n– Tải file lên kho lưu trữ, dòng chuyển sang trạng thái chờ lưu cùng phiếu.'],
        ['Bấm Lưu / Lưu và tiếp tục', 'Click', 'Before:\n– Kiểm tra quyền "%s".\nDuring:\n– Có phiếu kiểm kê, kho, ghi chú (≤ 255 ký tự), ít nhất 1 file; phiếu kiểm kê còn lập được (khóa phiếu kiểm kê trong lúc ghi để 2 người không cùng lập); kho thuộc phiếu kiểm kê ("Kho – Kho không thuộc phiếu kiểm kê."); kho còn hàng thừa.\n' % Q_TAO + TRUOC_LUU + '\nAfter:\n– Sinh số phiếu, ghi phiếu Đang tạo + dòng hàng lấy lại từ phiếu kiểm kê; công ty / phòng ban của phiếu = của người lập phiếu kiểm kê.\n– Phiếu kiểm kê chuyển Đang xử lý (ghi lịch sử phiếu kiểm kê).\n– Ghi nhận Tạo mới trong lịch sử phiếu.\n– Báo "Lưu thành công."; Lưu → về danh sách, Lưu và tiếp tục → form trống.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa nhập gì → về danh sách.\n– Đã nhập → hộp "Thông tin chưa lưu" ("Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"): Thoát thì về danh sách không lưu, Ở lại thì quay về form.'],
    ],
})

# 2.5 Gửi duyệt --------------------------------------------------------------------
FR.append({
    'ten': 'Gửi duyệt phiếu', 'uc': 'uc_guiduyet', 'uc_ten': 'FR-05 Gửi duyệt phiếu nhập kho điều chỉnh kiểm kê',
    'qtc': 'Quy tắc gửi duyệt, Thông báo và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Gửi duyệt phiếu nhập kho điều chỉnh kiểm kê'],
        ['Mô tả', 'Lưu phiếu ở trạng thái Chờ duyệt: hệ thống NHẬP NGAY hàng thừa vào kho (tăng tồn kho vật lý tại vị trí) và thông báo cho Kế toán kho để lập phiếu nhập hàng điều chỉnh kiểm kê. Sau khi gửi không sửa được phiếu.'],
        ['Tác nhân', 'Người lập phiếu (trang Thêm cần quyền "%s"; trang Sửa: người tạo phiếu Đang tạo)' % Q_TAO],
        ['Điều kiện ban đầu', DK + '\n2. Đang ở trang Thêm, hoặc trang Sửa của phiếu Đang tạo do chính mình tạo.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập đủ thông tin và bấm Gửi duyệt.\n2. Hệ thống hiện hộp "Xác nhận gửi duyệt": "Gửi duyệt sẽ nhập ngay hàng thừa vào kho và không sửa được phiếu nữa. Bạn có chắc muốn gửi duyệt?".\n3. Người dùng bấm Gửi duyệt.\n4. Hệ thống lưu phiếu trạng thái Chờ duyệt; mỗi dòng chi tiết sinh 1 lô nhập điều chỉnh và cộng tồn kho vật lý tại vị trí của dòng.\n5. Ghi nhận lịch sử (Tạo mới, hoặc Thay đổi trạng thái Đang tạo → Chờ duyệt khi gửi từ trang Sửa).\n6. Gửi thông báo tới người có quyền "%s" cùng công ty với người gửi.\n7. Báo "Gửi duyệt thành công.", quay về danh sách.' % Q_KT],
        ['Dòng sự kiện phụ', '• Bấm Hủy / (x) ở hộp xác nhận → đóng hộp, không lưu.\n• Thiếu dữ liệu → báo lỗi như khi Lưu, không hiện hộp xác nhận.\n• Phiếu vừa bị gửi ở nơi khác (trang Sửa) → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi} => Gửi duyệt {icon:btn_guiduyet}',
    'hoac_menu': ['Hoặc Menu: Phân hệ Kho => Nhập kho => Phiếu nhập kho điều chỉnh kiểm kê => Sửa {icon:btn_sua} => Gửi duyệt {icon:btn_guiduyet}'],
    'ghi_chu_layout': 'Modal Xác nhận gửi duyệt được mở ngay trên trang Thêm / Sửa phiếu theo đường dẫn ở trên.',
    'anh': [('15_send_confirm', 'Hộp Xác nhận gửi duyệt')],
    'ui': ui(UI4, [
        ['Nút Gửi duyệt (chân trang Thêm / Sửa)', 'Button', 'Nút chính màu xanh; kiểm tra dữ liệu như Lưu trước khi hỏi xác nhận.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận gửi duyệt".'],
        ['Nội dung', 'Label', '"Gửi duyệt sẽ nhập ngay hàng thừa vào kho và không sửa được phiếu nữa. Bạn có chắc muốn gửi duyệt?"'],
        ['Nút Gửi duyệt', 'Button', 'Xác nhận gửi duyệt.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không lưu.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Gửi duyệt', 'Click', 'During:\n– Kiểm dữ liệu như Lưu; thiếu thì báo lỗi, không hỏi.\nAfter:\n– Hiện hộp Xác nhận gửi duyệt.'],
        ['Bấm Gửi duyệt trong hộp', 'Click', 'Before:\n– Kiểm quyền (trang Thêm) / phiếu còn Đang tạo của chính mình (trang Sửa).\nDuring:\n' + TRUOC_LUU + '\nAfter:\n– Lưu phiếu Chờ duyệt; mỗi dòng sinh 1 lô nhập điều chỉnh, cộng tồn kho vật lý tại kho + vị trí của dòng (ghi thẻ kho).\n– Ghi nhận lịch sử; gửi thông báo "[NKĐCKK] Chờ duyệt: <số phiếu>. Người gửi: <họ tên>. Kho: <tên kho>" tới Kế toán kho cùng công ty người gửi; bấm thông báo mở Chi tiết phiếu.\n– Báo "Gửi duyệt thành công.", về danh sách.'],
        ['Bấm Hủy / (x)', 'Click', 'After:\n– Đóng hộp, giữ nguyên form.'],
    ],
})

# 2.6 Sửa ---------------------------------------------------------------------------
FR.append({
    'ten': 'Sửa phiếu', 'uc': 'uc_sua', 'uc_ten': 'FR-06 Sửa phiếu nhập kho điều chỉnh kiểm kê',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Sửa phiếu nhập kho điều chỉnh kiểm kê'],
        ['Mô tả', 'Sửa phiếu Đang tạo do chính mình tạo: chỉ đổi được Ghi chú và File đính kèm. Phiếu kiểm kê, Kho và dòng hàng giữ nguyên như lúc lập (không nạp lại).'],
        ['Tác nhân', 'Người tạo phiếu'],
        ['Điều kiện ban đầu', DK_SUA],
        ['Dòng sự kiện chính', '1. Bấm Sửa ở cột Hành động (hoặc nút Sửa ở trang Chi tiết).\n2. Hệ thống mở trang "Sửa phiếu nhập kho điều chỉnh kiểm kê: <số phiếu>"; Phiếu kiểm kê (liên kết) và Kho chỉ đọc.\n3. Người dùng sửa Ghi chú, thêm / xóa file và bấm Lưu (hoặc Gửi duyệt — mục 2.5).\n4. Hệ thống kiểm tra, ghi thay đổi.\n5. Ghi nhận Thay đổi thông tin (Ghi chú, File đính kèm: cũ → mới) trong lịch sử.\n6. Báo "Lưu thành công.", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Xóa file ĐÃ LƯU: hộp "Xác nhận xóa" ("Bạn có chắc muốn xóa file đính kèm này?") → Xóa thì file bị gỡ NGAY (không chờ Lưu), báo "Xóa file thành công".\n• Phiếu không còn Đang tạo / không phải của mình → mở trang Sửa bị chuyển sang trang Chi tiết; bấm Lưu khi trạng thái vừa đổi → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n• Không còn file nào: "File đính kèm – Vui lòng đính kèm ít nhất 1 file.".\n• Bấm Quay lại khi đã sửa → hỏi "Thông tin chưa lưu".'],
    ],
    'menu_them': ' => Sửa {icon:btn_sua}',
    'ghi_chu_layout': TRANG % '"Sửa phiếu nhập kho điều chỉnh kiểm kê"',
    'anh': [('12_edit', 'Trang Sửa phiếu (ảnh giả lập phiếu ở trạng thái Đang tạo)')],
    'ui': ui(UI8, [
        ['Phiếu kiểm kê', 'Link', 'Read-only', '–', '–', 'Dữ liệu phiếu', 'Liên kết mở chi tiết phiếu kiểm kê ở tab mới.'],
        ['Kho', 'Textbox', 'Read-only', '–', '–', 'Dữ liệu phiếu', 'ⓘ "Kho không đổi được sau khi tạo phiếu."'],
        ['Ghi chú', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Dữ liệu phiếu', 'Như trang Thêm.'],
        ['Khối File đính kèm', 'File', 'Enable', 'pdf, png, jpg, jpeg; ≤ 20MB/file', 'Có (≥ 1 file)', 'File đã lưu', 'Như trang Thêm; file đã lưu chỉ Xem trước / Tải xuống / Xóa (không Thay đổi).'],
        ['Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', '–', 'Dòng hàng đã lưu', 'Không nạp lại.'],
        ['Nút Lưu / Gửi duyệt / Quay lại', 'Button', 'Enable', '–', '–', '–', 'Trang Sửa không có "Lưu và tiếp tục".'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện với phiếu Đang tạo của chính người dùng.\nAfter:\n– Tải phiếu; ngoài phạm vi / không còn → trang "Không tìm thấy"; không còn sửa được → trang Chi tiết.'],
        ['Bấm Xóa file đã lưu → Xóa', 'Click', 'Before:\n– Phiếu còn Đang tạo.\nAfter:\n– Gỡ file khỏi phiếu, ghi lịch sử File đính kèm, báo "Xóa file thành công".'],
        ['Bấm Lưu', 'Click', 'Before:\n– Phiếu phải còn Đang tạo và của chính người dùng.\nDuring:\n– Ghi chú bắt buộc ≤ 255 ký tự; sau khi gộp file cũ + mới phải còn ≥ 1 file.\n' + TRUOC_LUU + '\nAfter:\n– Ghi thay đổi; ghi nhận Thay đổi thông tin trong lịch sử.\n– Báo "Lưu thành công.", về danh sách.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa đổi gì → về danh sách; đã đổi → hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
    ],
})

# 2.7 Xem chi tiết ------------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết phiếu', 'uc': 'uc_xem', 'uc_ten': 'FR-07 Xem chi tiết phiếu nhập kho điều chỉnh kiểm kê',
    'qtc': 'Màn Xem chi tiết và Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết phiếu nhập kho điều chỉnh kiểm kê'],
        ['Mô tả', 'Xem toàn bộ thông tin 1 phiếu ở chế độ chỉ đọc, kèm khối Lịch sử; nút thao tác ở chân trang theo trạng thái và người dùng.'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK + '\n2. Phiếu thuộc phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Bấm Số phiếu ở danh sách (hoặc bấm thông báo).\n2. Hệ thống mở trang "Chi tiết phiếu nhập kho điều chỉnh kiểm kê: <số phiếu>": khối Thông tin chung (Phiếu kiểm kê, Kho, Ghi chú, Người duyệt và Ngày duyệt khi đã có; góc phải "<Người tạo> - <ngày giờ tạo>"), khối File đính kèm, khối Chi tiết, khối Lịch sử (thu gọn).'],
        ['Dòng sự kiện phụ', '• Phiếu Đang tạo của mình: chân trang có Sửa, In, Quay lại.\n• Phiếu Chờ duyệt + người dùng có quyền "%s": có thêm "Tạo phiếu nhập hàng".\n• Phiếu Đang hạch toán / Đã hạch toán: chỉ In, Quay lại.\n• Phiếu ngoài phạm vi / không tồn tại: chuyển trang "Không tìm thấy".' % Q_KT],
    ],
    'menu_them': ' => Số phiếu (liên kết)',
    'anh': [('17_detail_wait', 'Trang Chi tiết phiếu Chờ duyệt (người dùng có quyền Kế toán kho)'),
            ('17c_detail_done', 'Trang Chi tiết phiếu Đã hạch toán: có Người duyệt, Ngày duyệt')],
    'ui': ui(UI6, [
        ['Phiếu kiểm kê', 'Link', 'Read-only', 'Dữ liệu phiếu', 'Mở chi tiết phiếu kiểm kê ở tab mới.'],
        ['Kho, Ghi chú', 'Textbox', 'Read-only', 'Dữ liệu phiếu', 'Chỉ đọc.'],
        ['Người duyệt, Ngày duyệt', 'Textbox', 'Read-only / Ẩn', 'Dữ liệu phiếu', 'Chỉ hiện khi Kế toán kho đã lập phiếu nhập hàng.'],
        ['Người tạo - ngày giờ', 'Label', 'Read-only', 'Dữ liệu phiếu', 'Góc phải khối Thông tin chung.'],
        ['Khối File đính kèm', 'File', 'Read-only', 'File của phiếu', 'Xem trước, Tải xuống.'],
        ['Bảng Chi tiết', 'Table/Grid', 'Read-only', 'Dòng hàng', 'STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, Vị trí, Số lượng.'],
        ['Khối Lịch sử', 'Label', 'Enable', 'Thu gọn', 'Bấm "Xem lịch sử" để mở (mục 2.12).'],
        ['Nút Tạo phiếu nhập hàng', 'Button', 'Enable / Ẩn', 'Theo trạng thái', 'Phiếu Chờ duyệt + quyền "%s" (mục 2.8).' % Q_KT],
        ['Nút Sửa', 'Button', 'Enable / Ẩn', 'Theo trạng thái', 'Phiếu Đang tạo của chính người dùng.'],
        ['Nút In', 'Button', 'Enable', '–', 'In phiếu (mục 2.9).'],
        ['Nút Quay lại', 'Button', 'Enable', '–', 'Về danh sách.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở trang', 'System', 'Before:\n– Kiểm tra phạm vi dữ liệu (BR-02).\nAfter:\n– Hiển thị phiếu, tính các nút theo trạng thái và người dùng.'],
        ['Bấm Tạo phiếu nhập hàng / Sửa / In / Quay lại', 'Click', 'After:\n– Mở trang Thêm phiếu nhập hàng điều chỉnh kiểm kê / trang Sửa / xem trước bản in / về danh sách.'],
    ],
})

# 2.8 Tạo phiếu nhập hàng -----------------------------------------------------------
FR.append({
    'ten': 'Tạo phiếu nhập hàng (bước Kế toán kho)', 'uc': 'uc_nhaphang', 'uc_ten': 'FR-08 Tạo phiếu nhập hàng điều chỉnh kiểm kê',
    'qtc': 'Quy tắc chuyển trạng thái và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tạo phiếu nhập hàng từ phiếu nhập kho điều chỉnh kiểm kê'],
        ['Mô tả', 'Bước duyệt của phiếu: Kế toán kho lập phiếu nhập hàng điều chỉnh kiểm kê (phân hệ Tài chính) từ phiếu Chờ duyệt. Lưu phiếu nhập hàng thì phiếu nhập kho chuyển Đang hạch toán; "Lưu và duyệt" thì chuyển Đã hạch toán.'],
        ['Tác nhân', 'Người dùng có quyền "%s"' % Q_KT],
        ['Điều kiện ban đầu', DK + '\n2. Phiếu ở trạng thái Chờ duyệt.'],
        ['Dòng sự kiện chính', '1. Bấm "Tạo phiếu nhập hàng" ở cột Hành động hoặc chân trang Chi tiết.\n2. Hệ thống mở trang Thêm Phiếu nhập hàng điều chỉnh kiểm kê, ô Phiếu nhập kho chọn sẵn phiếu này, nạp dòng hàng và file đính kèm của phiếu.\n3. Kế toán kho hoàn tất và lưu phiếu nhập hàng (theo SRS màn Phiếu nhập hàng điều chỉnh kiểm kê).\n4. Hệ thống đổi trạng thái phiếu nhập kho: Lưu → Đang hạch toán; Lưu và duyệt → Đã hạch toán; ghi Người duyệt = Kế toán kho, Ngày duyệt = thời điểm lưu.\n5. Ghi nhận Thay đổi trạng thái trong lịch sử phiếu nhập kho, kèm ghi chú "Phiếu nhập hàng điều chỉnh kiểm kê <mã>."; phiếu kiểm kê chuyển Hoàn thành nếu đã xử lý hết.'],
        ['Dòng sự kiện phụ', '• Phiếu nhập hàng đang Đang tạo được "Lưu và duyệt" sau đó → phiếu nhập kho chuyển Đang hạch toán → Đã hạch toán.\n• Màn này KHÔNG có Từ chối / Hủy / Xóa phiếu.'],
    ],
    'menu_them': ' => Tạo phiếu nhập hàng {icon:btn_taophieunhaphang_row}',
    'ghi_chu_layout': 'Nút mở trang Thêm Phiếu nhập hàng điều chỉnh kiểm kê (phân hệ Tài chính) với phiếu này chọn sẵn.',
    'anh': [('17_detail_wait', 'Nút Tạo phiếu nhập hàng ở chân trang Chi tiết phiếu Chờ duyệt')],
    'ui': ui(UI4, [
        ['Nút Tạo phiếu nhập hàng (cột Hành động)', 'Button', 'Biểu tượng tài liệu có dấu cộng; chỉ hiện với phiếu Chờ duyệt và người có quyền "%s".' % Q_KT],
        ['Nút Tạo phiếu nhập hàng (chân trang Chi tiết)', 'Button', 'Nút chính màu xanh, cùng điều kiện.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Tạo phiếu nhập hàng', 'Click', 'After:\n– Mở trang Thêm Phiếu nhập hàng điều chỉnh kiểm kê, chọn sẵn phiếu nhập kho này.'],
        ['Kế toán kho lưu phiếu nhập hàng', 'System', 'After:\n– Phiếu nhập kho: Đang hạch toán (phiếu nhập hàng Đang tạo) hoặc Đã hạch toán (Lưu và duyệt); ghi Người duyệt, Ngày duyệt; ghi lịch sử Thay đổi trạng thái.'],
    ],
})

# 2.9 In phiếu ---------------------------------------------------------------------
FR.append({
    'ten': 'In phiếu', 'uc': 'uc_inphieu', 'uc_ten': 'FR-09 In phiếu nhập kho điều chỉnh kiểm kê',
    'qtc': 'Quy tắc màn In và bố cục bản in.',
    'gioi_thieu': [
        ['Tên chức năng', 'In phiếu nhập kho điều chỉnh kiểm kê'],
        ['Mô tả', 'In 1 phiếu theo mẫu "PHIẾU NHẬP KHO ĐIỀU CHỈNH KIỂM KÊ", phần đầu là tiêu đề công ty của phiếu.'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK + '\n2. Phiếu thuộc phạm vi dữ liệu của người dùng (mọi trạng thái).'],
        ['Dòng sự kiện chính', '1. Bấm In ở cột Hành động hoặc chân trang Chi tiết.\n2. Hệ thống mở cửa sổ "Xem trước phiếu nhập kho điều chỉnh kiểm kê <số phiếu>".\n3. Bấm In để mở hộp in của trình duyệt.'],
        ['Dòng sự kiện phụ', '• Thiếu mẫu in trên hệ thống → "Thiếu mẫu in phiếu nhập kho điều chỉnh kiểm kê.".'],
    ],
    'menu_them': ' => In {icon:btn_in_row}',
    'ghi_chu_layout': 'Cửa sổ Xem trước bản in được mở ngay trên màn hình danh sách / chi tiết theo đường dẫn ở trên.',
    'anh': [('19_print', 'Cửa sổ xem trước bản in phiếu')],
    'ui': ui(UI6, [
        ['Phần đầu bản in', 'Label', 'Read-only', 'Tiêu đề công ty', 'Logo, tên, địa chỉ công ty của phiếu.'],
        ['Thông tin phiếu', 'Label', 'Read-only', 'Dữ liệu phiếu', 'Số phiếu, Ngày lập, Phiếu kiểm kê, Kho, Ghi chú.'],
        ['Bảng in', 'Table/Grid', 'Read-only', 'Dòng hàng', 'STT, Tên hàng, Model, Mã hàng, ĐVT, Vị trí, SL nhập (số gọn, không thêm .00).'],
        ['Chân bản in', 'Label', 'Read-only', '–', '"Ngày <dd> Tháng <mm> Năm <yyyy>" (ngày in), "Người lập" + họ tên người tạo phiếu.'],
        ['Nút In / (x)', 'Button', 'Enable', '–', 'Mở hộp in của trình duyệt / đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In (dòng / chân trang)', 'Click', 'Before:\n– Kiểm tra phạm vi dữ liệu.\nAfter:\n– Dựng bản in theo mẫu, hiện cửa sổ xem trước.'],
        ['Bấm In trong cửa sổ', 'Click', 'After:\n– Mở hộp in của trình duyệt.'],
    ],
})

# 2.10 In danh sách -----------------------------------------------------------------
FR.append({
    'ten': 'In danh sách', 'uc': 'uc_in', 'uc_ten': 'FR-10 In danh sách phiếu',
    'qtc': 'Quy tắc màn In và bố cục bản in.',
    'gioi_thieu': [
        ['Tên chức năng', 'In danh sách phiếu nhập kho điều chỉnh kiểm kê'],
        ['Mô tả', 'In mọi dòng khớp bộ lọc theo mẫu "DANH SÁCH PHIẾU NHẬP KHO ĐIỀU CHỈNH KIỂM KÊ", tiêu đề công ty của người đăng nhập, 9 cột cố định.'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm In danh sách.\n2. Hệ thống mở cửa sổ "Xem trước danh sách phiếu nhập kho điều chỉnh kiểm kê".\n3. Bấm In để mở hộp in của trình duyệt.'],
        ['Dòng sự kiện phụ', '• Vượt 2,000 dòng: không in, báo "Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài." (BR-09).'],
    ],
    'menu_them': ' => In danh sách {icon:btn_indanhsach}',
    'ghi_chu_layout': 'Cửa sổ Xem trước bản in được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('19b_printlist', 'Cửa sổ xem trước bản in danh sách')],
    'ui': ui(UI6, [
        ['Phần đầu bản in', 'Label', 'Read-only', 'Tiêu đề công ty', 'Công ty của người đăng nhập.'],
        ['Bảng in', 'Table/Grid', 'Read-only', 'Theo bộ lọc', 'STT, Số phiếu, Phiếu kiểm kê, Kho, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái (không theo Tuỳ chỉnh cột).'],
        ['Chân bản in', 'Label', 'Read-only', '–', 'Ngày in, Người lập = người đăng nhập.'],
        ['Nút In / (x)', 'Button', 'Enable', '–', 'Mở hộp in / đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In danh sách', 'Click', 'After:\n– Dựng bản in theo bộ lọc hiện tại; vượt 2,000 dòng thì chỉ hiện câu nhắc.'],
        ['Bấm In', 'Click', 'After:\n– Mở hộp in của trình duyệt.'],
    ],
})

# 2.11 Xuất Excel ------------------------------------------------------------------
FR.append({
    'ten': 'Xuất Excel danh sách', 'uc': 'uc_xuat', 'uc_ten': 'FR-11 Xuất Excel danh sách phiếu',
    'qtc': 'Quy tắc Excel và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách phiếu ra Excel'],
        ['Mô tả', 'Xuất mọi dòng khớp bộ lọc (không chỉ trang đang xem) ra file danh_sach_phieu_nhap_kho_dieu_chinh_kiem_ke.xlsx, tiêu đề "DANH SÁCH PHIẾU NHẬP KHO ĐIỀU CHỈNH KIỂM KÊ", cột theo lựa chọn và thứ tự người dùng.'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất Excel", tích sẵn các cột đang hiện trên bảng.\n3. Người dùng tích / bỏ, kéo đổi thứ tự, bấm Xuất file.\n4. Hệ thống tải dữ liệu theo lô (cạnh nút hiện "Đã tải x/y dòng…", "Đang dựng file … dòng…"), dựng file và tải về; báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Không có dòng nào khớp bộ lọc → "Không có dữ liệu để xuất", không tải file.\n• Lỗi → "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất Excel')],
    'ui': ui(UI8, [
        ['Danh sách trường', 'Checkbox', 'Enable', '9 trường', 'Có (≥ 1)', 'Các cột đang hiện', 'Số phiếu, Phiếu kiểm kê, Ngày kiểm kê, Kho, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái. Kéo đổi thứ tự cột trong file; file luôn có cột STT đầu.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', 'Chọn / bỏ nhanh mọi trường.'],
        ['Dòng đếm', 'Label', 'Read-only', '–', '–', '–', '"Đang chọn x/9 trường".'],
        ['Nút Xuất file', 'Button', 'Enable', '–', '–', '–', 'Xuất file theo trường đã chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng, không xuất.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất file', 'Click', 'After:\n– Tải dữ liệu theo bộ lọc hiện tại và phạm vi dữ liệu, dựng file đúng thứ tự cột, tải về; báo kết quả.'],
        ['Kéo đổi thứ tự', 'Drag', 'After:\n– Đổi thứ tự cột trong file.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.12 Lịch sử ----------------------------------------------------------------------
FR.append({
    'ten': 'Xem lịch sử thay đổi',
    'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem lịch sử thay đổi phiếu'],
        ['Mô tả', 'Liệt kê các lần thao tác trên 1 phiếu (Tạo mới, Thay đổi thông tin, Thay đổi trạng thái), mới nhất ở trên, kèm người thực hiện, phòng ban, thời điểm, giá trị cũ → mới (Ghi chú, File đính kèm, Trạng thái) và ghi chú (vd mã phiếu nhập hàng).'],
        ['Tác nhân', NV],
        ['Điều kiện ban đầu', DK + '\n2. Phiếu thuộc phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Bấm Lịch sử ở cột Hành động → cửa sổ "Lịch sử thay đổi: <số phiếu>".\n2. Hoặc ở trang Chi tiết bấm "Xem lịch sử" ở khối Lịch sử.\n3. Hệ thống liệt kê các mốc; có nút Bộ lọc (loại hành động, người thực hiện, khoảng ngày).'],
        ['Dòng sự kiện phụ', '• Giá trị cũ in đỏ, giá trị mới in xanh.\n• Phiếu cũ lập trước khi có lịch sử có thể không có mốc nào.'],
    ],
    'menu_them': ' => Lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': 'Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối Lịch sử nằm cuối trang Chi tiết phiếu.',
    'anh': [('16_history', 'Cửa sổ Lịch sử thay đổi mở từ danh sách'), ('17b_detail_history', 'Khối Lịch sử ở trang Chi tiết')],
    'ui': ui(UI6, [
        ['Tiêu đề', 'Label', 'Read-only', '"Lịch sử thay đổi: <số phiếu>"', '–'],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Lọc theo loại hành động, người thực hiện, Từ ngày, Đến ngày.'],
        ['Mốc lịch sử', 'Label', 'Read-only', 'Mới nhất trên cùng', 'Thời điểm, tên hành động, "Người thực hiện: <họ tên> — <phòng ban>", trường đổi: cũ → mới, ghi chú.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lịch sử / Xem lịch sử', 'Click', 'Before:\n– Kiểm tra phạm vi dữ liệu.\nAfter:\n– Tải và hiển thị các mốc lịch sử của phiếu.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

FR_NAMES = ['FR-%02d %s' % (i + 1, f['ten']) for i, f in enumerate(FR)]
MT = {  # cột: Mọi người dùng | Người tạo phiếu | Tạo + Xử lý PKK | Kế toán kho
    0: ['Có (phiếu mình tạo + theo phạm vi xem)', 'Có', 'Có', 'Có (+ mọi phiếu Chờ duyệt)'],
    1: ['Có', 'Có', 'Có', 'Có'], 2: ['Có', 'Có', 'Có', 'Có'],
    3: ['Không', '–', 'Có', 'Không (nếu thiếu 2 quyền)'],
    4: ['Không', 'Có (phiếu Đang tạo của mình)', 'Có', 'Không'],
    5: ['Không', 'Có (phiếu Đang tạo của mình)', '–', 'Không'],
    6: ['Có (trong phạm vi)', 'Có', 'Có', 'Có'],
    7: ['Không', 'Không', 'Không', 'Có (phiếu Chờ duyệt)'],
    8: ['Có', 'Có', 'Có', 'Có'], 9: ['Có', 'Có', 'Có', 'Có'], 10: ['Có', 'Có', 'Có', 'Có'], 11: ['Có', 'Có', 'Có', 'Có'],
}

S = {
    'ten': TEN, 'ten_ngan': 'phiếu nhập kho điều chỉnh kiểm kê', 'phan_he': 'Kho',
    'menu': [('Kho', 'menu_phanhe'), ('Nhập kho', 'menu_nhom'), (TEN, 'menu_muc')],
    'muc_dich': [
        'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho việc NHẬP VÀO KHO phần hàng THỪA phát hiện khi kiểm kê hàng hóa.',
        'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
        'Làm rõ nguồn dữ liệu: dòng hàng lấy từ phiếu kiểm kê hàng hóa (Chờ xử lý / Đang xử lý), mỗi phiếu kiểm kê chỉ lập được 1 phiếu nhập kho điều chỉnh.',
        'Làm rõ tác động số liệu: Gửi duyệt cộng ngay tồn kho vật lý; Kế toán kho lập phiếu nhập hàng điều chỉnh kiểm kê để hạch toán.',
        'Làm rõ phạm vi dữ liệu theo quyền xem và quyền Kế toán kho.',
    ],
    'thuat_ngu': [
        ['Phiếu nhập kho điều chỉnh kiểm kê', 'Phiếu nhập vào kho phần hàng thừa chưa xử lý của 1 phiếu kiểm kê hàng hóa tại 1 kho. Số phiếu dạng PNKĐCKK-<5 chữ số>.'],
        ['Phiếu kiểm kê hàng hóa', 'Phiếu ghi kết quả kiểm kê theo hàng hóa (màn Kiểm kê theo hàng hóa); là nguồn của phiếu nhập kho điều chỉnh.'],
        ['Hàng thừa', 'Dòng kết quả kiểm kê có số thực tế lớn hơn số sổ sách; số lượng cần nhập = số chênh − số đã xử lý.'],
        ['Lô nhập điều chỉnh', 'Lô hàng hệ thống sinh cho mỗi dòng chi tiết khi Gửi duyệt; làm tăng tồn kho vật lý tại vị trí.'],
        ['Phiếu nhập hàng điều chỉnh kiểm kê', 'Phiếu do Kế toán kho lập ở phân hệ Tài chính từ phiếu nhập kho Chờ duyệt, để hạch toán tồn kho kế toán.'],
        ['Kế toán kho', 'Người dùng có quyền "Kế toán kho": thấy mọi phiếu Chờ duyệt, nhận thông báo, lập phiếu nhập hàng.'],
    ],
    'trang_thai': {
        'cau_dan': 'Phiếu có 4 trạng thái. Người lập quyết định Đang tạo / Chờ duyệt (nút Lưu / Gửi duyệt); hai trạng thái sau do hệ thống '
                   'tự chuyển khi Kế toán kho lập phiếu nhập hàng điều chỉnh kiểm kê. Màn KHÔNG có Xóa, Hủy, Từ chối.',
        'rows': [
            ['Đang tạo', 'Đã lưu nháp, CHƯA nhập hàng vào kho. Chỉ người tạo thấy.', 'Xem, Sửa, Gửi duyệt, In, Lịch sử', 'Người tạo phiếu'],
            ['Chờ duyệt', 'Đã gửi duyệt: hàng thừa đã nhập vào kho (tồn vật lý tăng), chờ Kế toán kho hạch toán.', 'Xem, In, Lịch sử, Tạo phiếu nhập hàng (Kế toán kho)', 'Người lập bấm Gửi duyệt'],
            ['Đang hạch toán', 'Kế toán kho đã lưu phiếu nhập hàng điều chỉnh kiểm kê ở trạng thái Đang tạo.', 'Xem, In, Lịch sử', 'Tự chuyển khi Kế toán kho lưu phiếu nhập hàng'],
            ['Đã hạch toán', 'Phiếu nhập hàng điều chỉnh kiểm kê đã "Lưu và duyệt" (tồn kho kế toán + bút toán đã ghi).', 'Xem, In, Lịch sử', 'Tự chuyển khi Kế toán kho Lưu và duyệt phiếu nhập hàng'],
        ],
        'anh': 'state_flow',
        'ghi_chu': ['Mọi lần đổi trạng thái được ghi nhận trong lịch sử phiếu (Thay đổi trạng thái: cũ → mới). Phiếu kiểm kê nguồn chuyển '
                    'Đang xử lý khi lập phiếu nhập kho điều chỉnh, và Hoàn thành khi mọi chênh lệch đã xử lý xong.'],
    },
    'quyen_truoc': ['Mục menu không gắn quyền: mọi người dùng đăng nhập đều vào được màn và thấy phiếu do mình tạo. Các quyền liên quan:'],
    'quyen_rows': [
        [Q_XEM, 'Quyền xem có phạm vi (mức Tổng công ty / Công ty) — xem bảng phạm vi bên dưới.'],
        [Q_TAO, 'Thấy nút Tạo mới, mở trang Thêm, lưu / gửi duyệt phiếu mới.'],
        [Q_XL, 'Cần CÙNG với quyền trên để có phiếu kiểm kê trong ô "Phiếu kiểm kê" (điều kiện của phiếu kiểm kê nguồn).'],
        [Q_KT, 'Thấy thêm mọi phiếu Chờ duyệt (mọi công ty), có nút "Tạo phiếu nhập hàng", nhận thông báo khi có phiếu gửi duyệt cùng công ty.'],
        ['(người tạo phiếu)', 'Sửa, Gửi duyệt phiếu Đang tạo của chính mình — không cần quyền riêng.'],
    ],
    'pham_vi_truoc': ['Phạm vi dữ liệu theo quyền "%s" (xét từ trên xuống, có mức nào trước thì áp mức đó):' % Q_XEM],
    'pham_vi_rows': [
        ['1', Q_XEM + ' — mức Tổng công ty', 'Phiếu của mọi công ty; ô lọc Công ty và Phòng ban dùng được.'],
        ['2', Q_XEM + ' — mức Công ty', 'Phiếu thuộc công ty đang làm việc của người dùng; ô Phòng ban dùng được.'],
        ['3', '(không có quyền xem)', 'Chỉ phiếu do chính người dùng tạo.'],
        ['+', Q_KT, 'Cộng thêm mọi phiếu Chờ duyệt, không giới hạn công ty.'],
    ],
    'pham_vi_sau': ['Ở mọi mức, phiếu Đang tạo của NGƯỜI KHÁC không bao giờ hiện. Công ty / phòng ban của phiếu = của NGƯỜI LẬP PHIẾU KIỂM KÊ '
                    '(BR-05). Phạm vi áp như nhau cho danh sách, chi tiết, lịch sử, in và xuất Excel; ngoài phạm vi mở thẳng đường dẫn thì '
                    'chuyển trang "Không tìm thấy".'],
    'ma_tran': [['Chức năng', 'Mọi người dùng', 'Người tạo phiếu', '"%s" + "%s"' % (Q_TAO, Q_XL), Q_KT]] +
               [[f] + MT[i] for i, f in enumerate(FR_NAMES)],
    'ma_tran_widths': [2.0, 1.3, 1.2, 1.3, 1.2],
    'quyen_sau': ['Phạm vi dữ liệu của mọi chức năng theo bảng quyền phạm vi ở trên; một người có thể có đồng thời nhiều quyền.'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Nguồn phiếu = phiếu kiểm kê hàng hóa', ['– Chỉ phiếu kiểm kê Chờ xử lý / Đang xử lý, còn hàng thừa chưa xử lý (tổng chênh của hàng ≠ 0), CHƯA có phiếu nhập kho điều chỉnh.', '– Người lập cần quyền "%s" + "%s".' % (Q_TAO, Q_XL), '– Kho chọn được = các kho của phiếu kiểm kê; dòng hàng = hàng thừa chưa xử lý tại kho, số lượng = số chênh − đã xử lý.'], ['Lập phiếu']),
        ('BR-02', 'Phạm vi dữ liệu', ['– Tổng công ty → mọi phiếu; Công ty → phiếu của công ty đang làm việc; không có quyền xem → phiếu mình tạo; Kế toán kho thêm mọi phiếu Chờ duyệt.', '– Phiếu Đang tạo của người khác luôn ẩn; ngoài phạm vi mở thẳng thì trang "Không tìm thấy".'], ['Mọi chức năng']),
        ('BR-03', 'Số phiếu', ['– Dạng PNKĐCKK-<số thứ tự 5 chữ số>, sinh khi lưu lần đầu, không đổi.'], ['Lập phiếu']),
        ('BR-04', 'Thao tác theo trạng thái', ['– Sửa / Gửi duyệt: chỉ phiếu Đang tạo của chính người tạo.', '– Tạo phiếu nhập hàng: phiếu Chờ duyệt + quyền "%s".' % Q_KT, '– In, Lịch sử: mọi trạng thái. Không có Xóa / Hủy / Từ chối.', '– Nút không dùng được thì ẩn.'], ['Xem danh sách', 'Sửa', 'Xem chi tiết']),
        ('BR-05', 'Tổ chức của phiếu', ['– Công ty / phòng ban của phiếu = của người lập phiếu kiểm kê nguồn (không có thì lấy của người lập phiếu nhập).'], ['Lập phiếu', 'Tìm kiếm và lọc']),
        ('BR-06', 'Một phiếu kiểm kê chỉ 1 phiếu nhập kho điều chỉnh', ['– Khi lưu, hệ thống khóa phiếu kiểm kê và kiểm lại điều kiện: người thứ 2 lưu cùng lúc nhận "Phiếu kiểm kê không còn lập được phiếu nhập kho điều chỉnh. Vui lòng load lại trang".', '– Dòng hàng được lấy LẠI từ phiếu kiểm kê lúc lưu (không lấy theo dữ liệu trên màn).'], ['Lập phiếu']),
        ('BR-07', 'Dữ liệu bắt buộc', ['– Phiếu kiểm kê, Kho (khi lập), Ghi chú 1–255 ký tự, ít nhất 1 file đính kèm.', '– File: pdf, png, jpg, jpeg; tối đa 20MB/file ("File đính kèm – Dung lượng tối đa 20MB.").', '– Sửa chỉ đổi Ghi chú và File; phiếu kiểm kê, kho, dòng hàng giữ nguyên.'], ['Lập phiếu', 'Sửa']),
        ('BR-08', 'Gửi duyệt nhập kho ngay', ['– Mỗi dòng chi tiết sinh 1 lô nhập điều chỉnh và cộng tồn kho vật lý tại kho + vị trí của dòng (số lượng quy đổi theo hệ số ĐVT).', '– Thông báo "[NKĐCKK] Chờ duyệt: <số phiếu>. Người gửi: <họ tên>. Kho: <tên kho>" tới người có quyền "%s" cùng công ty người gửi.' % Q_KT, '– Lưu (Đang tạo) không tác động tồn kho.'], ['Gửi duyệt']),
        ('BR-09', 'In và xuất', ['– In danh sách và Xuất Excel theo đúng bộ lọc + phạm vi (mọi trang); in tối đa 2,000 dòng, vượt thì không in.', '– Không có dữ liệu thì không xuất file.'], ['In danh sách', 'Xuất Excel']),
        ('BR-10', 'Ghi lịch sử', ['– Tạo mới; Thay đổi thông tin (Ghi chú, File đính kèm, kể cả xóa file đã lưu); Thay đổi trạng thái (Gửi duyệt từ trang Sửa, Chờ duyệt → Đang hạch toán → Đã hạch toán kèm mã phiếu nhập hàng).'], ['Lập phiếu', 'Sửa', 'Gửi duyệt', 'Tạo phiếu nhập hàng']),
        ('BR-11', 'Thao tác xong quay về danh sách', ['– Lưu, Gửi duyệt xong thì về danh sách; "Lưu và tiếp tục" ở lại trang Thêm với form trống.'], ['Lập phiếu', 'Sửa', 'Gửi duyệt']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây mở màn này, đọc hoặc dùng dữ liệu do Phiếu nhập kho điều chỉnh kiểm kê ghi ra (phiếu, dòng hàng, lô nhập điều chỉnh).',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng (theo quyền)',
    'mains': [('FR-01', 'Xem danh sách phiếu', 'view'), ('FR-04', 'Lập phiếu nhập kho điều chỉnh', 'crud'),
              ('FR-05', 'Gửi duyệt phiếu', 'action'), ('FR-06', 'Sửa phiếu', 'crud'),
              ('FR-08', 'Tạo phiếu nhập hàng', 'action'), ('FR-09', 'In phiếu', 'io'),
              ('FR-10', 'In danh sách', 'io'), ('FR-11', 'Xuất Excel danh sách', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc danh sách', 'view'), ('FR-03', 'Cài đặt bộ lọc, tuỳ chỉnh cột', 'view'),
             ('FR-07', 'Xem chi tiết phiếu', 'view'), ('FR-12', 'Xem lịch sử thay đổi', 'view')],
    'rieng': [('FR-04', 'Lập phiếu nhập kho điều chỉnh', 'crud', 'uc_them'), ('FR-05', 'Gửi duyệt phiếu', 'action', 'uc_guiduyet'),
              ('FR-06', 'Sửa phiếu', 'crud', 'uc_sua'), ('FR-07', 'Xem chi tiết phiếu', 'view', 'uc_xem'),
              ('FR-08', 'Tạo phiếu nhập hàng', 'action', 'uc_nhaphang'), ('FR-09', 'In phiếu', 'io', 'uc_inphieu'),
              ('FR-10', 'In danh sách', 'io', 'uc_in'), ('FR-11', 'Xuất Excel danh sách', 'io', 'uc_xuat')],
}

STATES = [('start', '', None), ('tao', 'Đang tạo', '#e2e8f0'), ('cho', 'Chờ duyệt', '#fef3c7'),
          ('dang', 'Đang hạch toán', '#dbeafe'), ('da', 'Đã hạch toán', '#dcfce7')]
TRANS = [('start', 'tao', 'Lưu'), ('start', 'cho', 'Gửi duyệt khi lập'), ('tao', 'cho', 'Gửi duyệt'),
         ('cho', 'dang', 'KT kho lưu phiếu nhập hàng'), ('dang', 'da', 'Lưu và duyệt'),
         ('cho', 'da', 'Lưu và duyệt ngay')]

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    L.draw_state_flow(os.path.join(scr.uml, 'state_flow.png'), STATES, TRANS)
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))

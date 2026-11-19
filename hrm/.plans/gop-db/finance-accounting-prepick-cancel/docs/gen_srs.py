# -*- coding: utf-8 -*-
"""SRS - Phiếu huỷ hàng giữ kế toán (STT 202) — chép khuôn màn mẫu finance-declare-debt-beginning/docs/kh/gen_srs.py.

Nguồn (code HRM origin/develop, 02/11/2026):
  FE hrm-client/pages/finance/accounting-prepick-cancels/{index, create, _id/index}.vue,
     components/{AccountingPrepickCancelForm.vue, export-excel.js}, components/finance/prepick/{PrepickStockSearchModal,
     PrepickHistoryPanel, PrepickHistoryModal}.vue, components/subsystem-menu/finance.js
  BE Modules/Finance: Entities/AccountingPrepickCancel/*, Services/{AccountingPrepickCancelService,
     AccountingPrepickCancelHistoryService, PrepickStockService}.php, Http/Controllers/V1/AccountingPrepickCancelController.php,
     Http/Requests/AccountingPrepickCancel/AccountingPrepickCancelStoreRequest.php, Resources/views/prints/accounting-prepick-cancel*.blade.php
  Ảnh: capture.js (dev-hrm). Phần 5: dò code FE/BE 02/11/2026.
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'xuat-tai-lieu-chuyen-doi')))
import _lib_phieu as L  # noqa: E402
from _lib_phieu import ui, UI4, UI4W, UI6, UI6W, UI7, UI7W, UI8, UI8W, TRUOC_LUU  # noqa: E402

TEN = 'Phiếu huỷ hàng giữ kế toán'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
QUYEN = 'Quản lý giữ hàng'
Q = 'Người dùng có quyền thực hiện chức năng (quyền "%s")' % QUYEN
DK = '1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền "%s".' % QUYEN
DK_XEM = DK + '\n3. Phiếu thuộc phạm vi dữ liệu của người dùng (BR-02).'
TRANG = 'Trang %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'
POPUP = 'Modal %s được mở ngay trên màn hình %s theo đường dẫn ở trên.'

# ------------------------------------------------------------------ Phần 5 (dò code 02/11/2026)
GH = 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng'
P5 = [
    ('Tài chính', 'Danh sách hàng giữ (số đang giữ giảm sau khi lập phiếu; lịch sử lô có dòng giảm gắn mã phiếu, bấm mở chi tiết phiếu)', GH),
    ('Tài chính', 'Hàng sắp hết hạn giữ (số đang giữ của lô sau khi bị huỷ)', GH),
    ('Tài chính', 'Yêu cầu hủy hàng giữ, Phiếu hủy hàng giữ (số có thể huỷ còn lại của nhân viên)', GH),
    ('Tài chính', 'Yêu cầu gia hạn hàng giữ, Phiếu Yêu cầu điều chuyển hàng giữ (chỉ còn lô / số giữ chưa bị huỷ)', GH),
    ('Bán hàng', 'Báo cáo theo dõi giữ hàng (chứng từ huỷ giữ dẫn tới phiếu huỷ hàng giữ kế toán)', 'Bán hàng => Báo cáo => Hàng giữ'),
    ('Danh mục', 'Hàng hoá (hàng đã có trên phiếu huỷ hàng giữ kế toán không xoá cứng được)', 'Danh mục => Hàng hoá'),
    ('Hệ thống', 'Chuông thông báo của nhân viên bị huỷ hàng (thông báo kèm mã phiếu, bấm mở chi tiết phiếu)', 'Biểu tượng chuông ở thanh trên cùng'),
]

FR = []

# 2.1 Xem danh sách -------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách phiếu huỷ hàng giữ kế toán',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách phiếu huỷ hàng giữ kế toán'],
        ['Mô tả', 'Hiển thị các phiếu huỷ hàng giữ do kế toán lập trong phạm vi dữ liệu của người dùng, có phân trang, sắp xếp và nút In, Lịch sử ở từng dòng. Phiếu lập xong là chốt nên danh sách không có Sửa, Xóa.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), phiếu tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Không có phiếu khớp → bảng hiện "Không có dữ liệu phù hợp."\n• Không có quyền "%s" → thay bảng bằng biểu tượng khoá và câu "Bạn chưa có quyền Quản lý giữ hàng nên không xem được màn này.", không có bộ lọc, không có nút.\n• Phạm vi dữ liệu theo Phần 2 (BR-02).' % QUYEN],
    ],
    'anh': [('01_list', 'Màn danh sách Phiếu huỷ hàng giữ kế toán lúc mới truy cập')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Phiếu hủy hàng giữ kế toán', 'Tiêu đề khối danh sách và tiêu đề trang.'],
        ['Nút Tạo mới', 'Button', 'Enable', 'Hiển thị', 'Mở trang "Thêm phiếu hủy hàng giữ kế toán" (mục 2.4).'],
        ['Nút In', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ xem trước bản in danh sách (mục 2.8).'],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất Excel" (mục 2.9).'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.3).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa.'],
        ['Cột Mã phiếu', 'Table/Grid', 'Read-only', 'Hiển thị', '- Dạng KTPHHG-<5 chữ số> (BR-04).\n- Sắp xếp được. Chữ dạng liên kết: bấm mở trang Chi tiết (mục 2.6).\n- Cột khóa.'],
        ['Cột Hủy của nhân viên', 'Table/Grid', 'Read-only', 'Hiển thị', 'Họ tên nhân viên BỊ huỷ hàng giữ (chủ lô hàng giữ).'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', '"Họ tên - Mã phòng ban" của kế toán lập phiếu.'],
        ['Cột Người cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', '"Họ tên - Mã phòng ban". Phiếu không sửa được nên trùng Người tạo.'],
        ['Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Ghi chú', 'Table/Grid', 'Read-only', 'Ẩn', 'Ghi chú phiếu; mặc định ẩn, bật ở Tuỳ chỉnh cột. Trống thì để trống.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- In: mở bản in phiếu (mục 2.7).\n- Lịch sử: mở cửa sổ lịch sử (mục 2.10).\n- Không có Sửa, Xóa. Cột khóa.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Kiểm tra quyền "%s"; thiếu quyền → màn báo chưa có quyền thay cho bảng.\nAfter:\n– Tải trang 1 theo phạm vi dữ liệu (BR-02), phiếu tạo gần nhất trên cùng; khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút).' % QUYEN],
        ['Bấm tiêu đề cột Mã phiếu / Ngày tạo / Ngày cập nhật', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, quay về trang 1, tải lại dữ liệu.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp, tải lại dữ liệu; đổi số dòng thì quay về trang 1.'],
        ['Bấm Mã phiếu', 'Click', 'After:\n– Mở trang Chi tiết phiếu (mục 2.6).'],
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc danh sách',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách phiếu'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh (theo mã phiếu) và các ô lọc ở khu vực Tìm kiếm nâng cao.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn danh sách.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập mã phiếu rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô tìm nhanh chỉ lọc khi bấm Tìm kiếm / Enter; các ô lọc khác tự tải lại ngay khi đổi giá trị.\n• Bấm Làm mới → xoá mọi điều kiện, sắp xếp về mặc định và tải lại danh sách.\n• Ô Công ty chỉ hiện với tài khoản quản trị cao nhất (BR-02).\n• Hệ thống ghi nhớ bộ lọc 10 phút khi rời màn rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực Tìm kiếm nâng cao ở trạng thái mở (tài khoản quản trị cao nhất: có ô Công ty)')],
    'ui': ui(UI7, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', '- Placeholder "Tìm theo mã phiếu...".\n- Tìm gần đúng CHỈ theo mã phiếu.'],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Áp dụng từ khóa và các ô lọc.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá mọi điều kiện lọc, sắp xếp về mặc định, tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực ô lọc (khi mở, nút đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" (mục 2.3).'],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Trống', 'Chỉ hiện với tài khoản quản trị cao nhất; lọc theo công ty của phiếu (công ty người lập).'],
        ['Ô Hủy của nhân viên', 'Dropdown', 'Enable', 'Nhân viên đang làm việc', 'Trống', 'Lọc phiếu huỷ hàng của nhân viên được chọn.'],
        ['Ô Người tạo', 'Dropdown', 'Enable', 'Nhân viên đang làm việc', 'Trống', 'Lọc phiếu do người được chọn lập.'],
        ['Ô Tên/mã hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Placeholder "Nhập tên hoặc mã hàng hóa"; ra phiếu có ít nhất 1 hàng hoá chứa chữ đã nhập trong tên HOẶC mã.'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy, Từ → Đến', 'Trống', 'Lọc theo ngày lập phiếu, lấy trọn cả 2 ngày đầu mút.'],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm Tìm kiếm / nhấn Enter ở ô tìm nhanh', 'Click', 'After:\n– Áp đồng thời từ khóa và các ô lọc, tải lại bảng từ trang 1.'],
        ['Đổi giá trị ô lọc', 'Change', 'After:\n– Tải lại bảng từ trang 1 ngay.'],
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
        ['Dòng sự kiện chính', '1. Bấm "Cài đặt bộ lọc" (hoặc biểu tượng Cấu hình cột hiển thị).\n2. Tích / bỏ tích, kéo biểu tượng ba gạch để đổi thứ tự.\n3. Bấm Lưu: hệ thống lưu cấu hình và áp dụng ngay.'],
        ['Dòng sự kiện phụ', '• Bấm Đóng: bỏ thay đổi.\n• Cài đặt bộ lọc có nút "Khôi phục mặc định".\n• Cột STT, Mã phiếu, Hành động không bỏ được.'],
    ],
    'menu_them': ' => Cài đặt bộ lọc {icon:btn_caidatboloc} / Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': 'Modal Cài đặt bộ lọc và Modal Tuỳ chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('26_filtercfg', 'Cửa sổ Cài đặt bộ lọc'), ('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột')],
    'ui': ui(UI6, [
        ['Danh sách ô lọc', 'Checkbox', 'Enable', '4 ô (5 ô với tài khoản quản trị cao nhất)', 'Tích ô lọc muốn hiện, kéo đổi thứ tự.'],
        ['Nút Khôi phục mặc định', 'Button', 'Enable', '–', 'Đưa cấu hình ô lọc về mặc định.'],
        ['Danh sách cột', 'Checkbox', 'Enable', '8/9 cột (Ghi chú tắt)', 'Tích cột muốn hiện; STT, Mã phiếu, Hành động bị khóa. Kéo đổi thứ tự.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Chọn / bỏ nhanh mọi cột (trừ cột khóa).'],
        ['Nút Lưu', 'Button', 'Enable', '–', 'Lưu cấu hình theo người dùng, áp dụng ngay.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ, không lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình theo người dùng, đóng cửa sổ, bảng / khu vực lọc vẽ lại theo cấu hình.'],
        ['Kéo biểu tượng ba gạch', 'Drag', 'After:\n– Đổi thứ tự dòng trong cửa sổ.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ, không lưu.'],
    ],
})

# 2.4 Lập phiếu (Duyệt) ----------------------------------------------------------
FR.append({
    'ten': 'Lập phiếu huỷ hàng giữ kế toán (Duyệt)', 'uc': 'uc_them', 'uc_ten': 'FR-04 Lập phiếu huỷ hàng giữ kế toán',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Lập phiếu huỷ hàng giữ kế toán'],
        ['Mô tả', 'Kế toán chọn 1 nhân viên, thêm các hàng hoá nhân viên đó đang giữ (mục 2.5); mỗi hàng hoá chọn 1 hoặc nhiều khách hàng đang được giữ hàng, nhập số lượng huỷ và đơn vị tính. Bấm Duyệt là LƯU phiếu và TRỪ TỒN HÀNG GIỮ ngay (BR-05), không có bước nháp / gửi duyệt; sau đó phiếu không sửa, không xoá được.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở trang "Thêm phiếu hủy hàng giữ kế toán"; góc phải khối Thông tin chung hiện "<Người đăng nhập> - <ngày giờ hiện tại>"; khối Chi tiết ghi "Chọn nhân viên trước để thêm hàng hóa".\n3. Người dùng chọn "Hủy của nhân viên" → hiện nút "Thêm hàng hóa".\n4. Bấm "Thêm hàng hóa", tích hàng và bấm "Chọn (n)" (mục 2.5). Mỗi hàng hoá được thêm 1 dòng, ô Khách hàng tự chọn khách đầu tiên, ĐVT là đơn vị cơ bản.\n5. Mỗi dòng khách hàng nhập Duyệt hủy; đổi ĐVT nếu cần; bấm "Thêm khách hàng" để huỷ cho khách khác của cùng hàng hoá.\n6. Bấm Duyệt → hệ thống kiểm tra dữ liệu trên form, hiện hộp "Xác nhận duyệt".\n7. Bấm Duyệt trong hộp: hệ thống kiểm tra lại, sinh mã phiếu (BR-04), ghi phiếu + hàng hoá + dòng khách hàng, trừ tồn hàng giữ từng dòng theo thứ tự hạn giữ sớm trước (BR-05).\n8. Ghi nhận Tạo mới trong lịch sử phiếu ("Đã trừ tồn hàng giữ trên N lô.").\n9. Gửi thông báo cho nhân viên bị huỷ hàng (BR-09).\n10. Báo "Duyệt thành công.", quay về danh sách.'],
        ['Dòng sự kiện phụ', '• Bấm "Lưu và tiếp tục": xử lý như Duyệt rồi mở lại trang Thêm trống để lập tiếp.\n• Thiếu ô bắt buộc → báo đỏ dưới ô + toast "Bạn chưa nhập đầy đủ thông tin.", cuộn tới ô lỗi đầu tiên, không hiện hộp xác nhận.\n• Số không hợp lệ (vượt số có thể hủy, bằng 0…) → toast lỗi đầu tiên kèm tên hàng, ví dụ ""<tên hàng>": Vượt quá số có thể hủy (tối đa 4)".\n• Đổi / xoá nhân viên khi đã có hàng → hộp "Đổi nhân viên" ("Đổi nhân viên sẽ xóa toàn bộ hàng hóa đã chọn. Bạn có chắc chắn không?"); đồng ý thì bảng Chi tiết bị xoá trắng, Hủy thì giữ nhân viên cũ.\n• Tồn giữ vừa bị chứng từ khác lấy bớt → bấm Duyệt bị từ chối, lỗi gắn đúng dòng, KHÔNG tạo phiếu, KHÔNG trừ dòng nào (BR-06).\n• Bấm Hủy ở hộp "Xác nhận duyệt" → về form, không lưu.\n• Bấm Quay lại: chưa nhập gì thì về danh sách; đã nhập thì hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', 'Nút Duyệt chỉ xử lý 1 lần cho tới khi có kết quả, tránh trừ tồn 2 lần.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': TRANG % '"Thêm phiếu hủy hàng giữ kế toán"',
    'anh': [('10_create', 'Trang Thêm phiếu hủy hàng giữ kế toán lúc mới mở'),
            ('11_validate', 'Bấm Duyệt khi chưa nhập số lượng: báo đỏ dưới ô và toast'),
            ('10b_create_filled', 'Đã chọn nhân viên, 2 hàng hoá (hàng 1 huỷ cho 2 khách, hàng 2 dùng ĐVT Túi)'),
            ('10c_over', 'Nhập vượt số có thể hủy: báo đỏ, giữ nguyên số đã nhập'),
            ('13_confirm', 'Hộp Xác nhận duyệt'),
            ('15_change_emp', 'Hộp hỏi khi đổi nhân viên lúc đã có hàng hoá'),
            ('18_unsaved', 'Hộp Thông tin chưa lưu khi bấm Quay lại')],
    'ui': ui(UI8, [
        ['Người tạo - ngày giờ', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại', 'Góc phải khối Thông tin chung.'],
        ['Hủy của nhân viên', 'Dropdown', 'Enable', 'Mọi nhân viên đang làm việc (mọi công ty)', 'Có', 'Trống', '- Placeholder "Chọn nhân viên"; có nút x xoá nhanh.\n- Bỏ trống mà bấm Duyệt: "Bắt buộc phải chọn".'],
        ['Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Placeholder "Nhập ghi chú"; không gõ quá 255 ký tự.'],
        ['Nút Thêm hàng hóa', 'Button', 'Enable / Ẩn', '–', '–', '–', 'Chỉ hiện khi đã chọn nhân viên; mở cửa sổ "Hàng đang giữ của nhân viên" (mục 2.5).'],
        ['Cột STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu', 'Table/Grid', 'Read-only', '–', '–', 'Theo hàng đã chọn', 'Gộp ô theo số dòng khách hàng của hàng hoá. Trống thì để trống.'],
        ['Khách hàng', 'Dropdown', 'Enable', 'Khách nhân viên còn số có thể huỷ > 0 cho hàng này', 'Có', 'Khách đầu tiên (theo tên)', '- Khách đã chọn ở dòng khác của CÙNG hàng hoá không hiện lại (BR-07).\n- Bỏ trống: "Bắt buộc phải chọn".'],
        ['Nút xoá khách hàng', 'Button', 'Enable / Ẩn', '–', '–', '–', 'Biểu tượng thùng rác cạnh ô Khách hàng; chỉ hiện khi hàng có từ 2 khách.'],
        ['Liên kết Thêm khách hàng', 'Link', 'Enable / Ẩn', '–', '–', '–', 'Thêm 1 dòng khách cho hàng hoá (tự chọn khách tiếp theo); ẩn khi đã chọn hết khách.'],
        ['Có thể hủy', 'Label', 'Read-only', 'Số ≥ 0', '–', 'Theo khách + ĐVT', 'Số có thể huỷ (BR-08) quy theo ĐVT đang chọn, làm tròn XUỐNG 2 chữ số thập phân. Chỉ có ở trang Thêm.'],
        ['Duyệt hủy', 'Textbox', 'Enable', 'Số > 0, ≤ Có thể hủy, tối đa 2 chữ số thập phân', 'Có', 'Trống', '- Placeholder "Nhập số lượng"; chỉ nhận số và dấu chấm thập phân.\n- Trống: "Chưa nhập số lượng"; ≤ 0: "Phải lớn hơn 0"; vượt: "Vượt quá số có thể hủy (tối đa X)" — giữ nguyên số đã gõ; quy đổi về 0: "Số lượng quá nhỏ so với đơn vị tính đã chọn."'],
        ['Đơn vị tính', 'Dropdown', 'Enable', 'Mọi ĐVT của hàng hoá', 'Có', 'Đơn vị cơ bản', 'Đổi ĐVT thì Có thể hủy tính lại và kiểm lại số đã nhập ngay.'],
        ['Nút xoá dòng hàng', 'Button', 'Enable', '–', '–', '–', 'Thùng rác cuối dòng hàng: bỏ hàng hoá cùng mọi dòng khách, không hỏi lại.'],
        ['Nút Duyệt', 'Button', 'Enable / Ẩn', '–', '–', '–', 'Chỉ hiện khi đã chọn nhân viên và có ít nhất 1 hàng hoá. Lưu + trừ tồn ngay.'],
        ['Nút Lưu và tiếp tục', 'Button', 'Enable / Ẩn', '–', '–', '–', 'Hiện cùng điều kiện với Duyệt; lưu + trừ tồn rồi mở lại trang Thêm trống.'],
        ['Nút Quay lại', 'Button', 'Enable', '–', '–', '–', 'Về danh sách (đã nhập thì hỏi "Thông tin chưa lưu").'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'After:\n– Mở trang Thêm trống.'],
        ['Chọn / đổi / xoá Hủy của nhân viên', 'Change', 'After:\n– Chưa có hàng: nhận nhân viên mới, hiện nút Thêm hàng hóa.\n– Đã có hàng: hỏi "Đổi nhân viên"; Đổi nhân viên → xoá trắng bảng Chi tiết; Hủy → giữ nhân viên cũ.'],
        ['Đổi Khách hàng / ĐVT, nhập Duyệt hủy', 'Change', 'After:\n– Tính lại Có thể hủy, kiểm số ngay và báo đỏ dưới ô nếu sai.'],
        ['Bấm Duyệt / Lưu và tiếp tục', 'Click', 'Before:\n– Kiểm tra trên form: có nhân viên, ≥ 1 hàng hoá, mỗi dòng đủ Khách hàng, ĐVT, Duyệt hủy hợp lệ. Sai → báo lỗi, không hiện hộp xác nhận.\nDuring:\n– Hộp "Xác nhận duyệt": "Duyệt phiếu sẽ TRỪ TỒN HÀNG GIỮ ngay lập tức và không thể hoàn tác. Bạn có chắc chắn không?" (Duyệt / Hủy).\n– Bấm Duyệt: kiểm quyền; kiểm lại nhân viên, hàng hoá, ĐVT thuộc hàng, không trùng hàng / khách, số quy đổi ≤ số có thể huỷ hiện tại (BR-06, BR-07, BR-08).\n' + TRUOC_LUU + '\nAfter:\n– Sinh mã KTPHHG-xxxxx, ghi phiếu (công ty = công ty người lập), hàng hoá (chụp lại tên, mã, model, thương hiệu), dòng khách hàng (số lượng, ĐVT, hệ số, số quy đổi).\n– Trừ tồn hàng giữ từng dòng theo FIFO hạn giữ; thiếu tồn ở bất kỳ dòng nào → huỷ toàn bộ, không lưu gì.\n– Ghi nhận Tạo mới trong lịch sử; gửi thông báo cho nhân viên bị huỷ.\n– Báo "Duyệt thành công."; Duyệt → về danh sách, Lưu và tiếp tục → trang Thêm trống.'],
        ['Bấm Quay lại', 'Click', 'After:\n– Chưa nhập gì → về danh sách.\n– Đã nhập → hộp "Thông tin chưa lưu" ("Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"): Thoát thì về danh sách không lưu, Ở lại thì quay về form.'],
    ],
})

# 2.5 Chọn hàng hoá đang giữ -----------------------------------------------------
FR.append({
    'ten': 'Chọn hàng hoá nhân viên đang giữ', 'uc': 'uc_chonhang', 'uc_ten': 'FR-05 Chọn hàng hoá nhân viên đang giữ',
    'qtc': 'Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chọn hàng hoá nhân viên đang giữ'],
        ['Mô tả', 'Cửa sổ liệt kê hàng hoá nhân viên đã chọn còn đang giữ cho MỌI khách hàng (tra theo công ty của nhân viên chủ lô — BR-03). Tích nhiều hàng rồi bấm "Chọn (n)" để đưa vào bảng Chi tiết.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở trang Thêm và đã chọn Hủy của nhân viên.'],
        ['Dòng sự kiện chính', '1. Bấm "Thêm hàng hóa".\n2. Hệ thống mở cửa sổ "Hàng đang giữ của nhân viên", dòng phụ "Chỉ liệt kê hàng nhân viên đã chọn còn đang giữ (mọi khách hàng)", tải trang 1 (10 dòng).\n3. Người dùng lọc theo Mã / Tên hàng hóa (nếu cần), tích các hàng cần huỷ.\n4. Bấm "Chọn (n)": hệ thống nạp danh sách khách đang được giữ + các ĐVT của từng hàng, thêm vào bảng Chi tiết, đóng cửa sổ.'],
        ['Dòng sự kiện phụ', '• Nhân viên không giữ hàng nào → bảng ghi "Nhân viên này hiện không giữ hàng hóa nào."\n• Hàng đã có trên phiếu: không hiện lại trong cửa sổ.\n• Hàng không còn khách nào có số có thể huỷ > 0 → không thêm, toast đỏ "Hàng hóa <tên> không còn số lượng có thể hủy."\n• Bấm Đóng / (x): đóng cửa sổ, không thêm gì.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi} => Thêm hàng hóa {icon:btn_themhang}',
    'ghi_chu_layout': POPUP % ('Hàng đang giữ của nhân viên', 'Thêm phiếu hủy hàng giữ kế toán'),
    'anh': [('14_picker', 'Cửa sổ Hàng đang giữ của nhân viên'), ('14b_picker_selected', 'Đã tích 2 hàng hoá, nút "Chọn (2)"')],
    'ui': ui(UI8, [
        ['Ô Mã hàng hóa / Tên hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Placeholder "Nhập mã hàng hóa" / "Nhập tên hàng hóa"; tìm gần đúng khi Enter / Tìm kiếm.'],
        ['Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', '–', 'Áp dụng / xoá điều kiện lọc.'],
        ['Cột ô tích', 'Checkbox', 'Enable', '–', '–', 'Không tích', 'Chọn nhiều hàng cùng lúc.'],
        ['Cột STT, Mã hàng hóa, Tên hàng hóa, Model, Thương hiệu, ĐVT', 'Table/Grid', 'Read-only', '–', '–', '–', 'Thông tin hàng hoá; ĐVT là đơn vị cơ bản. Ô trống để trống.'],
        ['Cột Đang giữ', 'Table/Grid', 'Read-only', 'Số ≥ 0', '–', '–', 'Tổng số có thể huỷ của nhân viên cho hàng này (mọi khách, đơn vị cơ bản, đã trừ phần đang chờ xuất kho).'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 / 20 / 50 / 100', '–', '10', 'Chọn số dòng/trang, chuyển trang.'],
        ['Nút Chọn (n)', 'Button', 'Enable', '–', '–', '–', 'n = số hàng đang tích; đưa hàng vào bảng Chi tiết.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ, không thêm.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Mở cửa sổ', 'System', 'Before:\n– Kiểm tra quyền "%s".\nAfter:\n– Tải hàng nhân viên đang giữ (bỏ hàng đã có trên phiếu).' % QUYEN],
        ['Bấm Tìm kiếm / Enter', 'Click', 'After:\n– Tải lại từ trang 1 theo mã / tên.'],
        ['Bấm Chọn (n)', 'Click', 'After:\n– Với từng hàng: tải khách đang được giữ (kèm số có thể huỷ) và các ĐVT; hàng không còn khách → bỏ qua và báo; hàng còn lại thêm 1 dòng, khách đầu tiên, ĐVT cơ bản.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.6 Xem chi tiết --------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết phiếu', 'uc': 'uc_xem', 'uc_ten': 'FR-06 Xem chi tiết phiếu huỷ hàng giữ kế toán',
    'qtc': 'Màn Xem chi tiết và Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết phiếu huỷ hàng giữ kế toán'],
        ['Mô tả', 'Xem toàn bộ thông tin 1 phiếu ở chế độ chỉ đọc, kèm khối Lịch sử thay đổi; chân trang có In, Quay lại.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_XEM],
        ['Dòng sự kiện chính', '1. Bấm Mã phiếu ở danh sách (hoặc bấm thông báo).\n2. Hệ thống mở trang "Chi tiết phiếu hủy hàng giữ kế toán: <mã phiếu>": khối Thông tin chung (Mã phiếu, Hủy của nhân viên "Mã NV - Họ tên", Phòng ban của nhân viên, Ghi chú; góc phải "<Người tạo> - <ngày giờ tạo>"), khối Chi tiết (gộp ô theo hàng hoá; nhóm Số lượng gồm Duyệt hủy, Đơn vị tính), khối Lịch sử thay đổi (thu gọn).'],
        ['Dòng sự kiện phụ', '• Phiếu không tồn tại → toast "Không tìm thấy dữ liệu.", quay về danh sách.\n• Phiếu ngoài phạm vi / không có quyền → toast "Bạn không có quyền xem phiếu này.", quay về danh sách.\n• Khách hàng không còn trong danh mục → hiện "Khách hàng #<số>".'],
    ],
    'menu_them': ' => Mã phiếu (liên kết)',
    'anh': [('17_detail', 'Trang Chi tiết phiếu huỷ hàng giữ kế toán')],
    'ui': ui(UI6, [
        ['Mã phiếu, Hủy của nhân viên, Phòng ban, Ghi chú', 'Textbox', 'Read-only', 'Dữ liệu phiếu', 'Chỉ đọc.'],
        ['Người tạo - ngày giờ', 'Label', 'Read-only', 'Dữ liệu phiếu', 'Góc phải khối Thông tin chung.'],
        ['Bảng Chi tiết', 'Table/Grid', 'Read-only', 'Theo phiếu', 'STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, Khách hàng, Duyệt hủy, Đơn vị tính; không có Có thể hủy, không có nút xoá / thêm.'],
        ['Khối Lịch sử thay đổi', 'Label', 'Enable', 'Thu gọn', 'Tiêu đề kèm số mốc; bấm "Xem lịch sử" để mở (mục 2.10).'],
        ['Nút In', 'Button', 'Enable', '–', 'Mở bản in phiếu (mục 2.7).'],
        ['Nút Quay lại', 'Button', 'Enable', '–', 'Về danh sách. Không có Sửa, Xóa.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở trang', 'System', 'Before:\n– Kiểm tra quyền + phạm vi dữ liệu.\nAfter:\n– Hiển thị phiếu; chỉ dựng khối Lịch sử khi đã tải được phiếu.'],
        ['Bấm In / Quay lại', 'Click', 'After:\n– Mở bản in / về danh sách.'],
    ],
})

# 2.7 In phiếu --------------------------------------------------------------------
FR.append({
    'ten': 'In phiếu', 'uc': 'uc_in', 'uc_ten': 'FR-07 In phiếu huỷ hàng giữ kế toán',
    'qtc': 'Quy tắc màn In và bố cục bản in.',
    'gioi_thieu': [
        ['Tên chức năng', 'In phiếu huỷ hàng giữ kế toán'],
        ['Mô tả', 'In 1 phiếu khổ A4 dọc theo mẫu "PHIẾU HUỶ HÀNG GIỮ KẾ TOÁN", tiêu đề công ty là công ty CỦA PHIẾU.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_XEM],
        ['Dòng sự kiện chính', '1. Bấm In ở cột Hành động (hoặc nút In ở trang Chi tiết).\n2. Hệ thống mở cửa sổ "Xem trước phiếu <mã phiếu>" ngay trên màn (không mở tab mới).\n3. Bấm In để mở hộp in của trình duyệt.'],
        ['Dòng sự kiện phụ', '• Ô thông tin trống in "....." để viết tay.'],
    ],
    'menu_them': ' => In {icon:btn_in_row}',
    'ghi_chu_layout': 'Cửa sổ Xem trước bản in được mở ngay trên màn hình danh sách hoặc màn hình chi tiết phiếu theo đường dẫn ở trên.',
    'anh': [('19_print', 'Cửa sổ xem trước bản in phiếu')],
    'ui': ui(UI6, [
        ['Phần đầu bản in', 'Label', 'Read-only', 'Tiêu đề công ty của phiếu', 'Logo, tên, địa chỉ công ty.'],
        ['Tiêu đề', 'Label', 'Read-only', '"PHIẾU HUỶ HÀNG GIỮ KẾ TOÁN"', 'Kèm "Số phiếu: <mã>", "Ngày tạo: dd/mm/yyyy".'],
        ['Khối thông tin', 'Table/Grid', 'Read-only', 'Dữ liệu phiếu', 'Huỷ của nhân viên, Phòng ban, Người tạo, Ghi chú.'],
        ['Bảng hàng hoá', 'Table/Grid', 'Read-only', 'Dữ liệu phiếu', 'STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, Khách hàng, SL duyệt huỷ, ĐVT; gộp ô theo hàng hoá, không cắt ngang nhóm khi sang trang.'],
        ['Khối ký', 'Label', 'Read-only', '–', '"Ngày ..... tháng ..... năm .....", Người lập phiếu, Kế toán trưởng, Nhân viên giữ hàng.'],
        ['Nút In / (x)', 'Button', 'Enable', '–', 'Mở hộp in của trình duyệt / đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In (dòng / chi tiết)', 'Click', 'Before:\n– Kiểm tra quyền + phạm vi.\nAfter:\n– Dựng bản in, hiện cửa sổ xem trước.'],
        ['Bấm In trong cửa sổ', 'Click', 'After:\n– Mở hộp in của trình duyệt.'],
    ],
})

# 2.8 In danh sách ------------------------------------------------------------------
FR.append({
    'ten': 'In danh sách', 'uc': 'uc_inds', 'uc_ten': 'FR-08 In danh sách phiếu',
    'qtc': 'Quy tắc màn In và bố cục bản in.',
    'gioi_thieu': [
        ['Tên chức năng', 'In danh sách phiếu huỷ hàng giữ kế toán'],
        ['Mô tả', 'In mọi phiếu khớp bộ lọc (không chỉ trang đang xem) khổ A4 ngang, tiêu đề công ty của người đăng nhập, 5 cột cố định.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm In trên thanh công cụ danh sách.\n2. Hệ thống mở cửa sổ "Xem trước danh sách phiếu hủy hàng giữ kế toán".\n3. Bấm In để mở hộp in của trình duyệt.'],
        ['Dòng sự kiện phụ', '• Có lọc Ngày tạo → thêm dòng "Khoảng thời gian: Từ ngày … đến ngày …".\n• Không có dữ liệu → bảng ghi "Không có dữ liệu".'],
    ],
    'menu_them': ' => In {icon:btn_indanhsach}',
    'ghi_chu_layout': 'Cửa sổ Xem trước bản in danh sách được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('19b_printlist', 'Cửa sổ xem trước bản in danh sách')],
    'ui': ui(UI6, [
        ['Tiêu đề bản in', 'Label', 'Read-only', '"DANH SÁCH PHIẾU HUỶ HÀNG GIỮ KẾ TOÁN"', 'Kèm "Khoảng thời gian" (nếu lọc ngày) và "Tổng số phiếu: N".'],
        ['Bảng in', 'Table/Grid', 'Read-only', 'Theo bộ lọc', 'STT, Mã phiếu, Huỷ của nhân viên, Ngày lập, Người lập.'],
        ['Nút In / (x)', 'Button', 'Enable', '–', 'Mở hộp in / đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In', 'Click', 'Before:\n– Kiểm tra quyền.\nAfter:\n– Dựng bản in theo bộ lọc + phạm vi dữ liệu.'],
    ],
})

# 2.9 Xuất Excel -----------------------------------------------------------------
FR.append({
    'ten': 'Xuất Excel danh sách', 'uc': 'uc_xuat', 'uc_ten': 'FR-09 Xuất Excel danh sách phiếu',
    'qtc': 'Quy tắc Excel và Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách phiếu ra Excel'],
        ['Mô tả', 'Xuất mọi phiếu khớp bộ lọc ra file danh_sach_huy_hang_giu_ke_toan.xlsx, tiêu đề "DANH SÁCH PHIẾU HUỶ HÀNG GIỮ KẾ TOÁN", cột STT đứng đầu, các cột theo lựa chọn và thứ tự người dùng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất Excel", tích sẵn các cột đang hiện trên bảng.\n3. Người dùng tích / bỏ, kéo đổi thứ tự, bấm Xuất file.\n4. Hệ thống tải dữ liệu, dựng file và tải về; báo "Xuất Excel thành công."'],
        ['Dòng sự kiện phụ', '• Có lọc Ngày tạo → dòng 2 ghi "Từ ngày … đến ngày …".\n• Cuối bảng có khối "Ngày…Tháng…Năm…", "Người lập (Ký, họ tên)".\n• Lỗi → "Xuất Excel thất bại."'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất Excel')],
    'ui': ui(UI8, [
        ['Danh sách trường', 'Checkbox', 'Enable', '7 trường', 'Có (≥ 1)', 'Các cột đang hiện', 'Mã phiếu, Hủy của nhân viên, Ngày tạo, Người tạo, Người cập nhật, Ngày cập nhật, Ghi chú. Kéo đổi thứ tự cột trong file.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', 'Chọn / bỏ nhanh mọi trường.'],
        ['Dòng đếm', 'Label', 'Read-only', '–', '–', '–', '"Đang chọn x/7 trường".'],
        ['Nút Xuất file', 'Button', 'Enable', '–', '–', '–', 'Xuất file theo trường đã chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng, không xuất.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất file', 'Click', 'Before:\n– Kiểm tra quyền.\nAfter:\n– Tải dữ liệu theo bộ lọc + phạm vi, dựng file đúng thứ tự cột (ô dạng chữ, không cảnh báo số dạng chữ), tải về; báo kết quả.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.10 Lịch sử --------------------------------------------------------------------
FR.append({
    'ten': 'Xem lịch sử thay đổi',
    'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem lịch sử thay đổi phiếu'],
        ['Mô tả', 'Liệt kê các mốc thao tác trên phiếu, mới nhất ở trên. Phiếu không sửa / xoá được nên chỉ có mốc Tạo mới, ghi chú "Đã trừ tồn hàng giữ trên N lô."'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_XEM],
        ['Dòng sự kiện chính', '1. Bấm Lịch sử ở cột Hành động → cửa sổ "Lịch sử phiếu hủy hàng giữ kế toán", dòng "Mã phiếu: <mã>".\n2. Hoặc ở trang Chi tiết bấm "Xem lịch sử" ở khối Lịch sử thay đổi (có nút Làm mới, Thu gọn).\n3. Hệ thống liệt kê các mốc; có nút Bộ lọc.'],
        ['Dòng sự kiện phụ', '• Phiếu chuyển từ hệ thống cũ không có lịch sử → "Chưa có lịch sử thao tác nào."\n• Mốc Tạo mới không liệt kê chi tiết từng hàng hoá.'],
    ],
    'menu_them': ' => Lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': 'Modal Lịch sử được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối Lịch sử thay đổi nằm cuối trang Chi tiết phiếu.',
    'anh': [('16_history', 'Cửa sổ Lịch sử mở từ danh sách'), ('17b_detail_history', 'Khối Lịch sử thay đổi ở trang Chi tiết')],
    'ui': ui(UI6, [
        ['Tiêu đề', 'Label', 'Read-only', '"Lịch sử phiếu hủy hàng giữ kế toán"', 'Kèm "Mã phiếu: <mã>".'],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Lọc theo loại hành động, người thực hiện, khoảng ngày.'],
        ['Mốc lịch sử', 'Label', 'Read-only', 'Mới nhất trên cùng', 'Thời điểm dd/mm/yyyy hh:mm, nhãn "Tạo mới" (xanh lá), "Người thực hiện: <họ tên> - <phòng ban>", ghi chú số lô đã trừ.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lịch sử / Xem lịch sử', 'Click', 'Before:\n– Kiểm tra quyền + phạm vi.\nAfter:\n– Tải và hiển thị các mốc lịch sử.'],
        ['Bấm Đóng / (x) / Thu gọn', 'Click', 'After:\n– Đóng cửa sổ / thu gọn khối.'],
    ],
})

FR_NAMES = ['FR-%02d %s' % (i + 1, f['ten']) for i, f in enumerate(FR)]

S = {
    'ten': TEN, 'ten_ngan': 'phiếu huỷ hàng giữ kế toán', 'phan_he': 'Tài chính',
    'menu': [('Tài chính', 'menu_phanhe'), ('Hàng hoá - Dịch vụ - Vận chuyển', 'menu_nhom'), ('Giữ hàng', 'menu_nhom2'), (TEN, 'menu_muc')],
    'muc_dich': [
        'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho việc kế toán HUỶ THẲNG hàng đang giữ của một nhân viên, không cần phiếu yêu cầu.',
        'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
        'Làm rõ tác động số liệu: bấm Duyệt là trừ tồn hàng giữ ngay theo thứ tự hạn giữ, không hoàn tác, phiếu không sửa / xoá được.',
        'Làm rõ cách tính số có thể huỷ, quy đổi đơn vị tính và các ràng buộc chống huỷ vượt tồn.',
        'Làm rõ phạm vi dữ liệu: phiếu thuộc công ty người lập, còn lô hàng giữ tra theo công ty nhân viên chủ lô.',
    ],
    'thuat_ngu': [
        ['Hàng giữ', 'Hàng hoá nhân viên kinh doanh đang giữ cho khách hàng, chia theo lô có hạn giữ (sinh ra từ Phiếu xuất giữ).'],
        ['Phiếu huỷ hàng giữ kế toán', 'Phiếu kế toán lập để huỷ (trả lại) hàng đang giữ của 1 nhân viên; mã KTPHHG-xxxxx.'],
        ['Hủy của nhân viên', 'Nhân viên bị huỷ hàng giữ (chủ lô). Khác Người tạo (kế toán lập phiếu).'],
        ['Có thể hủy', 'Số đang giữ của nhân viên cho 1 khách + 1 hàng, đã trừ phần đang nằm trong đề nghị xuất kho chưa hoàn tất.'],
        ['Duyệt hủy', 'Số lượng huỷ nhập trên phiếu, theo ĐVT đã chọn.'],
        ['Số quy đổi', 'Duyệt hủy × hệ số ĐVT, quy về đơn vị cơ bản, làm tròn 2 chữ số thập phân — là số bị trừ khỏi tồn giữ.'],
        ['FIFO hạn giữ', 'Trừ lô có hạn giữ sớm nhất trước (kể cả lô đã quá hạn), hết lô mới sang lô sau.'],
        ['ĐVT', 'Đơn vị tính.'],
    ],
    'trang_thai': {
        'cau_dan': 'Phiếu KHÔNG có bước lưu nháp / gửi duyệt / từ chối / huỷ duyệt và không có ô trạng thái. Nút Duyệt trên trang Thêm vừa lưu phiếu vừa trừ tồn hàng giữ; '
                   'phiếu đã lưu là chốt vĩnh viễn (không sửa, không xoá).',
        'rows': [
            ['Đang lập (chưa lưu)', 'Dữ liệu chỉ nằm trên trang Thêm, chưa ghi vào hệ thống, chưa trừ tồn.', 'Chọn nhân viên, thêm / bỏ hàng hoá và khách hàng, Duyệt, Lưu và tiếp tục, Quay lại', 'Người có quyền "%s"' % QUYEN],
            ['Đã duyệt (đã trừ tồn hàng giữ)', 'Phiếu đã ghi, tồn hàng giữ của nhân viên đã bị trừ theo FIFO hạn giữ, nhân viên đã được thông báo.', 'Xem, In, Xuất, Lịch sử (không Sửa, không Xóa, không huỷ duyệt)', 'Người có quyền "%s" trong phạm vi dữ liệu' % QUYEN],
        ],
        'anh': 'state_flow',
        'ghi_chu': ['Duyệt thất bại (thiếu tồn, sai dữ liệu) thì không có phiếu nào được ghi và không lô nào bị trừ — phiếu vẫn ở trạng thái Đang lập trên form (BR-06).'],
    },
    'quyen_truoc': ['Nhóm quyền thao tác: một quyền duy nhất cho cả màn (xem lẫn lập phiếu). Không có quyền riêng cho Thêm / Sửa / Xoá; ba quyền xem phiếu hàng giữ theo cấp của màn Phiếu hủy hàng giữ thường KHÔNG có tác dụng ở màn này.'],
    'quyen_rows': [[QUYEN, 'Vào màn; xem danh sách, tìm kiếm, xem chi tiết, lịch sử, tuỳ chỉnh cột, in phiếu, in danh sách, xuất Excel; Tạo mới (Duyệt, Lưu và tiếp tục).']],
    'pham_vi_truoc': ['Phạm vi dữ liệu (xét theo thứ tự từ trên xuống):'],
    'pham_vi_rows': [
        ['1', 'Tài khoản quản trị cao nhất', 'Phiếu của mọi công ty; khu vực lọc có thêm ô Công ty.'],
        ['2', QUYEN, 'Phiếu có công ty phiếu = công ty đang làm việc của người dùng.'],
        ['3', '(không có quyền nào ở trên)', 'Không xem được màn, chi tiết, bản in, file Excel; không lập được phiếu.'],
    ],
    'pham_vi_sau': ['Công ty của phiếu = công ty của NGƯỜI LẬP (kế toán), không phải công ty của nhân viên bị huỷ hàng. Phạm vi áp như nhau cho danh sách, chi tiết, lịch sử, in và xuất Excel (BR-02).'],
    'ma_tran': [['Chức năng', QUYEN, 'Không có quyền']] + [[f, 'Có', 'Không'] for f in FR_NAMES],
    'ma_tran_widths': [3.0, 2.0, 1.2],
    'quyen_sau': ['Phạm vi dữ liệu của mọi chức năng theo bảng quyền phạm vi ở trên.'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Cấu trúc phiếu', ['– 1 phiếu = 1 nhân viên bị huỷ hàng × nhiều hàng hoá; mỗi hàng hoá × 1 hoặc nhiều khách hàng.', '– Tên, mã, model, thương hiệu hàng hoá được chụp lại lúc lập; hàng thiếu model / thương hiệu vẫn lập được (để trống).'], ['Lập phiếu', 'Xem chi tiết', 'In phiếu']),
        ('BR-02', 'Phạm vi dữ liệu', ['– Quyền "%s": chỉ phiếu có công ty phiếu = công ty đang làm việc; tài khoản quản trị cao nhất xem mọi công ty.' % QUYEN, '– Công ty phiếu = công ty người lập. Phiếu ngoài phạm vi: không hiện; mở thẳng thì báo không có quyền và quay về danh sách.'], ['Mọi chức năng']),
        ('BR-03', 'Lô hàng giữ tra theo công ty nhân viên chủ lô', ['– Cửa sổ chọn hàng, ô Khách hàng, Có thể hủy và bước trừ tồn đều tra lô theo công ty của nhân viên bị huỷ hàng, nên kế toán khác công ty vẫn huỷ đúng lô.', '– Ô "Hủy của nhân viên" liệt kê mọi nhân viên đang làm việc, kể cả người không giữ hàng.'], ['Lập phiếu', 'Chọn hàng hoá']),
        ('BR-04', 'Mã phiếu', ['– Dạng KTPHHG-<5 chữ số>, sinh tự động khi Duyệt; không nhập tay.'], ['Lập phiếu']),
        ('BR-05', 'Duyệt = lưu + trừ tồn hàng giữ ngay', ['– Không có nháp; bấm Duyệt (sau hộp xác nhận) là trừ tồn.', '– Mỗi dòng khách hàng trừ số quy đổi trên các lô của đúng nhân viên + khách + hàng, hạn giữ sớm trước (kể cả lô quá hạn).', '– Phiếu đã lưu không sửa, không xoá, không huỷ duyệt; mỗi lô bị trừ có dòng giảm trong lịch sử giữ hàng gắn với phiếu.'], ['Lập phiếu']),
        ('BR-06', 'Toàn vẹn khi trừ tồn', ['– Một dòng thiếu tồn (do chứng từ khác vừa lấy) thì huỷ toàn bộ: không tạo phiếu, không trừ dòng nào; lỗi gắn đúng dòng.', '– Hai người cùng huỷ một hàng giữ: người sau bị từ chối, tồn giữ không bao giờ âm.'], ['Lập phiếu']),
        ('BR-07', 'Không trùng', ['– Một phiếu không có 2 dòng cùng hàng hoá ("Hàng hóa bị chọn trùng.").', '– Một hàng hoá không chọn trùng khách hàng ("Khách hàng bị chọn trùng trong cùng một hàng hóa.").', '– ĐVT phải thuộc hàng hoá ("Đơn vị tính không thuộc hàng hóa này.").'], ['Lập phiếu']),
        ('BR-08', 'Số có thể huỷ và quy đổi ĐVT', ['– Có thể hủy = số đang giữ trừ phần đang nằm trong đề nghị xuất kho chưa hoàn tất (đơn vị cơ bản); hiển thị = số đó ÷ hệ số ĐVT, làm tròn XUỐNG 2 chữ số thập phân.', '– Duyệt hủy > 0, tối đa 2 chữ số thập phân; số quy đổi ≤ Có thể hủy, vượt thì báo đỏ "Vượt quá số có thể hủy (tối đa X)" và giữ nguyên số đã nhập.', '– Số quy đổi làm tròn thành 0 (ĐVT hệ số < 1) → "Số lượng quá nhỏ so với đơn vị tính đã chọn."', '– Dòng có Duyệt hủy = 0 không được ghi; phiếu phải có ít nhất 1 dòng > 0 ("Phải có ít nhất 1 dòng Duyệt hủy lớn hơn 0.").'], ['Lập phiếu']),
        ('BR-09', 'Thông báo cho nhân viên bị huỷ hàng', ['– Sau khi Duyệt thành công, nhân viên bị huỷ nhận thông báo "[KTHHG] Hủy: <mã phiếu>. Người huỷ: <họ tên>. Số mặt hàng: n. Ghi chú: …", bấm mở chi tiết phiếu.', '– Người lập tự huỷ hàng của chính mình thì không gửi. Lỗi gửi thông báo không làm hỏng phiếu.'], ['Lập phiếu']),
        ('BR-10', 'In và xuất', ['– In danh sách, xuất Excel theo đúng bộ lọc và phạm vi đang áp (mọi trang).', '– In phiếu dùng tiêu đề công ty của phiếu; in danh sách dùng công ty người đăng nhập.'], ['In phiếu', 'In danh sách', 'Xuất Excel']),
        ('BR-11', 'Thao tác xong quay về danh sách', ['– Duyệt thành công → về danh sách (Lưu và tiếp tục → trang Thêm trống); lỗi mở chi tiết → về danh sách.'], ['Lập phiếu', 'Xem chi tiết']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây đọc hoặc dùng dữ liệu do Phiếu huỷ hàng giữ kế toán ghi ra (phiếu, dòng hàng × khách và các dòng giảm tồn hàng giữ).',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng có quyền "%s"' % QUYEN,
    'mains': [('FR-01', 'Xem danh sách phiếu', 'view'), ('FR-04', 'Lập phiếu (Duyệt)', 'crud'),
              ('FR-07', 'In phiếu', 'io'), ('FR-08', 'In danh sách', 'io'), ('FR-09', 'Xuất Excel danh sách', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc danh sách', 'view'), ('FR-03', 'Cài đặt bộ lọc, tuỳ chỉnh cột', 'view'),
             ('FR-06', 'Xem chi tiết phiếu', 'view'), ('FR-10', 'Xem lịch sử thay đổi', 'view')],
    'rieng': [('FR-04', 'Lập phiếu huỷ hàng giữ kế toán', 'crud', 'uc_them'), ('FR-05', 'Chọn hàng hoá nhân viên đang giữ', 'crud', 'uc_chonhang'),
              ('FR-06', 'Xem chi tiết phiếu', 'view', 'uc_xem'), ('FR-07', 'In phiếu', 'io', 'uc_in'),
              ('FR-08', 'In danh sách', 'io', 'uc_inds'), ('FR-09', 'Xuất Excel danh sách', 'io', 'uc_xuat')],
}

STATES = [('start', '', None), ('lap', 'Đang lập (chưa lưu)', '#e0f2fe'), ('duyet', 'Đã duyệt (đã trừ tồn hàng giữ)', '#dcfce7'),
          ('end', '', None)]
TRANS = [('start', 'lap', 'Tạo mới'), ('lap', 'duyet', 'Duyệt / Lưu và tiếp tục'),
         ('lap', 'end', 'Quay lại → Thoát (không lưu)')]

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    L.draw_state_flow(os.path.join(scr.uml, 'state_flow.png'), STATES, TRANS)
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        L.finalize_and_check(OUT, PDF, extra_banned=('ERP', 'API'))

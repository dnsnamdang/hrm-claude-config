# -*- coding: utf-8 -*-
"""SRS - Danh mục kho kế toán (form Danh mục quốc gia, TPE duyệt) — chép khuôn màn mẫu docs/warehouses/gen_srs.py.

Nguồn (code HRM hiện tại, nhánh có code kho):
  FE hrm-client/pages/warehouse/accounting-warehouses/{index.vue, AddAccountingWarehouseModal.vue}, utils/mixins/
     {vehicleCatalogScreenMixin, vehicleCatalogModalMixin, warehouseCatalogModalMixin, warehouseCatalogImportMixin,
     createdRangeFilterMixin}.js, utils/warehouse-catalog-import.js, components/subsystem-menu/warehouse.js
  BE Modules/MasterData: Entities/Warehouse/AccountingWarehouseCatalog.php, Http/Controllers/V1/Warehouse/
     {AccountingWarehouseCatalogController, WarehouseTreeCatalogController}.php, ProductClassification/BaseCatalogController.php,
     Http/Requests/Warehouse/AccountingWarehouseCatalogRequest.php, Services/Warehouse/{AccountingWarehouseCatalogService,
     WarehouseCatalogScope, Concerns/ImportsWarehouseCatalogRows}.php, Transformers/Warehouse/AccountingWarehouseCatalogResource.php;
     app/Services/CatalogHistoryService.php
  Phần 5: dò code FE/BE + menu (02/11/2026).
Chạy:  python gen_srs.py          (dựng + Word cập nhật mục lục + PDF out/ + tự kiểm)
       python gen_srs.py --no-word (chỉ dựng .docx)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import _lib_win as L  # noqa: E402

TEN = 'Danh mục kho kế toán'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q = 'Người dùng có quyền thực hiện chức năng (quyền "Quản lý kho")'
DK = '1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền "Quản lý kho".'
TRUOC_LUU = '– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung SRS_Các quy tắc chung_VN_1.0, không thực hiện bước After.'
POPUP = 'Modal %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'

UI6 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả']
UI6W = [0.55, 1.35, 0.9, 0.8, 1.0, 2.6]
UI8 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả']
UI8W = [0.55, 1.1, 0.85, 0.75, 0.95, 0.7, 0.9, 2.2]
UI4 = ['STT', 'Tên đối tượng', 'Loại', 'Mô tả']
UI4W = [0.5, 1.6, 1.0, 3.6]
UI7I = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả']
UI7IW = [0.55, 1.3, 0.85, 0.8, 0.7, 0.9, 2.6]


def ui(header, rows):
    return [header] + [[str(i + 1)] + r for i, r in enumerate(rows)]


# ------------------------------------------------------------------ Phần 5 (dò code 02/11/2026)
P5 = [
    ('Kho', 'Khai báo tồn kho đầu kỳ', 'Kho => Tồn kho đầu kỳ'),
    ('Kho', 'Phiếu nhập kho điều chỉnh kiểm kê', 'Kho => Nhập kho'),
    ('Kho', 'Phiếu đề nghị xuất kho (xem tồn kho kế toán)', 'Kho => Xuất kho'),
    ('Kho', 'Phiếu xuất kho điều chỉnh kiểm kê', 'Kho => Xuất kho'),
    ('Kho', 'Kiểm kê theo hàng hóa', 'Kho => Kiểm kho => Theo vị trí'),
    ('Kho', 'Thẻ kho', 'Kho => Báo cáo kho'),
    ('Bán hàng', 'YC xuất hàng', 'Bán hàng => Yêu cầu => Hàng hóa'),
    ('Bán hàng', 'YC chuyển hàng (xem tồn theo kho)', 'Bán hàng => Yêu cầu => Hàng hóa'),
    ('Bán hàng', 'Phiếu cung cấp thông tin làm báo giá (xem tồn)', 'Bán hàng => Bán dịch vụ => Báo giá dịch vụ SC-BD-BT'),
    ('Bán hàng', 'Báo cáo theo dõi giữ hàng', 'Bán hàng => Báo cáo => Hàng giữ'),
    ('CSKH sau bán', 'Phiếu cung cấp thông tin làm báo giá (xem tồn)', 'CSKH sau bán => Kiểm tra bảo hành sửa chữa'),
    ('Tài chính', 'Khai Quy chế – Cấu hình (Kho khuyến mại, Kho hàng gửi)', 'Tài chính'),
    ('Tài chính', 'Phiếu nhập hàng', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
    ('Tài chính', 'Phiếu nhập hàng điều chỉnh kiểm kê', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
    ('Tài chính', 'Yêu cầu xuất hàng', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ('Tài chính', 'Đề nghị xuất kho (xem tồn kho kế toán)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ('Tài chính', 'Phiếu xuất hàng', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ('Tài chính', 'Phiếu yêu cầu chuyển hàng (xem tồn theo kho)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ('Tài chính', 'Phiếu xuất hàng điều chỉnh kiểm kê', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ('Tài chính', 'Danh sách hàng mượn', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng'),
    ('Tài chính', 'Hàng sắp hết hạn mượn', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng'),
    ('Tài chính', 'Danh sách hàng giữ', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng'),
    ('Tài chính', 'Hàng sắp hết hạn giữ', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng'),
    ('Tài chính', 'Yêu cầu hủy hàng giữ (kế toán kho phụ trách)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng'),
    ('Tài chính', 'Phiếu hủy hàng giữ (kế toán kho phụ trách)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng'),
    ('Tài chính', 'Phiếu điều chuyển hàng', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Điều chuyển'),
    ('Tài chính', 'Kế hoạch kiểm kê theo hàng hóa', 'Tài chính => Kiểm kê'),
    ('Tài chính', 'Kế hoạch tổng kiểm kê hàng hóa', 'Tài chính => Kiểm kê'),
    ('Tài chính', 'Biên bản xử lý hàng thừa, thiếu sau kiểm kê', 'Tài chính => Kiểm kê'),
    ('Tài chính', 'Cập nhật giá bán (cột Tồn kho)', 'Tài chính => Giá bán'),
    ('Tài chính', 'Bảng giá bán hiện hành (cột Tồn kho)', 'Tài chính => Giá bán'),
    ('Thông báo', 'Hàng có thể bán theo công ty', 'Thông báo => Tra cứu tồn kho'),
    ('Thông báo', 'Danh sách hàng mượn', 'Thông báo => Thông báo'),
    ('Thông báo', 'Hàng sắp hết hạn mượn', 'Thông báo => Thông báo'),
]

# ------------------------------------------------------------------ dữ liệu SRS
FR = []

# 2.1 Xem danh sách -------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách kho kế toán',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang, Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách kho kế toán'],
        ['Mô tả', 'Hiển thị các kho kế toán trong phạm vi dữ liệu của người dùng (cả Hoạt động lẫn Khóa), có phân trang, sắp xếp và các nút thao tác theo từng dòng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn Danh mục kho kế toán theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), kho tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Người dùng thường chỉ thấy kho kế toán của công ty mình (theo công ty của chính kho kế toán, không theo kho vật lý); Super admin thấy mọi công ty (BR-01).\n• Không có kho khớp → bảng hiện "Không có dữ liệu phù hợp.", chân bảng "Không có kho kế toán nào."'],
    ],
    'anh': [('01_list', 'Màn Danh mục kho kế toán lúc mới truy cập')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Danh sách kho kế toán', 'Tiêu đề khối danh sách và tiêu đề trang.'],
        ['Nút Tạo mới', 'Button', 'Enable / Ẩn', 'Hiển thị', '- Mở cửa sổ "Tạo mới kho kế toán" (mục 2.3).\n- Ẩn khi thiếu quyền "Quản lý kho".'],
        ['Nút Import Excel', 'Button', 'Enable / Ẩn', 'Hiển thị', '- Mở cửa sổ "Import kho kế toán" (mục 2.8).\n- Ẩn khi thiếu quyền.'],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất file" (mục 2.9).'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.11).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa, không ẩn được.'],
        ['Cột Mã kho kế toán', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sắp xếp được.\n- Chữ dạng liên kết: bấm vào mở cửa sổ "Xem chi tiết kho kế toán" (mục 2.10).\n- Cột khóa, không ẩn được.'],
        ['Cột Tên kho kế toán', 'Table/Grid', 'Read-only', 'Hiển thị', 'Sắp xếp được. Dài thì xuống tối đa 2 dòng, rê chuột xem đủ.'],
        ['Cột Kho vật lý', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên kho vật lý chứa kho kế toán (chỉ tên, không kèm mã). Kho Nhập xuất thẳng để trống.'],
        ['Cột Nhập xuất thẳng', 'Table/Grid', 'Read-only', 'Ẩn', '"Có" / "Không". Mặc định ẩn, bật ở Tuỳ chỉnh cột.'],
        ['Cột Địa chỉ', 'Table/Grid', 'Read-only', 'Ẩn', 'Địa chỉ kho kế toán. Mặc định ẩn.'],
        ['Cột Kế toán kho', 'Table/Grid', 'Read-only', 'Hiển thị', 'Họ tên các kế toán kho, cách nhau dấu phẩy.'],
        ['Cột Công ty', 'Table/Grid', 'Read-only', 'Hiển thị', 'Công ty sở hữu kho kế toán (công ty của người tạo).'],
        ['Cột Mô tả', 'Table/Grid', 'Read-only', 'Ẩn', 'Mặc định ẩn.'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng "Họ tên - Mã phòng ban".'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Người cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng "Họ tên - Mã phòng ban".'],
        ['Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Trạng thái', 'Table/Grid', 'Read-only', 'Hiển thị', '- "Hoạt động" nền xanh.\n- "Khóa" nền đỏ.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sửa: kho Hoạt động, có quyền.\n- Xóa: kho Hoạt động, chưa được dùng ở đâu, có quyền (BR-09).\n- Khóa: kho Hoạt động và không còn tồn (BR-08); Mở khóa: kho đang Khóa.\n- Lịch sử: luôn có.\n- Có 4 nút thì hiện 2 nút đầu, các nút còn lại nằm trong nút ba chấm "Hành động khác".\n- Nút không dùng được thì ẩn, không làm mờ. Cột khóa, không ẩn được.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Kiểm tra quyền "Quản lý kho"; thiếu quyền → menu không hiện, mở thẳng màn bị từ chối.\nAfter:\n– Tải trang 1 theo phạm vi công ty (BR-01), kho tạo gần nhất trên cùng.'],
        ['Bấm tiêu đề cột Mã kho kế toán / Tên kho kế toán / Ngày tạo / Ngày cập nhật', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại từ trang 1.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp, tải lại dữ liệu; đổi số dòng thì quay về trang 1.'],
        ['Bấm Mã kho kế toán', 'Click', 'After:\n– Mở cửa sổ "Xem chi tiết kho kế toán" (mục 2.10).'],
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách kho kế toán'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao: Công ty (chỉ Super admin), Trạng thái, Người tạo, Ngày tạo.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn Danh mục kho kế toán.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô tìm nhanh chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Ngày tạo "Từ" lớn hơn "Đến" → báo đỏ dưới ô, xoá bảng, không tải dữ liệu (BR-12).\n• Bấm Làm mới → xoá mọi điều kiện và tải lại danh sách.\n• Hệ thống ghi nhớ bộ lọc 10 phút khi rời màn rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực tìm kiếm và lọc (đã mở Tìm kiếm nâng cao)')],
    'ui': ui(['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả'], [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', '- Placeholder "Tìm theo mã, tên kho kế toán, người tạo".\n- Tìm gần đúng theo Mã kho kế toán, Tên kho kế toán, họ tên Người tạo, không phân biệt hoa thường.'],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Áp dụng từ khóa và các ô lọc.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá mọi điều kiện lọc và tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực các ô lọc (khi mở, nút đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" chọn ô lọc nào được hiển thị (áp dụng quy tắc chung).'],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Trống', '- Chỉ hiện với Super admin.\n- Lọc theo công ty sở hữu kho kế toán.'],
        ['Ô Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Trống', 'Bỏ trống thì hiện cả hai trạng thái.'],
        ['Ô Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc kho do người được chọn tạo.'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Một ô chọn khoảng Từ ngày → Đến ngày, tính cả 2 đầu mút.\n- Từ > Đến: báo đỏ "Đến ngày phải lớn hơn hoặc bằng Từ ngày."'],
    ]),
    'ui_widths': [0.45, 1.25, 0.85, 0.8, 1.05, 0.8, 2.6],
    'events': [
        ['Bấm Tìm kiếm / nhấn Enter ở ô tìm nhanh', 'Click', 'After:\n– Áp đồng thời từ khóa và các ô lọc, tải lại bảng từ trang 1.'],
        ['Chọn giá trị ở ô lọc', 'Change', 'During:\n– Ô Ngày tạo: Từ > Đến → báo đỏ dưới ô, toast cùng câu, xoá bảng, không tải dữ liệu.\nAfter:\n– Tải lại bảng từ trang 1.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khu vực ô lọc.'],
    ],
})

# 2.3 Thêm mới -------------------------------------------------------------------
FORM_ROWS = [
    ['Mã kho kế toán', 'Textbox', 'Enable', '1–50 ký tự: chữ không dấu, số, dấu - và _', 'Có', 'Trống', '- Duy nhất toàn hệ thống (BR-02).\n- Sai ký tự: báo đỏ ngay khi gõ "Chỉ gồm chữ không dấu, số, dấu - và _".\n- Quá 50 ký tự: "Vui lòng nhập tối đa 50 ký tự."\n- Trùng: "Đã tồn tại".'],
    ['Tên kho kế toán', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', '- Duy nhất toàn hệ thống (BR-03).\n- Ô không cho gõ quá 255 ký tự.\n- Trùng: "Đã tồn tại".'],
    ['Nhập xuất thẳng', 'Checkbox', 'Enable', 'Tích / bỏ tích', 'Không', 'Bỏ tích', 'Tích thì ẩn ô Kho vật lý và Địa chỉ; kho lưu không có kho vật lý, địa chỉ (BR-04).'],
    ['Kho vật lý', 'Dropdown', 'Enable / Ẩn', 'Kho vật lý đang Hoạt động của mọi công ty', 'Có (khi không Nhập xuất thẳng)', 'Trống', '- Hiển thị "Mã kho - Tên kho", có ô tìm.\n- Bỏ trống: "Bắt buộc phải nhập".\n- Kho vừa bị khóa: "Kho vật lý "<Tên kho>" đã bị khóa, vui lòng chọn kho khác" (BR-05).'],
    ['Địa chỉ', 'Textbox', 'Enable / Ẩn', '1–255 ký tự', 'Có (khi không Nhập xuất thẳng)', 'Trống', 'Bỏ trống: "Bắt buộc phải nhập".'],
    ['Kế toán kho', 'Dropdown', 'Enable', 'Nhân viên đang làm việc, chọn nhiều', 'Có', 'Trống', '- Hiển thị "Mã NV - Họ tên", có ô tìm.\n- Bỏ trống: "Bắt buộc phải nhập" (BR-06).'],
    ['Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động', 'Có nút × xoá nhanh; để trống thì lưu là Hoạt động.'],
    ['Mô tả', 'Textarea', 'Enable', '0–500 ký tự', 'Không', 'Trống', 'Quá 500 ký tự: "Nhập tối đa 500 ký tự".'],
]
FR.append({
    'ten': 'Thêm mới kho kế toán', 'uc': 'uc_them',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Thêm mới kho kế toán'],
        ['Mô tả', 'Tạo một kho kế toán mới qua cửa sổ nhập liệu; công ty của kho = công ty của người tạo (BR-07).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống tải lại danh sách kho vật lý đang Hoạt động, mở cửa sổ "Tạo mới kho kế toán", Trạng thái mặc định Hoạt động.\n3. Người dùng nhập Mã, Tên; tích Nhập xuất thẳng hoặc chọn Kho vật lý + nhập Địa chỉ; chọn Kế toán kho (Trạng thái, Mô tả nếu cần) rồi bấm Lưu.\n4. Hệ thống kiểm tra dữ liệu, ghi kho kế toán (công ty = công ty người tạo) và danh sách kế toán kho.\n5. Ghi nhận Tạo mới trong lịch sử.\n6. Đóng cửa sổ, tải lại danh sách, báo "Thêm mới thành công."'],
        ['Dòng sự kiện phụ', '• Thiếu / sai dữ liệu → báo đỏ dưới ô + toast "Bạn chưa nhập đầy đủ thông tin.", cửa sổ không đóng, dữ liệu đã nhập còn nguyên.\n• Bấm "Lưu & Tiếp tục" → lưu rồi giữ cửa sổ, các ô về trống để nhập kho tiếp.\n• Tích rồi bỏ tích Nhập xuất thẳng → 2 ô Kho vật lý, Địa chỉ hiện lại với giá trị đã chọn.\n• Bấm Đóng / (x) / bấm ra ngoài: chưa nhập gì thì đóng; đã nhập thì hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', 'Nút Lưu / Lưu & Tiếp tục bị khóa trong lúc đang lưu để tránh tạo trùng.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': POPUP % 'Tạo mới kho kế toán',
    'anh': [('10_create', 'Cửa sổ Tạo mới kho kế toán'), ('11_code_error', 'Lỗi định dạng Mã kho kế toán báo ngay khi gõ'),
            ('18_unsaved', 'Hộp xác nhận Thông tin chưa lưu khi đóng cửa sổ đã nhập dữ liệu')],
    'ui': ui(UI8, FORM_ROWS + [
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi đóng cửa sổ.'],
        ['Nút Lưu & Tiếp tục', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi giữ cửa sổ, xoá trắng các ô.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ, không lưu (đã nhập thì hỏi xác nhận).'],
        ['Hộp Thông tin chưa lưu', 'Label', 'Enable / Ẩn', '–', '–', 'Ẩn', '- Nội dung "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"\n- Nút Thoát: đóng không lưu; nút Ở lại: quay về cửa sổ.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho" (thiếu quyền thì nút ẩn).\nAfter:\n– Tải lại danh sách kho vật lý đang Hoạt động, mở cửa sổ với các ô trống, Trạng thái = Hoạt động.'],
        ['Gõ Mã kho kế toán', 'Change', 'During:\n– Sai ký tự hoặc quá 50 ký tự → báo đỏ ngay dưới ô.'],
        ['Tích / bỏ tích Nhập xuất thẳng', 'Change', 'After:\n– Tích: ẩn ô Kho vật lý, Địa chỉ. Bỏ tích: hiện lại 2 ô.'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho".\nDuring:\n– Kiểm tra bắt buộc, độ dài, ký tự Mã, trùng Mã / Tên toàn hệ thống, Kho vật lý + Địa chỉ khi không Nhập xuất thẳng, Kho vật lý đang Hoạt động, Kế toán kho ≥ 1 người.\n' + TRUOC_LUU + '\nAfter:\n– Ghi kho kế toán (công ty = công ty người tạo; Nhập xuất thẳng thì không lưu kho vật lý, địa chỉ), ghi danh sách kế toán kho.\n– Ghi nhận Tạo mới trong lịch sử.\n– Đóng cửa sổ, tải lại danh sách, báo "Thêm mới thành công."'],
        ['Bấm Lưu & Tiếp tục', 'Click', 'During:\n– Như nút Lưu.\n' + TRUOC_LUU + '\nAfter:\n– Ghi như nút Lưu, giữ cửa sổ, các ô về trống, Trạng thái về Hoạt động.'],
        ['Bấm Đóng / (x) / bấm ra ngoài', 'Click', 'After:\n– Chưa nhập gì → đóng cửa sổ.\n– Đã nhập → hiện hộp "Thông tin chưa lưu": Thoát thì đóng không lưu, Ở lại thì quay về cửa sổ.'],
    ],
})

# 2.4 Chỉnh sửa ------------------------------------------------------------------
EDIT_ROWS = [[r[0], r[1], r[2], r[3], r[4], 'Dữ liệu hiện tại', r[6]] for r in FORM_ROWS]
EDIT_ROWS[2] = ['Nhập xuất thẳng', 'Checkbox', 'Enable / Disable', 'Tích / bỏ tích', 'Không', 'Dữ liệu hiện tại',
                'Kho đã phát sinh tồn kho: ô bị khóa, không chuyển sang Nhập xuất thẳng được (BR-05).']
EDIT_ROWS[3] = ['Kho vật lý', 'Dropdown', 'Enable / Disable / Ẩn', 'Kho vật lý đang Hoạt động + kho đang gắn', 'Có (khi không Nhập xuất thẳng)', 'Dữ liệu hiện tại',
                '- Kho vật lý đang gắn mà đã bị khóa vẫn hiện tên kèm biểu tượng khóa, giữ nguyên thì lưu được.\n- Kho đã phát sinh tồn: ô bị khóa, icon ⓘ "Kho đã có phát sinh tồn kho nên không đổi được kho vật lý."']
EDIT_ROWS[6] = ['Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Không', 'Dữ liệu hiện tại',
                '- Kho còn tồn: ô bị khóa, icon ⓘ "Kho còn tồn nên không khóa được. Xuất hết hàng khỏi kho trước khi khóa."\n- Chọn Khóa rồi Lưu = khóa kho (BR-08).']
FR.append({
    'ten': 'Chỉnh sửa kho kế toán', 'uc': 'uc_sua',
    'qtc': 'Validate dữ liệu, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chỉnh sửa kho kế toán'],
        ['Mô tả', 'Sửa thông tin kho kế toán đang Hoạt động. Không đổi công ty của kho; kho đã phát sinh tồn kho thì không đổi được kho vật lý.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Kho đang Hoạt động và thuộc phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Sửa ở cột Hành động.\n2. Hệ thống tải lại danh sách kho vật lý, mở cửa sổ "Sửa kho kế toán" với dữ liệu hiện tại.\n3. Người dùng sửa và bấm Lưu.\n4. Hệ thống kiểm tra, ghi thay đổi, đồng bộ danh sách kế toán kho.\n5. Ghi nhận Thay đổi thông tin (đổi Trạng thái ghi riêng Khóa / Mở khóa) trong lịch sử.\n6. Đóng cửa sổ, báo "Cập nhật thành công."'],
        ['Dòng sự kiện phụ', '• Giữ nguyên Mã / Tên của chính kho → không báo trùng.\n• Kế toán kho đã nghỉ việc vẫn hiện trong ô kèm biểu tượng khóa, lưu lại không bị mất.\n• Kho cũ chưa gắn công ty → khi lưu được gán công ty của người sửa.\n• Chọn Trạng thái Khóa cho kho còn tồn (ô đã khóa trên giao diện; nếu dữ liệu vừa đổi) → báo "Kho có tồn không thể khóa."\n• Đổi kho vật lý / chuyển Nhập xuất thẳng khi kho đã phát sinh tồn (dữ liệu vừa đổi) → "Kho đã có phát sinh tồn kho, không thể thay đổi kho vật lý" / "Kho đã có phát sinh tồn kho, không thể chuyển sang nhập xuất thẳng".\n• Kho vừa bị người khác khóa → báo "Dữ liệu đã thay đổi, vui lòng tải lại".\n• Bấm Đóng khi đã sửa → hỏi "Thông tin chưa lưu".'],
    ],
    'menu_them': ' => Sửa {icon:btn_sua}',
    'ghi_chu_layout': POPUP % 'Sửa kho kế toán',
    'anh': [('12_edit', 'Cửa sổ Sửa kho kế toán (kho đã phát sinh tồn: ô Nhập xuất thẳng, Kho vật lý, Trạng thái bị khóa)')],
    'ui': ui(UI8, EDIT_ROWS + [
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu thay đổi rồi đóng cửa sổ.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng không lưu (đã sửa thì hỏi xác nhận). Cửa sổ Sửa không có nút Lưu & Tiếp tục.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện khi kho Hoạt động và người dùng có quyền.\nAfter:\n– Tải dữ liệu kho, mở cửa sổ; kho không còn (vừa bị xoá / ngoài phạm vi) → báo "Dữ liệu đã thay đổi, vui lòng tải lại".'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền, kho phải đang Hoạt động.\nDuring:\n– Kiểm tra như Thêm mới (bỏ qua trùng với chính kho; kho vật lý đang gắn được giữ dù đã khóa), kho đã phát sinh tồn thì không đổi kho vật lý, kho còn tồn thì không được chọn Khóa.\n' + TRUOC_LUU + '\nAfter:\n– Ghi thay đổi, đồng bộ kế toán kho; kho chưa có công ty thì gán công ty người sửa.\n– Ghi nhận Thay đổi thông tin / Khóa trong lịch sử.\n– Đóng cửa sổ, tải lại danh sách, báo "Cập nhật thành công."'],
        ['Bấm Đóng / (x) / bấm ra ngoài', 'Click', 'After:\n– Chưa đổi gì → đóng; đã đổi → hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
    ],
})

# 2.5 Xóa ---------------------------------------------------------------------------
FR.append({
    'ten': 'Xóa kho kế toán', 'uc': 'uc_xoa',
    'qtc': 'Quy tắc Xóa, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xóa kho kế toán'],
        ['Mô tả', 'Xóa hẳn kho kế toán đang Hoạt động và chưa được dùng ở đâu (BR-09). Kho đã được dùng thì không xóa được, dùng Khóa.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Kho đang Hoạt động, chưa được dùng ở đâu.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Xóa ở cột Hành động.\n2. Hệ thống hiện hộp "Xác nhận xóa": "Bạn có chắc muốn xóa kho kế toán \'<Tên kho kế toán>\'?"\n3. Người dùng bấm Xóa.\n4. Hệ thống ghi nhận Xóa trong lịch sử, xóa hẳn kho kèm danh sách kế toán kho.\n5. Tải lại danh sách, báo "Xóa thành công."'],
        ['Dòng sự kiện phụ', '• Bấm Hủy → đóng hộp, không thay đổi.\n• Kho vừa bị khóa → "Không thể xóa kho kế toán đang ở trạng thái khóa. Hãy mở khóa trước."\n• Kho vừa được dùng (tồn, chứng từ, khai ở công ty) → "Không thể xóa do dữ liệu đang được sử dụng."\n• Kho vừa bị người khác xóa → "Dữ liệu đã thay đổi, vui lòng tải lại".'],
    ],
    'menu_them': ' => Xóa {icon:btn_xoa}',
    'ghi_chu_layout': POPUP % 'Xác nhận xóa',
    'anh': [('13_delete', 'Hộp xác nhận xóa kho kế toán')],
    'ui': ui(UI4, [
        ['Nút Xóa (cột Hành động)', 'Button', 'Biểu tượng thùng rác; chỉ hiện khi kho Hoạt động, chưa được dùng ở đâu và người dùng có quyền.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận xóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn xóa kho kế toán \'<Tên kho kế toán>\'?"'],
        ['Nút Xóa', 'Button', 'Xác nhận xóa.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không xóa.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Xóa ở cột Hành động', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên kho.'],
        ['Bấm Xóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền, kho thuộc phạm vi.\nDuring:\n– Kho phải đang Hoạt động và chưa được dùng ở đâu.\n' + TRUOC_LUU + '\nAfter:\n– Ghi nhận Xóa trong lịch sử.\n– Xóa hẳn kho và danh sách kế toán kho; Mã, Tên được dùng lại.\n– Tải lại danh sách, báo "Xóa thành công."'],
        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.6 Khóa / Mở khóa -----------------------------------------------------------
FR.append({
    'ten': 'Khóa / Mở khóa kho kế toán', 'uc': 'uc_khoa',
    'qtc': 'Quy tắc Khóa/Mở khóa, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Khóa / Mở khóa kho kế toán'],
        ['Mô tả', 'Đổi trạng thái kho kế toán giữa Hoạt động và Khóa. Kho Khóa vẫn nằm trong danh mục nhưng không còn sửa được (BR-08).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Khóa: kho Hoạt động và không còn tồn. Mở khóa: kho đang Khóa.'],
        ['Dòng sự kiện chính', '1. Người dùng chọn Khóa (hoặc Mở khóa) ở cột Hành động.\n2. Hệ thống hiện hộp "Xác nhận khóa" / "Xác nhận mở khóa" kèm tên kho.\n3. Người dùng bấm Khóa / Mở khóa.\n4. Hệ thống đổi trạng thái, ghi nhận Khóa / Mở khóa trong lịch sử.\n5. Tải lại danh sách, báo "Khóa thành công." / "Mở khóa thành công."'],
        ['Dòng sự kiện phụ', '• Bấm Hủy → không thay đổi.\n• Kho còn tồn: không có nút Khóa; nếu tồn vừa phát sinh → báo "Kho có tồn không thể khóa."\n• Kho đã bị người khác đổi trạng thái → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n• Sau khi Khóa: nút Sửa, Xóa ẩn; sau khi Mở khóa: nút Sửa hiện lại.'],
    ],
    'menu_them': ' => Khóa {icon:btn_khoa_row} / Mở khóa {icon:btn_mokhoa_row}',
    'ghi_chu_layout': POPUP % 'Xác nhận khóa / Xác nhận mở khóa',
    'anh': [('14_lock', 'Hộp xác nhận khóa kho kế toán'), ('15_unlock', 'Hộp xác nhận mở khóa kho kế toán')],
    'ui': ui(UI4, [
        ['Nút Khóa (cột Hành động)', 'Button', '- Biểu tượng ổ khóa; hiện khi kho Hoạt động, không còn tồn, có quyền.\n- Dòng có nút Xóa thì Khóa nằm trong nút ba chấm "Hành động khác".'],
        ['Nút Mở khóa (cột Hành động)', 'Button', 'Biểu tượng ổ khóa mở; hiện khi kho đang Khóa, có quyền.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận khóa" hoặc "Xác nhận mở khóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn khóa kho kế toán \'<Tên kho kế toán>\'?" / "Bạn có chắc muốn mở khóa kho kế toán \'<Tên kho kế toán>\'?"'],
        ['Nút Khóa / Mở khóa', 'Button', 'Xác nhận đổi trạng thái.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không thay đổi.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Chọn Khóa / Mở khóa', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên kho.'],
        ['Bấm Khóa / Mở khóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền, kho thuộc phạm vi.\nDuring:\n– Kho đã ở trạng thái đích → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n– Khóa mà kho còn tồn → "Kho có tồn không thể khóa."\n' + TRUOC_LUU + '\nAfter:\n– Đổi trạng thái, ghi nhận Khóa / Mở khóa trong lịch sử, tải lại danh sách, báo thành công.'],
        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.7 Lịch sử --------------------------------------------------------------------
FR.append({
    'ten': 'Xem lịch sử thay đổi',
    'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem lịch sử thay đổi kho kế toán'],
        ['Mô tả', 'Liệt kê các lần thao tác trên một kho kế toán (Tạo mới, Thay đổi thông tin, Khóa, Mở khóa, Xóa), mới nhất ở trên, kèm người thực hiện, thời điểm, giá trị cũ → mới.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Lịch sử ở cột Hành động (hoặc Xem lịch sử trong cửa sổ Xem chi tiết).\n2. Hệ thống mở cửa sổ "Lịch sử thay đổi: <Tên kho kế toán>" và liệt kê các mốc.'],
        ['Dòng sự kiện phụ', '• Lọc theo Loại hành động, Người thực hiện, Từ ngày / Đến ngày bằng nút Bộ lọc trong cửa sổ.\n• Các trường được ghi: Mã kho kế toán, Tên kho kế toán, Nhập xuất thẳng (Có / Không), Kho vật lý (bằng tên), Địa chỉ, Mô tả, Kế toán kho (bằng họ tên), Trạng thái.'],
    ],
    'menu_them': ' => Lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': POPUP % 'Lịch sử thay đổi',
    'anh': [('16_history', 'Cửa sổ Lịch sử thay đổi của kho kế toán')],
    'ui': ui(UI6, [
        ['Nút Lịch sử (cột Hành động)', 'Button', 'Enable', 'Hiển thị', 'Luôn có ở mọi dòng (kể cả kho Khóa); dòng có 4 nút thì nằm trong nút ba chấm.'],
        ['Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Lịch sử thay đổi: <Tên kho kế toán>', ''],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Mở các ô lọc Loại hành động, Người thực hiện, Từ ngày, Đến ngày.'],
        ['Danh sách mốc', 'Table/Grid', 'Read-only', 'Theo dữ liệu', '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, loại hành động, "Người thực hiện: Họ tên — Phòng ban".\n- Dòng thay đổi: "<Trường>: giá trị cũ → giá trị mới".\n- Chưa có dữ liệu: "Chưa có lịch sử thao tác nào."'],
        ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lịch sử', 'Click', 'After:\n– Tải lịch sử của kho, mới nhất trên cùng.'],
        ['Chọn điều kiện ở Bộ lọc', 'Change', 'After:\n– Lọc lại các mốc; không có mốc khớp → "Không có lịch sử phù hợp bộ lọc."'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.8 Import ---------------------------------------------------------------------
FR.append({
    'ten': 'Import kho kế toán từ file Excel', 'uc': 'uc_import',
    'qtc': 'Quy tắc Import file, Validate dữ liệu, Thông báo.',
    'gioi_thieu': [
        ['Tên chức năng', 'Import kho kế toán từ file Excel'],
        ['Mô tả', 'Tạo nhiều kho kế toán từ file Excel theo file mẫu. Mỗi dòng được kiểm tra và ghi như khi Tạo mới (ghi lịch sử) (BR-10).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Import Excel, hệ thống mở cửa sổ "Import kho kế toán".\n2. Bấm Tải file mẫu (Mau_import_kho_ke_toan.xlsx), điền dữ liệu.\n3. Bấm Chọn file Excel, chọn file, bấm Load lên bảng: dữ liệu hiện ở bảng xem trước, ô Tổng = số dòng.\n4. Bấm Validate: hệ thống kiểm tra từng dòng (chưa ghi dữ liệu), hiện Tổng / Hợp lệ / Lỗi; dòng lỗi tô đỏ kèm lý do, dòng hợp lệ bị khóa.\n5. Sửa dòng lỗi rồi Validate lại, hoặc bấm Bỏ dòng lỗi.\n6. Khi không còn dòng lỗi, bấm Import: hệ thống ghi từng dòng, ghi nhận Tạo mới trong lịch sử, báo "Import thành công N kho kế toán.", tải lại danh sách.'],
        ['Dòng sự kiện phụ', '• File quá 500 dòng dữ liệu → "File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần."\n• Dòng vừa bị trùng với kho người khác tạo trong lúc Import → bị bỏ qua, bảng kết quả "Import xong: a dòng thành công, b dòng lỗi bị bỏ qua" (nút Sao chép).\n• Bấm Xoá trạng thái validate để sửa lại cả dòng đã khóa.\n• Bấm Làm mới để làm lại từ đầu; Đóng để thoát.'],
    ],
    'menu_them': ' => Import Excel {icon:btn_import}',
    'ghi_chu_layout': POPUP % 'Import kho kế toán',
    'anh': [('21_import_open', 'Cửa sổ Import kho kế toán khi vừa mở'), ('22_import_loaded', 'Dữ liệu sau khi Load lên bảng'),
            ('23_import_validated', 'Kết quả Validate — dòng lỗi nêu rõ lý do')],
    'ui': ui(UI7I, [
        ['Nút Chọn file Excel', 'Button', 'Enable', '–', '–', 'Chọn file .xlsx, hiện tên file bên cạnh.'],
        ['Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Tải Mau_import_kho_ke_toan.xlsx: dòng 1 tên cột (cột bắt buộc có *), dòng 2 hướng dẫn, 2 dòng dữ liệu mẫu.'],
        ['Nút Load lên bảng', 'Button', 'Enable / Disable', '–', 'Disable', 'Bấm được khi đã chọn file; đọc file lên bảng xem trước.'],
        ['Nút Validate', 'Button', 'Enable / Disable', '–', 'Disable', 'Bấm được khi bảng có dữ liệu; kiểm tra từng dòng, chưa ghi dữ liệu.'],
        ['Nút Import', 'Button', 'Enable / Disable', '–', 'Disable', 'Chỉ bấm được khi đã Validate, còn ≥ 1 dòng hợp lệ và KHÔNG còn dòng lỗi.'],
        ['Ô Tổng / Hợp lệ / Lỗi', 'Label', 'Read-only', '–', 'Tổng: 0', 'Tổng hiện sau Load; Hợp lệ, Lỗi hiện sau Validate.'],
        ['Cột Mã kho kế toán *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Chữ không dấu, số, dấu - và _, tối đa 50 ký tự, không trùng hệ thống và trong file.'],
        ['Cột Tên kho kế toán *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Tối đa 255 ký tự, không trùng hệ thống và trong file.'],
        ['Cột Nhập xuất thẳng', 'Table/Grid', 'Enable', 'Không', 'Theo file', 'Có / Không; để trống = Không.'],
        ['Cột Mã kho vật lý', 'Table/Grid', 'Enable', 'Khi Nhập xuất thẳng = Không', 'Theo file', 'Mã ở màn Kho vật lý (mọi công ty), kho phải đang Hoạt động. Nhập xuất thẳng = Có thì bỏ qua cột này.'],
        ['Cột Địa chỉ', 'Table/Grid', 'Enable', 'Khi Nhập xuất thẳng = Không', 'Theo file', 'Tối đa 255 ký tự.'],
        ['Cột Mã kế toán kho *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Mã nhân viên đang làm việc; nhiều người cách nhau dấu phẩy.'],
        ['Cột Trạng thái', 'Table/Grid', 'Enable', 'Không', 'Theo file', 'Hoạt động / Khóa; để trống = Hoạt động.'],
        ['Cột Mô tả', 'Table/Grid', 'Enable', 'Không', 'Theo file', 'Tối đa 500 ký tự.'],
        ['Nút Bỏ dòng lỗi', 'Button', 'Enable', '–', '–', 'Loại các dòng lỗi khỏi bảng xem trước.'],
        ['Nút Xoá trạng thái validate', 'Button', 'Enable', '–', '–', 'Mở khóa mọi dòng để sửa lại, phải Validate lại.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', 'Đóng cửa sổ.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá file và bảng, làm lại từ đầu.'],
    ]),
    'ui_widths': UI7IW,
    'bang_cot': True,
    'events': [
        ['Bấm Load lên bảng', 'Click', 'During:\n– File không có dòng dữ liệu → "Không có dòng dữ liệu hợp lệ."\n– Quá 500 dòng → báo giới hạn 500 dòng.\nAfter:\n– Hiện dữ liệu lên bảng xem trước, ô Tổng = số dòng.'],
        ['Bấm Validate', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho".\nDuring:\n– Mỗi dòng kiểm như Tạo mới; Nhập xuất thẳng chỉ nhận Có / Không; mã kho vật lý không tồn tại; mã kế toán không tồn tại / đã nghỉ việc; trùng Mã / Tên trong file ("Bị trùng trong file").\nAfter:\n– Hiện Tổng / Hợp lệ / Lỗi, toast "Validate xong: X hợp lệ, Y không hợp lệ" (hoặc "Validate thành công"); dòng lỗi tô đỏ kèm lý do theo thứ tự cột, dòng hợp lệ bị khóa.'],
        ['Bấm Import', 'Click', 'Before:\n– Đã Validate, không còn dòng lỗi.\nDuring:\n– Hệ thống kiểm lại từng dòng ngay trước khi ghi.\n' + TRUOC_LUU + '\nAfter:\n– Ghi từng dòng như Tạo mới, ghi nhận Tạo mới trong lịch sử.\n– Báo "Import thành công N kho kế toán.", đóng cửa sổ, tải lại danh sách; có dòng bị bỏ qua thì hiện bảng kết quả.'],
        ['Bấm Bỏ dòng lỗi / Xoá trạng thái validate', 'Click', 'After:\n– Bỏ dòng lỗi khỏi bảng / mở khóa các dòng để sửa.'],
        ['Bấm Đóng / Làm mới', 'Click', 'After:\n– Đóng cửa sổ / xoá dữ liệu đang xem để làm lại.'],
    ],
})

# 2.9 Xuất Excel -------------------------------------------------------------------
FR.append({
    'ten': 'Xuất danh sách ra Excel', 'uc': 'uc_xuat',
    'qtc': 'Quy tắc Excel, Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách kho kế toán ra Excel'],
        ['Mô tả', 'Xuất toàn bộ kho kế toán khớp bộ lọc đang áp dụng (mọi trang) ra file Excel, người dùng chọn trường và thứ tự cột (BR-11).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng lọc danh sách (nếu cần), bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất file", tích sẵn các cột đang hiện trên bảng.\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự rồi bấm Xuất file.\n4. Hệ thống tải file danh_sach_kho_ke_toan.xlsx, báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Kết quả rỗng vẫn xuất file (tiêu đề + tên cột).\n• Ô Ngày tạo đang sai (Từ > Đến) → báo lỗi, không xuất.\n• Lỗi hệ thống → "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': POPUP % 'Chọn trường xuất file',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất file')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '"Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file."'],
        ['Danh sách trường', 'Table/Grid', 'Enable', 'Tích theo cột đang hiện', '13 trường: Mã kho kế toán, Tên kho kế toán, Kho vật lý, Nhập xuất thẳng, Địa chỉ, Kế toán kho, Công ty, Mô tả, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. Trường đang tích xếp trước; mỗi trường có ô tích và biểu tượng ☰ kéo đổi vị trí.'],
        ['Nút Chọn tất cả', 'Button', 'Enable', '–', 'Tích mọi trường.'],
        ['Nút Bỏ chọn hết', 'Button', 'Enable', '–', 'Bỏ tích mọi trường.'],
        ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn x/13 trường', ''],
        ['Nút Xuất file', 'Button', 'Enable / Disable', 'Enable', 'Tải file; không bấm được khi không còn trường nào được chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ, không xuất.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ, tích sẵn theo cột đang hiện.'],
        ['Bấm Xuất file', 'Click', 'During:\n– Ô Ngày tạo sai → báo "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", không xuất.\n' + TRUOC_LUU + '\nAfter:\n– Tải file danh_sach_kho_ke_toan.xlsx: tiêu đề "Danh sách kho kế toán", cột theo thứ tự đã chọn, mọi dòng khớp bộ lọc; báo "Xuất Excel thành công".'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.10 Xem chi tiết ----------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết kho kế toán', 'uc': 'uc_xem',
    'qtc': 'Màn Xem chi tiết, Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết kho kế toán'],
        ['Mô tả', 'Xem toàn bộ thông tin một kho kế toán ở chế độ chỉ đọc, kèm khối Lịch sử.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm vào Mã kho kế toán trên bảng.\n2. Hệ thống mở cửa sổ "Xem chi tiết kho kế toán", mọi ô chỉ đọc.\n3. Bấm Xem lịch sử để mở khối Lịch sử ngay trong cửa sổ.'],
        ['Dòng sự kiện phụ', '• Kho Nhập xuất thẳng: ô Nhập xuất thẳng được tích, không hiện Kho vật lý / Địa chỉ.\n• Kho vừa bị xoá / ngoài phạm vi → báo "Dữ liệu đã thay đổi, vui lòng tải lại", không mở cửa sổ.'],
    ],
    'menu_them': ' => Bấm Mã kho kế toán',
    'ghi_chu_layout': POPUP % 'Xem chi tiết kho kế toán',
    'anh': [('17_detail', 'Cửa sổ Xem chi tiết kho kế toán ở chế độ chỉ đọc'),
            ('17b_detail_history', 'Khối Lịch sử trong cửa sổ Xem chi tiết')],
    'ui': ui(UI6, [
        ['Mã kho kế toán, Tên kho kế toán', 'Textbox', 'Read-only', 'Dữ liệu hiện tại', 'Không có dấu (*).'],
        ['Nhập xuất thẳng', 'Checkbox', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Kho vật lý, Địa chỉ', 'Dropdown / Textbox', 'Read-only / Ẩn', 'Dữ liệu hiện tại', 'Kho vật lý dạng "Mã kho - Tên kho". Ẩn với kho Nhập xuất thẳng.'],
        ['Kế toán kho', 'Dropdown', 'Read-only', 'Dữ liệu hiện tại', 'Các kế toán dạng "Mã NV - Họ tên".'],
        ['Trạng thái', 'Dropdown', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Mô tả', 'Textarea', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Khối Lịch sử', 'Table/Grid', 'Enable', 'Thu gọn', '- Nút Xem lịch sử mở khối, hiện số mốc.\n- Nút Làm mới tải lại, Thu gọn đóng khối, Bộ lọc lọc mốc như mục 2.7.'],
        ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ. Không có nút Lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Mã kho kế toán', 'Click', 'After:\n– Tải dữ liệu, mở cửa sổ chỉ đọc.'],
        ['Bấm Xem lịch sử', 'Click', 'After:\n– Mở khối Lịch sử, tải các mốc.'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.11 Tùy chỉnh cột ---------------------------------------------------------------
FR.append({
    'ten': 'Tùy chỉnh cột hiển thị',
    'qtc': 'Tùy chỉnh cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tùy chỉnh cột hiển thị'],
        ['Mô tả', 'Ẩn / hiện và đổi thứ tự các cột của bảng danh sách; cấu hình lưu theo từng người dùng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Cấu hình cột hiển thị.\n2. Hệ thống mở cửa sổ "Tuỳ chỉnh cột".\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự, bấm Lưu.\n4. Hệ thống áp dụng lên bảng, lưu cấu hình, báo "Cập nhật thành công".'],
        ['Dòng sự kiện phụ', '• Cột STT, Mã kho kế toán, Hành động là cột khóa: không bỏ tích, không kéo được.\n• Bấm Đóng → bỏ các thay đổi vừa chỉnh.'],
    ],
    'menu_them': ' => Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': POPUP % 'Tuỳ chỉnh cột',
    'anh': [('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột — STT, Mã kho kế toán, Hành động bị khóa')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '"Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng."'],
        ['Danh sách cột', 'Table/Grid', 'Enable', 'Theo cấu hình đã lưu', '15 cột theo thứ tự trên bảng. Mặc định ẩn: Nhập xuất thẳng, Địa chỉ, Mô tả.'],
        ['Cột khóa', 'Table/Grid', 'Disable', 'Luôn tích', 'STT, Mã kho kế toán, Hành động: ô tích xám kèm biểu tượng khóa, không ẩn và không đổi vị trí được.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Tích / bỏ tích mọi cột (trừ cột khóa).'],
        ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn x/15 cột', ''],
        ['Nút Lưu', 'Button', 'Enable', '–', 'Áp dụng và lưu cấu hình cho người dùng; báo "Cập nhật thành công" (lỗi: "Thao tác thất bại").'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng, bỏ thay đổi.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Cấu hình cột hiển thị', 'Click', 'After:\n– Mở cửa sổ theo cấu hình đang dùng.'],
        ['Tích / bỏ tích, kéo ☰', 'Drag', 'After:\n– Đổi trạng thái hiện / thứ tự trong cửa sổ (chưa áp dụng).'],
        ['Bấm Lưu', 'Click', 'After:\n– Áp dụng lên bảng, lưu cấu hình theo người dùng, báo "Cập nhật thành công".'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng, không áp dụng.'],
    ],
})

S = {
    'ten': TEN,
    'menu': [('Kho', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Kho kế toán', 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu chức năng.',
        'Làm rõ phạm vi dữ liệu theo công ty của kho kế toán, ràng buộc trùng Mã / Tên toàn hệ thống, kho Nhập xuất thẳng, ràng buộc đổi kho vật lý khi kho đã phát sinh tồn, điều kiện Khóa (kho còn tồn) và Xóa (kho chưa được dùng ở đâu).',
    ],
    'thuat_ngu': [
        ['Kho kế toán', 'Kho dùng để hạch toán tồn kho (tồn kế toán) của từng công ty; nằm trong một kho vật lý (trừ kho Nhập xuất thẳng).'],
        ['Kho vật lý', 'Kho hàng thực tế (màn Danh mục kho vật lý); một kho vật lý có thể chứa kho kế toán của nhiều công ty.'],
        ['Nhập xuất thẳng', 'Kho kế toán không gắn kho vật lý, dùng cho hàng nhập / xuất thẳng không qua kho.'],
        ['Kế toán kho', 'Nhân viên kế toán phụ trách kho kế toán; một kho có một hoặc nhiều kế toán kho.'],
        ['Tồn', 'Số lượng hàng đang có ở kho kế toán; "còn tồn" = có mặt hàng số lượng lớn hơn 0.'],
        ['Đã phát sinh tồn', 'Kho từng có dòng tồn kế toán (kể cả tồn đã về 0).'],
        ['Hoạt động', 'Trạng thái kho dùng được ở các màn nghiệp vụ.'],
        ['Khóa', 'Kho vẫn nằm trong danh mục, xem được lịch sử nhưng không sửa / xóa được.'],
        ['Super admin', 'Tài khoản quản trị cao nhất, xem được kho kế toán của mọi công ty.'],
    ],
    'quyen_truoc': ['Màn hình dùng một quyền duy nhất "Quản lý kho" (nhóm Danh mục kho) cho cả xem lẫn thao tác; quyền này dùng chung cho 7 màn Danh mục của phân hệ Kho. Quyền được gán vào vai trò theo công ty.'],
    'quyen_rows': [['Quản lý kho', 'Xem danh sách, tìm kiếm, xem chi tiết, lịch sử, tùy chỉnh cột, xuất Excel; Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Import Excel.']],
    'ma_tran': [['Chức năng', 'Quản lý kho', 'Không có quyền']] + [[f, 'Có', 'Không'] for f in [
        'FR-01 Xem danh sách kho kế toán', 'FR-02 Tìm kiếm và lọc', 'FR-03 Thêm mới kho kế toán', 'FR-04 Chỉnh sửa kho kế toán',
        'FR-05 Xóa kho kế toán', 'FR-06 Khóa / Mở khóa kho kế toán', 'FR-07 Xem lịch sử thay đổi',
        'FR-08 Import kho kế toán từ file Excel', 'FR-09 Xuất danh sách ra Excel', 'FR-10 Xem chi tiết kho kế toán',
        'FR-11 Tùy chỉnh cột hiển thị']],
    'ma_tran_widths': [2.6, 1.2, 1.2],
    'quyen_sau': ['Phạm vi dữ liệu: người dùng thường chỉ thấy và thao tác kho kế toán thuộc công ty của mình; Super admin thấy kho mọi công ty và có thêm ô lọc Công ty (BR-01).'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Phạm vi dữ liệu theo công ty', [
            '– Người dùng thường chỉ thấy, xem, sửa, khóa, xóa, xuất kho kế toán có công ty sở hữu = công ty đang làm việc của mình.',
            '– Phạm vi tính theo công ty của CHÍNH kho kế toán, không theo công ty của kho vật lý chứa nó.',
            '– Super admin thấy kho mọi công ty, có thêm ô lọc Công ty; kho chưa gắn công ty chỉ Super admin thấy.',
            '– Thao tác trên kho ngoài phạm vi bị từ chối như dữ liệu không tồn tại.'], ['Xem danh sách', 'Xuất Excel', 'Chỉnh sửa', 'Xóa', 'Khóa / Mở khóa']),
        ('BR-02', 'Mã kho kế toán', [
            '– Bắt buộc, 1–50 ký tự, chỉ gồm chữ không dấu, số, dấu - và _; cắt khoảng trắng đầu / cuối.',
            '– Duy nhất trên TOÀN hệ thống (mọi công ty, mọi trạng thái), không phân biệt hoa / thường.',
            '– Giữ nguyên chữ hoa / thường người dùng nhập.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-03', 'Tên kho kế toán', ['– Bắt buộc, tối đa 255 ký tự, duy nhất trên toàn hệ thống như Mã.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-04', 'Nhập xuất thẳng', [
            '– Tích Nhập xuất thẳng: kho không có kho vật lý, không cần địa chỉ; hệ thống không lưu 2 trường này.',
            '– Không tích: Kho vật lý và Địa chỉ bắt buộc.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-05', 'Kho vật lý', [
            '– Chỉ chọn kho vật lý đang Hoạt động, của mọi công ty; hiển thị "Mã kho - Tên kho".',
            '– Kho vật lý đang gắn mà đã bị khóa: vẫn hiện (biểu tượng khóa) và được giữ khi lưu; chọn mới kho đã khóa thì báo "Kho vật lý "<Tên kho>" đã bị khóa, vui lòng chọn kho khác".',
            '– Kho kế toán đã phát sinh tồn: không đổi được kho vật lý, không chuyển được sang Nhập xuất thẳng (ô bị khóa, máy chủ chặn khi lưu).'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-06', 'Kế toán kho', [
            '– Bắt buộc ít nhất 1 nhân viên; chỉ chọn được nhân viên đang làm việc (mọi công ty).',
            '– Kế toán đã nghỉ việc đang gắn với kho vẫn hiển thị (kèm biểu tượng khóa) và được giữ khi lưu.',
            '– Cột Kế toán kho trên bảng và file xuất chỉ ghi họ tên, cách nhau dấu phẩy.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-07', 'Công ty của kho kế toán', [
            '– Công ty sở hữu = công ty của người tạo (không chọn trên form), kể cả khi kho vật lý thuộc công ty khác.',
            '– Sửa kho cũ chưa gắn công ty thì gán công ty của người sửa; kho đã có công ty thì không đổi.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-08', 'Điều kiện Khóa / Mở khóa', [
            '– Chỉ khóa được kho đang Hoạt động và KHÔNG còn tồn ("Kho có tồn không thể khóa."); áp dụng cả khi đổi Trạng thái trong cửa sổ Sửa.',
            '– Kho từng có tồn nay đã về 0 vẫn khóa được.',
            '– Mở khóa luôn được, không phụ thuộc trạng thái kho vật lý.',
            '– Kho đang Khóa: ẩn Sửa, Xóa.'], ['Khóa / Mở khóa', 'Chỉnh sửa']),
        ('BR-09', 'Điều kiện Xóa', [
            '– Chỉ xóa kho đang Hoạt động và CHƯA được dùng ở đâu: tồn kế toán, tồn đầu kỳ, kiểm kê, chứng từ nhập / xuất / yêu cầu nhập / yêu cầu xuất, kho khuyến mại / kho hàng gửi khai ở công ty.',
            '– Xóa hẳn kho và danh sách kế toán kho; Mã, Tên dùng lại được.',
            '– Kho đã được dùng: không có nút Xóa, dùng Khóa khi không dùng nữa.'], ['Xóa']),
        ('BR-10', 'Import', [
            '– Mỗi dòng kiểm và ghi như Tạo mới (BR-02 → BR-07); kho vật lý nhập bằng mã, kế toán kho nhập bằng mã nhân viên.',
            '– Nhập xuất thẳng chỉ nhận Có / Không (trống = Không); Có thì bỏ qua Mã kho vật lý.',
            '– Trùng Mã / Tên giữa các dòng trong file → "Bị trùng trong file".',
            '– Tối đa 500 dòng dữ liệu mỗi lần; chỉ Import khi đã Validate và không còn dòng lỗi.'], ['Import']),
        ('BR-11', 'Xuất Excel', ['– Xuất mọi dòng khớp bộ lọc đang áp dụng (không chỉ trang đang xem), cột theo thứ tự người dùng chọn; tên file danh_sach_kho_ke_toan.xlsx.'], ['Xuất Excel']),
        ('BR-12', 'Lọc Ngày tạo', ['– Ngày tạo Từ lớn hơn Đến → báo đỏ "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", xoá bảng, không tải dữ liệu và không xuất Excel.'], ['Tìm kiếm và lọc', 'Xuất Excel']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây chọn, lọc, lưu hoặc hiển thị dữ liệu Kho kế toán (kho kế toán của dòng hàng, tồn kho kế toán theo kho, kế toán kho phụ trách).',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng có quyền "Quản lý kho"',
    'mains': [('FR-01', 'Xem danh sách kho kế toán', 'view'), ('FR-03', 'Thêm mới kho kế toán', 'crud'),
              ('FR-04', 'Chỉnh sửa kho kế toán', 'crud'), ('FR-05', 'Xóa kho kế toán', 'action'),
              ('FR-06', 'Khóa / Mở khóa kho kế toán', 'action'), ('FR-08', 'Import kho kế toán từ file Excel', 'io'),
              ('FR-09', 'Xuất danh sách kho kế toán ra Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc kho kế toán', 'view'), ('FR-10', 'Xem chi tiết kho kế toán', 'view'),
             ('FR-11', 'Tùy chỉnh cột hiển thị', 'view'), ('FR-07', 'Xem lịch sử thay đổi', 'view')],
    'rieng': [('FR-03', 'Thêm mới kho kế toán', 'crud', 'uc_them'), ('FR-04', 'Chỉnh sửa kho kế toán', 'crud', 'uc_sua'),
              ('FR-05', 'Xóa kho kế toán', 'action', 'uc_xoa'), ('FR-06', 'Khóa / Mở khóa kho kế toán', 'action', 'uc_khoa'),
              ('FR-08', 'Import kho kế toán từ file Excel', 'io', 'uc_import'),
              ('FR-09', 'Xuất danh sách kho kế toán ra Excel', 'io', 'uc_xuat'), ('FR-10', 'Xem chi tiết kho kế toán', 'view', 'uc_xem')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)

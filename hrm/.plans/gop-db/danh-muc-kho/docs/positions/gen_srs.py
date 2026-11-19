# -*- coding: utf-8 -*-
"""SRS - Danh mục vị trí (form Danh mục quốc gia, TPE duyệt) — chép khuôn màn mẫu docs/warehouses/gen_srs.py.

Nguồn (code HRM hiện tại, nhánh có code kho):
  FE hrm-client/pages/warehouse/positions/{index.vue, AddPositionModal.vue}, utils/mixins/{vehicleCatalogScreenMixin,
     vehicleCatalogModalMixin, warehouseCatalogModalMixin, warehouseCatalogImportMixin, createdRangeFilterMixin,
     warehouseLockedFilterMixin}.js, utils/warehouse-catalog-import.js, components/warehouse-catalog/LockableFilterSelect.vue,
     components/subsystem-menu/warehouse.js
  BE Modules/MasterData: Entities/Warehouse/Position.php, Http/Controllers/V1/Warehouse/{PositionController,
     WarehouseTreeCatalogController}.php, ProductClassification/BaseCatalogController.php,
     Http/Requests/Warehouse/PositionRequest.php, Services/Warehouse/{PositionService, WarehouseCatalogScope,
     Concerns/ImportsWarehouseCatalogRows, Concerns/SearchesCodeNameOnly}.php, Transformers/Warehouse/PositionResource.php;
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

TEN = 'Danh mục vị trí'
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
    ('Kho', 'Phiếu nhập kho (chọn vị trí xếp hàng)', 'Kho => Nhập kho'),
    ('Kho', 'Phiếu nhập kho điều chỉnh kiểm kê', 'Kho => Nhập kho'),
    ('Kho', 'Phiếu xuất điều chỉnh sai số liệu', 'Kho => Xuất kho'),
    ('Kho', 'Phiếu xuất kho điều chỉnh kiểm kê', 'Kho => Xuất kho'),
    ('Kho', 'Điều chuyển kho', 'Kho => Điều chuyển'),
    ('Kho', 'Phiếu điều chuyển vị trí', 'Kho => Điều chuyển'),
    ('Kho', 'Kiểm kê theo vị trí', 'Kho => Kiểm kho => Theo vị trí'),
    ('Kho', 'Kiểm kê theo hàng hóa', 'Kho => Kiểm kho => Theo vị trí'),
    ('Kho', 'Thẻ kho', 'Kho => Báo cáo kho'),
    ('Kho', 'Báo cáo tồn kho chi tiết theo mặt hàng', 'Kho => Báo cáo kho'),
    ('Kho', 'Báo cáo tồn kho theo vị trí', 'Kho => Báo cáo kho'),
    ('Kho', 'Tổng hợp xuất nhập tồn', 'Kho => Báo cáo kho'),
    ('Kho', 'Kho vật lý (tự sinh vị trí tách ghép hàng)', 'Kho => Danh mục'),
    ('Kho', 'Dãy (tự sinh vị trí khi tạo dãy)', 'Kho => Danh mục'),
    ('Kho', 'Khoang (chỉ khóa được khi không còn vị trí đang hoạt động)', 'Kho => Danh mục'),
    ('Tài chính', 'Phiếu nhập kho (chọn vị trí xếp hàng)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
    ('Tài chính', 'Phiếu nhập hàng điều chỉnh kiểm kê', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
    ('Tài chính', 'Phiếu xuất kho (lấy hàng theo vị trí)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ('Tài chính', 'Phiếu nhập lại', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ('Tài chính', 'Phiếu xuất hàng điều chỉnh kiểm kê', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ('Tài chính', 'Kế hoạch kiểm kê theo vị trí', 'Tài chính => Kiểm kê'),
    ('Tài chính', 'Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả', 'Tài chính => Kiểm kê'),
]

# ------------------------------------------------------------------ dữ liệu SRS
FR = []

# 2.1 Xem danh sách -------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách vị trí',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang, Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách vị trí'],
        ['Mô tả', 'Hiển thị các vị trí (cả loại Thuộc khoang lẫn Tự do, cả Hoạt động lẫn Khóa) thuộc kho trong phạm vi dữ liệu của người dùng, có phân trang, sắp xếp và các nút thao tác theo từng dòng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn Danh mục vị trí theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), vị trí tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Người dùng thường chỉ thấy vị trí thuộc kho của công ty mình; Super admin thấy vị trí mọi công ty (BR-01).\n• Vị trí Tự do: cột Nhà kho, Dãy, Khoang để trống.\n• Không có vị trí khớp → bảng hiện "Không có dữ liệu phù hợp."'],
    ],
    'anh': [('01_list', 'Màn Danh mục vị trí lúc mới truy cập')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Danh sách vị trí', 'Tiêu đề khối danh sách và tiêu đề trang.'],
        ['Nút Tạo mới', 'Button', 'Enable / Ẩn', 'Hiển thị', '- Mở cửa sổ "Tạo mới vị trí" (mục 2.3).\n- Ẩn khi thiếu quyền "Quản lý kho".'],
        ['Nút Import Excel', 'Button', 'Enable / Ẩn', 'Hiển thị', '- Mở cửa sổ "Import vị trí" (mục 2.8).\n- Ẩn khi thiếu quyền.'],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất file" (mục 2.9).'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.11).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa, không ẩn được.'],
        ['Cột Mã vị trí', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sắp xếp được.\n- Chữ dạng liên kết: bấm vào mở cửa sổ "Xem chi tiết vị trí" (mục 2.10).\n- Cột khóa, không ẩn được; đứng yên khi cuộn ngang.'],
        ['Cột Tên vị trí', 'Table/Grid', 'Read-only', 'Hiển thị', 'Sắp xếp được. Dài thì xuống tối đa 2 dòng, rê chuột xem đủ.'],
        ['Cột Loại vị trí', 'Table/Grid', 'Read-only', 'Ẩn', '"Thuộc khoang" hoặc "Tự do". Mặc định ẩn, bật ở Tuỳ chỉnh cột.'],
        ['Cột Kho', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên kho vật lý chứa vị trí.'],
        ['Cột Nhà kho, Dãy, Khoang', 'Table/Grid', 'Read-only', 'Hiển thị', '- Tên nhà kho, dãy, khoang của vị trí Thuộc khoang.\n- Vị trí Tự do: để trống.'],
        ['Cột Mô tả', 'Table/Grid', 'Read-only', 'Ẩn', 'Mặc định ẩn.'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng "Họ tên - Mã phòng ban".'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm.'],
        ['Cột Người cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng "Họ tên - Mã phòng ban".'],
        ['Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm.'],
        ['Cột Trạng thái', 'Table/Grid', 'Read-only', 'Hiển thị', '- "Hoạt động" nền xanh.\n- "Khóa" nền đỏ.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sửa: vị trí Hoạt động, có quyền.\n- Xóa: vị trí Hoạt động, chưa được dùng ở đâu, có quyền (BR-08).\n- Khóa: vị trí Hoạt động (BR-06); Mở khóa: vị trí đang Khóa và cấp cha đang Hoạt động (BR-07).\n- Lịch sử: luôn có.\n- Có 4 nút thì hiện 2 nút đầu, các nút còn lại nằm trong nút ba chấm "Hành động khác".\n- Nút không dùng được thì ẩn, không làm mờ. Cột khóa, không ẩn được.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Kiểm tra quyền "Quản lý kho"; thiếu quyền → menu không hiện, mở thẳng màn bị từ chối.\nAfter:\n– Tải trang 1 theo phạm vi công ty (BR-01), vị trí tạo gần nhất trên cùng.'],
        ['Bấm tiêu đề cột Mã vị trí / Tên vị trí', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại từ trang 1.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp, tải lại dữ liệu; đổi số dòng thì quay về trang 1.'],
        ['Bấm Mã vị trí', 'Click', 'After:\n– Mở cửa sổ "Xem chi tiết vị trí" (mục 2.10).'],
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách vị trí'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao: Công ty (chỉ Super admin), Kho, Trạng thái, Người tạo, Ngày tạo.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn Danh mục vị trí.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô tìm nhanh chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Ô Kho mặc định chỉ liệt kê kho đang Hoạt động; bấm biểu tượng ổ khóa cạnh nhãn để hiện cả kho đã khóa (BR-11).\n• Đổi Công ty mà kho đang chọn không thuộc công ty đó → ô Kho tự bỏ chọn.\n• Ngày tạo "Từ" lớn hơn "Đến" → báo đỏ dưới ô, xoá bảng, không tải dữ liệu (BR-11).\n• Bấm Làm mới → xoá mọi điều kiện và tải lại danh sách.\n• Hệ thống ghi nhớ bộ lọc 10 phút khi rời màn rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực tìm kiếm và lọc (đã mở Tìm kiếm nâng cao)')],
    'ui': ui(['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả'], [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', '- Placeholder "Tìm theo mã, tên vị trí".\n- Tìm gần đúng theo Mã vị trí, Tên vị trí, không phân biệt hoa thường.'],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Áp dụng từ khóa và các ô lọc.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá mọi điều kiện lọc và tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực các ô lọc (khi mở, nút đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" chọn ô lọc nào được hiển thị (áp dụng quy tắc chung).'],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Trống', '- Chỉ hiện với Super admin.\n- Lọc vị trí theo công ty sở hữu kho.\n- Biểu tượng ổ khóa cạnh nhãn: hiện cả công ty đã khóa.'],
        ['Ô Kho', 'Dropdown', 'Enable', 'Kho trong phạm vi, dạng "Mã - Tên"', 'Trống', '- Lọc vị trí thuộc kho đã chọn (cả Thuộc khoang lẫn Tự do).\n- Biểu tượng ổ khóa cạnh nhãn: "Hiện cả kho đã khoá"; bấm lần nữa để ẩn lại.\n- Có chọn Công ty thì chỉ còn kho của công ty đó.'],
        ['Ô Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Trống', 'Bỏ trống thì hiện cả hai trạng thái.'],
        ['Ô Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc vị trí do người được chọn tạo.'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Một ô chọn khoảng Từ ngày → Đến ngày, tính cả 2 đầu mút.\n- Từ > Đến: báo đỏ "Đến ngày phải lớn hơn hoặc bằng Từ ngày."'],
    ]),
    'ui_widths': [0.45, 1.25, 0.85, 0.8, 1.05, 0.8, 2.6],
    'events': [
        ['Bấm Tìm kiếm / nhấn Enter ở ô tìm nhanh', 'Click', 'After:\n– Áp đồng thời từ khóa và các ô lọc, tải lại bảng từ trang 1.'],
        ['Chọn giá trị ở ô lọc', 'Change', 'During:\n– Ô Ngày tạo: Từ > Đến → báo đỏ dưới ô, toast cùng câu, xoá bảng, không tải dữ liệu.\n– Đổi Công ty: bỏ chọn Kho không thuộc công ty mới.\nAfter:\n– Tải lại bảng từ trang 1.'],
        ['Bấm biểu tượng ổ khóa ở ô Kho / Công ty', 'Click', 'After:\n– Thêm (hoặc bỏ) các kho / công ty đã khóa vào danh sách chọn; mục đã khóa có biểu tượng ổ khóa.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khu vực ô lọc.'],
    ],
})

# 2.3 Thêm mới -------------------------------------------------------------------
FORM_ROWS = [
    ['Loại vị trí', 'Dropdown', 'Enable', 'Thuộc khoang / Tự do', 'Có', 'Thuộc khoang', '- Không có nút × xoá.\n- Tự do: ẩn 3 ô Nhà kho, Dãy, Khoang.'],
    ['Kho', 'Dropdown', 'Enable', 'Kho đang Hoạt động trong phạm vi, dạng "Mã - Tên"', 'Có', 'Trống', '- Thuộc khoang: chỉ dùng để lọc ô Nhà kho; kho lưu theo khoang đã chọn (BR-04).\n- Tự do: kho của vị trí.\n- Bỏ trống: "Bắt buộc phải nhập".'],
    ['Nhà kho', 'Dropdown', 'Enable / Disable', 'Nhà kho đang Hoạt động của kho đã chọn', 'Có (Thuộc khoang)', 'Trống', '- Khóa khi chưa chọn Kho.\n- Đổi Kho thì ô tự bỏ chọn nếu không còn thuộc kho mới.'],
    ['Dãy', 'Dropdown', 'Enable / Disable', 'Dãy đang Hoạt động của nhà kho đã chọn', 'Có (Thuộc khoang)', 'Trống', 'Khóa khi chưa chọn Nhà kho; đổi Nhà kho thì tự bỏ chọn.'],
    ['Khoang', 'Dropdown', 'Enable / Disable', 'Khoang đang Hoạt động của dãy đã chọn', 'Có (Thuộc khoang)', 'Trống', '- Khóa khi chưa chọn Dãy; đổi Dãy thì tự bỏ chọn.\n- Khoang (hoặc dãy, nhà kho, kho cha) vừa bị khóa: \'Khoang "<tên>" đã bị khóa, vui lòng chọn khoang khác\'.'],
    ['Mã vị trí', 'Textbox', 'Enable', '1–50 ký tự: chữ không dấu, số, dấu - và _', 'Có', 'Trống', '- Duy nhất trong cùng một kho (BR-02).\n- Sai ký tự: báo đỏ ngay khi gõ "Chỉ gồm chữ không dấu, số, dấu - và _".\n- Quá 50 ký tự: báo đỏ ngay khi gõ.\n- Trùng: "Đã tồn tại trong kho này".'],
    ['Tên vị trí', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', '- Duy nhất trong khoang / trong kho với vị trí tự do (BR-03).\n- Ô không cho gõ quá 255 ký tự.\n- Trùng: "Đã tồn tại".'],
    ['Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động', 'Có nút × xoá nhanh; để trống thì lưu là Hoạt động.'],
    ['Mô tả', 'Textarea', 'Enable', '0–500 ký tự', 'Không', 'Trống', 'Quá 500 ký tự: "Nhập tối đa 500 ký tự".'],
]
FR.append({
    'ten': 'Thêm mới vị trí', 'uc': 'uc_them',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Thêm mới vị trí'],
        ['Mô tả', 'Tạo một vị trí mới qua cửa sổ nhập liệu, theo 2 loại: Thuộc khoang (chọn dây chuyền Kho → Nhà kho → Dãy → Khoang) hoặc Tự do (gắn thẳng vào kho).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Có kho (và khoang, nếu loại Thuộc khoang) đang Hoạt động trong phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở cửa sổ "Tạo mới vị trí", Loại vị trí mặc định Thuộc khoang, Trạng thái Hoạt động.\n3. Người dùng chọn Loại vị trí, Kho (Thuộc khoang thì chọn tiếp Nhà kho, Dãy, Khoang), nhập Mã vị trí, Tên vị trí (Trạng thái, Mô tả nếu cần) rồi bấm Lưu.\n4. Hệ thống kiểm tra dữ liệu, ghi vị trí; vị trí Thuộc khoang lấy kho theo khoang đã chọn.\n5. Ghi nhận Tạo mới trong lịch sử của vị trí.\n6. Đóng cửa sổ, tải lại danh sách, báo "Thêm mới thành công."'],
        ['Dòng sự kiện phụ', '• Thiếu / sai dữ liệu → báo đỏ dưới các ô cùng lúc + toast "Bạn chưa nhập đầy đủ thông tin.", cửa sổ không đóng, dữ liệu đã nhập còn nguyên.\n• Đổi Loại vị trí sang Tự do → 3 ô Nhà kho, Dãy, Khoang biến mất, khoang đã chọn không được lưu.\n• Bấm "Lưu & Tiếp tục" → lưu rồi giữ cửa sổ, các ô về mặc định để nhập tiếp.\n• Bấm Đóng / (x) / bấm ra ngoài: chưa nhập gì thì đóng; đã nhập thì hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', 'Nút Lưu / Lưu & Tiếp tục bị khóa trong lúc đang lưu để tránh tạo trùng.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': POPUP % 'Tạo mới vị trí',
    'anh': [('10_create', 'Cửa sổ Tạo mới vị trí — loại Thuộc khoang'),
            ('10b_create_free', 'Cửa sổ Tạo mới vị trí — loại Tự do (ẩn Nhà kho, Dãy, Khoang)'),
            ('11_code_error', 'Lỗi định dạng Mã vị trí báo ngay khi gõ'),
            ('18_unsaved', 'Hộp xác nhận Thông tin chưa lưu khi đóng cửa sổ đã nhập dữ liệu')],
    'ui': ui(UI8, FORM_ROWS + [
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi đóng cửa sổ.'],
        ['Nút Lưu & Tiếp tục', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi giữ cửa sổ, đưa các ô về mặc định.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ, không lưu (đã nhập thì hỏi xác nhận).'],
        ['Hộp Thông tin chưa lưu', 'Label', 'Enable / Ẩn', '–', '–', 'Ẩn', '- Nội dung "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"\n- Nút Thoát: đóng không lưu; nút Ở lại: quay về cửa sổ.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho" (thiếu quyền thì nút ẩn).\nAfter:\n– Mở cửa sổ: Loại vị trí = Thuộc khoang, Trạng thái = Hoạt động, các ô khác trống.'],
        ['Đổi Loại vị trí', 'Change', 'After:\n– Tự do: ẩn Nhà kho, Dãy, Khoang. Thuộc khoang: hiện lại 3 ô.'],
        ['Chọn Kho / Nhà kho / Dãy', 'Change', 'After:\n– Ô cấp dưới chỉ liệt kê mục thuộc cấp vừa chọn; mục cấp dưới đã chọn không còn thuộc cấp mới thì tự bỏ chọn.'],
        ['Gõ Mã vị trí', 'Change', 'During:\n– Sai ký tự hoặc quá 50 ký tự → báo đỏ ngay dưới ô.'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho".\nDuring:\n– Kiểm tra bắt buộc (Thuộc khoang: Kho, Nhà kho, Dãy, Khoang; Tự do: Kho), độ dài, ký tự Mã vị trí, trùng Mã trong kho, trùng Tên trong khoang / trong kho; khoang hoặc kho đã chọn phải còn trong phạm vi và đang Hoạt động.\n' + TRUOC_LUU + '\nAfter:\n– Ghi vị trí (Thuộc khoang: kho = kho của khoang).\n– Ghi nhận Tạo mới trong lịch sử.\n– Đóng cửa sổ, tải lại danh sách, báo "Thêm mới thành công."'],
        ['Bấm Lưu & Tiếp tục', 'Click', 'During:\n– Như nút Lưu.\n' + TRUOC_LUU + '\nAfter:\n– Ghi như nút Lưu, giữ cửa sổ, các ô về mặc định.'],
        ['Bấm Đóng / (x) / bấm ra ngoài', 'Click', 'After:\n– Chưa nhập gì → đóng cửa sổ.\n– Đã nhập → hiện hộp "Thông tin chưa lưu": Thoát thì đóng không lưu, Ở lại thì quay về cửa sổ.'],
    ],
})

# 2.4 Chỉnh sửa ------------------------------------------------------------------
EDIT_ROWS = [
    ['Loại vị trí, Kho, Nhà kho, Dãy, Khoang', 'Dropdown', 'Disable', 'Dữ liệu hiện tại', 'Không', 'Dữ liệu hiện tại', '- Không đổi được sau khi tạo; ô khóa nền xám, không có dấu *.\n- Cấp cha đã khóa / ngoài danh sách chọn vẫn hiện đúng tên kèm biểu tượng ổ khóa.'],
] + [[r[0], r[1], r[2], r[3], r[4], 'Dữ liệu hiện tại', r[6]] for r in FORM_ROWS[5:]]
EDIT_ROWS[3] = ['Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Dữ liệu hiện tại',
                'Chọn Khóa rồi Lưu = khóa vị trí (BR-06).']
FR.append({
    'ten': 'Chỉnh sửa vị trí', 'uc': 'uc_sua',
    'qtc': 'Validate dữ liệu, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chỉnh sửa vị trí'],
        ['Mô tả', 'Sửa Mã vị trí, Tên vị trí, Trạng thái, Mô tả của vị trí đang Hoạt động. Loại vị trí, Kho, Nhà kho, Dãy, Khoang không đổi được.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Vị trí đang Hoạt động và thuộc phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Sửa ở cột Hành động.\n2. Hệ thống mở cửa sổ "Sửa vị trí" với dữ liệu hiện tại.\n3. Người dùng sửa và bấm Lưu.\n4. Hệ thống kiểm tra, ghi thay đổi.\n5. Ghi nhận Thay đổi thông tin (đổi Trạng thái ghi riêng Khóa) trong lịch sử.\n6. Đóng cửa sổ, báo "Cập nhật thành công."'],
        ['Dòng sự kiện phụ', '• Giữ nguyên Mã / Tên của chính vị trí → không báo trùng.\n• Vị trí vừa bị người khác khóa / xóa → báo "Dữ liệu đã thay đổi, vui lòng tải lại".\n• Bấm Đóng khi đã sửa → hỏi "Thông tin chưa lưu".'],
    ],
    'menu_them': ' => Sửa {icon:btn_sua}',
    'ghi_chu_layout': POPUP % 'Sửa vị trí',
    'anh': [('12_edit', 'Cửa sổ Sửa vị trí (Loại vị trí, Kho, Nhà kho, Dãy, Khoang bị khóa)')],
    'ui': ui(UI8, EDIT_ROWS + [
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu thay đổi rồi đóng cửa sổ.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng không lưu (đã sửa thì hỏi xác nhận). Cửa sổ Sửa không có nút Lưu & Tiếp tục.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện khi vị trí Hoạt động và người dùng có quyền.\nAfter:\n– Tải dữ liệu vị trí, mở cửa sổ; vị trí không còn (vừa bị xoá / ngoài phạm vi) → báo "Dữ liệu đã thay đổi, vui lòng tải lại".'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền, vị trí phải đang Hoạt động.\nDuring:\n– Kiểm tra Mã, Tên như Thêm mới (trong kho / khoang hiện tại của vị trí, bỏ qua trùng với chính nó); Loại, Kho, Khoang giữ nguyên dù có gửi giá trị khác.\n' + TRUOC_LUU + '\nAfter:\n– Ghi thay đổi, ghi nhận Thay đổi thông tin / Khóa trong lịch sử.\n– Đóng cửa sổ, tải lại danh sách, báo "Cập nhật thành công."'],
        ['Bấm Đóng / (x) / bấm ra ngoài', 'Click', 'After:\n– Chưa đổi gì → đóng; đã đổi → hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
    ],
})

# 2.5 Xóa ---------------------------------------------------------------------------
FR.append({
    'ten': 'Xóa vị trí', 'uc': 'uc_xoa',
    'qtc': 'Quy tắc Xóa, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xóa vị trí'],
        ['Mô tả', 'Xóa hẳn vị trí đang Hoạt động và chưa được dùng ở bất kỳ đâu (tồn kho, chứng từ kho, kiểm kê, điều chuyển, vị trí tách ghép / xuất thẳng của kho) (BR-08).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Vị trí đang Hoạt động, chưa được dùng ở đâu.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Xóa ở cột Hành động.\n2. Hệ thống hiện hộp "Xác nhận xóa": "Bạn có chắc muốn xóa vị trí \'<Tên vị trí>\'?"\n3. Người dùng bấm Xóa.\n4. Hệ thống ghi nhận Xóa trong lịch sử, xóa hẳn vị trí.\n5. Tải lại danh sách, báo "Xóa thành công."'],
        ['Dòng sự kiện phụ', '• Bấm Hủy → đóng hộp, không thay đổi.\n• Vị trí vừa bị khóa → "Không thể xóa vị trí đang ở trạng thái khóa. Hãy mở khóa trước."\n• Vị trí vừa được dùng → "Không thể xóa do dữ liệu đang được sử dụng."\n• Vị trí vừa bị người khác xóa → "Dữ liệu đã thay đổi, vui lòng tải lại".'],
    ],
    'menu_them': ' => Xóa {icon:btn_xoa}',
    'ghi_chu_layout': POPUP % 'Xác nhận xóa',
    'anh': [('13_delete', 'Hộp xác nhận xóa vị trí')],
    'ui': ui(UI4, [
        ['Nút Xóa (cột Hành động)', 'Button', 'Biểu tượng thùng rác; chỉ hiện khi vị trí Hoạt động, chưa được dùng ở đâu và người dùng có quyền.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận xóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn xóa vị trí \'<Tên vị trí>\'?"'],
        ['Nút Xóa', 'Button', 'Xác nhận xóa.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không xóa.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Xóa ở cột Hành động', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên vị trí.'],
        ['Bấm Xóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền, vị trí thuộc phạm vi.\nDuring:\n– Vị trí phải đang Hoạt động và chưa được dùng ở đâu.\n' + TRUOC_LUU + '\nAfter:\n– Ghi nhận Xóa trong lịch sử, xóa hẳn vị trí.\n– Tải lại danh sách, báo "Xóa thành công."'],
        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.6 Khóa / Mở khóa -----------------------------------------------------------
FR.append({
    'ten': 'Khóa / Mở khóa vị trí', 'uc': 'uc_khoa',
    'qtc': 'Quy tắc Khóa/Mở khóa, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Khóa / Mở khóa vị trí'],
        ['Mô tả', 'Đổi trạng thái vị trí giữa Hoạt động và Khóa. Vị trí là cấp cuối của cây kho nên khóa được cả khi đang có tồn (BR-06); mở khóa khi cấp cha đang Hoạt động (BR-07).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Khóa: vị trí Hoạt động. Mở khóa: vị trí đang Khóa, khoang (vị trí Tự do: kho) đang Hoạt động.'],
        ['Dòng sự kiện chính', '1. Người dùng chọn Khóa (hoặc Mở khóa) ở cột Hành động.\n2. Hệ thống hiện hộp "Xác nhận khóa" / "Xác nhận mở khóa" kèm tên vị trí.\n3. Người dùng bấm Khóa / Mở khóa.\n4. Hệ thống đổi trạng thái, ghi nhận Khóa / Mở khóa trong lịch sử.\n5. Tải lại danh sách, báo "Khóa thành công." / "Mở khóa thành công."'],
        ['Dòng sự kiện phụ', '• Bấm Hủy → không thay đổi.\n• Cấp cha đang Khóa: không có nút Mở khóa; nếu cấp cha vừa bị khóa → "Không thể mở khóa vị trí khi danh mục cha đang bị khóa."\n• Vị trí đã bị người khác đổi trạng thái → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n• Sau khi Khóa: nút Sửa, Xóa ẩn; sau khi Mở khóa: nút Sửa hiện lại.'],
    ],
    'menu_them': ' => Khóa {icon:btn_khoa_row} / Mở khóa {icon:btn_mokhoa_row}',
    'ghi_chu_layout': POPUP % 'Xác nhận khóa / Xác nhận mở khóa',
    'anh': [('14_lock', 'Hộp xác nhận khóa vị trí'), ('15_unlock', 'Hộp xác nhận mở khóa vị trí')],
    'ui': ui(UI4, [
        ['Nút Khóa (cột Hành động)', 'Button', '- Biểu tượng ổ khóa; hiện khi vị trí Hoạt động, có quyền.\n- Dòng có nút Xóa thì Khóa nằm trong nút ba chấm "Hành động khác".'],
        ['Nút Mở khóa (cột Hành động)', 'Button', 'Biểu tượng ổ khóa mở; hiện khi vị trí đang Khóa, cấp cha đang Hoạt động, có quyền.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận khóa" hoặc "Xác nhận mở khóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn khóa vị trí \'<Tên vị trí>\'?" / "Bạn có chắc muốn mở khóa vị trí \'<Tên vị trí>\'?"'],
        ['Nút Khóa / Mở khóa', 'Button', 'Xác nhận đổi trạng thái.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không thay đổi.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Chọn Khóa / Mở khóa', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên vị trí.'],
        ['Bấm Khóa / Mở khóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền, vị trí thuộc phạm vi.\nDuring:\n– Vị trí đã ở trạng thái đích → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n– Mở khóa mà cấp cha đang Khóa → "Không thể mở khóa vị trí khi danh mục cha đang bị khóa."\n' + TRUOC_LUU + '\nAfter:\n– Đổi trạng thái, ghi nhận Khóa / Mở khóa trong lịch sử, tải lại danh sách, báo thành công.'],
        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.7 Lịch sử --------------------------------------------------------------------
FR.append({
    'ten': 'Xem lịch sử thay đổi',
    'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem lịch sử thay đổi vị trí'],
        ['Mô tả', 'Liệt kê các lần thao tác trên một vị trí (Tạo mới, Thay đổi thông tin, Khóa, Mở khóa, Xóa), mới nhất ở trên, kèm người thực hiện, thời điểm, giá trị cũ → mới.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Lịch sử ở cột Hành động (hoặc Xem lịch sử trong cửa sổ Xem chi tiết).\n2. Hệ thống mở cửa sổ "Lịch sử thay đổi: <Tên vị trí>" và liệt kê các mốc.'],
        ['Dòng sự kiện phụ', '• Lọc theo Loại hành động, Người thực hiện, Từ ngày / Đến ngày bằng nút Bộ lọc trong cửa sổ.\n• Các trường được ghi: Mã vị trí, Tên vị trí, Kho, Khoang (bằng tên), Mô tả, Trạng thái.\n• Vị trí sinh tự động từ màn Dãy / Kho vật lý cũng có mốc Tạo mới.'],
    ],
    'menu_them': ' => Lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': POPUP % 'Lịch sử thay đổi',
    'anh': [('16_history', 'Cửa sổ Lịch sử thay đổi của vị trí')],
    'ui': ui(UI6, [
        ['Nút Lịch sử (cột Hành động)', 'Button', 'Enable', 'Hiển thị', 'Luôn có ở mọi dòng (kể cả vị trí Khóa); dòng có 4 nút thì nằm trong nút ba chấm.'],
        ['Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Lịch sử thay đổi: <Tên vị trí>', ''],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Mở các ô lọc Loại hành động, Người thực hiện, Từ ngày, Đến ngày.'],
        ['Danh sách mốc', 'Table/Grid', 'Read-only', 'Theo dữ liệu', '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, loại hành động, "Người thực hiện: Họ tên — Phòng ban".\n- Dòng thay đổi: "<Trường>: giá trị cũ → giá trị mới".\n- Chưa có dữ liệu: "Chưa có lịch sử thao tác nào."'],
        ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lịch sử', 'Click', 'After:\n– Tải lịch sử của vị trí, mới nhất trên cùng.'],
        ['Chọn điều kiện ở Bộ lọc', 'Change', 'After:\n– Lọc lại các mốc; không có mốc khớp → "Không có lịch sử phù hợp bộ lọc."'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.8 Import ---------------------------------------------------------------------
FR.append({
    'ten': 'Import vị trí từ file Excel', 'uc': 'uc_import',
    'qtc': 'Quy tắc Import file, Validate dữ liệu, Thông báo.',
    'gioi_thieu': [
        ['Tên chức năng', 'Import vị trí từ file Excel'],
        ['Mô tả', 'Tạo nhiều vị trí từ file Excel theo file mẫu. Kho, nhà kho, dãy, khoang nhập bằng MÃ; mỗi dòng được kiểm tra và ghi như khi Tạo mới (BR-09).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Import Excel, hệ thống mở cửa sổ "Import vị trí".\n2. Bấm Tải file mẫu (Mau_import_vi_tri.xlsx), điền dữ liệu.\n3. Bấm Chọn file Excel, chọn file, bấm Load lên bảng: dữ liệu hiện ở bảng xem trước, ô Tổng = số dòng.\n4. Bấm Validate: hệ thống kiểm tra từng dòng (chưa ghi dữ liệu), hiện Tổng / Hợp lệ / Lỗi; dòng lỗi tô đỏ kèm lý do, dòng hợp lệ bị khóa.\n5. Sửa dòng lỗi rồi Validate lại, hoặc bấm Bỏ dòng lỗi.\n6. Khi không còn dòng lỗi, bấm Import: hệ thống ghi từng dòng, ghi nhận Tạo mới trong lịch sử, báo "Import thành công N vị trí.", tải lại danh sách.'],
        ['Dòng sự kiện phụ', '• File quá 500 dòng dữ liệu → "File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần."\n• Dòng vừa bị trùng với vị trí người khác tạo trong lúc Import → bị bỏ qua, bảng kết quả "Import xong: a dòng thành công, b dòng lỗi bị bỏ qua" (nút Sao chép).\n• Bấm Xoá trạng thái validate để sửa lại cả dòng đã khóa.\n• Bấm Làm mới để làm lại từ đầu; Đóng để thoát.'],
    ],
    'menu_them': ' => Import Excel {icon:btn_import}',
    'ghi_chu_layout': POPUP % 'Import vị trí',
    'anh': [('21_import_open', 'Cửa sổ Import vị trí khi vừa mở'), ('22_import_loaded', 'Dữ liệu sau khi Load lên bảng'),
            ('23_import_validated', 'Kết quả Validate — dòng lỗi nêu rõ lý do')],
    'ui': ui(UI7I, [
        ['Nút Chọn file Excel', 'Button', 'Enable', '–', '–', 'Chọn file .xlsx, hiện tên file bên cạnh.'],
        ['Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Tải Mau_import_vi_tri.xlsx: dòng 1 tên cột (cột bắt buộc có *), dòng 2 hướng dẫn, 2 dòng dữ liệu mẫu (1 Thuộc khoang, 1 Tự do).'],
        ['Nút Load lên bảng', 'Button', 'Enable / Disable', '–', 'Disable', 'Bấm được khi đã chọn file; đọc file lên bảng xem trước.'],
        ['Nút Validate', 'Button', 'Enable / Disable', '–', 'Disable', 'Bấm được khi bảng có dữ liệu; kiểm tra từng dòng, chưa ghi dữ liệu.'],
        ['Nút Import', 'Button', 'Enable / Disable', '–', 'Disable', 'Chỉ bấm được khi đã Validate, còn ≥ 1 dòng hợp lệ và KHÔNG còn dòng lỗi.'],
        ['Ô Tổng / Hợp lệ / Lỗi', 'Label', 'Read-only', '–', 'Tổng: 0', 'Tổng hiện sau Load; Hợp lệ, Lỗi hiện sau Validate.'],
        ['Cột Loại vị trí *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Chọn Thuộc khoang / Tự do; giá trị khác: "Loại vị trí: Chỉ nhận Thuộc khoang hoặc Tự do".'],
        ['Cột Mã kho *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Mã ở màn Kho vật lý, trong phạm vi người dùng.'],
        ['Cột Mã nhà kho, Mã dãy, Mã khoang', 'Table/Grid', 'Enable', 'Có khi Thuộc khoang', 'Theo file', '- Bắt buộc khi Loại vị trí = Thuộc khoang; mã phải thuộc cấp trên ở cùng dòng.\n- Không thấy: \'Không tồn tại nhà kho có mã "<mã>" trong kho "<mã kho>"\'.'],
        ['Cột Mã vị trí *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Chữ không dấu, số, dấu - và _, tối đa 50 ký tự, không trùng trong kho và trong file.'],
        ['Cột Tên vị trí *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Tối đa 255 ký tự, không trùng trong khoang / trong kho với vị trí tự do.'],
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
        ['Bấm Validate', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho".\nDuring:\n– Mỗi dòng kiểm như Tạo mới; tra mã kho → nhà kho → dãy → khoang theo đúng cấp; khoang / kho đã khóa; trùng mã vị trí trong file ("Bị trùng trong file").\nAfter:\n– Hiện Tổng / Hợp lệ / Lỗi, toast "Validate xong: X hợp lệ, Y không hợp lệ" (hoặc "Validate thành công"); dòng lỗi tô đỏ kèm lý do theo thứ tự cột, dòng hợp lệ bị khóa.'],
        ['Bấm Import', 'Click', 'Before:\n– Đã Validate, không còn dòng lỗi.\nDuring:\n– Hệ thống kiểm lại từng dòng ngay trước khi ghi.\n' + TRUOC_LUU + '\nAfter:\n– Ghi từng dòng như Tạo mới, ghi nhận Tạo mới trong lịch sử.\n– Báo "Import thành công N vị trí.", đóng cửa sổ, tải lại danh sách; có dòng bị bỏ qua thì hiện bảng kết quả.'],
        ['Bấm Bỏ dòng lỗi / Xoá trạng thái validate', 'Click', 'After:\n– Bỏ dòng lỗi khỏi bảng / mở khóa các dòng để sửa.'],
        ['Bấm Đóng / Làm mới', 'Click', 'After:\n– Đóng cửa sổ / xoá dữ liệu đang xem để làm lại.'],
    ],
})

# 2.9 Xuất Excel -------------------------------------------------------------------
FR.append({
    'ten': 'Xuất danh sách ra Excel', 'uc': 'uc_xuat',
    'qtc': 'Quy tắc Excel, Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách vị trí ra Excel'],
        ['Mô tả', 'Xuất toàn bộ vị trí khớp bộ lọc đang áp dụng (mọi trang) ra file Excel, người dùng chọn trường và thứ tự cột (BR-10).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng lọc danh sách (nếu cần), bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất file", tích sẵn các cột đang hiện trên bảng.\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự rồi bấm Xuất file.\n4. Hệ thống tải file danh_sach_vi_tri.xlsx, báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Kết quả rỗng vẫn xuất file (tiêu đề + tên cột).\n• Ô Ngày tạo đang sai (Từ > Đến) → báo lỗi, không xuất.\n• Lỗi hệ thống → "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': POPUP % 'Chọn trường xuất file',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất file')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '"Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file."'],
        ['Danh sách trường', 'Table/Grid', 'Enable', 'Tích theo cột đang hiện', '13 trường: Mã vị trí, Tên vị trí, Loại vị trí, Kho, Nhà kho, Dãy, Khoang, Mô tả, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. Mỗi trường có ô tích và biểu tượng ☰ kéo đổi vị trí.'],
        ['Nút Chọn tất cả', 'Button', 'Enable', '–', 'Tích mọi trường.'],
        ['Nút Bỏ chọn hết', 'Button', 'Enable', '–', 'Bỏ tích mọi trường.'],
        ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn x/13 trường', ''],
        ['Nút Xuất file', 'Button', 'Enable / Disable', 'Enable', 'Tải file; không bấm được khi không còn trường nào được chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ, không xuất.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ, tích sẵn theo cột đang hiện.'],
        ['Bấm Xuất file', 'Click', 'During:\n– Ô Ngày tạo sai → báo "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", không xuất.\n' + TRUOC_LUU + '\nAfter:\n– Tải file danh_sach_vi_tri.xlsx: tiêu đề "Danh sách vị trí", cột theo thứ tự đã chọn, mọi dòng khớp bộ lọc; báo "Xuất Excel thành công".'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.10 Xem chi tiết ----------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết vị trí', 'uc': 'uc_xem',
    'qtc': 'Màn Xem chi tiết, Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết vị trí'],
        ['Mô tả', 'Xem toàn bộ thông tin một vị trí ở chế độ chỉ đọc, kèm khối Lịch sử.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm vào Mã vị trí trên bảng.\n2. Hệ thống mở cửa sổ "Xem chi tiết vị trí", mọi ô chỉ đọc.\n3. Bấm Xem lịch sử để mở khối Lịch sử ngay trong cửa sổ.'],
        ['Dòng sự kiện phụ', '• Vị trí vừa bị xoá / ngoài phạm vi → báo "Dữ liệu đã thay đổi, vui lòng tải lại", không mở cửa sổ.\n• Vị trí Tự do: không có 3 ô Nhà kho, Dãy, Khoang.'],
    ],
    'menu_them': ' => Bấm Mã vị trí',
    'ghi_chu_layout': POPUP % 'Xem chi tiết vị trí',
    'anh': [('17_detail', 'Cửa sổ Xem chi tiết vị trí ở chế độ chỉ đọc'),
            ('17b_detail_history', 'Khối Lịch sử trong cửa sổ Xem chi tiết')],
    'ui': ui(UI6, [
        ['Loại vị trí, Kho, Nhà kho, Dãy, Khoang', 'Dropdown', 'Read-only', 'Dữ liệu hiện tại', 'Dạng "Mã - Tên"; vị trí Tự do chỉ có Loại vị trí và Kho.'],
        ['Mã vị trí, Tên vị trí', 'Textbox', 'Read-only', 'Dữ liệu hiện tại', 'Không có dấu (*).'],
        ['Trạng thái', 'Dropdown', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Mô tả', 'Textarea', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Khối Lịch sử', 'Table/Grid', 'Enable', 'Thu gọn', '- Nút Xem lịch sử mở khối, hiện số mốc.\n- Nút Làm mới tải lại, Thu gọn đóng khối, Bộ lọc lọc mốc như mục 2.7.'],
        ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ. Không có nút Lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Mã vị trí', 'Click', 'After:\n– Tải dữ liệu, mở cửa sổ chỉ đọc.'],
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
        ['Dòng sự kiện phụ', '• Cột STT, Mã vị trí, Hành động là cột khóa: không bỏ tích, không kéo được.\n• Bấm Đóng → bỏ các thay đổi vừa chỉnh.'],
    ],
    'menu_them': ' => Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': POPUP % 'Tuỳ chỉnh cột',
    'anh': [('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột — STT, Mã vị trí, Hành động bị khóa')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '"Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng."'],
        ['Danh sách cột', 'Table/Grid', 'Enable', 'Theo cấu hình đã lưu', '15 cột theo thứ tự trên bảng. Mặc định ẩn: Loại vị trí, Mô tả.'],
        ['Cột khóa', 'Table/Grid', 'Disable', 'Luôn tích', 'STT, Mã vị trí, Hành động: ô tích xám kèm biểu tượng khóa, không ẩn và không đổi vị trí được.'],
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
    'menu': [('Kho', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Vị trí', 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu chức năng.',
        'Làm rõ phạm vi dữ liệu theo công ty, 2 loại vị trí (Thuộc khoang / Tự do), ràng buộc trùng Mã vị trí trong kho và Tên vị trí trong khoang, điều kiện Khóa / Mở khóa theo cấp cha và điều kiện Xóa (vị trí chưa được dùng ở đâu).',
    ],
    'thuat_ngu': [
        ['Vị trí', 'Cấp cuối của cây kho: Kho vật lý → Nhà kho → Dãy → Khoang → Vị trí; nơi xếp hàng cụ thể trong kho.'],
        ['Vị trí Thuộc khoang', 'Vị trí gắn với một khoang; nhà kho, dãy, kho suy theo khoang.'],
        ['Vị trí Tự do', 'Vị trí gắn thẳng vào kho, không qua nhà kho / dãy / khoang (ví dụ vị trí tách ghép hàng).'],
        ['Vị trí tách ghép hàng', 'Vị trí Tự do mã "<Mã kho>-TACH-GHEP" hệ thống tự sinh khi tạo kho vật lý.'],
        ['Tồn', 'Số lượng hàng đang có tại vị trí.'],
        ['Hoạt động', 'Trạng thái vị trí dùng được ở các màn nghiệp vụ.'],
        ['Khóa', 'Vị trí vẫn nằm trong danh mục, xem được lịch sử nhưng không còn chọn được ở các màn nghiệp vụ.'],
        ['Super admin', 'Tài khoản quản trị cao nhất, xem được vị trí của mọi công ty.'],
    ],
    'quyen_truoc': ['Màn hình dùng một quyền duy nhất "Quản lý kho" (nhóm Danh mục kho) cho cả xem lẫn thao tác; quyền này dùng chung cho 7 màn Danh mục của phân hệ Kho. Quyền được gán vào vai trò theo công ty.'],
    'quyen_rows': [['Quản lý kho', 'Xem danh sách, tìm kiếm, xem chi tiết, lịch sử, tùy chỉnh cột, xuất Excel; Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Import Excel.']],
    'ma_tran': [['Chức năng', 'Quản lý kho', 'Không có quyền']] + [[f, 'Có', 'Không'] for f in [
        'FR-01 Xem danh sách vị trí', 'FR-02 Tìm kiếm và lọc', 'FR-03 Thêm mới vị trí', 'FR-04 Chỉnh sửa vị trí',
        'FR-05 Xóa vị trí', 'FR-06 Khóa / Mở khóa vị trí', 'FR-07 Xem lịch sử thay đổi',
        'FR-08 Import vị trí từ file Excel', 'FR-09 Xuất danh sách ra Excel', 'FR-10 Xem chi tiết vị trí',
        'FR-11 Tùy chỉnh cột hiển thị']],
    'ma_tran_widths': [2.6, 1.2, 1.2],
    'quyen_sau': ['Phạm vi dữ liệu: người dùng thường chỉ thấy và thao tác vị trí thuộc kho của công ty mình; Super admin thấy vị trí mọi công ty và có thêm ô lọc Công ty (BR-01).'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Phạm vi dữ liệu theo công ty', [
            '– Người dùng thường chỉ thấy, xem, sửa, khóa, xóa, xuất vị trí thuộc kho có công ty sở hữu = công ty đang làm việc của mình.',
            '– Super admin thấy vị trí mọi công ty, có thêm ô lọc Công ty.',
            '– Không xác định được công ty của người dùng → không thấy vị trí nào.',
            '– Thao tác trên vị trí ngoài phạm vi bị từ chối như dữ liệu không tồn tại; tạo vị trí vào khoang / kho ngoài phạm vi báo "Khoang không tồn tại" / "Kho không tồn tại".'],
         ['Xem danh sách', 'Xuất Excel', 'Thêm mới', 'Chỉnh sửa', 'Xóa', 'Khóa / Mở khóa']),
        ('BR-02', 'Mã vị trí', [
            '– Bắt buộc, 1–50 ký tự, chỉ gồm chữ không dấu, số, dấu - và _; cắt khoảng trắng đầu / cuối.',
            '– Duy nhất trong CÙNG một kho (mọi trạng thái); kho khác được trùng. Trùng: "Đã tồn tại trong kho này".',
            '– Giữ nguyên chữ hoa / thường người dùng nhập, không thêm tiền tố.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-03', 'Tên vị trí', [
            '– Bắt buộc, tối đa 255 ký tự.',
            '– Vị trí Thuộc khoang: không trùng tên trong cùng khoang. Vị trí Tự do: không trùng tên với vị trí Tự do khác trong cùng kho (mọi trạng thái). Trùng: "Đã tồn tại".'],
         ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-04', 'Loại vị trí và cấp cha', [
            '– Thuộc khoang: bắt buộc chọn đủ Kho → Nhà kho → Dãy → Khoang; chỉ khoang được lưu, kho của vị trí lấy theo khoang (không theo ô Kho).',
            '– Tự do: chỉ bắt buộc Kho.',
            '– Ô chọn chỉ liệt kê kho / nhà kho / dãy / khoang đang Hoạt động trong phạm vi; khoang (hoặc cấp trên của nó) / kho vừa bị khóa → báo đỏ, không lưu.',
            '– Sau khi tạo không đổi được Loại vị trí, Kho, Khoang.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-05', 'Vị trí sinh tự động', [
            '– Tạo dãy ở màn Dãy: hệ thống sinh khoang và vị trí "Tầng 1"… theo số lượng khai báo, trạng thái Hoạt động.',
            '– Tạo kho ở màn Kho vật lý: hệ thống sinh vị trí Tự do "<Mã kho>-TACH-GHEP", tên "Vị trí tách ghép hàng".',
            '– Các vị trí này quản lý ở màn Vị trí như vị trí tạo tay (có lịch sử Tạo mới).'], ['Xem danh sách']),
        ('BR-06', 'Điều kiện Khóa', [
            '– Khóa được mọi vị trí đang Hoạt động, kể cả đang có tồn (vị trí là cấp cuối, khóa không làm mất tồn).',
            '– Đổi Trạng thái sang Khóa trong cửa sổ Sửa = Khóa.',
            '– Vị trí đang Khóa: ẩn Sửa, Xóa; không còn chọn được ở các màn nghiệp vụ.',
            '– Khoang chỉ khóa được khi không còn vị trí ĐANG HOẠT ĐỘNG trong khoang.'], ['Khóa / Mở khóa', 'Chỉnh sửa']),
        ('BR-07', 'Điều kiện Mở khóa', [
            '– Vị trí Thuộc khoang: mở khóa được khi khoang đang Hoạt động.',
            '– Vị trí Tự do: mở khóa được khi kho đang Hoạt động.',
            '– Không đủ điều kiện thì ẩn nút Mở khóa; cấp cha vừa bị khóa → "Không thể mở khóa vị trí khi danh mục cha đang bị khóa."'],
         ['Khóa / Mở khóa']),
        ('BR-08', 'Điều kiện Xóa', [
            '– Chỉ xóa vị trí đang Hoạt động và CHƯA được dùng ở bất kỳ đâu: tồn theo vị trí, tồn đầu kỳ, kiểm kê, phiếu nhập / xuất / nhập lại / xuất lại, điều chỉnh kiểm kê, điều chuyển vị trí, điều chuyển kho; không phải vị trí tách ghép / vị trí xuất thẳng của kho.',
            '– Xóa là xóa hẳn; vị trí đã dùng thì dùng Khóa.'], ['Xóa']),
        ('BR-09', 'Import', [
            '– Mỗi dòng kiểm và ghi như Tạo mới (BR-02 → BR-04); kho, nhà kho, dãy, khoang nhập bằng mã, tra theo đúng cấp trên ở cùng dòng.',
            '– Trùng Mã vị trí trong cùng kho giữa các dòng của file → "Bị trùng trong file".',
            '– Tối đa 500 dòng dữ liệu mỗi lần; chỉ Import khi đã Validate và không còn dòng lỗi.'], ['Import']),
        ('BR-10', 'Xuất Excel', ['– Xuất mọi dòng khớp bộ lọc đang áp dụng (không chỉ trang đang xem), cột theo thứ tự người dùng chọn; tên file danh_sach_vi_tri.xlsx.'], ['Xuất Excel']),
        ('BR-11', 'Bộ lọc', [
            '– Ngày tạo Từ lớn hơn Đến → báo đỏ "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", xoá bảng, không tải dữ liệu và không xuất Excel.',
            '– Ô Kho mặc định chỉ có kho đang Hoạt động; bật biểu tượng ổ khóa để lọc cả vị trí của kho đã khóa. Bộ lọc đã lưu trỏ tới kho đã khóa vẫn hiện đúng tên.'],
         ['Tìm kiếm và lọc', 'Xuất Excel']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây chọn, lọc, hiển thị hoặc lưu dữ liệu Vị trí; vị trí đang Khóa không còn chọn được ở các ô chọn vị trí.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng có quyền "Quản lý kho"',
    'mains': [('FR-01', 'Xem danh sách vị trí', 'view'), ('FR-03', 'Thêm mới vị trí', 'crud'),
              ('FR-04', 'Chỉnh sửa vị trí', 'crud'), ('FR-05', 'Xóa vị trí', 'action'),
              ('FR-06', 'Khóa / Mở khóa vị trí', 'action'), ('FR-08', 'Import vị trí từ file Excel', 'io'),
              ('FR-09', 'Xuất danh sách vị trí ra Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc vị trí', 'view'), ('FR-10', 'Xem chi tiết vị trí', 'view'),
             ('FR-11', 'Tùy chỉnh cột hiển thị', 'view'), ('FR-07', 'Xem lịch sử thay đổi', 'view')],
    'rieng': [('FR-03', 'Thêm mới vị trí', 'crud', 'uc_them'), ('FR-04', 'Chỉnh sửa vị trí', 'crud', 'uc_sua'),
              ('FR-05', 'Xóa vị trí', 'action', 'uc_xoa'), ('FR-06', 'Khóa / Mở khóa vị trí', 'action', 'uc_khoa'),
              ('FR-08', 'Import vị trí từ file Excel', 'io', 'uc_import'),
              ('FR-09', 'Xuất danh sách vị trí ra Excel', 'io', 'uc_xuat'), ('FR-10', 'Xem chi tiết vị trí', 'view', 'uc_xem')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)

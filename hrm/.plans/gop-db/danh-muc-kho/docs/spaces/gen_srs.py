# -*- coding: utf-8 -*-
"""SRS - Danh mục khoang (form Danh mục quốc gia, TPE duyệt) — chép khuôn màn mẫu docs/warehouses/gen_srs.py.

Nguồn (code HRM hiện tại, nhánh có code kho):
  FE hrm-client/pages/warehouse/spaces/{index.vue, AddSpaceModal.vue}, utils/mixins/{vehicleCatalogScreenMixin,
     vehicleCatalogModalMixin, warehouseCatalogModalMixin, warehouseCatalogImportMixin, createdRangeFilterMixin,
     warehouseLockedFilterMixin}.js, components/warehouse-catalog/LockableFilterSelect.vue,
     utils/warehouse-catalog-import.js, components/subsystem-menu/warehouse.js
  BE Modules/MasterData: Entities/Warehouse/Space.php, Http/Controllers/V1/Warehouse/{SpaceController,
     WarehouseTreeCatalogController}.php, ProductClassification/{BaseCatalogController, BaseCatalogRequest}.php,
     Http/Requests/Warehouse/SpaceRequest.php, Services/Warehouse/{SpaceService, RowService, WarehouseCatalogScope,
     Concerns/ImportsWarehouseCatalogRows, Concerns/SearchesCodeNameOnly}.php, Transformers/Warehouse/SpaceResource.php;
     app/Services/CatalogHistoryService.php, app/ExcelExport/ExportColumnRegistry.php
  Phần 5: dò code FE/BE + menu (02/11/2026).
Chạy:  python gen_srs.py          (dựng + Word cập nhật mục lục + PDF out/ + tự kiểm)
       python gen_srs.py --no-word (chỉ dựng .docx)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import _lib_win as L  # noqa: E402

TEN = 'Danh mục khoang'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q = 'Người dùng có quyền thực hiện chức năng (quyền "Quản lý kho")'
DK = '1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền "Quản lý kho".'
TRUOC_LUU = '– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung SRS_Các quy tắc chung_VN_1.0, không thực hiện bước After.'
POPUP = 'Modal %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'
KHOA_CON = 'Không thể khóa khoang khi vẫn còn danh mục con đang hoạt động.'

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
    ('Kho', 'Dãy (tạo dãy tự sinh khoang; khóa dãy khi khoang đã khóa hết)', 'Kho => Danh mục'),
    ('Kho', 'Vị trí (ô chọn Khoang của vị trí thuộc khoang)', 'Kho => Danh mục'),
    ('Kho', 'Khai báo tồn kho đầu kỳ (cột Khoang)', 'Kho => Tồn kho đầu kỳ'),
    ('Kho', 'Phiếu nhập kho (cột Khoang của vị trí nhập)', 'Kho => Nhập kho'),
    ('Kho', 'Phiếu điều chuyển vị trí (lọc vị trí theo Khoang)', 'Kho => Điều chuyển'),
    ('Kho', 'Kiểm kê theo vị trí (lọc và chọn phạm vi theo Khoang)', 'Kho => Kiểm kho => Theo vị trí'),
    ('Kho', 'Thẻ kho (chọn phạm vi theo Khoang)', 'Kho => Báo cáo kho'),
    ('Kho', 'Báo cáo tồn kho theo vị trí (chọn phạm vi theo Khoang)', 'Kho => Báo cáo kho'),
    ('Kho', 'Tổng hợp xuất nhập tồn (chọn phạm vi theo Khoang)', 'Kho => Báo cáo kho'),
    ('Tài chính', 'Phiếu nhập kho (cột Khoang của vị trí nhập)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
    ('Tài chính', 'Kế hoạch kiểm kê theo vị trí (lọc và chọn phạm vi theo Khoang)', 'Tài chính => Kiểm kê'),
]

# ------------------------------------------------------------------ dữ liệu SRS
FR = []

# 2.1 Xem danh sách -------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách khoang',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang, Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách khoang'],
        ['Mô tả', 'Hiển thị các khoang thuộc kho trong phạm vi dữ liệu của người dùng (cả Hoạt động lẫn Khóa), kèm dãy, nhà kho, kho chứa khoang; có phân trang, sắp xếp và các nút thao tác theo từng dòng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn Danh mục khoang theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), khoang tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Người dùng thường chỉ thấy khoang thuộc kho của công ty mình; Super admin thấy khoang mọi công ty (BR-01).\n• Không có khoang khớp → bảng hiện "Không có dữ liệu phù hợp."\n• Khoang đã bị xóa không còn hiển thị (BR-08).'],
    ],
    'anh': [('01_list', 'Màn Danh mục khoang lúc mới truy cập')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Danh sách khoang', 'Tiêu đề khối danh sách và tiêu đề trang.'],
        ['Nút Tạo mới', 'Button', 'Enable / Ẩn', 'Hiển thị', '- Mở cửa sổ "Tạo mới khoang" (mục 2.3).\n- Ẩn khi thiếu quyền "Quản lý kho".'],
        ['Nút Import Excel', 'Button', 'Enable / Ẩn', 'Hiển thị', '- Mở cửa sổ "Import khoang" (mục 2.8).\n- Ẩn khi thiếu quyền.'],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất file" (mục 2.9).'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.11).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa, không ẩn được.'],
        ['Cột Mã khoang', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sắp xếp được.\n- Chữ dạng liên kết: bấm vào mở cửa sổ "Xem chi tiết khoang" (mục 2.10).\n- Cột khóa, không ẩn được.'],
        ['Cột Tên khoang', 'Table/Grid', 'Read-only', 'Hiển thị', 'Sắp xếp được. Dài thì xuống tối đa 2 dòng, rê chuột xem đủ.'],
        ['Cột Dãy', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên dãy chứa khoang.'],
        ['Cột Nhà kho', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên nhà kho chứa dãy.'],
        ['Cột Kho', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên kho vật lý chứa nhà kho.'],
        ['Cột Số vị trí', 'Table/Grid', 'Read-only', 'Ẩn', 'Số vị trí thuộc khoang (đếm cả vị trí đã Khóa); khoang chưa có vị trí thì để trống. Mặc định ẩn, căn phải.'],
        ['Cột Mô tả', 'Table/Grid', 'Read-only', 'Ẩn', 'Mặc định ẩn.'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng "Họ tên - Mã phòng ban".'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Người cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng "Họ tên - Mã phòng ban".'],
        ['Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Trạng thái', 'Table/Grid', 'Read-only', 'Hiển thị', '- "Hoạt động" nền xanh.\n- "Khóa" nền đỏ.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sửa: khoang Hoạt động, có quyền.\n- Xóa: khoang Hoạt động, chưa có vị trí và chưa được chọn trong kế hoạch kiểm kê, có quyền (BR-08).\n- Khóa: khoang Hoạt động và không còn vị trí đang hoạt động (BR-07); Mở khóa: khoang đang Khóa và dãy chứa nó đang Hoạt động.\n- Lịch sử: luôn có.\n- Có 4 nút thì hiện 2 nút đầu, các nút còn lại nằm trong nút ba chấm "Hành động khác".\n- Nút không dùng được thì ẩn, không làm mờ. Cột khóa, không ẩn được.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Kiểm tra quyền "Quản lý kho"; thiếu quyền → menu không hiện, mở thẳng màn bị từ chối.\nAfter:\n– Tải trang 1 theo phạm vi công ty (BR-01), khoang tạo gần nhất trên cùng.'],
        ['Bấm tiêu đề cột Mã khoang / Tên khoang / Ngày tạo / Ngày cập nhật', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại từ trang 1.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp, tải lại dữ liệu; đổi số dòng thì quay về trang 1.'],
        ['Bấm Mã khoang', 'Click', 'After:\n– Mở cửa sổ "Xem chi tiết khoang" (mục 2.10).'],
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách khoang'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao: Công ty (chỉ Super admin), Kho, Nhà kho, Dãy, Trạng thái, Người tạo, Ngày tạo.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn Danh mục khoang.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô tìm nhanh chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Lọc dây chuyền Công ty → Kho → Nhà kho → Dãy: đổi cấp trên thì cấp dưới không còn thuộc nó tự về trống (BR-09).\n• Ô Kho / Nhà kho / Dãy mặc định chỉ liệt kê mục đang Hoạt động; bấm biểu tượng ổ khóa trên nhãn ô để hiện cả mục đã khóa.\n• Ngày tạo "Từ" lớn hơn "Đến" → báo đỏ dưới ô, xoá bảng, không tải dữ liệu (BR-11).\n• Bấm Làm mới → xoá mọi điều kiện và tải lại danh sách.\n• Hệ thống ghi nhớ bộ lọc 10 phút khi rời màn rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực tìm kiếm và lọc (đã mở Tìm kiếm nâng cao)')],
    'ui': ui(['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả'], [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', '- Placeholder "Tìm theo mã, tên khoang".\n- Tìm gần đúng theo Mã khoang, Tên khoang, không phân biệt hoa thường.'],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Áp dụng từ khóa và các ô lọc.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá mọi điều kiện lọc và tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực các ô lọc (khi mở, nút đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" chọn ô lọc nào được hiển thị (áp dụng quy tắc chung).'],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Trống', '- Chỉ hiện với Super admin.\n- Lọc khoang theo công ty sở hữu kho; đổi công ty thì Kho / Nhà kho / Dãy không thuộc công ty đó tự về trống.\n- Biểu tượng ổ khóa trên nhãn: hiện cả công ty đã khóa.'],
        ['Ô Kho', 'Dropdown', 'Enable', 'Kho trong phạm vi, dạng "Mã - Tên"', 'Trống', '- Lọc khoang thuộc kho được chọn.\n- Biểu tượng ổ khóa trên nhãn: bật thì hiện cả kho đã khóa (gợi ý "Hiện cả kho đã khoá").'],
        ['Ô Nhà kho', 'Dropdown', 'Enable', 'Nhà kho thuộc kho đã chọn (chưa chọn kho: mọi nhà kho trong phạm vi)', 'Trống', '- Lọc khoang thuộc nhà kho được chọn.\n- Biểu tượng ổ khóa: hiện cả nhà kho đã khóa.'],
        ['Ô Dãy', 'Dropdown', 'Enable', 'Dãy thuộc nhà kho / kho đã chọn', 'Trống', '- Lọc khoang thuộc dãy được chọn.\n- Biểu tượng ổ khóa: hiện cả dãy đã khóa.'],
        ['Ô Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Trống', 'Bỏ trống thì hiện cả hai trạng thái.'],
        ['Ô Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc khoang do người được chọn tạo.'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Một ô chọn khoảng Từ ngày → Đến ngày, tính cả 2 đầu mút.\n- Từ > Đến: báo đỏ "Đến ngày phải lớn hơn hoặc bằng Từ ngày."'],
    ]),
    'ui_widths': [0.45, 1.15, 0.85, 0.8, 1.15, 0.8, 2.6],
    'events': [
        ['Bấm Tìm kiếm / nhấn Enter ở ô tìm nhanh', 'Click', 'After:\n– Áp đồng thời từ khóa và các ô lọc, tải lại bảng từ trang 1.'],
        ['Chọn giá trị ở ô lọc', 'Change', 'During:\n– Đổi Công ty / Kho / Nhà kho: bỏ giá trị cấp dưới không còn thuộc cấp vừa chọn.\n– Ô Ngày tạo: Từ > Đến → báo đỏ dưới ô, toast cùng câu, xoá bảng, không tải dữ liệu.\nAfter:\n– Tải lại bảng từ trang 1.'],
        ['Bấm biểu tượng ổ khóa ở ô Kho / Nhà kho / Dãy', 'Click', 'After:\n– Tải danh sách đủ (cả mục đã khóa) cho ô; bấm lại thì chỉ còn mục đang Hoạt động (giá trị đang lọc vẫn giữ).'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khu vực ô lọc.'],
    ],
})

# 2.3 Thêm mới -------------------------------------------------------------------
LOC = ['Kho', 'Dropdown', 'Enable', 'Kho đang Hoạt động trong phạm vi, dạng "Mã - Tên"', 'Có', 'Trống',
       '- Chỉ để lọc ô Nhà kho, không lưu.\n- Bỏ trống: "Bắt buộc phải nhập".']
FORM_ROWS = [
    LOC,
    ['Nhà kho', 'Dropdown', 'Enable / Disable', 'Nhà kho đang Hoạt động thuộc kho đã chọn', 'Có', 'Trống',
     '- Chỉ để lọc ô Dãy, không lưu; bị khóa đến khi chọn Kho.\n- Đổi Kho thì ô tự về trống nếu nhà kho không thuộc kho mới.\n- Bỏ trống: "Bắt buộc phải nhập".'],
    ['Dãy', 'Dropdown', 'Enable / Disable', 'Dãy đang Hoạt động thuộc nhà kho đã chọn', 'Có', 'Trống',
     '- Dãy chứa khoang (giá trị được lưu); bị khóa đến khi chọn Nhà kho.\n- Bỏ trống: "Bắt buộc phải nhập".\n- Dãy (hoặc nhà kho, kho của nó) vừa bị khóa: "Dãy "<Tên dãy>" đã bị khóa, vui lòng chọn dãy khác".'],
    ['Mã khoang', 'Textbox', 'Enable', '1–50 ký tự: chữ không dấu, số, dấu - và _', 'Có', 'Trống',
     '- Không trùng khoang khác trong CÙNG dãy (BR-02).\n- Sai ký tự: báo đỏ ngay khi gõ "Chỉ gồm chữ không dấu, số, dấu - và _".\n- Quá 50 ký tự: báo đỏ ngay khi gõ.\n- Trùng: "Đã tồn tại trong dãy này".'],
    ['Tên khoang', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     '- Không trùng khoang khác trong CÙNG dãy (BR-03).\n- Ô không cho gõ quá 255 ký tự.\n- Trùng: "Đã tồn tại trong dãy này".'],
    ['Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động', 'Có nút × xoá nhanh; để trống thì lưu là Hoạt động.'],
    ['Mô tả', 'Textarea', 'Enable', '0–500 ký tự', 'Không', 'Trống', 'Quá 500 ký tự: "Nhập tối đa 500 ký tự".'],
]
FR.append({
    'ten': 'Thêm mới khoang', 'uc': 'uc_them',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Thêm mới khoang'],
        ['Mô tả', 'Tạo một khoang mới trong một dãy qua cửa sổ nhập liệu. Tạo khoang KHÔNG tự sinh vị trí; vị trí thêm ở màn Vị trí (BR-05).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Có ít nhất một dãy đang Hoạt động (cùng nhà kho, kho đang Hoạt động) trong phạm vi.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở cửa sổ "Tạo mới khoang", Trạng thái mặc định Hoạt động.\n3. Người dùng chọn Kho → Nhà kho → Dãy, nhập Mã khoang, Tên khoang (Trạng thái, Mô tả nếu cần) rồi bấm Lưu.\n4. Hệ thống kiểm tra dữ liệu, ghi khoang vào dãy đã chọn.\n5. Ghi nhận Tạo mới trong lịch sử của khoang.\n6. Đóng cửa sổ, tải lại danh sách, báo "Thêm mới thành công."'],
        ['Dòng sự kiện phụ', '• Thiếu / sai dữ liệu → báo đỏ dưới ô (Kho, Nhà kho, Dãy, Mã, Tên báo cùng lúc) + toast "Bạn chưa nhập đầy đủ thông tin.", cửa sổ không đóng, dữ liệu đã nhập còn nguyên.\n• Bấm "Lưu & Tiếp tục" → lưu rồi giữ cửa sổ, các ô về trống để nhập khoang tiếp.\n• Bấm Đóng / (x) / bấm ra ngoài: chưa nhập gì thì đóng; đã nhập thì hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', 'Nút Lưu / Lưu & Tiếp tục bị khóa trong lúc đang lưu để tránh tạo trùng.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': POPUP % 'Tạo mới khoang',
    'anh': [('10_create', 'Cửa sổ Tạo mới khoang'), ('11_code_error', 'Lỗi định dạng Mã khoang báo ngay khi gõ'),
            ('18_unsaved', 'Hộp xác nhận Thông tin chưa lưu khi đóng cửa sổ đã nhập dữ liệu')],
    'ui': ui(UI8, FORM_ROWS + [
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi đóng cửa sổ.'],
        ['Nút Lưu & Tiếp tục', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi giữ cửa sổ, xoá trắng các ô.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ, không lưu (đã nhập thì hỏi xác nhận).'],
        ['Hộp Thông tin chưa lưu', 'Label', 'Enable / Ẩn', '–', '–', 'Ẩn', '- Nội dung "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"\n- Nút Thoát: đóng không lưu; nút Ở lại: quay về cửa sổ.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho" (thiếu quyền thì nút ẩn).\nAfter:\n– Mở cửa sổ với các ô trống, Trạng thái = Hoạt động; Nhà kho, Dãy bị khóa.'],
        ['Chọn Kho / Nhà kho', 'Change', 'After:\n– Mở khóa ô cấp dưới, chỉ liệt kê mục thuộc cấp vừa chọn; giá trị cấp dưới không còn thuộc nó thì tự về trống.'],
        ['Gõ Mã khoang', 'Change', 'During:\n– Sai ký tự hoặc quá 50 ký tự → báo đỏ ngay dưới ô.'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho".\nDuring:\n– Kiểm tra bắt buộc Kho, Nhà kho, Dãy, Mã, Tên; độ dài, ký tự Mã khoang; dãy còn trong phạm vi và dãy / nhà kho / kho đang Hoạt động; trùng Mã / Tên trong cùng dãy.\n' + TRUOC_LUU + '\nAfter:\n– Ghi khoang vào dãy đã chọn (không sinh vị trí).\n– Ghi nhận Tạo mới trong lịch sử.\n– Đóng cửa sổ, tải lại danh sách, báo "Thêm mới thành công."'],
        ['Bấm Lưu & Tiếp tục', 'Click', 'During:\n– Như nút Lưu.\n' + TRUOC_LUU + '\nAfter:\n– Ghi như nút Lưu, giữ cửa sổ, các ô về trống, Trạng thái về Hoạt động.'],
        ['Bấm Đóng / (x) / bấm ra ngoài', 'Click', 'After:\n– Chưa nhập gì → đóng cửa sổ.\n– Đã nhập → hiện hộp "Thông tin chưa lưu": Thoát thì đóng không lưu, Ở lại thì quay về cửa sổ.'],
    ],
})

# 2.4 Chỉnh sửa ------------------------------------------------------------------
EDIT_ROWS = [
    ['Kho, Nhà kho, Dãy', 'Dropdown', 'Disable', 'Theo khoang', 'Không', 'Dữ liệu hiện tại',
     '- Bị khóa (nền xám): không đổi được dãy của khoang đã tạo.\n- Dãy / nhà kho / kho đang gắn với khoang đã bị khóa vẫn hiện đúng tên, kèm dấu khóa.'],
    [*FORM_ROWS[3][:5], 'Dữ liệu hiện tại', FORM_ROWS[3][6] + '\n- Giữ nguyên mã của chính khoang thì không báo trùng.'],
    [*FORM_ROWS[4][:5], 'Dữ liệu hiện tại', FORM_ROWS[4][6]],
    ['Số vị trí', 'Textbox', 'Read-only', 'Số nguyên ≥ 0', 'Không', 'Số vị trí hiện có',
     '- Chỉ xem, đếm cả vị trí đã khóa.\n- Icon ⓘ: "Số vị trí (ô chứa hàng) đang thuộc khoang này, đếm cả vị trí đã khoá. Ô chỉ để xem: vị trí được tạo sẵn khi tạo dãy, muốn thêm, sửa hay khoá vị trí thì làm ở màn Vị trí."'],
    ['Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Không', 'Dữ liệu hiện tại',
     '- Khoang còn vị trí đang Hoạt động: ô bị khóa ở "Hoạt động".\n- Chọn Khóa rồi Lưu = khóa khoang (BR-07).'],
    [*FORM_ROWS[6][:5], 'Dữ liệu hiện tại', FORM_ROWS[6][6]],
]
FR.append({
    'ten': 'Chỉnh sửa khoang', 'uc': 'uc_sua',
    'qtc': 'Validate dữ liệu, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chỉnh sửa khoang'],
        ['Mô tả', 'Sửa Mã, Tên, Trạng thái, Mô tả của khoang đang Hoạt động. Không đổi được dãy chứa khoang.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Khoang đang Hoạt động và thuộc phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Sửa ở cột Hành động.\n2. Hệ thống mở cửa sổ "Sửa khoang" với dữ liệu hiện tại; Kho, Nhà kho, Dãy bị khóa.\n3. Người dùng sửa và bấm Lưu.\n4. Hệ thống kiểm tra, ghi thay đổi.\n5. Ghi nhận Thay đổi thông tin (đổi Trạng thái ghi riêng Khóa) trong lịch sử.\n6. Đóng cửa sổ, báo "Cập nhật thành công."'],
        ['Dòng sự kiện phụ', '• Giữ nguyên Mã / Tên của chính khoang → không báo trùng.\n• Chọn Khóa cho khoang vừa có vị trí đang hoạt động → báo "' + KHOA_CON + '"\n• Khoang vừa bị người khác khóa / xóa → báo "Dữ liệu đã thay đổi, vui lòng tải lại".\n• Bấm Đóng khi đã sửa → hỏi "Thông tin chưa lưu".'],
    ],
    'menu_them': ' => Sửa {icon:btn_sua}',
    'ghi_chu_layout': POPUP % 'Sửa khoang',
    'anh': [('12_edit', 'Cửa sổ Sửa khoang (Kho, Nhà kho, Dãy bị khóa)')],
    'ui': ui(UI8, EDIT_ROWS + [
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu thay đổi rồi đóng cửa sổ.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng không lưu (đã sửa thì hỏi xác nhận). Cửa sổ Sửa không có nút Lưu & Tiếp tục.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện khi khoang Hoạt động và người dùng có quyền.\nAfter:\n– Tải dữ liệu khoang, mở cửa sổ; khoang không còn (vừa bị xoá / ngoài phạm vi) → báo "Dữ liệu đã thay đổi, vui lòng tải lại".'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền, khoang phải đang Hoạt động.\nDuring:\n– Kiểm tra như Thêm mới (bỏ qua trùng với chính khoang, dãy giữ nguyên theo bản ghi); khoang còn vị trí đang hoạt động thì không được chọn Khóa.\n' + TRUOC_LUU + '\nAfter:\n– Ghi thay đổi, ghi nhận Thay đổi thông tin / Khóa trong lịch sử.\n– Đóng cửa sổ, tải lại danh sách, báo "Cập nhật thành công."'],
        ['Bấm Đóng / (x) / bấm ra ngoài', 'Click', 'After:\n– Chưa đổi gì → đóng; đã đổi → hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
    ],
})

# 2.5 Xóa ---------------------------------------------------------------------------
FR.append({
    'ten': 'Xóa khoang', 'uc': 'uc_xoa',
    'qtc': 'Quy tắc Xóa, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xóa khoang'],
        ['Mô tả', 'Xóa hẳn khoang đang Hoạt động chưa có vị trí nào và chưa được chọn trong kế hoạch kiểm kê theo vị trí (BR-08).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Khoang đang Hoạt động, không có vị trí (kể cả vị trí đã khóa), chưa dùng trong kế hoạch kiểm kê.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Xóa ở cột Hành động.\n2. Hệ thống hiện hộp "Xác nhận xóa": "Bạn có chắc muốn xóa khoang \'<Tên khoang>\'?"\n3. Người dùng bấm Xóa.\n4. Hệ thống ghi nhận Xóa trong lịch sử rồi xóa hẳn khoang.\n5. Tải lại danh sách, báo "Xóa thành công."'],
        ['Dòng sự kiện phụ', '• Bấm Hủy → đóng hộp, không thay đổi.\n• Khoang vừa bị khóa → "Không thể xóa khoang đang ở trạng thái khóa. Hãy mở khóa trước."\n• Khoang vừa được thêm vị trí / dùng trong kế hoạch kiểm kê → "Không thể xóa do dữ liệu đang được sử dụng."\n• Khoang vừa bị người khác xóa → "Dữ liệu đã thay đổi, vui lòng tải lại".'],
    ],
    'menu_them': ' => Xóa {icon:btn_xoa}',
    'ghi_chu_layout': POPUP % 'Xác nhận xóa',
    'anh': [('13_delete', 'Hộp xác nhận xóa khoang')],
    'ui': ui(UI4, [
        ['Nút Xóa (cột Hành động)', 'Button', 'Biểu tượng thùng rác; chỉ hiện khi khoang Hoạt động, không có vị trí, chưa dùng trong kế hoạch kiểm kê và người dùng có quyền.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận xóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn xóa khoang \'<Tên khoang>\'?"'],
        ['Nút Xóa', 'Button', 'Xác nhận xóa.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không xóa.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Xóa ở cột Hành động', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên khoang.'],
        ['Bấm Xóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền, khoang thuộc phạm vi.\nDuring:\n– Khoang phải đang Hoạt động, không có vị trí, chưa dùng trong kế hoạch kiểm kê.\n' + TRUOC_LUU + '\nAfter:\n– Ghi nhận Xóa trong lịch sử, xóa hẳn khoang.\n– Tải lại danh sách, báo "Xóa thành công."'],
        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.6 Khóa / Mở khóa -----------------------------------------------------------
FR.append({
    'ten': 'Khóa / Mở khóa khoang', 'uc': 'uc_khoa',
    'qtc': 'Quy tắc Khóa/Mở khóa, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Khóa / Mở khóa khoang'],
        ['Mô tả', 'Đổi trạng thái khoang giữa Hoạt động và Khóa. Khoang Khóa vẫn nằm trong danh mục nhưng không còn chọn được ở các ô chọn khoang (màn Vị trí, kế hoạch kiểm kê…) (BR-07).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Khóa: khoang Hoạt động, không còn vị trí đang Hoạt động. Mở khóa: khoang đang Khóa, dãy chứa nó đang Hoạt động.'],
        ['Dòng sự kiện chính', '1. Người dùng chọn Khóa (hoặc Mở khóa) ở cột Hành động.\n2. Hệ thống hiện hộp "Xác nhận khóa" / "Xác nhận mở khóa" kèm tên khoang.\n3. Người dùng bấm Khóa / Mở khóa.\n4. Hệ thống đổi trạng thái, ghi nhận Khóa / Mở khóa trong lịch sử.\n5. Tải lại danh sách, báo "Khóa thành công." / "Mở khóa thành công."'],
        ['Dòng sự kiện phụ', '• Bấm Hủy → không thay đổi.\n• Khoang còn vị trí đang hoạt động: không có nút Khóa; nếu vị trí vừa được thêm → "' + KHOA_CON + '"\n• Dãy chứa khoang đang Khóa: không có nút Mở khóa; nếu dãy vừa bị khóa → "Không thể mở khóa khoang khi danh mục cha đang bị khóa."\n• Khoang đã bị người khác đổi trạng thái → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n• Sau khi Khóa: nút Sửa, Xóa ẩn; sau khi Mở khóa: nút Sửa hiện lại.'],
    ],
    'menu_them': ' => Khóa {icon:btn_khoa_row} / Mở khóa {icon:btn_mokhoa_row}',
    'ghi_chu_layout': POPUP % 'Xác nhận khóa / Xác nhận mở khóa',
    'anh': [('14_lock', 'Hộp xác nhận khóa khoang'), ('15_unlock', 'Hộp xác nhận mở khóa khoang')],
    'ui': ui(UI4, [
        ['Nút Khóa (cột Hành động)', 'Button', '- Biểu tượng ổ khóa; hiện khi khoang Hoạt động, không còn vị trí đang hoạt động, có quyền.\n- Dòng có nút Xóa thì Khóa nằm trong nút ba chấm "Hành động khác".'],
        ['Nút Mở khóa (cột Hành động)', 'Button', 'Biểu tượng ổ khóa mở; hiện khi khoang đang Khóa, dãy chứa nó đang Hoạt động, có quyền.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận khóa" hoặc "Xác nhận mở khóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn khóa khoang \'<Tên khoang>\'?" / "Bạn có chắc muốn mở khóa khoang \'<Tên khoang>\'?"'],
        ['Nút Khóa / Mở khóa', 'Button', 'Xác nhận đổi trạng thái.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không thay đổi.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Chọn Khóa / Mở khóa', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên khoang.'],
        ['Bấm Khóa / Mở khóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền, khoang thuộc phạm vi.\nDuring:\n– Khoang đã ở trạng thái đích → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n– Khóa mà khoang còn vị trí đang hoạt động → "' + KHOA_CON + '"\n– Mở khóa mà dãy đang Khóa → "Không thể mở khóa khoang khi danh mục cha đang bị khóa."\n' + TRUOC_LUU + '\nAfter:\n– Đổi trạng thái, ghi nhận Khóa / Mở khóa trong lịch sử, tải lại danh sách, báo thành công.'],
        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.7 Lịch sử --------------------------------------------------------------------
FR.append({
    'ten': 'Xem lịch sử thay đổi',
    'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem lịch sử thay đổi khoang'],
        ['Mô tả', 'Liệt kê các lần thao tác trên một khoang (Tạo mới, Thay đổi thông tin, Khóa, Mở khóa, Xóa), mới nhất ở trên, kèm người thực hiện, thời điểm, giá trị cũ → mới.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Lịch sử ở cột Hành động (hoặc Xem lịch sử trong cửa sổ Xem chi tiết).\n2. Hệ thống mở cửa sổ "Lịch sử thay đổi: <Tên khoang>" và liệt kê các mốc.'],
        ['Dòng sự kiện phụ', '• Lọc theo Loại hành động, Người thực hiện, Từ ngày / Đến ngày bằng nút Bộ lọc trong cửa sổ.\n• Các trường được ghi: Mã khoang, Tên khoang, Dãy (bằng tên), Mô tả, Trạng thái.\n• Khoang sinh tự động khi tạo dãy cũng có mốc Tạo mới.'],
    ],
    'menu_them': ' => Lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': POPUP % 'Lịch sử thay đổi',
    'anh': [('16_history', 'Cửa sổ Lịch sử thay đổi của khoang')],
    'ui': ui(UI6, [
        ['Nút Lịch sử (cột Hành động)', 'Button', 'Enable', 'Hiển thị', 'Luôn có ở mọi dòng (kể cả khoang Khóa); dòng có 4 nút thì nằm trong nút ba chấm.'],
        ['Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Lịch sử thay đổi: <Tên khoang>', ''],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Mở các ô lọc Loại hành động, Người thực hiện, Từ ngày, Đến ngày.'],
        ['Danh sách mốc', 'Table/Grid', 'Read-only', 'Theo dữ liệu', '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, loại hành động, "Người thực hiện: Họ tên — Phòng ban".\n- Dòng thay đổi: "<Trường>: giá trị cũ → giá trị mới".\n- Chưa có dữ liệu: "Chưa có lịch sử thao tác nào."'],
        ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lịch sử', 'Click', 'After:\n– Tải lịch sử của khoang, mới nhất trên cùng.'],
        ['Chọn điều kiện ở Bộ lọc', 'Change', 'After:\n– Lọc lại các mốc; không có mốc khớp → "Không có lịch sử phù hợp bộ lọc."'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.8 Import ---------------------------------------------------------------------
FR.append({
    'ten': 'Import khoang từ file Excel', 'uc': 'uc_import',
    'qtc': 'Quy tắc Import file, Validate dữ liệu, Thông báo.',
    'gioi_thieu': [
        ['Tên chức năng', 'Import khoang từ file Excel'],
        ['Mô tả', 'Tạo nhiều khoang từ file Excel theo file mẫu; dãy chứa khoang xác định bằng Mã kho → Mã nhà kho → Mã dãy. Mỗi dòng được kiểm tra và ghi như khi Tạo mới (ghi lịch sử Tạo mới) (BR-10).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Import Excel, hệ thống mở cửa sổ "Import khoang".\n2. Bấm Tải file mẫu (Mau_import_khoang.xlsx), điền dữ liệu.\n3. Bấm Chọn file Excel, chọn file, bấm Load lên bảng: dữ liệu hiện ở bảng xem trước, ô Tổng = số dòng.\n4. Bấm Validate: hệ thống kiểm tra từng dòng (chưa ghi dữ liệu), hiện Tổng / Hợp lệ / Lỗi; dòng lỗi tô đỏ kèm lý do, dòng hợp lệ bị khóa.\n5. Sửa dòng lỗi rồi Validate lại, hoặc bấm Bỏ dòng lỗi.\n6. Khi không còn dòng lỗi, bấm Import: hệ thống ghi từng dòng, ghi nhận Tạo mới trong lịch sử, báo kết quả, tải lại danh sách.'],
        ['Dòng sự kiện phụ', '• File quá 500 dòng dữ liệu → "File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần."\n• Dòng vừa bị trùng với khoang người khác tạo trong lúc Import → bị bỏ qua, các dòng khác vẫn ghi; bảng kết quả liệt kê dòng bị bỏ qua.\n• Bấm Xoá trạng thái validate để sửa lại cả dòng đã khóa.\n• Bấm Làm mới để làm lại từ đầu; Đóng để thoát.'],
    ],
    'menu_them': ' => Import Excel {icon:btn_import}',
    'ghi_chu_layout': POPUP % 'Import khoang',
    'anh': [('21_import_open', 'Cửa sổ Import khoang khi vừa mở'), ('22_import_loaded', 'Dữ liệu sau khi Load lên bảng'),
            ('23_import_validated', 'Kết quả Validate — dòng lỗi nêu rõ lý do')],
    'ui': ui(UI7I, [
        ['Nút Chọn file Excel', 'Button', 'Enable', '–', '–', 'Chọn file .xlsx, hiện tên file bên cạnh.'],
        ['Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Tải Mau_import_khoang.xlsx: dòng 1 tên cột (cột bắt buộc có *), dòng 2 hướng dẫn, 2 dòng dữ liệu mẫu.'],
        ['Nút Load lên bảng', 'Button', 'Enable / Disable', '–', 'Disable', 'Bấm được khi đã chọn file; đọc file lên bảng xem trước.'],
        ['Nút Validate', 'Button', 'Enable / Disable', '–', 'Disable', 'Bấm được khi bảng có dữ liệu; kiểm tra từng dòng, chưa ghi dữ liệu.'],
        ['Nút Import', 'Button', 'Enable / Disable', '–', 'Disable', 'Chỉ bấm được khi đã Validate, còn ≥ 1 dòng hợp lệ và KHÔNG còn dòng lỗi.'],
        ['Ô Tổng / Hợp lệ / Lỗi', 'Label', 'Read-only', '–', 'Tổng: 0', 'Tổng hiện sau Load; Hợp lệ, Lỗi hiện sau Validate.'],
        ['Cột Mã kho *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Mã kho ở màn Kho vật lý, thuộc phạm vi công ty. Không có: "Không tồn tại kho có mã "<mã>"".'],
        ['Cột Mã nhà kho *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Mã nhà kho thuộc kho trên. Không có: "Không tồn tại nhà kho có mã "<mã>" trong kho "<mã kho>"".'],
        ['Cột Mã dãy *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Mã dãy thuộc nhà kho trên; dãy / nhà kho / kho phải đang Hoạt động.'],
        ['Cột Mã khoang *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Chữ không dấu, số, dấu - và _, tối đa 50 ký tự, không trùng trong dãy và trong file.'],
        ['Cột Tên khoang *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Tối đa 255 ký tự, không trùng trong dãy và trong file.'],
        ['Cột Trạng thái', 'Table/Grid', 'Enable', 'Không', 'Theo file', 'Hoạt động / Khóa; để trống = Hoạt động. Giá trị khác: "Chỉ nhận Hoạt động hoặc Khóa".'],
        ['Cột Mô tả', 'Table/Grid', 'Enable', 'Không', 'Theo file', 'Tối đa 500 ký tự.'],
        ['Nút Bỏ dòng lỗi', 'Button', 'Enable', '–', '–', 'Loại các dòng lỗi khỏi bảng xem trước.'],
        ['Nút Xoá trạng thái validate', 'Button', 'Enable', '–', '–', 'Mở khóa mọi dòng để sửa lại, phải Validate lại.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', 'Đóng cửa sổ.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá file và bảng, làm lại từ đầu.'],
    ]),
    'ui_widths': UI7IW,
    'events': [
        ['Bấm Load lên bảng', 'Click', 'During:\n– File không có dòng dữ liệu → "Không có dòng dữ liệu hợp lệ."\n– Quá 500 dòng → báo giới hạn 500 dòng.\nAfter:\n– Hiện dữ liệu lên bảng xem trước, ô Tổng = số dòng.'],
        ['Bấm Validate', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho".\nDuring:\n– Mỗi dòng tra Mã kho → Mã nhà kho → Mã dãy, rồi kiểm như Tạo mới; trùng Mã / Tên khoang trong cùng dãy giữa các dòng của file ("Bị trùng trong file").\nAfter:\n– Hiện Tổng / Hợp lệ / Lỗi, toast "Validate xong: X hợp lệ, Y không hợp lệ" (hoặc "Validate thành công"); dòng lỗi tô đỏ kèm lý do theo thứ tự cột, dòng hợp lệ bị khóa.'],
        ['Bấm Import', 'Click', 'Before:\n– Đã Validate, không còn dòng lỗi.\nDuring:\n– Hệ thống kiểm lại từng dòng ngay trước khi ghi.\n' + TRUOC_LUU + '\nAfter:\n– Ghi từng dòng như Tạo mới, ghi nhận Tạo mới trong lịch sử.\n– Báo kết quả, đóng cửa sổ, tải lại danh sách; có dòng bị bỏ qua thì hiện bảng kết quả.'],
        ['Bấm Bỏ dòng lỗi / Xoá trạng thái validate', 'Click', 'After:\n– Bỏ dòng lỗi khỏi bảng / mở khóa các dòng để sửa.'],
        ['Bấm Đóng / Làm mới', 'Click', 'After:\n– Đóng cửa sổ / xoá dữ liệu đang xem để làm lại.'],
    ],
})

# 2.9 Xuất Excel -------------------------------------------------------------------
FR.append({
    'ten': 'Xuất danh sách ra Excel', 'uc': 'uc_xuat',
    'qtc': 'Quy tắc Excel, Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách khoang ra Excel'],
        ['Mô tả', 'Xuất toàn bộ khoang khớp bộ lọc đang áp dụng (mọi trang) ra file Excel, người dùng chọn trường và thứ tự cột (BR-11).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng lọc danh sách (nếu cần), bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất file", tích sẵn các cột đang hiện trên bảng.\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự rồi bấm Xuất file.\n4. Hệ thống tải file danh_sach_khoang.xlsx, báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Kết quả rỗng vẫn xuất file (tiêu đề + tên cột).\n• Ô Ngày tạo đang sai (Từ > Đến) → báo lỗi, không xuất.\n• Lỗi hệ thống → "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': POPUP % 'Chọn trường xuất file',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất file')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '"Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file."'],
        ['Danh sách trường', 'Table/Grid', 'Enable', 'Tích theo cột đang hiện', '12 trường: Mã khoang, Tên khoang, Dãy, Nhà kho, Kho, Số vị trí, Mô tả, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. Mỗi trường có ô tích và biểu tượng ☰ kéo đổi vị trí.'],
        ['Nút Chọn tất cả', 'Button', 'Enable', '–', 'Tích mọi trường.'],
        ['Nút Bỏ chọn hết', 'Button', 'Enable', '–', 'Bỏ tích mọi trường.'],
        ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn x/12 trường', ''],
        ['Nút Xuất file', 'Button', 'Enable / Disable', 'Enable', 'Tải file; không bấm được khi không còn trường nào được chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ, không xuất.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ, tích sẵn theo cột đang hiện.'],
        ['Bấm Xuất file', 'Click', 'During:\n– Ô Ngày tạo sai → báo "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", không xuất.\n' + TRUOC_LUU + '\nAfter:\n– Tải file danh_sach_khoang.xlsx: tiêu đề "Danh sách khoang", cột theo thứ tự đã chọn, mọi dòng khớp bộ lọc; báo "Xuất Excel thành công".'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.10 Xem chi tiết ----------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết khoang', 'uc': 'uc_xem',
    'qtc': 'Màn Xem chi tiết, Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết khoang'],
        ['Mô tả', 'Xem toàn bộ thông tin một khoang ở chế độ chỉ đọc, kèm khối Lịch sử.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm vào Mã khoang trên bảng.\n2. Hệ thống mở cửa sổ "Xem chi tiết khoang", mọi ô chỉ đọc.\n3. Bấm Xem lịch sử để mở khối Lịch sử ngay trong cửa sổ.'],
        ['Dòng sự kiện phụ', '• Khoang vừa bị xoá / ngoài phạm vi → báo "Dữ liệu đã thay đổi, vui lòng tải lại", không mở cửa sổ.'],
    ],
    'menu_them': ' => Bấm Mã khoang',
    'ghi_chu_layout': POPUP % 'Xem chi tiết khoang',
    'anh': [('17_detail', 'Cửa sổ Xem chi tiết khoang ở chế độ chỉ đọc'),
            ('17b_detail_history', 'Khối Lịch sử trong cửa sổ Xem chi tiết')],
    'ui': ui(UI6, [
        ['Kho, Nhà kho, Dãy', 'Dropdown', 'Read-only', 'Dữ liệu hiện tại', 'Dạng "Mã - Tên"; mục đã khóa vẫn hiện kèm dấu khóa.'],
        ['Mã khoang, Tên khoang', 'Textbox', 'Read-only', 'Dữ liệu hiện tại', 'Không có dấu (*).'],
        ['Số vị trí', 'Textbox', 'Read-only', 'Số vị trí hiện có', 'Có icon ⓘ giải thích như cửa sổ Sửa.'],
        ['Trạng thái', 'Dropdown', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Mô tả', 'Textarea', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Khối Lịch sử', 'Table/Grid', 'Enable', 'Thu gọn', '- Nút Xem lịch sử mở khối, hiện số mốc.\n- Nút Làm mới tải lại, Thu gọn đóng khối, Bộ lọc lọc mốc như mục 2.7.'],
        ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ. Không có nút Lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Mã khoang', 'Click', 'After:\n– Tải dữ liệu, mở cửa sổ chỉ đọc.'],
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
        ['Dòng sự kiện phụ', '• Cột STT, Mã khoang, Hành động là cột khóa: không bỏ tích, không kéo được.\n• Bấm Đóng → bỏ các thay đổi vừa chỉnh.'],
    ],
    'menu_them': ' => Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': POPUP % 'Tuỳ chỉnh cột',
    'anh': [('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột — STT, Mã khoang, Hành động bị khóa')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '"Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng."'],
        ['Danh sách cột', 'Table/Grid', 'Enable', 'Theo cấu hình đã lưu', '14 cột theo thứ tự trên bảng. Mặc định ẩn: Số vị trí, Mô tả.'],
        ['Cột khóa', 'Table/Grid', 'Disable', 'Luôn tích', 'STT, Mã khoang, Hành động: ô tích xám kèm biểu tượng khóa, không ẩn và không đổi vị trí được.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Tích / bỏ tích mọi cột (trừ cột khóa).'],
        ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn x/14 cột', ''],
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
    'menu': [('Kho', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Khoang', 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu chức năng.',
        'Làm rõ phạm vi dữ liệu theo công ty của kho, ràng buộc trùng Mã / Tên khoang trong cùng dãy, việc chọn dãy theo dây chuyền Kho → Nhà kho → Dãy, điều kiện Khóa (còn vị trí đang hoạt động), Mở khóa (dãy đang hoạt động) và Xóa (chưa có vị trí, chưa dùng trong kế hoạch kiểm kê).',
    ],
    'thuat_ngu': [
        ['Khoang', 'Cấp thứ 4 của cây kho: Kho vật lý → Nhà kho → Dãy → Khoang → Vị trí. Mỗi khoang thuộc đúng một dãy.'],
        ['Dãy', 'Cấp chứa khoang; khi tạo dãy hệ thống tự sinh các khoang "Khoang 1"… "Khoang N" (mã K1…KN) kèm vị trí.'],
        ['Vị trí', 'Ô chứa hàng thuộc khoang (hoặc vị trí tự do gắn thẳng vào kho, không thuộc khoang nào).'],
        ['Kế hoạch kiểm kê theo vị trí', 'Màn chọn phạm vi kiểm kê theo nhà kho / dãy / khoang / vị trí; khoang đã được chọn ở đây không xóa được.'],
        ['Hoạt động', 'Trạng thái khoang dùng được ở các màn nghiệp vụ.'],
        ['Khóa', 'Khoang vẫn nằm trong danh mục, xem được lịch sử nhưng không còn chọn được ở các ô chọn khoang.'],
        ['Super admin', 'Tài khoản quản trị cao nhất, xem được khoang của mọi công ty.'],
    ],
    'quyen_truoc': ['Màn hình dùng một quyền duy nhất "Quản lý kho" (nhóm Danh mục kho) cho cả xem lẫn thao tác; quyền này dùng chung cho 7 màn Danh mục của phân hệ Kho. Quyền được gán vào vai trò theo công ty.'],
    'quyen_rows': [['Quản lý kho', 'Xem danh sách, tìm kiếm, xem chi tiết, lịch sử, tùy chỉnh cột, xuất Excel; Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Import Excel.']],
    'ma_tran': [['Chức năng', 'Quản lý kho', 'Không có quyền']] + [[f, 'Có', 'Không'] for f in [
        'FR-01 Xem danh sách khoang', 'FR-02 Tìm kiếm và lọc', 'FR-03 Thêm mới khoang', 'FR-04 Chỉnh sửa khoang',
        'FR-05 Xóa khoang', 'FR-06 Khóa / Mở khóa khoang', 'FR-07 Xem lịch sử thay đổi',
        'FR-08 Import khoang từ file Excel', 'FR-09 Xuất danh sách ra Excel', 'FR-10 Xem chi tiết khoang',
        'FR-11 Tùy chỉnh cột hiển thị']],
    'ma_tran_widths': [2.6, 1.2, 1.2],
    'quyen_sau': ['Phạm vi dữ liệu: người dùng thường chỉ thấy và thao tác khoang thuộc kho của công ty mình; Super admin thấy khoang mọi công ty và có thêm ô lọc Công ty (BR-01).'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Phạm vi dữ liệu theo công ty', [
            '– Khoang thuộc công ty của kho chứa nó (suy qua dãy → nhà kho → kho).',
            '– Người dùng thường chỉ thấy, xem, sửa, khóa, xóa, xuất khoang thuộc kho của công ty đang làm việc; ô chọn Kho / Nhà kho / Dãy cũng chỉ có mục trong phạm vi.',
            '– Super admin thấy khoang mọi công ty, có thêm ô lọc Công ty.',
            '– Không xác định được công ty của người dùng → không thấy khoang nào.',
            '– Thao tác trên khoang ngoài phạm vi bị từ chối như dữ liệu không tồn tại.'], ['Xem danh sách', 'Xuất Excel', 'Chỉnh sửa', 'Xóa', 'Khóa / Mở khóa', 'Import']),
        ('BR-02', 'Mã khoang', [
            '– Bắt buộc, 1–50 ký tự, chỉ gồm chữ không dấu, số, dấu - và _; cắt khoảng trắng đầu / cuối.',
            '– Không trùng khoang khác TRONG CÙNG DÃY (so cả khoang đang Khóa); khác dãy thì được trùng (mỗi dãy đều có K1).',
            '– Giữ nguyên chữ hoa / thường người dùng nhập.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-03', 'Tên khoang', ['– Bắt buộc, tối đa 255 ký tự, không trùng trong cùng dãy như Mã khoang.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-04', 'Dãy chứa khoang', [
            '– Bắt buộc khi tạo; chọn qua Kho → Nhà kho → Dãy (Kho, Nhà kho chỉ để lọc, không lưu).',
            '– Dãy, nhà kho và kho của nó phải đang Hoạt động và thuộc phạm vi; ngược lại báo "Dãy "<Tên dãy>" đã bị khóa, vui lòng chọn dãy khác" / "Dãy không tồn tại".',
            '– Khi sửa không đổi được dãy (ô bị khóa; hệ thống giữ dãy theo bản ghi).'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-05', 'Khoang và vị trí', [
            '– Tạo khoang (tay hoặc Import) KHÔNG sinh vị trí; vị trí thêm ở màn Vị trí.',
            '– Khoang sinh sẵn khi tạo dãy: "Khoang i" mã Ki, có kèm vị trí.',
            '– Số vị trí = số vị trí thuộc khoang, đếm cả vị trí đã Khóa.'], ['Thêm mới', 'Import', 'Xem danh sách']),
        ('BR-06', 'Ô Trạng thái khi sửa', ['– Khoang còn vị trí đang Hoạt động: ô Trạng thái bị khóa; chọn Khóa rồi Lưu chịu cùng điều kiện với nút Khóa (BR-07).'], ['Chỉnh sửa']),
        ('BR-07', 'Điều kiện Khóa / Mở khóa', [
            '– Chỉ khóa được khoang đang Hoạt động và KHÔNG còn vị trí đang Hoạt động (vị trí đã khóa hết thì khóa được).',
            '– Chỉ mở khóa được khi dãy chứa khoang đang Hoạt động.',
            '– Khoang đang Khóa: ẩn Sửa, Xóa; không còn trong ô chọn khoang ở các màn khác; còn khoang đang Hoạt động thì dãy cha không khóa được.'], ['Khóa / Mở khóa', 'Chỉnh sửa']),
        ('BR-08', 'Điều kiện và cách Xóa', [
            '– Chỉ xóa khoang đang Hoạt động, KHÔNG có vị trí nào (kể cả vị trí đã Khóa) và chưa được chọn trong kế hoạch kiểm kê theo vị trí.',
            '– Xóa là xóa hẳn khoang; lịch sử ghi mốc Xóa trước khi xóa. Mã, tên dùng lại được sau khi xóa.'], ['Xóa']),
        ('BR-09', 'Lọc dây chuyền', [
            '– Bộ lọc: Công ty → Kho → Nhà kho → Dãy; đổi cấp trên thì giá trị cấp dưới không còn thuộc nó tự về trống.',
            '– Ô Kho / Nhà kho / Dãy mặc định chỉ có mục đang Hoạt động; biểu tượng ổ khóa trên nhãn để hiện cả mục đã khóa.'], ['Tìm kiếm và lọc', 'Thêm mới']),
        ('BR-10', 'Import', [
            '– Mỗi dòng tra dãy theo Mã kho → Mã nhà kho → Mã dãy rồi kiểm và ghi như Tạo mới (BR-02 → BR-05); báo đủ lỗi của dòng theo thứ tự cột.',
            '– Trùng Mã / Tên khoang trong cùng dãy giữa các dòng của file → "Bị trùng trong file".',
            '– Tối đa 500 dòng dữ liệu mỗi lần; chỉ Import khi đã Validate và không còn dòng lỗi.'], ['Import']),
        ('BR-11', 'Xuất Excel và lọc Ngày tạo', [
            '– Xuất mọi dòng khớp bộ lọc đang áp dụng (không chỉ trang đang xem), cột theo thứ tự người dùng chọn; tên file danh_sach_khoang.xlsx.',
            '– Ngày tạo Từ lớn hơn Đến → báo đỏ "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", xoá bảng, không tải dữ liệu và không xuất Excel.'], ['Tìm kiếm và lọc', 'Xuất Excel']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây sinh, chọn, lọc hoặc hiển thị dữ liệu Khoang; khoang đang Khóa không còn chọn được ở các ô chọn khoang.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng có quyền "Quản lý kho"',
    'mains': [('FR-01', 'Xem danh sách khoang', 'view'), ('FR-03', 'Thêm mới khoang', 'crud'),
              ('FR-04', 'Chỉnh sửa khoang', 'crud'), ('FR-05', 'Xóa khoang', 'action'),
              ('FR-06', 'Khóa / Mở khóa khoang', 'action'), ('FR-08', 'Import khoang từ file Excel', 'io'),
              ('FR-09', 'Xuất danh sách khoang ra Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc khoang', 'view'), ('FR-10', 'Xem chi tiết khoang', 'view'),
             ('FR-11', 'Tùy chỉnh cột hiển thị', 'view'), ('FR-07', 'Xem lịch sử thay đổi', 'view')],
    'rieng': [('FR-03', 'Thêm mới khoang', 'crud', 'uc_them'), ('FR-04', 'Chỉnh sửa khoang', 'crud', 'uc_sua'),
              ('FR-05', 'Xóa khoang', 'action', 'uc_xoa'), ('FR-06', 'Khóa / Mở khóa khoang', 'action', 'uc_khoa'),
              ('FR-08', 'Import khoang từ file Excel', 'io', 'uc_import'),
              ('FR-09', 'Xuất danh sách khoang ra Excel', 'io', 'uc_xuat'), ('FR-10', 'Xem chi tiết khoang', 'view', 'uc_xem')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)

# -*- coding: utf-8 -*-
"""SRS - Danh mục nhà kho (form Danh mục quốc gia, TPE duyệt) — chép khuôn màn mẫu docs/warehouses/gen_srs.py.

Nguồn (code HRM hiện tại, nhánh có code kho):
  FE hrm-client/pages/warehouse/houses/{index.vue, AddHouseModal.vue}, utils/mixins/{vehicleCatalogScreenMixin,
     vehicleCatalogModalMixin, warehouseCatalogModalMixin, warehouseCatalogImportMixin, warehouseLockedFilterMixin,
     createdRangeFilterMixin}.js, utils/warehouse-catalog-import.js, components/warehouse-catalog/LockableFilterSelect.vue,
     components/subsystem-menu/warehouse.js
  BE Modules/MasterData: Entities/Warehouse/House.php, Http/Controllers/V1/Warehouse/{HouseController,
     WarehouseTreeCatalogController}.php, ProductClassification/BaseCatalogController.php,
     Http/Requests/Warehouse/HouseRequest.php, Services/Warehouse/{HouseService, WarehouseCatalogScope,
     Concerns/ImportsWarehouseCatalogRows}.php; app/Services/CatalogHistoryService.php ('houses')
  Phần 5: dò code FE/BE + menu (02/11/2026).
Chạy:  python gen_srs.py          (dựng + Word cập nhật mục lục + PDF out/ + tự kiểm)
       python gen_srs.py --no-word (chỉ dựng .docx)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import _lib_win as L  # noqa: E402

TEN = 'Danh mục nhà kho'
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

HINT_SO_DAY = 'Hệ thống tự tạo các dãy "Dãy 1", "Dãy 2"... (mã D1, D2...) cho nhà kho này.'


def ui(header, rows):
    return [header] + [[str(i + 1)] + r for i, r in enumerate(rows)]


# ------------------------------------------------------------------ Phần 5 (dò code 02/11/2026)
P5 = [
    ('Kho', 'Khai báo tồn kho đầu kỳ (chọn vị trí, cột Nhà)', 'Kho => Tồn kho đầu kỳ'),
    ('Kho', 'Phiếu nhập kho (xếp hàng vào vị trí, cột Nhà)', 'Kho => Nhập kho'),
    ('Kho', 'Phiếu điều chuyển vị trí (lọc vị trí theo Nhà)', 'Kho => Điều chuyển'),
    ('Kho', 'Kiểm kê theo vị trí (phạm vi Nhà / Dãy / Khoang)', 'Kho => Kiểm kho => Theo vị trí'),
    ('Kho', 'Thẻ kho (lọc theo Nhà)', 'Kho => Báo cáo kho'),
    ('Kho', 'Báo cáo tồn kho theo vị trí', 'Kho => Báo cáo kho'),
    ('Kho', 'Tổng hợp xuất nhập tồn', 'Kho => Báo cáo kho'),
    ('Kho', 'Kho vật lý (tự sinh nhà kho, cột Số nhà kho)', 'Kho => Danh mục'),
    ('Kho', 'Dãy', 'Kho => Danh mục'),
    ('Kho', 'Khoang', 'Kho => Danh mục'),
    ('Kho', 'Vị trí', 'Kho => Danh mục'),
    ('Tài chính', 'Phiếu nhập kho (xếp hàng vào vị trí, cột Nhà)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
    ('Tài chính', 'Kế hoạch kiểm kê theo vị trí', 'Tài chính => Kiểm kê'),
]

# ------------------------------------------------------------------ dữ liệu SRS
FR = []

# 2.1 Xem danh sách -------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách nhà kho',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang, Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách nhà kho'],
        ['Mô tả', 'Hiển thị các nhà kho thuộc kho vật lý trong phạm vi dữ liệu của người dùng (cả Hoạt động lẫn Khóa), có phân trang, sắp xếp và các nút thao tác theo từng dòng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn Danh mục nhà kho theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), nhà kho tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Người dùng thường chỉ thấy nhà kho thuộc kho vật lý của công ty mình; Super admin thấy nhà kho của mọi công ty (BR-01).\n• Nhà kho thuộc kho vật lý đang Khóa vẫn hiển thị.\n• Không có nhà kho khớp → bảng hiện "Không có dữ liệu phù hợp."'],
    ],
    'anh': [('01_list', 'Màn Danh mục nhà kho lúc mới truy cập')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Danh sách nhà kho', 'Tiêu đề khối danh sách và tiêu đề trang.'],
        ['Nút Tạo mới', 'Button', 'Enable / Ẩn', 'Hiển thị', '- Mở cửa sổ "Tạo mới nhà kho" (mục 2.3).\n- Ẩn khi thiếu quyền "Quản lý kho".'],
        ['Nút Import Excel', 'Button', 'Enable / Ẩn', 'Hiển thị', '- Mở cửa sổ "Import nhà kho" (mục 2.8).\n- Ẩn khi thiếu quyền.'],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất file" (mục 2.9).'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.11).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa, không ẩn được.'],
        ['Cột Mã nhà kho', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sắp xếp được.\n- Chữ dạng liên kết: bấm vào mở cửa sổ "Xem chi tiết nhà kho" (mục 2.10).\n- Cột khóa, không ẩn được.'],
        ['Cột Tên nhà kho', 'Table/Grid', 'Read-only', 'Hiển thị', 'Sắp xếp được. Dài thì xuống tối đa 2 dòng, rê chuột xem đủ.'],
        ['Cột Kho', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên kho vật lý chứa nhà kho (chỉ tên, không kèm mã).'],
        ['Cột Số dãy', 'Table/Grid', 'Read-only', 'Ẩn', 'Số dãy hiện có của nhà kho (mọi trạng thái); nhà chưa có dãy thì để trống. Mặc định ẩn, căn phải.'],
        ['Cột Mô tả', 'Table/Grid', 'Read-only', 'Ẩn', 'Mặc định ẩn.'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng "Họ tên - Mã phòng ban".'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Người cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng "Họ tên - Mã phòng ban".'],
        ['Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Trạng thái', 'Table/Grid', 'Read-only', 'Hiển thị', '- "Hoạt động" nền xanh.\n- "Khóa" nền đỏ.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sửa: nhà kho Hoạt động, có quyền.\n- Xóa: nhà kho Hoạt động, chưa có dãy nào và chưa được chọn trong kế hoạch kiểm kê theo vị trí, có quyền (BR-07).\n- Khóa: nhà kho Hoạt động và không còn dãy Hoạt động; Mở khóa: nhà kho đang Khóa và kho cha Hoạt động (BR-06).\n- Lịch sử: luôn có.\n- Có 4 nút thì hiện 2 nút đầu, các nút còn lại nằm trong nút ba chấm "Hành động khác".\n- Nút không dùng được thì ẩn, không làm mờ. Cột khóa, không ẩn được.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Kiểm tra quyền "Quản lý kho"; thiếu quyền → menu không hiện, mở thẳng màn bị từ chối.\nAfter:\n– Tải trang 1 theo phạm vi công ty (BR-01), nhà kho tạo gần nhất trên cùng.'],
        ['Bấm tiêu đề cột Mã nhà kho / Tên nhà kho / Ngày tạo / Ngày cập nhật', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại từ trang 1.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp, tải lại dữ liệu; đổi số dòng thì quay về trang 1.'],
        ['Bấm Mã nhà kho', 'Click', 'After:\n– Mở cửa sổ "Xem chi tiết nhà kho" (mục 2.10).'],
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách nhà kho'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao: Công ty (chỉ Super admin), Kho, Trạng thái, Người tạo, Ngày tạo.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn Danh mục nhà kho.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô tìm nhanh chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Ô Kho mặc định chỉ liệt kê kho Hoạt động; bấm biểu tượng ổ khóa trên nhãn ô để hiện cả kho đã khóa (BR-11). Ô Công ty có công tắc tương tự.\n• Đổi Công ty → ô Kho bỏ giá trị không thuộc công ty mới.\n• Ngày tạo "Từ" lớn hơn "Đến" → báo đỏ dưới ô, xoá bảng, không tải dữ liệu (BR-10).\n• Bấm Làm mới → xoá mọi điều kiện và tải lại danh sách.\n• Hệ thống ghi nhớ bộ lọc 10 phút khi rời màn rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực tìm kiếm và lọc (đã mở Tìm kiếm nâng cao)')],
    'ui': ui(['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả'], [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', '- Placeholder "Tìm theo mã, tên nhà kho".\n- Tìm gần đúng theo Mã nhà kho, Tên nhà kho, không phân biệt hoa thường.'],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Áp dụng từ khóa và các ô lọc.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá mọi điều kiện lọc và tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực các ô lọc (khi mở, nút đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" chọn ô lọc nào được hiển thị (áp dụng quy tắc chung).'],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Trống', '- Chỉ hiện với Super admin.\n- Lọc nhà kho theo công ty của kho vật lý cha.\n- Biểu tượng ổ khóa trên nhãn: hiện cả công ty đã khóa.'],
        ['Ô Kho', 'Dropdown', 'Enable', 'Kho vật lý trong phạm vi, dạng "Mã - Tên"', 'Trống', '- Mặc định chỉ kho Hoạt động; đã chọn Công ty thì chỉ kho của công ty đó.\n- Biểu tượng ổ khóa trên nhãn: gợi ý "Hiện cả kho đã khoá", bấm để hiện thêm kho đã khóa (kèm biểu tượng khóa), bấm lần nữa để ẩn.'],
        ['Ô Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Trống', 'Bỏ trống thì hiện cả hai trạng thái.'],
        ['Ô Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc nhà kho do người được chọn tạo.'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Một ô chọn khoảng Từ ngày → Đến ngày, tính cả 2 đầu mút.\n- Từ > Đến: báo đỏ "Đến ngày phải lớn hơn hoặc bằng Từ ngày."'],
    ]),
    'ui_widths': [0.45, 1.25, 0.85, 0.8, 1.05, 0.8, 2.6],
    'events': [
        ['Bấm Tìm kiếm / nhấn Enter ở ô tìm nhanh', 'Click', 'After:\n– Áp đồng thời từ khóa và các ô lọc, tải lại bảng từ trang 1.'],
        ['Chọn giá trị ở ô lọc', 'Change', 'During:\n– Ô Công ty: bỏ giá trị ô Kho nếu kho không thuộc công ty vừa chọn.\n– Ô Ngày tạo: Từ > Đến → báo đỏ dưới ô, toast cùng câu, xoá bảng, không tải dữ liệu.\nAfter:\n– Tải lại bảng từ trang 1.'],
        ['Bấm biểu tượng ổ khóa trên nhãn ô Kho / Công ty', 'Click', 'After:\n– Bật: ô liệt kê thêm mục đã khóa (kèm biểu tượng khóa). Tắt: chỉ còn mục Hoạt động; giá trị đang chọn vẫn giữ.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khu vực ô lọc.'],
    ],
})

# 2.3 Thêm mới -------------------------------------------------------------------
FORM_ROWS = [
    ['Kho', 'Dropdown', 'Enable', 'Kho vật lý Hoạt động trong phạm vi, dạng "Mã - Tên"', 'Có', 'Trống', '- Có ô tìm trong danh sách.\n- Bỏ trống: "Bắt buộc phải nhập".\n- Kho vừa bị khóa: "Kho "<Tên kho>" đã bị khóa, vui lòng chọn kho khác" (BR-02).'],
    ['Số dãy', 'Textbox', 'Enable', 'Số nguyên 1–999', 'Có', 'Trống', '- Chỉ nhận chữ số, tối đa 3 ký tự.\n- Icon ⓘ: "' + HINT_SO_DAY + '"\n- Bỏ trống: "Bắt buộc phải nhập"; ngoài khoảng: "Nhập số nguyên từ 1 đến 999" (BR-05).'],
    ['Mã nhà kho', 'Textbox', 'Enable', '1–50 ký tự: chữ không dấu, số, dấu - và _', 'Có', 'Trống', '- Duy nhất trong cùng kho (BR-03).\n- Sai ký tự: báo đỏ ngay khi gõ "Chỉ gồm chữ không dấu, số, dấu - và _".\n- Quá 50 ký tự: "Vui lòng nhập tối đa 50 ký tự."\n- Trùng: "Đã tồn tại trong kho này".'],
    ['Tên nhà kho', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', '- Duy nhất trong cùng kho (BR-04).\n- Ô không cho gõ quá 255 ký tự.\n- Trùng: "Đã tồn tại trong kho này".'],
    ['Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động', 'Có nút × xoá nhanh; để trống thì lưu là Hoạt động.'],
    ['Mô tả', 'Textarea', 'Enable', '0–500 ký tự', 'Không', 'Trống', 'Quá 500 ký tự: "Nhập tối đa 500 ký tự".'],
]
FR.append({
    'ten': 'Thêm mới nhà kho', 'uc': 'uc_them',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Thêm mới nhà kho'],
        ['Mô tả', 'Tạo một nhà kho mới trong một kho vật lý qua cửa sổ nhập liệu; hệ thống tự sinh các dãy cho nhà kho (BR-05).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Có ít nhất một kho vật lý Hoạt động trong phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở cửa sổ "Tạo mới nhà kho", Trạng thái mặc định Hoạt động.\n3. Người dùng chọn Kho, nhập Số dãy, Mã nhà kho, Tên nhà kho (Trạng thái, Mô tả nếu cần) rồi bấm Lưu.\n4. Hệ thống kiểm tra dữ liệu, ghi nhà kho, sinh N dãy "Dãy 1"… "Dãy N" (mã D1… DN).\n5. Ghi nhận Tạo mới trong lịch sử của nhà kho (và của từng dãy sinh kèm).\n6. Đóng cửa sổ, tải lại danh sách, báo "Thêm mới thành công."'],
        ['Dòng sự kiện phụ', '• Thiếu / sai dữ liệu → báo đỏ dưới ô + toast "Bạn chưa nhập đầy đủ thông tin.", cửa sổ không đóng, dữ liệu đã nhập còn nguyên.\n• Bấm "Lưu & Tiếp tục" → lưu rồi giữ cửa sổ, các ô về trống để nhập nhà kho tiếp.\n• Bấm Đóng / (x) / bấm ra ngoài: chưa nhập gì thì đóng; đã nhập thì hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', 'Nút Lưu / Lưu & Tiếp tục bị khóa trong lúc đang lưu để tránh tạo trùng.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': POPUP % 'Tạo mới nhà kho',
    'anh': [('10_create', 'Cửa sổ Tạo mới nhà kho'), ('11_code_error', 'Lỗi định dạng Mã nhà kho báo ngay khi gõ'),
            ('18_unsaved', 'Hộp xác nhận Thông tin chưa lưu khi đóng cửa sổ đã nhập dữ liệu')],
    'ui': ui(UI8, FORM_ROWS + [
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi đóng cửa sổ.'],
        ['Nút Lưu & Tiếp tục', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi giữ cửa sổ, xoá trắng các ô.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ, không lưu (đã nhập thì hỏi xác nhận).'],
        ['Hộp Thông tin chưa lưu', 'Label', 'Enable / Ẩn', '–', '–', 'Ẩn', '- Nội dung "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"\n- Nút Thoát: đóng không lưu; nút Ở lại: quay về cửa sổ.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho" (thiếu quyền thì nút ẩn).\nAfter:\n– Mở cửa sổ với các ô trống, Trạng thái = Hoạt động; ô Kho liệt kê kho Hoạt động trong phạm vi.'],
        ['Gõ Mã nhà kho', 'Change', 'During:\n– Sai ký tự hoặc quá 50 ký tự → báo đỏ ngay dưới ô.'],
        ['Gõ Số dãy', 'Change', 'During:\n– Ký tự không phải chữ số bị loại ngay, ô nhận tối đa 3 chữ số.'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho".\nDuring:\n– Kiểm tra bắt buộc, độ dài, ký tự Mã nhà kho; kho thuộc phạm vi và đang Hoạt động; trùng Mã / Tên nhà kho trong cùng kho; Số dãy 1–999.\n' + TRUOC_LUU + '\nAfter:\n– Ghi nhà kho, sinh N dãy "Dãy i" / mã Di trạng thái Hoạt động.\n– Ghi nhận Tạo mới trong lịch sử (nhà kho và từng dãy).\n– Đóng cửa sổ, tải lại danh sách, báo "Thêm mới thành công."'],
        ['Bấm Lưu & Tiếp tục', 'Click', 'During:\n– Như nút Lưu.\n' + TRUOC_LUU + '\nAfter:\n– Ghi như nút Lưu, giữ cửa sổ, các ô về trống, Trạng thái về Hoạt động.'],
        ['Bấm Đóng / (x) / bấm ra ngoài', 'Click', 'After:\n– Chưa nhập gì → đóng cửa sổ.\n– Đã nhập → hiện hộp "Thông tin chưa lưu": Thoát thì đóng không lưu, Ở lại thì quay về cửa sổ.'],
    ],
})

# 2.4 Chỉnh sửa ------------------------------------------------------------------
EDIT_ROWS = [
    ['Kho', 'Dropdown', 'Disable', 'Kho hiện tại', 'Không', 'Dữ liệu hiện tại', '- Không đổi được kho của nhà kho đã tạo (ô xám, không có dấu *).\n- Kho đã bị khóa vẫn hiện đúng tên kèm biểu tượng khóa.'],
    ['Số dãy', 'Textbox', 'Enable / Disable', 'Số nguyên 1–999', 'Có / Không', 'Số dãy hiện có / Trống',
     '- Nhà đã có dãy: ô xám hiện số dãy hiện có, không sửa được, không sinh thêm dãy.\n- Nhà CHƯA có dãy: ô mở, bắt buộc nhập, icon ⓘ "' + HINT_SO_DAY + '"; lưu xong sinh N dãy (BR-05).'],
    FORM_ROWS[2][:5] + ['Dữ liệu hiện tại', FORM_ROWS[2][6]],
    FORM_ROWS[3][:5] + ['Dữ liệu hiện tại', FORM_ROWS[3][6]],
    ['Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Không', 'Dữ liệu hiện tại',
     '- Nhà còn dãy Hoạt động: ô bị khóa ở Hoạt động.\n- Chọn Khóa rồi Lưu = khóa nhà kho (BR-06).'],
    FORM_ROWS[5][:5] + ['Dữ liệu hiện tại', FORM_ROWS[5][6]],
]
FR.append({
    'ten': 'Chỉnh sửa nhà kho', 'uc': 'uc_sua',
    'qtc': 'Validate dữ liệu, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chỉnh sửa nhà kho'],
        ['Mô tả', 'Sửa Mã, Tên, Trạng thái, Mô tả của nhà kho đang Hoạt động; nhà chưa có dãy thì nhập Số dãy để sinh dãy. Không đổi được Kho.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Nhà kho đang Hoạt động và thuộc phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Sửa ở cột Hành động.\n2. Hệ thống mở cửa sổ "Sửa nhà kho" với dữ liệu hiện tại.\n3. Người dùng sửa và bấm Lưu.\n4. Hệ thống kiểm tra, ghi thay đổi; nhà chưa có dãy thì sinh N dãy theo Số dãy vừa nhập.\n5. Ghi nhận Thay đổi thông tin (đổi Trạng thái ghi riêng Khóa) trong lịch sử.\n6. Đóng cửa sổ, báo "Cập nhật thành công."'],
        ['Dòng sự kiện phụ', '• Giữ nguyên Mã / Tên của chính nhà kho → không báo trùng.\n• Chọn Trạng thái Khóa cho nhà còn dãy Hoạt động (ô đã khóa trên giao diện; nếu dữ liệu vừa đổi) → báo "Không thể khóa nhà kho khi vẫn còn danh mục con đang hoạt động."\n• Nhà kho vừa bị người khác khóa / xóa → báo "Dữ liệu đã thay đổi, vui lòng tải lại".\n• Bấm Đóng khi đã sửa → hỏi "Thông tin chưa lưu".'],
    ],
    'menu_them': ' => Sửa {icon:btn_sua}',
    'ghi_chu_layout': POPUP % 'Sửa nhà kho',
    'anh': [('12_edit', 'Cửa sổ Sửa nhà kho đã có dãy (Kho, Số dãy, Trạng thái bị khóa)'),
            ('12b_edit_norows', 'Cửa sổ Sửa nhà kho chưa có dãy (ô Số dãy mở để nhập)')],
    'ui': ui(UI8, EDIT_ROWS + [
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu thay đổi rồi đóng cửa sổ.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng không lưu (đã sửa thì hỏi xác nhận). Cửa sổ Sửa không có nút Lưu & Tiếp tục.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện khi nhà kho Hoạt động và người dùng có quyền.\nAfter:\n– Tải dữ liệu nhà kho, mở cửa sổ; nhà kho không còn (vừa bị xoá / ngoài phạm vi) → báo "Dữ liệu đã thay đổi, vui lòng tải lại".'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền, nhà kho phải đang Hoạt động.\nDuring:\n– Kiểm tra như Thêm mới (bỏ qua trùng với chính nhà kho, giữ nguyên Kho); nhà chưa có dãy thì Số dãy bắt buộc 1–999; nhà còn dãy Hoạt động thì không được chọn Khóa.\n' + TRUOC_LUU + '\nAfter:\n– Ghi thay đổi; nhà chưa có dãy thì sinh N dãy (ghi lịch sử Tạo mới cho từng dãy).\n– Ghi nhận Thay đổi thông tin / Khóa trong lịch sử.\n– Đóng cửa sổ, tải lại danh sách, báo "Cập nhật thành công."'],
        ['Bấm Đóng / (x) / bấm ra ngoài', 'Click', 'After:\n– Chưa đổi gì → đóng; đã đổi → hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
    ],
})

# 2.5 Xóa ---------------------------------------------------------------------------
FR.append({
    'ten': 'Xóa nhà kho', 'uc': 'uc_xoa',
    'qtc': 'Quy tắc Xóa, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xóa nhà kho'],
        ['Mô tả', 'Xóa hẳn nhà kho đang Hoạt động, chưa có dãy nào và chưa được chọn trong kế hoạch kiểm kê theo vị trí (BR-07).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Nhà kho đang Hoạt động, chưa có dãy, chưa được dùng ở kế hoạch kiểm kê theo vị trí.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Xóa ở cột Hành động.\n2. Hệ thống hiện hộp "Xác nhận xóa": "Bạn có chắc muốn xóa nhà kho \'<Tên nhà kho>\'?"\n3. Người dùng bấm Xóa.\n4. Hệ thống ghi nhận Xóa trong lịch sử rồi xóa hẳn nhà kho.\n5. Tải lại danh sách, báo "Xóa thành công."'],
        ['Dòng sự kiện phụ', '• Bấm Hủy → đóng hộp, không thay đổi.\n• Nhà kho vừa bị khóa → "Không thể xóa nhà kho đang ở trạng thái khóa. Hãy mở khóa trước."\n• Nhà kho vừa có dãy / vừa được chọn trong kế hoạch kiểm kê → "Không thể xóa do dữ liệu đang được sử dụng."\n• Nhà kho vừa bị người khác xóa → "Dữ liệu đã thay đổi, vui lòng tải lại".'],
    ],
    'menu_them': ' => Xóa {icon:btn_xoa}',
    'ghi_chu_layout': POPUP % 'Xác nhận xóa',
    'anh': [('13_delete', 'Hộp xác nhận xóa nhà kho')],
    'ui': ui(UI4, [
        ['Nút Xóa (cột Hành động)', 'Button', 'Biểu tượng thùng rác; chỉ hiện khi nhà kho Hoạt động, chưa có dãy, chưa được chọn trong kế hoạch kiểm kê theo vị trí và người dùng có quyền.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận xóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn xóa nhà kho \'<Tên nhà kho>\'?"'],
        ['Nút Xóa', 'Button', 'Xác nhận xóa.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không xóa.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Xóa ở cột Hành động', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên nhà kho.'],
        ['Bấm Xóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền, nhà kho thuộc phạm vi.\nDuring:\n– Nhà kho phải đang Hoạt động, không có dãy, chưa được chọn trong kế hoạch kiểm kê theo vị trí.\n' + TRUOC_LUU + '\nAfter:\n– Ghi nhận Xóa trong lịch sử, xóa hẳn nhà kho.\n– Tải lại danh sách, báo "Xóa thành công."'],
        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.6 Khóa / Mở khóa -----------------------------------------------------------
FR.append({
    'ten': 'Khóa / Mở khóa nhà kho', 'uc': 'uc_khoa',
    'qtc': 'Quy tắc Khóa/Mở khóa, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Khóa / Mở khóa nhà kho'],
        ['Mô tả', 'Đổi trạng thái nhà kho giữa Hoạt động và Khóa. Phải khóa (hoặc xóa) hết dãy Hoạt động trước khi khóa nhà; chỉ mở khóa được khi kho cha đang Hoạt động (BR-06).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Khóa: nhà kho Hoạt động và không còn dãy Hoạt động. Mở khóa: nhà kho đang Khóa, kho cha Hoạt động.'],
        ['Dòng sự kiện chính', '1. Người dùng chọn Khóa (hoặc Mở khóa) ở cột Hành động.\n2. Hệ thống hiện hộp "Xác nhận khóa" / "Xác nhận mở khóa" kèm tên nhà kho.\n3. Người dùng bấm Khóa / Mở khóa.\n4. Hệ thống đổi trạng thái, ghi nhận Khóa / Mở khóa trong lịch sử.\n5. Tải lại danh sách, báo "Khóa thành công." / "Mở khóa thành công."'],
        ['Dòng sự kiện phụ', '• Bấm Hủy → không thay đổi.\n• Dãy vừa được mở khóa lại → "Không thể khóa nhà kho khi vẫn còn danh mục con đang hoạt động."\n• Kho cha vừa bị khóa → "Không thể mở khóa nhà kho khi danh mục cha đang bị khóa."\n• Nhà kho đã bị người khác đổi trạng thái → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n• Sau khi Khóa: nút Sửa, Xóa ẩn; sau khi Mở khóa: nút Sửa hiện lại.'],
    ],
    'menu_them': ' => Khóa {icon:btn_khoa_row} / Mở khóa {icon:btn_mokhoa_row}',
    'ghi_chu_layout': POPUP % 'Xác nhận khóa / Xác nhận mở khóa',
    'anh': [('14_lock', 'Hộp xác nhận khóa nhà kho'), ('15_unlock', 'Hộp xác nhận mở khóa nhà kho')],
    'ui': ui(UI4, [
        ['Nút Khóa (cột Hành động)', 'Button', '- Biểu tượng ổ khóa; hiện khi nhà kho Hoạt động, không còn dãy Hoạt động, có quyền.\n- Dòng có nút Xóa thì Khóa nằm trong nút ba chấm "Hành động khác".'],
        ['Nút Mở khóa (cột Hành động)', 'Button', 'Biểu tượng ổ khóa mở; hiện khi nhà kho đang Khóa, kho cha Hoạt động, có quyền.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận khóa" hoặc "Xác nhận mở khóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn khóa nhà kho \'<Tên nhà kho>\'?" / "Bạn có chắc muốn mở khóa nhà kho \'<Tên nhà kho>\'?"'],
        ['Nút Khóa / Mở khóa', 'Button', 'Xác nhận đổi trạng thái.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không thay đổi.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Chọn Khóa / Mở khóa', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên nhà kho.'],
        ['Bấm Khóa / Mở khóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền, nhà kho thuộc phạm vi.\nDuring:\n– Nhà kho đã ở trạng thái đích → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n– Khóa mà còn dãy Hoạt động → "Không thể khóa nhà kho khi vẫn còn danh mục con đang hoạt động."\n– Mở khóa mà kho cha đang Khóa → "Không thể mở khóa nhà kho khi danh mục cha đang bị khóa."\n' + TRUOC_LUU + '\nAfter:\n– Đổi trạng thái, ghi nhận Khóa / Mở khóa trong lịch sử, tải lại danh sách, báo thành công.'],
        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.7 Lịch sử --------------------------------------------------------------------
FR.append({
    'ten': 'Xem lịch sử thay đổi',
    'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem lịch sử thay đổi nhà kho'],
        ['Mô tả', 'Liệt kê các lần thao tác trên một nhà kho (Tạo mới, Thay đổi thông tin, Khóa, Mở khóa, Xóa), mới nhất ở trên, kèm người thực hiện, thời điểm, giá trị cũ → mới.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Lịch sử ở cột Hành động (hoặc Xem lịch sử trong cửa sổ Xem chi tiết).\n2. Hệ thống mở cửa sổ "Lịch sử thay đổi: <Tên nhà kho>" và liệt kê các mốc.'],
        ['Dòng sự kiện phụ', '• Lọc theo Loại hành động (Tạo mới / Thay đổi thông tin / Thay đổi trạng thái), Người thực hiện, Từ ngày / Đến ngày bằng nút Bộ lọc trong cửa sổ.\n• Các trường được ghi: Mã nhà kho, Tên nhà kho, Kho (bằng tên kho), Mô tả, Trạng thái.\n• Nhà kho sinh tự động khi tạo kho vật lý cũng có mốc Tạo mới.'],
    ],
    'menu_them': ' => Lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': POPUP % 'Lịch sử thay đổi',
    'anh': [('16_history', 'Cửa sổ Lịch sử thay đổi của nhà kho')],
    'ui': ui(UI6, [
        ['Nút Lịch sử (cột Hành động)', 'Button', 'Enable', 'Hiển thị', 'Luôn có ở mọi dòng (kể cả nhà kho Khóa); dòng có 4 nút thì nằm trong nút ba chấm.'],
        ['Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Lịch sử thay đổi: <Tên nhà kho>', ''],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Mở các ô lọc Loại hành động, Người thực hiện, Từ ngày, Đến ngày.'],
        ['Danh sách mốc', 'Table/Grid', 'Read-only', 'Theo dữ liệu', '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, loại hành động, "Người thực hiện: Họ tên — Phòng ban".\n- Dòng thay đổi: "<Trường>: giá trị cũ → giá trị mới".\n- Chưa có dữ liệu: "Chưa có lịch sử thao tác nào."'],
        ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lịch sử', 'Click', 'After:\n– Tải lịch sử của nhà kho, mới nhất trên cùng.'],
        ['Chọn điều kiện ở Bộ lọc', 'Change', 'After:\n– Lọc lại các mốc; không có mốc khớp → "Không có lịch sử phù hợp bộ lọc."'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.8 Import ---------------------------------------------------------------------
FR.append({
    'ten': 'Import nhà kho từ file Excel', 'uc': 'uc_import',
    'qtc': 'Quy tắc Import file, Validate dữ liệu, Thông báo.',
    'gioi_thieu': [
        ['Tên chức năng', 'Import nhà kho từ file Excel'],
        ['Mô tả', 'Tạo nhiều nhà kho từ file Excel theo file mẫu. Kho cha nhập bằng mã kho; mỗi dòng được kiểm tra và ghi như khi Tạo mới (sinh dãy, ghi lịch sử) (BR-08).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Import Excel, hệ thống mở cửa sổ "Import nhà kho".\n2. Bấm Tải file mẫu (Mau_import_nha_kho.xlsx), điền dữ liệu.\n3. Bấm Chọn file Excel, chọn file, bấm Load lên bảng: dữ liệu hiện ở bảng xem trước, ô Tổng = số dòng.\n4. Bấm Validate: hệ thống kiểm tra từng dòng (chưa ghi dữ liệu), hiện Tổng / Hợp lệ / Lỗi; dòng lỗi tô đỏ kèm lý do, dòng hợp lệ bị khóa.\n5. Sửa dòng lỗi rồi Validate lại, hoặc bấm Bỏ dòng lỗi.\n6. Khi không còn dòng lỗi, bấm Import: hệ thống ghi từng dòng, ghi nhận Tạo mới trong lịch sử, báo "Import thành công N nhà kho.", tải lại danh sách.'],
        ['Dòng sự kiện phụ', '• File quá 500 dòng dữ liệu → "File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần."\n• Dòng vừa bị trùng với nhà kho người khác tạo trong lúc Import → bị bỏ qua, bảng kết quả "Import xong: a dòng thành công, b dòng lỗi bị bỏ qua" (nút Sao chép).\n• Bấm Xoá trạng thái validate để sửa lại cả dòng đã khóa.\n• Bấm Làm mới để làm lại từ đầu; Đóng để thoát.'],
    ],
    'menu_them': ' => Import Excel {icon:btn_import}',
    'ghi_chu_layout': POPUP % 'Import nhà kho',
    'anh': [('21_import_open', 'Cửa sổ Import nhà kho khi vừa mở'), ('22_import_loaded', 'Dữ liệu sau khi Load lên bảng'),
            ('23_import_validated', 'Kết quả Validate — dòng lỗi nêu rõ lý do')],
    'ui': ui(UI7I, [
        ['Nút Chọn file Excel', 'Button', 'Enable', '–', '–', 'Chọn file .xlsx, hiện tên file bên cạnh.'],
        ['Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Tải Mau_import_nha_kho.xlsx: dòng 1 tên cột (cột bắt buộc có *), dòng 2 hướng dẫn, 2 dòng dữ liệu mẫu.'],
        ['Nút Load lên bảng', 'Button', 'Enable / Disable', '–', 'Disable', 'Bấm được khi đã chọn file; đọc file lên bảng xem trước.'],
        ['Nút Validate', 'Button', 'Enable / Disable', '–', 'Disable', 'Bấm được khi bảng có dữ liệu; kiểm tra từng dòng, chưa ghi dữ liệu.'],
        ['Nút Import', 'Button', 'Enable / Disable', '–', 'Disable', 'Chỉ bấm được khi đã Validate, còn ≥ 1 dòng hợp lệ và KHÔNG còn dòng lỗi.'],
        ['Ô Tổng / Hợp lệ / Lỗi', 'Label', 'Read-only', '–', 'Tổng: 0', 'Tổng hiện sau Load; Hợp lệ, Lỗi hiện sau Validate.'],
        ['Cột Mã kho *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Mã kho vật lý trong phạm vi của người nhập; kho đang Khóa bị báo lỗi như popup Tạo mới.'],
        ['Cột Mã nhà kho *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Chữ không dấu, số, dấu - và _, tối đa 50 ký tự, không trùng trong kho (cả trong file).'],
        ['Cột Tên nhà kho *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Tối đa 255 ký tự, không trùng trong kho (cả trong file).'],
        ['Cột Số dãy *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Số nguyên 1–999; tự sinh Dãy 1..N như khi tạo tay.'],
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
        ['Bấm Validate', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho".\nDuring:\n– Mỗi dòng kiểm như Tạo mới; mã kho không tồn tại / ngoài phạm vi ("Không tồn tại kho có mã "<mã>""); trùng Mã / Tên nhà kho trong cùng kho giữa các dòng của file ("Bị trùng trong file").\nAfter:\n– Hiện Tổng / Hợp lệ / Lỗi, toast "Validate xong: X hợp lệ, Y không hợp lệ" (hoặc "Validate thành công"); dòng lỗi tô đỏ kèm lý do theo thứ tự cột, dòng hợp lệ bị khóa.'],
        ['Bấm Import', 'Click', 'Before:\n– Đã Validate, không còn dòng lỗi.\nDuring:\n– Hệ thống kiểm lại từng dòng ngay trước khi ghi.\n' + TRUOC_LUU + '\nAfter:\n– Ghi từng dòng như Tạo mới (sinh dãy), ghi nhận Tạo mới trong lịch sử.\n– Báo "Import thành công N nhà kho.", đóng cửa sổ, tải lại danh sách; có dòng bị bỏ qua thì hiện bảng kết quả.'],
        ['Bấm Bỏ dòng lỗi / Xoá trạng thái validate', 'Click', 'After:\n– Bỏ dòng lỗi khỏi bảng / mở khóa các dòng để sửa.'],
        ['Bấm Đóng / Làm mới', 'Click', 'After:\n– Đóng cửa sổ / xoá dữ liệu đang xem để làm lại.'],
    ],
})

# 2.9 Xuất Excel -------------------------------------------------------------------
FR.append({
    'ten': 'Xuất danh sách ra Excel', 'uc': 'uc_xuat',
    'qtc': 'Quy tắc Excel, Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách nhà kho ra Excel'],
        ['Mô tả', 'Xuất toàn bộ nhà kho khớp bộ lọc đang áp dụng (mọi trang) ra file Excel, người dùng chọn trường và thứ tự cột (BR-09).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng lọc danh sách (nếu cần), bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất file", tích sẵn các cột đang hiện trên bảng.\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự rồi bấm Xuất file.\n4. Hệ thống tải file danh_sach_nha_kho.xlsx, báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Kết quả rỗng vẫn xuất file (tiêu đề + tên cột).\n• Ô Ngày tạo đang sai (Từ > Đến) → báo lỗi, không xuất.\n• Lỗi hệ thống → "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': POPUP % 'Chọn trường xuất file',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất file')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '"Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file."'],
        ['Danh sách trường', 'Table/Grid', 'Enable', 'Tích theo cột đang hiện', '10 trường: Mã nhà kho, Tên nhà kho, Kho, Số dãy, Mô tả, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. Mỗi trường có ô tích và biểu tượng ☰ kéo đổi vị trí.'],
        ['Nút Chọn tất cả', 'Button', 'Enable', '–', 'Tích mọi trường.'],
        ['Nút Bỏ chọn hết', 'Button', 'Enable', '–', 'Bỏ tích mọi trường.'],
        ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn x/10 trường', ''],
        ['Nút Xuất file', 'Button', 'Enable / Disable', 'Enable', 'Tải file; không bấm được khi không còn trường nào được chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ, không xuất.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ, tích sẵn theo cột đang hiện.'],
        ['Bấm Xuất file', 'Click', 'During:\n– Ô Ngày tạo sai → báo "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", không xuất.\n' + TRUOC_LUU + '\nAfter:\n– Tải file danh_sach_nha_kho.xlsx: tiêu đề "Danh sách nhà kho", cột theo thứ tự đã chọn, mọi dòng khớp bộ lọc; báo "Xuất Excel thành công".'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.10 Xem chi tiết ----------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết nhà kho', 'uc': 'uc_xem',
    'qtc': 'Màn Xem chi tiết, Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết nhà kho'],
        ['Mô tả', 'Xem toàn bộ thông tin một nhà kho ở chế độ chỉ đọc, kèm khối Lịch sử.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm vào Mã nhà kho trên bảng.\n2. Hệ thống mở cửa sổ "Xem chi tiết nhà kho", mọi ô chỉ đọc.\n3. Bấm Xem lịch sử để mở khối Lịch sử ngay trong cửa sổ.'],
        ['Dòng sự kiện phụ', '• Nhà kho vừa bị xoá / ngoài phạm vi → báo "Dữ liệu đã thay đổi, vui lòng tải lại", không mở cửa sổ.\n• Nhà kho đang Khóa vẫn xem được.'],
    ],
    'menu_them': ' => Bấm Mã nhà kho',
    'ghi_chu_layout': POPUP % 'Xem chi tiết nhà kho',
    'anh': [('17_detail', 'Cửa sổ Xem chi tiết nhà kho ở chế độ chỉ đọc'),
            ('17b_detail_history', 'Khối Lịch sử trong cửa sổ Xem chi tiết')],
    'ui': ui(UI6, [
        ['Kho', 'Dropdown', 'Read-only', 'Dữ liệu hiện tại', 'Dạng "Mã kho - Tên kho"; kho đã khóa kèm biểu tượng khóa. Không có dấu (*).'],
        ['Số dãy', 'Textbox', 'Read-only', 'Số dãy hiện có', ''],
        ['Mã nhà kho, Tên nhà kho', 'Textbox', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Trạng thái', 'Dropdown', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Mô tả', 'Textarea', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Khối Lịch sử', 'Table/Grid', 'Enable', 'Thu gọn', '- Nút Xem lịch sử mở khối, hiện số mốc.\n- Nút Làm mới tải lại, Thu gọn đóng khối, Bộ lọc lọc mốc như mục 2.7.'],
        ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ. Không có nút Lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Mã nhà kho', 'Click', 'After:\n– Tải dữ liệu, mở cửa sổ chỉ đọc.'],
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
        ['Dòng sự kiện phụ', '• Cột STT, Mã nhà kho, Hành động là cột khóa: không bỏ tích được.\n• Bấm Đóng → bỏ các thay đổi vừa chỉnh.'],
    ],
    'menu_them': ' => Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': POPUP % 'Tuỳ chỉnh cột',
    'anh': [('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột — STT, Mã nhà kho, Hành động bị khóa')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '"Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng."'],
        ['Danh sách cột', 'Table/Grid', 'Enable', 'Theo cấu hình đã lưu', '12 cột theo thứ tự trên bảng. Mặc định ẩn: Số dãy, Mô tả.'],
        ['Cột khóa', 'Table/Grid', 'Disable', 'Luôn tích', 'STT, Mã nhà kho, Hành động: ô tích xám, không ẩn được.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Tích / bỏ tích mọi cột (trừ cột khóa).'],
        ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn x/12 cột', ''],
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
    'menu': [('Kho', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Nhà kho', 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu chức năng.',
        'Làm rõ phạm vi dữ liệu theo công ty của kho vật lý cha, ràng buộc trùng Mã / Tên nhà kho trong cùng kho, dãy tự sinh theo Số dãy, điều kiện Khóa (không còn dãy Hoạt động), Mở khóa (kho cha Hoạt động) và Xóa (chưa có dãy, chưa dùng ở kiểm kê).',
    ],
    'thuat_ngu': [
        ['Kho vật lý', 'Kho hàng thực tế, cấp gốc của cây kho: Kho vật lý → Nhà kho → Dãy → Khoang → Vị trí. Là "kho cha" của nhà kho.'],
        ['Nhà kho', 'Cấp con trực tiếp của kho vật lý; khi tạo kho vật lý hệ thống tự sinh "Nhà 1"… "Nhà N" (mã N1…NN).'],
        ['Dãy', 'Cấp con trực tiếp của nhà kho; khi tạo nhà kho hệ thống tự sinh "Dãy 1"… "Dãy N" (mã D1…DN).'],
        ['Kế hoạch kiểm kê theo vị trí', 'Phiếu lên kế hoạch kiểm kê, có phạm vi chọn theo Nhà / Dãy / Khoang / Vị trí; nhà kho đã được chọn ở đây coi là đã được dùng.'],
        ['Hoạt động', 'Trạng thái nhà kho dùng được ở các màn nghiệp vụ.'],
        ['Khóa', 'Nhà kho vẫn nằm trong danh mục, xem được lịch sử nhưng không còn chọn được ở các ô chọn nhà kho.'],
        ['Super admin', 'Tài khoản quản trị cao nhất, xem được nhà kho của mọi công ty.'],
    ],
    'quyen_truoc': ['Màn hình dùng một quyền duy nhất "Quản lý kho" (nhóm Danh mục kho) cho cả xem lẫn thao tác; quyền này dùng chung cho 7 màn Danh mục của phân hệ Kho. Quyền được gán vào vai trò theo công ty.'],
    'quyen_rows': [['Quản lý kho', 'Xem danh sách, tìm kiếm, xem chi tiết, lịch sử, tùy chỉnh cột, xuất Excel; Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Import Excel.']],
    'ma_tran': [['Chức năng', 'Quản lý kho', 'Không có quyền']] + [[f, 'Có', 'Không'] for f in [
        'FR-01 Xem danh sách nhà kho', 'FR-02 Tìm kiếm và lọc', 'FR-03 Thêm mới nhà kho', 'FR-04 Chỉnh sửa nhà kho',
        'FR-05 Xóa nhà kho', 'FR-06 Khóa / Mở khóa nhà kho', 'FR-07 Xem lịch sử thay đổi',
        'FR-08 Import nhà kho từ file Excel', 'FR-09 Xuất danh sách ra Excel', 'FR-10 Xem chi tiết nhà kho',
        'FR-11 Tùy chỉnh cột hiển thị']],
    'ma_tran_widths': [2.6, 1.2, 1.2],
    'quyen_sau': ['Phạm vi dữ liệu: người dùng thường chỉ thấy và thao tác nhà kho thuộc kho vật lý của công ty mình; Super admin thấy nhà kho của mọi công ty và có thêm ô lọc Công ty (BR-01).'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Phạm vi dữ liệu theo công ty', [
            '– Người dùng thường chỉ thấy, xem, sửa, khóa, xóa, xuất nhà kho thuộc kho vật lý có công ty sở hữu = công ty đang làm việc của mình.',
            '– Super admin thấy nhà kho mọi công ty, có thêm ô lọc Công ty.',
            '– Không xác định được công ty của người dùng → không thấy nhà kho nào.',
            '– Thao tác trên nhà kho ngoài phạm vi bị từ chối như dữ liệu không tồn tại.'], ['Xem danh sách', 'Xuất Excel', 'Chỉnh sửa', 'Xóa', 'Khóa / Mở khóa']),
        ('BR-02', 'Kho cha', [
            '– Bắt buộc khi tạo; chỉ chọn được kho vật lý Hoạt động trong phạm vi (dạng "Mã kho - Tên kho").',
            '– Kho vừa bị khóa → "Kho "<Tên kho>" đã bị khóa, vui lòng chọn kho khác"; kho ngoài phạm vi → "Kho không tồn tại".',
            '– Không đổi được kho sau khi tạo (ô Kho ở cửa sổ Sửa bị khóa).',
            '– Nhà kho thuộc kho đã khóa vẫn hiển thị trong danh sách; ô Kho hiện đúng tên kèm biểu tượng khóa.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-03', 'Mã nhà kho', [
            '– Bắt buộc, 1–50 ký tự, chỉ gồm chữ không dấu, số, dấu - và _; cắt khoảng trắng đầu / cuối.',
            '– Duy nhất TRONG CÙNG KHO (so cả nhà kho đang Khóa); khác kho thì được trùng.',
            '– Giữ nguyên chữ hoa / thường người dùng nhập.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-04', 'Tên nhà kho', ['– Bắt buộc, tối đa 255 ký tự, duy nhất trong cùng kho như Mã nhà kho.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-05', 'Số dãy và dãy tự sinh', [
            '– Số nguyên từ 1 đến 999.',
            '– Tạo nhà kho: sinh N dãy "Dãy 1"… "Dãy N", mã D1… DN, trạng thái Hoạt động; mỗi dãy có lịch sử Tạo mới.',
            '– Sửa nhà kho CHƯA có dãy: Số dãy bắt buộc, lưu xong sinh dãy như trên (đúng 1 lần).',
            '– Sửa nhà kho ĐÃ có dãy: ô Số dãy chỉ hiển thị số hiện có, không sinh thêm (thêm dãy ở màn Dãy).'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-06', 'Điều kiện Khóa / Mở khóa', [
            '– Chỉ khóa được nhà kho đang Hoạt động và KHÔNG còn dãy Hoạt động; áp dụng cả khi đổi Trạng thái trong cửa sổ Sửa.',
            '– Chỉ mở khóa được khi kho cha đang Hoạt động.',
            '– Nhà kho đang Khóa: ẩn Sửa, Xóa; không còn trong ô chọn Nhà kho ở các màn khác (Dãy, Khoang, Vị trí, Kế hoạch kiểm kê…).'], ['Khóa / Mở khóa', 'Chỉnh sửa']),
        ('BR-07', 'Điều kiện và cách Xóa', [
            '– Chỉ xóa nhà kho đang Hoạt động, CHƯA có dãy nào (kể cả dãy đã khóa) và chưa được chọn trong kế hoạch kiểm kê theo vị trí.',
            '– Xóa hẳn; mốc Xóa được ghi vào lịch sử trước khi xóa. Mã, tên dùng lại được sau khi xóa.'], ['Xóa']),
        ('BR-08', 'Import', [
            '– Mỗi dòng kiểm và ghi như Tạo mới (BR-02 → BR-05), kho cha nhập bằng mã kho.',
            '– Trùng Mã / Tên nhà kho trong cùng kho giữa các dòng của file → "Bị trùng trong file".',
            '– Tối đa 500 dòng dữ liệu mỗi lần; chỉ Import khi đã Validate và không còn dòng lỗi.'], ['Import']),
        ('BR-09', 'Xuất Excel', ['– Xuất mọi dòng khớp bộ lọc đang áp dụng (không chỉ trang đang xem), cột theo thứ tự người dùng chọn; tên file danh_sach_nha_kho.xlsx.'], ['Xuất Excel']),
        ('BR-10', 'Lọc Ngày tạo', ['– Ngày tạo Từ lớn hơn Đến → báo đỏ "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", xoá bảng, không tải dữ liệu và không xuất Excel.'], ['Tìm kiếm và lọc', 'Xuất Excel']),
        ('BR-11', 'Ô lọc Kho / Công ty có công tắc ổ khóa', [
            '– Mặc định ô chỉ liệt kê mục Hoạt động; bật công tắc ổ khóa trên nhãn để hiện thêm mục đã khóa (kèm biểu tượng khóa).',
            '– Bộ lọc đã lưu đang trỏ tới kho đã khóa vẫn hiện đúng tên.'], ['Tìm kiếm và lọc']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây chọn, lọc hoặc hiển thị dữ liệu Nhà kho; nhà kho đang Khóa không còn chọn được ở các ô chọn nhà kho.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng có quyền "Quản lý kho"',
    'mains': [('FR-01', 'Xem danh sách nhà kho', 'view'), ('FR-03', 'Thêm mới nhà kho', 'crud'),
              ('FR-04', 'Chỉnh sửa nhà kho', 'crud'), ('FR-05', 'Xóa nhà kho', 'action'),
              ('FR-06', 'Khóa / Mở khóa nhà kho', 'action'), ('FR-08', 'Import nhà kho từ file Excel', 'io'),
              ('FR-09', 'Xuất danh sách nhà kho ra Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc nhà kho', 'view'), ('FR-10', 'Xem chi tiết nhà kho', 'view'),
             ('FR-11', 'Tùy chỉnh cột hiển thị', 'view'), ('FR-07', 'Xem lịch sử thay đổi', 'view')],
    'rieng': [('FR-03', 'Thêm mới nhà kho', 'crud', 'uc_them'), ('FR-04', 'Chỉnh sửa nhà kho', 'crud', 'uc_sua'),
              ('FR-05', 'Xóa nhà kho', 'action', 'uc_xoa'), ('FR-06', 'Khóa / Mở khóa nhà kho', 'action', 'uc_khoa'),
              ('FR-08', 'Import nhà kho từ file Excel', 'io', 'uc_import'),
              ('FR-09', 'Xuất danh sách nhà kho ra Excel', 'io', 'uc_xuat'), ('FR-10', 'Xem chi tiết nhà kho', 'view', 'uc_xem')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)

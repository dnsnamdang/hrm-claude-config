# -*- coding: utf-8 -*-
"""SRS - Danh mục dãy (form Danh mục quốc gia, TPE duyệt) — chép khuôn màn mẫu docs/warehouses/gen_srs.py (đã duyệt
02/11/2026), chỉ đổi dữ liệu + phần riêng của màn Dãy.

Nguồn (code HRM hiện tại):
  FE hrm-client/pages/warehouse/rows/{index.vue, AddRowModal.vue}, utils/mixins/{vehicleCatalogScreenMixin,
     vehicleCatalogModalMixin, warehouseCatalogModalMixin, warehouseCatalogImportMixin, createdRangeFilterMixin,
     warehouseLockedFilterMixin}.js, components/warehouse-catalog/LockableFilterSelect.vue,
     utils/warehouse-catalog-import.js, components/subsystem-menu/warehouse.js
  BE Modules/MasterData: Entities/Warehouse/Row.php, Http/Controllers/V1/Warehouse/{RowController,
     WarehouseTreeCatalogController}.php, ProductClassification/BaseCatalogController.php,
     Http/Requests/Warehouse/RowRequest.php, Services/Warehouse/{RowService, WarehouseCatalogScope,
     Concerns/ImportsWarehouseCatalogRows, Concerns/SearchesCodeNameOnly}.php, Transformers/Warehouse/RowResource.php
  Phần 5: dò code FE/BE + menu (02/11/2026).
Chạy:  python gen_srs.py          (dựng + Word cập nhật mục lục + PDF out/ + tự kiểm)
       python gen_srs.py --no-word (chỉ dựng .docx)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import _lib_win as L  # noqa: E402

TEN = 'Danh mục dãy'
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

HINT_KHOANG = ('Số khoang của dãy này. Khi lưu, hệ thống tự tạo các khoang "Khoang 1", "Khoang 2"... (mã K1, K2...). '
               'Chỉ nhập được khi dãy chưa có khoang nào; sau đó muốn thêm, sửa hay khoá khoang thì làm ở màn Khoang.')
HINT_VITRI = ('Số vị trí (tầng) tạo sẵn trong MỖI khoang của dãy: "Tầng 1", "Tầng 2"..., mã <Mã kho>-<Mã nhà>-<Mã dãy>-'
              'K<số khoang>-T<số tầng>. Tổng số vị trí tạo ra = Số khoang × Số vị trí mỗi khoang, tối đa 10,000. '
              'Sau khi tạo, thêm/bớt vị trí làm ở màn Vị trí.')
LOI_TONG = 'Tổng số vị trí sinh ra (số khoang × số vị trí mỗi khoang) tối đa 10,000'
LOI_TRUNG_VT = 'Mã vị trí sinh ra đã tồn tại trong kho: <tối đa 3 mã>. Hãy đổi mã dãy'
LOI_DAI_VT = 'Mã vị trí sinh ra (<mã>) dài quá 50 ký tự. Hãy rút ngắn mã dãy'


def ui(header, rows):
    return [header] + [[str(i + 1)] + r for i, r in enumerate(rows)]


# ------------------------------------------------------------------ Phần 5 (dò code 02/11/2026)
P5 = [
    ('Kho', 'Khai báo tồn kho đầu kỳ (cột Dãy ở ô chọn vị trí)', 'Kho => Tồn kho đầu kỳ'),
    ('Kho', 'Phiếu nhập kho (cột Dãy ở ô chọn vị trí)', 'Kho => Nhập kho'),
    ('Kho', 'Phiếu điều chuyển vị trí (ô lọc Dãy)', 'Kho => Điều chuyển'),
    ('Kho', 'Kiểm kê theo vị trí', 'Kho => Kiểm kho => Theo vị trí'),
    ('Kho', 'Thẻ kho (cột tick Dãy)', 'Kho => Báo cáo kho'),
    ('Kho', 'Báo cáo tồn kho theo vị trí (cột tick Dãy)', 'Kho => Báo cáo kho'),
    ('Kho', 'Tổng hợp xuất nhập tồn (cột tick Dãy)', 'Kho => Báo cáo kho'),
    ('Kho', 'Nhà kho (điều kiện Khóa / Xóa nhà kho)', 'Kho => Danh mục'),
    ('Kho', 'Khoang (ô chọn Dãy, cột Dãy)', 'Kho => Danh mục'),
    ('Kho', 'Vị trí (ô chọn Dãy, cột Dãy)', 'Kho => Danh mục'),
    ('Tài chính', 'Phiếu nhập kho (cột Dãy ở ô chọn vị trí)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
    ('Tài chính', 'Kế hoạch kiểm kê theo vị trí', 'Tài chính => Kiểm kê'),
]

# ------------------------------------------------------------------ dữ liệu SRS
FR = []

# 2.1 Xem danh sách -------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách dãy',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang, Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách dãy'],
        ['Mô tả', 'Hiển thị các dãy thuộc kho trong phạm vi dữ liệu của người dùng (cả Hoạt động lẫn Khóa), kèm Nhà kho và Kho chứa dãy, có phân trang, sắp xếp và các nút thao tác theo từng dòng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn Danh mục dãy theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), dãy tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Người dùng thường chỉ thấy dãy thuộc kho của công ty mình; Super admin thấy dãy mọi công ty (BR-01).\n• Không có dãy khớp → bảng hiện "Không có dữ liệu phù hợp."\n• Dãy thuộc nhà kho / kho đang Khóa vẫn hiện trong danh sách.'],
    ],
    'anh': [('01_list', 'Màn Danh mục dãy lúc mới truy cập')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Danh sách dãy', 'Tiêu đề khối danh sách và tiêu đề trang.'],
        ['Nút Tạo mới', 'Button', 'Enable / Ẩn', 'Hiển thị', '- Mở cửa sổ "Tạo mới dãy" (mục 2.3).\n- Ẩn khi thiếu quyền "Quản lý kho".'],
        ['Nút Import Excel', 'Button', 'Enable / Ẩn', 'Hiển thị', '- Mở cửa sổ "Import dãy" (mục 2.8).\n- Ẩn khi thiếu quyền.'],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất file" (mục 2.9).'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.11).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa, không ẩn được.'],
        ['Cột Mã dãy', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sắp xếp được.\n- Chữ dạng liên kết: bấm vào mở cửa sổ "Xem chi tiết dãy" (mục 2.10).\n- Cột khóa, không ẩn được.'],
        ['Cột Tên dãy', 'Table/Grid', 'Read-only', 'Hiển thị', 'Sắp xếp được. Dài thì xuống tối đa 2 dòng.'],
        ['Cột Nhà kho', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên nhà kho chứa dãy (chỉ tên, không kèm mã). Sắp xếp được theo tên.'],
        ['Cột Kho', 'Table/Grid', 'Read-only', 'Hiển thị', 'Tên kho chứa nhà kho của dãy. Sắp xếp được theo tên.'],
        ['Cột Số khoang', 'Table/Grid', 'Read-only', 'Ẩn', 'Số khoang hiện có của dãy (mọi trạng thái); dãy chưa có khoang thì để trống. Mặc định ẩn, căn phải.'],
        ['Cột Mô tả', 'Table/Grid', 'Read-only', 'Ẩn', 'Mặc định ẩn.'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng "Họ tên - Mã phòng ban".'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm.'],
        ['Cột Người cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng "Họ tên - Mã phòng ban".'],
        ['Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm.'],
        ['Cột Trạng thái', 'Table/Grid', 'Read-only', 'Hiển thị', '- "Hoạt động" nền xanh.\n- "Khóa" nền đỏ.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sửa: dãy Hoạt động, có quyền.\n- Xóa: dãy Hoạt động, chưa có khoang, chưa được chọn trong kế hoạch kiểm kê, có quyền (BR-08).\n- Khóa: dãy Hoạt động và không còn khoang Hoạt động (BR-07); Mở khóa: dãy đang Khóa và nhà kho đang Hoạt động.\n- Lịch sử: luôn có.\n- Có 4 nút thì hiện 2 nút đầu, các nút còn lại nằm trong nút ba chấm "Hành động khác".\n- Nút không dùng được thì ẩn, không làm mờ. Cột khóa, không ẩn được.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Kiểm tra quyền "Quản lý kho"; thiếu quyền → menu không hiện, mở thẳng màn bị từ chối.\nAfter:\n– Tải trang 1 theo phạm vi công ty (BR-01), dãy tạo gần nhất trên cùng.'],
        ['Bấm tiêu đề cột Mã dãy / Tên dãy / Nhà kho / Kho', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại từ trang 1.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp, tải lại dữ liệu; đổi số dòng thì quay về trang 1.'],
        ['Bấm Mã dãy', 'Click', 'After:\n– Mở cửa sổ "Xem chi tiết dãy" (mục 2.10).'],
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách dãy'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao: Công ty (chỉ Super admin), Kho, Nhà kho, Trạng thái, Người tạo, Ngày tạo. Công ty → Kho → Nhà kho lọc dây chuyền (BR-12).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn Danh mục dãy.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô tìm nhanh chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Đổi Công ty / Kho → Kho / Nhà kho đang chọn không còn thuộc cấp trên thì tự bỏ chọn.\n• Bấm công tắc ổ khóa trên nhãn ô Công ty / Kho / Nhà kho → danh sách chọn có thêm mục đã khóa.\n• Ngày tạo "Từ" lớn hơn "Đến" → báo đỏ dưới ô, xoá bảng, không tải dữ liệu (BR-11).\n• Bấm Làm mới → xoá mọi điều kiện và tải lại danh sách.\n• Hệ thống ghi nhớ bộ lọc 10 phút khi rời màn rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực tìm kiếm và lọc (đã mở Tìm kiếm nâng cao)')],
    'ui': ui(['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả'], [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', '- Placeholder "Tìm theo mã, tên dãy".\n- Tìm gần đúng theo Mã dãy, Tên dãy, không phân biệt hoa thường.'],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Áp dụng từ khóa và các ô lọc.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá mọi điều kiện lọc và tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực các ô lọc (khi mở, nút đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" chọn ô lọc nào được hiển thị (áp dụng quy tắc chung).'],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Trống', '- Chỉ hiện với Super admin.\n- Lọc dãy theo công ty sở hữu kho.\n- Công tắc ổ khóa trên nhãn: hiện cả công ty đã khóa.'],
        ['Ô Kho', 'Dropdown', 'Enable', 'Kho đang Hoạt động trong phạm vi', 'Trống', '- Dạng "Mã - Tên"; đã chọn Công ty thì chỉ còn kho của công ty đó.\n- Công tắc ổ khóa trên nhãn: gợi ý "Hiện cả kho đã khoá", bật thì có thêm kho đã khóa.'],
        ['Ô Nhà kho', 'Dropdown', 'Enable', 'Nhà kho đang Hoạt động của kho đã chọn', 'Trống', '- Chưa chọn Kho: nhà kho của mọi kho trong danh sách.\n- Công tắc ổ khóa: "Hiện cả nhà kho đã khoá".'],
        ['Ô Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Trống', 'Bỏ trống thì hiện cả hai trạng thái.'],
        ['Ô Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc dãy do người được chọn tạo.'],
        ['Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Một ô chọn khoảng Từ ngày → Đến ngày, tính cả 2 đầu mút.\n- Từ > Đến: báo đỏ "Đến ngày phải lớn hơn hoặc bằng Từ ngày."'],
    ]),
    'ui_widths': [0.45, 1.25, 0.85, 0.8, 1.05, 0.8, 2.6],
    'events': [
        ['Bấm Tìm kiếm / nhấn Enter ở ô tìm nhanh', 'Click', 'After:\n– Áp đồng thời từ khóa và các ô lọc, tải lại bảng từ trang 1.'],
        ['Chọn giá trị ở ô lọc', 'Change', 'During:\n– Đổi Công ty: bỏ Kho, Nhà kho không thuộc công ty mới.\n– Đổi Kho: bỏ Nhà kho không thuộc kho mới.\n– Ô Ngày tạo: Từ > Đến → báo đỏ dưới ô, toast cùng câu, xoá bảng, không tải dữ liệu.\nAfter:\n– Tải lại bảng từ trang 1.'],
        ['Bấm công tắc ổ khóa trên nhãn ô Công ty / Kho / Nhà kho', 'Click', 'After:\n– Bật: danh sách chọn có thêm mục đã khóa (đánh dấu ổ khóa); tắt: chỉ mục đang Hoạt động. Mục đang được chọn luôn giữ trong danh sách.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, tải lại danh sách đầy đủ.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khu vực ô lọc.'],
    ],
})

# 2.3 Thêm mới -------------------------------------------------------------------
FORM_ROWS = [
    ['Kho', 'Dropdown', 'Enable', 'Kho đang Hoạt động trong phạm vi', 'Có', 'Trống', '- Dạng "Mã - Tên", có ô tìm.\n- Chỉ dùng để lọc ô Nhà kho, không lưu vào dãy.\n- Đổi Kho thì Nhà kho đang chọn không thuộc kho mới bị bỏ.'],
    ['Nhà kho', 'Dropdown', 'Enable / Disable', 'Nhà kho đang Hoạt động của Kho đã chọn', 'Có', 'Trống', '- Bị khóa cho tới khi chọn Kho.\n- Bỏ trống: "Bắt buộc phải nhập".\n- Nhà kho vừa bị khóa: "Nhà kho "<Tên nhà kho>" đã bị khóa, vui lòng chọn nhà kho khác".'],
    ['Mã dãy', 'Textbox', 'Enable', '1–50 ký tự: chữ không dấu, số, dấu - và _', 'Có', 'Trống', '- Duy nhất trong cùng nhà kho (BR-02).\n- Sai ký tự: báo đỏ ngay khi gõ "Chỉ gồm chữ không dấu, số, dấu - và _".\n- Quá 50 ký tự: báo đỏ ngay khi gõ.\n- Trùng: "Đã tồn tại trong nhà kho này".'],
    ['Tên dãy', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', '- Duy nhất trong cùng nhà kho (BR-03).\n- Ô không cho gõ quá 255 ký tự.\n- Trùng: "Đã tồn tại trong nhà kho này".'],
    ['Số khoang', 'Textbox', 'Enable', 'Số nguyên 1–999', 'Có', 'Trống', '- Chỉ nhận chữ số, tối đa 3 ký tự.\n- Icon ⓘ: "' + HINT_KHOANG + '"\n- Ngoài khoảng: "Nhập số nguyên từ 1 đến 999".'],
    ['Số vị trí mỗi khoang', 'Textbox', 'Enable', 'Số nguyên 1–999', 'Có', 'Trống', '- Chỉ nhận chữ số, tối đa 3 ký tự.\n- Icon ⓘ: "' + HINT_VITRI + '"\n- Ngoài khoảng: "Nhập số nguyên từ 1 đến 999".\n- Lỗi tổng số / mã vị trí sinh ra hiện dưới ô này (BR-06).'],
    ['Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động', 'Có nút × xoá nhanh; để trống thì lưu là Hoạt động.'],
    ['Mô tả', 'Textarea', 'Enable', '0–500 ký tự', 'Không', 'Trống', 'Quá 500 ký tự: "Nhập tối đa 500 ký tự".'],
]
FR.append({
    'ten': 'Thêm mới dãy', 'uc': 'uc_them',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Thêm mới dãy'],
        ['Mô tả', 'Tạo một dãy mới trong một nhà kho qua cửa sổ nhập liệu; hệ thống tự sinh khoang và vị trí cho dãy theo Số khoang × Số vị trí mỗi khoang (BR-05).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Có ít nhất một nhà kho đang Hoạt động trong phạm vi.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở cửa sổ "Tạo mới dãy", Trạng thái mặc định Hoạt động.\n3. Người dùng chọn Kho, Nhà kho, nhập Mã dãy, Tên dãy, Số khoang, Số vị trí mỗi khoang (Trạng thái, Mô tả nếu cần) rồi bấm Lưu.\n4. Hệ thống kiểm tra dữ liệu, ghi dãy vào nhà kho đã chọn, sinh khoang và vị trí.\n5. Ghi nhận Tạo mới trong lịch sử của dãy (và của từng khoang, vị trí sinh kèm).\n6. Đóng cửa sổ, tải lại danh sách, báo "Thêm mới thành công."'],
        ['Dòng sự kiện phụ', '• Thiếu / sai dữ liệu → báo đỏ dưới ô + toast "Bạn chưa nhập đầy đủ thông tin.", cửa sổ không đóng, dữ liệu đã nhập còn nguyên.\n• Bấm "Lưu & Tiếp tục" → lưu rồi giữ cửa sổ, các ô về trống để nhập dãy tiếp.\n• Bấm Đóng / (x) / bấm ra ngoài: chưa nhập gì thì đóng; đã nhập thì hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', 'Nút Lưu / Lưu & Tiếp tục bị khóa trong lúc đang lưu để tránh tạo trùng. Mỗi lần lưu sinh tối đa 10,000 vị trí.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': POPUP % 'Tạo mới dãy',
    'anh': [('10_create', 'Cửa sổ Tạo mới dãy'), ('11_code_error', 'Lỗi định dạng Mã dãy báo ngay khi gõ'),
            ('18_unsaved', 'Hộp xác nhận Thông tin chưa lưu khi đóng cửa sổ đã nhập dữ liệu')],
    'ui': ui(UI8, FORM_ROWS + [
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi đóng cửa sổ.'],
        ['Nút Lưu & Tiếp tục', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi giữ cửa sổ, xoá trắng các ô.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ, không lưu (đã nhập thì hỏi xác nhận).'],
        ['Hộp Thông tin chưa lưu', 'Label', 'Enable / Ẩn', '–', '–', 'Ẩn', '- Nội dung "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"\n- Nút Thoát: đóng không lưu; nút Ở lại: quay về cửa sổ.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho" (thiếu quyền thì nút ẩn).\nAfter:\n– Mở cửa sổ với các ô trống, Trạng thái = Hoạt động, ô Nhà kho khóa.'],
        ['Chọn Kho', 'Change', 'After:\n– Mở khóa ô Nhà kho, chỉ liệt kê nhà kho Hoạt động của kho đã chọn; bỏ Nhà kho đang chọn nếu không thuộc kho mới.'],
        ['Gõ Mã dãy', 'Change', 'During:\n– Sai ký tự hoặc quá 50 ký tự → báo đỏ ngay dưới ô.'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho".\nDuring:\n– Kiểm tra bắt buộc (Kho, Nhà kho, Mã dãy, Tên dãy, Số khoang, Số vị trí mỗi khoang), nhà kho thuộc phạm vi và đang Hoạt động (cả kho của nó), độ dài, ký tự Mã dãy, trùng Mã / Tên trong nhà kho, 2 ô số 1–999, tổng vị trí ≤ 10,000, mã vị trí sinh ra ≤ 50 ký tự và chưa có trong kho.\n' + TRUOC_LUU + '\nAfter:\n– Ghi dãy, sinh N khoang "Khoang i"/Ki, mỗi khoang M vị trí "Tầng j" mã <Mã kho>-<Mã nhà>-<Mã dãy>-Ki-Tj, đều Hoạt động.\n– Ghi nhận Tạo mới trong lịch sử dãy, khoang, vị trí.\n– Đóng cửa sổ, tải lại danh sách, báo "Thêm mới thành công."'],
        ['Bấm Lưu & Tiếp tục', 'Click', 'During:\n– Như nút Lưu.\n' + TRUOC_LUU + '\nAfter:\n– Ghi như nút Lưu, giữ cửa sổ, các ô về trống, Trạng thái về Hoạt động.'],
        ['Bấm Đóng / (x) / bấm ra ngoài', 'Click', 'After:\n– Chưa nhập gì → đóng cửa sổ.\n– Đã nhập → hiện hộp "Thông tin chưa lưu": Thoát thì đóng không lưu, Ở lại thì quay về cửa sổ.'],
    ],
})

# 2.4 Chỉnh sửa ------------------------------------------------------------------
EDIT_ROWS = [
    ['Kho', 'Dropdown', 'Disable', 'Kho của dãy', 'Không', 'Dữ liệu hiện tại', 'Chỉ đọc (nền xám), không có dấu *; kho đã khóa vẫn hiện đúng tên kèm biểu tượng ổ khóa.'],
    ['Nhà kho', 'Dropdown', 'Disable', 'Nhà kho của dãy', 'Không', 'Dữ liệu hiện tại', 'Chỉ đọc, không đổi được nhà kho của dãy đã tạo; nhà kho đã khóa hiện kèm biểu tượng ổ khóa.'],
    ['Mã dãy', 'Textbox', 'Enable', '1–50 ký tự: chữ không dấu, số, dấu - và _', 'Có', 'Dữ liệu hiện tại', 'Quy tắc như Thêm mới; đổi mã KHÔNG đổi mã các vị trí đã sinh.'],
    ['Tên dãy', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Dữ liệu hiện tại', 'Quy tắc như Thêm mới.'],
    ['Số khoang (dãy đã có khoang)', 'Textbox', 'Read-only', 'Số khoang hiện có', 'Không', 'Số khoang hiện có', 'Chỉ đọc; thêm / sửa / khóa khoang làm ở màn Khoang.'],
    ['Số khoang, Số vị trí mỗi khoang (dãy chưa có khoang)', 'Textbox', 'Enable', 'Số nguyên 1–999', 'Có', 'Trống', 'Hiện thay ô chỉ đọc khi dãy chưa có khoang nào; bắt buộc nhập, quy tắc và icon ⓘ như Thêm mới; lưu thì sinh khoang + vị trí.'],
    ['Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Không', 'Dữ liệu hiện tại', '- Dãy còn khoang Hoạt động: ô bị khóa (nền xám, không có nút ×).\n- Chọn Khóa rồi Lưu = khóa dãy (BR-07).'],
    ['Mô tả', 'Textarea', 'Enable', '0–500 ký tự', 'Không', 'Dữ liệu hiện tại', 'Quá 500 ký tự: "Nhập tối đa 500 ký tự".'],
]
FR.append({
    'ten': 'Chỉnh sửa dãy', 'uc': 'uc_sua',
    'qtc': 'Validate dữ liệu, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chỉnh sửa dãy'],
        ['Mô tả', 'Sửa Mã dãy, Tên dãy, Trạng thái, Mô tả của dãy đang Hoạt động. Không đổi được Kho / Nhà kho. Dãy chưa có khoang thì phải nhập Số khoang + Số vị trí mỗi khoang để sinh khoang.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Dãy đang Hoạt động và thuộc phạm vi dữ liệu của người dùng.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Sửa ở cột Hành động.\n2. Hệ thống mở cửa sổ "Sửa dãy" với dữ liệu hiện tại.\n3. Người dùng sửa và bấm Lưu.\n4. Hệ thống kiểm tra, ghi thay đổi; dãy chưa có khoang thì sinh khoang + vị trí.\n5. Ghi nhận Thay đổi thông tin (đổi Trạng thái ghi riêng Khóa) trong lịch sử.\n6. Đóng cửa sổ, báo "Cập nhật thành công."'],
        ['Dòng sự kiện phụ', '• Giữ nguyên Mã / Tên của chính dãy → không báo trùng.\n• Chọn Trạng thái Khóa khi dãy vừa có khoang Hoạt động → "Không thể khóa dãy khi vẫn còn danh mục con đang hoạt động."\n• Dãy vừa bị người khác khóa → "Dữ liệu đã thay đổi, vui lòng tải lại".\n• Bấm Đóng khi đã sửa → hỏi "Thông tin chưa lưu".'],
    ],
    'menu_them': ' => Sửa {icon:btn_sua}',
    'ghi_chu_layout': POPUP % 'Sửa dãy',
    'anh': [('12_edit', 'Cửa sổ Sửa dãy đã có khoang (Số khoang chỉ đọc, Trạng thái bị khóa)'),
            ('12b_edit_nospace', 'Cửa sổ Sửa dãy chưa có khoang (phải nhập Số khoang, Số vị trí mỗi khoang)')],
    'ui': ui(UI8, EDIT_ROWS + [
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu thay đổi rồi đóng cửa sổ.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng không lưu (đã sửa thì hỏi xác nhận). Cửa sổ Sửa không có nút Lưu & Tiếp tục.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện khi dãy Hoạt động và người dùng có quyền.\nAfter:\n– Tải dữ liệu dãy, mở cửa sổ; dãy không còn (vừa bị xoá / ngoài phạm vi) → báo "Dữ liệu đã thay đổi, vui lòng tải lại".'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền, dãy phải đang Hoạt động.\nDuring:\n– Kiểm tra như Thêm mới (bỏ qua trùng với chính dãy, nhà kho lấy theo dãy); dãy còn khoang Hoạt động thì không được chọn Khóa; dãy chưa có khoang thì bắt buộc 2 ô số.\n' + TRUOC_LUU + '\nAfter:\n– Ghi thay đổi; dãy chưa có khoang thì sinh khoang + vị trí (ghi lịch sử Tạo mới cho khoang, vị trí mới).\n– Ghi nhận Thay đổi thông tin / Khóa trong lịch sử.\n– Đóng cửa sổ, tải lại danh sách, báo "Cập nhật thành công."'],
        ['Bấm Đóng / (x) / bấm ra ngoài', 'Click', 'After:\n– Chưa đổi gì → đóng; đã đổi → hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
    ],
})

# 2.5 Xóa ---------------------------------------------------------------------------
FR.append({
    'ten': 'Xóa dãy', 'uc': 'uc_xoa',
    'qtc': 'Quy tắc Xóa, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xóa dãy'],
        ['Mô tả', 'Xóa hẳn dãy đang Hoạt động, chưa có khoang và chưa được chọn trong Kế hoạch kiểm kê theo vị trí (BR-08).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Dãy đang Hoạt động, không có khoang nào, chưa được dùng ở kế hoạch kiểm kê.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Xóa ở cột Hành động.\n2. Hệ thống hiện hộp "Xác nhận xóa": "Bạn có chắc muốn xóa dãy \'<Tên dãy>\'?"\n3. Người dùng bấm Xóa.\n4. Hệ thống ghi nhận Xóa trong lịch sử, xóa hẳn dãy.\n5. Tải lại danh sách, báo "Xóa thành công."'],
        ['Dòng sự kiện phụ', '• Bấm Hủy → đóng hộp, không thay đổi.\n• Dãy vừa bị khóa → "Không thể xóa dãy đang ở trạng thái khóa. Hãy mở khóa trước."\n• Dãy vừa có khoang / vừa được chọn trong kế hoạch kiểm kê → "Không thể xóa do dữ liệu đang được sử dụng."\n• Dãy vừa bị người khác xóa → "Dữ liệu đã thay đổi, vui lòng tải lại".'],
    ],
    'menu_them': ' => Xóa {icon:btn_xoa}',
    'ghi_chu_layout': POPUP % 'Xác nhận xóa',
    'anh': [('13_delete', 'Hộp xác nhận xóa dãy')],
    'ui': ui(UI4, [
        ['Nút Xóa (cột Hành động)', 'Button', 'Biểu tượng thùng rác; chỉ hiện khi dãy Hoạt động, chưa có khoang, chưa được dùng ở kế hoạch kiểm kê và người dùng có quyền.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận xóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn xóa dãy \'<Tên dãy>\'?"'],
        ['Nút Xóa', 'Button', 'Xác nhận xóa.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không xóa.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Xóa ở cột Hành động', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên dãy.'],
        ['Bấm Xóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền, dãy thuộc phạm vi.\nDuring:\n– Dãy phải đang Hoạt động, không có khoang, chưa được chọn trong kế hoạch kiểm kê.\n' + TRUOC_LUU + '\nAfter:\n– Ghi nhận Xóa trong lịch sử, xóa hẳn dãy.\n– Tải lại danh sách, báo "Xóa thành công."'],
        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.6 Khóa / Mở khóa -----------------------------------------------------------
FR.append({
    'ten': 'Khóa / Mở khóa dãy', 'uc': 'uc_khoa',
    'qtc': 'Quy tắc Khóa/Mở khóa, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Khóa / Mở khóa dãy'],
        ['Mô tả', 'Đổi trạng thái dãy giữa Hoạt động và Khóa. Khóa được khi không còn khoang Hoạt động; mở khóa được khi nhà kho chứa dãy đang Hoạt động (BR-07).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Khóa: dãy Hoạt động, mọi khoang đã Khóa (hoặc chưa có khoang). Mở khóa: dãy đang Khóa, nhà kho Hoạt động.'],
        ['Dòng sự kiện chính', '1. Người dùng chọn Khóa (hoặc Mở khóa) ở cột Hành động.\n2. Hệ thống hiện hộp "Xác nhận khóa" / "Xác nhận mở khóa" kèm tên dãy.\n3. Người dùng bấm Khóa / Mở khóa.\n4. Hệ thống đổi trạng thái, ghi nhận Khóa / Mở khóa trong lịch sử.\n5. Tải lại danh sách, báo "Khóa thành công." / "Mở khóa thành công."'],
        ['Dòng sự kiện phụ', '• Bấm Hủy → không thay đổi.\n• Khoang vừa được mở khóa ở nơi khác → "Không thể khóa dãy khi vẫn còn danh mục con đang hoạt động."\n• Nhà kho vừa bị khóa → "Không thể mở khóa dãy khi danh mục cha đang bị khóa."\n• Dãy đã bị người khác đổi trạng thái → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n• Mở khóa dãy không mở khóa khoang, vị trí bên dưới.'],
    ],
    'menu_them': ' => Khóa {icon:btn_khoa_row} / Mở khóa {icon:btn_mokhoa_row}',
    'ghi_chu_layout': POPUP % 'Xác nhận khóa / Xác nhận mở khóa',
    'anh': [('14_lock', 'Hộp xác nhận khóa dãy'), ('15_unlock', 'Hộp xác nhận mở khóa dãy')],
    'ui': ui(UI4, [
        ['Nút Khóa (cột Hành động)', 'Button', '- Biểu tượng ổ khóa; hiện khi dãy Hoạt động, không còn khoang Hoạt động, có quyền.\n- Dòng có nút Xóa thì Khóa nằm trong nút ba chấm "Hành động khác".'],
        ['Nút Mở khóa (cột Hành động)', 'Button', 'Biểu tượng ổ khóa mở; hiện khi dãy đang Khóa, nhà kho Hoạt động, có quyền.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận khóa" hoặc "Xác nhận mở khóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn khóa dãy \'<Tên dãy>\'?" / "Bạn có chắc muốn mở khóa dãy \'<Tên dãy>\'?"'],
        ['Nút Khóa / Mở khóa', 'Button', 'Xác nhận đổi trạng thái.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không thay đổi.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Chọn Khóa / Mở khóa', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên dãy.'],
        ['Bấm Khóa / Mở khóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền, dãy thuộc phạm vi.\nDuring:\n– Dãy đã ở trạng thái đích → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n– Khóa mà còn khoang Hoạt động → "Không thể khóa dãy khi vẫn còn danh mục con đang hoạt động."\n– Mở khóa mà nhà kho đang Khóa → "Không thể mở khóa dãy khi danh mục cha đang bị khóa."\n' + TRUOC_LUU + '\nAfter:\n– Đổi trạng thái, ghi nhận Khóa / Mở khóa trong lịch sử, tải lại danh sách, báo thành công.'],
        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.7 Lịch sử --------------------------------------------------------------------
FR.append({
    'ten': 'Xem lịch sử thay đổi',
    'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem lịch sử thay đổi dãy'],
        ['Mô tả', 'Liệt kê các lần thao tác trên một dãy (Tạo mới, Thay đổi thông tin, Khóa, Mở khóa, Xóa), mới nhất ở trên, kèm người thực hiện, thời điểm, giá trị cũ → mới.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Lịch sử ở cột Hành động (hoặc Xem lịch sử trong cửa sổ Xem chi tiết).\n2. Hệ thống mở cửa sổ "Lịch sử thay đổi: <Tên dãy>" và liệt kê các mốc.'],
        ['Dòng sự kiện phụ', '• Lọc theo Loại hành động, Người thực hiện, Từ ngày / Đến ngày bằng nút Bộ lọc trong cửa sổ.\n• Các trường được ghi: Mã dãy, Tên dãy, Nhà kho (bằng tên), Mô tả, Trạng thái.'],
    ],
    'menu_them': ' => Lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': POPUP % 'Lịch sử thay đổi',
    'anh': [('16_history', 'Cửa sổ Lịch sử thay đổi của dãy')],
    'ui': ui(UI6, [
        ['Nút Lịch sử (cột Hành động)', 'Button', 'Enable', 'Hiển thị', 'Luôn có ở mọi dòng (kể cả dãy Khóa); dòng có 4 nút thì nằm trong nút ba chấm.'],
        ['Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Lịch sử thay đổi: <Tên dãy>', ''],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Mở các ô lọc Loại hành động, Người thực hiện, Từ ngày, Đến ngày.'],
        ['Danh sách mốc', 'Table/Grid', 'Read-only', 'Theo dữ liệu', '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, loại hành động, "Người thực hiện: Họ tên — Phòng ban".\n- Dòng thay đổi: "<Trường>: giá trị cũ → giá trị mới".\n- Chưa có dữ liệu: "Chưa có lịch sử thao tác nào."'],
        ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lịch sử', 'Click', 'After:\n– Tải lịch sử của dãy, mới nhất trên cùng.'],
        ['Chọn điều kiện ở Bộ lọc', 'Change', 'After:\n– Lọc lại các mốc; không có mốc khớp → "Không có lịch sử phù hợp bộ lọc."'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.8 Import ---------------------------------------------------------------------
FR.append({
    'ten': 'Import dãy từ file Excel', 'uc': 'uc_import',
    'qtc': 'Quy tắc Import file, Validate dữ liệu, Thông báo.',
    'gioi_thieu': [
        ['Tên chức năng', 'Import dãy từ file Excel'],
        ['Mô tả', 'Tạo nhiều dãy từ file Excel theo file mẫu. Kho, nhà kho ghi bằng MÃ; mỗi dòng được kiểm tra và ghi như khi Tạo mới (sinh khoang, vị trí, ghi lịch sử) (BR-09).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Import Excel, hệ thống mở cửa sổ "Import dãy".\n2. Bấm Tải file mẫu (Mau_import_day.xlsx), điền dữ liệu.\n3. Bấm Chọn file Excel, chọn file, bấm Load lên bảng: dữ liệu hiện ở bảng xem trước, ô Tổng = số dòng.\n4. Bấm Validate: hệ thống kiểm tra từng dòng (chưa ghi dữ liệu), hiện Tổng / Hợp lệ / Lỗi; dòng lỗi tô đỏ kèm lý do, dòng hợp lệ bị khóa.\n5. Sửa dòng lỗi rồi Validate lại, hoặc bấm Bỏ dòng lỗi.\n6. Khi không còn dòng lỗi, bấm Import: hệ thống ghi từng dòng, ghi nhận Tạo mới trong lịch sử, báo "Import thành công N dãy.", tải lại danh sách.'],
        ['Dòng sự kiện phụ', '• File quá 500 dòng dữ liệu → "File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần."\n• Dòng vừa bị trùng với dãy người khác tạo trong lúc Import → bị bỏ qua, bảng kết quả "Import xong: a dòng thành công, b dòng lỗi bị bỏ qua" (nút Sao chép).\n• Bấm Xoá trạng thái validate để sửa lại cả dòng đã khóa.\n• Bấm Làm mới để làm lại từ đầu; Đóng để thoát.'],
    ],
    'menu_them': ' => Import Excel {icon:btn_import}',
    'ghi_chu_layout': POPUP % 'Import dãy',
    'anh': [('21_import_open', 'Cửa sổ Import dãy khi vừa mở'), ('22_import_loaded', 'Dữ liệu sau khi Load lên bảng'),
            ('23_import_validated', 'Kết quả Validate — dòng lỗi nêu rõ lý do')],
    'ui': ui(UI7I, [
        ['Nút Chọn file Excel', 'Button', 'Enable', '–', '–', 'Chọn file .xlsx, hiện tên file bên cạnh.'],
        ['Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Tải Mau_import_day.xlsx: dòng 1 tên cột (cột bắt buộc có *), dòng 2 hướng dẫn, 2 dòng dữ liệu mẫu.'],
        ['Nút Load lên bảng', 'Button', 'Enable / Disable', '–', 'Disable', 'Bấm được khi đã chọn file; đọc file lên bảng xem trước.'],
        ['Nút Validate', 'Button', 'Enable / Disable', '–', 'Disable', 'Bấm được khi bảng có dữ liệu; kiểm tra từng dòng, chưa ghi dữ liệu.'],
        ['Nút Import', 'Button', 'Enable / Disable', '–', 'Disable', 'Chỉ bấm được khi đã Validate, còn ≥ 1 dòng hợp lệ và KHÔNG còn dòng lỗi.'],
        ['Ô Tổng / Hợp lệ / Lỗi', 'Label', 'Read-only', '–', 'Tổng: 0', 'Tổng hiện sau Load; Hợp lệ, Lỗi hiện sau Validate.'],
        ['Cột Mã kho *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Mã ở màn Kho vật lý, trong phạm vi công ty; sai: "Không tồn tại kho có mã "<mã>"".'],
        ['Cột Mã nhà kho *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Mã nhà kho thuộc kho trên; sai: "Không tồn tại nhà kho có mã "<mã>" trong kho "<mã kho>""; nhà kho đã khóa báo như popup.'],
        ['Cột Mã dãy *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Chữ không dấu, số, dấu - và _, tối đa 50 ký tự, không trùng trong nhà kho và trong file.'],
        ['Cột Tên dãy *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Tối đa 255 ký tự, không trùng trong nhà kho và trong file.'],
        ['Cột Số khoang *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Số nguyên 1–999; tự sinh khoang + vị trí như khi tạo tay.'],
        ['Cột Số vị trí mỗi khoang *', 'Table/Grid', 'Enable', 'Có', 'Theo file', 'Số nguyên 1–999; Số khoang × Số vị trí tối đa 10,000.'],
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
        ['Bấm Validate', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho".\nDuring:\n– Mỗi dòng tra Mã kho → Mã nhà kho rồi kiểm như Tạo mới; trùng Mã dãy / Tên dãy cùng nhà kho trong file ("Bị trùng trong file").\nAfter:\n– Hiện Tổng / Hợp lệ / Lỗi, toast "Validate xong: X hợp lệ, Y không hợp lệ" (hoặc "Validate thành công"); dòng lỗi tô đỏ kèm lý do, dòng hợp lệ bị khóa.'],
        ['Bấm Import', 'Click', 'Before:\n– Đã Validate, không còn dòng lỗi.\nDuring:\n– Hệ thống kiểm lại từng dòng ngay trước khi ghi.\n' + TRUOC_LUU + '\nAfter:\n– Ghi từng dòng như Tạo mới (sinh khoang, vị trí), ghi nhận Tạo mới trong lịch sử.\n– Báo "Import thành công N dãy.", đóng cửa sổ, tải lại danh sách; có dòng bị bỏ qua thì hiện bảng kết quả.'],
        ['Bấm Bỏ dòng lỗi / Xoá trạng thái validate', 'Click', 'After:\n– Bỏ dòng lỗi khỏi bảng / mở khóa các dòng để sửa.'],
        ['Bấm Đóng / Làm mới', 'Click', 'After:\n– Đóng cửa sổ / xoá dữ liệu đang xem để làm lại.'],
    ],
})

# 2.9 Xuất Excel -------------------------------------------------------------------
FR.append({
    'ten': 'Xuất danh sách ra Excel', 'uc': 'uc_xuat',
    'qtc': 'Quy tắc Excel, Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách dãy ra Excel'],
        ['Mô tả', 'Xuất toàn bộ dãy khớp bộ lọc đang áp dụng (mọi trang) ra file Excel, người dùng chọn trường và thứ tự cột (BR-10).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng lọc danh sách (nếu cần), bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất file", tích sẵn các cột đang hiện trên bảng.\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự rồi bấm Xuất file.\n4. Hệ thống tải file danh_sach_day.xlsx, báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Kết quả rỗng vẫn xuất file (tiêu đề + tên cột).\n• Ô Ngày tạo đang sai (Từ > Đến) → báo lỗi, không xuất.\n• Lỗi hệ thống → "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': POPUP % 'Chọn trường xuất file',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất file')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '"Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file."'],
        ['Danh sách trường', 'Table/Grid', 'Enable', 'Tích theo cột đang hiện', '11 trường: Mã dãy, Tên dãy, Nhà kho, Kho, Số khoang, Mô tả, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. Mỗi trường có ô tích và biểu tượng ☰ kéo đổi vị trí.'],
        ['Nút Chọn tất cả', 'Button', 'Enable', '–', 'Tích mọi trường.'],
        ['Nút Bỏ chọn hết', 'Button', 'Enable', '–', 'Bỏ tích mọi trường.'],
        ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn x/11 trường', ''],
        ['Nút Xuất file', 'Button', 'Enable / Disable', 'Enable', 'Tải file; không bấm được khi không còn trường nào được chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ, không xuất.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ, tích sẵn theo cột đang hiện.'],
        ['Bấm Xuất file', 'Click', 'During:\n– Ô Ngày tạo sai → báo "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", không xuất.\n' + TRUOC_LUU + '\nAfter:\n– Tải file danh_sach_day.xlsx: tiêu đề "Danh sách dãy", cột theo thứ tự đã chọn, mọi dòng khớp bộ lọc; báo "Xuất Excel thành công".'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.10 Xem chi tiết ----------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết dãy', 'uc': 'uc_xem',
    'qtc': 'Màn Xem chi tiết, Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết dãy'],
        ['Mô tả', 'Xem toàn bộ thông tin một dãy ở chế độ chỉ đọc, kèm khối Lịch sử.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm vào Mã dãy trên bảng.\n2. Hệ thống mở cửa sổ "Xem chi tiết dãy", mọi ô chỉ đọc.\n3. Bấm Xem lịch sử để mở khối Lịch sử ngay trong cửa sổ.'],
        ['Dòng sự kiện phụ', '• Dãy vừa bị xoá / ngoài phạm vi → báo "Dữ liệu đã thay đổi, vui lòng tải lại", không mở cửa sổ.'],
    ],
    'menu_them': ' => Bấm Mã dãy',
    'ghi_chu_layout': POPUP % 'Xem chi tiết dãy',
    'anh': [('17_detail', 'Cửa sổ Xem chi tiết dãy ở chế độ chỉ đọc'),
            ('17b_detail_history', 'Khối Lịch sử trong cửa sổ Xem chi tiết')],
    'ui': ui(UI6, [
        ['Kho, Nhà kho', 'Dropdown', 'Read-only', 'Dữ liệu hiện tại', 'Dạng "Mã - Tên"; kho / nhà kho đã khóa kèm biểu tượng ổ khóa. Không có dấu (*).'],
        ['Mã dãy, Tên dãy', 'Textbox', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Số khoang', 'Textbox', 'Read-only', 'Số khoang hiện có', ''],
        ['Trạng thái', 'Dropdown', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Mô tả', 'Textarea', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Khối Lịch sử', 'Table/Grid', 'Enable', 'Thu gọn', '- Nút Xem lịch sử mở khối, hiện số mốc.\n- Nút Làm mới tải lại, Thu gọn đóng khối, Bộ lọc lọc mốc như mục 2.7.'],
        ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ. Không có nút Lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Mã dãy', 'Click', 'After:\n– Tải dữ liệu, mở cửa sổ chỉ đọc.'],
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
        ['Dòng sự kiện phụ', '• Cột STT, Mã dãy, Hành động là cột khóa: không bỏ tích, không kéo được.\n• Bấm Đóng → bỏ các thay đổi vừa chỉnh.'],
    ],
    'menu_them': ' => Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': POPUP % 'Tuỳ chỉnh cột',
    'anh': [('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột — STT, Mã dãy, Hành động bị khóa')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '"Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng."'],
        ['Danh sách cột', 'Table/Grid', 'Enable', 'Theo cấu hình đã lưu', '13 cột theo thứ tự trên bảng. Mặc định ẩn: Số khoang, Mô tả.'],
        ['Cột khóa', 'Table/Grid', 'Disable', 'Luôn tích', 'STT, Mã dãy, Hành động: ô tích xám kèm biểu tượng khóa, không ẩn và không đổi vị trí được.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Tích / bỏ tích mọi cột (trừ cột khóa).'],
        ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn x/13 cột', ''],
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
    'menu': [('Kho', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Dãy', 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu chức năng.',
        'Làm rõ phạm vi dữ liệu theo công ty, ràng buộc trùng Mã dãy / Tên dãy trong cùng nhà kho, dữ liệu tự sinh khi tạo dãy (khoang, vị trí) cùng các giới hạn của nó, điều kiện Khóa / Mở khóa theo cây kho và điều kiện Xóa.',
    ],
    'thuat_ngu': [
        ['Kho', 'Kho vật lý — cấp gốc của cây kho: Kho → Nhà kho → Dãy → Khoang → Vị trí.'],
        ['Nhà kho', 'Cấp con của kho, là cấp cha trực tiếp của dãy.'],
        ['Dãy', 'Cấp thứ 3 của cây kho, thuộc một nhà kho; chứa các khoang.'],
        ['Khoang', 'Cấp con của dãy; khi tạo dãy hệ thống tự sinh "Khoang 1"… "Khoang N" (mã K1…KN).'],
        ['Vị trí', 'Cấp con của khoang; khi tạo dãy mỗi khoang tự sinh các vị trí "Tầng 1"… mã <Mã kho>-<Mã nhà>-<Mã dãy>-K<i>-T<j>.'],
        ['Hoạt động', 'Trạng thái dãy dùng được ở các màn nghiệp vụ.'],
        ['Khóa', 'Dãy vẫn nằm trong danh mục, xem được lịch sử nhưng không còn chọn được ở các màn nghiệp vụ.'],
        ['Super admin', 'Tài khoản quản trị cao nhất, xem được dãy của mọi công ty.'],
    ],
    'quyen_truoc': ['Màn hình dùng một quyền duy nhất "Quản lý kho" (nhóm Danh mục kho) cho cả xem lẫn thao tác; quyền này dùng chung cho 7 màn Danh mục của phân hệ Kho. Quyền được gán vào vai trò theo công ty.'],
    'quyen_rows': [['Quản lý kho', 'Xem danh sách, tìm kiếm, xem chi tiết, lịch sử, tùy chỉnh cột, xuất Excel; Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Import Excel.']],
    'ma_tran': [['Chức năng', 'Quản lý kho', 'Không có quyền']] + [[f, 'Có', 'Không'] for f in [
        'FR-01 Xem danh sách dãy', 'FR-02 Tìm kiếm và lọc', 'FR-03 Thêm mới dãy', 'FR-04 Chỉnh sửa dãy',
        'FR-05 Xóa dãy', 'FR-06 Khóa / Mở khóa dãy', 'FR-07 Xem lịch sử thay đổi',
        'FR-08 Import dãy từ file Excel', 'FR-09 Xuất danh sách ra Excel', 'FR-10 Xem chi tiết dãy',
        'FR-11 Tùy chỉnh cột hiển thị']],
    'ma_tran_widths': [2.6, 1.2, 1.2],
    'quyen_sau': ['Phạm vi dữ liệu: người dùng thường chỉ thấy và thao tác dãy thuộc kho của công ty mình; Super admin thấy dãy mọi công ty và có thêm ô lọc Công ty (BR-01).'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Phạm vi dữ liệu theo công ty', [
            '– Dãy thuộc công ty của kho chứa nhà kho của dãy.',
            '– Người dùng thường chỉ thấy, xem, sửa, khóa, xóa, xuất, tạo dãy trong kho của công ty đang làm việc của mình.',
            '– Super admin thấy dãy mọi công ty, có thêm ô lọc Công ty.',
            '– Không xác định được công ty của người dùng → không thấy dãy nào.',
            '– Thao tác trên dãy ngoài phạm vi bị từ chối như dữ liệu không tồn tại; tạo dãy vào nhà kho ngoài phạm vi báo "Nhà kho không tồn tại".'],
         ['Xem danh sách', 'Xuất Excel', 'Thêm mới', 'Chỉnh sửa', 'Xóa', 'Khóa / Mở khóa', 'Import']),
        ('BR-02', 'Mã dãy', [
            '– Bắt buộc, 1–50 ký tự, chỉ gồm chữ không dấu, số, dấu - và _; cắt khoảng trắng đầu / cuối.',
            '– Duy nhất TRONG CÙNG nhà kho (mọi trạng thái); nhà kho khác được trùng.',
            '– Giữ nguyên chữ hoa / thường người dùng nhập; đổi mã về sau không đổi mã vị trí đã sinh.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-03', 'Tên dãy', ['– Bắt buộc, tối đa 255 ký tự, duy nhất trong cùng nhà kho như Mã dãy (không phân biệt hoa thường).'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-04', 'Kho / Nhà kho của dãy', [
            '– Chọn khi tạo: Kho chỉ để lọc Nhà kho, không lưu; chỉ chọn được kho / nhà kho đang Hoạt động trong phạm vi.',
            '– Nhà kho (hoặc kho của nó) vừa bị khóa → "Nhà kho "<Tên>" đã bị khóa, vui lòng chọn nhà kho khác".',
            '– Không đổi được Kho / Nhà kho khi sửa.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-05', 'Dữ liệu tự sinh khi tạo dãy', [
            '– Sinh N khoang "Khoang 1"… "Khoang N", mã K1… KN, trạng thái Hoạt động (N = Số khoang).',
            '– Mỗi khoang sinh M vị trí "Tầng 1"… "Tầng M", mã <Mã kho>-<Mã nhà>-<Mã dãy>-K<i>-T<j>, thuộc kho của dãy, Hoạt động (M = Số vị trí mỗi khoang).',
            '– Khoang và vị trí sinh kèm cũng được ghi lịch sử Tạo mới.',
            '– Sửa dãy CHƯA có khoang: bắt buộc nhập 2 số và sinh như trên; dãy đã có khoang thì không sinh thêm.'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-06', 'Số khoang / Số vị trí mỗi khoang', [
            '– Số nguyên từ 1 đến 999 ("Nhập số nguyên từ 1 đến 999"); ô chỉ nhận chữ số, tối đa 3 ký tự.',
            '– Tổng vị trí sinh ra (Số khoang × Số vị trí mỗi khoang) tối đa 10,000: "' + LOI_TONG + '".',
            '– Mã vị trí sinh ra tối đa 50 ký tự: "' + LOI_DAI_VT + '".',
            '– Mã vị trí sinh ra không được trùng mã vị trí đã có trong cùng kho: "' + LOI_TRUNG_VT + '".'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-07', 'Điều kiện Khóa / Mở khóa', [
            '– Chỉ khóa được dãy đang Hoạt động và KHÔNG còn khoang Hoạt động ("Không thể khóa dãy khi vẫn còn danh mục con đang hoạt động."); áp dụng cả khi đổi Trạng thái trong cửa sổ Sửa.',
            '– Chỉ mở khóa được khi nhà kho chứa dãy đang Hoạt động ("Không thể mở khóa dãy khi danh mục cha đang bị khóa."); mở khóa không lan xuống khoang, vị trí.',
            '– Dãy đang Khóa: ẩn Sửa, Xóa; không còn trong ô chọn Dãy ở các màn nghiệp vụ; nhà kho chỉ khóa được khi mọi dãy đã Khóa.'], ['Khóa / Mở khóa', 'Chỉnh sửa']),
        ('BR-08', 'Điều kiện và cách Xóa', [
            '– Chỉ xóa dãy đang Hoạt động ("Không thể xóa dãy đang ở trạng thái khóa. Hãy mở khóa trước.").',
            '– Dãy còn khoang (mọi trạng thái) hoặc đã được chọn trong Kế hoạch kiểm kê theo vị trí → "Không thể xóa do dữ liệu đang được sử dụng."',
            '– Xóa là xóa hẳn; Mã / Tên dùng lại được.'], ['Xóa']),
        ('BR-09', 'Import', [
            '– Mỗi dòng tra Mã kho (trong phạm vi) → Mã nhà kho (thuộc kho đó) rồi kiểm và ghi như Tạo mới (BR-02 → BR-06).',
            '– Trùng Mã dãy / Tên dãy cùng nhà kho giữa các dòng trong file → "Bị trùng trong file".',
            '– Tối đa 500 dòng dữ liệu mỗi lần; chỉ Import khi đã Validate và không còn dòng lỗi.'], ['Import']),
        ('BR-10', 'Xuất Excel', ['– Xuất mọi dòng khớp bộ lọc đang áp dụng (không chỉ trang đang xem), cột theo thứ tự người dùng chọn; tên file danh_sach_day.xlsx.'], ['Xuất Excel']),
        ('BR-11', 'Lọc Ngày tạo', ['– Ngày tạo Từ lớn hơn Đến → báo đỏ "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", xoá bảng, không tải dữ liệu và không xuất Excel.'], ['Tìm kiếm và lọc', 'Xuất Excel']),
        ('BR-12', 'Bộ lọc dây chuyền Công ty → Kho → Nhà kho', [
            '– Ô Kho chỉ liệt kê kho của Công ty đã chọn; ô Nhà kho chỉ liệt kê nhà kho của Kho đã chọn.',
            '– Đổi cấp trên thì giá trị cấp dưới không còn thuộc nó tự bỏ chọn.',
            '– Mặc định chỉ liệt kê mục đang Hoạt động; bật công tắc ổ khóa trên nhãn để thấy cả mục đã khóa.'], ['Tìm kiếm và lọc']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây chọn, lọc, hiển thị hoặc kiểm tra dữ liệu Dãy; dãy đang Khóa không còn chọn được ở các ô chọn dãy.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng có quyền "Quản lý kho"',
    'mains': [('FR-01', 'Xem danh sách dãy', 'view'), ('FR-03', 'Thêm mới dãy', 'crud'),
              ('FR-04', 'Chỉnh sửa dãy', 'crud'), ('FR-05', 'Xóa dãy', 'action'),
              ('FR-06', 'Khóa / Mở khóa dãy', 'action'), ('FR-08', 'Import dãy từ file Excel', 'io'),
              ('FR-09', 'Xuất danh sách dãy ra Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc dãy', 'view'), ('FR-10', 'Xem chi tiết dãy', 'view'),
             ('FR-11', 'Tùy chỉnh cột hiển thị', 'view'), ('FR-07', 'Xem lịch sử thay đổi', 'view')],
    'rieng': [('FR-03', 'Thêm mới dãy', 'crud', 'uc_them'), ('FR-04', 'Chỉnh sửa dãy', 'crud', 'uc_sua'),
              ('FR-05', 'Xóa dãy', 'action', 'uc_xoa'), ('FR-06', 'Khóa / Mở khóa dãy', 'action', 'uc_khoa'),
              ('FR-08', 'Import dãy từ file Excel', 'io', 'uc_import'),
              ('FR-09', 'Xuất danh sách dãy ra Excel', 'io', 'uc_xuat'), ('FR-10', 'Xem chi tiết dãy', 'view', 'uc_xem')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)

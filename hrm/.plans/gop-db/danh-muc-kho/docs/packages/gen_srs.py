# -*- coding: utf-8 -*-
"""SRS - Danh mục kiện (form Danh mục quốc gia, TPE duyệt) — chép khuôn màn mẫu docs/warehouses/gen_srs.py.

Nguồn (code HRM hiện tại):
  FE hrm-client/pages/warehouse/packages/{index.vue, AddPackageModal.vue}, utils/mixins/{vehicleCatalogScreenMixin,
     vehicleCatalogModalMixin, warehouseCatalogModalMixin, warehouseCatalogImportMixin, createdRangeFilterMixin}.js,
     utils/warehouse-catalog-import.js (packages), components/subsystem-menu/warehouse.js
  BE Modules/MasterData: Entities/Warehouse/Package.php, Http/Controllers/V1/Warehouse/{PackageController,
     WarehouseTreeCatalogController}.php, ProductClassification/{BaseCatalogController, BaseCatalogService,
     BaseCatalogModel, BaseCatalogRequest, BaseCatalogResource}.php, Http/Requests/Warehouse/PackageRequest.php,
     Services/Warehouse/{PackageService, Concerns/ImportsWarehouseCatalogRows}.php; app/Services/CatalogHistoryService.php
  Phần 5: dò code FE/BE (02/11/2026) — không màn nào có ô chọn Kiện; chỉ Chuyến xe chở hàng đếm kiện của lô hàng xuất.
Chạy:  python gen_srs.py          (dựng + Word cập nhật mục lục + PDF out/ + tự kiểm)
       python gen_srs.py --no-word (chỉ dựng .docx)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import _lib_win as L  # noqa: E402

TEN = 'Danh mục kiện'
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
# Không có màn nào có ô chọn Kiện (danh mục không có nguồn chọn cho màn khác). Kiện được gắn vào lô hàng của phiếu
# xuất kho; Chuyến xe chở hàng đếm số kiện khác nhau của các phiếu xuất kho trên chuyến khi lưu.
P5 = [
    ('Vận chuyển', 'Chuyến xe chở hàng (tự tính tổng số kiện của các phiếu xuất kho trên chuyến khi lưu)', 'Vận chuyển => Chuyến xe'),
]

# ------------------------------------------------------------------ dữ liệu SRS
FR = []

# 2.1 Xem danh sách -------------------------------------------------------------
FR.append({
    'ten': 'Xem danh sách kiện',
    'qtc': 'Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang, Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách kiện'],
        ['Mô tả', 'Hiển thị mọi kiện trong danh mục (cả Hoạt động lẫn Khóa), có phân trang, sắp xếp và các nút thao tác theo từng dòng. Kiện là danh mục dùng chung, không chia theo công ty (BR-01).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn Danh mục kiện theo đường dẫn menu.\n2. Hệ thống tải trang đầu (10 dòng), kiện tạo gần nhất ở trên cùng.\n3. Bảng hiển thị dữ liệu, chân bảng ghi "Hiển thị a–b / N".'],
        ['Dòng sự kiện phụ', '• Mọi người dùng có quyền thấy cùng một danh sách, không phân biệt công ty (BR-01).\n• Không có kiện khớp → bảng hiện "Không có dữ liệu phù hợp."\n• Kiện đã bị xóa không còn trong danh sách (BR-06).'],
    ],
    'anh': [('01_list', 'Màn Danh mục kiện lúc mới truy cập')],
    'ui': ui(UI6, [
        ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Danh sách kiện', 'Tiêu đề khối danh sách và tiêu đề trang.'],
        ['Nút Tạo mới', 'Button', 'Enable / Ẩn', 'Hiển thị', '- Mở cửa sổ "Tạo mới kiện" (mục 2.3).\n- Ẩn khi thiếu quyền "Quản lý kho".'],
        ['Nút Import Excel', 'Button', 'Enable / Ẩn', 'Hiển thị', '- Mở cửa sổ "Import kiện" (mục 2.8).\n- Ẩn khi thiếu quyền.'],
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', 'Mở cửa sổ "Chọn trường xuất file" (mục 2.9).'],
        ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', 'Biểu tượng cột, mở cửa sổ "Tuỳ chỉnh cột" (mục 2.11).'],
        ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự liên tục qua các trang. Cột khóa, không ẩn được.'],
        ['Cột Tên kiện', 'Table/Grid', 'Read-only', 'Hiển thị', '- Dạng "Kiện <thứ tự>".\n- Sắp xếp được, sắp theo con số Thứ tự (Kiện 2 đứng trước Kiện 10).\n- Chữ dạng liên kết: bấm vào mở cửa sổ "Xem chi tiết kiện" (mục 2.10).\n- Cột khóa, không ẩn được.'],
        ['Cột Thứ tự', 'Table/Grid', 'Read-only', 'Hiển thị', 'Số thứ tự của kiện, căn phải.'],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng "Họ tên - Mã phòng ban".'],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Người cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'Dạng "Họ tên - Mã phòng ban".'],
        ['Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'Hiển thị', 'dd/mm/yyyy hh:mm. Sắp xếp được.'],
        ['Cột Trạng thái', 'Table/Grid', 'Read-only', 'Hiển thị', '- "Hoạt động" nền xanh.\n- "Khóa" nền đỏ.'],
        ['Cột Hành động', 'Table/Grid', 'Read-only', 'Hiển thị', '- Sửa: kiện Hoạt động, có quyền.\n- Xóa: kiện Hoạt động, chưa được gắn vào lô hàng của phiếu xuất kho nào, có quyền (BR-06).\n- Khóa: kiện Hoạt động; Mở khóa: kiện đang Khóa (BR-05).\n- Lịch sử: luôn có.\n- Có 4 nút thì hiện 2 nút đầu, các nút còn lại nằm trong nút ba chấm "Hành động khác".\n- Nút không dùng được thì ẩn, không làm mờ. Cột khóa, không ẩn được.'],
        ['Phân trang', 'Table/Grid', 'Enable', '10 dòng/trang', 'Chọn số dòng/trang, chuyển trang; chân bảng "Hiển thị a–b / N".'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Kiểm tra quyền "Quản lý kho"; thiếu quyền → menu không hiện, mở thẳng màn bị từ chối.\nAfter:\n– Tải trang 1, kiện tạo gần nhất trên cùng.'],
        ['Bấm tiêu đề cột Tên kiện / Ngày tạo / Ngày cập nhật', 'Click', 'After:\n– Đổi chiều sắp xếp tăng / giảm, tải lại từ trang 1. Tên kiện sắp theo con số Thứ tự.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và thứ tự sắp xếp, tải lại dữ liệu; đổi số dòng thì quay về trang 1.'],
        ['Bấm Tên kiện', 'Click', 'After:\n– Mở cửa sổ "Xem chi tiết kiện" (mục 2.10).'],
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc danh sách kiện'],
        ['Mô tả', 'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao: Trạng thái, Người tạo, Người cập nhật, Ngày tạo.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn Danh mục kiện.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa rồi bấm Tìm kiếm hoặc Enter; hoặc bấm Tìm kiếm nâng cao và chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện và tải lại danh sách từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô tìm nhanh chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Tìm theo chữ chứa trong tên: "Kiện 1" ra cả Kiện 1, Kiện 10, Kiện 12…\n• Ngày tạo "Từ" lớn hơn "Đến" → báo đỏ dưới ô, xoá bảng, không tải dữ liệu (BR-08).\n• Bấm Làm mới → xoá mọi điều kiện và tải lại danh sách.\n• Hệ thống ghi nhớ bộ lọc 10 phút khi rời màn rồi quay lại.'],
    ],
    'anh': [('02_filter', 'Khu vực tìm kiếm và lọc (đã mở Tìm kiếm nâng cao)')],
    'ui': ui(['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả'], [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', '- Placeholder "Tìm theo tên kiện, người tạo".\n- Tìm gần đúng theo Tên kiện, họ tên Người tạo, không phân biệt hoa thường.'],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Áp dụng từ khóa và các ô lọc.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá mọi điều kiện lọc và tải lại danh sách.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Thu gọn', 'Mở / đóng khu vực các ô lọc (khi mở, nút đổi thành "Ẩn tìm kiếm nâng cao").'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" chọn ô lọc nào được hiển thị (áp dụng quy tắc chung).'],
        ['Ô Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Trống', 'Bỏ trống thì hiện cả hai trạng thái.'],
        ['Ô Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc kiện do người được chọn tạo.'],
        ['Ô Người cập nhật', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', 'Lọc kiện có người cập nhật gần nhất là người được chọn.'],
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
    ['Thứ tự', 'Textbox', 'Enable', 'Số nguyên lớn hơn 0, tối đa 9 chữ số', 'Có', 'Trống', '- Chỉ nhận chữ số: gõ ký tự khác bị bỏ ngay (gõ "-3" còn "3", "1.5" còn "15").\n- Duy nhất trong toàn danh mục, tính cả kiện đang Khóa (BR-02).\n- Icon ⓘ: "Tên kiện tự đặt theo thứ tự: "Kiện <thứ tự>"."\n- Bỏ trống: "Bắt buộc phải nhập".\n- Bằng 0: "Nhập số nguyên lớn hơn 0".\n- Trùng: "Đã tồn tại".'],
    ['Tên kiện', 'Textbox', 'Disable', '–', 'Không', 'Trống', '- Ô chỉ đọc, nền xám, placeholder "Tự đặt theo thứ tự".\n- Hiện ngay "Kiện <thứ tự>" khi gõ Thứ tự (BR-03).'],
    ['Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Hoạt động', 'Có nút × xoá nhanh; để trống thì lưu là Hoạt động.'],
]
FR.append({
    'ten': 'Thêm mới kiện', 'uc': 'uc_them',
    'qtc': 'Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Thêm mới kiện'],
        ['Mô tả', 'Tạo một kiện mới qua cửa sổ nhập liệu; người dùng chỉ nhập Thứ tự, Tên kiện do hệ thống tự đặt "Kiện <thứ tự>" (BR-03).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Tạo mới.\n2. Hệ thống mở cửa sổ "Tạo mới kiện", Trạng thái mặc định Hoạt động.\n3. Người dùng nhập Thứ tự (ô Tên kiện tự hiện "Kiện <thứ tự>"), chọn Trạng thái nếu cần rồi bấm Lưu.\n4. Hệ thống kiểm tra dữ liệu, ghi kiện với Tên kiện = "Kiện <thứ tự>".\n5. Ghi nhận Tạo mới trong lịch sử của kiện.\n6. Đóng cửa sổ, tải lại danh sách, báo "Thêm mới thành công."'],
        ['Dòng sự kiện phụ', '• Thiếu / sai dữ liệu → báo đỏ dưới ô + toast "Bạn chưa nhập đầy đủ thông tin.", cửa sổ không đóng, dữ liệu đã nhập còn nguyên.\n• Bấm "Lưu & Tiếp tục" → lưu rồi giữ cửa sổ, các ô về trống để nhập kiện tiếp.\n• Bấm Đóng / (x) / bấm ra ngoài: chưa nhập gì thì đóng; đã nhập thì hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
        ['Yêu cầu đặc biệt', 'Nút Lưu / Lưu & Tiếp tục bị khóa trong lúc đang lưu để tránh tạo trùng.'],
    ],
    'menu_them': ' => Tạo mới {icon:btn_taomoi}',
    'ghi_chu_layout': POPUP % 'Tạo mới kiện',
    'anh': [('10_create', 'Cửa sổ Tạo mới kiện'), ('11_name_preview', 'Gõ Thứ tự, ô Tên kiện tự hiện "Kiện <thứ tự>"'),
            ('18_unsaved', 'Hộp xác nhận Thông tin chưa lưu khi đóng cửa sổ đã nhập dữ liệu')],
    'ui': ui(UI8, FORM_ROWS + [
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi đóng cửa sổ.'],
        ['Nút Lưu & Tiếp tục', 'Button', 'Enable', '–', '–', '–', 'Lưu rồi giữ cửa sổ, xoá trắng các ô.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ, không lưu (đã nhập thì hỏi xác nhận).'],
        ['Hộp Thông tin chưa lưu', 'Label', 'Enable / Ẩn', '–', '–', 'Ẩn', '- Nội dung "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"\n- Nút Thoát: đóng không lưu; nút Ở lại: quay về cửa sổ.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tạo mới', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho" (thiếu quyền thì nút ẩn).\nAfter:\n– Mở cửa sổ với các ô trống, Trạng thái = Hoạt động.'],
        ['Gõ Thứ tự', 'Change', 'During:\n– Bỏ ngay ký tự không phải chữ số, tối đa 9 chữ số.\nAfter:\n– Ô Tên kiện hiện "Kiện <thứ tự>".'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho".\nDuring:\n– Kiểm tra bắt buộc, Thứ tự là số nguyên lớn hơn 0, không trùng kiện khác (kể cả kiện Khóa).\n' + TRUOC_LUU + '\nAfter:\n– Ghi kiện, Tên kiện = "Kiện <thứ tự>".\n– Ghi nhận Tạo mới trong lịch sử.\n– Đóng cửa sổ, tải lại danh sách, báo "Thêm mới thành công."'],
        ['Bấm Lưu & Tiếp tục', 'Click', 'During:\n– Như nút Lưu.\n' + TRUOC_LUU + '\nAfter:\n– Ghi như nút Lưu, giữ cửa sổ, các ô về trống, Trạng thái về Hoạt động.'],
        ['Bấm Đóng / (x) / bấm ra ngoài', 'Click', 'After:\n– Chưa nhập gì → đóng cửa sổ.\n– Đã nhập → hiện hộp "Thông tin chưa lưu": Thoát thì đóng không lưu, Ở lại thì quay về cửa sổ.'],
    ],
})

# 2.4 Chỉnh sửa ------------------------------------------------------------------
EDIT_ROWS = [[r[0], r[1], r[2], r[3], r[4], 'Dữ liệu hiện tại', r[6]] for r in FORM_ROWS]
EDIT_ROWS[0] = EDIT_ROWS[0][:6] + [FORM_ROWS[0][6] + '\n- Đổi Thứ tự thì Tên kiện đổi theo (BR-04).']
EDIT_ROWS[2] = ['Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Dữ liệu hiện tại',
                'Chọn Khóa rồi Lưu = khóa kiện, ghi lịch sử Khóa riêng (BR-05).']
FR.append({
    'ten': 'Chỉnh sửa kiện', 'uc': 'uc_sua',
    'qtc': 'Validate dữ liệu, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Chỉnh sửa kiện'],
        ['Mô tả', 'Sửa Thứ tự (Tên kiện đổi theo) và Trạng thái của kiện đang Hoạt động, kể cả kiện đã được gắn vào lô hàng xuất kho (BR-04).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Kiện đang Hoạt động.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Sửa ở cột Hành động.\n2. Hệ thống mở cửa sổ "Sửa kiện" với dữ liệu hiện tại.\n3. Người dùng sửa và bấm Lưu.\n4. Hệ thống kiểm tra, ghi thay đổi, đặt lại Tên kiện theo Thứ tự mới.\n5. Ghi nhận Thay đổi thông tin (đổi Trạng thái ghi riêng Khóa) trong lịch sử.\n6. Đóng cửa sổ, báo "Cập nhật thành công."'],
        ['Dòng sự kiện phụ', '• Giữ nguyên Thứ tự của chính kiện → không báo trùng.\n• Kiện vừa bị người khác khóa → báo "Dữ liệu đã thay đổi, vui lòng tải lại".\n• Bấm Đóng khi đã sửa → hỏi "Thông tin chưa lưu".'],
    ],
    'menu_them': ' => Sửa {icon:btn_sua}',
    'ghi_chu_layout': POPUP % 'Sửa kiện',
    'anh': [('12_edit', 'Cửa sổ Sửa kiện')],
    'ui': ui(UI8, EDIT_ROWS + [
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', 'Lưu thay đổi rồi đóng cửa sổ.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng không lưu (đã sửa thì hỏi xác nhận). Cửa sổ Sửa không có nút Lưu & Tiếp tục.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện khi kiện Hoạt động và người dùng có quyền.\nAfter:\n– Tải dữ liệu kiện, mở cửa sổ; kiện không còn (vừa bị xoá) → báo "Dữ liệu đã thay đổi, vui lòng tải lại".'],
        ['Bấm Lưu', 'Click', 'Before:\n– Kiểm tra quyền, kiện phải đang Hoạt động.\nDuring:\n– Kiểm tra như Thêm mới (bỏ qua trùng với chính kiện).\n' + TRUOC_LUU + '\nAfter:\n– Ghi thay đổi, Tên kiện = "Kiện <thứ tự mới>".\n– Ghi nhận Thay đổi thông tin / Khóa trong lịch sử.\n– Đóng cửa sổ, tải lại danh sách, báo "Cập nhật thành công."'],
        ['Bấm Đóng / (x) / bấm ra ngoài', 'Click', 'After:\n– Chưa đổi gì → đóng; đã đổi → hỏi "Thông tin chưa lưu" (Thoát / Ở lại).'],
    ],
})

# 2.5 Xóa ---------------------------------------------------------------------------
FR.append({
    'ten': 'Xóa kiện', 'uc': 'uc_xoa',
    'qtc': 'Quy tắc Xóa, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xóa kiện'],
        ['Mô tả', 'Xóa hẳn kiện đang Hoạt động và chưa được gắn vào lô hàng của phiếu xuất kho nào (BR-06). Kiện đã được dùng thì dùng Khóa.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Kiện đang Hoạt động, chưa được gắn vào lô hàng xuất kho.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Xóa ở cột Hành động.\n2. Hệ thống hiện hộp "Xác nhận xóa": "Bạn có chắc muốn xóa kiện \'<Tên kiện>\'?"\n3. Người dùng bấm Xóa.\n4. Hệ thống ghi nhận Xóa trong lịch sử, xóa hẳn kiện.\n5. Tải lại danh sách, báo "Xóa thành công."'],
        ['Dòng sự kiện phụ', '• Bấm Hủy → đóng hộp, không thay đổi.\n• Kiện vừa bị khóa → "Không thể xóa kiện đang ở trạng thái khóa. Hãy mở khóa trước."\n• Kiện vừa được gắn vào lô hàng xuất kho → "Không thể xóa do dữ liệu đang được sử dụng."\n• Kiện vừa bị người khác xóa → "Dữ liệu đã thay đổi, vui lòng tải lại".'],
    ],
    'menu_them': ' => Xóa {icon:btn_xoa}',
    'ghi_chu_layout': POPUP % 'Xác nhận xóa',
    'anh': [('13_delete', 'Hộp xác nhận xóa kiện')],
    'ui': ui(UI4, [
        ['Nút Xóa (cột Hành động)', 'Button', 'Biểu tượng thùng rác; chỉ hiện khi kiện Hoạt động, chưa được gắn vào lô hàng xuất kho và người dùng có quyền.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận xóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn xóa kiện \'<Tên kiện>\'?"'],
        ['Nút Xóa', 'Button', 'Xác nhận xóa.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không xóa.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Bấm Xóa ở cột Hành động', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên kiện.'],
        ['Bấm Xóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền.\nDuring:\n– Kiện phải đang Hoạt động và chưa được gắn vào lô hàng xuất kho.\n' + TRUOC_LUU + '\nAfter:\n– Ghi nhận Xóa trong lịch sử, xóa hẳn kiện; Thứ tự của kiện dùng lại được.\n– Tải lại danh sách, báo "Xóa thành công."'],
        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.6 Khóa / Mở khóa -----------------------------------------------------------
FR.append({
    'ten': 'Khóa / Mở khóa kiện', 'uc': 'uc_khoa',
    'qtc': 'Quy tắc Khóa/Mở khóa, Thông báo, Quy định chung về danh mục, Quy tắc ghi lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Khóa / Mở khóa kiện'],
        ['Mô tả', 'Đổi trạng thái kiện giữa Hoạt động và Khóa. Kiện không có danh mục cha / con nên luôn khóa và mở khóa được, kể cả kiện đã được dùng (BR-05).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Khóa: kiện Hoạt động. Mở khóa: kiện đang Khóa.'],
        ['Dòng sự kiện chính', '1. Người dùng chọn Khóa (hoặc Mở khóa) ở cột Hành động.\n2. Hệ thống hiện hộp "Xác nhận khóa" / "Xác nhận mở khóa" kèm tên kiện.\n3. Người dùng bấm Khóa / Mở khóa.\n4. Hệ thống đổi trạng thái, ghi nhận Khóa / Mở khóa trong lịch sử.\n5. Tải lại danh sách, báo "Khóa thành công." / "Mở khóa thành công."'],
        ['Dòng sự kiện phụ', '• Bấm Hủy → không thay đổi.\n• Kiện đã bị người khác đổi trạng thái → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n• Sau khi Khóa: nút Sửa, Xóa ẩn; sau khi Mở khóa: nút Sửa hiện lại (Xóa hiện lại nếu kiện chưa được dùng).'],
    ],
    'menu_them': ' => Khóa {icon:btn_khoa_row} / Mở khóa {icon:btn_mokhoa_row}',
    'ghi_chu_layout': POPUP % 'Xác nhận khóa / Xác nhận mở khóa',
    'anh': [('14_lock', 'Hộp xác nhận khóa kiện'), ('15_unlock', 'Hộp xác nhận mở khóa kiện')],
    'ui': ui(UI4, [
        ['Nút Khóa (cột Hành động)', 'Button', '- Biểu tượng ổ khóa; hiện khi kiện Hoạt động, có quyền.\n- Dòng có nút Xóa thì Khóa nằm trong nút ba chấm "Hành động khác".'],
        ['Nút Mở khóa (cột Hành động)', 'Button', 'Biểu tượng ổ khóa mở; hiện khi kiện đang Khóa, có quyền.'],
        ['Tiêu đề hộp', 'Label', '"Xác nhận khóa" hoặc "Xác nhận mở khóa".'],
        ['Nội dung', 'Label', '"Bạn có chắc muốn khóa kiện \'<Tên kiện>\'?" / "Bạn có chắc muốn mở khóa kiện \'<Tên kiện>\'?"'],
        ['Nút Khóa / Mở khóa', 'Button', 'Xác nhận đổi trạng thái.'],
        ['Nút Hủy', 'Button', 'Đóng hộp, không thay đổi.'],
    ]),
    'ui_widths': UI4W,
    'events': [
        ['Chọn Khóa / Mở khóa', 'Click', 'After:\n– Hiện hộp xác nhận kèm tên kiện.'],
        ['Bấm Khóa / Mở khóa trong hộp', 'Click', 'Before:\n– Kiểm tra quyền.\nDuring:\n– Kiện đã ở trạng thái đích → "Trạng thái đã bị thay đổi. Vui lòng load lại trang".\n' + TRUOC_LUU + '\nAfter:\n– Đổi trạng thái, ghi nhận Khóa / Mở khóa trong lịch sử, tải lại danh sách, báo thành công.'],
        ['Bấm Hủy', 'Click', 'After:\n– Đóng hộp, không thay đổi.'],
    ],
})

# 2.7 Lịch sử --------------------------------------------------------------------
FR.append({
    'ten': 'Xem lịch sử thay đổi',
    'qtc': 'Quy tắc ghi lịch sử và hiển thị lịch sử.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem lịch sử thay đổi kiện'],
        ['Mô tả', 'Liệt kê các lần thao tác trên một kiện (Tạo mới, Thay đổi thông tin, Khóa, Mở khóa, Xóa), mới nhất ở trên, kèm người thực hiện, thời điểm, giá trị cũ → mới.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Lịch sử ở cột Hành động (hoặc Xem lịch sử trong cửa sổ Xem chi tiết).\n2. Hệ thống mở cửa sổ "Lịch sử thay đổi: <Tên kiện>" và liệt kê các mốc.'],
        ['Dòng sự kiện phụ', '• Lọc theo Loại hành động, Người thực hiện, Từ ngày / Đến ngày bằng nút Bộ lọc trong cửa sổ.\n• Các trường được ghi: Tên kiện, Thứ tự, Trạng thái.'],
    ],
    'menu_them': ' => Lịch sử {icon:btn_lichsu_row}',
    'ghi_chu_layout': POPUP % 'Lịch sử thay đổi',
    'anh': [('16_history', 'Cửa sổ Lịch sử thay đổi của kiện')],
    'ui': ui(UI6, [
        ['Nút Lịch sử (cột Hành động)', 'Button', 'Enable', 'Hiển thị', 'Luôn có ở mọi dòng (kể cả kiện Khóa); dòng có 4 nút thì nằm trong nút ba chấm.'],
        ['Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Lịch sử thay đổi: <Tên kiện>', ''],
        ['Nút Bộ lọc', 'Button', 'Enable', 'Thu gọn', 'Mở các ô lọc Loại hành động, Người thực hiện, Từ ngày, Đến ngày.'],
        ['Danh sách mốc', 'Table/Grid', 'Read-only', 'Theo dữ liệu', '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, loại hành động, "Người thực hiện: Họ tên — Phòng ban".\n- Dòng thay đổi: "<Trường>: giá trị cũ → giá trị mới".\n- Chưa có dữ liệu: "Chưa có lịch sử thao tác nào."'],
        ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Lịch sử', 'Click', 'After:\n– Tải lịch sử của kiện, mới nhất trên cùng.'],
        ['Chọn điều kiện ở Bộ lọc', 'Change', 'After:\n– Lọc lại các mốc; không có mốc khớp → "Không có lịch sử phù hợp bộ lọc."'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.8 Import ---------------------------------------------------------------------
FR.append({
    'ten': 'Import kiện từ file Excel', 'uc': 'uc_import',
    'qtc': 'Quy tắc Import file, Validate dữ liệu, Thông báo.',
    'gioi_thieu': [
        ['Tên chức năng', 'Import kiện từ file Excel'],
        ['Mô tả', 'Tạo nhiều kiện từ file Excel theo file mẫu. Mỗi dòng được kiểm tra và ghi như khi Tạo mới (tên tự đặt "Kiện <thứ tự>", ghi lịch sử) (BR-07).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Import Excel, hệ thống mở cửa sổ "Import kiện".\n2. Bấm Tải file mẫu (Mau_import_kien.xlsx), điền dữ liệu.\n3. Bấm Chọn file Excel, chọn file, bấm Load lên bảng: dữ liệu hiện ở bảng xem trước, ô Tổng = số dòng.\n4. Bấm Validate: hệ thống kiểm tra từng dòng (chưa ghi dữ liệu), hiện Tổng / Hợp lệ / Lỗi; dòng lỗi tô đỏ kèm lý do, dòng hợp lệ bị khóa.\n5. Sửa dòng lỗi rồi Validate lại, hoặc bấm Bỏ dòng lỗi.\n6. Khi không còn dòng lỗi, bấm Import: hệ thống ghi từng dòng, ghi nhận Tạo mới trong lịch sử, báo "Import thành công N kiện.", tải lại danh sách.'],
        ['Dòng sự kiện phụ', '• File quá 500 dòng dữ liệu → "File có X dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần."\n• Dòng vừa bị trùng với kiện người khác tạo trong lúc Import → bị bỏ qua, bảng kết quả "Import xong: a dòng thành công, b dòng lỗi bị bỏ qua" (nút Sao chép).\n• Bấm Xoá trạng thái validate để sửa lại cả dòng đã khóa.\n• Bấm Làm mới để làm lại từ đầu; Đóng để thoát.'],
    ],
    'menu_them': ' => Import Excel {icon:btn_import}',
    'ghi_chu_layout': POPUP % 'Import kiện',
    'anh': [('21_import_open', 'Cửa sổ Import kiện khi vừa mở'), ('22_import_loaded', 'Dữ liệu sau khi Load lên bảng'),
            ('23_import_validated', 'Kết quả Validate — dòng lỗi nêu rõ lý do')],
    'ui': ui(UI7I, [
        ['Nút Chọn file Excel', 'Button', 'Enable', '–', '–', 'Chọn file .xlsx, hiện tên file bên cạnh.'],
        ['Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Tải Mau_import_kien.xlsx: dòng 1 tên cột (cột bắt buộc có *), dòng 2 hướng dẫn, 2 dòng dữ liệu mẫu.'],
        ['Nút Load lên bảng', 'Button', 'Enable / Disable', '–', 'Disable', 'Bấm được khi đã chọn file; đọc file lên bảng xem trước.'],
        ['Nút Validate', 'Button', 'Enable / Disable', '–', 'Disable', 'Bấm được khi bảng có dữ liệu; kiểm tra từng dòng, chưa ghi dữ liệu.'],
        ['Nút Import', 'Button', 'Enable / Disable', '–', 'Disable', 'Chỉ bấm được khi đã Validate, còn ≥ 1 dòng hợp lệ và KHÔNG còn dòng lỗi.'],
        ['Ô Tổng / Hợp lệ / Lỗi', 'Label', 'Read-only', '–', 'Tổng: 0', 'Tổng hiện sau Load; Hợp lệ, Lỗi hiện sau Validate.'],
        ['Cột Thứ tự *', 'Table/Grid', 'Enable', 'Có', 'Theo file', '- Số nguyên lớn hơn 0, không trùng kiện đang có và không trùng dòng khác trong file.\n- Lỗi: "Thứ tự: Bắt buộc phải nhập" / "Thứ tự: Nhập số nguyên lớn hơn 0" / "Thứ tự: Số quá lớn" / "Thứ tự: Đã tồn tại" / "Thứ tự: Bị trùng trong file".'],
        ['Cột Trạng thái', 'Table/Grid', 'Enable', 'Không', 'Theo file', 'Hoạt động / Khóa; để trống = Hoạt động. Giá trị khác: "Trạng thái: Chỉ nhận Hoạt động hoặc Khóa".'],
        ['Nút Bỏ dòng lỗi', 'Button', 'Enable', '–', '–', 'Loại các dòng lỗi khỏi bảng xem trước.'],
        ['Nút Xoá trạng thái validate', 'Button', 'Enable', '–', '–', 'Mở khóa mọi dòng để sửa lại, phải Validate lại.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', 'Đóng cửa sổ.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Xoá file và bảng, làm lại từ đầu.'],
    ]),
    'ui_widths': UI7IW,
    'bang_cot': True,
    'events': [
        ['Bấm Load lên bảng', 'Click', 'During:\n– File không có dòng dữ liệu → "Không có dòng dữ liệu hợp lệ."\n– Quá 500 dòng → báo giới hạn 500 dòng.\nAfter:\n– Hiện dữ liệu lên bảng xem trước, ô Tổng = số dòng.'],
        ['Bấm Validate', 'Click', 'Before:\n– Kiểm tra quyền "Quản lý kho".\nDuring:\n– Mỗi dòng kiểm như Tạo mới; trùng Thứ tự giữa các dòng trong file ("Bị trùng trong file").\nAfter:\n– Hiện Tổng / Hợp lệ / Lỗi, toast "Validate xong: X hợp lệ, Y không hợp lệ" (hoặc "Validate thành công"); dòng lỗi tô đỏ kèm lý do, dòng hợp lệ bị khóa.'],
        ['Bấm Import', 'Click', 'Before:\n– Đã Validate, không còn dòng lỗi.\nDuring:\n– Hệ thống kiểm lại từng dòng ngay trước khi ghi.\n' + TRUOC_LUU + '\nAfter:\n– Ghi từng dòng như Tạo mới (Tên kiện = "Kiện <thứ tự>"), ghi nhận Tạo mới trong lịch sử.\n– Báo "Import thành công N kiện.", đóng cửa sổ, tải lại danh sách; có dòng bị bỏ qua thì hiện bảng kết quả.'],
        ['Bấm Bỏ dòng lỗi / Xoá trạng thái validate', 'Click', 'After:\n– Bỏ dòng lỗi khỏi bảng / mở khóa các dòng để sửa.'],
        ['Bấm Đóng / Làm mới', 'Click', 'After:\n– Đóng cửa sổ / xoá dữ liệu đang xem để làm lại.'],
    ],
})

# 2.9 Xuất Excel -------------------------------------------------------------------
FR.append({
    'ten': 'Xuất danh sách ra Excel', 'uc': 'uc_xuat',
    'qtc': 'Quy tắc Excel, Cấu hình cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất danh sách kiện ra Excel'],
        ['Mô tả', 'Xuất toàn bộ kiện khớp bộ lọc đang áp dụng (mọi trang) ra file Excel, người dùng chọn trường và thứ tự cột (BR-09).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng lọc danh sách (nếu cần), bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất file", tích sẵn các cột đang hiện trên bảng.\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự rồi bấm Xuất file.\n4. Hệ thống tải file danh_sach_kien.xlsx, báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Kết quả rỗng vẫn xuất file (tiêu đề + tên cột).\n• Ô Ngày tạo đang sai (Từ > Đến) → báo lỗi, không xuất.\n• Lỗi hệ thống → "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': POPUP % 'Chọn trường xuất file',
    'anh': [('20_export', 'Cửa sổ Chọn trường xuất file')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '"Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file."'],
        ['Danh sách trường', 'Table/Grid', 'Enable', 'Tích theo cột đang hiện', '7 trường: Tên kiện, Thứ tự, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật, Trạng thái. Mỗi trường có ô tích và biểu tượng ☰ kéo đổi vị trí.'],
        ['Nút Chọn tất cả', 'Button', 'Enable', '–', 'Tích mọi trường.'],
        ['Nút Bỏ chọn hết', 'Button', 'Enable', '–', 'Bỏ tích mọi trường.'],
        ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn x/7 trường', ''],
        ['Nút Xuất file', 'Button', 'Enable / Disable', 'Enable', 'Tải file; không bấm được khi không còn trường nào được chọn.'],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Đóng cửa sổ, không xuất.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ, tích sẵn theo cột đang hiện.'],
        ['Bấm Xuất file', 'Click', 'During:\n– Ô Ngày tạo sai → báo "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", không xuất.\n' + TRUOC_LUU + '\nAfter:\n– Tải file danh_sach_kien.xlsx: tiêu đề "Danh sách kiện", cột theo thứ tự đã chọn, mọi dòng khớp bộ lọc, giữ thứ tự sắp xếp đang chọn; báo "Xuất Excel thành công".'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.10 Xem chi tiết ----------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết kiện', 'uc': 'uc_xem',
    'qtc': 'Màn Xem chi tiết, Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết kiện'],
        ['Mô tả', 'Xem toàn bộ thông tin một kiện ở chế độ chỉ đọc, kèm khối Lịch sử. Xem được cả kiện đang Khóa.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm vào Tên kiện trên bảng.\n2. Hệ thống mở cửa sổ "Xem chi tiết kiện", mọi ô chỉ đọc.\n3. Bấm Xem lịch sử để mở khối Lịch sử ngay trong cửa sổ.'],
        ['Dòng sự kiện phụ', '• Kiện vừa bị xoá → báo "Dữ liệu đã thay đổi, vui lòng tải lại", không mở cửa sổ.'],
    ],
    'menu_them': ' => Bấm Tên kiện',
    'ghi_chu_layout': POPUP % 'Xem chi tiết kiện',
    'anh': [('17_detail', 'Cửa sổ Xem chi tiết kiện ở chế độ chỉ đọc'),
            ('17b_detail_history', 'Khối Lịch sử trong cửa sổ Xem chi tiết')],
    'ui': ui(UI6, [
        ['Thứ tự, Tên kiện', 'Textbox', 'Read-only', 'Dữ liệu hiện tại', 'Không có dấu (*).'],
        ['Trạng thái', 'Dropdown', 'Read-only', 'Dữ liệu hiện tại', ''],
        ['Khối Lịch sử', 'Table/Grid', 'Enable', 'Thu gọn', '- Nút Xem lịch sử mở khối, hiện số mốc.\n- Nút Làm mới tải lại, Thu gọn đóng khối, Bộ lọc lọc mốc như mục 2.7.'],
        ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ. Không có nút Lưu.'],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Tên kiện', 'Click', 'After:\n– Tải dữ liệu, mở cửa sổ chỉ đọc.'],
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
        ['Dòng sự kiện phụ', '• Cột STT, Tên kiện, Hành động là cột khóa: không bỏ tích được.\n• Bấm Đóng → bỏ các thay đổi vừa chỉnh.'],
    ],
    'menu_them': ' => Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': POPUP % 'Tuỳ chỉnh cột',
    'anh': [('25_colcfg', 'Cửa sổ Tuỳ chỉnh cột — STT, Tên kiện, Hành động bị khóa')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '"Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng."'],
        ['Danh sách cột', 'Table/Grid', 'Enable', 'Theo cấu hình đã lưu', '9 cột theo thứ tự trên bảng, mặc định hiện cả 9.'],
        ['Cột khóa', 'Table/Grid', 'Disable', 'Luôn tích', 'STT, Tên kiện, Hành động: ô tích xám, không ẩn được; STT, Tên kiện còn có biểu tượng khóa, không đổi vị trí được.'],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Tích / bỏ tích mọi cột (trừ cột khóa).'],
        ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn x/9 cột', ''],
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
    'menu': [('Kho', 'menu_phanhe'), ('Danh mục', 'menu_nhom'), ('Kiện', 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu chức năng.',
        'Làm rõ cách đặt tên kiện tự động theo Thứ tự, ràng buộc Thứ tự duy nhất trong toàn danh mục, phạm vi dùng chung mọi công ty, điều kiện Xóa (kiện chưa được gắn vào lô hàng xuất kho) và Khóa / Mở khóa.',
    ],
    'thuat_ngu': [
        ['Kiện', 'Đơn vị đóng gói hàng khi xuất kho; mỗi lô hàng của phiếu xuất kho được gắn vào một hoặc nhiều kiện để đếm số kiện giao.'],
        ['Thứ tự', 'Số nguyên lớn hơn 0 người dùng nhập, duy nhất trong danh mục; quyết định Tên kiện.'],
        ['Tên kiện', 'Hệ thống tự đặt "Kiện <thứ tự>", ví dụ Thứ tự 7 → "Kiện 7".'],
        ['Lô hàng xuất kho', 'Một dòng hàng xuất theo lô trong phiếu xuất kho; kiện gắn vào lô hàng thì coi là "đã được dùng".'],
        ['Hoạt động', 'Trạng thái kiện dùng được.'],
        ['Khóa', 'Kiện vẫn nằm trong danh mục, xem được lịch sử nhưng ngừng sử dụng.'],
    ],
    'quyen_truoc': ['Màn hình dùng một quyền duy nhất "Quản lý kho" (nhóm Danh mục kho) cho cả xem lẫn thao tác; quyền này dùng chung cho 7 màn Danh mục của phân hệ Kho. Quyền được gán vào vai trò theo công ty.'],
    'quyen_rows': [['Quản lý kho', 'Xem danh sách, tìm kiếm, xem chi tiết, lịch sử, tùy chỉnh cột, xuất Excel; Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Import Excel.']],
    'ma_tran': [['Chức năng', 'Quản lý kho', 'Không có quyền']] + [[f, 'Có', 'Không'] for f in [
        'FR-01 Xem danh sách kiện', 'FR-02 Tìm kiếm và lọc', 'FR-03 Thêm mới kiện', 'FR-04 Chỉnh sửa kiện',
        'FR-05 Xóa kiện', 'FR-06 Khóa / Mở khóa kiện', 'FR-07 Xem lịch sử thay đổi',
        'FR-08 Import kiện từ file Excel', 'FR-09 Xuất danh sách ra Excel', 'FR-10 Xem chi tiết kiện',
        'FR-11 Tùy chỉnh cột hiển thị']],
    'ma_tran_widths': [2.6, 1.2, 1.2],
    'quyen_sau': ['Phạm vi dữ liệu: kiện là danh mục dùng chung mọi công ty — mọi người dùng có quyền "Quản lý kho" thấy và thao tác được mọi kiện, không có ô lọc Công ty (BR-01).'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Phạm vi dữ liệu', [
            '– Kiện không thuộc công ty, kho hay nhà kho nào; người dùng có quyền thấy và thao tác mọi kiện.',
            '– Không có ô lọc Công ty.'], ['Xem danh sách', 'Xuất Excel', 'Chỉnh sửa', 'Xóa', 'Khóa / Mở khóa']),
        ('BR-02', 'Thứ tự', [
            '– Bắt buộc, số nguyên lớn hơn 0; ô nhập chỉ nhận chữ số, tối đa 9 chữ số.',
            '– Duy nhất trong toàn danh mục, tính cả kiện đang Khóa.',
            '– Thông báo: "Bắt buộc phải nhập", "Nhập số nguyên lớn hơn 0", "Số quá lớn", "Đã tồn tại".'], ['Thêm mới', 'Chỉnh sửa', 'Import']),
        ('BR-03', 'Tên kiện tự đặt', [
            '– Tên kiện = "Kiện <thứ tự>", người dùng không nhập; ô Tên kiện trên cửa sổ chỉ đọc, hiện trước tên ngay khi gõ Thứ tự.',
            '– Vì Thứ tự duy nhất nên không có 2 kiện cùng tên.',
            '– Sắp xếp theo Tên kiện là sắp theo con số Thứ tự.'], ['Thêm mới', 'Chỉnh sửa', 'Import', 'Xem danh sách']),
        ('BR-04', 'Sửa kiện', [
            '– Chỉ sửa kiện đang Hoạt động; kiện Khóa phải Mở khóa trước.',
            '– Sửa được cả kiện đã được gắn vào lô hàng xuất kho; đổi Thứ tự thì Tên kiện đổi theo.',
            '– Lô hàng đã gắn kiện lưu sẵn tên kiện lúc gắn, nên đổi Thứ tự không làm đổi tên kiện ghi trên lô hàng cũ.'], ['Chỉnh sửa']),
        ('BR-05', 'Điều kiện Khóa / Mở khóa', [
            '– Kiện không có danh mục cha / con: kiện Hoạt động luôn khóa được (kể cả đã được dùng), kiện Khóa luôn mở khóa được.',
            '– Đổi Trạng thái sang Khóa trong cửa sổ Sửa cũng là khóa kiện, ghi lịch sử Khóa riêng.',
            '– Kiện đang Khóa: ẩn Sửa, Xóa.'], ['Khóa / Mở khóa', 'Chỉnh sửa']),
        ('BR-06', 'Điều kiện và cách Xóa', [
            '– Chỉ xóa kiện đang Hoạt động và CHƯA được gắn vào lô hàng của phiếu xuất kho nào; kiện đã được dùng thì dùng Khóa.',
            '– Xóa là xóa hẳn: kiện biến mất khỏi danh sách, Thứ tự dùng lại được để tạo kiện mới.',
            '– Lịch sử ghi nhận Xóa trước khi xóa.'], ['Xóa']),
        ('BR-07', 'Import', [
            '– Mỗi dòng kiểm và ghi như Tạo mới (BR-02, BR-03); Trạng thái để trống = Hoạt động.',
            '– Trùng Thứ tự giữa các dòng trong file → "Bị trùng trong file".',
            '– Tối đa 500 dòng dữ liệu mỗi lần; chỉ Import khi đã Validate và không còn dòng lỗi.'], ['Import']),
        ('BR-08', 'Lọc Ngày tạo', ['– Ngày tạo Từ lớn hơn Đến → báo đỏ "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", xoá bảng, không tải dữ liệu và không xuất Excel.'], ['Tìm kiếm và lọc', 'Xuất Excel']),
        ('BR-09', 'Xuất Excel', ['– Xuất mọi dòng khớp bộ lọc đang áp dụng (không chỉ trang đang xem), cột theo thứ tự người dùng chọn; tên file danh_sach_kien.xlsx.'], ['Xuất Excel']),
    ],
    'phan5': {
        'cau_dan': 'Hiện chưa có màn hình nào có ô chọn Kiện. Kiện được gắn vào lô hàng của phiếu xuất kho; màn hình dưới đây dùng dữ liệu kiện đã gắn này.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng có quyền "Quản lý kho"',
    'mains': [('FR-01', 'Xem danh sách kiện', 'view'), ('FR-03', 'Thêm mới kiện', 'crud'),
              ('FR-04', 'Chỉnh sửa kiện', 'crud'), ('FR-05', 'Xóa kiện', 'action'),
              ('FR-06', 'Khóa / Mở khóa kiện', 'action'), ('FR-08', 'Import kiện từ file Excel', 'io'),
              ('FR-09', 'Xuất danh sách kiện ra Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc kiện', 'view'), ('FR-10', 'Xem chi tiết kiện', 'view'),
             ('FR-11', 'Tùy chỉnh cột hiển thị', 'view'), ('FR-07', 'Xem lịch sử thay đổi', 'view')],
    'rieng': [('FR-03', 'Thêm mới kiện', 'crud', 'uc_them'), ('FR-04', 'Chỉnh sửa kiện', 'crud', 'uc_sua'),
              ('FR-05', 'Xóa kiện', 'action', 'uc_xoa'), ('FR-06', 'Khóa / Mở khóa kiện', 'action', 'uc_khoa'),
              ('FR-08', 'Import kiện từ file Excel', 'io', 'uc_import'),
              ('FR-09', 'Xuất danh sách kiện ra Excel', 'io', 'uc_xuat'), ('FR-10', 'Xem chi tiết kiện', 'view', 'uc_xem')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', L.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)

# -*- coding: utf-8 -*-
"""SRS - Báo cáo hàng có thể bán theo công ty (form Danh mục quốc gia + quy tắc màn báo cáo của skill srs-documenter).

Nguồn (code HRM hiện tại):
  FE hrm-client/pages/lookup/stock-companies/{index.vue, components/IncomingStockModal.vue, StockVoucherCell.vue,
     export-excel.js}, utils/stock-voucher-link.js, components/subsystem-menu/lookup.js, utils/filterRequiredErrors.js,
     components/modal/{export-fields-modal, column-customization-modal}.vue, components/report/ReportInfoTip.vue
  BE Modules/Finance/Http/Controllers/V1/StockCompanyController.php, Services/{SellableStockReportService,
     IncomingStockService}.php
  Ảnh: capture.js (dev-hrm, 02/11/2026). Phần 5: dò code FE/BE + menu.
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _lib_report as R  # noqa: E402
L = R.L

TEN = 'Báo cáo hàng có thể bán theo công ty'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q = 'Người dùng đã đăng nhập (màn hình không gắn quyền riêng)'
DK = '1. Người dùng đăng nhập thành công.\n2. Phân hệ Thông báo đang được bật ở màn Cài đặt phân hệ.'
POPUP = 'Cửa sổ %s được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'

UI7 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả']
UI7W = [0.55, 1.25, 0.85, 0.8, 0.95, 0.85, 2.6]
UI8 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả']
UI8W = [0.55, 1.15, 0.85, 0.75, 0.95, 0.65, 0.85, 2.3]


def ui(header, rows):
    return [header] + [[str(i + 1)] + r for i, r in enumerate(rows)]


TIP = {  # nguyên văn COLUMN_TIPS trong index.vue
    'stt': 'Số thứ tự mặt hàng • Đánh liên tục qua các trang.',
    'ten': 'Tên hàng hóa • Chỉ hiện hàng hóa đang có tồn, hàng gửi, hàng giữ hoặc đang có đề nghị xuất kho của công ty tại các kho đang lọc.',
    'model': 'Model của hàng hóa • Theo danh mục hàng hóa.',
    'ma': 'Mã hàng hóa • Theo danh mục hàng hóa.',
    'th': 'Thương hiệu của hàng hóa • Theo danh mục hàng hóa.',
    'dvt': 'Đơn vị tính dùng để hiển thị số lượng trên dòng • Mặc định là đơn vị tính cơ bản. • Đổi đơn vị tính thì mọi số trên dòng = số theo đơn vị cơ bản ÷ hệ số quy đổi (làm tròn 2 chữ số thập phân). • Dòng Tổng luôn tính theo đơn vị tính cơ bản.',
    'cs': 'Số lượng còn có thể bán của công ty tại các kho đang lọc • SL tồn có thể bán = Tổng tồn − SL KM − Tổng gửi − Tổng giữ − Tổng đang xuất (Hàng bán). • Kết quả âm thì tính là 0.',
    'ce': 'Số lượng hàng khuyến mại còn có thể xuất • SL KM có thể xuất = SL KM − Tổng đang xuất (Hàng KM). • Kết quả âm thì tính là 0.',
    'tt': 'Tổng tồn kho kế toán của công ty tại các kho đang lọc • Gồm cả tồn ở kho khuyến mại. • Bỏ trống ô lọc Kho = mọi kho của công ty.',
    'hdv': 'Hàng đã đặt mua / chờ nhập, đang trên đường về • Tính trên toàn hệ thống, không phân theo công ty và kho đang lọc.',
    'kd': 'Hàng đang về do kinh doanh đặt • KD đặt = SL đang về theo nhân viên của đơn đặt hàng nhập khẩu đã duyệt + SL đang về theo nhân viên của đơn đặt hàng trong nước đã duyệt + SL trên yêu cầu nhập hàng mua trong nước đã đề nghị, chưa hạch toán. • Đơn đặt hàng chỉ tính phát sinh từ 01/07/2024.',
    'tk': 'Hàng đang về theo đơn đặt hàng và chứng từ nhập kho • Tồn kho = SL đang về của đơn đặt hàng nhập khẩu, đơn đặt hàng trong nước (đã duyệt), tổng hợp đặt hàng nhập khẩu, tổng hợp đặt hàng trong nước + SL trên yêu cầu nhập hàng, đề nghị nhập kho, phiếu nhập kho chưa hoàn tất. • Chỉ tính chứng từ phát sinh từ 01/07/2024. • Bấm số để xem danh sách chứng từ.',
    'km': 'Tồn ở kho khuyến mại của công ty tại các kho đang lọc • Kho khuyến mại theo thiết lập của công ty.',
    'gui': 'Tổng hàng gửi của công ty tại các kho đang lọc • Theo số lượng hàng gửi đang ghi nhận tại kho.',
    'giu': 'Tổng hàng đang giữ của công ty • Tính trên MỌI kho của công ty, không theo ô lọc Kho.',
    'dx': 'Hàng trên đề nghị xuất kho chưa hoàn tất của công ty tại các kho đang lọc • Không tính đề nghị xuất kho đang tạo hoặc đã hủy.',
    'dxb': 'Phần đang xuất là hàng bán • Hàng bán = SL cần xuất − Hàng KM đang xuất − phần xuất từ hàng giữ − phần xuất từ hàng gửi.',
    'dxk': 'Phần đang xuất là hàng khuyến mại • Hàng KM = SL cần xuất trên đề nghị xuất kho loại Xuất khuyến mại (HĐ hãng).',
    'kho': 'Số liệu riêng của kho này (chỉ hiện kho có số liệu) • SL tồn: tồn kho kế toán của công ty tại kho, gồm cả kho khuyến mại. • SL KM: tồn ở kho khuyến mại của công ty tại kho. • SL gửi: hàng gửi của công ty tại kho. • Đang xuất - Hàng bán = SL cần xuất − phần xuất từ hàng giữ − phần xuất từ hàng gửi − Hàng KM đang xuất. • Đang xuất - Hàng KM: SL cần xuất trên đề nghị xuất kho loại Xuất khuyến mại (HĐ hãng). • Các cột theo kho chỉ hiện số dương.',
    'title': 'Tra cứu số lượng hàng hóa còn có thể bán của một công ty tại các kho đã chọn (bỏ trống = mọi kho của công ty), kèm tồn, hàng gửi, hàng giữ, hàng đang xuất và hàng đang về.',
}


def ic(key):
    return '- Icon ⓘ: “%s”' % TIP[key]


# ------------------------------------------------------------------ Phần 5 (dò code 02/11/2026)
P5 = [
    ('Nguồn số liệu — tồn kho', 'Khai báo tồn kho đầu kỳ', 'Kho => Tồn kho đầu kỳ'),
    ('Nguồn số liệu — tồn kho', 'Phiếu nhập hàng (ghi tăng tồn kho; loại Nhập hàng gửi ghi tăng hàng gửi)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
    ('Nguồn số liệu — tồn kho', 'Phiếu xuất hàng (ghi giảm tồn kho)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ('Nguồn số liệu — tồn kho', 'Phiếu điều chuyển hàng', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Điều chuyển'),
    ('Nguồn số liệu — tồn kho', 'Danh sách hàng mượn / Phiếu xuất hàng mượn', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng'),
    ('Nguồn số liệu — hàng giữ', 'Phiếu xuất giữ (sinh hàng giữ)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng'),
    ('Nguồn số liệu — hàng giữ', 'Phiếu hủy hàng giữ / Phiếu huỷ hàng giữ kế toán (giảm hàng giữ)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng'),
    ('Nguồn số liệu — đang xuất', 'Đề nghị xuất kho', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng; Kho => Xuất kho (Phiếu đề nghị xuất kho)'),
    ('Nguồn số liệu — hàng đang về', 'Yêu cầu nhập hàng (mở được từ popup Hàng đang về)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
    ('Nguồn số liệu — hàng đang về', 'Đề nghị nhập kho (mở được từ popup Hàng đang về)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng; Kho => Nhập kho (Phiếu đề nghị nhập kho)'),
    ('Nguồn số liệu — hàng đang về', 'Phiếu nhập kho', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng; Kho => Nhập kho'),
    ('Danh mục tham chiếu', 'Kho kế toán (gắn kho vật lý với công ty — quyết định danh sách ô Kho và nhóm cột theo kho)', 'Kho => Danh mục'),
    ('Danh mục tham chiếu', 'Kho vật lý', 'Kho => Danh mục'),
    ('Danh mục tham chiếu', 'Khai Quy chế – Cấu hình (kho khuyến mại của công ty)', 'Tài chính'),
    ('Danh mục tham chiếu', 'Dữ liệu hàng hoá công ty (tên, mã, model, thương hiệu, đơn vị tính)', 'Danh mục dùng chung => Hàng hoá => Hàng hoá, vật tư'),
    ('Danh mục tham chiếu', 'Tính chất hàng hóa, Hãng sản xuất, Thương hiệu, Model (nguồn các ô lọc)', 'Danh mục dùng chung => Hàng hoá => Phân loại hàng hoá'),
    ('Màn cùng nguồn số liệu', 'Danh sách hàng giữ', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng'),
    ('Màn cùng nguồn số liệu', 'Báo cáo tồn kho chi tiết / tổng hợp theo mặt hàng, Báo cáo tồn kho theo vị trí, Báo cáo tồn theo kho (dùng chung nguồn ô lọc nhóm / tính chất / loại / thương hiệu / hãng)', 'Kho => Báo cáo kho'),
]

# ------------------------------------------------------------------ dữ liệu SRS
FR = []

# 2.1 Xem báo cáo ----------------------------------------------------------------
COT_SO = [
    ['Cột SL tồn có thể bán', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', [
        '- Số lượng còn bán được của công ty tại các kho đang lọc (BR-04)', '- Sắp xếp được', '- Cột khóa, không ẩn được', ic('cs')]],
    ['Cột SL KM có thể xuất', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', [
        '- Hàng khuyến mại còn xuất được (BR-05)', ic('ce')]],
    ['Cột Tổng tồn', 'Table/Grid', 'Read-only', 'Số', 'Theo dữ liệu', [
        '- Tồn kho kế toán của công ty tại các kho đang lọc, gồm cả kho khuyến mại', '- Sắp xếp được', ic('tt')]],
    ['Nhóm cột Hàng đang về', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
        '- Tiêu đề gộp 2 cột KD đặt, Tồn kho', '- Số tính trên toàn hệ thống, không theo công ty / kho đang lọc (BR-08)', ic('hdv')]],
    ['Cột KD đặt', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', ['- Hàng đang về do kinh doanh đặt', ic('kd')]],
    ['Cột Tồn kho (Hàng đang về)', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', [
        '- Hàng đang về theo đơn đặt hàng và chứng từ nhập kho',
        '- Số khác 0 hiện dạng liên kết. Bấm số → mở popup Hàng đang về của mặt hàng (mục 2.4)',
        '- Số 0: ô trống, không bấm được', ic('tk')]],
    ['Cột SL KM', 'Table/Grid', 'Read-only', 'Số', 'Theo dữ liệu', ['- Tồn ở kho khuyến mại của công ty tại các kho đang lọc', ic('km')]],
    ['Cột Tổng gửi', 'Table/Grid', 'Read-only', 'Số', 'Theo dữ liệu', ['- Hàng gửi của công ty tại các kho đang lọc', ic('gui')]],
    ['Cột Tổng giữ', 'Table/Grid', 'Read-only', 'Số', 'Theo dữ liệu', ['- Hàng đang giữ của công ty trên MỌI kho (BR-07)', ic('giu')]],
    ['Nhóm cột Tổng đang xuất', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Tiêu đề gộp 2 cột Hàng bán, Hàng KM', ic('dx')]],
    ['Cột Hàng bán (Tổng đang xuất)', 'Table/Grid', 'Read-only', '> 0', 'Theo dữ liệu', ['- Chỉ hiện số dương, số 0 hoặc âm để trống', ic('dxb')]],
    ['Cột Hàng KM (Tổng đang xuất)', 'Table/Grid', 'Read-only', 'Số', 'Theo dữ liệu', [ic('dxk')]],
    ['Nhóm cột theo từng kho', 'Table/Grid', 'Read-only', '> 0', 'Theo dữ liệu', [
        '- Mỗi kho 1 nhóm, tiêu đề là mã kho (rê chuột hiện “Mã - Tên kho”), xếp theo mã kho',
        '- Chỉ hiện kho có số liệu khác 0 ở dòng Tổng (BR-11)',
        '- 5 cột con: SL tồn, SL KM, SL gửi, Đang xuất – Hàng bán, Đang xuất – Hàng KM',
        '- Chỉ hiện số dương', ic('kho')]],
]
UI_XEM = [
    ['Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Báo cáo hàng có thể bán theo công ty', ['- Trên thanh đầu trang', '- Icon ⓘ: “%s”' % TIP['title']]],
    ['Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Theo công ty đang chọn', ['- “Báo cáo hàng có thể bán theo công ty — <Tên công ty đang chọn>”', '- Chưa chọn công ty: không có phần tên công ty']],
    ['Nút Xuất Excel', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', ['- Mở cửa sổ “Chọn trường xuất Excel” (mục 2.5)', '- Ẩn khi ô Tồn theo công ty đang trống', '- Không bấm được khi đang xuất file']],
    ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', '–', 'Hiển thị', ['- Biểu tượng cột, mở cửa sổ “Tuỳ chỉnh cột” (mục 2.6)']],
    ['Bảng chi tiết báo cáo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
        '- Tiêu đề 2–3 tầng, dính trên cùng khi cuộn', '- Dòng Tổng nằm ngay dưới tiêu đề, sau đó là các dòng mặt hàng',
        '- Cột: STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn có thể bán, SL KM có thể xuất, Tổng tồn, Hàng đang về (KD đặt, Tồn kho), SL KM, Tổng gửi, Tổng giữ, Tổng đang xuất (Hàng bán, Hàng KM), nhóm cột theo từng kho — mỗi cột mô tả ở 1 dòng bên dưới',
        '- Số theo chuẩn 1,234,567.89 (tối đa 2 số lẻ); số 0 để trống']],
    ['Dòng Tổng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
        '- Nhãn “Tổng (N mặt hàng, theo ĐVT cơ bản)”: N = số mặt hàng khớp bộ lọc',
        '- Mỗi ô số = tổng của cột trên TOÀN bộ kết quả lọc (mọi trang), theo đơn vị tính cơ bản (BR-09)',
        '- Không đổi khi người dùng đổi ĐVT trên dòng']],
    ['Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Đánh liên tục qua các trang', '- Cột khóa', ic('stt')]],
    ['Cột Tên hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Sắp xếp được (mặc định sắp theo cột này tăng dần)', '- Tên dài tự xuống dòng', '- Cột khóa', ic('ten')]],
    ['Cột Model', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Sắp xếp được', '- Hàng chưa có model: để trống', ic('model')]],
    ['Cột Mã hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Sắp xếp được', ic('ma')]],
    ['Cột Thương hiệu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Sắp xếp được', ic('th')]],
    ['Cột ĐVT', 'Dropdown', 'Enable', 'Đơn vị tính của hàng', 'Đơn vị cơ bản', [
        '- Mỗi dòng 1 ô chọn, lựa chọn dạng “Tên đơn vị (xHệ số)”; đơn vị cơ bản không ghi hệ số',
        '- Mặc định: đơn vị cơ bản', '- Đổi đơn vị → số trên dòng đổi theo (mục 2.3)', '- Cột khóa', ic('dvt')]],
] + COT_SO + [
    ['Thông báo bảng trống', 'Label', 'Hiển thị', '–', 'Ẩn', ['- Chưa chọn công ty: “Chọn công ty để xem báo cáo.”', '- Không có mặt hàng khớp: “Không có dữ liệu phù hợp bộ lọc.”', '- Đang tải: “Đang tải dữ liệu...”']],
    ['Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', '10 dòng/trang', ['- Chân bảng “Hiển thị a–b / N”', '- Ô “Số dòng/trang:” và nút chuyển trang']],
    ['Thông báo lỗi', 'Toast / Alert', 'Ẩn', '–', 'Ẩn', ['- Lỗi tải dữ liệu: “Lỗi khi tải dữ liệu”']],
]

DATA_XEM = R.numbered(R.DATA_HEAD, [
    ('Tập dữ liệu (dòng mặt hàng)', ['Mặt hàng có dòng tồn kho kế toán tại kho kế toán của công ty đang chọn (thuộc các kho đang lọc), khớp các ô lọc hàng hóa, và tổng (Tổng tồn + SL KM + Tổng gửi + SL trên đề nghị xuất kho chưa hoàn tất + Tổng giữ) > 0 (BR-02).', 'Thời điểm số liệu: tức thời, lúc bấm Tìm kiếm / mở màn — báo cáo không có kỳ.'], TIP['ten']),
    ('Dòng Tổng', ['Cộng từng cột của MỌI dòng khớp bộ lọc (không chỉ trang đang xem), theo đơn vị tính cơ bản. N = số dòng mặt hàng.', 'Ô SL tồn có thể bán của dòng Tổng = tổng các dòng (mỗi dòng đã kéo âm về 0), nên có thể khác “Tổng tồn − SL KM − Tổng gửi − Tổng giữ − Hàng bán” tính trên dòng Tổng.'], '—'),
    ('SL tồn có thể bán', ['= Tổng tồn − SL KM − Tổng gửi − Tổng giữ − Tổng đang xuất (Hàng bán). Âm thì ghi 0.'], TIP['cs']),
    ('SL KM có thể xuất', ['= SL KM − Tổng đang xuất (Hàng KM). Âm thì ghi 0.'], TIP['ce']),
    ('Tổng tồn', ['Cộng số lượng tồn kho kế toán của công ty ở mọi kho kế toán gắn với các kho vật lý đang lọc (gồm cả kho khuyến mại).', 'Bỏ trống ô Kho = mọi kho có kho kế toán của công ty.'], TIP['tt']),
    ('Hàng đang về – KD đặt', ['Cộng: SL đang về theo nhân viên trên đơn đặt hàng nhập khẩu đã duyệt (dòng nhân viên chưa hủy, phát sinh sau 01/07/2024) + SL đang về theo nhân viên trên đơn đặt hàng trong nước đã duyệt (sau 01/07/2024) + SL trên yêu cầu nhập hàng loại Mua hàng trong nước không ở trạng thái Chờ duyệt / Đang tạo / Đã hạch toán / Đã hủy (không giới hạn ngày).', 'Không lọc theo công ty, kho; cộng theo SL ghi trên chứng từ, không quy đổi đơn vị (BR-08).'], TIP['kd']),
    ('Hàng đang về – Tồn kho', ['Cộng 7 nguồn, chứng từ phát sinh sau 01/07/2024: đơn đặt hàng nhập khẩu đã duyệt (SL đang về > 0); đơn đặt hàng trong nước đã duyệt (SL đang về > 0); tổng hợp đặt hàng nhập khẩu và tổng hợp đặt hàng trong nước ở trạng thái đang hiệu lực (SL đang về); yêu cầu nhập hàng (trừ các loại mua hàng nước ngoài / trong nước, nhập gửi; không ở trạng thái Chờ duyệt / Đang tạo / Đã hạch toán / Đã hủy); đề nghị nhập kho loại Nhập tách chưa hạch toán / chưa hủy; phiếu nhập kho loại Nhập ghép đang chờ duyệt / đang hạch toán.', 'Tổng âm thì ghi 0. Không lọc theo công ty, kho.', 'Khớp số: = cột SL cộng trong popup Hàng đang về (“Tổng SL” ở chân popup).'], TIP['tk']),
    ('SL KM', ['Cộng tồn kho kế toán của công ty ở các kho kế toán được khai là kho khuyến mại của công ty (Khai Quy chế – Cấu hình) và thuộc các kho đang lọc.'], TIP['km']),
    ('Tổng gửi', ['Cộng số lượng hàng gửi đang ghi nhận của công ty tại các kho đang lọc (hàng gửi sinh từ phiếu nhập hàng loại Nhập hàng gửi).'], TIP['gui']),
    ('Tổng giữ', ['Cộng số lượng hàng đang giữ của công ty trên MỌI kho, không theo ô lọc Kho (BR-07).'], TIP['giu']),
    ('Tổng đang xuất – Hàng bán', ['Trên các đề nghị xuất kho của công ty tại kho đang lọc, chưa hoàn tất, không ở trạng thái Đang tạo / Đã hủy, dòng hàng còn cần xuất: = SL cần xuất − Hàng KM đang xuất − phần xuất từ hàng giữ − phần xuất từ hàng gửi.', 'Chỉ hiện khi > 0 (ô dòng Tổng cũng vậy).'], TIP['dxb']),
    ('Tổng đang xuất – Hàng KM', ['Cộng SL cần xuất trên các đề nghị xuất kho nói trên mà yêu cầu xuất hàng gốc là loại Xuất khuyến mại (HĐ hãng).'], TIP['dxk']),
    ('Nhóm theo từng kho – SL tồn / SL KM / SL gửi', ['Như Tổng tồn, SL KM, Tổng gửi nhưng chỉ tính riêng kho vật lý đó.', 'Tổng các kho = cột tổng tương ứng.'], TIP['kho']),
    ('Nhóm theo từng kho – Đang xuất Hàng bán / Hàng KM', ['Như Tổng đang xuất nhưng riêng kho đó. Chỉ hiện số dương.', 'Không có cột Tổng giữ riêng theo kho (hàng giữ tính trên mọi kho).'], '(dùng chung ⓘ của nhóm kho)'),
    ('Số khi đổi ĐVT trên dòng', ['Mọi số trên dòng = số theo đơn vị cơ bản ÷ hệ số quy đổi của đơn vị đang chọn, làm tròn 2 chữ số thập phân (gồm cả 2 cột Hàng đang về).'], TIP['dvt']),
], )
POPUP_XEM = R.numbered(R.POPUP_HEAD, [
    ('Số ở cột Hàng đang về – Tồn kho (dòng mặt hàng, số khác 0)', 'Hàng đang về (mục 2.4)',
     'Số hàng đang về này nằm trên những chứng từ nào, bao nhiêu, dự kiến về kho ngày nào, ai lập — để kinh doanh hẹn ngày giao cho khách',
     'Các chứng từ đặt hàng / nhập kho đang về của mặt hàng đó trên toàn hệ thống; “Tổng SL” = số đã bấm (theo ĐVT cơ bản)'),
    ('Số phiếu / Số hợp đồng trong popup Hàng đang về', 'Không phải popup — mở chứng từ ở tab mới',
     'Xem chi tiết chứng từ gốc', 'Yêu cầu nhập hàng, Đề nghị nhập kho, Phiếu nhập hàng mở màn HRM; các chứng từ khác mở hệ thống ERP'),
    ('Số ở dòng Tổng, cột KD đặt, các cột còn lại', 'Không bấm được', '–', '–'),
])

FR.append({
    'ten': 'Xem báo cáo hàng có thể bán theo công ty',
    'qtc': 'Màn Báo cáo, Sắp xếp dữ liệu bảng, Phân trang, Định dạng số.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem báo cáo hàng có thể bán theo công ty'],
        ['Mô tả', 'Hiển thị từng mặt hàng của một công ty tại các kho đang lọc: số lượng còn có thể bán, hàng khuyến mại còn xuất được, tồn, hàng đang về, hàng gửi, hàng giữ, hàng đang xuất, kèm số liệu riêng từng kho và dòng Tổng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống lấy danh sách công ty, kho và chọn sẵn ô Tồn theo công ty = công ty đang làm việc của người dùng.\n3. Hệ thống tải trang 1 (10 dòng), sắp theo Tên hàng hóa tăng dần, kèm dòng Tổng của toàn bộ kết quả.\n4. Bảng hiện các nhóm cột theo kho có số liệu; chân bảng “Hiển thị a–b / N”.'],
        ['Dòng sự kiện phụ', '• Bấm tiêu đề cột sắp xếp được → tăng dần, bấm lần 2 → giảm dần, lần 3 → bỏ sắp xếp (về theo Tên hàng hóa).\n• Bấm số ở cột Hàng đang về – Tồn kho → mở popup Hàng đang về (mục 2.4).\n• Rê chuột vào icon ⓘ ở tiêu đề cột → hiện giải thích cách tính.\n• Ô công ty bị xóa trống → bảng trống “Chọn công ty để xem báo cáo.”, không tải dữ liệu, ẩn nút Xuất Excel.\n• Công ty không có kho kế toán nào → “Không có dữ liệu phù hợp bộ lọc.”'],
        ['Yêu cầu đặc biệt', 'Không lọc gì với công ty lớn (khoảng 6.000 mặt hàng) màn tải trong khoảng 5–7 giây trên môi trường thử nghiệm (đo 02/11/2026).'],
    ],
    'anh': [('01_report', 'Màn Báo cáo hàng có thể bán theo công ty lúc mới mở'),
            ('04c_read_right', 'Phần bên phải bảng chi tiết báo cáo (cuộn ngang): nhóm Hàng đang về, Tổng đang xuất, nhóm cột kho PTT'),
            ('05_tooltip', 'Icon ⓘ ở tiêu đề cột giải thích cách tính')],
    'ui': ui(UI7, UI_XEM),
    'ui_widths': UI7W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Không kiểm tra quyền riêng (BR-01).\nAfter:\n– Khôi phục bộ lọc đã ghi nhớ (nếu còn trong 10 phút, trừ ô Hàng hóa).\n– Ô công ty trống thì chọn công ty đang làm việc của người dùng.\n– Tải trang 1 kèm dòng Tổng và danh sách kho.'],
        ['Bấm tiêu đề cột sắp xếp được', 'Click', 'After:\n– Đổi chiều sắp xếp tăng → giảm → bỏ, tải lại từ trang 1. Dòng Tổng không đổi.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Giữ bộ lọc và sắp xếp, tải lại; đổi số dòng thì về trang 1.'],
        ['Bấm số cột Hàng đang về – Tồn kho', 'Click', 'After:\n– Mở popup Hàng đang về của mặt hàng (mục 2.4).'],
        ['Rê chuột vào icon ⓘ', 'Hover', 'After:\n– Hiện khung giải thích (dòng đậm + các gạch đầu dòng).'],
        ['Lỗi khi tải', 'System', 'After:\n– Toast “Lỗi khi tải dữ liệu”, bảng giữ trạng thái trống.'],
    ],
    'them': [
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', 'table', DATA_XEM, R.DATA_W,
         'Bảng dưới mô tả cách hệ thống tính từng chỉ tiêu, từng cột số liệu và nội dung icon ⓘ (nguyên văn trên giao diện). '
         '“Tập dữ liệu” là các mặt hàng của công ty đang chọn tại các kho đang lọc, sau khi áp các ô lọc hàng hóa. '
         'Mọi số tính theo đơn vị tính cơ bản của mặt hàng.'),
        ('Danh sách popup mở từ số liệu', 'table', POPUP_XEM, R.POPUP_W, None),
    ],
})

# 2.2 Tìm kiếm và lọc ----------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Cài đặt bộ lọc.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc báo cáo'],
        ['Mô tả', 'Chọn công ty (bắt buộc), kho và thu hẹp mặt hàng bằng ô tìm nhanh và các ô lọc ở khu vực Tìm kiếm nâng cao.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn báo cáo.'],
        ['Dòng sự kiện chính', '1. Người dùng nhập từ khóa rồi bấm Tìm kiếm / Enter; hoặc bấm Tìm kiếm nâng cao rồi chọn giá trị ở các ô lọc.\n2. Hệ thống áp đồng thời mọi điều kiện, tải lại bảng và dòng Tổng từ trang 1.'],
        ['Dòng sự kiện phụ', '• Ô tìm nhanh và ô Model chỉ lọc khi bấm Tìm kiếm / Enter; các ô chọn lọc ngay khi chọn.\n• Đổi công ty → các kho đã chọn bị bỏ, ô Kho chỉ còn kho của công ty mới.\n• Bấm Tìm kiếm khi ô Tồn theo công ty trống → ô viền đỏ, chữ đỏ “Vui lòng chọn tồn theo công ty”, khu vực Tìm kiếm nâng cao tự mở, không tải dữ liệu.\n• Bấm Làm mới → về công ty đang làm việc, bỏ mọi điều kiện và sắp xếp, tải lại.\n• Bộ lọc được ghi nhớ 10 phút khi rời màn rồi quay lại (trừ ô Hàng hóa).'],
    ],
    'anh': [('02_filter', 'Khu vực tìm kiếm và lọc (đã mở Tìm kiếm nâng cao)'),
            ('03_required', 'Xóa trống ô Tồn theo công ty rồi bấm Tìm kiếm')],
    'ui': ui(UI8, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', 'Chữ tự do', 'Không', 'Trống', ['- Placeholder “Tìm theo tên, mã hoặc model hàng hóa”', '- Tìm gần đúng theo Tên hàng hóa, Mã hàng, Model, không phân biệt hoa thường']],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', '–', ['- Kiểm tra ô bắt buộc rồi áp mọi điều kiện, tải lại từ trang 1']],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', '–', ['- Về công ty đang làm việc, xoá các điều kiện khác, bỏ sắp xếp, xóa bộ lọc đã ghi nhớ, tải lại']],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn', ['- Mở / đóng khu vực ô lọc', '- Khi mở, nút đổi thành “Ẩn tìm kiếm nâng cao”']],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', '–', ['- Mở cửa sổ “Cài đặt bộ lọc”: tích ô lọc muốn hiện, kéo đổi thứ tự, Lưu / Khôi phục mặc định / Đóng (quy tắc chung)']],
        ['Ô Tồn theo công ty', 'Dropdown', 'Enable', 'Các công ty đang hoạt động', 'Có', 'Công ty đang làm việc', [
            '- Chọn 1 công ty, có nút × xóa trống', '- Mặc định: công ty đang làm việc của người dùng', '- Chọn được MỌI công ty (BR-01)',
            '- Trống mà bấm Tìm kiếm: “Vui lòng chọn tồn theo công ty”', '- Đổi công ty: bỏ các kho đã chọn']],
        ['Ô Kho', 'Dropdown', 'Enable', 'Kho đang hoạt động có kho kế toán của công ty', 'Không', 'Trống', [
            '- Chọn nhiều, hiển thị “Mã kho - Tên kho”', '- Bỏ trống = mọi kho của công ty (BR-03)', '- Icon ⓘ: “Bỏ trống = toàn bộ kho của công ty”']],
        ['Ô Nhóm hàng hóa', 'Dropdown', 'Enable', 'Danh mục nhóm hàng', 'Không', 'Trống', ['- Chọn nhiều']],
        ['Ô Tính chất hàng hóa', 'Dropdown', 'Enable', 'Danh mục tính chất', 'Không', 'Trống', ['- Chọn nhiều']],
        ['Ô Loại hàng hóa', 'Dropdown', 'Enable', 'Danh mục loại hàng', 'Không', 'Trống', ['- Chọn nhiều; hàng thuộc ít nhất 1 loại đã chọn là khớp']],
        ['Ô Thương hiệu', 'Dropdown', 'Enable', 'Danh mục thương hiệu', 'Không', 'Trống', ['- Chọn nhiều']],
        ['Ô Hãng sản xuất', 'Dropdown', 'Enable', 'Danh mục hãng', 'Không', 'Trống', ['- Chọn nhiều']],
        ['Ô Model', 'Textbox', 'Enable', 'Chữ tự do', 'Không', 'Trống', ['- Tìm gần đúng theo tên model', '- Chỉ lọc khi bấm Tìm kiếm / Enter']],
        ['Ô Hàng hóa', 'Dropdown', 'Enable', 'Hàng của công ty đang làm việc', 'Không', 'Trống', [
            '- Gõ từ 2 ký tự để tìm, hiển thị “Mã - Tên”, có nút ×', '- Gồm cả hàng ngừng kinh doanh còn tồn, không gồm hàng đã xóa',
            '- Không được ghi nhớ khi rời màn']],
        ['Chữ lỗi ô bắt buộc', 'Label', 'Ẩn', '–', '–', 'Ẩn', ['- “Vui lòng chọn tồn theo công ty” dưới ô, ô viền đỏ', '- Tự tắt khi chọn lại công ty']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tìm kiếm / Enter', 'Click', 'Before:\n– Ô Tồn theo công ty trống → hiện chữ đỏ, mở khu vực Tìm kiếm nâng cao, dừng.\nAfter:\n– Ghi nhớ bộ lọc, tải lại bảng + dòng Tổng từ trang 1.'],
        ['Chọn giá trị ở ô chọn', 'Change', 'After:\n– Đổi công ty mà đang chọn kho → bỏ kho đã chọn.\n– Ghi nhớ bộ lọc, tải lại từ trang 1.\n– Ô công ty bị xóa trống → bảng trống “Chọn công ty để xem báo cáo.”, không tải.'],
        ['Gõ ô tìm nhanh / ô Model', 'Change', 'After:\n– Chỉ ghi nhớ, chưa tải lại cho tới khi bấm Tìm kiếm / Enter.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Về công ty đang làm việc, xoá điều kiện khác và sắp xếp, tải lại.'],
        ['Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khu vực ô lọc.'],
    ],
})

# 2.3 Đổi ĐVT --------------------------------------------------------------------
FR.append({
    'ten': 'Đổi đơn vị tính hiển thị trên dòng',
    'qtc': 'Định dạng số.',
    'gioi_thieu': [
        ['Tên chức năng', 'Đổi đơn vị tính hiển thị trên dòng'],
        ['Mô tả', 'Xem số lượng của một mặt hàng theo đơn vị tính khác (thùng, hộp…) ngay trên bảng; chỉ đổi cách hiển thị, không ghi dữ liệu.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Mặt hàng có khai từ 2 đơn vị tính trở lên.'],
        ['Dòng sự kiện chính', '1. Người dùng chọn đơn vị khác ở ô ĐVT của dòng.\n2. Hệ thống chia mọi số trên dòng cho hệ số quy đổi, làm tròn 2 chữ số thập phân (BR-10).'],
        ['Dòng sự kiện phụ', '• Dòng Tổng không đổi (luôn theo đơn vị cơ bản).\n• Tải lại bảng (tìm kiếm, chuyển trang, sắp xếp) → mọi dòng về đơn vị cơ bản.\n• Popup Hàng đang về và file Excel không theo đơn vị đang chọn.'],
    ],
    'menu_them': ' => ô ĐVT trên dòng {icon:o_dvt}',
    'anh': [('06_unit_card', 'Mặt hàng TATE-TZ-03 đổi ĐVT sang Hộp (x100): 13,375 Cái → 133.75 Hộp')],
    'ui': ui(UI8, [
        ['Ô ĐVT', 'Dropdown', 'Enable', 'Đơn vị tính khai cho mặt hàng', 'Không', 'Đơn vị cơ bản', [
            '- Lựa chọn “Tên đơn vị (xHệ số)”, ví dụ “Cái”, “Vỉ (x25)”, “Hộp (x100)”', '- Mặc định: đơn vị cơ bản', ic('dvt')]],
        ['Các ô số trên dòng', 'Table/Grid', 'Read-only', 'Số', '–', 'Theo đơn vị cơ bản', ['- Số mới = số theo đơn vị cơ bản ÷ hệ số, làm tròn 2 chữ số thập phân', '- Áp cho mọi cột số của dòng, kể cả nhóm cột theo kho và Hàng đang về']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Chọn đơn vị ở ô ĐVT', 'Change', 'After:\n– Tính lại mọi số trên dòng theo hệ số; không gọi lại dữ liệu, không ghi dữ liệu.'],
    ],
})

# 2.4 Popup Hàng đang về ---------------------------------------------------------
DATA_POP = R.numbered(R.DATA_HEAD, [
    ('Tập dòng popup', ['Mọi dòng chứng từ thuộc 7 nguồn của cột Hàng đang về – Tồn kho cho mặt hàng đã bấm, trên toàn hệ thống (không theo công ty / kho đang lọc).', 'Đơn đặt hàng / tổng hợp đặt hàng: mỗi lần chứng từ tiếp theo đã nhận phần hàng (PI, hợp đồng mua, invoice, tờ khai, hàng về, yêu cầu nhập hàng, đề nghị nhập kho, phiếu nhập kho, phiếu nhập hàng) ra 1 dòng mang số phiếu của chứng từ cuối chuỗi; chưa có chứng từ tiếp theo thì ra 1 dòng chính đơn đặt hàng kèm “(Phiếu gốc)”.', 'Yêu cầu nhập hàng, đề nghị nhập kho, phiếu nhập kho: 1 dòng mỗi dòng hàng, số phiếu lấy chứng từ cuối của chuỗi nhập kho.'], '—'),
    ('SL', ['SL đang về của dòng chứng từ, theo số ghi trên chứng từ (không quy đổi theo ĐVT đang chọn trên bảng).'], '—'),
    ('Ngày dự kiến về kho', ['Đơn đặt hàng / tổng hợp đặt hàng: ngày dự kiến sớm nhất trên hợp đồng mua hoặc PI của đơn đó. Nguồn nhập kho: để trống.', 'Dòng xếp theo ngày tăng dần, dòng không có ngày xuống cuối.'], '—'),
    ('Người tạo', ['Người lập chứng từ, dạng “Họ tên - Mã phòng ban”.'], '—'),
    ('Tổng SL (chân popup)', ['Cộng cột SL của mọi dòng (mọi trang). Khớp số đã bấm ở cột Hàng đang về – Tồn kho (đối chiếu dev 02/11/2026: 400/400 mặt hàng khớp).'], '—'),
])
FR.append({
    'ten': 'Xem chứng từ hàng đang về', 'uc': 'uc_hdv',
    'qtc': 'Popup danh sách, Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chứng từ hàng đang về'],
        ['Mô tả', 'Popup liệt kê các chứng từ đặt hàng / nhập kho tạo nên số ở cột Hàng đang về – Tồn kho của một mặt hàng.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Dòng mặt hàng có số ở cột Hàng đang về – Tồn kho khác 0.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm số ở cột Hàng đang về – Tồn kho.\n2. Hệ thống mở popup “Hàng đang về”, dòng phụ “<Mã hàng> - <Tên hàng>”.\n3. Hệ thống tải 10 dòng đầu, chân popup ghi “Tổng SL: <tổng>”.\n4. Người dùng bấm số phiếu / số hợp đồng để mở chứng từ ở tab mới, hoặc bấm Đóng.'],
        ['Dòng sự kiện phụ', '• Chứng từ đã có màn HRM (Yêu cầu nhập hàng, Đề nghị nhập kho, Phiếu nhập hàng) → mở màn HRM ở tab mới.\n• Chứng từ khác → mở hệ thống ERP ở tab mới; không xác định được loại → chữ thường, không bấm được.\n• Không có dòng → “Không có dữ liệu phù hợp.”\n• Lỗi → toast “Lỗi khi tải dữ liệu”.'],
    ],
    'menu_them': ' => bấm số cột Hàng đang về – Tồn kho {icon:link_tonkho}',
    'ghi_chu_layout': POPUP % 'Hàng đang về',
    'anh': [('07_incoming', 'Popup Hàng đang về của ENEO-700-V5231: 6 chứng từ, Tổng SL 726 = số ở cột Tồn kho')],
    'ui': ui(UI7, [
        ['Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Hàng đang về', ['- Biểu tượng xe tải', '- Dòng phụ “<Mã hàng> - <Tên hàng>” của dòng đã bấm']],
        ['Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Liên tục qua các trang']],
        ['Cột Số phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Số chứng từ dạng liên kết. Bấm → mở chứng từ ở tab mới (HRM hoặc ERP)', '- Đơn đặt hàng chưa có chứng từ tiếp theo: kèm chữ xám “(Phiếu gốc)”']],
        ['Cột Số hợp đồng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Hợp đồng mua của dòng (nếu có), dạng liên kết mở tab mới', '- Không có: để trống']],
        ['Cột SL', 'Table/Grid', 'Read-only', 'Số', 'Theo dữ liệu', ['- Định dạng 1,234,567.89; số 0 để trống']],
        ['Cột Ngày dự kiến về kho', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', ['- Không có ngày: để trống']],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- “Họ tên - Mã phòng ban”']],
        ['Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', '10 dòng/trang', ['- “Hiển thị a–b / N”']],
        ['Dòng Tổng SL', 'Label', 'Hiển thị', 'Số', 'Theo dữ liệu', ['- “Tổng SL: <tổng>” ở chân popup, cạnh nút Đóng', '- Ẩn khi không có dòng']],
        ['Nút Đóng / (x)', 'Button', 'Enable', '–', 'Hiển thị', ['- Đóng popup, giữ nguyên bảng báo cáo']],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm số cột Hàng đang về – Tồn kho', 'Click', 'After:\n– Mở popup, tải trang 1 các chứng từ của mặt hàng.'],
        ['Chuyển trang / đổi số dòng', 'Click', 'After:\n– Tải lại trang tương ứng.'],
        ['Bấm Số phiếu / Số hợp đồng', 'Click', 'After:\n– Mở chứng từ ở tab mới, popup vẫn mở.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng popup.'],
    ],
    'them': [
        ('Mục đích thiết kế popup', 'bullets', [
            'Trả lời câu hỏi: số hàng đang về của mặt hàng này nằm ở những đơn đặt hàng / chứng từ nhập nào, mỗi chứng từ bao nhiêu, dự kiến về kho ngày nào, ai lập.',
            'Là popup để giữ nguyên bảng báo cáo, bộ lọc và trang đang xem; người dùng xem xong đóng lại làm tiếp với dòng khác.',
            'Khớp số: “Tổng SL” = số đã bấm ở cột Hàng đang về – Tồn kho (theo đơn vị cơ bản); cùng điều kiện nguồn với cột đó; không theo công ty / kho đang lọc.',
            'Từ popup người dùng mở chứng từ gốc ở tab mới; mỗi lần mở popup tải lại từ trang 1.',
        ]),
        ('Các biến thể theo con số bấm', 'table', R.numbered(R.VARIANT_HEAD, [
            ('Số ở cột Hàng đang về – Tồn kho của 1 dòng mặt hàng', 'Mọi chứng từ đang về của mặt hàng đó', 'Hàng đang về + “<Mã> - <Tên hàng>”', 'Không có ô lọc'),
        ]), R.VARIANT_W, None),
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', 'table', DATA_POP, R.DATA_W, None),
    ],
})

# 2.5 Xuất Excel -------------------------------------------------------------------
FR.append({
    'ten': 'Xuất báo cáo ra Excel', 'uc': 'uc_xuat',
    'qtc': 'Quy tắc Excel.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất báo cáo ra Excel'],
        ['Mô tả', 'Xuất mọi mặt hàng khớp bộ lọc đang áp (không chỉ trang đang xem) ra file Excel theo khuôn báo cáo, người dùng chọn trường và thứ tự cột (BR-12).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Ô Tồn theo công ty đã có giá trị.'],
        ['Dòng sự kiện chính', '1. Người dùng lọc báo cáo (nếu cần), bấm Xuất Excel.\n2. Hệ thống mở cửa sổ “Chọn trường xuất Excel”, tích sẵn cả 16 trường.\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự rồi bấm Xuất file.\n4. Hệ thống tải file bao_cao_hang_co_the_ban_theo_cong_ty.xlsx, đóng cửa sổ, báo “Xuất Excel thành công”.'],
        ['Dòng sự kiện phụ', '• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Lỗi → “Lỗi khi xuất Excel”, cửa sổ không đóng.\n• Trong lúc xuất, nút Xuất Excel không bấm được để tránh bấm kép.'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': POPUP % 'Chọn trường xuất Excel',
    'anh': [('08_export', 'Cửa sổ Chọn trường xuất Excel')],
    'ui': ui(UI8, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', '–', ['- “Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file.”']],
        ['Danh sách trường', 'Table/Grid', 'Enable', '16 trường', 'Không', 'Tích tất cả', [
            '- Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn có thể bán, SL KM có thể xuất, Tổng tồn, Hàng đang về - KD đặt, Hàng đang về - Tồn kho, SL KM, Tổng gửi, Tổng giữ, Tổng đang xuất - Hàng bán, Tổng đang xuất - Hàng KM, Theo từng kho',
            '- Mỗi trường có ô tích và biểu tượng ☰ kéo đổi vị trí', '- Mặc định tích cả 16 trường (không theo cột đang ẩn trên bảng)']],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', ['- Tích / bỏ tích mọi trường']],
        ['Dòng đếm', 'Label', 'Hiển thị', '–', '–', 'Đang chọn 16/16 trường', ['- “Đang chọn x/16 trường”']],
        ['Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Enable', ['- Tải file', '- Không bấm được khi chưa chọn trường nào']],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', ['- Đóng cửa sổ, không xuất']],
        ['File Excel', 'Label', 'Hiển thị', '–', '–', '–', [
            '- Tên file bao_cao_hang_co_the_ban_theo_cong_ty.xlsx, trang tính “Tra cứu tồn kho”',
            '- Đầu file: ảnh tiêu đề công ty của người xuất (nếu có), tiêu đề “TRA CỨU TỒN KHO THEO CÔNG TY”, dòng nghiêng “Kho: <mã kho;…>” liệt kê mọi kho trong phạm vi lọc',
            '- Tiêu đề bảng 3 tầng như màn hình, cột STT luôn có ở đầu',
            '- Dòng “Tổng cộng” in đậm ngay dưới tiêu đề, rồi các dòng mặt hàng theo đúng thứ tự sắp xếp trên màn',
            '- Số theo đơn vị cơ bản, làm tròn 2 số lẻ, số 0 để trống; cột ĐVT ghi tên đơn vị cơ bản',
            '- Trường Theo từng kho bung 5 cột cho mỗi kho đang hiện nhóm cột trên màn',
            '- Cuối file khối ký “Ngày…….Tháng…….Năm…….”, “Người lập”, “(Ký, họ tên)”']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ, tích sẵn 16 trường.'],
        ['Bấm Xuất file', 'Click', 'During:\n– Lấy toàn bộ dòng theo bộ lọc + dòng Tổng.\n– Lỗi → “Lỗi khi xuất Excel”, không thực hiện bước After.\nAfter:\n– Dựng và tải file theo trường / thứ tự đã chọn, đóng cửa sổ, báo “Xuất Excel thành công”.'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.6 Tùy chỉnh cột ---------------------------------------------------------------
FR.append({
    'ten': 'Tùy chỉnh cột hiển thị',
    'qtc': 'Tùy chỉnh cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tùy chỉnh cột hiển thị'],
        ['Mô tả', 'Ẩn / hiện các cột hoặc nhóm cột của bảng báo cáo; cấu hình lưu theo từng người dùng. Bảng có tiêu đề gộp nên thứ tự cột trên bảng cố định.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Cấu hình cột hiển thị.\n2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột”.\n3. Người dùng tích / bỏ tích rồi bấm Lưu.\n4. Hệ thống áp dụng lên bảng, lưu cấu hình, báo “Cập nhật thành công”.'],
        ['Dòng sự kiện phụ', '• Cột STT, Tên hàng hóa, ĐVT, SL tồn có thể bán là cột khóa: luôn hiện.\n• Bỏ tích “Hàng đang về (KD đặt, Tồn kho)” / “Tổng đang xuất (Hàng bán, Hàng KM)” / “Theo từng kho” → ẩn cả nhóm cột.\n• Kéo ☰ đổi thứ tự trong cửa sổ không đổi vị trí cột trên bảng.\n• Bấm Đóng → bỏ thay đổi vừa chỉnh. Lỗi lưu: “Thao tác thất bại”.'],
    ],
    'menu_them': ' => Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': POPUP % 'Tuỳ chỉnh cột',
    'anh': [('09_colcfg', 'Cửa sổ Tuỳ chỉnh cột — STT, Tên hàng hóa, ĐVT, SL tồn có thể bán bị khóa')],
    'ui': ui(UI8, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', '–', ['- “Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng.”']],
        ['Danh sách cột', 'Table/Grid', 'Enable', '15 mục', 'Không', 'Theo cấu hình đã lưu', ['- STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn có thể bán, SL KM có thể xuất, Tổng tồn, Hàng đang về (KD đặt, Tồn kho), SL KM, Tổng gửi, Tổng giữ, Tổng đang xuất (Hàng bán, Hàng KM), Theo từng kho', '- Mặc định hiện tất cả']],
        ['Cột khóa', 'Table/Grid', 'Disable', '–', '–', 'Luôn tích', ['- STT, Tên hàng hóa, ĐVT, SL tồn có thể bán: ô tích xám kèm biểu tượng khóa']],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', ['- Tích / bỏ tích mọi cột (trừ cột khóa)']],
        ['Dòng đếm', 'Label', 'Hiển thị', '–', '–', 'Đang chọn 15/15 cột', ['- “Đang chọn x/15 cột”']],
        ['Nút Lưu', 'Button', 'Enable', '–', '–', '–', ['- Áp dụng, lưu cấu hình cho người dùng; “Cập nhật thành công” (lỗi: “Thao tác thất bại”)']],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', ['- Đóng, bỏ thay đổi']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Cấu hình cột hiển thị', 'Click', 'After:\n– Mở cửa sổ theo cấu hình đang dùng.'],
        ['Tích / bỏ tích', 'Change', 'After:\n– Đổi trạng thái hiện trong cửa sổ (chưa áp dụng).'],
        ['Bấm Lưu', 'Click', 'After:\n– Ẩn / hiện cột, nhóm cột trên bảng; lưu theo người dùng; “Cập nhật thành công”.'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng, không áp dụng.'],
    ],
})

MA_TRAN_FR = ['FR-01 Xem báo cáo hàng có thể bán theo công ty', 'FR-02 Tìm kiếm và lọc', 'FR-03 Đổi đơn vị tính hiển thị trên dòng',
              'FR-04 Xem chứng từ hàng đang về', 'FR-05 Xuất báo cáo ra Excel', 'FR-06 Tùy chỉnh cột hiển thị']

S = {
    'ten': TEN,
    'menu': [('Thông báo', 'menu_phanhe'), ('Tra cứu tồn kho', 'menu_nhom'), ('Hàng có thể bán theo công ty', 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu báo cáo.',
        'Làm rõ cách tính từng cột số liệu (SL tồn có thể bán, KM, gửi, giữ, đang xuất, hàng đang về), phạm vi công ty / kho của từng cột, dòng Tổng và popup Hàng đang về.',
    ],
    'thuat_ngu': [
        ['Tồn kho kế toán', 'Số lượng hàng đang có theo sổ kho kế toán của công ty.'],
        ['Kho kế toán', 'Kho sổ sách của một công ty, gắn với một kho vật lý; một kho vật lý có thể có kho kế toán của nhiều công ty.'],
        ['Kho khuyến mại', 'Kho kế toán được công ty khai là kho hàng khuyến mại (Khai Quy chế – Cấu hình).'],
        ['Hàng gửi', 'Hàng của khách gửi lại kho, ghi nhận từ phiếu nhập hàng loại Nhập hàng gửi.'],
        ['Hàng giữ', 'Hàng đã giữ cho nhân viên / hợp đồng qua phiếu xuất giữ, chưa xuất bán.'],
        ['Đang xuất', 'Hàng trên đề nghị xuất kho chưa hoàn tất.'],
        ['Hàng đang về', 'Hàng đã đặt mua / đang chờ nhập kho, chưa vào tồn.'],
        ['ĐVT cơ bản', 'Đơn vị tính gốc của mặt hàng (hệ số 1); các đơn vị khác quy đổi theo hệ số.'],
        ['KD', 'Kinh doanh.'],
        ['KM', 'Khuyến mại.'],
    ],
    'quyen_truoc': ['Màn hình CHỈ ĐỌC và không gắn quyền riêng: mọi người dùng đã đăng nhập, vào được phân hệ Thông báo đều mở được màn và dùng mọi chức năng (kể cả Xuất Excel). Menu chỉ bị ẩn khi phân hệ / mục menu bị tắt ở màn Cài đặt phân hệ.'],
    'quyen_rows': [['Không có quyền riêng (người dùng đã đăng nhập)', 'Xem báo cáo, tìm kiếm / lọc, đổi ĐVT, xem chứng từ hàng đang về, xuất Excel, tùy chỉnh cột.']],
    'ma_tran': [['Chức năng', 'Người dùng đã đăng nhập']] + [[f, 'Có'] for f in MA_TRAN_FR],
    'ma_tran_widths': [3.2, 1.6],
    'quyen_sau': [
        'Người dùng chọn được MỌI công ty đang hoạt động ở ô Tồn theo công ty, không giới hạn theo công ty / phòng ban của mình (BR-01). Mặc định là công ty đang làm việc.',
        'Cột Hàng đang về và popup Hàng đang về tính trên toàn hệ thống, không theo công ty (BR-08). Cột Tổng giữ tính trên mọi kho của công ty (BR-07).',
        'Mở chứng từ từ popup: màn HRM / ERP đích tự áp quyền xem của chính nó.',
    ],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Quyền và công ty', ['– Không gắn quyền riêng; ai đã đăng nhập cũng xem được.', '– Ô Tồn theo công ty bắt buộc, mặc định công ty đang làm việc của người dùng, chọn được mọi công ty đang hoạt động.', '– Ô công ty trống: không tải dữ liệu, bảng “Chọn công ty để xem báo cáo.”, ẩn Xuất Excel.'], ['Xem báo cáo', 'Tìm kiếm và lọc', 'Xuất Excel']),
        ('BR-02', 'Mặt hàng hiển thị', ['– Mặt hàng có dòng tồn kho kế toán tại kho kế toán của công ty thuộc các kho đang lọc.', '– Và Tổng tồn + SL KM + Tổng gửi + SL trên đề nghị xuất kho chưa hoàn tất + Tổng giữ > 0.', '– Khớp các ô lọc hàng hóa (nhóm, tính chất, loại, thương hiệu, hãng, model, hàng hóa, từ khóa).'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-03', 'Phạm vi kho', ['– Kho = kho vật lý có kho kế toán của công ty đang chọn.', '– Bỏ trống ô Kho = mọi kho có kho kế toán của công ty (theo dữ liệu kho kế toán, không xét trạng thái kho vật lý); ô chọn chỉ liệt kê kho vật lý đang hoạt động.', '– Đổi công ty thì bỏ các kho đã chọn.'], ['Tìm kiếm và lọc', 'Xem báo cáo']),
        ('BR-04', 'SL tồn có thể bán', ['– = Tổng tồn − SL KM − Tổng gửi − Tổng giữ − Tổng đang xuất (Hàng bán); âm thì 0.'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-05', 'SL KM có thể xuất', ['– = SL KM − Tổng đang xuất (Hàng KM); âm thì 0.', '– Kho khuyến mại theo khai báo của công ty, chỉ tính kho thuộc phạm vi lọc.'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-06', 'Hàng đang xuất', ['– Đề nghị xuất kho của công ty tại kho đang lọc, chưa hoàn tất, không ở Đang tạo / Đã hủy, dòng còn cần xuất.', '– Hàng KM = phần thuộc yêu cầu xuất loại Xuất khuyến mại (HĐ hãng).', '– Hàng bán = SL cần xuất − Hàng KM − phần xuất từ hàng giữ − phần xuất từ hàng gửi.'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-07', 'Hàng giữ', ['– Tổng giữ tính trên MỌI kho của công ty, không theo ô lọc Kho; không có cột giữ riêng theo kho.'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-08', 'Hàng đang về', ['– Tính trên toàn hệ thống, không lọc công ty / kho.', '– Đơn đặt hàng và các nguồn cột Tồn kho chỉ tính chứng từ phát sinh sau 01/07/2024; yêu cầu nhập hàng của cột KD đặt không giới hạn ngày.', '– Cộng theo SL ghi trên chứng từ.', '– Cột Tồn kho âm thì 0.'], ['Xem báo cáo', 'Xem chứng từ hàng đang về', 'Xuất Excel']),
        ('BR-09', 'Dòng Tổng và định dạng số', ['– Dòng Tổng cộng mọi dòng khớp bộ lọc (mọi trang), theo ĐVT cơ bản.', '– Số theo chuẩn 1,234,567.89, tối đa 2 số lẻ; số 0 để trống.', '– Cột Tổng đang xuất – Hàng bán và nhóm cột theo kho chỉ hiện số dương.'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-10', 'Đổi ĐVT trên dòng', ['– Mặc định đơn vị cơ bản; đổi đơn vị thì mọi số trên dòng = số cơ bản ÷ hệ số, làm tròn 2 số lẻ.', '– Chỉ là hiển thị: dòng Tổng, popup Hàng đang về, file Excel vẫn theo đơn vị cơ bản; tải lại bảng thì về đơn vị cơ bản.'], ['Đổi đơn vị tính']),
        ('BR-11', 'Nhóm cột theo kho', ['– Chỉ hiện kho có ít nhất 1 trong 5 số (SL tồn, SL KM, SL gửi, Đang xuất Hàng bán, Hàng KM) khác 0 ở dòng Tổng; xếp theo mã kho.'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-12', 'Xuất Excel', ['– Xuất mọi dòng khớp bộ lọc, đúng thứ tự sắp xếp trên màn, cột theo trường / thứ tự người dùng chọn.', '– Số theo ĐVT cơ bản; Theo từng kho chỉ gồm các kho đang hiện nhóm cột trên màn; dòng “Kho:” liệt kê mọi kho trong phạm vi lọc.'], ['Xuất Excel']),
        ('BR-13', 'Ghi nhớ bộ lọc', ['– Bộ lọc được ghi nhớ 10 phút khi rời màn; ô Hàng hóa không được ghi nhớ.', '– Làm mới xóa bộ lọc đã ghi nhớ.'], ['Tìm kiếm và lọc']),
    ],
    'phan5': {
        'title': 'Phần 5. Bảng danh sách các màn hình liên quan dữ liệu báo cáo',
        'cau_dan': 'Báo cáo chỉ đọc. Các màn hình dưới đây ghi ra số liệu mà báo cáo cộng lại (nguồn số liệu), cung cấp danh mục tham chiếu, hoặc dùng chung nguồn số liệu. Chứng từ đặt hàng nhập khẩu / trong nước, tổng hợp đặt hàng, PI, hợp đồng mua, invoice, tờ khai hiện vẫn lập ở hệ thống ERP nên không liệt kê.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng đã đăng nhập',
    'mains': [('FR-01', 'Xem báo cáo hàng có thể bán theo công ty', 'view'), ('FR-05', 'Xuất báo cáo ra Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc', 'view'), ('FR-03', 'Đổi đơn vị tính hiển thị', 'view'),
             ('FR-04', 'Xem chứng từ hàng đang về', 'view'), ('FR-06', 'Tùy chỉnh cột hiển thị', 'view')],
    'rieng': [('FR-04', 'Xem chứng từ hàng đang về', 'view', 'uc_hdv'), ('FR-05', 'Xuất báo cáo ra Excel', 'io', 'uc_xuat')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', R.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)

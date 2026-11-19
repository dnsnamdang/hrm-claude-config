# -*- coding: utf-8 -*-
"""SRS - BC tổng hợp công nợ KH theo nhân viên (form Danh mục quốc gia + quy tắc màn báo cáo của skill srs-documenter).

Nguồn (code HRM hiện tại, 02/11/2026):
  FE hrm-client/pages/sale/customer-debt-by-employee/{index.vue, components/export-excel.js},
     pages/sale/customer-debt-details/components/export-excel.js (cột phát sinh, tiêu đề 2 tầng),
     components/{V2BaseSmartFilterPanel, V2BaseCompanyDepartmentFilter, modal/export-fields-modal, report/ReportInfoTip}.vue,
     utils/{filterRequiredErrors.js, finance/customerDebtContractLink.js}, components/subsystem-menu/sale-hub.js
  BE hrm-api/Modules/Finance/Http/Controllers/V1/CustomerDebtByEmployeeController.php,
     Services/CustomerDebt/{CustomerDebtByEmployeeReportService, AbstractCustomerDebtReportService, CustomerDebtAggregator,
     CustomerDebtScope}.php
  Ảnh: hdsd_shots/ (capture.js, dev-hrm). Phần 5: dò code FE/BE + menu.
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _lib_bc as B  # noqa: E402

L = B.L
TEN_FILE = 'BC tổng hợp công nợ KH theo nhân viên'
TEN = 'Báo cáo tổng hợp công nợ khách hàng theo nhân viên'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN_FILE)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN_FILE)
Q4 = 'Xem báo cáo tổng hợp công nợ khách hàng theo nhân viên - '
QA = 'Người dùng có quyền thực hiện chức năng: mọi người dùng đã được cấp tài khoản; 4 quyền "%s<cấp>" chỉ mở rộng phạm vi dữ liệu (BR-01)' % Q4
DK = '1. Người dùng đăng nhập thành công.\n2. Không cần quyền riêng để mở màn; số liệu hiển thị theo phạm vi quyền (BR-01).'
LOI = '– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung SRS_Các quy tắc chung_VN_1.0, không thực hiện bước After.'
POPUP = 'Cửa sổ %s được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'

UI7 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả']
UI7W = [0.6, 1.3, 0.85, 0.95, 0.85, 0.85, 2.4]
UI8 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả']
UI8W = [0.6, 1.15, 0.85, 0.95, 0.85, 0.8, 0.85, 2.0]
DATA_HEAD = ['STT', 'Chỉ tiêu / Cột', 'Cách lấy dữ liệu', 'Nội dung icon ⓘ']
DATA_W = [0.6, 1.3, 2.8, 1.8]
LINK_HEAD = ['STT', 'Bấm vào', 'Popup mở ra', 'Mục đích thiết kế', 'Dữ liệu hiển thị']
LINK_W = [0.6, 1.3, 1.3, 1.6, 1.6]


def ui(header, rows):
    return [header] + [[str(i + 1)] + [('\n'.join(c) if isinstance(c, (list, tuple)) else c) for c in r] for i, r in enumerate(rows)]


# ------------------------------------------------------------------ nội dung icon ⓘ NGUYÊN VĂN (index.vue COLUMN_TIPS)
KY = 'Tính trên sổ tài khoản phải thu khách hàng (TK 131 và các tài khoản con), số tiền quy đổi VND, theo ngày hạch toán.'
TIP = {
    'stt': 'Số thứ tự. • Dòng nhân viên (in đậm) đánh số 1, 2, 3…; các hợp đồng của nhân viên đó đánh số 1.1, 1.2… • Số thứ tự nối tiếp khi sang trang sau.',
    'hd': 'Đơn hàng/hợp đồng phát sinh công nợ. • Dòng in đậm là nhân viên tạo hợp đồng (mã - tên), số liệu = cộng TẤT CẢ hợp đồng của nhân viên đó theo bộ lọc (kể cả hợp đồng nằm ở trang khác). • Bấm số hợp đồng để mở hợp đồng ở tab mới. • Ô trống: chứng từ không gắn hợp đồng (phiếu báo có hoặc kế toán chưa được ghi nhận).',
    'kh': 'Khách hàng của hợp đồng (mã - tên). • Hợp đồng có chứng từ của nhiều khách hàng thì chỉ hiện 1 khách hàng (giống ERP).',
    'dk': 'Công nợ phải thu còn lại trước "Từ ngày". • Số dư đầu kỳ = Tổng phát sinh Nợ − Tổng phát sinh Có của các chứng từ có ngày hạch toán trước "Từ ngày". • Số dương: khách còn nợ; số âm: khách trả thừa / trả trước. • ' + KY,
    'tang': 'Các khoản làm TĂNG công nợ phải thu, ngày hạch toán từ "Từ ngày" đến "Đến ngày". • Gồm: Hàng hóa/Dịch vụ, Điều chỉnh công nợ (ghi tăng). • ' + KY,
    'hh': 'Giá trị hàng hóa, dịch vụ bán cho khách ghi nhận công nợ trong kỳ. • Chứng từ: phiếu xuất kho, phiếu xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ bảo hành - sửa chữa, khai báo công nợ đầu kỳ. • Hàng hóa/Dịch vụ = Phát sinh Nợ của các chứng từ trên − Phát sinh Có của chính các chứng từ đó (trừ khai báo công nợ đầu kỳ).',
    'dct': 'Điều chỉnh làm TĂNG công nợ trong kỳ. • Điều chỉnh công nợ (tăng) = Phát sinh Nợ của phiếu kế toán (phiếu điều chỉnh công nợ).',
    'congt': 'Tổng phát sinh tăng trong kỳ. • Cộng phát sinh tăng = Hàng hóa/Dịch vụ + Điều chỉnh công nợ (tăng).',
    'giam': 'Các khoản làm GIẢM công nợ phải thu, ngày hạch toán từ "Từ ngày" đến "Đến ngày". • Gồm: Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ (ghi giảm). • "Trả lại tiền thừa" là cột riêng, không nằm trong nhóm này. • ' + KY,
    'ntl': 'Giá trị hàng khách trả lại trong kỳ. • Nhập trả lại = Phát sinh Có − Phát sinh Nợ của phiếu nhập hàng (hàng bán bị trả lại).',
    'dtt': 'Số tiền khách đã thanh toán trong kỳ. • Đã thanh toán = Phát sinh Có của phiếu thu, phiếu báo có và khai báo công nợ đầu kỳ.',
    'dcg': 'Điều chỉnh làm GIẢM công nợ trong kỳ. • Điều chỉnh công nợ (giảm) = Phát sinh Có của phiếu kế toán (phiếu điều chỉnh công nợ).',
    'congg': 'Tổng phát sinh giảm trong kỳ. • Cộng phát sinh giảm = Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ (giảm).',
    'tltt': 'Tiền chi trả lại cho khách (khách nộp thừa) trong kỳ. • Trả lại tiền thừa = Phát sinh Nợ của phiếu chi và phiếu ủy nhiệm chi. • Khoản này được CỘNG vào Số dư cuối kỳ (bù lại phần khách đã trả thừa).',
    'ck': 'Công nợ phải thu còn lại tại "Đến ngày". • Số dư cuối kỳ = Số dư đầu kỳ + Cộng phát sinh tăng − Cộng phát sinh giảm + Trả lại tiền thừa. • Số dương (dư nợ): khách còn nợ; số âm (dư có): khách trả thừa / trả trước. • Bộ lọc "Số dư cuối kỳ" (Dư nợ / Dư có) lọc theo số này.',
    'nt': 'Ngày nghiệm thu / bàn giao của hợp đồng — mốc tính Số ngày nợ. • Hợp đồng hãng cần lắp đặt: ngày của biên bản nghiệm thu mới nhất. • Hợp đồng hãng không cần lắp đặt: ngày muộn nhất trong các phiếu xuất kho bán hàng, phiếu xuất bán hàng mượn, hạch toán dịch vụ. • Hợp đồng dịch vụ bảo hành - sửa chữa: ngày muộn nhất trong các hạch toán dịch vụ, phiếu xuất bán hàng mượn, phiếu xuất kho. • Không có các chứng từ trên: lấy ngày bàn giao nghiệm thu khai ở công nợ đầu kỳ quá hạn.',
    'snn': 'Số ngày khách nợ, tính đến HÔM NAY (không theo "Đến ngày" của bộ lọc). • Số ngày nợ = Hôm nay − (Ngày nghiệm thu + 6 ngày); kết quả âm thì ghi 0. • Chỉ hiện khi hợp đồng còn dư nợ (Số dư cuối kỳ > 0) và có Ngày nghiệm thu.',
    'tong': 'Phát sinh cộng trên toàn bộ dòng theo bộ lọc. Số dư đầu kỳ tính mọi chứng từ trước "Từ ngày" (kể cả chưa gắn nhân viên / khách hàng), giống ERP.',
    'trang': 'Tổng hợp công nợ phải thu khách hàng theo nhân viên tạo hợp đồng, chi tiết đến từng hợp đồng, kèm ngày nghiệm thu và số ngày nợ để theo dõi thu hồi công nợ. Dữ liệu hiển thị theo quyền xem (tổng công ty / công ty / phòng ban / bộ phận — cấp phòng ban / bộ phận gồm cả đơn vị mình quản lý và đơn vị mình đang thuộc); không có quyền nào thì chỉ thấy hợp đồng do mình tạo.',
}


def ic(k):
    return 'Icon ⓘ: “%s”' % TIP[k]


TAP = ('“Tập dữ liệu” là các bút toán ghi vào tài khoản phải thu khách hàng (TK 131 và các tài khoản con trực tiếp) khi chứng '
       'từ được hạch toán, có gắn khách hàng, có nhân viên tạo hợp đồng, số tiền lớn hơn 0, ngày hạch toán đến hết “Đến ngày”, '
       'sau khi áp phạm vi quyền (BR-01) và bộ lọc. Bút toán gom thành 1 dòng cho mỗi cặp (nhân viên tạo hợp đồng, hợp đồng).')

# ------------------------------------------------------------------ Phần 5 (dò code 02/11/2026)
P5 = [
    ('Bán hàng', 'Báo cáo chi tiết công nợ khách hàng (cùng công thức công nợ)', 'Bán hàng => Báo cáo => Báo cáo công nợ => Chi tiết công nợ KH'),
    ('Bán hàng', 'Bảng đối chiếu công nợ 1 khách hàng (cùng công thức công nợ)', 'Bán hàng => Báo cáo => Báo cáo công nợ => Đối chiếu công nợ 1 KH'),
    ('Tài chính', 'Báo cáo hạn mức công nợ khách hàng (cột Số dư nợ, cùng công thức)', 'Tài chính => Kế toán công nợ => Khách hàng'),
    ('Tài chính', 'Báo cáo hạn mức công nợ nhân viên (gom theo nhân viên tạo hợp đồng, cùng công thức)', 'Tài chính => Kế toán công nợ => Nhân viên'),
    ('Tài chính', 'Phiếu xuất hàng (ghi tăng Hàng hóa/Dịch vụ)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ('Tài chính', 'Phiếu xuất bán hàng mượn (ghi tăng Hàng hóa/Dịch vụ, mốc Ngày nghiệm thu)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng'),
    ('Tài chính', 'Phiếu hạch toán dịch vụ - HDDV (ghi tăng Hàng hóa/Dịch vụ, mốc Ngày nghiệm thu)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Bán Dịch vụ'),
    ('Tài chính', 'Phiếu nhập hàng (hàng bán bị trả lại → Nhập trả lại)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
    ('Tài chính', 'Phiếu thu (Đã thanh toán)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu báo có (Đã thanh toán)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu chi (Trả lại tiền thừa)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu ủy nhiệm chi (Trả lại tiền thừa)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu yêu cầu điều chỉnh công nợ (nguồn lập Phiếu kế toán)', 'Tài chính => Khởi tạo => Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi'),
    ('Tài chính', 'Phiếu kế toán (Điều chỉnh công nợ tăng / giảm)', 'Tài chính => Sổ tổng hợp => Sổ tổng hợp'),
    ('Tài chính', 'Khai báo đầu kỳ công nợ (Hàng hóa/Dịch vụ, Đã thanh toán, ngày nghiệm thu dự phòng)', 'Tài chính => Khai báo đầu kỳ'),
    ('Bán hàng', 'Hợp đồng bán hàng (mở từ cột Đơn hàng/hợp đồng)', 'Bán hàng => Bán hàng => Hợp đồng bán hàng'),
]

FR = []

# 2.1 Xem báo cáo ---------------------------------------------------------------
FR.append({
    'ten': 'Xem báo cáo tổng hợp công nợ khách hàng theo nhân viên',
    'qtc': 'Màn Báo cáo, Phân trang, Định dạng số, Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem báo cáo tổng hợp công nợ khách hàng theo nhân viên'],
        ['Mô tả', 'Hiển thị công nợ phải thu gom theo nhân viên tạo hợp đồng, chi tiết từng hợp đồng: số dư đầu kỳ, phát sinh tăng, phát sinh giảm, trả lại tiền thừa, số dư cuối kỳ, ngày nghiệm thu và số ngày nợ — để giao nhân viên theo dõi, thu hồi công nợ. Màn chỉ đọc.'],
        ['Tác nhân', QA],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống hiện bộ lọc, ô Thời gian để trống, bảng ghi "Chọn thời gian để xem báo cáo."\n3. Người dùng chọn Thời gian (Từ ngày → Đến ngày).\n4. Hệ thống tự tải trang 1 (10 dòng hợp đồng): dòng Tổng cộng, dòng nhân viên (in đậm) và các dòng hợp đồng bên dưới; chân bảng "Hiển thị a–b / N dòng hợp đồng".'],
        ['Dòng sự kiện phụ', '• Đang tải: bảng hiện "Đang tải dữ liệu...".\n• Không có dòng khớp: "Không có dữ liệu phù hợp bộ lọc."\n• Đổi bộ lọc liên tiếp: chỉ nhận kết quả của lần lọc mới nhất.\n• Lỗi hệ thống: thông báo "Lỗi khi tải dữ liệu" (hoặc câu lỗi hệ thống trả về).\n• Bấm số hợp đồng: mở trang hợp đồng ở tab mới (mục 2.1.6).'],
    ],
    'anh': [('00b_empty', 'Màn Báo cáo tổng hợp công nợ khách hàng theo nhân viên lúc mới truy cập (chưa chọn Thời gian)'),
            ('01_report', 'Báo cáo sau khi chọn Thời gian 01/10/2026 – 31/10/2026')],
    'ui': ui(UI7, [
        ['Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Hiển thị', ['- "Báo cáo tổng hợp công nợ khách hàng theo nhân viên" trên thanh đầu trang và đầu khối bảng.', '- ' + ic('trang')]],
        ['Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', ['- Mở cửa sổ "Chọn trường xuất Excel" (mục 2.4).', '- Rê chuột: "Xuất Excel theo bộ lọc đang áp, chọn cột cần xuất".', '- Khoá trong lúc đang xuất file.']],
        ['Nút Xuất Excel mẫu in', 'Button', 'Enable', '–', 'Hiển thị', ['- Tải ngay file theo mẫu in (mục 2.5).', '- Rê chuột: "Xuất Excel theo mẫu in (có cột giải trình, kế hoạch thu hồi, xác nhận công nợ)".']],
        ['Bảng chi tiết báo cáo', 'Table/Grid', 'Read-only', '16 cột', 'Trống', ['- Tiêu đề 2 tầng, dính trên cùng khi cuộn dọc; có thanh cuộn ngang ở cả trên và dưới bảng.', '- Thứ tự dòng: dòng Tổng cộng → dòng nhân viên (in đậm, nền xám nhạt) → các dòng hợp đồng của nhân viên đó.', '- Không có sắp xếp theo cột. Không có cấu hình cột.']],
        ['Dòng Tổng cộng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Chữ "Tổng cộng" gộp 3 cột đầu, nền xám, in đậm.', '- ' + ic('tong'), '- Số 0 in "0" (khác các dòng khác để trống).', '- Không đổi khi chuyển trang. Cách tính: mục 2.1.5.']],
        ['Dòng nhân viên', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- "Mã NV - Họ tên" của nhân viên tạo hợp đồng, gộp cột Đơn hàng/hợp đồng và Khách hàng.', '- Số liệu = tổng ĐỦ mọi hợp đồng của nhân viên theo bộ lọc, kể cả hợp đồng ở trang khác (BR-05).', '- 2 cột Ngày nghiệm thu, Số ngày nợ để trống.']],
        ['Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Dòng nhân viên: 1, 2, 3…; dòng hợp đồng: 1.1, 1.2…; nối tiếp khi sang trang.', '- ' + ic('stt')]],
        ['Cột Đơn hàng/hợp đồng', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Số hợp đồng dạng liên kết: bấm số → mở trang hợp đồng ở tab mới (mục 2.1.6).', '- Loại hợp đồng không có trang xem: hiện chữ thường, không bấm được.', '- Chứng từ không gắn hợp đồng: để trống.', '- ' + ic('hd')]],
        ['Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- "Mã KH - Tên KH", xuống dòng khi dài.', '- ' + ic('kh')]],
        ['Cột Số dư đầu kỳ', 'Table/Grid', 'Read-only', 'Số, có thể âm', 'Hiển thị', ['- Định dạng 1,234,567, không lẻ; 0 để trống.', '- ' + ic('dk')]],
        ['Nhóm cột Phát sinh tăng trong kỳ', 'Table/Grid', 'Read-only', '3 cột con', 'Hiển thị', ['- Gồm Hàng hóa/Dịch vụ, Điều chỉnh công nợ, Cộng.', '- ' + ic('tang')]],
        ['Cột Hàng hóa/Dịch vụ', 'Table/Grid', 'Read-only', 'Số', 'Hiển thị', ['- 0 để trống.', '- ' + ic('hh')]],
        ['Cột Điều chỉnh công nợ (tăng)', 'Table/Grid', 'Read-only', 'Số', 'Hiển thị', ['- 0 để trống.', '- ' + ic('dct')]],
        ['Cột Cộng (tăng)', 'Table/Grid', 'Read-only', 'Số', 'Hiển thị', ['- = Hàng hóa/Dịch vụ + Điều chỉnh công nợ (tăng).', '- ' + ic('congt')]],
        ['Nhóm cột Phát sinh giảm trong kỳ', 'Table/Grid', 'Read-only', '4 cột con', 'Hiển thị', ['- Gồm Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ, Cộng.', '- ' + ic('giam')]],
        ['Cột Nhập trả lại', 'Table/Grid', 'Read-only', 'Số', 'Hiển thị', ['- 0 để trống.', '- ' + ic('ntl')]],
        ['Cột Đã thanh toán', 'Table/Grid', 'Read-only', 'Số', 'Hiển thị', ['- 0 để trống.', '- ' + ic('dtt')]],
        ['Cột Điều chỉnh công nợ (giảm)', 'Table/Grid', 'Read-only', 'Số', 'Hiển thị', ['- 0 để trống.', '- ' + ic('dcg')]],
        ['Cột Cộng (giảm)', 'Table/Grid', 'Read-only', 'Số', 'Hiển thị', ['- = Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ (giảm).', '- ' + ic('congg')]],
        ['Cột Trả lại tiền thừa', 'Table/Grid', 'Read-only', 'Số', 'Hiển thị', ['- 0 để trống.', '- ' + ic('tltt')]],
        ['Cột Số dư cuối kỳ', 'Table/Grid', 'Read-only', 'Số, có thể âm', 'Hiển thị', ['- Số âm có dấu "-" (khách trả thừa).', '- ' + ic('ck')]],
        ['Cột Ngày nghiệm thu', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Hiển thị', ['- Chỉ ở dòng hợp đồng; không xác định được thì để trống.', '- ' + ic('nt')]],
        ['Cột Số ngày nợ (Ngày)', 'Table/Grid', 'Read-only', 'Số nguyên ≥ 0', 'Hiển thị', ['- Chỉ ở dòng hợp đồng còn dư nợ và có Ngày nghiệm thu; còn lại để trống.', '- ' + ic('snn')]],
        ['Chân bảng', 'Label', 'Hiển thị', '–', 'Ẩn khi không có dòng', '"Hiển thị a–b / N dòng hợp đồng" — N là số dòng hợp đồng (không đếm dòng nhân viên).'],
        ['Ô Số dòng/trang', 'Dropdown', 'Enable', '10 / 20 / 50 / 100', '10', '- Mặc định: 10 dòng hợp đồng mỗi trang.\n- Đổi số dòng → quay về trang 1.'],
        ['Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Nút trang đầu / trước / số trang / sau / trang cuối; giữ nguyên bộ lọc.'],
        ['Thông báo trạng thái bảng', 'Label', 'Hiển thị', '–', '"Chọn thời gian để xem báo cáo."', ['- Chưa chọn đủ Thời gian: "Chọn thời gian để xem báo cáo."', '- Đang tải: "Đang tải dữ liệu..."', '- Không có dòng: "Không có dữ liệu phù hợp bộ lọc."']],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Tải phạm vi quyền của người dùng (BR-01) để quyết định hiện ô Công ty / Phòng ban / Bộ phận / Nhân viên.\n– Mở lại màn trong 10 phút (không tải lại trang): khôi phục bộ lọc lần trước; tải lại trang (F5) thì về bộ lọc trống.\nAfter:\n– Chưa có Thời gian: không tải số liệu, bảng ghi "Chọn thời gian để xem báo cáo."'],
        ['Chọn đủ Thời gian', 'Change', 'During:\n– Từ ngày > Đến ngày → xem mục 2.2, không tải số liệu.\n' + LOI + '\nAfter:\n– Tải trang 1 kèm dòng Tổng cộng theo bộ lọc hiện tại.'],
        ['Chuyển trang / đổi Số dòng/trang', 'Click', 'After:\n– Tải lại dòng của trang mới, GIỮ NGUYÊN dòng Tổng cộng (không tính lại); đổi số dòng thì về trang 1.'],
        ['Rê chuột vào icon ⓘ', 'Hover', 'After:\n– Hiện khung chú thích nguyên văn như cột "Nội dung icon ⓘ" mục 2.1.5.'],
        ['Bấm số hợp đồng', 'Click', 'After:\n– Mở trang xem hợp đồng ở tab mới, màn báo cáo giữ nguyên.'],
    ],
    'them': [
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', DATA_HEAD, [
            ('Thời điểm số liệu / kỳ báo cáo', 'Theo NGÀY HẠCH TOÁN của chứng từ. Chứng từ ngày < Từ ngày đi vào Số dư đầu kỳ; ngày từ Từ ngày đến hết Đến ngày đi vào các cột phát sinh; sau Đến ngày không tính. Chỉ chứng từ đã hạch toán (đã ghi sổ phải thu) mới có số; phiếu mới lập / chờ duyệt chưa làm đổi báo cáo. Số tiền là số đã quy đổi VND. ' + TAP, '—'),
            ('Dòng hợp đồng', '1 dòng cho mỗi cặp (nhân viên tạo hợp đồng, hợp đồng) có ít nhất 1 bút toán trong tập dữ liệu — kể cả hợp đồng mà mọi cột đều bằng 0 (công nợ đã tất toán trước kỳ). Bút toán không gắn hợp đồng của cùng nhân viên gom chung 1 dòng có ô hợp đồng trống.', '—'),
            ('Dòng nhân viên', 'Cộng từng cột của MỌI dòng hợp đồng thuộc nhân viên đó trong tập dữ liệu (kể cả dòng ở trang khác). Nhân viên xếp theo thứ tự tạo nhân viên trên hệ thống (không theo tên); hợp đồng trong 1 nhân viên xếp theo loại rồi thứ tự tạo hợp đồng.', '(dùng chung ⓘ của cột Đơn hàng/hợp đồng)'),
            ('Dòng Tổng cộng – các cột phát sinh và Trả lại tiền thừa', 'Cộng cột tương ứng của mọi dòng hợp đồng trong tập dữ liệu (mọi trang).', TIP['tong']),
            ('Dòng Tổng cộng – Số dư đầu kỳ', 'Phát sinh Nợ − Phát sinh Có của MỌI bút toán tài khoản phải thu có ngày hạch toán trước Từ ngày, trong phạm vi quyền, theo ô Công ty / Phòng ban / Bộ phận / Nhân viên / Khách hàng; ô Số hợp đồng so gần đúng (chứa chuỗi). KHÔNG cần gắn khách hàng / nhân viên, KHÔNG theo ô Số dư cuối kỳ, Ngày nghiệm thu, ô tìm nhanh ⇒ có thể khác tổng cột Số dư đầu kỳ của các dòng nhân viên.', TIP['tong']),
            ('Dòng Tổng cộng – Số dư cuối kỳ', '= Số dư đầu kỳ (dòng Tổng cộng) + Cộng phát sinh tăng − Cộng phát sinh giảm + Trả lại tiền thừa của dòng Tổng cộng.', TIP['tong']),
            ('Cột Số dư đầu kỳ (dòng hợp đồng)', 'Phát sinh Nợ − Phát sinh Có của các bút toán của hợp đồng có ngày hạch toán trước Từ ngày.', TIP['dk']),
            ('Cột Hàng hóa/Dịch vụ', 'Phát sinh Nợ trong kỳ của: phiếu xuất kho, phiếu xuất bán hàng mượn, khai báo công nợ đầu kỳ, hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ bảo hành - sửa chữa; TRỪ phát sinh Có trong kỳ của chính các loại đó (không trừ khai báo công nợ đầu kỳ).', TIP['hh']),
            ('Cột Điều chỉnh công nợ (tăng)', 'Phát sinh Nợ trong kỳ của phiếu kế toán điều chỉnh công nợ.', TIP['dct']),
            ('Cột Cộng (tăng)', 'Hàng hóa/Dịch vụ + Điều chỉnh công nợ (tăng) của chính dòng đó.', TIP['congt']),
            ('Cột Nhập trả lại', 'Phát sinh Có − Phát sinh Nợ trong kỳ của phiếu nhập hàng (hàng bán bị trả lại).', TIP['ntl']),
            ('Cột Đã thanh toán', 'Phát sinh Có trong kỳ của phiếu thu, phiếu báo có, khai báo công nợ đầu kỳ.', TIP['dtt']),
            ('Cột Điều chỉnh công nợ (giảm)', 'Phát sinh Có trong kỳ của phiếu kế toán điều chỉnh công nợ.', TIP['dcg']),
            ('Cột Cộng (giảm)', 'Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ (giảm) của chính dòng đó.', TIP['congg']),
            ('Cột Trả lại tiền thừa', 'Phát sinh Nợ trong kỳ của phiếu chi và phiếu ủy nhiệm chi.', TIP['tltt']),
            ('Cột Số dư cuối kỳ (dòng hợp đồng / nhân viên)', 'Số dư đầu kỳ + Cộng (tăng) − Cộng (giảm) + Trả lại tiền thừa.', TIP['ck']),
            ('Cột Ngày nghiệm thu', 'Hợp đồng hãng cần lắp đặt: ngày biên bản nghiệm thu mới nhất. Hợp đồng hãng không cần lắp đặt: ngày muộn nhất trong (ngày duyệt phiếu xuất kho bán hàng, ngày lập phiếu xuất bán hàng mượn, ngày duyệt hạch toán dịch vụ). Hợp đồng dịch vụ bảo hành - sửa chữa: ngày muộn nhất trong (ngày cập nhật hạch toán dịch vụ, ngày lập phiếu xuất bán hàng mượn, ngày duyệt phiếu xuất kho). Không có các chứng từ trên (mọi loại hợp đồng): ngày bàn giao nghiệm thu mới nhất khai ở công nợ đầu kỳ đánh dấu quá hạn. Không phụ thuộc Thời gian lọc.', TIP['nt']),
            ('Cột Số ngày nợ (Ngày)', '(Hôm nay) − (Ngày nghiệm thu + 6 ngày), lấy phần nguyên số ngày; âm thì ghi 0. Chỉ hiện khi Số dư cuối kỳ của hợp đồng > 0 và có Ngày nghiệm thu. Tính tới HÔM NAY, không tới Đến ngày.', TIP['snn']),
            ('Chân bảng – N dòng hợp đồng', 'Số dòng hợp đồng trong tập dữ liệu (không đếm dòng nhân viên, dòng Tổng cộng).', '—'),
        ], DATA_W, 'Bảng dưới mô tả cách hệ thống tính từng chỉ tiêu, từng cột số liệu và nội dung icon ⓘ (nguyên văn trên giao diện).'),
        ('Danh sách liên kết mở từ số liệu', LINK_HEAD, [
            ('Số hợp đồng ở cột Đơn hàng/hợp đồng (dòng hợp đồng)', 'Không phải popup — mở trang xem hợp đồng ở tab mới', 'Hợp đồng đang nợ này ký với ai, giá trị, tiến độ giao hàng / nghiệm thu thế nào để đi thu nợ', 'Đúng hợp đồng của dòng; số hợp đồng chỉ là chữ thường (không bấm) với loại hợp đồng chưa có trang xem'),
            ('Các ô số, dòng nhân viên, dòng Tổng cộng', 'Không bấm được', 'Màn không có cửa sổ chi tiết chứng từ (giữ như hệ thống cũ)', 'Muốn xem từng chứng từ: dùng Báo cáo chi tiết công nợ khách hàng hoặc Bảng đối chiếu công nợ 1 khách hàng'),
        ], LINK_W, None),
    ],
})

# 2.2 Tìm kiếm và lọc ------------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Datepicker.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc báo cáo tổng hợp công nợ khách hàng theo nhân viên'],
        ['Mô tả', 'Thu hẹp báo cáo bằng ô tìm nhanh và các ô lọc: Thời gian (bắt buộc), Khách hàng, Số hợp đồng, Số dư cuối kỳ, Ngày nghiệm thu, Công ty / Phòng ban / Bộ phận / Nhân viên (hiện theo phạm vi quyền).'],
        ['Tác nhân', QA],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn báo cáo.'],
        ['Dòng sự kiện chính', '1. Người dùng chọn Thời gian và các ô lọc cần dùng; hoặc nhập từ khoá vào ô tìm nhanh / ô Số hợp đồng rồi bấm Tìm kiếm hoặc Enter.\n2. Hệ thống áp đồng thời mọi điều kiện, tải lại trang 1 và dòng Tổng cộng.'],
        ['Dòng sự kiện phụ', '• Ô chọn (Thời gian, Khách hàng, Số dư cuối kỳ, Ngày nghiệm thu, Công ty… Nhân viên) lọc ngay khi chọn; ô gõ chữ (tìm nhanh, Số hợp đồng) chỉ lọc khi bấm Tìm kiếm / Enter.\n• Bấm Tìm kiếm khi chưa chọn Thời gian → chữ đỏ "Vui lòng chọn thời gian" dưới ô.\n• Lịch Từ ngày làm mờ các ngày sau Đến ngày, lịch Đến ngày làm mờ các ngày trước Từ ngày; gõ tay ngày bị mờ thì ô không nhận. Nếu Từ ngày > Đến ngày vẫn xảy ra → chữ đỏ và thông báo "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", xoá bảng.\n• Bấm Làm mới → mọi ô về trống (kể cả Thời gian), bảng về "Chọn thời gian để xem báo cáo."\n• Bộ lọc được ghi nhớ 10 phút khi rời màn rồi quay lại; tải lại trang (F5) thì xoá như Làm mới.'],
    ],
    'anh': [('02_filter', 'Khu vực bộ lọc (đã chọn Thời gian, Nhân viên, Số dư cuối kỳ = Dư nợ)'),
            ('02b_required', 'Bấm Tìm kiếm khi chưa chọn Thời gian')],
    'ui': ui(UI8, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', ['- Placeholder "Tìm theo số hợp đồng, mã hoặc tên khách hàng".', '- Tìm gần đúng, giữ dòng hợp đồng có số hợp đồng hoặc mã / tên khách hàng chứa từ khoá; số liệu của dòng giữ nguyên cả hợp đồng.', '- Lọc khi bấm Tìm kiếm / Enter.']],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', '–', ['- Áp từ khoá và mọi ô lọc, tải lại từ trang 1.', '- Thiếu Thời gian: chữ đỏ dưới ô, không tải.']],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', '–', 'Xoá mọi điều kiện (kể cả Thời gian), xoá bộ lọc đã ghi nhớ, bảng về trạng thái chưa chọn thời gian.'],
        ['Nút Ẩn tìm kiếm nâng cao / Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Đang mở', 'Đóng / mở khu vực các ô lọc; chữ nút đổi theo trạng thái.'],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', '–', 'Mở cửa sổ "Cài đặt bộ lọc" (mục 2.3).'],
        ['Ô Thời gian', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Có', 'Trống', ['- 2 ô Từ ngày → Đến ngày, có dấu (*).', '- Lọc theo ngày hạch toán; Từ ngày chia Số dư đầu kỳ / phát sinh (BR-02).', '- Trống khi bấm Tìm kiếm: "Vui lòng chọn thời gian".', '- Lịch Từ ngày làm mờ ngày sau Đến ngày; lịch Đến ngày làm mờ ngày trước Từ ngày; gõ tay ngày bị mờ thì không nhận.', '- Từ > Đến (nếu xảy ra): "Đến ngày phải lớn hơn hoặc bằng Từ ngày."']],
        ['Ô Khách hàng', 'Dropdown', 'Enable', 'Danh sách khách hàng, chọn 1', 'Không', 'Trống', ['- Placeholder "Nhập tên hoặc mã khách hàng"; gõ ít nhất 2 ký tự mới tìm.', '- Có nút × xoá nhanh.', '- Chỉ giữ bút toán của khách hàng đã chọn (cả Số dư đầu kỳ dòng Tổng cộng).']],
        ['Ô Số hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', ['- Khớp ĐÚNG toàn bộ số hợp đồng (không tìm gần đúng) với các dòng.', '- Riêng Số dư đầu kỳ dòng Tổng cộng so gần đúng (BR-06).', '- Lọc khi bấm Tìm kiếm / Enter.']],
        ['Ô Số dư cuối kỳ', 'Dropdown', 'Enable', 'Tất cả / Dư nợ / Dư có', 'Không', 'Trống (= Tất cả)', ['- Mặc định: trống = Tất cả.', '- Tất cả: mọi hợp đồng.', '- Dư nợ: hợp đồng có Số dư cuối kỳ > 0.', '- Dư có: hợp đồng có Số dư cuối kỳ < 0.', '- Hợp đồng Số dư cuối kỳ = 0 chỉ hiện khi chọn Tất cả.']],
        ['Ô Ngày nghiệm thu', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Chỉ giữ hợp đồng có Ngày nghiệm thu ĐÚNG BẰNG ngày chọn.'],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty, chọn nhiều', 'Không', 'Trống', ['- Chỉ hiện với quyền cấp tổng công ty.', '- Lọc theo công ty ghi trên bút toán.', '- Icon ổ khoá cạnh nhãn: bật / tắt "Hiện cả công ty đã khoá".']],
        ['Ô Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban, chọn nhiều', 'Không', 'Trống', ['- Hiện với quyền cấp tổng công ty, công ty, phòng ban.', '- Lọc theo phòng ban ghi trên bút toán.', '- Icon ổ khoá: bật / tắt "Hiện cả phòng ban đã khoá".']],
        ['Ô Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách bộ phận, chọn nhiều', 'Không', 'Trống', ['- Hiện khi có 1 trong 4 quyền.', '- Lọc theo bộ phận ghi trên bút toán.', '- Icon ổ khoá: bật / tắt "Hiện cả bộ phận đã khoá".']],
        ['Ô Nhân viên', 'Dropdown', 'Enable / Ẩn', 'Danh sách nhân viên, chọn nhiều', 'Không', 'Trống', ['- Hiện khi có 1 trong 4 quyền; không quyền thì ẩn (chỉ thấy hợp đồng của mình).', '- Lọc theo NHÂN VIÊN TẠO HỢP ĐỒNG.']],
        ['Chữ báo lỗi dưới ô Thời gian', 'Toast / Alert', 'Ẩn / Hiển thị', '–', '–', 'Ẩn', ['- "Vui lòng chọn thời gian" khi bấm Tìm kiếm mà ô trống; tự tắt khi đã chọn.', '- "Đến ngày phải lớn hơn hoặc bằng Từ ngày." khi Từ > Đến, kèm thông báo góc màn cùng câu.']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Chọn / đổi giá trị ô chọn', 'Change', 'During:\n– Thời gian chưa đủ 2 đầu: xoá bảng, không tải.\n– Từ ngày > Đến ngày: báo đỏ dưới ô + thông báo "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", xoá bảng, không tải.\n' + LOI + '\nAfter:\n– Ghi nhớ bộ lọc, tải lại trang 1 và dòng Tổng cộng.'],
        ['Gõ ô tìm nhanh / Số hợp đồng', 'Change', 'After:\n– Chỉ ghi nhớ giá trị, CHƯA lọc (chờ Tìm kiếm / Enter).'],
        ['Bấm Tìm kiếm / nhấn Enter', 'Click', 'During:\n– Thời gian trống → chữ đỏ "Vui lòng chọn thời gian", không tải.\n' + LOI + '\nAfter:\n– Áp mọi điều kiện, tải lại từ trang 1.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Mọi ô về trống, xoá bộ lọc đã ghi nhớ, bảng ghi "Chọn thời gian để xem báo cáo."'],
        ['Bấm Ẩn tìm kiếm nâng cao / Tìm kiếm nâng cao', 'Click', 'After:\n– Thu gọn / mở khu vực ô lọc.'],
    ],
})

# 2.3 Cài đặt bộ lọc --------------------------------------------------------------
FR.append({
    'ten': 'Cài đặt bộ lọc',
    'qtc': 'Cài đặt bộ lọc.',
    'gioi_thieu': [
        ['Tên chức năng', 'Cài đặt bộ lọc'],
        ['Mô tả', 'Chọn ô lọc nào hiển thị và thứ tự các ô trong khu vực bộ lọc; cài đặt lưu theo từng màn hình cho từng người dùng.'],
        ['Tác nhân', QA],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Cài đặt bộ lọc.\n2. Hệ thống mở cửa sổ "Cài đặt bộ lọc" với 6 trường lọc.\n3. Người dùng tích / bỏ tích, kéo đổi thứ tự rồi bấm Lưu.\n4. Hệ thống áp dụng lên khu vực bộ lọc.'],
        ['Dòng sự kiện phụ', '• Khôi phục mặc định: trả về cách hiển thị ban đầu.\n• Đóng / (x): không lưu thay đổi.'],
    ],
    'menu_them': ' => Cài đặt bộ lọc {icon:btn_caidatboloc}',
    'ghi_chu_layout': POPUP % '"Cài đặt bộ lọc"',
    'anh': [('04_settings', 'Cửa sổ Cài đặt bộ lọc')],
    'ui': ui(UI7, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', '"Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình."'],
        ['Danh sách trường lọc', 'Table/Grid', 'Enable', '6 trường', 'Theo cấu hình đã lưu', ['- Thời gian, Khách hàng, Số hợp đồng, Số dư cuối kỳ, Ngày nghiệm thu, Công ty / Phòng ban / Bộ phận / Nhân viên.', '- Mỗi dòng có ô tích và biểu tượng kéo đổi vị trí.', '- Dòng Công ty / Phòng ban / Bộ phận / Nhân viên chỉ có khi người dùng có 1 trong 4 quyền.']],
        ['Nút Lưu', 'Button', 'Enable', '–', '–', 'Lưu cài đặt cho người dùng ở màn này, áp dụng ngay.'],
        ['Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiện lại đủ trường theo thứ tự mặc định.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', 'Đóng cửa sổ, không lưu.'],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở cửa sổ theo cấu hình đang dùng.'],
        ['Tích / bỏ tích, kéo đổi thứ tự', 'Drag', 'After:\n– Đổi trong cửa sổ, chưa áp dụng.'],
        ['Bấm Lưu', 'Click', 'After:\n– Lưu và áp dụng lên khu vực bộ lọc.'],
        ['Bấm Khôi phục mặc định / Đóng', 'Click', 'After:\n– Khôi phục mặc định hoặc đóng không lưu.'],
    ],
})

# 2.4 Xuất Excel ----------------------------------------------------------------
EXPORT_FIELDS = ['Nhân viên / Đơn hàng - hợp đồng', 'Khách hàng', 'Số dư đầu kỳ', 'PS tăng - Hàng hóa/Dịch vụ', 'PS tăng - Điều chỉnh công nợ',
                 'PS tăng - Cộng', 'PS giảm - Nhập trả lại', 'PS giảm - Đã thanh toán', 'PS giảm - Điều chỉnh công nợ', 'PS giảm - Cộng',
                 'Trả lại tiền thừa', 'Số dư cuối kỳ', 'Ngày nghiệm thu', 'Số ngày nợ (Ngày)']
FR.append({
    'ten': 'Xuất Excel', 'uc': 'uc_xuat',
    'qtc': 'Quy tắc Excel.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất báo cáo ra Excel (chọn trường)'],
        ['Mô tả', 'Xuất TOÀN BỘ dòng theo bộ lọc đang áp (mọi trang) ra file Excel, bố cục như màn: dòng Tổng cộng → dòng nhân viên → dòng hợp đồng; người dùng chọn trường và thứ tự cột (BR-11).'],
        ['Tác nhân', QA],
        ['Điều kiện ban đầu', DK + '\n3. Đã chọn Thời gian hợp lệ.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất Excel", tích sẵn đủ 14 trường.\n3. Người dùng tích / bỏ tích, kéo đổi thứ tự rồi bấm Xuất file.\n4. Hệ thống tải file bao_cao_tong_hop_cong_no_khach_hang_theo_nhan_vien.xlsx, đóng cửa sổ, báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Chưa chọn Thời gian → chữ đỏ dưới ô + thông báo "Vui lòng chọn thời gian", không mở cửa sổ.\n• Từ ngày > Đến ngày → "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", không mở cửa sổ.\n• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Kết quả rỗng vẫn xuất file (tiêu đề, kỳ, tên cột, dòng Tổng cộng).\n• Lỗi → "Lỗi khi xuất Excel" (hoặc câu lỗi hệ thống trả về).'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': POPUP % '"Chọn trường xuất Excel"',
    'anh': [('03_export', 'Cửa sổ Chọn trường xuất Excel'),
            ('03c_excel', 'File Excel tải về (đủ 14 trường; lọc Thời gian 01/10/2026 – 31/10/2026, 1 nhân viên, Số dư cuối kỳ = Dư nợ)')],
    'ui': ui(UI8, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', '–', '"Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file."'],
        ['Danh sách trường', 'Table/Grid', 'Enable', '14 trường', 'Có (≥ 1)', 'Tích tất cả', ['- ' + ', '.join(EXPORT_FIELDS) + '.', '- Mỗi trường có ô tích và biểu tượng ☰ kéo đổi vị trí; cột STT luôn có ở đầu file.']],
        ['Nút Chọn tất cả', 'Button', 'Enable', '–', '–', '–', 'Tích mọi trường.'],
        ['Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', 'Bỏ tích mọi trường.'],
        ['Dòng đếm', 'Label', 'Hiển thị', '–', '–', 'Đang chọn 14/14 trường', '"Đang chọn x/14 trường".'],
        ['Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Enable', ['- Tải file Excel.', '- Không bấm được khi chưa chọn trường nào hoặc đang xuất.']],
        ['Nút Đóng / (x)', 'Button', 'Enable', '–', '–', '–', 'Đóng cửa sổ, không xuất.'],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'Before:\n– Thời gian trống → "Vui lòng chọn thời gian"; Từ > Đến → "Đến ngày phải lớn hơn hoặc bằng Từ ngày."; dừng.\nAfter:\n– Mở cửa sổ, tích sẵn 14 trường.'],
        ['Bấm Xuất file', 'Click', 'During:\n– Lấy toàn bộ dòng theo bộ lọc và phạm vi quyền (không chỉ trang đang xem).\n' + LOI + '\nAfter:\n– Tải file: dòng 1 "BÁO CÁO TỔNG HỢP CÔNG NỢ KHÁCH HÀNG THEO NHÂN VIÊN", dòng 2 "Thời gian: dd/mm/yyyy - dd/mm/yyyy", tiêu đề 2 tầng (nhóm PS tăng / PS giảm), dòng Tổng cộng, rồi từng nhân viên (in đậm) và hợp đồng.\n– Đóng cửa sổ, báo "Xuất Excel thành công".'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# 2.5 Xuất Excel mẫu in ------------------------------------------------------------
FR.append({
    'ten': 'Xuất Excel mẫu in', 'uc': 'uc_xuatmauin',
    'qtc': 'Quy tắc Excel.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất Excel theo mẫu in'],
        ['Mô tả', 'Tải ngay file Excel theo mẫu in cố định: 4 cột số gộp (Số dư đầu kỳ, Giá trị hợp đồng thực tế, Giá trị đã thanh toán, Giá trị còn nợ cuối kỳ), Ngày nghiệm thu, Số ngày nợ và các cột để trống cho nhân viên điền giải trình, kế hoạch thu hồi, xác nhận công nợ (BR-11).'],
        ['Tác nhân', QA],
        ['Điều kiện ban đầu', DK + '\n3. Đã chọn Thời gian hợp lệ.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm Xuất Excel mẫu in.\n2. Hệ thống lấy toàn bộ dòng theo bộ lọc, tải file bao_cao_tong_hop_cong_no_khach_hang_theo_nhan_vien_mau_in.xlsx, báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Chưa chọn Thời gian → "Vui lòng chọn thời gian"; Từ > Đến → "Đến ngày phải lớn hơn hoặc bằng Từ ngày."; không xuất.\n• Không có cửa sổ chọn trường.\n• Lỗi → "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel mẫu in {icon:btn_xuatexcelmauin}',
    'ghi_chu_layout': 'Không mở cửa sổ: bấm nút là tải file ngay. Ảnh dưới là bố cục file tải về (dữ liệu thật trên môi trường thử nghiệm).',
    'anh': [('07_mauin', 'Bố cục file Excel mẫu in')],
    'ui': ui(UI7, [
        ['Nút Xuất Excel mẫu in', 'Button', 'Enable', '–', 'Hiển thị', ['- Tải file ngay.', '- Khoá trong lúc đang xuất.']],
        ['File – dòng tiêu đề', 'Label', 'Hiển thị', '–', '–', ['- Dòng 1: "BÁO CÁO TỔNG HỢP CÔNG NỢ KHÁCH HÀNG THEO NHÂN VIÊN".', '- Dòng 2: "Thời gian: <Từ ngày> - <Đến ngày>".']],
        ['File – tiêu đề cột', 'Table/Grid', 'Hiển thị', '15 cột', '–', ['- STT, Đơn hàng/Hợp đồng, Khách hàng, Số dư đầu kỳ, Giá trị hợp đồng thực tế, Giá trị đã thanh toán, Giá trị còn nợ cuối kỳ, Ngày nghiệm thu, Ngày xuất hóa đơn, Số ngày nợ (Ngày), Giải trình lý do chưa thu nợ, Kế hoạch ngày thu hồi công nợ.', '- "Xác nhận công nợ" gộp 3 cột con: Đã có, Chưa có, Lý do chưa xác nhận nợ.']],
        ['File – cột Giá trị hợp đồng thực tế', 'Table/Grid', 'Hiển thị', 'Số', '–', '= Hàng hóa/Dịch vụ + Điều chỉnh công nợ (tăng) (= Cộng phát sinh tăng trên màn).'],
        ['File – cột Giá trị đã thanh toán', 'Table/Grid', 'Hiển thị', 'Số', '–', '= Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ (giảm) (= Cộng phát sinh giảm trên màn).'],
        ['File – cột Giá trị còn nợ cuối kỳ', 'Table/Grid', 'Hiển thị', 'Số', '–', '= Số dư cuối kỳ trên màn (đã gồm Trả lại tiền thừa).'],
        ['File – cột để trống', 'Table/Grid', 'Hiển thị', '–', 'Trống', 'Ngày xuất hóa đơn, Giải trình lý do chưa thu nợ, Kế hoạch ngày thu hồi công nợ, Xác nhận công nợ (Đã có / Chưa có / Lý do chưa xác nhận nợ): để nhân viên điền tay.'],
        ['File – dòng dữ liệu', 'Table/Grid', 'Hiển thị', '–', '–', ['- Dòng Tổng cộng (gộp 3 cột đầu), dòng nhân viên (in đậm, gộp cột Đơn hàng/Hợp đồng + Khách hàng), dòng hợp đồng.', '- Số định dạng 1,234,567; số 0 để trống.']],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm Xuất Excel mẫu in', 'Click', 'Before:\n– Thời gian trống / Từ > Đến → báo lỗi như mục 2.4, dừng.\nDuring:\n– Lấy toàn bộ dòng theo bộ lọc và phạm vi quyền.\n' + LOI + '\nAfter:\n– Tải file mẫu in, báo "Xuất Excel thành công".'],
    ],
})

S = {
    'ten': TEN,
    'menu': [('Bán hàng', 'menu_phanhe'), ('Báo cáo', 'menu_rail'), ('Báo cáo công nợ', 'menu_nhom'), ('Tổng hợp công nợ theo NV', 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu chức năng.',
        'Làm rõ từng con số trên báo cáo lấy từ chứng từ nào, điều kiện nào (ngày hạch toán, phạm vi quyền), cách tính dòng nhân viên, dòng Tổng cộng, Ngày nghiệm thu và Số ngày nợ.',
        'Làm rõ phạm vi dữ liệu 4 cấp (tổng công ty / công ty / phòng ban / bộ phận) và người không có quyền chỉ thấy hợp đồng do mình tạo.',
    ],
    'thuat_ngu': [
        ['Công nợ phải thu', 'Số tiền khách hàng còn phải trả, ghi trên tài khoản 131 và các tài khoản con.'],
        ['Hạch toán / ngày hạch toán', 'Kế toán ghi chứng từ vào sổ công nợ; báo cáo lọc theo ngày hạch toán, không theo ngày lập phiếu.'],
        ['Phát sinh Nợ / Có', 'Nợ làm tăng công nợ khách; Có làm giảm công nợ khách.'],
        ['Nhân viên tạo hợp đồng', 'Người lập hợp đồng trên hệ thống — báo cáo gom công nợ theo người này (không theo người phụ trách hiện tại).'],
        ['Dư nợ / Dư có', 'Số dư cuối kỳ dương: khách còn nợ; âm: khách trả thừa / trả trước.'],
        ['Ngày nghiệm thu', 'Mốc bàn giao của hợp đồng dùng tính Số ngày nợ (BR-07).'],
        ['Số ngày nợ', 'Số ngày khách nợ tính tới hôm nay, sau 6 ngày ân hạn kể từ Ngày nghiệm thu (BR-08).'],
        ['HĐ', 'Hợp đồng / đơn hàng.'],
        ['NV', 'Nhân viên.'],
    ],
    'quyen_truoc': ['Màn hình KHÔNG chặn quyền vào: mọi người dùng đăng nhập đều mở được. 4 quyền dưới đây (nhóm báo cáo công nợ) chỉ mở rộng PHẠM VI DỮ LIỆU. Người dùng có nhiều quyền thì lấy cấp rộng nhất. Quyền gán vào vai trò theo công ty.'],
    'quyen_rows': [
        [Q4 + 'tổng công ty', 'Thấy công nợ của mọi công ty; có ô lọc Công ty, Phòng ban, Bộ phận, Nhân viên.'],
        [Q4 + 'công ty', 'Thấy bút toán của công ty đang làm việc + hợp đồng do mình tạo; có ô Phòng ban, Bộ phận, Nhân viên.'],
        [Q4 + 'phòng ban', 'Thấy bút toán của các phòng ban mình quản lý và phòng ban mình đang thuộc + hợp đồng do mình tạo; có ô Phòng ban, Bộ phận, Nhân viên.'],
        [Q4 + 'bộ phận', 'Thấy bút toán của các bộ phận mình quản lý và bộ phận mình đang thuộc + hợp đồng do mình tạo; có ô Bộ phận, Nhân viên.'],
        ['(Không có quyền nào)', 'Chỉ thấy hợp đồng do mình tạo; không có ô Công ty / Phòng ban / Bộ phận / Nhân viên.'],
    ],
    'ma_tran': [['Chức năng', 'Tổng công ty', 'Công ty', 'Phòng ban', 'Bộ phận', 'Không quyền']] + [[f, 'Có', 'Có', 'Có', 'Có', 'Có'] for f in [
        'FR-01 Xem báo cáo', 'FR-02 Tìm kiếm và lọc', 'FR-03 Cài đặt bộ lọc', 'FR-04 Xuất Excel', 'FR-05 Xuất Excel mẫu in']] + [
        ['Ô lọc Công ty', 'Có', 'Không', 'Không', 'Không', 'Không'],
        ['Ô lọc Phòng ban', 'Có', 'Có', 'Có', 'Không', 'Không'],
        ['Ô lọc Bộ phận, Nhân viên', 'Có', 'Có', 'Có', 'Có', 'Không']],
    'ma_tran_widths': [2.2, 0.85, 0.8, 0.85, 0.8, 0.85],
    'quyen_sau': ['Phạm vi dữ liệu áp cho MỌI con số: dòng hợp đồng, dòng nhân viên, dòng Tổng cộng (kể cả Số dư đầu kỳ) và cả 2 file Excel (BR-01).'],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Phạm vi dữ liệu theo quyền', [
            '– Cấp lấy theo quyền rộng nhất người dùng có: tổng công ty > công ty > phòng ban > bộ phận > không quyền.',
            '– Tổng công ty: không giới hạn.',
            '– Công ty: bút toán ghi công ty = công ty đang làm việc, HOẶC hợp đồng do mình tạo.',
            '– Phòng ban: bút toán ghi phòng ban thuộc danh sách phòng mình quản lý + phòng mình đang thuộc, HOẶC hợp đồng do mình tạo.',
            '– Bộ phận: như phòng ban nhưng theo bộ phận.',
            '– Không quyền: chỉ hợp đồng do mình tạo.',
            '– Áp cho mọi dòng, dòng Tổng cộng (kể cả Số dư đầu kỳ) và Excel; ô lọc tổ chức chỉ thu hẹp thêm trong phạm vi này.'],
            ['Xem báo cáo', 'Tìm kiếm và lọc', 'Xuất Excel', 'Xuất Excel mẫu in']),
        ('BR-02', 'Nguồn số liệu và kỳ', [
            '– Chỉ đọc bút toán tài khoản phải thu khách hàng (131 và tài khoản con trực tiếp), số tiền quy đổi VND.',
            '– Lọc theo ngày hạch toán: trước Từ ngày → Số dư đầu kỳ; từ Từ ngày đến hết Đến ngày → phát sinh; sau Đến ngày → không tính.',
            '– Dòng hợp đồng chỉ lấy bút toán có khách hàng, có nhân viên tạo hợp đồng, số tiền > 0.',
            '– Phiếu chưa hạch toán chưa làm đổi báo cáo; huỷ hạch toán thì số trả về.'], ['Xem báo cáo', 'Xuất Excel', 'Xuất Excel mẫu in']),
        ('BR-03', 'Gom dòng', [
            '– 1 dòng cho mỗi cặp (nhân viên tạo hợp đồng, hợp đồng); hợp đồng có số liệu bằng 0 hết vẫn hiện khi chọn Số dư cuối kỳ = Tất cả.',
            '– Hợp đồng có bút toán của nhiều khách hàng: cột Khách hàng chỉ hiện 1 khách hàng.',
            '– Bút toán không gắn hợp đồng: gom 1 dòng có ô hợp đồng trống dưới nhân viên.',
            '– Nhân viên xếp theo thứ tự tạo nhân viên trên hệ thống; số hợp đồng lấy theo bút toán.'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-04', 'Công thức các cột', [
            '– Hàng hóa/Dịch vụ = Nợ − Có của phiếu xuất kho, xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ bảo hành - sửa chữa (+ Nợ của khai báo công nợ đầu kỳ).',
            '– Điều chỉnh công nợ tăng / giảm = Nợ / Có của phiếu kế toán điều chỉnh công nợ.',
            '– Nhập trả lại = Có − Nợ của phiếu nhập hàng; Đã thanh toán = Có của phiếu thu, phiếu báo có, khai báo công nợ đầu kỳ.',
            '– Trả lại tiền thừa = Nợ của phiếu chi, phiếu ủy nhiệm chi.',
            '– Số dư cuối kỳ = Đầu kỳ + Cộng tăng − Cộng giảm + Trả lại tiền thừa.'], ['Xem báo cáo', 'Xuất Excel', 'Xuất Excel mẫu in']),
        ('BR-05', 'Dòng nhân viên', ['– Bằng tổng ĐỦ mọi hợp đồng của nhân viên theo bộ lọc, kể cả hợp đồng ở trang khác; không đổi khi chuyển trang hay đổi số dòng/trang.'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-06', 'Dòng Tổng cộng', [
            '– Cột phát sinh, Trả lại tiền thừa: cộng mọi dòng hợp đồng theo bộ lọc (mọi trang).',
            '– Số dư đầu kỳ: Nợ − Có của mọi bút toán trước Từ ngày trong phạm vi quyền + ô Công ty / Phòng ban / Bộ phận / Nhân viên / Khách hàng, Số hợp đồng so gần đúng; không cần khách hàng / nhân viên; không theo Số dư cuối kỳ, Ngày nghiệm thu, ô tìm nhanh.',
            '– Số dư cuối kỳ = Số dư đầu kỳ (dòng Tổng cộng) + Cộng tăng − Cộng giảm + Trả lại tiền thừa.',
            '– Số 0 in "0".'], ['Xem báo cáo', 'Xuất Excel', 'Xuất Excel mẫu in']),
        ('BR-07', 'Ngày nghiệm thu', [
            '– Hợp đồng hãng cần lắp đặt: ngày biên bản nghiệm thu mới nhất.',
            '– Hợp đồng hãng còn lại: muộn nhất trong phiếu xuất kho bán hàng (ngày duyệt), phiếu xuất bán hàng mượn, hạch toán dịch vụ (ngày duyệt).',
            '– Hợp đồng dịch vụ bảo hành - sửa chữa: muộn nhất trong hạch toán dịch vụ, phiếu xuất bán hàng mượn, phiếu xuất kho.',
            '– Không có: ngày bàn giao nghiệm thu khai ở công nợ đầu kỳ quá hạn; vẫn không có thì để trống.'], ['Xem báo cáo', 'Tìm kiếm và lọc', 'Xuất Excel']),
        ('BR-08', 'Số ngày nợ', ['– = Hôm nay − (Ngày nghiệm thu + 6 ngày), âm thì 0; chỉ hiện khi Số dư cuối kỳ của hợp đồng > 0 và có Ngày nghiệm thu; không theo Đến ngày.'], ['Xem báo cáo', 'Xuất Excel', 'Xuất Excel mẫu in']),
        ('BR-09', 'Bộ lọc', [
            '– Thời gian bắt buộc; Từ ngày ≤ Đến ngày ("Đến ngày phải lớn hơn hoặc bằng Từ ngày.").',
            '– Số hợp đồng khớp đúng; ô tìm nhanh tìm gần đúng số hợp đồng, mã / tên khách hàng và giữ nguyên số của cả hợp đồng.',
            '– Số dư cuối kỳ: Dư nợ > 0, Dư có < 0, tính theo Số dư cuối kỳ từng hợp đồng.',
            '– Ngày nghiệm thu: đúng bằng ngày chọn.',
            '– Nhân viên = nhân viên tạo hợp đồng; Công ty / Phòng ban / Bộ phận theo đơn vị ghi trên bút toán; chọn nhiều.'], ['Tìm kiếm và lọc', 'Xuất Excel', 'Xuất Excel mẫu in']),
        ('BR-10', 'Định dạng số', ['– Số tiền 1,234,567, không lẻ; số âm có dấu "-"; số 0 để trống (trừ dòng Tổng cộng in "0").', '– Ngày dd/mm/yyyy.'], ['Xem báo cáo', 'Xuất Excel', 'Xuất Excel mẫu in']),
        ('BR-11', 'Xuất Excel', [
            '– Cả 2 mẫu xuất MỌI dòng theo bộ lọc đang áp và phạm vi quyền, tải ngay về máy.',
            '– Mẫu chọn trường: tên file bao_cao_tong_hop_cong_no_khach_hang_theo_nhan_vien.xlsx, STT + các trường đã chọn theo thứ tự đã kéo.',
            '– Mẫu in: tên file bao_cao_tong_hop_cong_no_khach_hang_theo_nhan_vien_mau_in.xlsx, 15 cột cố định.'], ['Xuất Excel', 'Xuất Excel mẫu in']),
    ],
    'phan5': {
        'title': 'Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu',
        'cau_dan': 'Các màn hình dưới đây dùng chung công thức công nợ với báo cáo này, hoặc là nơi lập chứng từ gốc làm thay đổi số liệu báo cáo (khi chứng từ được hạch toán), hoặc được mở từ báo cáo.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng (theo phạm vi quyền)',
    'mains': [('FR-01', 'Xem báo cáo tổng hợp công nợ KH theo NV', 'view'), ('FR-04', 'Xuất Excel', 'io'),
              ('FR-05', 'Xuất Excel mẫu in', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc', 'view'), ('FR-03', 'Cài đặt bộ lọc', 'view')],
    'rieng': [('FR-04', 'Xuất Excel', 'io', 'uc_xuat'), ('FR-05', 'Xuất Excel mẫu in', 'io', 'uc_xuatmauin')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', B.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)

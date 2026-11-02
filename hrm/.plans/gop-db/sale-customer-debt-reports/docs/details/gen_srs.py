# -*- coding: utf-8 -*-
"""SRS - BC chi tiết công nợ KH (form Danh mục quốc gia + quy tắc màn BÁO CÁO của skill srs-documenter).

Nguồn (code HRM hiện tại, 02/11/2026):
  FE hrm-client/pages/sale/customer-debt-details/{index.vue, components/InvoiceablesModal.vue, components/export-excel.js},
     components/V2BaseCompanyDepartmentFilter.vue, components/modal/export-fields-modal.vue, utils/invoiceable-link.js,
     utils/finance/customerDebtContractLink.js, components/subsystem-menu/sale-hub.js (Bán hàng > Báo cáo > Báo cáo công nợ)
  BE hrm-api/Modules/Finance: Http/Controllers/V1/CustomerDebtDetailController.php, Services/CustomerDebt/{CustomerDebtDetail
     ReportService, AbstractCustomerDebtReportService, CustomerDebtAggregator, CustomerDebtScope}.php; quyền 1683-1686
     (Timesheet PermissionsTableSeeder).
  Số liệu ảnh: dev-hrm 02/11/2026, kỳ 01/10/2026 - 31/10/2026, KH 89THUPTR-62 (capture.js).
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _report_lib as R  # noqa: E402
L = R.L

TEN = 'BC chi tiết công nợ KH'
TEN_MAN = 'Báo cáo chi tiết công nợ khách hàng'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q = 'Người dùng có quyền thực hiện chức năng (mọi người dùng đăng nhập; phạm vi số liệu theo 4 quyền "Xem báo cáo chi tiết công nợ khách hàng theo …")'
DK = '1. Người dùng đăng nhập thành công.\n2. Người dùng mở được phân hệ Bán hàng (màn không chặn quyền; quyền chỉ quyết phạm vi số liệu – Phần 2).'
LOI = '– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung SRS_Các quy tắc chung_VN_1.0, không thực hiện bước After.'
POPUP = 'Modal %s được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'
KY = 'Ngày hạch toán của chứng từ từ "Từ ngày" đến hết "Đến ngày"'

UI7 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả']
UI7W = [0.5, 1.1, 0.75, 0.7, 0.7, 0.7, 3.2]
UI8 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả']
UI8W = [0.5, 1.05, 0.75, 0.7, 0.8, 0.55, 0.7, 2.75]


def ui(header, rows):
    return [header] + [[str(i + 1)] + [('\n'.join(c) if isinstance(c, (list, tuple)) else c) for c in r]
                       for i, r in enumerate(rows)]


def tbl(header, rows):
    return [header] + [[str(i + 1)] + list(r) for i, r in enumerate(rows)]


# ---------------------------------------------------------------- ⓘ nguyên văn (index.vue COLUMN_TIPS)
P = 'Tính trên sổ tài khoản phải thu khách hàng (TK 131 và các tài khoản con), số tiền quy đổi VND, theo ngày hạch toán.'
TIP = {
    'stt': 'Số thứ tự. • Dòng khách hàng (in đậm) đánh số 1, 2, 3…; các hợp đồng của khách hàng đó đánh số 1.1, 1.2… • Số thứ tự nối tiếp khi sang trang sau.',
    'hd': 'Đơn hàng/hợp đồng phát sinh công nợ. • Dòng in đậm là khách hàng (mã - tên), số liệu = cộng TẤT CẢ hợp đồng của khách hàng đó theo bộ lọc (kể cả hợp đồng nằm ở trang khác). • Bấm số hợp đồng để mở hợp đồng ở tab mới. • Ô trống: chứng từ không gắn hợp đồng (phiếu báo có hoặc kế toán chưa được ghi nhận).',
    'pb': 'Phòng ban của người tạo hợp đồng. • Lấy theo hồ sơ HIỆN TẠI của người tạo hợp đồng (nhân viên đã chuyển phòng thì hiện phòng mới).',
    'bp': 'Bộ phận của người tạo hợp đồng. • Lấy theo hồ sơ HIỆN TẠI của người tạo hợp đồng (nhân viên đã chuyển bộ phận thì hiện bộ phận mới).',
    'nv': 'Nhân viên kinh doanh = người tạo hợp đồng. • Bộ lọc "Nhân viên" cũng lọc theo người tạo hợp đồng.',
    'dk': 'Công nợ phải thu còn lại trước "Từ ngày". • Số dư đầu kỳ = Tổng phát sinh Nợ − Tổng phát sinh Có của các chứng từ có ngày hạch toán trước "Từ ngày". • Số dương: khách còn nợ; số âm: khách trả thừa / trả trước. • ' + P,
    'tang': 'Các khoản làm TĂNG công nợ phải thu, ngày hạch toán từ "Từ ngày" đến "Đến ngày". • Gồm: Hàng hóa/Dịch vụ, Điều chỉnh công nợ (ghi tăng). • ' + P,
    'hh': 'Giá trị hàng hóa, dịch vụ bán cho khách ghi nhận công nợ trong kỳ. • Chứng từ: phiếu xuất kho, phiếu xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ bảo hành - sửa chữa, khai báo công nợ đầu kỳ. • Hàng hóa/Dịch vụ = Phát sinh Nợ của các chứng từ trên − Phát sinh Có của chính các chứng từ đó (trừ khai báo công nợ đầu kỳ). • Bấm vào số tiền để xem danh sách chứng từ.',
    'dct': 'Điều chỉnh làm TĂNG công nợ trong kỳ. • Điều chỉnh công nợ (tăng) = Phát sinh Nợ của phiếu kế toán (phiếu điều chỉnh công nợ). • Bấm vào số tiền để xem danh sách chứng từ.',
    'congt': 'Tổng phát sinh tăng trong kỳ. • Cộng phát sinh tăng = Hàng hóa/Dịch vụ + Điều chỉnh công nợ (tăng).',
    'giam': 'Các khoản làm GIẢM công nợ phải thu, ngày hạch toán từ "Từ ngày" đến "Đến ngày". • Gồm: Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ (ghi giảm). • "Trả lại tiền thừa" là cột riêng, không nằm trong nhóm này. • ' + P,
    'ntl': 'Giá trị hàng khách trả lại trong kỳ. • Nhập trả lại = Phát sinh Có − Phát sinh Nợ của phiếu nhập hàng (hàng bán bị trả lại). • Bấm vào số tiền để xem danh sách chứng từ.',
    'tt': 'Số tiền khách đã thanh toán trong kỳ. • Đã thanh toán = Phát sinh Có của phiếu thu, phiếu báo có và khai báo công nợ đầu kỳ. • Bấm vào số tiền để xem danh sách chứng từ.',
    'dcg': 'Điều chỉnh làm GIẢM công nợ trong kỳ. • Điều chỉnh công nợ (giảm) = Phát sinh Có của phiếu kế toán (phiếu điều chỉnh công nợ). • Bấm vào số tiền để xem danh sách chứng từ.',
    'congg': 'Tổng phát sinh giảm trong kỳ. • Cộng phát sinh giảm = Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ (giảm).',
    'tltt': 'Tiền chi trả lại cho khách (khách nộp thừa) trong kỳ. • Trả lại tiền thừa = Phát sinh Nợ của phiếu chi và phiếu ủy nhiệm chi. • Khoản này được CỘNG vào Số dư cuối kỳ (bù lại phần khách đã trả thừa). • Bấm vào số tiền để xem danh sách chứng từ.',
    'ck': 'Công nợ phải thu còn lại tại "Đến ngày". • Số dư cuối kỳ = Số dư đầu kỳ + Cộng phát sinh tăng − Cộng phát sinh giảm + Trả lại tiền thừa. • Số dương (dư nợ): khách còn nợ; số âm (dư có): khách trả thừa / trả trước. • Bộ lọc "Số dư cuối kỳ" (Dư nợ / Dư có) lọc theo số này.',
    'tong': 'Tổng trên toàn bộ công nợ theo bộ lọc. Lọc "Số dư cuối kỳ" (Dư nợ / Dư có) và ô tìm nhanh chỉ áp cho các dòng khách hàng, không áp cho dòng tổng (giống ERP). Số dư đầu kỳ tính cả chứng từ chưa gắn khách hàng.',
    'trang': 'Theo dõi công nợ phải thu của từng khách hàng, chi tiết đến từng hợp đồng: số dư đầu kỳ, phát sinh tăng / giảm trong kỳ và số dư cuối kỳ. Dữ liệu hiển thị theo quyền xem (tổng công ty / công ty / phòng ban / bộ phận); không có quyền nào thì chỉ thấy hợp đồng do mình tạo.',
}


def so(col, tip, cap):
    """Dòng bảng giao diện cho 1 cột số tiền bấm được."""
    return ['Cột %s' % col, 'Table/Grid', 'Read-only', '≥ 0 hoặc âm, VND', 'Theo dữ liệu', [
        '- Thuộc nhóm %s.' % cap if cap else '- Cột riêng.',
        '- Định dạng 1,234,567, không lẻ; số 0 để trống (dòng Tổng cộng in 0).',
        '- Dòng khách hàng và dòng hợp đồng: số khác 0 là liên kết, bấm → mở popup "Chi tiết chứng từ" (mục 2.3) đúng cột, đúng dòng đã bấm.',
        '- Icon ⓘ: "%s"' % TIP[tip]]]


# ---------------------------------------------------------------- 2.1 Xem báo cáo
FR = []
CACH_LAY = tbl(['STT', 'Chỉ tiêu / Cột', 'Cách lấy dữ liệu', 'Nội dung icon ⓘ'], [
    ('Tập dữ liệu / thời điểm số liệu', 'Chứng từ đã hạch toán vào sổ phải thu khách hàng (TK 131 và tài khoản con trực tiếp), số tiền quy đổi VND. Kỳ báo cáo theo NGÀY HẠCH TOÁN: trước "Từ ngày" là đầu kỳ; từ "Từ ngày" đến hết "Đến ngày" là phát sinh trong kỳ; sau "Đến ngày" không tính. Số liệu tính lại mỗi lần tải (không chốt sổ).', '—'),
    ('Dòng hợp đồng', 'Mỗi cặp (khách hàng, hợp đồng) có bút toán số tiền lớn hơn 0 với ngày hạch toán đến hết "Đến ngày" là 1 dòng — kể cả hợp đồng không phát sinh trong kỳ (các cột trong kỳ để trống). Chứng từ không gắn hợp đồng gom thành 1 dòng ô hợp đồng trống. Bút toán không gắn khách hàng không lên dòng.', TIP['hd']),
    ('Dòng khách hàng (in đậm)', 'Cộng TẤT CẢ dòng hợp đồng của khách hàng theo bộ lọc, kể cả dòng nằm ở trang khác. Khách hàng có hợp đồng vắt 2 trang thì 2 trang hiện cùng 1 tổng.', '(dùng chung ⓘ cột Đơn hàng/hợp đồng)'),
    ('Dòng Tổng cộng', 'Tính trên toàn bộ sổ theo phạm vi quyền + Thời gian + Khách hàng + Số hợp đồng + Công ty / Phòng ban / Bộ phận / Nhân viên. KHÔNG áp lọc "Số dư cuối kỳ" và ô tìm nhanh ⇒ khi đang dùng 2 bộ lọc này, dòng Tổng cộng có thể khác tổng các dòng khách hàng. Số dư đầu kỳ của dòng này tính cả chứng từ chưa gắn khách hàng; khi lọc Số hợp đồng thì đầu kỳ lấy mọi hợp đồng có số chứa chuỗi đã nhập (phát sinh lấy đúng số hợp đồng). Số 0 in "0".', TIP['tong']),
    ('Số dư đầu kỳ', 'Tổng phát sinh Nợ − tổng phát sinh Có của mọi chứng từ có ngày hạch toán trước "Từ ngày".', TIP['dk']),
    ('Phát sinh tăng – Hàng hóa/Dịch vụ', 'Trong kỳ: Nợ của phiếu xuất kho, phiếu xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ bảo hành - sửa chữa, khai báo công nợ đầu kỳ; TRỪ Có của các chứng từ đó (không trừ Có của khai báo công nợ đầu kỳ).', TIP['hh']),
    ('Phát sinh tăng – Điều chỉnh công nợ', 'Trong kỳ: Nợ của phiếu kế toán (phiếu điều chỉnh công nợ).', TIP['dct']),
    ('Phát sinh tăng – Cộng', 'Hàng hóa/Dịch vụ + Điều chỉnh công nợ (tăng), tính trên màn ở từng dòng.', TIP['congt']),
    ('Phát sinh giảm – Nhập trả lại', 'Trong kỳ: Có − Nợ của phiếu nhập hàng (hàng bán bị trả lại).', TIP['ntl']),
    ('Phát sinh giảm – Đã thanh toán', 'Trong kỳ: Có của phiếu thu, phiếu báo có, khai báo công nợ đầu kỳ.', TIP['tt']),
    ('Phát sinh giảm – Điều chỉnh công nợ', 'Trong kỳ: Có của phiếu kế toán (phiếu điều chỉnh công nợ).', TIP['dcg']),
    ('Phát sinh giảm – Cộng', 'Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ (giảm).', TIP['congg']),
    ('Trả lại tiền thừa', 'Trong kỳ: Nợ của phiếu chi và phiếu ủy nhiệm chi. Cột riêng, không nằm trong nhóm giảm; được CỘNG vào số dư cuối kỳ.', TIP['tltt']),
    ('Số dư cuối kỳ', 'Số dư đầu kỳ + Cộng phát sinh tăng − Cộng phát sinh giảm + Trả lại tiền thừa. Mọi dòng in cả số 0. Lọc Dư nợ: chỉ giữ dòng hợp đồng > 0; Dư có: < 0.', TIP['ck']),
    ('Ràng buộc khớp số', '– Dòng khách hàng = tổng các dòng hợp đồng của khách đó (mọi trang).\n– Khi không lọc Số dư cuối kỳ / ô tìm nhanh: dòng Tổng cộng (trừ cột Số dư đầu kỳ và Số dư cuối kỳ nếu có chứng từ chưa gắn khách hàng trước kỳ) = tổng mọi dòng khách hàng.\n– Ở mọi dòng: Cuối kỳ = Đầu kỳ + Cộng tăng − Cộng giảm + Trả lại tiền thừa.', '—'),
    ('Chân bảng', '"Hiển thị a–b / N dòng hợp đồng": N = số dòng hợp đồng khớp bộ lọc (dòng khách hàng không tính).', '—'),
])
POPUP_TBL = tbl(['STT', 'Bấm vào', 'Popup mở ra', 'Mục đích thiết kế', 'Dữ liệu hiển thị'], [
    ('Số ở cột Hàng hóa/Dịch vụ (dòng hợp đồng / dòng khách hàng); số 0 không bấm được', 'Chi tiết chứng từ (mục 2.3), bảng 2 cột Phát sinh nợ / Phát sinh có', 'Công nợ tăng do bán hàng hóa / dịch vụ đến từ những phiếu nào', 'Phiếu xuất kho, xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ BH-SC, khai báo công nợ đầu kỳ của dòng đã bấm, trong kỳ. Tổng phát sinh nợ − Tổng phát sinh có = số đã bấm (trừ khi có Có của khai báo công nợ đầu kỳ – BR-07)'),
    ('Số ở cột Điều chỉnh công nợ (tăng)', 'Chi tiết chứng từ (mục 2.3), cột Số tiền', 'Khoản điều chỉnh tăng nào đã ghi vào công nợ', 'Nợ của phiếu kế toán; popup có thêm khai báo đầu kỳ công nợ NCC và phiếu thu ghi Nợ (BR-07). Tổng số tiền = số đã bấm khi không có 2 loại thêm'),
    ('Số ở cột Nhập trả lại', 'Chi tiết chứng từ (mục 2.3), 2 cột Phát sinh nợ / Phát sinh có', 'Khách trả lại hàng bằng những phiếu nhập nào', 'Phiếu nhập hàng của dòng đã bấm; Tổng phát sinh có − Tổng phát sinh nợ = số đã bấm'),
    ('Số ở cột Đã thanh toán', 'Chi tiết chứng từ (mục 2.3), cột Số tiền', 'Khách đã trả tiền bằng phiếu thu / báo có nào', 'Có của phiếu thu, phiếu báo có, khai báo công nợ đầu kỳ; Tổng số tiền = số đã bấm'),
    ('Số ở cột Điều chỉnh công nợ (giảm); dòng hợp đồng in cả số 0 và bấm được', 'Chi tiết chứng từ (mục 2.3), cột Số tiền', 'Khoản điều chỉnh giảm nào đã trừ vào công nợ', 'Có của phiếu kế toán; popup có thêm phiếu thu ghi Có (BR-07). Bấm số 0 → popup "Không có dữ liệu phù hợp."'),
    ('Số ở cột Trả lại tiền thừa', 'Chi tiết chứng từ (mục 2.3), cột Số tiền', 'Đã chi trả lại khách bằng phiếu chi / ủy nhiệm chi nào', 'Nợ của phiếu chi, phiếu ủy nhiệm chi; Tổng số tiền = số đã bấm'),
    ('Số hợp đồng ở cột Đơn hàng/hợp đồng', 'Không phải popup — mở hợp đồng ở tab mới (màn HRM nếu đã có, chưa có thì mở hệ thống cũ)', 'Xem hợp đồng gốc của dòng công nợ', '—'),
    ('Cột Số dư đầu kỳ, các cột Cộng, Số dư cuối kỳ, dòng Tổng cộng', 'Không bấm được', '—', '—'),
])
FR.append({
    'ten': 'Xem báo cáo chi tiết công nợ khách hàng',
    'qtc': 'Màn Báo cáo, Định dạng số, Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem báo cáo chi tiết công nợ khách hàng'],
        ['Mô tả', 'Hiển thị công nợ phải thu theo khách hàng, chi tiết đến từng hợp đồng: số dư đầu kỳ, phát sinh tăng / giảm trong kỳ, trả lại tiền thừa, số dư cuối kỳ; dòng Tổng cộng trên cùng. Màn chỉ đọc.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống hiện bộ lọc trống, bảng báo "Chọn thời gian để xem báo cáo."\n3. Người dùng chọn Thời gian (Từ ngày → Đến ngày).\n4. Hệ thống tải báo cáo theo phạm vi quyền (BR-01): dòng Tổng cộng, rồi từng khách hàng (in đậm) và các hợp đồng của khách, 10 dòng hợp đồng/trang.\n5. Người dùng đọc số, bấm số tiền để xem chứng từ (mục 2.3) hoặc bấm số hợp đồng để mở hợp đồng ở tab mới.'],
        ['Dòng sự kiện phụ', '• Không có dòng khớp → "Không có dữ liệu phù hợp bộ lọc."\n• Đang tải → dòng "Đang tải dữ liệu..."; đổi bộ lọc liên tiếp thì chỉ hiện kết quả của lần lọc mới nhất.\n• Lỗi tải → thông báo lỗi của hệ thống hoặc "Lỗi khi tải dữ liệu".\n• Hợp đồng không mở được (loại lạ / đã xóa) → số hợp đồng hiện chữ thường, không bấm được.'],
    ],
    'anh': [('01_open', 'Màn báo cáo lúc mới mở — chưa chọn Thời gian'),
            ('03_list', 'Báo cáo tháng 10/2026, chưa lọc khách hàng'),
            ('04_customer', 'Báo cáo lọc 1 khách hàng — dòng Tổng cộng, dòng khách hàng, các dòng hợp đồng'),
            ('05b_table_right', 'Phần bên phải bảng — nhóm Phát sinh giảm, Trả lại tiền thừa, Số dư cuối kỳ'),
            ('06_tip', 'Icon ⓘ ở đầu cột Số dư cuối kỳ')],
    'ui': ui(UI7, [
        ['Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Hiển thị', ['- "Báo cáo chi tiết công nợ khách hàng" trên thanh đầu trang và đầu bảng.', '- Icon ⓘ: "%s"' % TIP['trang']]],
        ['Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', ['- Mở cửa sổ "Chọn trường xuất Excel" (mục 2.4).', '- Bị khóa trong lúc đang xuất.']],
        ['Bảng chi tiết báo cáo', 'Table/Grid', 'Read-only', '–', 'Trống', ['- Tiêu đề 2 tầng, dính trên cùng khi cuộn; thanh cuộn ngang ở cả trên và dưới bảng.', '- Các cột (mỗi cột 1 dòng bên dưới): STT, Đơn hàng/hợp đồng, Phòng ban, Bộ phận, NVKD, Số dư đầu kỳ, Phát sinh tăng trong kỳ (Hàng hóa/Dịch vụ, Điều chỉnh công nợ, Cộng), Phát sinh giảm trong kỳ (Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ, Cộng), Trả lại tiền thừa, Số dư cuối kỳ.', '- Thứ tự dòng: Tổng cộng → khách hàng (in đậm, theo thứ tự khách hàng) → các hợp đồng của khách.', '- Chưa chọn Thời gian: "Chọn thời gian để xem báo cáo."', '- Không có dữ liệu: "Không có dữ liệu phù hợp bộ lọc."', '- Không sắp xếp theo cột, không ẩn / hiện cột.']],
        ['Dòng Tổng cộng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Nền xám, chữ đậm, chỉ hiện khi có dữ liệu.', '- Số 0 in "0".', '- Không bấm được.', '- Icon ⓘ: "%s"' % TIP['tong']]],
        ['Dòng khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Chữ đậm, "Mã KH - Tên KH" gộp qua 4 cột Đơn hàng/hợp đồng…NVKD; không có mã / tên thì "Khách hàng #<số>".', '- Số = cộng mọi hợp đồng của khách (BR-03).', '- Số 0 để trống, riêng Số dư cuối kỳ in "0".']],
        ['Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Dòng khách hàng 1, 2, 3…; dòng hợp đồng 1.1, 1.2…', '- Nối tiếp khi sang trang.', '- Icon ⓘ: "%s"' % TIP['stt']]],
        ['Cột Đơn hàng/hợp đồng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Số hợp đồng dạng liên kết, bấm → mở hợp đồng ở tab mới.', '- Chứng từ không gắn hợp đồng: ô trống.', '- Icon ⓘ: "%s"' % TIP['hd']]],
        ['Cột Phòng ban', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Mã phòng ban của người tạo hợp đồng (hồ sơ hiện tại).', '- Icon ⓘ: "%s"' % TIP['pb']]],
        ['Cột Bộ phận', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Tên bộ phận của người tạo hợp đồng; không có thì trống.', '- Icon ⓘ: "%s"' % TIP['bp']]],
        ['Cột NVKD', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Họ tên người tạo hợp đồng.', '- Icon ⓘ: "%s"' % TIP['nv']]],
        ['Cột Số dư đầu kỳ', 'Table/Grid', 'Read-only', 'Số, có thể âm', 'Theo dữ liệu', ['- Định dạng 1,234,567; số 0 để trống (dòng Tổng cộng in 0).', '- Không bấm được.', '- Icon ⓘ: "%s"' % TIP['dk']]],
        ['Tiêu đề nhóm Phát sinh tăng trong kỳ', 'Label', 'Hiển thị', '–', 'Hiển thị', ['- Gộp 3 cột Hàng hóa/Dịch vụ, Điều chỉnh công nợ, Cộng.', '- Icon ⓘ: "%s"' % TIP['tang']]],
        so('Hàng hóa/Dịch vụ', 'hh', 'Phát sinh tăng'),
        so('Điều chỉnh công nợ (tăng)', 'dct', 'Phát sinh tăng'),
        ['Cột Cộng (phát sinh tăng)', 'Table/Grid', 'Read-only', 'Số', 'Theo dữ liệu', ['- = Hàng hóa/Dịch vụ + Điều chỉnh công nợ (tăng) của chính dòng đó.', '- Không bấm được.', '- Icon ⓘ: "%s"' % TIP['congt']]],
        ['Tiêu đề nhóm Phát sinh giảm trong kỳ', 'Label', 'Hiển thị', '–', 'Hiển thị', ['- Gộp 4 cột Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ, Cộng.', '- Icon ⓘ: "%s"' % TIP['giam']]],
        so('Nhập trả lại', 'ntl', 'Phát sinh giảm'),
        so('Đã thanh toán', 'tt', 'Phát sinh giảm'),
        ['Cột Điều chỉnh công nợ (giảm)', 'Table/Grid', 'Read-only', 'Số', 'Theo dữ liệu', ['- Thuộc nhóm Phát sinh giảm.', '- Dòng hợp đồng in cả số 0 và vẫn là liên kết; dòng khách hàng số 0 để trống.', '- Bấm số → mở popup "Chi tiết chứng từ" (mục 2.3).', '- Icon ⓘ: "%s"' % TIP['dcg']]],
        ['Cột Cộng (phát sinh giảm)', 'Table/Grid', 'Read-only', 'Số', 'Theo dữ liệu', ['- = Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ (giảm).', '- Không bấm được.', '- Icon ⓘ: "%s"' % TIP['congg']]],
        so('Trả lại tiền thừa', 'tltt', None),
        ['Cột Số dư cuối kỳ', 'Table/Grid', 'Read-only', 'Số, có thể âm', 'Theo dữ liệu', ['- Mọi dòng in cả số 0.', '- Số âm = khách trả thừa (dư có).', '- Không bấm được.', '- Icon ⓘ: "%s"' % TIP['ck']]],
        ['Chân bảng', 'Label', 'Hiển thị', '–', 'Ẩn khi không có dữ liệu', ['- "Hiển thị a–b / N dòng hợp đồng".']],
        ['Ô Số dòng/trang', 'Dropdown', 'Enable', '10 / 20 / 50 / 100', '10', ['- Đổi số dòng hợp đồng mỗi trang, quay về trang 1.']],
        ['Phân trang', 'Button', 'Enable', '–', 'Trang 1', ['- Chuyển trang; dòng Tổng cộng giữ nguyên, không tính lại.']],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Không kiểm quyền vào màn; đọc cấp phạm vi của người dùng (BR-01) để quyết ô lọc Công ty / Phòng ban / Bộ phận / Nhân viên.\nAfter:\n– Thời gian trống → bảng "Chọn thời gian để xem báo cáo.", không tải số.\n– Quay lại từ màn khác trong 10 phút: giữ bộ lọc cũ và tải lại; tải lại trang (F5) thì xoá bộ lọc như bấm Làm mới.'],
        ['Chọn đủ Thời gian / đổi bộ lọc', 'Change', 'During:\n– Từ ngày > Đến ngày → báo đỏ dưới ô + toast "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", xoá bảng, không tải (BR-08).\n' + LOI + '\nAfter:\n– Tải trang 1 kèm dòng Tổng cộng.'],
        ['Chuyển trang / đổi số dòng mỗi trang', 'Click', 'After:\n– Tải lại các dòng, giữ bộ lọc; dòng Tổng cộng không tính lại.'],
        ['Bấm số tiền (dòng khách hàng / hợp đồng)', 'Click', 'After:\n– Mở popup "Chi tiết chứng từ" của đúng cột + dòng (mục 2.3), kèm toàn bộ bộ lọc đang áp.'],
        ['Bấm số hợp đồng', 'Click', 'After:\n– Mở hợp đồng ở tab mới.'],
        ['Rê chuột vào icon ⓘ', 'Hover', 'After:\n– Hiện chú thích của cột / dòng (nội dung ở bảng mục 2.1.5).'],
    ],
    'extra': [
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', 'table', (CACH_LAY, [0.5, 1.2, 2.9, 2.1],
         'Bảng dưới mô tả cách hệ thống tính từng chỉ tiêu, từng cột và nội dung icon ⓘ (nguyên văn trên giao diện). "Tập dữ liệu" là các bút toán sổ phải thu khách hàng sau khi áp phạm vi quyền (BR-01) và bộ lọc.')),
        ('Danh sách popup mở từ số liệu', 'table', (POPUP_TBL, [0.5, 1.35, 1.3, 1.4, 2.0], None)),
    ],
})

# ---------------------------------------------------------------- 2.2 Tìm kiếm & lọc
FR.append({
    'ten': 'Tìm kiếm và lọc báo cáo',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc báo cáo chi tiết công nợ khách hàng'],
        ['Mô tả', 'Thu hẹp báo cáo bằng ô tìm nhanh và các ô lọc: Thời gian (bắt buộc), Khách hàng, Số hợp đồng, Số dư cuối kỳ, Công ty / Phòng ban / Bộ phận / Nhân viên (theo cấp quyền).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn báo cáo.'],
        ['Dòng sự kiện chính', '1. Người dùng chọn Thời gian và các ô lọc cần thiết (ô chọn lọc ngay khi chọn), hoặc gõ ô tìm nhanh / Số hợp đồng rồi bấm Tìm kiếm hoặc Enter.\n2. Hệ thống áp đồng thời mọi điều kiện, tải lại báo cáo từ trang 1.'],
        ['Dòng sự kiện phụ', '• Bấm Tìm kiếm khi chưa chọn Thời gian → chữ đỏ "Vui lòng chọn thời gian" dưới ô, không tải.\n• Từ ngày > Đến ngày → "Đến ngày phải lớn hơn hoặc bằng Từ ngày." (BR-08).\n• Bấm Làm mới → xoá mọi ô (kể cả Thời gian), bảng về "Chọn thời gian để xem báo cáo.".\n• Bấm Ẩn tìm kiếm nâng cao → thu gọn các ô lọc; Cài đặt bộ lọc → chọn ô lọc nào hiện và thứ tự.'],
    ],
    'anh': [('02_required', 'Bấm Tìm kiếm khi chưa chọn Thời gian'), ('10_balance_open', 'Ô Số dư cuối kỳ: Tất cả / Dư nợ / Dư có'),
            ('12_filter_settings', 'Cửa sổ Cài đặt bộ lọc')],
    'ui': ui(UI8, [
        ['Ô tìm nhanh', 'Textbox', 'Enable', 'Chuỗi ký tự', 'Không', 'Trống', ['- Placeholder "Tìm theo số hợp đồng, mã hoặc tên khách hàng".', '- Tìm gần đúng theo số hợp đồng, mã hoặc tên khách hàng; lọc khi bấm Tìm kiếm / Enter.', '- Chỉ áp cho dòng khách hàng / hợp đồng, không áp cho dòng Tổng cộng (BR-04).']],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', '–', ['- Áp từ khoá và các ô lọc; thiếu Thời gian thì báo đỏ.']],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', '–', ['- Xoá mọi điều kiện (kể cả Thời gian), xoá bộ lọc đã ghi nhớ.']],
        ['Nút Ẩn tìm kiếm nâng cao / Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Đang mở', ['- Thu gọn / mở khu vực các ô lọc.']],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', '–', ['- Mở cửa sổ "Cài đặt bộ lọc": tích ô lọc muốn hiện, kéo sắp thứ tự; nút Lưu, Khôi phục mặc định, Đóng (quy tắc chung).']],
        ['Ô Thời gian', 'Datepicker', 'Enable', 'dd/mm/yyyy, 2 ô Từ ngày → Đến ngày', 'Có', 'Trống', ['- Lọc theo ngày hạch toán của chứng từ (BR-02).', '- Mặc định trống, người dùng tự chọn.', '- Lịch ô Từ không cho chọn sau ngày Đến và ngược lại.', '- Thiếu: "Vui lòng chọn thời gian".', '- Từ > Đến: "Đến ngày phải lớn hơn hoặc bằng Từ ngày."']],
        ['Ô Khách hàng', 'Dropdown', 'Enable', 'Danh sách khách hàng, chọn 1', 'Không', 'Trống', ['- Gõ tối thiểu 2 ký tự mã hoặc tên để tìm; có nút × xoá.', '- Hiển thị "Mã - Tên khách hàng".']],
        ['Ô Số hợp đồng', 'Textbox', 'Enable', 'Chuỗi ký tự', 'Không', 'Trống', ['- Phải nhập ĐÚNG ĐỦ số hợp đồng (khớp chính xác); lọc khi Enter / Tìm kiếm.', '- Số dư đầu kỳ của dòng Tổng cộng lấy theo số hợp đồng CHỨA chuỗi đã nhập (BR-04).']],
        ['Ô Số dư cuối kỳ', 'Dropdown', 'Enable', 'Tất cả / Dư nợ / Dư có', 'Không', 'Trống (= Tất cả)', ['- Mặc định: trống, tính như Tất cả.', '- Dư nợ: giữ dòng hợp đồng có Số dư cuối kỳ > 0.', '- Dư có: giữ dòng hợp đồng có Số dư cuối kỳ < 0.', '- Không áp cho dòng Tổng cộng.']],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty, chọn nhiều', 'Không', 'Trống', ['- Chỉ hiện với quyền "…theo tổng công ty".', '- Icon khoá cạnh nhãn: bấm để hiện cả công ty đã khoá ("Hiện cả công ty đã khoá").']],
        ['Ô Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban, chọn nhiều', 'Không', 'Trống', ['- Hiện với quyền tổng công ty / công ty / phòng ban.', '- Lọc theo phòng ban ghi trên chứng từ.', '- Icon khoá: hiện cả phòng ban đã khoá.']],
        ['Ô Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách bộ phận, chọn nhiều', 'Không', 'Trống', ['- Hiện khi có 1 trong 4 quyền.', '- Lọc theo bộ phận ghi trên chứng từ.', '- Icon khoá: hiện cả bộ phận đã khoá.']],
        ['Ô Nhân viên', 'Dropdown', 'Enable / Ẩn', 'Danh sách nhân viên, chọn nhiều', 'Không', 'Trống', ['- Hiện khi có 1 trong 4 quyền.', '- Lọc theo NGƯỜI TẠO HỢP ĐỒNG.', '- Không có quyền nào: cả 4 ô Công ty / Phòng ban / Bộ phận / Nhân viên ẩn.']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Tìm kiếm / Enter ở ô gõ', 'Click', 'During:\n– Thời gian trống → chữ đỏ "Vui lòng chọn thời gian".\n– Từ > Đến → toast "Đến ngày phải lớn hơn hoặc bằng Từ ngày.".\n' + LOI + '\nAfter:\n– Ghi nhớ bộ lọc, tải lại từ trang 1.'],
        ['Chọn giá trị ở ô chọn (Thời gian, Khách hàng, Số dư cuối kỳ, Công ty…Nhân viên)', 'Change', 'After:\n– Tải lại ngay từ trang 1 (không cần bấm Tìm kiếm).'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi ô, bảng về "Chọn thời gian để xem báo cáo.".'],
        ['Bấm Cài đặt bộ lọc → Lưu', 'Click', 'After:\n– Ẩn / hiện, đổi thứ tự ô lọc, lưu theo người dùng và màn hình.'],
    ],
})

# ---------------------------------------------------------------- 2.3 Popup chi tiết chứng từ
BIEN_THE = tbl(['STT', 'Con số / vị trí bấm', 'Tập dòng hiển thị', 'Tiêu đề popup', 'Ô lọc ẩn / cố định'], [
    ('Ô số của dòng hợp đồng', 'Chứng từ của đúng khách hàng + hợp đồng đó', '"Chi tiết chứng từ" + dòng phụ "<Tên cột> — <Số hợp đồng>"', 'Cố định khách hàng, hợp đồng, cột; giữ Thời gian, Số hợp đồng, Công ty…Nhân viên của báo cáo'),
    ('Ô số của dòng không gắn hợp đồng', 'Chứng từ của khách hàng KHÔNG gắn hợp đồng', '"… — Không gắn hợp đồng"', 'Như trên, điều kiện hợp đồng = trống'),
    ('Ô số của dòng khách hàng', 'Chứng từ của mọi hợp đồng của khách', '"… — <Mã KH> - <Tên KH>"', 'Cố định khách hàng, cột; KHÔNG áp Số dư cuối kỳ và ô tìm nhanh (BR-07)'),
    ('Cột Hàng hóa/Dịch vụ, Nhập trả lại', 'Mỗi chứng từ 1 dòng, cộng cả Nợ và Có', 'Như trên; bảng có 2 cột Phát sinh nợ / Phát sinh có', 'Chân: "Tổng phát sinh nợ: … · Tổng phát sinh có: …"'),
    ('Cột Điều chỉnh công nợ (tăng / giảm), Đã thanh toán, Trả lại tiền thừa', 'Mỗi chứng từ 1 dòng, 1 bên Nợ hoặc Có', 'Như trên; bảng có cột Số tiền', 'Chân: "Tổng số tiền: …"'),
])
CACH_LAY_POPUP = tbl(['STT', 'Chỉ tiêu / Cột', 'Cách lấy dữ liệu', 'Nội dung icon ⓘ'], [
    ('Tập dòng', 'Bút toán số tiền > 0 vào sổ phải thu khách hàng, ngày hạch toán từ "Từ ngày" đến hết "Đến ngày", đúng loại chứng từ của cột (bảng mục 2.1.6), đúng khách hàng / hợp đồng đã bấm, áp phạm vi quyền + bộ lọc Công ty…Nhân viên, Số hợp đồng. Gom theo chứng từ, xếp theo loại chứng từ rồi theo thứ tự lập.', '—'),
    ('Cột Mã phiếu', 'Mã chứng từ; bấm → mở chứng từ ở tab mới (phiếu thu, phiếu chi, báo có, ủy nhiệm chi, phiếu kế toán, phiếu xuất hàng, phiếu nhập hàng, xuất bán hàng mượn, khai báo đầu kỳ mở màn HRM; hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ BH-SC mở hệ thống cũ).', '—'),
    ('Cột Phát sinh nợ / Phát sinh có', 'Tổng Nợ / Có của chứng từ trong sổ phải thu (chỉ ở cột Hàng hóa/Dịch vụ, Nhập trả lại).', '—'),
    ('Cột Số tiền', 'Tổng số tiền của chứng từ ở bên tương ứng của cột.', '—'),
    ('Cột Ngày tạo / Người tạo', 'Thời điểm lập chứng từ (dd/mm/yyyy hh:mm) và họ tên người lập.', '—'),
    ('Dòng tổng ở chân popup', 'Cộng trên TOÀN BỘ chứng từ của popup (mọi trang), không chỉ trang đang xem.', '—'),
])
FR.append({
    'ten': 'Xem chi tiết chứng từ của số liệu', 'uc': 'uc_xemct',
    'qtc': 'Màn Xem chi tiết, Phân trang.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết chứng từ của số liệu'],
        ['Mô tả', 'Popup "Chi tiết chứng từ" liệt kê các chứng từ tạo nên con số đã bấm trên báo cáo, kèm tổng để đối chiếu.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Báo cáo đang hiện số; ô bấm có số khác 0 (riêng Điều chỉnh công nợ giảm ở dòng hợp đồng bấm được cả số 0).'],
        ['Dòng sự kiện chính', '1. Người dùng bấm số tiền ở dòng khách hàng hoặc dòng hợp đồng.\n2. Hệ thống mở popup, tải chứng từ theo cột + dòng + bộ lọc đang áp, 10 dòng/trang.\n3. Người dùng xem, bấm Mã phiếu để mở chứng từ ở tab mới, chuyển trang nếu cần.\n4. Bấm Đóng / (x) để về báo cáo.'],
        ['Dòng sự kiện phụ', '• Không có chứng từ → "Không có dữ liệu phù hợp."\n• Lỗi tải → "Lỗi khi tải dữ liệu".\n• Mỗi lần mở là 1 popup mới, về trang 1.'],
    ],
    'menu_them': ' => Bấm số tiền trên bảng',
    'ghi_chu_layout': POPUP % 'Chi tiết chứng từ',
    'anh': [('07_popup_hanghoa', 'Popup bấm từ cột Hàng hóa/Dịch vụ của 1 hợp đồng (2 cột Phát sinh nợ / có)'),
            ('08_popup_dccn_tang', 'Popup bấm từ cột Điều chỉnh công nợ (tăng) — cột Số tiền'),
            ('09_popup_khachhang', 'Popup bấm từ dòng khách hàng — chứng từ của mọi hợp đồng')],
    'ui': ui(UI7, [
        ['Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Hiển thị', ['- "Chi tiết chứng từ".', '- Dòng phụ "<Phát sinh tăng / giảm - Tên cột> — <Số hợp đồng | Mã KH - Tên KH | Không gắn hợp đồng>".']],
        ['Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Liên tục qua các trang.']],
        ['Cột Mã phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Liên kết, bấm → mở chứng từ ở tab mới.', '- Loại chứng từ chưa có đường mở: chữ thường.']],
        ['Cột Phát sinh nợ', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', ['- Chỉ có khi bấm từ cột Hàng hóa/Dịch vụ hoặc Nhập trả lại.', '- Số 0 để trống.']],
        ['Cột Phát sinh có', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', ['- Như cột Phát sinh nợ.']],
        ['Cột Số tiền', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', ['- Có ở các cột còn lại (Điều chỉnh công nợ, Đã thanh toán, Trả lại tiền thừa).']],
        ['Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', ['- Ngày lập chứng từ (khác ngày hạch toán dùng để xếp kỳ).']],
        ['Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Họ tên người lập chứng từ.']],
        ['Phân trang', 'Button', 'Enable', '5 / 10 / 20 / 50 / 100', '10', ['- "Hiển thị a–b / N"; chọn số dòng/trang.']],
        ['Dòng tổng', 'Label', 'Hiển thị', '–', 'Ẩn khi không có dữ liệu', ['- "Tổng phát sinh nợ: … · Tổng phát sinh có: …" hoặc "Tổng số tiền: …".', '- Cộng mọi trang.']],
        ['Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', ['- Đóng popup, giữ nguyên báo cáo, bộ lọc, trang đang xem.']],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Bấm số tiền trên báo cáo', 'Click', 'After:\n– Mở popup, tải trang 1 chứng từ + dòng tổng.'],
        ['Bấm Mã phiếu', 'Click', 'After:\n– Mở chứng từ ở tab mới.'],
        ['Chuyển trang / đổi số dòng', 'Click', 'After:\n– Tải lại danh sách; dòng tổng không đổi.'],
        ['Bấm Đóng / (x)', 'Click', 'After:\n– Đóng popup.'],
    ],
    'extra': [
        ('Mục đích thiết kế popup', 'bullets', [
            'Trả lời câu hỏi "con số này gồm những chứng từ nào, lập ngày nào, ai lập" để kế toán / kinh doanh đối chiếu với khách.',
            'Là popup để giữ nguyên ngữ cảnh báo cáo (bộ lọc, trang đang xem, vị trí cuộn) — báo cáo tải chậm, chuyển màn rồi quay lại phải tải lại.',
            'Khớp số: cùng phạm vi quyền và bộ lọc của báo cáo; dòng tổng của popup = số đã bấm (Nợ − Có với cột Hàng hóa/Dịch vụ, Có − Nợ với cột Nhập trả lại), trừ các trường hợp ghi ở BR-07.',
            'Từ popup người dùng mở chứng từ gốc ở tab mới; mỗi lần mở popup là trạng thái mới (trang 1).',
        ]),
        ('Các biến thể theo con số bấm', 'table', (BIEN_THE, [0.5, 1.35, 1.6, 1.5, 1.8], None)),
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', 'table', (CACH_LAY_POPUP, [0.5, 1.25, 3.6, 1.0], None)),
    ],
})

# ---------------------------------------------------------------- 2.4 Xuất Excel
FR.append({
    'ten': 'Xuất báo cáo ra Excel', 'uc': 'uc_xuat',
    'qtc': 'Quy tắc Excel.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất báo cáo chi tiết công nợ khách hàng ra Excel'],
        ['Mô tả', 'Xuất TOÀN BỘ dòng khớp bộ lọc (mọi trang) ra file Excel theo bố cục màn hình; người dùng chọn trường và thứ tự cột (BR-06).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đã chọn Thời gian hợp lệ.'],
        ['Dòng sự kiện chính', '1. Người dùng lọc báo cáo, bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất Excel", tích sẵn đủ 14 trường.\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự, bấm Xuất file.\n4. Hệ thống tải file bao_cao_chi_tiet_cong_no_khach_hang.xlsx, đóng cửa sổ, báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Chưa chọn Thời gian → "Vui lòng chọn thời gian", không mở cửa sổ.\n• Từ > Đến → "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", không mở cửa sổ.\n• Bỏ chọn hết trường → nút Xuất file không bấm được.\n• Lỗi → câu lỗi của hệ thống hoặc "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': POPUP % 'Chọn trường xuất Excel',
    'anh': [('11_export', 'Cửa sổ Chọn trường xuất Excel')],
    'ui': ui(UI8, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', ['- "Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file."']],
        ['Danh sách trường', 'Table/Grid', 'Enable', '14 trường', 'Ít nhất 1', 'Tích tất cả', ['- Khách hàng / Đơn hàng - hợp đồng, Phòng ban, Bộ phận, NVKD, Số dư đầu kỳ, PS tăng - Hàng hóa/Dịch vụ, PS tăng - Điều chỉnh công nợ, PS tăng - Cộng, PS giảm - Nhập trả lại, PS giảm - Đã thanh toán, PS giảm - Điều chỉnh công nợ, PS giảm - Cộng, Trả lại tiền thừa, Số dư cuối kỳ.', '- Mỗi trường có ô tích và biểu tượng ☰ kéo đổi vị trí.']],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', ['- Tích / bỏ tích mọi trường.']],
        ['Dòng đếm', 'Label', 'Hiển thị', '–', '–', 'Đang chọn 14/14 trường', ['- "Đang chọn x/14 trường".']],
        ['Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Enable', ['- Tải file; khóa khi không còn trường nào hoặc đang xuất.']],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', '–', ['- Đóng cửa sổ, không xuất.']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'Before:\n– Thiếu Thời gian → "Vui lòng chọn thời gian"; Từ > Đến → "Đến ngày phải lớn hơn hoặc bằng Từ ngày.".\nAfter:\n– Mở cửa sổ chọn trường.'],
        ['Bấm Xuất file', 'Click', 'During:\n– Lấy mọi dòng khớp bộ lọc (kể cả ô tìm nhanh, Số dư cuối kỳ) + dòng Tổng cộng.\n' + LOI + '\nAfter:\n– Tải file: dòng 1 "BÁO CÁO CHI TIẾT CÔNG NỢ KHÁCH HÀNG", dòng 2 "Thời gian: dd/mm/yyyy - dd/mm/yyyy" (in đậm), tiêu đề 2 tầng như màn, cột STT luôn có + các trường đã chọn theo thứ tự; dòng Tổng cộng → khách hàng (đậm) → hợp đồng; cột số dạng số 1,234,567; số 0 để trống trừ dòng Tổng cộng, cột Số dư cuối kỳ và cột Điều chỉnh công nợ (giảm) ở dòng hợp đồng in 0.\n– Đóng cửa sổ, báo "Xuất Excel thành công".'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# ---------------------------------------------------------------- Phần 5
P5 = [
    ('Bán hàng – dùng chung cách tính và phạm vi', 'Bảng đối chiếu công nợ 1 khách hàng', 'Bán hàng => Báo cáo => Báo cáo công nợ => Đối chiếu công nợ 1 KH'),
    ('Bán hàng – dùng chung cách tính và phạm vi', 'Báo cáo tổng hợp công nợ khách hàng theo nhân viên', 'Bán hàng => Báo cáo => Báo cáo công nợ => Tổng hợp công nợ theo NV'),
    ('Tài chính – dùng chung cách tính công nợ', 'Báo cáo hạn mức công nợ khách hàng (cột Số dư nợ)', 'Tài chính => Kế toán công nợ => Khách hàng => Báo cáo hạn mức công nợ khách hàng'),
    ('Tài chính – dùng chung cách tính công nợ', 'Báo cáo hạn mức công nợ nhân viên', 'Tài chính => Kế toán công nợ => Nhân viên => Báo cáo hạn mức công nợ nhân viên'),
    ('Tài chính – dùng chung cách tính công nợ', 'Khai báo hạn mức công nợ KH', 'Tài chính => Kế toán công nợ => Khách hàng => Khai báo hạn mức công nợ KH'),
    ('Chứng từ nguồn (mở từ popup)', 'Phiếu xuất hàng', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng => Phiếu xuất hàng'),
    ('Chứng từ nguồn (mở từ popup)', 'Phiếu xuất bán hàng mượn', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng => Phiếu xuất bán hàng mượn'),
    ('Chứng từ nguồn (mở từ popup)', 'Phiếu nhập hàng', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng => Phiếu nhập hàng'),
    ('Chứng từ nguồn (mở từ popup)', 'Phiếu thu', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt => Phiếu thu'),
    ('Chứng từ nguồn (mở từ popup)', 'Phiếu chi', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt => Phiếu chi'),
    ('Chứng từ nguồn (mở từ popup)', 'Phiếu báo có', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt => Phiếu báo có'),
    ('Chứng từ nguồn (mở từ popup)', 'Phiếu ủy nhiệm chi', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt => Phiếu ủy nhiệm chi'),
    ('Chứng từ nguồn (mở từ popup)', 'Phiếu kế toán (điều chỉnh công nợ)', 'Tài chính => Sổ tổng hợp => Phiếu kế toán'),
    ('Chứng từ nguồn (mở từ popup)', 'Khai báo đầu kỳ công nợ', 'Tài chính => Khai báo đầu kỳ => Khai báo đầu kỳ công nợ'),
    ('Chứng từ nguồn (mở từ popup)', 'Khai báo đầu kỳ công nợ nhà cung cấp', 'Tài chính => Khai báo đầu kỳ => Khai báo đầu kỳ công nợ nhà cung cấp'),
]

S = {
    'ten': TEN,
    'menu': [('Bán hàng', 'menu_phanhe'), ('Báo cáo', 'menu_nhom'), ('Báo cáo công nợ', 'menu_nhomcon'), ('Chi tiết công nợ KH', 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu màn %s (tiêu đề trên màn: "%s").' % (TEN, TEN_MAN),
        'Giải thích từng cột số: lấy từ chứng từ nào, bên Nợ hay Có, kỳ tính theo ngày nào, dòng khách hàng / dòng Tổng cộng cộng ra sao.',
        'Làm rõ phạm vi số liệu theo 4 cấp quyền và các điểm số liệu có chủ đích không khớp nhau (dòng Tổng cộng, popup).',
    ],
    'thuat_ngu': [
        ['Công nợ phải thu', 'Số tiền khách hàng còn phải trả, theo dõi trên sổ tài khoản 131 (và các tài khoản con).'],
        ['Ngày hạch toán', 'Ngày chứng từ được ghi sổ; dùng để xếp chứng từ vào đầu kỳ / trong kỳ.'],
        ['Phát sinh Nợ / Có', 'Bút toán ghi tăng (Nợ) / ghi giảm (Có) công nợ phải thu.'],
        ['Dư nợ / Dư có', 'Số dư cuối kỳ dương (khách còn nợ) / âm (khách trả thừa, trả trước).'],
        ['NVKD', 'Nhân viên kinh doanh — trên báo cáo là người tạo hợp đồng.'],
        ['Dòng khách hàng', 'Dòng in đậm, cộng số của mọi hợp đồng của khách.'],
        ['Dòng hợp đồng', 'Dòng chi tiết của 1 hợp đồng (hoặc nhóm chứng từ không gắn hợp đồng) của khách.'],
        ['Phiếu kế toán', 'Chứng từ điều chỉnh công nợ, lập từ phiếu yêu cầu điều chỉnh công nợ.'],
    ],
    'quyen_truoc': ['Màn KHÔNG chặn quyền vào: mọi người dùng đăng nhập đều mở được. 4 quyền dưới đây (nhóm "Báo cáo chi tiết công nợ khách hàng") chỉ quyết PHẠM VI số liệu và ô lọc đơn vị. Người có nhiều quyền lấy cấp rộng nhất.'],
    'quyen_rows': [
        ['Xem báo cáo chi tiết công nợ khách hàng theo tổng công ty', 'Thấy mọi số liệu; có ô Công ty, Phòng ban, Bộ phận, Nhân viên.'],
        ['Xem báo cáo chi tiết công nợ khách hàng theo công ty', 'Thấy chứng từ của công ty đang làm việc + hợp đồng do mình tạo; có ô Phòng ban, Bộ phận, Nhân viên.'],
        ['Xem báo cáo chi tiết công nợ khách hàng theo phòng ban', 'Thấy chứng từ của các phòng mình quản lý + hợp đồng do mình tạo; có ô Phòng ban, Bộ phận, Nhân viên.'],
        ['Xem báo cáo chi tiết công nợ khách hàng theo bộ phận', 'Thấy chứng từ của các bộ phận mình quản lý + hợp đồng do mình tạo; có ô Bộ phận, Nhân viên.'],
        ['(Không có quyền nào)', 'Chỉ thấy hợp đồng do mình tạo; không có ô Công ty / Phòng ban / Bộ phận / Nhân viên.'],
    ],
    'ma_tran': [['Chức năng', 'Tổng công ty', 'Công ty', 'Phòng ban', 'Bộ phận', 'Không quyền']] + [
        [f, 'Có', 'Có', 'Có', 'Có', 'Có'] for f in [
            'FR-01 Xem báo cáo chi tiết công nợ khách hàng', 'FR-02 Tìm kiếm và lọc báo cáo',
            'FR-03 Xem chi tiết chứng từ của số liệu', 'FR-04 Xuất báo cáo ra Excel']],
    'ma_tran_widths': [2.4, 0.9, 0.8, 0.9, 0.8, 0.9],
    'quyen_sau': ['"Có" = dùng được chức năng; số liệu thấy được khác nhau theo cấp ở mục 3. Popup chi tiết, dòng Tổng cộng (kể cả Số dư đầu kỳ) và file Excel đều áp cùng phạm vi.'],
    'pham_vi': ('Phạm vi dữ liệu (ai xem được số của ai) — áp trên từng bút toán của sổ phải thu:',
                [['Cấp', 'Điều kiện thấy bút toán'],
                 ['Tổng công ty', 'Không giới hạn.'],
                 ['Công ty', 'Công ty ghi trên bút toán = công ty đang làm việc, HOẶC hợp đồng do chính mình tạo.'],
                 ['Phòng ban', 'Phòng ban trên bút toán thuộc các phòng mình quản lý, HOẶC hợp đồng do mình tạo. Không tự cộng phòng mình đang ngồi nếu không quản lý.'],
                 ['Bộ phận', 'Bộ phận trên bút toán thuộc các bộ phận mình quản lý, HOẶC hợp đồng do mình tạo.'],
                 ['Không quyền', 'Chỉ hợp đồng do mình tạo.']],
                [1.3, 5.0]),
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Phạm vi số liệu 4 cấp', ['– Theo bảng Phần 2 mục 3; cấp cao nhất người dùng có được áp.', '– Áp cho mọi số: dòng, dòng Tổng cộng (kể cả Số dư đầu kỳ), popup, Excel.', '– Ô lọc đơn vị chỉ hiện theo cấp (Phần 2).'], ['Xem báo cáo', 'Popup', 'Xuất Excel']),
        ('BR-02', 'Kỳ báo cáo theo ngày hạch toán', ['– Thời gian bắt buộc, mặc định trống.', '– Trước Từ ngày → Số dư đầu kỳ; từ Từ ngày đến hết Đến ngày → phát sinh; sau Đến ngày → không tính.', '– Dòng hợp đồng có mặt nếu có bút toán đến hết Đến ngày, kể cả không phát sinh trong kỳ.'], ['Xem báo cáo', 'Popup', 'Xuất Excel']),
        ('BR-03', 'Dòng khách hàng', ['– Bằng tổng MỌI dòng hợp đồng của khách theo bộ lọc, không phụ thuộc trang đang xem.', '– STT khách nối tiếp giữa các trang; hợp đồng đánh N.1, N.2…'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-04', 'Dòng Tổng cộng', ['– Không áp Số dư cuối kỳ (Dư nợ / Dư có) và ô tìm nhanh ⇒ có thể khác tổng các dòng.', '– Số dư đầu kỳ tính cả bút toán chưa gắn khách hàng; khi lọc Số hợp đồng thì đầu kỳ lấy số hợp đồng CHỨA chuỗi, phát sinh lấy ĐÚNG số hợp đồng.', '– Chuyển trang không tính lại.'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-05', 'Công thức cột', ['– Hàng hóa/Dịch vụ = Nợ (xuất kho, xuất bán hàng mượn, hạch toán DV, thanh lý, hạch toán DV BH-SC, khai báo đầu kỳ) − Có (cùng nhóm, trừ khai báo đầu kỳ).', '– ĐCCN tăng = Nợ phiếu kế toán; ĐCCN giảm = Có phiếu kế toán.', '– Nhập trả lại = Có − Nợ phiếu nhập hàng.', '– Đã thanh toán = Có phiếu thu, báo có, khai báo đầu kỳ.', '– Trả lại tiền thừa = Nợ phiếu chi, ủy nhiệm chi.', '– Cuối kỳ = Đầu kỳ + Cộng tăng − Cộng giảm + Trả lại tiền thừa.'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-06', 'Hiển thị số và Excel', ['– Định dạng 1,234,567, VND không lẻ.', '– Số 0 để trống, trừ: dòng Tổng cộng, cột Số dư cuối kỳ, cột ĐCCN giảm ở dòng hợp đồng (in 0).', '– Excel xuất mọi dòng khớp bộ lọc, không chỉ trang đang xem.'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-07', 'Popup chi tiết chứng từ', ['– Cùng phạm vi + Thời gian + Khách hàng + Số hợp đồng + Công ty…Nhân viên; KHÔNG áp Số dư cuối kỳ và ô tìm nhanh.', '– Popup ĐCCN tăng có thêm khai báo đầu kỳ công nợ NCC và phiếu thu ghi Nợ; popup ĐCCN giảm có thêm phiếu thu ghi Có (giữ như hệ thống cũ) ⇒ tổng popup có thể khác số đã bấm.', '– Popup Hàng hóa/Dịch vụ cộng cả Có của khai báo đầu kỳ ở cột Phát sinh có, trong khi số trên báo cáo không trừ khoản này.'], ['Popup']),
        ('BR-08', 'Khoảng ngày ngược chiều', ['– Từ ngày > Đến ngày: báo đỏ dưới ô Thời gian + toast "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", xoá bảng, không tải, không xuất Excel.'], ['Tìm kiếm và lọc', 'Xuất Excel']),
    ],
    'phan5': {
        'title': 'Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu',
        'cau_dan': 'Báo cáo chỉ đọc sổ công nợ phải thu khách hàng. Các màn dưới đây dùng chung cách tính / phạm vi với báo cáo, hoặc là chứng từ nguồn mà popup chi tiết mở tới (lập ở đó thì số trên báo cáo đổi).',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng (phạm vi theo 4 quyền xem)',
    'mains': [('FR-01', 'Xem báo cáo chi tiết công nợ KH', 'view'), ('FR-04', 'Xuất báo cáo ra Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc báo cáo', 'view'), ('FR-03', 'Xem chi tiết chứng từ của số liệu', 'view')],
    'rieng': [('FR-03', 'Xem chi tiết chứng từ của số liệu', 'view', 'uc_xemct'),
              ('FR-04', 'Xuất báo cáo ra Excel', 'io', 'uc_xuat')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', R.build_srs(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)

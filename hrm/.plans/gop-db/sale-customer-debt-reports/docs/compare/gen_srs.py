# -*- coding: utf-8 -*-
"""SRS - Bảng đối chiếu công nợ 1 khách hàng (form Danh mục quốc gia + quy tắc màn BÁO CÁO của skill srs-documenter).

Khuôn: danh-muc-kho/docs/warehouses/gen_srs.py + _lib_win.py (KHÔNG sửa lib dùng chung). Màn báo cáo cần thêm các mục
sau bảng event ("Cách lấy dữ liệu và giải thích chỉ tiêu", "Danh sách popup mở từ số liệu", "Mục đích thiết kế popup",
"Các biến thể theo con số bấm") nên hàm dựng `build_srs_report` viết lại TRONG FILE NÀY, chép từ `_lib_win.build_srs`.

Nguồn (code HRM hiện tại):
  FE hrm-client/pages/sale/customer-debt-compare/{index.vue, components/ProductsModal.vue, components/export-excel.js},
     components/subsystem-menu/sale-hub.js, components/V2BaseCompanyDepartmentFilter.vue, utils/filterRequiredErrors.js,
     utils/mixins/reportPrintPreviewMixin.js, utils/invoiceable-link.js, utils/finance/customerDebtContractLink.js
  BE Modules/Finance/Http/Controllers/V1/CustomerDebtCompareController.php,
     Services/CustomerDebt/{CustomerDebtCompareReportService, AbstractCustomerDebtReportService, CustomerDebtAggregator,
     CustomerDebtScope}.php; quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (1694-1697)
Ảnh: hdsd_shots/ (capture.js, dev-hrm 02/11/2026).
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(GOPDB, 'danh-muc-kho', 'docs'))
import _lib_win as L  # noqa: E402
from _lib_win import QgWriter, SRS_ROLES, QTC_LINK, h1_trang_moi  # noqa: E402

TEN = 'Bảng đối chiếu công nợ 1 khách hàng'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q = 'Người dùng đã đăng nhập (mọi người dùng; quyền chỉ quyết định phạm vi dữ liệu)'
DK = '1. Người dùng đăng nhập thành công.\n2. Không cần quyền để mở màn; phạm vi dữ liệu theo BR-02.'
DK_DATA = DK + '\n3. Đã chọn Thời gian (Từ ngày, Đến ngày) và ít nhất 1 Khách hàng.'

UI6 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả']
UI6W = [0.5, 1.35, 0.85, 0.8, 0.95, 2.75]
UI7 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả']
UI7W = [0.45, 1.2, 0.85, 0.8, 1.0, 0.85, 2.6]


def ui(header, rows):
    return [header] + [[str(i + 1)] + r for i, r in enumerate(rows)]


def tip(head, *lines):
    return '%s • %s' % (head, ' • '.join(lines))


# ---------------------------------------------------------------- nội dung ⓘ (nguyên văn COLUMN_TIPS trong index.vue)
TIP = {
    'stt': tip('Số thứ tự', 'Dòng đậm là hợp đồng, đánh số 1, 2, 3… liên tục qua các trang.',
               'Dòng chứng từ của hợp đồng đánh số theo hợp đồng: 1.1, 1.2…'),
    'ngay': tip('Ngày hạch toán của chứng từ', 'Dòng hợp đồng để trống.',
                'Chứng từ xếp theo ngày hạch toán, cùng ngày thì theo thời điểm tạo.'),
    'so': tip('Số hợp đồng / số chứng từ', 'Dòng đậm: số hợp đồng.',
              'Dòng chứng từ: số chứng từ ghi công nợ; phiếu xuất kho, phiếu xuất bán hàng mượn, phiếu nhập kho hàng trả lại kèm số phiếu yêu cầu trong ngoặc.',
              'Bấm số phiếu xuất kho / xuất bán hàng mượn để xem danh sách hàng hóa.'),
    'dg': tip('Diễn giải của chứng từ',
              'Phiếu thu, phiếu chi, ủy nhiệm chi, phiếu điều chỉnh công nợ: lấy ghi chú của dòng ứng với hợp đồng này.',
              'Chứng từ khác: lấy ghi chú chung của chứng từ.'),
    'ddk': tip('Công nợ khách hàng còn phải trả trước Từ ngày',
               'Dòng Tổng cộng = Tổng ghi Nợ − Tổng ghi Có của tài khoản phải thu khách hàng (131 và tài khoản con) có ngày hạch toán trước Từ ngày, theo khách hàng, số hợp đồng đang lọc và phạm vi quyền.',
               'Dòng hợp đồng và dòng chứng từ để trống (giữ cách tính của ERP).'),
    'tang': tip('Các khoản làm tăng công nợ khách hàng trong kỳ', 'Gồm 2 cột: Hàng hóa/Dịch vụ và Điều chỉnh công nợ (tăng).'),
    'hh': tip('Giá trị hàng hóa / dịch vụ bán cho khách trong kỳ',
              'Hàng hóa/Dịch vụ = Ghi Nợ − Ghi Có của phiếu xuất kho, phiếu xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ bảo hành - sửa chữa.',
              'Phần ghi Nợ tính thêm khai báo công nợ đầu kỳ.'),
    'dct': tip('Điều chỉnh tăng công nợ trong kỳ', 'Điều chỉnh công nợ tăng = Tổng ghi Nợ của phiếu điều chỉnh công nợ.'),
    'giam': tip('Các khoản làm giảm công nợ khách hàng trong kỳ', 'Gồm 3 cột: Nhập trả lại, Đã thanh toán và Điều chỉnh công nợ (giảm).'),
    'ntl': tip('Giá trị hàng khách trả lại trong kỳ', 'Nhập trả lại = Ghi Có − Ghi Nợ của phiếu nhập kho hàng trả lại.'),
    'dtt': tip('Số tiền khách đã thanh toán trong kỳ', 'Đã thanh toán = Tổng ghi Có của phiếu thu, phiếu báo có và khai báo công nợ đầu kỳ.'),
    'dcg': tip('Điều chỉnh giảm công nợ trong kỳ', 'Điều chỉnh công nợ giảm = Tổng ghi Có của phiếu điều chỉnh công nợ.'),
    'tltt': tip('Tiền thừa công ty trả lại cho khách trong kỳ', 'Trả lại tiền thừa = Tổng ghi Nợ của phiếu chi và ủy nhiệm chi.',
                'Khoản này làm tăng số dư cuối kỳ.'),
    'dck': tip('Công nợ khách hàng còn phải trả đến hết Đến ngày',
               'Dòng Tổng cộng = Số dư đầu kỳ + Hàng hóa/Dịch vụ + Điều chỉnh công nợ tăng − Nhập trả lại − Đã thanh toán − Điều chỉnh công nợ giảm + Trả lại tiền thừa.',
               'Dòng hợp đồng = Hàng hóa/Dịch vụ − Nhập trả lại − Đã thanh toán + Trả lại tiền thừa (không tính 2 cột Điều chỉnh công nợ — giữ cách tính của ERP).',
               'Dòng chứng từ = số dư cộng dồn từ chứng từ đầu tiên của hợp đồng: số dư dòng trên + Hàng hóa/Dịch vụ − Nhập trả lại − Đã thanh toán + Trả lại tiền thừa của chứng từ này.'),
    'tong': 'Tổng trên mọi chứng từ công nợ của khách hàng theo bộ lọc, kể cả chứng từ chưa gắn hợp đồng (giống ERP). Số dư đầu kỳ của từng hợp đồng để trống, số dư cuối kỳ từng hợp đồng chưa trừ điều chỉnh công nợ giảm — giữ nguyên cách tính của ERP. Ô tìm nhanh chỉ thu hẹp danh sách hợp đồng, không đổi dòng tổng.',
    'trang': 'Đối chiếu công nợ phải thu của khách hàng theo từng hợp đồng trong kỳ: số dư đầu kỳ, phát sinh tăng / giảm, trả lại tiền thừa, số dư cuối kỳ và từng chứng từ. Dữ liệu theo quyền xem (tổng công ty / công ty / phòng ban / bộ phận); không có quyền thì chỉ thấy hợp đồng do mình tạo.',
}
NUM = '- Số theo định dạng 1,234,567, không có phần lẻ; số âm có dấu "-".\n- Ô bằng 0 để trống (riêng dòng Tổng cộng in "0").'

# ---------------------------------------------------------------- Phần 5 (dò code FE/BE + menu 02/11/2026)
P5 = [
    ('Bán hàng', 'Tổng hợp công nợ theo NV (cùng công thức 8 cột công nợ, cùng cách phân phạm vi 4 cấp)', 'Bán hàng => Báo cáo => Báo cáo công nợ'),
    ('Bán hàng', 'Chi tiết công nợ KH (cùng công thức 8 cột công nợ, cùng cách phân phạm vi 4 cấp)', 'Bán hàng => Báo cáo => Báo cáo công nợ'),
    ('Tài chính', 'Báo cáo hạn mức công nợ khách hàng (cùng công thức số dư công nợ)', 'Tài chính => Kế toán công nợ => Khách hàng'),
    ('Tài chính', 'Báo cáo hạn mức công nợ nhân viên (cùng công thức số dư công nợ)', 'Tài chính => Kế toán công nợ => Nhân viên'),
    ('Tài chính', 'Phiếu xuất hàng (chứng từ nguồn cột Hàng hóa/Dịch vụ; mở từ số chứng từ / popup)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ('Tài chính', 'Phiếu xuất bán hàng mượn (chứng từ nguồn cột Hàng hóa/Dịch vụ; mở từ số chứng từ / popup)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng'),
    ('Tài chính', 'Phiếu nhập hàng (hàng khách trả lại — cột Nhập trả lại)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
    ('Tài chính', 'Phiếu thu (cột Đã thanh toán)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu báo có (cột Đã thanh toán)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu chi (cột Trả lại tiền thừa)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu ủy nhiệm chi (cột Trả lại tiền thừa)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu kế toán (phiếu điều chỉnh công nợ — 2 cột Điều chỉnh công nợ)', 'Tài chính => Sổ tổng hợp => Sổ tổng hợp'),
    ('Tài chính', 'Khai báo đầu kỳ công nợ (cột Hàng hóa/Dịch vụ, Đã thanh toán)', 'Tài chính => Khai báo đầu kỳ'),
    ('Tài chính', 'Công nợ đầu kỳ theo khách hàng - hợp đồng (cùng màn Khai báo đầu kỳ công nợ)', 'Tài chính => Kế toán công nợ => Khách hàng'),
    ('Bán hàng', 'YC điều chỉnh công nợ (đầu vào của phiếu điều chỉnh công nợ)', 'Bán hàng => Yêu cầu => Công nợ - Thu - Chi'),
    ('Bán hàng', 'Hợp đồng bán hàng (mở từ số hợp đồng ở dòng đậm)', 'Bán hàng => Bán hàng => Hợp đồng bán hàng'),
]

FR = []

# ================================================================ 2.1 Xem báo cáo
COT = [
    ['Tiêu đề trang', 'Label', 'Hiển thị', TEN, ['- Ở thanh trên cùng, kèm icon ⓘ.', '- Icon ⓘ: "%s"' % TIP['trang']]],
    ['Tiêu đề bảng', 'Label', 'Hiển thị', TEN, ['- Tiêu đề khối bảng kết quả.']],
    ['Nút In', 'Button', 'Enable', 'Hiển thị', ['- Mở cửa sổ xem trước bản in theo bộ lọc đang áp (mục 2.4).', '- Chưa chọn đủ Khách hàng và Thời gian: báo "Vui lòng chọn khách hàng và thời gian", không mở cửa sổ.']],
    ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', ['- Mở cửa sổ "Chọn trường xuất Excel" (mục 2.5).', '- Chưa chọn đủ Khách hàng và Thời gian: báo "Vui lòng chọn khách hàng và thời gian".', '- Bị khoá trong lúc đang xuất file.']],
    ['Bảng chi tiết báo cáo', 'Table/Grid', 'Read-only', 'Lời nhắc', [
        '- Tiêu đề 2 tầng, gồm 12 cột (mỗi cột mô tả ở 1 dòng bên dưới): STT, Ngày chứng từ, Số chứng từ, Diễn giải, Số dư đầu kỳ, Phát sinh tăng trong kỳ (Hàng hóa/Dịch vụ, Điều chỉnh công nợ), Phát sinh giảm trong kỳ (Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ), Trả lại tiền thừa, Số dư cuối kỳ.',
        '- Thứ tự dòng: dòng Tổng cộng → dòng hợp đồng (chữ đậm, nền xám nhạt) → các dòng chứng từ của hợp đồng đó.',
        '- Tiêu đề bảng dính khi cuộn dọc; có thanh cuộn ngang ở cả trên và dưới bảng.',
        '- Chưa chọn đủ Thời gian + Khách hàng: "Chọn thời gian và khách hàng để xem bảng đối chiếu."',
        '- Đang tải: "Đang tải dữ liệu..."',
        '- Không có hợp đồng nào: "Không có dữ liệu phù hợp bộ lọc."']],
    ['Dòng Tổng cộng', 'Table/Grid', 'Read-only', 'Theo dữ liệu', [
        '- Dòng đầu bảng, gộp 4 cột đầu, chữ "Tổng cộng" kèm icon ⓘ; 8 cột số là tổng của khách hàng theo bộ lọc (cách tính: mục 2.1.5).',
        '- Icon ⓘ: "%s"' % TIP['tong'],
        '- Số bằng 0 vẫn in "0".',
        '- Không đổi khi chuyển trang và khi dùng ô tìm nhanh.']],
    ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', [
        '- Dòng hợp đồng: 1, 2, 3… liên tục qua các trang.', '- Dòng chứng từ: <số hợp đồng>.<thứ tự>, vd 1.1, 1.2.',
        '- Icon ⓘ: "%s"' % TIP['stt']]],
    ['Cột Ngày chứng từ', 'Table/Grid', 'Read-only', 'Hiển thị', [
        '- Ngày hạch toán của chứng từ, dạng dd/mm/yyyy; dòng hợp đồng để trống.', '- Icon ⓘ: "%s"' % TIP['ngay']]],
    ['Cột Số chứng từ', 'Table/Grid', 'Read-only', 'Hiển thị', [
        '- Dòng hợp đồng: số hợp đồng, chữ dạng liên kết. Bấm → mở màn hợp đồng ở tab mới (loại hợp đồng chưa có màn thì hiện chữ thường).',
        '- Dòng phiếu xuất hàng / phiếu xuất bán hàng mượn: "<số phiếu> (<số phiếu yêu cầu>)". Bấm → mở popup Danh sách hàng hóa (mục 2.3).',
        '- Dòng phiếu nhập hàng trả lại: "<số phiếu> (<số phiếu yêu cầu nhập hàng>)". Bấm → mở phiếu ở tab mới.',
        '- Chứng từ khác (phiếu thu, phiếu chi, phiếu báo có, ủy nhiệm chi, phiếu kế toán, khai báo đầu kỳ…): bấm → mở chứng từ ở tab mới.',
        '- Icon ⓘ: "%s"' % TIP['so']]],
    ['Cột Diễn giải', 'Table/Grid', 'Read-only', 'Hiển thị', [
        '- Dòng chứng từ: ghi chú của chứng từ (cách lấy: mục 2.1.5); dòng hợp đồng để trống.', '- Dài thì tự xuống dòng.',
        '- Icon ⓘ: "%s"' % TIP['dg']]],
    ['Cột Số dư đầu kỳ', 'Table/Grid', 'Read-only', 'Hiển thị', [
        '- Chỉ có số ở dòng Tổng cộng; dòng hợp đồng và dòng chứng từ để trống.', NUM, '- Icon ⓘ: "%s"' % TIP['ddk']]],
    ['Tiêu đề nhóm Phát sinh tăng trong kỳ', 'Label', 'Hiển thị', 'Hiển thị', ['- Gộp 2 cột Hàng hóa/Dịch vụ, Điều chỉnh công nợ.', '- Icon ⓘ: "%s"' % TIP['tang']]],
    ['Cột Hàng hóa/Dịch vụ', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Giá trị hàng hóa / dịch vụ bán cho khách trong kỳ, ở cả 3 loại dòng.', NUM, '- Icon ⓘ: "%s"' % TIP['hh']]],
    ['Cột Điều chỉnh công nợ (tăng)', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Điều chỉnh tăng công nợ trong kỳ, ở cả 3 loại dòng.', NUM, '- Icon ⓘ: "%s"' % TIP['dct']]],
    ['Tiêu đề nhóm Phát sinh giảm trong kỳ', 'Label', 'Hiển thị', 'Hiển thị', ['- Gộp 3 cột Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ.', '- Icon ⓘ: "%s"' % TIP['giam']]],
    ['Cột Nhập trả lại', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Giá trị hàng khách trả lại trong kỳ.', NUM, '- Icon ⓘ: "%s"' % TIP['ntl']]],
    ['Cột Đã thanh toán', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Số tiền khách đã thanh toán trong kỳ.', NUM, '- Icon ⓘ: "%s"' % TIP['dtt']]],
    ['Cột Điều chỉnh công nợ (giảm)', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Điều chỉnh giảm công nợ trong kỳ.', NUM, '- Icon ⓘ: "%s"' % TIP['dcg']]],
    ['Cột Trả lại tiền thừa', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Tiền thừa công ty trả lại khách trong kỳ; làm TĂNG số dư cuối kỳ.', NUM, '- Icon ⓘ: "%s"' % TIP['tltt']]],
    ['Cột Số dư cuối kỳ', 'Table/Grid', 'Read-only', 'Hiển thị', [
        '- Dòng Tổng cộng: công nợ còn phải thu đến hết Đến ngày.',
        '- Dòng hợp đồng: không tính 2 cột Điều chỉnh công nợ (BR-07).',
        '- Dòng chứng từ: số dư cộng dồn trong hợp đồng.', NUM, '- Icon ⓘ: "%s"' % TIP['dck']]],
    ['Chân bảng', 'Label', 'Hiển thị', 'Ẩn khi không có dữ liệu', ['- "Hiển thị a–b / N hợp đồng": N = số hợp đồng lên bảng; phân trang theo HỢP ĐỒNG, không cắt rời chứng từ của 1 hợp đồng.']],
    ['Ô Số dòng/trang', 'Dropdown', 'Enable', '10', ['- Lựa chọn: 10, 20, 50, 100 hợp đồng / trang.', '- Mặc định: 10.', '- Đổi số dòng → quay về trang 1.']],
    ['Phân trang', 'Button', 'Enable', 'Trang 1', ['- Chuyển trang; giữ nguyên bộ lọc và dòng Tổng cộng.']],
]

DATA_MAIN = [
    ('Tập dữ liệu / thời điểm số liệu', 'Bút toán ghi sổ tài khoản phải thu khách hàng (131 và các tài khoản con trực tiếp) của các khách hàng đã chọn, có ngày hạch toán đến hết Đến ngày, sau khi áp phạm vi quyền (BR-02) và bộ lọc. "Trong kỳ" = ngày hạch toán từ Từ ngày đến hết Đến ngày; "đầu kỳ" = trước Từ ngày. Số liệu đọc tại thời điểm bấm Tìm kiếm (không lưu sẵn).', '—'),
    ('Dòng Tổng cộng — 7 cột phát sinh', 'Cộng MỌI bút toán trong kỳ của khách hàng theo bộ lọc, kể cả bút toán chưa gắn hợp đồng và hợp đồng không lên bảng. Ô tìm nhanh không làm đổi dòng này; ô Số hợp đồng, Công ty/Phòng ban/Bộ phận/Nhân viên có làm đổi.', TIP['tong']),
    ('Dòng hợp đồng (dòng đậm)', 'Một dòng cho mỗi hợp đồng có bút toán của khách hàng; chỉ hiện hợp đồng có ít nhất 1 trong 7 cột phát sinh khác 0 (so phần nguyên). Bút toán không gắn hợp đồng không thành dòng. Xếp theo thứ tự hợp đồng được tạo trong hệ thống.', '—'),
    ('Dòng chứng từ (N.i)', 'Mỗi chứng từ phát sinh trong kỳ của hợp đồng (gom theo chứng từ). Lấy theo bộ tài khoản phải thu cố định riêng của dòng chứng từ (khác tập tài khoản của dòng hợp đồng / Tổng cộng) và không lọc lại theo khách hàng. Bỏ chứng từ có 7 cột phát sinh đều bằng 0. Xếp theo ngày hạch toán, cùng ngày theo thời điểm tạo.', '—'),
    ('Ngày chứng từ', 'Ngày hạch toán của chứng từ.', TIP['ngay']),
    ('Số chứng từ', 'Dòng hợp đồng: số hợp đồng. Dòng chứng từ: số chứng từ; phiếu xuất hàng / phiếu xuất bán hàng mượn kèm số phiếu yêu cầu xuất; phiếu nhập hàng trả lại kèm số phiếu yêu cầu nhập hàng (lấy từ phiếu nhập, không có thì qua đề nghị nhập kho).', TIP['so']),
    ('Diễn giải', 'Phiếu thu, phiếu chi, ủy nhiệm chi, phiếu điều chỉnh công nợ: ghi chú của DÒNG chi tiết ứng với hợp đồng này trên chứng từ. Chứng từ khác: ghi chú chung của chứng từ.', TIP['dg']),
    ('Số dư đầu kỳ', 'Dòng Tổng cộng: Tổng ghi Nợ − Tổng ghi Có của các bút toán có ngày hạch toán trước Từ ngày, theo khách hàng, ô Số hợp đồng (gần đúng), Công ty / Phòng ban / Bộ phận ghi trên bút toán, Nhân viên = người tạo hợp đồng, và phạm vi quyền. Dòng hợp đồng, dòng chứng từ: luôn để trống.', TIP['ddk']),
    ('Hàng hóa/Dịch vụ', 'Ghi Nợ của phiếu xuất hàng, phiếu xuất bán hàng mượn, khai báo công nợ đầu kỳ, hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ bảo hành - sửa chữa − Ghi Có của cùng các loại đó (trừ khai báo đầu kỳ). Áp cho cả 3 loại dòng; dòng hợp đồng = phát sinh của hợp đồng; Tổng cộng = phát sinh của khách hàng.', TIP['hh']),
    ('Điều chỉnh công nợ (tăng)', 'Tổng ghi Nợ của phiếu điều chỉnh công nợ (phiếu kế toán) trong kỳ.', TIP['dct']),
    ('Nhập trả lại', 'Ghi Có − Ghi Nợ của phiếu nhập hàng (khách trả lại) trong kỳ.', TIP['ntl']),
    ('Đã thanh toán', 'Tổng ghi Có của phiếu thu, phiếu báo có, khai báo công nợ đầu kỳ trong kỳ.', TIP['dtt']),
    ('Điều chỉnh công nợ (giảm)', 'Tổng ghi Có của phiếu điều chỉnh công nợ (phiếu kế toán) trong kỳ.', TIP['dcg']),
    ('Trả lại tiền thừa', 'Tổng ghi Nợ của phiếu chi và phiếu ủy nhiệm chi trong kỳ.', TIP['tltt']),
    ('Số dư cuối kỳ — dòng Tổng cộng', 'Số dư đầu kỳ + Hàng hóa/Dịch vụ + Điều chỉnh công nợ tăng − Nhập trả lại − Đã thanh toán − Điều chỉnh công nợ giảm + Trả lại tiền thừa.', TIP['dck']),
    ('Số dư cuối kỳ — dòng hợp đồng', 'Hàng hóa/Dịch vụ − Nhập trả lại − Đã thanh toán + Trả lại tiền thừa (KHÔNG tính số dư đầu kỳ và 2 cột Điều chỉnh công nợ). Vì vậy tổng Số dư cuối kỳ các dòng hợp đồng thường KHÁC dòng Tổng cộng.', '(dùng chung ⓘ của cột Số dư cuối kỳ)'),
    ('Số dư cuối kỳ — dòng chứng từ', 'Cộng dồn từ chứng từ đầu tiên của hợp đồng (bắt đầu từ 0): số dư dòng trên + Hàng hóa/Dịch vụ − Nhập trả lại − Đã thanh toán + Trả lại tiền thừa của chứng từ này. Chứng từ chỉ có Điều chỉnh công nợ không làm đổi số dư. Bằng 0 thì để trống.', '(dùng chung ⓘ của cột Số dư cuối kỳ)'),
    ('Ràng buộc khớp số', '- 7 cột phát sinh: dòng Tổng cộng = tổng các dòng hợp đồng khi khách hàng không có bút toán chưa gắn hợp đồng và mọi hợp đồng đều lên bảng.\n- Dòng hợp đồng: mỗi cột phát sinh thường bằng tổng các dòng chứng từ của nó (có thể lệch khi bút toán ghi vào tài khoản con khác bộ tài khoản của dòng chứng từ).\n- Số dư cuối kỳ của dòng chứng từ CUỐI cùng = Số dư cuối kỳ của dòng hợp đồng (cùng điều kiện trên).', '—'),
    ('Chân bảng "Hiển thị a–b / N hợp đồng"', 'N = số dòng hợp đồng lên bảng (sau khi bỏ hợp đồng toàn số 0 và áp ô tìm nhanh).', '—'),
]

POPUP_MAIN = [
    ('Số phiếu xuất hàng ở cột Số chứng từ (dòng chứng từ)', 'Danh sách hàng hóa (mục 2.3)', 'Số Hàng hóa/Dịch vụ của phiếu xuất này gồm những mặt hàng nào, số lượng, đơn giá bao nhiêu', 'Mọi dòng hàng của đúng phiếu xuất đã bấm; cột SL đề nghị, SL thực xuất, Thành tiền bán'),
    ('Số phiếu xuất bán hàng mượn ở cột Số chứng từ (dòng chứng từ)', 'Danh sách hàng hóa (mục 2.3) — biến thể hàng mượn', 'Khách đã mua lại những mặt hàng mượn nào', 'Mọi dòng hàng của đúng phiếu xuất bán hàng mượn; cột Số lượng, không có Thành tiền bán'),
    ('Số hợp đồng ở dòng đậm', 'Không phải popup — mở màn chi tiết hợp đồng ở tab mới', 'Xem điều khoản / giá trị hợp đồng đang đối chiếu', 'Hợp đồng tương ứng; loại hợp đồng chưa có màn thì hiện chữ thường, không bấm được'),
    ('Số chứng từ khác (phiếu thu, phiếu chi, phiếu báo có, ủy nhiệm chi, phiếu kế toán, phiếu nhập hàng, khai báo đầu kỳ…)', 'Không phải popup — mở màn chi tiết chứng từ ở tab mới', 'Kiểm tra chứng từ gốc tạo ra con số', 'Đúng chứng từ của dòng'),
    ('Ô số tiền (mọi cột số, mọi dòng)', 'Không bấm được', '—', '—'),
]

FR.append({
    'ten': 'Xem báo cáo đối chiếu công nợ',
    'qtc': 'Màn Báo cáo, Phân trang, Định dạng số.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem báo cáo đối chiếu công nợ'],
        ['Mô tả', 'Hiển thị công nợ phải thu của khách hàng đã chọn trong kỳ: dòng Tổng cộng, từng hợp đồng và từng chứng từ phát sinh của hợp đồng, gồm số dư đầu kỳ, phát sinh tăng / giảm, trả lại tiền thừa và số dư cuối kỳ. Màn chỉ đọc.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu; bảng hiện lời nhắc "Chọn thời gian và khách hàng để xem bảng đối chiếu.", chưa tải số liệu.\n2. Người dùng chọn Thời gian và Khách hàng (mục 2.2).\n3. Hệ thống tính số liệu theo phạm vi quyền + bộ lọc, hiện dòng Tổng cộng, trang 1 gồm 10 hợp đồng và chứng từ của từng hợp đồng.\n4. Chân bảng ghi "Hiển thị a–b / N hợp đồng".'],
        ['Dòng sự kiện phụ', '• Không có hợp đồng nào có phát sinh → "Không có dữ liệu phù hợp bộ lọc." (dòng Tổng cộng ẩn).\n• Lỗi khi lấy dữ liệu → báo "Lỗi khi tải dữ liệu".\n• Người dùng đổi bộ lọc liên tục: chỉ kết quả của lần lọc mới nhất được hiển thị.\n• Chuyển trang / đổi số dòng: không tính lại dòng Tổng cộng.'],
        ['Yêu cầu đặc biệt', 'Thời gian tải 1 trang (10 hợp đồng) trên môi trường thử nghiệm dưới 1 giây; khách hàng nhiều hợp đồng (218 hợp đồng, 100 hợp đồng / trang) khoảng 2–3 giây.'],
    ],
    'anh': [('01_empty', 'Màn Bảng đối chiếu công nợ 1 khách hàng lúc mới mở (chưa chọn bộ lọc)'),
            ('03_report', 'Bảng đối chiếu có số liệu (Khách hàng CÔNG TY CỔ PHẦN BÁCH LIÊN, 01/01/2026 – 30/06/2026)'),
            ('12_read_zoom', 'Phóng to cột STT và 8 cột số (dòng Tổng cộng, hợp đồng 1, 2) của ảnh trên'),
            ('05_col_tip', 'Icon ⓘ ở tiêu đề cột giải thích cách tính (cột Số dư cuối kỳ)')],
    'ui': ui(UI6, COT),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Không kiểm quyền vào màn; đọc cấp phạm vi của người dùng (BR-02) để hiện các ô lọc tổ chức.\nAfter:\n– Khôi phục bộ lọc đã dùng trong 10 phút (BR-13); đủ Thời gian + Khách hàng thì tải dữ liệu, chưa đủ thì hiện lời nhắc.'],
        ['Bấm Tìm kiếm / đổi giá trị ô lọc', 'Click / Change', 'Xem mục 2.2.'],
        ['Chuyển trang / đổi Số dòng/trang', 'Click / Change', 'After:\n– Tải lại các dòng hợp đồng của trang mới, giữ bộ lọc và dòng Tổng cộng; đổi số dòng thì về trang 1.'],
        ['Bấm số phiếu xuất hàng / phiếu xuất bán hàng mượn', 'Click', 'After:\n– Mở popup Danh sách hàng hóa của phiếu (mục 2.3).'],
        ['Bấm số hợp đồng / số chứng từ khác', 'Click', 'After:\n– Mở màn chi tiết hợp đồng / chứng từ ở tab mới; màn báo cáo giữ nguyên.'],
        ['Rê chuột vào icon ⓘ', 'Hover', 'After:\n– Hiện chú thích cách tính của cột / dòng Tổng cộng (nội dung ở bảng 2.1.5).'],
    ],
    'them': [
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', [
            ('p', 'Bảng dưới mô tả cách hệ thống tính từng chỉ tiêu, từng cột số liệu và nội dung icon ⓘ (nguyên văn trên giao diện). "Tập dữ liệu" là các bút toán công nợ phải thu của khách hàng đã chọn sau khi áp phạm vi quyền và bộ lọc.'),
            ('data', DATA_MAIN)]),
        ('Danh sách popup mở từ số liệu', [('popup', POPUP_MAIN)]),
    ],
})

# ================================================================ 2.2 Tìm kiếm và lọc
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc bảng đối chiếu'],
        ['Mô tả', 'Chọn khách hàng, kỳ đối chiếu và thu hẹp số liệu bằng Số hợp đồng, ô tìm nhanh, Công ty / Phòng ban / Bộ phận / Nhân viên (theo cấp phạm vi).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn Bảng đối chiếu công nợ 1 khách hàng.'],
        ['Dòng sự kiện chính', '1. Người dùng chọn Thời gian (Từ ngày → Đến ngày) và một hoặc nhiều Khách hàng.\n2. Hệ thống tự tải bảng ngay khi đủ 2 ô bắt buộc.\n3. Người dùng nhập thêm Số hợp đồng / từ khoá tìm nhanh rồi bấm Tìm kiếm hoặc Enter; hoặc chọn Công ty / Phòng ban / Bộ phận / Nhân viên (tải lại ngay).\n4. Hệ thống áp đồng thời mọi điều kiện, tải lại từ trang 1.'],
        ['Dòng sự kiện phụ', '• Bấm Tìm kiếm khi thiếu ô bắt buộc → chữ đỏ dưới ô "Vui lòng chọn thời gian" / "Vui lòng chọn khách hàng", không tải dữ liệu; chọn xong ô thì chữ đỏ tự tắt.\n• Lịch của ô Thời gian khoá các ngày làm Từ ngày lớn hơn Đến ngày.\n• Bấm Làm mới → xoá mọi điều kiện (kể cả Thời gian, Khách hàng), bảng về lời nhắc.\n• Bấm F5 = Làm mới; rời màn rồi quay lại trong 10 phút thì giữ bộ lọc.'],
    ],
    'anh': [('02_required', 'Khu vực bộ lọc — bấm Tìm kiếm khi chưa chọn Thời gian, Khách hàng'),
            ('07_keyword', 'Ô tìm nhanh thu hẹp còn hợp đồng có chứng từ PXBHM-04941, dòng Tổng cộng giữ nguyên')],
    'ui': ui(UI7, [
        ['Ô tìm nhanh', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', ['- Placeholder "Tìm theo số hợp đồng hoặc số chứng từ".', '- Giữ hợp đồng có số hợp đồng hoặc có ít nhất 1 số chứng từ chứa từ khoá (gần đúng).', '- Chỉ áp khi bấm Tìm kiếm / Enter.', '- Không làm đổi dòng Tổng cộng (BR-09).']],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', ['- Kiểm 2 ô bắt buộc rồi tải lại bảng từ trang 1.']],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', ['- Xoá mọi điều kiện lọc, ẩn chữ đỏ, bảng về lời nhắc.']],
        ['Nút Ẩn / Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Mở', ['- Thu gọn / mở khu vực các ô lọc.']],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', ['- Chọn ô lọc nào được hiển thị (quy tắc chung).']],
        ['Ô Thời gian', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', ['- Bắt buộc (dấu *).', '- 1 ô gồm Từ ngày → Đến ngày, tính cả 2 đầu mút theo ngày hạch toán.', '- Lịch Từ ngày khoá ngày sau Đến ngày; lịch Đến ngày khoá ngày trước Từ ngày.', '- Trống khi bấm Tìm kiếm: "Vui lòng chọn thời gian".', '- Mặc định: trống (mở màn / F5 / Làm mới đều về trống).']],
        ['Ô Khách hàng', 'Dropdown', 'Enable', 'Danh sách khách hàng, chọn nhiều', 'Trống', ['- Bắt buộc (dấu *).', '- Gõ từ 2 ký tự để tìm; hiển thị "Mã KH - Tên khách hàng"; có nút × xoá.', '- Chọn nhiều khách hàng: số liệu cộng chung như một khách.', '- Trống khi bấm Tìm kiếm: "Vui lòng chọn khách hàng".', '- Mặc định: trống.']],
        ['Ô Số hợp đồng', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', ['- Lọc gần đúng theo số hợp đồng; áp cả dòng Tổng cộng và Số dư đầu kỳ (BR-09).', '- Áp khi bấm Tìm kiếm / Enter.']],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty, chọn nhiều', 'Trống', ['- Chỉ hiện với người có quyền xem theo tổng công ty.', '- Icon khoá cạnh nhãn: bật / tắt hiện cả công ty đã khoá ("Hiện cả công ty đã khoá").', '- Lọc theo công ty của người tạo hợp đồng (BR-10).']],
        ['Ô Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Theo công ty đã chọn, chọn nhiều', 'Trống', ['- Hiện với cấp tổng công ty, công ty, phòng ban.', '- Icon khoá: "Hiện cả phòng ban đã khoá".', '- Lọc theo phòng ban của người tạo hợp đồng.']],
        ['Ô Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Theo phòng ban đã chọn, chọn nhiều', 'Trống', ['- Hiện với cấp tổng công ty, công ty, phòng ban, bộ phận.', '- Icon khoá: "Hiện cả bộ phận đã khoá".', '- Lọc theo bộ phận của người tạo hợp đồng.']],
        ['Ô Nhân viên', 'Dropdown', 'Enable / Ẩn', 'Nhân viên, chọn nhiều', 'Trống', ['- Hiện với mọi cấp có quyền; người không có quyền không thấy cả 4 ô tổ chức.', '- Hiển thị "Tên - Mã phòng - Mã NV"; icon khoá: "Hiện cả nhân viên đã nghỉ".', '- Lọc hợp đồng do nhân viên đó tạo.']],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Chọn Thời gian / Khách hàng / ô tổ chức', 'Change', 'After:\n– Đủ Thời gian + Khách hàng → tải lại bảng từ trang 1 (không cần bấm Tìm kiếm); chưa đủ → bảng về lời nhắc.'],
        ['Gõ ô tìm nhanh / Số hợp đồng', 'Keypress', 'After:\n– Chưa lọc; chờ Enter hoặc nút Tìm kiếm.'],
        ['Bấm Tìm kiếm / Enter', 'Click', 'Before:\n– Thiếu Thời gian hoặc Khách hàng → chữ đỏ "Vui lòng chọn thời gian" / "Vui lòng chọn khách hàng", dừng.\nAfter:\n– Áp mọi điều kiện, tải lại từ trang 1, lưu bộ lọc.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện và bộ lọc đã lưu, bảng về lời nhắc.'],
    ],
})

# ================================================================ 2.3 Popup hàng hóa
POP_COLS = [
    ['Tiêu đề popup', 'Label', 'Hiển thị', 'Danh sách hàng hóa', ['- Dòng phụ: "Phiếu xuất hàng - <số phiếu>" hoặc "Phiếu xuất bán hàng mượn - <số phiếu>".']],
    ['Tiêu đề bảng', 'Label', 'Hiển thị', 'Hàng hóa', ['- Bảng không có lọc / phân trang riêng; đang tải thì hiện biểu tượng tải.', '- Không có dòng: "Không có dữ liệu phù hợp."']],
    ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', ['- 1, 2, 3… theo thứ tự dòng hàng trên phiếu.']],
    ['Cột Tên hàng hóa', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Tên hàng trên phiếu.']],
    ['Cột Model', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Model của hàng.']],
    ['Cột Mã hàng hóa', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Mã hàng.']],
    ['Cột Đơn vị tính', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Đơn vị tính.']],
    ['Cột SL đề nghị', 'Table/Grid', 'Read-only', 'Chỉ phiếu xuất hàng', ['- Số lượng đề nghị xuất; tối đa 2 chữ số lẻ; 0 để trống.']],
    ['Cột SL thực xuất', 'Table/Grid', 'Read-only', 'Chỉ phiếu xuất hàng', ['- Số lượng đã xuất; tối đa 2 chữ số lẻ.']],
    ['Cột Số lượng', 'Table/Grid', 'Read-only', 'Chỉ phiếu xuất bán hàng mượn', ['- Số lượng bán.']],
    ['Cột Giá niêm yết', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Định dạng 1,234,567; 0 để trống.']],
    ['Cột Giảm giá bán', 'Table/Grid', 'Read-only', 'Hiển thị', ['- = Giá niêm yết − Đơn giá bán; 0 để trống.']],
    ['Cột Đơn giá bán', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Đơn giá bán sau phân bổ giảm giá.']],
    ['Cột Thành tiền bán', 'Table/Grid', 'Read-only', 'Chỉ phiếu xuất hàng', ['- = SL thực xuất × Đơn giá bán.']],
    ['Nút Đóng', 'Button', 'Enable', 'Hiển thị', ['- Đóng popup, quay về bảng báo cáo (giữ trang, bộ lọc). Nút × góc phải tương tự.']],
    ['Nút Xem chi tiết phiếu', 'Button', 'Enable', 'Hiển thị', ['- Mở màn chi tiết phiếu xuất hàng / phiếu xuất bán hàng mượn ở tab mới.']],
]
FR.append({
    'ten': 'Xem danh sách hàng hóa của phiếu xuất', 'uc': 'uc_hanghoa',
    'qtc': 'Popup, Định dạng số.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách hàng hóa của phiếu xuất'],
        ['Mô tả', 'Popup liệt kê các mặt hàng của phiếu xuất hàng / phiếu xuất bán hàng mượn mà người dùng bấm ở cột Số chứng từ.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_DATA + '\n4. Bảng có dòng chứng từ là phiếu xuất hàng hoặc phiếu xuất bán hàng mượn.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm số phiếu ở cột Số chứng từ.\n2. Hệ thống mở popup "Danh sách hàng hóa", tải các dòng hàng của phiếu.\n3. Người dùng xem, bấm Đóng hoặc Xem chi tiết phiếu.'],
        ['Dòng sự kiện phụ', '• Lỗi tải → "Lỗi khi tải dữ liệu".\n• Phiếu không có dòng hàng → "Không có dữ liệu phù hợp."'],
    ],
    'menu_them': ' => Bấm số phiếu xuất ở cột Số chứng từ',
    'ghi_chu_layout': 'Popup Danh sách hàng hóa được mở ngay trên màn báo cáo theo đường dẫn ở trên.',
    'anh': [('06_products', 'Popup Danh sách hàng hóa của phiếu xuất hàng PXH-19789'),
            ('08_products_borrow', 'Popup Danh sách hàng hóa của phiếu xuất bán hàng mượn PXBHM-04941')],
    'ui': ui(UI6, POP_COLS),
    'ui_widths': UI6W,
    'events': [
        ['Bấm số phiếu xuất', 'Click', 'After:\n– Mở popup, tải dòng hàng của đúng phiếu đã bấm.'],
        ['Bấm Xem chi tiết phiếu', 'Click', 'After:\n– Mở màn chi tiết phiếu ở tab mới, popup vẫn mở.'],
        ['Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup; mở lại sẽ tải lại từ đầu.'],
    ],
    'them': [
        ('Mục đích thiết kế popup', [
            ('bullet', 'Trả lời câu hỏi "số Hàng hóa/Dịch vụ của phiếu xuất này gồm những mặt hàng nào, số lượng và giá bán bao nhiêu" khi đối chiếu với khách.'),
            ('bullet', 'Là popup để giữ nguyên bảng đối chiếu, bộ lọc và trang đang xem; không phải mở màn phiếu xuất.'),
            ('bullet', 'Ràng buộc khớp số: popup lấy ĐỦ mọi dòng hàng của phiếu, không phụ thuộc kỳ / phạm vi quyền. Tổng Thành tiền bán là giá bán CHƯA thuế nên có thể nhỏ hơn số Hàng hóa/Dịch vụ của phiếu trên báo cáo (số đó ghi theo công nợ, gồm thuế). Ví dụ PXH-19789: 5 × 1,390,000 = 6,950,000; báo cáo ghi 7,506,000.'),
            ('bullet', 'Từ popup người dùng chỉ xem, hoặc bấm Xem chi tiết phiếu để mở phiếu gốc; mỗi lần mở popup tải lại, không giữ trạng thái cũ.'),
        ]),
        ('Các biến thể theo con số bấm', [('variant', [
            ('Số phiếu xuất hàng (PXH-…)', 'Mọi dòng hàng của phiếu xuất hàng', 'Danh sách hàng hóa — "Phiếu xuất hàng - <số phiếu>"', 'Có cột SL đề nghị, SL thực xuất, Thành tiền bán; không có cột Số lượng'),
            ('Số phiếu xuất bán hàng mượn (PXBHM-…)', 'Mọi dòng hàng của phiếu xuất bán hàng mượn', 'Danh sách hàng hóa — "Phiếu xuất bán hàng mượn - <số phiếu>"', 'Có cột Số lượng; không có SL đề nghị, SL thực xuất, Thành tiền bán'),
        ])]),
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', [
            ('p', 'Tập dữ liệu là các dòng hàng của đúng phiếu đã bấm, xếp theo thứ tự nhập trên phiếu.'),
            ('data', [
                ('SL đề nghị / SL thực xuất', 'Phiếu xuất hàng: lấy theo lô hàng xuất của từng dòng phiếu (số lượng đề nghị và số lượng thực xuất).', '—'),
                ('Số lượng', 'Phiếu xuất bán hàng mượn: số lượng của dòng hàng.', '—'),
                ('Giá niêm yết', 'Giá niêm yết ghi trên dòng phiếu.', '—'),
                ('Đơn giá bán', 'Đơn giá sau phân bổ giảm giá ghi trên dòng phiếu.', '—'),
                ('Giảm giá bán', 'Giá niêm yết − Đơn giá bán.', '—'),
                ('Thành tiền bán', 'SL thực xuất × Đơn giá bán (chỉ phiếu xuất hàng).', '—'),
            ])]),
    ],
})

# ================================================================ 2.4 In
FR.append({
    'ten': 'In báo cáo', 'uc': 'uc_in',
    'qtc': 'In.',
    'gioi_thieu': [
        ['Tên chức năng', 'In báo cáo đối chiếu công nợ'],
        ['Mô tả', 'Xem trước và in bảng đối chiếu theo mẫu "BÁO CÁO ĐỐI SOÁT CÔNG NỢ KHÁCH HÀNG", khổ ngang, gồm MỌI trang theo bộ lọc đang áp.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_DATA],
        ['Dòng sự kiện chính', '1. Người dùng bấm In.\n2. Hệ thống mở cửa sổ "Xem trước bảng đối chiếu công nợ khách hàng": tiêu đề công ty, tên báo cáo, ngày in, thông tin lọc (Khách hàng, Số hợp đồng, Từ ngày, Đến ngày, Công ty, Phòng ban, Bộ phận, Nhân viên), bảng 12 cột (dòng Tổng cộng ngay dưới tiêu đề).\n3. Người dùng bấm In trong cửa sổ để in ra máy in.'],
        ['Dòng sự kiện phụ', '• Chưa đủ Khách hàng + Thời gian → "Vui lòng chọn khách hàng và thời gian", không mở cửa sổ.\n• Vượt 2.000 dòng → cửa sổ chỉ hiện: "Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.", ẩn nút In.\n• Thiếu mẫu in → "Không tìm thấy mẫu in".'],
    ],
    'menu_them': ' => In {icon:btn_in}',
    'ghi_chu_layout': 'Cửa sổ xem trước bản in được mở ngay trên màn báo cáo theo đường dẫn ở trên.',
    'anh': [('10_print', 'Cửa sổ Xem trước bảng đối chiếu công nợ khách hàng')],
    'ui': ui(UI6, [
        ['Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Xem trước bảng đối chiếu công nợ khách hàng', ['- Nút × đóng cửa sổ.']],
        ['Nút In', 'Button', 'Enable / Ẩn', 'Hiển thị', ['- In bản xem trước ra máy in.', '- Ẩn khi vượt trần 2.000 dòng.']],
        ['Bản xem trước', 'Label', 'Read-only', 'Theo dữ liệu', ['- Mẫu "BÁO CÁO ĐỐI SOÁT CÔNG NỢ KHÁCH HÀNG", khổ ngang, tiêu đề công ty của người in.', '- Dòng ngày: "Ngày dd Tháng mm Năm yyyy" (ngày in).', '- Bảng giống màn hình; dòng hợp đồng in đậm; ô bằng 0 để trống, KỂ CẢ dòng Tổng cộng.']],
        ['Dòng nhắc vượt trần', 'Label', 'Ẩn', 'Ẩn', ['- Chỉ hiện khi vượt 2.000 dòng (nội dung ở Dòng sự kiện phụ).']],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In (màn báo cáo)', 'Click', 'Before:\n– Thiếu Khách hàng / Thời gian → toast "Vui lòng chọn khách hàng và thời gian", dừng.\nAfter:\n– Lấy mọi dòng theo bộ lọc, điền mẫu in, mở cửa sổ xem trước.'],
        ['Bấm In (trong cửa sổ)', 'Click', 'After:\n– Gửi bản xem trước ra máy in, không mở tab mới.'],
        ['Bấm ×', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# ================================================================ 2.5 Xuất Excel
FR.append({
    'ten': 'Xuất Excel', 'uc': 'uc_xuat',
    'qtc': 'Xuất Excel.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất bảng đối chiếu ra Excel'],
        ['Mô tả', 'Xuất mọi dòng (mọi trang) theo bộ lọc đang áp ra file Excel; người dùng chọn và sắp xếp cột.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_DATA],
        ['Dòng sự kiện chính', '1. Người dùng bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Chọn trường xuất Excel" với 11 trường đã tích sẵn.\n3. Người dùng tích / bỏ tích, kéo biểu tượng ☰ đổi thứ tự, bấm Xuất file.\n4. Hệ thống tải file bang_doi_chieu_cong_no_1_khach_hang.xlsx, đóng cửa sổ, báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Chưa đủ Khách hàng + Thời gian → "Vui lòng chọn khách hàng và thời gian".\n• Bỏ chọn hết → nút Xuất file bị khoá.\n• Lỗi → "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'Cửa sổ Chọn trường xuất Excel được mở ngay trên màn báo cáo theo đường dẫn ở trên.',
    'anh': [('09_export', 'Cửa sổ Chọn trường xuất Excel')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', ['- "Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file."']],
        ['Danh sách trường', 'Checkbox', 'Enable', 'Tích tất cả', ['- 11 trường: Ngày chứng từ, Số chứng từ, Diễn giải, Số dư đầu kỳ, PS tăng - Hàng hóa/Dịch vụ, PS tăng - Điều chỉnh công nợ, PS giảm - Nhập trả lại, PS giảm - Đã thanh toán, PS giảm - Điều chỉnh công nợ, Trả lại tiền thừa, Số dư cuối kỳ.', '- Cột STT luôn có ở đầu file, không nằm trong danh sách.']],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', ['- Tích / bỏ tích mọi trường.']],
        ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn 11/11 trường', ['- Cập nhật theo số trường đang tích.']],
        ['Nút Xuất file', 'Button', 'Enable / Disable', 'Enable', ['- Khoá khi không tích trường nào hoặc đang xuất.']],
        ['Nút Đóng', 'Button', 'Enable', '–', ['- Đóng cửa sổ, không xuất.']],
        ['File Excel', 'File', '–', '–', ['- Sheet "Đối chiếu công nợ"; dòng 1 "BẢNG ĐỐI CHIẾU CÔNG NỢ KHÁCH HÀNG"; dòng 2 "Khách hàng: <Mã KH - Tên KH>" (nhiều KH cách nhau dấu ;); dòng 3 "Thời gian: dd/mm/yyyy - dd/mm/yyyy" — in đậm, căn giữa.', '- Tiêu đề 2 tầng: các trường PS tăng / PS giảm đứng liền nhau gộp dưới "Phát sinh tăng trong kỳ" / "Phát sinh giảm trong kỳ".', '- Dòng Tổng cộng ngay dưới tiêu đề, rồi dòng hợp đồng (in đậm) và chứng từ; tiêu đề cố định khi cuộn.', '- Cột số lưu dạng số, định dạng 1,234,567; ô 0 để trống (kể cả dòng Tổng cộng).']],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'Before:\n– Thiếu Khách hàng / Thời gian → "Vui lòng chọn khách hàng và thời gian", dừng.\nAfter:\n– Mở cửa sổ chọn trường.'],
        ['Tích / bỏ tích, kéo ☰', 'Change / Drag', 'After:\n– Đổi trường và thứ tự cột sẽ xuất.'],
        ['Bấm Xuất file', 'Click', 'After:\n– Lấy mọi dòng theo bộ lọc, dựng file theo trường đã chọn, tải về, đóng cửa sổ, báo "Xuất Excel thành công" (lỗi: "Lỗi khi xuất Excel").'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# ---------------------------------------------------------------- Phần 2 + 4
PERMS = [
    ('Xem báo cáo đối soát công nợ khách hàng theo tổng công ty', 'Thấy công nợ của mọi công ty; hiện đủ 4 ô Công ty, Phòng ban, Bộ phận, Nhân viên.'),
    ('Xem báo cáo đối soát công nợ khách hàng theo công ty', 'Thấy bút toán thuộc công ty đang làm việc, cộng hợp đồng do chính mình tạo; hiện ô Phòng ban, Bộ phận, Nhân viên.'),
    ('Xem báo cáo đối soát công nợ khách hàng theo phòng ban', 'Thấy bút toán của các phòng ban mình quản lý, cộng hợp đồng do chính mình tạo; hiện ô Phòng ban, Bộ phận, Nhân viên.'),
    ('Xem báo cáo đối soát công nợ khách hàng theo bộ phận', 'Thấy bút toán của các bộ phận mình quản lý, cộng hợp đồng do chính mình tạo; hiện ô Bộ phận, Nhân viên.'),
    ('(Không có quyền nào)', 'Vẫn mở được màn; chỉ thấy bút toán của hợp đồng do chính mình tạo; không có ô lọc tổ chức.'),
]
FUNCS = ['FR-01 Xem báo cáo đối chiếu công nợ', 'FR-02 Tìm kiếm và lọc', 'FR-03 Xem danh sách hàng hóa của phiếu xuất',
         'FR-04 In báo cáo', 'FR-05 Xuất Excel']

S = {
    'ten': TEN,
    'menu': [('Bán hàng', 'menu_phanhe'), ('Báo cáo', 'menu_nhom'), ('Báo cáo công nợ', 'menu_nhomcon'), ('Đối chiếu công nợ 1 KH', 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu màn báo cáo.',
        'Làm rõ cách tính từng cột số liệu ở 3 loại dòng (Tổng cộng, hợp đồng, chứng từ), phạm vi dữ liệu theo 4 cấp quyền, tác động của từng ô lọc lên dòng Tổng cộng, và các điểm số liệu cố ý không cộng khớp giữa các loại dòng.',
    ],
    'thuat_ngu': [
        ['Công nợ phải thu', 'Số tiền khách hàng còn phải trả công ty, ghi trên tài khoản phải thu khách hàng (131 và tài khoản con).'],
        ['Bút toán', 'Một dòng ghi Nợ hoặc ghi Có vào sổ công nợ do một chứng từ sinh ra khi hạch toán.'],
        ['Ngày hạch toán', 'Ngày chứng từ được ghi sổ; là ngày dùng để xếp kỳ.'],
        ['Kỳ', 'Từ ngày đến hết Đến ngày của ô Thời gian.'],
        ['Số dư đầu kỳ', 'Công nợ còn phải thu trước Từ ngày.'],
        ['Phát sinh tăng / giảm', 'Các khoản làm tăng / giảm công nợ trong kỳ.'],
        ['Phiếu điều chỉnh công nợ', 'Phiếu kế toán điều chỉnh tăng (ghi Nợ) hoặc giảm (ghi Có) công nợ.'],
        ['Dòng hợp đồng', 'Dòng chữ đậm, mỗi hợp đồng của khách hàng có phát sinh 1 dòng.'],
        ['Dòng chứng từ', 'Dòng N.i dưới dòng hợp đồng, mỗi chứng từ phát sinh trong kỳ 1 dòng.'],
        ['Phạm vi dữ liệu', 'Phần số liệu người dùng được xem theo cấp quyền (tổng công ty / công ty / phòng ban / bộ phận / của mình).'],
    ],
    'quyen_truoc': [
        'Màn KHÔNG chặn quyền vào: mọi người dùng đăng nhập đều thấy mục menu và mở được màn. 4 quyền của nhóm "Bảng đối chiếu công nợ 1 khách hàng" chỉ mở rộng PHẠM VI DỮ LIỆU. Người có nhiều quyền được tính theo cấp cao nhất (tổng công ty > công ty > phòng ban > bộ phận).',
    ],
    'quyen_rows': [list(p) for p in PERMS],
    'ma_tran': [['Chức năng', 'Tổng công ty', 'Công ty', 'Phòng ban', 'Bộ phận', 'Không quyền']] +
               [[f, 'Có', 'Có', 'Có', 'Có', 'Có'] for f in FUNCS],
    'ma_tran_widths': [2.6, 0.9, 0.8, 0.9, 0.8, 0.9],
    'quyen_sau': [
        'Mọi chức năng đều dùng được với mọi cấp; khác nhau ở phạm vi số liệu (BR-02). Phạm vi áp cho mọi con số: dòng hợp đồng, dòng chứng từ, dòng Tổng cộng, Số dư đầu kỳ, file Excel và bản in.',
        '"Hợp đồng do mình tạo" = bút toán có người tạo hợp đồng là người đang xem. "Công ty đang làm việc" = công ty người dùng đang chọn khi đăng nhập.',
    ],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Điều kiện bắt buộc', [
            '– Phải chọn đủ Thời gian (Từ ngày, Đến ngày) và ít nhất 1 Khách hàng mới tải số liệu, In, Xuất Excel.',
            '– Chưa đủ: bảng hiện "Chọn thời gian và khách hàng để xem bảng đối chiếu."; bấm Tìm kiếm báo đỏ dưới ô; bấm In / Xuất Excel báo "Vui lòng chọn khách hàng và thời gian".',
            '– Đến ngày không được nhỏ hơn Từ ngày.'], ['Xem báo cáo', 'Tìm kiếm và lọc', 'In', 'Xuất Excel']),
        ('BR-02', 'Phạm vi dữ liệu 4 cấp', [
            '– Tổng công ty: không giới hạn.',
            '– Công ty: bút toán thuộc công ty đang làm việc HOẶC thuộc hợp đồng do mình tạo.',
            '– Phòng ban / Bộ phận: bút toán thuộc phòng ban / bộ phận mình quản lý HOẶC hợp đồng do mình tạo.',
            '– Không quyền: chỉ bút toán của hợp đồng do mình tạo.',
            '– Nhiều quyền: lấy cấp cao nhất.'], ['Mọi chức năng hiện số liệu']),
        ('BR-03', 'Kỳ báo cáo', [
            '– Xếp kỳ theo NGÀY HẠCH TOÁN của bút toán.',
            '– Trong kỳ: từ Từ ngày đến hết ngày Đến ngày (tính cả 2 đầu). Đầu kỳ: trước Từ ngày. Sau Đến ngày: không tính.',
            '– Chứng từ chưa hạch toán (chưa ghi sổ) không lên báo cáo.'], ['Xem báo cáo']),
        ('BR-04', 'Chứng từ nguồn của từng cột', [
            '– Hàng hóa/Dịch vụ: phiếu xuất hàng, phiếu xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ bảo hành - sửa chữa (Nợ − Có), cộng ghi Nợ của khai báo công nợ đầu kỳ.',
            '– Điều chỉnh công nợ tăng / giảm: ghi Nợ / ghi Có của phiếu điều chỉnh công nợ.',
            '– Nhập trả lại: phiếu nhập hàng khách trả lại (Có − Nợ).',
            '– Đã thanh toán: ghi Có của phiếu thu, phiếu báo có, khai báo công nợ đầu kỳ.',
            '– Trả lại tiền thừa: ghi Nợ của phiếu chi, ủy nhiệm chi.',
            '– Bút toán của loại chứng từ khác: chỉ vào Số dư đầu kỳ (nếu trước kỳ), không vào cột phát sinh nào.'], ['Xem báo cáo', 'In', 'Xuất Excel']),
        ('BR-05', 'Hợp đồng lên bảng và phân trang', [
            '– Chỉ hợp đồng có ít nhất 1 trong 7 cột phát sinh khác 0 (so phần nguyên); hợp đồng toàn số 0 bị bỏ TRƯỚC khi chia trang nên không có trang trống, STT liên tục.',
            '– Bút toán chưa gắn hợp đồng hoặc hợp đồng không xác định được: không thành dòng nhưng vẫn cộng vào dòng Tổng cộng.',
            '– Phân trang theo hợp đồng (mặc định 10), các chứng từ của 1 hợp đồng luôn cùng trang.'], ['Xem báo cáo']),
        ('BR-06', 'Số dư đầu kỳ', [
            '– Chỉ tính ở dòng Tổng cộng; dòng hợp đồng và chứng từ để trống.',
            '– Lọc Công ty / Phòng ban / Bộ phận theo đơn vị ghi trên bút toán (khác các cột phát sinh: theo người tạo hợp đồng — BR-10).'], ['Xem báo cáo']),
        ('BR-07', 'Số dư cuối kỳ ở 3 loại dòng', [
            '– Tổng cộng: đầu kỳ + HH/DV + ĐCCN tăng − Nhập trả lại − Đã thanh toán − ĐCCN giảm + Trả lại tiền thừa.',
            '– Dòng hợp đồng: HH/DV − Nhập trả lại − Đã thanh toán + Trả lại tiền thừa (không tính đầu kỳ, không tính 2 cột ĐCCN).',
            '– Dòng chứng từ: cộng dồn trong hợp đồng theo công thức của dòng hợp đồng.',
            '– Hệ quả: tổng Số dư cuối kỳ các dòng hợp đồng KHÁC dòng Tổng cộng; hợp đồng đã được điều chỉnh giảm hết vẫn hiện số dư.'], ['Xem báo cáo', 'In', 'Xuất Excel']),
        ('BR-08', 'Dòng chứng từ', [
            '– Chứng từ phát sinh trong kỳ của hợp đồng, gom 1 dòng / chứng từ, bỏ chứng từ toàn 0.',
            '– Lấy theo bộ tài khoản phải thu cố định riêng, không lọc lại theo khách hàng.',
            '– Xếp theo ngày hạch toán, cùng ngày theo thời điểm tạo.',
            '– Số chứng từ phiếu xuất / xuất bán hàng mượn / nhập trả kèm số phiếu yêu cầu trong ngoặc.'], ['Xem báo cáo']),
        ('BR-09', 'Số hợp đồng và ô tìm nhanh', [
            '– Số hợp đồng: lọc gần đúng; áp cho dòng hợp đồng, dòng Tổng cộng và Số dư đầu kỳ.',
            '– Ô tìm nhanh: giữ hợp đồng có số hợp đồng hoặc số chứng từ chứa từ khoá; chỉ thu hẹp danh sách hợp đồng, KHÔNG đổi dòng Tổng cộng.'], ['Tìm kiếm và lọc']),
        ('BR-10', 'Lọc Công ty / Phòng ban / Bộ phận / Nhân viên', [
            '– Theo hồ sơ HIỆN TẠI của người tạo hợp đồng (Nhân viên = người tạo hợp đồng); mỗi ô chọn được nhiều giá trị.',
            '– Chỉ áp được cho hợp đồng bán hàng và hợp đồng dịch vụ sửa chữa - bảo dưỡng - bảo trì: chọn bất kỳ ô nào thì loại khỏi bảng và khỏi Tổng cộng mọi loại hợp đồng khác và bút toán chưa gắn hợp đồng.'], ['Tìm kiếm và lọc']),
        ('BR-11', 'Định dạng số', [
            '– Số tiền dạng 1,234,567, không phần lẻ, số âm có dấu "-".',
            '– Ô bằng 0 để trống; riêng dòng Tổng cộng trên màn in "0". File Excel và bản in để trống cả ở dòng Tổng cộng.'], ['Xem báo cáo', 'In', 'Xuất Excel']),
        ('BR-12', 'In / Xuất Excel', [
            '– Lấy MỌI dòng (mọi trang) theo bộ lọc đang áp, kể cả ô tìm nhanh.',
            '– In tối đa 2.000 dòng; vượt thì không in, gợi ý dùng Xuất Excel.'], ['In', 'Xuất Excel']),
        ('BR-13', 'Ghi nhớ bộ lọc', [
            '– Rời màn rồi quay lại trong 10 phút: giữ bộ lọc.',
            '– Tải lại trang (F5) hoặc bấm Làm mới: mọi ô về trống.'], ['Tìm kiếm và lọc']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây dùng chung cách tính / phạm vi công nợ với báo cáo này, hoặc là chứng từ nguồn sinh ra số liệu (mở được từ cột Số chứng từ).',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng đã đăng nhập',
    'mains': [('FR-01', 'Xem báo cáo đối chiếu công nợ', 'view'), ('FR-04', 'In báo cáo', 'io'), ('FR-05', 'Xuất Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc', 'view'), ('FR-03', 'Xem danh sách hàng hóa của phiếu xuất', 'view')],
    'rieng': [('FR-03', 'Xem danh sách hàng hóa của phiếu xuất', 'view', 'uc_hanghoa'),
              ('FR-04', 'In báo cáo', 'io', 'uc_in'), ('FR-05', 'Xuất Excel', 'io', 'uc_xuat')],
}


# ---------------------------------------------------------------- dựng tài liệu (chép _lib_win.build_srs + mục báo cáo)
def build_srs_report(scr, S, out):
    w = QgWriter(L.SRS_TPL, SRS_ROLES, body_from=10, cover_replace={'Danh mục quốc gia': S['ten']})

    def img(path, cap, width=6.2):
        w.image(path, width=width, caption=cap)
        L._keep_next(w)

    def sub(text):
        w.raw('sub', text)
        L._keep_with_next(w)

    menu = []
    for i, (text, icon) in enumerate(S['menu']):
        menu.append(('Phân hệ ' if i == 0 else ' => ') + text + ' ')
        if icon:
            menu.append(scr.ic(icon, 0.24))

    h1_trang_moi(w, 'Phần 1. Giới thiệu')
    w.h2('1 Mục đích')
    w.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s, nhằm:' % S['ten'])
    for b in S['muc_dich']:
        w.bullet(b)
    w.h2('2 Thuật ngữ và viết tắt')
    w.table([['Thuật ngữ', 'Mô tả']] + S['thuat_ngu'], widths=[1.3, 3])

    h1_trang_moi(w, 'Phần 2. Phân quyền')
    w.h2('1 Danh sách quyền')
    for p in S['quyen_truoc']:
        w.p(p)
    w.table([['Tên quyền', 'Phạm vi dữ liệu trên màn hình']] + S['quyen_rows'], widths=[2.0, 3])
    w.h2('2 Ma trận phân quyền')
    w.table(S['ma_tran'], widths=S.get('ma_tran_widths'))
    for p in S.get('quyen_sau', []):
        w.p(p)

    h1_trang_moi(w, 'Phần 3. Đặc tả chi tiết theo từng chức năng')
    w.h2('1 Sơ đồ UML tổng quan')
    img(os.path.join(scr.uml, 'overview.png'), 'Sơ đồ Use Case tổng quan màn %s' % S['ten'], 6.3)
    w.h2('2 Đặc tả chi tiết từng chức năng')
    for i, fr in enumerate(S['fr']):
        assert fr.get('ui') and fr.get('events'), fr['ten']
        n = '2.%d' % (i + 1)
        w.h3('%s %s' % (n, fr['ten']))
        k = 0
        if fr.get('uc'):
            k += 1
            sub('%s.%d Biểu đồ Usecase' % (n, k))
            img(os.path.join(scr.uml, fr['uc'] + '.png'), 'Biểu đồ Use Case — %s' % fr['ten'], 6.2)
        k += 1
        sub('%s.%d Giới thiệu' % (n, k))
        w.clone_texts('qtc', ['Quy tắc chung: ', 'Áp dụng SRS Các quy tắc chung ', QTC_LINK,
                              ' - %s Chỉ bổ sung quy tắc riêng của %s.' % (fr['qtc'], S['ten'])])
        w.table([['Mục', 'Nội dung']] + fr['gioi_thieu'], widths=[1, 3.2])
        k += 1
        sub('%s.%d Layout màn hình' % (n, k))
        w.p('Đường dẫn màn hình:')
        extra = scr.segs(fr['menu_them']) if fr.get('menu_them') else []
        w.raw('menu_b', 'Menu: ')
        w.raw('menu', menu + extra)
        if fr.get('ghi_chu_layout'):
            w.p(fr['ghi_chu_layout'])
        for name, cap in fr.get('anh', []):
            img(scr.shot(name), cap, L._fit_width(scr.shot(name)))
        k += 1
        sub('%s.%d Mô tả chi tiết giao diện' % (n, k))
        w.table(fr['ui'], widths=fr.get('ui_widths'))
        k += 1
        sub('%s.%d Danh sách event và xử lý event' % (n, k))
        w.table([['STT', 'Event', 'Loại event', 'Xử lý event']] +
                [[str(j + 1)] + e for j, e in enumerate(fr['events'])], widths=[0.5, 1.4, 0.8, 3.5])
        for title, items in fr.get('them', []):
            k += 1
            sub('%s.%d %s' % (n, k, title))
            for it in items:
                kind = it[0]
                if kind == 'p':
                    w.p(it[1])
                elif kind == 'bullet':
                    w.bullet(it[1])
                elif kind == 'data':
                    w.table([['STT', 'Chỉ tiêu / Cột', 'Cách lấy dữ liệu', 'Nội dung icon ⓘ']] +
                            [[str(j + 1)] + list(r) for j, r in enumerate(it[1])], widths=[0.55, 1.3, 2.9, 2.0])
                elif kind == 'popup':
                    w.table([['STT', 'Bấm vào', 'Popup mở ra', 'Mục đích thiết kế', 'Dữ liệu hiển thị']] +
                            [[str(j + 1)] + list(r) for j, r in enumerate(it[1])], widths=[0.55, 1.55, 1.4, 1.6, 1.65])
                elif kind == 'variant':
                    w.table([['STT', 'Con số / vị trí bấm', 'Tập dòng hiển thị', 'Tiêu đề popup', 'Ô lọc ẩn / cố định']] +
                            [[str(j + 1)] + list(r) for j, r in enumerate(it[1])], widths=[0.55, 1.4, 1.5, 1.6, 1.7])

    h1_trang_moi(w, 'Phần 4. Quy tắc nghiệp vụ')
    w.p('**Quy tắc áp dụng:** Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung '
        'SRS_Các quy tắc chung_VN_1.0. Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc '
        'đã có trong SRS quy tắc chung.' % S['ten'])
    j = lambda v: '\n'.join(v) if isinstance(v, (list, tuple)) else v  # noqa: E731
    rows = [['STT', 'Mã quy tắc', 'Tên quy tắc', 'Mô tả', 'Phạm vi áp dụng']]
    for i, q in enumerate(S['quy_tac'], 1):
        assert q[0] == 'BR-%02d' % i, q[0]
        rows.append([str(i), q[0], q[1], j(q[2]), j(q[3])])
    w.table(rows, widths=[0.5, 0.85, 1.3, 2.75, 1.2])

    p5 = S['phan5']
    h1_trang_moi(w, 'Phần 5. Bảng danh sách các màn hình dùng chung / tham chiếu dữ liệu')
    w.p(p5['cau_dan'])
    w.table([['STT', 'Nhóm', 'Màn hình', 'Đường dẫn']] +
            [[str(i + 1)] + list(r) for i, r in enumerate(p5['rows'])], widths=[0.5, 1.0, 2.6, 2.3])

    w.rebuild_toc(levels=(1, 2, 3))
    L._exclude_toc_heading(w)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    L._table_runs_13(w)
    w.save(out)
    L.force_times_new_roman(out)
    return out


if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', build_srs_report(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)

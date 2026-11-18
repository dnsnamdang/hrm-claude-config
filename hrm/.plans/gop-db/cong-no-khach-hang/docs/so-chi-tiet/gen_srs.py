# -*- coding: utf-8 -*-
"""SRS - Sổ chi tiết công nợ phải thu khách hàng (form Danh mục quốc gia + quy tắc màn BÁO CÁO của skill srs-documenter).

Khuôn: sale-customer-debt-reports/docs/compare/gen_srs.py (đã duyệt) + danh-muc-kho/docs/_lib_win.py (KHÔNG sửa lib dùng chung).
Hàm dựng `build_srs_report` chép từ màn mẫu (có thêm mục "Cách lấy dữ liệu và giải thích chỉ tiêu", "Danh sách popup mở từ số liệu").

Nguồn (code HRM hiện tại, nhánh develop):
  FE hrm-client/pages/finance/customer-ledger-details/{index.vue, components/constants.js}, components/subsystem-menu/finance.js,
     components/V2BaseCompanyDepartmentFilter.vue, utils/filterRequiredErrors.js, utils/mixins/{filterStateMixin, reportPrintPreviewMixin}.js,
     utils/export/listExportFile.js, utils/invoiceable-link.js, utils/contract-link.js,
     pages/finance/customer-debt-balances/components/constants.js (lối vào từ Bảng cân đối)
  BE Modules/Finance/Http/Controllers/V1/CustomerLedgerDetailController.php (+ Concerns/ValidatesAccountDebtFilters.php),
     Services/CustomerDebt/CustomerLedgerDetailService.php, Services/AccountDebt/{PartnerLedgerService, AccountLedgerService,
     Concerns/AccountDebtCommon}.php; quyền: app/Support/Permissions/Catalog/accounting.php
Ảnh: hdsd_shots/ (capture.js, dev-hrm 18/11/2026).
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(GOPDB, 'danh-muc-kho', 'docs'))
import _lib_win as L  # noqa: E402
from _lib_win import QgWriter, SRS_ROLES, QTC_LINK, h1_trang_moi  # noqa: E402

TEN = 'Sổ chi tiết công nợ phải thu khách hàng'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
QUYEN = 'Xem sổ chi tiết công nợ phải thu khách hàng'
Q = 'Người dùng có quyền "%s" (mức Công ty hoặc Tổng công ty)' % QUYEN
DK = '1. Người dùng đăng nhập thành công.\n2. Có quyền "%s" (BR-02).' % QUYEN
DK_DATA = DK + '\n3. Đã chọn Tài khoản, Khách hàng và Thời gian (Từ ngày, Đến ngày).'
HOAC = 'Hoặc: từ màn Bảng cân đối phát sinh công nợ khách hàng, bấm mã khách hàng ở một dòng — màn Sổ chi tiết mở ở tab mới với bộ lọc của dòng đó.'

UI6 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả']
UI6W = [0.5, 1.35, 0.85, 0.8, 0.95, 2.75]
UI7 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả']
UI7W = [0.45, 1.2, 0.85, 0.8, 1.0, 0.85, 2.6]


def ui(header, rows):
    return [header] + [[str(i + 1)] + r for i, r in enumerate(rows)]


TIP_TRANG = ('Sổ chi tiết từng bút toán công nợ của một khách hàng trên một tài khoản: số dư đầu kỳ, phát sinh Nợ / Có trong kỳ, '
             'số dư cuối kỳ. Quyền xem theo tổng công ty hoặc công ty (công ty: sổ của công ty mình và các hợp đồng do mình tạo).')
NUM = '- Số theo định dạng 1,234,567.89 (tối đa 2 chữ số lẻ, bỏ số 0 thừa).'
NUM2 = '- Ô không có giá trị để trống.'
MSG_THIEU = 'Vui lòng chọn tài khoản, khách hàng và thời gian'

# ---------------------------------------------------------------- Phần 5 (dò code FE/BE + menu 18/11/2026)
P5 = [
    ('Tài chính', 'Bảng cân đối phát sinh công nợ khách hàng (bấm mã khách hàng mở Sổ chi tiết này cùng bộ lọc; cùng sổ công nợ, cùng phạm vi)', 'Tài chính => Kế toán công nợ => Khách hàng'),
    ('Tài chính', 'Sổ chi tiết công nợ phải trả nhà cung cấp (cùng khung sổ chi tiết, cùng cách tính đầu kỳ / phát sinh / cuối kỳ)', 'Tài chính => Kế toán công nợ => Nhà cung cấp'),
    ('Tài chính', 'Sổ chi tiết công nợ nhân viên (cùng khung sổ chi tiết)', 'Tài chính => Kế toán công nợ => Nhân viên'),
    ('Tài chính', 'Phiếu xuất hàng (chứng từ ghi Nợ công nợ phải thu; mở từ cột Số chứng từ)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ('Tài chính', 'Phiếu xuất bán hàng mượn (chứng từ ghi Nợ công nợ phải thu)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng'),
    ('Tài chính', 'Phiếu nhập hàng (hàng khách trả lại — ghi Có công nợ)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
    ('Tài chính', 'Phiếu thu, Phiếu báo có (khách thanh toán — ghi Có công nợ)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu chi, Phiếu ủy nhiệm chi (trả lại tiền khách — ghi Nợ công nợ)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu kế toán (bù trừ / điều chỉnh công nợ)', 'Tài chính => Sổ tổng hợp => Sổ tổng hợp'),
    ('Tài chính', 'Khai báo đầu kỳ công nợ (số dư đầu kỳ theo khách hàng - hợp đồng)', 'Tài chính => Khai báo đầu kỳ'),
    ('Bán hàng', 'Hợp đồng bán hàng (mở từ cột Đơn hàng/Hợp đồng)', 'Bán hàng => Bán hàng => Hợp đồng bán hàng'),
]

FR = []

# ================================================================ 2.1 Xem sổ chi tiết
COT = [
    ['Tiêu đề trang', 'Label', 'Hiển thị', TEN, ['- Ở thanh trên cùng, kèm icon ⓘ.', '- Icon ⓘ: "%s"' % TIP_TRANG]],
    ['Tiêu đề bảng', 'Label', 'Hiển thị', TEN, ['- Tiêu đề khối bảng kết quả.']],
    ['Nút In', 'Button', 'Enable', 'Hiển thị', ['- Mở cửa sổ xem trước bản in theo bộ lọc đã áp (mục 2.3).', '- Thiếu ô bắt buộc: báo "%s", mở khung lọc và tô đỏ ô thiếu.' % MSG_THIEU]],
    ['Nút Xuất Excel', 'Button', 'Enable / Disable', 'Hiển thị', ['- Tải ngay file Excel theo bộ lọc đã áp (mục 2.4); không có cửa sổ chọn cột.', '- Thiếu ô bắt buộc: báo "%s".' % MSG_THIEU, '- Bị khoá trong lúc đang xuất; bên cạnh hiện tiến độ "Đang chuẩn bị dữ liệu…", "Đã tải a/b dòng…", "Đang dựng file N dòng…".']],
    ['Bảng sổ chi tiết', 'Table/Grid', 'Read-only', 'Lời nhắc', [
        '- Mẫu VNĐ: 11 cột — STT, Đơn hàng/Hợp đồng, Ngày hạch toán, Số chứng từ, NVKD, Phòng ban, Ghi chú, Phát sinh nợ, Phát sinh có, Tài khoản đối ứng (Tài khoản, Tên tài khoản).',
        '- Mẫu Ngoại tệ (Loại tiền = Ngoại tệ): thay 2 cột phát sinh bằng Loại tiền, Số phát sinh ngoại tệ (Nợ, Có), Tỷ giá, Số phát sinh VNĐ (Nợ, Có) — 15 cột.',
        '- Thứ tự: 3 dòng tổng (Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ; nền xám, chữ đậm) rồi các dòng bút toán.',
        '- Tiêu đề bảng dính khi cuộn dọc.',
        '- Thứ tự cố định theo ngày hạch toán rồi thời điểm tạo bút toán; tiêu đề cột không bấm sắp xếp được, không có tùy chỉnh cột.',
        '- Chưa chọn đủ ô bắt buộc: "Chọn tài khoản, khách hàng và thời gian để xem sổ chi tiết."',
        '- Đang tải: "Đang tải dữ liệu..."',
        '- Không có bút toán nào: vẫn hiện 3 dòng tổng, dưới là "Không có dữ liệu phù hợp bộ lọc."']],
    ['Dòng Số dư đầu kỳ', 'Table/Grid', 'Read-only', 'Theo dữ liệu', ['- Nhãn ở ô gộp 7 cột đầu. Dư dương ghi ở cột Phát sinh nợ, dư âm ghi (số tuyệt đối) ở cột Phát sinh có; bằng 0 thì để trống cả hai.', '- Mẫu Ngoại tệ: mỗi loại tiền 1 bộ 3 dòng tổng, cột Loại tiền ghi tên loại tiền.']],
    ['Dòng Tổng phát sinh', 'Table/Grid', 'Read-only', 'Theo dữ liệu', ['- Tổng ghi Nợ (cột nợ) và tổng ghi Có (cột có) trong kỳ, không bù trừ.']],
    ['Dòng Số dư cuối kỳ', 'Table/Grid', 'Read-only', 'Theo dữ liệu', ['- = Số dư đầu kỳ + Tổng phát sinh nợ − Tổng phát sinh có; dương ở cột nợ, âm ở cột có.', '- 3 dòng tổng không đổi khi chuyển trang.']],
    ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', ['- 1, 2, 3… liên tục qua các trang.']],
    ['Cột Đơn hàng/Hợp đồng', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Số hợp đồng ghi trên bút toán, chữ dạng liên kết: bấm mở màn hợp đồng ở tab mới.', '- Bút toán không gắn hợp đồng: để trống.']],
    ['Cột Ngày hạch toán', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Ngày ghi sổ của chứng từ, dạng dd/mm/yyyy.']],
    ['Cột Số chứng từ', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Số chứng từ sinh bút toán (PXH-…, TPE.PKT…, TPE.PBC…). Bấm mở màn chi tiết chứng từ ở tab mới; loại chứng từ chưa có màn thì hiện chữ thường.']],
    ['Cột NVKD', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Họ tên người tạo hợp đồng của bút toán; không gắn hợp đồng thì trống.']],
    ['Cột Phòng ban', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Phòng ban hiện tại của người tạo hợp đồng.']],
    ['Cột Ghi chú', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Ghi chú của chứng từ (phiếu xuất hàng, phiếu nhập hàng, phiếu thu, phiếu ủy nhiệm chi, phiếu báo có); loại chứng từ khác để trống. Dài thì xuống dòng.']],
    ['Cột Phát sinh nợ', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Số tiền quy đổi VNĐ của bút toán ghi Nợ; bút toán ghi Có để trống.', NUM, NUM2]],
    ['Cột Phát sinh có', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Số tiền quy đổi VNĐ của bút toán ghi Có; bút toán ghi Nợ để trống.', NUM, NUM2]],
    ['Cột Loại tiền (mẫu Ngoại tệ)', 'Table/Grid', 'Read-only', 'Chỉ mẫu Ngoại tệ', ['- Tên loại tiền của bút toán (vd USD).']],
    ['Cột Số phát sinh ngoại tệ - Nợ / Có', 'Table/Grid', 'Read-only', 'Chỉ mẫu Ngoại tệ', ['- Số nguyên tệ của bút toán, đặt ở cột Nợ hoặc Có theo chiều ghi sổ.', NUM, NUM2]],
    ['Cột Tỷ giá', 'Table/Grid', 'Read-only', 'Chỉ mẫu Ngoại tệ', ['- Tỷ giá ghi trên bút toán.']],
    ['Cột Số phát sinh VNĐ - Nợ / Có', 'Table/Grid', 'Read-only', 'Chỉ mẫu Ngoại tệ', ['- Số quy đổi VNĐ của bút toán.', NUM, NUM2]],
    ['Cột Tài khoản đối ứng - Tài khoản', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Số hiệu các tài khoản đối ứng của bút toán, cách nhau dấu phẩy (vd "5111, 33311").']],
    ['Cột Tài khoản đối ứng - Tên tài khoản', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Tên các tài khoản đối ứng tương ứng, cách nhau dấu phẩy.']],
    ['Chân bảng', 'Label', 'Hiển thị', 'Ẩn khi không có dữ liệu', ['- "Hiển thị a–b / N bút toán": N = số bút toán trong kỳ theo bộ lọc (không tính 3 dòng tổng).']],
    ['Ô Số dòng/trang', 'Dropdown', 'Enable', '10', ['- Lựa chọn: 10, 20, 50, 100 bút toán / trang.', '- Đổi số dòng → quay về trang 1.']],
    ['Phân trang', 'Button', 'Enable', 'Trang 1', ['- «, ‹, số trang, ›, »; chuyển trang giữ bộ lọc và 3 dòng tổng.']],
]

DATA_MAIN = [
    ('Tập dữ liệu / thời điểm số liệu', 'Bút toán đã ghi sổ của khách hàng đã chọn trên tài khoản đã chọn và các tài khoản con TRỰC TIẾP của nó (vd chọn 131 thì lấy 131, 1311, 1312, 1313), sau khi áp phạm vi quyền (BR-02) và mọi ô lọc. Loại tiền VNĐ: chỉ bút toán VNĐ; Ngoại tệ: chỉ bút toán khác VNĐ. Đọc tại thời điểm tải (không lưu sẵn).', '—'),
    ('Trong kỳ / đầu kỳ', 'Trong kỳ: ngày hạch toán từ đầu ngày Từ ngày đến hết ngày Đến ngày. Đầu kỳ: ngày hạch toán trước Từ ngày.', '—'),
    ('Số dư đầu kỳ', 'Tổng ghi Nợ − Tổng ghi Có (số quy đổi VNĐ) của các bút toán đầu kỳ, áp ĐÚNG bộ lọc của danh sách (kể cả ô tìm nhanh, Số chứng từ, Đơn hàng/Hợp đồng, Tài khoản đối ứng, Số tiền). Dương → cột nợ, âm → cột có.', '(chung ⓘ tiêu đề trang)'),
    ('Tổng phát sinh', 'Tổng ghi Nợ và tổng ghi Có (số quy đổi VNĐ) của mọi bút toán trong kỳ theo bộ lọc, trên TOÀN bộ kỳ (không phụ thuộc trang).', '—'),
    ('Số dư cuối kỳ', 'Số dư đầu kỳ + Tổng phát sinh nợ − Tổng phát sinh có, làm tròn 2 chữ số lẻ.', '—'),
    ('Dòng tổng mẫu Ngoại tệ', 'Tính riêng cho TỪNG loại tiền: cột ngoại tệ cộng số nguyên tệ, cột VNĐ cộng số quy đổi; mỗi loại tiền 3 dòng.', '—'),
    ('Dòng bút toán', 'Mỗi bút toán trong kỳ 1 dòng (không gom theo chứng từ — 1 chứng từ có thể ra nhiều dòng, vd phiếu xuất hàng có dòng doanh thu và dòng giảm giá). Xếp theo ngày hạch toán, cùng ngày theo thời điểm tạo bút toán.', '—'),
    ('Phát sinh nợ / Phát sinh có', 'Số quy đổi VNĐ của bút toán, đặt vào cột nợ hoặc có theo chiều ghi sổ. Mẫu Ngoại tệ thêm số nguyên tệ (chỉ bút toán khác VNĐ) và tỷ giá.', '—'),
    ('NVKD / Phòng ban', 'Người tạo hợp đồng ghi trên bút toán và phòng ban HIỆN TẠI trong hồ sơ của người đó.', '—'),
    ('Ghi chú', 'Ghi chú chung của chứng từ, chỉ với 5 loại: phiếu xuất hàng, phiếu nhập hàng, phiếu thu, phiếu ủy nhiệm chi, phiếu báo có.', '—'),
    ('Tài khoản đối ứng', 'Các tài khoản đối ứng của bút toán (không trùng số hiệu), nối bằng dấu phẩy theo thứ tự ghi.', '—'),
    ('Ràng buộc khớp số', '- Số dư cuối kỳ = Số dư đầu kỳ + Tổng phát sinh nợ − Tổng phát sinh có.\n- Tổng phát sinh nợ = cộng cột Phát sinh nợ của mọi bút toán ở mọi trang (tương tự cột có).\n- Cùng tài khoản, khách hàng, kỳ, loại tiền thì số khớp với dòng của khách hàng đó trên Bảng cân đối phát sinh công nợ khách hàng.', '—'),
    ('Chân bảng "Hiển thị a–b / N bút toán"', 'N = số bút toán trong kỳ theo bộ lọc.', '—'),
]

POPUP_MAIN = [
    ('Số hợp đồng ở cột Đơn hàng/Hợp đồng', 'Không phải popup — mở màn chi tiết hợp đồng ở tab mới', 'Xem hợp đồng gốc của bút toán', 'Hợp đồng tương ứng; loại chưa có màn thì hiện chữ thường'),
    ('Số chứng từ ở cột Số chứng từ', 'Không phải popup — mở màn chi tiết chứng từ ở tab mới', 'Kiểm tra chứng từ gốc tạo ra bút toán', 'Đúng chứng từ của dòng'),
    ('Ô số tiền / dòng tổng', 'Không bấm được', '—', '—'),
]

FR.append({
    'ten': 'Xem sổ chi tiết công nợ',
    'qtc': 'Màn Báo cáo, Phân trang, Định dạng số.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem sổ chi tiết công nợ phải thu khách hàng'],
        ['Mô tả', 'Hiển thị từng bút toán công nợ của một khách hàng trên một tài khoản trong kỳ, kèm Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ; xem theo VNĐ hoặc Ngoại tệ. Màn chỉ đọc.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu; bảng hiện "Chọn tài khoản, khách hàng và thời gian để xem sổ chi tiết.", chưa tải số liệu.\n2. Người dùng chọn Tài khoản, Khách hàng, Thời gian (mục 2.2).\n3. Hệ thống tính số liệu theo phạm vi quyền và bộ lọc, hiện 3 dòng tổng và trang 1 gồm 10 bút toán.\n4. Chân bảng ghi "Hiển thị a–b / N bút toán".'],
        ['Dòng sự kiện phụ', '• Mở từ Bảng cân đối phát sinh công nợ khách hàng: bộ lọc điền sẵn theo dòng đã bấm, tự tải số liệu.\n• Không có bút toán trong kỳ: 3 dòng tổng vẫn hiện, dưới là "Không có dữ liệu phù hợp bộ lọc.".\n• Lỗi khi lấy dữ liệu → "Lỗi khi tải dữ liệu".\n• Đổi bộ lọc liên tục: chỉ hiện kết quả của lần lọc mới nhất.\n• Chuyển trang / đổi số dòng: không tính lại 3 dòng tổng.\n• Phiên đăng nhập hết hạn: hệ thống chuyển về màn đăng nhập (quy tắc chung), không hiện số liệu cũ.'],
        ['Yêu cầu đặc biệt', 'Trên môi trường thử nghiệm, 1 trang (khách hàng 73 bút toán, kỳ 10 tháng) tải khoảng 1 giây; khách hàng có số dư lớn khoảng 2 giây.'],
    ],
    'anh': [('01_empty', 'Màn Sổ chi tiết công nợ phải thu khách hàng lúc mới mở (chưa chọn bộ lọc)'),
            ('03_report', 'Sổ chi tiết có số liệu (TK 131, khách hàng 14TQUPCA-2, 01/01/2026 – 31/10/2026, VNĐ)'),
            ('06_foreign', 'Mẫu Ngoại tệ: khách hàng có bút toán USD')],
    'ui': ui(UI6, COT),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Không có quyền "%s" → hệ thống báo không có quyền, không tải danh mục và số liệu.\nAfter:\n– Tải danh mục ô lọc; khôi phục bộ lọc đã dùng trong 10 phút (BR-11) hoặc bộ lọc từ link Bảng cân đối; đủ ô bắt buộc thì tải số liệu.' % QUYEN],
        ['Bấm Tìm kiếm / đổi giá trị ô lọc', 'Click / Change', 'Xem mục 2.2.'],
        ['Chuyển trang / đổi Số dòng/trang', 'Click / Change', 'After:\n– Tải lại bút toán của trang mới theo bộ lọc đã áp, giữ 3 dòng tổng; đổi số dòng thì về trang 1.'],
        ['Bấm số hợp đồng / số chứng từ', 'Click', 'After:\n– Mở màn chi tiết hợp đồng / chứng từ ở tab mới; sổ chi tiết giữ nguyên.'],
        ['Rê chuột vào icon ⓘ tiêu đề trang', 'Hover', 'After:\n– Hiện mô tả màn và phạm vi quyền.'],
    ],
    'them': [
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', [
            ('p', 'Bảng dưới mô tả cách hệ thống tính từng chỉ tiêu và từng cột. "Bút toán" là một dòng ghi Nợ hoặc ghi Có vào sổ công nợ do chứng từ sinh ra khi hạch toán.'),
            ('data', DATA_MAIN)]),
        ('Danh sách popup mở từ số liệu', [
            ('p', 'Màn không có popup chi tiết; các liên kết trên bảng mở màn gốc ở tab mới.'),
            ('popup', POPUP_MAIN)]),
    ],
})

# ================================================================ 2.2 Tìm kiếm và lọc
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc sổ chi tiết'],
        ['Mô tả', 'Chọn tài khoản, khách hàng, kỳ; thu hẹp bằng ô tìm nhanh, Tài khoản đối ứng, Đơn hàng/Hợp đồng, Số chứng từ, Số tiền, Công ty / Phòng ban / Bộ phận / Nhân viên; chọn Loại tiền.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn %s.' % TEN],
        ['Dòng sự kiện chính', '1. Người dùng chọn Tài khoản, Khách hàng (gõ từ 2 ký tự), Thời gian.\n2. Hệ thống tự tải bảng ngay khi đủ 3 ô bắt buộc.\n3. Người dùng gõ thêm ô tìm nhanh / Đơn hàng/Hợp đồng / Số chứng từ / Số tiền rồi bấm Tìm kiếm hoặc Enter; hoặc chọn Tài khoản đối ứng, Loại tiền, ô tổ chức (tải lại ngay).\n4. Hệ thống áp đồng thời mọi điều kiện, tính lại 3 dòng tổng, tải lại từ trang 1.'],
        ['Dòng sự kiện phụ', '• Bấm Tìm kiếm khi thiếu ô bắt buộc → chữ đỏ dưới ô "Vui lòng chọn tài khoản" / "Vui lòng chọn khách hàng" / "Vui lòng chọn thời gian", không tải; chọn xong ô thì chữ đỏ tự tắt.\n• Lịch của ô Thời gian không cho chọn Đến ngày trước Từ ngày.\n• Bấm Làm mới → mọi ô về mặc định (Loại tiền = VNĐ), bảng về lời nhắc.\n• F5 = Làm mới; chuyển sang màn khác rồi quay lại → bộ lọc về mặc định.\n• Bấm Cài đặt bộ lọc → chọn ô lọc được hiển thị, kéo đổi thứ tự (quy tắc chung).'],
    ],
    'anh': [('02_required', 'Bấm Tìm kiếm khi chưa chọn Tài khoản, Khách hàng, Thời gian'),
            ('05_keyword', 'Ô tìm nhanh "PXH": còn 31 bút toán, 3 dòng tổng tính lại theo từ khóa'),
            ('13_filter_setting', 'Cửa sổ Cài đặt bộ lọc (mặc định hiện đủ 9 ô)')],
    'ui': ui(UI7, [
        ['Ô tìm nhanh', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', ['- Placeholder "Tìm theo số chứng từ hoặc số hợp đồng".', '- Lọc gần đúng theo số chứng từ HOẶC số hợp đồng của bút toán.', '- Không giới hạn số ký tự; bỏ khoảng trắng đầu / cuối; ký tự % và _ được hiểu là ký tự thường.', '- Áp khi bấm Tìm kiếm / Enter; tính lại cả 3 dòng tổng (BR-05).']],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', ['- Kiểm 3 ô bắt buộc rồi tải lại bảng từ trang 1.']],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', ['- Xoá mọi điều kiện, Loại tiền về VNĐ, ẩn chữ đỏ, bảng về lời nhắc.']],
        ['Nút Ẩn / Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Mở', ['- Thu gọn / mở khu vực các ô lọc.']],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', ['- Chọn ô lọc hiển thị và thứ tự; lưu theo người dùng, từng màn. Ô bị ẩn thì giá trị đang lọc của ô đó bị xoá.']],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Trống', ['- Chỉ hiện với quyền mức Tổng công ty.', '- Icon khoá cạnh nhãn: bật / tắt hiện cả công ty đã khoá.', '- Lọc theo công ty ghi trên bút toán.']],
        ['Ô Phòng ban', 'Dropdown', 'Enable', 'Theo công ty đã chọn', 'Trống', ['- Lọc theo phòng ban ghi trên bút toán (không phải phòng ban của NVKD ở cột Phòng ban).', '- Icon khoá: hiện cả phòng ban đã khoá.']],
        ['Ô Bộ phận', 'Dropdown', 'Enable', 'Theo phòng ban đã chọn', 'Trống', ['- Lọc theo bộ phận ghi trên bút toán.']],
        ['Ô Nhân viên', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', ['- Lọc bút toán của hợp đồng do nhân viên đó tạo (khớp cột NVKD).', '- Icon khoá: hiện cả nhân viên đã nghỉ.']],
        ['Ô Tài khoản', 'Dropdown', 'Enable', 'Mọi tài khoản đang hoạt động, dạng "Số hiệu - Tên"', 'Trống', ['- Bắt buộc (dấu *).', '- Lấy tài khoản đã chọn + tài khoản con trực tiếp.', '- Trống khi Tìm kiếm: "Vui lòng chọn tài khoản".']],
        ['Ô Khách hàng', 'Dropdown', 'Enable', 'Gõ từ 2 ký tự, tối đa 20 kết quả', 'Trống', ['- Bắt buộc (dấu *); chọn 1 khách hàng.', '- Tìm theo mã, tên hoặc số điện thoại; hiển thị "Mã KH - Tên khách hàng"; có nút × xoá.', '- Trống khi Tìm kiếm: "Vui lòng chọn khách hàng".']],
        ['Ô Thời gian', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', ['- Bắt buộc (dấu *); 1 ô gồm Từ ngày → Đến ngày, tính cả 2 đầu theo ngày hạch toán.', '- Không chọn được Đến ngày trước Từ ngày.', '- Trống khi Tìm kiếm: "Vui lòng chọn thời gian".']],
        ['Ô Tài khoản đối ứng', 'Dropdown', 'Enable', 'Mọi tài khoản đang hoạt động', 'Trống', ['- Chỉ giữ bút toán có tài khoản đối ứng đã chọn.']],
        ['Ô Đơn hàng/Hợp đồng', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', ['- Lọc gần đúng theo số hợp đồng; áp khi Tìm kiếm / Enter.']],
        ['Ô Số chứng từ', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', ['- Lọc gần đúng theo số chứng từ; áp khi Tìm kiếm / Enter.']],
        ['Ô Loại tiền', 'Dropdown', 'Enable', 'VNĐ / Ngoại tệ', 'VNĐ', ['- VNĐ: chỉ bút toán VNĐ, bảng 11 cột.', '- Ngoại tệ: chỉ bút toán ngoại tệ, bảng 15 cột, dòng tổng theo từng loại tiền.', '- Đổi giá trị → tải lại ngay. Bấm × xoá → coi như VNĐ.']],
        ['Ô Số tiền', 'Number', 'Enable', 'Số, 1 ô "từ → đến"', 'Trống', ['- So với số quy đổi VNĐ của TỪNG bút toán (≥ từ, ≤ đến); nhập 0 = không lọc.', '- Tự thêm dấu phẩy ngăn nghìn; áp khi Enter / Tìm kiếm.']],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Chọn Tài khoản / Khách hàng / Thời gian / Tài khoản đối ứng / Loại tiền / ô tổ chức', 'Change', 'After:\n– Đủ 3 ô bắt buộc → tải lại bảng (kể cả 3 dòng tổng) từ trang 1; chưa đủ → bảng về lời nhắc.'],
        ['Gõ ô tìm nhanh / Đơn hàng/Hợp đồng / Số chứng từ / Số tiền', 'Keypress', 'After:\n– Chưa lọc; chờ Enter hoặc Tìm kiếm.'],
        ['Bấm Tìm kiếm / Enter', 'Click', 'Before:\n– Thiếu ô bắt buộc → chữ đỏ dưới ô, mở khung lọc nếu đang thu gọn, dừng.\nAfter:\n– Áp mọi điều kiện, tải lại từ trang 1, lưu bộ lọc.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện và bộ lọc đã lưu, bảng về lời nhắc.'],
    ],
})

# ================================================================ 2.3 In
FR.append({
    'ten': 'In báo cáo', 'uc': 'uc_in',
    'qtc': 'In.',
    'gioi_thieu': [
        ['Tên chức năng', 'In sổ chi tiết công nợ phải thu khách hàng'],
        ['Mô tả', 'Xem trước và in sổ theo mẫu "SỔ CHI TIẾT CÔNG NỢ PHẢI THU KHÁCH HÀNG", khổ ngang, gồm MỌI bút toán theo bộ lọc đã áp.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_DATA],
        ['Dòng sự kiện chính', '1. Người dùng bấm In.\n2. Hệ thống mở cửa sổ "Xem trước sổ chi tiết công nợ phải thu khách hàng": tiêu đề công ty của người in, tên sổ, khối thông tin lọc (Công ty, Phòng ban, Khách hàng, Tài khoản, Loại tiền, Thời gian), bảng như màn hình (3 dòng tổng đứng đầu), dòng "Ngày … tháng … năm …", chỗ ký Người lập, Kế toán trưởng.\n3. Người dùng bấm In trong cửa sổ để in ra máy in.'],
        ['Dòng sự kiện phụ', '• Thiếu ô bắt buộc → "%s", không mở cửa sổ.\n• Vượt 2.000 bút toán → cửa sổ chỉ hiện: "Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.", không có nội dung in.' % MSG_THIEU],
    ],
    'menu_them': ' => In {icon:btn_in}',
    'ghi_chu_layout': 'Cửa sổ xem trước bản in được mở ngay trên màn sổ chi tiết theo đường dẫn ở trên.',
    'anh': [('08_print', 'Cửa sổ Xem trước sổ chi tiết công nợ phải thu khách hàng')],
    'ui': ui(UI6, [
        ['Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Xem trước sổ chi tiết công nợ phải thu khách hàng', ['- Nút × đóng cửa sổ.']],
        ['Nút In', 'Button', 'Enable / Ẩn', 'Hiển thị', ['- In bản xem trước ra máy in.', '- Không dùng được khi vượt trần 2.000 dòng.']],
        ['Bản xem trước', 'Label', 'Read-only', 'Theo dữ liệu', ['- Khổ ngang; khối thông tin lọc dạng "Nhãn : Giá trị", ô Công ty / Phòng ban không chọn thì ghi "Tất cả"; người quyền mức Công ty luôn thấy Công ty "Tất cả".', '- Bảng cùng cột với màn hình theo Loại tiền; 3 dòng tổng in đậm; ô không có số để trống.']],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In (màn sổ)', 'Click', 'Before:\n– Thiếu ô bắt buộc → toast "%s", dừng.\nAfter:\n– Lấy mọi bút toán theo bộ lọc đã áp, dựng bản in, mở cửa sổ xem trước.' % MSG_THIEU],
        ['Bấm In (trong cửa sổ)', 'Click', 'After:\n– Gửi bản xem trước ra máy in.'],
        ['Bấm ×', 'Click', 'After:\n– Đóng cửa sổ.'],
    ],
})

# ================================================================ 2.4 Xuất Excel
FR.append({
    'ten': 'Xuất Excel', 'uc': 'uc_xuat',
    'qtc': 'Xuất Excel.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất sổ chi tiết ra Excel'],
        ['Mô tả', 'Tải ngay file Excel gồm 3 dòng tổng và MỌI bút toán (mọi trang) theo bộ lọc đã áp, đủ cột theo Loại tiền; không có cửa sổ chọn cột.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_DATA],
        ['Dòng sự kiện chính', '1. Người dùng bấm Xuất Excel.\n2. Hệ thống tải dữ liệu theo từng lượt 2.000 dòng, hiện tiến độ cạnh nút.\n3. Hệ thống tải về file so_chi_tiet_cong_no_kh.xlsx, báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Thiếu ô bắt buộc → "%s".\n• Không có bút toán nào trong kỳ: file vẫn có tiêu đề, hàng tên cột và 3 dòng tổng.\n• Lỗi → "Lỗi khi xuất Excel".' % MSG_THIEU],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'File được tải về ngay từ màn sổ chi tiết theo đường dẫn ở trên.',
    'anh': [('07_export', 'Xuất Excel thành công (thông báo góc màn hình)')],
    'ui': ui(UI6, [
        ['Nút Xuất Excel', 'Button', 'Enable / Disable', 'Enable', ['- Khoá trong lúc đang xuất; bên cạnh hiện tiến độ.']],
        ['File Excel', 'File', '–', '–', [
            '- Sheet "So chi tiet cong no KH"; dòng tiêu đề "SỔ CHI TIẾT CÔNG NỢ PHẢI THU KHÁCH HÀNG", dưới là dòng chữ nhỏ "Từ ngày dd/mm/yyyy đến ngày dd/mm/yyyy".',
            '- Tiêu đề cột 1 tầng: STT, Đơn hàng/Hợp đồng, Ngày hạch toán, Số chứng từ, NVKD, Phòng ban, Ghi chú, Phát sinh nợ, Phát sinh có, Tài khoản đối ứng, Tên tài khoản đối ứng (mẫu Ngoại tệ: Loại tiền, Số phát sinh ngoại tệ - Nợ / - Có, Tỷ giá, Số phát sinh VNĐ - Nợ / - Có).',
            '- 3 dòng tổng (nhãn ở cột Ghi chú) đứng trước các bút toán; cuối file có dòng "Ngày ..., tháng ..., năm ..." và chỗ ký "Người lập".',
            '- Cột số lưu dạng số, định dạng 1,234,567.']],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'Before:\n– Thiếu ô bắt buộc → "%s", dừng.\nAfter:\n– Tải mọi dòng theo bộ lọc đã áp, dựng file, tải về, báo "Xuất Excel thành công" (lỗi: "Lỗi khi xuất Excel").' % MSG_THIEU],
    ],
})

# ---------------------------------------------------------------- Phần 2 + 4
PERMS = [
    ('%s — mức Tổng công ty' % QUYEN, 'Thấy sổ của mọi công ty; có ô Công ty.'),
    ('%s — mức Công ty' % QUYEN, 'Thấy bút toán thuộc công ty đang làm việc, cộng bút toán của hợp đồng do chính mình tạo (ở công ty khác); không có ô Công ty.'),
    ('(Không có quyền)', 'Không thấy mục menu; mở màn bằng đường dẫn thì bị báo không có quyền, không có số liệu, không In / Xuất Excel được.'),
]
FUNCS = ['FR-01 Xem sổ chi tiết công nợ', 'FR-02 Tìm kiếm và lọc', 'FR-03 In báo cáo', 'FR-04 Xuất Excel']

S = {
    'ten': TEN,
    'menu': [('Tài chính', 'menu_phanhe'), ('Kế toán công nợ', 'menu_nhom'), ('Khách hàng', 'menu_nhomcon'), (TEN, 'menu_muc')],
    'hoac': HOAC,
    'muc_dich': [
        'Là căn cứ nghiệm thu màn báo cáo.',
        'Làm rõ cách lấy từng bút toán, cách tính Số dư đầu kỳ / Tổng phát sinh / Số dư cuối kỳ ở mẫu VNĐ và Ngoại tệ, tác động của từng ô lọc lên dòng tổng, và phạm vi dữ liệu theo 2 mức quyền.',
    ],
    'thuat_ngu': [
        ['Công nợ phải thu', 'Số tiền khách hàng còn phải trả công ty, ghi trên tài khoản phải thu khách hàng (131 và tài khoản con).'],
        ['Bút toán', 'Một dòng ghi Nợ hoặc ghi Có vào sổ công nợ do một chứng từ sinh ra khi hạch toán.'],
        ['Ngày hạch toán', 'Ngày chứng từ được ghi sổ; là ngày dùng để xếp kỳ.'],
        ['Kỳ', 'Từ ngày đến hết Đến ngày của ô Thời gian.'],
        ['Tài khoản con trực tiếp', 'Tài khoản cấp ngay dưới tài khoản đã chọn (131 → 1311, 1312, 1313), không lấy cấp sâu hơn.'],
        ['Tài khoản đối ứng', 'Tài khoản ghi bên kia của bút toán (vd 5111 doanh thu, 1121 tiền gửi).'],
        ['Số quy đổi VNĐ', 'Số tiền bút toán quy ra VNĐ theo tỷ giá ghi trên bút toán.'],
        ['NVKD', 'Nhân viên kinh doanh — người tạo hợp đồng của bút toán.'],
        ['Phạm vi dữ liệu', 'Phần sổ người dùng được xem theo mức quyền (Tổng công ty / Công ty).'],
    ],
    'quyen_truoc': [
        'Màn kiểm quyền "%s" (2 mức phạm vi). Không có quyền thì mục menu bị ẩn và mọi thao tác xem, In, Xuất Excel đều bị từ chối.' % QUYEN,
    ],
    'quyen_rows': [list(p) for p in PERMS],
    'ma_tran': [['Chức năng', 'Tổng công ty', 'Công ty', 'Không quyền']] + [[f, 'Có', 'Có', 'Không'] for f in FUNCS],
    'ma_tran_widths': [2.8, 1.1, 1.0, 1.1],
    'quyen_sau': [
        'Phạm vi áp cho mọi con số: dòng bút toán, 3 dòng tổng, file Excel và bản in.',
        '"Hợp đồng do mình tạo" = bút toán có người tạo hợp đồng là người đang xem. "Công ty đang làm việc" = công ty người dùng đang chọn khi đăng nhập.',
    ],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Điều kiện bắt buộc', [
            '– Phải chọn đủ Tài khoản, Khách hàng, Thời gian mới tải số liệu, In, Xuất Excel.',
            '– Chưa đủ: bảng hiện lời nhắc; Tìm kiếm báo đỏ dưới ô; In / Xuất Excel báo "%s".' % MSG_THIEU,
            '– Đến ngày không được nhỏ hơn Từ ngày ("Đến ngày phải lớn hơn hoặc bằng Từ ngày.").'], ['Mọi chức năng']),
        ('BR-02', 'Quyền và phạm vi dữ liệu', [
            '– Tổng công ty: không giới hạn.',
            '– Công ty: bút toán ghi cho công ty đang làm việc HOẶC thuộc hợp đồng do mình tạo.',
            '– Không quyền: ẩn menu, từ chối mọi thao tác.'], ['Mọi chức năng']),
        ('BR-03', 'Tập bút toán', [
            '– Chỉ bút toán của khách hàng đã chọn, trên tài khoản đã chọn + tài khoản con trực tiếp.',
            '– Loại tiền VNĐ: bút toán VNĐ; Ngoại tệ: bút toán khác VNĐ.',
            '– Mỗi bút toán 1 dòng, xếp theo ngày hạch toán rồi thời điểm tạo.'], ['Xem sổ chi tiết', 'In', 'Xuất Excel']),
        ('BR-04', 'Dòng tổng', [
            '– Số dư đầu kỳ = Nợ − Có trước Từ ngày; Tổng phát sinh = Σ Nợ, Σ Có trong kỳ (không bù trừ); Số dư cuối kỳ = đầu kỳ + Nợ − Có.',
            '– Số dư dương ghi cột nợ, âm ghi cột có (số tuyệt đối).',
            '– Tính trên toàn kỳ, không đổi khi chuyển trang. Mẫu Ngoại tệ tính riêng từng loại tiền.'], ['Xem sổ chi tiết', 'In', 'Xuất Excel']),
        ('BR-05', 'Ô lọc áp cả số dư đầu kỳ', [
            '– Mọi ô lọc (kể cả ô tìm nhanh, Đơn hàng/Hợp đồng, Số chứng từ, Tài khoản đối ứng, Số tiền, ô tổ chức) áp cho cả bút toán đầu kỳ.',
            '– Vì vậy khi lọc thêm ngoài 3 ô bắt buộc, Số dư đầu kỳ chỉ là số dư của phần bút toán khớp điều kiện, không còn là số dư công nợ của khách hàng.'], ['Tìm kiếm và lọc']),
        ('BR-06', 'Lọc tổ chức', [
            '– Công ty (chỉ mức Tổng công ty), Phòng ban, Bộ phận: theo đơn vị ghi trên bút toán.',
            '– Nhân viên: theo người tạo hợp đồng (cột NVKD).',
            '– Cột Phòng ban hiển thị phòng ban HIỆN TẠI của NVKD nên có thể khác Phòng ban đang lọc.'], ['Tìm kiếm và lọc']),
        ('BR-07', 'Ô Số tiền', [
            '– So với số quy đổi VNĐ của từng bút toán; nhập 0 hoặc để trống = không lọc.'], ['Tìm kiếm và lọc']),
        ('BR-08', 'Định dạng số', [
            '– Dạng 1,234,567.89, tối đa 2 chữ số lẻ; ô dòng tổng bằng 0 để trống; ô bút toán ghi đúng phía Nợ / Có.'], ['Xem sổ chi tiết', 'In', 'Xuất Excel']),
        ('BR-09', 'In / Xuất Excel', [
            '– Lấy MỌI bút toán theo bộ lọc ĐÃ ÁP (ô gõ dở chưa bấm Tìm kiếm không tính).',
            '– In tối đa 2.000 bút toán; Excel không giới hạn, tải theo lượt 2.000 dòng.'], ['In', 'Xuất Excel']),
        ('BR-10', 'Lối vào từ Bảng cân đối', [
            '– Bấm mã khách hàng ở Bảng cân đối phát sinh công nợ khách hàng → mở tab mới, điền sẵn Tài khoản, Khách hàng, Thời gian, Công ty, Phòng ban, Bộ phận, Nhân viên, Số tiền và Loại tiền theo loại tiền của dòng, tự tải số liệu (thắng bộ lọc đã lưu).'], ['Xem sổ chi tiết']),
        ('BR-11', 'Ghi nhớ bộ lọc', [
            '– Mở lại màn trong 10 phút (tab mới / đường dẫn): giữ bộ lọc.',
            '– Chuyển sang màn khác trong ứng dụng, tải lại trang (F5) hoặc Làm mới: bộ lọc về mặc định.'], ['Tìm kiếm và lọc']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây dùng chung sổ công nợ / khung tính với báo cáo này, mở sang màn này, hoặc là chứng từ nguồn sinh bút toán (mở được từ cột Số chứng từ, Đơn hàng/Hợp đồng).',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng có quyền xem sổ',
    'mains': [('FR-01', 'Xem sổ chi tiết công nợ', 'view'), ('FR-03', 'In báo cáo', 'io'), ('FR-04', 'Xuất Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc', 'view')],
    'rieng': [('FR-03', 'In báo cáo', 'io', 'uc_in'), ('FR-04', 'Xuất Excel', 'io', 'uc_xuat')],
}


# ---------------------------------------------------------------- dựng tài liệu (chép màn mẫu compare/gen_srs.py)
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
        if i == 0 and S.get('hoac'):
            w.p(S['hoac'])
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

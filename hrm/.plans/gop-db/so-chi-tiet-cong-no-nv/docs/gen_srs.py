# -*- coding: utf-8 -*-
"""SRS - Sổ chi tiết công nợ nhân viên (form Danh mục quốc gia + quy tắc màn BÁO CÁO của skill srs-documenter).

Khuôn: sale-customer-debt-reports/docs/compare/gen_srs.py (mẫu báo cáo đã duyệt) + danh-muc-kho/docs/_lib_win.py
(KHÔNG sửa lib dùng chung — hàm dựng `build_srs_report` chép trong file này).

Nguồn (code HRM, nhánh develop 18/11/2026):
  FE hrm-client/pages/finance/employee-debt-details/{index.vue, components/constants.js},
     components/subsystem-menu/finance.js, components/V2BaseCompanyDepartmentFilter.vue, utils/invoiceable-link.js,
     utils/contract-link.js, utils/export/listExportFile.js, utils/mixins/{filterStateMixin, reportPrintPreviewMixin}.js
  BE Modules/Finance/Http/Controllers/V1/EmployeeDebtDetailController.php (+ Concerns/ValidatesAccountDebtFilters),
     Services/EmployeeDebt/EmployeeDebtDetailService.php, Services/AccountDebt/{AccountLedgerService, Concerns/AccountDebtCommon}.php,
     quyền: app/Support/Permissions/Catalog/accounting.php (accounting.so_chi_tiet_cong_no_nhan_vien.view, phạm vi 3/4)
Ảnh: hdsd_shots/ (capture.js, dev-hrm 18/11/2026).
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(GOPDB, 'danh-muc-kho', 'docs'))
import _lib_win as L  # noqa: E402
from _lib_win import QgWriter, SRS_ROLES, QTC_LINK, h1_trang_moi  # noqa: E402

TEN = 'Sổ chi tiết công nợ nhân viên'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
QUYEN = 'Xem sổ chi tiết công nợ nhân viên'
Q = 'Người dùng có quyền "%s" (mức Tổng công ty hoặc Công ty)' % QUYEN
DK = '1. Người dùng đăng nhập thành công.\n2. Có quyền "%s" mức Tổng công ty hoặc Công ty (BR-02).' % QUYEN
DK_DATA = DK + '\n3. Đã chọn Tài khoản và Thời gian (Từ ngày, Đến ngày).'
MSG_THIEU = 'Vui lòng chọn tài khoản và thời gian'
LOI_NHAC = 'Chọn tài khoản và thời gian để xem sổ chi tiết.'
MSG_403 = 'Bạn không có quyền thực hiện thao tác này'
MSG_TRAN = ('Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, '
            'trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.')
TIP_TRANG = ('Sổ chi tiết từng bút toán của một tài khoản theo dõi công nợ gắn với nhân viên: số dư đầu kỳ, phát sinh Nợ / Có '
             'trong kỳ, số dư cuối kỳ. Quyền xem theo tổng công ty hoặc công ty (công ty: nhân viên công ty mình và sổ của chính mình).')

UI6 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả']
UI6W = [0.5, 1.35, 0.85, 0.8, 0.95, 2.75]
UI7 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả']
UI7W = [0.45, 1.2, 0.85, 0.8, 1.0, 0.85, 2.6]
NUM = '- Số theo định dạng 1,234,567.89 (tối đa 2 chữ số lẻ, bỏ số 0 vô nghĩa).'


def ui(header, rows):
    return [header] + [[str(i + 1)] + r for i, r in enumerate(rows)]


# ---------------------------------------------------------------- Phần 5 (dò code FE/BE + menu 18/11/2026)
P5 = [
    ('Tài chính', 'Bảng cân đối phát sinh công nợ nhân viên (cùng quyền, phạm vi, ô lọc; bấm số liệu mở sổ chi tiết này với bộ lọc tương ứng)', 'Tài chính => Kế toán công nợ => Nhân viên'),
    ('Tài chính', 'Sổ chi tiết công nợ phải trả nhà cung cấp (cùng khung sổ chi tiết: dòng tổng, cột, bản in, file Excel)', 'Tài chính => Kế toán công nợ => Nhà cung cấp'),
    ('Tài chính', 'Danh mục tài khoản (ô Tài khoản: tài khoản theo dõi công nợ đang hoạt động; ô Tài khoản đối ứng: mọi tài khoản đang hoạt động)', 'Tài chính => Danh mục => Danh mục tài khoản'),
    ('Tài chính', 'Danh mục tiền tệ (ô Loại tiền, cột Loại tiền)', 'Tài chính => Danh mục => Danh mục tiền tệ'),
    ('Tài chính', 'Danh mục vụ việc (ô Mã vụ việc)', 'Tài chính => Danh mục => Danh mục vụ việc'),
    ('Tài chính', 'Phiếu thu (chứng từ nguồn; mở từ cột Số chứng từ)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu chi (chứng từ nguồn; mở từ cột Số chứng từ)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu báo có (chứng từ nguồn; mở từ cột Số chứng từ)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu ủy nhiệm chi (chứng từ nguồn; mở từ cột Số chứng từ)', 'Tài chính => Quản lý tiền => Thanh toán tiền mặt'),
    ('Tài chính', 'Phiếu nhập hàng (chứng từ nguồn; mở từ cột Số chứng từ)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng'),
    ('Tài chính', 'Phiếu xuất hàng (chứng từ nguồn; mở từ cột Số chứng từ)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng'),
    ('Tài chính', 'Phiếu xuất bán hàng mượn (chứng từ nguồn; mở từ cột Số chứng từ)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng'),
    ('Tài chính', 'Phiếu kế toán (chứng từ nguồn; mở từ cột Số chứng từ)', 'Tài chính => Sổ tổng hợp => Sổ tổng hợp'),
    ('Tài chính', 'Khai báo đầu kỳ công nợ (chứng từ nguồn; mở từ cột Số chứng từ)', 'Tài chính => Khai báo đầu kỳ'),
    ('Bán hàng', 'Hợp đồng (dự án TKT) — mở từ cột Đơn hàng/Hợp đồng', 'Bán hàng => Hợp đồng bán hàng'),
    ('Bán hàng', 'Hợp đồng bán đầu kỳ — mở từ cột Đơn hàng/Hợp đồng', 'Bán hàng => Khác'),
]

FR = []

# ================================================================ 2.1 Xem sổ chi tiết
COT = [
    ['Tiêu đề trang', 'Label', 'Hiển thị', TEN, ['- Ở thanh trên cùng, kèm icon ⓘ.', '- Icon ⓘ: "%s"' % TIP_TRANG]],
    ['Tiêu đề bảng', 'Label', 'Hiển thị', TEN, ['- Tiêu đề khối bảng kết quả.']],
    ['Nút In', 'Button', 'Enable', 'Hiển thị', ['- Mở cửa sổ xem trước bản in theo bộ lọc đang áp (mục 2.3).', '- Chưa chọn đủ Tài khoản và Thời gian: báo "%s".' % MSG_THIEU]],
    ['Nút Xuất Excel', 'Button', 'Enable / Disable', 'Hiển thị', ['- Tải ngay file Excel theo bộ lọc đang áp (mục 2.4), không có cửa sổ chọn trường.', '- Chưa chọn đủ Tài khoản và Thời gian: báo "%s".' % MSG_THIEU, '- Bị khoá trong lúc đang xuất; cạnh nút hiện tiến độ "Đang chuẩn bị dữ liệu…" / "Đã tải x/y dòng…" / "Đang dựng file n dòng…".']],
    ['Bảng sổ chi tiết', 'Table/Grid', 'Read-only', 'Lời nhắc', [
        '- Mẫu VNĐ: 11 cột — STT, Đơn hàng/Hợp đồng, Ngày hạch toán, Số chứng từ, Nhân viên, Phòng ban, Ghi chú, Phát sinh nợ, Phát sinh có, Tài khoản đối ứng (Tài khoản, Tên tài khoản).',
        '- Mẫu Ngoại tệ: 15 cột — thay 2 cột Phát sinh nợ / Phát sinh có bằng Loại tiền, Số phát sinh ngoại tệ (Nợ, Có), Tỷ giá, Số phát sinh VNĐ (Nợ, Có).',
        '- Thứ tự dòng: 3 dòng tổng (Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ — nền xám, chữ đậm) → các dòng bút toán.',
        '- Tiêu đề bảng 2 tầng, dính khi cuộn dọc; bảng cuộn ngang khi màn hẹp.',
        '- Chưa chọn đủ Tài khoản + Thời gian: "%s"' % LOI_NHAC,
        '- Đang tải: "Đang tải dữ liệu..."',
        '- Không có bút toán: vẫn hiện 3 dòng tổng, dưới là "Không có dữ liệu phù hợp bộ lọc."']],
    ['Dòng Số dư đầu kỳ', 'Table/Grid', 'Read-only', 'Theo dữ liệu', [
        '- Nhãn gộp 7 cột đầu, căn phải.', '- Số dư dương (dư Nợ) ở cột Phát sinh nợ, số âm (dư Có) ở cột Phát sinh có, ghi giá trị tuyệt đối; bằng 0 để trống.', '- Cách tính: bảng 2.1.5.']],
    ['Dòng Tổng phát sinh', 'Table/Grid', 'Read-only', 'Theo dữ liệu', [
        '- Mẫu VNĐ: Tổng Nợ ở cột Phát sinh nợ, Tổng Có ở cột Phát sinh có (0 để trống).',
        '- Mẫu Ngoại tệ: mỗi loại tiền có phát sinh 1 dòng, ghi Loại tiền; số ròng (Nợ − Có) đặt ở cột Nợ nếu dương, cột Có nếu âm, cả phần ngoại tệ và phần VNĐ; dòng loại tiền VNĐ để trống phần ngoại tệ.']],
    ['Dòng Số dư cuối kỳ', 'Table/Grid', 'Read-only', 'Theo dữ liệu', [
        '- = Số dư đầu kỳ + Tổng Nợ − Tổng Có (VNĐ), đặt cột như dòng Số dư đầu kỳ.', '- Không đổi khi chuyển trang / đổi số dòng mỗi trang.']],
    ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', ['- 1, 2, 3… liên tục qua các trang (trang 2 bắt đầu 11 khi 10 dòng/trang).']],
    ['Cột Đơn hàng/Hợp đồng', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Số hợp đồng gắn với bút toán; trống nếu bút toán không gắn hợp đồng.', '- Loại hợp đồng có màn xem: chữ dạng liên kết, bấm mở hợp đồng ở tab mới; loại khác hiện chữ thường.']],
    ['Cột Ngày hạch toán', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Ngày hạch toán của chứng từ, dạng dd/mm/yyyy.']],
    ['Cột Số chứng từ', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Số chứng từ sinh bút toán.', '- Chứng từ có màn xem (phiếu thu, phiếu chi, phiếu báo có, phiếu ủy nhiệm chi, phiếu kế toán, phiếu xuất hàng, phiếu nhập hàng, phiếu xuất bán hàng mượn, khai báo đầu kỳ công nợ, hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ bảo hành - sửa chữa): chữ dạng liên kết, bấm mở chứng từ ở tab mới.', '- Loại chứng từ khác (vd hạch toán chi phí vận chuyển): chữ thường.']],
    ['Cột Nhân viên', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Họ tên nhân viên gắn với bút toán; trống nếu bút toán không gắn nhân viên. Tự xuống dòng.']],
    ['Cột Phòng ban', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Phòng ban của nhân viên ghi trên bút toán.']],
    ['Cột Ghi chú', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Ghi chú của chứng từ, chỉ lấy với phiếu xuất hàng, phiếu nhập hàng, phiếu thu, phiếu ủy nhiệm chi, phiếu báo có; loại chứng từ khác để trống.', '- Rộng tối đa ~320 px, dài thì xuống dòng.']],
    ['Cột Phát sinh nợ / Phát sinh có (mẫu VNĐ)', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Số tiền quy đổi VNĐ của bút toán, đặt ở cột Nợ hoặc Có theo chiều ghi sổ; cột còn lại để trống.', '- Bút toán 0 đồng vẫn in "0" ở đúng cột.', NUM]],
    ['Cột Loại tiền (mẫu Ngoại tệ)', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Loại tiền của bút toán (VNĐ, USD…).']],
    ['Cột Số phát sinh ngoại tệ — Nợ, Có (mẫu Ngoại tệ)', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Số tiền nguyên tệ của bút toán; CHỈ có số với bút toán khác VNĐ, bút toán VNĐ để trống.', NUM]],
    ['Cột Tỷ giá (mẫu Ngoại tệ)', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Tỷ giá ghi trên bút toán (VNĐ là 1).', NUM]],
    ['Cột Số phát sinh VNĐ — Nợ, Có (mẫu Ngoại tệ)', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Số tiền quy đổi VNĐ, như cột Phát sinh nợ / có của mẫu VNĐ.', NUM]],
    ['Cột Tài khoản đối ứng — Tài khoản, Tên tài khoản', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Số hiệu và tên mọi tài khoản đối ứng của bút toán, nhiều tài khoản cách nhau dấu phẩy.']],
    ['Chân bảng', 'Label', 'Hiển thị', 'Ẩn khi không có dữ liệu', ['- "Hiển thị a–b / N bút toán": N = số bút toán trong kỳ theo bộ lọc, có dấu phẩy ngăn hàng nghìn.']],
    ['Ô Số dòng/trang', 'Dropdown', 'Enable', '10', ['- Lựa chọn: 10, 20, 50, 100.', '- Đổi số dòng → quay về trang 1, giữ 3 dòng tổng.']],
    ['Phân trang', 'Button', 'Enable', 'Trang 1', ['- « ‹ số trang › »; chuyển trang giữ nguyên bộ lọc và 3 dòng tổng.']],
]

DATA_MAIN = [
    ('Tập dữ liệu / thời điểm số liệu', 'Bút toán ghi sổ của tài khoản đã chọn VÀ các tài khoản con trực tiếp của nó (không lấy cấp cháu), sau khi áp phạm vi quyền (BR-02) và mọi ô lọc. "Trong kỳ" = ngày hạch toán từ 00:00 Từ ngày đến 23:59:59 Đến ngày; "đầu kỳ" = trước Từ ngày. Số liệu đọc tại thời điểm tải (không lưu sẵn).'),
    ('Dòng bút toán', 'Mỗi bút toán trong kỳ 1 dòng (kể cả bút toán KHÔNG gắn nhân viên). Xếp theo ngày hạch toán tăng dần, cùng ngày theo thời điểm tạo bút toán.'),
    ('Số dư đầu kỳ', 'Tổng Nợ − Tổng Có (VNĐ quy đổi) của các bút toán có ngày hạch toán TRƯỚC Từ ngày, CHỈ tính bút toán có gắn nhân viên, cùng phạm vi quyền và cùng các ô lọc (trừ khoảng ngày). Dương ghi cột Nợ, âm ghi cột Có.'),
    ('Tổng phát sinh', 'Tổng Nợ và tổng Có (VNĐ quy đổi) của MỌI bút toán trong kỳ theo bộ lọc (kể cả bút toán không gắn nhân viên); tính trên toàn bộ kỳ, không phụ thuộc trang. Mẫu Ngoại tệ: tách theo loại tiền, mỗi loại 1 dòng số ròng.'),
    ('Số dư cuối kỳ', 'Số dư đầu kỳ + Tổng Nợ − Tổng Có, làm tròn 2 chữ số lẻ.'),
    ('Đơn hàng/Hợp đồng', 'Số hợp đồng ghi trên bút toán.'),
    ('Nhân viên / Phòng ban', 'Nhân viên và phòng ban ghi trên bút toán lúc hạch toán.'),
    ('Ghi chú', 'Ghi chú chung của chứng từ, chỉ với 5 loại: phiếu xuất hàng, phiếu nhập hàng, phiếu thu, phiếu ủy nhiệm chi, phiếu báo có.'),
    ('Phát sinh nợ / có (VNĐ)', 'Số tiền quy đổi VNĐ của bút toán, theo chiều ghi Nợ / Có.'),
    ('Số phát sinh ngoại tệ', 'Số tiền nguyên tệ của bút toán; chỉ hiện với bút toán khác VNĐ.'),
    ('Tỷ giá', 'Tỷ giá ghi trên bút toán.'),
    ('Tài khoản đối ứng', 'Mọi tài khoản đối ứng của bút toán (không trùng), theo thứ tự ghi; lọc Tài khoản đối ứng không làm mất các đối ứng khác của cùng bút toán.'),
    ('Ràng buộc khớp số', '- Tổng phát sinh Nợ / Có = tổng cột Phát sinh nợ / có của MỌI trang.\n- Số dư cuối kỳ = Số dư đầu kỳ + Tổng Nợ − Tổng Có.\n- Khi không lọc Nhân viên mà tài khoản có bút toán không gắn nhân viên: các bút toán này có trong dòng và Tổng phát sinh nhưng KHÔNG có trong Số dư đầu kỳ của kỳ sau (BR-04).\n- Mẫu VNĐ và mẫu Ngoại tệ cùng tập bút toán, cùng 3 số dư; chỉ khác cách bày cột.'),
    ('Chân bảng "Hiển thị a–b / N bút toán"', 'N = số bút toán trong kỳ theo bộ lọc (không tính 3 dòng tổng).'),
]

FR.append({
    'ten': 'Xem sổ chi tiết công nợ nhân viên',
    'qtc': 'Màn Báo cáo, Phân trang, Định dạng số.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem sổ chi tiết công nợ nhân viên'],
        ['Mô tả', 'Hiển thị từng bút toán trong kỳ của một tài khoản theo dõi công nợ (vd 141 Tạm ứng) kèm 3 dòng Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ; có 2 mẫu hiển thị VNĐ và Ngoại tệ. Màn chỉ đọc.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu; bảng hiện lời nhắc "%s", chưa tải số liệu.\n2. Người dùng chọn Tài khoản và Thời gian (mục 2.2).\n3. Hệ thống tính số liệu theo phạm vi quyền + bộ lọc, hiện 3 dòng tổng và trang 1 gồm 10 bút toán.\n4. Chân bảng ghi "Hiển thị 1–10 / N bút toán".' % LOI_NHAC],
        ['Dòng sự kiện phụ', '• Không có quyền: hệ thống báo "%s", ô Tài khoản không có lựa chọn nên không xem được số liệu.\n• Không có bút toán trong kỳ: vẫn hiện 3 dòng tổng (có thể có Số dư đầu kỳ), dưới là "Không có dữ liệu phù hợp bộ lọc.".\n• Lỗi khi lấy dữ liệu → "Lỗi khi tải dữ liệu".\n• Đổi bộ lọc liên tục: chỉ kết quả lần lọc mới nhất được hiển thị.\n• Chuyển trang / đổi số dòng: không tính lại 3 dòng tổng.\n• Phiên đăng nhập hết hạn: hệ thống đưa về màn đăng nhập.' % MSG_403],
        ['Yêu cầu đặc biệt', 'Thời gian tải trên môi trường thử nghiệm (18/11/2026), kỳ 01/01/2026 – 31/10/2026: tài khoản 141 (2.599 bút toán) dưới 1 giây; tài khoản 131 (68.866 bút toán) khoảng 6 giây.'],
    ],
    'anh': [('01_empty', 'Màn Sổ chi tiết công nợ nhân viên lúc mới mở (chưa chọn bộ lọc)'),
            ('03_report', 'Sổ chi tiết tài khoản 141 - Tạm ứng, kỳ 01/01/2026 – 31/10/2026, mẫu VNĐ'),
            ('04b_employee_table', 'Bảng sổ chi tiết lọc thêm Nhân viên Võ Cát Hào — 3 dòng tổng và trang 1'),
            ('05b_foreign_table', 'Mẫu Ngoại tệ — tài khoản 131, loại tiền USD, kỳ 01/01/2026 – 31/10/2026')],
    'ui': ui(UI6, COT),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Kiểm quyền "%s"; không có → báo "%s", không nạp danh mục lọc.\nAfter:\n– Nạp danh mục ô lọc; khôi phục bộ lọc đã dùng trong 10 phút (BR-10) hoặc bộ lọc trên đường dẫn mở từ Bảng cân đối phát sinh công nợ nhân viên; đủ Tài khoản + Thời gian thì tải dữ liệu, chưa đủ thì hiện lời nhắc.' % (QUYEN, MSG_403)],
        ['Đổi giá trị ô lọc / bấm Tìm kiếm', 'Click / Change', 'Xem mục 2.2.'],
        ['Đổi ô Mẫu', 'Change', 'After:\n– Đổi bộ cột VNĐ ↔ Ngoại tệ ngay trên số liệu đang có, không tải lại.'],
        ['Chuyển trang / đổi Số dòng/trang', 'Click / Change', 'After:\n– Tải bút toán của trang mới theo bộ lọc của lần tìm gần nhất, giữ 3 dòng tổng; đổi số dòng thì về trang 1.'],
        ['Bấm số chứng từ / số hợp đồng dạng liên kết', 'Click', 'After:\n– Mở màn chi tiết chứng từ / hợp đồng ở tab mới; màn sổ chi tiết giữ nguyên.'],
        ['Rê chuột vào icon ⓘ cạnh tiêu đề trang', 'Hover', 'After:\n– Hiện mô tả màn (nguyên văn ở dòng Tiêu đề trang).'],
    ],
    'them': [
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', [
            ('p', 'Bảng dưới mô tả cách hệ thống tính từng chỉ tiêu và từng cột. Màn không có icon ⓘ trên tiêu đề cột nên cột "Nội dung icon ⓘ" ghi "—".'),
            ('data', [(a, b, '—') for a, b in DATA_MAIN])]),
        ('Danh sách popup mở từ số liệu', [('popup', [
            ('Số chứng từ dạng liên kết', 'Không phải popup — mở màn chi tiết chứng từ ở tab mới', 'Kiểm tra chứng từ gốc tạo ra bút toán', 'Đúng chứng từ của dòng'),
            ('Số hợp đồng dạng liên kết (cột Đơn hàng/Hợp đồng)', 'Không phải popup — mở màn hợp đồng ở tab mới', 'Xem hợp đồng gắn với bút toán', 'Hợp đồng tương ứng; loại chưa có màn xem thì chữ thường'),
            ('Ô số tiền / dòng tổng', 'Không bấm được', '—', '—'),
        ])]),
    ],
})

# ================================================================ 2.2 Tìm kiếm và lọc
LOAI_CT = ('Phiếu xuất hàng - Xuất bán; Phiếu xuất hàng - Xuất khuyến mại; Phiếu xuất hàng - Xuất mượn; Phiếu xuất hàng - Xuất trả nhà cung cấp; '
           'Phiếu xuất hàng - Xuất bán (HĐDV); Phiếu xuất bán hàng mượn; Phiếu nhập hàng - Mua hàng ngoài; Phiếu nhập hàng - Mua hàng trong nước; '
           'Phiếu nhập hàng - Mua hàng nước ngoài (mới); Phiếu nhập hàng - Bán trả lại; Phiếu nhập hàng - Bán (khi mượn) trả lại; Phiếu thu; Phiếu chi; '
           'Phiếu ủy nhiệm chi; Phiếu báo có; Phiếu kế toán')
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc sổ chi tiết'],
        ['Mô tả', 'Chọn tài khoản, kỳ và thu hẹp bút toán bằng 16 ô lọc + ô tìm nhanh; chọn Mẫu hiển thị.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn Sổ chi tiết công nợ nhân viên.'],
        ['Dòng sự kiện chính', '1. Người dùng chọn Tài khoản và Thời gian (Từ ngày → Đến ngày).\n2. Hệ thống tự tải bảng ngay khi đủ 2 ô bắt buộc.\n3. Người dùng chọn thêm ô dạng danh sách (tải lại ngay) hoặc gõ ô chữ / số tiền / tìm nhanh rồi bấm Tìm kiếm hoặc Enter.\n4. Hệ thống áp đồng thời mọi điều kiện (VÀ), tải lại từ trang 1 và tính lại 3 dòng tổng.'],
        ['Dòng sự kiện phụ', '• Bấm Tìm kiếm khi thiếu ô bắt buộc → chữ đỏ dưới ô "Vui lòng chọn tài khoản" / "Vui lòng chọn thời gian", khung lọc tự mở nếu đang thu gọn, không tải dữ liệu.\n• Lịch của ô Thời gian khoá ngày làm Đến ngày nhỏ hơn Từ ngày; đường dẫn mở màn có Đến ngày < Từ ngày → báo "Đến ngày phải lớn hơn hoặc bằng Từ ngày.".\n• Bấm Làm mới → mọi ô về mặc định (Mẫu = VNĐ), bảng về lời nhắc.\n• F5 = Làm mới; rời màn rồi quay lại trong 10 phút thì giữ bộ lọc.'],
    ],
    'anh': [('02_required', 'Bấm Tìm kiếm khi chưa chọn Tài khoản, Thời gian'),
            ('06_keyword', 'Ô tìm nhanh "HTCXK" thu hẹp còn 158 bút toán, 3 dòng tổng tính lại theo từ khoá'),
            ('10_filter_settings', 'Cửa sổ Cài đặt bộ lọc (chọn ô lọc hiển thị, kéo đổi thứ tự)')],
    'ui': ui(UI7, [
        ['Ô tìm nhanh', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', ['- Placeholder "Tìm theo số chứng từ hoặc số hợp đồng".', '- Giữ bút toán có Số chứng từ HOẶC số hợp đồng chứa từ khoá (gần đúng, ký tự % _ hiểu là ký tự thường).', '- Áp khi bấm Tìm kiếm / Enter; có tính lại 3 dòng tổng.']],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', ['- Kiểm 2 ô bắt buộc rồi tải lại bảng từ trang 1.']],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', ['- Xoá mọi điều kiện, Mẫu về VNĐ, ẩn chữ đỏ, bảng về lời nhắc, xoá bộ lọc đã nhớ.']],
        ['Nút Ẩn / Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Mở', ['- Thu gọn / mở khu vực các ô lọc.']],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', ['- Mở cửa sổ "Cài đặt bộ lọc": tích chọn 14 nhóm ô lọc hiển thị, kéo đổi thứ tự; Lưu / Khôi phục mặc định / Đóng (quy tắc chung).']],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Trống', ['- Chỉ hiện với quyền mức Tổng công ty.', '- Icon khoá cạnh nhãn: bật / tắt hiện cả công ty đã khoá.', '- Lọc bút toán có nhân viên thuộc công ty này; đổi Công ty thì xoá Phòng ban, Bộ phận, Nhân viên.']],
        ['Ô Phòng ban', 'Dropdown', 'Enable', 'Theo công ty', 'Trống', ['- Lọc theo phòng ban của nhân viên ghi trên bút toán; đổi thì xoá Bộ phận, Nhân viên.']],
        ['Ô Bộ phận', 'Dropdown', 'Enable', 'Theo phòng ban', 'Trống', ['- Lọc theo bộ phận của nhân viên ghi trên bút toán.']],
        ['Ô Nhân viên', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', ['- Lọc bút toán gắn nhân viên này.', '- Mặc định bật sẵn hiện cả nhân viên đã nghỉ (icon khoá cạnh nhãn).']],
        ['Ô Tài khoản', 'Dropdown', 'Enable', 'Tài khoản theo dõi công nợ đang hoạt động, "Số hiệu - Tên"', 'Trống', ['- Bắt buộc (dấu *).', '- Lấy bút toán của tài khoản chọn và các tài khoản con trực tiếp.', '- Trống khi bấm Tìm kiếm: "Vui lòng chọn tài khoản".']],
        ['Ô Thời gian', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', ['- Bắt buộc (dấu *); 1 ô gồm Từ ngày → Đến ngày, tính cả 2 đầu mút theo ngày hạch toán.', '- Lịch khoá ngày làm Đến ngày < Từ ngày.', '- Trống khi bấm Tìm kiếm: "Vui lòng chọn thời gian".']],
        ['Ô Tài khoản đối ứng', 'Dropdown', 'Enable', 'Mọi tài khoản đang hoạt động', 'Trống', ['- Giữ bút toán có tài khoản đối ứng này; áp cả Số dư đầu kỳ.']],
        ['Ô Đơn hàng/Hợp đồng', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', ['- Lọc gần đúng theo số hợp đồng; áp khi Tìm kiếm / Enter.']],
        ['Ô Loại chứng từ', 'Dropdown (chọn nhiều)', 'Enable', '16 lựa chọn', 'Trống', ['- Lựa chọn: %s.' % LOAI_CT, '- Chọn nhiều = lấy bút toán thuộc BẤT KỲ loại đã chọn.', '- Lưu ý: các mục "Phiếu xuất hàng - …" đều lọc MỌI phiếu xuất hàng (không phân biệt loại con); tương tự các mục "Phiếu nhập hàng - …" (BR-06).']],
        ['Ô Số chứng từ', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', ['- Lọc gần đúng theo số chứng từ; áp khi Tìm kiếm / Enter.']],
        ['Ô Ghi chú', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', ['- Lọc gần đúng theo ghi chú của 5 loại phiếu ở cột Ghi chú; áp khi Tìm kiếm / Enter.']],
        ['Ô Loại tiền', 'Dropdown', 'Enable', 'Danh mục tiền tệ đang hoạt động', 'Trống', ['- Lọc bút toán theo loại tiền.']],
        ['Ô Mẫu', 'Dropdown', 'Enable', 'VNĐ / Ngoại tệ', 'VNĐ', ['- Chỉ đổi bộ cột hiển thị, In và Excel; không đổi tập bút toán, không tải lại.', '- Xoá (×) ô Mẫu thì hiển thị như VNĐ.']],
        ['Ô Khách hàng', 'Dropdown', 'Enable', 'Gõ từ 2 ký tự để tìm', 'Trống', ['- Lọc bút toán có khách hàng của hợp đồng là khách đã chọn; có nút × xoá.']],
        ['Ô Chỉ tiêu', 'Dropdown', 'Enable', 'Nợ / Có', 'Trống', ['- Chỉ lấy bút toán ghi Nợ hoặc ghi Có; áp cả 3 dòng tổng.']],
        ['Ô Mã vụ việc', 'Dropdown', 'Enable', 'Danh mục vụ việc, "Mã - Tên"', 'Trống', ['- Lọc bút toán theo vụ việc.']],
        ['Ô Số tiền', 'Textbox số (2 ô)', 'Enable', 'Số, định dạng 1,234,567', 'Trống', ['- "Nhập số tiền từ" → "Nhập số tiền đến"; so với số tiền VNĐ quy đổi của TỪNG bút toán (lớn hơn hoặc bằng / nhỏ hơn hoặc bằng).', '- Ô để trống hoặc bằng 0 thì bỏ qua.', '- Áp khi Tìm kiếm / Enter.']],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Chọn Tài khoản / Thời gian / ô dạng danh sách', 'Change', 'After:\n– Đủ Tài khoản + Thời gian → tải lại bảng từ trang 1 (không cần bấm Tìm kiếm); chưa đủ → bảng về lời nhắc. Lưu bộ lọc.'],
        ['Gõ ô tìm nhanh / Đơn hàng/Hợp đồng / Số chứng từ / Ghi chú / Số tiền', 'Keypress', 'After:\n– Chưa lọc; chờ Enter hoặc nút Tìm kiếm.'],
        ['Bấm Tìm kiếm / Enter', 'Click', 'Before:\n– Thiếu Tài khoản hoặc Thời gian → chữ đỏ dưới ô, mở khung lọc, dừng.\nAfter:\n– Áp mọi điều kiện, tải lại từ trang 1, tính lại 3 dòng tổng, lưu bộ lọc.'],
        ['Bấm Làm mới', 'Click', 'After:\n– Mọi ô về mặc định, bảng về lời nhắc, xoá bộ lọc đã nhớ.'],
        ['Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở cửa sổ Cài đặt bộ lọc (quy tắc chung).'],
    ],
})

# ================================================================ 2.3 In
FR.append({
    'ten': 'In sổ chi tiết', 'uc': 'uc_in',
    'qtc': 'In.',
    'gioi_thieu': [
        ['Tên chức năng', 'In sổ chi tiết công nợ nhân viên'],
        ['Mô tả', 'Xem trước và in sổ theo mẫu "SỔ CHI TIẾT CÔNG NỢ NHÂN VIÊN", khổ ngang, gồm 3 dòng tổng và MỌI bút toán theo bộ lọc đang áp, cột theo Mẫu.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_DATA],
        ['Dòng sự kiện chính', '1. Người dùng bấm In.\n2. Hệ thống mở cửa sổ "Xem trước sổ chi tiết công nợ nhân viên": tiêu đề công ty của người xem, tên sổ, khối thông tin (Công ty, Phòng ban, Tài khoản, Mẫu, Thời gian "Từ dd/mm/yyyy đến dd/mm/yyyy"), bảng, dòng "Ngày … tháng … năm …" và khối ký Người lập, Kế toán trưởng.\n3. Người dùng bấm In trong cửa sổ để in ra máy in.'],
        ['Dòng sự kiện phụ', '• Chưa đủ Tài khoản + Thời gian → "%s", không mở cửa sổ.\n• Quá 2.000 bút toán → cửa sổ chỉ hiện: "%s", ẩn nút In.' % (MSG_THIEU, MSG_TRAN)],
    ],
    'menu_them': ' => In {icon:btn_in}',
    'ghi_chu_layout': 'Cửa sổ xem trước bản in được mở ngay trên màn sổ chi tiết theo đường dẫn ở trên.',
    'anh': [('08_print', 'Cửa sổ Xem trước sổ chi tiết công nợ nhân viên (TK 141, Nhân viên Võ Cát Hào, mẫu VNĐ)'),
            ('09_print_limit', 'Bản in vượt mức 2.000 dòng (TK 141, 2.599 bút toán)')],
    'ui': ui(UI6, [
        ['Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Xem trước sổ chi tiết công nợ nhân viên', ['- Nút × đóng cửa sổ.']],
        ['Nút In', 'Button', 'Enable / Ẩn', 'Hiển thị', ['- In bản xem trước ra máy in.', '- Ẩn khi vượt mức 2.000 dòng.']],
        ['Khối thông tin', 'Label', 'Read-only', 'Theo bộ lọc', ['- Công ty, Phòng ban (trống ghi "Tất cả"), Tài khoản "Số hiệu - Tên", Mẫu (VNĐ / Ngoại tệ), Thời gian.']],
        ['Bảng in', 'Label', 'Read-only', 'Theo dữ liệu', ['- Cột như màn hình theo Mẫu; cột Nhân viên in nhãn "NVKD".', '- 3 dòng tổng ngay dưới tiêu đề, chữ đậm.', '- Số dạng 1,234,567.89; ô trống để trống.']],
        ['Khối ký', 'Label', 'Hiển thị', '–', ['- "Ngày dd tháng mm năm yyyy" (ngày in); Người lập, Kế toán trưởng (Ký, họ tên).']],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In (màn sổ)', 'Click', 'Before:\n– Thiếu Tài khoản / Thời gian → "%s", dừng.\nAfter:\n– Đếm bút toán; vượt 2.000 thì hiện câu nhắc, không dựng bảng; không vượt thì dựng bản in theo bộ lọc của lần tìm gần nhất.' % MSG_THIEU],
        ['Bấm In (trong cửa sổ)', 'Click', 'After:\n– Gửi bản xem trước ra máy in.'],
        ['Bấm ×', 'Click', 'After:\n– Đóng cửa sổ, màn sổ giữ nguyên.'],
    ],
})

# ================================================================ 2.4 Xuất Excel
FR.append({
    'ten': 'Xuất Excel', 'uc': 'uc_xuat',
    'qtc': 'Xuất Excel.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất sổ chi tiết ra Excel'],
        ['Mô tả', 'Xuất 3 dòng tổng và MỌI bút toán theo bộ lọc đang áp ra file Excel, đủ cột theo Mẫu; không giới hạn số dòng, không có cửa sổ chọn trường.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_DATA],
        ['Dòng sự kiện chính', '1. Người dùng bấm Xuất Excel.\n2. Hệ thống lấy dữ liệu theo từng lô 2.000 dòng, cạnh nút hiện tiến độ.\n3. Hệ thống tải file so_chi_tiet_cong_no_nhan_vien.xlsx và báo "Xuất Excel thành công".'],
        ['Dòng sự kiện phụ', '• Chưa đủ Tài khoản + Thời gian → "%s".\n• Không có dòng nào → "Không có dữ liệu để xuất".\n• Lỗi → "Lỗi khi xuất Excel".\n• Đang xuất: nút Xuất Excel bị khoá, bấm lại không có tác dụng.' % MSG_THIEU],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'anh': [('07_export', 'Xuất Excel xong — thông báo "Xuất Excel thành công"')],
    'ui': ui(UI6, [
        ['Nút Xuất Excel', 'Button', 'Enable / Disable', 'Enable', ['- Khoá trong lúc đang xuất.']],
        ['Chữ tiến độ', 'Label', 'Ẩn', 'Ẩn', ['- Chỉ hiện khi đang xuất: "Đang chuẩn bị dữ liệu…", "Đã tải x/y dòng…", "Đang dựng file n dòng…".']],
        ['File Excel', 'File', '–', '–', [
            '- Tên file so_chi_tiet_cong_no_nhan_vien.xlsx, sheet "So chi tiet cong no NV".',
            '- Dòng 1 ảnh tiêu đề công ty; dòng 2 "SỔ CHI TIẾT CÔNG NỢ NHÂN VIÊN (TỪ NGÀY dd/mm/yyyy ĐẾN NGÀY dd/mm/yyyy)".',
            '- Hàng tên cột 1 tầng: mẫu VNĐ STT, Đơn hàng/Hợp đồng, Ngày hạch toán, Số chứng từ, NVKD, Phòng ban, Ghi chú, Phát sinh nợ, Phát sinh có, Tài khoản đối ứng, Tên tài khoản đối ứng; mẫu Ngoại tệ thêm Loại tiền, Số phát sinh ngoại tệ - Nợ/Có, Tỷ giá, Số phát sinh VNĐ - Nợ/Có.',
            '- Tiếp theo 3 dòng tổng (nhãn ở cột Ghi chú), rồi các bút toán theo thứ tự trên màn.',
            '- Ô số lưu dạng số, định dạng 1,234,567; cuối file "Ngày ..., tháng ..., năm ...", "Người lập", "(Ký, họ tên)".']],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Xuất Excel', 'Click', 'Before:\n– Thiếu Tài khoản / Thời gian → "%s", dừng.\nDuring:\n– Lấy dữ liệu theo lô 2.000 dòng theo bộ lọc của lần tìm gần nhất, hiện tiến độ.\nAfter:\n– Tải file, báo "Xuất Excel thành công" (rỗng: "Không có dữ liệu để xuất"; lỗi: "Lỗi khi xuất Excel").' % MSG_THIEU],
    ],
})

# ---------------------------------------------------------------- Phần 2 + 4
FUNCS = ['FR-01 Xem sổ chi tiết công nợ nhân viên', 'FR-02 Tìm kiếm và lọc', 'FR-03 In sổ chi tiết', 'FR-04 Xuất Excel']

S = {
    'ten': TEN,
    'menu': [('Tài chính', 'menu_phanhe'), ('Kế toán công nợ', 'menu_nhom'), ('Nhân viên', 'menu_nhomcon'), (TEN, 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu màn báo cáo Sổ chi tiết công nợ nhân viên.',
        'Phạm vi chức năng: xem sổ chi tiết theo 2 mẫu (VNĐ, Ngoại tệ), tìm kiếm / lọc, in, xuất Excel; màn chỉ đọc, không thêm / sửa / xoá dữ liệu.',
        'Mục đích sử dụng dữ liệu: kế toán theo dõi từng bút toán công nợ của nhân viên (tạm ứng, phải thu khác…), đối chiếu số dư đầu kỳ / cuối kỳ với nhân viên.',
        'Làm rõ cách tính 3 dòng tổng, phạm vi dữ liệu theo 2 mức quyền, tác động của từng ô lọc và các điểm số liệu dễ hiểu nhầm (đầu kỳ chỉ tính bút toán có nhân viên; loại chứng từ phiếu xuất / nhập không phân biệt loại con).',
    ],
    'thuat_ngu': [
        ['Bút toán', 'Một dòng ghi Nợ hoặc ghi Có vào sổ tài khoản do một chứng từ sinh ra khi hạch toán.'],
        ['Tài khoản theo dõi công nợ', 'Tài khoản kế toán được đánh dấu theo dõi công nợ (vd 131, 141, 1388, 334).'],
        ['Tài khoản con trực tiếp', 'Tài khoản có số hiệu cha là tài khoản đang chọn (vd 1411, 1412 của 141); không tính cấp cháu.'],
        ['Ngày hạch toán', 'Ngày chứng từ được ghi sổ; là ngày dùng để xếp kỳ.'],
        ['Kỳ', 'Từ ngày đến hết Đến ngày của ô Thời gian.'],
        ['Số dư đầu kỳ / cuối kỳ', 'Tổng Nợ − Tổng Có trước Từ ngày / đến hết Đến ngày; dương là dư Nợ, âm là dư Có.'],
        ['Tài khoản đối ứng', 'Tài khoản ghi phía bên kia của cùng bút toán.'],
        ['Mẫu', 'Cách bày cột: VNĐ (chỉ số tiền quy đổi) hoặc Ngoại tệ (thêm nguyên tệ, tỷ giá).'],
        ['NVKD', 'Nhãn cột nhân viên trên bản in và file Excel.'],
        ['Phạm vi dữ liệu', 'Phần bút toán người dùng được xem theo mức quyền (Tổng công ty / Công ty).'],
    ],
    'quyen_truoc': [
        'Màn dùng 1 quyền "%s" với 2 mức phạm vi. Mục menu luôn hiện; người không có quyền mở màn sẽ bị từ chối xem dữ liệu ("%s"). Có quyền ở cả 2 mức thì tính theo mức Tổng công ty.' % (QUYEN, MSG_403),
    ],
    'quyen_rows': [
        ['%s — mức Tổng công ty' % QUYEN, 'Xem bút toán của mọi công ty (kể cả bút toán không gắn nhân viên); hiện đủ ô Công ty, Phòng ban, Bộ phận, Nhân viên.'],
        ['%s — mức Công ty' % QUYEN, 'Xem bút toán có nhân viên thuộc công ty đang làm việc, cộng bút toán gắn chính mình ở công ty khác; không có ô Công ty, có ô Phòng ban, Bộ phận, Nhân viên.'],
        ['(Không có quyền)', 'Vẫn thấy mục menu và mở được màn nhưng bị báo "%s"; ô Tài khoản không có lựa chọn, In / Xuất Excel không lấy được dữ liệu.' % MSG_403],
    ],
    'ma_tran': [['Chức năng', 'Tổng công ty', 'Công ty', 'Không quyền']] + [[f, 'Có', 'Có', 'Không'] for f in FUNCS],
    'ma_tran_widths': [3.2, 1.1, 1.1, 1.1],
    'quyen_sau': [
        'Phạm vi áp cho mọi con số: dòng bút toán, 3 dòng tổng, bản in và file Excel. "Công ty đang làm việc" = công ty người dùng đang chọn khi đăng nhập. Màn không có thêm / sửa / xoá / khoá / import / lịch sử.',
    ],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Điều kiện bắt buộc', [
            '– Phải chọn Tài khoản và đủ Thời gian (Từ ngày, Đến ngày) mới tải số liệu, In, Xuất Excel.',
            '– Chưa đủ: bảng hiện "%s"; bấm Tìm kiếm báo đỏ dưới ô; bấm In / Xuất Excel báo "%s".' % (LOI_NHAC, MSG_THIEU),
            '– Đến ngày không được nhỏ hơn Từ ngày ("Đến ngày phải lớn hơn hoặc bằng Từ ngày.").'], ['Xem', 'Tìm kiếm và lọc', 'In', 'Xuất Excel']),
        ('BR-02', 'Quyền và phạm vi dữ liệu', [
            '– Không có quyền "%s": từ chối mọi thao tác lấy dữ liệu, báo "%s".' % (QUYEN, MSG_403),
            '– Mức Tổng công ty: mọi bút toán.',
            '– Mức Công ty: bút toán có nhân viên thuộc công ty đang làm việc HOẶC nhân viên là chính mình; bút toán không gắn nhân viên KHÔNG thuộc phạm vi này.'], ['Mọi chức năng']),
        ('BR-03', 'Tài khoản và kỳ', [
            '– Lấy tài khoản chọn và các tài khoản con trực tiếp (không lấy cấp cháu).',
            '– Xếp kỳ theo ngày hạch toán; trong kỳ tính cả ngày Đến ngày đến 23:59:59.'], ['Xem', 'In', 'Xuất Excel']),
        ('BR-04', 'Ba dòng tổng', [
            '– Số dư đầu kỳ: Nợ − Có trước Từ ngày, CHỈ bút toán có gắn nhân viên, cùng phạm vi + ô lọc.',
            '– Tổng phát sinh: Nợ, Có trong kỳ của MỌI bút toán theo bộ lọc (kể cả không gắn nhân viên).',
            '– Số dư cuối kỳ = đầu kỳ + Nợ − Có, làm tròn 2 số lẻ. Dương ghi cột Nợ, âm ghi cột Có (giá trị tuyệt đối).',
            '– Tính trên toàn kỳ, không đổi khi chuyển trang.'], ['Xem', 'In', 'Xuất Excel']),
        ('BR-05', 'Mẫu VNĐ / Ngoại tệ', [
            '– Mẫu chỉ đổi cách bày cột; tập bút toán và số dư như nhau.',
            '– Mẫu Ngoại tệ: Tổng phát sinh tách theo loại tiền (số ròng); cột nguyên tệ chỉ có số với bút toán khác VNĐ.'], ['Xem', 'In', 'Xuất Excel']),
        ('BR-06', 'Ô Loại chứng từ', [
            '– Chọn nhiều = HOẶC.',
            '– Mọi mục "Phiếu xuất hàng - …" cùng lọc toàn bộ phiếu xuất hàng; mọi mục "Phiếu nhập hàng - …" cùng lọc toàn bộ phiếu nhập hàng (không tách theo loại con).'], ['Tìm kiếm và lọc']),
        ('BR-07', 'Các ô lọc khác', [
            '– Mọi ô áp đồng thời (VÀ), áp cho cả dòng và 3 dòng tổng.',
            '– Công ty / Phòng ban / Bộ phận / Nhân viên theo thông tin nhân viên ghi trên bút toán.',
            '– Đơn hàng/Hợp đồng, Số chứng từ, Ghi chú, ô tìm nhanh: tìm gần đúng.',
            '– Số tiền từ / đến so với số tiền VNĐ của từng bút toán; ô bằng 0 bị bỏ qua.',
            '– Tài khoản đối ứng: giữ bút toán có đối ứng này, cột vẫn hiện đủ mọi đối ứng.'], ['Tìm kiếm và lọc']),
        ('BR-08', 'Định dạng số và ô trống', [
            '– Số dạng 1,234,567.89 (tối đa 2 số lẻ).',
            '– Dòng bút toán: số 0 vẫn in "0" ở đúng cột Nợ / Có. Dòng tổng: bằng 0 để trống.'], ['Xem', 'In', 'Xuất Excel']),
        ('BR-09', 'In / Xuất Excel', [
            '– Theo bộ lọc của lần tìm gần nhất (ô gõ dở chưa bấm Tìm kiếm không được tính).',
            '– In tối đa 2.000 bút toán; vượt thì không in, gợi ý Xuất Excel.',
            '– Xuất Excel không giới hạn số dòng.'], ['In', 'Xuất Excel']),
        ('BR-10', 'Ghi nhớ bộ lọc và mở từ màn khác', [
            '– Rời màn rồi quay lại trong 10 phút: giữ bộ lọc. Tải lại trang (F5) hoặc Làm mới: về mặc định.',
            '– Mở từ Bảng cân đối phát sinh công nợ nhân viên: bộ lọc truyền sang (Tài khoản, Thời gian, Công ty, Phòng ban, Bộ phận, Nhân viên, Loại tiền, Mẫu, Số tiền, Chỉ tiêu) thay hẳn bộ lọc đã nhớ và tự tải số liệu.'], ['Tìm kiếm và lọc']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây dùng chung dữ liệu / cách tính với sổ này, cung cấp danh mục cho ô lọc, hoặc là chứng từ nguồn mở được từ cột Số chứng từ / Đơn hàng/Hợp đồng.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng có quyền xem sổ',
    'mains': [('FR-01', 'Xem sổ chi tiết công nợ nhân viên', 'view'), ('FR-03', 'In sổ chi tiết', 'io'), ('FR-04', 'Xuất Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc', 'view')],
    'rieng': [('FR-03', 'In sổ chi tiết', 'io', 'uc_in'), ('FR-04', 'Xuất Excel', 'io', 'uc_xuat')],
}


# ---------------------------------------------------------------- dựng tài liệu (chép mẫu compare/gen_srs.py)
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
                            [[str(j + 1)] + list(r) for j, r in enumerate(it[1])], widths=[0.55, 1.3, 3.6, 1.3])
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

# -*- coding: utf-8 -*-
"""SRS - Báo cáo chi tiết chuyến xe (form Danh mục quốc gia + quy tắc màn BÁO CÁO của skill srs-documenter).

Khuôn: sale-customer-debt-reports/docs/compare/gen_srs.py — hàm dựng dùng chung ở ../hieu-qua-gop-xe/_trp_docs.py.
Nguồn (code HRM develop 18/11/2026):
  FE hrm-client/pages/transport/trip-detail-report/index.vue, pages/transport/components/{TransportReportPage,
     TransportReportTable, TransportReportSummary, TransportItemModal, configs/tripDetail.js, tripDetailExcel.js, format.js},
     components/subsystem-menu/transport.js
  BE Modules/Finance/Http/Controllers/V1/{TransportReportController, TripDetailReportController},
     Services/DriverCostReport/{TripDetailReportService, TripDetailReportPrintService, TransportReportPrintService},
     resources/views/prints/finance/trip_detail_customer_summary.blade.php; quyền: app/Support/Permissions/Catalog/
     {warehouse.php: warehouse.bao_cao_van_chuyen.view, sale.php: sale.bao_cao_chi_phi_van_chuyen_theo_nhan_vien_kinh_doanh.view}
Ảnh: hdsd_shots/ (capture.js, dev-hrm 18/11/2026).
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'hieu-qua-gop-xe'))
import _trp_docs as D  # noqa: E402
from _trp_docs import L, ui, UI6, UI6W, UI7, UI7W  # noqa: E402

TEN = 'Báo cáo chi tiết chuyến xe'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q = 'Người dùng đã đăng nhập (mọi người dùng; quyền chỉ quyết định phạm vi dữ liệu)'
DK = '1. Người dùng đăng nhập thành công.\n2. Không cần quyền để mở màn; phạm vi dữ liệu theo BR-02.'
DK_DATA = DK + '\n3. Báo cáo đã tải xong theo bộ lọc đang chọn.'
NUM = ('- Số theo định dạng 1,234,567 (tối đa 2 chữ số lẻ); số âm có dấu "-".',
       '- Dòng TỔNG / dòng nhóm: số 0 in "0" (chữ nhạt); dòng phiếu: số 0 để trống.')
POPUP = 'Cửa sổ %s được mở ngay trên màn báo cáo theo đường dẫn ở trên.'
TRIP_ONLY = 'Số của cả chuyến — chuyến ghép nhiều khách hàng để trống (không chia cho khách); dòng TỔNG cộng mỗi chuyến 1 lần'
SHARE = 'Phần của khách = cộng các phiếu xuất / nhập của khách trên chuyến (kế toán đã chia khi hạch toán chuyến)'

TIP = {
    'trang': 'Chi tiết từng chuyến xe: cước tính toán, cước thực tế, thuế, vé cầu đường, xe, lái xe và các phiếu xuất / nhập kho của chuyến. Xem theo khách hàng (cước của riêng từng khách) hoặc theo chuyến xe (đủ chi phí của chuyến). Nguồn: chuyến xe chở hàng / chuyến xe khác đã hoàn thành và phiếu hạch toán chuyến xe. Kỳ lọc theo ngày tạo chuyến (ngày vận chuyển).',
    'ky': 'Lọc theo NGÀY TẠO CHUYẾN XE (ngày vận chuyển).',
    'xemtheo': 'Khách hàng: cước theo phần của từng khách. Chuyến xe: từng chuyến với đủ chi phí xe và các phiếu nhập/xuất của chuyến.',
    'ten_kh': 'KHÁCH HÀNG / TUYẾN ĐƯỜNG / PHIẾU HẠCH TOÁN • Cấp 1: khách hàng (cước sau thuế giảm dần, nhóm "Không có khách hàng" luôn cuối) — cấp 2: tuyến đường — cấp 3: phiếu hạch toán chuyến xe • Cước / thuế ở mỗi dòng là phần của khách (các phiếu xuất / nhập của khách trên chuyến) ⇒ cộng các khách = dòng TỔNG • Chuyến ghép nhiều khách (nhãn "ghép N KH"): KM, cước chính / phụ trội, vé cầu đường của cả chuyến để trống; dòng TỔNG cộng mỗi chuyến 1 lần nên các cột này có thể lớn hơn tổng các khách',
    'ten_cx': 'PHIẾU HẠCH TOÁN / PHIẾU NHẬP-XUẤT • Mỗi nhóm là 1 chuyến (phiếu hạch toán chuyến xe) với cước / thuế / vé / xe / lái xe • Mỗi dòng con là 1 phiếu xuất / nhập kho chở trên chuyến — NVKD, khách hàng, đối tượng chịu phí • Dòng TỔNG cộng theo chuyến, tính trên toàn bộ dữ liệu đã lọc, không theo trang',
    'count': 'SỐ PHIẾU HẠCH TOÁN • Số phiếu hạch toán chuyến xe (1 phiếu = 1 chuyến) của khách / tuyến • Bấm vào con số để mở danh sách phiếu nhập/xuất',
    'km': 'KM • Tổng km thực tế ghi trên chuyến xe (số âm hiển thị 0) • ' + TRIP_ONLY,
    'km_add': 'KM PHỤ TRỘI • ' + TRIP_ONLY,
    'main': 'CƯỚC TÍNH TOÁN — CHÍNH • Cước tính theo công thức vận chuyển của chuyến • ' + TRIP_ONLY,
    'extra': 'CƯỚC TÍNH TOÁN — PHỤ TRỘI • Cước của km phụ trội • ' + TRIP_ONLY,
    'fee': 'CƯỚC THỰC TẾ • ' + SHARE,
    'tax': 'THUẾ • ' + SHARE,
    'after': 'CƯỚC SAU THUẾ • Cước thực tế + Thuế • ' + SHARE,
    'toll': 'VÉ CẦU ĐƯỜNG • ' + TRIP_ONLY,
    'nvkd': 'NVKD • Người lập yêu cầu xuất / nhập hàng của các phiếu của khách trên chuyến',
    'blk_trips': 'CHUYẾN XE • Chuyến xe đã hoàn thành, ngày tạo chuyến trong kỳ — 1 phiếu hạch toán = 1 chuyến • Ghép nhiều KH: chuyến chở hàng của từ 2 khách hàng trở lên (cước đã chia theo phiếu xuất / nhập) • Bấm vào con số để mở danh sách phiếu nhập/xuất',
    'blk_subject': 'ĐỐI TƯỢNG CHỊU PHÍ • Số phiếu xuất / nhập do nhân viên chịu phí / công ty chịu phí vận chuyển',
    'blk_money': 'CƯỚC VẬN CHUYỂN • Cộng theo chuyến (mỗi chuyến tính 1 lần, không theo số phiếu) • Cước sau thuế = Cước thực tế + Thuế',
}

P5 = [
    ('Vận chuyển', 'Chuyến xe chở hàng (lập, hoàn thành chuyến; hạch toán chuyến — nguồn số của báo cáo)', 'Vận chuyển => Chuyến xe => Chuyến xe chở hàng'),
    ('Vận chuyển', 'Chuyến xe chở hàng chờ hạch toán', 'Vận chuyển => Chuyến xe => Chuyến xe chở hàng chờ hạch toán'),
    ('Vận chuyển', 'Chuyến xe khác (lập, kết thúc, hạch toán chuyến)', 'Vận chuyển => Chuyến xe => Chuyến xe khác'),
    ('Vận chuyển', 'Chuyến xe khác chờ duyệt / chờ hạch toán', 'Vận chuyển => Chuyến xe => Chuyến xe khác chờ duyệt; Chuyến xe khác chờ hạch toán'),
    ('Vận chuyển', 'Báo cáo hiệu quả gộp xe vận tải (cùng nguồn chuyến xe, dùng chung quyền Xem báo cáo vận chuyển)', 'Vận chuyển => Báo cáo vận chuyển => Báo cáo hiệu quả gộp xe vận tải'),
    ('Vận chuyển', 'Báo cáo chi tiết hiệu quả gộp theo chuyến xe (cùng nguồn, cùng quyền)', 'Vận chuyển => Báo cáo vận chuyển => Báo cáo chi tiết hiệu quả gộp theo chuyến xe'),
    ('Vận chuyển', 'Báo cáo tổng hợp / chi tiết chi phí vận chuyển theo lái xe (cùng nguồn phiếu hạch toán, cùng quyền)', 'Vận chuyển => Báo cáo vận chuyển'),
    ('Vận chuyển; Bán hàng', 'Báo cáo chi phí vận chuyển theo nhân viên kinh doanh (dùng chung quyền Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh)', 'Vận chuyển => Báo cáo vận chuyển => Báo cáo chi phí vận chuyển theo nhân viên kinh doanh'),
    ('Tài chính; Kho', 'Phiếu xuất kho (dòng phiếu nhập/xuất của chuyến; mở từ mã phiếu)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng => Phiếu xuất kho'),
    ('Tài chính; Kho', 'Phiếu nhập kho (dòng phiếu nhập/xuất của chuyến; mở từ mã phiếu)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng => Phiếu nhập kho; Kho => Nhập kho => Phiếu nhập kho'),
    ('Tài chính', 'Yêu cầu xuất hàng / Yêu cầu nhập hàng (người lập = NVKD; công ty / phòng ban / bộ phận dùng cho ô lọc)', 'Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng / Nhập hàng'),
    ('Danh mục tham chiếu', 'Biển số xe (ô lọc Biển số xe, cột Xe)', 'Danh mục dùng chung => Danh mục xe => Biển số xe'),
    ('Danh mục tham chiếu', 'Danh mục xe, Dòng xe, Tải trọng xe, Lái xe ngoài (cột Xe tính cước, Xe, Lái xe)', 'Danh mục dùng chung => Danh mục xe'),
]

FR = []

# ================================================================ 2.1 Xem báo cáo
COT = [
    ['Tiêu đề trang', 'Label', 'Hiển thị', TEN, ['- Ở thanh trên cùng, kèm icon ⓘ.', '- Icon ⓘ: "%s"' % TIP['trang']]],
    ['Dòng kỳ của khối tổng hợp', 'Label', 'Hiển thị', 'Kỳ tháng mm/yyyy (theo ngày vận chuyển)', [
        '- "Kỳ <nhãn kỳ> (theo ngày vận chuyển)" + icon ⓘ + "· K khách hàng · N chuyến · Cước sau thuế X".', '- Nút "Thu gọn" / "Mở rộng".']],
    ['Khối Chuyến xe', 'Label', 'Read-only', 'Theo dữ liệu', [
        '- Góc phải "K khách hàng".', '- Ô "Phiếu hạch toán": số chuyến + "M phiếu nhập/xuất".',
        '- Ô "Chuyến xe chở hàng", "Chuyến xe khác", "Ghép nhiều KH": số chuyến; ô bằng 0 thì ẩn.',
        '- Con số gạch chân bấm được → popup danh sách phiếu nhập/xuất (mục 2.3).', '- Icon ⓘ: "%s"' % TIP['blk_trips']]],
    ['Khối Đối tượng chịu phí', 'Label', 'Read-only', 'Theo dữ liệu', ['- Ô "NV chịu", "Công ty chịu": số phiếu nhập/xuất; bấm → popup; ô 0 ẩn, cả 2 bằng 0 thì ẩn khối.', '- Icon ⓘ: "%s"' % TIP['blk_subject']]],
    ['Khối Cước vận chuyển', 'Label', 'Read-only', 'Theo dữ liệu', ['- Góc phải "KM <tổng km>".', '- Ô Cước thực tế, Thuế, Cước sau thuế, Vé cầu đường (ô bằng 0 ẩn, trừ Cước sau thuế). Không bấm được.', '- Icon ⓘ: "%s"' % TIP['blk_money']]],
    ['Bảng báo cáo — góc nhìn Khách hàng (mặc định)', 'Table/Grid', 'Read-only', 'Theo dữ liệu', [
        '- 16 cột: STT, Khách hàng / Tuyến đường / Phiếu hạch toán, Số phiếu HT, Xe, Lái xe, KM, KM phụ trội, Cước chính, Cước phụ trội, Cước thực tế, Thuế, Cước sau thuế, Vé cầu đường, NVKD, NV chịu, Công ty chịu.',
        '- Cây 3 cấp: dòng TỔNG → khách hàng (I, II…, kèm mã KH chữ nhỏ) → tuyến đường (1, 2…) → phiếu hạch toán (1.1, 1.2…).',
        '- Dòng phiếu: mã phiếu hạch toán (liên kết) + dòng phụ "dd/mm/yyyy · mã chuyến xe"; chuyến ghép thêm nhãn "ghép N KH".',
        '- Không có dữ liệu: "Không có chuyến xe nào khớp bộ lọc."']],
    ['Bảng báo cáo — góc nhìn Chuyến xe', 'Table/Grid', 'Read-only', 'Theo dữ liệu', [
        '- 23 cột: STT, Phiếu hạch toán / Phiếu nhập-xuất, Số phiếu, Ngày vận chuyển, Chuyến xe, Tuyến đường, KM, KM phụ trội, Cước chính, Cước phụ trội, Cước thực tế, Thuế, Cước sau thuế, Vé cầu đường, Mã NVKD, NVKD, Khách hàng, NV chịu, Công ty chịu, Xe tính cước, Xe, Mã lái xe, Lái xe.',
        '- Cây 2 cấp: dòng TỔNG → chuyến (I, II…; mã phiếu hạch toán liên kết) → phiếu nhập/xuất (1, 2…; mã phiếu liên kết mở phiếu xuất kho / nhập kho).',
        '- Cột của chuyến (ngày, chuyến xe, tuyến, km, cước, xe, lái xe) chỉ ghi ở dòng chuyến; cột NVKD, Khách hàng, NV chịu, Công ty chịu chỉ ghi ở dòng phiếu.']],
    ['Ô chọn cấp bung', 'Dropdown', 'Enable', 'Đến tuyến đường / Đến từng phiếu nhập/xuất', [
        '- Khách hàng: "Chỉ khách hàng", "Đến tuyến đường" (mặc định), "Đến từng phiếu hạch toán".', '- Chuyến xe: "Chỉ chuyến", "Đến từng phiếu nhập/xuất" (mặc định).', '- Không tải lại dữ liệu.']],
    ['Dòng TỔNG', 'Table/Grid', 'Read-only', 'Theo dữ liệu', ['- Nền cam; cộng TOÀN BỘ chuyến theo bộ lọc, mỗi chuyến 1 lần, không theo trang.', '- Icon ⓘ (Khách hàng): "%s"' % TIP['ten_kh'], '- Icon ⓘ (Chuyến xe): "%s"' % TIP['ten_cx']]],
    ['Cột Số phiếu HT / Số phiếu', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Khách hàng: số phiếu hạch toán (chuyến) của nhóm, kèm chữ "phiếu"; Chuyến xe: số phiếu nhập/xuất của chuyến.', '- Gạch chân, bấm → popup danh sách phiếu nhập/xuất của nhóm; dòng TỔNG mở "Tất cả phiếu nhập/xuất".', '- Icon ⓘ: "%s"' % TIP['count']]],
    ['Cột Xe / Lái xe', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Biển số xe chạy thực tế; tên lái xe + dòng phụ mã lái xe (lái xe công ty: mã nhân viên; lái xe ngoài: số CCCD). Chỉ ở dòng phiếu (Khách hàng) / dòng chuyến (Chuyến xe).']],
    ['Cột KM', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Tổng km thực tế ghi trên chuyến; âm hiển thị 0.', *NUM, '- Icon ⓘ: "%s"' % TIP['km']]],
    ['Cột KM phụ trội', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Km phụ trội ghi trên chuyến.', *NUM, '- Icon ⓘ: "%s"' % TIP['km_add']]],
    ['Cột Cước chính / Cước phụ trội', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Cước tính theo công thức vận chuyển / cước của km phụ trội.', *NUM, '- Icon ⓘ: "%s" / "%s"' % (TIP['main'], TIP['extra'])]],
    ['Cột Cước thực tế / Thuế / Cước sau thuế', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Khách hàng: phần của khách; Chuyến xe: số của cả chuyến. Cước sau thuế = Cước thực tế + Thuế.', *NUM, '- Icon ⓘ: "%s"' % TIP['after']]],
    ['Cột Vé cầu đường', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Vé cầu đường ghi trên chuyến.', *NUM, '- Icon ⓘ: "%s"' % TIP['toll']]],
    ['Cột Mã NVKD / NVKD', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Người lập yêu cầu xuất / nhập hàng của phiếu; Khách hàng: các NVKD của khách trên chuyến, cách nhau dấu phẩy.', '- Icon ⓘ: "%s"' % TIP['nvkd']]],
    ['Cột Khách hàng (Chuyến xe)', 'Table/Grid', 'Read-only', 'Hiển thị', ['- "Mã KH - Tên KH" của phiếu xuất / nhập; phiếu không gắn khách để trống.']],
    ['Cột NV chịu / Công ty chịu', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Dấu ✓ đậm ở cột tương ứng với đối tượng chịu phí vận chuyển của phiếu.']],
    ['Cột Xe tính cước / Mã lái xe (Chuyến xe)', 'Table/Grid', 'Read-only', 'Hiển thị', ['- "Dòng xe - Tải trọng" của xe; mã lái xe.']],
    ['Chân bảng', 'Label', 'Hiển thị', 'Theo dữ liệu', ['- "Hiển thị a–b / N khách hàng" (Khách hàng) / "… / N chuyến" (Chuyến xe); phân trang theo nhóm cấp 1.']],
    ['Ô Số dòng/trang', 'Dropdown', 'Enable', '10', ['- 10, 20, 50, 100 nhóm / trang; đổi → về trang 1.']],
    ['Nút Cấu hình cột hiển thị / In báo cáo / Xuất Excel', 'Button', 'Enable', 'Hiển thị', ['- Mục 2.6 / 2.4 / 2.5.', '- Báo cáo chưa tải xong: "Báo cáo chưa tải xong, vui lòng thử lại."']],
]

DATA_MAIN = [
    ('Tập dữ liệu / thời điểm số liệu', 'Mỗi "chuyến" = 1 phiếu hạch toán chuyến xe của chuyến ĐÃ HOÀN THÀNH, ngày tạo chuyến trong kỳ, theo phạm vi quyền (BR-02) và bộ lọc. Chuyến xe khác còn phải có phiếu hạch toán Đã hạch toán. Số liệu đọc tại thời điểm tải.', TIP['trang']),
    ('Nhóm khách hàng (góc nhìn Khách hàng)', 'Khách hàng của phiếu xuất / nhập kho trên chuyến. Phiếu không gắn khách (vd phiếu nhập kho nội bộ) → nhóm "Không có khách hàng" (luôn cuối). Xếp theo Cước sau thuế giảm dần, bằng nhau theo tên.', TIP['ten_kh']),
    ('Nhóm tuyến đường', 'Tuyến đường của chuyến; chuyến xe khác không chọn tuyến: "điểm đầu - điểm cuối"; không có: "Không có tuyến đường". Xếp theo tên.', '—'),
    ('Dòng phiếu hạch toán (Khách hàng)', 'Phần của 1 khách trên 1 chuyến. Chuyến chở hàng của ≥ 2 khách: nhãn "ghép N KH" (rê chuột xem các khách còn lại + mã phiếu), các cột KM, KM phụ trội, Cước chính, Cước phụ trội, Vé cầu đường ĐỂ TRỐNG. Xếp chuyến mới → cũ.', '—'),
    ('Nhóm chuyến (góc nhìn Chuyến xe)', '1 dòng / phiếu hạch toán, xếp ngày tạo chuyến mới → cũ; dòng con là từng phiếu xuất / nhập kho chở trên chuyến.', TIP['ten_cx']),
    ('Số phiếu HT / Số phiếu', 'Khách hàng: đếm phiếu hạch toán (chuyến) của nhóm. Chuyến xe: đếm phiếu nhập/xuất của chuyến. Dòng TỔNG: Khách hàng = số chuyến; Chuyến xe = số phiếu nhập/xuất.', TIP['count']),
    ('KM', 'Tổng km thực tế ghi trên chuyến; âm thì 0.', TIP['km']),
    ('KM phụ trội, Cước chính, Cước phụ trội, Vé cầu đường', 'Số ghi trên chuyến xe. Góc nhìn Khách hàng: chuyến ghép để trống; nhóm khách / tuyến chỉ cộng các dòng có số (cả nhóm trống thì trống).', TIP['main']),
    ('Cước thực tế, Thuế', 'Góc nhìn Chuyến xe: cước thực tế / thuế ghi trên chuyến. Góc nhìn Khách hàng: cộng cước / thuế đã chia cho từng phiếu xuất / nhập của khách khi hạch toán chuyến. Nếu thuế ở các phiếu cộng không bằng thuế chuyến thì chia thuế chuyến theo tỉ lệ cước của khách (phần lẻ dồn cho khách cuối) — có thể ra số lẻ (vd 520,573.12).', TIP['fee']),
    ('Cước sau thuế', 'Cước thực tế + Thuế.', TIP['after']),
    ('NVKD / Mã NVKD', 'Người lập yêu cầu xuất hàng (phiếu xuất) / yêu cầu nhập hàng (phiếu nhập) — áp cho cả chuyến xe chở hàng và chuyến xe khác. Dòng không gắn phiếu xuất / nhập để trống.', TIP['nvkd']),
    ('NV chịu / Công ty chịu', 'Chuyến xe chở hàng: Công ty chịu khi phiếu đánh dấu công ty chịu phí, ngược lại NV chịu. Chuyến xe khác: theo 2 dấu NV chịu / Công ty chịu ghi trên dòng phiếu.', '—'),
    ('Khối Chuyến xe', 'Phiếu hạch toán = số chuyến; "M phiếu nhập/xuất" = số dòng phiếu; Chuyến xe chở hàng / khác theo loại; Ghép nhiều KH = số chuyến có ≥ 2 khách hàng; "K khách hàng" = số khách (không tính nhóm Không có khách hàng).', TIP['blk_trips']),
    ('Khối Đối tượng chịu phí', 'Đếm số phiếu nhập/xuất NV chịu / Công ty chịu.', TIP['blk_subject']),
    ('Khối Cước vận chuyển, dòng TỔNG', 'Cộng theo CHUYẾN (mỗi chuyến 1 lần). Góc nhìn Khách hàng: Cước thực tế / Thuế / Cước sau thuế dòng TỔNG = cộng phần của các khách đang hiện.', TIP['blk_money']),
    ('Ràng buộc khớp số', '- Góc nhìn Khách hàng: Cước thực tế / Thuế / Cước sau thuế dòng TỔNG = tổng các nhóm khách hàng; 1 chuyến ghép = tổng phần của các khách trên chuyến đó.\n- KM, Cước chính, Cước phụ trội, Vé cầu đường dòng TỔNG có thể LỚN HƠN tổng các nhóm khách (chuyến ghép để trống ở dòng khách).\n- Hai góc nhìn cùng bộ lọc: các cột tiền / km dòng TỔNG bằng nhau.', '—'),
]

POPUP_MAIN = [
    ('Ô số ở khối Chuyến xe (Phiếu hạch toán / Chuyến xe chở hàng / Chuyến xe khác / Ghép nhiều KH)', 'Danh sách phiếu nhập/xuất (mục 2.3)', 'Các phiếu xuất / nhập kho chở trên các chuyến của con số', 'Phiếu theo bộ lọc, thu theo loại chuyến / chuyến ghép'),
    ('Ô NV chịu / Công ty chịu', 'Danh sách phiếu nhập/xuất — "Phiếu nhân viên chịu phí" / "Phiếu công ty chịu phí"', 'Phiếu nào do nhân viên / công ty chịu phí', 'Phiếu có đúng đối tượng chịu phí'),
    ('Số ở dòng TỔNG', 'Danh sách — "Tất cả phiếu nhập/xuất"', 'Toàn bộ phiếu của báo cáo', 'Mọi phiếu theo bộ lọc'),
    ('Số ở dòng khách hàng / tuyến (Khách hàng)', 'Danh sách — "<khách hàng>" / "<khách hàng> › <tuyến>"', 'Phiếu của khách (trên tuyến)', 'Phiếu của đúng khách / tuyến'),
    ('Số ở dòng chuyến (Chuyến xe)', 'Danh sách — "<mã phiếu hạch toán>"', 'Phiếu của 1 chuyến', 'Phiếu của chuyến; ẩn ô Chọn phiếu hạch toán'),
    ('Mã phiếu hạch toán, chuyến xe, phiếu nhập/xuất', 'Không phải popup — mở màn chi tiết ở tab mới', 'Xem chứng từ gốc', 'Đúng chứng từ'),
    ('Ô tiền, km', 'Không bấm được', '—', '—'),
]

FR.append({
    'ten': 'Xem báo cáo chi tiết chuyến xe',
    'qtc': 'Màn Báo cáo, Phân trang, Định dạng số.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem báo cáo chi tiết chuyến xe'],
        ['Mô tả', 'Hiển thị từng chuyến xe đã hoàn thành trong kỳ với cước tính toán, cước thực tế, thuế, vé cầu đường, xe, lái xe và các phiếu xuất / nhập kho; xem theo khách hàng (phần cước của từng khách) hoặc theo chuyến xe. Màn chỉ đọc.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải ngay báo cáo kỳ "Tháng này", góc nhìn "Khách hàng": khối tổng hợp, dòng TỔNG, trang 1 gồm 10 khách hàng bung đến tuyến đường.\n3. Người dùng đổi bộ lọc / góc nhìn (mục 2.2), bấm số xem danh sách phiếu (mục 2.3), bấm mã chứng từ mở tab mới.'],
        ['Dòng sự kiện phụ', '• Không có chuyến: khối tổng hợp hiện 0, bảng "Không có chuyến xe nào khớp bộ lọc."\n• Đổi "Xem theo": bảng dựng lại với bộ cột của góc nhìn mới, cấp bung về mặc định.\n• Lỗi tải: báo lỗi, giữ số liệu đang hiện.\n• Chuyển trang / đổi số dòng: dòng TỔNG, khối tổng hợp không đổi.\n• Phiên đăng nhập hết hạn: hệ thống báo và đưa về màn đăng nhập (quy tắc chung).'],
        ['Yêu cầu đặc biệt', 'Môi trường thử nghiệm 18/11/2026: kỳ 1 tháng (56 chuyến) dưới 0,5 giây; kỳ "Năm nay" (2.313 chuyến, 3.880 phiếu) khoảng 0,7–0,8 giây.'],
    ],
    'anh': [('01_open', 'Màn Báo cáo chi tiết chuyến xe lúc mới mở (kỳ Tháng này chưa có chuyến)'),
            ('03_report', 'Kỳ Tháng trước (tháng 10/2026), xem theo Khách hàng — bung đến tuyến đường'),
            ('03d_level3', 'Bung đến từng phiếu hạch toán — chuyến ghép 2 khách có nhãn "ghép 2 KH"'),
            ('04_trip', 'Xem theo Chuyến xe — chuyến ▸ phiếu nhập/xuất'),
            ('04b_tip', 'Icon ⓘ ở tiêu đề cột Cước sau thuế')],
    'ui': ui(UI6, COT),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Không kiểm quyền vào màn; đọc phạm vi (BR-02) để mở / khoá ô Công ty.\nAfter:\n– Tải báo cáo kỳ "Tháng này", góc nhìn Khách hàng, 10 nhóm / trang.'],
        ['Đổi ô lọc / Xem theo / bấm Tìm kiếm', 'Change / Click', 'Xem mục 2.2.'],
        ['Chọn cấp bung / bấm mũi tên', 'Change / Click', 'After:\n– Ẩn / hiện dòng con; không tải lại.'],
        ['Chuyển trang / đổi Số dòng/trang', 'Click / Change', 'After:\n– Tải trang nhóm mới, giữ bộ lọc, dòng TỔNG.'],
        ['Bấm con số gạch chân', 'Click', 'After:\n– Mở popup danh sách phiếu nhập/xuất (mục 2.3).'],
        ['Bấm mã phiếu hạch toán / chuyến xe / phiếu nhập-xuất', 'Click', 'After:\n– Mở màn chi tiết tương ứng ở tab mới.'],
        ['Rê chuột vào nhãn "ghép N KH"', 'Hover', 'After:\n– Hiện: "Chuyến chở hàng của N khách hàng — cước / thuế ở dòng này là phần của khách đang xem.", "KM, cước chính / phụ trội, vé cầu đường của cả chuyến để trống (xem ở góc nhìn "Chuyến xe").", "Các khách hàng khác trên chuyến:" + danh sách khách kèm mã phiếu.'],
        ['Rê chuột vào icon ⓘ', 'Hover', 'After:\n– Hiện chú thích cách tính (bảng 2.1.5).'],
    ],
    'them': [
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', [
            ('p', 'Bảng dưới mô tả cách hệ thống tính từng chỉ tiêu, từng cột và nội dung icon ⓘ trên giao diện.'),
            ('data', DATA_MAIN)]),
        ('Danh sách popup mở từ số liệu', [('popup', POPUP_MAIN)]),
    ],
})

# ================================================================ 2.2 Tìm kiếm và lọc
FR.append({
    'ten': 'Tìm kiếm và lọc',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc báo cáo'],
        ['Mô tả', 'Chọn kỳ, góc nhìn, thu hẹp theo công ty / chứng từ / chuyến / tuyến / lái xe / xe / đối tượng chịu phí / phòng ban / bộ phận / nhân viên kinh doanh.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn Báo cáo chi tiết chuyến xe.'],
        ['Dòng sự kiện chính', '1. Người dùng chọn ô dạng danh sách → báo cáo tải lại ngay, về trang 1.\n2. Người dùng gõ ô dạng chữ (Phiếu hạch toán, Chuyến xe, Lái xe, Phiếu nhập/xuất) rồi nhấn Enter hoặc bấm Tìm kiếm.\n3. Hệ thống áp đồng thời mọi điều kiện.'],
        ['Dòng sự kiện phụ', '• Kỳ "Tuỳ chọn" thiếu ngày mà bấm Tìm kiếm → "Chọn đủ ngày bắt đầu và ngày kết thúc của kỳ Tuỳ chọn."; Đến ngày < Từ ngày → "Ngày kết thúc phải sau hoặc bằng ngày bắt đầu".\n• Đổi Công ty → xoá Phòng ban, Bộ phận, Nhân viên kinh doanh; đổi Phòng ban → xoá Bộ phận, Nhân viên kinh doanh.\n• Xóa lọc → Kỳ "Tháng này", Xem theo "Khách hàng", các ô khác trống (giữ công ty bị khoá), tải lại.'],
    ],
    'anh': [('07_filter_subject', 'Lọc Đối tượng chịu phí = Nhân viên chịu: còn 7 chuyến, 6 khách hàng'),
            ('07b_filter_doc', 'Lọc Phiếu hạch toán "03199" (gõ rồi nhấn Enter)')],
    'ui': ui(UI7, [
        ['Ô Kỳ', 'Dropdown', 'Enable', 'Tuần này, Tháng này, Tháng trước, Năm nay, Tuỳ chọn', 'Tháng này', ['- Lọc theo ngày tạo chuyến; icon ⓘ: "%s"' % TIP['ky'], '- Tuỳ chọn: hiện ô Thời gian (Từ ngày → Đến ngày).']],
        ['Ô Xem theo', 'Dropdown', 'Enable', 'Khách hàng, Chuyến xe', 'Khách hàng', ['- Không xoá trống được; icon ⓘ: "%s"' % TIP['xemtheo']]],
        ['Ô Công ty', 'Dropdown', 'Enable / Disable', 'Công ty đang hoạt động', 'Trống (tất cả)', ['- Mở khi có quyền mức Tổng công ty; khác: khoá ở công ty của người xem.', '- Giữ chuyến có ≥ 1 phiếu thuộc yêu cầu xuất / nhập hàng của công ty đã chọn.']],
        ['Ô Phiếu hạch toán', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', ['- Placeholder "Mã phiếu hạch toán chuyến xe"; gần đúng; Enter / Tìm kiếm.']],
        ['Ô Chuyến xe', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', ['- Placeholder "Mã chuyến xe"; gần đúng theo mã chuyến.']],
        ['Ô Tuyến đường', 'Dropdown', 'Enable', 'Tuyến đường đang hoạt động', 'Trống', ['- Đúng tuyến đã chọn trên chuyến.']],
        ['Ô Lái xe', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', ['- Placeholder "Tên lái xe"; gần đúng theo tên lái xe công ty / lái xe ngoài.']],
        ['Ô Biển số xe', 'Dropdown', 'Enable', 'Biển số đang hoạt động', 'Trống', ['- Biển số ghi trên chuyến.']],
        ['Ô Phiếu nhập/xuất', 'Textbox', 'Enable', 'Chữ tự do', 'Trống', ['- Placeholder "Mã phiếu xuất / nhập kho"; gần đúng. Chỉ giữ chuyến có phiếu khớp VÀ chỉ hiện dòng phiếu khớp.']],
        ['Ô Đối tượng chịu phí', 'Dropdown', 'Enable', 'Nhân viên chịu, Công ty chịu', 'Trống', ['- Chỉ giữ chuyến có phiếu khớp và chỉ hiện dòng phiếu khớp.']],
        ['Ô Phòng ban / Bộ phận', 'Dropdown', 'Enable', 'Theo công ty / phòng ban', 'Trống', ['- Phòng ban / bộ phận ghi trên yêu cầu xuất / nhập hàng; Bộ phận lọc theo Phòng ban đã chọn.']],
        ['Ô Nhân viên kinh doanh', 'Dropdown', 'Enable', '"Mã - Tên" nhân viên', 'Trống', ['- Người lập yêu cầu xuất / nhập hàng.']],
        ['Nút Tìm kiếm / Xóa lọc / Cài đặt bộ lọc / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', ['- Tải lại; về mặc định; chọn ô hiển thị; thu gọn / mở khu vực lọc.']],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Chọn ô dạng danh sách', 'Change', 'After:\n– Tải lại từ trang 1 (kỳ Tuỳ chọn chưa đủ ngày thì chưa tải).'],
        ['Gõ ô dạng chữ', 'Keypress', 'After:\n– Chưa lọc; chờ Enter / Tìm kiếm.'],
        ['Đổi Xem theo', 'Change', 'After:\n– Bỏ bảng cũ, tải lại với cây + cột của góc nhìn mới, cấp bung về mặc định; cấu hình cột lưu riêng từng góc nhìn.'],
        ['Bấm Xóa lọc', 'Click', 'After:\n– Mọi ô về mặc định, tải lại.'],
    ],
})

# ================================================================ 2.3 Popup
POP = [
    ['Tiêu đề popup', 'Label', 'Hiển thị', 'Theo ô số', ['- vd "Tất cả phiếu nhập/xuất", "Chuyến chở hàng của nhiều khách hàng", "Phiếu nhân viên chịu phí", "<khách hàng> - <mã KH>".', '- Dòng phụ "N phiếu · M chuyến · Kỳ <nhãn kỳ>".']],
    ['Ô tìm', 'Textbox', 'Enable', 'Trống', ['- Placeholder "Tìm phiếu nhập/xuất / khách hàng / NVKD / xe / lái xe…"; lọc ngay, không phân biệt hoa thường / dấu; nút ×.']],
    ['Ô Chọn phiếu hạch toán / Chọn loại chuyến', 'Dropdown', 'Enable / Ẩn', 'Trống', ['- Ẩn khi ô số đã cố định chuyến / loại chuyến.']],
    ['Bộ đếm', 'Label', 'Hiển thị', '"n / N phiếu"', ['- n sau lọc trong popup.']],
    ['Bảng', 'Table/Grid', 'Read-only', 'Theo dữ liệu', ['- 11 cột: STT, Ngày vận chuyển, Phiếu hạch toán, Chuyến xe, Phiếu nhập/xuất, Khách hàng, NVKD (kèm mã), NV chịu, Công ty chịu, Xe, Lái xe.', '- Sắp xếp được theo cột có mũi tên; 10 dòng/trang (10/20/50/100).', '- Không có dòng: "Không có phiếu xuất / nhập nào khớp bộ lọc."']],
    ['Nút In danh sách', 'Button', 'Enable', '–', ['- Chọn cột rồi xem trước "DANH SÁCH PHIẾU NHẬP/XUẤT THEO CHUYẾN XE".']],
    ['Nút Xuất Excel danh sách', 'Button', 'Enable', '–', ['- Tải ngay file danh_sach_phieu_nhap_xuat_theo_chuyen_xe_yyyymmdd.xlsx gồm các dòng đang hiện (đã lọc + sắp): tiêu đề "DANH SÁCH PHIẾU NHẬP/XUẤT THEO CHUYẾN XE", dòng kỳ + điều kiện lọc, dòng "Phạm vi: <tiêu đề popup>", cột STT, Phiếu nhập/xuất, Ngày vận chuyển, Phiếu hạch toán, Chuyến xe, Loại chuyến, Khách hàng, Mã NVKD, NVKD, NV chịu, Công ty chịu, Xe, Lái xe.']],
    ['Nút Đóng', 'Button', 'Enable', '–', ['- Đóng popup.']],
]
FR.append({
    'ten': 'Xem danh sách phiếu nhập/xuất', 'uc': 'uc_danhsach',
    'qtc': 'Popup, Định dạng số.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách phiếu nhập/xuất của con số'],
        ['Mô tả', 'Popup liệt kê các phiếu xuất / nhập kho (kèm chuyến) tạo nên con số đã bấm; lọc / sắp xếp / in / xuất Excel tại chỗ.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_DATA + '\n4. Ô số bấm vào lớn hơn 0.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm con số gạch chân.\n2. Hệ thống mở popup, tải đủ mọi phiếu của ô số theo bộ lọc màn chính.\n3. Người dùng tìm, lọc, sắp xếp; In danh sách / Xuất Excel danh sách / Đóng.'],
        ['Dòng sự kiện phụ', '• Chuyến không có phiếu xuất / nhập nào không có dòng trong popup (nên "M chuyến" ở popup có thể nhỏ hơn số chuyến ở báo cáo).\n• Lỗi tải: báo lỗi; lỗi xuất: "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Bấm số phiếu {icon:lnk_sophieu}',
    'ghi_chu_layout': POPUP % 'danh sách phiếu nhập/xuất',
    'anh': [('05_drill', 'Popup "Tất cả phiếu nhập/xuất" (bấm số ở dòng TỔNG)'),
            ('05b_drill_shared', 'Popup "Chuyến chở hàng của nhiều khách hàng" (ô Ghép nhiều KH)')],
    'ui': ui(UI6, POP),
    'ui_widths': UI6W,
    'events': [
        ['Bấm con số', 'Click', 'After:\n– Mở popup, tải đủ phiếu của ô số.'],
        ['Gõ ô tìm / chọn ô lọc / bấm tiêu đề cột', 'Keypress / Change / Click', 'After:\n– Lọc / sắp xếp ngay trong popup.'],
        ['Bấm In danh sách', 'Click', 'After:\n– Cửa sổ chọn cột → xem trước bản in.'],
        ['Bấm Xuất Excel danh sách', 'Click', 'After:\n– Dựng file ngay trên trình duyệt từ các dòng đang hiện, tải về.'],
        ['Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup.'],
    ],
    'them': [
        ('Mục đích thiết kế popup', [
            ('bullet', 'Trả lời "con số này gồm những phiếu xuất / nhập nào, của khách nào, NVKD nào, ai chịu phí".'),
            ('bullet', 'Là popup để giữ nguyên báo cáo và bộ lọc.'),
            ('bullet', 'Ràng buộc khớp số: số dòng = số phiếu nhập/xuất của ô số (ở khối Chuyến xe: "M phiếu nhập/xuất").'),
        ]),
        ('Các biến thể theo con số bấm', [('variant', [
            ('Phiếu hạch toán / dòng TỔNG', 'Mọi phiếu theo bộ lọc', 'Tất cả phiếu nhập/xuất', 'Hiện cả 2 ô lọc'),
            ('Chuyến xe chở hàng / Chuyến xe khác', 'Phiếu của loại chuyến đó', 'Chuyến xe chở hàng / Chuyến xe khác', 'Ẩn Chọn loại chuyến'),
            ('Ghép nhiều KH', 'Phiếu của chuyến có ≥ 2 khách', 'Chuyến chở hàng của nhiều khách hàng', 'Hiện cả 2 ô lọc'),
            ('NV chịu / Công ty chịu', 'Phiếu có đúng đối tượng chịu phí', 'Phiếu nhân viên chịu phí / Phiếu công ty chịu phí', 'Hiện cả 2 ô lọc'),
            ('Dòng khách hàng / tuyến', 'Phiếu của khách (trên tuyến)', '<khách hàng> / <khách hàng> › <tuyến>', 'Hiện cả 2 ô lọc'),
            ('Dòng chuyến (Chuyến xe)', 'Phiếu của chuyến', '<mã phiếu hạch toán>', 'Ẩn Chọn phiếu hạch toán'),
        ])]),
    ],
})

# ================================================================ 2.4 In
FR.append({
    'ten': 'In báo cáo', 'uc': 'uc_in',
    'qtc': 'In.',
    'gioi_thieu': [
        ['Tên chức năng', 'In báo cáo chi tiết chuyến xe'],
        ['Mô tả', 'Chọn bản in (bảng tổng hợp theo góc nhìn đang xem / danh sách phiếu nhập/xuất) và cột, xem trước rồi in; luôn lấy mọi trang theo bộ lọc đang hiển thị.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_DATA],
        ['Dòng sự kiện chính', '1. Bấm In báo cáo.\n2. Cửa sổ "In báo cáo": "In bảng tổng hợp" ("Đúng bảng đang xem, đủ mọi trang và mọi phiếu hạch toán, kèm dòng TỔNG.") / "Danh sách phiếu nhập/xuất"; "Chọn cột in".\n3. Chọn, bấm In → cửa sổ "Xem trước báo cáo chi tiết chuyến xe".\n4. Bấm In trong cửa sổ xem trước.'],
        ['Dòng sự kiện phụ', '• Bỏ hết cột: "Vui lòng chọn ít nhất 1 cột để in".\n• Vượt 2.000 dòng: chỉ báo vượt mức in tối đa 2,000 dòng, ẩn nút In.\n• Hủy / × → đóng.'],
    ],
    'menu_them': ' => In báo cáo {icon:btn_in}',
    'ghi_chu_layout': POPUP % 'In báo cáo',
    'anh': [('09_print_opt', 'Cửa sổ In báo cáo (góc nhìn Khách hàng)'), ('10_print', 'Xem trước bản in bảng tổng hợp theo khách hàng')],
    'ui': ui(UI6, [
        ['In bảng tổng hợp — Khách hàng', 'Radio', 'Enable', 'Được chọn', ['- 17 cột chọn được: Số phiếu hạch toán, Ngày vận chuyển, Chuyến xe, Xe, Mã lái xe, Tên lái xe, KM, KM phụ trội, Cước chính, Cước phụ trội, Cước thực tế, Thuế, Cước sau thuế, Vé cầu đường, NV kinh doanh, NV chịu, Công ty chịu.', '- Bản in 3 cấp: TỔNG → "Mã KH - Tên KH" (I…) → tuyến (1…) → phiếu (1.1…); chuyến ghép ghi "(ghép N KH)"; dòng kỳ kèm "· Xem theo khách hàng".']],
        ['In bảng tổng hợp — Chuyến xe', 'Radio', 'Enable', 'Được chọn', ['- Cột chọn được = các cột của bảng góc nhìn Chuyến xe; bản in 2 cấp chuyến → phiếu nhập/xuất.']],
        ['Danh sách phiếu nhập/xuất', 'Radio', 'Enable', 'Không', ['- "Mỗi dòng 1 phiếu xuất / nhập kho kèm chuyến xe của nó, đúng bộ lọc báo cáo hiện tại."', '- 12 cột: Ngày vận chuyển, Phiếu hạch toán, Chuyến xe, Loại chuyến, Phiếu nhập/xuất, Khách hàng, Mã NVKD, NVKD, NV chịu, Công ty chịu, Xe, Lái xe.']],
        ['Chọn cột in / Chọn tất cả', 'Checkbox', 'Enable', 'Tích tất cả', ['- Icon ⓘ "Cột STT luôn được in."']],
        ['Nút In / Hủy', 'Button', 'Enable', '–', ['- Mở xem trước / đóng.']],
        ['Cửa sổ xem trước', 'Label', 'Read-only', 'Theo dữ liệu', ['- Tiêu đề công ty, "BÁO CÁO CHI TIẾT CHUYẾN XE", dòng kỳ + điều kiện lọc + góc nhìn, bảng, "Người lập".']],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In báo cáo', 'Click', 'Before:\n– Chưa tải xong → "Báo cáo chưa tải xong, vui lòng thử lại.".\nAfter:\n– Mở cửa sổ chọn bản + cột.'],
        ['Bấm In (cửa sổ chọn)', 'Click', 'After:\n– Dựng bản in theo bộ lọc + góc nhìn đang hiển thị, mọi trang.'],
    ],
})

# ================================================================ 2.5 Xuất Excel
FR.append({
    'ten': 'Xuất Excel', 'uc': 'uc_xuat',
    'qtc': 'Xuất Excel.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất báo cáo ra Excel'],
        ['Mô tả', 'Tải ngay file Excel bảng cây đang xem (đủ mọi trang, mọi cấp) theo góc nhìn; không qua cửa sổ chọn cột.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_DATA],
        ['Dòng sự kiện chính', '1. Bấm Xuất Excel.\n2. Hệ thống lấy toàn bộ dữ liệu theo bộ lọc đang hiển thị, dựng file ngay trên trình duyệt (hiện biểu tượng đang xử lý).\n3. Tải file "bao_cao_chi_tiet_chuyen_xe_theo_khach_hang_yyyymmdd.xlsx" (sheet "Theo khách hàng") hoặc "bao_cao_chi_tiet_chuyen_xe_theo_chuyen_xe_yyyymmdd.xlsx" (sheet "Theo chuyến xe").'],
        ['Dòng sự kiện phụ', '• Lỗi: "Lỗi khi xuất Excel".\n• Kỳ cả năm: thời gian tạo file khoảng chục giây.'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'File được tải về ngay sau khi bấm nút trên màn báo cáo theo đường dẫn ở trên.',
    'anh': [('03_report', 'Nút Xuất Excel ở cụm nút trên khu vực lọc')],
    'ui': ui(UI6, [
        ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', ['- Tải file ngay, không mở cửa sổ chọn.']],
        ['File Excel', 'File', '–', '–', ['- Logo công ty, tiêu đề "BÁO CÁO CHI TIẾT CHUYẾN XE", dòng điều kiện lọc (nghiêng); hàng tiêu đề STT, cột cây, các cột của góc nhìn (góc nhìn Khách hàng tách Ngày vận chuyển, Chuyến xe, Mã lái xe thành cột riêng).', '- Dòng TỔNG nền cam, nhóm cấp 1 xanh đậm, cấp 2 xanh nhạt, dòng lá trắng; số 0 ở dòng lá để trống; cố định tiêu đề + 2 cột đầu; khối ký "Người lập" cuối.']],
    ]),
    'ui_widths': UI6W,
    'events': [['Bấm Xuất Excel', 'Click', 'Before:\n– Chưa tải xong → "Báo cáo chưa tải xong, vui lòng thử lại.".\nAfter:\n– Lấy mọi nhóm theo bộ lọc + góc nhìn, dựng và tải file.']],
})

# ================================================================ 2.6 Tuỳ chỉnh cột
FR.append({
    'ten': 'Tùy chỉnh cột hiển thị',
    'qtc': 'Tùy chỉnh cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tùy chỉnh cột hiển thị'],
        ['Mô tả', 'Ẩn / hiện và đổi thứ tự cột của bảng; lưu theo người dùng, RIÊNG cho từng góc nhìn (Khách hàng / Chuyến xe). Không ảnh hưởng In / Xuất Excel.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Bấm Cấu hình cột hiển thị.\n2. Cửa sổ "Tuỳ chỉnh cột" theo góc nhìn đang chọn.\n3. Tích / bỏ tích, kéo ☰, bấm Lưu → "Cập nhật thành công".'],
        ['Dòng sự kiện phụ', '• STT và cột cây (Khách hàng / Tuyến đường / Phiếu hạch toán hoặc Phiếu hạch toán / Phiếu nhập-xuất) luôn hiện.\n• Đóng → bỏ thay đổi; lỗi lưu: "Thao tác thất bại".'],
    ],
    'menu_them': ' => Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': POPUP % 'Tuỳ chỉnh cột',
    'anh': [('12_colcfg', 'Cửa sổ Tuỳ chỉnh cột (góc nhìn Khách hàng)')],
    'ui': ui(UI6, [
        ['Danh sách cột', 'Checkbox', 'Enable', 'Theo cấu hình đã lưu', ['- Khách hàng: 16 mục (STT, cột cây khoá + 14 cột). Chuyến xe: 23 mục (STT, cột cây khoá + 21 cột).']],
        ['Nút Chọn tất cả / Bỏ chọn hết, dòng đếm', 'Button', 'Enable', '–', ['- "Đang chọn x/y cột".']],
        ['Nút Lưu / Đóng', 'Button', 'Enable', '–', ['- Lưu: áp dụng + lưu; Đóng: không áp dụng.']],
    ]),
    'ui_widths': UI6W,
    'events': [['Bấm Lưu', 'Click', 'After:\n– Áp dụng lên bảng của góc nhìn đang xem, lưu theo người dùng.'], ['Đổi Xem theo', 'Change', 'After:\n– Nạp cấu hình cột của góc nhìn mới.']],
})

PERMS = [
    ('Xem báo cáo vận chuyển — mức Tổng công ty; hoặc Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh — mức Tổng công ty', 'Thấy mọi chuyến; ô Công ty mở.'),
    ('Xem báo cáo vận chuyển — mức Công ty; hoặc Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh — mức Công ty', 'Thấy chuyến thuộc công ty của người xem (công ty ghi trên chuyến xe); ô Công ty khoá.'),
    ('Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh — mức Phòng ban', 'Thấy chuyến thuộc phòng ban của người xem (phòng ban ghi trên chuyến xe); ô Công ty khoá.'),
    ('(Không có quyền nào)', 'Chỉ thấy chuyến do chính mình lập; ô Công ty khoá.'),
]
FUNCS = ['FR-01 Xem báo cáo chi tiết chuyến xe', 'FR-02 Tìm kiếm và lọc', 'FR-03 Xem danh sách phiếu nhập/xuất', 'FR-04 In báo cáo', 'FR-05 Xuất Excel', 'FR-06 Tùy chỉnh cột hiển thị']

S = {
    'ten': TEN,
    'menu': [('Vận chuyển', 'menu_phanhe'), ('Báo cáo vận chuyển', 'menu_nhom'), (TEN, 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu màn báo cáo.',
        'Phạm vi chức năng: Xem báo cáo (2 góc nhìn Khách hàng / Chuyến xe), Tìm kiếm và lọc, Xem danh sách phiếu nhập/xuất (popup), In báo cáo, Xuất Excel, Tùy chỉnh cột. Màn chỉ đọc.',
        'Mục đích sử dụng dữ liệu: biết cước vận chuyển của từng khách / từng chuyến, chuyến ghép nhiều khách, NVKD và đối tượng chịu phí của từng phiếu.',
        'Làm rõ cách chia cước cho khách, quy tắc để trống cột của chuyến ghép, phạm vi dữ liệu theo quyền.',
    ],
    'thuat_ngu': [
        ['Chuyến', 'Một phiếu hạch toán chuyến xe của chuyến xe chở hàng / chuyến xe khác đã hoàn thành.'],
        ['Ngày vận chuyển', 'Ngày tạo chuyến xe; dùng để xếp kỳ.'],
        ['Phiếu nhập/xuất', 'Phiếu xuất kho / phiếu nhập kho chở trên chuyến.'],
        ['Chuyến ghép', 'Chuyến chở hàng của từ 2 khách hàng trở lên (nhãn "ghép N KH").'],
        ['Phần của khách', 'Cước / thuế kế toán đã chia cho các phiếu xuất / nhập của khách khi hạch toán chuyến.'],
        ['NVKD', 'Nhân viên kinh doanh — người lập yêu cầu xuất / nhập hàng của phiếu.'],
        ['NV chịu / Công ty chịu', 'Đối tượng chịu phí vận chuyển của phiếu.'],
        ['Góc nhìn', 'Cách dựng bảng theo ô "Xem theo": Khách hàng hoặc Chuyến xe.'],
    ],
    'quyen_truoc': [
        'Màn KHÔNG chặn quyền vào: mọi người dùng đăng nhập đều thấy menu, mở được màn và dùng mọi chức năng. Hai quyền "Xem báo cáo vận chuyển" (phân hệ Kho, mức Công ty / Tổng công ty) và "Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh" (phân hệ Bán hàng, mức Phòng ban / Công ty / Tổng công ty) chỉ mở rộng PHẠM VI DỮ LIỆU; có nhiều quyền / mức thì lấy phạm vi rộng nhất.',
    ],
    'quyen_rows': [list(p) for p in PERMS],
    'ma_tran': [['Chức năng', 'Tổng công ty', 'Công ty', 'Phòng ban', 'Không quyền']] + [[f, 'Có', 'Có', 'Có', 'Có'] for f in FUNCS],
    'ma_tran_widths': [2.6, 0.9, 0.8, 0.9, 0.9],
    'quyen_sau': [
        'Phạm vi xét trên CHUYẾN XE (công ty / phòng ban / người lập chuyến), áp cho mọi con số, popup, bản in, file Excel.',
        'Ô lọc Công ty / Phòng ban / Bộ phận / Nhân viên kinh doanh lọc theo YÊU CẦU xuất / nhập hàng của phiếu — khác với phạm vi quyền.',
    ],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Kỳ báo cáo', ['– Mặc định "Tháng này"; Tuần này, Tháng trước, Năm nay, Tuỳ chọn (đủ 2 ngày, tính cả 2 đầu, Đến ngày ≥ Từ ngày).', '– Xếp kỳ theo NGÀY TẠO CHUYẾN XE.'], ['Xem báo cáo', 'Tìm kiếm và lọc']),
        ('BR-02', 'Phạm vi dữ liệu', ['– Tổng công ty: mọi chuyến.', '– Công ty: chuyến có công ty = công ty của người xem.', '– Phòng ban (chỉ quyền chi phí vận chuyển theo NVKD): chuyến có phòng ban = phòng ban của người xem.', '– Không quyền: chuyến do mình lập.', '– Không xác định được công ty / phòng ban của người xem thì không thấy chuyến nào ở mức đó.'], ['Mọi chức năng hiện số liệu']),
        ('BR-03', 'Chuyến lên báo cáo', ['– Chuyến xe chở hàng / chuyến xe khác ở trạng thái Hoàn thành, có phiếu hạch toán chuyến xe.', '– Chuyến xe khác: phiếu hạch toán phải Đã hạch toán.', '– 1 phiếu hạch toán = 1 chuyến.'], ['Xem báo cáo']),
        ('BR-04', 'Hai góc nhìn', ['– Khách hàng (mặc định): Khách hàng ▸ Tuyến đường ▸ Phiếu hạch toán; khách xếp Cước sau thuế giảm dần, "Không có khách hàng" cuối.', '– Chuyến xe: Chuyến ▸ Phiếu nhập/xuất; chuyến mới → cũ.', '– Phân trang theo nhóm cấp 1, mặc định 10.'], ['Xem báo cáo', 'In', 'Xuất Excel']),
        ('BR-05', 'Chia cước cho khách', ['– Cước thực tế / Thuế của khách = cộng phần đã chia cho các phiếu của khách.', '– Thuế ở phiếu không khớp thuế chuyến → chia thuế chuyến theo tỉ lệ cước, phần lẻ dồn khách cuối.', '– Cộng các khách = cước / thuế của chuyến.'], ['Xem báo cáo', 'In', 'Xuất Excel']),
        ('BR-06', 'Chuyến ghép nhiều khách', ['– Nhãn "ghép N KH"; KM, KM phụ trội, Cước chính, Cước phụ trội, Vé cầu đường để trống ở dòng khách.', '– Dòng TỔNG cộng các cột này mỗi chuyến 1 lần ⇒ có thể lớn hơn tổng các khách.'], ['Xem báo cáo', 'In', 'Xuất Excel']),
        ('BR-07', 'KM, NVKD, đối tượng chịu phí', ['– KM âm hiển thị 0.', '– NVKD = người lập yêu cầu xuất / nhập hàng (cả chuyến xe khác).', '– Chuyến xe chở hàng: không đánh dấu công ty chịu thì là NV chịu.'], ['Xem báo cáo']),
        ('BR-08', 'Ô lọc qua phiếu nhập/xuất', ['– Công ty, Phòng ban, Bộ phận, Nhân viên kinh doanh, Phiếu nhập/xuất, Đối tượng chịu phí: giữ chuyến có ≥ 1 phiếu khớp.', '– Riêng Phiếu nhập/xuất và Đối tượng chịu phí còn ẩn các dòng phiếu không khớp; 4 ô còn lại vẫn hiện mọi phiếu của chuyến.', '– Ô chữ lọc gần đúng, chỉ áp khi Enter / Tìm kiếm.'], ['Tìm kiếm và lọc']),
        ('BR-09', 'Định dạng số', ['– 1,234,567, tối đa 2 số lẻ; số âm có "-".', '– Dòng TỔNG / nhóm: 0 in "0"; dòng phiếu, popup: 0 để trống.'], ['Xem báo cáo', 'Xem danh sách phiếu nhập/xuất']),
        ('BR-10', 'In / Xuất Excel / cấu hình cột', ['– In / Excel lấy MỌI dòng theo bộ lọc + góc nhìn đang hiển thị; In tối đa 2.000 dòng.', '– Excel bảng tổng hợp xuất đủ cột, không chọn cột.', '– Cấu hình cột lưu theo người dùng + góc nhìn, không ảnh hưởng In / Excel.'], ['In', 'Xuất Excel', 'Tùy chỉnh cột hiển thị']),
    ],
    'phan5': {
        'cau_dan': 'Báo cáo chỉ đọc. Các màn hình dưới đây ghi ra số liệu mà báo cáo đọc (chuyến xe, phiếu hạch toán, phiếu xuất / nhập kho, yêu cầu xuất / nhập hàng), dùng chung nguồn / quyền, hoặc cung cấp danh mục.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng đã đăng nhập',
    'mains': [('FR-01', 'Xem báo cáo chi tiết chuyến xe', 'view'), ('FR-04', 'In báo cáo', 'io'), ('FR-05', 'Xuất Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc', 'view'), ('FR-03', 'Xem danh sách phiếu nhập/xuất', 'view'), ('FR-06', 'Tùy chỉnh cột hiển thị', 'view')],
    'rieng': [('FR-03', 'Xem danh sách phiếu nhập/xuất', 'view', 'uc_danhsach'), ('FR-04', 'In báo cáo', 'io', 'uc_in'), ('FR-05', 'Xuất Excel', 'io', 'uc_xuat')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', D.build_srs_report(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)

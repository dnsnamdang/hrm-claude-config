# -*- coding: utf-8 -*-
"""SRS - Báo cáo hiệu quả gộp xe vận tải (form Danh mục quốc gia + quy tắc màn BÁO CÁO của skill srs-documenter).

Khuôn: sale-customer-debt-reports/docs/compare/gen_srs.py (mẫu báo cáo đã duyệt) — hàm dựng chép sang _trp_docs.py.
Nguồn (code HRM develop 18/11/2026):
  FE hrm-client/pages/transport/trip-gross-reports/by-vehicle/index.vue, pages/transport/components/{TransportReportPage,
     TransportReportTable, TransportReportSummary, TransportItemModal, configs/tripGross.js, format.js},
     components/subsystem-menu/transport.js
  BE Modules/Finance/Http/Controllers/V1/{TransportReportController, TripGrossReportController},
     Services/DriverCostReport/{TripGrossReportService, TripAccountingQuery, TripGrossReportPrintService,
     TransportReportPrintService, DriverCostReportService}, Services/Concerns/ResolvesReportPeriod;
     quyền: app/Support/Permissions/Catalog/warehouse.php (warehouse.bao_cao_van_chuyen.view)
Ảnh: hdsd_shots/ (capture.js, dev-hrm 18/11/2026).
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _trp_docs as D  # noqa: E402
from _trp_docs import L, ui, UI6, UI6W, UI7, UI7W  # noqa: E402

TEN = 'Báo cáo hiệu quả gộp xe vận tải'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q = 'Người dùng đã đăng nhập (mọi người dùng; quyền chỉ quyết định phạm vi dữ liệu)'
DK = '1. Người dùng đăng nhập thành công.\n2. Không cần quyền để mở màn; phạm vi dữ liệu theo BR-02.'
DK_DATA = DK + '\n3. Báo cáo đã tải xong theo bộ lọc đang chọn.'
NUM = ('- Số theo định dạng 1,234,567 (tối đa 2 chữ số lẻ); số âm có dấu "-".', '- Dòng TỔNG, dòng công ty, dòng xe: số 0 in "0" (chữ nhạt).')
POPUP = 'Cửa sổ %s được mở ngay trên màn báo cáo theo đường dẫn ở trên.'

# ---------------------------------------------------------------- nội dung ⓘ (nguyên văn configs/tripGross.js)
TIP = {
    'trang': 'Hiệu quả gộp của xe vận tải: Cước của chuyến so với chi phí lái xe (công lái xe, xăng xe, chi phí khác, vé cầu đường). Nguồn: phiếu hạch toán chuyến xe chở hàng / chuyến xe khác đã hạch toán. Kỳ lọc theo ngày hạch toán.',
    'ky': 'Lọc theo NGÀY HẠCH TOÁN của phiếu hạch toán chuyến xe.',
    'congty': 'Công ty của lái xe trên bút toán hạch toán chuyến xe.',
    'ten': 'CÔNG TY / BIỂN SỐ XE • Nhóm cấp 1 là công ty (công ty của lái xe trên bút toán hạch toán chuyến xe); dòng con là từng xe (biển số) • Mỗi dòng xe cộng mọi chuyến xe chở hàng và chuyến xe khác của xe trong kỳ • Bấm biển số để mở Báo cáo chi tiết hiệu quả gộp của xe đó ở tab mới • Dòng TỔNG tính trên toàn bộ dữ liệu đã lọc, không theo trang',
    'km_norm': 'KM ĐỊNH MỨC • Km của tuyến đường × 2 nếu chuyến 2 chiều • Chuyến xe khác không có tuyến: km nhập trên chuyến',
    'km_real': 'KM THỰC CHẠY • Km kết thúc − km bắt đầu nhập trên chuyến xe',
    'km_diff': 'CHÊNH LỆCH (KM) • KM thực chạy − KM định mức',
    'diff_pct': '% CHÊNH LỆCH • Chênh lệch ÷ KM định mức × 100 • Dòng xe / TỔNG tính trên tổng km, không cộng dồn %',
    'revenue': 'CƯỚC • Cước cần phân bổ ghi trên chuyến xe',
    'driver_cost': 'CHI PHÍ LÁI XE • Tổng bút toán Công lái xe + Xăng xe + Chi phí khác + Vé cầu đường của phiếu hạch toán • Gồm cả bút toán không gắn lái xe; không gồm Công tác phí',
    'gross': 'LÃI GỘP • Cước − Chi phí lái xe',
    'blk_trips': 'CHUYẾN XE • Mỗi chuyến là 1 phiếu hạch toán chuyến xe đã hạch toán, có ngày hạch toán trong kỳ • Chữ nhỏ bên cạnh là lãi gộp của nhóm chuyến; "Chuyến lỗ" = lãi gộp âm • Bấm vào con số để mở danh sách chuyến',
    'blk_money': 'HIỆU QUẢ GỘP • Lãi gộp = Cước − Chi phí lái xe • Tổng bút toán Công lái xe + Xăng xe + Chi phí khác + Vé cầu đường của phiếu hạch toán',
    'blk_km': 'QUÃNG ĐƯỜNG • Km của tuyến đường × 2 nếu chuyến 2 chiều • Km kết thúc − km bắt đầu nhập trên chuyến xe • Chênh lệch ÷ KM định mức × 100',
}

P5 = [
    ('Vận chuyển', 'Chuyến xe chở hàng (nút Hạch toán chuyến xe lập phiếu hạch toán — nguồn số của báo cáo)', 'Vận chuyển => Chuyến xe => Chuyến xe chở hàng'),
    ('Vận chuyển', 'Chuyến xe chở hàng chờ hạch toán', 'Vận chuyển => Chuyến xe => Chuyến xe chở hàng chờ hạch toán'),
    ('Vận chuyển', 'Chuyến xe khác (lập, kết thúc chuyến; nút Hạch toán chuyến xe)', 'Vận chuyển => Chuyến xe => Chuyến xe khác'),
    ('Vận chuyển', 'Chuyến xe khác chờ duyệt / chờ hạch toán', 'Vận chuyển => Chuyến xe => Chuyến xe khác chờ duyệt; Chuyến xe khác chờ hạch toán'),
    ('Vận chuyển', 'Báo cáo chi tiết hiệu quả gộp theo chuyến xe (cùng nguồn, cùng cách tính; mở từ biển số xe)', 'Vận chuyển => Báo cáo vận chuyển => Báo cáo chi tiết hiệu quả gộp theo chuyến xe'),
    ('Vận chuyển', 'Báo cáo tổng hợp chi phí vận chuyển theo lái xe (cùng nguồn phiếu hạch toán, cùng quyền)', 'Vận chuyển => Báo cáo vận chuyển => Báo cáo tổng hợp chi phí vận chuyển theo lái xe'),
    ('Vận chuyển', 'Báo cáo chi tiết chi phí vận chuyển theo lái xe (cùng nguồn, cùng quyền)', 'Vận chuyển => Báo cáo vận chuyển => Báo cáo chi tiết chi phí vận chuyển theo lái xe'),
    ('Vận chuyển', 'Báo cáo chi tiết chuyến xe (cùng nguồn chuyến xe, dùng chung quyền Xem báo cáo vận chuyển)', 'Vận chuyển => Báo cáo vận chuyển => Báo cáo chi tiết chuyến xe'),
    ('Danh mục tham chiếu', 'Biển số xe (nguồn ô lọc Biển số xe, tên dòng xe)', 'Danh mục dùng chung => Danh mục xe => Biển số xe'),
    ('Danh mục tham chiếu', 'Danh mục xe (xe chạy thực tế của chuyến — biển số dùng để gom dòng)', 'Danh mục dùng chung => Danh mục xe => Danh mục xe'),
]

FR = []

# ================================================================ 2.1 Xem báo cáo
COT = [
    ['Tiêu đề trang', 'Label', 'Hiển thị', TEN, ['- Ở thanh trên cùng, kèm icon ⓘ.', '- Icon ⓘ: "%s"' % TIP['trang']]],
    ['Dòng kỳ của khối tổng hợp', 'Label', 'Hiển thị', 'Kỳ tháng mm/yyyy (theo ngày hạch toán)', [
        '- "Kỳ <nhãn kỳ> (theo ngày hạch toán)" + icon ⓘ mục đích báo cáo + "· N chuyến · M xe · Lãi gộp X".',
        '- Nhãn kỳ: "tuần này", "tháng mm/yyyy", "năm yyyy", "từ dd/mm/yyyy đến dd/mm/yyyy".',
        '- Nút "Thu gọn" / "Mở rộng" ẩn / hiện các khối số bên dưới.']],
    ['Khối Chuyến xe', 'Label', 'Read-only', 'Theo dữ liệu', [
        '- Góc phải: "Lãi gộp <tổng lãi gộp>".',
        '- Ô "Tất cả chuyến": số chuyến + chữ "chuyến".',
        '- Ô "Chuyến xe chở hàng", "Chuyến xe khác": số chuyến + "Lãi gộp <lãi gộp của nhóm>"; ẩn khi bằng 0.',
        '- Ô "Chuyến lỗ" (nền cam): số chuyến có lãi gộp âm + "Lãi gộp <tổng âm>"; ẩn khi không có chuyến lỗ.',
        '- Con số gạch chân bấm được → mở popup danh sách chuyến (mục 2.3); số 0 không bấm được.',
        '- Icon ⓘ: "%s"' % TIP['blk_trips']]],
    ['Khối Hiệu quả gộp', 'Label', 'Read-only', 'Theo dữ liệu', [
        '- 3 ô: Cước, Chi phí lái xe, Lãi gộp (Lãi gộp âm tô cam). Không bấm được.', '- Icon ⓘ: "%s"' % TIP['blk_money']]],
    ['Khối Quãng đường', 'Label', 'Read-only', 'Theo dữ liệu', [
        '- Ô KM định mức, KM thực chạy (đơn vị km); ô Chênh lệch, % Chênh lệch chỉ hiện khi khác 0.', '- Icon ⓘ: "%s"' % TIP['blk_km']]],
    ['Bảng báo cáo', 'Table/Grid', 'Read-only', 'Theo dữ liệu', [
        '- 10 cột (mỗi cột mô tả ở 1 dòng bên dưới): STT, Công ty / Biển số xe, Số chuyến, KM định mức, KM thực chạy, Chênh lệch (KM), % Chênh lệch, Cước, Chi phí lái xe, Lãi gộp.',
        '- Thứ tự dòng: dòng TỔNG → dòng công ty (I, II, III…, nền xanh) → các dòng xe của công ty (1, 2…).',
        '- Tiêu đề bảng dính khi cuộn; bảng rộng hơn màn hình thì có thanh cuộn ngang.',
        '- Không có dữ liệu: "Không có chuyến xe nào khớp bộ lọc."',
        '- Đang tải lại: bảng mờ đi, giữ số liệu cũ đến khi có kết quả mới.']],
    ['Ô chọn cấp bung (trong tiêu đề cột Công ty / Biển số xe)', 'Dropdown', 'Enable', 'Đến xe', [
        '- Lựa chọn: "Chỉ công ty", "Đến xe".', '- Chỉ đổi cách xem, không tải lại dữ liệu.']],
    ['Dòng TỔNG', 'Table/Grid', 'Read-only', 'Theo dữ liệu', [
        '- Dòng đầu bảng, nền cam; cột tên ghi "CÔNG TY / BIỂN SỐ XE" kèm icon ⓘ.',
        '- Cộng TOÀN BỘ chuyến theo bộ lọc, không theo trang.', '- Icon ⓘ: "%s"' % TIP['ten']]],
    ['Cột STT', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Dòng công ty: số La Mã I, II, III… liên tục qua các trang.', '- Dòng xe: 1, 2… trong từng công ty.']],
    ['Cột Công ty / Biển số xe', 'Table/Grid', 'Read-only', 'Hiển thị', [
        '- Dòng công ty: tên công ty của lái xe, có mũi tên bung / thu các dòng xe; dài quá thì cắt "…".',
        '- Dòng xe: biển số xe dạng liên kết; bấm → mở "Báo cáo chi tiết hiệu quả gộp theo chuyến xe" ở tab mới, đã lọc sẵn biển số đó, cùng Kỳ và Công ty.',
        '- Chuyến không xác định được biển số: dòng "Chưa có biển số" (không có liên kết).']],
    ['Cột Số chuyến', 'Table/Grid', 'Read-only', 'Hiển thị', [
        '- Số chuyến (phiếu hạch toán) của dòng; gạch chân, bấm → popup danh sách chuyến của đúng dòng đó (mục 2.3).',
        '- Số 0 không bấm được.']],
    ['Cột KM định mức', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Tổng km định mức các chuyến.', *NUM, '- Icon ⓘ: "%s"' % TIP['km_norm']]],
    ['Cột KM thực chạy', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Tổng km thực chạy các chuyến (có thể rất lớn / âm khi km trên chuyến nhập sai).', *NUM, '- Icon ⓘ: "%s"' % TIP['km_real']]],
    ['Cột Chênh lệch (KM)', 'Table/Grid', 'Read-only', 'Hiển thị', ['- KM thực chạy − KM định mức.', *NUM, '- Icon ⓘ: "%s"' % TIP['km_diff']]],
    ['Cột % Chênh lệch', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Chênh lệch ÷ KM định mức × 100, kèm dấu %; KM định mức = 0 thì để trống.', '- Icon ⓘ: "%s"' % TIP['diff_pct']]],
    ['Cột Cước', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Tổng cước các chuyến.', *NUM, '- Icon ⓘ: "%s"' % TIP['revenue']]],
    ['Cột Chi phí lái xe', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Tổng chi phí lái xe các chuyến.', *NUM, '- Icon ⓘ: "%s"' % TIP['driver_cost']]],
    ['Cột Lãi gộp', 'Table/Grid', 'Read-only', 'Hiển thị', ['- Cước − Chi phí lái xe; âm khi lỗ.', *NUM, '- Icon ⓘ: "%s"' % TIP['gross']]],
    ['Chân bảng', 'Label', 'Hiển thị', 'Theo dữ liệu', ['- "Hiển thị a–b / N công ty": phân trang theo CÔNG TY (dòng xe luôn cùng trang với công ty của nó).']],
    ['Ô Số dòng/trang', 'Dropdown', 'Enable', '10', ['- Lựa chọn 10, 20, 50, 100 công ty / trang; đổi → về trang 1.']],
    ['Phân trang', 'Button', 'Enable', 'Trang 1', ['- «, ‹, số trang, ›, »; giữ bộ lọc và dòng TỔNG.']],
    ['Nút Cấu hình cột hiển thị', 'Button', 'Enable', 'Hiển thị', ['- Biểu tượng cột, đầu cụm nút; mở cửa sổ Tuỳ chỉnh cột (mục 2.6).']],
    ['Nút In báo cáo', 'Button', 'Enable', 'Hiển thị', ['- Mở cửa sổ "In báo cáo" (mục 2.4).', '- Báo cáo chưa tải xong: "Báo cáo chưa tải xong, vui lòng thử lại."']],
    ['Nút Xuất Excel', 'Button', 'Enable', 'Hiển thị', ['- Mở cửa sổ "Xuất Excel" (mục 2.5).', '- Báo cáo chưa tải xong: "Báo cáo chưa tải xong, vui lòng thử lại."']],
]

DATA_MAIN = [
    ('Tập dữ liệu / thời điểm số liệu', 'Mỗi "chuyến" = 1 phiếu hạch toán chuyến xe chở hàng hoặc chuyến xe khác ĐÃ HẠCH TOÁN, có ít nhất 1 bút toán chi phí lái xe (Công lái xe, Xăng xe, Chi phí khác, Vé cầu đường) GẮN LÁI XE thoả: ngày hạch toán trong kỳ, phạm vi quyền (BR-02), ô Công ty. Số liệu đọc tại thời điểm tải (không lưu sẵn).', TIP['trang']),
    ('Dòng công ty', 'Công ty của lái xe ghi trên bút toán hạch toán của chuyến. Không xác định được: "Chưa xác định công ty". Xếp theo tên công ty A → Z.', TIP['ten']),
    ('Dòng xe (biển số)', 'Biển số của xe chạy thực tế gắn trên chuyến xe; xe không có biển số thì lấy biển số ghi trên chuyến; vẫn không có thì "Chưa có biển số". 1 xe chạy cho 2 công ty ra 2 dòng ở 2 công ty. Trong công ty xếp theo biển số Z → A.', TIP['ten']),
    ('Số chuyến', 'Đếm số phiếu hạch toán của dòng.', '—'),
    ('KM định mức', 'Mỗi chuyến: km của tuyến đường × 2 nếu chuyến 2 chiều (× 1 nếu 1 chiều); chuyến xe khác không có tuyến thì lấy km nhập trên chuyến. Dòng = cộng các chuyến.', TIP['km_norm']),
    ('KM thực chạy', 'Mỗi chuyến: km kết thúc − km bắt đầu nhập trên chuyến xe. Dòng = cộng các chuyến.', TIP['km_real']),
    ('Chênh lệch (KM)', 'KM thực chạy − KM định mức (cộng các chuyến).', TIP['km_diff']),
    ('% Chênh lệch', 'Chênh lệch ÷ KM định mức × 100, làm tròn 2 chữ số lẻ, tính trên TỔNG km của dòng (không cộng dồn % các chuyến). KM định mức = 0 thì để trống.', TIP['diff_pct']),
    ('Cước', 'Cước cần phân bổ ghi trên chuyến xe của phiếu hạch toán. Dòng = cộng các chuyến.', TIP['revenue']),
    ('Chi phí lái xe', 'Tổng số tiền MỌI bút toán Công lái xe + Xăng xe + Chi phí khác + Vé cầu đường của phiếu hạch toán, KỂ CẢ bút toán không gắn lái xe; không gồm Công tác phí.', TIP['driver_cost']),
    ('Lãi gộp', 'Cước − Chi phí lái xe (từng chuyến rồi cộng).', TIP['gross']),
    ('Khối Chuyến xe', 'Tất cả chuyến = số phiếu hạch toán; Chuyến xe chở hàng / Chuyến xe khác = theo loại phiếu, kèm lãi gộp của nhóm; Chuyến lỗ = số chuyến có lãi gộp < 0, kèm tổng lãi gộp âm.', TIP['blk_trips']),
    ('Khối Hiệu quả gộp, Quãng đường', 'Bằng đúng các cột tương ứng ở dòng TỔNG.', TIP['blk_money']),
    ('Ràng buộc khớp số', '- Dòng TỔNG = cộng các dòng công ty (mọi trang); dòng công ty = cộng các dòng xe của nó (riêng % Chênh lệch tính lại trên tổng km).\n- Số chuyến dòng TỔNG = ô "Tất cả chuyến" = Chuyến xe chở hàng + Chuyến xe khác.\n- Lãi gộp = Cước − Chi phí lái xe ở mọi dòng.', '—'),
    ('Chân bảng "Hiển thị a–b / N công ty"', 'N = số công ty có chuyến theo bộ lọc.', '—'),
]

POPUP_MAIN = [
    ('Ô số ở khối Chuyến xe (Tất cả chuyến / Chuyến xe chở hàng / Chuyến xe khác / Chuyến lỗ)', 'Danh sách chuyến (mục 2.3)', 'Những chuyến nào tạo nên con số; chuyến nào lỗ', 'Chuyến theo bộ lọc màn chính, thu theo loại chuyến hoặc lãi gộp âm'),
    ('Số chuyến ở dòng TỔNG', 'Danh sách chuyến — "Tất cả chuyến xe"', 'Xem toàn bộ chuyến của báo cáo', 'Mọi chuyến theo bộ lọc'),
    ('Số chuyến ở dòng công ty', 'Danh sách chuyến — "<tên công ty>"', 'Chuyến của 1 công ty', 'Chuyến có lái xe thuộc công ty đó'),
    ('Số chuyến ở dòng xe', 'Danh sách chuyến — "<công ty> › <biển số>"', 'Chuyến của 1 xe trong 1 công ty', 'Chuyến của xe đó trong đúng công ty của dòng'),
    ('Biển số xe ở dòng xe', 'Không phải popup — mở Báo cáo chi tiết hiệu quả gộp theo chuyến xe ở tab mới', 'Xem chi tiết từng chuyến của xe', 'Báo cáo chi tiết lọc sẵn biển số, cùng Kỳ / Công ty'),
    ('Ô tiền, km (mọi cột số)', 'Không bấm được', '—', '—'),
]

FR.append({
    'ten': 'Xem báo cáo hiệu quả gộp xe vận tải',
    'qtc': 'Màn Báo cáo, Phân trang, Định dạng số.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem báo cáo hiệu quả gộp xe vận tải'],
        ['Mô tả', 'Hiển thị hiệu quả gộp của từng xe trong kỳ, nhóm theo công ty: số chuyến, km định mức / thực chạy / chênh lệch, cước, chi phí lái xe và lãi gộp; khối tổng hợp đầu trang. Màn chỉ đọc.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng mở màn theo đường dẫn menu.\n2. Hệ thống tải ngay báo cáo kỳ mặc định "Tháng này" theo phạm vi quyền: khối tổng hợp, dòng TỔNG, trang 1 gồm 10 công ty, mỗi công ty bung sẵn các dòng xe.\n3. Người dùng đọc số, đổi bộ lọc (mục 2.2), bấm số chuyến xem danh sách (mục 2.3) hoặc bấm biển số mở báo cáo chi tiết.'],
        ['Dòng sự kiện phụ', '• Không có chuyến: khối tổng hợp hiện số 0, bảng "Không có chuyến xe nào khớp bộ lọc."\n• Lỗi tải: báo lỗi, giữ số liệu đang hiện (không xoá trắng màn); thông báo mặc định "Không tải được báo cáo. Vui lòng thử lại."\n• Đổi bộ lọc liên tục: chỉ kết quả của lần lọc mới nhất được hiển thị.\n• Chuyển trang / đổi số dòng: dòng TỔNG và khối tổng hợp không đổi.\n• Phiên đăng nhập hết hạn: hệ thống báo và đưa về màn đăng nhập (quy tắc chung).'],
        ['Yêu cầu đặc biệt', 'Môi trường thử nghiệm 18/11/2026: kỳ 1 tháng (40 chuyến) tải dưới 0,5 giây; kỳ "Năm nay" (1.801 chuyến, 13 xe) khoảng 1,2–1,4 giây.'],
    ],
    'anh': [('01_open', 'Màn Báo cáo hiệu quả gộp xe vận tải lúc mới mở (kỳ Tháng này)'),
            ('03_report', 'Báo cáo kỳ Tháng trước (tháng 10/2026): khối tổng hợp và bảng Công ty / Biển số xe'),
            ('04_tip', 'Icon ⓘ ở tiêu đề cột giải thích cách tính (cột Lãi gộp)'),
            ('03d_level1', 'Ô chọn cấp bung "Chỉ công ty" — chỉ hiện dòng TỔNG và dòng công ty')],
    'ui': ui(UI6, COT),
    'ui_widths': UI6W,
    'events': [
        ['Mở màn hình', 'System', 'Before:\n– Không kiểm quyền vào màn; đọc phạm vi của người dùng (BR-02) để mở / khoá ô Công ty.\nAfter:\n– Tải báo cáo kỳ "Tháng này", 10 công ty / trang, bung đến xe.'],
        ['Đổi ô lọc / bấm Tìm kiếm', 'Change / Click', 'Xem mục 2.2.'],
        ['Chọn cấp bung / bấm mũi tên ở dòng công ty', 'Change / Click', 'After:\n– Ẩn / hiện các dòng xe; không tải lại dữ liệu.'],
        ['Chuyển trang / đổi Số dòng/trang', 'Click / Change', 'After:\n– Tải trang công ty mới, giữ bộ lọc, dòng TỔNG, khối tổng hợp; đổi số dòng thì về trang 1.'],
        ['Bấm con số gạch chân (khối Chuyến xe / cột Số chuyến)', 'Click', 'After:\n– Mở popup danh sách chuyến của đúng ô số (mục 2.3).'],
        ['Bấm biển số xe', 'Click', 'After:\n– Mở Báo cáo chi tiết hiệu quả gộp theo chuyến xe ở tab mới, lọc sẵn biển số, cùng Kỳ và Công ty đang xem.'],
        ['Bấm Thu gọn / Mở rộng', 'Click', 'After:\n– Ẩn / hiện các khối số của khối tổng hợp.'],
        ['Rê chuột vào icon ⓘ', 'Hover', 'After:\n– Hiện chú thích cách tính (nội dung ở bảng 2.1.5).'],
    ],
    'them': [
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', [
            ('p', 'Bảng dưới mô tả cách hệ thống tính từng chỉ tiêu, từng cột số liệu và nội dung icon ⓘ (nguyên văn trên giao diện).'),
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
        ['Mô tả', 'Chọn kỳ báo cáo (kỳ có sẵn hoặc khoảng ngày tuỳ chọn), thu hẹp theo Công ty và Biển số xe.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn Báo cáo hiệu quả gộp xe vận tải.'],
        ['Dòng sự kiện chính', '1. Người dùng chọn Kỳ, Công ty, Biển số xe.\n2. Hệ thống tải lại báo cáo ngay khi đổi một ô (không cần bấm Tìm kiếm), về trang 1.\n3. Chọn Kỳ "Tuỳ chọn": hiện thêm ô Thời gian (Từ ngày → Đến ngày); chọn đủ 2 ngày thì báo cáo tự tải.'],
        ['Dòng sự kiện phụ', '• Kỳ "Tuỳ chọn" chưa đủ 2 ngày mà bấm Tìm kiếm → "Chọn đủ ngày bắt đầu và ngày kết thúc của kỳ Tuỳ chọn.", không tải.\n• Đến ngày nhỏ hơn Từ ngày → "Ngày kết thúc phải sau hoặc bằng ngày bắt đầu".\n• Đổi Kỳ khỏi "Tuỳ chọn" → ô Thời gian biến mất, khoảng ngày bị xoá.\n• Bấm Xóa lọc → mọi ô về mặc định (Kỳ "Tháng này"; người không có quyền tổng công ty giữ công ty bị khoá), về cấp bung "Đến xe", tải lại.'],
    ],
    'anh': [('07_filter_plate', 'Lọc Biển số xe 37C-31738 — kỳ Tháng trước còn 8 chuyến, 1 xe'),
            ('08_custom', 'Kỳ Tuỳ chọn: hiện ô Thời gian; bấm Tìm kiếm khi chưa chọn ngày')],
    'ui': ui(UI7, [
        ['Tiêu đề khu vực lọc', 'Label', 'Hiển thị', '–', '–', ['- "Bộ lọc báo cáo hiệu quả gộp xe vận tải" + icon ⓘ "MỤC ĐÍCH BÁO CÁO" (nội dung như tiêu đề trang).']],
        ['Ô Kỳ', 'Dropdown', 'Enable', 'Tuần này, Tháng này, Tháng trước, Năm nay, Tuỳ chọn', 'Tháng này', ['- Không xoá trống được.', '- Icon ⓘ: "%s"' % TIP['ky'], '- Tuần tính từ thứ Hai đến Chủ nhật; Năm nay = 01/01 → 31/12 năm hiện tại.']],
        ['Ô Thời gian', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy', 'Trống', ['- Chỉ hiện khi Kỳ = Tuỳ chọn, ngay sau ô Kỳ; 1 ô gồm Từ ngày → Đến ngày, tính cả 2 đầu.', '- Phải chọn đủ 2 ngày; Đến ngày ≥ Từ ngày.']],
        ['Ô Công ty', 'Dropdown', 'Enable / Disable', 'Công ty đang hoạt động', 'Trống (tất cả)', ['- Quyền mức Tổng công ty: chọn được mọi công ty, để trống = tất cả.', '- Mức khác: ô khoá ở công ty của người xem, không xoá được.', '- Lọc theo công ty của lái xe trên bút toán; icon ⓘ: "%s"' % TIP['congty']]],
        ['Ô Biển số xe', 'Dropdown', 'Enable', 'Danh mục biển số đang hoạt động', 'Trống', ['- Gõ để tìm; nút × xoá.', '- Giữ chuyến có biển số ghi trên chuyến xe bằng biển số đã chọn.']],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', ['- Tải lại báo cáo theo các ô đang chọn, về trang 1.']],
        ['Nút Xóa lọc', 'Button', 'Enable', '–', '–', ['- Mọi ô về mặc định và tải lại.']],
        ['Nút Cài đặt bộ lọc / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', ['- Chỉ hiện khi các ô lọc không vừa 1 hàng (vd khi có thêm ô Thời gian); chọn ô hiển thị, thu gọn / mở khu vực lọc (quy tắc chung).']],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Đổi Kỳ / Công ty / Biển số xe', 'Change', 'After:\n– Tải lại báo cáo từ trang 1 (Kỳ Tuỳ chọn chưa đủ 2 ngày thì chưa tải).'],
        ['Bấm Tìm kiếm', 'Click', 'Before:\n– Kỳ Tuỳ chọn chưa đủ ngày → "Chọn đủ ngày bắt đầu và ngày kết thúc của kỳ Tuỳ chọn.", dừng.\nAfter:\n– Tải lại báo cáo từ trang 1.'],
        ['Bấm Xóa lọc', 'Click', 'After:\n– Mọi ô về mặc định, tải lại báo cáo.'],
    ],
})

# ================================================================ 2.3 Popup danh sách chuyến
POP_COLS = [
    ['Tiêu đề popup', 'Label', 'Hiển thị', 'Theo ô số đã bấm', ['- "Tất cả chuyến xe" / "Chuyến xe chở hàng" / "Chuyến xe khác" / "Chuyến lỗ (lãi gộp âm)" / "<công ty>" / "<công ty> › <biển số>".', '- Dòng phụ: "N chuyến · Cước: X · Lãi gộp: Y · Kỳ <nhãn kỳ>".', '- Nút phóng to và × góc phải.']],
    ['Ô tìm', 'Textbox', 'Enable', 'Trống', ['- Placeholder "Tìm biển số / phiếu / chuyến / tuyến / lái xe…"; lọc ngay khi gõ, không phân biệt hoa thường / có dấu; nút × xoá.']],
    ['Ô Chọn biển số xe', 'Dropdown', 'Enable / Ẩn', 'Trống', ['- Các biển số có trong danh sách; ẩn khi popup mở từ 1 dòng xe.']],
    ['Ô Chọn loại chuyến', 'Dropdown', 'Enable / Ẩn', 'Trống', ['- Chuyến xe chở hàng / Chuyến xe khác; ẩn khi popup mở từ ô theo loại chuyến.']],
    ['Nút Xoá lọc (biểu tượng làm mới)', 'Button', 'Ẩn', 'Ẩn', ['- Hiện khi có ô lọc của popup đang chọn; bấm → bỏ lọc trong popup.']],
    ['Bộ đếm', 'Label', 'Hiển thị', '"n / N chuyến"', ['- n = số dòng sau lọc trong popup, N = tổng dòng của ô số.']],
    ['Bảng', 'Table/Grid', 'Read-only', 'Theo dữ liệu', ['- 12 cột: STT, Biển số xe, Thời gian, Phiếu hạch toán, Chuyến xe, Tuyến đường, Lái xe, KM định mức, KM thực chạy, Cước, Chi phí lái xe, Lãi gộp.', '- Bấm tiêu đề cột (có mũi tên) để sắp xếp tăng / giảm; số so số, ngày so ngày.', '- Số 0 để trống; không có dòng: "Không có chuyến xe nào khớp bộ lọc."']],
    ['Cột Thời gian', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', ['- Ngày cập nhật phiếu hạch toán (kỳ vẫn lọc theo ngày hạch toán).']],
    ['Cột Phiếu hạch toán / Chuyến xe', 'Table/Grid', 'Read-only', 'Liên kết', ['- Bấm → mở chi tiết phiếu hạch toán / chuyến xe ở tab mới.']],
    ['Cột Lái xe', 'Table/Grid', 'Read-only', 'Hiển thị', ['- "Tên - Mã nhân viên" của lái xe trên các bút toán, nhiều người cách nhau dấu phẩy.']],
    ['Phân trang', 'Button', 'Enable', '10 dòng/trang', ['- Lựa chọn 10, 20, 50, 100; "Hiển thị a–b / n chuyến".']],
    ['Nút In danh sách', 'Button', 'Enable', '–', ['- Mở cửa sổ "In danh sách" chọn cột (các cột đang hiện), bấm In → xem trước bản in "DANH SÁCH CHUYẾN XE — HIỆU QUẢ GỘP" theo ô số + ô tìm.']],
    ['Nút Xuất Excel danh sách', 'Button', 'Enable', '–', ['- Mở cửa sổ chọn cột, bấm Xuất Excel → tải file danh_sach_chuyen_xe_hieu_qua_gop_yyyymmdd.xlsx.']],
    ['Nút Đóng', 'Button', 'Enable', '–', ['- Đóng popup; mở lại thì sạch lọc / sắp xếp.']],
]
FR.append({
    'ten': 'Xem danh sách chuyến xe', 'uc': 'uc_danhsach',
    'qtc': 'Popup, Định dạng số.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem danh sách chuyến xe tạo nên con số'],
        ['Mô tả', 'Popup liệt kê từng chuyến (phiếu hạch toán) của ô số đã bấm, lọc / sắp xếp / in / xuất Excel tại chỗ.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_DATA + '\n4. Ô số bấm vào lớn hơn 0.'],
        ['Dòng sự kiện chính', '1. Người dùng bấm con số gạch chân (khối Chuyến xe hoặc cột Số chuyến).\n2. Hệ thống mở popup, tải đủ mọi chuyến của ô số theo bộ lọc màn chính.\n3. Người dùng tìm, lọc, sắp xếp, chuyển trang; bấm In danh sách / Xuất Excel danh sách / Đóng.'],
        ['Dòng sự kiện phụ', '• Đang tải: dòng phụ "Đang tải…".\n• Lỗi tải: báo lỗi, popup giữ nguyên.\n• Chọn cột in / xuất bỏ hết: "Vui lòng chọn ít nhất 1 cột để in" / "… để xuất".'],
    ],
    'menu_them': ' => Bấm số chuyến {icon:lnk_sochuyen}',
    'ghi_chu_layout': POPUP % 'danh sách chuyến',
    'anh': [('05_drill', 'Popup "Tất cả chuyến xe" (bấm số 40 ở dòng TỔNG)'),
            ('05b_drill_loss', 'Popup "Chuyến lỗ (lãi gộp âm)" mở từ khối Chuyến xe'),
            ('05e_drill_print', 'Xem trước bản in danh sách chuyến của 1 xe')],
    'ui': ui(UI6, POP_COLS),
    'ui_widths': UI6W,
    'events': [
        ['Bấm con số', 'Click', 'After:\n– Mở popup, tải đủ chuyến của ô số (bộ lọc màn chính + phạm vi ô số).'],
        ['Gõ ô tìm / chọn ô lọc', 'Keypress / Change', 'After:\n– Lọc ngay trong popup, về trang 1; bộ đếm cập nhật.'],
        ['Bấm tiêu đề cột', 'Click', 'After:\n– Sắp xếp tăng → giảm theo cột.'],
        ['Bấm In danh sách', 'Click', 'After:\n– Mở cửa sổ chọn cột; bấm In → cửa sổ xem trước bản in.'],
        ['Bấm Xuất Excel danh sách', 'Click', 'After:\n– Mở cửa sổ chọn cột; bấm Xuất Excel → tải file.'],
        ['Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup.'],
    ],
    'them': [
        ('Mục đích thiết kế popup', [
            ('bullet', 'Trả lời câu hỏi "con số này gồm những chuyến nào, chuyến nào lỗ, do lái xe nào chạy".'),
            ('bullet', 'Là popup để giữ nguyên báo cáo, bộ lọc và trang đang xem.'),
            ('bullet', 'Ràng buộc khớp số: số dòng popup = con số đã bấm; tổng Cước / Lãi gộp ở dòng phụ = số ở dòng tương ứng của báo cáo.'),
        ]),
        ('Các biến thể theo con số bấm', [('variant', [
            ('Tất cả chuyến / số chuyến dòng TỔNG', 'Mọi chuyến theo bộ lọc', 'Tất cả chuyến xe', 'Hiện cả 2 ô lọc'),
            ('Chuyến xe chở hàng / Chuyến xe khác', 'Chuyến của loại đó', 'Chuyến xe chở hàng / Chuyến xe khác', 'Ẩn ô Chọn loại chuyến'),
            ('Chuyến lỗ', 'Chuyến có lãi gộp âm', 'Chuyến lỗ (lãi gộp âm)', 'Hiện cả 2 ô lọc'),
            ('Số chuyến dòng công ty', 'Chuyến của công ty', '<tên công ty>', 'Hiện cả 2 ô lọc'),
            ('Số chuyến dòng xe', 'Chuyến của xe trong đúng công ty', '<công ty> › <biển số>', 'Ẩn ô Chọn biển số xe'),
        ])]),
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', [
            ('p', 'Mỗi dòng là 1 chuyến; các cột số tính như mục 2.1.5 cho 1 chuyến. Xếp mặc định theo biển số Z → A, cùng xe thì ngày hạch toán mới → cũ.'),
        ]),
    ],
})

# ================================================================ 2.4 In
FR.append({
    'ten': 'In báo cáo', 'uc': 'uc_in',
    'qtc': 'In.',
    'gioi_thieu': [
        ['Tên chức năng', 'In báo cáo hiệu quả gộp xe vận tải'],
        ['Mô tả', 'Chọn bản in (bảng tổng hợp hoặc danh sách chuyến xe) và cột in, xem trước rồi in; luôn lấy MỌI trang theo bộ lọc đang hiển thị.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_DATA],
        ['Dòng sự kiện chính', '1. Người dùng bấm In báo cáo.\n2. Hệ thống mở cửa sổ "In báo cáo": 2 bản "In bảng tổng hợp" (mặc định) / "Danh sách chuyến xe", khu vực "Chọn cột in" tích sẵn mọi cột.\n3. Người dùng chọn bản, tích / bỏ cột, bấm In.\n4. Hệ thống mở cửa sổ xem trước: tiêu đề công ty, tên báo cáo, dòng kỳ, bảng theo cột đã chọn, "Ngày dd Tháng mm Năm yyyy", "Người lập (Ký, họ tên)".\n5. Người dùng bấm In trong cửa sổ xem trước để in ra máy in.'],
        ['Dòng sự kiện phụ', '• Bỏ hết cột: "Vui lòng chọn ít nhất 1 cột để in", không mở xem trước.\n• Vượt 2.000 dòng: cửa sổ xem trước chỉ báo số dòng vượt mức in tối đa 2,000 dòng và gợi ý thu hẹp bộ lọc / dùng Xuất Excel, ẩn nút In.\n• Bấm Hủy / × → đóng, không in.'],
    ],
    'menu_them': ' => In báo cáo {icon:btn_in}',
    'ghi_chu_layout': POPUP % 'In báo cáo',
    'anh': [('09_print_opt', 'Cửa sổ In báo cáo — chọn bản in và cột in'),
            ('10_print', 'Xem trước bản in bảng tổng hợp')],
    'ui': ui(UI6, [
        ['Lựa chọn In bảng tổng hợp', 'Radio', 'Enable', 'Được chọn', ['- "Đúng bảng đang xem, đủ mọi trang, kèm dòng TỔNG."', '- Cột chọn được: Số chuyến, KM định mức, KM thực chạy, Chênh lệch (KM), % Chênh lệch, Cước, Chi phí lái xe, Lãi gộp; STT và Công ty / Biển số xe luôn in.', '- Bản in: TỔNG → công ty (I, II…) → xe (1, 2…).']],
        ['Lựa chọn Danh sách chuyến xe', 'Radio', 'Enable', 'Không', ['- "Mỗi dòng 1 chuyến (phiếu hạch toán), đúng bộ lọc báo cáo hiện tại."', '- 17 cột chọn được: Biển số xe, Thời gian, Phiếu hạch toán, Loại chuyến, Chuyến xe, Tuyến đường, Lái xe, Tải trọng tính cước, Dòng xe tính cước, Xe chạy thực tế, KM định mức, KM thực chạy, Chênh lệch (KM), % Chênh lệch, Cước, Chi phí lái xe, Lãi gộp.', '- Bản in "DANH SÁCH CHUYẾN XE — HIỆU QUẢ GỘP" kèm dòng đếm "N chuyến · Cước · Chi phí lái xe · Lãi gộp … VND".']],
        ['Chọn cột in / Chọn tất cả', 'Checkbox', 'Enable', 'Tích tất cả', ['- Icon ⓘ: "Cột STT luôn được in."']],
        ['Nút In', 'Button', 'Enable', '–', ['- Mở cửa sổ xem trước theo bản + cột đã chọn.']],
        ['Nút Hủy / ×', 'Button', 'Enable', '–', ['- Đóng cửa sổ.']],
        ['Cửa sổ xem trước', 'Label', 'Read-only', 'Theo dữ liệu', ['- Tiêu đề "Xem trước báo cáo hiệu quả gộp xe vận tải" (bản danh sách: "Xem trước danh sách chuyến xe"), nút In, nút ×.', '- Khổ ngang, tiêu đề công ty của người in; dòng kỳ + điều kiện lọc.', '- Số 0 ở bản in tổng hợp in "0".']],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm In báo cáo', 'Click', 'Before:\n– Báo cáo chưa tải xong → "Báo cáo chưa tải xong, vui lòng thử lại.", dừng.\nAfter:\n– Mở cửa sổ chọn bản + cột.'],
        ['Bấm In (cửa sổ chọn)', 'Click', 'Before:\n– Không có cột nào → "Vui lòng chọn ít nhất 1 cột để in".\nAfter:\n– Lấy mọi dòng theo bộ lọc đang hiển thị, dựng bản in, mở xem trước.'],
        ['Bấm In (xem trước)', 'Click', 'After:\n– Gửi ra máy in.'],
    ],
})

# ================================================================ 2.5 Xuất Excel
FR.append({
    'ten': 'Xuất Excel', 'uc': 'uc_xuat',
    'qtc': 'Xuất Excel.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất báo cáo ra Excel'],
        ['Mô tả', 'Chọn bản xuất (bảng tổng hợp / danh sách chuyến xe) và cột như In, tải file Excel gồm mọi trang theo bộ lọc đang hiển thị.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK_DATA],
        ['Dòng sự kiện chính', '1. Người dùng bấm Xuất Excel.\n2. Hệ thống mở cửa sổ "Xuất Excel": "Xuất bảng tổng hợp" / "Danh sách chuyến xe", "Chọn cột xuất".\n3. Người dùng chọn rồi bấm Xuất Excel.\n4. Trình duyệt tải file: bảng tổng hợp "bao_cao_hieu_qua_gop_xe_van_tai.xlsx"; danh sách "danh_sach_chuyen_xe_hieu_qua_gop_yyyymmdd.xlsx".'],
        ['Dòng sự kiện phụ', '• Bỏ hết cột: "Vui lòng chọn ít nhất 1 cột để xuất".\n• Lỗi: "Lỗi khi xuất Excel".'],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': POPUP % 'Xuất Excel',
    'anh': [('11_export_opt', 'Cửa sổ Xuất Excel — chọn bản xuất và cột')],
    'ui': ui(UI6, [
        ['Lựa chọn Xuất bảng tổng hợp / Danh sách chuyến xe', 'Radio', 'Enable', 'Xuất bảng tổng hợp', ['- Cùng bộ cột như In (mục 2.4); icon ⓘ "Cột STT luôn được xuất."']],
        ['Nút Xuất Excel', 'Button', 'Enable', '–', ['- Tải file theo bản + cột đã chọn.']],
        ['Nút Hủy / ×', 'Button', 'Enable', '–', ['- Đóng, không xuất.']],
        ['File Excel', 'File', '–', '–', ['- Logo + tiêu đề công ty, tên báo cáo in hoa, dòng điều kiện lọc; bảng có dòng TỔNG; khối "Người lập".', '- Ô số là kiểu số, định dạng 1,234,567.']],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Xuất Excel (màn chính)', 'Click', 'Before:\n– Báo cáo chưa tải xong → "Báo cáo chưa tải xong, vui lòng thử lại.".\nAfter:\n– Mở cửa sổ chọn bản + cột.'],
        ['Bấm Xuất Excel (cửa sổ)', 'Click', 'After:\n– Tải file theo đúng bộ lọc đang hiển thị, mọi trang.'],
    ],
})

# ================================================================ 2.6 Tuỳ chỉnh cột
FR.append({
    'ten': 'Tùy chỉnh cột hiển thị',
    'qtc': 'Tùy chỉnh cột.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tùy chỉnh cột hiển thị'],
        ['Mô tả', 'Ẩn / hiện và đổi thứ tự các cột của bảng báo cáo; cấu hình lưu theo người dùng và theo màn. Không ảnh hưởng In / Xuất Excel.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', '1. Người dùng bấm Cấu hình cột hiển thị.\n2. Hệ thống mở cửa sổ "Tuỳ chỉnh cột".\n3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự, bấm Lưu.\n4. Hệ thống áp lên bảng, lưu cấu hình, báo "Cập nhật thành công".'],
        ['Dòng sự kiện phụ', '• STT và Công ty / Biển số xe là cột khoá, luôn hiện.\n• Bấm Đóng → bỏ thay đổi. Lỗi lưu: "Thao tác thất bại".'],
    ],
    'menu_them': ' => Cấu hình cột hiển thị {icon:btn_cauhinhcot}',
    'ghi_chu_layout': POPUP % 'Tuỳ chỉnh cột',
    'anh': [('12_colcfg', 'Cửa sổ Tuỳ chỉnh cột')],
    'ui': ui(UI6, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', ['- "Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng."']],
        ['Danh sách cột', 'Checkbox', 'Enable', 'Theo cấu hình đã lưu', ['- STT, Công ty / Biển số xe (khoá), Số chuyến, KM định mức, KM thực chạy, Chênh lệch (KM), % Chênh lệch, Cước, Chi phí lái xe, Lãi gộp.', '- Mặc định hiện tất cả.']],
        ['Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', ['- Tích / bỏ tích mọi cột (trừ cột khoá).']],
        ['Dòng đếm', 'Label', 'Hiển thị', 'Đang chọn 10/10 cột', ['- Cập nhật theo số cột đang tích.']],
        ['Nút Lưu', 'Button', 'Enable', '–', ['- Áp dụng và lưu; "Cập nhật thành công".']],
        ['Nút Đóng / ×', 'Button', 'Enable', '–', ['- Đóng, không áp dụng.']],
    ]),
    'ui_widths': UI6W,
    'events': [
        ['Bấm Cấu hình cột hiển thị', 'Click', 'After:\n– Mở cửa sổ theo cấu hình đang dùng.'],
        ['Bấm Lưu', 'Click', 'After:\n– Ẩn / hiện, sắp lại cột trên bảng; lưu theo người dùng.'],
        ['Bấm Đóng', 'Click', 'After:\n– Đóng, không áp dụng.'],
    ],
})

# ---------------------------------------------------------------- Phần 2 + 4
PERMS = [
    ('Xem báo cáo vận chuyển — mức Tổng công ty', 'Thấy chuyến của mọi công ty; ô Công ty mở, để trống = tất cả công ty.'),
    ('Xem báo cáo vận chuyển — mức Công ty', 'Thấy chuyến có bút toán lái xe thuộc công ty của người xem; ô Công ty khoá ở công ty đó.'),
    ('(Không có quyền)', 'Vẫn mở được màn; chỉ thấy chuyến có bút toán lái xe do chính mình lập; ô Công ty khoá ở công ty của mình.'),
]
FUNCS = ['FR-01 Xem báo cáo hiệu quả gộp xe vận tải', 'FR-02 Tìm kiếm và lọc', 'FR-03 Xem danh sách chuyến xe',
         'FR-04 In báo cáo', 'FR-05 Xuất Excel', 'FR-06 Tùy chỉnh cột hiển thị']

S = {
    'ten': TEN,
    'menu': [('Vận chuyển', 'menu_phanhe'), ('Báo cáo vận chuyển', 'menu_nhom'), (TEN, 'menu_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu màn báo cáo.',
        'Phạm vi chức năng: Xem báo cáo, Tìm kiếm và lọc, Xem danh sách chuyến xe (popup), In báo cáo, Xuất Excel, Tùy chỉnh cột hiển thị. Màn chỉ đọc — không thêm / sửa / xoá dữ liệu.',
        'Mục đích sử dụng dữ liệu: đánh giá xe nào chạy có lãi / lỗ, chênh lệch km thực chạy so với định mức để kiểm soát chi phí lái xe.',
        'Làm rõ cách chọn chuyến, cách tính km, cước, chi phí lái xe, lãi gộp ở dòng xe / công ty / TỔNG và khối tổng hợp, phạm vi dữ liệu theo quyền, các popup và bản in / Excel.',
    ],
    'thuat_ngu': [
        ['Chuyến', 'Một phiếu hạch toán chuyến xe (chuyến xe chở hàng hoặc chuyến xe khác) đã hạch toán.'],
        ['Phiếu hạch toán chuyến xe', 'Chứng từ ghi các bút toán chi phí của một chuyến xe sau khi chuyến kết thúc.'],
        ['Bút toán chi phí lái xe', 'Bút toán Công lái xe, Xăng xe, Chi phí khác, Vé cầu đường của phiếu hạch toán.'],
        ['Ngày hạch toán', 'Ngày ghi sổ bút toán; dùng để xếp kỳ.'],
        ['Cước', 'Cước cần phân bổ ghi trên chuyến xe.'],
        ['Lãi gộp', 'Cước − Chi phí lái xe.'],
        ['KM định mức', 'Km chuẩn của tuyến đường (× 2 nếu 2 chiều).'],
        ['KM thực chạy', 'Km kết thúc − km bắt đầu nhập trên chuyến.'],
        ['Chuyến lỗ', 'Chuyến có lãi gộp âm.'],
        ['Phạm vi dữ liệu', 'Phần số liệu người dùng được xem theo mức quyền (tổng công ty / công ty / của mình).'],
    ],
    'quyen_truoc': [
        'Màn KHÔNG chặn quyền vào: mọi người dùng đăng nhập đều thấy mục menu và mở được màn, dùng được mọi chức năng. Quyền "Xem báo cáo vận chuyển" (phân hệ Kho, nhóm Vận chuyển - Bốc xếp; mức Công ty / Tổng công ty) chỉ mở rộng PHẠM VI DỮ LIỆU. Có cả 2 mức thì tính mức cao hơn.',
    ],
    'quyen_rows': [list(p) for p in PERMS],
    'ma_tran': [['Chức năng', 'Tổng công ty', 'Công ty', 'Không quyền']] + [[f, 'Có', 'Có', 'Có'] for f in FUNCS],
    'ma_tran_widths': [3.0, 1.0, 1.0, 1.0],
    'quyen_sau': [
        'Mọi chức năng dùng được với mọi mức; khác nhau ở phạm vi số liệu (BR-02). Phạm vi áp cho mọi con số: khối tổng hợp, bảng, popup, bản in, file Excel.',
        'Phạm vi xét ở bước CHỌN CHUYẾN (bút toán gắn lái xe); khi đã chọn, chi phí của chuyến cộng đủ mọi bút toán chi phí lái xe của phiếu (BR-05).',
        'Mở chi tiết phiếu hạch toán / chuyến xe từ popup: màn đích tự áp quyền xem của chính nó.',
    ],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Kỳ báo cáo', ['– Mặc định "Tháng này"; Tuần này (thứ Hai → Chủ nhật), Tháng trước, Năm nay, Tuỳ chọn (Từ ngày → Đến ngày, tính cả 2 đầu, phải đủ 2 ngày, Đến ngày ≥ Từ ngày).', '– Xếp kỳ theo NGÀY HẠCH TOÁN của bút toán chi phí lái xe.'], ['Xem báo cáo', 'Tìm kiếm và lọc']),
        ('BR-02', 'Phạm vi dữ liệu', ['– Mức Tổng công ty: mọi công ty; ô Công ty lọc thêm theo công ty của lái xe.', '– Mức Công ty: chuyến có bút toán gắn lái xe thuộc công ty của người xem.', '– Không quyền: chuyến có bút toán gắn lái xe do chính người xem lập.', '– Ô Công ty chỉ mở với mức Tổng công ty.'], ['Mọi chức năng hiện số liệu']),
        ('BR-03', 'Chuyến lên báo cáo', ['– Phiếu hạch toán chuyến xe chở hàng / chuyến xe khác ở trạng thái Đã hạch toán.', '– Có ≥ 1 bút toán Công lái xe / Xăng xe / Chi phí khác / Vé cầu đường GẮN LÁI XE thoả kỳ, phạm vi, ô Công ty.', '– Ô Biển số xe: biển số ghi trên chuyến xe.'], ['Xem báo cáo']),
        ('BR-04', 'Nhóm Công ty ▸ Biển số xe', ['– Công ty = công ty của lái xe trên bút toán; xếp tên A → Z.', '– Biển số = biển số xe chạy thực tế (thiếu thì biển số ghi trên chuyến); trong công ty xếp Z → A.', '– 1 xe chạy cho 2 công ty ra 2 dòng.', '– Phân trang theo công ty, mặc định 10.'], ['Xem báo cáo', 'In', 'Xuất Excel']),
        ('BR-05', 'Cước, chi phí, lãi gộp', ['– Cước = cước cần phân bổ của chuyến xe.', '– Chi phí lái xe = MỌI bút toán Công lái xe + Xăng xe + Chi phí khác + Vé cầu đường của phiếu, kể cả bút toán không gắn lái xe; không gồm Công tác phí.', '– Lãi gộp = Cước − Chi phí lái xe; Chuyến lỗ = lãi gộp < 0.'], ['Xem báo cáo', 'In', 'Xuất Excel']),
        ('BR-06', 'Km và % chênh lệch', ['– KM định mức = km tuyến × 2 nếu 2 chiều; chuyến xe khác không tuyến: km nhập trên chuyến.', '– KM thực chạy = km kết thúc − km bắt đầu; Chênh lệch = thực chạy − định mức.', '– % = Chênh lệch ÷ KM định mức × 100 tính trên tổng km của dòng; định mức = 0 thì để trống.'], ['Xem báo cáo', 'In', 'Xuất Excel']),
        ('BR-07', 'Dòng TỔNG và khối tổng hợp', ['– Tính trên toàn bộ dữ liệu đã lọc, không theo trang, không đổi khi chuyển trang / đổi cấp bung.'], ['Xem báo cáo']),
        ('BR-08', 'Định dạng số', ['– Dạng 1,234,567, tối đa 2 chữ số lẻ, số âm có dấu "-".', '– Bảng chính: số 0 in "0" (chữ nhạt); popup: số 0 để trống.'], ['Xem báo cáo', 'Xem danh sách chuyến xe']),
        ('BR-09', 'In / Xuất Excel', ['– Lấy MỌI dòng theo bộ lọc ĐANG HIỂN THỊ; cột theo lựa chọn; STT (và cột tên ở bản tổng hợp) luôn có.', '– In tối đa 2.000 dòng; vượt thì không in, gợi ý Xuất Excel.'], ['In', 'Xuất Excel', 'Xem danh sách chuyến xe']),
        ('BR-10', 'Cấu hình cột', ['– Lưu theo người dùng + màn; cột STT, Công ty / Biển số xe luôn hiện; không ảnh hưởng In / Excel.'], ['Tùy chỉnh cột hiển thị']),
    ],
    'phan5': {
        'cau_dan': 'Báo cáo chỉ đọc. Các màn hình dưới đây ghi ra số liệu mà báo cáo cộng lại (phiếu hạch toán chuyến xe), dùng chung nguồn / quyền với báo cáo, hoặc cung cấp danh mục cho ô lọc.',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng đã đăng nhập',
    'mains': [('FR-01', 'Xem báo cáo hiệu quả gộp xe vận tải', 'view'), ('FR-04', 'In báo cáo', 'io'), ('FR-05', 'Xuất Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc', 'view'), ('FR-03', 'Xem danh sách chuyến xe', 'view'), ('FR-06', 'Tùy chỉnh cột hiển thị', 'view')],
    'rieng': [('FR-03', 'Xem danh sách chuyến xe', 'view', 'uc_danhsach'), ('FR-04', 'In báo cáo', 'io', 'uc_in'), ('FR-05', 'Xuất Excel', 'io', 'uc_xuat')],
}

if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', D.build_srs_report(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)

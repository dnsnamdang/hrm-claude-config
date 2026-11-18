# -*- coding: utf-8 -*-
"""Testcase "Báo cáo hiệu quả gộp xe vận tải" — KHUÔN CHUẨN skill testcase-documenter (tc_chuan.build_chuan, loai='bao_cao').
Mẫu đã duyệt: sale-customer-debt-reports/docs/compare/gen_testcase.py. Case chung (phân trang, kỳ, popup, cột, quyền) ở _tc_trp.py.
Không có TC cũ cho màn này (van-chuyen-bao-cao/testcase/ là BC chi tiết hiệu quả gộp theo chuyến — chỉ tham khảo).
Chạy: python gen_testcase.py  (tự gọi check_tc — phải 0 lỗi)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _tc_trp import _sach, C, sections, dem, build_chuan, pt_chung, ky_chung, popup_chung, cot_chung, pq_chung  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

NGAY = '18/11/2026'
TEN = 'Báo cáo hiệu quả gộp xe vận tải'
MODULE = 'BC hiệu quả gộp xe vận tải'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
MENU = 'Vào phân hệ Vận chuyển > Báo cáo vận chuyển > bấm "Báo cáo hiệu quả gộp xe vận tải"'
LOC = 'Chọn Kỳ = Tháng trước (tháng 10/2026)'
T10 = 'Tài khoản TK-SA (quyền Xem báo cáo vận chuyển mức Tổng công ty); kỳ tháng 10/2026 trên môi trường thử có 40 chuyến, 6 xe, 3 công ty.'
Q = '"Xem báo cáo vận chuyển"'


def L_(*lines):
    return '\n'.join(lines)


M = {
    'ten': TEN, 'menu': MENU, 'url': '/transport/trip-gross-reports/by-vehicle', 'loc': LOC,
    'dv': 'công ty', 'loc_nhieu': 'Chọn Kỳ = Năm nay, ô Số dòng/trang = 10',
    'nhieu_trang': 'Tài khoản TK-SA; kỳ có hơn 20 công ty có chuyến (môi trường thử hiện chỉ 3–6 công ty có chuyến: chỉ kiểm được 1 trang, ghi lại vào cột Ghi chú).',
    'doi_loc': 'Chọn 1 biển số ở ô Biển số xe',
    'thu_tu': 'công ty theo tên A → Z, xe trong công ty theo biển số Z → A',
    'tong_ghi_chu': 'N chỉ đếm số công ty có chuyến theo bộ lọc',
    'theo': 'theo ngày hạch toán', 'ngay_loc': 'ngày hạch toán',
    'bien_ngay': 'Có chuyến TPV_HTCXCH_03199 (xe 37C-31738) hạch toán ngày 19/10/2026.',
    'loc_nhieu_o': 'Kỳ Năm nay, Công ty, Biển số xe 37C-31738',
    'man_khac': 'Vận chuyển > Báo cáo vận chuyển > Báo cáo chi tiết chuyến xe',
    'popup_mo': LOC + ', bấm số 40 ở cột Số chuyến dòng TỔNG', 'popup_dv': 'chuyến',
    'pre_popup': T10, 'pre_0': 'Kỳ có nhóm chuyến (vd Chuyến xe khác) bằng 0 hoặc dòng có số chuyến 0.',
    'popup_kw': 'vinh', 'popup_fields': 'biển số, phiếu hạch toán, chuyến xe, tuyến đường, xe chạy thực tế, lái xe',
    'popup_empty': 'Không có chuyến xe nào khớp bộ lọc.', 'popup_filter': 'Chọn biển số xe', 'popup_sort': 'Lãi gộp',
    'list_title': 'DANH SÁCH CHUYẾN XE — HIỆU QUẢ GỘP', 'list_file': 'danh_sach_chuyen_xe_hieu_qua_gop_yyyymmdd.xlsx',
    'popup_xl_buoc': ', tích các cột, bấm Xuất Excel',
    'popup_xl_noi_dung': 'File gồm đúng các dòng của ô số (+ từ khoá), đúng các cột đã chọn, có dòng "N chuyến · Cước · Chi phí lái xe · Lãi gộp … VND"',
    'cot_ds': 'STT, Công ty / Biển số xe, Số chuyến, KM định mức, KM thực chạy, Chênh lệch (KM), % Chênh lệch, Cước, Chi phí lái xe, Lãi gộp',
    'cot_n': '10', 'cot_khoa': 'Công ty / Biển số xe', 'cot_an': 'KM thực chạy', 'cot_keo': 'Lãi gộp',
    'quyen_ten': 'quyền ' + Q, 'quyen_cao': 'quyền ' + Q + ' mức Tổng công ty',
    'pre_url_cty': 'Tài khoản TK-CT (mức Công ty, công ty A); biết mã công ty B.',
}

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Báo cáo chỉ đọc: hiệu quả gộp của từng xe vận tải trong kỳ = Cước của chuyến so với chi phí lái xe (công lái xe, xăng xe, chi phí khác, vé cầu đường).',
        'Chức năng: Xem báo cáo, Tìm kiếm / lọc, Xem danh sách chuyến xe (popup), Tùy chỉnh cột, Xuất Excel, In.',
        'Đường vào: ' + MENU + '.')),
    ('2. Đối tượng được tính / hiển thị', L_(
        '1 "chuyến" = 1 phiếu hạch toán chuyến xe chở hàng hoặc chuyến xe khác ở trạng thái Đã hạch toán, có ít nhất 1 bút toán Công lái xe / Xăng xe / Chi phí khác / Vé cầu đường GẮN LÁI XE, ngày hạch toán trong kỳ.',
        'Bảng: dòng TỔNG -> dòng công ty (I, II…; công ty của lái xe trên bút toán) -> dòng xe (1, 2…; biển số xe chạy thực tế).',
        '10 cột: STT | Công ty / Biển số xe | Số chuyến | KM định mức | KM thực chạy | Chênh lệch (KM) | % Chênh lệch | Cước | Chi phí lái xe | Lãi gộp.',
        'Khối tổng hợp: Chuyến xe (Tất cả chuyến, Chuyến xe chở hàng, Chuyến xe khác, Chuyến lỗ), Hiệu quả gộp (Cước, Chi phí lái xe, Lãi gộp), Quãng đường.')),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '-  Phiếu hạch toán chưa hạch toán (đang lập / chờ duyệt / đã huỷ).',
        '-  Phiếu chỉ có bút toán không gắn lái xe (không có bút toán nào gắn lái xe).',
        '-  Bút toán Công tác phí (không cộng vào Chi phí lái xe).',
        '-  Bút toán có ngày hạch toán ngoài kỳ.',
        '-  Chuyến ngoài phạm vi quyền của người xem.')),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô Kỳ lọc theo NGÀY HẠCH TOÁN của bút toán chi phí lái xe: Tuần này / Tháng này (mặc định) / Tháng trước / Năm nay / Tuỳ chọn (Từ ngày → Đến ngày, tính cả 2 đầu).',
        'Cột "Thời gian" trong popup là ngày cập nhật phiếu hạch toán — có thể khác ngày dùng để lọc kỳ.')),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Cấp 0: dòng TỔNG. Cấp 1: công ty (phân trang theo công ty, mặc định 10, tên A → Z). Cấp 2: xe (biển số Z → A).',
        'Ô chọn cấp bung: "Chỉ công ty" / "Đến xe" (mặc định). Bảng chính không sắp xếp theo cột.')),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '-  Dòng xe = cộng các chuyến của xe trong công ty; 1 xe chạy cho 2 công ty ra 2 dòng ở 2 công ty.',
        '-  Chi phí lái xe của chuyến cộng MỌI bút toán chi phí lái xe của phiếu, kể cả bút toán không gắn lái xe.',
        '-  % Chênh lệch dòng xe / công ty / TỔNG tính lại trên tổng km, KHÔNG cộng dồn %.')),
    ('7. Phân quyền cấp', L_(
        'Màn không chặn quyền vào; mọi người đăng nhập đều mở được và dùng mọi nút. Quyền "Xem báo cáo vận chuyển" — mức: Công ty / Tổng công ty — chỉ mở rộng phạm vi:',
        '-  Mức Tổng công ty: mọi công ty; ô Công ty mở.',
        '-  Mức Công ty: chuyến có bút toán lái xe thuộc công ty của người xem; ô Công ty khoá.',
        '-  Không quyền: chuyến có bút toán lái xe do chính người xem lập; ô Công ty khoá.')),
    ('8. Cách tính các ô thống kê', L_(
        'Cước = cước cần phân bổ của chuyến xe. Chi phí lái xe = tổng bút toán Công lái xe + Xăng xe + Chi phí khác + Vé cầu đường của phiếu. Lãi gộp = Cước − Chi phí lái xe.',
        'KM định mức = km tuyến × 2 nếu 2 chiều (chuyến xe khác không tuyến: km nhập trên chuyến). KM thực chạy = km kết thúc − km bắt đầu. Chênh lệch = thực chạy − định mức. % = Chênh lệch ÷ KM định mức × 100.',
        'Chuyến lỗ = số chuyến có lãi gộp < 0. Chân bảng "Hiển thị a–b / N công ty".')),
    ('9. Ghi chú đọc bảng', L_(
        '-  Số dạng 1,234,567 (tối đa 2 số lẻ); bảng chính số 0 in "0" chữ nhạt; popup số 0 để trống.',
        '-  KM thực chạy có thể rất lớn / âm do km trên chuyến nhập sai — không phải lỗi báo cáo.',
        'Dữ liệu mẫu (môi trường thử 18/11/2026): tháng 10/2026 = 40 chuyến, 6 xe, 3 công ty, Cước 24,720,667, Chi phí lái xe 18,129,331, Lãi gộp 6,591,336, 14 chuyến lỗ; xe 37C-31738 = 8 chuyến; năm 2026 = 1.801 chuyến, 13 xe.',
        'TK-SA (mức Tổng công ty), TK-CT (mức Công ty, công ty A), NV-A (không quyền, lập bút toán của 1 số chuyến).')),
]

# ================================================================== I. HIỂN THỊ TRANG & TRUY CẬP
G1 = [
    C('Mở màn hình từ menu', 'P0', 'Tài khoản bất kỳ đã đăng nhập.', ['1. Đăng nhập', '2. ' + MENU], '',
      ['Tiêu đề trang "Báo cáo hiệu quả gộp xe vận tải" có icon (i); rê chuột hiện mục đích báo cáo',
       'Nhóm Báo cáo vận chuyển có đủ 6 mục, trong đó có "Báo cáo hiệu quả gộp xe vận tải"',
       'Báo cáo tự tải theo Kỳ "Tháng này"']),
    C('Bố cục khu vực lọc và các nút', 'P1', 'Đang mở màn.', ['1. Quan sát khu vực lọc'], '',
      ['Tiêu đề "Bộ lọc báo cáo hiệu quả gộp xe vận tải" + icon (i)', 'Ô Kỳ, Công ty, Biển số xe; nút Tìm kiếm, Xóa lọc',
       'Cụm nút góc phải theo thứ tự: Cấu hình cột hiển thị (biểu tượng cột), In báo cáo, Xuất Excel', 'Màn không có nút Thêm / Sửa / Xóa']),
    C('Khối tổng hợp đầu trang', 'P0', T10, ['1. ' + LOC, '2. Quan sát khối tổng hợp'], '',
      ['Dòng "Kỳ tháng 10/2026 (theo ngày hạch toán) · 40 chuyến · 6 xe · Lãi gộp 6,591,336"',
       'Khối CHUYẾN XE: Tất cả chuyến 40, Chuyến xe chở hàng 37 (Lãi gộp 4,195,131), Chuyến xe khác 3 (Lãi gộp 2,396,205), Chuyến lỗ 14 (Lãi gộp -2,564,542, nền cam)',
       'Khối HIỆU QUẢ GỘP: Cước 24,720,667, Chi phí lái xe 18,129,331, Lãi gộp 6,591,336',
       'Khối QUÃNG ĐƯỜNG: KM định mức 2,769 km, KM thực chạy 358,225 km, Chênh lệch 355,456 km, % Chênh lệch 12,836.98%']),
    C('Ô trong khối tổng hợp bằng 0 thì ẩn', 'P2', 'Kỳ Tháng này trên môi trường thử chỉ có 1 chuyến xe chở hàng, lãi gộp dương, km chênh lệch 0.',
      ['1. Mở màn (Kỳ Tháng này)'], '',
      ['Không hiện ô Chuyến xe khác, Chuyến lỗ', 'Khối Quãng đường chỉ có KM định mức, KM thực chạy (ẩn Chênh lệch, % Chênh lệch)']),
    C('Thu gọn / mở rộng khối tổng hợp', 'P2', 'Đang xem báo cáo.', ['1. Bấm "Thu gọn"', '2. Bấm "Mở rộng"'], '',
      ['Bước 1: chỉ còn dòng kỳ, các khối số ẩn', 'Bước 2: hiện lại đủ khối']),
    C('Kiểm tra đủ các cột của bảng', 'P0', 'Đang mở màn.', ['1. Đọc tiêu đề bảng từ trái sang phải'], '',
      ['STT | Công ty / Biển số xe (kèm ô chọn cấp bung) | Số chuyến | KM định mức | KM thực chạy | Chênh lệch (KM) | % Chênh lệch | Cước | Chi phí lái xe | Lãi gộp',
       'Các cột số có icon (i) (trừ Số chuyến); tiêu đề cột số canh phải']),
    C('Nội dung icon (i) của tiêu đề cột', 'P2', 'Đang mở màn.', ['1. Rê chuột vào icon (i) của cột Chi phí lái xe, % Chênh lệch'], '',
      ['Chi phí lái xe: "CHI PHÍ LÁI XE • Tổng bút toán Công lái xe + Xăng xe + Chi phí khác + Vé cầu đường của phiếu hạch toán • Gồm cả bút toán không gắn lái xe; không gồm Công tác phí"',
       '% Chênh lệch: "Chênh lệch ÷ KM định mức × 100 • Dòng xe / TỔNG tính trên tổng km, không cộng dồn %"']),
    C('Bảng có số liệu: phân biệt 3 loại dòng', 'P0', T10, ['1. ' + LOC], '',
      ['Dòng đầu "TỔNG" nền cam, cột tên ghi "CÔNG TY / BIỂN SỐ XE" có icon (i)',
       'Dòng công ty STT I, II, III nền xanh, có mũi tên thu / bung', 'Dòng xe STT 1, 2 trong từng công ty, biển số dạng liên kết']),
    C('Ô chọn cấp bung', 'P0', T10, ['1. ' + LOC, '2. Chọn "Chỉ công ty"', '3. Bấm mũi tên ở dòng công ty II', '4. Chọn "Đến xe"'], '',
      ['Bước 2: chỉ còn dòng TỔNG và 3 dòng công ty', 'Bước 3: chỉ công ty II bung ra 2 xe', 'Bước 4: mọi công ty bung đến xe', 'Không tải lại dữ liệu, số liệu không đổi']),
    C('Bấm biển số mở báo cáo chi tiết của xe', 'P0', T10, ['1. ' + LOC, '2. Bấm biển số 37C-31738'], '',
      ['Mở tab mới "Báo cáo chi tiết hiệu quả gộp theo chuyến xe", Kỳ Tháng trước, ô Biển số xe = 37C-31738',
       'Báo cáo chi tiết có 8 chuyến, Lãi gộp 1,966,619 = dòng xe 37C-31738 trên báo cáo này', 'Tab báo cáo gốc giữ nguyên']),
    C('Không có dữ liệu', 'P1', 'Kỳ Tuỳ chọn không có chuyến nào (vd 01/01/2020 - 02/01/2020).', ['1. Chọn Kỳ Tuỳ chọn với khoảng ngày trên'], '',
      ['Bảng hiện "Không có chuyến xe nào khớp bộ lọc."', 'Dòng TỔNG và khối tổng hợp hiện 0', 'Số 0 không bấm được']),
    C('Dòng "Chưa có biển số" / "Chưa xác định công ty"', 'P2', 'Có chuyến không xác định được biển số hoặc công ty lái xe.', ['1. Chọn kỳ có chuyến đó'], '',
      ['Chuyến vào dòng xe "Chưa có biển số" (không có liên kết) / nhóm "Chưa xác định công ty"', 'Không mất chuyến khỏi dòng TỔNG']),
    C('Thời gian tải báo cáo', 'P1', 'Tài khoản TK-SA; năm 2026 có 1.801 chuyến.', ['1. Chọn Kỳ = Năm nay', '2. Bấm giờ đến khi bảng hiện số'], '',
      ['Báo cáo hiện dưới 3 giây (môi trường thử đo 1,2–1,4 giây)', 'Trong lúc tải bảng mờ đi, không trắng màn']),
    C('Lỗi tải báo cáo giữ số liệu cũ', 'P2', 'Đang xem báo cáo có số; mạng chập chờn.', ['1. Ngắt mạng', '2. Đổi Kỳ'], '',
      ['Báo lỗi (vd "Không tải được báo cáo. Vui lòng thử lại.")', 'Bảng giữ số liệu cũ, không trắng màn; có mạng lại bấm Tìm kiếm thì tải bình thường']),
] + pt_chung(dict(M, loc=LOC))

# ================================================================== II. TÌM KIẾM & LỌC
G2 = ky_chung(M) + [
    C('Lọc theo Công ty', 'P0', T10, ['1. ' + LOC, '2. Chọn Công ty "CN HẢI PHÒNG - CÔNG TY CP CÔNG NGHỆ THIẾT BỊ TÂN PHÁT"'], '',
      ['Báo cáo tự tải lại, chỉ còn công ty đó với 2 xe 29D-54533, 15D-00500', 'Dòng kỳ: "18 chuyến · 2 xe · Lãi gộp 144,818"', 'Danh sách ô Công ty gồm các công ty đang hoạt động']),
    C('Lọc theo Biển số xe', 'P0', T10, ['1. ' + LOC, '2. Chọn Biển số xe 37C-31738'], '',
      ['Chỉ còn 1 công ty, 1 xe 37C-31738', 'Dòng kỳ: "8 chuyến · 1 xe · Lãi gộp 1,966,619"', 'Ô Biển số xe gõ được để tìm, có nút × xoá']),
    C('Lọc kết hợp Kỳ + Công ty + Biển số', 'P0', 'Tài khoản TK-SA.', ['1. Kỳ Năm nay', '2. Chọn công ty CN Vinh', '3. Chọn biển số 37C-28351'], '',
      ['Chỉ còn chuyến của xe 37C-28351 có lái xe thuộc công ty đã chọn trong năm', 'Bỏ ô Biển số (×) thì hiện lại mọi xe của công ty']),
    C('Lọc không có kết quả', 'P1', 'Tài khoản TK-SA.', ['1. ' + LOC, '2. Chọn 1 biển số không chạy chuyến nào trong tháng 10/2026'], '',
      ['"Không có chuyến xe nào khớp bộ lọc."', 'Khối tổng hợp toàn 0, chân bảng / phân trang không có dữ liệu']),
    C('Bấm Tìm kiếm tải lại theo bộ lọc hiện tại', 'P2', 'Đang xem báo cáo.', ['1. Ở trang 2, bấm Tìm kiếm'], '',
      ['Báo cáo tải lại từ trang 1, cùng bộ lọc; số liệu mới nhất (nếu vừa có phiếu được hạch toán thêm)']),
]

# ================================================================== III. SỐ LIỆU BÁO CÁO
PRE_CH = 'Phiếu hạch toán mẫu HT-1 (chuyến xe chở hàng, đã hạch toán 15/10/2026, xe 29D-53315): tuyến 30 km 2 chiều, km bắt đầu 1,000, km kết thúc 1,064; cước cần phân bổ 480,000; bút toán Công lái xe 50,000 (gắn lái xe), Xăng xe 27,278 (KHÔNG gắn lái xe), Công tác phí 20,000.'
G3 = [
    C('Cột Số chuyến đếm phiếu hạch toán', 'P0', T10, ['1. ' + LOC, '2. Bấm số chuyến của xe 37C-31738, đếm dòng popup'], '',
      ['Xe 37C-31738: 8 chuyến = 8 dòng popup, mỗi dòng 1 phiếu hạch toán khác nhau']),
    C('KM định mức tính theo tuyến × 2 chiều', 'P0', PRE_CH, ['1. Lọc kỳ chứa HT-1, biển số 29D-53315', '2. Bấm số chuyến, đọc dòng HT-1'], '',
      ['KM định mức của HT-1 = 30 × 2 = 60', 'Chuyến 1 chiều thì KM định mức = km tuyến']),
    C('KM định mức chuyến xe khác không có tuyến', 'P1', 'Chuyến xe khác HT-2 không chọn tuyến, km nhập trên chuyến 45, 1 chiều.', ['1. Lọc kỳ chứa HT-2, mở popup'], '',
      ['KM định mức của HT-2 = 45']),
    C('KM thực chạy và Chênh lệch', 'P0', PRE_CH, ['1. Mở popup có HT-1'], '',
      ['KM thực chạy = 1,064 − 1,000 = 64', 'Chênh lệch (KM) ở dòng xe = KM thực chạy − KM định mức (HT-1 góp 64 − 60 = 4)']),
    C('% Chênh lệch tính trên tổng km, không cộng dồn', 'P0', T10, ['1. ' + LOC, '2. Đọc công ty II (CN Vinh) và 2 xe của nó'], '',
      ['Xe 37C-31738: 0%; xe 37C-28351: 394 ÷ 1,322 × 100 = 29.8%', 'Công ty II: 394 ÷ 1,738 × 100 = 22.67% (KHÔNG phải 0% + 29.8%)',
       'Dòng TỔNG: 355,456 ÷ 2,769 × 100 = 12,836.98%']),
    C('% Chênh lệch để trống khi KM định mức bằng 0', 'P2', 'Có xe trong kỳ có tổng KM định mức = 0.', ['1. Chọn kỳ có xe đó'], '',
      ['Ô % Chênh lệch của xe để trống (không in 0%, không báo lỗi chia 0)']),
    C('Cột Cước lấy cước cần phân bổ của chuyến', 'P0', PRE_CH, ['1. Mở popup có HT-1'], '', ['Cước của HT-1 = 480,000 (đúng cước cần phân bổ ghi trên chuyến xe)']),
    C('Chi phí lái xe gồm cả bút toán không gắn lái xe, không gồm Công tác phí', 'P0', PRE_CH, ['1. Mở popup có HT-1'], '',
      ['Chi phí lái xe của HT-1 = 50,000 + 27,278 = 77,278', 'KHÔNG cộng Công tác phí 20,000', 'Lãi gộp HT-1 = 480,000 − 77,278 = 402,722']),
    C('Phiếu chỉ có bút toán không gắn lái xe thì không lên báo cáo', 'P1', 'Phiếu HT-3 đã hạch toán trong kỳ, mọi bút toán chi phí đều KHÔNG gắn lái xe.', ['1. Chọn kỳ chứa HT-3, mở popup Tất cả chuyến, tìm HT-3'], '',
      ['HT-3 không có trong popup, không được đếm ở Số chuyến']),
    C('Lãi gộp = Cước − Chi phí lái xe ở mọi dòng', 'P0', T10, ['1. ' + LOC, '2. Đối chiếu từng dòng'], '',
      ['Dòng TỔNG: 24,720,667 − 18,129,331 = 6,591,336', 'Xe 15D-00500: 2,282,600 − 3,498,641 = -1,216,041 (số âm có dấu "-")']),
    C('Dòng công ty bằng tổng các dòng xe', 'P0', T10, ['1. ' + LOC, '2. Cộng các xe của công ty I'], '',
      ['Số chuyến 12 + 6 = 18; Cước 7,607,395 + 2,282,600 = 9,889,995; Lãi gộp 1,360,859 + (-1,216,041) = 144,818']),
    C('Dòng TỔNG bằng tổng các công ty, không theo trang', 'P0', 'Tài khoản TK-SA; Kỳ Năm nay; đặt Số dòng/trang 10.', ['1. Ghi dòng TỔNG', '2. Cộng các dòng công ty ở mọi trang', '3. Sang trang 2'], '',
      ['Dòng TỔNG = tổng mọi công ty ở mọi trang', 'Chuyển trang không làm đổi dòng TỔNG và khối tổng hợp']),
    C('Khối tổng hợp khớp dòng TỔNG', 'P0', T10, ['1. ' + LOC, '2. So khối tổng hợp với dòng TỔNG'], '',
      ['Tất cả chuyến = Số chuyến dòng TỔNG = Chuyến xe chở hàng + Chuyến xe khác (40 = 37 + 3)', 'Cước / Chi phí lái xe / Lãi gộp / km ở khối = dòng TỔNG']),
    C('Chuyến lỗ đếm chuyến có lãi gộp âm', 'P0', T10, ['1. ' + LOC, '2. Bấm số 14 ở ô Chuyến lỗ'], '',
      ['Popup "Chuyến lỗ (lãi gộp âm)" có 14 dòng, mọi dòng có Lãi gộp < 0', 'Tổng lãi gộp ở dòng phụ popup = -2,564,542']),
    C('Phiếu hạch toán chưa hạch toán không lên báo cáo', 'P0', 'Phiếu HT-4 trong kỳ đang ở trạng thái chưa hạch toán (đang lập / chờ duyệt).', ['1. Chọn kỳ chứa HT-4, tìm HT-4 trong popup Tất cả chuyến'], '',
      ['HT-4 không có trên báo cáo']),
    C('Kỳ theo ngày hạch toán, không theo ngày tạo / ngày cập nhật', 'P1', 'Phiếu HT-5: tạo 30/09/2026, ngày hạch toán 02/10/2026.', ['1. Kỳ Tuỳ chọn 01/09/2026 - 30/09/2026', '2. Kỳ Tuỳ chọn 01/10/2026 - 31/10/2026'], '',
      ['HT-5 KHÔNG có ở kỳ tháng 9, CÓ ở kỳ tháng 10', 'Cột Thời gian trong popup là ngày cập nhật phiếu, có thể khác ngày hạch toán']),
    C('Một xe chạy cho 2 công ty ra 2 dòng', 'P1', 'Xe X có chuyến do lái xe công ty A và chuyến do lái xe công ty B trong kỳ.', ['1. Chọn kỳ đó'], '',
      ['Xe X xuất hiện dưới cả công ty A và công ty B, mỗi dòng chỉ cộng chuyến của công ty đó', 'Khối tổng hợp đếm "xe" theo số dòng xe']),
    C('Thứ tự công ty và xe', 'P2', T10, ['1. ' + LOC], '',
      ['Công ty xếp theo tên A → Z (CN HẢI PHÒNG…, CÔNG TY CỔ PHẦN … - CHI NHÁNH VINH, CÔNG TY CỔ PHẦN … TÂN PHÁT)', 'Trong công ty xe xếp theo biển số Z → A (29D-54533 trước 15D-00500)']),
    C('Định dạng số trên bảng', 'P1', T10, ['1. ' + LOC], '',
      ['Số có dấu phẩy ngăn hàng nghìn (24,720,667), tối đa 2 số lẻ (12,836.98%)', 'Số 0 ở dòng TỔNG / công ty / xe in "0" chữ nhạt; % bằng 0 in "0%"', 'Số âm có dấu "-" phía trước']),
    C('KM nhập sai làm KM thực chạy rất lớn', 'P2', T10, ['1. ' + LOC, '2. Đọc xe 29D-54533'], '',
      ['KM thực chạy 355,720, % Chênh lệch 51,829.93% — hiển thị đúng như dữ liệu km trên chuyến, không báo lỗi', 'Ghi chú cho QA: do km bắt đầu / kết thúc nhập sai, không phải lỗi báo cáo']),
]

# ================================================================== IV. XEM CHI TIẾT DANH SÁCH CHUYẾN XE
G4 = [
    C('Mở popup từ dòng TỔNG', 'P0', T10, ['1. ' + LOC, '2. Bấm số 40 ở cột Số chuyến dòng TỔNG'], '',
      ['Popup "Tất cả chuyến xe", dòng phụ "40 chuyến · Cước: 24,720,667 · Lãi gộp: 6,591,336 · Kỳ tháng 10/2026"',
       'Cột: STT, Biển số xe, Thời gian, Phiếu hạch toán, Chuyến xe, Tuyến đường, Lái xe, KM định mức, KM thực chạy, Cước, Chi phí lái xe, Lãi gộp',
       'Có ô tìm, ô "Chọn biển số xe", "Chọn loại chuyến", bộ đếm "40 / 40 chuyến"; nút In danh sách, Xuất Excel danh sách, Đóng']),
    C('Mở popup từ dòng xe', 'P0', T10, ['1. ' + LOC, '2. Bấm số 8 ở dòng xe 37C-31738'], '',
      ['Tiêu đề "CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT- CHI NHÁNH VINH › 37C-31738"', '8 dòng đều của xe 37C-31738', 'Ẩn ô "Chọn biển số xe"']),
    C('Mở popup từ dòng công ty', 'P0', T10, ['1. ' + LOC, '2. Bấm số 18 ở công ty I'], '', ['Tiêu đề là tên công ty, 18 dòng của 2 xe 29D-54533, 15D-00500']),
    C('Mở popup từ ô loại chuyến của khối tổng hợp', 'P0', T10, ['1. ' + LOC, '2. Bấm số 3 ở ô Chuyến xe khác'], '',
      ['Tiêu đề "Chuyến xe khác", 3 dòng', 'Ẩn ô "Chọn loại chuyến"']),
    C('Bấm phiếu hạch toán / chuyến xe trong popup', 'P1', T10, ['1. Mở popup', '2. Bấm mã phiếu hạch toán TPV_HTCXCH_03199', '3. Bấm tên chuyến xe'], '',
      ['Mỗi lần mở chi tiết phiếu hạch toán / chuyến xe tương ứng ở tab mới', 'Popup giữ nguyên']),
    C('Cột Lái xe ghi tên và mã', 'P2', T10, ['1. Mở popup', '2. Đọc cột Lái xe'], '', ['Mỗi lái xe ghi dạng tên + mã nhân viên, vd "Nguyễn Văn Tế - 41410781"', 'Chuyến nhiều lái xe ghi nhiều người cách nhau dấu phẩy']),
] + popup_chung(M)

# ================================================================== V. TÙY CHỈNH CỘT
G5 = cot_chung(M)

# ================================================================== VI. XUẤT DANH SÁCH EXCEL
G6 = [
    C('Mở cửa sổ Xuất Excel', 'P0', T10, ['1. ' + LOC, '2. Bấm Xuất Excel'], '',
      ['Cửa sổ "Xuất Excel" có 2 lựa chọn: "Xuất bảng tổng hợp" (mặc định, "Đúng bảng đang xem, đủ mọi trang, kèm dòng TỔNG.") và "Danh sách chuyến xe"',
       '"Chọn cột xuất" tích sẵn 8 cột: Số chuyến, KM định mức, KM thực chạy, Chênh lệch (KM), % Chênh lệch, Cước, Chi phí lái xe, Lãi gộp', 'Nút Xuất Excel, Hủy']),
    C('Xuất bảng tổng hợp đủ cột', 'P0', T10, ['1. ' + LOC, '2. Xuất Excel > Xuất bảng tổng hợp > Xuất Excel', '3. Mở file'], '',
      ['Tải file "bao_cao_hieu_qua_gop_xe_van_tai.xlsx", mở được bằng Excel',
       'Có logo + tiêu đề công ty, "BÁO CÁO HIỆU QUẢ GỘP XE VẬN TẢI", dòng điều kiện lọc có kỳ', 'Dòng TỔNG rồi công ty, xe — số liệu khớp màn hình']),
    C('Xuất một số cột', 'P0', T10, ['1. Bỏ tích KM thực chạy, Chênh lệch (KM)', '2. Xuất Excel, mở file'], '', ['File chỉ có STT, Công ty / Biển số xe và 6 cột còn lại, đúng thứ tự']),
    C('Không chọn cột nào', 'P1', 'Đang mở cửa sổ Xuất Excel.', ['1. Bỏ tích "Chọn tất cả"', '2. Bấm Xuất Excel'], '',
      ['Báo "Vui lòng chọn ít nhất 1 cột để xuất"', 'Không tải file']),
    C('Xuất danh sách chuyến xe', 'P0', T10, ['1. Xuất Excel > chọn "Danh sách chuyến xe"', '2. Bấm Xuất Excel'], '',
      ['Danh sách cột đổi thành 17 cột: Biển số xe, Thời gian, Phiếu hạch toán, Loại chuyến, Chuyến xe, Tuyến đường, Lái xe, Tải trọng tính cước, Dòng xe tính cước, Xe chạy thực tế, KM định mức, KM thực chạy, Chênh lệch (KM), % Chênh lệch, Cước, Chi phí lái xe, Lãi gộp',
       'File "danh_sach_chuyen_xe_hieu_qua_gop_yyyymmdd.xlsx" có đủ 40 dòng (1 dòng / chuyến)']),
    C('Xuất lấy mọi trang, đúng bộ lọc đang hiển thị', 'P0', 'Kỳ Năm nay, Số dòng/trang 10, đang ở trang 1.', ['1. Xuất bảng tổng hợp', '2. Đếm dòng công ty / xe'], '',
      ['File có đủ mọi công ty, mọi xe (không chỉ trang đang xem)', 'Đổi ô lọc nhưng báo cáo chưa tải xong thì file theo bộ lọc của báo cáo ĐANG hiển thị']),
    C('Xuất khi lọc biển số', 'P1', 'Lọc Biển số xe 37C-31738.', ['1. Xuất bảng tổng hợp'], '', ['File chỉ có 1 công ty, 1 xe; dòng điều kiện ghi "Biển số xe: 37C-31738"']),
    C('Xuất khi không có dữ liệu', 'P2', 'Bảng "Không có chuyến xe nào khớp bộ lọc."', ['1. Xuất bảng tổng hợp', '2. Mở file'], '', ['Vẫn tải file, có tiêu đề + dòng TỔNG = 0, không lỗi']),
    C('Định dạng số và tiếng Việt trong file', 'P1', T10, ['1. Xuất bảng tổng hợp', '2. Bấm 1 ô số, cộng cột bằng thanh trạng thái'], '',
      ['Ô số là kiểu SỐ, hiển thị 1,234,567; số âm có dấu "-"', 'Tên công ty tiếng Việt có dấu hiển thị đúng', 'Tiêu đề cột đúng nhãn trên màn']),
    C('Bấm Hủy thì không xuất', 'P2', 'Đang mở cửa sổ Xuất Excel.', ['1. Bấm Hủy (hoặc ×)'], '', ['Cửa sổ đóng, không tải file, báo cáo giữ nguyên']),
]

# ================================================================== VII. IN BÁO CÁO
G7 = [
    C('Mở cửa sổ In báo cáo', 'P0', T10, ['1. ' + LOC, '2. Bấm In báo cáo'], '',
      ['Cửa sổ "In báo cáo": "In bảng tổng hợp" (mặc định) / "Danh sách chuyến xe", "Chọn cột in" tích sẵn, icon (i) "Cột STT luôn được in."', 'Nút In, Hủy']),
    C('In bảng tổng hợp', 'P0', T10, ['1. In báo cáo > In bảng tổng hợp > In'], '',
      ['Cửa sổ "Xem trước báo cáo hiệu quả gộp xe vận tải", khổ ngang, tiêu đề công ty của người in',
       'Tên "BÁO CÁO HIỆU QUẢ GỘP XE VẬN TẢI", dòng "Kỳ tháng 10/2026 (theo ngày hạch toán)"',
       'Bảng TỔNG → công ty (I, II, III) → xe; số khớp màn hình; cuối có "Ngày dd Tháng mm Năm yyyy", "Người lập (Ký, họ tên)"']),
    C('In một số cột', 'P1', T10, ['1. Bỏ tích KM thực chạy, % Chênh lệch', '2. Bấm In'], '', ['Bản in không có 2 cột đã bỏ; STT và Công ty / Biển số xe luôn có']),
    C('In không chọn cột nào', 'P1', 'Đang mở cửa sổ In báo cáo.', ['1. Bỏ "Chọn tất cả"', '2. Bấm In'], '', ['Báo "Vui lòng chọn ít nhất 1 cột để in"', 'Không mở xem trước']),
    C('In danh sách chuyến xe', 'P0', T10, ['1. Chọn "Danh sách chuyến xe", giữ đủ cột, bấm In'], '',
      ['Xem trước "DANH SÁCH CHUYẾN XE — HIỆU QUẢ GỘP", 40 dòng, có dòng "40 chuyến · Cước: 24,720,667 · Chi phí lái xe: 18,129,331 · Lãi gộp: 6,591,336 VND"']),
    C('In lấy mọi trang theo bộ lọc', 'P0', 'Kỳ Năm nay, đang ở trang 1.', ['1. In bảng tổng hợp'], '', ['Bản in có đủ mọi công ty, mọi xe, dòng TỔNG khớp màn hình']),
    C('In vượt 2.000 dòng', 'P2', 'Bản danh sách chuyến xe kỳ có hơn 2.000 chuyến.', ['1. Chọn Danh sách chuyến xe, bấm In'], '',
      ['Cửa sổ xem trước chỉ báo số dòng vượt mức in tối đa 2,000 dòng, gợi ý thu hẹp bộ lọc hoặc dùng Xuất Excel', 'Không có nút In']),
    C('In ra máy in và đóng xem trước', 'P2', 'Đang ở cửa sổ xem trước.', ['1. Bấm In', '2. Bấm ×'], '', ['Bước 1: mở hộp thoại in của trình duyệt', 'Bước 2: đóng cửa sổ, báo cáo giữ nguyên']),
    C('Báo cáo chưa tải xong mà bấm In / Xuất Excel', 'P2', 'Mạng chậm, vừa mở màn.', ['1. Bấm In báo cáo trước khi báo cáo hiện số'], '',
      ['Báo "Báo cáo chưa tải xong, vui lòng thử lại."', 'Không mở cửa sổ chọn']),
]

# ================================================================== VIII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
G8 = [
    C('Hạch toán chuyến xe chở hàng mới thì báo cáo tăng', 'P0', 'Ghi số nền dòng xe 29D-53315 kỳ Tháng này. Chuyến xe chở hàng của xe 29D-53315 đã kết thúc, chưa hạch toán; cước 600,000.',
      ['1. Vận chuyển > Chuyến xe > Chuyến xe chở hàng chờ hạch toán, hạch toán chuyến với Công lái xe 60,000 (gắn lái xe), Xăng xe 40,000', '2. Mở lại báo cáo, Kỳ Tháng này'], '',
      ['Dòng 29D-53315: Số chuyến +1, Cước tăng 600,000, Chi phí lái xe tăng 100,000, Lãi gộp tăng 500,000', 'Khối tổng hợp và dòng TỔNG tăng tương ứng']),
    C('Hạch toán chuyến xe khác thì vào nhóm Chuyến xe khác', 'P1', 'Chuyến xe khác đã duyệt, kết thúc, chờ hạch toán.',
      ['1. Vận chuyển > Chuyến xe > Chuyến xe khác chờ hạch toán, hạch toán chuyến', '2. Mở lại báo cáo'], '',
      ['Ô Chuyến xe khác +1, Lãi gộp nhóm thay đổi đúng bằng lãi gộp chuyến mới']),
    C('Phiếu hạch toán bị huỷ / bỏ hạch toán thì báo cáo giảm', 'P1', 'Phiếu HT-1 đang có trên báo cáo.', ['1. Huỷ / bỏ hạch toán HT-1 ở màn phiếu hạch toán', '2. Mở lại báo cáo'], '',
      ['HT-1 không còn trên báo cáo; dòng xe, công ty, TỔNG giảm đúng số của HT-1']),
    C('Sửa km trên chuyến xe thì km đổi theo', 'P2', 'Chuyến của HT-1 có km bắt đầu 1,000, kết thúc 1,064.', ['1. Sửa km kết thúc thành 1,070 (khi chuyến còn cho sửa)', '2. Mở lại báo cáo'], '',
      ['KM thực chạy của HT-1 = 70; Chênh lệch, % Chênh lệch tính lại']),
    C('Khớp với Báo cáo chi tiết hiệu quả gộp theo chuyến xe', 'P0', 'Tài khoản TK-SA, Kỳ Năm nay.',
      ['1. Ghi dòng TỔNG báo cáo này', '2. Mở Báo cáo chi tiết hiệu quả gộp theo chuyến xe cùng Kỳ'], '',
      ['Số chuyến, Cước, Chi phí lái xe, Lãi gộp, các cột km ở dòng TỔNG 2 báo cáo bằng nhau', 'Từng xe khớp tổng các chuyến của xe đó ở báo cáo chi tiết']),
    C('Khớp chi phí với Báo cáo tổng hợp chi phí vận chuyển theo lái xe', 'P2', 'Tài khoản TK-SA, Kỳ Tháng trước.',
      ['1. Ghi Chi phí lái xe dòng TỔNG', '2. Mở Báo cáo tổng hợp chi phí vận chuyển theo lái xe cùng kỳ, cộng Công lái xe + Xăng xe + Chi phí khác + Vé cầu đường'], '',
      ['Hai số bằng nhau, trừ phần bút toán không gắn lái xe (báo cáo hiệu quả gộp CÓ tính, báo cáo theo lái xe không gắn được lái xe)', 'Ghi phần chênh vào Ghi chú để đối chiếu']),
    C('Biển số khoá ở danh mục vẫn giữ trên báo cáo cũ', 'P2', 'Biển số 29D-52336 có chuyến tháng 10/2026, sau đó bị khoá ở danh mục Biển số xe.', ['1. Mở báo cáo kỳ Tháng trước', '2. Mở ô Biển số xe'], '',
      ['Dòng xe 29D-52336 vẫn hiện số liệu', 'Ô Biển số xe chỉ liệt kê biển số đang hoạt động']),
]

# ================================================================== IX. PHÂN QUYỀN
G9 = [
    C('Mức Tổng công ty xem mọi công ty', 'P0', 'Tài khoản TK-SA có quyền ' + Q + ' mức Tổng công ty.', ['1. ' + MENU, '2. ' + LOC], '',
      ['Thấy chuyến của mọi công ty (3 công ty, 40 chuyến)', 'Ô Công ty mở, chọn được mọi công ty đang hoạt động, để trống = tất cả']),
    C('Mức Công ty chỉ thấy công ty của mình', 'P0', 'Tài khoản TK-CT có quyền ' + Q + ' mức Công ty, thuộc công ty CN Vinh.', ['1. ' + MENU, '2. ' + LOC], '',
      ['Chỉ còn công ty CN Vinh (18 chuyến, 2 xe)', 'Ô Công ty bị khoá ở CN Vinh, không xoá được', 'Popup, In, Excel cũng chỉ trong công ty CN Vinh']),
    C('Không quyền chỉ thấy chuyến mình lập bút toán', 'P0', 'Tài khoản NV-A không có quyền; NV-A lập bút toán hạch toán của 2 chuyến trong tháng 10/2026.', ['1. ' + MENU, '2. ' + LOC], '',
      ['Chỉ thấy đúng 2 chuyến đó', 'Ô Công ty khoá ở công ty của NV-A']),
    C('Có 2 vai trò khác mức thì áp mức cao hơn', 'P1', 'Tài khoản Z có vai trò cấp mức Công ty và vai trò khác cấp mức Tổng công ty.', ['1. Mở báo cáo'], '',
      ['Z thấy mọi công ty, ô Công ty mở (theo mức Tổng công ty)']),
] + pq_chung(M)

DESCRIPTION_BLOCK = [(a, _sach(b)) for a, b in DESCRIPTION_BLOCK]

GROUPS = [
    ('HIỂN THỊ TRANG & TRUY CẬP', G1),
    ('TÌM KIẾM & LỌC DANH SÁCH', G2),
    ('SỐ LIỆU BÁO CÁO', G3),
    ('XEM CHI TIẾT DANH SÁCH CHUYẾN XE', G4),
    ('TÙY CHỈNH CỘT', G5),
    ('XUẤT DANH SÁCH EXCEL', G6),
    ('IN BÁO CÁO', G7),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', G8),
    ('PHÂN QUYỀN', G9),
]

if __name__ == '__main__':
    print(dem(GROUPS))
    build_chuan(OUT, 'Trang tính1', '%s - Cập nhật ngày %s' % (TEN, NGAY), MODULE, DESCRIPTION_BLOCK, sections(GROUPS), loai='bao_cao')

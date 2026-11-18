# -*- coding: utf-8 -*-
"""Testcase "Báo cáo chi tiết chuyến xe" — KHUÔN CHUẨN skill testcase-documenter (tc_chuan.build_chuan, loai='bao_cao').
Mẫu đã duyệt: sale-customer-debt-reports/docs/compare/gen_testcase.py. Case chung ở ../hieu-qua-gop-xe/_tc_trp.py.
Không có TC cũ cho màn này.
Chạy: python gen_testcase.py  (tự gọi check_tc — phải 0 lỗi)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'hieu-qua-gop-xe'))
from _tc_trp import _sach, C, sections, dem, build_chuan, pt_chung, ky_chung, popup_chung, cot_chung, pq_chung  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

NGAY = '18/11/2026'
TEN = 'Báo cáo chi tiết chuyến xe'
MODULE = 'BC chi tiết chuyến xe'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
MENU = 'Vào phân hệ Vận chuyển > Báo cáo vận chuyển > bấm "Báo cáo chi tiết chuyến xe"'
LOC = 'Chọn Kỳ = Tháng trước (tháng 10/2026)'
T10 = 'Tài khoản TK-SA (quyền Xem báo cáo vận chuyển mức Tổng công ty); tháng 10/2026 trên môi trường thử có 56 chuyến (46 chở hàng, 10 khác), 132 phiếu nhập/xuất, 13 chuyến ghép, 65 khách hàng.'
Q1 = '"Xem báo cáo vận chuyển"'
Q2 = '"Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh"'


def L_(*lines):
    return '\n'.join(lines)


M = {
    'ten': TEN, 'menu': MENU, 'url': '/transport/trip-detail-report', 'loc': LOC,
    'dv': 'khách hàng', 'loc_nhieu': LOC + ', Xem theo = Khách hàng, ô Số dòng/trang = 10',
    'nhieu_trang': T10 + ' Có 66 nhóm khách hàng (7 trang).',
    'doi_loc': 'Chọn Đối tượng chịu phí = Nhân viên chịu',
    'thu_tu': 'khách hàng theo Cước sau thuế giảm dần (nhóm "Không có khách hàng" cuối), tuyến theo tên, phiếu mới đến cũ; góc nhìn Chuyến xe: chuyến mới đến cũ',
    'tong_ghi_chu': 'N đếm cả nhóm "Không có khách hàng" (tháng 10/2026: 66 = 65 khách + 1 nhóm không có khách)',
    'theo': 'theo ngày vận chuyển', 'ngay_loc': 'ngày tạo chuyến',
    'bien_ngay': 'Có chuyến TPE_CXCH_05504 tạo ngày 14/10/2026 (phiếu TPE_HTCXCH_03203).',
    'loc_nhieu_o': 'Kỳ Năm nay, Xem theo Chuyến xe, Tuyến đường, Lái xe "Bình"',
    'xoaloc_them': ', Xem theo về "Khách hàng"',
    'man_khac': 'Vận chuyển > Báo cáo vận chuyển > Báo cáo hiệu quả gộp xe vận tải',
    'popup_mo': LOC + ', bấm số 56 ở cột Số phiếu HT dòng TỔNG', 'popup_dv': 'phiếu',
    'pre_popup': T10, 'pre_0': 'Kỳ có ô Vé cầu đường / Chuyến xe khác bằng 0, hoặc Kỳ Tháng này chưa có chuyến.',
    'popup_kw': 'phong', 'popup_fields': 'phiếu nhập/xuất, khách hàng, mã và tên NVKD, xe, lái xe (KHÔNG tìm theo phiếu hạch toán / chuyến xe)',
    'popup_empty': 'Không có phiếu xuất / nhập nào khớp bộ lọc.', 'popup_filter': 'Chọn phiếu hạch toán', 'popup_sort': 'Ngày vận chuyển',
    'list_title': 'DANH SÁCH PHIẾU NHẬP/XUẤT THEO CHUYẾN XE', 'list_file': 'danh_sach_phieu_nhap_xuat_theo_chuyen_xe_yyyymmdd.xlsx',
    'popup_xl_noi_dung': 'File tải NGAY (không qua cửa sổ chọn cột), gồm đúng các dòng đang hiện trên popup (đã lọc + sắp), cột: STT, Phiếu nhập/xuất, Ngày vận chuyển, Phiếu hạch toán, Chuyến xe, Loại chuyến, Khách hàng, Mã NVKD, NVKD, NV chịu, Công ty chịu, Xe, Lái xe; dưới tiêu đề có dòng kỳ + điều kiện lọc và dòng "Phạm vi: <tiêu đề popup>"',
    'cot_ds': 'STT, Khách hàng / Tuyến đường / Phiếu hạch toán, Số phiếu HT, Xe, Lái xe, KM, KM phụ trội, Cước chính, Cước phụ trội, Cước thực tế, Thuế, Cước sau thuế, Vé cầu đường, NVKD, NV chịu, Công ty chịu',
    'cot_pre': ' (Xem theo Khách hàng)',
    'cot_n': '16', 'cot_khoa': 'Khách hàng / Tuyến đường / Phiếu hạch toán', 'cot_an': 'Cước phụ trội', 'cot_keo': 'Cước sau thuế',
    'quyen_ten': 'quyền ' + Q1 + ' và ' + Q2, 'quyen_cao': 'quyền ' + Q1 + ' mức Tổng công ty',
    'pre_url_cty': 'Tài khoản TK-CT (mức Công ty, công ty A); biết mã công ty B.',
}

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Báo cáo chỉ đọc: chi tiết từng chuyến xe đã hoàn thành trong kỳ — cước tính toán, cước thực tế, thuế, vé cầu đường, xe, lái xe, các phiếu xuất / nhập kho của chuyến; xem theo khách hàng (cước của từng khách) hoặc theo chuyến xe.',
        'Chức năng: Xem báo cáo (2 góc nhìn), Tìm kiếm / lọc, Xem danh sách phiếu nhập/xuất (popup), Tùy chỉnh cột, Xuất Excel, In.',
        'Đường vào: ' + MENU + '.')),
    ('2. Đối tượng được tính / hiển thị', L_(
        '1 "chuyến" = 1 phiếu hạch toán chuyến xe của chuyến xe chở hàng / chuyến xe khác ở trạng thái Hoàn thành, ngày tạo chuyến trong kỳ; chuyến xe khác còn phải có phiếu Đã hạch toán.',
        'Xem theo Khách hàng (mặc định): TỔNG -> khách hàng (I…) -> tuyến đường (1…) -> phiếu hạch toán (1.1…); 16 cột.',
        'Xem theo Chuyến xe: TỔNG -> chuyến (I…, mã phiếu hạch toán) -> phiếu nhập/xuất (1…); 23 cột.',
        'Khối tổng hợp: Chuyến xe (Phiếu hạch toán, Chuyến xe chở hàng, Chuyến xe khác, Ghép nhiều KH), Đối tượng chịu phí (NV chịu, Công ty chịu), Cước vận chuyển (Cước thực tế, Thuế, Cước sau thuế, Vé cầu đường).')),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '-  Chuyến chưa hoàn thành; chuyến xe khác có phiếu hạch toán chưa hạch toán.',
        '-  Chuyến có ngày tạo ngoài kỳ (dù phiếu hạch toán trong kỳ).',
        '-  Chuyến ngoài phạm vi quyền.',
        '-  Khi lọc Phiếu nhập/xuất hoặc Đối tượng chịu phí: các dòng phiếu không khớp bị ẩn.',
        '-  Chuyến không có phiếu nhập/xuất nào: có trên bảng, nhưng không có dòng trong popup danh sách phiếu.')),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô Kỳ lọc theo NGÀY TẠO CHUYẾN XE (ngày vận chuyển): Tuần này / Tháng này (mặc định) / Tháng trước / Năm nay / Tuỳ chọn (Từ ngày -> Đến ngày, tính cả 2 đầu).')),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Phân trang theo nhóm cấp 1 (khách hàng / chuyến), mặc định 10. Ô chọn cấp bung: Khách hàng = Chỉ khách hàng / Đến tuyến đường (mặc định) / Đến từng phiếu hạch toán; Chuyến xe = Chỉ chuyến / Đến từng phiếu nhập/xuất (mặc định).',
        'Bảng chính không sắp xếp theo cột. Cấu hình cột lưu riêng từng góc nhìn.')),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '-  Tiền / km dòng TỔNG cộng theo CHUYẾN, mỗi chuyến 1 lần.',
        '-  Góc nhìn Khách hàng: Cước thực tế / Thuế = cộng phần đã chia cho các phiếu của khách; thuế phiếu không khớp thuế chuyến thì chia theo tỉ lệ cước (có thể có số lẻ).',
        '-  Chuyến ghép >= 2 khách: KM, KM phụ trội, Cước chính, Cước phụ trội, Vé cầu đường để TRỐNG ở dòng khách; dòng TỔNG vẫn cộng.')),
    ('7. Phân quyền cấp', L_(
        'Màn không chặn quyền vào. Hai quyền chỉ mở rộng phạm vi (lấy phạm vi rộng nhất):',
        '-  "Xem báo cáo vận chuyển" — mức: Công ty / Tổng công ty.',
        '-  "Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh" — mức: Phòng ban / Công ty / Tổng công ty.',
        'Tổng công ty: mọi chuyến, ô Công ty mở. Công ty: chuyến thuộc công ty người xem. Phòng ban: chuyến thuộc phòng ban người xem. Không quyền: chuyến do mình lập.')),
    ('8. Cách tính các ô thống kê', L_(
        'Cước sau thuế = Cước thực tế + Thuế. KM = km thực tế trên chuyến (âm hiển thị 0). NVKD = người lập yêu cầu xuất / nhập hàng.',
        'Chuyến xe chở hàng: không đánh dấu công ty chịu thì là NV chịu. Ghép nhiều KH = số chuyến có >= 2 khách.',
        'Số phiếu HT (Khách hàng) = số phiếu hạch toán; Số phiếu (Chuyến xe) = số phiếu nhập/xuất. Chân bảng "Hiển thị a–b / N khách hàng" (hoặc N chuyến).')),
    ('9. Ghi chú đọc bảng', L_(
        '-  Số dạng 1,234,567, tối đa 2 số lẻ (Thuế có thể lẻ, vd 1,787,776.32); dòng TỔNG / nhóm số 0 in "0", dòng phiếu và popup số 0 để trống.',
        '-  KM, Cước chính… dòng TỔNG có thể lớn hơn tổng các khách — do chuyến ghép, không phải lỗi.',
        '-  Ô Công ty / Phòng ban / Bộ phận / Nhân viên kinh doanh lọc theo YÊU CẦU xuất / nhập hàng, nhưng phạm vi quyền xét theo CHUYẾN.',
        'Dữ liệu mẫu (môi trường thử 18/11/2026) tháng 10/2026: 56 chuyến, 132 phiếu, 13 chuyến ghép, NV chịu 9 phiếu, Công ty chịu 123 phiếu, Cước thực tế 59,166,384, Thuế 1,787,776.32, Cước sau thuế 60,954,160.32, KM 1,808; năm 2026: 2.313 chuyến, 3.880 phiếu.',
        'TK-SA (mức Tổng công ty), TK-CT (mức Công ty), TK-PB (quyền chi phí vận chuyển theo NVKD mức Phòng ban), NV-A (không quyền, có lập chuyến).')),
]

# ================================================================== I. HIỂN THỊ
G1 = [
    C('Mở màn hình từ menu', 'P0', 'Tài khoản bất kỳ.', ['1. Đăng nhập', '2. ' + MENU], '',
      ['Tiêu đề trang "Báo cáo chi tiết chuyến xe" có icon (i)', 'Báo cáo tự tải Kỳ "Tháng này", Xem theo "Khách hàng"', 'Kỳ chưa có chuyến: bảng "Không có chuyến xe nào khớp bộ lọc.", khối tổng hợp hiện 0']),
    C('Bố cục khu vực lọc và các nút', 'P1', 'Đang mở màn.', ['1. Quan sát khu vực lọc'], '',
      ['"Bộ lọc báo cáo chi tiết chuyến xe" + icon (i)', 'Ô: Kỳ, Xem theo, Công ty, Phiếu hạch toán, Chuyến xe, Tuyến đường, Lái xe, Biển số xe, Phiếu nhập/xuất, Đối tượng chịu phí, Phòng ban, Bộ phận, Nhân viên kinh doanh',
       'Nút Tìm kiếm, Xóa lọc; cụm nút: Cấu hình cột hiển thị, In báo cáo, Xuất Excel, Cài đặt bộ lọc, Ẩn tìm kiếm nâng cao']),
    C('Khối tổng hợp đầu trang', 'P0', T10, ['1. ' + LOC], '',
      ['Dòng "Kỳ tháng 10/2026 (theo ngày vận chuyển) · 65 khách hàng · 56 chuyến · Cước sau thuế 60,954,160.32"',
       'CHUYẾN XE (65 khách hàng): Phiếu hạch toán 56 (132 phiếu nhập/xuất), Chuyến xe chở hàng 46, Chuyến xe khác 10, Ghép nhiều KH 13',
       'ĐỐI TƯỢNG CHỊU PHÍ: NV chịu 9 phiếu, Công ty chịu 123 phiếu',
       'CƯỚC VẬN CHUYỂN (KM 1,808): Cước thực tế 59,166,384, Thuế 1,787,776.32, Cước sau thuế 60,954,160.32; ô Vé cầu đường ẩn vì bằng 0']),
    C('Kiểm tra đủ các cột — Xem theo Khách hàng', 'P0', 'Đang mở màn.', ['1. Đọc tiêu đề bảng'], '',
      ['STT | Khách hàng / Tuyến đường / Phiếu hạch toán (kèm ô chọn cấp) | Số phiếu HT | Xe | Lái xe | KM | KM phụ trội | Cước chính | Cước phụ trội | Cước thực tế | Thuế | Cước sau thuế | Vé cầu đường | NVKD | NV chịu | Công ty chịu']),
    C('Kiểm tra đủ các cột — Xem theo Chuyến xe', 'P0', 'Đang mở màn.', ['1. Chọn Xem theo = Chuyến xe', '2. Đọc tiêu đề bảng'], '',
      ['STT | Phiếu hạch toán / Phiếu nhập-xuất | Số phiếu | Ngày vận chuyển | Chuyến xe | Tuyến đường | KM | KM phụ trội | Cước chính | Cước phụ trội | Cước thực tế | Thuế | Cước sau thuế | Vé cầu đường | Mã NVKD | NVKD | Khách hàng | NV chịu | Công ty chịu | Xe tính cước | Xe | Mã lái xe | Lái xe',
       'Bảng rộng thì có thanh cuộn ngang']),
    C('Nội dung icon (i) tiêu đề cột', 'P2', 'Đang mở màn, Xem theo Khách hàng.', ['1. Rê chuột icon (i) cột KM, Cước sau thuế, NVKD'], '',
      ['KM: "Tổng km thực tế ghi trên chuyến xe…" + "Số của cả chuyến — chuyến ghép nhiều khách hàng để trống (không chia cho khách); dòng TỔNG cộng mỗi chuyến 1 lần"',
       'Cước sau thuế: "Cước thực tế + Thuế" + "Phần của khách = cộng các phiếu xuất / nhập của khách trên chuyến (kế toán đã chia khi hạch toán chuyến)"',
       'NVKD: "Người lập yêu cầu xuất / nhập hàng của các phiếu của khách trên chuyến"']),
    C('Cây 3 cấp góc nhìn Khách hàng', 'P0', T10, ['1. ' + LOC, '2. Chọn cấp "Đến từng phiếu hạch toán"'], '',
      ['Dòng TỔNG nền cam -> khách hàng I, II… (tên + mã KH chữ nhỏ) -> tuyến 1, 2… -> phiếu 1.1, 1.2…',
       'Dòng phiếu: mã phiếu hạch toán (liên kết) + dòng phụ "dd/mm/yyyy · mã chuyến xe"; Lái xe có mã lái xe ở dòng phụ',
       'Cột Xe, Lái xe, NVKD, NV chịu, Công ty chịu chỉ ghi ở dòng phiếu']),
    C('Nhãn "ghép N KH" của chuyến ghép', 'P0', T10, ['1. ' + LOC + ', bung đến từng phiếu', '2. Rê chuột vào nhãn "ghép 2 KH" của TPE_HTCXCH_03203'], '',
      ['Nhãn cam "ghép 2 KH" cạnh mã phiếu, ở cả 2 khách (VINFAST GIANG SƠN, Ô TÔ GIẢI PHÓNG)',
       'Tooltip: "Chuyến chở hàng của 2 khách hàng — cước / thuế ở dòng này là phần của khách đang xem.", "KM, cước chính / phụ trội, vé cầu đường của cả chuyến để trống (xem ở góc nhìn "Chuyến xe").", "Các khách hàng khác trên chuyến:" + tên khách kia và mã phiếu',
       'Cột KM, KM phụ trội, Cước chính, Cước phụ trội, Vé cầu đường của 2 dòng này để trống']),
    C('Cây 2 cấp góc nhìn Chuyến xe', 'P0', T10, ['1. ' + LOC + ', Xem theo Chuyến xe'], '',
      ['TỔNG -> chuyến I, II… (mã phiếu hạch toán liên kết, chuyến mới nhất trước: TPE_HTCXCH_03212 ngày 27/10/2026) -> phiếu nhập/xuất 1, 2… (PXK-…, PNK-… liên kết)',
       'Cột của chuyến chỉ ghi ở dòng chuyến; NVKD, Khách hàng, NV chịu, Công ty chịu chỉ ghi ở dòng phiếu']),
    C('Đổi Xem theo dựng lại bảng', 'P1', T10, ['1. ' + LOC + ', chọn cấp "Đến từng phiếu hạch toán"', '2. Đổi Xem theo = Chuyến xe', '3. Đổi lại Khách hàng'], '',
      ['Bảng dựng lại với bộ cột của góc nhìn mới, không còn cột / dòng cũ', 'Cấp bung về mặc định của góc nhìn ("Đến từng phiếu nhập/xuất" / "Đến tuyến đường")', 'Về trang 1; khối tổng hợp không đổi']),
    C('Ô chọn cấp bung', 'P1', T10, ['1. ' + LOC, '2. Chọn lần lượt Chỉ khách hàng / Đến tuyến đường / Đến từng phiếu hạch toán', '3. Bấm mũi tên ở 1 dòng tuyến'], '',
      ['Bảng thu / bung đúng cấp, không tải lại', 'Mũi tên chỉ bung / thu đúng dòng đã bấm']),
    C('Bấm mã chứng từ mở tab mới', 'P1', T10, ['1. Bấm mã phiếu hạch toán ở dòng phiếu', '2. Xem theo Chuyến xe: bấm mã chuyến xe, bấm PXK-38130'], '',
      ['Mỗi lần mở chi tiết phiếu hạch toán / chuyến xe / phiếu xuất kho ở tab mới', 'Màn báo cáo giữ nguyên']),
    C('Thu gọn / mở rộng khối tổng hợp', 'P2', 'Đang xem báo cáo.', ['1. Bấm Thu gọn', '2. Bấm Mở rộng'], '', ['Ẩn / hiện các khối số']),
    C('Thời gian tải báo cáo', 'P1', 'Tài khoản TK-SA; năm 2026 có 2.313 chuyến.', ['1. Chọn Kỳ Năm nay ở cả 2 góc nhìn'], '',
      ['Báo cáo hiện dưới 3 giây (môi trường thử đo 0,7–0,8 giây)', 'Trong lúc tải bảng mờ đi, không trắng màn']),
    C('Lỗi tải báo cáo giữ số liệu cũ', 'P2', 'Đang xem báo cáo có số.', ['1. Ngắt mạng', '2. Đổi Kỳ'], '', ['Báo lỗi, bảng giữ số liệu cũ']),
] + pt_chung(M)

# ================================================================== II. TÌM KIẾM & LỌC
G2 = ky_chung(M) + [
    C('Ô chữ chỉ lọc khi Enter hoặc Tìm kiếm', 'P0', T10, ['1. ' + LOC, '2. Gõ "03199" ở ô Phiếu hạch toán, chưa Enter', '3. Nhấn Enter'], '',
      ['Bước 2: báo cáo chưa đổi', 'Bước 3: còn 1 khách, 1 chuyến, Cước sau thuế 1,627,313']),
    C('Lọc Phiếu hạch toán / Chuyến xe gần đúng, không phân biệt hoa thường', 'P1', T10, ['1. Gõ "htcxch_032" ở Phiếu hạch toán, Enter', '2. Xoá, gõ "CXCH_055" ở Chuyến xe, Enter'], '',
      ['Mỗi lần chỉ còn chuyến có mã chứa chuỗi đã gõ (không phân biệt hoa thường)']),
    C('Lọc Lái xe theo tên', 'P0', T10, ['1. Gõ "Bình" ở ô Lái xe, Enter'], '', ['Chỉ còn chuyến có lái xe tên chứa "Bình" (lái xe công ty hoặc lái xe ngoài)']),
    C('Lọc Phiếu nhập/xuất chỉ hiện phiếu khớp', 'P0', T10, ['1. Xem theo Chuyến xe', '2. Gõ "PNK-11406" ở ô Phiếu nhập/xuất, Enter'], '',
      ['Chỉ còn chuyến TPV_HTCXK_00416 và CHỈ dòng PNK-11406 (3 phiếu nhập khác của chuyến bị ẩn)', 'Số phiếu của chuyến = 1']),
    C('Lọc Đối tượng chịu phí', 'P0', T10, ['1. ' + LOC, '2. Chọn Đối tượng chịu phí = Nhân viên chịu', '3. Đổi sang Công ty chịu'], '',
      ['Bước 2: "6 khách hàng · 7 chuyến"; khối Đối tượng chịu phí chỉ còn NV chịu 9 phiếu; dòng phiếu Công ty chịu bị ẩn',
       'Bước 3: còn 47 chuyến, Công ty chịu 123 phiếu']),
    C('Lọc Tuyến đường / Biển số xe', 'P0', T10, ['1. Chọn Tuyến đường "Liên Ninh, Hà Nội - Hà Giang, Hà Giang"', '2. Bỏ tuyến, chọn Biển số xe 29D-54533'], '',
      ['Mỗi lần chỉ còn chuyến có đúng tuyến / biển số ghi trên chuyến']),
    C('Lọc Công ty / Phòng ban / Bộ phận / Nhân viên kinh doanh theo yêu cầu xuất nhập', 'P0', 'Tài khoản TK-SA; chuyến CX-1 chở 2 phiếu: PXK-A (yêu cầu của NV-A, phòng P1) và PXK-B (yêu cầu của NV-B, phòng P2).',
      ['1. Chọn Phòng ban P1', '2. Bỏ Phòng ban, chọn Nhân viên kinh doanh NV-A'], '',
      ['Cả 2 lần CX-1 đều lên báo cáo vì có PXK-A khớp', 'Dòng PXK-B VẪN hiện dưới CX-1 (ô này chỉ chọn chuyến, không ẩn phiếu)']),
    C('Ô con bị xoá khi đổi ô cha', 'P1', 'Tài khoản TK-SA.', ['1. Chọn Công ty A, Phòng ban P1, Bộ phận B1, Nhân viên kinh doanh NV-A', '2. Đổi Công ty sang B', '3. Chọn lại Phòng ban, rồi đổi Phòng ban'], '',
      ['Bước 2: Phòng ban, Bộ phận, Nhân viên kinh doanh về trống; danh sách Phòng ban theo công ty B', 'Bước 3: Bộ phận, Nhân viên kinh doanh về trống; Bộ phận chỉ liệt kê bộ phận của phòng ban đã chọn']),
    C('Lọc kết hợp nhiều ô', 'P1', T10, ['1. Xem theo Chuyến xe, Đối tượng chịu phí = Công ty chịu, Biển số xe 37H-08470'], '', ['Chỉ còn chuyến của xe 37H-08470 có phiếu công ty chịu; tổng hợp tính lại']),
    C('Lọc không có kết quả', 'P1', T10, ['1. Gõ "zzz" ở Phiếu nhập/xuất, Enter'], '', ['"Không có chuyến xe nào khớp bộ lọc."; khối tổng hợp 0']),
    C('Ô chữ: ký tự đặc biệt, khoảng trắng, chuỗi dài', 'P2', T10, ['1. Lần lượt gõ các chuỗi ở Test data vào ô Phiếu hạch toán, Enter'], ['%', '_', '  03199  ', 'Chuỗi 300 ký tự'],
      ['% và _ hiểu là ký tự thường (không khớp tất cả)', 'Khoảng trắng đầu / cuối được bỏ qua: "  03199  " ra như "03199"', 'Chuỗi dài: không lỗi, "Không có chuyến xe nào khớp bộ lọc."']),
    C('Xoá chữ trong ô thì lọc bỏ', 'P1', 'Đang lọc Phiếu hạch toán "03199".', ['1. Xoá hết chữ trong ô', '2. Nhấn Enter'], '', ['Báo cáo quay về đủ 56 chuyến']),
]

# ================================================================== III. SỐ LIỆU
G3 = [
    C('Cước sau thuế = Cước thực tế + Thuế', 'P0', T10, ['1. ' + LOC + ', bung đến phiếu', '2. Đọc khách I'], '', ['6,520,000 + 521,600 = 7,041,600 ở dòng khách, tuyến, phiếu']),
    C('Chuyến ghép: cước chia cho các khách, cộng lại bằng cước chuyến', 'P0', T10, ['1. Đọc 2 dòng TPE_HTCXCH_03203 ở khách I và II', '2. Xem theo Chuyến xe, đọc dòng chuyến TPE_HTCXCH_03203'], '',
      ['Cước thực tế: 6,520,000 + 6,507,164 = 13,027,164 = Cước thực tế của chuyến ở góc nhìn Chuyến xe', 'Thuế 2 khách cộng lại = Thuế của chuyến']),
    C('Thuế chia theo tỉ lệ khi phiếu không ghi thuế', 'P1', 'Chuyến xe khác CX-2: thuế 100,000 ghi ở chuyến, các phiếu để thuế 0; khách A cước 300,000, khách B cước 700,000.', ['1. Chọn kỳ chứa CX-2, bung đến phiếu'], '',
      ['Thuế khách A = 100,000 × 300,000 / 1,000,000 = 30,000; khách B = 70,000 (phần lẻ dồn khách cuối)', 'Cộng 2 khách = 100,000']),
    C('Dòng TỔNG góc nhìn Khách hàng khớp tổng các khách', 'P0', T10, ['1. Cộng Cước thực tế, Thuế, Cước sau thuế của 66 nhóm (7 trang)'], '',
      ['= 59,166,384 / 1,787,776.32 / 60,954,160.32 ở dòng TỔNG']),
    C('KM, Cước chính dòng TỔNG có thể lớn hơn tổng các khách', 'P1', T10, ['1. Cộng cột KM của 66 nhóm', '2. So dòng TỔNG 1,808'], '',
      ['Tổng các khách NHỎ HƠN 1,808 vì 13 chuyến ghép để trống ở dòng khách', 'Ghi chú: không phải lỗi (dòng TỔNG cộng mỗi chuyến 1 lần)']),
    C('Hai góc nhìn cùng dòng TỔNG tiền / km', 'P0', T10, ['1. Ghi dòng TỔNG góc nhìn Khách hàng', '2. Đổi Xem theo Chuyến xe'], '',
      ['KM, KM phụ trội, Cước chính, Cước phụ trội, Cước thực tế, Thuế, Cước sau thuế, Vé cầu đường bằng nhau', 'Số phiếu dòng TỔNG: Khách hàng 56 (phiếu hạch toán), Chuyến xe 132 (phiếu nhập/xuất)']),
    C('Số phiếu HT của nhóm khách / tuyến', 'P0', T10, ['1. Đọc khách IV (Xây dựng hạ tầng Bắc Trung Nam)'], '', ['Khách IV: 3 phiếu = 1 + 1 + 1 của 3 tuyến']),
    C('Số phiếu dòng chuyến = số phiếu nhập/xuất', 'P0', T10, ['1. Xem theo Chuyến xe', '2. Đọc chuyến TPV_HTCXK_00416'], '', ['Số phiếu 4 = 4 dòng PNK-11406, 11405, 11410, 11408']),
    C('KM âm hiển thị 0', 'P1', 'Chuyến CX-3 có km thực tế ghi âm (-20).', ['1. Chọn kỳ chứa CX-3'], '', ['KM của chuyến CX-3 = 0 (không cộng số âm vào TỔNG)']),
    C('NVKD là người lập yêu cầu xuất / nhập', 'P0', 'Phiếu PXK-38130 thuộc yêu cầu xuất do Trịnh Thị Lợi (12310452) lập.', ['1. Xem theo Chuyến xe, tìm PXK-38130'], '', ['Mã NVKD 12310452, NVKD Trịnh Thị Lợi', 'Chuyến xe khác cũng lấy NVKD theo người lập yêu cầu']),
    C('NV chịu / Công ty chịu', 'P0', T10, ['1. Đọc khối Đối tượng chịu phí', '2. Đếm ✓ ở 2 cột trong popup Tất cả phiếu'], '',
      ['NV chịu 9 + Công ty chịu 123 = 132 phiếu', 'Chuyến xe chở hàng: phiếu không đánh dấu công ty chịu thì có ✓ ở NV chịu']),
    C('Kỳ theo ngày tạo chuyến', 'P0', 'Chuyến CX-4 tạo 30/09/2026, hoàn thành và hạch toán 02/10/2026.', ['1. Kỳ Tuỳ chọn 01/09/2026 - 30/09/2026', '2. Kỳ Tháng 10/2026'], '', ['CX-4 có ở kỳ tháng 9, KHÔNG có ở kỳ tháng 10']),
    C('Chuyến chưa hoàn thành không lên', 'P0', 'Chuyến CX-5 trong kỳ đang ở trạng thái chưa hoàn thành.', ['1. Chọn kỳ chứa CX-5, tìm mã chuyến'], '', ['CX-5 không có trên báo cáo']),
    C('Chuyến xe khác chưa hạch toán không lên', 'P1', 'Chuyến xe khác CX-6 hoàn thành nhưng phiếu hạch toán chưa hạch toán.', ['1. Chọn kỳ chứa CX-6'], '', ['CX-6 không có trên báo cáo']),
    C('Nhóm "Không có khách hàng" luôn cuối', 'P1', T10, ['1. ' + LOC + ', về trang cuối'], '', ['Nhóm "Không có khách hàng" là nhóm cuối cùng, chứa phiếu nhập kho / dòng không gắn khách']),
    C('Thứ tự khách theo Cước sau thuế giảm dần', 'P0', T10, ['1. ' + LOC], '', ['I 7,041,600 > II 7,027,737.12 > III 3,951,763.2 > IV 3,713,795 > …']),
    C('Định dạng số', 'P1', T10, ['1. ' + LOC], '',
      ['Dấu phẩy ngăn nghìn, tối đa 2 số lẻ (1,787,776.32); số âm có "-" (KM phụ trội -3)', 'Dòng TỔNG / nhóm: 0 in "0" chữ nhạt; dòng phiếu: 0 để trống', 'Cột chuyến ghép để trống, không in 0']),
]

# ================================================================== IV. XEM CHI TIẾT
G4 = [
    C('Mở popup từ dòng TỔNG', 'P0', T10, ['1. ' + LOC, '2. Bấm số 56 ở dòng TỔNG'], '',
      ['Popup "Tất cả phiếu nhập/xuất", dòng phụ "132 phiếu · 54 chuyến · Kỳ tháng 10/2026"',
       'Cột: STT, Ngày vận chuyển, Phiếu hạch toán, Chuyến xe, Phiếu nhập/xuất, Khách hàng, NVKD (mã ở dòng phụ), NV chịu, Công ty chịu, Xe, Lái xe',
       'Ghi chú: 54 < 56 vì 2 chuyến không có phiếu nhập/xuất']),
    C('Mở popup từ ô Ghép nhiều KH', 'P0', T10, ['1. Bấm số 13 ở ô Ghép nhiều KH'], '', ['Tiêu đề "Chuyến chở hàng của nhiều khách hàng"; mọi phiếu thuộc 13 chuyến ghép']),
    C('Mở popup từ NV chịu / Công ty chịu', 'P0', T10, ['1. Bấm số 9 ở ô NV chịu'], '', ['Tiêu đề "Phiếu nhân viên chịu phí", 9 dòng, cột NV chịu đều ✓']),
    C('Mở popup từ dòng khách / tuyến', 'P0', T10, ['1. Bấm số ở dòng khách I', '2. Bấm số ở dòng tuyến của khách IV'], '',
      ['Bước 1: tiêu đề "CÔNG TY TRÁCH NHIỆM HỮU HẠN VINFAST GIANG SƠN - 22TTUPHA-102", chỉ phiếu của khách', 'Bước 2: tiêu đề "<khách> › <tuyến>", chỉ phiếu của khách trên tuyến']),
    C('Mở popup từ dòng chuyến (Chuyến xe)', 'P1', T10, ['1. Xem theo Chuyến xe', '2. Bấm số 4 ở chuyến TPV_HTCXK_00416'], '', ['4 dòng; ẩn ô "Chọn phiếu hạch toán"']),
    C('Mở popup từ ô Chuyến xe khác', 'P1', T10, ['1. Bấm số 10 ở ô Chuyến xe khác'], '', ['Tiêu đề "Chuyến xe khác"; ẩn ô "Chọn loại chuyến"']),
] + popup_chung(M)

# ================================================================== V. TÙY CHỈNH CỘT
G5 = cot_chung(M) + [
    C('Cấu hình cột lưu riêng từng góc nhìn', 'P1', 'Đã ẩn cột Cước phụ trội ở góc nhìn Khách hàng.', ['1. Đổi Xem theo = Chuyến xe', '2. Mở Tuỳ chỉnh cột'], '',
      ['Góc nhìn Chuyến xe vẫn hiện Cước phụ trội', 'Cửa sổ liệt kê 23 mục của góc nhìn Chuyến xe (khoá STT, Phiếu hạch toán / Phiếu nhập-xuất)']),
]

# ================================================================== VI. XUẤT EXCEL
G6 = [
    C('Xuất Excel tải file ngay theo góc nhìn Khách hàng', 'P0', T10, ['1. ' + LOC, '2. Bấm Xuất Excel', '3. Mở file'], '',
      ['Không mở cửa sổ chọn; hiện biểu tượng đang xử lý rồi tải "bao_cao_chi_tiet_chuyen_xe_theo_khach_hang_yyyymmdd.xlsx" (sheet "Theo khách hàng")',
       'Logo + "BÁO CÁO CHI TIẾT CHUYẾN XE", dòng điều kiện "… · Xem theo khách hàng"; dòng TỔNG -> khách -> tuyến -> phiếu, đủ mọi trang, mọi cấp',
       'Cột Ngày vận chuyển, Chuyến xe, Mã lái xe tách riêng; số khớp màn hình']),
    C('Xuất Excel theo góc nhìn Chuyến xe', 'P0', T10, ['1. Xem theo Chuyến xe', '2. Bấm Xuất Excel'], '', ['File "bao_cao_chi_tiet_chuyen_xe_theo_chuyen_xe_yyyymmdd.xlsx", sheet "Theo chuyến xe", TỔNG -> chuyến -> phiếu']),
    C('Xuất lấy mọi trang theo bộ lọc', 'P0', 'Đang lọc Đối tượng chịu phí = Nhân viên chịu, trang 1.', ['1. Xuất Excel'], '', ['File chỉ gồm 7 chuyến, 9 phiếu NV chịu, đủ mọi nhóm']),
    C('Định dạng file', 'P1', T10, ['1. Mở file, bấm 1 ô số, cuộn xuống'], '',
      ['Ô số kiểu SỐ, 1,234,567; tiêu đề + 2 cột đầu cố định khi cuộn', 'Màu dòng: TỔNG cam, cấp 1 xanh đậm, cấp 2 xanh nhạt, lá trắng; số 0 dòng lá để trống', 'Cuối file có khối ký "Người lập"; tiếng Việt đúng']),
    C('Xuất khi không có dữ liệu', 'P2', 'Kỳ Tháng này chưa có chuyến.', ['1. Xuất Excel'], '', ['Vẫn tải file có tiêu đề, dòng TỔNG = 0, không lỗi']),
    C('Thời gian xuất cả năm', 'P2', 'Tài khoản TK-SA, Kỳ Năm nay (2.313 chuyến).', ['1. Xuất Excel, bấm giờ'], '', ['File tải về trong khoảng 15 giây, không báo lỗi quá thời gian']),
    C('Cấu hình cột không ảnh hưởng file', 'P2', 'Đã ẩn cột Cước phụ trội.', ['1. Xuất Excel'], '', ['File vẫn có cột Cước phụ trội']),
]

# ================================================================== VII. IN
G7 = [
    C('Mở cửa sổ In báo cáo', 'P0', T10, ['1. ' + LOC, '2. Bấm In báo cáo'], '',
      ['"In bảng tổng hợp" ("Đúng bảng đang xem, đủ mọi trang và mọi phiếu hạch toán, kèm dòng TỔNG.") / "Danh sách phiếu nhập/xuất"',
       'Chọn cột in 17 cột: Số phiếu hạch toán, Ngày vận chuyển, Chuyến xe, Xe, Mã lái xe, Tên lái xe, KM, KM phụ trội, Cước chính, Cước phụ trội, Cước thực tế, Thuế, Cước sau thuế, Vé cầu đường, NV kinh doanh, NV chịu, Công ty chịu']),
    C('In bảng tổng hợp góc nhìn Khách hàng', 'P0', T10, ['1. In bảng tổng hợp, đủ cột, bấm In'], '',
      ['"Xem trước báo cáo chi tiết chuyến xe": tiêu đề công ty, "BÁO CÁO CHI TIẾT CHUYẾN XE", "Kỳ tháng 10/2026 (theo ngày vận chuyển) · Xem theo khách hàng"',
       'TỔNG -> "Mã KH - Tên KH" (I…) -> tuyến (1…) -> phiếu (1.1…, chuyến ghép ghi "(ghép 2 KH)"); số khớp màn hình']),
    C('In bảng tổng hợp góc nhìn Chuyến xe', 'P1', T10, ['1. Xem theo Chuyến xe, In báo cáo > In bảng tổng hợp > In'], '', ['Cột chọn = cột của góc nhìn Chuyến xe; bản in chuyến -> phiếu nhập/xuất']),
    C('In danh sách phiếu nhập/xuất', 'P0', T10, ['1. Chọn "Danh sách phiếu nhập/xuất", bấm In'], '', ['"DANH SÁCH PHIẾU NHẬP/XUẤT THEO CHUYẾN XE", 132 dòng, 12 cột']),
    C('In một số cột / không chọn cột', 'P1', 'Đang mở cửa sổ In báo cáo.', ['1. Bỏ tích Cước chính, Cước phụ trội, bấm In', '2. Mở lại, bỏ "Chọn tất cả", bấm In'], '',
      ['Bước 1: bản in không có 2 cột đó', 'Bước 2: "Vui lòng chọn ít nhất 1 cột để in", không mở xem trước']),
    C('In vượt 2.000 dòng', 'P1', 'Kỳ Năm nay, Xem theo Khách hàng (745 nhóm, hơn 2.000 dòng in).', ['1. In bảng tổng hợp'], '',
      ['Cửa sổ xem trước chỉ báo vượt mức in tối đa 2,000 dòng, gợi ý thu hẹp bộ lọc / Xuất Excel; không có nút In']),
    C('Hủy / đóng cửa sổ in', 'P2', 'Đang mở cửa sổ In báo cáo.', ['1. Bấm Hủy'], '', ['Đóng, báo cáo giữ nguyên']),
    C('Bản in khớp dòng phiếu trên màn', 'P2', T10, ['1. In bảng tổng hợp góc nhìn Khách hàng', '2. So cột Số phiếu hạch toán ở dòng phiếu TPE_HTCXCH_03203 của khách II'], '',
      ['Dòng phiếu trên màn để trống Số phiếu HT; ghi nhận giá trị trên bản in vào Ghi chú (bản in có thể ghi số phiếu nhập/xuất của khách trên chuyến)']),
]

# ================================================================== VIII. RÀNG BUỘC
G8 = [
    C('Hoàn thành + hạch toán chuyến xe chở hàng mới thì báo cáo tăng', 'P0', 'Ghi số nền dòng TỔNG kỳ Tháng này. Có chuyến xe chở hàng tạo trong tháng này, chở 1 phiếu xuất kho của khách K, cước 800,000, thuế 64,000.',
      ['1. Hoàn thành chuyến, hạch toán ở Vận chuyển > Chuyến xe > Chuyến xe chở hàng chờ hạch toán', '2. Mở lại báo cáo, Kỳ Tháng này'], '',
      ['Phiếu hạch toán +1, phiếu nhập/xuất +1; Cước thực tế +800,000, Thuế +64,000, Cước sau thuế +864,000', 'Khách K có dòng phiếu mới; NVKD = người lập yêu cầu xuất của phiếu']),
    C('Chuyến chở 2 khách hiện nhãn ghép', 'P1', 'Chuyến mới chở phiếu xuất của khách K1 và K2, kế toán chia cước 500,000 / 300,000 khi hạch toán.', ['1. Hạch toán chuyến', '2. Mở báo cáo, bung đến phiếu'], '',
      ['2 dòng phiếu "ghép 2 KH" ở K1 (500,000) và K2 (300,000); Ghép nhiều KH +1']),
    C('Chuyến xe khác vào báo cáo sau khi hạch toán', 'P1', 'Chuyến xe khác hoàn thành, chưa hạch toán.', ['1. Mở báo cáo, tìm chuyến', '2. Hạch toán ở Chuyến xe khác chờ hạch toán', '3. Mở lại báo cáo'], '',
      ['Bước 1: chưa có', 'Bước 3: có trong nhóm Chuyến xe khác']),
    C('Khớp NVKD với yêu cầu xuất hàng', 'P2', 'Phiếu PXK-38130.', ['1. Mở phiếu xuất kho PXK-38130 từ báo cáo, mở yêu cầu xuất của phiếu'], '', ['Người lập yêu cầu xuất = NVKD trên báo cáo (Trịnh Thị Lợi)']),
    C('Khớp với Báo cáo hiệu quả gộp xe vận tải', 'P2', 'Cùng tài khoản, cùng xe, cùng tháng.', ['1. So số chuyến của 1 xe ở 2 báo cáo'], '',
      ['Có thể lệch vì báo cáo này lọc theo ngày tạo chuyến, báo cáo hiệu quả gộp lọc theo ngày hạch toán — ghi ngày của chuyến lệch vào Ghi chú']),
    C('Mở phiếu nhập kho từ báo cáo', 'P2', T10, ['1. Xem theo Chuyến xe, bấm PNK-11406'], '', ['Mở màn chi tiết Phiếu nhập kho PNK-11406 ở tab mới']),
]

# ================================================================== IX. PHÂN QUYỀN
G9 = [
    C('Mức Tổng công ty (quyền Xem báo cáo vận chuyển)', 'P0', 'TK-SA có quyền ' + Q1 + ' mức Tổng công ty.', ['1. ' + MENU, '2. ' + LOC], '', ['Thấy 56 chuyến của mọi công ty; ô Công ty mở']),
    C('Mức Tổng công ty (quyền chi phí vận chuyển theo NVKD)', 'P0', 'Tài khoản chỉ có quyền ' + Q2 + ' mức Tổng công ty.', ['1. ' + LOC], '', ['Thấy như TK-SA (mọi chuyến), ô Công ty mở']),
    C('Mức Công ty', 'P0', 'TK-CT có quyền ' + Q1 + ' mức Công ty, công ty CN Vinh.', ['1. ' + LOC], '',
      ['Chỉ thấy chuyến có công ty ghi trên chuyến = CN Vinh', 'Ô Công ty khoá ở CN Vinh; ô Phòng ban chỉ liệt kê phòng ban CN Vinh']),
    C('Mức Phòng ban (chỉ có ở quyền chi phí vận chuyển theo NVKD)', 'P0', 'TK-PB có quyền ' + Q2 + ' mức Phòng ban, thuộc phòng P1.', ['1. ' + LOC], '',
      ['Chỉ thấy chuyến có phòng ban ghi trên chuyến = P1', 'Ô Công ty khoá ở công ty của TK-PB']),
    C('Không quyền chỉ thấy chuyến mình lập', 'P0', 'NV-A không có 2 quyền; NV-A lập 3 chuyến trong tháng 10/2026.', ['1. ' + LOC], '', ['Chỉ thấy đúng 3 chuyến đó']),
    C('Nhiều quyền khác mức thì lấy phạm vi rộng nhất', 'P1', 'Tài khoản có ' + Q2 + ' mức Phòng ban và ' + Q1 + ' mức Công ty.', ['1. ' + LOC], '', ['Phạm vi theo mức Công ty (rộng hơn)']),
] + pq_chung(M)

DESCRIPTION_BLOCK = [(a, _sach(b)) for a, b in DESCRIPTION_BLOCK]

GROUPS = [
    ('HIỂN THỊ TRANG & TRUY CẬP', G1),
    ('TÌM KIẾM & LỌC DANH SÁCH', G2),
    ('SỐ LIỆU BÁO CÁO', G3),
    ('XEM CHI TIẾT DANH SÁCH PHIẾU NHẬP/XUẤT', G4),
    ('TÙY CHỈNH CỘT', G5),
    ('XUẤT DANH SÁCH EXCEL', G6),
    ('IN BÁO CÁO', G7),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', G8),
    ('PHÂN QUYỀN', G9),
]

if __name__ == '__main__':
    print(dem(GROUPS))
    build_chuan(OUT, 'Trang tính1', '%s - Cập nhật ngày %s' % (TEN, NGAY), MODULE, DESCRIPTION_BLOCK, sections(GROUPS), loai='bao_cao')

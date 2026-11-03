# -*- coding: utf-8 -*-
"""Testcase "BC chi tiết công nợ KH" — KHUÔN CHUẨN tab "13. DM quốc gia" (loại bao_cao, 03/11/2026).

Viết lại từ gen_testcase_v1.py (bản 02/11 sai khuôn, giữ để tra): giữ mọi case nghiệp vụ, xếp lại theo nhóm chuẩn
(xuat-tai-lieu-chuyen-doi/TC_CHUAN.md), bổ sung case theo checklist "Mẫu tài liệu.xlsx". Case chung sinh từ
../compare/_tc_bc_chung.py (dùng chung 3 màn báo cáo công nợ).
Màn KHÔNG có nút In, KHÔNG có sắp xếp / tùy chỉnh cột => không có các nhóm đó.
Chạy: python gen_testcase.py  (tự gọi check_tc — phải 0 lỗi)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'compare'))
sys.path.insert(0, os.path.join(GOPDB, 'xuat-tai-lieu-chuyen-doi'))
from _tc_chuan import build_chuan  # noqa: E402
from _tc_bc_chung import C, sections, dem, pt_chung, tk_chung, luu_chung, xl_chung, pq_chung  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

NGAY = '03/11/2026'
TEN = 'BC chi tiết công nợ KH'
MODULE = 'BC chi tiết công nợ KH'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)


def J(*lines):
    return '\n'.join(lines)


MENU = 'Vào phân hệ Bán hàng > Báo cáo > nhóm Báo cáo công nợ > bấm "Chi tiết công nợ KH"'
LN = 'Chọn thời gian để xem báo cáo.'
TC_ = 'phân hệ Tài chính > '
MN = {
    'pxh': TC_ + 'Hàng hoá - Dịch vụ - Vận chuyển > Xuất hàng > "Phiếu xuất hàng"',
    'pnh': TC_ + 'Hàng hoá - Dịch vụ - Vận chuyển > Nhập hàng > "Phiếu nhập hàng"',
    'pt': TC_ + 'Quản lý tiền > "Phiếu thu"',
    'pbc': TC_ + 'Quản lý tiền > "Phiếu báo có"',
    'pc': TC_ + 'Quản lý tiền > "Phiếu chi"',
    'unc': TC_ + 'Quản lý tiền > "Phiếu ủy nhiệm chi"',
    'ycdc': TC_ + 'Khởi tạo > "Phiếu yêu cầu điều chỉnh công nợ"',
    'pkt': TC_ + 'Sổ tổng hợp > "Phiếu kế toán"',
    'dk': TC_ + 'Khai báo đầu kỳ > "Khai báo đầu kỳ công nợ"',
}
LOC = 'Chọn Thời gian = ngày 1 tháng này đến hôm nay, Khách hàng = KH-TEST'
XEM = 'dòng hợp đồng HD-TEST-01, dòng khách hàng KH-TEST (chữ đậm) và dòng Tổng cộng'
TT = 'Lọc khách hàng 89THUPTR-62, Thời gian 01/10/2026 - 31/10/2026 (môi trường thử).'
NHIEU = 'Tài khoản TK-ALL (quyền tổng công ty); Thời gian 01/10/2026 - 31/10/2026 cho ra hơn 30 dòng hợp đồng.'
NEN = 'Đã ghi số nền của ' + XEM + ' (case "Ghi số nền trước khi lập chứng từ").'

M = {
    'dv': 'dòng hợp đồng',
    'loc': 'Đăng nhập TK-ALL, chọn Thời gian 01/10/2026 - 31/10/2026',
    'nhieu_trang': NHIEU,
    'tong_ghi_chu': ' (không đếm dòng khách hàng, dòng Tổng cộng)',
    'pre_tong': NHIEU + ' Môi trường thử: "Hiển thị 1–10 / 25,309 dòng hợp đồng".',
    'doi_loc': 'Chọn Số dư cuối kỳ = "Dư nợ"',
    'tu_khoa': '1141',
    'loi_nhac': LN,
    'man_khac': 'Bán hàng > Báo cáo > Báo cáo công nợ > Tổng hợp công nợ theo NV',
    'excel_file': 'bao_cao_chi_tiet_cong_no_khach_hang.xlsx',
    'so_truong': '14',
    'xl_ngay': 'Không có cột ngày; cột Phòng ban / Bộ phận / NVKD là chữ',
    'nhom_quyen': 'Báo cáo chi tiết công nợ khách hàng',
    'menu': MENU,
    'nut': 'Xuất Excel',
    'url': '<địa chỉ hệ thống>/sale/customer-debt-details',
    'quyen_rong': 'Xem báo cáo chi tiết công nợ khách hàng theo tổng công ty',
    'co_dau': 'Từ khóa: "THIÊN TRƯỜNG" rồi "THIEN TRUONG"',
    'loc_khong_kh': 'Chọn Thời gian 01/10/2026 - 31/10/2026, không chọn Khách hàng',
}
PT = pt_chung(M)
M['loc'] = 'Chọn Thời gian 01/10/2026 - 31/10/2026, Khách hàng 89THUPTR-62'

DU_LIEU = J(
    'Dữ liệu mẫu dùng xuyên suốt:',
    '-  TK-ALL: có quyền "Xem báo cáo chi tiết công nợ khách hàng theo tổng công ty".',
    '-  TK-CTY: chỉ có quyền "... theo công ty" (Công ty A). TK-PB: chỉ quyền "... theo phòng ban", quản lý phòng PB-1.',
    '-  TK-BP: chỉ quyền "... theo bộ phận", quản lý bộ phận BP-1. TK-NV: nhân viên PB-1, KHÔNG có quyền nào, là người tạo HD-TEST-01.',
    '-  KH-TEST: khách hàng mới, chưa có công nợ. HD-TEST-01, HD-TEST-02: hợp đồng bán hàng của KH-TEST do TK-NV tạo, đã ký '
    '(hợp đồng bán hàng lập ở hệ thống cũ — có sẵn).',
    '-  Mỗi chứng từ lập ở các case lập chứng từ phải được HẠCH TOÁN (có ngày hạch toán) mới lên báo cáo.',
    '-  Số mẫu trên môi trường thử (02/11/2026): kỳ 01/10/2026 - 31/10/2026, khách 89THUPTR-62 có 3 hợp đồng; dòng khách hàng: Số dư đầu kỳ '
    '848,527,621; Hàng hóa/Dịch vụ 1,595,658,222; Số dư cuối kỳ 943,656,841.',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', J(
        'Báo cáo công nợ phải thu theo khách hàng, chi tiết đến từng hợp đồng: Số dư đầu kỳ, Phát sinh tăng (Hàng hóa/Dịch vụ, '
        'Điều chỉnh công nợ, Cộng), Phát sinh giảm (Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ, Cộng), Trả lại tiền thừa, '
        'Số dư cuối kỳ. Màn chỉ đọc.',
        'Chức năng: xem báo cáo, lọc, popup "Chi tiết chứng từ" khi bấm số tiền, mở hợp đồng ở tab mới, Xuất Excel.',
        'Đường vào: ' + MENU + '. Tiêu đề màn: "Báo cáo chi tiết công nợ khách hàng".',
    )),
    ('2. Đối tượng được tính / hiển thị', J(
        'Bút toán vào sổ phải thu khách hàng (TK 131 + tài khoản con), số tiền quy đổi VND, số tiền > 0.',
        '-  Dòng hợp đồng: mỗi cặp (khách hàng, hợp đồng) có bút toán đến hết Đến ngày — kể cả không phát sinh trong kỳ.',
        '-  Chứng từ không gắn hợp đồng: 1 dòng, ô hợp đồng trống.',
        '-  Dòng khách hàng (đậm): cộng mọi hợp đồng của khách (mọi trang).',
        '-  Dòng Tổng cộng: tổng toàn bộ theo bộ lọc (xem mục 6).',
        'Chứng từ theo cột: Hàng hóa/Dịch vụ = phiếu xuất hàng, xuất bán hàng mượn, hạch toán dịch vụ, thanh lý, hạch toán dịch vụ BH-SC, '
        'khai báo công nợ đầu kỳ; ĐCCN = phiếu kế toán; Nhập trả lại = phiếu nhập hàng; Đã thanh toán = phiếu thu, phiếu báo có, '
        'khai báo công nợ đầu kỳ; Trả lại tiền thừa = phiếu chi, phiếu ủy nhiệm chi.',
    )),
    ('3. Đối tượng bị ẩn / không tính', J(
        '-  Chứng từ chưa hạch toán (chưa duyệt / chưa ghi sổ).',
        '-  Bút toán ngày hạch toán SAU Đến ngày.',
        '-  Bút toán không gắn khách hàng: không lên dòng nào, nhưng VẪN tính vào Số dư đầu kỳ của dòng Tổng cộng.',
        '-  Số liệu ngoài phạm vi quyền (mục 7).',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', J(
        'Ô Thời gian (bắt buộc, mặc định trống) lọc theo NGÀY HẠCH TOÁN: trước Từ ngày -> Số dư đầu kỳ; Từ ngày -> hết Đến ngày -> phát sinh.',
        'Thiếu Thời gian: "Vui lòng chọn thời gian". Từ > Đến: "Đến ngày phải lớn hơn hoặc bằng Từ ngày." — bảng rỗng, không xuất Excel.',
        'Rời màn rồi quay lại, tải lại trang (F5) hoặc bấm Làm mới thì bộ lọc về trống.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', J(
        'Tổng cộng -> Khách hàng (STT 1, 2…) -> Hợp đồng (STT 1.1, 1.2…). Phân trang theo dòng hợp đồng (10/20/50/100, mặc định 10); '
        'chân bảng "Hiển thị a–b / N dòng hợp đồng". STT khách nối tiếp sang trang sau.',
        'Phòng ban / Bộ phận / NVKD = của người tạo hợp đồng theo hồ sơ hiện tại. Bảng không có sắp xếp cột, không có tùy chỉnh cột, không có nút In.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', J(
        '-  Dòng khách hàng = tổng các dòng hợp đồng của khách (kể cả ở trang khác).',
        '-  Dòng Tổng cộng KHÔNG áp ô tìm nhanh và lọc Số dư cuối kỳ (Dư nợ / Dư có) => khi dùng 2 ô này Tổng cộng có thể khác tổng các dòng — đúng thiết kế.',
        '-  Số dư đầu kỳ dòng Tổng cộng: khi lọc Số hợp đồng lấy mọi hợp đồng có số CHỨA chuỗi; các cột khác lấy ĐÚNG số hợp đồng.',
        '-  Popup: mỗi chứng từ 1 dòng; tổng popup tính mọi trang.',
    )),
    ('7. Phân quyền cấp', J(
        'Ai cũng mở được màn. 4 quyền (nhóm "Báo cáo chi tiết công nợ khách hàng") chỉ quyết phạm vi:',
        '-  Tổng công ty: toàn bộ; có ô Công ty, Phòng ban, Bộ phận, Nhân viên.',
        '-  Công ty: công ty đang làm việc + hợp đồng mình tạo; có ô Phòng ban, Bộ phận, Nhân viên.',
        '-  Phòng ban: các phòng mình quản lý + hợp đồng mình tạo. Bộ phận: các bộ phận mình quản lý + hợp đồng mình tạo (ô Bộ phận, Nhân viên).',
        '-  Không quyền: chỉ hợp đồng mình tạo; không có ô Công ty / Phòng ban / Bộ phận / Nhân viên.',
        'Phạm vi áp cho cả dòng Tổng cộng (kể cả Số dư đầu kỳ), popup, Excel.',
    )),
    ('8. Cách tính các ô thống kê', J(
        'Hàng hóa/Dịch vụ = Nợ - Có (Có không tính khai báo công nợ đầu kỳ). Nhập trả lại = Có - Nợ. ĐCCN tăng = Nợ, ĐCCN giảm = Có của phiếu kế toán.',
        'Cộng tăng = HH/DV + ĐCCN tăng. Cộng giảm = Nhập trả lại + Đã thanh toán + ĐCCN giảm.',
        'Số dư cuối kỳ = Đầu kỳ + Cộng tăng - Cộng giảm + Trả lại tiền thừa.',
        'Định dạng 1,234,567, không lẻ. Số 0 để trống, trừ dòng Tổng cộng, cột Số dư cuối kỳ, cột ĐCCN giảm ở dòng hợp đồng (in 0).',
    )),
    ('9. Ghi chú đọc bảng', J(
        DU_LIEU,
        'Bẫy dễ sai:',
        '-  Ô chọn lọc ngay; ô tìm nhanh và Số hợp đồng chỉ lọc khi nhấn Enter / Tìm kiếm. Số hợp đồng phải nhập ĐỦ.',
        '-  Popup ĐCCN tăng có thêm khai báo đầu kỳ công nợ NCC và phiếu thu ghi Nợ; popup ĐCCN giảm có thêm phiếu thu ghi Có (giữ như hệ thống cũ).',
        '-  Popup không áp ô tìm nhanh / Số dư cuối kỳ.',
    )),
]

# ================================================================== I. HIỂN THỊ TRANG & TRUY CẬP
G1 = [
    C('Mở màn hình từ menu: bộ lọc trống, bảng chờ chọn thời gian', 'P0', 'Tài khoản TK-ALL đã đăng nhập.', ['1. ' + MENU], '',
      ['Tiêu đề "Báo cáo chi tiết công nợ khách hàng", có icon (i) cạnh tiêu đề',
       'Bảng: "' + LN + '"; không tự tải số liệu']),
    C('Bố cục khu vực lọc và các nút chức năng', 'P1', 'Tài khoản TK-ALL.', ['1. Mở màn', '2. Quan sát khu vực lọc và hàng nút trên bảng'], '',
      ['Ô tìm nhanh gợi ý "Tìm theo số hợp đồng, mã hoặc tên khách hàng"; nút Tìm kiếm, Làm mới, Cài đặt bộ lọc, Ẩn tìm kiếm nâng cao',
       'Ô Thời gian có dấu * đỏ; ô Khách hàng, Số hợp đồng, Số dư cuối kỳ; Công ty, Phòng ban, Bộ phận, Nhân viên',
       'Trên bảng có nút Xuất Excel; không có nút In, Thêm, Sửa, Xóa']),
    C('Kiểm tra đủ các cột của bảng (tiêu đề 2 tầng)', 'P0', 'Đã chọn Thời gian.', ['1. Quan sát hàng tiêu đề, cuộn ngang hết bảng'], '',
      ['Tầng 1: STT, Đơn hàng/hợp đồng, Phòng ban, Bộ phận, NVKD, Số dư đầu kỳ, "Phát sinh tăng trong kỳ" (3 cột), '
       '"Phát sinh giảm trong kỳ" (4 cột), Trả lại tiền thừa, Số dư cuối kỳ',
       'Tầng 2: Hàng hóa/Dịch vụ, Điều chỉnh công nợ, Cộng | Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ, Cộng',
       'Mỗi tiêu đề cột có icon (i); có thanh cuộn ngang trên và dưới bảng',
       'Bảng không có cột ẩn / cột tùy chọn, không có nút cấu hình cột']),
    C('Icon (i) đầu cột hiện đúng chú thích', 'P2', 'Đã chọn Thời gian.', ['1. Rê chuột vào icon (i) của cột Số dư cuối kỳ', '2. Rê vào icon (i) cạnh chữ Tổng cộng'], '',
      ['Bước 1: "Công nợ phải thu còn lại tại "Đến ngày"." kèm "Số dư cuối kỳ = Số dư đầu kỳ + Cộng phát sinh tăng - Cộng phát sinh giảm + Trả lại tiền thừa."',
       'Bước 2: "Tổng trên toàn bộ công nợ theo bộ lọc. Lọc "Số dư cuối kỳ" (Dư nợ / Dư có) và ô tìm nhanh chỉ áp cho các dòng khách hàng, không áp cho dòng tổng…"']),
    C('Tiêu đề bảng dính khi cuộn dọc', 'P2', 'Kết quả hơn 20 dòng, chọn 50 dòng/trang.', ['1. Cuộn bảng xuống cuối'], '',
      ['Hàng tiêu đề 2 tầng vẫn hiện trên cùng vùng bảng']),
    C('Phân biệt 3 loại dòng: Tổng cộng, khách hàng, hợp đồng', 'P1', TT, ['1. Quan sát 3 loại dòng'], 'Khách hàng 89THUPTR-62',
      ['Dòng 1: "Tổng cộng" nền xám đậm', 'Dòng 2: "1 | 89THUPTR-62 - CÔNG TY TNHH ĐẦU TƯ THƯƠNG MẠI THIÊN TRƯỜNG" chữ đậm, tên gộp qua 4 cột',
       '3 dòng 1.1, 1.2, 1.3 chữ thường; số hợp đồng gạch chân, bấm được']),
    C('Hiển thị khi không có dữ liệu khớp', 'P1', 'Đã chọn Thời gian.', ['1. Tìm nhanh "ZZZ-KHONG-CO", nhấn Enter'], 'Từ khóa: ZZZ-KHONG-CO',
      ['Bảng "Không có dữ liệu phù hợp bộ lọc."', 'Không hiện dòng Tổng cộng, không có chân phân trang']),
    C('Khách hàng chưa có phát sinh nào', 'P2', 'KH-MOI vừa tạo, chưa có chứng từ công nợ nào.',
      ['1. Chọn Thời gian 01/10/2026 - 31/10/2026, Khách hàng KH-MOI'], 'Khách hàng: KH-MOI',
      ['Bảng "Không có dữ liệu phù hợp bộ lọc."', 'Màn không báo lỗi; nút Xuất Excel vẫn bấm được']),
    C('Thứ tự mặc định của dòng khách hàng và dòng hợp đồng', 'P1', NHIEU,
      ['1. Đăng nhập TK-ALL, chọn Thời gian 01/10/2026 - 31/10/2026', '2. Đọc thứ tự dòng khách hàng', '3. Đọc thứ tự dòng hợp đồng của 1 khách'], '',
      ['Dòng khách hàng xếp theo thứ tự khách hàng được tạo trong hệ thống, không đổi khi mở lại',
       'Dòng hợp đồng của 1 khách xếp theo thứ tự hợp đồng được tạo (tạo trước đứng trước)']),
    C('Số thứ tự liên tục qua các trang', 'P0', NHIEU,
      ['1. Đăng nhập TK-ALL, chọn Thời gian 01/10/2026 - 31/10/2026', '2. Ghi STT dòng khách hàng cuối trang 1', '3. Sang trang 2'], '',
      ['STT khách hàng ở trang 2 nối tiếp trang 1 (không quay về 1)', 'Khách có hợp đồng vắt sang trang 2 hiện lại dòng khách hàng ở đầu trang 2 với cùng STT',
       'Dòng Tổng cộng không đổi']),
    C('Dữ liệu trên bảng đúng với chứng từ đã tạo', 'P0', TT,
      ['1. Lọc như Tiền điều kiện', '2. Bấm số 453,829,501 ở cột Điều chỉnh công nợ (tăng) dòng 1.1, bấm mã phiếu TPE.PKT1026.00436 mở phiếu', '3. So số tiền, người tạo'], '',
      ['Phiếu kế toán ghi đúng 453,829,501 cho hợp đồng của dòng 1.1', 'Cột Phòng ban / Bộ phận / NVKD của dòng là của người tạo hợp đồng']),
] + PT + [
    C('Thời gian tải khi chỉ chọn Thời gian 1 tháng', 'P1', 'Tài khoản TK-ALL.',
      ['1. Chọn 01/10/2026 - 31/10/2026, đo đến khi bảng có dòng'], '',
      ['Bảng hiện trong 10 giây (môi trường thử 02/11/2026: khoảng 4,5 giây, 25,309 dòng hợp đồng)']),
    C('Thời gian tải kỳ dài', 'P2', 'Tài khoản TK-ALL.', ['1. Chọn 01/01/2026 - 31/10/2026'], '',
      ['Bảng hiện trong 10 giây (môi trường thử: khoảng 4,4 giây)']),
    C('Chuyển trang nhanh hơn lần tải đầu', 'P2', 'Đang xem kết quả 1 tháng.', ['1. Sang trang 2, đo thời gian'], '',
      ['Nhanh hơn lần tải đầu (không tính lại dòng Tổng cộng); dòng Tổng cộng không đổi']),
]

# ================================================================== II. TÌM KIẾM & LỌC DANH SÁCH
G2 = [
    C('Mặc định mọi ô lọc trống', 'P1', 'Lần đầu mở màn trong phiên làm việc.', ['1. Mở màn', '2. Quan sát khu vực lọc'], '',
      ['Thời gian, Khách hàng, Số hợp đồng, Số dư cuối kỳ, ô tìm nhanh và các ô tổ chức đều trống']),
    C('Bắt buộc Thời gian khi bấm Tìm kiếm', 'P0', 'Mở màn, Thời gian trống.', ['1. Bấm Tìm kiếm'], '',
      ['Dưới ô Thời gian chữ đỏ "Vui lòng chọn thời gian"', 'Bảng vẫn "' + LN + '"']),
    C('Chọn Thời gian thì báo cáo tự tải', 'P0', 'Tài khoản TK-ALL, mở màn.', ['1. Chọn 01/10/2026 - 31/10/2026, không bấm Tìm kiếm'], 'Thời gian: 01/10/2026 - 31/10/2026',
      ['Dòng "Đang tải dữ liệu..." rồi hiện báo cáo', 'Môi trường thử: Tổng cộng Số dư đầu kỳ 898,996,927,176; Số dư cuối kỳ 955,376,161,388']),
    C('Ngày ngược chiều', 'P0', 'Đang mở màn.',
      ['1. Gõ Từ ngày 31/10/2026, Đến ngày 01/10/2026 (lịch không cho chọn ngược thì gõ tay)'], '',
      ['Dưới ô Thời gian chữ đỏ "Đến ngày phải lớn hơn hoặc bằng Từ ngày."', 'Thông báo nổi cùng câu',
       'Bảng rỗng, không còn số của khoảng cũ', 'Bấm Xuất Excel: thông báo cùng câu, không mở cửa sổ']),
    C('Từ ngày bằng Đến ngày', 'P2', 'Đang mở màn.', ['1. Chọn 15/10/2026 - 15/10/2026'], '',
      ['Tải bình thường; phát sinh chỉ gồm chứng từ hạch toán ngày 15/10/2026']),
    C('Lọc Khách hàng', 'P0', 'Đang mở màn.', ['1. Chọn Thời gian tháng 10/2026', '2. Ô Khách hàng gõ "89THUPTR-62", chọn'], 'Khách hàng: 89THUPTR-62',
      ['Gõ 1 ký tự chưa gợi ý; từ 2 ký tự mới gợi ý', 'Môi trường thử: còn 1 khách, 3 dòng hợp đồng, chân "Hiển thị 1–3 / 3 dòng hợp đồng"',
       'Dòng Tổng cộng = dòng khách hàng (848,527,621 … 943,656,841)']),
    C('Lọc Số hợp đồng khớp chính xác', 'P1', 'Lọc khách hàng 89THUPTR-62, tháng 10/2026.',
      ['1. Ô Số hợp đồng nhập "HĐ_TPE_HN_KD2_26_1141_TT - TP", nhấn Enter', '2. Đổi thành "HĐ_TPE_HN_KD2_26_1141", nhấn Enter'], '',
      ['Bước 1: còn đúng dòng 1.1 HĐ_TPE_HN_KD2_26_1141_TT - TP, Số dư cuối kỳ 938,818,441',
       'Bước 2 (thiếu đuôi): "Không có dữ liệu phù hợp bộ lọc."', 'Gõ xong chưa nhấn Enter: bảng chưa đổi']),
    C('Lọc Số dư cuối kỳ Dư nợ / Dư có / Tất cả', 'P0', TT,
      ['1. Chọn Dư nợ', '2. Chọn Dư có', '3. Chọn Tất cả'], '',
      ['Dư nợ: còn 2 dòng (1.2 = 938,818,441 và 1.3 = 4,838,400); dòng 1.1 (cuối kỳ 0) bị loại',
       'Dư có: "Không có dữ liệu phù hợp bộ lọc." (khách này không có hợp đồng âm)',
       'Tất cả: 3 dòng như ban đầu', 'Dòng Tổng cộng KHÔNG đổi giữa 3 lựa chọn (thiết kế)']),
    C('Tìm nhanh theo số hợp đồng / mã / tên khách', 'P1', 'Thời gian tháng 10/2026.',
      ['1. Gõ "1141", nhấn Enter (lọc thêm khách hàng 89THUPTR-62)', '2. Gõ "THIÊN TRƯỜNG", nhấn Enter', '3. Gõ "89thuptr-62" chữ thường, nhấn Enter'], '',
      ['Bước 1: còn dòng HĐ_TPE_HN_KD2_26_1141_TT - TP; dòng khách hàng Hàng hóa/Dịch vụ 1,380,623,222',
       'Dòng Tổng cộng vẫn 1,595,658,222 (ô tìm nhanh không áp cho Tổng cộng)',
       'Bước 2, 3: ra các hợp đồng của khách THIÊN TRƯỜNG, không phân biệt hoa thường']),
    C('Tìm nhanh khớp chính xác số hợp đồng', 'P1', TT,
      ['1. Gõ đủ "HĐ_TPE_HN_KD2_26_1303_26.9" vào ô tìm nhanh, nhấn Enter'], 'Từ khóa: HĐ_TPE_HN_KD2_26_1303_26.9',
      ['Còn đúng dòng HĐ_TPE_HN_KD2_26_1303_26.9, Số dư cuối kỳ 4,838,400', 'Chân bảng "Hiển thị 1–1 / 1 dòng hợp đồng"']),
] + tk_chung(M) + [
    C('Lọc Công ty / Phòng ban / Bộ phận chọn nhiều', 'P1', 'Tài khoản TK-ALL, Thời gian tháng 10/2026.',
      ['1. Chọn 2 công ty', '2. Thêm 1 phòng ban', '3. Bấm icon khóa cạnh nhãn "Phòng ban"'], '',
      ['Bảng chỉ còn chứng từ của 2 công ty, rồi của phòng đã chọn (cột Phòng ban khớp)',
       'Bước 3: danh sách có thêm phòng ban đã khóa, gợi ý "Đang hiện cả phòng ban đã khoá — bấm để ẩn đi"']),
    C('Lọc Nhân viên theo người tạo hợp đồng', 'P1', 'Tài khoản TK-ALL; HD-TEST-01 do TK-NV tạo.',
      ['1. Chọn Thời gian tháng này', '2. Chọn Nhân viên = TK-NV'], '', ['Mọi dòng có NVKD = TK-NV', 'Có HD-TEST-01']),
    C('Kết hợp nhiều ô lọc', 'P1', 'Tài khoản TK-ALL.',
      ['1. Thời gian tháng 10/2026 + Khách hàng 89THUPTR-62 + Số dư cuối kỳ Dư nợ + tìm nhanh "1303", nhấn Enter'], '',
      ['Còn đúng dòng HĐ_TPE_HN_KD2_26_1303_26.9, Số dư cuối kỳ 4,838,400']),
    C('Tổng số và phân trang sau khi lọc', 'P1', NHIEU,
      ['1. Đăng nhập TK-ALL, chọn Thời gian 01/10/2026 - 31/10/2026, ghi N ở chân bảng', '2. Chọn Số dư cuối kỳ = "Dư có"', '3. Đọc chân bảng, chuyển trang'], '',
      ['Chân bảng hiện "Hiển thị 1–… / M dòng hợp đồng" với M nhỏ hơn N, bằng số dòng hợp đồng dư có',
       'Số trang tính lại theo M; chuyển trang chỉ trong tập đã lọc']),
    C('Làm mới xóa hết, kể cả Thời gian', 'P1', 'Đang lọc nhiều ô.', ['1. Bấm Làm mới'], '',
      ['Mọi ô trống (kể cả Thời gian, ô tìm nhanh)', 'Bảng "' + LN + '"']),
    C('Đổi bộ lọc liên tiếp chỉ hiện kết quả lần cuối', 'P2', 'Tài khoản TK-ALL.',
      ['1. Chọn Thời gian cả năm 2026', '2. Ngay lập tức đổi Khách hàng = 89THUPTR-62'], '',
      ['Bảng cuối cùng chỉ có khách 89THUPTR-62, không bị số của lần lọc trước đè lên']),
    C('Ẩn / hiện khu vực tìm kiếm nâng cao', 'P2', 'Đang mở màn.', ['1. Bấm "Ẩn tìm kiếm nâng cao"', '2. Bấm "Tìm kiếm nâng cao"'], '',
      ['Bước 1: các ô lọc thu gọn, còn ô tìm nhanh và nút; nút đổi chữ thành "Tìm kiếm nâng cao"', 'Bước 2: các ô lọc hiện lại']),
    C('Cài đặt bộ lọc', 'P2', 'Đang mở màn.', ['1. Bấm Cài đặt bộ lọc', '2. Bỏ tích "Số hợp đồng", bấm Lưu'], '',
      ['Cửa sổ liệt kê: Thời gian, Khách hàng, Số hợp đồng, Số dư cuối kỳ, Công ty / Phòng ban / Bộ phận / Nhân viên; nút Lưu, Khôi phục mặc định, Đóng',
       'Sau Lưu: ô Số hợp đồng ẩn khỏi bộ lọc']),
] + luu_chung(M)

# ================================================================== III. SỐ LIỆU BÁO CÁO
G3 = [
    C('Định dạng số và số 0', 'P1', TT, ['1. Quan sát các ô số'], '',
      ['Dạng 1,234,567, không có số lẻ', 'Dòng Tổng cộng: Đã thanh toán "0", Trả lại tiền thừa "0"',
       'Dòng khách hàng: Đã thanh toán, Trả lại tiền thừa để trống', 'Dòng 1.1: Số dư cuối kỳ "0"; dòng 1.1 và 1.3: ĐCCN giảm "0" (gạch chân)']),
    C('Cộng phát sinh tăng / giảm từng dòng', 'P0', TT,
      ['1. Dòng 1.1: cộng Hàng hóa/Dịch vụ + ĐCCN tăng', '2. Cộng Nhập trả lại + Đã thanh toán + ĐCCN giảm'], '',
      ['Bước 1: 215,035,000 + 453,829,501 = 668,864,501 = cột Cộng (tăng)', 'Bước 2: 1,500,529,002 + 0 + 0 = 1,500,529,002 = cột Cộng (giảm)']),
    C('Số dư cuối kỳ từng dòng', 'P0', TT, ['1. Tính tay cho dòng 1.1, 1.2, 1.3'], '',
      ['1.1: 831,664,501 + 668,864,501 - 1,500,529,002 = 0', '1.2: 12,024,720 + 1,380,623,222 - 453,829,501 = 938,818,441',
       '1.3: 4,838,400 = 4,838,400']),
    C('Dòng khách hàng = tổng các hợp đồng', 'P0', TT, ['1. Cộng từng cột của 1.1, 1.2, 1.3'], '',
      ['Số dư đầu kỳ: 831,664,501 + 12,024,720 + 4,838,400 = 848,527,621', 'Hàng hóa/Dịch vụ: 215,035,000 + 1,380,623,222 = 1,595,658,222',
       'Số dư cuối kỳ: 0 + 938,818,441 + 4,838,400 = 943,656,841']),
    C('Dòng khách hàng tính đủ khi hợp đồng vắt sang trang sau', 'P0', 'Khách có hơn 10 hợp đồng, 10 dòng/trang, hợp đồng của khách nằm ở cả trang 1 và 2.',
      ['1. Ghi số dòng khách hàng ở trang 1', '2. Sang trang 2', '3. Đổi 100 dòng/trang, cộng tay các hợp đồng của khách'], '',
      ['Dòng khách hàng ở trang 1 và trang 2 cùng một số', 'Bằng tổng mọi hợp đồng của khách (bước 3)']),
    C('Dòng Tổng cộng = tổng các dòng khi không lọc Dư nợ / tìm nhanh', 'P1', 'Lọc 1 khách có từ 2 hợp đồng.',
      ['1. So dòng Tổng cộng với dòng khách hàng'], '', ['Mọi cột bằng nhau (khách không có chứng từ chưa gắn khách hàng)']),
    C('Dòng Tổng cộng không áp Dư nợ / tìm nhanh (thiết kế)', 'P1', TT,
      ['1. Chọn Số dư cuối kỳ = Dư nợ', '2. So dòng Tổng cộng với dòng khách hàng'], '',
      ['Dòng khách hàng: Hàng hóa/Dịch vụ 1,380,623,222', 'Dòng Tổng cộng vẫn 1,595,658,222', 'Đúng thiết kế — ghi nhận, không ghi Failed']),
    C('Chuyển trang và đổi số dòng không đổi dòng Tổng cộng', 'P1', NHIEU,
      ['1. Đăng nhập TK-ALL, chọn Thời gian 01/10/2026 - 31/10/2026, ghi dòng Tổng cộng', '2. Sang trang cuối', '3. Đổi 50 dòng/trang'], '',
      ['Dòng Tổng cộng giữ nguyên mọi cột ở cả 3 bước']),
    C('Hợp đồng không phát sinh trong kỳ vẫn hiện', 'P2', 'HD-TEST-02 chỉ có chứng từ tháng trước.',
      ['1. ' + LOC], '',
      ['Có dòng HD-TEST-02: Số dư đầu kỳ = số dư tháng trước, các cột phát sinh trống, Số dư cuối kỳ = Số dư đầu kỳ']),
    C('Đổi Từ ngày chuyển số giữa đầu kỳ và phát sinh', 'P1', 'Biết số liệu khách 89THUPTR-62.',
      ['1. Lọc 01/10/2026 - 31/10/2026', '2. Lọc 01/01/2026 - 31/10/2026'], '',
      ['Số dư cuối kỳ của dòng khách hàng KHÔNG đổi giữa 2 lần (cùng Đến ngày)', 'Số dư đầu kỳ và các cột phát sinh thay đổi tương ứng']),
    C('Phòng ban / Bộ phận / NVKD lấy theo người tạo hợp đồng hiện tại', 'P2', 'Nhân viên tạo HD-TEST-01 vừa chuyển sang PB-2.',
      ['1. ' + LOC + ', xem dòng HD-TEST-01'], '', ['Cột Phòng ban hiện mã PB-2 (phòng mới), NVKD = TK-NV']),
    C('Số dư âm (dư có)', 'P1', 'Có hợp đồng khách trả thừa.', ['1. Chọn Thời gian tháng này', '2. Lọc Dư có'], '',
      ['Số dư cuối kỳ âm, dạng -1,234,567', 'Mọi dòng hiện đều có Số dư cuối kỳ nhỏ hơn 0']),
    C('Chứng từ không gắn hợp đồng', 'P2', 'Khách có phiếu báo có không chọn hợp đồng.', ['1. Lọc khách đó'], '',
      ['Có 1 dòng ô Đơn hàng/hợp đồng trống, Phòng ban / Bộ phận / NVKD trống', 'Bấm số ở dòng đó: popup tiêu đề phụ "… — Không gắn hợp đồng"']),
    C('Số dư đầu kỳ Tổng cộng tính cả chứng từ chưa gắn khách hàng', 'P2', 'Có bút toán phải thu không gắn khách hàng trước Từ ngày.',
      ['1. Lọc không chọn khách, so Số dư đầu kỳ Tổng cộng với tổng các dòng khách hàng (xuất Excel để cộng)'], '',
      ['Tổng cộng lệch đúng bằng số của bút toán không gắn khách hàng — đúng thiết kế']),
    # --- lập chứng từ rồi kiểm số tăng / giảm
    C('Ghi số nền trước khi lập chứng từ', 'P0', 'KH-TEST, HD-TEST-01 có sẵn (xem mục 9).',
      ['1. Mở báo cáo, lọc: ' + LOC, '2. Ghi lại mọi cột của ' + XEM], 'KH-TEST, HD-TEST-01',
      ['Có đủ số nền (khách mới thì trống, Số dư cuối kỳ 0) để so ở các case sau']),
    C('Phiếu xuất hàng tăng Hàng hóa/Dịch vụ', 'P0', NEN + ' Phiếu xuất kho cho HD-TEST-01 đã có sẵn (lập ở hệ thống cũ).',
      ['1. Vào ' + MN['pxh'] + ', lập phiếu xuất hàng cho HD-TEST-01 giá trị 10,000,000, hạch toán hôm nay', '2. Lọc lại báo cáo'], 'Số tiền: 10,000,000',
      ['Hàng hóa/Dịch vụ +10,000,000; Cộng (tăng) +10,000,000; Số dư cuối kỳ +10,000,000 ở ' + XEM,
       'Bấm số Hàng hóa/Dịch vụ dòng HD-TEST-01: popup có phiếu vừa lập, Phát sinh nợ 10,000,000']),
    C('Phiếu thu tăng Đã thanh toán', 'P0', NEN,
      ['1. Vào ' + MN['pt'] + ', lập phiếu thu KH-TEST, hợp đồng HD-TEST-01, 4,000,000, duyệt và hạch toán hôm nay', '2. Lọc lại'], 'Số tiền: 4,000,000',
      ['Đã thanh toán +4,000,000; Cộng (giảm) +4,000,000; Số dư cuối kỳ -4,000,000', 'Popup Đã thanh toán có mã phiếu thu vừa lập, bấm mã mở đúng phiếu']),
    C('Phiếu báo có tăng Đã thanh toán', 'P1', NEN,
      ['1. Vào ' + MN['pbc'] + ', lập phiếu báo có KH-TEST cho HD-TEST-01, 1,000,000, hạch toán hôm nay', '2. Lọc lại'], 'Số tiền: 1,000,000',
      ['Đã thanh toán +1,000,000; Số dư cuối kỳ -1,000,000']),
    C('Điều chỉnh công nợ TĂNG', 'P0', NEN,
      ['1. Vào ' + MN['ycdc'] + ', lập yêu cầu điều chỉnh TĂNG KH-TEST, HD-TEST-01, 2,000,000; duyệt', '2. Vào ' + MN['pkt'] + ', lập phiếu kế toán từ yêu cầu, hạch toán hôm nay', '3. Lọc lại'], 'Số tiền: 2,000,000',
      ['Điều chỉnh công nợ (nhóm tăng) +2,000,000; Cộng (tăng) +2,000,000; Số dư cuối kỳ +2,000,000']),
    C('Điều chỉnh công nợ GIẢM', 'P0', NEN,
      ['1. Làm như case Điều chỉnh công nợ TĂNG nhưng điều chỉnh GIẢM 500,000', '2. Lọc lại'], 'Số tiền: 500,000',
      ['Điều chỉnh công nợ (nhóm giảm) +500,000; Cộng (giảm) +500,000; Số dư cuối kỳ -500,000']),
    C('Khách trả lại hàng tăng Nhập trả lại', 'P0', 'HD-TEST-01 đã xuất hàng (case Phiếu xuất hàng). ' + NEN,
      ['1. Vào ' + MN['pnh'] + ', lập phiếu nhập hàng trả lại theo HD-TEST-01, 3,000,000, hạch toán hôm nay', '2. Lọc lại'], 'Số tiền: 3,000,000',
      ['Nhập trả lại +3,000,000; Số dư cuối kỳ -3,000,000', 'Popup Nhập trả lại: 2 cột Phát sinh nợ / có, phiếu vừa lập ở cột Phát sinh có']),
    C('Phiếu chi tăng Trả lại tiền thừa và TĂNG số dư', 'P0', NEN,
      ['1. Vào ' + MN['pc'] + ', lập phiếu chi trả KH-TEST cho HD-TEST-01, 200,000, hạch toán hôm nay', '2. Lọc lại'], 'Số tiền: 200,000',
      ['Trả lại tiền thừa +200,000; Số dư cuối kỳ TĂNG 200,000; nhóm Phát sinh giảm không đổi']),
    C('Phiếu ủy nhiệm chi tăng Trả lại tiền thừa', 'P1', NEN,
      ['1. Vào ' + MN['unc'] + ', lập ủy nhiệm chi trả KH-TEST cho HD-TEST-01, 300,000, hạch toán hôm nay', '2. Lọc lại'], 'Số tiền: 300,000',
      ['Trả lại tiền thừa +300,000 (lũy kế 500,000); Số dư cuối kỳ +300,000']),
    C('Thu vượt chuyển sang Dư có', 'P1', 'HD-TEST-01 đang dư nợ 4,000,000 (số nền 0).',
      ['1. Lập phiếu thu 5,000,000 cho HD-TEST-01, hạch toán hôm nay', '2. Lọc Tất cả / Dư nợ / Dư có'], 'Số tiền: 5,000,000',
      ['Số dư cuối kỳ HD-TEST-01 = -1,000,000', 'Dư nợ: không có HD-TEST-01; Dư có: có HD-TEST-01', 'Dòng Tổng cộng không đổi giữa 3 lựa chọn']),
    C('Ngày hạch toán quyết định kỳ', 'P1', 'Phiếu thu 700,000 cho HD-TEST-01, ngày hạch toán là ngày cuối tháng trước.',
      ['1. Lọc ngày 1 tháng này - hôm nay', '2. Lọc ngày 1 tháng trước - hôm nay'], 'Số tiền: 700,000',
      ['Bước 1: phiếu nằm trong Số dư đầu kỳ (giảm 700,000), không ở cột Đã thanh toán',
       'Bước 2: phiếu ở cột Đã thanh toán; Số dư cuối kỳ hai lần bằng nhau']),
    C('Khai báo đầu kỳ công nợ', 'P2', 'Có quyền "Quản lý công nợ đầu kỳ".',
      ['1. Vào ' + MN['dk'] + ', khai báo công nợ đầu kỳ KH-TEST, HD-TEST-02, 1,500,000 ghi Nợ, ngày trước Từ ngày', '2. Lọc lại'], 'Số tiền: 1,500,000',
      ['Dòng HD-TEST-02: Số dư đầu kỳ +1,500,000; Số dư cuối kỳ +1,500,000',
       'Lọc kỳ chứa ngày khai báo: cột Hàng hóa/Dịch vụ +1,500,000']),
]

# ================================================================== IV. XEM CHI TIẾT CHỨNG TỪ (popup)
G4 = [
    C('Mở popup Hàng hóa/Dịch vụ dòng hợp đồng (2 cột)', 'P0', TT,
      ['1. Bấm 215,035,000 ở dòng HĐ_TPE_HN_KD2_26_1094_TP-TT'], '',
      ['Tiêu đề "Chi tiết chứng từ", dòng phụ "Phát sinh tăng - Hàng hóa/Dịch vụ — HĐ_TPE_HN_KD2_26_1094_TP-TT"',
       'Cột: STT, Mã phiếu, Phát sinh nợ, Phát sinh có, Ngày tạo, Người tạo',
       '4 phiếu PXH-41186 (115,027,000), PXH-41935, PXH-42762, PXH-42763; "Hiển thị 1–4 / 4"',
       'Chân: "Tổng phát sinh nợ: 215,035,000 · Tổng phát sinh có:" — Nợ - Có = số đã bấm']),
    C('Popup dòng khách hàng gồm mọi hợp đồng', 'P0', TT,
      ['1. Bấm 1,595,658,222 ở dòng khách hàng'], '',
      ['Dòng phụ "… — 89THUPTR-62 - CÔNG TY TNHH ĐẦU TƯ THƯƠNG MẠI THIÊN TRƯỜNG"', '10 phiếu PXH',
       'Chân "Tổng phát sinh nợ: 1,745,711,122 · Tổng phát sinh có: 150,052,900"; 1,745,711,122 - 150,052,900 = 1,595,658,222']),
    C('Popup 1 cột Số tiền (Điều chỉnh công nợ)', 'P1', TT,
      ['1. Bấm 453,829,501 ở cột Điều chỉnh công nợ (tăng) dòng 1.1'], '',
      ['Cột: STT, Mã phiếu, Số tiền, Ngày tạo, Người tạo', '1 phiếu TPE.PKT1026.00436, 453,829,501, 20/10/2026 08:37', 'Chân "Tổng số tiền: 453,829,501"']),
    C('Popup Nhập trả lại', 'P1', TT,
      ['1. Bấm 1,500,529,002 ở cột Nhập trả lại dòng 1.1'], '',
      ['10 phiếu PNH, số ở cột Phát sinh có', 'Chân "Tổng phát sinh có: 1,500,529,002"']),
    C('Chứng từ trong popup khớp chứng từ đã tạo', 'P0', TT,
      ['1. Mở popup Hàng hóa/Dịch vụ dòng HĐ_TPE_HN_KD2_26_1094_TP-TT', '2. Bấm mã PXH-41186 mở phiếu', '3. So số tiền, ngày tạo, người tạo'], '',
      ['Số tiền, ngày tạo, người tạo trong popup đúng như trên phiếu xuất hàng PXH-41186']),
    C('Số 0 không bấm được, trừ ĐCCN giảm dòng hợp đồng', 'P2', TT,
      ['1. Rê chuột vào ô trống cột Đã thanh toán', '2. Bấm "0" cột ĐCCN giảm dòng 1.3'], '',
      ['Bước 1: không phải liên kết', 'Bước 2: mở popup, "Không có dữ liệu phù hợp."']),
    C('Popup chỉ để xem, không có nút Lưu', 'P1', 'Đang mở popup Chi tiết chứng từ.',
      ['1. Bấm thử vào các ô trong popup', '2. Quan sát chân popup'], '',
      ['Không ô nào cho sửa', 'Chân popup chỉ có dòng tổng và nút Đóng; không có nút Lưu']),
    C('Bấm Mã phiếu mở chứng từ ở tab mới', 'P1', 'Popup đang mở.', ['1. Bấm mã PXH-41186'], '',
      ['Mở Phiếu xuất hàng PXH-41186 ở tab mới; popup và báo cáo giữ nguyên']),
    C('Phân trang popup và đóng', 'P2', 'Popup có hơn 10 chứng từ.',
      ['1. Chọn 5 dòng/trang, sang trang 2', '2. Bấm Đóng', '3. Mở lại popup'], '',
      ['Tổng ở chân không đổi khi chuyển trang', 'Đóng: về báo cáo, giữ bộ lọc và trang', 'Mở lại: về trang 1, 10 dòng/trang']),
    C('Đóng popup bằng nút X góc trên', 'P2', 'Đang mở popup Chi tiết chứng từ, báo cáo đang ở trang 2.',
      ['1. Bấm nút X góc trên popup'], '', ['Popup đóng, báo cáo giữ nguyên trang 2 và bộ lọc']),
    C('Popup dòng khách hàng khi đang lọc Dư nợ', 'P1', TT + ' Số dư cuối kỳ = Dư nợ.',
      ['1. Bấm số Hàng hóa/Dịch vụ ở dòng khách hàng (1,380,623,222)'], '',
      ['Mong đợi: tổng popup (Nợ - Có) = 1,380,623,222 — số đã bấm',
       'Ghi chú: popup không áp lọc Số dư cuối kỳ nên hiện tại có thể ra 1,745,711,122 - 150,052,900 = 1,595,658,222 (gồm cả hợp đồng 1.1 đã bị lọc ra) — nếu vậy ghi Failed, đưa đội phát triển xem']),
    C('Popup ĐCCN tăng có thêm phiếu thu ghi Nợ (giữ như hệ thống cũ)', 'P2', 'Hợp đồng có phiếu thu ghi Nợ sổ phải thu trong kỳ.',
      ['1. Bấm số ĐCCN tăng của hợp đồng đó'], '',
      ['Popup có cả phiếu kế toán và phiếu thu; tổng popup lớn hơn số đã bấm đúng bằng số phiếu thu — ghi nhận, không ghi Failed']),
]

# ================================================================== V. XUẤT DANH SÁCH EXCEL
G5 = [
    C('Chưa chọn Thời gian thì không xuất', 'P1', 'Bộ lọc trống.', ['1. Bấm Xuất Excel'], '',
      ['Thông báo "Vui lòng chọn thời gian"; ô Thời gian chữ đỏ; không mở cửa sổ']),
    C('Mở cửa sổ chọn trường xuất Excel', 'P0', 'Đã chọn Thời gian.', ['1. Bấm Xuất Excel'], '',
      ['Tiêu đề "Chọn trường xuất Excel"; dòng "Tích chọn trường cần xuất, kéo biểu tượng ba gạch để đổi thứ tự cột trong file."',
       '14 trường tích sẵn: Khách hàng / Đơn hàng - hợp đồng, Phòng ban, Bộ phận, NVKD, Số dư đầu kỳ, PS tăng - Hàng hóa/Dịch vụ, PS tăng - Điều chỉnh công nợ, PS tăng - Cộng, PS giảm - Nhập trả lại, PS giảm - Đã thanh toán, PS giảm - Điều chỉnh công nợ, PS giảm - Cộng, Trả lại tiền thừa, Số dư cuối kỳ',
       '"Đang chọn 14/14 trường"; nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng']),
    C('File đúng bố cục và số liệu (trường mặc định)', 'P0', TT,
      ['1. Xuất Excel đủ 14 trường', '2. Mở file bao_cao_chi_tiet_cong_no_khach_hang.xlsx'], '',
      ['Sheet "Chi tiết công nợ KH"; dòng 1 "BÁO CÁO CHI TIẾT CÔNG NỢ KHÁCH HÀNG"; dòng 2 "Thời gian: 01/10/2026 - 31/10/2026" in đậm',
       'Tiêu đề 2 tầng "Phát sinh tăng trong kỳ" / "Phát sinh giảm trong kỳ"; cột STT đầu tiên',
       'Dòng Tổng cộng, dòng "1 | 89THUPTR-62 - …" (đậm), 3 dòng 1.1, 1.2, 1.3; số khớp màn (vd Số dư cuối kỳ 943,656,841)',
       'Ô số là kiểu số (cộng được trong Excel); thông báo "Xuất Excel thành công"']),
    C('Chọn một số trường và đổi thứ tự', 'P1', 'Đang mở cửa sổ chọn trường.',
      ['1. Bỏ chọn hết, tích Số dư cuối kỳ rồi Khách hàng / Đơn hàng - hợp đồng', '2. Xuất file'], '',
      ['File có 3 cột: STT, Số dư cuối kỳ, Khách hàng / Đơn hàng - hợp đồng (theo thứ tự tích)']),
    C('Xuất theo đúng bộ lọc đang áp dụng', 'P0', TT,
      ['1. Chọn Số dư cuối kỳ = Dư nợ', '2. Xuất Excel, mở file'], '',
      ['File chỉ có 2 dòng hợp đồng dư nợ (1.2, 1.3) như trên màn', 'Dòng Tổng cộng trong file bằng dòng Tổng cộng trên màn']),
    C('Số 0 trong file', 'P2', TT, ['1. Xuất file', '2. Xem ô Đã thanh toán dòng khách hàng và dòng Tổng cộng'], '',
      ['Dòng Tổng cộng hiện 0; dòng khách hàng ô trống; Số dư cuối kỳ dòng 1.1 hiện 0']),
] + xl_chung(M) + [
    C('Xuất Excel khi KHÔNG lọc khách hàng (dữ liệu lớn)', 'P1', 'TK-ALL, Thời gian 01/10/2026 - 31/10/2026, không lọc thêm (môi trường thử: 25,309 dòng hợp đồng).',
      ['1. Xuất Excel đủ 14 trường', '2. Đo thời gian đến khi tải xong file'], '',
      ['Tải được file đủ 25,309 dòng hợp đồng + dòng khách hàng, trong thời gian chấp nhận được (dưới 60 giây)',
       'Ghi chú: thử trên môi trường thử 02/11/2026 lấy dữ liệu xuất cả tháng bị lỗi máy chủ sau khoảng 7 giây — nếu gặp thông báo "Lỗi khi xuất Excel" hoặc lỗi máy chủ thì ghi Failed']),
]

# ================================================================== VI. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
G6 = [
    C('Chứng từ chưa hạch toán không làm đổi báo cáo', 'P0', NEN,
      ['1. Lập phiếu thu 1,000,000 cho HD-TEST-01, để chưa duyệt / chưa hạch toán', '2. Lọc lại'], '',
      ['Không cột nào thay đổi']),
    C('Kiểm tổng sau cả chuỗi chứng từ', 'P0', 'Đã làm lần lượt các case lập chứng từ (xuất hàng, thu, báo có, điều chỉnh tăng / giảm, trả lại hàng, phiếu chi, ủy nhiệm chi).',
      ['1. So Số dư cuối kỳ HD-TEST-01 với số nền'], '',
      ['Chênh: +10,000,000 - 4,000,000 - 1,000,000 + 2,000,000 - 500,000 - 3,000,000 + 200,000 + 300,000 = +4,000,000',
       'Dòng khách hàng KH-TEST và dòng Tổng cộng chênh đúng như vậy']),
    C('Hủy hạch toán thì số trả về', 'P1', 'Phiếu thu 4,000,000 cho HD-TEST-01 đã hạch toán và đang hiện trên báo cáo.',
      ['1. Kế toán hủy hạch toán (hoặc hủy) phiếu thu đó', '2. Lọc lại báo cáo', '3. Mở popup Đã thanh toán của HD-TEST-01'], '',
      ['Đã thanh toán giảm lại 4,000,000; Số dư cuối kỳ tăng lại 4,000,000', 'Popup không còn phiếu thu đó']),
    C('Bấm số hợp đồng mở hợp đồng ở tab mới', 'P1', 'Có dòng HD-TEST-01.',
      ['1. Bấm số HD-TEST-01'], '', ['Mở hợp đồng ở tab mới, tab báo cáo giữ nguyên bộ lọc', 'Dòng không gắn hợp đồng: ô trống, không bấm được']),
    C('Khớp số với Báo cáo tổng hợp công nợ theo nhân viên', 'P1', 'HD-TEST-01 có phát sinh trong kỳ; cùng một tài khoản xem.',
      ['1. Lọc cùng Thời gian, cùng KH-TEST ở màn này và màn Bán hàng > Báo cáo > Báo cáo công nợ > "Tổng hợp công nợ theo NV"', '2. So các cột của HD-TEST-01'], '',
      ['Số dư đầu kỳ, các cột phát sinh, Trả lại tiền thừa, Số dư cuối kỳ của HD-TEST-01 bằng nhau ở 2 màn',
       'Lệch thì ghi số của từng màn vào Ghi chú']),
    C('Khách hàng mới tạo có ngay ở ô chọn Khách hàng', 'P1', 'Vừa tạo khách hàng KH-MOI ở màn danh mục khách hàng.',
      ['1. Mở màn báo cáo', '2. Gõ 2 ký tự đầu mã KH-MOI vào ô Khách hàng'], 'Khách hàng: KH-MOI',
      ['KH-MOI có trong danh sách gợi ý, chọn được']),
    C('Đổi tên khách hàng thì báo cáo hiện tên mới', 'P2', 'KH-TEST có phát sinh trong kỳ.',
      ['1. Sửa tên KH-TEST ở màn danh mục khách hàng', '2. Mở báo cáo, lọc KH-TEST', '3. Xuất Excel'], '',
      ['Dòng khách hàng trên màn và trong file hiện "Mã - Tên mới"', 'Số liệu không đổi']),
    C('Không có hợp đồng bị lặp', 'P1', TT,
      ['1. Đặt 100 dòng/trang', '2. Rà cột Đơn hàng/hợp đồng của từng khách'], '',
      ['Mỗi hợp đồng chỉ có 1 dòng dưới đúng 1 khách hàng', 'Mỗi khách hàng chỉ có 1 dòng in đậm trên 1 trang']),
]

# ================================================================== VII. PHÂN QUYỀN
G7 = [
    C('Không có quyền nào vẫn mở được màn, chỉ thấy hợp đồng mình tạo', 'P0',
      'TK-NV không có quyền nào; KH-TEST có HD-TEST-01 (TK-NV tạo) đã có phát sinh; có hợp đồng khác của người khác cùng kỳ.',
      ['1. Đăng nhập TK-NV', '2. ' + MENU, '3. Chọn Thời gian = tháng có phát sinh'], 'Tài khoản TK-NV',
      ['Mở được màn, không báo thiếu quyền', 'Bảng chỉ có các hợp đồng có cột NVKD = TK-NV',
       'KHÔNG có ô Công ty, Phòng ban, Bộ phận, Nhân viên',
       'Dòng Tổng cộng chỉ cộng hợp đồng của TK-NV (so bằng tay tổng các dòng khi không lọc thêm)']),
    C('Quyền tổng công ty thấy toàn bộ và đủ 4 ô đơn vị', 'P0', 'Tài khoản TK-ALL.',
      ['1. Đăng nhập TK-ALL, mở báo cáo', '2. Chọn Thời gian 01/10/2026 - 31/10/2026'], 'Tài khoản TK-ALL',
      ['Có ô Công ty, Phòng ban, Bộ phận, Nhân viên', 'Bảng có hợp đồng của nhiều công ty / phòng ban',
       'Môi trường thử: chân bảng "Hiển thị 1–10 / 25,309 dòng hợp đồng"']),
    C('Quyền công ty: chỉ công ty đang làm việc và hợp đồng mình tạo', 'P0', 'TK-CTY thuộc Công ty A; có hợp đồng của Công ty B cùng kỳ.',
      ['1. Đăng nhập TK-CTY, mở báo cáo, chọn Thời gian', '2. Quan sát ô lọc và các dòng', '3. Tìm nhanh số hợp đồng của Công ty B'], 'Tài khoản TK-CTY',
      ['Không có ô Công ty; có ô Phòng ban, Bộ phận, Nhân viên', 'Không thấy hợp đồng Công ty B (trừ hợp đồng do TK-CTY tạo)',
       'Bước 3: "Không có dữ liệu phù hợp bộ lọc."']),
    C('Quyền phòng ban: các phòng mình quản lý', 'P1', 'TK-PB quản lý PB-1, đang ngồi PB-2 (không quản lý PB-2).',
      ['1. Đăng nhập TK-PB, mở báo cáo, chọn Thời gian', '2. Xem cột Phòng ban'], 'Tài khoản TK-PB',
      ['Chỉ thấy số của PB-1 và hợp đồng TK-PB tự tạo', 'KHÔNG tự thấy PB-2 chỉ vì đang ngồi ở đó',
       'Có ô Phòng ban, Bộ phận, Nhân viên; không có ô Công ty']),
    C('Quyền bộ phận: các bộ phận mình quản lý', 'P1', 'TK-BP quản lý BP-1.',
      ['1. Đăng nhập TK-BP, mở báo cáo, chọn Thời gian'], 'Tài khoản TK-BP',
      ['Chỉ thấy số của BP-1 và hợp đồng TK-BP tạo', 'Chỉ có ô Bộ phận, Nhân viên']),
    C('Có nhiều quyền thì lấy cấp rộng nhất', 'P2', 'TK-X có cả quyền "... theo bộ phận" và "... theo tổng công ty".',
      ['1. Đăng nhập TK-X, mở báo cáo, chọn Thời gian'], 'Tài khoản TK-X', ['Như TK-ALL: có ô Công ty, thấy toàn bộ']),
    C('Phạm vi áp cho dòng Tổng cộng, popup và Excel', 'P0', 'TK-NV (không quyền); đã biết Tổng cộng của TK-ALL cùng kỳ.',
      ['1. TK-NV mở báo cáo, chọn cùng kỳ', '2. So dòng Tổng cộng với TK-ALL', '3. Bấm 1 số ở dòng khách hàng, xem popup',
       '4. Xuất Excel, mở file'], 'Tài khoản TK-NV',
      ['Tổng cộng (cả Số dư đầu kỳ) chỉ gồm số trong phạm vi TK-NV, nhỏ hơn TK-ALL',
       'Popup chỉ có chứng từ của hợp đồng TK-NV tạo', 'File Excel chỉ có các dòng TK-NV thấy trên màn']),
] + pq_chung(M)

GROUPS = [
    ('HIỂN THỊ TRANG & TRUY CẬP', G1),
    ('TÌM KIẾM & LỌC DANH SÁCH', G2),
    ('SỐ LIỆU BÁO CÁO', G3),
    ('XEM CHI TIẾT CHỨNG TỪ', G4),
    ('XUẤT DANH SÁCH EXCEL', G5),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', G6),
    ('PHÂN QUYỀN', G7),
]

if __name__ == '__main__':
    build_chuan(OUT, 'Trang tính1', TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, sections(GROUPS), loai='bao_cao')
    print(dem(GROUPS))

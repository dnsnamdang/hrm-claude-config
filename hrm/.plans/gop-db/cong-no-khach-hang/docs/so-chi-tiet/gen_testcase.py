# -*- coding: utf-8 -*-
"""Testcase "Sổ chi tiết công nợ phải thu khách hàng" — KHUÔN CHUẨN tab "13. DM quốc gia" (skill testcase-documenter,
tc_chuan.build_chuan, loại bao_cao). Mẫu: sale-customer-debt-reports/docs/compare/gen_testcase.py.
Case chung (phân trang, lưu bộ lọc) lấy từ _tc_bc_chung.py (bản sao trong thư mục này).
Không có TC cũ cho màn này. Số liệu mẫu đọc trên dev-hrm 18/11/2026 (capture.js).
Chạy: python gen_testcase.py  (tự gọi check_tc — phải 0 lỗi)
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(GOPDB, '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets'))
from tc_chuan import build_chuan  # noqa: E402
from _tc_bc_chung import C, sections, dem, pt_chung, luu_chung  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

TEN = 'Sổ chi tiết công nợ phải thu khách hàng'
MODULE = 'Sổ chi tiết công nợ phải thu KH'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)


def L_(*lines):
    return '\n'.join(lines)


MENU = 'Vào phân hệ Tài chính > menu Kế toán công nợ > nhóm Khách hàng > bấm "Sổ chi tiết công nợ phải thu khách hàng"'
MENU_CD = 'Tài chính > Kế toán công nợ > Khách hàng > Bảng cân đối phát sinh công nợ khách hàng'
LOC = 'Chọn Tài khoản 131 - Phải thu của khách hàng, Khách hàng KH-TEST, Thời gian 01/01/2026 - 31/10/2026'
LN = 'Chọn tài khoản, khách hàng và thời gian để xem sổ chi tiết.'
QN = 'Xem sổ chi tiết công nợ phải thu khách hàng'
MSG = 'Vui lòng chọn tài khoản, khách hàng và thời gian'
KND = 'Không có dữ liệu phù hợp bộ lọc.'
BL = 'Tài khoản TK-TCT; đã chọn TK 131, khách hàng 14TQUPCA-2, kỳ 01/01/2026 - 31/10/2026, Loại tiền VNĐ (môi trường thử: 73 bút toán).'
NEN = 'Đã ghi lại 3 dòng tổng và chân bảng của KH-TEST, TK 131, kỳ 01/01/2026 - 31/10/2026 (số nền).'
MENU_PX = 'Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Xuất hàng > Phiếu xuất hàng'
MENU_PT = 'Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu thu'
MENU_PC = 'Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu chi'
MENU_PKT = 'Tài chính > Sổ tổng hợp > Phiếu kế toán'
MENU_NH = 'Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Nhập hàng > Phiếu nhập hàng'

M = {
    'dv': 'bút toán',
    'loc': LOC,
    'nhieu_trang': 'Tài khoản TK-TCT; khách hàng 14TQUPCA-2 có 73 bút toán trên TK 131 kỳ 01/01/2026 - 31/10/2026 (8 trang 10 dòng).',
    'doi_loc': 'Nhập "PXH" vào ô Số chứng từ, nhấn Enter',
    'loi_nhac': LN,
    'man_khac': 'Tài chính > Kế toán công nợ > Khách hàng > Bảng cân đối phát sinh công nợ khách hàng',
}
M['loc'] = 'Chọn Tài khoản 131, Khách hàng 14TQUPCA-2, Thời gian 01/01/2026 - 31/10/2026'
PT = pt_chung(M)
M['loc'] = LOC
LUU = luu_chung(M)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Báo cáo chỉ đọc: liệt kê từng bút toán công nợ của 1 khách hàng trên 1 tài khoản trong kỳ, kèm Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ; xem theo VNĐ hoặc Ngoại tệ.',
        'Chức năng: Xem sổ, Tìm kiếm / lọc, In, Xuất Excel.',
        'Đường vào: ' + MENU + '; hoặc bấm mã khách hàng ở ' + MENU_CD + '.',
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Bút toán đã ghi sổ của khách hàng đã chọn, trên tài khoản đã chọn và các tài khoản con trực tiếp (131 -> 1311, 1312, 1313).',
        'Loại tiền VNĐ: chỉ bút toán VNĐ. Loại tiền Ngoại tệ: chỉ bút toán khác VNĐ (USD…).',
        'Bảng: 3 dòng tổng (Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ) -> các dòng bút toán.',
        'Cột mẫu VNĐ: STT | Đơn hàng/Hợp đồng | Ngày hạch toán | Số chứng từ | NVKD | Phòng ban | Ghi chú | Phát sinh nợ | Phát sinh có | Tài khoản đối ứng (Tài khoản, Tên tài khoản).',
        'Mẫu Ngoại tệ thay 2 cột phát sinh bằng: Loại tiền | Số phát sinh ngoại tệ (Nợ, Có) | Tỷ giá | Số phát sinh VNĐ (Nợ, Có).',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '-  Bút toán của khách hàng khác, tài khoản khác, tài khoản cháu (cấp sâu hơn con trực tiếp).',
        '-  Bút toán có ngày hạch toán sau Đến ngày; bút toán trước Từ ngày chỉ vào Số dư đầu kỳ.',
        '-  Bút toán khác loại tiền đang chọn.',
        '-  Chứng từ chưa hạch toán (chưa ghi sổ).',
        '-  Bút toán ngoài phạm vi quyền của người xem.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô Thời gian (bắt buộc) lọc theo NGÀY HẠCH TOÁN của bút toán, tính cả 2 đầu mút.',
        'Mặc định trống; F5 / Làm mới / chuyển sang màn khác rồi quay lại đều về trống.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Không phân cấp: 3 dòng tổng rồi danh sách bút toán phẳng, 1 bút toán 1 dòng (1 chứng từ có thể nhiều dòng).',
        'Xếp theo ngày hạch toán, cùng ngày theo thời điểm tạo; phân trang 10 / 20 / 50 / 100 bút toán.',
        'Không sắp xếp theo cột, không có tùy chỉnh cột, không có popup chi tiết.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '-  Số dư đầu kỳ = Tổng Nợ - Tổng Có (số quy đổi VNĐ) trước Từ ngày; dương ghi cột nợ, âm ghi cột có.',
        '-  Tổng phát sinh = Tổng Nợ và Tổng Có trong kỳ (không bù trừ), tính trên mọi trang.',
        '-  Số dư cuối kỳ = Số dư đầu kỳ + Tổng phát sinh nợ - Tổng phát sinh có.',
        '-  Mẫu Ngoại tệ: 3 dòng tổng cho TỪNG loại tiền.',
        '-  MỌI ô lọc (kể cả ô tìm nhanh) áp cả cho Số dư đầu kỳ.',
    )),
    ('7. Phân quyền cấp', L_(
        'Quyền "%s" — mức: Tổng công ty / Công ty.' % QN,
        '-  Tổng công ty: mọi công ty; có ô Công ty.',
        '-  Công ty: bút toán của công ty đang làm việc + bút toán của hợp đồng do mình tạo; không có ô Công ty.',
        '-  Không có quyền: ẩn mục menu; mở bằng đường dẫn thì báo không có quyền, không có số liệu, không In / Xuất Excel được.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Phát sinh nợ / có của dòng = số quy đổi VNĐ của bút toán theo chiều ghi sổ.',
        'Chân bảng "Hiển thị a–b / N bút toán": N = số bút toán trong kỳ theo bộ lọc.',
        'Ví dụ môi trường thử (14TQUPCA-2, TK 131, 01/01–31/10/2026): 167,583,599 + 686,725,656 - 632,677,254 = 221,632,001.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        '-  Số dạng 1,234,567.89 (tối đa 2 số lẻ); ô bằng 0 ở dòng tổng để trống.',
        '-  Lọc thêm ô tìm nhanh / Số chứng từ / Đơn hàng/Hợp đồng / Số tiền / Tài khoản đối ứng thì Số dư đầu kỳ chỉ còn là số dư của phần bút toán khớp điều kiện — đúng thiết kế, không phải lỗi.',
        '-  Ô Phòng ban / Bộ phận lọc theo đơn vị ghi trên bút toán; cột Phòng ban hiện phòng ban hiện tại của NVKD nên có thể khác.',
        'Dữ liệu mẫu: KH-TEST = khách hàng có >= 15 bút toán VNĐ trên TK 131 trong 2026, có phiếu xuất hàng và phiếu thu; KH-USD = khách hàng có bút toán USD.',
        'TK-TCT (quyền mức Tổng công ty), TK-CT (mức Công ty, đang làm việc công ty A), NV-A (mức Công ty, người tạo hợp đồng HD-B ở công ty B), TK-KQ (không có quyền).',
    )),
]

# ================================================================== I. HIỂN THỊ TRANG & TRUY CẬP
G1 = [
    C('Mở màn hình từ menu', 'P0', 'Tài khoản TK-TCT đã đăng nhập.', ['1. Đăng nhập', '2. ' + MENU], '',
      ['Tiêu đề trang và tiêu đề bảng "%s", cạnh tiêu đề trang có icon (i)' % TEN,
       'Bảng hiện "' + LN + '", không tự tải số liệu',
       'Nhóm Khách hàng có các mục: Sổ chi tiết công nợ phải thu khách hàng, Bảng cân đối phát sinh công nợ khách hàng, Báo cáo hạn mức công nợ khách hàng, Công nợ đầu kỳ theo khách hàng - hợp đồng, Khai báo hạn mức công nợ KH']),
    C('Mở màn từ Bảng cân đối phát sinh công nợ khách hàng', 'P0', 'Tài khoản TK-TCT; Bảng cân đối đã lọc TK 131, kỳ 01/01/2026 - 31/10/2026, có dòng khách hàng 14TQUPCA-2.',
      ['1. Vào ' + MENU_CD, '2. Chọn Tài khoản 131, Thời gian 01/01/2026 - 31/10/2026', '3. Bấm mã khách hàng 14TQUPCA-2'], '',
      ['Mở tab mới màn "%s"' % TEN, 'Bộ lọc điền sẵn: Tài khoản 131 - Phải thu của khách hàng, Khách hàng 14TQUPCA-2 - CÔNG TY CỔ PHẦN CƠ KHÍ GIAO THÔNG QUẢNG NINH, Thời gian 01/01/2026 - 31/10/2026, Loại tiền VNĐ',
       'Bảng tự tải, không cần bấm Tìm kiếm', 'Số dư đầu kỳ / cuối kỳ khớp số của dòng khách hàng đó trên Bảng cân đối']),
    C('Mở từ Bảng cân đối thắng bộ lọc đã lưu', 'P1', 'Trong 10 phút trước đó đã xem sổ chi tiết của khách hàng khác.',
      ['1. Vào ' + MENU_CD + ', lọc như case trên', '2. Bấm mã một khách hàng khác'], '',
      ['Sổ chi tiết mở với khách hàng vừa bấm, không giữ khách hàng cũ', 'Thanh địa chỉ không còn tham số lọc sau khi mở']),
    C('Bố cục khu vực lọc và các nút', 'P1', 'Tài khoản TK-TCT, chưa đổi Cài đặt bộ lọc.', ['1. Mở màn', '2. Quan sát khung "Bộ lọc danh sách" và hàng nút trên bảng'], '',
      ['Ô tìm nhanh gợi ý "Tìm theo số chứng từ hoặc số hợp đồng"; nút Tìm kiếm, Làm mới, Cài đặt bộ lọc, Ẩn tìm kiếm nâng cao',
       'Các ô: Công ty, Phòng ban, Bộ phận, Nhân viên, Tài khoản *, Khách hàng *, Thời gian *, Tài khoản đối ứng, Đơn hàng/Hợp đồng, Số chứng từ, Loại tiền (mặc định VNĐ), Số tiền',
       'Trên bảng: nút In, Xuất Excel; không có nút Thêm / Sửa / Xóa']),
    C('Kiểm tra đủ các cột mẫu VNĐ', 'P0', 'Đang mở màn, Loại tiền VNĐ.', ['1. Đọc tiêu đề bảng từ trái sang phải'], '',
      ['STT | Đơn hàng/Hợp đồng | Ngày hạch toán | Số chứng từ | NVKD | Phòng ban | Ghi chú | Phát sinh nợ | Phát sinh có | Tài khoản đối ứng (Tài khoản, Tên tài khoản)',
       'Tiêu đề "Tài khoản đối ứng" gộp 2 cột con; các cột khác gộp dọc 2 tầng']),
    C('Kiểm tra cột mẫu Ngoại tệ', 'P0', 'Đang mở màn.', ['1. Chọn Loại tiền: Ngoại tệ', '2. Đọc tiêu đề bảng'], '',
      ['Thay 2 cột Phát sinh nợ / Phát sinh có bằng: Loại tiền | Số phát sinh ngoại tệ (Nợ, Có) | Tỷ giá | Số phát sinh VNĐ (Nợ, Có)', 'Các cột còn lại giữ nguyên']),
    C('Nội dung icon (i) cạnh tiêu đề trang', 'P2', 'Đang mở màn.', ['1. Rê chuột vào icon (i) cạnh tiêu đề trang'], '',
      ['Hiện: "Sổ chi tiết từng bút toán công nợ của một khách hàng trên một tài khoản: số dư đầu kỳ, phát sinh Nợ / Có trong kỳ, số dư cuối kỳ. Quyền xem theo tổng công ty hoặc công ty (công ty: sổ của công ty mình và các hợp đồng do mình tạo)."']),
    C('Bảng có số liệu: 3 dòng tổng và dòng bút toán', 'P0', BL, ['1. Quan sát bảng'], '',
      ['3 dòng đầu nền xám, chữ đậm: Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ (nhãn căn phải ở ô gộp 7 cột đầu)',
       'Môi trường thử: Số dư đầu kỳ 167,583,599 (cột nợ); Tổng phát sinh 686,725,656 / 632,677,254; Số dư cuối kỳ 221,632,001',
       'Tiếp theo là bút toán STT 1, 2, 3…; dòng 1: HĐ_TPE_HN_KD2_25_0672_FQN | 19/01/2026 | PXH-16319 | Lê Ngọc Tiến | PHÒNG THIẾT BỊ Ô TÔ 2 | | 96,184,800 | | 5111, 33311 | Doanh thu bán hàng hóa, Thuế GTGT đầu ra']),
    C('Không có bút toán trong kỳ', 'P1', 'Khách hàng KH-TEST không có bút toán ngày 31/10/2026.',
      ['1. Chọn Tài khoản 131, Khách hàng KH-TEST, Thời gian 31/10/2026 - 31/10/2026'], '',
      ['3 dòng tổng vẫn hiện; Tổng phát sinh để trống; Số dư cuối kỳ = Số dư đầu kỳ', 'Dưới 3 dòng tổng hiện "' + KND + '"', 'Không có chân bảng và thanh phân trang']),
    C('Đang tải dữ liệu', 'P2', 'Khách hàng nhiều bút toán.', ['1. Chọn đủ 3 ô bắt buộc', '2. Quan sát bảng ngay khi chọn xong'], '',
      ['Bảng hiện biểu tượng xoay và "Đang tải dữ liệu..."', 'Tải xong thì thay bằng số liệu']),
    C('Tiêu đề bảng dính khi cuộn', 'P2', BL, ['1. Đổi Số dòng/trang = 100', '2. Cuộn bảng xuống cuối'], '',
      ['Hàng tiêu đề cột luôn hiện ở trên cùng khung bảng khi cuộn']),
    C('Hiệu năng tải số liệu', 'P1', BL, ['1. Bấm Làm mới', '2. Chọn lại đủ 3 ô bắt buộc, bấm giờ đến khi bảng hiện số liệu'], '',
      ['Môi trường thử: khoảng 1 giây; không quá 3 giây', 'Chuyển trang nhanh hơn lần đầu (không tính lại 3 dòng tổng)']),
] + PT + [
    C('3 dòng tổng giữ nguyên khi chuyển trang', 'P0', BL, ['1. Ghi lại 3 dòng tổng ở trang 1', '2. Sang trang 2, trang cuối', '3. Đổi Số dòng/trang = 50'], '',
      ['3 dòng tổng luôn hiện ở đầu mọi trang với cùng giá trị', 'STT trang 2 bắt đầu từ 11']),
    C('Thứ tự bút toán', 'P1', BL, ['1. Đọc cột Ngày hạch toán trang 1 và trang 2'], '',
      ['Ngày hạch toán tăng dần; cùng ngày thì xếp theo thời điểm tạo bút toán', 'Các dòng của cùng một chứng từ đứng liền nhau (vd PXH-16319 dòng 1, 2)']),
]

# ================================================================== II. TÌM KIẾM & LỌC
TK = [
    C('Bấm Tìm kiếm khi thiếu ô bắt buộc', 'P0', 'Đang mở màn, chưa chọn gì.', ['1. Bấm Tìm kiếm'], '',
      ['Viền đỏ và chữ đỏ dưới ô: "Vui lòng chọn tài khoản", "Vui lòng chọn khách hàng", "Vui lòng chọn thời gian"', 'Không tải số liệu; bảng giữ lời nhắc']),
    C('Chữ đỏ tự tắt khi chọn xong ô', 'P1', 'Đang hiện chữ đỏ 3 ô bắt buộc.', ['1. Chọn Tài khoản 131', '2. Chọn Khách hàng', '3. Chọn Thời gian'], '',
      ['Chọn xong ô nào thì chữ đỏ ô đó biến mất ngay', 'Đủ 3 ô thì bảng tự tải số liệu']),
    C('Thiếu ô bắt buộc khi khung lọc đang thu gọn', 'P2', 'Khung lọc đã bấm "Ẩn tìm kiếm nâng cao", chưa chọn Tài khoản.', ['1. Bấm In'], '',
      ['Thông báo "' + MSG + '"', 'Khung lọc tự mở ra, ô thiếu viền đỏ']),
    C('Ô Tài khoản: danh sách và tài khoản con', 'P0', 'Đang mở màn.', ['1. Mở ô Tài khoản, gõ "131"', '2. Chọn 131 - Phải thu của khách hàng, chọn Khách hàng 14TQUPCA-2, kỳ 01/01–31/10/2026', '3. Đọc cột Tài khoản đối ứng và đối chiếu chứng từ'], '',
      ['Danh sách hiện dạng "Số hiệu - Tên", gồm 131, 1311, 1312, 1313', 'Chọn 131: sổ gồm bút toán ghi vào 131 và các tài khoản con trực tiếp 1311, 1312, 1313']),
    C('Ô Tài khoản: chọn tài khoản con', 'P0', 'Khách hàng 14TQUPCA-2 có bút toán ở cả 131 và 1311.', ['1. Chọn Tài khoản 1311, giữ khách hàng và kỳ', '2. So với khi chọn 131'], '',
      ['Chỉ còn bút toán của 1311 (và con trực tiếp của 1311 nếu có)', 'Chân bảng nhỏ hơn hoặc bằng khi chọn 131']),
    C('Ô Khách hàng: gõ tối thiểu 2 ký tự', 'P0', 'Đang mở màn.', ['1. Bấm ô Khách hàng, gõ 1 ký tự "1"', '2. Gõ thêm "4T"'], '',
      ['Bước 1: chưa tìm, nhắc gõ thêm ký tự', 'Bước 2: hiện tối đa 20 khách hàng dạng "Mã KH - Tên khách hàng" có mã / tên / số điện thoại chứa "14T"']),
    C('Ô Khách hàng: tìm theo tên, số điện thoại', 'P1', 'Khách hàng 14TQUPCA-2 có số điện thoại đã khai.', ['1. Gõ một phần tên "CƠ KHÍ GIAO THÔNG"', '2. Xóa, gõ số điện thoại của khách'], '',
      ['Cả 2 lần đều tìm thấy khách hàng 14TQUPCA-2', 'Dòng gợi ý ghi "14TQUPCA-2 - CÔNG TY CỔ PHẦN CƠ KHÍ GIAO THÔNG QUẢNG NINH"']),
    C('Ô Khách hàng: xóa bằng nút x', 'P1', BL, ['1. Bấm nút x trong ô Khách hàng'], '',
      ['Ô Khách hàng trống', 'Bảng về lời nhắc "' + LN + '"']),
    C('Ô Thời gian: chặn Đến ngày trước Từ ngày', 'P0', 'Đang mở màn.', ['1. Chọn Từ ngày 31/10/2026', '2. Mở lịch Đến ngày, thử chọn hoặc gõ 01/01/2026'], '',
      ['Các ngày trước 31/10/2026 bị mờ, không chọn được', 'Gõ tay 01/01/2026 không được nhận, Đến ngày giữ giá trị hợp lệ']),
    C('Ô Thời gian tính cả 2 đầu mút', 'P0', 'KH-TEST có bút toán ngày 01/02/2026 và 03/02/2026.', ['1. Chọn Thời gian 01/02/2026 - 03/02/2026'], '',
      ['Có cả bút toán ngày 01/02/2026 và ngày 03/02/2026', 'Bút toán ngày 31/01/2026 và 04/02/2026 không có trên bảng']),
    C('Ô tìm nhanh theo số chứng từ', 'P0', BL, ['1. Gõ "PXH-16319" vào ô tìm nhanh, nhấn Enter'], 'Từ khóa: PXH-16319',
      ['Chỉ còn 2 bút toán của PXH-16319 (96,184,800 nợ và 4,809,240 có)', 'Chân bảng "Hiển thị 1–2 / 2 bút toán"', 'Tổng phát sinh = 96,184,800 / 4,809,240']),
    C('Ô tìm nhanh theo một phần số hợp đồng', 'P0', BL, ['1. Gõ "0672_FQN" vào ô tìm nhanh, nhấn Enter'], 'Từ khóa: 0672_FQN',
      ['Chỉ còn bút toán của hợp đồng HĐ_TPE_HN_KD2_25_0672_FQN']),
    C('Ô tìm nhanh làm đổi cả Số dư đầu kỳ', 'P0', BL, ['1. Ghi lại Số dư đầu kỳ (167,583,599)', '2. Gõ "PXH" vào ô tìm nhanh, nhấn Enter', '3. Đọc 3 dòng tổng'], 'Từ khóa: PXH',
      ['Môi trường thử: còn 31 bút toán; Số dư đầu kỳ 604,627,127; Tổng phát sinh 568,072,256 / 37,187,441; Số dư cuối kỳ 1,135,511,942',
       'Lưu ý: Số dư đầu kỳ chỉ tính bút toán đầu kỳ có số chứng từ / số hợp đồng chứa từ khóa — đúng thiết kế (lọc áp cả đầu kỳ)',
       'Số dư cuối kỳ = Số dư đầu kỳ + Tổng phát sinh nợ - Tổng phát sinh có']),
    C('Tìm nhanh không phân biệt hoa thường, bỏ khoảng trắng', 'P1', BL, ['1. Gõ "pxh-16319", nhấn Enter', '2. Gõ "  PXH-16319  ", nhấn Enter'], '',
      ['Cả 2 lần ra cùng 2 bút toán của PXH-16319']),
    C('Tìm nhanh từ khóa không tồn tại', 'P1', BL, ['1. Gõ "zzzkhongtontai999", nhấn Enter'], '',
      ['3 dòng tổng vẫn hiện nhưng để trống số', 'Dưới hiện "' + KND + '"', 'Không có chân bảng']),
    C('Tìm nhanh với ký tự đặc biệt', 'P2', BL, ['1. Gõ lần lượt từng chuỗi ở Test data, nhấn Enter'], ['%', '_', "' OR 1=1 --", '<b>abc</b>'],
      ['% và _ được hiểu là ký tự thường: hiện "' + KND + '"', 'Không báo lỗi hệ thống, không hiện chữ in đậm từ chuỗi đã gõ']),
    C('Giới hạn độ dài ô tìm nhanh', 'P2', BL, ['1. Dán chuỗi 500 ký tự vào ô tìm nhanh, nhấn Enter'], 'Chuỗi "abcde" lặp 100 lần',
      ['Ô nhận đủ chuỗi, không báo lỗi', 'Bảng hiện "' + KND + '", màn không treo']),
    C('Gõ chưa nhấn Enter thì chưa lọc', 'P1', BL, ['1. Gõ "PXH" vào ô tìm nhanh, không nhấn Enter', '2. Bấm sang trang 2', '3. Bấm Xuất Excel'], '',
      ['Bước 1: bảng chưa đổi', 'Bước 2, 3: vẫn theo bộ lọc đã áp trước đó, chưa tính từ khóa đang gõ dở']),
    C('Xóa từ khóa thì về đầy đủ', 'P1', 'Đang lọc ô tìm nhanh "PXH" (31 bút toán).', ['1. Xóa hết ô tìm nhanh', '2. Nhấn Enter'], '',
      ['Chân bảng về "Hiển thị 1–10 / 73 bút toán"', '3 dòng tổng về số nền']),
    C('Ô Số chứng từ lọc gần đúng', 'P1', BL, ['1. Nhập "PKT0226" vào ô Số chứng từ, nhấn Enter'], '',
      ['Chỉ còn bút toán có số chứng từ chứa "PKT0226" (vd TPE.PKT0226.00052, TPE.PKT0226.00131)']),
    C('Ô Đơn hàng/Hợp đồng lọc gần đúng', 'P1', BL, ['1. Nhập "CSKH" vào ô Đơn hàng/Hợp đồng, nhấn Enter'], '',
      ['Chỉ còn bút toán của hợp đồng có số chứa "CSKH"', 'Bút toán không gắn hợp đồng không còn']),
    C('Ô Tài khoản đối ứng', 'P0', BL, ['1. Chọn Tài khoản đối ứng 5111'], '',
      ['Bảng tải lại ngay', 'Chỉ còn bút toán có Tài khoản đối ứng chứa 5111 (dòng doanh thu của phiếu xuất hàng)']),
    C('Ô Số tiền từ - đến', 'P0', BL, ['1. Nhập Số tiền từ 1,000,000 đến 5,000,000, nhấn Enter'], ['Số tiền từ: 1,000,000', 'Số tiền đến: 5,000,000'],
      ['Chỉ còn bút toán có số tiền (VNĐ) trong khoảng 1,000,000 - 5,000,000 (vd 1,143,655 và 4,254,120)', 'Ô tự thêm dấu phẩy ngăn nghìn khi gõ']),
    C('Ô Số tiền nhập 0 thì không lọc', 'P2', BL, ['1. Nhập Số tiền từ 0, nhấn Enter'], '', ['Kết quả như không nhập Số tiền']),
    C('Ô Loại tiền: Ngoại tệ', 'P0', 'Khách hàng KH-USD có bút toán USD trên TK 131 năm 2026.', ['1. Chọn TK 131, Khách hàng KH-USD, Thời gian 01/01/2026 - 31/10/2026', '2. Chọn Loại tiền: Ngoại tệ'], '',
      ['Bảng tải lại ngay theo mẫu Ngoại tệ', 'Chỉ có bút toán USD; cột Loại tiền ghi USD, có Tỷ giá', 'Loại tiền VNĐ: không có bút toán USD của khách này']),
    C('Ô Loại tiền bấm x xóa', 'P2', BL, ['1. Bấm nút x ở ô Loại tiền'], '', ['Số liệu và cột như mẫu VNĐ']),
    C('Ô Công ty (quyền Tổng công ty)', 'P1', 'TK-TCT; khách hàng có bút toán ở 2 công ty.', ['1. Lọc như thường', '2. Chọn Công ty: CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT'], '',
      ['Chỉ còn bút toán ghi cho công ty đã chọn; 3 dòng tổng tính lại', 'Icon ổ khóa cạnh nhãn bật / tắt hiện cả công ty đã khóa']),
    C('Ô Phòng ban / Bộ phận lọc theo đơn vị ghi trên bút toán', 'P1', BL, ['1. Chọn Phòng ban: PHÒNG THIẾT BỊ Ô TÔ 2', '2. Đọc cột Phòng ban'], '',
      ['Chỉ còn bút toán ghi cho phòng ban đó', 'Lưu ý: cột Phòng ban là phòng ban HIỆN TẠI của NVKD nên có thể khác phòng ban đang lọc']),
    C('Ô Nhân viên lọc theo người tạo hợp đồng', 'P0', BL, ['1. Chọn Nhân viên: Cao Xuân Khang'], '',
      ['Chỉ còn bút toán có NVKD = Cao Xuân Khang', 'Bút toán không gắn hợp đồng không còn']),
    C('Kết hợp nhiều điều kiện', 'P1', BL, ['1. Nhập Số chứng từ "PXH", chọn Tài khoản đối ứng 5111, nhấn Enter'], '',
      ['Chỉ còn bút toán thỏa ĐỒNG THỜI 2 điều kiện', 'Trở về trang 1, chân bảng và 3 dòng tổng tính lại']),
    C('Bấm Làm mới', 'P0', 'Đang lọc nhiều ô, Loại tiền Ngoại tệ.', ['1. Bấm Làm mới'], '',
      ['Mọi ô về trống, Loại tiền về VNĐ, chữ đỏ ẩn', 'Bảng về lời nhắc "' + LN + '"']),
    C('Ẩn / mở khu vực lọc', 'P2', 'Đang mở màn.', ['1. Bấm "Ẩn tìm kiếm nâng cao"', '2. Bấm lại nút'], '',
      ['Bước 1: các ô lọc thu gọn, ô tìm nhanh vẫn hiện', 'Bước 2: các ô lọc hiện lại, giữ giá trị']),
    C('Cài đặt bộ lọc: ẩn ô và đóng không lưu', 'P2', 'Đang mở màn.', ['1. Bấm Cài đặt bộ lọc', '2. Bỏ tích "Loại tiền", bấm Đóng', '3. Mở lại, bỏ tích "Loại tiền", bấm Lưu'], '',
      ['Cửa sổ "Cài đặt bộ lọc" liệt kê 9 mục: Công ty / Phòng ban / Bộ phận / Nhân viên, Tài khoản, Khách hàng, Thời gian, Tài khoản đối ứng, Đơn hàng/Hợp đồng, Số chứng từ, Loại tiền, Số tiền',
       'Bước 2: ô Loại tiền vẫn hiện', 'Bước 3: ô Loại tiền ẩn; giữ sau khi tải lại trang (lưu theo người dùng)']),
] + LUU

# ================================================================== III. SỐ LIỆU BÁO CÁO
SL = [
    C('Số dư cuối kỳ = đầu kỳ + nợ - có', 'P0', BL, ['1. Đọc 3 dòng tổng'], '',
      ['Số dư đầu kỳ 167,583,599 cộng Tổng phát sinh nợ 686,725,656 trừ Tổng phát sinh có 632,677,254 bằng 221,632,001', 'Đúng số ở dòng Số dư cuối kỳ']),
    C('Tổng phát sinh = cộng mọi trang', 'P0', BL, ['1. Xuất Excel', '2. Cộng cột Phát sinh nợ, Phát sinh có của 73 bút toán'], '',
      ['Tổng cột nợ = 686,725,656; tổng cột có = 632,677,254 (bằng dòng Tổng phát sinh)']),
    C('Số dư âm ghi ở cột Phát sinh có', 'P0', 'Khách hàng 14TQUPCA-181 có Số dư đầu kỳ âm 163,072 trên TK 131 tại 01/01/2026.',
      ['1. Chọn TK 131, Khách hàng 14TQUPCA-181, Thời gian 01/01/2026 - 31/10/2026'], '',
      ['Số dư đầu kỳ: cột nợ trống, cột có 163,072', 'Số dư cuối kỳ dương ghi ở cột nợ']),
    C('Số dư bằng 0 thì để trống', 'P1', 'Khách hàng có Số dư cuối kỳ bằng 0 (vd 14TQUPVI-1 kỳ 01/01/2026 - 31/10/2026).', ['1. Lọc khách hàng đó', '2. Đọc dòng Số dư cuối kỳ'], '',
      ['Cả 2 ô nợ, có của dòng Số dư cuối kỳ để trống (không in "0")']),
    C('Số dư đầu kỳ chỉ tính bút toán trước Từ ngày', 'P0', 'Biết số dư cuối kỳ của KH-TEST kỳ 01/01/2026 - 31/01/2026 là X.',
      ['1. Chọn Thời gian 01/02/2026 - 31/10/2026', '2. Đọc Số dư đầu kỳ'], '', ['Số dư đầu kỳ = X (số dư cuối kỳ của kỳ liền trước)']),
    C('Phát sinh nợ / có từng bút toán', 'P0', BL, ['1. Bấm số chứng từ PXH-16319, xem phiếu', '2. So 2 dòng PXH-16319 trên sổ'], '',
      ['Dòng doanh thu ghi nợ 96,184,800 (đối ứng 5111, 33311)', 'Dòng giảm giá ghi có 4,809,240 (đối ứng 5213, 33311)', 'Mỗi bút toán chỉ có số ở 1 trong 2 cột']),
    C('Cột Tài khoản đối ứng nhiều tài khoản', 'P1', BL, ['1. Đọc dòng 1'], '',
      ['Cột Tài khoản: "5111, 33311"; cột Tên tài khoản: "Doanh thu bán hàng hóa, Thuế GTGT đầu ra" — cùng thứ tự, cách nhau dấu phẩy']),
    C('Cột NVKD và Phòng ban', 'P1', BL, ['1. Đọc cột NVKD, Phòng ban của bút toán thuộc hợp đồng CSKH'], '',
      ['NVKD = người tạo hợp đồng (vd Cao Xuân Khang)', 'Phòng ban = phòng ban hiện tại của người đó (PHÒNG CHĂM SÓC KHÁCH HÀNG)', 'Bút toán không gắn hợp đồng: 2 cột trống']),
    C('Cột Ghi chú', 'P2', 'KH-TEST có phiếu thu có ghi chú "Thu tiền hàng tháng 3".', ['1. Tìm dòng phiếu thu đó'], '',
      ['Cột Ghi chú hiện đúng ghi chú của phiếu thu', 'Bút toán của phiếu kế toán: Ghi chú để trống']),
    C('Mẫu Ngoại tệ: số nguyên tệ, tỷ giá, quy đổi', 'P0', 'KH-USD có phiếu báo có USD 11,000 tỷ giá 26,145.', ['1. Lọc KH-USD, Loại tiền Ngoại tệ', '2. Đọc dòng phiếu báo có đó'], '',
      ['Loại tiền USD; cột Số phát sinh ngoại tệ (Có) 11,000; Tỷ giá 26,145', 'Cột Số phát sinh VNĐ (Có) 287,595,000 = 11,000 x 26,145']),
    C('Mẫu Ngoại tệ: dòng tổng theo loại tiền', 'P0', 'KH-USD (môi trường thử: khách 29TPHPTH-203).', ['1. Lọc KH-USD, Loại tiền Ngoại tệ', '2. Đọc 3 dòng tổng'], '',
      ['Mỗi loại tiền có 3 dòng tổng, cột Loại tiền ghi USD', 'Môi trường thử: đầu kỳ có 2,948,733.45 USD; phát sinh nợ 256,050, có 37,895,482.17; cuối kỳ có 40,588,165.62 (= 2,948,733.45 + 37,895,482.17 - 256,050)']),
    C('Định dạng số', 'P1', BL, ['1. Quan sát các cột số'], '',
      ['Dấu phẩy ngăn nghìn, dấu chấm thập phân, tối đa 2 số lẻ (vd 2,948,733.45)', 'Số căn phải; ô không có số để trống']),
    C('Bút toán chỉ của khách hàng đã chọn', 'P0', 'Phiếu kế toán PKT-TEST bù trừ công nợ giữa KH-TEST và 1 khách hàng khác.', ['1. Lọc KH-TEST', '2. Tìm số PKT-TEST ở ô Số chứng từ'], '',
      ['Chỉ hiện các dòng của phiếu ghi cho KH-TEST, không hiện dòng ghi cho khách hàng kia']),
    C('Khớp với Bảng cân đối phát sinh công nợ khách hàng', 'P0', 'Cùng TK 131, kỳ 01/01/2026 - 31/10/2026, Loại tiền VNĐ.',
      ['1. Vào ' + MENU_CD + ', lọc như trên, đọc dòng 14TQUPCA-2', '2. So với 3 dòng tổng của sổ chi tiết cùng khách'], '',
      ['Dư đầu kỳ, Phát sinh, Dư cuối kỳ trên Bảng cân đối bằng 3 dòng tổng của sổ chi tiết']),
    C('Lập phiếu thu thì số tăng đúng', 'P0', NEN + '\nCó quyền lập và hạch toán phiếu thu.',
      ['1. Vào ' + MENU_PT + ', lập phiếu thu cho KH-TEST 5,000,000, ngày 15/10/2026, hạch toán', '2. Quay lại sổ chi tiết, lọc như số nền'], 'Số tiền: 5,000,000',
      ['Có thêm 1 dòng phiếu thu ngày 15/10/2026, cột Phát sinh có 5,000,000, Tài khoản đối ứng là tài khoản tiền', 'Tổng phát sinh có tăng 5,000,000; Số dư cuối kỳ giảm 5,000,000; Số dư đầu kỳ không đổi', 'Chân bảng tăng 1 bút toán']),
    C('Lập phiếu xuất hàng thì số tăng đúng', 'P0', NEN + '\nKH-TEST có hợp đồng bán hàng còn hàng chờ xuất.',
      ['1. Vào ' + MENU_PX + ', lập và hạch toán phiếu xuất hàng cho KH-TEST, ngày 16/10/2026', '2. Quay lại sổ chi tiết'], '',
      ['Có thêm dòng số phiếu xuất ghi nợ (đối ứng 5111, 33311); nếu có giảm giá thì thêm dòng ghi có (đối ứng 5213 / 5211)', 'Tổng phát sinh nợ tăng đúng giá trị phiếu (gồm thuế); Số dư cuối kỳ tăng tương ứng']),
    C('Chứng từ có ngày hạch toán sau Đến ngày không lên sổ', 'P1', NEN, ['1. Lập phiếu thu cho KH-TEST ngày 05/11/2026, hạch toán', '2. Xem sổ kỳ 01/01/2026 - 31/10/2026', '3. Đổi Đến ngày thành 30/11/2026'], '',
      ['Bước 2: số không đổi', 'Bước 3: có dòng phiếu thu ngày 05/11/2026']),
    C('Chứng từ chưa hạch toán không lên sổ', 'P1', NEN, ['1. Lập phiếu thu cho KH-TEST nhưng chưa hạch toán', '2. Xem lại sổ'], '', ['Không có dòng phiếu thu đó; số không đổi']),
]

# ================================================================== IV. XUẤT DANH SÁCH EXCEL
XL = [
    C('Xuất Excel khi thiếu ô bắt buộc', 'P0', 'Đang mở màn, chưa chọn Khách hàng.', ['1. Bấm Xuất Excel'], '',
      ['Thông báo "' + MSG + '"', 'Không tải file; ô thiếu viền đỏ']),
    C('Xuất Excel thành công', 'P0', BL, ['1. Bấm Xuất Excel', '2. Quan sát nút và thông báo'], '',
      ['Không có cửa sổ chọn cột, tải ngay', 'Trong lúc xuất nút bị khóa, cạnh nút hiện tiến độ ("Đang chuẩn bị dữ liệu…", "Đang dựng file … dòng…")',
       'Thông báo "Xuất Excel thành công"; file tên "so_chi_tiet_cong_no_kh.xlsx"']),
    C('Cấu trúc file', 'P1', BL, ['1. Xuất Excel', '2. Mở file'], '',
      ['Sheet "So chi tiet cong no KH"; dòng tiêu đề "SỔ CHI TIẾT CÔNG NỢ PHẢI THU KHÁCH HÀNG", ngay dưới "Từ ngày 01/01/2026 đến ngày 31/10/2026"',
       'Hàng tên cột: STT, Đơn hàng/Hợp đồng, Ngày hạch toán, Số chứng từ, NVKD, Phòng ban, Ghi chú, Phát sinh nợ, Phát sinh có, Tài khoản đối ứng, Tên tài khoản đối ứng',
       '3 dòng tổng (nhãn ở cột Ghi chú) đứng trước bút toán; cuối file có "Ngày ..., tháng ..., năm ..." và "Người lập"']),
    C('Xuất lấy mọi trang', 'P0', BL + ' Đang ở trang 1, 10 dòng/trang.', ['1. Xuất Excel', '2. Đếm số dòng bút toán'], '',
      ['File có đủ 73 bút toán (STT 1–73), không chỉ 10 dòng trang đang xem', '3 dòng tổng trong file bằng trên màn']),
    C('Xuất theo bộ lọc đã áp', 'P0', BL, ['1. Gõ "PXH" ô tìm nhanh, nhấn Enter', '2. Xuất Excel'], '',
      ['File chỉ có 31 bút toán khớp "PXH"', 'Dòng tổng trong file bằng dòng tổng trên màn sau lọc']),
    C('Xuất mẫu Ngoại tệ', 'P1', 'Đang xem KH-USD, Loại tiền Ngoại tệ.', ['1. Xuất Excel', '2. Mở file'], '',
      ['Có thêm các cột: Loại tiền, Số phát sinh ngoại tệ (Nợ, Có), Tỷ giá, Số phát sinh VNĐ (Nợ, Có)', 'Số nguyên tệ có tối đa 2 số lẻ']),
    C('Xuất khi không có bút toán', 'P2', 'Đang lọc ra "' + KND + '"', ['1. Xuất Excel', '2. Mở file'], '',
      ['Vẫn tải file, không báo lỗi', 'File có tiêu đề, hàng tên cột, 3 dòng tổng; không có dòng bút toán']),
    C('Định dạng số và tiếng Việt trong file', 'P1', BL, ['1. Mở file', '2. Bấm vào 1 ô số tiền, xem thanh công thức', '3. Chọn cả cột Phát sinh nợ, xem tổng ở thanh trạng thái'], '',
      ['Ô số tiền là kiểu SỐ, hiển thị 1,234,567, không cảnh báo "số lưu dạng chữ"', 'Tổng cột nợ = Tổng phát sinh nợ + Số dư đầu kỳ (nếu đầu kỳ ghi cột nợ) + Số dư cuối kỳ (nếu ghi cột nợ) — vì 3 dòng tổng cũng nằm trong cột', 'Ngày dạng dd/mm/yyyy; tiếng Việt có dấu hiển thị đúng']),
    C('Bấm Xuất Excel liên tục', 'P2', BL, ['1. Bấm Xuất Excel 3 lần thật nhanh'], '', ['Chỉ tải 1 file (nút khóa trong lúc đang xuất)']),
]

# ================================================================== V. IN BÁO CÁO
IN = [
    C('In khi thiếu ô bắt buộc', 'P0', 'Đang mở màn, chưa chọn Tài khoản.', ['1. Bấm In'], '', ['Thông báo "' + MSG + '"', 'Không mở cửa sổ xem trước']),
    C('Mở cửa sổ xem trước bản in', 'P0', BL, ['1. Bấm In'], '',
      ['Cửa sổ "Xem trước sổ chi tiết công nợ phải thu khách hàng" có nút In, nút x',
       'Bản in khổ ngang: tiêu đề công ty của người in, "SỔ CHI TIẾT CÔNG NỢ PHẢI THU KHÁCH HÀNG"',
       'Khối thông tin: Công ty : Tất cả; Phòng ban : Tất cả; Khách hàng : 14TQUPCA-2 - CÔNG TY CỔ PHẦN CƠ KHÍ GIAO THÔNG QUẢNG NINH; Tài khoản : 131 - Phải thu của khách hàng; Loại tiền : VNĐ; Thời gian : Từ 01/01/2026 đến 31/10/2026']),
    C('Nội dung bảng in', 'P0', BL, ['1. Bấm In', '2. Cuộn bản xem trước đến cuối'], '',
      ['Cùng cột với màn hình; 3 dòng tổng in đậm ở đầu', 'Có đủ 73 bút toán (mọi trang)', 'Cuối bản in: "Ngày … tháng … năm …" (ngày in), chỗ ký Người lập, Kế toán trưởng (Ký, họ tên)']),
    C('In theo bộ lọc đã áp', 'P0', BL, ['1. Chọn Phòng ban PHÒNG THIẾT BỊ Ô TÔ 2', '2. Bấm In'], '', ['Khối thông tin Phòng ban : PHÒNG THIẾT BỊ Ô TÔ 2', 'Chỉ in bút toán đang thấy trên màn']),
    C('In mẫu Ngoại tệ', 'P2', 'Đang xem KH-USD, Loại tiền Ngoại tệ.', ['1. Bấm In'], '', ['Loại tiền : Ngoại tệ; bảng in đủ 15 cột như màn hình']),
    C('In quá 2.000 bút toán', 'P1', 'Khách hàng có hơn 2.000 bút toán trong kỳ.', ['1. Bấm In'], '',
      ['Cửa sổ chỉ hiện: "Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài."', 'Không in được']),
    C('Bấm In trong cửa sổ và đóng', 'P2', 'Đang mở cửa sổ xem trước.', ['1. Bấm In', '2. Hủy hộp in của trình duyệt', '3. Bấm x'], '',
      ['Bước 1: mở hộp in của trình duyệt với đúng nội dung xem trước', 'Bước 3: cửa sổ đóng, màn giữ nguyên bộ lọc, trang']),
]

# ================================================================== VI. RÀNG BUỘC
RB = [
    C('Liên kết số hợp đồng mở hợp đồng', 'P1', BL, ['1. Bấm HĐ_TPE_HN_KD2_25_0672_FQN ở dòng 1'], '',
      ['Mở tab mới màn chi tiết hợp đồng đó', 'Sổ chi tiết giữ nguyên']),
    C('Liên kết số chứng từ mở chứng từ', 'P1', BL, ['1. Bấm PXH-16319', '2. Bấm TPE.PKT0226.00052'], '',
      ['Bước 1: tab mới mở phiếu xuất hàng PXH-16319', 'Bước 2: tab mới mở phiếu kế toán TPE.PKT0226.00052', 'Loại chứng từ chưa có màn: số hiện chữ thường, không bấm được']),
    C('Màn dùng chung khung với Sổ chi tiết công nợ NCC / NV', 'P2', 'Có quyền 2 màn Sổ chi tiết công nợ phải trả nhà cung cấp và Sổ chi tiết công nợ nhân viên.', ['1. Mở 2 màn đó', '2. So bố cục 3 dòng tổng, cột phát sinh, In, Xuất Excel'], '',
      ['Cùng cách tính Số dư đầu kỳ / Tổng phát sinh / Số dư cuối kỳ và cùng khuôn In / Excel']),
    C('Sửa hạch toán chứng từ thì sổ cập nhật', 'P1', NEN + '\nCó phiếu kế toán bù trừ công nợ của KH-TEST chưa khóa sổ.', ['1. Vào ' + MENU_PKT + ', sửa số tiền phiếu kế toán đó tăng 1,000,000, hạch toán lại', '2. Tải lại sổ chi tiết'], '',
      ['Dòng của phiếu kế toán hiện số mới', 'Tổng phát sinh và Số dư cuối kỳ thay đổi đúng 1,000,000']),
    C('Phiếu nhập hàng trả lại ghi có công nợ', 'P1', NEN, ['1. Vào ' + MENU_NH + ', lập và hạch toán phiếu nhập hàng khách KH-TEST trả lại', '2. Tải lại sổ'], '',
      ['Có thêm dòng số phiếu nhập ghi có', 'Số dư cuối kỳ giảm đúng giá trị phiếu']),
    C('Phiếu chi trả lại tiền khách ghi nợ', 'P2', NEN, ['1. Vào ' + MENU_PC + ', lập và hạch toán phiếu chi trả lại tiền cho KH-TEST 500,000', '2. Tải lại sổ'], '',
      ['Có thêm dòng phiếu chi ghi nợ 500,000', 'Số dư cuối kỳ tăng 500,000']),
]

# ================================================================== VII. PHÂN QUYỀN
PQ = [
    C('Quyền mức Tổng công ty', 'P0', 'TK-TCT có quyền "%s" mức Tổng công ty; khách hàng KH-TEST có bút toán ở công ty A và B.' % QN, ['1. ' + MENU, '2. ' + LOC], '',
      ['Thấy mục menu, mở được màn', 'Có ô Công ty', 'Thấy bút toán của cả công ty A và B']),
    C('Quyền mức Công ty', 'P0', 'TK-CT có quyền mức Công ty, đang làm việc công ty A; KH-TEST có bút toán ở công ty A và B.', ['1. Đăng nhập TK-CT', '2. ' + MENU, '3. ' + LOC], '',
      ['Không có ô Công ty', 'Chỉ thấy bút toán ghi cho công ty A', '3 dòng tổng chỉ tính bút toán công ty A']),
    C('Mức Công ty thấy thêm hợp đồng do mình tạo', 'P0', 'NV-A quyền mức Công ty, làm việc công ty A, là người tạo hợp đồng HD-B có bút toán ghi cho công ty B.', ['1. Đăng nhập NV-A', '2. Lọc khách hàng của HD-B'], '',
      ['Thấy bút toán công ty A và bút toán của HD-B (công ty B)', 'Không thấy bút toán công ty B của hợp đồng người khác tạo']),
    C('Không có quyền thì ẩn menu', 'P0', 'TK-KQ không có quyền "%s".' % QN, ['1. Đăng nhập TK-KQ', '2. Mở phân hệ Tài chính > Kế toán công nợ > Khách hàng'], '',
      ['Không có mục "Sổ chi tiết công nợ phải thu khách hàng"']),
    C('Mở đường dẫn trực tiếp khi không có quyền', 'P0', 'TK-KQ biết đường dẫn màn.', ['1. Đăng nhập TK-KQ', '2. Dán đường dẫn màn vào thanh địa chỉ, nhấn Enter', '3. Thử chọn bộ lọc, bấm In, Xuất Excel'], 'Đường dẫn: <địa chỉ hệ thống>/finance/customer-ledger-details',
      ['Hệ thống báo "Bạn không có quyền thực hiện thao tác này"', 'Không có số liệu; In, Xuất Excel không ra kết quả', 'Không hiện ô Công ty']),
    C('Bấm mã khách hàng ở Bảng cân đối khi không có quyền Sổ chi tiết', 'P1', 'TK-X có quyền Bảng cân đối phát sinh công nợ khách hàng nhưng không có quyền "%s".' % QN, ['1. Vào ' + MENU_CD + ', lọc có số liệu', '2. Bấm mã một khách hàng'], '',
      ['Tab mới mở màn Sổ chi tiết nhưng báo không có quyền, không có số liệu']),
    C('Đổi quyền trong lúc đang xem', 'P1', 'TK-TCT đang xem sổ có bút toán công ty A và B.', ['1. Quản trị đổi quyền TK-TCT sang mức Công ty (công ty A)', '2. Ở màn đang mở, bấm Tìm kiếm', '3. Nhấn F5, lọc lại'], '',
      ['Bước 2: chỉ còn bút toán trong phạm vi mức Công ty', 'Bước 3: ô Công ty biến mất', 'Không lúc nào hiện số ngoài phạm vi mới']),
    C('Đổi công ty đang làm việc', 'P1', 'TK-CT quyền mức Công ty ở cả công ty A và B.', ['1. Đang làm việc công ty A, xem sổ KH-TEST', '2. Đổi sang công ty B, xem lại'], '',
      ['Sau khi đổi: chỉ thấy bút toán công ty B (và hợp đồng do mình tạo)', 'Không còn bút toán công ty A']),
    C('Người có 2 vai trò khác mức', 'P2', 'TK-Y có 1 vai trò mức Công ty và 1 vai trò mức Tổng công ty.', ['1. Đăng nhập TK-Y', '2. Mở màn, lọc KH-TEST'], '',
      ['Áp mức lớn hơn (Tổng công ty): có ô Công ty, thấy mọi công ty']),
    C('Phạm vi áp cho In và Excel', 'P1', 'TK-CT quyền mức Công ty.', ['1. Lọc KH-TEST', '2. Bấm In, Xuất Excel'], '',
      ['Bản in ghi Công ty : Tất cả nhưng chỉ có bút toán trong phạm vi quyền', 'File Excel cùng số dòng và dòng tổng như màn']),
]

GROUPS = [
    ('HIỂN THỊ TRANG & TRUY CẬP', G1),
    ('TÌM KIẾM & LỌC DANH SÁCH', TK),
    ('SỐ LIỆU BÁO CÁO', SL),
    ('XUẤT DANH SÁCH EXCEL', XL),
    ('IN BÁO CÁO', IN),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', RB),
    ('PHÂN QUYỀN', PQ),
]
SECTIONS = sections(GROUPS)

if __name__ == '__main__':
    ids = [(s[0], c[0]) for s in SECTIONS for c in s[2]]
    assert len(ids) == len(set(ids))
    txt = '\n'.join(str(x) for s in SECTIONS for c in s[2] for x in c) + '\n'.join(v for _, v in DESCRIPTION_BLOCK)
    BANNED = [r"`[a-z_]{3,}`", r"\bBE\b", r"\bFE\b", r"\bHTTP\b", r"\b(400|403|404|422)\b", r"localStorage", r"\bAPI\b", r"\bERP\b",
              r"[←-⇿☀-➿\U0001F300-\U0001FAFF]"]
    found = {p: len(re.findall(p, txt)) for p in BANNED if re.findall(p, txt)}
    print('!!! CON THUAT NGU:', found) if found else print('OK - sach')
    print(dem(GROUPS))
    p0 = sum(1 for _, cs in GROUPS for c in cs if c[1] == 'P0')
    print('P0: %d/%d = %.0f%%' % (p0, sum(len(c) for _, c in GROUPS), 100.0 * p0 / sum(len(c) for _, c in GROUPS)))
    build_chuan(OUT, 'Trang tính1', TEN, MODULE, DESCRIPTION_BLOCK, SECTIONS, loai='bao_cao')

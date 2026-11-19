# -*- coding: utf-8 -*-
"""Testcase "Sổ chi tiết công nợ nhân viên" — KHUÔN CHUẨN tab "13. DM quốc gia" (skill testcase-documenter, loại bao_cao).

Sinh bằng `assets/tc_chuan.build_chuan` (tự gọi check_tc — phải 0 lỗi). Câu chữ bám TC_MAU_QUOC_GIA.xlsx; độ phủ theo tab
"Testcase" của CHECKLIST_TC_SRS.xlsx (dòng không áp dụng: thêm / sửa / xoá / khoá / lịch sử / import / sắp xếp theo cột /
tùy chỉnh cột / popup chi tiết — màn chỉ đọc, không có các chức năng này).
Hành vi bám code develop 18/11/2026 (xem gen_srs.py) + quan sát dev-hrm (hdsd_shots/_log.txt).
Chạy: python gen_testcase.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HRM_CFG = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(HRM_CFG, '.claude', 'skills', 'testcase-documenter', 'assets'))
from tc_chuan import build_chuan  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

NGAY = '18/11/2026'
TEN = 'Sổ chi tiết công nợ nhân viên'
MODULE = 'Sổ chi tiết công nợ NV'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)

ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
QUYEN = 'Xem sổ chi tiết công nợ nhân viên'
MENU = 'Vào phân hệ Tài chính > menu Kế toán công nợ > nhóm Nhân viên > bấm "Sổ chi tiết công nợ nhân viên"'
LOC = 'Chọn Tài khoản "141 - Tạm ứng", Thời gian 01/01/2026 - 31/10/2026'
LOC_NV = LOC + ', Nhân viên NV-X'
LN = 'Chọn tài khoản và thời gian để xem sổ chi tiết.'
THIEU = 'Vui lòng chọn tài khoản và thời gian'
KQ403 = 'Bạn không có quyền thực hiện thao tác này'
TRAN = ('Danh sách có 2,599 dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, '
        'trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.')
SA = 'Tài khoản TK-TCT (quyền "%s" mức Tổng công ty).' % QUYEN
NEN = 'Đã ghi lại 3 dòng tổng của sổ TK 141 - NV-X kỳ 01/11/2026 - 30/11/2026 (Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ).'
MENU_PC = 'Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu chi'
MENU_PT = 'Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu thu'
MENU_PKT = 'Tài chính > Sổ tổng hợp > Sổ tổng hợp > Phiếu kế toán'
MENU_BCD = 'Tài chính > Kế toán công nợ > Nhân viên > Bảng cân đối phát sinh công nợ nhân viên'


def _lines(x):
    if x is None:
        return []
    return [x] if isinstance(x, str) else list(x)


def _exp(x):
    out = []
    for s in _lines(x):
        s = s.strip()
        if s.startswith('- '):
            s = s[2:].strip()
        out.append('-  ' + s)
    return '\n'.join(out)


def _d(x):
    # khoảng ngày "dd/mm/yyyy - dd/mm/yyyy" viết thành "dd/mm/yyyy đến dd/mm/yyyy" (dấu " - " bị bộ kiểm coi là gạch đầu dòng)
    return re.sub(r'(\d{2}/\d{2}/\d{4}) - (\d{2}/\d{2}/\d{4})', lambda m: m.group(1) + ' đến ' + m.group(2), x)


def C(func, prio, pre, steps, data, exp):
    assert prio in ('P0', 'P1', 'P2'), func
    pre, steps, data, exp = ([_d(v) for v in _lines(x)] for x in (pre, steps, data, exp))
    return (func, prio, '\n'.join(_lines(pre)), '\n'.join(_lines(steps)), '\n'.join(_lines(data)), _exp(exp))


def sections(groups):
    return [(ROMAN[i], t, [('%03d' % (k + 1),) + c for k, c in enumerate(cs)]) for i, (t, cs) in enumerate(groups)]


def L_(*lines):
    return '\n'.join(lines)


DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Báo cáo chỉ đọc: sổ chi tiết từng bút toán của 1 tài khoản theo dõi công nợ gắn với nhân viên (vd 141 Tạm ứng) trong kỳ, '
        'kèm Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ.',
        'Chức năng: Xem sổ (mẫu VNĐ / Ngoại tệ), Tìm kiếm / lọc, In, Xuất Excel.',
        'Đường vào: ' + MENU + '; hoặc bấm số liệu ở màn Bảng cân đối phát sinh công nợ nhân viên.',
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Bút toán ghi sổ của tài khoản đã chọn và các tài khoản con trực tiếp (vd 141 gồm 1411, 1412), có ngày hạch toán trong kỳ, '
        'thuộc phạm vi quyền, khớp mọi ô lọc — KỂ CẢ bút toán không gắn nhân viên (cột Nhân viên trống).',
        'Bảng: 3 dòng tổng (Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ) -> các dòng bút toán.',
        'Mẫu VNĐ 11 cột: STT | Đơn hàng/Hợp đồng | Ngày hạch toán | Số chứng từ | Nhân viên | Phòng ban | Ghi chú | Phát sinh nợ | '
        'Phát sinh có | Tài khoản đối ứng (Tài khoản, Tên tài khoản).',
        'Mẫu Ngoại tệ 15 cột: thay Phát sinh nợ / có bằng Loại tiền | Số phát sinh ngoại tệ (Nợ, Có) | Tỷ giá | Số phát sinh VNĐ (Nợ, Có).',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '-  Bút toán của tài khoản cấp cháu (vd tài khoản con của 1411): không lấy.',
        '-  Bút toán có ngày hạch toán ngoài kỳ: không thành dòng (trước Từ ngày chỉ vào Số dư đầu kỳ).',
        '-  Số dư đầu kỳ KHÔNG tính bút toán không gắn nhân viên.',
        '-  Người có quyền mức Công ty: không thấy bút toán không gắn nhân viên và bút toán của nhân viên công ty khác (trừ bút toán gắn chính mình).',
        '-  Chứng từ chưa hạch toán (chưa ghi sổ): không có bút toán nên không lên sổ.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô Thời gian (bắt buộc) lọc theo NGÀY HẠCH TOÁN của bút toán, tính cả 2 đầu mút (Đến ngày tính tới 23:59:59).',
        'Trước Từ ngày = đầu kỳ (chỉ vào dòng Số dư đầu kỳ). Mặc định trống; F5 / Làm mới về trống.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Không phân cấp. 3 dòng tổng luôn ở đầu bảng (mọi trang), sau đó bút toán xếp theo ngày hạch toán tăng dần, cùng ngày theo thời điểm tạo.',
        'Phân trang theo bút toán, mặc định 10 dòng (10 / 20 / 50 / 100). Không sắp xếp theo cột, không tùy chỉnh cột.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '-  Mỗi bút toán 1 dòng (1 chứng từ có nhiều bút toán thì nhiều dòng cùng số chứng từ).',
        '-  Cột Tài khoản đối ứng gộp mọi đối ứng của bút toán, không trùng, cách nhau dấu phẩy.',
        '-  Mẫu Ngoại tệ: dòng Tổng phát sinh tách theo loại tiền, mỗi loại 1 dòng số ròng (Nợ - Có).',
    )),
    ('7. Phân quyền cấp', L_(
        'Một quyền "%s" — mức: Tổng công ty / Công ty.' % QUYEN,
        '-  Mức Tổng công ty: mọi bút toán; có ô Công ty, Phòng ban, Bộ phận, Nhân viên.',
        '-  Mức Công ty: bút toán có nhân viên thuộc công ty đang làm việc + bút toán gắn chính mình; không có ô Công ty.',
        '-  Không có quyền: menu vẫn hiện, mở màn báo "%s", không xem / in / xuất được.' % KQ403,
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Số dư đầu kỳ = Tổng Nợ - Tổng Có (VNĐ) trước Từ ngày, chỉ bút toán có nhân viên, cùng phạm vi + ô lọc. Dương ghi cột Nợ, âm ghi cột Có.',
        'Tổng phát sinh = Tổng Nợ, Tổng Có (VNĐ) của mọi bút toán trong kỳ (cả các trang).',
        'Số dư cuối kỳ = Số dư đầu kỳ + Tổng Nợ - Tổng Có, làm tròn 2 số lẻ.',
        'Chân bảng "Hiển thị a–b / N bút toán": N = số bút toán trong kỳ theo bộ lọc.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        '-  Số dạng 1,234,567.89; dòng bút toán 0 đồng vẫn in "0", dòng tổng bằng 0 để trống.',
        '-  Lưu ý: không lọc Nhân viên mà tài khoản có bút toán không gắn nhân viên thì Số dư cuối kỳ kỳ này KHÁC Số dư đầu kỳ của kỳ liền sau — không phải lỗi.',
        '-  Lưu ý: ô Loại chứng từ chọn bất kỳ mục "Phiếu xuất hàng - …" đều ra MỌI phiếu xuất hàng (tương tự "Phiếu nhập hàng - …").',
        '-  Ô Mẫu chỉ đổi cột hiển thị, không tải lại. Ô Số tiền bằng 0 bị bỏ qua.',
        'Dữ liệu mẫu: TK-TCT (mức Tổng công ty), TK-CT (mức Công ty, công ty A), TK-KQ (không quyền), NV-X (nhân viên công ty A có tạm ứng), '
        'NV-Y (nhân viên công ty B). Số liệu mẫu đọc trên môi trường thử 18/11/2026: TK 141, kỳ 01/01/2026 - 31/10/2026 có 2,599 bút toán; '
        'Nhân viên Võ Cát Hào có 116 bút toán, Số dư đầu kỳ Có 14,582,880, Tổng phát sinh Có 33,798,960, Số dư cuối kỳ Có 48,381,840.',
    )),
]

# ================================================================== I. HIỂN THỊ TRANG & TRUY CẬP
G1 = [
    C('Mở màn hình từ menu', 'P0', SA, ['1. Đăng nhập', '2. ' + MENU], '',
      ['Tiêu đề trang và tiêu đề bảng "Sổ chi tiết công nợ nhân viên"; cạnh tiêu đề trang có icon (i)',
       'Bảng hiện "' + LN + '", chưa tải số liệu',
       'Nhóm Nhân viên có 3 mục: Sổ chi tiết công nợ nhân viên, Bảng cân đối phát sinh công nợ nhân viên, Báo cáo hạn mức công nợ nhân viên']),
    C('Nội dung icon (i) cạnh tiêu đề trang', 'P2', 'Đang mở màn.', ['1. Rê chuột vào icon (i) cạnh tiêu đề trang'], '',
      ['Hiện: "Sổ chi tiết từng bút toán của một tài khoản theo dõi công nợ gắn với nhân viên: số dư đầu kỳ, phát sinh Nợ / Có trong kỳ, '
       'số dư cuối kỳ. Quyền xem theo tổng công ty hoặc công ty (công ty: nhân viên công ty mình và sổ của chính mình)."']),
    C('Bố cục khu vực lọc và các nút chức năng', 'P1', SA, ['1. Mở màn', '2. Quan sát khung "Bộ lọc danh sách" và hàng nút trên bảng'], '',
      ['Ô tìm nhanh gợi ý "Tìm theo số chứng từ hoặc số hợp đồng"; nút Tìm kiếm, Làm mới, Cài đặt bộ lọc, Ẩn tìm kiếm nâng cao',
       'Các ô: Công ty, Phòng ban, Bộ phận, Nhân viên, Tài khoản *, Thời gian *, Tài khoản đối ứng, Đơn hàng/Hợp đồng, Loại chứng từ, Số chứng từ, '
       'Ghi chú, Loại tiền, Mẫu (mặc định VNĐ), Khách hàng, Chỉ tiêu, Mã vụ việc, Số tiền',
       'Trên bảng: nút In đứng trước nút Xuất Excel; không có nút Thêm / Sửa / Xóa, không có nút cấu hình cột']),
    C('Các cột mặc định của mẫu VNĐ', 'P0', 'Đang mở màn, Mẫu = VNĐ.', ['1. Đọc tiêu đề bảng từ trái sang phải'], '',
      ['STT | Đơn hàng/Hợp đồng | Ngày hạch toán | Số chứng từ | Nhân viên | Phòng ban | Ghi chú | Phát sinh nợ | Phát sinh có | '
       'Tài khoản đối ứng (2 cột con Tài khoản, Tên tài khoản)', 'Không có cột ẩn, không có cột ngoại tệ']),
    C('Các cột của mẫu Ngoại tệ', 'P0', 'Đã chọn bộ lọc có số liệu.', ['1. ' + LOC, '2. Chọn ô Mẫu = Ngoại tệ', '3. Đọc tiêu đề bảng'], 'Mẫu: Ngoại tệ',
      ['Sau cột Ghi chú là: Loại tiền | Số phát sinh ngoại tệ (Nợ, Có) | Tỷ giá | Số phát sinh VNĐ (Nợ, Có) | Tài khoản đối ứng (Tài khoản, Tên tài khoản)',
       'Bảng đổi cột ngay, KHÔNG hiện "Đang tải dữ liệu...", 3 dòng tổng và số bút toán không đổi']),
    C('Bảng có số liệu: 3 dòng tổng và dòng bút toán', 'P0', SA, ['1. ' + LOC], '',
      ['3 dòng đầu nền xám chữ đậm: "Số dư đầu kỳ", "Tổng phát sinh", "Số dư cuối kỳ" (nhãn căn phải, gộp 7 cột đầu)',
       'Dưới là các dòng bút toán STT 1, 2, 3…; Ngày hạch toán dạng dd/mm/yyyy',
       'Tiêu đề bảng 2 tầng, dính khi cuộn dọc',
       'Môi trường thử: chân bảng "Hiển thị 1–10 / 2,599 bút toán"']),
    C('Tài khoản không có bút toán trong kỳ', 'P1', 'Tài khoản "3388 - Phải trả, phải nộp khác" không có bút toán trong 01/11/2026 - 15/11/2026.',
      ['1. Chọn Tài khoản 3388, Thời gian 01/11/2026 - 15/11/2026'], '',
      ['Vẫn hiện 3 dòng tổng (Số dư đầu kỳ nếu có, Tổng phát sinh trống)', 'Dưới là "Không có dữ liệu phù hợp bộ lọc."',
       'Không có chân bảng và thanh phân trang; màn không báo lỗi']),
    C('Không có dữ liệu khớp bộ lọc', 'P1', 'Đã chọn bộ lọc, bảng có dữ liệu.', ['1. ' + LOC, '2. Gõ "ZZZ999" vào ô tìm nhanh, nhấn Enter'], 'Từ khóa: ZZZ999',
      ['Hiện "Không có dữ liệu phù hợp bộ lọc."', 'Tổng phát sinh trống; Số dư cuối kỳ = Số dư đầu kỳ', 'Không có chân bảng và thanh phân trang']),
    C('Thứ tự mặc định của dòng bút toán', 'P1', 'TK 141 có nhiều bút toán cùng ngày hạch toán.', ['1. ' + LOC, '2. Đọc cột Ngày hạch toán từ trên xuống'], '',
      ['Ngày hạch toán tăng dần', 'Cùng ngày: bút toán tạo trước đứng trước (vd 23/01/2026: TPV_HTCXCH_01225 rồi TPV_HTCXCH_01226 khi lọc Nhân viên Võ Cát Hào)']),
    C('Số dòng mặc định mỗi trang và đổi số dòng', 'P0', SA, ['1. ' + LOC, '2. Đọc ô "Số dòng/trang"', '3. Sang trang 2', '4. Đổi "Số dòng/trang" sang 50'], '',
      ['Bước 2: mặc định 10, lựa chọn 10 / 20 / 50 / 100; trang 1 có 10 bút toán', 'Bước 4: về trang 1, hiện 50 bút toán, chân bảng "Hiển thị 1–50 / 2,599 bút toán"',
       '3 dòng tổng không đổi']),
    C('Nút sang trang kế tiếp và lùi về trang trước', 'P0', SA, ['1. ' + LOC, '2. Bấm ›', '3. Bấm ‹'], '',
      ['Bước 2: sang trang 2, chân bảng "Hiển thị 11–20 / 2,599 bút toán", STT bắt đầu từ 11', 'Bước 3: về trang 1 "Hiển thị 1–10 / 2,599 bút toán"',
       'Bút toán giữa các trang không lặp, không thiếu']),
    C('Nút về trang cuối và trang đầu, trạng thái nút', 'P1', SA, ['1. ' + LOC + ', quan sát « và ‹ ở trang 1', '2. Bấm », quan sát › và »', '3. Bấm «'], '',
      ['Trang 1: « và ‹ mờ, bấm không có tác dụng', 'Trang cuối (260): chân bảng "Hiển thị 2,591–2,599 / 2,599 bút toán"; › và » mờ', 'Bước 3: về trang 1']),
    C('Chuyển trang không làm đổi 3 dòng tổng', 'P0', SA, ['1. ' + LOC + ', ghi lại 3 dòng tổng', '2. Sang trang 5, rồi trang cuối', '3. Đổi Số dòng/trang = 100'], '',
      ['3 dòng tổng giữ nguyên ở mọi trang, đúng như bước 1']),
    C('Đổi bộ lọc khi đang ở trang giữa thì về trang 1', 'P0', SA, ['1. ' + LOC + ', sang trang 3', '2. Chọn ô Chỉ tiêu = Có'], '',
      ['Bảng về trang 1 theo kết quả lọc mới', 'Chân bảng tính lại N, 3 dòng tổng tính lại']),
    C('Các cột không cho sắp xếp', 'P2', 'Bảng có dữ liệu.', ['1. ' + LOC, '2. Bấm vào tiêu đề từng cột'], '',
      ['Tiêu đề không có mũi tên sắp xếp', 'Thứ tự dòng không đổi (luôn theo ngày hạch toán)']),
    C('Thời gian tải khi không lọc thêm', 'P1', SA, ['1. Chọn Tài khoản 141, Thời gian 01/01/2026 - 31/10/2026, đo thời gian đến khi bảng hiện', '2. Chọn Tài khoản 131 cùng kỳ, đo lại'], '',
      ['Bước 1: dưới 2 giây (môi trường thử ~0,9 giây, 2,599 bút toán)', 'Bước 2: dưới 10 giây (môi trường thử ~6 giây, 68,866 bút toán); trong lúc chờ hiện "Đang tải dữ liệu..."']),
    C('Đường chữ dài tự xuống dòng', 'P2', 'Có bút toán ghi chú dài (vd phiếu báo có "Tiền về USD ngân hàng MB Công ty ngày 28/10/2025").',
      ['1. Chọn Tài khoản 131, Thời gian 01/01/2026 - 31/10/2026, Loại tiền USD', '2. Quan sát cột Ghi chú'], '',
      ['Ghi chú dài xuống dòng trong ô, không đẩy bảng giãn ngang vô hạn', 'Số tiền không bị xuống dòng giữa chừng']),
    C('Phiên đăng nhập hết hạn', 'P2', 'Đang mở màn, phiên đăng nhập đã hết hạn.', ['1. Đổi một ô lọc'], '',
      ['Hệ thống đưa về màn đăng nhập, không hiện số liệu']),
]

# ================================================================== II. TÌM KIẾM & LỌC DANH SÁCH
G2 = [
    C('Bấm Tìm kiếm khi chưa chọn ô bắt buộc', 'P0', SA, ['1. Mở màn, không chọn gì', '2. Bấm Tìm kiếm'], '',
      ['Dưới ô Tài khoản: "Vui lòng chọn tài khoản"; dưới ô Thời gian: "Vui lòng chọn thời gian" (chữ đỏ, viền đỏ)', 'Bảng vẫn là lời nhắc, không tải dữ liệu']),
    C('Chữ đỏ tự tắt khi đã chọn', 'P1', 'Đang có chữ đỏ dưới 2 ô bắt buộc.', ['1. Chọn Tài khoản 141', '2. Chọn Thời gian 01/01/2026 - 31/10/2026'], '',
      ['Bước 1: chữ đỏ ô Tài khoản tắt, ô Thời gian vẫn đỏ', 'Bước 2: hết chữ đỏ, bảng tự tải số liệu (không cần bấm Tìm kiếm)']),
    C('Bấm Tìm kiếm khi khung lọc đang thu gọn', 'P2', 'Khung lọc đang thu gọn (đã bấm Ẩn tìm kiếm nâng cao), chưa chọn Tài khoản.', ['1. Bấm Tìm kiếm'], '',
      ['Khung lọc tự mở ra, thấy chữ đỏ dưới ô bắt buộc']),
    C('Chọn Thời gian ngược chiều', 'P1', 'Đang mở màn.', ['1. Ở ô Thời gian chọn Từ ngày 31/10/2026', '2. Mở lịch Đến ngày, chọn 01/01/2026'], '',
      ['Lịch Đến ngày khóa các ngày trước 31/10/2026, không chọn được; ô Đến ngày giữ trống', 'Không tải dữ liệu']),
    C('Lọc theo Tài khoản lấy cả tài khoản con trực tiếp', 'P0', 'TK 141 có tài khoản con 1411, 1412; có bút toán ghi vào 1411 trong kỳ.',
      ['1. Chọn Tài khoản 1411, kỳ 01/01/2026 - 31/10/2026, ghi N1', '2. Chọn Tài khoản 1412, ghi N2', '3. Chọn Tài khoản 141, ghi N'], '',
      ['N = N1 + N2 + số bút toán ghi thẳng vào 141', 'Bút toán của tài khoản cấp cháu (con của 1411, nếu có) KHÔNG xuất hiện khi chọn 141']),
    C('Ô Tài khoản chỉ có tài khoản theo dõi công nợ đang hoạt động', 'P1', SA, ['1. Mở ô Tài khoản, cuộn danh sách', '2. Gõ "141"'], '',
      ['Hiển thị "Số hiệu - Tên" (vd "141 - Tạm ứng"); không có tài khoản không theo dõi công nợ (vd 511) hay tài khoản đã khóa', 'Bước 2: lọc còn 141, 1411, 1412']),
    C('Lọc theo khoảng thời gian tính cả 2 đầu mút', 'P0', 'Có bút toán NV-X ngày hạch toán 05/01/2026 và 31/01/2026.',
      ['1. Chọn Tài khoản 141, Thời gian 05/01/2026 - 31/01/2026, Nhân viên NV-X'], '',
      ['Có cả bút toán ngày 05/01/2026 và 31/01/2026 (kể cả bút toán hạch toán lúc 23:00 ngày 31/01/2026)', 'Không có bút toán ngày 04/01 hay 01/02']),
    C('Lọc theo Công ty', 'P0', SA, ['1. ' + LOC, '2. Chọn Công ty B'], 'Công ty: B',
      ['Chỉ còn bút toán có nhân viên thuộc công ty B; bút toán không gắn nhân viên biến mất', 'Ô Phòng ban chỉ còn phòng ban công ty B']),
    C('Đổi Công ty thì xóa Phòng ban, Bộ phận, Nhân viên', 'P1', SA, ['1. Chọn Công ty A, Phòng ban P1, Nhân viên NV-X', '2. Đổi Công ty sang B'], '',
      ['Ô Phòng ban, Bộ phận, Nhân viên về trống; bảng tải lại theo công ty B']),
    C('Lọc theo Phòng ban / Bộ phận', 'P1', SA, ['1. ' + LOC, '2. Chọn Phòng ban "Kinh doanh CN Vinh"', '3. Chọn thêm Bộ phận'], '',
      ['Bước 2: cột Phòng ban mọi dòng là "Kinh doanh CN Vinh"', 'Bước 3: thu hẹp tiếp theo bộ phận; 3 dòng tổng tính lại']),
    C('Lọc theo Nhân viên', 'P0', SA, ['1. ' + LOC, '2. Chọn Nhân viên Võ Cát Hào'], 'Nhân viên: Võ Cát Hào',
      ['Mọi dòng có cột Nhân viên "Võ Cát Hào"', 'Môi trường thử: "Hiển thị 1–10 / 116 bút toán"; Số dư đầu kỳ Có 14,582,880; Tổng phát sinh Có 33,798,960; Số dư cuối kỳ Có 48,381,840']),
    C('Ô Nhân viên tìm được nhân viên đã nghỉ', 'P1', 'Nhân viên NV-NGHI đã nghỉ việc, có bút toán tạm ứng năm 2026.', ['1. Mở ô Nhân viên, gõ tên NV-NGHI'], '',
      ['Icon khóa cạnh nhãn Nhân viên đang bật sẵn (hiện cả nhân viên đã nghỉ)', 'Tìm thấy NV-NGHI, chọn được và sổ ra bút toán của NV-NGHI']),
    C('Lọc theo Tài khoản đối ứng', 'P1', SA, ['1. ' + LOC, '2. Chọn Tài khoản đối ứng 3311'], 'Tài khoản đối ứng: 3311',
      ['Mọi dòng có 3311 trong cột Tài khoản đối ứng', 'Bút toán có nhiều đối ứng vẫn hiện đủ (vd "3311, 1111")', 'Số dư đầu kỳ cũng chỉ tính bút toán có đối ứng 3311']),
    C('Lọc theo Đơn hàng/Hợp đồng gần đúng', 'P1', 'Tài khoản 131 có bút toán gắn hợp đồng.',
      ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026', '2. Gõ một phần số hợp đồng vào ô Đơn hàng/Hợp đồng, chưa nhấn Enter', '3. Nhấn Enter'], 'Đơn hàng/Hợp đồng: _26_',
      ['Bước 2: bảng chưa đổi', 'Bước 3: còn bút toán có số hợp đồng chứa "_26_" (ký tự _ hiểu đúng là ký tự gạch dưới)']),
    C('Lọc theo Loại chứng từ một loại', 'P0', SA, ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026', '2. Ô Loại chứng từ chọn "Phiếu báo có"'], '',
      ['Ô có 16 lựa chọn: 5 mục "Phiếu xuất hàng - …", Phiếu xuất bán hàng mượn, 5 mục "Phiếu nhập hàng - …", Phiếu thu, Phiếu chi, Phiếu ủy nhiệm chi, Phiếu báo có, Phiếu kế toán',
       'Bước 2: chỉ còn bút toán của phiếu báo có (số chứng từ dạng …PBC…); 3 dòng tổng tính lại']),
    C('Lọc theo nhiều Loại chứng từ', 'P1', SA, ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026', '2. Chọn "Phiếu báo có" và "Phiếu kế toán"'], '',
      ['Ra bút toán của CẢ 2 loại (HOẶC); số bút toán = tổng khi lọc riêng từng loại']),
    C('Mục "Phiếu xuất hàng - …" không phân biệt loại con', 'P1', 'Tài khoản 131 có bút toán phiếu xuất hàng trong kỳ.',
      ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026, Loại chứng từ "Phiếu xuất hàng - Xuất bán", ghi N1', '2. Đổi sang "Phiếu xuất hàng - Xuất khuyến mại", ghi N2'], '',
      ['N1 = N2 = mọi phiếu xuất hàng của tài khoản trong kỳ', 'Lưu ý: hành vi đã chốt giữ nguyên, không phải lỗi; tương tự các mục "Phiếu nhập hàng - …"']),
    C('Lọc theo Số chứng từ gần đúng', 'P1', SA, ['1. ' + LOC, '2. Gõ "HTCXCH_0116" vào ô Số chứng từ, nhấn Enter'], '',
      ['Chỉ còn bút toán có số chứng từ chứa "HTCXCH_0116" (vd TPV_HTCXCH_01164, TPV_HTCXCH_01167)']),
    C('Lọc theo Ghi chú', 'P1', 'Tài khoản 131 có phiếu báo có ghi chú "Tiền về USD ngân hàng MB…".',
      ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026', '2. Gõ "ngân hàng MB" vào ô Ghi chú, nhấn Enter'], '',
      ['Chỉ còn bút toán có ghi chú chứa "ngân hàng MB"', 'Lưu ý: chỉ tìm được ghi chú của phiếu xuất hàng, phiếu nhập hàng, phiếu thu, phiếu ủy nhiệm chi, phiếu báo có']),
    C('Lọc theo Loại tiền', 'P1', SA, ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026', '2. Chọn Loại tiền USD'], '',
      ['Môi trường thử: còn 16 bút toán, mọi dòng là USD', 'Ở mẫu VNĐ cột Phát sinh nợ / có là số VNĐ quy đổi']),
    C('Lọc theo Khách hàng', 'P1', 'Tài khoản 131 có bút toán gắn hợp đồng của khách hàng KH-A.',
      ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026', '2. Ở ô Khách hàng gõ 1 ký tự', '3. Gõ thêm ký tự thứ 2, chọn KH-A'], '',
      ['Bước 2: chưa hiện danh sách gợi ý', 'Bước 3: chỉ còn bút toán thuộc hợp đồng của KH-A; bấm × xóa thì bảng về như trước']),
    C('Lọc theo Chỉ tiêu Nợ / Có', 'P0', SA, ['1. ' + LOC_NV, '2. Chọn Chỉ tiêu = Nợ', '3. Đổi Chỉ tiêu = Có'], '',
      ['Bước 2: chỉ còn bút toán có số ở cột Phát sinh nợ; Tổng phát sinh chỉ có Nợ', 'Bước 3: chỉ còn bút toán ở cột Phát sinh có; Số dư đầu kỳ cũng chỉ tính phần Có']),
    C('Lọc theo Mã vụ việc', 'P2', 'Có bút toán gắn vụ việc "BX - Bốc xếp".', ['1. ' + LOC, '2. Chọn Mã vụ việc "BX - Bốc xếp"'], '',
      ['Lựa chọn hiển thị dạng "Mã - Tên"', 'Chỉ còn bút toán gắn vụ việc đó']),
    C('Lọc theo khoảng Số tiền', 'P0', SA, ['1. ' + LOC_NV, '2. Ô Số tiền nhập từ 300,000 đến 450,000, nhấn Enter'], 'Từ: 300,000\nĐến: 450,000',
      ['Ô tự định dạng 300,000 / 450,000', 'Chỉ còn bút toán có số tiền VNĐ từ 300,000 đến 450,000 (vd 313,560; 439,920; 383,760), gồm cả bút toán đúng bằng 2 đầu mút']),
    C('Ô Số tiền bằng 0 bị bỏ qua', 'P2', SA, ['1. ' + LOC, '2. Ô Số tiền từ nhập 0, nhấn Enter'], '', ['Kết quả như khi để trống ô Số tiền']),
    C('Đổi ô Mẫu không tải lại dữ liệu', 'P1', 'Đang xem sổ có số liệu, đứng ở trang 3.', ['1. Đổi Mẫu sang Ngoại tệ', '2. Đổi lại VNĐ', '3. Bấm × xóa ô Mẫu'], '',
      ['Bước 1-2: chỉ đổi cột, giữ trang 3, không hiện "Đang tải dữ liệu..."', 'Bước 3: bảng hiển thị như mẫu VNĐ']),
    C('Tìm nhanh theo số chứng từ hoặc số hợp đồng', 'P0', SA, ['1. ' + LOC, '2. Gõ "HTCXK" vào ô tìm nhanh, nhấn Enter'], 'Từ khóa: HTCXK',
      ['Còn bút toán có số chứng từ HOẶC số hợp đồng chứa "HTCXK" (môi trường thử: 158 bút toán)', '3 dòng tổng tính lại theo từ khóa', 'Bảng về trang 1']),
    C('Tìm nhanh không phân biệt chữ hoa chữ thường', 'P1', SA, ['1. ' + LOC, '2. Tìm "htcxk", ghi kết quả', '3. Tìm "HTCXK"'], '', ['Hai lần ra cùng kết quả']),
    C('Tìm nhanh có khoảng trắng đầu cuối', 'P2', SA, ['1. ' + LOC, '2. Tìm "  HTCXK  "'], '', ['Kết quả như tìm "HTCXK"']),
    C('Tìm nhanh với ký tự đặc biệt', 'P2', SA, ['1. ' + LOC, '2. Lần lượt tìm các chuỗi ở Test data'], ['%', "' OR 1=1 --", '<b>abc</b>'],
      ['% hiểu là ký tự thường: "Không có dữ liệu phù hợp bộ lọc." nếu không có số chứng từ chứa %', 'Không báo lỗi hệ thống, không hiện chữ in đậm']),
    C('Tìm nhanh chuỗi rất dài', 'P2', SA, ['1. ' + LOC, '2. Dán chuỗi 500 ký tự vào ô tìm nhanh, nhấn Enter'], 'Chuỗi "abcde" lặp 100 lần',
      ['Ô nhận đủ chuỗi, bảng hiện "Không có dữ liệu phù hợp bộ lọc.", màn không treo']),
    C('Xóa từ khóa thì danh sách về đầy đủ', 'P1', 'Đang tìm nhanh "HTCXK".', ['1. Xóa hết ô tìm nhanh', '2. Nhấn Enter'], '',
      ['Bước 1: bảng chưa đổi', 'Bước 2: về 2,599 bút toán như trước khi tìm']),
    C('Lọc kết hợp nhiều ô', 'P0', SA, ['1. ' + LOC, '2. Chọn Nhân viên Võ Cát Hào, Chỉ tiêu Có, Tài khoản đối ứng 3311, gõ "HTCXCH" ở ô tìm nhanh, nhấn Enter'], '',
      ['Mọi dòng thỏa ĐỒNG THỜI các điều kiện', 'Chân bảng và 3 dòng tổng tính theo kết quả đã lọc']),
    C('Bấm Làm mới', 'P0', 'Đang lọc nhiều ô, Mẫu = Ngoại tệ.', ['1. Bấm Làm mới'], '',
      ['Mọi ô về trống, Mẫu về VNĐ, không còn chữ đỏ', 'Bảng hiện "' + LN + '"']),
    C('Cài đặt bộ lọc', 'P2', 'Đang mở màn.', ['1. Bấm Cài đặt bộ lọc', '2. Bỏ tích "Mã vụ việc", bấm Lưu', '3. Mở lại, bấm Khôi phục mặc định'], '',
      ['Cửa sổ "Cài đặt bộ lọc" liệt kê 14 mục (Công ty / Phòng ban / Bộ phận / Nhân viên, Tài khoản, Thời gian, …, Số tiền), đều tích sẵn',
       'Bước 2: ô Mã vụ việc ẩn khỏi khung lọc', 'Bước 3: ô hiện lại']),
    C('Rời màn rồi quay lại trong 10 phút thì giữ bộ lọc', 'P1', 'Đang xem sổ đã lọc.', ['1. ' + LOC_NV, '2. Vào màn Bảng cân đối phát sinh công nợ nhân viên', '3. Quay lại sổ chi tiết bằng menu'], '',
      ['Bộ lọc giữ nguyên và tự tải số liệu như bước 1']),
    C('Tải lại trang (F5) khi đang lọc', 'P1', 'Đang xem sổ đã lọc.', ['1. ' + LOC, '2. Nhấn F5'], '',
      ['Mọi ô về mặc định (Mẫu VNĐ), bảng hiện lời nhắc, không tự tải số liệu']),
    C('Mở ở tab mới khi tab cũ đang lọc', 'P2', 'Tab 1 đang xem sổ đã lọc.', ['1. Trong 10 phút, mở tab mới, vào màn bằng menu', '2. Quay lại tab 1'], '',
      ['Tab 2 mở với đúng bộ lọc tab 1 và tự tải số liệu', 'Tab 1 giữ nguyên']),
    C('Đăng xuất, đăng nhập tài khoản khác trên cùng trình duyệt', 'P1', 'Có 2 tài khoản TK-TCT và TK-CT.',
      ['1. Đăng nhập TK-TCT, ' + LOC[0].lower() + LOC[1:], '2. Đăng xuất', '3. Đăng nhập TK-CT, mở màn'], '',
      ['TK-CT thấy bộ lọc trống, bảng hiện lời nhắc', 'Không thấy bộ lọc / số liệu của TK-TCT']),
]

# ================================================================== III. SỐ LIỆU BÁO CÁO
G3 = [
    C('Số dư cuối kỳ = đầu kỳ + Nợ - Có', 'P0', SA, ['1. ' + LOC + ', Nhân viên Võ Cát Hào', '2. Đọc 3 dòng tổng'], '',
      ['Số dư cuối kỳ = Số dư đầu kỳ + Tổng Nợ - Tổng Có', 'Môi trường thử: đầu kỳ dư Có 14,582,880 + phát sinh Có 33,798,960 = cuối kỳ dư Có 48,381,840 (ghi ở cột Phát sinh có)']),
    C('Tổng phát sinh bằng tổng mọi trang', 'P0', SA, ['1. ' + LOC_NV, '2. Đổi Số dòng/trang = 100, cộng cột Phát sinh nợ, Phát sinh có qua mọi trang (hoặc cộng trong file Excel)'], '',
      ['Tổng cột Phát sinh nợ = Tổng phát sinh Nợ; tổng cột Phát sinh có = Tổng phát sinh Có']),
    C('Số dư âm ghi ở cột Có, dương ghi ở cột Nợ', 'P0', 'NV-X có tạm ứng còn dư Nợ; tài khoản 141 tổng (không lọc NV) dư Có.',
      ['1. ' + LOC_NV + ', đọc Số dư đầu kỳ', '2. Bỏ ô Nhân viên, đọc lại'], '',
      ['Dư Nợ: số nằm ở cột Phát sinh nợ, cột Có trống', 'Dư Có: số dương (bỏ dấu) nằm ở cột Phát sinh có, cột Nợ trống', 'Số dư bằng 0: cả 2 ô trống']),
    C('Số dư đầu kỳ chỉ tính bút toán có nhân viên', 'P0', 'TK 1388 có bút toán trước 01/07/2026 KHÔNG gắn nhân viên (vd TPV.PKT0626.00005).',
      ['1. Chọn Tài khoản 1388, kỳ 01/01/2026 - 30/06/2026, ghi Số dư cuối kỳ (A)', '2. Đổi kỳ 01/07/2026 - 31/10/2026, ghi Số dư đầu kỳ (B)'], '',
      ['Bước 1: các bút toán phiếu kế toán không gắn nhân viên có trong dòng và Tổng phát sinh', 'Bước 2: B KHÁC A — B bỏ phần bút toán không gắn nhân viên',
       'Lưu ý: đây là quy tắc đã chốt, không phải lỗi']),
    C('Số dư đầu kỳ nối tiếp khi lọc theo nhân viên', 'P1', 'NV-X có bút toán tạm ứng năm 2026.',
      ['1. ' + LOC_NV.replace('31/10/2026', '30/06/2026') + ', ghi Số dư cuối kỳ', '2. Đổi kỳ 01/07/2026 - 31/10/2026, ghi Số dư đầu kỳ'], '',
      ['Số dư đầu kỳ bước 2 = Số dư cuối kỳ bước 1 (cùng nhân viên)']),
    C('Cột Phát sinh nợ / có theo chiều ghi sổ', 'P0', 'NV-X có 1 phiếu chi tạm ứng và 1 phiếu thu hoàn ứng trong kỳ.', ['1. ' + LOC_NV], '',
      ['Bút toán phiếu chi tạm ứng: số ở cột Phát sinh nợ', 'Bút toán phiếu thu hoàn ứng: số ở cột Phát sinh có', 'Mỗi dòng chỉ có số ở 1 trong 2 cột']),
    C('Bút toán 0 đồng hiện "0"', 'P2', 'Có bút toán 0 đồng ghi Nợ trong kỳ.', ['1. Lọc tới bút toán đó'], '',
      ['Cột Phát sinh nợ hiện "0", cột Phát sinh có trống']),
    C('Định dạng số', 'P1', 'Mẫu Ngoại tệ, TK 131, Loại tiền USD.', ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026, Loại tiền USD, Mẫu Ngoại tệ', '2. Đọc các cột số'], '',
      ['Số dạng 1,234,567.89, có phẩy ngăn hàng nghìn, tối đa 2 số lẻ (vd 1,007,419.5; 4,658,722.68)', 'Không có dấu "-" ở dòng tổng (âm chuyển sang cột Có)']),
    C('Mẫu Ngoại tệ: cột nguyên tệ và tỷ giá', 'P0', 'TK 131 có phiếu báo có USD TPE.PBC0126.00046: 11,000 USD, tỷ giá 26,145.',
      ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026, Loại tiền USD, Mẫu Ngoại tệ', '2. Đọc dòng TPE.PBC0126.00046'], '',
      ['Loại tiền "USD"; Số phát sinh ngoại tệ Có 11,000; Tỷ giá 26,145; Số phát sinh VNĐ Có 287,595,000', 'Bút toán VNĐ (nếu bỏ lọc Loại tiền) để trống 2 cột ngoại tệ']),
    C('Mẫu Ngoại tệ: Tổng phát sinh theo từng loại tiền', 'P0', 'TK 131 có bút toán VNĐ và USD trong kỳ.',
      ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026, Mẫu Ngoại tệ (không lọc Loại tiền)'], '',
      ['Có 2 dòng "Tổng phát sinh": 1 dòng VNĐ (trống phần ngoại tệ), 1 dòng USD',
       'Mỗi dòng ghi số ròng: Nợ - Có dương ở cột Nợ, âm ở cột Có (môi trường thử khi lọc USD: Có 37,639,432.17 USD, quy đổi 976,381,619,156)']),
    C('Mẫu VNĐ và Ngoại tệ cùng số dư', 'P1', SA, ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026, ghi Số dư đầu kỳ / cuối kỳ ở mẫu VNĐ', '2. Đổi Mẫu Ngoại tệ'], '',
      ['Số dư đầu kỳ, Số dư cuối kỳ giống nhau ở 2 mẫu; số bút toán giống nhau']),
    C('Cột Tài khoản đối ứng', 'P1', 'Có bút toán có 2 tài khoản đối ứng.', ['1. Lọc tới bút toán đó'], '',
      ['Cột Tài khoản: 2 số hiệu cách nhau ", "; cột Tên tài khoản: 2 tên tương ứng cùng thứ tự']),
    C('Cột Ghi chú theo loại chứng từ', 'P2', SA, ['1. Chọn Tài khoản 131 kỳ 01/01/2026 - 31/10/2026', '2. So cột Ghi chú của phiếu báo có và phiếu kế toán'], '',
      ['Phiếu báo có hiện ghi chú của phiếu', 'Phiếu kế toán, phiếu chi để trống cột Ghi chú']),
    C('Mở chứng từ từ cột Số chứng từ', 'P1', SA, ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026', '2. Bấm số chứng từ TPE.PBC0126.00046', '3. Lọc TK 141, quan sát số TPV_HTCXCH_01164'], '',
      ['Bước 2: mở màn chi tiết phiếu báo có ở tab mới; tab sổ giữ nguyên', 'Bước 3: số chứng từ hạch toán chi phí vận chuyển hiện chữ thường, không bấm được']),
    C('Mở hợp đồng từ cột Đơn hàng/Hợp đồng', 'P2', 'Có bút toán gắn hợp đồng bán hàng.', ['1. Bấm số hợp đồng dạng liên kết'], '',
      ['Mở màn hợp đồng ở tab mới; loại hợp đồng chưa có màn xem thì hiện chữ thường']),
    C('Lập phiếu chi tạm ứng thì sổ tăng phát sinh Nợ', 'P0', NEN,
      ['1. ' + MENU_PC + ': lập phiếu chi tạm ứng cho NV-X 5,000,000, ngày 10/11/2026, hạch toán Nợ 141 / Có 1111 (lưu, duyệt cho tới khi được ghi sổ)',
       '2. Mở lại sổ: Tài khoản 141, Thời gian 01/11/2026 - 30/11/2026, Nhân viên NV-X'], 'Số tiền: 5,000,000',
      ['Có dòng mới: Ngày hạch toán 10/11/2026, số phiếu chi, Nhân viên NV-X, Phát sinh nợ 5,000,000, Tài khoản đối ứng 1111',
       'Tổng phát sinh Nợ tăng 5,000,000; Số dư cuối kỳ tăng 5,000,000 về phía Nợ; Số dư đầu kỳ không đổi']),
    C('Lập phiếu thu hoàn ứng thì sổ tăng phát sinh Có', 'P0', NEN,
      ['1. ' + MENU_PT + ': lập phiếu thu hoàn ứng của NV-X 2,000,000, ngày 12/11/2026, Có 141 (cho tới khi được ghi sổ)', '2. Mở lại sổ như trên'], 'Số tiền: 2,000,000',
      ['Có dòng mới ở cột Phát sinh có 2,000,000', 'Tổng phát sinh Có tăng 2,000,000; Số dư cuối kỳ giảm 2,000,000']),
    C('Chứng từ chưa ghi sổ không lên sổ', 'P1', NEN, ['1. Lập phiếu chi tạm ứng cho NV-X nhưng chỉ lưu nháp, chưa duyệt / ghi sổ', '2. Mở lại sổ'], '',
      ['Không có dòng mới, 3 dòng tổng không đổi']),
    C('Chứng từ ngày trước kỳ chỉ vào Số dư đầu kỳ', 'P1', NEN, ['1. ' + MENU_PKT + ': lập phiếu kế toán ghi Nợ 141 cho NV-X 1,000,000, ngày hạch toán 20/10/2026, ghi sổ', '2. Mở lại sổ kỳ 01/11/2026 - 30/11/2026'], '',
      ['Không có dòng mới trong bảng', 'Số dư đầu kỳ và Số dư cuối kỳ cùng tăng 1,000,000 về phía Nợ']),
]

# ================================================================== IV. XUẤT DANH SÁCH EXCEL
FILE = 'so_chi_tiet_cong_no_nhan_vien.xlsx'
G4 = [
    C('Xuất Excel khi chưa chọn đủ ô bắt buộc', 'P0', 'Mở màn, chưa chọn Tài khoản.', ['1. Bấm Xuất Excel'], '',
      ['Thông báo "' + THIEU + '"', 'Hiện chữ đỏ dưới ô Tài khoản, Thời gian; không tải file']),
    C('Xuất Excel thành công', 'P0', SA, ['1. ' + LOC_NV, '2. Bấm Xuất Excel'], '',
      ['Không có cửa sổ chọn trường; cạnh nút hiện tiến độ ("Đang chuẩn bị dữ liệu…", "Đã tải x/y dòng…", "Đang dựng file n dòng…") rồi tải file',
       'Thông báo "Xuất Excel thành công"', 'Tên file "' + FILE + '", mở được bằng Excel']),
    C('Cấu trúc file mẫu VNĐ', 'P0', 'Đã xuất file ở case trước.', ['1. Mở file'], '',
      ['Sheet "So chi tiet cong no NV"; dòng 1 ảnh tiêu đề công ty; dòng 2 "SỔ CHI TIẾT CÔNG NỢ NHÂN VIÊN (TỪ NGÀY 01/01/2026 ĐẾN NGÀY 31/10/2026)"',
       'Hàng tên cột: STT, Đơn hàng/Hợp đồng, Ngày hạch toán, Số chứng từ, NVKD, Phòng ban, Ghi chú, Phát sinh nợ, Phát sinh có, Tài khoản đối ứng, Tên tài khoản đối ứng',
       'Tiếp theo 3 dòng "Số dư đầu kỳ", "Tổng phát sinh", "Số dư cuối kỳ" (nhãn ở cột Ghi chú), rồi bút toán',
       'Cuối file: "Ngày ..., tháng ..., năm ...", "Người lập", "(Ký, họ tên)"']),
    C('Cấu trúc file mẫu Ngoại tệ', 'P1', SA, ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026, Loại tiền USD, Mẫu Ngoại tệ', '2. Xuất Excel, mở file'], '',
      ['Hàng tên cột thêm: Loại tiền, Số phát sinh ngoại tệ - Nợ, Số phát sinh ngoại tệ - Có, Tỷ giá, Số phát sinh VNĐ - Nợ, Số phát sinh VNĐ - Có',
       'Dòng Tổng phát sinh tách theo loại tiền như trên màn']),
    C('File lấy tất cả các trang', 'P0', SA, ['1. ' + LOC_NV + ', để 10 dòng/trang, đứng ở trang 1', '2. Xuất Excel, đếm số bút toán trong file'], '',
      ['File có đủ 116 bút toán (bằng N ở chân bảng), STT từ 1 đến 116']),
    C('File khớp số liệu trên màn', 'P0', 'Đã xuất file sổ NV Võ Cát Hào.', ['1. So 3 dòng tổng và 10 dòng đầu trong file với màn'], '',
      ['Số dư đầu kỳ Có 14,582,880; Tổng phát sinh Có 33,798,960; Số dư cuối kỳ Có 48,381,840 — khớp màn', '10 dòng đầu trùng số chứng từ, ngày, số tiền với trang 1']),
    C('Xuất theo bộ lọc và từ khóa tìm nhanh', 'P1', SA, ['1. ' + LOC + ', tìm nhanh "HTCXK", nhấn Enter', '2. Xuất Excel'], '',
      ['File chỉ có 158 bút toán khớp từ khóa; 3 dòng tổng khớp màn']),
    C('Ô gõ dở chưa bấm Tìm kiếm không vào file', 'P1', 'Đang xem sổ TK 141.', ['1. Gõ "XYZ" vào ô Số chứng từ, KHÔNG nhấn Enter', '2. Bấm Xuất Excel'], '',
      ['File theo bộ lọc của lần tìm gần nhất (chưa có "XYZ"), không phải bộ lọc đang gõ dở']),
    C('Xuất khi không có bút toán', 'P2', 'Bộ lọc cho ra "Không có dữ liệu phù hợp bộ lọc.".', ['1. Bấm Xuất Excel', '2. Mở file'], '',
      ['Vẫn tải file có tiêu đề, hàng tên cột và 3 dòng tổng (không có dòng bút toán)']),
    C('Định dạng số, ngày, tiếng Việt trong file', 'P1', 'Đã xuất file.', ['1. Bấm 1 ô số tiền, xem thanh công thức', '2. Chọn cả cột Phát sinh có, xem tổng ở thanh trạng thái', '3. Đọc cột NVKD, Phòng ban, Tên tài khoản đối ứng'], '',
      ['Ô số là kiểu SỐ, hiển thị 1,234,567, Excel cộng được', 'Ngày hạch toán dạng dd/mm/yyyy', 'Tiếng Việt có dấu hiển thị đúng']),
    C('Xuất sổ lớn không giới hạn dòng', 'P1', SA, ['1. ' + LOC + ' (2,599 bút toán)', '2. Bấm Xuất Excel, bấm thêm lần nữa khi đang xuất'], '',
      ['Tiến độ chạy qua nhiều lô "Đã tải x/2,602 dòng…"; nút Xuất Excel khóa trong lúc xuất, bấm lần 2 không tải thêm file', 'File đủ 2,599 bút toán + 3 dòng tổng']),
]

# ================================================================== V. IN BÁO CÁO
G5 = [
    C('In khi chưa chọn đủ ô bắt buộc', 'P0', 'Mở màn, chưa chọn gì.', ['1. Bấm In'], '',
      ['Thông báo "' + THIEU + '", không mở cửa sổ xem trước']),
    C('Mở cửa sổ xem trước bản in', 'P0', SA, ['1. ' + LOC_NV, '2. Bấm In'], '',
      ['Cửa sổ "Xem trước sổ chi tiết công nợ nhân viên" có nút In và ×', 'Tiêu đề công ty của người xem, tên "SỔ CHI TIẾT CÔNG NỢ NHÂN VIÊN"',
       'Khối thông tin: Công ty "Tất cả", Phòng ban "Tất cả", Tài khoản "141 - Tạm ứng", Mẫu "VNĐ", Thời gian "Từ 01/01/2026 đến 31/10/2026"']),
    C('Bảng trên bản in khớp màn hình', 'P0', 'Đang mở bản xem trước ở case trước.', ['1. So bảng in với màn'], '',
      ['Cột như màn mẫu VNĐ, cột nhân viên ghi "NVKD"', '3 dòng tổng ngay dưới tiêu đề, chữ đậm, khớp màn', 'Đủ 116 bút toán (mọi trang), không chỉ trang đang xem',
       'Cuối bản in: "Ngày dd tháng mm năm yyyy" (ngày in), khối ký Người lập, Kế toán trưởng không đóng khung']),
    C('In mẫu Ngoại tệ', 'P1', SA, ['1. Chọn Tài khoản 131, kỳ 01/01/2026 - 31/10/2026, Loại tiền USD, Mẫu Ngoại tệ', '2. Bấm In'], '',
      ['Khối thông tin Mẫu "Ngoại tệ"; bảng 15 cột, tiêu đề 2 tầng Số phát sinh ngoại tệ / Số phát sinh VNĐ / Tài khoản đối ứng']),
    C('Vượt mức 2.000 dòng thì không in', 'P0', SA, ['1. ' + LOC + ' (2,599 bút toán)', '2. Bấm In'], '',
      ['Cửa sổ chỉ hiện: "' + TRAN + '"', 'Không có nút In trong cửa sổ']),
    C('In ra máy in và đóng cửa sổ', 'P2', 'Đang mở bản xem trước có dữ liệu.', ['1. Bấm In trong cửa sổ', '2. Bấm ×'], '',
      ['Bước 1: mở hộp thoại in của trình duyệt, khổ ngang', 'Bước 2: cửa sổ đóng, màn sổ giữ nguyên bộ lọc và trang']),
]

# ================================================================== VI. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
G6 = [
    C('Mở sổ chi tiết từ Bảng cân đối phát sinh công nợ nhân viên', 'P0', SA,
      ['1. ' + MENU_BCD + ': chọn Tài khoản 141, kỳ 01/01/2026 - 31/10/2026', '2. Bấm số liệu ở dòng nhân viên Võ Cát Hào để mở sổ chi tiết'], '',
      ['Sổ chi tiết mở với Tài khoản 141, Thời gian 01/01/2026 - 31/10/2026, Nhân viên Võ Cát Hào và tự tải số liệu',
       'Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ khớp dòng của nhân viên đó trên Bảng cân đối']),
    C('Link từ Bảng cân đối thắng bộ lọc đã nhớ', 'P1', 'Trong 10 phút trước đã xem sổ chi tiết với Nhân viên NV-Y.',
      ['1. Từ Bảng cân đối bấm số liệu của nhân viên NV-X'], '',
      ['Sổ mở theo NV-X, KHÔNG còn NV-Y hay các ô lọc cũ']),
    C('Link từ Bảng cân đối giữ đủ Công ty, Phòng ban, Nhân viên', 'P1', 'Bảng cân đối đang lọc Công ty A, Phòng ban P1.', ['1. Bấm số liệu của NV-X (thuộc P1)'], '',
      ['Sổ mở có Công ty A, Phòng ban P1, Nhân viên NV-X — ô Nhân viên không bị tự xóa', 'Số liệu chỉ của NV-X, không cộng cả phòng ban']),
    C('Sửa tay đường dẫn có ngày ngược chiều', 'P2', 'Đang mở sổ bằng link từ Bảng cân đối.', ['1. Sửa tay trên thanh địa chỉ cho Đến ngày nhỏ hơn Từ ngày, nhấn Enter'], '',
      ['Báo "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", không hiện số liệu, màn không lỗi']),
    C('Cùng nhân viên, Sổ chi tiết và Bảng cân đối ra cùng số', 'P0', SA, ['1. Xem Bảng cân đối TK 141 kỳ 01/01/2026 - 31/10/2026, ghi số của NV-X', '2. Xem sổ chi tiết cùng điều kiện, Nhân viên NV-X'], '',
      ['Đầu kỳ, phát sinh Nợ / Có, cuối kỳ của 2 màn bằng nhau']),
]

# ================================================================== VII. PHÂN QUYỀN
G7 = [
    C('Quyền mức Tổng công ty thấy mọi công ty', 'P0', SA, ['1. Đăng nhập TK-TCT', '2. ' + MENU, '3. ' + LOC], '',
      ['Có đủ ô Công ty, Phòng ban, Bộ phận, Nhân viên', 'Thấy bút toán của nhân viên mọi công ty và bút toán không gắn nhân viên (môi trường thử 2,599 bút toán)']),
    C('Quyền mức Công ty chỉ thấy nhân viên công ty mình', 'P0', 'TK-CT có quyền "%s" mức Công ty, đang làm việc ở công ty A.' % QUYEN,
      ['1. Đăng nhập TK-CT', '2. ' + MENU, '3. ' + LOC], '',
      ['Không có ô Công ty; có ô Phòng ban, Bộ phận, Nhân viên', 'Chỉ bút toán có nhân viên thuộc công ty A', 'KHÔNG thấy bút toán không gắn nhân viên, không thấy NV-Y (công ty B)']),
    C('Quyền mức Công ty thấy bút toán của chính mình ở công ty khác', 'P0', 'TK-CT có bút toán tạm ứng ghi nhận ở công ty B.', ['1. Đăng nhập TK-CT', '2. ' + LOC + ', Nhân viên = chính TK-CT'], '',
      ['Thấy cả bút toán của chính mình ghi ở công ty B']),
    C('Đổi công ty đang làm việc thì phạm vi tính lại', 'P1', 'TK-CT có quyền mức Công ty ở cả công ty A và B.', ['1. Đăng nhập TK-CT ở công ty A, xem sổ, ghi N', '2. Đổi công ty đang làm việc sang B', '3. Mở lại sổ cùng bộ lọc'], '',
      ['Bước 3: số liệu theo nhân viên công ty B, không còn bút toán công ty A (trừ của chính mình)']),
    C('Có cả 2 mức thì áp mức Tổng công ty', 'P2', 'Tài khoản có quyền ở cả mức Công ty và Tổng công ty.', ['1. Đăng nhập', '2. ' + MENU, '3. ' + LOC], '',
      ['Ô lọc và số liệu giống TK-TCT']),
    C('Không có quyền thì không xem được sổ', 'P0', 'TK-KQ không có quyền "%s".' % QUYEN, ['1. Đăng nhập TK-KQ', '2. ' + MENU], '',
      ['Mục menu vẫn hiện, mở được màn', 'Thông báo "' + KQ403 + '"', 'Ô Tài khoản không có lựa chọn nào; không có ô Công ty']),
    C('Không có quyền thì In, Xuất Excel không lấy được dữ liệu', 'P0', 'TK-KQ không có quyền.', ['1. Đăng nhập TK-KQ, mở màn', '2. Bấm In', '3. Bấm Xuất Excel'], '',
      ['Báo "' + THIEU + '" (không chọn được Tài khoản), không mở bản in, không tải file']),
    C('Mở bằng đường dẫn trực tiếp khi không có quyền', 'P0', 'TK-KQ không có quyền; có link sổ chi tiết từ Bảng cân đối (đủ Tài khoản, Thời gian).', ['1. Đăng nhập TK-KQ', '2. Dán link vào thanh địa chỉ, nhấn Enter'], '',
      ['Báo "' + KQ403 + '"', 'Bảng không hiện số liệu nào']),
    C('Bị gỡ quyền trong lúc đang xem', 'P1', 'TK-CT đang xem sổ có số liệu.', ['1. Quản trị gỡ quyền "%s" của TK-CT' % QUYEN, '2. Ở màn đang mở, bấm Tìm kiếm', '3. Nhấn F5'], '',
      ['Bước 2: báo "' + KQ403 + '", không hiện số liệu mới', 'Bước 3: ô Tài khoản trống lựa chọn']),
    C('Phạm vi quyền áp cho cả Excel và bản In', 'P1', 'TK-CT mức Công ty, công ty A.', ['1. Đăng nhập TK-CT, ' + LOC[0].lower() + LOC[1:], '2. Xuất Excel', '3. Bấm In'], '',
      ['File và bản in chỉ có bút toán trong phạm vi công ty A; 3 dòng tổng khớp màn']),
]

GROUPS = [
    ('HIỂN THỊ TRANG & TRUY CẬP', G1),
    ('TÌM KIẾM & LỌC DANH SÁCH', G2),
    ('SỐ LIỆU BÁO CÁO', G3),
    ('XUẤT DANH SÁCH EXCEL', G4),
    ('IN BÁO CÁO', G5),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', G6),
    ('PHÂN QUYỀN', G7),
]

if __name__ == '__main__':
    build_chuan(OUT, 'Trang tính1', TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, sections(GROUPS), loai='bao_cao')
    print(' · '.join('%s %d' % (t, len(c)) for t, c in GROUPS), '· tổng', sum(len(c) for _, c in GROUPS))

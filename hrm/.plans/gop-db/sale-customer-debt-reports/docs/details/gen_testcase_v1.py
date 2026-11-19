# -*- coding: utf-8 -*-
"""Testcase "BC chi tiết công nợ KH" (HRM: phân hệ Bán hàng > Báo cáo > Báo cáo công nợ > Chi tiết công nợ KH).

Viết mới theo code HRM hiện tại (02/11/2026) — TC ERP cũ (erp/.plans/erp-bao-cao-cong-no-khach-hang/tc_chi_tiet.py)
chỉ tham khảo ý; luồng phát sinh theo khuôn `common.data_change_tcs`, chứng từ lập trên HRM (menu phân hệ Tài chính),
chứng từ chỉ có ở hệ thống cũ (hợp đồng bán hàng, phiếu xuất kho) ghi ở Tiền điều kiện "có sẵn".
Số liệu mẫu đọc trên dev 02/11/2026 (capture.js, hdsd_shots/_capture_log.json).
Chạy: python gen_testcase.py
"""
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _report_lib as R  # noqa: E402,F401  (đặt sys.path tới tc_engine)
from tc_engine import build  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

L = R.L
NGAY = L.NGAY
TEN = 'BC chi tiết công nợ KH'
MODULE = 'BC chi tiết công nợ KH'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
CNT = Counter()


def J(*lines):
    return '\n'.join(lines)


def T(grp, n, func, prio, pre, steps, data, exp):
    CNT[grp] += 1

    def j(x):
        return x if isinstance(x, str) else J(*x)
    return (n, func, prio, j(pre), j(steps), j(data), j(exp))


MENU = 'Vào phân hệ Bán hàng > Báo cáo > nhóm Báo cáo công nợ > bấm "Chi tiết công nợ KH"'
TC_ = 'phân hệ Tài chính > '
M = {
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
LOC = 'Thời gian = ngày 1 tháng này → hôm nay, Khách hàng = KH-TEST'
XEM = 'dòng hợp đồng HD-TEST-01, dòng khách hàng KH-TEST (chữ đậm) và dòng Tổng cộng'

DU_LIEU = J(
    'Dữ liệu mẫu dùng xuyên suốt:',
    '- TK-ALL: có quyền "Xem báo cáo chi tiết công nợ khách hàng theo tổng công ty".',
    '- TK-CTY: chỉ có quyền "... theo công ty" (Công ty A). TK-PB: chỉ quyền "... theo phòng ban", quản lý phòng PB-1.',
    '- TK-BP: chỉ quyền "... theo bộ phận", quản lý bộ phận BP-1. TK-NV: nhân viên PB-1, KHÔNG có quyền nào, là người tạo HD-TEST-01.',
    '- KH-TEST: khách hàng mới, chưa có công nợ. HD-TEST-01, HD-TEST-02: hợp đồng bán hàng của KH-TEST do TK-NV tạo, đã ký '
    '(hợp đồng bán hàng lập ở hệ thống cũ — có sẵn).',
    '- Mỗi chứng từ lập ở luồng phát sinh phải được HẠCH TOÁN (có ngày hạch toán) mới lên báo cáo.',
    '- Số mẫu trên dev (02/11/2026): kỳ 01/10/2026 → 31/10/2026, khách 89THUPTR-62 có 3 hợp đồng; dòng khách hàng: Số dư đầu kỳ '
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
        '- Dòng hợp đồng: mỗi cặp (khách hàng, hợp đồng) có bút toán đến hết Đến ngày — kể cả không phát sinh trong kỳ.',
        '- Chứng từ không gắn hợp đồng: 1 dòng, ô hợp đồng trống.',
        '- Dòng khách hàng (đậm): cộng mọi hợp đồng của khách (mọi trang).',
        '- Dòng Tổng cộng: tổng toàn bộ theo bộ lọc (xem mục 6).',
        'Chứng từ theo cột: Hàng hóa/Dịch vụ = phiếu xuất hàng, xuất bán hàng mượn, hạch toán dịch vụ, thanh lý, hạch toán dịch vụ BH-SC, '
        'khai báo công nợ đầu kỳ; ĐCCN = phiếu kế toán; Nhập trả lại = phiếu nhập hàng; Đã thanh toán = phiếu thu, phiếu báo có, '
        'khai báo công nợ đầu kỳ; Trả lại tiền thừa = phiếu chi, phiếu ủy nhiệm chi.',
    )),
    ('3. Đối tượng bị ẩn / không tính', J(
        '- Chứng từ chưa hạch toán (chưa duyệt / chưa ghi sổ).',
        '- Bút toán ngày hạch toán SAU Đến ngày.',
        '- Bút toán không gắn khách hàng: không lên dòng nào, nhưng VẪN tính vào Số dư đầu kỳ của dòng Tổng cộng.',
        '- Số liệu ngoài phạm vi quyền (mục 7).',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', J(
        'Ô Thời gian (bắt buộc, mặc định trống) lọc theo NGÀY HẠCH TOÁN: trước Từ ngày → Số dư đầu kỳ; Từ ngày → hết Đến ngày → phát sinh.',
        'Thiếu Thời gian: "Vui lòng chọn thời gian". Từ > Đến: "Đến ngày phải lớn hơn hoặc bằng Từ ngày." — bảng rỗng, không xuất Excel.',
        'Ghi nhớ bộ lọc 10 phút khi rời màn; tải lại trang (F5) thì xoá bộ lọc.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', J(
        'Tổng cộng → Khách hàng (STT 1, 2…) → Hợp đồng (STT 1.1, 1.2…). Phân trang theo dòng hợp đồng (10/20/50/100, mặc định 10); '
        'chân bảng "Hiển thị a–b / N dòng hợp đồng". STT khách nối tiếp sang trang sau.',
        'Phòng ban / Bộ phận / NVKD = của người tạo hợp đồng theo hồ sơ hiện tại.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', J(
        '- Dòng khách hàng = tổng các dòng hợp đồng của khách (kể cả ở trang khác).',
        '- Dòng Tổng cộng KHÔNG áp ô tìm nhanh và lọc Số dư cuối kỳ (Dư nợ / Dư có) ⇒ khi dùng 2 ô này Tổng cộng có thể khác tổng các dòng — đúng thiết kế.',
        '- Số dư đầu kỳ dòng Tổng cộng: khi lọc Số hợp đồng lấy mọi hợp đồng có số CHỨA chuỗi; các cột khác lấy ĐÚNG số hợp đồng.',
        '- Popup: mỗi chứng từ 1 dòng; tổng popup tính mọi trang.',
    )),
    ('7. Phân quyền cấp', J(
        'Ai cũng mở được màn. 4 quyền (nhóm "Báo cáo chi tiết công nợ khách hàng") chỉ quyết phạm vi:',
        '- Tổng công ty: toàn bộ; có ô Công ty, Phòng ban, Bộ phận, Nhân viên.',
        '- Công ty: công ty đang làm việc + hợp đồng mình tạo; có ô Phòng ban, Bộ phận, Nhân viên.',
        '- Phòng ban: các phòng mình quản lý + hợp đồng mình tạo. Bộ phận: các bộ phận mình quản lý + hợp đồng mình tạo (ô Bộ phận, Nhân viên).',
        '- Không quyền: chỉ hợp đồng mình tạo; không có ô Công ty / Phòng ban / Bộ phận / Nhân viên.',
        'Phạm vi áp cho cả dòng Tổng cộng (kể cả Số dư đầu kỳ), popup, Excel.',
    )),
    ('8. Cách tính các ô thống kê', J(
        'Hàng hóa/Dịch vụ = Nợ − Có (Có không tính khai báo công nợ đầu kỳ). Nhập trả lại = Có − Nợ. ĐCCN tăng = Nợ, ĐCCN giảm = Có của phiếu kế toán.',
        'Cộng tăng = HH/DV + ĐCCN tăng. Cộng giảm = Nhập trả lại + Đã thanh toán + ĐCCN giảm.',
        'Số dư cuối kỳ = Đầu kỳ + Cộng tăng − Cộng giảm + Trả lại tiền thừa.',
        'Định dạng 1,234,567, không lẻ. Số 0 để trống, trừ dòng Tổng cộng, cột Số dư cuối kỳ, cột ĐCCN giảm ở dòng hợp đồng (in 0).',
    )),
    ('9. Ghi chú đọc bảng', J(
        DU_LIEU,
        'Bẫy dễ sai:',
        '- Ô chọn lọc ngay; ô tìm nhanh và Số hợp đồng chỉ lọc khi Enter / Tìm kiếm. Số hợp đồng phải nhập ĐỦ.',
        '- Popup ĐCCN tăng có thêm khai báo đầu kỳ công nợ NCC và phiếu thu ghi Nợ; popup ĐCCN giảm có thêm phiếu thu ghi Có (giữ như hệ thống cũ).',
        '- Popup không áp ô tìm nhanh / Số dư cuối kỳ.',
    )),
]

# ------------------------------------------------------------------ I. PHÂN QUYỀN & PHẠM VI
ROLE_TCS = [
    T('Q', '00', 'Không có quyền nào vẫn mở được màn, chỉ thấy hợp đồng mình tạo', 'P0',
      'TK-NV không có quyền nào; KH-TEST có HD-TEST-01 (TK-NV tạo) đã có phát sinh; có hợp đồng khác của người khác cùng kỳ',
      ['1. Đăng nhập TK-NV', '2. ' + MENU, '3. Chọn Thời gian = tháng có phát sinh'],
      'Tài khoản TK-NV',
      ['- Mở được màn, không báo thiếu quyền',
       '- Bảng chỉ có các hợp đồng có cột NVKD = TK-NV',
       '- KHÔNG có ô Công ty, Phòng ban, Bộ phận, Nhân viên',
       '- Dòng Tổng cộng chỉ cộng hợp đồng của TK-NV (so bằng tay tổng các dòng khi không lọc thêm)']),
    T('Q', '01', 'Quyền tổng công ty thấy toàn bộ và đủ 4 ô đơn vị', 'P0',
      'TK-ALL', ['1. Đăng nhập TK-ALL, mở báo cáo', '2. Chọn Thời gian 01/10/2026 → 31/10/2026'], 'Tài khoản TK-ALL',
      ['- Có ô Công ty, Phòng ban, Bộ phận, Nhân viên',
       '- Bảng có hợp đồng của nhiều công ty / phòng ban',
       '- Trên dev: chân bảng "Hiển thị 1–10 / 25,309 dòng hợp đồng"']),
    T('Q', '02', 'Quyền công ty: chỉ công ty đang làm việc + hợp đồng mình tạo', 'P0',
      'TK-CTY thuộc Công ty A; có hợp đồng của Công ty B cùng kỳ',
      ['1. Đăng nhập TK-CTY, mở báo cáo, chọn Thời gian', '2. Quan sát ô lọc và các dòng', '3. Tìm nhanh số hợp đồng của Công ty B'],
      'Tài khoản TK-CTY',
      ['- Không có ô Công ty; có ô Phòng ban, Bộ phận, Nhân viên',
       '- Không thấy hợp đồng Công ty B (trừ hợp đồng do TK-CTY tạo)',
       '- Bước 3: "Không có dữ liệu phù hợp bộ lọc."']),
    T('Q', '03', 'Quyền phòng ban: các phòng mình quản lý', 'P1',
      'TK-PB quản lý PB-1, đang ngồi PB-2 (không quản lý PB-2)',
      ['1. Đăng nhập TK-PB, mở báo cáo, chọn Thời gian', '2. Xem cột Phòng ban'], 'Tài khoản TK-PB',
      ['- Chỉ thấy số của PB-1 và hợp đồng TK-PB tự tạo',
       '- KHÔNG tự thấy PB-2 chỉ vì đang ngồi ở đó',
       '- Có ô Phòng ban, Bộ phận, Nhân viên; không có ô Công ty']),
    T('Q', '04', 'Quyền bộ phận: các bộ phận mình quản lý', 'P1',
      'TK-BP quản lý BP-1', ['1. Đăng nhập TK-BP, mở báo cáo, chọn Thời gian'], 'Tài khoản TK-BP',
      ['- Chỉ thấy số của BP-1 và hợp đồng TK-BP tạo', '- Chỉ có ô Bộ phận, Nhân viên']),
    T('Q', '05', 'Có nhiều quyền thì lấy cấp rộng nhất', 'P2',
      'TK-X có cả quyền "... theo bộ phận" và "... theo tổng công ty"', ['1. Đăng nhập TK-X, mở báo cáo, chọn Thời gian'],
      'Tài khoản TK-X', ['- Như TK-ALL: có ô Công ty, thấy toàn bộ']),
    T('Q', '06', 'Phạm vi áp cho dòng Tổng cộng, popup và Excel', 'P0',
      'TK-NV (không quyền); đã biết Tổng cộng của TK-ALL cùng kỳ',
      ['1. TK-NV mở báo cáo, chọn cùng kỳ', '2. So dòng Tổng cộng với TK-ALL', '3. Bấm 1 số ở dòng khách hàng, xem popup',
       '4. Xuất Excel, mở file'],
      'Tài khoản TK-NV',
      ['- Tổng cộng (cả Số dư đầu kỳ) chỉ gồm số trong phạm vi TK-NV, nhỏ hơn TK-ALL',
       '- Popup chỉ có chứng từ của hợp đồng TK-NV tạo',
       '- File Excel chỉ có các dòng TK-NV thấy trên màn']),
]

# ------------------------------------------------------------------ II. GIAO DIỆN
S_UI = [
    T('U', '001', 'Mở màn lần đầu: bộ lọc trống, bảng chờ chọn thời gian', 'P0', 'TK-ALL',
      ['1. ' + MENU], '',
      ['- Tiêu đề "Báo cáo chi tiết công nợ khách hàng", có icon ⓘ cạnh tiêu đề',
       '- Ô tìm nhanh placeholder "Tìm theo số hợp đồng, mã hoặc tên khách hàng"; nút Tìm kiếm, Làm mới, Cài đặt bộ lọc, Ẩn tìm kiếm nâng cao',
       '- Ô Thời gian có dấu * đỏ, trống; Khách hàng, Số hợp đồng, Số dư cuối kỳ trống',
       '- Bảng: "Chọn thời gian để xem báo cáo."; có nút Xuất Excel']),
    T('U', '002', 'Tiêu đề bảng 2 tầng đúng thứ tự cột', 'P1', 'Đã chọn Thời gian',
      ['1. Quan sát hàng tiêu đề, cuộn ngang hết bảng'], '',
      ['- Tầng 1: STT, Đơn hàng/hợp đồng, Phòng ban, Bộ phận, NVKD, Số dư đầu kỳ, "Phát sinh tăng trong kỳ" (3 cột), '
       '"Phát sinh giảm trong kỳ" (4 cột), Trả lại tiền thừa, Số dư cuối kỳ',
       '- Tầng 2: Hàng hóa/Dịch vụ, Điều chỉnh công nợ, Cộng | Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ, Cộng',
       '- Mỗi tiêu đề cột có icon ⓘ; có thanh cuộn ngang trên và dưới bảng']),
    T('U', '003', 'Icon ⓘ đầu cột hiện đúng chú thích', 'P2', 'Đã chọn Thời gian',
      ['1. Rê chuột vào ⓘ của cột Số dư cuối kỳ', '2. Rê vào ⓘ cạnh chữ Tổng cộng'], '',
      ['- Bước 1: "Công nợ phải thu còn lại tại "Đến ngày"." kèm "Số dư cuối kỳ = Số dư đầu kỳ + Cộng phát sinh tăng − Cộng phát sinh giảm + Trả lại tiền thừa."',
       '- Bước 2: "Tổng trên toàn bộ công nợ theo bộ lọc. Lọc "Số dư cuối kỳ" (Dư nợ / Dư có) và ô tìm nhanh chỉ áp cho các dòng khách hàng, không áp cho dòng tổng (giống ERP). ..."']),
    T('U', '004', 'Tiêu đề bảng dính khi cuộn dọc', 'P3', 'Kết quả > 20 dòng, chọn 50 dòng/trang',
      ['1. Cuộn bảng xuống cuối'], '', ['- Hàng tiêu đề 2 tầng vẫn hiện trên cùng vùng bảng']),
    T('U', '005', 'Dòng khách hàng đậm, dòng Tổng cộng nền xám', 'P2', 'Lọc KH 89THUPTR-62, tháng 10/2026 (dev)',
      ['1. Quan sát 3 loại dòng'], 'KH 89THUPTR-62',
      ['- Dòng 1: "Tổng cộng" nền xám đậm', '- Dòng 2: "1 | 89THUPTR-62 - CÔNG TY TNHH ĐẦU TƯ THƯƠNG MẠI THIÊN TRƯỜNG" chữ đậm, tên gộp qua 4 cột',
       '- 3 dòng 1.1, 1.2, 1.3 chữ thường; số hợp đồng gạch chân, bấm được']),
    T('U', '006', 'Phân trang và số dòng/trang', 'P1', 'Kết quả > 10 dòng hợp đồng',
      ['1. Quan sát chân bảng', '2. Chọn 20 dòng/trang', '3. Sang trang 2'], '',
      ['- Mặc định 10; lựa chọn 10 / 20 / 50 / 100', '- Chân "Hiển thị 1–20 / N dòng hợp đồng" sau bước 2',
       '- Trang 2: STT khách hàng nối tiếp trang 1 (không quay về 1); dòng Tổng cộng không đổi']),
    T('U', '007', 'Không có dữ liệu', 'P2', '', ['1. Tìm nhanh "ZZZ-KHONG-CO", Enter'], 'ZZZ-KHONG-CO',
      ['- Bảng "Không có dữ liệu phù hợp bộ lọc."', '- Không hiện dòng Tổng cộng, không có chân phân trang']),
    T('U', '008', 'Bấm số hợp đồng mở hợp đồng ở tab mới', 'P1', 'Có dòng HD-TEST-01',
      ['1. Bấm số HD-TEST-01'], '', ['- Mở hợp đồng ở tab mới, tab báo cáo giữ nguyên bộ lọc', '- Dòng không gắn hợp đồng: ô trống, không bấm được']),
]

# ------------------------------------------------------------------ III. BỘ LỌC
S_LOC = [
    T('L', '001', 'Bắt buộc Thời gian khi bấm Tìm kiếm', 'P0', 'Mở màn, Thời gian trống',
      ['1. Bấm Tìm kiếm'], '', ['- Dưới ô Thời gian chữ đỏ "Vui lòng chọn thời gian"', '- Bảng vẫn "Chọn thời gian để xem báo cáo."']),
    T('L', '002', 'Chọn Thời gian thì báo cáo tự tải', 'P0', '', ['1. Chọn 01/10/2026 → 31/10/2026, không bấm Tìm kiếm'], '01/10/2026 - 31/10/2026',
      ['- Dòng "Đang tải dữ liệu..." rồi hiện báo cáo', '- Dev: Tổng cộng Số dư đầu kỳ 898,996,927,176; Số dư cuối kỳ 955,376,161,388']),
    T('L', '003', 'Ngày ngược chiều', 'P0', '',
      ['1. Gõ Từ ngày 31/10/2026, Đến ngày 01/10/2026 (lịch không cho chọn ngược thì gõ tay)'], '',
      ['- Dưới ô Thời gian chữ đỏ "Đến ngày phải lớn hơn hoặc bằng Từ ngày."', '- Toast cùng câu',
       '- Bảng rỗng, không còn số của khoảng cũ', '- Bấm Xuất Excel: toast cùng câu, không mở cửa sổ']),
    T('L', '004', 'Từ ngày = Đến ngày', 'P2', '', ['1. Chọn 15/10/2026 → 15/10/2026'], '',
      ['- Tải bình thường; phát sinh chỉ gồm chứng từ hạch toán ngày 15/10/2026']),
    T('L', '005', 'Lọc Khách hàng', 'P0', '', ['1. Chọn Thời gian tháng 10/2026', '2. Ô Khách hàng gõ "89THUPTR-62", chọn'], '89THUPTR-62',
      ['- Gõ 1 ký tự chưa gợi ý; từ 2 ký tự mới gợi ý', '- Dev: còn 1 khách, 3 dòng hợp đồng, chân "Hiển thị 1–3 / 3 dòng hợp đồng"',
       '- Dòng Tổng cộng = dòng khách hàng (848,527,621 … 943,656,841)']),
    T('L', '006', 'Lọc Số hợp đồng khớp chính xác', 'P1', 'Lọc KH 89THUPTR-62',
      ['1. Ô Số hợp đồng nhập "HĐ_TPE_HN_KD2_26_1141_TT - TP", Enter', '2. Đổi thành "HĐ_TPE_HN_KD2_26_1141", Enter'], '',
      ['- Bước 1: còn đúng dòng 1.1 HĐ_TPE_HN_KD2_26_1141_TT - TP, Số dư cuối kỳ 938,818,441',
       '- Bước 2 (thiếu đuôi): "Không có dữ liệu phù hợp bộ lọc."', '- Gõ xong chưa Enter: bảng chưa đổi']),
    T('L', '007', 'Lọc Số dư cuối kỳ Dư nợ / Dư có / Tất cả', 'P0', 'Lọc KH 89THUPTR-62, tháng 10/2026 (dev)',
      ['1. Chọn Dư nợ', '2. Chọn Dư có', '3. Chọn Tất cả'], '',
      ['- Dư nợ: còn 2 dòng (1.2 = 938,818,441 và 1.3 = 4,838,400); dòng 1.1 (cuối kỳ 0) bị loại',
       '- Dư có: "Không có dữ liệu phù hợp bộ lọc." (khách này không có hợp đồng âm)',
       '- Tất cả: 3 dòng như ban đầu', '- Dòng Tổng cộng KHÔNG đổi giữa 3 lựa chọn (thiết kế)']),
    T('L', '008', 'Ô tìm nhanh theo số hợp đồng / mã / tên khách', 'P1', 'Thời gian tháng 10/2026',
      ['1. Gõ "1141", Enter (lọc thêm KH 89THUPTR-62)', '2. Gõ "THIÊN TRƯỜNG", Enter', '3. Gõ "89thuptr-62" chữ thường, Enter'], '',
      ['- Bước 1: còn dòng HĐ_TPE_HN_KD2_26_1141_TT - TP; dòng khách hàng Hàng hóa/Dịch vụ 1,380,623,222',
       '- Dòng Tổng cộng vẫn 1,595,658,222 (ô tìm nhanh không áp cho Tổng cộng)',
       '- Bước 2, 3: ra các hợp đồng của khách THIÊN TRƯỜNG, không phân biệt hoa thường']),
    T('L', '009', 'Lọc Công ty / Phòng ban / Bộ phận chọn nhiều', 'P1', 'TK-ALL, Thời gian tháng 10/2026',
      ['1. Chọn 2 công ty', '2. Thêm 1 phòng ban', '3. Bấm icon khoá cạnh nhãn "Phòng ban"'], '',
      ['- Bảng chỉ còn chứng từ của 2 công ty, rồi của phòng đã chọn (cột Phòng ban khớp)',
       '- Bước 3: danh sách có thêm phòng ban đã khoá, gợi ý "Đang hiện cả phòng ban đã khoá — bấm để ẩn đi"']),
    T('L', '010', 'Lọc Nhân viên theo người tạo hợp đồng', 'P1', 'TK-ALL; HD-TEST-01 do TK-NV tạo',
      ['1. Chọn Nhân viên = TK-NV'], '', ['- Mọi dòng có NVKD = TK-NV', '- Có HD-TEST-01']),
    T('L', '011', 'Kết hợp nhiều ô lọc', 'P1', '',
      ['1. Thời gian tháng 10/2026 + Khách hàng 89THUPTR-62 + Số dư cuối kỳ Dư nợ + tìm nhanh "1303"'], '',
      ['- Còn đúng dòng HĐ_TPE_HN_KD2_26_1303_26.9, Số dư cuối kỳ 4,838,400']),
    T('L', '012', 'Làm mới xoá hết, kể cả Thời gian', 'P1', 'Đang lọc nhiều ô',
      ['1. Bấm Làm mới'], '', ['- Mọi ô trống (kể cả Thời gian)', '- Bảng "Chọn thời gian để xem báo cáo."']),
    T('L', '013', 'Ghi nhớ bộ lọc khi rời màn, F5 thì xoá', 'P2', 'Đang lọc KH 89THUPTR-62, tháng 10/2026',
      ['1. Sang màn khác rồi quay lại trong 10 phút', '2. Nhấn F5'], '',
      ['- Bước 1: bộ lọc và kết quả giữ nguyên', '- Bước 2: bộ lọc về trống như bấm Làm mới']),
    T('L', '014', 'Cài đặt bộ lọc', 'P3', '', ['1. Bấm Cài đặt bộ lọc', '2. Bỏ tích "Số hợp đồng", Lưu'], '',
      ['- Cửa sổ liệt kê: Thời gian, Khách hàng, Số hợp đồng, Số dư cuối kỳ, Công ty / Phòng ban / Bộ phận / Nhân viên; nút Lưu, Khôi phục mặc định, Đóng',
       '- Sau Lưu: ô Số hợp đồng ẩn khỏi bộ lọc']),
    T('L', '015', 'Đổi bộ lọc liên tiếp chỉ hiện kết quả lần cuối', 'P2', '',
      ['1. Chọn Thời gian cả năm 2026', '2. Ngay lập tức đổi Khách hàng = 89THUPTR-62'], '',
      ['- Bảng cuối cùng chỉ có khách 89THUPTR-62, không bị số của lần lọc trước đè lên']),
]

# ------------------------------------------------------------------ IV. SỐ LIỆU
S_SO = [
    T('S', '001', 'Định dạng số và số 0', 'P1', 'Lọc KH 89THUPTR-62, tháng 10/2026 (dev)',
      ['1. Quan sát các ô số'], '',
      ['- Dạng 1,234,567, không có số lẻ', '- Dòng Tổng cộng: Đã thanh toán "0", Trả lại tiền thừa "0"',
       '- Dòng khách hàng: Đã thanh toán, Trả lại tiền thừa để trống', '- Dòng 1.1: Số dư cuối kỳ "0"; dòng 1.1 và 1.3: ĐCCN giảm "0" (gạch chân)']),
    T('S', '002', 'Cộng phát sinh tăng / giảm từng dòng', 'P0', 'Như trên',
      ['1. Dòng 1.1: cộng Hàng hóa/Dịch vụ + ĐCCN tăng', '2. Cộng Nhập trả lại + Đã thanh toán + ĐCCN giảm'], '',
      ['- Bước 1: 215,035,000 + 453,829,501 = 668,864,501 = cột Cộng (tăng)', '- Bước 2: 1,500,529,002 + 0 + 0 = 1,500,529,002 = cột Cộng (giảm)']),
    T('S', '003', 'Số dư cuối kỳ từng dòng', 'P0', 'Như trên',
      ['1. Tính tay cho dòng 1.1, 1.2, 1.3'], '',
      ['- 1.1: 831,664,501 + 668,864,501 − 1,500,529,002 = 0', '- 1.2: 12,024,720 + 1,380,623,222 − 453,829,501 = 938,818,441',
       '- 1.3: 4,838,400 = 4,838,400']),
    T('S', '004', 'Dòng khách hàng = tổng các hợp đồng', 'P0', 'Như trên',
      ['1. Cộng từng cột của 1.1, 1.2, 1.3'], '',
      ['- Số dư đầu kỳ: 831,664,501 + 12,024,720 + 4,838,400 = 848,527,621', '- Hàng hóa/Dịch vụ: 215,035,000 + 1,380,623,222 = 1,595,658,222',
       '- Số dư cuối kỳ: 0 + 938,818,441 + 4,838,400 = 943,656,841']),
    T('S', '005', 'Dòng khách hàng tính đủ khi hợp đồng vắt sang trang sau', 'P0', 'Khách có > 10 hợp đồng, 10 dòng/trang, hợp đồng của khách nằm ở cả trang 1 và 2',
      ['1. Ghi số dòng khách hàng ở trang 1', '2. Sang trang 2', '3. Đổi 100 dòng/trang, cộng tay các hợp đồng của khách'], '',
      ['- Dòng khách hàng ở trang 1 và trang 2 cùng một số', '- Bằng tổng mọi hợp đồng của khách (bước 3)']),
    T('S', '006', 'Dòng Tổng cộng = tổng các dòng khi không lọc Dư nợ / tìm nhanh', 'P1', 'Lọc 1 khách có 2+ hợp đồng',
      ['1. So dòng Tổng cộng với dòng khách hàng'], '', ['- Mọi cột bằng nhau (khách không có chứng từ chưa gắn khách hàng)']),
    T('S', '007', 'Dòng Tổng cộng không áp Dư nợ / tìm nhanh (thiết kế)', 'P1', 'Lọc KH 89THUPTR-62, tháng 10/2026',
      ['1. Chọn Số dư cuối kỳ = Dư nợ', '2. So dòng Tổng cộng với dòng khách hàng'], '',
      ['- Dòng khách hàng: Hàng hóa/Dịch vụ 1,380,623,222', '- Dòng Tổng cộng vẫn 1,595,658,222',
       '- Đúng thiết kế — ghi nhận, không ghi Failed']),
    T('S', '008', 'Kỳ chỉ giới hạn Đến ngày: hợp đồng không phát sinh vẫn hiện', 'P2', 'HD-TEST-02 chỉ có chứng từ tháng trước',
      ['1. Lọc tháng này, KH-TEST'], '',
      ['- Có dòng HD-TEST-02: Số dư đầu kỳ = số dư tháng trước, các cột phát sinh trống, Số dư cuối kỳ = Số dư đầu kỳ']),
    T('S', '009', 'Đổi Từ ngày chuyển số giữa đầu kỳ và phát sinh', 'P1', 'Biết số liệu khách 89THUPTR-62',
      ['1. Lọc 01/10/2026 → 31/10/2026', '2. Lọc 01/01/2026 → 31/10/2026'], '',
      ['- Số dư cuối kỳ của dòng khách hàng KHÔNG đổi giữa 2 lần (cùng Đến ngày)', '- Số dư đầu kỳ và các cột phát sinh thay đổi tương ứng']),
    T('S', '010', 'Phòng ban / Bộ phận / NVKD lấy theo người tạo hợp đồng hiện tại', 'P2', 'NV tạo HD-TEST-01 vừa chuyển sang PB-2',
      ['1. Lọc KH-TEST, xem dòng HD-TEST-01'], '', ['- Cột Phòng ban hiện mã PB-2 (phòng mới), NVKD = TK-NV']),
    T('S', '011', 'Số dư âm (dư có)', 'P1', 'Có hợp đồng khách trả thừa',
      ['1. Lọc Dư có'], '', ['- Số dư cuối kỳ âm, dạng -1,234,567', '- Mọi dòng hiện đều có Số dư cuối kỳ < 0']),
    T('S', '012', 'Chứng từ không gắn hợp đồng', 'P2', 'Khách có phiếu báo có không chọn hợp đồng',
      ['1. Lọc khách đó'], '', ['- Có 1 dòng ô Đơn hàng/hợp đồng trống, Phòng ban / Bộ phận / NVKD trống', '- Bấm số ở dòng đó: popup tiêu đề phụ "… — Không gắn hợp đồng"']),
    T('S', '013', 'Số dư đầu kỳ Tổng cộng tính cả chứng từ chưa gắn khách hàng', 'P3', 'Có bút toán phải thu không gắn khách hàng trước Từ ngày',
      ['1. Lọc không chọn khách, so Số dư đầu kỳ Tổng cộng với tổng các dòng khách hàng (xuất Excel để cộng)'], '',
      ['- Tổng cộng lệch đúng bằng số của bút toán không gắn khách hàng — đúng thiết kế']),
]

# ------------------------------------------------------------------ V. LUỒNG PHÁT SINH
NEN = 'Đã ghi số nền (TC 001) ở ' + XEM
S_PS = [
    T('P', '001', 'Ghi số nền trước khi lập chứng từ', 'P0', 'KH-TEST, HD-TEST-01 có sẵn (mục 9)',
      ['1. Mở báo cáo, lọc: ' + LOC, '2. Ghi lại mọi cột của ' + XEM], 'KH-TEST, HD-TEST-01',
      ['- Có đủ số nền (khách mới thì trống, Số dư cuối kỳ 0) để so ở các TC sau']),
    T('P', '002', 'Phiếu xuất hàng tăng Hàng hóa/Dịch vụ', 'P0', NEN + '; phiếu xuất kho cho HD-TEST-01 đã có sẵn (lập ở hệ thống cũ)',
      ['1. Vào ' + M['pxh'] + ', lập phiếu xuất hàng cho HD-TEST-01 giá trị 10,000,000, hạch toán hôm nay', '2. Lọc lại báo cáo'], '10,000,000',
      ['- Hàng hóa/Dịch vụ +10,000,000; Cộng (tăng) +10,000,000; Số dư cuối kỳ +10,000,000 ở ' + XEM,
       '- Bấm số Hàng hóa/Dịch vụ dòng HD-TEST-01: popup có phiếu vừa lập, Phát sinh nợ 10,000,000']),
    T('P', '003', 'Chứng từ chưa hạch toán không làm đổi báo cáo', 'P0', 'Số nền mới',
      ['1. Lập phiếu thu 1,000,000 cho HD-TEST-01, để chưa duyệt / chưa hạch toán', '2. Lọc lại'], '',
      ['- Không cột nào thay đổi']),
    T('P', '004', 'Phiếu thu tăng Đã thanh toán', 'P0', 'Số nền mới',
      ['1. Vào ' + M['pt'] + ', lập phiếu thu KH-TEST, hợp đồng HD-TEST-01, 4,000,000, duyệt và hạch toán hôm nay', '2. Lọc lại'], '4,000,000',
      ['- Đã thanh toán +4,000,000; Cộng (giảm) +4,000,000; Số dư cuối kỳ −4,000,000', '- Popup Đã thanh toán có mã phiếu thu vừa lập, bấm mã mở đúng phiếu']),
    T('P', '005', 'Phiếu báo có tăng Đã thanh toán', 'P1', 'Số nền mới',
      ['1. Vào ' + M['pbc'] + ', lập phiếu báo có KH-TEST cho HD-TEST-01, 1,000,000, hạch toán hôm nay', '2. Lọc lại'], '1,000,000',
      ['- Đã thanh toán +1,000,000; Số dư cuối kỳ −1,000,000']),
    T('P', '006', 'Điều chỉnh công nợ TĂNG', 'P0', 'Số nền mới',
      ['1. Vào ' + M['ycdc'] + ', lập yêu cầu điều chỉnh TĂNG KH-TEST, HD-TEST-01, 2,000,000; duyệt', '2. Vào ' + M['pkt'] + ', lập phiếu kế toán từ yêu cầu, hạch toán hôm nay', '3. Lọc lại'], '2,000,000',
      ['- Điều chỉnh công nợ (nhóm tăng) +2,000,000; Cộng (tăng) +2,000,000; Số dư cuối kỳ +2,000,000']),
    T('P', '007', 'Điều chỉnh công nợ GIẢM', 'P0', 'Số nền mới',
      ['1. Làm như TC 006 nhưng điều chỉnh GIẢM 500,000', '2. Lọc lại'], '500,000',
      ['- Điều chỉnh công nợ (nhóm giảm) +500,000; Cộng (giảm) +500,000; Số dư cuối kỳ −500,000']),
    T('P', '008', 'Khách trả lại hàng tăng Nhập trả lại', 'P0', 'HD-TEST-01 đã xuất hàng (TC 002)',
      ['1. Vào ' + M['pnh'] + ', lập phiếu nhập hàng trả lại theo HD-TEST-01, 3,000,000, hạch toán hôm nay', '2. Lọc lại'], '3,000,000',
      ['- Nhập trả lại +3,000,000; Số dư cuối kỳ −3,000,000', '- Popup Nhập trả lại: 2 cột Phát sinh nợ / có, phiếu vừa lập ở cột Phát sinh có']),
    T('P', '009', 'Phiếu chi tăng Trả lại tiền thừa và TĂNG số dư', 'P0', 'Số nền mới',
      ['1. Vào ' + M['pc'] + ', lập phiếu chi trả KH-TEST cho HD-TEST-01, 200,000, hạch toán hôm nay', '2. Lọc lại'], '200,000',
      ['- Trả lại tiền thừa +200,000; Số dư cuối kỳ TĂNG 200,000; nhóm Phát sinh giảm không đổi']),
    T('P', '010', 'Phiếu ủy nhiệm chi tăng Trả lại tiền thừa', 'P1', 'Số nền mới',
      ['1. Vào ' + M['unc'] + ', lập ủy nhiệm chi trả KH-TEST cho HD-TEST-01, 300,000, hạch toán hôm nay', '2. Lọc lại'], '300,000',
      ['- Trả lại tiền thừa +300,000 (lũy kế 500,000); Số dư cuối kỳ +300,000']),
    T('P', '011', 'Kiểm tổng sau cả chuỗi', 'P0', 'Đã làm TC 002 → 010',
      ['1. So Số dư cuối kỳ HD-TEST-01 với số nền TC 001'], '',
      ['- Chênh: +10,000,000 − 4,000,000 − 1,000,000 + 2,000,000 − 500,000 − 3,000,000 + 200,000 + 300,000 = +4,000,000',
       '- Dòng khách hàng KH-TEST và dòng Tổng cộng chênh đúng như vậy']),
    T('P', '012', 'Thu vượt chuyển sang Dư có', 'P1', 'HD-TEST-01 đang dư nợ 4,000,000 (số nền 0)',
      ['1. Lập phiếu thu 5,000,000 cho HD-TEST-01, hạch toán hôm nay', '2. Lọc Tất cả / Dư nợ / Dư có'], '5,000,000',
      ['- Số dư cuối kỳ HD-TEST-01 = -1,000,000', '- Dư nợ: không có HD-TEST-01; Dư có: có HD-TEST-01', '- Dòng Tổng cộng không đổi giữa 3 lựa chọn']),
    T('P', '013', 'Ngày hạch toán quyết định kỳ', 'P1', 'Phiếu thu 700,000 cho HD-TEST-01, ngày hạch toán là ngày cuối tháng trước',
      ['1. Lọc ngày 1 tháng này → hôm nay', '2. Lọc ngày 1 tháng trước → hôm nay'], '700,000',
      ['- Bước 1: phiếu nằm trong Số dư đầu kỳ (giảm 700,000), không ở cột Đã thanh toán',
       '- Bước 2: phiếu ở cột Đã thanh toán; Số dư cuối kỳ hai lần bằng nhau']),
    T('P', '014', 'Khai báo đầu kỳ công nợ', 'P2', 'Có quyền "Quản lý công nợ đầu kỳ"',
      ['1. Vào ' + M['dk'] + ', khai báo công nợ đầu kỳ KH-TEST, HD-TEST-02, 1,500,000 ghi Nợ, ngày trước Từ ngày', '2. Lọc lại'], '1,500,000',
      ['- Dòng HD-TEST-02: Số dư đầu kỳ +1,500,000; Số dư cuối kỳ +1,500,000',
       '- Lọc kỳ chứa ngày khai báo: cột Hàng hóa/Dịch vụ +1,500,000']),
]

# ------------------------------------------------------------------ VI. POPUP
S_POP = [
    T('O', '001', 'Popup Hàng hóa/Dịch vụ dòng hợp đồng (2 cột)', 'P0', 'Lọc KH 89THUPTR-62, tháng 10/2026 (dev)',
      ['1. Bấm 215,035,000 ở dòng HĐ_TPE_HN_KD2_26_1094_TP-TT'], '',
      ['- Tiêu đề "Chi tiết chứng từ", dòng phụ "Phát sinh tăng - Hàng hóa/Dịch vụ — HĐ_TPE_HN_KD2_26_1094_TP-TT"',
       '- Cột: STT, Mã phiếu, Phát sinh nợ, Phát sinh có, Ngày tạo, Người tạo',
       '- 4 phiếu PXH-41186 (115,027,000), PXH-41935, PXH-42762, PXH-42763; "Hiển thị 1–4 / 4"',
       '- Chân: "Tổng phát sinh nợ: 215,035,000 · Tổng phát sinh có:" — Nợ − Có = số đã bấm']),
    T('O', '002', 'Popup dòng khách hàng gồm mọi hợp đồng', 'P0', 'Như trên',
      ['1. Bấm 1,595,658,222 ở dòng khách hàng'], '',
      ['- Dòng phụ "… — 89THUPTR-62 - CÔNG TY TNHH ĐẦU TƯ THƯƠNG MẠI THIÊN TRƯỜNG"', '- 10 phiếu PXH',
       '- Chân "Tổng phát sinh nợ: 1,745,711,122 · Tổng phát sinh có: 150,052,900"; 1,745,711,122 − 150,052,900 = 1,595,658,222']),
    T('O', '003', 'Popup 1 cột Số tiền (Điều chỉnh công nợ)', 'P1', 'Như trên',
      ['1. Bấm 453,829,501 ở cột Điều chỉnh công nợ (tăng) dòng 1.1'], '',
      ['- Cột: STT, Mã phiếu, Số tiền, Ngày tạo, Người tạo', '- 1 phiếu TPE.PKT1026.00436, 453,829,501, 20/10/2026 08:37', '- Chân "Tổng số tiền: 453,829,501"']),
    T('O', '004', 'Popup Nhập trả lại', 'P1', 'Như trên',
      ['1. Bấm 1,500,529,002 ở cột Nhập trả lại dòng 1.1'], '',
      ['- 10 phiếu PNH, số ở cột Phát sinh có', '- Chân "Tổng phát sinh có: 1,500,529,002"']),
    T('O', '005', 'Số 0 không bấm được, trừ ĐCCN giảm dòng hợp đồng', 'P2', 'Như trên',
      ['1. Rê chuột vào ô trống cột Đã thanh toán', '2. Bấm "0" cột ĐCCN giảm dòng 1.3'], '',
      ['- Bước 1: không phải liên kết', '- Bước 2: mở popup, "Không có dữ liệu phù hợp."']),
    T('O', '006', 'Bấm Mã phiếu mở chứng từ ở tab mới', 'P1', 'Popup đang mở', ['1. Bấm mã PXH-41186'], '',
      ['- Mở Phiếu xuất hàng PXH-41186 ở tab mới; popup và báo cáo giữ nguyên']),
    T('O', '007', 'Phân trang popup và đóng', 'P2', 'Popup > 10 chứng từ',
      ['1. Chọn 5 dòng/trang, sang trang 2', '2. Bấm Đóng', '3. Mở lại popup'], '',
      ['- Tổng ở chân không đổi khi chuyển trang', '- Đóng: về báo cáo, giữ bộ lọc và trang', '- Mở lại: về trang 1, 10 dòng/trang']),
    T('O', '008', 'Popup dòng khách hàng khi đang lọc Dư nợ', 'P1', 'Lọc KH 89THUPTR-62, tháng 10/2026, Số dư cuối kỳ = Dư nợ',
      ['1. Bấm số Hàng hóa/Dịch vụ ở dòng khách hàng (1,380,623,222)'], '',
      ['- Mong đợi: tổng popup (Nợ − Có) = 1,380,623,222 — số đã bấm',
       '- Ghi chú: popup không áp lọc Số dư cuối kỳ nên hiện tại có thể ra 1,745,711,122 − 150,052,900 = 1,595,658,222 (gồm cả hợp đồng 1.1 đã bị lọc ra) — nếu vậy ghi Failed, đưa đội phát triển xem']),
    T('O', '009', 'Popup ĐCCN tăng có thêm phiếu thu ghi Nợ (giữ như hệ thống cũ)', 'P3', 'Hợp đồng có phiếu thu ghi Nợ sổ phải thu trong kỳ',
      ['1. Bấm số ĐCCN tăng của hợp đồng đó'], '',
      ['- Popup có cả phiếu kế toán và phiếu thu; tổng popup lớn hơn số đã bấm đúng bằng số phiếu thu — ghi nhận, không ghi Failed']),
]

# ------------------------------------------------------------------ VII. XUẤT EXCEL
S_X = [
    T('X', '001', 'Chưa chọn Thời gian thì không xuất', 'P1', 'Bộ lọc trống', ['1. Bấm Xuất Excel'], '',
      ['- Toast "Vui lòng chọn thời gian"; ô Thời gian chữ đỏ; không mở cửa sổ']),
    T('X', '002', 'Cửa sổ chọn trường', 'P1', 'Đã chọn Thời gian', ['1. Bấm Xuất Excel'], '',
      ['- Tiêu đề "Chọn trường xuất Excel"; dòng "Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file."',
       '- 14 trường tích sẵn: Khách hàng / Đơn hàng - hợp đồng, Phòng ban, Bộ phận, NVKD, Số dư đầu kỳ, PS tăng - Hàng hóa/Dịch vụ, PS tăng - Điều chỉnh công nợ, PS tăng - Cộng, PS giảm - Nhập trả lại, PS giảm - Đã thanh toán, PS giảm - Điều chỉnh công nợ, PS giảm - Cộng, Trả lại tiền thừa, Số dư cuối kỳ',
       '- "Đang chọn 14/14 trường"; nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng']),
    T('X', '003', 'File đúng bố cục và số', 'P0', 'Lọc KH 89THUPTR-62, tháng 10/2026 (dev)',
      ['1. Xuất Excel đủ 14 trường', '2. Mở file bao_cao_chi_tiet_cong_no_khach_hang.xlsx'], '',
      ['- Sheet "Chi tiết công nợ KH"; dòng 1 "BÁO CÁO CHI TIẾT CÔNG NỢ KHÁCH HÀNG"; dòng 2 "Thời gian: 01/10/2026 - 31/10/2026" in đậm',
       '- Tiêu đề 2 tầng "Phát sinh tăng trong kỳ" / "Phát sinh giảm trong kỳ"; cột STT đầu tiên',
       '- Dòng Tổng cộng, dòng "1 | 89THUPTR-62 - …" (đậm), 3 dòng 1.1, 1.2, 1.3; số khớp màn (vd Số dư cuối kỳ 943,656,841)',
       '- Ô số là kiểu số (cộng được trong Excel); toast "Xuất Excel thành công"']),
    T('X', '004', 'Chọn trường và đổi thứ tự', 'P1', '', ['1. Bỏ chọn hết, tích Số dư cuối kỳ rồi Khách hàng / Đơn hàng - hợp đồng', '2. Xuất file'], '',
      ['- File có 3 cột: STT, Số dư cuối kỳ, Khách hàng / Đơn hàng - hợp đồng (theo thứ tự tích)', '- Bỏ chọn hết: nút Xuất file không bấm được']),
    T('X', '005', 'Excel theo bộ lọc, mọi trang', 'P1', 'Kết quả 25 dòng hợp đồng, đang ở trang 1 (10 dòng)',
      ['1. Xuất Excel'], '', ['- File có đủ 25 dòng hợp đồng (không chỉ 10 dòng trang đang xem)', '- Có áp ô tìm nhanh và Số dư cuối kỳ nếu đang lọc']),
    T('X', '006', 'Số 0 trong file', 'P2', 'Như TC 003', ['1. Xem ô Đã thanh toán dòng khách hàng và dòng Tổng cộng'], '',
      ['- Dòng Tổng cộng hiện 0; dòng khách hàng ô trống; Số dư cuối kỳ dòng 1.1 hiện 0']),
    T('X', '007', 'Xuất Excel khi KHÔNG lọc khách hàng (dữ liệu lớn)', 'P1', 'TK-ALL, Thời gian 01/10/2026 → 31/10/2026, không lọc thêm (dev: 25,309 dòng hợp đồng)',
      ['1. Xuất Excel đủ 14 trường', '2. Đo thời gian đến khi tải xong file'], '',
      ['- Tải được file đủ 25,309 dòng hợp đồng + dòng khách hàng, trong thời gian chấp nhận được (dưới 60 giây)',
       '- Ghi chú: thử trên dev 02/11/2026 lấy dữ liệu xuất cả tháng bị lỗi máy chủ (502) sau khoảng 7 giây — nếu gặp toast "Lỗi khi xuất Excel" hoặc lỗi máy chủ thì ghi Failed']),
]

# ------------------------------------------------------------------ VIII. HIỆU NĂNG
S_HN = [
    T('H', '001', 'Thời gian tải khi chỉ chọn Thời gian 1 tháng', 'P1', 'TK-ALL',
      ['1. Chọn 01/10/2026 → 31/10/2026, đo đến khi bảng có dòng'], '',
      ['- Bảng hiện trong ≤ 10 giây (dev 02/11/2026: ~4,5 giây, 25,309 dòng hợp đồng)']),
    T('H', '002', 'Thời gian tải kỳ dài', 'P2', 'TK-ALL', ['1. Chọn 01/01/2026 → 31/10/2026'], '',
      ['- Bảng hiện trong ≤ 10 giây (dev: ~4,4 giây)']),
    T('H', '003', 'Chuyển trang nhanh hơn lần tải đầu', 'P2', 'Đang xem kết quả 1 tháng',
      ['1. Sang trang 2, đo thời gian'], '', ['- Nhanh hơn lần tải đầu (không tính lại dòng Tổng cộng); dòng Tổng cộng không đổi']),
]

SECTIONS = [
    ('I', 'GIAO DIỆN', S_UI),
    ('II', 'BỘ LỌC & TÌM KIẾM', S_LOC),
    ('III', 'SỐ LIỆU & DÒNG TỔNG', S_SO),
    ('IV', 'LUỒNG PHÁT SINH CHỨNG TỪ', S_PS),
    ('V', 'POPUP CHI TIẾT CHỨNG TỪ', S_POP),
    ('VI', 'XUẤT EXCEL', S_X),
    ('VII', 'HIỆU NĂNG', S_HN),
]

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name=TEN + ' - Cập nhật ngày ' + NGAY, module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS,
          role_section_title='Phân quyền & phạm vi dữ liệu')
    print('Số TC theo nhóm:', dict(CNT), 'tổng', sum(CNT.values()))

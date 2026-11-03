# -*- coding: utf-8 -*-
"""Testcase "Bảng đối chiếu công nợ 1 khách hàng" (HRM: phân hệ Bán hàng > Báo cáo > Báo cáo công nợ > Đối chiếu công nợ 1 KH).

Viết mới theo code HRM hiện tại (02/11/2026) — form 17 cột, engine testcase-documenter/assets/tc_engine.py.
Ý tưởng nhóm "luồng phát sinh" theo khuôn data_change_tcs (chỉ dùng chứng từ HRM lập được; chứng từ khác ghi "có sẵn").
Số liệu mẫu đọc trên dev 02/11/2026 (KH CÔNG TY CỔ PHẦN BÁCH LIÊN, 01/01/2026 - 30/06/2026) — môi trường test khác
thì ghi lại số thật vào cột Ghi chú.
Chạy: python gen_testcase.py
"""
import os
import sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(GOPDB, 'danh-muc-kho', 'docs'))
import _lib_win as L  # noqa: E402,F401  (đặt sys.path tới tc_engine)
from tc_engine import build  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

NGAY = L.NGAY
TEN = 'Bảng đối chiếu công nợ 1 khách hàng'
MODULE = 'BC đối chiếu công nợ 1 KH'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
COUNT = OrderedDict()


def L_(*lines):
    return '\n'.join(lines)


def T(n, func, prio, pre, steps, data, exp):
    def j(x):
        return x if isinstance(x, str) else L_(*x)
    return (n, func, prio, j(pre), j(steps), j(data), j(exp))


MENU = 'Vào phân hệ Bán hàng > Báo cáo > nhóm Báo cáo công nợ > bấm "Đối chiếu công nợ 1 KH"'
LOC = 'chọn Thời gian 01/01/2026 - 30/06/2026, Khách hàng KH-TEST'
Q = 'Xem báo cáo đối soát công nợ khách hàng theo'
MENU_PX = 'Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Xuất hàng > Phiếu xuất hàng'
MENU_PT = 'Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu thu'
MENU_BC = 'Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu báo có'
MENU_PC = 'Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu chi'
MENU_UNC = 'Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu ủy nhiệm chi'
MENU_PKT = 'Tài chính > Sổ tổng hợp > Phiếu kế toán'
MENU_YCDC = 'Bán hàng > Yêu cầu > Công nợ - Thu - Chi > YC điều chỉnh công nợ'
MENU_NH = 'Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Nhập hàng > Phiếu nhập hàng'
MENU_BS = 'Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Mượn hàng > Phiếu xuất bán hàng mượn'

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Báo cáo chỉ đọc: đối chiếu công nợ phải thu của 1 (hoặc nhiều) khách hàng trong kỳ, theo từng hợp đồng và từng chứng từ.',
        'Chức năng: Xem báo cáo, Tìm kiếm / lọc, Xem danh sách hàng hóa của phiếu xuất (popup), In, Xuất Excel.',
        'Đường vào: ' + MENU + '.',
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Bút toán ghi sổ tài khoản phải thu khách hàng (131 và tài khoản con) của khách hàng đã chọn.',
        'Bảng: dòng Tổng cộng -> dòng hợp đồng (chữ đậm, STT 1, 2…) -> dòng chứng từ của hợp đồng (STT 1.1, 1.2…).',
        '12 cột: STT | Ngày chứng từ | Số chứng từ | Diễn giải | Số dư đầu kỳ | Phát sinh tăng (Hàng hóa/Dịch vụ, Điều chỉnh công nợ) | '
        'Phát sinh giảm (Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ) | Trả lại tiền thừa | Số dư cuối kỳ.',
        'Chứng từ nguồn: phiếu xuất hàng, phiếu xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, khai báo công nợ đầu kỳ, '
        'phiếu kế toán điều chỉnh công nợ, phiếu nhập hàng trả lại, phiếu thu, phiếu báo có, phiếu chi, ủy nhiệm chi.',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '- Hợp đồng có 7 cột phát sinh đều bằng 0 (so phần nguyên): không lên bảng.',
        '- Bút toán chưa gắn hợp đồng: không thành dòng nhưng VẪN cộng vào dòng Tổng cộng.',
        '- Chứng từ chưa hạch toán (chưa ghi sổ): không tính.',
        '- Bút toán có ngày hạch toán sau Đến ngày: không tính.',
        '- Hợp đồng ngoài phạm vi quyền của người xem.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô Thời gian (bắt buộc) lọc theo NGÀY HẠCH TOÁN của chứng từ, tính cả 2 đầu mút.',
        'Trong kỳ = Từ ngày đến hết Đến ngày; trước Từ ngày = đầu kỳ (chỉ vào Số dư đầu kỳ của dòng Tổng cộng).',
        'Mặc định để trống; mở màn / F5 / Làm mới đều về trống.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Cấp 1: dòng Tổng cộng (1 dòng).',
        'Cấp 2: dòng hợp đồng, xếp theo thứ tự hợp đồng được tạo; phân trang theo hợp đồng (mặc định 10).',
        'Cấp 3: dòng chứng từ trong kỳ của hợp đồng, xếp theo ngày hạch toán, cùng ngày theo thời điểm tạo.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '- Mỗi chứng từ gom 1 dòng / hợp đồng (nhiều bút toán của cùng chứng từ cộng lại).',
        '- Số dư cuối kỳ dòng chứng từ = cộng dồn từ chứng từ đầu của hợp đồng: dòng trên + HH/DV - Nhập trả lại - Đã thanh toán + Trả lại tiền thừa.',
        '- Số dư cuối kỳ dòng hợp đồng = HH/DV - Nhập trả lại - Đã thanh toán + Trả lại tiền thừa (KHÔNG tính đầu kỳ và 2 cột Điều chỉnh công nợ).',
        '- Số dư cuối kỳ dòng Tổng cộng = Đầu kỳ + HH/DV + ĐCCN tăng - Nhập trả lại - Đã thanh toán - ĐCCN giảm + Trả lại tiền thừa.',
    )),
    ('7. Phân quyền cấp', L_(
        'Màn không chặn quyền vào; mọi người dùng đăng nhập đều thấy menu và mở được. 4 quyền chỉ mở rộng phạm vi:',
        '- "%s tổng công ty": mọi công ty; ô lọc Công ty, Phòng ban, Bộ phận, Nhân viên.' % Q,
        '- "%s công ty": công ty đang làm việc + hợp đồng mình tạo; ô Phòng ban, Bộ phận, Nhân viên.' % Q,
        '- "%s phòng ban": phòng ban mình quản lý + hợp đồng mình tạo; ô Phòng ban, Bộ phận, Nhân viên.' % Q,
        '- "%s bộ phận": bộ phận mình quản lý + hợp đồng mình tạo; ô Bộ phận, Nhân viên.' % Q,
        '- Không quyền: chỉ hợp đồng do mình tạo; không có ô lọc tổ chức.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Hàng hóa/Dịch vụ = Nợ - Có của phiếu xuất hàng, xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, hạch toán DV BH-SC (+ Nợ của khai báo công nợ đầu kỳ).',
        'Điều chỉnh công nợ tăng / giảm = Nợ / Có của phiếu kế toán điều chỉnh công nợ.',
        'Nhập trả lại = Có - Nợ của phiếu nhập hàng trả lại. Đã thanh toán = Có của phiếu thu, phiếu báo có, khai báo đầu kỳ.',
        'Trả lại tiền thừa = Nợ của phiếu chi, ủy nhiệm chi. Số dư đầu kỳ = Nợ - Có trước Từ ngày (chỉ dòng Tổng cộng).',
        'Chân bảng "Hiển thị a–b / N hợp đồng".',
    )),
    ('9. Ghi chú đọc bảng', L_(
        '- Số dạng 1,234,567, không phần lẻ; ô bằng 0 để trống, riêng dòng Tổng cộng trên màn in "0".',
        '- Tổng Số dư cuối kỳ các dòng hợp đồng KHÁC dòng Tổng cộng (do khác công thức) — không phải lỗi.',
        '- Ô tìm nhanh chỉ thu hẹp danh sách hợp đồng, KHÔNG đổi dòng Tổng cộng; ô Số hợp đồng có đổi dòng Tổng cộng.',
        'Dữ liệu mẫu: KH-TEST = khách hàng có >= 2 hợp đồng bán hàng do NV-A tạo, có phiếu xuất hàng trong kỳ; HD-TEST-01 = 1 hợp đồng của KH-TEST.',
        'TK-SA (quyền tổng công ty), TK-CT (quyền công ty A), TK-PB (quyền phòng ban, quản lý phòng P1), TK-BP (quyền bộ phận), NV-A (không quyền, người tạo HD-TEST-01), NV-B (không quyền, không tạo hợp đồng nào của KH-TEST).',
    )),
]

ROLE_TCS = [
    T('00', 'Người không có quyền vẫn vào được màn, chỉ thấy hợp đồng do mình tạo', 'P0',
      'NV-A không có quyền nào của nhóm "Bảng đối chiếu công nợ 1 khách hàng"; HD-TEST-01 do NV-A tạo',
      ['1. Đăng nhập NV-A', '2. ' + MENU, '3. ' + LOC],
      'Tài khoản NV-A',
      ['- Menu có mục "Đối chiếu công nợ 1 KH", màn mở bình thường',
       '- Khu vực lọc KHÔNG có ô Công ty, Phòng ban, Bộ phận, Nhân viên',
       '- Bảng chỉ có hợp đồng do NV-A tạo (có HD-TEST-01), không có hợp đồng của người khác',
       '- Dòng Tổng cộng và Số dư đầu kỳ chỉ cộng bút toán của hợp đồng do NV-A tạo']),
    T('01', 'Người không quyền, không tạo hợp đồng nào của khách', 'P1',
      'NV-B không quyền, không tạo hợp đồng nào của KH-TEST',
      ['1. Đăng nhập NV-B', '2. ' + MENU, '3. ' + LOC],
      'Tài khoản NV-B',
      ['- Bảng hiện "Không có dữ liệu phù hợp bộ lọc."', '- Không hiện dòng Tổng cộng, không có chân bảng']),
    T('02', 'Quyền theo tổng công ty thấy mọi hợp đồng + đủ 4 ô lọc tổ chức', 'P0',
      'TK-SA có quyền "%s tổng công ty"' % Q,
      ['1. Đăng nhập TK-SA', '2. ' + MENU, '3. ' + LOC],
      '-',
      ['- Có 4 ô Công ty, Phòng ban, Bộ phận, Nhân viên',
       '- Bảng có mọi hợp đồng của KH-TEST (của mọi công ty, mọi người tạo)',
       '- Ghi lại Tổng cộng làm số đối chiếu cho các TC phân quyền sau']),
    T('03', 'Quyền theo công ty chỉ thấy công ty đang làm việc + hợp đồng mình tạo', 'P0',
      'TK-CT có quyền "%s công ty", đang làm việc ở Công ty A; KH-TEST có hợp đồng ở Công ty A và Công ty B' % Q,
      ['1. Đăng nhập TK-CT (chọn Công ty A)', '2. ' + MENU, '3. ' + LOC, '4. Đổi công ty đang làm việc sang Công ty B, lọc lại'],
      '-',
      ['- Không có ô Công ty; có ô Phòng ban, Bộ phận, Nhân viên',
       '- Bước 3: chỉ hợp đồng có bút toán thuộc Công ty A (và hợp đồng TK-CT tạo); Tổng cộng nhỏ hơn hoặc bằng số của TC-ROLE-02',
       '- Bước 4: số liệu đổi theo Công ty B']),
    T('04', 'Quyền theo phòng ban chỉ thấy phòng mình quản lý', 'P1',
      'TK-PB có quyền "%s phòng ban", quản lý phòng P1' % Q,
      ['1. Đăng nhập TK-PB', '2. ' + MENU, '3. ' + LOC],
      '-',
      ['- Có ô Phòng ban, Bộ phận, Nhân viên; không có ô Công ty',
       '- Chỉ hợp đồng có bút toán thuộc phòng P1 (và hợp đồng TK-PB tạo)']),
    T('05', 'Quyền theo bộ phận chỉ thấy bộ phận mình quản lý', 'P1',
      'TK-BP có quyền "%s bộ phận"' % Q,
      ['1. Đăng nhập TK-BP', '2. ' + MENU, '3. ' + LOC],
      '-',
      ['- Chỉ có ô Bộ phận, Nhân viên', '- Chỉ hợp đồng có bút toán thuộc bộ phận TK-BP quản lý (và hợp đồng TK-BP tạo)']),
    T('06', 'Có nhiều quyền thì lấy cấp cao nhất', 'P2',
      'Tài khoản có cả quyền theo bộ phận và theo công ty',
      ['1. Đăng nhập', '2. ' + MENU, '3. ' + LOC],
      '-',
      ['- Ô lọc và số liệu giống tài khoản chỉ có quyền theo công ty (TC-ROLE-03)']),
    T('07', 'Phạm vi áp cho cả Excel và bản In', 'P1',
      'NV-A không quyền (như TC-ROLE-00)',
      ['1. ' + LOC, '2. Bấm Xuất Excel > Xuất file', '3. Bấm In'],
      '-',
      ['- File Excel và bản xem trước chỉ có hợp đồng do NV-A tạo, dòng Tổng cộng khớp màn hình']),
]

# ------------------------------------------------------------------ I. GIAO DIỆN
S1 = [
    T('001', 'Mở màn từ menu', 'P0', 'Đã đăng nhập',
      ['1. ' + MENU],
      '-',
      ['- Tiêu đề trang và tiêu đề bảng "Bảng đối chiếu công nợ 1 khách hàng", cạnh tiêu đề trang có icon ⓘ',
       '- Bảng hiện "Chọn thời gian và khách hàng để xem bảng đối chiếu.", không tự tải số liệu',
       '- Nhóm Báo cáo công nợ có các mục: Đối chiếu công nợ 1 KH, Tổng hợp công nợ theo NV, Chi tiết công nợ KH']),
    T('002', 'Bố cục khu vực lọc và nút', 'P1', 'TK-SA',
      ['1. Mở màn', '2. Quan sát khung "Bộ lọc danh sách" và hàng nút trên bảng'],
      '-',
      ['- Ô tìm nhanh, gợi ý "Tìm theo số hợp đồng hoặc số chứng từ"; nút Tìm kiếm, Làm mới, Cài đặt bộ lọc, Ẩn tìm kiếm nâng cao',
       '- Hàng 1: Thời gian * (Từ ngày -> Đến ngày), Khách hàng *, Số hợp đồng',
       '- Hàng 2: Công ty, Phòng ban, Bộ phận, Nhân viên',
       '- Trên bảng: nút In, Xuất Excel (In đứng trước)']),
    T('003', 'Tiêu đề cột 2 tầng, đủ và đúng thứ tự', 'P0', 'Đang mở màn',
      ['1. Đọc tiêu đề bảng từ trái sang phải'],
      '-',
      ['- STT | Ngày chứng từ | Số chứng từ | Diễn giải | Số dư đầu kỳ | Phát sinh tăng trong kỳ (Hàng hóa/Dịch vụ, Điều chỉnh công nợ) | '
       'Phát sinh giảm trong kỳ (Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ) | Trả lại tiền thừa | Số dư cuối kỳ',
       '- Mỗi tiêu đề có icon ⓘ']),
    T('004', 'Nội dung icon ⓘ của tiêu đề cột', 'P2', 'Đang mở màn',
      ['1. Rê chuột vào ⓘ của cột Số dư cuối kỳ', '2. Rê chuột vào ⓘ của cột Đã thanh toán'],
      '-',
      ['- Bước 1: dòng đầu "Công nợ khách hàng còn phải trả đến hết Đến ngày", có 3 dòng công thức cho dòng Tổng cộng, dòng hợp đồng, dòng chứng từ',
       '- Bước 2: "Số tiền khách đã thanh toán trong kỳ" - "Đã thanh toán = Tổng ghi Có của phiếu thu, phiếu báo có và khai báo công nợ đầu kỳ."']),
    T('005', 'Bảng có số liệu: phân biệt 3 loại dòng', 'P0', 'KH-TEST có >= 2 hợp đồng phát sinh trong kỳ',
      ['1. ' + LOC],
      'Kỳ 01/01/2026 - 30/06/2026',
      ['- Dòng đầu "Tổng cộng" (gộp 4 cột đầu, nền xám, có ⓘ)',
       '- Dòng hợp đồng chữ đậm nền xám nhạt, STT 1, 2…, cột Ngày chứng từ trống',
       '- Dòng chứng từ STT 1.1, 1.2…, có Ngày chứng từ',
       '- Tiêu đề bảng dính khi cuộn dọc; có thanh cuộn ngang ở cả trên và dưới bảng']),
    T('006', 'Chân bảng và phân trang', 'P1', 'KH-TEST có > 10 hợp đồng phát sinh',
      ['1. ' + LOC, '2. Đọc chân bảng', '3. Mở ô Số dòng/trang'],
      '-',
      ['- Chân bảng "Hiển thị 1–10 / N hợp đồng"', '- Ô Số dòng/trang có 10, 20, 50, 100, mặc định 10']),
]

# ------------------------------------------------------------------ II. BỘ LỌC
S2 = [
    T('001', 'Mặc định mọi ô lọc trống', 'P1', 'Lần đầu mở màn (hoặc đã quá 10 phút)',
      ['1. Mở màn'], '-', ['- Thời gian, Khách hàng, Số hợp đồng, ô tìm nhanh, các ô tổ chức đều trống']),
    T('002', 'Bấm Tìm kiếm khi chưa chọn ô bắt buộc', 'P0', 'Đang mở màn, chưa chọn gì',
      ['1. Bấm Tìm kiếm'], '-',
      ['- Dưới ô Thời gian: "Vui lòng chọn thời gian"; dưới ô Khách hàng: "Vui lòng chọn khách hàng" (chữ đỏ)',
       '- Bảng vẫn hiện lời nhắc, không tải số liệu']),
    T('003', 'Chữ đỏ tự tắt khi chọn đủ', 'P2', 'Đang có chữ đỏ (TC_02.002)',
      ['1. Chọn Thời gian', '2. Chọn Khách hàng'], '-',
      ['- Chọn xong ô nào thì chữ đỏ của ô đó tắt', '- Đủ 2 ô: bảng tự tải số liệu, không cần bấm Tìm kiếm']),
    T('004', 'Chỉ chọn Khách hàng, chưa chọn Thời gian', 'P1', 'Đang mở màn',
      ['1. Chọn KH-TEST'], '-', ['- Bảng vẫn hiện "Chọn thời gian và khách hàng để xem bảng đối chiếu."']),
    T('005', 'Ô Khách hàng cần gõ từ 2 ký tự', 'P2', 'Đang mở màn',
      ['1. Bấm ô Khách hàng, gõ 1 ký tự', '2. Gõ thêm 1 ký tự'], 'Từ khoá: "BÁ" (khách hàng BÁCH LIÊN)',
      ['- Bước 1: chưa hiện kết quả', '- Bước 2: hiện danh sách khách hàng dạng "Mã KH - Tên khách hàng"']),
    T('006', 'Chọn nhiều khách hàng', 'P1', 'KH-TEST và KH-TEST-2 cùng có phát sinh trong kỳ',
      ['1. Chọn Thời gian', '2. Chọn KH-TEST, ghi Tổng cộng', '3. Chọn thêm KH-TEST-2'], '-',
      ['- Bước 3: bảng gồm hợp đồng của cả 2 khách', '- Các cột phát sinh của Tổng cộng = tổng khi xem riêng từng khách']),
    T('007', 'Lịch không cho chọn ngày ngược chiều', 'P1', 'Đang mở màn',
      ['1. Chọn Từ ngày 30/06/2026', '2. Mở lịch Đến ngày, thử bấm 01/01/2026', '3. Gõ tay 01/01/2026 vào Đến ngày, Enter'],
      'Từ 30/06/2026, Đến 01/01/2026',
      ['- Bước 2: các ngày trước 30/06/2026 bị khoá, không bấm được',
       '- Bước 3: ô Đến ngày không nhận ngày nhỏ hơn Từ ngày; không có lỗi "Lỗi khi tải dữ liệu"',
       '- Ghi lại giá trị thực tế ô Đến ngày hiển thị sau bước 3 vào cột Ghi chú']),
    T('008', 'Từ ngày = Đến ngày (1 ngày)', 'P2', 'KH-TEST có chứng từ hạch toán ngày X',
      ['1. Chọn Thời gian X - X, KH-TEST'], 'X = ngày hạch toán của 1 chứng từ',
      ['- Chỉ có chứng từ hạch toán đúng ngày X', '- Số dư đầu kỳ = công nợ trước ngày X']),
    T('009', 'Tính cả 2 đầu mút của kỳ', 'P1', 'KH-TEST có chứng từ C1 hạch toán ngày D1, chứng từ C2 ngày D2 (D1 < D2)',
      ['1. Lọc Thời gian D1 - D2', '2. Lọc D1+1 - D2', '3. Lọc D1 - D2-1'], '-',
      ['- Bước 1: có cả C1, C2', '- Bước 2: không có C1; số của C1 chuyển vào Số dư đầu kỳ', '- Bước 3: không có C2']),
    T('010', 'Ô Số hợp đồng lọc gần đúng và đổi dòng Tổng cộng', 'P0', 'KH-TEST có HD-TEST-01 và hợp đồng khác',
      ['1. ' + LOC + ', ghi Tổng cộng', '2. Nhập 1 phần số của HD-TEST-01 vào ô Số hợp đồng, Enter'],
      'Một đoạn giữa số HD-TEST-01',
      ['- Chỉ còn hợp đồng có số chứa đoạn đã nhập', '- Dòng Tổng cộng (kể cả Số dư đầu kỳ) tính lại chỉ theo các hợp đồng đó',
       '- Chỉ áp khi Enter / Tìm kiếm, gõ chưa Enter thì bảng chưa đổi']),
    T('011', 'Ô tìm nhanh thu hẹp hợp đồng, KHÔNG đổi Tổng cộng', 'P0', 'KH-TEST có nhiều hợp đồng',
      ['1. ' + LOC + ', ghi Tổng cộng', '2. Gõ số 1 phiếu xuất của hợp đồng thứ 2 vào ô tìm nhanh, bấm Tìm kiếm'],
      'Dev: KH TOYOTA HÀ ĐÔNG, 01/01-31/10/2026, từ khoá PXBHM-04941',
      ['- Chỉ còn hợp đồng có chứng từ đó (hiện đủ mọi chứng từ của hợp đồng)', '- Dòng Tổng cộng giữ nguyên số ở bước 1',
       '- Chân bảng "Hiển thị 1–1 / 1 hợp đồng"']),
    T('012', 'Ô tìm nhanh không khớp gì', 'P2', '-',
      ['1. ' + LOC, '2. Tìm nhanh "ZZZ999", Enter'], '-',
      ['- Bảng hiện "Không có dữ liệu phù hợp bộ lọc."']),
    T('013', 'Lọc Nhân viên = người tạo hợp đồng', 'P1', 'TK-SA; HD-TEST-01 do NV-A tạo',
      ['1. ' + LOC, '2. Ô Nhân viên chọn NV-A'], '-',
      ['- Chỉ còn hợp đồng bán hàng / hợp đồng dịch vụ SC-BD-BT do NV-A tạo', '- Dòng Tổng cộng tính lại theo các hợp đồng đó']),
    T('014', 'Lọc Công ty / Phòng ban / Bộ phận theo hồ sơ người tạo hợp đồng', 'P1', 'TK-SA; NV-A thuộc phòng P1',
      ['1. ' + LOC, '2. Chọn Công ty A', '3. Chọn thêm Phòng ban P1', '4. Chọn thêm Bộ phận của NV-A'], '-',
      ['- Mỗi bước bảng tải lại ngay (không cần Tìm kiếm), số hợp đồng giảm dần hoặc giữ nguyên',
       '- Phòng ban chỉ liệt kê phòng của công ty đã chọn; Bộ phận chỉ của phòng đã chọn']),
    T('015', 'Lọc tổ chức loại các loại hợp đồng khác và bút toán chưa gắn hợp đồng', 'P2',
      'KH-TEST có bút toán chưa gắn hợp đồng hoặc hợp đồng mở đầu kỳ',
      ['1. ' + LOC + ', ghi Tổng cộng', '2. Chọn ô Công ty = công ty có mọi hợp đồng của KH-TEST'], '-',
      ['- Hợp đồng không phải hợp đồng bán hàng / dịch vụ SC-BD-BT biến mất', '- Các cột phát sinh của Tổng cộng giảm đúng phần bút toán chưa gắn hợp đồng / hợp đồng loại khác']),
    T('016', 'Kết hợp nhiều điều kiện', 'P1', '-',
      ['1. ' + LOC, '2. Nhập Số hợp đồng', '3. Chọn Nhân viên', '4. Nhập tìm nhanh'], '-',
      ['- Kết quả thoả đồng thời mọi điều kiện', '- Chân bảng tính lại theo số hợp đồng còn lại']),
    T('017', 'Làm mới xoá mọi điều kiện', 'P1', 'Đã lọc như TC_02.016',
      ['1. Bấm Làm mới'], '-',
      ['- Mọi ô (kể cả Thời gian, Khách hàng) về trống, chữ đỏ không hiện', '- Bảng về lời nhắc "Chọn thời gian và khách hàng để xem bảng đối chiếu."']),
    T('018', 'Giữ bộ lọc khi rời màn 10 phút, F5 thì xoá', 'P2', 'Đã lọc có số liệu',
      ['1. Mở màn khác rồi quay lại trong 10 phút', '2. Bấm F5'], '-',
      ['- Bước 1: giữ nguyên bộ lọc và bảng', '- Bước 2: mọi ô về trống, bảng về lời nhắc']),
    T('019', 'Đổi bộ lọc liên tục chỉ hiện kết quả lần cuối', 'P2', 'KH-TEST và KH-TEST-2 có số liệu khác nhau',
      ['1. ' + LOC, '2. Liên tiếp bỏ KH-TEST, chọn KH-TEST-2 thật nhanh'], '-',
      ['- Bảng cuối cùng là số của KH-TEST-2, không bị số của KH-TEST đè lên', '- "Đang tải dữ liệu..." tắt khi số mới về']),
]

# ------------------------------------------------------------------ III. SỐ LIỆU
S3 = [
    T('001', 'Cột Hàng hóa/Dịch vụ dòng hợp đồng = tổng các dòng chứng từ', 'P0', 'Dev: KH CÔNG TY CỔ PHẦN BÁCH LIÊN, 01/01-30/06/2026',
      ['1. Lọc như Tiền điều kiện', '2. Đọc hợp đồng 2 và các dòng 2.1, 2.2, 2.3'], '-',
      ['- Hợp đồng 2 (HĐ_TPE_HN_KD2_26_0267_236): Hàng hóa/Dịch vụ 663,120 = 259,200 (2.1) + 403,920 (2.2)',
       '- Điều chỉnh công nợ giảm 663,120 = dòng 2.3']),
    T('002', 'Các cột phát sinh dòng Tổng cộng = tổng các dòng hợp đồng (khách không có bút toán chưa gắn hợp đồng)', 'P0', 'Như TC_03.001',
      ['1. Cộng từng cột của 10 dòng hợp đồng'], '-',
      ['- Hàng hóa/Dịch vụ: 16,173,540; Điều chỉnh công nợ giảm: 9,601,740 — bằng dòng Tổng cộng',
       '- Các cột còn lại của Tổng cộng in "0"']),
    T('003', 'Số dư cuối kỳ dòng Tổng cộng theo công thức', 'P0', 'Như TC_03.001',
      ['1. Tính: Đầu kỳ + HH/DV + ĐCCN tăng - Nhập trả lại - Đã thanh toán - ĐCCN giảm + Trả lại tiền thừa'], '-',
      ['- -2,251,800 + 16,173,540 + 0 - 0 - 0 - 9,601,740 + 0 = 4,320,000 = Số dư cuối kỳ dòng Tổng cộng']),
    T('004', 'Số dư cuối kỳ dòng hợp đồng KHÔNG trừ điều chỉnh công nợ', 'P0', 'Như TC_03.001',
      ['1. Đọc hợp đồng 1'], '-',
      ['- Hàng hóa/Dịch vụ 7,506,000, Điều chỉnh công nợ giảm 5,254,200, Số dư cuối kỳ 7,506,000 (không trừ 5,254,200)',
       '- Ghi nhận đúng thiết kế (không ghi Failed): tổng Số dư cuối kỳ các dòng hợp đồng khác dòng Tổng cộng']),
    T('005', 'Số dư cuối kỳ dòng chứng từ cộng dồn', 'P0', 'Như TC_03.001',
      ['1. Đọc cột Số dư cuối kỳ dòng 2.1, 2.2, 2.3'], '-',
      ['- 2.1: 259,200; 2.2: 663,120; 2.3 (phiếu điều chỉnh giảm): vẫn 663,120',
       '- Dòng chứng từ cuối của hợp đồng có Số dư cuối kỳ = Số dư cuối kỳ dòng hợp đồng']),
    T('006', 'Số dư đầu kỳ chỉ ở dòng Tổng cộng', 'P0', 'Như TC_03.001',
      ['1. Đọc cột Số dư đầu kỳ'], '-',
      ['- Tổng cộng: -2,251,800', '- Mọi dòng hợp đồng và chứng từ: để trống']),
    T('007', 'Số dư đầu kỳ = Số dư cuối kỳ của kỳ liền trước', 'P1', 'KH-TEST',
      ['1. Lọc 01/01/2026 - 30/06/2026, ghi Số dư cuối kỳ Tổng cộng = A', '2. Lọc 01/07/2026 - 31/10/2026, đọc Số dư đầu kỳ'],
      'Dev: BÁCH LIÊN: A = 4,320,000',
      ['- Số dư đầu kỳ bước 2 = A (cùng bộ lọc khác)']),
    T('008', 'Hợp đồng toàn số 0 không lên bảng, STT liên tục', 'P1', 'KH-TEST có hợp đồng chỉ có bút toán trước kỳ',
      ['1. ' + LOC, '2. Đọc STT các dòng hợp đồng qua các trang'], '-',
      ['- Không có hợp đồng nào 7 cột phát sinh đều trống', '- STT 1, 2, 3… liên tục qua các trang, trang 1 không trống']),
    T('009', 'Bút toán chưa gắn hợp đồng chỉ vào Tổng cộng', 'P1', 'KH-TEST có chứng từ trong kỳ không gắn hợp đồng (có sẵn)',
      ['1. ' + LOC, '2. So tổng các dòng hợp đồng với dòng Tổng cộng'], '-',
      ['- Không có dòng nào cho chứng từ đó', '- Dòng Tổng cộng lớn hơn tổng các dòng hợp đồng đúng bằng số của chứng từ đó']),
    T('010', 'Thứ tự dòng chứng từ', 'P2', 'Hợp đồng có >= 2 chứng từ cùng ngày hạch toán',
      ['1. Đọc thứ tự dòng chứng từ của hợp đồng'], '-',
      ['- Xếp theo Ngày chứng từ tăng dần; cùng ngày thì chứng từ tạo trước đứng trước (dev: dòng 2.1 PXH-19849, 2.2 PXH-19852 cùng 04/03/2026)']),
    T('011', 'Số chứng từ kèm số phiếu yêu cầu', 'P1', 'Như TC_03.001',
      ['1. Đọc cột Số chứng từ các dòng phiếu xuất'], '-',
      ['- Dạng "PXH-19789 (PYCXH-20388)"', '- Phiếu kế toán chỉ có số phiếu, vd "TPE.PKT0326.00055"']),
    T('012', 'Diễn giải phiếu kế toán / phiếu thu lấy ghi chú của dòng hợp đồng', 'P2', 'Có phiếu kế toán ghi cho 2 hợp đồng với 2 ghi chú khác nhau',
      ['1. Đọc cột Diễn giải ở 2 dòng chứng từ của phiếu đó'], '-',
      ['- Mỗi dòng hiện đúng ghi chú của dòng chi tiết ứng với hợp đồng của nó']),
    T('013', 'Định dạng số và ô bằng 0', 'P1', 'Như TC_03.001',
      ['1. Quan sát các cột số'], '-',
      ['- Số dạng 1,234,567, không phần lẻ; số âm có dấu "-" (vd -2,251,800)',
       '- Ô 0 ở dòng hợp đồng / chứng từ để trống; dòng Tổng cộng in "0"']),
    T('014', 'Chuyển trang không đổi dòng Tổng cộng', 'P1', 'KH-TEST có > 10 hợp đồng',
      ['1. ' + LOC + ', ghi Tổng cộng', '2. Sang trang 2', '3. Đổi Số dòng/trang = 20'], '-',
      ['- Tổng cộng giữ nguyên', '- Bước 3 quay về trang 1, chân bảng "Hiển thị 1–20 / N hợp đồng"',
       '- Chứng từ của 1 hợp đồng không bị cắt sang trang khác']),
    T('015', 'Bấm số hợp đồng / số chứng từ mở tab mới', 'P1', 'Như TC_03.001',
      ['1. Bấm số hợp đồng ở dòng đậm', '2. Bấm số phiếu kế toán ở dòng chứng từ'], '-',
      ['- Mở đúng hợp đồng / phiếu kế toán ở tab mới', '- Màn báo cáo giữ nguyên bộ lọc, trang']),
]

# ------------------------------------------------------------------ IV. LUỒNG PHÁT SINH
BASE = 'Đã có số nền (TC_04.001)'
S4 = [
    T('001', 'Ghi lại số nền', 'P0', 'KH-TEST, HD-TEST-01 do NV-A tạo; kỳ = 01/01/2026 đến hôm nay',
      ['1. ' + MENU, '2. Chọn kỳ đến hôm nay, KH-TEST', '3. Chụp màn hình dòng Tổng cộng và dòng HD-TEST-01'], '-',
      ['- Có đủ 8 cột số của Tổng cộng và HD-TEST-01 để làm số nền cho các TC sau']),
    T('002', 'Phiếu xuất hàng làm tăng Hàng hóa/Dịch vụ', 'P0', BASE + '; có sẵn yêu cầu xuất hàng đã duyệt cho HD-TEST-01',
      ['1. Vào ' + MENU_PX + ', lập phiếu xuất cho yêu cầu đó, hoàn tất để phiếu được hạch toán hôm nay', '2. Lọc lại báo cáo'],
      'Giá trị xuất (gồm thuế): 10,000,000',
      ['- Hàng hóa/Dịch vụ của HD-TEST-01 và Tổng cộng tăng 10,000,000; Số dư cuối kỳ của cả 2 dòng tăng 10,000,000',
       '- Có thêm dòng chứng từ ngày hôm nay, Số chứng từ = "<số phiếu xuất> (<số phiếu yêu cầu>)", bấm vào mở popup Danh sách hàng hóa']),
    T('003', 'Chứng từ chưa hạch toán không làm đổi báo cáo', 'P0', 'Số nền đã cập nhật sau TC trước',
      ['1. Lập phiếu thu 1,000,000 cho HD-TEST-01, để chưa hạch toán', '2. Lọc lại báo cáo'], '-',
      ['- Không cột nào đổi so với số nền']),
    T('004', 'Phiếu thu làm tăng Đã thanh toán', 'P0', BASE,
      ['1. Vào ' + MENU_PT + ', lập phiếu thu của KH-TEST cho HD-TEST-01, hạch toán hôm nay', '2. Lọc lại báo cáo'],
      'Số tiền: 4,000,000',
      ['- Đã thanh toán tăng 4,000,000 ở HD-TEST-01 và Tổng cộng', '- Số dư cuối kỳ của cả 2 dòng giảm 4,000,000',
       '- Dòng chứng từ mới: Diễn giải = ghi chú của dòng HD-TEST-01 trên phiếu thu; bấm số phiếu mở phiếu thu ở tab mới']),
    T('005', 'Phiếu báo có làm tăng Đã thanh toán', 'P1', BASE,
      ['1. Vào ' + MENU_BC + ', lập phiếu báo có của KH-TEST cho HD-TEST-01, hạch toán hôm nay', '2. Lọc lại'],
      '1,000,000', ['- Đã thanh toán tăng 1,000,000; Số dư cuối kỳ giảm 1,000,000 (HD-TEST-01 và Tổng cộng)']),
    T('006', 'Điều chỉnh công nợ TĂNG', 'P0', BASE,
      ['1. Vào ' + MENU_YCDC + ', lập yêu cầu điều chỉnh tăng cho KH-TEST, HD-TEST-01, duyệt đủ', '2. Kế toán lập phiếu ở ' + MENU_PKT + ', hạch toán hôm nay', '3. Lọc lại'],
      'Tăng 2,000,000',
      ['- Cột Điều chỉnh công nợ (nhóm tăng) tăng 2,000,000 ở HD-TEST-01 và Tổng cộng',
       '- Số dư cuối kỳ Tổng cộng tăng 2,000,000',
       '- Ghi nhận đúng thiết kế: Số dư cuối kỳ dòng HD-TEST-01 và dòng chứng từ mới KHÔNG đổi']),
    T('007', 'Điều chỉnh công nợ GIẢM', 'P0', BASE,
      ['1. Lập yêu cầu điều chỉnh giảm KH-TEST, HD-TEST-01, duyệt và lập phiếu kế toán, hạch toán hôm nay', '2. Lọc lại'],
      'Giảm 500,000',
      ['- Cột Điều chỉnh công nợ (nhóm giảm) tăng 500,000; Số dư cuối kỳ Tổng cộng giảm 500,000',
       '- Ghi nhận đúng thiết kế: Số dư cuối kỳ dòng HD-TEST-01 KHÔNG giảm']),
    T('008', 'Khách trả lại hàng làm tăng Nhập trả lại', 'P0', 'HD-TEST-01 đã xuất hàng ở TC_04.002; có sẵn yêu cầu nhập hàng trả lại đã duyệt',
      ['1. Vào ' + MENU_NH + ', lập phiếu nhập hàng trả lại cho yêu cầu đó, hạch toán hôm nay', '2. Lọc lại'],
      'Trả lại 3,000,000',
      ['- Nhập trả lại tăng 3,000,000; Số dư cuối kỳ HD-TEST-01 và Tổng cộng giảm 3,000,000',
       '- Dòng chứng từ: "<số phiếu nhập> (<số phiếu yêu cầu nhập hàng>)"']),
    T('009', 'Phiếu chi trả lại tiền thừa', 'P1', BASE,
      ['1. Vào ' + MENU_PC + ', lập phiếu chi trả tiền thừa cho KH-TEST theo HD-TEST-01, hạch toán hôm nay', '2. Lọc lại'],
      '800,000', ['- Trả lại tiền thừa tăng 800,000; Số dư cuối kỳ HD-TEST-01 và Tổng cộng TĂNG 800,000']),
    T('010', 'Ủy nhiệm chi trả lại tiền thừa', 'P2', BASE,
      ['1. Vào ' + MENU_UNC + ', lập ủy nhiệm chi cho KH-TEST theo HD-TEST-01, hạch toán hôm nay', '2. Lọc lại'],
      '200,000', ['- Trả lại tiền thừa tăng 200,000; Số dư cuối kỳ tăng 200,000']),
    T('011', 'Phiếu xuất bán hàng mượn làm tăng Hàng hóa/Dịch vụ', 'P1', BASE + '; có sẵn yêu cầu xuất bán hàng mượn đã duyệt cho HD-TEST-01',
      ['1. Vào ' + MENU_BS + ', lập phiếu cho yêu cầu đó, hạch toán hôm nay', '2. Lọc lại'],
      '1,500,000', ['- Hàng hóa/Dịch vụ tăng 1,500,000', '- Bấm số phiếu mở popup Danh sách hàng hóa dạng hàng mượn (cột Số lượng)']),
    T('012', 'Chứng từ hạch toán ngoài kỳ', 'P1', 'Đã có các chứng từ hôm nay ở các TC trên',
      ['1. Lọc kỳ 01/01/2026 đến hôm qua', '2. Lọc kỳ từ ngày mai đến cuối tháng'], '-',
      ['- Bước 1: không có các chứng từ hôm nay', '- Bước 2: các chứng từ hôm nay chỉ nằm trong Số dư đầu kỳ, không có dòng hợp đồng / chứng từ nào của chúng']),
    T('013', 'Hạch toán dịch vụ / biên bản thanh lý / khai báo đầu kỳ', 'P2', 'Có sẵn chứng từ các loại này của KH-TEST trong kỳ (lập ở hệ thống khác)',
      ['1. ' + LOC, '2. Tìm dòng chứng từ tương ứng'], '-',
      ['- Hạch toán dịch vụ, biên bản thanh lý: vào cột Hàng hóa/Dịch vụ', '- Khai báo công nợ đầu kỳ: phần ghi Nợ vào Hàng hóa/Dịch vụ, phần ghi Có vào Đã thanh toán']),
]

# ------------------------------------------------------------------ V. POPUP
S5 = [
    T('001', 'Popup hàng hóa của phiếu xuất hàng', 'P0', 'Dev: BÁCH LIÊN, 01/01-30/06/2026',
      ['1. Bấm "PXH-19789 (PYCXH-20388)" (dòng 1.2)'], '-',
      ['- Popup "Danh sách hàng hóa", dòng phụ "Phiếu xuất hàng - PXH-19789"',
       '- Cột: STT, Tên hàng hóa, Model, Mã hàng hóa, Đơn vị tính, SL đề nghị, SL thực xuất, Giá niêm yết, Giảm giá bán, Đơn giá bán, Thành tiền bán',
       '- 1 dòng: XUPER 680CGS, KG, SL 5 / 5, Giá niêm yết 1,390,000, Giảm giá bán trống, Đơn giá bán 1,390,000, Thành tiền bán 6,950,000']),
    T('002', 'Thành tiền bán là giá chưa thuế', 'P2', 'Như TC_05.001',
      ['1. So Thành tiền bán với cột Hàng hóa/Dịch vụ của dòng 1.2'], '-',
      ['- Popup 6,950,000; báo cáo 7,506,000 (chênh do thuế) — đúng thiết kế, ghi nhận không ghi Failed']),
    T('003', 'Popup hàng hóa của phiếu xuất bán hàng mượn', 'P1', 'Dev: KH TOYOTA HÀ ĐÔNG, 01/01-31/10/2026',
      ['1. Tìm nhanh PXBHM-04941', '2. Bấm số phiếu'], '-',
      ['- Dòng phụ "Phiếu xuất bán hàng mượn - PXBHM-04941"', '- Có cột Số lượng; KHÔNG có SL đề nghị, SL thực xuất, Thành tiền bán']),
    T('004', 'Nút Xem chi tiết phiếu và Đóng', 'P1', 'Đang mở popup TC_05.001',
      ['1. Bấm Xem chi tiết phiếu', '2. Quay lại tab báo cáo, bấm Đóng'], '-',
      ['- Bước 1: mở phiếu xuất hàng ở tab mới', '- Bước 2: popup đóng, bảng giữ nguyên trang và bộ lọc']),
    T('005', 'Số chứng từ khác không mở popup', 'P2', 'Như TC_05.001',
      ['1. Bấm số phiếu kế toán TPE.PKT0326.00055'], '-', ['- Không mở popup; mở phiếu kế toán ở tab mới']),
]

# ------------------------------------------------------------------ VI. XUẤT EXCEL / IN
S6 = [
    T('001', 'Xuất Excel / In khi chưa chọn đủ', 'P0', 'Đang mở màn, chưa chọn gì',
      ['1. Bấm Xuất Excel', '2. Bấm In'], '-',
      ['- Cả 2 lần báo "Vui lòng chọn khách hàng và thời gian", không mở cửa sổ']),
    T('002', 'Cửa sổ Chọn trường xuất Excel', 'P1', 'Đã lọc có số liệu',
      ['1. Bấm Xuất Excel'], '-',
      ['- Tiêu đề "Chọn trường xuất Excel"; 11 trường đã tích: Ngày chứng từ, Số chứng từ, Diễn giải, Số dư đầu kỳ, PS tăng - Hàng hóa/Dịch vụ, '
       'PS tăng - Điều chỉnh công nợ, PS giảm - Nhập trả lại, PS giảm - Đã thanh toán, PS giảm - Điều chỉnh công nợ, Trả lại tiền thừa, Số dư cuối kỳ',
       '- "Đang chọn 11/11 trường"; nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng', '- Bỏ chọn hết: nút Xuất file bị khoá']),
    T('003', 'Nội dung file Excel', 'P0', 'Dev: BÁCH LIÊN, 01/01-30/06/2026',
      ['1. Bấm Xuất Excel > Xuất file', '2. Mở file'], '-',
      ['- Tên file bang_doi_chieu_cong_no_1_khach_hang.xlsx, sheet "Đối chiếu công nợ"; báo "Xuất Excel thành công"',
       '- Dòng 1 "BẢNG ĐỐI CHIẾU CÔNG NỢ KHÁCH HÀNG"; dòng 2 "Khách hàng: 29TPHPHO-209 - CÔNG TY CỔ PHẦN BÁCH LIÊN"; dòng 3 "Thời gian: 01/01/2026 - 30/06/2026"',
       '- Tiêu đề 2 tầng, cột STT đầu tiên; dòng Tổng cộng: -2,251,800 | 16,173,540 | … | 9,601,740 | … | 4,320,000',
       '- 37 dòng: 5 dòng đầu + Tổng cộng + 10 hợp đồng (in đậm) + 21 chứng từ; số là kiểu số, định dạng 1,234,567']),
    T('004', 'Excel theo trường đã chọn và thứ tự kéo', 'P1', 'Đã lọc có số liệu',
      ['1. Bỏ tích Diễn giải, kéo Số dư cuối kỳ lên đầu', '2. Xuất file'], '-',
      ['- File không có cột Diễn giải; sau STT là Số dư cuối kỳ', '- Các trường PS tăng / PS giảm không đứng liền nhau thì không gộp tiêu đề nhóm']),
    T('005', 'Excel lấy mọi trang và theo bộ lọc đang áp', 'P1', 'KH-TEST có > 10 hợp đồng',
      ['1. Lọc, đang ở trang 1', '2. Xuất file', '3. Nhập tìm nhanh 1 số chứng từ, xuất lại'], '-',
      ['- Bước 2: đủ mọi hợp đồng (bằng N ở chân bảng)', '- Bước 3: chỉ hợp đồng khớp tìm nhanh, dòng Tổng cộng như màn hình']),
    T('006', 'Ô bằng 0 trong Excel', 'P3', 'Như TC_06.003',
      ['1. Xem các ô 0 của dòng Tổng cộng trong file'], '-',
      ['- Ghi lại thực tế: trên màn dòng Tổng cộng in "0", trong file ô 0 hiển thị trống (giá trị vẫn là 0)']),
    T('007', 'Xem trước bản in', 'P0', 'Dev: BÁCH LIÊN, 01/01-30/06/2026',
      ['1. Bấm In'], '-',
      ['- Cửa sổ "Xem trước bảng đối chiếu công nợ khách hàng", khổ ngang, có nút In',
       '- Mẫu "BÁO CÁO ĐỐI SOÁT CÔNG NỢ KHÁCH HÀNG", ngày in, Khách hàng: CÔNG TY CỔ PHẦN BÁCH LIÊN, Từ ngày 01/01/2026, Đến ngày 30/06/2026',
       '- Bảng đủ 10 hợp đồng (mọi trang), dòng Tổng cộng ngay dưới tiêu đề khớp màn hình',
       '- Bấm In trong cửa sổ in ra máy in, không mở tab mới']),
    T('008', 'In vượt 2.000 dòng', 'P2', 'Khách hàng có > 2.000 dòng (hợp đồng + chứng từ) trong kỳ dài',
      ['1. Lọc kỳ dài', '2. Bấm In'], '-',
      ['- Cửa sổ chỉ hiện "Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài."',
       '- Không có nút In']),
]

# ------------------------------------------------------------------ VII. HIỆU NĂNG
S7 = [
    T('001', 'Mở màn không lọc', 'P1', '-',
      ['1. ' + MENU + ', đo thời gian tới khi màn hiện đủ'], '-',
      ['- Dưới 3 giây; bảng hiện lời nhắc, không tải số liệu (báo cáo bắt buộc chọn khách hàng + thời gian)']),
    T('002', 'Tải 1 khách hàng kỳ 6 tháng', 'P1', 'Dev: BÁCH LIÊN, 01/01-30/06/2026 (10 hợp đồng)',
      ['1. Chọn đủ bộ lọc, đo thời gian từ lúc chọn khách tới khi bảng có dòng'], '-',
      ['- Dưới 2 giây (dev 02/11/2026: khoảng 0,3–0,6 giây)']),
    T('003', 'Khách hàng nhiều hợp đồng, 100 hợp đồng / trang', 'P2', 'Khách hàng có > 200 hợp đồng phát sinh trong 10 tháng',
      ['1. Lọc kỳ 01/01-31/10/2026', '2. Đổi Số dòng/trang = 100', '3. Xuất Excel'], '-',
      ['- Bước 2 dưới 5 giây (dev: khách 218 hợp đồng khoảng 2,3 giây)', '- Bước 3 xuất xong dưới 30 giây, màn không treo']),
]

SECTIONS = [
    ('I', 'GIAO DIỆN', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'SỐ LIỆU', S3),
    ('IV', 'LUỒNG PHÁT SINH', S4),
    ('V', 'POPUP DANH SÁCH HÀNG HÓA', S5),
    ('VI', 'XUẤT EXCEL & IN', S6),
    ('VII', 'HIỆU NĂNG', S7),
]

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name=TEN + ' - Cập nhật ngày ' + NGAY, module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS,
          role_section_title='Phân quyền & phạm vi dữ liệu')
    print('Phân quyền & phạm vi:', len(ROLE_TCS))
    for code, title, items in SECTIONS:
        print('%s %s: %d' % (code, title, len(items)))
    print('Tổng:', len(ROLE_TCS) + sum(len(s[2]) for s in SECTIONS))

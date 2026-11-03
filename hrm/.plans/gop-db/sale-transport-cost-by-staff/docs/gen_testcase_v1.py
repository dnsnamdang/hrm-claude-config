# -*- coding: utf-8 -*-
"""Testcase "BC chi phí vận chuyển theo NV kinh doanh" (HRM: Bán hàng > Báo cáo > Vận chuyển, và Vận chuyển > Báo cáo
vận chuyển) — form 17 cột, engine tc_engine.py.

Viết MỚI theo code HRM hiện tại (02/11/2026). TC cũ của màn ERP (erp/.plans/erp-bao-cao-chi-phi-van-chuyen-theo-nvkd/)
chỉ tham khảo ý tưởng, không chép. Số liệu ví dụ lấy trên dev-hrm 02/11/2026 (hdsd_shots/_capture_log.json) — môi
trường test khác thì tester ghi lại số thật ở cột Ghi chú.
Không dùng ký tự mũi tên / biểu tượng (engine coi là emoji).
Chạy: python gen_testcase.py
"""
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'danh-muc-kho', 'docs'))
import _lib_win as L  # noqa: E402,F401  (đặt sys.path tới tc_engine)
from tc_engine import build  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

TEN = 'BC chi phí vận chuyển theo NV kinh doanh'
MODULE = 'BC chi phí VC theo NVKD'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
NHOM = Counter()


def J(*lines):
    return '\n'.join(lines)


def T(n, func, prio, pre, steps, data, exp):
    def j(x):
        return x if isinstance(x, str) else J(*x)
    return (n, func, prio, j(pre), j(steps), j(data), j(exp))


MENU = 'Vào phân hệ Bán hàng > menu Báo cáo > nhóm Vận chuyển > bấm "Chi phí vận chuyển theo nhân viên kinh doanh"'
MENU2 = 'Vào phân hệ Vận chuyển > menu Báo cáo vận chuyển > bấm "Báo cáo chi phí vận chuyển theo nhân viên kinh doanh"'
MO = 'Mở báo cáo (' + MENU + ')'
KY10 = 'Thời gian: 01/10/2026 đến 02/11/2026'
KYNAM = 'Thời gian: 01/01/2026 đến 02/11/2026'
Q_TCT = '"Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh theo tổng công ty"'
Q_CT = '"Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh theo công ty"'
Q_PB = '"Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh theo phòng ban"'
Q_VC_TCT = '"Xem báo cáo vận chuyển theo công ty theo tổng công ty"'
Q_VC_CT = '"Xem báo cáo vận chuyển theo công ty"'

DU_LIEU = J(
    'Tài khoản test:',
    '- TK-TCT: có quyền ' + Q_TCT + '.',
    '- TK-CT: nhân viên Công ty A, có quyền ' + Q_CT + '.',
    '- TK-PB: trưởng phòng P1 (quản lý phòng P1, P2), có quyền ' + Q_PB + '.',
    '- TK-NV: nhân viên kinh doanh NV-A (phòng P1, Công ty A), KHÔNG có quyền nào ở trên.',
    '- TK-VC: chỉ có quyền ' + Q_VC_TCT + ' (khối quyền Vận chuyển).',
    'Dữ liệu dev-hrm ngày 02/11/2026 (dùng làm số đối chiếu, môi trường khác thì ghi lại số thật):',
    '- Kỳ 01/10/2026 đến 02/11/2026: 4 phòng ban, Tổng cộng 6,156,920 (Kinh doanh CN Vinh 379,012; Phòng hành chính nhân sự '
    'chi nhánh Hải Phòng 436,800; Phòng KD Khu vực 4 1,627,313; Phòng kinh doanh chi nhánh Hải Phòng 3,713,795).',
    '- Kỳ 01/01/2026 đến 02/11/2026: 21 phòng ban, 100 dòng nhân viên, 610 chuyến, Tổng cộng 1,352,293,432.',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', J(
        'Báo cáo tổng hợp CƯỚC VẬN CHUYỂN đã hạch toán, tính cho từng nhân viên kinh doanh, theo 3 cấp Phòng ban > Nhân '
        'viên kinh doanh > Chuyến xe. Màn chỉ để xem và xuất Excel, không sửa dữ liệu.',
        'Có 2 đường vào cùng một màn:',
        '- ' + MENU + '.',
        '- ' + MENU2 + '.',
    )),
    ('2. Đối tượng được tính / hiển thị', J(
        'Một dòng hạch toán (bút toán) được cộng khi thỏa ĐỦ:',
        '- Thuộc phiếu hạch toán chuyến xe chở hàng hoặc phiếu hạch toán chuyến xe khác.',
        '- Có gắn nhân viên kinh doanh chịu cước.',
        '- Ngày hạch toán trong khoảng Thời gian (tính cả ngày đầu và ngày cuối).',
        '- Có mã công việc và mã đó không thuộc 5 mã bị loại (mục 3).',
        '- Nằm trong phạm vi quyền của người xem (mục 7) và khớp các ô lọc.',
    )),
    ('3. Đối tượng bị ẩn / không tính', J(
        '- Dòng hạch toán có mã công việc Công lái xe (CLX), Xăng xe (XXE), Chi phí khác (CPK), Vé cầu đường (VCD), Công tác phí (CTP).',
        '- Dòng hạch toán chưa gắn mã công việc.',
        '- Dòng hạch toán không gắn nhân viên.',
        '- Chuyến xe chưa hạch toán; phiếu chi / ủy nhiệm chi trả tiền vận chuyển cho nhà cung cấp (không làm đổi báo cáo).',
        '- Phòng ban / nhân viên không có cước trong kỳ: không có dòng.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', J(
        'Ô "Thời gian" (Từ ngày - Đến ngày) BẮT BUỘC, lọc theo NGÀY HẠCH TOÁN của phiếu hạch toán chuyến xe.',
        'Mở màn / tải lại trang / bấm Làm mới: ô trống, bảng ghi "Chọn thời gian để xem báo cáo."',
        'Không chọn được Từ ngày lớn hơn Đến ngày (lịch làm mờ ngày không hợp lệ, gõ tay thì ô không nhận).',
        'Bộ lọc được nhớ 10 phút khi rời màn rồi quay lại.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', J(
        'Dòng Tổng cộng (trên cùng) > Phòng ban (STT 1, đậm, nền xám) > Nhân viên kinh doanh (STT 1.1) > Chuyến xe (STT 1.1.1, '
        'chỉ khi tích "Xem chi tiết chuyến xe").',
        'Phòng ban và nhân viên lấy theo thông tin GHI TRÊN PHIẾU HẠCH TOÁN lúc hạch toán, không theo hồ sơ hiện tại.',
        '11 cột: STT, Mã NVKD, Thời gian, Tải trọng tính cước, Dòng xe tính cước, Xe chạy thực tế, Tuyến đường, Cước vận chuyển, '
        'Yêu cầu xuất hàng, Hợp đồng, Số chuyến xe. Mỗi tiêu đề có biểu tượng chú thích (rê chuột xem).',
        'Phân trang theo PHÒNG BAN: mặc định 10, chọn 10 / 20 / 50 / 100.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', J(
        '- Dòng chuyến xe = tổng các dòng hạch toán của 1 phiếu ghi cho 1 nhân viên (trong 1 phòng).',
        '- Dòng nhân viên = tổng các chuyến; dòng phòng ban = tổng các nhân viên; Tổng cộng = tổng mọi phòng ban của MỌI trang.',
        '- 1 phiếu chia cước cho 2 nhân viên: hiện ở cả 2 nhân viên, mỗi người phần của mình.',
        '- Nhân viên đổi phòng giữa kỳ: hiện ở 2 phòng, mỗi phòng phần hạch toán lúc ở phòng đó.',
        '- Cột Yêu cầu xuất hàng / Hợp đồng: mỗi mã 1 dòng, không lặp.',
    )),
    ('7. Phân quyền cấp', J(
        'Ai cũng mở được màn (menu không ẩn). Quyền chỉ quyết định phạm vi số liệu, ưu tiên rộng nhất:',
        '- Tổng công ty (' + Q_TCT + ' hoặc ' + Q_VC_TCT + '): mọi công ty; có ô Công ty, Phòng ban, Nhân viên KD.',
        '- Công ty (' + Q_CT + ' hoặc ' + Q_VC_CT + '): công ty đang làm việc; có ô Phòng ban, Nhân viên KD.',
        '- Phòng ban (' + Q_PB + '): các phòng mình quản lý + phòng của mình; có ô Nhân viên KD.',
        '- Không quyền: chỉ cước của chính mình; không có 3 ô trên.',
    )),
    ('8. Cách tính các ô thống kê', J(
        'Cước vận chuyển: số nguyên, dấu phẩy ngăn hàng nghìn (1,234,567), căn phải. Số 0 để trống, riêng dòng Tổng cộng in "0".',
        'Chân bảng "Hiển thị a–b / N": N = số phòng ban có cước.',
        'File Excel: cùng số với màn, mọi trang, cấp chuyến xe chỉ có khi đang tích Xem chi tiết chuyến xe.',
    )),
    ('9. Ghi chú đọc bảng', J(
        DU_LIEU,
        'Bẫy dễ sai:',
        '- Ô chữ (tìm nhanh, Số chuyến xe, Hợp đồng, Yêu cầu xuất hàng) chỉ lọc khi nhấn Enter hoặc bấm Tìm kiếm; ô chọn lọc ngay.',
        '- Lọc Yêu cầu xuất hàng / Hợp đồng / Đối tượng chịu phí giữ CẢ chuyến (cước nguyên chuyến) và loại chuyến không có yêu cầu xuất hàng.',
        '- Tổng cộng là tổng MỌI trang, không phải trang đang xem.',
        '- Phòng ban hiện theo phòng lúc hạch toán, có thể khác phòng hiện tại của nhân viên.',
    )),
]

ROLE_TCS = [
    T('00', 'Không có quyền - vẫn mở được màn, chỉ thấy cước của mình', 'P0',
      ['TK-NV không có quyền nào ở mục 7', 'NV-A có chuyến đã hạch toán trong kỳ'],
      ['1. Đăng nhập TK-NV', '2. ' + MENU, '3. Chọn Thời gian có cước của NV-A'],
      'TK-NV',
      ['- Menu có mục, mở được màn',
       '- Bộ lọc KHÔNG có ô Công ty, Phòng ban, Nhân viên KD',
       '- Bảng chỉ có 1 dòng nhân viên NV-A (dưới phòng ghi trên phiếu hạch toán); Tổng cộng = cước của NV-A']),
    T('01', 'Quyền theo tổng công ty - thấy mọi công ty', 'P0',
      'TK-TCT', ['1. Đăng nhập TK-TCT', '2. ' + MO, '3. ' + KY10],
      'TK-TCT; ' + KY10,
      ['- Có ô Công ty, Phòng ban, Nhân viên KD',
       '- Có phòng của nhiều công ty (dev: 4 phòng ban, Tổng cộng 6,156,920)']),
    T('02', 'Quyền theo công ty - chỉ công ty đang làm việc', 'P0',
      'TK-CT thuộc Công ty A',
      ['1. Đăng nhập TK-CT', '2. Mở báo cáo, chọn ' + KYNAM, '3. Đăng nhập TK-TCT, cùng kỳ, chọn ô Công ty = Công ty A'],
      'TK-CT, TK-TCT',
      ['- TK-CT: không có ô Công ty; có ô Phòng ban (chỉ phòng của Công ty A), Nhân viên KD',
       '- Tổng cộng của TK-CT = Tổng cộng của TK-TCT khi lọc Công ty A']),
    T('03', 'Quyền theo phòng ban - phòng mình quản lý và phòng của mình', 'P0',
      'TK-PB quản lý P1, P2',
      ['1. Đăng nhập TK-PB', '2. Mở báo cáo, chọn ' + KYNAM],
      'TK-PB',
      ['- Chỉ có ô Nhân viên KD (danh sách nhân viên của P1, P2)',
       '- Bảng chỉ có phòng P1, P2 (nếu có cước); không thấy phòng khác']),
    T('04', 'Quyền khối Vận chuyển cho phạm vi như quyền khối Bán hàng', 'P1',
      'TK-VC chỉ có quyền ' + Q_VC_TCT,
      ['1. Đăng nhập TK-VC', '2. ' + MENU2, '3. Chọn ' + KY10],
      'TK-VC',
      ['- Thấy phạm vi tổng công ty như TK-TCT (có ô Công ty)', '- Tổng cộng bằng TK-TCT cùng kỳ']),
    T('05', 'Có nhiều quyền - lấy phạm vi rộng nhất', 'P1',
      'Gán cho TK-PB thêm quyền ' + Q_CT,
      ['1. Đăng nhập TK-PB', '2. Mở báo cáo, chọn ' + KYNAM],
      'TK-PB (2 quyền)',
      ['- Phạm vi công ty: có ô Phòng ban, thấy mọi phòng của công ty đang làm việc']),
    T('06', 'Phạm vi theo phòng ghi trên phiếu hạch toán', 'P2',
      ['NV-B được chuyển từ P1 sang P3 trong tháng', 'NV-B có chuyến hạch toán lúc còn ở P1'],
      ['1. Đăng nhập TK-PB (quản lý P1, P2)', '2. Chọn kỳ chứa chuyến của NV-B'],
      'TK-PB, NV-B',
      ['- Chuyến lúc NV-B còn ở P1 vẫn hiện dưới phòng P1', '- Chuyến sau khi sang P3 không hiện']),
    T('07', 'Không quyền - ô lọc không vượt được phạm vi', 'P1',
      'TK-NV',
      ['1. Đăng nhập TK-NV, chọn ' + KYNAM, '2. Nhập mã một nhân viên khác vào ô tìm nhanh, nhấn Enter'],
      'Mã nhân viên khác NV-A',
      ['- Bảng "Không có dữ liệu phù hợp bộ lọc."', '- Không lộ cước của người khác']),
]

S1 = [
    T('001', 'Mở màn từ phân hệ Bán hàng', 'P0', 'TK-TCT', ['1. ' + MENU],
      '-', ['- Tiêu đề "Báo cáo chi phí vận chuyển theo nhân viên kinh doanh"',
            '- Ô Thời gian trống, có dấu * đỏ',
            '- Bảng có 11 tiêu đề cột, dòng "Chọn thời gian để xem báo cáo."',
            '- Có ô tích "Xem chi tiết chuyến xe" (chưa tích) và nút "Xuất Excel"']),
    T('002', 'Mở màn từ phân hệ Vận chuyển', 'P0', 'TK-TCT', ['1. ' + MENU2],
      '-', ['- Mở đúng màn như TC_01.001, cùng bộ lọc, cùng số liệu khi chọn cùng kỳ']),
    T('003', 'Bộ lọc khi mới mở', 'P1', 'TK-TCT', ['1. ' + MO, '2. Quan sát khu vực "Bộ lọc danh sách"'],
      '-', ['- Ô tìm nhanh placeholder "Tìm theo mã / tên nhân viên KD, phòng ban hoặc số chuyến xe"',
            '- Nút Tìm kiếm, Làm mới, Cài đặt bộ lọc, Ẩn tìm kiếm nâng cao',
            '- 8 ô: Thời gian, Công ty, Phòng ban, Nhân viên KD, Số chuyến xe, Hợp đồng, Yêu cầu xuất hàng, Đối tượng chịu phí']),
    T('004', 'Chú thích cạnh tiêu đề trang và tiêu đề cột', 'P2', 'TK-TCT', ['1. ' + MO, '2. Rê chuột vào biểu tượng chú thích cạnh tiêu đề trang', '3. Rê chuột vào biểu tượng chú thích cạnh tiêu đề cột Cước vận chuyển'],
      '-', ['- Bước 2: "Tổng hợp chi phí vận chuyển (cước chuyến xe) theo phòng ban và nhân viên kinh doanh trong kỳ, xem được chi tiết đến từng chuyến xe. ..."',
            '- Bước 3: "Chi phí vận chuyển tính cho nhân viên kinh doanh", 3 ý: dòng chuyến xe, mã công việc không tính, cách cộng dòng nhân viên / phòng ban / Tổng cộng']),
    T('005', 'Tiêu đề bảng dính và thanh cuộn ngang', 'P3', 'TK-TCT, đã chọn ' + KYNAM, ['1. Cuộn bảng xuống', '2. Cuộn ngang'],
      '-', ['- Hàng tiêu đề cột luôn hiện khi cuộn dọc', '- Có thanh cuộn ngang ở trên và dưới bảng; cuộn sang phải thấy cột Số chuyến xe']),
]

S2 = [
    T('001', 'Thời gian bắt buộc - bấm Tìm kiếm khi trống', 'P0', 'TK-TCT', ['1. ' + MO, '2. Bấm Tìm kiếm'],
      '-', ['- Ô Thời gian viền đỏ, chữ đỏ "Vui lòng chọn thời gian"', '- Bảng vẫn "Chọn thời gian để xem báo cáo."']),
    T('002', 'Chỉ chọn Từ ngày', 'P1', 'TK-TCT', ['1. Chọn Từ ngày 01/10/2026, để trống Đến ngày'],
      '-', ['- Không tải báo cáo, bảng "Chọn thời gian để xem báo cáo."']),
    T('003', 'Chọn đủ Thời gian - báo cáo tự tải', 'P0', 'TK-TCT', ['1. Chọn ' + KY10],
      KY10, ['- Báo cáo tải ngay không cần bấm Tìm kiếm', '- Chữ đỏ (nếu có) tự tắt', '- dev: 4 phòng ban, Tổng cộng 6,156,920']),
    T('004', 'Không chọn được khoảng ngày ngược chiều', 'P1', 'TK-TCT',
      ['1. Chọn Từ ngày 02/11/2026', '2. Mở lịch ô Đến ngày', '3. Gõ tay 01/10/2026 vào ô Đến ngày, nhấn Enter'],
      '-', ['- Bước 2: các ngày trước 02/11/2026 bị làm mờ, không bấm được',
            '- Bước 3: ô Đến ngày không nhận (để trống), bảng "Chọn thời gian để xem báo cáo."']),
    T('005', 'Biên ngày - tính cả ngày đầu và ngày cuối', 'P1', 'Có phiếu hạch toán chuyến xe ngày D (vd 08/10/2026, số TPV_HTCXCH_03182)',
      ['1. Chọn Từ ngày = Đến ngày = D', '2. Chọn Từ ngày = D + 1'],
      'D = 08/10/2026',
      ['- Bước 1: có chuyến của phiếu đó (dev: Nguyễn Đình Huỳnh 379,012)', '- Bước 2: chuyến đó không còn']),
    T('006', 'Tìm nhanh theo tên / mã nhân viên', 'P0', 'TK-TCT, ' + KYNAM,
      ['1. Nhập "Huỳnh" vào ô tìm nhanh', '2. Nhấn Enter', '3. Thay bằng mã nhân viên "41610788", bấm Tìm kiếm'],
      'Huỳnh / 41610788', ['- Trước khi nhấn Enter bảng chưa đổi', '- Bước 2, 3: chỉ còn nhân viên Nguyễn Đình Huỳnh (dev: 847,237)']),
    T('007', 'Tìm nhanh theo phòng ban', 'P1', 'TK-TCT, ' + KYNAM, ['1. Nhập "Vinh" vào ô tìm nhanh, nhấn Enter'],
      'Vinh', ['- Còn các phòng có tên / mã chứa "Vinh" và nhân viên có tên chứa "Vinh" (dev: Tổng cộng 51,383,086)']),
    T('008', 'Tìm nhanh theo số chuyến xe', 'P1', 'TK-TCT, ' + KYNAM, ['1. Nhập "TPHP_HTCXK_00411", nhấn Enter', '2. Tích Xem chi tiết chuyến xe'],
      'TPHP_HTCXK_00411', ['- Chỉ còn 1 chuyến của Vũ Bá Hoàng, Tổng cộng 463,795']),
    T('009', 'Lọc Công ty', 'P0', 'TK-TCT, ' + KYNAM, ['1. Chọn ô Công ty = Công ty A', '2. Mở ô Phòng ban, Nhân viên KD'],
      'Công ty A', ['- Báo cáo tải lại ngay, chỉ còn cước có công ty ghi trên phiếu hạch toán = Công ty A',
                    '- Ô Phòng ban, Nhân viên KD chỉ còn lựa chọn thuộc Công ty A']),
    T('010', 'Lọc Phòng ban', 'P0', 'TK-TCT, ' + KYNAM, ['1. Chọn Phòng ban "MT_KD - Kinh doanh CN Vinh"'],
      'Phòng MT_KD', ['- Chỉ còn phòng Kinh doanh CN Vinh (dev: 23,879,782, 4 nhân viên)', '- Ô Nhân viên KD chỉ còn nhân viên của phòng này']),
    T('011', 'Lọc Nhân viên KD', 'P0', 'TK-TCT, ' + KYNAM, ['1. Chọn Nhân viên KD "41610788 - Nguyễn Đình Huỳnh"'],
      '-', ['- Chỉ còn 1 dòng nhân viên, Tổng cộng = cước của người đó (dev: 847,237)']),
    T('012', 'Đổi Công ty / Phòng ban thì bỏ lựa chọn con không còn thuộc', 'P1', 'TK-TCT, ' + KYNAM,
      ['1. Chọn Phòng ban P1, Nhân viên KD thuộc P1', '2. Đổi Phòng ban sang P2', '3. Chọn Công ty khác công ty của P2'],
      '-', ['- Bước 2: ô Nhân viên KD tự xóa, bảng hiện cước của P2 (không ra rỗng)', '- Bước 3: ô Phòng ban tự xóa']),
    T('013', 'Lọc Số chuyến xe', 'P1', 'TK-TCT, ' + KYNAM, ['1. Nhập "HTCXK" vào ô Số chuyến xe, nhấn Enter'],
      'HTCXK', ['- Chỉ còn chuyến xe khác (số phiếu chứa HTCXK) (dev: 148 chuyến, 334,760,347)']),
    T('014', 'Lọc Yêu cầu xuất hàng', 'P1', 'TK-TCT, ' + KYNAM, ['1. Nhập "PYCXH-42950" vào ô Yêu cầu xuất hàng, nhấn Enter', '2. Tích Xem chi tiết chuyến xe'],
      'PYCXH-42950', ['- Chỉ còn chuyến TPV_HTCXCH_03182, 379,012', '- Cột Yêu cầu xuất hàng chỉ có PYCXH-42950']),
    T('015', 'Lọc Hợp đồng theo mã đang hiện trên cột Hợp đồng', 'P0', 'TK-TCT, ' + KYNAM + ', đã tích Xem chi tiết chuyến xe',
      ['1. Ghi lại mã hợp đồng ở cột Hợp đồng của chuyến TPHP_HTCXK_00411', '2. Nhập đúng mã đó vào ô Hợp đồng, nhấn Enter'],
      'HĐ_TPHP_HP_KD_26_0317_BTN', ['- Chuyến TPHP_HTCXK_00411 (463,795) có trong kết quả',
                                     '- Mọi chuyến trong kết quả đều có mã hợp đồng chứa chữ đã nhập ở cột Hợp đồng']),
    T('016', 'Lọc Hợp đồng gần đúng', 'P1', 'TK-TCT, ' + KYNAM, ['1. Nhập "HĐ_TPV_MT_KD" vào ô Hợp đồng, nhấn Enter'],
      'HĐ_TPV_MT_KD', ['- Chỉ còn chuyến có hợp đồng chứa "HĐ_TPV_MT_KD"', '- Cột Hợp đồng chỉ còn hợp đồng khớp']),
    T('017', 'Lọc Đối tượng chịu phí', 'P1', 'TK-TCT, ' + KYNAM,
      ['1. Chọn "Nhân viên chịu", ghi Tổng cộng = A', '2. Chọn "Công ty chịu", ghi Tổng cộng = B', '3. Bỏ chọn, ghi Tổng cộng = T'],
      '-', ['- Mỗi lựa chọn chỉ còn chuyến có yêu cầu xuất hàng đánh dấu đúng đối tượng; cước là cước nguyên chuyến',
            '- A + B có thể nhỏ hơn T: chuyến không có yêu cầu xuất hàng không thuộc nhóm nào (dev: A 1,032,047,327; B 1,794,182; T 1,352,293,432)']),
    T('018', 'Kết hợp nhiều ô lọc', 'P1', 'TK-TCT, ' + KYNAM,
      ['1. Chọn Phòng ban "Kinh doanh CN Vinh"', '2. Nhập Số chuyến xe "TPV_HTCXCH_02", nhấn Enter', '3. Chọn Đối tượng chịu phí "Nhân viên chịu"'],
      '-', ['- Kết quả thỏa đồng thời 3 điều kiện', '- Tổng cộng = tổng các dòng phòng ban còn lại']),
    T('019', 'Bộ lọc không có kết quả', 'P2', 'TK-TCT, ' + KYNAM, ['1. Nhập "KHONGTONTAI" vào ô tìm nhanh, nhấn Enter'],
      'KHONGTONTAI', ['- Bảng "Không có dữ liệu phù hợp bộ lọc."', '- Không có dòng Tổng cộng, không có chân phân trang']),
    T('020', 'Làm mới', 'P0', 'Đang lọc nhiều ô', ['1. Bấm Làm mới'],
      '-', ['- Mọi ô kể cả Thời gian về trống', '- Bảng "Chọn thời gian để xem báo cáo."', '- Không còn chữ đỏ']),
    T('021', 'Nhớ bộ lọc khi rời màn và quay lại', 'P2', 'Đang lọc ' + KY10 + ' và Phòng ban P1',
      ['1. Chuyển sang màn khác', '2. Trong 10 phút quay lại báo cáo', '3. Tải lại trang (F5)'],
      '-', ['- Bước 2: giữ nguyên Thời gian và Phòng ban, bảng có số', '- Bước 3: mọi ô về trống']),
    T('022', 'Ẩn / hiện tìm kiếm nâng cao', 'P3', 'TK-TCT', ['1. Bấm "Ẩn tìm kiếm nâng cao"', '2. Bấm lại'],
      '-', ['- Bước 1: ẩn 8 ô lọc, vẫn còn ô tìm nhanh và nút Tìm kiếm / Làm mới', '- Bước 2: hiện lại']),
]

S3 = [
    T('001', 'Dòng Tổng cộng = tổng các dòng phòng ban', 'P0', 'TK-TCT', ['1. Chọn ' + KY10, '2. Cộng tay Cước vận chuyển 4 dòng phòng ban'],
      KY10, ['- 379,012 + 436,800 + 1,627,313 + 3,713,795 = 6,156,920 = dòng Tổng cộng']),
    T('002', 'Dòng phòng ban = tổng các nhân viên', 'P0', 'TK-TCT, ' + KYNAM, ['1. Cộng tay 4 dòng nhân viên của phòng Kinh doanh CN Vinh'],
      '-', ['- 1,245,648 + 847,237 + 11,147,097 + 10,639,800 = 23,879,782 = dòng phòng']),
    T('003', 'Dòng nhân viên = tổng các chuyến', 'P0', 'TK-TCT, ' + KY10 + ', tích Xem chi tiết chuyến xe',
      ['1. Cộng tay các chuyến của Vũ Bá Hoàng'], '-', ['- 463,795 + 2,500,000 + 750,000 = 3,713,795 = dòng nhân viên = dòng phòng Phòng kinh doanh chi nhánh Hải Phòng']),
    T('004', 'Tổng cộng tính mọi trang', 'P0', 'TK-TCT, ' + KYNAM + ', 10 dòng/trang (3 trang)',
      ['1. Ghi Tổng cộng ở trang 1', '2. Sang trang 2, 3', '3. Cộng tay mọi dòng phòng ban của 3 trang'],
      '-', ['- Tổng cộng giống nhau ở cả 3 trang (dev: 1,352,293,432)', '- Bằng tổng 21 dòng phòng ban']),
    T('005', 'Định dạng số', 'P1', 'TK-TCT, ' + KYNAM, ['1. Quan sát cột Cước vận chuyển'],
      '-', ['- Dạng 1,352,293,432: dấu phẩy ngăn hàng nghìn, không có phần lẻ, căn phải']),
    T('006', 'Số lẻ được làm tròn đến đồng', 'P2', 'Có phiếu hạch toán ngoại tệ / số tiền quy đổi có phần lẻ (vd 100,000.6)',
      ['1. Chọn kỳ chứa phiếu đó', '2. Tích Xem chi tiết chuyến xe'],
      '-', ['- Dòng chuyến hiện 100,001', '- Tổng cộng làm tròn từ tổng thật (có thể lệch 1 đồng so với cộng các dòng đã làm tròn)']),
    T('007', 'Tổng cộng bằng 0 in "0"', 'P3', 'Người dùng không quyền không có cước nào; hoặc lọc chỉ ra phòng cước 0',
      ['1. Đăng nhập TK-NV chưa có cước, chọn kỳ'], '-', ['- Không có dòng Tổng cộng khi bảng rỗng ("Không có dữ liệu phù hợp bộ lọc.")', '- Khi có dòng mà tổng bằng 0 thì Tổng cộng in "0", các dòng khác để trống']),
    T('008', 'Bỏ 5 mã công việc và dòng không có mã công việc', 'P0', 'Phiếu hạch toán X (đã có sẵn) có 3 dòng cho NV-A: Cước vận chuyển 1,000,000; Xăng xe (XXE) 200,000; 1 dòng không gắn mã công việc 50,000',
      ['1. Chọn kỳ chứa ngày hạch toán của X', '2. Tích Xem chi tiết chuyến xe, tìm chuyến X'],
      'Phiếu X', ['- Dòng chuyến X = 1,000,000 (không cộng 200,000 và 50,000)']),
    T('009', 'Cột Thời gian / Tải trọng / Dòng xe / Xe chạy thực tế / Tuyến đường', 'P1', 'TK-TCT, ' + KY10 + ', tích Xem chi tiết chuyến xe',
      ['1. Đọc dòng 1.1.1'], '-', ['- Thời gian 08/10/2026; Tải trọng tính cước 1.21 tấn; Dòng xe tính cước Xe tải thùng kín',
                                   '- Xe chạy thực tế "37C-31738 - 1.21 tấn - Xe tải thùng kín"',
                                   '- Tuyến đường "72M, Nghi Phú, TP Vinh, Nghệ An - Đức Thọ, Đức Thọ, Hà Tĩnh"',
                                   '- Các cột này để trống ở dòng phòng ban, nhân viên']),
    T('010', 'Tuyến đường của chuyến xe khác không chọn tuyến', 'P2', 'Có chuyến xe khác đã hạch toán, không chọn tuyến, có Điểm đi / Điểm đến',
      ['1. Tìm chuyến đó trong báo cáo (tích Xem chi tiết)'], '-', ['- Cột Tuyến đường hiện "Điểm đi - Điểm đến" của chuyến', '- Không để trống']),
    T('011', 'Cột Yêu cầu xuất hàng và Hợp đồng nhiều mã', 'P1', 'TK-TCT, ' + KY10 + ', tích Xem chi tiết',
      ['1. Đọc dòng chuyến TPHP_HTCXCH_03170'], '-', ['- Cột Yêu cầu xuất hàng 2 dòng: PYCXH-42192, PYCXH-42193', '- Cột Hợp đồng không lặp mã']),
    T('012', 'Phòng ban / nhân viên theo phiếu hạch toán, không theo hồ sơ hiện tại', 'P1', 'NV-B chuyển từ P1 sang P3 giữa kỳ, có chuyến ở cả 2 giai đoạn',
      ['1. Chọn kỳ bao cả 2 giai đoạn'], '-', ['- NV-B hiện ở cả phòng P1 và P3, mỗi phòng phần cước tương ứng', '- Tổng của NV-B ở 2 phòng = tổng cước NV-B']),
    T('013', 'Một chuyến chia cho nhiều nhân viên', 'P1', 'Phiếu hạch toán Y (có sẵn) chia cước 650,000 cho NV-A và 350,000 cho NV-C',
      ['1. Chọn kỳ chứa Y, tích Xem chi tiết'], '-', ['- Chuyến Y hiện dưới NV-A 650,000 và dưới NV-C 350,000', '- Tổng cộng chỉ tăng 1,000,000']),
    T('014', 'Thứ tự sắp xếp', 'P2', 'TK-TCT, ' + KYNAM + ', tích Xem chi tiết',
      ['1. Quan sát thứ tự phòng ban, nhân viên, chuyến'], '-', ['- Phòng ban theo tên A đến Z', '- Nhân viên trong phòng theo họ tên A đến Z', '- Chuyến xe theo Thời gian mới đến cũ']),
    T('015', 'Số 0 để trống', 'P3', 'Nhân viên có cước âm và dương bù trừ về 0 trong kỳ (nếu có)', ['1. Chọn kỳ đó'],
      '-', ['- Ô Cước vận chuyển của dòng đó để trống, không ghi 0']),
]

S4 = [
    T('001', 'Phân trang theo phòng ban', 'P1', 'TK-TCT, ' + KYNAM, ['1. Xem chân bảng', '2. Bấm trang 2'],
      '-', ['- "Hiển thị 1–10 / 21", "Số dòng/trang" = 10', '- Trang 2: STT phòng ban bắt đầu từ 11; nhân viên của phòng không bị cắt sang trang khác']),
    T('002', 'Đổi số dòng / trang', 'P2', 'Đang ở trang 2', ['1. Chọn Số dòng/trang = 50'],
      '-', ['- Về trang 1, hiện cả 21 phòng ban, "Hiển thị 1–21 / 21"', '- Lựa chọn có: 10, 20, 50, 100']),
    T('003', 'Đổi bộ lọc khi đang ở trang sau', 'P2', 'Đang ở trang 3', ['1. Chọn Phòng ban bất kỳ'],
      '-', ['- Tải lại về trang 1']),
]

S5 = [
    T('001', 'Tích Xem chi tiết chuyến xe', 'P0', 'TK-TCT, ' + KY10, ['1. Tích "Xem chi tiết chuyến xe"'],
      '-', ['- Dưới mỗi nhân viên có các dòng chuyến STT 1.1.1, ...', '- Số ở dòng phòng ban, nhân viên, Tổng cộng không đổi', '- dev: 6 chuyến']),
    T('002', 'Bỏ tích', 'P1', 'Đang tích', ['1. Bỏ tích'], '-', ['- Ẩn dòng chuyến, giữ trang và bộ lọc']),
    T('003', 'Mở yêu cầu xuất hàng', 'P1', 'Đang tích, ' + KY10, ['1. Bấm "PYCXH-42950" ở dòng 1.1.1'],
      '-', ['- Mở tab mới màn YC xuất hàng PYCXH-42950', '- Tab báo cáo giữ nguyên']),
    T('004', 'Mở hợp đồng', 'P1', 'Đang tích', ['1. Bấm mã hợp đồng hãng ở dòng chuyến', '2. Bấm mã hợp đồng sửa chữa - bảo dưỡng (nếu có)'],
      '-', ['- Bước 1: mở hợp đồng ở tab mới', '- Bước 2: mở màn hợp đồng sửa chữa - bảo dưỡng ở tab mới']),
    T('005', 'Mở phiếu hạch toán chuyến xe', 'P1', 'Đang tích', ['1. Bấm "TPV_HTCXCH_03182"', '2. Bấm một số chuyến xe khác (…_HTCXK_…)'],
      '-', ['- Mở đúng phiếu hạch toán chuyến xe chở hàng / chuyến xe khác ở tab mới', '- Số tiền trên phiếu cho nhân viên đó = cước của dòng chuyến (trừ các dòng mã công việc bị loại)']),
    T('006', 'Xem chi tiết với kỳ dài', 'P2', 'TK-TCT', ['1. Chọn ' + KYNAM, '2. Tích Xem chi tiết'],
      '-', ['- Tải trong vài giây, không treo màn (dev: 610 chuyến cả năm)']),
]

S6 = [
    T('001', 'Xuất Excel khi chưa chọn Thời gian', 'P1', 'TK-TCT, Thời gian trống', ['1. Bấm Xuất Excel'],
      '-', ['- Thông báo "Vui lòng chọn thời gian", ô Thời gian báo đỏ', '- Không mở cửa sổ chọn trường']),
    T('002', 'Cửa sổ Chọn trường xuất Excel', 'P1', 'Đã chọn ' + KY10, ['1. Bấm Xuất Excel'],
      '-', ['- Tiêu đề "Chọn trường xuất Excel"', '- 10 trường đều đã tích: Mã NVKD, Thời gian, Tải trọng tính cước, Dòng xe tính cước, Xe chạy thực tế, Tuyến đường, Cước vận chuyển, Yêu cầu xuất hàng, Hợp đồng, Số chuyến xe',
            '- "Đang chọn 10/10 trường", nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng']),
    T('003', 'Bỏ chọn hết', 'P2', 'Cửa sổ đang mở', ['1. Bấm Bỏ chọn hết'], '-', ['- "Đang chọn 0/10 trường", nút Xuất file không bấm được']),
    T('004', 'Xuất có cấp chuyến xe', 'P0', 'Đã chọn ' + KY10 + ', đã tích Xem chi tiết', ['1. Bấm Xuất Excel > Xuất file', '2. Mở file'],
      '-', ['- Thông báo "Xuất Excel thành công", file bao_cao_chi_phi_van_chuyen_theo_nhan_vien_kinh_doanh.xlsx',
            '- Dòng 1 "BÁO CÁO CHI PHÍ VẬN CHUYỂN THEO NHÂN VIÊN KINH DOANH", dòng 2 "Từ ngày: 01/10/2026 đến ngày: 02/11/2026"',
            '- Dòng Tổng cộng 6,156,920 ngay dưới tên cột; 4 phòng (STT 1..4, đậm), nhân viên (1.1, đậm xanh), chuyến (1.1.1)',
            '- Có đủ 6 chuyến như màn; cuối file khối "Người lập (Ký, họ tên)"']),
    T('005', 'Xuất không có cấp chuyến xe', 'P1', 'Đã chọn ' + KY10 + ', KHÔNG tích Xem chi tiết', ['1. Xuất file, mở file'],
      '-', ['- Chỉ có Tổng cộng, phòng ban, nhân viên; không có dòng 1.1.1', '- Số khớp màn']),
    T('006', 'Xuất mọi trang', 'P0', 'Đã chọn ' + KYNAM + ' (3 trang), đang ở trang 1', ['1. Xuất file', '2. Đếm số dòng phòng ban trong file'],
      '-', ['- File có đủ 21 phòng ban (không chỉ 10 phòng của trang 1)', '- Tổng cộng 1,352,293,432']),
    T('007', 'Xuất theo bộ lọc đang áp', 'P1', 'Đã lọc Phòng ban "Kinh doanh CN Vinh"', ['1. Xuất file'],
      '-', ['- File chỉ có phòng Kinh doanh CN Vinh, Tổng cộng = số trên màn']),
    T('008', 'Chọn và đổi thứ tự cột', 'P2', 'Cửa sổ đang mở', ['1. Chỉ tích Số chuyến xe, Cước vận chuyển', '2. Kéo Số chuyến xe lên đầu', '3. Xuất file'],
      '-', ['- File có cột STT, Số chuyến xe, Cước vận chuyển theo đúng thứ tự', '- Tên phòng / nhân viên vẫn hiện ở dòng cấp tương ứng']),
    T('009', 'Định dạng file', 'P2', 'File của TC_06.004', ['1. Mở file, xem ô số và khung'],
      '-', ['- Cột Cước vận chuyển là số (cộng được), dạng 1,234,567; số 0 để trống', '- Mọi ô có khung; tên phòng / nhân viên gộp ô; chữ dài xuống dòng']),
    T('010', 'Xuất khi không có số liệu', 'P3', 'Lọc ra "Không có dữ liệu phù hợp bộ lọc."', ['1. Xuất file'],
      '-', ['- Vẫn tải file: tiêu đề, dòng kỳ, tên cột, dòng Tổng cộng trống']),
    T('011', 'Ô chữ đã gõ nhưng chưa nhấn Enter', 'P3', 'Đã chọn ' + KYNAM + '; gõ "HTCXK" vào ô Số chuyến xe nhưng KHÔNG nhấn Enter',
      ['1. Bấm Xuất Excel > Xuất file', '2. So file với màn'],
      '-', ['- Số trong file khớp đúng bảng đang hiện trên màn']),
]

S7 = [
    T('001', 'Ghi số nền', 'P0', ['NV-A thuộc phòng P1', 'Kỳ: ngày 1 tháng hiện tại đến hôm nay'],
      ['1. Đăng nhập TK-TCT, mở báo cáo, chọn kỳ', '2. Tích Xem chi tiết, ghi lại cước NV-A (= N), phòng P1 (= P), Tổng cộng (= T)'],
      'NV-A, P1', ['- Có số nền N, P, T cho các TC sau']),
    T('002', 'Lập chuyến xe khác chưa hạch toán - báo cáo không đổi', 'P0', 'Đã có số nền',
      ['1. Vào phân hệ Vận chuyển > Chuyến xe > Chuyến xe khác, Tạo mới chuyến gắn yêu cầu xuất hàng của NV-A, lưu, duyệt, kết thúc chuyến',
       '2. Mở lại báo cáo cùng kỳ'],
      'Chuyến xe khác CXK-TEST', ['- Báo cáo không đổi (N, P, T giữ nguyên) vì chưa có phiếu hạch toán']),
    T('003', 'Hạch toán chuyến - báo cáo tăng', 'P0', ['Phiếu hạch toán của CXK-TEST có sẵn (kế toán lập qua nút "Hạch toán chuyến xe" ở màn Chuyến xe khác chờ hạch toán), ngày hạch toán hôm nay',
                                                     'Phiếu có 1 dòng Cước vận chuyển 1,000,000 ghi cho NV-A'],
      ['1. Mở lại báo cáo cùng kỳ, tích Xem chi tiết'],
      '1,000,000', ['- NV-A = N + 1,000,000; P1 = P + 1,000,000; Tổng cộng = T + 1,000,000',
                    '- Có dòng chuyến mới: Thời gian hôm nay, Số chuyến xe = số phiếu hạch toán, cột Yêu cầu xuất hàng có yêu cầu đã gắn']),
    T('004', 'Dòng mã công việc bị loại không làm tăng', 'P0', 'Phiếu hạch toán CXK-TEST có thêm dòng Xăng xe (XXE) 200,000 và Vé cầu đường (VCD) 50,000 cho NV-A (có sẵn)',
      ['1. Mở lại báo cáo'], '-', ['- Cước NV-A vẫn N + 1,000,000']),
    T('005', 'Ngày hạch toán ngoài kỳ', 'P1', 'Có sẵn phiếu hạch toán chuyến xe chở hàng của NV-A ngày hạch toán tháng trước, 500,000',
      ['1. Chọn kỳ tháng hiện tại', '2. Chọn kỳ tháng trước'], '-', ['- Bước 1: không có 500,000', '- Bước 2: có chuyến 500,000']),
    T('006', 'Hạch toán chuyến xe chở hàng', 'P0', ['Chuyến xe chở hàng (Vận chuyển > Chuyến xe > Chuyến xe chở hàng) đã kết thúc, có yêu cầu xuất hàng của NV-A',
                                                    'Phiếu hạch toán của chuyến có sẵn, 1 dòng cước 300,000 cho NV-A, ngày hôm nay'],
      ['1. Mở lại báo cáo cùng kỳ'], '-', ['- NV-A tăng thêm 300,000; dòng chuyến có Số chuyến xe dạng …_HTCXCH_…']),
    T('007', 'Đổi nhân viên chịu cước trên phiếu hạch toán', 'P1', 'Phiếu hạch toán CXK-TEST được kế toán sửa: dòng 1,000,000 chuyển sang NV-C (phòng P2)',
      ['1. Mở lại báo cáo'], '-', ['- NV-A giảm 1,000,000, NV-C tăng 1,000,000 (dưới phòng P2)', '- Tổng cộng không đổi']),
    T('008', 'Xóa phiếu hạch toán - báo cáo giảm về số nền', 'P1', 'Phiếu hạch toán CXK-TEST và phiếu của TC_07.006 bị xóa / hủy hạch toán',
      ['1. Mở lại báo cáo'], '-', ['- N, P, T về đúng số nền']),
    T('009', 'Phiếu chi trả tiền vận chuyển không làm đổi báo cáo', 'P2', 'Có sẵn phiếu chi thanh toán tiền chuyến xe cho nhà cung cấp vận chuyển trong kỳ',
      ['1. Mở báo cáo cùng kỳ'], '-', ['- Số liệu không đổi so với trước khi lập phiếu chi']),
]

S8 = [
    T('001', 'Thời gian tải khi không lọc gì ngoài Thời gian', 'P2', 'TK-TCT', ['1. Chọn ' + KYNAM + ' (không lọc ô khác), đo thời gian đến khi có bảng'],
      '-', ['- Có bảng trong không quá 3 giây (dev 02/11/2026: khoảng 0,9 giây)']),
    T('002', 'Thời gian tải khi bật Xem chi tiết cả năm', 'P2', 'TK-TCT, ' + KYNAM, ['1. Tích Xem chi tiết chuyến xe, đo thời gian'],
      '-', ['- Có dòng chuyến trong không quá 5 giây (dev: khoảng 1,5 giây)']),
    T('003', 'Đổi bộ lọc liên tục', 'P3', 'TK-TCT, ' + KYNAM, ['1. Đổi Phòng ban 3 lần thật nhanh'],
      '-', ['- Bảng cuối cùng đúng phòng chọn sau cùng, không bị kết quả cũ đè lên']),
    T('004', 'Thời gian xuất Excel cả năm', 'P3', 'TK-TCT, ' + KYNAM + ', tích Xem chi tiết', ['1. Xuất file'],
      '-', ['- File tải về trong không quá 5 giây (dev: khoảng 1 giây cho 610 chuyến)']),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'SỐ LIỆU', S3),
    ('IV', 'PHÂN TRANG', S4),
    ('V', 'XEM CHI TIẾT CHUYẾN XE & LIÊN KẾT', S5),
    ('VI', 'XUẤT EXCEL', S6),
    ('VII', 'LUỒNG PHÁT SINH (lập chứng từ rồi kiểm số)', S7),
    ('VIII', 'HIỆU NĂNG', S8),
]

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name=TEN + ' - Cập nhật ngày ' + L.NGAY, module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
    print('Số TC: phân quyền %d; ' % len(ROLE_TCS) + '; '.join('%s %d' % (t, len(s)) for _, t, s in SECTIONS)
          + ' -> tổng %d' % (len(ROLE_TCS) + sum(len(s) for _, _, s in SECTIONS)))

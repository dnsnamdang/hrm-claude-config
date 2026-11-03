# -*- coding: utf-8 -*-
"""Testcase "BC tổng hợp công nợ KH theo nhân viên" (HRM: Bán hàng > Báo cáo > Báo cáo công nợ > Tổng hợp công nợ theo NV).

Viết mới theo code HRM hiện tại (02/11/2026), form 17 cột (engine tc_engine). Tham khảo ý tưởng (KHÔNG chép):
TC ERP `erp/.plans/erp-bao-cao-cong-no-khach-hang/tc_theo_nhan_vien.py` + `common.py:data_change_tcs`, kịch bản nghiệm thu
`sale-customer-debt-reports/kich-ban-nghiem-thu/`. Chỉ dùng chứng từ HRM lập được; chứng từ chưa có màn HRM (hợp đồng bán
hàng, phiếu xuất kho, biên bản nghiệm thu) ghi ở Tiền điều kiện là "có sẵn".
Số đo trên dev 02/11/2026: tải 1 tháng không lọc 4,7 giây (25,302 dòng hợp đồng); 10 tháng 4,1 giây.
Chạy: python gen_testcase.py
"""
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _lib_bc as B  # noqa: E402,F401  (đặt sys.path tới tc_engine)
from tc_engine import build  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

L = B.L
TEN = 'BC tổng hợp công nợ KH theo nhân viên'
MODULE = 'BC công nợ KH theo NV'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)
NHOM = Counter()


def L_(*lines):
    return '\n'.join(lines)


def T(n, func, prio, pre, steps, data, exp):
    def j(x):
        return x if isinstance(x, str) else L_(*x)
    return (n, func, prio, j(pre), j(steps), j(data), j(exp))


MENU = 'Vào phân hệ Bán hàng > Báo cáo > nhóm Báo cáo công nợ > bấm "Tổng hợp công nợ theo NV"'
Q = 'Xem báo cáo tổng hợp công nợ khách hàng theo nhân viên - '
LOC = 'Thời gian = ngày 1 tháng này đến hôm nay, Khách hàng = KH-TEST'
NOI = 'dòng hợp đồng HD-TEST-01, dòng nhân viên A (in đậm, phía trên) và dòng Tổng cộng'
PT = 'Tài chính > Quản lý tiền > "Phiếu thu"'
PBC = 'Tài chính > Quản lý tiền > "Phiếu báo có"'
PC = 'Tài chính > Quản lý tiền > "Phiếu chi"'
UNC = 'Tài chính > Quản lý tiền > "Phiếu ủy nhiệm chi"'
YCDC = 'Tài chính > Khởi tạo > "Phiếu yêu cầu điều chỉnh công nợ"'
PKT = 'Tài chính > Sổ tổng hợp > "Phiếu kế toán"'
YCXH = 'Tài chính > Xuất hàng > "Yêu cầu xuất hàng"'
PXH = 'Tài chính > Xuất hàng > "Phiếu xuất hàng"'
YCNH = 'Tài chính > Nhập hàng > "Yêu cầu nhập hàng"'
PNH = 'Tài chính > Nhập hàng > "Phiếu nhập hàng"'
HTDV = 'Tài chính > Bán Dịch vụ > "Phiếu hạch toán dịch vụ - HDDV"'
XBM = 'Tài chính > Mượn hàng > "Phiếu xuất bán hàng mượn"'

DU_LIEU = L_(
    'Dữ liệu mẫu (lập trước khi test, ghi mã thật vào cột Ghi chú nếu khác):',
    '- KH-TEST: khách hàng mới, chưa có phát sinh. HD-TEST-01, HD-TEST-02: hợp đồng bán hàng của KH-TEST do nhân viên A lập, đã ký, hàng KHÔNG cần lắp đặt (có sẵn).',
    '- Nhân viên A thuộc công ty CT1, phòng P1, bộ phận BP1; nhân viên B thuộc phòng P2, bộ phận BP2; nhân viên C thuộc công ty CT2.',
    '- TK-A: tài khoản nhân viên A, không có quyền xem nào. TK-BP: có quyền "' + Q + 'bộ phận", đang thuộc BP1, quản lý BP2.',
    '- TK-PB: có quyền "' + Q + 'phòng ban", đang thuộc P1, quản lý P2. TK-CT: có quyền "' + Q + 'công ty" (đang làm việc ở CT1). TK-TCT: có quyền "' + Q + 'tổng công ty".',
    '- Trước mỗi bước ở nhóm "Luồng phát sinh" ghi lại "số nền" (số đang có) của ' + NOI + '; kết quả đúng là phần CHÊNH so với số nền.',
    '- Chứng từ phải được HẠCH TOÁN (ghi sổ) mới lên báo cáo. Ai không lập / duyệt được phiếu thì nhờ kế toán, chỉ cần đúng khách hàng, hợp đồng, số tiền, ngày hạch toán.',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Báo cáo công nợ phải thu GOM THEO NHÂN VIÊN TẠO HỢP ĐỒNG: mỗi nhân viên có những hợp đồng nào còn nợ, nợ bao nhiêu, nghiệm thu ngày nào, đã nợ bao nhiêu ngày. Dùng để giao nhân viên thu hồi công nợ. Màn chỉ xem, có Xuất Excel (chọn trường) và Xuất Excel mẫu in.',
        'Đường vào: ' + MENU + '.',
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Nguồn: bút toán tài khoản phải thu khách hàng 131 (và tài khoản con) sinh ra khi chứng từ được hạch toán. Cột và chứng từ làm nó đổi:',
        '- Số dư đầu kỳ: mọi phát sinh có ngày hạch toán trước Từ ngày (Nợ trừ Có).',
        '- Hàng hóa/Dịch vụ: phiếu xuất kho, phiếu xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ bảo hành - sửa chữa, khai báo công nợ đầu kỳ.',
        '- Điều chỉnh công nợ (nhóm tăng / nhóm giảm): phiếu kế toán điều chỉnh công nợ ghi tăng / ghi giảm.',
        '- Nhập trả lại: phiếu nhập hàng khách trả lại. Đã thanh toán: phiếu thu, phiếu báo có, khai báo công nợ đầu kỳ (phần đã thu).',
        '- Trả lại tiền thừa: phiếu chi, phiếu ủy nhiệm chi; làm số dư TĂNG.',
        '- Số dư cuối kỳ = Đầu kỳ + Cộng tăng - Cộng giảm + Trả lại tiền thừa. Dương = Dư nợ, âm = Dư có.',
        '- Ngày nghiệm thu, Số ngày nợ (= hôm nay - (Ngày nghiệm thu + 6 ngày), âm thì 0, chỉ hiện khi còn dư nợ).',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '- Bút toán chưa gắn khách hàng, chưa có nhân viên tạo hợp đồng hoặc số tiền bằng 0: không thành dòng hợp đồng (nhưng VẪN tính vào Số dư đầu kỳ của dòng Tổng cộng).',
        '- Chứng từ chưa hạch toán, chứng từ có ngày hạch toán sau Đến ngày.',
        '- Hợp đồng ngoài phạm vi quyền xem (mục 7).',
        '- Số ngày nợ để trống khi hợp đồng không còn dư nợ hoặc không xác định được Ngày nghiệm thu.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô "Thời gian" (Từ ngày - Đến ngày) BẮT BUỘC, lọc theo NGÀY HẠCH TOÁN: trước Từ ngày vào Số dư đầu kỳ, từ Từ ngày đến hết Đến ngày vào phát sinh.',
        'Mở màn chưa có Thời gian: bảng ghi "Chọn thời gian để xem báo cáo.". Chọn đủ 2 ngày thì bảng tự tải.',
        'Lịch không cho chọn Từ ngày sau Đến ngày (ngày bị làm mờ, gõ tay không nhận).',
        'Ô "Ngày nghiệm thu" (không bắt buộc) lọc hợp đồng có Ngày nghiệm thu ĐÚNG BẰNG ngày chọn.',
        'Số ngày nợ luôn tính tới HÔM NAY, không theo Đến ngày.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Bảng 16 cột, tiêu đề 2 tầng: STT, Đơn hàng/hợp đồng, Khách hàng, Số dư đầu kỳ, [Phát sinh tăng trong kỳ: Hàng hóa/Dịch vụ, Điều chỉnh công nợ, Cộng], [Phát sinh giảm trong kỳ: Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ, Cộng], Trả lại tiền thừa, Số dư cuối kỳ, Ngày nghiệm thu, Số ngày nợ (Ngày). Mọi đầu cột có icon (i) chú thích.',
        'Thứ tự dòng: Tổng cộng > dòng nhân viên in đậm "Mã - Họ tên" (STT 1, 2…) > dòng hợp đồng (STT 1.1, 1.2…, số hợp đồng bấm được mở tab mới, Khách hàng "Mã - Tên").',
        'Phân trang theo DÒNG HỢP ĐỒNG: mặc định 10, chọn 10/20/50/100; chân bảng "Hiển thị a–b / N dòng hợp đồng". Không có sắp xếp cột, không có tùy chỉnh cột, không có cửa sổ chi tiết chứng từ.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '- Gom theo (nhân viên tạo hợp đồng, hợp đồng): mỗi hợp đồng 1 dòng; hợp đồng có số liệu toàn 0 vẫn hiện khi Số dư cuối kỳ = Tất cả.',
        '- Hợp đồng có bút toán của nhiều khách: cột Khách hàng chỉ hiện 1 khách (ghi nhận).',
        '- Dòng nhân viên = cộng ĐỦ mọi hợp đồng của nhân viên theo bộ lọc, KỂ CẢ hợp đồng ở trang sau.',
        '- Dòng Tổng cộng: cột phát sinh = cộng mọi dòng (mọi trang); Số dư đầu kỳ = mọi bút toán trước Từ ngày trong phạm vi quyền (không theo ô Số dư cuối kỳ, Ngày nghiệm thu, ô tìm nhanh); Số dư cuối kỳ = Đầu kỳ (Tổng cộng) + Cộng tăng - Cộng giảm + Trả lại tiền thừa.',
    )),
    ('7. Phân quyền cấp', L_(
        'Mọi tài khoản mở được màn. 4 quyền chỉ mở rộng PHẠM VI (có nhiều quyền thì lấy cấp rộng nhất):',
        '- "' + Q + 'tổng công ty": mọi công ty; có ô Công ty, Phòng ban, Bộ phận, Nhân viên.',
        '- "' + Q + 'công ty": công ty đang làm việc + hợp đồng mình tạo; có ô Phòng ban, Bộ phận, Nhân viên.',
        '- "' + Q + 'phòng ban": phòng mình quản lý + phòng mình đang thuộc + hợp đồng mình tạo; có ô Phòng ban, Bộ phận, Nhân viên.',
        '- "' + Q + 'bộ phận": bộ phận mình quản lý + bộ phận đang thuộc + hợp đồng mình tạo; có ô Bộ phận, Nhân viên.',
        '- Không quyền: chỉ hợp đồng mình tạo; không có 4 ô lọc tổ chức.',
        'Phạm vi áp cho mọi dòng, dòng Tổng cộng (kể cả Số dư đầu kỳ) và cả 2 file Excel.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        '- Cộng tăng = Hàng hóa/Dịch vụ + Điều chỉnh công nợ (tăng); Cộng giảm = Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ (giảm).',
        '- Ngày nghiệm thu: hợp đồng hãng cần lắp đặt = ngày biên bản nghiệm thu mới nhất; hợp đồng hãng khác = ngày muộn nhất trong phiếu xuất kho bán hàng (ngày duyệt), phiếu xuất bán hàng mượn, hạch toán dịch vụ; hợp đồng dịch vụ bảo hành - sửa chữa = muộn nhất trong hạch toán dịch vụ, xuất bán hàng mượn, phiếu xuất kho; không có thì lấy ngày bàn giao nghiệm thu khai ở công nợ đầu kỳ quá hạn.',
        '- Định dạng số 1,234,567, không lẻ; số âm có dấu "-"; số 0 để trống, riêng dòng Tổng cộng in "0".',
        '- Excel mẫu in: Giá trị hợp đồng thực tế = Cộng tăng; Giá trị đã thanh toán = Cộng giảm; Giá trị còn nợ cuối kỳ = Số dư cuối kỳ.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        DU_LIEU,
        'Thông báo nguyên văn: "Vui lòng chọn thời gian", "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", "Chọn thời gian để xem báo cáo.", "Không có dữ liệu phù hợp bộ lọc.", "Đang tải dữ liệu...", "Xuất Excel thành công", "Lỗi khi xuất Excel".',
    )),
]

ROLE_TCS = [
    ('01', 'Không có quyền: chỉ thấy hợp đồng mình tạo', 'P0',
     'TK-A không có 4 quyền xem; A tạo HD-TEST-01, HD-TEST-02 có công nợ; B có hợp đồng khác',
     ['1. Đăng nhập TK-A, ' + MENU, '2. Chọn Thời gian tháng này', '3. Quan sát bộ lọc và bảng'],
     'Tài khoản: TK-A',
     ['- Mở được màn, không báo thiếu quyền',
      '- Không có ô Công ty, Phòng ban, Bộ phận, Nhân viên',
      '- Chỉ có 1 dòng nhân viên A với các hợp đồng do A tạo; không có hợp đồng của B',
      '- Số dư đầu kỳ dòng Tổng cộng chỉ tính chứng từ của hợp đồng A tạo (không phải số của toàn hệ thống)']),
    ('02', 'Quyền bộ phận: bộ phận quản lý + bộ phận đang thuộc', 'P0',
     'TK-BP có quyền "' + Q + 'bộ phận", đang thuộc BP1, quản lý BP2',
     ['1. Đăng nhập TK-BP, mở màn, chọn Thời gian tháng này', '2. Quan sát ô lọc và các dòng nhân viên'],
     'Tài khoản: TK-BP',
     ['- Có ô Bộ phận, Nhân viên; không có ô Công ty, Phòng ban',
      '- Có công nợ ghi ở BP1 và BP2, cộng hợp đồng do TK-BP tạo',
      '- Không có công nợ của bộ phận khác']),
    ('03', 'Quyền phòng ban: phòng quản lý + phòng đang thuộc', 'P0',
     'TK-PB có quyền "' + Q + 'phòng ban", đang thuộc P1, quản lý P2',
     ['1. Đăng nhập TK-PB, mở màn, chọn Thời gian tháng này'],
     'Tài khoản: TK-PB',
     ['- Có ô Phòng ban, Bộ phận, Nhân viên; không có ô Công ty',
      '- Có công nợ của P1 và P2, cộng hợp đồng do TK-PB tạo; không có phòng khác']),
    ('04', 'Quyền công ty: công ty đang làm việc', 'P0',
     'TK-CT có quyền "' + Q + 'công ty", đang làm việc ở CT1',
     ['1. Đăng nhập TK-CT, mở màn, chọn Thời gian tháng này', '2. Đổi công ty đang làm việc sang CT2 (nếu tài khoản có), mở lại màn'],
     'Tài khoản: TK-CT',
     ['- Bước 1: có ô Phòng ban, Bộ phận, Nhân viên; chỉ công nợ ghi ở CT1 (cộng hợp đồng mình tạo); không có nhân viên C',
      '- Bước 2: số liệu đổi theo CT2 nếu tài khoản có quyền ở CT2; không có quyền ở CT2 thì chỉ còn hợp đồng mình tạo']),
    ('05', 'Quyền tổng công ty: mọi công ty', 'P0',
     'TK-TCT có quyền "' + Q + 'tổng công ty"',
     ['1. Đăng nhập TK-TCT, mở màn, chọn Thời gian tháng này'],
     'Tài khoản: TK-TCT',
     ['- Có đủ 4 ô Công ty, Phòng ban, Bộ phận, Nhân viên',
      '- Có nhân viên của cả CT1 và CT2']),
    ('06', 'Có nhiều quyền: lấy cấp rộng nhất', 'P1',
     'Một tài khoản có đồng thời quyền "bộ phận" và quyền "công ty"',
     ['1. Đăng nhập, mở màn, chọn Thời gian tháng này'],
     '',
     ['- Phạm vi và ô lọc giống quyền "công ty" (TC-ROLE-04), không bị thu hẹp về bộ phận']),
    ('07', 'Hợp đồng mình tạo luôn thấy dù ngoài phạm vi', 'P1',
     'TK-BP (quyền bộ phận BP1, BP2) tự tạo một hợp đồng mà bút toán ghi ở bộ phận BP3',
     ['1. Đăng nhập TK-BP, lọc tháng này, nhập số hợp đồng đó vào ô Số hợp đồng, nhấn Enter'],
     '',
     ['- Hợp đồng vẫn hiện dưới dòng nhân viên TK-BP']),
    ('08', 'Xuất Excel theo phạm vi quyền', 'P1',
     'TK-BP',
     ['1. Lọc tháng này, bấm "Xuất Excel" > "Xuất file"', '2. Bấm "Xuất Excel mẫu in"', '3. Mở 2 file'],
     '',
     ['- Cả 2 file chỉ có nhân viên / hợp đồng giống trên màn của TK-BP (BP1, BP2 và hợp đồng mình tạo)',
      '- Dòng Tổng cộng trong file bằng dòng Tổng cộng trên màn']),
]

ROLE_TCS = [T(*r) for r in ROLE_TCS]

S1 = [
    T('001', 'Mở màn từ menu', 'P0', 'TK-TCT', [MENU], '',
      ['- Mở màn "Báo cáo tổng hợp công nợ khách hàng theo nhân viên"',
       '- Tiêu đề trang có icon (i); rê chuột hiện đoạn "Tổng hợp công nợ phải thu khách hàng theo nhân viên tạo hợp đồng, chi tiết đến từng hợp đồng…"']),
    T('002', 'Trạng thái lúc mới mở', 'P0', 'Chưa lọc gì (vừa đăng nhập)', ['1. Mở màn', '2. Quan sát bộ lọc và bảng'], '',
      ['- Ô Thời gian trống, có dấu (*)',
       '- Ô tìm nhanh có chữ mờ "Tìm theo số hợp đồng, mã hoặc tên khách hàng"',
       '- Có nút "Tìm kiếm", "Làm mới", "Cài đặt bộ lọc", "Ẩn tìm kiếm nâng cao"',
       '- Bảng ghi "Chọn thời gian để xem báo cáo.", không có dòng Tổng cộng, không có phân trang',
       '- Có nút "Xuất Excel", "Xuất Excel mẫu in"']),
    T('003', 'Tiêu đề cột và icon chú thích', 'P0', 'Đã chọn Thời gian', ['1. Đọc tiêu đề bảng', '2. Rê chuột lần lượt vào icon (i) mỗi cột'], '',
      ['- Đủ 16 cột theo thứ tự ở mục 5, tiêu đề 2 tầng "Phát sinh tăng trong kỳ" (3 cột) và "Phát sinh giảm trong kỳ" (4 cột)',
       '- Mỗi icon hiện chú thích; ví dụ cột Số dư cuối kỳ: "Công nợ phải thu còn lại tại "Đến ngày"." kèm công thức "Số dư cuối kỳ = Số dư đầu kỳ + Cộng phát sinh tăng - Cộng phát sinh giảm + Trả lại tiền thừa."',
       '- Icon cạnh chữ "Tổng cộng": "Phát sinh cộng trên toàn bộ dòng theo bộ lọc. Số dư đầu kỳ tính mọi chứng từ trước "Từ ngày" (kể cả chưa gắn nhân viên / khách hàng), giống ERP."']),
    T('004', 'Tiêu đề dính khi cuộn, thanh cuộn ngang', 'P2', 'Có trên 20 dòng', ['1. Chọn 50 dòng/trang, cuộn dọc bảng', '2. Cuộn ngang'], '',
      ['- Tiêu đề bảng đứng yên trên cùng khi cuộn dọc', '- Có thanh cuộn ngang ở cả trên và dưới bảng']),
    T('005', 'Ẩn / hiện khu vực bộ lọc', 'P2', '', ['1. Bấm "Ẩn tìm kiếm nâng cao"', '2. Bấm "Tìm kiếm nâng cao"'], '',
      ['- Bước 1: các ô lọc thu gọn, còn ô tìm nhanh và nút; nút đổi chữ thành "Tìm kiếm nâng cao"', '- Bước 2: các ô lọc hiện lại']),
    T('006', 'Ghi nhớ bộ lọc khi rời màn', 'P1', 'Đã chọn Thời gian và Khách hàng', ['1. Sang màn khác', '2. Quay lại màn trong 10 phút', '3. Nhấn F5'], '',
      ['- Bước 2: bộ lọc và bảng giữ như lúc rời đi', '- Bước 3: bộ lọc về trống như mới mở, bảng ghi "Chọn thời gian để xem báo cáo."']),
    T('007', 'Cài đặt bộ lọc', 'P2', '', ['1. Bấm "Cài đặt bộ lọc"', '2. Bỏ tích "Ngày nghiệm thu", kéo "Số hợp đồng" lên đầu, bấm "Lưu"', '3. Mở lại, bấm "Khôi phục mặc định", "Lưu"'], '',
      ['- Cửa sổ "Cài đặt bộ lọc" có 6 dòng: Thời gian, Khách hàng, Số hợp đồng, Số dư cuối kỳ, Ngày nghiệm thu, Công ty / Phòng ban / Bộ phận / Nhân viên',
       '- Bước 2: ô Ngày nghiệm thu ẩn, ô Số hợp đồng lên đầu',
       '- Bước 3: về như ban đầu']),
]

S2 = [
    T('001', 'Thời gian bắt buộc', 'P0', 'Mới mở màn', ['1. Không chọn Thời gian, bấm "Tìm kiếm"', '2. Chọn đủ Thời gian'], '',
      ['- Bước 1: chữ đỏ "Vui lòng chọn thời gian" dưới ô Thời gian, bảng không tải',
       '- Bước 2: chữ đỏ mất, bảng tự tải (không cần bấm Tìm kiếm)']),
    T('002', 'Chỉ chọn 1 đầu Thời gian', 'P1', '', ['1. Chọn Từ ngày, để trống Đến ngày'], '',
      ['- Bảng vẫn ghi "Chọn thời gian để xem báo cáo.", không tải số liệu']),
    T('003', 'Không cho chọn ngày ngược chiều', 'P0', '', ['1. Chọn Từ ngày 15/10/2026', '2. Mở lịch Đến ngày, xem tháng 10/2026', '3. Gõ tay 01/10/2026 vào Đến ngày, nhấn Enter'], '',
      ['- Bước 2: các ngày trước 15/10/2026 bị làm mờ, không bấm được',
       '- Bước 3: ô Đến ngày không nhận giá trị, bảng không tải; không có số liệu sai',
       '- Tương tự: lịch Từ ngày làm mờ các ngày sau Đến ngày đã chọn']),
    T('004', 'Từ ngày bằng Đến ngày', 'P1', 'KH-TEST có phiếu thu hạch toán hôm nay', ['1. Chọn Từ ngày = Đến ngày = hôm nay, Khách hàng = KH-TEST'], '',
      ['- Bảng có số; phiếu thu hôm nay nằm ở cột "Đã thanh toán"']),
    T('005', 'Lọc Khách hàng', 'P0', 'KH-TEST có hợp đồng của nhân viên A và B', ['1. Ô Khách hàng gõ 1 ký tự', '2. Gõ thêm cho đủ 2 ký tự mã KH-TEST, chọn', '3. Bấm nút x xoá ô'], '',
      ['- Bước 1: chưa tìm (cần ít nhất 2 ký tự)',
       '- Bước 2: bảng tự tải lại, chỉ còn hợp đồng của KH-TEST dưới dòng A và dòng B',
       '- Bước 3: bảng về đủ khách hàng']),
    T('006', 'Lọc Số hợp đồng khớp đúng', 'P0', '', ['1. Nhập đủ "HD-TEST-01" vào ô Số hợp đồng (chưa nhấn Enter)', '2. Nhấn Enter', '3. Sửa thành "HD-TEST" (thiếu), nhấn Enter'], '',
      ['- Bước 1: bảng chưa đổi', '- Bước 2: chỉ còn 1 dòng hợp đồng HD-TEST-01 dưới nhân viên A',
       '- Bước 3: "Không có dữ liệu phù hợp bộ lọc." (ô này không tìm gần đúng)']),
    T('007', 'Ô tìm nhanh theo số hợp đồng / mã / tên khách', 'P0', '', ['1. Gõ "TEST-01" vào ô tìm nhanh, bấm "Tìm kiếm"', '2. Gõ một phần tên KH-TEST, nhấn Enter', '3. Gõ một phần mã KH-TEST, nhấn Enter'], '',
      ['- Bước 1: còn HD-TEST-01 (tìm gần đúng)', '- Bước 2, 3: còn các hợp đồng của KH-TEST',
       '- Số liệu của từng hợp đồng giống khi không tìm (cả hợp đồng, không bị cắt bớt chứng từ)']),
    T('008', 'Ô tìm nhanh không lọc khi chưa Enter', 'P2', '', ['1. Gõ từ khoá, không nhấn Enter / Tìm kiếm', '2. Đổi ô Số dư cuối kỳ'], '',
      ['- Bước 1: bảng chưa đổi', '- Bước 2: bảng tải lại có áp cả từ khoá đã gõ']),
    T('009', 'Lọc Số dư cuối kỳ', 'P0', 'Trong kỳ có hợp đồng dư nợ, dư có và bằng 0',
      ['1. Chọn "Dư nợ"', '2. Chọn "Dư có"', '3. Chọn "Tất cả"', '4. Xoá ô (để trống)'], '',
      ['- Bước 1: mọi dòng hợp đồng có Số dư cuối kỳ lớn hơn 0', '- Bước 2: mọi dòng có Số dư cuối kỳ âm',
       '- Bước 3, 4: đủ mọi hợp đồng, kể cả hợp đồng Số dư cuối kỳ trống (bằng 0)',
       '- Dòng Tổng cộng: các cột phát sinh đổi theo lựa chọn; Số dư đầu kỳ KHÔNG đổi (ghi nhận theo thiết kế)']),
    T('010', 'Lọc Ngày nghiệm thu', 'P1', 'HD-TEST-01 có Ngày nghiệm thu 15/10/2026', ['1. Chọn Ngày nghiệm thu 15/10/2026', '2. Chọn 16/10/2026'], '',
      ['- Bước 1: có HD-TEST-01, mọi dòng có Ngày nghiệm thu 15/10/2026', '- Bước 2: không có HD-TEST-01 (lọc đúng bằng ngày)']),
    T('011', 'Lọc Nhân viên chọn nhiều', 'P0', 'TK-TCT', ['1. Ô Nhân viên chọn A', '2. Chọn thêm B'], '',
      ['- Bước 1: chỉ dòng nhân viên A', '- Bước 2: dòng A và dòng B',
       '- Lọc theo NGƯỜI TẠO hợp đồng (hợp đồng do người khác tạo cho khách của A không hiện dưới A)']),
    T('012', 'Lọc Công ty / Phòng ban / Bộ phận', 'P1', 'TK-TCT', ['1. Chọn Công ty CT1', '2. Chọn Phòng ban P1', '3. Chọn Bộ phận BP1'], '',
      ['- Mỗi bước bảng tự tải lại, chỉ còn công nợ ghi ở đơn vị đã chọn',
       '- Ô Phòng ban / Bộ phận / Nhân viên thu hẹp danh sách theo ô phía trước',
       '- Bấm icon ổ khoá cạnh nhãn: danh sách hiện thêm đơn vị đã khoá']),
    T('013', 'Kết hợp nhiều ô lọc', 'P1', '', ['1. Thời gian tháng này + Nhân viên A + Số dư cuối kỳ "Dư nợ" + Khách hàng KH-TEST'], '',
      ['- Chỉ còn hợp đồng của A, khách KH-TEST, đang dư nợ']),
    T('014', 'Không có dữ liệu', 'P1', '', ['1. Chọn Thời gian, nhập số hợp đồng không tồn tại, nhấn Enter'], '',
      ['- Bảng ghi "Không có dữ liệu phù hợp bộ lọc."', '- Dòng Tổng cộng và chân phân trang ẩn']),
    T('015', 'Làm mới', 'P0', 'Đã chọn nhiều ô lọc', ['1. Bấm "Làm mới"'], '',
      ['- Mọi ô (kể cả Thời gian, ô tìm nhanh) về trống', '- Bảng ghi "Chọn thời gian để xem báo cáo."']),
    T('016', 'Đổi bộ lọc liên tiếp nhanh', 'P2', '', ['1. Đổi Số dư cuối kỳ Dư nợ > Dư có > Tất cả liên tục trong 2 giây'], '',
      ['- Bảng cuối cùng khớp lựa chọn cuối (Tất cả), không hiện số của lần lọc cũ']),
]

S3 = [
    T('001', 'Cấu trúc dòng', 'P0', 'Đã chọn Thời gian tháng này', ['1. Quan sát bảng'], '',
      ['- Dòng đầu "Tổng cộng" nền xám, chữ đậm',
       '- Dòng nhân viên chữ đậm "Mã - Họ tên", STT 1, 2…; dòng hợp đồng STT 1.1, 1.2…',
       '- Dòng hợp đồng: số hợp đồng dạng liên kết, Khách hàng "Mã - Tên"; dòng nhân viên để trống Ngày nghiệm thu, Số ngày nợ']),
    T('002', 'Dòng nhân viên bằng tổng các hợp đồng', 'P0', 'Nhân viên A có 3 hợp đồng trên cùng 1 trang', ['1. Cộng tay từng cột của 3 dòng hợp đồng', '2. So với dòng nhân viên A'], '',
      ['- Mọi cột tiền của dòng A bằng tổng 3 dòng hợp đồng', '- Ví dụ đã đối chiếu trên môi trường thử: 27,940,000 + 7,528,680 + 25,229,820 = 60,698,500 (Số dư đầu kỳ)']),
    T('003', 'Dòng nhân viên tính cả hợp đồng ở trang sau', 'P0', 'Nhân viên A có 15 hợp đồng (10 dòng/trang)', ['1. Ghi số dòng A ở trang 1', '2. Sang trang 2', '3. Đổi 50 dòng/trang'], '',
      ['- Trang 2 vẫn có dòng A, STT nối tiếp (1.11…), số của dòng A GIỐNG trang 1',
       '- Bước 3: dòng A không đổi; bằng tổng đủ 15 hợp đồng']),
    T('004', 'Dòng Tổng cộng không đổi khi chuyển trang', 'P0', 'Có nhiều trang', ['1. Ghi dòng Tổng cộng trang 1', '2. Sang trang cuối, đổi số dòng/trang'], '',
      ['- Dòng Tổng cộng giữ nguyên mọi cột']),
    T('005', 'Tổng cộng các cột phát sinh', 'P0', 'Lọc 1 nhân viên A, Số dư cuối kỳ = Tất cả, 50 dòng/trang', ['1. Cộng tay cột Hàng hóa/Dịch vụ, Đã thanh toán, Trả lại tiền thừa của mọi dòng hợp đồng'], '',
      ['- Bằng số ở dòng Tổng cộng của cột tương ứng']),
    T('006', 'Tổng cộng Số dư đầu kỳ / cuối kỳ', 'P0', 'Lọc 1 nhân viên A', ['1. Lọc Số dư cuối kỳ = Tất cả, ghi Số dư đầu kỳ dòng Tổng cộng (X)', '2. Chọn "Dư nợ"', '3. Kiểm Số dư cuối kỳ dòng Tổng cộng'], '',
      ['- Bước 1: X bằng Số dư đầu kỳ dòng A',
       '- Bước 2: Số dư đầu kỳ dòng Tổng cộng vẫn là X; có thể khác dòng A (dòng A chỉ cộng hợp đồng dư nợ) - ghi nhận theo thiết kế',
       '- Bước 3: Số dư cuối kỳ Tổng cộng = Số dư đầu kỳ Tổng cộng + Cộng tăng - Cộng giảm + Trả lại tiền thừa (ví dụ đã đối chiếu: 60,624,980 + 7,767,360 - 10,000,000 = 58,392,340)']),
    T('007', 'Cột Cộng tăng / Cộng giảm', 'P0', 'Có dòng có đủ các cột', ['1. Kiểm 1 dòng hợp đồng và dòng Tổng cộng'], '',
      ['- Cộng (tăng) = Hàng hóa/Dịch vụ + Điều chỉnh công nợ (nhóm tăng)', '- Cộng (giảm) = Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ (nhóm giảm)']),
    T('008', 'Cột Số dư cuối kỳ', 'P0', '', ['1. Kiểm 3 dòng hợp đồng bất kỳ'], '',
      ['- Số dư cuối kỳ = Số dư đầu kỳ + Cộng (tăng) - Cộng (giảm) + Trả lại tiền thừa',
       '- Ví dụ đã đối chiếu: 27,940,000 - 10,000,000 = 17,940,000']),
    T('009', 'Định dạng số', 'P1', '', ['1. Quan sát các cột tiền'], '',
      ['- Dạng 1,234,567, không có số lẻ', '- Số âm có dấu "-" (ví dụ -520,344)',
       '- Số 0 để trống ở dòng nhân viên / hợp đồng; dòng Tổng cộng in "0"']),
    T('010', 'Hợp đồng toàn số 0 vẫn hiện', 'P2', 'Hợp đồng đã tất toán trước kỳ', ['1. Lọc Số dư cuối kỳ = Tất cả, nhập số hợp đồng đó'], '',
      ['- Vẫn có 1 dòng, mọi cột tiền trống', '- Chọn "Dư nợ" / "Dư có" thì dòng này không hiện']),
    T('011', 'Chứng từ không gắn hợp đồng', 'P2', 'Có phiếu báo có của khách, chưa gắn hợp đồng, người lập là nhân viên A', ['1. Lọc theo khách đó'], '',
      ['- Dưới dòng A có 1 dòng ô Đơn hàng/hợp đồng TRỐNG (không in "-")']),
    T('012', 'Hợp đồng có chứng từ của 2 khách', 'P2', 'Một hợp đồng có bút toán của 2 khách hàng', ['1. Lọc theo số hợp đồng đó'], '',
      ['- Ghi nhận: 1 dòng duy nhất, cột Khách hàng hiện 1 trong 2 khách']),
    T('013', 'Bấm số hợp đồng', 'P1', '', ['1. Bấm số hợp đồng ở dòng hợp đồng'], '',
      ['- Mở trang xem hợp đồng ở tab mới, đúng hợp đồng', '- Màn báo cáo giữ nguyên bộ lọc, trang đang xem']),
    T('014', 'Ngày nghiệm thu - hợp đồng không cần lắp đặt', 'P0', 'HD-TEST-01 (không lắp đặt) có 2 phiếu xuất kho bán hàng duyệt ngày 05/10 và 20/10/2026 (có sẵn)', ['1. Lọc theo HD-TEST-01'], '',
      ['- Ngày nghiệm thu = 20/10/2026 (ngày muộn nhất)']),
    T('015', 'Ngày nghiệm thu - hợp đồng cần lắp đặt', 'P0', 'Hợp đồng hãng HD-LD (cần lắp đặt) đã xuất hàng 01/10, biên bản nghiệm thu ngày 10/10/2026 (có sẵn)', ['1. Lọc theo HD-LD'], '',
      ['- Ngày nghiệm thu = 10/10/2026 (theo biên bản, không theo ngày xuất kho)', '- Chưa có biên bản: ô trống']),
    T('016', 'Ngày nghiệm thu - xuất bán hàng mượn / hạch toán dịch vụ', 'P1', 'HD-TEST-02 có phiếu xuất bán hàng mượn lập hôm nay', ['1. Vào ' + XBM + ', lập phiếu xuất bán hàng mượn cho HD-TEST-02', '2. Lọc lại báo cáo'], '',
      ['- Ngày nghiệm thu HD-TEST-02 = hôm nay (nếu là ngày muộn nhất)', '- Số ngày nợ = 0']),
    T('017', 'Ngày nghiệm thu dự phòng từ công nợ đầu kỳ quá hạn', 'P2', 'Hợp đồng cũ chỉ có khai báo đầu kỳ công nợ đánh dấu quá hạn, ngày bàn giao nghiệm thu 01/03/2026', ['1. Lọc theo hợp đồng đó'], '',
      ['- Ngày nghiệm thu = 01/03/2026']),
    T('018', 'Công thức Số ngày nợ', 'P0', 'Hợp đồng còn dư nợ, Ngày nghiệm thu cách hôm nay 30 ngày', ['1. Đọc Số ngày nợ (Ngày)', '2. Đổi Đến ngày về tháng trước'], '',
      ['- Bước 1: 24 (30 - 6)', '- Bước 2: Số ngày nợ không đổi theo Đến ngày (tính tới hôm nay) nếu hợp đồng vẫn dư nợ',
       '- Ví dụ đã đối chiếu: nghiệm thu 07/09/2026, xem ngày 02/11/2026 ra 50']),
    T('019', 'Số ngày nợ - chưa quá 6 ngày / hết nợ', 'P1', 'HD1 dư nợ, nghiệm thu 3 ngày trước; HD2 Số dư cuối kỳ bằng 0 hoặc âm', ['1. Đọc Số ngày nợ của HD1, HD2'], '',
      ['- HD1: 0 (không hiện số âm)', '- HD2: trống, Ngày nghiệm thu vẫn hiện']),
    T('020', 'Chân bảng và phân trang', 'P1', 'Có trên 10 dòng hợp đồng', ['1. Đọc chân bảng', '2. Đổi Số dòng/trang 20, 50, 100', '3. Sang trang 2'], '',
      ['- "Hiển thị 1–10 / N dòng hợp đồng", N chỉ đếm dòng hợp đồng', '- Mặc định 10; đổi số dòng thì về trang 1',
       '- Trang 2: STT hợp đồng nối tiếp, STT nhân viên nối tiếp']),
    T('021', 'Khớp với Báo cáo chi tiết công nợ khách hàng', 'P1', 'HD-TEST-01 có phát sinh trong kỳ', ['1. Lọc cùng Thời gian, cùng KH-TEST ở màn này và màn Bán hàng > Báo cáo > Báo cáo công nợ > "Chi tiết công nợ KH"', '2. So các cột của HD-TEST-01'], '',
      ['- Số dư đầu kỳ, các cột phát sinh, Trả lại tiền thừa, Số dư cuối kỳ của HD-TEST-01 bằng nhau ở 2 màn',
       '- Số dư cuối kỳ dòng Tổng cộng bằng nhau ở 2 màn (cùng phạm vi quyền); lệch thì ghi số của từng màn vào Ghi chú']),
]

S4 = [
    T('001', 'Ghi số nền', 'P0', 'Đã có KH-TEST, HD-TEST-01 (mục 9)', ['1. Mở báo cáo, lọc: ' + LOC, '2. Chụp ' + NOI], 'KH-TEST, HD-TEST-01',
      ['- Có đủ số liệu các cột làm số nền cho các TC sau (khách mới thì mọi ô trống)']),
    T('002', 'Phiếu chưa hạch toán không làm đổi số', 'P0', 'Có số nền',
      ['1. Vào ' + YCXH + ', lập yêu cầu xuất hàng 5,000,000 cho HD-TEST-01, CHƯA xuất kho',
       '2. Vào ' + PT + ', lập phiếu thu 1,000,000 cho HD-TEST-01, để chưa duyệt / chưa hạch toán', '3. Lọc lại báo cáo'], '',
      ['- Không cột nào đổi so với số nền']),
    T('003', 'Xuất bán hàng làm tăng Hàng hóa/Dịch vụ', 'P0', 'Có số nền',
      ['1. Vào ' + YCXH + ', lập và duyệt yêu cầu xuất hàng HD-TEST-01 giá trị 10,000,000',
       '2. Kho lập và duyệt phiếu xuất kho (có sẵn quy trình)', '3. Vào ' + PXH + ', lập phiếu xuất hàng, hạch toán hôm nay', '4. Lọc lại báo cáo'],
      'Giá trị: 10,000,000',
      ['- Hàng hóa/Dịch vụ +10,000,000; Cộng (tăng) +10,000,000; Số dư cuối kỳ +10,000,000 ở ' + NOI,
       '- Ngày nghiệm thu HD-TEST-01 = ngày duyệt phiếu xuất kho; Số ngày nợ = 0']),
    T('004', 'Phiếu thu làm tăng Đã thanh toán', 'P0', 'Số nền = sau TC 003',
      ['1. Vào ' + PT + ', lập phiếu thu của KH-TEST cho HD-TEST-01, 4,000,000, duyệt và hạch toán hôm nay', '2. Lọc lại báo cáo'], '4,000,000',
      ['- Đã thanh toán +4,000,000; Cộng (giảm) +4,000,000; Số dư cuối kỳ -4,000,000 ở ' + NOI]),
    T('005', 'Phiếu báo có làm tăng Đã thanh toán', 'P1', 'Số nền = sau TC 004',
      ['1. Vào ' + PBC + ', lập phiếu báo có của KH-TEST cho HD-TEST-01, 1,000,000, hạch toán hôm nay', '2. Lọc lại báo cáo'], '1,000,000',
      ['- Đã thanh toán +1,000,000 (luỹ kế 5,000,000); Số dư cuối kỳ -1,000,000']),
    T('006', 'Điều chỉnh công nợ TĂNG', 'P0', 'Số nền = sau TC 005',
      ['1. Vào ' + YCDC + ', lập yêu cầu điều chỉnh TĂNG công nợ KH-TEST, HD-TEST-01, 2,000,000, gửi duyệt và duyệt',
       '2. Lọc lại báo cáo', '3. Vào ' + PKT + ', lập phiếu kế toán từ yêu cầu, hạch toán hôm nay', '4. Lọc lại báo cáo'], '2,000,000',
      ['- Bước 2: chưa đổi', '- Bước 4: Điều chỉnh công nợ (nhóm tăng) +2,000,000; Cộng (tăng) +2,000,000; Số dư cuối kỳ +2,000,000']),
    T('007', 'Điều chỉnh công nợ GIẢM', 'P0', 'Số nền = sau TC 006',
      ['1. Làm như TC 006 nhưng loại điều chỉnh GIẢM, 500,000', '2. Lọc lại báo cáo'], '500,000',
      ['- Điều chỉnh công nợ (nhóm giảm) +500,000; Cộng (giảm) +500,000; Số dư cuối kỳ -500,000']),
    T('008', 'Khách trả lại hàng', 'P0', 'HD-TEST-01 đã xuất hàng ở TC 003; số nền = sau TC 007',
      ['1. Vào ' + YCNH + ', lập yêu cầu nhập hàng khách trả lại theo HD-TEST-01, 3,000,000, duyệt',
       '2. Lập, duyệt đề nghị nhập kho và phiếu nhập kho', '3. Vào ' + PNH + ', lập phiếu nhập hàng, hạch toán hôm nay', '4. Lọc lại báo cáo'], '3,000,000',
      ['- Nhập trả lại +3,000,000; Cộng (giảm) +3,000,000; Số dư cuối kỳ -3,000,000', '- Trước bước 3 báo cáo chưa đổi']),
    T('009', 'Phiếu chi trả lại tiền thừa', 'P1', 'Số nền = sau TC 008',
      ['1. Vào ' + PC + ', lập phiếu chi trả KH-TEST cho HD-TEST-01, 200,000, hạch toán hôm nay', '2. Lọc lại báo cáo'], '200,000',
      ['- Trả lại tiền thừa +200,000; Số dư cuối kỳ TĂNG 200,000; nhóm Phát sinh giảm không đổi']),
    T('010', 'Phiếu ủy nhiệm chi trả lại tiền thừa', 'P2', 'Số nền = sau TC 009',
      ['1. Vào ' + UNC + ', lập ủy nhiệm chi trả KH-TEST cho HD-TEST-01, 300,000, hạch toán hôm nay', '2. Lọc lại báo cáo'], '300,000',
      ['- Trả lại tiền thừa +300,000 (luỹ kế 500,000); Số dư cuối kỳ tăng 300,000']),
    T('011', 'Hạch toán dịch vụ làm tăng Hàng hóa/Dịch vụ', 'P2', 'KH-TEST có hợp đồng dịch vụ HD-TEST-DV do nhân viên A lập (có sẵn)',
      ['1. Vào ' + HTDV + ', lập và duyệt phiếu hạch toán dịch vụ 1,500,000 cho HD-TEST-DV', '2. Lọc lại báo cáo'], '1,500,000',
      ['- Có / tăng dòng HD-TEST-DV dưới nhân viên A, Hàng hóa/Dịch vụ +1,500,000', '- Ngày nghiệm thu HD-TEST-DV = ngày của phiếu hạch toán']),
    T('012', 'Kiểm tổng sau chuỗi phiếu', 'P0', 'Đã chạy TC 003 đến 010',
      ['1. Lọc lại báo cáo', '2. So Số dư cuối kỳ HD-TEST-01 với số nền TC 001'], '',
      ['- Chênh = +10,000,000 - 4,000,000 - 1,000,000 + 2,000,000 - 500,000 - 3,000,000 + 200,000 + 300,000 = +4,000,000',
       '- Dòng nhân viên A và dòng Tổng cộng cũng chênh đúng +4,000,000']),
    T('013', 'Chứng từ trước Từ ngày vào Số dư đầu kỳ', 'P0', 'Phiếu thu 700,000 cho HD-TEST-01 hạch toán ngày cuối tháng trước',
      ['1. Lọc Thời gian tháng này', '2. Đổi Từ ngày về ngày 1 tháng trước'], '700,000',
      ['- Bước 1: phiếu không ở cột Đã thanh toán mà làm Số dư đầu kỳ giảm 700,000',
       '- Bước 2: phiếu chuyển sang Đã thanh toán; Số dư cuối kỳ không đổi giữa 2 lần lọc']),
    T('014', 'Chứng từ sau Đến ngày không tính', 'P1', 'Phiếu thu cho HD-TEST-01 hạch toán hôm nay', ['1. Lọc Đến ngày = hôm qua', '2. Lọc Đến ngày = hôm nay'], '',
      ['- Bước 1: phiếu không được tính ở cột nào', '- Bước 2: phiếu vào Đã thanh toán']),
    T('015', 'Huỷ hạch toán thì số trả về', 'P1', 'Phiếu thu 4,000,000 ở TC 004', ['1. Kế toán huỷ hạch toán (hoặc huỷ) phiếu thu đó', '2. Lọc lại báo cáo'], '',
      ['- Đã thanh toán giảm lại 4,000,000; Số dư cuối kỳ tăng lại 4,000,000']),
    T('016', 'Thu vượt chuyển sang Dư có', 'P1', 'HD-TEST-01 đang dư nợ 4,000,000',
      ['1. Lập phiếu thu 5,000,000 cho HD-TEST-01, hạch toán hôm nay', '2. Lọc Số dư cuối kỳ = Dư nợ', '3. Lọc Dư có'], '',
      ['- Số dư cuối kỳ HD-TEST-01 = -1,000,000; Số ngày nợ trống', '- Bước 2: không có HD-TEST-01', '- Bước 3: có HD-TEST-01']),
    T('017', 'Hợp đồng mới hiện dưới đúng nhân viên tạo', 'P1', 'HD-TEST-02 do A tạo chưa có phát sinh',
      ['1. Xuất hàng 6,000,000 cho HD-TEST-02 như TC 003', '2. Lọc lại báo cáo'], '',
      ['- HD-TEST-02 hiện dưới dòng nhân viên A, Hàng hóa/Dịch vụ 6,000,000', '- Dòng A tăng 6,000,000 ở Số dư cuối kỳ']),
]

S5 = [
    T('001', 'Xuất Excel chưa chọn Thời gian', 'P0', 'Mới mở màn', ['1. Bấm "Xuất Excel"', '2. Bấm "Xuất Excel mẫu in"'], '',
      ['- Cả 2: thông báo "Vui lòng chọn thời gian", chữ đỏ dưới ô Thời gian, không mở cửa sổ, không tải file']),
    T('002', 'Cửa sổ chọn trường', 'P0', 'Đã chọn Thời gian', ['1. Bấm "Xuất Excel"'], '',
      ['- Cửa sổ "Chọn trường xuất Excel", dòng "Tích chọn trường cần xuất, kéo biểu tượng ba gạch để đổi thứ tự cột trong file."',
       '- 14 trường đều được tích: Nhân viên / Đơn hàng - hợp đồng, Khách hàng, Số dư đầu kỳ, PS tăng - Hàng hóa/Dịch vụ, PS tăng - Điều chỉnh công nợ, PS tăng - Cộng, PS giảm - Nhập trả lại, PS giảm - Đã thanh toán, PS giảm - Điều chỉnh công nợ, PS giảm - Cộng, Trả lại tiền thừa, Số dư cuối kỳ, Ngày nghiệm thu, Số ngày nợ (Ngày)',
       '- Có "Chọn tất cả", "Bỏ chọn hết", "Đang chọn 14/14 trường", "Xuất file", "Đóng"']),
    T('003', 'Bỏ chọn hết trường', 'P1', 'Cửa sổ đang mở', ['1. Bấm "Bỏ chọn hết"', '2. Bấm "Chọn tất cả"'], '',
      ['- Bước 1: "Đang chọn 0/14 trường", nút "Xuất file" không bấm được', '- Bước 2: về 14/14']),
    T('004', 'Nội dung file khớp màn hình', 'P0', 'Lọc 1 nhân viên A (nhiều trang)', ['1. Bấm "Xuất Excel" > "Xuất file"', '2. Mở file'], '',
      ['- Thông báo "Xuất Excel thành công", file bao_cao_tong_hop_cong_no_khach_hang_theo_nhan_vien.xlsx',
       '- Dòng 1 "BÁO CÁO TỔNG HỢP CÔNG NỢ KHÁCH HÀNG THEO NHÂN VIÊN", dòng 2 "Thời gian: dd/mm/yyyy - dd/mm/yyyy", tiêu đề 2 tầng',
       '- Dòng Tổng cộng, dòng nhân viên (đậm), dòng hợp đồng; có ĐỦ hợp đồng của mọi trang',
       '- Số từng dòng bằng số trên màn; số dạng 1,234,567']),
    T('005', 'Đổi thứ tự / bỏ bớt trường', 'P1', '', ['1. Bỏ tích Khách hàng, kéo Số dư cuối kỳ lên đầu', '2. Xuất file'], '',
      ['- File không có cột Khách hàng; cột STT đứng đầu, ngay sau là Số dư cuối kỳ']),
    T('006', 'Xuất khi không có dữ liệu', 'P2', 'Lọc số hợp đồng không tồn tại', ['1. Xuất Excel > Xuất file'], '',
      ['- Vẫn tải file: tiêu đề, dòng thời gian, tên cột, dòng Tổng cộng']),
    T('007', 'Xuất Excel mẫu in', 'P0', 'Lọc 1 nhân viên A', ['1. Bấm "Xuất Excel mẫu in"', '2. Mở file'], '',
      ['- Tải ngay (không có cửa sổ chọn trường), "Xuất Excel thành công", file bao_cao_tong_hop_cong_no_khach_hang_theo_nhan_vien_mau_in.xlsx',
       '- Cột: STT, Đơn hàng/Hợp đồng, Khách hàng, Số dư đầu kỳ, Giá trị hợp đồng thực tế, Giá trị đã thanh toán, Giá trị còn nợ cuối kỳ, Ngày nghiệm thu, Ngày xuất hóa đơn, Số ngày nợ (Ngày), Giải trình lý do chưa thu nợ, Kế hoạch ngày thu hồi công nợ, Xác nhận công nợ (Đã có / Chưa có / Lý do chưa xác nhận nợ)',
       '- Ngày xuất hóa đơn và các cột giải trình / kế hoạch / xác nhận để trống']),
    T('008', 'Công thức các cột mẫu in', 'P0', 'File mẫu in của TC 007 và màn đang lọc như nhau', ['1. So 1 dòng hợp đồng giữa file và màn'], '',
      ['- Giá trị hợp đồng thực tế = Cộng (tăng) trên màn', '- Giá trị đã thanh toán = Cộng (giảm) trên màn',
       '- Giá trị còn nợ cuối kỳ = Số dư cuối kỳ trên màn (đã gồm Trả lại tiền thừa)']),
]

S6 = [
    T('001', 'Thời gian tải khi chỉ lọc Thời gian', 'P1', 'TK-TCT, Thời gian 1 tháng, không lọc khác (trên môi trường thử khoảng 25,000 dòng hợp đồng)', ['1. Chọn Thời gian, bấm giờ tới khi bảng hiện số'], '',
      ['- Bảng hiện trong 10 giây (đo trên môi trường thử 02/11/2026: khoảng 4,7 giây)']),
    T('002', 'Thời gian tải kỳ dài', 'P2', 'TK-TCT, Thời gian 01/01/2026 - 31/10/2026', ['1. Chọn Thời gian, bấm giờ'], '',
      ['- Bảng hiện trong 10 giây (đo trên môi trường thử: khoảng 4,1 giây)']),
    T('003', 'Chuyển trang nhanh', 'P2', 'Đã tải 1 tháng không lọc', ['1. Sang trang 2, trang cuối'], '',
      ['- Mỗi lần chuyển trang hiện trong 5 giây, dòng Tổng cộng không tải lại']),
    T('004', 'Xuất Excel khi chỉ lọc Thời gian', 'P1', 'TK-TCT, Thời gian 1 tháng, không lọc khác', ['1. Bấm "Xuất Excel" > "Xuất file", bấm giờ', '2. Bấm "Xuất Excel mẫu in"'], '',
      ['- Tải được file đủ mọi dòng trong 60 giây, không báo lỗi',
       '- Ghi chú: đo trên môi trường thử 02/11/2026 KHÔNG tải được (báo lỗi sau khoảng 8 giây) - ghi kết quả thực tế vào cột Ghi chú']),
]

SECTIONS = [
    ('I', 'GIAO DIỆN & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'SỐ LIỆU, DÒNG TỔNG & PHÂN TRANG', S3),
    ('IV', 'LUỒNG PHÁT SINH: LẬP CHỨNG TỪ - KIỂM SỐ', S4),
    ('V', 'XUẤT EXCEL', S5),
    ('VI', 'HIỆU NĂNG', S6),
]

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1',
          feature_name=TEN + ' - Cập nhật ngày ' + L.NGAY, module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
    print('Số TC: phân quyền %d · ' % len(ROLE_TCS) + ' · '.join('%s %d' % (t, len(s)) for _, t, s in SECTIONS)
          + ' · tổng %d' % (len(ROLE_TCS) + sum(len(s) for _, _, s in SECTIONS)))

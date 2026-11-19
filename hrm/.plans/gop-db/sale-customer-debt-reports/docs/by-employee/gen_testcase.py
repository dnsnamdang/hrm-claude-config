# -*- coding: utf-8 -*-
"""Testcase "BC tổng hợp công nợ KH theo nhân viên" — KHUÔN CHUẨN tab "13. DM quốc gia" (loại bao_cao, 03/11/2026).

Viết lại từ gen_testcase_v1.py (bản 02/11 sai khuôn, giữ để tra): giữ mọi case nghiệp vụ, xếp lại theo nhóm chuẩn
(xuat-tai-lieu-chuyen-doi/TC_CHUAN.md), bổ sung case theo checklist "Mẫu tài liệu.xlsx". Case chung sinh từ
../compare/_tc_bc_chung.py (dùng chung 3 màn báo cáo công nợ).
Màn KHÔNG có popup chi tiết, KHÔNG có nút In, KHÔNG có sắp xếp / tùy chỉnh cột => không có các nhóm đó.
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
TEN = 'BC tổng hợp công nợ KH theo nhân viên'
MODULE = 'BC công nợ KH theo NV'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)


def L_(*lines):
    return '\n'.join(lines)


MENU = 'Vào phân hệ Bán hàng > Báo cáo > nhóm Báo cáo công nợ > bấm "Tổng hợp công nợ theo NV"'
Q = 'Xem báo cáo tổng hợp công nợ khách hàng theo nhân viên - '
LOC = 'Chọn Thời gian = ngày 1 tháng này đến hôm nay, Khách hàng = KH-TEST'
LN = 'Chọn thời gian để xem báo cáo.'
NOI = 'dòng hợp đồng HD-TEST-01, dòng nhân viên A (in đậm, phía trên) và dòng Tổng cộng'
PT_ = 'Tài chính > Quản lý tiền > "Phiếu thu"'
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
NHIEU = 'Tài khoản TK-TCT (quyền tổng công ty); Thời gian 1 tháng cho ra hơn 30 dòng hợp đồng.'
NEN = 'Đã ghi số nền của ' + NOI + ' (case "Ghi số nền trước khi lập chứng từ").'

M = {
    'dv': 'dòng hợp đồng',
    'loc': 'Đăng nhập TK-TCT, chọn Thời gian 01/10/2026 - 31/10/2026',
    'nhieu_trang': NHIEU,
    'tong_ghi_chu': ' (không đếm dòng nhân viên, dòng Tổng cộng)',
    'doi_loc': 'Chọn Số dư cuối kỳ = "Dư nợ"',
    'tu_khoa': 'HD-TEST',
    'loi_nhac': LN,
    'man_khac': 'Bán hàng > Báo cáo > Báo cáo công nợ > Chi tiết công nợ KH',
    'excel_file': 'bao_cao_tong_hop_cong_no_khach_hang_theo_nhan_vien.xlsx',
    'so_truong': '14',
    'xl_ngay': 'Cột Ngày nghiệm thu hiển thị dạng dd/mm/yyyy; Số ngày nợ là số nguyên',
    'nhom_quyen': 'Báo cáo tổng hợp công nợ khách hàng theo nhân viên',
    'menu': MENU,
    'nut': 'Xuất Excel, Xuất Excel mẫu in',
    'url': '<địa chỉ hệ thống>/sale/customer-debt-by-employee',
    'quyen_rong': Q + 'tổng công ty',
    'co_dau': 'Từ khóa: "BÁCH LIÊN" rồi "BACH LIEN"',
    'loc_khong_kh': 'Chọn Thời gian 01/01/2026 - 31/10/2026, không chọn Khách hàng',
}
PT = pt_chung(M)
M['loc'] = LOC

DU_LIEU = L_(
    'Dữ liệu mẫu (lập trước khi test, ghi mã thật vào cột Ghi chú nếu khác):',
    '-  KH-TEST: khách hàng mới, chưa có phát sinh. HD-TEST-01, HD-TEST-02: hợp đồng bán hàng của KH-TEST do nhân viên A lập, đã ký, hàng KHÔNG cần lắp đặt (có sẵn).',
    '-  Nhân viên A thuộc công ty CT1, phòng P1, bộ phận BP1; nhân viên B thuộc phòng P2, bộ phận BP2; nhân viên C thuộc công ty CT2.',
    '-  TK-A: tài khoản nhân viên A, không có quyền xem nào. TK-BP: có quyền "' + Q + 'bộ phận", đang thuộc BP1, quản lý BP2.',
    '-  TK-PB: có quyền "' + Q + 'phòng ban", đang thuộc P1, quản lý P2. TK-CT: có quyền "' + Q + 'công ty" (đang làm việc ở CT1). TK-TCT: có quyền "' + Q + 'tổng công ty".',
    '-  Trước mỗi case lập chứng từ ghi lại "số nền" (số đang có) của ' + NOI + '; kết quả đúng là phần CHÊNH so với số nền.',
    '-  Chứng từ phải được HẠCH TOÁN (ghi sổ) mới lên báo cáo. Ai không lập / duyệt được phiếu thì nhờ kế toán, chỉ cần đúng khách hàng, hợp đồng, số tiền, ngày hạch toán.',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Báo cáo công nợ phải thu GOM THEO NHÂN VIÊN TẠO HỢP ĐỒNG: mỗi nhân viên có những hợp đồng nào còn nợ, nợ bao nhiêu, nghiệm thu ngày nào, đã nợ bao nhiêu ngày. Dùng để giao nhân viên thu hồi công nợ. Màn chỉ xem, có Xuất Excel (chọn trường) và Xuất Excel mẫu in.',
        'Đường vào: ' + MENU + '.',
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Nguồn: bút toán tài khoản phải thu khách hàng 131 (và tài khoản con) sinh ra khi chứng từ được hạch toán. Cột và chứng từ làm nó đổi:',
        '-  Số dư đầu kỳ: mọi phát sinh có ngày hạch toán trước Từ ngày (Nợ trừ Có).',
        '-  Hàng hóa/Dịch vụ: phiếu xuất kho, phiếu xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, hạch toán dịch vụ bảo hành - sửa chữa, khai báo công nợ đầu kỳ.',
        '-  Điều chỉnh công nợ (nhóm tăng / nhóm giảm): phiếu kế toán điều chỉnh công nợ ghi tăng / ghi giảm.',
        '-  Nhập trả lại: phiếu nhập hàng khách trả lại. Đã thanh toán: phiếu thu, phiếu báo có, khai báo công nợ đầu kỳ (phần đã thu).',
        '-  Trả lại tiền thừa: phiếu chi, phiếu ủy nhiệm chi; làm số dư TĂNG.',
        '-  Số dư cuối kỳ = Đầu kỳ + Cộng tăng - Cộng giảm + Trả lại tiền thừa. Dương = Dư nợ, âm = Dư có.',
        '-  Ngày nghiệm thu, Số ngày nợ (= hôm nay - (Ngày nghiệm thu + 6 ngày), âm thì 0, chỉ hiện khi còn dư nợ).',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '-  Bút toán chưa gắn khách hàng, chưa có nhân viên tạo hợp đồng hoặc số tiền bằng 0: không thành dòng hợp đồng (nhưng VẪN tính vào Số dư đầu kỳ của dòng Tổng cộng).',
        '-  Chứng từ chưa hạch toán, chứng từ có ngày hạch toán sau Đến ngày.',
        '-  Hợp đồng ngoài phạm vi quyền xem (mục 7).',
        '-  Số ngày nợ để trống khi hợp đồng không còn dư nợ hoặc không xác định được Ngày nghiệm thu.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô "Thời gian" (Từ ngày - Đến ngày) BẮT BUỘC, lọc theo NGÀY HẠCH TOÁN: trước Từ ngày vào Số dư đầu kỳ, từ Từ ngày đến hết Đến ngày vào phát sinh.',
        'Mở màn chưa có Thời gian: bảng ghi "' + LN + '". Chọn đủ 2 ngày thì bảng tự tải.',
        'Lịch không cho chọn Từ ngày sau Đến ngày (ngày bị làm mờ, gõ tay không nhận).',
        'Ô "Ngày nghiệm thu" (không bắt buộc) lọc hợp đồng có Ngày nghiệm thu ĐÚNG BẰNG ngày chọn.',
        'Số ngày nợ luôn tính tới HÔM NAY, không theo Đến ngày.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Bảng 16 cột, tiêu đề 2 tầng: STT, Đơn hàng/hợp đồng, Khách hàng, Số dư đầu kỳ, [Phát sinh tăng trong kỳ: Hàng hóa/Dịch vụ, Điều chỉnh công nợ, Cộng], [Phát sinh giảm trong kỳ: Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ, Cộng], Trả lại tiền thừa, Số dư cuối kỳ, Ngày nghiệm thu, Số ngày nợ (Ngày). Mọi đầu cột có icon (i) chú thích.',
        'Thứ tự dòng: Tổng cộng > dòng nhân viên in đậm "Mã - Họ tên" (STT 1, 2…) > dòng hợp đồng (STT 1.1, 1.2…, số hợp đồng bấm được mở tab mới, Khách hàng "Mã - Tên").',
        'Phân trang theo DÒNG HỢP ĐỒNG: mặc định 10, chọn 10/20/50/100; chân bảng "Hiển thị a–b / N dòng hợp đồng". Không có sắp xếp cột, không có tùy chỉnh cột, không có cửa sổ chi tiết chứng từ, không có nút In.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '-  Gom theo (nhân viên tạo hợp đồng, hợp đồng): mỗi hợp đồng 1 dòng; hợp đồng có số liệu toàn 0 vẫn hiện khi Số dư cuối kỳ = Tất cả.',
        '-  Hợp đồng có bút toán của nhiều khách: cột Khách hàng chỉ hiện 1 khách (ghi nhận).',
        '-  Dòng nhân viên = cộng ĐỦ mọi hợp đồng của nhân viên theo bộ lọc, KỂ CẢ hợp đồng ở trang sau.',
        '-  Dòng Tổng cộng: cột phát sinh = cộng mọi dòng (mọi trang); Số dư đầu kỳ = mọi bút toán trước Từ ngày trong phạm vi quyền (không theo ô Số dư cuối kỳ, Ngày nghiệm thu, ô tìm nhanh); Số dư cuối kỳ = Đầu kỳ (Tổng cộng) + Cộng tăng - Cộng giảm + Trả lại tiền thừa.',
    )),
    ('7. Phân quyền cấp', L_(
        'Mọi tài khoản mở được màn. 4 quyền chỉ mở rộng PHẠM VI (có nhiều quyền thì lấy cấp rộng nhất):',
        '-  "' + Q + 'tổng công ty": mọi công ty; có ô Công ty, Phòng ban, Bộ phận, Nhân viên.',
        '-  "' + Q + 'công ty": công ty đang làm việc + hợp đồng mình tạo; có ô Phòng ban, Bộ phận, Nhân viên.',
        '-  "' + Q + 'phòng ban": phòng mình quản lý + phòng mình đang thuộc + hợp đồng mình tạo; có ô Phòng ban, Bộ phận, Nhân viên.',
        '-  "' + Q + 'bộ phận": bộ phận mình quản lý + bộ phận đang thuộc + hợp đồng mình tạo; có ô Bộ phận, Nhân viên.',
        '-  Không quyền: chỉ hợp đồng mình tạo; không có 4 ô lọc tổ chức.',
        'Phạm vi áp cho mọi dòng, dòng Tổng cộng (kể cả Số dư đầu kỳ) và cả 2 file Excel.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        '-  Cộng tăng = Hàng hóa/Dịch vụ + Điều chỉnh công nợ (tăng); Cộng giảm = Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ (giảm).',
        '-  Ngày nghiệm thu: hợp đồng hãng cần lắp đặt = ngày biên bản nghiệm thu mới nhất; hợp đồng hãng khác = ngày muộn nhất trong phiếu xuất kho bán hàng (ngày duyệt), phiếu xuất bán hàng mượn, hạch toán dịch vụ; hợp đồng dịch vụ bảo hành - sửa chữa = muộn nhất trong hạch toán dịch vụ, xuất bán hàng mượn, phiếu xuất kho; không có thì lấy ngày bàn giao nghiệm thu khai ở công nợ đầu kỳ quá hạn.',
        '-  Định dạng số 1,234,567, không lẻ; số âm có dấu "-"; số 0 để trống, riêng dòng Tổng cộng in "0".',
        '-  Excel mẫu in: Giá trị hợp đồng thực tế = Cộng tăng; Giá trị đã thanh toán = Cộng giảm; Giá trị còn nợ cuối kỳ = Số dư cuối kỳ.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        DU_LIEU,
        'Thông báo nguyên văn: "Vui lòng chọn thời gian", "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", "' + LN + '", "Không có dữ liệu phù hợp bộ lọc.", "Đang tải dữ liệu...", "Xuất Excel thành công", "Lỗi khi xuất Excel".',
    )),
]

# ================================================================== I. HIỂN THỊ TRANG & TRUY CẬP
G1 = [
    C('Mở màn hình từ menu', 'P0', 'Tài khoản TK-TCT đã đăng nhập.', ['1. ' + MENU], '',
      ['Mở màn "Báo cáo tổng hợp công nợ khách hàng theo nhân viên"',
       'Tiêu đề trang có icon (i); rê chuột hiện đoạn "Tổng hợp công nợ phải thu khách hàng theo nhân viên tạo hợp đồng, chi tiết đến từng hợp đồng…"']),
    C('Trạng thái lúc mới mở và các nút chức năng', 'P0', 'Chưa lọc gì (vừa đăng nhập).', ['1. Mở màn', '2. Quan sát bộ lọc và bảng'], '',
      ['Ô Thời gian trống, có dấu (*)',
       'Ô tìm nhanh có chữ mờ "Tìm theo số hợp đồng, mã hoặc tên khách hàng"',
       'Có nút "Tìm kiếm", "Làm mới", "Cài đặt bộ lọc", "Ẩn tìm kiếm nâng cao"',
       'Bảng ghi "' + LN + '", không có dòng Tổng cộng, không có phân trang',
       'Có nút "Xuất Excel", "Xuất Excel mẫu in"; không có nút In, Thêm, Sửa, Xóa']),
    C('Kiểm tra đủ các cột của bảng', 'P0', 'Đã chọn Thời gian.', ['1. Đọc tiêu đề bảng từ trái sang phải'], '',
      ['Đủ 16 cột theo thứ tự: STT, Đơn hàng/hợp đồng, Khách hàng, Số dư đầu kỳ, Phát sinh tăng trong kỳ (Hàng hóa/Dịch vụ, Điều chỉnh công nợ, Cộng), '
       'Phát sinh giảm trong kỳ (Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ, Cộng), Trả lại tiền thừa, Số dư cuối kỳ, Ngày nghiệm thu, Số ngày nợ (Ngày)',
       'Bảng không có cột ẩn / cột tùy chọn, không có nút cấu hình cột']),
    C('Nội dung icon (i) của tiêu đề cột', 'P2', 'Đã chọn Thời gian.', ['1. Rê chuột lần lượt vào icon (i) mỗi cột', '2. Rê chuột vào icon (i) cạnh chữ "Tổng cộng"'], '',
      ['Mỗi icon hiện chú thích; ví dụ cột Số dư cuối kỳ: "Công nợ phải thu còn lại tại "Đến ngày"." kèm công thức "Số dư cuối kỳ = Số dư đầu kỳ + Cộng phát sinh tăng - Cộng phát sinh giảm + Trả lại tiền thừa."',
       'Icon cạnh chữ "Tổng cộng": "Phát sinh cộng trên toàn bộ dòng theo bộ lọc. Số dư đầu kỳ tính mọi chứng từ trước "Từ ngày" (kể cả chưa gắn nhân viên / khách hàng)…"']),
    C('Cấu trúc 3 loại dòng', 'P0', 'Đã chọn Thời gian tháng này, có dữ liệu.', ['1. Quan sát bảng'], '',
      ['Dòng đầu "Tổng cộng" nền xám, chữ đậm',
       'Dòng nhân viên chữ đậm "Mã - Họ tên", STT 1, 2…; dòng hợp đồng STT 1.1, 1.2…',
       'Dòng hợp đồng: số hợp đồng dạng liên kết, Khách hàng "Mã - Tên"; dòng nhân viên để trống Ngày nghiệm thu, Số ngày nợ']),
    C('Tiêu đề dính khi cuộn, thanh cuộn ngang', 'P2', 'Có trên 20 dòng hợp đồng.', ['1. Chọn 50 dòng/trang, cuộn dọc bảng', '2. Cuộn ngang'], '',
      ['Tiêu đề bảng đứng yên trên cùng khi cuộn dọc', 'Có thanh cuộn ngang ở cả trên và dưới bảng']),
    C('Hiển thị khi không có dữ liệu', 'P1', 'Đã chọn Thời gian.', ['1. Nhập số hợp đồng không tồn tại vào ô Số hợp đồng, nhấn Enter'], 'Số hợp đồng: HD-KHONG-CO-999',
      ['Bảng ghi "Không có dữ liệu phù hợp bộ lọc."', 'Dòng Tổng cộng và chân phân trang ẩn']),
    C('Khách hàng chưa có phát sinh nào', 'P2', 'KH-MOI vừa tạo, chưa có chứng từ công nợ nào.',
      ['1. Chọn Thời gian 01/01/2026 - 31/10/2026, Khách hàng KH-MOI'], 'Khách hàng: KH-MOI',
      ['Bảng ghi "Không có dữ liệu phù hợp bộ lọc."', 'Màn không báo lỗi; 2 nút Xuất Excel vẫn bấm được']),
    C('Thứ tự mặc định của dòng nhân viên và dòng hợp đồng', 'P1', 'Có ít nhất 2 nhân viên, mỗi người ít nhất 2 hợp đồng trong kỳ.',
      ['1. Chọn Thời gian tháng này', '2. Đọc thứ tự dòng nhân viên', '3. Đọc thứ tự dòng hợp đồng dưới 1 nhân viên'], '',
      ['Dòng nhân viên xếp cố định theo nhân viên (cùng thứ tự mỗi lần mở lại), không đổi khi chuyển trang',
       'Dòng hợp đồng của 1 nhân viên xếp theo thứ tự hợp đồng được tạo (tạo trước đứng trước)']),
    C('Số thứ tự liên tục qua các trang', 'P0', NHIEU,
      ['1. Đăng nhập TK-TCT, chọn Thời gian 01/10/2026 - 31/10/2026', '2. Ghi STT dòng hợp đồng cuối trang 1 và STT dòng nhân viên đang có', '3. Sang trang 2'], '',
      ['STT hợp đồng nối tiếp (vd 1.11 sau 1.10), STT nhân viên nối tiếp, không quay về 1',
       'Nhân viên có hợp đồng vắt sang trang 2 vẫn hiện lại dòng nhân viên ở đầu trang 2 với cùng STT']),
    C('Dữ liệu trên bảng đúng với chứng từ đã tạo', 'P0', 'HD-TEST-01 có 1 phiếu thu đã hạch toán trong kỳ.',
      ['1. ' + LOC, '2. Bấm số HD-TEST-01, mở hợp đồng ở tab mới', '3. So khách hàng, người tạo hợp đồng với dòng trên báo cáo'], '',
      ['Dòng HD-TEST-01 nằm dưới đúng nhân viên tạo hợp đồng, cột Khách hàng đúng mã - tên của hợp đồng',
       'Cột Đã thanh toán có đúng số tiền của phiếu thu']),
] + PT + [
    C('Thời gian tải khi chỉ lọc Thời gian', 'P1', 'TK-TCT, Thời gian 1 tháng, không lọc khác (môi trường thử khoảng 25,000 dòng hợp đồng).',
      ['1. Chọn Thời gian, bấm giờ tới khi bảng hiện số'], '',
      ['Bảng hiện trong 10 giây (đo trên môi trường thử 02/11/2026: khoảng 4,7 giây)']),
    C('Thời gian tải kỳ dài', 'P2', 'TK-TCT, Thời gian 01/01/2026 - 31/10/2026.', ['1. Chọn Thời gian, bấm giờ'], '',
      ['Bảng hiện trong 10 giây (đo trên môi trường thử: khoảng 4,1 giây)']),
    C('Chuyển trang nhanh', 'P2', 'Đã tải 1 tháng không lọc.', ['1. Sang trang 2, trang cuối'], '',
      ['Mỗi lần chuyển trang hiện trong 5 giây, dòng Tổng cộng không tải lại']),
]

# ================================================================== II. TÌM KIẾM & LỌC DANH SÁCH
G2 = [
    C('Mặc định mọi ô lọc trống', 'P1', 'Lần đầu mở màn trong phiên làm việc.', ['1. Mở màn', '2. Quan sát khu vực lọc'], '',
      ['Thời gian, Khách hàng, Số hợp đồng, Số dư cuối kỳ, Ngày nghiệm thu, ô tìm nhanh và các ô tổ chức đều trống']),
    C('Thời gian bắt buộc', 'P0', 'Mới mở màn.', ['1. Không chọn Thời gian, bấm "Tìm kiếm"', '2. Chọn đủ Thời gian'], '',
      ['Bước 1: chữ đỏ "Vui lòng chọn thời gian" dưới ô Thời gian, bảng không tải',
       'Bước 2: chữ đỏ mất, bảng tự tải (không cần bấm Tìm kiếm)']),
    C('Chỉ chọn 1 đầu Thời gian', 'P1', 'Mới mở màn.', ['1. Chọn Từ ngày, để trống Đến ngày'], '',
      ['Bảng vẫn ghi "' + LN + '", không tải số liệu']),
    C('Không cho chọn ngày ngược chiều', 'P0', 'Mới mở màn.', ['1. Chọn Từ ngày 15/10/2026', '2. Mở lịch Đến ngày, xem tháng 10/2026', '3. Gõ tay 01/10/2026 vào Đến ngày, nhấn Enter'], '',
      ['Bước 2: các ngày trước 15/10/2026 bị làm mờ, không bấm được',
       'Bước 3: ô Đến ngày không nhận giá trị, bảng không tải; không có số liệu sai',
       'Tương tự: lịch Từ ngày làm mờ các ngày sau Đến ngày đã chọn']),
    C('Từ ngày bằng Đến ngày', 'P1', 'KH-TEST có phiếu thu hạch toán hôm nay.', ['1. Chọn Từ ngày = Đến ngày = hôm nay, Khách hàng = KH-TEST'], '',
      ['Bảng có số; phiếu thu hôm nay nằm ở cột "Đã thanh toán"']),
    C('Lọc Khách hàng', 'P0', 'KH-TEST có hợp đồng của nhân viên A và B.', ['1. Ô Khách hàng gõ 1 ký tự', '2. Gõ thêm cho đủ 2 ký tự mã KH-TEST, chọn', '3. Bấm nút x xóa ô'], '',
      ['Bước 1: chưa tìm (cần ít nhất 2 ký tự)',
       'Bước 2: bảng tự tải lại, chỉ còn hợp đồng của KH-TEST dưới dòng A và dòng B',
       'Bước 3: bảng về đủ khách hàng']),
    C('Lọc Số hợp đồng khớp đúng', 'P0', 'Đã chọn Thời gian tháng này.', ['1. Nhập đủ "HD-TEST-01" vào ô Số hợp đồng (chưa nhấn Enter)', '2. Nhấn Enter', '3. Sửa thành "HD-TEST" (thiếu), nhấn Enter'], '',
      ['Bước 1: bảng chưa đổi', 'Bước 2: chỉ còn 1 dòng hợp đồng HD-TEST-01 dưới nhân viên A',
       'Bước 3: "Không có dữ liệu phù hợp bộ lọc." (ô này không tìm gần đúng)']),
    C('Tìm nhanh theo số hợp đồng / mã / tên khách (khớp chính xác và một phần)', 'P0', 'Đã chọn Thời gian tháng này.',
      ['1. Gõ đủ "HD-TEST-01" vào ô tìm nhanh, bấm "Tìm kiếm"', '2. Gõ "TEST-01", nhấn Enter', '3. Gõ một phần tên KH-TEST, nhấn Enter', '4. Gõ một phần mã KH-TEST, nhấn Enter'], '',
      ['Bước 1, 2: còn HD-TEST-01 (tìm gần đúng)', 'Bước 3, 4: còn các hợp đồng của KH-TEST',
       'Số liệu của từng hợp đồng giống khi không tìm (cả hợp đồng, không bị cắt bớt chứng từ)']),
    C('Gõ tìm nhanh chưa nhấn Enter rồi đổi ô lọc khác', 'P2', 'Đã chọn Thời gian tháng này.', ['1. Gõ từ khóa, không nhấn Enter / Tìm kiếm', '2. Đổi ô Số dư cuối kỳ'], '',
      ['Bước 1: bảng chưa đổi', 'Bước 2: bảng tải lại có áp cả từ khóa đã gõ']),
] + tk_chung(M) + [
    C('Lọc Số dư cuối kỳ', 'P0', 'Trong kỳ có hợp đồng dư nợ, dư có và bằng 0.',
      ['1. Chọn "Dư nợ"', '2. Chọn "Dư có"', '3. Chọn "Tất cả"', '4. Xóa ô (để trống)'], '',
      ['Bước 1: mọi dòng hợp đồng có Số dư cuối kỳ lớn hơn 0', 'Bước 2: mọi dòng có Số dư cuối kỳ âm',
       'Bước 3, 4: đủ mọi hợp đồng, kể cả hợp đồng Số dư cuối kỳ trống (bằng 0)',
       'Dòng Tổng cộng: các cột phát sinh đổi theo lựa chọn; Số dư đầu kỳ KHÔNG đổi (ghi nhận theo thiết kế)']),
    C('Lọc Ngày nghiệm thu', 'P1', 'HD-TEST-01 có Ngày nghiệm thu 15/10/2026.', ['1. Chọn Ngày nghiệm thu 15/10/2026', '2. Chọn 16/10/2026'], '',
      ['Bước 1: có HD-TEST-01, mọi dòng có Ngày nghiệm thu 15/10/2026', 'Bước 2: không có HD-TEST-01 (lọc đúng bằng ngày)']),
    C('Lọc Nhân viên chọn nhiều', 'P0', 'Tài khoản TK-TCT.', ['1. Ô Nhân viên chọn A', '2. Chọn thêm B'], '',
      ['Bước 1: chỉ dòng nhân viên A', 'Bước 2: dòng A và dòng B',
       'Lọc theo NGƯỜI TẠO hợp đồng (hợp đồng do người khác tạo cho khách của A không hiện dưới A)']),
    C('Lọc Công ty / Phòng ban / Bộ phận', 'P1', 'Tài khoản TK-TCT.', ['1. Chọn Công ty CT1', '2. Chọn Phòng ban P1', '3. Chọn Bộ phận BP1'], '',
      ['Mỗi bước bảng tự tải lại, chỉ còn công nợ ghi ở đơn vị đã chọn',
       'Ô Phòng ban / Bộ phận / Nhân viên thu hẹp danh sách theo ô phía trước',
       'Bấm icon ổ khóa cạnh nhãn: danh sách hiện thêm đơn vị đã khóa']),
    C('Kết hợp nhiều ô lọc', 'P1', 'Tài khoản TK-TCT.', ['1. Thời gian tháng này + Nhân viên A + Số dư cuối kỳ "Dư nợ" + Khách hàng KH-TEST'], '',
      ['Chỉ còn hợp đồng của A, khách KH-TEST, đang dư nợ', 'Chân bảng tính lại theo số dòng hợp đồng còn lại, bảng về trang 1']),
    C('Tổng số và phân trang sau khi lọc', 'P1', NHIEU,
      ['1. Đăng nhập TK-TCT, chọn Thời gian 01/10/2026 - 31/10/2026, ghi N ở chân bảng', '2. Chọn Số dư cuối kỳ = "Dư có"', '3. Đọc chân bảng, chuyển trang'], '',
      ['Chân bảng hiện "Hiển thị 1–… / M dòng hợp đồng" với M nhỏ hơn N, bằng số dòng hợp đồng dư có',
       'Số trang tính lại theo M; chuyển trang chỉ trong tập đã lọc']),
    C('Làm mới', 'P0', 'Đã chọn nhiều ô lọc.', ['1. Bấm "Làm mới"'], '',
      ['Mọi ô (kể cả Thời gian, ô tìm nhanh) về trống', 'Bảng ghi "' + LN + '"']),
    C('Đổi bộ lọc liên tiếp nhanh', 'P2', 'Đã chọn Thời gian tháng này.', ['1. Đổi Số dư cuối kỳ Dư nợ > Dư có > Tất cả liên tục trong 2 giây'], '',
      ['Bảng cuối cùng khớp lựa chọn cuối (Tất cả), không hiện số của lần lọc cũ']),
    C('Ẩn / hiện khu vực bộ lọc', 'P2', 'Đang mở màn.', ['1. Bấm "Ẩn tìm kiếm nâng cao"', '2. Bấm "Tìm kiếm nâng cao"'], '',
      ['Bước 1: các ô lọc thu gọn, còn ô tìm nhanh và nút; nút đổi chữ thành "Tìm kiếm nâng cao"', 'Bước 2: các ô lọc hiện lại']),
    C('Cài đặt bộ lọc', 'P2', 'Đang mở màn.', ['1. Bấm "Cài đặt bộ lọc"', '2. Bỏ tích "Ngày nghiệm thu", kéo "Số hợp đồng" lên đầu, bấm "Lưu"', '3. Mở lại, bấm "Khôi phục mặc định", "Lưu"'], '',
      ['Cửa sổ "Cài đặt bộ lọc" có 6 dòng: Thời gian, Khách hàng, Số hợp đồng, Số dư cuối kỳ, Ngày nghiệm thu, Công ty / Phòng ban / Bộ phận / Nhân viên',
       'Bước 2: ô Ngày nghiệm thu ẩn, ô Số hợp đồng lên đầu',
       'Bước 3: về như ban đầu']),
] + luu_chung(M)

# ================================================================== III. SỐ LIỆU BÁO CÁO
G3 = [
    C('Dòng nhân viên bằng tổng các hợp đồng', 'P0', 'Nhân viên A có 3 hợp đồng trên cùng 1 trang.', ['1. Cộng tay từng cột của 3 dòng hợp đồng', '2. So với dòng nhân viên A'], '',
      ['Mọi cột tiền của dòng A bằng tổng 3 dòng hợp đồng', 'Ví dụ đã đối chiếu trên môi trường thử: 27,940,000 + 7,528,680 + 25,229,820 = 60,698,500 (Số dư đầu kỳ)']),
    C('Dòng nhân viên tính cả hợp đồng ở trang sau', 'P0', 'Nhân viên A có 15 hợp đồng (10 dòng/trang).', ['1. Ghi số dòng A ở trang 1', '2. Sang trang 2', '3. Đổi 50 dòng/trang'], '',
      ['Trang 2 vẫn có dòng A, STT nối tiếp (1.11…), số của dòng A GIỐNG trang 1',
       'Bước 3: dòng A không đổi; bằng tổng đủ 15 hợp đồng']),
    C('Dòng Tổng cộng không đổi khi chuyển trang', 'P0', 'Có nhiều trang.', ['1. Ghi dòng Tổng cộng trang 1', '2. Sang trang cuối, đổi số dòng/trang'], '',
      ['Dòng Tổng cộng giữ nguyên mọi cột']),
    C('Tổng cộng các cột phát sinh', 'P0', 'Lọc 1 nhân viên A, Số dư cuối kỳ = Tất cả, 50 dòng/trang.', ['1. Cộng tay cột Hàng hóa/Dịch vụ, Đã thanh toán, Trả lại tiền thừa của mọi dòng hợp đồng'], '',
      ['Bằng số ở dòng Tổng cộng của cột tương ứng']),
    C('Tổng cộng Số dư đầu kỳ / cuối kỳ', 'P0', 'Lọc 1 nhân viên A.', ['1. Lọc Số dư cuối kỳ = Tất cả, ghi Số dư đầu kỳ dòng Tổng cộng (X)', '2. Chọn "Dư nợ"', '3. Kiểm Số dư cuối kỳ dòng Tổng cộng'], '',
      ['Bước 1: X bằng Số dư đầu kỳ dòng A',
       'Bước 2: Số dư đầu kỳ dòng Tổng cộng vẫn là X; có thể khác dòng A (dòng A chỉ cộng hợp đồng dư nợ) - ghi nhận theo thiết kế',
       'Bước 3: Số dư cuối kỳ Tổng cộng = Số dư đầu kỳ Tổng cộng + Cộng tăng - Cộng giảm + Trả lại tiền thừa (ví dụ đã đối chiếu: 60,624,980 + 7,767,360 - 10,000,000 = 58,392,340)']),
    C('Cột Cộng tăng / Cộng giảm', 'P0', 'Có dòng có đủ các cột.', ['1. Kiểm 1 dòng hợp đồng và dòng Tổng cộng'], '',
      ['Cộng (tăng) = Hàng hóa/Dịch vụ + Điều chỉnh công nợ (nhóm tăng)', 'Cộng (giảm) = Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ (nhóm giảm)']),
    C('Cột Số dư cuối kỳ', 'P0', 'Đã chọn Thời gian, có dữ liệu.', ['1. Kiểm 3 dòng hợp đồng bất kỳ'], '',
      ['Số dư cuối kỳ = Số dư đầu kỳ + Cộng (tăng) - Cộng (giảm) + Trả lại tiền thừa',
       'Ví dụ đã đối chiếu: 27,940,000 - 10,000,000 = 17,940,000']),
    C('Định dạng số', 'P1', 'Đã chọn Thời gian, có dữ liệu.', ['1. Quan sát các cột tiền'], '',
      ['Dạng 1,234,567, không có số lẻ', 'Số âm có dấu "-" (ví dụ -520,344)',
       'Số 0 để trống ở dòng nhân viên / hợp đồng; dòng Tổng cộng in "0"']),
    C('Hợp đồng toàn số 0 vẫn hiện', 'P2', 'Hợp đồng đã tất toán trước kỳ.', ['1. Lọc Số dư cuối kỳ = Tất cả, nhập số hợp đồng đó'], '',
      ['Vẫn có 1 dòng, mọi cột tiền trống', 'Chọn "Dư nợ" / "Dư có" thì dòng này không hiện']),
    C('Chứng từ không gắn hợp đồng', 'P2', 'Có phiếu báo có của khách, chưa gắn hợp đồng, người lập là nhân viên A.', ['1. Lọc theo khách đó'], '',
      ['Dưới dòng A có 1 dòng ô Đơn hàng/hợp đồng TRỐNG (không in "-")']),
    C('Hợp đồng có chứng từ của 2 khách', 'P2', 'Một hợp đồng có bút toán của 2 khách hàng.', ['1. Lọc theo số hợp đồng đó'], '',
      ['Ghi nhận: 1 dòng duy nhất, cột Khách hàng hiện 1 trong 2 khách']),
    C('Ngày nghiệm thu - hợp đồng không cần lắp đặt', 'P0', 'HD-TEST-01 (không lắp đặt) có 2 phiếu xuất kho bán hàng duyệt ngày 05/10 và 20/10/2026 (có sẵn).', ['1. Lọc theo HD-TEST-01'], '',
      ['Ngày nghiệm thu = 20/10/2026 (ngày muộn nhất)']),
    C('Ngày nghiệm thu - hợp đồng cần lắp đặt', 'P0', 'Hợp đồng hãng HD-LD (cần lắp đặt) đã xuất hàng 01/10, biên bản nghiệm thu ngày 10/10/2026 (có sẵn).', ['1. Lọc theo HD-LD'], '',
      ['Ngày nghiệm thu = 10/10/2026 (theo biên bản, không theo ngày xuất kho)', 'Chưa có biên bản: ô trống']),
    C('Ngày nghiệm thu - xuất bán hàng mượn / hạch toán dịch vụ', 'P1', 'HD-TEST-02 có phiếu xuất bán hàng mượn lập hôm nay.', ['1. Vào ' + XBM + ', lập phiếu xuất bán hàng mượn cho HD-TEST-02', '2. Lọc lại báo cáo'], '',
      ['Ngày nghiệm thu HD-TEST-02 = hôm nay (nếu là ngày muộn nhất)', 'Số ngày nợ = 0']),
    C('Ngày nghiệm thu dự phòng từ công nợ đầu kỳ quá hạn', 'P2', 'Hợp đồng cũ chỉ có khai báo đầu kỳ công nợ đánh dấu quá hạn, ngày bàn giao nghiệm thu 01/03/2026.', ['1. Lọc theo hợp đồng đó'], '',
      ['Ngày nghiệm thu = 01/03/2026']),
    C('Công thức Số ngày nợ', 'P0', 'Hợp đồng còn dư nợ, Ngày nghiệm thu cách hôm nay 30 ngày.', ['1. Đọc Số ngày nợ (Ngày)', '2. Đổi Đến ngày về tháng trước'], '',
      ['Bước 1: 24 (30 - 6)', 'Bước 2: Số ngày nợ không đổi theo Đến ngày (tính tới hôm nay) nếu hợp đồng vẫn dư nợ',
       'Ví dụ đã đối chiếu: nghiệm thu 07/09/2026, xem ngày 02/11/2026 ra 50']),
    C('Số ngày nợ - chưa quá 6 ngày / hết nợ', 'P1', 'HD1 dư nợ, nghiệm thu 3 ngày trước; HD2 Số dư cuối kỳ bằng 0 hoặc âm.', ['1. Đọc Số ngày nợ của HD1, HD2'], '',
      ['HD1: 0 (không hiện số âm)', 'HD2: trống, Ngày nghiệm thu vẫn hiện']),
    # --- lập chứng từ rồi kiểm số tăng / giảm
    C('Ghi số nền trước khi lập chứng từ', 'P0', 'Đã có KH-TEST, HD-TEST-01 (xem mục 9).', ['1. Mở báo cáo, lọc: ' + LOC, '2. Chụp ' + NOI], 'KH-TEST, HD-TEST-01',
      ['Có đủ số liệu các cột làm số nền cho các case sau (khách mới thì mọi ô trống)']),
    C('Xuất bán hàng làm tăng Hàng hóa/Dịch vụ', 'P0', NEN,
      ['1. Vào ' + YCXH + ', lập và duyệt yêu cầu xuất hàng HD-TEST-01 giá trị 10,000,000',
       '2. Kho lập và duyệt phiếu xuất kho (có sẵn quy trình)', '3. Vào ' + PXH + ', lập phiếu xuất hàng, hạch toán hôm nay', '4. Lọc lại báo cáo'],
      'Giá trị: 10,000,000',
      ['Hàng hóa/Dịch vụ +10,000,000; Cộng (tăng) +10,000,000; Số dư cuối kỳ +10,000,000 ở ' + NOI,
       'Ngày nghiệm thu HD-TEST-01 = ngày duyệt phiếu xuất kho; Số ngày nợ = 0']),
    C('Phiếu thu làm tăng Đã thanh toán', 'P0', NEN,
      ['1. Vào ' + PT_ + ', lập phiếu thu của KH-TEST cho HD-TEST-01, 4,000,000, duyệt và hạch toán hôm nay', '2. Lọc lại báo cáo'], 'Số tiền: 4,000,000',
      ['Đã thanh toán +4,000,000; Cộng (giảm) +4,000,000; Số dư cuối kỳ -4,000,000 ở ' + NOI]),
    C('Phiếu báo có làm tăng Đã thanh toán', 'P1', NEN,
      ['1. Vào ' + PBC + ', lập phiếu báo có của KH-TEST cho HD-TEST-01, 1,000,000, hạch toán hôm nay', '2. Lọc lại báo cáo'], 'Số tiền: 1,000,000',
      ['Đã thanh toán +1,000,000; Số dư cuối kỳ -1,000,000']),
    C('Điều chỉnh công nợ TĂNG', 'P0', NEN,
      ['1. Vào ' + YCDC + ', lập yêu cầu điều chỉnh TĂNG công nợ KH-TEST, HD-TEST-01, 2,000,000, gửi duyệt và duyệt',
       '2. Lọc lại báo cáo', '3. Vào ' + PKT + ', lập phiếu kế toán từ yêu cầu, hạch toán hôm nay', '4. Lọc lại báo cáo'], 'Số tiền: 2,000,000',
      ['Bước 2: chưa đổi', 'Bước 4: Điều chỉnh công nợ (nhóm tăng) +2,000,000; Cộng (tăng) +2,000,000; Số dư cuối kỳ +2,000,000']),
    C('Điều chỉnh công nợ GIẢM', 'P0', NEN,
      ['1. Làm như case Điều chỉnh công nợ TĂNG nhưng loại điều chỉnh GIẢM, 500,000', '2. Lọc lại báo cáo'], 'Số tiền: 500,000',
      ['Điều chỉnh công nợ (nhóm giảm) +500,000; Cộng (giảm) +500,000; Số dư cuối kỳ -500,000']),
    C('Khách trả lại hàng', 'P0', 'HD-TEST-01 đã xuất hàng ở case Xuất bán hàng. ' + NEN,
      ['1. Vào ' + YCNH + ', lập yêu cầu nhập hàng khách trả lại theo HD-TEST-01, 3,000,000, duyệt',
       '2. Lập, duyệt đề nghị nhập kho và phiếu nhập kho', '3. Vào ' + PNH + ', lập phiếu nhập hàng, hạch toán hôm nay', '4. Lọc lại báo cáo'], 'Số tiền: 3,000,000',
      ['Nhập trả lại +3,000,000; Cộng (giảm) +3,000,000; Số dư cuối kỳ -3,000,000', 'Trước bước 3 báo cáo chưa đổi']),
    C('Phiếu chi trả lại tiền thừa', 'P1', NEN,
      ['1. Vào ' + PC + ', lập phiếu chi trả KH-TEST cho HD-TEST-01, 200,000, hạch toán hôm nay', '2. Lọc lại báo cáo'], 'Số tiền: 200,000',
      ['Trả lại tiền thừa +200,000; Số dư cuối kỳ TĂNG 200,000; nhóm Phát sinh giảm không đổi']),
    C('Phiếu ủy nhiệm chi trả lại tiền thừa', 'P2', NEN,
      ['1. Vào ' + UNC + ', lập ủy nhiệm chi trả KH-TEST cho HD-TEST-01, 300,000, hạch toán hôm nay', '2. Lọc lại báo cáo'], 'Số tiền: 300,000',
      ['Trả lại tiền thừa +300,000 (lũy kế 500,000); Số dư cuối kỳ tăng 300,000']),
    C('Hạch toán dịch vụ làm tăng Hàng hóa/Dịch vụ', 'P2', 'KH-TEST có hợp đồng dịch vụ HD-TEST-DV do nhân viên A lập (có sẵn).',
      ['1. Vào ' + HTDV + ', lập và duyệt phiếu hạch toán dịch vụ 1,500,000 cho HD-TEST-DV', '2. Lọc lại báo cáo'], 'Số tiền: 1,500,000',
      ['Có / tăng dòng HD-TEST-DV dưới nhân viên A, Hàng hóa/Dịch vụ +1,500,000', 'Ngày nghiệm thu HD-TEST-DV = ngày của phiếu hạch toán']),
    C('Chứng từ trước Từ ngày vào Số dư đầu kỳ', 'P0', 'Phiếu thu 700,000 cho HD-TEST-01 hạch toán ngày cuối tháng trước.',
      ['1. Lọc Thời gian tháng này', '2. Đổi Từ ngày về ngày 1 tháng trước'], 'Số tiền: 700,000',
      ['Bước 1: phiếu không ở cột Đã thanh toán mà làm Số dư đầu kỳ giảm 700,000',
       'Bước 2: phiếu chuyển sang Đã thanh toán; Số dư cuối kỳ không đổi giữa 2 lần lọc']),
    C('Chứng từ sau Đến ngày không tính', 'P1', 'Phiếu thu cho HD-TEST-01 hạch toán hôm nay.', ['1. Lọc Đến ngày = hôm qua', '2. Lọc Đến ngày = hôm nay'], '',
      ['Bước 1: phiếu không được tính ở cột nào', 'Bước 2: phiếu vào Đã thanh toán']),
    C('Thu vượt chuyển sang Dư có', 'P1', 'HD-TEST-01 đang dư nợ 4,000,000.',
      ['1. Lập phiếu thu 5,000,000 cho HD-TEST-01, hạch toán hôm nay', '2. Lọc Số dư cuối kỳ = Dư nợ', '3. Lọc Dư có'], '',
      ['Số dư cuối kỳ HD-TEST-01 = -1,000,000; Số ngày nợ trống', 'Bước 2: không có HD-TEST-01', 'Bước 3: có HD-TEST-01']),
    C('Hợp đồng mới hiện dưới đúng nhân viên tạo', 'P1', 'HD-TEST-02 do A tạo chưa có phát sinh.',
      ['1. Xuất hàng 6,000,000 cho HD-TEST-02 như case Xuất bán hàng', '2. Lọc lại báo cáo'], '',
      ['HD-TEST-02 hiện dưới dòng nhân viên A, Hàng hóa/Dịch vụ 6,000,000', 'Dòng A tăng 6,000,000 ở Số dư cuối kỳ']),
]

# ================================================================== IV. XUẤT DANH SÁCH EXCEL
G4 = [
    C('Xuất Excel khi chưa chọn Thời gian', 'P0', 'Mới mở màn.', ['1. Bấm "Xuất Excel"', '2. Bấm "Xuất Excel mẫu in"'], '',
      ['Cả 2: thông báo "Vui lòng chọn thời gian", chữ đỏ dưới ô Thời gian, không mở cửa sổ, không tải file']),
    C('Mở cửa sổ chọn trường xuất Excel', 'P0', 'Đã chọn Thời gian.', ['1. Bấm "Xuất Excel"'], '',
      ['Cửa sổ "Chọn trường xuất Excel", dòng "Tích chọn trường cần xuất, kéo biểu tượng ba gạch để đổi thứ tự cột trong file."',
       '14 trường đều được tích: Nhân viên / Đơn hàng - hợp đồng, Khách hàng, Số dư đầu kỳ, PS tăng - Hàng hóa/Dịch vụ, PS tăng - Điều chỉnh công nợ, PS tăng - Cộng, PS giảm - Nhập trả lại, PS giảm - Đã thanh toán, PS giảm - Điều chỉnh công nợ, PS giảm - Cộng, Trả lại tiền thừa, Số dư cuối kỳ, Ngày nghiệm thu, Số ngày nợ (Ngày)',
       'Có "Chọn tất cả", "Bỏ chọn hết", "Đang chọn 14/14 trường", "Xuất file", "Đóng"']),
    C('Nội dung file khớp màn hình', 'P0', 'Lọc 1 nhân viên A (nhiều trang).', ['1. Bấm "Xuất Excel" > "Xuất file"', '2. Mở file'], '',
      ['Thông báo "Xuất Excel thành công", file bao_cao_tong_hop_cong_no_khach_hang_theo_nhan_vien.xlsx',
       'Dòng 1 "BÁO CÁO TỔNG HỢP CÔNG NỢ KHÁCH HÀNG THEO NHÂN VIÊN", dòng 2 "Thời gian: dd/mm/yyyy - dd/mm/yyyy", tiêu đề 2 tầng',
       'Dòng Tổng cộng, dòng nhân viên (đậm), dòng hợp đồng; có ĐỦ hợp đồng của mọi trang',
       'Số từng dòng bằng số trên màn; số dạng 1,234,567']),
    C('Đổi thứ tự / bỏ bớt trường', 'P1', 'Đang mở cửa sổ chọn trường.', ['1. Bỏ tích Khách hàng, kéo Số dư cuối kỳ lên đầu', '2. Xuất file'], '',
      ['File không có cột Khách hàng; cột STT đứng đầu, ngay sau là Số dư cuối kỳ']),
    C('Xuất theo đúng bộ lọc đang áp dụng', 'P0', 'Đã chọn Thời gian tháng này; có hợp đồng dư nợ và dư có.',
      ['1. Chọn Số dư cuối kỳ = "Dư nợ", Nhân viên A', '2. Bấm "Xuất Excel" > "Xuất file", mở file'], '',
      ['File chỉ có dòng nhân viên A và các hợp đồng dư nợ của A như trên màn', 'Dòng Tổng cộng trong file bằng dòng Tổng cộng trên màn']),
] + xl_chung(M) + [
    C('Xuất Excel mẫu in', 'P0', 'Lọc 1 nhân viên A.', ['1. Bấm "Xuất Excel mẫu in"', '2. Mở file'], '',
      ['Tải ngay (không có cửa sổ chọn trường), "Xuất Excel thành công", file bao_cao_tong_hop_cong_no_khach_hang_theo_nhan_vien_mau_in.xlsx',
       'Cột: STT, Đơn hàng/Hợp đồng, Khách hàng, Số dư đầu kỳ, Giá trị hợp đồng thực tế, Giá trị đã thanh toán, Giá trị còn nợ cuối kỳ, Ngày nghiệm thu, Ngày xuất hóa đơn, Số ngày nợ (Ngày), Giải trình lý do chưa thu nợ, Kế hoạch ngày thu hồi công nợ, Xác nhận công nợ (Đã có / Chưa có / Lý do chưa xác nhận nợ)',
       'Ngày xuất hóa đơn và các cột giải trình / kế hoạch / xác nhận để trống']),
    C('Công thức các cột mẫu in', 'P0', 'Đã có file mẫu in, màn đang lọc như lúc xuất.', ['1. So 1 dòng hợp đồng giữa file và màn'], '',
      ['Giá trị hợp đồng thực tế = Cộng (tăng) trên màn', 'Giá trị đã thanh toán = Cộng (giảm) trên màn',
       'Giá trị còn nợ cuối kỳ = Số dư cuối kỳ trên màn (đã gồm Trả lại tiền thừa)']),
    C('Xuất Excel mẫu in theo bộ lọc, mọi trang', 'P1', NHIEU,
      ['1. Đăng nhập TK-TCT, chọn Thời gian 01/10/2026 - 31/10/2026, Nhân viên A, đứng ở trang 1', '2. Bấm "Xuất Excel mẫu in", mở file'], '',
      ['File có đủ mọi hợp đồng của A (mọi trang), không chỉ trang đang xem', 'Không có nhân viên khác ngoài A']),
    C('Xuất Excel khi chỉ lọc Thời gian (dữ liệu lớn)', 'P1', 'TK-TCT, Thời gian 1 tháng, không lọc khác.', ['1. Bấm "Xuất Excel" > "Xuất file", bấm giờ', '2. Bấm "Xuất Excel mẫu in"'], '',
      ['Tải được file đủ mọi dòng trong 60 giây, không báo lỗi',
       'Ghi chú: đo trên môi trường thử 02/11/2026 KHÔNG tải được (báo lỗi sau khoảng 8 giây) - ghi kết quả thực tế vào cột Ghi chú']),
]

# ================================================================== V. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
G5 = [
    C('Phiếu chưa hạch toán không làm đổi số', 'P0', NEN,
      ['1. Vào ' + YCXH + ', lập yêu cầu xuất hàng 5,000,000 cho HD-TEST-01, CHƯA xuất kho',
       '2. Vào ' + PT_ + ', lập phiếu thu 1,000,000 cho HD-TEST-01, để chưa duyệt / chưa hạch toán', '3. Lọc lại báo cáo'], '',
      ['Không cột nào đổi so với số nền']),
    C('Kiểm tổng sau chuỗi phiếu', 'P0', 'Đã chạy lần lượt các case lập chứng từ (xuất hàng, thu, báo có, điều chỉnh tăng / giảm, trả lại hàng, phiếu chi, ủy nhiệm chi).',
      ['1. Lọc lại báo cáo', '2. So Số dư cuối kỳ HD-TEST-01 với số nền'], '',
      ['Chênh = +10,000,000 - 4,000,000 - 1,000,000 + 2,000,000 - 500,000 - 3,000,000 + 200,000 + 300,000 = +4,000,000',
       'Dòng nhân viên A và dòng Tổng cộng cũng chênh đúng +4,000,000']),
    C('Hủy hạch toán thì số trả về', 'P1', 'Phiếu thu 4,000,000 cho HD-TEST-01 đã hạch toán và đang hiện trên báo cáo.', ['1. Kế toán hủy hạch toán (hoặc hủy) phiếu thu đó', '2. Lọc lại báo cáo'], '',
      ['Đã thanh toán giảm lại 4,000,000; Số dư cuối kỳ tăng lại 4,000,000']),
    C('Bấm số hợp đồng mở đúng hợp đồng', 'P1', 'Đã chọn Thời gian, có dữ liệu.', ['1. Bấm số hợp đồng ở dòng hợp đồng'], '',
      ['Mở trang xem hợp đồng ở tab mới, đúng hợp đồng', 'Màn báo cáo giữ nguyên bộ lọc, trang đang xem']),
    C('Khớp với Báo cáo chi tiết công nợ khách hàng', 'P1', 'HD-TEST-01 có phát sinh trong kỳ; cùng một tài khoản xem.',
      ['1. Lọc cùng Thời gian, cùng KH-TEST ở màn này và màn Bán hàng > Báo cáo > Báo cáo công nợ > "Chi tiết công nợ KH"', '2. So các cột của HD-TEST-01'], '',
      ['Số dư đầu kỳ, các cột phát sinh, Trả lại tiền thừa, Số dư cuối kỳ của HD-TEST-01 bằng nhau ở 2 màn',
       'Số dư cuối kỳ dòng Tổng cộng bằng nhau ở 2 màn (cùng phạm vi quyền); lệch thì ghi số của từng màn vào Ghi chú']),
    C('Khách hàng mới tạo có ngay ở ô chọn Khách hàng', 'P1', 'Vừa tạo khách hàng KH-MOI ở màn danh mục khách hàng.',
      ['1. Mở màn báo cáo', '2. Gõ 2 ký tự đầu mã KH-MOI vào ô Khách hàng'], 'Khách hàng: KH-MOI',
      ['KH-MOI có trong danh sách gợi ý, chọn được']),
    C('Đổi tên khách hàng thì báo cáo hiện tên mới', 'P2', 'KH-TEST có phát sinh trong kỳ.',
      ['1. Sửa tên KH-TEST ở màn danh mục khách hàng', '2. Mở báo cáo, lọc KH-TEST', '3. Xuất Excel'], '',
      ['Cột Khách hàng trên màn và trong file hiện tên mới', 'Số liệu không đổi']),
    C('Không có hợp đồng bị lặp', 'P1', 'Đã chọn Thời gian tháng này.',
      ['1. Lọc 1 nhân viên A, đặt 100 dòng/trang', '2. Rà cột Đơn hàng/hợp đồng'], '',
      ['Mỗi hợp đồng chỉ có 1 dòng dưới đúng 1 nhân viên']),
]

# ================================================================== VI. PHÂN QUYỀN
G6 = [
    C('Không có quyền: chỉ thấy hợp đồng mình tạo', 'P0', 'TK-A không có 4 quyền xem; A tạo HD-TEST-01, HD-TEST-02 có công nợ; B có hợp đồng khác.',
      ['1. Đăng nhập TK-A, ' + MENU[0].lower() + MENU[1:], '2. Chọn Thời gian tháng này', '3. Quan sát bộ lọc và bảng'], 'Tài khoản: TK-A',
      ['Mở được màn, không báo thiếu quyền',
       'Không có ô Công ty, Phòng ban, Bộ phận, Nhân viên',
       'Chỉ có 1 dòng nhân viên A với các hợp đồng do A tạo; không có hợp đồng của B',
       'Số dư đầu kỳ dòng Tổng cộng chỉ tính chứng từ của hợp đồng A tạo (không phải số của toàn hệ thống)']),
    C('Quyền bộ phận: bộ phận quản lý và bộ phận đang thuộc', 'P0', 'TK-BP có quyền "' + Q + 'bộ phận", đang thuộc BP1, quản lý BP2.',
      ['1. Đăng nhập TK-BP, mở màn, chọn Thời gian tháng này', '2. Quan sát ô lọc và các dòng nhân viên'], 'Tài khoản: TK-BP',
      ['Có ô Bộ phận, Nhân viên; không có ô Công ty, Phòng ban',
       'Có công nợ ghi ở BP1 và BP2, cộng hợp đồng do TK-BP tạo', 'Không có công nợ của bộ phận khác']),
    C('Quyền phòng ban: phòng quản lý và phòng đang thuộc', 'P0', 'TK-PB có quyền "' + Q + 'phòng ban", đang thuộc P1, quản lý P2.',
      ['1. Đăng nhập TK-PB, mở màn, chọn Thời gian tháng này'], 'Tài khoản: TK-PB',
      ['Có ô Phòng ban, Bộ phận, Nhân viên; không có ô Công ty',
       'Có công nợ của P1 và P2, cộng hợp đồng do TK-PB tạo; không có phòng khác']),
    C('Quyền công ty: công ty đang làm việc', 'P0', 'TK-CT có quyền "' + Q + 'công ty", đang làm việc ở CT1.',
      ['1. Đăng nhập TK-CT, mở màn, chọn Thời gian tháng này', '2. Đổi công ty đang làm việc sang CT2 (nếu tài khoản có), mở lại màn'], 'Tài khoản: TK-CT',
      ['Bước 1: có ô Phòng ban, Bộ phận, Nhân viên; chỉ công nợ ghi ở CT1 (cộng hợp đồng mình tạo); không có nhân viên C',
       'Bước 2: số liệu đổi theo CT2 nếu tài khoản có quyền ở CT2; không có quyền ở CT2 thì chỉ còn hợp đồng mình tạo']),
    C('Quyền tổng công ty: mọi công ty', 'P0', 'TK-TCT có quyền "' + Q + 'tổng công ty".',
      ['1. Đăng nhập TK-TCT, mở màn, chọn Thời gian tháng này'], 'Tài khoản: TK-TCT',
      ['Có đủ 4 ô Công ty, Phòng ban, Bộ phận, Nhân viên', 'Có nhân viên của cả CT1 và CT2']),
    C('Có nhiều quyền: lấy cấp rộng nhất', 'P1', 'Một tài khoản có đồng thời quyền "bộ phận" và quyền "công ty".',
      ['1. Đăng nhập, mở màn, chọn Thời gian tháng này'], '',
      ['Phạm vi và ô lọc giống quyền "công ty", không bị thu hẹp về bộ phận']),
    C('Hợp đồng mình tạo luôn thấy dù ngoài phạm vi', 'P1', 'TK-BP (quyền bộ phận BP1, BP2) tự tạo một hợp đồng mà bút toán ghi ở bộ phận BP3.',
      ['1. Đăng nhập TK-BP, lọc tháng này, nhập số hợp đồng đó vào ô Số hợp đồng, nhấn Enter'], '',
      ['Hợp đồng vẫn hiện dưới dòng nhân viên TK-BP']),
    C('Xuất Excel theo phạm vi quyền', 'P1', 'Tài khoản TK-BP.',
      ['1. Lọc tháng này, bấm "Xuất Excel" > "Xuất file"', '2. Bấm "Xuất Excel mẫu in"', '3. Mở 2 file'], '',
      ['Cả 2 file chỉ có nhân viên / hợp đồng giống trên màn của TK-BP (BP1, BP2 và hợp đồng mình tạo)',
       'Dòng Tổng cộng trong file bằng dòng Tổng cộng trên màn']),
] + pq_chung(M)

GROUPS = [
    ('HIỂN THỊ TRANG & TRUY CẬP', G1),
    ('TÌM KIẾM & LỌC DANH SÁCH', G2),
    ('SỐ LIỆU BÁO CÁO', G3),
    ('XUẤT DANH SÁCH EXCEL', G4),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', G5),
    ('PHÂN QUYỀN', G6),
]

if __name__ == '__main__':
    build_chuan(OUT, 'Trang tính1', TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, sections(GROUPS), loai='bao_cao')
    print(dem(GROUPS))

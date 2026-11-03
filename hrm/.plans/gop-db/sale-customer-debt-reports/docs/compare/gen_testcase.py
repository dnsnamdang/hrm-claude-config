# -*- coding: utf-8 -*-
"""Testcase "Bảng đối chiếu công nợ 1 khách hàng" — KHUÔN CHUẨN tab "13. DM quốc gia" (loại bao_cao, 03/11/2026).

Viết lại từ gen_testcase_v1.py (bản 02/11 sai khuôn, giữ để tra): giữ mọi case nghiệp vụ, xếp lại theo nhóm chuẩn
(xuat-tai-lieu-chuyen-doi/TC_CHUAN.md), bổ sung case theo checklist "Mẫu tài liệu.xlsx". Case chung (phân trang,
tìm nhanh, lưu bộ lọc, Excel, phân quyền) sinh từ _tc_bc_chung.py.
Chạy: python gen_testcase.py  (tự gọi check_tc — phải 0 lỗi)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(GOPDB, 'xuat-tai-lieu-chuyen-doi'))
from _tc_chuan import build_chuan  # noqa: E402
from _tc_bc_chung import C, sections, dem, pt_chung, tk_chung, luu_chung, xl_chung, pq_chung  # noqa: E402

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

NGAY = '03/11/2026'
TEN = 'Bảng đối chiếu công nợ 1 khách hàng'
MODULE = 'BC đối chiếu công nợ 1 KH'
OUT = os.path.join(HERE, 'testcase - %s.xlsx' % TEN)


def L_(*lines):
    return '\n'.join(lines)


MENU = 'Vào phân hệ Bán hàng > Báo cáo > nhóm Báo cáo công nợ > bấm "Đối chiếu công nợ 1 KH"'
LOC = 'Chọn Thời gian 01/01/2026 - 30/06/2026, Khách hàng KH-TEST'
LN = 'Chọn thời gian và khách hàng để xem bảng đối chiếu.'
Q = 'Xem báo cáo đối soát công nợ khách hàng theo'
BL = 'Đã chọn Thời gian 01/01/2026 - 30/06/2026, Khách hàng CÔNG TY CỔ PHẦN BÁCH LIÊN (môi trường thử).'
MENU_PX = 'Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Xuất hàng > Phiếu xuất hàng'
MENU_PT = 'Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu thu'
MENU_BC = 'Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu báo có'
MENU_PC = 'Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu chi'
MENU_UNC = 'Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu ủy nhiệm chi'
MENU_PKT = 'Tài chính > Sổ tổng hợp > Phiếu kế toán'
MENU_YCDC = 'Bán hàng > Yêu cầu > Công nợ - Thu - Chi > YC điều chỉnh công nợ'
MENU_NH = 'Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Nhập hàng > Phiếu nhập hàng'
MENU_BS = 'Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Mượn hàng > Phiếu xuất bán hàng mượn'
NEN = 'Đã ghi lại số nền của dòng Tổng cộng và dòng HD-TEST-01 (case "Ghi lại số nền trước khi lập chứng từ").'

M = {
    'dv': 'hợp đồng',
    'loc': LOC,
    'nhieu_trang': 'Tài khoản quyền tổng công ty; khách hàng KH-NHIEU có hơn 30 hợp đồng phát sinh trong kỳ 01/01/2026 - 31/10/2026.',
    'doi_loc': 'Nhập một phần số hợp đồng vào ô Số hợp đồng, nhấn Enter',
    'tu_khoa': 'PXH',
    'loi_nhac': LN,
    'man_khac': 'Bán hàng > Báo cáo > Báo cáo công nợ > Tổng hợp công nợ theo NV',
    'excel_file': 'bang_doi_chieu_cong_no_1_khach_hang.xlsx',
    'so_truong': '11',
    'xl_ngay': 'Cột Ngày chứng từ hiển thị dạng dd/mm/yyyy',
    'nhom_quyen': 'Bảng đối chiếu công nợ 1 khách hàng',
    'menu': MENU,
    'nut': 'In, Xuất Excel',
    'url': '<địa chỉ hệ thống>/sale/customer-debt-compare',
    'quyen_rong': Q + ' tổng công ty',
}
M['loc'] = 'Chọn Thời gian 01/01/2026 - 31/10/2026, Khách hàng KH-NHIEU'
PT = pt_chung(M)
M['loc'] = LOC

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
        '-  Hợp đồng có 7 cột phát sinh đều bằng 0 (so phần nguyên): không lên bảng.',
        '-  Bút toán chưa gắn hợp đồng: không thành dòng nhưng VẪN cộng vào dòng Tổng cộng.',
        '-  Chứng từ chưa hạch toán (chưa ghi sổ): không tính.',
        '-  Bút toán có ngày hạch toán sau Đến ngày: không tính.',
        '-  Hợp đồng ngoài phạm vi quyền của người xem.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô Thời gian (bắt buộc) lọc theo NGÀY HẠCH TOÁN của chứng từ, tính cả 2 đầu mút.',
        'Trong kỳ = Từ ngày đến hết Đến ngày; trước Từ ngày = đầu kỳ (chỉ vào Số dư đầu kỳ của dòng Tổng cộng).',
        'Mặc định để trống; mở màn / rời màn rồi quay lại / F5 / Làm mới đều về trống.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Cấp 1: dòng Tổng cộng (1 dòng).',
        'Cấp 2: dòng hợp đồng, xếp theo thứ tự hợp đồng được tạo; phân trang theo hợp đồng (mặc định 10).',
        'Cấp 3: dòng chứng từ trong kỳ của hợp đồng, xếp theo ngày hạch toán, cùng ngày theo thời điểm tạo.',
        'Bảng không có sắp xếp theo cột, không có tùy chỉnh cột.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '-  Mỗi chứng từ gom 1 dòng / hợp đồng (nhiều bút toán của cùng chứng từ cộng lại).',
        '-  Số dư cuối kỳ dòng chứng từ = cộng dồn từ chứng từ đầu của hợp đồng: dòng trên + HH/DV - Nhập trả lại - Đã thanh toán + Trả lại tiền thừa.',
        '-  Số dư cuối kỳ dòng hợp đồng = HH/DV - Nhập trả lại - Đã thanh toán + Trả lại tiền thừa (KHÔNG tính đầu kỳ và 2 cột Điều chỉnh công nợ).',
        '-  Số dư cuối kỳ dòng Tổng cộng = Đầu kỳ + HH/DV + ĐCCN tăng - Nhập trả lại - Đã thanh toán - ĐCCN giảm + Trả lại tiền thừa.',
    )),
    ('7. Phân quyền cấp', L_(
        'Màn không chặn quyền vào; mọi người dùng đăng nhập đều thấy menu và mở được. 4 quyền chỉ mở rộng phạm vi:',
        '-  "%s tổng công ty": mọi công ty; ô lọc Công ty, Phòng ban, Bộ phận, Nhân viên.' % Q,
        '-  "%s công ty": công ty đang làm việc + hợp đồng mình tạo; ô Phòng ban, Bộ phận, Nhân viên.' % Q,
        '-  "%s phòng ban": phòng ban mình quản lý + hợp đồng mình tạo; ô Phòng ban, Bộ phận, Nhân viên.' % Q,
        '-  "%s bộ phận": bộ phận mình quản lý + hợp đồng mình tạo; ô Bộ phận, Nhân viên.' % Q,
        '-  Không quyền: chỉ hợp đồng do mình tạo; không có ô lọc tổ chức.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Hàng hóa/Dịch vụ = Nợ - Có của phiếu xuất hàng, xuất bán hàng mượn, hạch toán dịch vụ, biên bản thanh lý, hạch toán DV BH-SC (+ Nợ của khai báo công nợ đầu kỳ).',
        'Điều chỉnh công nợ tăng / giảm = Nợ / Có của phiếu kế toán điều chỉnh công nợ.',
        'Nhập trả lại = Có - Nợ của phiếu nhập hàng trả lại. Đã thanh toán = Có của phiếu thu, phiếu báo có, khai báo đầu kỳ.',
        'Trả lại tiền thừa = Nợ của phiếu chi, ủy nhiệm chi. Số dư đầu kỳ = Nợ - Có trước Từ ngày (chỉ dòng Tổng cộng).',
        'Chân bảng "Hiển thị a–b / N hợp đồng".',
    )),
    ('9. Ghi chú đọc bảng', L_(
        '-  Số dạng 1,234,567, không phần lẻ; ô bằng 0 để trống, riêng dòng Tổng cộng trên màn in "0".',
        '-  Tổng Số dư cuối kỳ các dòng hợp đồng KHÁC dòng Tổng cộng (do khác công thức) — không phải lỗi.',
        '-  Ô tìm nhanh chỉ thu hẹp danh sách hợp đồng, KHÔNG đổi dòng Tổng cộng; ô Số hợp đồng có đổi dòng Tổng cộng.',
        'Dữ liệu mẫu: KH-TEST = khách hàng có >= 2 hợp đồng bán hàng do NV-A tạo, có phiếu xuất hàng trong kỳ; HD-TEST-01 = 1 hợp đồng của KH-TEST; '
        'KH-NHIEU = khách hàng có hơn 30 hợp đồng phát sinh trong năm.',
        'TK-SA (quyền tổng công ty), TK-CT (quyền công ty A), TK-PB (quyền phòng ban, quản lý phòng P1), TK-BP (quyền bộ phận), '
        'NV-A (không quyền, người tạo HD-TEST-01), NV-B (không quyền, không tạo hợp đồng nào của KH-TEST).',
        'Số liệu mẫu đọc trên môi trường thử 02/11/2026; môi trường khác thì ghi số thật vào cột Ghi chú.',
    )),
]

# ================================================================== I. HIỂN THỊ TRANG & TRUY CẬP
G1 = [
    C('Mở màn hình từ menu', 'P0', 'Tài khoản bất kỳ đã đăng nhập.',
      ['1. Đăng nhập', '2. ' + MENU], '',
      ['Tiêu đề trang và tiêu đề bảng "Bảng đối chiếu công nợ 1 khách hàng", cạnh tiêu đề trang có icon (i)',
       'Bảng hiện "' + LN + '", không tự tải số liệu',
       'Nhóm Báo cáo công nợ có các mục: Đối chiếu công nợ 1 KH, Tổng hợp công nợ theo NV, Chi tiết công nợ KH']),
    C('Bố cục khu vực lọc và các nút chức năng', 'P1', 'Tài khoản TK-SA (quyền tổng công ty).',
      ['1. Mở màn', '2. Quan sát khung "Bộ lọc danh sách" và hàng nút trên bảng'], '',
      ['Ô tìm nhanh, gợi ý "Tìm theo số hợp đồng hoặc số chứng từ"; nút Tìm kiếm, Làm mới, Cài đặt bộ lọc, Ẩn tìm kiếm nâng cao',
       'Hàng 1: Thời gian * (Từ ngày -> Đến ngày), Khách hàng *, Số hợp đồng',
       'Hàng 2: Công ty, Phòng ban, Bộ phận, Nhân viên',
       'Trên bảng: nút In, Xuất Excel (In đứng trước); màn không có nút Thêm / Sửa / Xóa']),
    C('Kiểm tra đủ các cột của bảng', 'P0', 'Đang mở màn.',
      ['1. Đọc tiêu đề bảng từ trái sang phải'], '',
      ['STT | Ngày chứng từ | Số chứng từ | Diễn giải | Số dư đầu kỳ | Phát sinh tăng trong kỳ (Hàng hóa/Dịch vụ, Điều chỉnh công nợ) | '
       'Phát sinh giảm trong kỳ (Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ) | Trả lại tiền thừa | Số dư cuối kỳ',
       'Mỗi tiêu đề có icon (i)',
       'Bảng không có cột ẩn / cột tùy chọn, không có nút cấu hình cột']),
    C('Nội dung icon (i) của tiêu đề cột', 'P2', 'Đang mở màn.',
      ['1. Rê chuột vào icon (i) của cột Số dư cuối kỳ', '2. Rê chuột vào icon (i) của cột Đã thanh toán'], '',
      ['Bước 1: dòng đầu "Công nợ khách hàng còn phải trả đến hết Đến ngày", có 3 dòng công thức cho dòng Tổng cộng, dòng hợp đồng, dòng chứng từ',
       'Bước 2: "Số tiền khách đã thanh toán trong kỳ" - "Đã thanh toán = Tổng ghi Có của phiếu thu, phiếu báo có và khai báo công nợ đầu kỳ."']),
    C('Bảng có số liệu: phân biệt 3 loại dòng', 'P0', 'KH-TEST có ít nhất 2 hợp đồng phát sinh trong kỳ.',
      ['1. ' + LOC], 'Kỳ 01/01/2026 - 30/06/2026',
      ['Dòng đầu "Tổng cộng" (gộp 4 cột đầu, nền xám, có icon (i))',
       'Dòng hợp đồng chữ đậm nền xám nhạt, STT 1, 2…, cột Ngày chứng từ trống',
       'Dòng chứng từ STT 1.1, 1.2…, có Ngày chứng từ',
       'Tiêu đề bảng dính khi cuộn dọc; có thanh cuộn ngang ở cả trên và dưới bảng']),
    C('Khách hàng chưa có phát sinh nào', 'P2', 'Có khách hàng KH-MOI vừa tạo, chưa có chứng từ công nợ nào.',
      ['1. Chọn Thời gian 01/01/2026 - 31/10/2026, Khách hàng KH-MOI'], 'Khách hàng: KH-MOI',
      ['Bảng hiện "Không có dữ liệu phù hợp bộ lọc."', 'Không hiện dòng Tổng cộng, không có chân bảng', 'Màn không báo lỗi, nút In và Xuất Excel vẫn bấm được']),
    C('Hiển thị khi không có dữ liệu khớp', 'P1', 'Đã chọn bộ lọc, bảng có dữ liệu.',
      ['1. ' + LOC, '2. Gõ "ZZZ999" vào ô tìm nhanh, nhấn Enter'], 'Từ khóa: ZZZ999',
      ['Bảng hiện "Không có dữ liệu phù hợp bộ lọc."', 'Không có chân bảng và thanh phân trang']),
    C('Thứ tự mặc định của dòng hợp đồng và dòng chứng từ', 'P1', 'KH-TEST có ít nhất 2 hợp đồng; 1 hợp đồng có ít nhất 2 chứng từ cùng ngày hạch toán.',
      ['1. ' + LOC, '2. Đọc thứ tự các dòng hợp đồng', '3. Đọc thứ tự dòng chứng từ của 1 hợp đồng'], '',
      ['Dòng hợp đồng xếp theo thứ tự hợp đồng được tạo (tạo trước đứng trước)',
       'Dòng chứng từ xếp theo Ngày chứng từ tăng dần; cùng ngày thì chứng từ tạo trước đứng trước (môi trường thử: dòng 2.1 PXH-19849, 2.2 PXH-19852 cùng 04/03/2026)']),
    C('Số thứ tự liên tục qua các trang', 'P0', M['nhieu_trang'],
      ['1. Chọn Thời gian 01/01/2026 - 31/10/2026, Khách hàng KH-NHIEU', '2. Ghi lại STT dòng hợp đồng cuối trang 1', '3. Sang trang 2, đọc STT dòng hợp đồng đầu'], '',
      ['STT dòng hợp đồng nối tiếp liền mạch (trang 1 kết thúc ở 10 thì trang 2 bắt đầu 11), không quay về 1',
       'Chứng từ của 1 hợp đồng không bị cắt sang trang khác',
       'Không có hợp đồng nào 7 cột phát sinh đều trống; trang 1 không trống']),
    C('Dữ liệu trên bảng đúng với chứng từ đã tạo', 'P0', BL,
      ['1. Lọc như Tiền điều kiện', '2. Bấm số phiếu kế toán TPE.PKT0326.00055 ở dòng chứng từ, mở phiếu ở tab mới', '3. So ngày hạch toán, số tiền, ghi chú giữa phiếu và dòng chứng từ'], '',
      ['Ngày chứng từ = ngày hạch toán của phiếu', 'Số tiền ở cột Điều chỉnh công nợ = số tiền ghi trên phiếu cho hợp đồng đó',
       'Diễn giải = ghi chú của dòng chi tiết ứng với hợp đồng trên phiếu']),
] + PT + [
    C('Thời gian mở màn khi chưa lọc', 'P1', 'Tài khoản bất kỳ đã đăng nhập.',
      ['1. ' + MENU + ', đo thời gian tới khi màn hiện đủ'], '',
      ['Dưới 3 giây; bảng hiện lời nhắc, không tải số liệu (báo cáo bắt buộc chọn khách hàng + thời gian)']),
    C('Thời gian tải 1 khách hàng kỳ 6 tháng', 'P1', BL + ' Khách hàng có 10 hợp đồng.',
      ['1. Chọn đủ bộ lọc, đo thời gian từ lúc chọn khách tới khi bảng có dòng'], '',
      ['Dưới 2 giây (môi trường thử 02/11/2026: khoảng 0,3–0,6 giây)']),
    C('Thời gian tải khách hàng nhiều hợp đồng, 100 hợp đồng / trang', 'P2', 'Khách hàng có hơn 200 hợp đồng phát sinh trong 10 tháng.',
      ['1. Lọc kỳ 01/01/2026 - 31/10/2026', '2. Đổi Số dòng/trang = 100'], '',
      ['Bước 2 dưới 5 giây (môi trường thử: khách 218 hợp đồng khoảng 2,3 giây), màn không treo']),
]

# ================================================================== II. TÌM KIẾM & LỌC DANH SÁCH
G2 = [
    C('Mặc định mọi ô lọc trống', 'P1', 'Lần đầu mở màn trong phiên làm việc.',
      ['1. Mở màn', '2. Quan sát khu vực lọc'], '',
      ['Thời gian, Khách hàng, Số hợp đồng, ô tìm nhanh, các ô tổ chức đều trống', 'Ô Thời gian và Khách hàng có dấu * đỏ']),
    C('Bấm Tìm kiếm khi chưa chọn ô bắt buộc', 'P0', 'Đang mở màn, chưa chọn gì.',
      ['1. Bấm Tìm kiếm'], '',
      ['Dưới ô Thời gian: "Vui lòng chọn thời gian"; dưới ô Khách hàng: "Vui lòng chọn khách hàng" (chữ đỏ)',
       'Bảng vẫn hiện lời nhắc, không tải số liệu']),
    C('Chữ đỏ tự tắt khi chọn đủ ô bắt buộc', 'P2', 'Đang có chữ đỏ dưới ô Thời gian và ô Khách hàng.',
      ['1. Chọn Thời gian', '2. Chọn Khách hàng'], '',
      ['Chọn xong ô nào thì chữ đỏ của ô đó tắt', 'Đủ 2 ô: bảng tự tải số liệu, không cần bấm Tìm kiếm']),
    C('Chỉ chọn Khách hàng, chưa chọn Thời gian', 'P1', 'Đang mở màn.',
      ['1. Chọn KH-TEST'], '', ['Bảng vẫn hiện "' + LN + '"']),
    C('Ô Khách hàng cần gõ từ 2 ký tự', 'P2', 'Đang mở màn.',
      ['1. Bấm ô Khách hàng, gõ 1 ký tự', '2. Gõ thêm 1 ký tự'], 'Từ khóa: "BÁ" (khách hàng BÁCH LIÊN)',
      ['Bước 1: chưa hiện kết quả', 'Bước 2: hiện danh sách khách hàng dạng "Mã KH - Tên khách hàng"']),
    C('Chọn nhiều khách hàng', 'P1', 'KH-TEST và KH-TEST-2 cùng có phát sinh trong kỳ.',
      ['1. Chọn Thời gian', '2. Chọn KH-TEST, ghi Tổng cộng', '3. Chọn thêm KH-TEST-2'], '',
      ['Bước 3: bảng gồm hợp đồng của cả 2 khách', 'Các cột phát sinh của Tổng cộng = tổng khi xem riêng từng khách']),
    C('Lịch không cho chọn ngày ngược chiều', 'P1', 'Đang mở màn.',
      ['1. Chọn Từ ngày 30/06/2026', '2. Mở lịch Đến ngày, thử bấm 01/01/2026', '3. Gõ tay 01/01/2026 vào Đến ngày, nhấn Enter'],
      'Từ 30/06/2026, Đến 01/01/2026',
      ['Bước 2: các ngày trước 30/06/2026 bị khóa, không bấm được',
       'Bước 3: ô Đến ngày không nhận ngày nhỏ hơn Từ ngày; không có lỗi "Lỗi khi tải dữ liệu"',
       'Ghi lại giá trị thực tế ô Đến ngày hiển thị sau bước 3 vào cột Ghi chú']),
    C('Từ ngày bằng Đến ngày (1 ngày)', 'P2', 'KH-TEST có chứng từ hạch toán ngày X.',
      ['1. Chọn Thời gian X - X, Khách hàng KH-TEST'], 'X = ngày hạch toán của 1 chứng từ',
      ['Chỉ có chứng từ hạch toán đúng ngày X', 'Số dư đầu kỳ = công nợ trước ngày X']),
    C('Tính cả 2 đầu mút của kỳ', 'P1', 'KH-TEST có chứng từ C1 hạch toán ngày D1, chứng từ C2 ngày D2 (D1 < D2).',
      ['1. Lọc Thời gian D1 - D2', '2. Lọc D1+1 - D2', '3. Lọc D1 - D2-1'], '',
      ['Bước 1: có cả C1, C2', 'Bước 2: không có C1; số của C1 chuyển vào Số dư đầu kỳ', 'Bước 3: không có C2']),
    C('Ô Số hợp đồng lọc gần đúng và đổi dòng Tổng cộng', 'P0', 'KH-TEST có HD-TEST-01 và hợp đồng khác.',
      ['1. ' + LOC + ', ghi Tổng cộng', '2. Nhập 1 phần số của HD-TEST-01 vào ô Số hợp đồng, nhấn Enter'],
      'Một đoạn giữa số HD-TEST-01',
      ['Chỉ còn hợp đồng có số chứa đoạn đã nhập', 'Dòng Tổng cộng (kể cả Số dư đầu kỳ) tính lại chỉ theo các hợp đồng đó',
       'Chỉ áp khi nhấn Enter / Tìm kiếm, gõ chưa nhấn Enter thì bảng chưa đổi']),
    C('Tìm nhanh đúng số chứng từ: thu hẹp hợp đồng, KHÔNG đổi Tổng cộng', 'P0', 'Khách hàng có nhiều hợp đồng phát sinh trong kỳ.',
      ['1. Chọn Thời gian 01/01/2026 - 31/10/2026, khách hàng ở Test data, ghi Tổng cộng', '2. Gõ đủ số 1 phiếu xuất của hợp đồng thứ 2 vào ô tìm nhanh, bấm Tìm kiếm'],
      'Môi trường thử: khách hàng TOYOTA HÀ ĐÔNG, từ khóa PXBHM-04941',
      ['Chỉ còn hợp đồng có chứng từ đó (hiện đủ mọi chứng từ của hợp đồng)', 'Dòng Tổng cộng giữ nguyên số ở bước 1',
       'Chân bảng "Hiển thị 1–1 / 1 hợp đồng"']),
    C('Tìm nhanh một phần số hợp đồng / số chứng từ', 'P1', 'Đã chọn bộ lọc, bảng có dữ liệu.',
      ['1. ' + LOC, '2. Gõ "PXH" vào ô tìm nhanh, nhấn Enter', '3. Gõ một đoạn giữa số HD-TEST-01, nhấn Enter'], 'Từ khóa: PXH; một đoạn số HD-TEST-01',
      ['Bước 2: chỉ còn hợp đồng có ít nhất 1 phiếu xuất hàng trong kỳ', 'Bước 3: còn HD-TEST-01 (tìm gần đúng)',
       'Dòng Tổng cộng giữ nguyên như khi chưa tìm']),
] + tk_chung(M) + [
    C('Lọc Nhân viên = người tạo hợp đồng', 'P1', 'Tài khoản TK-SA; HD-TEST-01 do NV-A tạo.',
      ['1. ' + LOC, '2. Ô Nhân viên chọn NV-A'], '',
      ['Chỉ còn hợp đồng bán hàng / hợp đồng dịch vụ SC-BD-BT do NV-A tạo', 'Dòng Tổng cộng tính lại theo các hợp đồng đó']),
    C('Lọc Công ty / Phòng ban / Bộ phận theo hồ sơ người tạo hợp đồng', 'P1', 'Tài khoản TK-SA; NV-A thuộc phòng P1.',
      ['1. ' + LOC, '2. Chọn Công ty A', '3. Chọn thêm Phòng ban P1', '4. Chọn thêm Bộ phận của NV-A'], '',
      ['Mỗi bước bảng tải lại ngay (không cần Tìm kiếm), số hợp đồng giảm dần hoặc giữ nguyên',
       'Phòng ban chỉ liệt kê phòng của công ty đã chọn; Bộ phận chỉ của phòng đã chọn']),
    C('Lọc tổ chức loại các loại hợp đồng khác và bút toán chưa gắn hợp đồng', 'P2', 'KH-TEST có bút toán chưa gắn hợp đồng hoặc hợp đồng mở đầu kỳ.',
      ['1. ' + LOC + ', ghi Tổng cộng', '2. Chọn ô Công ty = công ty có mọi hợp đồng của KH-TEST'], '',
      ['Hợp đồng không phải hợp đồng bán hàng / dịch vụ SC-BD-BT biến mất',
       'Các cột phát sinh của Tổng cộng giảm đúng phần bút toán chưa gắn hợp đồng / hợp đồng loại khác']),
    C('Kết hợp nhiều điều kiện lọc và tìm nhanh', 'P1', 'Tài khoản TK-SA, đã chọn bộ lọc, bảng có dữ liệu.',
      ['1. ' + LOC, '2. Nhập Số hợp đồng', '3. Chọn Nhân viên', '4. Nhập tìm nhanh, nhấn Enter'], '',
      ['Kết quả thỏa đồng thời mọi điều kiện', 'Chân bảng tính lại theo số hợp đồng còn lại, bảng về trang 1']),
    C('Tổng số và phân trang sau khi lọc', 'P1', M['nhieu_trang'],
      ['1. Chọn Thời gian 01/01/2026 - 31/10/2026, Khách hàng KH-NHIEU, ghi N ở chân bảng', '2. Chọn Nhân viên = 1 người tạo một phần hợp đồng',
       '3. Đọc chân bảng, chuyển trang'], '',
      ['Chân bảng hiện "Hiển thị 1–… / M hợp đồng" với M nhỏ hơn N, bằng số hợp đồng còn lại',
       'Số trang tính lại theo M; chuyển trang chỉ trong tập đã lọc']),
    C('Nút Làm mới xóa hết tiêu chí', 'P0', 'Đã lọc nhiều điều kiện, có tìm nhanh.',
      ['1. Bấm Làm mới'], '',
      ['Mọi ô (kể cả Thời gian, Khách hàng, ô tìm nhanh) về trống, chữ đỏ không hiện', 'Bảng về lời nhắc "' + LN + '"']),
    C('Đổi bộ lọc liên tục chỉ hiện kết quả lần cuối', 'P2', 'KH-TEST và KH-TEST-2 có số liệu khác nhau.',
      ['1. ' + LOC, '2. Liên tiếp bỏ KH-TEST, chọn KH-TEST-2 thật nhanh'], '',
      ['Bảng cuối cùng là số của KH-TEST-2, không bị số của KH-TEST đè lên', '"Đang tải dữ liệu..." tắt khi số mới về']),
    C('Ẩn / hiện khu vực tìm kiếm nâng cao', 'P2', 'Đang mở màn.',
      ['1. Bấm "Ẩn tìm kiếm nâng cao"', '2. Bấm "Tìm kiếm nâng cao"'], '',
      ['Bước 1: các ô lọc thu gọn, còn ô tìm nhanh và các nút; nút đổi chữ thành "Tìm kiếm nâng cao"', 'Bước 2: các ô lọc hiện lại, giá trị đã chọn giữ nguyên']),
    C('Cài đặt bộ lọc', 'P2', 'Đang mở màn.',
      ['1. Bấm "Cài đặt bộ lọc"', '2. Bỏ tích "Số hợp đồng", bấm Lưu', '3. Mở lại, bấm "Khôi phục mặc định", Lưu'], '',
      ['Cửa sổ "Cài đặt bộ lọc" liệt kê các ô lọc của màn; có nút Lưu, Khôi phục mặc định, Đóng',
       'Bước 2: ô Số hợp đồng ẩn khỏi khu vực lọc', 'Bước 3: các ô lọc về như ban đầu']),
] + luu_chung(M)

# ================================================================== III. SỐ LIỆU BÁO CÁO
G3 = [
    C('Cột Hàng hóa/Dịch vụ dòng hợp đồng = tổng các dòng chứng từ', 'P0', BL,
      ['1. Lọc như Tiền điều kiện', '2. Đọc hợp đồng 2 và các dòng 2.1, 2.2, 2.3'], '',
      ['Hợp đồng 2 (HĐ_TPE_HN_KD2_26_0267_236): Hàng hóa/Dịch vụ 663,120 = 259,200 (2.1) + 403,920 (2.2)',
       'Điều chỉnh công nợ giảm 663,120 = dòng 2.3']),
    C('Các cột phát sinh dòng Tổng cộng = tổng các dòng hợp đồng', 'P0', BL + ' Khách không có bút toán chưa gắn hợp đồng.',
      ['1. Cộng từng cột của 10 dòng hợp đồng'], '',
      ['Hàng hóa/Dịch vụ: 16,173,540; Điều chỉnh công nợ giảm: 9,601,740 — bằng dòng Tổng cộng',
       'Các cột còn lại của Tổng cộng in "0"']),
    C('Số dư cuối kỳ dòng Tổng cộng theo công thức', 'P0', BL,
      ['1. Tính: Đầu kỳ + HH/DV + ĐCCN tăng - Nhập trả lại - Đã thanh toán - ĐCCN giảm + Trả lại tiền thừa'], '',
      ['-2,251,800 + 16,173,540 + 0 - 0 - 0 - 9,601,740 + 0 = 4,320,000 = Số dư cuối kỳ dòng Tổng cộng']),
    C('Số dư cuối kỳ dòng hợp đồng KHÔNG trừ điều chỉnh công nợ', 'P0', BL,
      ['1. Đọc hợp đồng 1'], '',
      ['Hàng hóa/Dịch vụ 7,506,000, Điều chỉnh công nợ giảm 5,254,200, Số dư cuối kỳ 7,506,000 (không trừ 5,254,200)',
       'Ghi nhận đúng thiết kế (không ghi Failed): tổng Số dư cuối kỳ các dòng hợp đồng khác dòng Tổng cộng']),
    C('Số dư cuối kỳ dòng chứng từ cộng dồn', 'P0', BL,
      ['1. Đọc cột Số dư cuối kỳ dòng 2.1, 2.2, 2.3'], '',
      ['2.1: 259,200; 2.2: 663,120; 2.3 (phiếu điều chỉnh giảm): vẫn 663,120',
       'Dòng chứng từ cuối của hợp đồng có Số dư cuối kỳ = Số dư cuối kỳ dòng hợp đồng']),
    C('Số dư đầu kỳ chỉ ở dòng Tổng cộng', 'P0', BL,
      ['1. Đọc cột Số dư đầu kỳ'], '', ['Tổng cộng: -2,251,800', 'Mọi dòng hợp đồng và chứng từ: để trống']),
    C('Số dư đầu kỳ = Số dư cuối kỳ của kỳ liền trước', 'P1', 'Khách hàng BÁCH LIÊN (môi trường thử).',
      ['1. Lọc 01/01/2026 - 30/06/2026, ghi Số dư cuối kỳ Tổng cộng = A', '2. Lọc 01/07/2026 - 31/10/2026, đọc Số dư đầu kỳ'],
      'Môi trường thử: A = 4,320,000', ['Số dư đầu kỳ bước 2 = A']),
    C('Hợp đồng toàn số 0 không lên bảng', 'P1', 'KH-TEST có hợp đồng chỉ có bút toán trước kỳ.',
      ['1. ' + LOC, '2. Tìm hợp đồng đó trên bảng'], '',
      ['Không có hợp đồng nào 7 cột phát sinh đều trống', 'Hợp đồng chỉ có bút toán trước kỳ không có dòng; số của nó nằm trong Số dư đầu kỳ dòng Tổng cộng']),
    C('Bút toán chưa gắn hợp đồng chỉ vào Tổng cộng', 'P1', 'KH-TEST có chứng từ trong kỳ không gắn hợp đồng (có sẵn).',
      ['1. ' + LOC, '2. So tổng các dòng hợp đồng với dòng Tổng cộng'], '',
      ['Không có dòng nào cho chứng từ đó', 'Dòng Tổng cộng lớn hơn tổng các dòng hợp đồng đúng bằng số của chứng từ đó']),
    C('Số chứng từ kèm số phiếu yêu cầu', 'P1', BL,
      ['1. Đọc cột Số chứng từ các dòng phiếu xuất'], '',
      ['Dạng "PXH-19789 (PYCXH-20388)"', 'Phiếu kế toán chỉ có số phiếu, vd "TPE.PKT0326.00055"']),
    C('Diễn giải lấy ghi chú của dòng hợp đồng trên phiếu', 'P2', 'Có phiếu kế toán ghi cho 2 hợp đồng với 2 ghi chú khác nhau.',
      ['1. Đọc cột Diễn giải ở 2 dòng chứng từ của phiếu đó'], '',
      ['Mỗi dòng hiện đúng ghi chú của dòng chi tiết ứng với hợp đồng của nó']),
    C('Định dạng số và ô bằng 0', 'P1', BL,
      ['1. Quan sát các cột số'], '',
      ['Số dạng 1,234,567, không phần lẻ; số âm có dấu "-" (vd -2,251,800)',
       'Ô 0 ở dòng hợp đồng / chứng từ để trống; dòng Tổng cộng in "0"']),
    C('Chuyển trang và đổi số dòng không đổi dòng Tổng cộng', 'P1', 'KH-TEST có hơn 10 hợp đồng.',
      ['1. ' + LOC + ', ghi Tổng cộng', '2. Sang trang 2', '3. Đổi Số dòng/trang = 20'], '',
      ['Tổng cộng giữ nguyên ở cả 3 bước', 'Bước 3 quay về trang 1, chân bảng "Hiển thị 1–20 / N hợp đồng"']),
    # --- lập chứng từ rồi kiểm số tăng / giảm
    C('Ghi lại số nền trước khi lập chứng từ', 'P0', 'KH-TEST, HD-TEST-01 do NV-A tạo; kỳ = 01/01/2026 đến hôm nay.',
      ['1. ' + MENU, '2. Chọn kỳ đến hôm nay, Khách hàng KH-TEST', '3. Chụp màn hình dòng Tổng cộng và dòng HD-TEST-01'], '',
      ['Có đủ 8 cột số của Tổng cộng và HD-TEST-01 để làm số nền cho các case sau']),
    C('Phiếu xuất hàng làm tăng Hàng hóa/Dịch vụ', 'P0', NEN + ' Có sẵn yêu cầu xuất hàng đã duyệt cho HD-TEST-01.',
      ['1. Vào ' + MENU_PX + ', lập phiếu xuất cho yêu cầu đó, hoàn tất để phiếu được hạch toán hôm nay', '2. Lọc lại báo cáo'],
      'Giá trị xuất (gồm thuế): 10,000,000',
      ['Hàng hóa/Dịch vụ của HD-TEST-01 và Tổng cộng tăng 10,000,000; Số dư cuối kỳ của cả 2 dòng tăng 10,000,000',
       'Có thêm dòng chứng từ ngày hôm nay, Số chứng từ = "<số phiếu xuất> (<số phiếu yêu cầu>)", bấm vào mở popup Danh sách hàng hóa']),
    C('Phiếu thu làm tăng Đã thanh toán', 'P0', NEN,
      ['1. Vào ' + MENU_PT + ', lập phiếu thu của KH-TEST cho HD-TEST-01, hạch toán hôm nay', '2. Lọc lại báo cáo'],
      'Số tiền: 4,000,000',
      ['Đã thanh toán tăng 4,000,000 ở HD-TEST-01 và Tổng cộng', 'Số dư cuối kỳ của cả 2 dòng giảm 4,000,000',
       'Dòng chứng từ mới: Diễn giải = ghi chú của dòng HD-TEST-01 trên phiếu thu; bấm số phiếu mở phiếu thu ở tab mới']),
    C('Phiếu báo có làm tăng Đã thanh toán', 'P1', NEN,
      ['1. Vào ' + MENU_BC + ', lập phiếu báo có của KH-TEST cho HD-TEST-01, hạch toán hôm nay', '2. Lọc lại báo cáo'],
      'Số tiền: 1,000,000', ['Đã thanh toán tăng 1,000,000; Số dư cuối kỳ giảm 1,000,000 (HD-TEST-01 và Tổng cộng)']),
    C('Điều chỉnh công nợ TĂNG', 'P0', NEN,
      ['1. Vào ' + MENU_YCDC + ', lập yêu cầu điều chỉnh tăng cho KH-TEST, HD-TEST-01, duyệt đủ',
       '2. Kế toán lập phiếu ở ' + MENU_PKT + ', hạch toán hôm nay', '3. Lọc lại báo cáo'],
      'Tăng 2,000,000',
      ['Cột Điều chỉnh công nợ (nhóm tăng) tăng 2,000,000 ở HD-TEST-01 và Tổng cộng',
       'Số dư cuối kỳ Tổng cộng tăng 2,000,000',
       'Ghi nhận đúng thiết kế: Số dư cuối kỳ dòng HD-TEST-01 và dòng chứng từ mới KHÔNG đổi']),
    C('Điều chỉnh công nợ GIẢM', 'P0', NEN,
      ['1. Lập yêu cầu điều chỉnh giảm KH-TEST, HD-TEST-01, duyệt và lập phiếu kế toán, hạch toán hôm nay', '2. Lọc lại báo cáo'],
      'Giảm 500,000',
      ['Cột Điều chỉnh công nợ (nhóm giảm) tăng 500,000; Số dư cuối kỳ Tổng cộng giảm 500,000',
       'Ghi nhận đúng thiết kế: Số dư cuối kỳ dòng HD-TEST-01 KHÔNG giảm']),
    C('Khách trả lại hàng làm tăng Nhập trả lại', 'P0', 'HD-TEST-01 đã xuất hàng; có sẵn yêu cầu nhập hàng trả lại đã duyệt.',
      ['1. Vào ' + MENU_NH + ', lập phiếu nhập hàng trả lại cho yêu cầu đó, hạch toán hôm nay', '2. Lọc lại báo cáo'],
      'Trả lại 3,000,000',
      ['Nhập trả lại tăng 3,000,000; Số dư cuối kỳ HD-TEST-01 và Tổng cộng giảm 3,000,000',
       'Dòng chứng từ: "<số phiếu nhập> (<số phiếu yêu cầu nhập hàng>)"']),
    C('Phiếu chi trả lại tiền thừa', 'P1', NEN,
      ['1. Vào ' + MENU_PC + ', lập phiếu chi trả tiền thừa cho KH-TEST theo HD-TEST-01, hạch toán hôm nay', '2. Lọc lại báo cáo'],
      'Số tiền: 800,000', ['Trả lại tiền thừa tăng 800,000; Số dư cuối kỳ HD-TEST-01 và Tổng cộng TĂNG 800,000']),
    C('Ủy nhiệm chi trả lại tiền thừa', 'P2', NEN,
      ['1. Vào ' + MENU_UNC + ', lập ủy nhiệm chi cho KH-TEST theo HD-TEST-01, hạch toán hôm nay', '2. Lọc lại báo cáo'],
      'Số tiền: 200,000', ['Trả lại tiền thừa tăng 200,000; Số dư cuối kỳ tăng 200,000']),
    C('Phiếu xuất bán hàng mượn làm tăng Hàng hóa/Dịch vụ', 'P1', NEN + ' Có sẵn yêu cầu xuất bán hàng mượn đã duyệt cho HD-TEST-01.',
      ['1. Vào ' + MENU_BS + ', lập phiếu cho yêu cầu đó, hạch toán hôm nay', '2. Lọc lại báo cáo'],
      'Số tiền: 1,500,000', ['Hàng hóa/Dịch vụ tăng 1,500,000', 'Bấm số phiếu mở popup Danh sách hàng hóa dạng hàng mượn (cột Số lượng)']),
    C('Chứng từ hạch toán ngoài kỳ', 'P1', 'Đã có các chứng từ hạch toán hôm nay ở các case trên.',
      ['1. Lọc kỳ 01/01/2026 đến hôm qua', '2. Lọc kỳ từ ngày mai đến cuối tháng'], '',
      ['Bước 1: không có các chứng từ hôm nay',
       'Bước 2: các chứng từ hôm nay chỉ nằm trong Số dư đầu kỳ, không có dòng hợp đồng / chứng từ nào của chúng']),
    C('Hạch toán dịch vụ / biên bản thanh lý / khai báo đầu kỳ', 'P2', 'Có sẵn chứng từ các loại này của KH-TEST trong kỳ.',
      ['1. ' + LOC, '2. Tìm dòng chứng từ tương ứng'], '',
      ['Hạch toán dịch vụ, biên bản thanh lý: vào cột Hàng hóa/Dịch vụ',
       'Khai báo công nợ đầu kỳ: phần ghi Nợ vào Hàng hóa/Dịch vụ, phần ghi Có vào Đã thanh toán']),
]

# ================================================================== IV. XEM CHI TIẾT DANH SÁCH HÀNG HÓA (popup)
G4 = [
    C('Mở popup hàng hóa của phiếu xuất hàng', 'P0', BL,
      ['1. Bấm "PXH-19789 (PYCXH-20388)" (dòng 1.2)'], '',
      ['Popup "Danh sách hàng hóa", dòng phụ "Phiếu xuất hàng - PXH-19789"',
       'Cột: STT, Tên hàng hóa, Model, Mã hàng hóa, Đơn vị tính, SL đề nghị, SL thực xuất, Giá niêm yết, Giảm giá bán, Đơn giá bán, Thành tiền bán',
       '1 dòng: XUPER 680CGS, KG, SL 5 / 5, Giá niêm yết 1,390,000, Giảm giá bán trống, Đơn giá bán 1,390,000, Thành tiền bán 6,950,000']),
    C('Hàng hóa trong popup khớp phiếu xuất đã lập', 'P0', 'Phiếu xuất hàng PXH-19789 đang mở ở tab khác.',
      ['1. Mở popup của PXH-19789', '2. So từng dòng với phiếu xuất (tên hàng, đơn vị tính, số lượng, đơn giá)'], '',
      ['Số dòng hàng hóa, tên hàng, số lượng, đơn giá trong popup đúng như trên phiếu xuất']),
    C('Thành tiền bán là giá chưa thuế', 'P2', BL,
      ['1. Mở popup PXH-19789', '2. So Thành tiền bán với cột Hàng hóa/Dịch vụ của dòng 1.2'], '',
      ['Popup 6,950,000; báo cáo 7,506,000 (chênh do thuế) — đúng thiết kế, ghi nhận không ghi Failed']),
    C('Popup hàng hóa của phiếu xuất bán hàng mượn', 'P1', 'Môi trường thử: khách hàng TOYOTA HÀ ĐÔNG, kỳ 01/01/2026 - 31/10/2026.',
      ['1. Tìm nhanh PXBHM-04941', '2. Bấm số phiếu'], '',
      ['Dòng phụ "Phiếu xuất bán hàng mượn - PXBHM-04941"', 'Có cột Số lượng; KHÔNG có SL đề nghị, SL thực xuất, Thành tiền bán']),
    C('Popup chỉ để xem, không có nút Lưu', 'P1', 'Đang mở popup Danh sách hàng hóa.',
      ['1. Bấm thử vào các ô trong popup', '2. Quan sát các nút ở chân popup'], '',
      ['Không ô nào cho sửa', 'Chỉ có nút Xem chi tiết phiếu và Đóng; không có nút Lưu']),
    C('Nút Xem chi tiết phiếu và Đóng', 'P1', 'Đang mở popup của PXH-19789, bảng đang ở trang 2.',
      ['1. Bấm Xem chi tiết phiếu', '2. Quay lại tab báo cáo, bấm Đóng'], '',
      ['Bước 1: mở phiếu xuất hàng ở tab mới', 'Bước 2: popup đóng, bảng giữ nguyên trang và bộ lọc']),
    C('Đóng popup bằng nút X góc trên', 'P2', 'Đang mở popup Danh sách hàng hóa.',
      ['1. Bấm nút X góc trên popup'], '', ['Popup đóng, bảng giữ nguyên trang, bộ lọc và vị trí đang xem']),
    C('Số chứng từ khác không mở popup', 'P2', BL,
      ['1. Bấm số phiếu kế toán TPE.PKT0326.00055'], '', ['Không mở popup; mở phiếu kế toán ở tab mới']),
]

# ================================================================== V. XUẤT DANH SÁCH EXCEL
G5 = [
    C('Xuất Excel khi chưa chọn đủ bộ lọc bắt buộc', 'P0', 'Đang mở màn, chưa chọn gì.',
      ['1. Bấm Xuất Excel'], '', ['Báo "Vui lòng chọn khách hàng và thời gian", không mở cửa sổ, không tải file']),
    C('Mở cửa sổ chọn trường xuất Excel', 'P0', 'Đã lọc có số liệu.',
      ['1. Bấm Xuất Excel'], '',
      ['Tiêu đề "Chọn trường xuất Excel"; 11 trường đã tích sẵn: Ngày chứng từ, Số chứng từ, Diễn giải, Số dư đầu kỳ, PS tăng - Hàng hóa/Dịch vụ, '
       'PS tăng - Điều chỉnh công nợ, PS giảm - Nhập trả lại, PS giảm - Đã thanh toán, PS giảm - Điều chỉnh công nợ, Trả lại tiền thừa, Số dư cuối kỳ',
       '"Đang chọn 11/11 trường"; nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng']),
    C('Nội dung file Excel với các trường mặc định', 'P0', BL,
      ['1. Bấm Xuất Excel > Xuất file', '2. Mở file'], '',
      ['Sheet "Đối chiếu công nợ"; báo "Xuất Excel thành công"',
       'Dòng 1 "BẢNG ĐỐI CHIẾU CÔNG NỢ KHÁCH HÀNG"; dòng 2 "Khách hàng: 29TPHPHO-209 - CÔNG TY CỔ PHẦN BÁCH LIÊN"; dòng 3 "Thời gian: 01/01/2026 - 30/06/2026"',
       'Tiêu đề 2 tầng, cột STT đầu tiên; dòng Tổng cộng: -2,251,800 | 16,173,540 | … | 9,601,740 | … | 4,320,000',
       '37 dòng: 5 dòng đầu + Tổng cộng + 10 hợp đồng (in đậm) + 21 chứng từ; số là kiểu số, định dạng 1,234,567']),
    C('Bỏ tích một số trường và đổi thứ tự', 'P1', 'Đã lọc có số liệu, đang mở cửa sổ chọn trường.',
      ['1. Bỏ tích Diễn giải, kéo Số dư cuối kỳ lên đầu', '2. Xuất file, mở file'], '',
      ['File không có cột Diễn giải; sau STT là Số dư cuối kỳ', 'Các trường PS tăng / PS giảm không đứng liền nhau thì không gộp tiêu đề nhóm']),
    C('Xuất theo đúng bộ lọc đang áp dụng', 'P0', 'KH-TEST có HD-TEST-01 và hợp đồng khác.',
      ['1. ' + LOC + ', nhập số HD-TEST-01 vào ô Số hợp đồng, nhấn Enter', '2. Bấm Xuất Excel > Xuất file, mở file'], '',
      ['File chỉ có HD-TEST-01 và chứng từ của nó', 'Dòng Tổng cộng trong file bằng dòng Tổng cộng trên màn (đã tính lại theo Số hợp đồng)']),
    C('Ô bằng 0 trong file Excel', 'P2', BL,
      ['1. Xuất file', '2. Xem các ô 0 của dòng Tổng cộng trong file'], '',
      ['Ghi lại thực tế: trên màn dòng Tổng cộng in "0", trong file ô 0 hiển thị trống (giá trị vẫn là 0)']),
] + xl_chung(M) + [
    C('Thời gian xuất Excel khách hàng nhiều hợp đồng', 'P2', 'Khách hàng có hơn 200 hợp đồng phát sinh trong 10 tháng.',
      ['1. Lọc kỳ 01/01/2026 - 31/10/2026', '2. Bấm Xuất Excel > Xuất file, đo thời gian'], '',
      ['Xuất xong dưới 30 giây, màn không treo, file đủ mọi hợp đồng']),
]

# ================================================================== VI. IN BÁO CÁO
G6 = [
    C('In khi chưa chọn đủ bộ lọc bắt buộc', 'P0', 'Đang mở màn, chưa chọn gì.',
      ['1. Bấm In'], '', ['Báo "Vui lòng chọn khách hàng và thời gian", không mở cửa sổ xem trước']),
    C('Xem trước bản in', 'P0', BL,
      ['1. Bấm In'], '',
      ['Cửa sổ "Xem trước bảng đối chiếu công nợ khách hàng", khổ ngang, có nút In',
       'Mẫu "BÁO CÁO ĐỐI SOÁT CÔNG NỢ KHÁCH HÀNG", ngày in, Khách hàng: CÔNG TY CỔ PHẦN BÁCH LIÊN, Từ ngày 01/01/2026, Đến ngày 30/06/2026',
       'Bảng đủ 10 hợp đồng (mọi trang), dòng Tổng cộng ngay dưới tiêu đề khớp màn hình',
       'Bấm In trong cửa sổ in ra máy in, không mở tab mới']),
    C('Bản in theo bộ lọc đang áp và lấy mọi trang', 'P1', 'KH-NHIEU có hơn 10 hợp đồng; bảng đang ở trang 1.',
      ['1. Chọn Thời gian 01/01/2026 - 31/10/2026, Khách hàng KH-NHIEU', '2. Bấm In, đếm số hợp đồng', '3. Đóng, gõ 1 số chứng từ vào ô tìm nhanh, nhấn Enter, bấm In lại'], '',
      ['Bước 2: bản in có đủ N hợp đồng (bằng N ở chân bảng), không chỉ 10 hợp đồng trang đang xem',
       'Bước 3: bản in chỉ có hợp đồng khớp tìm nhanh, dòng Tổng cộng như màn hình']),
    C('In vượt 2.000 dòng', 'P2', 'Khách hàng có hơn 2.000 dòng (hợp đồng + chứng từ) trong kỳ dài.',
      ['1. Lọc kỳ dài', '2. Bấm In'], '',
      ['Cửa sổ chỉ hiện "Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài."',
       'Không có nút In']),
    C('Đóng cửa sổ xem trước', 'P2', 'Đang mở cửa sổ xem trước bản in.',
      ['1. Bấm nút đóng cửa sổ xem trước'], '', ['Cửa sổ đóng, không in', 'Bảng báo cáo giữ nguyên bộ lọc và trang đang xem']),
]

# ================================================================== VII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
G7 = [
    C('Kiểm tổng sau cả chuỗi chứng từ', 'P0', 'Đã lập lần lượt các chứng từ ở nhóm Số liệu báo cáo (xuất hàng, thu, báo có, điều chỉnh tăng / giảm, trả lại hàng, phiếu chi, ủy nhiệm chi), chưa lập phiếu xuất bán hàng mượn.',
      ['1. Lọc lại báo cáo', '2. So Số dư cuối kỳ dòng Tổng cộng với số nền'], '',
      ['Chênh = +10,000,000 - 4,000,000 - 1,000,000 + 2,000,000 - 500,000 - 3,000,000 + 800,000 + 200,000 = +4,500,000',
       'Số dư cuối kỳ dòng HD-TEST-01 chênh +10,000,000 - 4,000,000 - 1,000,000 - 3,000,000 + 800,000 + 200,000 = +3,000,000 (không tính 2 cột Điều chỉnh công nợ)']),
    C('Chứng từ chưa hạch toán không lên báo cáo, hạch toán xong mới lên', 'P0', NEN,
      ['1. Lập phiếu thu 1,000,000 cho HD-TEST-01, để chưa hạch toán', '2. Lọc lại báo cáo', '3. Kế toán hạch toán phiếu thu đó hôm nay', '4. Lọc lại báo cáo'], '',
      ['Bước 2: không cột nào đổi so với số nền', 'Bước 4: Đã thanh toán tăng 1,000,000, có thêm dòng chứng từ của phiếu thu']),
    C('Hủy hạch toán chứng từ thì số trả về', 'P1', 'Phiếu thu 4,000,000 cho HD-TEST-01 đã hạch toán và đang hiện trên báo cáo.',
      ['1. Kế toán hủy hạch toán (hoặc hủy) phiếu thu đó', '2. Lọc lại báo cáo'], '',
      ['Dòng chứng từ của phiếu thu biến mất', 'Đã thanh toán giảm lại 4,000,000; Số dư cuối kỳ tăng lại 4,000,000 (HD-TEST-01 và Tổng cộng)']),
    C('Bấm số hợp đồng / số chứng từ mở đúng màn liên quan', 'P1', BL,
      ['1. Bấm số hợp đồng ở dòng đậm', '2. Bấm số phiếu kế toán ở dòng chứng từ'], '',
      ['Mở đúng hợp đồng / phiếu kế toán ở tab mới', 'Màn báo cáo giữ nguyên bộ lọc, trang']),
    C('Khách hàng mới tạo có ngay ở ô chọn Khách hàng', 'P1', 'Vừa tạo khách hàng KH-MOI ở màn danh mục khách hàng.',
      ['1. Mở màn báo cáo', '2. Gõ 2 ký tự đầu mã KH-MOI vào ô Khách hàng'], 'Khách hàng: KH-MOI',
      ['KH-MOI có trong danh sách gợi ý dạng "Mã KH - Tên khách hàng", chọn được']),
    C('Đổi tên khách hàng thì báo cáo hiện tên mới', 'P2', 'KH-TEST có phát sinh trong kỳ.',
      ['1. Sửa tên KH-TEST ở màn danh mục khách hàng', '2. Mở báo cáo, chọn lại KH-TEST', '3. Bấm Xuất Excel > Xuất file và bấm In'], '',
      ['Ô Khách hàng, dòng "Khách hàng:" trong file Excel và bản in hiện tên mới', 'Số liệu không đổi']),
    C('Khớp số với Báo cáo chi tiết công nợ khách hàng', 'P1', 'KH-TEST có phát sinh trong kỳ; cùng một tài khoản xem.',
      ['1. Lọc cùng Thời gian, cùng KH-TEST ở màn này và màn Bán hàng > Báo cáo > Báo cáo công nợ > "Chi tiết công nợ KH"',
       '2. So các cột phát sinh và Số dư cuối kỳ'], '',
      ['Các cột phát sinh của dòng Tổng cộng (màn này) bằng các cột tương ứng của dòng khách hàng KH-TEST (màn Chi tiết)',
       'Số dư cuối kỳ dòng Tổng cộng bằng nhau; lệch thì ghi số của từng màn vào Ghi chú']),
    C('Không có hợp đồng hoặc chứng từ bị lặp', 'P1', BL,
      ['1. Đặt 100 dòng/trang', '2. Rà danh sách số hợp đồng và số chứng từ'], '',
      ['Mỗi hợp đồng chỉ có 1 dòng', 'Mỗi chứng từ chỉ có 1 dòng trong 1 hợp đồng (nhiều bút toán của cùng chứng từ được cộng lại)']),
]

# ================================================================== VIII. PHÂN QUYỀN
G8 = [
    C('Người không có quyền vẫn vào được màn, chỉ thấy hợp đồng do mình tạo', 'P0',
      'NV-A không có quyền nào của nhóm "Bảng đối chiếu công nợ 1 khách hàng"; HD-TEST-01 do NV-A tạo.',
      ['1. Đăng nhập NV-A', '2. ' + MENU, '3. ' + LOC], 'Tài khoản NV-A',
      ['Menu có mục "Đối chiếu công nợ 1 KH", màn mở bình thường',
       'Khu vực lọc KHÔNG có ô Công ty, Phòng ban, Bộ phận, Nhân viên',
       'Bảng chỉ có hợp đồng do NV-A tạo (có HD-TEST-01), không có hợp đồng của người khác',
       'Dòng Tổng cộng và Số dư đầu kỳ chỉ cộng bút toán của hợp đồng do NV-A tạo']),
    C('Người không quyền, không tạo hợp đồng nào của khách', 'P1', 'NV-B không quyền, không tạo hợp đồng nào của KH-TEST.',
      ['1. Đăng nhập NV-B', '2. ' + MENU, '3. ' + LOC], 'Tài khoản NV-B',
      ['Bảng hiện "Không có dữ liệu phù hợp bộ lọc."', 'Không hiện dòng Tổng cộng, không có chân bảng']),
    C('Quyền theo tổng công ty thấy mọi hợp đồng và đủ 4 ô lọc tổ chức', 'P0', 'TK-SA có quyền "%s tổng công ty".' % Q,
      ['1. Đăng nhập TK-SA', '2. ' + MENU, '3. ' + LOC], 'Tài khoản TK-SA',
      ['Có 4 ô Công ty, Phòng ban, Bộ phận, Nhân viên',
       'Bảng có mọi hợp đồng của KH-TEST (của mọi công ty, mọi người tạo)',
       'Ghi lại Tổng cộng làm số đối chiếu cho các case phân quyền sau']),
    C('Quyền theo công ty chỉ thấy công ty đang làm việc và hợp đồng mình tạo', 'P0',
      'TK-CT có quyền "%s công ty", đang làm việc ở Công ty A; KH-TEST có hợp đồng ở Công ty A và Công ty B.' % Q,
      ['1. Đăng nhập TK-CT (chọn Công ty A)', '2. ' + MENU, '3. ' + LOC, '4. Đổi công ty đang làm việc sang Công ty B, lọc lại'], 'Tài khoản TK-CT',
      ['Không có ô Công ty; có ô Phòng ban, Bộ phận, Nhân viên',
       'Bước 3: chỉ hợp đồng có bút toán thuộc Công ty A (và hợp đồng TK-CT tạo); Tổng cộng nhỏ hơn hoặc bằng số của TK-SA',
       'Bước 4: số liệu đổi theo Công ty B']),
    C('Quyền theo phòng ban chỉ thấy phòng mình quản lý', 'P1', 'TK-PB có quyền "%s phòng ban", quản lý phòng P1.' % Q,
      ['1. Đăng nhập TK-PB', '2. ' + MENU, '3. ' + LOC], 'Tài khoản TK-PB',
      ['Có ô Phòng ban, Bộ phận, Nhân viên; không có ô Công ty',
       'Chỉ hợp đồng có bút toán thuộc phòng P1 (và hợp đồng TK-PB tạo)']),
    C('Quyền theo bộ phận chỉ thấy bộ phận mình quản lý', 'P1', 'TK-BP có quyền "%s bộ phận".' % Q,
      ['1. Đăng nhập TK-BP', '2. ' + MENU, '3. ' + LOC], 'Tài khoản TK-BP',
      ['Chỉ có ô Bộ phận, Nhân viên', 'Chỉ hợp đồng có bút toán thuộc bộ phận TK-BP quản lý (và hợp đồng TK-BP tạo)']),
    C('Có nhiều quyền thì lấy cấp cao nhất', 'P2', 'Tài khoản có cả quyền theo bộ phận và theo công ty.',
      ['1. Đăng nhập', '2. ' + MENU, '3. ' + LOC], '',
      ['Ô lọc và số liệu giống tài khoản chỉ có quyền theo công ty']),
    C('Phạm vi quyền áp cho cả popup, Excel và bản In', 'P1', 'NV-A không quyền; HD-TEST-01 do NV-A tạo có phiếu xuất hàng trong kỳ.',
      ['1. Đăng nhập NV-A, ' + LOC[0].lower() + LOC[1:], '2. Bấm số phiếu xuất của HD-TEST-01, xem popup', '3. Bấm Xuất Excel > Xuất file', '4. Bấm In'], '',
      ['Popup mở được cho chứng từ trong phạm vi', 'File Excel và bản xem trước chỉ có hợp đồng do NV-A tạo, dòng Tổng cộng khớp màn hình']),
] + pq_chung(M)

GROUPS = [
    ('HIỂN THỊ TRANG & TRUY CẬP', G1),
    ('TÌM KIẾM & LỌC DANH SÁCH', G2),
    ('SỐ LIỆU BÁO CÁO', G3),
    ('XEM CHI TIẾT DANH SÁCH HÀNG HÓA', G4),
    ('XUẤT DANH SÁCH EXCEL', G5),
    ('IN BÁO CÁO', G6),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', G7),
    ('PHÂN QUYỀN', G8),
]

if __name__ == '__main__':
    build_chuan(OUT, 'Trang tính1', TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, sections(GROUPS), loai='bao_cao')
    print(dem(GROUPS))

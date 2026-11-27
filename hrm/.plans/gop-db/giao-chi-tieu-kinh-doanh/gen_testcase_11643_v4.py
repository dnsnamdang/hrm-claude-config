# -*- coding: utf-8 -*-
"""Testcase #11643 — bản 4 (27/11/2026) theo góp ý tester/user:
  - Thêm khối MÔ TẢ CHỨC NĂNG 10 mục (2-3 dòng / mục) đúng form tab 25.
  - Thêm nhóm HIỂN THỊ & TRUY CẬP; gộp mọi case Thêm mới vào 1 nhóm; viết chi tiết hơn phần Sửa;
    PHÂN QUYỀN nêu rõ chức năng nào cần quyền nào.
  - Tiền điều kiện trùng case ngay trước thì ghi "Giống TC_...".
GIỮ NGUYÊN mọi case đang có trên tab 52 (nội dung + cột J..R kết quả / ghi chú) — đọc từ dump
`tab52_truoc_doi_form_27-11.csv`; chỉ đổi cột A/B (gộp theo nhóm kiểu form) và F khi trùng case trước. ID giữ nguyên.
"""
import csv
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_testcase_11643_v2 as v2  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font  # noqa: E402
from openpyxl.worksheet.datavalidation import DataValidation  # noqa: E402

OUT = os.path.join(HERE, 'testcase - #11643 theo form 27-11.xlsx')
SRC = os.path.join(HERE, 'tab52_truoc_doi_form_27-11.csv')
rows = list(csv.reader(open(SRC, encoding='utf-8')))
CUR = {r[2]: (r + [''] * 18)[:18] for r in rows if len(r) > 2 and r[2].startswith('TC_')}
assert len(CUR) == 56, len(CUR)

MENU = v2.MENU
MENU_CD = v2.MENU_CD
Q_VIEW, Q_CREATE, Q_APPROVE = v2.Q_VIEW, v2.Q_CREATE, v2.Q_APPROVE
ACC_A, ACC_D = v2.ACC_A, v2.ACC_D
PRE_EDIT, DRAFT, PENDING, APPROVED = v2.PRE_EDIT, v2.DRAFT, v2.PENDING, v2.APPROVED
SUA = v2.SUA
LIST_PRE = ('Tài khoản V có quyền ' + Q_VIEW + ' mức Công ty và quyền ' + Q_CREATE + ', đang làm việc ở công ty TPE.\n'
            'Công ty TPE có 4 phiếu: TPE_CTKD_2025.00004 (Đã duyệt), TPE_CTKD_2026.00009 (Đã duyệt), TPE_CTKD_2027.00015 '
            '(Chờ duyệt), TPE_CTKD_2028.00002 (Hủy); V lập thêm 1 phiếu Đang tạo năm 2029.')


def nr(tid, fn, pr, pre, st, data, ex):
    """Case mới → 18 cột (J..R trống)."""
    return ['', '', tid, fn, pr, pre, v2.steps(st), data or '', v2.exp(ex)] + [''] * 9


def keep(tid):
    return list(CUR[tid])


# ───────────── I. HIỂN THỊ & TRUY CẬP ─────────────
G_HT = [
    nr('TC_01.001', 'Mở màn từ menu', 'P0', LIST_PRE, [MENU], '',
       ['Mở màn "Danh sách phiếu giao chỉ tiêu kinh doanh theo phòng ban"',
        'Có ô tìm nhanh (placeholder "Tìm theo số phiếu"), nút Tìm kiếm nâng cao',
        'Có nút Tạo mới, Xuất Excel, Cấu hình cột (biểu tượng cột)']),
    nr('TC_01.002', 'Các cột mặc định và màu trạng thái', 'P0', LIST_PRE, [MENU], '',
       ['Cột hiện: STT, Số phiếu, Công ty, Năm, Người tạo, Ngày tạo, Người duyệt, Người cập nhật, Ngày cập nhật, Trạng thái, Hành động',
        'Cột Ngày duyệt ẩn mặc định, bật lại được ở Cấu hình cột',
        'Trạng thái: Đang tạo (xám), Chờ duyệt (cam), Đã duyệt (xanh lá), Hủy (đỏ nhạt)',
        'Ngày có kèm giờ; Người tạo / Người duyệt hiện "tên - mã phòng"']),
    nr('TC_01.003', 'Bấm số phiếu mở màn Chi tiết', 'P0', LIST_PRE, [MENU, 'Bấm số phiếu TPE_CTKD_2026.00009.'], '',
       ['Mở màn "Chi tiết phiếu giao chỉ tiêu kinh doanh theo phòng ban: TPE_CTKD_2026.00009" kèm nhãn Đã duyệt',
        'Cột Hành động không có nút Xem riêng (xem chi tiết bằng cách bấm số phiếu)']),
    nr('TC_01.004', 'Tìm nhanh theo số phiếu', 'P1', LIST_PRE, [MENU, 'Gõ lần lượt vào ô tìm nhanh, bấm Enter.'],
       'tpe_ctkd_2026\n2027.00015\nKHONGCO', ['"tpe_ctkd_2026": ra TPE_CTKD_2026.00009 (không phân biệt hoa thường, khớp một phần)',
                                            '"2027.00015": ra đúng 1 phiếu', '"KHONGCO": bảng hiện "Không có phiếu giao chỉ tiêu nào"']),
    nr('TC_01.005', 'Bộ lọc nâng cao và Làm mới', 'P1', LIST_PRE, [MENU, 'Bấm Tìm kiếm nâng cao, lọc Năm = 2026, bấm Tìm kiếm.',
                                                                   'Lọc Trạng thái = Hủy.', 'Bấm Làm mới.'], '',
       ['Có ô lọc: Năm, Người tạo, Người duyệt, Trạng thái (ô Công ty chỉ hiện với người xem mức Tổng công ty)',
        'Bước 1: chỉ còn TPE_CTKD_2026.00009; bước 2: chỉ còn TPE_CTKD_2028.00002',
        'Bước 3: các ô lọc về trống, danh sách hiện lại đủ 5 phiếu']),
    nr('TC_01.006', 'Sắp xếp và phân trang', 'P2', 'Giống TC_01.001', [MENU, 'Bấm tiêu đề cột Năm 2 lần.', 'Đổi số dòng / trang, bấm trang sau.'], '',
       ['Mặc định phiếu mới nhất ở đầu', 'Bấm lần 1 xếp tăng, lần 2 xếp giảm theo Năm; STT liên tục khi sang trang',
        'Các cột có biểu tượng sắp xếp; cột STT, Hành động không sắp xếp']),
    nr('TC_01.007', 'Phiếu Đang tạo của người khác không hiện', 'P0',
       'Tài khoản V2 có quyền ' + Q_VIEW + ' mức Tổng công ty. Phiếu Đang tạo năm 2029 do V lập.', ['Đăng nhập V2.', MENU], '',
       ['Danh sách KHÔNG có phiếu Đang tạo năm 2029 của V (phiếu Đang tạo chỉ người lập thấy)']),
    nr('TC_01.008', 'Lối vào Giao chỉ tiêu chờ duyệt', 'P0', ACC_D + '\nCông ty TPE có 1 phiếu Chờ duyệt TPE_CTKD_2027.00015; công ty TPSG có 1 phiếu Chờ duyệt.',
       [MENU_CD], '',
       ['Tiêu đề "Danh sách phiếu giao chỉ tiêu kinh doanh theo phòng ban chờ duyệt"',
        'Chỉ có TPE_CTKD_2027.00015 (phiếu Chờ duyệt của công ty đang làm việc), không có phiếu của TPSG',
        'Không có nút Tạo mới, không có ô lọc Trạng thái']),
    nr('TC_01.009', 'Danh sách trống', 'P2', 'Tài khoản N không có quyền nào của màn, chưa lập phiếu nào.', ['Đăng nhập N.', MENU], '',
       ['Bảng hiện "Không có phiếu giao chỉ tiêu nào"', 'Không có nút Tạo mới; vẫn có Xuất Excel, Cấu hình cột']),
]

# ───────────── II. THÊM MỚI (gộp 1 nhóm) ─────────────
G_TM = [keep('TC_03.%03d' % i) for i in range(1, 35)]

# ───────────── III. CHỈNH SỬA ─────────────
G_SUA = [keep('TC_04.001'), keep('TC_04.002'), keep('TC_04.003')] + [
    nr('TC_04.004', 'Nút Sửa chỉ có ở phiếu Đang tạo của chính mình', 'P0',
       ACC_A + '\nA có 4 phiếu: P1 Đang tạo, P2 Chờ duyệt, P3 Đã duyệt, P4 Hủy.', [MENU, 'Xem cột Hành động của 4 phiếu.', 'Mở màn Chi tiết P2, P3.'], '',
       ['Chỉ P1 có biểu tượng Sửa (bút chì); P2, P3, P4 không có', 'Màn Chi tiết P2, P3 không có nút Sửa']),
    nr('TC_04.005', 'Thêm Tỉnh/TP, thêm phòng khi Sửa', 'P0', PRE_EDIT,
       SUA + ['Ô Khu vực chọn thêm "Duyên hải miền Trung".', 'Ở Thành phố Hải Phòng chọn PHÒNG KINH DOANH 1, nhập Khách hãng / Hàng hóa 2 / 750,000,000.', 'Bấm Lưu, mở lại Chi tiết.'], '',
       ['Bảng thêm các Tỉnh/TP của Duyên hải miền Trung', 'Lưu thành công; Chi tiết có đủ Hà Nội (số cũ) và Hải Phòng 2 / 750,000,000',
        'Khối thống kê và dòng TỔNG cộng đúng số mới']),
    nr('TC_04.006', 'Xoá dòng phòng có số liệu', 'P1', 'Giống TC_04.005', SUA + ['Bấm thùng rác ở dòng PHÒNG KINH DOANH 1 (Hà Nội).', 'Bấm Hủy.', 'Bấm thùng rác lần nữa, bấm Xoá, bấm Lưu.'], '',
       ['Hộp "Xoá dòng phòng": "Xoá dòng PHÒNG KINH DOANH 1 tại Thành phố Hà Nội? Số liệu của dòng sẽ mất.", 2 nút Hủy / Xoá',
        'Bấm Hủy: dòng và số giữ nguyên', 'Bấm Xoá rồi Lưu: dòng mất, dòng Tỉnh/TP và TỔNG trừ đúng số của dòng']),
    nr('TC_04.007', 'Đổi phòng đã chia bộ phận', 'P1', PRE_EDIT + '\nP1 ở Hà Nội: PHÒNG KINH DOANH 1 đã chia bộ phận Nhóm KD1-1 (2 / 400,000,000).',
       SUA + ['Đổi ô phòng PHÒNG KINH DOANH 1 sang PHÒNG KINH DOANH 2.', 'Bấm Hủy, rồi đổi lại và bấm Đồng ý.'], '',
       ['Hộp "Đổi phòng": "Đổi phòng? Các bộ phận đã chia sẽ bị bỏ.", 2 nút Hủy / Đồng ý',
        'Hủy: giữ phòng cũ và bộ phận', 'Đồng ý: đổi phòng, các dòng bộ phận bị bỏ']),
    nr('TC_04.008', 'Sửa xong bấm Quay lại khi chưa lưu', 'P1', 'Giống TC_04.007', SUA + ['Đổi một ô Doanh số.', 'Bấm Quay lại.', 'Bấm Ở lại; bấm Quay lại lần nữa, bấm Thoát.'], '',
       ['Hiện hộp "Thông tin chưa lưu", 2 nút Ở lại / Thoát', 'Ở lại: vẫn ở màn Sửa, số vừa gõ còn nguyên',
        'Thoát: về danh sách, phiếu không đổi']),
    nr('TC_04.009', 'Không sửa gì bấm Quay lại thì không hỏi', 'P2', 'Giống TC_04.007', SUA + ['Không đổi gì, bấm Quay lại.'], '',
       ['Về danh sách ngay, không hiện hộp "Thông tin chưa lưu"']),
    nr('TC_04.010', 'Mở đường link Sửa của phiếu không còn Đang tạo', 'P1', ACC_A + '\n' + PENDING,
       ['Đang ở màn Sửa P1 thì A2 (tab khác) gửi duyệt P1; hoặc mở lại link màn Sửa của P1 đã lưu từ trước.'], '',
       ['Mở link: hệ thống tự chuyển sang màn Chi tiết P1, không cho sửa',
        'Đang mở màn Sửa mà phiếu đã đổi trạng thái thì bấm Lưu bị chặn, báo phiếu không còn sửa được, dữ liệu không bị ghi']),
    nr('TC_04.011', 'Phiếu bị Từ chối sửa lại rồi gửi duyệt lại', 'P0', ACC_A + '\nP1 vừa bị D Từ chối (lý do "Sai số liệu"), về Đang tạo.',
       SUA + ['Sửa Doanh số theo yêu cầu.', 'Bấm Lưu và gửi.'], '',
       ['P1 có nút Sửa trở lại', 'Lưu và gửi thành công, P1 chuyển Chờ duyệt; lịch sử có dòng Thay đổi trạng thái Đang tạo sang Chờ duyệt']),
]

# ───────────── IV. GỬI DUYỆT ─────────────
G_GD = [keep('TC_05.%03d' % i) for i in range(1, 5)] + [
    nr('TC_05.005', 'Gửi duyệt từ danh sách', 'P0', ACC_A + '\n' + DRAFT, [MENU, 'Ở phiếu P1 mở menu ⋮, bấm Gửi duyệt.', 'Bấm Gửi duyệt trong hộp xác nhận.'], '',
       ['Hộp "Gửi duyệt": "Gửi duyệt phiếu TPE_CTKD_2027.000NN?", 2 nút Hủy / Gửi duyệt',
        'P1 chuyển Chờ duyệt, mất nút Sửa; người có quyền Duyệt nhận thông báo']),
]

# ───────────── V. DUYỆT / TỪ CHỐI / HỦY DUYỆT / HỦY PHIẾU ─────────────
G_DUYET = [
    nr('TC_06.003', 'Duyệt phiếu', 'P0', ACC_D + '\n' + PENDING, [MENU_CD, 'Ở phiếu P1 bấm ⋮ > Duyệt (mở màn Chi tiết).', 'Bấm Duyệt, bấm Duyệt trong hộp xác nhận.'], '',
       ['Hộp "Duyệt phiếu": "Duyệt phiếu TPE_CTKD_2027.000NN? Phiếu đã duyệt không sửa được.", 2 nút Hủy / Duyệt',
        'P1 chuyển Đã duyệt, về danh sách; Người duyệt = D, có Ngày duyệt; người lập nhận thông báo']),
] + [keep(t) for t in ['TC_06.001', 'TC_06.002', 'TC_07.001', 'TC_07.002', 'TC_08.001']]

G_LS = [keep('TC_09.%03d' % i) for i in range(1, 4)]
G_CT = [keep(t) for t in ['TC_10.001', 'TC_10.002', 'TC_10.010', 'TC_10.011']]
G_IN = [keep('TC_11.003')]
G_RB = [keep('TC_14.001')]

# ───────────── X. PHÂN QUYỀN — chức năng nào cần quyền nào ─────────────
NOQ = 'Tài khoản N không có quyền nào của màn.'
G_PQ = [
    nr('TC_15.002', 'Tạo mới cần quyền ' + Q_CREATE, 'P0', NOQ + '\nTài khoản A chỉ có quyền ' + Q_CREATE + '.',
       ['Đăng nhập N, ' + MENU[0].lower() + MENU[1:], 'Đăng nhập A, vào lại màn.'], '',
       ['N: không có nút Tạo mới', 'A: có nút Tạo mới, lập và lưu phiếu được']),
    nr('TC_15.003', 'Sửa / Gửi duyệt / Hủy phiếu cần quyền ' + Q_CREATE + ' và là người lập', 'P0',
       ACC_A + '\nTài khoản A2 cũng có quyền ' + Q_CREATE + '. P1 (Đang tạo) và P2 (Chờ duyệt) do A lập.', ['Đăng nhập A2.', MENU, 'Mở ⋮ của phiếu P2 (P1 Đang tạo không hiện với A2).'], '',
       ['A2 không thấy P1; ở P2 không có Sửa, Gửi duyệt, Hủy phiếu',
        'Đăng nhập A: P1 có Sửa, Gửi duyệt, Hủy phiếu; P2 có Hủy phiếu']),
    nr('TC_15.004', 'Duyệt / Từ chối / Hủy duyệt cần quyền ' + Q_APPROVE, 'P0',
       ACC_D + '\nTài khoản A chỉ có quyền ' + Q_CREATE + '. Có P2 Chờ duyệt, P3 Đã duyệt của TPE.', ['Đăng nhập D, mở ⋮ của P2, P3.', 'Đăng nhập A, mở ⋮ của P2, P3.'], '',
       ['D: P2 có Duyệt, Từ chối; P3 có Hủy duyệt; có mục menu "Giao chỉ tiêu chờ duyệt"',
        'A: không có Duyệt, Từ chối, Hủy duyệt; không có mục menu "Giao chỉ tiêu chờ duyệt"']),
    keep('TC_15.001'),
    nr('TC_15.005', 'Quyền Duyệt chỉ áp dụng cho phiếu của công ty đang làm việc', 'P0',
       ACC_D + '\nCó phiếu Chờ duyệt của TPE và của TPSG; D có quyền Xem mức Tổng công ty.', [MENU, 'Mở ⋮ của phiếu Chờ duyệt TPSG.', 'Đổi công ty đang làm việc sang TPSG, mở lại.'], '',
       ['Đang ở TPE: phiếu TPSG không có Duyệt / Từ chối', 'Sau khi đổi sang TPSG: phiếu TPSG có Duyệt / Từ chối, phiếu TPE thì không']),
    nr('TC_15.006', 'Quyền ' + Q_VIEW + ' mức Tổng công ty', 'P0', 'Tài khoản V2 có quyền ' + Q_VIEW + ' mức Tổng công ty, đang làm việc ở TPE.', ['Đăng nhập V2.', MENU, 'Mở Tìm kiếm nâng cao.'], '',
       ['Thấy phiếu của mọi công ty (trừ phiếu Đang tạo của người khác)', 'Có ô lọc Công ty']),
    nr('TC_15.007', 'Quyền ' + Q_VIEW + ' mức Công ty', 'P0', 'Tài khoản V có quyền ' + Q_VIEW + ' mức Công ty, đang làm việc ở TPE.', ['Đăng nhập V.', MENU], '',
       ['Chỉ thấy phiếu của TPE (trừ phiếu Đang tạo của người khác); không có ô lọc Công ty',
        'Đổi công ty đang làm việc sang TPSG thì danh sách chuyển sang phiếu của TPSG']),
    nr('TC_15.008', 'Không có quyền ' + Q_VIEW, 'P0', ACC_A + '\nA đã lập P1, P2; công ty TPE có 5 phiếu.', ['Đăng nhập A (không có quyền Xem).', MENU], '',
       ['Chỉ thấy phiếu A lập (và phiếu A đã duyệt nếu có)', 'Người có quyền Duyệt (không có quyền Xem) thấy thêm phiếu Chờ duyệt của công ty đang làm việc']),
    nr('TC_15.009', 'In / Xuất Excel / Lịch sử: ai xem được phiếu là dùng được', 'P1', 'Giống TC_15.008',
       [MENU, 'Mở ⋮ của phiếu Đã duyệt và phiếu Hủy.'], '',
       ['Phiếu Đã duyệt: có In, Xuất Excel, Lịch sử (không cần quyền riêng)', 'Phiếu Hủy: chỉ còn Lịch sử, không có In / Xuất Excel',
        'Nút Xuất Excel danh sách có với mọi người vào được màn']),
    nr('TC_15.010', 'Mở đường link phiếu không có quyền xem', 'P1', NOQ + '\nPhiếu TPE_CTKD_2026.00009 không do N lập / duyệt.',
       ['Đăng nhập N, dán đường link màn Chi tiết của TPE_CTKD_2026.00009 vào thanh địa chỉ.'], '',
       ['Không hiện dữ liệu phiếu, hệ thống đưa về danh sách']),
]

SEC = [
    ('HIỂN THỊ & TRUY CẬP', 'Hiển thị & truy cập', G_HT),
    ('THÊM MỚI', 'Thêm mới', G_TM),
    ('CHỈNH SỬA', 'Chỉnh sửa', G_SUA),
    ('GỬI DUYỆT', 'Gửi duyệt', G_GD),
    ('DUYỆT / TỪ CHỐI / HỦY DUYỆT / HỦY PHIẾU', 'Duyệt / Từ chối / Hủy duyệt / Hủy phiếu', G_DUYET),
    ('LỊCH SỬ THAY ĐỔI', 'Lịch sử thay đổi', G_LS),
    ('XEM CHI TIẾT PHIẾU', 'Xem chi tiết phiếu', G_CT),
    ('IN PHIẾU', 'In phiếu', G_IN),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', 'Ràng buộc với các chức năng khác', G_RB),
    ('PHÂN QUYỀN', 'Phân quyền', G_PQ),
]

DESC = [
    ('1. Mục đích', 'Giao chỉ tiêu kinh doanh năm (SL khách, Doanh số; tách Khách hãng / Khách khác, Hàng hóa / Dịch vụ) cho từng phòng ban, '
                    'tuỳ chọn tới bộ phận, theo Khối kinh doanh > Khu vực > Tỉnh/TP.\nTask #11643: bỏ chọn chi tiết khách hàng, nhập thẳng SL và Doanh số.'),
    ('2. Đường dẫn', 'Phân hệ Bán hàng > Kế hoạch > Giao chỉ tiêu kinh doanh > Theo phòng ban (Danh sách, Tạo, Sửa, Chi tiết).\n'
                     'Lối vào duyệt: Bán hàng > Phê Duyệt > Kế hoạch & chỉ tiêu > Giao chỉ tiêu chờ duyệt.'),
    ('3. Phạm vi dữ liệu', 'Phòng / bộ phận lấy từ Phiếu phân chia thị trường theo phòng ban ĐÃ DUYỆT tại từng Tỉnh/TP; Tỉnh/TP lấy theo Khu vực đã chọn.\n'
                           'Danh sách theo quyền Xem; phiếu Đang tạo chỉ người lập thấy.'),
    ('4. Danh sách', 'Tìm nhanh theo số phiếu; lọc Năm, Người tạo, Người duyệt, Trạng thái (Công ty nếu xem Tổng công ty); sắp xếp theo cột.\n'
                     'Bấm số phiếu mở Chi tiết; Cấu hình cột; menu ⋮ chứa các thao tác.'),
    ('5. Chức năng chính', 'Tạo mới (Lưu, Lưu và gửi), Sửa, Gửi duyệt, Duyệt, Từ chối, Hủy duyệt, Hủy phiếu.\n'
                           'Dòng phòng / bộ phận có 8 ô nhập SL khách, Doanh số (VNĐ); Tổng cộng, dòng Tỉnh/TP, TỔNG tự tính.'),
    ('6. Quy tắc nghiệp vụ', 'Bắt buộc Năm, Khối kinh doanh, Khu vực; mỗi công ty 1 phiếu còn hiệu lực / năm (ô Năm ẩn năm đã có phiếu). SL khách số nguyên, '
                             'Doanh số tối đa 2 số lẻ, tối đa 13 chữ số.\nGửi duyệt: phải có doanh số, có SL khách thì phải có Doanh số và ngược lại.'),
    ('7. Luồng trạng thái', 'Đang tạo > Chờ duyệt (Gửi duyệt) > Đã duyệt (Duyệt). Từ chối, Hủy duyệt đưa về Đang tạo (bắt buộc lý do).\n'
                            'Hủy phiếu (Đang tạo / Chờ duyệt, bắt buộc lý do) chuyển Hủy. Chỉ phiếu Đang tạo sửa được.'),
    ('8. Phân quyền', Q_CREATE + ': Tạo mới; Sửa, Gửi duyệt, Hủy phiếu của mình. ' + Q_APPROVE + ': Duyệt, Từ chối, Hủy duyệt phiếu công ty đang làm việc.\n'
                      + Q_VIEW + ' mức Tổng công ty / Công ty; không có quyền Xem chỉ thấy phiếu mình lập / mình duyệt. In, Xuất Excel, Lịch sử: ai xem được phiếu.'),
    ('9. Ảnh hưởng dữ liệu', 'Phiếu Đã duyệt là nguồn chỉ tiêu của Phiếu giao chỉ tiêu theo nhân viên và dòng "Năm trước" của phiếu năm sau.\n'
                             'Gửi duyệt / Duyệt / Từ chối / Hủy duyệt gửi thông báo; có phiếu theo nhân viên đang dùng thì không Hủy duyệt được.'),
    ('10. Chức năng bổ trợ', 'In phiếu; Xuất Excel danh sách và từng phiếu; Lịch sử thay đổi (chuyển trạng thái kèm lý do, Sửa chỉ ghi phần đổi).\n'
                             'Popup danh sách khu vực kinh doanh / phòng được chia; ⓘ giải thích tiêu đề cột; khối thống kê toàn phiếu.'),
]
assert len(DESC) == 10


def apply_same_pre(all_rows):
    """Tiền điều kiện trùng case ngay trước → "Giống TC_<case đầu tiên có tiền điều kiện đó>"."""
    origin_of = {}
    prev_text = None
    for r in all_rows:
        t = r[5]
        if t.startswith('Giống TC_'):
            prev_text = None
            continue
        if prev_text is not None and t == prev_text:
            r[5] = 'Giống ' + origin_of[t]
        else:
            origin_of[t] = r[2]
            prev_text = t


def build():
    allr = [r for _, _, g in SEC for r in g]
    apply_same_pre(allr)
    ids = [r[2] for r in allr]
    assert len(ids) == len(set(ids)), 'trùng ID'
    assert set(CUR) <= set(ids), set(CUR) - set(ids)
    wb = Workbook()
    ws = wb.active
    ws.title = 'Trang tính1'
    TNR = v2.TNR
    for k, v in v2.WIDTHS.items():
        ws.column_dimensions[k].width = v
    wrap = Alignment(wrap_text=True, vertical='center')
    wrapc = Alignment(wrap_text=True, vertical='center', horizontal='center')
    fill = v2.fill
    ws['A1'] = 'MÔ TẢ CHỨC NĂNG'
    ws['A1'].font = Font(name=TNR, size=12, bold=True)
    ws.merge_cells('A1:I1')
    for i, (k, v) in enumerate(DESC):
        r = 2 + i
        ws.cell(r, 1, k).font = Font(name=TNR, size=12, bold=True)
        ws.cell(r, 1).alignment = wrap
        ws.cell(r, 2, v).font = Font(name=TNR, size=12)
        ws.cell(r, 2).alignment = wrap
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=10)
    ws['A12'] = v2.TITLE
    ws['A12'].font = Font(name=TNR, size=15, bold=True, color='4A86E8')
    ws['A12'].alignment = wrapc
    ws.merge_cells('A12:E16')
    ws['F12'] = 'TEST SUMMARY'
    ws['F12'].font = Font(name=TNR, size=11, bold=True, color='FFFFFF')
    ws['F12'].alignment = wrapc
    for r in range(12, 18):
        for c in 'FGH':
            ws[f'{c}{r}'].fill = fill('4472C4')
    ws.merge_cells('F12:H17')
    L = 400
    dns = [('Số trường hợp DNS kiểm thử đạt (P):', f'=COUNTIFS(L20:L{L},"Passed")+COUNTIFS(K20:K{L},"Passed",L20:L{L},"")'),
           ('Số trường hợp DNS kiểm thử không đạt (F)', f'=COUNTIFS(L20:L{L},"Failed")+COUNTIFS(K20:K{L},"Failed",L20:L{L},"")'),
           ('Số trường hợp DNS kiểm thử đang xem xét (PE)', f'=COUNTIFS(L20:L{L},"Pending")+COUNTIFS(K20:K{L},"Pending",L20:L{L},"")'),
           ('Số trường hợp DNS kiểm thử chưa thực hiện', '=K17-K16'),
           ('Tổng số trường hợp DNS kiểm thử', '=SUM(K12:L14)'),
           ('Tổng số testcase', f'=COUNTIF(C20:C{L},"TC_*")')]
    tp = [('Số trường hợp TP kiểm thử đạt (P):', f'=COUNTIF(Q20:Q{L},"P")'),
          ('Số trường hợp TP kiểm thử không đạt (F)', f'=COUNTIF(Q20:Q{L},"F")'),
          ('Số trường hợp TP kiểm thử đang xem xét (PE)', f'=COUNTIF(Q20:Q{L},"PE")'),
          ('Số trường hợp TP kiểm thử chưa thực hiện', '=K17-P16'),
          ('Tổng số trường hợp TP đã kiểm thử', '=SUM(P12:Q14)')]
    for i, (lab, f) in enumerate(dns):
        r = 12 + i
        ws.cell(r, 9, lab).font = Font(name=TNR, size=11)
        ws.cell(r, 11, f).font = Font(name=TNR, size=11, bold=True)
        ws.cell(r, 9).alignment = wrap
        ws.cell(r, 11).alignment = wrapc
        for c in (9, 10, 11, 12):
            ws.cell(r, c).fill = fill('00FF00')
        ws.merge_cells(start_row=r, start_column=9, end_row=r, end_column=10)
        ws.merge_cells(start_row=r, start_column=11, end_row=r, end_column=12)
    for i, (lab, f) in enumerate(tp):
        r = 12 + i
        ws.cell(r, 13, lab).font = Font(name=TNR, size=11)
        ws.cell(r, 16, f).font = Font(name=TNR, size=11, bold=True)
        ws.cell(r, 13).alignment = wrap
        ws.cell(r, 16).alignment = wrapc
        ws.merge_cells(start_row=r, start_column=13, end_row=r, end_column=15)
        ws.merge_cells(start_row=r, start_column=16, end_row=r, end_column=17)
    ws.merge_cells('A18:I18')
    for c, h in enumerate(v2.HEAD, 1):
        cell = ws.cell(19, c, h)
        cell.font = Font(name=TNR, size=12, bold=True)
        cell.fill = fill('FF9900')
        cell.alignment = wrapc
    r = 20
    for gi, (gname, bname, grows) in enumerate(SEC):
        ws.cell(r, 3, '%s. %s' % (v2.ROMAN[gi], gname))
        for c in range(1, 19):
            ws.cell(r, c).fill = fill('D6E4F0')
            ws.cell(r, c).font = Font(name=TNR, size=12, bold=True, color='1F4E79')
            ws.cell(r, c).alignment = Alignment(vertical='center')
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=13)
        r += 1
        first = r
        for row in grows:
            row = list(row)
            row[0] = v2.MODULE if r == first else None
            row[1] = bname if r == first else None
            for c in range(1, 19):
                v = row[c - 1]
                cell = ws.cell(r, c, v if v != '' else None)
                cell.font = Font(name=TNR, size=12)
                cell.alignment = wrapc if c in (3, 5, 11, 12, 17) else wrap
            ws.cell(r, 17, f'=IF(P{r}<>"",P{r},IF(O{r}<>"",O{r},IF(N{r}<>"",N{r},"")))')
            r += 1
        ws.merge_cells(start_row=first, start_column=1, end_row=r - 1, end_column=1)
        ws.merge_cells(start_row=first, start_column=2, end_row=r - 1, end_column=2)
    last = r - 1
    dv1 = DataValidation(type='list', formula1='"Passed,Failed,Pending,Not Executed"', allow_blank=True)
    dv2 = DataValidation(type='list', formula1='"P,F,PE"', allow_blank=True)
    ws.add_data_validation(dv1)
    ws.add_data_validation(dv2)
    dv1.add(f'K21:L{last}')
    dv2.add(f'N21:P{last}')
    wb.save(OUT)
    return allr, last


if __name__ == '__main__':
    allr, last = build()
    newc = [r for r in allr if r[2] not in CUR]
    same = sum(1 for r in allr if r[5].startswith('Giống TC_'))
    print('Tổng %d case (giữ %d, mới %d), %d tiền điều kiện ghi "Giống TC_...", dòng cuối %d'
          % (len(allr), len(CUR), len(newc), same, last))
    for gi, (g, _, rws) in enumerate(SEC):
        print('  %s. %s: %d' % (v2.ROMAN[gi], g, len(rws)))
    print(OUT)

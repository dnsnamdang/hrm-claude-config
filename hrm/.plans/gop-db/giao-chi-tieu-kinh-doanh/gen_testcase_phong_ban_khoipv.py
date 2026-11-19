# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu giao chỉ tiêu kinh doanh theo phòng ban" (Redmine #11643) — skill testcase-documenter,
KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu').

Chạy: python gen_testcase_phong_ban_khoipv.py -> "testcase - Phiếu giao chỉ tiêu KD theo phòng ban.xlsx" (tự chạy check_tc, 0 lỗi).
Trọng tâm #11643: bỏ phần chọn chi tiết khách hàng (popup "Thêm / Xem Khách Hàng", "Khách hàng mới") -> nhập thẳng 8 ô
SL khách / Doanh số trên dòng phòng ban (thêm cấp Bộ phận tuỳ chọn).
Nguồn hành vi (đọc 19/11/2026, nhánh develop cả 2 repo): FE pages/finance/business-target-departments/**,
components/business-target/{BusinessTargetList,TargetTreeTable}.vue, utils/mixins/businessTargetActionsMixin.js,
utils/export/businessTargetExcel.js, components/subsystem-menu/sale-hub.js; BE Modules/Finance BusinessTargetDepartment
(Controller / Request / Service), Concerns/BusinessTargetTransitions, Entities/BusinessTarget/Concerns/HasBusinessTargetAccess,
quyền Catalog app/Support/Permissions/Catalog/sale.php.
Số liệu mẫu: DB local gop_db 19/11/2026 (9 phiếu Đã duyệt chuyển từ hệ thống cũ) — QA dựng lại nếu môi trường test khác.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets'))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from tc_chuan import build_chuan  # noqa: E402
from tc_phieu_bosung import ListScreen, filter_memory_cases, check_no_dash_pre  # noqa: E402

OUT = os.path.join(HERE, 'testcase - Phiếu giao chỉ tiêu KD theo phòng ban.xlsx')

# ───────────────────────────── Hằng dùng chung ─────────────────────────────
MENU = 'Vào phân hệ Bán hàng > nhóm "Kế hoạch" > "Giao chỉ tiêu kinh doanh" > bấm "Theo phòng ban".'
MENU_CD = 'Vào phân hệ Bán hàng > nhóm "Phê Duyệt" > "Kế hoạch & chỉ tiêu" > bấm "Giao chỉ tiêu chờ duyệt".'
ADV = 'Bấm Tìm kiếm nâng cao.'
REQ = '"Bắt buộc phải nhập"'
CHECK = '"Vui lòng kiểm tra lại dữ liệu nhập"'
EMPTY = '"Không có phiếu giao chỉ tiêu nào"'
LIST_TITLE = 'Danh sách phiếu giao chỉ tiêu kinh doanh theo phòng ban'
STALE = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'
UNSAVED = 'cửa sổ "Thông tin chưa lưu" với câu "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?", 2 nút Ở lại / Thoát'

Q_VIEW = '"Xem chỉ tiêu"'
Q_CREATE = '"Tạo chỉ tiêu kinh doanh theo phòng ban"'
Q_APPROVE = '"Duyệt chỉ tiêu kinh doanh theo phòng ban"'

OLD9 = ('Hệ thống có sẵn 9 phiếu Đã duyệt chuyển từ hệ thống cũ: TPE_CTKD_2024, TPE_CTKD_2025.00003, TPV_CTKD_2025.00004, '
        'TPHP_CTKD_2025.00005, TPSG_CTKD_2025.00006, TPE_CTKD_2026.00008, TPV_CTKD_2026.00009, TPHP_CTKD_2026.00010, '
        'TPSG_CTKD_2026.00011.')
ACC_V4 = 'Tài khoản V4: Vai trò cấp quyền ' + Q_VIEW + ' mức Tổng công ty (không có quyền Tạo, Duyệt).'
ACC_V3 = ('Tài khoản V3: Vai trò cấp quyền ' + Q_VIEW + ' mức Công ty, đang làm việc ở công ty TPSG (CÔNG TY TNHH THIẾT BỊ '
          'TÂN PHÁT SÀI GÒN).')
ACC_A = ('Tài khoản A (người lập): có quyền ' + Q_CREATE + ', không có quyền Xem, đang làm việc ở công ty TPE (CÔNG TY CỔ '
         'PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT).')
ACC_D = 'Tài khoản D (người duyệt): có quyền ' + Q_APPROVE + ', đang làm việc ở công ty TPE.'
ACC_N = 'Tài khoản N: không có quyền nào của màn, chưa lập phiếu nào.'
PRE_LIST = ACC_V4 + '\n' + OLD9

CAT = ('Danh mục công ty TPE: 3 khối kinh doanh "Nghiệp vụ", "Kinh doanh", "Chi nhánh/Đơn vị thành viên"; khối "Kinh doanh" có '
       'các phòng PHÒNG THIẾT BỊ Ô TÔ 1 (không có bộ phận), PHÒNG KINH DOANH THƯƠNG MẠI (3 bộ phận: "BP Thiết bị, vật tư, hóa '
       'chất chăm sóc xe", "BP Thiết bị, vật tư lốp", "Kinh doanh dự án"); khu vực "Đồng bằng sông Hồng" có Thành phố Hà Nội.')
NO2027 = 'Công ty TPE chưa có phiếu nào cho năm 2027.'
PRE_NEW = ACC_A + '\n' + CAT + '\n' + NO2027
TAO = [MENU, 'Bấm "Tạo mới".']
TAO_KD = TAO + ['Chọn Năm = Năm 2027.', 'Chọn Khối kinh doanh = Kinh doanh.', 'Chọn Khu vực = Đồng bằng sông Hồng.']
HN_OTO1 = 'Ở Tỉnh/TP "Thành phố Hà Nội", dòng phòng 1 chọn PHÒNG THIẾT BỊ Ô TÔ 1.'

DRAFT = ('Phiếu TPE_CTKD_2027.000NN do A lập, trạng thái Đang tạo: Năm 2027, khối Kinh doanh, khu vực Đồng bằng sông Hồng; '
         'Thành phố Hà Nội có PHÒNG THIẾT BỊ Ô TÔ 1 với Khách hãng / Hàng hóa: SL khách 4, Doanh số 15,000,000,000.')
PRE_EDIT = ACC_A + '\n' + CAT + '\n' + DRAFT
SUA = [MENU, 'Ở dòng phiếu TPE_CTKD_2027.000NN bấm Sửa (biểu tượng bút chì).']
PENDING = DRAFT.replace('trạng thái Đang tạo', 'trạng thái Chờ duyệt (A đã gửi duyệt)')
APPROVED = DRAFT.replace('trạng thái Đang tạo', 'trạng thái Đã duyệt (D đã duyệt)')
XEM_CD = [MENU_CD, 'Bấm số phiếu TPE_CTKD_2027.000NN.']

OLD8 = ('Phiếu TPE_CTKD_2026.00008 (Đã duyệt, khối Kinh doanh, 34 Tỉnh/TP; được lập ở hệ thống cũ CÓ danh sách chi tiết '
        'khách hàng): Thành phố Hà Nội có Khách hãng / Hàng hóa SL khách 13, Doanh số 23,762,500,000; trong đó PHÒNG THIẾT BỊ Ô TÔ 1 '
        'SL khách 4, Doanh số 15,000,000,000; PHÒNG DỰ ÁN SL khách 3, Doanh số 5,262,500,000; PHÒNG THIẾT BỊ Ô TÔ 2 SL khách 6, '
        'Doanh số 3,500,000,000.')

CK = []


def T(no, func, prio, pre, steps, td, exp):
    if isinstance(pre, (list, tuple)):
        pre = '\n'.join(pre)
    if isinstance(td, (list, tuple)):
        td = '\n'.join(td)
    st = '\n'.join('%d. %s' % (i + 1, s) for i, s in enumerate(steps))
    ex = '\n'.join(x if x.startswith('- ') else '- ' + x for x in exp)
    return ('%03d' % no, func, prio, pre, st, td, ex)


class Sec(list):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx

    def add(self, func, prio, pre, steps, td, exp):
        self.append(T(len(self) + 1, func, prio, pre, steps, td, exp))

    def raw(self, tcs):
        for tc in tcs:
            self.append(('%03d' % (len(self) + 1),) + tuple(tc[1:]))


# ───────────────────────────── Mô tả 9 mục ─────────────────────────────
DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Phiếu giao chỉ tiêu kinh doanh theo phòng ban (số phiếu dạng <mã công ty>_CTKD_<năm>.<5 số>) dùng để công ty giao chỉ tiêu '
     'năm cho từng phòng ban (và tuỳ chọn tới từng bộ phận) theo Khối kinh doanh > Khu vực > Tỉnh/TP.\n'
     'Thay đổi của task #11643: BỎ phần chọn chi tiết khách hàng (cửa sổ "Thêm / Xem Khách Hàng", dòng "Khách hàng mới") — người '
     'dùng NHẬP THẲNG SL khách và Doanh số vào 8 ô số trên dòng phòng ban / bộ phận; thêm cấp Bộ phận (Chia Bộ Phận) và luồng '
     'Gửi duyệt / Duyệt / Từ chối / Hủy duyệt / Hủy phiếu.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Danh sách: phiếu trong phạm vi xem (xem mục 7).\n'
     '- 4 trạng thái: Đang tạo (xám), Chờ duyệt (cam), Đã duyệt (xanh lá), Hủy (đỏ nhạt).\n'
     '- Lối vào "Giao chỉ tiêu chờ duyệt": chỉ phiếu Chờ duyệt của công ty đang làm việc, chỉ hiện với người có quyền Duyệt.\n'
     '- Bảng chi tiết: 12 cột số — Khách hãng (Hàng hóa: SL khách, Doanh số · Dịch vụ: SL khách, Doanh số), Khách khác (4 cột '
     'tương tự), Tổng cộng (4 cột = Khách hãng + Khách khác); các dòng TỔNG, Tỉnh/TP, Năm trước, Phòng ban, Bộ phận.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác luôn bị ẩn (kể cả với người có quyền Xem mức Tổng công ty).\n'
     '- Phiếu ngoài phạm vi: không có trong danh sách; mở đường link thì bị đưa về danh sách.\n'
     '- Ô chọn Phòng ban chỉ có phòng thuộc khối đang mở, đang hoạt động, chưa chọn ở cùng Tỉnh/TP; ô Bộ phận chỉ có bộ phận của '
     'phòng, đang hoạt động, chưa chọn.\n'
     '- Dòng phòng / bộ phận để trống hoàn toàn (không chọn, không số) bị bỏ khi lưu.\n'
     '- Phiếu Hủy không tính vào "Năm trước", không chặn tạo phiếu mới cùng năm, không có In / Xuất Excel.\n'
     '- Màn KHÔNG có Xóa phiếu, Khóa / Mở khóa, Import.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     '- Ô lọc Năm lọc theo Năm của phiếu (lựa chọn từ năm hiện tại + 2 lùi về 2023).\n'
     '- Dòng "Năm trước" lấy từ phiếu ĐÃ DUYỆT của năm liền trước, cùng công ty, cùng khối.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Phiếu (1 công ty, 1 năm) > Khối kinh doanh (mỗi khối 1 tab + tab Tổng hợp) > Khu vực (chọn nhiều, tự bung Tỉnh/TP) > '
     'Tỉnh/TP > Phòng ban > Bộ phận (tuỳ chọn).\n'
     '- Ô "Hiển thị đến cấp": Chỉ Tỉnh/TP / Đến Phòng ban / Đến Bộ phận (mặc định Đến Bộ phận - mở hết).'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Phòng đã chia bộ phận: 8 số của phòng = tổng các bộ phận (ô phòng chỉ đọc).\n'
     '- Tỉnh/TP = tổng các phòng; TỔNG của khối = tổng các Tỉnh/TP; Tổng cộng = Khách hãng + Khách khác.\n'
     '- Tab Tổng hợp: mỗi Tỉnh/TP = tổng các khối; Năm trước = tổng Năm trước các khối.\n'
     '- Một công ty chỉ có 1 phiếu hiệu lực (khác Hủy) cho mỗi năm.\n'
     '- Không chọn trùng phòng trong cùng Tỉnh/TP, không chọn trùng bộ phận trong cùng phòng.'),
    ('7. Phân quyền cấp',
     '- ' + Q_VIEW + ' — mức: Tổng công ty (mọi phiếu, có ô lọc Công ty) / Công ty (phiếu của công ty đang làm việc).\n'
     '- ' + Q_CREATE + ': nút Tạo mới; Sửa, Gửi duyệt, Hủy phiếu trên phiếu CỦA MÌNH.\n'
     '- ' + Q_APPROVE + ': Duyệt / Từ chối phiếu Chờ duyệt, Hủy duyệt phiếu Đã duyệt — chỉ phiếu của công ty đang làm việc; có '
     'mục menu "Giao chỉ tiêu chờ duyệt".\n'
     '- Không có quyền Xem: chỉ thấy phiếu mình lập và phiếu mình đã duyệt. Không có đặc cách Super admin.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là khoảng STT trang đang xem, N là tổng phiếu khớp bộ lọc trong phạm vi xem.\n'
     '- Dòng TỔNG của khối ghi "x Tỉnh/TP · y phòng · z bộ phận"; dòng Tỉnh/TP ghi "<tên> (y phòng)"; góc phải khối Chi tiết ghi '
     'tổng của cả phiếu.\n'
     '- Ô Năm trước của Tỉnh/TP = tổng số của Tỉnh/TP đó trong phiếu năm liền trước đã duyệt cùng khối.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: A (Tạo, công ty TPE), D (Duyệt, công ty TPE), V3 (Xem mức Công ty, TPSG), V4 (Xem mức Tổng '
     'công ty), N (không quyền).\n'
     '- Số tiền / số lượng hiển thị có dấu phẩy ngăn hàng nghìn (15,000,000,000); chỉ nhận số nguyên từ 0 trở lên, tối đa 13 chữ số.\n'
     '- Ô số bằng 0 ở dòng phòng / bộ phận / Tỉnh/TP để TRỐNG; riêng dòng TỔNG hiện 0.\n'
     '- Lưu ý: Lưu (nháp) KHÔNG bắt cặp SL khách / Doanh số; chỉ "Lưu và gửi" / "Gửi duyệt" mới bắt (có Doanh số thì phải có SL '
     'khách và ngược lại).\n'
     '- Lưu ý: "Lưu và gửi" bị chặn ở bước gửi thì phiếu KHÔNG được lưu (cả lần lưu bị huỷ).\n'
     '- Phiếu cũ lập ở hệ thống cũ (có danh sách khách hàng chi tiết) vẫn mở được, số hiện theo đúng số đã chốt.\n'
     '- Số phiếu mẫu "TPE_CTKD_2027.000NN": NN là số thứ tự hệ thống cấp khi lưu.'),
]

SCREEN = ListScreen(menu=MENU, title=LIST_TITLE, total=9, quick_label='số phiếu', quick_sample='TPE_CTKD_2026',
                    quick_hit='phiếu TPE_CTKD_2026.00008', filters=[('Năm', '2026'), ('Công ty', 'TPE')])

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', PRE_LIST, ['Đăng nhập V4.', MENU], '—',
       ['Tiêu đề bảng "' + LIST_TITLE + '".', 'Mặc định 10 phiếu / trang; ô Số dòng/trang có các lựa chọn 5, 10, 20, 50, 100.',
        'Sắp xếp phiếu tạo mới nhất ở trên.', 'Dưới bảng ghi "Hiển thị 1–9 / 9".'])
S1.add('Mở lối vào "Giao chỉ tiêu chờ duyệt"', 'P0',
       [ACC_D, 'Công ty TPE có 2 phiếu Chờ duyệt (năm 2027 và 2028); công ty TPSG có 1 phiếu Chờ duyệt.'],
       ['Đăng nhập D.', MENU_CD], '—',
       ['Tiêu đề bảng "' + LIST_TITLE + ' chờ duyệt".', 'Chỉ có 2 phiếu Chờ duyệt của công ty TPE; KHÔNG có phiếu của TPSG.',
        'Không có nút Tạo mới, không có ô lọc Trạng thái.'])
S1.add('Mục menu chờ duyệt chỉ hiện với người có quyền Duyệt', 'P1', [ACC_A, ACC_D],
       ['Đăng nhập A, mở nhóm "Phê Duyệt" > "Kế hoạch & chỉ tiêu".', 'Đăng nhập D, mở lại nhóm đó.'], '—',
       ['A: KHÔNG thấy mục "Giao chỉ tiêu chờ duyệt".', 'D: thấy mục "Giao chỉ tiêu chờ duyệt".'])
S1.add('Đang ở danh sách chờ duyệt rồi mở lối vào thường', 'P1', [ACC_D, 'D tự lập 1 phiếu Đang tạo năm 2029.'],
       ['Đăng nhập D.', MENU_CD, MENU], '—',
       ['Bước 3: danh sách đổi theo lối vào mới — tiêu đề không còn chữ "chờ duyệt", có ô lọc Trạng thái, thấy cả phiếu Đang '
        'tạo năm 2029 của D.', 'Không giữ phạm vi chờ duyệt của lần trước.'])
S1.add('Sửa tay tham số chế độ trên thanh địa chỉ thành giá trị lạ', 'P2', [ACC_D],
       [MENU_CD, 'Sửa phần tham số chế độ trên thanh địa chỉ thành "abc", nhấn Enter.'], '—',
       ['Mở chế độ danh sách thường (như vào từ menu "Theo phòng ban").', 'Không báo lỗi, không lộ thêm phiếu ngoài phạm vi.'])
S1.add('Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát tiêu đề trang, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Tiêu đề bảng: "' + LIST_TITLE + '".'])
S1.add('Các nút chức năng được hiển thị', 'P0', [ACC_A, 'A đã lập 1 phiếu Đang tạo năm 2027.'],
       ['Đăng nhập A.', MENU, 'Quan sát khối bộ lọc, thanh công cụ, cột Hành động.'], '—',
       ['Bộ lọc: ô tìm nhanh (gợi ý "Tìm theo số phiếu"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao.',
        'Thanh công cụ: Tạo mới, Xuất Excel, nút biểu tượng cột (gợi ý "Cấu hình cột hiển thị").',
        'Dòng phiếu Đang tạo: Sửa (bút chì) + menu: Xem, Gửi duyệt, Hủy phiếu, In, Xuất Excel, Lịch sử.',
        'KHÔNG có nút Xóa phiếu.'])
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Hiện 9 cột: STT, Số phiếu, Công ty, Năm, Người tạo, Ngày tạo, Người duyệt, Trạng thái, Hành động.',
        'Cột Ngày duyệt ẩn mặc định (bật được ở cấu hình cột).'])
S1.add('Dữ liệu trên dòng khớp phiếu', 'P0', [PRE_LIST, OLD8], [MENU, 'Đối chiếu dòng TPE_CTKD_2026.00008.'], '—',
       ['Số phiếu là liên kết; Công ty "CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT"; Năm 2026.',
        'Người tạo, Người duyệt đúng người lập / người duyệt ở hệ thống cũ; nhãn xanh lá "Đã duyệt".'])
S1.add('Màu nhãn trạng thái', 'P1', [ACC_A, 'A có 4 phiếu: Đang tạo (2027), Chờ duyệt (2028), Đã duyệt (2029), Hủy (2030).'],
       ['Đăng nhập A.', MENU, 'Quan sát cột Trạng thái.'], '—',
       ['Đang tạo: xám; Chờ duyệt: cam; Đã duyệt: xanh lá; Hủy: đỏ nhạt.'])
S1.add('Danh sách chưa có dữ liệu', 'P1', ACC_N, ['Đăng nhập N.', MENU], '—',
       ['Bảng hiện ' + EMPTY + '.', 'Không có nút Tạo mới.', 'Không báo lỗi.'])
S1.add('Không có phiếu khớp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       ['Bảng hiện ' + EMPTY + '.', 'Không báo lỗi.'])
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Đổi Số dòng/trang thành 5.'], 'Số dòng/trang: 5',
       ['Bảng hiện 5 phiếu, "Hiển thị 1–5 / 9".', 'Có 2 trang.'])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Đổi Số dòng/trang = 5.', 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 3: "Hiển thị 6–9 / 9".', 'Bước 4: "Hiển thị 1–5 / 9".'])
S1.add('Trang đầu / trang cuối và trạng thái nút', 'P2', PRE_LIST, [MENU, 'Đổi Số dòng/trang = 5.', 'Bấm ».', 'Bấm «.'], '—',
       ['Ở trang 2: › và » mờ.', 'Ở trang 1: « và ‹ mờ.'])
S1.add('STT liên tục giữa các trang', 'P1', PRE_LIST, [MENU, 'Đổi Số dòng/trang = 5.', 'Sang trang 2.'], '—',
       ['Trang 2 có STT 6–9.'])
S1.add('Về trang 1 khi đổi bộ lọc', 'P1', PRE_LIST, [MENU, 'Đổi Số dòng/trang = 5, sang trang 2.', ADV, 'Chọn Năm = 2025.'],
       'Năm: 2025', ['Tự nạp lại ở trang 1; "Hiển thị 1–4 / 4".'])
S1.add('Sắp xếp tăng / giảm theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Số phiếu.', 'Bấm lần nữa.'], '—',
       ['Lần 1: tăng dần theo chữ (TPE_CTKD_2024 ở trên các phiếu TPE khác); mũi tên lên.', 'Lần 2: giảm dần; mũi tên xuống.'])
S1.add('Sắp xếp theo Năm', 'P1', PRE_LIST, [MENU, 'Bấm tiêu đề cột Năm.'], '—',
       ['TPE_CTKD_2024 lên đầu, sau đó 4 phiếu 2025, cuối là 4 phiếu 2026.'])
S1.add('Sắp xếp theo các cột còn lại', 'P2', PRE_LIST,
       [MENU, 'Lần lượt bấm tiêu đề Công ty, Người tạo, Ngày tạo, Người duyệt, Trạng thái.'], '—',
       ['Mỗi cột đều sắp xếp được, mũi tên đổi chiều mỗi lần bấm.', 'Cột STT, Hành động không sắp xếp.'])
S1.add('Giữ sắp xếp khi chuyển trang, về trang 1 khi đổi sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Đổi Số dòng/trang = 5, bấm Năm (tăng).', 'Sang trang 2.', 'Bấm tiêu đề Số phiếu.'], '—',
       ['Bước 2: trang 2 tiếp tục thứ tự Năm tăng.', 'Bước 3: về trang 1.'])
S1.add('Bấm sắp xếp không làm vỡ bố cục bảng', 'P2', PRE_LIST, [MENU, 'Bấm liên tục tiêu đề Năm, Số phiếu, Trạng thái.'], '—',
       ['Độ rộng các cột giữ nguyên, không nhảy bố cục.'])

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo số phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "TPE_CTKD_2026.00008", bấm Tìm kiếm.'],
       'Ô tìm nhanh: TPE_CTKD_2026.00008', ['Chỉ còn phiếu TPE_CTKD_2026.00008; "Hiển thị 1–1 / 1".'])
S2.add('Tìm theo một phần số phiếu', 'P0', PRE_LIST, [MENU, 'Nhập "2025", bấm Tìm kiếm.'], 'Ô tìm nhanh: 2025',
       ['Còn 4 phiếu có chữ 2025 trong số phiếu.'])
S2.add('Tìm không phân biệt hoa thường', 'P1', PRE_LIST, [MENU, 'Nhập "tpsg_ctkd", bấm Tìm kiếm.'], 'Ô tìm nhanh: tpsg_ctkd',
       ['Còn 2 phiếu TPSG_CTKD_2025.00006, TPSG_CTKD_2026.00011.'])
S2.add('Từ khoá có khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  TPV_CTKD  ", bấm Tìm kiếm.'], 'Ô tìm nhanh:   TPV_CTKD  ',
       ['Bỏ khoảng trắng, còn 2 phiếu TPV.'])
S2.add('Ký tự đặc biệt / từ khoá không tồn tại', 'P2', PRE_LIST, [MENU, 'Nhập "%_@#", bấm Tìm kiếm.'], 'Ô tìm nhanh: %_@#',
       ['Bảng hiện ' + EMPTY + ', không báo lỗi, màn không treo.'])
S2.add('Nhấn Enter để tìm và xoá từ khoá', 'P1', PRE_LIST, [MENU, 'Nhập "TPHP", nhấn Enter.', 'Xoá hết chữ, bấm Tìm kiếm.'],
       'Ô tìm nhanh: TPHP', ['Bước 2: còn 2 phiếu TPHP.', 'Bước 3: hiện lại đủ 9 phiếu.'])
S2.add('Độ dài ô tìm nhanh', 'P2', PRE_LIST, [MENU, 'Dán chuỗi 300 ký tự, bấm Tìm kiếm.'], 'Chuỗi 300 ký tự chữ và số',
       ['Ô nhận hết, không báo lỗi; bảng hiện ' + EMPTY + '.'])
S2.add('Các ô trong Tìm kiếm nâng cao', 'P0', PRE_LIST, [MENU, ADV], '—',
       ['Có các ô: Công ty, Năm, Người tạo, Người duyệt, Trạng thái.'])
S2.add('Lọc theo Công ty', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Công ty = CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT.'], 'Công ty: TPE',
       ['Còn 3 phiếu TPE_CTKD_2024, TPE_CTKD_2025.00003, TPE_CTKD_2026.00008.'])
S2.add('Ô Công ty không hiện với quyền Xem mức Công ty', 'P1', ACC_V3, ['Đăng nhập V3.', MENU, ADV], '—',
       ['KHÔNG có ô Công ty; vẫn có Năm, Người tạo, Người duyệt, Trạng thái.'])
S2.add('Lọc theo Năm', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Năm = 2026.'], 'Năm: 2026', ['Còn 4 phiếu năm 2026.'])
S2.add('Lựa chọn của ô Năm', 'P2', PRE_LIST, [MENU, ADV, 'Mở ô Năm.'], '—',
       ['Có các năm từ (năm hiện tại + 2) lùi về 2023, năm lớn ở trên.'])
S2.add('Lọc theo Người tạo / Người duyệt', 'P1', [PRE_LIST, 'Phiếu TPE_CTKD_2026.00008 do người P lập, người Q duyệt.'],
       [MENU, ADV, 'Chọn Người tạo = P.', 'Bỏ Người tạo, chọn Người duyệt = Q.'], 'Người tạo: P\nNgười duyệt: Q',
       ['Bước 3: chỉ còn phiếu do P lập.', 'Bước 4: chỉ còn phiếu do Q duyệt.'])
S2.add('Lọc theo Trạng thái', 'P0', [ACC_A, 'A có 4 phiếu: Đang tạo (2027), Chờ duyệt (2028), Đã duyệt (2029), Hủy (2030).'],
       ['Đăng nhập A.', MENU, ADV, 'Lần lượt chọn Trạng thái = Đang tạo, Chờ duyệt, Đã duyệt, Hủy.'], '—',
       ['Mỗi lần chỉ còn 1 phiếu đúng trạng thái.', 'Ô Trạng thái có đủ 4 lựa chọn Đang tạo, Chờ duyệt, Đã duyệt, Hủy.'])
S2.add('Kết hợp tìm nhanh với ô lọc', 'P0', PRE_LIST, [MENU, 'Nhập "TPE", bấm Tìm kiếm.', ADV, 'Chọn Năm = 2025.'],
       'Từ khoá: TPE\nNăm: 2025', ['Chỉ còn TPE_CTKD_2025.00003.'])
S2.add('Kết hợp nhiều ô lọc', 'P1', PRE_LIST, [MENU, ADV, 'Chọn Công ty = TPSG.', 'Chọn Năm = 2026.', 'Chọn Trạng thái = Đang tạo.'],
       'Công ty: TPSG\nNăm: 2026\nTrạng thái: Đang tạo',
       ['Bước 4: chỉ còn TPSG_CTKD_2026.00011.', 'Bước 5: bảng hiện ' + EMPTY + '.'])
S2.add('Bấm Làm mới', 'P0', PRE_LIST, [MENU, 'Nhập "TPE", chọn Năm = 2025.', 'Bấm Làm mới.'], '—',
       ['Xoá từ khoá và mọi ô lọc, hiện lại 9 phiếu, về trang 1.'])
S2.add('Làm mới ở lối vào chờ duyệt giữ nguyên phạm vi', 'P1', [ACC_D, 'Công ty TPE có 2 phiếu Chờ duyệt (2027, 2028).'],
       [MENU_CD, ADV, 'Chọn Năm = 2027.', 'Bấm Làm mới.'], '—',
       ['Sau Làm mới vẫn là danh sách chờ duyệt (2 phiếu), không chuyển sang danh sách thường.'])
S2.raw(filter_memory_cases(SCREEN, 1))

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Mở màn Tạo mới', 'P0', PRE_NEW, ['Đăng nhập A.', MENU, 'Bấm "Tạo mới".'], '—',
       ['Trang "Tạo phiếu giao chỉ tiêu kinh doanh theo phòng ban".',
        'Khối "Thông tin phiếu": Số phiếu khoá, gợi ý "Số phiếu tự sinh khi lưu"; Năm (bắt buộc) mặc định năm hiện tại; Khối kinh '
        'doanh (bắt buộc, chọn nhiều, gợi ý "Chọn khối kinh doanh").',
        'Khối "Chi tiết" ghi "Chưa có dữ liệu".', 'Dưới trang: Quay lại, Lưu, Lưu và gửi.'])
S3.add('KHÔNG còn phần chọn chi tiết khách hàng', 'P0', PRE_NEW, TAO_KD + [HN_OTO1, 'Quan sát dòng phòng và toàn trang.'], '—',
       ['Không có nút / liên kết "Thêm / Xem Khách Hàng", không có dòng "Khách hàng mới", không có cửa sổ chọn khách hàng.',
        'Dòng phòng có sẵn 8 ô số nhập thẳng: Khách hãng (Hàng hóa SL khách, Doanh số; Dịch vụ SL khách, Doanh số) và Khách khác '
        '(4 ô tương tự).', '4 cột Tổng cộng là ô chỉ đọc.'])
S3.add('Lựa chọn của ô Khối kinh doanh', 'P1', PRE_NEW, TAO + ['Mở ô Khối kinh doanh.'], '—',
       ['Chỉ có 3 khối của công ty TPE: Nghiệp vụ, Kinh doanh, Chi nhánh/Đơn vị thành viên.'])
S3.add('Chọn khối thì sinh tab', 'P0', PRE_NEW, TAO + ['Chọn Khối kinh doanh = Kinh doanh, Nghiệp vụ.'], '—',
       ['Khối Chi tiết có tab "Nghiệp vụ", "Kinh doanh" (theo thứ tự danh mục) và tab "Tổng hợp".',
        'Tab của khối vừa chọn được mở; có ô Khu vực (bắt buộc, chọn nhiều, gợi ý "Chọn khu vực").',
        'Bảng ghi "Chọn khu vực để thêm Tỉnh/TP".'])
S3.add('Chọn Khu vực thì bung Tỉnh/TP', 'P0', PRE_NEW, TAO_KD, 'Khu vực: Đồng bằng sông Hồng',
       ['Bảng hiện các Tỉnh/TP thuộc vùng, STT La Mã I, II, III…, mỗi Tỉnh/TP có dòng "Năm trước" và 1 dòng phòng trống.',
        'Dòng TỔNG ghim trên cùng, ghi "x Tỉnh/TP · 0 phòng · 0 bộ phận".', 'Tỉnh/TP ghi "<tên> (0 phòng)".'])
S3.add('Lựa chọn của ô Phòng ban trên dòng', 'P1', PRE_NEW, TAO_KD + ['Mở ô "Chọn phòng ban" ở Thành phố Hà Nội.'], '—',
       ['Chỉ có phòng thuộc khối Kinh doanh, đang hoạt động (có PHÒNG THIẾT BỊ Ô TÔ 1, PHÒNG KINH DOANH THƯƠNG MẠI…).',
        'Không có phòng của khối khác.'])
S3.add('Nhập thẳng SL khách và Doanh số', 'P0', PRE_NEW,
       TAO_KD + [HN_OTO1, 'Nhập Khách hãng / Hàng hóa: SL khách 4, Doanh số 15000000000.',
                 'Nhập Khách khác / Dịch vụ: SL khách 2, Doanh số 500000000.'],
       ['Khách hãng / Hàng hóa SL khách: 4', 'Khách hãng / Hàng hóa Doanh số: 15000000000', 'Khách khác / Dịch vụ SL khách: 2',
        'Khách khác / Dịch vụ Doanh số: 500000000'],
       ['Ô hiện 15,000,000,000 và 500,000,000 (dấu phẩy ngăn nghìn).',
        'Tổng cộng của dòng: Hàng hóa SL 4 / Doanh số 15,000,000,000; Dịch vụ SL 2 / Doanh số 500,000,000.',
        'Dòng Thành phố Hà Nội và dòng TỔNG cộng đúng các số trên; Tỉnh/TP ghi "Thành phố Hà Nội (1 phòng)".'])
S3.add('Ô số chỉ nhận số nguyên không âm', 'P0', PRE_NEW, TAO_KD + [HN_OTO1, 'Gõ vào ô Doanh số: "-5", "1.5", "abc".'], '—',
       ['Ô không nhận dấu trừ, phần thập phân, chữ; chỉ còn lại chữ số.'])
S3.add('Số quá 13 chữ số bị chặn', 'P1', PRE_NEW, TAO_KD + [HN_OTO1, 'Nhập Doanh số = 12345678901234 (14 chữ số).', 'Bấm Lưu.'],
       'Doanh số: 12345678901234',
       ['Ô Doanh số viền đỏ, dưới ô "Giá trị vượt quá giới hạn cho phép"; toast ' + CHECK + '.', 'Phiếu chưa được lưu.'])
S3.add('Số đúng 13 chữ số lưu được', 'P2', PRE_NEW, TAO_KD + [HN_OTO1, 'Nhập Doanh số = 9999999999999, SL khách = 1.', 'Bấm Lưu.'],
       'Doanh số: 9999999999999', ['Lưu thành công, mở lại thấy 9,999,999,999,999.'])
S3.add('Thiếu Khối kinh doanh thì bị chặn', 'P0', PRE_NEW, TAO + ['Không chọn khối, bấm Lưu.'], '—',
       ['Ô Khối kinh doanh viền đỏ, dưới ô ' + REQ + '; toast ' + CHECK + '.', 'Ở lại màn Tạo, không sinh phiếu.'])
S3.add('Thiếu Khu vực thì bị chặn và tab có chấm đỏ', 'P0', PRE_NEW,
       TAO + ['Chọn Khối = Kinh doanh, Nghiệp vụ.', 'Chọn Khu vực cho tab Kinh doanh, KHÔNG chọn cho tab Nghiệp vụ.',
              'Đứng ở tab Kinh doanh, bấm Lưu.'], '—',
       ['Tự chuyển sang tab Nghiệp vụ; ô Khu vực viền đỏ, dưới ô ' + REQ + '.', 'Tab Nghiệp vụ có dấu báo lỗi đỏ.',
        'Toast ' + CHECK + '.'])
S3.add('Có số mà chưa chọn phòng thì bị chặn', 'P0', PRE_NEW,
       TAO_KD + ['Ở Thành phố Hà Nội KHÔNG chọn phòng, nhập Doanh số 100000000.', 'Bấm Lưu.'], '—',
       ['Ô "Chọn phòng ban" của dòng viền đỏ, dưới ô ' + REQ + '; bảng tự cuộn tới ô lỗi.', 'Toast ' + CHECK + '.'])
S3.add('Lỗi biến mất khi sửa đúng', 'P1', PRE_NEW,
       TAO_KD + ['Để trống phòng, nhập Doanh số, bấm Lưu (báo lỗi).', 'Chọn PHÒNG THIẾT BỊ Ô TÔ 1.'], '—',
       ['Viền đỏ và chữ ' + REQ + ' ở ô phòng biến mất ngay khi chọn.'])
S3.add('Dòng trống bị bỏ khi lưu', 'P1', PRE_NEW,
       TAO_KD + [HN_OTO1 + ' Nhập SL khách 4, Doanh số 15000000000.', 'Các Tỉnh/TP khác để trống.', 'Bấm Lưu, mở lại phiếu.'], '—',
       ['Lưu thành công, không báo lỗi các dòng trống.', 'Mở lại: các Tỉnh/TP không có phòng hiện 1 dòng phòng trống (màn Sửa) / '
        'không có dòng phòng (màn Chi tiết).'])
S3.add('Lưu (nháp) thành công', 'P0', PRE_NEW,
       TAO_KD + [HN_OTO1 + ' Nhập Khách hãng / Hàng hóa SL khách 4, Doanh số 15000000000.', 'Bấm Lưu.'], '—',
       ['Toast "Đã lưu TPE_CTKD_2027.000NN" (số phiếu dạng <mã công ty>_CTKD_<năm>.<5 số>); quay về danh sách.',
        'Phiếu mới ở đầu danh sách, trạng thái Đang tạo, Công ty TPE, Năm 2027, Người tạo A.'])
S3.add('Lưu nháp không bắt cặp SL khách / Doanh số', 'P0', PRE_NEW,
       TAO_KD + [HN_OTO1 + ' Chỉ nhập Doanh số 100000000, để trống SL khách.', 'Bấm Lưu.'], '—',
       ['Lưu thành công (Đang tạo), không báo lỗi cặp.'])
S3.add('Lưu và gửi thành công', 'P0', [PRE_NEW, ACC_D],
       TAO_KD + [HN_OTO1 + ' Nhập SL khách 4, Doanh số 15000000000.', 'Bấm "Lưu và gửi".'], '—',
       ['Toast "Đã gửi duyệt TPE_CTKD_2027.000NN"; quay về danh sách.', 'Phiếu ở trạng thái Chờ duyệt.',
        'D nhận thông báo gửi duyệt kèm số phiếu, bấm vào mở đúng màn chi tiết phiếu.'])
S3.add('Lưu và gửi: có Doanh số mà thiếu SL khách', 'P0', PRE_NEW,
       TAO_KD + [HN_OTO1 + ' Nhập Khách hãng / Hàng hóa Doanh số 15000000000, để trống SL khách.', 'Bấm "Lưu và gửi".'], '—',
       ['Ô SL khách của Khách hãng / Hàng hóa viền đỏ, dưới ô "Bắt buộc nhập SL Khách vì đã có doanh số".',
        'Phiếu KHÔNG được lưu.'])
S3.add('Lưu và gửi: có SL khách mà thiếu Doanh số', 'P0', PRE_NEW,
       TAO_KD + [HN_OTO1 + ' Nhập Khách khác / Dịch vụ SL khách 3, để trống Doanh số.', 'Bấm "Lưu và gửi".'], '—',
       ['Ô Doanh số của Khách khác / Dịch vụ viền đỏ, dưới ô "Bắt buộc nhập doanh số vì đã có SL Khách".',
        'Phiếu KHÔNG được lưu.'])
S3.add('Lưu và gửi: khối chưa có phòng nào', 'P1', PRE_NEW,
       TAO + ['Chọn Khối = Kinh doanh, Nghiệp vụ; chọn Khu vực cho cả 2 tab.',
              'Tab Kinh doanh: ' + HN_OTO1 + ' nhập SL khách 4, Doanh số 15000000000.', 'Tab Nghiệp vụ không chọn phòng nào.',
              'Bấm "Lưu và gửi".'], '—',
       ['Tab Nghiệp vụ báo lỗi; dưới ô Khu vực của tab Nghiệp vụ ' + REQ + '.', 'Phiếu KHÔNG được lưu.'])
S3.add('Lưu và gửi: phiếu không có doanh số', 'P0', PRE_NEW, TAO_KD + [HN_OTO1 + ' Không nhập số nào.', 'Bấm "Lưu và gửi".'], '—',
       ['Toast "Phiếu chưa có chỉ tiêu doanh số — không gửi được".', 'Phiếu KHÔNG được lưu (danh sách không có phiếu mới).'])
S3.add('Lưu và gửi khi công ty chưa có người duyệt', 'P1',
       [PRE_NEW, 'Trong công ty TPE không ai có quyền ' + Q_APPROVE + '.'],
       TAO_KD + [HN_OTO1 + ' Nhập SL khách 4, Doanh số 15000000000.', 'Bấm "Lưu và gửi".'], '—',
       ['Toast "Chưa phân quyền người duyệt".', 'Phiếu KHÔNG được lưu.'])
S3.add('Trùng năm với phiếu đang hiệu lực', 'P0', [ACC_A, OLD8],
       TAO + ['Chọn Năm = Năm 2026, Khối = Kinh doanh, Khu vực = Đồng bằng sông Hồng.', HN_OTO1 + ' Nhập Doanh số 1000.', 'Bấm Lưu.'],
       'Năm: Năm 2026',
       ['Ô Năm viền đỏ, dưới ô "Công ty đã có phiếu TPE_CTKD_2026.00008 (Đã duyệt) cho năm 2026".', 'Không sinh phiếu mới.'])
S3.add('Tạo lại được khi phiếu cùng năm đã Hủy', 'P1', [ACC_A, 'Phiếu năm 2030 của công ty TPE đã ở trạng thái Hủy.'],
       TAO + ['Chọn Năm = Năm 2030, Khối = Kinh doanh, Khu vực = Đồng bằng sông Hồng.', HN_OTO1 + ' Nhập SL khách 1, Doanh số 1000.',
              'Bấm Lưu.'], 'Năm: Năm 2030', ['Lưu thành công, sinh phiếu mới năm 2030 trạng thái Đang tạo.'])
S3.add('Hai người lưu cùng năm cùng lúc', 'P2', [ACC_A, 'Tài khoản A2 cũng có quyền Tạo, cùng công ty TPE; ' + NO2027],
       ['A và A2 cùng mở màn Tạo, nhập phiếu năm 2027.', 'A bấm Lưu trước.', 'A2 bấm Lưu ngay sau.'], '—',
       ['A lưu thành công.', 'A2 bị báo dưới ô Năm "Công ty đã có phiếu TPE_CTKD_2027.000NN (Đang tạo) cho năm 2027".'])
S3.add('Bấm Lưu liên tục nhiều lần', 'P1', PRE_NEW, TAO_KD + [HN_OTO1 + ' Nhập SL khách 4, Doanh số 15000000000.',
                                                           'Bấm Lưu 3 lần thật nhanh.'], '—',
       ['Chỉ sinh 1 phiếu.'])
S3.add('Dòng Năm trước lấy từ phiếu năm trước đã duyệt', 'P0', [ACC_A, OLD8, NO2027], TAO_KD, '—',
       ['Dòng Năm trước của Thành phố Hà Nội: Khách hãng / Hàng hóa SL khách 13, Doanh số 23,762,500,000 (đúng số của '
        'TPE_CTKD_2026.00008).'])
S3.add('Đổi Năm thì Năm trước tính lại', 'P1', [ACC_A, OLD8, 'Phiếu TPE_CTKD_2025.00003 (Đã duyệt) có số khác năm 2026.'],
       TAO_KD + ['Đổi Năm = Năm 2026 (rồi về Năm 2027).'], '—',
       ['Năm 2026: dòng Năm trước lấy số của TPE_CTKD_2025.00003.', 'Năm 2027: lại lấy số của TPE_CTKD_2026.00008.',
        'Số đã nhập trên các dòng phòng giữ nguyên.'])
S3.add('Năm trước trống khi năm trước chưa có phiếu đã duyệt', 'P2',
       [ACC_A, 'Công ty TPE chưa có phiếu nào cho năm 2031.'], TAO + ['Chọn Năm = Năm 2032, Khối = Kinh doanh, Khu vực.'], '—',
       ['Dòng Năm trước của mọi Tỉnh/TP để trống.'])
S3.add('Không chọn trùng phòng trong cùng Tỉnh/TP', 'P0', PRE_NEW,
       TAO_KD + [HN_OTO1, 'Bấm "+ Thêm Phòng Ban" ở Thành phố Hà Nội.', 'Mở ô phòng của dòng 2.'], '—',
       ['Dòng 2 KHÔNG có PHÒNG THIẾT BỊ Ô TÔ 1 trong danh sách chọn.',
        'Ở Tỉnh/TP khác vẫn chọn được PHÒNG THIẾT BỊ Ô TÔ 1.'])
S3.add('Xoá dòng phòng có số', 'P1', PRE_NEW,
       TAO_KD + [HN_OTO1 + ' Nhập Doanh số 1000.', 'Thêm dòng 2, bấm biểu tượng thùng rác ở dòng 1.', 'Bấm Hủy, rồi làm lại và '
                                                                                                     'bấm Xoá.'], '—',
       ['Hỏi "Xoá dòng phòng": "Xoá dòng PHÒNG THIẾT BỊ Ô TÔ 1 tại Thành phố Hà Nội? Số liệu của dòng sẽ mất."',
        'Hủy: dòng giữ nguyên.', 'Xoá: dòng mất, tổng Tỉnh/TP và TỔNG giảm tương ứng.'])
S3.add('Xoá dòng phòng cuối cùng của Tỉnh/TP chỉ làm trống', 'P2', PRE_NEW,
       TAO_KD + [HN_OTO1 + ' (chỉ có 1 dòng, chưa nhập số).', 'Bấm thùng rác ở dòng đó.'], '—',
       ['Không hỏi; dòng vẫn còn nhưng trở về trống (chưa chọn phòng, không số).'])
S3.add('Chia Bộ Phận khi chưa chọn phòng', 'P2', PRE_NEW, TAO_KD + ['Ở Thành phố Hà Nội, dòng phòng chưa chọn, rê chuột vào '
                                                                   '"+ Chia Bộ Phận".'], '—',
       ['Liên kết mờ, gợi ý "Chọn phòng trước", bấm không có tác dụng.'])
S3.add('Chia Bộ Phận cho phòng không có bộ phận', 'P1', PRE_NEW, TAO_KD + [HN_OTO1, 'Bấm "+ Chia Bộ Phận".'], '—',
       ['Toast "Phòng chưa có bộ phận trong danh mục"; dòng phòng giữ nguyên.'])
S3.add('Chia Bộ Phận chuyển số của phòng sang bộ phận đầu', 'P0', PRE_NEW,
       TAO_KD + ['Ở Thành phố Hà Nội chọn PHÒNG KINH DOANH THƯƠNG MẠI, nhập SL khách 5, Doanh số 2000000000.',
                 'Bấm "+ Chia Bộ Phận".'], '—',
       ['Dưới phòng có dòng bộ phận 1.1 (gợi ý "Chọn bộ phận") mang SL khách 5, Doanh số 2,000,000,000.',
        'Ô số của dòng phòng thành chỉ đọc, bằng tổng bộ phận; tổng Tỉnh/TP không đổi.',
        'Liên kết đổi thành "+ Thêm Bộ Phận".'])
S3.add('Phòng có bộ phận = tổng các bộ phận', 'P0', PRE_NEW,
       TAO_KD + ['Chọn PHÒNG KINH DOANH THƯƠNG MẠI, bấm "+ Chia Bộ Phận", chọn bộ phận "BP Thiết bị, vật tư lốp", nhập SL khách 3.',
                 'Bấm "+ Thêm Bộ Phận", chọn "Kinh doanh dự án", nhập SL khách 4.'],
       'Bộ phận 1: SL khách 3\nBộ phận 2: SL khách 4',
       ['Dòng phòng SL khách = 7; Thành phố Hà Nội và TỔNG cộng 7.', 'Dòng TỔNG ghi "… · 1 phòng · 2 bộ phận".',
        'Ô bộ phận của dòng 2 KHÔNG có "BP Thiết bị, vật tư lốp".'])
S3.add('Thêm Bộ Phận khi đã chia hết', 'P2', PRE_NEW,
       TAO_KD + ['Chọn PHÒNG KINH DOANH THƯƠNG MẠI, chia đủ 3 bộ phận.', 'Rê chuột vào "+ Thêm Bộ Phận".'], '—',
       ['Liên kết mờ, gợi ý "Đã chia hết bộ phận của phòng", bấm không có tác dụng.'])
S3.add('Có số ở bộ phận mà chưa chọn bộ phận', 'P1', PRE_NEW,
       TAO_KD + ['Chọn PHÒNG KINH DOANH THƯƠNG MẠI, chia bộ phận, để trống ô bộ phận, nhập Doanh số 1000.', 'Bấm Lưu.'], '—',
       ['Ô "Chọn bộ phận" viền đỏ, dưới ô ' + REQ + '; toast ' + CHECK + '.'])
S3.add('Xoá bộ phận có số (còn bộ phận khác)', 'P1', PRE_NEW,
       TAO_KD + ['Phòng KINH DOANH THƯƠNG MẠI có 2 bộ phận: "BP Thiết bị, vật tư lốp" SL 3, "Kinh doanh dự án" SL 4.',
                 'Bấm thùng rác ở "Kinh doanh dự án", bấm Xoá.'], '—',
       ['Hỏi "Xoá bộ phận": "Xoá dòng Kinh doanh dự án của PHÒNG KINH DOANH THƯƠNG MẠI? Số liệu của dòng sẽ mất."',
        'Sau Xoá: phòng còn SL khách 3.'])
S3.add('Xoá bộ phận cuối cùng thì phòng nhận lại số', 'P1', PRE_NEW,
       TAO_KD + ['Phòng KINH DOANH THƯƠNG MẠI chỉ có 1 bộ phận SL khách 3, Doanh số 900000000.', 'Bấm thùng rác ở bộ phận đó.'], '—',
       ['Không hỏi; phòng trở lại nhập thẳng với SL khách 3, Doanh số 900,000,000.', 'Liên kết trở lại "+ Chia Bộ Phận".'])
S3.add('Đổi phòng khi đã chia bộ phận', 'P1', PRE_NEW,
       TAO_KD + ['Phòng KINH DOANH THƯƠNG MẠI có 2 bộ phận (SL 3 và 4).', 'Đổi ô phòng sang PHÒNG THIẾT BỊ Ô TÔ 1.',
                 'Bấm Hủy; làm lại và bấm Đồng ý.'], '—',
       ['Hỏi "Đổi phòng": "Đổi phòng? Các bộ phận đã chia sẽ bị bỏ."', 'Hủy: giữ phòng cũ và 2 bộ phận.',
        'Đồng ý: phòng mới, không còn bộ phận, dòng phòng giữ SL khách 7 (tổng cũ) để nhập thẳng.'])
S3.add('Bỏ khối đã có số', 'P1', PRE_NEW, TAO_KD + [HN_OTO1 + ' Nhập Doanh số 1000.', 'Ở ô Khối kinh doanh bỏ "Kinh doanh".',
                                                   'Bấm Hủy; làm lại và bấm "Bỏ khối".'], '—',
       ['Hỏi "Bỏ khối kinh doanh": "Bỏ khối Kinh doanh? Số liệu đã nhập của khối sẽ mất."', 'Hủy: khối và số giữ nguyên.',
        'Bỏ khối: tab Kinh doanh mất.'])
S3.add('Bỏ vùng đã có số', 'P1', PRE_NEW, TAO_KD + [HN_OTO1 + ' Nhập Doanh số 1000.', 'Ở ô Khu vực bỏ "Đồng bằng sông Hồng".',
                                                   'Bấm "Bỏ vùng".'], '—',
       ['Hỏi "Bỏ khu vực": "Bỏ vùng Đồng bằng sông Hồng? 1 Tỉnh/TP có số liệu sẽ bị xoá."', 'Bỏ vùng: các Tỉnh/TP của vùng mất.'])
S3.add('Bỏ khối / vùng chưa có số thì không hỏi', 'P2', PRE_NEW, TAO_KD + ['Không nhập số, bỏ vùng rồi bỏ khối.'], '—',
       ['Không hiện hộp hỏi, bỏ ngay.'])
S3.add('Ô Hiển thị đến cấp và thu / mở dòng', 'P1', PRE_NEW,
       TAO_KD + ['Phòng KINH DOANH THƯƠNG MẠI ở Hà Nội đã chia 2 bộ phận.', 'Chọn "Hiển thị đến cấp" = Chỉ Tỉnh/TP, rồi Đến Phòng '
                                                                            'ban, rồi Đến Bộ phận.', 'Bấm mũi tên ở dòng Hà Nội.'],
       '—', ['Chỉ Tỉnh/TP: chỉ còn dòng Tỉnh/TP và Năm trước.', 'Đến Phòng ban: hiện phòng, ẩn bộ phận.',
             'Đến Bộ phận: mở hết (mặc định).', 'Mũi tên: thu / mở riêng dòng đó (gợi ý "Thu gọn" / "Mở rộng").'])
S3.add('Tab Tổng hợp', 'P0', PRE_NEW,
       TAO + ['Chọn Khối = Kinh doanh, Nghiệp vụ, cùng Khu vực Đồng bằng sông Hồng.',
              'Hà Nội: tab Kinh doanh nhập Doanh số 1000 (SL 1); tab Nghiệp vụ nhập Doanh số 2000 (SL 2).', 'Mở tab Tổng hợp.'], '—',
       ['Dòng "TỔNG CỘNG" = SL 3, Doanh số 3,000.', 'Dòng Thành phố Hà Nội = 3 / 3,000; dưới có dòng Năm trước và 2 dòng '
                                                    '"Kinh doanh" 1,000, "Nghiệp vụ" 2,000.', 'Tab Tổng hợp chỉ đọc.'])
S3.add('Đóng / Quay lại khi đã nhập dữ liệu', 'P0', PRE_NEW, TAO_KD + ['Bấm Quay lại.', 'Bấm Ở lại; bấm Quay lại lần nữa, bấm Thoát.'],
       '—', ['Hiện ' + UNSAVED + '.', 'Ở lại: giữ nguyên dữ liệu.', 'Thoát: về danh sách, không sinh phiếu.'])
S3.add('Quay lại khi chưa nhập gì', 'P2', PRE_NEW, TAO + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'])

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
S4.add('Mở màn Sửa', 'P0', PRE_EDIT, ['Đăng nhập A.'] + SUA, '—',
       ['Trang "Sửa phiếu giao chỉ tiêu kinh doanh theo phòng ban: TPE_CTKD_2027.000NN".',
        'Điền sẵn đúng: Năm 2027, khối Kinh doanh, khu vực Đồng bằng sông Hồng, PHÒNG THIẾT BỊ Ô TÔ 1 SL khách 4, Doanh số '
        '15,000,000,000.', 'Đầu khối có nhãn "Đang tạo", tên người tạo + ngày tạo.'])
S4.add('Sửa số liệu và lưu', 'P0', PRE_EDIT, SUA + ['Đổi Doanh số thành 16000000000, bấm Lưu.', 'Mở lại phiếu.'],
       'Doanh số: 16000000000', ['Toast "Đã lưu TPE_CTKD_2027.000NN"; mở lại thấy 16,000,000,000.', 'Số phiếu không đổi.'])
S4.add('Lưu nhiều lần không nhân đôi dòng', 'P1', PRE_EDIT, SUA + ['Bấm Lưu.', 'Mở Sửa lần nữa, bấm Lưu.', 'Mở màn Chi tiết.'], '—',
       ['Hà Nội vẫn chỉ có 1 dòng PHÒNG THIẾT BỊ Ô TÔ 1, số không bị cộng gấp đôi.'])
S4.add('Thêm khối / phòng / bộ phận khi sửa', 'P1', PRE_EDIT,
       SUA + ['Thêm khối Nghiệp vụ + khu vực; ở Hà Nội khối Kinh doanh thêm PHÒNG KINH DOANH THƯƠNG MẠI chia 2 bộ phận SL 3 và 4.',
              'Bấm Lưu, mở lại.'], '—', ['Mở lại thấy đủ 2 tab khối, phòng mới với 2 bộ phận, phòng = 7.'])
S4.add('Đổi Năm khi sửa', 'P1', [PRE_EDIT, 'Công ty TPE chưa có phiếu năm 2028.'], SUA + ['Đổi Năm = Năm 2028, bấm Lưu.'],
       'Năm: Năm 2028', ['Lưu thành công; số phiếu đổi theo năm mới thành TPE_CTKD_2028.000NN (giữ 5 số cuối).',
                         'Dòng Năm trước tính theo phiếu 2027 đã duyệt (nếu có).'])
S4.add('Đổi Năm trùng phiếu khác khi sửa', 'P0', [PRE_EDIT, OLD8], SUA + ['Đổi Năm = Năm 2026, bấm Lưu.'], 'Năm: Năm 2026',
       ['Dưới ô Năm "Công ty đã có phiếu TPE_CTKD_2026.00008 (Đã duyệt) cho năm 2026"; phiếu giữ năm 2027.'])
S4.add('Không đổi gì vẫn lưu được', 'P2', PRE_EDIT, SUA + ['Bấm Lưu ngay.'], '—', ['Toast "Đã lưu …", dữ liệu giữ nguyên.'])
S4.add('Sửa rồi Lưu và gửi', 'P0', [PRE_EDIT, ACC_D], SUA + ['Đổi SL khách = 5, bấm "Lưu và gửi".'], '—',
       ['Toast "Đã gửi duyệt TPE_CTKD_2027.000NN"; phiếu thành Chờ duyệt, SL khách 5.'])
S4.add('Xoá hết số rồi Lưu và gửi', 'P1', PRE_EDIT, SUA + ['Xoá SL khách và Doanh số của PHÒNG THIẾT BỊ Ô TÔ 1.',
                                                         'Bấm "Lưu và gửi".'], '—',
       ['Toast "Phiếu chưa có chỉ tiêu doanh số — không gửi được"; phiếu vẫn giữ số cũ (lần lưu bị huỷ).'])
S4.add('Thoát màn Sửa khi chưa lưu', 'P1', PRE_EDIT, SUA + ['Đổi SL khách = 9.', 'Bấm Quay lại, bấm Thoát.'], '—',
       ['Hiện ' + UNSAVED + '.', 'Thoát: phiếu giữ SL khách 4.'])
S4.add('Không sửa được phiếu không còn Đang tạo', 'P0', [ACC_A, PENDING], [MENU, 'Quan sát dòng phiếu.',
                                                                          'Mở đường link màn Sửa của phiếu.'], '—',
       ['Dòng phiếu không có nút Sửa.', 'Mở màn Sửa: tự chuyển sang màn Chi tiết phiếu, không cho sửa.'])
S4.add('Phiếu bị gửi duyệt ở tab khác khi đang sửa', 'P1', PRE_EDIT,
       ['Tab 1: mở màn Sửa phiếu.', 'Tab 2: mở danh sách, bấm Gửi duyệt phiếu đó.', 'Tab 1: đổi số, bấm Lưu.'], '—',
       ['Tab 1 báo phiếu đã bị khoá / ' + STALE + ', không ghi đè dữ liệu.'])
S4.add('Phiếu cũ có danh sách khách hàng mở Sửa được', 'P1',
       ['Người lập P của TPE_CTKD_2026.00008; phiếu được Hủy duyệt về Đang tạo.', OLD8],
       ['Đăng nhập P.', MENU, 'Bấm Sửa ở TPE_CTKD_2026.00008.', 'Không đổi gì, bấm Lưu.'], '—',
       ['Màn Sửa mở bình thường; Hà Nội PHÒNG THIẾT BỊ Ô TÔ 1 hiện SL khách 4, Doanh số 15,000,000,000.',
        'Không có phần khách hàng chi tiết; lưu xong số giữ nguyên.'])

# ============================================================== V. GỬI DUYỆT
S5 = Sec(5)
S5.add('Gửi duyệt từ danh sách', 'P0', [ACC_A, ACC_D, DRAFT], [MENU, 'Ở dòng phiếu mở menu, bấm "Gửi duyệt".', 'Bấm "Gửi duyệt".'],
       '—', ['Hỏi "Gửi duyệt": "Gửi duyệt phiếu TPE_CTKD_2027.000NN?" (nút Hủy / Gửi duyệt).',
             'Toast "Đã gửi duyệt TPE_CTKD_2027.000NN"; trạng thái Chờ duyệt.', 'D nhận thông báo.'])
S5.add('Gửi duyệt từ màn Chi tiết', 'P0', [ACC_A, DRAFT], [MENU, 'Bấm số phiếu.', 'Bấm "Gửi duyệt", xác nhận.'], '—',
       ['Toast "Đã gửi duyệt …"; màn tải lại, nhãn đổi sang "Chờ duyệt"; nút Sửa, Gửi duyệt biến mất, còn Hủy phiếu, In, Xuất '
        'Excel.'])
S5.add('Bấm Hủy ở hộp hỏi gửi duyệt', 'P2', [ACC_A, DRAFT], [MENU, 'Bấm "Gửi duyệt", bấm Hủy.'], '—',
       ['Phiếu vẫn Đang tạo.'])
S5.add('Gửi duyệt phiếu thiếu cặp SL khách / Doanh số', 'P0',
       [ACC_A, DRAFT.replace('SL khách 4, Doanh số 15,000,000,000', 'Doanh số 15,000,000,000, SL khách trống')],
       [MENU, 'Bấm "Gửi duyệt", xác nhận.'], '—',
       ['Toast "Bắt buộc nhập SL Khách vì đã có doanh số" (hoặc báo lỗi tương ứng); phiếu vẫn Đang tạo.'])
S5.add('Gửi duyệt phiếu không có doanh số', 'P0', [ACC_A, 'Phiếu Đang tạo năm 2027 của A chỉ có SL khách, mọi ô Doanh số trống.'],
       [MENU, 'Bấm "Gửi duyệt", xác nhận.'], '—',
       ['Toast "Phiếu chưa có chỉ tiêu doanh số — không gửi được"; phiếu vẫn Đang tạo.'])
S5.add('Gửi duyệt khi chưa có người duyệt', 'P1', [ACC_A, DRAFT, 'Công ty TPE không ai có quyền ' + Q_APPROVE + '.'],
       [MENU, 'Bấm "Gửi duyệt", xác nhận.'], '—', ['Toast "Chưa phân quyền người duyệt"; phiếu vẫn Đang tạo.'])
S5.add('Gửi duyệt phiếu đã đổi trạng thái ở tab khác', 'P1', [ACC_A, DRAFT],
       ['Tab 1, tab 2 cùng mở danh sách.', 'Tab 1 gửi duyệt phiếu.', 'Tab 2 bấm Gửi duyệt phiếu đó.'], '—',
       ['Tab 2 báo không thực hiện được (' + STALE + ' hoặc không có quyền); phiếu vẫn Chờ duyệt.'])

# ============================================================== VI. DUYỆT PHIẾU (gồm HỦY DUYỆT)
S6 = Sec(6)
S6.add('Duyệt phiếu', 'P0', [ACC_D, PENDING], ['Đăng nhập D.'] + XEM_CD + ['Bấm "Duyệt", bấm "Duyệt" ở hộp hỏi.'], '—',
       ['Hỏi "Duyệt phiếu": "Duyệt phiếu TPE_CTKD_2027.000NN? Phiếu đã duyệt không sửa được."',
        'Toast "Đã duyệt TPE_CTKD_2027.000NN"; nhãn "Đã duyệt"; Người duyệt = D, Ngày duyệt = hôm nay.',
        'A nhận thông báo Đã duyệt kèm số phiếu.'])
S6.add('Duyệt ở danh sách mở sang màn Chi tiết', 'P1', [ACC_D, PENDING], [MENU_CD, 'Ở dòng phiếu mở menu, bấm "Duyệt".'], '—',
       ['Mở màn Chi tiết phiếu (duyệt tại đây); bấm Quay lại về danh sách chờ duyệt.'])
S6.add('Bấm Hủy ở hộp hỏi Duyệt', 'P2', [ACC_D, PENDING], XEM_CD + ['Bấm "Duyệt", bấm Hủy.'], '—', ['Phiếu vẫn Chờ duyệt.'])
S6.add('Phiếu đã duyệt không còn sửa / gửi / hủy', 'P0', [ACC_A, APPROVED], ['Đăng nhập A.', MENU, 'Quan sát dòng phiếu, mở Chi tiết.'],
       '—', ['Không có Sửa, Gửi duyệt, Hủy phiếu; còn Xem, In, Xuất Excel, Lịch sử.'])
S6.add('Duyệt phiếu đã bị duyệt / hủy ở tab khác', 'P1', [ACC_D, PENDING],
       ['Tab 1 và tab 2 cùng mở màn Chi tiết phiếu.', 'Tab 1 bấm Duyệt.', 'Tab 2 bấm Duyệt.'], '—',
       ['Tab 2 báo không thực hiện được; phiếu chỉ được duyệt 1 lần, lịch sử chỉ có 1 mốc duyệt.'])
S6.add('Hủy duyệt phiếu', 'P0', [ACC_D, APPROVED], [MENU, 'Ở dòng phiếu mở menu, bấm "Hủy duyệt", bấm "Hủy duyệt".'], '—',
       ['Hỏi "Hủy duyệt phiếu": "Hủy duyệt phiếu TPE_CTKD_2027.000NN? Phiếu trở về Đang tạo để người lập sửa."',
        'Toast "Đã hủy duyệt …"; phiếu về Đang tạo, Người duyệt / Ngày duyệt trống.', 'A nhận thông báo Hủy duyệt; A sửa lại được.'])
S6.add('Hủy duyệt bị chặn khi đã có phiếu theo nhân viên dùng chỉ tiêu', 'P0',
       [ACC_D, APPROVED, 'Phiếu giao chỉ tiêu theo nhân viên TPE_CTKDNV_2027.000MM của PHÒNG THIẾT BỊ Ô TÔ 1 năm 2027 đang Chờ duyệt.'],
       [MENU, 'Bấm "Hủy duyệt" ở phiếu TPE_CTKD_2027.000NN, xác nhận.'], '—',
       ['Toast "Đã có phiếu giao chỉ tiêu theo nhân viên TPE_CTKDNV_2027.000MM dùng chỉ tiêu của phiếu này, cần hủy duyệt/từ chối '
        'phiếu đó trước".', 'Phiếu vẫn Đã duyệt.'])
S6.add('Hủy duyệt được khi phiếu theo nhân viên chỉ ở Đang tạo / Hủy', 'P1',
       [ACC_D, APPROVED, 'Phiếu theo nhân viên của PHÒNG THIẾT BỊ Ô TÔ 1 năm 2027 đang Đang tạo.'],
       [MENU, 'Bấm "Hủy duyệt", xác nhận.'], '—', ['Hủy duyệt thành công.'])

# ============================================================== VII. KHÔNG DUYỆT PHIẾU (TỪ CHỐI)
S7 = Sec(7)
S7.add('Từ chối phiếu có lý do', 'P0', [ACC_D, PENDING], XEM_CD + ['Bấm "Từ chối".', 'Nhập lý do "Doanh số Hà Nội quá thấp", bấm '
                                                                                  '"Từ chối".'],
       'Lý do: Doanh số Hà Nội quá thấp',
       ['Hộp "Từ chối phiếu": "Từ chối phiếu TPE_CTKD_2027.000NN? Phiếu trở về Đang tạo để người lập sửa.", ô Lý do (gợi ý "Nhập '
        'lý do từ chối").', 'Toast "Đã từ chối …"; phiếu về Đang tạo.', 'A nhận thông báo Từ chối kèm "Lý do: Doanh số Hà Nội quá '
                                                                         'thấp".'])
S7.add('Từ chối mà không nhập lý do', 'P0', [ACC_D, PENDING], XEM_CD + ['Bấm "Từ chối", để trống lý do, bấm "Từ chối".'], '—',
       ['Dưới ô Lý do ' + REQ + '; hộp không đóng; phiếu vẫn Chờ duyệt.'])
S7.add('Lý do chỉ có khoảng trắng', 'P2', [ACC_D, PENDING], XEM_CD + ['Bấm "Từ chối", nhập "   ", bấm "Từ chối".'], '—',
       ['Không từ chối; phiếu vẫn Chờ duyệt.'])
S7.add('Người lập thấy lý do từ chối', 'P0', [ACC_A, 'Phiếu TPE_CTKD_2027.000NN vừa bị D từ chối với lý do "Doanh số Hà Nội quá thấp".'],
       [MENU, 'Mở Sửa phiếu.'], '—', ['Khối Thông tin phiếu có dòng đỏ "Lý do từ chối: Doanh số Hà Nội quá thấp".'])
S7.add('Gửi lại sau khi bị từ chối', 'P1', [ACC_A, ACC_D, 'Phiếu vừa bị từ chối có lý do.'],
       [MENU, 'Sửa số, bấm "Lưu và gửi".', 'D duyệt phiếu.'], '—',
       ['Phiếu sang Chờ duyệt, không còn dòng lý do từ chối cũ.', 'D duyệt được.'])

# ============================================================== VIII. HỦY PHIẾU
S8 = Sec(8)
S8.add('Hủy phiếu Đang tạo', 'P0', [ACC_A, DRAFT], [MENU, 'Ở dòng phiếu mở menu, bấm "Hủy phiếu", bấm "Hủy phiếu".'], '—',
       ['Hỏi "Hủy phiếu": "Hủy phiếu TPE_CTKD_2027.000NN? Phiếu Hủy không sửa được; công ty được tạo phiếu khác cho năm 2027." '
        '(nút Đóng / Hủy phiếu).', 'Toast "Đã hủy …"; nhãn đỏ nhạt "Hủy".'])
S8.add('Người lập hủy phiếu Chờ duyệt', 'P1', [ACC_A, PENDING], [MENU, 'Bấm "Hủy phiếu", xác nhận.'], '—',
       ['Hủy thành công; phiếu biến khỏi danh sách chờ duyệt của D.'])
S8.add('Bấm Đóng ở hộp hỏi hủy', 'P2', [ACC_A, DRAFT], [MENU, 'Bấm "Hủy phiếu", bấm Đóng.'], '—', ['Phiếu giữ nguyên trạng thái.'])
S8.add('Phiếu Hủy chỉ còn Xem và Lịch sử', 'P0', [ACC_A, 'Phiếu năm 2027 của A đã Hủy.'], [MENU, 'Mở menu dòng phiếu, mở Chi tiết.'],
       '—', ['Chỉ có Xem, Lịch sử; KHÔNG có Sửa, Gửi duyệt, Hủy phiếu, In, Xuất Excel.'])
S8.add('Không hủy được phiếu Đã duyệt', 'P1', [ACC_A, APPROVED], [MENU, 'Mở menu dòng phiếu.'], '—', ['Không có "Hủy phiếu".'])
S8.add('Phiếu Hủy không tính Năm trước', 'P1', [ACC_A, 'Phiếu năm 2027 của công ty TPE đã Hủy (trước đó có Doanh số Hà Nội).'],
       TAO + ['Chọn Năm = Năm 2028, Khối = Kinh doanh, Khu vực = Đồng bằng sông Hồng.'], '—',
       ['Dòng Năm trước của Hà Nội để trống (phiếu 2027 đã Hủy không được lấy).'])

# ============================================================== IX. LỊCH SỬ THAY ĐỔI
S9 = Sec(9)
S9.add('Xem lịch sử từ danh sách', 'P0', [ACC_A, 'Phiếu TPE_CTKD_2027.000NN đã: tạo, sửa, gửi duyệt, bị từ chối (lý do "Thiếu số"), '
                                                  'gửi lại, duyệt, hủy duyệt.'],
       [MENU, 'Ở dòng phiếu mở menu, bấm "Lịch sử".'], '—',
       ['Cửa sổ lịch sử ghi "Phiếu TPE_CTKD_2027.000NN", mốc mới nhất trên cùng.',
        'Có đủ mốc: Tạo mới, Thay đổi thông tin, Gửi duyệt (Đang tạo sang Chờ duyệt), Từ chối kèm "Lý do: Thiếu số", Duyệt (Chờ duyệt '
        'sang Đã duyệt), Hủy duyệt (Đã duyệt sang Đang tạo); mỗi mốc có người thực hiện và thời gian.'])
S9.add('Lịch sử ghi mốc Hủy phiếu', 'P1', [ACC_A, 'Phiếu Đang tạo vừa bị A hủy.'], [MENU, 'Mở Lịch sử phiếu.'], '—',
       ['Có mốc thay đổi trạng thái Đang tạo sang Hủy, người thực hiện A.'])
S9.add('Lịch sử trên màn Chi tiết', 'P1', [ACC_A, DRAFT], [MENU, 'Bấm số phiếu, xem khối thông tin hệ thống / Lịch sử ở cuối trang.'],
       '—', ['Hiện cùng các mốc như cửa sổ Lịch sử ở danh sách.'])
S9.add('Phiếu cũ chưa có lịch sử', 'P2', [PRE_LIST, OLD8], [MENU, 'Mở Lịch sử TPE_CTKD_2026.00008.'], '—',
       ['Cửa sổ mở bình thường, báo chưa có lịch sử, không lỗi.'])

# ============================================================== X. XEM CHI TIẾT PHIẾU
S10 = Sec(10)
S10.add('Mở màn Chi tiết', 'P0', [ACC_A, DRAFT], [MENU, 'Bấm số phiếu TPE_CTKD_2027.000NN.'], '—',
        ['Trang "Chi tiết phiếu giao chỉ tiêu kinh doanh theo phòng ban: TPE_CTKD_2027.000NN" kèm nhãn trạng thái.',
         'Mọi ô chỉ đọc: Năm, Khối kinh doanh, Khu vực hiện dạng chữ; ô số không sửa được; không có liên kết Thêm Phòng Ban / '
         'Chia Bộ Phận, không có thùng rác.'])
S10.add('Phiếu cũ có danh sách khách hàng hiển thị đủ số', 'P0', [PRE_LIST, OLD8], [MENU, 'Bấm TPE_CTKD_2026.00008.'], '—',
        ['Hà Nội: Khách hãng / Hàng hóa SL khách 13, Doanh số 23,762,500,000; PHÒNG THIẾT BỊ Ô TÔ 1 4 / 15,000,000,000; PHÒNG DỰ ÁN '
         '3 / 5,262,500,000; PHÒNG THIẾT BỊ Ô TÔ 2 6 / 3,500,000,000.',
         'KHÔNG có phần / nút xem chi tiết khách hàng.', 'Dòng TỔNG ghi "34 Tỉnh/TP · … phòng · 0 bộ phận".'])
S10.add('Ô số 0 để trống, dòng TỔNG hiện 0', 'P1', [PRE_LIST, OLD8], [MENU, 'Mở TPE_CTKD_2026.00008, xem dòng PHÒNG KINH DOANH THƯƠNG '
                                                                              'MẠI ở Hà Nội.'], '—',
        ['Các ô của phòng này trống (không ghi 0).', 'Cột không có số ở dòng TỔNG hiện 0.'])
S10.add('Quay lại về đúng danh sách', 'P1', [ACC_D, PENDING], [MENU_CD, 'Bấm số phiếu, bấm Quay lại.'], '—',
        ['Về danh sách chờ duyệt (không phải danh sách thường).'])
S10.add('Nút theo trạng thái ở màn Chi tiết', 'P0', [ACC_A, ACC_D, PENDING], ['A mở Chi tiết phiếu.', 'D mở Chi tiết phiếu.'], '—',
        ['A: Hủy phiếu, Xuất Excel, In (không có Sửa, Gửi duyệt, Duyệt, Từ chối).', 'D: Duyệt, Từ chối, Xuất Excel, In.'])
S10.add('Tên phòng / bộ phận đã ngừng hoạt động', 'P1', [ACC_A, APPROVED, 'Sau khi duyệt, PHÒNG THIẾT BỊ Ô TÔ 1 bị ngừng hoạt động.'],
        [MENU, 'Mở Chi tiết phiếu.'], '—', ['Vẫn hiện tên "PHÒNG THIẾT BỊ Ô TÔ 1" và số đã giao.'])
S10.add('Tab Tổng hợp ở màn Chi tiết', 'P1', [PRE_LIST, 'Phiếu TPHP_CTKD_2026.00010 có 2 khối.'], [MENU, 'Mở phiếu, bấm tab Tổng hợp.'],
        '—', ['Mỗi Tỉnh/TP có dòng Năm trước và dòng từng khối; TỔNG CỘNG bằng tổng 2 tab khối.'])

# ============================================================== XI. IN PHIẾU
S11 = Sec(11)
S11.add('In phiếu', 'P0', [ACC_D, APPROVED], [MENU, 'Ở dòng phiếu mở menu, bấm "In".'], '—',
        ['Mở cửa sổ xem trước "Xem trước phiếu: TPE_CTKD_2027.000NN", khổ A4 ngang.',
         'Đầu phiếu: letterhead của công ty TPE (công ty ghi trên phiếu), tiêu đề "PHIẾU GIAO CHỈ TIÊU KINH DOANH THEO PHÒNG BAN", '
         'Số phiếu, Ngày lập, Năm, Trạng thái.',
         'Bảng mỗi khối + bảng Tổng hợp, số khớp màn Chi tiết.',
         'Cuối phiếu 3 chỗ ký: Người lập (tên A), Trưởng phòng, Người duyệt (tên D), mỗi chỗ có "(Ký, ghi rõ họ tên)".'])
S11.add('In từ màn Chi tiết', 'P1', [ACC_A, DRAFT], [MENU, 'Mở Chi tiết, bấm "In".'], '—',
        ['Cùng nội dung bản in như từ danh sách; chỗ Người duyệt để trống.'])
S11.add('Letterhead theo công ty của phiếu, không theo người in', 'P0',
        [ACC_V4, 'V4 đang làm việc ở công ty TPE.'], ['Đăng nhập V4.', MENU, 'In phiếu TPSG_CTKD_2026.00011.'], '—',
        ['Letterhead là của công ty TPSG, KHÔNG phải TPE.'])
S11.add('In phiếu có bộ phận và phiếu cũ nhiều Tỉnh/TP', 'P1', [PRE_LIST, OLD8], [MENU, 'In TPE_CTKD_2026.00008.'], '—',
        ['Bản in đủ 34 Tỉnh/TP, sang trang không mất viền / tiêu đề cột, chữ không bị cắt lề phải.'])

# ============================================================== XII. TÙY CHỈNH CỘT
S12 = Sec(12)
S12.add('Mở cửa sổ tùy chỉnh cột', 'P1', PRE_LIST, [MENU, 'Bấm nút biểu tượng cột.'], '—',
        ['Cửa sổ "Tuỳ chỉnh cột" liệt kê 10 cột, ghi "Đang chọn 9/10 cột" (Ngày duyệt chưa chọn).',
         'STT, Số phiếu, Hành động là cột bắt buộc, không bỏ chọn được.'])
S12.add('Bật cột Ngày duyệt', 'P1', PRE_LIST, [MENU, 'Mở tùy chỉnh cột, tích Ngày duyệt, bấm Lưu.'], '—',
        ['Toast "Cập nhật thành công"; bảng có thêm cột Ngày duyệt, phiếu cũ hiện đúng ngày duyệt.'])
S12.add('Ẩn cột và đổi thứ tự', 'P1', PRE_LIST, [MENU, 'Bỏ chọn Người tạo, kéo Năm lên sau Số phiếu, bấm Lưu.'], '—',
        ['Bảng không còn cột Người tạo; cột Năm đứng ngay sau Số phiếu.'])
S12.add('Cấu hình cột được nhớ', 'P2', PRE_LIST, [MENU, 'Ẩn cột Người duyệt, Lưu.', 'Tải lại trang; đăng nhập tài khoản khác mở màn.'],
        '—', ['Sau tải lại vẫn ẩn Người duyệt.', 'Tài khoản khác vẫn thấy cột mặc định (cấu hình lưu theo từng người).'])
S12.add('Chọn tất cả / Bỏ chọn hết / Đóng', 'P2', PRE_LIST, [MENU, 'Mở tùy chỉnh cột, bấm Bỏ chọn hết, rồi Chọn tất cả, bấm Đóng.'], '—',
        ['Bỏ chọn hết vẫn giữ các cột bắt buộc.', 'Đóng không lưu: bảng giữ nguyên.'])

# ============================================================== XIII. XUẤT DANH SÁCH EXCEL
S13 = Sec(13)
S13.add('Xuất danh sách Excel', 'P0', PRE_LIST, [MENU, 'Bấm "Xuất Excel".', 'Giữ các cột mặc định, bấm xuất file.'], '—',
        ['Cửa sổ chọn cột: Số phiếu, Công ty, Năm, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái.',
         'Tải file "phieu_giao_chi_tieu_theo_phong_ban.xlsx", tiêu đề "DANH SÁCH PHIẾU GIAO CHỈ TIÊU KINH DOANH THEO PHÒNG BAN", '
         'có logo công ty; 9 dòng, cột STT; toast "Xuất Excel thành công".'])
S13.add('Xuất theo bộ lọc đang áp', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Năm = 2026.', 'Xuất Excel.'], 'Năm: 2026',
        ['File chỉ có 4 phiếu năm 2026.'])
S13.add('Xuất chỉ cột đã chọn', 'P1', PRE_LIST, [MENU, 'Xuất Excel, chỉ chọn Số phiếu, Năm, Trạng thái.'], '—',
        ['File có STT + 3 cột đã chọn, đúng thứ tự.'])
S13.add('Xuất khi không có dữ liệu', 'P1', PRE_LIST, [MENU, 'Tìm "ZZZ999".', 'Xuất Excel.'], '—',
        ['Toast "Không có dữ liệu để xuất"; không tải file.'])
S13.add('Xuất danh sách chờ duyệt', 'P2', [ACC_D, 'Công ty TPE có 2 phiếu Chờ duyệt.'], [MENU_CD, 'Xuất Excel.'], '—',
        ['File chỉ có 2 phiếu Chờ duyệt của TPE.'])
S13.add('Xuất Excel 1 phiếu', 'P0', [PRE_LIST, 'Phiếu TPHP_CTKD_2026.00010 có 2 khối.'],
        [MENU, 'Ở dòng TPHP_CTKD_2026.00010 mở menu, bấm "Xuất Excel".'], '—',
        ['Tải file "TPHP_CTKD_2026.00010.xlsx"; mỗi khối 1 sheet (tên "1. <tên khối>", "2. <tên khối>") + sheet "Tổng hợp".',
         'Mỗi sheet mở hết cây (Năm trước, Tổng cộng, phòng, bộ phận), số khớp màn Chi tiết, có chỗ ký cuối sheet.'])
S13.add('Xuất Excel phiếu có khối tên chứa dấu gạch chéo', 'P1',
        [ACC_A, 'Phiếu Đang tạo của A có khối "Chi nhánh/Đơn vị thành viên" đã nhập số.'], [MENU, 'Xuất Excel phiếu đó.'], '—',
        ['Tải file bình thường, sheet của khối mang tên đã bỏ dấu "/" (vd "1. Chi nhánhĐơn vị thành viên"), không lỗi.'])

# ============================================================== XIV. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S14 = Sec(14)
MENU_NV = 'Vào phân hệ Bán hàng > nhóm "Kế hoạch" > "Giao chỉ tiêu kinh doanh" > bấm "Theo nhân viên".'
S14.add('Phiếu theo nhân viên nạp chỉ tiêu từ phiếu phòng ban đã duyệt', 'P0',
        ['Phiếu TPE_CTKD_2027.000NN Đã duyệt: Hà Nội PHÒNG THIẾT BỊ Ô TÔ 1 SL khách 4, Doanh số 15,000,000,000.',
         'Tài khoản trưởng PHÒNG THIẾT BỊ Ô TÔ 1 có quyền Tạo chỉ tiêu kinh doanh theo nhân viên.'],
        [MENU_NV, 'Bấm Tạo mới, chọn Năm 2027, Phòng ban = PHÒNG THIẾT BỊ Ô TÔ 1.'], '—',
        ['Dòng "Chỉ tiêu giao" của Hà Nội: SL khách 4, Doanh số 15,000,000,000.'])
S14.add('Phiếu phòng ban Chờ duyệt chưa được nạp', 'P0', ['Phiếu TPE_CTKD_2027.000NN đang Chờ duyệt.'],
        [MENU_NV, 'Tạo mới, chọn Năm 2027, mở ô Phòng ban.'], '—',
        ['PHÒNG THIẾT BỊ Ô TÔ 1 không có trong ô chọn (chưa có chỉ tiêu được duyệt).'])
S14.add('Phòng ở 2 khối cùng Tỉnh/TP thì chỉ tiêu cộng dồn', 'P1',
        ['Phiếu 2027 Đã duyệt: PHÒNG THIẾT BỊ Ô TÔ 1 ở Hà Nội khối Kinh doanh SL khách 5, khối Nghiệp vụ SL khách 7.'],
        [MENU_NV, 'Tạo mới, Năm 2027, Phòng = PHÒNG THIẾT BỊ Ô TÔ 1.'], '—', ['Chỉ tiêu giao Hà Nội: SL khách 12.'])
S14.add('Phòng chia bộ phận vẫn nạp tổng phòng', 'P1',
        ['Phiếu 2027 Đã duyệt: PHÒNG KINH DOANH THƯƠNG MẠI ở Hà Nội chia 2 bộ phận SL khách 3 và 4.'],
        [MENU_NV, 'Tạo mới, Năm 2027, Phòng = PHÒNG KINH DOANH THƯƠNG MẠI.'], '—', ['Chỉ tiêu giao Hà Nội: SL khách 7.'])
S14.add('Báo cáo giao chỉ tiêu theo phòng ban đếm SL khách theo số đã nhập', 'P0',
        ['Phiếu 2027 Đã duyệt: Hà Nội PHÒNG THIẾT BỊ Ô TÔ 1 Khách hãng / Hàng hóa SL khách 4, Doanh số 15,000,000,000 (nhập thẳng, '
         'không có danh sách khách hàng).', 'Tài khoản có quyền "Xem báo cáo giao chỉ tiêu kinh doanh theo phòng ban".'],
        ['Mở Báo cáo giao chỉ tiêu kinh doanh theo phòng ban, chọn năm 2027, công ty TPE.'], '—',
        ['Số khách hãng của PHÒNG THIẾT BỊ Ô TÔ 1 = 4 (bằng số đã nhập), doanh số 15,000,000,000.',
         'Lưu ý: KHÔNG được ra 0 vì phiếu không còn danh sách khách hàng chi tiết.'])
S14.add('Màn tạo / sửa cũ không còn được dùng', 'P1', ['Tài khoản có quyền Tạo chỉ tiêu kinh doanh theo phòng ban.'],
        ['Ở hệ thống cũ mở menu giao chỉ tiêu kinh doanh theo phòng ban.'], '—',
        ['Mục menu mở sang màn mới ở hệ thống này (tab mới), không còn màn nhập có chọn chi tiết khách hàng.'])
S14.add('Phiếu theo nhân viên đã duyệt chặn Hủy duyệt phiếu phòng ban', 'P0',
        [ACC_D, APPROVED, 'Phiếu theo nhân viên của PHÒNG THIẾT BỊ Ô TÔ 1 năm 2027 Đã duyệt.'],
        [MENU, 'Hủy duyệt phiếu TPE_CTKD_2027.000NN.'], '—',
        ['Bị chặn với câu "Đã có phiếu giao chỉ tiêu theo nhân viên … dùng chỉ tiêu của phiếu này, cần hủy duyệt/từ chối phiếu đó '
         'trước".'])
S14.add('Phiếu duyệt năm nay thành Năm trước của năm sau', 'P1', [ACC_A, APPROVED],
        TAO + ['Chọn Năm = Năm 2028, Khối = Kinh doanh, Khu vực = Đồng bằng sông Hồng.'], '—',
        ['Dòng Năm trước của Hà Nội = SL khách 4, Doanh số 15,000,000,000.'])

# ============================================================== XV. PHÂN QUYỀN
S15 = Sec(15)
S15.add('Quyền ' + Q_VIEW + ' mức Tổng công ty', 'P0', PRE_LIST, ['Đăng nhập V4.', MENU], '—',
        ['Thấy đủ 9 phiếu của 4 công ty; có ô lọc Công ty.', 'Không có Tạo mới; mọi dòng chỉ có Xem, In, Xuất Excel, Lịch sử.'])
S15.add('Quyền ' + Q_VIEW + ' mức Công ty', 'P0', [ACC_V3, OLD9], ['Đăng nhập V3.', MENU], '—',
        ['Chỉ thấy 2 phiếu TPSG_CTKD_2025.00006, TPSG_CTKD_2026.00011.', 'Không có ô lọc Công ty.'])
S15.add('Không có quyền Xem: chỉ phiếu của mình', 'P0', [ACC_A, OLD9, 'A đã lập 1 phiếu năm 2027.'], ['Đăng nhập A.', MENU], '—',
        ['Chỉ thấy phiếu A lập; không thấy 9 phiếu cũ.'])
S15.add('Không có quyền nào', 'P0', ACC_N, ['Đăng nhập N.', MENU], '—', ['Danh sách ' + EMPTY + ', không có Tạo mới.'])
S15.add('Phiếu Đang tạo của người khác luôn bị ẩn', 'P0', [ACC_V4, DRAFT], ['Đăng nhập V4.', MENU], '—',
        ['V4 KHÔNG thấy phiếu Đang tạo của A; khi A gửi duyệt thì V4 mới thấy.'])
S15.add('Quyền ' + Q_CREATE, 'P0', PRE_NEW, ['Đăng nhập A.', MENU], '—',
        ['Có Tạo mới; tạo, sửa, gửi duyệt, hủy được phiếu của mình.'])
S15.add('Quyền Tạo không sửa được phiếu người khác', 'P0',
        [ACC_A, 'Tài khoản A2 cùng quyền Tạo, cùng công ty; A2 có phiếu Chờ duyệt năm 2028.', 'A có quyền Xem mức Công ty.'],
        ['Đăng nhập A.', MENU, 'Mở phiếu năm 2028 của A2.'], '—', ['Xem được nhưng KHÔNG có Sửa, Gửi duyệt, Hủy phiếu.'])
S15.add('Quyền ' + Q_APPROVE, 'P0', [ACC_D, PENDING], ['Đăng nhập D.', MENU], '—',
        ['Thấy phiếu Chờ duyệt của công ty TPE (dù không có quyền Xem), có Duyệt / Từ chối; Hủy duyệt phiếu Đã duyệt do mình duyệt.',
         'Không có Tạo mới.'])
S15.add('Quyền Duyệt chỉ trong công ty đang làm việc', 'P0', [ACC_D, 'Công ty TPSG có 1 phiếu Chờ duyệt.'],
        ['Đăng nhập D (đang ở TPE).', MENU_CD], '—', ['Không thấy phiếu Chờ duyệt của TPSG, không duyệt được.'])
S15.add('Người duyệt thấy lại phiếu mình đã duyệt', 'P1', [ACC_D, 'D đã duyệt phiếu năm 2027 của TPE.'], ['Đăng nhập D.', MENU], '—',
        ['Danh sách có phiếu D đã duyệt dù D không có quyền Xem.'])
S15.add('Đổi công ty đang làm việc', 'P0', [ACC_D, 'D có Vai trò Duyệt ở cả công ty TPE và TPSG; mỗi công ty có 1 phiếu Chờ duyệt.'],
        ['Đăng nhập D, đang ở TPE, mở ' + MENU_CD, 'Đổi công ty đang làm việc sang TPSG, mở lại.'], '—',
        ['Ở TPE: chỉ phiếu của TPE.', 'Ở TPSG: chỉ phiếu của TPSG; quyền tính lại theo công ty mới.'])
S15.add('Có 2 Vai trò Xem khác mức', 'P1', ['Tài khoản V có 2 Vai trò: ' + Q_VIEW + ' mức Công ty (TPSG) và mức Tổng công ty.', OLD9],
        ['Đăng nhập V.', MENU], '—', ['Áp mức lớn hơn: thấy đủ 9 phiếu, có ô lọc Công ty.'])
S15.add('Ẩn nút khi thiếu quyền', 'P0', [ACC_V4, PENDING], ['Đăng nhập V4.', MENU, 'Mở menu dòng phiếu Chờ duyệt.'], '—',
        ['Không có Tạo mới, Sửa, Gửi duyệt, Duyệt, Từ chối, Hủy duyệt, Hủy phiếu.'])
S15.add('Mở đường link Chi tiết ngoài phạm vi', 'P0', [ACC_N, 'N có đường link màn Chi tiết TPE_CTKD_2026.00008.'],
        ['Đăng nhập N, mở đường link.'], '—', ['Bị đưa về danh sách, không lộ số liệu phiếu.'])
S15.add('Mở đường link màn Tạo khi không có quyền Tạo', 'P0', ACC_V4, ['Đăng nhập V4.', 'Mở đường link màn Tạo, nhập phiếu, bấm Lưu.'],
        '—', ['Hệ thống từ chối, báo không có quyền; không sinh phiếu.'])
S15.add('Mở đường link màn Sửa phiếu người khác', 'P0', [ACC_V4, PENDING], ['Đăng nhập V4.', 'Mở đường link màn Sửa của phiếu.'], '—',
        ['Tự chuyển sang màn Chi tiết, không sửa được.'])
S15.add('Bị gỡ quyền giữa lúc thao tác', 'P1', [ACC_D, PENDING, 'Quản trị gỡ quyền Duyệt của D khi D đang mở màn Chi tiết phiếu.'],
        ['D bấm Duyệt, xác nhận.'], '—', ['Hệ thống từ chối, báo không có quyền; phiếu vẫn Chờ duyệt.'])
S15.add('Không có đặc cách Super admin', 'P1', ['Tài khoản Super admin không được cấp 3 quyền của màn, chưa lập phiếu.', OLD9],
        ['Đăng nhập tài khoản đó.', MENU], '—', ['Danh sách rỗng, không có Tạo mới (như tài khoản không quyền).'])

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'CHỈNH SỬA', S4),
    ('V', 'GỬI DUYỆT', S5),
    ('VI', 'DUYỆT PHIẾU / HỦY DUYỆT', S6),
    ('VII', 'KHÔNG DUYỆT PHIẾU (TỪ CHỐI)', S7),
    ('VIII', 'HỦY PHIẾU', S8),
    ('IX', 'LỊCH SỬ THAY ĐỔI', S9),
    ('X', 'XEM CHI TIẾT PHIẾU GIAO CHỈ TIÊU', S10),
    ('XI', 'IN PHIẾU', S11),
    ('XII', 'TÙY CHỈNH CỘT', S12),
    ('XIII', 'XUẤT DANH SÁCH EXCEL', S13),
    ('XIV', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S14),
    ('XV', 'PHÂN QUYỀN', S15),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
check_no_dash_pre(SECTIONS, [])
_ids = ['TC_%02d.%s' % (s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
assert len(_ids) == len(set(_ids)), 'Trùng TC ID'

if __name__ == '__main__':
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='Phiếu giao chỉ tiêu KD theo phòng ban (#11643) - Cập nhật ngày 19/11/2026',
                module_name='Giao chỉ tiêu KD theo phòng ban', description_block=DESCRIPTION_BLOCK, sections=SECTIONS,
                loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

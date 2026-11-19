# -*- coding: utf-8 -*-
"""Testcase màn "Khai báo hạn mức công nợ KH" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='danh_muc').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'danh_muc' — lý do từ code (18/11/2026): màn là bảng cấu hình gắn theo khách hàng (khách × công ty: Cách tính lãi + 2 hạn mức),
không có số chứng từ, không có vòng đời trạng thái / gửi duyệt / duyệt; được màn khác đọc ngược (Báo cáo hạn mức, Yêu cầu xuất hàng,
Yêu cầu xuất bán hàng mượn) — đúng bản chất danh mục, không phải phiếu hay báo cáo.
Nhóm theo đúng tên + thứ tự chuẩn 'danh_muc' (check_tc.THU_TU), BỎ nhóm màn không có (kiểm pages/finance/declare-limit-debts/index.vue
+ Routes/api.php: không có nút / route Thêm mới, Xóa, Khóa - Mở khóa, Xem chi tiết, Import):
I Hiển thị · II Tìm kiếm & lọc · III Chỉnh sửa (sửa thẳng trong bảng + Lưu từng khách; gồm khai báo lần đầu cho khách chưa có hạn mức —
không có nút Thêm mới nên không tách nhóm THÊM MỚI) · IV Lịch sử · V Tùy chỉnh cột · VI Xuất danh sách Excel · VII Ràng buộc · VIII Phân quyền.
Màn KHÔNG có Cài đặt bộ lọc (bộ lọc 2 ô, hiện thẳng). Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../benefit-rates/gen_testcase.py (06/11, qua check_tc 0 lỗi).
Nguồn hành vi: FE pages/finance/declare-limit-debts/index.vue; BE Modules/Finance DeclareLimitDebtService / Controller / Routes;
ReportLimitDebtService, ProductExportOverLimitService, BorrowSellRequestService::isOverLimit (nơi đọc hạn mức).
Số liệu mẫu: dữ liệu thật trên dev 18/11/2026 (43TPHDKH, 29TPHPNG-26, 65TPHPAN-03), QA dựng lại trên môi trường test nếu khác.
"""
import os
import sys
from collections import defaultdict

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets'))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from tc_chuan import build_chuan  # noqa: E402
from tc_phieu_bosung import check_no_dash_pre  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Tài chính > nhóm "Kế toán công nợ" > "Khách hàng" > bấm "Khai báo hạn mức công nợ KH".'
Q_VIEW = '"Xem khai báo hạn mức công nợ khách hàng"'
Q_MAN = '"Quản lý khai báo hạn mức công nợ khách hàng"'
EMPTY = '"Không có dữ liệu phù hợp."'
OK = '"Cập nhật thành công."'
CHECK = '"Vui lòng kiểm tra lại dữ liệu nhập"'
TYPE_REQ = '"Vui lòng chọn cách tính lãi"'
MAXE = '"Không được lớn hơn 999,999,999,999,999"'
NOPERM = '"Bạn không có quyền thực hiện chức năng này"'
NOPERM_ROW = '"Bạn không có quyền sửa hạn mức của khách hàng này."'
CONFLICT = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'
UNSAVED = '"Thông tin chưa lưu" – "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"'

ACC_A = 'Tài khoản A: kế toán công ty Tân Phát (CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT), có cả 2 quyền %s và %s.' % (Q_VIEW, Q_MAN)
ACC_B = 'Tài khoản B: kế toán công ty Tân Phát Sài Gòn, CHỈ có quyền %s.' % Q_MAN
ACC_C = 'Tài khoản C: nhân viên công ty Tân Phát, KHÔNG có quyền nào của màn.'
ACC_D = 'Tài khoản D: nhân viên công ty Tân Phát, CHỈ có quyền %s.' % Q_VIEW
KH1 = ('Khách "43TPHDKH - NGUYEN VAN TEST" đã có 9 dòng hạn mức (9 công ty); dòng công ty Tân Phát: Theo vượt hạn mức công nợ / '
       '120,000 / 120,000, 8 dòng khác trống.')
KH2 = ('Khách "29TPHPNG-26 - CÔNG TY TNHH THƯƠNG MẠI DỊCH VỤ VÀ XUẤT NHẬP KHẨU DUY ANH" (MST 0108839168) đã có 7 dòng (không có '
       'dòng 2 công ty: Đầu tư Tập đoàn Etek, Giải pháp Etek Green); dòng Tân Phát: Theo thời gian thanh toán / trống / 500,000,000.')
KH3 = 'Khách "65TPHPAN-03 - KHÁCH HÀNG CÁ NHÂN AN" chưa có dòng hạn mức nào (hệ thống có 9 công ty).'
DATA = 'Danh mục Khách hàng có 13,266 khách hàng (không tính nhà cung cấp); khách tạo gần nhất là 65TPHPAN-03.'
PRE = ACC_A + '\n' + DATA
LOC_KH1 = 'Gõ "43TPHDKH" vào ô Khách hàng, chọn "43TPHDKH - NGUYEN VAN TEST".'

CK = defaultdict(list)


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

    def add(self, func, prio, pre, steps, td, exp, ck=()):
        self.append(T(len(self) + 1, func, prio, pre, steps, td, exp))
        tid = 'TC_%02d.%s' % (self.idx, self[-1][0])
        for s in (ck if isinstance(ck, (list, tuple)) else [ck]):
            CK[s].append(tid)


DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Mỗi công ty khai cho từng khách hàng: Cách tính lãi, Hạn mức công nợ tính lãi, Hạn mức công nợ xuất hàng. Sửa thẳng trên bảng '
     'danh sách và bấm Lưu theo từng khách (giữ như hệ thống cũ). Hạn mức công nợ xuất hàng dùng để chặn / chuyển duyệt khi gửi duyệt '
     'Yêu cầu xuất hàng, Yêu cầu xuất bán hàng mượn vượt hạn mức; 2 hạn mức hiện ở Báo cáo hạn mức công nợ khách hàng.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Mọi khách hàng trong danh mục Khách hàng (không gồm nhà cung cấp), mới nhất trước.\n'
     '- Khách đã có dòng hạn mức: chỉ các dòng đã có.\n- Khách chưa có dòng nào: mỗi công ty trong hệ thống 1 dòng trống.\n'
     '- Màn KHÔNG có trạng thái (không có Hoạt động / Khóa / duyệt).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Người CHỈ có quyền Quản lý (không có quyền Xem): không thấy dòng của công ty khác.\n'
     '- Nhà cung cấp (không phải khách hàng) không hiện.\n- Khách bị xóa khỏi danh mục không còn hiện.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Không áp dụng: màn không có ô lọc ngày (chỉ cửa sổ Lịch sử thay đổi có Từ ngày / Đến ngày, lọc '
                                         'theo thời điểm thao tác).'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Khách hàng > các dòng hạn mức theo công ty (mỗi khách × công ty tối đa 1 dòng).\n'
     '- Ô STT, Mã, Tên, MST/CMND, Hành động gộp dọc trên các dòng công ty của khách.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Lưu = xoá hết dòng của khách rồi ghi lại các dòng đang hiện với người lưu (giữ như hệ thống cũ) — không sinh dòng trùng.\n'
     '- Lưu không đổi gì thì không ghi, không ghi lịch sử.'),
    ('7. Phân quyền cấp',
     '- Xem màn KHÔNG cần quyền (giữ như hệ thống cũ).\n'
     '- Quyền "Xem khai báo hạn mức công nợ khách hàng": thấy dòng mọi công ty khi đi cùng quyền Quản lý.\n'
     '- Quyền "Quản lý khai báo hạn mức công nợ khách hàng": sửa dòng công ty mình; không có quyền Xem thì chỉ thấy dòng công ty mình.\n'
     '- Không có mức phạm vi Tổng công ty / Công ty / Phòng ban.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là thứ tự KHÁCH đầu – cuối của trang, N là tổng số KHÁCH khớp bộ lọc (không đếm dòng công ty).\n'
     '- STT đánh theo khách, liên tục giữa các trang.\n- Hạn mức dạng 1,234,567; chưa khai thì trống.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: A (2 quyền, Tân Phát), B (chỉ Quản lý, Tân Phát Sài Gòn), C (không quyền), D (chỉ Xem).\n'
     '- Lưu ý: hai hành vi GIỮ NHƯ HỆ THỐNG CŨ (user chốt 14/10/2026, không báo lỗi): Lưu xoá hết dòng rồi ghi lại dòng đang hiện '
     '(người chỉ có Quản lý lưu là mất dòng công ty khác); khách đã có dòng thì không hiện thêm công ty khác.\n'
     '- Lưu ý: đổi trang / lọc / sắp xếp khi đang sửa dở thì mất phần sửa, KHÔNG hỏi.\n'
     '- Lưu ý: nhập Hạn mức công nợ tính lãi thì PHẢI chọn Cách tính lãi.\n'
     '- Không có Thêm mới, Xóa, Khóa, Xem chi tiết, Import, Cài đặt bộ lọc.'),
]

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', PRE, [MENU], '—',
       ['Mở màn "Khai báo hạn mức công nợ khách hàng", không báo lỗi.', 'Bảng hiện 10 khách đầu, "Hiển thị 1–10 / 13266".',
        'Mỗi khách gồm nhiều dòng công ty, ô STT / Mã / Tên / MST/CMND / Hành động gộp dọc.'], [1, 10, 16])
S1.add('Tiêu đề màn hình', 'P1', PRE, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt và mục menu.'], '—',
       ['Thanh tiêu đề, tiêu đề bảng, tab: "Khai báo hạn mức công nợ khách hàng".', 'Mục menu ghi "Khai báo hạn mức công nợ KH".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', [PRE, KH1], [MENU, 'Quan sát khối bộ lọc, thanh công cụ và cột Hành động của 43TPHDKH.'],
       '—', ['Khối "Bộ lọc danh sách": ô tìm nhanh, ô Khách hàng, Tìm kiếm, Làm mới (KHÔNG có Tìm kiếm nâng cao, Cài đặt bộ lọc).',
             'Thanh công cụ: Xuất Excel, nút biểu tượng cột; KHÔNG có Tạo mới, Import.',
             'Cột Hành động: nút Lưu (đĩa mềm xanh ngọc) và Lịch sử (đồng hồ).'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 9 cột: STT, Mã khách hàng, Tên khách hàng, MST/CMND, Khai báo theo công ty, Cách tính lãi, Hạn mức công nợ tính lãi, '
        'Hạn mức công nợ xuất hàng, Hành động.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 9/9 cột".'], 5)
S1.add('Dữ liệu dòng khớp hạn mức đã khai', 'P0', [PRE, KH2], [MENU, 'Gõ "29TPHPNG-26" vào ô Khách hàng và chọn khách.',
                                                          'Đối chiếu dòng công ty Tân Phát.'], '—',
       ['MST/CMND "0108839168".', 'Khách có đúng 7 dòng công ty (không tự thêm dòng Giải pháp Etek Green).',
        'Dòng Tân Phát: Cách tính lãi "Theo thời gian thanh toán", Hạn mức công nợ tính lãi trống, Hạn mức công nợ xuất hàng '
        '"500,000,000" căn phải.'], [6])
S1.add('Khách chưa khai hiện đủ dòng công ty trống', 'P0', [ACC_C, KH3], [MENU, 'Quan sát nhóm dòng của 65TPHPAN-03.'], '—',
       ['Có 9 dòng, mỗi công ty trong hệ thống 1 dòng.', 'Cách tính lãi và 2 hạn mức trống (KHÔNG hiện 0).'], [6, 7])
S1.add('MST/CMND lấy số CMND khi không có mã số thuế', 'P2',
       [PRE, 'Khách cá nhân "Anh Đức" không có mã số thuế, CMND 012345678.'], [MENU, 'Lọc khách "Anh Đức", quan sát cột MST/CMND.'],
       '—', ['Cột MST/CMND hiện "012345678".', 'Khách không có cả hai thì ô trống.'], 6)
S1.add('Trạng thái bản ghi', 'P2', PRE, [MENU, 'Quan sát các cột và bộ lọc.'], '—',
       ['Không có cột / ô lọc trạng thái (màn không có Hoạt động / Khóa).', 'Dòng có giá trị là hạn mức đang áp dụng ngay.'], 7)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       ['Trong bảng: ' + EMPTY, 'Dưới bảng: "Không có khách hàng nào."', 'Không báo lỗi.'], [8, 9])
S1.add('Đổi số dòng/trang', 'P1', PRE, [MENU, 'Chọn Số dòng/trang = 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 20 khách, "Hiển thị 1–20 / 13266", về trang 1.', 'Lựa chọn có 5 / 10 / 20 / 50 / 100.'], [11, 18])
S1.add('Chuyển trang trước / tiếp theo', 'P1', PRE, [MENU, 'Bấm › (trang sau).', 'Bấm ‹ (trang trước).'], '—',
       ['Sau bước 2: "Hiển thị 11–20 / 13266", STT bắt đầu 11.', 'Sau bước 3: về "Hiển thị 1–10 / 13266".'], [12, 15])
S1.add('Trang đầu / trang cuối và trạng thái nút', 'P2', PRE, [MENU, 'Quan sát nút « ‹ ở trang 1.', 'Bấm » (trang cuối).'], '—',
       ['Trang 1: « ‹ mờ, không bấm được.', 'Trang cuối (1327): › » mờ; dòng "Hiển thị 13261–13266 / 13266".'], [13, 14])
S1.add('STT đánh theo khách, liên tục giữa các trang', 'P1', PRE, [MENU, 'Sang trang 2, quan sát cột STT.'], '—',
       ['Mỗi khách 1 số (ô gộp), các dòng công ty của khách không có STT riêng.', 'Trang 2 bắt đầu 11.'], 15)
S1.add('Tổng số đếm theo khách', 'P0', [PRE, KH1], [MENU, LOC_KH1], '—',
       ['Dòng ghi "Hiển thị 1–1 / 1" dù khách có 9 dòng công ty (N đếm khách, không đếm dòng).'], 16)
S1.add('Về trang 1 khi đổi bộ lọc', 'P1', PRE, [MENU, 'Sang trang 3.', 'Nhập "0987" vào ô tìm nhanh, bấm Tìm kiếm.'],
       'Ô tìm nhanh: 0987', ['Danh sách về trang 1, "Hiển thị 1–10 / 216".'], 17)
S1.add('Thứ tự mặc định: khách mới nhất trước', 'P0', PRE, [MENU, 'Quan sát 2 khách đầu.'], '—',
       ['Khách đầu là 65TPHPAN-03 (tạo gần nhất), tiếp theo 65TPHPAN-02.', 'Không cột nào đang có mũi tên sắp xếp.'], 19)
S1.add('Sắp xếp Mã khách hàng tăng / giảm', 'P1', PRE, [MENU, 'Bấm tiêu đề "Mã khách hàng".', 'Bấm lần nữa.'], '—',
       ['Lần 1: tăng dần, khách đầu "0SUBKBR-1".', 'Lần 2: giảm dần.', 'Mỗi lần về trang 1.'], [20, 21, 25])
S1.add('Sắp xếp Tên khách hàng giảm dần', 'P2', PRE, [MENU, 'Bấm tiêu đề "Tên khách hàng" 2 lần.'], '—',
       ['Tên xếp từ Z về A (theo cách so sánh chữ của hệ thống).'], [20, 21])
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE, [MENU, 'Bấm tiêu đề các cột MST/CMND, Khai báo theo công ty, Cách tính lãi, 2 cột hạn mức.'],
       '—', ['Không có biểu tượng sắp xếp, thứ tự không đổi.', 'Không có cột Ngày tạo / Ngày cập nhật trên màn.'], [22, 23])
S1.add('Giữ sắp xếp khi chuyển trang', 'P2', PRE, [MENU, 'Sắp Mã khách hàng tăng dần.', 'Sang trang 2.'], '—',
       ['Trang 2 vẫn theo Mã khách hàng tăng dần, nối tiếp trang 1.'], 24)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm đúng mã số thuế', 'P0', [PRE, KH2], [MENU, 'Nhập "0108839168" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: 0108839168',
       ['Chỉ còn khách 29TPHPNG-26, "Hiển thị 1–1 / 1".'], [26, 37])
S2.add('Tìm một phần số điện thoại', 'P0', PRE, [MENU, 'Nhập "0987", bấm Tìm kiếm.'], 'Ô tìm nhanh: 0987',
       ['Hiện mọi khách có số điện thoại / MST / CMND chứa "0987": "Hiển thị 1–10 / 216".'], [27, 41])
S2.add('Không tìm theo mã / tên khách ở ô tìm nhanh', 'P1', PRE, [MENU, 'Nhập "NGUYEN VAN TEST", bấm Tìm kiếm.'],
       'Ô tìm nhanh: NGUYEN VAN TEST', ['Danh sách rỗng ' + EMPTY + ' (ô tìm nhanh chỉ tìm SĐT, MST, CMND — mã / tên tìm ở ô Khách hàng).'],
       [28, 29])
S2.add('Từ khóa không tồn tại', 'P1', PRE, [MENU, 'Nhập "ZZZ999", bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       [EMPTY, '"Không có khách hàng nào."'], [30, 40])
S2.add('Ký tự đặc biệt % và _', 'P2', PRE, [MENU, 'Nhập "%", bấm Tìm kiếm.', 'Nhập "_", bấm Tìm kiếm.'], 'Ô tìm nhanh: % ; _',
       ['Ký tự được tìm đúng nghĩa đen, không trả về toàn bộ danh sách.', 'Không báo lỗi.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', [PRE, KH2], [MENU, 'Nhập "  0108839168  ", bấm Tìm kiếm.'], 'Ô tìm nhanh: "  0108839168  "',
       ['Kết quả như tìm "0108839168" (1 khách).'], 32)
S2.add('Nhập chuỗi rất dài', 'P2', PRE, [MENU, 'Dán 300 ký tự số vào ô tìm nhanh, bấm Tìm kiếm.'], '300 ký tự "1"',
       ['Ô nhận đủ (không giới hạn số ký tự), danh sách rỗng, không lỗi.'], 33)
S2.add('Xóa từ khóa bằng nút ×', 'P1', PRE, [MENU, 'Tìm "0987".', 'Bấm × trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], 'Ô tìm nhanh: 0987',
       ['Sau bước 3: ô trống, danh sách chưa đổi.', 'Sau bước 4: về "Hiển thị 1–10 / 13266".'], 34)
S2.add('Enter và nút Tìm kiếm', 'P1', PRE, [MENU, 'Nhập "0987" (chưa bấm gì).', 'Nhấn Enter.'], 'Ô tìm nhanh: 0987',
       ['Bước 2: danh sách chưa đổi.', 'Bước 3: danh sách lọc như bấm Tìm kiếm.'], 35)
S2.add('Giá trị mặc định bộ lọc', 'P2', [PRE, 'Chưa dùng màn trong 10 phút gần nhất.'], [MENU], '—',
       ['Ô tìm nhanh trống, gợi ý "Tìm theo SĐT hoặc MST/CMND khách hàng".', 'Ô Khách hàng trống, gợi ý "Gõ để tìm khách hàng...".'], 36)
S2.add('Lọc theo ô Khách hàng', 'P0', [PRE, KH1], [MENU, 'Gõ "43" vào ô Khách hàng.', 'Gõ tiếp "TPHDKH", chọn gợi ý.'], 'Khách hàng: 43TPHDKH',
       ['Gõ dưới 2 ký tự chưa có gợi ý; gợi ý dạng "43TPHDKH - NGUYEN VAN TEST".', 'Chọn xong danh sách lọc NGAY (không cần bấm '
        'Tìm kiếm), "Hiển thị 1–1 / 1".'], [37, 47])
S2.add('Kết hợp ô tìm nhanh và ô Khách hàng', 'P0', [PRE, KH1, KH2],
       [MENU, 'Chọn khách 43TPHDKH ở ô Khách hàng.', 'Nhập "0108839168" vào ô tìm nhanh, bấm Tìm kiếm.'], '—',
       ['Danh sách rỗng vì 2 điều kiện kết hợp kiểu VÀ (MST thuộc khách khác).', 'Hiện ' + EMPTY + '.'], [38, 39])
S2.add('Phân trang và sắp xếp sau lọc', 'P1', PRE, [MENU, 'Tìm "0987".', 'Sắp Mã khách hàng tăng dần.', 'Sang trang 2.'], '—',
       ['Tổng vẫn 216, 22 trang; trang 2 "Hiển thị 11–20 / 216".', 'Kết quả vẫn trong tập đã lọc, theo Mã tăng dần.'], [41, 42, 43])
S2.add('Làm mới xóa toàn bộ lọc', 'P0', PRE, [MENU, 'Chọn khách 43TPHDKH, tìm "0987", sắp Mã tăng.', 'Bấm Làm mới.'], '—',
       ['2 ô lọc trống, bỏ sắp xếp, về trang 1 "Hiển thị 1–10 / 13266".'], 44)
S2.add('Chuyển màn rồi quay lại', 'P1', PRE, [MENU, 'Chọn khách 43TPHDKH.', 'Mở màn "Báo cáo hạn mức công nợ khách hàng".',
                                              'Quay lại màn Khai báo.'], '—',
       ['Bộ lọc về mặc định (chuyển sang màn khác thì không giữ bộ lọc).'], 45)
S2.add('Tải lại trang (F5) trong 10 phút', 'P0', PRE, [MENU, 'Chọn khách 43TPHDKH, sắp Mã tăng.', 'Nhấn F5.'], '—',
       ['Vẫn lọc khách 43TPHDKH, ô Khách hàng hiện lại tên khách, giữ sắp xếp.', 'Sau 10 phút không thao tác, F5 thì bộ lọc về mặc định.'], 46)
S2.add('Mở tab mới', 'P2', PRE, [MENU, 'Chọn khách 43TPHDKH.', 'Mở màn ở tab mới trong vòng 10 phút.'], '—',
       ['Tab mới dùng lại bộ lọc vừa chọn (bộ lọc nhớ trên trình duyệt 10 phút).'], 47)
S2.add('Tài khoản khác cùng trình duyệt', 'P2', [PRE, ACC_C], [MENU, 'A chọn khách 43TPHDKH, đăng xuất.', 'C đăng nhập ngay, mở màn.'],
       '—', ['Lưu ý: bộ lọc nhớ theo trình duyệt (không theo tài khoản) nên C có thể thấy lại bộ lọc của A trong 10 phút — ghi nhận '
             'theo hiện trạng.'], 48)

# ============================================================== III. CHỈNH SỬA
S3 = Sec(3)
S3.add('Dòng công ty mình hiện ô nhập', 'P0', [PRE, KH1], [MENU, LOC_KH1], '—',
       ['Dòng Tân Phát: ô chọn Cách tính lãi, 2 ô hạn mức có giá trị đã lưu (120,000).',
        '8 dòng công ty khác hiện chữ, không sửa được.', 'Có nút Lưu ở cột Hành động.'], [51, 103, 104, 105, 106])
S3.add('Các trường bắt buộc / không bắt buộc', 'P1', [PRE, KH3], [MENU, 'Lọc 65TPHPAN-03.', 'Quan sát dòng Tân Phát.'], '—',
       ['Cả 3 ô trống, có gợi ý "Chọn cách tính lãi", "Nhập hạn mức công nợ tính lãi", "Nhập hạn mức công nợ xuất hàng".',
        'Không có dấu sao bắt buộc; Cách tính lãi chỉ bắt buộc khi có Hạn mức công nợ tính lãi.'], [52, 53])
S3.add('Ô Cách tính lãi có đúng 2 lựa chọn', 'P0', [PRE, KH3], [MENU, 'Lọc 65TPHPAN-03.', 'Bấm ô Cách tính lãi dòng Tân Phát.'], '—',
       ['Lựa chọn: "Theo vượt hạn mức công nợ", "Theo thời gian thanh toán".', 'Chọn xong có nút × để bỏ chọn.'], [51, 105])
S3.add('Khai báo lần đầu đầy đủ 3 trường', 'P0', [PRE, KH3],
       [MENU, 'Lọc 65TPHPAN-03.', 'Dòng Tân Phát: chọn Cách tính lãi, nhập 2 hạn mức.', 'Bấm Lưu (đĩa mềm).'],
       ['Cách tính lãi: Theo vượt hạn mức công nợ', 'Hạn mức công nợ tính lãi: 100000000', 'Hạn mức công nợ xuất hàng: 200000000'],
       ['Thông báo ' + OK, 'Dòng Tân Phát hiện "100,000,000" / "200,000,000".',
        'Khách vẫn hiện 9 dòng (8 dòng công ty khác được ghi với giá trị trống).',
        'Báo cáo hạn mức công nợ khách hàng của công ty Tân Phát có thêm dòng 65TPHPAN-03.'], [55, 58, 59, 54])
S3.add('Khai báo chỉ Hạn mức công nợ xuất hàng', 'P0', [PRE, KH3],
       [MENU, 'Lọc 65TPHPAN-03.', 'Chỉ nhập Hạn mức công nợ xuất hàng.', 'Bấm Lưu.'], 'Hạn mức công nợ xuất hàng: 50000000',
       ['Lưu được (không bắt Cách tính lãi), ' + OK, 'Cách tính lãi và Hạn mức tính lãi để trống.'], [56, 57])
S3.add('Ghi lịch sử lần khai đầu', 'P1', [PRE, KH3], [MENU, 'Khai báo như TC trên rồi bấm Lịch sử của khách.'], '—',
       ['Có 1 mốc "Thay đổi thông tin", chỉ công ty Tân Phát: Cách tính lãi (trống) thành Theo vượt hạn mức công nợ, 2 hạn mức (trống) thành '
        'giá trị mới.', 'Không có mốc "Tạo mới"; 8 dòng trống không sinh log.'], [60, 112])
S3.add('Sửa một trường', 'P0', [PRE, KH1], [MENU, LOC_KH1, 'Sửa Hạn mức công nợ xuất hàng thành 150000.', 'Bấm Lưu.'],
       'Hạn mức công nợ xuất hàng: 150000',
       [OK, 'Dòng Tân Phát hiện "150,000"; các trường khác giữ nguyên.', 'Lịch sử thêm mốc chỉ có Hạn mức công nợ xuất hàng 120,000 thành '
        '150,000.'], [107, 110, 112, 177])
S3.add('Sửa nhiều trường cùng lúc', 'P0', [PRE, KH1], [MENU, LOC_KH1, 'Đổi Cách tính lãi, 2 hạn mức.', 'Bấm Lưu.'],
       ['Cách tính lãi: Theo thời gian thanh toán', 'Hạn mức công nợ tính lãi: 300000', 'Hạn mức công nợ xuất hàng: 400000'],
       [OK, 'Cả 3 giá trị đổi; lịch sử 1 mốc liệt kê đủ 3 trường cũ - mới.'], [108, 178, 183])
S3.add('Lưu không đổi gì', 'P0', [PRE, KH1], [MENU, LOC_KH1, 'Không sửa, bấm Lưu.'], '—',
       ['Vẫn báo ' + OK, 'Không thêm mốc lịch sử, người cập nhật không đổi.'], [109, 125, 182])
S3.add('Người tạo / người cập nhật dòng là người lưu', 'P2', [PRE, KH1], [MENU, LOC_KH1, 'Sửa hạn mức, Lưu.', 'Mở Lịch sử.'], '—',
       ['Mốc mới ghi "Người thực hiện: <tên A> — <phòng ban A>", thời điểm vừa lưu.', 'Màn không có cột Ngày / Người cập nhật.'], 111)
S3.add('Xoá trắng hạn mức đã khai', 'P1', [PRE, KH1], [MENU, LOC_KH1, 'Xóa trắng 2 ô hạn mức, bỏ chọn Cách tính lãi (×).', 'Bấm Lưu.'],
       '—', [OK, 'Dòng Tân Phát vẫn còn, 3 ô trống.', 'Báo cáo hạn mức công nợ khách hàng không còn dòng 43TPHDKH.'], [110, 280])
S3.add('Có hạn mức tính lãi nhưng thiếu Cách tính lãi', 'P0', [PRE, KH3],
       [MENU, 'Lọc 65TPHPAN-03.', 'Nhập Hạn mức công nợ tính lãi, để trống Cách tính lãi.', 'Bấm Lưu.'], 'Hạn mức công nợ tính lãi: 1000000',
       ['Chữ đỏ dưới ô Cách tính lãi ' + TYPE_REQ + ', viền đỏ.', 'Thông báo ' + CHECK + '; không lưu.'], [61, 70, 113, 117])
S3.add('Lỗi thiếu Cách tính lãi biến mất khi chọn', 'P1', [PRE, KH3],
       [MENU, 'Làm như TC trên để hiện lỗi.', 'Chọn Cách tính lãi "Theo thời gian thanh toán".'], '—',
       ['Lỗi dưới ô mất ngay khi chọn.', 'Xóa trắng Hạn mức tính lãi thì lỗi cũng mất.'], [71, 118])
S3.add('Hạn mức vượt trần', 'P0', [PRE, KH3], [MENU, 'Lọc 65TPHPAN-03.', 'Nhập Hạn mức công nợ xuất hàng 1000000000000000.'],
       'Hạn mức công nợ xuất hàng: 1,000,000,000,000,000',
       ['Ngay khi gõ: chữ đỏ ' + MAXE + ' dưới ô, KHÔNG tự sửa về trần.', 'Bấm Lưu: thông báo ' + CHECK + ', không lưu.'],
       [66, 115, 117])
S3.add('Nhập đúng trần', 'P0', [PRE, KH3], [MENU, 'Lọc 65TPHPAN-03.', 'Nhập 999999999999999 cho cả 2 hạn mức, chọn Cách tính lãi.',
                                             'Bấm Lưu.'], 'Hạn mức: 999,999,999,999,999',
       [OK, 'Hiện "999,999,999,999,999" đúng từng chữ số (không bị làm tròn).'], 65)
S3.add('Nhập 0 và ký tự không phải số', 'P0', [PRE, KH3], [MENU, 'Lọc 65TPHPAN-03.', 'Gõ "abc-1.5" vào ô Hạn mức công nợ xuất hàng.',
                                                           'Xóa, nhập 0, Lưu.'], 'abc-1.5 ; 0',
       ['Ô chỉ nhận chữ số, không nhận chữ, dấu âm, số lẻ.', 'Giá trị 0 lưu được (0 = không kiểm vượt hạn mức).'],
       [62, 63, 64, 114])
S3.add('Khoảng trắng và dấu phẩy ngăn nghìn', 'P2', [PRE, KH3], [MENU, 'Lọc 65TPHPAN-03.', 'Gõ " 1234567 " vào ô hạn mức.'], '1234567',
       ['Ô tự hiển thị "1,234,567"; khoảng trắng không được nhận.', 'Lưu ra đúng 1,234,567.'], [68, 69])
S3.add('Không có kiểm trùng', 'P2', [PRE, KH1], [MENU, LOC_KH1, 'Đặt hạn mức giống hệt khách khác, Lưu.'], '—',
       ['Lưu được — màn không có trường duy nhất (mỗi khách × công ty 1 dòng do hệ thống quản).'], [67, 116])
S3.add('Rời màn khi còn khách sửa dở — chọn Ở lại', 'P0', [PRE, KH1],
       [MENU, LOC_KH1, 'Sửa Hạn mức công nợ tính lãi thành 150000 (chưa Lưu).', 'Bấm menu "Báo cáo hạn mức công nợ khách hàng".',
        'Chọn Ở lại.'], '—', ['Hiện hộp ' + UNSAVED + '.', 'Ở lại: vẫn ở màn, ô vẫn là 150,000.'], [94, 97, 121, 123])
S3.add('Rời màn khi còn khách sửa dở — chọn Thoát', 'P0', [PRE, KH1],
       [MENU, LOC_KH1, 'Sửa hạn mức (chưa Lưu).', 'Bấm menu màn khác.', 'Chọn Thoát.', 'Quay lại màn, lọc 43TPHDKH.'], '—',
       ['Rời màn, KHÔNG lưu.', 'Quay lại thấy giá trị cũ 120,000; lịch sử không thêm mốc.'], [96, 122, 124])
S3.add('Đóng hộp chưa lưu bằng (x)', 'P2', [PRE, KH1], [MENU, LOC_KH1, 'Sửa hạn mức.', 'Bấm menu màn khác.', 'Bấm (x) của hộp.'], '—',
       ['Như Ở lại: vẫn ở màn, giữ giá trị đang nhập.'], 95)
S3.add('Rời màn khi chưa sửa gì', 'P1', [PRE, KH1], [MENU, LOC_KH1, 'Không sửa, bấm menu màn khác.'], '—',
       ['Chuyển màn ngay, không hỏi.'], [93, 119])
S3.add('Sửa rồi trả về giá trị ban đầu', 'P1', [PRE, KH1], [MENU, LOC_KH1, 'Đổi 120000 thành 130000 rồi về 120000.', 'Bấm menu màn khác.'],
       '—', ['Không hỏi — so với giá trị đã lưu thì không có thay đổi.'], [99, 120])
S3.add('Nhập rồi xóa hết ở khách chưa khai', 'P2', [PRE, KH3], [MENU, 'Lọc 65TPHPAN-03.', 'Gõ 1000 rồi xóa trắng.', 'Bấm menu màn khác.'],
       '—', ['Không hỏi (ô trở lại trống như ban đầu).'], 98)
S3.add('Đổi trang khi đang sửa dở', 'P0', [PRE, KH1], [MENU, 'Sửa hạn mức dòng Tân Phát của một khách ở trang 1 (chưa Lưu).',
                                                      'Bấm sang trang 2 rồi về trang 1.'], '—',
       ['KHÔNG có hộp hỏi; phần sửa dở mất, ô về giá trị đã lưu (giữ như hệ thống cũ).'], [124])
S3.add('Để màn lâu rồi Lưu', 'P2', [PRE, KH1], [MENU, LOC_KH1, 'Sửa hạn mức, để 30 phút (phiên còn hạn).', 'Bấm Lưu.'], '—',
       ['Lưu bình thường, ' + OK, 'Nếu phiên đã hết hạn: báo hết phiên, chuyển về đăng nhập, không lưu.'], 100)
S3.add('Bấm Lưu liên tục', 'P0', [PRE, KH1], [MENU, LOC_KH1, 'Sửa hạn mức, bấm Lưu 3 lần thật nhanh.'], '—',
       ['Nút khóa trong lúc lưu (chú thích "Đang lưu..."), chỉ 1 lần lưu.', 'Lịch sử chỉ thêm 1 mốc.'], 101)
S3.add('Hai người cùng lưu một khách', 'P0', [PRE, ACC_B, KH1],
       ['A và B cùng mở khách 43TPHDKH.', 'A sửa dòng Tân Phát, Lưu.', 'B (chỉ thấy dòng Tân Phát Sài Gòn) sửa dòng của mình, Lưu.',
        'A tải lại trang.'], '—',
       ['Cả 2 lần lưu thành công, mỗi lần 1 mốc lịch sử.', 'Lưu ý: do cách lưu giữ như hệ thống cũ, lần lưu của B XOÁ dòng công ty Tân '
        'Phát vừa sửa (B không thấy dòng đó) — A tải lại chỉ còn dòng Tân Phát Sài Gòn.'], [102, 128])
S3.add('Khách vừa bị xóa khỏi danh mục', 'P2', [PRE, KH3], [MENU, 'Lọc 65TPHPAN-03.', 'Người khác xóa khách ở danh mục Khách hàng.',
                                                            'Nhập hạn mức, Lưu.'], '—',
       ['Thông báo ' + CONFLICT + ', danh sách nạp lại, không còn khách.'], 127)
S3.add('Hạn mức đã dùng ở phiếu xuất', 'P1', [PRE, KH1, 'Có phiếu Yêu cầu xuất hàng của khách đang Đợi TP duyệt do vượt hạn mức.'],
       [MENU, LOC_KH1, 'Tăng Hạn mức công nợ xuất hàng, Lưu.'], '—',
       ['Lưu được, không chặn.', 'Phiếu đã ở Đợi TP duyệt giữ nguyên; hạn mức mới áp cho lần gửi duyệt sau.'], 129)

# ============================================================== IV. LỊCH SỬ THAY ĐỔI
S4 = Sec(4)
S4.add('Mở cửa sổ lịch sử', 'P0', [PRE, KH1], [MENU, LOC_KH1, 'Bấm Lịch sử (đồng hồ).'], '—',
       ['Cửa sổ "Lịch sử thay đổi: 43TPHDKH - NGUYEN VAN TEST".', 'Có nút Bộ lọc, Đóng, (x).'], [162, 163])
S4.add('Nội dung một mốc', 'P0', [PRE, KH1, 'DNS Admin khai hạn mức lần đầu lúc 26/10/2026 16:15.'], [MENU, LOC_KH1, 'Bấm Lịch sử.'], '—',
       ['Mốc "26/10/2026 16:15" — "Thay đổi thông tin".', '"Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ".',
        '"Hạn mức theo công ty sửa thông tin:" — "- CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT:" Cách tính lãi (trống) thành Theo vượt '
        'hạn mức công nợ; 2 hạn mức (trống) thành 120,000.'], [165, 166, 167, 168])
S4.add('Mốc mới nhất ở trên', 'P1', [PRE, KH1, 'Khách có 3 lần lưu có thay đổi.'], [MENU, LOC_KH1, 'Bấm Lịch sử.'], '—',
       ['3 mốc, lần lưu gần nhất đứng đầu.'], 164)
S4.add('Khách chưa có lịch sử', 'P1', [ACC_C, KH3], [MENU, 'Lọc 65TPHPAN-03.', 'Bấm Lịch sử.'], '—',
       ['Hiện "Chưa có lịch sử thao tác nào.".'], [162])
S4.add('Lọc theo loại hành động', 'P2', [PRE, KH1], [MENU, LOC_KH1, 'Bấm Lịch sử > Bộ lọc.', 'Chọn Loại hành động "Tạo mới".',
                                                    'Đổi sang "Thay đổi thông tin".'], '—',
       ['"Tạo mới": "Không có lịch sử phù hợp bộ lọc." (màn không ghi mốc Tạo mới).', '"Thay đổi thông tin": hiện đủ mốc.'],
       [169, 173, 175])
S4.add('Lọc theo người thực hiện và thời gian', 'P2', [PRE, KH1],
       [MENU, LOC_KH1, 'Bấm Lịch sử > Bộ lọc.', 'Chọn Người thực hiện DNS Admin, Từ ngày 26/10/2026, Đến ngày 26/10/2026.'], '—',
       ['Chỉ còn mốc 26/10/2026 16:15.', 'Đổi Từ ngày 27/10/2026 thành không còn mốc.'], [170, 171, 172])
S4.add('Làm mới bộ lọc lịch sử', 'P2', [PRE, KH1], [MENU, LOC_KH1, 'Lọc lịch sử như TC trên.', 'Bấm Làm mới.'], '—',
       ['Các ô lọc trống, hiện lại đủ mốc.'], 174)
S4.add('Lưu chỉ ghi công ty có đổi', 'P0', [PRE, KH1], [MENU, LOC_KH1, 'Sửa Hạn mức công nợ tính lãi, Lưu.', 'Bấm Lịch sử.'], '—',
       ['Mốc mới chỉ có công ty Tân Phát và chỉ trường Hạn mức công nợ tính lãi; 8 công ty khác không xuất hiện.'], [177, 182])
S4.add('Đóng lịch sử giữ trạng thái danh sách', 'P1', [PRE, KH1],
       [MENU, 'Sang trang 2, sửa hạn mức một khách (chưa Lưu).', 'Bấm Lịch sử của khách đó, bấm Đóng.'], '—',
       ['Về đúng trang 2, giữ bộ lọc và giá trị đang sửa dở.', 'Bấm (x) hoặc click ra ngoài cũng đóng như vậy.'], [184, 185])

# ============================================================== V. TÙY CHỈNH CỘT
S5 = Sec(5)
S5.add('Mở cửa sổ Tùy chỉnh cột', 'P1', PRE, [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột", liệt kê 9 cột đúng thứ tự, "Đang chọn 9/9 cột".'], [198, 199, 200])
S5.add('Cột khóa không ẩn được', 'P0', PRE, [MENU, 'Mở Tùy chỉnh cột, thử bỏ tích STT, Mã khách hàng, Hành động.'], '—',
       ['3 cột này không bỏ tích được (ô mờ, Mã khách hàng có ổ khóa).', 'Bấm Bỏ chọn hết vẫn giữ 3 cột này.'], [203, 205])
S5.add('Ẩn cột rồi lưu', 'P0', PRE, [MENU, 'Mở Tùy chỉnh cột, bỏ tích MST/CMND.', 'Bấm Lưu.'], '—',
       ['Thông báo "Cập nhật thành công"; bảng không còn cột MST/CMND.', 'Dữ liệu, bộ lọc, tổng số không đổi.'], [202, 206, 210, 211])
S5.add('Hiện lại cột đã ẩn', 'P1', [PRE, 'Đã ẩn MST/CMND.'], [MENU, 'Mở Tùy chỉnh cột, tích MST/CMND (hoặc Chọn tất cả), Lưu.'], '—',
       ['Cột MST/CMND hiện lại đúng vị trí.'], 201)
S5.add('Kéo đổi thứ tự cột', 'P1', PRE, [MENU, 'Kéo "Hạn mức công nợ xuất hàng" lên trên "Cách tính lãi", Lưu.'], '—',
       ['Bảng hiện cột Hạn mức công nợ xuất hàng đứng trước Cách tính lãi.'], 204)
S5.add('Đóng không lưu', 'P2', PRE, [MENU, 'Mở Tùy chỉnh cột, bỏ tích vài cột.', 'Bấm Đóng.'], '—',
       ['Bảng giữ nguyên cấu hình cũ.'], 207)
S5.add('Ghi nhớ sau F5 và theo tài khoản', 'P1', [PRE, ACC_C], [MENU, 'A ẩn cột MST/CMND, Lưu.', 'F5.', 'C đăng nhập mở màn.'], '—',
       ['A: sau F5 vẫn ẩn MST/CMND.', 'C: vẫn đủ 9 cột (cấu hình lưu riêng từng người).'], [208, 209])

# ============================================================== VI. XUẤT DANH SÁCH EXCEL
S6 = Sec(6)
S6.add('Mở cửa sổ chọn trường', 'P1', PRE, [MENU, 'Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất file", 7 trường: Mã khách hàng, Tên khách hàng, MST/CMND, Khai báo theo công ty, Cách tính lãi, '
        'Hạn mức công nợ tính lãi, Hạn mức công nợ xuất hàng; tích sẵn cả 7.'], [212, 213, 214])
S6.add('Xuất mặc định theo bộ lọc 1 khách', 'P0', [PRE, KH1], [MENU, LOC_KH1, 'Bấm Xuất Excel > Xuất file.'], '—',
       ['Tải file "khai-bao-han-muc-cong-no-khach-hang.xlsx", thông báo "Xuất Excel thành công.".',
        'File: letterhead công ty, tiêu đề "KHAI BÁO HẠN MỨC CÔNG NỢ KHÁCH HÀNG", cột STT + 7 trường.',
        '9 dòng (mỗi công ty 1 dòng), ô STT / Mã / Tên / MST gộp 9 dòng; dòng Tân Phát 120,000 / 120,000.',
        'Cuối file: "Ngày ..., tháng ..., năm ...", "Người lập", "(Ký, họ tên)".'],
       [215, 220, 223, 224, 225, 227, 228])
S6.add('Chọn một số trường và đổi thứ tự', 'P1', [PRE, KH1], [MENU, LOC_KH1, 'Bấm Xuất Excel, bỏ tích MST/CMND, kéo Hạn mức công nợ '
                                                              'xuất hàng lên đầu.', 'Xuất file.'], '—',
       ['File có STT, Hạn mức công nợ xuất hàng, rồi các trường còn lại; không có MST/CMND.'], [217, 226])
S6.add('Chọn tất cả / Bỏ chọn hết', 'P2', PRE, [MENU, 'Bấm Xuất Excel > Bỏ chọn hết.', 'Bấm Chọn tất cả.'], '—',
       ['Bỏ chọn hết: "Đang chọn 0/7 trường", nút Xuất file bị khóa.', 'Chọn tất cả: 7/7.'], [216, 218])
S6.add('Xuất theo ô tìm nhanh, nhiều trang', 'P1', PRE, [MENU, 'Tìm "0987" (216 khách, 22 trang).', 'Xuất file.'], '—',
       ['File chứa đủ 216 khách (không chỉ trang đang xem), mỗi khách đủ dòng công ty.', 'Hiện tiến độ "Đã tải x/y dòng…".'],
       [219, 221, 227])
S6.add('Xuất danh sách rỗng', 'P0', PRE, [MENU, 'Tìm "ZZZ999".', 'Xuất file.'], '—',
       ['Thông báo "Không có dữ liệu để xuất", KHÔNG tạo file.'], 222)
S6.add('Định dạng số và chữ tiếng Việt', 'P1', [PRE, KH2], [MENU, 'Lọc 29TPHPNG-26, xuất file.'], '—',
       ['Hạn mức là ô SỐ dạng 500,000,000 (cộng được), chưa khai thì trống.', 'Tên khách, tên công ty, "Theo thời gian thanh toán" '
        'đúng dấu tiếng Việt.'], [229, 230])

# ============================================================== VII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S7 = Sec(7)
S7.add('Khách chưa có dòng: dựng dòng trống mọi công ty', 'P0', [ACC_D, KH3], [MENU, 'Lọc 65TPHPAN-03.'], '—',
       ['9 dòng trống theo 9 công ty trong hệ thống.'], [268, 283])
S7.add('Khách đã có dòng: không thêm công ty khác', 'P0', [PRE, KH2], [MENU, 'Lọc 29TPHPNG-26.'], '—',
       ['Chỉ 7 dòng đã có; KHÔNG có dòng Giải pháp Etek Green để khai (giữ như hệ thống cũ).'], [269, 283])
S7.add('Người chỉ có quyền Quản lý lưu làm mất dòng công ty khác', 'P0', [ACC_B, KH1],
       [MENU, LOC_KH1, 'Quan sát dòng hiện.', 'Nhập hạn mức dòng Tân Phát Sài Gòn, Lưu.', 'A mở lại khách này.'], '—',
       ['B chỉ thấy 1 dòng Tân Phát Sài Gòn.', 'Sau khi B lưu: A chỉ còn thấy 1 dòng Tân Phát Sài Gòn — 8 dòng khác (kể cả Tân Phát '
        '120,000) bị xoá. Lưu ý: giữ như hệ thống cũ, user chốt 14/10/2026.', 'Lịch sử ghi dòng Tân Phát 120,000 thành (trống).'],
       [285, 286])
S7.add('Lưu nhiều lần không sinh dòng trùng', 'P1', [PRE, KH1], [MENU, LOC_KH1, 'Lưu 3 lần với giá trị khác nhau.', 'Xuất Excel.'], '—',
       ['File vẫn đúng 9 dòng, mỗi công ty 1 dòng.'], [285, 286])
S7.add('Đổi tên / mã khách ở danh mục', 'P1', [PRE, KH1], ['Ở danh mục Khách hàng đổi tên 43TPHDKH thành "NGUYEN VAN TEST 2".', MENU,
                                                         LOC_KH1], '—',
       ['Màn hiện tên mới, hạn mức giữ nguyên.', 'Đổi mã khách cũng không mất hạn mức (gắn theo khách, không theo mã).'],
       [272, 278, 279])
S7.add('Khách mới tạo hiện ngay', 'P1', PRE, ['Tạo khách mới "KH TEST HM" ở danh mục Khách hàng.', MENU, 'Gõ "KH TEST" vào ô Khách hàng.'],
       '—', ['Khách mới đứng đầu danh sách với 9 dòng trống.', 'Ô Khách hàng gợi ý được khách mới.'], [274, 282])
S7.add('Báo cáo hạn mức đọc đúng giá trị', 'P0', [PRE, KH2],
       [MENU, 'Lọc 29TPHPNG-26, ghi lại dòng Tân Phát.', 'Mở "Báo cáo hạn mức công nợ khách hàng", lọc cùng khách.'], '—',
       ['Báo cáo: Hạn mức tính lãi 0, Hạn mức xuất hàng 500,000,000 (khớp màn khai báo; trống ở màn khai báo = 0 ở báo cáo).',
        'Sửa hạn mức ở màn khai báo thì báo cáo đổi ngay.'], [274, 281])
S7.add('Gửi duyệt Yêu cầu xuất hàng vượt hạn mức', 'P0',
       [PRE, 'Khách 43TPHDKH: Hạn mức công nợ xuất hàng Tân Phát 120,000; công nợ hiện tại 0.'],
       ['A lập Yêu cầu xuất hàng loại "Xuất bán hàng" cho khách, giá trị sau thuế 200,000.', 'Bấm gửi duyệt.'], '—',
       ['Hệ thống hỏi xác nhận "Yêu cầu vượt hạn mức công nợ xuất hàng cho khách hàng (120,000 VNĐ)…".',
        'Đồng ý thành phiếu sang "Đợi TP duyệt".', 'Đổi hạn mức lên 300,000 rồi gửi phiếu khác 200,000 thành không hỏi, phiếu "Chờ duyệt".'],
       [281])
S7.add('Hạn mức trống / 0 thì không kiểm vượt', 'P1', [PRE, KH3], ['Lập Yêu cầu xuất bán hàng mượn cho 65TPHPAN-03, gửi.'], '—',
       ['Không bị chuyển chờ Trưởng phòng duyệt vì khách chưa khai Hạn mức công nợ xuất hàng.'], [281])

# ============================================================== VIII. PHÂN QUYỀN
S8 = Sec(8)
S8.add('Không có quyền nào vẫn xem được', 'P0', [ACC_C, KH1], [MENU, LOC_KH1], '—',
       ['Thấy menu, vào được màn, thấy đủ 9 dòng mọi công ty.', 'Mọi ô là chữ, KHÔNG có nút Lưu; vẫn có Lịch sử, Xuất Excel, Cấu hình '
        'cột.'], [287, 293, 294, 295])
S8.add('Chỉ quyền Xem', 'P0', [ACC_D, KH1], [MENU, LOC_KH1], '—',
       ['Như không có quyền: thấy mọi công ty, không sửa được, không có nút Lưu.'], [287, 295])
S8.add('Quyền Quản lý + Xem', 'P0', [PRE, KH1], [MENU, LOC_KH1], '—',
       ['Thấy 9 dòng mọi công ty; chỉ dòng Tân Phát có ô nhập; có nút Lưu.'], [290, 299])
S8.add('Chỉ quyền Quản lý: chỉ thấy dòng công ty mình', 'P0', [ACC_B, KH1], [MENU, LOC_KH1], '—',
       ['Khách chỉ hiện 1 dòng Tân Phát Sài Gòn (khách chưa có dòng này thì hiện 1 dòng trống của công ty mình).',
        'Dòng đó có ô nhập + nút Lưu.'], [289, 290, 299])
S8.add('Quản lý không sửa được khách thiếu dòng công ty mình', 'P1', [PRE, 'Tài khoản E: kế toán công ty Cổ phần Giải pháp Etek Green, có cả 2 quyền của màn.', KH2],
       [MENU, 'Lọc 29TPHPNG-26.'], '—', ['Không có ô nhập, không có nút Lưu ở khách này (không có dòng Giải pháp Etek Green).'], [295, 299])
S8.add('Mở đường dẫn màn khi không có quyền', 'P1', [ACC_C], ['Dán đường dẫn màn (sao từ tài khoản A) vào trình duyệt của C.'], '—',
       ['Mở được màn ở chế độ chỉ xem (màn không chặn quyền xem), không có ô nhập.'], 296)
S8.add('Bị thu hồi quyền Quản lý khi đang mở màn', 'P0', [PRE, KH1],
       [MENU, LOC_KH1, 'Quản trị gỡ quyền Quản lý của A.', 'A (chưa tải lại) sửa hạn mức, bấm Lưu.'], '—',
       ['Hệ thống từ chối, báo ' + NOPERM + ', không lưu.', 'Tải lại trang: không còn ô nhập, không còn nút Lưu.'], [297, 298])
S8.add('Đổi công ty đang làm việc', 'P0', [PRE, 'A có vai trò ở cả Tân Phát và Tân Phát Sài Gòn.', KH1],
       [MENU, LOC_KH1, 'Đổi công ty đang làm việc sang Tân Phát Sài Gòn, mở lại màn.'], '—',
       ['Ô nhập chuyển sang dòng Tân Phát Sài Gòn; dòng Tân Phát thành chữ.'], [298, 299])
S8.add('Super admin không được đặc cách', 'P2', ['Tài khoản Super admin không được cấp 2 quyền của màn.', KH1], [MENU, LOC_KH1], '—',
       ['Chỉ xem, không có nút Lưu (quyền tính theo vai trò được cấp).'], 299)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'CHỈNH SỬA', S3),
    ('IV', 'LỊCH SỬ THAY ĐỔI', S4),
    ('V', 'TÙY CHỈNH CỘT', S5),
    ('VI', 'XUẤT DANH SÁCH EXCEL', S6),
    ('VII', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S7),
    ('VIII', 'PHÂN QUYỀN', S8),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
check_no_dash_pre(SECTIONS, [])
_ids = ['TC_%02d.%s' % (s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
assert len(_ids) == len(set(_ids)), 'Trùng TC ID'

if __name__ == '__main__':
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='Khai báo hạn mức công nợ KH - Cập nhật ngày 18/11/2026',
                module_name='Khai báo hạn mức công nợ KH', description_block=DESCRIPTION_BLOCK, sections=SECTIONS,
                loai='danh_muc')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

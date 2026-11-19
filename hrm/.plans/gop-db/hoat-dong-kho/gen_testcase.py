# -*- coding: utf-8 -*-
"""Testcase màn "Hoạt động kho" (phân hệ Kho, mục cấp 1) — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026
(tc_chuan.build_chuan, loai='bao_cao').

Chạy: python gen_testcase.py -> testcase.xlsx (sau đó chạy check_tc ... bao_cao, phải 0 lỗi).
LOẠI 'bao_cao' (đọc code 10/11/2026): màn THEO DÕI chỉ đọc — 1 API GET, không Thêm / Sửa / Xóa / Khóa / Duyệt / Import / Lịch sử; có
khối tổng hợp đếm số phiếu (Tổng số phiếu nhận / Tổng hoàn thành / Tổng chưa xử lý) + trạng thái và Tổng thời gian xử lý suy ra từ mốc
thời gian thì cần nhóm SỐ LIỆU BÁO CÁO để đối soát với màn Phiếu đề nghị xuất / nhập kho; loại 'danh_muc' không có nhóm đó. (Tô màu dòng
theo thời gian chờ ĐÃ BỎ 29/10/2026 — #11901, nên không có case ngưỡng màu.)
Nhóm có mặt: I Hiển thị · II Tìm kiếm & lọc · III Số liệu báo cáo · IV Xem chi tiết (mở phiếu đề nghị ở tab mới) · V Tùy chỉnh cột ·
VI Xuất danh sách Excel · VII Ràng buộc · VIII Phân quyền (theo PHẠM VI KHO — màn không gắn quyền). Không có In thì bỏ nhóm.
Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../tong-hop-xuat-nhap-ton/gen_testcase.py (09/11, check_tc 0 lỗi).
Số liệu mẫu dev-hrm 10/11/2026 (_capture/doisoat.js, chỉ đọc): kho PTT 54 phiếu = 39 đề nghị xuất + 15 đề nghị nhập (33 Đã nhận đề nghị,
12 Đang lấy hàng, 9 Đang xếp hàng, 0 Đã hoàn thành); kho MT 5 = 1 + 4; KTCN 2 = 2 + 0.
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
from tc_chuan import build_chuan  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Kho > bấm mục "Hoạt động kho" (mục cấp 1, không có nhóm con).'
EMPTY = 'Không có dữ liệu phù hợp'
LOADERR = 'Lỗi khi tải dữ liệu'
FILE = 'hoat_dong_kho.xlsx'
DNXK = 'Phiếu đề nghị xuất kho'
DNNK = 'Phiếu đề nghị nhập kho'
ACC_K = ('Tài khoản K: là Thủ kho DUY NHẤT của kho PTT - Phan Trọng Tuệ (danh mục Kho vật lý), không là thủ kho kho khác.\n'
         'Kho PTT hôm nay 10/11/2026 có 54 phiếu đang xử lý: 39 %s + 15 %s; 33 Đã nhận đề nghị, 12 Đang lấy hàng, 9 Đang xếp hàng, '
         '0 Đã hoàn thành.' % (DNXK, DNNK))
ACC_K2 = 'Tài khoản K2: là Thủ kho của 2 kho PTT (54 phiếu) và MT - Kho Miền Trung (5 phiếu: 1 đề nghị xuất, 4 đề nghị nhập).'
ACC_N = 'Tài khoản N: không là Thủ kho của kho nào.'
ACC_SA = 'Tài khoản DNS Admin: vai trò Super Admin.'
OPEN = [MENU]
VIEW_DNXK = 'Vào phân hệ Kho > menu "Xuất kho" > "Phiếu đề nghị xuất kho".'
VIEW_DNNK = 'Vào phân hệ Kho > menu "Nhập kho" > "Phiếu đề nghị nhập kho".'
TIP_KHOI = ('HOẠT ĐỘNG KHO • Phiếu đề nghị xuất kho và đề nghị nhập kho của các kho bạn là thủ kho • Gồm phiếu đang xử lý và phiếu '
            'nhận trong hôm nay (kể cả đã hoàn thành) • Danh sách tự tải lại mỗi 60 giây')
COLS = ('STT, Phiếu đề nghị, Loại, Người yêu cầu, Hình thức vận chuyển, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn '
        'thành, Trạng thái, Tổng thời gian xử lý')
FIELDS = ('Phiếu đề nghị, Loại, Người yêu cầu, Hình thức vận chuyển, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn '
          'thành, Trạng thái, Tổng thời gian xử lý')
TEST_ENV = 'Môi trường kiểm thử (không làm trên dữ liệu thật).'

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
     'Bảng theo dõi việc của thủ kho: liệt kê %s và %s của các kho người dùng là Thủ kho — phiếu đang xử lý và phiếu nhận trong hôm nay '
     '— kèm 3 ô tổng hợp (Tổng số phiếu nhận, Tổng hoàn thành, Tổng chưa xử lý), tự tải lại mỗi 60 giây. Màn chỉ đọc: có tìm theo mã, '
     'sắp xếp, mở phiếu ở tab mới, Tùy chỉnh cột, Xuất Excel.' % (DNXK, DNNK)),
    ('2. Đối tượng được tính / hiển thị',
     '- Phiếu đề nghị xuất / nhập kho thuộc kho mình là Thủ kho, trạng thái phiếu Chờ duyệt hoặc Đang xuất kho / Đang nhập kho (bất kể '
     'ngày).\n'
     '- Phiếu có Thời gian nhận từ 00:00 hôm nay, trạng thái Đã xuất / nhập kho, Đang / Đã hạch toán (hiện dòng "Đã hoàn thành" tới hết '
     'ngày).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo, Đã hủy.\n- Phiếu đã xong mà Thời gian nhận trước hôm nay.\n- Phiếu của kho mình không là Thủ kho.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Không có ô lọc thời gian. Mốc "hôm nay" tính theo Thời gian nhận từ 00:00 ngày hiện tại (qua ngày, phiếu xong hôm trước tự rời '
     'bảng).'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Bảng phẳng 11 cột, mỗi phiếu 1 dòng (đề nghị xuất và đề nghị nhập trộn chung), không phân trang. Mặc định: phiếu chưa hoàn thành '
     'trước, trong nhóm Thời gian nhận mới nhất trước.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Mỗi phiếu đúng 1 dòng (phiếu xuất và phiếu nhập trùng số thứ tự vẫn là 2 dòng riêng).\n'
     '- Trạng thái: có Thời gian hoàn thành thì Đã hoàn thành; có Thời gian lấy/xếp hàng thì Đang lấy hàng (đề nghị xuất) / Đang xếp hàng '
     '(đề nghị nhập); còn lại thì Đã nhận đề nghị.'),
    ('7. Phân quyền cấp',
     '- Màn KHÔNG gắn quyền: ai đăng nhập cũng mở được.\n- Phạm vi theo kho: chỉ phiếu của các kho mình là Thủ kho; không là thủ kho kho '
     'nào thì bảng trống.\n- Super Admin: theo thiết kế xem mọi kho (TC_08.004).'),
    ('8. Cách tính các ô thống kê',
     '- Tổng số phiếu nhận = số dòng của bảng (sau tìm kiếm).\n- Tổng hoàn thành = số dòng "Đã hoàn thành".\n'
     '- Tổng chưa xử lý = Tổng số phiếu nhận - Tổng hoàn thành.\n'
     '- Tổng thời gian xử lý = Thời gian hoàn thành - Thời gian nhận, dạng "x ngày y giờ z phút", dưới 1 phút "Vài giây".'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản: K (thủ kho PTT), K2 (thủ kho PTT + MT), N (không là thủ kho), DNS Admin (Super Admin).\n'
     '- Lưu ý: số liệu thay đổi theo thời gian thực (tự tải lại 60 giây) — chụp lại số trước khi đối soát.\n'
     '- Lưu ý: không phân trang, không có ô lọc nâng cao; nhóm Phân trang của checklist kiểm theo dạng "mọi dòng trên 1 trang".\n'
     '- Lưu ý: dev 10/11/2026 DNS Admin (Super Admin, không là thủ kho kho nào) thấy 0 phiếu — lệch thiết kế, đã báo (TC_08.004).\n'
     '- Lưu ý: không còn tô màu dòng theo thời gian chờ (bỏ theo yêu cầu 29/10/2026).'),
]

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', ACC_K, OPEN, '—',
       ['Mở màn "Hoạt động kho", không báo lỗi.', 'Khối "Bộ lọc danh sách", khối "PHIẾU NHẬN" (54 / 0 / 54) và bảng 54 dòng.'], [1, 6])
S1.add('Tiêu đề màn hình', 'P1', ACC_K, OPEN + ['Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.', 'Rê chuột vào chữ i cạnh tiêu đề trang.'],
       '—', ['Cả 3 nơi là "Hoạt động kho".',
             'Chữ i hiện: "Theo dõi phiếu đề nghị xuất kho / nhập kho của các kho bạn là thủ kho: phiếu đang xử lý và phiếu nhận trong hôm '
             'nay. Phiếu chưa hoàn thành xếp trên, phiếu đã hoàn thành xếp dưới cùng."'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', ACC_K, OPEN + ['Quan sát các khối.'], '—',
       ['Khối lọc: ô "Tìm theo mã phiếu đề nghị", nút Tìm kiếm, Làm mới.', 'Khối PHIẾU NHẬN: nút Thu gọn.',
        'Đầu bảng: Xuất Excel, biểu tượng Cấu hình cột hiển thị.',
        'KHÔNG có Tạo mới, Sửa, Xóa, Import, In, cột Hành động, Tìm kiếm nâng cao, Cài đặt bộ lọc.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', ACC_K, OPEN + ['Đọc tiêu đề cột.'], '—',
       ['Đủ 11 cột: %s.' % COLS, 'Biểu tượng sắp xếp ở 5 cột: Phiếu đề nghị, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn thành.'], 4)
S1.add('Không có cột ẩn mặc định', 'P2', ACC_K, OPEN + ['Bấm Cấu hình cột hiển thị.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" tích đủ 11 cột, "Đang chọn 11/11 cột"; không cột nào ẩn sẵn.'], 5)
S1.add('Dữ liệu dòng đúng với phiếu', 'P0', ACC_K, OPEN + ['Đọc dòng 1.', 'Mở phiếu PDNXK-39053 ở màn Phiếu đề nghị xuất kho để so.'], '—',
       ['Dòng 1: PDNXK-39053, Xuất mượn, DNS Admin, Công ty vận chuyển, PTT - Phan Trọng Tuệ, 29/10/2026 15:53, 29/10/2026 15:56, trống, '
        'Đang lấy hàng, trống.', 'Kho, mã, thời gian khớp phiếu gốc; Người yêu cầu = người lập Yêu cầu xuất hàng gốc.'], 6)
S1.add('Nhãn trạng thái của dòng', 'P0', ACC_K, OPEN + ['Đọc cột Trạng thái các dòng.'], '—',
       ['Phiếu chưa có Thời gian lấy/xếp hàng: nhãn cam "Đã nhận đề nghị".',
        'Đề nghị xuất có Thời gian lấy hàng: nhãn xanh dương "Đang lấy hàng"; đề nghị nhập: "Đang xếp hàng".',
        'Không có trạng thái Khóa / Hoạt động.'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', ACC_N, ['Đăng nhập N.'] + OPEN, '—',
       ['Bảng hiện "%s".' % EMPTY, 'Khối PHIẾU NHẬN: 0 / 0 / 0 phiếu; không báo lỗi.'], [8, 38])
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', ACC_K, OPEN + ['Nhập "ZZZ999" vào ô tìm nhanh, nhấn Enter.'], 'Tìm: ZZZ999',
       ['Bảng hiện "%s"; 3 ô tổng hợp = 0.' % EMPTY], [9, 30, 40])
S1.add('Mọi phiếu nằm trên một trang', 'P0', ACC_K, OPEN + ['Cuộn hết bảng.'], '—',
       ['54 dòng trên 1 trang, STT 1 đến 54 liên tục.', 'Không có ô Số dòng/trang, nút trang, dòng "Hiển thị a–b / N" (màn không phân trang).'],
       [10, 11, 12, 13, 14, 15, 18])
S1.add('Tổng số bản ghi', 'P0', ACC_K, OPEN, '—', ['Ô "Tổng số phiếu nhận" = 54 = số dòng bảng.'], [16, 37])
S1.add('Thứ tự mặc định', 'P0', ACC_K, OPEN, '—',
       ['Phiếu chưa hoàn thành ở trên, Thời gian nhận mới nhất trước: 1 PDNXK-39053 (29/10 15:53), 2 PDNXK-39035 (21/10 14:59), 3 '
        'PDNXK-39034 (21/10 14:59)…', 'Phiếu "Đã hoàn thành" (nếu có) luôn ở cuối.'], 19)
S1.add('Sắp xếp tăng dần', 'P0', ACC_K, OPEN + ['Bấm tiêu đề "Phiếu đề nghị".'], '—',
       ['Mũi tên lên; mã xếp A đến Z: PDNNK-07592, PDNNK-09815, PDNNK-10376…'], 20)
S1.add('Sắp xếp giảm dần', 'P0', ACC_K, OPEN + ['Bấm "Phiếu đề nghị" 2 lần.'], '—',
       ['Mũi tên xuống; mã xếp Z đến A, đầu bảng PDNXK-39053.'], 21)
S1.add('Sắp xếp theo cột thời gian', 'P1', ACC_K, OPEN + ['Bấm "Thời gian nhận".', 'Bấm "Thời gian lấy/xếp hàng" 2 lần.'], '—',
       ['Thời gian nhận tăng dần: phiếu cũ nhất (18/06/2026) lên đầu.',
        'Thời gian lấy/xếp hàng giảm dần: phiếu có mốc mới nhất lên đầu, phiếu trống mốc xuống cuối.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', ACC_K, OPEN + ['Bấm tiêu đề Loại, Người yêu cầu, Trạng thái, Tổng thời gian xử lý.'], '—',
       ['Không có biểu tượng sắp xếp, thứ tự không đổi.'], 23)
S1.add('Sắp xếp theo Kho với 2 kho', 'P1', ACC_K2, ['Đăng nhập K2.'] + OPEN + ['Bấm "Kho".'], '—',
       ['59 dòng; phiếu kho MT (mã MT) xếp sau kho PTT theo mã kho tăng dần; trong cùng kho theo thứ tự mặc định.'], [20, 24])
S1.add('Đổi sắp xếp giữ từ khóa', 'P2', ACC_K, OPEN + ['Tìm "PDNNK".', 'Bấm "Thời gian nhận".'], 'Tìm: PDNNK',
       ['Vẫn 15 dòng đề nghị nhập, xếp theo Thời gian nhận tăng dần (không có trang để về trang 1).'], [25, 43])
S1.add('Thu gọn / mở rộng khối tổng hợp', 'P2', ACC_K, OPEN + ['Bấm Thu gọn.', 'Bấm Mở rộng.'], '—',
       ['Thu gọn: ẩn 3 ô, nút đổi "Mở rộng".', 'Mở rộng: hiện lại, số không đổi; bảng không tải lại.'], 3)
S1.add('Tự tải lại sau 60 giây', 'P0', [ACC_K, TEST_ENV], OPEN + ['Để màn mở.', 'Ở tab khác, gửi thủ kho 1 Phiếu đề nghị xuất kho mới của kho PTT.',
                                                                  'Quay lại, chờ tối đa 60 giây, không bấm gì.'], '—',
       ['Phiếu mới tự xuất hiện ở đầu bảng, Tổng số phiếu nhận 55, Tổng chưa xử lý 55.', 'Không hiện vòng tải, không báo lỗi.'], [40, 281])
S1.add('Tải lại thất bại không báo lỗi', 'P2', [ACC_K, 'Mạng chập chờn.'], OPEN + ['Ngắt mạng 70 giây, rồi bật lại.'], '—',
       ['Trong lúc mất mạng không hiện thông báo; bảng giữ dữ liệu cũ.', 'Có mạng lại, lượt kế tiếp cập nhật bình thường.'], 40)
S1.add('Phiên đăng nhập hết hạn', 'P2', [ACC_K, 'Phiên đăng nhập đã hết hạn.'], OPEN + ['Bấm Tìm kiếm.'], '—',
       ['Chuyển về màn đăng nhập, không hiện dữ liệu.'], 39)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm đúng mã đầy đủ', 'P0', ACC_K, OPEN + ['Nhập "PDNXK-39053", bấm Tìm kiếm.'], 'Tìm: PDNXK-39053',
       ['Còn 1 dòng PDNXK-39053.', 'Khối PHIẾU NHẬN: 1 / 0 / 1.'], [26, 41, 39])
S2.add('Tìm một phần mã', 'P0', ACC_K, OPEN + ['Nhập "39053", nhấn Enter.'], 'Tìm: 39053', ['Còn 1 dòng PDNXK-39053.'], 27)
S2.add('Tìm theo tiền tố loại phiếu', 'P1', ACC_K, OPEN + ['Nhập "PDNNK", nhấn Enter.'], 'Tìm: PDNNK',
       ['Còn 15 dòng, đều là Phiếu đề nghị nhập kho; Tổng số phiếu nhận 15.'], [27, 37])
S2.add('Không phân biệt hoa thường', 'P0', ACC_K, OPEN + ['Nhập "pdnnk", nhấn Enter.'], 'Tìm: pdnnk', ['Kết quả 15 dòng như khi nhập "PDNNK".'], 28)
S2.add('Có dấu / không dấu', 'P2', ACC_K, OPEN + ['Nhập "PĐNNK" (chữ Đ), nhấn Enter.'], 'Tìm: PĐNNK',
       ['Kết quả theo cách so chữ của hệ thống; mã phiếu không có dấu nên chỉ cần kiểm không lỗi, không treo.'], 29)
S2.add('Ký tự đặc biệt', 'P1', ACC_K, OPEN + ['Lần lượt nhập "%", "_", "\'", nhấn Enter.'], 'Tìm: % ; _ ; \'',
       ['"%" và "_" được tìm đúng nghĩa đen (không ra toàn bộ) thì "' + EMPTY + '".', 'Không báo lỗi hệ thống.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', ACC_K, OPEN + ['Nhập "  39053  ", nhấn Enter.'], 'Tìm: "  39053  "',
       ['Bỏ khoảng trắng 2 đầu, ra 1 dòng PDNXK-39053.'], 32)
S2.add('Chuỗi dài', 'P2', ACC_K, OPEN + ['Dán chuỗi 300 ký tự, nhấn Enter.'], 'Chuỗi 300 ký tự',
       ['Ô nhận đủ (không giới hạn ký tự); bảng "%s"; không lỗi.' % EMPTY], 33)
S2.add('Xóa từ khóa bằng dấu ×', 'P1', ACC_K, OPEN + ['Tìm "39053".', 'Bấm × trong ô tìm.', 'Bấm Tìm kiếm.'], '—',
       ['Sau bấm ×: ô trống, bảng chưa đổi (vẫn 1 dòng).', 'Sau Tìm kiếm: lại 54 dòng.'], 34)
S2.add('Gõ chưa bấm Tìm kiếm thì chưa lọc', 'P1', ACC_K, OPEN + ['Nhập "39053", không bấm gì (dưới 60 giây).'], 'Tìm: 39053',
       ['Bảng vẫn 54 dòng.', 'Bấm Tìm kiếm hoặc Enter mới còn 1 dòng.'], 35)
S2.add('Chữ đang gõ được áp khi sắp xếp / tự tải lại', 'P2', ACC_K, OPEN + ['Nhập "PDNNK", không bấm Tìm kiếm.', 'Bấm tiêu đề "Kho".'],
       'Tìm: PDNNK', ['Bảng còn 15 dòng đề nghị nhập (chữ đang gõ được áp cùng sắp xếp); để yên 60 giây cũng vậy.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', ACC_K, ['Rời màn sang màn khác.'] + OPEN, '—',
       ['Ô tìm trống, chưa sắp xếp, bảng đủ 54 dòng.', 'Màn không có ô lọc nào khác (bộ lọc gọn).'], [36, 37, 38])
S2.add('Tìm kết hợp sắp xếp', 'P2', ACC_K, OPEN + ['Bấm "Thời gian nhận" (tăng).', 'Tìm "PDNXK".'], 'Tìm: PDNXK',
       ['39 dòng đề nghị xuất, vẫn theo Thời gian nhận tăng dần.'], [39, 43])
S2.add('Tổng số sau tìm', 'P0', ACC_K, OPEN + ['Tìm "PDNXK".'], 'Tìm: PDNXK',
       ['Tổng số phiếu nhận 39, Tổng chưa xử lý 39; STT 1–39 (không có phân trang).'], [41, 42])
S2.add('Làm mới', 'P0', ACC_K, OPEN + ['Tìm "39053".', 'Bấm "Phiếu đề nghị" để sắp xếp.', 'Bấm Làm mới.'], '—',
       ['Ô tìm trống, bỏ sắp xếp (về thứ tự mặc định), 54 dòng, 3 ô 54 / 0 / 54.'], 44)
S2.add('Tải lại trang giữ từ khóa', 'P1', ACC_K, OPEN + ['Tìm "39053".', 'Nhấn F5 (trong 10 phút).'], '—',
       ['Ô tìm vẫn "39053", bảng còn 1 dòng; sắp xếp về mặc định.'], 46)
S2.add('Chuyển màn rồi quay lại', 'P0', ACC_K, OPEN + ['Tìm "39053".', 'Vào màn khác từ menu.', 'Quay lại Hoạt động kho từ menu.'], '—',
       ['Ô tìm trống, bảng 54 dòng (từ khóa bị xóa khi rời màn).'], 45)
S2.add('Mở ở tab mới', 'P2', ACC_K, OPEN + ['Tìm "39053".', 'Mở Hoạt động kho ở tab mới trong 10 phút.'], '—',
       ['Tab mới hiện sẵn "39053" (ghi tạm trên trình duyệt, chung các tab), 1 dòng.'], 47)
S2.add('Tài khoản khác cùng trình duyệt', 'P2', [ACC_K, ACC_K2], OPEN + ['K tìm "39053", đăng xuất.', 'K2 đăng nhập, mở màn trong 10 phút.'], '—',
       ['K2 thấy ô tìm "39053" (ghi tạm theo trình duyệt, không theo tài khoản); bấm Làm mới để xóa. Dữ liệu vẫn theo kho của K2.'], 48)
S2.add('Máy chủ lỗi khi tìm', 'P2', [ACC_K, 'Máy chủ tạm lỗi.'], OPEN + ['Bấm Tìm kiếm.'], '—',
       ['Thông báo "%s"; bảng giữ dữ liệu cũ.' % LOADERR], 40)

# ============================================================== III. SỐ LIỆU BÁO CÁO
S3 = Sec(3)
S3.add('Ô tổng hợp bằng số dòng bảng', 'P0', ACC_K, OPEN + ['Đếm dòng bảng theo cột Trạng thái.'], '—',
       ['Tổng số phiếu nhận 54 = số dòng.', 'Tổng hoàn thành 0 = số dòng "Đã hoàn thành".',
        'Tổng chưa xử lý 54 = 54 - 0 = 33 Đã nhận đề nghị + 12 Đang lấy hàng + 9 Đang xếp hàng.'], [16, 37])
S3.add('Đối soát dòng đề nghị xuất với màn Phiếu đề nghị xuất kho', 'P0', ACC_K,
       OPEN + ['Tìm "PDNXK" ở Hoạt động kho, ghi danh sách mã.', VIEW_DNXK, 'Lọc Kho = PTT, Trạng thái = Chờ duyệt; rồi Trạng thái = Đang xuất kho.'],
       '—', ['Hoạt động kho 39 dòng = tổng 2 lần lọc (Chờ duyệt + Đang xuất kho) ở màn Phiếu đề nghị xuất kho, khớp ĐÚNG từng mã.'], [6, 274])
S3.add('Đối soát dòng đề nghị nhập với màn Phiếu đề nghị nhập kho', 'P0', ACC_K,
       OPEN + ['Tìm "PDNNK", ghi danh sách mã.', VIEW_DNNK, 'Lọc Kho = PTT, Trạng thái = Chờ duyệt; rồi Đang nhập kho.'], '—',
       ['15 dòng = tổng 2 lần lọc, khớp đúng từng mã.'], [6, 274])
S3.add('Đối soát với màn Theo dõi theo kho', 'P1', [ACC_K, 'Tài khoản K có quyền Quản lý kho.'],
       OPEN + ['Vào phân hệ Kho > "Theo dõi theo kho", bấm kho PTT.'], '—',
       ['Bảng hoạt động của kho PTT trùng từng dòng, cùng thứ tự, cùng 3 ô (54 / 0 / 54) với Hoạt động kho của K.'], [6, 274])
S3.add('Phiếu Đang tạo / Đã hủy không hiện', 'P0', [ACC_K, 'Kho PTT có phiếu PDNXK đang Đang tạo và 1 phiếu Đã hủy hôm nay.'], OPEN + ['Tìm mã 2 phiếu đó.'],
       '—', ['Cả 2 không có trên bảng; không tính vào ô tổng hợp.'], [6, 281])
S3.add('Trạng thái Đã nhận đề nghị', 'P0', [ACC_K, TEST_ENV], ['Gửi thủ kho 1 Phiếu đề nghị xuất kho kho PTT.'] + OPEN, '—',
       ['Dòng mới: Thời gian nhận = lúc gửi, Thời gian lấy hàng trống, nhãn cam "Đã nhận đề nghị".'], [7, 281])
S3.add('Chuyển sang Đang lấy hàng khi lập phiếu xuất kho', 'P0', [ACC_K, TEST_ENV, 'Phiếu đề nghị xuất kho X đang "Đã nhận đề nghị".'],
       ['Lập Phiếu xuất kho cho X (Tài chính > Xuất hàng > Phiếu xuất kho).'] + OPEN, '—',
       ['Dòng X: Thời gian lấy/xếp hàng = lúc lập, nhãn xanh dương "Đang lấy hàng"; Tổng chưa xử lý không đổi.'], [7, 281])
S3.add('Đề nghị nhập kho hiện "Đang xếp hàng"', 'P1', [ACC_K, TEST_ENV, 'Phiếu đề nghị nhập kho Y đang "Đã nhận đề nghị".'],
       ['Lập Phiếu nhập kho cho Y.'] + OPEN, '—', ['Dòng Y nhãn "Đang xếp hàng", Hình thức vận chuyển trống.'], [7, 281])
S3.add('Hoàn thành trong ngày', 'P0', [ACC_K, TEST_ENV, 'Phiếu đề nghị xuất kho X nhận hôm nay 08:00, đang lấy hàng.'],
       ['Gửi Phiếu xuất kho của X lúc 10:15.'] + OPEN, '—',
       ['Dòng X: Thời gian hoàn thành 10:15, nhãn xanh lá "Đã hoàn thành", Tổng thời gian xử lý "2 giờ 15 phút", xuống CUỐI bảng.',
        'Tổng hoàn thành tăng 1, Tổng chưa xử lý giảm 1, Tổng số phiếu nhận không đổi.'], [7, 281])
S3.add('Phiếu hoàn thành rời bảng sang ngày hôm sau', 'P1', [ACC_K, TEST_ENV, 'Có dòng "Đã hoàn thành" nhận hôm nay.'],
       ['Để màn mở qua 00:00, chờ lượt tự tải lại.'], '—',
       ['Dòng đã hoàn thành của hôm trước biến mất; phiếu chưa hoàn thành nhận hôm trước vẫn còn.'], 281)
S3.add('Phiếu xong nhưng nhận từ hôm trước', 'P1', [ACC_K, TEST_ENV, 'Phiếu Z nhận hôm qua, hôm nay gửi Phiếu xuất kho xong.'], OPEN, '—',
       ['Z không có trên bảng (không nhận hôm nay, đã hết Đang xuất kho); không tính vào Tổng hoàn thành.'], 281)
S3.add('Tổng thời gian xử lý dưới 1 phút', 'P2', [ACC_K, TEST_ENV, 'Phiếu nhận 09:00:10, hoàn thành 09:00:40 hôm nay.'], OPEN, '—',
       ['Cột Tổng thời gian xử lý ghi "Vài giây".'], 7)
S3.add('Tổng thời gian xử lý trên 1 ngày', 'P2', [ACC_K, TEST_ENV, 'Phiếu nhận hôm nay 00:05 (gửi lại), hoàn thành 26 giờ 3 phút sau.'],
       OPEN, '—', ['Ghi "1 ngày 2 giờ 3 phút" (bỏ phần bằng 0, vd đúng 1 ngày: "1 ngày").'], 7)
S3.add('Người yêu cầu và Hình thức vận chuyển', 'P1', ACC_K, OPEN + ['Mở Yêu cầu xuất hàng gốc của PDNXK-39034.'], '—',
       ['Người yêu cầu "Tạ Xuân Quyết" = người lập Yêu cầu xuất hàng; Hình thức vận chuyển "Khách hàng vận chuyển" = của yêu cầu đó.',
        'Dòng đề nghị nhập kho luôn trống Hình thức vận chuyển.'], 6)
S3.add('Tên Loại theo bảng tên hệ thống cũ', 'P2', ACC_K, OPEN, '—',
       ['Loại hiện đúng tên: "Xuất mượn", "Xuất khuyến mại (HĐ hãng)", "Xuất bán (HĐH)", "Xuất điều chuyển kho chi nhánh", '
        '"Nhập hàng mượn trả lại", "Nhập hàng mua trong nước (TỰ DO + HÃNG)"; không có dòng Loại trống.'], 6)
S3.add('Ô tổng hợp theo kết quả tìm', 'P0', ACC_K, OPEN + ['Tìm "PDNXK-3901".'], 'Tìm: PDNXK-3901',
       ['3 ô đếm lại đúng trên các dòng còn lại (Tổng số phiếu nhận = số dòng hiện).'], [41, 39])
S3.add('Chữ i khối và từng ô tổng hợp', 'P2', ACC_K, OPEN + ['Rê chuột vào chữ i cạnh "PHIẾU NHẬN" và 3 ô.'], '—',
       ['Khối: "%s".' % TIP_KHOI,
        'Tổng số phiếu nhận: "Số phiếu đề nghị xuất kho + đề nghị nhập kho đang hiện ở danh sách bên dưới".',
        'Tổng hoàn thành: "Số phiếu đã hoàn thành (đã có Thời gian hoàn thành)".',
        'Tổng chưa xử lý: "Tổng số phiếu nhận trừ Tổng hoàn thành" và "Gồm phiếu "Đã nhận đề nghị" và phiếu đang lấy hàng / xếp hàng".'], 3)
S3.add('Số trên ô tổng hợp không bấm được', 'P2', ACC_K, OPEN + ['Bấm vào số 54.'], '—', ['Không mở cửa sổ hay màn nào.'], 3)

# ============================================================== IV. XEM CHI TIẾT PHIẾU ĐỀ NGHỊ
S4 = Sec(4)
S4.add('Mở phiếu đề nghị xuất kho từ mã', 'P0', ACC_K, OPEN + ['Bấm mã PDNXK-39053.'], '—',
       ['Mở TAB MỚI màn chi tiết Phiếu đề nghị xuất kho PDNXK-39053; tab Hoạt động kho giữ nguyên.'], [186, 187])
S4.add('Mở phiếu đề nghị nhập kho từ mã', 'P0', ACC_K, OPEN + ['Bấm mã PDNNK-11037.'], '—',
       ['Tab mới mở "Chi tiết đề nghị nhập kho: PDNNK-11037".'], [186, 187])
S4.add('Thông tin chi tiết khớp dòng', 'P1', ACC_K, OPEN + ['Bấm PDNXK-39053.', 'So Kho, Thời gian nhận, Người duyệt / thời gian duyệt.'], '—',
       ['Kho PTT, Thời gian nhận 29/10/2026 15:53, thời gian duyệt 29/10/2026 15:56 khớp dòng ở Hoạt động kho; đủ dòng hàng.'], [188, 189, 190])
S4.add('Chi tiết chỉ đọc khi mở từ Hoạt động kho', 'P1', ACC_K, OPEN + ['Bấm mã phiếu, quan sát màn chi tiết.'], '—',
       ['Màn chi tiết là màn xem; nút thao tác (Sửa, Duyệt, Lập phiếu…) hiện theo quyền và trạng thái của màn phiếu, Hoạt động kho không thêm '
        'nút nào.'], [191, 192, 193])
S4.add('Đóng tab chi tiết giữ trạng thái danh sách', 'P1', ACC_K, OPEN + ['Tìm "PDNXK", bấm "Kho" để sắp xếp.', 'Bấm 1 mã phiếu, đóng tab mới.'], '—',
       ['Tab Hoạt động kho vẫn từ khóa "PDNXK", vẫn sắp theo Kho.'], [196, 197])
S4.add('Xử lý phiếu rồi quay lại', 'P1', [ACC_K, TEST_ENV], OPEN + ['Bấm mã 1 phiếu "Đã nhận đề nghị", lập Phiếu xuất kho ở tab mới.',
                                                                    'Quay lại tab Hoạt động kho, chờ tối đa 60 giây.'], '—',
       ['Dòng đó đổi sang "Đang lấy hàng" ở lượt tự tải lại; không cần F5.'], [196, 281])

# ============================================================== V. TÙY CHỈNH CỘT
S5 = Sec(5)
S5.add('Mở cửa sổ Tuỳ chỉnh cột', 'P0', ACC_K, OPEN + ['Bấm biểu tượng Cấu hình cột hiển thị.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột", hướng dẫn "Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.", 11 cột, "Đang chọn 11/11 cột", '
        'nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng.'], [198, 199, 200])
S5.add('Ẩn cột', 'P0', ACC_K, OPEN + ['Mở Tuỳ chỉnh cột, bỏ tích Người yêu cầu, Hình thức vận chuyển.', 'Bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công"; bảng còn 9 cột.'], [202, 206])
S5.add('Hiện lại cột đã ẩn', 'P1', [ACC_K, 'Đã ẩn cột Người yêu cầu.'], OPEN + ['Mở Tuỳ chỉnh cột, tích Người yêu cầu, Lưu.'], '—',
       ['Cột Người yêu cầu hiện lại đúng vị trí đang xếp.'], 201)
S5.add('Cột khóa không ẩn được', 'P0', ACC_K, OPEN + ['Mở Tuỳ chỉnh cột.', 'Bấm Bỏ chọn hết.'], '—',
       ['STT, Phiếu đề nghị có ổ khóa, luôn tích, không kéo được; "Đang chọn 2/11 cột".'], [203, 205])
S5.add('Kéo thả thứ tự cột', 'P1', ACC_K, OPEN + ['Kéo Trạng thái lên ngay sau Phiếu đề nghị.', 'Lưu.'], '—',
       ['Bảng hiện Trạng thái là cột thứ 3.'], 204)
S5.add('Đóng không lưu', 'P1', ACC_K, OPEN + ['Bỏ tích Kho.', 'Bấm Đóng (hoặc ×, hoặc bấm ra ngoài).'], '—',
       ['Cửa sổ đóng không hỏi; cột Kho vẫn hiện.'], 207)
S5.add('Ghi nhớ sau F5 và đăng nhập lại', 'P1', [ACC_K, 'Đã ẩn cột Loại.'], OPEN + ['Nhấn F5.', 'Đăng xuất, đăng nhập lại trên trình duyệt khác.'],
       '—', ['Cột Loại vẫn ẩn ở cả 2 lần.'], 208)
S5.add('Cấu hình theo từng tài khoản', 'P1', [ACC_K, ACC_K2, 'K đã ẩn cột Loại.'], ['K2 đăng nhập.'] + OPEN, '—',
       ['K2 vẫn thấy đủ 11 cột.'], 209)
S5.add('Không ảnh hưởng dữ liệu và từ khóa', 'P2', ACC_K, OPEN + ['Tìm "PDNNK".', 'Ẩn cột Trạng thái, Lưu.'], '—',
       ['Vẫn 15 dòng, từ khóa giữ; 3 ô tổng hợp không đổi (vẫn đếm cả trạng thái dù cột ẩn).'], [210, 211])

# ============================================================== VI. XUẤT DANH SÁCH EXCEL
S6 = Sec(6)
S6.add('Mở cửa sổ chọn trường', 'P0', ACC_K, OPEN + ['Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất Excel", hướng dẫn "Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.", 10 trường: %s; '
        '"Đang chọn 10/10 trường"; nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng.' % FIELDS], [212, 213])
S6.add('Trường tích sẵn không theo cột ẩn', 'P1', [ACC_K, 'Đã ẩn cột Loại ở Tuỳ chỉnh cột.'], OPEN + ['Bấm Xuất Excel.'], '—',
       ['Vẫn tích đủ 10 trường, kể cả Loại (cửa sổ không theo cấu hình cột).'], 214)
S6.add('Xuất với trường mặc định', 'P0', ACC_K, OPEN + ['Bấm Xuất Excel > Xuất file.'], '—',
       ['Tải file "%s", báo "Xuất Excel thành công.", cửa sổ đóng.' % FILE,
        'File: ảnh letterhead công ty người xuất, tiêu đề "HOẠT ĐỘNG KHO", 11 cột (STT + 10 trường), 54 dòng, khối ký "Người lập".'],
       [215, 223, 224, 227, 128])
S6.add('Chọn tất cả / Bỏ chọn hết', 'P1', ACC_K, OPEN + ['Bấm Xuất Excel.', 'Bấm Bỏ chọn hết.', 'Bấm Chọn tất cả.'], '—',
       ['Bỏ chọn hết: "Đang chọn 0/10 trường", nút Xuất file mờ không bấm được.', 'Chọn tất cả: 10/10.'], [216, 218])
S6.add('Xuất một số trường và đổi thứ tự', 'P0', ACC_K, OPEN + ['Bấm Xuất Excel, chỉ tích Phiếu đề nghị, Trạng thái, Kho.',
                                                                'Kéo Trạng thái lên đầu.', 'Xuất file.'], '—',
       ['File có 4 cột theo đúng thứ tự: STT, Trạng thái, Phiếu đề nghị, Kho.'], [217, 225, 226])
S6.add('Xuất theo từ khóa tìm', 'P0', ACC_K, OPEN + ['Tìm "PDNNK".', 'Xuất file.'], 'Tìm: PDNNK',
       ['File đúng 15 dòng đề nghị nhập kho, cùng thứ tự với bảng.'], [219, 220])
S6.add('Xuất theo sắp xếp đang áp', 'P1', ACC_K, OPEN + ['Bấm "Phiếu đề nghị" (tăng).', 'Xuất file.'], '—',
       ['Dòng 1 file là PDNNK-07592 như bảng.'], [221, 228])
S6.add('Xuất khi danh sách rỗng', 'P1', ACC_K, OPEN + ['Tìm "ZZZ999".', 'Xuất file.'], 'Tìm: ZZZ999',
       ['Vẫn tải file có tiêu đề, hàng tên cột, khối ký, không có dòng dữ liệu; báo "Xuất Excel thành công.".'], 222)
S6.add('Định dạng dữ liệu trong file', 'P1', ACC_K, OPEN + ['Xuất file, mở bằng Excel.'], '—',
       ['Ngày giờ dạng dd/mm/yyyy hh:mm; Trạng thái ghi chữ (vd "Đang lấy hàng"); ô trống để trống.',
        'Tên người, tên kho tiếng Việt đúng dấu; ô dài tự xuống dòng, không bị cắt chữ.'], [229, 230])
S6.add('Đóng cửa sổ không xuất', 'P2', ACC_K, OPEN + ['Bấm Xuất Excel > Đóng (hoặc ×).'], '—', ['Cửa sổ đóng, không tải file.'], 128)
S6.add('Dữ liệu mới nhất lúc xuất', 'P2', [ACC_K, TEST_ENV], OPEN + ['Gửi thủ kho 1 phiếu mới của kho PTT.', 'Ngay lập tức (chưa tới lượt tải lại) bấm Xuất file.'],
       '—', ['File có 55 dòng (lấy lại dữ liệu lúc bấm) dù bảng còn 54.'], 220)

# ============================================================== VII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S7 = Sec(7)
S7.add('Phiếu mới gửi thủ kho xuất hiện', 'P0', [ACC_K, TEST_ENV], ['Lập và gửi thủ kho 1 Phiếu đề nghị nhập kho kho PTT.'] + OPEN, '—',
       ['Dòng mới PDNNK-… "Đã nhận đề nghị" ở đầu nhóm chưa hoàn thành.'], [274, 281])
S7.add('Hủy phiếu thì rời bảng', 'P0', [ACC_K, TEST_ENV, 'Phiếu đề nghị xuất kho X đang "Đã nhận đề nghị".'], ['Hủy X ở màn Phiếu đề nghị xuất kho.'] + OPEN,
       '—', ['X không còn trên bảng; Tổng số phiếu nhận giảm 1.'], [280, 281])
S7.add('Đổi kho của phiếu', 'P1', [ACC_K, TEST_ENV, 'Phiếu nháp được sửa kho từ MT sang PTT rồi gửi thủ kho.'], OPEN, '—',
       ['Phiếu hiện ở Hoạt động kho của K (kho PTT), không còn ở thủ kho MT.'], [278, 282])
S7.add('Đổi tên kho đồng bộ', 'P2', [ACC_K, TEST_ENV], ['Sửa tên kho PTT ở Kho vật lý thành "Phan Trọng Tuệ 2".'] + OPEN, '—',
       ['Cột Kho hiện mã PTT kèm tên mới "Phan Trọng Tuệ 2" ở lượt tải kế tiếp; không mất dòng.'], [278, 279, 284])
S7.add('Thêm thủ kho cho người dùng', 'P1', [ACC_N, TEST_ENV], ['Gán N vào ô Thủ kho của kho MT (Kho vật lý).', 'N mở Hoạt động kho.'], '—',
       ['N thấy 5 phiếu của kho MT.'], [274, 282])
S7.add('Gỡ thủ kho khi đang mở màn', 'P0', [ACC_K2, TEST_ENV], OPEN + ['Ở tab khác gỡ K2 khỏi Thủ kho kho MT.', 'Chờ tối đa 60 giây.'], '—',
       ['5 phiếu kho MT biến mất ở lượt tải lại; còn 54 phiếu PTT.'], [282, 298])
S7.add('Không có dòng trùng / mồ côi', 'P1', ACC_K2, ['Đăng nhập K2.'] + OPEN, '—',
       ['59 dòng, không mã nào lặp; mọi dòng có Kho; phiếu đề nghị xuất và nhập cùng số thứ tự vẫn là 2 dòng riêng.'], [285, 286, 283])

# ============================================================== VIII. PHÂN QUYỀN
S8 = Sec(8)
S8.add('Thủ kho xem kho mình', 'P0', ACC_K, ['Đăng nhập K.'] + OPEN, '—',
       ['Chỉ thấy 54 phiếu của kho PTT; không thấy phiếu kho MT, LN, SG…'], [287, 299])
S8.add('Thủ kho nhiều kho', 'P0', ACC_K2, ['Đăng nhập K2.'] + OPEN, '—', ['Thấy 59 phiếu (54 PTT + 5 MT).'], 299)
S8.add('Không là thủ kho kho nào', 'P0', ACC_N, ['Đăng nhập N.'] + OPEN, '—',
       ['Menu "Hoạt động kho" vẫn hiện, màn mở được.', 'Bảng "%s", 3 ô 0 / 0 / 0, không báo lỗi quyền.' % EMPTY], [287, 295, 299])
S8.add('Super Admin xem mọi kho', 'P0', ACC_SA, ['Đăng nhập DNS Admin.'] + OPEN, '—',
       ['Theo thiết kế (như hệ thống cũ): thấy phiếu của MỌI kho (dev 10/11 ước khoảng 290 phiếu: SG 122, LN 99, PTT 54…).',
        'Lưu ý: dev 10/11/2026 DNS Admin thấy 0 phiếu — đã báo lỗi, chờ xử lý.'], 299)
S8.add('Mở thẳng màn khi không là thủ kho', 'P0', ACC_N, ['Đăng nhập N.', 'Dán địa chỉ màn Hoạt động kho vào trình duyệt.'], '—',
       ['Mở được, bảng trống — không lộ phiếu kho khác.'], 296)
S8.add('Xuất Excel theo phạm vi kho', 'P0', ACC_K2, ['Đăng nhập K2.'] + OPEN + ['Xuất file.'], '—',
       ['File 59 dòng, chỉ kho PTT và MT.'], 293)
S8.add('Mở phiếu khi thiếu quyền xem phiếu', 'P1', [ACC_K, 'K không có quyền xem ở màn Phiếu đề nghị xuất kho.'], OPEN + ['Bấm mã PDNXK-39053.'], '—',
       ['Tab mới xử lý theo quyền của màn Phiếu đề nghị xuất kho (báo không có quyền / không xem được); Hoạt động kho vẫn hiện dòng.'], 288)
S8.add('Không có nút ghi dữ liệu để ẩn', 'P2', ACC_N, ['Đăng nhập N.'] + OPEN, '—',
       ['Mọi người dùng thấy cùng bộ nút (Tìm kiếm, Làm mới, Xuất Excel, Cấu hình cột); không có nút Thêm / Sửa / Xóa / Khóa / Import.'],
       [289, 290, 291, 292, 294, 295])
S8.add('Đổi thủ kho giữa thao tác', 'P0', [ACC_K, TEST_ENV], OPEN + ['Ở tab khác gỡ K khỏi Thủ kho kho PTT.', 'Bấm Tìm kiếm.'], '—',
       ['Bảng trống ngay (không chờ 60 giây).'], 298)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'SỐ LIỆU BÁO CÁO', S3),
    ('IV', 'XEM CHI TIẾT PHIẾU ĐỀ NGHỊ', S4),
    ('V', 'TÙY CHỈNH CỘT', S5),
    ('VI', 'XUẤT DANH SÁCH EXCEL', S6),
    ('VII', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S7),
    ('VIII', 'PHÂN QUYỀN', S8),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
_ids = ['TC_%02d.%s' % (s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
assert len(_ids) == len(set(_ids)), 'Trùng TC ID'

if __name__ == '__main__':
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='Hoạt động kho - Cập nhật ngày 10/11/2026',
                module_name='Hoạt động kho', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='bao_cao')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

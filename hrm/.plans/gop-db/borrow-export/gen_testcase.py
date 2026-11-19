# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu xuất hàng mượn" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Nhóm theo đúng tên + thứ tự chuẩn loại 'phieu' (check_tc.THU_TU), bỏ nhóm màn không có (Chỉnh sửa, Xóa, Khóa / Mở khóa, Gửi duyệt,
Không duyệt phiếu, Hủy phiếu, Import — kiểm code 05/11/2026: không có route / nút sửa, xóa, từ chối; phiếu sinh ra đã Đã duyệt):
I Hiển thị trang & truy cập · II Tìm kiếm & lọc danh sách (gồm Cài đặt bộ lọc) · III Thêm mới (Lập phiếu, popup chọn phiếu yêu cầu,
Lưu và tiếp tục, rời màn) · IV Duyệt phiếu (tác dụng của Lưu và duyệt lên phiếu yêu cầu / phiếu mượn, thông báo) · V Lịch sử thay đổi ·
VI Xem chi tiết · VII In phiếu (kèm In danh sách) · VIII Tùy chỉnh cột · IX Xuất danh sách Excel · X Ràng buộc với các chức năng khác ·
XI Phân quyền (cuối). Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../finance-bill-adjust-dept/gen_testcase.py (đã qua check_tc 0 lỗi 04/11).
Nguồn hành vi (đọc 05/11/2026, nhánh develop cả 2 repo): FE pages/finance/borrow-exports/**; BE Modules/Finance BorrowExport
(Entity / Service / Controller / StoreRequest / HistoryService), BorrowExportRequestNotifyService::onApproved.
Số liệu mẫu: dev-hrm 05/11/2026 (DNS Admin) 353 phiếu Đã duyệt, PXHM-00355; phiếu yêu cầu Chờ duyệt lấy từ dữ liệu thử local.
"""
import os
import re
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
from tc_phieu_bosung import ListScreen, open_menu_case, filter_memory_cases, combo_cases, check_no_dash_pre  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Tài chính > menu "Hàng hoá - Dịch vụ - Vận chuyển" > nhóm "Mượn hàng" > bấm "Phiếu xuất hàng mượn".'
YC_MENU = 'Vào phân hệ Tài chính > menu "Hàng hoá - Dịch vụ - Vận chuyển" > nhóm "Mượn hàng" > bấm "Yêu cầu xuất hàng mượn".'
TAO = [MENU, 'Bấm "Tạo mới".']
ADV = 'Bấm Tìm kiếm nâng cao.'

ACC_K = 'Tài khoản K: có quyền Kế toán kho, không có quyền Xem giá vốn hàng hoá.'
ACC_KG = 'Tài khoản KG: có quyền Kế toán kho và quyền Xem giá vốn hàng hoá.'
ACC_B = 'Tài khoản B: nhân viên, không có quyền Kế toán kho.'
PRE_LIST = 'Tài khoản DNS Admin (Super admin); hệ thống có 353 phiếu xuất hàng mượn, đều Đã duyệt.'
P355 = ('Phiếu PXHM-00355: Phiếu yêu cầu PYCXHM-00367, Người yêu cầu Võ Cát Hào, Người tạo "Cao Thị Thùy Linh - MT_KTHC", Ngày tạo '
        '21/10/2026 07:51; 1 dòng hàng "Ắc quy khô cho xe gắn máy PTZ7A" (Cái, Đơn giá bán 353,704, Số lượng 1) xuất trên phiếu mượn '
        'PYCXH-43208; Phiếu xuất mượn PYCXH-43967, PYCXH-43208.')
YC1 = ('Phiếu yêu cầu YC1 (PYCXHM-00337) Chờ duyệt do nhân viên M lập, gom phiếu mượn PYCXH-TEST-001; 2 dòng: "Máy mài săm lốp '
       '2500 rpm" (Cái, 1,700,000, đề nghị 2, Đang mượn 13) và "Keo vá lốp màu trắng 250ml" (Lọ, 140,000, đề nghị 2, Đang mượn 20).')
YC2 = 'Phiếu yêu cầu YC2 (PYCXHM-TEST-01) Chờ duyệt do M lập.'
PRE_FORM = ACC_K + '\n' + YC1
CHON = TAO + ['Bấm ô Phiếu yêu cầu xuất hàng mượn.', 'Bấm dòng PYCXHM-00337.']
FULL = ['Phiếu yêu cầu: PYCXHM-00337', 'Xuất Máy mài: 2', 'Xuất Keo vá lốp: 2', 'Ghi chú: Xuất hẳn cho khách']

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
        self.mark(ck)

    def raw(self, tcs, ck_list=None):
        for i, tc in enumerate(tcs):
            assert int(tc[0]) == len(self) + 1, 'Lệch số TC %s ở section %d' % (tc[0], self.idx)
            self.append(tc)
            if ck_list:
                self.mark(ck_list[i])

    def mark(self, ck):
        tid = 'TC_%02d.%s' % (self.idx, self[-1][0])
        for s in (ck if isinstance(ck, (list, tuple)) else [ck]):
            CK[s].append(tid)


DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn Phiếu xuất hàng mượn dùng để Kế toán kho DUYỆT một phiếu Yêu cầu xuất hàng mượn: tất toán phần hàng người mượn không trả '
     'lại mà xuất hẳn.\nMột lần bấm Lưu và duyệt: sinh phiếu PXHM-NNNNN Đã duyệt, ghi số Được duyệt + trạng thái Đã duyệt về phiếu '
     'yêu cầu, cộng số đã trả vào phiếu mượn gốc, ghi lịch sử, báo người lập phiếu yêu cầu.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Danh sách: mọi phiếu xuất hàng mượn (không giới hạn công ty / phòng ban), chỉ trạng thái Đã duyệt (nhãn xanh lá).\n'
     '- Popup chọn: chỉ phiếu yêu cầu xuất hàng mượn đang Chờ duyệt.\n'
     '- Bảng Chi tiết: dòng hàng có số đề nghị > 0 của phiếu yêu cầu, mỗi phiếu mượn 1 dòng con.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu yêu cầu Đã duyệt / Không duyệt: không có trong popup chọn.\n'
     '- Màn không có Lưu nháp, Sửa, Xóa, Không duyệt, Hủy, Khóa / Mở khóa, Import.\n'
     '- Đơn giá vốn ẩn với người không có quyền Xem giá vốn hàng hoá.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo ngày tạo phiếu xuất, lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Phiếu xuất > dòng hàng (hàng + đơn vị) > dòng chi tiết theo phiếu mượn (Phiếu mượn, Đang mượn, Xuất).\n'
     '- Phiếu xuất gắn đúng 1 phiếu yêu cầu; phiếu yêu cầu gom 1 hoặc nhiều phiếu mượn.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Số lượng dòng hàng = tổng ô Xuất; Tổng cộng = tổng Số lượng; Thành tiền = Số lượng × Đơn giá bán.\n'
     '- Đang mượn = đã xuất - đã trả - phần đang chờ ở phiếu khác (không tính chính phiếu yêu cầu đang duyệt), làm tròn xuống.\n'
     '- Một phiếu yêu cầu chỉ duyệt được 1 lần.'),
    ('7. Phân quyền cấp',
     '- Kế toán kho: mọi chức năng của màn (xem, lập, in, xuất, lịch sử); không có quyền xem theo cấp.\n'
     '- Xem giá vốn hàng hoá: hiện thêm cột Đơn giá vốn ở màn chi tiết và bản in phiếu.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là khoảng số thứ tự trang đang xem, N là tổng phiếu khớp bộ lọc.\n'
     '- Cột Số lượng ở form = tổng các ô Xuất của dòng; dòng Tổng cộng = tổng cột Số lượng.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: K (Kế toán kho), KG (Kế toán kho + Xem giá vốn hàng hoá), B (không quyền), M (người lập phiếu yêu '
     'cầu), DNS Admin (Super admin).\n'
     '- Số hiển thị dạng 1,234,567 (dấu phẩy ngăn nghìn).\n'
     '- Lưu ý: Lưu và duyệt GHI NGAY, không có hộp xác nhận và không hoàn tác — chạy trên phiếu yêu cầu thử.\n'
     '- Lưu ý: màn Lập / Chi tiết là TRANG riêng, không phải cửa sổ nổi.'),
]

SCREEN = ListScreen(menu=MENU, title='Phiếu xuất hàng mượn', total=353, quick_label='mã phiếu, mã phiếu yêu cầu',
                    quick_sample='PXHM-00355', quick_hit='phiếu PXHM-00355',
                    filters=[('Người tạo', 'Cao Thị Thùy Linh'), ('Người yêu cầu', 'Võ Cát Hào')])

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Cả 3 nơi đều là "Phiếu xuất hàng mượn".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', ACC_K, ['Đăng nhập K.', MENU, 'Quan sát khối bộ lọc và thanh công cụ.'], '—',
       ['Khối bộ lọc: ô tìm nhanh (gợi ý "Tìm theo mã phiếu, mã phiếu yêu cầu"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
        'Thanh công cụ: Tạo mới, In, Xuất Excel, nút biểu tượng cột.', 'Cột Hành động mỗi dòng chỉ có In và Lịch sử; không có Sửa, '
        'Xóa, Duyệt, Import, Khóa.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột từ trái sang phải.'],
       '—', ['Đúng 11 cột: STT, Mã phiếu, Phiếu yêu cầu, Người yêu cầu, Người tạo, Ngày tạo, Trạng thái, Ghi chú, Người cập nhật, Ngày '
             'cập nhật, Hành động.', 'STT và Mã phiếu ghim trái khi cuộn ngang.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 11/11 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp phiếu đã tạo', 'P0', [PRE_LIST, P355], [MENU, 'Tìm "PXHM-00355", đối chiếu dòng.'], '—',
       ['Phiếu yêu cầu "PYCXHM-00367" (liên kết); Người yêu cầu "Võ Cát Hào"; Người tạo "Cao Thị Thùy Linh - MT_KTHC"; Ngày tạo '
        '"21/10/2026 07:51".', 'Trạng thái nhãn xanh lá "Đã duyệt".'], 6)
S1.add('Ghi chú hiển thị đúng và tự xuống dòng', 'P2', [PRE_LIST, 'Phiếu PXHM-00352 có ghi chú "Xuất hàng gửi đi bảo hành BB076935".'],
       [MENU, 'Tìm "PXHM-00352".'], '—', ['Cột Ghi chú hiện đúng nguyên văn; chữ dài tự xuống dòng, không tràn ô.'], 6)
S1.add('Liên kết Phiếu yêu cầu mở ở tab mới', 'P1', [PRE_LIST, P355], [MENU, 'Ở dòng PXHM-00355 bấm "PYCXHM-00367".'], '—',
       ['Mở chi tiết phiếu yêu cầu PYCXHM-00367 ở TAB MỚI.', 'Tab danh sách giữ nguyên trang, bộ lọc.'], 6)
S1.add('Trạng thái bản ghi', 'P0', PRE_LIST, [MENU, ADV, 'Mở ô Trạng thái.'], '—',
       ['Ô chỉ có 1 lựa chọn "Đã duyệt".', 'Mọi dòng đều nhãn xanh lá "Đã duyệt" (phiếu lưu xong là Đã duyệt, không đổi về sau).'], 7)
S1.add('Danh sách chưa có dữ liệu phù hợp', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       ['Trong bảng hiện "Không có dữ liệu phù hợp.", dưới bảng "Không có phiếu nào.".', 'Không báo lỗi.'], [8, 9])
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 3.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 20 phiếu, tự về trang 1, "Hiển thị 1–20 / 353".', 'Ô có các lựa chọn 5, 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–20 / 353".', 'Bước 3: "Hiển thị 1–10 / 353".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—',
       ['Bước 2: trang 36, "Hiển thị 351–353 / 353".', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang cuối quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ, bấm không tác dụng.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2, rồi trang 3.'], '—', ['Trang 2: 11–20; trang 3: 21–30.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 4.', ADV, 'Chọn Trạng thái = Đã duyệt.'],
       'Trạng thái: Đã duyệt', ['Tự nạp lại ở trang 1; "Hiển thị 1–10 / 353".'], 17)
S1.add('Sắp xếp tăng dần theo Mã phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Mã phiếu.'], '—',
       ['Xếp từ mã nhỏ đến lớn (PXHM-00001… trên cùng), mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Mã phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Mã phiếu 2 lần.'], '—',
       ['Xếp từ mã lớn đến nhỏ, mũi tên xuống.'], 21)
S1.add('Sắp xếp theo Ngày tạo', 'P1', PRE_LIST, [MENU, 'Bấm tiêu đề Ngày tạo.', 'Bấm lần nữa.'], '—',
       ['Lần 1 cũ nhất trên, lần 2 mới nhất trên.', 'Mặc định khi mới vào: mới nhất trên.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Phiếu yêu cầu, Người yêu cầu, Người tạo, Trạng thái, Ghi chú, Người cập nhật, Ngày cập nhật.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Mã phiếu (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự tăng của trang 1.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 4.', 'Bấm tiêu đề Ngày tạo.'], '—', ['Về trang 1.'], 25)
S1.add('Mở màn Lập từ nút trên phiếu yêu cầu', 'P0', [ACC_K, YC1],
       ['Đăng nhập K.', YC_MENU, 'Bấm mã PYCXHM-00337 để mở chi tiết.', 'Bấm "Tạo phiếu xuất hàng mượn".'], '—',
       ['Mở màn "Lập phiếu xuất hàng mượn" với ô Phiếu yêu cầu = PYCXHM-00337, bảng Chi tiết điền sẵn 2 dòng.'], [1, 49])
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo mã phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "PXHM-00355", bấm Tìm kiếm.'], 'Ô tìm nhanh: PXHM-00355',
       ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần mã phiếu', 'P0', PRE_LIST, [MENU, 'Nhập "0035", bấm Tìm kiếm.'], 'Ô tìm nhanh: 0035',
       ['Còn các phiếu có mã hoặc mã phiếu yêu cầu chứa "0035" (có PXHM-00350 … PXHM-00355).'], 27)
S2.add('Ô tìm nhanh tìm theo mã phiếu yêu cầu', 'P0', PRE_LIST, [MENU, 'Nhập "PYCXHM-00367", bấm Tìm kiếm.'], '—',
       ['Ra phiếu PXHM-00355.'], 27)
S2.add('Ô tìm nhanh không tìm theo tên người', 'P1', PRE_LIST, [MENU, 'Nhập "Võ Cát Hào", bấm Tìm kiếm.'], '—',
       ['"Không có dữ liệu phù hợp." (tìm người dùng ô Người yêu cầu / Người tạo).'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "pxhm-00355", bấm Tìm kiếm.'], '—',
       ['Ra phiếu PXHM-00355 như khi gõ chữ hoa.'], 28)
S2.add('Có dấu / không dấu ở ô Hàng hóa', 'P2', PRE_LIST, [MENU, ADV, 'Nhập Hàng hóa "ac quy kho".'], '—',
       ['Ra các phiếu có hàng "Ắc quy khô…" nếu cơ sở dữ liệu so khớp không dấu.', 'Lưu ý: so khớp theo cách so sánh chữ của cơ sở dữ liệu.'],
       29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; ký tự % được hiểu là ký tự đại diện nên ra toàn bộ phiếu.'],
       31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  PXHM-00355  ", bấm Tìm kiếm.'], '—',
       ['Ra phiếu PXHM-00355 (bỏ khoảng trắng đầu / cuối).'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "PXHM-00355", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Sau bước 2 hiện lại đủ 353 phiếu.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST, [MENU, 'Nhập "PXHM-00355", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'],
       '—', ['Cả 2 cách đều ra phiếu PXHM-00355, về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['7 ô lọc (Mã phiếu, Mã phiếu yêu cầu, Người yêu cầu, Người tạo, Hàng hóa, Trạng thái, Ngày tạo) đều trống.',
        'Không có ô Công ty, Phòng ban.', 'Đủ 353 phiếu.'], 36)
S2.add('Lọc Mã phiếu', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "00355" vào ô Mã phiếu.'], '—',
       ['Lọc ngay khi gõ; còn PXHM-00355.'], 37)
S2.add('Lọc Mã phiếu yêu cầu', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "PYCXHM-00367" vào ô Mã phiếu yêu cầu.'], '—',
       ['Còn PXHM-00355.'], 37)
S2.add('Lọc Người yêu cầu', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người yêu cầu = Võ Cát Hào.'], '—',
       ['Chỉ phiếu có phiếu yêu cầu do Võ Cát Hào lập (có PXHM-00355, 00354, 00352).'], 37)
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = Trần Thị Dung.'], '—',
       ['Chỉ phiếu do Trần Thị Dung lập (có PXHM-00353, PXHM-00347).'], 37)
S2.add('Lọc Hàng hóa theo tên hoặc mã', 'P0', PRE_LIST, [MENU, ADV, 'Nhập Hàng hóa "PTZ7A".', 'Đổi thành "PINA-PTZ7A".'], '—',
       ['Cả 2 lần đều có PXHM-00355 (khớp tên hoặc mã hàng trên phiếu).'], 37)
S2.add('Lọc Trạng thái', 'P1', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đã duyệt.'], '—', ['Lọc ngay; vẫn 353 phiếu.'], 37)
S2.add('Lọc Ngày tạo lấy trọn ngày biên', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày tạo 21/10/2026 – 21/10/2026.'], '—',
       ['Ra phiếu PXHM-00355 (tạo 07:51 ngày 21/10/2026).', 'Bỏ trống ngày cuối vẫn lọc được từ ngày đầu.'], 37)
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người yêu cầu = Võ Cát Hào.', 'Nhập Hàng hóa "PTZ7A".'],
       '—', ['Chỉ phiếu thỏa cả 2 điều kiện (có PXHM-00355).'], 38)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST, [MENU, 'Nhập "PXHM-00355", bấm Tìm kiếm.', ADV, 'Chọn Người tạo = Trần Thị Dung.'],
       '—', ['"Không có dữ liệu phù hợp." vì PXHM-00355 do người khác tạo.'], [39, 40])
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = Cao Thị Thùy Linh.', 'Bấm trang cuối.'],
       '—', ['Dòng "Hiển thị" ghi đúng tổng phiếu của người đó.', 'Trang cuối hiện phần còn lại, STT liên tục.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Người tạo = Cao Thị Thùy Linh.', ['Bấm tiêu đề Mã phiếu.'], '—',
       ['Chỉ phiếu đang lọc được sắp; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "PXHM", lọc Người tạo, Hàng hóa, sắp Mã phiếu, ở trang 2.',
       ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống, bỏ sắp xếp, nạp lại trang 1, đủ 353 phiếu.'], 44)
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Người tạo = Cao Thị Thùy Linh, chưa mở màn con.'],
       ['Nhấn F5.'], '—', ['Bộ lọc trở về trống, đủ 353 phiếu (bộ lọc chỉ nhớ khi đi vào màn chi tiết / lập phiếu của màn).'], 46)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Hàng hóa, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô Hàng hóa.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Người tạo = Cao Thị Thùy Linh.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Người tạo, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị bỏ, nạp lại đủ phiếu.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Hàng hóa.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Hàng hóa vẫn ẩn.', 'Bước 2: tích đủ 7 ô, Hàng hóa hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Ngày tạo lên đầu, bấm Lưu.'], '—',
       ['Ô Ngày tạo đứng đầu khối Tìm kiếm nâng cao; cấu hình giữ sau khi đăng nhập lại.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Lập', 'P0', PRE_FORM, TAO, '—', ['Mở TRANG "Lập phiếu xuất hàng mượn", tab cùng tiêu đề.'], 49)
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải "<tên K> - <ngày giờ hiện tại>".', 'Không có ô Mã phiếu (mã tự sinh khi lưu).'], 50)
S3.add('Các trường, khối và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Phiếu yêu cầu xuất hàng mượn * (gợi ý "Nhấn vào đây để chọn phiếu yêu cầu xuất hàng mượn"), Phiếu xuất mượn '
        '("Chưa chọn phiếu xuất mượn"), Ghi chú.', 'Khối Chi tiết: "Chưa chọn phiếu yêu cầu.".',
        'Chân màn: Lưu và duyệt, Lưu và tiếp tục, Quay lại.'], [51, 54])
S3.add('Trường bắt buộc / không bắt buộc', 'P0', PRE_FORM, TAO + ['Quan sát dấu *.'], '—',
       ['Chỉ Phiếu yêu cầu xuất hàng mượn có dấu *; ô Xuất bắt buộc > 0 khi đã chọn phiếu; Ghi chú không bắt buộc.'], 52)
S3.add('Giá trị mặc định sau khi chọn phiếu', 'P0', PRE_FORM, CHON, '—',
       ['Hiện Người lập phiếu yêu cầu = M, Phòng ban người lập phiếu yêu cầu, chip PYCXH-TEST-001.',
        'Bảng 2 dòng: Máy mài (Cái, Đơn giá 1,700,000, Đang mượn 13, Xuất điền sẵn 2), Keo vá lốp (Lọ, 140,000, Đang mượn 20, Xuất 2).',
        'Số lượng mỗi dòng 2, Tổng cộng 4.'], 53)
S3.add('Lưu và duyệt với dữ liệu hợp lệ đầy đủ', 'P0', PRE_FORM, CHON + ['Nhập Ghi chú.', 'Bấm Lưu và duyệt.'], FULL,
       ['Báo "Thao tác thành công.", về danh sách.', 'Dòng mới trên cùng, mã PXHM-NNNNN kế tiếp, Phiếu yêu cầu PYCXHM-00337, nhãn '
        '"Đã duyệt", Ghi chú đúng.', 'Không có hộp xác nhận trước khi lưu.'], [55, 86, 92])
S3.add('Lưu chỉ với trường bắt buộc', 'P0', PRE_FORM, CHON + ['Không nhập Ghi chú.', 'Bấm Lưu và duyệt.'], FULL[:3],
       ['Lưu được; cột Ghi chú trống.'], [56, 57])
S3.add('Dữ liệu sau lưu', 'P0', PRE_FORM, CHON + ['Nhập Ghi chú.', 'Bấm Lưu và duyệt.', 'Bấm mã phiếu vừa tạo.'], FULL,
       ['Màn chi tiết: Phiếu yêu cầu PYCXHM-00337, Người lập phiếu yêu cầu M, Phiếu xuất mượn PYCXH-TEST-001, Ghi chú đúng.',
        'Bảng: Máy mài Số lượng 2, Thành tiền = 2 × 1,700,000; Keo vá lốp Số lượng 2, Thành tiền = 2 × 140,000; Tổng cộng Số lượng 4.'], 58)
S3.add('Trạng thái mặc định sau lưu', 'P0', PRE_FORM, CHON + ['Bấm Lưu và duyệt.'], FULL[:3],
       ['Phiếu ở trạng thái Đã duyệt (nhãn xanh lá) ngay khi lưu; không có trạng thái nháp.'], 59)
S3.add('Lịch sử tạo', 'P1', PRE_FORM, CHON + ['Bấm Lưu và duyệt.', 'Ở dòng phiếu mới bấm Lịch sử.'], FULL[:3],
       ['Có 1 mốc "Tạo mới", người thực hiện K, thời gian lúc lưu, kèm Phiếu yêu cầu và bảng hàng.'], [60, 176])
S3.add('Chưa chọn phiếu yêu cầu thì bị chặn', 'P0', PRE_FORM, TAO + ['Bấm Lưu và duyệt ngay.'], '—',
       ['Viền đỏ, "Bắt buộc phải chọn" dưới ô Phiếu yêu cầu.', 'Thông báo "Bạn chưa nhập đầy đủ thông tin.", không lưu.'],
       [61, 70, 87])
S3.add('Ô Xuất bằng 0 thì bị chặn', 'P0', PRE_FORM, CHON + ['Xóa ô Xuất của Máy mài (về 0).', 'Bấm Lưu và duyệt.'], 'Xuất Máy mài: 0',
       ['Dưới ô hiện "Phải lớn hơn 0", viền đỏ.', 'Thông báo "Vui lòng kiểm tra lại thông tin đã nhập", tự cuộn tới ô lỗi; không lưu.'],
       [61, 70])
S3.add('Ô Xuất vượt Đang mượn', 'P0', PRE_FORM, CHON + ['Nhập Xuất Máy mài 14.'], 'Xuất Máy mài: 14 (Đang mượn 13)',
       ['Ngay khi gõ hiện "Không được vượt quá 13" dưới ô.', 'Bấm Lưu và duyệt: thông báo "Vui lòng kiểm tra lại thông tin đã nhập", '
        'không lưu.'], [62, 88])
S3.add('Ô Xuất không nhận chữ và dấu', 'P1', PRE_FORM, CHON + ['Gõ "abc", "-5", "1.5" vào ô Xuất Máy mài.'], '—',
       ['Ô bỏ chữ cái, dấu trừ, dấu thập phân; chỉ giữ chữ số.'], [62, 63])
S3.add('Ô Xuất đúng bằng Đang mượn', 'P1', PRE_FORM, CHON + ['Nhập Xuất Máy mài 13.', 'Bấm Lưu và duyệt.'], 'Xuất Máy mài: 13',
       ['Lưu được (cho phép bằng Đang mượn).'], 65)
S3.add('Ô Xuất tối thiểu là 1', 'P2', PRE_FORM, CHON + ['Nhập Xuất Máy mài 1.', 'Bấm Lưu và duyệt.'], 'Xuất Máy mài: 1',
       ['Lưu được; không có ràng buộc độ dài tối thiểu khác.'], 64)
S3.add('Ghi chú tối đa 255 ký tự', 'P1', PRE_FORM, CHON + ['Dán chuỗi 300 ký tự vào Ghi chú.'], 'Chuỗi 300 ký tự',
       ['Ô chỉ nhận 255 ký tự đầu; lưu được 255 ký tự.'], [65, 66])
S3.add('Ký tự đặc biệt trong Ghi chú', 'P2', PRE_FORM, CHON + ['Nhập Ghi chú "<b>Test</b> & @#$%".', 'Bấm Lưu và duyệt.'], '—',
       ['Lưu được; danh sách và chi tiết hiện nguyên chuỗi, không in đậm.'], 63)
S3.add('Ghi chú chỉ có khoảng trắng', 'P2', PRE_FORM, CHON + ['Nhập Ghi chú "   ".', 'Bấm Lưu và duyệt.'], 'Ghi chú: 3 khoảng trắng',
       ['Lưu được (Ghi chú không bắt buộc); Ghi chú hiển thị trống.'], [68, 69])
S3.add('Không lập được 2 phiếu cho cùng phiếu yêu cầu', 'P0', [PRE_FORM, 'Đã lưu phiếu xuất cho PYCXHM-00337.'],
       TAO + ['Bấm ô Phiếu yêu cầu.'], '—',
       ['PYCXHM-00337 không còn trong cửa sổ chọn (đã Đã duyệt).', 'Phiếu không có trường nhập duy nhất: mã PXHM tự sinh, không trùng.'],
       [67, 75, 89])
S3.add('Lỗi biến mất sau khi sửa', 'P1', PRE_FORM, CHON + ['Nhập Xuất Máy mài 14 (báo lỗi).', 'Sửa lại 3.'], '—',
       ['Chữ đỏ dưới ô biến mất ngay khi sửa hợp lệ.'], 71)
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', [PRE_FORM, YC2], CHON + ['Bấm Lưu và tiếp tục.'], FULL[:3],
       ['Báo "Thao tác thành công."; vẫn ở màn Lập, form trắng (ô Phiếu yêu cầu trống, khối Chi tiết "Chưa chọn phiếu yêu cầu.").',
        'Danh sách có phiếu vừa lưu.'], [72, 76, 77, 90, 91])
S3.add('Lưu và tiếp tục khi chưa chọn phiếu', 'P1', PRE_FORM, TAO + ['Bấm Lưu và tiếp tục.'], '—',
       ['"Bắt buộc phải chọn" dưới ô; thông báo "Bạn chưa nhập đầy đủ thông tin.", không lưu.'], 73)
S3.add('Lưu và tiếp tục khi ô Xuất sai', 'P1', PRE_FORM, CHON + ['Nhập Xuất Máy mài 14.', 'Bấm Lưu và tiếp tục.'], '—',
       ['Báo lỗi như Lưu và duyệt; không lưu, giữ dữ liệu.'], 74)
S3.add('Lưu và tiếp tục khi vào từ phiếu yêu cầu', 'P1', [ACC_K, YC1],
       [YC_MENU, 'Mở chi tiết PYCXHM-00337, bấm Tạo phiếu xuất hàng mượn.', 'Bấm Lưu và tiếp tục.'], '—',
       ['Lưu thành công; form mới trắng, KHÔNG tự nạp lại PYCXHM-00337 đã duyệt.'], [72, 77])
S3.add('Rời màn sau Lưu và tiếp tục', 'P2', [PRE_FORM, YC2], CHON + ['Bấm Lưu và tiếp tục.', 'Bấm Quay lại.'], FULL[:3],
       ['Form vừa làm mới chưa đổi gì: về danh sách ngay, không hỏi.'], 78)
S3.add('Quay lại khi chưa nhập gì', 'P1', PRE_FORM, TAO + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 93)
S3.add('Quay lại khi đã chọn phiếu', 'P0', PRE_FORM, CHON + ['Bấm Quay lại.'], '—',
       ['Hiện hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" với 2 nút Thoát, Ở lại.'], [94, 95])
S3.add('Chọn Thoát', 'P0', PRE_FORM, CHON + ['Bấm Quay lại.', 'Bấm Thoát.'], '—',
       ['Về danh sách; không có phiếu mới; PYCXHM-00337 vẫn Chờ duyệt.'], 96)
S3.add('Chọn Ở lại', 'P1', PRE_FORM, CHON + ['Sửa Xuất Máy mài 3.', 'Bấm Quay lại.', 'Bấm Ở lại.'], '—',
       ['Hộp đóng, vẫn ở màn Lập, Xuất Máy mài vẫn 3.'], 97)
S3.add('Chuyển menu khác khi đã nhập', 'P1', PRE_FORM, CHON + ['Bấm một mục menu khác ở thanh bên.'], '—',
       ['Hiện hộp "Thông tin chưa lưu" như khi bấm Quay lại.', 'Màn là trang, không có nút X / click ra ngoài.'], 95)
S3.add('Bỏ phiếu đã chọn bằng dấu ×', 'P1', PRE_FORM, CHON + ['Bấm × trong ô Phiếu yêu cầu.', 'Bấm Quay lại.'], '—',
       ['Bước 4: ô trống, khối Chi tiết về "Chưa chọn phiếu yêu cầu.".', 'Bước 5: form đã thay đổi so với lúc mở nên vẫn hỏi '
        '"Thông tin chưa lưu" (ghi nhận nếu không hỏi).'], [98, 99])
S3.add('Đổi Xuất rồi trả về giá trị ban đầu', 'P2', [ACC_K, YC1],
       [YC_MENU, 'Mở chi tiết PYCXHM-00337, bấm Tạo phiếu xuất hàng mượn.', 'Đổi Xuất Máy mài 3 rồi sửa lại 2.', 'Bấm Quay lại.'], '—',
       ['Dữ liệu như lúc mở: về danh sách không hỏi.'], 99)
S3.add('Để màn Lập lâu không thao tác', 'P2', [PRE_FORM, 'Đã chọn phiếu, để nguyên 30 phút.'], ['Bấm Lưu và duyệt.'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên đăng nhập, về màn đăng nhập, không lưu.'], 100)
S3.add('Bấm Lưu và duyệt liên tục', 'P1', PRE_FORM, CHON + ['Bấm Lưu và duyệt 3 lần thật nhanh.'], '—',
       ['Nút khóa trong lúc lưu; chỉ tạo 1 phiếu.'], 101)
S3.add('Hai Kế toán kho cùng lập cho một phiếu yêu cầu', 'P1', [ACC_K, 'Tài khoản K2 cũng có quyền Kế toán kho.', YC1],
       ['K và K2 cùng mở màn Lập, chọn PYCXHM-00337.', 'K bấm Lưu và duyệt.', 'K2 bấm Lưu và duyệt.'], '—',
       ['K lưu được.', 'K2 nhận "Không thể duyệt yêu cầu này!", không tạo phiếu thứ 2.'], 102)
S3.add('Đang mượn bị phiếu khác trừ trước khi lưu', 'P1', [PRE_FORM, 'Trong lúc K mở form, phiếu khác đã duyệt làm Đang mượn của Máy '
       'mài còn 1.'], CHON + ['Giữ Xuất Máy mài 2.', 'Bấm Lưu và duyệt.'], '—',
       ['Hệ thống báo "Số lượng không hợp lệ", không lưu gì; phiếu yêu cầu vẫn Chờ duyệt.'], [102, 304])
S3.add('Popup chọn phiếu: giao diện', 'P0', [PRE_FORM, YC2], TAO + ['Bấm ô Phiếu yêu cầu.'], '—',
       ['Cửa sổ "Chọn phiếu yêu cầu xuất hàng mượn", dòng mô tả "Chỉ hiện phiếu đang ở trạng thái Chờ duyệt trong phạm vi Kế toán kho".',
        'Ô Mã phiếu, Người tạo, nút Tìm kiếm, Làm mới; bảng STT, Mã phiếu, Người tạo, Ngày tạo, "Bấm để chọn"; nút Đóng.',
        'Chỉ có phiếu Chờ duyệt (có PYCXHM-00337, PYCXHM-TEST-01).'], 51)
S3.add('Popup chọn phiếu: tìm theo mã phiếu', 'P0', [PRE_FORM, YC2], TAO + ['Bấm ô Phiếu yêu cầu.', 'Nhập "00337", bấm Tìm kiếm.'],
       '—', ['Còn 1 dòng PYCXHM-00337.'], 26)
S3.add('Popup chọn phiếu: lọc Người tạo và Làm mới', 'P1', [PRE_FORM, YC2],
       TAO + ['Bấm ô Phiếu yêu cầu.', 'Chọn Người tạo = M.', 'Bấm Làm mới.'], '—',
       ['Bước 4: lọc ngay, chỉ phiếu của M.', 'Bước 5: xóa 2 ô lọc, hiện lại đủ phiếu Chờ duyệt.'], 44)
S3.add('Popup chọn phiếu: không có phiếu Chờ duyệt', 'P1', [ACC_K, 'Không còn phiếu yêu cầu nào Chờ duyệt.'],
       TAO + ['Bấm ô Phiếu yêu cầu.'], '—', ['Bảng hiện "Không có phiếu yêu cầu nào đang chờ duyệt.".'], [8, 268])
S3.add('Popup chọn phiếu: chọn xong tự đóng', 'P0', PRE_FORM, CHON, '—',
       ['Cửa sổ tự đóng ngay khi bấm dòng; ô Phiếu yêu cầu = PYCXHM-00337; bảng Chi tiết nạp đúng 2 dòng.'], [76, 269])
S3.add('Popup chọn phiếu: Đóng không chọn', 'P1', PRE_FORM, TAO + ['Bấm ô Phiếu yêu cầu.', 'Bấm Đóng.'], '—',
       ['Cửa sổ đóng, ô Phiếu yêu cầu vẫn trống.'], 95)
S3.add('Chọn lại phiếu khác', 'P1', [PRE_FORM, YC2], CHON + ['Bấm ô Phiếu yêu cầu, chọn PYCXHM-TEST-01.'], '—',
       ['Thông tin chung và bảng Chi tiết thay bằng dữ liệu của PYCXHM-TEST-01.'], 283)
S3.add('Dòng hàng không có phiếu mượn', 'P2', [ACC_K, 'Phiếu yêu cầu YC3 Chờ duyệt có 1 dòng hàng không thuộc phiếu mượn nào.'],
       TAO + ['Chọn YC3.'], '—', ['Dòng đó tô mờ, 3 ô chi tiết gộp thành "Chưa có phiếu mượn", không nhập được.'], 283)
S3.add('Liên kết phiếu mượn mở ở tab mới', 'P2', PRE_FORM, CHON + ['Bấm chip PYCXH-TEST-001.', 'Bấm mã PYCXH-TEST-001 ở cột Phiếu mượn.'],
       '—', ['Cả 2 lần mở phiếu mượn ở tab mới; form đang nhập giữ nguyên.'], 51)

# ============================================================== IV. DUYỆT PHIẾU (Lưu và duyệt)
S4 = Sec(4)
S4.add('Điều kiện hiện nút Tạo phiếu xuất hàng mượn ở phiếu yêu cầu', 'P0', [ACC_K, YC1, 'PYCXHM-00367 Đã duyệt.'],
       ['Đăng nhập K.', YC_MENU, 'Mở chi tiết PYCXHM-00337.', 'Mở chi tiết PYCXHM-00367.'], '—',
       ['PYCXHM-00337: có nút "Tạo phiếu xuất hàng mượn".', 'PYCXHM-00367: không có nút.', 'Màn Phiếu xuất hàng mượn không có nút "Duyệt" '
        'riêng: Lưu và duyệt chính là duyệt.'], 300)
S4.add('Không có hộp xác nhận duyệt', 'P1', PRE_FORM, CHON + ['Bấm Lưu và duyệt.'], FULL[:3],
       ['Hệ thống lưu ngay, không hiện cửa sổ xác nhận.'], 301)
S4.add('Duyệt thành công chuyển phiếu yêu cầu sang Đã duyệt', 'P0', PRE_FORM, CHON + ['Bấm Lưu và duyệt.', YC_MENU,
       'Tìm PYCXHM-00337, mở chi tiết.'], FULL[:3],
       ['Phiếu yêu cầu nhãn "Đã duyệt"; Người duyệt = K, Ngày duyệt = thời điểm lưu.', 'Cột Được duyệt: Máy mài 2, Keo vá lốp 2.'],
       [302, 305, 306])
S4.add('Duyệt với số Xuất khác số đề nghị', 'P0', PRE_FORM, CHON + ['Sửa Xuất Máy mài 1.', 'Bấm Lưu và duyệt.', YC_MENU,
       'Mở chi tiết PYCXHM-00337.'], 'Xuất Máy mài: 1', ['Được duyệt Máy mài = 1, Keo vá lốp = 2 (theo số Kế toán kho nhập).'], 306)
S4.add('Kiểm tra dữ liệu bắt buộc trước khi duyệt', 'P0', PRE_FORM, TAO + ['Bấm Lưu và duyệt.'], '—',
       ['Chưa chọn phiếu đến "Bắt buộc phải chọn", không duyệt gì.'], 303)
S4.add('Kiểm tra điều kiện nghiệp vụ trước khi duyệt', 'P0', PRE_FORM, CHON + ['Nhập Xuất Keo vá lốp 21.', 'Bấm Lưu và duyệt.'],
       'Xuất Keo vá lốp: 21 (Đang mượn 20)', ['"Không được vượt quá 20"; không lưu; phiếu yêu cầu vẫn Chờ duyệt.'], 304)
S4.add('Số đã trả của phiếu mượn tăng sau duyệt', 'P0', [PRE_FORM, 'Phiếu mượn PYCXH-TEST-001: Máy mài còn mượn 13.'],
       CHON + ['Bấm Lưu và duyệt.', 'Lập lại form với phiếu yêu cầu khác có cùng phiếu mượn PYCXH-TEST-001.'], FULL[:3],
       ['Cột Đang mượn của Máy mài trên PYCXH-TEST-001 còn 11 (giảm đúng 2).'], [307, 281])
S4.add('Phiếu mượn trả hết chuyển Đã trả', 'P1', [ACC_K, 'Phiếu yêu cầu YC4 Chờ duyệt, phiếu mượn PM4 chỉ còn nợ 1 Cái, YC4 đề nghị 1.'],
       TAO + ['Chọn YC4, giữ Xuất 1.', 'Bấm Lưu và duyệt.', 'Mở chi tiết phiếu mượn PM4 ở màn Yêu cầu xuất hàng.'], '—',
       ['Phiếu mượn PM4 chuyển trạng thái mượn "Đã trả".', 'PM4 không còn trong Danh sách hàng mượn.'], [281, 307])
S4.add('Thông báo gửi người lập phiếu yêu cầu', 'P0', [PRE_FORM, 'M là người lập PYCXHM-00337.'], CHON + ['Bấm Lưu và duyệt.',
       'Đăng nhập M, mở chuông thông báo.'], FULL[:3],
       ['M nhận thông báo "[YCXHM] Đã duyệt: PYCXHM-00337", nội dung có "Người duyệt: <tên K>" và "Phiếu xuất: PXHM-…".',
        'K (người duyệt) không nhận thông báo này.'], 308)
S4.add('Bấm thông báo mở đúng phiếu', 'P1', 'M vừa nhận thông báo duyệt PYCXHM-00337.', ['M bấm vào thông báo.'], '—',
       ['Mở màn chi tiết phiếu yêu cầu PYCXHM-00337 (trạng thái Đã duyệt).'], 309)
S4.add('Thoát không lưu thì phiếu yêu cầu không đổi', 'P0', PRE_FORM, CHON + ['Bấm Quay lại, chọn Thoát.', YC_MENU,
       'Mở chi tiết PYCXHM-00337.'], '—', ['Phiếu yêu cầu vẫn Chờ duyệt, Được duyệt 0, không có thông báo, không có mốc lịch sử mới.'], 310)
S4.add('Không duyệt lại phiếu đã xử lý', 'P0', [ACC_K, 'PYCXHM-00337 vừa Đã duyệt; tab cũ vẫn mở màn Lập với phiếu này.'],
       ['Ở tab cũ bấm Lưu và duyệt.'], '—', ['Báo "Không thể duyệt yêu cầu này!"; không tạo phiếu.'], 311)
S4.add('Mở lại màn Lập từ phiếu đã duyệt', 'P1', [ACC_K, 'PYCXHM-00337 đã Đã duyệt.'],
       ['Mở lại đường dẫn màn Lập đã lưu trong lịch sử trình duyệt (kèm phiếu PYCXHM-00337).'], '—',
       ['Báo "Phiếu yêu cầu này không ở trạng thái chờ duyệt hoặc bạn không có quyền duyệt.", bảng Chi tiết không nạp.'], 311)
S4.add('Ghi nhận người duyệt và lịch sử duyệt', 'P0', PRE_FORM, CHON + ['Bấm Lưu và duyệt.', YC_MENU, 'Ở dòng PYCXHM-00337 bấm Lịch sử.'],
       FULL[:3], ['Có mốc "Duyệt": "Trạng thái: Chờ duyệt sang Đã duyệt", ghi chú "Phiếu xuất hàng mượn: PXHM-…", người thực hiện K.',
                  'Lịch sử của phiếu xuất chỉ có mốc "Tạo mới" (không ghi lặp mốc duyệt).'], [312, 183])

# ============================================================== V. LỊCH SỬ THAY ĐỔI
S5 = Sec(5)
P291 = 'Phiếu PXHM-00291 lập trên màn này, có 1 mốc lịch sử "Tạo mới" (05/10/2026 14:38, DNS Admin).'
S5.add('Mở cửa sổ lịch sử từ danh sách', 'P0', [PRE_LIST, P291], [MENU, 'Tìm PXHM-00291.', 'Bấm Lịch sử ở cột Hành động.'], '—',
       ['Mở cửa sổ "Lịch sử thay đổi: PXHM-00291", nút Bộ lọc, nút Đóng.'], 162)
S5.add('Thông tin mỗi mốc', 'P0', [PRE_LIST, P291], [MENU, 'Mở lịch sử PXHM-00291.'], '—',
       ['Mốc "Tạo mới", thời gian "05/10/2026 14:38", "Người thực hiện: DNS Admin — <phòng ban>".',
        'Nội dung tạo: Ghi chú, Phiếu yêu cầu, bảng hàng (Mã hàng hóa, Đơn vị tính, Đơn giá bán, số lượng), chi tiết theo phiếu mượn.',
        'Không có Đơn giá vốn trong lịch sử.'], [163, 165, 166, 167, 168])
S5.add('Mới nhất ở trên', 'P1', 'Phiếu yêu cầu PYCXHM-00337 vừa duyệt có 2 mốc (Tạo mới, Duyệt).', [YC_MENU, 'Mở lịch sử PYCXHM-00337.'],
       '—', ['Mốc Duyệt nằm trên mốc Tạo mới.'], 164)
S5.add('Phiếu chưa có lịch sử', 'P1', [PRE_LIST, P355, 'PXHM-00355 lập từ hệ thống cũ, chưa có mốc nào.'], [MENU, 'Mở lịch sử PXHM-00355.'],
       '—', ['Hiện "Chưa có lịch sử thao tác nào.".'], 173)
S5.add('Lọc theo loại hành động', 'P1', [PRE_LIST, P291], [MENU, 'Mở lịch sử PXHM-00291.', 'Bấm Bộ lọc, chọn Loại hành động = Tạo mới.',
       'Đổi thành Thay đổi trạng thái.'], '—', ['Bước 3: còn mốc Tạo mới.', 'Bước 4: "Không có lịch sử phù hợp bộ lọc.".'], [169, 173, 175])
S5.add('Lọc theo người thực hiện', 'P2', [PRE_LIST, P291], [MENU, 'Mở lịch sử, bấm Bộ lọc, chọn Người thực hiện = DNS Admin.'], '—',
       ['Còn mốc của DNS Admin.'], 170)
S5.add('Lọc theo thời gian và kết hợp', 'P2', [PRE_LIST, P291], [MENU, 'Mở lịch sử, bấm Bộ lọc.', 'Chọn Từ ngày 05/10/2026, Đến ngày '
       '05/10/2026, Loại hành động Tạo mới.'], '—', ['Còn mốc Tạo mới; đổi Từ ngày 06/10/2026 thì không còn mốc nào.'], [171, 172])
S5.add('Làm mới bộ lọc lịch sử', 'P2', 'Đang lọc lịch sử theo Loại hành động.', ['Bấm Làm mới trong khối lọc.'], '—',
       ['Xóa điều kiện, hiện lại đủ mốc.'], 174)
S5.add('Xem, in, xuất không ghi lịch sử', 'P1', [PRE_LIST, P291], [MENU, 'Mở chi tiết PXHM-00291, bấm In, đóng.', 'Xuất Excel danh sách.',
       'Mở lịch sử PXHM-00291.'], '—', ['Vẫn chỉ có 1 mốc Tạo mới.'], 182)
S5.add('Đóng cửa sổ lịch sử', 'P1', [PRE_LIST, 'Đang ở trang 3, lọc Người tạo.'], ['Mở lịch sử 1 phiếu.', 'Bấm Đóng.', 'Mở lại, bấm (x).'],
       '—', ['Cửa sổ đóng; danh sách giữ trang 3, bộ lọc, sắp xếp, không nạp lại.'], [184, 185])
S5.add('Khối Lịch sử ở màn chi tiết', 'P1', [PRE_LIST, P291], [MENU, 'Mở chi tiết PXHM-00291.', 'Bấm Xem lịch sử ở khối Lịch sử.'], '—',
       ['Khối mở rộng, cùng nội dung với cửa sổ ở danh sách; có nút Làm mới, Thu gọn, Bộ lọc.'], [162, 195])

# ============================================================== VI. XEM CHI TIẾT
S6 = Sec(6)
S6.add('Mở màn chi tiết', 'P0', [ACC_KG, P355], [MENU, 'Bấm mã PXHM-00355.'], '—',
       ['Mở TRANG "Chi tiết phiếu xuất hàng mượn: PXHM-00355".'], [186, 187])
S6.add('Đầy đủ trường thông tin', 'P0', [ACC_KG, P355], [MENU, 'Mở chi tiết PXHM-00355.'], '—',
       ['Khối Thông tin chung: Phiếu yêu cầu xuất hàng mượn (PYCXHM-00367), Trạng thái "Đã duyệt", Người lập phiếu yêu cầu (Võ Cát Hào), '
        'Phòng ban người lập phiếu yêu cầu (Kinh doanh CN Vinh), Phiếu xuất mượn (PYCXH-43967, PYCXH-43208), Ghi chú.',
        'Góc phải "Cao Thị Thùy Linh - 21/10/2026 07:51".'], [188, 189])
S6.add('Bảng chi tiết khớp dữ liệu', 'P0', [ACC_KG, P355], [MENU, 'Mở chi tiết PXHM-00355.'], '—',
       ['Dòng Ắc quy PTZ7A: Model PTZ7A, Mã PINA-PTZ7A, Thương hiệu PINACO, Cái, Đơn giá bán 353,704, Đơn giá vốn 353,327, Số lượng 1.',
        'Chi tiết: PYCXH-43208 Xuất 1; Thành tiền 353,704; Tổng cộng 1 / 353,704.'], [189, 190])
S6.add('Ẩn Đơn giá vốn khi thiếu quyền', 'P0', [ACC_K, P355], ['Đăng nhập K.', MENU, 'Mở chi tiết PXHM-00355.'], '—',
       ['Không có cột Đơn giá vốn; các cột khác giữ nguyên.'], [188, 299])
S6.add('Mọi trường chỉ đọc, không có nút Lưu', 'P0', [ACC_K, P355], [MENU, 'Mở chi tiết PXHM-00355.', 'Thử gõ vào các ô.'], '—',
       ['Các ô khóa, không sửa được.', 'Chân màn chỉ có In, Quay lại; không có Sửa, Xóa, Lưu.'], [191, 192, 193])
S6.add('Liên kết phiếu yêu cầu và phiếu mượn', 'P1', [ACC_K, P355], [MENU, 'Mở chi tiết PXHM-00355.', 'Bấm chip PYCXHM-00367.',
       'Quay lại, bấm chip PYCXH-43208.'], '—', ['Bước 3: mở chi tiết phiếu yêu cầu.', 'Bước 4: mở phiếu mượn ở tab mới.'], 190)
S6.add('Phiếu không ở trạng thái khóa', 'P2', [ACC_K, P355], [MENU, 'Mở chi tiết PXHM-00355.'], '—',
       ['Màn không có trạng thái Khóa; phiếu luôn Đã duyệt, chỉ xem.'], 194)
S6.add('Quay lại giữ trang và bộ lọc', 'P0', [ACC_K, 'Đang ở trang 2, lọc Người tạo = Cao Thị Thùy Linh.'],
       ['Bấm mã một phiếu.', 'Bấm Quay lại.'], '—', ['Về danh sách, còn bộ lọc Người tạo (trong 10 phút).'], [196, 197])
S6.add('Mở chi tiết phiếu không tồn tại', 'P2', ACC_K, ['Mở đường dẫn chi tiết với số phiếu 999999 (sửa tay trên thanh địa chỉ).'], '—',
       ['Báo lỗi không tìm thấy, quay về danh sách; không treo trang.'], 186)

# ============================================================== VII. IN PHIẾU
S7 = Sec(7)
S7.add('In phiếu từ danh sách', 'P0', [ACC_KG, P355], [MENU, 'Ở dòng PXHM-00355 bấm In.'], '—',
       ['Mở cửa sổ "Xem trước phiếu PXHM-00355" ngay trên danh sách.', 'Bản in: logo + tên công ty của phiếu yêu cầu, "PHIẾU XUẤT HÀNG '
        'MƯỢN", Số phiếu, Ngày tạo; bảng thông tin Người lập, Phiếu yêu cầu, Người yêu cầu, Phòng ban yêu cầu, Phiếu xuất mượn, Trạng thái.',
        'Bảng hàng có Đơn giá vốn; chỗ ký Người lập, Kế toán kho, Thủ kho.'], 188)
S7.add('In phiếu không có Đơn giá vốn khi thiếu quyền', 'P0', [ACC_K, P355], ['Đăng nhập K.', MENU, 'Ở dòng PXHM-00355 bấm In.'], '—',
       ['Bản in không có cột Đơn giá vốn.'], 299)
S7.add('In phiếu từ màn chi tiết', 'P1', [ACC_K, P355], [MENU, 'Mở chi tiết PXHM-00355.', 'Bấm In ở chân màn.'], '—',
       ['Mở cùng cửa sổ xem trước; bấm In trong cửa sổ mở hộp thoại in của trình duyệt.'], 188)
S7.add('Letterhead theo công ty của phiếu yêu cầu', 'P1', [ACC_K, 'Phiếu PXHM-00355 có phiếu yêu cầu thuộc Chi nhánh Vinh; K thuộc công ty '
       'khác.'], [MENU, 'In phiếu PXHM-00355.'], '—', ['Đầu bản in là "CHI NHÁNH VINH", không theo công ty của K.'], 188)
S7.add('In danh sách theo bộ lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày tạo 01/10/2026 – 21/10/2026.', 'Bấm In trên thanh công cụ.'], '—',
       ['Cửa sổ "Xem trước danh sách phiếu xuất hàng mượn": tiêu đề "DANH SÁCH PHIẾU XUẤT HÀNG MƯỢN", Khoảng thời gian "Từ ngày '
        '01/10/2026 đến ngày 21/10/2026", Tổng số phiếu đúng.', 'Cột: STT, Mã phiếu, Phiếu yêu cầu, Người yêu cầu, Người lập, Ngày lập, '
        'Trạng thái.'], 219)
S7.add('In danh sách vượt 2.000 dòng', 'P2', 'Bộ lọc khớp hơn 2.000 phiếu (dữ liệu thử).', ['Bấm In trên thanh công cụ.'], '—',
       ['Không dựng bản in, ẩn nút In, hiện dòng nhắc thu hẹp bộ lọc hoặc dùng Xuất Excel.'], 221)
S7.add('Đóng cửa sổ xem trước', 'P2', PRE_LIST, [MENU, 'In 1 phiếu.', 'Bấm (x).'], '—', ['Cửa sổ đóng, danh sách giữ nguyên.'], 184)

# ============================================================== VIII. TÙY CHỈNH CỘT
S8 = Sec(8)
S8.add('Mở cửa sổ Tùy chỉnh cột', 'P0', PRE_LIST, [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột", dòng hướng dẫn, Chọn tất cả, Bỏ chọn hết, danh sách 11 cột, "Đang chọn 11/11 cột", Lưu, Đóng.'],
       [198, 199, 200])
S8.add('Ẩn một cột', 'P0', PRE_LIST, [MENU, 'Mở Tùy chỉnh cột, bỏ tích Ghi chú, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công"; bảng không còn cột Ghi chú; "Đang chọn 10/11 cột" khi mở lại.'], [202, 206])
S8.add('Hiện lại cột đã ẩn', 'P0', 'Đã ẩn cột Ghi chú.', ['Mở Tùy chỉnh cột, tích Ghi chú, bấm Lưu.'], '—', ['Cột Ghi chú hiện lại.'], 201)
S8.add('Cột bắt buộc không ẩn được', 'P0', PRE_LIST, [MENU, 'Mở Tùy chỉnh cột, bấm Bỏ chọn hết.'], '—',
       ['STT, Mã phiếu, Hành động vẫn tích (biểu tượng ổ khóa); các cột khác bỏ tích.'], [203, 205])
S8.add('Kéo đổi thứ tự cột', 'P1', PRE_LIST, ['Mở Tùy chỉnh cột, kéo Ngày tạo lên trên Phiếu yêu cầu, bấm Lưu.'], '—',
       ['Bảng hiện Ngày tạo trước Phiếu yêu cầu; cột khóa không kéo được.'], 204)
S8.add('Đóng không lưu', 'P1', PRE_LIST, ['Mở Tùy chỉnh cột, bỏ tích Người cập nhật.', 'Bấm Đóng.'], '—',
       ['Bảng vẫn còn cột Người cập nhật.'], 207)
S8.add('Ghi nhớ sau F5 và theo tài khoản', 'P1', 'K đã ẩn cột Ghi chú.', ['Nhấn F5.', 'Đăng nhập K trên trình duyệt khác.',
       'Đăng nhập DNS Admin.'], '—', ['Bước 1, 2: cột Ghi chú vẫn ẩn.', 'Bước 3: DNS Admin vẫn thấy đủ 11 cột.'], [208, 209])
S8.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', 'Đang lọc Người tạo, tổng 120 phiếu.', ['Ẩn cột Người tạo, Lưu.'], '—',
       ['Bộ lọc giữ nguyên, tổng vẫn 120.'], [210, 211])

# ============================================================== IX. XUẤT DANH SÁCH EXCEL
S9 = Sec(9)
S9.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất Excel", 9 trường tích sẵn: Mã phiếu, Phiếu yêu cầu, Người yêu cầu, Người tạo, Ngày tạo, Trạng thái, '
        'Ghi chú, Người cập nhật, Ngày cập nhật; "Đang chọn 9/9 trường"; nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng.'],
       [212, 213, 214])
S9.add('Xuất với trường mặc định', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel, bấm Xuất file.'], '—',
       ['Tải file "danh_sach_phieu_xuat_hang_muon.xlsx", báo "Xuất Excel thành công".', 'File: tiêu đề "DANH SÁCH PHIẾU XUẤT HÀNG MƯỢN", '
        'dòng tên cột STT + 9 cột, 353 dòng dữ liệu (không phân trang), khối ký "Người lập" cuối file.'],
       [215, 216, 221, 223, 224, 225, 227])
S9.add('Xuất một số trường theo thứ tự chọn', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel, Bỏ chọn hết.', 'Tích Ngày tạo, rồi Mã phiếu.',
       'Kéo Mã phiếu lên trên, bấm Xuất file.'], '—', ['File chỉ có STT, Mã phiếu, Ngày tạo đúng thứ tự trong cửa sổ.'], [217, 226])
S9.add('Không chọn trường nào', 'P1', PRE_LIST, [MENU, 'Bấm Xuất Excel, Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S9.add('Xuất theo từ khóa và bộ lọc', 'P0', PRE_LIST, [MENU, 'Nhập "PXHM-0035", Tìm kiếm.', ADV, 'Chọn Ngày tạo 01/10/2026 – 21/10/2026.',
       'Xuất Excel, Xuất file.'], '—', ['File chỉ có các phiếu đang hiện trên màn; dòng thứ 2 "Từ ngày 01/10/2026 đến ngày 21/10/2026".'],
       [219, 220])
S9.add('Xuất danh sách rỗng', 'P1', PRE_LIST, [MENU, 'Tìm "ZZZ999".', 'Xuất Excel, Xuất file.'], '—',
       ['Vẫn tải file: tiêu đề, dòng tên cột, khối ký; không có dòng dữ liệu.'], 222)
S9.add('Dữ liệu và định dạng trong file khớp màn', 'P0', [PRE_LIST, P355], [MENU, 'Xuất toàn bộ trường.', 'Mở file, tìm PXHM-00355.'],
       '—', ['Phiếu yêu cầu PYCXHM-00367, Người yêu cầu Võ Cát Hào, Người tạo Cao Thị Thùy Linh, Ngày tạo "21/10/2026 07:51" dạng chữ, '
             'Trạng thái Đã duyệt.', 'Mã phiếu không bị Excel cảnh báo số dạng chữ.'], [228, 229])
S9.add('Tiếng Việt và ký tự đặc biệt trong file', 'P2', 'Có phiếu Ghi chú "<b>Test</b> & @#$% – Đã xuất".', ['Xuất file, mở cột Ghi chú.'],
       '—', ['Hiện đúng nguyên văn có dấu, không lỗi phông.'], 230)
S9.add('Đóng không xuất', 'P2', PRE_LIST, [MENU, 'Bấm Xuất Excel, bấm Đóng.'], '—', ['Không tải file.'], 214)

# ============================================================== X. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S10 = Sec(10)
S10.add('Phiếu yêu cầu mới gửi xuất hiện trong popup chọn', 'P0', [ACC_K, 'M vừa gửi phiếu yêu cầu mới YC5 ở màn Yêu cầu xuất hàng mượn.'],
        TAO + ['Bấm ô Phiếu yêu cầu.'], '—', ['YC5 có trong danh sách chọn (Chờ duyệt).'], [274, 269])
S10.add('Phiếu yêu cầu bị từ chối không còn trong popup', 'P0', [ACC_K, 'YC5 vừa bị Kế toán kho khác từ chối ở màn Yêu cầu xuất hàng mượn.'],
        TAO + ['Bấm ô Phiếu yêu cầu.'], '—', ['YC5 không có trong danh sách chọn.'], [268, 281])
S10.add('Bộ lọc màn Yêu cầu xuất hàng mượn cập nhật sau duyệt', 'P1', [ACC_K, 'Vừa lưu phiếu xuất cho PYCXHM-00337.'],
        [YC_MENU, 'Lọc Trạng thái = Chờ duyệt.', 'Lọc Trạng thái = Đã duyệt.'], '—',
        ['Bước 2: không còn PYCXHM-00337.', 'Bước 3: có PYCXHM-00337.'], 282)
S10.add('Số còn mượn ở Danh sách hàng mượn giảm', 'P0', [PRE_FORM, 'Danh sách hàng mượn: Máy mài trên PYCXH-TEST-001 còn mượn 13.'],
        CHON + ['Bấm Lưu và duyệt.', 'Vào nhóm Mượn hàng > Danh sách hàng mượn, tìm PYCXH-TEST-001.'], FULL[:3],
        ['Máy mài còn mượn 11.'], [274, 281])
S10.add('Phần đã xuất hẳn không còn cho Yêu cầu xuất bán hàng mượn', 'P1', [PRE_FORM, 'Vừa duyệt Xuất Máy mài 2.'],
        ['Vào nhóm Mượn hàng > Yêu cầu xuất bán hàng mượn, lập phiếu chọn PYCXH-TEST-001.'], '—',
        ['Số còn mượn của Máy mài là 11, không cho nhập quá 11.'], 274)
S10.add('Đổi tên hàng ở danh mục không làm đổi phiếu đã lập', 'P1', [ACC_K, 'Phiếu PXHM-NNNNN đã lập có hàng "Keo vá lốp màu trắng 250ml".'],
        ['Đổi tên hàng hóa đó ở danh mục hàng hóa.', 'Mở chi tiết phiếu xuất.'], '—',
        ['Phiếu vẫn hiện tên cũ (tên lưu cố định lúc lập).'], [278, 272])
S10.add('Liên kết phiếu yêu cầu không mất', 'P1', [ACC_K, P355], [MENU, 'Mở chi tiết PXHM-00355, bấm chip PYCXHM-00367.'], '—',
        ['Mở đúng phiếu yêu cầu đã duyệt; phiếu yêu cầu hiện Được duyệt khớp số Xuất.'], [279, 284])
S10.add('Dòng chi tiết đúng phiếu mượn của phiếu yêu cầu', 'P0', [ACC_K, P355], [MENU, 'Mở chi tiết PXHM-00355.'], '—',
        ['Mỗi dòng con thuộc đúng một phiếu mượn có trong khối Phiếu xuất mượn (PYCXH-43208 thuộc danh sách chip).'], 283)
S10.add('Lưu lỗi giữa chừng không sinh phiếu dở dang', 'P1', [PRE_FORM, 'Đang mượn bị trừ trước khi lưu (như TC_03.037).'],
        CHON + ['Bấm Lưu và duyệt (bị báo "Số lượng không hợp lệ").', 'Xem danh sách và phiếu yêu cầu.'], '—',
        ['Không có phiếu xuất mới; phiếu yêu cầu vẫn Chờ duyệt, Được duyệt 0; số đã trả phiếu mượn không đổi.'], [285, 286])

# ============================================================== XI. PHÂN QUYỀN (cuối)
S11 = Sec(11)
S11.add('Quyền Kế toán kho: xem danh sách', 'P0', ACC_K, ['Đăng nhập K.', MENU], '—', ['Thấy đủ 353 phiếu của mọi công ty.'], [287, 299])
S11.add('Không có quyền Kế toán kho: không xem được danh sách', 'P0', ACC_B, ['Đăng nhập B.', MENU], '—',
        ['Menu vẫn hiện; mở màn báo "Bạn không có quyền thực hiện chức năng này", bảng "Không có dữ liệu phù hợp.".'], [287, 295])
S11.add('Không có quyền: mở chi tiết bằng đường link', 'P0', [ACC_B, 'B có đường link chi tiết PXHM-00355 do người khác gửi.'],
        ['Đăng nhập B, mở đường link.'], '—', ['Báo "Bạn không có quyền thực hiện chức năng này", quay về danh sách.'], [288, 296])
S11.add('Quyền Kế toán kho: xem chi tiết', 'P0', [ACC_K, P355], ['Đăng nhập K.', MENU, 'Mở chi tiết PXHM-00355.'], '—',
        ['Xem được đầy đủ, ẩn cột Đơn giá vốn.'], 288)
S11.add('Quyền Xem giá vốn hàng hoá: hiện Đơn giá vốn', 'P0', [ACC_KG, P355], ['Đăng nhập KG.', MENU, 'Mở chi tiết PXHM-00355.'], '—',
        ['Có cột Đơn giá vốn 353,327.'], [288, 299])
S11.add('Quyền Kế toán kho: lập phiếu', 'P0', PRE_FORM, CHON + ['Bấm Lưu và duyệt.'], FULL[:3], ['Lưu thành công.'], 289)
S11.add('Không có quyền: không lập được phiếu', 'P0', [ACC_B, YC1], ['Đăng nhập B.', MENU, 'Bấm Tạo mới.', 'Bấm ô Phiếu yêu cầu.'], '—',
        ['Cửa sổ chọn không có phiếu nào, báo không có quyền; không lập được phiếu.'], [289, 296])
S11.add('Không có quyền: không thấy nút Tạo phiếu xuất hàng mượn', 'P0', [ACC_B, 'B mở được chi tiết PYCXHM-00337 (phiếu của B).'],
        ['Đăng nhập B.', YC_MENU, 'Mở chi tiết PYCXHM-00337.'], '—', ['Không có nút "Tạo phiếu xuất hàng mượn".'], 295)
S11.add('Quyền Kế toán kho: xuất Excel', 'P1', ACC_K, ['Đăng nhập K.', MENU, 'Xuất Excel, Xuất file.'], '—', ['Tải file thành công.'], 293)
S11.add('Quyền Kế toán kho: xem lịch sử', 'P1', [ACC_K, P291], ['Đăng nhập K.', MENU, 'Mở lịch sử PXHM-00291.'], '—',
        ['Xem được mốc Tạo mới.'], 294)
S11.add('Bị gỡ quyền giữa lúc thao tác', 'P1', [PRE_FORM, 'Quản trị gỡ quyền Kế toán kho của K khi K đang ở màn Lập.'],
        CHON + ['Bấm Lưu và duyệt.'], FULL[:3], ['Báo "Bạn không có quyền thực hiện chức năng này"; không lưu.'], [297, 298])
S11.add('Super admin có đủ quyền', 'P2', 'Tài khoản DNS Admin (Super admin), không gán quyền Kế toán kho riêng.',
        ['Đăng nhập DNS Admin.', MENU, 'Mở chi tiết PXHM-00355.'], '—', ['Xem được danh sách, chi tiết có Đơn giá vốn.'], 287)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'DUYỆT PHIẾU', S4),
    ('V', 'LỊCH SỬ THAY ĐỔI', S5),
    ('VI', 'XEM CHI TIẾT PHIẾU XUẤT HÀNG MƯỢN', S6),
    ('VII', 'IN PHIẾU', S7),
    ('VIII', 'TÙY CHỈNH CỘT', S8),
    ('IX', 'XUẤT DANH SÁCH EXCEL', S9),
    ('X', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S10),
    ('XI', 'PHÂN QUYỀN', S11),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
check_no_dash_pre(SECTIONS, [])
_ids = ['TC_%02d.%s' % (s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
assert len(_ids) == len(set(_ids)), 'Trùng TC ID'
_txt = ' | '.join(str(x) for _, _, s in SECTIONS for tc in s for x in tc[1:])
_bad = sorted(set(re.findall(r'TC_\d{2}\.\d{3}', _txt)) - set(_ids))
assert not _bad, 'Nhắc mã TC không tồn tại: %s' % _bad

if __name__ == '__main__':
    build_chuan(output_file=OUT, sheet_name='Trang tính1', feature_name='Phiếu xuất hàng mượn - Cập nhật ngày 05/11/2026',
                module_name='Phiếu xuất hàng mượn', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

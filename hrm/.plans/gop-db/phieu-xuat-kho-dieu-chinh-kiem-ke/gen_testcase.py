# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu xuất kho điều chỉnh kiểm kê" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan,
loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (xác định từ code 09/11/2026): chứng từ có trạng thái (Đang tạo / Chờ duyệt / Đang hạch toán / Đã hạch toán), có Tạo
mới (Lưu nháp, Lưu và tiếp tục), Sửa (Đang tạo + người tạo), Gửi duyệt (trừ tồn), bước duyệt của Kế toán kho = nút Tạo phiếu xuất
hàng (lưu phiếu xuất hàng đổi trạng thái phiếu này), In phiếu / In danh sách, Lịch sử. KHÔNG có Xóa, Khóa, Không duyệt, Hủy,
Import (kiểm code: không route / nút) sang bỏ các nhóm đó. Nhóm: I Hiển thị · II Tìm kiếm & lọc (gồm Cài đặt bộ lọc) · III Thêm mới ·
IV Chỉnh sửa · V Gửi duyệt · VI Duyệt phiếu (Tạo phiếu xuất hàng) · VII Lịch sử · VIII Xem chi tiết · IX In phiếu (gồm In danh
sách) · X Tùy chỉnh cột · XI Xuất danh sách Excel · XII Ràng buộc · XIII Phân quyền (cuối). Mỗi case ghi stt checklist nó phủ (ck)
— gen_checklist.py đọc CK.
Khuôn: ../phieu-xuat-dieu-chinh-sai-so-lieu/gen_testcase.py.
Nguồn hành vi (đọc 09/11/2026, nhánh develop cả 2 repo): FE pages/warehouse/inventory-exports/**; BE WarehouseInventoryExport
(Entity / Controller / Service / WriteService), InventoryExportWriteService::afterSave, PhysicalStockWriter::exportShortage,
SelfInventory::canInventoryExport.
Số liệu mẫu: dev-hrm 09/11/2026 (DNS Admin — Super admin): 76 phiếu (72 Đã hạch toán, 2 Đang hạch toán, 2 Chờ duyệt, 0 Đang tạo).
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
from tc_phieu_bosung import ListScreen, open_menu_case, filter_memory_cases, combo_cases, org_cases, check_no_dash_pre  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Kho > menu "Xuất kho" > bấm "Phiếu xuất kho điều chỉnh kiểm kê".'
KK_MENU = 'Vào phân hệ Kho > menu "Kiểm kho" > "Theo vị trí" > bấm "Kiểm kê theo hàng hóa".'
PX_MENU = 'Vào phân hệ Tài chính > nhóm "Hàng hoá - Dịch vụ - Vận chuyển" > menu "Xuất hàng" > bấm "Phiếu xuất hàng điều chỉnh kiểm kê".'
ADV = 'Bấm Tìm kiếm nâng cao.'
REQ = '"Bắt buộc phải nhập"'

PRE_LIST = ('Tài khoản DNS Admin (Super admin); hệ thống có 76 phiếu: 72 Đã hạch toán, 2 Đang hạch toán (PXKĐCKK-00088, 00084), '
            '2 Chờ duyệt (PXKĐCKK-00091, 00083), chưa có phiếu Đang tạo.')
P91 = ('Phiếu PXKĐCKK-00091: Phiếu kiểm kê TPE.KKK-01095, Kho "LN - Liên Ninh", Người tạo "HDQT - DNS Admin", Ngày tạo 05/11/2026 '
       '15:04, Chờ duyệt, Ghi chú "g"; 1 dòng "Đèn soi màu sơn 3000 lumens" (Model MULTIMATCH3, Mã 3M-035653, ĐVT Bộ, Vị trí '
       '"XỬ LÝ C/TỪ", Lô NHAPDIEUCHINH-97-16747-39, SL xuất 1, Đơn giá bán 1, Thành tiền bán 1).')
P90 = ('Phiếu PXKĐCKK-00090 (TPE.KKK-01087, Kho LN - Liên Ninh, Đã hạch toán, Người duyệt DNS Admin, Ngày duyệt 02/11/2026 11:17) '
       'có 3 mốc lịch sử: Tạo mới 30/10/2026 22:58; Thay đổi trạng thái 02/11/2026 11:16 Chờ duyệt sang Đang hạch toán; Thay đổi '
       'trạng thái 02/11/2026 11:17 Đang hạch toán sang Đã hạch toán, ghi chú "Phiếu xuất hàng điều chỉnh kiểm kê PXHĐCKK-00073.".')
ACC_L = ('Tài khoản L: có quyền "Xử lý phiếu kiểm kê hàng hóa", không có quyền xem phiếu xuất kho điều chỉnh kiểm kê, không phải Kế '
         'toán kho.')
SI = ('Phiếu kiểm kê TPE.KKK-01096 (Chờ xử lý) có 3 kho: "CSKH - Chăm sóc khách hàng" và "DATD - Kho Dự án trọng điểm" không còn '
      'hàng thiếu, "HP - Hải Phòng" còn hàng thiếu chưa xử lý; chưa có phiếu xuất kho điều chỉnh; kho đủ tồn.')
PRE_FORM = ACC_L + '\n' + SI
TAO = [MENU, 'Bấm "Tạo mới".']
CHON = TAO + ['Chọn Phiếu kiểm kê = TPE.KKK-01096.', 'Chọn Kho = HP - Hải Phòng.']
DRAFT = ('Phiếu PXKĐCKK-00092 do L lập từ TPE.KKK-01096 (Kho HP - Hải Phòng), trạng thái Đang tạo, Ghi chú "Nháp", chưa có file.')
PRE_EDIT = ACC_L + '\n' + DRAFT
SUA = [MENU, 'Ở dòng PXKĐCKK-00092 bấm Sửa (biểu tượng bút chì).']
ACC_K = 'Tài khoản K: có quyền "Kế toán kho" (Công ty TPE), không có quyền xem theo tổng công ty / công ty.'
ACC_Q1 = 'Tài khoản Q1: có quyền "Xem phiếu xuất kho điều chỉnh kiểm kê - theo tổng công ty".'
ACC_Q2 = 'Tài khoản Q2: có quyền "Xem phiếu xuất kho điều chỉnh kiểm kê - theo công ty", đang làm việc ở công ty TPSG.'
ACC_N = 'Tài khoản N: không có quyền nào của màn; đã tự lập 1 phiếu PXKĐCKK-00093 (Chờ duyệt).'
FILE = 'File: bien_ban.pdf (1 MB)'

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
     'Màn Phiếu xuất kho điều chỉnh kiểm kê (mã PXKĐCKK-NNNNN) dùng để xuất khỏi kho phần hàng THIẾU phát hiện khi kiểm kê theo hàng '
     'hóa: người xử lý phiếu kiểm kê lập phiếu cho 1 kho, Gửi duyệt thì hệ thống trừ ngay tồn kho theo đúng lô, đúng vị trí và báo '
     'Kế toán kho; Kế toán kho lập Phiếu xuất hàng điều chỉnh kiểm kê để hạch toán.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Danh sách: phiếu trong phạm vi xem (theo tổng công ty: mọi phiếu; theo công ty: phiếu của công ty đang làm việc; không có '
     'quyền: phiếu mình tạo); Kế toán kho thấy thêm mọi phiếu Chờ duyệt.\n'
     '- 4 trạng thái: Đang tạo (xám), Chờ duyệt (vàng), Đang hạch toán (xanh dương), Đã hạch toán (xanh lá).\n'
     '- Bảng Chi tiết: các dòng hàng thiếu chưa xử lý của phiếu kiểm kê tại kho đã chọn (vị trí, lô, SL xuất, đơn giá, thành tiền).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác luôn bị ẩn.\n- Phiếu ngoài phạm vi: không có trong danh sách, mở đường link ra trang không tìm '
     'thấy.\n- Ô Phiếu kiểm kê không liệt kê phiếu kiểm kê đã có phiếu xuất điều chỉnh / hết hàng thiếu / không ở Chờ xử lý, Đang xử lý.\n'
     '- Màn không có Xóa, Khóa / Mở khóa, Không duyệt, Hủy, Import.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo ngày tạo phiếu, lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Phiếu kiểm kê > phiếu xuất kho điều chỉnh (1 kho) > dòng hàng (hàng, ĐVT, vị trí, lô, SL xuất, giá).\n'
     '- Mỗi phiếu kiểm kê chỉ lập 1 phiếu xuất kho điều chỉnh.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- SL xuất = phần thiếu (chênh lệch âm) trừ số đã xử lý.\n- Thành tiền bán = SL xuất × Đơn giá bán.\n'
     '- Kiểm tồn kế toán cộng dồn SL các dòng cùng hàng, cùng công ty của lô.'),
    ('7. Phân quyền cấp',
     '- Xem phiếu xuất kho điều chỉnh kiểm kê - theo tổng công ty: mọi phiếu; có ô Công ty, Phòng ban.\n'
     '- Xem phiếu xuất kho điều chỉnh kiểm kê - theo công ty: phiếu của công ty đang làm việc; có ô Phòng ban.\n'
     '- Kế toán kho: thêm mọi phiếu Chờ duyệt, nút Tạo phiếu xuất hàng, nhận thông báo Chờ duyệt.\n'
     '- Xử lý phiếu kiểm kê hàng hóa: lập phiếu.\n- Sửa / Gửi duyệt phiếu Đang tạo: chỉ người tạo.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là khoảng số thứ tự trang đang xem, N là tổng phiếu khớp bộ lọc trong phạm vi xem.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: L (lập phiếu), K (Kế toán kho), Q1, Q2, N (không quyền), DNS Admin (Super admin).\n'
     '- Lưu ý: Gửi duyệt TRỪ TỒN NGAY, không hoàn tác; chạy trên dữ liệu thử.\n'
     '- Lưu ý: ô Ghi chú luôn có dấu * nhưng chỉ bắt buộc khi Gửi duyệt; File đính kèm cũng chỉ bắt khi Gửi duyệt.\n'
     '- Lưu ý: cột "Ngày kiểm kê" hiển thị ngày lập phiếu xuất (giữ như hệ thống cũ).\n'
     '- Màn Tạo / Sửa / Chi tiết là TRANG riêng, không phải cửa sổ nổi.'),
]

SCREEN = ListScreen(menu=MENU, title='Danh sách phiếu xuất kho điều chỉnh kiểm kê', total=76, quick_label='số phiếu',
                    quick_sample='PXKĐCKK-00091', quick_hit='phiếu PXKĐCKK-00091',
                    filters=[('Trạng thái', 'Chờ duyệt'), ('Kho', 'LN - Liên Ninh')])

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Thanh tiêu đề và tab: "Phiếu xuất kho điều chỉnh kiểm kê".', 'Tiêu đề bảng: "Danh sách phiếu xuất kho điều chỉnh kiểm kê".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE_LIST, [MENU, 'Quan sát khối bộ lọc, thanh công cụ, cột Hành động.'], '—',
       ['Khối "Bộ lọc danh sách": ô tìm nhanh (gợi ý "Tìm theo số phiếu"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
        'Thanh công cụ: Tạo mới, Xuất Excel, In danh sách, nút biểu tượng cột.',
        'Cột Hành động: In, Lịch sử mọi dòng; Tạo phiếu xuất hàng ở dòng Chờ duyệt; không có Xóa.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 11 cột: STT, Số phiếu, Phiếu kiểm kê, Ngày kiểm kê, Kho, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái, '
        'Hành động.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 11/11 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp phiếu', 'P0', [PRE_LIST, P91], [MENU, 'Đối chiếu dòng PXKĐCKK-00091.'], '—',
       ['Phiếu kiểm kê "TPE.KKK-01095" (liên kết), Ngày kiểm kê 05/11/2026, Kho "LN - Liên Ninh", Người tạo "HDQT - DNS Admin", '
        'Ngày tạo 05/11/2026 15:04.', 'Người duyệt, Ngày duyệt trống; nhãn vàng "Chờ duyệt".'], 6)
S1.add('Cột Ngày kiểm kê là ngày lập phiếu', 'P2', [PRE_LIST, P91], [MENU, 'So cột Ngày kiểm kê và Ngày tạo của PXKĐCKK-00091.'], '—',
       ['Ngày kiểm kê 05/11/2026 trùng ngày của Ngày tạo.', 'Lưu ý: giữ như hệ thống cũ, không phải ngày kiểm kê của phiếu kiểm kê.'], 6)
S1.add('Người duyệt / Ngày duyệt của phiếu đã hạch toán', 'P1', [PRE_LIST, P90], [MENU, 'Đối chiếu dòng PXKĐCKK-00090.'], '—',
       ['Người duyệt "DNS Admin", Ngày duyệt "02/11/2026 11:17", nhãn xanh lá "Đã hạch toán".'], 6)
S1.add('Liên kết Phiếu kiểm kê mở ở tab mới', 'P1', [PRE_LIST, P91], [MENU, 'Ở dòng PXKĐCKK-00091 bấm "TPE.KKK-01095".'], '—',
       ['Mở chi tiết phiếu kiểm kê ở TAB MỚI.', 'Tab danh sách giữ nguyên trang, bộ lọc.'], 6)
S1.add('Trạng thái bản ghi', 'P0', PRE_LIST, [MENU, 'Quan sát cột Trạng thái của 00091, 00088, 00090.'], '—',
       ['00091: vàng "Chờ duyệt"; 00088: xanh dương "Đang hạch toán"; 00090: xanh lá "Đã hạch toán".',
        'Phiếu Đang tạo (khi có) hiện nhãn xám "Đang tạo".'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', ['Tài khoản mới, không có quyền nào, chưa lập phiếu nào.'], ['Đăng nhập.', MENU], '—',
       ['Bảng hiện "Không có dữ liệu phù hợp.", không có dòng "Hiển thị".', 'Không báo lỗi.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'],
       'Ô tìm nhanh: ZZZ999', ['Bảng hiện "Không có dữ liệu phù hợp.".', 'Không báo lỗi.'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 20 phiếu, tự về trang 1, "Hiển thị 1–20 / 76".', 'Ô có các lựa chọn 5, 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–20 / 76".', 'Bước 3: "Hiển thị 1–10 / 76".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—',
       ['Bước 2: trang 8, "Hiển thị 71–76 / 76".', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang 8 quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2, rồi trang 8.'], '—',
       ['Trang 2: STT 11–20; trang 8: STT 71–76.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 3.', ADV, 'Chọn Trạng thái = Đã hạch toán.'],
       'Trạng thái: Đã hạch toán', ['Tự nạp lại ở trang 1; "Hiển thị 1–10 / 72".'], 17)
S1.add('Sắp xếp tăng dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Số phiếu.'], '—',
       ['Số phiếu nhỏ nhất ở trên cùng, tăng dần; mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Số phiếu 2 lần.'], '—',
       ['PXKĐCKK-00091 trên cùng, giảm dần; mũi tên xuống.'], 21)
S1.add('Sắp xếp theo Ngày tạo', 'P1', PRE_LIST, [MENU, 'Bấm tiêu đề Ngày tạo.', 'Bấm lần nữa.'], '—',
       ['Lần 1: cũ nhất trên.', 'Lần 2: mới nhất trên (PXKĐCKK-00091, 05/11/2026 15:04).', 'Mặc định khi mới vào: mới nhất trên.'], 22)
S1.add('Sắp xếp theo Ngày duyệt', 'P1', PRE_LIST, [MENU, 'Bấm tiêu đề Ngày duyệt 2 lần.'], '—',
       ['Giảm dần: PXKĐCKK-00084 (07/11/2026 09:25) trên cùng; phiếu chưa có ngày duyệt nằm cuối.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Phiếu kiểm kê, Ngày kiểm kê, Kho, Người tạo, Người duyệt, Trạng thái, Hành động.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Số phiếu (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự tăng của Số phiếu.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 3.', 'Bấm tiêu đề Ngày tạo.'], '—', ['Về trang 1.'], 25)
S1.add('Bấm sắp xếp không làm vỡ bố cục bảng', 'P2', PRE_LIST, [MENU, 'Bấm tiêu đề Ngày tạo nhiều lần.'], '—',
       ['Độ rộng các cột giữ nguyên, mũi tên sắp xếp không nhảy chỗ.'], 22)
S1.add('Mở màn từ số chứng từ ở Thẻ kho', 'P1', [PRE_LIST, 'Thẻ kho của hàng 3M-035653 kho LN - Liên Ninh có dòng xuất PXKĐCKK-00091.'],
       ['Vào phân hệ Kho > menu "Báo cáo kho" > bấm "Thẻ kho".', 'Lọc hàng 3M-035653, kho LN - Liên Ninh.', 'Bấm số chứng từ PXKĐCKK-00091.'],
       '—', ['Mở màn "Chi tiết phiếu xuất kho điều chỉnh kiểm kê: PXKĐCKK-00091".'], 1)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo số phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "PXKĐCKK-00091", bấm Tìm kiếm.'], 'Ô tìm nhanh: PXKĐCKK-00091',
       ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần số phiếu', 'P0', PRE_LIST, [MENU, 'Nhập "0009", bấm Tìm kiếm.'], 'Ô tìm nhanh: 0009',
       ['Còn PXKĐCKK-00090, PXKĐCKK-00091.'], 27)
S2.add('Ô tìm nhanh không tìm theo mã phiếu kiểm kê', 'P1', PRE_LIST, [MENU, 'Nhập "TPE.KKK-01095", bấm Tìm kiếm.'], '—',
       ['"Không có dữ liệu phù hợp." (ô tìm nhanh chỉ tìm theo số phiếu).'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "pxkđckk-00091", bấm Tìm kiếm.'], '—',
       ['Ra phiếu PXKĐCKK-00091 như khi gõ chữ hoa.'], 28)
S2.add('Có dấu / không dấu', 'P2', PRE_LIST, [MENU, 'Nhập "PXKDCKK-00091" (chữ D không gạch), bấm Tìm kiếm.'], '—',
       ['Kết quả theo cách so khớp của hệ thống: chữ Đ và D có thể không được coi là một; ghi nhận kết quả thực tế.',
        'Lưu ý: số phiếu có chữ Đ, nhập đúng "PXKĐCKK" để tìm.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; % được hiểu là ký tự đại diện nên ra cả 76 phiếu.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  PXKĐCKK-00091  ", bấm Tìm kiếm.'], '—',
       ['Ra phiếu PXKĐCKK-00091.'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "PXKĐCKK-00091", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Hiện lại đủ 76 phiếu.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST,
       [MENU, 'Nhập "PXKĐCKK-00091", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'], '—',
       ['Cả 2 cách đều ra phiếu PXKĐCKK-00091, về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['Các ô Mã phiếu, Kho, Trạng thái, Người tạo, Mã hàng hóa, Tên hàng hóa, Ngày tạo, Công ty, Phòng ban đều trống.',
        'Đủ 76 phiếu.'], 36)
S2.add('Lọc Mã phiếu', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "00088" vào ô Mã phiếu.'], '—', ['Lọc ngay khi gõ; còn PXKĐCKK-00088.'], 37)
S2.add('Lọc Kho', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = LN - Liên Ninh.'], '—',
       ['Ô Kho có 4 lựa chọn: LN - Liên Ninh, PTT - Phan Trọng Tuệ, SG - Kho Sài Gòn, SG-CSKH - Kho Sài Gòn - Chăm sóc khách hàng.',
        'Còn 6 phiếu: PXKĐCKK-00091, 00090, 00089, 00088, 00086, 00085.'], 37)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Chờ duyệt.'], '—',
       ['Ô có 4 lựa chọn: Đang tạo, Chờ duyệt, Đang hạch toán, Đã hạch toán.', 'Còn 2 phiếu PXKĐCKK-00091, 00083.'], 37)
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = "HDQT - DNS Admin".'], '—',
       ['Ô liệt kê 3 người: HDQT - DNS Admin, SG_CSKH - Nguyễn Thị Thuỳ Trang, SG_KHO - Nguyễn Thu Hòa.',
        'Còn 9 phiếu PXKĐCKK-00083 đến 00091.'], 37)
S2.add('Lọc Mã hàng hóa', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "3M-035653" vào ô Mã hàng hóa.'], '—',
       ['Còn các phiếu có ít nhất 1 dòng hàng mã chứa "3M-035653" (có PXKĐCKK-00091).'], 37)
S2.add('Lọc Tên hàng hóa', 'P1', PRE_LIST, [MENU, ADV, 'Gõ "mặt nạ" vào ô Tên hàng hóa.'], '—',
       ['Còn các phiếu có dòng hàng tên chứa "mặt nạ" (có PXKĐCKK-00090), không phân biệt hoa / thường.'], 37)
S2.add('Lọc Ngày tạo lấy trọn ngày biên', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày tạo 22/10/2026 – 24/10/2026.'], '—',
       ['Còn 5 phiếu: 00087 (24/10 15:45), 00086 (23/10), 00085, 00084, 00083 (22/10).', 'Bỏ trống ngày cuối vẫn lọc được.'], 37)
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = SG - Kho Sài Gòn.', 'Chọn Trạng thái = Đang hạch toán.'],
       '—', ['Chỉ còn PXKĐCKK-00084.'], 38)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST,
       [MENU, 'Nhập "PXKĐCKK-00091", bấm Tìm kiếm.', ADV, 'Chọn Trạng thái = Đã hạch toán.'], '—',
       ['"Không có dữ liệu phù hợp." vì 00091 đang Chờ duyệt.'], [39, 40])
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đã hạch toán.', 'Bấm trang cuối.'], '—',
       ['Dòng "Hiển thị" ghi tổng 72.', 'Trang 8 hiện "Hiển thị 71–72 / 72", STT liên tục.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Kho = LN - Liên Ninh.', ['Bấm tiêu đề Số phiếu.'], '—',
       ['Chỉ 6 phiếu của kho LN được sắp; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "PXKĐCKK", lọc Kho, Trạng thái, sắp Số phiếu, ở trang 2.',
       ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống, bỏ sắp xếp, nạp lại trang 1, đủ 76 phiếu.'], 44)
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.raw(org_cases(SCREEN, len(S2) + 1), [[37], [37], [37]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Chờ duyệt, chưa mở màn chi tiết.'],
       ['Nhấn F5.'], '—', ['Bộ lọc trở về trống, đủ 76 phiếu (bộ lọc chỉ nhớ khi đi vào màn chi tiết / sửa của màn).'], 46)
S2.add('Ô Công ty chỉ có với quyền tổng công ty', 'P1', [ACC_Q2], ['Đăng nhập Q2.', MENU, ADV], '—',
       ['Không có ô Công ty, chỉ có ô Phòng ban.'], 37)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Tên hàng hóa, bấm Lưu.'], '—',
       ['Cửa sổ liệt kê 8 mục: Mã phiếu, Kho, Trạng thái, Người tạo, Mã hàng hóa, Tên hàng hóa, Ngày tạo, Công ty – Phòng ban.',
        'Báo "Cập nhật thành công"; khối Tìm kiếm nâng cao không còn ô Tên hàng hóa.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Chờ duyệt.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Trạng thái, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị bỏ, nạp lại đủ 76 phiếu.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Tên hàng hóa.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Tên hàng hóa vẫn ẩn.', 'Bước 2: tích đủ 8 mục, Tên hàng hóa hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Ngày tạo lên đầu, bấm Lưu.'], '—',
       ['Ô Ngày tạo đứng đầu khối Tìm kiếm nâng cao; giữ sau khi đăng nhập lại.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo mới từ danh sách', 'P0', PRE_FORM, ['Đăng nhập L.'] + TAO, '—',
       ['Mở TRANG "Tạo phiếu xuất kho điều chỉnh kiểm kê", tab cùng tiêu đề.'], 49)
S3.add('Mở từ chi tiết phiếu kiểm kê', 'P0', PRE_FORM, ['Đăng nhập L.', KK_MENU, 'Mở chi tiết TPE.KKK-01096.',
       'Bấm "Tạo phiếu xuất kho điều chuyển".'], '—',
       ['Mở màn Tạo với Phiếu kiểm kê = TPE.KKK-01096 chọn sẵn, Kho tự điền, bảng Chi tiết đã nạp.'], [49, 53])
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải "<tên L> - <ngày giờ hiện tại>".', 'Không có ô Số phiếu (mã tự sinh khi lưu).'], 50)
S3.add('Các trường, khối và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Phiếu kiểm kê, Kho, Ghi chú (2 dòng, gợi ý "Nhập ghi chú").',
        'Khối "File đính kèm" có nút "Thêm tài liệu"; khối "Chi tiết": STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, Vị trí, Lô, SL '
        'xuất, Đơn giá bán, Thành tiền bán.', 'Chân màn: Lưu nháp, Gửi duyệt, Lưu và tiếp tục, Quay lại.'], [51, 54])
S3.add('Trường bắt buộc / không bắt buộc', 'P0', PRE_FORM, TAO + ['Quan sát dấu *.'], '—',
       ['Phiếu kiểm kê, Kho, Ghi chú, File đính kèm có dấu *.', 'Lưu ý: Ghi chú và File chỉ bắt buộc khi Gửi duyệt.',
        'Bảng Chi tiết chỉ đọc, không sửa số lượng / giá.'], 52)
S3.add('Giá trị mặc định', 'P0', PRE_FORM, TAO, '—',
       ['Ô Phiếu kiểm kê trống (gợi ý "Chọn phiếu kiểm kê"); Kho khóa; Ghi chú trống; chưa có file.',
        'Bảng ghi "Chọn phiếu kiểm kê để nạp hàng thiếu cần xuất điều chỉnh".'], 53)
S3.add('Danh sách ô Phiếu kiểm kê', 'P0', PRE_FORM, TAO + ['Mở ô Phiếu kiểm kê.'], '—',
       ['Chỉ liệt kê phiếu kiểm kê Chờ xử lý / Đang xử lý còn hàng thiếu chưa có phiếu xuất điều chỉnh, mới nhất trên (có TPE.KKK-01096).',
        'Biểu tượng i cạnh nhãn: "Chỉ liệt kê phiếu kiểm kê Chờ xử lý / Đang xử lý còn hàng thiếu chưa xuất điều chỉnh."'], [51, 53])
S3.add('Chọn phiếu kiểm kê thì tự điền Kho và nạp hàng', 'P0', PRE_FORM, TAO + ['Chọn Phiếu kiểm kê = TPE.KKK-01096.'], '—',
       ['Kho mở khóa, tự điền "CSKH - Chăm sóc khách hàng" (kho đầu tiên của phiếu).',
        'Bảng ghi "Kho này không còn hàng thiếu cần xuất điều chỉnh".', 'Cạnh nhãn Phiếu kiểm kê có biểu tượng mở phiếu ở tab mới.'],
       [53, 269])
S3.add('Đổi kho thì nạp lại hàng thiếu', 'P0', PRE_FORM, CHON, '—',
       ['Ô Kho chỉ có 3 kho của TPE.KKK-01096.', 'Chọn HP - Hải Phòng: bảng nạp các dòng thiếu (vị trí, lô, SL xuất, đơn giá, '
        'thành tiền) của kho Hải Phòng.'], [53, 269])
S3.add('Lưu nháp với dữ liệu hợp lệ đầy đủ', 'P0', PRE_FORM, CHON + ['Nhập Ghi chú, thêm file.', 'Bấm Lưu nháp.'],
       ['Ghi chú: Xuất hàng thiếu kho HP', FILE],
       ['Báo "Lưu thành công.", về danh sách.', 'Dòng mới trên cùng mã PXKĐCKK-NNNNN kế tiếp, Kho HP - Hải Phòng, Người tạo L, nhãn '
        'xám "Đang tạo".'], [55, 79, 85])
S3.add('Lưu nháp chỉ với trường bắt buộc', 'P0', PRE_FORM, CHON + ['Bấm Lưu nháp.'], 'Ghi chú, File: để trống',
       ['Lưu được, phiếu Đang tạo, Ghi chú trống.'], [56, 57])
S3.add('Dữ liệu sau lưu', 'P0', PRE_FORM, CHON + ['Bấm Lưu nháp.', 'Bấm số phiếu vừa tạo.'], '—',
       ['Màn chi tiết đúng Phiếu kiểm kê TPE.KKK-01096, Kho HP - Hải Phòng.', 'Bảng Chi tiết đúng các dòng như lúc lập.'], 58)
S3.add('Trạng thái mặc định sau lưu', 'P0', PRE_FORM, CHON + ['Bấm Lưu nháp.'], '—',
       ['Phiếu ở trạng thái Đang tạo (nhãn xám), chưa trừ tồn.', 'Phiếu kiểm kê TPE.KKK-01096 chuyển "Đang xử lý".'], [59, 281])
S3.add('Lịch sử tạo', 'P1', PRE_FORM, CHON + ['Bấm Lưu nháp.', 'Ở dòng phiếu mới bấm Lịch sử.'], '—',
       ['Có 1 mốc "Tạo mới", người thực hiện L.'], [60, 176])
S3.add('Lưu nháp khi chưa chọn Phiếu kiểm kê', 'P0', PRE_FORM, TAO + ['Bấm Lưu nháp.'], '—',
       ['Ô Phiếu kiểm kê viền đỏ, dưới ô ' + REQ + '.', 'Thông báo "Bạn chưa nhập đầy đủ thông tin."; không lưu.'],
       [61, 70, 80])
S3.add('Kho không còn hàng thiếu thì bị chặn', 'P0', PRE_FORM, TAO + ['Chọn Phiếu kiểm kê = TPE.KKK-01096 (kho CSKH).',
       'Bấm Lưu nháp.'], '—', ['Dưới bảng hiện "Kho không còn hàng thiếu cần xuất điều chỉnh."; không lưu.'], [62, 268])
S3.add('Ghi chú tối đa 255 ký tự', 'P1', PRE_FORM, CHON + ['Dán chuỗi 300 ký tự vào Ghi chú.'], 'Ghi chú: 300 ký tự',
       ['Ô chỉ nhận 255 ký tự đầu (không gõ thêm được).'], [66, 74, 81])
S3.add('Ghi chú đúng 255 ký tự', 'P1', PRE_FORM, CHON + ['Nhập Ghi chú đúng 255 ký tự.', 'Bấm Lưu nháp.'], 'Ghi chú: 255 ký tự',
       ['Lưu được, hiển thị đủ 255 ký tự.'], 65)
S3.add('Ghi chú 1 ký tự', 'P2', PRE_FORM, CHON + ['Nhập Ghi chú "a".', 'Bấm Lưu nháp.'], 'Ghi chú: a', ['Lưu được.'], 64)
S3.add('Ký tự đặc biệt trong Ghi chú', 'P2', PRE_FORM, CHON + ['Nhập Ghi chú "<b>Test</b> & @#$%".', 'Bấm Lưu nháp.'], '—',
       ['Lưu được; màn chi tiết và bản in hiện nguyên chuỗi, không in đậm.'], 63)
S3.add('Ghi chú khoảng trắng đầu / cuối', 'P2', PRE_FORM, CHON + ['Nhập Ghi chú "  Thiếu hàng  ".', 'Bấm Lưu nháp.'], '—',
       ['Lưu được; khoảng trắng đầu / cuối không làm lỗi.'], 68)
S3.add('Ghi chú chỉ có khoảng trắng khi Lưu nháp', 'P2', PRE_FORM, CHON + ['Nhập Ghi chú "   ".', 'Bấm Lưu nháp.'], '—',
       ['Lưu được (Lưu nháp không bắt Ghi chú).'], 69)
S3.add('File sai định dạng', 'P1', PRE_FORM, CHON + ['Bấm Thêm tài liệu, chọn file "bang.xlsx".'], 'File: bang.xlsx',
       ['Báo "Định dạng file không hợp lệ"; file không được thêm.', 'Chỉ nhận pdf, png, jpg, jpeg.'], [62, 70])
S3.add('File quá 20 MB', 'P2', PRE_FORM, CHON + ['Bấm Thêm tài liệu, chọn file pdf 25 MB.'], 'File: 25 MB',
       ['Báo "File quá lớn"; file không được thêm.'], 62)
S3.add('Một phiếu kiểm kê chỉ lập 1 phiếu', 'P0', [PRE_FORM, 'Đã lưu nháp 1 phiếu từ TPE.KKK-01096.'], TAO + ['Mở ô Phiếu kiểm kê.'],
       '—', ['TPE.KKK-01096 không còn trong danh sách chọn.', 'Mã PXKĐCKK tự sinh, không trùng.'], [67, 75, 82])
S3.add('Mở đường link Tạo với phiếu kiểm kê đã dùng', 'P1', [PRE_FORM, 'TPE.KKK-01096 đã có phiếu xuất kho điều chỉnh.'],
       ['Mở lại đường link màn Tạo vào từ chi tiết TPE.KKK-01096.'], '—',
       ['Dưới ô Phiếu kiểm kê: "Phiếu kiểm kê không còn lập được phiếu xuất kho điều chỉnh hoặc bạn không có quyền."; ô bỏ chọn.'], 67)
S3.add('Lỗi biến mất sau khi sửa', 'P1', PRE_FORM, TAO + ['Bấm Lưu nháp (báo lỗi Phiếu kiểm kê).', 'Chọn Phiếu kiểm kê.'], '—',
       ['Chữ đỏ dưới ô biến mất ngay khi chọn.'], 71)
S3.add('Tồn kế toán không đủ thì bị chặn', 'P0', [PRE_FORM, 'Hàng thiếu đầu tiên ở kho HP đang bị giữ hàng hết tồn kế toán của công ty.'],
       CHON + ['Bấm Lưu nháp.'], '—',
       ['Dưới bảng: "<mã hàng>: Tồn kế toán không đủ để xuất (SL được xuất: X, SL xuất: Y). Kiểm tra hàng đang giữ chỗ/giữ hàng của '
        'công ty."', 'Không lưu.'], [62, 304])
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, CHON + ['Bấm Lưu và tiếp tục.'], '—',
       ['Báo "Lưu thành công.", ở lại màn Thêm với form trống.', 'Danh sách phiếu kiểm kê nạp lại, không còn TPE.KKK-01096.'],
       [72, 76, 77])
S3.add('Lưu và tiếp tục khi thiếu Phiếu kiểm kê', 'P1', PRE_FORM, TAO + ['Bấm Lưu và tiếp tục.'], '—',
       [REQ + ' dưới ô Phiếu kiểm kê; không lưu, form giữ nguyên.'], 73)
S3.add('Đóng sau Lưu và tiếp tục', 'P2', PRE_FORM, CHON + ['Bấm Lưu và tiếp tục.', 'Bấm Quay lại.'], '—',
       ['Về danh sách ngay (form trống, không hỏi); phiếu vừa lưu có trong danh sách.'], 78)
S3.add('Lưu nháp: popup còn mở và trường làm mới', 'P2', PRE_FORM, CHON + ['Bấm Lưu nháp.'], '—',
       ['Màn là trang: Lưu nháp xong về danh sách (không còn form).', 'Mở Tạo mới lại thì form trống.'], [83, 84])
S3.add('Quay lại khi chưa nhập gì', 'P1', PRE_FORM, TAO + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 93)
S3.add('Quay lại khi đã chọn / nhập', 'P0', PRE_FORM, CHON + ['Nhập Ghi chú.', 'Bấm Quay lại.'], '—',
       ['Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" với nút Thoát, Ở lại.'], [94, 95])
S3.add('Chọn Thoát', 'P1', PRE_FORM, CHON + ['Bấm Quay lại.', 'Bấm Thoát.'], '—',
       ['Về danh sách, không tạo phiếu.'], 96)
S3.add('Chọn Ở lại', 'P1', PRE_FORM, CHON + ['Bấm Quay lại.', 'Bấm Ở lại.'], '—',
       ['Ở lại form, dữ liệu đã chọn / nhập giữ nguyên.'], 97)
S3.add('Nhập rồi xóa hết', 'P2', PRE_FORM, TAO + ['Nhập Ghi chú rồi xóa hết.', 'Bấm Quay lại.'], '—',
       ['Về danh sách ngay, không hỏi.'], 98)
S3.add('Chọn rồi bỏ chọn Phiếu kiểm kê', 'P2', PRE_FORM, TAO + ['Chọn Phiếu kiểm kê rồi bấm × bỏ chọn.', 'Bấm Quay lại.'], '—',
       ['Kho, bảng Chi tiết trở về trống.', 'Về danh sách không hỏi (dữ liệu như ban đầu).'], 99)
S3.add('Để màn lâu không thao tác', 'P2', [PRE_FORM, 'Đã mở màn, để nguyên 30 phút.'], CHON + ['Bấm Lưu nháp.'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên, về màn đăng nhập, không lưu.'], 100)
S3.add('Bấm Lưu nháp liên tục', 'P1', PRE_FORM, CHON + ['Bấm Lưu nháp 3 lần thật nhanh.'], '—',
       ['Nút khóa trong lúc lưu; chỉ tạo 1 phiếu.'], 101)
S3.add('Hai tab cùng lập từ 1 phiếu kiểm kê', 'P1', [PRE_FORM, 'Tab 1 và tab 2 cùng mở form, cùng chọn TPE.KKK-01096 / HP.'],
       ['Tab 1 bấm Lưu nháp.', 'Tab 2 bấm Lưu nháp.'], '—',
       ['Tab 1 lưu được.', 'Tab 2 báo "Phiếu kiểm kê không còn lập được phiếu xuất kho điều chỉnh. Vui lòng load lại trang"; chỉ có 1 '
        'phiếu.'], 102)
S3.add('Không có quyền xử lý phiếu kiểm kê', 'P1', [ACC_N], ['Đăng nhập N.'] + TAO + ['Mở ô Phiếu kiểm kê.'], '—',
       ['Form vẫn mở, ô Phiếu kiểm kê không có lựa chọn nào; không lập được phiếu.'], [52, 295])

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
S4.add('Mở màn Sửa từ cột Hành động', 'P0', PRE_EDIT, ['Đăng nhập L.'] + SUA, '—',
       ['Mở trang "Sửa phiếu xuất kho điều chỉnh kiểm kê: PXKĐCKK-00092".'], 103)
S4.add('Mở màn Sửa từ màn chi tiết', 'P1', PRE_EDIT, [MENU, 'Bấm PXKĐCKK-00092.', 'Bấm Sửa ở chân màn.'], '—',
       ['Mở màn Sửa của phiếu.'], 103)
S4.add('Dữ liệu điền đúng', 'P0', PRE_EDIT, SUA, '—',
       ['Phiếu kiểm kê TPE.KKK-01096 (liên kết), Ghi chú "Nháp".', 'Kho "HP - Hải Phòng"; bảng Chi tiết như lúc lưu.'], 104)
S4.add('Trường được / không được sửa', 'P0', PRE_EDIT, SUA, '—',
       ['Chỉ Ghi chú và File đính kèm sửa được.', 'Phiếu kiểm kê là liên kết, Kho khóa (biểu tượng i: "Kho không đổi được sau khi tạo phiếu."), '
        'bảng Chi tiết chỉ đọc.'], 105)
S4.add('Các nút', 'P1', PRE_EDIT, SUA, '—', ['Chân màn: Lưu nháp, Gửi duyệt, Quay lại; không có Lưu và tiếp tục.'], 106)
S4.add('Sửa Ghi chú', 'P0', PRE_EDIT, SUA + ['Sửa Ghi chú thành "Nháp lần 2".', 'Bấm Lưu nháp.'], 'Ghi chú: Nháp lần 2',
       ['Báo "Lưu thành công.", về danh sách; phiếu vẫn Đang tạo.', 'Chi tiết hiện Ghi chú mới.'], [107, 110])
S4.add('Sửa Ghi chú và thêm file', 'P1', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Thêm file bien_ban.pdf.', 'Bấm Lưu nháp.'], FILE,
       ['Lưu được; khối File đính kèm có bien_ban.pdf.'], 108)
S4.add('Giữ nguyên giá trị khi Lưu nháp không đổi', 'P1', PRE_EDIT, SUA + ['Không đổi gì, bấm Lưu nháp.'], '—',
       ['Lưu được, dữ liệu không đổi.', 'Lịch sử không có mốc "Thay đổi thông tin" mới.'], [109, 125, 182])
S4.add('Lịch sử sau khi sửa', 'P0', PRE_EDIT, SUA + ['Sửa Ghi chú thành "Nháp lần 2", Lưu nháp.', 'Bấm Lịch sử ở dòng phiếu.'], '—',
       ['Có mốc "Thay đổi thông tin" người thực hiện L, Ghi chú "Nháp" sang "Nháp lần 2".'], [111, 112, 177])
S4.add('Sửa nhiều thông tin cùng lúc ghi 1 mốc', 'P2', PRE_EDIT, SUA + ['Sửa Ghi chú, thêm 1 file.', 'Lưu nháp.', 'Mở Lịch sử.'], '—',
       ['1 mốc "Thay đổi thông tin" gồm Ghi chú và File đính kèm (dạng bảng).'], [178, 183])
S4.add('Ghi chú vượt 255 ký tự', 'P1', PRE_EDIT, SUA + ['Dán chuỗi 300 ký tự.'], '—', ['Ô chỉ nhận 255 ký tự.'], [114, 115])
S4.add('Bỏ trống Ghi chú khi Lưu nháp', 'P1', PRE_EDIT, SUA + ['Xóa hết Ghi chú.', 'Bấm Lưu nháp.'], '—',
       ['Lưu được (Lưu nháp không bắt Ghi chú).'], 113)
S4.add('Bỏ trống Ghi chú khi Gửi duyệt từ màn Sửa', 'P0', PRE_EDIT, SUA + ['Xóa hết Ghi chú.', 'Bấm Gửi duyệt.'], '—',
       ['Ghi chú viền đỏ ' + REQ + '; khối File ' + REQ + '; "Bạn chưa nhập đầy đủ thông tin.".'], [113, 117])
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P2', PRE_EDIT, SUA + ['Xóa Ghi chú, bấm Gửi duyệt (báo lỗi).', 'Nhập lại Ghi chú.'], '—',
       ['Chữ đỏ dưới Ghi chú biến mất ngay.'], 118)
S4.add('Không có trường duy nhất để trùng', 'P2', PRE_EDIT, SUA, '—',
       ['Màn Sửa không có trường cần kiểm trùng (phiếu kiểm kê / kho khóa).'], 116)
S4.add('Mở Sửa rồi Quay lại không đổi', 'P1', PRE_EDIT, SUA + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 119)
S4.add('Đổi rồi trả về ban đầu', 'P2', PRE_EDIT, SUA + ['Sửa Ghi chú rồi gõ lại "Nháp".', 'Bấm Quay lại.'], '—',
       ['Về danh sách không hỏi.'], 120)
S4.add('Quay lại khi đã đổi', 'P0', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Bấm Quay lại.'], '—',
       ['Hộp "Thông tin chưa lưu" (Thoát / Ở lại).'], 121)
S4.add('Thoát không lưu', 'P1', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Bấm Quay lại, chọn Thoát.'], '—',
       ['Về danh sách; Ghi chú của phiếu vẫn "Nháp".'], [122, 124])
S4.add('Ở lại', 'P2', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Bấm Quay lại, chọn Ở lại.'], '—', ['Giữ form với Ghi chú đã sửa.'], 123)
S4.add('Phiếu đã gửi duyệt không sửa được', 'P0', [ACC_L, 'PXKĐCKK-00092 đã Chờ duyệt.'], [MENU, 'Quan sát dòng 00092.',
       'Mở đường link màn Sửa của 00092.'], '—',
       ['Không có nút Sửa.', 'Mở đường link màn Sửa sang tự chuyển về màn chi tiết.'], [126, 129])
S4.add('Phiếu đổi trạng thái trong lúc đang sửa', 'P1', [PRE_EDIT, 'Tab 1 đang mở màn Sửa; tab 2 vừa Gửi duyệt phiếu.'],
       ['Ở tab 1 bấm Lưu nháp.'], '—', ['Báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang"; không lưu.'], [128, 127])
S4.add('Xóa file đã lưu', 'P1', [ACC_L, 'PXKĐCKK-00092 Đang tạo có file bien_ban.pdf.'], SUA + ['Bấm xóa ở dòng bien_ban.pdf.',
       'Bấm Xóa trong hộp.'], '—',
       ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa file đính kèm này?" (Xóa / Hủy).',
        'Báo "Xóa file thành công", file biến mất ngay (không cần bấm Lưu); lịch sử có mốc thay đổi File đính kèm.'], 108)
S4.add('Người khác không sửa được phiếu Đang tạo', 'P0', [ACC_Q1, DRAFT], ['Đăng nhập Q1.', MENU, 'Tìm PXKĐCKK-00092.'], '—',
       ['Không thấy phiếu (phiếu Đang tạo của người khác luôn ẩn).'], [126, 290])

# ============================================================== V. GỬI DUYỆT
S5 = Sec(5)
S5.add('Gửi duyệt từ màn Tạo với dữ liệu đầy đủ', 'P0', PRE_FORM,
       CHON + ['Nhập Ghi chú, thêm file.', 'Bấm Gửi duyệt.', 'Bấm Gửi duyệt trong hộp xác nhận.'],
       ['Ghi chú: Xuất hàng thiếu kho HP', FILE],
       ['Báo "Gửi duyệt thành công.", về danh sách.', 'Phiếu mới nhãn vàng "Chờ duyệt"; không có nút Sửa.'], [86, 92])
S5.add('Hộp xác nhận gửi duyệt', 'P0', PRE_FORM, CHON + ['Nhập Ghi chú, thêm file.', 'Bấm Gửi duyệt.'], '—',
       ['Hộp "Xác nhận gửi duyệt": "Gửi duyệt sẽ xuất ngay hàng thiếu khỏi kho và không sửa được phiếu nữa. Bạn có chắc muốn gửi '
        'duyệt?" với nút Gửi duyệt, Hủy.'], 90)
S5.add('Gửi duyệt thiếu Ghi chú và File', 'P0', PRE_FORM, CHON + ['Bấm Gửi duyệt.'], '—',
       ['Ghi chú và khối File đính kèm báo ' + REQ + '; "Bạn chưa nhập đầy đủ thông tin."; không hiện hộp xác nhận.'], 87)
S5.add('Gửi duyệt thiếu Phiếu kiểm kê', 'P1', PRE_FORM, TAO + ['Bấm Gửi duyệt.'], '—', [REQ + ' dưới ô Phiếu kiểm kê.'], 87)
S5.add('Gửi duyệt với file sai định dạng', 'P2', PRE_FORM, CHON + ['Nhập Ghi chú.', 'Thêm file "a.docx".'], '—',
       ['File bị từ chối "Định dạng file không hợp lệ"; Gửi duyệt vẫn báo thiếu file.'], 88)
S5.add('Trừ tồn kho ngay khi gửi', 'P0', [PRE_FORM, 'Hàng thiếu dòng 1 ở kho HP: tồn tại vị trí / lô của dòng là 5, SL xuất 2.'],
       CHON + ['Nhập Ghi chú, thêm file.', 'Gửi duyệt, xác nhận.', 'Mở Thẻ kho của hàng dòng 1, kho HP - Hải Phòng.'], '—',
       ['Tồn tại vị trí / lô còn 3.', 'Thẻ kho có dòng xuất với số chứng từ PXKĐCKK-NNNNN.'], [306, 307])
S5.add('Thiếu tồn tại vị trí / lô thì không trừ gì', 'P0', [PRE_FORM, 'Tồn lô của dòng 1 tại vị trí đã bị xuất hết bởi phiếu khác.'],
       CHON + ['Nhập Ghi chú, thêm file.', 'Gửi duyệt, xác nhận.'], '—',
       ['Báo "Hàng <mã - tên> không đủ tồn trong lô tại vị trí <mã vị trí>. Cần X, còn 0" (hoặc câu "không đủ tồn kho" / "không đủ '
        'tồn tại vị trí" tương ứng).', 'Không lưu phiếu, tồn các dòng khác không đổi.'], [304, 285])
S5.add('Bấm Hủy trong hộp xác nhận', 'P0', PRE_FORM, CHON + ['Nhập Ghi chú, thêm file.', 'Bấm Gửi duyệt.', 'Bấm Hủy.'], '—',
       ['Hộp đóng, form giữ nguyên, không lưu, tồn không đổi.'], [91, 310])
S5.add('Gửi duyệt từ màn Sửa', 'P0', [ACC_L, DRAFT, 'Đã thêm file bien_ban.pdf cho phiếu.'],
       SUA + ['Bấm Gửi duyệt, xác nhận.'], '—',
       ['Báo "Gửi duyệt thành công."; phiếu Chờ duyệt; tồn bị trừ như khi gửi từ màn Tạo.',
        'Lịch sử có mốc "Thay đổi trạng thái" Đang tạo sang Chờ duyệt.'], [86, 305])
S5.add('Thông báo tới Kế toán kho', 'P0', [PRE_FORM, ACC_K, 'L và K cùng công ty TPE.'], CHON + ['Nhập Ghi chú, thêm file.',
       'Gửi duyệt, xác nhận.', 'Đăng nhập K, mở chuông thông báo.'], '—',
       ['K nhận "[XKĐCKK] Chờ duyệt: <mã phiếu>. Người gửi: <tên L>. Kho: <tên kho>".', 'Bấm thông báo sang mở chi tiết phiếu.'], [308, 309])
S5.add('Kế toán kho khác công ty không nhận thông báo', 'P1', [PRE_FORM, 'Tài khoản K2 Kế toán kho công ty TPSG.'],
       CHON + ['Gửi duyệt phiếu (đủ dữ liệu).', 'Đăng nhập K2, mở chuông.'], '—',
       ['K2 không nhận thông báo; vẫn thấy phiếu Chờ duyệt trong danh sách.'], 308)
S5.add('Bấm Gửi duyệt liên tục', 'P1', PRE_FORM, CHON + ['Nhập Ghi chú, thêm file.', 'Bấm Gửi duyệt trong hộp nhiều lần nhanh.'],
       '—', ['Chỉ tạo 1 phiếu, tồn chỉ bị trừ 1 lần.'], 101)
S5.add('Phiếu đã Chờ duyệt không gửi lại được', 'P1', [ACC_L, 'PXKĐCKK-00092 đã Chờ duyệt.'], [MENU, 'Mở chi tiết 00092.'], '—',
       ['Không có nút Sửa / Gửi duyệt.'], 311)
S5.add('Trường được làm mới sau gửi duyệt', 'P2', PRE_FORM, CHON + ['Gửi duyệt (đủ dữ liệu).', 'Bấm Tạo mới lại.'], '—',
       ['Form mới trống; TPE.KKK-01096 không còn trong ô Phiếu kiểm kê.'], [89, 91])

# ============================================================== VI. DUYỆT PHIẾU (Tạo phiếu xuất hàng)
S6 = Sec(6)
PRE_K = [ACC_K, P91]
S6.add('Nút Tạo phiếu xuất hàng hiện đúng điều kiện', 'P0', PRE_K, ['Đăng nhập K.', MENU], '—',
       ['Dòng Chờ duyệt (00091, 00083) có nút Tạo phiếu xuất hàng.', 'Dòng Đang hạch toán / Đã hạch toán không có.'], 300)
S6.add('Mở màn Tạo phiếu xuất hàng', 'P0', PRE_K, ['Đăng nhập K.', MENU, 'Ở dòng 00091 bấm Tạo phiếu xuất hàng.'], '—',
       ['Mở màn "Tạo phiếu xuất hàng điều chỉnh kiểm kê" chọn sẵn phiếu PXKĐCKK-00091.',
        'Màn có nút Lưu, Lưu và tiếp tục, Lưu và duyệt, Quay lại.'], 301)
S6.add('Mở từ màn chi tiết', 'P1', PRE_K, ['Đăng nhập K.', MENU, 'Bấm PXKĐCKK-00091.', 'Bấm Tạo phiếu xuất hàng.'], '—',
       ['Mở cùng màn như từ danh sách.'], 301)
S6.add('Lưu phiếu xuất hàng thì phiếu Đang hạch toán', 'P0', PRE_K,
       ['Đăng nhập K.', 'Mở Tạo phiếu xuất hàng từ 00091.', 'Nhập đủ thông tin, bấm Lưu.', 'Mở lại danh sách phiếu xuất kho.'], '—',
       ['00091 chuyển xanh dương "Đang hạch toán"; Người duyệt = K, Ngày duyệt = lúc lưu.'], [302, 305])
S6.add('Lưu và duyệt thì phiếu Đã hạch toán', 'P0', PRE_K,
       ['Đăng nhập K.', 'Mở Tạo phiếu xuất hàng từ 00091.', 'Nhập đủ, bấm Lưu và duyệt.', 'Mở lại danh sách.'], '—',
       ['00091 chuyển xanh lá "Đã hạch toán"; Người duyệt / Ngày duyệt được ghi.'], [302, 305, 306])
S6.add('Thiếu dữ liệu ở phiếu xuất hàng', 'P1', PRE_K, ['Đăng nhập K.', 'Mở Tạo phiếu xuất hàng từ 00091.', 'Bấm Lưu và duyệt khi thiếu thông tin bắt buộc.'],
       '—', ['Màn phiếu xuất hàng báo lỗi tại ô; phiếu 00091 vẫn Chờ duyệt.'], 303)
S6.add('Phiếu kiểm kê hoàn thành sau hạch toán', 'P1', [ACC_K, 'TPE.KKK-01095 chỉ còn phần thiếu của phiếu 00091.'],
       ['Lưu và duyệt phiếu xuất hàng từ 00091.', KK_MENU, 'Xem TPE.KKK-01095.'], '—',
       ['Phiếu kiểm kê chuyển "Hoàn thành" (hoặc giữ "Đang xử lý" nếu còn việc).'], 307)
S6.add('Quay lại ở màn phiếu xuất hàng không đổi trạng thái', 'P0', PRE_K,
       ['Đăng nhập K.', 'Mở Tạo phiếu xuất hàng từ 00091.', 'Nhập thông tin, bấm Quay lại, chọn Thoát.'], '—',
       ['Không tạo phiếu xuất hàng; 00091 vẫn Chờ duyệt.'], 310)
S6.add('Không lập lại khi đã hạch toán', 'P1', [ACC_K, P90], ['Đăng nhập K.', MENU, 'Quan sát dòng 00090.'], '—',
       ['Không có nút Tạo phiếu xuất hàng.'], 311)
S6.add('Lịch sử ghi người duyệt và mã phiếu xuất hàng', 'P0', [PRE_LIST, P90], [MENU, 'Mở lịch sử 00090.'], '—',
       ['Mốc "Thay đổi trạng thái" 02/11/2026 11:16 Chờ duyệt sang Đang hạch toán và 11:17 Đang hạch toán sang Đã hạch toán, '
        'người thực hiện DNS Admin, ghi chú "Phiếu xuất hàng điều chỉnh kiểm kê PXHĐCKK-00073.".'], 312)
S6.add('Không phải Kế toán kho không thấy nút', 'P0', [ACC_Q1, P91], ['Đăng nhập Q1.', MENU], '—',
       ['Dòng 00091 không có nút Tạo phiếu xuất hàng.'], [300, 295])

# ============================================================== VII. LỊCH SỬ THAY ĐỔI
S7 = Sec(7)
S7.add('Mở cửa sổ lịch sử từ danh sách', 'P0', [PRE_LIST, P90], [MENU, 'Ở dòng 00090 bấm Lịch sử.'], '—',
       ['Mở cửa sổ "Lịch sử thay đổi: PXKĐCKK-00090", nút Bộ lọc, nút Đóng.'], 162)
S7.add('Thông tin mỗi mốc', 'P0', [PRE_LIST, P90], [MENU, 'Mở lịch sử 00090.'], '—',
       ['Mỗi mốc: thời gian dd/mm/yyyy hh:mm, hành động, "Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ".',
        'Mốc trạng thái ghi "Trạng thái: Đang hạch toán sang Đã hạch toán" và ghi chú mã phiếu xuất hàng.'], [163, 165, 166, 167, 168])
S7.add('Mới nhất ở trên', 'P1', [PRE_LIST, P90], [MENU, 'Mở lịch sử 00090.'], '—',
       ['Thứ tự: 02/11 11:17, 02/11 11:16, 30/10 22:58 (Tạo mới).'], 164)
S7.add('Phiếu lập ở hệ thống cũ chưa có lịch sử', 'P2', [PRE_LIST, 'PXKĐCKK-00082 (SG_KHO - Nguyễn Thu Hòa) chưa có mốc ghi.'],
       [MENU, 'Mở lịch sử 00082.'], '—', ['Cửa sổ báo chưa có lịch sử, không lỗi.'], 173)
S7.add('Lọc theo loại hành động', 'P1', [PRE_LIST, P90],
       [MENU, 'Mở lịch sử 00090.', 'Bấm Bộ lọc, chọn Loại hành động = Tạo mới.', 'Đổi thành Thay đổi thông tin.'], '—',
       ['Bước 3: còn mốc Tạo mới.', 'Bước 4: "Không có lịch sử phù hợp bộ lọc.".',
        'Ô có: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.'], [169, 173, 175])
S7.add('Lọc theo người thực hiện', 'P2', [PRE_LIST, P90], [MENU, 'Mở lịch sử, Bộ lọc, chọn Người thực hiện = DNS Admin.'], '—',
       ['Còn đủ 3 mốc.'], 170)
S7.add('Lọc theo thời gian', 'P2', [PRE_LIST, P90], [MENU, 'Mở lịch sử, Bộ lọc, Từ ngày = Đến ngày = 02/11/2026.'], '—',
       ['Còn 2 mốc ngày 02/11.'], 171)
S7.add('Kết hợp lọc và Làm mới', 'P2', [PRE_LIST, P90],
       [MENU, 'Mở lịch sử, lọc Loại = Thay đổi trạng thái và Từ ngày 02/11/2026.', 'Bấm Làm mới.'], '—',
       ['Bước 2: 2 mốc trạng thái.', 'Bước 3: hiện lại đủ 3 mốc.'], [172, 174])
S7.add('Lịch sử tạo bằng Gửi duyệt từ màn Tạo', 'P1', PRE_FORM, CHON + ['Gửi duyệt (đủ dữ liệu).', 'Mở lịch sử phiếu mới.'], '—',
       ['Có 1 mốc "Tạo mới".'], 176)
S7.add('Đóng cửa sổ', 'P1', [PRE_LIST, P90], [MENU, 'Sang trang 2, lọc Trạng thái.', 'Mở lịch sử 1 dòng, bấm Đóng.',
       'Mở lại, bấm (x).'], '—', ['Cửa sổ đóng; danh sách giữ trang, bộ lọc.'], [184, 185])
S7.add('Xem / in không ghi lịch sử', 'P2', [PRE_LIST, P90], [MENU, 'Mở chi tiết 00090, bấm In, đóng.', 'Mở lịch sử.'], '—',
       ['Không có mốc mới.'], 182)

# ============================================================== VIII. XEM CHI TIẾT
S8 = Sec(8)
S8.add('Mở màn chi tiết', 'P0', [PRE_LIST, P90], [MENU, 'Bấm PXKĐCKK-00090.'], '—',
       ['Mở TRANG chi tiết, tab "Chi tiết phiếu xuất kho điều chỉnh kiểm kê: PXKĐCKK-00090".'], 186)
S8.add('Tiêu đề kèm trạng thái', 'P1', [PRE_LIST, P90], [MENU, 'Bấm PXKĐCKK-00090.'], '—',
       ['Tiêu đề trang có nhãn xanh lá "Đã hạch toán".'], 187)
S8.add('Đầy đủ trường', 'P0', [PRE_LIST, P90], [MENU, 'Bấm PXKĐCKK-00090.'], '—',
       ['Thông tin chung: Phiếu kiểm kê TPE.KKK-01087 (liên kết), Kho LN - Liên Ninh, Ghi chú "test", Người duyệt DNS Admin, '
        'Ngày duyệt 02/11/2026 11:17.', 'Khối File đính kèm có 1 file pdf.',
        'Bảng Chi tiết: MẶT NẠ BẢO VỆ, H8A/PW96, 3M-H8APW96, Cái, LN-N1-D10-K3-T2, lô, SL 4, Đơn giá 1,150,000, Thành tiền 4,600,000.'],
       [188, 189])
S8.add('Khớp dữ liệu danh sách', 'P1', [PRE_LIST, P90], [MENU, 'So dòng 00090 và màn chi tiết.'], '—',
       ['Kho, Người duyệt, Ngày duyệt, Trạng thái trùng khớp.'], 190)
S8.add('Chế độ chỉ đọc', 'P0', [PRE_LIST, P90], [MENU, 'Bấm PXKĐCKK-00090.'], '—',
       ['Mọi ô khóa; không có Lưu nháp / Gửi duyệt.', 'Chân màn: In, Quay lại (Tạo phiếu xuất hàng / Sửa chỉ khi đủ điều kiện).'],
       [191, 192])
S8.add('Phiếu Chờ duyệt / Đang tạo', 'P1', [PRE_LIST, P91], [MENU, 'Bấm PXKĐCKK-00091.'], '—',
       ['Không có ô Người duyệt / Ngày duyệt; nhãn vàng Chờ duyệt.'], [193, 194])
S8.add('Khu vực lịch sử', 'P1', [PRE_LIST, P90], [MENU, 'Bấm 00090.', 'Bấm Xem lịch sử.'], '—',
       ['Khối Lịch sử mở rộng, có 3 mốc như cửa sổ lịch sử.'], 195)
S8.add('Quay lại giữ trang và bộ lọc', 'P1', [PRE_LIST, 'Đang lọc Kho = LN - Liên Ninh.'], ['Bấm 00090.', 'Bấm Quay lại.'], '—',
       ['Về danh sách, vẫn lọc Kho LN.'], [196, 197])
S8.add('Liên kết phiếu kiểm kê', 'P2', [PRE_LIST, P90], ['Bấm 00090.', 'Bấm TPE.KKK-01087.'], '—',
       ['Mở chi tiết phiếu kiểm kê ở tab mới.'], 188)
S8.add('Phiếu không tồn tại', 'P1', PRE_LIST, ['Mở đường link chi tiết với số phiếu không tồn tại.'], '—',
       ['Chuyển sang trang không tìm thấy, không báo lỗi nổi.'], 196)

# ============================================================== IX. IN PHIẾU
S9 = Sec(9)
S9.add('In phiếu từ danh sách', 'P0', [PRE_LIST, P91], [MENU, 'Ở dòng 00091 bấm In.'], '—',
       ['Cửa sổ "Xem trước phiếu xuất kho điều chỉnh kiểm kê PXKĐCKK-00091".',
        'Bản in: "PHIẾU XUẤT KHO ĐIỀU CHỈNH KIỂM KÊ", Số phiếu, Ngày lập 05/11/2026, Phiếu kiểm kê TPE.KKK-01095, Kho LN - Liên Ninh, '
        'Ghi chú g; bảng STT, Tên hàng, Model, Mã hàng, ĐVT, Vị trí, Lô, SL xuất; Người lập DNS Admin.'], 6)
S9.add('In phiếu từ màn chi tiết', 'P1', [PRE_LIST, P91], [MENU, 'Bấm 00091.', 'Bấm In.'], '—', ['Cùng bản xem trước.'], 6)
S9.add('Letterhead theo công ty của phiếu', 'P1', [ACC_Q1, 'PXKĐCKK-00082 thuộc công ty TPSG; Q1 thuộc công ty TPE.'],
       ['Đăng nhập Q1.', MENU, 'In 00082.'], '—', ['Đầu bản in là logo / letterhead công ty TPSG.'], 6)
S9.add('Bấm In trong cửa sổ', 'P1', [PRE_LIST, P91], ['Mở xem trước 00091.', 'Bấm In.'], '—', ['Mở hộp thoại in của trình duyệt.'], 6)
S9.add('In danh sách: theo bộ lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = LN - Liên Ninh.', 'Bấm In danh sách.'], '—',
       ['Cửa sổ "Xem trước danh sách phiếu xuất kho điều chỉnh kiểm kê", tiêu đề "DANH SÁCH PHIẾU XUẤT KHO ĐIỀU CHỈNH KIỂM KÊ".',
        'Đúng 6 dòng; cột STT, Số phiếu, Phiếu kiểm kê, Kho, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái.'], [219, 220])
S9.add('In danh sách: không có dữ liệu', 'P2', PRE_LIST, [MENU, 'Tìm "ZZZ", bấm In danh sách.'], '—', ['Cửa sổ báo "Không có dữ liệu để in".'], 222)
S9.add('In danh sách: vượt 2.000 dòng', 'P2', 'Phạm vi xem có 2.500 phiếu.', [MENU, 'Bấm In danh sách.'], '—',
       ['Không có bản in, ẩn nút In; hiện "Danh sách có 2,500 dòng, vượt mức in tối đa 2,000 dòng nên chưa in được…".'], 221)
S9.add('Đóng cửa sổ xem trước', 'P2', [PRE_LIST, P91], ['Mở xem trước 00091.', 'Bấm (x).'], '—',
       ['Cửa sổ đóng, danh sách giữ nguyên.'], 185)

# ============================================================== X. TÙY CHỈNH CỘT
S10 = Sec(10)
S10.add('Mở cửa sổ Tùy chỉnh cột', 'P0', PRE_LIST, [MENU, 'Bấm nút biểu tượng cột.'], '—',
        ['Cửa sổ "Tuỳ chỉnh cột", dòng hướng dẫn, 11 cột, "Đang chọn 11/11 cột", nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng.'], [198, 199])
S10.add('Cột chọn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa lưu cấu hình.'], ['Mở Tuỳ chỉnh cột.'], '—', ['Cả 11 cột được tích.'], 200)
S10.add('Ẩn cột', 'P0', PRE_LIST, ['Mở Tuỳ chỉnh cột, bỏ tích Ngày kiểm kê, bấm Lưu.'], '—',
        ['Báo "Cập nhật thành công"; bảng không còn cột Ngày kiểm kê.'], [202, 206])
S10.add('Hiện lại cột ẩn', 'P1', 'Đang ẩn cột Ngày kiểm kê.', ['Mở Tuỳ chỉnh cột, tích Ngày kiểm kê, Lưu.'], '—',
        ['Cột hiện lại đúng vị trí.'], 201)
S10.add('Cột khóa không ẩn được', 'P0', PRE_LIST, ['Mở Tuỳ chỉnh cột.'], '—',
        ['STT, Số phiếu, Hành động có biểu tượng ổ khóa, không bỏ tích / kéo được.'], [203, 205])
S10.add('Kéo đổi thứ tự cột', 'P1', PRE_LIST, ['Kéo cột Kho lên sau Số phiếu, Lưu.'], '—', ['Bảng hiện Kho ngay sau Số phiếu.'], 204)
S10.add('Đóng không lưu', 'P1', PRE_LIST, ['Bỏ tích Kho, bấm Đóng.'], '—', ['Bảng vẫn có cột Kho.'], 207)
S10.add('Ghi nhớ sau F5', 'P1', 'Đã ẩn cột Ngày kiểm kê và Lưu.', ['Nhấn F5.'], '—', ['Cột Ngày kiểm kê vẫn ẩn.'], 208)
S10.add('Cấu hình theo tài khoản', 'P2', 'Tài khoản A đã ẩn cột Kho.', ['Đăng nhập B, mở màn.'], '—', ['B vẫn thấy cột Kho.'], 209)
S10.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', 'Đang lọc Kho = LN.', ['Ẩn cột Người duyệt, Lưu.'], '—',
        ['Vẫn 6 phiếu, bộ lọc giữ nguyên.'], [210, 211])

# ============================================================== XI. XUẤT DANH SÁCH EXCEL
S11 = Sec(11)
S11.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel.'], '—',
        ['Cửa sổ "Chọn trường xuất Excel": 9 trường Số phiếu, Phiếu kiểm kê, Ngày kiểm kê, Kho, Người tạo, Ngày tạo, Người duyệt, '
         'Ngày duyệt, Trạng thái; "Đang chọn 9/9 trường".'], [212, 213])
S11.add('Trường chọn mặc định theo cột đang hiện', 'P1', 'Đang ẩn cột Ngày kiểm kê.', ['Bấm Xuất Excel.'], '—',
        ['Ngày kiểm kê không được tích sẵn.'], [214, 215])
S11.add('Xuất tất cả trường', 'P0', PRE_LIST, ['Bấm Xuất Excel, Chọn tất cả, Xuất file.'], '—',
        ['Tải "danh_sach_phieu_xuat_kho_dieu_chinh_kiem_ke.xlsx", báo "Xuất Excel thành công".', 'Đủ 76 dòng, cột STT + 9 cột.'],
        [216, 223, 227])
S11.add('Xuất một số trường', 'P1', PRE_LIST, ['Bỏ chọn hết, tích Số phiếu, Trạng thái, Xuất file.'], '—',
        ['File chỉ có STT, Số phiếu, Trạng thái.'], 217)
S11.add('Không chọn trường', 'P1', PRE_LIST, ['Bấm Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S11.add('Xuất theo tìm kiếm', 'P1', PRE_LIST, ['Tìm "0009".', 'Xuất file.'], '—', ['File có 2 dòng 00090, 00091.'], 219)
S11.add('Xuất theo bộ lọc', 'P0', PRE_LIST, [ADV, 'Chọn Trạng thái = Chờ duyệt.', 'Xuất file.'], '—', ['File có đúng 2 dòng.'], 220)
S11.add('Xuất nhiều trang', 'P1', PRE_LIST, ['Đang ở trang 1 (10 dòng/trang), Xuất file.'], '—',
        ['File đủ 76 dòng, không chỉ trang đang xem; hiện tiến độ "Đã tải x/y dòng…".'], 221)
S11.add('Danh sách rỗng', 'P1', PRE_LIST, ['Tìm "ZZZ".', 'Xuất file.'], '—', ['Báo "Không có dữ liệu để xuất", không tạo file.'], 222)
S11.add('Cấu trúc file', 'P0', PRE_LIST, ['Xuất tất cả trường.', 'Mở file.'], '—',
        ['Đầu file có letterhead công ty người xuất và "DANH SÁCH PHIẾU XUẤT KHO ĐIỀU CHỈNH KIỂM KÊ"; trang tính "Xuat dieu chinh kiem ke".',
         'Dòng tên cột đúng tên trường; cuối file khối ký "Người lập".'], [224, 225])
S11.add('Thứ tự cột theo kéo thả', 'P1', PRE_LIST, ['Kéo Trạng thái lên đầu, Xuất file.'], '—', ['Cột sau STT là Trạng thái.'], 226)
S11.add('Dữ liệu khớp và định dạng', 'P0', [PRE_LIST, P90], ['Xuất tất cả, tìm dòng 00090.'], '—',
        ['Ngày tạo "30/10/2026 22:58", Ngày duyệt "02/11/2026 11:17", Trạng thái "Đã hạch toán".',
         'Tiếng Việt có dấu hiển thị đúng (Kho "LN - Liên Ninh").'], [228, 229, 230])

# ============================================================== XII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S12 = Sec(12)
S12.add('Phiếu kiểm kê chuyển Đang xử lý khi lập phiếu', 'P0', PRE_FORM, CHON + ['Bấm Lưu nháp.', KK_MENU, 'Xem TPE.KKK-01096.'], '—',
        ['TPE.KKK-01096 chuyển "Đang xử lý"; lịch sử phiếu kiểm kê có mốc kèm "Phiếu xuất kho điều chỉnh kiểm kê <mã>.".'], [281, 274])
S12.add('Nút Tạo phiếu xuất kho điều chuyển biến mất sau khi lập', 'P0', [PRE_FORM, 'Đã lưu phiếu từ TPE.KKK-01096.'],
        [KK_MENU, 'Mở chi tiết TPE.KKK-01096.'], '—', ['Không còn nút "Tạo phiếu xuất kho điều chuyển".'], [274, 282])
S12.add('Dòng xuất ở Thẻ kho', 'P0', [PRE_LIST, P91], ['Vào Thẻ kho, lọc 3M-035653, kho LN - Liên Ninh.'], '—',
        ['Có dòng xuất SL 1 số chứng từ PXKĐCKK-00091; bấm số chứng từ mở chi tiết phiếu.'], [274, 279])
S12.add('Báo cáo tồn giảm sau Gửi duyệt', 'P1', [PRE_FORM, 'Ghi nhận tồn hàng dòng 1 tại kho HP trước khi gửi.'],
        CHON + ['Gửi duyệt (đủ dữ liệu).', 'Mở Báo cáo tồn kho theo vị trí và Tổng hợp xuất nhập tồn.'], '—',
        ['Tồn tại vị trí giảm đúng SL xuất; số xuất trong kỳ tăng tương ứng.'], 307)
S12.add('Lưu nháp không trừ tồn', 'P0', PRE_FORM, CHON + ['Bấm Lưu nháp.', 'Mở Thẻ kho hàng dòng 1.'], '—',
        ['Không có dòng xuất mới; tồn không đổi.'], 307)
S12.add('Phiếu xuất hàng điều chỉnh kiểm kê thấy phiếu Chờ duyệt', 'P0', [ACC_K, P91], ['Đăng nhập K.', PX_MENU, 'Bấm Tạo mới, mở ô Phiếu xuất kho.'],
        '—', ['Có PXKĐCKK-00091 (Chờ duyệt).'], 274)
S12.add('Cấp con đúng cấp cha', 'P1', [PRE_LIST, P91], [MENU, 'Mở 00091.'], '—',
        ['Dòng hàng thuộc đúng phiếu kiểm kê TPE.KKK-01095, kho LN; không có dòng của kho khác.'], [283, 286])
S12.add('Tham chiếu giữ khi đổi trạng thái', 'P1', [PRE_LIST, P90], [MENU, 'Mở 00090 (Đã hạch toán).'], '—',
        ['Liên kết phiếu kiểm kê, dòng hàng, file vẫn đủ.'], 284)
S12.add('Tên hàng lưu cố định lúc lập', 'P2', [PRE_LIST, P91], ['Đổi tên hàng 3M-035653 ở danh mục.', 'Mở 00091.'], '—',
        ['Phiếu vẫn hiện tên cũ "Đèn soi màu sơn 3000 lumens".'], [272, 278])
S12.add('Không xóa được vị trí / kho đã dùng', 'P1', [PRE_LIST, P91], ['Vào phân hệ Kho > menu "Danh mục" > "Vị trí", xóa vị trí "XỬ LÝ C/TỪ".'],
        '—', ['Hệ thống chặn xóa vì vị trí đã có trên phiếu.'], 270)
S12.add('Phiếu kiểm kê hết hàng thiếu không lập được', 'P1', [ACC_L, 'TPE.KKK-01098 Hoàn thành.'], TAO + ['Mở ô Phiếu kiểm kê.'], '—',
        ['Không có TPE.KKK-01098.'], 268)

# ============================================================== XIII. PHÂN QUYỀN (cuối)
S13 = Sec(13)
S13.add('Quyền Xem theo tổng công ty', 'P0', ACC_Q1, ['Đăng nhập Q1.', MENU, ADV], '—',
        ['Thấy đủ phiếu của mọi công ty (trừ phiếu Đang tạo của người khác).', 'Có ô lọc Công ty và Phòng ban.'], [287, 299])
S13.add('Quyền Xem theo công ty', 'P0', [ACC_Q2, 'PXKĐCKK-00082 thuộc TPSG; PXKĐCKK-00091 thuộc TPE.'],
        ['Đăng nhập Q2.', MENU, ADV], '—', ['Thấy 00082, KHÔNG thấy 00091.', 'Có ô Phòng ban, không có ô Công ty.'], [287, 299])
S13.add('Không có quyền nào', 'P0', ACC_N, ['Đăng nhập N.', MENU], '—',
        ['Menu vẫn hiện, mở được màn.', 'Chỉ thấy PXKĐCKK-00093 do N tạo.'], [287, 295, 299])
S13.add('Kế toán kho thấy phiếu Chờ duyệt', 'P0', ACC_K, ['Đăng nhập K.', MENU], '—',
        ['Thấy thêm mọi phiếu Chờ duyệt (00091, 00083) dù không có quyền xem theo cấp.'], [287, 299])
S13.add('Quyền Xử lý phiếu kiểm kê để lập phiếu', 'P0', PRE_FORM, ['Đăng nhập L.'] + CHON + ['Bấm Lưu nháp.'], '—',
        ['L lập được phiếu và thấy phiếu đó trong danh sách.'], 289)
S13.add('Xem chi tiết trong phạm vi', 'P0', [ACC_Q2], ['Đăng nhập Q2.', MENU, 'Mở 00082.'], '—', ['Xem được đầy đủ.'], 288)
S13.add('URL chi tiết ngoài phạm vi', 'P0', [ACC_N, 'N có đường link chi tiết 00090.'], ['Đăng nhập N, mở đường link.'], '—',
        ['Chuyển sang trang không tìm thấy; không lộ dữ liệu.'], [288, 296])
S13.add('Sửa chỉ dành cho người tạo', 'P0', [ACC_Q1, DRAFT], ['Đăng nhập Q1.', 'Mở đường link màn Sửa của 00092.'], '—',
        ['Chuyển sang trang không tìm thấy (phiếu Đang tạo của người khác nằm ngoài phạm vi).'], [290, 296])
S13.add('Ẩn nút khi thiếu quyền', 'P0', [ACC_N, P91], ['Đăng nhập N.', MENU], '—',
        ['Không có nút Tạo phiếu xuất hàng, Sửa ở các dòng không đủ điều kiện.'], 295)
S13.add('Xuất Excel / In danh sách theo quyền', 'P1', ACC_Q2, ['Đăng nhập Q2.', 'Xuất Excel, Xuất file.'], '—',
        ['File chỉ có phiếu của công ty TPSG.'], 293)
S13.add('Xem lịch sử theo quyền', 'P1', [ACC_Q1, P90], ['Đăng nhập Q1.', 'Mở lịch sử 00090.'], '—', ['Xem được 3 mốc.'], 294)
S13.add('Bị gỡ quyền giữa lúc thao tác', 'P1', [ACC_Q1, 'Quản trị gỡ quyền theo tổng công ty của Q1 khi đang ở danh sách.'],
        ['Bấm sang trang 2.'], '—', ['Danh sách chỉ còn phiếu Q1 tự tạo (phạm vi kiểm lại ở mỗi lần nạp).'], [297, 298])
S13.add('Super admin xem mọi phiếu', 'P2', 'Tài khoản DNS Admin (Super admin).', ['Đăng nhập DNS Admin.', MENU, ADV], '—',
        ['Thấy đủ 76 phiếu, có ô Công ty, Phòng ban.'], 287)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'CHỈNH SỬA', S4),
    ('V', 'GỬI DUYỆT', S5),
    ('VI', 'DUYỆT PHIẾU (TẠO PHIẾU XUẤT HÀNG)', S6),
    ('VII', 'LỊCH SỬ THAY ĐỔI', S7),
    ('VIII', 'XEM CHI TIẾT PHIẾU XUẤT KHO ĐIỀU CHỈNH KIỂM KÊ', S8),
    ('IX', 'IN PHIẾU', S9),
    ('X', 'TÙY CHỈNH CỘT', S10),
    ('XI', 'XUẤT DANH SÁCH EXCEL', S11),
    ('XII', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S12),
    ('XIII', 'PHÂN QUYỀN', S13),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
check_no_dash_pre(SECTIONS, [])
_ids = ['TC_%02d.%s' % (s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
assert len(_ids) == len(set(_ids)), 'Trùng TC ID'

if __name__ == '__main__':
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='Phiếu xuất kho điều chỉnh kiểm kê - Cập nhật ngày 09/11/2026',
                module_name='Phiếu xuất kho điều chỉnh kiểm kê', description_block=DESCRIPTION_BLOCK, sections=SECTIONS,
                loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

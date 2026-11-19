# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu xuất hàng điều chỉnh kiểm kê" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan,
loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (xác định từ code 18/11/2026): chứng từ có trạng thái (Đang tạo / Đã hạch toán), có Tạo mới (Lưu, Lưu và tiếp tục),
Sửa (Đang tạo + người tạo), Lưu và duyệt (= bước duyệt, trừ tồn kho kế toán + tính đơn giá vốn, KHÔNG bút toán), In phiếu / In danh
sách, Lịch sử. KHÔNG có Xóa (hệ thống cũ đã bỏ — routes chỉ có GET/POST/PUT, không DELETE phiếu), Khóa, Gửi duyệt, Không duyệt, Hủy,
Import (kiểm code: không route / nút) nên bỏ các nhóm đó.
Nhóm: I Hiển thị · II Tìm kiếm & lọc (gồm Cài đặt bộ lọc) · III Thêm mới · IV Chỉnh sửa · V Duyệt phiếu (Lưu và duyệt) ·
VI Lịch sử · VII Xem chi tiết · VIII In phiếu (gồm In danh sách) · IX Tùy chỉnh cột · X Xuất danh sách Excel · XI Ràng buộc ·
XII Phân quyền (cuối). Mỗi case ghi stt checklist nó phủ (ck) — gen_checklist.py đọc CK.
Khuôn: ../phieu-nhap-hang-dieu-chinh-kiem-ke/gen_testcase.py (màn đối xứng).
Nguồn hành vi (đọc 18/11/2026, nhánh develop cả 2 repo): FE pages/finance/inventory-exports/**; BE InventoryExport (Entity /
Controller / Service / WriteService — validate rẽ nháp #11970), AccountingStockWriter::export, WarehouseInventoryExport::
canCreateProductExport, SelfInventory::handleCompleted; quyền Catalog warehouse.phieu_xuat_hang_dieu_chinh_kiem_ke.view (mức Công ty /
Tổng công ty) + accounting.ke_toan_kho.manage.
Số liệu mẫu: dev-hrm 18/11/2026 (DNS Admin — quyền Xem mức Tổng công ty + Kế toán kho): 74 phiếu (72 Đã hạch toán, 2 Đang tạo
PXHĐCKK-00074, 00072); phiếu xuất kho PXKĐCKK-00091, 00083 đang Chờ duyệt.
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
MENU = ('Vào phân hệ Tài chính > nhóm "Hàng hoá - Dịch vụ - Vận chuyển" > menu "Xuất hàng" > bấm "Phiếu xuất hàng điều chỉnh '
        'kiểm kê".')
WIE_MENU = 'Vào phân hệ Kho > menu "Xuất kho" > bấm "Phiếu xuất kho điều chỉnh kiểm kê".'
KK_MENU = 'Vào phân hệ Kho > menu "Kiểm kho" > "Theo vị trí" > bấm "Kiểm kê theo hàng hóa".'
ADV = 'Bấm Tìm kiếm nâng cao.'
REQ = '"Bắt buộc phải nhập"'
INC = '"Bạn chưa nhập đầy đủ thông tin."'
MIS = '"Số lượng xuất kho kế toán không khớp!"'
OVER = '"Số lượng xuất không được vượt quá số lượng được xuất!"'
OVER_BE = '"Kho LN01 - Liên Ninh - Hàng bán: Số lượng xuất không được vượt quá số lượng được xuất!"'

PRE_LIST = ('Tài khoản DNS Admin (quyền Xem mức Tổng công ty + Kế toán kho); hệ thống có 74 phiếu: 72 Đã hạch toán, 2 Đang tạo '
            '(PXHĐCKK-00074, PXHĐCKK-00072 do DNS Admin tạo).')
P73 = ('Phiếu PXHĐCKK-00073: Phiếu xuất kho PXKĐCKK-00090, Phiếu kiểm kê TPE.KKK-01087, Kho "LN - Liên Ninh", Thủ kho "DNS01 - DNS '
       'Admin", Nhân viên "DNS01 - DNS Admin", Ghi chú trống, Đã hạch toán, Ngày tạo 02/11/2026 11:16; 1 dòng "MẶT NẠ BẢO VỆ" (Model '
       'H8A/PW96, Mã 3M-H8APW96, ĐVT Cái, SL xuất 4, Đơn giá 12,323, Thành tiền 49,292, Đơn giá vốn 980,000, Thành tiền vốn '
       '3,920,000, Kho kế toán "LN01 - Liên Ninh - Hàng bán" số lượng 4); lịch sử 3 mốc: Tạo mới, Thay đổi thông tin, Thay đổi '
       'trạng thái (02/11/2026).')
P74 = ('Phiếu PXHĐCKK-00074 (DNS Admin tạo 02/11/2026 16:21, Đang tạo): Phiếu xuất kho PXKĐCKK-00084, Phiếu kiểm kê TPE.KKK-01067, '
       'Kho "SG - Kho Sài Gòn", Nhân viên trống, 1 file pdf; dòng đầu "Bộ gạt mưa UP PARTS cho xe Mazda CX5" (Mã DG-802W-B79CX5, ĐVT '
       'Bộ, SL xuất 1, Đơn giá 150,000), các dòng chưa phân bổ kho kế toán; lịch sử: Tạo mới + 2 mốc Thay đổi thông tin.')
ACC_K = ('Tài khoản K: có quyền "Kế toán kho", không có quyền Xem phiếu xuất hàng điều chỉnh kiểm kê, làm việc ở công ty TPE '
         '(cùng công ty kho LN).')
SRC = ('Phiếu xuất kho PXKĐCKK-00091 (Kho "LN - Liên Ninh", Thủ kho "DNS01 - DNS Admin", Phiếu kiểm kê TPE.KKK-01095) đang Chờ '
       'duyệt, 1 dòng "Đèn soi màu sơn 3000 lumens" (Model MULTIMATCH3, Mã 3M-035653, ĐVT Bộ) SL xuất 1, đơn giá bán 1; kho LN có 2 '
       'kho kế toán: "LN01 - Liên Ninh - Hàng bán" (tồn kế toán của hàng = 2), "LN02 - Liên Ninh - Hàng khuyến mại" (tồn = 0).')
PRE_FORM = ACC_K + '\n' + SRC
TAO = [MENU, 'Bấm "Tạo mới".']
CHON = TAO + ['Chọn Phiếu xuất kho = PXKĐCKK-00091.']
DU = CHON + ['Chọn Nhân viên = "DNS01 - DNS Admin".', 'Chọn Kho kế toán dòng 1 = LN01 - Liên Ninh - Hàng bán (Số lượng tự điền 1).']
DRAFT = ('Phiếu PXHĐCKK-00075 do K lập từ PXKĐCKK-00091, trạng thái Đang tạo, Nhân viên "DNS01 - DNS Admin", Ghi chú "Nháp", Kho kế '
         'toán LN01 số lượng 1, có 1 file (kế thừa từ phiếu xuất kho).')
PRE_EDIT = ACC_K + '\n' + DRAFT
SUA = [MENU, 'Ở dòng PXHĐCKK-00075 bấm Sửa (biểu tượng bút chì).']
ACC_Q1 = 'Tài khoản Q1: Vai trò cấp quyền "Xem phiếu xuất hàng điều chỉnh kiểm kê" mức Tổng công ty, không có Kế toán kho.'
ACC_Q2 = ('Tài khoản Q2: Vai trò cấp quyền "Xem phiếu xuất hàng điều chỉnh kiểm kê" mức Công ty, đang làm việc ở công ty TPSG, không '
          'có Kế toán kho.')
ACC_N = 'Tài khoản N: không có quyền nào của màn, không phải Kế toán kho; đã tự lập 1 phiếu PXHĐCKK-00076 (Đã hạch toán).'
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
     'Màn Phiếu xuất hàng điều chỉnh kiểm kê (mã PXHĐCKK-NNNNN) dùng để Kế toán kho hạch toán phần hàng THIẾU phát hiện khi kiểm '
     'kê: lập từ Phiếu xuất kho điều chỉnh kiểm kê đang Chờ duyệt, xem / sửa đơn giá, chọn Nhân viên, phân bổ từng dòng vào kho kế '
     'toán trong giới hạn "SL được xuất"; Lưu để giữ Đang tạo, Lưu và duyệt để trừ tồn kho kế toán và tính đơn giá vốn (không ghi '
     'bút toán).'),
    ('2. Đối tượng được tính / hiển thị',
     '- Danh sách: phiếu trong phạm vi xem (quyền Xem mức Tổng công ty: mọi phiếu; mức Công ty: phiếu của công ty đang làm việc '
     'hoặc do mình tạo; không có quyền: phiếu mình tạo).\n'
     '- 2 trạng thái: Đang tạo (xám), Đã hạch toán (xanh lá).\n'
     '- Bảng Chi tiết: dòng hàng của phiếu xuất kho (SL xuất, Đơn giá, Thành tiền), mỗi dòng 1..n dòng kho kế toán + số lượng; màn '
     'Tạo / Sửa có thêm cột SL được xuất, màn Chi tiết có thêm Đơn giá vốn / Thành tiền vốn.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác luôn bị ẩn.\n- Phiếu ngoài phạm vi: không có trong danh sách, mở đường link ra trang không tìm '
     'thấy.\n- Ô Phiếu xuất kho chỉ liệt kê phiếu xuất kho điều chỉnh kiểm kê đang Chờ duyệt, chỉ với Kế toán kho.\n'
     '- Ô Kho kế toán không liệt kê kho kế toán đã khóa / thuộc kho vật lý hoặc công ty khác.\n'
     '- Màn không có Xóa, Khóa / Mở khóa, Gửi duyệt, Không duyệt, Hủy, Import.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo ngày tạo phiếu, lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Phiếu kiểm kê > phiếu xuất kho điều chỉnh > phiếu xuất hàng điều chỉnh > dòng hàng > dòng phân bổ kho kế toán.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Thành tiền = SL xuất × Đơn giá; Thành tiền vốn = SL xuất × Đơn giá vốn.\n'
     '- Lưu và duyệt: tổng Số lượng các kho kế toán của 1 dòng phải bằng SL xuất.\n'
     '- Mọi kiểu lưu: Số lượng mỗi kho (cộng dồn cùng hàng – cùng kho – cùng ĐVT) không vượt SL được xuất; không chọn trùng kho '
     'kế toán trong 1 dòng.\n- Mỗi lần lưu cộng SL xuất vào số đã xử lý của phiếu kiểm kê (kể cả khi sửa).'),
    ('7. Phân quyền cấp',
     '- Xem phiếu xuất hàng điều chỉnh kiểm kê mức Tổng công ty: mọi phiếu; có ô Công ty, Phòng ban.\n'
     '- Xem phiếu xuất hàng điều chỉnh kiểm kê mức Công ty: phiếu của công ty đang làm việc hoặc do mình tạo; có ô Phòng ban.\n'
     '- Kế toán kho: nút Tạo mới, ô Phiếu xuất kho có dữ liệu, nút Tạo phiếu xuất hàng ở màn Phiếu xuất kho điều chỉnh kiểm kê.\n'
     '- Sửa / Lưu và duyệt phiếu Đang tạo: chỉ người tạo. Không có đặc cách Super admin.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là khoảng số thứ tự trang đang xem, N là tổng phiếu khớp bộ lọc trong phạm vi xem.\n'
     '- SL được xuất = tồn kho kế toán còn lại của hàng ở kho kế toán đang chọn, quy theo ĐVT của dòng.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: K (Kế toán kho), Q1, Q2, N (không quyền), DNS Admin (Xem mức Tổng công ty + Kế toán kho).\n'
     '- Lưu ý: Lưu và duyệt TRỪ TỒN KHO KẾ TOÁN NGAY, không hoàn tác; chạy trên dữ liệu thử.\n'
     '- Lưu ý: Lưu (nháp) chỉ bắt buộc Phiếu xuất kho; Nhân viên, Đơn giá, Kho kế toán, Số lượng chỉ bắt buộc khi Lưu và duyệt '
     '(máy chủ báo lỗi SAU khi bấm xác nhận).\n'
     '- Lưu ý: giữ như hệ thống cũ — mỗi lần Lưu (kể cả sửa) đều cộng thêm số đã xử lý vào phiếu kiểm kê; không chặn lập nhiều '
     'phiếu cho 1 phiếu xuất kho; không ghi bút toán.\n'
     '- Màn Tạo / Sửa / Chi tiết là TRANG riêng, không phải cửa sổ nổi.'),
]

SCREEN = ListScreen(menu=MENU, title='Danh sách phiếu xuất hàng điều chỉnh kiểm kê', total=74, quick_label='số phiếu',
                    quick_sample='PXHĐCKK-00073', quick_hit='phiếu PXHĐCKK-00073',
                    filters=[('Trạng thái', 'Đã hạch toán'), ('Kho', 'LN - Liên Ninh')])

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Thanh tiêu đề và tab: "Phiếu xuất hàng điều chỉnh kiểm kê".', 'Tiêu đề bảng: "Danh sách phiếu xuất hàng điều chỉnh kiểm kê".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE_LIST, [MENU, 'Quan sát khối bộ lọc, thanh công cụ, cột Hành động.'], '—',
       ['Khối "Bộ lọc danh sách": ô tìm nhanh (gợi ý "Tìm theo số phiếu"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
        'Thanh công cụ: Tạo mới, In danh sách, Xuất Excel, nút biểu tượng cột.',
        'Cột Hành động: In, Lịch sử mọi dòng; Sửa ở dòng PXHĐCKK-00074, 00072 (Đang tạo); không có Xóa.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 9 cột: STT, Số phiếu, Phiếu xuất kho, Phiếu kiểm kê, Kho, Người tạo, Ngày tạo, Trạng thái, Hành động.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 9/9 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp phiếu', 'P0', [PRE_LIST, P73], [MENU, 'Đối chiếu dòng PXHĐCKK-00073.'], '—',
       ['Phiếu xuất kho "PXKĐCKK-00090", Phiếu kiểm kê "TPE.KKK-01087" (đều là liên kết), Kho "LN - Liên Ninh", Người tạo '
        '"HDQT - DNS Admin", Ngày tạo 02/11/2026 11:16.', 'Nhãn xanh lá "Đã hạch toán".'], 6)
S1.add('Liên kết Phiếu xuất kho / Phiếu kiểm kê mở ở tab mới', 'P1', [PRE_LIST, P73],
       [MENU, 'Ở dòng PXHĐCKK-00073 bấm "PXKĐCKK-00090".', 'Quay lại tab danh sách, bấm "TPE.KKK-01087".'], '—',
       ['Mỗi lần mở chi tiết phiếu tương ứng ở TAB MỚI.', 'Tab danh sách giữ nguyên trang, bộ lọc.'], 6)
S1.add('Trạng thái bản ghi', 'P0', PRE_LIST, [MENU, 'Quan sát cột Trạng thái của 00074 và 00073.'], '—',
       ['00074: nhãn xám "Đang tạo".', '00073: nhãn xanh lá "Đã hạch toán".'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', ['Tài khoản mới, không có quyền nào, chưa lập phiếu nào.'], ['Đăng nhập.', MENU], '—',
       ['Bảng hiện "Không có dữ liệu phù hợp.", không có dòng "Hiển thị".', 'Không báo lỗi.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'],
       'Ô tìm nhanh: ZZZ999', ['Bảng hiện "Không có dữ liệu phù hợp.".', 'Không báo lỗi.'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 20 phiếu, tự về trang 1, "Hiển thị 1–20 / 74".', 'Ô có các lựa chọn 5, 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–20 / 74".', 'Bước 3: "Hiển thị 1–10 / 74".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—',
       ['Bước 2: trang 8, "Hiển thị 71–74 / 74".', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang 8 quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2, rồi trang 8.'], '—',
       ['Trang 2: STT 11–20; trang 8: STT 71–74.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 3.', ADV, 'Chọn Trạng thái = Đã hạch toán.'],
       'Trạng thái: Đã hạch toán', ['Tự nạp lại ở trang 1; "Hiển thị 1–10 / 72".'], 17)
S1.add('Sắp xếp tăng dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Số phiếu.'], '—',
       ['PXHĐCKK-00001 ở trên cùng, tăng dần; mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Số phiếu 2 lần.'], '—',
       ['PXHĐCKK-00074 trên cùng, giảm dần; mũi tên xuống.'], 21)
S1.add('Sắp xếp theo Ngày tạo', 'P1', PRE_LIST, [MENU, 'Bấm tiêu đề Ngày tạo.', 'Bấm lần nữa.'], '—',
       ['Lần 1: cũ nhất trên (PXHĐCKK-00001, 21/10/2025 11:23).', 'Lần 2: mới nhất trên (PXHĐCKK-00074, 02/11/2026 16:21).',
        'Mặc định khi mới vào: mới nhất trên.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Phiếu xuất kho, Phiếu kiểm kê, Kho, Người tạo, Trạng thái, Hành động.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Số phiếu (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 bắt đầu từ PXHĐCKK-00011, tiếp tục thứ tự tăng.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 3.', 'Bấm tiêu đề Ngày tạo.'], '—', ['Về trang 1.'], 25)
S1.add('Bấm sắp xếp không làm vỡ bố cục bảng', 'P2', PRE_LIST, [MENU, 'Bấm tiêu đề Ngày tạo, Số phiếu nhiều lần.'], '—',
       ['Độ rộng các cột giữ nguyên, mũi tên sắp xếp không nhảy chỗ.'], 22)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo số phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "PXHĐCKK-00073", bấm Tìm kiếm.'], 'Ô tìm nhanh: PXHĐCKK-00073',
       ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần số phiếu', 'P0', PRE_LIST, [MENU, 'Nhập "0007", bấm Tìm kiếm.'], 'Ô tìm nhanh: 0007',
       ['Còn 6 phiếu PXHĐCKK-00007, 00070, 00071, 00072, 00073, 00074.'], 27)
S2.add('Ô tìm nhanh không tìm theo mã phiếu xuất kho', 'P1', PRE_LIST, [MENU, 'Nhập "PXKĐCKK-00090", bấm Tìm kiếm.'], '—',
       ['"Không có dữ liệu phù hợp." (ô tìm nhanh chỉ tìm theo số phiếu).'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "pxhđckk-00073", bấm Tìm kiếm.'], '—',
       ['Ra phiếu PXHĐCKK-00073 như khi gõ chữ hoa.'], 28)
S2.add('Có dấu / không dấu', 'P2', PRE_LIST, [MENU, 'Nhập "PXHDCKK-00073" (chữ D không gạch), bấm Tìm kiếm.'], '—',
       ['Kết quả theo cách so khớp của hệ thống: chữ Đ và D có thể không được coi là một; ghi nhận kết quả thực tế.',
        'Lưu ý: số phiếu có chữ Đ, nhập đúng "PXHĐCKK" để tìm.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; % được hiểu là ký tự đại diện nên ra cả 74 phiếu.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  PXHĐCKK-00073  ", bấm Tìm kiếm.'], '—',
       ['Ra phiếu PXHĐCKK-00073.'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "PXHĐCKK-00073", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Hiện lại đủ 74 phiếu.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST,
       [MENU, 'Nhập "PXHĐCKK-00073", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'], '—',
       ['Cả 2 cách đều ra phiếu PXHĐCKK-00073, về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['Các ô Mã phiếu, Kho, Trạng thái, Người tạo, Mã hàng hóa, Tên hàng hóa, Ngày tạo, Công ty, Phòng ban đều trống.',
        'Đủ 74 phiếu.'], 36)
S2.add('Lọc Mã phiếu', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "00074" vào ô Mã phiếu.'], '—', ['Lọc ngay khi gõ; còn PXHĐCKK-00074.'], 37)
S2.add('Lọc Kho', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = LN - Liên Ninh.'], '—',
       ['Ô Kho có 4 lựa chọn: LN - Liên Ninh, PTT - Phan Trọng Tuệ, SG - Kho Sài Gòn, SG-CSKH - Kho Sài Gòn - Chăm sóc khách hàng.',
        'Còn 5 phiếu: PXHĐCKK-00073, 00072, 00071, 00069, 00068.'], 37)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đang tạo.'], '—',
       ['Ô có 2 lựa chọn: Đang tạo, Đã hạch toán.', 'Còn 2 phiếu PXHĐCKK-00074, 00072.'], 37)
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = "SG_KT - Võ Thị Hà".'], '—',
       ['Ô liệt kê 4 người: HDQT - DNS Admin, SG_KT - Nguyễn Thị Vân, SG_KT - Võ Thị Hà, SG_KT - Vương Thị Thùy.',
        'Còn 1 phiếu PXHĐCKK-00067.'], 37)
S2.add('Lọc Mã hàng hóa', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "3M-H8APW96" vào ô Mã hàng hóa.'], '—',
       ['Còn các phiếu có ít nhất 1 dòng hàng mã chứa "3M-H8APW96" (có PXHĐCKK-00073).'], 37)
S2.add('Lọc Tên hàng hóa', 'P1', PRE_LIST, [MENU, ADV, 'Gõ "mặt nạ bảo vệ" vào ô Tên hàng hóa.'], '—',
       ['Còn các phiếu có dòng hàng tên chứa "mặt nạ bảo vệ" (có PXHĐCKK-00073), không phân biệt hoa / thường.'], 37)
S2.add('Lọc Ngày tạo lấy trọn ngày biên', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày tạo 22/10/2026 – 24/10/2026.'], '—',
       ['Còn 3 phiếu: 00070 (24/10 15:46), 00069 (23/10 10:25), 00068 (22/10 14:51).', 'Bỏ trống ngày cuối vẫn lọc được.'], 37)
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = PTT - Phan Trọng Tuệ.', 'Chọn Trạng thái = Đang tạo.'],
       '—', ['"Không có dữ liệu phù hợp." (phiếu duy nhất của kho PTT đã Đã hạch toán).',
             'Đổi Trạng thái = Đã hạch toán thì còn PXHĐCKK-00070.'], [38, 40])
S2.add('Kết hợp tìm kiếm và bộ lọc', 'P1', PRE_LIST,
       [MENU, 'Nhập "PXHĐCKK-0007", bấm Tìm kiếm.', ADV, 'Chọn Trạng thái = Đã hạch toán.'], '—',
       ['Còn 3 phiếu 00070, 00071, 00073 (00072, 00074 đang Đang tạo bị loại).'], 39)
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đã hạch toán.', 'Bấm trang cuối.'], '—',
       ['Dòng "Hiển thị" ghi tổng 72.', 'Trang 8 hiện "Hiển thị 71–72 / 72", STT liên tục.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Kho = LN - Liên Ninh (5 phiếu).', ['Bấm tiêu đề Số phiếu.'], '—',
       ['Chỉ 5 phiếu của kho LN được sắp; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "PXHĐCKK", lọc Kho, Trạng thái, sắp Số phiếu, ở trang 2.',
       ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống, bỏ sắp xếp, nạp lại trang 1, đủ 74 phiếu.'], 44)
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.raw(org_cases(SCREEN, len(S2) + 1), [[37], [37], [37]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Đã hạch toán, chưa mở màn chi tiết.'],
       ['Nhấn F5.'], '—', ['Bộ lọc trở về trống, đủ 74 phiếu (bộ lọc chỉ nhớ khi đi vào màn chi tiết / sửa của màn).'], 46)
S2.add('Ô Công ty chỉ có với quyền mức Tổng công ty', 'P1', [ACC_Q2], ['Đăng nhập Q2.', MENU, ADV], '—',
       ['Không có ô Công ty, chỉ có ô Phòng ban.'], 37)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Tên hàng hóa, bấm Lưu.'], '—',
       ['Cửa sổ liệt kê 8 mục: Mã phiếu, Kho, Trạng thái, Người tạo, Mã hàng hóa, Tên hàng hóa, Ngày tạo, Công ty – Phòng ban.',
        'Báo "Cập nhật thành công"; khối Tìm kiếm nâng cao không còn ô Tên hàng hóa.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Đang tạo.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Trạng thái, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị bỏ, nạp lại đủ 74 phiếu.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Tên hàng hóa.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Tên hàng hóa vẫn ẩn.', 'Bước 2: tích đủ 8 mục, Tên hàng hóa hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Ngày tạo lên đầu, bấm Lưu.'], '—',
       ['Ô Ngày tạo đứng đầu khối Tìm kiếm nâng cao; giữ sau khi đăng nhập lại.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo mới từ danh sách', 'P0', PRE_FORM, ['Đăng nhập K.'] + TAO, '—',
       ['Mở TRANG "Tạo phiếu xuất hàng điều chỉnh kiểm kê", tab cùng tiêu đề.'], 49)
S3.add('Mở từ phiếu xuất kho điều chỉnh kiểm kê', 'P0', PRE_FORM,
       ['Đăng nhập K.', WIE_MENU, 'Ở dòng PXKĐCKK-00091 bấm "Tạo phiếu xuất hàng".'], '—',
       ['Mở màn Tạo với Phiếu xuất kho = PXKĐCKK-00091 chọn sẵn, đã điền Phiếu kiểm kê, Kho, Thủ kho, bảng Chi tiết đã nạp.',
        'Từ màn chi tiết PXKĐCKK-00091 bấm "Tạo phiếu xuất hàng" cũng mở như vậy.'], [49, 53])
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải "<tên K> - <ngày giờ hiện tại>".', 'Không có ô Số phiếu (mã tự sinh khi lưu).'], 50)
S3.add('Các trường, khối và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Phiếu xuất kho, Phiếu kiểm kê, Kho, Thủ kho, Nhân viên, Ghi chú (2 dòng, gợi ý "Nhập ghi chú").',
        'Khối "File đính kèm" có nút "Thêm tài liệu"; khối "Chi tiết": STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, SL xuất, Đơn giá, '
        'Thành tiền, Kho kế toán, Số lượng, SL được xuất.', 'Chân màn: Lưu, Lưu và tiếp tục, Lưu và duyệt, Quay lại.'], [51, 54])
S3.add('Trường bắt buộc / không bắt buộc', 'P0', PRE_FORM, TAO + ['Quan sát dấu *.'], '—',
       ['Phiếu xuất kho, Nhân viên có dấu *; tiêu đề cột Đơn giá, Kho kế toán, Số lượng có dấu *.',
        'Ghi chú và File đính kèm không có dấu * ở màn Tạo.', 'Phiếu kiểm kê, Kho, Thủ kho chỉ đọc.'], 52)
S3.add('Giá trị mặc định', 'P0', PRE_FORM, TAO, '—',
       ['Ô Phiếu xuất kho trống (gợi ý "Chọn phiếu xuất kho"); Nhân viên trống (gợi ý "Chọn nhân viên"); Ghi chú trống.',
        'Bảng ghi "Chọn phiếu xuất kho để nạp hàng hóa".'], 53)
S3.add('Danh sách ô Phiếu xuất kho', 'P0', PRE_FORM, TAO + ['Mở ô Phiếu xuất kho.'], '—',
       ['Chỉ liệt kê phiếu xuất kho điều chỉnh kiểm kê đang Chờ duyệt, mới nhất trên: PXKĐCKK-00091, PXKĐCKK-00083.',
        'Không có PXKĐCKK-00084 (Đang hạch toán) và các phiếu Đã hạch toán.'], [51, 53])
S3.add('Chọn phiếu xuất kho thì nạp thông tin và dòng hàng', 'P0', PRE_FORM, CHON, '—',
       ['Điền Phiếu kiểm kê "TPE.KKK-01095" (liên kết), Kho "LN - Liên Ninh", Thủ kho "DNS01 - DNS Admin".',
        'Bảng 1 dòng "Đèn soi màu sơn 3000 lumens" SL xuất 1, Đơn giá 1 (đơn giá bán của phiếu xuất kho), Thành tiền 1; ô Kho kế '
        'toán trống, ô Số lượng trống, cột SL được xuất trống.'], [53, 269])
S3.add('Ô Kho kế toán chỉ có kho của kho vật lý và công ty', 'P1', PRE_FORM, CHON + ['Mở ô Kho kế toán dòng 1.'], '—',
       ['Chỉ có "LN01 - Liên Ninh - Hàng bán", "LN02 - Liên Ninh - Hàng khuyến mại".',
        'Đó là các kho kế toán đang hoạt động của kho LN, cùng công ty của phiếu xuất kho.'], [53, 276])
S3.add('Chọn kho kế toán dòng đầu tự điền kho và số lượng', 'P1', PRE_FORM,
       CHON + ['Chọn Kho kế toán dòng 1 = LN01 - Liên Ninh - Hàng bán.'], '—',
       ['Ô Số lượng tự điền 1 (= SL xuất); cột SL được xuất hiện 2.',
        'Phiếu nhiều dòng: ô kho kế toán đầu tiên của các dòng khác cũng nhận LN01 và Số lượng = SL xuất của dòng đó.'], 53)
S3.add('Lưu với dữ liệu hợp lệ đầy đủ', 'P0', PRE_FORM, DU + ['Nhập Ghi chú, thêm file.', 'Bấm Lưu.'],
       ['Ghi chú: Xuất hàng thiếu kho LN', FILE],
       ['Báo "Lưu thành công.", về danh sách.', 'Dòng mới trên cùng mã PXHĐCKK-NNNNN kế tiếp, Phiếu xuất kho PXKĐCKK-00091, Kho LN - '
        'Liên Ninh, nhãn xám "Đang tạo".'], [55, 79, 85])
S3.add('Lưu nháp chỉ với Phiếu xuất kho', 'P0', PRE_FORM, CHON + ['Không chọn Nhân viên, Kho kế toán.', 'Bấm Lưu.'],
       'Nhân viên, Kho kế toán, Số lượng, Ghi chú, File: để trống',
       ['Lưu được, báo "Lưu thành công.", phiếu Đang tạo.', 'Chi tiết phiếu: Nhân viên trống, dòng hàng có ô kho kế toán trống.',
        'Khối File đính kèm của phiếu có sẵn file của PXKĐCKK-00091.'], [56, 57])
S3.add('Dữ liệu sau lưu', 'P0', PRE_FORM, DU + ['Sửa Đơn giá dòng 1 thành 50,000.', 'Bấm Lưu.', 'Bấm số phiếu vừa tạo.'],
       'Đơn giá dòng 1: 50,000',
       ['Màn chi tiết đúng Phiếu xuất kho PXKĐCKK-00091, Kho LN - Liên Ninh, Nhân viên DNS01 - DNS Admin.',
        'Dòng 1: Đơn giá 50,000, Thành tiền 50,000, Đơn giá vốn 0 (chưa duyệt), Kho kế toán LN01 số lượng 1.'], 58)
S3.add('Trạng thái mặc định sau lưu', 'P0', PRE_FORM, DU + ['Bấm Lưu.', WIE_MENU], '—',
       ['Phiếu ở trạng thái Đang tạo (nhãn xám), chưa trừ tồn kho kế toán.',
        'PXKĐCKK-00091 chuyển "Đang hạch toán", Người duyệt = K.'], [59, 281])
S3.add('Lịch sử tạo', 'P1', PRE_FORM, DU + ['Bấm Lưu.', 'Ở dòng phiếu mới bấm Lịch sử.'], '—',
       ['Có 1 mốc "Tạo mới", người thực hiện K.'], [60, 176])
S3.add('Lưu khi chưa chọn Phiếu xuất kho', 'P0', PRE_FORM, TAO + ['Bấm Lưu.'], '—',
       ['Ô Phiếu xuất kho viền đỏ, dưới ô ' + REQ + ' (Nhân viên không báo lỗi khi Lưu).', 'Thông báo ' + INC + '; không lưu.'],
       [61, 70, 80])
S3.add('Số lượng vượt SL được xuất bị chặn', 'P0', PRE_FORM, CHON + ['Chọn Kho kế toán dòng 1 = LN02 - Liên Ninh - Hàng khuyến mại.',
                                                                     'Bấm Lưu.'], '—',
       ['Số lượng tự điền 1, cột SL được xuất = 0.', 'Dưới ô Số lượng: ' + OVER + '; thông báo ' + INC + '; không lưu.'],
       [61, 62, 70])
S3.add('Số lượng bằng đúng SL được xuất', 'P1', [PRE_FORM, 'Tồn LN01 của hàng 3M-035653 = 1 (dữ liệu thử).'], DU + ['Bấm Lưu.'], '—',
       ['Lưu được (bằng SL được xuất là hợp lệ).'], 64)
S3.add('Bỏ trống Đơn giá khi Lưu nháp', 'P1', PRE_FORM, DU + ['Xóa Đơn giá dòng 1.', 'Bấm Lưu.'], '—',
       ['Lưu được; chi tiết phiếu ghi Đơn giá 0.'], 61)
S3.add('Chia 1 dòng vào 2 kho kế toán', 'P0', [PRE_FORM, 'Tồn LN02 của hàng 3M-035653 = 1 (dữ liệu thử).'],
       DU + ['Bấm "Thêm kho", chọn LN02.', 'Sửa Số lượng LN01 = 0.5, LN02 = 0.5.', 'Bấm Lưu.'], 'LN01 = 0.5, LN02 = 0.5',
       ['Lưu được; chi tiết phiếu gộp 2 dòng kho kế toán LN01 (0.5) và LN02 (0.5).'], [55, 269])
S3.add('Chọn trùng kho kế toán trong 1 dòng', 'P1', PRE_FORM, DU + ['Bấm "Thêm kho", chọn lại LN01.'], '—',
       ['Dưới ô vừa chọn: "Kho kế toán đã được chọn!" ngay khi chọn.', 'Bấm Lưu vẫn báo lỗi đó, không lưu.'], [62, 67])
S3.add('Cộng dồn nhiều ô cùng kho vượt SL được xuất', 'P0', [PRE_FORM, 'Phiếu xuất kho có 2 dòng cùng hàng, cùng ĐVT, SL xuất 1 và 2; '
                                                           'tồn LN01 = 2 (dữ liệu thử).'],
       TAO + ['Chọn phiếu xuất kho đó, chọn Kho kế toán dòng 1 = LN01 (dòng 2 tự điền LN01).', 'Bấm Lưu.'], '—',
       ['Mỗi ô riêng không vượt 2 nên màn cho gửi.', 'Máy chủ cộng dồn 1 + 2 = 3 > 2, báo dưới cả 2 ô Số lượng: "Kho LN01 - Liên '
        'Ninh - Hàng bán: Số lượng xuất không được vượt quá số lượng được xuất!"; không lưu.'], [62, 304])
S3.add('Bỏ kho kế toán thêm thừa', 'P2', PRE_FORM, DU + ['Bấm "Thêm kho".', 'Bấm thùng rác "Bỏ kho kế toán này" ở dòng kho mới.'],
       '—', ['Dòng kho mới biến mất, lỗi cũ của dòng bị xóa; dòng kho đầu tiên không có nút thùng rác.'], 99)
S3.add('Số lượng chỉ nhận số', 'P1', PRE_FORM, DU + ['Gõ "abc", "1,5" và "1.255" vào ô Số lượng dòng 1.'], '—',
       ['Chữ không nhập được; chỉ nhận số, tối đa 2 chữ số thập phân.'], [62, 63, 74, 81])
S3.add('Đơn giá bằng 0', 'P2', PRE_FORM, DU + ['Nhập Đơn giá dòng 1 = 0.', 'Bấm Lưu.'], 'Đơn giá: 0',
       ['Lưu được (đơn giá từ 0 trở lên là hợp lệ); Thành tiền dòng 1 = 0.'], 64)
S3.add('Ghi chú dài', 'P2', PRE_FORM, DU + ['Dán Ghi chú 1.000 ký tự.', 'Bấm Lưu.'], 'Ghi chú: 1.000 ký tự',
       ['Lưu được, hiển thị đủ ở màn chi tiết.', 'Lưu ý: tối đa 65.000 ký tự, vượt thì báo "Vui lòng nhập tối đa 65000 ký tự."'],
       [65, 66])
S3.add('Ký tự đặc biệt trong Ghi chú', 'P2', PRE_FORM, DU + ['Nhập Ghi chú "<b>Test</b> & @#$%".', 'Bấm Lưu.'], '—',
       ['Lưu được; màn chi tiết và bản in hiện nguyên chuỗi, không in đậm.'], 63)
S3.add('Ghi chú khoảng trắng', 'P2', PRE_FORM, DU + ['Nhập Ghi chú "   ".', 'Bấm Lưu.'], '—',
       ['Lưu được (Ghi chú không bắt buộc).'], [68, 69])
S3.add('File sai định dạng', 'P1', PRE_FORM, CHON + ['Bấm Thêm tài liệu, chọn file "bang.xlsx".'], 'File: bang.xlsx',
       ['Báo "Định dạng file không hợp lệ"; file không được thêm.', 'Chỉ nhận pdf, png, jpg, jpeg.'], [62, 70])
S3.add('File quá 20 MB', 'P2', PRE_FORM, CHON + ['Bấm Thêm tài liệu, chọn file pdf 25 MB.'], 'File: 25 MB',
       ['Báo "File quá lớn"; file không được thêm.'], 62)
S3.add('Không có trường duy nhất, phiếu xuất kho đã dùng biến khỏi ô chọn', 'P0', [PRE_FORM, 'Đã lưu 1 phiếu từ PXKĐCKK-00091.'],
       TAO + ['Mở ô Phiếu xuất kho.'], '—',
       ['PXKĐCKK-00091 không còn trong danh sách chọn (đã sang Đang hạch toán).', 'Mã PXHĐCKK tự sinh, không trùng.'], [67, 75, 82])
S3.add('Mở đường link Tạo với phiếu xuất kho không còn Chờ duyệt', 'P1', [PRE_FORM, 'PXKĐCKK-00091 đã sang Đang hạch toán.'],
       ['Mở lại đường link màn Tạo đã vào từ nút "Tạo phiếu xuất hàng" của PXKĐCKK-00091.'], '—',
       ['Dưới ô Phiếu xuất kho: "Phiếu xuất kho không còn lập được phiếu xuất hàng điều chỉnh hoặc bạn không có quyền."; bảng trống.'],
       [67, 311])
S3.add('Lỗi biến mất sau khi sửa', 'P1', PRE_FORM, TAO + ['Bấm Lưu (báo lỗi).', 'Chọn Phiếu xuất kho.'], '—',
       ['Chữ đỏ dưới ô Phiếu xuất kho biến mất ngay khi chọn.'], 71)
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, DU + ['Bấm Lưu và tiếp tục.'], '—',
       ['Báo "Lưu thành công.", ở lại màn Thêm với form trống.', 'Ô Phiếu xuất kho nạp lại, không còn PXKĐCKK-00091.'], [72, 76, 77])
S3.add('Lưu và tiếp tục khi chưa chọn Phiếu xuất kho', 'P1', PRE_FORM, TAO + ['Bấm Lưu và tiếp tục.'], '—',
       [REQ + ' dưới ô Phiếu xuất kho; không lưu, form giữ nguyên.'], 73)
S3.add('Đóng sau Lưu và tiếp tục', 'P2', PRE_FORM, DU + ['Bấm Lưu và tiếp tục.', 'Bấm Quay lại.'], '—',
       ['Về danh sách ngay (form trống, không hỏi); phiếu vừa lưu có trong danh sách.'], 78)
S3.add('Lưu: màn là trang, không còn form', 'P2', PRE_FORM, DU + ['Bấm Lưu.'], '—',
       ['Lưu xong về danh sách (không còn form).', 'Mở Tạo mới lại thì form trống.'], [83, 84])
S3.add('Quay lại khi chưa nhập gì', 'P1', PRE_FORM, TAO + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 93)
S3.add('Quay lại khi đã chọn / nhập', 'P0', PRE_FORM, CHON + ['Chọn Nhân viên.', 'Bấm Quay lại.'], '—',
       ['Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" với nút Thoát, Ở lại.',
        'Màn là trang nên không có nút X đóng form.'], [94, 95])
S3.add('Chọn Thoát', 'P1', PRE_FORM, CHON + ['Bấm Quay lại.', 'Bấm Thoát.'], '—', ['Về danh sách, không tạo phiếu.'], 96)
S3.add('Chọn Ở lại', 'P1', PRE_FORM, CHON + ['Bấm Quay lại.', 'Bấm Ở lại.'], '—',
       ['Ở lại form, dữ liệu đã chọn / nhập giữ nguyên.'], 97)
S3.add('Nhập rồi xóa hết', 'P2', PRE_FORM, TAO + ['Nhập Ghi chú rồi xóa hết.', 'Bấm Quay lại.'], '—',
       ['Về danh sách ngay, không hỏi.'], 98)
S3.add('Chọn rồi bỏ chọn Phiếu xuất kho', 'P2', PRE_FORM, CHON + ['Bấm × bỏ chọn Phiếu xuất kho.', 'Bấm Quay lại.'], '—',
       ['Phiếu kiểm kê, Kho, Thủ kho, bảng Chi tiết trở về trống.', 'Về danh sách không hỏi (dữ liệu như ban đầu).'], 99)
S3.add('Để màn lâu không thao tác', 'P2', [PRE_FORM, 'Đã mở màn, để nguyên 30 phút.'], DU + ['Bấm Lưu.'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên, về màn đăng nhập, không lưu.'], 100)
S3.add('Bấm Lưu liên tục', 'P1', PRE_FORM, DU + ['Bấm Lưu 3 lần thật nhanh.'], '—',
       ['Nút khóa trong lúc lưu; chỉ tạo 1 phiếu.'], 101)
S3.add('Hai tab cùng lập từ 1 phiếu xuất kho', 'P1', [PRE_FORM, 'Tab 1 và tab 2 cùng mở form, cùng chọn PXKĐCKK-00091 và nhập đủ.'],
       ['Tab 1 bấm Lưu.', 'Tab 2 bấm Lưu.'], '—',
       ['Cả 2 tab đều lưu được, sinh 2 phiếu cho cùng PXKĐCKK-00091.',
        'Lưu ý: giữ như hệ thống cũ (đã chốt) — không chặn lập trùng; số đã xử lý của phiếu kiểm kê bị cộng 2 lần.'], 102)
S3.add('Không phải Kế toán kho', 'P1', [ACC_N], ['Đăng nhập N.', MENU], '—',
       ['Không có nút Tạo mới.', 'Mở thẳng màn Tạo: ô Phiếu xuất kho không có lựa chọn nào; không lập được phiếu.'], [52, 295])

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
S4.add('Mở màn Sửa từ cột Hành động', 'P0', PRE_EDIT, ['Đăng nhập K.'] + SUA, '—',
       ['Mở trang "Sửa phiếu xuất hàng điều chỉnh kiểm kê: PXHĐCKK-00075".'], 103)
S4.add('Mở màn Sửa từ màn chi tiết', 'P1', PRE_EDIT, [MENU, 'Bấm PXHĐCKK-00075.', 'Bấm Sửa ở chân màn.'], '—',
       ['Mở màn Sửa của phiếu.'], 103)
S4.add('Dữ liệu điền đúng', 'P0', [PRE_LIST, P74], ['Đăng nhập DNS Admin.', MENU, 'Ở dòng PXHĐCKK-00074 bấm Sửa.'], '—',
       ['Phiếu xuất kho PXKĐCKK-00084, Phiếu kiểm kê TPE.KKK-01067 (liên kết), Kho "SG - Kho Sài Gòn", Thủ kho "DNS01 - DNS Admin".',
        'Nhân viên trống; File đính kèm 1 file pdf; Ghi chú đúng nội dung đã lưu.',
        'Bảng: dòng đầu Bộ gạt mưa UP PARTS cho xe Mazda CX5, SL xuất 1, Đơn giá 150,000; mỗi dòng 1 ô kho kế toán trống; có cột SL '
        'được xuất.'], 104)
S4.add('Trường được / không được sửa', 'P0', PRE_EDIT, SUA, '—',
       ['Sửa được: Nhân viên, Ghi chú, File đính kèm, Đơn giá, Kho kế toán, Số lượng, Thêm kho.',
        'Phiếu xuất kho, Phiếu kiểm kê là liên kết; Kho, Thủ kho khóa; dòng hàng, SL xuất không sửa được.',
        'File đính kèm có dấu *.'], 105)
S4.add('Các nút', 'P1', PRE_EDIT, SUA, '—', ['Chân màn: Lưu, Lưu và duyệt, Quay lại; không có Lưu và tiếp tục.'], 106)
S4.add('Sửa Đơn giá', 'P0', PRE_EDIT, SUA + ['Sửa Đơn giá dòng 1 thành 60,000.', 'Bấm Lưu.'], 'Đơn giá: 60,000',
       ['Báo "Lưu thành công.", về danh sách; phiếu vẫn Đang tạo.', 'Chi tiết hiện đơn giá mới, Thành tiền tính lại 60,000.'],
       [107, 110])
S4.add('Sửa nhiều trường', 'P1', PRE_EDIT, SUA + ['Đổi Nhân viên, sửa Ghi chú, thêm file bien_ban.pdf.', 'Bấm Lưu.'], FILE,
       ['Lưu được; chi tiết hiện Nhân viên, Ghi chú mới và có thêm bien_ban.pdf.'], 108)
S4.add('Giữ nguyên giá trị khi Lưu không đổi', 'P1', PRE_EDIT, SUA + ['Không đổi gì, bấm Lưu.'], '—',
       ['Lưu được, dữ liệu không đổi.', 'Lịch sử không có mốc "Thay đổi thông tin" mới.',
        'Lưu ý: giữ như hệ thống cũ — số đã xử lý của phiếu kiểm kê vẫn bị cộng thêm.'], [109, 125, 182])
S4.add('Ngày / người cập nhật và lịch sử sau khi sửa', 'P0', PRE_EDIT,
       SUA + ['Sửa Ghi chú thành "Nháp lần 2", Lưu.', 'Bấm Lịch sử ở dòng phiếu.'], '—',
       ['Có mốc "Thay đổi thông tin" người thực hiện K, thời điểm vừa lưu, Ghi chú "Nháp" sang "Nháp lần 2".'], [111, 112, 177])
S4.add('Sửa nhiều thông tin cùng lúc ghi 1 mốc', 'P2', PRE_EDIT,
       SUA + ['Đổi Nhân viên, sửa Đơn giá, thêm 1 file.', 'Lưu.', 'Mở Lịch sử.'], '—',
       ['1 mốc "Thay đổi thông tin" gồm Nhân viên, bảng dòng hàng (Đơn giá, Kho kế toán: số lượng) và File đính kèm.'],
       [178, 183])
S4.add('Bỏ trống Nhân viên khi Lưu nháp', 'P0', PRE_EDIT, SUA + ['Bấm × xóa Nhân viên.', 'Bấm Lưu.'], '—',
       ['Lưu được (Lưu nháp không bắt buộc Nhân viên); chi tiết hiện Nhân viên trống.',
        'Bấm Lưu và duyệt khi trống Nhân viên thì máy chủ báo ' + REQ + ' (xem nhóm Duyệt phiếu).'], [113, 117])
S4.add('Xóa hết file khi sửa', 'P1', [ACC_K, 'Phiếu PXHĐCKK-00075 Đang tạo có 1 file duy nhất.'],
       SUA + ['Bấm xóa file đó, bấm Xóa trong hộp.'], '—',
       ['Báo lỗi "Phiếu phải có ít nhất 1 file đính kèm."; file vẫn còn.'], 113)
S4.add('Vượt SL được xuất khi sửa', 'P1', PRE_EDIT, SUA + ['Đổi Kho kế toán dòng 1 sang LN02 (SL được xuất 0).', 'Bấm Lưu.'], '—',
       ['Dưới ô Số lượng: ' + OVER + '; ' + INC + '; không lưu.'], [114, 115])
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P2', PRE_EDIT, SUA + ['Đổi kho sang LN02, bấm Lưu (báo lỗi).', 'Sửa Số lượng ô đó.'], '—',
       ['Chữ đỏ dưới ô Số lượng biến mất ngay khi gõ.'], 118)
S4.add('Không có trường duy nhất để trùng', 'P2', PRE_EDIT, SUA, '—',
       ['Màn Sửa không có trường cần kiểm trùng (phiếu xuất kho, kho khóa).'], 116)
S4.add('Mở Sửa rồi Quay lại không đổi', 'P1', PRE_EDIT, SUA + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 119)
S4.add('Đổi rồi trả về ban đầu', 'P2', PRE_EDIT, SUA + ['Sửa Ghi chú rồi gõ lại "Nháp".', 'Bấm Quay lại.'], '—',
       ['Về danh sách không hỏi.'], 120)
S4.add('Quay lại khi đã đổi', 'P0', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Bấm Quay lại.'], '—',
       ['Hộp "Thông tin chưa lưu" (Thoát / Ở lại).'], 121)
S4.add('Thoát không lưu', 'P1', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Bấm Quay lại, chọn Thoát.'], '—',
       ['Về danh sách; Ghi chú của phiếu vẫn "Nháp".'], [122, 124])
S4.add('Ở lại', 'P2', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Bấm Quay lại, chọn Ở lại.'], '—', ['Giữ form với Ghi chú đã sửa.'], 123)
S4.add('Phiếu đã hạch toán không sửa được', 'P0', [PRE_LIST, P73], [MENU, 'Quan sát dòng 00073.', 'Mở đường link màn Sửa của 00073.'],
       '—', ['Không có nút Sửa.', 'Mở đường link màn Sửa tự chuyển về màn chi tiết.'], [126, 129])
S4.add('Phiếu đổi trạng thái trong lúc đang sửa', 'P1', [PRE_EDIT, 'Tab 1 đang mở màn Sửa; tab 2 vừa Lưu và duyệt phiếu.'],
       ['Ở tab 1 bấm Lưu.'], '—', ['Báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang"; không lưu.'], [128, 127])
S4.add('Xóa file đã lưu', 'P1', [ACC_K, 'PXHĐCKK-00075 Đang tạo có 2 file.'], SUA + ['Bấm xóa ở dòng bien_ban.pdf.',
       'Bấm Xóa trong hộp.'], '—',
       ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa file đính kèm này?" (Xóa / Hủy).',
        'Báo "Xóa file thành công", file biến mất ngay (không cần bấm Lưu); lịch sử có mốc thay đổi File đính kèm.'], 108)
S4.add('Người khác không sửa được phiếu Đang tạo', 'P0', [ACC_Q1, DRAFT], ['Đăng nhập Q1.', MENU, 'Tìm PXHĐCKK-00075.'], '—',
       ['Không thấy phiếu (phiếu Đang tạo của người khác luôn ẩn).'], [126, 290])

# ============================================================== V. DUYỆT PHIẾU (LƯU VÀ DUYỆT)
S5 = Sec(5)
S5.add('Nút Lưu và duyệt hiện đúng điều kiện', 'P0', [PRE_EDIT, P73], [MENU, 'Mở màn Tạo.', 'Mở màn Sửa của 00075.', 'Mở chi tiết 00073.'],
       '—', ['Màn Tạo và màn Sửa có nút chính "Lưu và duyệt".', 'Màn chi tiết phiếu Đã hạch toán không có nút này.'], 300)
S5.add('Hộp xác nhận Lưu và duyệt', 'P0', PRE_FORM, DU + ['Bấm Lưu và duyệt.'], '—',
       ['Hộp "Xác nhận lưu và duyệt": "Lưu và duyệt sẽ trừ tồn kho kế toán ngay và không sửa được phiếu nữa. Bạn có chắc muốn tiếp '
        'tục?" với nút Lưu và duyệt, Hủy.'], [90, 301])
S5.add('Lưu và duyệt từ màn Tạo với dữ liệu đầy đủ', 'P0', PRE_FORM,
       DU + ['Nhập Ghi chú.', 'Bấm Lưu và duyệt.', 'Bấm Lưu và duyệt trong hộp xác nhận.'], 'Ghi chú: Xuất hàng thiếu kho LN',
       ['Báo "Duyệt thành công.", về danh sách.', 'Phiếu mới nhãn xanh lá "Đã hạch toán"; không có nút Sửa.'], [86, 92, 302, 305])
S5.add('Lưu và duyệt thiếu Nhân viên / Kho kế toán', 'P0', PRE_FORM,
       CHON + ['Bấm Lưu và duyệt.', 'Bấm Lưu và duyệt trong hộp xác nhận.'], '—',
       ['Hộp xác nhận VẪN hiện (màn chưa kiểm bắt buộc).', 'Sau khi xác nhận: dưới Nhân viên, Kho kế toán, Số lượng ' + REQ +
        '; dưới Thành tiền ' + MIS + '; thông báo lỗi "Bắt buộc phải nhập"; phiếu không được lưu.'], [87, 303])
S5.add('Lưu và duyệt khi tổng số lượng kho kế toán khác SL xuất', 'P0', [PRE_FORM, 'Tồn LN02 của hàng = 1 (dữ liệu thử).'],
       DU + ['Bấm "Thêm kho", chọn LN02, nhập Số lượng 1 (LN01 vẫn 1).', 'Bấm Lưu và duyệt, xác nhận.'], 'LN01 = 1, LN02 = 1',
       ['Dưới Thành tiền dòng 1: ' + MIS + '; không lưu.', 'Lưu ý: cùng dữ liệu này bấm Lưu (nháp) thì lưu được.'], [88, 304])
S5.add('Trừ tồn kho kế toán khi duyệt', 'P0', [PRE_FORM, 'Ghi nhận tồn kho kế toán của hàng 3M-035653 ở kho LN01 trước khi duyệt: 2.'],
       DU + ['Lưu và duyệt, xác nhận.', 'Mở Hàng có thể bán theo công ty, tra hàng 3M-035653.'], '—',
       ['Tồn kho kế toán LN01 của hàng 3M-035653 giảm 1 thành 1.'], [306, 307])
S5.add('Đơn giá vốn tính khi duyệt', 'P0', [PRE_FORM, 'Ghi nhận giá trị tồn kho kế toán LN01 của hàng 3M-035653 trước khi duyệt.'],
       DU + ['Lưu và duyệt, xác nhận.', 'Mở chi tiết phiếu vừa duyệt.'], '—',
       ['Có cột Đơn giá vốn = giá trị tồn giảm đi / 1 (lớp nhập cũ nhất còn tồn — nhập trước xuất trước); Thành tiền vốn = 1 × Đơn '
        'giá vốn.', 'Không phát sinh bút toán nào cho phiếu (giữ như hệ thống cũ).'], 306)
S5.add('Phiếu xuất kho và phiếu kiểm kê sau khi duyệt', 'P0', PRE_FORM,
       DU + ['Lưu và duyệt, xác nhận.', WIE_MENU, 'Xem PXKĐCKK-00091.', KK_MENU, 'Xem phiếu kiểm kê TPE.KKK-01095.'], '—',
       ['PXKĐCKK-00091 chuyển "Đã hạch toán", Người duyệt = K, lịch sử có mốc kèm "Phiếu xuất hàng điều chỉnh kiểm kê <mã>.".',
        'Phiếu kiểm kê chuyển "Hoàn thành" nếu đã xử lý hết, còn việc thì "Đang xử lý".'], [307, 312])
S5.add('Bấm Hủy trong hộp xác nhận', 'P0', PRE_FORM, DU + ['Bấm Lưu và duyệt.', 'Bấm Hủy.'], '—',
       ['Hộp đóng, form giữ nguyên, không lưu, tồn không đổi.'], [91, 310])
S5.add('Lưu và duyệt từ màn Sửa', 'P0', PRE_EDIT, SUA + ['Bấm Lưu và duyệt, xác nhận.'], '—',
       ['Báo "Duyệt thành công."; phiếu Đã hạch toán; tồn kho kế toán trừ như khi duyệt từ màn Tạo.',
        'Lịch sử có mốc "Thay đổi trạng thái" Đang tạo sang Đã hạch toán.'], [86, 305, 312])
S5.add('Lưu và duyệt từ màn Sửa khi phiếu không còn file', 'P0', [ACC_K, 'PXHĐCKK-00075 Đang tạo không có file nào.'],
       SUA + ['Bấm Lưu và duyệt, xác nhận.'], '—', ['Dưới khối File đính kèm: ' + REQ + '; không duyệt.'], 303)
S5.add('Tồn bị phiếu khác dùng trước khi duyệt', 'P0', [PRE_EDIT, 'Sau khi mở màn Sửa, phiếu khác đã xuất hết tồn LN01 của hàng.'],
       SUA + ['Bấm Lưu và duyệt, xác nhận.'], '—', ['Dưới ô Số lượng: ' + OVER_BE + '.', 'Không lưu, tồn không đổi.'], [304, 310])
S5.add('Không gửi thông báo khi duyệt', 'P2', [PRE_FORM, 'Tài khoản Q1 cùng công ty.'], DU + ['Lưu và duyệt, xác nhận.',
       'Đăng nhập Q1, mở chuông thông báo.'], '—',
       ['Không phát sinh thông báo nào (màn không gửi thông báo, giống hệ thống cũ).'], [308, 309])
S5.add('Bấm Lưu và duyệt liên tục', 'P1', PRE_FORM, DU + ['Bấm Lưu và duyệt trong hộp nhiều lần nhanh.'], '—',
       ['Chỉ tạo 1 phiếu, tồn chỉ trừ 1 lần.'], 101)
S5.add('Không duyệt lại phiếu đã hạch toán', 'P1', [PRE_LIST, P73], [MENU, 'Mở chi tiết 00073.', 'Mở đường link màn Sửa 00073.'],
       '—', ['Không có nút Sửa / Lưu và duyệt; đường link Sửa tự về màn chi tiết.'], 311)
S5.add('Trường được làm mới sau khi duyệt', 'P2', PRE_FORM, DU + ['Lưu và duyệt (đủ dữ liệu).', 'Bấm Tạo mới lại.'], '—',
       ['Form mới trống; PXKĐCKK-00091 không còn trong ô Phiếu xuất kho.'], [89, 91])

# ============================================================== VI. LỊCH SỬ THAY ĐỔI
S6 = Sec(6)
S6.add('Mở cửa sổ lịch sử từ danh sách', 'P0', [PRE_LIST, P73], [MENU, 'Ở dòng 00073 bấm Lịch sử.'], '—',
       ['Mở cửa sổ "Lịch sử thay đổi: PXHĐCKK-00073", nút Bộ lọc, nút Đóng.'], 162)
S6.add('Thông tin mỗi mốc', 'P0', [PRE_LIST, P73], [MENU, 'Mở lịch sử 00073.'], '—',
       ['3 mốc ngày 02/11/2026, mỗi mốc ghi "Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ".',
        'Mốc "Thay đổi trạng thái" 11:17: "Trạng thái: Đang tạo sang Đã hạch toán".'], [163, 165, 166, 167])
S6.add('Nội dung thay đổi cũ sang mới', 'P0', [PRE_LIST, P73], [MENU, 'Mở lịch sử 00073, đọc mốc "Thay đổi thông tin" 11:17.'], '—',
       ['Bảng "Chi tiết hàng hóa sửa thông tin", dòng MẶT NẠ BẢO VỆ.',
        'Kho kế toán cũ: "LN02 - Liên Ninh - Hàng khuyến mại: 0; LN01 - Liên Ninh - Hàng bán: 4".',
        'Kho kế toán mới: "LN01 - Liên Ninh - Hàng bán: 4".'], 168)
S6.add('Mới nhất ở trên', 'P1', [PRE_LIST, P73], [MENU, 'Mở lịch sử 00073.'], '—',
       ['Thứ tự: Thay đổi trạng thái, Thay đổi thông tin (11:17), Tạo mới (11:16).'], 164)
S6.add('Phiếu lập ở hệ thống cũ chưa có lịch sử', 'P2', [PRE_LIST, 'PXHĐCKK-00040 (SG_KT - Nguyễn Thị Vân) chưa có mốc ghi.'],
       [MENU, 'Mở lịch sử 00040.'], '—', ['Cửa sổ báo chưa có lịch sử, không lỗi.'], 173)
S6.add('Lọc theo loại hành động', 'P1', [PRE_LIST, P73],
       [MENU, 'Mở lịch sử 00073.', 'Bấm Bộ lọc, chọn Loại hành động = Tạo mới.', 'Đổi thành Thay đổi trạng thái.'], '—',
       ['Bước 3: còn mốc Tạo mới.', 'Bước 4: còn mốc Thay đổi trạng thái.',
        'Ô có: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.'], [169, 175])
S6.add('Lọc theo người thực hiện', 'P2', [PRE_LIST, P73], [MENU, 'Mở lịch sử, Bộ lọc, chọn Người thực hiện = DNS Admin.'], '—',
       ['Còn đủ 3 mốc.'], 170)
S6.add('Lọc theo thời gian', 'P2', [PRE_LIST, P73], [MENU, 'Mở lịch sử, Bộ lọc, Từ ngày = Đến ngày = 01/11/2026.'], '—',
       ['"Không có lịch sử phù hợp bộ lọc."; đổi thành 02/11/2026 thì hiện đủ 3 mốc.'], [171, 173])
S6.add('Kết hợp lọc và Làm mới', 'P2', [PRE_LIST, P73],
       [MENU, 'Mở lịch sử, lọc Loại = Tạo mới và Từ ngày 02/11/2026.', 'Bấm Làm mới.'], '—',
       ['Bước 2: 1 mốc.', 'Bước 3: hiện lại đủ các mốc.'], [172, 174])
S6.add('Lịch sử tạo bằng Lưu và duyệt từ màn Tạo', 'P1', PRE_FORM, DU + ['Lưu và duyệt (đủ dữ liệu).', 'Mở lịch sử phiếu mới.'], '—',
       ['Có 1 mốc "Tạo mới".'], 176)
S6.add('Đóng cửa sổ', 'P1', [PRE_LIST, P73], [MENU, 'Sang trang 2, lọc Trạng thái.', 'Mở lịch sử 1 dòng, bấm Đóng.',
       'Mở lại, bấm (x).'], '—', ['Cửa sổ đóng; danh sách giữ trang, bộ lọc.'], [184, 185])
S6.add('Xem / in không ghi lịch sử', 'P2', [PRE_LIST, P73], [MENU, 'Mở chi tiết 00073, bấm In, đóng.', 'Mở lịch sử.'], '—',
       ['Không có mốc mới.'], 182)

# ============================================================== VII. XEM CHI TIẾT
S7 = Sec(7)
S7.add('Mở màn chi tiết', 'P0', [PRE_LIST, P73], [MENU, 'Bấm PXHĐCKK-00073.'], '—',
       ['Mở TRANG chi tiết, tab "Chi tiết phiếu xuất hàng điều chỉnh kiểm kê: PXHĐCKK-00073"; tiêu đề kèm nhãn "Đã hạch toán".'],
       [186, 187])
S7.add('Đầy đủ trường', 'P0', [PRE_LIST, P73], [MENU, 'Bấm PXHĐCKK-00073.'], '—',
       ['Thông tin chung: Phiếu xuất kho PXKĐCKK-00090, Phiếu kiểm kê TPE.KKK-01087 (liên kết), Kho LN - Liên Ninh, Thủ kho DNS01 - '
        'DNS Admin, Nhân viên DNS01 - DNS Admin, Ghi chú trống.', 'Khối File đính kèm có 2 file pdf.',
        'Bảng Chi tiết: MẶT NẠ BẢO VỆ, H8A/PW96, 3M-H8APW96, Cái, SL xuất 4, Đơn giá 12,323, Thành tiền 49,292, Đơn giá vốn 980,000, '
        'Thành tiền vốn 3,920,000, Kho kế toán LN01 - Liên Ninh - Hàng bán, Số lượng 4; không có cột SL được xuất.'], [188, 189])
S7.add('Khớp dữ liệu danh sách', 'P1', [PRE_LIST, P73], [MENU, 'So dòng 00073 và màn chi tiết.'], '—',
       ['Phiếu xuất kho, Phiếu kiểm kê, Kho, người tạo, ngày tạo trùng khớp.'], 190)
S7.add('Chế độ chỉ đọc', 'P0', [PRE_LIST, P73], [MENU, 'Bấm PXHĐCKK-00073.'], '—',
       ['Mọi ô khóa; bảng không có dấu *; không có Lưu / Lưu và duyệt.', 'Chân màn: In, Quay lại.'], [191, 192])
S7.add('Phiếu Đang tạo của mình', 'P1', [PRE_LIST, P74], [MENU, 'Bấm PXHĐCKK-00074.'], '—',
       ['Chân màn có thêm nút Sửa.', 'Đơn giá vốn, Thành tiền vốn = 0 (chưa trừ tồn); Nhân viên trống.'], [193, 194])
S7.add('Khu vực lịch sử', 'P1', [PRE_LIST, P73], [MENU, 'Bấm 00073.', 'Bấm Xem lịch sử.'], '—',
       ['Khối Lịch sử mở rộng, có 3 mốc như cửa sổ lịch sử.'], 195)
S7.add('Quay lại giữ trang và bộ lọc', 'P1', [PRE_LIST, 'Đang lọc Kho = LN - Liên Ninh.'], ['Bấm một số phiếu.', 'Bấm Quay lại.'], '—',
       ['Về danh sách, vẫn lọc Kho LN.'], [196, 197])
S7.add('Liên kết phiếu nguồn', 'P2', [PRE_LIST, P73], ['Bấm 00073.', 'Bấm PXKĐCKK-00090, rồi TPE.KKK-01087.'], '—',
       ['Mở chi tiết phiếu xuất kho / phiếu kiểm kê ở tab mới.'], 188)
S7.add('Phiếu không tồn tại', 'P1', PRE_LIST, ['Mở đường link chi tiết với số phiếu không tồn tại.'], '—',
       ['Chuyển sang trang không tìm thấy, không báo lỗi nổi.'], 196)

# ============================================================== VIII. IN PHIẾU
S8 = Sec(8)
S8.add('In phiếu từ danh sách', 'P0', [PRE_LIST, P73], [MENU, 'Ở dòng 00073 bấm In.'], '—',
       ['Cửa sổ "Xem trước phiếu xuất hàng điều chỉnh kiểm kê PXHĐCKK-00073".',
        'Bản in: "PHIẾU XUẤT HÀNG ĐIỀU CHỈNH KIỂM KÊ", Số phiếu, Ngày lập 02/11/2026, Phiếu xuất kho PXKĐCKK-00090, Phiếu kiểm kê '
        'TPE.KKK-01087, Kho LN - Liên Ninh, Thủ kho DNS Admin, Ghi chú; bảng STT, Tên hàng, Model, Mã hàng, ĐVT, SL xuất, Đơn giá '
        'vốn, Thành tiền vốn, Kho kế toán, Số lượng (dòng: 4, 980,000, 3,920,000, LN01, 4); Người lập DNS Admin in đậm.'], 6)
S8.add('In phiếu từ màn chi tiết', 'P1', [PRE_LIST, P73], [MENU, 'Bấm 00073.', 'Bấm In.'], '—', ['Cùng bản xem trước.'], 6)
S8.add('Letterhead theo công ty của phiếu', 'P1', [ACC_Q1, 'PXHĐCKK-00067 thuộc công ty TPSG; Q1 thuộc công ty TPE.'],
       ['Đăng nhập Q1.', MENU, 'In 00067.'], '—', ['Đầu bản in là logo / letterhead công ty TPSG.'], 6)
S8.add('In phiếu Đang tạo', 'P2', [PRE_LIST, P74], [MENU, 'Ở dòng 00074 bấm In.'], '—',
       ['In được; cột Đơn giá vốn, Thành tiền vốn = 0; Kho kế toán, Số lượng trống.'], 6)
S8.add('Bấm In trong cửa sổ', 'P1', [PRE_LIST, P73], ['Mở xem trước 00073.', 'Bấm In.'], '—', ['Mở hộp thoại in của trình duyệt.'], 6)
S8.add('In danh sách: theo bộ lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = LN - Liên Ninh.', 'Bấm In danh sách.'], '—',
       ['Cửa sổ "Xem trước danh sách phiếu xuất hàng điều chỉnh kiểm kê", tiêu đề "DANH SÁCH PHIẾU XUẤT HÀNG ĐIỀU CHỈNH KIỂM KÊ".',
        'Đúng 5 dòng; cột STT, Số phiếu, Phiếu xuất kho, Phiếu kiểm kê, Kho, Người tạo, Ngày tạo, Trạng thái.'], [219, 220])
S8.add('In danh sách: không có dữ liệu', 'P2', PRE_LIST, [MENU, 'Tìm "ZZZ", bấm In danh sách.'], '—',
       ['Cửa sổ báo "Không có dữ liệu để in".'], 222)
S8.add('In danh sách: vượt 2.000 dòng', 'P2', 'Phạm vi xem có 2.500 phiếu.', [MENU, 'Bấm In danh sách.'], '—',
       ['Không có bản in, ẩn nút In; hiện "Danh sách có 2,500 dòng, vượt mức in tối đa 2,000 dòng nên chưa in được…".'], 221)
S8.add('Đóng cửa sổ xem trước', 'P2', [PRE_LIST, P73], ['Mở xem trước 00073.', 'Bấm (x).'], '—',
       ['Cửa sổ đóng, danh sách giữ nguyên.'], 185)

# ============================================================== IX. TÙY CHỈNH CỘT
S9 = Sec(9)
S9.add('Mở cửa sổ Tùy chỉnh cột', 'P0', PRE_LIST, [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột", dòng hướng dẫn, 9 cột, "Đang chọn 9/9 cột", nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng.'], [198, 199])
S9.add('Cột chọn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa lưu cấu hình.'], ['Mở Tuỳ chỉnh cột.'], '—', ['Cả 9 cột được tích.'], 200)
S9.add('Ẩn cột', 'P0', PRE_LIST, ['Mở Tuỳ chỉnh cột, bỏ tích Phiếu kiểm kê, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công"; bảng không còn cột Phiếu kiểm kê.'], [202, 206])
S9.add('Hiện lại cột ẩn', 'P1', 'Đang ẩn cột Phiếu kiểm kê.', ['Mở Tuỳ chỉnh cột, tích Phiếu kiểm kê, Lưu.'], '—',
       ['Cột hiện lại đúng vị trí.'], 201)
S9.add('Cột khóa không ẩn được', 'P0', PRE_LIST, ['Mở Tuỳ chỉnh cột.'], '—',
       ['STT, Số phiếu, Hành động có biểu tượng ổ khóa, không bỏ tích / kéo được.'], [203, 205])
S9.add('Kéo đổi thứ tự cột', 'P1', PRE_LIST, ['Kéo cột Kho lên sau Số phiếu, Lưu.'], '—', ['Bảng hiện Kho ngay sau Số phiếu.'], 204)
S9.add('Đóng không lưu', 'P1', PRE_LIST, ['Bỏ tích Kho, bấm Đóng.'], '—', ['Bảng vẫn có cột Kho.'], 207)
S9.add('Ghi nhớ sau F5', 'P1', 'Đã ẩn cột Phiếu kiểm kê và Lưu.', ['Nhấn F5.'], '—', ['Cột Phiếu kiểm kê vẫn ẩn.'], 208)
S9.add('Cấu hình theo tài khoản', 'P2', 'Tài khoản A đã ẩn cột Kho.', ['Đăng nhập B, mở màn.'], '—', ['B vẫn thấy cột Kho.'], 209)
S9.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', 'Đang lọc Kho = LN - Liên Ninh.', ['Ẩn cột Người tạo, Lưu.'], '—',
       ['Vẫn 5 phiếu, bộ lọc giữ nguyên.'], [210, 211])

# ============================================================== X. XUẤT DANH SÁCH EXCEL
S10 = Sec(10)
S10.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel.'], '—',
        ['Cửa sổ "Chọn trường xuất Excel": 7 trường Số phiếu, Phiếu xuất kho, Phiếu kiểm kê, Kho, Người tạo, Ngày tạo, Trạng thái; '
         '"Đang chọn 7/7 trường".'], [212, 213])
S10.add('Trường chọn mặc định theo cột đang hiện', 'P1', 'Đang ẩn cột Phiếu kiểm kê.', ['Bấm Xuất Excel.'], '—',
        ['Phiếu kiểm kê không được tích sẵn.'], [214, 215])
S10.add('Xuất tất cả trường', 'P0', PRE_LIST, ['Bấm Xuất Excel, Chọn tất cả, Xuất file.'], '—',
        ['Tải "danh_sach_phieu_xuat_hang_dieu_chinh_kiem_ke.xlsx", báo "Xuất Excel thành công".', 'Đủ 74 dòng, cột STT + 7 cột.'],
        [216, 223, 227])
S10.add('Xuất một số trường', 'P1', PRE_LIST, ['Bỏ chọn hết, tích Số phiếu, Trạng thái, Xuất file.'], '—',
        ['File chỉ có STT, Số phiếu, Trạng thái.'], 217)
S10.add('Không chọn trường', 'P1', PRE_LIST, ['Bấm Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S10.add('Xuất theo tìm kiếm', 'P1', PRE_LIST, ['Tìm "0007".', 'Xuất file.'], '—', ['File có 6 dòng 00007, 00070–00074.'], 219)
S10.add('Xuất theo bộ lọc', 'P0', PRE_LIST, [ADV, 'Chọn Kho = LN - Liên Ninh.', 'Xuất file.'], '—', ['File có đúng 5 dòng.'], 220)
S10.add('Xuất nhiều trang', 'P1', PRE_LIST, ['Đang ở trang 1 (10 dòng/trang), Xuất file.'], '—',
        ['File đủ 74 dòng, không chỉ trang đang xem; hiện tiến độ "Đã tải x/y dòng…".'], 221)
S10.add('Danh sách rỗng', 'P1', PRE_LIST, ['Tìm "ZZZ".', 'Xuất file.'], '—', ['Báo "Không có dữ liệu để xuất", không tạo file.'], 222)
S10.add('Cấu trúc file', 'P0', PRE_LIST, ['Xuất tất cả trường.', 'Mở file.'], '—',
        ['Đầu file có letterhead công ty người xuất và "DANH SÁCH PHIẾU XUẤT HÀNG ĐIỀU CHỈNH KIỂM KÊ"; trang tính "Xuat hang dieu '
         'chinh kiem ke".', 'Dòng tên cột đúng tên trường; cuối file khối ký "Người lập".'], [224, 225])
S10.add('Thứ tự cột theo kéo thả', 'P1', PRE_LIST, ['Kéo Trạng thái lên đầu, Xuất file.'], '—', ['Cột sau STT là Trạng thái.'], 226)
S10.add('Dữ liệu khớp và định dạng', 'P0', [PRE_LIST, P73], ['Xuất tất cả, tìm dòng 00073.'], '—',
        ['Phiếu xuất kho "PXKĐCKK-00090", Ngày tạo "02/11/2026 11:16", Trạng thái "Đã hạch toán".',
         'Tiếng Việt có dấu hiển thị đúng (Kho "LN - Liên Ninh").'], [228, 229, 230])

# ============================================================== XI. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S11 = Sec(11)
S11.add('Nút Tạo phiếu xuất hàng ở phiếu xuất kho', 'P0', [ACC_K, SRC], ['Đăng nhập K.', WIE_MENU], '—',
        ['Dòng PXKĐCKK-00091 (Chờ duyệt) có nút "Tạo phiếu xuất hàng"; dòng Đang hạch toán / Đã hạch toán không có.'], [274, 300])
S11.add('Phiếu xuất kho chuyển Đang hạch toán khi Lưu', 'P0', PRE_FORM, DU + ['Bấm Lưu.', WIE_MENU, 'Xem PXKĐCKK-00091.'], '—',
        ['PXKĐCKK-00091 nhãn "Đang hạch toán", không còn nút Tạo phiếu xuất hàng.',
         'Lịch sử phiếu xuất kho có mốc "Thay đổi trạng thái" kèm "Phiếu xuất hàng điều chỉnh kiểm kê <mã>.".'], [281, 282])
S11.add('Lưu (Đang tạo) không trừ tồn kho kế toán', 'P0', PRE_FORM, DU + ['Bấm Lưu.', 'Tra tồn kho kế toán hàng 3M-035653.'], '—',
        ['Tồn kho kế toán không đổi (LN01 vẫn 2).'], 307)
S11.add('Phiếu kiểm kê được cộng số đã xử lý', 'P0', PRE_FORM, DU + ['Bấm Lưu.', KK_MENU, 'Xem phiếu kiểm kê TPE.KKK-01095.'], '—',
        ['Dòng hàng thiếu được ghi đã xử lý; phiếu kiểm kê chuyển Hoàn thành nếu hết việc, ngược lại Đang xử lý.'], [281, 307])
S11.add('Sửa phiếu Đang tạo cộng số đã xử lý lần nữa', 'P1', [PRE_EDIT, 'Ghi nhận số đã xử lý của dòng kết quả kiểm kê trước khi sửa.'],
        SUA + ['Không đổi gì, bấm Lưu.', 'Xem lại phiếu kiểm kê.'], '—',
        ['Số đã xử lý tăng thêm đúng SL xuất.', 'Lưu ý: giữ như hệ thống cũ (đã chốt 30/10/2026), không phải lỗi mới.'], 286)
S11.add('Giá vốn hàng thiếu ở Biên bản xử lý hàng thừa, thiếu', 'P1', [PRE_LIST, P73],
        ['Vào phân hệ Tài chính > menu "Kiểm kê" > bấm "Biên bản xử lý hàng thừa, thiếu sau kiểm kê".',
         'Lập / xem biên bản của phiếu kiểm kê TPE.KKK-01087, kho LN.'], '—',
        ['Dòng hàng thiếu 3M-H8APW96 lấy giá vốn 980,000 từ phiếu PXHĐCKK-00073.'], 274)
S11.add('Giá vốn phiếu xuất sau dùng lớp giá còn lại', 'P2', [PRE_FORM, 'Phiếu từ PXKĐCKK-00091 đã Lưu và duyệt, tiêu lớp nhập cũ nhất.'],
        ['Vào Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Xuất hàng > Phiếu xuất hàng.',
         'Lập và duyệt phiếu xuất hàng 3M-035653 từ kho kế toán LN01.'], '—',
        ['Giá vốn phiếu xuất hàng lấy lớp giá kế tiếp (lớp đã bị phiếu điều chỉnh tiêu không còn).'], 274)
S11.add('Cấp con đúng cấp cha', 'P1', [PRE_LIST, P73], [MENU, 'Mở 00073.'], '—',
        ['Dòng hàng thuộc đúng phiếu xuất kho PXKĐCKK-00090, phiếu kiểm kê TPE.KKK-01087, kho LN; kho kế toán thuộc kho LN.'],
        [283, 285])
S11.add('Tham chiếu giữ khi đổi trạng thái', 'P1', [PRE_LIST, P73], [MENU, 'Mở 00073 (Đã hạch toán).'], '—',
        ['Liên kết phiếu xuất kho, phiếu kiểm kê, dòng hàng, file vẫn đủ.'], 284)
S11.add('Tên hàng lưu cố định lúc lập', 'P2', [PRE_LIST, P73], ['Đổi tên hàng 3M-H8APW96 ở danh mục.', 'Mở 00073.'], '—',
        ['Phiếu vẫn hiện tên cũ "MẶT NẠ BẢO VỆ".'], [272, 278, 279])
S11.add('Không xóa được kho kế toán / kho / vị trí / hàng đã dùng', 'P1', [PRE_LIST, P73],
        ['Vào phân hệ Kho > menu "Danh mục" > bấm "Kho kế toán".', 'Xóa kho kế toán "LN01 - Liên Ninh - Hàng bán".'], '—',
        ['Hệ thống chặn xóa vì kho kế toán đã có trên phiếu / đã phát sinh tồn.'], 270)
S11.add('Kho kế toán đã khóa không chọn mới được', 'P1', [PRE_FORM, 'Kho kế toán LN02 vừa bị khóa ở danh mục.'], CHON + ['Mở ô Kho kế toán.'],
        '—', ['Không còn LN02 trong danh sách chọn.'], [271, 276])
S11.add('Phiếu xuất kho chưa Chờ duyệt không lập được', 'P1', [ACC_K, 'PXKĐCKK-00092 đang Đang tạo.'], TAO + ['Mở ô Phiếu xuất kho.'],
        '—', ['Không có PXKĐCKK-00092.'], 268)

# ============================================================== XII. PHÂN QUYỀN (cuối)
S12 = Sec(12)
S12.add('Quyền Xem mức Tổng công ty', 'P0', ACC_Q1, ['Đăng nhập Q1.', MENU, ADV], '—',
        ['Thấy đủ phiếu của mọi công ty (trừ phiếu Đang tạo của người khác — không thấy 00074, 00072).',
         'Có ô lọc Công ty và Phòng ban; không có nút Tạo mới.'], [287, 299])
S12.add('Quyền Xem mức Công ty', 'P0', [ACC_Q2, 'PXHĐCKK-00067 thuộc TPSG; PXHĐCKK-00073 thuộc TPE.'],
        ['Đăng nhập Q2.', MENU, ADV], '—', ['Thấy 00067, KHÔNG thấy 00073.', 'Có ô Phòng ban, không có ô Công ty.'], [287, 299])
S12.add('Hai Vai trò khác mức thì áp mức lớn hơn', 'P1', ['Tài khoản Q12: 2 Vai trò ở công ty TPSG, một cấp mức Công ty, một cấp mức '
                                                          'Tổng công ty.'],
        ['Đăng nhập Q12.', MENU, ADV], '—', ['Thấy cả 00067 và 00073 (mức Tổng công ty); có ô Công ty.'], 287)
S12.add('Đổi công ty đang làm việc', 'P1', [ACC_Q2, 'Q2 làm việc ở 2 công ty TPSG, TPE; Vai trò mức Công ty chỉ được cấp ở TPSG.'],
        ['Đăng nhập Q2 (đang ở TPSG), mở màn.', 'Đổi công ty đang làm việc sang TPE, mở lại màn.'], '—',
        ['Bước 1: thấy 00067.', 'Bước 2: quyền tính theo TPE — chỉ còn phiếu Q2 tự tạo; không thấy 00067.'], [297, 298])
S12.add('Không có quyền nào', 'P0', ACC_N, ['Đăng nhập N.', MENU], '—',
        ['Menu vẫn hiện, mở được màn.', 'Chỉ thấy PXHĐCKK-00076 do N tạo; không có nút Tạo mới.'], [287, 295, 299])
S12.add('Kế toán kho lập được phiếu', 'P0', PRE_FORM, ['Đăng nhập K.'] + DU + ['Bấm Lưu.'], '—',
        ['K thấy nút Tạo mới, lập được phiếu và thấy phiếu đó trong danh sách.'], 289)
S12.add('Xem chi tiết trong phạm vi', 'P0', [ACC_Q2], ['Đăng nhập Q2.', MENU, 'Mở 00067.'], '—', ['Xem được đầy đủ.'], 288)
S12.add('URL chi tiết ngoài phạm vi', 'P0', [ACC_N, 'N có đường link chi tiết 00073.'], ['Đăng nhập N, mở đường link.'], '—',
        ['Chuyển sang trang không tìm thấy; không lộ dữ liệu.'], [288, 296])
S12.add('Sửa chỉ dành cho người tạo', 'P0', [ACC_Q1, DRAFT], ['Đăng nhập Q1.', 'Mở đường link màn Sửa của 00075.'], '—',
        ['Chuyển sang trang không tìm thấy (phiếu Đang tạo của người khác nằm ngoài phạm vi).'], [290, 296])
S12.add('Ẩn nút khi thiếu quyền', 'P0', [ACC_N, SRC], ['Đăng nhập N.', MENU, WIE_MENU], '—',
        ['Màn này không có nút Tạo mới; màn Phiếu xuất kho điều chỉnh kiểm kê không có nút Tạo phiếu xuất hàng ở PXKĐCKK-00091.'], 295)
S12.add('Mở thẳng màn Tạo kèm phiếu xuất kho khi không phải Kế toán kho', 'P1', [ACC_N, SRC],
        ['Đăng nhập N.', 'Mở đường link màn Tạo kèm phiếu PXKĐCKK-00091.'], '—',
        ['Dưới ô Phiếu xuất kho: "Phiếu xuất kho không còn lập được phiếu xuất hàng điều chỉnh hoặc bạn không có quyền."; bảng trống.'],
        [295, 296])
S12.add('Xuất Excel / In danh sách theo quyền', 'P1', ACC_Q2, ['Đăng nhập Q2.', 'Xuất Excel, Xuất file.'], '—',
        ['File chỉ có phiếu của công ty TPSG (và phiếu Q2 tự tạo).'], 293)
S12.add('Xem lịch sử theo quyền', 'P1', [ACC_Q1, P73], ['Đăng nhập Q1.', 'Mở lịch sử 00073.'], '—', ['Xem được các mốc.'], 294)
S12.add('Bị gỡ quyền giữa lúc thao tác', 'P1', [ACC_Q1, 'Quản trị gỡ Vai trò cấp quyền Xem của Q1 khi đang ở danh sách.'],
        ['Bấm sang trang 2.'], '—', ['Danh sách chỉ còn phiếu Q1 tự tạo (phạm vi kiểm lại ở mỗi lần nạp).'], [297, 298])

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'CHỈNH SỬA', S4),
    ('V', 'DUYỆT PHIẾU (LƯU VÀ DUYỆT)', S5),
    ('VI', 'LỊCH SỬ THAY ĐỔI', S6),
    ('VII', 'XEM CHI TIẾT PHIẾU XUẤT HÀNG ĐIỀU CHỈNH KIỂM KÊ', S7),
    ('VIII', 'IN PHIẾU', S8),
    ('IX', 'TÙY CHỈNH CỘT', S9),
    ('X', 'XUẤT DANH SÁCH EXCEL', S10),
    ('XI', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S11),
    ('XII', 'PHÂN QUYỀN', S12),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
check_no_dash_pre(SECTIONS, [])
_ids = ['TC_%02d.%s' % (s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
assert len(_ids) == len(set(_ids)), 'Trùng TC ID'

if __name__ == '__main__':
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='Phiếu xuất hàng điều chỉnh kiểm kê - Cập nhật ngày 18/11/2026',
                module_name='Phiếu xuất hàng điều chỉnh kiểm kê', description_block=DESCRIPTION_BLOCK, sections=SECTIONS,
                loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

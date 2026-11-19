# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu điều chuyển vị trí" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (xác định từ code 09/11/2026): chứng từ có trạng thái (Đang tạo / Đã chuyển), có Tạo mới (Lưu nháp, Lưu và tiếp tục),
Sửa + Xóa (phiếu Đang tạo), bước chốt = nút Điều chuyển (ghi tồn ngay, tương đương duyệt — không có người duyệt riêng), In phiếu / In
dự kiến, Lịch sử. KHÔNG có Khóa, Gửi duyệt riêng, Không duyệt, Hủy, Import (kiểm code: không route / nút) nên bỏ các nhóm đó. Nhóm:
I Hiển thị · II Tìm kiếm & lọc (gồm Cài đặt bộ lọc) · III Thêm mới (gồm popup chọn hàng / vị trí / lô) · IV Chỉnh sửa · V Xóa ·
VI Duyệt phiếu (Điều chuyển) · VII Lịch sử · VIII Xem chi tiết · IX In phiếu (gồm In dự kiến) · X Tùy chỉnh cột · XI Xuất danh sách
Excel · XII Ràng buộc · XIII Phân quyền (cuối). Mỗi case ghi stt checklist nó phủ (ck) — gen_checklist.py đọc CK.
Khuôn: ../phieu-xuat-kho-dieu-chinh-kiem-ke/gen_testcase.py.
Nguồn hành vi (đọc 09/11/2026, nhánh develop cả 2 repo): FE pages/warehouse/position-transfers/**; BE PositionTransfer (Entity /
Controller / StoreRequest / Service / WriteService / PrintService), WarehouseInventoryLockService, PhysicalStockWriter::transferLot.
Số liệu mẫu: dev-hrm 09/11/2026 (DNS Admin — quyền tổng công ty): 943 phiếu (4 Đang tạo, 939 Đã chuyển).
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
MENU = 'Vào phân hệ Kho > menu "Điều chuyển" > bấm "Phiếu điều chuyển vị trí".'
KKVT_MENU = 'Vào phân hệ Kho > menu "Kiểm kho" > "Theo vị trí" > bấm "Kiểm kê theo vị trí".'
KKHH_MENU = 'Vào phân hệ Kho > menu "Kiểm kho" > "Theo vị trí" > bấm "Kiểm kê theo hàng hóa".'
CARD_MENU = 'Vào phân hệ Kho > menu "Báo cáo kho" > bấm "Thẻ kho".'
ADV = 'Bấm Tìm kiếm nâng cao.'
REQ = '"Bắt buộc phải nhập"'
MISS = '"Bạn chưa nhập đầy đủ thông tin."'
CONFIRM = ('"Hàng hóa sẽ được chuyển sang vị trí nhập và cập nhật tồn kho ngay. Phiếu đã điều chuyển không sửa, xóa được. Bạn có '
           'muốn tiếp tục?"')

PRE_LIST = ('Tài khoản DNS Admin (quyền xem theo tổng công ty); hệ thống có 943 phiếu: 4 Đang tạo (PĐCVT-01235, 01231, 01228, 00436), '
            '939 Đã chuyển.')
P1234 = ('Phiếu PĐCVT-01234: Kho "PTT - Phan Trọng Tuệ", Đã chuyển, Người tạo "DNS Admin - HDQT", Ngày tạo 05/11/2026 15:00, Ngày cập '
         'nhật 05/11/2026 15:03, 2 file ảnh; 1 dòng "Mỡ bôi trơn đa năng chịu nhiệt L3 (15kg/xô)" (Model ANOPEC L3 15 KG, Mã '
         'ANOP-ANOPECL315KG, ĐVT Xô 15KG, Vị trí xuất PTT-N1-D6-K7-T1, Lô xuất TPHP-05/10/2026-10974-44676-81-1-46077, Vị trí nhập '
         'PTT-N1-D5-K8-T1, SL 1). Lịch sử 4 mốc: Tạo mới 05/11 15:00; Thay đổi thông tin 15:00; Thay đổi thông tin 15:03; Thay đổi '
         'trạng thái 15:03 Đang tạo sang Đã chuyển.')
P1235 = ('Phiếu PĐCVT-01235: Kho "PTT - Phan Trọng Tuệ", Đang tạo, Ghi chú trống, chưa có file; dòng 1 "Khay inox chữ nhật kích thước '
         '300X400X50" (ĐVT Cái, Vị trí xuất PTT-N1-D1-K1-T1, Lô TPE-30/10/2026-11617-38213-40-1-48721, SL tồn 8, chưa có Vị trí nhập, '
         'SL); dòng 2 "Giá để phụ tùng KT: 700x1690x800mm" (chỉ có ĐVT Cái).')
P1233 = 'Phiếu PĐCVT-01233 (Đã chuyển, Kho LN - Liên Ninh) lập từ phiếu Kiểm kê theo hàng hóa TPE.KKK-01093.'
ACC_L = ('Tài khoản L: có quyền "Điều chuyển vị trí", là thủ kho của kho "PTT - Phan Trọng Tuệ" và "LN - Liên Ninh", không có quyền xem '
         'theo cấp.')
ACC_V1 = 'Tài khoản V1: có quyền "Xem điều chuyển vị trí theo tổng công ty", không có quyền "Điều chuyển vị trí".'
ACC_V2 = 'Tài khoản V2: có quyền "Xem điều chuyển vị trí theo công ty", đang làm việc ở công ty TPSG.'
ACC_V3 = 'Tài khoản V3: có quyền "Xem điều chuyển vị trí theo kho", là thủ kho kho "HP - Hải Phòng" (8 phiếu).'
ACC_N = 'Tài khoản N: không có quyền nào của màn; đã tự lập 1 phiếu PĐCVT-01240 (Đang tạo).'
STOCK = ('Hàng "Giá để phụ tùng KT: 700x1690x800mm" (Mã 2Q-GIADEPHUTUNG, ĐVT Cái) tại kho PTT: vị trí PTT-N1-D1-K1-T1 có lô '
         'TPE-29/10/2026-11613-39025-40-1-48711 tồn 27 và lô TPE-30/10/2026-11616-39025-40-1-48718 tồn 1; không có phiếu nhập chưa '
         'hạch toán tại vị trí.')
PRE_FORM = ACC_L + '\n' + STOCK
TAO = [MENU, 'Bấm "Tạo mới".']
CHON = TAO + ['Chọn Kho = PTT - Phan Trọng Tuệ.', 'Bấm Thêm hàng hóa, bấm tên hàng "Giá để phụ tùng KT: 700x1690x800mm".',
              'Bấm ô Vị trí xuất, chọn PTT-N1-D1-K1-T1.', 'Bấm ô Lô xuất, chọn lô TPE-29/10/2026-11613-39025-40-1-48711.',
              'Bấm ô Vị trí nhập, chọn PTT-N1-D1-K1-T2.', 'Nhập SL = 1.']
DRAFT = 'Phiếu PĐCVT-01241 do L lập ở kho PTT, Đang tạo, Ghi chú "Nháp", 1 dòng đủ cột (Giá để phụ tùng, SL 1), chưa có file.'
PRE_EDIT = ACC_L + '\n' + DRAFT
SUA = [MENU, 'Ở dòng PĐCVT-01241 bấm Sửa (biểu tượng bút chì).']
PKK = ('Phiếu Kiểm kê theo vị trí TPE-KKVT-00142 (Chờ xử lý, kho KTCN - Kỹ thuật công nghệ) còn 1 dòng chênh thiếu: "Vít nở DK16 - '
       'Phụ kiện dùng cho cầu nâng 2 trụ GL-3.5-2E1", Vị trí xuất KTCN-N1-D1-K1-T1, lô TPE-20/10/2025-1692-14260-40-1-15609, SL 2, SL tồn '
       '16.' + chr(10) + 'Tài khoản đang dùng có quyền "Xử lý phiếu kiểm kê vị trí" và "Điều chuyển vị trí".')
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
     'Màn Phiếu điều chuyển vị trí (mã PĐCVT-NNNNN, phân hệ Kho) dùng để chuyển hàng giữa 2 vị trí trong CÙNG một kho theo từng lô: '
     'thủ kho chọn hàng, vị trí xuất, lô xuất, vị trí nhập, số lượng, Lưu nháp (Đang tạo), rồi Điều chuyển (Đã chuyển: trừ tồn lô ở vị trí '
     'xuất, cộng ở vị trí nhập, tổng tồn kho không đổi). Phiếu cũng được lập từ phiếu Kiểm kê theo vị trí / theo hàng hóa cho dòng chênh '
     'thiếu.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Danh sách: phiếu trong phạm vi xem (theo tổng công ty: mọi phiếu; theo công ty: phiếu của công ty + phiếu mình tạo; theo kho: '
     'phiếu của kho mình là thủ kho + phiếu mình tạo; không có quyền: phiếu mình tạo).\n'
     '- 2 trạng thái: Đang tạo (nhãn xám), Đã chuyển (nhãn xanh lá).\n'
     '- Popup Vị trí xuất: vị trí của kho còn tồn hàng; popup Vị trí nhập: mọi vị trí của kho; popup Lô: lô còn tồn tại vị trí xuất.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu ngoài phạm vi: không có trong danh sách, mở đường link ra trang không tìm thấy.\n'
     '- Vị trí đang kiểm kho, vị trí trùng vị trí còn lại của dòng, lô hết tồn: hiện mờ, không chọn được.\n'
     '- Màn không có Khóa / Mở khóa, Gửi duyệt riêng, Không duyệt, Hủy, In danh sách, Import.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo ngày tạo phiếu, lấy trọn hai ngày biên; xuất Excel ghi dòng "Từ ngày … đến '
                                        'ngày …".'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Phiếu (1 kho) > dòng hàng (hàng, ĐVT, vị trí xuất, lô xuất, vị trí nhập, SL).\n'
     '- Vị trí thuộc cấu trúc Nhà > Dãy > Khoang > vị trí của kho.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Kiểm tồn khi Điều chuyển cộng dồn SL (quy về ĐVT cơ sở) của các dòng cùng hàng + vị trí + lô và cùng hàng + vị trí.\n'
     '- Tồn vị trí khả dụng = tồn vị trí trừ SL các phiếu nhập kho chưa hạch toán tại vị trí đó.'),
    ('7. Phân quyền cấp',
     '- Điều chuyển vị trí: nút Tạo mới, lập phiếu cho kho mình là thủ kho.\n'
     '- Xem điều chuyển vị trí theo tổng công ty: mọi phiếu; có ô Công ty, Phòng ban.\n'
     '- Xem điều chuyển vị trí theo công ty: phiếu công ty đang làm việc + mình tạo; có ô Phòng ban.\n'
     '- Xem điều chuyển vị trí theo kho: phiếu của kho mình là thủ kho + mình tạo.\n'
     '- Sửa / Xóa / Điều chuyển phiếu Đang tạo: ai xem được phiếu đều làm được (giữ như hệ thống cũ).'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là khoảng số thứ tự trang đang xem, N là tổng phiếu khớp bộ lọc trong phạm vi xem.\n'
     '- Cột SL tồn trên form = tồn của lô tại vị trí xuất chia hệ số ĐVT (lập từ phiếu kiểm kê: tồn của cả lô).'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: L (lập phiếu, thủ kho PTT / LN), V1, V2, V3 (xem theo cấp), N (không quyền), DNS Admin.\n'
     '- Lưu ý: Điều chuyển GHI TỒN NGAY, không hoàn tác; chạy trên dữ liệu thử.\n'
     '- Lưu ý: Lưu nháp CHỈ bắt Kho; Ghi chú, File đính kèm và các cột của dòng chỉ bắt khi Điều chuyển (các ô vẫn có dấu *).\n'
     '- Lưu ý: SL lưu nháp chỉ giữ phần nguyên (1,5 lưu thành 1).\n'
     '- Màn Tạo / Sửa / Chi tiết là TRANG riêng, không phải cửa sổ nổi.'),
]

SCREEN = ListScreen(menu=MENU, title='Danh sách phiếu điều chuyển vị trí', total=943, quick_label='mã phiếu',
                    quick_sample='PĐCVT-01234', quick_hit='phiếu PĐCVT-01234',
                    filters=[('Trạng thái', 'Đang tạo'), ('Kho', 'PTT - Phan Trọng Tuệ')])

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Tiêu đề màn hình', 'P0', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Thanh tiêu đề, tab và tiêu đề bảng: "Danh sách phiếu điều chuyển vị trí".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE_LIST + '\nDNS Admin có quyền "Điều chuyển vị trí".',
       [MENU, 'Quan sát khối bộ lọc, thanh công cụ, cột Hành động.'], '—',
       ['Khối "Bộ lọc danh sách": ô tìm nhanh (gợi ý "Tìm theo mã phiếu"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
        'Thanh công cụ: Tạo mới, Xuất Excel, nút biểu tượng cột; không có In danh sách.',
        'Cột Hành động: dòng Đang tạo có Sửa, Xóa, Lịch sử; dòng Đã chuyển có In, Lịch sử.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 10 cột: STT, Mã phiếu, Ngày tạo, Kho, Phiếu kiểm kê, Trạng thái, Người tạo, Ngày cập nhật, Người cập nhật, Hành động.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 10/10 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp phiếu', 'P0', [PRE_LIST, P1234], [MENU, 'Đối chiếu dòng PĐCVT-01234.'], '—',
       ['Ngày tạo "05/11/2026 15:00", Kho "PTT - Phan Trọng Tuệ", Phiếu kiểm kê trống, nhãn xanh lá "Đã chuyển".',
        'Người tạo / Người cập nhật "DNS Admin - HDQT", Ngày cập nhật "05/11/2026 15:03".'], 6)
S1.add('Liên kết Phiếu kiểm kê mở ở tab mới', 'P0', [PRE_LIST, P1233], [MENU, 'Ở dòng PĐCVT-01233 bấm "TPE.KKK-01093".'], '—',
       ['Mở chi tiết phiếu Kiểm kê theo hàng hóa TPE.KKK-01093 ở TAB MỚI.', 'Tab danh sách giữ nguyên trang, bộ lọc.'], 6)
S1.add('Trạng thái bản ghi', 'P0', PRE_LIST, [MENU, 'Quan sát cột Trạng thái của PĐCVT-01235 và PĐCVT-01234.'], '—',
       ['01235: nhãn xám "Đang tạo"; 01234: nhãn xanh lá "Đã chuyển".'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', ['Tài khoản mới, không có quyền nào, chưa lập phiếu nào.'], ['Đăng nhập.', MENU], '—',
       ['Bảng hiện "Không có dữ liệu phù hợp.".', 'Không báo lỗi.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'],
       'Ô tìm nhanh: ZZZ999', ['Bảng hiện "Không có dữ liệu phù hợp.".', 'Không báo lỗi.'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 20 phiếu, tự về trang 1, "Hiển thị 1–20 / 943".', 'Ô có các lựa chọn 5, 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–20 / 943".', 'Bước 3: "Hiển thị 1–10 / 943".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—',
       ['Bước 2: trang 95, "Hiển thị 941–943 / 943".', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang 95 quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2, rồi trang 95.'], '—',
       ['Trang 2: STT 11–20; trang 95: STT 941–943.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 3.', ADV, 'Chọn Trạng thái = Đang tạo.'],
       'Trạng thái: Đang tạo', ['Tự nạp lại ở trang 1; "Hiển thị 1–4 / 4".'], 17)
S1.add('Thứ tự mặc định', 'P0', PRE_LIST, [MENU], '—',
       ['Phiếu tạo mới nhất ở trên: PĐCVT-01235 (07/11/2026 09:15), rồi 01234, 01233…', 'Không cột nào hiện mũi tên đang sắp.'], 19)
S1.add('Sắp xếp tăng dần theo Mã phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Mã phiếu.'], '—',
       ['PĐCVT-00001 ở trên cùng, tăng dần; mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Mã phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Mã phiếu 2 lần.'], '—',
       ['PĐCVT-01235 trên cùng, giảm dần; mũi tên xuống.'], 21)
S1.add('Sắp xếp theo Kho', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Kho.', 'Bấm lần nữa.'], '—',
       ['Lần 1: tên kho từ A đến Z; lần 2: từ Z đến A.'], 20)
S1.add('Cột Ngày tạo / Ngày cập nhật không sắp xếp', 'P1', PRE_LIST, [MENU, 'Bấm tiêu đề Ngày tạo, Ngày cập nhật.'], '—',
       ['Không có biểu tượng sắp xếp, thứ tự không đổi (vẫn mới nhất trên).'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Ngày tạo, Phiếu kiểm kê, Trạng thái, Người tạo, Người cập nhật, Hành động.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Mã phiếu (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 bắt đầu PĐCVT-00011, tiếp tục tăng dần.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 3.', 'Bấm tiêu đề Kho.'], '—', ['Về trang 1.'], 25)
S1.add('Mở màn từ số chứng từ ở Thẻ kho', 'P1', [PRE_LIST, P1234],
       [CARD_MENU, 'Lọc hàng ANOP-ANOPECL315KG, kho PTT - Phan Trọng Tuệ.', 'Bấm số chứng từ PĐCVT-01234.'],
       '—', ['Mở màn "Chi tiết phiếu điều chuyển vị trí: PĐCVT-01234".'], 1)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo mã phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "PĐCVT-01234", bấm Tìm kiếm.'], 'Ô tìm nhanh: PĐCVT-01234',
       ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần mã phiếu', 'P0', PRE_LIST, [MENU, 'Nhập "0123", bấm Tìm kiếm.'], 'Ô tìm nhanh: 0123',
       ['Còn 7 phiếu: PĐCVT-01230 đến 01235 và PĐCVT-00123.'], 27)
S2.add('Ô tìm nhanh không tìm theo phiếu kiểm kê / kho', 'P1', PRE_LIST, [MENU, 'Nhập "TPE.KKK-01093", bấm Tìm kiếm.'], '—',
       ['"Không có dữ liệu phù hợp." (ô tìm nhanh chỉ tìm theo mã phiếu).'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "pđcvt-01234", bấm Tìm kiếm.'], '—',
       ['Ra phiếu PĐCVT-01234 như khi gõ chữ hoa.'], 28)
S2.add('Có dấu / không dấu', 'P2', PRE_LIST, [MENU, 'Nhập "PDCVT-01234" (chữ D không gạch), bấm Tìm kiếm.'], '—',
       ['"Không có dữ liệu phù hợp." (chữ Đ và D không được coi là một).', 'Lưu ý: nhập đúng "PĐCVT" để tìm.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; % được hiểu là ký tự đại diện nên ra cả 943 phiếu.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  PĐCVT-01234  ", bấm Tìm kiếm.'], '—',
       ['Ra phiếu PĐCVT-01234.'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "PĐCVT-01234", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Hiện lại đủ 943 phiếu.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST,
       [MENU, 'Nhập "PĐCVT-01234", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'], '—',
       ['Cả 2 cách đều ra phiếu PĐCVT-01234, về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['Các ô Trạng thái, Kho, Người tạo, Hàng hóa, Ngày tạo, Công ty, Phòng ban đều trống.', 'Đủ 943 phiếu.'], 36)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đang tạo.'], '—',
       ['Ô có 2 lựa chọn: Đang tạo, Đã chuyển.', 'Còn 4 phiếu: PĐCVT-01235, 01231, 01228, 00436; lọc ngay khi chọn.'], 37)
S2.add('Lọc Kho', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = HP - Hải Phòng.'], '—',
       ['Ô Kho liệt kê mọi kho dạng "Mã kho - Tên kho".', 'Còn 8 phiếu (có PĐCVT-01231).'], 37)
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = DNS Admin.'], '—',
       ['Ô liệt kê toàn bộ nhân viên (kể cả người chưa tạo phiếu).', 'Còn 9 phiếu PĐCVT-01227 đến 01235.'], 37)
S2.add('Lọc Hàng hóa theo tên', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "Khay inox" vào ô Hàng hóa.', 'Bấm Tìm kiếm.'], '—',
       ['Gõ xong chưa bấm Tìm kiếm: danh sách chưa đổi.', 'Sau Tìm kiếm còn 8 phiếu có dòng hàng tên chứa "Khay inox" (có phiếu nháp '
        'PĐCVT-01235).'], 37)
S2.add('Lọc Hàng hóa theo mã', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "2Q-INOX300" vào ô Hàng hóa, bấm Tìm kiếm.'], '—',
       ['Còn 3 phiếu: PĐCVT-01235, 01234, 00776.'], 37)
S2.add('Lọc Ngày tạo lấy trọn ngày biên', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày tạo 23/10/2026 – 24/10/2026.'], '—',
       ['Còn 4 phiếu: PĐCVT-01230 (24/10 15:39), 01229 (24/10 09:45), 01228, 01227 (23/10).', 'Bỏ trống ngày cuối vẫn lọc được.'], 37)
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = PTT - Phan Trọng Tuệ.', 'Chọn Trạng thái = Đang tạo.'],
       '—', ['Còn 3 phiếu: PĐCVT-01235, 01228, 00436.'], 38)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST,
       [MENU, 'Nhập "PĐCVT-01234", bấm Tìm kiếm.', ADV, 'Chọn Trạng thái = Đang tạo.'], '—',
       ['"Không có dữ liệu phù hợp." vì 01234 đã Đã chuyển.'], [39, 40])
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = PTT - Phan Trọng Tuệ.', 'Bấm trang cuối.'], '—',
       ['Dòng "Hiển thị" ghi tổng 412.', 'Trang 42 hiện "Hiển thị 411–412 / 412", STT liên tục.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Trạng thái = Đang tạo.', ['Bấm tiêu đề Mã phiếu.'], '—',
       ['Chỉ 4 phiếu Đang tạo được sắp (00436 đầu); bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "PĐCVT", lọc Kho, Trạng thái, sắp Mã phiếu, ở trang 2.',
       ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống, bỏ sắp xếp, nạp lại trang 1, đủ 943 phiếu.'], 44)
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.raw(org_cases(SCREEN, len(S2) + 1), [[37], [37], [37]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Đang tạo, chưa mở màn chi tiết.'],
       ['Nhấn F5.'], '—', ['Bộ lọc trở về trống, đủ 943 phiếu (bộ lọc chỉ nhớ khi đi vào màn chi tiết / sửa của màn).'], 46)
S2.add('Ô Công ty chỉ có với quyền tổng công ty', 'P1', [ACC_V2], ['Đăng nhập V2.', MENU, ADV], '—',
       ['Không có ô Công ty, chỉ có ô Phòng ban.'], 37)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Hàng hóa, bấm Lưu.'], '—',
       ['Cửa sổ liệt kê 6 mục: Trạng thái, Kho, Người tạo, Hàng hóa, Ngày tạo, Công ty – Phòng ban.',
        'Báo "Cập nhật thành công"; khối Tìm kiếm nâng cao không còn ô Hàng hóa.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Đang tạo.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Trạng thái, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị bỏ, nạp lại đủ 943 phiếu.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Hàng hóa.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Hàng hóa vẫn ẩn.', 'Bước 2: tích đủ 6 mục, Hàng hóa hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Ngày tạo lên đầu, bấm Lưu.'], '—',
       ['Ô Ngày tạo đứng đầu khối Tìm kiếm nâng cao; giữ sau khi đăng nhập lại.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo mới từ danh sách', 'P0', PRE_FORM, ['Đăng nhập L.'] + TAO, '—',
       ['Mở TRANG "Tạo phiếu điều chuyển vị trí", tab cùng tiêu đề.'], 49)
S3.add('Mở từ phiếu Kiểm kê theo vị trí', 'P0', [PKK], [KKVT_MENU, 'Ở dòng TPE-KKVT-00142 bấm biểu tượng "Tạo phiếu điều chuyển vị trí".'],
       '—', ['Mở màn Tạo: ô Phiếu kiểm kê "TPE-KKVT-00142" (liên kết), Kho "KTCN - Kỹ thuật công nghệ" khóa.',
             'Bảng có 1 dòng Vít nở DK16: ĐVT Cái, Vị trí xuất KTCN-N1-D1-K1-T1, lô, SL tồn 16, SL 2 đều khóa; Vị trí nhập trống "Chọn vị '
             'trí nhập".', 'Không có nút Thêm hàng hóa, Lưu và tiếp tục.'], [49, 53, 269])
S3.add('Mở từ chi tiết phiếu kiểm kê', 'P1', [PKK], [KKVT_MENU, 'Mở chi tiết TPE-KKVT-00142.', 'Bấm "Tạo phiếu điều chuyển vị trí".'],
       '—', ['Mở cùng form như từ danh sách phiếu kiểm kê.'], 49)
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải "<tên L> - <ngày giờ hiện tại>".', 'Không có ô Mã phiếu (mã tự sinh khi lưu).'], 50)
S3.add('Các trường, khối và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Kho, Ghi chú (gợi ý "Nhập ghi chú").',
        'Khối "File đính kèm" có nút "Thêm tài liệu"; khối "Chi tiết" có nút "Thêm hàng hóa", cột STT, Tên hàng hóa, Model, Mã hàng '
        'hóa, ĐVT, Vị trí xuất, Lô xuất, SL tồn, Vị trí nhập, SL, Hành động.',
        'Chân màn: Lưu nháp, Điều chuyển, Lưu và tiếp tục, In dự kiến, Quay lại.'], [51, 54])
S3.add('Trường bắt buộc / không bắt buộc', 'P0', PRE_FORM, TAO + ['Quan sát dấu *.'], '—',
       ['Kho, Ghi chú, File đính kèm, Chi tiết, ĐVT, Vị trí xuất, Lô xuất, Vị trí nhập, SL có dấu *.',
        'Lưu ý: Lưu nháp chỉ bắt Kho; các ô còn lại chỉ bắt khi Điều chuyển.'], 52)
S3.add('Giá trị mặc định', 'P0', PRE_FORM, TAO, '—',
       ['Kho trống (gợi ý "Chọn kho"); Ghi chú trống; chưa có file; bảng ghi "Không có dữ liệu".',
        'Ô Kho chỉ liệt kê PTT - Phan Trọng Tuệ, LN - Liên Ninh (kho L là thủ kho).'], 53)
S3.add('Thêm hàng hóa khi chưa chọn Kho', 'P0', PRE_FORM, TAO + ['Bấm Thêm hàng hóa.'], '—',
       ['Ô Kho viền đỏ ' + REQ + '; thông báo "Vui lòng chọn kho trước khi thêm hàng hóa."; không mở popup.'], [61, 70])
S3.add('Popup Thêm hàng hóa chỉ hàng còn tồn', 'P0', PRE_FORM, TAO + ['Chọn Kho = PTT - Phan Trọng Tuệ.', 'Bấm Thêm hàng hóa.'], '—',
       ['Popup "Thêm hàng hóa" chỉ liệt kê hàng còn tồn trong kho PTT.', 'Bấm tên "Giá để phụ tùng KT: 700x1690x800mm": thêm 1 dòng, ĐVT '
        'mặc định Cái, báo "Thêm thành công.".'], [53, 269])
S3.add('Thêm trùng hàng đã có', 'P2', PRE_FORM, CHON[:3] + ['Bấm Thêm hàng hóa, chọn lại cùng hàng.'], '—',
       ['Bảng có 2 dòng cùng hàng (cho phép, mỗi dòng 1 vị trí / lô khác nhau).'], 286)
S3.add('Popup Chọn vị trí xuất', 'P0', PRE_FORM, CHON[:3] + ['Bấm ô Vị trí xuất.'], '—',
       ['Popup "Chọn vị trí xuất": ô tìm "Tìm theo mã vị trí", ô Nhà, Dãy, Khoang, nút Tìm kiếm, Làm mới.',
        'Bảng STT, Vị trí, Nhà, Dãy, Khoang, Tồn; chỉ vị trí còn tồn hàng (PTT-N1-D1-K1-T1, Tồn "28 Cái").',
        'Bấm dòng: điền "PTT-N1-D1-K1-T1" vào ô, đóng popup.'], 51)
S3.add('Lọc Nhà / Dãy / Khoang phân cấp', 'P1', PRE_FORM, CHON[:3] + ['Bấm ô Vị trí nhập sau khi đã có Vị trí xuất.',
       'Chọn Nhà = Nhà 1, mở ô Dãy.', 'Chọn Dãy, rồi đổi Nhà khác.'], '—',
       ['Chọn là tìm ngay; ô Dãy chỉ còn dãy của Nhà 1.', 'Đổi Nhà thì Dãy không thuộc Nhà mới bị bỏ.'], 37)
S3.add('Ô tìm vị trí chỉ theo mã', 'P2', PRE_FORM, CHON[:3] + ['Mở popup Vị trí nhập, nhập "Tầng 1", bấm Tìm kiếm.',
       'Nhập "PTT-N1-D1", bấm Tìm kiếm.'], '—', ['Bước 2: "Không có vị trí nào phù hợp.".', 'Bước 3: còn vị trí có mã chứa "PTT-N1-D1".'], 27)
S3.add('Chọn Lô / Vị trí nhập khi chưa có Vị trí xuất', 'P1', PRE_FORM, CHON[:3] + ['Bấm ô Lô xuất.', 'Bấm ô Vị trí nhập.'], '—',
       ['Không mở popup; dưới ô Vị trí xuất: "Vui lòng chọn vị trí xuất trước.".'], 70)
S3.add('Popup Chọn lô xuất', 'P0', PRE_FORM, CHON[:4] + ['Bấm ô Lô xuất.'], '—',
       ['Popup "Chọn lô xuất": ô "Tìm theo số lô"; bảng STT, Lô, Ngày nhập, Tồn: 2 lô (tồn 27 và 1).',
        'Chọn lô ...-48711: ô Lô xuất điền số lô, cột SL tồn = 27.'], 51)
S3.add('Đổi Vị trí xuất thì bỏ lô đã chọn', 'P0', PRE_FORM, CHON[:5] + ['Mở lại popup Vị trí xuất, chọn vị trí khác.'], '—',
       ['Ô Lô xuất và SL tồn bị xóa, phải chọn lại lô.'], 272)
S3.add('Vị trí trùng hoặc đang kiểm kho hiện mờ', 'P1', [PRE_FORM, 'Vị trí PTT-N1-D2-K1-T1 thuộc phiếu kiểm kê theo vị trí Đang kiểm.'],
       CHON[:5] + ['Bấm ô Vị trí nhập.', 'Rê chuột dòng PTT-N1-D1-K1-T1 và PTT-N1-D2-K1-T1.'], '—',
       ['Hai dòng mờ, không chọn được; rê chuột hiện "Trùng vị trí xuất / nhập" và "Đang kiểm kho".'], 70)
S3.add('Lưu nháp với dữ liệu hợp lệ đầy đủ', 'P0', PRE_FORM, CHON + ['Nhập Ghi chú, thêm file.', 'Bấm Lưu nháp.'],
       ['Ghi chú: Chuyển hàng sang vị trí mới', FILE],
       ['Báo "Lưu thành công.", về danh sách.', 'Dòng mới trên cùng mã PĐCVT-NNNNN kế tiếp, Kho PTT - Phan Trọng Tuệ, Người tạo L, nhãn '
        'xám "Đang tạo".'], [55, 79, 85])
S3.add('Lưu nháp chỉ với trường bắt buộc', 'P0', PRE_FORM, TAO + ['Chọn Kho = LN - Liên Ninh.', 'Bấm Lưu nháp.'], 'Ghi chú, File, Chi tiết: trống',
       ['Lưu được, phiếu Đang tạo, không có dòng hàng.'], [56, 57])
S3.add('Dữ liệu sau lưu', 'P0', PRE_FORM, CHON + ['Bấm Lưu nháp.', 'Bấm mã phiếu vừa tạo.'], '—',
       ['Màn chi tiết đúng Kho PTT, dòng Giá để phụ tùng: PTT-N1-D1-K1-T1, lô ...-48711, PTT-N1-D1-K1-T2, SL 1.'], 58)
S3.add('Trạng thái mặc định sau lưu', 'P0', PRE_FORM, CHON + ['Bấm Lưu nháp.', 'Mở Thẻ kho hàng 2Q-GIADEPHUTUNG kho PTT.'], '—',
       ['Phiếu ở trạng thái Đang tạo (nhãn xám).', 'Thẻ kho không có dòng mới; tồn lô ...-48711 tại PTT-N1-D1-K1-T1 vẫn 27.'], 59)
S3.add('Lịch sử tạo', 'P1', PRE_FORM, CHON + ['Bấm Lưu nháp.', 'Ở dòng phiếu mới bấm Lịch sử.'], '—',
       ['Có 1 mốc "Tạo mới", người thực hiện L.'], [60, 176])
S3.add('Lưu nháp khi chưa chọn Kho', 'P0', PRE_FORM, TAO + ['Bấm Lưu nháp.'], '—',
       ['Ô Kho viền đỏ, dưới ô ' + REQ + '.', 'Thông báo ' + MISS + '; không lưu.'], [61, 70, 80])
S3.add('SL vượt trần / số âm', 'P1', PRE_FORM, CHON[:6] + ['Nhập SL = 1000000000.', 'Bấm Lưu nháp.'], 'SL: 1000000000',
       ['Dưới ô SL: "Giá trị nhập vào không được vượt quá 999,999,999.", thông báo ' + MISS + '.', 'Ô SL không nhận chữ, dấu âm.'],
       [62, 74, 81])
S3.add('SL có phần thập phân khi lưu nháp', 'P2', PRE_FORM, CHON[:6] + ['Nhập SL = 1,5.', 'Bấm Lưu nháp, mở lại phiếu.'], 'SL: 1,5',
       ['Ô nhận tối đa 2 chữ số thập phân.', 'Lưu ý: phiếu nháp lưu SL = 1 (chỉ giữ phần nguyên, như hệ thống cũ).'], 62)
S3.add('Ghi chú tối đa 255 ký tự', 'P1', PRE_FORM, CHON + ['Dán chuỗi 300 ký tự vào Ghi chú.'], 'Ghi chú: 300 ký tự',
       ['Ô chỉ nhận 255 ký tự đầu (không gõ thêm được).'], [66, 74, 81])
S3.add('Ghi chú đúng 255 ký tự', 'P1', PRE_FORM, CHON + ['Nhập Ghi chú đúng 255 ký tự.', 'Bấm Lưu nháp.'], 'Ghi chú: 255 ký tự',
       ['Lưu được, hiển thị đủ 255 ký tự.'], 65)
S3.add('Ghi chú 1 ký tự', 'P2', PRE_FORM, CHON + ['Nhập Ghi chú "a".', 'Bấm Lưu nháp.'], 'Ghi chú: a', ['Lưu được.'], 64)
S3.add('Ký tự đặc biệt trong Ghi chú', 'P2', PRE_FORM, CHON + ['Nhập Ghi chú "<b>Test</b> & @#$%".', 'Bấm Lưu nháp.'], '—',
       ['Lưu được; màn chi tiết và bản in hiện nguyên chuỗi, không in đậm.'], 63)
S3.add('Ghi chú khoảng trắng đầu / cuối', 'P2', PRE_FORM, CHON + ['Nhập Ghi chú "  Chuyển hàng  ".', 'Bấm Lưu nháp.'], '—',
       ['Lưu được; khoảng trắng đầu / cuối không làm lỗi.'], 68)
S3.add('Ghi chú chỉ có khoảng trắng khi Lưu nháp', 'P2', PRE_FORM, CHON + ['Nhập Ghi chú "   ".', 'Bấm Lưu nháp.'], '—',
       ['Lưu được (Lưu nháp không bắt Ghi chú).'], 69)
S3.add('File sai định dạng', 'P1', PRE_FORM, CHON + ['Bấm Thêm tài liệu, chọn file "bang.xlsx".'], 'File: bang.xlsx',
       ['Báo lỗi định dạng, file không được thêm.', 'Chỉ nhận pdf, png, jpg, jpeg.'], [62, 70])
S3.add('File quá 20 MB', 'P2', PRE_FORM, CHON + ['Bấm Thêm tài liệu, chọn file pdf 25 MB.'], 'File: 25 MB',
       ['Báo vượt dung lượng; file không được thêm.'], 62)
S3.add('Không có trường duy nhất để trùng', 'P1', PRE_FORM, CHON + ['Bấm Lưu nháp.', 'Tạo mới lại đúng dữ liệu như trên, Lưu nháp.'],
       '—', ['Cả 2 phiếu đều lưu được, mã PĐCVT khác nhau (phiếu không có trường duy nhất, mã tự sinh).'], [67, 75, 82])
S3.add('Kho không phải kho mình là thủ kho', 'P1', [ACC_L, 'Kho HP - Hải Phòng không phải kho của L.'],
       TAO + ['Dùng đường link màn Tạo do người khác gửi đã chọn kho HP, bấm Lưu nháp.'], '—',
       ['Dưới ô Kho: "Bạn không phải thủ kho của kho này."; không lưu.'], 67)
S3.add('Vị trí xuất trùng Vị trí nhập', 'P1', PRE_FORM, CHON[:5] + ['Mở popup Vị trí nhập (dòng trùng bị mờ, không chọn được).'], '—',
       ['Không chọn được vị trí trùng.', 'Nếu dữ liệu cũ có trùng: dưới ô Vị trí nhập "Không thể xuất và nhập cùng một vị trí!".'], 70)
S3.add('Lỗi biến mất sau khi sửa', 'P1', PRE_FORM, TAO + ['Bấm Lưu nháp (báo lỗi Kho).', 'Chọn Kho.'], '—',
       ['Chữ đỏ dưới ô Kho biến mất ngay khi chọn.'], 71)
S3.add('SL tồn đỏ khi SL vượt tồn', 'P1', PRE_FORM, CHON[:6] + ['Chọn lô tồn 1, nhập SL = 5.'], 'SL: 5',
       ['Cột SL tồn "1" chữ đỏ đậm.', 'Lưu nháp vẫn cho lưu; chặn khi Điều chuyển.'], 70)
S3.add('Đổi Kho khi đã có hàng', 'P0', PRE_FORM, CHON + ['Đổi Kho sang LN - Liên Ninh.', 'Bấm Hủy.', 'Đổi lại sang LN, bấm Đổi kho.'],
       '—', ['Hộp "Đổi kho": "Nếu bạn thay đổi kho, danh sách hàng hóa sẽ được làm mới. Bạn có chắc chắn muốn thực hiện?".',
             'Hủy: giữ kho PTT và các dòng; Đổi kho: bảng về "Không có dữ liệu".'], 99)
S3.add('Xóa dòng hàng', 'P1', PRE_FORM, CHON + ['Bấm biểu tượng thùng rác ở dòng 1.'], '—',
       ['Dòng bị xóa ngay, không hỏi; bảng về "Không có dữ liệu".'], 99)
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, CHON + ['Bấm Lưu và tiếp tục.'], '—',
       ['Báo "Lưu thành công.", ở lại màn Tạo với form trống (Kho trống, bảng rỗng).'], [72, 76, 77])
S3.add('Lưu và tiếp tục khi thiếu Kho', 'P1', PRE_FORM, TAO + ['Bấm Lưu và tiếp tục.'], '—',
       [REQ + ' dưới ô Kho; không lưu, form giữ nguyên.'], [73, 74])
S3.add('Đóng sau Lưu và tiếp tục', 'P2', PRE_FORM, CHON + ['Bấm Lưu và tiếp tục.', 'Bấm Quay lại.'], '—',
       ['Về danh sách ngay (form trống, không hỏi); phiếu vừa lưu có trong danh sách.'], 78)
S3.add('Lưu và tiếp tục không có khi lập từ phiếu kiểm kê', 'P2', [PKK], [KKVT_MENU, 'Mở form tạo từ TPE-KKVT-00142.'], '—',
       ['Chân màn chỉ có Lưu nháp, Điều chuyển, In dự kiến, Quay lại.'], 54)
S3.add('Lưu nháp: màn sau khi lưu và trường làm mới', 'P2', PRE_FORM, CHON + ['Bấm Lưu nháp.', 'Bấm Tạo mới lại.'], '—',
       ['Màn là trang: Lưu nháp xong về danh sách.', 'Mở Tạo mới lại thì form trống.'], [83, 84])
S3.add('Quay lại khi chưa nhập gì', 'P1', PRE_FORM, TAO + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 93)
S3.add('Quay lại khi đã chọn / nhập', 'P0', PRE_FORM, CHON + ['Bấm Quay lại.'], '—',
       ['Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" với nút Thoát, Ở lại.'], [94, 95])
S3.add('Chọn Thoát', 'P1', PRE_FORM, CHON + ['Bấm Quay lại.', 'Bấm Thoát.'], '—', ['Về danh sách, không tạo phiếu.'], 96)
S3.add('Chọn Ở lại', 'P1', PRE_FORM, CHON + ['Bấm Quay lại.', 'Bấm Ở lại.'], '—',
       ['Ở lại form, dữ liệu đã chọn / nhập giữ nguyên.'], 97)
S3.add('Nhập rồi xóa hết', 'P2', PRE_FORM, TAO + ['Nhập Ghi chú rồi xóa hết.', 'Bấm Quay lại.'], '—',
       ['Về danh sách ngay, không hỏi.'], 98)
S3.add('Để màn lâu không thao tác', 'P2', [PRE_FORM, 'Đã mở màn, để nguyên 30 phút.'], CHON + ['Bấm Lưu nháp.'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên, về màn đăng nhập, không lưu.'], 100)
S3.add('Bấm Lưu nháp liên tục', 'P1', PRE_FORM, CHON + ['Bấm Lưu nháp 3 lần thật nhanh.'], '—',
       ['Nút khóa trong lúc lưu; chỉ tạo 1 phiếu.'], 101)
S3.add('Hai tab cùng lập từ 1 phiếu kiểm kê', 'P1', [PKK, 'Tab 1 và tab 2 cùng mở form tạo từ TPE-KKVT-00142, chọn Vị trí nhập.'],
       ['Tab 1 bấm Điều chuyển, xác nhận.', 'Tab 2 bấm Điều chuyển, xác nhận.'], '—',
       ['Tab 1 thành công.', 'Tab 2 báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang" (phiếu kiểm kê không còn dòng cần điều '
        'chuyển); không ghi tồn lần 2.'], 102)
S3.add('Không có quyền Điều chuyển vị trí', 'P1', [ACC_V1], ['Đăng nhập V1.', MENU], '—',
       ['Không có nút Tạo mới.', 'Mở form từ phiếu kiểm kê bằng đường link: chuyển trang không tìm thấy.'], [52, 295])

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
S4.add('Mở màn Sửa từ cột Hành động', 'P0', PRE_EDIT, ['Đăng nhập L.'] + SUA, '—',
       ['Mở trang "Sửa phiếu điều chuyển vị trí: PĐCVT-01241".'], 103)
S4.add('Mở màn Sửa từ màn chi tiết', 'P1', PRE_EDIT, [MENU, 'Bấm PĐCVT-01241.', 'Bấm Sửa ở chân màn.'], '—',
       ['Mở màn Sửa của phiếu.'], 103)
S4.add('Dữ liệu điền đúng', 'P0', [ACC_L, P1235], [MENU, 'Ở dòng PĐCVT-01235 bấm Sửa.'], '—',
       ['Kho "PTT - Phan Trọng Tuệ" (khóa), Ghi chú trống.', 'Dòng 1 đủ ĐVT, Vị trí xuất, Lô, SL tồn 8; dòng 2 chỉ có ĐVT, các ô '
        '"Chọn vị trí xuất", "Chọn lô xuất" trống.'], 104)
S4.add('Trường được / không được sửa', 'P0', PRE_EDIT, SUA, '—',
       ['Kho là ô khóa, không đổi được.', 'Ghi chú, File đính kèm, dòng hàng (thêm / xóa / ĐVT / vị trí / lô / SL) sửa được.'], 105)
S4.add('Các nút', 'P1', PRE_EDIT, SUA, '—', ['Chân màn: Lưu nháp, Điều chuyển, In dự kiến, Quay lại; không có Lưu và tiếp tục.'], 106)
S4.add('Sửa Ghi chú', 'P0', PRE_EDIT, SUA + ['Sửa Ghi chú thành "Nháp lần 2".', 'Bấm Lưu nháp.'], 'Ghi chú: Nháp lần 2',
       ['Báo "Lưu thành công.", về danh sách; phiếu vẫn Đang tạo.', 'Chi tiết hiện Ghi chú mới.'], [107, 110])
S4.add('Sửa nhiều thông tin', 'P1', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Đổi SL dòng 1 thành 2.', 'Thêm file bien_ban.pdf.', 'Bấm Lưu nháp.'],
       FILE, ['Lưu được; Ghi chú, SL 2 và file đều được lưu.'], 108)
S4.add('Ngày / người cập nhật', 'P0', PRE_EDIT, SUA + ['Sửa Ghi chú, Lưu nháp.'], '—',
       ['Dòng PĐCVT-01241 ở danh sách: Ngày cập nhật = thời điểm lưu, Người cập nhật là tên L kèm mã phòng.'], 111)
S4.add('Giữ nguyên giá trị khi Lưu nháp không đổi', 'P1', PRE_EDIT, SUA + ['Không đổi gì, bấm Lưu nháp.'], '—',
       ['Lưu được, dữ liệu không đổi.', 'Lịch sử không có mốc "Thay đổi thông tin" mới.'], [109, 125, 182])
S4.add('Lịch sử sau khi sửa', 'P0', PRE_EDIT, SUA + ['Sửa Ghi chú thành "Nháp lần 2", Lưu nháp.', 'Bấm Lịch sử ở dòng phiếu.'], '—',
       ['Có mốc "Thay đổi thông tin" người thực hiện L, Ghi chú "Nháp" sang "Nháp lần 2".'], [112, 177])
S4.add('Ghi chú vượt 255 ký tự', 'P1', PRE_EDIT, SUA + ['Dán chuỗi 300 ký tự.'], '—', ['Ô chỉ nhận 255 ký tự.'], [114, 115])
S4.add('Bỏ trống Ghi chú khi Lưu nháp', 'P1', PRE_EDIT, SUA + ['Xóa hết Ghi chú.', 'Bấm Lưu nháp.'], '—',
       ['Lưu được (Lưu nháp không bắt Ghi chú).'], 113)
S4.add('Bỏ trống Ghi chú khi Điều chuyển từ màn Sửa', 'P0', PRE_EDIT, SUA + ['Xóa hết Ghi chú.', 'Bấm Điều chuyển, xác nhận.'], '—',
       ['Ghi chú viền đỏ ' + REQ + '; khối File ' + REQ + '; thông báo ' + MISS + '; không ghi tồn.'], [113, 117])
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P2', PRE_EDIT, SUA + ['Xóa Ghi chú, bấm Điều chuyển, xác nhận (báo lỗi).', 'Nhập lại Ghi chú.'],
       '—', ['Chữ đỏ dưới Ghi chú biến mất ngay.'], 118)
S4.add('Không có trường duy nhất để trùng', 'P2', PRE_EDIT, SUA, '—',
       ['Màn Sửa không có trường cần kiểm trùng (mã tự sinh, Kho khóa).'], 116)
S4.add('Mở Sửa rồi Quay lại không đổi', 'P1', PRE_EDIT, SUA + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 119)
S4.add('Đổi rồi trả về ban đầu', 'P2', PRE_EDIT, SUA + ['Sửa Ghi chú rồi gõ lại "Nháp".', 'Bấm Quay lại.'], '—',
       ['Về danh sách không hỏi.'], 120)
S4.add('Quay lại khi đã đổi', 'P0', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Bấm Quay lại.'], '—',
       ['Hộp "Thông tin chưa lưu" (Thoát / Ở lại).'], 121)
S4.add('Thoát không lưu', 'P1', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Bấm Quay lại, chọn Thoát.'], '—',
       ['Về danh sách; Ghi chú của phiếu vẫn "Nháp".'], [122, 124])
S4.add('Ở lại', 'P2', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Bấm Quay lại, chọn Ở lại.'], '—', ['Giữ form với Ghi chú đã sửa.'], 123)
S4.add('Phiếu đã chuyển không sửa được', 'P0', [ACC_L, 'PĐCVT-01241 đã Đã chuyển.'],
       [MENU, 'Quan sát dòng 01241.', 'Mở đường link màn Sửa của 01241.'], '—',
       ['Không có nút Sửa, Xóa.', 'Mở đường link màn Sửa tự chuyển về màn chi tiết.'], [126, 129])
S4.add('Phiếu đổi trạng thái trong lúc đang sửa', 'P0', [PRE_EDIT, 'Tab 1 đang mở màn Sửa; tab 2 vừa Điều chuyển phiếu.'],
       ['Ở tab 1 bấm Lưu nháp.'], '—', ['Báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang"; không lưu.'], 128)
S4.add('Phiếu bị người khác xóa', 'P1', [PRE_EDIT, 'Tab 1 đang mở màn Sửa; tài khoản khác vừa xóa phiếu.'],
       ['Ở tab 1 bấm Lưu nháp.'], '—', ['Báo phiếu không tìm thấy / trạng thái đã thay đổi; không tạo lại phiếu.'], 127)
S4.add('Xóa file đã lưu', 'P1', [ACC_L, 'PĐCVT-01241 Đang tạo có file bien_ban.pdf.'], SUA + ['Bấm xóa ở dòng bien_ban.pdf.',
       'Bấm Xóa trong hộp.'], '—',
       ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa file đính kèm này?".',
        'Báo "Xóa file thành công", file biến mất ngay (không cần bấm Lưu); lịch sử có mốc thay đổi File đính kèm.'], 108)
S4.add('Người khác xem được cũng sửa được phiếu Đang tạo', 'P0', [ACC_V1 + ' Có quyền xem theo tổng công ty.', DRAFT],
       ['Đăng nhập V1.', MENU, 'Tìm PĐCVT-01241.'], '—',
       ['Dòng có nút Sửa, Xóa; V1 sửa được (giữ như hệ thống cũ, không bắt buộc là người tạo).'], [126, 290])

# ============================================================== V. XÓA
S5 = Sec(5)
S5.add('Nút Xóa chỉ ở phiếu Đang tạo', 'P0', PRE_LIST, [MENU, 'Quan sát cột Hành động dòng 01235 và 01234.'], '—',
       ['01235 (Đang tạo): có nút thùng rác đỏ "Xóa".', '01234 (Đã chuyển): không có nút Xóa.'], 130)
S5.add('Hộp xác nhận xóa', 'P0', [PRE_EDIT], [MENU, 'Ở dòng PĐCVT-01241 bấm Xóa.'], '—',
       ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa bản ghi này không?" với nút Xóa (đỏ), Hủy.'], [131, 132])
S5.add('Xóa phiếu Đang tạo', 'P0', [PRE_EDIT], [MENU, 'Ở dòng PĐCVT-01241 bấm Xóa.', 'Bấm Xóa trong hộp.'], '—',
       ['Báo "Xóa thành công.", danh sách nạp lại, không còn PĐCVT-01241.', 'Tổng số ở dòng "Hiển thị" giảm 1.'], [133, 139, 140])
S5.add('Hủy xóa', 'P0', [PRE_EDIT], [MENU, 'Ở dòng PĐCVT-01241 bấm Xóa.', 'Bấm Hủy.'], '—',
       ['Hộp đóng, phiếu vẫn còn.'], 134)
S5.add('Xóa từ màn chi tiết', 'P1', [PRE_EDIT], [MENU, 'Bấm PĐCVT-01241.', 'Bấm Xóa ở chân màn, xác nhận.'], '—',
       ['Báo "Xóa thành công.", quay về danh sách.'], 133)
S5.add('Xóa phiếu đã có dòng hàng', 'P1', [PRE_EDIT], [MENU, 'Xóa PĐCVT-01241 (có 1 dòng hàng).'], '—',
       ['Xóa được cả phiếu và dòng hàng (không có ràng buộc chặn); tồn kho, Thẻ kho không đổi.'], [135, 136, 141])
S5.add('Xóa phiếu lập từ phiếu kiểm kê', 'P2', [PKK, 'Đã lưu nháp 1 phiếu từ TPE-KKVT-00142.'], [MENU, 'Xóa phiếu nháp đó.',
       KKVT_MENU, 'Xem TPE-KKVT-00142.'], '—', ['Xóa được; phiếu kiểm kê vẫn Chờ xử lý, vẫn có nút Tạo phiếu điều chuyển vị trí.'], 141)
S5.add('Phiếu đã chuyển không xóa được', 'P1', [PRE_EDIT, 'Tab 1 mở hộp xác nhận xóa; tab 2 vừa Điều chuyển phiếu.'],
       ['Ở tab 1 bấm Xóa.'], '—', ['Báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang"; phiếu còn.'], 137)
S5.add('Phiếu đã bị người khác xóa', 'P1', [PRE_EDIT, 'Hai tab cùng mở danh sách.'], ['Tab 1 xóa 01241.', 'Tab 2 bấm Xóa 01241, xác nhận.'],
       '—', ['Tab 2 báo không tìm thấy / lỗi, không treo màn.'], 138)

# ============================================================== VI. DUYỆT PHIẾU (ĐIỀU CHUYỂN)
S6 = Sec(6)
S6.add('Nút Điều chuyển ở màn Tạo / Sửa', 'P0', PRE_EDIT, SUA, '—',
       ['Chân màn có nút "Điều chuyển" (rê chuột: "Điều chuyển hàng sang vị trí nhập (ghi tồn kho, không hoàn tác)").',
        'Màn chi tiết / phiếu Đã chuyển không có nút này.'], 300)
S6.add('Hộp xác nhận điều chuyển', 'P0', PRE_FORM, CHON + ['Bấm Điều chuyển.'], '—',
       ['Hộp "Xác nhận điều chuyển": ' + CONFIRM + ' với nút Điều chuyển, Hủy.'], [90, 301])
S6.add('Điều chuyển từ màn Tạo với dữ liệu đầy đủ', 'P0', PRE_FORM,
       CHON + ['Nhập Ghi chú, thêm file.', 'Bấm Điều chuyển, xác nhận.'], ['Ghi chú: Chuyển hàng sang vị trí mới', FILE],
       ['Báo "Điều chuyển thành công.", về danh sách.', 'Phiếu mới nhãn xanh lá "Đã chuyển"; có nút In, không có Sửa / Xóa.'],
       [86, 92, 302, 305])
S6.add('Điều chuyển thiếu dữ liệu', 'P0', PRE_FORM, TAO + ['Chọn Kho = PTT - Phan Trọng Tuệ.', 'Bấm Điều chuyển, xác nhận.'], '—',
       ['Cùng một lượt: Ghi chú, khối File đính kèm ' + REQ + ', bảng Chi tiết viền đỏ ' + REQ + '.', 'Thông báo ' + MISS + '; không lưu.'],
       [87, 303])
S6.add('Điều chuyển khi dòng thiếu cột', 'P0', PRE_FORM, CHON[:5] + ['Nhập Ghi chú, thêm file.', 'Bấm Điều chuyển, xác nhận.'], '—',
       ['Dòng 1: dưới ô Vị trí nhập và SL ' + REQ + '.', 'Thông báo ' + MISS + '.'], [87, 303])
S6.add('Điều chuyển với file sai định dạng', 'P2', PRE_FORM, CHON + ['Nhập Ghi chú.', 'Thêm file "a.docx".'], '—',
       ['File bị từ chối; Điều chuyển vẫn báo thiếu file.'], 88)
S6.add('Ghi tồn đúng khi điều chuyển', 'P0', PRE_FORM,
       CHON + ['Nhập Ghi chú, thêm file.', 'Điều chuyển, xác nhận.', 'Mở Báo cáo tồn kho theo vị trí và Thẻ kho của hàng 2Q-GIADEPHUTUNG, kho PTT.'],
       '—', ['Lô ...-48711: PTT-N1-D1-K1-T1 còn 26, PTT-N1-D1-K1-T2 thêm 1 (cùng lô).', 'Tổng tồn của hàng tại kho PTT không đổi.',
             'Thẻ kho có dòng xuất ở vị trí cũ và dòng nhập ở vị trí mới, số chứng từ PĐCVT-NNNNN.'], [306, 307])
S6.add('Vượt tồn lô thì không ghi gì', 'P0', PRE_FORM,
       CHON[:4] + ['Chọn lô tồn 1 (...-48718).', 'Chọn Vị trí nhập, nhập SL = 5.', 'Nhập Ghi chú, thêm file, Điều chuyển, xác nhận.'], 'SL: 5',
       ['Dưới ô SL: "Vượt quá SL tồn của lô."; không lưu phiếu, tồn không đổi.'], [304, 285])
S6.add('Cộng dồn nhiều dòng cùng lô vượt tồn', 'P0', PRE_FORM,
       CHON + ['Thêm dòng 2 cùng hàng, cùng vị trí, cùng lô ...-48711, SL 27.', 'Nhập Ghi chú, file, Điều chuyển, xác nhận.'], '—',
       ['Cả 2 dòng báo dưới ô SL "Vượt quá SL tồn của lô." (tổng 28 > 27); không ghi dòng nào.'], 304)
S6.add('Vượt tồn vị trí do phiếu nhập chưa hạch toán', 'P2',
       [PRE_FORM, 'Tại PTT-N1-D1-K1-T1 có phiếu nhập kho chưa hạch toán 20 Cái hàng này.'],
       CHON[:6] + ['Nhập SL = 10, Ghi chú, file; Điều chuyển, xác nhận.'], '—',
       ['Dưới ô SL: "Vượt quá SL tồn tại vị trí xuất." (tồn vị trí khả dụng 28 trừ 20 = 8).'], 304)
S6.add('Hàng hoặc vị trí đang kiểm kho', 'P0',
       [PRE_FORM, 'Hàng 2Q-GIADEPHUTUNG thuộc phiếu kiểm kê theo hàng hóa đang kiểm tại kho PTT.'],
       CHON + ['Nhập Ghi chú, file; Điều chuyển, xác nhận.'], '—',
       ['Dưới ô Tên hàng hóa: "Hàng đang kiểm kho."; không ghi tồn.', 'Vị trí đang kiểm: dưới ô vị trí "Vị trí đang kiểm kho.".'], 304)
S6.add('Bấm Hủy trong hộp xác nhận', 'P0', PRE_FORM, CHON + ['Nhập Ghi chú, thêm file.', 'Bấm Điều chuyển.', 'Bấm Hủy.'], '—',
       ['Hộp đóng, form giữ nguyên, không lưu, tồn không đổi.'], [91, 310])
S6.add('Điều chuyển từ màn Sửa', 'P0', [PRE_EDIT, 'Đã thêm Vị trí nhập và file cho phiếu.'], SUA + ['Bấm Điều chuyển, xác nhận.'], '—',
       ['Báo "Điều chuyển thành công."; phiếu Đã chuyển; tồn được ghi như khi điều chuyển từ màn Tạo.',
        'Lịch sử có mốc "Thay đổi trạng thái" Đang tạo sang Đã chuyển.'], [86, 305, 312])
S6.add('Phiếu nháp đã có file không bắt thêm file', 'P0', [PRE_EDIT, 'Phiếu đã lưu nháp kèm 1 file.'],
       SUA + ['Không thêm file, bấm Điều chuyển, xác nhận.'], '—', ['Điều chuyển được, không báo thiếu File đính kèm.'], 303)
S6.add('Lập từ phiếu Kiểm kê theo vị trí thì phiếu kiểm kê hoàn thành', 'P0', [PKK],
       [KKVT_MENU, 'Bấm Tạo phiếu điều chuyển vị trí ở TPE-KKVT-00142.', 'Chọn Vị trí nhập, nhập Ghi chú, file; Điều chuyển, xác nhận.',
        'Xem lại TPE-KKVT-00142.'], '—',
       ['Phiếu kiểm kê chuyển "Hoàn thành" (kế hoạch kiểm kê cha cũng Hoàn thành); lịch sử phiếu kiểm kê ghi "Phiếu điều chuyển vị trí '
        '<mã>.".', 'Nút Tạo phiếu điều chuyển vị trí biến mất.'], [307, 281])
S6.add('Không có thông báo gửi đi', 'P2', PRE_FORM, CHON + ['Điều chuyển (đủ dữ liệu).', 'Mở chuông thông báo của thủ kho khác.'], '—',
       ['Không phát sinh thông báo (màn không gửi thông báo khi điều chuyển).'], [308, 309])
S6.add('Bấm Điều chuyển liên tục', 'P1', PRE_FORM, CHON + ['Nhập Ghi chú, file.', 'Bấm Điều chuyển trong hộp nhiều lần nhanh.'],
       '—', ['Chỉ tạo 1 phiếu, tồn chỉ bị chuyển 1 lần.'], 101)
S6.add('Phiếu Đã chuyển không điều chuyển lại', 'P1', [PRE_LIST, P1234], [MENU, 'Mở chi tiết 01234.', 'Mở đường link màn Sửa của 01234.'],
       '—', ['Không có nút Sửa / Điều chuyển; đường link Sửa chuyển về màn chi tiết.'], [311, 89])
S6.add('Trường được làm mới sau điều chuyển', 'P2', PRE_FORM, CHON + ['Điều chuyển (đủ dữ liệu).', 'Bấm Tạo mới lại.'], '—',
       ['Form mới trống.'], 91)

# ============================================================== VII. LỊCH SỬ THAY ĐỔI
S7 = Sec(7)
S7.add('Mở cửa sổ lịch sử từ danh sách', 'P0', [PRE_LIST, P1234], [MENU, 'Ở dòng 01234 bấm Lịch sử.'], '—',
       ['Mở cửa sổ "Lịch sử thay đổi: PĐCVT-01234", nút Bộ lọc, nút Đóng.'], 162)
S7.add('Thông tin mỗi mốc', 'P0', [PRE_LIST, P1234], [MENU, 'Mở lịch sử 01234.'], '—',
       ['Mỗi mốc: thời gian dd/mm/yyyy hh:mm, hành động, "Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ".',
        'Mốc trạng thái ghi "Trạng thái: Đang tạo" sang "Đã chuyển".',
        'Mốc thông tin ghi "Chi tiết hàng hóa đã xóa" / "sửa thông tin" (tên hàng: trường cũ sang mới).'], [163, 165, 166, 167, 168])
S7.add('Mới nhất ở trên', 'P1', [PRE_LIST, P1234], [MENU, 'Mở lịch sử 01234.'], '—',
       ['Thứ tự: 05/11 15:03 Thay đổi trạng thái, 15:03 Thay đổi thông tin, 15:00 Thay đổi thông tin, 15:00 Tạo mới.'], 164)
S7.add('Phiếu lập ở hệ thống cũ chưa có lịch sử', 'P2', [PRE_LIST, 'PĐCVT-01226 (Nguyễn Thị Nguyệt) lập ở hệ thống cũ.'],
       [MENU, 'Mở lịch sử 01226.'], '—', ['Cửa sổ báo chưa có lịch sử, không lỗi.'], 173)
S7.add('Lọc theo loại hành động', 'P1', [PRE_LIST, P1234],
       [MENU, 'Mở lịch sử 01234.', 'Bấm Bộ lọc, chọn Loại hành động = Tạo mới.'], '—',
       ['Còn mốc Tạo mới.', 'Ô có: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.'], [169, 175])
S7.add('Lọc theo người thực hiện', 'P2', [PRE_LIST, P1234], [MENU, 'Mở lịch sử, Bộ lọc, chọn Người thực hiện = DNS Admin.'], '—',
       ['Còn đủ 4 mốc.'], 170)
S7.add('Lọc theo thời gian', 'P2', [PRE_LIST, P1234], [MENU, 'Mở lịch sử, Bộ lọc, Từ ngày = Đến ngày = 04/11/2026.'], '—',
       ['"Không có lịch sử phù hợp bộ lọc.".'], [171, 173])
S7.add('Kết hợp lọc và Làm mới', 'P2', [PRE_LIST, P1234],
       [MENU, 'Mở lịch sử, lọc Loại = Thay đổi thông tin và Từ ngày 05/11/2026.', 'Bấm Làm mới.'], '—',
       ['Bước 2: 2 mốc Thay đổi thông tin.', 'Bước 3: hiện lại đủ 4 mốc.'], [172, 174])
S7.add('Điều chuyển ngay từ màn Tạo chỉ có mốc Tạo mới', 'P1', PRE_FORM, CHON + ['Điều chuyển (đủ dữ liệu).', 'Mở lịch sử phiếu mới.'],
       '—', ['Có đúng 1 mốc "Tạo mới".'], 176)
S7.add('Sửa nhiều thông tin ghi 1 mốc', 'P2', PRE_EDIT, SUA + ['Sửa Ghi chú, đổi SL, thêm 1 file.', 'Lưu nháp.', 'Mở Lịch sử.'], '—',
       ['1 mốc "Thay đổi thông tin" gồm Ghi chú, Chi tiết hàng hóa sửa thông tin (SL cũ sang mới) và File đính kèm.'], [178, 183])
S7.add('Xóa 1 dòng giữa bảng', 'P2', [ACC_L, 'Phiếu nháp có 3 dòng hàng khác nhau.'], ['Sửa, xóa dòng 2, Lưu nháp.', 'Mở Lịch sử.'], '—',
       ['Chỉ 1 dòng "Chi tiết hàng hóa đã xóa" ghi tên hàng dòng 2; 2 dòng còn lại không bị coi là sửa.'], 177)
S7.add('Đóng cửa sổ', 'P1', [PRE_LIST, P1234], [MENU, 'Sang trang 2, lọc Trạng thái.', 'Mở lịch sử 1 dòng, bấm Đóng.',
       'Mở lại, bấm (x).'], '—', ['Cửa sổ đóng; danh sách giữ trang, bộ lọc.'], [184, 185])
S7.add('Xem / in không ghi lịch sử', 'P2', [PRE_LIST, P1234], [MENU, 'Mở chi tiết 01234, bấm In, đóng.', 'Mở lịch sử.'], '—',
       ['Không có mốc mới.'], 182)

# ============================================================== VIII. XEM CHI TIẾT
S8 = Sec(8)
S8.add('Mở màn chi tiết', 'P0', [PRE_LIST, P1234], [MENU, 'Bấm PĐCVT-01234.'], '—',
       ['Mở TRANG chi tiết, tab "Chi tiết phiếu điều chuyển vị trí: PĐCVT-01234".'], 186)
S8.add('Tiêu đề', 'P1', [PRE_LIST, P1234], [MENU, 'Bấm PĐCVT-01234.'], '—',
       ['Tiêu đề trang "Chi tiết phiếu điều chuyển vị trí: PĐCVT-01234" (không gắn nhãn trạng thái).'], 187)
S8.add('Đầy đủ trường', 'P0', [PRE_LIST, P1234], [MENU, 'Bấm PĐCVT-01234.'], '—',
       ['Thông tin chung: Kho PTT - Phan Trọng Tuệ, Ghi chú; góc phải "DNS Admin - 05/11/2026 15:00".',
        'Khối File đính kèm có 2 file ảnh.', 'Bảng Chi tiết: STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, Vị trí xuất, Lô xuất, Vị trí '
        'nhập, SL (không có SL tồn, Hành động).'], [188, 189])
S8.add('Khớp dữ liệu danh sách', 'P1', [PRE_LIST, P1234], [MENU, 'So dòng 01234 và màn chi tiết.'], '—',
       ['Kho, Người tạo, Ngày tạo trùng khớp.'], 190)
S8.add('Chế độ chỉ đọc', 'P0', [PRE_LIST, P1234], [MENU, 'Bấm PĐCVT-01234.'], '—',
       ['Mọi ô khóa; không có Lưu nháp / Điều chuyển.', 'Chân màn: In, Quay lại.'], [191, 192])
S8.add('Phiếu Đang tạo', 'P1', [PRE_LIST, P1235], [MENU, 'Bấm PĐCVT-01235.'], '—',
       ['Chân màn: Sửa, Xóa, Quay lại; không có In.', 'Khối File: "Không có file đính kèm."; dòng 2 các ô vị trí / lô trống.'], [193, 194])
S8.add('Phiếu lập từ phiếu kiểm kê', 'P2', [PRE_LIST, P1233], [MENU, 'Bấm PĐCVT-01233.', 'Bấm "TPE.KKK-01093".'], '—',
       ['Có ô Phiếu kiểm kê là liên kết; bấm mở chi tiết phiếu kiểm kê ở tab mới.'], 188)
S8.add('Khu vực lịch sử', 'P1', [PRE_LIST, P1234], [MENU, 'Bấm 01234.', 'Bấm Xem lịch sử.'], '—',
       ['Khối Lịch sử mở rộng, có 4 mốc như cửa sổ lịch sử.'], 195)
S8.add('Quay lại giữ trang và bộ lọc', 'P1', [PRE_LIST, 'Đang lọc Kho = PTT - Phan Trọng Tuệ, ở trang 2.'], ['Bấm 1 mã phiếu.', 'Bấm Quay lại.'],
       '—', ['Về danh sách, vẫn lọc Kho PTT ở trang 1 với bộ lọc giữ nguyên.'], [196, 197])
S8.add('Phiếu không tồn tại', 'P1', PRE_LIST, ['Mở đường link chi tiết với số phiếu không tồn tại.'], '—',
       ['Chuyển sang trang không tìm thấy, không báo lỗi nổi.'], 196)

# ============================================================== IX. IN PHIẾU
S9 = Sec(9)
S9.add('In phiếu từ danh sách', 'P0', [PRE_LIST, P1234], [MENU, 'Ở dòng 01234 bấm In.'], '—',
       ['Cửa sổ "Xem trước phiếu điều chuyển vị trí PĐCVT-01234".',
        'Bản in: logo, tên, địa chỉ công ty; tiêu đề "KIỂM KÊ KHO", "No: PĐCVT-01234", Ngày kiểm kê 05/11/2026, Kho PTT - Phan Trọng '
        'Tuệ, Ghi chú; bảng STT, Hàng hóa, ĐVT, Vị trí xuất, Lô xuất, Vị trí nhập, SL; ký Người lập phiếu (DNS Admin), Thủ kho, Trưởng '
        'phòng.'], 6)
S9.add('In phiếu từ màn chi tiết', 'P1', [PRE_LIST, P1234], [MENU, 'Bấm 01234.', 'Bấm In.'], '—', ['Cùng bản xem trước.'], 6)
S9.add('Phiếu Đang tạo không có nút In', 'P1', [PRE_LIST, P1235], [MENU, 'Quan sát dòng 01235, mở chi tiết.'], '—',
       ['Không có nút In ở dòng và màn chi tiết.'], 6)
S9.add('Letterhead theo công ty của phiếu', 'P1', [ACC_V1, 'Phiếu PĐCVT-01226 thuộc công ty TPE; V1 đang làm việc ở công ty TPSG.'],
       ['Đăng nhập V1.', MENU, 'In 01226.'], '—', ['Đầu bản in là logo / tên công ty TPE (công ty của phiếu).'], 6)
S9.add('Bấm In trong cửa sổ', 'P1', [PRE_LIST, P1234], ['Mở xem trước 01234.', 'Bấm In.'], '—', ['Mở hộp thoại in của trình duyệt.'], 6)
S9.add('Đóng cửa sổ xem trước', 'P2', [PRE_LIST, P1234], ['Mở xem trước 01234.', 'Bấm (x).'], '—',
       ['Cửa sổ đóng, danh sách giữ nguyên.'], 185)
S9.add('In dự kiến ở màn Tạo', 'P0', PRE_FORM, CHON + ['Nhập Ghi chú.', 'Bấm In dự kiến.'], '—',
       ['Cửa sổ "Xem trước phiếu dự kiến điều chuyển vị trí"; "No:" trống, Ngày kiểm kê = hôm nay, Kho PTT, Ghi chú đã nhập.',
        'Bảng có thêm cột Ghi chú trống; Người lập phiếu = L.', 'Không lưu phiếu.'], 6)
S9.add('In dự kiến khi thiếu dữ liệu', 'P0', [ACC_L, P1235], [MENU, 'Ở dòng 01235 bấm Sửa.', 'Bấm In dự kiến.'], '—',
       ['Dưới Ghi chú ' + REQ + '; dòng 2 dưới Vị trí xuất, Lô xuất ' + REQ + '.', 'Thông báo ' + MISS + '; không mở cửa sổ.'], 6)
S9.add('In dự kiến ở màn Sửa có mã phiếu', 'P1', [PRE_EDIT, 'Dòng đủ ĐVT, Vị trí xuất, Lô xuất.'], SUA + ['Bấm In dự kiến.'], '—',
       ['"No: PĐCVT-01241", Ngày kiểm kê = ngày tạo phiếu, Người lập phiếu = người tạo.'], 6)
S9.add('In dự kiến không bắt Vị trí nhập, SL', 'P2', PRE_FORM, CHON[:5] + ['Nhập Ghi chú.', 'Bấm In dự kiến.'], '—',
       ['Mở được bản dự kiến; cột Vị trí nhập, SL trống.'], 6)

# ============================================================== X. TÙY CHỈNH CỘT
S10 = Sec(10)
S10.add('Mở cửa sổ Tùy chỉnh cột', 'P0', PRE_LIST, [MENU, 'Bấm nút biểu tượng cột.'], '—',
        ['Cửa sổ "Tuỳ chỉnh cột", dòng hướng dẫn, 10 cột, "Đang chọn 10/10 cột", nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng.'], [198, 199])
S10.add('Cột chọn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa lưu cấu hình.'], ['Mở Tuỳ chỉnh cột.'], '—', ['Cả 10 cột được tích.'], 200)
S10.add('Ẩn cột', 'P0', PRE_LIST, ['Mở Tuỳ chỉnh cột, bỏ tích Người cập nhật, bấm Lưu.'], '—',
        ['Báo "Cập nhật thành công"; bảng không còn cột Người cập nhật.'], [202, 206])
S10.add('Hiện lại cột ẩn', 'P1', 'Đang ẩn cột Người cập nhật.', ['Mở Tuỳ chỉnh cột, tích Người cập nhật, Lưu.'], '—',
        ['Cột hiện lại đúng vị trí.'], 201)
S10.add('Cột khóa không ẩn được', 'P0', PRE_LIST, ['Mở Tuỳ chỉnh cột.'], '—',
        ['STT, Mã phiếu, Hành động có biểu tượng ổ khóa, không bỏ tích / kéo được.'], [203, 205])
S10.add('Kéo đổi thứ tự cột', 'P1', PRE_LIST, ['Kéo cột Kho lên sau Mã phiếu, Lưu.'], '—', ['Bảng hiện Kho ngay sau Mã phiếu.'], 204)
S10.add('Đóng không lưu', 'P1', PRE_LIST, ['Bỏ tích Kho, bấm Đóng.'], '—', ['Bảng vẫn có cột Kho.'], 207)
S10.add('Ghi nhớ sau F5', 'P1', 'Đã ẩn cột Người cập nhật và Lưu.', ['Nhấn F5.'], '—', ['Cột Người cập nhật vẫn ẩn.'], 208)
S10.add('Cấu hình theo tài khoản', 'P2', 'Tài khoản A đã ẩn cột Kho.', ['Đăng nhập B, mở màn.'], '—', ['B vẫn thấy cột Kho.'], 209)
S10.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', 'Đang lọc Kho = HP - Hải Phòng.', ['Ẩn cột Người tạo, Lưu.'], '—',
        ['Vẫn 8 phiếu, bộ lọc giữ nguyên.'], [210, 211])

# ============================================================== XI. XUẤT DANH SÁCH EXCEL
S11 = Sec(11)
S11.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel.'], '—',
        ['Cửa sổ "Chọn trường xuất Excel": 8 trường Mã phiếu, Ngày tạo, Kho, Phiếu kiểm kê, Trạng thái, Người tạo, Ngày cập nhật, Người '
         'cập nhật; "Đang chọn 8/8 trường".'], [212, 213])
S11.add('Trường chọn mặc định theo cột đang hiện', 'P1', 'Đang ẩn cột Người cập nhật.', ['Bấm Xuất Excel.'], '—',
        ['Người cập nhật không được tích sẵn.'], [214, 215])
S11.add('Xuất tất cả trường', 'P0', PRE_LIST, ['Bấm Xuất Excel, Chọn tất cả, Xuất file.'], '—',
        ['Tải "danh_sach_phieu_dieu_chuyen_vi_tri.xlsx", báo "Xuất Excel thành công.".', 'Đủ 943 dòng, cột STT + 8 cột.'],
        [216, 223, 227])
S11.add('Xuất một số trường', 'P1', PRE_LIST, ['Bỏ chọn hết, tích Mã phiếu, Trạng thái, Xuất file.'], '—',
        ['File chỉ có STT, Mã phiếu, Trạng thái.'], 217)
S11.add('Không chọn trường', 'P1', PRE_LIST, ['Bấm Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S11.add('Xuất theo tìm kiếm', 'P1', PRE_LIST, ['Tìm "0123".', 'Xuất file.'], '—', ['File có 7 dòng.'], 219)
S11.add('Xuất theo bộ lọc', 'P0', PRE_LIST, [ADV, 'Chọn Trạng thái = Đang tạo.', 'Xuất file.'], '—', ['File có đúng 4 dòng.'], 220)
S11.add('Xuất nhiều trang', 'P1', PRE_LIST, ['Đang ở trang 1 (10 dòng/trang), Xuất file.'], '—',
        ['File đủ 943 dòng, không chỉ trang đang xem.'], 221)
S11.add('Danh sách rỗng', 'P1', PRE_LIST, ['Tìm "ZZZ".', 'Xuất file.'], '—',
        ['Vẫn tải file chỉ có tiêu đề và dòng tên cột, báo "Xuất Excel thành công.".'], 222)
S11.add('Cấu trúc file', 'P0', PRE_LIST, [ADV, 'Chọn Ngày tạo 23/10/2026 – 24/10/2026.', 'Xuất tất cả trường, mở file.'], '—',
        ['Đầu file có letterhead công ty người xuất, tiêu đề "DANH SÁCH PHIẾU ĐIỀU CHUYỂN VỊ TRÍ", dòng "Từ ngày 23/10/2026 đến ngày '
         '24/10/2026"; trang tính "Điều chuyển vị trí".', 'Dòng tên cột đúng tên trường; cuối file có khối ký.'], [224, 225])
S11.add('Thứ tự cột theo kéo thả', 'P1', PRE_LIST, ['Kéo Trạng thái lên đầu, Xuất file.'], '—', ['Cột sau STT là Trạng thái.'], 226)
S11.add('Dữ liệu khớp và định dạng', 'P0', [PRE_LIST, P1234], ['Xuất tất cả, tìm dòng 01234.'], '—',
        ['Ngày tạo "05/11/2026", Kho "PTT - Phan Trọng Tuệ", Trạng thái "Đã chuyển", Ngày cập nhật "05/11/2026 15:03".',
         'Tiếng Việt có dấu, chữ Đ trong mã phiếu hiển thị đúng.'], [228, 229, 230])

# ============================================================== XII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S12 = Sec(12)
S12.add('Dòng điều chuyển ở Thẻ kho', 'P0', [PRE_LIST, P1234], [CARD_MENU, 'Lọc ANOP-ANOPECL315KG, kho PTT.'], '—',
        ['Có dòng xuất ở PTT-N1-D6-K7-T1 và dòng nhập ở PTT-N1-D5-K8-T1, SL 1, số chứng từ PĐCVT-01234; bấm số chứng từ mở chi tiết.'],
        [274, 279])
S12.add('Tổng hợp xuất nhập tồn', 'P0', [PRE_LIST, P1234], ['Vào phân hệ Kho > "Báo cáo kho" > "Tổng hợp xuất nhập tồn", kỳ có 05/11/2026.',
        'Đổi loại báo cáo "Không nhặt điều chuyển".'], '—',
        ['Mặc định số nhập / xuất trong kỳ cộng cả điều chuyển (cộng 1 nhập, 1 xuất).', 'Loại "Không nhặt điều chuyển" bỏ 2 dòng này; tồn cuối kỳ không '
         'đổi.'], 274)
S12.add('Báo cáo tồn kho theo vị trí', 'P0', PRE_FORM,
        CHON + ['Nhập Ghi chú, file; Điều chuyển.', 'Vào phân hệ Kho > "Báo cáo kho" > "Báo cáo tồn kho theo vị trí".'], '—',
        ['PTT-N1-D1-K1-T1 giảm 1, PTT-N1-D1-K1-T2 tăng 1; tổng tồn hàng tại kho không đổi.'], 274)
S12.add('Lưu nháp từ Kiểm kê theo hàng hóa chuyển Đang xử lý', 'P0',
        ['Phiếu Kiểm kê theo hàng hóa TPE.KKK-01096 Chờ xử lý, còn dòng cần điều chuyển, chưa có phiếu điều chuyển; tài khoản có quyền '
         'xử lý và "Điều chuyển vị trí".'],
        [KKHH_MENU, 'Mở chi tiết TPE.KKK-01096, bấm "Tạo phiếu điều chuyển vị trí".', 'Chọn Vị trí nhập, bấm Lưu nháp.',
         'Xem lại TPE.KKK-01096.'], '—',
        ['Phiếu kiểm kê chuyển "Đang xử lý", lịch sử ghi "Phiếu điều chuyển vị trí <mã>.".',
         'Nút Tạo phiếu điều chuyển vị trí không còn (đã có phiếu).'], [281, 282])
S12.add('Phiếu kiểm kê không còn dòng thiếu không lập được', 'P1', [PKK, 'Đã điều chuyển hết dòng của TPE-KKVT-00142.'],
        [KKVT_MENU, 'Quan sát dòng TPE-KKVT-00142.', 'Mở lại đường link tạo phiếu từ phiếu kiểm kê này.'], '—',
        ['Không còn nút Tạo phiếu điều chuyển vị trí.', 'Đường link chuyển trang không tìm thấy.'], [268, 269])
S12.add('Cấp con đúng cấp cha', 'P1', [PRE_LIST, P1234], [MENU, 'Mở 01234.'], '—',
        ['Mọi vị trí xuất / nhập trên phiếu thuộc kho PTT.'], 283)
S12.add('Vị trí ngoài kho bị chặn', 'P2', [PRE_EDIT, 'Dữ liệu dòng bị đổi sang vị trí thuộc kho LN.'], SUA + ['Điều chuyển, xác nhận.'], '—',
        ['Dưới ô vị trí: "Vị trí không thuộc kho của phiếu."; không ghi tồn.'], [283, 285])
S12.add('Tham chiếu giữ khi đổi trạng thái', 'P1', [PRE_LIST, P1234], [MENU, 'Mở 01234 (Đã chuyển).'], '—',
        ['Dòng hàng, vị trí, lô, file vẫn đủ như lúc lập.'], 284)
S12.add('Đổi tên hàng ở danh mục', 'P2', [PRE_LIST, P1234], ['Đổi tên hàng ANOP-ANOPECL315KG ở danh mục.', 'Mở 01234.'], '—',
        ['Phiếu hiện tên hàng theo danh mục hiện tại (phiếu lưu theo mã hàng, không mất liên kết).'], [272, 278])
S12.add('Không xóa được vị trí / kho / hàng đã dùng', 'P1', [PRE_LIST, P1235],
        ['Vào phân hệ Kho > "Danh mục" > "Vị trí", xóa vị trí PTT-N1-D1-K1-T1.', 'Xóa hàng 2Q-INOX300 ở Kho dữ liệu hàng hoá.'], '—',
        ['Hệ thống chặn xóa vị trí vì đã có trên phiếu (kể cả nháp).', 'Chặn xóa hàng: "Hàng hoá đã phát sinh chứng từ, không xoá được."'],
        [270, 280])
S12.add('Không phát sinh dữ liệu mồ côi khi xóa phiếu', 'P2', [PRE_EDIT], ['Xóa PĐCVT-01241.', 'Thử xóa vị trí đã dùng trên phiếu đó.'],
        '—', ['Phiếu và dòng hàng bị xóa cùng nhau; vị trí không còn bị chặn bởi phiếu đã xóa.'], [285, 280])

# ============================================================== XIII. PHÂN QUYỀN (cuối)
S13 = Sec(13)
S13.add('Quyền Xem theo tổng công ty', 'P0', ACC_V1, ['Đăng nhập V1.', MENU, ADV], '—',
        ['Thấy đủ 943 phiếu của mọi công ty.', 'Có ô lọc Công ty và Phòng ban.'], [287, 299])
S13.add('Quyền Xem theo công ty', 'P0', [ACC_V2, 'PĐCVT-01226 thuộc công ty TPE.'],
        ['Đăng nhập V2.', MENU, ADV], '—', ['Chỉ thấy phiếu công ty TPSG + phiếu mình tạo; KHÔNG thấy 01226.',
                                             'Có ô Phòng ban, không có ô Công ty.'], [287, 299])
S13.add('Quyền Xem theo kho', 'P0', ACC_V3, ['Đăng nhập V3.', MENU], '—',
        ['Thấy 8 phiếu kho HP - Hải Phòng + phiếu mình tạo.', 'Không có khối lọc Công ty, Phòng ban.'], [287, 299])
S13.add('Không có quyền nào', 'P0', ACC_N, ['Đăng nhập N.', MENU], '—',
        ['Menu vẫn hiện, mở được màn.', 'Chỉ thấy PĐCVT-01240 do N tạo; không có nút Tạo mới.'], [287, 295, 299])
S13.add('Quyền Điều chuyển vị trí để lập phiếu', 'P0', PRE_FORM, ['Đăng nhập L.'] + CHON + ['Bấm Lưu nháp.'], '—',
        ['L thấy nút Tạo mới, lập được phiếu và thấy phiếu đó trong danh sách.'], 289)
S13.add('Có quyền lập nhưng không là thủ kho', 'P1', ['Tài khoản M: có quyền "Điều chuyển vị trí", không là thủ kho kho nào.'],
        ['Đăng nhập M.', MENU, 'Bấm Tạo mới, mở ô Kho.'], '—', ['Ô Kho không có lựa chọn; không lập phiếu tay được.'], 289)
S13.add('Xem chi tiết trong phạm vi', 'P0', [ACC_V3], ['Đăng nhập V3.', MENU, 'Mở PĐCVT-01231.'], '—', ['Xem được đầy đủ.'], 288)
S13.add('URL chi tiết ngoài phạm vi', 'P0', [ACC_N, 'N có đường link chi tiết 01234.'], ['Đăng nhập N, mở đường link.'], '—',
        ['Chuyển sang trang không tìm thấy; không lộ dữ liệu.'], [288, 296])
S13.add('Sửa / Xóa phiếu Đang tạo theo phạm vi', 'P0', [ACC_N, 'PĐCVT-01235 của DNS Admin (Đang tạo).'],
        ['Đăng nhập N.', 'Mở đường link màn Sửa của 01235.'], '—',
        ['Chuyển trang không tìm thấy (ngoài phạm vi).', 'Với phiếu 01240 của chính N: có Sửa, Xóa.'], [290, 291, 296])
S13.add('Ẩn nút khi thiếu quyền', 'P0', [ACC_V1, P1235], ['Đăng nhập V1.', MENU], '—',
        ['Không có nút Tạo mới (thiếu "Điều chuyển vị trí").', 'Dòng Đã chuyển không có Sửa / Xóa; dòng Đang tạo không có In.'], 295)
S13.add('Xuất Excel theo quyền', 'P1', ACC_V3, ['Đăng nhập V3.', 'Xuất Excel, Xuất file.'], '—',
        ['File chỉ có phiếu trong phạm vi của V3.'], 293)
S13.add('Xem lịch sử theo quyền', 'P1', [ACC_V1, P1234], ['Đăng nhập V1.', 'Mở lịch sử 01234.'], '—', ['Xem được 4 mốc.'], 294)
S13.add('Bị gỡ quyền giữa lúc thao tác', 'P1', [ACC_V1, 'Quản trị gỡ quyền theo tổng công ty của V1 khi đang ở danh sách.'],
        ['Bấm sang trang 2.'], '—', ['Danh sách chỉ còn phiếu V1 tự tạo (phạm vi kiểm lại ở mỗi lần nạp).'], [297, 298])
S13.add('Không có khóa / mở khóa', 'P2', PRE_LIST, [MENU, 'Quan sát cột Hành động mọi dòng.'], '—',
        ['Không có nút Khóa / Mở khóa ở bất kỳ phiếu nào.'], 292)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'CHỈNH SỬA', S4),
    ('V', 'XÓA', S5),
    ('VI', 'DUYỆT PHIẾU (ĐIỀU CHUYỂN)', S6),
    ('VII', 'LỊCH SỬ THAY ĐỔI', S7),
    ('VIII', 'XEM CHI TIẾT PHIẾU ĐIỀU CHUYỂN VỊ TRÍ', S8),
    ('IX', 'IN PHIẾU (GỒM IN DỰ KIẾN)', S9),
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
                feature_name='Phiếu điều chuyển vị trí - Cập nhật ngày 09/11/2026',
                module_name='Phiếu điều chuyển vị trí', description_block=DESCRIPTION_BLOCK, sections=SECTIONS,
                loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

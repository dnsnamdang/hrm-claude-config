# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu xuất điều chỉnh sai số liệu" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan,
loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (xác định từ code 09/11/2026): màn có trạng thái phiếu (Chờ nhập lại / Đã nhập lại), có In phiếu, Lịch sử, nút Tạo
phiếu nhập lại đổi trạng thái; phiếu sinh ra từ Phiếu nhập kho bị Không duyệt (màn Tạo phiếu xuất lại = THÊM MỚI của chứng từ
này, lối vào nằm ở màn Phiếu nhập kho, lưu xong về danh sách này). Bỏ nhóm màn không có (kiểm code: không có route / nút Sửa,
Xóa, Khóa, Gửi duyệt, Duyệt, Không duyệt, Hủy, Import): I Hiển thị trang & truy cập · II Tìm kiếm & lọc danh sách (gồm Cài đặt bộ
lọc, Công ty – Phòng ban) · III Thêm mới (Tạo phiếu xuất lại) · IV Lịch sử thay đổi · V Xem chi tiết · VI In phiếu · VII Tùy chỉnh
cột · VIII Xuất danh sách Excel · IX Ràng buộc với các chức năng khác (Tạo phiếu nhập lại, Phiếu nhập kho, Thẻ kho, tồn kho,
danh mục) · X Phân quyền (cuối). Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../borrow-export/gen_testcase.py.
Nguồn hành vi (đọc 09/11/2026, nhánh develop cả 2 repo): FE pages/finance/warehouse-reexports/**, warehouse-imports/_id/
{re-export, re-import, index}.vue; BE WarehouseReExportService / Controller, WarehouseImportController (reExport / reImport),
WarehouseImportWriteService::reImport, PhysicalStockWriter, PermissionHelper::checkPermissionListWithColumn.
Số liệu mẫu: dev-hrm 09/11/2026 (DNS Admin): 23 phiếu (21 Đã nhập lại, 2 Chờ nhập lại), PXL-00022 / PXL-00021 / PNK-11608.
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
from tc_phieu_bosung import ListScreen, open_menu_case, filter_memory_cases, combo_cases, org_cases, check_no_dash_pre  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Kho > menu "Xuất kho" > bấm "Phiếu xuất điều chỉnh sai số liệu".'
PNK_MENU = 'Vào phân hệ Kho > menu "Nhập kho" > bấm "Phiếu nhập kho".'
ADV = 'Bấm Tìm kiếm nâng cao.'

PRE_LIST = ('Tài khoản DNS Admin (Super admin); hệ thống có 23 phiếu xuất lại: 21 Đã nhập lại, 2 Chờ nhập lại '
            '(PXL-00022, PXL-00020).')
P22 = ('Phiếu PXL-00022: Phiếu nhập kho PNK-11607, Ngày tạo 28/10/2026 10:20, Người tạo "HDQT - DNS Admin", trạng thái Chờ '
       'nhập lại; Loại nhập "Nhập hàng mua trong nước (TỰ DO + HÃNG)", Kho Sài Gòn, Người giao hàng "trang gấu", Ghi chú "Ghi chú '
       'trang"; 1 dòng "Xe bảo dưỡng nhanh EM tiêu chuẩn Vinfast" (Model MN-EM.VF, Mã SG-MN-EMVF, KOURITSU, Cái, Tổng SL 16: '
       'vị trí SG-N1-D1-K1-T1 SL 15, SG-N1-D1-K1-T5 SL 1).')
P21 = ('Phiếu PXL-00021 (PNK-11594, Đã nhập lại) có 2 mốc lịch sử: Tạo mới 27/10/2026 22:44 và Thay đổi trạng thái 28/10/2026 '
       '09:14 "Chờ nhập lại sang Đã nhập lại", ghi chú "Tạo phiếu nhập lại PNK-11606", người thực hiện DNS Admin.')
ACC_A = 'Tài khoản A: không có quyền xem phiếu xuất lại nào; là người tạo phiếu nhập kho PNK-11608.'
PNK = ('Phiếu nhập kho PNK-11608 do A tạo, trạng thái Không duyệt (lý do "787"), Kho Sài Gòn, Người giao hàng "78787"; 2 dòng: '
       '"Bộ mũi khoét (5 chi tiết)" Bộ SL 1 tại SG-N1-D1-K1-T1 và "Bộ 13 mũi khoan khoét lỗ hợp kim HSS cao cấp" Bộ SL 1 tại '
       'SG-N1-D1-K1-T2; kho đủ tồn.')
PRE_FORM = ACC_A + '\n' + PNK
TAO = [PNK_MENU, 'Bấm mã PNK-11608 để mở chi tiết.', 'Bấm "Tạo phiếu xuất lại".']
XL = TAO + ['Bấm "Xuất lại" ở chân màn.', 'Bấm "Xuất lại" trong hộp xác nhận.']
ACC_Q1 = 'Tài khoản Q1: có quyền Xem phiếu xuất lại theo tổng công ty.'
ACC_Q2 = 'Tài khoản Q2: có quyền Xem phiếu xuất lại theo công ty, đang làm việc ở Công ty Sài Gòn.'
ACC_Q3 = 'Tài khoản Q3: có quyền Xem phiếu xuất lại theo phòng ban, quản lý phòng SG_KHO.'
ACC_Q4 = 'Tài khoản Q4: có quyền Xem phiếu xuất lại theo bộ phận, quản lý 1 bộ phận của SG_KHO.'
ACC_N = 'Tài khoản N: không có quyền xem phiếu xuất lại; tự tạo 1 phiếu PXL-00099 (Chờ nhập lại) từ phiếu nhập kho của mình.'

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
     'Màn Phiếu xuất điều chỉnh sai số liệu (phiếu xuất lại, mã PXL-NNNNN) dùng khi Kế toán kho Không duyệt một phiếu nhập kho '
     'đã ghi tồn: người tạo phiếu nhập kho lập phiếu xuất lại để trừ TOÀN BỘ hàng đã nhập (đúng lô, đúng vị trí), rồi lập phiếu '
     'nhập lại với số liệu đúng.\nMàn danh sách để tra cứu, in, xuất Excel, xem lịch sử và mở Tạo phiếu nhập lại.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Danh sách: phiếu xuất lại trong phạm vi xem của người dùng (theo 4 quyền xem; không có quyền thì chỉ phiếu mình tạo).\n'
     '- 2 trạng thái: Chờ nhập lại (nhãn vàng), Đã nhập lại (nhãn xanh lá).\n'
     '- Nút Tạo phiếu nhập lại: chỉ người tạo phiếu nhập kho gốc, khi phiếu nhập kho đang Đã xuất lại.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu ngoài phạm vi xem: không có trong danh sách, mở thẳng đường link ra trang không tìm thấy.\n'
     '- Màn không có Tạo mới trên danh sách, Sửa, Xóa, Khóa / Mở khóa, Duyệt, Không duyệt, Hủy, Import, In danh sách.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo ngày tạo phiếu xuất lại, lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Phiếu xuất lại > dòng hàng (hàng + đơn vị tính, Tổng SL) > dòng vị trí (Vị trí, SL).\n'
     '- Mỗi phiếu xuất lại gắn đúng 1 phiếu nhập kho gốc; công ty / phòng ban của phiếu lấy theo phiếu nhập kho.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Tổng SL của dòng hàng = tổng SL các vị trí.\n- Một phiếu nhập kho chỉ xuất lại được 1 lần (sau đó đã Đã xuất lại).'),
    ('7. Phân quyền cấp',
     '- Xem phiếu xuất lại theo tổng công ty: mọi phiếu; có ô lọc Công ty, Phòng ban.\n'
     '- Xem phiếu xuất lại theo công ty: phiếu của công ty đang làm việc + phiếu mình tạo; có ô Phòng ban.\n'
     '- Xem phiếu xuất lại theo phòng ban: phiếu của phòng ban / bộ phận mình quản lý + phiếu mình tạo.\n'
     '- Xem phiếu xuất lại theo bộ phận: phiếu của bộ phận mình quản lý + phiếu mình tạo.\n'
     '- Tạo phiếu xuất lại / Tạo phiếu nhập lại: theo người tạo phiếu nhập kho, không theo quyền.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là khoảng số thứ tự trang đang xem, N là tổng phiếu khớp bộ lọc trong phạm vi xem.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: A (người tạo phiếu nhập kho), Q1–Q4 (4 quyền xem), N (không quyền), DNS Admin (Super admin).\n'
     '- Lưu ý: Xuất lại TRỪ TỒN NGAY và không hoàn tác — chạy trên phiếu nhập kho thử.\n'
     '- Lưu ý: tiêu đề màn là "Danh sách phiếu xuất lại" dù mục menu là "Phiếu xuất điều chỉnh sai số liệu".\n'
     '- Màn Tạo phiếu xuất lại / Chi tiết là TRANG riêng, không phải cửa sổ nổi.'),
]

SCREEN = ListScreen(menu=MENU, title='Danh sách phiếu xuất lại', total=23, quick_label='mã phiếu, mã phiếu nhập kho',
                    quick_sample='PXL-00022', quick_hit='phiếu PXL-00022',
                    filters=[('Trạng thái', 'Chờ nhập lại'), ('Người tạo', 'HDQT - DNS Admin')])

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Cả 3 nơi đều là "Danh sách phiếu xuất lại".', 'Mục menu vẫn ghi "Phiếu xuất điều chỉnh sai số liệu".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE_LIST, [MENU, 'Quan sát khối bộ lọc, thanh công cụ và cột Hành động.'], '—',
       ['Khối "Bộ lọc danh sách": ô tìm nhanh (gợi ý "Tìm theo mã phiếu, mã phiếu nhập kho"), Tìm kiếm, Làm mới, Tìm kiếm nâng '
        'cao, Cài đặt bộ lọc.', 'Thanh công cụ: Xuất Excel, nút biểu tượng cột.', 'KHÔNG có nút Tạo mới, In danh sách, Import.',
        'Cột Hành động: In, Lịch sử ở mọi dòng; thêm Tạo phiếu nhập lại ở dòng đủ điều kiện; không có Sửa, Xóa.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 7 cột theo thứ tự: STT, Mã phiếu, Phiếu nhập kho, Ngày tạo, Người tạo, Trạng thái, Hành động.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 7/7 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp phiếu đã tạo', 'P0', [PRE_LIST, P22], [MENU, 'Tìm "PXL-00022", đối chiếu dòng.'], '—',
       ['Phiếu nhập kho "PNK-11607" (liên kết); Ngày tạo "28/10/2026 10:20"; Người tạo "HDQT - DNS Admin".',
        'Trạng thái nhãn vàng "Chờ nhập lại".'], 6)
S1.add('Liên kết Phiếu nhập kho mở ở tab mới', 'P1', [PRE_LIST, P22], [MENU, 'Ở dòng PXL-00022 bấm "PNK-11607".'], '—',
       ['Mở chi tiết phiếu nhập kho PNK-11607 ở TAB MỚI.', 'Tab danh sách giữ nguyên trang, bộ lọc.'], 6)
S1.add('Trạng thái bản ghi', 'P0', PRE_LIST, [MENU, 'Quan sát cột Trạng thái của PXL-00022 và PXL-00021.'], '—',
       ['PXL-00022: nhãn vàng "Chờ nhập lại".', 'PXL-00021: nhãn xanh lá "Đã nhập lại".', 'Không có trạng thái nào khác.'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', ['Tài khoản N mới, chưa tạo phiếu xuất lại nào, không có quyền xem.'],
       ['Đăng nhập N.', MENU], '—', ['Bảng hiện "Không có dữ liệu phù hợp.", không có dòng "Hiển thị".', 'Không báo lỗi.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'],
       'Ô tìm nhanh: ZZZ999', ['Bảng hiện "Không có dữ liệu phù hợp.".', 'Không báo lỗi.'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 20 phiếu, tự về trang 1, "Hiển thị 1–20 / 23".', 'Ô có các lựa chọn 5, 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–20 / 23".', 'Bước 3: "Hiển thị 1–10 / 23".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—',
       ['Bước 2: trang 3, "Hiển thị 21–23 / 23".', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang 3 quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ, bấm không tác dụng.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2, rồi trang 3.'], '—',
       ['Trang 2: STT 11–20; trang 3: STT 21–23.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 3.', ADV, 'Chọn Trạng thái = Đã nhập lại.'],
       'Trạng thái: Đã nhập lại', ['Tự nạp lại ở trang 1; "Hiển thị 1–10 / 21".'], 17)
S1.add('Sắp xếp tăng dần theo Mã phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Mã phiếu.'], '—',
       ['Xếp từ PXL-00001 trên cùng đến PXL-00010 ở dòng 10, mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Mã phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Mã phiếu 2 lần.'], '—',
       ['Xếp từ PXL-00023 trên cùng xuống, mũi tên xuống.'], 21)
S1.add('Sắp xếp theo Ngày tạo', 'P1', PRE_LIST, [MENU, 'Bấm tiêu đề Ngày tạo.', 'Bấm lần nữa.'], '—',
       ['Lần 1: cũ nhất trên (PXL-00001, 21/08/2025 10:11).', 'Lần 2: mới nhất trên (PXL-00023, 30/10/2026 10:54).',
        'Mặc định khi mới vào: mới nhất trên.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Phiếu nhập kho, Người tạo, Trạng thái, Hành động.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Mã phiếu (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 bắt đầu PXL-00011, tiếp tục thứ tự tăng.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 3.', 'Bấm tiêu đề Ngày tạo.'], '—', ['Về trang 1.'], 25)
S1.add('Bấm sắp xếp không làm vỡ bố cục bảng', 'P2', PRE_LIST, [MENU, 'Bấm tiêu đề Ngày tạo nhiều lần.'], '—',
       ['Độ rộng các cột giữ nguyên, mũi tên sắp xếp không nhảy chỗ.'], 22)
S1.add('Mở màn từ liên kết Phiếu xuất lại ở màn Phiếu nhập kho', 'P1',
       [PRE_LIST, 'Phiếu nhập kho PNK-11607 (Đã xuất lại) có ô "Phiếu xuất lại" = PXL-00022.'],
       [PNK_MENU, 'Mở chi tiết PNK-11607.', 'Bấm "PXL-00022" ở ô Phiếu xuất lại.'], '—',
       ['Mở màn "Chi tiết phiếu xuất điều chỉnh sai số liệu: PXL-00022".'], 1)
S1.add('Tạo phiếu xuất lại xong chuyển về danh sách', 'P0', PRE_FORM, XL, '—',
       ['Báo "Hàng đã được xuất lại".', 'Chuyển về màn "Danh sách phiếu xuất lại", phiếu mới ở dòng đầu, trạng thái Chờ nhập lại.'],
       [1, 274])
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo mã phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "PXL-00022", bấm Tìm kiếm.'], 'Ô tìm nhanh: PXL-00022',
       ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần mã phiếu', 'P0', PRE_LIST, [MENU, 'Nhập "0002", bấm Tìm kiếm.'], 'Ô tìm nhanh: 0002',
       ['Còn các phiếu có mã phiếu hoặc mã phiếu nhập kho chứa "0002" (có PXL-00002, PXL-00020 … PXL-00023).'], 27)
S2.add('Ô tìm nhanh tìm theo mã phiếu nhập kho', 'P0', PRE_LIST, [MENU, 'Nhập "PNK-11607", bấm Tìm kiếm.'], '—',
       ['Ra phiếu PXL-00022.'], 27)
S2.add('Ô tìm nhanh không tìm theo tên người', 'P1', PRE_LIST, [MENU, 'Nhập "Nguyễn Thu Hòa", bấm Tìm kiếm.'], '—',
       ['"Không có dữ liệu phù hợp." (tìm người dùng ô Người tạo).'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "pxl-00022", bấm Tìm kiếm.'], '—',
       ['Ra phiếu PXL-00022 như khi gõ chữ hoa.'], 28)
S2.add('Có dấu / không dấu', 'P2', PRE_LIST, [MENU, 'Nhập "pxl-00022" và "PXL-00022" (mã không có dấu tiếng Việt).'], '—',
       ['Kết quả như nhau.', 'Lưu ý: ô tìm nhanh chỉ tìm theo mã nên không có trường hợp có dấu.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; ký tự % được hiểu là ký tự đại diện nên ra cả 23 phiếu.'],
       31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  PXL-00022  ", bấm Tìm kiếm.'], '—',
       ['Ra phiếu PXL-00022 (bỏ khoảng trắng đầu / cuối).'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "PXL-00022", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Sau bước 2 hiện lại đủ 23 phiếu.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST,
       [MENU, 'Nhập "PXL-00022", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'], '—',
       ['Cả 2 cách đều ra phiếu PXL-00022, về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['Các ô Mã phiếu, Phiếu nhập kho, Người tạo, Trạng thái, Ngày tạo, Công ty, Phòng ban đều trống.', 'Đủ 23 phiếu.'], 36)
S2.add('Lọc Mã phiếu', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "00021" vào ô Mã phiếu.'], '—', ['Lọc ngay khi gõ; còn PXL-00021.'], 37)
S2.add('Lọc Phiếu nhập kho', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "11607" vào ô Phiếu nhập kho.'], '—', ['Còn PXL-00022.'], 37)
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = "HN_KHO_LN - Lưu Thị Hồng".'], '—',
       ['Còn 6 phiếu: PXL-00012, 00010, 00007, 00006, 00003, 00002.',
        'Ô Người tạo chỉ liệt kê 8 người đã tạo phiếu, dạng "Mã phòng ban - Họ tên".'], 37)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Chờ nhập lại.'], '—',
       ['Ô có 2 lựa chọn: Đã nhập lại, Chờ nhập lại.', 'Còn 2 phiếu PXL-00022, PXL-00020.'], 37)
S2.add('Lọc Ngày tạo lấy trọn ngày biên', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày tạo 27/10/2026 – 28/10/2026.'], '—',
       ['Còn 3 phiếu PXL-00022 (28/10 10:20), PXL-00021 (27/10 22:44), PXL-00020 (27/10 22:37).',
        'Bỏ trống ngày cuối vẫn lọc được từ ngày đầu.'], 37)
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = HDQT - DNS Admin.', 'Chọn Trạng thái = Đã nhập lại.'],
       '—', ['Chỉ còn PXL-00021.'], 38)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST,
       [MENU, 'Nhập "PXL-00022", bấm Tìm kiếm.', ADV, 'Chọn Trạng thái = Đã nhập lại.'], '—',
       ['"Không có dữ liệu phù hợp." vì PXL-00022 đang Chờ nhập lại.'], [39, 40])
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đã nhập lại.', 'Bấm trang cuối.'], '—',
       ['Dòng "Hiển thị" ghi tổng 21.', 'Trang 3 hiện "Hiển thị 21–21 / 21", STT liên tục.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Trạng thái = Đã nhập lại.', ['Bấm tiêu đề Mã phiếu.'], '—',
       ['Chỉ phiếu Đã nhập lại được sắp; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "PXL", lọc Người tạo, Trạng thái, sắp Mã phiếu, ở trang 2.',
       ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống, bỏ sắp xếp, nạp lại trang 1, đủ 23 phiếu.'], 44)
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.raw(org_cases(SCREEN, len(S2) + 1), [[37], [37], [37]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Chờ nhập lại, chưa mở màn chi tiết.'],
       ['Nhấn F5.'], '—', ['Bộ lọc trở về trống, đủ 23 phiếu (bộ lọc chỉ nhớ khi đi vào màn chi tiết của màn).'], 46)
S2.add('Ô Công ty chỉ có hiệu lực với quyền tổng công ty', 'P1', [ACC_Q2],
       ['Đăng nhập Q2.', MENU, ADV], '—', ['Không có ô Công ty, chỉ có ô Phòng ban.'], 37)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Phiếu nhập kho, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô Phiếu nhập kho.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Chờ nhập lại.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Trạng thái, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị bỏ, nạp lại đủ 23 phiếu.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Phiếu nhập kho.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Phiếu nhập kho vẫn ẩn.', 'Bước 2: tích đủ 6 mục, Phiếu nhập kho hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Ngày tạo lên đầu, bấm Lưu.'], '—',
       ['Ô Ngày tạo đứng đầu khối Tìm kiếm nâng cao; cấu hình giữ sau khi đăng nhập lại.'], 36)

# ============================================================== III. THÊM MỚI (Tạo phiếu xuất lại)
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo phiếu xuất lại', 'P0', PRE_FORM, ['Đăng nhập A.'] + TAO, '—',
       ['Mở TRANG "Tạo phiếu xuất lại", tab cùng tiêu đề.', 'Màn Danh sách phiếu xuất lại không có nút Tạo mới: lối vào duy nhất '
        'là nút "Tạo phiếu xuất lại" ở phiếu nhập kho Không duyệt.'], 49)
S3.add('Mở từ cột Hành động danh sách Phiếu nhập kho', 'P1', PRE_FORM,
       [PNK_MENU, 'Ở dòng PNK-11608 bấm biểu tượng "Tạo phiếu xuất lại".'], '—', ['Mở màn "Tạo phiếu xuất lại" của PNK-11608.'], 49)
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải "<tên A> - <ngày giờ hiện tại>".', 'Không có ô Mã phiếu (mã tự sinh khi lưu).'], 50)
S3.add('Các trường, khối và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Phiếu nhập kho (PNK-11608, liên kết), Người tạo, Kho (Kho Sài Gòn), Người giao hàng (78787), Lý do không '
        'duyệt (787), Ghi chú (gợi ý "Nhập ghi chú").',
        'Khối "Hàng hoá xuất lại": dòng "Toàn bộ hàng của phiếu nhập kho được xuất ra khỏi kho đúng lô, đúng vị trí đã nhập."; '
        'bảng STT, Tên hàng hoá, Model, Mã hàng hoá, Thương hiệu, ĐVT, SL đề nghị, SL thực nhập, Chi tiết (Vị trí, SL nhập), '
        'dòng Tổng cộng.', 'Chân màn: Xuất lại, Quay lại.'], [51, 54])
S3.add('Trường bắt buộc / không bắt buộc', 'P0', PRE_FORM, TAO + ['Quan sát dấu *.'], '—',
       ['Không ô nào có dấu *; chỉ Ghi chú nhập được (không bắt buộc), các ô khác khóa.', 'Số lượng trong bảng không sửa được.'],
       52)
S3.add('Giá trị mặc định', 'P0', PRE_FORM, TAO, '—',
       ['Các ô điền sẵn từ PNK-11608; Ghi chú trống.', 'Bảng 2 dòng: Bộ mũi khoét SL 1 tại SG-N1-D1-K1-T1, Bộ 13 mũi khoan SL 1 tại '
        'SG-N1-D1-K1-T2; Tổng cộng 2.'], [53, 269])
S3.add('Hộp xác nhận xuất lại', 'P0', PRE_FORM, TAO + ['Bấm "Xuất lại" ở chân màn.'], '—',
       ['Hiện hộp "Xác nhận xuất lại": "Toàn bộ hàng của phiếu PNK-11608 sẽ bị trừ khỏi tồn kho. Thao tác không hoàn tác được." '
        'với 2 nút Xuất lại, Đóng.'], [54, 95, 301])
S3.add('Xuất lại với dữ liệu hợp lệ đầy đủ', 'P0', PRE_FORM, TAO + ['Nhập Ghi chú.', 'Bấm "Xuất lại", rồi "Xuất lại" trong hộp.'],
       'Ghi chú: Nhập sai số lượng, xuất lại',
       ['Báo "Hàng đã được xuất lại", chuyển về Danh sách phiếu xuất lại.', 'Dòng mới trên cùng, mã PXL-NNNNN kế tiếp (PXL-00024), '
        'Phiếu nhập kho PNK-11608, Người tạo là A, nhãn vàng "Chờ nhập lại".'], [55, 92])
S3.add('Lưu chỉ với trường bắt buộc (bỏ trống Ghi chú)', 'P0', PRE_FORM, XL, 'Ghi chú: để trống',
       ['Lưu được; phiếu mới có Ghi chú trống.'], [56, 57])
S3.add('Dữ liệu sau lưu', 'P0', PRE_FORM, XL + ['Bấm mã phiếu vừa tạo.'], '—',
       ['Màn chi tiết: Phiếu nhập kho PNK-11608, Kho Sài Gòn, Người giao hàng 78787.',
        'Bảng 2 dòng đúng hàng, vị trí và SL như phiếu nhập kho.'], 58)
S3.add('Trạng thái mặc định sau lưu', 'P0', PRE_FORM, XL, '—',
       ['Phiếu xuất lại ở trạng thái Chờ nhập lại (nhãn vàng).', 'Phiếu nhập kho PNK-11608 chuyển "Đã xuất lại".'], [59, 281])
S3.add('Lịch sử tạo', 'P1', PRE_FORM, XL + ['Ở dòng phiếu mới bấm Lịch sử.'], '—',
       ['Có 1 mốc "Tạo mới", người thực hiện A, thời gian lúc lưu.'], [60, 176])
S3.add('Không có trường bắt buộc nào để bỏ trống', 'P1', PRE_FORM, XL, 'Mọi ô để nguyên',
       ['Lưu được ngay; màn không có trường bắt buộc nhập tay.'], 61)
S3.add('Ghi chú quá 255 ký tự bị chặn', 'P0', PRE_FORM, TAO + ['Dán chuỗi 300 ký tự vào Ghi chú.', 'Bấm "Xuất lại", rồi "Xuất lại" '
       'trong hộp.'], 'Ghi chú: 300 ký tự',
       ['Viền đỏ, dưới ô hiện "Không được vượt quá 255 ký tự"; thông báo cùng câu.', 'Không tạo phiếu, không trừ tồn.'],
       [62, 66, 70])
S3.add('Ghi chú đúng 255 ký tự', 'P1', PRE_FORM, TAO + ['Nhập Ghi chú đúng 255 ký tự.', 'Xác nhận Xuất lại.'], 'Ghi chú: 255 ký tự',
       ['Lưu được, hiển thị đủ 255 ký tự ở màn chi tiết.'], 65)
S3.add('Ghi chú 1 ký tự', 'P2', PRE_FORM, TAO + ['Nhập Ghi chú "a".', 'Xác nhận Xuất lại.'], 'Ghi chú: a',
       ['Lưu được; không có độ dài tối thiểu.'], 64)
S3.add('Ký tự đặc biệt trong Ghi chú', 'P2', PRE_FORM, TAO + ['Nhập Ghi chú "<b>Test</b> & @#$%".', 'Xác nhận Xuất lại.'], '—',
       ['Lưu được; màn chi tiết và bản in hiện nguyên chuỗi, không in đậm.'], 63)
S3.add('Ghi chú có khoảng trắng đầu / cuối', 'P2', PRE_FORM, TAO + ['Nhập Ghi chú "  Xuất lại  ".', 'Xác nhận Xuất lại.'], '—',
       ['Lưu được; Ghi chú hiển thị "Xuất lại" (khoảng trắng đầu / cuối bị bỏ khi lưu).'], 68)
S3.add('Ghi chú chỉ có khoảng trắng', 'P2', PRE_FORM, TAO + ['Nhập Ghi chú "   ".', 'Xác nhận Xuất lại.'], 'Ghi chú: 3 khoảng trắng',
       ['Lưu được (Ghi chú không bắt buộc); Ghi chú hiển thị trống.'], 69)
S3.add('Không xuất lại được 2 lần cho cùng phiếu nhập kho', 'P0', [PRE_FORM, 'Đã tạo phiếu xuất lại cho PNK-11608.'],
       [PNK_MENU, 'Mở chi tiết PNK-11608.'], '—',
       ['Phiếu nhập kho đã "Đã xuất lại", không còn nút "Tạo phiếu xuất lại".',
        'Phiếu không có trường nhập duy nhất: mã PXL tự sinh, không trùng.'], [67, 89])
S3.add('Lỗi biến mất sau khi sửa', 'P1', PRE_FORM, TAO + ['Nhập Ghi chú 300 ký tự, xác nhận (báo lỗi).', 'Xóa bớt còn 100 ký tự, '
       'xác nhận lại.'], '—', ['Lưu được; chữ đỏ dưới ô không còn.'], 71)
S3.add('Kho không đủ tồn thì bị chặn', 'P0', [PRE_FORM, 'Tồn của "Bộ mũi khoét (5 chi tiết)" tại SG-N1-D1-K1-T1 đã bị xuất hết bởi '
       'phiếu khác.'], XL, '—',
       ['Thông báo "Hàng Bộ mũi khoét (5 chi tiết) không đủ tồn tại vị trí SG-N1-D1-K1-T1. Cần 1, còn 0" (hoặc câu "không đủ tồn '
        'kho" / "không đủ tồn trong lô" tương ứng).', 'Không tạo phiếu, không trừ tồn dòng nào, phiếu nhập kho vẫn Không duyệt.'],
       [62, 304, 285])
S3.add('Phiếu đổi trạng thái trong lúc đang mở màn', 'P1', [PRE_FORM, 'Tab 1 đang mở màn Tạo phiếu xuất lại; tab 2 vừa xuất lại '
       'xong PNK-11608.'], ['Ở tab 1 bấm "Xuất lại", rồi "Xuất lại" trong hộp.'], '—',
       ['Thông báo "Chỉ người tạo phiếu nhập kho bị Không duyệt mới được tạo phiếu xuất lại.".', 'Không tạo phiếu thứ 2.'],
       [102, 311])
S3.add('Bấm Đóng trong hộp xác nhận', 'P0', PRE_FORM, TAO + ['Nhập Ghi chú.', 'Bấm "Xuất lại".', 'Bấm "Đóng" trong hộp.'], '—',
       ['Hộp đóng, vẫn ở màn Tạo phiếu xuất lại, Ghi chú giữ nguyên.', 'Không tạo phiếu; PNK-11608 vẫn Không duyệt.'], [97, 310])
S3.add('Bấm (x) trong hộp xác nhận', 'P1', PRE_FORM, TAO + ['Bấm "Xuất lại".', 'Bấm (x) góc hộp.'], '—',
       ['Hộp đóng, không tạo phiếu.'], 95)
S3.add('Quay lại khi chưa nhập gì', 'P1', PRE_FORM, TAO + ['Bấm Quay lại.'], '—', ['Về chi tiết PNK-11608 ngay, không hỏi.'], 93)
S3.add('Quay lại khi đã nhập Ghi chú', 'P1', PRE_FORM, TAO + ['Nhập Ghi chú.', 'Bấm Quay lại.'], '—',
       ['Về chi tiết PNK-11608 NGAY, không có hộp "Thông tin chưa lưu"; Ghi chú bị bỏ.',
        'Lưu ý: màn chưa có cảnh báo chưa lưu — ghi nhận theo hành vi hiện tại.'], [94, 96])
S3.add('Nhập rồi xóa hết Ghi chú', 'P2', PRE_FORM, TAO + ['Nhập Ghi chú rồi xóa hết.', 'Bấm Quay lại.'], '—',
       ['Về chi tiết phiếu nhập kho ngay.'], [98, 99])
S3.add('Để màn lâu không thao tác', 'P2', [PRE_FORM, 'Đã mở màn, để nguyên 30 phút.'], ['Xác nhận Xuất lại.'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên đăng nhập, về màn đăng nhập, không lưu.'], 100)
S3.add('Bấm Xuất lại liên tục', 'P1', PRE_FORM, TAO + ['Bấm "Xuất lại" trong hộp 3 lần thật nhanh.'], '—',
       ['Nút khóa trong lúc lưu; chỉ tạo 1 phiếu, tồn chỉ bị trừ 1 lần.'], 101)
S3.add('Không phải người tạo phiếu nhập kho', 'P0', [ACC_Q1, PNK], ['Đăng nhập Q1.', PNK_MENU, 'Mở chi tiết PNK-11608.'], '—',
       ['Không có nút "Tạo phiếu xuất lại".'], [52, 295])
S3.add('Mở thẳng màn Tạo phiếu xuất lại khi không đủ điều kiện', 'P1',
       [ACC_Q1, 'Q1 có đường link màn Tạo phiếu xuất lại của PNK-11608 do A gửi.'], ['Đăng nhập Q1, mở đường link.'], '—',
       ['Báo "Phiếu không xuất lại được hoặc bạn không có quyền.", quay về danh sách Phiếu nhập kho.'], [52, 296])
S3.add('Phiếu nhập kho không ở trạng thái Không duyệt', 'P1', [ACC_A, 'Phiếu nhập kho PNK-11700 do A tạo đang Chờ duyệt.'],
       [PNK_MENU, 'Mở chi tiết PNK-11700.'], '—', ['Không có nút "Tạo phiếu xuất lại".'], 52)
S3.add('Liên kết Phiếu nhập kho trên màn tạo', 'P2', PRE_FORM, TAO + ['Bấm "PNK-11608" ở ô Phiếu nhập kho.'], '—',
       ['Mở chi tiết phiếu nhập kho PNK-11608.'], 51)

# ============================================================== IV. LỊCH SỬ THAY ĐỔI
S4 = Sec(4)
S4.add('Mở cửa sổ lịch sử từ danh sách', 'P0', [PRE_LIST, P21], [MENU, 'Tìm PXL-00021.', 'Bấm Lịch sử ở cột Hành động.'], '—',
       ['Mở cửa sổ "Lịch sử thay đổi: PXL-00021", nút Bộ lọc, nút Đóng.'], 162)
S4.add('Thông tin mỗi mốc', 'P0', [PRE_LIST, P21], [MENU, 'Mở lịch sử PXL-00021.'], '—',
       ['Mốc "Thay đổi trạng thái" 28/10/2026 09:14, "Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ", "Trạng thái: Chờ nhập lại sang '
        'Đã nhập lại", ghi chú "Tạo phiếu nhập lại PNK-11606".', 'Mốc "Tạo mới" 27/10/2026 22:44, người thực hiện DNS Admin.'],
       [163, 165, 166, 167, 168])
S4.add('Mới nhất ở trên', 'P1', [PRE_LIST, P21], [MENU, 'Mở lịch sử PXL-00021.'], '—',
       ['Mốc Thay đổi trạng thái nằm trên mốc Tạo mới.'], 164)
S4.add('Phiếu lập từ hệ thống cũ vẫn có mốc Tạo mới', 'P1',
       [PRE_LIST, 'PXL-00023 (Người tạo Nguyễn Thị Thu Huyền, 30/10/2026 10:54) chưa có mốc ghi thật.'],
       [MENU, 'Mở lịch sử PXL-00023.'], '—',
       ['Có 1 mốc "Tạo mới" 30/10/2026 10:54, người thực hiện Nguyễn Thị Thu Huyền.', 'Không hiện "Chưa có lịch sử".'], 173)
S4.add('Lọc theo loại hành động', 'P1', [PRE_LIST, P21],
       [MENU, 'Mở lịch sử PXL-00021.', 'Bấm Bộ lọc, chọn Loại hành động = Tạo mới.', 'Đổi thành Thay đổi thông tin.'], '—',
       ['Bước 3: còn mốc Tạo mới.', 'Bước 4: "Không có lịch sử phù hợp bộ lọc.".',
        'Ô Loại hành động có: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.'], [169, 173, 175])
S4.add('Lọc theo người thực hiện', 'P2', [PRE_LIST, P21], [MENU, 'Mở lịch sử, bấm Bộ lọc, chọn Người thực hiện = DNS Admin.'], '—',
       ['Còn 2 mốc của DNS Admin.'], 170)
S4.add('Lọc theo thời gian và kết hợp', 'P2', [PRE_LIST, P21],
       [MENU, 'Mở lịch sử, bấm Bộ lọc.', 'Chọn Từ ngày 28/10/2026, Đến ngày 28/10/2026.', 'Thêm Loại hành động = Tạo mới.'], '—',
       ['Bước 3: còn mốc Thay đổi trạng thái.', 'Bước 4: không còn mốc nào.'], [171, 172])
S4.add('Làm mới bộ lọc lịch sử', 'P2', 'Đang lọc lịch sử theo Loại hành động.', ['Bấm Làm mới trong khối lọc.'], '—',
       ['Xóa điều kiện, hiện lại đủ mốc.'], 174)
S4.add('Ghi mốc khi tạo phiếu nhập lại', 'P0', [ACC_A, 'Phiếu PXL-00024 (Chờ nhập lại) vừa tạo từ PNK-11608.'],
       [MENU, 'Ở dòng PXL-00024 bấm Tạo phiếu nhập lại, nhập đủ thông tin, bấm Lưu và nhập.', 'Mở lịch sử PXL-00024.'], '—',
       ['Có thêm mốc "Thay đổi trạng thái": Chờ nhập lại sang Đã nhập lại, ghi chú "Tạo phiếu nhập lại PNK-…" (mã phiếu nhập kho mới).'],
       [183, 312])
S4.add('Xem, in, xuất không ghi lịch sử', 'P1', [PRE_LIST, P21],
       [MENU, 'Mở chi tiết PXL-00021, bấm In, đóng.', 'Xuất Excel danh sách.', 'Mở lịch sử PXL-00021.'], '—',
       ['Vẫn chỉ có 2 mốc.'], 182)
S4.add('Đóng cửa sổ lịch sử', 'P1', [PRE_LIST, 'Đang ở trang 2, lọc Trạng thái = Đã nhập lại.'],
       ['Mở lịch sử 1 phiếu.', 'Bấm Đóng.', 'Mở lại, bấm (x).'], '—',
       ['Cửa sổ đóng; danh sách giữ trang 2, bộ lọc, sắp xếp, không nạp lại.'], [184, 185])
S4.add('Khối Lịch sử ở màn chi tiết', 'P1', [PRE_LIST, P21], [MENU, 'Mở chi tiết PXL-00021.', 'Bấm Xem lịch sử ở khối Lịch sử.'], '—',
       ['Khối mở rộng, cùng 2 mốc như cửa sổ ở danh sách; có nút Làm mới, Thu gọn, Bộ lọc.'], [162, 195])

# ============================================================== V. XEM CHI TIẾT
S5 = Sec(5)
S5.add('Mở màn chi tiết', 'P0', [PRE_LIST, P22], [MENU, 'Bấm mã PXL-00022.'], '—',
       ['Mở TRANG "Chi tiết phiếu xuất điều chỉnh sai số liệu: PXL-00022" kèm nhãn vàng "Chờ nhập lại".'], [186, 187])
S5.add('Đầy đủ trường thông tin', 'P0', [PRE_LIST, P22], [MENU, 'Mở chi tiết PXL-00022.'], '—',
       ['Khối Thông tin chung: Phiếu nhập kho (PNK-11607), Loại nhập "Nhập hàng mua trong nước (TỰ DO + HÃNG)", Kho "Kho Sài Gòn", '
        'Người giao hàng "trang gấu", Ghi chú "Ghi chú trang".', 'Góc phải "DNS Admin - 28/10/2026 10:20".',
        'Không có ô Trạng thái trong khối (trạng thái ở tiêu đề).'], [188, 189])
S5.add('Bảng chi tiết khớp dữ liệu', 'P0', [PRE_LIST, P22], [MENU, 'Mở chi tiết PXL-00022.'], '—',
       ['Dòng 1: Xe bảo dưỡng nhanh EM tiêu chuẩn Vinfast, MN-EM.VF, SG-MN-EMVF, KOURITSU, Cái, Tổng SL 16.',
        'Chi tiết: SG-N1-D1-K1-T1 SL 15; SG-N1-D1-K1-T5 SL 1.'], [189, 190])
S5.add('Mọi trường chỉ đọc, không có nút Lưu', 'P0', [PRE_LIST, P22], [MENU, 'Mở chi tiết PXL-00022.', 'Thử gõ vào các ô.'], '—',
       ['Các ô khóa, không sửa được.', 'Chân màn: Tạo phiếu nhập lại, In, Quay lại; không có Sửa, Xóa, Lưu.'], [191, 192, 193])
S5.add('Phiếu Đã nhập lại không có Tạo phiếu nhập lại', 'P0', [PRE_LIST, P21], [MENU, 'Mở chi tiết PXL-00021.'], '—',
       ['Tiêu đề kèm nhãn xanh lá "Đã nhập lại".', 'Chân màn chỉ có In, Quay lại.'], 193)
S5.add('Phiếu không có trạng thái khóa', 'P2', [PRE_LIST, P22], [MENU, 'Mở chi tiết PXL-00022.'], '—',
       ['Màn không có trạng thái Khóa; phiếu chỉ Chờ nhập lại / Đã nhập lại.'], 194)
S5.add('Liên kết phiếu nhập kho mở tab mới', 'P1', [PRE_LIST, P22], [MENU, 'Mở chi tiết PXL-00022.', 'Bấm "PNK-11607".'], '—',
       ['Mở chi tiết phiếu nhập kho PNK-11607 ở tab mới; màn chi tiết giữ nguyên.'], 190)
S5.add('Quay lại giữ trang và bộ lọc', 'P0', [PRE_LIST, 'Đang ở trang 2, lọc Trạng thái = Đã nhập lại.'],
       ['Bấm mã một phiếu.', 'Bấm Quay lại.'], '—', ['Về danh sách, còn bộ lọc Trạng thái (trong 10 phút).'], [196, 197])
S5.add('Mở chi tiết phiếu không tồn tại', 'P2', PRE_LIST, ['Mở đường dẫn chi tiết với số phiếu 999999 (sửa tay trên thanh địa chỉ).'],
       '—', ['Chuyển sang trang không tìm thấy; không treo trang, không báo lỗi nổi.'], 186)

# ============================================================== VI. IN PHIẾU
S6 = Sec(6)
S6.add('In phiếu từ danh sách', 'P0', [PRE_LIST, P22], [MENU, 'Ở dòng PXL-00022 bấm In.'], '—',
       ['Mở cửa sổ "Xem trước phiếu xuất lại PXL-00022" ngay trên danh sách.',
        'Bản in: logo + tên công ty, "PHIẾU XUẤT LẠI ĐIỀU CHỈNH SAI SỐ LIỆU", Số phiếu PXL-00022, Ngày tạo 28/10/2026 10:20.',
        'Thông tin: Người tạo DNS Admin, Phiếu nhập kho PNK-11607, Loại nhập, Kho Sài Gòn, Người giao hàng trang gấu, Ghi chú, '
        'Trạng thái Chờ nhập lại.', 'Bảng hàng có Chi tiết Vị trí / SL; chỗ ký Người lập, Kế toán kho, Thủ kho.'], 188)
S6.add('In phiếu từ màn chi tiết', 'P1', [PRE_LIST, P22], [MENU, 'Mở chi tiết PXL-00022.', 'Bấm In ở chân màn.'], '—',
       ['Mở cùng cửa sổ xem trước; bấm In trong cửa sổ mở hộp thoại in của trình duyệt.'], 188)
S6.add('Letterhead theo công ty của phiếu', 'P1', [ACC_Q1, 'Q1 thuộc Công ty Hà Nội; PXL-00022 thuộc Công ty Sài Gòn.'],
       ['Đăng nhập Q1.', MENU, 'In phiếu PXL-00022.'], '—', ['Đầu bản in là letterhead Công ty Sài Gòn, không theo công ty của Q1.'],
       188)
S6.add('Hàng nhiều vị trí in thành nhóm', 'P2', [PRE_LIST, P22], [MENU, 'In phiếu PXL-00022.'], '—',
       ['Dòng hàng gộp ô cho 2 vị trí; khi sang trang không bị cắt ngang nhóm.'], 188)
S6.add('Ghi chú trống thì bỏ dòng', 'P2', [PRE_LIST, 'PXL-00023 không có ghi chú.'], [MENU, 'In phiếu PXL-00023.'], '—',
       ['Bản in không có dòng Ghi chú.'], 188)
S6.add('Đóng cửa sổ xem trước', 'P2', PRE_LIST, [MENU, 'In 1 phiếu.', 'Bấm (x).'], '—', ['Cửa sổ đóng, danh sách giữ nguyên.'], 184)
S6.add('In phiếu ngoài phạm vi', 'P1', [ACC_N], ['Đăng nhập N.', 'Mở đường link chi tiết PXL-00022 do người khác gửi.'], '—',
       ['Chuyển trang không tìm thấy; không xem được bản in.'], [296, 188])

# ============================================================== VII. TÙY CHỈNH CỘT
S7 = Sec(7)
S7.add('Mở cửa sổ Tùy chỉnh cột', 'P0', PRE_LIST, [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột", dòng hướng dẫn, Chọn tất cả, Bỏ chọn hết, danh sách 7 cột, "Đang chọn 7/7 cột", Lưu, Đóng.'],
       [198, 199, 200])
S7.add('Ẩn một cột', 'P0', PRE_LIST, [MENU, 'Mở Tùy chỉnh cột, bỏ tích Người tạo, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công"; bảng không còn cột Người tạo; "Đang chọn 6/7 cột" khi mở lại.'], [202, 206])
S7.add('Hiện lại cột đã ẩn', 'P0', 'Đã ẩn cột Người tạo.', ['Mở Tùy chỉnh cột, tích Người tạo, bấm Lưu.'], '—',
       ['Cột Người tạo hiện lại.'], 201)
S7.add('Cột bắt buộc không ẩn được', 'P0', PRE_LIST, [MENU, 'Mở Tùy chỉnh cột, bấm Bỏ chọn hết.'], '—',
       ['STT, Mã phiếu, Hành động vẫn tích (biểu tượng ổ khóa); các cột khác bỏ tích.'], [203, 205])
S7.add('Kéo đổi thứ tự cột', 'P1', PRE_LIST, ['Mở Tùy chỉnh cột, kéo Ngày tạo lên trên Phiếu nhập kho, bấm Lưu.'], '—',
       ['Bảng hiện Ngày tạo trước Phiếu nhập kho; cột khóa không kéo được.'], 204)
S7.add('Đóng không lưu', 'P1', PRE_LIST, ['Mở Tùy chỉnh cột, bỏ tích Trạng thái.', 'Bấm Đóng.'], '—',
       ['Bảng vẫn còn cột Trạng thái.'], 207)
S7.add('Ghi nhớ sau F5 và theo tài khoản', 'P1', 'Q1 đã ẩn cột Người tạo.',
       ['Nhấn F5.', 'Đăng nhập Q1 trên trình duyệt khác.', 'Đăng nhập DNS Admin.'], '—',
       ['Bước 1, 2: cột Người tạo vẫn ẩn.', 'Bước 3: DNS Admin vẫn thấy đủ 7 cột.'], [208, 209])
S7.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', 'Đang lọc Trạng thái = Đã nhập lại, tổng 21 phiếu.', ['Ẩn cột Trạng thái, Lưu.'],
       '—', ['Bộ lọc giữ nguyên, tổng vẫn 21.'], [210, 211])

# ============================================================== VIII. XUẤT DANH SÁCH EXCEL
S8 = Sec(8)
S8.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất Excel", 5 trường tích sẵn: Mã phiếu, Phiếu nhập kho, Ngày tạo, Người tạo, Trạng thái; "Đang chọn '
        '5/5 trường"; nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng.'], [212, 213])
S8.add('Trường tích sẵn theo cột đang hiện', 'P1', 'Đã ẩn cột Người tạo bằng Tùy chỉnh cột.', ['Bấm Xuất Excel.'], '—',
       ['Trường Người tạo không được tích sẵn; "Đang chọn 4/5 trường".'], 214)
S8.add('Xuất với trường mặc định', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel, bấm Xuất file.'], '—',
       ['Tải file "danh_sach_phieu_xuat_lai.xlsx", báo "Xuất Excel thành công".', 'File: tiêu đề "DANH SÁCH PHIẾU XUẤT ĐIỀU CHỈNH SAI '
        'SỐ LIỆU", dòng tên cột STT + 5 cột, 23 dòng dữ liệu (không phân trang), khối ký "Người lập" cuối file.'],
       [215, 216, 221, 223, 224, 225, 227])
S8.add('Xuất một số trường theo thứ tự chọn', 'P0', PRE_LIST,
       [MENU, 'Bấm Xuất Excel, Bỏ chọn hết.', 'Tích Ngày tạo, rồi Mã phiếu.', 'Kéo Mã phiếu lên trên, bấm Xuất file.'], '—',
       ['File chỉ có STT, Mã phiếu, Ngày tạo đúng thứ tự trong cửa sổ.'], [217, 226])
S8.add('Không chọn trường nào', 'P1', PRE_LIST, [MENU, 'Bấm Xuất Excel, Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S8.add('Xuất theo từ khóa và bộ lọc', 'P0', PRE_LIST,
       [MENU, 'Nhập "PXL-0002", Tìm kiếm.', ADV, 'Chọn Trạng thái = Chờ nhập lại.', 'Xuất Excel, Xuất file.'], '—',
       ['File chỉ có PXL-00022, PXL-00020 (đúng các phiếu đang hiện trên màn).'], [219, 220])
S8.add('Xuất danh sách rỗng', 'P1', PRE_LIST, [MENU, 'Tìm "ZZZ999".', 'Xuất Excel, Xuất file.'], '—',
       ['Không tải file, báo "Không có dữ liệu để xuất".'], 222)
S8.add('Dữ liệu và định dạng trong file khớp màn', 'P0', [PRE_LIST, P22], [MENU, 'Xuất toàn bộ trường.', 'Mở file, tìm PXL-00022.'],
       '—', ['Phiếu nhập kho PNK-11607, Ngày tạo "28/10/2026 10:20", Người tạo "HDQT - DNS Admin", Trạng thái "Chờ nhập lại".',
             'Mã phiếu không bị Excel cảnh báo số dạng chữ.'], [228, 229])
S8.add('Tiếng Việt trong file', 'P2', PRE_LIST, ['Xuất file, mở cột Người tạo, Trạng thái.'], '—',
       ['"Nguyễn Thị Thu Huyền", "Đã nhập lại" hiện đúng dấu, không lỗi phông.'], 230)
S8.add('Xuất theo phạm vi xem', 'P0', [ACC_N], ['Đăng nhập N.', MENU, 'Xuất Excel, Xuất file.'], '—',
       ['File chỉ có 1 dòng PXL-00099 (phiếu của N).'], [293, 299])
S8.add('Đóng không xuất', 'P2', PRE_LIST, [MENU, 'Bấm Xuất Excel, bấm Đóng.'], '—', ['Không tải file.'], 214)

# ============================================================== IX. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S9 = Sec(9)
RI = [MENU, 'Ở dòng PXL-00024 (Chờ nhập lại) bấm "Tạo phiếu nhập lại".']
PRE_RI = ACC_A + '\nA vừa tạo PXL-00024 (Chờ nhập lại) từ PNK-11608; PNK-11608 đang Đã xuất lại.'
S9.add('Điều kiện hiện nút Tạo phiếu nhập lại', 'P0', [PRE_RI, 'PXL-00021 Đã nhập lại.'], ['Đăng nhập A.', MENU], '—',
       ['Dòng PXL-00024: có nút Tạo phiếu nhập lại.', 'Dòng Đã nhập lại: chỉ In, Lịch sử.'], [281, 300])
S9.add('Người khác không thấy nút Tạo phiếu nhập lại', 'P0', [ACC_Q1, 'PXL-00024 do A tạo, Chờ nhập lại.'],
       ['Đăng nhập Q1.', MENU, 'Tìm PXL-00024.', 'Mở chi tiết PXL-00024.'], '—',
       ['Dòng và màn chi tiết không có nút Tạo phiếu nhập lại (kể cả Super admin).'], 295)
S9.add('Mở màn Tạo phiếu nhập lại', 'P0', PRE_RI, RI, '—',
       ['Mở TRANG "Tạo phiếu nhập lại" điền sẵn dữ liệu PNK-11608; ô Người giao hàng khóa; file đính kèm trống.',
        'Chân màn: Lưu, Lưu và nhập, Quay lại.'], 49)
S9.add('Lưu và nhập phiếu nhập lại đổi trạng thái phiếu xuất lại', 'P0', PRE_RI,
       RI + ['Đính kèm file, kiểm số lượng, vị trí.', 'Bấm Lưu và nhập.', MENU], '—',
       ['Sinh phiếu nhập kho mới; về danh sách Phiếu nhập kho.', 'PXL-00024 chuyển "Đã nhập lại" (nhãn xanh lá), mất nút Tạo phiếu '
        'nhập lại.', 'PNK-11608 chuyển "Đã nhập lại".'], [281, 302, 305, 306, 307])
S9.add('Lưu (Đang tạo) cũng đổi trạng thái', 'P1', PRE_RI, RI + ['Nhập đủ, bấm Lưu.', MENU], '—',
       ['Phiếu nhập kho mới ở trạng thái Đang tạo.', 'PXL-00024 vẫn chuyển "Đã nhập lại".'], [281, 305])
S9.add('Quay lại khi đã sửa ở màn nhập lại', 'P1', PRE_RI, RI + ['Sửa SL một dòng.', 'Bấm Quay lại.', 'Bấm Thoát.', MENU], '—',
       ['Bước 4: hiện hộp "Thông tin chưa lưu" (Thoát / Ở lại).', 'Sau khi Thoát: PXL-00024 vẫn "Chờ nhập lại".'], [310, 96])
S9.add('Lưu nhập lại khi dữ liệu sai', 'P1', PRE_RI, RI + ['Không đính kèm file, bấm Lưu và nhập.'], '—',
       ['Báo lỗi tại ô như màn Nhập kho; PXL-00024 vẫn Chờ nhập lại.'], [303, 304])
S9.add('Không nhập lại 2 lần', 'P0', [PRE_RI, 'Tab 2 vừa lưu phiếu nhập lại cho PNK-11608.'], ['Ở tab 1 (đang mở màn nhập lại) bấm '
       'Lưu và nhập.'], '—', ['Báo "Bạn không có quyền nhập lại phiếu này."; không sinh phiếu thứ 2.'], [311, 102])
S9.add('Tạo phiếu xuất lại chuyển phiếu nhập kho sang Đã xuất lại', 'P0', PRE_FORM, XL + [PNK_MENU, 'Mở chi tiết PNK-11608.'], '—',
       ['PNK-11608 trạng thái "Đã xuất lại"; ô "Phiếu xuất lại" = mã phiếu vừa tạo (liên kết).',
        'Lịch sử PNK-11608 có mốc đổi trạng thái ghi "Tạo phiếu xuất lại PXL-…".', 'Có nút "Tạo phiếu nhập lại".'],
       [274, 281, 284])
S9.add('Tồn kho giảm sau xuất lại', 'P0', [PRE_FORM, 'Báo cáo tồn kho theo vị trí: Bộ mũi khoét tại SG-N1-D1-K1-T1 tồn 1.'],
       XL + ['Vào phân hệ Kho > menu "Báo cáo kho" > "Báo cáo tồn kho theo vị trí", xem Bộ mũi khoét.'], '—',
       ['Tồn tại SG-N1-D1-K1-T1 giảm 1 (về 0); tương tự với Bộ 13 mũi khoan tại SG-N1-D1-K1-T2.'], [274, 307])
S9.add('Thẻ kho hiện dòng xuất lại', 'P0', [PRE_FORM, 'Đã xuất lại PNK-11608 thành PXL-00024.'],
       ['Vào phân hệ Kho > menu "Báo cáo kho" > "Thẻ kho", chọn Kho Sài Gòn, hàng Bộ mũi khoét.', 'Bấm số chứng từ PXL-00024.'], '—',
       ['Có dòng xuất 1 với số chứng từ PXL-00024.', 'Bấm số chứng từ mở chi tiết phiếu xuất lại PXL-00024 ở tab mới.'], [274, 279])
S9.add('Tổng hợp xuất nhập tồn tăng số xuất', 'P1', [PRE_FORM, 'Đã xuất lại PNK-11608 hôm nay.'],
       ['Vào phân hệ Kho > menu "Báo cáo kho" > "Tổng hợp xuất nhập tồn", kỳ hôm nay, Kho Sài Gòn.'], '—',
       ['Bộ mũi khoét có số xuất 1 trong kỳ.'], 274)
S9.add('Bộ lọc màn Phiếu nhập kho cập nhật', 'P1', [PRE_FORM, 'Vừa xuất lại PNK-11608.'],
       [PNK_MENU, 'Lọc Trạng thái = Không duyệt.', 'Lọc Trạng thái = Đã xuất lại.'], '—',
       ['Bước 2: không còn PNK-11608.', 'Bước 3: có PNK-11608.'], 282)
S9.add('Đổi tên hàng ở danh mục không làm đổi phiếu đã lập', 'P1', [PRE_LIST, P22],
       ['Đổi tên hàng "Xe bảo dưỡng nhanh EM tiêu chuẩn Vinfast" ở danh mục hàng hóa.', 'Mở chi tiết PXL-00022.'], '—',
       ['Phiếu vẫn hiện tên cũ (tên lưu cố định lúc tạo).'], [278, 272])
S9.add('Không xóa được vị trí đã có trên phiếu', 'P1', [PRE_LIST, P22],
       ['Vào phân hệ Kho > menu "Danh mục" > "Vị trí".', 'Xóa vị trí SG-N1-D1-K1-T5.'], '—',
       ['Hệ thống không cho xóa vì vị trí đã được dùng trên chứng từ (trong đó có PXL-00022).'], 270)
S9.add('Dòng chi tiết đúng phiếu nhập kho gốc', 'P0', [PRE_LIST, P22], [MENU, 'Mở chi tiết PXL-00022 và chi tiết PNK-11607.'], '—',
       ['Hàng, đơn vị, vị trí, SL của phiếu xuất lại trùng các dòng đã nhập của PNK-11607.'], [283, 286])
S9.add('Lưu lỗi giữa chừng không sinh phiếu dở dang', 'P1', [PRE_FORM, 'Dòng 2 không đủ tồn (dòng 1 đủ).'],
       XL + ['Xem danh sách phiếu xuất lại, tồn dòng 1, trạng thái PNK-11608.'], '—',
       ['Không có phiếu mới; tồn dòng 1 không đổi; PNK-11608 vẫn Không duyệt.'], [285, 286])
S9.add('Phiếu mới xuất hiện cho người xem theo phạm vi', 'P1', [ACC_Q2, 'A (Công ty Sài Gòn) vừa tạo PXL-00024.'],
       ['Đăng nhập Q2.', MENU], '—', ['Q2 thấy PXL-00024 ở đầu danh sách.'], [274, 299])

# ============================================================== X. PHÂN QUYỀN (cuối)
S10 = Sec(10)
S10.add('Quyền Xem theo tổng công ty', 'P0', ACC_Q1, ['Đăng nhập Q1.', MENU, ADV], '—',
        ['Thấy đủ 23 phiếu của mọi công ty.', 'Có ô lọc Công ty và Phòng ban.'], [287, 299])
S10.add('Quyền Xem theo công ty', 'P0', [ACC_Q2, 'Có phiếu của Công ty Sài Gòn (PXL-00022) và phiếu của Công ty Hà Nội (PXL-00012).'],
        ['Đăng nhập Q2.', MENU, ADV], '—',
        ['Thấy PXL-00022, KHÔNG thấy PXL-00012; chỉ phiếu của Công ty Sài Gòn và phiếu Q2 tự tạo.', 'Có ô Phòng ban, không có ô Công ty.'], [287, 299])
S10.add('Quyền Xem theo phòng ban', 'P0', ACC_Q3, ['Đăng nhập Q3.', MENU], '—',
        ['Chỉ thấy phiếu của phòng / bộ phận Q3 quản lý (SG_KHO) và phiếu Q3 tự tạo.', 'Không có ô Công ty, Phòng ban.'], [287, 299])
S10.add('Quyền Xem theo bộ phận', 'P0', ACC_Q4, ['Đăng nhập Q4.', MENU], '—',
        ['Chỉ thấy phiếu của bộ phận Q4 quản lý và phiếu Q4 tự tạo.'], [287, 299])
S10.add('Không có quyền nào', 'P0', ACC_N, ['Đăng nhập N.', MENU], '—',
        ['Menu vẫn hiện, mở được màn.', 'Chỉ thấy 1 phiếu PXL-00099 do N tạo; không báo lỗi.'], [287, 295, 299])
S10.add('Có nhiều quyền thì áp quyền cao nhất', 'P1', 'Tài khoản có cả quyền theo bộ phận và theo tổng công ty.',
        ['Đăng nhập.', MENU], '—', ['Thấy đủ 23 phiếu.'], 299)
S10.add('Quyền xem chi tiết trong phạm vi', 'P0', [ACC_Q2, P22], ['Đăng nhập Q2.', MENU, 'Mở chi tiết PXL-00022.'], '—',
        ['Xem được đầy đủ.'], 288)
S10.add('URL chi tiết ngoài phạm vi', 'P0', [ACC_N, 'N có đường link chi tiết PXL-00022 do người khác gửi.'],
        ['Đăng nhập N, mở đường link.'], '—', ['Chuyển sang trang không tìm thấy; không lộ dữ liệu phiếu.'], [288, 296])
S10.add('Xem được chi tiết khi xem được phiếu nhập kho gốc', 'P1',
        ['Tài khoản K: không có quyền xem phiếu xuất lại; là Kế toán kho cùng công ty, xem được PNK-11607.'],
        ['Đăng nhập K.', PNK_MENU, 'Mở chi tiết PNK-11607, bấm "PXL-00022" ở ô Phiếu xuất lại.'], '—',
        ['Mở được chi tiết PXL-00022 dù danh sách của K không có phiếu này.'], 288)
S10.add('Tạo phiếu xuất lại theo người tạo phiếu nhập kho', 'P0', PRE_FORM, ['Đăng nhập A.'] + XL, '—',
        ['A không có quyền xem nào vẫn tạo được phiếu và thấy phiếu đó trong danh sách.'], 289)
S10.add('Ẩn nút khi không phải người tạo', 'P0', [ACC_Q1, PNK, 'PXL-00022 do DNS Admin tạo từ PNK-11607 của DNS Admin.'],
        ['Đăng nhập Q1.', PNK_MENU, 'Mở PNK-11608.', MENU, 'Tìm PXL-00022.'], '—',
        ['PNK-11608 không có nút Tạo phiếu xuất lại.', 'Dòng PXL-00022 không có nút Tạo phiếu nhập lại.'], 295)
S10.add('Xuất Excel theo quyền', 'P1', ACC_Q3, ['Đăng nhập Q3.', MENU, 'Xuất Excel, Xuất file.'], '—',
        ['File chỉ có phiếu trong phạm vi phòng ban của Q3.'], 293)
S10.add('Xem lịch sử theo quyền', 'P1', [ACC_Q1, P21], ['Đăng nhập Q1.', MENU, 'Mở lịch sử PXL-00021.'], '—',
        ['Xem được 2 mốc.'], 294)
S10.add('Bị gỡ quyền giữa lúc thao tác', 'P1', [ACC_Q1, 'Quản trị gỡ quyền theo tổng công ty của Q1 khi Q1 đang ở danh sách.'],
        ['Bấm sang trang 2 hoặc bấm Tìm kiếm.'], '—', ['Danh sách chỉ còn phiếu Q1 tự tạo (phạm vi kiểm lại ở mỗi lần nạp).'],
        [297, 298])
S10.add('Super admin xem mọi phiếu', 'P2', 'Tài khoản DNS Admin (Super admin), không gán quyền xem riêng.',
        ['Đăng nhập DNS Admin.', MENU, ADV], '—', ['Thấy đủ 23 phiếu, có ô Công ty, Phòng ban.'], 287)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'LỊCH SỬ THAY ĐỔI', S4),
    ('V', 'XEM CHI TIẾT PHIẾU XUẤT LẠI', S5),
    ('VI', 'IN PHIẾU', S6),
    ('VII', 'TÙY CHỈNH CỘT', S7),
    ('VIII', 'XUẤT DANH SÁCH EXCEL', S8),
    ('IX', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S9),
    ('X', 'PHÂN QUYỀN', S10),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
check_no_dash_pre(SECTIONS, [])
_ids = ['TC_%02d.%s' % (s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
assert len(_ids) == len(set(_ids)), 'Trùng TC ID'

if __name__ == '__main__':
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='Phiếu xuất điều chỉnh sai số liệu - Cập nhật ngày 09/11/2026',
                module_name='Phiếu xuất điều chỉnh sai số liệu', description_block=DESCRIPTION_BLOCK, sections=SECTIONS,
                loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

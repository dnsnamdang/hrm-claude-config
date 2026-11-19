# -*- coding: utf-8 -*-
"""Testcase màn "Kiểm kê theo vị trí" (phiếu kiểm kê theo vị trí) — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026
(tc_chuan.build_chuan, loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (lý do — đọc code 06/11/2026): màn là chứng từ có vòng đời Đang tạo > Đang kiểm > Chờ duyệt kết quả > Chờ xử lý >
Hoàn thành, có Thêm (từ kế hoạch hoặc lập tay) / Sửa / Xóa theo trạng thái + người tạo, Lưu và gửi, Nhập kết quả (Lưu kết quả gửi
Ban kiểm soát), Duyệt kết quả / Không duyệt (ApproveNoteModal), Xử lý (Tổng kiểm kê, điều chuyển, Hoàn thành), In phiếu, Xuất Excel 1
phiếu, lịch sử. Không có route / nút Khóa, Hủy phiếu, Import → bỏ 3 nhóm đó.
Thứ tự nhóm chuẩn 'phieu': I Hiển thị · II Tìm kiếm & lọc (gồm Cài đặt bộ lọc) · III Thêm mới (Lưu, Lưu và tiếp tục, chọn kế
hoạch, phạm vi + Lấy vị trí + ĐVT kiểm kê, rời màn) · IV Chỉnh sửa · V Xóa · VI Gửi duyệt (Lưu và gửi + Nhập kết quả / Lưu kết quả)
· VII Duyệt phiếu (Duyệt kết quả + bước Xử lý sau duyệt) · VIII Không duyệt phiếu · IX Lịch sử · X Xem chi tiết · XI In phiếu (kèm
In danh sách) · XII Tùy chỉnh cột · XIII Xuất danh sách Excel (kèm Xuất 1 phiếu) · XIV Ràng buộc · XV Phân quyền.
Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../ke-hoach-kiem-ke-theo-vi-tri/gen_testcase.py (05/11, check_tc 0 lỗi).
Nguồn hành vi (đọc 06/11/2026, nhánh develop): FE pages/warehouse/position-inventory-results/**; BE Modules/Finance
PositionInventoryResult* (Entity / Service / WriteService / Controller / 2 FormRequest / PrintService / Export), PositionInventoryTreeService,
WarehouseInventoryLockService, WarehouseImportWriteService, PositionTransferWriteService.
Số liệu mẫu: dev-hrm 06/11/2026 (DNS Admin): 52 phiếu (4 Đang kiểm, 2 Chờ xử lý, 46 Hoàn thành); TPE-KKVT-00140 có 7 mốc lịch sử.
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
MENU = 'Vào phân hệ Kho > menu "Kiểm kho" > nhóm "Theo vị trí" > bấm "Kiểm kê theo vị trí".'
TAO = [MENU, 'Bấm "Tạo mới".']
ADV = 'Bấm Tìm kiếm nâng cao.'

Q1 = 'Lập phiếu kiểm kê kho theo vị trí'
Q2 = 'Ban kiểm soát duyệt kết quả kiểm kê'
Q3 = 'Xử lý phiếu kiểm kê vị trí'
V1 = 'Xem phiếu kiểm kê vị trí - theo tổng công ty'
V2 = 'Xem phiếu kiểm kê vị trí - theo công ty'
CONFLICT = 'Trạng thái đã bị thay đổi. Vui lòng load lại trang'
NOTFOUND = 'Không tìm thấy phiếu kiểm kê hoặc bạn không có quyền xem.'
NOPERM = 'Bạn không có quyền thực hiện chức năng này.'

ACC_A = 'Tài khoản A: thủ kho kho Phan Trọng Tuệ, công ty TPE, có quyền "%s", không có quyền xem theo cấp.' % Q1
ACC_B = 'Tài khoản B: nhân viên công ty TPE, không có quyền nào của màn.'
ACC_C = 'Tài khoản C: có quyền "%s", thuộc công ty TPE.' % V2
ACC_T = 'Tài khoản T: có quyền "%s".' % V1
ACC_K = 'Tài khoản K: Ban kiểm soát công ty TPE, có quyền "%s", không có quyền xem theo cấp.' % Q2
ACC_X = 'Tài khoản X: người xử lý công ty TPE, có quyền "%s", không có quyền xem theo cấp.' % Q3
PRE_LIST = 'Tài khoản DNS Admin (Super admin); trong phạm vi xem có 52 phiếu: 4 Đang kiểm, 2 Chờ xử lý, 46 Hoàn thành.'
P140 = ('Phiếu TPE-KKVT-00140: lập tay, kho Phan Trọng Tuệ, Hoàn thành, Người tạo / Người duyệt DNS Admin, Ngày kiểm kê 23/10/2026, '
        'Ngày duyệt 23/10/2026, Ngày cập nhật 23/10/2026 11:39; có 1 file đính kèm, 7 mốc lịch sử.')
P139 = 'Phiếu TPE-KKVT-00139 lập từ kế hoạch TPE-KHKKVT-00137, kho Phan Trọng Tuệ, Hoàn thành.'
KHO = ('Kho Phan Trọng Tuệ (mã PTT): vị trí tự do N1-T2-KV có hàng "Quạt ENEOS" (Cái., SL tồn 1,227, công ty TPE, 4 lô, lô '
       'TONDAUKHO-9113-11191-41 SL 670); hàng có ĐVT Cái. (cơ sở) và Hộp 20 (hệ số 20).')
PRE_FORM = ACC_A + '\n' + KHO
KH = 'Kế hoạch KH1 (TPE-KHKKVT-00150) trạng thái Đang kiểm, kho Phan Trọng Tuệ, vị trí N1-T2-KV, hội đồng Bùi Duy Trước.'
PH1 = 'Phiếu PH1 trạng thái Đang tạo do A lập tay ở kho PTT, vị trí N1-T2-KV.'
PH2 = 'Phiếu PH2 trạng thái Đang kiểm do A lập, chưa có file đính kèm; dòng lô TONDAUKHO-9113-11191-41 SL 670.'
PH3 = 'Phiếu PH3 trạng thái Chờ duyệt kết quả do A lập, có dòng Thực kiểm 669 / SL 670 (Chênh lệch -1).'
PH3B = 'Phiếu PH3B trạng thái Chờ duyệt kết quả do A lập, mọi dòng Chênh lệch = 0, lập từ kế hoạch KH2 (Đã lập kiểm kê).'
PH4 = 'Phiếu PH4 trạng thái Chờ xử lý: 2 dòng thiếu (-1 và -3), chưa tick Tổng kiểm kê, chưa điều chuyển.'
FILL = TAO + ['Chọn Kho vật lý = PTT - Phan Trọng Tuệ.', 'Ở cột Vị trí tick N1-T2-KV (nhóm Vị trí tự do).', 'Bấm Lấy vị trí.',
              'Ở dòng 1 Hội đồng chọn Nhân viên = Bùi Duy Trước.']
FULL = ['Kho vật lý: PTT - Phan Trọng Tuệ', 'Vị trí: N1-T2-KV', 'Nhân viên: Bùi Duy Trước']
OK_LIST = 'Báo "Lưu thành công.", về màn danh sách; dòng mới ở trên cùng, trạng thái Đang tạo (nhãn xám).'
DET = lambda code: [MENU, 'Bấm số phiếu %s.' % code]  # noqa: E731

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
     'Lập phiếu kiểm kê theo vị trí cho một kho vật lý (từ Kế hoạch kiểm kê theo vị trí hoặc lập tay), chọn ĐVT kiểm kê cho từng '
     'lô, nhập kết quả thực kiểm kèm file biên bản, Ban kiểm soát duyệt / không duyệt, người xử lý xử lý chênh lệch thiếu (Tổng kiểm '
     'kê, Phiếu điều chuyển vị trí, Hoàn thành). Phiếu KHÔNG tự đổi tồn kho.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Danh sách: phiếu trong phạm vi xem; trạng thái Đang tạo (xám), Đang kiểm, Chờ duyệt kết quả, Chờ xử lý (vàng), Hoàn thành '
     '(xanh lá).\n- Bảng Chi tiết: hàng có tồn > 0 và lô tồn > 0 tại vị trí đã tick (hoặc của kế hoạch), mỗi lô >= 1 dòng ĐVT kiểm kê.\n'
     '- Popup Chọn kế hoạch: kế hoạch Đang kiểm của kho mà người dùng là thủ kho.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác (kể cả Super admin).\n- Phiếu ngoài phạm vi quyền xem (trừ phiếu đang chờ chính người đó '
     'duyệt / xử lý).\n- Kế hoạch kiểm kê (màn khác).\n- Nhà / dãy / khoang / vị trí đã khóa ở danh mục (không hiện để tick mới).'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô Ngày kiểm kê lọc theo ngày của phiếu (phiếu lập từ kế hoạch mang ngày tạo kế hoạch), lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Phiếu > vị trí > hàng (SL tồn) > công ty (Cộng) > lô > dòng ĐVT kiểm kê (SL, Thực kiểm, Chênh lệch, Ghi chú, Tổng kiểm kê).\n'
     '- Phạm vi: Nhà > Dãy > Khoang > Vị trí; vị trí tự do không thuộc khoang.\n- Hội đồng: nhân viên + chức vụ. File đính kèm.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Tổng SL × hệ số các dòng ĐVT kiểm kê của 1 lô = SL lô.\n- Chênh lệch = Thực kiểm - SL (máy chủ tự tính).\n'
     '- Hội đồng không được trùng nhân viên.'),
    ('7. Phân quyền cấp',
     '- %s: xem mọi phiếu.\n- %s: phiếu công ty mình + của mình.\n- Không quyền xem: chỉ phiếu mình tạo.\n'
     '- %s: Tạo mới, chọn kế hoạch.\n- %s: Duyệt kết quả / Không duyệt.\n- %s: Tổng kiểm kê, Tạo phiếu điều chuyển vị trí, Hoàn thành.\n'
     '- Sửa / Xóa / Nhập kết quả: người tạo phiếu (không cần quyền riêng).' % (V1, V2, Q1, Q2, Q3)),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là khoảng thứ tự dòng của trang, N là tổng phiếu khớp bộ lọc trong phạm vi xem.\n'
     '- Cột Chênh lệch = Thực kiểm - SL, khác 0 chữ đỏ.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: A (thủ kho, lập phiếu), B (không quyền), C (xem theo công ty), T (xem tổng công ty), K (Ban kiểm '
     'soát), X (người xử lý), DNS Admin (Super admin).\n'
     '- Lưu ý: Lưu và gửi, Lưu kết quả gửi NGAY, không có hộp xác nhận; Duyệt / Không duyệt qua popup ghi chú; Hoàn thành có hộp xác nhận.\n'
     '- Lưu ý: số tồn trên phiếu là ảnh chụp lúc Lấy vị trí / lúc lập kế hoạch.\n'
     '- Màn Tạo / Sửa / Chi tiết là TRANG riêng, không phải cửa sổ nổi.'),
]

SCREEN = ListScreen(menu=MENU, title='Kiểm kê theo vị trí', total=52, quick_label='số phiếu',
                    quick_sample='00140', quick_hit='phiếu TPE-KKVT-00140',
                    filters=[('Trạng thái', 'Hoàn thành'), ('Kho', 'PTT - Phan Trọng Tuệ')], unit='phiếu')

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Cả 3 nơi đều là "Kiểm kê theo vị trí".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE_LIST, [MENU, 'Quan sát khối bộ lọc và thanh công cụ.'], '—',
       ['Khối bộ lọc: ô tìm nhanh (gợi ý "Tìm theo số phiếu"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
        'Thanh công cụ: Tạo mới, Xuất Excel, In danh sách, nút biểu tượng cột.',
        'Dòng Hoàn thành: cột Hành động có In, Xuất Excel, Lịch sử.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 13 cột: STT, Số phiếu, Kế hoạch kiểm kê, Ngày kiểm kê, Kho, Trạng thái, Người tạo, Người duyệt, Ngày duyệt, Ngày tạo, '
        'Ngày cập nhật, Người cập nhật, Hành động.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 13/13 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp phiếu', 'P0', [PRE_LIST, P140], [MENU, 'Tìm "TPE-KKVT-00140", đối chiếu dòng.'], '—',
       ['Kế hoạch kiểm kê trống, Ngày kiểm kê "23/10/2026", Kho "Phan Trọng Tuệ", Trạng thái "Hoàn thành", Người tạo / Người duyệt '
        '"DNS Admin", Ngày duyệt "23/10/2026", Ngày tạo "23/10/2026 11:25", Ngày cập nhật "23/10/2026 11:39".'], [6, 58])
S1.add('Cột Kế hoạch kiểm kê là liên kết', 'P1', [PRE_LIST, P139], [MENU, 'Bấm mã "TPE-KHKKVT-00137" ở dòng TPE-KKVT-00139.'], '—',
       ['Mở chi tiết kế hoạch TPE-KHKKVT-00137 ở tab mới; danh sách giữ nguyên.'], 6)
S1.add('Trạng thái bản ghi', 'P0', PRE_LIST, [MENU, ADV, 'Mở ô Trạng thái.', 'Quan sát cột Trạng thái.'], '—',
       ['Ô có 5 lựa chọn: Đang tạo, Đang kiểm, Chờ duyệt kết quả, Chờ xử lý, Hoàn thành.',
        'Nhãn: Đang tạo xám; Đang kiểm, Chờ duyệt kết quả, Chờ xử lý vàng; Hoàn thành xanh lá.'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', [ACC_B, 'B chưa tạo phiếu nào.'], ['Đăng nhập B.', MENU], '—',
       ['Bảng hiện "Không có dữ liệu phù hợp.", không báo lỗi; không có nút Tạo mới.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       ['Bảng hiện "Không có dữ liệu phù hợp.".'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 20 phiếu, tự về trang 1, "Hiển thị 1–20 / 52".', 'Chỉ nạp lại 1 lần.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–20 / 52".', 'Bước 3: "Hiển thị 1–10 / 52".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—', ['Bước 2: trang 6 "Hiển thị 51–52 / 52".', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang 6 quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.'], '—', ['Trang 2 đánh số 11–20.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', ADV, 'Chọn Trạng thái = Hoàn thành.'],
       'Trạng thái: Hoàn thành', ['Tự nạp lại ở trang 1; "Hiển thị 1–10 / 46".'], 17)
S1.add('Sắp xếp tăng dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Số phiếu.'], '—', ['Xếp theo số phiếu tăng dần, mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Số phiếu 2 lần.'], '—', ['Xếp theo số phiếu giảm dần.'], 21)
S1.add('Sắp xếp theo Ngày kiểm kê, Kế hoạch, Kho', 'P1', PRE_LIST,
       [MENU, 'Bấm tiêu đề Ngày kiểm kê (2 lần).', 'Bấm tiêu đề Kế hoạch kiểm kê.', 'Bấm tiêu đề Kho.'], '—',
       ['Ngày kiểm kê: lần 1 cũ nhất trên, lần 2 mới nhất trên.', 'Kế hoạch kiểm kê xếp theo mã kế hoạch; Kho xếp theo tên kho A > Z.',
        'Khi mới vào chưa chọn cột nào: tạo mới nhất trên, các cột hiện biểu tượng sắp xếp trung tính.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Trạng thái, Người tạo, Người duyệt, Ngày duyệt, Ngày tạo, Ngày cập nhật, Người cập nhật.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Số phiếu (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự tăng của trang 1.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 2.', 'Bấm tiêu đề Ngày kiểm kê.'], '—', ['Về trang 1.'], 25)
S1.add('Nút thao tác theo trạng thái', 'P0', [PRE_LIST, 'TPE-KKVT-00146 Đang kiểm do DNS Admin tạo; TPE-KKVT-00142 Chờ xử lý còn dòng thiếu.'],
       [MENU, 'Quan sát cột Hành động 2 dòng TPE-KKVT-00146, TPE-KKVT-00142.'], '—',
       ['00146: Nhập kết quả, In và nút ba chấm "Hành động khác" chứa Xuất Excel, Lịch sử.',
        '00142: Tạo phiếu điều chuyển vị trí, In và ba chấm chứa Xuất Excel, Lịch sử.'], [3, 34])
S1.add('Mở màn từ menu khi phân hệ Kho đang bật', 'P1', PRE_LIST,
       ['Đăng nhập.', 'Bấm nút lưới phân hệ ở đầu trang, chọn ô "Kho".', 'Bấm "Kiểm kho" ở thanh bên, chọn nhóm "Theo vị trí".'], '—',
       ['Thanh bên phân hệ Kho có mục Kiểm kho; nhóm Theo vị trí có 2 mục: Kiểm kê theo vị trí, Kiểm kê theo hàng hóa.',
        'Bấm "Kiểm kê theo vị trí" mở màn danh sách.'], 1)
S1.add('Mở màn từ thông báo của Ban kiểm soát', 'P1', [ACC_K, PH3, 'K đã nhận thông báo "[KKVT] Chờ duyệt: <số phiếu PH3>".'],
       ['Đăng nhập K.', 'Bấm chuông thông báo, bấm thông báo của PH3.'], '—',
       ['Mở màn chi tiết PH3 dù K không có quyền xem theo cấp.', 'Có nút Duyệt kết quả, Không duyệt.'], 1)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo số phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "TPE-KKVT-00140", bấm Tìm kiếm.'], 'Ô tìm nhanh: TPE-KKVT-00140',
       ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần số phiếu', 'P0', PRE_LIST, [MENU, 'Nhập "TPSG", bấm Tìm kiếm.'], 'Ô tìm nhanh: TPSG',
       ['Chỉ còn 12 phiếu có số phiếu chứa "TPSG".'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "tpe-kkvt-00140", bấm Tìm kiếm.'], '—', ['Ra TPE-KKVT-00140.'], 28)
S2.add('Có dấu / không dấu ở ô Hàng hóa', 'P2', PRE_LIST, [MENU, ADV, 'Nhập Hàng hóa "quat eneos", bấm Tìm kiếm.'], '—',
       ['Ra các phiếu có hàng "Quạt ENEOS" nếu cơ sở dữ liệu so khớp không dấu.', 'Lưu ý: so khớp theo cách so sánh chữ của cơ sở dữ liệu.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; ký tự % được hiểu là ký tự đại diện nên ra toàn bộ.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  TPE-KKVT-00140  ", bấm Tìm kiếm.'], '—', ['Ra TPE-KKVT-00140.'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "TPE-KKVT-00140", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Hiện lại đủ 52 phiếu.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST, [MENU, 'Nhập "00140", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'], '—',
       ['Cả 2 cách đều ra TPE-KKVT-00140, về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['Các ô Trạng thái, Người tạo, Người duyệt, Hàng hóa, Ngày kiểm kê, Kho, Nhà, Dãy, Khoang, Vị trí, Công ty, Phòng ban đều trống.',
        'Đủ 52 phiếu.'], 36)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Chờ xử lý.'], '—',
       ['Lọc ngay; còn 2 phiếu TPE-KKVT-00142, TPV-KKVT-00106.'], 37)
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = Nguyễn Thu Hòa.'], '—',
       ['Chỉ còn phiếu do Nguyễn Thu Hòa tạo (TPSG-KKVT-00132, 00130, …).', 'Ô Người tạo liệt kê toàn bộ nhân viên.'], 37)
S2.add('Lọc Người duyệt', 'P1', PRE_LIST, [MENU, ADV, 'Chọn Người duyệt = Võ Thị Hà.'], '—',
       ['Chỉ còn phiếu do Võ Thị Hà duyệt (TPSG-KKVT-00130, 00129, 00128, 00127).', 'Phiếu chưa duyệt không xuất hiện.'], 37)
S2.add('Lọc Hàng hóa theo mã hoặc tên', 'P1', PRE_LIST, [MENU, ADV, 'Nhập Hàng hóa "Quạt ENEOS", bấm Tìm kiếm.'], '—',
       ['Ra các phiếu có hàng Quạt ENEOS (có TPE-KKVT-00146, 00140).'], 37)
S2.add('Lọc Ngày kiểm kê lấy trọn ngày biên', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày kiểm kê 23/10/2026 – 23/10/2026.'], '—',
       ['Ra 4 phiếu TPE-KKVT-00140, 00139, 00136, 00134.', 'Bỏ trống ngày cuối vẫn lọc được từ ngày đầu.'], 37)
S2.add('Lọc Kho', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = PTT - Phan Trọng Tuệ.'], '—',
       ['Còn TPE-KKVT-00146, 00140, 00139.', 'Ô Nhà nạp các nhà của kho PTT.'], 37)
S2.add('Chuỗi Kho > Nhà > Dãy > Khoang > Vị trí', 'P0', PRE_LIST,
       [MENU, ADV, 'Chọn Kho = PTT.', 'Chọn Nhà = N1 - Nhà 1.', 'Chọn Dãy = D1 - Dãy 1.', 'Chọn Khoang = K1 - Khoang 1.'],
       '—', ['Mỗi ô con chỉ còn mục thuộc ô cha đã chọn.', 'Mỗi lần chọn danh sách lọc lại theo phiếu có tick mục đó trong phạm vi.'], [37, 38])
S2.add('Đổi cấp cha xóa cấp con', 'P0', 'Đang lọc Kho PTT, Nhà N1, Dãy D1, Khoang K1.', [ADV, 'Đổi Kho = HP - Hải Phòng.'], '—',
       ['Ô Nhà, Dãy, Khoang, Vị trí bị xóa trắng, ô Nhà nạp nhà của kho Hải Phòng.', 'Danh sách nạp lại 1 lần.'], [37, 283])
S2.add('Lọc Vị trí tự do', 'P1', PRE_LIST, [MENU, ADV, 'Chọn Kho = PTT.', 'Chọn Vị trí = N1-T2-KV (không chọn Nhà / Dãy / Khoang).'],
       '—', ['Ô Vị trí có cả vị trí tự do khi chưa chọn cấp cha.', 'Ra các phiếu tick N1-T2-KV (có TPE-KKVT-00140).'], 37)
S2.raw(org_cases(SCREEN, len(S2) + 1), [[37], [37, 283], [37]])
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đang kiểm.', 'Chọn Kho = PTT.'], '—',
       ['Chỉ còn TPE-KKVT-00146.'], 38)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST, [MENU, 'Nhập "TPSG", bấm Tìm kiếm.', ADV, 'Chọn Kho = PTT.'], '—',
       ['"Không có dữ liệu phù hợp." vì phiếu TPSG thuộc Kho Sài Gòn.'], [39, 40])
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Hoàn thành.', 'Bấm trang 2.'], '—',
       ['"Hiển thị 1–10 / 46" rồi "Hiển thị 11–20 / 46"; STT liên tục.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Trạng thái = Hoàn thành.', ['Bấm tiêu đề Số phiếu.'], '—',
       ['Chỉ 46 phiếu đang lọc được sắp; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "TPE", lọc Kho PTT, Nhà N1, sắp Số phiếu, ở trang 2.', ['Bấm Làm mới.'],
       '—', ['Mọi ô kể cả ô tìm nhanh về trống, bỏ sắp xếp, nạp lại trang 1, đủ 52 phiếu.'], 44)
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Hoàn thành, chưa mở màn con.'], ['Nhấn F5.'], '—',
       ['Bộ lọc trở về trống, đủ 52 phiếu (chỉ nhớ khi đi vào màn con của màn này).'], 46)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Người duyệt, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô Người duyệt.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Hoàn thành.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Trạng thái, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị bỏ, nạp lại đủ 52 phiếu.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Người duyệt.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Người duyệt vẫn ẩn.', 'Bước 2: tích đủ 11 mục, Người duyệt hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Kho lên đầu, bấm Lưu.'], '—',
       ['Ô Kho đứng đầu khối Tìm kiếm nâng cao; cấu hình giữ sau khi đăng nhập lại.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo', 'P0', PRE_FORM, TAO, '—', ['Mở TRANG "Tạo phiếu kiểm kê theo vị trí", tab cùng tiêu đề.'], 49)
S3.add('Mở màn Tạo từ màn Kế hoạch', 'P0', [PRE_FORM, KH],
       ['Vào phân hệ Tài chính > menu "Kiểm kê" > bấm "Kế hoạch kiểm kê theo vị trí".', 'Ở dòng KH1 bấm Lập phiếu kiểm kê.'], '—',
       ['Mở màn Tạo phiếu với ô Kế hoạch kiểm kê = TPE-KHKKVT-00150, kho, phạm vi, chi tiết, hội đồng nạp sẵn.'], [49, 274])
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải "<tên A> - <ngày giờ hiện tại>".', 'Không có ô Số phiếu (tự sinh khi lưu).'], 50)
S3.add('Các trường, khối và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Kế hoạch kiểm kê (gợi ý "Chọn kế hoạch kiểm kê"), Ngày kiểm kê *, Kho vật lý *.',
        'Phạm vi kiểm kê: 4 cột Nhà, Dãy, Khoang, Vị trí, nút Lấy vị trí ở góc phải.',
        'Chi tiết * (bảng "Không có dữ liệu"); Hội đồng kiểm kê * có 1 dòng trống và nút Thêm dòng.',
        'Chân màn: Lưu, Lưu và gửi, Lưu và tiếp tục, Quay lại; không có ô Ghi chú, không có File đính kèm.'], [51, 54])
S3.add('Trường bắt buộc / không bắt buộc', 'P0', PRE_FORM, TAO + ['Quan sát dấu *.'], '—',
       ['Dấu * ở Ngày kiểm kê, Kho vật lý, Nhà, Dãy, Khoang, Vị trí, Chi tiết, ĐVT kiểm kê, Hội đồng kiểm kê, Nhân viên, Chức vụ.',
        'Kế hoạch kiểm kê không bắt buộc.', 'Lưu ý: chỉ bắt buộc ít nhất 1 Vị trí; Nhà / Dãy / Khoang không tick vẫn lưu được.'], 52)
S3.add('Giá trị mặc định', 'P0', PRE_FORM, TAO, '—',
       ['Ngày kiểm kê = ngày hôm nay, ô khóa.', 'Kế hoạch, Kho vật lý trống; 4 cột phạm vi ghi "Chưa chọn kho vật lý".', 'Hội đồng có 1 dòng trống.'], 53)
S3.add('Lưu phiếu lập tay hợp lệ đầy đủ', 'P0', PRE_FORM, FILL + ['Bấm Lưu.'], FULL,
       [OK_LIST, 'Số phiếu dạng "TPE-KKVT-<số>" theo công ty của A.'], [55, 58, 59, 79])
S3.add('Lưu chỉ với trường bắt buộc tối thiểu', 'P0', PRE_FORM, FILL + ['Không chọn kế hoạch, không tick Nhà / Dãy / Khoang.', 'Bấm Lưu.'],
       FULL, [OK_LIST, 'Chi tiết phiếu: cột Nhà, Dãy, Khoang không tick mục nào; Vị trí N1-T2-KV được tick.'], [56, 57])
S3.add('Dữ liệu sau lưu', 'P0', [PRE_FORM, 'A vừa lưu phiếu ở TC_03.007.'], ['Bấm số phiếu vừa tạo.'], '—',
       ['Chi tiết: Kho PTT, vị trí N1-T2-KV được tick, bảng Chi tiết có Quạt ENEOS SL tồn 1,227, 4 lô, mỗi lô 1 dòng ĐVT Cái. SL = SL lô.',
        'Hội đồng: Bùi Duy Trước, chức vụ tự điền.'], 58)
S3.add('Trạng thái mặc định sau Lưu', 'P0', [PRE_FORM, 'A vừa lưu phiếu.'], [MENU, 'Đăng nhập DNS Admin, mở danh sách.'], '—',
       ['A thấy phiếu Đang tạo (nhãn xám).', 'DNS Admin KHÔNG thấy phiếu này (Đang tạo chỉ người tạo thấy).'], [59, 84])
S3.add('Lịch sử tạo', 'P1', [PRE_FORM, 'A vừa lưu phiếu.'], ['Ở dòng phiếu bấm Lịch sử.'], '—',
       ['Có 1 mốc "Tạo mới", Người thực hiện A, thời điểm lưu.'], [60, 176])
S3.add('Bỏ trống mọi trường bắt buộc', 'P0', PRE_FORM, TAO + ['Bấm Lưu ngay.'], '—',
       ['Báo "Bạn chưa nhập đầy đủ thông tin.", không lưu.',
        'Lỗi đỏ CÙNG LÚC: "Kho vật lý – Vui lòng chọn kho vật lý.", "Phạm vi kiểm kê – Chưa chọn đủ thông tin vị trí!", '
        '"Chi tiết – Chưa có vị trí nào. Vui lòng bấm \\"Lấy vị trí\\".", "Nhân viên – Vui lòng chọn nhân viên.", '
        '"Chức vụ – Vui lòng chọn chức vụ.".', 'Cuộn tới ô lỗi đầu tiên.'], [61, 70, 80])
S3.add('Chọn kho nhưng chưa Lấy vị trí', 'P0', PRE_FORM, TAO + ['Chọn Kho PTT, tick N1-T2-KV, chọn nhân viên.', 'Bấm Lưu.'], '—',
       ['Chỉ báo lỗi bảng Chi tiết "Chi tiết – Chưa có vị trí nào. Vui lòng bấm \\"Lấy vị trí\\".", khung bảng viền đỏ.'], [61, 62])
S3.add('Hội đồng trùng nhân viên', 'P0', PRE_FORM, FILL + ['Bấm Thêm dòng, chọn lại Bùi Duy Trước.', 'Bấm Lưu.'], '—',
       ['Dòng 2 báo "Nhân viên – Bị trùng.", không lưu.'], [62, 67])
S3.add('Xóa hết dòng hội đồng', 'P1', PRE_FORM, FILL + ['Bấm thùng rác ở dòng hội đồng.', 'Bấm Lưu.'], '—',
       ['Bảng hội đồng hiện "Không có dữ liệu", báo "Hội đồng kiểm kê – Vui lòng thêm ít nhất 1 thành viên.".'], 61)
S3.add('Chọn nhân viên tự điền chức vụ', 'P1', PRE_FORM, TAO + ['Chọn Nhân viên = Bùi Duy Trước.', 'Bỏ chọn nhân viên.'], '—',
       ['Bước 1: ô Chức vụ tự điền chức vụ đầu tiên của nhân viên.', 'Bước 2: ô Chức vụ bị xóa.'], 53)
S3.add('Trường không có ký tự / độ dài nhập tay', 'P2', PRE_FORM, TAO + ['Quan sát các ô nhập.'], '—',
       ['Form chỉ có ô chọn, ô tick và ô tìm; không có ô văn bản tự do cần kiểm độ dài, ký tự đặc biệt, khoảng trắng.',
        'Ô tìm của cột phạm vi gõ "  N1  " vẫn tìm ra N1 - Nhà 1.'], [63, 64, 65, 66, 68, 69, 81])
S3.add('Lỗi biến mất sau khi sửa', 'P1', 'Đang có lỗi đỏ ở TC_03.012.', ['Chọn Kho PTT.', 'Tick N1-T2-KV.', 'Bấm Lấy vị trí.'], '—',
       ['Lỗi Kho, Phạm vi, Chi tiết lần lượt biến mất ngay khi sửa đúng.'], 71)
S3.add('Trùng dữ liệu: 2 phiếu cùng kho, cùng phạm vi', 'P1', [PRE_FORM, PH1], FILL + ['Bấm Lưu.'], FULL,
       ['Lưu được; 2 phiếu có số phiếu khác nhau (không có trường duy nhất).'], [67, 75, 82])
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, FILL + ['Bấm Lưu và tiếp tục.'], FULL,
       ['Báo "Lưu thành công.", VẪN ở màn Tạo.', 'Form trắng: Kế hoạch, Kho trống, phạm vi trống, Chi tiết trống, Hội đồng 1 dòng trống.',
        'Phiếu vừa lưu ở trạng thái Đang tạo.'], [72, 76, 77, 83])
S3.add('Lưu và tiếp tục khi vào từ kế hoạch', 'P1', [PRE_FORM, KH], ['Mở màn Tạo từ nút Lập phiếu kiểm kê của KH1.', 'Bấm Lưu và tiếp tục.'],
       '—', ['Lưu thành công, form trắng KHÔNG còn KH1 (kế hoạch đã chuyển Đã lập kiểm kê).'], [77, 84])
S3.add('Lưu và tiếp tục khi thiếu bắt buộc', 'P0', PRE_FORM, TAO + ['Bấm Lưu và tiếp tục.'], '—',
       ['Báo lỗi như Lưu, không lưu, form giữ dữ liệu đã nhập.'], [73, 74])
S3.add('Rời màn sau Lưu và tiếp tục', 'P1', 'Vừa Lưu và tiếp tục, form trắng.', ['Bấm Quay lại.'], '—',
       ['Về danh sách ngay, không hỏi; phiếu vừa lưu có trong danh sách.'], [78, 85])
S3.add('Lưu: màn chuyển về danh sách', 'P1', PRE_FORM, FILL + ['Bấm Lưu.'], FULL,
       ['Màn Tạo đóng, về danh sách (màn là trang, không phải cửa sổ còn mở).'], [76, 85])
S3.add('Quay lại khi chưa nhập', 'P1', PRE_FORM, TAO + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 93)
S3.add('Quay lại khi đã nhập', 'P0', PRE_FORM, FILL + ['Bấm Quay lại.'], '—',
       ['Hiện hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" với nút Thoát, Ở lại.'], 94)
S3.add('Rời màn bằng menu / (x) của hộp', 'P1', PRE_FORM, FILL + ['Bấm menu sang màn khác.', 'Ở hộp "Thông tin chưa lưu" bấm (x).'],
       '—', ['Hộp hiện khi bấm menu; bấm (x) đóng hộp, ở lại màn Tạo, dữ liệu giữ nguyên.'], 95)
S3.add('Chọn Thoát', 'P0', 'Đang ở hộp "Thông tin chưa lưu".', ['Bấm Thoát.'], '—', ['Về danh sách, không lưu phiếu nào.'], 96)
S3.add('Chọn Ở lại', 'P1', 'Đang ở hộp "Thông tin chưa lưu".', ['Bấm Ở lại.'], '—', ['Đóng hộp, dữ liệu đã nhập giữ nguyên.'], 97)
S3.add('Nhập rồi trả về như ban đầu', 'P2', PRE_FORM, TAO + ['Chọn Kho PTT.', 'Bấm × trong ô Kho để bỏ chọn.', 'Bấm Quay lại.'],
       '—', ['Không hỏi "Thông tin chưa lưu".'], [98, 99])
S3.add('Không thao tác lâu', 'P2', PRE_FORM, FILL + ['Để yên 30 phút.', 'Bấm Lưu.'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên, chuyển về đăng nhập, không lưu.'], 100)
S3.add('Bấm Lưu liên tục', 'P0', PRE_FORM, FILL + ['Bấm Lưu 3 lần thật nhanh.'], FULL, ['Chỉ tạo 1 phiếu (nút khóa trong lúc lưu).'], 101)
S3.add('Tạo đồng thời ở 2 tab từ cùng kế hoạch', 'P1', [PRE_FORM, KH], ['Mở 2 tab màn Tạo, chọn KH1 ở cả 2.', 'Bấm Lưu ở tab 1 rồi tab 2.'],
       '—', ['Tab 1 lưu được, KH1 chuyển Đã lập kiểm kê.', 'Tab 2 báo "%s", không lưu.' % CONFLICT], 102)
S3.add('Chọn kế hoạch từ popup', 'P0', [PRE_FORM, KH], TAO + ['Bấm ô Kế hoạch kiểm kê.', 'Bấm dòng TPE-KHKKVT-00150.'], '—',
       ['Popup "Chọn kế hoạch kiểm kê theo vị trí" (dòng phụ "Chỉ kế hoạch đang kiểm mà bạn được lập phiếu"), cột STT, Mã phiếu, Kho, '
        'Người tạo, Ngày tạo.', 'Chọn dòng: popup đóng, ô Kế hoạch = TPE-KHKKVT-00150, Ngày kiểm kê = ngày tạo kế hoạch, Kho PTT khóa, '
        'phạm vi khóa, nút Lấy vị trí ẩn, chi tiết + hội đồng nạp sẵn.'], [53, 274, 269])
S3.add('Popup chọn kế hoạch: tìm và rỗng', 'P1', [ACC_A, 'Không có kế hoạch Đang kiểm nào ở kho A làm thủ kho.'],
       TAO + ['Bấm ô Kế hoạch kiểm kê.', 'Nhập mã "ABC", bấm Tìm kiếm.'], '—',
       ['Bảng hiện "Không có kế hoạch kiểm kê nào bạn được lập phiếu.".'], [268, 40])
S3.add('Popup chọn kế hoạch: bấm mã mở tab mới', 'P2', [PRE_FORM, KH], TAO + ['Bấm ô Kế hoạch.', 'Bấm mã TPE-KHKKVT-00150 trong popup.'],
       '—', ['Mở chi tiết kế hoạch ở tab mới, popup vẫn mở, chưa chọn kế hoạch.'], 274)
S3.add('Bỏ kế hoạch đã chọn', 'P1', 'Đang ở màn Tạo, đã chọn KH1.', ['Bấm × trong ô Kế hoạch kiểm kê.'], '—',
       ['Form về lập tay trống: kho, phạm vi, chi tiết trống; Hội đồng 1 dòng trống; nút Lấy vị trí hiện lại.'], 98)
S3.add('Lưu phiếu lập từ kế hoạch', 'P0', [PRE_FORM, KH], TAO + ['Chọn KH1.', 'Bấm Lưu.'], '—',
       [OK_LIST, 'KH1 ở màn Kế hoạch chuyển "Đã lập kiểm kê"; lịch sử KH1 có mốc ghi chú "Lập phiếu kiểm kê <số phiếu>.".'], [55, 281])
S3.add('Lấy vị trí khi chưa chọn kho', 'P0', PRE_FORM, TAO + ['Bấm Lấy vị trí.'], '—',
       ['Báo "Bạn chưa nhập đầy đủ thông tin.", lỗi đỏ dưới ô Kho vật lý.'], [61, 62])
S3.add('Lấy vị trí khi chưa tick vị trí', 'P0', PRE_FORM, TAO + ['Chọn Kho PTT.', 'Tick Nhà N1, không tick vị trí.', 'Bấm Lấy vị trí.'],
       '—', ['Báo "Chưa chọn đủ thông tin vị trí!", khung cột Vị trí viền đỏ.'], 61)
S3.add('Lấy vị trí ra đúng hàng tồn', 'P0', PRE_FORM, TAO + ['Chọn Kho PTT.', 'Tick N1-T2-KV.', 'Bấm Lấy vị trí.'], '—',
       ['Bảng Chi tiết: Vị trí N1-T2-KV, Quạt ENEOS ĐVT Cái., SL tồn 1,227; công ty "TPE (1,227)" phần ngoặc chữ đỏ; 4 lô, lô '
        '"TONDAUKHO-9113-11191-41 (670)" SL 670, ĐVT kiểm kê Cái.'], [58, 269])
S3.add('Lấy vị trí ở vị trí không có tồn', 'P1', [PRE_FORM, 'Vị trí PTT-N1-KV7-01 không có hàng tồn.'],
       TAO + ['Chọn Kho PTT.', 'Tick PTT-N1-KV7-01.', 'Bấm Lấy vị trí.'], '—',
       ['Báo "Các vị trí đã chọn không có hàng tồn.", bảng Chi tiết giữ nguyên.'], [268, 61])
S3.add('ĐVT kiểm kê: đổi sang đơn vị lớn tách dòng', 'P0', [PRE_FORM, 'Lô L1 của hàng H có SL 119 Cái; H có ĐVT Hộp 20 (hệ số 20).'],
       TAO + ['Lấy vị trí có lô L1.', 'Đổi ĐVT kiểm kê của lô L1 sang Hộp 20.'], '—',
       ['Lô L1 thành 2 dòng: Hộp 20 SL 5, Cái SL 19 (5 × 20 + 19 = 119).'], [53, 283, 286])
S3.add('ĐVT kiểm kê: không đủ quy đổi', 'P0', [PRE_FORM, 'Lô L2 SL 7 Cái; hàng có ĐVT Hộp 20.'], TAO + ['Đổi ĐVT lô L2 sang Hộp 20.'], '—',
       ['Báo "Số lượng không đủ để quy đổi!", ô trở lại Cái, SL 7.'], [62, 283])
S3.add('ĐVT kiểm kê: đổi về đơn vị cơ sở gộp dòng', 'P1', 'Lô L1 đang 2 dòng Hộp 20 SL 5 + Cái SL 19.', ['Đổi dòng 1 về Cái.'], '—',
       ['Lô còn 1 dòng Cái SL 119.'], 283)
S3.add('Phạm vi: chọn cấp cha mới hiện cấp con', 'P0', PRE_FORM, TAO + ['Chọn Kho PTT.', 'Tick N1 - Nhà 1.', 'Tick D1 - Dãy 1.'],
       '—', ['Trước khi tick: cột Dãy ghi "Chưa chọn nhà hoặc không có dữ liệu".',
             'Sau tick Nhà: cột Dãy hiện nhóm "N1 - Nhà 1"; sau tick Dãy: cột Khoang hiện nhóm "N1 | D1".', 'Nhóm "Vị trí tự do" luôn hiện.'],
       [53, 283])
S3.add('Phạm vi: bỏ tick cấp cha tự bỏ cấp con', 'P1', 'Đã tick N1, D1, K1 và 1 vị trí trong K1, 1 vị trí tự do.', ['Bỏ tick N1 - Nhà 1.'], '—',
       ['D1, K1 và vị trí thuộc K1 tự bỏ tick; vị trí tự do vẫn được tick.'], [283, 285])
S3.add('Phạm vi: ô tìm và Chọn hết', 'P1', PRE_FORM, TAO + ['Chọn Kho PTT, tick N1.', 'Gõ "D1" vào ô tìm cột Dãy.', 'Tick "Chọn hết" của cột Dãy.'],
       '—', ['Cột Dãy chỉ còn dãy có mã / tên chứa "D1".', 'Chọn hết chỉ tick các dãy đang hiện.'], 53)
S3.add('Đổi kho khi đã có Chi tiết: Hủy', 'P0', 'Đang ở màn Tạo, đã Lấy vị trí ở kho PTT.', ['Đổi Kho vật lý = HP - Hải Phòng.', 'Bấm Hủy.'],
       '—', ['Hiện hộp "Đổi kho vật lý": "Đổi kho vật lý sẽ xóa phạm vi kiểm kê và danh sách vị trí đã lấy. Bạn có muốn tiếp tục?".',
             'Bấm Hủy: ô Kho trở lại PTT, phạm vi và Chi tiết giữ nguyên.'], 53)
S3.add('Đổi kho khi đã có Chi tiết: Đổi kho', 'P1', 'Đang ở màn Tạo, đã Lấy vị trí ở kho PTT.', ['Đổi Kho = HP - Hải Phòng.', 'Bấm Đổi kho.'],
       '—', ['Phạm vi và bảng Chi tiết bị xóa, 4 cột nạp cấu trúc kho Hải Phòng.'], [53, 283])
S3.add('Không có quyền Lập phiếu', 'P0', ACC_B, ['Đăng nhập B.', MENU], '—',
       ['Không có nút Tạo mới.', 'Mở đường link màn Tạo, nhập đủ, bấm Lưu > báo "%s", không lưu.' % NOPERM], [49, 295])

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
PRE_E = [ACC_A, PH1]
EDIT = ['Đăng nhập A.', MENU, 'Ở dòng PH1 bấm Sửa (bút chì).']
S4.add('Mở màn Sửa', 'P0', PRE_E, EDIT, '—', ['Mở TRANG "Sửa phiếu kiểm kê theo vị trí: <số phiếu PH1>".'], 103)
S4.add('Dữ liệu điền đúng', 'P0', PRE_E, EDIT, '—',
       ['Số phiếu, Ngày kiểm kê, Kho PTT, vị trí N1-T2-KV đã tick, bảng Chi tiết + ĐVT kiểm kê như lúc lưu, hội đồng Bùi Duy Trước + chức vụ.'], 104)
S4.add('Trường được / không được sửa', 'P0', PRE_E, EDIT, '—',
       ['Không sửa được: Số phiếu, Ngày kiểm kê, Kế hoạch kiểm kê (rê nhãn: "Kế hoạch kiểm kê chỉ chọn được lúc tạo phiếu, khi sửa phiếu '
        'giữ nguyên kế hoạch đã chọn.").', 'Sửa được: Kho vật lý, phạm vi, Lấy vị trí, ĐVT kiểm kê, hội đồng.'], 105)
S4.add('Sửa phiếu lập từ kế hoạch', 'P1', [ACC_A, 'Phiếu PH5 Đang tạo do A lập từ kế hoạch.'], ['Mở Sửa PH5.'], '—',
       ['Kế hoạch là liên kết mở tab mới; Kho vật lý và Phạm vi khóa; không có nút Lấy vị trí; ĐVT kiểm kê, hội đồng vẫn sửa được.'], 105)
S4.add('Các nút ở màn Sửa', 'P1', PRE_E, EDIT, '—', ['Có Lưu, Lưu và gửi, Quay lại; KHÔNG có Lưu và tiếp tục.'], 106)
S4.add('Sửa một trường', 'P0', PRE_E, EDIT + ['Đổi chức vụ của Bùi Duy Trước.', 'Bấm Lưu.'], 'Chức vụ: chức vụ khác',
       ['Báo "Lưu thành công.", về danh sách; trạng thái vẫn Đang tạo.'], [107, 69])
S4.add('Sửa nhiều trường', 'P0', PRE_E, EDIT + ['Tick thêm vị trí PTT-N1-KV1, bấm Lấy vị trí.', 'Thêm dòng hội đồng mới.', 'Bấm Lưu.'],
       '—', ['Lưu thành công; chi tiết có thêm hàng của PTT-N1-KV1 và 2 thành viên hội đồng.'], [108, 110])
S4.add('Giữ nguyên giá trị khi lưu không đổi', 'P1', PRE_E, EDIT + ['Không đổi gì, bấm Lưu.'], '—', ['Lưu thành công, không báo trùng.'], [109, 68])
S4.add('Ngày / người cập nhật', 'P1', PRE_E, EDIT + ['Đổi chức vụ, bấm Lưu.', 'Xem dòng PH1 ở danh sách.'], '—',
       ['Ngày cập nhật = thời điểm lưu, Người cập nhật = A.'], 111)
S4.add('Lịch sử sửa', 'P0', PRE_E, EDIT + ['Tick thêm vị trí, Lấy vị trí, bấm Lưu.', 'Mở Lịch sử của PH1.'], '—',
       ['Có mốc "Thay đổi thông tin", ghi Vị trí cũ > mới và Danh sách hàng tồn theo lô thêm dòng.'], [112, 177, 178])
S4.add('Bỏ trống bắt buộc khi sửa', 'P0', PRE_E, EDIT + ['Bỏ chọn nhân viên hội đồng.', 'Bấm Lưu.'], '—',
       ['"Nhân viên – Vui lòng chọn nhân viên." dưới ô, "Bạn chưa nhập đầy đủ thông tin.", không lưu.'], [113, 117])
S4.add('Sai định dạng / vượt giới hạn khi sửa', 'P2', PRE_E, EDIT + ['Quan sát các ô.'], '—',
       ['Form không có ô nhập tự do: Kho, ĐVT, Nhân viên, Chức vụ là ô chọn; không có giới hạn ký tự cần kiểm.'], [114, 115])
S4.add('Trùng bản ghi khác khi sửa', 'P2', [ACC_A, PH1, 'Có phiếu khác cùng kho, cùng phạm vi.'], EDIT + ['Bấm Lưu.'], '—',
       ['Lưu được (phiếu không có trường duy nhất).'], 116)
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P1', 'Đang có lỗi "Nhân viên – Vui lòng chọn nhân viên.".', ['Chọn lại nhân viên.'], '—', ['Lỗi biến mất ngay.'], 118)
S4.add('Mở Sửa rồi Quay lại không đổi', 'P1', PRE_E, EDIT + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], [119, 125])
S4.add('Đổi rồi trả về ban đầu', 'P2', PRE_E, EDIT + ['Đổi chức vụ rồi chọn lại chức vụ cũ.', 'Bấm Quay lại.'], '—', ['Không hỏi "Thông tin chưa lưu".'], 120)
S4.add('Rời màn khi đã đổi', 'P0', PRE_E, EDIT + ['Đổi chức vụ.', 'Bấm Quay lại.'], '—', ['Hiện hộp "Thông tin chưa lưu".'], 121)
S4.add('Xác nhận Thoát', 'P1', 'Đang ở hộp "Thông tin chưa lưu" của màn Sửa.', ['Bấm Thoát.'], '—',
       ['Về danh sách; PH1 không đổi; lịch sử không có mốc mới.'], [122, 124, 125])
S4.add('Xác nhận Ở lại', 'P2', 'Đang ở hộp "Thông tin chưa lưu" của màn Sửa.', ['Bấm Ở lại.'], '—', ['Ở lại màn Sửa, dữ liệu giữ nguyên.'], 123)
S4.add('Sửa phiếu đã gửi', 'P0', [ACC_A, PH2], ['Đăng nhập A.', MENU, 'Quan sát dòng PH2.', 'Mở đường link màn Sửa của PH2.'],
       '—', ['Dòng PH2 không có nút Sửa.', 'Mở màn Sửa tự chuyển sang màn chi tiết PH2.'], [126, 63])
S4.add('Phiếu bị xóa ở tab khác', 'P1', PRE_E, ['Tab 1 mở màn Sửa PH1.', 'Tab 2 xóa PH1.', 'Tab 1 bấm Lưu.'], '—',
       ['Báo "%s", không lưu.' % NOTFOUND], [127, 138])
S4.add('Phiếu vừa được gửi ở tab khác', 'P0', PRE_E, ['Tab 1 mở màn Sửa PH1.', 'Tab 2 mở Sửa PH1, bấm Lưu và gửi.', 'Tab 1 bấm Lưu.'],
       '—', ['Tab 1 báo "%s", không lưu.' % CONFLICT], [128, 91])
S4.add('Người khác không sửa được', 'P0', [ACC_T, PH1], ['Đăng nhập T.', MENU, 'Tìm PH1.'], '—',
       ['T không thấy PH1 (Đang tạo chỉ người tạo thấy) nên không sửa được.'], [128, 63])
S4.add('Phiếu đã có kết quả / đã duyệt', 'P1', [ACC_A, PH3], ['Đăng nhập A.', MENU, 'Quan sát dòng PH3.'], '—',
       ['Không có nút Sửa, Xóa (phiếu đang dùng ở bước duyệt).'], 129)

# ============================================================== V. XÓA
S5 = Sec(5)
S5.add('Nút Xóa chỉ ở phiếu Đang tạo của mình', 'P0', [ACC_A, PH1, PH2], ['Đăng nhập A.', MENU], '—',
       ['PH1 có nút Xóa (thùng rác đỏ); PH2 không có.'], 130)
S5.add('Hộp xác nhận xóa', 'P0', [ACC_A, PH1], ['Đăng nhập A.', MENU, 'Bấm Xóa ở dòng PH1.'], '—',
       ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa bản ghi này không?", nút Xóa (đỏ), Hủy.'], [131, 132])
S5.add('Xóa thành công', 'P0', [ACC_A, PH1], ['Bấm Xóa ở dòng PH1.', 'Bấm Xóa.'], '—',
       ['Báo "Xóa thành công.", PH1 biến mất, tổng giảm 1.'], [133, 139, 140])
S5.add('Hủy xóa', 'P1', [ACC_A, PH1], ['Bấm Xóa ở dòng PH1.', 'Bấm Hủy.'], '—', ['Đóng hộp, PH1 còn nguyên.'], 134)
S5.add('Xóa từ màn chi tiết', 'P1', [ACC_A, PH1], ['Mở chi tiết PH1.', 'Bấm Xóa ở chân màn, bấm Xóa.'], '—', ['Báo "Xóa thành công.", về danh sách.'], 133)
S5.add('Xóa phiếu lập từ kế hoạch trả kế hoạch về Đang kiểm', 'P0', [ACC_A, 'Phiếu PH5 Đang tạo lập từ KH1 (KH1 Đã lập kiểm kê).'],
       ['Xóa PH5.', 'Mở màn Kế hoạch kiểm kê theo vị trí.'], '—',
       ['KH1 trở về Đang kiểm; lịch sử KH1 có mốc ghi chú "Xóa phiếu kiểm kê <số phiếu PH5>.".', 'Thủ kho lập lại được phiếu từ KH1.'], [141, 281])
S5.add('Không xóa được phiếu đang dùng', 'P0', [ACC_A, PH2, PH3], ['Đăng nhập A.', MENU], '—',
       ['PH2, PH3 không có nút Xóa (đã gửi / đã nhập kết quả).'], [135, 137, 270])
S5.add('Xóa phiếu có dữ liệu con', 'P1', [ACC_A, PH1, 'PH1 có 3 vị trí, 10 lô (12 dòng ĐVT kiểm kê), 2 thành viên hội đồng.'], ['Xóa PH1.'], '—',
       ['Xóa thành công, toàn bộ phạm vi, chi tiết, dòng ĐVT, hội đồng bị xóa theo.'], [136, 285])
S5.add('Phiếu đã bị xóa ở tab khác', 'P1', [ACC_A, PH1], ['Tab 2 xóa PH1.', 'Tab 1 xóa PH1.'], '—', ['Tab 1 báo "%s".' % NOTFOUND], 138)
S5.add('Phiếu vừa được gửi ở tab khác', 'P1', [ACC_A, PH1], ['Tab 2 gửi PH1.', 'Tab 1 bấm Xóa PH1, bấm Xóa.'], '—',
       ['Báo "%s", không xóa.' % CONFLICT], 138)
S5.add('Dữ liệu liên quan sau xóa', 'P1', [ACC_A, PH1], ['Xóa PH1.', 'Vào danh mục Vị trí, xóa vị trí chỉ dùng ở PH1.'], '—',
       ['Vị trí xóa được (không còn phiếu nào dùng).'], [141, 280])

# ============================================================== VI. GỬI DUYỆT (Lưu và gửi + Nhập kết quả)
S6 = Sec(6)
S6.add('Nút Lưu và gửi', 'P0', PRE_FORM, TAO, '—', ['Nút Lưu và gửi (màu chính, biểu tượng máy bay giấy) ở chân màn Tạo và Sửa.'], 300)
S6.add('Lưu và gửi thành công', 'P0', PRE_FORM, FILL + ['Bấm Lưu và gửi.'], FULL,
       ['KHÔNG có hộp xác nhận; báo "Lưu và gửi thành công.", về danh sách.', 'Phiếu mới trạng thái Đang kiểm (nhãn vàng); dòng có Nhập kết quả.'],
       [86, 92, 301, 302, 305])
S6.add('Lưu và gửi khi thiếu bắt buộc', 'P0', PRE_FORM, TAO + ['Bấm Lưu và gửi.'], '—',
       ['Cùng bộ lỗi như Lưu, "Bạn chưa nhập đầy đủ thông tin.", không lưu.'], [87, 88, 303])
S6.add('Lưu và gửi trùng dữ liệu', 'P2', [PRE_FORM, PH2], FILL + ['Bấm Lưu và gửi.'], FULL, ['Lưu được, số phiếu khác PH2.'], 89)
S6.add('Gửi từ màn Sửa', 'P0', [ACC_A, PH1], ['Mở Sửa PH1.', 'Bấm Lưu và gửi.'], '—',
       ['Báo "Lưu và gửi thành công.", PH1 chuyển Đang kiểm; không còn Sửa, Xóa.'], [302, 305, 311])
S6.add('Màn sau khi gửi', 'P1', PRE_FORM, FILL + ['Bấm Lưu và gửi.'], FULL, ['Màn Tạo đóng, về danh sách.'], [90, 91, 92])
S6.add('Lịch sử khi gửi', 'P1', [ACC_A, PH1], ['Sửa PH1, bấm Lưu và gửi.', 'Mở Lịch sử PH1.'], '—',
       ['Có mốc "Thay đổi trạng thái" Đang tạo > Đang kiểm, người thực hiện A.'], [312, 92])
S6.add('Vị trí bị khóa sau khi gửi', 'P0', [ACC_A, 'PH2 Đang kiểm có vị trí N1-T2-KV.'],
       ['Vào Phiếu điều chuyển vị trí (phân hệ Kho), tạo phiếu ở kho PTT, chọn vị trí xuất N1-T2-KV.'], '—',
       ['Vị trí N1-T2-KV đánh dấu đang kiểm kho, không chọn được.'], [307, 281])
S6.add('Nhập kết quả: mở bước nhập', 'P0', [ACC_A, PH2], ['Đăng nhập A.', MENU, 'Ở dòng PH2 bấm Nhập kết quả.'], '—',
       ['Mở chi tiết PH2; bảng Chi tiết thêm cột Thực kiểm *, Chênh lệch, Ghi chú, Tổng kiểm kê; Thực kiểm mặc định = SL.',
        'Khối File đính kèm có nút Thêm tài liệu; chân màn có Lưu kết quả.'], [300, 51])
S6.add('Nhập kết quả: Chênh lệch tự tính', 'P0', [ACC_A, PH2], ['Mở Nhập kết quả PH2.', 'Đổi Thực kiểm lô TONDAUKHO-9113-11191-41 thành 669.'],
       'Thực kiểm: 669', ['Chênh lệch = -1, chữ đỏ; ô Tổng kiểm kê hiện ở dòng đó.', 'Đổi lại 670: Chênh lệch 0, ô Tổng kiểm kê ẩn.'], 306)
S6.add('Nhập kết quả: thiếu Ghi chú khi có chênh lệch', 'P0', [ACC_A, PH2], ['Đổi Thực kiểm thành 669, để trống Ghi chú.', 'Bấm Lưu kết quả.'],
       '—', ['Ghi chú viền đỏ "Bắt buộc phải nhập", báo "Bạn chưa nhập đầy đủ thông tin.", không lưu.'], [303, 304])
S6.add('Nhập kết quả: Thực kiểm trống / âm / quá lớn', 'P0', [ACC_A, PH2],
       ['Xóa trống Thực kiểm 1 dòng, bấm Lưu kết quả.', 'Nhập 1000000000, bấm Lưu kết quả.'], '—',
       ['Bước 1: "Bắt buộc phải nhập".', 'Bước 2: "Giá trị nhập vào không được vượt quá 999,999,999.".',
        'Ô chỉ nhận số, tối đa 2 chữ số thập phân; không gõ được dấu âm.'], [62, 303])
S6.add('Nhập kết quả: Ghi chú quá 255 ký tự', 'P2', [ACC_A, PH2], ['Nhập Ghi chú 256 ký tự ở dòng chênh lệch, bấm Lưu kết quả.'], '—',
       ['Báo "Vui lòng nhập tối đa 255 ký tự." dưới ô, không lưu.'], 303)
S6.add('Nhập kết quả: thiếu file khi phiếu chưa có file', 'P0', [ACC_A, PH2], ['Nhập đủ Thực kiểm, không đính file.', 'Bấm Lưu kết quả.'], '—',
       ['Báo "File đính kèm – Vui lòng chọn file đính kèm.", không lưu.'], [303, 304])
S6.add('Nhập kết quả: file sai loại / quá dung lượng', 'P1', [ACC_A, PH2], ['Bấm Thêm tài liệu, chọn file .zip.', 'Chọn file .pdf 25MB.'], '—',
       ['Bước 1: "Chỉ nhận file pdf, png, jpg, jpeg, doc, docx, xls, xlsx".', 'Bước 2: "Dung lượng tối đa 20MB".'], 303)
S6.add('Lưu kết quả thành công', 'P0', [ACC_A, PH2, ACC_K], ['Nhập Thực kiểm 669 + Ghi chú "Thiếu 1", đính 1 file pdf.', 'Bấm Lưu kết quả.'],
       ['Thực kiểm: 669', 'Ghi chú: Thiếu 1'],
       ['KHÔNG có hộp xác nhận; báo "Lưu kết quả thành công.", về danh sách.', 'PH2 chuyển Chờ duyệt kết quả; A không còn Nhập kết quả.'],
       [302, 305, 306])
S6.add('Thông báo đến Ban kiểm soát', 'P0', [ACC_A, PH2, ACC_K, 'Tài khoản K2 có quyền "%s" thuộc công ty TPSG.' % Q2],
       ['A Lưu kết quả PH2.'], '—',
       ['K nhận "[KKVT] Chờ duyệt: <số phiếu PH2>" kèm Người nhập kết quả, Kho, Kế hoạch.', 'K2 (khác công ty) KHÔNG nhận.',
        'Bấm thông báo mở chi tiết PH2.'], [308, 309])
S6.add('Lịch sử khi Lưu kết quả', 'P1', [ACC_A, 'A vừa Lưu kết quả PH2.'], ['Mở Lịch sử PH2.'], '—',
       ['Mốc "Thay đổi thông tin": Kết quả kiểm kê (Thực kiểm, Chênh lệch, Ghi chú, Tổng kiểm kê cũ > mới), File đính kèm.',
        'Mốc "Thay đổi trạng thái" Đang kiểm > Chờ duyệt kết quả.'], [312, 183])
S6.add('Rời bước nhập kết quả chưa lưu', 'P1', [ACC_A, PH2], ['Đổi Thực kiểm 1 dòng.', 'Bấm Quay lại.', 'Bấm Thoát.'], '—',
       ['Hiện hộp "Thông tin chưa lưu"; Thoát > về danh sách, PH2 vẫn Đang kiểm, không có mốc lịch sử mới.'], 310)
S6.add('Không gửi lại phiếu đã gửi', 'P0', [ACC_A, PH3], [MENU, 'Quan sát dòng PH3.', 'Mở chi tiết PH3.'], '—',
       ['Không có Sửa, Lưu và gửi, Nhập kết quả, Lưu kết quả cho PH3.'], 311)
S6.add('Lưu kết quả khi phiếu vừa bị đổi', 'P1', [ACC_A, PH2], ['Tab 1, tab 2 mở Nhập kết quả PH2.', 'Tab 2 Lưu kết quả.', 'Tab 1 Lưu kết quả.'],
       '—', ['Tab 1 báo "%s", không ghi.' % CONFLICT], [311, 128])

# ============================================================== VII. DUYỆT PHIẾU (Duyệt kết quả + Xử lý)
S7 = Sec(7)
S7.add('Điều kiện hiện nút Duyệt kết quả', 'P0', [ACC_K, PH3, PH2], ['Đăng nhập K.', 'Mở chi tiết PH3 (từ thông báo).', 'Mở chi tiết PH2.'], '—',
       ['PH3: chân màn có Duyệt kết quả, Không duyệt.', 'PH2: không có 2 nút.', 'A (người tạo, không có quyền) mở PH3: không có 2 nút.'], 300)
S7.add('Giao diện popup Duyệt kết quả', 'P0', [ACC_K, PH3], ['Mở chi tiết PH3.', 'Bấm Duyệt kết quả.'], '—',
       ['Popup "Duyệt kết quả kiểm kê", dòng phụ "Phiếu: <số phiếu PH3>".', 'Ô Ghi chú duyệt (gợi ý "Nhập ghi chú duyệt"), không bắt buộc.',
        'Nút Duyệt kết quả, Hủy (mũi tên trái), (x).'], 301)
S7.add('Duyệt phiếu có chênh lệch thiếu', 'P0', [ACC_K, PH3, ACC_X], ['Bấm Duyệt kết quả, nhập "Đồng ý", bấm Duyệt kết quả.'], 'Ghi chú duyệt: Đồng ý',
       ['Báo "Duyệt kết quả thành công.", về danh sách.', 'PH3 chuyển Chờ xử lý; Người duyệt K, Ngày duyệt hôm nay.'], [302, 305, 306])
S7.add('Duyệt phiếu không chênh lệch thiếu', 'P0', [ACC_K, PH3B], ['Duyệt PH3B, không nhập ghi chú.'], '—',
       ['PH3B chuyển Hoàn thành; kế hoạch KH2 chuyển Hoàn thành, lịch sử KH2 ghi "Phiếu kiểm kê <số phiếu> được duyệt kết quả.".'],
       [302, 304, 307])
S7.add('Không cần dữ liệu bắt buộc khi duyệt', 'P1', [ACC_K, PH3], ['Bấm Duyệt kết quả, để trống Ghi chú, bấm Duyệt kết quả.'], '—',
       ['Duyệt thành công (ghi chú không bắt buộc).', 'Ghi chú quá 5000 ký tự > "Ghi chú duyệt – Tối đa 5000 ký tự.".'], 303)
S7.add('Thông báo đến người xử lý', 'P0', [ACC_K, PH3, ACC_X], ['K duyệt PH3 (có thiếu).'], '—',
       ['X nhận "[KKVT] Đã duyệt: <số phiếu>" kèm Người duyệt, "Có chênh lệch thiếu cần xử lý", Kho, Ghi chú duyệt.',
        'Duyệt phiếu không thiếu thì không gửi thông báo.'], 308)
S7.add('Bấm thông báo mở phiếu Chờ xử lý', 'P1', [ACC_X, 'X vừa nhận thông báo của PH3.'], ['Bấm thông báo.'], '—',
       ['Mở chi tiết PH3 dù X không có quyền xem theo cấp; có nút Tạo phiếu điều chuyển vị trí.'], 309)
S7.add('Hủy thao tác duyệt', 'P1', [ACC_K, PH3], ['Bấm Duyệt kết quả, nhập ghi chú.', 'Bấm Hủy.'], '—',
       ['Popup đóng; PH3 vẫn Chờ duyệt kết quả, Người duyệt trống.'], 310)
S7.add('Không duyệt lại phiếu đã xử lý', 'P0', [ACC_K, PH3], ['Tab 1, tab 2 mở chi tiết PH3.', 'Tab 2 duyệt.', 'Tab 1 bấm Duyệt kết quả trong popup.'],
       '—', ['Tab 1 báo "%s".' % CONFLICT, 'Phiếu Chờ xử lý / Hoàn thành không còn nút Duyệt kết quả.'], 311)
S7.add('Lịch sử duyệt', 'P0', [ACC_K, 'K vừa duyệt PH3 với ghi chú "Đồng ý".'], ['Mở Lịch sử PH3.'], '—',
       ['Mốc "Duyệt", Người thực hiện K, "Trạng thái: Chờ duyệt kết quả > Chờ xử lý", ghi chú "Đồng ý".'], 312)
S7.add('Xử lý: tick Tổng kiểm kê lưu ngay', 'P0', [ACC_X, PH4], ['Mở chi tiết PH4.', 'Tick Tổng kiểm kê ở dòng -1.'], '—',
       ['Báo "Cập nhật thành công."; còn dòng -3 nên vẫn có Tạo phiếu điều chuyển vị trí.', 'Lịch sử có mốc "Thay đổi thông tin" Tổng kiểm kê Không > Có.'],
       [306, 177])
S7.add('Xử lý: tick hết dòng thiếu hiện Hoàn thành', 'P0', [ACC_X, PH4], ['Tick Tổng kiểm kê cả 2 dòng thiếu.'], '—',
       ['Nút Tạo phiếu điều chuyển vị trí biến mất, hiện Hoàn thành; trên danh sách dòng PH4 có nút Xử lý.'], 306)
S7.add('Xử lý: Tạo phiếu điều chuyển vị trí', 'P0', [ACC_X, PH4], ['Mở chi tiết PH4.', 'Bấm Tạo phiếu điều chuyển vị trí.'], '—',
       ['Mở màn Tạo phiếu điều chuyển vị trí (phân hệ Kho) với kho PTT và 2 dòng thiếu nạp sẵn.'], [307, 274])
S7.add('Xử lý: Hoàn thành', 'P0', [ACC_X, 'PH4 đã tick Tổng kiểm kê cả 2 dòng.'], ['Bấm Hoàn thành.', 'Bấm Hoàn thành ở hộp xác nhận.'], '—',
       ['Hộp "Xác nhận hoàn thành": "Hoàn thành phiếu kiểm kê \\"<số phiếu>\\"? Phiếu sẽ chuyển sang trạng thái Hoàn thành và không xử lý thêm được nữa.".',
        'Báo "Hoàn thành phiếu kiểm kê thành công.", PH4 Hoàn thành; kế hoạch cha KHÔNG đổi.'], [305, 307])
S7.add('Xử lý: Hủy hộp Hoàn thành', 'P2', [ACC_X, 'PH4 đã tick hết dòng thiếu.'], ['Bấm Hoàn thành.', 'Bấm Hủy.'], '—', ['PH4 vẫn Chờ xử lý.'], 310)
S7.add('Xử lý: điều chuyển hết tự Hoàn thành', 'P0', [ACC_X, PH4], ['Lập Phiếu điều chuyển vị trí từ PH4 cho đủ 4 đơn vị thiếu, bấm Điều chuyển.',
                                                                   'Mở danh sách Kiểm kê theo vị trí.'], '—',
       ['PH4 tự chuyển Hoàn thành; kế hoạch cha (nếu có) chuyển Hoàn thành.'], [281, 307])
S7.add('Xử lý: Hoàn thành khi còn dòng cần điều chuyển', 'P1', [ACC_X, 'PH4 đã tick hết; tab 2 bỏ tick 1 dòng.'], ['Tab 1 bấm Hoàn thành, xác nhận.'],
       '—', ['Báo "Còn dòng chênh lệch thiếu chưa xử lý. Vui lòng tạo phiếu điều chuyển vị trí hoặc tick \\"Tổng kiểm kê\\".", không đổi.'], 304)

# ============================================================== VIII. KHÔNG DUYỆT PHIẾU
S8 = Sec(8)
S8.add('Điều kiện hiện nút Không duyệt', 'P0', [ACC_K, PH3], ['Đăng nhập K, mở chi tiết PH3.', 'Đăng nhập A, mở chi tiết PH3.'], '—',
       ['K: có Không duyệt (nút đỏ).', 'A: không có.'], 313)
S8.add('Giao diện popup Không duyệt', 'P0', [ACC_K, PH3], ['Bấm Không duyệt.'], '—',
       ['Popup "Không duyệt kết quả kiểm kê", dòng phụ "Phiếu: <số phiếu>".', 'Ô Ghi chú duyệt * (gợi ý "Nhập lý do không duyệt").',
        'Nút Không duyệt (đỏ), Hủy, (x).'], 314)
S8.add('Không duyệt thành công', 'P0', [ACC_K, PH3], ['Bấm Không duyệt, nhập "Đếm lại lô 670", bấm Không duyệt.'], 'Lý do: Đếm lại lô 670',
       ['Báo "Không duyệt kết quả thành công.", về danh sách.'], 315)
S8.add('Bỏ trống lý do', 'P0', [ACC_K, PH3], ['Bấm Không duyệt, để trống, bấm Không duyệt.'], '—',
       ['Ô viền đỏ "Vui lòng nhập lý do không duyệt", popup không đóng, phiếu không đổi.', 'Nhập chỉ khoảng trắng cũng báo như trên.'], 316)
S8.add('Lý do quá giới hạn', 'P2', [ACC_K, PH3], ['Nhập lý do 5001 ký tự, bấm Không duyệt.'], '—', ['Báo "Ghi chú duyệt – Tối đa 5000 ký tự.".'], 317)
S8.add('Trạng thái sau không duyệt', 'P0', [ACC_K, PH3], ['Không duyệt PH3.', 'Đăng nhập A, mở PH3.'], '—',
       ['PH3 về Đang kiểm; A thấy lại Nhập kết quả, Thực kiểm giữ giá trị đã nhập trước.'], [318, 320])
S8.add('Lý do được lưu', 'P1', [ACC_K, 'K vừa không duyệt PH3.'], ['Mở Lịch sử PH3.', 'In phiếu PH3.'], '—',
       ['Lịch sử: mốc "Từ chối", "Trạng thái: Chờ duyệt kết quả > Đang kiểm", ghi chú lý do.', 'Bản in: mục "Nhận xét, đánh giá" là lý do.'],
       [319, 324])
S8.add('Thông báo đến người tạo', 'P0', [ACC_K, PH3], ['K không duyệt PH3.'], '—',
       ['A nhận "[KKVT] Từ chối: <số phiếu>" kèm Người từ chối, Lý do; bấm mở chi tiết PH3.'], 321)
S8.add('Hủy thao tác không duyệt', 'P1', [ACC_K, PH3], ['Bấm Không duyệt, nhập lý do, bấm Hủy.'], '—', ['PH3 vẫn Chờ duyệt kết quả.'], 322)
S8.add('Không duyệt phiếu đã đổi trạng thái', 'P1', [ACC_K, PH3], ['Tab 2 duyệt PH3.', 'Tab 1 bấm Không duyệt, nhập lý do, xác nhận.'], '—',
       ['Tab 1 báo "%s".' % CONFLICT], 323)

# ============================================================== IX. LỊCH SỬ THAY ĐỔI
S9 = Sec(9)
PRE_H = [PRE_LIST, P140]
HIS = [MENU, 'Ở dòng TPE-KKVT-00140 bấm Lịch sử.']
S9.add('Mở cửa sổ lịch sử', 'P0', PRE_H, HIS, '—', ['Cửa sổ "Lịch sử thay đổi: TPE-KKVT-00140".'], 162)
S9.add('Các thông tin của mốc', 'P0', PRE_H, HIS, '—',
       ['Mỗi mốc: thời điểm, hành động, "Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ", nội dung.'], [163, 165, 166, 167])
S9.add('Mới nhất trước', 'P0', PRE_H, HIS, '—',
       ['7 mốc; trên cùng 23/10/2026 11:39 "Duyệt" (Chờ duyệt kết quả > Hoàn thành), dưới cùng "Tạo mới".'], 164)
S9.add('Nội dung kết quả kiểm kê', 'P0', PRE_H, HIS, '—',
       ['Mốc "Thay đổi thông tin" liệt kê từng dòng "Quạt ENEOS (Vị trí: N1-T2-KV; Lô: …; ĐVT kiểm kê: Cái.)": Thực kiểm (trống) 670; '
        'Chênh lệch (trống) 0; Tổng kiểm kê (trống) Không.'], 168)
S9.add('Lọc theo hành động', 'P1', PRE_H, HIS + ['Bấm Bộ lọc, chọn Loại hành động = Tạo mới.'], '—', ['Chỉ còn mốc Tạo mới.'], 169)
S9.add('Lọc theo người thực hiện', 'P2', PRE_H, HIS + ['Bấm Bộ lọc, chọn Người thực hiện = DNS Admin.'], '—', ['Còn đủ 7 mốc.'], 170)
S9.add('Lọc theo thời gian', 'P1', PRE_H, HIS + ['Bấm Bộ lọc, Từ ngày 24/10/2026.'], '—', ['"Không có lịch sử phù hợp bộ lọc." (mọi mốc ngày 23/10/2026).'], [171, 173])
S9.add('Kết hợp lọc', 'P2', PRE_H, HIS + ['Chọn Loại hành động = Thay đổi trạng thái, Người thực hiện = DNS Admin.'], '—', ['Chỉ còn các mốc Thay đổi trạng thái.'], 172)
S9.add('Làm mới / đóng mở bộ lọc', 'P2', PRE_H, HIS + ['Lọc rồi bấm Làm mới.', 'Bấm Bộ lọc lần nữa.'], '—',
       ['Làm mới: hiện lại 7 mốc.', 'Bộ lọc thu gọn / mở lại.'], [174, 175])
S9.add('Phiếu chưa có lịch sử', 'P1', [PRE_LIST, 'TPSG-KKVT-00132 lập trên hệ thống cũ.'], [MENU, 'Mở Lịch sử TPSG-KKVT-00132 (ba chấm > Lịch sử).'],
       '—', ['"Chưa có lịch sử thao tác nào.".'], 162)
S9.add('Sửa không đổi gì thì không ghi', 'P1', [ACC_A, PH1], ['Sửa PH1, không đổi, bấm Lưu.', 'Mở Lịch sử.'], '—',
       ['Không có mốc "Thay đổi thông tin" mới.'], [182, 125])
S9.add('Đổi nhiều thông tin cùng lúc', 'P1', [ACC_A, PH1], ['Sửa PH1: đổi phạm vi + hội đồng, bấm Lưu và gửi.', 'Mở Lịch sử.'], '—',
       ['1 mốc "Thay đổi thông tin" liệt kê Vị trí, Danh sách hàng tồn theo lô, Hội đồng (cũ > mới) + 1 mốc "Thay đổi trạng thái".'], 183)
S9.add('Đóng cửa sổ', 'P1', PRE_H, HIS + ['Bấm Đóng.', 'Mở lại, bấm (x).'], '—', ['Cả 2 cách đều đóng cửa sổ.'], 184)
S9.add('Trạng thái danh sách sau khi đóng', 'P1', 'Đang ở trang 2, lọc Trạng thái = Hoàn thành.', ['Mở Lịch sử 1 dòng, bấm Đóng.'], '—',
       ['Danh sách giữ trang 2, bộ lọc, sắp xếp.'], 185)
S9.add('Lịch sử ở màn chi tiết', 'P1', PRE_H, DET('TPE-KKVT-00140') + ['Ở khối Lịch sử bấm Xem lịch sử.'], '—',
       ['Khối Lịch sử có số 7; bấm mở rộng hiện 7 mốc; nút đổi thành Thu gọn.'], [195, 162])

# ============================================================== X. XEM CHI TIẾT
S10 = Sec(10)
S10.add('Mở màn chi tiết', 'P0', PRE_H, DET('TPE-KKVT-00140'), '—', ['Mở TRANG chi tiết (không phải cửa sổ nổi).'], 186)
S10.add('Tiêu đề', 'P1', PRE_H, DET('TPE-KKVT-00140'), '—', ['"Chi tiết phiếu kiểm kê theo vị trí: TPE-KKVT-00140", không kèm nhãn trạng thái.'], 187)
S10.add('Đầy đủ trường', 'P0', PRE_H, DET('TPE-KKVT-00140'), '—',
       ['Thông tin chung: Số phiếu, Kế hoạch kiểm kê (trống), Ngày kiểm kê, Kho vật lý; File đính kèm (1 file); Phạm vi 4 cột; Chi tiết có '
        'Thực kiểm, Chênh lệch, Ghi chú, Tổng kiểm kê; Hội đồng (Bùi Hữu Hanh); khối Lịch sử.'], 188)
S10.add('Khớp dữ liệu tạo và danh sách', 'P1', PRE_H, DET('TPE-KKVT-00140'), '—',
       ['Kho Phan Trọng Tuệ, Ngày kiểm kê 23/10/2026, người tạo DNS Admin khớp dòng ở danh sách.'], [189, 190])
S10.add('Trường chỉ đọc, không có nút Lưu', 'P0', PRE_H, DET('TPE-KKVT-00140'), '—',
       ['Mọi ô khóa, phạm vi không tick được, Thực kiểm / Ghi chú là chữ.', 'Chân màn: In, Xuất Excel, Quay lại; không có Lưu.'], [191, 192])
S10.add('Nút theo trạng thái ở chi tiết', 'P0', [ACC_A, PH1, PH2], ['Mở chi tiết PH1.', 'Mở chi tiết PH2.'], '—',
       ['PH1: Sửa, In, Xuất Excel, Xóa, Quay lại.', 'PH2: Lưu kết quả, In, Xuất Excel, Quay lại.'], [193, 194])
S10.add('Phiếu lập từ kế hoạch', 'P1', [PRE_LIST, P139], DET('TPE-KKVT-00139'), '—',
       ['Ô Kế hoạch kiểm kê là liên kết "TPE-KHKKVT-00137", bấm mở tab mới.'], 188)
S10.add('Phiếu chưa có file', 'P2', [ACC_A, PH1], ['Mở chi tiết PH1.'], '—', ['Không có khối File đính kèm.'], 188)
S10.add('Quay lại giữ trang và bộ lọc', 'P0', 'Đang ở trang 2, lọc Trạng thái = Hoàn thành.', ['Bấm số phiếu 1 dòng.', 'Bấm Quay lại.'], '—',
       ['Về danh sách giữ bộ lọc Trạng thái = Hoàn thành (trong 10 phút).'], [196, 197])
S10.add('Phiếu ngoài phạm vi', 'P0', [ACC_B, 'Phiếu TPSG-KKVT-00130 Hoàn thành công ty TPSG.'], ['Đăng nhập B.', 'Mở đường link chi tiết phiếu đó.'],
       '—', ['Chuyển sang trang "Không tìm thấy trang".'], [186, 296])

# ============================================================== XI. IN PHIẾU
S11 = Sec(11)
S11.add('In phiếu từ danh sách', 'P0', PRE_H, [MENU, 'Bấm In ở dòng TPE-KKVT-00140.'], '—',
       ['Cửa sổ "Xem trước phiếu kiểm kê theo vị trí TPE-KKVT-00140".',
        'Bản in: letterhead công ty của phiếu, "KIỂM KÊ THEO VỊ TRÍ", Số phiếu, Ngày kiểm kê, Kế hoạch kiểm kê, Kho vật lý, Hội đồng.',
        'Bảng: STT, Nhà kho, Vị trí, Tên hàng, Mã hàng, ĐVT, SL tồn, Công ty, Lô, SL, ĐVT kiểm kê, Thực kiểm, Ghi chú; Nhận xét, đánh giá; khối ký.'], 228)
S11.add('In phiếu từ màn chi tiết', 'P1', PRE_H, DET('TPE-KKVT-00140') + ['Bấm In.'], '—', ['Cùng cửa sổ xem trước như in từ danh sách.'], 228)
S11.add('In phiếu chưa nhập kết quả', 'P2', [ACC_A, PH2], ['In PH2.'], '—', ['Cột Thực kiểm để trống.'], 228)
S11.add('Bấm In trong cửa sổ', 'P1', 'Đang mở cửa sổ xem trước.', ['Bấm In.'], '—', ['Mở hộp thoại in của trình duyệt.'], 228)
S11.add('In danh sách theo bộ lọc', 'P0', PRE_LIST, [MENU, 'Lọc Trạng thái = Chờ xử lý.', 'Bấm In danh sách.'], '—',
       ['Cửa sổ "Xem trước danh sách kiểm kê theo vị trí".',
        'Bảng 2 dòng: STT, Số phiếu, Kế hoạch kiểm kê, Ngày kiểm kê, Kho, Người tạo, Người duyệt, Ngày duyệt, Trạng thái; khối ký Người lập = người in.'],
       [220, 227])
S11.add('In danh sách vượt 2.000 dòng', 'P2', 'Bộ lọc ra hơn 2.000 phiếu.', ['Bấm In danh sách.'], '—',
       ['Không có bản xem trước, ẩn nút In, hiện dòng nhắc thu hẹp bộ lọc.'], 221)
S11.add('In danh sách rỗng', 'P2', 'Bộ lọc không ra phiếu nào.', ['Bấm In danh sách.'], '—', ['"Không có dữ liệu để in".'], 222)
S11.add('Đóng cửa sổ xem trước', 'P2', 'Đang mở cửa sổ xem trước.', ['Bấm (x).'], '—', ['Đóng, giữ nguyên màn đang đứng.'], 184)

# ============================================================== XII. TÙY CHỈNH CỘT
S12 = Sec(12)
S12.add('Mở cửa sổ tùy chỉnh cột', 'P0', PRE_LIST, [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" liệt kê 13 cột, "Đang chọn 13/13 cột".'], [198, 199, 200])
S12.add('Ẩn cột', 'P0', PRE_LIST, ['Bỏ tích Người duyệt, bấm Lưu.'], '—', ['"Cập nhật thành công", bảng không còn cột Người duyệt.'], [202, 206])
S12.add('Hiện cột đã ẩn', 'P1', 'Đã ẩn Người duyệt.', ['Tích lại Người duyệt, bấm Lưu.'], '—', ['Cột hiện lại.'], 201)
S12.add('Cột bắt buộc không ẩn', 'P0', PRE_LIST, ['Mở cửa sổ, thử bỏ tích STT, Số phiếu, Hành động.'], '—',
       ['3 cột có biểu tượng ổ khóa, không bỏ tích, không kéo được.'], [203, 205])
S12.add('Kéo thả thứ tự', 'P1', PRE_LIST, ['Kéo Kho lên trên Ngày kiểm kê, bấm Lưu.'], '—', ['Bảng hiện Kho trước Ngày kiểm kê.'], 204)
S12.add('Chọn tất cả / Bỏ chọn hết', 'P2', PRE_LIST, ['Bấm Bỏ chọn hết.', 'Bấm Chọn tất cả.'], '—',
       ['Bỏ chọn hết: còn 3 cột khóa.', 'Chọn tất cả: 13/13.'], 202)
S12.add('Đóng không lưu', 'P1', PRE_LIST, ['Bỏ tích Kho, bấm Đóng.'], '—', ['Bảng vẫn có cột Kho.'], 207)
S12.add('Ghi nhớ sau F5 và theo tài khoản', 'P1', 'A đã ẩn cột Người duyệt.', ['Nhấn F5.', 'Đăng nhập B trên cùng máy.'], '—',
       ['A: vẫn ẩn sau F5 và đăng nhập máy khác.', 'B: thấy đủ 13 cột.'], [208, 209])
S12.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', 'Đang lọc Trạng thái = Hoàn thành (46).', ['Ẩn cột Trạng thái, bấm Lưu.'], '—',
       ['Vẫn 46 phiếu, bộ lọc giữ nguyên.'], [210, 211])

# ============================================================== XIII. XUẤT DANH SÁCH EXCEL
S13 = Sec(13)
S13.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất Excel" với 11 trường: Số phiếu, Kế hoạch kiểm kê, Ngày kiểm kê, Kho, Trạng thái, Người tạo, Người duyệt, '
        'Ngày duyệt, Ngày tạo, Ngày cập nhật, Người cập nhật.', 'Trường tích sẵn theo cột đang hiện trên bảng (13/13 cột đang hiện > đủ 11/11 trường).',
        'Lưu ý: hiện "Người duyệt" không được tích sẵn ("Đang chọn 10/11 trường") — nếu vẫn vậy thì ghi nhận lỗi.'], [212, 213, 214])
S13.add('Xuất trường mặc định', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel, bấm Xuất file.'], '—',
       ['Tải "danh_sach_phieu_kiem_ke_theo_vi_tri.xlsx", báo "Xuất Excel thành công.".',
        'File: letterhead, "DANH SÁCH PHIẾU KIỂM KÊ THEO VỊ TRÍ", cột STT + trường đã tích, 52 dòng, khối ký.'], [215, 223, 224, 225, 227])
S13.add('Xuất tất cả trường', 'P1', PRE_LIST, ['Bấm Xuất Excel, Chọn tất cả, Xuất file.'], '—', ['File có STT + 11 cột.'], 216)
S13.add('Xuất một số trường theo thứ tự kéo', 'P1', PRE_LIST, ['Bỏ chọn hết, tích Kho rồi Số phiếu, kéo Kho lên đầu, Xuất file.'], '—',
       ['File chỉ có STT, Kho, Số phiếu theo đúng thứ tự.'], [217, 226])
S13.add('Không chọn trường', 'P1', PRE_LIST, ['Bấm Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S13.add('Xuất theo tìm kiếm / bộ lọc', 'P0', PRE_LIST, ['Lọc Trạng thái = Hoàn thành, Ngày kiểm kê 01/10/2026 – 31/10/2026.', 'Xuất file.'],
       '—', ['File chỉ có phiếu khớp (TPE-KKVT-00140, 00139); có dòng "Từ ngày 01/10/2026 đến ngày 31/10/2026".'], [219, 220])
S13.add('Xuất nhiều trang', 'P1', PRE_LIST, ['Đang ở trang 1 (10 dòng), Xuất file.'], '—', ['File có đủ 52 dòng.'], 221)
S13.add('Danh sách rỗng', 'P2', 'Bộ lọc không ra phiếu nào.', ['Xuất file.'], '—', ['Vẫn ra file có tiêu đề, dòng tên cột, khối ký.'], 222)
S13.add('Dữ liệu khớp, định dạng ngày và tiếng Việt', 'P1', [PRE_LIST, P140], ['Xuất file, mở dòng TPE-KKVT-00140.'], '—',
       ['Ngày kiểm kê "23/10/2026", Ngày tạo "23/10/2026 11:25" dạng chữ; Kho "Phan Trọng Tuệ", Trạng thái "Hoàn thành" đủ dấu.'], [228, 229, 230])
S13.add('Xuất Excel 1 phiếu', 'P0', PRE_H, [MENU, 'Ở dòng TPE-KKVT-00140 bấm Xuất Excel.'], '—',
       ['Tải "kiem_ke_theo_vi_tri_TPE-KKVT-00140.xlsx", báo "Xuất Excel thành công.".',
        'File: letterhead công ty của phiếu, Số phiếu, Ngày kiểm kê, Kế hoạch kiểm kê, Kho vật lý, Hội đồng, bảng chi tiết (số là ô số), '
        '"Nhận xét, đánh giá:", khối ký Hội đồng kiểm kê / Trưởng bộ phận kho.'], [223, 228, 293])

# ============================================================== XIV. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S14 = Sec(14)
S14.add('Kế hoạch Đang kiểm hiện ở popup Chọn kế hoạch', 'P0', [ACC_A, KH, 'Kế hoạch KH3 Đang kiểm ở kho Cát Bà (A không phải thủ kho).'],
       TAO + ['Bấm ô Kế hoạch kiểm kê.'], '—', ['Popup có KH1; không có KH3, không có kế hoạch Đang tạo / Đã lập kiểm kê / Hoàn thành.'], [274, 276])
S14.add('Bộ lọc màn liên quan cập nhật', 'P2', [ACC_A, KH], ['Lập và lưu phiếu từ KH1.', 'Mở lại popup Chọn kế hoạch.'], '—',
       ['KH1 không còn trong popup.'], 282)
S14.add('Trạng thái kế hoạch đổi theo phiếu', 'P0', [ACC_A, KH], ['Lập phiếu từ KH1, lưu.', 'Mở màn Kế hoạch kiểm kê theo vị trí.'], '—',
       ['KH1 chuyển Đã lập kiểm kê; lịch sử KH1 có mốc Thay đổi trạng thái kèm mã phiếu.'], [281, 284])
S14.add('Phiếu nhập kho chặn vị trí đang kiểm', 'P0', [ACC_A, 'PH2 Đang kiểm có vị trí N1-T2-KV.'],
       ['Vào phân hệ Kho > Nhập kho > Phiếu nhập kho, lập phiếu nhập hàng vào vị trí N1-T2-KV, bấm lưu nhập kho.'], '—',
       ['Hệ thống chặn: "Vị trí N1-T2-KV đang kiểm kho".', 'Lưu ý: khi phiếu đã Chờ duyệt kết quả, Phiếu nhập kho KHÔNG còn chặn (Phiếu điều '
        'chuyển vị trí vẫn chặn) — ghi nhận nếu nghiệp vụ yêu cầu chặn cả bước chờ duyệt.'], [281, 307])
S14.add('Phiếu điều chuyển đọc dòng thiếu', 'P0', [ACC_X, PH4], ['Bấm Tạo phiếu điều chuyển vị trí ở PH4.'], '—',
       ['Màn Tạo phiếu điều chuyển nạp đúng 2 dòng thiếu (-1, -3), kho PTT; cột nguồn liên kết về PH4.'], [274, 272])
S14.add('Không xóa được danh mục kho đang dùng', 'P0', [ACC_A, PH2], ['Vào phân hệ Kho > Danh mục > Vị trí, xóa vị trí N1-T2-KV.'], '—',
       ['Hệ thống chặn xóa vì vị trí đang được dùng.', 'Tương tự với Nhà kho, Dãy, Khoang, Kho vật lý đã có trong phiếu.'], 270)
S14.add('Không xóa được hàng hóa đang dùng', 'P1', [ACC_A, PH2], ['Vào danh mục Hàng hoá, xóa "Quạt ENEOS".'], '—',
       ['Hệ thống chặn xóa vì hàng đã có trong chứng từ.'], 270)
S14.add('Đổi tên danh mục không đổi phiếu', 'P1', [ACC_A, PH2], ['Đổi tên vị trí N1-T2-KV thành "N1-T2-KV-NEW".', 'Mở chi tiết PH2.'], '—',
       ['Bảng Chi tiết vẫn ghi tên hàng, mã hàng như lúc lấy; liên kết vị trí không mất.'], [272, 278, 279])
S14.add('Số tồn là ảnh chụp', 'P1', [ACC_A, PH1], ['Nhập thêm 10 Quạt ENEOS vào N1-T2-KV.', 'Mở chi tiết PH1.'], '—',
       ['SL tồn trên PH1 vẫn 1,227; chỉ đổi khi Sửa và bấm Lấy vị trí lại.'], [286, 269])
S14.add('Tồn kho không đổi khi duyệt', 'P0', [ACC_K, PH3], ['Ghi tồn lô TONDAUKHO-9113-11191-41.', 'Duyệt PH3.', 'Xem lại tồn.'], '—',
       ['Tồn không đổi (phiếu không ghi tồn; chỉ phiếu điều chuyển ghi).'], 286)
S14.add('Danh mục kho đã khóa không hiện để tick', 'P1', [PRE_FORM, 'Vị trí PTT-N1-KV9 đã bị khóa ở danh mục Vị trí.'],
       TAO + ['Chọn Kho PTT.', 'Tìm "KV9" ở cột Vị trí.'], '—', ['Không có PTT-N1-KV9 để tick.'], [276, 284])

# ============================================================== XV. PHÂN QUYỀN (cuối)
S15 = Sec(15)
S15.add('Quyền tổng công ty: xem mọi phiếu', 'P0', [ACC_T, '52 phiếu không Đang tạo thuộc TPE, TPSG, TPV, TPHP.'], ['Đăng nhập T.', MENU], '—',
       ['Thấy đủ 52 phiếu; có ô Công ty – Phòng ban, chọn được mọi công ty.'], [287, 299])
S15.add('Quyền công ty: chỉ công ty mình + của mình', 'P0', [ACC_C, 'TPE có 7 phiếu, TPSG 12, TPV 28, TPHP 5.'], ['Đăng nhập C.', MENU], '—',
       ['Chỉ thấy 7 phiếu TPE (và phiếu C tự tạo); ô Công ty khóa ở TPE.'], [287, 299])
S15.add('Không quyền: chỉ phiếu mình tạo', 'P0', [ACC_A, 'A tạo 2 phiếu.'], ['Đăng nhập A.', MENU], '—',
       ['Chỉ thấy 2 phiếu của A; không có ô Công ty – Phòng ban.'], [287, 299])
S15.add('Đang tạo chỉ người tạo thấy', 'P0', [ACC_T, PH1], ['Đăng nhập T.', MENU, 'Tìm số phiếu PH1.'], '—', ['T không thấy PH1.'], [287, 299])
S15.add('Xem chi tiết theo phạm vi', 'P0', [ACC_C, 'Phiếu TPSG-KKVT-00130 công ty TPSG.'], ['Đăng nhập C.', 'Mở đường link chi tiết phiếu đó.'], '—',
       ['Trang "Không tìm thấy trang".'], [288, 296])
S15.add('Ban kiểm soát / người xử lý mở phiếu đang chờ mình', 'P0', [ACC_K, ACC_X, PH3, PH4], ['K mở chi tiết PH3.', 'X mở chi tiết PH4.'], '—',
       ['Cả 2 mở được dù không có quyền xem theo cấp; sau khi phiếu đổi trạng thái thì mở lại ra "Không tìm thấy trang".'], 288)
S15.add('Thêm mới cần quyền Lập phiếu', 'P0', [ACC_A, ACC_B], ['Đăng nhập A, mở danh sách.', 'Đăng nhập B, mở danh sách.'], '—',
       ['A có nút Tạo mới; B không có.'], [289, 295])
S15.add('Sửa / Nhập kết quả chỉ người tạo', 'P0', [ACC_T, PH2, 'PH5 Đang tạo do T tạo.'], ['Đăng nhập T.', MENU], '—',
       ['PH5 có Sửa; PH2 (A tạo) không có Nhập kết quả dù T thấy được.'], [290, 295])
S15.add('Xóa chỉ người tạo', 'P0', [ACC_T, 'PH5 Đang tạo do T tạo.'], ['Đăng nhập T.', MENU], '—', ['Chỉ PH5 có nút Xóa.'], [291, 295])
S15.add('Duyệt / Không duyệt cần quyền Ban kiểm soát', 'P0', [ACC_T, PH3], ['Đăng nhập T, mở chi tiết PH3.'], '—',
       ['T (chỉ có quyền xem) không có Duyệt kết quả, Không duyệt.'], 295)
S15.add('Xử lý cần quyền Xử lý', 'P0', [ACC_K, PH4], ['Đăng nhập K (có quyền xem tổng công ty thêm), mở chi tiết PH4.'], '—',
       ['Không có Tạo phiếu điều chuyển vị trí, Hoàn thành; ô Tổng kiểm kê khóa.'], 295)
S15.add('Xuất / In / Lịch sử theo phạm vi', 'P1', ACC_A, ['Đăng nhập A.', MENU, 'Xuất Excel; mở Lịch sử 1 phiếu của A.'], '—',
       ['File chỉ chứa phiếu của A; lịch sử xem được.'], [293, 294])
S15.add('Mở đường link màn Sửa khi không phải người tạo', 'P0', [ACC_C, 'Phiếu PH6 Đang kiểm công ty TPE do A tạo.'],
       ['Đăng nhập C.', 'Mở đường link màn Sửa của PH6.'], '—', ['Tự chuyển sang màn chi tiết PH6, không sửa được.'], 296)
S15.add('Thao tác bị chặn lại ở máy chủ', 'P1', [ACC_A, PH1], ['Tab 1 mở danh sách.', 'Tab 2 gửi PH1.', 'Tab 1 bấm Xóa PH1, xác nhận.'], '—',
       ['Báo "%s"; máy chủ kiểm lại điều kiện từng thao tác, không dựa vào việc ẩn nút.' % CONFLICT], 297)
S15.add('Đổi quyền giữa thao tác', 'P1', [ACC_K, PH3, 'Quản trị gỡ quyền "%s" của K khi K đang mở chi tiết PH3.' % Q2],
       ['K bấm Duyệt kết quả, xác nhận.'], '—', ['Báo "%s" (hoặc không tìm thấy phiếu nếu K hết phạm vi xem), PH3 không đổi.' % NOPERM], 298)
S15.add('Super admin có đủ quyền', 'P2', 'Tài khoản DNS Admin (Super admin), không gán quyền riêng.', ['Đăng nhập DNS Admin.', MENU], '—',
       ['Thấy 52 phiếu mọi công ty, có nút Tạo mới, ô Công ty – Phòng ban.',
        'Popup Chọn kế hoạch vẫn chỉ hiện kế hoạch của kho DNS Admin làm thủ kho (Super admin không được miễn).'], 287)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'CHỈNH SỬA', S4),
    ('V', 'XÓA', S5),
    ('VI', 'GỬI DUYỆT', S6),
    ('VII', 'DUYỆT PHIẾU', S7),
    ('VIII', 'KHÔNG DUYỆT PHIẾU', S8),
    ('IX', 'LỊCH SỬ THAY ĐỔI', S9),
    ('X', 'XEM CHI TIẾT PHIẾU KIỂM KÊ', S10),
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
    build_chuan(output_file=OUT, sheet_name='Trang tính1', feature_name='Kiểm kê theo vị trí - Cập nhật ngày 06/11/2026',
                module_name='Kiểm kê theo vị trí', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

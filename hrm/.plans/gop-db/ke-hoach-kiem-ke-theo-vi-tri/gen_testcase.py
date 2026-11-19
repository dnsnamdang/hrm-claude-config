# -*- coding: utf-8 -*-
"""Testcase màn "Kế hoạch kiểm kê theo vị trí" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (không phải danh mục): màn là chứng từ có vòng đời trạng thái Đang tạo > Đang kiểm > Đã lập kiểm kê > Hoàn thành,
có Thêm / Sửa / Xóa theo trạng thái + người tạo, Lưu và gửi (gửi thủ kho), In phiếu, Xuất Excel 1 phiếu, lịch sử.
Nhóm theo đúng tên + thứ tự chuẩn loại 'phieu' (check_tc.THU_TU), bỏ nhóm màn không có (kiểm code 05/11/2026: không có route / nút
Khóa, Duyệt, Không duyệt, Hủy, Import):
I Hiển thị · II Tìm kiếm & lọc (gồm Cài đặt bộ lọc) · III Thêm mới (Lưu, Lưu và tiếp tục, phạm vi + Lấy vị trí, rời màn) ·
IV Chỉnh sửa · V Xóa · VI Gửi duyệt (Lưu và gửi > Đang kiểm, thông báo thủ kho) · VII Lịch sử · VIII Xem chi tiết (gồm Lập phiếu
kiểm kê) · IX In phiếu (kèm In danh sách) · X Tùy chỉnh cột · XI Xuất danh sách Excel (kèm Xuất 1 phiếu) · XII Ràng buộc · XIII Phân quyền.
Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../borrow-export/gen_testcase.py (05/11, qua check_tc 0 lỗi).
Nguồn hành vi (đọc 05/11/2026, nhánh develop): FE pages/finance/position-inventories/**; BE Modules/Finance PositionInventory*
(Entity / Service / WriteService / Controller / StoreRequest / PrintService / Export), WarehouseInventoryLockService,
PositionInventoryResultWriteService, PositionTransferWriteService.
Số liệu mẫu: dev-hrm 05/11/2026 (DNS Admin) 20 kế hoạch (6 Đã lập kiểm kê, 14 Hoàn thành), TPE-KHKKVT-00137 có 5 mốc lịch sử.
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
MENU = 'Vào phân hệ Tài chính > menu "Kiểm kê" > bấm "Kế hoạch kiểm kê theo vị trí".'
TAO = [MENU, 'Bấm "Tạo mới".']
ADV = 'Bấm Tìm kiếm nâng cao.'

ACC_A = 'Tài khoản A: nhân viên công ty TPE, không có quyền xem theo cấp; là người lập kế hoạch.'
ACC_B = 'Tài khoản B: nhân viên công ty TPE, không có quyền xem theo cấp, không phải người tạo.'
ACC_C = 'Tài khoản C: có quyền "Xem kế hoạch kiểm kê theo vị trí theo công ty", thuộc công ty TPE.'
ACC_T = 'Tài khoản T: có quyền "Xem kế hoạch kiểm kê theo vị trí theo tổng công ty".'
ACC_TK = ('Tài khoản TK: thủ kho của kho Phan Trọng Tuệ, công ty TPE, có quyền "Lập phiếu kiểm kê kho theo vị trí", không có '
          'quyền xem theo cấp.')
PRE_LIST = 'Tài khoản DNS Admin (Super admin); trong phạm vi xem có 20 kế hoạch: 6 Đã lập kiểm kê, 14 Hoàn thành.'
P137 = ('Kế hoạch TPE-KHKKVT-00137: kho Phan Trọng Tuệ, trạng thái Hoàn thành, Người tạo DNS Admin, Ngày kiểm kê 23/10/2026 '
        '11:19, Ngày cập nhật 26/10/2026 10:26; có 5 mốc lịch sử.')
KHO = ('Kho Phan Trọng Tuệ (mã PTT): Nhà N1 - Nhà 1 > Dãy D1 - Dãy 1 > Khoang K1 - Khoang 1; vị trí tự do N1-T2-KV có hàng '
       '"Quạt ENEOS" (Cái., SL tồn 1,227, công ty TPE, 4 lô, lô TONDAUKHO-9113-11191-41 SL 670).')
PRE_FORM = ACC_A + '\n' + KHO
KH1 = 'Kế hoạch KH1 trạng thái Đang tạo do A tạo: kho Phan Trọng Tuệ, vị trí N1-T2-KV, hội đồng 1 người (Bùi Duy Trước).'
KH2 = 'Kế hoạch KH2 trạng thái Đang kiểm do A tạo ở kho Phan Trọng Tuệ.'
FILL = TAO + ['Chọn Kho vật lý = PTT - Phan Trọng Tuệ.', 'Ở cột Vị trí tick N1-T2-KV (nhóm Vị trí tự do).', 'Bấm Lấy vị trí.',
              'Ở dòng 1 Hội đồng chọn Nhân viên = Bùi Duy Trước.']
FULL = ['Kho vật lý: PTT - Phan Trọng Tuệ', 'Vị trí: N1-T2-KV', 'Nhân viên: Bùi Duy Trước']
OK_LIST = 'Báo "Lưu thành công.", về màn danh sách; dòng mới ở trên cùng, trạng thái Đang tạo (nhãn xám).'

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
     'Lập kế hoạch kiểm kê cho một kho vật lý: chọn phạm vi Nhà / Dãy / Khoang / Vị trí, chụp hàng tồn từng lô tại các vị trí đó '
     '(Lấy vị trí), chỉ định Hội đồng kiểm kê, rồi gửi cho thủ kho lập phiếu kiểm kê. Kế hoạch KHÔNG làm đổi tồn kho.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Danh sách: kế hoạch trong phạm vi xem; trạng thái Đang tạo (xám), Đang kiểm (vàng), Đã lập kiểm kê (xanh dương), '
     'Hoàn thành (xanh lá).\n- Bảng Chi tiết: hàng có tồn > 0 và lô tồn > 0 tại vị trí đã tick, gom theo công ty.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Kế hoạch Đang tạo của người khác (kể cả với quyền tổng công ty).\n- Kế hoạch ngoài phạm vi quyền xem.\n'
     '- Nhà / dãy / khoang / vị trí đã khóa ở danh mục kho (không hiện để tick mới).\n- Phiếu kiểm kê theo vị trí (màn khác).'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày kiểm kê lọc theo ngày lập kế hoạch, lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Kế hoạch > vị trí > hàng (SL tồn) > công ty (Cộng) > lô (SL).\n- Phạm vi: Nhà > Dãy > Khoang > Vị trí; vị trí tự do không '
     'thuộc khoang.\n- Hội đồng: danh sách nhân viên + chức vụ.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Cộng (theo công ty) = tổng SL các lô của công ty đó; SL tồn = tồn của hàng tại vị trí.\n'
     '- Hội đồng không được trùng nhân viên.'),
    ('7. Phân quyền cấp',
     '- Xem kế hoạch kiểm kê theo vị trí theo tổng công ty: xem mọi kế hoạch.\n'
     '- Xem kế hoạch kiểm kê theo vị trí theo công ty: kế hoạch công ty mình + của mình.\n'
     '- Không quyền: chỉ kế hoạch mình tạo. Tạo / Sửa / Xóa không cần quyền (Sửa / Xóa chỉ người tạo, Đang tạo).\n'
     '- Lập phiếu kiểm kê kho theo vị trí: nút Lập phiếu kiểm kê (thủ kho) + nhận thông báo.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là khoảng thứ tự dòng của trang, N là tổng kế hoạch khớp bộ lọc trong phạm vi xem.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: A (người lập, không quyền xem theo cấp), B (nhân viên khác), C (quyền theo công ty), T (quyền '
     'tổng công ty), TK (thủ kho kho Phan Trọng Tuệ), DNS Admin (Super admin).\n'
     '- Lưu ý: Lưu và gửi gửi NGAY, không có hộp xác nhận; kế hoạch đã gửi không sửa / xóa được — chạy trên dữ liệu thử.\n'
     '- Lưu ý: số tồn trên kế hoạch là ảnh chụp lúc bấm Lấy vị trí, không tự cập nhật.\n'
     '- Màn Tạo / Sửa / Chi tiết là TRANG riêng, không phải cửa sổ nổi.'),
]

SCREEN = ListScreen(menu=MENU, title='Danh sách kế hoạch kiểm kê theo vị trí', total=20, quick_label='số phiếu',
                    quick_sample='00137', quick_hit='kế hoạch TPE-KHKKVT-00137',
                    filters=[('Trạng thái', 'Hoàn thành'), ('Kho', 'PTT - Phan Trọng Tuệ')], unit='kế hoạch')

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Cả 3 nơi đều là "Danh sách kế hoạch kiểm kê theo vị trí".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE_LIST, [MENU, 'Quan sát khối bộ lọc và thanh công cụ.'], '—',
       ['Khối bộ lọc: ô tìm nhanh (gợi ý "Tìm theo số phiếu"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
        'Thanh công cụ: Tạo mới, Xuất Excel, In danh sách, nút biểu tượng cột.',
        'Dòng Hoàn thành / Đã lập kiểm kê: cột Hành động có In, Xuất Excel, Lịch sử; không có Sửa, Xóa.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 10 cột: STT, Số phiếu, Ngày kiểm kê, Kho, Trạng thái, Người tạo, Ngày tạo, Ngày cập nhật, Người cập nhật, Hành động.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 10/10 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp kế hoạch đã tạo', 'P0', [PRE_LIST, P137], [MENU, 'Tìm "TPE-KHKKVT-00137", đối chiếu dòng.'], '—',
       ['Ngày kiểm kê "23/10/2026 11:19", Kho "Phan Trọng Tuệ", Người tạo "DNS Admin", Ngày tạo "23/10/2026 11:19", Ngày cập nhật '
        '"26/10/2026 10:26", Người cập nhật "DNS Admin".'], [6, 58])
S1.add('Trạng thái bản ghi', 'P0', PRE_LIST, [MENU, ADV, 'Mở ô Trạng thái.', 'Quan sát cột Trạng thái.'], '—',
       ['Ô có 4 lựa chọn: Đang tạo, Đang kiểm, Đã lập kiểm kê, Hoàn thành.',
        'Nhãn: Đã lập kiểm kê xanh dương, Hoàn thành xanh lá; Đang tạo xám, Đang kiểm vàng.'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', [ACC_B, 'B chưa tạo kế hoạch nào.'], ['Đăng nhập B.', MENU], '—',
       ['Bảng hiện "Không có dữ liệu phù hợp.", dòng tổng "Hiển thị 0–0 / 0" hoặc trống; không báo lỗi.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       ['Bảng hiện "Không có dữ liệu phù hợp.".'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 20 kế hoạch, tự về trang 1, "Hiển thị 1–20 / 20".', 'Chỉ nạp lại 1 lần (không nháy 2 lần).'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–20 / 20".', 'Bước 3: "Hiển thị 1–10 / 20".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—', ['Bước 2: trang 2.', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang 2 quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.'], '—', ['Trang 2 đánh số 11–20.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', ADV, 'Chọn Trạng thái = Hoàn thành.'],
       'Trạng thái: Hoàn thành', ['Tự nạp lại ở trang 1; "Hiển thị 1–10 / 14".'], 17)
S1.add('Sắp xếp tăng dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Số phiếu.'], '—',
       ['Xếp theo số phiếu tăng dần, mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Số phiếu 2 lần.'], '—',
       ['Xếp theo số phiếu giảm dần, mũi tên xuống.'], 21)
S1.add('Sắp xếp theo Ngày kiểm kê và Người tạo', 'P1', PRE_LIST,
       [MENU, 'Bấm tiêu đề Ngày kiểm kê (2 lần).', 'Bấm tiêu đề Người tạo.'], '—',
       ['Ngày kiểm kê: lần 1 cũ nhất trên, lần 2 mới nhất trên.', 'Người tạo: xếp theo họ tên A > Z.',
        'Khi mới vào chưa chọn cột nào: tạo mới nhất trên, các cột hiện biểu tượng sắp xếp trung tính.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Kho, Trạng thái, Ngày tạo, Ngày cập nhật, Người cập nhật.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Số phiếu (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự tăng của trang 1.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 2.', 'Bấm tiêu đề Ngày kiểm kê.'], '—', ['Về trang 1.'], 25)
S1.add('Nút thao tác theo trạng thái', 'P0', [ACC_A, KH1, KH2], ['Đăng nhập A.', MENU, 'Quan sát cột Hành động 2 dòng KH1, KH2.'], '—',
       ['KH1 (Đang tạo): Sửa, Xóa và nút ba chấm "Hành động khác" chứa In, Xuất Excel, Lịch sử.',
        'KH2 (Đang kiểm, A không phải thủ kho): In, Xuất Excel, Lịch sử; không có Sửa, Xóa, Lập phiếu kiểm kê.'], [3, 34])
S1.add('Mở màn từ thông báo của thủ kho', 'P1', [ACC_TK, KH2, 'TK đã nhận thông báo "[KHKKVT] Tạo mới: <số phiếu KH2>".'],
       ['Đăng nhập TK.', 'Bấm chuông thông báo, bấm thông báo của KH2.'], '—',
       ['Mở màn chi tiết KH2 (TK không có quyền xem theo cấp vẫn mở được).', 'Có nút Lập phiếu kiểm kê.'], 1)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo số phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "TPE-KHKKVT-00137", bấm Tìm kiếm.'], 'Ô tìm nhanh: TPE-KHKKVT-00137',
       ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần số phiếu', 'P0', PRE_LIST, [MENU, 'Nhập "TPSG", bấm Tìm kiếm.'], 'Ô tìm nhanh: TPSG',
       ['Chỉ còn các kế hoạch có số phiếu chứa "TPSG" (TPSG-KHKKVT-00131, 00126, …).'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "tpe-khkkvt-00137", bấm Tìm kiếm.'], '—',
       ['Ra TPE-KHKKVT-00137 như khi gõ chữ hoa.'], 28)
S2.add('Có dấu / không dấu ở ô Hàng hóa', 'P2', PRE_LIST, [MENU, ADV, 'Nhập Hàng hóa "quat eneos", bấm Tìm kiếm.'], '—',
       ['Ra các kế hoạch có hàng "Quạt ENEOS" nếu cơ sở dữ liệu so khớp không dấu.',
        'Lưu ý: so khớp theo cách so sánh chữ của cơ sở dữ liệu.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; ký tự % được hiểu là ký tự đại diện nên ra toàn bộ.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  TPE-KHKKVT-00137  ", bấm Tìm kiếm.'], '—',
       ['Ra TPE-KHKKVT-00137 (bỏ khoảng trắng đầu / cuối).'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "TPE-KHKKVT-00137", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Sau bước 2 hiện lại đủ 20 kế hoạch.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST,
       [MENU, 'Nhập "00137", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'], '—',
       ['Cả 2 cách đều ra TPE-KHKKVT-00137, về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['Các ô Trạng thái, Người tạo, Hàng hóa, Ngày kiểm kê, Kho, Nhà, Dãy, Khoang, Vị trí, Công ty, Phòng ban đều trống.',
        'Đủ 20 kế hoạch.'], 36)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đã lập kiểm kê.'], '—',
       ['Lọc ngay; còn 6 kế hoạch, tất cả nhãn xanh dương.'], 37)
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = Trần Thị Phương.'], '—',
       ['Chỉ còn kế hoạch do Trần Thị Phương tạo (TPSG-KHKKVT-00046, 00045, …).',
        'Ô Người tạo liệt kê toàn bộ nhân viên, kể cả người chưa tạo kế hoạch nào.'], 37)
S2.add('Lọc Hàng hóa theo mã hoặc tên', 'P0', PRE_LIST, [MENU, ADV, 'Nhập Hàng hóa "ENEO-QUATCAY", bấm Tìm kiếm.',
                                                         'Đổi thành "Quạt ENEOS", bấm Tìm kiếm.'], '—',
       ['Cả 2 lần đều ra các kế hoạch có hàng Quạt ENEOS (có TPE-KHKKVT-00145).'], 37)
S2.add('Lọc Ngày kiểm kê lấy trọn ngày biên', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày kiểm kê 23/10/2026 – 23/10/2026.'], '—',
       ['Ra 3 kế hoạch TPE-KHKKVT-00137, 00135, 00133 (tạo 11:17 – 11:19 ngày 23/10/2026).',
        'Bỏ trống ngày cuối vẫn lọc được từ ngày đầu.'], 37)
S2.add('Lọc Kho', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = PTT - Phan Trọng Tuệ.'], '—',
       ['Còn TPE-KHKKVT-00145 và 00137.', 'Ô Nhà nạp các nhà của kho PTT (N1 - Nhà 1, test1 - Nhà 11).'], 37)
S2.add('Chuỗi Kho > Nhà > Dãy > Khoang > Vị trí', 'P0', PRE_LIST,
       [MENU, ADV, 'Chọn Kho = PTT - Phan Trọng Tuệ.', 'Chọn Nhà = N1 - Nhà 1.', 'Chọn Dãy = D1 - Dãy 1.', 'Chọn Khoang = K1 - Khoang 1.'],
       '—', ['Mỗi ô con chỉ còn mục thuộc ô cha đã chọn.', 'Mỗi lần chọn danh sách lọc lại theo kế hoạch có tick mục đó trong phạm vi.'],
       [37, 38])
S2.add('Đổi cấp cha xóa cấp con', 'P0', 'Đang lọc Kho PTT, Nhà N1, Dãy D1, Khoang K1.', [ADV, 'Đổi Kho = HP - Hải Phòng.'], '—',
       ['Ô Nhà, Dãy, Khoang, Vị trí bị xóa trắng, ô Nhà nạp nhà của kho Hải Phòng.', 'Danh sách nạp lại 1 lần.'], [37, 283])
S2.add('Lọc Vị trí tự do', 'P1', PRE_LIST, [MENU, ADV, 'Chọn Kho = PTT.', 'Chọn Vị trí = N1-T2-KV (không chọn Nhà / Dãy / Khoang).'],
       '—', ['Ô Vị trí có cả vị trí tự do khi chưa chọn cấp cha.', 'Ra TPE-KHKKVT-00145.'], 37)
S2.raw(org_cases(SCREEN, len(S2) + 1), [[37], [37, 283], [37]])
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Hoàn thành.', 'Chọn Kho = PTT.'], '—',
       ['Chỉ còn TPE-KHKKVT-00137.'], 38)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST, [MENU, 'Nhập "TPSG", bấm Tìm kiếm.', ADV, 'Chọn Kho = PTT.'], '—',
       ['"Không có dữ liệu phù hợp." vì kế hoạch TPSG thuộc Kho Sài Gòn.'], [39, 40])
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Hoàn thành.', 'Bấm trang 2.'], '—',
       ['"Hiển thị 1–10 / 14" rồi "Hiển thị 11–14 / 14"; STT liên tục.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Trạng thái = Hoàn thành.', ['Bấm tiêu đề Số phiếu.'], '—',
       ['Chỉ 14 kế hoạch đang lọc được sắp; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "TPE", lọc Kho PTT, Nhà N1, sắp Số phiếu, ở trang 2.', ['Bấm Làm mới.'],
       '—', ['Mọi ô kể cả ô tìm nhanh, Kho, Nhà về trống, bỏ sắp xếp, nạp lại trang 1, đủ 20 kế hoạch.'], 44)
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Hoàn thành, chưa mở màn con.'], ['Nhấn F5.'], '—',
       ['Bộ lọc trở về trống, đủ 20 kế hoạch (chỉ nhớ khi đi vào màn con của màn này).'], 46)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Hàng hóa, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô Hàng hóa.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Hoàn thành.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Trạng thái, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị bỏ, nạp lại đủ 20 kế hoạch.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Hàng hóa.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Hàng hóa vẫn ẩn.', 'Bước 2: tích đủ 10 mục, Hàng hóa hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Kho lên đầu, bấm Lưu.'], '—',
       ['Ô Kho đứng đầu khối Tìm kiếm nâng cao; cấu hình giữ sau khi đăng nhập lại.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo', 'P0', PRE_FORM, TAO, '—', ['Mở TRANG "Tạo kế hoạch kiểm kê theo vị trí", tab cùng tiêu đề.'], 49)
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải "<tên A> - <ngày giờ hiện tại>".', 'Không có ô Số phiếu (tự sinh khi lưu).'], 50)
S3.add('Các trường, khối và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Ngày kiểm kê *, Kho vật lý * (gợi ý "Chọn kho vật lý").',
        'Phạm vi kiểm kê: 4 cột Nhà, Dãy, Khoang, Vị trí, nút Lấy vị trí ở góc phải.',
        'Chi tiết * (bảng "Không có dữ liệu"); Hội đồng kiểm kê * có 1 dòng trống và nút Thêm dòng.',
        'Chân màn: Lưu, Lưu và gửi, Lưu và tiếp tục, Quay lại.'], [51, 54])
S3.add('Trường bắt buộc / không bắt buộc', 'P0', PRE_FORM, TAO + ['Quan sát dấu *.'], '—',
       ['Dấu * ở Ngày kiểm kê, Kho vật lý, Nhà, Dãy, Khoang, Vị trí, Chi tiết, Hội đồng kiểm kê, Nhân viên, Chức vụ.',
        'Lưu ý: thực tế chỉ bắt buộc ít nhất 1 Vị trí; Nhà / Dãy / Khoang không tick vẫn lưu được (vị trí tự do).'], 52)
S3.add('Giá trị mặc định', 'P0', PRE_FORM, TAO, '—',
       ['Ngày kiểm kê = ngày hôm nay, ô khóa.', 'Kho vật lý trống; 4 cột phạm vi ghi "Chưa chọn kho vật lý".',
        'Hội đồng có 1 dòng trống.'], 53)
S3.add('Lưu với dữ liệu hợp lệ đầy đủ', 'P0', PRE_FORM, FILL + ['Bấm Lưu.'], FULL,
       [OK_LIST, 'Số phiếu dạng "TPE-KHKKVT-<số>" theo công ty của A.'], [55, 58, 59, 79])
S3.add('Lưu chỉ với trường bắt buộc tối thiểu', 'P0', PRE_FORM, FILL + ['Không tick Nhà / Dãy / Khoang.', 'Bấm Lưu.'], FULL,
       [OK_LIST, 'Chi tiết kế hoạch: cột Nhà, Dãy, Khoang không tick mục nào; Vị trí N1-T2-KV được tick.'], [56, 57])
S3.add('Dữ liệu sau lưu', 'P0', [PRE_FORM, 'A vừa lưu kế hoạch ở TC_03.006.'], ['Bấm số phiếu vừa tạo.'], '—',
       ['Chi tiết: Kho PTT - Phan Trọng Tuệ, vị trí N1-T2-KV được tick, bảng Chi tiết có Quạt ENEOS SL tồn 1,227, 4 lô, Cộng 1,227.',
        'Hội đồng: Bùi Duy Trước, chức vụ tự điền.'], 58)
S3.add('Trạng thái mặc định sau Lưu', 'P0', [PRE_FORM, 'A vừa lưu kế hoạch.'], [MENU, 'Đăng nhập DNS Admin, mở danh sách.'], '—',
       ['A thấy kế hoạch Đang tạo (nhãn xám).', 'DNS Admin KHÔNG thấy kế hoạch này (Đang tạo chỉ người tạo thấy).'], [59, 84])
S3.add('Lịch sử tạo', 'P1', [PRE_FORM, 'A vừa lưu kế hoạch.'], ['Ở dòng kế hoạch bấm ba chấm > Lịch sử.'], '—',
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
S3.add('Xóa hết dòng hội đồng', 'P1', PRE_FORM, FILL + ['Bấm biểu tượng thùng rác ở dòng hội đồng.', 'Bấm Lưu.'], '—',
       ['Bảng hội đồng hiện "Không có dữ liệu", báo "Hội đồng kiểm kê – Vui lòng thêm ít nhất 1 thành viên.".'], 61)
S3.add('Chọn nhân viên tự điền chức vụ', 'P1', PRE_FORM, TAO + ['Chọn Nhân viên = Bùi Duy Trước.', 'Bỏ chọn nhân viên.'], '—',
       ['Bước 1: ô Chức vụ tự điền chức vụ đầu tiên của nhân viên.', 'Bước 2: ô Chức vụ bị xóa.'], 53)
S3.add('Trường không có ký tự / độ dài nhập tay', 'P2', PRE_FORM, TAO + ['Quan sát các ô nhập.'], '—',
       ['Form chỉ có ô chọn, ô tick và ô tìm; không có ô văn bản tự do cần kiểm độ dài, ký tự đặc biệt, khoảng trắng.',
        'Ô tìm của cột phạm vi gõ "  N1  " vẫn tìm ra N1 - Nhà 1.'], [63, 64, 65, 66, 68, 69, 81])
S3.add('Lỗi biến mất sau khi sửa', 'P1', 'Đang có lỗi đỏ ở TC_03.011.', ['Chọn Kho PTT.', 'Tick N1-T2-KV.', 'Bấm Lấy vị trí.'], '—',
       ['Lỗi Kho, Phạm vi, Chi tiết lần lượt biến mất ngay khi sửa đúng.'], 71)
S3.add('Trùng dữ liệu: 2 kế hoạch cùng kho, cùng phạm vi', 'P1', [PRE_FORM, KH1],
       FILL + ['Bấm Lưu.'], FULL, ['Lưu được; 2 kế hoạch có số phiếu khác nhau (không có trường duy nhất).'], [67, 75, 82])
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, FILL + ['Bấm Lưu và tiếp tục.'], FULL,
       ['Báo "Lưu thành công.", VẪN ở màn Tạo.', 'Form trắng: Kho trống, phạm vi trống, Chi tiết trống, Hội đồng 1 dòng trống.',
        'Kế hoạch vừa lưu ở trạng thái Đang tạo.'], [72, 76, 77, 83])
S3.add('Lưu và tiếp tục khi thiếu bắt buộc', 'P0', PRE_FORM, TAO + ['Bấm Lưu và tiếp tục.'], '—',
       ['Báo lỗi như Lưu, không lưu, form giữ dữ liệu đã nhập.'], [73, 74])
S3.add('Rời màn sau Lưu và tiếp tục', 'P1', 'Vừa Lưu và tiếp tục, form trắng.', ['Bấm Quay lại.'], '—',
       ['Về danh sách ngay, không hỏi; kế hoạch vừa lưu có trong danh sách.'], [78, 85])
S3.add('Lưu: màn chuyển về danh sách', 'P1', PRE_FORM, FILL + ['Bấm Lưu.'], FULL,
       ['Màn Tạo đóng, về danh sách (màn là trang, không phải cửa sổ còn mở).'], [76, 85])
S3.add('Quay lại khi chưa nhập', 'P1', PRE_FORM, TAO + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 93)
S3.add('Quay lại khi đã nhập', 'P0', PRE_FORM, FILL + ['Bấm Quay lại.'], '—',
       ['Hiện hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" với nút Thoát, Ở lại.'], 94)
S3.add('Rời màn bằng menu / (x) của hộp', 'P1', PRE_FORM, FILL + ['Bấm menu sang màn khác.', 'Ở hộp "Thông tin chưa lưu" bấm (x).'],
       '—', ['Hộp hiện khi bấm menu; bấm (x) đóng hộp, ở lại màn Tạo, dữ liệu giữ nguyên (màn là trang, không có nút X riêng).'], 95)
S3.add('Chọn Thoát', 'P0', 'Đang ở hộp "Thông tin chưa lưu".', ['Bấm Thoát.'], '—', ['Về danh sách, không lưu kế hoạch nào.'], 96)
S3.add('Chọn Ở lại', 'P1', 'Đang ở hộp "Thông tin chưa lưu".', ['Bấm Ở lại.'], '—', ['Đóng hộp, dữ liệu đã nhập giữ nguyên.'], 97)
S3.add('Nhập rồi trả về như ban đầu', 'P2', PRE_FORM, TAO + ['Chọn Kho PTT.', 'Bấm × trong ô Kho để bỏ chọn.', 'Bấm Quay lại.'],
       '—', ['Không hỏi "Thông tin chưa lưu" (dữ liệu như lúc mở).'], [98, 99])
S3.add('Không thao tác lâu', 'P2', PRE_FORM, FILL + ['Để yên 30 phút.', 'Bấm Lưu.'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên, chuyển về đăng nhập, không lưu.'], 100)
S3.add('Bấm Lưu liên tục', 'P0', PRE_FORM, FILL + ['Bấm Lưu 3 lần thật nhanh.'], FULL,
       ['Chỉ tạo 1 kế hoạch (nút khóa trong lúc lưu).'], 101)
S3.add('Tạo đồng thời ở 2 tab', 'P1', PRE_FORM, ['Mở 2 tab màn Tạo, nhập cùng dữ liệu.', 'Bấm Lưu ở cả 2 tab.'], FULL,
       ['Tạo 2 kế hoạch, số phiếu khác nhau, không lỗi.'], 102)
S3.add('Lấy vị trí khi chưa chọn kho', 'P0', PRE_FORM, TAO + ['Bấm Lấy vị trí.'], '—',
       ['Báo "Bạn chưa nhập đầy đủ thông tin.", lỗi đỏ dưới ô Kho vật lý; không gửi yêu cầu.'], [61, 62])
S3.add('Lấy vị trí khi chưa tick vị trí', 'P0', PRE_FORM, TAO + ['Chọn Kho PTT.', 'Tick Nhà N1, không tick vị trí.', 'Bấm Lấy vị trí.'],
       '—', ['Báo "Chưa chọn đủ thông tin vị trí!", khung cột Vị trí viền đỏ.'], 61)
S3.add('Lấy vị trí ra đúng hàng tồn', 'P0', PRE_FORM, TAO + ['Chọn Kho PTT.', 'Tick N1-T2-KV.', 'Bấm Lấy vị trí.'], '—',
       ['Bảng Chi tiết: STT 1, Vị trí N1-T2-KV, các hàng có tồn > 0 (có Quạt ENEOS, Model QUATCAY, Mã ENEO-QUATCAY:01, Thương hiệu '
        'ENEOS, ĐVT Cái., SL tồn 1,227).', 'Công ty TPE, 4 lô (TONDAUKHO-9113-11191-41 SL 670, …), Cộng 1,227.',
        'Ô gộp theo vị trí > hàng > công ty; tiêu đề 2 tầng.'], [58, 269])
S3.add('Lấy vị trí ở vị trí không có tồn', 'P1', [PRE_FORM, 'Vị trí PTT-N1-KV7-01 không có hàng tồn.'],
       TAO + ['Chọn Kho PTT.', 'Tick PTT-N1-KV7-01.', 'Bấm Lấy vị trí.'], '—',
       ['Báo "Các vị trí đã chọn không có hàng tồn.", bảng Chi tiết giữ nguyên.'], [268, 61])
S3.add('Phạm vi: chọn cấp cha mới hiện cấp con', 'P0', PRE_FORM, TAO + ['Chọn Kho PTT.', 'Tick N1 - Nhà 1.', 'Tick D1 - Dãy 1.'],
       '—', ['Trước khi tick: cột Dãy ghi "Chưa chọn nhà hoặc không có dữ liệu".',
             'Sau tick Nhà: cột Dãy hiện nhóm "N1 - Nhà 1" với các dãy; sau tick Dãy: cột Khoang hiện nhóm "N1 | D1".',
             'Nhóm "Vị trí tự do" luôn hiện ở cột Vị trí.'], [53, 283])
S3.add('Phạm vi: bỏ tick cấp cha tự bỏ cấp con', 'P0', 'Đã tick N1, D1, K1 và 1 vị trí trong K1, 1 vị trí tự do.',
       ['Bỏ tick N1 - Nhà 1.'], '—', ['D1, K1 và vị trí thuộc K1 tự bỏ tick; vị trí tự do vẫn được tick.'], [283, 285])
S3.add('Phạm vi: ô tìm và Chọn hết', 'P1', PRE_FORM, TAO + ['Chọn Kho PTT, tick N1.', 'Gõ "D1" vào ô tìm cột Dãy.',
                                                       'Tick "Chọn hết" của cột Dãy.', 'Bấm × trong ô tìm.'], '—',
       ['Cột Dãy chỉ còn dãy có mã / tên chứa "D1" (D1, D10–D17).', 'Chọn hết chỉ tick các dãy đang hiện.', '× xóa ô tìm, hiện lại đủ.'],
       53)
S3.add('Phạm vi: Chọn hết của từng nhóm', 'P2', PRE_FORM, TAO + ['Chọn Kho PTT, tick N1 và test1.', 'Tick "Chọn hết" ở nhóm N1 - Nhà 1 (cột Dãy).'],
       '—', ['Chỉ các dãy của Nhà 1 được tick; dãy của Nhà 11 không đổi.'], 53)
S3.add('Đổi kho khi đã có Chi tiết: Hủy', 'P0', 'Đang ở màn Tạo, đã Lấy vị trí ở kho PTT.', ['Đổi Kho vật lý = HP - Hải Phòng.', 'Bấm Hủy.'],
       '—', ['Hiện hộp "Đổi kho vật lý": "Đổi kho vật lý sẽ xóa phạm vi kiểm kê và danh sách vị trí đã lấy. Bạn có muốn tiếp tục?".',
             'Bấm Hủy: ô Kho trở lại PTT, phạm vi và Chi tiết giữ nguyên.'], 53)
S3.add('Đổi kho khi đã có Chi tiết: Đổi kho', 'P1', 'Đang ở màn Tạo, đã Lấy vị trí ở kho PTT.', ['Đổi Kho = HP - Hải Phòng.', 'Bấm Đổi kho.'],
       '—', ['Phạm vi và bảng Chi tiết bị xóa, 4 cột nạp cấu trúc kho Hải Phòng.'], [53, 283])
S3.add('Danh mục kho đã khóa không hiện để tick', 'P1', [PRE_FORM, 'Vị trí PTT-N1-KV9 đã bị khóa ở danh mục Vị trí.'],
       TAO + ['Chọn Kho PTT.', 'Tìm "KV9" ở cột Vị trí.'], '—', ['Không có PTT-N1-KV9 để tick.'], [276, 284])

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
PRE_E = [ACC_A, KH1]
EDIT = ['Đăng nhập A.', MENU, 'Ở dòng KH1 bấm Sửa (bút chì).']
S4.add('Mở màn Sửa', 'P0', PRE_E, EDIT, '—', ['Mở TRANG "Sửa kế hoạch kiểm kê theo vị trí: <số phiếu KH1>".'], 103)
S4.add('Dữ liệu điền đúng', 'P0', PRE_E, EDIT, '—',
       ['Số phiếu, Ngày kiểm kê (ngày tạo), Kho PTT (Phan Trọng Tuệ), vị trí N1-T2-KV đã tick, bảng Chi tiết như lúc lưu, hội đồng '
        'Bùi Duy Trước + chức vụ.'], 104)
S4.add('Trường được / không được sửa', 'P0', PRE_E, EDIT, '—',
       ['Không sửa được: Số phiếu, Ngày kiểm kê (ô khóa).', 'Sửa được: Kho vật lý, phạm vi, Lấy vị trí, hội đồng.'], 105)
S4.add('Các nút ở màn Sửa', 'P1', PRE_E, EDIT, '—', ['Có Lưu, Lưu và gửi, Quay lại; KHÔNG có Lưu và tiếp tục.'], 106)
S4.add('Sửa một trường', 'P0', PRE_E, EDIT + ['Đổi chức vụ của Bùi Duy Trước.', 'Bấm Lưu.'], 'Chức vụ: chức vụ khác',
       ['Báo "Lưu thành công.", về danh sách; trạng thái vẫn Đang tạo.'], [107, 69])
S4.add('Sửa nhiều trường', 'P0', PRE_E, EDIT + ['Tick thêm vị trí PTT-N1-KV1, bấm Lấy vị trí.', 'Thêm dòng hội đồng mới.', 'Bấm Lưu.'],
       '—', ['Lưu thành công; chi tiết có thêm hàng của PTT-N1-KV1 và 2 thành viên hội đồng.'], [108, 110])
S4.add('Giữ nguyên giá trị khi lưu không đổi', 'P1', PRE_E, EDIT + ['Không đổi gì, bấm Lưu.'], '—',
       ['Lưu thành công, không báo trùng chính kế hoạch.'], [109, 68])
S4.add('Ngày / người cập nhật', 'P1', PRE_E, EDIT + ['Đổi chức vụ, bấm Lưu.', 'Xem dòng KH1 ở danh sách.'], '—',
       ['Ngày cập nhật = thời điểm lưu, Người cập nhật = A.'], 111)
S4.add('Lịch sử sửa', 'P0', PRE_E, EDIT + ['Tick thêm vị trí, Lấy vị trí, bấm Lưu.', 'Mở Lịch sử của KH1.'], '—',
       ['Có mốc "Thay đổi thông tin", ghi Vị trí cũ > mới.', 'Không ghi từng lô hàng tồn.'], [112, 177, 178])
S4.add('Bỏ trống bắt buộc khi sửa', 'P0', PRE_E, EDIT + ['Bỏ chọn nhân viên hội đồng.', 'Bấm Lưu.'], '—',
       ['"Nhân viên – Vui lòng chọn nhân viên." dưới ô, "Bạn chưa nhập đầy đủ thông tin.", không lưu.'], [113, 117])
S4.add('Sai định dạng / vượt giới hạn khi sửa', 'P2', PRE_E, EDIT + ['Quan sát các ô.'], '—',
       ['Form không có ô nhập tự do: Kho, Nhân viên, Chức vụ là ô chọn; không có giới hạn ký tự cần kiểm.'], [114, 115])
S4.add('Trùng bản ghi khác khi sửa', 'P2', [ACC_A, KH1, 'Có kế hoạch khác cùng kho, cùng phạm vi.'], EDIT + ['Bấm Lưu.'], '—',
       ['Lưu được (kế hoạch không có trường duy nhất).'], 116)
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P1', 'Đang có lỗi "Nhân viên – Vui lòng chọn nhân viên.".', ['Chọn lại nhân viên.'], '—',
       ['Lỗi biến mất ngay.'], 118)
S4.add('Mở Sửa rồi Quay lại không đổi', 'P1', PRE_E, EDIT + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], [119, 125])
S4.add('Đổi rồi trả về ban đầu', 'P2', PRE_E, EDIT + ['Đổi chức vụ rồi chọn lại chức vụ cũ.', 'Bấm Quay lại.'], '—',
       ['Không hỏi "Thông tin chưa lưu".'], 120)
S4.add('Rời màn khi đã đổi', 'P0', PRE_E, EDIT + ['Đổi chức vụ.', 'Bấm Quay lại.'], '—', ['Hiện hộp "Thông tin chưa lưu".'], 121)
S4.add('Xác nhận Thoát', 'P1', 'Đang ở hộp "Thông tin chưa lưu" của màn Sửa.', ['Bấm Thoát.'], '—',
       ['Về danh sách; KH1 không đổi; lịch sử không có mốc mới.'], [122, 124, 125])
S4.add('Xác nhận Ở lại', 'P2', 'Đang ở hộp "Thông tin chưa lưu" của màn Sửa.', ['Bấm Ở lại.'], '—', ['Ở lại màn Sửa, dữ liệu đã đổi giữ nguyên.'], 123)
S4.add('Sửa kế hoạch đã gửi', 'P0', [ACC_A, KH2], ['Đăng nhập A.', MENU, 'Quan sát dòng KH2.', 'Mở đường link màn Sửa của KH2 từ lịch sử trình duyệt.'],
       '—', ['Dòng KH2 không có nút Sửa.', 'Mở màn Sửa tự chuyển sang màn chi tiết KH2.'], [126, 63])
S4.add('Kế hoạch bị xóa ở tab khác', 'P1', PRE_E, ['Tab 1 mở màn Sửa KH1.', 'Tab 2 xóa KH1.', 'Tab 1 bấm Lưu.'], '—',
       ['Báo "Không tìm thấy kế hoạch kiểm kê hoặc bạn không có quyền xem.", không lưu.'], [127, 138])
S4.add('Kế hoạch vừa được gửi ở tab khác', 'P0', PRE_E, ['Tab 1 mở màn Sửa KH1.', 'Tab 2 mở Sửa KH1, bấm Lưu và gửi.', 'Tab 1 bấm Lưu.'],
       '—', ['Tab 1 báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang", không lưu.'], [128, 91])
S4.add('Người khác không sửa được', 'P0', [ACC_B, KH1], ['Đăng nhập B.', MENU, 'Tìm KH1.'], '—',
       ['B không thấy KH1 (Đang tạo chỉ người tạo thấy) nên không sửa được.'], [128, 63])
S4.add('Kế hoạch đã có phiếu kiểm kê', 'P1', [ACC_A, 'KH3 Đã lập kiểm kê do A tạo.'], ['Đăng nhập A.', MENU, 'Quan sát dòng KH3.'], '—',
       ['Không có nút Sửa, Xóa (kế hoạch đang được dùng ở màn Kiểm kê theo vị trí).'], 129)

# ============================================================== V. XÓA
S5 = Sec(5)
S5.add('Nút Xóa chỉ ở kế hoạch Đang tạo của mình', 'P0', [ACC_A, KH1, KH2], ['Đăng nhập A.', MENU], '—',
       ['KH1 có nút Xóa (thùng rác đỏ); KH2 không có.'], [130, 74])
S5.add('Hộp xác nhận xóa', 'P0', [ACC_A, KH1], ['Đăng nhập A.', MENU, 'Bấm Xóa ở dòng KH1.'], '—',
       ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa bản ghi này không?", nút Xóa (đỏ), Hủy.'], [131, 132])
S5.add('Xóa thành công', 'P0', [ACC_A, KH1], ['Bấm Xóa ở dòng KH1.', 'Bấm Xóa.'], '—',
       ['Báo "Xóa thành công.", KH1 biến mất, tổng giảm 1.'], [133, 139, 140])
S5.add('Hủy xóa', 'P1', [ACC_A, KH1], ['Bấm Xóa ở dòng KH1.', 'Bấm Hủy.'], '—', ['Đóng hộp, KH1 còn nguyên.'], 134)
S5.add('Xóa từ màn chi tiết', 'P1', [ACC_A, KH1], ['Mở chi tiết KH1.', 'Bấm Xóa ở chân màn, bấm Xóa.'], '—',
       ['Báo "Xóa thành công.", về danh sách.'], 133)
S5.add('Không xóa được kế hoạch đang dùng', 'P0', [ACC_A, KH2, 'KH3 Đã lập kiểm kê.'], ['Đăng nhập A.', MENU], '—',
       ['KH2, KH3 không có nút Xóa (đã gửi thủ kho / đã có phiếu kiểm kê).'], [135, 137, 270])
S5.add('Xóa kế hoạch có dữ liệu con', 'P1', [ACC_A, KH1, 'KH1 có 3 vị trí, 10 lô, 2 thành viên hội đồng.'], ['Xóa KH1.'], '—',
       ['Xóa thành công, toàn bộ phạm vi, chi tiết, hội đồng của KH1 bị xóa theo (không còn dữ liệu mồ côi).'], [136, 285])
S5.add('Kế hoạch đã bị xóa ở tab khác', 'P1', [ACC_A, KH1], ['Tab 1, tab 2 cùng mở danh sách.', 'Tab 2 xóa KH1.', 'Tab 1 xóa KH1.'], '—',
       ['Tab 1 báo "Không tìm thấy kế hoạch kiểm kê hoặc bạn không có quyền xem.".'], 138)
S5.add('Kế hoạch vừa được gửi ở tab khác', 'P1', [ACC_A, KH1], ['Tab 2 gửi KH1.', 'Tab 1 bấm Xóa KH1, bấm Xóa.'], '—',
       ['Báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang", không xóa.'], 138)
S5.add('Dữ liệu liên quan sau xóa', 'P1', [ACC_A, KH1], ['Xóa KH1.', 'Vào danh mục Vị trí, xóa vị trí chỉ dùng ở KH1.'], '—',
       ['Vị trí xóa được (không còn kế hoạch nào dùng).'], [141, 280])
S5.add('Lịch sử xóa', 'P2', [ACC_A, KH1], ['Xóa KH1.'], '—', ['Hệ thống ghi mốc "Xóa" cho KH1 trước khi xóa.'], 141)

# ============================================================== VI. GỬI DUYỆT (Lưu và gửi)
S6 = Sec(6)
S6.add('Nút Lưu và gửi', 'P0', PRE_FORM, TAO, '—', ['Nút Lưu và gửi (màu chính, biểu tượng máy bay giấy) ở chân màn Tạo và Sửa.'], 300)
S6.add('Lưu và gửi thành công', 'P0', [PRE_FORM, ACC_TK], FILL + ['Bấm Lưu và gửi.'], FULL,
       ['KHÔNG có hộp xác nhận; báo "Lưu và gửi thành công.", về danh sách.', 'Kế hoạch mới trạng thái Đang kiểm (nhãn vàng).'],
       [86, 92, 301, 302, 305])
S6.add('Lưu và gửi khi thiếu bắt buộc', 'P0', PRE_FORM, TAO + ['Bấm Lưu và gửi.'], '—',
       ['Cùng bộ lỗi như Lưu, "Bạn chưa nhập đầy đủ thông tin.", không lưu, không gửi.'], [87, 88, 303])
S6.add('Lưu và gửi trùng dữ liệu', 'P2', [PRE_FORM, KH2], FILL + ['Bấm Lưu và gửi.'], FULL,
       ['Lưu được, số phiếu khác KH2.'], 89)
S6.add('Gửi từ màn Sửa', 'P0', [ACC_A, KH1], ['Mở Sửa KH1.', 'Bấm Lưu và gửi.'], '—',
       ['Báo "Lưu và gửi thành công.", KH1 chuyển Đang kiểm; không còn nút Sửa, Xóa.'], [302, 305, 311])
S6.add('Màn sau khi gửi', 'P1', PRE_FORM, FILL + ['Bấm Lưu và gửi.'], FULL,
       ['Màn Tạo đóng, về danh sách (không ở lại như Lưu và tiếp tục).'], [90, 91, 92])
S6.add('Dữ liệu sau khi gửi', 'P0', [PRE_FORM, 'Vừa gửi kế hoạch.'], ['Mở chi tiết kế hoạch vừa gửi.'], '—',
       ['Tiêu đề kèm nhãn "Đang kiểm"; phạm vi, chi tiết, hội đồng đúng như đã nhập.'], 306)
S6.add('Thông báo đến thủ kho', 'P0', [PRE_FORM, ACC_TK, 'Kho PTT có thủ kho TK và thủ kho X công ty khác.'], FILL + ['Bấm Lưu và gửi.'],
       FULL, ['TK nhận thông báo "[KHKKVT] Tạo mới: <số phiếu>. Người lập: <tên A>. Chờ lập phiếu kiểm kê. Kho: Phan Trọng Tuệ".',
              'X (khác công ty) và nhân viên không phải thủ kho KHÔNG nhận.'], 308)
S6.add('Bấm thông báo mở kế hoạch', 'P1', [ACC_TK, 'TK vừa nhận thông báo.'], ['Bấm thông báo.'], '—',
       ['Mở màn chi tiết kế hoạch, có nút Lập phiếu kiểm kê.'], 309)
S6.add('Lưu thường không gửi thông báo', 'P1', [PRE_FORM, ACC_TK], FILL + ['Bấm Lưu.'], FULL, ['TK không nhận thông báo nào.'], 308)
S6.add('Kho không có thủ kho', 'P2', [ACC_A, 'Kho Cát Bà chưa khai thủ kho.'], TAO + ['Chọn Kho Cát Bà, nhập đủ, bấm Lưu và gửi.'], '—',
       ['Lưu và gửi thành công, không ai nhận thông báo, không báo lỗi.'], 304)
S6.add('Vị trí không thuộc kho', 'P2', [ACC_A, 'Đang ở màn Tạo, bảng Chi tiết lấy ở kho PTT.'],
       ['Mở tab khác, xóa / chuyển vị trí N1-T2-KV sang kho khác ở danh mục.', 'Quay lại bấm Lưu và gửi.'], '—',
       ['Báo lỗi "Vị trí – Không thuộc kho đã chọn." hoặc "Phạm vi kiểm kê – Vị trí không thuộc kho đã chọn.", không lưu.'], 304)
S6.add('Hủy thao tác gửi (rời màn)', 'P1', PRE_FORM, FILL + ['Bấm Quay lại, chọn Thoát.'], '—',
       ['Không có kế hoạch nào được gửi; thủ kho không nhận thông báo.'], 310)
S6.add('Không gửi lại kế hoạch đã gửi', 'P0', [ACC_A, KH2], [MENU, 'Quan sát dòng KH2.'], '—',
       ['Không có nút Sửa / Lưu và gửi cho KH2 (đã Đang kiểm).'], 311)
S6.add('Lịch sử khi gửi', 'P1', [ACC_A, KH1], ['Sửa KH1, bấm Lưu và gửi.', 'Mở Lịch sử KH1.'], '—',
       ['Có mốc "Thay đổi trạng thái" Đang tạo > Đang kiểm, người thực hiện A, thời điểm gửi.'], [312, 92])
S6.add('Vị trí bị khóa sau khi gửi', 'P0', [ACC_A, 'Kế hoạch KH2 Đang kiểm có vị trí N1-T2-KV.'],
       ['Vào Phiếu điều chuyển vị trí (phân hệ Kho), tạo phiếu ở kho PTT, chọn vị trí xuất N1-T2-KV.'], '—',
       ['Vị trí N1-T2-KV đánh dấu đang kiểm kho, không chọn được; cố điều chuyển > "Vị trí đang kiểm kho.".'], [307, 281])

# ============================================================== VII. LỊCH SỬ THAY ĐỔI
S7 = Sec(7)
PRE_H = [PRE_LIST, P137]
HIS = [MENU, 'Ở dòng TPE-KHKKVT-00137 bấm Lịch sử.']
S7.add('Mở cửa sổ lịch sử', 'P0', PRE_H, HIS, '—', ['Cửa sổ "Lịch sử thay đổi: TPE-KHKKVT-00137".'], 162)
S7.add('Các thông tin của mốc', 'P0', PRE_H, HIS, '—',
       ['Mỗi mốc: thời điểm, hành động, "Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ", nội dung.'], [163, 165, 166, 167])
S7.add('Mới nhất trước', 'P0', PRE_H, HIS, '—',
       ['5 mốc theo thứ tự: 26/10/2026 10:26 Thay đổi trạng thái (Đã lập kiểm kê > Hoàn thành) … cuối cùng 23/10/2026 11:19 Tạo mới.'], 164)
S7.add('Nội dung thay đổi trạng thái do màn khác', 'P0', PRE_H, HIS, '—',
       ['Mốc 23/10 11:20: Đang kiểm > Đã lập kiểm kê, ghi chú "Lập phiếu kiểm kê TPE-KKVT-00138.".',
        'Mốc xóa phiếu: Đã lập kiểm kê > Đang kiểm, ghi chú "Xóa phiếu kiểm kê TPE-KKVT-00138.".',
        'Mốc 26/10: Đã lập kiểm kê > Hoàn thành, "Phiếu kiểm kê TPE-KKVT-00139 được duyệt kết quả.".'], [168, 281])
S7.add('Lọc theo hành động', 'P1', PRE_H, HIS + ['Bấm Bộ lọc, chọn Loại hành động = Tạo mới.'], '—', ['Chỉ còn mốc Tạo mới.'], 169)
S7.add('Lọc theo người thực hiện', 'P2', PRE_H, HIS + ['Bấm Bộ lọc, chọn Người thực hiện = DNS Admin.'], '—', ['Còn đủ 5 mốc.'], 170)
S7.add('Lọc theo thời gian', 'P1', PRE_H, HIS + ['Bấm Bộ lọc, Từ ngày 26/10/2026.'], '—', ['Chỉ còn mốc 26/10/2026 10:26.'], 171)
S7.add('Kết hợp lọc', 'P2', PRE_H, HIS + ['Chọn Loại hành động = Thay đổi trạng thái, Từ ngày 24/10/2026.'], '—', ['Còn 1 mốc.'], 172)
S7.add('Không có kết quả lọc', 'P2', PRE_H, HIS + ['Từ ngày 01/11/2026.'], '—', ['"Không có lịch sử phù hợp bộ lọc.".'], 173)
S7.add('Làm mới / đóng mở bộ lọc', 'P2', PRE_H, HIS + ['Lọc rồi bấm Làm mới.', 'Bấm Bộ lọc lần nữa.'], '—',
       ['Làm mới: hiện lại 5 mốc.', 'Bộ lọc thu gọn / mở lại.'], [174, 175])
S7.add('Kế hoạch chưa có lịch sử', 'P1', [PRE_LIST, 'TPSG-KHKKVT-00131 lập trên hệ thống cũ.'], [MENU, 'Bấm Lịch sử dòng TPSG-KHKKVT-00131.'],
       '—', ['"Chưa có lịch sử thao tác nào.".'], 162)
S7.add('Sửa không đổi gì thì không ghi', 'P1', [ACC_A, KH1], ['Sửa KH1, không đổi, bấm Lưu.', 'Mở Lịch sử.'], '—',
       ['Không có mốc "Thay đổi thông tin" mới.'], [182, 125])
S7.add('Đổi nhiều thông tin cùng lúc', 'P1', [ACC_A, KH1], ['Sửa KH1: đổi phạm vi + hội đồng, bấm Lưu và gửi.', 'Mở Lịch sử.'], '—',
       ['1 mốc "Thay đổi thông tin" liệt kê Vị trí và Danh sách thành viên hội đồng kiểm kê (cũ > mới) + 1 mốc "Thay đổi trạng thái".'],
       183)
S7.add('Đóng cửa sổ', 'P1', PRE_H, HIS + ['Bấm Đóng.', 'Mở lại, bấm (x).'], '—', ['Cả 2 cách đều đóng cửa sổ.'], 184)
S7.add('Trạng thái danh sách sau khi đóng', 'P1', 'Đang ở trang 2, lọc Trạng thái = Hoàn thành.', ['Mở Lịch sử 1 dòng, bấm Đóng.'], '—',
       ['Danh sách giữ trang 2, bộ lọc, sắp xếp.'], 185)
S7.add('Lịch sử ở màn chi tiết', 'P1', PRE_H, [MENU, 'Bấm TPE-KHKKVT-00137.', 'Ở khối Lịch sử bấm Xem lịch sử.'], '—',
       ['Khối Lịch sử có số 5; bấm mở rộng hiện 5 mốc như cửa sổ; nút đổi thành Thu gọn.'], [195, 162])

# ============================================================== VIII. XEM CHI TIẾT
S8 = Sec(8)
DET = [MENU, 'Bấm TPE-KHKKVT-00137.']
S8.add('Mở màn chi tiết', 'P0', PRE_H, DET, '—', ['Mở TRANG chi tiết (không phải cửa sổ nổi).'], 186)
S8.add('Tiêu đề', 'P0', PRE_H, DET, '—', ['"Chi tiết kế hoạch kiểm kê theo vị trí: TPE-KHKKVT-00137" kèm nhãn "Hoàn thành".'], 187)
S8.add('Đầy đủ trường', 'P0', PRE_H, DET, '—',
       ['Thông tin chung: Số phiếu, Ngày kiểm kê, Kho vật lý; Phạm vi kiểm kê 4 cột; Chi tiết; Hội đồng kiểm kê (Bùi Hải Ninh – '
        'Nhân viên kinh doanh); khối Lịch sử.'], 188)
S8.add('Khớp dữ liệu tạo và danh sách', 'P0', PRE_H, DET, '—',
       ['Kho Phan Trọng Tuệ, Ngày kiểm kê 23/10/2026, người tạo DNS Admin khớp dòng ở danh sách.'], [189, 190])
S8.add('Trường chỉ đọc, không có nút Lưu', 'P0', PRE_H, DET, '—',
       ['Mọi ô khóa, mục phạm vi không tick / bỏ tick được, không có ô tìm, Lấy vị trí.', 'Chân màn: In, Xuất Excel, Quay lại; không có Lưu.'],
       [191, 192])
S8.add('Nút theo trạng thái ở chi tiết', 'P0', [ACC_A, KH1, KH2], ['Mở chi tiết KH1.', 'Mở chi tiết KH2.'], '—',
       ['KH1: Sửa, In, Xuất Excel, Xóa, Quay lại.', 'KH2: In, Xuất Excel, Quay lại.'], [193, 194])
S8.add('Quay lại giữ trang và bộ lọc', 'P0', 'Đang ở trang 2, lọc Trạng thái = Hoàn thành.', ['Bấm số phiếu 1 dòng.', 'Bấm Quay lại.'], '—',
       ['Về danh sách giữ bộ lọc Trạng thái = Hoàn thành (trong 10 phút).'], [196, 197])
S8.add('Kế hoạch ngoài phạm vi', 'P0', [ACC_B, 'KH4 Hoàn thành công ty TPSG.'], ['Đăng nhập B.', 'Mở đường link chi tiết KH4.'], '—',
       ['Chuyển sang trang "Không tìm thấy trang".'], [186, 296])
S8.add('Lập phiếu kiểm kê từ kế hoạch', 'P0', [ACC_TK, KH2], ['Đăng nhập TK.', 'Mở chi tiết KH2.', 'Bấm Lập phiếu kiểm kê.'], '—',
       ['Mở màn Thêm phiếu kiểm kê theo vị trí (phân hệ Kho) với KH2 đã chọn sẵn: phạm vi, chi tiết lô, hội đồng.'], [274, 193])
S8.add('Lập phiếu kiểm kê từ danh sách', 'P1', [ACC_TK, KH2], ['Đăng nhập TK.', MENU], '—',
       ['TK chỉ thấy KH2 khi có quyền xem theo cấp; nếu thấy, dòng KH2 có nút Lập phiếu kiểm kê.'], 274)
S8.add('Không phải thủ kho không thấy Lập phiếu kiểm kê', 'P0', [ACC_C, KH2], ['Đăng nhập C.', 'Mở chi tiết KH2.'], '—',
       ['Không có nút Lập phiếu kiểm kê.'], [193, 295])

# ============================================================== IX. IN PHIẾU
S9 = Sec(9)
S9.add('In phiếu từ danh sách', 'P0', PRE_H, [MENU, 'Bấm In ở dòng TPE-KHKKVT-00137.'], '—',
       ['Cửa sổ "Xem trước kế hoạch kiểm kê theo vị trí TPE-KHKKVT-00137".',
        'Bản in: logo / tên công ty của kế hoạch, "KẾ HOẠCH KIỂM KÊ THEO VỊ TRÍ", Số phiếu, Ngày kiểm kê, Kho vật lý, Hội đồng.',
        'Bảng: STT, Nhà kho, Vị trí, Tên hàng, Mã hàng, ĐVT, SL tồn, Công ty, Lô, SL, Cộng; chỗ ký Người lập.'], 228)
S9.add('In phiếu từ màn chi tiết', 'P1', PRE_H, DET + ['Bấm In.'], '—', ['Cùng cửa sổ xem trước như in từ danh sách.'], 228)
S9.add('Bấm In trong cửa sổ', 'P1', 'Đang mở cửa sổ xem trước.', ['Bấm In.'], '—', ['Mở hộp thoại in của trình duyệt.'], 228)
S9.add('In danh sách theo bộ lọc', 'P0', PRE_LIST, [MENU, 'Lọc Trạng thái = Hoàn thành.', 'Bấm In danh sách.'], '—',
       ['Cửa sổ "Xem trước danh sách kế hoạch kiểm kê theo vị trí".',
        'Bảng 14 dòng: STT, Số phiếu, Ngày kiểm kê, Kho, Người tạo, Trạng thái; khối ký "Ngày … Tháng … Năm …", Người lập.'], [220, 227])
S9.add('In danh sách vượt 2.000 dòng', 'P2', 'Bộ lọc ra hơn 2.000 kế hoạch.', ['Bấm In danh sách.'], '—',
       ['Không có bản xem trước, ẩn nút In, hiện dòng nhắc thu hẹp bộ lọc.'], 221)
S9.add('In danh sách rỗng', 'P2', 'Bộ lọc không ra kế hoạch nào.', ['Bấm In danh sách.'], '—', ['"Không có dữ liệu để in".'], 222)
S9.add('Đóng cửa sổ xem trước', 'P2', 'Đang mở cửa sổ xem trước.', ['Bấm (x).'], '—', ['Đóng, giữ nguyên màn đang đứng.'], 184)

# ============================================================== X. TÙY CHỈNH CỘT
S10 = Sec(10)
S10.add('Mở cửa sổ tùy chỉnh cột', 'P0', PRE_LIST, [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" liệt kê 10 cột, "Đang chọn 10/10 cột".'], [198, 199, 200])
S10.add('Ẩn cột', 'P0', PRE_LIST, ['Bỏ tích Ngày cập nhật, bấm Lưu.'], '—', ['"Cập nhật thành công", bảng không còn cột Ngày cập nhật.'], [202, 206])
S10.add('Hiện cột đã ẩn', 'P1', 'Đã ẩn Ngày cập nhật.', ['Tích lại Ngày cập nhật, bấm Lưu.'], '—', ['Cột hiện lại.'], 201)
S10.add('Cột bắt buộc không ẩn', 'P0', PRE_LIST, ['Mở cửa sổ, thử bỏ tích STT, Số phiếu, Hành động.'], '—',
       ['3 cột có biểu tượng ổ khóa, không bỏ tích, không kéo được.'], [203, 205])
S10.add('Kéo thả thứ tự', 'P1', PRE_LIST, ['Kéo Kho lên trên Ngày kiểm kê, bấm Lưu.'], '—', ['Bảng hiện Kho trước Ngày kiểm kê.'], 204)
S10.add('Chọn tất cả / Bỏ chọn hết', 'P2', PRE_LIST, ['Bấm Bỏ chọn hết.', 'Bấm Chọn tất cả.'], '—',
       ['Bỏ chọn hết: còn 3 cột khóa.', 'Chọn tất cả: 10/10.'], 202)
S10.add('Đóng không lưu', 'P1', PRE_LIST, ['Bỏ tích Kho, bấm Đóng.'], '—', ['Bảng vẫn có cột Kho.'], 207)
S10.add('Ghi nhớ sau F5 và theo tài khoản', 'P1', 'A đã ẩn cột Ngày cập nhật.', ['Nhấn F5.', 'Đăng nhập B trên cùng máy.'], '—',
       ['A: vẫn ẩn sau F5 và đăng nhập máy khác.', 'B: thấy đủ 10 cột.'], [208, 209])
S10.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', 'Đang lọc Trạng thái = Hoàn thành (14).', ['Ẩn cột Trạng thái, bấm Lưu.'], '—',
       ['Vẫn 14 kế hoạch, bộ lọc giữ nguyên.'], [210, 211])

# ============================================================== XI. XUẤT DANH SÁCH EXCEL
S11 = Sec(11)
S11.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất Excel" với 8 trường: Số phiếu, Ngày kiểm kê, Kho, Trạng thái, Người tạo, Ngày tạo, Ngày cập nhật, '
        'Người cập nhật; tích sẵn theo cột đang hiện ("Đang chọn 8/8 trường").'], [212, 213, 214])
S11.add('Xuất trường mặc định', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel, bấm Xuất file.'], '—',
       ['Tải "danh_sach_ke_hoach_kiem_ke_theo_vi_tri.xlsx", báo "Xuất Excel thành công.".',
        'File: letterhead, "DANH SÁCH KẾ HOẠCH KIỂM KÊ THEO VỊ TRÍ", cột STT + 8 trường, 20 dòng, khối ký.'], [215, 216, 223, 224, 225, 227])
S11.add('Xuất một số trường theo thứ tự kéo', 'P1', PRE_LIST, ['Bỏ chọn hết, tích Kho rồi Số phiếu, kéo Kho lên đầu, Xuất file.'], '—',
       ['File chỉ có STT, Kho, Số phiếu theo đúng thứ tự.'], [217, 226])
S11.add('Không chọn trường', 'P1', PRE_LIST, ['Bấm Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S11.add('Xuất theo tìm kiếm / bộ lọc', 'P0', PRE_LIST, ['Lọc Trạng thái = Hoàn thành, Ngày kiểm kê 01/10/2026 – 31/10/2026.', 'Xuất file.'],
       '—', ['File chỉ có kế hoạch khớp; có dòng "Từ ngày 01/10/2026 đến ngày 31/10/2026".'], [219, 220])
S11.add('Xuất nhiều trang', 'P1', PRE_LIST, ['Đang ở trang 1 (10 dòng), Xuất file.'], '—', ['File có đủ 20 dòng, không chỉ trang đang xem.'], 221)
S11.add('Danh sách rỗng', 'P2', 'Bộ lọc không ra kế hoạch nào.', ['Xuất file.'], '—',
       ['Vẫn ra file có tiêu đề, dòng tên cột, khối ký, không có dòng dữ liệu.'], 222)
S11.add('Dữ liệu khớp, định dạng ngày và tiếng Việt', 'P1', [PRE_LIST, P137], ['Xuất file, mở dòng TPE-KHKKVT-00137.'], '—',
       ['Ngày kiểm kê "23/10/2026 11:19" giữ dạng chữ; Kho "Phan Trọng Tuệ", Trạng thái "Hoàn thành" đủ dấu tiếng Việt.'], [228, 229, 230])
S11.add('Xuất Excel 1 kế hoạch', 'P0', PRE_H, [MENU, 'Bấm Xuất Excel ở dòng TPE-KHKKVT-00137.'], '—',
       ['Tải "ke_hoach_kiem_ke_theo_vi_tri_TPE-KHKKVT-00137.xlsx", báo "Xuất Excel thành công.".',
        'File có thông tin chung và bảng chi tiết như bản in; số lượng là ô số.'], [223, 228, 293])

# ============================================================== XII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S12 = Sec(12)
S12.add('Kế hoạch Đang kiểm hiện ở popup Chọn kế hoạch', 'P0', [ACC_TK, KH2],
       ['Đăng nhập TK.', 'Vào phân hệ Kho > Kiểm kho > Theo vị trí > Kiểm kê theo vị trí, bấm Tạo mới, mở ô chọn kế hoạch.'], '—',
       ['Popup "Chọn kế hoạch kiểm kê theo vị trí" có KH2; không có kế hoạch Đang tạo / Hoàn thành.'], [274, 276])
S12.add('Lập phiếu kiểm kê đổi trạng thái kế hoạch', 'P0', [ACC_TK, KH2], ['Lập và lưu phiếu kiểm kê từ KH2.', 'Mở danh sách kế hoạch.'], '—',
       ['KH2 chuyển Đã lập kiểm kê (xanh dương); lịch sử có mốc Thay đổi trạng thái kèm mã phiếu kiểm kê.'], [281, 284])
S12.add('Xóa phiếu kiểm kê trả kế hoạch về Đang kiểm', 'P1', [ACC_TK, 'KH2 Đã lập kiểm kê, phiếu kiểm kê còn sửa / xóa được.'],
       ['Xóa phiếu kiểm kê.', 'Mở danh sách kế hoạch.'], '—', ['KH2 trở về Đang kiểm, lập lại phiếu được.'], [281, 284])
S12.add('Duyệt kết quả phiếu kiểm kê > Hoàn thành', 'P1', [ACC_TK, 'KH2 Đã lập kiểm kê.'],
       ['Phiếu kiểm kê của KH2 được duyệt kết quả, không còn chênh lệch thiếu.'], '—', ['KH2 chuyển Hoàn thành (xanh lá).'], 281)
S12.add('Bộ lọc màn liên quan cập nhật', 'P2', [ACC_TK, KH2], ['Sau khi KH2 Đã lập kiểm kê, mở lại popup Chọn kế hoạch.'], '—',
       ['KH2 không còn trong popup.'], 282)
S12.add('Không xóa được danh mục kho đang dùng', 'P0', [ACC_A, KH2], ['Vào phân hệ Kho > Danh mục > Vị trí, xóa vị trí N1-T2-KV.'], '—',
       ['Hệ thống chặn xóa vì vị trí đang được dùng.', 'Tương tự với Nhà kho, Dãy, Khoang, Kho vật lý đã có trong kế hoạch.'], 270)
S12.add('Không xóa được hàng hóa đang dùng', 'P1', [ACC_A, KH2], ['Vào danh mục Hàng hoá, xóa "Quạt ENEOS".'], '—',
       ['Hệ thống chặn xóa vì hàng đã có trong chứng từ.'], 270)
S12.add('Đổi tên danh mục không đổi kế hoạch', 'P1', [ACC_A, KH2], ['Đổi tên vị trí N1-T2-KV thành "N1-T2-KV-NEW".', 'Mở chi tiết KH2.'], '—',
       ['Bảng Chi tiết vẫn ghi vị trí, tên hàng như lúc Lấy vị trí (lưu cố định); liên kết vị trí không mất.'], [272, 278, 279])
S12.add('Số tồn là ảnh chụp', 'P1', [ACC_A, KH1], ['Nhập thêm 10 Quạt ENEOS vào N1-T2-KV.', 'Mở chi tiết KH1.'], '—',
       ['SL tồn trên KH1 vẫn 1,227; chỉ đổi khi Sửa và bấm Lấy vị trí lại.'], [286, 269])
S12.add('Kế hoạch mới xuất hiện ở màn liên quan', 'P1', [ACC_TK, PRE_FORM], ['A tạo và Lưu và gửi kế hoạch.', 'TK mở popup Chọn kế hoạch.'],
       '—', ['Kế hoạch mới có trong popup.'], 274)
S12.add('Tồn kho không đổi khi lưu kế hoạch', 'P0', PRE_FORM, ['Ghi tồn Quạt ENEOS tại N1-T2-KV.', 'Tạo và gửi kế hoạch.', 'Xem lại tồn.'],
       '—', ['Tồn không đổi (kế hoạch không ghi tồn).'], 286)

# ============================================================== XIII. PHÂN QUYỀN (cuối)
S13 = Sec(13)
S13.add('Quyền tổng công ty: xem mọi kế hoạch', 'P0', [ACC_T, '20 kế hoạch không Đang tạo thuộc TPE, TPSG, TPHP.'], ['Đăng nhập T.', MENU], '—',
       ['Thấy đủ 20 kế hoạch; có ô Công ty – Phòng ban, chọn được mọi công ty.'], [287, 299])
S13.add('Quyền công ty: chỉ công ty mình + của mình', 'P0', [ACC_C, 'TPE có 6 kế hoạch, TPSG 8, TPHP 6.'], ['Đăng nhập C.', MENU], '—',
       ['Chỉ thấy 6 kế hoạch TPE (và kế hoạch C tự tạo); ô Công ty khóa ở TPE.'], [287, 299])
S13.add('Không quyền: chỉ kế hoạch mình tạo', 'P0', [ACC_A, 'A tạo 2 kế hoạch.'], ['Đăng nhập A.', MENU], '—',
       ['Chỉ thấy 2 kế hoạch của A; không có ô Công ty – Phòng ban.'], [287, 299])
S13.add('Đang tạo chỉ người tạo thấy', 'P0', [ACC_T, KH1], ['Đăng nhập T.', MENU, 'Tìm số phiếu KH1.'], '—',
       ['T không thấy KH1 dù có quyền tổng công ty.'], [287, 299])
S13.add('Xem chi tiết theo phạm vi', 'P0', [ACC_C, 'KH4 công ty TPSG.'], ['Đăng nhập C.', 'Mở đường link chi tiết KH4.'], '—',
       ['Trang "Không tìm thấy trang".'], [288, 296])
S13.add('Thủ kho xem kế hoạch Đang kiểm của kho mình', 'P0', [ACC_TK, KH2], ['Đăng nhập TK.', 'Mở chi tiết KH2 từ thông báo.'], '—',
       ['Mở được (ngoại lệ cho thủ kho có quyền Lập phiếu kiểm kê kho theo vị trí).'], 288)
S13.add('Thêm mới không cần quyền', 'P0', ACC_B, ['Đăng nhập B.', MENU, 'Bấm Tạo mới, nhập đủ, bấm Lưu.'], FULL, ['Lưu thành công.'], 289)
S13.add('Sửa chỉ người tạo', 'P0', [ACC_T, 'Kế hoạch KH5 Đang tạo do T tạo, KH2 do A tạo.'], ['Đăng nhập T.', MENU], '—',
       ['KH5 có Sửa; KH2 không có Sửa (không phải người tạo, không Đang tạo).'], [290, 295])
S13.add('Xóa chỉ người tạo', 'P0', [ACC_T, 'KH5 Đang tạo do T tạo.'], ['Đăng nhập T.', MENU], '—',
       ['Chỉ KH5 có nút Xóa.'], [291, 295])
S13.add('Xuất / In / Lịch sử theo phạm vi', 'P1', ACC_A, ['Đăng nhập A.', MENU, 'Xuất Excel; mở Lịch sử 1 kế hoạch của A.'], '—',
       ['File chỉ chứa kế hoạch của A; lịch sử xem được.'], [293, 294])
S13.add('Lập phiếu kiểm kê cần quyền và là thủ kho', 'P0',
       [ACC_TK, KH2, 'Tài khoản TK2: thủ kho kho PTT nhưng không có quyền Lập phiếu kiểm kê kho theo vị trí.'],
       ['Đăng nhập TK, mở chi tiết KH2.', 'Đăng nhập TK2, mở chi tiết KH2 (bằng quyền xem theo cấp).'], '—',
       ['TK: có nút Lập phiếu kiểm kê.', 'TK2: không có nút.'], [295, 287])
S13.add('Mở đường link màn Sửa khi không phải người tạo', 'P0', [ACC_C, 'KH6 Đang kiểm công ty TPE do A tạo.'],
       ['Đăng nhập C.', 'Mở đường link màn Sửa của KH6.'], '—', ['Tự chuyển sang màn chi tiết KH6, không sửa được.'], 296)
S13.add('Thao tác bị chặn lại ở máy chủ', 'P1', [ACC_A, KH1], ['Tab 1 mở Sửa KH1.', 'Tab 2 gửi KH1.', 'Tab 1 bấm Xóa ở danh sách cũ.'], '—',
       ['Báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang"; máy chủ kiểm lại điều kiện ở từng thao tác, không dựa vào việc ẩn nút.'], 297)
S13.add('Đổi quyền giữa thao tác', 'P1', [ACC_C, 'Quản trị gỡ quyền "theo công ty" của C khi C đang ở danh sách.'],
       ['C bấm sang trang 2 / mở chi tiết kế hoạch TPE của người khác.'], '—',
       ['Danh sách chỉ còn kế hoạch của C; chi tiết kế hoạch người khác > "Không tìm thấy trang".'], 298)
S13.add('Super admin có đủ quyền', 'P2', 'Tài khoản DNS Admin (Super admin), không gán quyền riêng.', ['Đăng nhập DNS Admin.', MENU], '—',
       ['Thấy 20 kế hoạch mọi công ty, có ô Công ty – Phòng ban.'], 287)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'CHỈNH SỬA', S4),
    ('V', 'XÓA', S5),
    ('VI', 'GỬI DUYỆT', S6),
    ('VII', 'LỊCH SỬ THAY ĐỔI', S7),
    ('VIII', 'XEM CHI TIẾT KẾ HOẠCH KIỂM KÊ', S8),
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
    build_chuan(output_file=OUT, sheet_name='Trang tính1', feature_name='Kế hoạch kiểm kê theo vị trí - Cập nhật ngày 05/11/2026',
                module_name='Kế hoạch kiểm kê theo vị trí', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

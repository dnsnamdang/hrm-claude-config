# -*- coding: utf-8 -*-
"""Testcase màn "Kế hoạch kiểm kê theo hàng hóa" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (không phải danh mục) — lý do từ code: màn là chứng từ có số phiếu tự sinh <mã công ty>.KHKKHH-NNNNN, vòng đời trạng
thái Đang tạo > Đang kiểm > Đã lập phiếu kiểm kê (SelfInventoryRequest::STATUSES), Thêm / Sửa / Xóa theo trạng thái + người tạo,
Lưu và kiểm (chuyển trạng thái + thông báo), In phiếu (mẫu in), Xuất Excel 1 phiếu, lịch sử; không có Khóa / Mở khóa như danh mục.
Nhóm theo đúng tên + thứ tự chuẩn loại 'phieu' (check_tc.THU_TU), bỏ nhóm màn không có (kiểm code 05/11/2026: không có route / nút
Khóa, Duyệt, Không duyệt, Hủy, Import):
I Hiển thị · II Tìm kiếm & lọc (gồm Cài đặt bộ lọc) · III Thêm mới (Lưu, Lưu và tiếp tục, Thêm hàng hóa, Làm mới số liệu, rời màn) ·
IV Chỉnh sửa · V Xóa · VI Gửi duyệt (Lưu và kiểm > Đang kiểm, chặn phiếu treo, thông báo) · VII Lịch sử · VIII Xem chi tiết (gồm Lập
phiếu kiểm kê) · IX In phiếu (kèm In danh sách) · X Tùy chỉnh cột · XI Xuất danh sách Excel (kèm Xuất 1 phiếu) · XII Ràng buộc · XIII Phân quyền.
Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../ke-hoach-kiem-ke-theo-vi-tri/gen_testcase.py (05/11, qua check_tc 0 lỗi).
Nguồn hành vi (đọc 05/11/2026, nhánh develop): FE pages/finance/self-inventory-requests/**; BE Modules/Finance SelfInventoryRequest*
(Entity / Service / WriteService / Controller / StoreRequest / PrintService / Export), SelfInventoryWriteService, SelfInventoryService.
Số liệu mẫu: dev-hrm 05/11/2026 (DNS Admin) 20 kế hoạch, cả 20 Đã lập phiếu kiểm kê; TPE.KHKKHH-00020 có 2 mốc lịch sử.
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
MENU = 'Vào phân hệ Tài chính > menu "Kiểm kê" > bấm "Kế hoạch kiểm kê theo hàng hóa".'
TAO = [MENU, 'Bấm "Tạo mới".']
ADV = 'Bấm Tìm kiếm nâng cao.'
Q1 = 'Lập phiếu kiểm kê kho theo hàng hóa'

ACC_A = 'Tài khoản A: nhân viên công ty TPE, không có quyền xem theo cấp; là người lập kế hoạch.'
ACC_B = 'Tài khoản B: nhân viên công ty TPE, không có quyền xem theo cấp, không phải người tạo.'
ACC_C = 'Tài khoản C: có quyền "Tổng kiểm kê kho theo hàng hóa", thuộc công ty TPE.'
ACC_T = 'Tài khoản T: có quyền "Tổng kiểm kê kho theo hàng hóa - tổng công ty".'
ACC_K = 'Tài khoản K: nhân viên công ty TPE, có quyền "%s", không có quyền xem theo cấp.' % Q1
PRE_LIST = 'Tài khoản DNS Admin (Super admin); trong phạm vi xem có 20 kế hoạch, cả 20 ở trạng thái Đã lập phiếu kiểm kê.'
P20 = ('Kế hoạch TPE.KHKKHH-00020: kho Phan Trọng Tuệ, trạng thái Đã lập phiếu kiểm kê, Người tạo DNS Admin, Ngày kiểm kê 31/10/2026 '
       '09:38, Ghi chú "Ghi chú"; 2 hàng (Máy tính xách tay ACER-A315-34-P3LC SL 50, MẶT NẠ BẢO VỆ 3M-H8APW96 SL 15); hội đồng Bùi Sỹ '
       'Phú; có 2 mốc lịch sử.')
KHO = ('Kho PTT - Phan Trọng Tuệ có hàng "Máy tính xách tay" (mã ACER-A315-34-P3LC) còn tồn kho kế toán ở 2 kho kế toán, trong đó '
       'PTT01 - Phan Trọng Tuệ - Hàng bán SL 50.')
PRE_FORM = ACC_A + '\n' + KHO
KH1 = 'Kế hoạch KH1 trạng thái Đang tạo do A tạo: kho Phan Trọng Tuệ, 1 hàng Máy tính xách tay, hội đồng 1 người (Bùi Duy Trước).'
KH2 = 'Kế hoạch KH2 trạng thái Đang kiểm do A tạo ở kho Phan Trọng Tuệ.'
FILL = TAO + ['Chọn Kho = PTT - Phan Trọng Tuệ.', 'Bấm Thêm hàng hóa, tick "Máy tính xách tay", bấm Thêm (1).',
              'Ở dòng 1 Hội đồng chọn Thành viên = Bùi Duy Trước.']
FULL = ['Kho: PTT - Phan Trọng Tuệ', 'Hàng hóa: Máy tính xách tay', 'Thành viên: Bùi Duy Trước']
OK_LIST = 'Báo "Lưu thành công.", về màn danh sách; dòng mới ở trên cùng, trạng thái Đang tạo (nhãn xám).'
PENDING_PRE = 'Kho PTT có phiếu nhập kho PNK-11618 chưa xử lý xong, chứa hàng Máy tính xách tay.'

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
     'Lập kế hoạch kiểm kê theo hàng hóa: chọn một hoặc nhiều kho, chọn các hàng cần kiểm (chỉ hàng còn tồn kho kế toán), chụp '
     'tồn kho kế toán theo từng kho kế toán, chỉ định Hội đồng kiểm kê, rồi Lưu và kiểm để người có quyền lập phiếu kiểm kê theo '
     'hàng hóa. Kế hoạch KHÔNG làm đổi tồn kho.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Danh sách: kế hoạch trong phạm vi xem; trạng thái Đang tạo (xám), Đang kiểm (vàng), Đã lập phiếu kiểm kê (xanh dương), '
     'Hoàn thành (xanh lá, chỉ dữ liệu cũ).\n- Bảng Hàng hóa: mỗi hàng kèm các kho kế toán có tồn > 0 trong các kho đã chọn.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Kế hoạch Đang tạo của người khác (kể cả với quyền tổng công ty).\n- Kế hoạch ngoài phạm vi quyền xem.\n'
     '- Hàng không còn tồn kho kế toán trong kho đã chọn (không hiện ở popup, không thêm được).\n'
     '- Kế hoạch của màn Kế hoạch tổng kiểm kê hàng hóa (màn khác).'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày kiểm kê lọc theo ngày lập kế hoạch, lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Kế hoạch > các kho.\n- Kế hoạch > hàng hóa (Tổng SL) > kho kế toán (SL tồn kho kế toán).\n'
     '- Hội đồng: danh sách thành viên + chức vụ.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Tổng SL = cộng SL tồn kho kế toán các dòng kho kế toán của hàng.\n'
     '- Mỗi hàng chỉ 1 lần trong kế hoạch; hội đồng không trùng thành viên; kho không trùng.'),
    ('7. Phân quyền cấp',
     '- Tổng kiểm kê kho theo hàng hóa - tổng công ty: xem mọi kế hoạch.\n'
     '- Tổng kiểm kê kho theo hàng hóa: kế hoạch công ty mình + của mình.\n'
     '- Không quyền: chỉ kế hoạch mình tạo. Tạo / Sửa / Xóa không cần quyền (Sửa / Xóa chỉ người tạo, Đang tạo).\n'
     '- Lập phiếu kiểm kê kho theo hàng hóa: nút Lập phiếu kiểm kê theo hàng hóa + nhận thông báo.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là khoảng thứ tự dòng của trang, N là tổng kế hoạch khớp bộ lọc trong phạm vi xem.\n'
     '- Tổng SL của hàng = cộng SL tồn kho kế toán các dòng của hàng đó.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: A (người lập, không quyền xem theo cấp), B (nhân viên khác), C (quyền theo công ty), T (quyền '
     'tổng công ty), K (quyền Lập phiếu kiểm kê kho theo hàng hóa), DNS Admin (Super admin).\n'
     '- Lưu ý: Lưu và kiểm chuyển trạng thái NGAY, không có hộp xác nhận; kế hoạch đã Đang kiểm không sửa / xóa được — chạy trên '
     'dữ liệu thử.\n'
     '- Lưu ý: số tồn trên kế hoạch là ảnh chụp lúc thêm hàng; Làm mới số liệu chỉ đổi trên màn, phải Lưu mới ghi.\n'
     '- Lưu ý: số phiếu dùng dấu chấm sau mã công ty (TPE.KHKKHH-00020).\n'
     '- Màn Tạo / Sửa / Chi tiết là TRANG riêng, không phải cửa sổ nổi.'),
]

SCREEN = ListScreen(menu=MENU, title='Danh sách kế hoạch kiểm kê theo hàng hóa', total=20, quick_label='số phiếu',
                    quick_sample='00020', quick_hit='kế hoạch TPE.KHKKHH-00020',
                    filters=[('Trạng thái', 'Đã lập phiếu kiểm kê'), ('Kho', 'LN - Liên Ninh')], unit='kế hoạch')

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Cả 3 nơi đều là "Danh sách kế hoạch kiểm kê theo hàng hóa".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE_LIST, [MENU, 'Quan sát khối bộ lọc và thanh công cụ.'], '—',
       ['Khối bộ lọc: ô tìm nhanh (gợi ý "Tìm theo số phiếu"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
        'Thanh công cụ: Tạo mới, Xuất Excel, In danh sách, nút biểu tượng cột.',
        'Dòng Đã lập phiếu kiểm kê: cột Hành động có In, Xuất Excel, Lịch sử; không có Sửa, Xóa.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 10 cột theo thứ tự: STT, Số phiếu, Ngày kiểm kê, Kho, Trạng thái, Người tạo, Ngày tạo, Ngày cập nhật, Người cập '
        'nhật, Hành động.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 10/10 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp kế hoạch đã tạo', 'P0', [PRE_LIST, P20], [MENU, 'Tìm "TPE.KHKKHH-00020", đối chiếu dòng.'], '—',
       ['Ngày kiểm kê "31/10/2026 09:38", Kho "Phan Trọng Tuệ", Trạng thái "Đã lập phiếu kiểm kê", Người tạo "DNS Admin", Ngày '
        'tạo "31/10/2026 09:38", Ngày cập nhật "31/10/2026 09:38", Người cập nhật "DNS Admin".'], [6, 58])
S1.add('Kế hoạch nhiều kho', 'P1', [PRE_LIST, 'TPSG.KHKKHH-00002 gồm 2 kho Kho Sài Gòn và Chăm sóc khách hàng.'],
       [MENU, 'Tìm "TPSG.KHKKHH-00002".'], '—', ['Cột Kho ghi "Kho Sài Gòn, Chăm sóc khách hàng" (nối dấu phẩy).'], 6)
S1.add('Trạng thái bản ghi', 'P0', PRE_LIST, [MENU, ADV, 'Mở ô Trạng thái.', 'Quan sát cột Trạng thái.'], '—',
       ['Ô có 3 lựa chọn: Đang tạo, Đang kiểm, Đã lập phiếu kiểm kê (KHÔNG có Hoàn thành).',
        'Nhãn: Đang tạo xám, Đang kiểm vàng, Đã lập phiếu kiểm kê xanh dương.'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', [ACC_B, 'B chưa tạo kế hoạch nào.'], ['Đăng nhập B.', MENU], '—',
       ['Bảng hiện "Không có dữ liệu phù hợp."; không báo lỗi.'], 8)
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
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', ADV, 'Chọn Kho = LN - Liên Ninh.'],
       'Kho: LN - Liên Ninh', ['Tự nạp lại ở trang 1; "Hiển thị 1–10 / 10".'], 17)
S1.add('Sắp xếp tăng dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Số phiếu.'], '—',
       ['Xếp theo số phiếu tăng dần (TPE.KHKKHH-00004 … rồi TPSG.KHKKHH-…), mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Số phiếu 2 lần.'], '—',
       ['Xếp theo số phiếu giảm dần, mũi tên xuống.'], 21)
S1.add('Sắp xếp theo Ngày kiểm kê và Ngày tạo', 'P1', PRE_LIST,
       [MENU, 'Bấm tiêu đề Ngày kiểm kê (2 lần).', 'Bấm tiêu đề Ngày tạo.'], '—',
       ['Ngày kiểm kê: lần 1 cũ nhất trên (TPSG.KHKKHH-00001 13/10/2025), lần 2 mới nhất trên.', 'Ngày tạo: lần 1 cũ nhất trên.',
        'Khi mới vào chưa chọn cột nào: tạo mới nhất trên, các cột hiện biểu tượng sắp xếp trung tính.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Kho, Trạng thái, Người tạo, Ngày cập nhật, Người cập nhật.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Số phiếu (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự tăng của trang 1.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 2.', 'Bấm tiêu đề Ngày kiểm kê.'], '—', ['Về trang 1.'], 25)
S1.add('Nút thao tác theo trạng thái', 'P0', [ACC_A, KH1, KH2], ['Đăng nhập A.', MENU, 'Quan sát cột Hành động 2 dòng KH1, KH2.'], '—',
       ['KH1 (Đang tạo): Sửa, Xóa và nút ba chấm "Hành động khác" chứa In, Xuất Excel, Lịch sử.',
        'KH2 (Đang kiểm, A không có quyền Lập phiếu kiểm kê kho theo hàng hóa): In, Xuất Excel, Lịch sử; không có Sửa, Xóa, Lập '
        'phiếu.'], [3, 34])
S1.add('Mở màn từ thông báo', 'P1', [ACC_K, KH2, 'K đã nhận thông báo "[KHKKHH] Tạo mới: <số phiếu KH2>".'],
       ['Đăng nhập K.', 'Bấm chuông thông báo, bấm thông báo của KH2.'], '—',
       ['Mở màn chi tiết KH2 (K không có quyền xem theo cấp vẫn mở được).', 'Có nút Lập phiếu kiểm kê theo hàng hóa.'], 1)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo số phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "TPE.KHKKHH-00020", bấm Tìm kiếm.'], 'Ô tìm nhanh: TPE.KHKKHH-00020',
       ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần số phiếu', 'P0', PRE_LIST, [MENU, 'Nhập "TPSG", bấm Tìm kiếm.'], 'Ô tìm nhanh: TPSG',
       ['Chỉ còn 3 kế hoạch TPSG.KHKKHH-00003, 00002, 00001.'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "tpe.khkkhh-00020", bấm Tìm kiếm.'], '—',
       ['Ra TPE.KHKKHH-00020 như khi gõ chữ hoa.'], 28)
S2.add('Có dấu / không dấu ở ô Tên hàng hóa', 'P2', PRE_LIST, [MENU, ADV, 'Nhập Tên hàng hóa "may tinh xach tay", bấm Tìm kiếm.'], '—',
       ['Ra kế hoạch có hàng "Máy tính xách tay" nếu cơ sở dữ liệu so khớp không dấu.',
        'Lưu ý: so khớp theo cách so sánh chữ của cơ sở dữ liệu.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; ký tự % được hiểu là ký tự đại diện nên ra toàn bộ.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  TPE.KHKKHH-00020  ", bấm Tìm kiếm.'], '—',
       ['Ra TPE.KHKKHH-00020 (bỏ khoảng trắng đầu / cuối).'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "TPE.KHKKHH-00020", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Sau bước 2 hiện lại đủ 20 kế hoạch.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST,
       [MENU, 'Nhập "00020", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'], '—',
       ['Cả 2 cách đều ra TPE.KHKKHH-00020, về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['Các ô Kho, Trạng thái, Người tạo, Mã hàng hóa, Tên hàng hóa, Ngày kiểm kê, Công ty, Phòng ban đều trống.',
        'Đủ 20 kế hoạch.'], 36)
S2.add('Lọc Kho', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = LN - Liên Ninh.'], '—',
       ['Lọc ngay; còn 10 kế hoạch có kho Liên Ninh.', 'Ô Kho liệt kê mọi kho, hiển thị "Mã - Tên".'], 37)
S2.add('Lọc Kho với kế hoạch nhiều kho', 'P1', PRE_LIST, [MENU, ADV, 'Chọn Kho = CSKH - Chăm sóc khách hàng.'], '—',
       ['Ra 3 kế hoạch: TPE.KHKKHH-00014 và 2 kế hoạch TPSG.KHKKHH-00002, 00001 (gồm 2 kho).'], 37)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đã lập phiếu kiểm kê.', 'Đổi Trạng thái = Đang kiểm.'], '—',
       ['Bước 3: đủ 20 kế hoạch, nhãn xanh dương.', 'Bước 4: "Không có dữ liệu phù hợp.".'], 37)
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = Trần Thị Phương.'], '—',
       ['Chỉ còn TPSG.KHKKHH-00003 và TPSG.KHKKHH-00001.',
        'Ô Người tạo liệt kê toàn bộ nhân viên, kể cả người chưa tạo kế hoạch nào.'], 37)
S2.add('Lọc Mã hàng hóa', 'P0', PRE_LIST, [MENU, ADV, 'Nhập Mã hàng hóa "ACER-A315", bấm Tìm kiếm.'], '—',
       ['Ra các kế hoạch có hàng mã chứa "ACER-A315" (có TPE.KHKKHH-00020).', 'Chỉ gõ chưa bấm Tìm kiếm thì danh sách chưa đổi.'], 37)
S2.add('Lọc Tên hàng hóa', 'P0', PRE_LIST, [MENU, ADV, 'Nhập Tên hàng hóa "mặt nạ", bấm Tìm kiếm.'], '—',
       ['Ra các kế hoạch có hàng tên chứa "mặt nạ" (có TPE.KHKKHH-00020), không phân biệt hoa / thường.'], 37)
S2.add('Lọc Ngày kiểm kê lấy trọn ngày biên', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày kiểm kê 23/10/2026 – 23/10/2026.'], '—',
       ['Ra 5 kế hoạch TPE.KHKKHH-00014, 00013, 00012, 00011, 00010 (tạo 10:17 – 15:48 ngày 23/10/2026).',
        'Bỏ trống ngày cuối vẫn lọc được từ ngày đầu.'], 37)
S2.raw(org_cases(SCREEN, len(S2) + 1), [[37], [37, 283], [37]])
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = LN - Liên Ninh.', 'Chọn Ngày kiểm kê 26/10/2026 – 26/10/2026.'],
       '—', ['Chỉ còn TPE.KHKKHH-00018 và 00017.'], 38)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST, [MENU, 'Nhập "TPSG", bấm Tìm kiếm.', ADV, 'Chọn Kho = PTT.'], '—',
       ['"Không có dữ liệu phù hợp." vì kế hoạch TPSG thuộc Kho Sài Gòn.'], [39, 40])
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = LN - Liên Ninh.', 'Đổi Số dòng/trang = 5, bấm trang 2.'],
       '—', ['"Hiển thị 1–5 / 10" rồi "Hiển thị 6–10 / 10"; STT liên tục.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Kho = LN - Liên Ninh.', ['Bấm tiêu đề Số phiếu.'], '—',
       ['Chỉ 10 kế hoạch đang lọc được sắp; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "TPE", lọc Kho Liên Ninh, Tên hàng hóa "giá", sắp Số phiếu, ở trang 2.',
       ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh, Kho, Tên hàng hóa về trống, bỏ sắp xếp, nạp lại trang 1, đủ 20 kế hoạch.'], 44)
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Kho = LN - Liên Ninh, chưa mở màn con.'], ['Nhấn F5.'], '—',
       ['Bộ lọc trở về trống, đủ 20 kế hoạch (chỉ nhớ khi đi vào màn con của màn này).'], 46)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Mã hàng hóa, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô Mã hàng hóa.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Kho = LN - Liên Ninh.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Kho, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị bỏ, nạp lại đủ 20 kế hoạch.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Mã hàng hóa.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Mã hàng hóa vẫn ẩn.', 'Bước 2: tích đủ 7 mục, Mã hàng hóa hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Trạng thái lên đầu, bấm Lưu.'], '—',
       ['Ô Trạng thái đứng đầu khối Tìm kiếm nâng cao; cấu hình giữ sau khi đăng nhập lại.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo', 'P0', PRE_FORM, TAO, '—', ['Mở TRANG "Tạo kế hoạch kiểm kê theo hàng hóa", tab cùng tiêu đề.'], 49)
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải ghi tên A.', 'Không có ô Số phiếu (tự sinh khi lưu).'], 50)
S3.add('Các trường, khối và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Ngày kiểm kê *, Kho * (gợi ý "Chọn kho"), Ghi chú (gợi ý "Nhập ghi chú").',
        'Hàng hóa *: nút Làm mới số liệu (mờ), Thêm hàng hóa; bảng STT, Tên hàng, Model, Mã hàng, ĐVT, Kho kế toán, SL tồn kho kế '
        'toán, Tổng SL, Hành động; "Không có dữ liệu".',
        'Hội đồng kiểm kê * có 1 dòng trống và nút Thêm dòng.',
        'Chân màn: Lưu, Lưu và kiểm, Lưu và tiếp tục, Quay lại.'], [51, 54])
S3.add('Trường bắt buộc / không bắt buộc', 'P0', PRE_FORM, TAO + ['Quan sát dấu *.'], '—',
       ['Dấu * ở Ngày kiểm kê, Kho, Hàng hóa, Hội đồng kiểm kê, Thành viên, Chức vụ.', 'Ghi chú không bắt buộc.'], 52)
S3.add('Giá trị mặc định', 'P0', PRE_FORM, TAO, '—',
       ['Ngày kiểm kê = ngày hôm nay, ô khóa nền xám.', 'Kho trống, Ghi chú trống, bảng Hàng hóa "Không có dữ liệu".',
        'Hội đồng có 1 dòng trống.'], 53)
S3.add('Lưu với dữ liệu hợp lệ đầy đủ', 'P0', PRE_FORM, FILL + ['Nhập Ghi chú "Kiểm kê định kỳ tháng 11".', 'Bấm Lưu.'],
       FULL + ['Ghi chú: Kiểm kê định kỳ tháng 11'],
       [OK_LIST, 'Số phiếu dạng "TPE.KHKKHH-<số>" theo công ty của A.'], [55, 58, 59, 79])
S3.add('Lưu chỉ với trường bắt buộc tối thiểu', 'P0', PRE_FORM, FILL + ['Để trống Ghi chú.', 'Bấm Lưu.'], FULL,
       [OK_LIST, 'Chi tiết kế hoạch: Ghi chú trống.'], [56, 57])
S3.add('Dữ liệu sau lưu', 'P0', [PRE_FORM, 'A vừa lưu kế hoạch ở TC_03.006.'], ['Bấm số phiếu vừa tạo.'], '—',
       ['Chi tiết: Kho Phan Trọng Tuệ, Ghi chú đúng, bảng Hàng hóa có Máy tính xách tay với các dòng kho kế toán đúng như lúc thêm, '
        'Tổng SL = cộng các dòng.', 'Hội đồng: Bùi Duy Trước, chức vụ tự điền.'], 58)
S3.add('Trạng thái mặc định sau Lưu', 'P0', [PRE_FORM, 'A vừa lưu kế hoạch.'], [MENU, 'Đăng nhập DNS Admin, mở danh sách.'], '—',
       ['A thấy kế hoạch Đang tạo (nhãn xám).', 'DNS Admin KHÔNG thấy kế hoạch này (Đang tạo chỉ người tạo thấy).'], [59, 84])
S3.add('Lịch sử tạo', 'P1', [PRE_FORM, 'A vừa lưu kế hoạch.'], ['Ở dòng kế hoạch bấm ba chấm > Lịch sử.'], '—',
       ['Có 1 mốc "Tạo mới", Người thực hiện A, thời điểm lưu.'], [60, 176])
S3.add('Bỏ trống mọi trường bắt buộc', 'P0', PRE_FORM, TAO + ['Bấm Lưu ngay.'], '—',
       ['Báo "Bạn chưa nhập đầy đủ thông tin.", không lưu.',
        'Lỗi đỏ CÙNG LÚC: "Kho – Vui lòng chọn kho.", "Hàng hóa – Vui lòng thêm ít nhất 1 hàng hóa." (khung bảng viền đỏ), '
        '"Thành viên – Vui lòng chọn thành viên.", "Chức vụ – Vui lòng chọn chức vụ.".', 'Cuộn tới ô lỗi đầu tiên.'], [61, 70, 80])
S3.add('Chọn kho nhưng chưa thêm hàng', 'P0', PRE_FORM, TAO + ['Chọn Kho PTT, chọn thành viên.', 'Bấm Lưu.'], '—',
       ['Chỉ báo "Hàng hóa – Vui lòng thêm ít nhất 1 hàng hóa.", khung bảng viền đỏ.'], [61, 62])
S3.add('Hội đồng trùng thành viên', 'P0', PRE_FORM, FILL + ['Bấm Thêm dòng, chọn lại Bùi Duy Trước.', 'Bấm Lưu.'], '—',
       ['Dòng 2 báo "Thành viên – Bị trùng.", không lưu.'], [62, 67])
S3.add('Xóa hết dòng hội đồng', 'P1', PRE_FORM, FILL + ['Bấm biểu tượng thùng rác ở dòng hội đồng.', 'Bấm Lưu.'], '—',
       ['Bảng hội đồng hiện "Không có dữ liệu", báo "Hội đồng kiểm kê – Vui lòng thêm ít nhất 1 thành viên.".'], 61)
S3.add('Chọn thành viên tự điền chức vụ', 'P1', PRE_FORM, TAO + ['Chọn Thành viên = Bùi Duy Trước.', 'Bỏ chọn thành viên.'], '—',
       ['Bước 1: ô Chức vụ tự điền chức vụ đầu tiên của nhân viên.', 'Bước 2: ô Chức vụ bị xóa.'], 53)
S3.add('Ghi chú đúng 255 ký tự', 'P1', PRE_FORM, FILL + ['Dán 255 ký tự vào Ghi chú.', 'Bấm Lưu.'], 'Ghi chú: 255 ký tự',
       ['Lưu thành công, Ghi chú đủ 255 ký tự.'], [64, 65])
S3.add('Ghi chú vượt 255 ký tự', 'P1', PRE_FORM, TAO + ['Dán 300 ký tự vào Ghi chú.'], 'Ghi chú: 300 ký tự',
       ['Ô chỉ nhận 255 ký tự đầu (không gõ thêm được); nếu vượt vẫn bị chặn "Ghi chú – Tối đa 255 ký tự.".'], [65, 66])
S3.add('Ghi chú có ký tự đặc biệt, tiếng Việt, khoảng trắng', 'P2', PRE_FORM,
       FILL + ['Nhập Ghi chú "  Kiểm kê <Kho 1> & \'đợt 2\'  ".', 'Bấm Lưu.'], '—',
       ['Lưu thành công, Ghi chú hiển thị đúng ký tự đã nhập, tiếng Việt có dấu đầy đủ, không lỗi giao diện.',
        'Lưu ý: hệ thống bỏ khoảng trắng đầu / cuối theo quy tắc chung.'], [63, 68, 69, 81])
S3.add('Lỗi biến mất sau khi sửa', 'P1', 'Đang có lỗi đỏ ở TC_03.011.', ['Chọn Kho PTT.', 'Thêm hàng Máy tính xách tay.', 'Chọn thành viên.'],
       '—', ['Lỗi Kho, Hàng hóa, Thành viên, Chức vụ lần lượt biến mất ngay khi sửa đúng.'], 71)
S3.add('Trùng dữ liệu: 2 kế hoạch cùng kho, cùng hàng', 'P1', [PRE_FORM, KH1],
       FILL + ['Bấm Lưu.'], FULL, ['Lưu được; 2 kế hoạch có số phiếu khác nhau (không có trường duy nhất).'], [67, 75, 82])
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, FILL + ['Bấm Lưu và tiếp tục.'], FULL,
       ['Báo "Lưu thành công.", VẪN ở màn Tạo.', 'Form trắng: Kho trống, Ghi chú trống, Hàng hóa trống, Hội đồng 1 dòng trống.',
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
S3.add('Nhập rồi trả về như ban đầu', 'P2', PRE_FORM, TAO + ['Nhập Ghi chú "abc".', 'Xóa hết chữ vừa nhập.', 'Bấm Quay lại.'],
       '—', ['Không hỏi "Thông tin chưa lưu" (dữ liệu như lúc mở).'], [98, 99])
S3.add('Không thao tác lâu', 'P2', PRE_FORM, FILL + ['Để yên 30 phút.', 'Bấm Lưu.'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên, chuyển về đăng nhập, không lưu.'], 100)
S3.add('Bấm Lưu liên tục', 'P0', PRE_FORM, FILL + ['Bấm Lưu 3 lần thật nhanh.'], FULL,
       ['Chỉ tạo 1 kế hoạch (nút khóa trong lúc lưu).'], 101)
S3.add('Tạo đồng thời ở 2 tab', 'P1', PRE_FORM, ['Mở 2 tab màn Tạo, nhập cùng dữ liệu.', 'Bấm Lưu ở cả 2 tab.'], FULL,
       ['Tạo 2 kế hoạch, số phiếu khác nhau, không lỗi.'], 102)
S3.add('Thêm hàng hóa khi chưa chọn kho', 'P0', PRE_FORM, TAO + ['Bấm Thêm hàng hóa.'], '—',
       ['Báo "Vui lòng chọn kho trước khi thêm hàng hóa.", lỗi đỏ "Kho – Vui lòng chọn kho." dưới ô Kho; không mở popup.'], [61, 62])
S3.add('Popup chỉ hiện hàng còn tồn kho kế toán', 'P0', PRE_FORM, TAO + ['Chọn Kho PTT.', 'Bấm Thêm hàng hóa.'], '—',
       ['Mở popup "Thêm hàng hóa": ô tìm, cây phân loại, bảng STT, Ảnh, Mã hàng, Tên hàng hoá, Model, Thương hiệu, Loại sản phẩm, '
        'ĐVT, Tồn bán được.', 'Chỉ liệt kê hàng có tồn kho kế toán > 0 trong kho PTT (có Máy tính xách tay).',
        'Chân popup: "Đã chọn 0 hàng hoá", nút Thêm (0) mờ, Đóng.'], [53, 269])
S3.add('Thêm hàng ra đúng tồn theo kho kế toán', 'P0', PRE_FORM,
       TAO + ['Chọn Kho PTT.', 'Bấm Thêm hàng hóa, tick Máy tính xách tay và MẶT NẠ BẢO VỆ, bấm Thêm (2).'], '—',
       ['Báo "Thêm thành công.".', 'Máy tính xách tay: mỗi kho kế toán có tồn 1 dòng (PTT01 - Phan Trọng Tuệ - Hàng bán …), Tổng SL '
        '= cộng các dòng; các ô STT, Tên hàng, Model, Mã hàng, ĐVT, Tổng SL gộp ô.', 'Số hiển thị dạng 1,234.'], [58, 269])
S3.add('Thêm hàng đã có trong bảng', 'P1', 'Bảng đã có Máy tính xách tay.', ['Bấm Thêm hàng hóa, bấm vào tên Máy tính xách tay.'], '—',
       ['Hàng được đánh dấu đã có trong popup; nếu vẫn chọn thì báo "Hàng hóa đã được chọn.", không thêm dòng.'], [67, 62])
S3.add('Thêm hàng không còn tồn', 'P1', [PRE_FORM, 'Hàng X vừa xuất hết tồn kho kế toán ở PTT sau khi mở popup.'],
       ['Tick X trong popup, bấm Thêm (1).'], '—',
       ['Báo "Hàng hóa không còn tồn kho kế toán trong kho đã chọn: <mã X>.", không thêm.'], [268, 61])
S3.add('Đổi kho khi đã có hàng: Hủy', 'P0', 'Đang ở màn Tạo, đã thêm 2 hàng ở kho PTT.', ['Chọn thêm Kho LN - Liên Ninh.', 'Bấm Hủy.'],
       '—', ['Hiện hộp "Đổi kho": "Đổi kho sẽ xóa danh sách hàng hóa đã chọn. Bạn có muốn tiếp tục?".',
             'Bấm Hủy: ô Kho trở lại chỉ PTT, 2 hàng giữ nguyên.'], 53)
S3.add('Đổi kho khi đã có hàng: Đổi kho', 'P1', 'Đang ở màn Tạo, đã thêm 2 hàng ở kho PTT.', ['Đổi Kho = LN - Liên Ninh.', 'Bấm Đổi kho.'],
       '—', ['Bảng Hàng hóa bị xóa hết; Kho = Liên Ninh.'], [53, 283])
S3.add('Làm mới số liệu', 'P0', 'Đang ở màn Tạo, đã thêm 2 hàng ở kho PTT; sau đó tồn Máy tính xách tay thay đổi.',
       ['Bấm Làm mới số liệu.'], '—',
       ['Báo "Làm mới số liệu thành công.", SL tồn từng kho kế toán + Tổng SL đổi theo tồn hiện tại.', 'Chưa lưu; phải bấm Lưu mới ghi.'],
       [53, 286])
S3.add('Làm mới số liệu bỏ hàng hết tồn', 'P1', 'Bảng có 2 hàng; MẶT NẠ BẢO VỆ đã hết tồn kho kế toán ở PTT.', ['Bấm Làm mới số liệu.'],
       '—', ['Báo "Làm mới số liệu thành công. Đã bỏ 1 hàng hóa hết tồn.", bảng còn 1 hàng.'], [53, 286])
S3.add('Làm mới số liệu khi bảng trống', 'P2', PRE_FORM, TAO, '—', ['Nút Làm mới số liệu mờ, không bấm được.'], 53)
S3.add('Bỏ một hàng khỏi bảng', 'P1', 'Bảng có 2 hàng.', ['Bấm thùng rác ở dòng MẶT NẠ BẢO VỆ.'], '—', ['Dòng bị bỏ ngay, không hỏi.'], 53)

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
PRE_E = [ACC_A, KH1]
EDIT = ['Đăng nhập A.', MENU, 'Ở dòng KH1 bấm Sửa (bút chì).']
S4.add('Mở màn Sửa', 'P0', PRE_E, EDIT, '—', ['Mở TRANG "Sửa kế hoạch kiểm kê theo hàng hóa: <số phiếu KH1>".'], 103)
S4.add('Dữ liệu điền đúng', 'P0', PRE_E, EDIT, '—',
       ['Ngày kiểm kê (đã lưu), Kho Phan Trọng Tuệ, Ghi chú, bảng Hàng hóa như lúc lưu, hội đồng Bùi Duy Trước + chức vụ.'], 104)
S4.add('Trường được / không được sửa', 'P0', PRE_E, EDIT, '—',
       ['Không sửa được: Ngày kiểm kê (ô khóa); không có ô Số phiếu.', 'Sửa được: Kho, Ghi chú, hàng hóa, hội đồng.'], 105)
S4.add('Các nút ở màn Sửa', 'P1', PRE_E, EDIT, '—', ['Có Lưu, Lưu và kiểm, Quay lại; KHÔNG có Lưu và tiếp tục.'], 106)
S4.add('Sửa một trường', 'P0', PRE_E, EDIT + ['Sửa Ghi chú thành "Đợt 2".', 'Bấm Lưu.'], 'Ghi chú: Đợt 2',
       ['Báo "Lưu thành công.", về danh sách; trạng thái vẫn Đang tạo.'], [107, 69])
S4.add('Sửa nhiều trường', 'P0', PRE_E, EDIT + ['Thêm hàng MẶT NẠ BẢO VỆ.', 'Thêm dòng hội đồng mới.', 'Bấm Lưu.'],
       '—', ['Lưu thành công; kế hoạch có 2 hàng và 2 thành viên hội đồng.'], [108, 110])
S4.add('Giữ nguyên giá trị khi lưu không đổi', 'P1', PRE_E, EDIT + ['Không đổi gì, bấm Lưu.'], '—',
       ['Lưu thành công, không báo trùng chính kế hoạch.'], [109, 68])
S4.add('Ngày kiểm kê, ngày / người cập nhật', 'P1', [ACC_A, 'KH1 lưu ngày 01/11/2026.'], EDIT + ['Sửa Ghi chú, bấm Lưu ngày 05/11/2026.',
                                                                                              'Xem dòng KH1 ở danh sách.'], '—',
       ['Ngày cập nhật = thời điểm lưu, Người cập nhật = A.', 'Ngày kiểm kê trên phiếu chi tiết đổi thành 05/11/2026 (hệ thống ghi '
        'ngày lưu).'], 111)
S4.add('Lịch sử sửa', 'P0', PRE_E, EDIT + ['Sửa Ghi chú, thêm 1 hàng, bấm Lưu.', 'Mở Lịch sử của KH1.'], '—',
       ['Có mốc "Thay đổi thông tin", ghi Ghi chú cũ > mới và Danh sách hàng hóa có thêm dòng (Mã hàng, Kho kế toán, SL tồn).'],
       [112, 177, 178])
S4.add('Bỏ trống bắt buộc khi sửa', 'P0', PRE_E, EDIT + ['Bỏ chọn thành viên hội đồng.', 'Bấm Lưu.'], '—',
       ['"Thành viên – Vui lòng chọn thành viên." dưới ô, "Bạn chưa nhập đầy đủ thông tin.", không lưu.'], [113, 117])
S4.add('Vượt giới hạn khi sửa', 'P2', PRE_E, EDIT + ['Dán 300 ký tự vào Ghi chú.'], '—',
       ['Ô Ghi chú chỉ nhận 255 ký tự; Kho, Thành viên, Chức vụ là ô chọn nên không có định dạng sai.'], [114, 115])
S4.add('Trùng bản ghi khác khi sửa', 'P2', [ACC_A, KH1, 'Có kế hoạch khác cùng kho, cùng hàng.'], EDIT + ['Bấm Lưu.'], '—',
       ['Lưu được (kế hoạch không có trường duy nhất).'], 116)
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P1', 'Đang có lỗi "Thành viên – Vui lòng chọn thành viên.".', ['Chọn lại thành viên.'], '—',
       ['Lỗi biến mất ngay.'], 118)
S4.add('Mở Sửa rồi Quay lại không đổi', 'P1', PRE_E, EDIT + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], [119, 125])
S4.add('Đổi rồi trả về ban đầu', 'P2', PRE_E, EDIT + ['Sửa Ghi chú rồi gõ lại đúng nội dung cũ.', 'Bấm Quay lại.'], '—',
       ['Không hỏi "Thông tin chưa lưu".'], 120)
S4.add('Rời màn khi đã đổi', 'P0', PRE_E, EDIT + ['Sửa Ghi chú.', 'Bấm Quay lại.'], '—', ['Hiện hộp "Thông tin chưa lưu".'], 121)
S4.add('Xác nhận Thoát', 'P1', 'Đang ở hộp "Thông tin chưa lưu" của màn Sửa.', ['Bấm Thoát.'], '—',
       ['Về danh sách; KH1 không đổi; lịch sử không có mốc mới.'], [122, 124, 125])
S4.add('Xác nhận Ở lại', 'P2', 'Đang ở hộp "Thông tin chưa lưu" của màn Sửa.', ['Bấm Ở lại.'], '—', ['Ở lại màn Sửa, dữ liệu đã đổi giữ nguyên.'], 123)
S4.add('Sửa kế hoạch đã Đang kiểm', 'P0', [ACC_A, KH2], ['Đăng nhập A.', MENU, 'Quan sát dòng KH2.', 'Mở đường link màn Sửa của KH2 từ lịch sử trình duyệt.'],
       '—', ['Dòng KH2 không có nút Sửa.', 'Mở màn Sửa tự chuyển sang màn chi tiết KH2.'], [126, 63])
S4.add('Kế hoạch bị xóa ở tab khác', 'P1', PRE_E, ['Tab 1 mở màn Sửa KH1.', 'Tab 2 xóa KH1.', 'Tab 1 bấm Lưu.'], '—',
       ['Báo "Không tìm thấy kế hoạch kiểm kê hoặc bạn không có quyền xem.", không lưu.'], [127, 138])
S4.add('Kế hoạch vừa chuyển Đang kiểm ở tab khác', 'P0', PRE_E, ['Tab 1 mở màn Sửa KH1.', 'Tab 2 mở Sửa KH1, bấm Lưu và kiểm.', 'Tab 1 bấm Lưu.'],
       '—', ['Tab 1 báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang", không lưu.'], [128, 91])
S4.add('Người khác không sửa được', 'P0', [ACC_B, KH1], ['Đăng nhập B.', MENU, 'Tìm KH1.'], '—',
       ['B không thấy KH1 (Đang tạo chỉ người tạo thấy) nên không sửa được.'], [128, 63])
S4.add('Kế hoạch đã có phiếu kiểm kê', 'P1', [PRE_LIST, P20], [MENU, 'Quan sát dòng TPE.KHKKHH-00020.'], '—',
       ['Không có nút Sửa, Xóa (kế hoạch đã Đã lập phiếu kiểm kê).'], 129)
S4.add('Kho đã khóa vẫn hiện ở màn Sửa', 'P2', [ACC_A, KH1, 'Kho Phan Trọng Tuệ bị ngừng hoạt động sau khi lưu KH1.'], EDIT, '—',
       ['Ô Kho vẫn hiện kho Phan Trọng Tuệ (mã PTT).', 'Ở màn Tạo mới kho này không còn để chọn.'], [276, 284])

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
S5.add('Không xóa được kế hoạch đang dùng', 'P0', [ACC_A, KH2, P20], ['Đăng nhập A.', MENU], '—',
       ['KH2 và TPE.KHKKHH-00020 không có nút Xóa (đã Đang kiểm / đã có phiếu kiểm kê).'], [135, 137, 270])
S5.add('Xóa kế hoạch có dữ liệu con', 'P1', [ACC_A, KH1, 'KH1 có 2 kho, 3 hàng, 2 thành viên hội đồng.'], ['Xóa KH1.'], '—',
       ['Xóa thành công, toàn bộ kho, hàng hóa, tồn kho kế toán, hội đồng của KH1 bị xóa theo (không còn dữ liệu mồ côi).'], [136, 285])
S5.add('Kế hoạch đã bị xóa ở tab khác', 'P1', [ACC_A, KH1], ['Tab 1, tab 2 cùng mở danh sách.', 'Tab 2 xóa KH1.', 'Tab 1 xóa KH1.'], '—',
       ['Tab 1 báo "Không tìm thấy kế hoạch kiểm kê hoặc bạn không có quyền xem.".'], 138)
S5.add('Kế hoạch vừa chuyển Đang kiểm ở tab khác', 'P1', [ACC_A, KH1], ['Tab 2 Lưu và kiểm KH1.', 'Tab 1 bấm Xóa KH1, bấm Xóa.'], '—',
       ['Báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang", không xóa.'], 138)
S5.add('Dữ liệu liên quan sau xóa', 'P1', [ACC_A, KH1, 'Kho Cát Bà chỉ có trong KH1.'], ['Xóa KH1.', 'Vào phân hệ Kho > Danh mục > Kho vật lý, xóa kho Cát Bà.'],
       '—', ['Không còn bị chặn vì KH1 (kế hoạch không còn dùng kho này).'], [141, 280])
S5.add('Lịch sử xóa', 'P2', [ACC_A, KH1], ['Xóa KH1.'], '—', ['Hệ thống ghi mốc "Xóa" cho KH1 trước khi xóa.'], 141)

# ============================================================== VI. GỬI DUYỆT (Lưu và kiểm)
S6 = Sec(6)
S6.add('Nút Lưu và kiểm', 'P0', PRE_FORM, TAO, '—', ['Nút Lưu và kiểm (màu chính, biểu tượng máy bay giấy) ở chân màn Tạo và Sửa.'], 300)
S6.add('Lưu và kiểm thành công', 'P0', [PRE_FORM, ACC_K, 'Kho PTT không có phiếu nhập / xuất kho chưa xử lý xong.'], FILL + ['Bấm Lưu và kiểm.'], FULL,
       ['KHÔNG có hộp xác nhận; báo "Lưu và kiểm thành công.", về danh sách.', 'Kế hoạch mới trạng thái Đang kiểm (nhãn vàng).'],
       [86, 92, 301, 302, 305])
S6.add('Lưu và kiểm khi thiếu bắt buộc', 'P0', PRE_FORM, TAO + ['Bấm Lưu và kiểm.'], '—',
       ['Cùng bộ lỗi như Lưu, "Bạn chưa nhập đầy đủ thông tin.", không lưu, không gửi.'], [87, 88, 303])
S6.add('Chặn khi còn phiếu chưa xử lý xong', 'P0', [PRE_FORM, PENDING_PRE], FILL + ['Bấm Lưu và kiểm.'], FULL,
       ['Hiện popup "Cảnh báo phiếu chưa xử lý xong": "Còn phiếu nhập kho / xuất kho chưa xử lý xong của hàng hóa trong kế hoạch. '
        'Vui lòng xử lý xong các phiếu dưới đây trước khi lưu và kiểm.".', 'Bảng: STT 1, Loại phiếu "Phiếu nhập kho", Số phiếu PNK-11618.',
        'Kế hoạch KHÔNG được lưu; không có thông báo lỗi khác.'], [304, 89])
S6.add('Mở phiếu treo từ popup', 'P1', 'Đang mở popup cảnh báo ở TC_06.004.', ['Bấm PNK-11618.', 'Quay lại tab cũ, bấm Đóng.'], '—',
       ['Phiếu nhập kho mở ở tab mới; tab cũ giữ form.', 'Bấm Đóng: popup đóng, dữ liệu form còn nguyên.'], [304, 310])
S6.add('Lưu thường không kiểm phiếu treo', 'P1', [PRE_FORM, PENDING_PRE], FILL + ['Bấm Lưu.'], FULL,
       ['Lưu thành công ở trạng thái Đang tạo (không hiện popup cảnh báo).'], 304)
S6.add('Kiểm phiếu treo xét mọi hàng', 'P2', [PRE_FORM, 'Chỉ hàng thứ nhất (Máy tính xách tay) có phiếu nhập kho treo.'],
       FILL + ['Thêm hàng MẶT NẠ BẢO VỆ (thứ hai).', 'Bấm Lưu và kiểm.'], '—', ['Vẫn bị chặn và liệt kê phiếu của hàng thứ nhất.'], 304)
S6.add('Gửi từ màn Sửa', 'P0', [ACC_A, KH1], ['Mở Sửa KH1.', 'Bấm Lưu và kiểm.'], '—',
       ['Báo "Lưu và kiểm thành công.", KH1 chuyển Đang kiểm; không còn nút Sửa, Xóa.'], [302, 305, 311])
S6.add('Màn sau khi Lưu và kiểm', 'P1', PRE_FORM, FILL + ['Bấm Lưu và kiểm.'], FULL,
       ['Màn Tạo đóng, về danh sách (không ở lại như Lưu và tiếp tục).'], [90, 91, 92])
S6.add('Dữ liệu sau khi Lưu và kiểm', 'P0', [PRE_FORM, 'Vừa Lưu và kiểm kế hoạch.'], ['Mở chi tiết kế hoạch vừa lưu.'], '—',
       ['Kho, ghi chú, hàng hóa, hội đồng đúng như đã nhập; danh sách ghi Đang kiểm.'], 306)
S6.add('Thông báo đến người lập phiếu kiểm kê', 'P0', [PRE_FORM, ACC_K, 'Nhân viên X công ty khác có cùng quyền.'], FILL + ['Bấm Lưu và kiểm.'],
       FULL, ['K nhận thông báo "[KHKKHH] Tạo mới: <số phiếu>", ghi chú "Người lập: <tên A>. Chờ lập phiếu kiểm kê. Ngày kiểm kê: '
              '<hôm nay>. Kho: Phan Trọng Tuệ".', 'X (khác công ty) và nhân viên không có quyền KHÔNG nhận.'], 308)
S6.add('Bấm thông báo mở kế hoạch', 'P1', [ACC_K, 'K vừa nhận thông báo.'], ['Bấm thông báo.'], '—',
       ['Mở màn chi tiết kế hoạch, có nút Lập phiếu kiểm kê theo hàng hóa.'], 309)
S6.add('Lưu thường không gửi thông báo', 'P1', [PRE_FORM, ACC_K], FILL + ['Bấm Lưu.'], FULL, ['K không nhận thông báo nào.'], 308)
S6.add('Hủy thao tác (rời màn)', 'P1', PRE_FORM, FILL + ['Bấm Quay lại, chọn Thoát.'], '—',
       ['Không có kế hoạch nào được lưu; K không nhận thông báo.'], 310)
S6.add('Không gửi lại kế hoạch đã Đang kiểm', 'P0', [ACC_A, KH2], [MENU, 'Quan sát dòng KH2.'], '—',
       ['Không có nút Sửa / Lưu và kiểm cho KH2.'], 311)
S6.add('Lịch sử khi Lưu và kiểm', 'P1', [ACC_A, KH1], ['Sửa KH1, bấm Lưu và kiểm.', 'Mở Lịch sử KH1.'], '—',
       ['Có mốc "Thay đổi trạng thái" Đang tạo > Đang kiểm, người thực hiện A, thời điểm lưu.'], [312, 92])
S6.add('Kế hoạch Đang kiểm hiện ở popup Chọn kế hoạch', 'P0', [ACC_K, KH2],
       ['Đăng nhập K.', 'Vào phân hệ Kho > Kiểm kho > Kiểm kê theo hàng hóa, bấm Tạo mới, mở ô chọn kế hoạch.'], '—',
       ['Popup chọn kế hoạch có KH2.'], [307, 274])

# ============================================================== VII. LỊCH SỬ THAY ĐỔI
S7 = Sec(7)
PRE_H = [PRE_LIST, P20]
HIS = [MENU, 'Ở dòng TPE.KHKKHH-00020 bấm Lịch sử.']
S7.add('Mở cửa sổ lịch sử', 'P0', PRE_H, HIS, '—', ['Cửa sổ "Lịch sử thay đổi: TPE.KHKKHH-00020".'], 162)
S7.add('Các thông tin của mốc', 'P0', PRE_H, HIS, '—',
       ['Mỗi mốc: thời điểm, hành động, "Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ", nội dung.'], [163, 165, 166, 167])
S7.add('Mới nhất trước', 'P0', PRE_H, HIS, '—',
       ['2 mốc: trên là 31/10/2026 09:38 Thay đổi trạng thái, dưới là 31/10/2026 09:38 Tạo mới.'], 164)
S7.add('Nội dung thay đổi trạng thái do màn khác', 'P0', PRE_H, HIS, '—',
       ['Mốc Thay đổi trạng thái: "Trạng thái: Đang kiểm > Đã lập phiếu kiểm kê", ghi chú "Lập phiếu kiểm kê TPE.KKK-01092.".'],
       [168, 281])
S7.add('Lọc theo hành động', 'P1', PRE_H, HIS + ['Bấm Bộ lọc, chọn Loại hành động = Tạo mới.'], '—', ['Chỉ còn mốc Tạo mới.'], 169)
S7.add('Lọc theo người thực hiện', 'P2', PRE_H, HIS + ['Bấm Bộ lọc, chọn Người thực hiện = DNS Admin.'], '—', ['Còn đủ 2 mốc.'], 170)
S7.add('Lọc theo thời gian', 'P1', PRE_H, HIS + ['Bấm Bộ lọc, Từ ngày 01/11/2026.'], '—', ['"Không có lịch sử phù hợp bộ lọc.".'], 171)
S7.add('Kết hợp lọc', 'P2', PRE_H, HIS + ['Chọn Loại hành động = Thay đổi trạng thái, Từ ngày 31/10/2026.'], '—', ['Còn 1 mốc.'], 172)
S7.add('Không có kết quả lọc', 'P2', PRE_H, HIS + ['Đến ngày 30/10/2026.'], '—', ['"Không có lịch sử phù hợp bộ lọc.".'], 173)
S7.add('Làm mới / đóng mở bộ lọc', 'P2', PRE_H, HIS + ['Lọc rồi bấm Làm mới.', 'Bấm Bộ lọc lần nữa.'], '—',
       ['Làm mới: hiện lại 2 mốc.', 'Bộ lọc thu gọn / mở lại.'], [174, 175])
S7.add('Kế hoạch chưa có lịch sử', 'P1', [PRE_LIST, 'TPSG.KHKKHH-00001 lập trên hệ thống cũ.'], [MENU, 'Bấm Lịch sử dòng TPSG.KHKKHH-00001.'],
       '—', ['"Chưa có lịch sử thao tác nào.".'], 162)
S7.add('Sửa không đổi gì thì không ghi', 'P1', [ACC_A, KH1], ['Sửa KH1, không đổi, bấm Lưu.', 'Mở Lịch sử.'], '—',
       ['Không có mốc "Thay đổi thông tin" mới.'], [182, 125])
S7.add('Đổi nhiều thông tin cùng lúc', 'P1', [ACC_A, KH1], ['Sửa KH1: đổi Ghi chú + hội đồng, bấm Lưu và kiểm.', 'Mở Lịch sử.'], '—',
       ['1 mốc "Thay đổi thông tin" liệt kê Ghi chú và Danh sách thành viên hội đồng kiểm kê (cũ > mới) + 1 mốc "Thay đổi trạng thái".'],
       183)
S7.add('Đóng cửa sổ', 'P1', PRE_H, HIS + ['Bấm Đóng.', 'Mở lại, bấm (x).'], '—', ['Cả 2 cách đều đóng cửa sổ.'], 184)
S7.add('Trạng thái danh sách sau khi đóng', 'P1', 'Đang ở trang 2, lọc Kho = LN - Liên Ninh, số dòng 5.', ['Mở Lịch sử 1 dòng, bấm Đóng.'], '—',
       ['Danh sách giữ trang 2, bộ lọc, sắp xếp.'], 185)
S7.add('Lịch sử ở màn chi tiết', 'P1', PRE_H, [MENU, 'Bấm TPE.KHKKHH-00020.', 'Ở khối Lịch sử bấm Xem lịch sử.'], '—',
       ['Khối Lịch sử có số 2; bấm mở rộng hiện 2 mốc như cửa sổ; nút đổi thành Thu gọn.'], [195, 162])

# ============================================================== VIII. XEM CHI TIẾT
S8 = Sec(8)
DET = [MENU, 'Bấm TPE.KHKKHH-00020.']
S8.add('Mở màn chi tiết', 'P0', PRE_H, DET, '—', ['Mở TRANG chi tiết (không phải cửa sổ nổi).'], 186)
S8.add('Tiêu đề', 'P0', PRE_H, DET, '—', ['"Chi tiết kế hoạch kiểm kê theo hàng hóa: TPE.KHKKHH-00020" (không kèm nhãn trạng thái).'], 187)
S8.add('Đầy đủ trường', 'P0', PRE_H, DET, '—',
       ['Thông tin chung: Ngày kiểm kê 31/10/2026, Kho Phan Trọng Tuệ, Ghi chú "Ghi chú"; góc phải "DNS Admin - 31/10/2026 09:38".',
        'Hàng hóa: 2 dòng (Máy tính xách tay 50, MẶT NẠ BẢO VỆ 15), kho kế toán PTT01 - Phan Trọng Tuệ - Hàng bán.',
        'Hội đồng kiểm kê: Bùi Sỹ Phú; khối Lịch sử.'], 188)
S8.add('Khớp dữ liệu tạo và danh sách', 'P0', PRE_H, DET, '—',
       ['Kho, ngày, người tạo khớp dòng ở danh sách.'], [189, 190])
S8.add('Trường chỉ đọc, không có nút Lưu', 'P0', PRE_H, DET, '—',
       ['Mọi ô khóa, không có Thêm hàng hóa, Thêm dòng, thùng rác.', 'Chân màn: In, Xuất Excel, Quay lại; không có Lưu.'],
       [191, 192])
S8.add('Làm mới số liệu ở chi tiết không lưu', 'P1', PRE_H, DET + ['Bấm Làm mới số liệu.', 'Bấm Quay lại.', 'Mở lại chi tiết.'], '—',
       ['Bước 3: số tồn đổi theo tồn hiện tại, báo "Làm mới số liệu thành công.".', 'Bước 4: về danh sách không hỏi "chưa lưu".',
        'Bước 5: số tồn trở lại 50 / 15 như đã lưu.'], [191, 286])
S8.add('Nút theo trạng thái ở chi tiết', 'P0', [ACC_A, KH1, KH2], ['Mở chi tiết KH1.', 'Mở chi tiết KH2.'], '—',
       ['KH1: Sửa, In, Xuất Excel, Xóa, Quay lại.', 'KH2: In, Xuất Excel, Quay lại.'], [193, 194])
S8.add('Quay lại giữ trang và bộ lọc', 'P0', 'Đang ở trang 2, lọc Kho = LN - Liên Ninh, số dòng 5.', ['Bấm số phiếu 1 dòng.', 'Bấm Quay lại.'], '—',
       ['Về danh sách giữ bộ lọc Kho = Liên Ninh (trong 10 phút).'], [196, 197])
S8.add('Kế hoạch ngoài phạm vi', 'P0', [ACC_B, 'TPSG.KHKKHH-00003 công ty TPSG.'], ['Đăng nhập B.', 'Mở đường link chi tiết TPSG.KHKKHH-00003.'], '—',
       ['Chuyển sang trang "Không tìm thấy trang".'], [186, 296])
S8.add('Lập phiếu kiểm kê từ màn chi tiết', 'P0', [ACC_K, KH2], ['Đăng nhập K.', 'Mở chi tiết KH2.', 'Bấm Lập phiếu kiểm kê theo hàng hóa.'], '—',
       ['Mở màn Tạo phiếu kiểm kê theo hàng hóa (phân hệ Kho) cùng tab với KH2 đã chọn sẵn: kho, hàng hóa, hội đồng; không thêm / '
        'bớt hàng được.'], [274, 193])
S8.add('Lập phiếu kiểm kê từ danh sách', 'P1', [ACC_K, KH2, 'K có thêm quyền "Tổng kiểm kê kho theo hàng hóa".'], ['Đăng nhập K.', MENU], '—',
       ['Dòng KH2 có nút Lập phiếu kiểm kê theo hàng hóa và nút ba chấm chứa Xuất Excel, Lịch sử.'], 274)
S8.add('Không có quyền thì không thấy Lập phiếu kiểm kê', 'P0', [ACC_C, KH2], ['Đăng nhập C.', 'Mở chi tiết KH2.'], '—',
       ['Không có nút Lập phiếu kiểm kê theo hàng hóa.'], [193, 295])

# ============================================================== IX. IN PHIẾU
S9 = Sec(9)
S9.add('In phiếu từ danh sách', 'P0', PRE_H, [MENU, 'Bấm In ở dòng TPE.KHKKHH-00020.'], '—',
       ['Cửa sổ "Xem trước kế hoạch kiểm kê theo hàng hóa TPE.KHKKHH-00020".',
        'Bản in: logo / tên công ty của kế hoạch, "KẾ HOẠCH KIỂM KÊ THEO MẶT HÀNG", Số phiếu, Ngày kiểm kê 31/10/2026, Kho vật lý, '
        'Ghi chú, Hội đồng kiểm kê Bùi Sỹ Phú.',
        'Bảng: STT, Tên hàng, Mã hàng, ĐVT, Kho kế toán, SL tồn, Tổng SL; chỗ ký "Ngày … Tháng … Năm …" (ngày in), Người lập DNS Admin.'],
       228)
S9.add('In phiếu từ màn chi tiết', 'P1', PRE_H, DET + ['Bấm In.'], '—', ['Cùng cửa sổ xem trước như in từ danh sách.'], 228)
S9.add('Bấm In trong cửa sổ', 'P1', 'Đang mở cửa sổ xem trước.', ['Bấm In.'], '—', ['Mở hộp thoại in của trình duyệt.'], 228)
S9.add('In danh sách theo bộ lọc', 'P0', PRE_LIST, [MENU, 'Lọc Kho = LN - Liên Ninh.', 'Bấm In danh sách.'], '—',
       ['Cửa sổ "Xem trước danh sách kế hoạch kiểm kê theo hàng hóa".',
        'Bảng 10 dòng: STT, Số phiếu, Ngày kiểm kê (kèm giờ), Kho, Người tạo, Trạng thái; khối ký "Ngày … Tháng … Năm …", Người lập.'],
       [220, 227])
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
S10.add('Kéo thả thứ tự', 'P1', PRE_LIST, ['Kéo Trạng thái xuống sau Người cập nhật, bấm Lưu.'], '—', ['Bảng hiện Trạng thái sau Người cập nhật.'], 204)
S10.add('Chọn tất cả / Bỏ chọn hết', 'P2', PRE_LIST, ['Bấm Bỏ chọn hết.', 'Bấm Chọn tất cả.'], '—',
       ['Bỏ chọn hết: còn 3 cột khóa.', 'Chọn tất cả: 10/10.'], 202)
S10.add('Đóng không lưu', 'P1', PRE_LIST, ['Bỏ tích Kho, bấm Đóng.'], '—', ['Bảng vẫn có cột Kho.'], 207)
S10.add('Ghi nhớ sau F5 và theo tài khoản', 'P1', 'A đã ẩn cột Ngày cập nhật.', ['Nhấn F5.', 'Đăng nhập B trên cùng máy.'], '—',
       ['A: vẫn ẩn sau F5 và đăng nhập máy khác.', 'B: thấy đủ 10 cột.'], [208, 209])
S10.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', 'Đang lọc Kho = LN - Liên Ninh (10).', ['Ẩn cột Kho, bấm Lưu.'], '—',
       ['Vẫn 10 kế hoạch, bộ lọc giữ nguyên.'], [210, 211])

# ============================================================== XI. XUẤT DANH SÁCH EXCEL
S11 = Sec(11)
S11.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất Excel" với 8 trường: Số phiếu, Ngày kiểm kê, Kho, Trạng thái, Người tạo, Ngày tạo, Ngày cập nhật, '
        'Người cập nhật; tích sẵn theo cột đang hiện ("Đang chọn 8/8 trường").'], [212, 213, 214])
S11.add('Xuất trường mặc định', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel, bấm Xuất file.'], '—',
       ['Tải "danh_sach_ke_hoach_kiem_ke_theo_hang_hoa.xlsx", báo "Xuất Excel thành công.".',
        'File: letterhead, "DANH SÁCH KẾ HOẠCH KIỂM KÊ THEO HÀNG HÓA", cột STT + 8 trường, 20 dòng, khối ký.'], [215, 216, 223, 224, 225, 227])
S11.add('Xuất một số trường theo thứ tự kéo', 'P1', PRE_LIST, ['Bỏ chọn hết, tích Kho rồi Số phiếu, kéo Kho lên đầu, Xuất file.'], '—',
       ['File chỉ có STT, Kho, Số phiếu theo đúng thứ tự.'], [217, 226])
S11.add('Không chọn trường', 'P1', PRE_LIST, ['Bấm Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S11.add('Xuất theo tìm kiếm / bộ lọc', 'P0', PRE_LIST, ['Lọc Kho = LN - Liên Ninh, Ngày kiểm kê 01/10/2026 – 31/10/2026.', 'Xuất file.'],
       '—', ['File chỉ có 10 kế hoạch khớp; có dòng "Từ ngày 01/10/2026 đến ngày 31/10/2026".'], [219, 220])
S11.add('Xuất nhiều trang', 'P1', PRE_LIST, ['Đang ở trang 1 (10 dòng), Xuất file.'], '—', ['File có đủ 20 dòng, không chỉ trang đang xem.'], 221)
S11.add('Danh sách rỗng', 'P2', 'Bộ lọc không ra kế hoạch nào.', ['Xuất file.'], '—',
       ['Vẫn ra file có tiêu đề, dòng tên cột, khối ký, không có dòng dữ liệu.'], 222)
S11.add('Dữ liệu khớp, định dạng ngày và tiếng Việt', 'P1', [PRE_LIST, P20], ['Xuất file, mở dòng TPE.KHKKHH-00020.'], '—',
       ['Ngày kiểm kê "31/10/2026 09:38" giữ dạng chữ; Kho "Phan Trọng Tuệ", Trạng thái "Đã lập phiếu kiểm kê" đủ dấu tiếng Việt.'],
       [228, 229, 230])
S11.add('Xuất Excel 1 kế hoạch', 'P0', PRE_H, [MENU, 'Bấm Xuất Excel ở dòng TPE.KHKKHH-00020.'], '—',
       ['Tải "ke_hoach_kiem_ke_theo_mat_hang_TPE-KHKKHH-00020.xlsx", báo "Xuất Excel thành công.".',
        'File: "KẾ HOẠCH KIỂM KÊ THEO MẶT HÀNG", Số phiếu, Ngày kiểm kê, Kho vật lý, Hội đồng kiểm kê, Ghi chú, bảng 7 cột như bản in '
        '(số là ô số), "Nhận xét, đánh giá:", khối ký Hội đồng kiểm kê / Trưởng bộ phận kho.'], [223, 228, 293])

# ============================================================== XII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S12 = Sec(12)
S12.add('Chỉ kế hoạch Đang kiểm hiện ở popup Chọn kế hoạch', 'P0', [ACC_K, KH1, KH2],
       ['Đăng nhập K.', 'Vào phân hệ Kho > Kiểm kho > Kiểm kê theo hàng hóa, bấm Tạo mới, mở ô chọn kế hoạch.'], '—',
       ['Popup có KH2; không có KH1 (Đang tạo) và các kế hoạch Đã lập phiếu kiểm kê.'], [274, 276])
S12.add('Lập phiếu kiểm kê đổi trạng thái kế hoạch', 'P0', [ACC_K, KH2], ['Lập và lưu phiếu kiểm kê từ KH2.', 'Mở danh sách kế hoạch.'], '—',
       ['KH2 chuyển Đã lập phiếu kiểm kê (xanh dương); Ngày / Người cập nhật đổi; lịch sử có mốc Thay đổi trạng thái kèm mã phiếu '
        'kiểm kê.'], [281, 284])
S12.add('Xóa phiếu kiểm kê không trả kế hoạch về', 'P1', [ACC_K, 'KH2 Đã lập phiếu kiểm kê, phiếu kiểm kê còn xóa được.'],
       ['Xóa phiếu kiểm kê.', 'Mở danh sách kế hoạch.'], '—', ['KH2 vẫn Đã lập phiếu kiểm kê, không lập lại phiếu từ KH2 được.'], [281, 284])
S12.add('Bộ lọc màn liên quan cập nhật', 'P2', [ACC_K, KH2], ['Sau khi KH2 Đã lập phiếu kiểm kê, mở lại popup Chọn kế hoạch.'], '—',
       ['KH2 không còn trong popup.'], 282)
S12.add('Lưu phiếu kiểm kê khi kế hoạch đã đổi trạng thái', 'P1', [ACC_K, KH2], ['Tab 1 mở Tạo phiếu kiểm kê từ KH2.', 'Tab 2 lập phiếu từ KH2 xong.',
                                                                               'Tab 1 bấm Lưu.'], '—',
       ['Tab 1 báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang".'], 282)
S12.add('Liên kết từ phiếu kiểm kê mở kế hoạch', 'P1', [ACC_K, 'Phiếu kiểm kê TPE.KKK-01092 lập từ TPE.KHKKHH-00020.'],
       ['Mở chi tiết phiếu kiểm kê TPE.KKK-01092.', 'Bấm số kế hoạch.'], '—', ['Mở chi tiết TPE.KHKKHH-00020 ở tab mới.'], [272, 279])
S12.add('Không xóa được kho vật lý đang dùng', 'P0', [ACC_A, KH2], ['Vào phân hệ Kho > Danh mục > Kho vật lý, xóa kho Phan Trọng Tuệ.'], '—',
       ['Hệ thống chặn xóa vì kho đang được dùng.'], 270)
S12.add('Đổi tên hàng không đổi kế hoạch', 'P1', [ACC_A, KH2], ['Đổi tên hàng Máy tính xách tay ở danh mục.', 'Mở chi tiết KH2.'], '—',
       ['Bảng Hàng hóa vẫn ghi tên như lúc lưu kế hoạch (lưu cố định).'], [272, 278])
S12.add('Số tồn là ảnh chụp', 'P1', [ACC_A, KH1], ['Nhập thêm 10 Máy tính xách tay vào kho PTT.', 'Mở chi tiết KH1.'], '—',
       ['SL tồn trên KH1 không đổi; chỉ đổi khi Sửa, bấm Làm mới số liệu rồi Lưu.'], [286, 269])
S12.add('Kế hoạch mới xuất hiện ở màn liên quan', 'P1', [ACC_K, PRE_FORM], ['A tạo và Lưu và kiểm kế hoạch.', 'K mở popup Chọn kế hoạch.'],
       '—', ['Kế hoạch mới có trong popup.'], 274)
S12.add('Tồn kho không đổi khi lưu kế hoạch', 'P0', PRE_FORM, ['Ghi tồn Máy tính xách tay tại kho PTT.', 'Tạo và Lưu và kiểm kế hoạch.', 'Xem lại tồn.'],
       '—', ['Tồn không đổi (kế hoạch không ghi tồn).'], 286)
S12.add('Phiếu nhập kho xử lý xong thì Lưu và kiểm được', 'P1', [PRE_FORM, PENDING_PRE], ['Hoàn tất phiếu PNK-11618.', 'Quay lại form, bấm Lưu và kiểm.'],
       '—', ['Lưu và kiểm thành công.'], [280, 283])

# ============================================================== XIII. PHÂN QUYỀN (cuối)
S13 = Sec(13)
S13.add('Quyền tổng công ty: xem mọi kế hoạch', 'P0', [ACC_T, '20 kế hoạch không Đang tạo thuộc TPE (17) và TPSG (3).'], ['Đăng nhập T.', MENU], '—',
        ['Thấy đủ 20 kế hoạch; có ô Công ty – Phòng ban, chọn được mọi công ty.'], [287, 299])
S13.add('Quyền công ty: chỉ công ty mình + của mình', 'P0', [ACC_C, 'TPE có 17 kế hoạch, TPSG 3.'], ['Đăng nhập C.', MENU], '—',
        ['Chỉ thấy 17 kế hoạch TPE (và kế hoạch C tự tạo); ô Công ty khóa ở TPE.'], [287, 299])
S13.add('Không quyền: chỉ kế hoạch mình tạo', 'P0', [ACC_A, 'A tạo 2 kế hoạch.'], ['Đăng nhập A.', MENU], '—',
        ['Chỉ thấy 2 kế hoạch của A; không có ô Công ty – Phòng ban.'], [287, 299])
S13.add('Đang tạo chỉ người tạo thấy', 'P0', [ACC_T, KH1], ['Đăng nhập T.', MENU, 'Tìm số phiếu KH1.'], '—',
        ['T không thấy KH1 dù có quyền tổng công ty.'], [287, 299])
S13.add('Xem chi tiết theo phạm vi', 'P0', [ACC_C, 'TPSG.KHKKHH-00003 công ty TPSG.'], ['Đăng nhập C.', 'Mở đường link chi tiết TPSG.KHKKHH-00003.'], '—',
        ['Trang "Không tìm thấy trang".'], [288, 296])
S13.add('Có quyền Lập phiếu xem kế hoạch Đang kiểm', 'P0', [ACC_K, KH2], ['Đăng nhập K.', 'Mở chi tiết KH2 từ thông báo.'], '—',
        ['Mở được (ngoại lệ cho người có quyền "%s").' % Q1], 288)
S13.add('Thêm mới không cần quyền', 'P0', ACC_B, ['Đăng nhập B.', MENU, 'Bấm Tạo mới, nhập đủ, bấm Lưu.'], FULL, ['Lưu thành công.'], 289)
S13.add('Sửa chỉ người tạo', 'P0', [ACC_T, 'Kế hoạch KH5 Đang tạo do T tạo, KH2 do A tạo.'], ['Đăng nhập T.', MENU], '—',
        ['KH5 có Sửa; KH2 không có Sửa (không phải người tạo, không Đang tạo).'], [290, 295])
S13.add('Xóa chỉ người tạo', 'P0', [ACC_T, 'KH5 Đang tạo do T tạo.'], ['Đăng nhập T.', MENU], '—',
        ['Chỉ KH5 có nút Xóa.'], [291, 295])
S13.add('Xuất / In / Lịch sử theo phạm vi', 'P1', ACC_A, ['Đăng nhập A.', MENU, 'Xuất Excel; mở Lịch sử 1 kế hoạch của A.'], '—',
        ['File chỉ chứa kế hoạch của A; lịch sử xem được.'], [293, 294])
S13.add('Lập phiếu kiểm kê cần quyền', 'P0',
        [ACC_K, KH2, 'Tài khoản C không có quyền "%s".' % Q1],
        ['Đăng nhập K, mở chi tiết KH2.', 'Đăng nhập C, mở chi tiết KH2.'], '—',
        ['K: có nút Lập phiếu kiểm kê theo hàng hóa.', 'C: không có nút.'], [295, 287])
S13.add('Mở đường link màn Sửa khi không phải người tạo', 'P0', [ACC_C, 'KH6 Đang kiểm công ty TPE do A tạo.'],
        ['Đăng nhập C.', 'Mở đường link màn Sửa của KH6.'], '—', ['Tự chuyển sang màn chi tiết KH6, không sửa được.'], 296)
S13.add('Thao tác bị chặn lại ở máy chủ', 'P1', [ACC_A, KH1], ['Tab 1 mở danh sách.', 'Tab 2 Lưu và kiểm KH1.', 'Tab 1 bấm Xóa KH1.'], '—',
        ['Báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang"; máy chủ kiểm lại điều kiện ở từng thao tác, không dựa vào việc ẩn nút.'],
        297)
S13.add('Đổi quyền giữa thao tác', 'P1', [ACC_C, 'Quản trị gỡ quyền "Tổng kiểm kê kho theo hàng hóa" của C khi C đang ở danh sách.'],
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
    build_chuan(output_file=OUT, sheet_name='Trang tính1', feature_name='Kế hoạch kiểm kê theo hàng hóa - Cập nhật ngày 05/11/2026',
                module_name='Kế hoạch kiểm kê theo hàng hóa', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

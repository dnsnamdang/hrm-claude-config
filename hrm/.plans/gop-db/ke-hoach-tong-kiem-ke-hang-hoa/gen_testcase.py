# -*- coding: utf-8 -*-
"""Testcase màn "Kế hoạch tổng kiểm kê hàng hóa" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (không phải danh mục) — lý do từ code: màn là chứng từ có số phiếu tự sinh <mã công ty>.KHTKK-NNNNN
(SelfInventoryRequestAll::generateCode), vòng đời trạng thái Đang tạo > Đã duyệt (SelfInventoryRequestAll::STATUSES), Thêm / Sửa / Xóa
theo trạng thái + người tạo, Lưu và duyệt (chuyển trạng thái + thông báo), In phiếu (mẫu in), lịch sử; không có Khóa / Mở khóa như danh mục.
Nhóm theo đúng tên + thứ tự chuẩn loại 'phieu' (check_tc.THU_TU), bỏ nhóm màn không có (kiểm code 05/11/2026: không có route / nút
Khóa, Gửi duyệt riêng, Không duyệt, Hủy, Import):
I Hiển thị · II Tìm kiếm & lọc (gồm Cài đặt bộ lọc) · III Thêm mới (Lưu nháp, Lưu và tiếp tục, rời màn) · IV Chỉnh sửa · V Xóa ·
VI Duyệt phiếu (Lưu và duyệt > Đã duyệt, thông báo) · VII Lịch sử · VIII Xem chi tiết (gồm Lập phiếu kiểm kê hàng hóa) · IX In phiếu
(kèm In danh sách) · X Tùy chỉnh cột · XI Xuất danh sách Excel · XII Ràng buộc · XIII Phân quyền.
Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../ke-hoach-kiem-ke-theo-hang-hoa/gen_testcase.py (05/11, qua check_tc 0 lỗi).
Nguồn hành vi (đọc 05/11/2026, nhánh develop): FE pages/finance/self-inventory-request-alls/**; BE Modules/Finance SelfInventoryRequestAll*
(Entity / Service / WriteService / Controller / StoreRequest / PrintService), SelfInventoryService, SelfInventoryWriteService,
SelfInventoryReportService.
Số liệu mẫu: dev-hrm 05/11/2026 (DNS Admin) 5 kế hoạch TPE.KHTKK-00001 … 00005, cả 5 Đã duyệt; 00003 có 4 mốc lịch sử.
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
MENU = 'Vào phân hệ Tài chính > menu "Kiểm kê" > bấm "Kế hoạch tổng kiểm kê hàng hóa".'
TAO = [MENU, 'Bấm "Tạo mới".']
ADV = 'Bấm Tìm kiếm nâng cao.'
Q1 = 'Lập phiếu kiểm kê kho theo hàng hóa'
LAP = 'Lập phiếu kiểm kê hàng hóa'
REQ = '"Bắt buộc phải nhập"'
CONFLICT = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'
NOTFOUND = '"Không tìm thấy kế hoạch tổng kiểm kê hoặc bạn không có quyền xem."'

ACC_A = 'Tài khoản A: nhân viên công ty TPE, không có quyền xem theo cấp; là người lập kế hoạch.'
ACC_B = 'Tài khoản B: nhân viên công ty TPE, không có quyền xem theo cấp, không phải người tạo.'
ACC_C = 'Tài khoản C: có quyền "Tổng kiểm kê kho theo hàng hóa", thuộc công ty TPE.'
ACC_T = 'Tài khoản T: có quyền "Tổng kiểm kê kho theo hàng hóa - tổng công ty".'
ACC_K = 'Tài khoản K: nhân viên công ty TPE, có quyền "%s", không có quyền xem theo cấp.' % Q1
PRE_LIST = ('Tài khoản DNS Admin (Super admin); trong phạm vi xem có 12 kế hoạch: 5 kế hoạch Đã duyệt TPE.KHTKK-00001 … 00005 và '
            '7 kế hoạch Đang tạo do DNS Admin lưu nháp để thử.')
P5 = ('Kế hoạch TPE.KHTKK-00005: Ngày kiểm kê 07/11/2026 - 07/11/2026; Kho Chăm sóc khách hàng, Kho Dự án trọng điểm, Hải Phòng; '
      'Công ty thuê kho TPE, TPV; Thành phần tham gia Ban Điều hành, BAN ĐIỀU HÀNH, Ban giám đốc CN Hải Phòng; Nội dung yêu cầu '
      '"test 1uuq2yi"; Đã duyệt; Người tạo DNS Admin; Ngày tạo 05/11/2026 15:08; Ngày cập nhật 05/11/2026 15:11.')
P3 = ('Kế hoạch TPE.KHTKK-00003: Đã duyệt, Ngày kiểm kê 21/10/2026 - 22/10/2026, kho Chăm sóc khách hàng; 4 mốc lịch sử: Tạo mới '
      '26/10/2026 15:21, Thay đổi thông tin 26/10/2026 15:22, Thay đổi thông tin + Thay đổi trạng thái 27/10/2026 15:55.')
PRE_FORM = ACC_A + '\nCông ty TPE có kho CSKH - Chăm sóc khách hàng và HP - Hải Phòng đang hoạt động, có kho kế toán.'
KH1 = ('Kế hoạch KH1 trạng thái Đang tạo do A tạo: Ngày kiểm kê 10/11/2026 - 12/11/2026, kho Chăm sóc khách hàng, công ty thuê '
       'kho TPE, thành phần tham gia BAN ĐIỀU HÀNH, nội dung "Tổng kiểm kê cuối năm".')
KH2 = 'Kế hoạch KH2 trạng thái Đã duyệt do A tạo, Ngày kiểm kê từ = ngày mai, kho Chăm sóc khách hàng.'
KH3 = 'Kế hoạch KH3 trạng thái Đã duyệt, Ngày kiểm kê từ = hôm qua (đợt kiểm đã bắt đầu).'
FILL = TAO + ['Chọn Ngày kiểm kê từ 10/11/2026, Ngày kiểm kê đến 12/11/2026.',
              'Chọn Kho = CSKH - Chăm sóc khách hàng.',
              'Chọn Thành phần tham gia = BDH - BAN ĐIỀU HÀNH.',
              'Nhập Nội dung yêu cầu "Tổng kiểm kê cuối năm".']
FULL = ['Ngày kiểm kê từ: 10/11/2026', 'Ngày kiểm kê đến: 12/11/2026', 'Kho: CSKH - Chăm sóc khách hàng',
        'Công ty thuê kho: tự chọn', 'Thành phần tham gia: BDH - BAN ĐIỀU HÀNH', 'Nội dung yêu cầu: Tổng kiểm kê cuối năm']
DATES = TAO + ['Chọn Ngày kiểm kê từ 10/11/2026, Ngày kiểm kê đến 12/11/2026.']
OK_DRAFT = 'Báo "Thêm mới thành công.", về màn danh sách; dòng mới ở trên cùng, trạng thái Đang tạo (nhãn xám).'

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
     'Lập kế hoạch tổng kiểm kê hàng hóa: khai thời gian kiểm kê (từ – đến), chọn các kho, công ty thuê kho (tự chọn theo kho), '
     'phòng ban tham gia và nội dung yêu cầu, rồi Lưu và duyệt để người có quyền lập các phiếu kiểm kê theo hàng hóa cho đợt '
     'kiểm kê. Kế hoạch KHÔNG có danh sách hàng và KHÔNG làm đổi tồn kho.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Danh sách: kế hoạch trong phạm vi xem; trạng thái Đang tạo (nhãn xám), Đã duyệt (nhãn xanh lá).\n'
     '- Ô Kho ở form: kho đang hoạt động có kho kế toán thuộc công ty người đăng nhập.\n'
     '- Ô Công ty thuê kho: công ty có kho kế toán trong các kho đã chọn.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Kế hoạch Đang tạo của người khác (kể cả với quyền tổng công ty).\n- Kế hoạch ngoài phạm vi quyền xem.\n'
     '- Kho ngừng hoạt động / không có kho kế toán của công ty mình (không chọn mới được ở form).\n'
     '- Kế hoạch của màn Kế hoạch kiểm kê theo hàng hóa (màn khác).'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo NGÀY TẠO kế hoạch (không phải ngày kiểm kê), lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Kế hoạch > các kho > các công ty thuê kho (thuộc kho đã chọn).\n- Kế hoạch > các phòng ban tham gia.\n'
     '- Kế hoạch > các phiếu kiểm kê theo hàng hóa lập từ kế hoạch.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Công ty thuê nhiều kho đã chọn chỉ hiện 1 lần ở ô Công ty thuê kho.\n'
     '- Kho / công ty / phòng ban không được trùng trong 1 kế hoạch.\n'
     '- Mỗi hàng chỉ được kiểm ở 1 phiếu kiểm kê của cùng kế hoạch.'),
    ('7. Phân quyền cấp',
     '- Tổng kiểm kê kho theo hàng hóa - tổng công ty: xem mọi kế hoạch.\n'
     '- Tổng kiểm kê kho theo hàng hóa: kế hoạch công ty mình + của mình.\n'
     '- Không quyền: chỉ kế hoạch mình tạo. Tạo / Sửa / Xóa không cần quyền (Sửa / Xóa chỉ người tạo, Đang tạo).\n'
     '- Lập phiếu kiểm kê kho theo hàng hóa: nút Lập phiếu kiểm kê hàng hóa + nhận thông báo.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là khoảng thứ tự dòng của trang, N là tổng kế hoạch khớp bộ lọc trong phạm vi xem.\n'
     '- Cột Ngày kiểm kê = "Ngày kiểm kê từ - Ngày kiểm kê đến".'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: A (người lập, không quyền xem theo cấp), B (nhân viên khác), C (quyền theo công ty), T (quyền '
     'tổng công ty), K (quyền Lập phiếu kiểm kê kho theo hàng hóa), DNS Admin (Super admin).\n'
     '- Lưu ý: Lưu nháp chỉ bắt 2 ô ngày; Lưu và duyệt bắt đủ 6 ô (cả 6 ô đều có dấu *).\n'
     '- Lưu ý: Lưu và duyệt chuyển trạng thái NGAY, không có hộp xác nhận; kế hoạch Đã duyệt không sửa / xóa được — chạy trên '
     'dữ liệu thử.\n'
     '- Lưu ý: nút Lập phiếu kiểm kê hàng hóa chỉ hiện khi Ngày kiểm kê từ là hôm nay hoặc sau hôm nay; đợt đã bắt đầu thì mất nút.\n'
     '- Lưu ý: đổi Kho làm Công ty thuê kho tự chọn lại hết theo kho mới.\n'
     '- Màn Tạo / Sửa / Chi tiết là TRANG riêng, không phải cửa sổ nổi.'),
]

SCREEN = ListScreen(menu=MENU, title='Kế hoạch tổng kiểm kê hàng hóa', total=12, quick_label='số phiếu',
                    quick_sample='00005', quick_hit='kế hoạch TPE.KHTKK-00005',
                    filters=[('Trạng thái', 'Đã duyệt'), ('Kho', 'CSKH - Chăm sóc khách hàng')], unit='kế hoạch')

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Cả 3 nơi đều là "Kế hoạch tổng kiểm kê hàng hóa" (không có chữ "Danh sách").'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE_LIST, [MENU, 'Quan sát khối bộ lọc và thanh công cụ.'], '—',
       ['Khối bộ lọc: ô tìm nhanh (gợi ý "Tìm theo số phiếu"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
        'Thanh công cụ: Tạo mới, Xuất Excel, In danh sách, nút biểu tượng cột.',
        'Dòng Đã duyệt: cột Hành động có In, Lịch sử; không có Sửa, Xóa.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 11 cột theo thứ tự: STT, Số phiếu, Ngày kiểm kê, Kho, Nội dung yêu cầu, Trạng thái, Người tạo, Ngày tạo, Ngày cập '
        'nhật, Người cập nhật, Hành động.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 11/11 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp kế hoạch đã tạo', 'P0', [PRE_LIST, P5], [MENU, 'Tìm "TPE.KHTKK-00005", đối chiếu dòng.'], '—',
       ['Ngày kiểm kê "07/11/2026 - 07/11/2026".', 'Kho "Chăm sóc khách hàng, Kho Dự án trọng điểm, Hải Phòng" (nối dấu phẩy), Nội dung '
        'yêu cầu "test 1uuq2yi", Trạng thái "Đã duyệt", Người tạo "DNS Admin", Ngày tạo "05/11/2026 15:08", Ngày cập nhật '
        '"05/11/2026 15:11", Người cập nhật "DNS Admin".'], [6, 58])
S1.add('Nội dung yêu cầu dài kẹp 2 dòng', 'P2', [PRE_LIST, 'TPE.KHTKK-00003 có Nội dung yêu cầu dài hơn 2 dòng.'],
       [MENU, 'Quan sát ô Nội dung yêu cầu dòng TPE.KHTKK-00003.', 'Rê chuột vào ô.'], '—',
       ['Ô chỉ hiện 2 dòng, cuối có dấu "…".', 'Rê chuột hiện đủ nội dung.'], 6)
S1.add('Trạng thái bản ghi', 'P0', PRE_LIST, [MENU, ADV, 'Mở ô Trạng thái.', 'Quan sát cột Trạng thái.'], '—',
       ['Ô có 2 lựa chọn: Đang tạo, Đã duyệt.', 'Nhãn: Đang tạo xám, Đã duyệt xanh lá.'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', [ACC_B, 'B chưa tạo kế hoạch nào.'], ['Đăng nhập B.', MENU], '—',
       ['Bảng hiện "Không có dữ liệu phù hợp."; không báo lỗi.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       ['Bảng hiện "Không có dữ liệu phù hợp.".'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 12 kế hoạch, tự về trang 1, "Hiển thị 1–12 / 12".', 'Chỉ nạp lại 1 lần (không nháy 2 lần).'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–12 / 12".', 'Bước 3: "Hiển thị 1–10 / 12".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—', ['Bước 2: trang 2.', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang 2 quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.'], '—', ['Trang 2 đánh số 11–12.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', ADV, 'Chọn Trạng thái = Đã duyệt.'],
       'Trạng thái: Đã duyệt', ['Tự nạp lại ở trang 1; "Hiển thị 1–5 / 5".'], 17)
S1.add('Sắp xếp tăng dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Số phiếu.'], '—',
       ['Xếp theo số phiếu tăng dần (TPE.KHTKK-00001 trên cùng), mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Số phiếu 2 lần.'], '—',
       ['Xếp theo số phiếu giảm dần, mũi tên xuống.'], 21)
S1.add('Sắp xếp theo Ngày kiểm kê; mặc định theo Ngày tạo', 'P1', PRE_LIST,
       [MENU, 'Quan sát thứ tự khi mới vào.', 'Bấm tiêu đề Ngày kiểm kê (2 lần).'], '—',
       ['Mới vào: kế hoạch tạo mới nhất ở trên, các cột hiện biểu tượng sắp xếp trung tính.',
        'Ngày kiểm kê lần 1: Ngày kiểm kê từ cũ nhất trên (TPE.KHTKK-00001 08/10/2026); lần 2 mới nhất trên.',
        'Cột Ngày tạo, Ngày cập nhật không có biểu tượng sắp xếp.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Kho, Nội dung yêu cầu, Trạng thái, Người tạo, Ngày tạo, Ngày cập nhật, Người cập nhật.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Số phiếu (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự tăng của trang 1.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 2.', 'Bấm tiêu đề Ngày kiểm kê.'], '—', ['Về trang 1.'], 25)
S1.add('Nút thao tác theo trạng thái', 'P0', [ACC_A, KH1, KH2], ['Đăng nhập A.', MENU, 'Quan sát cột Hành động 2 dòng KH1, KH2.'], '—',
       ['KH1 (Đang tạo): Sửa, Xóa và nút ba chấm "Hành động khác" chứa In, Lịch sử.',
        'KH2 (Đã duyệt, A không có quyền "%s"): In, Lịch sử; không có Sửa, Xóa, %s.' % (Q1, LAP)], [3, 34])
S1.add('Mở màn từ thông báo', 'P1', [ACC_K, KH2, 'K đã nhận thông báo "[KHTKK] Đã duyệt: <số phiếu KH2>".'],
       ['Đăng nhập K.', 'Bấm chuông thông báo, bấm thông báo của KH2.'], '—',
       ['Mở màn chi tiết KH2 (K không có quyền xem theo cấp vẫn mở được).', 'Có nút %s.' % LAP], 1)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo số phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "TPE.KHTKK-00005", bấm Tìm kiếm.'], 'Ô tìm nhanh: TPE.KHTKK-00005',
       ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần số phiếu', 'P0', PRE_LIST, [MENU, 'Nhập "KHTKK-0000", bấm Tìm kiếm.'], 'Ô tìm nhanh: KHTKK-0000',
       ['Ra các kế hoạch có số phiếu chứa chuỗi nhập (có TPE.KHTKK-00001 … 00005).'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "tpe.khtkk-00005", bấm Tìm kiếm.'], '—',
       ['Ra TPE.KHTKK-00005 như khi gõ chữ hoa.'], 28)
S2.add('Có dấu / không dấu ở ô Tên hàng hóa', 'P2', [PRE_LIST, 'Đã có phiếu kiểm kê lập từ TPE.KHTKK-00005 chứa hàng "Máy tính xách tay".'],
       [MENU, ADV, 'Nhập Tên hàng hóa "may tinh xach tay", bấm Tìm kiếm.'], '—',
       ['Ra TPE.KHTKK-00005 nếu cơ sở dữ liệu so khớp không dấu.', 'Lưu ý: so khớp theo cách so sánh chữ của cơ sở dữ liệu.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; ký tự % được hiểu là ký tự đại diện nên ra toàn bộ.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  TPE.KHTKK-00005  ", bấm Tìm kiếm.'], '—',
       ['Ra TPE.KHTKK-00005 (bỏ khoảng trắng đầu / cuối).'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "TPE.KHTKK-00005", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Sau bước 2 hiện lại đủ 12 kế hoạch.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST,
       [MENU, 'Nhập "00005", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'], '—',
       ['Cả 2 cách đều ra TPE.KHTKK-00005, về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['Các ô Kho, Trạng thái, Người tạo, Mã hàng hóa, Tên hàng hóa, Ngày tạo, Công ty, Phòng ban đều trống.',
        'Đủ 12 kế hoạch.'], 36)
S2.add('Lọc Kho', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = HP - Hải Phòng.'], '—',
       ['Lọc ngay; còn TPE.KHTKK-00005 và TPE.KHTKK-00002 (có kho Hải Phòng).', 'Ô Kho liệt kê mọi kho, hiển thị "Mã - Tên".'], 37)
S2.add('Lọc Kho với kế hoạch nhiều kho', 'P1', PRE_LIST, [MENU, ADV, 'Chọn Kho = DATD - Kho Dự án trọng điểm.'], '—',
       ['Ra TPE.KHTKK-00005 (gồm 3 kho).'], 37)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đã duyệt.', 'Đổi Trạng thái = Đang tạo.'], '—',
       ['Bước 3: 5 kế hoạch, nhãn xanh lá.', 'Bước 4: 7 kế hoạch Đang tạo của DNS Admin, nhãn xám.'], 37)
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = DNS Admin.', 'Đổi Người tạo = Bùi Duy Trước.'], '—',
       ['Bước 3: đủ 12 kế hoạch.', 'Bước 4: "Không có dữ liệu phù hợp.".',
        'Ô Người tạo liệt kê toàn bộ nhân viên, kể cả người chưa tạo kế hoạch nào.'], 37)
S2.add('Lọc Mã hàng hóa', 'P0', [PRE_LIST, 'Phiếu kiểm kê lập từ TPE.KHTKK-00005 có hàng mã ACER-A315-34-P3LC.'],
       [MENU, ADV, 'Nhập Mã hàng hóa "ACER-A315", bấm Tìm kiếm.'], '—',
       ['Ra TPE.KHTKK-00005 (kế hoạch có phiếu kiểm kê chứa hàng khớp mã).', 'Kế hoạch chưa lập phiếu kiểm kê nào không bao giờ khớp.',
        'Chỉ gõ chưa bấm Tìm kiếm thì danh sách chưa đổi.'], 37)
S2.add('Lọc Tên hàng hóa', 'P0', [PRE_LIST, 'Phiếu kiểm kê lập từ TPE.KHTKK-00005 có hàng "Máy tính xách tay".'],
       [MENU, ADV, 'Nhập Tên hàng hóa "MÁY TÍNH", bấm Tìm kiếm.'], '—',
       ['Ra TPE.KHTKK-00005, không phân biệt hoa / thường.'], 37)
S2.add('Lọc Ngày tạo lấy trọn ngày biên', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày tạo 26/10/2026 – 26/10/2026.'], '—',
       ['Ra 3 kế hoạch TPE.KHTKK-00003, 00002, 00001 (tạo 15:20 – 15:21 ngày 26/10/2026).',
        'Lọc theo ngày tạo, KHÔNG theo ngày kiểm kê; bỏ trống ngày cuối vẫn lọc được từ ngày đầu.'], 37)
S2.raw(org_cases(SCREEN, len(S2) + 1), [[37], [37, 283], [37]])
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = CSKH - Chăm sóc khách hàng.', 'Chọn Ngày tạo 26/10/2026 – 26/10/2026.'],
       '—', ['Chỉ còn TPE.KHTKK-00003.'], 38)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST, [MENU, 'Nhập "00001", bấm Tìm kiếm.', ADV, 'Chọn Kho = HP - Hải Phòng.'], '—',
       ['"Không có dữ liệu phù hợp." vì TPE.KHTKK-00001 thuộc kho Liên Ninh.'], [39, 40])
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đang tạo.', 'Đổi Số dòng/trang = 5, bấm trang 2.'],
       '—', ['"Hiển thị 1–5 / 7" rồi "Hiển thị 6–7 / 7"; STT liên tục.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Trạng thái = Đã duyệt.', ['Bấm tiêu đề Số phiếu.'], '—',
       ['Chỉ 5 kế hoạch đang lọc được sắp; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "TPE", lọc Kho Hải Phòng, Mã hàng hóa "ACER", sắp Số phiếu, ở trang 2.',
       ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh, Kho, Mã hàng hóa về trống, bỏ sắp xếp, nạp lại trang 1, đủ 12 kế hoạch.'], 44)
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Đã duyệt, chưa mở màn con.'], ['Nhấn F5.'], '—',
       ['Bộ lọc trở về trống, đủ 12 kế hoạch (chỉ nhớ khi đi vào màn con của màn này).'], 46)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Mã hàng hóa, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô Mã hàng hóa.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Kho = HP - Hải Phòng.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Kho, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị bỏ, nạp lại đủ 12 kế hoạch.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Mã hàng hóa.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Mã hàng hóa vẫn ẩn.', 'Bước 2: tích đủ 7 mục, Mã hàng hóa hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Trạng thái lên đầu, bấm Lưu.'], '—',
       ['Ô Trạng thái đứng đầu khối Tìm kiếm nâng cao; cấu hình giữ sau khi đăng nhập lại.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo', 'P0', PRE_FORM, TAO, '—', ['Mở TRANG "Tạo kế hoạch tổng kiểm kê hàng hóa", tab cùng tiêu đề.'], 49)
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải ghi tên A.', 'Không có ô Số phiếu (tự sinh khi lưu).'], 50)
S3.add('Các trường và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Ngày kiểm kê từ (gợi ý "Chọn ngày kiểm kê từ"), Ngày kiểm kê đến (gợi ý "Chọn ngày kiểm kê đến"), Kho '
        '(gợi ý "Chọn kho"), Công ty thuê kho (gợi ý "Chọn kho trước"), Thành phần tham gia (gợi ý "Chọn phòng ban"), Nội dung yêu '
        'cầu (gợi ý "Nhập nội dung yêu cầu").',
        'Chân màn: Lưu nháp, Lưu và duyệt, Lưu và tiếp tục, Quay lại.'], [51, 54])
S3.add('Trường bắt buộc / không bắt buộc', 'P0', PRE_FORM, TAO + ['Quan sát dấu *.'], '—',
       ['Cả 6 ô có dấu *.', 'Lưu ý: Lưu nháp chỉ bắt 2 ô ngày; Lưu và duyệt bắt đủ 6 ô.'], 52)
S3.add('Giá trị mặc định', 'P0', PRE_FORM, TAO, '—',
       ['Mọi ô trống.', 'Công ty thuê kho bị khóa cho tới khi chọn Kho.'], 53)
S3.add('Ô Kho chỉ có kho của công ty mình', 'P1', [PRE_FORM, 'Kho Sài Gòn chỉ có kho kế toán của công ty TPSG.'],
       TAO + ['Mở ô Kho.'], '—', ['Liệt kê kho đang hoạt động có kho kế toán của TPE, hiển thị "Mã - Tên".', 'KHÔNG có Kho Sài Gòn.'], [53, 276])
S3.add('Chọn kho tự chọn công ty thuê kho', 'P0', PRE_FORM, TAO + ['Chọn Kho = CSKH - Chăm sóc khách hàng và HP - Hải Phòng.'], '—',
       ['Ô Công ty thuê kho mở khóa, gợi ý đổi thành "Chọn công ty thuê kho".',
        'Tự chọn HẾT công ty có kho kế toán trong 2 kho, hiển thị mã công ty, mỗi công ty 1 lần.'], [53, 283, 269])
S3.add('Đổi kho chọn lại công ty thuê kho', 'P1', 'Đang ở màn Tạo, đã chọn 2 kho và bỏ bớt 1 công ty thuê kho.',
       ['Bỏ kho Hải Phòng khỏi ô Kho.'], '—',
       ['Công ty thuê kho chọn lại hết công ty của kho còn lại (công ty đã bỏ bớt được chọn lại nếu thuê kho đó).',
        'Bỏ hết kho: ô Công ty thuê kho trống và khóa.'], [53, 283])
S3.add('Lịch Ngày kiểm kê đến chặn ngày trước Ngày kiểm kê từ', 'P1', PRE_FORM,
       TAO + ['Chọn Ngày kiểm kê từ 10/11/2026.', 'Mở lịch Ngày kiểm kê đến.'], '—',
       ['Các ngày trước 10/11/2026 bị mờ, không chọn được.'], 62)
S3.add('Lưu nháp với dữ liệu hợp lệ đầy đủ', 'P0', PRE_FORM, FILL + ['Bấm Lưu nháp.'], FULL,
       [OK_DRAFT, 'Số phiếu dạng "TPE.KHTKK-<số>" theo công ty của A.'], [55, 58, 59, 79])
S3.add('Lưu nháp chỉ với 2 ô ngày', 'P0', PRE_FORM, DATES + ['Để trống Kho, Thành phần tham gia, Nội dung yêu cầu.', 'Bấm Lưu nháp.'],
       ['Ngày kiểm kê từ: 10/11/2026', 'Ngày kiểm kê đến: 12/11/2026'],
       [OK_DRAFT, 'Chi tiết kế hoạch: Kho, Công ty thuê kho, Thành phần tham gia, Nội dung yêu cầu trống.'], [56, 57])
S3.add('Dữ liệu sau lưu', 'P0', [PRE_FORM, 'A vừa Lưu nháp kế hoạch ở TC_03.010.'], ['Bấm số phiếu vừa tạo.'], '—',
       ['Chi tiết: Ngày kiểm kê 10/11/2026 – 12/11/2026, Kho Chăm sóc khách hàng, Công ty thuê kho (mã công ty), Thành phần tham gia '
        'BAN ĐIỀU HÀNH, Nội dung yêu cầu "Tổng kiểm kê cuối năm".'], 58)
S3.add('Trạng thái mặc định sau Lưu nháp', 'P0', [PRE_FORM, 'A vừa Lưu nháp kế hoạch.'], [MENU, 'Đăng nhập DNS Admin, mở danh sách.'], '—',
       ['A thấy kế hoạch Đang tạo (nhãn xám).', 'DNS Admin KHÔNG thấy kế hoạch này (Đang tạo chỉ người tạo thấy).'], [59, 84])
S3.add('Lịch sử tạo', 'P1', [PRE_FORM, 'A vừa Lưu nháp kế hoạch.'], ['Ở dòng kế hoạch bấm ba chấm > Lịch sử.'], '—',
       ['Có 1 mốc "Tạo mới", Người thực hiện A, thời điểm lưu.'], [60, 176])
S3.add('Lưu nháp khi bỏ trống ngày', 'P0', PRE_FORM, TAO + ['Bấm Lưu nháp ngay.'], '—',
       ['Báo "Bạn chưa nhập đầy đủ thông tin.", không lưu.',
        'Lỗi đỏ ' + REQ + ' CÙNG LÚC dưới Ngày kiểm kê từ và Ngày kiểm kê đến; các ô khác không báo lỗi.', 'Cuộn tới ô lỗi đầu tiên.'],
       [61, 70, 80])
S3.add('Ngày kiểm kê đến trước Ngày kiểm kê từ', 'P0', PRE_FORM,
       TAO + ['Chọn Ngày kiểm kê đến 05/11/2026.', 'Chọn Ngày kiểm kê từ 10/11/2026.', 'Bấm Lưu nháp.'], '—',
       ['Dưới Ngày kiểm kê đến báo "Phải lớn hơn hoặc bằng Ngày kiểm kê từ.", không lưu (chặn cả ở Lưu nháp).'], [62, 81])
S3.add('Nội dung yêu cầu đúng 255 ký tự', 'P1', PRE_FORM, FILL[:-1] + ['Dán 255 ký tự vào Nội dung yêu cầu.', 'Bấm Lưu nháp.'],
       'Nội dung yêu cầu: 255 ký tự', ['Lưu thành công, nội dung đủ 255 ký tự.'], [64, 65])
S3.add('Nội dung yêu cầu vượt 255 ký tự', 'P1', PRE_FORM, TAO + ['Dán 300 ký tự vào Nội dung yêu cầu.'], 'Nội dung yêu cầu: 300 ký tự',
       ['Ô chỉ nhận 255 ký tự đầu (không gõ thêm được); nếu vượt vẫn bị chặn "Vui lòng nhập tối đa 255 ký tự.".'], [65, 66])
S3.add('Nội dung có ký tự đặc biệt, tiếng Việt, khoảng trắng', 'P2', PRE_FORM,
       FILL[:-1] + ['Nhập Nội dung yêu cầu "  Kiểm kê <Kho 1> & \'đợt 2\'  ".', 'Bấm Lưu nháp.'], '—',
       ['Lưu thành công, nội dung hiển thị đúng ký tự đã nhập, tiếng Việt có dấu đầy đủ, không lỗi giao diện.',
        'Khoảng trắng đầu / cuối bị bỏ khi lưu.'], [63, 68, 69, 81])
S3.add('Nội dung chỉ có khoảng trắng', 'P2', PRE_FORM, FILL[:-1] + ['Nhập Nội dung yêu cầu "     ".', 'Bấm Lưu và duyệt.'], '—',
       ['Coi như trống: báo ' + REQ + ' dưới Nội dung yêu cầu, không lưu.'], 69)
S3.add('Ký tự không hợp lệ ở ô chọn', 'P2', PRE_FORM, TAO + ['Gõ "abc" vào ô Kho.'], '—',
       ['Ô chỉ lọc danh sách gợi ý, không nhận giá trị tự gõ; Kho / Công ty / Thành phần tham gia là ô chọn nên không có định dạng sai.'],
       [63, 64])
S3.add('Lỗi biến mất sau khi sửa', 'P1', 'Đang có lỗi đỏ ở 2 ô ngày (TC_03.015).', ['Chọn Ngày kiểm kê từ.', 'Chọn Ngày kiểm kê đến.'],
       '—', ['Lỗi của từng ô biến mất ngay khi chọn ngày.'], 71)
S3.add('Trùng dữ liệu: 2 kế hoạch cùng kho, cùng thời gian', 'P1', [PRE_FORM, KH1], FILL + ['Bấm Lưu nháp.'], FULL,
       ['Lưu được; 2 kế hoạch có số phiếu khác nhau (không có trường duy nhất).'], [67, 75, 82])
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, FILL + ['Bấm Lưu và tiếp tục.'], FULL,
       ['Báo "Thêm mới thành công.", VẪN ở màn Tạo.', 'Form trắng: mọi ô trống, Công ty thuê kho khóa.',
        'Kế hoạch vừa lưu ở trạng thái Đang tạo.'], [72, 76, 77, 83])
S3.add('Lưu và tiếp tục khi thiếu ngày', 'P0', PRE_FORM, TAO + ['Bấm Lưu và tiếp tục.'], '—',
       ['Báo lỗi như Lưu nháp, không lưu, form giữ dữ liệu đã nhập.'], [73, 74])
S3.add('Rời màn sau Lưu và tiếp tục', 'P1', 'Vừa Lưu và tiếp tục, form trắng.', ['Bấm Quay lại.'], '—',
       ['Về danh sách ngay, không hỏi; kế hoạch vừa lưu có trong danh sách.'], [78, 85])
S3.add('Lưu nháp: màn chuyển về danh sách', 'P1', PRE_FORM, FILL + ['Bấm Lưu nháp.'], FULL,
       ['Màn Tạo đóng, về danh sách (màn là trang, không phải cửa sổ còn mở).'], [76, 85])
S3.add('Quay lại khi chưa nhập', 'P1', PRE_FORM, TAO + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 93)
S3.add('Quay lại khi đã nhập', 'P0', PRE_FORM, FILL + ['Bấm Quay lại.'], '—',
       ['Hiện hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" với nút Thoát, Ở lại.'], 94)
S3.add('Rời màn bằng menu / (x) của hộp', 'P1', PRE_FORM, FILL + ['Bấm menu sang màn khác.', 'Ở hộp "Thông tin chưa lưu" bấm (x).'],
       '—', ['Hộp hiện khi bấm menu; bấm (x) đóng hộp, ở lại màn Tạo, dữ liệu giữ nguyên (màn là trang, không có nút X riêng).'], 95)
S3.add('Chọn Thoát', 'P0', 'Đang ở hộp "Thông tin chưa lưu".', ['Bấm Thoát.'], '—', ['Về danh sách, không lưu kế hoạch nào.'], 96)
S3.add('Chọn Ở lại', 'P1', 'Đang ở hộp "Thông tin chưa lưu".', ['Bấm Ở lại.'], '—', ['Đóng hộp, dữ liệu đã nhập giữ nguyên.'], 97)
S3.add('Nhập rồi trả về như ban đầu', 'P2', PRE_FORM, TAO + ['Nhập Nội dung yêu cầu "abc".', 'Xóa hết chữ vừa nhập.', 'Bấm Quay lại.'],
       '—', ['Không hỏi "Thông tin chưa lưu" (dữ liệu như lúc mở).'], [98, 99])
S3.add('Không thao tác lâu', 'P2', PRE_FORM, FILL + ['Để yên 30 phút.', 'Bấm Lưu nháp.'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên, chuyển về đăng nhập, không lưu.'], 100)
S3.add('Bấm Lưu nháp liên tục', 'P0', PRE_FORM, FILL + ['Bấm Lưu nháp 3 lần thật nhanh.'], FULL,
       ['Chỉ tạo 1 kế hoạch (nút khóa trong lúc lưu).'], 101)
S3.add('Tạo đồng thời ở 2 tab', 'P1', PRE_FORM, ['Mở 2 tab màn Tạo, nhập cùng dữ liệu.', 'Bấm Lưu nháp ở cả 2 tab.'], FULL,
       ['Tạo 2 kế hoạch, số phiếu khác nhau, không lỗi.'], 102)
S3.add('Công ty không thuê kho đã chọn', 'P2', [PRE_FORM, 'Công ty TPSG không có kho kế toán trong kho Chăm sóc khách hàng.'],
       ['Dùng 2 tab: tab 1 chọn Kho CSKH + HP (công ty thuê kho tự chọn), tab 2 bị đổi kho kế toán khiến 1 công ty không còn thuê kho.',
        'Tab 1 bấm Lưu và duyệt.'], '—', ['Dưới Công ty thuê kho báo "Có công ty không thuê các kho đã chọn.", không lưu.'], [62, 268])

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
PRE_E = [ACC_A, KH1]
EDIT = ['Đăng nhập A.', MENU, 'Ở dòng KH1 bấm Sửa (bút chì).']
S4.add('Mở màn Sửa', 'P0', PRE_E, EDIT, '—', ['Mở TRANG "Sửa kế hoạch tổng kiểm kê hàng hóa: <số phiếu KH1>".'], 103)
S4.add('Dữ liệu điền đúng', 'P0', PRE_E, EDIT, '—',
       ['Số phiếu (khóa), Ngày kiểm kê 10/11/2026 – 12/11/2026, Kho Chăm sóc khách hàng, Công ty thuê kho TPE, Thành phần tham gia '
        'BAN ĐIỀU HÀNH, Nội dung "Tổng kiểm kê cuối năm".', 'Góc phải "<A> - <ngày giờ tạo>".'], 104)
S4.add('Trường được / không được sửa', 'P0', PRE_E, EDIT, '—',
       ['Không sửa được: Số phiếu (ô khóa).', 'Sửa được: 2 ô ngày, Kho, Công ty thuê kho, Thành phần tham gia, Nội dung yêu cầu.'], 105)
S4.add('Các nút ở màn Sửa', 'P1', PRE_E, EDIT, '—', ['Có Lưu nháp, Lưu và duyệt, Quay lại; KHÔNG có Lưu và tiếp tục.'], 106)
S4.add('Sửa một trường', 'P0', PRE_E, EDIT + ['Sửa Nội dung yêu cầu thành "Đợt 2".', 'Bấm Lưu nháp.'], 'Nội dung yêu cầu: Đợt 2',
       ['Báo "Cập nhật thành công.", về danh sách; trạng thái vẫn Đang tạo; số phiếu không đổi.'], [107, 69])
S4.add('Sửa nhiều trường', 'P0', PRE_E, EDIT + ['Đổi Ngày kiểm kê đến 15/11/2026.', 'Thêm Kho HP - Hải Phòng.', 'Bấm Lưu nháp.'],
       '—', ['Lưu thành công; kế hoạch có 2 kho, công ty thuê kho chọn lại theo 2 kho, ngày đến 15/11/2026.'], [108, 110])
S4.add('Giữ nguyên giá trị khi lưu không đổi', 'P1', PRE_E, EDIT + ['Không đổi gì, bấm Lưu nháp.'], '—',
       ['Lưu thành công, không báo trùng chính kế hoạch; Công ty thuê kho giữ đúng như đã lưu.'], [109, 68])
S4.add('Ngày / người cập nhật', 'P1', [ACC_A, 'KH1 lưu ngày 01/11/2026.'], EDIT + ['Sửa Nội dung, bấm Lưu nháp ngày 05/11/2026.',
                                                                                 'Xem dòng KH1 ở danh sách.'], '—',
       ['Ngày cập nhật = thời điểm lưu, Người cập nhật = A; Ngày tạo không đổi.'], 111)
S4.add('Lịch sử sửa', 'P0', PRE_E, EDIT + ['Sửa Nội dung yêu cầu và thêm 1 kho, bấm Lưu nháp.', 'Mở Lịch sử của KH1.'], '—',
       ['Có mốc "Thay đổi thông tin", ghi Nội dung yêu cầu cũ > mới, Kho cũ > mới, Công ty thuê kho cũ > mới (nếu đổi).'],
       [112, 177, 178])
S4.add('Bỏ trống bắt buộc khi sửa', 'P0', PRE_E, EDIT + ['Xóa Ngày kiểm kê từ.', 'Bấm Lưu nháp.'], '—',
       [REQ + ' dưới Ngày kiểm kê từ, "Bạn chưa nhập đầy đủ thông tin.", không lưu.'], [113, 117])
S4.add('Vượt giới hạn khi sửa', 'P2', PRE_E, EDIT + ['Dán 300 ký tự vào Nội dung yêu cầu.'], '—',
       ['Ô chỉ nhận 255 ký tự; Kho, Công ty thuê kho, Thành phần tham gia là ô chọn nên không có định dạng sai.'], [114, 115])
S4.add('Trùng bản ghi khác khi sửa', 'P2', [ACC_A, KH1, 'Có kế hoạch khác cùng kho, cùng thời gian.'], EDIT + ['Bấm Lưu nháp.'], '—',
       ['Lưu được (kế hoạch không có trường duy nhất).'], 116)
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P1', 'Đang có lỗi ' + REQ + ' dưới Ngày kiểm kê từ.', ['Chọn lại Ngày kiểm kê từ.'], '—',
       ['Lỗi biến mất ngay.'], 118)
S4.add('Mở Sửa rồi Quay lại không đổi', 'P1', PRE_E, EDIT + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], [119, 125])
S4.add('Đổi rồi trả về ban đầu', 'P2', PRE_E, EDIT + ['Sửa Nội dung rồi gõ lại đúng nội dung cũ.', 'Bấm Quay lại.'], '—',
       ['Không hỏi "Thông tin chưa lưu".'], 120)
S4.add('Rời màn khi đã đổi', 'P0', PRE_E, EDIT + ['Sửa Nội dung yêu cầu.', 'Bấm Quay lại.'], '—', ['Hiện hộp "Thông tin chưa lưu".'], 121)
S4.add('Xác nhận Thoát', 'P1', 'Đang ở hộp "Thông tin chưa lưu" của màn Sửa.', ['Bấm Thoát.'], '—',
       ['Về danh sách; KH1 không đổi; lịch sử không có mốc mới.'], [122, 124, 125])
S4.add('Xác nhận Ở lại', 'P2', 'Đang ở hộp "Thông tin chưa lưu" của màn Sửa.', ['Bấm Ở lại.'], '—', ['Ở lại màn Sửa, dữ liệu đã đổi giữ nguyên.'], 123)
S4.add('Sửa kế hoạch đã Đã duyệt', 'P0', [ACC_A, KH2], ['Đăng nhập A.', MENU, 'Quan sát dòng KH2.', 'Mở đường link màn Sửa của KH2 từ lịch sử trình duyệt.'],
       '—', ['Dòng KH2 không có nút Sửa.', 'Mở màn Sửa tự chuyển sang màn chi tiết KH2.'], [126, 63])
S4.add('Kế hoạch bị xóa ở tab khác', 'P1', PRE_E, ['Tab 1 mở màn Sửa KH1.', 'Tab 2 xóa KH1.', 'Tab 1 bấm Lưu nháp.'], '—',
       ['Báo ' + NOTFOUND + ', không lưu.'], [127, 138])
S4.add('Kế hoạch vừa được duyệt ở tab khác', 'P0', PRE_E, ['Tab 1 mở màn Sửa KH1.', 'Tab 2 mở Sửa KH1, bấm Lưu và duyệt.', 'Tab 1 bấm Lưu nháp.'],
       '—', ['Tab 1 báo ' + CONFLICT + ', không lưu.'], [128, 91])
S4.add('Người khác không sửa được', 'P0', [ACC_B, KH1], ['Đăng nhập B.', MENU, 'Tìm KH1.'], '—',
       ['B không thấy KH1 (Đang tạo chỉ người tạo thấy) nên không sửa được.'], [128, 63])
S4.add('Kế hoạch đã có phiếu kiểm kê', 'P1', [PRE_LIST, P5, 'Đã có phiếu kiểm kê lập từ TPE.KHTKK-00005.'], [MENU, 'Quan sát dòng TPE.KHTKK-00005.'], '—',
       ['Không có nút Sửa, Xóa (kế hoạch Đã duyệt).'], 129)
S4.add('Kho / phòng ban đã ngừng vẫn hiện ở màn Sửa', 'P2', [ACC_A, KH1, 'Kho Chăm sóc khách hàng và phòng ban BAN ĐIỀU HÀNH bị ngừng '
                                                                       'hoạt động sau khi lưu KH1.'], EDIT, '—',
       ['Ô Kho vẫn hiện "CSKH - Chăm sóc khách hàng", Thành phần tham gia vẫn hiện BAN ĐIỀU HÀNH.',
        'Ở màn Tạo mới kho / phòng ban này không còn để chọn.'], [276, 284])

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
S5.add('Không xóa được kế hoạch Đã duyệt', 'P0', [ACC_A, KH2, P5], ['Đăng nhập A.', MENU], '—',
       ['KH2 và TPE.KHTKK-00005 không có nút Xóa (Đã duyệt, có thể đã lập phiếu kiểm kê).'], [135, 137, 270])
S5.add('Xóa kế hoạch có dữ liệu con', 'P1', [ACC_A, KH1, 'KH1 có 2 kho, 3 công ty thuê kho, 2 phòng ban tham gia.'], ['Xóa KH1.'], '—',
       ['Xóa thành công, toàn bộ kho, công ty thuê kho, phòng ban của KH1 bị xóa theo (không còn dữ liệu mồ côi).'], [136, 285])
S5.add('Kế hoạch đã bị xóa ở tab khác', 'P1', [ACC_A, KH1], ['Tab 1, tab 2 cùng mở danh sách.', 'Tab 2 xóa KH1.', 'Tab 1 xóa KH1.'], '—',
       ['Tab 1 báo ' + NOTFOUND + '.'], 138)
S5.add('Kế hoạch vừa được duyệt ở tab khác', 'P1', [ACC_A, KH1], ['Tab 2 Lưu và duyệt KH1.', 'Tab 1 bấm Xóa KH1, bấm Xóa.'], '—',
       ['Báo ' + CONFLICT + ', không xóa.'], 138)
S5.add('Dữ liệu liên quan sau xóa', 'P1', [ACC_A, KH1, 'Kho Cát Bà chỉ có trong KH1.'], ['Xóa KH1.', 'Vào phân hệ Kho > Danh mục > Kho vật lý, xóa kho Cát Bà.'],
       '—', ['Không còn bị chặn vì KH1 (kế hoạch không còn dùng kho này).'], [141, 280])
S5.add('Lịch sử xóa', 'P2', [ACC_A, KH1], ['Xóa KH1.'], '—', ['Hệ thống ghi mốc "Xóa" cho KH1 trước khi xóa.'], 141)

# ============================================================== VI. DUYỆT PHIẾU (Lưu và duyệt)
S6 = Sec(6)
S6.add('Nút Lưu và duyệt', 'P0', PRE_FORM, TAO, '—',
       ['Nút Lưu và duyệt (màu chính, biểu tượng dấu tích tròn) ở chân màn Tạo và Sửa; rê chuột "Lưu và chuyển kế hoạch sang trạng '
        'thái Đã duyệt".'], 300)
S6.add('Lưu và duyệt thành công', 'P0', [PRE_FORM, ACC_K], FILL + ['Bấm Lưu và duyệt.'], FULL,
       ['KHÔNG có hộp xác nhận; báo "Lưu và duyệt thành công.", về danh sách.', 'Kế hoạch mới trạng thái Đã duyệt (nhãn xanh lá).'],
       [86, 92, 301, 302, 305])
S6.add('Lưu và duyệt khi bỏ trống mọi trường', 'P0', PRE_FORM, TAO + ['Bấm Lưu và duyệt.'], '—',
       ['Báo "Bạn chưa nhập đầy đủ thông tin.", không lưu, không gửi.',
        'Lỗi ' + REQ + ' CÙNG LÚC dưới cả 6 ô: Ngày kiểm kê từ, Ngày kiểm kê đến, Kho, Công ty thuê kho, Thành phần tham gia, Nội dung '
        'yêu cầu.'], [87, 303])
S6.add('Lưu và duyệt khi chỉ có 2 ô ngày', 'P0', PRE_FORM, DATES + ['Bấm Lưu và duyệt.'], '—',
       ['Báo lỗi ' + REQ + ' dưới Kho, Công ty thuê kho, Thành phần tham gia, Nội dung yêu cầu; không lưu.',
        'Lưu ý: cùng dữ liệu này bấm Lưu nháp thì lưu được.'], [87, 303])
S6.add('Lưu và duyệt khi sai ngày', 'P1', PRE_FORM, FILL + ['Đổi Ngày kiểm kê từ thành 15/11/2026 (sau ngày đến).', 'Bấm Lưu và duyệt.'],
       '—', ['Báo "Phải lớn hơn hoặc bằng Ngày kiểm kê từ." dưới Ngày kiểm kê đến, không lưu.'], [88, 304])
S6.add('Lưu và duyệt từ màn Sửa', 'P0', [ACC_A, KH1], ['Mở Sửa KH1.', 'Bấm Lưu và duyệt.'], '—',
       ['Báo "Lưu và duyệt thành công.", KH1 chuyển Đã duyệt; không còn nút Sửa, Xóa.'], [302, 305, 311])
S6.add('Kế hoạch lưu nháp thiếu thông tin rồi duyệt', 'P1', [ACC_A, 'KH4 Đang tạo chỉ có 2 ô ngày.'], ['Mở Sửa KH4.', 'Bấm Lưu và duyệt.'],
       '—', ['Báo thiếu Kho, Công ty thuê kho, Thành phần tham gia, Nội dung yêu cầu; KH4 giữ Đang tạo.'], 303)
S6.add('Màn sau khi Lưu và duyệt', 'P1', PRE_FORM, FILL + ['Bấm Lưu và duyệt.'], FULL,
       ['Màn Tạo đóng, về danh sách (không ở lại như Lưu và tiếp tục).'], [90, 91, 92])
S6.add('Trùng dữ liệu khi Lưu và duyệt', 'P2', [PRE_FORM, 'Đã có kế hoạch Đã duyệt cùng kho, cùng thời gian.'], FILL + ['Bấm Lưu và duyệt.'],
       FULL, ['Lưu được, số phiếu khác (không có trường duy nhất).'], 89)
S6.add('Dữ liệu sau khi Lưu và duyệt', 'P0', [PRE_FORM, 'Vừa Lưu và duyệt kế hoạch.'], ['Mở chi tiết kế hoạch vừa lưu.'], '—',
       ['Ngày, kho, công ty thuê kho, thành phần tham gia, nội dung đúng như đã nhập; danh sách ghi Đã duyệt.'], 306)
S6.add('Thông báo đến người lập phiếu kiểm kê', 'P0', [PRE_FORM, ACC_K, 'Nhân viên X công ty khác có cùng quyền.'], FILL + ['Bấm Lưu và duyệt.'],
       FULL, ['K nhận thông báo "[KHTKK] Đã duyệt: <số phiếu>", ghi chú "Người lập: <tên A>. Cần lập phiếu kiểm kê. Thời gian: '
              '10/11/2026 – 12/11/2026. Kho: Chăm sóc khách hàng. Ghi chú: Tổng kiểm kê cuối năm".',
              'X (khác công ty) và nhân viên không có quyền KHÔNG nhận.'], 308)
S6.add('Thông báo nhiều kho', 'P2', [PRE_FORM, ACC_K, 'Kế hoạch chọn 5 kho.'], ['Bấm Lưu và duyệt.'], '—',
       ['Phần Kho của thông báo ghi 3 tên kho đầu + "và 2 kho khác".'], 309)
S6.add('Bấm thông báo mở kế hoạch', 'P1', [ACC_K, 'K vừa nhận thông báo; Ngày kiểm kê từ chưa qua.'], ['Bấm thông báo.'], '—',
       ['Mở màn chi tiết kế hoạch, có nút %s.' % LAP], 309)
S6.add('Lưu nháp không gửi thông báo', 'P1', [PRE_FORM, ACC_K], FILL + ['Bấm Lưu nháp.'], FULL, ['K không nhận thông báo nào.'], 308)
S6.add('Hủy thao tác (rời màn)', 'P1', PRE_FORM, FILL + ['Bấm Quay lại, chọn Thoát.'], '—',
       ['Không có kế hoạch nào được lưu; K không nhận thông báo.'], 310)
S6.add('Không duyệt lại kế hoạch đã Đã duyệt', 'P0', [ACC_A, KH2], [MENU, 'Quan sát dòng KH2.'], '—',
       ['Không có nút Sửa / Lưu và duyệt cho KH2; không có luồng trả về Đang tạo.'], 311)
S6.add('Lịch sử khi Lưu và duyệt', 'P1', [ACC_A, KH1], ['Sửa KH1, bấm Lưu và duyệt.', 'Mở Lịch sử KH1.'], '—',
       ['Có mốc "Thay đổi trạng thái" Đang tạo > Đã duyệt, người thực hiện A, thời điểm lưu.'], [312, 92])
S6.add('Kế hoạch Đã duyệt hiện ở popup Chọn kế hoạch', 'P0', [ACC_K, KH2],
       ['Đăng nhập K.', 'Vào phân hệ Kho > Kiểm kho > Kiểm kê theo hàng hóa, bấm Tạo mới, mở ô chọn kế hoạch.'], '—',
       ['Popup chọn kế hoạch có KH2 (loại Kế hoạch tổng kiểm kê).'], [307, 274])

# ============================================================== VII. LỊCH SỬ THAY ĐỔI
S7 = Sec(7)
PRE_H = [PRE_LIST, P3]
HIS = [MENU, 'Ở dòng TPE.KHTKK-00003 bấm Lịch sử.']
S7.add('Mở cửa sổ lịch sử', 'P0', PRE_H, HIS, '—', ['Cửa sổ "Lịch sử thay đổi: TPE.KHTKK-00003".'], 162)
S7.add('Các thông tin của mốc', 'P0', PRE_H, HIS, '—',
       ['Mỗi mốc: thời điểm, hành động, "Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ", nội dung.'], [163, 165, 166, 167])
S7.add('Mới nhất trước', 'P0', PRE_H, HIS, '—',
       ['4 mốc: trên cùng 27/10/2026 15:55 Thay đổi trạng thái, dưới cùng 26/10/2026 15:21 Tạo mới.'], 164)
S7.add('Nội dung thay đổi trạng thái và thông tin', 'P0', PRE_H, HIS, '—',
       ['Mốc Thay đổi trạng thái: "Trạng thái: Đang tạo > Đã duyệt".',
        'Mốc Thay đổi thông tin 27/10: Kho, Công ty thuê kho (mã), Thành phần tham gia (tên) cũ > mới.'], [168, 281])
S7.add('Lọc theo hành động', 'P1', PRE_H, HIS + ['Bấm Bộ lọc, chọn Loại hành động = Tạo mới.'], '—', ['Chỉ còn mốc Tạo mới.'], 169)
S7.add('Lọc theo người thực hiện', 'P2', PRE_H, HIS + ['Bấm Bộ lọc, chọn Người thực hiện = DNS Admin.'], '—', ['Còn đủ 4 mốc.'], 170)
S7.add('Lọc theo thời gian', 'P1', PRE_H, HIS + ['Bấm Bộ lọc, Từ ngày 27/10/2026.'], '—', ['Còn 2 mốc ngày 27/10/2026.'], 171)
S7.add('Kết hợp lọc', 'P2', PRE_H, HIS + ['Chọn Loại hành động = Thay đổi thông tin, Từ ngày 27/10/2026.'], '—', ['Còn 1 mốc.'], 172)
S7.add('Không có kết quả lọc', 'P2', PRE_H, HIS + ['Đến ngày 25/10/2026.'], '—', ['"Không có lịch sử phù hợp bộ lọc.".'], 173)
S7.add('Làm mới / đóng mở bộ lọc', 'P2', PRE_H, HIS + ['Lọc rồi bấm Làm mới.', 'Bấm Bộ lọc lần nữa.'], '—',
       ['Làm mới: hiện lại 4 mốc.', 'Bộ lọc thu gọn / mở lại.'], [174, 175])
S7.add('Kế hoạch chưa có lịch sử', 'P1', [PRE_LIST, 'Kế hoạch KH9 lập trên hệ thống cũ, chưa có thao tác nào ở hệ thống mới.'],
       [MENU, 'Bấm Lịch sử dòng KH9.'], '—', ['"Chưa có lịch sử thao tác nào.".'], 162)
S7.add('Sửa không đổi gì thì không ghi', 'P1', [ACC_A, KH1], ['Sửa KH1, không đổi, bấm Lưu nháp.', 'Mở Lịch sử.'], '—',
       ['Không có mốc "Thay đổi thông tin" mới.'], [182, 125])
S7.add('Đổi nhiều thông tin cùng lúc', 'P1', [ACC_A, KH1], ['Sửa KH1: đổi Ngày kiểm kê đến + Nội dung yêu cầu, bấm Lưu và duyệt.', 'Mở Lịch sử.'],
       '—', ['1 mốc "Thay đổi thông tin" liệt kê Ngày kiểm kê đến và Nội dung yêu cầu (cũ > mới) + 1 mốc "Thay đổi trạng thái".'], 183)
S7.add('Đóng cửa sổ', 'P1', PRE_H, HIS + ['Bấm Đóng.', 'Mở lại, bấm (x).'], '—', ['Cả 2 cách đều đóng cửa sổ.'], 184)
S7.add('Trạng thái danh sách sau khi đóng', 'P1', 'Đang ở trang 2, lọc Trạng thái = Đang tạo, số dòng 5.', ['Mở Lịch sử 1 dòng, bấm Đóng.'], '—',
       ['Danh sách giữ trang 2, bộ lọc, sắp xếp.'], 185)
S7.add('Lịch sử ở màn chi tiết', 'P1', PRE_H, [MENU, 'Bấm TPE.KHTKK-00003.', 'Ở khối Lịch sử bấm Xem lịch sử.'], '—',
       ['Khối Lịch sử có số 4; bấm mở rộng hiện 4 mốc như cửa sổ; nút đổi thành Thu gọn.'], [195, 162])

# ============================================================== VIII. XEM CHI TIẾT
S8 = Sec(8)
DET = [MENU, 'Bấm TPE.KHTKK-00005.']
PRE_D = [PRE_LIST, P5]
S8.add('Mở màn chi tiết', 'P0', PRE_D, DET, '—', ['Mở TRANG chi tiết (không phải cửa sổ nổi).'], 186)
S8.add('Tiêu đề', 'P0', PRE_D, DET, '—', ['"Chi tiết kế hoạch tổng kiểm kê hàng hóa: TPE.KHTKK-00005" (không kèm nhãn trạng thái).'], 187)
S8.add('Đầy đủ trường', 'P0', PRE_D, DET, '—',
       ['Thông tin chung: Số phiếu, Ngày kiểm kê từ 07/11/2026, Ngày kiểm kê đến 07/11/2026, Kho (3 tên kho), Công ty thuê kho '
        '"TPE, TPV", Thành phần tham gia (3 tên phòng ban), Nội dung yêu cầu "test 1uuq2yi"; góc phải "DNS Admin - 05/11/2026 15:08".',
        'Khối Lịch sử.'], 188)
S8.add('Khớp dữ liệu tạo và danh sách', 'P0', PRE_D, DET, '—', ['Ngày kiểm kê, kho, nội dung, người tạo khớp dòng ở danh sách.'], [189, 190])
S8.add('Trường chỉ đọc, không có nút Lưu', 'P0', PRE_D, DET, '—',
       ['Mọi ô khóa, không có dấu *.', 'Chân màn không có Lưu nháp / Lưu và duyệt.'], [191, 192])
S8.add('Nút theo trạng thái ở chi tiết', 'P0', [ACC_A, KH1, KH2], ['Mở chi tiết KH1.', 'Mở chi tiết KH2.'], '—',
       ['KH1: Sửa, In, Xóa, Quay lại.', 'KH2 (A không có quyền lập phiếu): In, Quay lại.'], [193, 194])
S8.add('Quay lại giữ trang và bộ lọc', 'P0', 'Đang ở trang 2, lọc Trạng thái = Đang tạo, số dòng 5.', ['Bấm số phiếu 1 dòng.', 'Bấm Quay lại.'], '—',
       ['Về danh sách giữ bộ lọc Trạng thái = Đang tạo (trong 10 phút).'], [196, 197])
S8.add('Kế hoạch ngoài phạm vi', 'P0', [ACC_B, 'Kế hoạch KH7 công ty TPSG do người khác tạo.'], ['Đăng nhập B.', 'Mở đường link chi tiết KH7.'], '—',
       ['Chuyển sang trang "Không tìm thấy trang".'], [186, 296])
S8.add('Lập phiếu kiểm kê từ màn chi tiết', 'P0', [ACC_K, KH2], ['Đăng nhập K.', 'Mở chi tiết KH2.', 'Bấm %s.' % LAP], '—',
       ['Mở màn "Tạo phiếu kiểm kê theo hàng hóa" (phân hệ Kho) cùng tab với KH2 đã chọn sẵn ở ô Kế hoạch kiểm kê: Kho, Công ty thuê '
        'kho, Ghi chú = Nội dung yêu cầu; bảng Hàng hóa trống, thêm hàng được.'], [274, 193])
S8.add('Lập phiếu kiểm kê từ danh sách', 'P1', [ACC_K, KH2], ['Đăng nhập K.', MENU, 'Bấm nút %s ở dòng KH2.' % LAP], '—',
       ['Dòng KH2 có nút %s, In, Lịch sử; bấm mở màn Tạo phiếu kiểm kê như ở chi tiết.' % LAP], 274)
S8.add('Hết hạn lập phiếu khi đợt kiểm đã bắt đầu', 'P0', [ACC_K, KH3], ['Đăng nhập K.', 'Mở chi tiết KH3.'], '—',
       ['Không có nút %s (Ngày kiểm kê từ đã qua).' % LAP,
        'Lưu ý: điều kiện giữ như hệ thống cũ — kế hoạch đang trong đợt kiểm cũng không lập thêm phiếu được.'], [193, 304])
S8.add('Lập nhiều phiếu kiểm kê từ 1 kế hoạch', 'P1', [ACC_K, KH2, 'Đã có phiếu kiểm kê P1 lập từ KH2 chứa hàng Máy tính xách tay.'],
       ['Bấm %s ở KH2 lần nữa.' % LAP, 'Thêm hàng MẶT NẠ BẢO VỆ, lưu phiếu.', 'Lập phiếu thứ 3, thêm Máy tính xách tay, lưu.'], '—',
       ['Phiếu thứ 2 lưu được; KH2 vẫn Đã duyệt.', 'Phiếu thứ 3 bị chặn: "Hàng hóa đã lập phiếu kiểm kê." ở dòng Máy tính xách tay.'],
       [274, 286])
S8.add('Không có quyền thì không thấy Lập phiếu', 'P0', [ACC_C, KH2], ['Đăng nhập C.', 'Mở chi tiết KH2.'], '—',
       ['Không có nút %s.' % LAP], [193, 295])

# ============================================================== IX. IN PHIẾU
S9 = Sec(9)
S9.add('In phiếu từ danh sách', 'P0', PRE_D, [MENU, 'Bấm In ở dòng TPE.KHTKK-00005.'], '—',
       ['Cửa sổ "Xem trước kế hoạch tổng kiểm kê hàng hóa TPE.KHTKK-00005".',
        'Bản in: logo / tên công ty TÂN PHÁT của kế hoạch, "KẾ HOẠCH TỔNG KIỂM KÊ HÀNG HÓA", "Số phiếu: TPE.KHTKK-00005", "Ngày lập: '
        '05/11/2026".', 'Thời gian kiểm kê: "Từ ngày 07/11/2026 đến ngày 07/11/2026"; Kho vật lý: 3 tên kho; Công ty thuê kho: "TPE, '
        'TPV"; Thành phần tham gia: 3 tên phòng ban; Nội dung yêu cầu: "test 1uuq2yi".',
        'Chỗ ký "Ngày … Tháng … Năm …" (ngày in), Người lập DNS Admin, sát lề phải.'], 228)
S9.add('In phiếu từ màn chi tiết', 'P1', PRE_D, DET + ['Bấm In.'], '—', ['Cùng cửa sổ xem trước như in từ danh sách.'], 228)
S9.add('Letterhead theo công ty của kế hoạch', 'P1', ['Tài khoản T thuộc công ty TPSG.', P5], ['Đăng nhập T.', 'In TPE.KHTKK-00005.'], '—',
       ['Đầu bản in là letterhead công ty TPE (công ty ghi trên kế hoạch), không phải TPSG.'], 228)
S9.add('Bấm In trong cửa sổ', 'P1', 'Đang mở cửa sổ xem trước.', ['Bấm In.'], '—', ['Mở hộp thoại in của trình duyệt.'], 228)
S9.add('In danh sách theo bộ lọc', 'P0', PRE_LIST, [MENU, 'Lọc Trạng thái = Đã duyệt.', 'Bấm In danh sách.'], '—',
       ['Cửa sổ "Xem trước danh sách kế hoạch tổng kiểm kê hàng hóa".',
        'Bảng 5 dòng: STT, Số phiếu, Thời gian kiểm kê, Kho, Nội dung yêu cầu, Người tạo, Ngày tạo (kèm giờ), Trạng thái; khối ký '
        '"Ngày … Tháng … Năm …", Người lập (người in).'], [220, 227])
S9.add('In danh sách vượt 2.000 dòng', 'P2', 'Bộ lọc ra hơn 2.000 kế hoạch.', ['Bấm In danh sách.'], '—',
       ['Không có bản xem trước, ẩn nút In, hiện dòng nhắc thu hẹp bộ lọc.'], 221)
S9.add('In danh sách rỗng', 'P2', 'Bộ lọc không ra kế hoạch nào.', ['Bấm In danh sách.'], '—', ['"Không có dữ liệu để in".'], 222)
S9.add('Đóng cửa sổ xem trước', 'P2', 'Đang mở cửa sổ xem trước.', ['Bấm (x).'], '—', ['Đóng, giữ nguyên màn đang đứng.'], 184)

# ============================================================== X. TÙY CHỈNH CỘT
S10 = Sec(10)
S10.add('Mở cửa sổ tùy chỉnh cột', 'P0', PRE_LIST, [MENU, 'Bấm nút biểu tượng cột.'], '—',
        ['Cửa sổ "Tuỳ chỉnh cột" liệt kê 11 cột, "Đang chọn 11/11 cột".'], [198, 199, 200])
S10.add('Ẩn cột', 'P0', PRE_LIST, ['Bỏ tích Ngày cập nhật, bấm Lưu.'], '—', ['"Cập nhật thành công", bảng không còn cột Ngày cập nhật.'], [202, 206])
S10.add('Hiện cột đã ẩn', 'P1', 'Đã ẩn Ngày cập nhật.', ['Tích lại Ngày cập nhật, bấm Lưu.'], '—', ['Cột hiện lại.'], 201)
S10.add('Cột bắt buộc không ẩn', 'P0', PRE_LIST, ['Mở cửa sổ, thử bỏ tích STT, Số phiếu, Hành động.'], '—',
        ['3 cột có biểu tượng ổ khóa, không bỏ tích, không kéo được.'], [203, 205])
S10.add('Kéo thả thứ tự', 'P1', PRE_LIST, ['Kéo Trạng thái xuống sau Người cập nhật, bấm Lưu.'], '—', ['Bảng hiện Trạng thái sau Người cập nhật.'], 204)
S10.add('Chọn tất cả / Bỏ chọn hết', 'P2', PRE_LIST, ['Bấm Bỏ chọn hết.', 'Bấm Chọn tất cả.'], '—',
        ['Bỏ chọn hết: còn 3 cột khóa.', 'Chọn tất cả: 11/11.'], 202)
S10.add('Đóng không lưu', 'P1', PRE_LIST, ['Bỏ tích Kho, bấm Đóng.'], '—', ['Bảng vẫn có cột Kho.'], 207)
S10.add('Ghi nhớ sau F5 và theo tài khoản', 'P1', 'A đã ẩn cột Ngày cập nhật.', ['Nhấn F5.', 'Đăng nhập B trên cùng máy.'], '—',
        ['A: vẫn ẩn sau F5 và đăng nhập máy khác.', 'B: thấy đủ 11 cột.'], [208, 209])
S10.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', 'Đang lọc Trạng thái = Đã duyệt (5).', ['Ẩn cột Kho, bấm Lưu.'], '—',
        ['Vẫn 5 kế hoạch, bộ lọc giữ nguyên.'], [210, 211])

# ============================================================== XI. XUẤT DANH SÁCH EXCEL
S11 = Sec(11)
S11.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel.'], '—',
        ['Cửa sổ "Chọn trường xuất Excel" với 9 trường: Số phiếu, Thời gian kiểm kê, Kho, Nội dung yêu cầu, Trạng thái, Người tạo, '
         'Ngày tạo, Ngày cập nhật, Người cập nhật; tích sẵn theo cột đang hiện ("Đang chọn 9/9 trường").'], [212, 213, 214])
S11.add('Xuất trường mặc định', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel, bấm Xuất file.'], '—',
        ['Tải "danh_sach_ke_hoach_tong_kiem_ke_hang_hoa.xlsx", báo "Xuất Excel thành công.".',
         'File: letterhead, "DANH SÁCH KẾ HOẠCH TỔNG KIỂM KÊ HÀNG HÓA", cột STT + 9 trường, 12 dòng, khối ký; dòng tên cột in đậm, '
         'không tô nền.'], [215, 216, 223, 224, 225, 227])
S11.add('Xuất một số trường theo thứ tự kéo', 'P1', PRE_LIST, ['Bỏ chọn hết, tích Kho rồi Số phiếu, kéo Kho lên đầu, Xuất file.'], '—',
        ['File chỉ có STT, Kho, Số phiếu theo đúng thứ tự.'], [217, 226])
S11.add('Không chọn trường', 'P1', PRE_LIST, ['Bấm Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S11.add('Xuất theo tìm kiếm / bộ lọc', 'P0', PRE_LIST, ['Lọc Trạng thái = Đã duyệt, Ngày tạo 01/10/2026 – 31/10/2026.', 'Xuất file.'],
        '—', ['File chỉ có 4 kế hoạch khớp (00001 … 00004); có dòng "Từ ngày 01/10/2026 đến ngày 31/10/2026".'], [219, 220])
S11.add('Xuất nhiều trang', 'P1', PRE_LIST, ['Đang ở trang 1 (10 dòng), Xuất file.'], '—', ['File có đủ 12 dòng, không chỉ trang đang xem.'], 221)
S11.add('Danh sách rỗng', 'P2', 'Bộ lọc không ra kế hoạch nào.', ['Xuất file.'], '—',
        ['Vẫn ra file có tiêu đề, dòng tên cột, khối ký, không có dòng dữ liệu.'], 222)
S11.add('Dữ liệu khớp, định dạng ngày và tiếng Việt', 'P1', [PRE_LIST, P5], ['Xuất file, mở dòng TPE.KHTKK-00005.'], '—',
        ['Thời gian kiểm kê "07/11/2026 - 07/11/2026".', 'Ngày tạo "05/11/2026 15:08" giữ dạng chữ; Kho, Trạng thái "Đã duyệt" đủ dấu '
         'tiếng Việt.'], [228, 229, 230])
S11.add('Không có xuất Excel 1 kế hoạch', 'P2', PRE_D, [MENU, 'Quan sát cột Hành động dòng TPE.KHTKK-00005.', 'Mở chi tiết.'], '—',
        ['Không có nút Xuất Excel ở dòng và ở màn chi tiết (hệ thống cũ cũng không có).'], [223, 293])

# ============================================================== XII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S12 = Sec(12)
S12.add('Chỉ kế hoạch Đã duyệt còn hạn hiện ở popup Chọn kế hoạch', 'P0', [ACC_K, KH1, KH2, KH3],
        ['Đăng nhập K.', 'Vào phân hệ Kho > Kiểm kho > Kiểm kê theo hàng hóa, bấm Tạo mới, mở ô chọn kế hoạch.'], '—',
        ['Popup có KH2; không có KH1 (Đang tạo) và KH3 (Ngày kiểm kê từ đã qua).'], [274, 276])
S12.add('Lập phiếu kiểm kê không đổi trạng thái kế hoạch', 'P0', [ACC_K, KH2], ['Lập và lưu phiếu kiểm kê từ KH2.', 'Mở danh sách kế hoạch.'], '—',
        ['KH2 vẫn Đã duyệt; lịch sử KH2 không có mốc mới.'], [281, 284])
S12.add('Bộ lọc Mã hàng của màn này cập nhật theo phiếu kiểm kê', 'P2', [ACC_K, KH2],
        ['Lập phiếu kiểm kê từ KH2 có hàng ACER-A315-34-P3LC.', 'Ở danh sách kế hoạch lọc Mã hàng hóa "ACER-A315".'], '—',
        ['KH2 xuất hiện trong kết quả lọc.'], 282)
S12.add('Lưu phiếu kiểm kê khi kế hoạch không còn Đã duyệt', 'P1', [ACC_K, 'Kế hoạch KH8 Đã duyệt bị đưa về trạng thái khác ở hệ thống cũ.'],
        ['Tab 1 mở Tạo phiếu kiểm kê từ KH8.', 'KH8 đổi trạng thái.', 'Tab 1 bấm Lưu.'], '—', ['Tab 1 báo ' + CONFLICT + '.'], 282)
S12.add('Liên kết từ phiếu kiểm kê mở kế hoạch', 'P1', [ACC_K, 'Phiếu kiểm kê P1 lập từ TPE.KHTKK-00005.'],
        ['Mở danh sách Kiểm kê theo hàng hóa, bấm số kế hoạch ở dòng P1.'], '—', ['Mở chi tiết TPE.KHTKK-00005.'], [272, 279])
S12.add('Báo cáo hàng thừa thiếu lọc theo kế hoạch', 'P1', [ACC_K, 'Phiếu kiểm kê P1 lập từ TPE.KHTKK-00005 đã Hoàn thành, có chênh lệch.'],
        ['Vào phân hệ Kho > Báo cáo kho > Báo cáo hàng thừa thiếu sau tổng kiểm kê hàng hóa.', 'Ở ô Kế hoạch tổng kiểm kê chọn '
                                                                                             'TPE.KHTKK-00005, xem báo cáo.'], '—',
        ['Popup chọn liệt kê mọi kế hoạch tổng; báo cáo chỉ còn dòng của phiếu kiểm kê lập từ TPE.KHTKK-00005; dòng tóm tắt ghi số '
         'kế hoạch.'], [274, 282])
S12.add('Không xóa được kho vật lý đang dùng', 'P0', [ACC_A, KH2], ['Vào phân hệ Kho > Danh mục > Kho vật lý, xóa kho Chăm sóc khách hàng.'], '—',
        ['Hệ thống chặn xóa vì kho đang được dùng.'], 270)
S12.add('Đổi tên kho hiển thị theo tên mới', 'P1', [ACC_A, KH2], ['Đổi tên kho Chăm sóc khách hàng ở danh mục Kho vật lý.', 'Mở chi tiết KH2.'], '—',
        ['Ô Kho của KH2 hiện tên kho mới (kế hoạch lưu liên kết tới kho, không lưu chữ).'], [272, 278])
S12.add('Kế hoạch mới xuất hiện ở màn liên quan', 'P1', [ACC_K, PRE_FORM], ['A tạo và Lưu và duyệt kế hoạch có Ngày kiểm kê từ = ngày mai.', 'K mở popup Chọn kế hoạch.'],
        '—', ['Kế hoạch mới có trong popup.'], 274)
S12.add('Tồn kho không đổi khi lưu kế hoạch', 'P0', PRE_FORM, ['Ghi tồn hàng Máy tính xách tay tại kho CSKH.', 'Tạo và Lưu và duyệt kế hoạch.', 'Xem lại tồn.'],
        '—', ['Tồn không đổi (kế hoạch không ghi tồn).'], 286)
S12.add('Công ty thuê kho đúng kho cha', 'P1', PRE_FORM, TAO + ['Chọn Kho HP - Hải Phòng.', 'Mở ô Công ty thuê kho.'], '—',
        ['Chỉ liệt kê công ty có kho kế toán trong kho Hải Phòng.'], [283, 280])

# ============================================================== XIII. PHÂN QUYỀN (cuối)
S13 = Sec(13)
S13.add('Quyền tổng công ty: xem mọi kế hoạch', 'P0', [ACC_T, 'Có 5 kế hoạch Đã duyệt của TPE và 2 kế hoạch Đã duyệt của TPSG.'], ['Đăng nhập T.', MENU], '—',
        ['Thấy đủ 7 kế hoạch; có ô Công ty – Phòng ban, chọn được mọi công ty.'], [287, 299])
S13.add('Quyền công ty: chỉ công ty mình + của mình', 'P0', [ACC_C, 'TPE có 5 kế hoạch Đã duyệt, TPSG 2.'], ['Đăng nhập C.', MENU], '—',
        ['Chỉ thấy 5 kế hoạch TPE (và kế hoạch C tự tạo); ô Công ty khóa ở TPE.'], [287, 299])
S13.add('Không quyền: chỉ kế hoạch mình tạo', 'P0', [ACC_A, 'A tạo 2 kế hoạch.'], ['Đăng nhập A.', MENU], '—',
        ['Chỉ thấy 2 kế hoạch của A; không có ô Công ty – Phòng ban.'], [287, 299])
S13.add('Đang tạo chỉ người tạo thấy', 'P0', [ACC_T, KH1], ['Đăng nhập T.', MENU, 'Tìm số phiếu KH1.'], '—',
        ['T không thấy KH1 dù có quyền tổng công ty.'], [287, 299])
S13.add('Xem chi tiết theo phạm vi', 'P0', [ACC_C, 'Kế hoạch KH7 công ty TPSG.'], ['Đăng nhập C.', 'Mở đường link chi tiết KH7.'], '—',
        ['Trang "Không tìm thấy trang".'], [288, 296])
S13.add('Có quyền Lập phiếu xem kế hoạch Đã duyệt', 'P0', [ACC_K, KH2], ['Đăng nhập K.', 'Mở chi tiết KH2 từ thông báo.'], '—',
        ['Mở được (ngoại lệ cho người có quyền "%s").' % Q1], 288)
S13.add('Thêm mới không cần quyền', 'P0', ACC_B, ['Đăng nhập B.', MENU, 'Bấm Tạo mới, nhập đủ, bấm Lưu nháp.'], FULL, ['Lưu thành công.'], 289)
S13.add('Sửa chỉ người tạo', 'P0', [ACC_T, 'Kế hoạch KH5 Đang tạo do T tạo, KH2 do A tạo.'], ['Đăng nhập T.', MENU], '—',
        ['KH5 có Sửa; KH2 không có Sửa (không phải người tạo, không Đang tạo).'], [290, 295])
S13.add('Xóa chỉ người tạo', 'P0', [ACC_T, 'KH5 Đang tạo do T tạo.'], ['Đăng nhập T.', MENU], '—', ['Chỉ KH5 có nút Xóa.'], [291, 295])
S13.add('Xuất / In / Lịch sử theo phạm vi', 'P1', ACC_A, ['Đăng nhập A.', MENU, 'Xuất Excel; mở Lịch sử 1 kế hoạch của A.'], '—',
        ['File chỉ chứa kế hoạch của A; lịch sử xem được.'], [293, 294])
S13.add('Lập phiếu kiểm kê cần quyền', 'P0', [ACC_K, KH2, 'Tài khoản C không có quyền "%s".' % Q1],
        ['Đăng nhập K, mở chi tiết KH2.', 'Đăng nhập C, mở chi tiết KH2.'], '—',
        ['K: có nút %s.' % LAP, 'C: không có nút.'], [295, 287])
S13.add('Mở đường link màn Sửa khi không phải người tạo', 'P0', [ACC_C, 'KH6 Đã duyệt công ty TPE do A tạo.'],
        ['Đăng nhập C.', 'Mở đường link màn Sửa của KH6.'], '—', ['Tự chuyển sang màn chi tiết KH6, không sửa được.'], 296)
S13.add('Thao tác bị chặn lại ở máy chủ', 'P1', [ACC_A, KH1], ['Tab 1 mở danh sách.', 'Tab 2 Lưu và duyệt KH1.', 'Tab 1 bấm Xóa KH1.'], '—',
        ['Báo ' + CONFLICT + '; máy chủ kiểm lại điều kiện ở từng thao tác, không dựa vào việc ẩn nút.'], 297)
S13.add('Đổi quyền giữa thao tác', 'P1', [ACC_C, 'Quản trị gỡ quyền "Tổng kiểm kê kho theo hàng hóa" của C khi C đang ở danh sách.'],
        ['C bấm sang trang 2 / mở chi tiết kế hoạch TPE của người khác.'], '—',
        ['Danh sách chỉ còn kế hoạch của C; chi tiết kế hoạch người khác > "Không tìm thấy trang".'], 298)
S13.add('Super admin có đủ quyền', 'P2', 'Tài khoản DNS Admin (Super admin), không gán quyền riêng.', ['Đăng nhập DNS Admin.', MENU], '—',
        ['Thấy mọi kế hoạch không Đang tạo của mọi công ty, có ô Công ty – Phòng ban, có nút %s ở kế hoạch còn hạn.' % LAP], 287)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'CHỈNH SỬA', S4),
    ('V', 'XÓA', S5),
    ('VI', 'DUYỆT PHIẾU', S6),
    ('VII', 'LỊCH SỬ THAY ĐỔI', S7),
    ('VIII', 'XEM CHI TIẾT KẾ HOẠCH TỔNG KIỂM KÊ', S8),
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
    build_chuan(output_file=OUT, sheet_name='Trang tính1', feature_name='Kế hoạch tổng kiểm kê hàng hóa - Cập nhật ngày 05/11/2026',
                module_name='Kế hoạch tổng kiểm kê hàng hóa', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

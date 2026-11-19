# -*- coding: utf-8 -*-
"""Testcase màn "Biên bản xử lý hàng thừa, thiếu sau kiểm kê" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan,
loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (không phải danh mục) — lý do từ code: màn là chứng từ có số tự sinh BBXLKKHH-NNNNN (InventoryAuditReport::generateCode),
vòng đời trạng thái Đang tạo > Chờ duyệt > Đã duyệt (InventoryAuditReport::STATUSES), Lưu và gửi duyệt (gửi thông báo), Duyệt riêng
theo quyền (ghi bút toán), In phiếu (mẫu in), lịch sử; không có Khóa / Mở khóa như danh mục.
Nhóm theo đúng tên + thứ tự chuẩn loại 'phieu' (check_tc.THU_TU), bỏ nhóm màn không có (kiểm code 06/11/2026: không có route / nút
Xóa, Khóa, Không duyệt, Hủy, Import):
I Hiển thị · II Tìm kiếm & lọc (gồm Cài đặt bộ lọc) · III Thêm mới (Lấy dữ liệu, Lưu, Lưu và tiếp tục, rời màn) · IV Chỉnh sửa ·
V Gửi duyệt · VI Duyệt phiếu · VII Lịch sử · VIII Xem chi tiết · IX In phiếu (kèm In danh sách) · X Tùy chỉnh cột · XI Xuất danh sách
Excel (kèm Xuất 1 biên bản) · XII Ràng buộc · XIII Phân quyền.
Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../ke-hoach-tong-kiem-ke-hang-hoa/gen_testcase.py (05/11, qua check_tc 0 lỗi).
Nguồn hành vi (đọc 06/11/2026, nhánh develop): FE pages/finance/inventory-audit-reports/**; BE Modules/Finance InventoryAuditReport*
(Entity / Service / WriteService / PrintService / Controller / StoreRequest / ApproveRequest).
Số liệu mẫu: dev-hrm 06/11/2026 (DNS Admin) 6 biên bản BBXLKKHH-00001 … 00006: 4 Đã duyệt (00001, 00003, 00005, 00006), 2 Chờ duyệt
(00002, 00004); 00006 kho Liên Ninh, phiếu kiểm kê TPE.KKK-01068, 01069, 2 hàng thừa + 1 hàng thiếu, có 3 mốc lịch sử.
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
from tc_phieu_bosung import ListScreen, open_menu_case, filter_memory_cases, combo_cases, check_no_dash_pre  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Tài chính > menu "Kiểm kê" > bấm "Biên bản xử lý hàng thừa, thiếu sau kiểm kê".'
TAO = [MENU, 'Bấm "Tạo mới".']
ADV = 'Bấm Tìm kiếm nâng cao.'
Q1 = 'Kế toán kho'
Q2 = 'Duyệt biên bản xử lý hàng thừa, thiếu sau kiểm kê'
V1 = 'Xem biên bản xử lý hàng thừa, thiếu sau kiểm kê - theo tổng công ty'
V2 = 'Xem biên bản xử lý hàng thừa, thiếu sau kiểm kê - theo công ty'
MISS = '"Bạn chưa nhập đầy đủ thông tin."'
CONFLICT = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'
NOTFOUND = 'trang "Không tìm thấy trang"'
NOPERM = '"Bạn không có quyền thực hiện chức năng này."'
CHANGED = '"Dữ liệu kiểm kê đã thay đổi. Vui lòng bấm "Lấy dữ liệu" lại."'

ACC_A = 'Tài khoản A: kế toán kho công ty TPE, có quyền "%s", không có quyền xem theo cấp.' % Q1
ACC_B = 'Tài khoản B: nhân viên công ty TPE, không có quyền nào của màn.'
ACC_C = 'Tài khoản C: có quyền "%s", thuộc công ty TPE.' % V2
ACC_T = 'Tài khoản T: có quyền "%s".' % V1
ACC_D = 'Tài khoản D: có quyền "%s", thuộc công ty TPE, không có quyền xem theo cấp.' % Q2
PRE_LIST = ('Tài khoản DNS Admin (Super admin); trong phạm vi xem có 13 biên bản: 6 biên bản BBXLKKHH-00001 … 00006 (4 Đã duyệt, 2 '
            'Chờ duyệt) và 7 biên bản Đang tạo do DNS Admin lưu để thử.')
P6 = ('Biên bản BBXLKKHH-00006: Từ ngày 22/10/2026, Đến ngày 22/10/2026, kho LN - Liên Ninh, phiếu kiểm kê TPE.KKK-01068 và '
      'TPE.KKK-01069; tab Hàng thừa 2 dòng, tab Hàng thiếu 1 dòng; 1 file ảnh đính kèm; Đã duyệt; Người tạo, Người duyệt DNS Admin; '
      'Ngày tạo 22/10/2026 14:58, Ngày duyệt 22/10/2026 15:00.')
SRC = ('Kho LN - Liên Ninh có 2 phiếu kiểm kê theo hàng hóa Hoàn thành ngày 22/10/2026: TPE.KKK-01068 (thừa 1 Bộ điều khiển từ xa '
       'MULTIFLEX 06 EASY) và TPE.KKK-01069 (thừa 1 Công tắc nguồn KS350.30038, thiếu 1 Rơ le điện KS350.30039); đã có phiếu nhập '
       'kho điều chỉnh kiểm kê PNHĐCKK-00041, 00042 và phiếu xuất PXHĐCKK-00068 Hoàn thành.')
PRE_FORM = ACC_A + '\n' + SRC
GET = TAO + ['Chọn Từ ngày 22/10/2026, Đến ngày 22/10/2026, Kho vật lý LN - Liên Ninh.', 'Bấm "Lấy dữ liệu".']
FILL = GET + ['Ở cả 3 dòng (2 tab) nhập Lý do "Chênh lệch kiểm kê", giữ Giá xử lý Giá vốn, % Chi phí nhân viên 100, chọn NV chịu '
              '"Bùi Duy Trước".']
FULL = ['Từ ngày: 22/10/2026', 'Đến ngày: 22/10/2026', 'Kho vật lý: LN - Liên Ninh', 'Lý do: Chênh lệch kiểm kê',
        'Giá xử lý: Giá vốn', '% Chi phí nhân viên: 100', 'NV chịu: Bùi Duy Trước']
BB1 = 'Biên bản BB1 trạng thái Đang tạo do A lập từ dữ liệu kho Liên Ninh ngày 22/10/2026 (3 dòng đã nhập đủ).'
BB2 = 'Biên bản BB2 trạng thái Chờ duyệt do A lập (3 dòng, NV chịu Bùi Duy Trước, % nhân viên 100).'
OK_SAVE = 'Báo "Lưu thành công.", về màn danh sách; dòng mới ở trên cùng, trạng thái Đang tạo (nhãn xám).'

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
     'Lập biên bản xử lý hàng thừa, thiếu sau kiểm kê: lấy kết quả các phiếu kiểm kê theo hàng hóa đã Hoàn thành của một kho trong '
     'khoảng ngày, ghi cho từng hàng thừa / thiếu lý do, giá xử lý (giá vốn / giá bán), % chi phí nhân viên / công ty, nhân viên chịu; '
     'gửi duyệt; người có quyền Duyệt chốt và hệ thống ghi bút toán. Biên bản KHÔNG làm đổi tồn kho.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Danh sách: biên bản trong phạm vi xem; trạng thái Đang tạo (nhãn xám), Chờ duyệt (nhãn cam), Đã duyệt (nhãn xanh lá).\n'
     '- Lấy dữ liệu: phiếu kiểm kê theo hàng hóa Hoàn thành, có kho đã chọn, ngày kiểm kê trong Từ ngày – Đến ngày, hàng có chênh '
     'lệch khác 0.\n- Tab Hàng thừa: chênh lệch > 0; tab Hàng thiếu: chênh lệch < 0.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Biên bản Đang tạo của người khác (kể cả với quyền tổng công ty).\n- Biên bản ngoài phạm vi quyền xem.\n'
     '- Phiếu kiểm kê chưa Hoàn thành, khác kho, ngoài khoảng ngày; hàng chênh lệch 0.\n'
     '- Dòng của phiếu kiểm kê bị bỏ tích (không lưu).'),
    ('4. Bộ lọc thời gian áp dụng cho',
     '- Ô Ngày tạo ở danh sách lọc theo NGÀY TẠO biên bản, lấy trọn hai ngày biên.\n'
     '- Từ ngày / Đến ngày trên form lọc phiếu kiểm kê theo NGÀY KIỂM KÊ.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Biên bản > các phiếu kiểm kê (ô tích) > các dòng hàng thừa / thiếu > phiếu xử lý (phiếu nhập / xuất kho điều chỉnh kiểm kê).'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Một hàng trong một phiếu kiểm kê cộng dồn mọi chênh lệch thành 1 dòng.\n'
     '- Cột Hàng thừa / Hàng thiếu ở danh sách = tổng SL các dòng thừa / thiếu đã lưu.\n'
     '- Bút toán khi Duyệt cộng theo từng nhân viên chịu.'),
    ('7. Phân quyền cấp',
     '- Kế toán kho: Tạo mới, Lấy dữ liệu.\n'
     '- Duyệt biên bản xử lý hàng thừa, thiếu sau kiểm kê: nút Duyệt, thấy mọi biên bản Chờ duyệt, nhận thông báo.\n'
     '- Xem biên bản xử lý hàng thừa, thiếu sau kiểm kê - theo tổng công ty: mọi biên bản.\n'
     '- Xem biên bản xử lý hàng thừa, thiếu sau kiểm kê - theo công ty: công ty mình + của mình.\n'
     '- Không quyền: biên bản mình tạo. Sửa: người tạo, khi Đang tạo.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là khoảng thứ tự dòng của trang, N là tổng biên bản khớp bộ lọc trong phạm vi xem.\n'
     '- Thành tiền = Đơn giá × SL; Chi phí nhân viên = thành tiền (vốn hoặc bán theo Giá xử lý) × % nhân viên.\n'
     '- % Chi phí công ty = 100 - % Chi phí nhân viên.\n'
     '- Lưu ý: Chi phí công ty LƯU bằng Chi phí nhân viên (giữ như hệ thống cũ) — màn tính theo %, bản in / Excel in số đã lưu.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: A (kế toán kho), B (không quyền), C (xem theo công ty), T (xem tổng công ty), D (quyền Duyệt), '
     'DNS Admin (Super admin).\n'
     '- Lưu ý: Lưu và Lưu và gửi duyệt bắt CÙNG một bộ trường (mọi dòng phải đủ Lý do, Giá xử lý, %, NV chịu).\n'
     '- Lưu ý: Lưu và gửi duyệt, Duyệt đều KHÔNG có hộp xác nhận; Duyệt ghi bút toán — chạy trên dữ liệu thử.\n'
     '- Lưu ý: đổi Từ ngày / Đến ngày / Kho vật lý thì phải Lấy dữ liệu lại mới lưu được.\n'
     '- Màn Tạo / Sửa / Chi tiết là TRANG riêng, không phải cửa sổ nổi. Số hiển thị dấu phẩy ngăn nghìn, dấu chấm thập phân.'),
]

SCREEN = ListScreen(menu=MENU, title='Danh sách biên bản xử lý hàng thừa, thiếu sau kiểm kê', total=13, quick_label='số phiếu',
                    quick_sample='00006', quick_hit='biên bản BBXLKKHH-00006',
                    filters=[('Trạng thái', 'Đã duyệt'), ('Kho', 'LN - Liên Ninh')], unit='biên bản')

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát tiêu đề bảng và tab trình duyệt.'], '—',
       ['Cả 2 nơi đều là "Danh sách biên bản xử lý hàng thừa, thiếu sau kiểm kê".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE_LIST, [MENU, 'Quan sát khối bộ lọc và thanh công cụ.'], '—',
       ['Khối bộ lọc: ô tìm nhanh (gợi ý "Tìm theo số phiếu"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
        'Thanh công cụ: Tạo mới, Xuất Excel, In danh sách, nút biểu tượng cột.',
        'Dòng Đã duyệt: cột Hành động có In, Xuất Excel, Lịch sử; không có Sửa, Duyệt, Xóa.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 11 cột theo thứ tự: STT, Số phiếu, Ngày tạo, Kho, Hàng thừa, Hàng thiếu, Người tạo, Người duyệt, Ngày duyệt, Trạng thái, '
        'Hành động.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 11/11 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp biên bản đã tạo', 'P0', [PRE_LIST, P6], [MENU, 'Tìm "BBXLKKHH-00006", đối chiếu dòng.'], '—',
       ['Ngày tạo "22/10/2026 14:58", Kho "Liên Ninh", Hàng thừa "2", Hàng thiếu "1", Người tạo "DNS Admin", Người duyệt "DNS Admin", '
        'Ngày duyệt "22/10/2026 15:00", Trạng thái "Đã duyệt".'], [6, 58])
S1.add('Số lượng bằng 0 hiện "0"', 'P1', [PRE_LIST, 'BBXLKKHH-00001 chỉ có hàng thiếu (2), không có hàng thừa.'],
       [MENU, 'Quan sát dòng BBXLKKHH-00001.'], '—', ['Cột Hàng thừa hiện "0" (không để trống), Hàng thiếu "2", căn phải.'], 6)
S1.add('Trạng thái bản ghi', 'P0', PRE_LIST, [MENU, ADV, 'Mở ô Trạng thái.', 'Quan sát cột Trạng thái.'], '—',
       ['Ô có 3 lựa chọn: Đang tạo, Chờ duyệt, Đã duyệt.', 'Nhãn: Đang tạo xám, Chờ duyệt cam, Đã duyệt xanh lá.'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', [ACC_B, 'B chưa tạo biên bản nào.'], ['Đăng nhập B.', MENU], '—',
       ['Bảng hiện "Không có dữ liệu phù hợp."; không báo lỗi; không có nút Tạo mới.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       ['Bảng hiện "Không có dữ liệu phù hợp.".'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 13 biên bản, tự về trang 1, "Hiển thị 1–13 / 13".', 'Chỉ nạp lại 1 lần.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–13 / 13".', 'Bước 3: "Hiển thị 1–10 / 13".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—', ['Bước 2: trang 2.', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang 2 quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.'], '—', ['Trang 2 đánh số 11–13.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', ADV, 'Chọn Trạng thái = Đã duyệt.'],
       'Trạng thái: Đã duyệt', ['Tự nạp lại ở trang 1; "Hiển thị 1–4 / 4".'], 17)
S1.add('Sắp xếp tăng dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Số phiếu.'], '—',
       ['Xếp theo số phiếu tăng dần (BBXLKKHH-00001 trên cùng), mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Số phiếu 2 lần.'], '—',
       ['Xếp theo số phiếu giảm dần, mũi tên xuống.'], 21)
S1.add('Sắp xếp theo Ngày tạo / Ngày duyệt; mặc định theo Ngày tạo', 'P1', PRE_LIST,
       [MENU, 'Quan sát thứ tự khi mới vào.', 'Bấm tiêu đề Ngày tạo (2 lần).', 'Bấm tiêu đề Ngày duyệt.'], '—',
       ['Mới vào: biên bản tạo mới nhất ở trên, không cột nào có mũi tên.',
        'Ngày tạo lần 1 cũ nhất trên, lần 2 mới nhất trên.', 'Ngày duyệt: biên bản chưa duyệt (trống) xếp cùng nhau.'], 22)
S1.add('Sắp xếp theo Kho, Hàng thừa, Hàng thiếu', 'P1', PRE_LIST, [MENU, 'Bấm lần lượt tiêu đề Kho, Hàng thừa, Hàng thiếu.'], '—',
       ['Kho xếp theo tên kho (Kho Sài Gòn trước Liên Ninh khi tăng).', 'Hàng thừa / Hàng thiếu xếp theo số.',
        'Cột không nhảy bề rộng khi sắp xếp.'], 20)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST, [MENU, 'Bấm tiêu đề Người tạo, Người duyệt, Trạng thái, Hành động.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Số phiếu (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự tăng của trang 1.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 2.', 'Bấm tiêu đề Ngày tạo.'], '—', ['Về trang 1.'], 25)
S1.add('Nút thao tác theo trạng thái', 'P0', [ACC_A, BB1, BB2, 'A có thêm quyền "%s".' % Q2],
       ['Đăng nhập A.', MENU, 'Quan sát cột Hành động 2 dòng BB1, BB2.'], '—',
       ['BB1 (Đang tạo): Sửa, In và nút ba chấm "Hành động khác" chứa Xuất Excel, Lịch sử.',
        'BB2 (Chờ duyệt): Duyệt, In và "Hành động khác" chứa Xuất Excel, Lịch sử; không có Sửa.'], [3, 34])
S1.add('Mở màn từ thông báo chờ duyệt', 'P1', [ACC_D, BB2, 'D đã nhận thông báo "[BBXLKKHH] Chờ duyệt: <số phiếu BB2>".'],
       ['Đăng nhập D.', 'Bấm chuông thông báo, bấm thông báo của BB2.'], '—',
       ['Mở màn chi tiết BB2, có nút Duyệt.'], 1)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo số phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "BBXLKKHH-00006", bấm Tìm kiếm.'], 'Ô tìm nhanh: BBXLKKHH-00006',
       ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần số phiếu', 'P0', PRE_LIST, [MENU, 'Nhập "0000", bấm Tìm kiếm.'], 'Ô tìm nhanh: 0000',
       ['Ra các biên bản có số phiếu chứa chuỗi nhập (BBXLKKHH-00001 … 00009).'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "bbxlkkhh-00006", bấm Tìm kiếm.'], '—',
       ['Ra BBXLKKHH-00006 như khi gõ chữ hoa.'], 28)
S2.add('Có dấu / không dấu', 'P2', PRE_LIST, [MENU, 'Nhập "BBXLKKHH-0000Ư", bấm Tìm kiếm.'], '—',
       ['"Không có dữ liệu phù hợp."; số phiếu không có chữ có dấu nên không có trường hợp khớp có dấu / không dấu.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; ký tự % được hiểu là ký tự đại diện nên ra toàn bộ.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  BBXLKKHH-00006  ", bấm Tìm kiếm.'], '—',
       ['Ra BBXLKKHH-00006 (bỏ khoảng trắng đầu / cuối).'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "BBXLKKHH-00006", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Sau bước 2 hiện lại đủ 13 biên bản.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST,
       [MENU, 'Nhập "00006", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'], '—',
       ['Cả 2 cách đều ra BBXLKKHH-00006, về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['Các ô Kho, Trạng thái, Người tạo, Người duyệt, Ngày tạo đều trống.', 'Đủ 13 biên bản.'], 36)
S2.add('Lọc Kho', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = LN - Liên Ninh.'], '—',
       ['Lọc ngay; còn BBXLKKHH-00003 … 00006 (kho Liên Ninh) và các biên bản thử cùng kho.',
        'Ô Kho liệt kê mọi kho vật lý, hiển thị "Mã - Tên".'], 37)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Chờ duyệt.', 'Đổi Trạng thái = Đang tạo.'], '—',
       ['Bước 3: BBXLKKHH-00002, 00004, nhãn cam.', 'Bước 4: 7 biên bản Đang tạo của DNS Admin, nhãn xám.'], 37)
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Mở ô Người tạo.', 'Chọn Người tạo = DNS Admin.'], '—',
       ['Ô chỉ liệt kê người đã tạo biên bản trong phạm vi xem, dạng "Họ tên - Mã phòng ban - Mã nhân viên".', 'Ra đủ 13 biên bản.'], 37)
S2.add('Lọc Người duyệt', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người duyệt = DNS Admin.'], '—',
       ['Còn 4 biên bản Đã duyệt; biên bản chưa duyệt không hiện.', 'Ô chỉ liệt kê người đã duyệt biên bản trong phạm vi.'], 37)
S2.add('Lọc Ngày tạo lấy trọn ngày biên', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày tạo 22/10/2026 – 22/10/2026.'], '—',
       ['Ra 6 biên bản BBXLKKHH-00001 … 00006 (tạo 09:56 – 14:58 ngày 22/10/2026).',
        'Lọc theo ngày tạo, KHÔNG theo Từ ngày – Đến ngày kiểm kê; bỏ trống ngày cuối vẫn lọc được từ ngày đầu.'], 37)
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = LN - Liên Ninh.', 'Chọn Trạng thái = Chờ duyệt.'],
       '—', ['Chỉ còn BBXLKKHH-00004.'], 38)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST, [MENU, 'Nhập "00001", bấm Tìm kiếm.', ADV, 'Chọn Kho = LN - Liên Ninh.'], '—',
       ['"Không có dữ liệu phù hợp." vì BBXLKKHH-00001 thuộc Kho Sài Gòn.'], [39, 40])
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đang tạo.', 'Đổi Số dòng/trang = 5, bấm trang 2.'],
       '—', ['"Hiển thị 1–5 / 7" rồi "Hiển thị 6–7 / 7"; STT liên tục.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Trạng thái = Đã duyệt.', ['Bấm tiêu đề Số phiếu.'], '—',
       ['Chỉ 4 biên bản đang lọc được sắp; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "BBXL", lọc Kho Liên Ninh, Trạng thái Đã duyệt, sắp Số phiếu, ở trang 2.',
       ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống, bỏ sắp xếp, nạp lại trang 1, đủ 13 biên bản.'], 44)
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Đã duyệt, chưa mở màn con.'], ['Nhấn F5.'], '—',
       ['Bộ lọc trở về trống, đủ 13 biên bản (chỉ nhớ khi đi vào màn con của màn này).'], 46)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Người duyệt, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô Người duyệt.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Kho = LN - Liên Ninh.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Kho, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị bỏ, nạp lại đủ 13 biên bản.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Người duyệt.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Người duyệt vẫn ẩn.', 'Bước 2: tích đủ 5 mục, Người duyệt hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Trạng thái lên đầu, bấm Lưu.'], '—',
       ['Ô Trạng thái đứng đầu khối Tìm kiếm nâng cao; cấu hình giữ sau khi đăng nhập lại.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo', 'P0', PRE_FORM, TAO, '—', ['Mở TRANG "Tạo biên bản xử lý hàng thừa, thiếu sau kiểm kê", tab cùng tiêu đề.'], 49)
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải ghi "<tên A> - <ngày giờ hiện tại>".', 'Không có ô Số phiếu (tự sinh khi lưu).'], 50)
S3.add('Các trường và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Từ ngày (gợi ý "Chọn từ ngày"), Đến ngày ("Chọn đến ngày"), Kho vật lý ("Chọn kho vật lý"), Ghi chú '
        '("Nhập ghi chú").', 'Khối File đính kèm có nút Thêm tài liệu; khối Phiếu kiểm kê; khối Chi tiết có nút Lấy dữ liệu, 2 tab '
        'Hàng thừa (0), Hàng thiếu (0).', 'Chân màn: Lưu, Lưu và gửi duyệt, Lưu và tiếp tục, Quay lại.'], [51, 54])
S3.add('Trường bắt buộc / không bắt buộc', 'P0', PRE_FORM, TAO + ['Quan sát dấu *.'], '—',
       ['Có dấu *: Từ ngày, Đến ngày, Kho vật lý, tiêu đề khối Chi tiết, cột Lý do, Giá xử lý, % Chi phí nhân viên, % Chi phí công ty, '
        'NV chịu.', 'Ghi chú, File đính kèm không bắt buộc.'], 52)
S3.add('Giá trị mặc định', 'P0', PRE_FORM, TAO, '—',
       ['Mọi ô trống; khối Phiếu kiểm kê ghi "Chọn Từ ngày, Đến ngày, Kho vật lý rồi bấm "Lấy dữ liệu"."',
        'Bảng chi tiết "Không có dữ liệu".'], 53)
S3.add('Lấy dữ liệu khi chưa chọn ngày, kho', 'P0', PRE_FORM, TAO + ['Bấm "Lấy dữ liệu" ngay.'], '—',
       ['Báo ' + MISS + '.', 'Dưới 3 ô CÙNG LÚC: "Từ ngày – Vui lòng chọn từ ngày.", "Đến ngày – Vui lòng chọn đến ngày.", '
        '"Kho vật lý – Vui lòng chọn kho vật lý.".'], [61, 70])
S3.add('Lấy dữ liệu thành công', 'P0', PRE_FORM, GET, ['Từ ngày: 22/10/2026', 'Đến ngày: 22/10/2026', 'Kho vật lý: LN - Liên Ninh'],
       ['Khối Phiếu kiểm kê có TPE.KKK-01068, TPE.KKK-01069, cả 2 đã tích, số phiếu là liên kết.',
        'Tab "Hàng thừa (2)": Bộ điều khiển từ xa (Phiếu xử lý PNHĐCKK-00041, Đơn giá vốn 35,000), Công tắc nguồn (PNHĐCKK-00042).',
        'Tab "Hàng thiếu (1)": Rơ le điện, Phiếu xử lý PXHĐCKK-00068.',
        'Mỗi dòng: Giá xử lý Giá vốn, % Chi phí nhân viên 100, % Chi phí công ty 0, Lý do và NV chịu trống.'], [53, 269, 283])
S3.add('Lấy dữ liệu không có kết quả', 'P1', PRE_FORM,
       TAO + ['Chọn Từ ngày 01/01/2020, Đến ngày 02/01/2020, Kho vật lý LN - Liên Ninh.', 'Bấm "Lấy dữ liệu".'], '—',
       ['Báo "Không có kết quả kiểm kê chênh lệch trong khoảng ngày của kho đã chọn.".', 'Hai tab (0), bảng "Không có dữ liệu".'], 268)
S3.add('Lịch Đến ngày chặn ngày trước Từ ngày', 'P1', PRE_FORM, TAO + ['Chọn Từ ngày 22/10/2026.', 'Mở lịch Đến ngày.'], '—',
       ['Các ngày trước 22/10/2026 bị mờ, không chọn được.'], 62)
S3.add('Tính % và chi phí trên dòng', 'P0', PRE_FORM, GET + ['Ở dòng Bộ điều khiển từ xa nhập % Chi phí nhân viên 40.'],
       '% Chi phí nhân viên: 40',
       ['% Chi phí công ty tự thành 60.', 'Chi phí nhân viên 14,000 (35,000 × 40%), Chi phí công ty 21,000.'], 62)
S3.add('Đổi Giá xử lý sang Giá bán', 'P1', PRE_FORM, GET + ['Ở dòng Bộ điều khiển từ xa chọn Giá xử lý = Giá bán.'], '—',
       ['Chi phí nhân viên = Thành tiền bán 999,999.99 × 100% = 999,999.99.'], 62)
S3.add('% vượt 100', 'P1', PRE_FORM, GET + ['Nhập % Chi phí nhân viên 120.'], '% Chi phí nhân viên: 120',
       ['Ô % Chi phí công ty về trống.', 'Dưới ô báo "% Chi phí – Từ 0 đến 100.".'], [62, 74])
S3.add('Ô % không nhận chữ', 'P2', PRE_FORM, GET + ['Gõ "abc" vào ô % Chi phí nhân viên.'], '—',
       ['Ô không nhận chữ; chỉ nhận số, tối đa 2 số lẻ.'], 63)
S3.add('Lưu với dữ liệu hợp lệ đầy đủ', 'P0', PRE_FORM, FILL + ['Nhập Ghi chú "Xử lý kiểm kê tháng 10".', 'Bấm "Lưu".'], FULL,
       [OK_SAVE, 'Số phiếu dạng "BBXLKKHH-<5 số>".', 'Hàng thừa 2, Hàng thiếu 1.'], [55, 79, 85])
S3.add('Lưu chỉ với trường bắt buộc', 'P0', PRE_FORM, FILL + ['Để trống Ghi chú, không thêm file.', 'Bấm "Lưu".'], FULL,
       [OK_SAVE, 'Chi tiết: Ghi chú trống, khối File đính kèm "Không có file đính kèm.".'], [56, 57])
S3.add('Dữ liệu sau lưu', 'P0', [PRE_FORM, 'A vừa Lưu biên bản ở TC_03.014.'], ['Bấm số phiếu vừa tạo.'], '—',
       ['Chi tiết: Từ ngày / Đến ngày 22/10/2026, Kho vật lý "LN - Liên Ninh", Ghi chú "Xử lý kiểm kê tháng 10".', '2 phiếu kiểm kê '
        'đã tích, 3 dòng với Lý do, Giá vốn, 100 %, 0 %, NV chịu "10610026-Bùi Duy Trước".'], 58)
S3.add('Trạng thái mặc định sau Lưu', 'P0', [PRE_FORM, 'A vừa Lưu biên bản.'], [MENU, 'Đăng nhập DNS Admin, mở danh sách.'], '—',
       ['A thấy biên bản Đang tạo (nhãn xám).', 'DNS Admin KHÔNG thấy biên bản này (Đang tạo chỉ người tạo thấy).'], [59, 84])
S3.add('Lịch sử tạo', 'P1', [PRE_FORM, 'A vừa Lưu biên bản.'], ['Ở dòng biên bản bấm ba chấm > Lịch sử.'], '—',
       ['Có 1 mốc "Tạo mới", Người thực hiện A, thời điểm lưu.'], [60, 176])
S3.add('Lưu khi thiếu Lý do, NV chịu', 'P0', PRE_FORM, GET + ['Bấm "Lưu".'], '—',
       ['Báo ' + MISS + ', không lưu.', 'Mỗi dòng báo đỏ "Lý do – Vui lòng nhập lý do." và "NV chịu – Vui lòng chọn nhân viên chịu.".',
        'Tab có lỗi được đánh dấu; cuộn tới ô lỗi đầu tiên.'], [61, 70, 80])
S3.add('Lưu khi chưa Lấy dữ liệu', 'P0', PRE_FORM,
       TAO + ['Chọn Từ ngày, Đến ngày 22/10/2026, Kho vật lý LN - Liên Ninh.', 'Bấm "Lưu".'], '—',
       ['Báo đỏ ở khối Chi tiết "Chi tiết – Chưa có hàng thừa, thiếu. Vui lòng bấm "Lấy dữ liệu".", không lưu.'], [61, 80])
S3.add('Đổi kho sau khi Lấy dữ liệu', 'P0', PRE_FORM, FILL + ['Đổi Kho vật lý sang SG - Kho Sài Gòn.', 'Bấm "Lưu".'], '—',
       ['Báo "Chi tiết – Từ ngày / Đến ngày / Kho vật lý đã đổi. Vui lòng bấm "Lấy dữ liệu" lại.", không lưu.'], [62, 81])
S3.add('Đến ngày trước Từ ngày', 'P1', PRE_FORM, TAO + ['Chọn Đến ngày 20/10/2026.', 'Chọn Từ ngày 22/10/2026.', 'Bấm "Lấy dữ liệu".'],
       '—', ['Dưới Đến ngày báo "Đến ngày – Phải lớn hơn hoặc bằng Từ ngày.", không lấy dữ liệu.'], [62, 81])
S3.add('Bỏ tích phiếu kiểm kê', 'P0', PRE_FORM, FILL + ['Bỏ tích TPE.KKK-01069.', 'Bấm "Lưu".'], '—',
       ['Sau khi bỏ tích: tab "Hàng thừa (1)", "Hàng thiếu (0)".', 'Lưu thành công; chi tiết chỉ có dòng của TPE.KKK-01068, ô '
        'TPE.KKK-01069 không tích.'], [57, 283])
S3.add('Bỏ tích hết phiếu kiểm kê', 'P1', PRE_FORM, FILL + ['Bỏ tích cả 2 phiếu.', 'Bấm "Lưu".'], '—',
       ['Báo "Chi tiết – Chưa có hàng thừa, thiếu. Vui lòng bấm "Lấy dữ liệu".", không lưu.'], 80)
S3.add('Lý do đúng 255 ký tự', 'P1', PRE_FORM, GET + ['Dán 255 ký tự vào Lý do cả 3 dòng, nhập đủ ô khác.', 'Bấm "Lưu".'],
       'Lý do: 255 ký tự', ['Lưu thành công, Lý do đủ 255 ký tự.'], [64, 65])
S3.add('Lý do, Ghi chú vượt 255 ký tự', 'P1', PRE_FORM, GET + ['Dán 300 ký tự vào Lý do và Ghi chú.'], 'Chuỗi 300 ký tự',
       ['Ô chỉ nhận 255 ký tự đầu (không gõ thêm được).'], 66)
S3.add('Lý do có ký tự đặc biệt, tiếng Việt', 'P2', PRE_FORM, FILL[:-1] + ['Nhập Lý do "Hỏng <vỏ> & \'mất\' 50%", nhập đủ ô khác.', 'Bấm "Lưu".'],
       '—', ['Lưu thành công, Lý do hiển thị đúng ký tự đã nhập.'], 63)
S3.add('Lý do chỉ có khoảng trắng', 'P1', PRE_FORM, GET + ['Nhập Lý do "   " cả 3 dòng, nhập đủ ô khác.', 'Bấm "Lưu".'], '—',
       ['Báo "Lý do – Vui lòng nhập lý do." ở từng dòng, không lưu.'], 69)
S3.add('Khoảng trắng đầu / cuối Lý do', 'P2', PRE_FORM, GET + ['Nhập Lý do "  Thiếu hàng  ", nhập đủ ô khác, bấm "Lưu".', 'Mở chi tiết.'],
       '—', ['Lý do lưu là "Thiếu hàng" (bỏ khoảng trắng đầu / cuối).'], 68)
S3.add('Lỗi biến mất sau khi sửa', 'P1', 'Đang ở màn Tạo, các dòng báo lỗi Lý do / NV chịu.', ['Nhập Lý do dòng 1.', 'Chọn NV chịu dòng 1.'],
       '—', ['Lỗi của từng ô mất ngay khi nhập / chọn.', 'Hết lỗi ở tab thì dấu lỗi trên tab mất.'], 71)
S3.add('Biên bản trùng nội dung', 'P1', [PRE_FORM, 'A đã lưu 1 biên bản từ dữ liệu kho Liên Ninh 22/10/2026.'],
       FILL + ['Bấm "Lưu".'], FULL,
       ['Lưu thành công, số phiếu khác biên bản trước.', 'Lưu ý: hệ thống KHÔNG chặn lập 2 biên bản cho cùng phiếu kiểm kê.'],
       [67, 75, 82, 89])
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, FILL + ['Bấm "Lưu và tiếp tục".'], FULL,
       ['Báo "Lưu thành công.", ở lại màn Tạo.', 'Form trắng: ngày, kho, ghi chú, phiếu kiểm kê, 2 tab về rỗng.',
        'Biên bản vừa lưu ở trạng thái Đang tạo.'], [72, 76, 77, 83])
S3.add('Lưu và tiếp tục khi thiếu dữ liệu', 'P1', PRE_FORM, GET + ['Bấm "Lưu và tiếp tục".'], '—',
       ['Báo ' + MISS + ', không lưu, form giữ nguyên dữ liệu.'], [73, 74])
S3.add('Rời màn sau Lưu và tiếp tục', 'P2', 'Vừa Lưu và tiếp tục, form trắng chưa nhập gì.', ['Bấm "Quay lại".'], '—',
       ['Về danh sách ngay, không hỏi; biên bản đã lưu có trong danh sách.'], 78)
S3.add('Quay lại khi chưa nhập', 'P1', PRE_FORM, TAO + ['Bấm "Quay lại".'], '—', ['Về danh sách ngay, không hỏi.'], 93)
S3.add('Quay lại khi đã nhập', 'P0', PRE_FORM, GET + ['Bấm "Quay lại".'], '—',
       ['Hiện hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?", nút Thoát, Ở lại.'], 94)
S3.add('Đóng hộp chưa lưu bằng (x)', 'P2', 'Đang mở hộp "Thông tin chưa lưu".', ['Bấm (x) của hộp.'], '—',
       ['Hộp đóng, ở lại màn Tạo, dữ liệu giữ nguyên.', 'Màn Tạo là trang, không có nút X riêng.'], 95)
S3.add('Chọn Thoát', 'P1', 'Đang mở hộp "Thông tin chưa lưu".', ['Bấm "Thoát".'], '—', ['Về danh sách, không có biên bản mới.'], 96)
S3.add('Chọn Ở lại', 'P1', 'Đang mở hộp "Thông tin chưa lưu".', ['Bấm "Ở lại".'], '—', ['Ở lại màn Tạo, dữ liệu đã nhập giữ nguyên.'], 97)
S3.add('Nhập rồi xóa hết', 'P2', PRE_FORM, TAO + ['Nhập Ghi chú "abc" rồi xóa hết.', 'Bấm "Quay lại".'], '—',
       ['Về danh sách ngay, không hỏi.'], [98, 99])
S3.add('Không thao tác lâu', 'P2', PRE_FORM, GET + ['Để màn 30 phút không thao tác.', 'Bấm "Lưu" (đủ dữ liệu).'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên, chuyển màn đăng nhập.'], 100)
S3.add('Bấm Lưu liên tục', 'P1', PRE_FORM, FILL + ['Bấm "Lưu" 3 lần thật nhanh.'], '—',
       ['Chỉ tạo 1 biên bản (nút khóa trong lúc lưu).'], 101)
S3.add('Tạo đồng thời 2 tab', 'P2', PRE_FORM, ['Mở màn Tạo ở 2 tab, nhập cùng dữ liệu.', 'Bấm "Lưu" ở cả 2 tab.'], '—',
       ['Cả 2 lưu được, 2 số phiếu khác nhau (không có trường duy nhất).'], 102)
S3.add('Dữ liệu kiểm kê đổi giữa chừng', 'P1', [PRE_FORM, 'Sau khi A Lấy dữ liệu, có thêm 1 phiếu kiểm kê Hoàn thành cùng kho, ngày.'],
       ['Bấm "Lưu".'], '—', ['Báo ' + CHANGED + ' ở khối Chi tiết, không lưu.', 'Bấm Lấy dữ liệu lại thì lưu được.'], [62, 81])
S3.add('Thêm file đính kèm sai loại', 'P2', PRE_FORM, TAO + ['Bấm "Thêm tài liệu", chọn file .docx.'], 'File: bien_ban.docx',
       ['Báo "Chỉ nhận file pdf, png, jpg, jpeg".'], 62)
S3.add('Thêm file .pdf hợp lệ', 'P1', PRE_FORM, TAO + ['Bấm "Thêm tài liệu", chọn file .pdf 2MB.'], 'File: bien_ban.pdf',
       ['File hiện trong bảng (tên, dung lượng); lưu biên bản thì file gắn vào biên bản.'], 57)
S3.add('Lấy dữ liệu lại giữ ô đã nhập', 'P1', PRE_FORM, FILL + ['Bấm "Lấy dữ liệu" lần nữa.'], '—',
       ['3 dòng giữ nguyên Lý do, %, NV chịu đã nhập; tích phiếu giữ như trước.'], 71)

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
S4.add('Mở màn Sửa', 'P0', [ACC_A, BB1], ['Đăng nhập A.', MENU, 'Ở dòng BB1 bấm Sửa (bút chì).'], '—',
       ['Mở TRANG "Sửa biên bản xử lý hàng thừa, thiếu: <số phiếu BB1>".'], 103)
S4.add('Dữ liệu điền đúng', 'P0', [ACC_A, BB1], ['Mở màn Sửa BB1.'], '—',
       ['Từ ngày, Đến ngày, Kho vật lý, Ghi chú, phiếu kiểm kê (tích như đã lưu), 3 dòng với Lý do, Giá xử lý, %, NV chịu đúng như '
        'lúc lưu.'], 104)
S4.add('Trường được / không được sửa', 'P0', [ACC_A, BB1], ['Mở màn Sửa BB1.'], '—',
       ['Sửa được: Từ ngày, Đến ngày, Kho vật lý, Ghi chú, file, tích phiếu, ô từng dòng.',
        'Không có ô Số phiếu; người tạo, ngày tạo không đổi.'], 105)
S4.add('Các nút ở màn Sửa', 'P1', [ACC_A, BB1], ['Mở màn Sửa BB1.'], '—',
       ['Chân màn: Lưu, Lưu và gửi duyệt, Quay lại; KHÔNG có Lưu và tiếp tục.'], 106)
S4.add('Sửa một trường', 'P0', [ACC_A, BB1], ['Mở màn Sửa BB1.', 'Sửa Ghi chú thành "Đã đối chiếu".', 'Bấm "Lưu".'],
       'Ghi chú: Đã đối chiếu', ['Báo "Lưu thành công.", về danh sách; BB1 vẫn Đang tạo.'], 107)
S4.add('Sửa nhiều trường', 'P0', [ACC_A, BB1],
       ['Mở màn Sửa BB1.', 'Dòng 1 đổi Giá xử lý = Giá bán, % nhân viên 50, NV chịu khác.', 'Bấm "Lưu".'], '—',
       ['Lưu thành công; chi tiết hiện đúng giá trị mới; chi phí tính lại.'], [108, 110])
S4.add('Giữ nguyên giá trị không sửa', 'P1', [ACC_A, BB1], ['Mở màn Sửa BB1, không đổi gì.', 'Bấm "Lưu".'], '—',
       ['Lưu thành công, dữ liệu không đổi.', 'Không sinh mốc "Thay đổi thông tin" mới.'], [109, 125, 182])
S4.add('Người cập nhật sau sửa', 'P2', [ACC_A, BB1], ['Sửa và Lưu BB1.', 'Mở Lịch sử BB1.'], '—',
       ['Mốc "Thay đổi thông tin" ghi Người thực hiện A, thời điểm lưu.'], 111)
S4.add('Lịch sử sửa ghi giá trị cũ / mới', 'P0', [ACC_A, BB1], ['Sửa Ghi chú và Lý do dòng 1 rồi Lưu.', 'Mở Lịch sử BB1.'], '—',
       ['Mốc "Thay đổi thông tin": Ghi chú cũ > mới, dòng chi tiết Lý do cũ > mới.'], [112, 177, 178, 183])
S4.add('Bỏ trống bắt buộc khi sửa', 'P0', [ACC_A, BB1], ['Mở màn Sửa BB1.', 'Xóa Lý do dòng 1, bấm (x) bỏ NV chịu dòng 2.', 'Bấm "Lưu".'],
       '—', ['Báo ' + MISS + '; lỗi tại đúng ô, không lưu.'], [113, 117])
S4.add('Sai định dạng / vượt giới hạn khi sửa', 'P1', [ACC_A, BB1], ['Nhập % nhân viên 150 ở dòng 1.', 'Dán 300 ký tự vào Ghi chú.'],
       '—', ['% báo "% Chi phí – Từ 0 đến 100.".', 'Ghi chú chỉ nhận 255 ký tự.'], [114, 115])
S4.add('Không kiểm trùng khi sửa', 'P2', [ACC_A, BB1, 'Có biên bản khác cùng kho, cùng ngày.'], ['Sửa BB1 rồi Lưu.'], '—',
       ['Lưu được; biên bản không có trường duy nhất nên không báo trùng (kể cả với chính nó).'], 116)
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P1', 'Màn Sửa đang báo lỗi Lý do dòng 1.', ['Nhập Lý do dòng 1.'], '—', ['Lỗi mất ngay.'], 118)
S4.add('Mở Sửa rồi quay lại không đổi', 'P1', [ACC_A, BB1], ['Mở màn Sửa BB1.', 'Bấm "Quay lại".'], '—',
       ['Về danh sách ngay, không hỏi.'], 119)
S4.add('Đổi rồi trả về giá trị ban đầu', 'P2', [ACC_A, BB1], ['Đổi Ghi chú rồi gõ lại đúng như cũ.', 'Bấm "Quay lại".'], '—',
       ['Về danh sách ngay, không hỏi.'], 120)
S4.add('Quay lại khi đã đổi', 'P0', [ACC_A, BB1], ['Đổi Ghi chú.', 'Bấm "Quay lại".'], '—', ['Hiện hộp "Thông tin chưa lưu".'], 121)
S4.add('Xác nhận Thoát / Ở lại', 'P1', 'Đang mở hộp "Thông tin chưa lưu" ở màn Sửa BB1.', ['Bấm "Ở lại".', 'Bấm "Quay lại", chọn "Thoát".'],
       '—', ['Ở lại: giữ form.', 'Thoát: về danh sách, BB1 không đổi.'], [122, 123, 124])
S4.add('Sửa biên bản đã gửi duyệt ở tab khác', 'P0', [ACC_A, BB1, 'A mở màn Sửa BB1 ở tab 1, tab 2 bấm Lưu và gửi duyệt BB1.'],
       ['Ở tab 1 bấm "Lưu".'], '—', ['Báo ' + CONFLICT + ', không lưu.'], [128, 126])
S4.add('Mở Sửa biên bản không còn Đang tạo', 'P1', [ACC_A, BB2], ['Mở thẳng màn Sửa của BB2 (đường link cũ đã lưu).'], '—',
       ['Tự chuyển về màn chi tiết BB2, không có nút Sửa.'], [126, 129])
S4.add('Người khác không sửa được', 'P0', [ACC_C, BB1, 'C cùng công ty TPE, không phải người tạo.'], ['Đăng nhập C.', MENU], '—',
       ['C không thấy BB1 (Đang tạo chỉ người tạo thấy).', 'Mở link màn Sửa BB1 > ' + NOTFOUND + '.'], [126, 290])
S4.add('Xóa file đã lưu', 'P1', [ACC_A, BB1, 'BB1 có 1 file .pdf.'], ['Mở màn Sửa BB1.', 'Bấm biểu tượng xóa của file.'], '—',
       ['Báo "Xóa file thành công"; file mất khỏi biên bản; lịch sử có mốc "Thay đổi thông tin" phần File.'], 112)

# ============================================================== V. GỬI DUYỆT
S5 = Sec(5)
S5.add('Lưu và gửi duyệt khi tạo', 'P0', [PRE_FORM, 'Tài khoản D có quyền "%s" cùng công ty TPE.' % Q2],
       FILL + ['Bấm "Lưu và gửi duyệt".'], FULL,
       ['Báo "Lưu và gửi duyệt thành công.", về danh sách.', 'Biên bản mới trạng thái Chờ duyệt (nhãn cam); A không còn nút Sửa.',
        'Không có hộp xác nhận.'], [86, 90, 91, 92])
S5.add('Thiếu dữ liệu khi gửi duyệt', 'P0', PRE_FORM, GET + ['Bấm "Lưu và gửi duyệt".'], '—',
       ['Báo ' + MISS + '; lỗi Lý do, NV chịu tại từng dòng; không lưu, không gửi thông báo.'], [87, 88])
S5.add('Gửi duyệt từ màn Sửa', 'P0', [ACC_A, BB1], ['Mở màn Sửa BB1.', 'Bấm "Lưu và gửi duyệt".'], '—',
       ['BB1 chuyển Chờ duyệt.', 'Lịch sử có mốc "Thay đổi trạng thái": Đang tạo > Chờ duyệt.'], [86, 92])
S5.add('Thông báo đến người có quyền Duyệt', 'P0', [ACC_D, 'A (công ty TPE) vừa Lưu và gửi duyệt biên bản BB3.'],
       ['Đăng nhập D.', 'Bấm chuông thông báo.'], '—',
       ['Có thông báo "[BBXLKKHH] Chờ duyệt: <số phiếu BB3>", ghi chú có Người lập, Kỳ, Kho, Thừa: 2, thiếu: 1.',
        'Nhân viên có quyền Duyệt ở công ty khác KHÔNG nhận.'], 308)
S5.add('Mở biên bản từ thông báo', 'P1', 'D đang có thông báo chờ duyệt BB3.', ['Bấm vào thông báo.'], '—',
       ['Mở màn chi tiết BB3 có nút Duyệt.'], 309)
S5.add('Biên bản trùng khi gửi duyệt', 'P2', [PRE_FORM, 'Đã có biên bản Chờ duyệt từ cùng dữ liệu.'], FILL + ['Bấm "Lưu và gửi duyệt".'],
       '—', ['Vẫn lưu được (không chặn trùng); lưu ý người lập tự kiểm tra tránh hạch toán trùng.'], 89)
S5.add('Không còn sửa được sau khi gửi', 'P1', [ACC_A, BB2], ['Mở chi tiết BB2.'], '—',
       ['Không có nút Sửa; ô Lý do / % / NV chịu chỉ đọc với A (không có quyền Duyệt).'], 281)

# ============================================================== VI. DUYỆT PHIẾU
S6 = Sec(6)
S6.add('Điều kiện hiển thị nút Duyệt', 'P0', [ACC_D, BB2, 'Biên bản BBXLKKHH-00006 Đã duyệt.'], ['Đăng nhập D.', MENU], '—',
       ['Dòng BB2 có nút Duyệt; dòng BBXLKKHH-00006 không có.', 'Bấm Duyệt ở dòng > mở màn chi tiết BB2, nút Duyệt ở chân màn.'], 300)
S6.add('Không có hộp xác nhận duyệt', 'P1', [ACC_D, BB2], ['Mở chi tiết BB2.', 'Bấm "Duyệt".'], '—',
       ['Hệ thống duyệt ngay, không hiện hộp xác nhận (giữ như hệ thống cũ).'], 301)
S6.add('Duyệt thành công', 'P0', [ACC_D, BB2], ['Mở chi tiết BB2.', 'Bấm "Duyệt".'], '—',
       ['Báo "Duyệt thành công.", về danh sách.', 'BB2 trạng thái Đã duyệt, Người duyệt D, Ngày duyệt = thời điểm duyệt.'], [302, 305])
S6.add('Người duyệt sửa ô trước khi duyệt', 'P0', [ACC_D, BB2],
       ['Mở chi tiết BB2.', 'Dòng 1 đổi % nhân viên 40, NV chịu "Chu Thị Kiều Trinh".', 'Bấm "Duyệt".'], '—',
       ['Duyệt thành công; chi tiết hiện 40 % / 60 %, NV chịu mới.', 'Ô Lý do không sửa được.'], [302, 306])
S6.add('Thiếu dữ liệu khi duyệt', 'P0', [ACC_D, BB2], ['Mở chi tiết BB2.', 'Bấm (x) bỏ Giá xử lý và NV chịu dòng 1.', 'Bấm "Duyệt".'],
       '—', ['Báo ' + MISS + '; dưới ô "Giá xử lý – Vui lòng chọn giá xử lý.", "NV chịu – Vui lòng chọn nhân viên chịu."; không duyệt.'],
       303)
S6.add('Điều kiện % khi duyệt', 'P1', [ACC_D, BB2], ['Nhập % nhân viên 120 ở dòng 1.', 'Bấm "Duyệt".'], '—',
       ['Báo lỗi % từ 0 đến 100, không duyệt.'], 304)
S6.add('Bút toán sau khi duyệt', 'P0', [ACC_D, BB2, 'BB2: 2 dòng thừa thành tiền vốn 35,000 và 100,000 (100% nhân viên), 1 dòng thiếu '
                                                    '1,608,915.50 (40%), cùng NV chịu Bùi Duy Trước.'],
       ['Duyệt BB2.', 'Mở Sổ chi tiết công nợ nhân viên, tài khoản 3341, nhân viên Bùi Duy Trước.'], '—',
       ['Có các dòng chứng từ <số phiếu BB2>: hàng thừa Nợ 3381 / Có 3341 135,000; hàng thiếu Nợ 3341 / Có 1381 643,566.2.',
        'Chi phí công ty ghi bằng chi phí nhân viên (Nợ 3381 / Có 711, Nợ 811 / Có 1381) — giữ như hệ thống cũ.'], [306, 307])
S6.add('Hủy thao tác duyệt', 'P1', [ACC_D, BB2], ['Mở chi tiết BB2, sửa % dòng 1.', 'Bấm "Quay lại", chọn "Thoát".'], '—',
       ['BB2 vẫn Chờ duyệt, dữ liệu không đổi.'], 310)
S6.add('Không duyệt lại biên bản đã duyệt', 'P0', [ACC_D, BB2, 'D mở chi tiết BB2 ở 2 tab.'], ['Tab 1 bấm "Duyệt".', 'Tab 2 bấm "Duyệt".'],
       '—', ['Tab 2 báo ' + CONFLICT + ', không ghi bút toán lần 2.'], 311)
S6.add('Lịch sử duyệt', 'P0', [ACC_D, 'D vừa duyệt BB2.'], ['Mở Lịch sử BB2.'], '—',
       ['Có mốc "Duyệt": "Trạng thái: Chờ duyệt > Đã duyệt", Người thực hiện D, thời điểm duyệt.'], 312)
S6.add('Duyệt không gửi thông báo', 'P2', [ACC_A, 'D vừa duyệt BB2 của A.'], ['A mở chuông thông báo.'], '—',
       ['Không có thông báo mới về việc duyệt BB2.'], 308)

# ============================================================== VII. LỊCH SỬ THAY ĐỔI
S7 = Sec(7)
S7.add('Mở lịch sử từ danh sách', 'P0', [PRE_LIST, P6], [MENU, 'Ở dòng BBXLKKHH-00006 bấm Lịch sử.'], '—',
       ['Mở cửa sổ "Lịch sử thay đổi: BBXLKKHH-00006".'], 162)
S7.add('Nội dung các mốc', 'P0', [PRE_LIST, P6], ['Mở Lịch sử BBXLKKHH-00006.'], '—',
       ['3 mốc mới nhất trên: 22/10/2026 15:00 Duyệt (Chờ duyệt > Đã duyệt); 22/10/2026 14:58 Thay đổi trạng thái (Đang tạo > Chờ '
        'duyệt); 22/10/2026 14:58 Tạo mới.', 'Mỗi mốc ghi "Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ".'],
       [163, 164, 165, 166, 167, 168])
S7.add('Lọc theo loại hành động', 'P1', 'Đang mở Lịch sử BBXLKKHH-00006.', ['Bấm Bộ lọc.', 'Chọn Loại hành động = Tạo mới.'], '—',
       ['Chỉ còn mốc Tạo mới.'], 169)
S7.add('Lọc theo người thực hiện', 'P1', 'Đang mở Lịch sử BBXLKKHH-00006.', ['Bấm Bộ lọc.', 'Chọn Người thực hiện = DNS Admin.'], '—',
       ['Hiện đủ 3 mốc.'], 170)
S7.add('Lọc theo thời gian', 'P1', 'Đang mở Lịch sử BBXLKKHH-00006.', ['Chọn Từ ngày 23/10/2026.'], '—',
       ['"Không có lịch sử phù hợp bộ lọc.".'], [171, 173])
S7.add('Kết hợp lọc', 'P2', 'Đang mở Lịch sử BBXLKKHH-00006.', ['Chọn Loại hành động = Thay đổi trạng thái, Từ ngày 22/10/2026.'], '—',
       ['Chỉ còn mốc Thay đổi trạng thái.'], 172)
S7.add('Đóng / mở Bộ lọc', 'P2', 'Đang mở Lịch sử.', ['Bấm Bộ lọc 2 lần.'], '—', ['Khối ô lọc mở rồi thu gọn.'], [174, 175])
S7.add('Lịch sử ở màn chi tiết và Làm mới', 'P1', [PRE_LIST, P6], ['Mở chi tiết BBXLKKHH-00006.', 'Ở khối Lịch sử bấm Xem lịch sử.',
                                                                    'Bấm Làm mới.'], '—',
       ['Hiện 3 mốc như cửa sổ ở danh sách; Làm mới nạp lại mốc mới nhất.'], [174, 195])
S7.add('Chưa có lịch sử', 'P2', [PRE_LIST, 'BBXLKKHH-00002 chưa có mốc nào (dữ liệu cũ).'], ['Mở Lịch sử BBXLKKHH-00002.'], '—',
       ['"Chưa có lịch sử thao tác nào.".'], 173)
S7.add('Đóng cửa sổ lịch sử', 'P1', 'Đang ở trang 2 danh sách, lọc Trạng thái Đã duyệt, mở Lịch sử 1 dòng.', ['Bấm "Đóng".'], '—',
       ['Cửa sổ đóng; danh sách giữ trang 2 và bộ lọc.'], [184, 185])

# ============================================================== VIII. XEM CHI TIẾT
S8 = Sec(8)
S8.add('Mở chi tiết', 'P0', [PRE_LIST, P6], [MENU, 'Bấm số phiếu BBXLKKHH-00006.'], '—',
       ['Mở TRANG chi tiết (không phải cửa sổ nổi).'], [186, 288])
S8.add('Tiêu đề', 'P1', [PRE_LIST, P6], ['Mở chi tiết BBXLKKHH-00006.'], '—',
       ['Tiêu đề "Chi tiết biên bản xử lý hàng thừa, thiếu: BBXLKKHH-00006", không gắn nhãn trạng thái.'], 187)
S8.add('Đầy đủ trường và khớp dữ liệu', 'P0', [PRE_LIST, P6], ['Mở chi tiết BBXLKKHH-00006.'], '—',
       ['Từ ngày 22/10/2026, Đến ngày 22/10/2026, Kho vật lý "LN - Liên Ninh", 1 file ảnh, phiếu kiểm kê TPE.KKK-01068, 01069 đã tích.',
        'Tab "Hàng thừa (2)": dòng 1 Lý do "th", Giá vốn, 40 % / 60 %, NV chịu "10610026-Bùi Duy Trước", Chi phí nhân viên 14,000.',
        'Tab "Hàng thiếu (1)": Rơ le điện.'], [188, 189])
S8.add('Khớp với danh sách', 'P1', [PRE_LIST, P6], ['So dòng BBXLKKHH-00006 ở danh sách với chi tiết.'], '—',
       ['Hàng thừa 2 = tổng SL tab Hàng thừa; Hàng thiếu 1 = tổng SL tab Hàng thiếu; Kho khớp.'], 190)
S8.add('Trường chỉ đọc, không có nút Lưu', 'P0', [PRE_LIST, P6], ['Mở chi tiết BBXLKKHH-00006.'], '—',
       ['Mọi ô khóa, ô tích phiếu kiểm kê khóa.', 'Chân màn chỉ có In, Xuất Excel, Quay lại; không có Lưu.'], [191, 192, 193])
S8.add('Chi tiết theo trạng thái', 'P1', [ACC_A, BB1, BB2], ['Mở chi tiết BB1.', 'Mở chi tiết BB2.'], '—',
       ['BB1 (Đang tạo): có nút Sửa.', 'BB2 (Chờ duyệt, A không có quyền Duyệt): không có Sửa, Duyệt.'], 194)
S8.add('Mở phiếu xử lý và phiếu kiểm kê', 'P2', [PRE_LIST, P6], ['Bấm PNHĐCKK-00041.', 'Bấm TPE.KKK-01068.'], '—',
       ['Mỗi liên kết mở phiếu tương ứng ở tab mới; màn chi tiết giữ nguyên.'], 188)
S8.add('Quay lại giữ trang và bộ lọc', 'P0', 'Đang ở trang 2 danh sách, lọc Trạng thái Đã duyệt.', ['Bấm số phiếu một dòng.', 'Bấm "Quay lại".'],
       '—', ['Về danh sách trang đang xem với bộ lọc Trạng thái Đã duyệt (trong 10 phút).'], [196, 197])
S8.add('Chi tiết ngoài phạm vi', 'P0', [ACC_B, 'B có đường link chi tiết BBXLKKHH-00006 (không phải của B).'], ['Đăng nhập B.', 'Mở link.'],
       '—', ['Chuyển sang ' + NOTFOUND + ', không lộ dữ liệu.'], [296, 288])

# ============================================================== IX. IN PHIẾU
S9 = Sec(9)
S9.add('In biên bản', 'P0', [PRE_LIST, P6], [MENU, 'Ở dòng BBXLKKHH-00006 bấm In.'], '—',
       ['Mở cửa sổ "Xem trước biên bản xử lý hàng thừa, thiếu BBXLKKHH-00006", khổ ngang.',
        'Nội dung: letterhead công ty của biên bản, "BIÊN BẢN XỬ LÝ HÀNG THỪA THIẾU SAU KIỂM KÊ", Số phiếu, Ngày lập 22/10/2026, Từ ngày, '
        'Đến ngày, Kho vật lý Liên Ninh, Phiếu kiểm kê "TPE.KKK-01068; TPE.KKK-01069", Ghi chú.',
        '2 bảng "Tab1 - Hàng Thừa", "Tab2 - Hàng Thiếu" có nhóm cột Chi tiết.'], 3)
S9.add('Bản in ghi chi phí công ty đã lưu', 'P1', [PRE_LIST, P6], ['In BBXLKKHH-00006.'], '—',
       ['Dòng 1 tab Hàng thừa: Chi phí nhân viên 14,000, Chi phí công ty 14,000 (màn chi tiết hiện 21,000 theo %).',
        'Lưu ý: giữ như hệ thống cũ.'], 6)
S9.add('In từ màn chi tiết và bấm In', 'P1', [PRE_LIST, P6], ['Mở chi tiết BBXLKKHH-00006, bấm In.', 'Bấm In trong cửa sổ.'], '—',
       ['Mở cùng cửa sổ xem trước; bấm In mở hộp thoại in của trình duyệt.'], 3)
S9.add('In danh sách', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày tạo 22/10/2026 – 22/10/2026.', 'Bấm "In danh sách".'], '—',
       ['Cửa sổ "Xem trước danh sách biên bản xử lý hàng thừa, thiếu sau kiểm kê": 6 dòng, 10 cột STT, Số phiếu, Ngày tạo, Kho vật '
        'lý, SL hàng thừa, SL hàng thiếu, Người tạo, Người duyệt, Ngày duyệt, Trạng thái.'], 3)
S9.add('In danh sách vượt 2.000 dòng', 'P2', 'Danh sách theo bộ lọc có 2.500 biên bản.', ['Bấm "In danh sách".'], '—',
       ['Hiện "Danh sách có 2,500 dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. …", không có nút In.'], 3)
S9.add('Đóng cửa sổ xem trước', 'P2', 'Đang mở cửa sổ xem trước.', ['Bấm (x).'], '—', ['Đóng, không in; màn giữ nguyên.'], 3)

# ============================================================== X. TÙY CHỈNH CỘT
S10 = Sec(10)
S10.add('Mở cửa sổ Tùy chỉnh cột', 'P0', PRE_LIST, [MENU, 'Bấm nút biểu tượng cột.'], '—',
        ['Mở "Tuỳ chỉnh cột" liệt kê 11 cột, "Đang chọn 11/11 cột".'], [198, 199, 200])
S10.add('Ẩn cột', 'P0', PRE_LIST, ['Bỏ tích Người duyệt, Ngày duyệt.', 'Bấm Lưu.'], '—',
        ['Báo "Cập nhật thành công"; bảng không còn 2 cột.'], [202, 206])
S10.add('Hiện lại cột đã ẩn', 'P1', 'Đã ẩn Người duyệt.', ['Mở Tùy chỉnh cột, tích Người duyệt, bấm Lưu.'], '—',
        ['Cột Người duyệt hiện lại đúng vị trí.'], 201)
S10.add('Cột khóa', 'P0', PRE_LIST, ['Mở Tùy chỉnh cột.'], '—',
        ['STT, Số phiếu, Hành động có ổ khóa, không bỏ tích, không kéo được.'], [203, 205])
S10.add('Kéo thả thứ tự', 'P1', PRE_LIST, ['Kéo Trạng thái lên sau Số phiếu, bấm Lưu.'], '—',
        ['Bảng hiện cột Trạng thái ngay sau Số phiếu.'], 204)
S10.add('Đóng không lưu', 'P1', PRE_LIST, ['Bỏ tích Kho, bấm Đóng.'], '—', ['Bảng vẫn có cột Kho.'], 207)
S10.add('Ghi nhớ sau F5 và theo tài khoản', 'P1', 'A đã ẩn cột Người duyệt.', ['Nhấn F5.', 'Đăng nhập B trên cùng trình duyệt.'], '—',
        ['A: vẫn ẩn sau F5 và khi đổi trình duyệt.', 'B: thấy đủ 11 cột.'], [208, 209])
S10.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', 'Đang lọc Kho Liên Ninh, 4 dòng.', ['Ẩn cột Kho, bấm Lưu.'], '—',
        ['Vẫn 4 dòng, bộ lọc Kho giữ nguyên, tổng số không đổi.'], [210, 211])

# ============================================================== XI. XUẤT DANH SÁCH EXCEL
S11 = Sec(11)
S11.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, [MENU, 'Bấm "Xuất Excel".'], '—',
        ['Mở "Chọn trường xuất Excel" 9 trường: Số phiếu, Ngày tạo, Kho, Hàng thừa, Hàng thiếu, Người tạo, Người duyệt, Ngày duyệt, '
         'Trạng thái.'], [212, 213])
S11.add('Trường chọn mặc định', 'P1', [PRE_LIST, 'Bảng đang hiện đủ 11 cột.'], ['Bấm "Xuất Excel".'], '—',
        ['Hiện tích sẵn 5/9: Số phiếu, Hàng thừa, Hàng thiếu, Người tạo, Trạng thái.',
         'Lưu ý: Ngày tạo, Kho, Người duyệt, Ngày duyệt chưa tích dù đang hiện — ghi nhận lệch so với quy ước tích theo cột đang hiện.'],
        [214, 215])
S11.add('Xuất tất cả trường', 'P0', PRE_LIST, ['Bấm "Chọn tất cả", bấm "Xuất file".'], '—',
        ['Tải file danh_sach_bien_ban_xu_ly_hang_thua_thieu_sau_kiem_ke.xlsx; báo "Xuất Excel thành công.".',
         'File có letterhead, tiêu đề "DANH SÁCH BIÊN BẢN XỬ LÝ HÀNG THỪA THIẾU SAU KIỂM KÊ", cột STT + 9 cột, khối ký.'],
        [216, 223, 224, 225])
S11.add('Xuất một số trường theo thứ tự kéo', 'P1', PRE_LIST, ['Tích Số phiếu, Trạng thái, kéo Trạng thái lên trước, bấm "Xuất file".'],
        '—', ['File có STT, Trạng thái, Số phiếu đúng thứ tự.'], [217, 226])
S11.add('Không chọn trường', 'P1', PRE_LIST, ['Bấm "Bỏ chọn hết".'], '—', ['"Đang chọn 0/9 trường", nút Xuất file bị khóa.'], 218)
S11.add('Xuất theo tìm kiếm và bộ lọc', 'P0', PRE_LIST, [ADV, 'Chọn Kho = LN - Liên Ninh, Ngày tạo 22/10/2026 – 22/10/2026.', 'Xuất Excel.'],
        '—', ['File chỉ có 4 biên bản Liên Ninh; dòng dưới tiêu đề "Từ ngày 22/10/2026 đến ngày 22/10/2026".'], [219, 220, 227])
S11.add('Xuất nhiều trang', 'P1', PRE_LIST, ['Đang ở trang 1 (10 dòng), bấm Xuất Excel, Xuất file.'], '—',
        ['File có đủ 13 biên bản (không chỉ trang đang xem).'], 221)
S11.add('Xuất danh sách rỗng', 'P2', 'Lọc ra 0 biên bản.', ['Xuất Excel, Xuất file.'], '—',
        ['Vẫn tải file có tiêu đề, tên cột, khối ký, không có dòng dữ liệu.'], 222)
S11.add('Định dạng và dữ liệu khớp', 'P0', [PRE_LIST, P6], ['Xuất tất cả trường, mở file, tìm BBXLKKHH-00006.'], '—',
        ['Ngày tạo "22/10/2026 14:58"; Hàng thừa / Hàng thiếu là ô số 2 / 1, căn phải; tiếng Việt hiển thị đúng.'], [228, 229, 230])
S11.add('Xuất Excel 1 biên bản', 'P0', [PRE_LIST, P6], ['Ở dòng BBXLKKHH-00006 bấm Xuất Excel.'], '—',
        ['Tải file bien_ban_xu_ly_hang_thua_thieu<số phiếu>.xlsx; báo "Xuất Excel thành công.".',
         'File có thông tin chung + 2 bảng Tab1 - Hàng Thừa, Tab2 - Hàng Thiếu như bản in.'], [223, 293])

# ============================================================== XII. RÀNG BUỘC
S12 = Sec(12)
S12.add('Chỉ lấy phiếu kiểm kê Hoàn thành', 'P0', [PRE_FORM, 'Kho Liên Ninh có thêm phiếu kiểm kê TPE.KKK-01070 ngày 22/10/2026 còn '
                                                                'Đang kiểm.'], GET, '—',
        ['Không có TPE.KKK-01070 trong khối Phiếu kiểm kê; khi phiếu đó Hoàn thành thì Lấy dữ liệu lại mới có.'], [274, 282])
S12.add('Giá vốn từ phiếu nhập / xuất điều chỉnh kiểm kê', 'P0', PRE_FORM, GET, '—',
        ['Dòng thừa lấy giá nhập của PNHĐCKK-00041 (35,000); dòng thiếu lấy giá xuất của PXHĐCKK-00068 (1,608,915.5).',
         'Hàng không có phiếu điều chỉnh > Đơn giá vốn 0, Phiếu xử lý trống.'], [272, 284])
S12.add('Không xóa kho vật lý đã dùng', 'P0', [PRE_LIST, 'Kho LN - Liên Ninh có trong biên bản.'],
        ['Vào phân hệ Kho > menu "Danh mục" > "Kho vật lý".', 'Xóa kho Liên Ninh.'], '—',
        ['Hệ thống chặn xóa vì kho đang được sử dụng.'], 270)
S12.add('Bút toán hiện ở sổ công nợ nhân viên', 'P1', 'BB2 đã duyệt.',
        ['Vào phân hệ Tài chính > nhóm "Nhân viên" > "Bảng cân đối phát sinh công nợ nhân viên".', 'Lọc nhân viên Bùi Duy Trước.'],
        '—', ['Phát sinh Nợ / Có tăng đúng số chi phí của BB2.'], 274)
S12.add('Không có biên bản mồ côi / dòng trùng', 'P2', 'A lưu BB1 rồi sửa và lưu lại 2 lần.', ['Mở chi tiết BB1.'], '—',
        ['Chỉ có đúng các dòng của phiếu được tích, không nhân đôi dòng sau mỗi lần lưu.'], [285, 286])
S12.add('Đổi tên kho vẫn giữ liên kết', 'P2', [PRE_LIST, 'Đổi tên kho Liên Ninh ở danh mục Kho vật lý thành "Liên Ninh 1".'],
        [MENU, 'Quan sát BBXLKKHH-00006.'], '—', ['Cột Kho hiện tên mới "Liên Ninh 1"; liên kết không mất.'], [278, 279])
S12.add('Nhân viên nghỉ việc vẫn hiện ở dòng', 'P2', [ACC_D, 'BB2 có NV chịu đã nghỉ việc.'], ['Mở chi tiết BB2.'], '—',
        ['Ô NV chịu vẫn hiện người đó; danh sách chọn mới chỉ có nhân viên đang làm việc.'], [276, 284])

# ============================================================== XIII. PHÂN QUYỀN
S13 = Sec(13)
S13.add('Quyền Kế toán kho', 'P0', ACC_A, ['Đăng nhập A.', MENU, 'Bấm "Tạo mới", Lấy dữ liệu.'], '—',
        ['Có nút Tạo mới; Lấy dữ liệu chạy được.', 'A chỉ thấy biên bản mình tạo.'], [289, 299])
S13.add('Không có Kế toán kho', 'P0', ACC_B, ['Đăng nhập B.', MENU], '—',
        ['Không có nút Tạo mới.', 'Mở thẳng màn Tạo rồi bấm Lấy dữ liệu > ' + NOPERM + '.'], [289, 295, 296])
S13.add('Quyền Duyệt', 'P0', ACC_D, ['Đăng nhập D.', MENU], '—',
        ['Thấy mọi biên bản Chờ duyệt (kể cả người khác lập), có nút Duyệt.'], [299, 300])
S13.add('Không có quyền Duyệt', 'P0', [ACC_A, BB2], ['Đăng nhập A.', 'Mở chi tiết BB2.'], '—',
        ['Không có nút Duyệt; ô xử lý chỉ đọc.'], 295)
S13.add('Quyền xem theo tổng công ty', 'P0', ACC_T, ['Đăng nhập T.', MENU], '—',
        ['Thấy mọi biên bản của mọi công ty, trừ biên bản Đang tạo của người khác.'], [287, 299])
S13.add('Quyền xem theo công ty', 'P0', ACC_C, ['Đăng nhập C.', MENU], '—',
        ['Thấy biên bản của công ty TPE + biên bản mình tạo; không thấy biên bản công ty khác.'], [287, 299])
S13.add('Không có quyền nào', 'P0', ACC_B, ['Đăng nhập B (đã tạo 0 biên bản).', MENU], '—',
        ['Danh sách "Không có dữ liệu phù hợp."; vẫn vào được màn, In / Xuất Excel danh sách rỗng.'], [287, 299])
S13.add('In, Xuất, Lịch sử theo phạm vi', 'P1', [ACC_C, 'Biên bản X của công ty khác.'], ['Mở link chi tiết X.'], '—',
        ['Chuyển ' + NOTFOUND + '; không In / Xuất / xem Lịch sử được.'], [293, 294, 296])
S13.add('Sửa chỉ người tạo', 'P0', [ACC_T, BB1], ['Đăng nhập T (có quyền tổng công ty).', MENU], '—',
        ['T không thấy BB1 Đang tạo của A; không có nút Sửa ở biên bản người khác.'], 290)
S13.add('Đổi quyền giữa thao tác', 'P1', [ACC_D, BB2, 'Quản trị gỡ quyền Duyệt của D khi D đang mở chi tiết BB2.'], ['D bấm "Duyệt".'],
        '—', ['Hệ thống từ chối, báo ' + NOPERM + '; BB2 vẫn Chờ duyệt.'], [298, 297])
S13.add('Đổi quyền Kế toán kho giữa thao tác', 'P2', [ACC_A, 'Quản trị gỡ quyền Kế toán kho của A khi A đang ở màn Tạo.'],
        ['A bấm "Lưu".'], '—', ['Báo ' + NOPERM + ', không lưu.'], 298)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'CHỈNH SỬA', S4),
    ('V', 'GỬI DUYỆT', S5),
    ('VI', 'DUYỆT PHIẾU', S6),
    ('VII', 'LỊCH SỬ THAY ĐỔI', S7),
    ('VIII', 'XEM CHI TIẾT BIÊN BẢN XỬ LÝ HÀNG THỪA, THIẾU', S8),
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
                feature_name='Biên bản xử lý hàng thừa, thiếu sau kiểm kê - Cập nhật ngày 06/11/2026',
                module_name='Biên bản xử lý hàng thừa, thiếu', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

# -*- coding: utf-8 -*-
"""Testcase màn "Kiểm kê theo hàng hóa" (phiếu kiểm kê theo hàng hóa) — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026
(tc_chuan.build_chuan, loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (lý do — đọc code 06/11/2026): màn là chứng từ có vòng đời Đang tạo > Đang kiểm > Chờ KT duyệt > (Không duyệt) >
Chờ xử lý > Đang xử lý > Hoàn thành, có Thêm (lập tay / từ 2 loại kế hoạch) / Sửa / Xóa theo trạng thái + người tạo, Lưu và gửi,
Cập nhật kết quả (Gửi duyệt), Duyệt kết quả / Không duyệt (popup ghi chú), Xử lý (mở 3 màn tạo phiếu xử lý), In phiếu, Xuất Excel 1
phiếu, lịch sử. Không có route / nút Khóa, Hủy phiếu, Import → bỏ 3 nhóm đó.
Thứ tự nhóm chuẩn 'phieu': I Hiển thị · II Tìm kiếm & lọc (gồm Cài đặt bộ lọc) · III Thêm mới (Lưu, Lưu và tiếp tục, chọn kế
hoạch, thêm hàng + làm mới số liệu + ĐVT kiểm kê, rời màn) · IV Chỉnh sửa · V Xóa · VI Gửi duyệt (Lưu và gửi + Cập nhật kết quả /
Gửi duyệt) · VII Duyệt phiếu (Duyệt kết quả + bước Xử lý sau duyệt) · VIII Không duyệt phiếu · IX Lịch sử · X Xem chi tiết · XI In
phiếu (kèm In danh sách) · XII Tùy chỉnh cột · XIII Xuất danh sách Excel (kèm Xuất 1 phiếu) · XIV Ràng buộc · XV Phân quyền.
Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../kiem-ke-theo-vi-tri/gen_testcase.py (06/11, check_tc 0 lỗi).
Nguồn hành vi (đọc 06/11/2026, nhánh develop): FE pages/warehouse/self-inventories/**; BE Modules/Finance SelfInventory* (Entity /
Service / WriteService / Controller / 2 FormRequest / PrintService / Export), PhysicalStockReader, WarehouseInventoryLockService,
WarehouseImportWriteService, ProductTransferWriteService, PositionTransferWriteService, WarehouseInventory{Import,Export}WriteService.
Số liệu mẫu: dev-hrm 06/11/2026 (DNS Admin): 898 phiếu (879 Hoàn thành, 5 Đang xử lý, 4 Chờ xử lý, 2 Đang kiểm, 6 Không duyệt,
1 Chờ KT duyệt TPE.KKK-01097); TPE.KKK-01089 có 8 mốc lịch sử.
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
MENU = 'Vào phân hệ Kho > menu "Kiểm kho" > nhóm "Theo vị trí" > bấm "Kiểm kê theo hàng hóa".'
MENU_TC = 'Vào phân hệ Tài chính > menu "Kiểm kê" > bấm "Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả".'
TAO = [MENU, 'Bấm "Tạo mới".']
ADV = 'Bấm Tìm kiếm nâng cao.'

Q1 = 'Lập phiếu kiểm kê kho theo hàng hóa'
Q2 = 'Ban kiểm soát duyệt kết quả kiểm kê'
Q3 = 'Xử lý phiếu kiểm kê hàng hóa'
Q4 = 'Kế toán kho'
Q5 = 'Tạo phiếu nhập kho điều chỉnh kiểm kê'
V1 = 'Xem phiếu kiểm kê hàng hóa - theo tổng công ty'
V2 = 'Xem phiếu kiểm kê hàng hóa - theo công ty'
CONFLICT = 'Trạng thái đã bị thay đổi. Vui lòng load lại trang'
NOTFOUND = 'Không tìm thấy phiếu kiểm kê hoặc bạn không có quyền xem.'
NOPERM = 'Bạn không có quyền thực hiện chức năng này.'
INVALID = 'Vui lòng kiểm tra lại thông tin đã nhập.'
PLAN404 = 'Không tìm thấy kế hoạch kiểm kê hoặc bạn không được lập phiếu cho kế hoạch này.'

ACC_A = 'Tài khoản A: thủ kho kho Hải Phòng, công ty TPE, không có quyền nào của màn.'
ACC_L = 'Tài khoản L: thủ kho công ty TPE, có quyền "%s".' % Q1
ACC_B = 'Tài khoản B: nhân viên công ty TPE, không có quyền nào của màn, chưa lập phiếu nào.'
ACC_C = 'Tài khoản C: có quyền "%s", thuộc công ty TPE.' % V2
ACC_T = 'Tài khoản T: có quyền "%s".' % V1
ACC_K = 'Tài khoản K: Ban kiểm soát công ty TPE, có quyền "%s", không có quyền xem theo cấp.' % Q2
ACC_X = 'Tài khoản X: người xử lý công ty TPE, có quyền "%s", không có quyền xem theo cấp.' % Q3
ACC_KT = 'Tài khoản KT: công ty TPE, có quyền "%s".' % Q4
PRE_LIST = ('Tài khoản DNS Admin (Super admin); trong phạm vi xem có 898 phiếu: 879 Hoàn thành, 6 Không duyệt, 5 Đang xử lý, '
            '4 Chờ xử lý, 2 Đang kiểm, 1 Chờ KT duyệt.')
P85 = ('Phiếu TPE.KKK-01085: lập từ kế hoạch TPE.KHKKHH-00019, kho Liên Ninh, Hoàn thành, Người tạo / Người duyệt DNS Admin, '
       'Ngày kiểm kê 28/10/2026, Ngày tạo 28/10/2026 10:39, Ngày cập nhật 28/10/2026 11:13; 1 hàng "Giá để sạc ắc quy" (2Q-GSAQ), 1 file.')
P89 = 'Phiếu TPE.KKK-01089 lập tay, kho Kỹ thuật công nghệ, Hoàn thành, 8 mốc lịch sử.'
KHO = ('Kho Hải Phòng (mã HP) gắn kho kế toán của 3 công ty TPE, TPHP, TPV; hàng "Mỡ bôi trơn L1 (15kg/xô)" (ANOP-ANOPECL115KG) '
       'tồn 10 Xô 15KG tại vị trí KHOANG6, công ty TPHP.')
PRE_FORM = ACC_A + '\n' + KHO
KH = 'Kế hoạch KH1 (Kế hoạch kiểm kê theo hàng hóa) Đang kiểm, kho Hải Phòng, 2 hàng, hội đồng 1 thành viên.'
KHT = 'Kế hoạch tổng TPE.KHTKK-00005 Đã duyệt, kỳ từ hôm nay, 3 kho Chăm sóc khách hàng, Kho Dự án trọng điểm, Hải Phòng.'
PH1 = 'Phiếu PH1 trạng thái Đang tạo do A lập tay ở kho Hải Phòng, 1 hàng Mỡ bôi trơn L1.'
PH2 = 'Phiếu PH2 trạng thái Đang kiểm do A lập, chưa có file kết quả; dòng lô của Mỡ bôi trơn L1 SL 10.'
PH3 = 'Phiếu PH3 trạng thái Chờ KT duyệt do A lập, có dòng Thực kiểm 9 / SL 10 (Chênh lệch -1).'
PH3B = 'Phiếu PH3B trạng thái Chờ KT duyệt do A lập, mọi dòng Chênh lệch = 0.'
PH4 = 'Phiếu PH4 trạng thái Chờ xử lý: hàng H1 tổng chênh +2 (dòng thừa), hàng H2 tổng chênh -3 (dòng thiếu), chưa lập phiếu xử lý.'
FILL = TAO + ['Chọn Kho = HP - Hải Phòng (Công ty thuê kho tự chọn TPE, TPHP, TPV).', 'Bấm Thêm hàng hóa, tích "Mỡ bôi trơn L1 (15kg/xô)", bấm chọn.',
              'Ở dòng 1 Hội đồng chọn Thành viên = Bùi Duy Trước.']
FULL = ['Kho: HP - Hải Phòng', 'Công ty thuê kho: TPE, TPHP, TPV', 'Hàng hóa: Mỡ bôi trơn L1 (15kg/xô)', 'Thành viên: Bùi Duy Trước']
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
     'Lập phiếu kiểm kê theo từng mặt hàng cho một hoặc nhiều kho (lập tay, từ Kế hoạch kiểm kê theo hàng hóa hoặc từ Kế hoạch tổng '
     'kiểm kê hàng hóa), chọn ĐVT kiểm kê từng lô, nhập kết quả thực kiểm + hàng thừa khác + file kết quả, Ban kiểm soát duyệt / không '
     'duyệt, người xử lý lập phiếu điều chuyển vị trí / nhập kho / xuất kho điều chỉnh cho phần chênh lệch. Phiếu KHÔNG tự đổi tồn kho.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Danh sách: phiếu trong phạm vi xem; trạng thái Đang tạo (xám), Đang kiểm (xanh dương), Chờ KT duyệt (vàng), Không duyệt (đỏ), '
     'Chờ xử lý (vàng), Đang xử lý (xanh dương), Hoàn thành (xanh lá).\n'
     '- Lối "Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả": chỉ phiếu Chờ KT duyệt (với Ban kiểm soát).\n'
     '- Bảng Hàng hóa: hàng có tồn tại vị trí có lô của công ty thuê kho; mỗi lô còn tồn >= 1 dòng ĐVT kiểm kê.\n'
     '- Popup Chọn kế hoạch: Kế hoạch theo hàng hóa Đang kiểm + Kế hoạch tổng Đã duyệt còn trong kỳ.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác (kể cả Super admin).\n- Phiếu ngoài phạm vi quyền xem (trừ phiếu đang chờ chính người đó '
     'duyệt / xử lý).\n- Lô / vị trí / hàng đã hết tồn khi thêm hàng hoặc làm mới số liệu.\n- Kho đã khóa ở ô lọc Kho (trừ khi bật công tắc ổ khóa).'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô Ngày tạo lọc theo ngày lập phiếu, lấy trọn hai ngày biên. Cột Ngày kiểm kê = ngày lưu gần nhất của phiếu.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Phiếu > hàng (SL tồn kho) > vị trí > lô (công ty, tồn theo lô) > dòng ĐVT kiểm kê (Thực kiểm, Chênh lệch, Ghi chú).\n'
     '- Kèm: kho, công ty thuê kho, hàng thừa khác (hàng > vị trí > Thực kiểm), hội đồng (thành viên + chức vụ), file kết quả.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Tổng SL × hệ số các dòng ĐVT kiểm kê của 1 lô = tồn theo lô.\n- Chênh lệch = Thực kiểm - SL (máy chủ tự tính).\n'
     '- Không trùng hàng trên phiếu, không trùng thành viên hội đồng; hàng của kế hoạch tổng chỉ có ở 1 phiếu.'),
    ('7. Phân quyền cấp',
     '- %s: xem mọi phiếu.\n- %s: phiếu công ty mình + của mình.\n- Không quyền xem: chỉ phiếu mình tạo.\n'
     '- Thêm mới lập tay: mọi người dùng. %s: lập phiếu từ kế hoạch.\n- %s: Duyệt kết quả / Không duyệt, lối chờ duyệt kết quả.\n'
     '- %s: Xử lý (nút nhập kho điều chuyển cần thêm "%s").\n- %s: nhận thông báo Chờ duyệt.\n'
     '- Sửa / Xóa / Cập nhật kết quả: người tạo phiếu (không cần quyền riêng).' % (V1, V2, Q1, Q2, Q3, Q5, Q4)),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là khoảng thứ tự dòng của trang, N là tổng phiếu khớp bộ lọc trong phạm vi xem.\n'
     '- Cột Chênh lệch = Thực kiểm - SL, khác 0 chữ đỏ. SL tồn kho = tồn của hàng trong các kho đã chọn.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: A (thủ kho, không quyền), L (có quyền lập phiếu từ kế hoạch), B (không quyền), C (xem theo công ty), '
     'T (xem tổng công ty), K (Ban kiểm soát), X (người xử lý), KT (Kế toán kho), DNS Admin (Super admin).\n'
     '- Lưu ý: Lưu và gửi, Gửi duyệt gửi NGAY, không có hộp xác nhận; Duyệt / Không duyệt qua popup ghi chú.\n'
     '- Lưu ý: form chỉ tự chặn Ghi chú > 255 ký tự; lỗi bắt buộc do hệ thống trả về sau khi bấm Lưu, hiện dưới từng ô.\n'
     '- Lưu ý: số tồn trên phiếu là ảnh chụp lúc thêm hàng / làm mới số liệu; mở màn Sửa thì nạp lại tồn hiện tại.\n'
     '- Lưu ý: xóa phiếu KHÔNG trả trạng thái kế hoạch nguồn.\n'
     '- Màn Tạo / Sửa / Chi tiết là TRANG riêng, không phải cửa sổ nổi.'),
]

SCREEN = ListScreen(menu=MENU, title='Danh sách phiếu kiểm kê theo hàng hóa', total=898, quick_label='số phiếu',
                    quick_sample='01085', quick_hit='phiếu TPE.KKK-01085',
                    filters=[('Trạng thái', 'Hoàn thành'), ('Kho', 'HP - Hải Phòng')], unit='phiếu')

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Mở lối "chờ duyệt kết quả" ở phân hệ Tài chính', 'P0', [ACC_K, 'Có 1 phiếu Chờ KT duyệt TPE.KKK-01097 (công ty TPE).'],
       ['Đăng nhập K.', MENU_TC], '—',
       ['Tiêu đề "Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả".', 'Chỉ 1 dòng TPE.KKK-01097, "Hiển thị 1–1 / 1".'], 1)
S1.add('Lối chờ duyệt khi không có quyền Ban kiểm soát', 'P1', [ACC_A, 'A đã lập 3 phiếu (1 Đang kiểm, 2 Hoàn thành).'], ['Đăng nhập A.', MENU_TC],
       '—', ['Chỉ thấy 3 phiếu của A (đường link là cách xem, không cấp thêm quyền).'], 1)
S1.add('Chuyển giữa 2 lối vào', 'P1', [ACC_K, 'Đang ở lối phân hệ Kho, lọc Trạng thái = Hoàn thành.'], [MENU_TC, MENU], '—',
       ['Lối chờ duyệt không mang theo bộ lọc của lối Kho, tiêu đề đổi theo lối.', 'Quay lại lối Kho: bộ lọc Hoàn thành được khôi phục.'], [1, 45])
S1.add('Tham số lối vào lạ trên thanh địa chỉ', 'P2', PRE_LIST, ['Mở màn từ lối Kho.', 'Sửa tay tham số lối vào trên thanh địa chỉ thành "abc", Enter.'],
       '—', ['Màn hiển thị như lối phân hệ Kho, không lỗi, không lộ thêm dữ liệu.'], 1)
S1.add('Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Cả 3 nơi đều là "Danh sách phiếu kiểm kê theo hàng hóa".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE_LIST, [MENU, 'Quan sát khối bộ lọc và thanh công cụ.'], '—',
       ['Khối bộ lọc: ô tìm nhanh (gợi ý "Tìm theo số phiếu"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
        'Thanh công cụ: Tạo mới, Xuất Excel, In danh sách, nút biểu tượng cột.',
        'Dòng Hoàn thành: cột Hành động có In, Xuất Excel, Lịch sử.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 13 cột: STT, Số phiếu, Kế hoạch kiểm kê, Ngày kiểm kê, Kho, Trạng thái, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, '
        'Ngày cập nhật, Người cập nhật, Hành động.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 13/13 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp phiếu', 'P0', [PRE_LIST, P85], [MENU, 'Tìm "TPE.KKK-01085", đối chiếu dòng.'], '—',
       ['Kế hoạch kiểm kê "TPE.KHKKHH-00019", Ngày kiểm kê "28/10/2026", Kho "Liên Ninh", Trạng thái "Hoàn thành", Người tạo / Người duyệt '
        '"DNS Admin", Ngày tạo "28/10/2026 10:39", Ngày duyệt "28/10/2026 10:39", Ngày cập nhật "28/10/2026 11:13".'], [6, 58])
S1.add('Cột Kế hoạch kiểm kê là liên kết', 'P1', [PRE_LIST, 'Phiếu TPE.KKK-01097 lập từ kế hoạch tổng TPE.KHTKK-00005.'],
       [MENU, 'Bấm mã "TPE.KHTKK-00005" ở dòng TPE.KKK-01097.'], '—', ['Mở chi tiết Kế hoạch tổng kiểm kê TPE.KHTKK-00005.'], 6)
S1.add('Trạng thái bản ghi', 'P0', PRE_LIST, [MENU, ADV, 'Mở ô Trạng thái.', 'Quan sát cột Trạng thái.'], '—',
       ['Ô có 7 lựa chọn: Đang tạo, Đang kiểm, Chờ KT duyệt, Không duyệt, Chờ xử lý, Đang xử lý, Hoàn thành.',
        'Nhãn: Đang tạo xám; Đang kiểm, Đang xử lý xanh dương; Chờ KT duyệt, Chờ xử lý vàng; Không duyệt đỏ; Hoàn thành xanh lá.'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', ACC_B, ['Đăng nhập B.', MENU], '—',
       ['Bảng hiện "Không có dữ liệu phù hợp.", không báo lỗi; vẫn có nút Tạo mới.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       ['Bảng hiện "Không có dữ liệu phù hợp.".'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 20 phiếu, tự về trang 1, "Hiển thị 1–20 / 898".', 'Chỉ nạp lại 1 lần.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–20 / 898".', 'Bước 3: "Hiển thị 1–10 / 898".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—', ['Bước 2: trang 90 "Hiển thị 891–898 / 898".', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang 90 quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.'], '—', ['Trang 2 đánh số 11–20.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', ADV, 'Chọn Trạng thái = Hoàn thành.'],
       'Trạng thái: Hoàn thành', ['Tự nạp lại ở trang 1; "Hiển thị 1–10 / 879".'], 17)
S1.add('Sắp xếp tăng dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Số phiếu.'], '—', ['Xếp theo số phiếu tăng dần, mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Số phiếu', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Số phiếu 2 lần.'], '—', ['Xếp theo số phiếu giảm dần.'], 21)
S1.add('Sắp xếp theo các cột ngày', 'P1', PRE_LIST,
       [MENU, 'Bấm tiêu đề Ngày kiểm kê (2 lần).', 'Bấm tiêu đề Ngày tạo, Ngày duyệt, Ngày cập nhật.'], '—',
       ['Ngày kiểm kê: lần 1 cũ nhất trên, lần 2 mới nhất trên.', 'Ngày tạo / Ngày duyệt / Ngày cập nhật sắp đúng thứ tự ngày giờ.',
        'Khi mới vào chưa chọn cột nào: phiếu tạo mới nhất trên, các cột hiện biểu tượng sắp xếp trung tính.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Kế hoạch kiểm kê, Kho, Trạng thái, Người tạo, Người duyệt, Người cập nhật.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Số phiếu (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự tăng của trang 1.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 2.', 'Bấm tiêu đề Ngày kiểm kê.'], '—', ['Về trang 1.'], 25)
S1.add('Nút thao tác theo trạng thái', 'P0', [PRE_LIST, 'TPE.KKK-01090 Đang kiểm do DNS Admin tạo; TPE.KKK-01096 Chờ xử lý; TPE.KKK-01097 Chờ KT duyệt.'],
       [MENU, 'Quan sát cột Hành động 3 dòng.'], '—',
       ['01090: Cập nhật kết quả, In và nút ba chấm "Hành động khác" chứa Xuất Excel, Lịch sử.',
        '01096: Xử lý, In, ba chấm.', '01097: Duyệt, In, ba chấm.'], [3, 34])
S1.add('Mở màn từ menu khi phân hệ Kho đang bật', 'P1', PRE_LIST,
       ['Đăng nhập.', 'Bấm nút lưới phân hệ ở đầu trang, chọn ô "Kho".', 'Bấm "Kiểm kho" ở thanh bên, chọn nhóm "Theo vị trí".'], '—',
       ['Nhóm Theo vị trí có 2 mục: Kiểm kê theo vị trí, Kiểm kê theo hàng hóa.', 'Bấm "Kiểm kê theo hàng hóa" mở màn danh sách.'], 1)
S1.add('Mở màn từ thông báo của Kế toán kho', 'P1', [ACC_KT, PH3, 'KT đã nhận thông báo "Chờ duyệt" của PH3.'],
       ['Đăng nhập KT.', 'Bấm chuông thông báo, bấm thông báo của PH3.'], '—',
       ['Mở màn chi tiết PH3 nếu PH3 trong phạm vi xem của KT; ngoài phạm vi thì chuyển trang "Không tìm thấy trang".'], 1)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo số phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "TPE.KKK-01085", bấm Tìm kiếm.'], 'Ô tìm nhanh: TPE.KKK-01085',
       ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần số phiếu', 'P0', PRE_LIST, [MENU, 'Nhập "TPSG", bấm Tìm kiếm.'], 'Ô tìm nhanh: TPSG',
       ['Còn 303 phiếu có số phiếu chứa "TPSG".'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "tpe.kkk-01085", bấm Tìm kiếm.'], '—', ['Ra TPE.KKK-01085.'], 28)
S2.add('Có dấu / không dấu ở ô Tên hàng hóa', 'P2', PRE_LIST, [MENU, ADV, 'Nhập Tên hàng hóa "gia de sac", bấm Tìm kiếm.'], '—',
       ['Ra các phiếu có hàng "Giá để sạc ắc quy" nếu cơ sở dữ liệu so khớp không dấu.', 'Lưu ý: so khớp theo cách so sánh chữ của cơ sở dữ liệu.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; ký tự % được hiểu là ký tự đại diện nên ra toàn bộ.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  TPE.KKK-01085  ", bấm Tìm kiếm.'], '—', ['Ra TPE.KKK-01085.'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "TPE.KKK-01085", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Hiện lại đủ 898 phiếu.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST, [MENU, 'Nhập "01085", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'], '—',
       ['Cả 2 cách đều ra TPE.KKK-01085, về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['Các ô Kho, Trạng thái, Người tạo, Người duyệt, Mã hàng hóa, Tên hàng hóa, Ngày tạo đều trống.', 'Đủ 898 phiếu.'], 36)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Chờ xử lý.'], '—',
       ['Lọc ngay; còn 4 phiếu TPE.KKK-01096, 01080, 01066, 01064.'], 37)
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = DNS Admin.'], '—',
       ['Còn 34 phiếu do DNS Admin tạo.', 'Ô Người tạo chỉ liệt kê người đã lập phiếu, dạng "Họ tên - Phòng ban - Mã NV".'], 37)
S2.add('Lọc Người duyệt', 'P1', PRE_LIST, [MENU, ADV, 'Chọn Người duyệt = DNS Admin.'], '—',
       ['Còn 31 phiếu do DNS Admin duyệt / không duyệt.', 'Phiếu chưa duyệt không xuất hiện.'], 37)
S2.add('Lọc Mã hàng hóa', 'P1', PRE_LIST, [MENU, ADV, 'Nhập Mã hàng hóa "2Q-GSAQ", bấm Tìm kiếm.'], '—',
       ['Ra 4 phiếu TPE.KKK-01086, 01085, 01076, 01070.'], 37)
S2.add('Lọc Tên hàng hóa', 'P1', PRE_LIST, [MENU, ADV, 'Nhập Tên hàng hóa "Giá để sạc", bấm Tìm kiếm.'], '—',
       ['Ra 4 phiếu TPE.KKK-01086, 01085, 01076, 01070.', 'Chỉ gõ chưa bấm Tìm kiếm thì chưa lọc.'], 37)
S2.add('Lọc Ngày tạo lấy trọn ngày biên', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày tạo 31/10/2026 – 31/10/2026.'], '—',
       ['Ra 4 phiếu TPE.KKK-01092, 01091, 01090, 01089.', 'Bỏ trống ngày cuối vẫn lọc được từ ngày đầu.'], 37)
S2.add('Lọc Kho', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Kho = HP - Hải Phòng.'], '—',
       ['Còn 6 phiếu có gắn kho Hải Phòng (gồm phiếu nhiều kho TPE.KKK-01097, 01096).'], 37)
S2.add('Ô Kho: công tắc xem kho đã khóa', 'P1', [PRE_LIST, 'Có 1 kho đã khóa ở danh mục Kho vật lý.'], [MENU, ADV, 'Mở ô Kho.', 'Bật công tắc ổ khóa, mở lại ô Kho.'],
       '—', ['Mặc định không có kho đã khóa.', 'Bật công tắc: có thêm kho đã khóa, gắn biểu tượng ổ khóa trước tên; tắt lại thì ẩn (trừ kho đang lọc).'], [37, 283])
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Hoàn thành.', 'Chọn Kho = HP - Hải Phòng.'], '—',
       ['Chỉ còn 2 phiếu TPE.KKK-01094, 01091.'], 38)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST, [MENU, 'Nhập "TPSG", bấm Tìm kiếm.', ADV, 'Chọn Kho = HP - Hải Phòng.'], '—',
       ['"Không có dữ liệu phù hợp." vì không phiếu TPSG nào gắn kho Hải Phòng.'], [39, 40])
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Hoàn thành.', 'Bấm trang 2.'], '—',
       ['"Hiển thị 1–10 / 879" rồi "Hiển thị 11–20 / 879"; STT liên tục.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Trạng thái = Hoàn thành.', ['Bấm tiêu đề Số phiếu.'], '—',
       ['Chỉ 879 phiếu đang lọc được sắp; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "TPE", lọc Kho Hải Phòng, sắp Số phiếu, ở trang 2.', ['Bấm Làm mới.'],
       '—', ['Mọi ô kể cả ô tìm nhanh về trống, bỏ sắp xếp, nạp lại trang 1, đủ 898 phiếu; vẫn ở lối đang xem.'], 44)
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Hoàn thành, chưa mở màn con.'], ['Nhấn F5.'], '—',
       ['Bộ lọc trở về trống, đủ 898 phiếu (chỉ nhớ khi đi vào màn con của màn này).'], 46)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Người duyệt, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô Người duyệt.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Hoàn thành.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Trạng thái, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị bỏ, nạp lại đủ 898 phiếu.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Người duyệt.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Người duyệt vẫn ẩn.', 'Bước 2: tích đủ 7 mục, Người duyệt hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Ngày tạo lên đầu, bấm Lưu.'], '—',
       ['Ô Ngày tạo đứng đầu khối Tìm kiếm nâng cao; cấu hình giữ sau khi đăng nhập lại, áp cho cả 2 lối vào.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo', 'P0', PRE_FORM, TAO, '—', ['Mở TRANG "Tạo phiếu kiểm kê theo hàng hóa", tab cùng tiêu đề.'], 49)
S3.add('Mở màn Tạo từ màn Kế hoạch kiểm kê theo hàng hóa', 'P0', [ACC_L, KH],
       ['Vào phân hệ Tài chính > menu "Kiểm kê" > bấm "Kế hoạch kiểm kê theo hàng hóa".', 'Ở dòng KH1 bấm Lập phiếu.'], '—',
       ['Mở màn Tạo phiếu với ô Kế hoạch kiểm kê = mã KH1, Kho, Công ty thuê kho khóa, 2 hàng và hội đồng nạp sẵn.',
        'Không có nút Thêm hàng hóa, không có nút xóa hàng.'], [49, 274])
S3.add('Mở màn Tạo từ màn Kế hoạch tổng kiểm kê', 'P1', [ACC_L, KHT],
       ['Vào phân hệ Tài chính > menu "Kiểm kê" > bấm "Kế hoạch tổng kiểm kê hàng hóa".', 'Ở dòng TPE.KHTKK-00005 bấm Lập phiếu kiểm kê.'], '—',
       ['Màn Tạo nạp sẵn kế hoạch tổng: 3 kho, Công ty thuê kho TPE, TPHP, TPV (khóa); bảng hàng trống, có nút Thêm hàng hóa.'], [49, 274])
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải hiện tên người đang đăng nhập.', 'Không có ô Số phiếu (mã tự sinh khi lưu).'], 50)
S3.add('Các trường, khối và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Kế hoạch kiểm kê (gợi ý "Chọn kế hoạch kiểm kê"), Ngày kiểm kê *, Kho *, Công ty thuê kho *, Ghi chú.',
        'Hàng hóa * (bảng "Không có dữ liệu") có nút Làm mới số liệu, Thêm hàng hóa.',
        'Hội đồng kiểm kê * có 1 dòng trống và nút Thêm dòng.',
        'Chân màn: Lưu, Lưu và gửi, Lưu và tiếp tục, Quay lại; không có File đính kèm, không có Hàng thừa khác.'], [51, 54])
S3.add('Trường bắt buộc / không bắt buộc', 'P0', PRE_FORM, TAO + ['Quan sát dấu *.'], '—',
       ['Dấu * ở Ngày kiểm kê, Kho, Công ty thuê kho, Hàng hóa, ĐVT kiểm kê, Hội đồng kiểm kê, Thành viên, Chức vụ.',
        'Kế hoạch kiểm kê, Ghi chú không bắt buộc.'], 52)
S3.add('Giá trị mặc định', 'P0', PRE_FORM, TAO, '—',
       ['Ngày kiểm kê = ngày hôm nay, ô khóa.', 'Kho trống; Công ty thuê kho khóa, gợi ý "Chọn công ty thuê kho".', 'Hội đồng có 1 dòng trống.'], 53)
S3.add('Chọn kho tự chọn công ty thuê kho', 'P0', PRE_FORM, TAO + ['Chọn Kho = HP - Hải Phòng.'], '—',
       ['Ô Công ty thuê kho mở khóa và tự chọn hết TPE, TPHP, TPV (các công ty có kho kế toán gắn kho Hải Phòng).'], [53, 283])
S3.add('Lưu phiếu lập tay hợp lệ đầy đủ', 'P0', PRE_FORM, FILL + ['Nhập Ghi chú "Kiểm định kỳ".', 'Bấm Lưu.'], FULL + ['Ghi chú: Kiểm định kỳ'],
       [OK_LIST, 'Số phiếu dạng "TPE.KKK-<số>" theo công ty của A.'], [55, 58, 59, 79])
S3.add('Lưu chỉ với trường bắt buộc tối thiểu', 'P0', PRE_FORM, FILL + ['Không chọn kế hoạch, không nhập Ghi chú.', 'Bấm Lưu.'],
       FULL, [OK_LIST], [56, 57])
S3.add('Dữ liệu sau lưu', 'P0', [PRE_FORM, 'A vừa lưu phiếu ở TC_03.009.'], ['Bấm số phiếu vừa tạo.'], '—',
       ['Chi tiết: Kho Hải Phòng, Công ty thuê kho TPE, TPHP, TPV, Ghi chú "Kiểm định kỳ"; bảng có Mỡ bôi trơn L1, vị trí KHOANG6 (10), '
        'công ty TPHP, ĐVT kiểm kê Xô 15KG, Tồn theo lô 10.', 'Hội đồng: Bùi Duy Trước, chức vụ tự điền.'], 58)
S3.add('Trạng thái mặc định sau Lưu', 'P0', [PRE_FORM, 'A vừa lưu phiếu.'], [MENU, 'Đăng nhập DNS Admin, mở danh sách.'], '—',
       ['A thấy phiếu Đang tạo (nhãn xám).', 'DNS Admin KHÔNG thấy phiếu này (Đang tạo chỉ người tạo thấy).'], [59, 84])
S3.add('Lịch sử tạo', 'P1', [PRE_FORM, 'A vừa lưu phiếu.'], ['Ở dòng phiếu bấm Lịch sử.'], '—',
       ['Có 1 mốc "Tạo mới", Người thực hiện A, thời điểm lưu.'], [60, 176])
S3.add('Bỏ trống mọi trường bắt buộc', 'P0', PRE_FORM, TAO + ['Bấm Lưu ngay.'], '—',
       ['Báo "%s", không lưu.' % INVALID,
        'Lỗi đỏ "Bắt buộc phải nhập" CÙNG LÚC dưới ô Kho, Công ty thuê kho, bảng Hàng hóa, Thành viên, Chức vụ.', 'Cuộn tới ô lỗi đầu tiên.'],
       [61, 70, 80])
S3.add('Chọn kho nhưng chưa thêm hàng', 'P0', PRE_FORM, TAO + ['Chọn Kho Hải Phòng, chọn thành viên.', 'Bấm Lưu.'], '—',
       ['Chỉ báo "Bắt buộc phải nhập" dưới bảng Hàng hóa, khung bảng viền đỏ.'], [61, 62])
S3.add('Hội đồng trùng thành viên', 'P0', PRE_FORM, FILL + ['Bấm Thêm dòng, chọn lại Bùi Duy Trước.', 'Bấm Lưu.'], '—',
       ['Dòng hội đồng báo "Bị trùng.", không lưu.'], [62, 67])
S3.add('Xóa hết dòng hội đồng', 'P1', PRE_FORM, FILL + ['Bấm thùng rác ở dòng hội đồng.', 'Bấm Lưu.'], '—',
       ['Bảng hội đồng hiện "Không có dữ liệu", báo "Bắt buộc phải nhập" dưới bảng.'], 61)
S3.add('Chọn thành viên tự điền chức vụ', 'P1', PRE_FORM, TAO + ['Chọn Thành viên = Bùi Duy Trước.', 'Bỏ chọn thành viên.'], '—',
       ['Bước 1: ô Chức vụ tự điền chức vụ đầu tiên của nhân viên.', 'Bước 2: ô Chức vụ bị xóa.'], 53)
S3.add('Ghi chú vượt 255 ký tự', 'P1', PRE_FORM, FILL + ['Dán 256 ký tự vào Ghi chú.', 'Bấm Lưu.'], 'Ghi chú: 256 ký tự',
       ['Ô chỉ nhận tối đa 255 ký tự; nếu dán lọt thì báo "Vui lòng nhập tối đa 255 ký tự." dưới ô, không lưu.'], [63, 64, 81])
S3.add('Ghi chú đúng 255 ký tự, ký tự đặc biệt, khoảng trắng', 'P2', PRE_FORM, FILL + ['Nhập Ghi chú 255 ký tự có "@#<>" và khoảng trắng đầu.', 'Bấm Lưu.'],
       'Ghi chú: 255 ký tự', ['Lưu được; chi tiết hiện đúng nội dung, ký tự đặc biệt hiển thị nguyên văn.'], [65, 66, 68, 69])
S3.add('Lỗi biến mất sau khi sửa', 'P1', 'Đang có lỗi đỏ ở TC_03.014.', ['Chọn Kho Hải Phòng.', 'Thêm hàng.', 'Chọn thành viên.'], '—',
       ['Lỗi Kho, Công ty thuê kho, Hàng hóa, Thành viên, Chức vụ lần lượt biến mất ngay khi sửa đúng.'], 71)
S3.add('Trùng dữ liệu: 2 phiếu cùng kho, cùng hàng (lập tay)', 'P1', [PRE_FORM, PH1], FILL + ['Bấm Lưu.'], FULL,
       ['Lưu được; 2 phiếu có số phiếu khác nhau (không có trường duy nhất).'], [67, 75, 82])
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, FILL + ['Bấm Lưu và tiếp tục.'], FULL,
       ['Báo "Lưu thành công.", VẪN ở màn Tạo.', 'Form trắng: Kế hoạch, Kho, Công ty thuê kho, Hàng hóa trống, Hội đồng 1 dòng trống.',
        'Phiếu vừa lưu ở trạng thái Đang tạo.'], [72, 76, 77, 83])
S3.add('Lưu và tiếp tục khi vào từ kế hoạch', 'P1', [ACC_L, KH], ['Mở màn Tạo từ nút Lập phiếu của KH1.', 'Bấm Lưu và tiếp tục.'],
       '—', ['Lưu thành công, form trắng KHÔNG còn KH1 (kế hoạch đã chuyển Đã lập phiếu kiểm kê).'], [77, 84])
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
S3.add('Nhập rồi trả về như ban đầu', 'P2', PRE_FORM, TAO + ['Nhập Ghi chú "abc".', 'Xóa hết Ghi chú.', 'Bấm Quay lại.'],
       '—', ['Không hỏi "Thông tin chưa lưu".'], [98, 99])
S3.add('Không thao tác lâu', 'P2', PRE_FORM, FILL + ['Để yên 30 phút.', 'Bấm Lưu.'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên, chuyển về đăng nhập, không lưu.'], 100)
S3.add('Bấm Lưu liên tục', 'P0', PRE_FORM, FILL + ['Bấm Lưu 3 lần thật nhanh.'], FULL, ['Chỉ tạo 1 phiếu (nút khóa trong lúc lưu).'], 101)
S3.add('Tạo đồng thời ở 2 tab từ cùng kế hoạch', 'P1', [ACC_L, KH], ['Mở 2 tab màn Tạo, chọn KH1 ở cả 2.', 'Bấm Lưu ở tab 1 rồi tab 2.'],
       '—', ['Tab 1 lưu được, KH1 chuyển Đã lập phiếu kiểm kê.', 'Tab 2 báo "%s", không lưu.' % CONFLICT], 102)
S3.add('Chọn kế hoạch từ popup', 'P0', [ACC_L, KHT], TAO + ['Bấm ô Kế hoạch kiểm kê.', 'Bấm dòng TPE.KHTKK-00005.'], '—',
       ['Popup "Chọn kế hoạch kiểm kê hàng hóa" (dòng phụ "Kế hoạch kiểm kê theo hàng hóa đang kiểm và kế hoạch tổng kiểm kê đã duyệt"), '
        'ô Mã phiếu, Người tạo; cột STT, Mã phiếu, Người tạo, Ngày tạo.',
        'Chọn dòng: popup đóng, ô Kế hoạch = TPE.KHTKK-00005, Kho 3 kho và Công ty thuê kho khóa, vẫn có Thêm hàng hóa.'], [53, 274, 269])
S3.add('Chọn kế hoạch theo hàng hóa: khóa thêm / bớt hàng', 'P0', [ACC_L, KH], TAO + ['Bấm ô Kế hoạch kiểm kê, chọn KH1.'], '—',
       ['Nạp 2 hàng của KH1 theo tồn hiện tại + hội đồng của KH1.', 'Ẩn nút Thêm hàng hóa và cột xóa hàng; ĐVT kiểm kê vẫn đổi được.'], [53, 269])
S3.add('Chọn kế hoạch khi không có quyền lập phiếu', 'P0', [ACC_A, KHT], TAO + ['Bấm ô Kế hoạch kiểm kê, bấm dòng TPE.KHTKK-00005.'], '—',
       ['Popup vẫn liệt kê kế hoạch.', 'Bấm chọn báo "%s", form không đổi.' % PLAN404], [268, 295])
S3.add('Popup chọn kế hoạch: tìm và rỗng', 'P1', ACC_L, TAO + ['Bấm ô Kế hoạch kiểm kê.', 'Nhập mã "ABC", bấm Tìm kiếm.'], '—',
       ['Bảng hiện "Không có kế hoạch kiểm kê phù hợp.".'], [268, 40])
S3.add('Popup chọn kế hoạch: bấm mã mở tab mới', 'P2', [ACC_L, KHT], TAO + ['Bấm ô Kế hoạch.', 'Bấm mã TPE.KHTKK-00005 trong popup.'],
       '—', ['Mở chi tiết kế hoạch ở tab mới, popup vẫn mở, chưa chọn kế hoạch.'], 274)
S3.add('Bỏ kế hoạch đã chọn', 'P1', 'Đang ở màn Tạo, đã chọn TPE.KHTKK-00005.', ['Bấm × trong ô Kế hoạch kiểm kê.'], '—',
       ['Form về lập tay trống: Kho, Công ty thuê kho, Hàng hóa trống; Hội đồng 1 dòng trống.'], 98)
S3.add('Lưu phiếu lập từ Kế hoạch theo hàng hóa', 'P0', [ACC_L, KH], TAO + ['Chọn KH1.', 'Bấm Lưu.'], '—',
       [OK_LIST, 'KH1 ở màn Kế hoạch chuyển "Đã lập phiếu kiểm kê"; lịch sử KH1 có mốc ghi chú "Lập phiếu kiểm kê <số phiếu>.".'], [55, 281])
S3.add('Kế hoạch tổng: hàng đã có ở phiếu khác', 'P0', [ACC_L, KHT, 'Phiếu TPE.KKK-01096 lập từ kế hoạch tổng này đã có hàng H1.'],
       TAO + ['Chọn TPE.KHTKK-00005.', 'Thêm hàng H1, khai hội đồng.', 'Bấm Lưu.'], '—',
       ['Dòng H1 tô đỏ, dưới tên hàng "Hàng hóa đã lập phiếu kiểm kê.", báo "%s", không lưu.' % INVALID], [62, 75, 270])
S3.add('Thêm hàng khi chưa chọn kho', 'P0', PRE_FORM, TAO + ['Bấm Thêm hàng hóa.'], '—',
       ['Báo "Vui lòng chọn kho trước khi thêm hàng hóa.", ô Kho báo "Bắt buộc phải nhập".'], [61, 62])
S3.add('Popup Thêm hàng hóa chỉ hàng còn tồn', 'P0', PRE_FORM, TAO + ['Chọn Kho Hải Phòng.', 'Bấm Thêm hàng hóa.'], '—',
       ['Popup "Thêm hàng hóa" chỉ liệt kê hàng còn tồn ở kho Hải Phòng của công ty TPE / TPHP / TPV.'], [269, 53])
S3.add('Thêm hàng ra đúng vị trí, lô', 'P0', PRE_FORM, TAO + ['Chọn Kho Hải Phòng.', 'Thêm Mỡ bôi trơn L1.'], '—',
       ['Báo "Thêm thành công.".', 'Dòng: Tên hàng, Model "ANOPEC L1 15 KG", Mã hàng, ĐVT Xô 15KG, SL tồn kho 10, Vị trí "KHOANG6 (10)", Công ty '
        'TPHP, Lô, Tồn theo lô 10, ĐVT kiểm kê Xô 15KG.'], [58, 269])
S3.add('Thêm lại hàng đã có', 'P1', 'Đang ở màn Tạo, đã có Mỡ bôi trơn L1.', ['Bấm Thêm hàng hóa.'], '—',
       ['Mỡ bôi trơn L1 không chọn lại được trong popup; nếu chọn trùng thì báo "Hàng hóa đã được chọn.".'], [67, 62])
S3.add('Hàng hết tồn: cảnh báo vàng', 'P1', [PRE_FORM, 'Hàng H5 vừa xuất hết tồn sau khi mở popup.'], TAO + ['Thêm H5.'], '—',
       ['Cảnh báo vàng "Có 1 hàng hóa đã hết tồn trong kho đã chọn, không đưa vào phiếu: <mã H5>.", H5 không vào bảng.'], [268, 286])
S3.add('Làm mới số liệu', 'P1', 'Đang ở màn Tạo, có Mỡ bôi trơn L1 (tồn lô 10); kho vừa nhập thêm 2 vào lô đó.', ['Bấm Làm mới số liệu.'], '—',
       ['Báo "Làm mới số liệu thành công.", Tồn theo lô cập nhật 12.', 'Hàng đã hết tồn bị bỏ, báo "… Đã bỏ N hàng hóa hết tồn.".'], [286, 269])
S3.add('ĐVT kiểm kê: đổi sang đơn vị lớn tách dòng', 'P0', [PRE_FORM, 'Lô L1 của hàng H có SL 119 Cái; H có ĐVT Hộp 20 (hệ số 20).'],
       TAO + ['Thêm hàng H.', 'Đổi ĐVT kiểm kê của lô L1 sang Hộp 20.'], '—',
       ['Lô L1 thành 2 dòng: Hộp 20 SL 5, Cái SL 19 (5 × 20 + 19 = 119).'], [53, 283, 286])
S3.add('ĐVT kiểm kê: không đủ quy đổi', 'P0', [PRE_FORM, 'Lô L2 SL 7 Cái; hàng có ĐVT Hộp 20.'], TAO + ['Đổi ĐVT lô L2 sang Hộp 20.'], '—',
       ['Báo "Số lượng không đủ để quy đổi!", ô trở lại Cái, SL 7.'], [62, 283])
S3.add('ĐVT kiểm kê: bấm × để trống', 'P1', 'Đang ở màn Tạo, có hàng.', ['Bấm × ở ô ĐVT kiểm kê.', 'Bấm Lưu.'], '—',
       ['Ô trống; bảng vẫn cuộn được.', 'Báo "Bắt buộc phải nhập" ngay dưới ô ĐVT kiểm kê, không lưu.'], [61, 62])
S3.add('Đổi kho khi đã có hàng: Hủy', 'P0', 'Đang ở màn Tạo, đã thêm hàng ở kho Hải Phòng.', ['Đổi Kho = LN - Liên Ninh.', 'Bấm Hủy.'],
       '—', ['Hiện hộp "Đổi kho": "Đổi kho sẽ xóa danh sách hàng hóa đã chọn. Bạn có muốn tiếp tục?".',
             'Bấm Hủy: ô Kho vẫn là Hải Phòng, Công ty thuê kho và hàng giữ nguyên.'], 53)
S3.add('Đổi kho khi đã có hàng: Đồng ý', 'P1', 'Đang ở màn Tạo, đã thêm hàng ở kho Hải Phòng.', ['Đổi Kho = LN - Liên Ninh.', 'Bấm Đồng ý.'],
       '—', ['Danh sách hàng bị xóa; Công ty thuê kho tự chọn hết công ty của kho Liên Ninh.'], [53, 283])
S3.add('Đổi công ty thuê kho khi đã có hàng', 'P1', 'Đang ở màn Tạo, đã thêm hàng.', ['Bỏ TPV ở Công ty thuê kho.', 'Bấm Hủy.', 'Làm lại, bấm Đồng ý.'],
       '—', ['Hộp "Đổi công ty thuê kho": "Đổi công ty thuê kho sẽ xóa danh sách hàng hóa đã chọn. Bạn có muốn tiếp tục?".',
             'Hủy: giữ TPV; Đồng ý: bỏ TPV, xóa danh sách hàng.'], [53, 283])

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
PRE_E = [ACC_A, PH1]
EDIT = ['Đăng nhập A.', MENU, 'Ở dòng PH1 bấm Sửa (bút chì).']
S4.add('Mở màn Sửa', 'P0', PRE_E, EDIT, '—', ['Mở TRANG "Sửa phiếu kiểm kê theo hàng hóa: <số phiếu PH1>".'], 103)
S4.add('Dữ liệu điền đúng', 'P0', PRE_E, EDIT, '—',
       ['Ngày kiểm kê, Kho Hải Phòng, Công ty thuê kho, Ghi chú, bảng hàng + ĐVT kiểm kê (tồn hiện tại), hội đồng Bùi Duy Trước + chức vụ.'], 104)
S4.add('Trường được / không được sửa', 'P0', PRE_E, EDIT, '—',
       ['Không sửa được: Ngày kiểm kê, Kế hoạch kiểm kê (rê nhãn: "Kế hoạch kiểm kê chỉ chọn được lúc tạo phiếu, khi sửa phiếu '
        'giữ nguyên kế hoạch đã chọn.").', 'Sửa được: Kho, Công ty thuê kho, Ghi chú, hàng hóa, ĐVT kiểm kê, hội đồng.'], 105)
S4.add('Sửa phiếu lập từ kế hoạch theo hàng hóa', 'P1', [ACC_L, 'Phiếu PH5 Đang tạo do L lập từ KH1.'], ['Mở Sửa PH5.'], '—',
       ['Kế hoạch là liên kết mở tab mới; Kho và Công ty thuê kho khóa; không có Thêm hàng hóa, không có nút xóa hàng.'], 105)
S4.add('Hàng hết tồn khi mở Sửa', 'P1', [ACC_A, PH1, 'Mỡ bôi trơn L1 vừa xuất hết tồn.'], EDIT, '—',
       ['Cảnh báo vàng "Có 1 hàng hóa đã hết tồn trong kho đã chọn, không đưa vào phiếu: ANOP-ANOPECL115KG."; hàng không còn trong bảng.'], [104, 286])
S4.add('Các nút ở màn Sửa', 'P1', PRE_E, EDIT, '—', ['Có Lưu, Lưu và gửi, Quay lại; KHÔNG có Lưu và tiếp tục.'], 106)
S4.add('Sửa một trường', 'P0', PRE_E, EDIT + ['Đổi Ghi chú thành "Kiểm lại".', 'Bấm Lưu.'], 'Ghi chú: Kiểm lại',
       ['Báo "Lưu thành công.", về danh sách; trạng thái vẫn Đang tạo; Ngày kiểm kê = ngày lưu.'], [107, 69])
S4.add('Sửa nhiều trường', 'P0', PRE_E, EDIT + ['Thêm 1 hàng khác.', 'Thêm dòng hội đồng mới.', 'Bấm Lưu.'],
       '—', ['Lưu thành công; phiếu có 2 hàng và 2 thành viên hội đồng.'], [108, 110])
S4.add('Giữ nguyên giá trị khi lưu không đổi', 'P1', PRE_E, EDIT + ['Không đổi gì, bấm Lưu.'], '—', ['Lưu thành công, không báo trùng.'], [109, 68])
S4.add('Ngày / người cập nhật', 'P1', PRE_E, EDIT + ['Đổi Ghi chú, bấm Lưu.', 'Xem dòng PH1 ở danh sách.'], '—',
       ['Ngày cập nhật = thời điểm lưu, Người cập nhật = A.'], 111)
S4.add('Lịch sử sửa', 'P0', PRE_E, EDIT + ['Đổi Ghi chú, thêm hàng, bấm Lưu.', 'Mở Lịch sử của PH1.'], '—',
       ['Có mốc "Thay đổi thông tin", ghi Ghi chú cũ > mới và danh sách hàng thêm dòng.'], [112, 177, 178])
S4.add('Bỏ trống bắt buộc khi sửa', 'P0', PRE_E, EDIT + ['Bỏ chọn thành viên hội đồng.', 'Bấm Lưu.'], '—',
       ['"Bắt buộc phải nhập" dưới ô Thành viên, Chức vụ; báo "%s", không lưu.' % INVALID], [113, 117])
S4.add('Vượt giới hạn khi sửa', 'P2', PRE_E, EDIT + ['Dán 256 ký tự vào Ghi chú, bấm Lưu.'], '—',
       ['Báo "Vui lòng nhập tối đa 255 ký tự." dưới ô, không lưu.'], [114, 115])
S4.add('Trùng bản ghi khác khi sửa', 'P2', [ACC_A, PH1, 'Có phiếu khác cùng kho, cùng hàng.'], EDIT + ['Bấm Lưu.'], '—',
       ['Lưu được (phiếu không có trường duy nhất).'], 116)
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P1', 'Đang có lỗi "Bắt buộc phải nhập" ở ô Thành viên.', ['Chọn lại thành viên.'], '—', ['Lỗi biến mất ngay.'], 118)
S4.add('Mở Sửa rồi Quay lại không đổi', 'P1', PRE_E, EDIT + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], [119, 125])
S4.add('Đổi rồi trả về ban đầu', 'P2', PRE_E, EDIT + ['Sửa Ghi chú rồi gõ lại như cũ.', 'Bấm Quay lại.'], '—', ['Không hỏi "Thông tin chưa lưu".'], 120)
S4.add('Rời màn khi đã đổi', 'P0', PRE_E, EDIT + ['Đổi Ghi chú.', 'Bấm Quay lại.'], '—', ['Hiện hộp "Thông tin chưa lưu".'], 121)
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
       ['Không có nút Sửa, Xóa (phiếu đang ở bước duyệt).'], 129)

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
S5.add('Xóa phiếu lập từ kế hoạch không trả kế hoạch', 'P0', [ACC_L, 'Phiếu PH5 Đang tạo lập từ KH1 (KH1 Đã lập phiếu kiểm kê).'],
       ['Xóa PH5.', 'Mở màn Kế hoạch kiểm kê theo hàng hóa.'], '—',
       ['KH1 VẪN ở "Đã lập phiếu kiểm kê", không có lại nút Lập phiếu; popup Chọn kế hoạch không còn KH1.',
        'Lưu ý: giữ như hệ thống cũ (đã chốt) — nếu nghiệp vụ cần lập lại phiếu thì ghi nhận.'], [141, 281])
S5.add('Không xóa được phiếu đang dùng', 'P0', [ACC_A, PH2, PH3], ['Đăng nhập A.', MENU], '—',
       ['PH2, PH3 không có nút Xóa (đã gửi / đã nhập kết quả).'], [135, 137, 270])
S5.add('Xóa phiếu có dữ liệu con', 'P1', [ACC_A, PH1, 'PH1 có 3 hàng, 5 lô, 2 thành viên hội đồng.'], ['Xóa PH1.'], '—',
       ['Xóa thành công, toàn bộ hàng, lô, dòng ĐVT, hội đồng, kho, công ty thuê bị xóa theo.'], [136, 285])
S5.add('Phiếu đã bị xóa ở tab khác', 'P1', [ACC_A, PH1], ['Tab 2 xóa PH1.', 'Tab 1 xóa PH1.'], '—', ['Tab 1 báo "%s".' % NOTFOUND], 138)
S5.add('Phiếu vừa được gửi ở tab khác', 'P1', [ACC_A, PH1], ['Tab 2 gửi PH1.', 'Tab 1 bấm Xóa PH1, bấm Xóa.'], '—',
       ['Báo "%s", không xóa.' % CONFLICT], 138)
S5.add('Dữ liệu liên quan sau xóa', 'P1', [ACC_A, PH1, 'Vị trí V9 chỉ dùng ở PH1.'],
       ['Xóa PH1.', 'Vào danh mục Vị trí, xóa vị trí V9.'], '—', ['Vị trí xóa được (không còn phiếu nào dùng).'], [141, 280])

# ============================================================== VI. GỬI DUYỆT (Lưu và gửi + Cập nhật kết quả)
S6 = Sec(6)
S6.add('Nút Lưu và gửi', 'P0', PRE_FORM, TAO, '—', ['Nút Lưu và gửi (màu chính, biểu tượng máy bay giấy) ở chân màn Tạo và Sửa.'], 300)
S6.add('Lưu và gửi thành công', 'P0', PRE_FORM, FILL + ['Bấm Lưu và gửi.'], FULL,
       ['KHÔNG có hộp xác nhận; báo "Lưu và gửi thành công.", về danh sách.', 'Phiếu mới trạng thái Đang kiểm (nhãn xanh dương); dòng có Cập nhật kết quả.'],
       [86, 92, 301, 302, 305])
S6.add('Lưu và gửi khi thiếu bắt buộc', 'P0', PRE_FORM, TAO + ['Bấm Lưu và gửi.'], '—',
       ['Cùng bộ lỗi như Lưu, "%s", không lưu.' % INVALID], [87, 88, 303])
S6.add('Lưu và gửi trùng dữ liệu', 'P2', [PRE_FORM, PH2], FILL + ['Bấm Lưu và gửi.'], FULL, ['Lưu được, số phiếu khác PH2.'], 89)
S6.add('Gửi từ màn Sửa', 'P0', [ACC_A, PH1], ['Mở Sửa PH1.', 'Bấm Lưu và gửi.'], '—',
       ['Báo "Lưu và gửi thành công.", PH1 chuyển Đang kiểm; không còn Sửa, Xóa.'], [302, 305, 311])
S6.add('Màn sau khi gửi', 'P1', PRE_FORM, FILL + ['Bấm Lưu và gửi.'], FULL, ['Màn Tạo đóng, về danh sách.'], [90, 91, 92])
S6.add('Lịch sử khi gửi', 'P1', [ACC_A, PH1], ['Sửa PH1, bấm Lưu và gửi.', 'Mở Lịch sử PH1.'], '—',
       ['Có mốc "Thay đổi trạng thái" Đang tạo > Đang kiểm, người thực hiện A.'], [312, 92])
S6.add('Hàng bị khóa sau khi gửi', 'P0', [ACC_A, 'PH2 Đang kiểm có hàng Mỡ bôi trơn L1 ở kho Hải Phòng.'],
       ['Vào phân hệ Kho > Nhập kho > Phiếu nhập kho, lập phiếu nhập Mỡ bôi trơn L1 vào kho Hải Phòng, bấm lưu nhập kho.'], '—',
       ['Hệ thống chặn: "Hàng Mỡ bôi trơn L1 (15kg/xô) đang kiểm kho!".'], [307, 281])
S6.add('Cập nhật kết quả: mở bước nhập', 'P0', [ACC_A, PH2], ['Đăng nhập A.', MENU, 'Ở dòng PH2 bấm Cập nhật kết quả.'], '—',
       ['Mở chi tiết PH2; bảng Hàng hóa thêm cột Thực kiểm *, Chênh lệch, Ghi chú; Thực kiểm mặc định = SL.',
        'Có khối File đính kèm * (nút Thêm tài liệu), Hàng thừa khác * (nút Thêm dòng); chân màn có Gửi duyệt.'], [300, 51])
S6.add('Cập nhật kết quả: Chênh lệch tự tính', 'P0', [ACC_A, PH2], ['Mở Cập nhật kết quả PH2.', 'Đổi Thực kiểm dòng Mỡ bôi trơn L1 thành 9.'],
       'Thực kiểm: 9', ['Chênh lệch = -1, chữ đỏ.', 'Đổi lại 10: Chênh lệch 0, chữ thường.'], 306)
S6.add('Cập nhật kết quả: Thực kiểm trống / quá lớn', 'P0', [ACC_A, PH2],
       ['Xóa trống Thực kiểm 1 dòng, bấm Gửi duyệt.', 'Nhập 1000000000, bấm Gửi duyệt.'], '—',
       ['Bước 1: "Bắt buộc phải nhập" dưới ô, báo "Bạn chưa nhập đầy đủ thông tin.".', 'Bước 2: "Không hợp lệ".',
        'Ô chỉ nhận số, tối đa 2 chữ số thập phân; không gõ được dấu âm.'], [62, 303, 304])
S6.add('Cập nhật kết quả: Ghi chú dòng quá 255 ký tự', 'P2', [ACC_A, PH2], ['Nhập Ghi chú 256 ký tự, bấm Gửi duyệt.'], '—',
       ['Ô chỉ nhận 255 ký tự; nếu lọt thì báo "Vui lòng nhập tối đa 255 ký tự.", không lưu.'], 303)
S6.add('Cập nhật kết quả: thiếu file khi phiếu chưa có file', 'P0', [ACC_A, PH2], ['Nhập đủ Thực kiểm, không đính file.', 'Bấm Gửi duyệt.'], '—',
       ['Khối File đính kèm báo "Bắt buộc phải nhập", báo "Bạn chưa nhập đầy đủ thông tin.", không lưu.'], [303, 304])
S6.add('Cập nhật kết quả: file sai loại / quá dung lượng', 'P1', [ACC_A, PH2], ['Bấm Thêm tài liệu, chọn file .zip.', 'Chọn file .pdf 25MB.'], '—',
       ['Bước 1: "Chỉ nhận file pdf, png, jpg, jpeg, doc, docx, xls, xlsx".', 'Bước 2: "Dung lượng tối đa 20MB".'], 303)
S6.add('Hàng thừa khác: dòng mới thiếu thông tin', 'P0', [ACC_A, PH2], ['Bấm Thêm dòng ở khối Hàng thừa khác.', 'Bấm Gửi duyệt.'], '—',
       ['"Bắt buộc phải nhập" ở Tên hàng, ĐVT, Vị trí, Thực kiểm của dòng mới; không lưu.'], [303, 62])
S6.add('Hàng thừa khác: chọn hàng có mã', 'P1', [ACC_A, PH2], ['Bấm Thêm dòng, bấm kính lúp "Chọn hàng hóa có mã", chọn hàng H7.'], '—',
       ['Dòng điền Tên hàng, Model, Mã hàng, ĐVT cơ sở, SL tồn và các vị trí có tồn của H7; báo "Thêm thành công.".',
        'Chọn trùng hàng đã có ở dòng khác > "Hàng hóa đã được chọn.".'], [306, 67])
S6.add('Hàng thừa khác: nhiều vị trí', 'P2', [ACC_A, PH2], ['Ở dòng hàng mới, bấm + "Thêm vị trí".', 'Bấm thùng rác "Xóa vị trí" ở vị trí 2.'], '—',
       ['Bước 1: thêm 1 dòng vị trí con.', 'Bước 2: dòng vị trí 2 bị bỏ.'], 306)
S6.add('Gửi duyệt thành công', 'P0', [ACC_A, PH2, ACC_KT], ['Nhập Thực kiểm 9 + Ghi chú "Thiếu 1", đính 1 file pdf.', 'Bấm Gửi duyệt.'],
       ['Thực kiểm: 9', 'Ghi chú: Thiếu 1'],
       ['KHÔNG có hộp xác nhận; báo "Gửi duyệt thành công.", về danh sách.', 'PH2 chuyển Chờ KT duyệt; A không còn Cập nhật kết quả.'],
       [302, 305, 306])
S6.add('Thông báo đến Kế toán kho', 'P0', [ACC_A, PH2, ACC_KT, 'Tài khoản KT2 có quyền "%s" thuộc công ty TPSG.' % Q4],
       ['A Gửi duyệt PH2.'], '—',
       ['KT nhận thông báo "Chờ duyệt" của PH2 kèm Người nhập kết quả, Ngày kiểm kê, Kho.', 'KT2 (khác công ty) KHÔNG nhận.',
        'Bấm thông báo mở chi tiết PH2.'], [308, 309])
S6.add('Lịch sử khi Gửi duyệt', 'P1', [ACC_A, 'A vừa Gửi duyệt PH2.'], ['Mở Lịch sử PH2.'], '—',
       ['Mốc "Thay đổi thông tin": Kết quả kiểm kê (Thực kiểm, Chênh lệch cũ > mới), File đính kèm.',
        'Mốc "Thay đổi trạng thái" Đang kiểm > Chờ KT duyệt.'], [312, 183])
S6.add('Rời bước nhập kết quả chưa lưu', 'P1', [ACC_A, PH2], ['Đổi Thực kiểm 1 dòng.', 'Bấm Quay lại.', 'Bấm Thoát.'], '—',
       ['Hiện hộp "Thông tin chưa lưu"; Thoát > về danh sách, PH2 vẫn Đang kiểm, không có mốc lịch sử mới.'], 310)
S6.add('Không gửi lại phiếu đã gửi', 'P0', [ACC_A, PH3], [MENU, 'Quan sát dòng PH3.', 'Mở chi tiết PH3.'], '—',
       ['Không có Sửa, Lưu và gửi, Cập nhật kết quả, Gửi duyệt cho PH3.'], 311)
S6.add('Gửi duyệt khi phiếu vừa bị đổi', 'P1', [ACC_A, PH2], ['Tab 1, tab 2 mở Cập nhật kết quả PH2.', 'Tab 2 Gửi duyệt.', 'Tab 1 Gửi duyệt.'],
       '—', ['Tab 1 báo "%s", không ghi.' % CONFLICT], [311, 128])

# ============================================================== VII. DUYỆT PHIẾU (Duyệt kết quả + Xử lý)
S7 = Sec(7)
S7.add('Điều kiện hiện nút Duyệt kết quả', 'P0', [ACC_K, PH3, PH2], ['Đăng nhập K.', 'Mở chi tiết PH3.', 'Mở chi tiết PH2.'], '—',
       ['PH3: chân màn có Duyệt kết quả, Không duyệt đứng liền nhau.', 'PH2: không có 2 nút.', 'A (người tạo, không có quyền) mở PH3: không có 2 nút.'], 300)
S7.add('Giao diện popup Duyệt kết quả', 'P0', [ACC_K, PH3], ['Mở chi tiết PH3.', 'Bấm Duyệt kết quả.'], '—',
       ['Popup "Duyệt kết quả kiểm kê", dòng phụ "Phiếu: <số phiếu PH3>".', 'Ô Ghi chú duyệt (gợi ý "Nhập ghi chú duyệt"), không bắt buộc.',
        'Nút Duyệt kết quả, Hủy, (x).'], 301)
S7.add('Duyệt phiếu có chênh lệch', 'P0', [ACC_K, PH3, ACC_X], ['Bấm Duyệt kết quả, nhập "Đồng ý", bấm Duyệt kết quả.'], 'Ghi chú duyệt: Đồng ý',
       ['Báo "Duyệt thành công.", về danh sách.', 'PH3 chuyển Chờ xử lý; Người duyệt K, Ngày duyệt = thời điểm duyệt.'], [302, 305, 306])
S7.add('Duyệt phiếu không chênh lệch', 'P0', [ACC_K, PH3B], ['Duyệt PH3B, không nhập ghi chú.'], '—',
       ['PH3B chuyển Hoàn thành; không gửi thông báo cho người xử lý.'], [302, 304, 307])
S7.add('Không cần dữ liệu bắt buộc khi duyệt', 'P1', [ACC_K, PH3], ['Bấm Duyệt kết quả, để trống Ghi chú, bấm Duyệt kết quả.'], '—',
       ['Duyệt thành công (ghi chú không bắt buộc).', 'Ghi chú quá 5000 ký tự > "Vui lòng nhập tối đa 5000 ký tự.".'], 303)
S7.add('Thông báo đến người xử lý', 'P0', [ACC_K, PH3, ACC_X], ['K duyệt PH3 (có chênh lệch).'], '—',
       ['X nhận thông báo "Đã duyệt" kèm Người duyệt, "Có chênh lệch cần xử lý", Ngày kiểm kê, Kho, Ghi chú duyệt.'], 308)
S7.add('Bấm thông báo mở phiếu Chờ xử lý', 'P1', [ACC_X, 'X vừa nhận thông báo của PH3.'], ['Bấm thông báo.'], '—',
       ['Mở chi tiết PH3 dù X không có quyền xem theo cấp; có nút xử lý theo loại chênh lệch.'], 309)
S7.add('Hủy thao tác duyệt', 'P1', [ACC_K, PH3], ['Bấm Duyệt kết quả, nhập ghi chú.', 'Bấm Hủy.'], '—',
       ['Popup đóng; PH3 vẫn Chờ KT duyệt, Người duyệt trống.'], 310)
S7.add('Không duyệt lại phiếu đã xử lý', 'P0', [ACC_K, PH3], ['Tab 1, tab 2 mở chi tiết PH3.', 'Tab 2 duyệt.', 'Tab 1 bấm Duyệt kết quả trong popup.'],
       '—', ['Tab 1 báo "%s".' % CONFLICT, 'Phiếu Chờ xử lý / Hoàn thành không còn nút Duyệt kết quả.'], 311)
S7.add('Lịch sử duyệt', 'P0', [ACC_K, 'K vừa duyệt PH3 với ghi chú "Đồng ý".'], ['Mở Lịch sử PH3.'], '—',
       ['Mốc tiêu đề "Thay đổi trạng thái" màu cam, Người thực hiện K, "Trạng thái: Chờ KT duyệt > Chờ xử lý", ghi chú "Đồng ý".'], 312)
S7.add('Xử lý: nút theo loại chênh lệch', 'P0', [ACC_X, PH4, 'X có thêm quyền "%s".' % Q5], ['Mở chi tiết PH4.'], '—',
       ['Có Tạo phiếu nhập kho điều chuyển (H1 thừa) và Tạo phiếu xuất kho điều chuyển (H2 thiếu); không có Tạo phiếu điều chuyển vị trí.'], 306)
S7.add('Xử lý: thiếu quyền tạo phiếu nhập kho điều chỉnh', 'P1', [ACC_X, PH4], ['Mở chi tiết PH4 (X không có quyền "%s").' % Q5], '—',
       ['Chỉ còn Tạo phiếu xuất kho điều chuyển.'], [306, 295])
S7.add('Xử lý: Tạo phiếu xuất kho điều chuyển', 'P0', [ACC_X, PH4], ['Bấm Tạo phiếu xuất kho điều chuyển.'], '—',
       ['Mở màn tạo Phiếu xuất kho điều chỉnh kiểm kê đã nạp phiếu PH4 và dòng thiếu của H2.'], [307, 274])
S7.add('Xử lý: lưu phiếu xử lý chuyển Đang xử lý', 'P0', [ACC_X, PH4], ['Lưu phiếu xuất kho điều chỉnh vừa lập.', 'Mở lại PH4.'], '—',
       ['PH4 chuyển Đang xử lý; lịch sử có mốc "Thay đổi trạng thái" Chờ xử lý > Đang xử lý.', 'Nút Tạo phiếu xuất kho điều chuyển không còn.'],
       [305, 307, 281])
S7.add('Xử lý: Tạo phiếu điều chuyển vị trí', 'P1', [ACC_X, 'Phiếu PH6 Chờ xử lý: hàng H3 thiếu 2 ở vị trí V1, thừa 2 ở vị trí V2 (tổng 0).'],
       ['Mở chi tiết PH6.', 'Bấm Tạo phiếu điều chuyển vị trí.'], '—',
       ['Mở màn Tạo phiếu điều chuyển vị trí (phân hệ Kho) với kho đầu tiên của PH6 và dòng thiếu của H3.'], [307, 274])
S7.add('Xử lý: xử lý hết tự Hoàn thành', 'P0', [ACC_X, PH4], ['Hoàn tất phiếu nhập và phiếu xuất điều chỉnh cho đủ chênh lệch.', 'Mở danh sách.'],
       '—', ['PH4 tự chuyển Hoàn thành.'], [281, 307])
S7.add('Xử lý: thiếu quyền Xử lý', 'P1', [ACC_K, PH4], ['Đăng nhập K, mở chi tiết PH4.'], '—',
       ['Không có nút xử lý; dòng PH4 ở danh sách không có nút Xử lý.'], [304, 295])

# ============================================================== VIII. KHÔNG DUYỆT PHIẾU
S8 = Sec(8)
S8.add('Điều kiện hiện nút Không duyệt', 'P0', [ACC_K, PH3], ['Đăng nhập K, mở chi tiết PH3.', 'Đăng nhập A, mở chi tiết PH3.'], '—',
       ['K: có Không duyệt (nút đỏ, ngay sau Duyệt kết quả).', 'A: không có.'], 313)
S8.add('Giao diện popup Không duyệt', 'P0', [ACC_K, PH3], ['Bấm Không duyệt.'], '—',
       ['Popup "Không duyệt kết quả kiểm kê", dòng phụ "Phiếu: <số phiếu>".', 'Ô Ghi chú duyệt * (gợi ý "Nhập lý do không duyệt").',
        'Nút Không duyệt (đỏ), Hủy, (x).'], 314)
S8.add('Không duyệt thành công', 'P0', [ACC_K, PH3], ['Bấm Không duyệt, nhập "Đếm lại lô", bấm Không duyệt.'], 'Lý do: Đếm lại lô',
       ['Báo "Không duyệt thành công.", về danh sách.'], 315)
S8.add('Bỏ trống lý do', 'P0', [ACC_K, PH3], ['Bấm Không duyệt, để trống, bấm Không duyệt.'], '—',
       ['Ô viền đỏ "Vui lòng nhập lý do không duyệt", popup không đóng, phiếu không đổi.', 'Nhập chỉ khoảng trắng cũng báo như trên.'], 316)
S8.add('Lý do quá giới hạn', 'P2', [ACC_K, PH3], ['Nhập lý do 5001 ký tự, bấm Không duyệt.'], '—', ['Báo "Vui lòng nhập tối đa 5000 ký tự.".'], 317)
S8.add('Trạng thái sau không duyệt', 'P0', [ACC_K, PH3], ['Không duyệt PH3.', 'Đăng nhập A, mở PH3.'], '—',
       ['PH3 chuyển Không duyệt (nhãn đỏ); A thấy lại Cập nhật kết quả, Thực kiểm giữ giá trị đã nhập trước.'], [318, 320])
S8.add('Lý do được lưu', 'P1', [ACC_K, 'K vừa không duyệt PH3.'], ['Mở Lịch sử PH3.', 'In phiếu PH3.'], '—',
       ['Lịch sử: mốc "Từ chối", "Trạng thái: Chờ KT duyệt > Không duyệt", ghi chú lý do.', 'Bản in: mục "Nhận xét, đánh giá" là lý do.'],
       [319, 324])
S8.add('Thông báo đến người tạo', 'P0', [ACC_K, PH3], ['K không duyệt PH3.'], '—',
       ['A nhận thông báo "Từ chối" kèm Người từ chối, Lý do; bấm mở chi tiết PH3.'], 321)
S8.add('Hủy thao tác không duyệt', 'P1', [ACC_K, PH3], ['Bấm Không duyệt, nhập lý do, bấm Hủy.'], '—', ['PH3 vẫn Chờ KT duyệt.'], 322)
S8.add('Không duyệt phiếu đã đổi trạng thái', 'P1', [ACC_K, PH3], ['Tab 2 duyệt PH3.', 'Tab 1 bấm Không duyệt, nhập lý do, xác nhận.'], '—',
       ['Tab 1 báo "%s".' % CONFLICT], 323)
S8.add('Gửi duyệt lại sau không duyệt', 'P1', [ACC_A, 'PH3 vừa bị Không duyệt.'], ['A mở PH3, sửa Thực kiểm, bấm Gửi duyệt.'], '—',
       ['PH3 về Chờ KT duyệt; K nhận lại thông báo "Chờ duyệt".'], [318, 320])

# ============================================================== IX. LỊCH SỬ THAY ĐỔI
S9 = Sec(9)
PRE_H = [PRE_LIST, P89]
HIS = [MENU, 'Tìm TPE.KKK-01089, ở dòng đó bấm Lịch sử.']
S9.add('Mở cửa sổ lịch sử', 'P0', PRE_H, HIS, '—', ['Cửa sổ "Lịch sử thay đổi: TPE.KKK-01089".'], 162)
S9.add('Các thông tin của mốc', 'P0', PRE_H, HIS, '—',
       ['Mỗi mốc: thời điểm, hành động, "Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ", nội dung.'], [163, 165, 166, 167])
S9.add('Mới nhất trước', 'P0', PRE_H, HIS, '—',
       ['8 mốc; trên cùng 31/10/2026 09:22 "Thay đổi trạng thái" (Chờ xử lý > Hoàn thành, ghi chú "Phiếu điều chuyển vị trí PĐCVT-01232."), dưới cùng "Tạo mới".'], 164)
S9.add('Nội dung kết quả kiểm kê', 'P0', PRE_H, HIS, '—',
       ['Mốc "Thay đổi thông tin" liệt kê từng dòng hàng: "Thực kiểm: 141 > 142; Chênh lệch: 0 > 1".', 'Mốc "Từ chối" Chờ KT duyệt > Không duyệt.'], 168)
S9.add('Lọc theo hành động', 'P1', PRE_H, HIS + ['Bấm Bộ lọc, chọn Loại hành động = Tạo mới.'], '—', ['Chỉ còn mốc Tạo mới.'], 169)
S9.add('Lọc theo người thực hiện', 'P2', PRE_H, HIS + ['Bấm Bộ lọc, chọn Người thực hiện = DNS Admin.'], '—', ['Còn đủ 8 mốc.'], 170)
S9.add('Lọc theo thời gian', 'P1', PRE_H, HIS + ['Bấm Bộ lọc, Từ ngày 01/11/2026.'], '—', ['"Không có lịch sử phù hợp bộ lọc." (mọi mốc ngày 31/10/2026).'], [171, 173])
S9.add('Kết hợp lọc', 'P2', PRE_H, HIS + ['Chọn Loại hành động = Thay đổi trạng thái, Người thực hiện = DNS Admin.'], '—', ['Chỉ còn 4 mốc Thay đổi trạng thái.'], 172)
S9.add('Làm mới / đóng mở bộ lọc', 'P2', PRE_H, HIS + ['Lọc rồi bấm Làm mới.', 'Bấm Bộ lọc lần nữa.'], '—',
       ['Làm mới: hiện lại 8 mốc.', 'Bộ lọc thu gọn / mở lại.'], [174, 175])
S9.add('Phiếu chưa có lịch sử', 'P1', [PRE_LIST, 'TPE.KKK-00707 lập trên hệ thống cũ.'], [MENU, 'Mở Lịch sử TPE.KKK-00707 (ba chấm > Lịch sử).'],
       '—', ['"Chưa có lịch sử thao tác nào.".'], 162)
S9.add('Sửa không đổi gì thì không ghi', 'P1', [ACC_A, PH1], ['Sửa PH1, không đổi, bấm Lưu.', 'Mở Lịch sử.'], '—',
       ['Không có mốc "Thay đổi thông tin" mới.'], [182, 125])
S9.add('Đổi nhiều thông tin cùng lúc', 'P1', [ACC_A, PH1], ['Sửa PH1: đổi Ghi chú + hội đồng, bấm Lưu và gửi.', 'Mở Lịch sử.'], '—',
       ['1 mốc "Thay đổi thông tin" liệt kê Ghi chú, Hội đồng (cũ > mới) + 1 mốc "Thay đổi trạng thái".'], 183)
S9.add('Đóng cửa sổ', 'P1', PRE_H, HIS + ['Bấm Đóng.', 'Mở lại, bấm (x).'], '—', ['Cả 2 cách đều đóng cửa sổ.'], 184)
S9.add('Trạng thái danh sách sau khi đóng', 'P1', 'Đang ở trang 2, lọc Trạng thái = Hoàn thành.', ['Mở Lịch sử 1 dòng, bấm Đóng.'], '—',
       ['Danh sách giữ trang 2, bộ lọc, sắp xếp.'], 185)
S9.add('Lịch sử ở màn chi tiết', 'P1', PRE_H, DET('TPE.KKK-01089') + ['Ở khối Lịch sử bấm Xem lịch sử.'], '—',
       ['Khối Lịch sử có số 8; bấm mở rộng hiện 8 mốc; nút đổi thành Thu gọn.'], [195, 162])

# ============================================================== X. XEM CHI TIẾT
S10 = Sec(10)
PRE_D = [PRE_LIST, P85]
S10.add('Mở màn chi tiết', 'P0', PRE_D, DET('TPE.KKK-01085'), '—', ['Mở TRANG chi tiết (không phải cửa sổ nổi).'], 186)
S10.add('Tiêu đề', 'P1', PRE_D, DET('TPE.KKK-01085'), '—', ['"Chi tiết phiếu kiểm kê theo hàng hóa: TPE.KKK-01085", không kèm nhãn trạng thái.'], 187)
S10.add('Đầy đủ trường', 'P0', PRE_D, DET('TPE.KKK-01085'), '—',
       ['Thông tin chung: Kế hoạch kiểm kê (liên kết TPE.KHKKHH-00019), Ngày kiểm kê, Kho, Công ty thuê kho, Ghi chú; File đính kèm (1 file); '
        'Hàng hóa có Thực kiểm, Chênh lệch, Ghi chú; Hàng thừa khác ("Không có dữ liệu"); Hội đồng (Bùi Đức Thịnh); khối Lịch sử.'], 188)
S10.add('Khớp dữ liệu tạo và danh sách', 'P1', PRE_D, DET('TPE.KKK-01085'), '—',
       ['Kho Liên Ninh, Ngày kiểm kê 28/10/2026, người tạo DNS Admin khớp dòng ở danh sách.'], [189, 190])
S10.add('Trường chỉ đọc, không có nút Lưu', 'P0', PRE_D, DET('TPE.KKK-01085'), '—',
       ['Mọi ô khóa nền xám, Thực kiểm / Ghi chú là chữ; Chênh lệch khác 0 chữ đỏ.', 'Chân màn: In, Xuất Excel, Quay lại; không có Lưu.'], [191, 192])
S10.add('Nút theo trạng thái ở chi tiết', 'P0', [ACC_A, PH1, PH2], ['Mở chi tiết PH1.', 'Mở chi tiết PH2.'], '—',
       ['PH1: Sửa, Xóa, In, Xuất Excel, Quay lại.', 'PH2: Gửi duyệt, In, Xuất Excel, Quay lại.'], [193, 194])
S10.add('Phiếu chưa nhập kết quả', 'P2', [ACC_A, PH1], ['Mở chi tiết PH1.'], '—',
       ['Không có cột Thực kiểm / Chênh lệch / Ghi chú, không có khối File đính kèm và Hàng thừa khác.'], 188)
S10.add('Quay lại giữ trang và bộ lọc', 'P0', 'Đang ở trang 2, lọc Trạng thái = Hoàn thành.', ['Bấm số phiếu 1 dòng.', 'Bấm Quay lại.'], '—',
       ['Về danh sách giữ bộ lọc Trạng thái = Hoàn thành (trong 10 phút).'], [196, 197])
S10.add('Quay lại về đúng lối chờ duyệt', 'P1', [ACC_K, 'Có phiếu TPE.KKK-01097 Chờ KT duyệt.'], [MENU_TC, 'Bấm TPE.KKK-01097.', 'Bấm Quay lại.'], '—',
       ['Về danh sách "Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả", không về lối phân hệ Kho.'], [196, 1])
S10.add('Phiếu ngoài phạm vi', 'P0', [ACC_B, 'Phiếu TPSG.KKK-01057 Hoàn thành công ty TPSG.'], ['Đăng nhập B.', 'Mở đường link chi tiết phiếu đó.'],
       '—', ['Chuyển sang trang "Không tìm thấy trang".'], [186, 296])

# ============================================================== XI. IN PHIẾU
S11 = Sec(11)
S11.add('In phiếu từ danh sách', 'P0', PRE_D, [MENU, 'Bấm In ở dòng TPE.KKK-01085.'], '—',
       ['Cửa sổ "Xem trước phiếu kiểm kê theo hàng hóa TPE.KKK-01085".',
        'Bản in: letterhead công ty của phiếu, "PHIẾU KIỂM KÊ THEO MẶT HÀNG", Số phiếu, Ngày kiểm kê 28/10/2026, Kho vật lý Liên Ninh, Ghi chú.',
        'Bảng: STT, Tên hàng, Mã hàng, Vị trí, Công ty, Lô, SL tồn, ĐVT kiểm kê, Thực kiểm, Ghi chú; dòng Cộng; Nhận xét, đánh giá; khối ký '
        'Hội đồng kiểm kê / Trưởng bộ phận kho.'], 228)
S11.add('In phiếu từ màn chi tiết', 'P1', PRE_D, DET('TPE.KKK-01085') + ['Bấm In.'], '—', ['Cùng cửa sổ xem trước như in từ danh sách.'], 228)
S11.add('In phiếu chưa nhập kết quả', 'P2', [ACC_A, PH2], ['In PH2.'], '—', ['Cột Thực kiểm để trống.'], 228)
S11.add('Bấm In trong cửa sổ', 'P1', 'Đang mở cửa sổ xem trước.', ['Bấm In.'], '—', ['Mở hộp thoại in của trình duyệt.'], 228)
S11.add('In danh sách theo bộ lọc', 'P0', PRE_LIST, [MENU, 'Lọc Trạng thái = Chờ xử lý.', 'Bấm In danh sách.'], '—',
       ['Cửa sổ "Xem trước danh sách phiếu kiểm kê theo hàng hóa", tiêu đề "DANH SÁCH PHIẾU KIỂM KÊ THEO HÀNG HÓA".',
        'Bảng 4 dòng: STT, Số phiếu, Kế hoạch KK, Ngày kiểm kê (kèm giờ), Kho, Người tạo, Người duyệt, Ngày duyệt, Trạng thái; khối ký Người lập = người in.'],
       [220, 227])
S11.add('In danh sách vượt mức in tối đa', 'P2', 'Bộ lọc ra hơn 2.000 phiếu (vượt mức in tối đa 2.000 dòng).', ['Bấm In danh sách.'], '—',
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
S12.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', 'Đang lọc Trạng thái = Hoàn thành (879).', ['Ẩn cột Trạng thái, bấm Lưu.'], '—',
       ['Vẫn 879 phiếu, bộ lọc giữ nguyên.'], [210, 211])

# ============================================================== XIII. XUẤT DANH SÁCH EXCEL
S13 = Sec(13)
S13.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất Excel" với 11 trường: Số phiếu, Kế hoạch kiểm kê, Ngày kiểm kê, Kho, Trạng thái, Người tạo, Ngày tạo, '
        'Người duyệt, Ngày duyệt, Ngày cập nhật, Người cập nhật.', 'Trường tích sẵn theo cột đang hiện trên bảng (13/13 cột đang hiện > đủ 11/11 trường).',
        'Lưu ý: hiện "Người duyệt" không được tích sẵn ("Đang chọn 10/11 trường") — nếu vẫn vậy thì ghi nhận lỗi.'], [212, 213, 214])
S13.add('Xuất trường mặc định', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel, bấm Xuất file.'], '—',
       ['Tải "danh_sach_phieu_kiem_ke_theo_hang_hoa.xlsx", báo "Xuất Excel thành công.".',
        'File: letterhead, "DANH SÁCH PHIẾU KIỂM KÊ THEO HÀNG HÓA", cột STT + trường đã tích (tiêu đề cột không tô nền), 898 dòng, khối ký.'],
       [215, 223, 224, 225, 227])
S13.add('Xuất tất cả trường', 'P1', PRE_LIST, ['Bấm Xuất Excel, Chọn tất cả, Xuất file.'], '—', ['File có STT + 11 cột.'], 216)
S13.add('Xuất một số trường theo thứ tự kéo', 'P1', PRE_LIST, ['Bỏ chọn hết, tích Kho rồi Số phiếu, kéo Kho lên đầu, Xuất file.'], '—',
       ['File chỉ có STT, Kho, Số phiếu theo đúng thứ tự.'], [217, 226])
S13.add('Không chọn trường', 'P1', PRE_LIST, ['Bấm Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S13.add('Xuất theo tìm kiếm / bộ lọc', 'P0', PRE_LIST, ['Lọc Ngày tạo 31/10/2026 – 31/10/2026.', 'Xuất file.'],
       '—', ['File chỉ có 4 phiếu TPE.KKK-01092, 01091, 01090, 01089; có dòng thời gian "Từ ngày 31/10/2026 đến ngày 31/10/2026".'], [219, 220])
S13.add('Xuất nhiều trang', 'P1', PRE_LIST, ['Đang ở trang 1 (10 dòng), Xuất file.'], '—', ['File có đủ 898 dòng.'], 221)
S13.add('Danh sách rỗng', 'P2', 'Bộ lọc không ra phiếu nào.', ['Xuất file.'], '—', ['Vẫn ra file có tiêu đề, dòng tên cột, khối ký.'], 222)
S13.add('Dữ liệu khớp, định dạng ngày và tiếng Việt', 'P1', PRE_D, ['Xuất file, mở dòng TPE.KKK-01085.'], '—',
       ['Ngày kiểm kê "28/10/2026", Ngày tạo "28/10/2026 10:39", Ngày duyệt "28/10/2026 10:39" (kèm giờ); Kho "Liên Ninh", Trạng thái "Hoàn thành" đủ dấu.'],
       [228, 229, 230])
S13.add('Xuất Excel 1 phiếu', 'P0', PRE_D, [MENU, 'Ở dòng TPE.KKK-01085 bấm Xuất Excel.'], '—',
       ['Tải "phieu_kiem_ke_theo_mat_hang_TPE.KKK-01085.xlsx", báo "Xuất Excel thành công.".',
        'File: letterhead công ty của phiếu, "PHIẾU KIỂM KÊ THEO MẶT HÀNG", Số phiếu, Ngày kiểm kê, Kho vật lý, Ghi chú, bảng chi tiết (số là ô số), '
        '"Nhận xét, đánh giá:", khối ký Hội đồng kiểm kê / Trưởng bộ phận kho.'], [223, 228, 293])

# ============================================================== XIV. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S14 = Sec(14)
S14.add('Kế hoạch hiện ở popup Chọn kế hoạch', 'P0', [ACC_L, KH, KHT, 'Kế hoạch KH2 Đã lập phiếu kiểm kê; kế hoạch tổng KHT2 Đã duyệt nhưng đã hết kỳ.'],
       TAO + ['Bấm ô Kế hoạch kiểm kê.'], '—', ['Popup có KH1 và TPE.KHTKK-00005; không có KH2, KHT2, kế hoạch Đang tạo.'], [274, 276])
S14.add('Bộ lọc màn liên quan cập nhật', 'P2', [ACC_L, KH], ['Lập và lưu phiếu từ KH1.', 'Mở lại popup Chọn kế hoạch.'], '—',
       ['KH1 không còn trong popup.'], 282)
S14.add('Trạng thái kế hoạch đổi theo phiếu', 'P0', [ACC_L, KH], ['Lập phiếu từ KH1, chỉ bấm Lưu.', 'Mở màn Kế hoạch kiểm kê theo hàng hóa.'], '—',
       ['KH1 chuyển Đã lập phiếu kiểm kê (dù phiếu mới Đang tạo); lịch sử KH1 có mốc Thay đổi trạng thái kèm mã phiếu.'], [281, 284])
S14.add('Phiếu nhập kho chặn hàng đang kiểm', 'P0', [ACC_A, 'PH2 Đang kiểm có Mỡ bôi trơn L1 ở kho Hải Phòng.'],
       ['Vào phân hệ Kho > Nhập kho > Phiếu nhập kho, lập phiếu nhập Mỡ bôi trơn L1 vào kho Hải Phòng, bấm lưu nhập kho.'], '—',
       ['Hệ thống chặn: "Hàng Mỡ bôi trơn L1 (15kg/xô) đang kiểm kho!".', 'Khi PH2 đã Chờ xử lý / Hoàn thành thì không còn chặn.'], [281, 307])
S14.add('Phiếu điều chuyển hàng chặn hàng đang kiểm', 'P1', [ACC_A, 'PH3 Chờ KT duyệt có Mỡ bôi trơn L1 ở kho Hải Phòng.'],
       ['Vào phân hệ Tài chính > menu "Điều chuyển" > bấm "Phiếu điều chuyển hàng".', 'Lập phiếu điều chuyển Mỡ bôi trơn L1 từ kho Hải Phòng, bấm lưu.'], '—',
       ['Báo "Hàng hóa đang được kiểm kho, không thể điều chuyển" tại dòng hàng.'], [281, 307])
S14.add('Phiếu xuất kho điều chỉnh đọc dòng thiếu', 'P0', [ACC_X, PH4], ['Bấm Tạo phiếu xuất kho điều chuyển ở PH4.'], '—',
       ['Màn tạo nạp đúng dòng thiếu của H2 (SL = |chênh lệch| trừ phần đã xử lý); liên kết về PH4.'], [274, 272])
S14.add('Báo cáo hàng thừa thiếu đọc phiếu Hoàn thành', 'P1', [ACC_T, 'Phiếu PH7 Hoàn thành lập từ kế hoạch tổng, hàng H1 chênh +2.'],
       ['Vào phân hệ Kho > Báo cáo kho > Báo cáo hàng thừa thiếu sau tổng kiểm kê hàng hóa, chọn kỳ chứa ngày kiểm kê của PH7.'], '—',
       ['Báo cáo có H1 SL thừa 2 của PH7; phiếu chưa Hoàn thành không được tính.'], [272, 284])
S14.add('Biên bản xử lý thừa thiếu đọc phiếu', 'P1', [ACC_T, 'Phiếu PH7 Hoàn thành ở kho Hải Phòng.'],
       ['Vào phân hệ Tài chính > Kiểm kê > Biên bản xử lý hàng thừa, thiếu sau kiểm kê, tạo biên bản kho Hải Phòng.'], '—',
       ['Danh sách nguồn có PH7 với chênh lệch theo hàng; mã phiếu liên kết về chi tiết PH7.'], [272, 274])
S14.add('Không xóa được danh mục kho đang dùng', 'P0', [ACC_A, PH2], ['Vào phân hệ Kho > Danh mục > Vị trí, xóa vị trí KHOANG6.'], '—',
       ['Hệ thống chặn xóa vì vị trí đang được dùng.', 'Tương tự với Kho vật lý Hải Phòng.'], 270)
S14.add('Đổi tên danh mục không đổi phiếu', 'P1', [ACC_A, PH2], ['Đổi tên hàng Mỡ bôi trơn L1 ở danh mục.', 'Mở chi tiết PH2.'], '—',
       ['Bảng Hàng hóa vẫn ghi tên hàng như lúc thêm.'], [272, 278, 279])
S14.add('Số tồn là ảnh chụp', 'P1', [ACC_A, PH2], ['Nhập thêm 5 Mỡ bôi trơn L1 vào kho Hải Phòng (sau khi PH2 Hoàn thành).', 'Mở chi tiết PH2.'], '—',
       ['Tồn theo lô trên PH2 vẫn 10.'], [286, 269])
S14.add('Tồn kho không đổi khi duyệt', 'P0', [ACC_K, PH3], ['Ghi tồn Mỡ bôi trơn L1.', 'Duyệt PH3.', 'Xem lại tồn.'], '—',
       ['Tồn không đổi (chỉ phiếu xử lý mới ghi tồn).'], 286)
S14.add('Kho đã khóa không chọn được khi tạo', 'P1', [PRE_FORM, 'Kho Sơn La đã khóa ở danh mục Kho vật lý.'],
       TAO + ['Mở ô Kho.'], '—', ['Không có kho Sơn La để chọn.'], [276, 284])

# ============================================================== XV. PHÂN QUYỀN (cuối)
S15 = Sec(15)
S15.add('Quyền tổng công ty: xem mọi phiếu', 'P0', [ACC_T, 'Có 898 phiếu không Đang tạo thuộc TPE, TPSG, TPV, TPHP.'], ['Đăng nhập T.', MENU], '—',
       ['Thấy đủ 898 phiếu.'], [287, 299])
S15.add('Quyền công ty: chỉ công ty mình + của mình', 'P0', [ACC_C, 'Phiếu công ty TPE là N1, các công ty khác N2.'], ['Đăng nhập C.', MENU], '—',
       ['Chỉ thấy N1 phiếu TPE và phiếu C tự tạo; không thấy phiếu TPSG.'], [287, 299])
S15.add('Không quyền: chỉ phiếu mình tạo', 'P0', [ACC_A, 'A tạo 3 phiếu.'], ['Đăng nhập A.', MENU], '—', ['Chỉ thấy 3 phiếu của A.'], [287, 299])
S15.add('Quyền theo công ty đang đăng nhập', 'P1', ['Tài khoản M có quyền "%s" ở công ty TPSG, đang đăng nhập công ty TPE.' % V1], ['Đăng nhập M (TPE).', MENU],
       '—', ['M chỉ thấy phiếu mình tạo (quyền ở TPSG không áp khi đang ở TPE).'], [287, 299])
S15.add('Đang tạo chỉ người tạo thấy', 'P0', [ACC_T, PH1], ['Đăng nhập T.', MENU, 'Tìm số phiếu PH1.'], '—', ['T không thấy PH1.'], [287, 299])
S15.add('Xem chi tiết theo phạm vi', 'P0', [ACC_C, 'Phiếu TPSG.KKK-01057 công ty TPSG.'], ['Đăng nhập C.', 'Mở đường link chi tiết phiếu đó.'], '—',
       ['Trang "Không tìm thấy trang".'], [288, 296])
S15.add('Ban kiểm soát / người xử lý mở phiếu đang chờ mình', 'P0', [ACC_K, ACC_X, PH3, PH4], ['K mở chi tiết PH3.', 'X mở chi tiết PH4.'], '—',
       ['Cả 2 mở được dù không có quyền xem theo cấp; sau khi phiếu đổi trạng thái (Hoàn thành) thì mở lại ra "Không tìm thấy trang".'], 288)
S15.add('Thêm mới không cần quyền', 'P0', [ACC_A, ACC_B], ['Đăng nhập B, mở danh sách, bấm Tạo mới, lập tay và Lưu.'], '—',
       ['B có nút Tạo mới và lưu được phiếu lập tay.'], [289, 295])
S15.add('Lập từ kế hoạch cần quyền Lập phiếu', 'P0', [ACC_A, ACC_L, KH], ['A mở đường link màn Tạo từ KH1.', 'L bấm Lập phiếu ở KH1.'], '—',
       ['A: chuyển trang "Không tìm thấy trang".', 'L: màn Tạo nạp sẵn KH1.'], [289, 295, 296])
S15.add('Sửa / Cập nhật kết quả chỉ người tạo', 'P0', [ACC_T, PH2, 'PH5 Đang tạo do T tạo.'], ['Đăng nhập T.', MENU], '—',
       ['PH5 có Sửa; PH2 (A tạo) không có Cập nhật kết quả dù T thấy được.'], [290, 295])
S15.add('Xóa chỉ người tạo', 'P0', [ACC_T, 'PH5 Đang tạo do T tạo.'], ['Đăng nhập T.', MENU], '—', ['Chỉ PH5 có nút Xóa.'], [291, 295])
S15.add('Duyệt / Không duyệt cần quyền Ban kiểm soát', 'P0', [ACC_T, PH3], ['Đăng nhập T, mở chi tiết PH3.'], '—',
       ['T (chỉ có quyền xem) không có Duyệt kết quả, Không duyệt; dòng PH3 không có nút Duyệt.'], 295)
S15.add('Xử lý cần quyền Xử lý', 'P0', [ACC_K, PH4], ['Đăng nhập K (có thêm quyền xem tổng công ty), mở chi tiết PH4.'], '—',
       ['Không có nút Tạo phiếu điều chuyển vị trí / nhập kho / xuất kho điều chuyển.'], 295)
S15.add('Thông báo Chờ duyệt theo quyền Kế toán kho', 'P1', [ACC_KT, ACC_K, PH2], ['A Gửi duyệt PH2.'], '—',
       ['KT nhận thông báo; K (không có quyền Kế toán kho) không nhận.'], [295, 308])
S15.add('Xuất / In / Lịch sử theo phạm vi', 'P1', ACC_A, ['Đăng nhập A.', MENU, 'Xuất Excel; mở Lịch sử 1 phiếu của A.'], '—',
       ['File chỉ chứa phiếu của A; lịch sử xem được.'], [293, 294])
S15.add('Mở đường link màn Sửa khi không phải người tạo', 'P0', [ACC_C, 'Phiếu PH6 Đang kiểm công ty TPE do A tạo.'],
       ['Đăng nhập C.', 'Mở đường link màn Sửa của PH6.'], '—', ['Tự chuyển sang màn chi tiết PH6, không sửa được.'], 296)
S15.add('Thao tác bị chặn lại ở máy chủ', 'P1', [ACC_A, PH1], ['Tab 1 mở danh sách.', 'Tab 2 gửi PH1.', 'Tab 1 bấm Xóa PH1, xác nhận.'], '—',
       ['Báo "%s"; máy chủ kiểm lại điều kiện từng thao tác, không dựa vào việc ẩn nút.' % CONFLICT], 297)
S15.add('Đổi quyền giữa thao tác', 'P1', [ACC_K, PH3, 'Quản trị gỡ quyền "%s" của K khi K đang mở chi tiết PH3.' % Q2],
       ['K bấm Duyệt kết quả, xác nhận.'], '—', ['Báo "%s" (hoặc không tìm thấy phiếu nếu K hết phạm vi xem), PH3 không đổi.' % NOPERM], 298)
S15.add('Super admin', 'P2', 'Tài khoản DNS Admin (Super admin), vai trò có các quyền của màn ở công ty đang đăng nhập.', ['Đăng nhập DNS Admin.', MENU], '—',
       ['Thấy 898 phiếu mọi công ty, có Tạo mới, lối chờ duyệt thấy TPE.KKK-01097.',
        'Lập phiếu từ kế hoạch được miễn kiểm quyền Lập phiếu.'], 287)

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
    build_chuan(output_file=OUT, sheet_name='Trang tính1', feature_name='Kiểm kê theo hàng hóa - Cập nhật ngày 06/11/2026',
                module_name='Kiểm kê theo hàng hóa', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

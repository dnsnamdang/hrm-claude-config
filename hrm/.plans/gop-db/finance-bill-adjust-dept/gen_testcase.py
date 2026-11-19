# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu kế toán" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu').
Bản đầu 04/11/2026 (khuôn cũ tc_engine.build); làm lại theo chuẩn mới cùng ngày 04/11/2026.

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Nhóm theo đúng tên + thứ tự chuẩn loại 'phieu' (check_tc.THU_TU), bỏ nhóm màn không có (Khóa / Mở khóa, Gửi duyệt,
Không duyệt phiếu, Hủy phiếu, Import): I Hiển thị trang & truy cập · II Tìm kiếm & lọc danh sách · III Thêm mới (gồm cả các
cửa sổ chọn Phiếu yêu cầu / Đối tượng / Hợp đồng / Phiếu yêu cầu xuất hàng trên form) · IV Chỉnh sửa · V Xóa · VI Duyệt phiếu
(luồng Lưu và duyệt ghi sổ cái) · VII Lịch sử thay đổi · VIII Xem chi tiết phiếu kế toán · IX In phiếu · X Tùy chỉnh cột ·
XI Xuất danh sách Excel (kèm Xuất Excel 1 phiếu) · XII Ràng buộc với các chức năng khác · XIII Phân quyền (cuối).
Cài đặt bộ lọc nằm trong nhóm Tìm kiếm & lọc. Mỗi case ghi kèm stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK
để dựng bảng đối chiếu theo assets/CHECKLIST_TC_SRS.xlsx.
Khuôn cấu trúc: ../buy-service-accounting/gen_testcase.py (màn Lưu nháp / Lưu và duyệt ghi sổ gần nhất về nghiệp vụ).
Nguồn hành vi (đọc 04/11/2026, nhánh develop cả 2 repo): FE pages/finance/bill-adjust-depts/** (index, create, _id/index, _id/edit,
  components/{BillAdjustDeptForm, AccountingDetailTable, BillAdjustDeptRequestPickerModal, ObjectSearchModal, ContractPickerModal,
  ExportRequestSearchModal}); BE Modules/Finance BillAdjustDept (searchByFilter / canView / canEdit), BillAdjustDept{Write,Source,
  Notify,History,Picker,OddBalance,Print}Service, BillAdjustDeptStoreRequest, BillAdjustDeptController, Routes/api.php.
Số liệu mẫu lấy từ dev-hrm 04/11/2026 (DNS Admin): 15.410 phiếu, TPE.PKT1126.00001 Đang tạo (EURO), TPE.PKT1026.00458 Đã duyệt.
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
from tc_phieu_bosung import (ListScreen, open_menu_case, filter_memory_cases, combo_cases, org_cases,  # noqa: E402
                             check_no_dash_pre)

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Tài chính > menu "Sổ tổng hợp" > nhóm "Sổ tổng hợp" > bấm "Phiếu kế toán".'
TAO = [MENU, 'Bấm "Tạo mới".']
ADV = 'Bấm Tìm kiếm nâng cao.'
YC_MENU = 'Vào phân hệ Tài chính > menu "Khởi tạo" > nhóm "Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi" > bấm "Phiếu yêu cầu điều chỉnh công nợ".'
HT_MENU = ('Vào phân hệ Tài chính > menu "Khởi tạo" > nhóm "Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi" > bấm "Phiếu yêu cầu hạch toán '
           'bổ sung".')

ACC_K = 'Tài khoản K: có quyền Kế toán thanh toán, thuộc công ty 1, không có quyền xem theo cấp.'
ACC_K2 = 'Tài khoản K2: có quyền Kế toán thanh toán, thuộc công ty 1 (kế toán khác).'
ACC_B = 'Tài khoản B: nhân viên công ty 1, không có quyền nào của màn.'
ACC_C = 'Tài khoản C: có quyền Xem tất cả phiếu kế toán của tổng công ty.'
ACC_D = 'Tài khoản D: có quyền Xem tất cả phiếu kế toán của công ty, thuộc công ty 1.'
PRE_LIST = ('Tài khoản DNS Admin (Super admin, có quyền Kế toán thanh toán); trong phạm vi xem có 15.410 phiếu (15.409 Đã duyệt, 1 '
            'Đang tạo của DNS Admin).')
YCDC = ('Phiếu yêu cầu điều chỉnh công nợ TPE.DNDCCN1026.00401 Chờ tạo phiếu kế toán, khách hàng 38THAPTR-15, 2 dòng, mỗi dòng có '
        'số tiền 779,760.')
HTBS = 'Phiếu yêu cầu hạch toán bổ sung PYCHTBS-002288 Chờ duyệt, Điều chỉnh công nợ khách hàng 43TPHPHO-129, 567,000 VNĐ.'
DRAFT_K = ('K có phiếu TPE.PKT1126.00001 Đang tạo, nhập tay, Loại tiền EURO, Tỷ giá 29,569.91, 2 dòng nhóm 1: TK 35241 Nợ 3,100 '
           '(91,666,721 VNĐ) và TK 811 Có 3,100, đối tượng 29TPHXNA-2.')
DONE = ('Phiếu TPE.PKT1026.00458 Đã duyệt, lập từ PYCHTBS-002289, Tổng phát sinh 6,594,953, 2 dòng (111 Có, 112 Nợ), 2 mốc lịch '
        'sử (Tạo mới, Thay đổi trạng thái).')
PRE_FORM = ACC_K + '\n' + YCDC + '\nTrên máy có file chungtu.pdf (1MB).'
FULL = ['Ngày hạch toán: hôm nay', 'Loại tiền: VNĐ', 'Diễn giải: Điều chỉnh công nợ T11',
        'Dòng 1: TK 1311, KH 38THAPTR-15, Nợ 1,000,000, Diễn giải "Nợ KH"',
        'Dòng 2: TK 3311, KH 38THAPTR-15, Có 1,000,000, Diễn giải "Có KH"']
TAO_FULL = TAO + ['Nhập Diễn giải "Điều chỉnh công nợ T11".', 'Bấm Thêm dòng 2 lần, nhập 2 dòng như Test Data.']

CK = defaultdict(list)       # stt checklist Testcase -> [TC ID]


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
     'Màn Phiếu kế toán dùng để kế toán ghi bút toán Nợ / Có vào sổ cái theo nhóm định khoản.\n'
     'Phiếu lập tay hoặc lập từ phiếu nguồn (Phiếu yêu cầu điều chỉnh công nợ, Phiếu yêu cầu hạch toán bổ sung, Danh sách cần hạch toán '
     'chi phí vận chuyển nhanh). Lưu nháp tạo phiếu Đang tạo; Lưu và duyệt kiểm tra cân đối từng nhóm, đề xuất điều chỉnh số dư lẻ, '
     'ghi sổ cái và chuyển phiếu nguồn sang Đã duyệt.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Trạng thái: Đang tạo (xám), Đã duyệt (xanh).\n'
     '- Danh sách: phiếu trong phạm vi quyền xem; không có quyền xem thì chỉ phiếu mình tạo.\n'
     '- Đối tượng của dòng định khoản: Khách hàng, Nhà cung cấp, Nhân viên.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác: luôn ẩn ở mọi cấp quyền.\n'
     '- Không có Khóa / Mở khóa, Import Excel, Không duyệt, Hủy (trả phiếu về làm ở màn phiếu nguồn).'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo ngày tạo phiếu, lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Phiếu > nhóm định khoản > dòng định khoản > đối tượng > hợp đồng > phiếu yêu cầu xuất hàng.\n'
     '- Phiếu > file đính kèm; phiếu Đã duyệt > bút toán sổ cái.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Dòng Tổng = tổng Phát sinh nợ / tổng Phát sinh có; ngoại tệ có thêm tổng quy đổi VNĐ = nguyên tệ × Tỷ giá.\n'
     '- Khi duyệt: trong mỗi nhóm Tổng Nợ = Tổng Có, không trùng cặp tài khoản + đối tượng + hợp đồng.\n'
     '- Một Phiếu yêu cầu hạch toán bổ sung chỉ có 1 phiếu kế toán còn hiệu lực.'),
    ('7. Phân quyền cấp',
     '- Xem tất cả phiếu kế toán của tổng công ty / Xem tất cả phiếu kế toán của công ty.\n'
     '- Kế toán thanh toán: nút Tạo mới, Lưu nháp, Lưu và duyệt, sửa / xóa (sửa / xóa thêm điều kiện người tạo + Đang tạo).\n'
     '- In, Xuất Excel, Lịch sử không gắn quyền riêng.'),
    ('8. Cách tính các ô thống kê',
     '- Cột Tổng phát sinh = tổng quy đổi VNĐ của phiếu.\n'
     '- Dòng "Hiển thị a–b / N": a–b là khoảng số thứ tự trang đang xem, N là tổng phiếu khớp bộ lọc trong phạm vi quyền.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: K, K2 (Kế toán thanh toán, công ty 1), B (không quyền), C (xem tổng công ty), D (xem công ty 1), '
     'DNS Admin (Super admin).\n'
     '- Số tiền hiển thị dạng 1,234,567 (dấu phẩy ngăn nghìn).\n'
     '- Lưu ý: Lưu nháp chỉ bắt buộc Ngày hạch toán; Lưu và duyệt mới kiểm tra đủ, hỏi xác nhận và GHI SỔ CÁI (không hoàn tác).\n'
     '- Lưu ý: Màn Tạo / Sửa / Chi tiết là TRANG riêng, không phải cửa sổ nổi.\n'
     '- Lưu ý: chạy case Lưu và duyệt trên phiếu thử, ghi sổ thật không đảo được.'),
]

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
SCREEN = ListScreen(menu=MENU, title='Phiếu kế toán', total=15410, quick_label='mã phiếu', quick_sample='PKT1026.00458',
                    quick_hit='phiếu TPE.PKT1026.00458', filters=[('Trạng thái', 'Đã duyệt'), ('Người tạo', 'DNS Admin')])
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Tiêu đề màn hình', 'P0', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Cả 3 nơi đều là "Phiếu kế toán".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', [ACC_K], ['Đăng nhập K.', MENU, 'Quan sát khối bộ lọc và thanh công cụ của bảng.'], '—',
       ['Khối bộ lọc: ô tìm nhanh (gợi ý "Tìm theo mã phiếu..."), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
        'Thanh công cụ: Tạo mới, Xuất Excel, nút biểu tượng cột.', 'Không có nút Import, Khóa, In danh sách.'], 3)
S1.add('Nút Tạo mới ẩn khi không có quyền Kế toán thanh toán', 'P0', [ACC_B], ['Đăng nhập B.', MENU], '—',
       ['Không có nút Tạo mới; vẫn có Xuất Excel, nút biểu tượng cột.'], [3, 295])
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột từ trái sang phải.'],
       '—', ['Đúng 14 cột: STT, Mã phiếu, Mã phiếu YCĐC, Tổng phát sinh, Diễn giải, Ngày hạch toán, Ngày tạo, Người tạo, Ngày cập nhật, '
             'Người cập nhật, Phòng ban, Loại tiền, Trạng thái, Hành động.', 'STT và Mã phiếu ghim trái khi cuộn ngang.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 14/14 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp phiếu đã tạo', 'P0', [PRE_LIST, DONE], [MENU, 'Tìm "PKT1026.00458", đối chiếu dòng.'], '—',
       ['Mã phiếu YCĐC "PYCHTBS-002289" (link); Tổng phát sinh "6,594,953" căn phải; Loại tiền VNĐ; Người tạo DNS Admin; '
        'Ngày tạo 30/10/2026 15:27.', 'Ngày hạch toán dạng dd/mm/yyyy 00:00.', 'Trạng thái nhãn xanh "Đã duyệt".'], 6)
S1.add('Cột Phòng ban lấy theo phiếu yêu cầu nguồn', 'P1', [PRE_LIST, 'Phiếu EG.PKT1026.00005 lập từ EG.DNDCCN1026.00005 của phòng Kinh '
       'doanh 1, người tạo phiếu kế toán thuộc phòng Tài chính.'], [MENU, 'Tìm "EG.PKT1026.00005".'], '—',
       ['Cột Phòng ban là phòng của phiếu yêu cầu nguồn (Phòng Kinh doanh 1), không phải phòng người tạo phiếu kế toán.'], 6)
S1.add('Link Mã phiếu YCĐC mở phiếu nguồn ở tab mới', 'P2', [PRE_LIST, DONE],
       [MENU, 'Bấm "PYCHTBS-002289" ở dòng TPE.PKT1026.00458.', 'Bấm mã phiếu YCĐC ở dòng lập từ phiếu YCĐC.'], '—',
       ['Bước 2: mở màn chi tiết Phiếu yêu cầu hạch toán bổ sung ở tab mới.', 'Bước 3: mở màn chi tiết Phiếu yêu cầu điều chỉnh công '
        'nợ ở tab mới; danh sách giữ nguyên.'], 6)
S1.add('Nhãn trạng thái của phiếu', 'P0', [PRE_LIST], [MENU, ADV, 'Lọc Trạng thái = Đang tạo.', 'Lọc Trạng thái = Đã duyệt.'],
       '—', ['Đang tạo: nhãn xám; Đã duyệt: nhãn xanh.', 'Ô Trạng thái chỉ có 2 lựa chọn, không có Hủy.'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', 'Tài khoản N mới, không có quyền, chưa tạo phiếu.', ['Đăng nhập N.', MENU], '—',
       ['Bảng hiện "Không có dữ liệu phù hợp.".', 'Không báo lỗi.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       ['Bảng hiện "Không có dữ liệu phù hợp.".'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 3.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 20 phiếu, tự về trang 1, "Hiển thị 1–20 / 15410".', 'STT từ 1 đến 20; danh sách chỉ nạp 1 lần.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–20 / 15410".', 'Bước 3: "Hiển thị 1–10 / 15410".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—',
       ['Bước 2: trang 1541, "Hiển thị 15401–15410 / 15410".', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang cuối quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ, bấm không tác dụng.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2, rồi trang 3.'], '—', ['Trang 2: 11–20; trang 3: 21–30.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 4.', ADV, 'Chọn Trạng thái = Đã duyệt.'],
       'Trạng thái: Đã duyệt', ['Tự nạp lại ở trang 1; "Hiển thị 1–10 / 15409".'], 17)
S1.add('Sắp xếp tăng dần theo Tổng phát sinh', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Tổng phát sinh.'], '—',
       ['Xếp từ nhỏ đến lớn, mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Tổng phát sinh', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Tổng phát sinh 2 lần.'], '—',
       ['Xếp từ lớn đến nhỏ, mũi tên xuống.'], 21)
S1.add('Sắp xếp theo Ngày tạo / Mã phiếu', 'P1', PRE_LIST, [MENU, 'Bấm tiêu đề Ngày tạo 2 lần.', 'Bấm tiêu đề Mã phiếu.'], '—',
       ['Ngày tạo: lần 1 cũ nhất trên, lần 2 mới nhất trên.', 'Mã phiếu xếp theo thứ tự chữ.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Mã phiếu YCĐC, Diễn giải, Ngày hạch toán, Người tạo, Ngày cập nhật, Người cập nhật, Phòng ban, Loại tiền, '
              'Trạng thái.'], '—', ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Tổng phát sinh (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự tăng của trang 1.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 4.', 'Bấm tiêu đề Ngày tạo.'], '—', ['Về trang 1.'], 25)
S1.add('Mở màn Tạo từ nút trên phiếu nguồn', 'P1', [ACC_K, YCDC, HTBS],
       ['Đăng nhập K.', YC_MENU, 'Ở dòng TPE.DNDCCN1026.00401 bấm Tạo phiếu kế toán.', HT_MENU, 'Ở dòng PYCHTBS-002288 bấm Lập phiếu kế toán.'],
       '—', ['Bước 3: mở màn "Tạo phiếu kế toán" với ô Phiếu yêu cầu điều chỉnh công nợ = TPE.DNDCCN1026.00401, dữ liệu điền sẵn.',
             'Bước 5: mở màn Tạo với ô Phiếu yêu cầu hạch toán bổ sung = PYCHTBS-002288 (khóa), dữ liệu điền sẵn.'], 1)
S1.add('Menu "…" trên dòng có hơn 3 nút', 'P2', [ACC_K, DRAFT_K], ['Đăng nhập K.', MENU, 'Ở dòng TPE.PKT1126.00001 bấm "…".'], '—',
       ['Dòng hiện Sửa, Xóa và nút "…"; menu "…" có In, Xuất Excel, Lịch sử.', 'Dòng Đã duyệt hiện thẳng In, Xuất Excel, Lịch sử.'], 3)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo mã phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "TPE.PKT1026.00458", bấm Tìm kiếm.'],
       'Ô tìm nhanh: TPE.PKT1026.00458', ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần mã phiếu', 'P0', PRE_LIST, [MENU, 'Nhập "PKT1126", bấm Tìm kiếm.'], 'PKT1126',
       ['Chỉ còn các phiếu tạo tháng 11/2026 (có TPE.PKT1126.00001).'], 27)
S2.add('Ô tìm nhanh không tìm theo mã phiếu nguồn / diễn giải', 'P1', PRE_LIST, [MENU, 'Nhập "PYCHTBS-002289", bấm Tìm kiếm.'], '—',
       ['"Không có dữ liệu phù hợp." (mã phiếu nguồn dùng ô lọc Mã phiếu YCĐC).'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "tpe.pkt1026.00458", bấm Tìm kiếm.'], '—',
       ['Ra phiếu TPE.PKT1026.00458 như khi gõ chữ hoa.'], 28)
S2.add('Có dấu / không dấu', 'P1', 'Có phiếu dòng định khoản ngân hàng "Ngân hàng Công Thương".', [MENU, ADV, 'Nhập Ngân hàng "cong thuong", bấm Tìm kiếm.'],
       '—', ['Ra phiếu có ngân hàng "Ngân hàng Công Thương" nếu cơ sở dữ liệu so khớp không dấu.',
             'Lưu ý: so khớp theo cách so sánh chữ của cơ sở dữ liệu.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; ký tự % được hiểu là ký tự đại diện nên ra toàn bộ phiếu.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  PKT1026.00458  ", bấm Tìm kiếm.'], '—',
       ['Ra phiếu TPE.PKT1026.00458 (hệ thống bỏ khoảng trắng đầu / cuối); không ra thì ghi nhận lỗi.'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "PKT1026.00458", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Sau bước 2 hiện lại đủ 15.410 phiếu.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST, [MENU, 'Nhập "PKT1026.00458", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'],
       '—', ['Cả 2 cách đều ra phiếu TPE.PKT1026.00458, về trang 1.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['13 ô lọc (Công ty, Phòng ban, Mã phiếu YCĐC, Người tạo, Trạng thái, Tài khoản, Đơn hàng / Hợp đồng, Khách hàng, Số tiền, Ngân '
        'hàng, STK ngân hàng, NVKD, Ngày tạo) đều trống.', 'Đủ 15.410 phiếu.'], 36)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đang tạo.'], '—',
       ['Lọc ngay khi chọn; chỉ phiếu nhãn xám Đang tạo của DNS Admin (1 phiếu).'], 37)
S2.add('Lọc Mã phiếu YCĐC', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "PYCHTBS-002289" vào Mã phiếu YCĐC.', 'Bấm Tìm kiếm.'], '—',
       ['Bước 3: chưa lọc khi chỉ gõ.', 'Bước 4: ra phiếu TPE.PKT1026.00458 (ô soi cả mã phiếu YCĐC và mã phiếu hạch toán bổ sung).'], 37)
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = DNS Admin.'], '—', ['Chỉ phiếu do DNS Admin tạo.'], 37)
S2.add('Lọc Tài khoản theo số hoặc tên', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "35241" vào Tài khoản, bấm Tìm kiếm.', 'Đổi thành "Tiền mặt", bấm Tìm kiếm.'],
       '—', ['Bước 3: có TPE.PKT1126.00001 (dòng TK 35241).', 'Bước 4: phiếu có dòng tài khoản tên chứa "Tiền mặt" (có TPE.PKT1026.00458).'], 37)
S2.add('Lọc Đơn hàng / Hợp đồng', 'P1', PRE_LIST, [MENU, ADV, 'Gõ "HD_TPE_HN_KD2_26_0352" vào Đơn hàng / Hợp đồng, bấm Tìm kiếm.'], '—',
       ['Ra phiếu có dòng gắn hợp đồng đó (có TPE.PKT1026.00458).'], 37)
S2.add('Lọc Khách hàng', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "35TNIPTH" vào ô Khách hàng, chọn dòng gợi ý.'], '—',
       ['Gõ dưới 2 ký tự chưa gợi ý.', 'Chọn xong lọc ngay; có TPE.PKT1026.00458.'], 37)
S2.add('Lọc khoảng Số tiền', 'P0', PRE_LIST, [MENU, ADV, 'Nhập Số tiền từ 6,594,953 đến 6,594,953, bấm Tìm kiếm.'], '—',
       ['Lấy cả 2 biên: có TPE.PKT1026.00458 (Tổng phát sinh 6,594,953).'], 37)
S2.add('Lọc Ngân hàng / STK ngân hàng', 'P1', 'Có phiếu dòng định khoản STK ngân hàng 999888777.', [MENU, ADV, 'Gõ "999888777" vào STK ngân hàng, bấm '
       'Tìm kiếm.'], '—', ['Ra phiếu có dòng STK đó; không báo lỗi.'], 37)
S2.add('Lọc NVKD', 'P1', 'Có 84 phiếu có dòng gắn hợp đồng do nhân viên N1 lập.', [MENU, ADV, 'Chọn NVKD = N1.'], '—',
       ['Lọc ngay; 84 phiếu.'], 37)
S2.add('Lọc Ngày tạo lấy trọn ngày biên', 'P0', 'Có phiếu TPE.PKT1026.00458 tạo 30/10/2026 15:27.', [MENU, ADV, 'Chọn Ngày tạo 30/10/2026 – 30/10/2026.'],
       '—', ['Ra phiếu TPE.PKT1026.00458.'], 37)
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đã duyệt.', 'Chọn Người tạo = DNS Admin.'],
       '—', ['Chỉ phiếu thỏa cả 2 điều kiện.'], 38)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST, [MENU, 'Nhập "PKT1026.00458", bấm Tìm kiếm.', ADV, 'Chọn Trạng thái = Đang tạo.'], '—',
       ['"Không có dữ liệu phù hợp." vì phiếu đó Đã duyệt.'], [39, 40])
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đã duyệt.', 'Bấm trang cuối.'],
       '—', ['"Hiển thị 1–10 / 15409".', 'Trang cuối "Hiển thị 15401–15409 / 15409".'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Trạng thái = Đã duyệt.', ['Bấm tiêu đề Tổng phát sinh.'], '—',
       ['Chỉ phiếu Đã duyệt được sắp; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "PKT1026", lọc Trạng thái, Khách hàng, sắp Tổng phát sinh, ở trang 2.',
       ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống, bỏ sắp xếp, nạp lại trang 1, đủ 15.410 phiếu.'], 44)
S2.raw(org_cases(SCREEN, len(S2) + 1), [[37], [37], [37]])
S2.add('Ô Công ty khóa với quyền xem theo công ty', 'P1', ACC_D, ['Đăng nhập D.', MENU, ADV], '—',
       ['Ô Công ty khóa (không chọn được); ô Phòng ban chọn được trong công ty 1.'], [37, 299])
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Đã duyệt, chưa mở màn con nào.'],
       ['Nhấn F5.'], '—', ['Bộ lọc trở về trống, đủ 15.410 phiếu (bộ lọc chỉ nhớ khi đi vào màn chi tiết / sửa / tạo của màn).'], 46)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích NVKD, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô NVKD.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Đã duyệt.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Trạng thái, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị xóa, nạp lại đủ phiếu.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn NVKD.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, NVKD vẫn ẩn.', 'Bước 2: tích đủ 12 dòng tiêu chí, NVKD hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Ngày tạo lên đầu, bấm Lưu.'], '—',
       ['Ô Ngày tạo đứng đầu khối Tìm kiếm nâng cao.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo', 'P0', PRE_FORM, TAO, '—', ['Mở TRANG "Tạo phiếu kế toán", tab cùng tiêu đề.'], 49)
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải "<tên K> - <ngày giờ hiện tại>".', 'Không có nhãn trạng thái, không có ô Mã phiếu.'], 50)
S3.add('Các trường, khối và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Phiếu yêu cầu điều chỉnh công nợ, Ngày hạch toán *, Loại tiền *, Tỷ giá (VND) *, Diễn giải *.',
        'Khối File đính kèm (nút Thêm tài liệu), khối Chi tiết (nút Thêm dòng).',
        'Chân màn: Lưu nháp, Lưu và duyệt, Lưu và tiếp tục, Quay lại.'], [51, 54])
S3.add('Trường bắt buộc khi Lưu nháp và khi Lưu và duyệt', 'P0', PRE_FORM, TAO + ['Quan sát dấu * và thử 2 nút (xem TC_03.012, TC_06.003).'],
       '—', ['Dấu * ở Ngày hạch toán, Loại tiền, Tỷ giá, Diễn giải, Số tài khoản, Diễn giải dòng.', 'Lưu nháp chỉ bắt Ngày hạch toán.'], 52)
S3.add('Giá trị mặc định', 'P0', PRE_FORM, TAO, '—',
       ['Ngày hạch toán = hôm nay; Loại tiền VNĐ; Tỷ giá 1 (ô khóa); Diễn giải trống; bảng Chi tiết "Chưa có dòng định khoản nào.".'], 53)
S3.add('Lưu nháp đầy đủ thông tin hợp lệ', 'P0', PRE_FORM, TAO_FULL + ['Bấm Lưu nháp.'], FULL,
       ['Báo "Thêm mới thành công.", về danh sách.', 'Dòng mới trên cùng, mã dạng TPE.PKT1126.000NN, nhãn xám Đang tạo.'], [55, 79, 85])
S3.add('Lưu nháp chỉ có Ngày hạch toán', 'P0', PRE_FORM, TAO + ['Bấm Lưu nháp ngay.'], '—',
       ['Lưu được phiếu Đang tạo không có dòng định khoản, Diễn giải trống.'], [56, 57])
S3.add('Lưu nháp với dòng thiếu Số tài khoản', 'P1', PRE_FORM, TAO + ['Bấm Thêm dòng, nhập Nợ 100, không chọn Số tài khoản.', 'Bấm Lưu nháp.'],
       '—', ['Lưu được; mở lại màn Sửa, dòng giữ Nợ 100, Số tài khoản trống.'], 57)
S3.add('Dữ liệu sau lưu', 'P0', PRE_FORM, TAO_FULL + ['Bấm Lưu nháp.', 'Bấm mã phiếu vừa tạo.'], FULL,
       ['Màn chi tiết hiện đúng Ngày hạch toán, VNĐ, Diễn giải, 2 dòng như đã nhập, dòng Tổng 1,000,000 / 1,000,000.'], 58)
S3.add('Trạng thái mặc định sau lưu', 'P0', PRE_FORM, TAO_FULL + ['Bấm Lưu nháp.'], FULL, ['Phiếu ở trạng thái Đang tạo (nhãn xám), chưa ghi sổ.'], 59)
S3.add('Lịch sử tạo', 'P1', PRE_FORM, TAO_FULL + ['Bấm Lưu nháp.', 'Ở dòng phiếu mới bấm "…" > Lịch sử.'], FULL,
       ['Có 1 mốc "Tạo mới", người thực hiện K, thời gian lúc lưu.'], [60, 176])
S3.add('Bỏ trống Ngày hạch toán', 'P0', PRE_FORM, TAO + ['Xóa ô Ngày hạch toán.', 'Bấm Lưu nháp.'], '—',
       ['Viền đỏ, chữ "Bắt buộc phải nhập" dưới ô; thông báo "Bạn chưa nhập đầy đủ thông tin.".', 'Không lưu, vẫn ở màn Tạo.'],
       [61, 70, 80])
S3.add('Sai định dạng số tiền', 'P1', PRE_FORM, TAO + ['Bấm Thêm dòng, gõ "abc" vào Phát sinh nợ.'], '—',
       ['Ô không nhận chữ, giữ 0.'], [62, 81])
S3.add('Ký tự đặc biệt trong Diễn giải', 'P2', PRE_FORM, TAO + ['Nhập Diễn giải "<b>Test</b> & @#$%".', 'Bấm Lưu nháp.'], '—',
       ['Lưu được; màn chi tiết hiện nguyên chuỗi, không định dạng in đậm.'], 63)
S3.add('Diễn giải không có độ dài tối thiểu', 'P2', PRE_FORM, TAO + ['Nhập Diễn giải "a".', 'Bấm Lưu nháp.'], '—', ['Lưu được.'], 64)
S3.add('Diễn giải dòng đúng / vượt 255 ký tự', 'P1', PRE_FORM, TAO_FULL + ['Nhập Diễn giải dòng 1 dài 255 ký tự, Lưu nháp.',
       'Tạo phiếu khác, Diễn giải dòng 256 ký tự, Lưu nháp.'], 'Chuỗi 255 / 256 ký tự',
       ['Bước 4: lưu được.', 'Bước 5: máy chủ báo lỗi độ dài Diễn giải dòng, không lưu.'], [65, 66])
S3.add('Lập 2 phiếu cùng nội dung', 'P1', PRE_FORM, TAO_FULL + ['Bấm Lưu nháp.', 'Tạo lại phiếu y hệt, Lưu nháp.'], FULL,
       ['Cả 2 phiếu lưu được, mã khác nhau (phiếu không có trường duy nhất).'], [67, 75, 82])
S3.add('Khoảng trắng đầu / cuối và chỉ khoảng trắng', 'P1', PRE_FORM,
       TAO_FULL + ['Đổi Diễn giải thành "   ".', 'Bấm Lưu và duyệt, bấm Duyệt.'], 'Diễn giải: 3 khoảng trắng',
       ['Diễn giải chỉ khoảng trắng bị coi là trống: "Bắt buộc phải nhập" dưới ô, không mở ghi sổ.'], [68, 69])
S3.add('Lỗi biến mất sau khi sửa', 'P1', PRE_FORM, TAO + ['Xóa Ngày hạch toán, Lưu nháp.', 'Chọn lại ngày hôm nay.'], '—',
       ['Chữ đỏ dưới ô biến mất ngay khi chọn ngày.'], 71)
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, TAO_FULL + ['Bấm Lưu và tiếp tục.'], FULL,
       ['Báo "Thêm mới thành công."; vẫn ở màn Tạo, form làm mới (Ngày hạch toán hôm nay, bảng trống).', 'Danh sách có phiếu vừa lưu.'],
       [72, 76, 77])
S3.add('Lưu và tiếp tục khi thiếu Ngày hạch toán', 'P1', PRE_FORM, TAO + ['Xóa Ngày hạch toán.', 'Bấm Lưu và tiếp tục.'], '—',
       ['"Bắt buộc phải nhập" dưới ô; không lưu, giữ dữ liệu.'], [73, 74])
S3.add('Rời màn sau Lưu và tiếp tục', 'P2', PRE_FORM, TAO_FULL + ['Bấm Lưu và tiếp tục.', 'Bấm Quay lại.'], FULL,
       ['Form vừa làm mới chưa đổi gì: về danh sách ngay, không hỏi.'], 78)
S3.add('Sau Lưu nháp màn chuyển về danh sách', 'P1', PRE_FORM, TAO_FULL + ['Bấm Lưu nháp.'], FULL,
       ['Màn Tạo là trang: sau lưu chuyển về danh sách (không có cửa sổ nào còn mở).'], [83, 84])
S3.add('Lưu và duyệt từ màn Tạo với dữ liệu hợp lệ', 'P0', PRE_FORM, TAO_FULL + ['Bấm Lưu và duyệt, bấm Duyệt.'], FULL,
       ['Báo "Duyệt phiếu kế toán thành công.", về danh sách; phiếu mới nhãn xanh Đã duyệt.'], [86, 90, 91, 92])
S3.add('Lưu và duyệt khi thiếu thông tin', 'P0', PRE_FORM, TAO + ['Bấm Thêm dòng.', 'Bấm Lưu và duyệt, bấm Duyệt.'], '—',
       ['Đỏ dưới Diễn giải, Số tài khoản, Diễn giải dòng ("Bắt buộc phải nhập") và 2 ô tiền ("Bắt buộc nhập phát sinh nợ hoặc phát sinh '
        'có").', 'Thông báo "Bạn chưa nhập đầy đủ thông tin.", cuộn tới ô lỗi đầu, không lưu.'], [87, 88])
S3.add('Lưu và duyệt 2 phiếu cùng nội dung', 'P2', PRE_FORM, TAO_FULL + ['Lưu và duyệt.', 'Lập phiếu y hệt, Lưu và duyệt.'], FULL,
       ['Cả 2 ghi sổ được (không có ràng buộc trùng giữa các phiếu).'], 89)
S3.add('Rời màn khi chưa nhập gì', 'P1', PRE_FORM, TAO + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 93)
S3.add('Rời màn khi đã nhập', 'P0', PRE_FORM, TAO + ['Nhập Diễn giải "abc".', 'Bấm Quay lại.'], '—',
       ['Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?", nút Thoát, Ở lại.'], 94)
S3.add('Rời màn bằng menu hoặc nút trình duyệt', 'P2', PRE_FORM, TAO + ['Nhập Diễn giải "abc".', 'Bấm 1 mục menu khác.'], '—',
       ['Hiện hộp "Thông tin chưa lưu" (màn là trang, không có nút X).'], 95)
S3.add('Chọn Thoát', 'P1', PRE_FORM, TAO + ['Nhập Diễn giải "abc".', 'Bấm Quay lại, chọn Thoát.'], '—', ['Về danh sách, không có phiếu mới.'], [96, 124])
S3.add('Chọn Ở lại', 'P1', PRE_FORM, TAO + ['Nhập Diễn giải "abc".', 'Bấm Quay lại, chọn Ở lại.'], '—', ['Ở lại màn Tạo, Diễn giải vẫn "abc".'], 97)
S3.add('Nhập rồi xóa hết', 'P2', PRE_FORM, TAO + ['Nhập Diễn giải "abc" rồi xóa hết.', 'Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 98)
S3.add('Đổi rồi khôi phục giá trị ban đầu', 'P2', PRE_FORM, TAO + ['Đổi Loại tiền sang USD rồi về VNĐ (tỷ giá về 1).', 'Bấm Quay lại.'], '—',
       ['Về danh sách ngay, không hỏi.'], 99)
S3.add('Không thao tác lâu', 'P2', PRE_FORM, TAO_FULL + ['Để màn 30 phút, bấm Lưu nháp.'], FULL,
       ['Còn phiên: lưu bình thường; hết phiên: báo hết phiên, chuyển màn đăng nhập.'], 100)
S3.add('Bấm Lưu nháp liên tục', 'P0', PRE_FORM, TAO_FULL + ['Bấm Lưu nháp 3 lần thật nhanh.'], FULL,
       ['Chỉ tạo 1 phiếu (nút khóa trong lúc lưu).'], 101)
S3.add('Lập đồng thời 2 tab từ cùng phiếu YCĐC', 'P1', PRE_FORM,
       ['Tab 1 và tab 2 mở màn Tạo, chọn cùng TPE.DNDCCN1026.00401.', 'Tab 1 Lưu nháp.', 'Tab 2 Lưu nháp.'], '—',
       ['Tab 1 lưu được, phiếu YCĐC sang Đã tạo phiếu kế toán.', 'Tab 2: ghi nhận kết quả (máy chủ không chặn trùng ở bước lưu nháp — '
        'nếu tạo được phiếu thứ 2 thì báo lỗi nghiệp vụ).'], 102)
S3.add('Đổi Loại tiền sang ngoại tệ', 'P1', PRE_FORM, TAO + ['Chọn Loại tiền = USD.', 'Bấm Thêm dòng, nhập Nợ 100.'], 'Loại tiền: USD',
       ['Tỷ giá tự điền tỷ giá danh mục (vd 26,520), ô mở sửa được.', 'Cột Phát sinh nợ / có tách USD và VNĐ; VNĐ = 100 × tỷ giá.'], 62)
S3.add('Nhập Nợ tự xóa Có và Thêm dòng tự cân', 'P0', PRE_FORM, TAO + ['Thêm dòng, nhập Có 500.', 'Nhập Nợ 300 ở cùng dòng.',
       'Bấm Thêm dòng.'], '—', ['Bước 3: Có của dòng về 0.', 'Bước 4: dòng mới cùng nhóm, Phát sinh có tự điền 300.'], 55)
S3.add('Đính kèm file vượt 20MB', 'P1', PRE_FORM, TAO + ['Bấm Thêm tài liệu, chọn file 25MB.'], 'File 25MB',
       ['Báo "Dung lượng tối đa 20MB", file không vào danh sách.'], 62)

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
EDIT = ['Đăng nhập K.', MENU, 'Ở dòng TPE.PKT1126.00001 bấm Sửa (bút chì).']
PRE_E = [ACC_K, DRAFT_K]
S4.add('Mở màn Sửa', 'P0', PRE_E, EDIT, '—', ['Mở TRANG "Sửa phiếu kế toán: TPE.PKT1126.00001".'], 103)
S4.add('Dữ liệu điền đúng', 'P0', PRE_E, EDIT, '—',
       ['Ngày hạch toán 04/11/2026, Loại tiền EURO, Tỷ giá 29,569.91, file pdf đã lưu kèm dung lượng.',
        'Bảng 2 dòng 35241 Nợ 3,100 / 91,666,721 và 811 Có 3,100, đối tượng 29TPHXNA-2.'], 104)
S4.add('Trường được và không được sửa', 'P0', PRE_E, EDIT, '—',
       ['Sửa được: Phiếu YCĐC, Ngày hạch toán, Loại tiền, Tỷ giá, Diễn giải, file, mọi cột dòng định khoản.',
        'Không có ô Mã phiếu; phiếu lập từ yêu cầu hạch toán bổ sung thì ô phiếu nguồn khóa.'], 105)
S4.add('Các nút ở màn Sửa', 'P1', PRE_E, EDIT, '—', ['Chân màn: Lưu nháp, Lưu và duyệt, Quay lại; không có Lưu và tiếp tục.'], 106)
S4.add('Sửa một trường', 'P0', PRE_E, EDIT + ['Đổi Diễn giải thành "Sửa lần 1".', 'Bấm Lưu nháp.'], 'Diễn giải: Sửa lần 1',
       ['Báo "Cập nhật thành công.", về danh sách; phiếu vẫn Đang tạo.'], [107, 110])
S4.add('Sửa nhiều trường', 'P0', PRE_E, EDIT + ['Đổi Ngày hạch toán, Diễn giải, Nợ dòng 1 thành 3,200 và Có dòng 2 thành 3,200.', 'Lưu nháp.'],
       '—', ['Lưu đủ các thay đổi, dòng Tổng 3,200 / 3,200.'], [108, 110])
S4.add('Giữ nguyên giá trị khi lưu không đổi', 'P1', PRE_E, EDIT + ['Bấm Lưu nháp ngay.'], '—',
       ['Lưu thành công, dữ liệu không đổi; không sinh mốc lịch sử mới.'], [109, 125])
S4.add('Ngày / người cập nhật', 'P1', PRE_E, EDIT + ['Đổi Diễn giải, Lưu nháp.'], '—',
       ['Cột Ngày cập nhật = thời điểm lưu, Người cập nhật = K.'], 111)
S4.add('Lịch sử sửa', 'P0', PRE_E, EDIT + ['Đổi Diễn giải "A" thành "B", đổi Số tài khoản dòng 1 sang 1311.', 'Lưu nháp, mở Lịch sử.'], '—',
       ['Mốc "Thay đổi thông tin": "Diễn giải: A -> B" và trên dòng 1 "Tài khoản: 35241 -> 1311".'], [112, 177])
S4.add('Bỏ trống trường bắt buộc khi sửa', 'P0', PRE_E, EDIT + ['Xóa Ngày hạch toán.', 'Lưu nháp.'], '—',
       ['"Bắt buộc phải nhập" dưới ô, không lưu.'], [113, 117])
S4.add('Sai định dạng tỷ giá', 'P1', PRE_E, EDIT + ['Xóa Tỷ giá (để 0).', 'Bấm Lưu và duyệt, Duyệt.'], '—',
       ['"Tỷ giá (VND) – Phải lớn hơn 0" dưới ô, không ghi sổ.'], [114, 115])
S4.add('Không thể trùng phiếu khác', 'P2', PRE_E, EDIT + ['Sửa nội dung giống phiếu TPE.PKT1026.00458, Lưu nháp.'], '—',
       ['Lưu được (phiếu không có trường duy nhất).'], 116)
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P1', PRE_E, EDIT + ['Xóa Ngày hạch toán, Lưu nháp.', 'Chọn lại ngày.'], '—',
       ['Chữ đỏ biến mất.'], 118)
S4.add('Mở Sửa không thay đổi rồi Quay lại', 'P1', PRE_E, EDIT + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 119)
S4.add('Đổi rồi trả về giá trị ban đầu', 'P2', PRE_E, EDIT + ['Đổi Diễn giải rồi gõ lại như cũ.', 'Bấm Quay lại.'], '—',
       ['Về danh sách ngay, không hỏi.'], 120)
S4.add('Rời màn khi đã đổi', 'P0', PRE_E, EDIT + ['Đổi Diễn giải.', 'Bấm Quay lại.'], '—', ['Hiện hộp "Thông tin chưa lưu".'], 121)
S4.add('Xác nhận Thoát', 'P1', PRE_E, EDIT + ['Đổi Diễn giải.', 'Quay lại, chọn Thoát.'], '—',
       ['Về danh sách; phiếu giữ Diễn giải cũ, không ghi lịch sử.'], [122, 124])
S4.add('Xác nhận Ở lại', 'P1', PRE_E, EDIT + ['Đổi Diễn giải.', 'Quay lại, chọn Ở lại.'], '—', ['Ở lại màn Sửa, giữ nội dung đã đổi.'], 123)
S4.add('Sửa phiếu đã duyệt', 'P0', [ACC_K, DONE, 'Phiếu do K tạo.'], ['Đăng nhập K.', MENU, 'Quan sát dòng TPE.PKT1026.00458.'], '—',
       ['Không có nút Sửa / Xóa (phiếu Đã duyệt là trạng thái cuối, coi như khóa sửa).'], 126)
S4.add('Phiếu bị người tạo xóa khi đang sửa', 'P1', PRE_E,
       ['Tab 1 mở màn Sửa TPE.PKT1126.00001.', 'Tab 2 xóa phiếu đó.', 'Tab 1 bấm Lưu nháp.'], '—',
       ['Tab 1 báo không tìm thấy dữ liệu, không tạo phiếu mới.'], 127)
S4.add('Hai tab cùng sửa, 1 tab đã duyệt', 'P1', PRE_E,
       ['Tab 1 và tab 2 mở màn Sửa cùng phiếu.', 'Tab 1 Lưu và duyệt, Duyệt.', 'Tab 2 đổi Diễn giải, Lưu nháp.'], '—',
       ['Tab 2 bị từ chối "Bạn không có quyền sửa phiếu này"; phiếu giữ dữ liệu đã duyệt.'], 128)
S4.add('Phiếu đang dùng ở màn phiếu nguồn', 'P1', [ACC_K, 'K có phiếu Đang tạo lập từ TPE.DNDCCN1026.00401.'],
       ['Đăng nhập K.', 'Sửa phiếu đó, đổi Diễn giải, Lưu nháp.', YC_MENU], '—',
       ['Phiếu YCĐC vẫn ở "Đã tạo phiếu kế toán", liên kết giữ nguyên.'], [129, 272])
S4.add('Bỏ phiếu YCĐC đã chọn ở màn Sửa', 'P1', [ACC_K, 'K có phiếu Đang tạo lập từ TPE.DNDCCN1026.00401.'],
       ['Đăng nhập K.', 'Sửa phiếu đó, bấm × ở ô Phiếu yêu cầu điều chỉnh công nợ.'], '—',
       ['Ô trống, Loại tiền về VNĐ, Tỷ giá 1, bảng Chi tiết trống; hiện lại nút Thêm dòng.'], 105)

# ============================================================== V. XÓA
S5 = Sec(5)
PRE_D = [ACC_K, DRAFT_K]
S5.add('Nút Xóa chỉ ở phiếu Đang tạo của mình', 'P0', PRE_D + [DONE], ['Đăng nhập K.', MENU], '—',
       ['Dòng TPE.PKT1126.00001 có nút Xóa (đỏ); dòng Đã duyệt không có.'], 130)
S5.add('Hộp xác nhận xóa', 'P0', PRE_D, ['Đăng nhập K.', MENU, 'Ở dòng TPE.PKT1126.00001 bấm Xóa.'], '—',
       ['Hộp "Xác nhận xóa", nội dung "Bạn có chắc muốn xóa phiếu kế toán \'TPE.PKT1126.00001\'?", nút Xóa, Hủy.'], [131, 132])
S5.add('Xóa thành công', 'P0', PRE_D, ['Đăng nhập K.', MENU, 'Xóa TPE.PKT1126.00001, bấm Xóa.'], '—',
       ['Báo "Xóa thành công.", dòng biến mất, tổng N giảm 1.'], [133, 139, 140])
S5.add('Hủy xóa', 'P0', PRE_D, ['Đăng nhập K.', MENU, 'Bấm Xóa, bấm Hủy.'], '—', ['Hộp đóng, phiếu còn nguyên.'], 134)
S5.add('Xóa phiếu đang liên kết phiếu nguồn', 'P0', [ACC_K, 'K có phiếu Đang tạo lập từ TPE.DNDCCN1026.00401 và phiếu Đang tạo lập từ '
       'PYCHTBS-002288.'], ['Đăng nhập K.', 'Xóa 2 phiếu đó.', YC_MENU, HT_MENU], '—',
       ['Xóa được; TPE.DNDCCN1026.00401 về "Chờ tạo phiếu kế toán", PYCHTBS-002288 về "Chờ duyệt".'], [135, 141, 280])
S5.add('Xóa phiếu có dòng định khoản (dữ liệu con)', 'P1', PRE_D, ['Đăng nhập K.', 'Xóa TPE.PKT1126.00001.', 'Mở Lịch sử của phiếu qua lọc '
       'Loại hành động = Xóa (người quản trị đối chiếu).'], '—', ['Phiếu và 2 dòng định khoản bị xóa hẳn; mốc "Xóa" kèm bảng dòng trước khi xóa.'], 136)
S5.add('Không xóa được phiếu Đã duyệt', 'P0', [ACC_K, DONE], ['Đăng nhập K.', MENU, 'Mở chi tiết TPE.PKT1026.00458.'], '—',
       ['Không có nút Xóa ở danh sách lẫn màn chi tiết.'], 137)
S5.add('Phiếu đã bị người khác xóa', 'P1', PRE_D, ['Tab 1 mở danh sách.', 'Tab 2 xóa TPE.PKT1126.00001.', 'Tab 1 bấm Xóa phiếu đó, Xóa.'], '—',
       ['Tab 1 báo lỗi không tìm thấy, danh sách nạp lại.'], 138)
S5.add('Xóa từ màn chi tiết', 'P1', PRE_D, ['Đăng nhập K.', 'Mở chi tiết TPE.PKT1126.00001, bấm Xóa, Xóa.'], '—',
       ['Báo "Xóa thành công.", quay về danh sách.'], [130, 139])

# ============================================================== VII. LỊCH SỬ THAY ĐỔI
S6 = Sec(7)
HIS = [MENU, 'Ở dòng TPE.PKT1026.00458 bấm Lịch sử.']
S6.add('Mở cửa sổ lịch sử', 'P0', [PRE_LIST, DONE], HIS, '—', ['Cửa sổ "Lịch sử thay đổi: TPE.PKT1026.00458".'], 162)
S6.add('Thông tin mỗi mốc', 'P0', [PRE_LIST, DONE], HIS, '—',
       ['Mỗi mốc: thời gian, loại hành động có màu, "Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ", nội dung.'], [163, 165, 166, 167])
S6.add('Mới nhất trước', 'P0', [PRE_LIST, DONE], HIS, '—', ['"Thay đổi trạng thái" (Đang tạo -> Đã duyệt) trên, "Tạo mới" dưới.'], 164)
S6.add('Nội dung thay đổi cũ -> mới', 'P0', [ACC_K, DRAFT_K, 'Đã đổi Diễn giải và Nợ dòng 1.'], ['Đăng nhập K.', MENU, 'Lịch sử phiếu TPE.PKT1126.00001.'],
       '—', ['Mốc "Thay đổi thông tin" ghi "Diễn giải: <cũ> -> <mới>" và bảng dòng định khoản sửa "Nợ: 3,100 -> <mới>".'], 168)
S6.add('Lọc theo hành động', 'P1', [PRE_LIST, DONE], HIS + ['Bấm Bộ lọc, chọn Loại hành động = Tạo mới.'], '—', ['Chỉ còn mốc Tạo mới.'], 169)
S6.add('Lọc theo người thực hiện', 'P1', [PRE_LIST, DONE], HIS + ['Bấm Bộ lọc, chọn Người thực hiện = DNS Admin.'], '—', ['Còn đủ 2 mốc.'], 170)
S6.add('Lọc theo thời gian', 'P1', [PRE_LIST, DONE], HIS + ['Bấm Bộ lọc, Từ ngày 30/10/2026, Đến ngày 30/10/2026.'], '—', ['Còn đủ 2 mốc.'], 171)
S6.add('Kết hợp lọc và không có kết quả', 'P2', [PRE_LIST, DONE], HIS + ['Chọn Loại = Xóa, Người = DNS Admin.'], '—',
       ['Không còn mốc nào.'], [172, 173])
S6.add('Làm mới và đóng mở bộ lọc', 'P2', [PRE_LIST, DONE], HIS + ['Lọc Loại = Tạo mới, xóa giá trị ô lọc.', 'Bấm Bộ lọc lần nữa.'], '—',
       ['Bước 4: hiện lại đủ mốc.', 'Bước 5: khối lọc thu gọn.'], [174, 175])
S6.add('Ghi sửa nhiều trường cùng lúc', 'P1', PRE_E, EDIT + ['Đổi Ngày hạch toán, Tỷ giá, Diễn giải, Lưu nháp.', 'Mở Lịch sử.'], '—',
       ['1 mốc "Thay đổi thông tin" gồm 3 dòng cũ -> mới.'], [178, 183])
S6.add('Không ghi khi không đổi', 'P1', PRE_E, EDIT + ['Bấm Lưu nháp ngay.', 'Mở Lịch sử.'], '—', ['Không có mốc mới.'], 182)
S6.add('Ghi xóa file đính kèm', 'P2', [ACC_K, DRAFT_K], EDIT + ['Ở khối File đính kèm bấm Xóa file pdf, xác nhận.', 'Mở Lịch sử.'], '—',
       ['Có mốc ghi file đính kèm đã xóa.'], 183)
S6.add('Đóng cửa sổ lịch sử', 'P1', [PRE_LIST, DONE, 'Đang ở trang 3, lọc Trạng thái = Đã duyệt.'], ['Bấm Lịch sử 1 dòng.', 'Bấm Đóng.'], '—',
       ['Cửa sổ đóng; danh sách giữ trang 3 và bộ lọc.'], [184, 185])
S6.add('Lịch sử ở màn chi tiết giống popup', 'P1', [PRE_LIST, DONE], [MENU, 'Bấm TPE.PKT1026.00458.', 'Bấm Xem lịch sử.'], '—',
       ['Khối Lịch sử hiện đúng 2 mốc như popup ở danh sách.'], 162)

# ============================================================== VIII. XEM CHI TIẾT PHIẾU KẾ TOÁN
S7 = Sec(8)
DET = [MENU, 'Bấm mã phiếu TPE.PKT1026.00458.']
S7.add('Mở màn chi tiết', 'P0', [PRE_LIST, DONE], DET, '—', ['Mở TRANG "Chi tiết phiếu kế toán: TPE.PKT1026.00458".'], [186, 187])
S7.add('Đủ trường và khớp dữ liệu', 'P0', [PRE_LIST, DONE], DET, '—',
       ['Ô Phiếu yêu cầu hạch toán bổ sung "PYCHTBS-002289" (link), Ngày hạch toán 31/10/2026, VNĐ, Tỷ giá 1, Diễn giải, file đính kèm.',
        'Bảng 2 dòng 111 / 112, dòng Tổng 6,594,953 / 6,594,953 — khớp cột Tổng phát sinh ở danh sách.'], [188, 189, 190])
S7.add('Mọi trường chỉ đọc, không có nút Lưu', 'P0', [PRE_LIST, DONE], DET, '—',
       ['Ô khóa, bảng hiện chữ thường; không có Thêm dòng, Thêm tài liệu, Lưu nháp, Lưu và duyệt.',
        'Chân màn: In, Xuất Excel, Quay lại.'], [191, 192])
S7.add('Phiếu Đang tạo của mình', 'P1', PRE_D, ['Đăng nhập K.', MENU, 'Bấm TPE.PKT1126.00001.'], '—',
       ['Chân màn: Sửa, In, Xuất Excel, Xóa, Quay lại.'], 193)
S7.add('Phiếu Đã duyệt (trạng thái cuối)', 'P1', [PRE_LIST, DONE], DET, '—', ['Không có Sửa, Xóa.'], 194)
S7.add('Khu vực lịch sử', 'P2', [PRE_LIST, DONE], DET + ['Bấm Xem lịch sử, rồi Thu gọn.'], '—', ['Khối mở ra 2 mốc, Thu gọn thì ẩn.'], 195)
S7.add('Quay lại giữ trang và bộ lọc', 'P0', [PRE_LIST, 'Đang ở trang 2, lọc Trạng thái = Đã duyệt.'], ['Bấm 1 mã phiếu.', 'Bấm Quay lại.'], '—',
       ['Về danh sách đúng trang 2 và bộ lọc (màn chi tiết là trang: Quay lại thay cho đóng).'], [196, 197])
S7.add('Mở chi tiết phiếu ngoài phạm vi', 'P0', [ACC_B, DONE], ['Đăng nhập B.', 'Mở thẳng đường dẫn chi tiết phiếu TPE.PKT1026.00458 (lấy từ người '
       'khác).'], '—', ['Hệ thống từ chối, báo "Không tải được phiếu"; không lộ dữ liệu.'], [186, 296])

# ============================================================== X. TÙY CHỈNH CỘT
S8 = Sec(10)
COL = [MENU, 'Bấm nút biểu tượng cột (Cấu hình cột hiển thị).']
COL_PRE = [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.']
S8.add('Mở cửa sổ Tùy chỉnh cột', 'P0', COL_PRE, COL, '—', ['Cửa sổ "Tuỳ chỉnh cột", "Đang chọn 14/14 cột".'], [198, 199, 200])
S8.add('Ẩn một cột', 'P0', COL_PRE, COL + ['Bỏ tích Diễn giải, bấm Lưu.'], '—', ['Bảng không còn cột Diễn giải.'], [202, 206])
S8.add('Hiện lại cột đã ẩn', 'P1', 'Đã ẩn cột Diễn giải.', COL + ['Tích Diễn giải, Lưu.'], '—', ['Cột Diễn giải hiện lại đúng vị trí.'], 201)
S8.add('Cột bắt buộc không ẩn', 'P0', COL_PRE, COL + ['Thử bỏ tích STT, Mã phiếu, Hành động.'], '—', ['3 cột xám, không bỏ tích được, không kéo được.'], [203, 205])
S8.add('Kéo thả thứ tự', 'P1', COL_PRE, COL + ['Kéo Loại tiền lên ngay sau Mã phiếu, Lưu.'], '—', ['Cột Loại tiền đứng sau Mã phiếu.'], 204)
S8.add('Đóng không lưu', 'P1', COL_PRE, COL + ['Bỏ tích Phòng ban, bấm Đóng.'], '—', ['Bảng vẫn có Phòng ban.'], 207)
S8.add('Ghi nhớ sau F5 và theo tài khoản', 'P0', 'K đã ẩn cột Diễn giải.', ['Đăng nhập K, F5.', 'Đăng nhập K2 trên máy khác.'], '—',
       ['K: vẫn ẩn Diễn giải; K2: đủ 14 cột.'], [208, 209])
S8.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P1', 'Đang lọc Trạng thái = Đã duyệt.', COL + ['Ẩn Diễn giải, Lưu.'], '—',
       ['Tổng số và bộ lọc giữ nguyên.'], [210, 211])

# ============================================================== XI. XUẤT DANH SÁCH EXCEL
S9 = Sec(11)
EXP = [MENU, 'Bấm Xuất Excel.']
S9.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, EXP, '—',
       ['Cửa sổ "Chọn trường xuất file": 12 trường Mã phiếu, Mã phiếu YCĐC, Tổng phát sinh, Diễn giải, Ngày hạch toán, Ngày tạo, Người '
        'tạo, Ngày cập nhật, Người cập nhật, Phòng ban, Loại tiền, Trạng thái.', 'Tích sẵn đúng cột đang hiện ("Đang chọn 12/12 trường").'],
       [212, 213, 214])
S9.add('Xuất với trường mặc định', 'P0', [PRE_LIST, 'Đang lọc Trạng thái = Đang tạo (1 phiếu).'], EXP + ['Bấm Xuất file.'], '—',
       ['Tải Danh-sach-phieu-ke-toan-<ngày>.xlsx; báo "Xuất Excel thành công".', 'File có 1 dòng, đủ 12 cột + STT.'], [215, 219, 220, 223])
S9.add('Xuất tất cả trường và một số trường', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Đang tạo.'],
       EXP + ['Bấm Bỏ chọn hết, tích Mã phiếu, Tổng phát sinh, Xuất file.', 'Lặp lại với Chọn tất cả.'], '—',
       ['Lần 1: file chỉ STT, Mã phiếu, Tổng phát sinh.', 'Lần 2: đủ 12 trường.'], [216, 217])
S9.add('Không chọn trường nào', 'P1', PRE_LIST, EXP + ['Bấm Bỏ chọn hết, bấm Xuất file.'], '—', ['Không xuất file.'], 218)
S9.add('Theo từ khóa tìm kiếm', 'P1', PRE_LIST, [MENU, 'Tìm "PKT1026.00458".'] + ['Bấm Xuất Excel, Xuất file.'], '—', ['File đúng 1 dòng TPE.PKT1026.00458.'], 219)
S9.add('Xuất nhiều trang', 'P1', [PRE_LIST, 'Lọc Người tạo = DNS Admin (vd 120 phiếu).'], EXP + ['Bấm Xuất file.'], '—',
       ['Nút hiện tiến độ "Đang tải…", file đủ 120 dòng (không chỉ trang đang xem).'], [221, 227])
S9.add('Danh sách rỗng', 'P1', [PRE_LIST, 'Tìm "ZZZ999", bảng rỗng.'], EXP + ['Bấm Xuất file.'], '—',
       ['Báo "Không có dữ liệu để xuất", không tải file.'], 222)
S9.add('Định dạng file, tiêu đề và thứ tự cột', 'P0', [PRE_LIST, 'Đã xuất file của TC_11.002.'], ['Mở file bằng Excel.'], '—',
       ['File .xlsx mở được; dòng 1 letterhead công ty, tiêu đề "DANH SÁCH PHIẾU KẾ TOÁN".', 'Tên cột đúng nhãn, đúng thứ tự đã chọn.'],
       [224, 225, 226])
S9.add('Dữ liệu khớp và định dạng', 'P0', [PRE_LIST, DONE], [MENU, 'Tìm "PKT1026.00458", xuất file, mở file.'], '—',
       ['Tổng phát sinh là ô số 6,594,953 (có dấu phẩy, cộng được); ngày dạng dd/mm/yyyy hh:mm; tiếng Việt có dấu hiển thị đúng.'],
       [228, 229, 230])
S9.add('Xuất Excel một phiếu', 'P0', [PRE_LIST, DONE], [MENU, 'Ở dòng TPE.PKT1026.00458 bấm Xuất Excel.'], '—',
       ['Tải Phieu-ke-toan-TPE-PKT1026-00458.xlsx, báo "Xuất Excel thành công".',
        'File có letterhead, "Ngày 30 Tháng 10 Năm 2026", Mã phiếu, Người tạo, Phòng ban, Loại tiền, Tỷ giá, Diễn giải, bảng định khoản, '
        'dòng Tổng, 5 ô ký.'], [223, 228])

# ============================================================== XII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S10 = Sec(12)
S10.add('Lập phiếu nhập tay khi chưa có phiếu nguồn', 'P1', PRE_FORM, TAO_FULL + ['Lưu nháp.'], FULL,
       ['Lưu được; cột Mã phiếu YCĐC trống.'], 268)
S10.add('Lập phiếu từ phiếu YCĐC cập nhật trạng thái nguồn', 'P0', PRE_FORM,
       TAO + ['Chọn phiếu TPE.DNDCCN1026.00401, nhập Diễn giải dòng còn trống, Lưu nháp.', YC_MENU], '—',
       ['Phiếu YCĐC chuyển "Đã tạo phiếu kế toán", không còn trong cửa sổ chọn và nút Tạo phiếu kế toán biến mất.'], [269, 274, 281])
S10.add('Lập phiếu từ Phiếu yêu cầu hạch toán bổ sung', 'P0', [ACC_K, HTBS],
       ['Đăng nhập K.', HT_MENU, 'Ở PYCHTBS-002288 bấm Lập phiếu kế toán, nhập đủ, Lưu nháp.', 'Quay lại màn hạch toán bổ sung.'], '—',
       ['PYCHTBS-002288 chuyển "Đang duyệt".', 'Bấm Lập phiếu kế toán lần nữa (gọi lại màn Tạo) -> "Phiếu yêu cầu này đã có phiếu kế toán".'],
       [269, 281, 286])
S10.add('Không xóa phiếu đã ghi sổ đang được báo cáo dùng', 'P1', [ACC_K, DONE], ['Đăng nhập K.', MENU], '—',
       ['Phiếu Đã duyệt không có nút Xóa (bút toán đang dùng ở báo cáo công nợ).'], 270)
S10.add('Đổi Diễn giải đồng bộ ở màn liên quan', 'P2', [ACC_K, 'K có phiếu Đang tạo lập từ PYCHTBS-002288.'],
       ['Sửa Diễn giải phiếu, Lưu nháp.', 'Mở PYCHTBS-002288, bấm link phiếu kế toán.'], '—',
       ['Màn phiếu kế toán mở ra hiện Diễn giải mới.'], 278)
S10.add('Mã phiếu không đổi nên không mất liên kết', 'P2', [ACC_K, 'K có phiếu Đang tạo lập từ PYCHTBS-002288.'],
       ['Sửa phiếu, Lưu nháp.', 'Mở PYCHTBS-002288.'], '—', ['Liên kết tới phiếu kế toán còn nguyên (mã phiếu tự sinh, không sửa).'], 279)
S10.add('Bút toán xuất hiện ở báo cáo công nợ', 'P0', [ACC_K, 'K vừa Lưu và duyệt phiếu Nợ 1311 KH 38THAPTR-15 1,000,000.'],
       ['Vào phân hệ Bán hàng > menu "Báo cáo" > nhóm "Báo cáo công nợ" > bấm "Chi tiết công nợ KH".', 'Lọc KH 38THAPTR-15.',
        'Bấm mã chứng từ của bút toán.'], '—',
       ['Có dòng phát sinh 1,000,000 của phiếu kế toán vừa duyệt.', 'Bấm chứng từ mở màn chi tiết phiếu kế toán.'], [274, 282])
S10.add('Phiếu Đã duyệt không còn phiếu nguồn mồ côi', 'P1', [ACC_K, 'Phiếu lập từ TPE.DNDCCN1026.00401 vừa Lưu và duyệt.'], ['Đăng nhập K.', YC_MENU, 'Tìm TPE.DNDCCN1026.00401.'], '—',
       ['Phiếu YCĐC "Đã duyệt phiếu kế toán", người lập nhận thông báo; không có phiếu kế toán nào trỏ tới phiếu nguồn không tồn tại.'],
       [281, 284, 285])
S10.add('Hợp đồng đúng đối tượng của dòng', 'P0', PRE_FORM, TAO + ['Thêm dòng, chọn đối tượng 0SUBKBR-1.', 'Bấm ô Đơn hàng/Hợp đồng.'], '—',
       ['Chỉ hợp đồng của 0SUBKBR-1 (vd HĐDA_TPE_HN-DATD_26_0110…).', 'Đổi đối tượng -> hợp đồng đã chọn bị xóa.'], 283)
S10.add('Dòng vận chuyển nhanh gắn và gỡ phiếu', 'P1', [ACC_K, 'Danh sách cần hạch toán chi phí vận chuyển nhanh có 2 dòng chưa hạch toán.'],
       ['Vào phân hệ Tài chính > menu "Hàng hoá - Dịch vụ - Vận chuyển" > nhóm "Nhập hàng" > bấm "Danh sách cần hạch toán chi phí vận '
        'chuyển nhanh".', 'Tích 2 dòng, bấm Tạo phiếu kế toán, Lưu nháp.', 'Xóa phiếu kế toán vừa tạo.'], '—',
       ['Bước 2: mỗi dòng sinh cặp Nợ 35241 / Có 811; 2 dòng nguồn gắn mã phiếu (link).', 'Bước 3: 2 dòng về chưa hạch toán.'], [274, 280])

# ============================================================== XIII. PHÂN QUYỀN (cuối)
S11 = Sec(13)
S11.add('Xem danh sách theo quyền tổng công ty', 'P0', [ACC_C, 'Toàn hệ thống có 15.410 phiếu, 1 phiếu Đang tạo của DNS Admin.'],
       ['Đăng nhập C.', MENU], '—', ['Thấy 15.409 phiếu (trừ phiếu Đang tạo của người khác); ô Công ty mở.'], [287, 299])
S11.add('Xem danh sách theo quyền công ty', 'P0', ACC_D, ['Đăng nhập D.', MENU], '—', ['Chỉ phiếu của công ty 1; ô Công ty khóa.'], [287, 299])
S11.add('Không có quyền xem', 'P0', [ACC_K, 'K tạo 2 phiếu.'], ['Đăng nhập K.', MENU], '—', ['Chỉ 2 phiếu K tạo.'], [287, 299])
S11.add('Xem chi tiết theo quyền', 'P0', [ACC_D, 'Phiếu P2 thuộc công ty 2.'], ['Đăng nhập D.', 'Mở thẳng đường dẫn chi tiết P2.'], '—',
       ['Báo "Không tải được phiếu" (máy chủ từ chối "Bạn không có quyền xem phiếu này").'], [288, 296])
S11.add('Thêm mới cần Kế toán thanh toán', 'P0', [ACC_B], ['Đăng nhập B.', MENU, 'Mở thẳng đường dẫn màn Tạo phiếu kế toán, nhập đủ, Lưu nháp.'],
       '—', ['Không có nút Tạo mới, không có Lưu và duyệt.', 'Lưu nháp bị từ chối "Bạn không có quyền thực hiện chức năng này".'],
       [289, 295, 296])
S11.add('Sửa, xóa chỉ người tạo', 'P0', [ACC_K2, DRAFT_K], ['Đăng nhập K2.', MENU], '—',
       ['K2 không thấy phiếu Đang tạo của K, không sửa / xóa được.'], [290, 291])
S11.add('Không có Khóa / Import; Xuất Excel không cần quyền riêng', 'P1', ACC_B, ['Đăng nhập B.', MENU, 'Bấm Xuất Excel, Xuất file.'], '—',
       ['Xuất được các phiếu B tạo; không có nút Khóa, Import.'], [292, 293])
S11.add('Xem lịch sử theo phạm vi xem', 'P1', ACC_B, ['Đăng nhập B.', MENU, 'Bấm Lịch sử phiếu của mình.'], '—', ['Xem được lịch sử phiếu của mình.'], 294)
S11.add('Đổi quyền giữa thao tác', 'P1', [ACC_K, 'K đang mở màn Tạo.'], ['Quản trị gỡ quyền Kế toán thanh toán của K.', 'K bấm Lưu nháp.'], '—',
       ['Bị từ chối "Bạn không có quyền thực hiện chức năng này"; tải lại thì mất nút Tạo mới.'], 298)
S11.add('Phiếu nháp của tài khoản đã bị gỡ quyền Kế toán thanh toán', 'P1',
       [ACC_B, 'B có phiếu Đang tạo PKT-B lập khi còn quyền Kế toán thanh toán; quản trị đã gỡ quyền này.'],
       ['Đăng nhập B.', MENU, 'Mở phiếu PKT-B ở màn Sửa (nếu nút Sửa còn hiện), đổi Diễn giải, bấm Lưu nháp.', 'Quay lại danh sách, bấm Xóa '
        'phiếu PKT-B, bấm Xóa.'], '—',
       ['Màn Sửa không có nút Lưu và duyệt.', 'Bước 3 và bước 4 đều bị từ chối "Bạn không có quyền thực hiện chức năng này".',
        'Phiếu PKT-B giữ nguyên Diễn giải cũ, vẫn Đang tạo, không ghi sổ cái.'], 297)
S11.add('Tài khoản không có quyền nào của màn', 'P0', [ACC_B, 'B tạo 2 phiếu khi còn quyền, không có quyền nào của màn ở thời điểm test.'],
       ['Đăng nhập B.', MENU, 'Mở chi tiết 1 phiếu của B, bấm In, Xuất Excel, Xem lịch sử.'], '—',
       ['Danh sách chỉ 2 phiếu B tạo; không có nút Tạo mới.', 'Xem chi tiết, In, Xuất Excel, Lịch sử phiếu của mình vẫn dùng được (không gắn '
        'quyền riêng).'], [287, 295])
S11.add('Mở thẳng đường dẫn màn Sửa phiếu của người khác', 'P0', [ACC_K2, DRAFT_K, 'K2 có đường dẫn màn Sửa phiếu TPE.PKT1126.00001 (K gửi).'],
       ['Đăng nhập K2.', 'Dán đường dẫn màn Sửa phiếu TPE.PKT1126.00001 vào thanh địa chỉ.'], '—',
       ['Báo "Không tải được phiếu"; form không hiện dữ liệu của phiếu.', 'K2 không lưu, không duyệt được phiếu của K.'], 296)

# ============================================================== VI. DUYỆT PHIẾU (Lưu và duyệt)
S12 = Sec(6)
PRE_A = [ACC_K, DRAFT_K]
S12.add('Điều kiện hiện nút Lưu và duyệt', 'P0', [ACC_K, ACC_B], ['Đăng nhập K, mở màn Tạo.', 'Đăng nhập B, mở màn Tạo (đường dẫn trực tiếp).'], '—',
       ['K thấy Lưu và duyệt; B không thấy.'], 300)
S12.add('Hộp xác nhận duyệt', 'P0', PRE_A, EDIT + ['Bấm Lưu và duyệt.'], '—',
       ['Hộp "Xác nhận duyệt phiếu kế toán": "Duyệt phiếu sẽ GHI BÚT TOÁN VÀO SỔ CÁI và không thể hoàn tác. Bạn có chắc chắn muốn duyệt?", '
        'nút Duyệt, Hủy.'], 301)
S12.add('Kiểm tra dữ liệu bắt buộc trước khi duyệt', 'P0', PRE_A, EDIT + ['Xóa Diễn giải dòng 1.', 'Lưu và duyệt, Duyệt.'], '—',
       ['"Bắt buộc phải nhập" dưới Diễn giải dòng 1 và Diễn giải phiếu; không ghi sổ.'], 303)
S12.add('Duyệt thành công', 'P0', PRE_A, EDIT + ['Nhập Diễn giải phiếu và 2 dòng.', 'Lưu và duyệt, Duyệt.'], '—',
       ['"Duyệt phiếu kế toán thành công.", về danh sách; phiếu nhãn xanh Đã duyệt, không còn Sửa / Xóa.'], [302, 305])
S12.add('Nhóm định khoản lệch Nợ / Có', 'P0', PRE_A, EDIT + ['Đổi Có dòng 2 thành 3,000.', 'Lưu và duyệt, Duyệt.'], '—',
       ['"Tổng số phát sinh nợ và phát sinh có trong một nhóm không bằng nhau"; không lưu gì.'], 304)
S12.add('Trùng tài khoản, đối tượng, hợp đồng trong nhóm', 'P1', PRE_A,
       EDIT + ['Tạo 2 dòng Nợ cùng TK 1311, cùng KH, cùng hợp đồng, 1 dòng Có cân.', 'Lưu và duyệt, Duyệt.'], '—',
       ['"Nhóm định khoản 1 đang bị trùng số tài khoản, khách hàng và hợp đồng".'], 304)
S12.add('Nhiều dòng Nợ và nhiều dòng Có trong 1 nhóm', 'P1', PRE_A, EDIT + ['Nhóm 1: 2 dòng Nợ 50 + 50, 2 dòng Có 50 + 50.', 'Lưu và duyệt, Duyệt.'],
       '—', ['"Có nhiều phát sinh có và phát sinh nợ trong một nhóm định khoản".'], 304)
S12.add('Dữ liệu ghi sổ sau duyệt', 'P0', [ACC_K, 'K vừa duyệt phiếu Nợ 1311 KH 38THAPTR-15 1,000,000 / Có 3311 1,000,000.'],
       ['Mở Chi tiết công nợ KH (Bán hàng > Báo cáo > Báo cáo công nợ), lọc KH 38THAPTR-15.'], '—',
       ['Có bút toán Nợ 1311 1,000,000 của phiếu, ngày theo Ngày hạch toán.'], 306)
S12.add('Ảnh hưởng phiếu nguồn sau duyệt', 'P0', [ACC_K, 'K có phiếu Đang tạo lập từ PYCHTBS-002288.'],
       ['Sửa phiếu, Lưu và duyệt, Duyệt.', HT_MENU], '—', ['PYCHTBS-002288 chuyển Đã duyệt, có người duyệt K và thời gian duyệt.'], 307)
S12.add('Thông báo gửi người lập phiếu nguồn', 'P0', [ACC_K, 'Phiếu nguồn PYCHTBS-002288 do nhân viên S lập.'],
       ['K duyệt phiếu kế toán lập từ PYCHTBS-002288.', 'Đăng nhập S, mở chuông thông báo.'], '—',
       ['S có thông báo "[PKT] Đã duyệt: <mã phiếu>. Từ đề nghị: PYCHTBS-002288. Số tiền: 567,000 … Người duyệt: K".',
        'Phiếu nhập tay không gửi thông báo cho ai.'], 308)
S12.add('Bấm thông báo mở đúng phiếu', 'P1', 'S có thông báo duyệt ở TC_06.010.', ['Bấm thông báo.'], '—',
       ['Mở màn chi tiết phiếu kế toán tương ứng.'], 309)
S12.add('Hủy thao tác duyệt', 'P0', PRE_A, EDIT + ['Bấm Lưu và duyệt, bấm Hủy.'], '—',
       ['Hộp đóng, phiếu vẫn Đang tạo, không ghi sổ, không có mốc lịch sử mới.'], 310)
S12.add('Không duyệt lại phiếu đã duyệt', 'P0', [ACC_K, 'Tab 1, tab 2 cùng mở màn Sửa phiếu Đang tạo của K.'],
       ['Tab 1 Lưu và duyệt, Duyệt.', 'Tab 2 Lưu và duyệt, Duyệt.'], '—',
       ['Tab 2 bị từ chối, không ghi sổ lần 2.'], 311)
S12.add('Lịch sử ghi người và thời gian duyệt', 'P0', [ACC_K, 'K vừa duyệt phiếu ở TC_06.004.'], ['Mở Lịch sử phiếu.'], '—',
       ['Mốc "Thay đổi trạng thái: Đang tạo -> Đã duyệt", người thực hiện K, thời gian duyệt.'], 312)
S12.add('Đề xuất điều chỉnh số dư lẻ', 'P1', [ACC_K, 'Hợp đồng H còn dư nợ TK 1311 là 2,000 sau phiếu, ngưỡng số dư lẻ công ty 1 là 5,000.'],
       TAO + ['Lập phiếu có dòng Có 1311 hợp đồng H, cân nhóm.', 'Lưu và duyệt, Duyệt.', 'Tích hợp đồng H, bấm "Áp dụng vào bảng định khoản".',
              'Lưu và duyệt, Duyệt.'], '—',
       ['Bước 4: thông báo "Hợp đồng có số dư lẻ", khối "Hợp đồng H còn số dư nợ 2,000"; chưa lưu.',
        'Bước 5: thêm nhóm mới Nợ 811 / Có 1311 2,000, diễn giải "Điều chỉnh số dư lẻ".', 'Bước 6: duyệt thành công.'], [302, 304])
S12.add('Bấm Duyệt liên tục', 'P1', PRE_A, EDIT + ['Bấm Lưu và duyệt, bấm Duyệt 3 lần thật nhanh.'], '—',
       ['Chỉ ghi sổ 1 lần.'], 311)

# ============================================================== IX. IN PHIẾU
S13 = Sec(9)
S13.add('In phiếu từ danh sách', 'P0', [PRE_LIST, DONE], [MENU, 'Ở dòng TPE.PKT1026.00458 bấm In.'], '—',
       ['Cửa sổ "Xem trước phiếu TPE.PKT1026.00458" khổ ngang, letterhead công ty ghi trên phiếu, tiêu đề "PHIẾU KẾ TOÁN".',
        'Mã phiếu, Mã phiếu yêu cầu điều chỉnh công nợ, Người tạo, Phòng ban, Loại tiền, Diễn giải; bảng 9 cột, dòng Tổng; 3 ô ký.'])
S13.add('In từ màn chi tiết và từ menu "…"', 'P1', PRE_D, ['Đăng nhập K.', MENU, 'Dòng TPE.PKT1126.00001 bấm "…" > In.', 'Mở chi tiết, bấm In.'],
       '—', ['Cả 2 cách mở cùng cửa sổ xem trước.'])
S13.add('In phiếu ngoại tệ', 'P1', PRE_D, ['Đăng nhập K.', 'In TPE.PKT1126.00001 (EURO).'], '—',
       ['Bảng 11 cột (Nợ / Có tách EURO và VND), dòng "- Tỷ giá ngoại tệ: 29,569.91" căn trái.'])
S13.add('Bấm In trong cửa sổ và đóng', 'P2', [PRE_LIST, DONE], [MENU, 'Bấm In ở 1 dòng, bấm In trong cửa sổ.', 'Đóng hộp in, bấm (x).'], '—',
       ['Mở hộp in trình duyệt; đóng cửa sổ thì danh sách giữ nguyên.'])
S13.add('Letterhead theo công ty ghi trên phiếu', 'P1',
        [PRE_LIST, 'Phiếu EG.PKT1026.00005 thuộc công ty EG; tài khoản DNS Admin thuộc công ty khác.'],
        [MENU, 'Tìm "EG.PKT1026.00005", bấm In.', 'Bấm In ở dòng TPE.PKT1026.00458.'], '—',
        ['Bước 2: đầu bản in là letterhead của công ty EG (công ty ghi trên phiếu), không phải công ty của người đang in.',
         'Bước 3: letterhead công ty TPE.'])

# ============================================================== III (tiếp). THÊM MỚI — CHỌN PHIẾU YÊU CẦU, ĐỐI TƯỢNG VÀ HỢP ĐỒNG
S14 = S3   # các cửa sổ chọn trên form thuộc nhóm THÊM MỚI (khuôn chuẩn)
S14.add('Mở cửa sổ chọn phiếu YCĐC', 'P0', PRE_FORM, TAO + ['Bấm ô Phiếu yêu cầu điều chỉnh công nợ.'], '—',
       ['Cửa sổ "Chọn phiếu yêu cầu điều chỉnh công nợ", dòng phụ "Chỉ phiếu đang Chờ tạo phiếu kế toán".',
        'Cột STT, Mã phiếu yêu cầu, Người tạo, Ngày tạo; 10 dòng/trang; có TPE.DNDCCN1026.00401.'])
S14.add('Chọn phiếu YCĐC điền sẵn dữ liệu', 'P0', PRE_FORM, TAO + ['Mở cửa sổ, bấm dòng TPE.DNDCCN1026.00401.'], '—',
       ['Báo "Thêm phiếu thành công"; ô hiện mã phiếu; Loại tiền khóa; bảng 2 dòng TK 1311 điền sẵn (Mã khách, Nợ / Có chỉ đọc); ẩn Thêm dòng.'])
S14.add('Lọc và Làm mới trong cửa sổ chọn phiếu', 'P1', PRE_FORM, TAO + ['Mở cửa sổ, nhập "00401", Tìm kiếm.', 'Bấm Làm mới.'], '—',
       ['Bước 3: chỉ còn TPE.DNDCCN1026.00401.', 'Bước 4: hiện lại đủ phiếu.'])
S14.add('Bấm mã phiếu trong cửa sổ', 'P2', PRE_FORM, TAO + ['Mở cửa sổ, bấm vào chữ mã TPE.DNDCCN1026.00401.'], '—',
       ['Mở phiếu yêu cầu ở tab mới; dòng không bị chọn.'])
S14.add('Chọn đối tượng cho dòng', 'P0', PRE_FORM, TAO + ['Thêm dòng, bấm ô Mã khách.', 'Lọc Loại = Khách hàng, bấm dòng 0SUBKBR-1.'], '—',
       ['Cửa sổ "Chọn đối tượng" có ô Mã, Tên, Loại (Tất cả / Khách hàng / Nhà cung cấp / Nhân viên).',
        'Dòng điền Mã khách 0SUBKBR-1, Tên khách "PT VINFAST AUTOMOBILE INDONESIA".'])
S14.add('Chọn hợp đồng khi chưa có đối tượng', 'P0', PRE_FORM, TAO + ['Thêm dòng, bấm ô Đơn hàng/Hợp đồng.'], '—',
       ['Thông báo "Chưa chọn đối tượng", không mở cửa sổ.'])
S14.add('Chọn hợp đồng của đối tượng', 'P0', PRE_FORM, TAO + ['Thêm dòng, chọn đối tượng 0SUBKBR-1.', 'Bấm ô Đơn hàng/Hợp đồng, bấm dòng đầu.'], '—',
       ['Cửa sổ "Chọn đơn hàng / hợp đồng", dòng phụ "Đối tượng: 0SUBKBR-1 - PT VINFAST…".', 'Dòng điền mã hợp đồng và NVKD.'])
S14.add('Chọn phiếu yêu cầu xuất hàng', 'P2', [ACC_K, 'Có hợp đồng mua trong nước loại 3 HĐ3 có 2 phiếu YCXH.'],
       TAO + ['Thêm dòng, chọn NCC của HĐ3, chọn HĐ3.', 'Bấm ô Số phiếu yc xuất hàng, chọn loại Yêu cầu xuất hàng, bấm 1 dòng.'], '—',
       ['Dòng hiện ô tích "Số dư nợ đầu kì"; cửa sổ "Chọn phiếu yêu cầu xuất hàng" có 2 phiếu; chọn xong điền mã phiếu.'])
S14.add('Đóng cửa sổ không chọn', 'P2', PRE_FORM, TAO + ['Mở cửa sổ Chọn đối tượng, bấm Đóng (hoặc (x) / ra ngoài).'], '—',
       ['Dòng giữ nguyên.'])

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'CHỈNH SỬA', S4),
    ('V', 'XÓA', S5),
    ('VI', 'DUYỆT PHIẾU', S12),
    ('VII', 'LỊCH SỬ THAY ĐỔI', S6),
    ('VIII', 'XEM CHI TIẾT PHIẾU KẾ TOÁN', S7),
    ('IX', 'IN PHIẾU', S13),
    ('X', 'TÙY CHỈNH CỘT', S8),
    ('XI', 'XUẤT DANH SÁCH EXCEL', S9),
    ('XII', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S10),
    ('XIII', 'PHÂN QUYỀN', S11),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
check_no_dash_pre(SECTIONS, [])
_ids = ['TC_%02d.%s' % (s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
assert len(_ids) == len(set(_ids)), 'Trùng TC ID'
# Mọi mã TC nhắc trong nội dung case phải tồn tại (chống lệch sau khi đổi thứ tự nhóm)
_txt = ' | '.join(str(x) for _, _, s in SECTIONS for tc in s for x in tc[1:])
_bad = sorted(set(re.findall(r'TC_\d{2}\.\d{3}', _txt)) - set(_ids))
assert not _bad, 'Nhắc mã TC không tồn tại: %s' % _bad

if __name__ == '__main__':
    build_chuan(output_file=OUT, sheet_name='Trang tính1', feature_name='Phiếu kế toán - Cập nhật ngày 04/11/2026',
                module_name='Phiếu kế toán', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

# -*- coding: utf-8 -*-
"""Testcase màn "Hạch toán mua dịch vụ" — skill testcase-documenter (tc_engine). Bản đầu 03/11/2026.

Chạy: python gen_testcase.py -> testcase.xlsx
Section xếp đúng thứ tự + tên nhóm của checklist "Mẫu tài liệu.xlsx" (../phieu-theo-form-quoc-gia/checklist_mau_tai_lieu.json),
bỏ nhóm Khóa/Mở khóa, Import, Không duyệt (màn không có); nhóm Duyệt phiếu = luồng Lưu và duyệt (ghi sổ); rồi phần riêng
(XIII In, XIV Chọn phiếu yêu cầu). Chỉ 1 nhóm Phân quyền (role_tcs=[]); Cài đặt bộ lọc nằm trong nhóm Tìm kiếm và lọc.
Mỗi case ghi kèm stt checklist nó phủ (tham số ck) sang gen_checklist.py đọc CK để dựng bảng đối chiếu.
Nguồn hành vi (đọc 03/11/2026, nhánh develop cả 2 repo): FE pages/finance/buy-service-accountings/**, SourcePickerModal,
  AttachmentSection, V2BaseDataTable, filterStateMixin, unsavedChangesMixin, saveAndContinueMixin; BE Modules/Finance
  BuyServiceAccounting (Entity searchByFilter / canView / canEdit), BuyServiceAccountingService (store / update / destroy / ghi sổ),
  BuyServiceAccountingStoreRequest, BuyServiceAccountingController, CatalogHistoryService, ExportColumnRegistry.
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
from tc_engine import build  # noqa: E402
from tc_phieu_bosung import (ListScreen, open_menu_case, filter_memory_cases, combo_cases, org_cases,  # noqa: E402
                             weird_param_case, check_no_dash_pre)

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Bán hàng > menu "Yêu cầu" > nhóm "Mua dịch vụ" > bấm "Hạch toán mua dịch vụ".'
MENU_TC = ('Vào phân hệ Tài chính > menu "Hàng hoá - Dịch vụ - Vận chuyển" > nhóm "Mua dịch vụ" > bấm "Hạch toán mua dịch vụ".')
TAO = [MENU, 'Bấm "Tạo mới".']
CHON = 'Bấm ô Phiếu yêu cầu, bấm dòng TPE.YCHTMDV.2026000069.'
TAO_YC = TAO + [CHON]
ADV = 'Bấm Tìm kiếm nâng cao.'

ACC_K = 'Tài khoản K: có quyền Hạch toán mua dịch vụ, thuộc công ty 1, không có quyền xem theo cấp.'
ACC_K2 = 'Tài khoản K2: có quyền Hạch toán mua dịch vụ, thuộc công ty 1 (kế toán khác).'
ACC_B = 'Tài khoản B: nhân viên công ty 1, không có quyền nào của màn.'
WAIT = ('Phiếu yêu cầu TPE.YCHTMDV.2026000069 Chờ duyệt do K tạo, công ty 1, loại Dịch vụ thuê ngoài, HĐ TPE.HDMDV-91-13131313, NCC '
        '"20TTHPGI-27 - A HẢI", 1 dịch vụ "Chi phí đi lại" đơn giá 22,222, SL yêu cầu 20, Không kèm hóa đơn, 1 file mau-import-rows.xlsx.')
PRE_LIST = 'Tài khoản DNS Admin (Super admin); trong phạm vi xem có 60 phiếu (59 Đã duyệt, 1 Đang tạo của DNS Admin), loại Dịch vụ thuê ngoài.'
PRE_FORM = ACC_K + '\n' + WAIT + '\nTrên máy có file hoadon.pdf (1MB).'
DRAFT_K = ('K có phiếu TPE.HTMDV.2026000061 Đang tạo, lập từ phiếu yêu cầu TPE.YCHTMDV.2026000070 (đang Đang hạch toán), dịch vụ "Chi phí '
           'đi lại" đơn giá 22,222, SL yêu cầu 20, SL hạch toán 20, Không kèm hóa đơn, TK nợ 128, TK có 3311, Diễn giải "Đi lại T10".')
DONE = 'Phiếu TPE.HTMDV.2026000060 Đã duyệt (Tổng thanh toán 7,408.93, ngày hạch toán 23/10/2026 10:19), có 4 mốc lịch sử.'

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
     'Màn Hạch toán mua dịch vụ dùng để kế toán ghi sổ chi phí mua dịch vụ.\n'
     'Phiếu lập từ 1 phiếu Yêu cầu hạch toán mua dịch vụ đang Chờ duyệt (chọn ở cửa sổ hoặc bấm nút Hạch toán ở màn Yêu cầu). Kế toán '
     'chọn tài khoản nợ / có, sửa đơn giá, SL hạch toán, mã phí, mã vụ việc rồi Lưu nháp (Đang tạo) hoặc Lưu và duyệt (Đã duyệt — ghi '
     'bút toán vào sổ kế toán, cộng SL đã hạch toán vào hợp đồng, phiếu yêu cầu sang Đã hạch toán).'),
    ('2. Đối tượng được tính / hiển thị',
     '- 2 loại yêu cầu: Dịch vụ thuê ngoài, Công nợ bảo hiểm (theo phiếu yêu cầu).\n'
     '- Trạng thái: Đang tạo (xám), Đã duyệt (xanh).\n'
     '- Danh sách: phiếu trong phạm vi quyền xem; không có quyền xem thì chỉ phiếu mình tạo.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác: luôn ẩn ở mọi cấp quyền.\n'
     '- Không có Khóa / Mở khóa, Import Excel, Không duyệt (trả phiếu về làm ở màn Yêu cầu).'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo ngày tạo phiếu, lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Dịch vụ thuê ngoài: phiếu > dòng dịch vụ (Đơn giá, Mã phí, Mã vụ việc) > dòng yêu cầu mua dịch vụ (SL hạch toán).\n'
     '- Công nợ bảo hiểm: phiếu gắn 1 đơn bảo hiểm, 1 dòng bảo hiểm.\n'
     '- Phiếu Đã duyệt có các bút toán Nợ / Có (khối Hạch toán ở màn chi tiết).'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Số lượng dịch vụ = tổng SL hạch toán; Thành tiền = SL × Đơn giá; Tổng thanh toán = Thành tiền + VAT.\n'
     '- SL hạch toán từ 0 đến SL yêu cầu.\n'
     '- Mỗi phiếu yêu cầu chỉ có 1 phiếu hạch toán (lưu xong phiếu yêu cầu rời Chờ duyệt).'),
    ('7. Phân quyền cấp',
     '- Xem hạch toán mua dịch vụ - theo tổng công ty / - theo công ty / - theo phòng ban.\n'
     '- Hạch toán mua dịch vụ: nút Tạo mới, lập / sửa / xóa / Lưu và duyệt (sửa / xóa thêm điều kiện người tạo + Đang tạo).\n'
     '- In, Xuất Excel, Lịch sử không gắn quyền riêng.'),
    ('8. Cách tính các ô thống kê',
     '- 3 dòng tổng của bảng dịch vụ: Thành tiền, VAT (x%), Tổng thanh toán.\n'
     '- Khối Hạch toán: dòng Tổng cộng Nợ = Tổng cộng Có.\n'
     '- Dòng "Hiển thị a–b / N": a–b là khoảng số thứ tự trang đang xem, N là tổng phiếu khớp bộ lọc trong phạm vi quyền.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: K (Hạch toán mua dịch vụ, công ty 1), K2 (Hạch toán mua dịch vụ, công ty 1, kế toán khác), B (không '
     'quyền), C (Xem - theo tổng công ty), D (Xem - theo công ty, công ty 1), E (Xem - theo phòng ban), DNS Admin (Super admin).\n'
     '- Số tiền hiển thị dạng 1,234,567.89 (tối đa 2 số lẻ).\n'
     '- Lưu ý: Lưu nháp chỉ bắt buộc Phiếu yêu cầu; Lưu và duyệt mới kiểm tra đủ và hỏi xác nhận.\n'
     '- Lưu ý: Màn Tạo / Sửa / Chi tiết là TRANG riêng, không phải cửa sổ nổi.\n'
     '- Các case "dùng công cụ kiểm thử API" dành cho tester kỹ thuật.'),
]

# ============================================================== I. HIỂN THỊ DANH SÁCH VÀ TRUY CẬP
SCREEN = ListScreen(menu=MENU, title='Hạch toán mua dịch vụ', total=60, quick_label='số phiếu, phiếu yêu cầu, số hợp đồng',
                    quick_sample='HDMDV-92', quick_hit='phiếu TPE.HTMDV.2026000060 (hợp đồng TPE.HDMDV-92-EWEW)',
                    filters=[('Trạng thái', 'Đã duyệt'), ('Loại yêu cầu', 'Dịch vụ thuê ngoài')])
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Mở màn từ phân hệ Tài chính', 'P1', PRE_LIST, [MENU_TC, 'So tổng số với lối vào Bán hàng (TC_01.001).'], '—',
       ['Tiêu đề "Hạch toán mua dịch vụ", cùng tổng 60 phiếu, cùng thứ tự dòng.'], 1)
S1.add('Mở màn từ nút Hạch toán ở màn Yêu cầu', 'P1', [ACC_K, WAIT],
       ['Đăng nhập K.', 'Vào màn Yêu cầu hạch toán mua dịch vụ, ở dòng TPE.YCHTMDV.2026000069 bấm Hạch toán.'], '—',
       ['Mở màn "Tạo phiếu hạch toán mua dịch vụ" với Phiếu yêu cầu = TPE.YCHTMDV.2026000069, dữ liệu điền sẵn.'], 1)
S1.add('Tiêu đề màn hình', 'P0', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Cả 3 nơi đều là "Hạch toán mua dịch vụ".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', [ACC_K], ['Đăng nhập K.', MENU, 'Quan sát khối bộ lọc và thanh công cụ của bảng.'], '—',
       ['Khối bộ lọc: ô tìm nhanh (gợi ý "Tìm theo số phiếu, phiếu yêu cầu, số hợp đồng"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, '
        'Cài đặt bộ lọc.', 'Thanh công cụ: Tạo mới, Xuất Excel, In danh sách, nút biểu tượng cột.', 'Không có nút Import, Khóa.'], 3)
S1.add('Nút Tạo mới ẩn khi không có quyền Hạch toán', 'P0', [ACC_B], ['Đăng nhập B.', MENU], '—',
       ['Không có nút Tạo mới; vẫn có Xuất Excel, In danh sách, nút biểu tượng cột.'], [3, 295])
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột từ trái sang phải.'],
       '—', ['Đúng 14 cột: STT, Số phiếu, Loại yêu cầu, Phiếu yêu cầu, Số hợp đồng, Nhà cung cấp, Tổng thanh toán, Người tạo, Ngày tạo, '
             'Ngày hạch toán, Người cập nhật, Ngày cập nhật, Trạng thái, Hành động.', 'STT và Số phiếu ghim trái khi cuộn ngang.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" tích đủ 14/14 cột ("Đang chọn 14/14 cột").', 'Không có cột Công ty, Phòng ban, Diễn giải trên màn.'], 5)
S1.add('Dữ liệu trên dòng khớp phiếu đã tạo', 'P0', PRE_LIST, [MENU, 'Đối chiếu dòng TPE.HTMDV.2026000060.'], '—',
       ['Loại "Dịch vụ thuê ngoài"; Phiếu yêu cầu TPE.YCHTMDV.2026000068 (link); Số hợp đồng TPE.HDMDV-92-EWEW (link); NCC '
        '"50TPHPTA-749 - ANH SỸ".', 'Tổng thanh toán "7,408.93" căn phải; Người tạo DNS Admin; Ngày tạo 23/10/2026 10:17; Ngày hạch '
        'toán 23/10/2026 10:19.', 'Trạng thái nhãn xanh "Đã duyệt".'], 6)
S1.add('Link phiếu yêu cầu và số hợp đồng mở tab mới', 'P2', PRE_LIST,
       [MENU, 'Bấm số phiếu yêu cầu dòng 060.', 'Bấm số hợp đồng dòng 060.'], '—',
       ['Bước 2: mở màn chi tiết phiếu yêu cầu ở tab mới.', 'Bước 3: mở hợp đồng mua dịch vụ trên ERP ở tab mới; danh sách giữ nguyên.'], 6)
S1.add('Nhãn trạng thái của phiếu', 'P0', [PRE_LIST], [MENU, ADV, 'Lọc Trạng thái = Đang tạo.', 'Lọc Trạng thái = Đã duyệt.'],
       '—', ['Đang tạo: nhãn xám; Đã duyệt: nhãn xanh.', 'Cột Trạng thái không sắp xếp.'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', 'Tài khoản N mới, không có quyền, chưa tạo phiếu.', ['Đăng nhập N.', MENU], '—',
       ['Bảng hiện "Không có dữ liệu phù hợp.".', 'Không báo lỗi.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       ['Bảng hiện "Không có dữ liệu phù hợp.".'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 3.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 20 phiếu, tự về trang 1, "Hiển thị 1–20 / 60".', 'STT từ 1 đến 20; danh sách chỉ nạp 1 lần.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–20 / 60".', 'Bước 3: "Hiển thị 1–10 / 60".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—',
       ['Bước 2: trang 6, "Hiển thị 51–60 / 60".', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang cuối quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ, bấm không tác dụng.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2, rồi trang 3.'], '—', ['Trang 2: 11–20; trang 3: 21–30.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 4.', ADV, 'Chọn Trạng thái = Đã duyệt.'],
       'Trạng thái: Đã duyệt', ['Tự nạp lại ở trang 1; "Hiển thị 1–10 / 59".'], 17)
S1.add('Sắp xếp tăng dần theo Tổng thanh toán', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Tổng thanh toán.'], '—',
       ['Xếp từ nhỏ đến lớn, mũi tên lên; dòng đầu 2,211,000 hoặc nhỏ hơn.'], 20)
S1.add('Sắp xếp giảm dần theo Tổng thanh toán', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Tổng thanh toán 2 lần.'], '—',
       ['Xếp từ lớn đến nhỏ, mũi tên xuống; dòng đầu 754,596,250.'], 21)
S1.add('Sắp xếp theo Ngày tạo / Ngày cập nhật / Ngày hạch toán / Số phiếu', 'P1', PRE_LIST,
       [MENU, 'Bấm tiêu đề Ngày tạo 2 lần.', 'Bấm tiêu đề Ngày cập nhật.', 'Bấm tiêu đề Ngày hạch toán.', 'Bấm tiêu đề Số phiếu.'], '—',
       ['Ngày tạo: lần 1 cũ nhất trên, lần 2 mới nhất trên.', 'Ngày cập nhật, Ngày hạch toán, Số phiếu xếp đúng thứ tự.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Loại yêu cầu, Phiếu yêu cầu, Số hợp đồng, Nhà cung cấp, Người tạo, Người cập nhật, Trạng thái.'],
       '—', ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Tổng thanh toán (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự tăng của trang 1.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 4.', 'Bấm tiêu đề Ngày hạch toán.'], '—', ['Về trang 1.'], 25)
S1.raw([weird_param_case('%03d' % (len(S1) + 1), SCREEN, 'tiêu đề "Hạch toán mua dịch vụ"')], [[1]])
S1.add('Mở danh sách "phiếu của tôi" bằng tham số', 'P2', [ACC_K, 'K tạo 2 phiếu; công ty 1 có 50 phiếu Đã duyệt của người khác.'],
       [MENU, 'Đổi tham số chế độ trên thanh địa chỉ thành "index".'], '—',
       ['Tiêu đề "Hạch toán mua dịch vụ của tôi"; chỉ 2 phiếu K tạo.'], 1)
S1.add('Menu "…" trên dòng có hơn 3 nút', 'P2', [ACC_K, DRAFT_K], ['Đăng nhập K.', MENU, 'Ở dòng 061 bấm "…".'], '—',
       ['Dòng hiện Sửa, Xóa và nút "…"; menu "…" có In phiếu, Lịch sử.'], 3)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM VÀ LỌC
S2 = Sec(2)
S2.add('Tìm theo số phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "TPE.HTMDV.2026000060", bấm Tìm kiếm.'],
       'Ô tìm nhanh: TPE.HTMDV.2026000060', ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần số phiếu / phiếu yêu cầu / số hợp đồng', 'P0', PRE_LIST,
       [MENU, 'Nhập "000060", bấm Tìm kiếm.', 'Nhập "YCHTMDV.2026000068", bấm Tìm kiếm.', 'Nhập "HDMDV-92", bấm Tìm kiếm.'],
       ['000060', 'YCHTMDV.2026000068', 'HDMDV-92'], ['Cả 3 bước đều ra phiếu TPE.HTMDV.2026000060.'], 27)
S2.add('Ô tìm nhanh không tìm theo nhà cung cấp / tên dịch vụ', 'P1', PRE_LIST, [MENU, 'Nhập "ANH SỸ", bấm Tìm kiếm.'], '—',
       ['"Không có dữ liệu phù hợp." (nhà cung cấp dùng ô lọc riêng).'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "tpe.htmdv.2026000060", bấm Tìm kiếm.'], '—',
       ['Ra phiếu 060 như khi gõ chữ hoa.'], 28)
S2.add('Có dấu / không dấu', 'P1', 'Có phiếu dịch vụ "Phí vận chuyển hàng gấp".', [MENU, ADV, 'Nhập Tên dịch vụ "phi van chuyen", bấm Tìm kiếm.'],
       '—', ['Ra phiếu có dịch vụ "Phí vận chuyển hàng gấp" nếu cơ sở dữ liệu so khớp không dấu.',
             'Lưu ý: so khớp theo cách so sánh chữ của cơ sở dữ liệu.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; ký tự % được hiểu là ký tự đại diện nên ra toàn bộ phiếu.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  000060  ", bấm Tìm kiếm.'], '—', ['Vẫn ra phiếu 060.'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "000060", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Sau bước 1 bảng chưa đổi.', 'Sau bước 2 hiện lại đủ 60 phiếu.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST, [MENU, 'Nhập "000060", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'],
       '—', ['Cả 2 cách đều ra phiếu 060, về trang 1.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['Các ô Công ty, Phòng ban, Nhà cung cấp, Tên dịch vụ, Loại yêu cầu, Trạng thái, Ngày tạo đều trống.', 'Đủ 60 phiếu.'], 36)
S2.add('Lọc Loại yêu cầu', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Loại yêu cầu = Dịch vụ thuê ngoài.', 'Chọn Công nợ bảo hiểm.'], '—',
       ['Lọc ngay khi chọn; bước 3: 60 phiếu; bước 4: "Không có dữ liệu phù hợp.".'], 37)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đang tạo.'], '—', ['Chỉ phiếu nhãn xám Đang tạo (của DNS Admin).'], 37)
S2.add('Lọc Nhà cung cấp gõ tay', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "ANH SỸ" vào Nhà cung cấp.', 'Bấm Tìm kiếm.', 'Đổi thành "50TPHPTA-749", '
       'bấm Tìm kiếm.'], '—', ['Bước 3: chưa lọc khi chỉ gõ.', 'Bước 4: ra phiếu 060.', 'Bước 5: khớp theo mã NCC, vẫn ra phiếu 060.'], 37)
S2.add('Lọc Tên dịch vụ', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "vận chuyển hàng gấp" vào Tên dịch vụ, bấm Tìm kiếm.'], '—',
       ['Chỉ phiếu có dòng dịch vụ chứa chuỗi đó.'], 37)
S2.add('Lọc Ngày tạo lấy trọn ngày biên', 'P0', 'Có phiếu tạo 23/10/2026 10:17.', [MENU, ADV, 'Chọn Ngày tạo 23/10/2026 – 23/10/2026.'],
       '—', ['Ra phiếu 060; ô đã chọn ẩn biểu tượng lịch.'], 37)
S2.add('Lọc Công ty, Phòng ban', 'P1', 'Tài khoản C (Xem - theo tổng công ty).', [MENU, ADV, 'Chọn Công ty = Công ty 1.', 'Chọn 1 phòng ban.'],
       '—', ['Chỉ phiếu của công ty 1, rồi của phòng ban đã chọn.'], 37)
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đã duyệt.', 'Gõ Nhà cung cấp "ANH SỸ", bấm Tìm kiếm.'],
       '—', ['Chỉ phiếu thỏa cả 2 điều kiện.'], 38)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST, [MENU, 'Nhập "000060", bấm Tìm kiếm.', ADV, 'Chọn Trạng thái = Đang tạo.'], '—',
       ['"Không có dữ liệu phù hợp." vì phiếu 060 Đã duyệt.'], [39, 40])
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đã duyệt.', 'Bấm trang cuối.'],
       '—', ['"Hiển thị 1–10 / 59"; 6 trang.', 'Trang cuối "Hiển thị 51–59 / 59".'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Trạng thái = Đã duyệt.', ['Bấm tiêu đề Tổng thanh toán.'], '—',
       ['Chỉ phiếu Đã duyệt được sắp; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "HDMDV", lọc Loại yêu cầu, Nhà cung cấp, sắp Tổng thanh toán, ở trang 2.',
       ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống, bỏ sắp xếp, nạp lại trang 1, đủ 60 phiếu.'], 44)
S2.raw(org_cases(SCREEN, len(S2) + 1), [[37], [37], [37]])
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Loại yêu cầu = Dịch vụ thuê ngoài, chưa mở màn con nào.'],
       ['Nhấn F5.'], '—', ['Bộ lọc trở về trống, đủ 60 phiếu (bộ lọc chỉ nhớ khi đi vào màn chi tiết / sửa / tạo của màn).'], 46)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Tên dịch vụ, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô Tên dịch vụ.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Loại yêu cầu = Dịch vụ thuê ngoài.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Loại yêu cầu, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị xóa, nạp lại đủ phiếu.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn Tên dịch vụ.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Tên dịch vụ vẫn ẩn.', 'Bước 2: tích đủ 6 tiêu chí, Tên dịch vụ hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Ngày tạo lên đầu, bấm Lưu.'], '—',
       ['Ô Ngày tạo đứng đầu khối Tìm kiếm nâng cao.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo', 'P0', PRE_FORM, TAO, '—', ['Mở TRANG "Tạo phiếu hạch toán mua dịch vụ", tab cùng tiêu đề.'], 49)
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải "<tên K> – <ngày giờ hiện tại>"; không có nhãn trạng thái, không có ô Số phiếu.'], 50)
S3.add('Các trường, khối và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Phiếu yêu cầu, Loại yêu cầu, Hợp đồng mua dịch vụ, Hóa đơn VAT, Nhà cung cấp, Tài khoản nợ, Tài khoản có, Diễn giải.',
        'Khối File đính kèm (nút Thêm tài liệu), khối Chi tiết.', 'Chân màn: Lưu nháp, Lưu và duyệt, Lưu và tiếp tục, Quay lại.'],
       [51, 54])
S3.add('Đánh dấu bắt buộc', 'P1', PRE_FORM, TAO, '—',
       ['Dấu * ở Phiếu yêu cầu, Hóa đơn VAT, Nhà cung cấp, Tài khoản nợ, Tài khoản có, tiêu đề Chi tiết, cột Đơn giá, SL hạch toán.',
        'Diễn giải, Loại yêu cầu, Hợp đồng không có *.'], 52)
S3.add('Giá trị mặc định', 'P1', PRE_FORM, TAO, '—',
       ['Tài khoản có = 3311 (Phải trả cho người bán ngắn hạn); các ô khác trống; bảng Chi tiết hiện "Chọn phiếu yêu cầu để nạp danh '
        'sách dịch vụ.".'], 53)
S3.add('Dữ liệu điền khi chọn phiếu yêu cầu', 'P0', PRE_FORM, TAO_YC, '—',
       ['Loại "Dịch vụ thuê ngoài", HĐ TPE.HDMDV-91-13131313 (link), NCC "20TTHPGI-27 - A HẢI", Hóa đơn VAT "Không kèm hóa đơn".',
        'Bảng: "Chi phí đi lại", Đơn giá 22,222, SL yêu cầu 20, SL hạch toán 20, Thành tiền 444,440, Tổng thanh toán 444,440.',
        'File mau-import-rows.xlsx của phiếu yêu cầu hiện sẵn kèm dung lượng.'], 53)
S3.add('Lưu và duyệt đầy đủ thông tin hợp lệ', 'P0', PRE_FORM,
       TAO_YC + ['Chọn Tài khoản nợ "128 - Đầu tư nắm giữ đến ngày đáo hạn".', 'Nhập Diễn giải "Đi lại T10".', 'Bấm Lưu và duyệt.',
                 'Bấm Duyệt.'], 'TK nợ: 128',
       ['Hộp "Xác nhận duyệt" hiện ở bước 5.', 'Bước 6: "Duyệt thành công.", về danh sách; phiếu mới đứng đầu, nhãn xanh Đã duyệt, Tổng '
        'thanh toán 444,440, có Ngày hạch toán.'], [55, 86])
S3.add('Lưu nháp chỉ với trường bắt buộc', 'P0', PRE_FORM, TAO_YC + ['Bấm Lưu nháp ngay (chưa chọn Tài khoản nợ).'], '—',
       ['"Thêm mới thành công.", về danh sách; phiếu Đang tạo (xám), Ngày hạch toán trống.',
        'Phiếu yêu cầu 069 chuyển Đang hạch toán.'], [56, 79])
S3.add('Bỏ trống trường không bắt buộc', 'P1', PRE_FORM, TAO_YC + ['Chọn TK nợ 128, để trống Diễn giải, Lưu và duyệt > Duyệt.'], '—',
       ['Lưu thành công, Đã duyệt; Không kèm hóa đơn nên không bắt buộc file.'], 57)
S3.add('Dữ liệu sau lưu', 'P0', 'Vừa lưu phiếu ở TC_03.007.', ['Bấm số phiếu mở chi tiết.'], '—',
       ['Số phiếu dạng TPE.HTMDV.2026xxxxxx; Phiếu yêu cầu, HĐ, NCC, TK nợ 128, TK có 3311, Diễn giải, file, bảng dịch vụ (SL 20, '
        'đơn giá 22,222, Thành tiền 444,440) khớp lúc nhập.', 'Khối Hạch toán: Nợ 128 = 444,440; Có 3311 = 444,440 (đối tượng NCC).'], 58)
S3.add('Trạng thái mặc định', 'P0', PRE_FORM, TAO_YC + ['Bấm Lưu nháp.'], '—',
       ['Phiếu mới ở Đang tạo; chỉ Lưu và duyệt mới sang Đã duyệt.'], 59)
S3.add('Lịch sử tạo', 'P1', 'Vừa lưu nháp phiếu ở TC_03.008.', ['Ở dòng phiếu bấm Lịch sử.'], '—', ['Có mốc "Tạo mới" của K.'], 60)
S3.add('Bỏ trống trường bắt buộc khi Lưu và duyệt', 'P0', PRE_FORM, TAO + ['Bấm Lưu và duyệt khi chưa nhập gì.'], '—',
       ['Báo "Bạn chưa nhập đầy đủ thông tin."; không mở hộp xác nhận, không gửi máy chủ.',
        'Dưới ô: "Phiếu yêu cầu – Bắt buộc phải nhập", "Hóa đơn VAT – Bắt buộc phải nhập", "Nhà cung cấp – Bắt buộc phải nhập", '
        '"Tài khoản nợ – Bắt buộc phải nhập"; viền đỏ; cuộn tới ô lỗi đầu.'], [61, 70, 87])
S3.add('Kèm hóa đơn mà chưa có file', 'P0', PRE_FORM, TAO_YC + ['Chọn Hóa đơn VAT = Kèm hóa đơn, gỡ file kế thừa, chọn TK nợ 128.',
       'Bấm Lưu và duyệt.'], '—', ['Dưới khối File đính kèm: "File đính kèm – Bắt buộc khi kèm hóa đơn VAT".'], [61, 87])
S3.add('Mã phí / Mã vụ việc bắt buộc theo tài khoản nợ', 'P0', PRE_FORM,
       TAO_YC + ['Chọn TK nợ thuộc nhánh 642, bấm Lưu và duyệt.', 'Đổi TK nợ thuộc nhánh 154, bấm Lưu và duyệt.'], '—',
       ['Bước 4: dưới ô "Mã phí – Bắt buộc phải nhập"; cột Mã phí có *.', 'Bước 5: "Mã vụ việc – Bắt buộc phải nhập".'], [61, 87])
S3.add('Sai định dạng: SL hạch toán âm hoặc vượt SL yêu cầu', 'P0', PRE_FORM,
       TAO_YC + ['Nhập SL hạch toán -1, bấm Lưu nháp.', 'Nhập 25, bấm Lưu nháp.'], ['-1', '25'],
       ['Bước 4: "SL hạch toán – Không được nhỏ hơn 0".', 'Bước 5: "SL hạch toán – Không được vượt SL yêu cầu (20)"; không lưu, không tự '
        'kéo về 20.'], [62, 81, 88, 74])
S3.add('Sai định dạng: Đơn giá âm, VAT ngoài 0–100', 'P1', PRE_FORM,
       TAO_YC + ['Nhập Đơn giá -5, bấm Lưu nháp.', 'Sửa Đơn giá 22,222, Kèm hóa đơn, VAT (%) 150, bấm Lưu nháp.'], '—',
       ['"Đơn giá – Không được nhỏ hơn 0".', '"VAT (%) – Phải trong khoảng 0 đến 100".'], [62, 81])
S3.add('Tổng thanh toán bằng 0 khi duyệt', 'P1', PRE_FORM, TAO_YC + ['Nhập SL hạch toán 0, chọn TK nợ 128, bấm Lưu và duyệt.'], '0',
       ['"Tổng thanh toán – Phải lớn hơn 0 trước khi duyệt"; không mở hộp xác nhận.'], [62, 88])
S3.add('Ký tự đặc biệt ở Diễn giải', 'P2', PRE_FORM, TAO_YC + ['Nhập Diễn giải "<b>Test</b> @#$%", bấm Lưu nháp.', 'Mở chi tiết.'], '—',
       ['Lưu được; hiển thị nguyên văn, không thực thi định dạng.'], 63)
S3.add('Diễn giải không có độ dài tối thiểu', 'P2', PRE_FORM, TAO_YC + ['Nhập Diễn giải 1 ký tự "a", bấm Lưu nháp.'], '—', ['Lưu được.'], 64)
S3.add('Diễn giải đúng 1.000 ký tự', 'P1', PRE_FORM, TAO_YC + ['Dán 1.000 ký tự vào Diễn giải, bấm Lưu nháp.'], '1.000 ký tự',
       ['Lưu được, giữ đủ.'], 65)
S3.add('Diễn giải vượt 1.000 ký tự', 'P1', PRE_FORM, TAO_YC + ['Dán 1.050 ký tự vào Diễn giải.'], '1.050 ký tự',
       ['Ô chỉ nhận 1.000 ký tự đầu, phần thừa không gõ được.'], 66)
S3.add('Trùng dữ liệu: lập lại từ phiếu yêu cầu đã có phiếu hạch toán', 'P0', [ACC_K, 'Đã lưu nháp phiếu từ TPE.YCHTMDV.2026000069.'],
       TAO + ['Bấm ô Phiếu yêu cầu.'], '—',
       ['Phiếu 069 không còn trong cửa sổ chọn (đã sang Đang hạch toán) — mỗi phiếu yêu cầu chỉ 1 phiếu hạch toán.',
        'Hai phiếu khác nhau luôn có số phiếu khác nhau (số tự sinh).'], [67, 82])
S3.add('Trùng đồng thời: 2 kế toán cùng lập từ 1 phiếu yêu cầu', 'P0', [ACC_K, ACC_K2, WAIT],
       ['K mở màn Tạo bằng nút Hạch toán ở phiếu 069.', 'K2 cũng mở như vậy.', 'K bấm Lưu nháp.', 'K2 bấm Lưu nháp.'], '—',
       ['K lưu được.', 'K2 báo "Phiếu yêu cầu – Không ở trạng thái Chờ duyệt hoặc bạn không có quyền hạch toán phiếu này."; không lưu.'],
       [75, 89, 102])
S3.add('Khoảng trắng đầu / cuối Diễn giải', 'P2', PRE_FORM, TAO_YC + ['Nhập "  Đi lại  ", Lưu nháp, mở chi tiết.'], '—',
       ['Lưu được; Diễn giải hiển thị không lỗi.', 'Lưu ý: chưa xác minh bằng code việc bỏ khoảng trắng hai đầu — ghi nhận nếu còn.'], 68)
S3.add('Diễn giải chỉ có khoảng trắng', 'P2', PRE_FORM, TAO_YC + ['Nhập "   " vào Diễn giải, chọn TK nợ 128, Lưu và duyệt > Duyệt.'], '—',
       ['Lưu được (Diễn giải không bắt buộc).'], 69)
S3.add('Lỗi biến mất sau khi sửa', 'P1', 'Đang ở TC_03.013 với các ô báo đỏ.', ['Chọn Phiếu yêu cầu 069.'], '—',
       ['Lỗi dưới Phiếu yêu cầu biến mất ngay; chọn TK nợ thì lỗi TK nợ biến mất.'], 71)
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, TAO_YC + ['Bấm Lưu và tiếp tục.'], '—',
       ['Báo "Thêm mới thành công."; vẫn ở màn Tạo, form trống như lúc mới vào (Tài khoản có 3311).', 'Phiếu vừa lưu ở Đang tạo.'],
       [72, 76, 77])
S3.add('Lưu và tiếp tục khi thiếu Phiếu yêu cầu', 'P1', PRE_FORM, TAO + ['Bấm Lưu và tiếp tục.'], '—',
       ['"Phiếu yêu cầu – Bắt buộc phải nhập"; không lưu, ở lại form.'], 73)
S3.add('Lưu và tiếp tục sau đó rời màn', 'P2', 'Vừa Lưu và tiếp tục ở TC_03.028, form trống.', ['Bấm Quay lại.'], '—',
       ['Về danh sách ngay, không hỏi; danh sách có phiếu vừa lưu.'], 78)
S3.add('Lưu nháp thiếu Phiếu yêu cầu', 'P1', PRE_FORM, TAO + ['Bấm Lưu nháp.'], '—', ['"Phiếu yêu cầu – Bắt buộc phải nhập".'], 80)
S3.add('Sau Lưu nháp chuyển về danh sách', 'P1', PRE_FORM, TAO_YC + ['Bấm Lưu nháp.', 'Bấm Back của trình duyệt.'], '—',
       ['Sau lưu về danh sách (màn Tạo là trang).', 'Back không quay lại form vừa lưu.'], [83, 84, 85])
S3.add('Sau Lưu và duyệt chuyển về danh sách', 'P1', PRE_FORM, TAO_YC + ['Chọn TK nợ 128, Lưu và duyệt > Duyệt.'], '—',
       ['Về danh sách, phiếu mới ở đầu; mở Tạo mới lại thì form trống.'], [90, 91, 92])
S3.add('Rời màn khi chưa nhập', 'P1', PRE_FORM, TAO + ['Bấm Quay lại ngay.'], '—', ['Về danh sách, không hỏi.'], 93)
S3.add('Rời màn khi đã nhập', 'P0', PRE_FORM, TAO_YC + ['Bấm Quay lại.'], '—',
       ['Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" (Thoát / Ở lại).'], 94)
S3.add('Vào từ nút Hạch toán rồi rời màn ngay', 'P2', [ACC_K, WAIT], ['Ở màn Yêu cầu bấm Hạch toán dòng 069.', 'Bấm Quay lại ngay.'], '—',
       ['Về danh sách Hạch toán mua dịch vụ, không hỏi (phiếu chọn sẵn là trạng thái gốc); phiếu 069 vẫn Chờ duyệt.'], 93)
S3.add('Rời màn bằng menu / đóng tab', 'P2', PRE_FORM, TAO_YC + ['Bấm 1 mục menu khác.', 'Ở lại, nhấn F5.'], '—',
       ['Bước 4: hộp Thông tin chưa lưu (màn là trang, không có nút X).', 'Bước 5: hộp cảnh báo rời trang của trình duyệt.'], 95)
S3.add('Chọn Thoát', 'P1', 'Đang ở hộp Thông tin chưa lưu.', ['Bấm Thoát.'], '—', ['Về danh sách, không lưu phiếu.'], 96)
S3.add('Chọn Ở lại', 'P1', 'Đang ở hộp Thông tin chưa lưu.', ['Bấm Ở lại.'], '—', ['Đóng hộp, dữ liệu đã nhập giữ nguyên.'], 97)
S3.add('Nhập rồi xóa hết', 'P2', PRE_FORM, TAO + ['Nhập Diễn giải "abc" rồi xóa hết.', 'Bấm Quay lại.'], '—', ['Về danh sách, không hỏi.'], 98)
S3.add('Đổi rồi khôi phục ban đầu', 'P2', PRE_FORM, TAO + ['Đổi Tài khoản có sang 3312 rồi chọn lại 3311.', 'Bấm Quay lại.'], '—',
       ['Về danh sách, không hỏi (dữ liệu như lúc mở).'], 99)
S3.add('Không thao tác lâu', 'P2', PRE_FORM, TAO_YC + ['Để yên 30 phút, bấm Lưu nháp.'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên, về màn đăng nhập, phiếu không lưu.'], 100)
S3.add('Bấm nút lưu liên tục', 'P0', PRE_FORM, TAO_YC + ['Bấm Lưu nháp 3 lần liên tiếp.'], '—', ['Nút khóa khi đang lưu, chỉ tạo 1 phiếu.'], 101)
S3.add('Mã phí đổi ở dòng đầu áp cho mọi dòng', 'P1', [ACC_K, 'Phiếu yêu cầu 071 Chờ duyệt có 2 dịch vụ.'],
       TAO + ['Chọn phiếu 071.', 'Chọn Mã phí ở dòng 1.', 'Đổi Mã phí ở dòng 2.'], '—',
       ['Bước 4: cả 2 dòng cùng Mã phí.', 'Bước 5: chỉ dòng 2 đổi.'], 51)
S3.add('Đổi Hóa đơn VAT tính lại VAT', 'P1', [ACC_K, 'Phiếu yêu cầu 072 Chờ duyệt, Kèm hóa đơn, VAT 10%, Thành tiền 1,000,000.'],
       TAO + ['Chọn phiếu 072.', 'Chọn Không kèm hóa đơn.', 'Chọn lại Kèm hóa đơn.'], '—',
       ['Bước 3: dòng VAT (%) = 10, Tổng 1,100,000.', 'Bước 4: ẩn dòng VAT, Tổng 1,000,000.', 'Bước 5: VAT (%) trở lại 10.'], 53)
S3.add('Bỏ chọn phiếu yêu cầu bằng nút ×', 'P1', PRE_FORM, TAO_YC + ['Thêm file hoadon.pdf.', 'Bấm × ở ô Phiếu yêu cầu.'], '—',
       ['Xóa loại, HĐ, NCC, bảng dịch vụ, file mau-import-rows.xlsx; giữ hoadon.pdf, Diễn giải; Tài khoản có trống.'], 51)
S3.add('File sai định dạng / quá 20MB', 'P1', PRE_FORM, TAO_YC + ['Thêm tài liệu, chọn file .exe.', 'Chọn file 21MB.'], '—',
       ['"File "<tên>" không thuộc định dạng cho phép".', '"File "<tên>" vượt quá 20MB"; file không được thêm.'], 62)
S3.add('Gỡ file kế thừa không ảnh hưởng phiếu yêu cầu', 'P1', PRE_FORM, TAO_YC + ['Bấm xóa dòng file mau-import-rows.xlsx.', 'Lưu nháp.',
       'Mở chi tiết phiếu yêu cầu 069.'], '—', ['Phiếu hạch toán không có file đó; phiếu yêu cầu vẫn còn file.'], 58)

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
EDIT = ['Đăng nhập K.', MENU, 'Ở dòng TPE.HTMDV.2026000061 bấm Sửa (bút chì).']
PRE_E = [ACC_K, DRAFT_K]
S4.add('Mở màn Sửa', 'P0', PRE_E, EDIT, '—', ['Mở TRANG "Sửa phiếu hạch toán mua dịch vụ: TPE.HTMDV.2026000061".'], 103)
S4.add('Dữ liệu điền sẵn đúng', 'P0', PRE_E, EDIT, '—',
       ['Phiếu yêu cầu TPE.YCHTMDV.2026000070 (link), Đơn giá 22,222, SL yêu cầu 20, SL 20, Không kèm hóa đơn, TK nợ 128, TK có 3311, '
        'Diễn giải "Đi lại T10".'], 104)
S4.add('Trường được / không được sửa', 'P0', PRE_E, EDIT, '—',
       ['Phiếu yêu cầu là link chỉ đọc; Loại yêu cầu, Hợp đồng chỉ đọc.',
        'Sửa được Hóa đơn VAT, NCC, TK nợ, TK có, Diễn giải, Đơn giá, SL, Mã phí, Mã vụ việc, file.'], 105)
S4.add('Các nút màn Sửa', 'P1', PRE_E, EDIT, '—', ['Có Lưu nháp, Lưu và duyệt, Quay lại; KHÔNG có Lưu và tiếp tục.'], 106)
S4.add('Sửa một trường', 'P0', PRE_E, EDIT + ['Sửa Diễn giải "Đi lại T11", bấm Lưu nháp.'], '—',
       ['"Cập nhật thành công.", về danh sách; Diễn giải mới.'], 107)
S4.add('Sửa nhiều trường', 'P0', PRE_E, EDIT + ['Sửa SL 8, Đơn giá 20,000, Kèm hóa đơn + file hoadon.pdf, Lưu nháp.'], '—',
       ['Lưu đủ thay đổi; Tổng thanh toán tính lại (160,000 + VAT).'], 108)
S4.add('Giữ nguyên giá trị khi lưu không đổi', 'P1', PRE_E, EDIT + ['Không sửa gì, bấm Lưu nháp.'], '—', ['Lưu được, dữ liệu giữ nguyên.'], 109)
S4.add('Dữ liệu sau lưu', 'P0', 'Đã sửa ở TC_04.006.', ['Mở chi tiết phiếu.'], '—', ['SL 8, Đơn giá 20,000, VAT, file, Diễn giải khớp.'], 110)
S4.add('Ngày / người cập nhật', 'P0', 'Đã sửa ở TC_04.005.', [MENU, 'Quan sát cột Người cập nhật, Ngày cập nhật của phiếu.'], '—',
       ['Người cập nhật = K, Ngày cập nhật = thời điểm lưu.'], 111)
S4.add('Lịch sử sửa', 'P0', 'Đã sửa ở TC_04.006.', ['Mở Lịch sử của phiếu.'], '—',
       ['Mốc "Thay đổi thông tin" ghi cũ sang mới: Hóa đơn VAT, Thuế VAT (%), "Dòng dịch vụ sửa thông tin" (SL hạch toán, Đơn giá), '
        '"File đính kèm thêm mới".'], 112)
S4.add('Sửa rồi Lưu và duyệt', 'P0', PRE_E, EDIT + ['Sửa Diễn giải, bấm Lưu và duyệt > Duyệt.'], '—',
       ['"Duyệt thành công."; phiếu Đã duyệt; lịch sử có "Thay đổi thông tin" và "Thay đổi trạng thái: Đang tạo sang Đã duyệt".'], [112, 107])
S4.add('Bỏ trống bắt buộc khi Lưu và duyệt', 'P0', PRE_E, EDIT + ['Bấm × ở Tài khoản nợ, bấm Lưu và duyệt.'], '—',
       ['"Tài khoản nợ – Bắt buộc phải nhập"; không mở hộp xác nhận.'], 113)
S4.add('Sai định dạng SL', 'P0', PRE_E, EDIT + ['Nhập SL -2, Lưu nháp.'], '-2', ['"SL hạch toán – Không được nhỏ hơn 0".'], 114)
S4.add('Vượt giới hạn SL / Diễn giải', 'P1', PRE_E, EDIT + ['Nhập SL 21, Lưu nháp.', 'Dán 1.050 ký tự vào Diễn giải.'], '—',
       ['"SL hạch toán – Không được vượt SL yêu cầu (20)".', 'Diễn giải chỉ nhận 1.000 ký tự.'], 115)
S4.add('Không trùng với phiếu khác', 'P1', PRE_E, EDIT + ['Quan sát ô Phiếu yêu cầu.'], '—',
       ['Không đổi được phiếu yêu cầu nên không thể trùng phiếu yêu cầu của phiếu khác; số phiếu giữ nguyên.'], 116)
S4.add('Không tính trùng chính phiếu', 'P1', PRE_E, EDIT + ['Giữ SL 20, Lưu nháp.'], '—', ['Lưu được (SL bằng SL yêu cầu, không bị coi là vượt).'], 116)
S4.add('Thông báo lỗi', 'P1', PRE_E, EDIT + ['Bấm × Tài khoản nợ, × Nhà cung cấp, bấm Lưu và duyệt.'], '—',
       ['"Bạn chưa nhập đầy đủ thông tin."; lỗi đỏ dưới 2 ô; cuộn tới ô lỗi đầu.'], 117)
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P1', 'Đang ở TC_04.017.', ['Chọn lại TK nợ 128.'], '—', ['Lỗi TK nợ biến mất; lỗi NCC vẫn còn.'], 118)
S4.add('Mở không thay đổi rồi rời', 'P1', PRE_E, EDIT + ['Bấm Quay lại.'], '—', ['Về danh sách, không hỏi.'], 119)
S4.add('Đổi rồi trả về ban đầu', 'P2', PRE_E, EDIT + ['Sửa Diễn giải rồi gõ lại đúng như cũ.', 'Bấm Quay lại.'], '—', ['Không hỏi.'], 120)
S4.add('Rời màn khi đã đổi', 'P0', PRE_E, EDIT + ['Sửa SL 7.', 'Bấm Quay lại.'], '—', ['Hộp "Thông tin chưa lưu".'], 121)
S4.add('Xác nhận Thoát', 'P1', 'Đang ở hộp của TC_04.021.', ['Bấm Thoát.'], '—', ['Về danh sách; phiếu vẫn SL 20.'], [122, 124])
S4.add('Xác nhận Ở lại', 'P1', 'Đang ở hộp của TC_04.021.', ['Bấm Ở lại.'], '—', ['Ở lại form, SL 7 giữ nguyên.'], 123)
S4.add('Không ghi lịch sử khi không thay đổi', 'P1', 'Đã làm TC_04.007.', ['Mở Lịch sử phiếu 061.'], '—',
       ['Không có mốc mới cho lần lưu không đổi.'], 125)
S4.add('Phiếu Đã duyệt không sửa được', 'P0', [ACC_K, 'K là người tạo phiếu TPE.HTMDV.2026000062 Đã duyệt.'],
       [MENU, 'Quan sát cột Hành động dòng 062.', 'Mở thẳng đường dẫn màn Sửa của phiếu 062.'], '—',
       ['Không có nút Sửa.', 'Tự chuyển sang màn chi tiết.'], [126, 295])
S4.add('Phiếu bị xóa khi đang sửa', 'P2', PRE_E, ['Tab 1 mở màn Sửa phiếu 061.', 'Tab 2 xóa phiếu 061.', 'Tab 1 bấm Lưu nháp.'], '—',
       ['Máy chủ báo không tìm thấy bản ghi, không lưu.'], 127)
S4.add('Hai tab cùng sửa', 'P1', PRE_E, ['Tab 1 và tab 2 mở Sửa phiếu 061.', 'Tab 1 Lưu và duyệt > Duyệt.', 'Tab 2 Lưu nháp.'], '—',
       ['Tab 2 báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang", không lưu.'], 128)
S4.add('Phiếu đã ghi sổ (đang dùng ở sổ kế toán)', 'P1', DONE, [MENU, 'Quan sát dòng 060.'], '—',
       ['Không có Sửa / Xóa; chỉ In phiếu, Lịch sử.'], 129)
S4.add('Gỡ file đã lưu khi sửa', 'P1', [ACC_K, DRAFT_K + ' Có 1 file hoadon.pdf đã lưu.'], EDIT + ['Bấm xóa ở dòng file, xác nhận.'],
       '—', ['Xóa có hiệu lực ngay, báo "Xóa thành công.".', 'Lịch sử có "File đính kèm đã xóa".'], 112)

# ============================================================== V. XÓA
S5 = Sec(5)
PRE_D = [ACC_K, DRAFT_K]
S5.add('Nút Xóa', 'P0', [ACC_K, DRAFT_K, 'K có phiếu 062 Đã duyệt.'], ['Đăng nhập K.', MENU, 'Quan sát cột Hành động phiếu 061 và 062.'], '—',
       ['Phiếu 061: có Xóa (đỏ).', 'Phiếu 062: không có Xóa.'], 130)
S5.add('Hộp xác nhận', 'P0', PRE_D, ['Đăng nhập K.', MENU, 'Bấm Xóa ở dòng 061.'], '—',
       ['Hộp "Xác nhận xóa" ngay trên danh sách, nội dung "Bạn có chắc muốn xóa bản ghi này không?", nút Xóa (đỏ) / Hủy.'], [131, 132])
S5.add('Xóa phiếu không ràng buộc', 'P0', PRE_D, ['Ở hộp xác nhận bấm Xóa.'], '—',
       ['"Xóa thành công.", danh sách nạp lại; phiếu 061 không còn; tổng giảm 1.'], [133, 139, 140])
S5.add('Xóa từ màn chi tiết', 'P1', PRE_D, ['Mở chi tiết 061, bấm Xóa ở chân màn, bấm Xóa.'], '—',
       ['"Xóa thành công.", quay về danh sách.'], 133)
S5.add('Hủy xóa', 'P1', PRE_D, ['Mở hộp xác nhận, bấm Hủy.', 'Mở lại, bấm (x).'], '—', ['Phiếu giữ nguyên.'], 134)
S5.add('Xóa phiếu đã ghi sổ', 'P0', [DONE, 'Dùng công cụ kiểm thử API, tài khoản DNS Admin (người tạo phiếu 060).'], ['Gọi xóa phiếu 060.'], '—',
       ['Máy chủ trả "Trạng thái đã bị thay đổi. Vui lòng load lại trang", không xóa.'], 135)
S5.add('Xóa có dữ liệu cấp con', 'P1', PRE_D, ['Xóa phiếu 061.', 'Kiểm dữ liệu dòng dịch vụ / dòng yêu cầu của phiếu 061.'], '—',
       ['Dòng dịch vụ / yêu cầu xóa theo, không còn bản ghi mồ côi.'], 136)
S5.add('Phiếu đã bị người khác xóa', 'P2', PRE_D, ['Tab 1 mở danh sách.', 'Tab 2 xóa phiếu 061.', 'Tab 1 bấm Xóa > Xóa ở dòng 061.'], '—',
       ['Máy chủ báo không tìm thấy bản ghi; bảng nạp lại thì phiếu không còn.'], 138)
S5.add('Dữ liệu liên quan: phiếu yêu cầu về Chờ duyệt', 'P0', PRE_D, ['Xóa phiếu 061.', 'Mở màn Yêu cầu, xem phiếu 070.'], '—',
       ['Phiếu 070 về Chờ duyệt, lại có nút Hạch toán; lịch sử phiếu 070 ghi "Đang hạch toán sang Chờ duyệt".'], 141)
S5.add('Người khác không xóa được', 'P0', [ACC_K2, DRAFT_K], ['K2 dùng công cụ kiểm thử API gọi xóa phiếu 061.'], '—',
       ['"Bạn không có quyền xóa phiếu này".'], 297)
S5.add('Lịch sử xóa', 'P2', 'Đã xóa ở TC_05.003.', ['Kiểm bảng lịch sử của phiếu (công cụ kiểm thử API).'], '—', ['Có mốc "Xóa" kèm dòng dịch vụ.'], 141)

# ============================================================== VI. LỊCH SỬ THAY ĐỔI
S6 = Sec(6)
HIS = [MENU, 'Ở dòng 060 bấm Lịch sử.']
S6.add('Mở cửa sổ lịch sử', 'P0', DONE, HIS, '—', ['Cửa sổ "Lịch sử thay đổi: TPE.HTMDV.2026000060".'], 162)
S6.add('Thông tin mỗi mốc', 'P1', DONE, HIS, '—',
       ['Mỗi mốc: nhãn hành động có màu, thời gian dd/mm/yyyy hh:mm, "Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ", nội dung.'],
       [163, 165, 166, 167])
S6.add('Mới nhất trước', 'P0', DONE, HIS, '—', ['Mốc 23/10/2026 10:19 "Thay đổi trạng thái" trên cùng, "Tạo mới" 10:17 dưới cùng.'], 164)
S6.add('Nội dung thay đổi', 'P0', DONE, HIS, '—',
       ['"Nhà cung cấp: ANH DƯƠNG sang ANH SỸ", "Tài khoản nợ: 1282 (Trái phiếu) sang 128", "Thuế VAT (%): 11.57 sang 11.58", "Dòng dịch vụ '
        'sửa thông tin" (SL hạch toán 10 sang 6; Đơn giá 11,000 sang 1,106.67).'], 168)
S6.add('Lọc theo hành động', 'P1', DONE, HIS + ['Bấm Bộ lọc, chọn Loại hành động = Thay đổi trạng thái.'], '—', ['Chỉ còn mốc trạng thái.'], [169, 175])
S6.add('Lọc theo người thực hiện', 'P1', DONE, HIS + ['Bấm Bộ lọc, chọn Người thực hiện = DNS Admin.'], '—', ['Chỉ mốc của người đó.'], 170)
S6.add('Lọc theo thời gian', 'P1', DONE, HIS + ['Bấm Bộ lọc, Từ ngày 23/10/2026, Đến ngày 23/10/2026.'], '—', ['Hiện cả 4 mốc.'], 171)
S6.add('Kết hợp lọc / không có kết quả', 'P2', DONE, HIS + ['Chọn hành động Tạo mới và ngày 01/01/2026.'], '—',
       ['"Không có lịch sử phù hợp bộ lọc."'], [172, 173])
S6.add('Làm mới bộ lọc lịch sử', 'P2', 'Đang lọc ở TC_06.008.', ['Bấm Làm mới.'], '—', ['Ô lọc trống, hiện lại 4 mốc.'], 174)
S6.add('Ghi nhận Tạo mới', 'P0', 'Vừa lưu nháp phiếu mới.', ['Mở Lịch sử.'], '—', ['Mốc "Tạo mới".'], 176)
S6.add('Ghi nhận sửa một trường', 'P0', 'Vừa sửa Diễn giải phiếu nháp.', ['Mở Lịch sử.'], '—', ['"Diễn giải: cũ sang mới".'], 177)
S6.add('Ghi nhận sửa nhiều trường cùng lúc', 'P1', 'Vừa sửa NCC, Hóa đơn VAT, SL.', ['Mở Lịch sử.'], '—',
       ['1 mốc "Thay đổi thông tin" liệt kê đủ các trường.'], [178, 183])
S6.add('Không ghi khi không đổi', 'P1', 'Mở Sửa, không đổi, Lưu nháp.', ['Mở Lịch sử.'], '—', ['Không thêm mốc.'], 182)
S6.add('Ghi nhận Lưu và duyệt', 'P0', DONE, HIS, '—', ['"Trạng thái: Đang tạo sang Đã duyệt" ở mốc "Thay đổi trạng thái".'], 183)
S6.add('Phiếu chưa có lịch sử', 'P2', 'Phiếu TPE.HTMDV.2025000001 tạo trên ERP trước khi bật lịch sử.', [MENU, 'Mở Lịch sử phiếu đó.'], '—',
       ['"Chưa có lịch sử thao tác nào."'], 173)
S6.add('Đóng cửa sổ lịch sử', 'P1', DONE, HIS + ['Bấm Đóng / (x) / ra ngoài.'], '—', ['Cửa sổ đóng.'], 184)
S6.add('Trạng thái danh sách sau đóng', 'P1', [DONE, 'Đang ở trang 2, lọc Đã duyệt.'], ['Ở trang 2 bấm Lịch sử 1 dòng.', 'Đóng cửa sổ.'],
       '—', ['Vẫn trang 2, giữ bộ lọc, sắp xếp.'], 185)
S6.add('Lịch sử ở màn chi tiết', 'P1', DONE, ['Mở chi tiết 060, bấm Xem lịch sử.'], '—', ['Cùng nội dung cửa sổ; nút đổi thành Thu gọn.'], 162)
S6.add('Bấm tên file trong lịch sử', 'P2', 'Phiếu có mốc "File đính kèm thêm mới" ghi sau 15/10/2026.', ['Mở Lịch sử, bấm tên file.'], '—',
       ['Mở xem trước file.'], 168)

# ============================================================== VII. XEM CHI TIẾT
S7 = Sec(7)
DET = [MENU, 'Bấm số phiếu TPE.HTMDV.2026000060.']
S7.add('Mở màn chi tiết', 'P0', [PRE_LIST, DONE], DET, '—', ['Mở TRANG chi tiết (không phải cửa sổ).'], 186)
S7.add('Tiêu đề', 'P1', [PRE_LIST, DONE], DET, '—', ['"Chi tiết hạch toán mua dịch vụ: TPE.HTMDV.2026000060".'], 187)
S7.add('Đầy đủ trường', 'P0', [PRE_LIST, DONE], DET, '—',
       ['Thông tin chung, File đính kèm (5 file), Chi tiết (không có cột SL yêu cầu), 3 dòng tổng, khối Hạch toán, khối Lịch sử.'], 188)
S7.add('Khớp dữ liệu tạo và danh sách', 'P0', [PRE_LIST, DONE], DET, '—',
       ['Phiếu yêu cầu 068, HĐ TPE.HDMDV-92-EWEW, NCC 50TPHPTA-749 (ANH SỸ), Tổng thanh toán 7,408.93, người tạo, ngày tạo khớp dòng '
        'ở danh sách.'], [189, 190])
S7.add('Khối Hạch toán', 'P0', [PRE_LIST, DONE], DET + ['Kéo xuống khối Hạch toán.'], '—',
       ['3 bút toán: Nợ 128 = 6,640.02; Nợ 1331 = 768.91; Có 35232 = 7,408.93 (đối tượng 50TPHPTA-749 ANH SỸ).',
        'Dòng Tổng cộng Nợ = Có = 7,408.93, khớp Tổng thanh toán.'], 188)
S7.add('Trường chỉ đọc, không có nút lưu', 'P0', [PRE_LIST, DONE], DET, '—', ['Mọi ô xám chỉ đọc; không có Lưu nháp / Lưu và duyệt.'], [191, 192])
S7.add('Nút theo trạng thái — phiếu Đang tạo', 'P0', [ACC_K, DRAFT_K], ['Đăng nhập K.', MENU, 'Mở chi tiết 061.'], '—',
       ['Chân màn: Sửa, In phiếu, Xóa, Quay lại; không có khối Hạch toán.'], 193)
S7.add('Phiếu Đã duyệt chỉ xem', 'P1', [PRE_LIST, DONE], DET, '—', ['Chân màn chỉ In phiếu, Quay lại.'], 194)
S7.add('Khu vực lịch sử', 'P1', [PRE_LIST, DONE], DET + ['Bấm Xem lịch sử.'], '—', ['Mở khối, hiện 4 mốc; bấm Thu gọn đóng lại.'], 195)
S7.add('Quay lại danh sách', 'P1', [PRE_LIST, DONE], DET + ['Bấm Quay lại.'], '—', ['Về danh sách.'], 196)
S7.add('Giữ bộ lọc khi quay lại', 'P1', 'Đang lọc Trạng thái = Đã duyệt, ở trang 2.', ['Bấm số phiếu ở trang 2.', 'Bấm Quay lại.'], '—',
       ['Danh sách vẫn lọc Đã duyệt (trong 10 phút).'], 197)
S7.add('Mở chi tiết ngoài phạm vi', 'P0', [ACC_B, DONE], ['B mở thẳng đường dẫn chi tiết phiếu 060.'], '—',
       ['Chuyển sang trang không tìm thấy; không lộ dữ liệu.'], [186, 296])
S7.add('Link chứng từ ở chi tiết', 'P2', [PRE_LIST, DONE], DET + ['Bấm Phiếu yêu cầu.', 'Bấm số yêu cầu TPE.YCMDV.2026000107.'], '—',
       ['Phiếu yêu cầu mở màn chi tiết ở tab mới.', 'Yêu cầu mua dịch vụ mở màn chi tiết ở tab mới.'], 188)

# ============================================================== VIII. TÙY CHỈNH CỘT
S8 = Sec(8)
COL = [MENU, 'Bấm nút biểu tượng cột (Cấu hình cột hiển thị).']
COL_PRE = [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.']
S8.add('Mở cửa sổ', 'P0', COL_PRE, COL, '—', ['Cửa sổ "Tuỳ chỉnh cột".'], 198)
S8.add('Danh sách cột', 'P0', COL_PRE, COL, '—', ['Liệt kê 14 cột đúng thứ tự trên bảng.'], 199)
S8.add('Cột chọn mặc định', 'P1', COL_PRE, COL, '—', ['Tích đủ 14/14.'], 200)
S8.add('Ẩn cột', 'P0', COL_PRE, COL + ['Bỏ tích Người cập nhật, Lưu.'], '—', ['"Cập nhật thành công"; bảng mất cột Người cập nhật.'], [202, 206])
S8.add('Hiện lại cột đã ẩn', 'P0', 'Đã ẩn Người cập nhật.', COL + ['Tích Người cập nhật, Lưu.'], '—', ['Cột hiện lại.'], 201)
S8.add('Cột bắt buộc không ẩn', 'P0', COL_PRE, COL + ['Thử bỏ tích STT, Số phiếu, Hành động.'], '—',
       ['Ô tích xám, không bỏ được; di chuột "Cột bắt buộc — không thể ẩn hoặc đổi vị trí".'], [203, 205])
S8.add('Kéo thả thứ tự', 'P1', COL_PRE, COL + ['Kéo Trạng thái lên sau Số phiếu, Lưu.'], '—', ['Trạng thái đứng ngay sau Số phiếu.'], 204)
S8.add('Đóng không lưu', 'P1', COL_PRE, COL + ['Bỏ tích Người tạo, bấm Đóng.'], '—', ['Bảng giữ cột Người tạo; mở lại vẫn tích.'], 207)
S8.add('Ghi nhớ sau F5', 'P1', 'Đã ẩn Người cập nhật.', ['Nhấn F5.'], '—', ['Vẫn ẩn Người cập nhật.'], 208)
S8.add('Theo tài khoản', 'P1', 'K đã ẩn Người cập nhật.', ['Đăng nhập B trên cùng trình duyệt, mở màn.', 'K đăng nhập trình duyệt khác.'], '—',
       ['B thấy đủ cột.', 'K ở trình duyệt khác vẫn ẩn Người cập nhật.'], 209)
S8.add('Không ảnh hưởng dữ liệu và lọc', 'P1', 'Đang lọc Đã duyệt, 59 phiếu.', COL + ['Ẩn 3 cột, Lưu.'], '—',
       ['Vẫn 59 phiếu, bộ lọc giữ.'], [210, 211])
S8.add('Chọn tất cả / Bỏ chọn hết', 'P2', COL_PRE, COL + ['Bấm Bỏ chọn hết.', 'Bấm Chọn tất cả.'], '—',
       ['Bỏ chọn hết: chỉ còn 3 cột khóa.', 'Chọn tất cả: 14/14.'], 199)

# ============================================================== IX. XUẤT EXCEL
S9 = Sec(9)
EXP = [MENU, 'Bấm Xuất Excel.']
S9.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, EXP, '—', ['Cửa sổ "Chọn trường xuất file".'], 212)
S9.add('Danh sách trường', 'P0', PRE_LIST, EXP, '—',
       ['12 trường: Số phiếu, Loại yêu cầu, Phiếu yêu cầu, Số hợp đồng, Nhà cung cấp, Tổng thanh toán, Người tạo, Ngày tạo, Ngày hạch '
        'toán, Người cập nhật, Ngày cập nhật, Trạng thái.'], 213)
S9.add('Trường chọn mặc định theo cột đang hiện', 'P1', 'Đã ẩn cột Người cập nhật.', EXP, '—',
       ['Người cập nhật bỏ tích; còn lại tích; "Đang chọn 11/12 trường".'], 214)
S9.add('Xuất với trường mặc định', 'P0', PRE_LIST, EXP + ['Bấm Xuất file.'], '—',
       ['"Xuất Excel thành công."; tải danh_sach_hach_toan_mua_dich_vu.xlsx.'], [215, 223])
S9.add('Xuất tất cả trường', 'P1', PRE_LIST, EXP + ['Bấm Chọn tất cả, Xuất file.'], '—', ['File có STT + 12 cột.'], 216)
S9.add('Xuất một số trường, đổi thứ tự', 'P0', PRE_LIST, EXP + ['Bỏ chọn hết, tích Số phiếu, Trạng thái, Tổng thanh toán; kéo Trạng thái lên đầu.',
       'Xuất file.'], '—', ['File: STT, Trạng thái, Số phiếu, Tổng thanh toán đúng thứ tự.'], [217, 226])
S9.add('Không chọn trường nào', 'P1', PRE_LIST, EXP + ['Bấm Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S9.add('Xuất theo tìm kiếm', 'P0', PRE_LIST, [MENU, 'Tìm "HDMDV-92".', 'Xuất Excel, Xuất file.'], '—', ['File chỉ có phiếu 060.'], 219)
S9.add('Xuất theo bộ lọc', 'P0', PRE_LIST, [MENU, ADV, 'Lọc Trạng thái = Đã duyệt.', 'Xuất Excel, Xuất file.'], '—',
       ['File có đúng 59 phiếu Đã duyệt.'], 220)
S9.add('Xuất nhiều trang', 'P0', PRE_LIST, [MENU, 'Đang ở trang 1 (10 dòng), Xuất file.'], '—', ['File có đủ 60 dòng, không riêng trang đang xem.'], [221, 227])
S9.add('Danh sách rỗng', 'P1', PRE_LIST, [MENU, 'Tìm "ZZZ999".', 'Xuất Excel, Xuất file.'], '—',
       ['Vẫn tải file: logo, tiêu đề, hàng tên cột, không có dòng dữ liệu.'], 222)
S9.add('Định dạng file', 'P1', 'Đã tải file ở TC_09.004.', ['Mở file bằng Excel.'], '—', ['File .xlsx mở được, không cảnh báo hỏng.'], 224)
S9.add('Tiêu đề cột và cấu trúc', 'P1', 'File của TC_09.004.', ['Quan sát 3 dòng đầu.'], '—',
       ['Dòng 1 logo công ty; dòng 2 "Danh sách hạch toán mua dịch vụ"; dòng 3 STT + tên cột đúng nhãn.'], 225)
S9.add('Dữ liệu khớp màn hình', 'P0', 'File của TC_09.004.', ['So 5 dòng với màn hình.'], '—',
       ['Số phiếu, NCC, Tổng thanh toán, trạng thái khớp; thứ tự dòng theo sắp xếp đang áp.'], 228)
S9.add('Định dạng ngày / số / chữ', 'P1', 'File của TC_09.004; có hợp đồng số toàn chữ số (vd 1812000).', ['Kiểm cột Tổng thanh toán, Ngày tạo, '
       'Số hợp đồng.'], '—', ['Tổng thanh toán là ô số, SUM được; ngày dd/mm/yyyy hh:mm.',
                              'Số phiếu / Phiếu yêu cầu / Số hợp đồng là ô chữ, căn trái, giữ số 0 đầu.'], 229)
S9.add('Tiếng Việt và ký tự đặc biệt', 'P1', 'Có phiếu NCC "CÔNG TY TNHH ĐIỆN VÀ PHÒNG CHÁY CHỮA CHÁY THÀNH ANH".', ['Xuất, mở file.'], '—',
       ['Hiển thị đúng dấu tiếng Việt, ký tự đặc biệt; chuỗi bắt đầu "=" không thành công thức.'], 230)
S9.add('Phạm vi quyền khi xuất', 'P0', [ACC_K, 'K tạo 2 phiếu, không có quyền xem theo cấp.'], ['Đăng nhập K, Xuất Excel tất cả.'], '—',
       ['File chỉ 2 phiếu của K.'], [220, 293])
S9.add('Đóng cửa sổ không xuất', 'P2', PRE_LIST, EXP + ['Bấm Đóng.'], '—', ['Không tải file.'], 212)

# ============================================================== X. ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU
S10 = Sec(10)
S10.add('Lập phiếu khi phiếu yêu cầu chưa có dòng dịch vụ', 'P1', [ACC_K, 'Phiếu yêu cầu 073 Chờ duyệt loại Dịch vụ thuê ngoài không có dòng '
        'dịch vụ.'], TAO + ['Chọn phiếu 073, chọn TK nợ, bấm Lưu và duyệt.'], '—',
        ['Bảng Chi tiết hiện "Chọn phiếu yêu cầu để nạp danh sách dịch vụ."; báo "Danh sách dịch vụ – Phiếu yêu cầu chưa có dòng dịch vụ nào".'],
        268)
S10.add('Lập phiếu khi phiếu yêu cầu có dòng dịch vụ', 'P0', PRE_FORM, TAO_YC, '—',
        ['Nạp dịch vụ "Chi phí đi lại", yêu cầu TPE.YCMDV.2026000108, SL yêu cầu 20.'], 269)
S10.add('Không xóa khi đã ghi sổ', 'P0', DONE, [MENU, 'Quan sát dòng 060.'], '—', ['Không có Xóa.'], 270)
S10.add('Không mất liên kết khi sửa', 'P1', [ACC_K, DRAFT_K], ['Sửa Diễn giải phiếu 061.', 'Mở chi tiết.'], '—',
        ['Phiếu yêu cầu, hợp đồng, yêu cầu mua dịch vụ, link vẫn đúng.'], 272)
S10.add('Phiếu yêu cầu Chờ duyệt xuất hiện ở màn này', 'P0', [ACC_K, WAIT], TAO + ['Bấm ô Phiếu yêu cầu.'], '—',
        ['Có phiếu 069 trong cửa sổ chọn.', 'Ở màn Yêu cầu, dòng 069 có nút Hạch toán mở màn Tạo chọn sẵn 069.'], 274)
S10.add('Đổi thông tin đồng bộ', 'P1', [ACC_K, DRAFT_K], ['Sửa Diễn giải phiếu 061.', 'Xem chi tiết, bản in.'], '—',
        ['Diễn giải mới hiện đồng bộ ở chi tiết và bản in.'], 278)
S10.add('Số phiếu không đổi, liên kết giữ nguyên', 'P2', DONE, ['Mở chi tiết phiếu yêu cầu 068.'], '—',
        ['Phiếu 068 Đã hạch toán; lịch sử phiếu 068 có mốc "Từ phiếu hạch toán mua dịch vụ".'], 279)
S10.add('Xóa đồng bộ', 'P1', [ACC_K, DRAFT_K], ['Xóa phiếu 061.', 'Mở cửa sổ chọn phiếu yêu cầu.'], '—',
        ['Phiếu 061 không còn; phiếu yêu cầu 070 chọn lại được (đã về Chờ duyệt).'], 280)
S10.add('Trạng thái phiếu yêu cầu tự cập nhật khi lưu nháp', 'P0', PRE_FORM, TAO_YC + ['Bấm Lưu nháp.', 'Mở màn Yêu cầu, xem phiếu 069.'], '—',
        ['Phiếu 069 thành Đang hạch toán; lịch sử ghi "Chờ duyệt sang Đang hạch toán" kèm "Từ phiếu hạch toán mua dịch vụ".'], 281)
S10.add('Trạng thái phiếu yêu cầu tự cập nhật khi duyệt', 'P0', PRE_FORM, TAO_YC + ['Chọn TK nợ 128, Lưu và duyệt > Duyệt.',
        'Mở màn Yêu cầu, xem phiếu 069.'], '—', ['Phiếu 069 Đã hạch toán, Người duyệt = K, Ngày duyệt = thời điểm duyệt.'], [281, 306])
S10.add('Bộ lọc màn liên quan cập nhật', 'P2', 'Phiếu 069 vừa Đã hạch toán.', ['Ở màn Yêu cầu lọc Trạng thái = Chờ duyệt.'], '—',
        ['Phiếu 069 không còn trong kết quả; lọc Đã hạch toán thì có.'], 282)
S10.add('Dòng phải thuộc phiếu yêu cầu cha', 'P1', 'Công cụ kiểm thử API.', ['Gửi lưu phiếu với id dòng dịch vụ của phiếu yêu cầu khác.'], '—',
        ['"Dịch vụ – Không thuộc phiếu yêu cầu đã chọn"; không lưu.'], 283)
S10.add('Tham chiếu không mất khi đổi trạng thái', 'P1', [ACC_K, DRAFT_K], ['Sửa phiếu 061, Lưu và duyệt > Duyệt.', 'Mở chi tiết.'], '—',
        ['Phiếu yêu cầu, dòng dịch vụ, file vẫn đủ; thêm khối Hạch toán.'], 284)
S10.add('Không có bản ghi mồ côi', 'P2', 'Đã xóa phiếu 061.', ['Kiểm dữ liệu dòng dịch vụ / yêu cầu của phiếu 061 (công cụ kiểm thử API).'],
        '—', ['Không còn dòng nào của phiếu 061.'], 285)
S10.add('Không có dữ liệu trùng: 1 phiếu yêu cầu 1 phiếu hạch toán', 'P0', 'Phiếu 069 đã có phiếu hạch toán nháp.',
        ['Dùng công cụ kiểm thử API gửi lưu phiếu mới với phiếu yêu cầu 069.'], '—',
        ['"Phiếu yêu cầu – Không ở trạng thái Chờ duyệt hoặc bạn không có quyền hạch toán phiếu này."; không tạo phiếu thứ 2.'], 286)
S10.add('Duyệt cộng SL đã hạch toán vào hợp đồng', 'P1', PRE_FORM, TAO_YC + ['Chọn TK nợ 128, Lưu và duyệt > Duyệt.',
        'Mở hợp đồng TPE.HDMDV-91 trên ERP.'], '—', ['SL đã hạch toán của dòng phân bổ tăng thêm 20.'], [274, 307])
S10.add('Bút toán xuất hiện ở sổ kế toán', 'P1', 'Đã duyệt ở TC_10.010.', ['Mở sổ chi tiết tài khoản 128 trên ERP, lọc số phiếu vừa duyệt.'],
        '—', ['Có bút toán Nợ 128 = 444,440 với số phiếu, ngày hạch toán của phiếu.'], 274)

# ============================================================== XI. PHÂN QUYỀN
S11 = Sec(11)
S11.add('Không có quyền xem chỉ thấy phiếu mình tạo', 'P0', [ACC_K, 'K tạo 2 phiếu; hệ thống có 60 phiếu.'], ['Đăng nhập K.', MENU], '—',
        ['"Hiển thị 1–2 / 2"; không có ô Công ty, Phòng ban.'], [287, 299])
S11.add('Xem - theo tổng công ty', 'P1', 'Tài khoản C.', ['Đăng nhập C.', MENU, ADV], '—', ['Thấy phiếu mọi công ty (trừ nháp người khác); có ô Công ty.'],
        [287, 299])
S11.add('Xem - theo công ty', 'P0', 'Tài khoản D thuộc công ty 1.', ['Đăng nhập D.', MENU], '—', ['Chỉ phiếu công ty 1.'], [287, 299])
S11.add('Xem - theo phòng ban', 'P1', 'Tài khoản E quản lý phòng Kế toán.', ['Đăng nhập E.', MENU], '—', ['Chỉ phiếu phòng Kế toán.'], [287, 299])
S11.add('Nháp của người khác luôn ẩn', 'P0', [DRAFT_K, 'Tài khoản C.'], ['Đăng nhập C.', MENU, ADV, 'Lọc Đang tạo.'], '—',
        ['Không thấy phiếu 061.'], [287, 299])
S11.add('Xem chi tiết theo quyền', 'P0', [ACC_B, DONE, 'Tài khoản D thuộc công ty 1 (công ty của phiếu 060).'],
        ['B mở đường dẫn chi tiết 060.', 'D mở chi tiết 060.'], '—', ['B: trang không tìm thấy.', 'D: xem được.'], 288)
S11.add('Thêm mới cần quyền Hạch toán mua dịch vụ', 'P0', [ACC_B, ACC_K], ['Đăng nhập B, mở màn.', 'Đăng nhập K, mở màn.'], '—',
        ['B không có nút Tạo mới.', 'K có nút Tạo mới, mở được màn Tạo.'], [289, 295])
S11.add('Super admin chưa gán quyền Hạch toán', 'P1', 'DNS Admin chưa được gán quyền Hạch toán mua dịch vụ.', [MENU], '—',
        ['Thấy mọi phiếu nhưng không có nút Tạo mới.'], [289, 295])
S11.add('URL trực tiếp màn Tạo khi thiếu quyền', 'P1', ACC_B, ['B mở thẳng đường dẫn màn Tạo phiếu.', 'Bấm ô Phiếu yêu cầu.'], '—',
        ['Danh mục tài khoản / cửa sổ chọn không tải được; bấm lưu bị máy chủ từ chối "Bạn không có quyền thực hiện chức năng này".'], 296)
S11.add('Sửa / Xóa chỉ người tạo', 'P0', [ACC_K2, DRAFT_K], ['K2 (có quyền Hạch toán) xem phiếu 061 của K.'], '—',
        ['K2 không thấy phiếu 061 (nháp người khác); gọi API sửa / xóa sang "Bạn không có quyền sửa phiếu này" / "Bạn không có quyền xóa '
         'phiếu này".'], [290, 291, 297])
S11.add('Xem lịch sử, In, Xuất Excel không gắn quyền', 'P1', [ACC_B, 'B tạo 1 phiếu trước khi bị gỡ quyền Hạch toán.'],
        ['Đăng nhập B, mở Lịch sử, In, Xuất Excel phiếu mình.'], '—', ['Dùng được cả 3.'], [293, 294])
S11.add('Không có Import / Khóa', 'P2', PRE_LIST, [MENU], '—', ['Không có nút Import, Khóa / Mở khóa.'], [292, 293])
S11.add('URL trực tiếp màn Sửa khi không đủ quyền', 'P0', [ACC_K2, DRAFT_K], ['K2 mở đường dẫn màn Sửa phiếu 061.'], '—',
        ['Phiếu nháp người khác: trang không tìm thấy.'], 296)
S11.add('API lưu khi thiếu quyền Hạch toán', 'P0', [ACC_B, WAIT], ['B dùng công cụ kiểm thử API gửi lưu phiếu từ phiếu yêu cầu 069.'], '—',
        ['"Bạn không có quyền thực hiện chức năng này"; không tạo phiếu.'], 297)
S11.add('API in phiếu ngoài phạm vi', 'P1', [ACC_B, DONE], ['B gọi dữ liệu in phiếu 060.'], '—', ['"Bạn không có quyền xem phiếu này".'], 297)
S11.add('Đổi quyền giữa thao tác', 'P1', PRE_FORM, TAO_YC + ['Quản trị gỡ quyền Hạch toán mua dịch vụ của K.', 'K bấm Lưu nháp.'],
        '—', ['"Bạn không có quyền thực hiện chức năng này"; không lưu.', 'Tải lại danh sách thì không còn nút Tạo mới.'], 298)
S11.add('Phiếu yêu cầu khác công ty', 'P1', [ACC_K, 'Phiếu yêu cầu 074 Chờ duyệt của công ty 2.'],
        ['Dùng công cụ kiểm thử API gọi dữ liệu phiếu yêu cầu 074 cho màn Tạo.'], '—',
        ['"Phiếu yêu cầu – Không ở trạng thái Chờ duyệt hoặc bạn không có quyền hạch toán phiếu này."'], [297, 299])

# ============================================================== XII. DUYỆT PHIẾU (LƯU VÀ DUYỆT)
S12 = Sec(12)
S12.add('Điều kiện hiển thị nút Lưu và duyệt', 'P0', [ACC_K, DRAFT_K, DONE], ['K mở màn Tạo.', 'K mở màn Sửa phiếu 061.', 'Mở chi tiết 060.'],
        '—', ['Màn Tạo và màn Sửa có Lưu và duyệt; màn chi tiết phiếu Đã duyệt không có.',
              'Màn không có nút "Duyệt" / "Không duyệt" riêng: Lưu và duyệt chính là duyệt.'], 300)
S12.add('Giao diện hộp xác nhận duyệt', 'P0', PRE_FORM, TAO_YC + ['Chọn TK nợ 128, bấm Lưu và duyệt.'], '—',
        ['Hộp "Xác nhận duyệt": "Phiếu đã duyệt sẽ ghi sổ kế toán và không sửa, xóa được nữa. Thao tác này có thể ảnh hưởng đến dữ '
         'liệu. Bạn có muốn tiếp tục?" (Duyệt / Hủy).'], 301)
S12.add('Duyệt thành công', 'P0', 'Đang ở hộp TC_12.002.', ['Bấm Duyệt.'], '—',
        ['"Duyệt thành công."; phiếu mới Đã duyệt, Ngày hạch toán = thời điểm duyệt.'], [302, 305])
S12.add('Dữ liệu bắt buộc trước khi duyệt', 'P0', PRE_FORM, TAO_YC + ['Để trống TK nợ, bấm Lưu và duyệt.'], '—',
        ['"Bạn chưa nhập đầy đủ thông tin."; "Tài khoản nợ – Bắt buộc phải nhập"; không mở hộp xác nhận.'], 303)
S12.add('Điều kiện nghiệp vụ: phiếu yêu cầu đã đổi trạng thái', 'P0', [ACC_K, WAIT],
        ['Tab 1 K mở màn Tạo từ phiếu 069.', 'Tab 2 ở màn Yêu cầu, kế toán khác Không duyệt phiếu 069.', 'Tab 1 Lưu và duyệt > Duyệt.'], '—',
        ['"Phiếu yêu cầu – Không ở trạng thái Chờ duyệt hoặc bạn không có quyền hạch toán phiếu này."; không ghi sổ.'], 304)
S12.add('Bút toán sinh ra sau duyệt', 'P0', 'Đã duyệt ở TC_12.003 (Kèm hóa đơn VAT 10%, Thành tiền 444,440, TK nợ 128, TK có 3311).',
        ['Mở chi tiết phiếu, xem khối Hạch toán.'], '—',
        ['Nợ 128 = 444,440; Nợ 1331 = 44,444; Có 3311 = 488,884 (đối tượng NCC); Tổng cộng Nợ = Có.'], 306)
S12.add('Ảnh hưởng hợp đồng, phiếu yêu cầu', 'P1', 'Đã duyệt ở TC_12.003.', ['Mở phiếu yêu cầu 069.', 'Mở hợp đồng TPE.HDMDV-91 trên ERP.'], '—',
        ['Phiếu 069 Đã hạch toán.', 'SL đã hạch toán của hợp đồng tăng 20.'], 307)
S12.add('Duyệt phiếu Công nợ bảo hiểm', 'P1', [ACC_K, 'Phiếu yêu cầu 075 Chờ duyệt loại Công nợ bảo hiểm, đơn DBH-001, Tổng sau thuế 5,500,000.'],
        TAO + ['Chọn phiếu 075, chọn Mã phí, Vụ việc, Lưu và duyệt > Duyệt.'], '—',
        ['TK nợ 1541 / TK có 3311 cố định; bút toán Nợ 1541 = Có 3311 = 5,500,000 kèm Mã phí, Vụ việc.', 'Đơn DBH-001 chuyển Đã hạch toán.'],
        [302, 307])
S12.add('Thông báo sau khi duyệt', 'P2', 'Đã duyệt ở TC_12.003.', ['Người tạo phiếu yêu cầu 069 mở chuông thông báo.'], '—',
        ['Không có thông báo (màn không gửi thông báo khi duyệt).', 'Lưu ý: ghi nhận nếu nghiệp vụ cần báo người tạo.'], [308, 309])
S12.add('Hủy thao tác duyệt', 'P0', 'Đang ở hộp TC_12.002.', ['Bấm Hủy.'], '—', ['Không lưu; form giữ nguyên dữ liệu; phiếu 069 vẫn Chờ duyệt.'], 310)
S12.add('Không duyệt lại phiếu đã xử lý', 'P0', DONE, ['Mở chi tiết 060.', 'Dùng công cụ kiểm thử API gửi sửa phiếu 060 với Lưu và duyệt.'],
        '—', ['Không có nút Sửa / Lưu và duyệt.', 'Máy chủ trả "Trạng thái đã bị thay đổi. Vui lòng load lại trang".'], 311)
S12.add('Lịch sử và người duyệt', 'P1', 'Đã duyệt ở TC_12.003.', ['Mở Lịch sử phiếu.', 'Mở Lịch sử phiếu yêu cầu 069.'], '—',
        ['Phiếu: mốc "Tạo mới" của K.', 'Phiếu 069: mốc "Thay đổi trạng thái" kèm "Từ phiếu hạch toán mua dịch vụ"; Người duyệt K, Ngày duyệt.'],
        312)
S12.add('Ghi sổ thất bại thì không lưu gì', 'P2', [PRE_FORM, 'Tài khoản 128 bị cấu hình không cho ghi sổ.'],
        TAO_YC + ['Chọn TK nợ 128, Lưu và duyệt > Duyệt.'], '—',
        ['Báo "Tài khoản nợ – <lý do>"; không tạo phiếu; phiếu 069 vẫn Chờ duyệt.', 'Lưu ý: chưa xác minh được câu lỗi cụ thể trên dev.'], 304)

# ============================================================== XIII. IN PHIẾU VÀ IN DANH SÁCH
S13 = Sec(13)
S13.add('In phiếu từ danh sách', 'P0', [PRE_LIST, DONE], [MENU, 'Ở dòng 060 bấm In phiếu.'], '—',
        ['Cửa sổ "Xem trước phiếu hạch toán mua dịch vụ" ngay trên màn.',
         'Bản in: "PHIẾU HẠCH TOÁN MUA DỊCH VỤ", số phiếu, ngày lập 23/10/2026, loại, Hóa đơn VAT, phiếu yêu cầu, TK nợ, TK có, NCC, hợp '
         'đồng, Diễn giải, bảng dịch vụ, 3 dòng tổng (7,408.93).'])
S13.add('Letterhead theo công ty ghi trên phiếu', 'P0', 'Tài khoản C thuộc công ty 2; phiếu 060 công ty 1.', ['C in phiếu 060.'], '—',
        ['Letterhead công ty 1, không phải công ty 2.'])
S13.add('In phiếu từ màn chi tiết', 'P1', [PRE_LIST, DONE], ['Mở chi tiết 060, bấm In phiếu.'], '—', ['Cùng bản in như từ danh sách.'])
S13.add('In và đóng cửa sổ', 'P2', 'Đang ở cửa sổ xem trước.', ['Bấm In.', 'Đóng hộp in, bấm (x).'], '—', ['Mở hộp thoại in; (x) đóng cửa sổ.'])
S13.add('Số tiền giữ số lẻ trên bản in', 'P1', DONE, ['In phiếu 060.'], '—', ['Đơn giá 1,106.67; Tổng thanh toán 7,408.93 (không làm tròn).'])
S13.add('In danh sách theo bộ lọc', 'P1', PRE_LIST, [MENU, 'Lọc Đã duyệt.', 'Bấm In danh sách.'], '—',
        ['Cửa sổ "Xem trước danh sách hạch toán mua dịch vụ" chỉ có 59 phiếu Đã duyệt.'])
S13.add('In danh sách vượt 2.000 dòng', 'P2', 'Phạm vi có hơn 2.000 phiếu.', ['Bấm In danh sách không lọc.'], '—',
        ['Báo vượt mức in tối đa 2.000 dòng, nhắc thu hẹp bộ lọc; không hiện bản in.'])

# ============================================================== XIV. CHỌN PHIẾU YÊU CẦU
S14 = Sec(14)
S14.add('Cửa sổ Chọn phiếu yêu cầu', 'P0', PRE_FORM, TAO + ['Bấm ô Phiếu yêu cầu.'], '—',
        ['Cửa sổ "Chọn phiếu yêu cầu hạch toán mua dịch vụ": ô Mã phiếu, Tìm kiếm, Làm mới; cột STT, Mã phiếu, Ngày tạo; 10 dòng/trang.',
         'Chỉ phiếu Chờ duyệt do K tạo (có 069).'])
S14.add('Không có phiếu nào', 'P1', [ACC_K2, 'K2 không tạo phiếu yêu cầu Chờ duyệt nào.'], ['K2 Tạo mới, bấm ô Phiếu yêu cầu.'], '—',
        ['"Không có phiếu yêu cầu hạch toán Chờ duyệt nào do bạn tạo."'])
S14.add('Tìm và sắp xếp trong cửa sổ', 'P1', PRE_FORM, TAO + ['Mở cửa sổ, nhập "069", Enter.', 'Bấm tiêu đề Ngày tạo.'], '—',
        ['Ra TPE.YCHTMDV.2026000069.', 'Sắp theo ngày tạo.'])
S14.add('Bấm link mã phiếu không chọn dòng', 'P1', PRE_FORM, TAO + ['Mở cửa sổ, bấm link TPE.YCHTMDV.2026000069.'], '—',
        ['Mở màn chi tiết phiếu yêu cầu ở tab mới; cửa sổ vẫn mở, chưa chọn.'])
S14.add('Chọn phiếu nạp dữ liệu', 'P0', PRE_FORM, TAO + ['Bấm dòng 069 (ô Ngày tạo).'], '—',
        ['Cửa sổ đóng; điền đủ dữ liệu như TC_03.006; file kế thừa có cột Dung lượng.'])
S14.add('Đổi phiếu yêu cầu', 'P1', [ACC_K, WAIT, 'K có thêm phiếu yêu cầu 076 Chờ duyệt.'],
        TAO + ['Chọn 069, thêm file hoadon.pdf.', 'Mở lại cửa sổ, chọn 076.'], '—',
        ['Dữ liệu theo 076; file của 069 được thay bằng file của 076; giữ hoadon.pdf.'])
S14.add('Đóng cửa sổ không chọn', 'P2', PRE_FORM, TAO + ['Mở cửa sổ, bấm Đóng (hoặc (x) / ra ngoài).'], '—', ['Ô giữ nguyên trống.'])
S14.add('Làm mới trong cửa sổ', 'P2', PRE_FORM, TAO + ['Mở cửa sổ, nhập "999", Tìm kiếm, bấm Làm mới.'], '—',
        ['Xóa điều kiện, hiện lại đủ phiếu.'])

SECTIONS = [
    ('I', 'HIỂN THỊ DANH SÁCH VÀ TRUY CẬP', S1),
    ('II', 'TÌM KIẾM VÀ LỌC', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'CHỈNH SỬA', S4),
    ('V', 'XÓA', S5),
    ('VI', 'LỊCH SỬ THAY ĐỔI', S6),
    ('VII', 'XEM CHI TIẾT', S7),
    ('VIII', 'TÙY CHỈNH CỘT', S8),
    ('IX', 'XUẤT EXCEL', S9),
    ('X', 'ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU', S10),
    ('XI', 'PHÂN QUYỀN', S11),
    ('XII', 'DUYỆT PHIẾU (LƯU VÀ DUYỆT)', S12),
    ('XIII', 'IN PHIẾU VÀ IN DANH SÁCH', S13),
    ('XIV', 'CHỌN PHIẾU YÊU CẦU HẠCH TOÁN', S14),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
check_no_dash_pre(SECTIONS, [])

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1', feature_name='Hạch toán mua dịch vụ - Cập nhật ngày 03/11/2026',
          module_name='Hạch toán mua dịch vụ', description_block=DESCRIPTION_BLOCK, role_tcs=[], sections=SECTIONS)
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.0f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))

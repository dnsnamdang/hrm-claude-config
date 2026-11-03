# -*- coding: utf-8 -*-
"""Testcase màn "Yêu cầu hạch toán mua dịch vụ" — skill testcase-documenter (tc_engine). Bản đầu 03/11/2026.

Chạy: python gen_testcase.py -> testcase.xlsx
Section xếp đúng thứ tự + tên nhóm của checklist "Mẫu tài liệu.xlsx" (../phieu-theo-form-quoc-gia/checklist_mau_tai_lieu.json),
bỏ nhóm Khóa/Mở khóa, Import (màn không có); rồi phần riêng (XIV In, XV Chọn hợp đồng / đơn bảo hiểm). Chỉ 1 nhóm Phân quyền
(role_tcs=[]); Cài đặt bộ lọc nằm trong nhóm Tìm kiếm và lọc (tiền tố "Cài đặt bộ lọc:").
Mỗi case ghi kèm stt checklist nó phủ (tham số ck) sang gen_checklist.py đọc CK để dựng bảng đối chiếu.
Nguồn hành vi (đọc 03/11/2026, nhánh develop cả 2 repo): FE pages/finance/buy-service-accounting-requests/**,
  buy-service-requests/components/CommentModal.vue, bill-payment-requests/components/AttachmentSection.vue, V2BaseDataTable,
  filterStateMixin, unsavedChangesMixin, saveAndContinueMixin, plugins/axios.js; BE Modules/Finance BuyServiceAccountingRequest
  (Entity searchByFilter / canView / canEdit / canAccounting), Service (store / update / reject / destroy / availableQty / fillHeader),
  StoreRequest / RejectRequest, NotifyService, BuyServiceAccountingService (đổi trạng thái phiếu yêu cầu), CatalogHistoryService.
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
MENU = 'Vào phân hệ Bán hàng > menu "Yêu cầu" > nhóm "Mua dịch vụ" > bấm "YC hạch toán mua dịch vụ".'
MENU_TC = ('Vào phân hệ Tài chính > menu "Hàng hoá - Dịch vụ - Vận chuyển" > nhóm "Mua dịch vụ" > bấm '
           '"Yêu cầu hạch toán mua dịch vụ".')
TAO = [MENU, 'Bấm "Tạo mới".']
ADV = 'Bấm Tìm kiếm nâng cao.'

ACC_A = ('Tài khoản A: nhân viên Kinh doanh công ty 1, không có quyền xem theo cấp, không có quyền Hạch toán mua dịch vụ.')
ACC_B = 'Tài khoản B: nhân viên khác cùng công ty 1, không có quyền nào của màn.'
ACC_K = 'Tài khoản K: có quyền Hạch toán mua dịch vụ, thuộc công ty 1.'
ACC_K2 = 'Tài khoản K2: có quyền Hạch toán mua dịch vụ, thuộc công ty 2.'
HD = ('A là người tạo hợp đồng mua dịch vụ TPE.HDMDV-91 đã duyệt, NCC "20TTHPGI-27 – A HẢI", VAT 10%, 1 dịch vụ "Chi phí đi lại" '
      'đơn giá 22,222, phân bổ SL 20 cho yêu cầu TPE.YCMDV.2026000108, chưa phiếu nào giữ (SL HĐ còn lại 20).')
PRE_LIST = 'Tài khoản DNS Admin (Super admin); trong phạm vi xem có 65 phiếu đủ 5 trạng thái, cả 2 loại yêu cầu.'
PRE_FORM = ACC_A + '\n' + HD + '\nTrên máy có file hoadon.pdf (1MB).'
DRAFT_A = ('A có phiếu TPE.YCHTMDV.2026000101 Đang tạo, loại Dịch vụ thuê ngoài, HĐ TPE.HDMDV-91, SL hạch toán 5, Không kèm hóa đơn, '
           'Diễn giải "Đi lại T10".')
REJ_A = ('A có phiếu TPE.YCHTMDV.2026000102 Không duyệt (Ghi chú duyệt "Sai SL"), loại Dịch vụ thuê ngoài, HĐ TPE.HDMDV-91, SL 5.')
WAIT = ('Phiếu TPE.YCHTMDV.2026000069 Chờ duyệt do A tạo, công ty 1, loại Dịch vụ thuê ngoài, HĐ TPE.HDMDV-91, SL 20, Tổng '
        'thanh toán 444,440.')

CK = defaultdict(list)       # stt checklist Testcase -> [TC ID]
SEC = {}                     # tên biến section -> số thứ tự section


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
     'Màn Yêu cầu hạch toán mua dịch vụ dùng để nhân viên đề nghị kế toán hạch toán chi phí mua dịch vụ.\n'
     'Loại Dịch vụ thuê ngoài lập từ hợp đồng mua dịch vụ đã duyệt do mình tạo (chỉ nhập SL hạch toán); loại Công nợ bảo hiểm lập '
     'từ đơn bảo hiểm. Người tạo Lưu nháp (Đang tạo) hoặc Lưu và gửi duyệt (Chờ duyệt). Kế toán có quyền Hạch toán mua dịch vụ: '
     'Không duyệt (phiếu thành Không duyệt kèm Ghi chú duyệt) hoặc Hạch toán (lập phiếu Hạch toán mua dịch vụ: lưu nháp sang Đang hạch '
     'toán, duyệt sang Đã hạch toán).'),
    ('2. Đối tượng được tính / hiển thị',
     '- 2 loại yêu cầu: Dịch vụ thuê ngoài, Công nợ bảo hiểm.\n'
     '- Trạng thái: Đang tạo (xám), Chờ duyệt (vàng), Đang hạch toán (vàng), Đã hạch toán (xanh), Không duyệt (đỏ).\n'
     '- Danh sách: phiếu trong phạm vi quyền + phiếu Chờ duyệt cùng công ty cho người có quyền Hạch toán.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác: luôn ẩn ở mọi cấp quyền.\n'
     '- Không có Khóa / Mở khóa, không có Import Excel, không có màn chờ duyệt riêng.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo ngày tạo phiếu, lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Dịch vụ thuê ngoài: phiếu > dòng dịch vụ (theo hợp đồng) > dòng yêu cầu mua dịch vụ (SL hạch toán).\n'
     '- Công nợ bảo hiểm: phiếu gắn 1 đơn bảo hiểm (phụ lục, hợp đồng mua), không có dòng dịch vụ.\n'
     '- Mỗi phiếu có danh sách file đính kèm.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- SL HĐ còn lại = SL phân bổ trừ SL đã hạch toán trừ SL các phiếu Đang tạo / Chờ duyệt / Đang hạch toán khác đang giữ.\n'
     '- Số lượng dịch vụ = tổng SL hạch toán các yêu cầu; Thành tiền = SL × đơn giá; Tổng thanh toán = Thành tiền + VAT.\n'
     '- Không có trường duy nhất: 2 phiếu cùng hợp đồng đều lưu được nếu tổng SL không vượt hợp đồng.\n'
     '- Một đơn bảo hiểm chỉ một phiếu Chờ duyệt / Đang hạch toán / Đã hạch toán giữ.'),
    ('7. Phân quyền cấp',
     '- Xem yêu cầu hạch toán mua dịch vụ - theo tổng công ty.\n- Xem yêu cầu hạch toán mua dịch vụ - theo công ty.\n'
     '- Xem yêu cầu hạch toán mua dịch vụ - theo phòng ban.\n'
     '- Hạch toán mua dịch vụ: thấy phiếu Chờ duyệt cùng công ty, Hạch toán, Không duyệt, nhận thông báo gửi duyệt.\n'
     '- Lập phiếu, In, Xuất Excel, Lịch sử không gắn quyền riêng; Sửa / Xóa chỉ người tạo, phiếu Đang tạo / Không duyệt.'),
    ('8. Cách tính các ô thống kê',
     '- 3 dòng tổng của bảng dịch vụ: Thành tiền, VAT (x%), Tổng thanh toán.\n'
     '- Dòng "Hiển thị a–b / N": a–b là khoảng số thứ tự trang đang xem, N là tổng phiếu khớp bộ lọc trong phạm vi quyền.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: A (người lập, công ty 1, không quyền), B (nhân viên khác công ty 1), K (Hạch toán mua dịch vụ, '
     'công ty 1), K2 (Hạch toán mua dịch vụ, công ty 2), C (Xem - theo tổng công ty), D (Xem - theo công ty, công ty 1), E (Xem - '
     'theo phòng ban, quản lý phòng Kinh doanh 1), DNS Admin (Super admin).\n'
     '- Số tiền hiển thị dạng 1,234,567.89 (tối đa 2 số lẻ).\n'
     '- Lưu ý: Lưu nháp chỉ bắt buộc Loại yêu cầu; Lưu và gửi duyệt mới kiểm tra đủ.\n'
     '- Lưu ý: Màn Tạo / Sửa / Chi tiết là TRANG riêng, không phải cửa sổ nổi.\n'
     '- Các case "dùng công cụ kiểm thử API" dành cho tester kỹ thuật.'),
]

# ============================================================== I. HIỂN THỊ DANH SÁCH VÀ TRUY CẬP
SCREEN = ListScreen(menu=MENU, title='Yêu cầu hạch toán mua dịch vụ', total=65, quick_label='số phiếu, số hợp đồng, tên dịch vụ',
                    quick_sample='HDMDV-91', quick_hit='các phiếu của hợp đồng TPE.HDMDV-91',
                    filters=[('Trạng thái', 'Chờ duyệt'), ('Loại yêu cầu', 'Dịch vụ thuê ngoài')])
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Mở màn từ phân hệ Tài chính', 'P1', PRE_LIST, [MENU_TC, 'So tổng số với lối vào Bán hàng (TC_01.001).'], '—',
       ['Tiêu đề "Yêu cầu hạch toán mua dịch vụ", cùng tổng 65 phiếu, cùng thứ tự dòng.'], 1)
S1.add('Tiêu đề màn hình', 'P0', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Cả 3 nơi đều là "Yêu cầu hạch toán mua dịch vụ".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE_LIST, [MENU, 'Quan sát khối bộ lọc và thanh công cụ của bảng.'], '—',
       ['Khối bộ lọc: ô tìm nhanh (gợi ý "Tìm theo số phiếu, số hợp đồng, tên dịch vụ"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, '
        'Cài đặt bộ lọc.', 'Thanh công cụ: Tạo mới, Xuất Excel, In danh sách, nút biểu tượng cột (Cấu hình cột hiển thị).',
        'Không có nút Import, Khóa.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột từ trái sang phải.'],
       '—', ['Đúng 15 cột: STT, Số phiếu, Loại yêu cầu, Số hợp đồng, Nhà cung cấp, Tổng thanh toán, Ngày tạo, Người tạo, Người duyệt, '
             'Ngày duyệt, Người cập nhật, Ngày cập nhật, Diễn giải, Trạng thái, Hành động.', 'STT và Số phiếu ghim trái khi cuộn ngang.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" tích đủ 15/15 cột ("Đang chọn 15/15 cột").', 'Không có cột Công ty, Phòng ban trên màn.'], 5)
S1.add('Dữ liệu trên dòng khớp phiếu đã tạo', 'P0', [ACC_A, WAIT],
       ['Đăng nhập A.', MENU, 'Đối chiếu dòng TPE.YCHTMDV.2026000069.'], '—',
       ['Loại yêu cầu "Dịch vụ thuê ngoài"; Số hợp đồng TPE.HDMDV-91 (link); Nhà cung cấp "20TTHPGI-27 – A HẢI".',
        'Tổng thanh toán "444,440" căn phải; Ngày tạo dd/mm/yyyy hh:mm; Người tạo là A; Người duyệt, Ngày duyệt trống.',
        'Trạng thái nhãn vàng "Chờ duyệt".'], 6)
S1.add('Số hợp đồng mở ERP ở tab mới', 'P2', PRE_LIST, [MENU, 'Bấm số hợp đồng của 1 phiếu Dịch vụ thuê ngoài.'], '—',
       ['Mở hợp đồng mua dịch vụ trên ERP ở tab mới; danh sách giữ nguyên.'], 6)
S1.add('Nhãn trạng thái của phiếu', 'P0', 'Trong phạm vi xem có đủ 5 trạng thái.', [MENU, ADV, 'Lần lượt lọc Trạng thái từng giá trị.'],
       '—', ['Đang tạo: xám; Chờ duyệt: vàng; Đang hạch toán: vàng; Đã hạch toán: xanh; Không duyệt: đỏ.', 'Cột Trạng thái không sắp xếp.'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', 'Tài khoản N mới, không có quyền, chưa tạo phiếu.', ['Đăng nhập N.', MENU], '—',
       ['Bảng hiện "Không có dữ liệu phù hợp.".', 'Không báo lỗi, vẫn có nút Tạo mới.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'], 'Ô tìm nhanh: ZZZ999',
       ['Bảng hiện "Không có dữ liệu phù hợp.".'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 3.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 20 phiếu, tự về trang 1, "Hiển thị 1–20 / 65".', 'STT từ 1 đến 20.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–20 / 65".', 'Bước 3: "Hiển thị 1–10 / 65".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—',
       ['Bước 2: trang 7, "Hiển thị 61–65 / 65", 5 dòng.', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang cuối quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ, bấm không tác dụng.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2, rồi trang 3.'], '—', ['Trang 2: 11–20; trang 3: 21–30.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 4.', ADV, 'Chọn Trạng thái = Đã hạch toán.'],
       'Trạng thái: Đã hạch toán', ['Tự nạp lại ở trang 1; "Hiển thị 1–10 / <số phiếu Đã hạch toán>".'], 17)
S1.add('Sắp xếp tăng dần theo Tổng thanh toán', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Tổng thanh toán.'], '—',
       ['Xếp từ nhỏ đến lớn (phiếu loại bảo hiểm tính theo Tổng sau thuế), mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Tổng thanh toán', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Tổng thanh toán 2 lần.'], '—',
       ['Xếp từ lớn đến nhỏ, mũi tên xuống.'], 21)
S1.add('Sắp xếp theo Ngày tạo / Ngày cập nhật / Ngày duyệt / Số phiếu', 'P1', PRE_LIST,
       [MENU, 'Bấm tiêu đề Ngày tạo 2 lần.', 'Bấm tiêu đề Ngày cập nhật.', 'Bấm tiêu đề Ngày duyệt.'], '—',
       ['Ngày tạo: lần 1 cũ nhất trên, lần 2 mới nhất trên.', 'Ngày cập nhật xếp theo thời điểm lưu gần nhất.',
        'Ngày duyệt xếp đúng (phiếu chưa duyệt dồn về một phía); Số phiếu cũng sắp được.'], 22)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Loại yêu cầu, Số hợp đồng, Nhà cung cấp, Người tạo, Người duyệt, Người cập nhật, Diễn giải, Trạng thái.'],
       '—', ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Tổng thanh toán (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự tăng của trang 1.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 4.', 'Bấm tiêu đề Ngày duyệt.'], '—', ['Về trang 1.'], 25)
S1.raw([weird_param_case('%03d' % (len(S1) + 1), SCREEN, 'tiêu đề "Yêu cầu hạch toán mua dịch vụ", có nút Tạo mới')], [[1]])
S1.add('Mở danh sách "phiếu của tôi" bằng tham số', 'P2', [ACC_K, 'K có 2 phiếu tự tạo, công ty 1 có 3 phiếu Chờ duyệt của người khác.'],
       [MENU, 'Đổi tham số chế độ trên thanh địa chỉ thành "index".'], '—',
       ['Tiêu đề "Yêu cầu hạch toán mua dịch vụ của tôi"; chỉ 2 phiếu K tạo.'], 1)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM VÀ LỌC
S2 = Sec(2)
S2.add('Tìm theo số phiếu chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "TPE.YCHTMDV.2026000069", bấm Tìm kiếm.'],
       'Ô tìm nhanh: TPE.YCHTMDV.2026000069', ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần số phiếu / số hợp đồng / tên dịch vụ', 'P0', PRE_LIST,
       [MENU, 'Nhập "000069", bấm Tìm kiếm.', 'Nhập "HDMDV-91", bấm Tìm kiếm.', 'Nhập "đi lại", bấm Tìm kiếm.'],
       ['000069', 'HDMDV-91', 'đi lại'],
       ['Bước 2: ra phiếu 069.', 'Bước 3: ra mọi phiếu của hợp đồng TPE.HDMDV-91.', 'Bước 4: ra phiếu có dịch vụ "Chi phí đi lại".'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "tpe.ychtmdv.2026000069", bấm Tìm kiếm.'], '—',
       ['Ra phiếu 069 như khi gõ chữ hoa.'], 28)
S2.add('Có dấu / không dấu', 'P1', 'Có phiếu có dịch vụ "Chi phí đi lại".', [MENU, 'Nhập "chi phi di lai", bấm Tìm kiếm.'], '—',
       ['Ra phiếu có dịch vụ "Chi phí đi lại" nếu cơ sở dữ liệu so khớp không dấu; chữ "đ" khác "d".',
        'Lưu ý: so khớp theo cách so sánh chữ của cơ sở dữ liệu.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; ký tự % được hiểu là ký tự đại diện nên ra toàn bộ phiếu.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  000069  ", bấm Tìm kiếm.'], '—', ['Vẫn ra phiếu 069.'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "000069", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Sau bước 1 bảng chưa đổi.', 'Sau bước 2 hiện lại đủ 65 phiếu.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST, [MENU, 'Nhập "000069", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'],
       '—', ['Cả 2 cách đều ra phiếu 069, về trang 1.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['8 ô Công ty, Phòng ban, Loại yêu cầu, Trạng thái, Nhà cung cấp, Người duyệt, Người tạo, Ngày tạo đều trống.', 'Đủ 65 phiếu.'], 36)
S2.add('Lọc Loại yêu cầu', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Loại yêu cầu = Dịch vụ thuê ngoài.'], '—',
       ['Lọc ngay; mọi dòng là Dịch vụ thuê ngoài.'], 37)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Không duyệt.'], '—', ['Chỉ phiếu nhãn đỏ Không duyệt.'], 37)
S2.add('Lọc Nhà cung cấp', 'P0', 'Có 2 phiếu NCC "20TTHPGI-27 – A HẢI".', [MENU, ADV, 'Gõ "A" vào Nhà cung cấp.', 'Gõ "A HẢI", chọn.'],
       '—', ['Gõ 1 ký tự chưa tìm; từ 2 ký tự hiện tối đa 50 gợi ý.', 'Ra đúng 2 phiếu.'], 37)
S2.add('Lọc Người tạo, Người duyệt', 'P1', 'A tạo 3 phiếu; K đã Không duyệt 1 phiếu.', [MENU, ADV, 'Chọn Người tạo = A.',
       'Bỏ Người tạo, chọn Người duyệt = K.'], '—', ['Bước 3: 3 phiếu của A.', 'Bước 4: phiếu K đã xử lý.'], 37)
S2.add('Lọc Ngày tạo lấy trọn ngày biên', 'P0', 'Có phiếu tạo 23/10/2026 00:05 và 23:59.', [MENU, ADV, 'Chọn Ngày tạo 23/10/2026 – 23/10/2026.'],
       '—', ['Ra cả 2 phiếu.'], 37)
S2.add('Lọc Công ty, Phòng ban', 'P1', 'Tài khoản C (Xem - theo tổng công ty).', [MENU, ADV, 'Chọn Công ty = Công ty 2.', 'Chọn 1 phòng ban.'],
       '—', ['Chỉ phiếu của công ty 2, rồi của phòng ban đã chọn.'], 37)
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đã hạch toán.', 'Chọn Người tạo = Đào Phúc Sơn.'],
       '—', ['Chỉ phiếu thỏa cả 2 điều kiện.'], 38)
S2.add('Không có kết quả khi kết hợp', 'P1', PRE_LIST, [MENU, 'Nhập "000069", bấm Tìm kiếm.', ADV, 'Chọn Trạng thái = Đang tạo.'], '—',
       ['"Không có dữ liệu phù hợp." vì phiếu 069 đang Chờ duyệt.'], [39, 40])
S2.add('Tổng số và phân trang sau lọc', 'P0', 'Có 60 phiếu Đã hạch toán.', [MENU, ADV, 'Chọn Trạng thái = Đã hạch toán.', 'Bấm trang cuối.'],
       '—', ['"Hiển thị 1–10 / 60"; 6 trang.', 'Trang cuối "Hiển thị 51–60 / 60".'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang lọc Trạng thái = Đã hạch toán.', ['Bấm tiêu đề Tổng thanh toán.'], '—',
       ['Chỉ phiếu Đã hạch toán được sắp; bộ lọc giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "HDMDV", lọc Loại yêu cầu, Trạng thái, sắp Tổng thanh toán, ở trang 2.',
       ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống, bỏ sắp xếp, nạp lại trang 1, đủ 65 phiếu.'], 44)
S2.raw(org_cases(SCREEN, len(S2) + 1), [[37], [37], [37]])
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Loại yêu cầu = Dịch vụ thuê ngoài, chưa mở màn con nào.'],
       ['Nhấn F5.'], '—', ['Bộ lọc trở về trống, đủ 65 phiếu (bộ lọc chỉ nhớ khi đi vào màn chi tiết / sửa / tạo của màn).'], 46)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Người duyệt, bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công".', 'Khối Tìm kiếm nâng cao không còn ô Người duyệt.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Loại yêu cầu = Dịch vụ thuê ngoài.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Loại yêu cầu, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị xóa, nạp lại đủ phiếu.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn Người duyệt.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Người duyệt vẫn ẩn.', 'Bước 2: tích đủ 7 tiêu chí, Người duyệt hiện lại.'], 36)
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự', 'P2', PRE_LIST, ['Bấm Cài đặt bộ lọc, kéo Ngày tạo lên đầu, bấm Lưu.'], '—',
       ['Ô Ngày tạo đứng đầu khối Tìm kiếm nâng cao.'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo', 'P0', PRE_FORM, TAO, '—', ['Mở TRANG "Tạo phiếu yêu cầu hạch toán mua dịch vụ", tab cùng tiêu đề.'], 49)
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải "<tên A> – <ngày giờ hiện tại>"; không có nhãn trạng thái, không có ô Số phiếu.'], 50)
S3.add('Các trường, khối và nút loại Dịch vụ thuê ngoài', 'P0', PRE_FORM, TAO, '—',
       ['Khối Thông tin chung: Loại yêu cầu, Hợp đồng mua dịch vụ, Nhà cung cấp, Hóa đơn VAT, Diễn giải.',
        'Khối File đính kèm (nút Thêm tài liệu), khối Danh sách dịch vụ.', 'Chân màn: Lưu nháp, Lưu và gửi duyệt, Lưu và tiếp tục, Quay lại.'],
       [51, 54])
S3.add('Các trường loại Công nợ bảo hiểm', 'P1', PRE_FORM, TAO + ['Chọn Loại yêu cầu = Công nợ bảo hiểm.'], '—',
       ['Thông tin chung: Loại yêu cầu, Số đơn bảo hiểm, Phụ lục bổ sung, Số hợp đồng mua, Hóa đơn VAT, Ghi chú.',
        'Thêm 3 khối chỉ đọc: Thông tin công ty bảo hiểm, người liên hệ, người đại diện; bảng phí bảo hiểm.'], 51)
S3.add('Đánh dấu bắt buộc', 'P1', PRE_FORM, TAO, '—',
       ['Dấu * ở Loại yêu cầu, Hợp đồng mua dịch vụ, Nhà cung cấp, Hóa đơn VAT, tiêu đề Danh sách dịch vụ, cột SL hạch toán.',
        'Diễn giải không bắt buộc.'], 52)
S3.add('Giá trị mặc định', 'P1', PRE_FORM, TAO, '—',
       ['Loại yêu cầu = Dịch vụ thuê ngoài; Hóa đơn VAT trống; bảng dịch vụ hiện "Chọn hợp đồng mua dịch vụ để nạp danh sách dịch vụ.".'], 53)
S3.add('Lưu và gửi duyệt đầy đủ thông tin hợp lệ', 'P0', PRE_FORM,
       TAO + ['Chọn hợp đồng TPE.HDMDV-91.', 'Chọn Hóa đơn VAT = Kèm hóa đơn.', 'Bấm Thêm tài liệu, chọn hoadon.pdf.',
              'Nhập Diễn giải "Đi lại T10".', 'Bấm Lưu và gửi duyệt.'], 'SL hạch toán: 20 (tự điền)',
       ['Báo "Thêm mới thành công.", về danh sách.', 'Phiếu mới đứng đầu, nhãn Chờ duyệt, Tổng thanh toán 488,884 (444,440 + VAT 10%).'],
       [55, 86])
S3.add('Lưu nháp chỉ với trường bắt buộc', 'P0', PRE_FORM, TAO + ['Bấm Lưu nháp ngay.'], '—',
       ['Báo "Thêm mới thành công.", phiếu Đang tạo với hợp đồng, nhà cung cấp trống, Tổng thanh toán trống.'], [56, 79])
S3.add('Bỏ trống trường không bắt buộc', 'P1', PRE_FORM, TAO + ['Chọn hợp đồng, Hóa đơn VAT = Không kèm hóa đơn, để trống Diễn giải, không '
       'đính kèm.', 'Bấm Lưu và gửi duyệt.'], '—', ['Lưu thành công, Chờ duyệt; Không kèm hóa đơn nên không bắt buộc file.'], 57)
S3.add('Dữ liệu sau lưu', 'P0', 'Vừa lưu phiếu ở TC_03.007.', ['Bấm số phiếu mở chi tiết.'], '—',
       ['Số phiếu dạng TPE.YCHTMDV.2026xxxxxx; Hợp đồng, NCC, Hóa đơn VAT, Diễn giải, file, bảng dịch vụ (SL 20, đơn giá 22,222, Thành '
        'tiền 444,440, VAT 10% 44,444, Tổng 488,884) khớp lúc nhập.'], 58)
S3.add('Trạng thái mặc định', 'P0', PRE_FORM, TAO + ['Bấm Lưu nháp.', 'Tạo phiếu khác, bấm Lưu và gửi duyệt (đủ dữ liệu).'], '—',
       ['Lưu nháp sang Đang tạo.', 'Lưu và gửi duyệt sang Chờ duyệt.'], 59)
S3.add('Lịch sử tạo', 'P1', 'Vừa lưu phiếu ở TC_03.007.', ['Ở dòng phiếu, bấm "…" > Lịch sử.'], '—',
       ['Có mốc "Tạo mới" của A; tiếp theo không có mốc nào khác.'], 60)
S3.add('Thông báo cho kế toán khi gửi duyệt', 'P0', [PRE_FORM, ACC_K, ACC_K2], ['A lập phiếu và Lưu và gửi duyệt.', 'Đăng nhập K, mở chuông.',
       'Đăng nhập K2, mở chuông.'], '—', ['K nhận "[YCHTMDV] Chờ duyệt: <số phiếu>" kèm người gửi, loại, NCC, hợp đồng, tổng thanh toán.',
       'K2 (công ty 2) không nhận.', 'Bấm thông báo mở màn chi tiết phiếu.'], 86)
S3.add('Bỏ trống trường bắt buộc khi gửi duyệt', 'P0', PRE_FORM, TAO + ['Bấm Lưu và gửi duyệt khi chưa nhập gì.'], '—',
       ['Báo "Bạn chưa nhập đầy đủ thông tin."; không gửi máy chủ.', 'Dưới ô: "Hợp đồng mua dịch vụ – Bắt buộc phải nhập", "Nhà cung cấp – '
        'Bắt buộc phải nhập", "Hóa đơn VAT – Bắt buộc phải nhập"; viền đỏ; cuộn tới ô lỗi đầu.'], [61, 70, 87])
S3.add('Kèm hóa đơn mà chưa có file', 'P0', PRE_FORM, TAO + ['Chọn hợp đồng, Hóa đơn VAT = Kèm hóa đơn, không đính kèm.', 'Bấm Lưu và gửi duyệt.'],
       '—', ['Dưới khối File đính kèm: "File đính kèm – Bắt buộc khi kèm hóa đơn VAT".'], [61, 87])
S3.add('Sai định dạng: SL hạch toán âm hoặc vượt SL còn lại', 'P0', PRE_FORM,
       TAO + ['Chọn hợp đồng TPE.HDMDV-91.', 'Nhập SL hạch toán -1, bấm Lưu nháp.', 'Nhập 25, bấm Lưu nháp.'], ['-1', '25'],
       ['Bước 3: dưới ô "Không được âm".', 'Bước 4: "Không được vượt SL còn lại"; không lưu (áp cả khi lưu nháp).'], [62, 81, 88, 74])
S3.add('Sai định dạng: VAT (%) ngoài 0–100', 'P1', PRE_FORM, TAO + ['Chọn hợp đồng, Kèm hóa đơn.', 'Sửa VAT (%) thành 150, bấm Lưu nháp.'],
       'VAT: 150', ['"VAT (%) – Phải trong khoảng 0 đến 100".'], [62, 81])
S3.add('Ký tự đặc biệt ở Diễn giải', 'P2', PRE_FORM, TAO + ['Nhập Diễn giải "<b>Test</b> @#$%", bấm Lưu nháp.', 'Mở chi tiết.'], '—',
       ['Lưu được; hiển thị nguyên văn, không thực thi định dạng.'], 63)
S3.add('Diễn giải không có độ dài tối thiểu', 'P2', PRE_FORM, TAO + ['Nhập Diễn giải 1 ký tự "a", bấm Lưu nháp.'], '—', ['Lưu được.'], 64)
S3.add('Diễn giải đúng 1.000 ký tự', 'P1', PRE_FORM, TAO + ['Dán 1.000 ký tự vào Diễn giải, bấm Lưu nháp.'], '1.000 ký tự', ['Lưu được, giữ đủ.'], 65)
S3.add('Diễn giải vượt 1.000 ký tự', 'P1', PRE_FORM, TAO + ['Dán 1.050 ký tự vào Diễn giải.'], '1.050 ký tự',
       ['Ô chỉ nhận 1.000 ký tự đầu, phần thừa không gõ được.'], 66)
S3.add('Trùng dữ liệu: 2 phiếu cùng hợp đồng', 'P0', PRE_FORM,
       TAO + ['Chọn TPE.HDMDV-91, sửa SL hạch toán 10, Lưu nháp.', 'Tạo phiếu thứ 2 cùng hợp đồng, quan sát SL HĐ còn lại.', 'Nhập 10, Lưu nháp.'],
       '—', ['Bước 2: SL HĐ còn lại = 10.', 'Bước 3: lưu được, số phiếu khác phiếu 1 (không có trường duy nhất).'], [67, 82])
S3.add('Trùng: phiếu thứ 2 vượt phần còn lại', 'P0', 'Đã có phiếu nháp giữ 10/20 của TPE.HDMDV-91.',
       TAO + ['Chọn TPE.HDMDV-91, nhập SL 15, bấm Lưu và gửi duyệt.'], '15', ['"Không được vượt SL còn lại" tại ô SL; không lưu.'], [67, 89, 75])
S3.add('Khoảng trắng đầu / cuối Diễn giải', 'P2', PRE_FORM, TAO + ['Nhập "  Đi lại  ", Lưu nháp, mở chi tiết.'], '—',
       ['Lưu được; Diễn giải hiển thị không lỗi (khoảng trắng hai đầu được bỏ).', 'Lưu ý: nếu còn khoảng trắng thì ghi nhận theo quy tắc chung.'], 68)
S3.add('Diễn giải chỉ có khoảng trắng', 'P2', PRE_FORM, TAO + ['Nhập "   " vào Diễn giải, chọn đủ trường, Lưu và gửi duyệt.'], '—',
       ['Lưu được (Diễn giải không bắt buộc), Diễn giải coi như trống.'], 69)
S3.add('Lỗi biến mất sau khi sửa', 'P1', 'Đang ở TC_03.014 với 3 ô báo đỏ.', ['Chọn Hóa đơn VAT.'], '—',
       ['Lỗi dưới Hóa đơn VAT biến mất ngay; các ô khác vẫn đỏ.'], 71)
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, TAO + ['Chọn hợp đồng, Hóa đơn VAT, bấm Lưu và tiếp tục.'], '—',
       ['Báo "Thêm mới thành công."; vẫn ở màn Tạo, form trống như lúc mới vào.', 'Phiếu vừa lưu ở trạng thái Đang tạo.'], [72, 76, 77])
S3.add('Lưu và tiếp tục khi thiếu Loại yêu cầu', 'P1', PRE_FORM, TAO + ['Xóa Loại yêu cầu (×), bấm Lưu và tiếp tục.'], '—',
       ['"Loại yêu cầu – Bắt buộc phải nhập"; không lưu, ở lại form.'], 73)
S3.add('Lưu và tiếp tục sau đó rời màn', 'P2', 'Vừa Lưu và tiếp tục ở TC_03.026, form trống.', ['Bấm Quay lại.'], '—',
       ['Về danh sách ngay, không hỏi; danh sách có phiếu vừa lưu.'], 78)
S3.add('Lưu nháp thiếu Loại yêu cầu', 'P1', PRE_FORM, TAO + ['Xóa Loại yêu cầu, bấm Lưu nháp.'], '—', ['"Loại yêu cầu – Bắt buộc phải nhập".'], 80)
S3.add('Sau Lưu nháp chuyển về danh sách', 'P1', PRE_FORM, TAO + ['Bấm Lưu nháp.', 'Bấm Back của trình duyệt.'], '—',
       ['Sau lưu về danh sách (màn Tạo là trang).', 'Back không quay lại form vừa lưu.'], [83, 84, 85])
S3.add('Sau Lưu và gửi duyệt chuyển về danh sách', 'P1', PRE_FORM, TAO + ['Nhập đủ, bấm Lưu và gửi duyệt.'], '—',
       ['Về danh sách, phiếu mới ở đầu; mở Tạo mới lại thì form trống.'], [90, 91, 92])
S3.add('Rời màn khi chưa nhập', 'P1', PRE_FORM, TAO + ['Bấm Quay lại ngay.'], '—', ['Về danh sách, không hỏi.'], 93)
S3.add('Rời màn khi đã nhập', 'P0', PRE_FORM, TAO + ['Chọn hợp đồng.', 'Bấm Quay lại.'], '—',
       ['Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" (Thoát / Ở lại).'], 94)
S3.add('Rời màn bằng menu / đóng tab', 'P2', PRE_FORM, TAO + ['Chọn hợp đồng.', 'Bấm 1 mục menu khác.', 'Ở lại, nhấn F5.'], '—',
       ['Bước 3: hộp Thông tin chưa lưu (màn là trang, không có nút X).', 'Bước 4: hộp cảnh báo rời trang của trình duyệt.'], 95)
S3.add('Chọn Thoát', 'P1', 'Đang ở hộp Thông tin chưa lưu.', ['Bấm Thoát.'], '—', ['Về danh sách, không lưu phiếu.'], 96)
S3.add('Chọn Ở lại', 'P1', 'Đang ở hộp Thông tin chưa lưu.', ['Bấm Ở lại.'], '—', ['Đóng hộp, dữ liệu đã nhập giữ nguyên.'], 97)
S3.add('Nhập rồi xóa hết', 'P2', PRE_FORM, TAO + ['Nhập Diễn giải "abc" rồi xóa hết.', 'Bấm Quay lại.'], '—', ['Về danh sách, không hỏi.'], 98)
S3.add('Đổi rồi khôi phục ban đầu', 'P2', PRE_FORM, TAO + ['Chọn Công nợ bảo hiểm rồi chọn lại Dịch vụ thuê ngoài.', 'Bấm Quay lại.'], '—',
       ['Về danh sách, không hỏi (dữ liệu như lúc mở).'], 99)
S3.add('Không thao tác lâu', 'P2', PRE_FORM, TAO + ['Nhập dở, để yên 30 phút, bấm Lưu nháp.'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên, về màn đăng nhập, phiếu không lưu.'], 100)
S3.add('Bấm nút lưu liên tục', 'P0', PRE_FORM, TAO + ['Bấm Lưu nháp 3 lần liên tiếp.'], '—', ['Nút khóa khi đang lưu, chỉ tạo 1 phiếu.'], 101)
S3.add('Hai tab cùng lập phiếu một hợp đồng', 'P1', PRE_FORM,
       ['Mở 2 tab màn Tạo, cả 2 chọn TPE.HDMDV-91 (SL còn lại 20), để SL 20.', 'Tab 1 Lưu nháp.', 'Tab 2 Lưu nháp.'], '—',
       ['Tab 1 lưu được.', 'Tab 2 báo "Không được vượt SL còn lại" (máy chủ tính lại có khóa dòng hợp đồng).'], 102)
S3.add('Đổi Loại yêu cầu xóa dữ liệu loại cũ', 'P1', PRE_FORM, TAO + ['Chọn hợp đồng TPE.HDMDV-91.', 'Đổi Loại yêu cầu = Công nợ bảo hiểm.',
       'Đổi lại Dịch vụ thuê ngoài.'], '—', ['Không hỏi xác nhận; hợp đồng, NCC, bảng dịch vụ bị xóa.'], 51)
S3.add('Đổi Hóa đơn VAT tính lại VAT', 'P1', PRE_FORM, TAO + ['Chọn hợp đồng (VAT 10%).', 'Chọn Kèm hóa đơn.', 'Chọn Không kèm hóa đơn.'], '—',
       ['Kèm hóa đơn: hiện dòng VAT (%) = 10, Tổng 488,884.', 'Không kèm: ẩn dòng VAT, Tổng 444,440.'], 53)
S3.add('Lập phiếu loại Công nợ bảo hiểm', 'P0', [PRE_FORM, 'Có đơn bảo hiểm DBH-001 đã duyệt, phụ lục PL-001, hợp đồng mua HĐM-01, Tổng '
       'sau thuế 5,500,000.'], TAO + ['Chọn Công nợ bảo hiểm, chọn đơn DBH-001.', 'Chọn Không kèm hóa đơn, Lưu và gửi duyệt.'], '—',
       ['Phụ lục, Số hợp đồng mua, 3 khối bảo hiểm tự điền chỉ đọc.', 'Lưu Chờ duyệt, Tổng thanh toán 5,500,000; đơn DBH-001 không còn trong '
        'cửa sổ chọn đơn của phiếu khác.'], [55, 86])
S3.add('Đơn bảo hiểm đã bị phiếu khác giữ', 'P1', 'DBH-001 đang được phiếu Chờ duyệt khác giữ (2 tab mở trước khi gửi).',
       ['Tab 2 chọn DBH-001 từ trước, bấm Lưu và gửi duyệt.'], '—',
       ['"Số đơn bảo hiểm – Đơn không hợp lệ hoặc đã có yêu cầu hạch toán khác."; không lưu.'], 89)
S3.add('Gửi duyệt khi tổng SL hạch toán bằng 0', 'P1', PRE_FORM, TAO + ['Chọn hợp đồng, sửa SL = 0, Không kèm hóa đơn, Lưu và gửi duyệt.'],
       '0', ['"Vui lòng nhập SL hạch toán trước khi gửi duyệt."'], 87)
S3.add('File sai định dạng / quá 20MB', 'P1', PRE_FORM, TAO + ['Thêm tài liệu, chọn file .exe.', 'Chọn file 21MB.'], '—',
       ['"File "<tên>" không thuộc định dạng cho phép".', '"File "<tên>" vượt quá 20MB"; file không được thêm.'], 62)

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
EDIT = [MENU, 'Ở dòng TPE.YCHTMDV.2026000101 bấm Sửa (bút chì).']
PRE_E = [ACC_A, DRAFT_A]
S4.add('Mở màn Sửa', 'P0', PRE_E, EDIT, '—', ['Mở TRANG "Sửa phiếu yêu cầu hạch toán mua dịch vụ: TPE.YCHTMDV.2026000101".'], 103)
S4.add('Dữ liệu điền sẵn đúng', 'P0', PRE_E, EDIT, '—',
       ['Hợp đồng TPE.HDMDV-91, NCC A HẢI, Không kèm hóa đơn, Diễn giải "Đi lại T10", SL 5; SL HĐ còn lại 20 (không trừ phần phiếu này giữ).'], 104)
S4.add('Trường được / không được sửa', 'P0', PRE_E, EDIT, '—',
       ['Loại yêu cầu bị khóa; dòng người tạo, các ô theo hợp đồng chỉ đọc.', 'Sửa được hợp đồng, NCC, Hóa đơn VAT, Diễn giải, SL, file.'], 105)
S4.add('Các nút màn Sửa', 'P1', PRE_E, EDIT, '—', ['Có Lưu nháp, Lưu và gửi duyệt, Quay lại; KHÔNG có Lưu và tiếp tục.'], 106)
S4.add('Sửa một trường', 'P0', PRE_E, EDIT + ['Sửa Diễn giải "Đi lại T11", bấm Lưu nháp.'], '—', ['"Cập nhật thành công.", về danh sách, Diễn giải mới.'], 107)
S4.add('Sửa nhiều trường', 'P0', PRE_E, EDIT + ['Sửa SL 8, Kèm hóa đơn + file, Diễn giải mới, Lưu nháp.'], '—',
       ['Lưu đủ 3 thay đổi; Tổng thanh toán tính lại.'], 108)
S4.add('Giữ nguyên giá trị khi lưu không đổi', 'P1', PRE_E, EDIT + ['Không sửa gì, bấm Lưu nháp.'], '—', ['Lưu được, dữ liệu giữ nguyên.'], 109)
S4.add('Dữ liệu sau lưu', 'P0', 'Đã sửa ở TC_04.006.', ['Mở chi tiết phiếu.'], '—', ['SL 8, VAT, file, Diễn giải mới khớp.'], 110)
S4.add('Ngày / người cập nhật', 'P0', 'Đã sửa ở TC_04.005.', [MENU, 'Quan sát cột Người cập nhật, Ngày cập nhật của phiếu.'], '—',
       ['Người cập nhật = A, Ngày cập nhật = thời điểm lưu.'], 111)
S4.add('Lịch sử sửa', 'P0', 'Đã sửa ở TC_04.006.', ['Mở Lịch sử của phiếu.'], '—',
       ['Mốc "Thay đổi thông tin" ghi cũ sang mới: Hóa đơn VAT, Thuế VAT (%), Diễn giải, "Dòng dịch vụ thêm mới / đã xóa", "File đính kèm thêm mới".'], 112)
S4.add('Sửa phiếu Không duyệt rồi gửi duyệt lại', 'P0', [ACC_A, REJ_A], [MENU, 'Sửa phiếu 102: SL 6, bấm Lưu và gửi duyệt.'], '—',
       ['Phiếu Chờ duyệt; lịch sử có "Thay đổi thông tin" và "Thay đổi trạng thái" Không duyệt sang Chờ duyệt; kế toán K nhận thông báo.'], [112, 107])
S4.add('Bỏ trống bắt buộc khi gửi duyệt', 'P0', PRE_E, EDIT + ['Bấm × ở Hợp đồng mua dịch vụ, bấm Lưu và gửi duyệt.'], '—',
       ['"Hợp đồng mua dịch vụ – Bắt buộc phải nhập", "Nhà cung cấp – Bắt buộc phải nhập"; không lưu.'], 113)
S4.add('Sai định dạng SL', 'P0', PRE_E, EDIT + ['Nhập SL -2, Lưu nháp.'], '-2', ['"Không được âm".'], 114)
S4.add('Vượt giới hạn SL / Diễn giải', 'P1', PRE_E, EDIT + ['Nhập SL 21, Lưu nháp.', 'Dán 1.050 ký tự vào Diễn giải.'], '—',
       ['"Không được vượt SL còn lại".', 'Diễn giải chỉ nhận 1.000 ký tự.'], 115)
S4.add('Trùng với phiếu khác cùng hợp đồng', 'P0', [ACC_A, DRAFT_A, 'Phiếu 103 của A (Đang tạo) giữ 12 của TPE.HDMDV-91.'],
       EDIT + ['Quan sát SL HĐ còn lại.', 'Nhập SL 9, Lưu nháp.'], '—',
       ['SL HĐ còn lại = 8 (20 trừ 12, không trừ 5 của chính phiếu).', '"Không được vượt SL còn lại".'], [116])
S4.add('Không tính trùng chính phiếu', 'P1', PRE_E, EDIT + ['Giữ SL 5, Lưu nháp.'], '—', ['Lưu được (phần 5 của chính phiếu không bị trừ).'], 116)
S4.add('Thông báo lỗi', 'P1', PRE_E, EDIT + ['Bấm × Hợp đồng, bấm Lưu và gửi duyệt.'], '—',
       ['"Bạn chưa nhập đầy đủ thông tin."; lỗi đỏ dưới ô; cuộn tới ô lỗi đầu.'], 117)
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P1', 'Đang ở TC_04.017.', ['Chọn lại hợp đồng TPE.HDMDV-91.'], '—', ['Lỗi Hợp đồng, NCC biến mất.'], 118)
S4.add('Mở không thay đổi rồi rời', 'P1', PRE_E, EDIT + ['Bấm Quay lại.'], '—', ['Về danh sách, không hỏi.'], 119)
S4.add('Đổi rồi trả về ban đầu', 'P2', PRE_E, EDIT + ['Sửa Diễn giải rồi gõ lại đúng như cũ.', 'Bấm Quay lại.'], '—', ['Không hỏi.'], 120)
S4.add('Rời màn khi đã đổi', 'P0', PRE_E, EDIT + ['Sửa SL 7.', 'Bấm Quay lại.'], '—', ['Hộp "Thông tin chưa lưu".'], 121)
S4.add('Xác nhận Thoát', 'P1', 'Đang ở hộp của TC_04.021.', ['Bấm Thoát.'], '—', ['Về danh sách; phiếu vẫn SL 5.'], [122, 124])
S4.add('Xác nhận Ở lại', 'P1', 'Đang ở hộp của TC_04.021.', ['Bấm Ở lại.'], '—', ['Ở lại form, SL 7 giữ nguyên.'], 123)
S4.add('Không ghi lịch sử khi không thay đổi', 'P1', 'Đã làm TC_04.007.', ['Mở Lịch sử phiếu 101.'], '—',
       ['Không có mốc mới cho lần lưu không đổi.'], 125)
S4.add('Phiếu đã gửi duyệt không sửa được', 'P0', [ACC_A, WAIT], [MENU, 'Quan sát cột Hành động dòng 069.',
       'Mở thẳng đường dẫn màn Sửa của phiếu 069.'], '—', ['Không có nút Sửa.', 'Tự chuyển sang màn chi tiết.'], [126, 295])
S4.add('Phiếu bị người khác xóa khi đang sửa', 'P2', PRE_E, ['Tab 1 mở màn Sửa phiếu 101.', 'Tab 2 xóa phiếu 101.', 'Tab 1 bấm Lưu nháp.'], '—',
       ['Báo lỗi chung "Item Not Found!", không lưu.'], 127)
S4.add('Hai tab cùng sửa', 'P1', PRE_E, ['Tab 1 và tab 2 mở Sửa phiếu 101.', 'Tab 1 Lưu và gửi duyệt.', 'Tab 2 Lưu nháp.'], '—',
       ['Tab 2 báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang", không lưu.'], 128)
S4.add('Phiếu đã có phiếu hạch toán', 'P1', 'Phiếu 068 Đã hạch toán.', [MENU, 'Quan sát dòng 068.'], '—',
       ['Không có Sửa / Xóa; chỉ In phiếu, Lịch sử.'], 129)
S4.add('Gỡ file đã lưu khi sửa', 'P1', [ACC_A, DRAFT_A + ' Có 1 file hoadon.pdf.'], EDIT + ['Bấm Xóa ở dòng file, bấm Xóa trong hộp xác nhận.'],
       '—', ['Hộp "Bạn có chắc muốn xóa file đính kèm này?"; xóa xong báo "Xóa file thành công", có hiệu lực ngay.',
             'Lịch sử có "File đính kèm đã xóa".'], 112)

# ============================================================== V. XÓA
S5 = Sec(5)
PRE_D = [ACC_A, DRAFT_A]
S5.add('Nút Xóa', 'P0', [ACC_A, DRAFT_A, WAIT], ['Đăng nhập A.', MENU, 'Quan sát cột Hành động phiếu 101 và 069.'], '—',
       ['Phiếu 101: có Xóa (đỏ).', 'Phiếu 069: không có Xóa.'], 130)
S5.add('Hộp xác nhận', 'P0', PRE_D, [MENU, 'Bấm Xóa ở dòng 101.', 'Ở màn chi tiết bấm Xóa.'], '—',
       ['Bước 2 mở màn chi tiết phiếu.', 'Bước 3: hộp "Xác nhận xóa" nội dung "Bạn có chắc muốn xóa bản ghi này không?", nút Xóa / Hủy.'],
       [131, 132])
S5.add('Xóa phiếu không ràng buộc', 'P0', PRE_D, ['Ở hộp xác nhận bấm Xóa.'], '—',
       ['"Xóa thành công.", về danh sách; phiếu 101 không còn; tổng giảm 1.'], [133, 139, 140])
S5.add('Hủy xóa', 'P1', PRE_D, ['Mở hộp xác nhận, bấm Hủy.', 'Mở lại, bấm (x).'], '—', ['Phiếu giữ nguyên.'], 134)
S5.add('Xóa phiếu đang sử dụng', 'P0', 'Phiếu 068 Đã hạch toán; dùng công cụ kiểm thử API.', ['Gọi xóa phiếu 068.'], '—',
       ['Máy chủ trả "Trạng thái đã bị thay đổi. Vui lòng load lại trang", không xóa.'], 135)
S5.add('Xóa có dữ liệu cấp con', 'P1', [ACC_A, DRAFT_A + ' 1 dịch vụ, 1 yêu cầu.'], ['Xóa phiếu 101.', 'Lập phiếu mới chọn TPE.HDMDV-91.'], '—',
       ['Dòng dịch vụ / yêu cầu xóa theo.', 'SL HĐ còn lại trở về 20 (SL đã được trả).'], [136, 141])
S5.add('Phiếu đã bị người khác xóa', 'P2', PRE_D, ['Tab 1 mở chi tiết 101.', 'Tab 2 xóa phiếu 101.', 'Tab 1 bấm Xóa > Xóa.'], '—',
       ['Báo lỗi chung "Item Not Found!".'], 138)
S5.add('Xóa phiếu Không duyệt', 'P1', [ACC_A, REJ_A], ['Mở chi tiết 102, bấm Xóa > Xóa.'], '—', ['Xóa được.'], 133)
S5.add('Người khác không xóa được', 'P0', [ACC_B, DRAFT_A], ['B dùng công cụ kiểm thử API gọi xóa phiếu 101.'], '—',
       ['"Bạn không có quyền xóa phiếu này".'], [297])
S5.add('Lịch sử xóa', 'P2', 'Đã xóa ở TC_05.003.', ['Kiểm bảng lịch sử của phiếu (công cụ kiểm thử API).'], '—', ['Có mốc "Xóa" kèm dòng dịch vụ.'], 141)

# ============================================================== VI. LỊCH SỬ THAY ĐỔI
S6 = Sec(6)
HPRE = 'Phiếu TPE.YCHTMDV.2026000068 có 11 mốc (Tạo mới, Thay đổi thông tin, Thay đổi trạng thái gửi duyệt / Không duyệt / hạch toán).'
HIS = [MENU, 'Ở dòng 068 bấm Lịch sử.']
S6.add('Mở cửa sổ lịch sử', 'P0', HPRE, HIS, '—', ['Cửa sổ "Lịch sử thay đổi: TPE.YCHTMDV.2026000068".'], 162)
S6.add('Thông tin mỗi mốc', 'P1', HPRE, HIS, '—', ['Mỗi mốc: nhãn hành động có màu, thời gian dd/mm/yyyy hh:mm, "Người thực hiện: <tên> — <phòng ban>", nội dung.'],
       [163, 165, 166, 167])
S6.add('Mới nhất trước', 'P0', HPRE, HIS, '—', ['Mốc 23/10/2026 10:19 (Đã hạch toán) trên cùng.'], 164)
S6.add('Nội dung thay đổi', 'P0', HPRE, HIS, '—',
       ['"Hợp đồng mua dịch vụ: A sang B", "Nhà cung cấp: cũ sang mới", "Dòng dịch vụ thêm mới / đã xóa" kèm Yêu cầu, SL hạch toán, Đơn giá.'], 168)
S6.add('Lọc theo hành động', 'P1', HPRE, HIS + ['Bấm Bộ lọc, chọn Loại hành động = Thay đổi trạng thái.'], '—', ['Chỉ còn mốc trạng thái.'], [169, 175])
S6.add('Lọc theo người thực hiện', 'P1', HPRE, HIS + ['Bấm Bộ lọc, chọn Người thực hiện.'], '—', ['Chỉ mốc của người đó.'], 170)
S6.add('Lọc theo thời gian', 'P1', HPRE, HIS + ['Bấm Bộ lọc, Từ ngày 23/10/2026, Đến ngày 23/10/2026.'], '—', ['Chỉ mốc trong ngày.'], 171)
S6.add('Kết hợp lọc / không có kết quả', 'P2', HPRE, HIS + ['Chọn hành động Xóa và ngày 01/01/2026.'], '—',
       ['"Không có lịch sử phù hợp bộ lọc."'], [172, 173])
S6.add('Làm mới bộ lọc lịch sử', 'P2', 'Đang lọc ở TC_06.007.', ['Bấm Làm mới.'], '—', ['Ô lọc trống, hiện lại 11 mốc.'], 174)
S6.add('Ghi nhận Tạo mới', 'P0', 'Vừa tạo phiếu mới.', ['Mở Lịch sử.'], '—', ['Mốc "Tạo mới".'], 176)
S6.add('Ghi nhận sửa một trường', 'P0', 'Vừa sửa Diễn giải phiếu nháp.', ['Mở Lịch sử.'], '—', ['"Diễn giải: cũ sang mới".'], 177)
S6.add('Ghi nhận sửa nhiều trường cùng lúc', 'P1', 'Vừa sửa NCC, Hóa đơn VAT, SL.', ['Mở Lịch sử.'], '—',
       ['1 mốc "Thay đổi thông tin" liệt kê đủ các trường.'], [178, 183])
S6.add('Không ghi khi không đổi', 'P1', 'Mở Sửa, không đổi, Lưu nháp.', ['Mở Lịch sử.'], '—', ['Không thêm mốc.'], 182)
S6.add('Ghi nhận Không duyệt và hạch toán', 'P0', HPRE, HIS, '—',
       ['"Trạng thái: Chờ duyệt sang Không duyệt" kèm ghi chú; "Chờ duyệt sang Đang hạch toán", "Đang hạch toán sang Đã hạch toán" kèm "Từ phiếu hạch '
        'toán mua dịch vụ".'], 183)
S6.add('Phiếu chưa có lịch sử', 'P2', 'Phiếu 067 tạo trên ERP trước khi bật lịch sử.', [MENU, 'Mở Lịch sử phiếu 067.'], '—',
       ['"Chưa có lịch sử thao tác nào."'], 173)
S6.add('Đóng cửa sổ lịch sử', 'P1', HPRE, HIS + ['Bấm Đóng / (x) / ra ngoài.'], '—', ['Cửa sổ đóng.'], 184)
S6.add('Trạng thái danh sách sau đóng', 'P1', [HPRE, 'Đang ở trang 2, lọc Đã hạch toán.'], HIS + ['Đóng cửa sổ.'], '—',
       ['Vẫn trang 2, giữ bộ lọc, sắp xếp.'], 185)
S6.add('Lịch sử ở màn chi tiết', 'P1', HPRE, ['Mở chi tiết 068, bấm Xem lịch sử.'], '—', ['Cùng nội dung cửa sổ; nút đổi thành Thu gọn.'], 162)
S6.add('Bấm tên file trong lịch sử', 'P2', 'Phiếu có mốc "File đính kèm thêm mới".', ['Mở Lịch sử, bấm tên file.'], '—', ['Mở xem trước file.'], 168)

# ============================================================== VII. XEM CHI TIẾT
S7 = Sec(7)
DET = [MENU, 'Bấm số phiếu TPE.YCHTMDV.2026000069.']
S7.add('Mở màn chi tiết', 'P0', [PRE_LIST, WAIT], DET, '—', ['Mở TRANG chi tiết (không phải cửa sổ).'], 186)
S7.add('Tiêu đề', 'P1', [PRE_LIST, WAIT], DET, '—', ['"Chi tiết yêu cầu hạch toán mua dịch vụ: TPE.YCHTMDV.2026000069".'], 187)
S7.add('Đầy đủ trường', 'P0', [PRE_LIST, WAIT], DET, '—',
       ['Thông tin chung, File đính kèm, Danh sách dịch vụ (không có cột SL HĐ còn lại), 3 dòng tổng, khối Lịch sử.'], 188)
S7.add('Khớp dữ liệu tạo và danh sách', 'P0', [PRE_LIST, WAIT], DET, '—',
       ['Loại, hợp đồng, NCC, Tổng thanh toán 444,440, người tạo, ngày tạo khớp dòng ở danh sách.'], [189, 190])
S7.add('Trường chỉ đọc, không có nút lưu', 'P0', [PRE_LIST, WAIT], DET, '—', ['Mọi ô xám chỉ đọc; không có Lưu nháp / Lưu và gửi duyệt.'], [191, 192])
S7.add('Nút theo trạng thái', 'P0', [ACC_K, WAIT], ['Đăng nhập K.'] + DET, '—',
       ['Chân màn: Hạch toán, Không duyệt, In phiếu, Quay lại; không có Sửa / Xóa.'], 193)
S7.add('Phiếu Đã hạch toán chỉ xem', 'P1', PRE_LIST, [MENU, 'Mở chi tiết 068.'], '—', ['Chỉ In phiếu, Quay lại.'], 194)
S7.add('Phiếu Không duyệt hiện Ghi chú duyệt', 'P1', [ACC_A, REJ_A], [MENU, 'Mở chi tiết 102.'], '—', ['Ô Ghi chú duyệt "Sai SL"; có Sửa, Xóa.'], 193)
S7.add('Khu vực lịch sử', 'P1', [PRE_LIST, WAIT], DET + ['Bấm Xem lịch sử.'], '—', ['Mở khối, hiện mốc; bấm Thu gọn đóng lại.'], 195)
S7.add('Quay lại danh sách', 'P1', [PRE_LIST, WAIT], DET + ['Bấm Quay lại.'], '—', ['Về danh sách.'], 196)
S7.add('Giữ bộ lọc khi quay lại', 'P1', 'Đang lọc Trạng thái = Chờ duyệt.', ['Bấm số phiếu 069.', 'Bấm Quay lại.'], '—',
       ['Danh sách vẫn lọc Chờ duyệt (trong 10 phút).'], 197)
S7.add('Mở chi tiết ngoài phạm vi', 'P0', [ACC_B, WAIT], ['B mở thẳng đường dẫn chi tiết phiếu 069.'], '—',
       ['Chuyển sang trang không tìm thấy; không lộ dữ liệu.'], [186, 296])
S7.add('Link chứng từ ở chi tiết', 'P2', [PRE_LIST, WAIT], DET + ['Bấm số hợp đồng.', 'Bấm số yêu cầu TPE.YCMDV.2026000108.'], '—',
       ['Hợp đồng mở ERP ở tab mới.', 'Yêu cầu mua dịch vụ mở màn chi tiết ở tab mới.'], 188)

# ============================================================== VIII. TÙY CHỈNH CỘT
S8 = Sec(8)
COL = [MENU, 'Bấm nút biểu tượng cột (Cấu hình cột hiển thị).']
COL_PRE = [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.']
S8.add('Mở cửa sổ', 'P0', COL_PRE, COL, '—', ['Cửa sổ "Tuỳ chỉnh cột".'], 198)
S8.add('Danh sách cột', 'P0', COL_PRE, COL, '—', ['Liệt kê 15 cột đúng thứ tự trên bảng.'], 199)
S8.add('Cột chọn mặc định', 'P1', COL_PRE, COL, '—', ['Tích đủ 15/15.'], 200)
S8.add('Ẩn cột', 'P0', COL_PRE, COL + ['Bỏ tích Diễn giải, Lưu.'], '—', ['"Cập nhật thành công"; bảng mất cột Diễn giải.'], [202, 206])
S8.add('Hiện lại cột đã ẩn', 'P0', 'Đã ẩn Diễn giải.', COL + ['Tích Diễn giải, Lưu.'], '—', ['Cột Diễn giải hiện lại.'], 201)
S8.add('Cột bắt buộc không ẩn', 'P0', COL_PRE, COL + ['Thử bỏ tích STT, Số phiếu, Hành động.'], '—',
       ['Ô tích xám, không bỏ được; di chuột "Cột bắt buộc — không thể ẩn hoặc đổi vị trí".'], [203, 205])
S8.add('Kéo thả thứ tự', 'P1', COL_PRE, COL + ['Kéo Trạng thái lên sau Số phiếu, Lưu.'], '—', ['Trạng thái đứng ngay sau Số phiếu.'], 204)
S8.add('Đóng không lưu', 'P1', COL_PRE, COL + ['Bỏ tích Người tạo, bấm Đóng.'], '—', ['Bảng giữ cột Người tạo; mở lại vẫn tích.'], 207)
S8.add('Ghi nhớ sau F5', 'P1', 'Đã ẩn Diễn giải.', ['Nhấn F5.'], '—', ['Vẫn ẩn Diễn giải.'], 208)
S8.add('Theo tài khoản', 'P1', 'A đã ẩn Diễn giải.', ['Đăng nhập B trên cùng trình duyệt, mở màn.', 'A đăng nhập trình duyệt khác.'], '—',
       ['B thấy đủ cột.', 'A ở trình duyệt khác vẫn ẩn Diễn giải.'], 209)
S8.add('Không ảnh hưởng dữ liệu và lọc', 'P1', 'Đang lọc Chờ duyệt, 3 phiếu.', COL + ['Ẩn 3 cột, Lưu.'], '—',
       ['Vẫn 3 phiếu, bộ lọc giữ.'], [210, 211])
S8.add('Chọn tất cả / Bỏ chọn hết', 'P2', COL_PRE, COL + ['Bấm Bỏ chọn hết.', 'Bấm Chọn tất cả.'], '—',
       ['Bỏ chọn hết: chỉ còn 3 cột khóa.', 'Chọn tất cả: 15/15.'], 199)

# ============================================================== IX. XUẤT EXCEL
S9 = Sec(9)
EXP = [MENU, 'Bấm Xuất Excel.']
S9.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, EXP, '—', ['Cửa sổ "Chọn trường xuất file".'], 212)
S9.add('Danh sách trường', 'P0', PRE_LIST, EXP, '—',
       ['12 trường: Số phiếu, Loại yêu cầu, Số hợp đồng, Nhà cung cấp, Tổng thanh toán, Ngày tạo, Người tạo, Ngày duyệt, Người duyệt, '
        'Người cập nhật, Ngày cập nhật, Trạng thái.'], 213)
S9.add('Trường chọn mặc định theo cột đang hiện', 'P1', 'Đã ẩn cột Người cập nhật.', EXP, '—', ['Người cập nhật bỏ tích; còn lại tích; "Đang chọn 11/12 trường".'], 214)
S9.add('Xuất với trường mặc định', 'P0', PRE_LIST, EXP + ['Bấm Xuất file.'], '—',
       ['"Xuất Excel thành công"; tải danh_sach_yeu_cau_hach_toan_mua_dich_vu.xlsx.'], [215, 223])
S9.add('Xuất tất cả trường', 'P1', PRE_LIST, EXP + ['Bấm Chọn tất cả, Xuất file.'], '—', ['File có STT + 12 cột.'], 216)
S9.add('Xuất một số trường, đổi thứ tự', 'P0', PRE_LIST, EXP + ['Bỏ chọn hết, tích Số phiếu, Trạng thái, Tổng thanh toán; kéo Trạng thái lên đầu.',
       'Xuất file.'], '—', ['File: STT, Trạng thái, Số phiếu, Tổng thanh toán đúng thứ tự.'], [217, 226])
S9.add('Không chọn trường nào', 'P1', PRE_LIST, EXP + ['Bấm Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S9.add('Xuất theo tìm kiếm', 'P0', PRE_LIST, [MENU, 'Tìm "HDMDV-91".', 'Xuất Excel, Xuất file.'], '—', ['File chỉ có phiếu của hợp đồng đó.'], 219)
S9.add('Xuất theo bộ lọc', 'P0', PRE_LIST, [MENU, ADV, 'Lọc Trạng thái = Đã hạch toán.', 'Xuất Excel, Xuất file.'], '—',
       ['File có đúng 60 phiếu Đã hạch toán.'], 220)
S9.add('Xuất nhiều trang', 'P0', PRE_LIST, [MENU, 'Đang ở trang 1 (10 dòng), Xuất file.'], '—', ['File có đủ 65 dòng, không riêng trang đang xem.'], [221, 227])
S9.add('Danh sách rỗng', 'P1', PRE_LIST, [MENU, 'Tìm "ZZZ999".', 'Xuất Excel, Xuất file.'], '—',
       ['Vẫn tải file: logo, tiêu đề, hàng tên cột, không có dòng dữ liệu.'], 222)
S9.add('Định dạng file', 'P1', 'Đã tải file ở TC_09.004.', ['Mở file bằng Excel.'], '—', ['File .xlsx mở được, không cảnh báo hỏng.'], 224)
S9.add('Tiêu đề cột và cấu trúc', 'P1', 'File của TC_09.004.', ['Quan sát 3 dòng đầu.'], '—',
       ['Dòng 1 logo công ty; dòng 2 "Danh sách yêu cầu hạch toán mua dịch vụ"; dòng 3 STT + tên cột đúng nhãn.'], 225)
S9.add('Dữ liệu khớp màn hình', 'P0', 'File của TC_09.004.', ['So 5 dòng với màn hình.'], '—',
       ['Số phiếu, NCC, Tổng thanh toán, trạng thái khớp; thứ tự dòng theo sắp xếp đang áp.'], 228)
S9.add('Định dạng ngày / số', 'P1', 'File của TC_09.004.', ['Kiểm cột Tổng thanh toán, Ngày tạo.'], '—',
       ['Tổng thanh toán là ô số, SUM được; ngày dd/mm/yyyy hh:mm.'], 229)
S9.add('Tiếng Việt và ký tự đặc biệt', 'P1', 'Có phiếu NCC "CÔNG TY TNHH KỸ THUẬT HÙNG VƯƠNG", Diễn giải có "&".', ['Xuất, mở file.'], '—',
       ['Hiển thị đúng dấu tiếng Việt, ký tự đặc biệt; chuỗi bắt đầu "=" không thành công thức.'], 230)
S9.add('Phạm vi quyền khi xuất', 'P0', [ACC_A, 'A tạo 3 phiếu.'], ['Đăng nhập A, Xuất Excel tất cả.'], '—', ['File chỉ 3 phiếu của A.'], [220, 293])
S9.add('Đóng cửa sổ không xuất', 'P2', PRE_LIST, EXP + ['Bấm Đóng.'], '—', ['Không tải file.'], 212)

# ============================================================== X. ẢNH HƯỞNG CÁC MÀN HÌNH SỬ DỤNG DỮ LIỆU
S10 = Sec(10)
S10.add('Lập phiếu khi hợp đồng chưa có dòng dịch vụ', 'P1', [ACC_A, 'A có hợp đồng TPE.HDMDV-93 đã duyệt chưa có dòng dịch vụ.'],
       TAO + ['Chọn TPE.HDMDV-93.'], '—', ['Báo "Hợp đồng chưa có dòng dịch vụ nào."; gửi duyệt bị chặn "Danh sách dịch vụ – Hợp đồng chưa có dòng dịch vụ nào".'], 268)
S10.add('Lập phiếu khi hợp đồng có dòng dịch vụ', 'P0', PRE_FORM, TAO + ['Chọn TPE.HDMDV-91.'], '—',
       ['Nạp dịch vụ "Chi phí đi lại", yêu cầu TPE.YCMDV.2026000108, SL HĐ còn lại 20.'], 269)
S10.add('Không xóa khi đã có phiếu hạch toán', 'P0', 'Phiếu 068 Đã hạch toán.', [MENU, 'Quan sát dòng 068.'], '—', ['Không có Xóa.'], 270)
S10.add('Không mất liên kết khi sửa', 'P1', [ACC_A, DRAFT_A], ['Sửa Diễn giải phiếu 101.', 'Mở chi tiết.'], '—',
       ['Hợp đồng, yêu cầu mua dịch vụ, link vẫn đúng.'], 272)
S10.add('Phiếu Chờ duyệt xuất hiện ở màn Hạch toán', 'P0', [ACC_K, WAIT], ['K vào màn Hạch toán mua dịch vụ, Tạo mới, mở chọn phiếu yêu cầu.'], '—',
       ['Có phiếu 069 (do người khác tạo thì theo quy tắc màn đó).', 'Hoặc bấm Hạch toán ở dòng 069: màn Tạo phiếu hạch toán chọn sẵn 069.'], 274)
S10.add('Đổi thông tin đồng bộ', 'P1', [ACC_A, DRAFT_A], ['Sửa Diễn giải phiếu 101.', 'Xem danh sách, chi tiết, bản in, Excel.'], '—',
       ['Diễn giải mới hiện đồng bộ cả 4 nơi.'], 278)
S10.add('Số phiếu không đổi, liên kết giữ nguyên', 'P2', 'Phiếu 069 đã được lập phiếu hạch toán nháp.', ['Mở phiếu hạch toán.'], '—',
       ['Ô Phiếu yêu cầu vẫn TPE.YCHTMDV.2026000069; bấm mở đúng phiếu.'], 279)
S10.add('Xóa đồng bộ', 'P1', [ACC_A, DRAFT_A], ['Xóa phiếu 101.', 'Mở màn chọn hợp đồng, xem SL còn lại.'], '—',
       ['Phiếu 101 không còn; SL HĐ còn lại tăng lại.'], 280)
S10.add('Trạng thái tự cập nhật khi lưu nháp phiếu hạch toán', 'P0', [ACC_K, WAIT], ['K bấm Hạch toán ở 069, Lưu nháp phiếu hạch toán.',
        'Quay lại danh sách yêu cầu.'], '—', ['Phiếu 069 thành Đang hạch toán; lịch sử ghi "Chờ duyệt sang Đang hạch toán".'], 281)
S10.add('Trạng thái về Chờ duyệt khi xóa phiếu hạch toán nháp', 'P1', 'Phiếu 069 Đang hạch toán (TC_10.009).', ['K xóa phiếu hạch toán nháp.'],
        '—', ['Phiếu 069 về Chờ duyệt, lại có nút Hạch toán / Không duyệt.'], 281)
S10.add('Bộ lọc màn liên quan cập nhật', 'P2', 'Phiếu 069 vừa Đã hạch toán.', ['Ở danh sách lọc Trạng thái = Chờ duyệt.'], '—',
        ['Phiếu 069 không còn trong kết quả; lọc Đã hạch toán thì có.'], 282)
S10.add('Dòng yêu cầu đúng hợp đồng cha', 'P1', 'Công cụ kiểm thử API.', ['Gửi lưu phiếu với id dòng yêu cầu của hợp đồng khác.'], '—',
        ['"Dòng yêu cầu không thuộc hợp đồng đã chọn."; không lưu.'], 283)
S10.add('Tham chiếu không mất khi đổi trạng thái', 'P1', [ACC_K, WAIT], ['K Không duyệt 069.', 'Mở chi tiết.'], '—',
        ['Hợp đồng, dòng dịch vụ, file vẫn đủ.'], 284)
S10.add('Không có bản ghi mồ côi', 'P2', 'Đã xóa phiếu 101 (TC_10.008).', ['Kiểm dữ liệu dòng dịch vụ / yêu cầu của phiếu 101 (công cụ kiểm thử API).'],
        '—', ['Không còn dòng nào của phiếu 101.'], 285)
S10.add('Không vượt / trùng giữ SL hợp đồng', 'P0', 'TPE.HDMDV-91 SL 20; phiếu X Chờ duyệt giữ 20.', TAO + ['Chọn TPE.HDMDV-91.'], '—',
        ['SL HĐ còn lại 0; nhập 1 sang "Không được vượt SL còn lại".'], 286)
S10.add('Duyệt phiếu hạch toán cộng SL đã hạch toán vào hợp đồng', 'P1', [ACC_K, WAIT], ['K Hạch toán 069, Lưu và duyệt > Duyệt.',
        'A lập phiếu mới từ TPE.HDMDV-91.'], '—', ['Phiếu 069 Đã hạch toán.', 'SL HĐ còn lại vẫn 0 (20 đã hạch toán).'], [281, 274])

# ============================================================== XI. PHÂN QUYỀN
S11 = Sec(11)
S11.add('Không có quyền nào chỉ thấy phiếu mình tạo', 'P0', [ACC_A, 'A tạo 3 phiếu; hệ thống có 65 phiếu.'], ['Đăng nhập A.', MENU], '—',
        ['"Hiển thị 1–3 / 3"; không có ô Công ty, Phòng ban.'], [287, 299])
S11.add('Xem - theo tổng công ty', 'P1', 'Tài khoản C.', ['Đăng nhập C.', MENU, ADV], '—', ['Thấy phiếu mọi công ty (trừ nháp người khác); có ô Công ty.'], [287, 299])
S11.add('Xem - theo công ty', 'P0', 'Tài khoản D thuộc công ty 1.', ['Đăng nhập D.', MENU], '—', ['Chỉ phiếu công ty 1.'], [287, 299])
S11.add('Xem - theo phòng ban', 'P1', 'Tài khoản E quản lý phòng Kinh doanh 1.', ['Đăng nhập E.', MENU], '—', ['Chỉ phiếu phòng Kinh doanh 1.'], [287, 299])
S11.add('Nháp của người khác luôn ẩn', 'P0', [ACC_A, 'Tài khoản C; A có phiếu nháp 101.'], ['Đăng nhập C.', MENU, ADV, 'Lọc Đang tạo.'], '—',
        ['Không thấy phiếu 101.'], [287, 299])
S11.add('Quyền Hạch toán thấy phiếu Chờ duyệt cùng công ty', 'P0', [ACC_K, WAIT, ACC_K2], ['Đăng nhập K.', MENU, 'Đăng nhập K2.', MENU], '—',
        ['K thấy 069 với nút Hạch toán, Không duyệt.', 'K2 không thấy 069.'], [287, 299, 295])
S11.add('Xem chi tiết theo quyền', 'P0', [ACC_B, WAIT, ACC_K], ['B mở đường dẫn chi tiết 069.', 'K mở chi tiết 069.'], '—',
        ['B: trang không tìm thấy.', 'K: xem được.'], 288)
S11.add('Thêm mới không cần quyền', 'P1', ACC_B, ['Đăng nhập B.', MENU, 'Bấm Tạo mới.'], '—', ['Mở được màn Tạo.'], 289)
S11.add('Chỉ chọn hợp đồng do mình tạo', 'P0', [ACC_B, HD], ['Đăng nhập B, Tạo mới, mở chọn hợp đồng.'], '—',
        ['Không có TPE.HDMDV-91; "Không có hợp đồng mua dịch vụ đã duyệt nào do bạn tạo." nếu B không có hợp đồng.'], 289)
S11.add('Sửa / Xóa chỉ người tạo', 'P0', [ACC_B, ACC_K, DRAFT_A], ['C (tổng công ty) xem phiếu 102 Không duyệt của A.'], '—',
        ['Không có nút Sửa / Xóa.'], [290, 291, 295])
S11.add('Xem lịch sử, In, Xuất Excel không gắn quyền', 'P1', ACC_A, ['Đăng nhập A, mở Lịch sử, In, Xuất Excel phiếu mình.'], '—',
        ['Dùng được cả 3.'], [293, 294])
S11.add('Không có Import / Khóa', 'P2', PRE_LIST, [MENU], '—', ['Không có nút Import, Khóa / Mở khóa.'], [292, 293])
S11.add('URL trực tiếp màn Sửa khi không đủ quyền', 'P0', [ACC_B, DRAFT_A], ['B mở đường dẫn màn Sửa phiếu 101.'], '—',
        ['Phiếu nháp người khác: trang không tìm thấy.'], 296)
S11.add('API Không duyệt khi thiếu quyền', 'P0', [ACC_A, WAIT], ['A dùng công cụ kiểm thử API gọi Không duyệt 069.'], '—',
        ['"Bạn không có quyền thực hiện chức năng này"; phiếu giữ Chờ duyệt.'], 297)
S11.add('API Không duyệt khác công ty', 'P1', [ACC_K2, WAIT], ['K2 dùng công cụ kiểm thử API gọi Không duyệt 069.'], '—',
        ['"Bạn không có quyền thao tác trên phiếu này".'], 297)
S11.add('API Sửa phiếu người khác', 'P0', [ACC_B, DRAFT_A], ['B gọi sửa phiếu 101.'], '—', ['"Bạn không có quyền sửa phiếu này".'], 297)
S11.add('Đổi quyền giữa thao tác', 'P1', [ACC_K, WAIT], ['K mở chi tiết 069.', 'Quản trị gỡ quyền Hạch toán của K.', 'K bấm Không duyệt, nhập ghi chú, xác nhận.'],
        '—', ['"Bạn không có quyền thực hiện chức năng này"; phiếu giữ Chờ duyệt.', 'Tải lại thì không còn nút.'], 298)
S11.add('Super admin không có quyền Hạch toán', 'P2', 'Tài khoản Super admin chưa gán quyền Hạch toán mua dịch vụ.', ['Mở danh sách, xem dòng Chờ duyệt.'],
        '—', ['Thấy phiếu nhưng không có nút Hạch toán / Không duyệt.'], [295, 299])

# ============================================================== XII. DUYỆT PHIẾU (HẠCH TOÁN)
S12 = Sec(12)
S12.add('Điều kiện hiển thị nút Hạch toán', 'P0', [ACC_K, WAIT, 'Phiếu 068 Đã hạch toán.'], ['Đăng nhập K.', MENU], '—',
        ['Dòng 069 có Hạch toán (biểu tượng máy tính); dòng 068 không có.', 'Màn không có nút "Duyệt": kế toán duyệt bằng Hạch toán.'], 300)
S12.add('Bấm Hạch toán mở màn Tạo phiếu hạch toán', 'P0', [ACC_K, WAIT], ['Bấm Hạch toán ở dòng 069.'], '—',
        ['Mở "Tạo phiếu hạch toán mua dịch vụ" chọn sẵn 069; không có hộp xác nhận ở bước này.'], 301)
S12.add('Hộp xác nhận duyệt ở màn hạch toán', 'P1', 'Đang ở TC_12.002, nhập đủ.', ['Bấm Lưu và duyệt.'], '—',
        ['Hộp "Xác nhận duyệt": "Phiếu đã duyệt sẽ ghi sổ kế toán và không sửa, xóa được nữa. Thao tác này có thể ảnh hưởng đến dữ liệu. '
         'Bạn có muốn tiếp tục?" (Duyệt / Hủy).'], 301)
S12.add('Hạch toán thành công', 'P0', 'Đang ở hộp TC_12.003.', ['Bấm Duyệt.'], '—',
        ['"Duyệt thành công."; phiếu 069 Đã hạch toán.'], [302, 305])
S12.add('Dữ liệu bắt buộc trước khi duyệt', 'P1', 'Đang ở TC_12.002.', ['Bỏ trống trường bắt buộc của phiếu hạch toán, bấm Lưu và duyệt.'],
        '—', ['"Bạn chưa nhập đầy đủ thông tin."; phiếu 069 giữ Chờ duyệt.'], 303)
S12.add('Điều kiện nghiệp vụ: phiếu đã đổi trạng thái', 'P0', [ACC_K, WAIT], ['Tab 1 K mở màn hạch toán từ 069.', 'Tab 2 K Không duyệt 069.',
        'Tab 1 Lưu nháp.'], '—', ['"Phiếu yêu cầu – Không ở trạng thái Chờ duyệt hoặc bạn không có quyền hạch toán phiếu này."'], 304)
S12.add('Người duyệt / Ngày duyệt sau hạch toán', 'P0', 'Đã duyệt ở TC_12.004.', [MENU, 'Xem dòng 069.'], '—',
        ['Người duyệt = K, Ngày duyệt = thời điểm duyệt.'], [306, 312])
S12.add('Ảnh hưởng hợp đồng', 'P1', 'Đã duyệt ở TC_12.004.', ['A Tạo mới, chọn TPE.HDMDV-91.'], '—', ['SL đã hạch toán cộng vào hợp đồng; SL còn lại không tăng lại.'], 307)
S12.add('Thông báo sau khi hạch toán', 'P2', 'Đã duyệt ở TC_12.004.', ['A mở chuông.'], '—',
        ['Không có thông báo riêng cho người tạo (hiện chỉ thông báo khi gửi duyệt và Không duyệt).',
         'Lưu ý: ghi nhận nếu nghiệp vụ cần báo người tạo.'], [308, 309])
S12.add('Hủy thao tác duyệt', 'P0', 'Đang ở hộp TC_12.003.', ['Bấm Hủy.'], '—', ['Không lưu; phiếu 069 giữ Chờ duyệt.'], 310)
S12.add('Không duyệt lại phiếu đã xử lý', 'P0', 'Phiếu 069 Đã hạch toán.', ['K mở chi tiết 069.', 'Gọi lập phiếu hạch toán từ 069 bằng công cụ kiểm thử API.'],
        '—', ['Không có nút Hạch toán.', 'Máy chủ từ chối với câu "Phiếu yêu cầu – Không ở trạng thái Chờ duyệt …".'], 311)
S12.add('Lịch sử ghi nhận hạch toán', 'P1', 'Đã duyệt ở TC_12.004.', ['Mở Lịch sử 069.'], '—',
        ['2 mốc "Thay đổi trạng thái" (Chờ duyệt sang Đang hạch toán / sang Đã hạch toán hoặc trực tiếp) kèm "Từ phiếu hạch toán mua dịch vụ".'], 312)

# ============================================================== XIII. KHÔNG DUYỆT PHIẾU
S13 = Sec(13)
REJ = ['Đăng nhập K.', MENU, 'Ở dòng 069 bấm Không duyệt.']
S13.add('Điều kiện hiển thị nút Không duyệt', 'P0', [ACC_K, WAIT, ACC_A], ['K mở danh sách.', 'A mở danh sách.'], '—',
        ['K: dòng 069 có Không duyệt (đỏ).', 'A: không có.'], 313)
S13.add('Giao diện cửa sổ Không duyệt', 'P0', [ACC_K, WAIT], REJ, '—',
        ['Tiêu đề "Không duyệt yêu cầu hạch toán mua dịch vụ", dòng "Phiếu: TPE.YCHTMDV.2026000069"; ô Ghi chú duyệt * (con trỏ sẵn); '
         'nút Không duyệt (đỏ), Hủy.'], 314)
S13.add('Không duyệt thành công', 'P0', [ACC_K, WAIT], REJ + ['Nhập "Sai SL", bấm Không duyệt.'], 'Ghi chú: Sai SL',
        ['"Thao tác thành công."; danh sách nạp lại; 069 nhãn đỏ Không duyệt.'], [315, 318])
S13.add('Bỏ trống ghi chú', 'P0', [ACC_K, WAIT], REJ + ['Bấm Không duyệt ngay.', 'Nhập 3 dấu cách, bấm lại.'], '—',
        ['"Bắt buộc phải nhập", viền đỏ; không gửi máy chủ.'], 316)
S13.add('Ghi chú vượt 255 ký tự', 'P1', [ACC_K, WAIT], REJ + ['Dán 300 ký tự, bấm Không duyệt.'], '300 ký tự',
        ['Máy chủ báo lỗi độ dài (tối đa 255 ký tự); phiếu giữ Chờ duyệt.', 'Ghi chú 255 ký tự thì lưu được.'], 317)
S13.add('Hiển thị và lưu ghi chú', 'P0', 'Đã Không duyệt ở TC_13.003.', ['A mở chi tiết 069.'], '—',
        ['Ô Ghi chú duyệt "Sai SL"; Người duyệt K, Ngày duyệt = thời điểm Không duyệt.'], [319, 324])
S13.add('Ảnh hưởng: trả SL hợp đồng', 'P1', 'Đã Không duyệt 069 (giữ 20 của TPE.HDMDV-91).', ['A Tạo mới, chọn TPE.HDMDV-91.'], '—',
        ['SL HĐ còn lại 20 (phiếu Không duyệt không giữ SL).'], 320)
S13.add('Ảnh hưởng: trả đơn bảo hiểm', 'P1', 'Phiếu bảo hiểm Chờ duyệt giữ đơn DBH-001.', ['K Không duyệt phiếu đó.', 'A Tạo mới loại Công nợ bảo '
        'hiểm, mở chọn đơn.'], '—', ['DBH-001 chọn lại được.'], 320)
S13.add('Thông báo cho người tạo', 'P0', 'Đã Không duyệt ở TC_13.003.', ['A mở chuông.'], '—',
        ['"[YCHTMDV] Từ chối: TPE.YCHTMDV.2026000069" kèm "Người từ chối: <K>", "Lý do: Sai SL"; bấm mở chi tiết.'], 321)
S13.add('Hủy thao tác', 'P0', [ACC_K, WAIT], REJ + ['Nhập ghi chú, bấm Hủy (hoặc (x) / ra ngoài).'], '—',
        ['Đóng không hỏi; phiếu giữ Chờ duyệt.'], 322)
S13.add('Không duyệt lại phiếu đã xử lý', 'P0', [ACC_K, WAIT], ['Tab 1 mở cửa sổ Không duyệt 069.', 'Tab 2 Không duyệt 069.', 'Tab 1 nhập ghi chú, bấm Không duyệt.'],
        '—', ['"Trạng thái đã bị thay đổi. Vui lòng load lại trang".'], 323)
S13.add('Lịch sử Không duyệt', 'P0', 'Đã Không duyệt ở TC_13.003.', ['Mở Lịch sử 069.'], '—',
        ['"Thay đổi trạng thái: Chờ duyệt sang Không duyệt" kèm "Sai SL", người thực hiện K.'], 324)
S13.add('Không duyệt từ màn chi tiết', 'P1', [ACC_K, WAIT], ['K mở chi tiết 069, bấm Không duyệt, nhập ghi chú, xác nhận.'], '—',
        ['"Thao tác thành công."; quay về danh sách.'], 315)

# ============================================================== XIV. IN PHIẾU VÀ IN DANH SÁCH
S14 = Sec(14)
S14.add('In phiếu từ danh sách', 'P0', [PRE_LIST, WAIT], [MENU, 'Ở dòng 069 bấm "…" > In phiếu.'], '—',
        ['Cửa sổ "Xem trước phiếu yêu cầu hạch toán mua dịch vụ" ngay trên màn, "Đang tải dữ liệu in…".',
         'Bản in: "PHIẾU YÊU CẦU HẠCH TOÁN MUA DỊCH VỤ", số phiếu, ngày lập, loại, Hóa đơn VAT, NCC, hợp đồng, bảng dịch vụ, 3 dòng tổng.'])
S14.add('Letterhead theo công ty ghi trên phiếu', 'P0', 'Tài khoản C thuộc công ty 2; phiếu 069 công ty 1.', ['C in phiếu 069.'], '—',
        ['Letterhead công ty 1, không phải công ty 2.'])
S14.add('In và đóng cửa sổ', 'P2', 'Đang ở cửa sổ xem trước.', ['Bấm In.', 'Đóng hộp in, bấm (x).'], '—', ['Mở hộp thoại in; (x) đóng cửa sổ.'])
S14.add('In phiếu loại Công nợ bảo hiểm', 'P2', 'Có phiếu loại Công nợ bảo hiểm.', ['Mở chi tiết, bấm In phiếu.'], '—',
        ['Bản in có Số đơn bảo hiểm, Số hợp đồng mua, Phụ lục bổ sung, Ghi chú, bảng phí bảo hiểm.'])
S14.add('In danh sách theo bộ lọc', 'P1', PRE_LIST, [MENU, 'Lọc Đã hạch toán.', 'Bấm In danh sách.'], '—',
        ['Cửa sổ "Xem trước danh sách yêu cầu hạch toán mua dịch vụ" chỉ có 60 phiếu Đã hạch toán.'])
S14.add('In danh sách vượt 2.000 dòng', 'P2', 'Phạm vi có hơn 2.000 phiếu.', ['Bấm In danh sách không lọc.'], '—',
        ['Báo "Danh sách có <N> dòng, vượt mức in tối đa 2.000 dòng nên chưa in được. …"; không hiện bản in.'])
S14.add('In phiếu ngoài phạm vi', 'P2', [ACC_B, WAIT], ['B gọi dữ liệu in phiếu 069 (công cụ kiểm thử API).'], '—', ['"Bạn không có quyền xem phiếu này".'])

# ============================================================== XV. CHỌN HỢP ĐỒNG / ĐƠN BẢO HIỂM
S15 = Sec(15)
S15.add('Cửa sổ Chọn hợp đồng mua dịch vụ', 'P0', PRE_FORM, TAO + ['Bấm ô Hợp đồng mua dịch vụ.'], '—',
        ['Cửa sổ "Chọn hợp đồng mua dịch vụ": ô Số hợp đồng, Tìm kiếm, Làm mới; cột STT, Số hợp đồng, Nhà cung cấp, Ngày tạo; 10 dòng/trang.',
         'Chỉ hợp đồng đã duyệt do A tạo.'])
S15.add('Tìm và sắp xếp trong cửa sổ', 'P1', PRE_FORM, TAO + ['Mở cửa sổ, nhập "91", Enter.', 'Bấm tiêu đề Số hợp đồng.'], '—',
        ['Ra TPE.HDMDV-91.', 'Sắp theo số hợp đồng.'])
S15.add('Bấm link số hợp đồng không chọn dòng', 'P1', PRE_FORM, TAO + ['Mở cửa sổ, bấm link TPE.HDMDV-91.'], '—',
        ['Mở ERP ở tab mới; cửa sổ vẫn mở, chưa chọn.'])
S15.add('Chọn hợp đồng nạp dữ liệu', 'P0', PRE_FORM, TAO + ['Bấm dòng TPE.HDMDV-91.'], '—',
        ['Cửa sổ đóng; điền hợp đồng, NCC "20TTHPGI-27 – A HẢI"; bảng dịch vụ có SL HĐ còn lại 20, SL hạch toán 20.'])
S15.add('Bỏ chọn hợp đồng bằng nút ×', 'P1', 'Đã chọn TPE.HDMDV-91, Kèm hóa đơn.', ['Bấm × ở ô Hợp đồng.'], '—',
        ['Xóa hợp đồng, NCC, bảng dịch vụ; VAT về 0.'])
S15.add('Cửa sổ Chọn đơn bảo hiểm', 'P1', PRE_FORM, TAO + ['Chọn Công nợ bảo hiểm, bấm ô Số đơn bảo hiểm.'], '—',
        ['Ô Số đơn, Số phụ lục, Số hợp đồng mua; cột Số đơn, Số phụ lục, Số hợp đồng mua, Ngày tạo (đều sắp xếp được).',
         'Không có đơn: "Không có đơn bảo hiểm phù hợp."'])
S15.add('Đóng cửa sổ không chọn', 'P2', PRE_FORM, TAO + ['Mở cửa sổ, bấm Đóng (hoặc (x) / ra ngoài).'], '—', ['Ô giữ nguyên trống.'])
S15.add('Xóa nhanh chữ trong ô tìm', 'P2', PRE_FORM, TAO + ['Mở cửa sổ, nhập "91", bấm × trong ô.'], '—', ['Xóa chữ và tìm lại ngay.'])

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
    ('XII', 'DUYỆT PHIẾU (HẠCH TOÁN)', S12),
    ('XIII', 'KHÔNG DUYỆT PHIẾU', S13),
    ('XIV', 'IN PHIẾU VÀ IN DANH SÁCH', S14),
    ('XV', 'CHỌN HỢP ĐỒNG MUA DỊCH VỤ VÀ ĐƠN BẢO HIỂM', S15),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
check_no_dash_pre(SECTIONS, [])

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1', feature_name='Yêu cầu hạch toán mua dịch vụ - Cập nhật ngày 03/11/2026',
          module_name='YC hạch toán mua dịch vụ', description_block=DESCRIPTION_BLOCK, role_tcs=[], sections=SECTIONS)
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.0f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))

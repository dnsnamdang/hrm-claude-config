# -*- coding: utf-8 -*-
"""Testcase màn "Biên bản bàn giao nghiệm thu" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan,
loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (xác định từ code 10/11/2026): chứng từ có trạng thái (Đang tạo / Chờ duyệt / Đã duyệt), có Tạo mới (Lưu nháp, Lưu và
tiếp tục), Sửa + Xóa (Đang tạo + người tạo + quyền Tạo), Lưu và duyệt (= bước duyệt, hỏi xác nhận), In biên bản / In danh sách,
Lịch sử, Xuất Excel, Tùy chỉnh cột. KHÔNG có Khóa, Gửi duyệt, Không duyệt, Hủy phiếu, Import (kiểm code: không route / nút) nên bỏ
các nhóm đó.
Nhóm: I Hiển thị (3 lối vào) · II Tìm kiếm & lọc (gồm Cài đặt bộ lọc) · III Thêm mới (gồm popup Chọn hợp đồng) · IV Chỉnh sửa ·
V Xóa · VI Duyệt phiếu (Lưu và duyệt) · VII Lịch sử · VIII Xem chi tiết · IX In phiếu (biên bản + danh sách) · X Tùy chỉnh cột ·
XI Xuất danh sách Excel · XII Ràng buộc · XIII Phân quyền (cuối). Mỗi case ghi stt checklist nó phủ (ck) — gen_checklist.py đọc CK.
Khuôn: ../phieu-nhap-hang-dieu-chinh-kiem-ke/gen_testcase.py.
Nguồn hành vi (đọc 10/11/2026, nhánh develop cả 2 repo): FE pages/assign/handover-acceptance-records/**; BE Modules/CustomerCare
HandoverAcceptanceRecord* (Controller / Request / Service / StoreService / PrintService), HandoverContractSourceService.
Số liệu mẫu: dev-hrm 10/11/2026 (DNS Admin — Super admin, có quyền Tạo): lối "tất cả" 8.271 biên bản (2 Đang tạo do DNS Admin tạo:
TPE.BBBG.02738, 02737; 0 Chờ duyệt; còn lại Đã duyệt); lối "theo NV" 1 biên bản; popup chọn hợp đồng 1.632 hợp đồng (0 hợp đồng HRM).
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
from tc_phieu_bosung import ListScreen, open_menu_case, filter_memory_cases, combo_cases, org_cases, weird_param_case, \
    check_no_dash_pre  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Công việc > nhóm "Kết quả công việc" > bấm "Biên bản bàn giao nghiệm thu".'
MENU_CC = 'Vào phân hệ CSKH sau bán > nhóm "Hồ sơ công việc" > bấm "Biên bản bàn giao nghiệm thu".'
MENU_NV = 'Vào phân hệ Thông báo > nhóm "Thông báo" > bấm "BB bàn giao nghiệm thu theo NV".'
ADV = 'Bấm Tìm kiếm nâng cao.'
REQ = '"Bắt buộc phải nhập"'
REQS = '"Bắt buộc phải chọn"'
HD = '"Bắt buộc phải chọn 1 hợp đồng"'
INC = '"Bạn chưa nhập đầy đủ thông tin."'
CHK = '"Vui lòng kiểm tra lại thông tin đã nhập"'
PHONE = '"Số điện thoại không đúng định dạng"'
FILEMSG = '"Vui lòng chọn file đính kèm"'
OKC = '"Tạo biên bản bàn giao nghiệm thu thành công."'
OKE = '"Chỉnh sửa biên bản bàn giao nghiệm thu thành công."'
CONFLICT = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'
DUP = '"Không thể tạo biên bản bàn giao nghiệm thu cho hợp đồng này"'

PRE_LIST = ('Tài khoản DNS Admin (Super admin, có quyền "Tạo biên bản bàn giao nghiệm thu"); lối "tất cả" có 8.271 biên bản: 2 Đang '
            'tạo (TPE.BBBG.02738, TPE.BBBG.02737 do DNS Admin tạo), còn lại Đã duyệt, 0 Chờ duyệt.')
B36 = ('Biên bản TPE.BBBG.02736 (Đã duyệt, DNS Admin tạo 09/11/2026 14:30): Ngày BGNT 09/11/2026 00:00, hợp đồng "DHNT_TPE_HN_DAU_26_'
       '0239_ML 05.1610.2026.PN", khách hàng "CÔNG TY TNHH MORI LUBRICANTS VIỆT NAM", NVKD "Trần Thị Phương Nhung - HN_DAU", NV kỹ '
       'thuật "Nguyễn Thị Cần - HN_KD1", người nhận "Ms NHUNG"; 2 hàng ENEO-640-V5235 (SL 1) và ENEO-700-V5252 (SL 3); 1 file docx; '
       'lịch sử 2 mốc Tạo mới + Thay đổi trạng thái.')
B38 = ('Biên bản TPE.BBBG.02738 (Đang tạo, DNS Admin tạo 10/11/2026 11:12): hợp đồng "HĐ_TPE_HN_KDTM_26_1363_21.10", khách hàng "HỘ '
       'KINH DOANH NGUYỄN VĂN THẮNG", NVKD "Nguyễn Văn Thắng", chưa có Ngày bàn giao, chưa có NV kỹ thuật, chưa có file; hàng "Má phanh '
       'trước UP PARTS…" SL theo hợp đồng 10, đã xuất 10, đã nghiệm thu 0.')
ACC_K = 'Tài khoản K: có quyền "Tạo biên bản bàn giao nghiệm thu", không có quyền xem theo cấp, thuộc công ty TPE.'
HDX = ('Hợp đồng "HĐ_TPE_HN_KD1_26_1118_2110" (Hợp đồng bán hàng hóa - vật tư, CÔNG TY TNHH DỊCH VỤ Ô TÔ QUANG TRUNG, duyệt 21/10/2026 10:28) đã xuất hết hàng, chưa có biên bản: NVKD "Lê Huy Thắng", phòng "PHÒNG THIẾT BỊ Ô TÔ 1", '
       'người nhận "Nguyễn Hồng Vương" SĐT 0832551333; 1 hàng "Lọc sàn phòng sơn sợi thủy tinh 0,8x20m, 3540g/m2" (VITO-PA50, '
       'Cuộn) SL theo hợp đồng 3, đã xuất 3, đã trả 0.')
PRE_FORM = ACC_K + '\n' + HDX
TAO = [MENU, 'Bấm "Tạo mới".']
CHON = TAO + ['Bấm ô Hợp đồng/đơn hàng, bấm vào dòng HĐ_TPE_HN_KD1_26_1118_2110.']
DU = CHON + ['Nhập SL đã nghiệm thu = 3.', 'Chọn Nhân viên kỹ thuật = "Nguyễn Thị Cần".', 'Chọn Ngày bàn giao = hôm nay 09:00.']
DUYET = DU + ['Bấm "Thêm tài liệu", chọn file bien_ban.pdf.']
DRAFT = ('Biên bản TPE.BBBG.02740 do K lập từ HĐ_TPE_HN_KD1_26_1118_2110, Đang tạo, SL đã nghiệm thu 3, Ghi chú "Nháp", chưa có '
         'NV kỹ thuật, chưa có file.')
PRE_EDIT = ACC_K + '\n' + DRAFT
SUA = [MENU, 'Ở dòng TPE.BBBG.02740 bấm Sửa (biểu tượng bút chì).']
ACC_V1 = 'Tài khoản V1: quyền "Xem biên bản bàn giao nghiệm thu" mức Tổng công ty.'
ACC_V2 = 'Tài khoản V2: quyền "Xem biên bản bàn giao nghiệm thu" mức Công ty, thuộc công ty TPSG.'
ACC_V3 = 'Tài khoản V3: quyền "Xem biên bản bàn giao nghiệm thu" mức Phòng ban, quản lý phòng KV3 của TPSG.'
ACC_N = ('Tài khoản N: không có quyền nào của màn; đã tự lập 1 biên bản TPE.BBBG.02741 (Đã duyệt); là NVKD của 2 biên bản do người '
         'khác lập.')
FILE = 'File: bien_ban.pdf (1 MB)'

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
     'Màn Biên bản bàn giao nghiệm thu (mã <mã công ty>.BBBG.NNNNN) ghi nhận hàng của 1 hợp đồng / đơn hàng đã bàn giao cho khách: '
     'chọn hợp đồng đã xuất hết hàng (hợp đồng hãng hoặc hợp đồng HRM), hệ thống điền khách hàng, NVKD, hàng hoá; người lập nhập SL '
     'đã nghiệm thu, seri, ngày bàn giao, bảo hành, NV kỹ thuật, file; Lưu nháp (Đang tạo) hoặc Lưu và duyệt (Đã duyệt).'),
    ('2. Đối tượng được tính / hiển thị',
     '- Lối "tất cả" (phân hệ Công việc > Kết quả công việc và CSKH sau bán > Hồ sơ công việc): biên bản theo quyền Xem — Tổng công '
     'ty: mọi biên bản; Công ty: công ty của mình; Phòng ban: phòng mình quản lý; không quyền: biên bản mình tạo.\n'
     '- Lối "theo NV" (phân hệ Thông báo > BB bàn giao nghiệm thu theo NV): biên bản mình là NVKD.\n'
     '- 3 trạng thái: Đang tạo (xám), Chờ duyệt (vàng, chỉ dữ liệu cũ), Đã duyệt (xanh lá).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Lối "tất cả": biên bản Đang tạo của người khác luôn bị ẩn.\n'
     '- Popup chọn hợp đồng không có: hợp đồng khác công ty, chưa có hiệu lực, còn hàng chưa xuất hết, đã có biên bản.\n'
     '- Màn không có Khóa / Mở khóa, Gửi duyệt, Không duyệt, Hủy, Import.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     '- Ngày BGNT: đúng 1 ngày bàn giao (không tính giờ).\n- Ngày tạo: khoảng từ ngày – đến ngày, lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Hợp đồng > biên bản (tối đa 1) > dòng hàng (hàng, ĐVT, SL theo hợp đồng / đã xuất / đã trả / đã nghiệm thu) > dòng thông '
     'tin chi tiết (Seri, Ngày bàn giao, Thời gian bảo hành, Hết hạn, Ghi chú).'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- 1 hợp đồng chỉ có 1 biên bản.\n- SL theo hợp đồng = hợp đồng gốc + phụ lục bổ sung trừ phụ lục giảm; gộp theo hàng + ĐVT.\n'
     '- SL đã nghiệm thu không lớn hơn SL đã xuất + SL đã trả; Lưu và duyệt: = SL đã xuất.\n- Hết hạn = Ngày bàn giao + Thời gian bảo hành (ngày).'),
    ('7. Phân quyền cấp',
     '- Tạo biên bản bàn giao nghiệm thu: nút Tạo mới, Lưu nháp / Lưu và tiếp tục / Lưu và duyệt, tải file; Sửa / Xóa biên bản '
     'Đang tạo do mình tạo.\n'
     '- Xem biên bản bàn giao nghiệm thu — mức: Tổng công ty / Công ty / Phòng ban (chỉ áp cho lối "tất cả").\n'
     '- Không quyền: biên bản mình tạo; chi tiết xem được cả biên bản mình là NVKD.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a–b là khoảng số thứ tự trang đang xem, N là tổng biên bản khớp bộ lọc trong phạm vi lối vào.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản dùng trong file: K (có quyền Tạo), V1 / V2 / V3 (quyền Xem 3 mức), N (không quyền), DNS Admin (Super admin).\n'
     '- Lưu ý: Lưu nháp chỉ bắt buộc hợp đồng; các ô có dấu * (SĐT người nhận, NV kỹ thuật, Ngày bàn giao, File) chỉ bắt buộc khi '
     'Lưu và duyệt.\n'
     '- Lưu ý: giữ như hệ thống cũ — Lưu và duyệt KHÔNG cần quyền duyệt riêng; trạng thái Chờ duyệt không có thao tác tạo ra.\n'
     '- Lưu ý: Super admin chưa được tích quyền Tạo thì KHÔNG có nút Tạo mới / Sửa / Xóa.\n'
     '- Màn Tạo / Sửa / Chi tiết là TRANG riêng, không phải cửa sổ nổi; Lưu xong về danh sách lối "tất cả".'),
]

SCREEN = ListScreen(menu=MENU, title='Biên bản bàn giao nghiệm thu', total=8271, quick_label='số BBBG',
                    quick_sample='TPE.BBBG.0273', quick_hit='8 biên bản TPE.BBBG.02730–02738',
                    filters=[('Trạng thái', 'Đã duyệt'), ('Người tạo', 'Nguyễn Diệu Hoa')], unit='biên bản')

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.raw([open_menu_case(SCREEN, pre=PRE_LIST)], [[1, 10, 16, 19]])
S1.add('Mở từ phân hệ CSKH sau bán', 'P0', PRE_LIST, ['Đăng nhập.', MENU_CC], '—',
       ['Mở cùng màn, tiêu đề "Biên bản bàn giao nghiệm thu".', 'Cùng phạm vi với lối từ phân hệ Công việc: "Hiển thị 1–10 / 8271".'], 1)
S1.add('Mở lối BB bàn giao nghiệm thu theo NV', 'P0',
       [PRE_LIST, 'DNS Admin là NVKD của 1 biên bản TPE.BBBG.02737.'], ['Đăng nhập.', MENU_NV], '—',
       ['Tiêu đề "Biên bản bàn giao nghiệm thu theo nhân viên".', 'Chỉ 1 dòng TPE.BBBG.02737, "Hiển thị 1–1 / 1".',
        'Không có ô lọc Công ty – Phòng ban.'], [1, 16])
S1.add('Đang ở lối này bấm sang lối khác', 'P1', PRE_LIST,
       [MENU, ADV, 'Chọn Trạng thái = Đã duyệt.', MENU_NV], '—',
       ['Màn đổi sang lối "theo NV", bộ lọc Trạng thái không còn, 1 dòng.', 'Quay lại lối "tất cả" thì bộ lọc riêng của lối đó.'], 1)
S1.raw([weird_param_case('005', SCREEN, 'chỉ biên bản mình tạo — tiêu đề "Biên bản bàn giao nghiệm thu của tôi"')], [[1]])
S1.add('Tiêu đề màn hình', 'P1', PRE_LIST, [MENU, 'Quan sát thanh tiêu đề, tiêu đề bảng, tab trình duyệt.'], '—',
       ['Thanh tiêu đề, tab và tiêu đề bảng: "Biên bản bàn giao nghiệm thu".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE_LIST, [MENU, 'Quan sát khối bộ lọc, thanh công cụ, cột Hành động.'], '—',
       ['Khối "Bộ lọc danh sách": ô tìm nhanh (gợi ý "Tìm theo số BBBG"), Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc.',
        'Thanh công cụ: Tạo mới, In danh sách, Xuất Excel, nút biểu tượng cột.',
        'Dòng Đang tạo của mình: Sửa, Xóa, nút ba chấm (In, Lịch sử); dòng Đã duyệt: In, Lịch sử.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Đọc tiêu đề cột.'], '—',
       ['Đúng 13 cột: STT, Số BBBG, Ngày BGNT, Số hợp đồng, Khách hàng, NVKD, NV kỹ thuật, Ngày tạo, Người tạo, Ngày cập nhật, '
        'Người cập nhật, Trạng thái, Hành động.'], 4)
S1.add('Không có cột ẩn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa từng lưu cấu hình cột.'], [MENU, 'Bấm nút biểu tượng cột.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột" ghi "Đang chọn 13/13 cột".'], 5)
S1.add('Dữ liệu trên dòng khớp biên bản', 'P0', [PRE_LIST, B36], [MENU, 'Đối chiếu dòng TPE.BBBG.02736.'], '—',
       ['Ngày BGNT 09/11/2026 00:00, Số hợp đồng là liên kết, Khách hàng "CÔNG TY TNHH MORI LUBRICANTS VIỆT NAM", NVKD "Trần Thị '
        'Phương Nhung - HN_DAU", NV kỹ thuật "Nguyễn Thị Cần - HN_KD1", Ngày tạo 09/11/2026 14:30, Người tạo "DNS Admin - HDQT".',
        'Nhãn xanh lá "Đã duyệt".'], 6)
S1.add('Liên kết Số hợp đồng mở tab mới', 'P0', [PRE_LIST, B36], [MENU, 'Ở dòng TPE.BBBG.02736 bấm số hợp đồng.'], '—',
       ['Mở hợp đồng hãng ở hệ thống cũ trong TAB MỚI.', 'Tab danh sách giữ nguyên trang, bộ lọc.'], 6)
S1.add('Trạng thái bản ghi', 'P0', PRE_LIST, [MENU, 'Quan sát cột Trạng thái của 02738 và 02736.'], '—',
       ['02738: nhãn xám "Đang tạo".', '02736: nhãn xanh lá "Đã duyệt".'], 7)
S1.add('Danh sách chưa có dữ liệu', 'P1', ['Tài khoản mới, không có quyền nào, chưa lập biên bản nào, không là NVKD của biên bản nào.'],
       ['Đăng nhập.', MENU], '—', ['Bảng hiện "Không có dữ liệu phù hợp.".', 'Không báo lỗi.'], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_LIST, [MENU, 'Nhập "ZZZ999" vào ô tìm nhanh, bấm Tìm kiếm.'],
       'Ô tìm nhanh: ZZZ999', ['Bảng hiện "Không có dữ liệu phù hợp.".', 'Không báo lỗi.'], 9)
S1.add('Thay đổi số dòng / trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2.', 'Đổi Số dòng/trang từ 10 thành 20.'], 'Số dòng/trang: 20',
       ['Bảng hiện 20 biên bản, tự về trang 1, "Hiển thị 1–20 / 8271".', 'Ô có các lựa chọn 5, 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE_LIST, [MENU, 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 2: "Hiển thị 11–20 / 8271".', 'Bước 3: "Hiển thị 1–10 / 8271".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE_LIST, [MENU, 'Bấm ».', 'Bấm «.'], '—',
       ['Bước 2: trang 828, "Hiển thị 8271–8271 / 8271".', 'Bước 3: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE_LIST, [MENU, 'Ở trang 1 quan sát « ‹.', 'Ở trang cuối quan sát › ».'],
       '—', ['Trang 1: « và ‹ mờ.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE_LIST, [MENU, 'Sang trang 2, rồi trang 3.'], '—',
       ['Trang 2: STT 11–20; trang 3: STT 21–30.'], 15)
S1.add('Về trang 1 khi thay đổi bộ lọc', 'P0', PRE_LIST, [MENU, 'Sang trang 3.', ADV, 'Chọn Trạng thái = Đang tạo.'],
       'Trạng thái: Đang tạo', ['Tự nạp lại ở trang 1; "Hiển thị 1–2 / 2".'], 17)
S1.add('Sắp xếp tăng dần theo Số BBBG', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề cột Số BBBG.'], '—',
       ['DTTDETEK.BBBG.00001 ở trên cùng, rồi TPE.BBBG.00001, TPE.BBBG.00002…; mũi tên lên.'], 20)
S1.add('Sắp xếp giảm dần theo Số BBBG', 'P0', PRE_LIST, [MENU, 'Bấm tiêu đề Số BBBG 2 lần.'], '—',
       ['Số BBBG lớn nhất theo thứ chữ ở trên cùng, giảm dần; mũi tên xuống.'], 21)
S1.add('Sắp xếp theo Ngày tạo / Ngày cập nhật', 'P1', PRE_LIST, [MENU, 'Bấm tiêu đề Ngày tạo hai lần.', 'Bấm tiêu đề Ngày cập nhật.'],
       '—', ['Ngày tạo lần 1 cũ nhất trên, lần 2 mới nhất trên (TPE.BBBG.02738 10/11/2026 11:12).',
             'Ngày cập nhật sắp tăng dần.', 'Mặc định khi mới vào: Ngày tạo mới nhất trên.'], 22)
S1.add('Sắp xếp theo Ngày BGNT và Số hợp đồng', 'P1', PRE_LIST, [MENU, 'Bấm tiêu đề Ngày BGNT.', 'Bấm tiêu đề Số hợp đồng.'], '—',
       ['Lần lượt sắp theo ngày bàn giao, theo số hợp đồng (thứ tự chữ); về trang 1.'], 20)
S1.add('Cột không hỗ trợ sắp xếp', 'P2', PRE_LIST,
       [MENU, 'Bấm tiêu đề Khách hàng, NVKD, NV kỹ thuật, Người tạo, Người cập nhật, Trạng thái, Hành động.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự.'], 23)
S1.add('Giữ sắp xếp khi chuyển trang', 'P1', PRE_LIST, [MENU, 'Bấm Số BBBG (tăng).', 'Sang trang 2.'], '—',
       ['Trang 2 tiếp tục thứ tự tăng của Số BBBG.'], 24)
S1.add('Về trang 1 khi đổi sắp xếp', 'P1', PRE_LIST, [MENU, 'Sang trang 3.', 'Bấm tiêu đề Ngày tạo.'], '—', ['Về trang 1.'], 25)
S1.add('Bấm sắp xếp không làm vỡ bố cục bảng', 'P2', PRE_LIST, [MENU, 'Bấm tiêu đề Ngày tạo, Số BBBG nhiều lần.'], '—',
       ['Độ rộng các cột giữ nguyên, mũi tên sắp xếp không nhảy chỗ.'], 22)
S1.add('Phiên đăng nhập hết hạn khi đang ở danh sách', 'P2', [PRE_LIST, 'Phiên đăng nhập đã hết hạn.'], [MENU, 'Bấm sang trang 2.'],
       '—', ['Báo hết phiên đăng nhập, chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Tìm theo số BBBG chính xác', 'P0', PRE_LIST, [MENU, 'Nhập "TPE.BBBG.02736", bấm Tìm kiếm.'], 'Ô tìm nhanh: TPE.BBBG.02736',
       ['Chỉ còn 1 dòng, "Hiển thị 1–1 / 1".'], 26)
S2.add('Tìm theo một phần số BBBG', 'P0', PRE_LIST, [MENU, 'Nhập "TPE.BBBG.0273", bấm Tìm kiếm.'], 'Ô tìm nhanh: TPE.BBBG.0273',
       ['Còn 8 biên bản TPE.BBBG.02730–02738 (02732 không có trong lối này).'], 27)
S2.add('Ô tìm nhanh không tìm theo số hợp đồng', 'P1', PRE_LIST, [MENU, 'Nhập "HĐ_TPE_HN_KDTM_26_1363", bấm Tìm kiếm.'], '—',
       ['"Không có dữ liệu phù hợp." (ô tìm nhanh chỉ tìm theo số BBBG; tìm hợp đồng dùng ô Số hợp đồng).'], 27)
S2.add('Không phân biệt hoa / thường', 'P0', PRE_LIST, [MENU, 'Nhập "tpe.bbbg.02736", bấm Tìm kiếm.'], '—',
       ['Ra biên bản TPE.BBBG.02736 như khi gõ chữ hoa.'], 28)
S2.add('Có dấu / không dấu', 'P2', PRE_LIST, [MENU, 'Ở ô Số hợp đồng nhập "HD_TPE_HN_KDTM" (chữ D không gạch), bấm Tìm kiếm.'], '—',
       ['Kết quả theo cách so khớp của hệ thống: chữ Đ và D có thể không được coi là một; ghi nhận kết quả thực tế.',
        'Lưu ý: số hợp đồng có chữ Đ, nhập đúng "HĐ_" để tìm.'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE_LIST, [MENU, 'Nhập "999999999", bấm Tìm kiếm.'], '—', ['"Không có dữ liệu phù hợp.".'], 30)
S2.add('Ký tự đặc biệt', 'P2', PRE_LIST, [MENU, 'Nhập "@#$<>", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], '—',
       ['Bước 2: không lỗi, "Không có dữ liệu phù hợp.".', 'Bước 3: không lỗi; % được hiểu là ký tự đại diện nên ra cả 8271 biên bản.'],
       31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE_LIST, [MENU, 'Nhập "  TPE.BBBG.02736  ", bấm Tìm kiếm.'], '—',
       ['Ra biên bản TPE.BBBG.02736.'], 32)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "TPE.BBBG.02736", bảng còn 1 dòng.', ['Xóa hết chữ trong ô tìm nhanh.', 'Bấm Tìm kiếm.'], '—',
       ['Hiện lại đủ 8271 biên bản.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE_LIST,
       [MENU, 'Nhập "TPE.BBBG.02736", nhấn Enter.', 'Làm mới, nhập lại, bấm Tìm kiếm.'], '—',
       ['Cả 2 cách đều ra TPE.BBBG.02736, về trang 1.', 'Chỉ gõ mà chưa Enter / Tìm kiếm thì danh sách chưa đổi.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P1', [PRE_LIST, 'Chưa lọc gì trong 10 phút.'], [MENU, ADV], '—',
       ['Các ô Công ty, Phòng ban, Ngày BGNT, Số hợp đồng, Khách hàng, NV kỹ thuật, Người tạo, Trạng thái, Ngày tạo đều trống.',
        'Đủ 8271 biên bản.'], 36)
S2.add('Lọc Ngày BGNT', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày BGNT = 09/11/2026.'], '—',
       ['Còn các biên bản có ngày bàn giao 09/11/2026 bất kể giờ: TPE.BBBG.02737 (05:04) và 02736 (00:00).'], 37)
S2.add('Lọc Số hợp đồng', 'P0', PRE_LIST, [MENU, ADV, 'Nhập "KD3_26_08" vào ô Số hợp đồng, nhấn Enter.'], '—',
       ['Còn các biên bản có số hợp đồng chứa chuỗi (có TPE.BBBG.02735, 02734).', 'Chưa nhấn Enter thì danh sách chưa đổi.'], 37)
S2.add('Lọc Khách hàng', 'P0', PRE_LIST, [MENU, ADV, 'Gõ "MORI" vào ô Khách hàng, chọn "CÔNG TY TNHH MORI LUBRICANTS VIỆT NAM".'], '—',
       ['Gõ 1 ký tự chưa hiện gợi ý; từ 2 ký tự hiện tối đa 30 khách hàng.', 'Chọn xong lọc ngay, có TPE.BBBG.02736.'], 37)
S2.add('Lọc NV kỹ thuật', 'P0', PRE_LIST, [MENU, ADV, 'Chọn NV kỹ thuật = "Nguyễn Thị Cần".'], '—',
       ['Lọc ngay; còn các biên bản có NV kỹ thuật Nguyễn Thị Cần (có 02736, 02734).'], 37)
S2.add('Lọc Người tạo', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Người tạo = "Nguyễn Diệu Hoa".'], '—',
       ['Còn các biên bản do Nguyễn Diệu Hoa tạo (có 02731, 02730).'], 37)
S2.add('Lọc Trạng thái', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đang tạo.', 'Đổi thành Chờ duyệt.'], '—',
       ['Ô có 3 lựa chọn theo thứ tự: Đang tạo, Chờ duyệt, Đã duyệt.', 'Đang tạo: 2 biên bản 02738, 02737.',
        'Chờ duyệt: "Không có dữ liệu phù hợp.".'], [37, 40])
S2.add('Lọc Ngày tạo lấy trọn ngày biên', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Ngày tạo 09/11/2026 – 10/11/2026.'], '—',
       ['Còn 02738 (10/11 11:12), 02737 (09/11 14:33), 02736 (09/11 14:30), 02735 (09/11 14:28).',
        'Bỏ trống ngày cuối vẫn lọc được.'], 37)
S2.add('Lọc kết hợp nhiều tiêu chí', 'P0', PRE_LIST, [MENU, ADV, 'Chọn NV kỹ thuật = Nguyễn Thị Cần.', 'Chọn Trạng thái = Đang tạo.'],
       '—', ['"Không có dữ liệu phù hợp." (2 biên bản Đang tạo không có NV kỹ thuật Nguyễn Thị Cần).'], [38, 40])
S2.add('Kết hợp tìm kiếm và bộ lọc', 'P1', PRE_LIST,
       [MENU, 'Nhập "TPE.BBBG.0273", bấm Tìm kiếm.', ADV, 'Chọn Trạng thái = Đã duyệt.'], '—',
       ['Còn 6 biên bản 02730, 02731, 02733–02736.'], 39)
S2.add('Tổng số và phân trang sau lọc', 'P0', PRE_LIST, [MENU, ADV, 'Chọn Trạng thái = Đã duyệt.', 'Bấm trang cuối.'], '—',
       ['Dòng "Hiển thị" ghi tổng 8269.', 'Trang cuối STT liên tục tới 8269.'], [41, 42])
S2.add('Sắp xếp sau lọc', 'P1', 'Đang tìm "TPE.BBBG.0273" (8 biên bản).', ['Bấm tiêu đề Số BBBG.'], '—',
       ['Chỉ 8 biên bản được sắp tăng dần; ô tìm nhanh giữ nguyên.'], 43)
S2.add('Làm mới xóa toàn bộ điều kiện', 'P0', 'Đang tìm "TPE", lọc Trạng thái, NV kỹ thuật, sắp Số BBBG, ở trang 2.',
       ['Bấm Làm mới.'], '—', ['Mọi ô kể cả ô tìm nhanh về trống, bỏ sắp xếp, nạp lại trang 1, đủ 8271 biên bản.',
                              'Vẫn ở đúng lối vào đang xem.'], 44)
S2.raw(filter_memory_cases(SCREEN, len(S2) + 1), [[45], [45], [45], [48], [47]])
S2.raw(combo_cases(SCREEN, len(S2) + 1), [[38, 39], [38], [38, 39], [33]])
S2.raw(org_cases(SCREEN, len(S2) + 1), [[37], [37], [37]])
S2.add('Tải lại trang (F5) khi đang lọc', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Đã duyệt, chưa mở màn chi tiết.'],
       ['Nhấn F5.'], '—', ['Bộ lọc trở về trống, đủ 8271 biên bản (bộ lọc chỉ nhớ khi đi vào màn chi tiết / sửa của màn).'], 46)
S2.add('Lối theo NV không có ô Công ty – Phòng ban', 'P1', PRE_LIST, [MENU_NV, ADV], '—',
       ['Khối lọc có Ngày BGNT, Số hợp đồng, Khách hàng, NV kỹ thuật, Người tạo, Trạng thái, Ngày tạo; không có Công ty, Phòng ban.'], 37)
S2.add('Ô Công ty chỉ có hiệu lực với quyền Tổng công ty', 'P1', [ACC_V2], ['Đăng nhập V2.', MENU, ADV], '—',
       ['Có khối Công ty – Phòng ban nhưng ô Công ty khóa theo công ty TPSG; chọn Phòng ban lọc được.'], 37)
S2.add('Cài đặt bộ lọc: ẩn một tiêu chí', 'P1', PRE_LIST, [MENU, 'Bấm Cài đặt bộ lọc, bỏ tích Khách hàng, bấm Lưu.'], '—',
       ['Cửa sổ liệt kê 8 mục: Công ty – Phòng ban, Ngày BGNT, Số hợp đồng, Khách hàng, NV kỹ thuật, Người tạo, Trạng thái, Ngày tạo.',
        'Báo "Cập nhật thành công"; khối Tìm kiếm nâng cao không còn ô Khách hàng.'], 37)
S2.add('Cài đặt bộ lọc: bỏ tích tiêu chí đang có giá trị', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Đang tạo.'],
       ['Bấm Cài đặt bộ lọc, bỏ tích Trạng thái, bấm Lưu.'], '—', ['Ô ẩn, giá trị bị bỏ, nạp lại đủ 8271 biên bản.'], 44)
S2.add('Cài đặt bộ lọc: Khôi phục mặc định và đóng không lưu', 'P2', 'Đã ẩn ô Khách hàng.',
       ['Bấm Cài đặt bộ lọc, Khôi phục mặc định, bấm Đóng.', 'Mở lại, Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 1: không lưu, Khách hàng vẫn ẩn.', 'Bước 2: tích đủ 8 mục, Khách hàng hiện lại.'], 36)
S2.add('Cài đặt bộ lọc riêng từng lối vào', 'P2', PRE_LIST, ['Ở lối "tất cả" ẩn ô Ngày tạo, Lưu.', MENU_NV, ADV], '—',
       ['Lối "theo NV" vẫn có ô Ngày tạo (cấu hình lưu riêng theo lối vào).'], 36)

# ============================================================== III. THÊM MỚI
S3 = Sec(3)
S3.add('Điều hướng vào màn Tạo mới', 'P0', PRE_FORM, ['Đăng nhập K.'] + TAO, '—',
       ['Mở TRANG "Tạo biên bản bàn giao nghiệm thu", tab cùng tiêu đề.'], 49)
S3.add('Tiêu đề và dòng người tạo', 'P1', PRE_FORM, TAO + ['Quan sát đầu khối Thông tin chung.'], '—',
       ['Góc phải "<tên K> - <ngày giờ hiện tại>".', 'Không có ô Số BBBG (mã tự sinh khi lưu).'], 50)
S3.add('Các trường, khối và nút', 'P0', PRE_FORM, TAO, '—',
       ['Thông tin chung: Hợp đồng/đơn hàng, Khách hàng, CMT/MST, Số điện thoại, Địa chỉ, Nhân viên kinh doanh, Phòng ban, Số điện '
        'thoại người nhận, Người nhận bàn giao, Nhân viên kỹ thuật, Ngày bàn giao, Ghi chú.',
        'Khối "File đính kèm" có nút "Thêm tài liệu"; khối "Hàng hoá": STT, Tên hàng, Mã hàng hóa, Model, ĐVT, Số lượng theo hợp '
        'đồng, Số lượng đã xuất, Số lượng đã trả, Số lượng đã nghiệm thu, Thông tin chi tiết (Seri, Ngày bàn giao, Thời gian bảo hành '
        '(ngày), Hết hạn, Ghi chú).', 'Chân màn theo thứ tự: Lưu nháp, Lưu và duyệt, Lưu và tiếp tục, Quay lại.'], [51, 54])
S3.add('Trường bắt buộc / không bắt buộc', 'P0', PRE_FORM, TAO + ['Quan sát dấu *.'], '—',
       ['Có dấu *: Hợp đồng/đơn hàng, Số điện thoại người nhận, Nhân viên kỹ thuật, Ngày bàn giao, File đính kèm.',
        '6 ô Khách hàng, CMT/MST, Số điện thoại, Địa chỉ, Nhân viên kinh doanh, Phòng ban khóa.',
        'Lưu ý: khi Lưu nháp chỉ Hợp đồng/đơn hàng thật sự bắt buộc; các ô * còn lại bắt buộc khi Lưu và duyệt.'], 52)
S3.add('Giá trị mặc định', 'P0', PRE_FORM, TAO, '—',
       ['Ô Hợp đồng/đơn hàng gợi ý "Chọn hợp đồng/đơn hàng"; 6 ô khóa gợi ý "Tự điền theo hợp đồng".',
        'SĐT người nhận gợi ý "Nhập số điện thoại", Người nhận "Nhập người nhận bàn giao", NV kỹ thuật "Chọn nhân viên kỹ thuật", '
        'Ngày bàn giao "dd/mm/yyyy hh:mm", Ghi chú "Nhập ghi chú" — đều trống.',
        'Bảng Hàng hoá ghi "Chưa có hàng hóa nào"; File đính kèm "Chưa có tài liệu nào."'], 53)
S3.add('Mở popup Chọn hợp đồng/đơn hàng', 'P0', PRE_FORM, TAO + ['Bấm ô Hợp đồng/đơn hàng.'], '—',
       ['Popup "Chọn hợp đồng/đơn hàng", phụ đề "Hợp đồng có hiệu lực / đã thanh lý của công ty bạn, đã xuất hết hàng, chưa có biên '
        'bản bàn giao nghiệm thu".', 'Ô "Tìm theo số hợp đồng", ô Loại hợp đồng, Tìm kiếm, Làm mới; cột STT, Loại hợp đồng, Số hợp '
        'đồng, Khách hàng, Tổng thanh toán, Ngày duyệt, Người duyệt; nút Đóng.',
        'Hợp đồng duyệt gần nhất ở trên (HĐ_TPE_HN_KD1_26_1118_2110 21/10/2026 10:28).'], [51, 53])
S3.add('Popup: lọc Loại hợp đồng tự lọc', 'P1', PRE_FORM, TAO + ['Bấm ô Hợp đồng/đơn hàng.', ADV, 'Chọn Loại hợp đồng = Đơn hàng nguyên tắc.'],
       '—', ['Ô có 4 lựa chọn: Hợp đồng bán hàng hóa - vật tư, Hợp đồng dự án, Đơn hàng nguyên tắc, Hợp đồng HRM.',
             'Chọn xong danh sách lọc ngay, về trang 1, chỉ còn Đơn hàng nguyên tắc.'], 37)
S3.add('Popup: tìm theo số hợp đồng', 'P1', PRE_FORM, TAO + ['Bấm ô Hợp đồng/đơn hàng.', 'Nhập "1118_2110", bấm Tìm kiếm.'], '—',
       ['Còn HĐ_TPE_HN_KD1_26_1118_2110.'], 26)
S3.add('Popup: không có hợp đồng phù hợp', 'P2', PRE_FORM, TAO + ['Bấm ô Hợp đồng/đơn hàng.', 'Nhập "ZZZ", bấm Tìm kiếm.'], '—',
       ['Hiện "Không có hợp đồng nào phù hợp. Chỉ hợp đồng có hiệu lực / đã thanh lý của công ty bạn, đã xuất hết hàng và chưa có biên '
        'bản bàn giao nghiệm thu mới hiện ở đây."'], 40)
S3.add('Chọn hợp đồng thì điền thông tin và hàng hoá', 'P0', PRE_FORM, CHON, '—',
       ['Khách hàng "CÔNG TY TNHH DỊCH VỤ Ô TÔ QUANG TRUNG", NVKD "Lê Huy Thắng", Phòng ban "PHÒNG THIẾT BỊ Ô TÔ 1", Người nhận '
        '"Nguyễn Hồng Vương", SĐT người nhận 0832551333 được điền.',
        'Bảng 1 hàng "Lọc sàn phòng sơn sợi thủy tinh 0,8x20m, 3540g/m2", VITO-PA50, PA50, Cuộn, SL theo hợp đồng 3, đã xuất 3, đã '
        'trả 0, SL đã nghiệm thu trống.'], [53, 269])
S3.add('Nhập SL đã nghiệm thu tự thêm dòng chi tiết', 'P0', PRE_FORM, CHON + ['Chọn Ngày bàn giao = hôm nay 09:00.', 'Nhập SL đã nghiệm thu = 3.'],
       '—', ['Hàng không bắt buộc seri: thêm 1 dòng chi tiết; Ngày bàn giao dòng = hôm nay; Thời gian bảo hành = mặc định của hàng.',
             'Hết hạn = Ngày bàn giao + số ngày bảo hành.', 'Hàng bắt buộc seri: thêm đủ 3 dòng.'], [53, 269])
S3.add('Đổi Ngày bàn giao ghi đè ngày các dòng chi tiết', 'P1', PRE_FORM, DU + ['Đổi Ngày bàn giao sang hôm qua 08:00.'], '—',
       ['Ngày bàn giao mọi dòng chi tiết đổi theo (chỉ phần ngày); Hết hạn tính lại.'], 53)
S3.add('Lưu nháp với dữ liệu hợp lệ đầy đủ', 'P0', PRE_FORM, DU + ['Nhập Ghi chú, nhập Seri "SN001".', 'Bấm Lưu nháp.'],
       ['Ghi chú: Bàn giao lần 1', 'Seri: SN001'],
       ['Báo ' + OKC + ', về danh sách lối "tất cả".', 'Dòng mới trên cùng mã TPE.BBBG.NNNNN kế tiếp, Số hợp đồng '
        'HĐ_TPE_HN_KD1_26_1118_2110, nhãn xám "Đang tạo".'], [55, 79, 85])
S3.add('Lưu nháp chỉ với hợp đồng', 'P0', PRE_FORM, CHON + ['Bấm Lưu nháp.'], 'Các ô khác để trống',
       ['Lưu được, biên bản Đang tạo; Ngày BGNT, NV kỹ thuật trống trên danh sách.'], [56, 57])
S3.add('Dữ liệu sau lưu', 'P0', PRE_FORM, DU + ['Nhập Seri "SN001", Thời gian bảo hành 365.', 'Bấm Lưu nháp.', 'Bấm số biên bản vừa tạo.'],
       'Thời gian bảo hành: 365',
       ['Chi tiết đúng hợp đồng, khách hàng, NV kỹ thuật Nguyễn Thị Cần, Ngày bàn giao hôm nay 09:00.',
        'Dòng hàng SL đã nghiệm thu 3, Seri SN001, Bảo hành 365, Hết hạn = hôm nay + 365 ngày.'], 58)
S3.add('Trạng thái mặc định sau lưu', 'P0', PRE_FORM, DU + ['Bấm Lưu nháp.'], '—',
       ['Biên bản ở trạng thái Đang tạo (nhãn xám); có nút Sửa, Xóa ở dòng.'], 59)
S3.add('Lịch sử tạo', 'P1', PRE_FORM, DU + ['Bấm Lưu nháp.', 'Ở dòng biên bản mới bấm ba chấm > Lịch sử.'], '—',
       ['Có 1 mốc "Tạo mới", người thực hiện K.'], [60, 176])
S3.add('Lưu nháp khi chưa chọn hợp đồng', 'P0', PRE_FORM, TAO + ['Bấm Lưu nháp.'], '—',
       ['Ô Hợp đồng/đơn hàng viền đỏ, dưới ô ' + HD + '.', 'Thông báo ' + INC + '; không lưu.'], [61, 70, 80])
S3.add('SĐT người nhận sai định dạng', 'P0', PRE_FORM, CHON + ['Sửa SĐT người nhận thành "12345".', 'Bấm Lưu nháp.'], 'SĐT: 12345',
       ['Dưới ô ' + PHONE + '; thông báo ' + CHK + '; không lưu.',
        'Hợp lệ: bắt đầu bằng 0, tổng 10–12 chữ số (vd 0832551333).'], [62, 70, 81])
S3.add('SĐT có chữ hoặc ký tự đặc biệt', 'P1', PRE_FORM, CHON + ['Nhập SĐT người nhận "09abc#1234".', 'Bấm Lưu nháp.'], '—',
       ['Báo ' + PHONE + '.'], 63)
S3.add('SĐT dưới / đúng / vượt độ dài', 'P1', PRE_FORM,
       CHON + ['Nhập SĐT "091234567" (9 số), Lưu nháp.', 'Nhập "091234567890" (12 số), Lưu nháp.', 'Nhập "0912345678901" (13 số).'],
       '—', ['9 số: ' + PHONE + '.', '12 số: hợp lệ.', '13 số: ' + PHONE + '.'], [64, 65, 66])
S3.add('Người nhận / Seri / Ghi chú dòng vượt 255 ký tự', 'P2', PRE_FORM, DU + ['Dán 256 ký tự vào ô Seri.', 'Bấm Lưu nháp.'], '—',
       ['Dưới ô Seri "Tối đa 255 ký tự"; 255 ký tự thì lưu được.'], [65, 66])
S3.add('Ghi chú dài và ký tự đặc biệt', 'P2', PRE_FORM, CHON + ['Nhập Ghi chú "<b>Test</b> & @#$%" dài 1.000 ký tự.', 'Bấm Lưu nháp.'],
       '—', ['Lưu được; màn chi tiết và bản in hiện nguyên chuỗi, không in đậm.', 'Ghi chú tối đa 65.000 ký tự.'], [63, 65])
S3.add('Người nhận chỉ khoảng trắng', 'P2', PRE_FORM, CHON + ['Bấm × xóa ô Người nhận, nhập "   ".', 'Bấm Lưu nháp.'], '—',
       ['Lưu được (Người nhận không bắt buộc).'], [68, 69])
S3.add('Nút × xóa nhanh ô Người nhận và SĐT', 'P2', PRE_FORM, CHON + ['Bấm × ở ô Người nhận bàn giao, rồi ở ô SĐT người nhận.'], '—',
       ['2 ô trở về trống, nút × biến mất; lỗi cũ dưới ô (nếu có) tự xóa.'], 71)
S3.add('SL đã nghiệm thu vượt SL đã xuất', 'P0', PRE_FORM, CHON + ['Nhập SL đã nghiệm thu = 5.', 'Bấm Lưu nháp.'], 'SL: 5',
       ['Dưới ô "Không được lớn hơn số lượng đã xuất (3)"; không lưu.',
        'Hàng có SL đã trả > 0 thì câu là "Không được lớn hơn tổng số lượng đã xuất và đã trả (X)".'], [62, 70])
S3.add('SL đã nghiệm thu nhập chữ', 'P0', PRE_FORM, CHON + ['Gõ "abc" vào ô SL đã nghiệm thu.'], '—',
       ['Chữ không nhận; không tự thêm dòng chi tiết.'], [62, 74])
S3.add('Hàng bắt buộc seri lệch số dòng', 'P0', ['Hợp đồng có 1 hàng thuộc nhóm bắt buộc seri, đã xuất 2.'] + [ACC_K],
       TAO + ['Chọn hợp đồng đó, nhập SL = 2 (tự thêm 2 dòng).', 'Đổi SL = 1, bấm Lưu nháp.'], '—',
       ['Dưới ô SL "Phải bằng số dòng seri (2)"; nút Xóa dòng hiện ở các dòng chi tiết.',
        'Bấm Xóa dòng bỏ 1 dòng thì lưu được.'], [62, 99])
S3.add('Ngày bàn giao không chọn được ngày tương lai', 'P1', PRE_FORM, CHON + ['Mở ô Ngày bàn giao.'], '—',
       ['Các ngày sau hôm nay bị mờ, không chọn được.'], 62)
S3.add('Trùng hợp đồng: hợp đồng đã có biên bản', 'P0', [PRE_FORM, 'Tài khoản K2 vừa lập biên bản cho HĐ_TPE_HN_KD1_26_1118_2110 '
                                                                 'sau khi K mở popup.'],
       CHON + ['Bấm Lưu nháp.'], '—',
       ['Dưới ô Hợp đồng/đơn hàng ' + DUP + '; không lưu.',
        'Mở lại popup: hợp đồng này không còn trong danh sách.'], [67, 75, 82])
S3.add('Có Ngày bàn giao nhưng hợp đồng còn hàng chưa xuất', 'P1',
       [ACC_K, 'Hợp đồng X đã chọn trong form, sau đó phát sinh phụ lục bổ sung 2 hàng chưa xuất.'],
       TAO + ['Chọn hợp đồng X, chọn Ngày bàn giao, bấm Lưu nháp.'], '—',
       ['Dưới ô Hợp đồng "Hợp đồng chưa xuất hết hàng"; dưới SL hàng đó "Chưa xuất hết hàng"; không lưu.',
        'Không chọn Ngày bàn giao thì Lưu nháp vẫn được.'], [62, 304])
S3.add('Lỗi biến mất sau khi sửa', 'P1', PRE_FORM, TAO + ['Bấm Lưu nháp (báo lỗi).', 'Chọn hợp đồng.'], '—',
       ['Chữ đỏ dưới ô Hợp đồng biến mất ngay khi chọn.'], 71)
S3.add('Đổi hợp đồng khi đã chọn', 'P0', PRE_FORM, CHON + ['Mở lại popup, bấm dòng hợp đồng khác.', 'Bấm Hủy.', 'Làm lại, bấm Xác nhận.'],
       '—', ['Hộp "Xác nhận thay đổi hợp đồng": "Nếu bạn thay đổi hợp đồng các thông tin hiện có sẽ bị thay thế! Bạn có chắc chắn muốn '
             'thay đổi?".', 'Hủy: giữ hợp đồng cũ.', 'Xác nhận: thông tin chung và bảng Hàng hoá thay theo hợp đồng mới.'], 99)
S3.add('Lưu và tiếp tục với dữ liệu hợp lệ', 'P0', PRE_FORM, DU + ['Bấm Lưu và tiếp tục.'], '—',
       ['Báo ' + OKC + ', ở lại màn Tạo với form trống (bảng "Chưa có hàng hóa nào").',
        'Mở popup: hợp đồng vừa lập không còn.'], [72, 76, 77])
S3.add('Lưu và tiếp tục khi thiếu hợp đồng', 'P1', PRE_FORM, TAO + ['Bấm Lưu và tiếp tục.'], '—',
       [HD + ' dưới ô; không lưu, form giữ nguyên.'], 73)
S3.add('Lưu và tiếp tục khi SĐT sai', 'P2', PRE_FORM, CHON + ['Nhập SĐT "123".', 'Bấm Lưu và tiếp tục.'], '—',
       [PHONE + '; không lưu.'], 74)
S3.add('Đóng sau Lưu và tiếp tục', 'P2', PRE_FORM, DU + ['Bấm Lưu và tiếp tục.', 'Bấm Quay lại.'], '—',
       ['Về danh sách ngay (form trống, không hỏi); biên bản vừa lưu có trong danh sách.'], 78)
S3.add('Lưu nháp: màn là trang, không còn form', 'P2', PRE_FORM, DU + ['Bấm Lưu nháp.', 'Bấm Tạo mới lại.'], '—',
       ['Lưu xong về danh sách (không còn form).', 'Mở Tạo mới lại thì form trống.'], [83, 84])
S3.add('Quay lại khi chưa nhập gì', 'P1', PRE_FORM, TAO + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 93)
S3.add('Quay lại khi đã chọn / nhập', 'P0', PRE_FORM, CHON + ['Bấm Quay lại.'], '—',
       ['Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" với nút Thoát, Ở lại.',
        'Màn là trang nên không có nút X đóng form.'], [94, 95])
S3.add('Chọn Thoát', 'P1', PRE_FORM, CHON + ['Bấm Quay lại.', 'Bấm Thoát.'], '—', ['Về danh sách, không tạo biên bản.'], 96)
S3.add('Chọn Ở lại', 'P1', PRE_FORM, CHON + ['Bấm Quay lại.', 'Bấm Ở lại.'], '—', ['Ở lại form, dữ liệu đã chọn / nhập giữ nguyên.'], 97)
S3.add('Nhập rồi xóa hết', 'P2', PRE_FORM, TAO + ['Nhập Ghi chú rồi xóa hết.', 'Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 98)
S3.add('Để màn lâu không thao tác', 'P2', [PRE_FORM, 'Đã mở màn, để nguyên 30 phút.'], DU + ['Bấm Lưu nháp.'], '—',
       ['Còn phiên: lưu bình thường.', 'Hết phiên: báo hết phiên, về màn đăng nhập, không lưu.'], 100)
S3.add('Bấm Lưu nháp liên tục', 'P1', PRE_FORM, DU + ['Bấm Lưu nháp 3 lần thật nhanh.'], '—',
       ['Nút khóa trong lúc lưu; chỉ tạo 1 biên bản.'], 101)
S3.add('Hai tab cùng lập cho 1 hợp đồng', 'P1', [PRE_FORM, 'Tab 1 và tab 2 cùng mở form, cùng chọn HĐ_TPE_HN_KD1_26_1118_2110.'],
       ['Tab 1 bấm Lưu nháp.', 'Tab 2 bấm Lưu nháp.'], '—',
       ['Tab 1 lưu được.', 'Tab 2 báo ' + DUP + ' dưới ô Hợp đồng, không tạo biên bản thứ 2.'], 102)
S3.add('File sai định dạng / quá 30 MB', 'P1', PRE_FORM, CHON + ['Bấm Thêm tài liệu, chọn "bang.xlsx".', 'Chọn file pdf 35 MB.'],
       ['File: bang.xlsx', 'File: 35 MB'],
       ['Báo file không hợp lệ, không thêm (chỉ nhận pdf, jpg, jpeg, png, docx).', 'File 35 MB báo vượt dung lượng 30 MB, không thêm.'],
       62)
S3.add('Không có quyền Tạo', 'P1', [ACC_N], ['Đăng nhập N.', MENU], '—',
       ['Không có nút Tạo mới.', 'Mở thẳng màn Tạo, chọn hợp đồng, bấm Lưu nháp: hệ thống từ chối, báo không có quyền.'], [52, 295])

# ============================================================== IV. CHỈNH SỬA
S4 = Sec(4)
S4.add('Mở màn Sửa từ cột Hành động', 'P0', PRE_EDIT, ['Đăng nhập K.'] + SUA, '—',
       ['Mở trang "Sửa biên bản bàn giao nghiệm thu: TPE.BBBG.02740".'], 103)
S4.add('Mở màn Sửa từ màn chi tiết', 'P1', PRE_EDIT, [MENU, 'Bấm TPE.BBBG.02740.', 'Bấm Sửa ở chân màn.'], '—',
       ['Mở màn Sửa của biên bản.'], 103)
S4.add('Dữ liệu điền đúng', 'P0', [PRE_LIST, B38], ['Đăng nhập DNS Admin.', MENU, 'Ở dòng TPE.BBBG.02738 bấm Sửa.'], '—',
       ['Hợp đồng HĐ_TPE_HN_KDTM_26_1363_21.10, Khách hàng "HỘ KINH DOANH NGUYỄN VĂN THẮNG", NVKD Nguyễn Văn Thắng, Phòng ban '
        '"PHÒNG KINH DOANH THƯƠNG MẠI", SĐT người nhận 0932936899.', 'NV kỹ thuật, Ngày bàn giao trống.',
        'Bảng: Má phanh trước UP PARTS…, SL theo hợp đồng 10, đã xuất 10, SL đã nghiệm thu 0.'], 104)
S4.add('Trường được / không được sửa', 'P0', PRE_EDIT, SUA, '—',
       ['Sửa được: Hợp đồng (chọn lại qua popup), SĐT người nhận, Người nhận, NV kỹ thuật, Ngày bàn giao, Ghi chú, File, SL đã '
        'nghiệm thu, thông tin chi tiết.', 'Khóa: Khách hàng, CMT/MST, Số điện thoại, Địa chỉ, NVKD, Phòng ban, SL theo hợp đồng / '
        'đã xuất / đã trả.', 'SĐT người nhận KHÔNG có dấu * ở màn Sửa.'], 105)
S4.add('Các nút', 'P1', PRE_EDIT, SUA, '—', ['Chân màn: Lưu nháp, Lưu và duyệt, Quay lại; không có Lưu và tiếp tục.'], 106)
S4.add('Sửa một trường', 'P0', PRE_EDIT, SUA + ['Sửa Ghi chú thành "Nháp lần 2".', 'Bấm Lưu nháp.'], 'Ghi chú: Nháp lần 2',
       ['Báo ' + OKE + ', về danh sách; biên bản vẫn Đang tạo.', 'Chi tiết hiện Ghi chú mới.'], [107, 110])
S4.add('Sửa nhiều trường', 'P1', PRE_EDIT, SUA + ['Chọn NV kỹ thuật, Ngày bàn giao, thêm file bien_ban.pdf.', 'Bấm Lưu nháp.'], FILE,
       ['Lưu được; chi tiết hiện NV kỹ thuật, Ngày bàn giao mới và có thêm bien_ban.pdf.'], 108)
S4.add('Giữ nguyên giá trị khi Lưu không đổi', 'P1', PRE_EDIT, SUA + ['Không đổi gì, bấm Lưu nháp.'], '—',
       ['Lưu được, dữ liệu không đổi.', 'Lịch sử không có mốc "Thay đổi thông tin" mới.'], [109, 125, 182])
S4.add('Ngày / người cập nhật và lịch sử sau khi sửa', 'P0', PRE_EDIT, SUA + ['Sửa Ghi chú thành "Nháp lần 2", Lưu nháp.',
       'Quan sát cột Ngày cập nhật, Người cập nhật.', 'Mở Lịch sử của dòng.'], '—',
       ['Ngày cập nhật = thời điểm vừa lưu, Người cập nhật = K.',
        'Có mốc "Thay đổi thông tin" người thực hiện K, Ghi chú "Nháp" sang "Nháp lần 2".'], [111, 112, 177])
S4.add('Sửa nhiều thông tin cùng lúc ghi 1 mốc', 'P2', PRE_EDIT, SUA + ['Đổi Người nhận, Ghi chú, SL đã nghiệm thu, thêm 1 file.',
       'Lưu nháp.', 'Mở Lịch sử.'], '—',
       ['1 mốc "Thay đổi thông tin" gồm Người nhận bàn giao, Ghi chú, bảng Hàng hoá và File đính kèm.'], [178, 183])
S4.add('Bỏ trống hợp đồng không được', 'P1', PRE_EDIT, SUA, '—',
       ['Ô Hợp đồng/đơn hàng không có nút × (không bỏ trống được); chỉ chọn lại hợp đồng khác.'], [113, 117])
S4.add('SĐT sai định dạng khi sửa', 'P0', PRE_EDIT, SUA + ['Sửa SĐT người nhận thành "abc".', 'Bấm Lưu nháp.'], '—',
       [PHONE + '; ' + CHK + '; không lưu.'], [114, 117])
S4.add('SL vượt khi sửa', 'P1', PRE_EDIT, SUA + ['Sửa SL đã nghiệm thu thành 4.', 'Bấm Lưu nháp.'], '—',
       ['"Không được lớn hơn số lượng đã xuất (3)"; không lưu.'], 115)
S4.add('Chọn hợp đồng đã có biên bản khác', 'P1', [PRE_EDIT, 'Hợp đồng Y vừa được lập biên bản khác sau khi K mở popup.'],
       SUA + ['Chọn hợp đồng Y trong popup.'], '—',
       ['Báo "BBBG cho hợp đồng: <số Y> đã tồn tại."; form giữ hợp đồng cũ.',
        'Không tính trùng với chính biên bản TPE.BBBG.02740 (hợp đồng của chính nó vẫn chọn lại được).'], 116)
S4.add('Lỗi biến mất khi sửa hợp lệ', 'P2', PRE_EDIT, SUA + ['Nhập SĐT "abc", Lưu nháp (báo lỗi).', 'Bấm × rồi nhập 0832551333.'], '—',
       ['Chữ đỏ dưới ô SĐT biến mất ngay.'], 118)
S4.add('Mở Sửa rồi Quay lại không đổi', 'P1', PRE_EDIT, SUA + ['Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi.'], 119)
S4.add('Đổi rồi trả về ban đầu', 'P2', PRE_EDIT, SUA + ['Sửa Ghi chú rồi gõ lại "Nháp".', 'Bấm Quay lại.'], '—',
       ['Về danh sách không hỏi.'], 120)
S4.add('Quay lại khi đã đổi', 'P0', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Bấm Quay lại.'], '—',
       ['Hộp "Thông tin chưa lưu" (Thoát / Ở lại).'], 121)
S4.add('Thoát không lưu', 'P1', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Bấm Quay lại, chọn Thoát.'], '—',
       ['Về danh sách; Ghi chú vẫn "Nháp".'], [122, 124])
S4.add('Ở lại', 'P2', PRE_EDIT, SUA + ['Sửa Ghi chú.', 'Bấm Quay lại, chọn Ở lại.'], '—', ['Giữ form với Ghi chú đã sửa.'], 123)
S4.add('Biên bản đã duyệt không sửa được', 'P0', [PRE_LIST, B36], [MENU, 'Quan sát dòng 02736.', 'Mở đường link màn Sửa của 02736.'],
       '—', ['Không có nút Sửa.', 'Mở đường link màn Sửa chuyển sang trang không tìm thấy.'], [126, 129])
S4.add('Biên bản bị xóa trong lúc đang sửa', 'P1', [PRE_EDIT, 'Tab 1 đang mở màn Sửa; tab 2 vừa Xóa biên bản.'],
       ['Ở tab 1 bấm Lưu nháp.'], '—', ['Hệ thống báo không tìm thấy biên bản bàn giao nghiệm thu; không tạo lại.'], 127)
S4.add('Biên bản đổi trạng thái trong lúc đang sửa', 'P0', [PRE_EDIT, 'Tab 1 đang mở màn Sửa; tab 2 vừa Lưu và duyệt biên bản.'],
       ['Ở tab 1 bấm Lưu nháp.'], '—', ['Báo ' + CONFLICT + '; không lưu.'], 128)
S4.add('Super admin không sửa biên bản của người khác', 'P1', [PRE_LIST, DRAFT], ['Đăng nhập DNS Admin.', MENU, 'Mở chi tiết TPE.BBBG.02740 qua đường link.'],
       '—', ['Không có nút Sửa, Xóa (chỉ người tạo).', 'Danh sách lối "tất cả" không hiện biên bản Đang tạo của K.'], [126, 290])

# ============================================================== V. XÓA
S5 = Sec(5)
S5.add('Nút Xóa hiện đúng điều kiện', 'P0', [PRE_LIST, B36, B38], [MENU, 'Quan sát dòng 02738 và 02736.'], '—',
       ['02738 (Đang tạo, mình tạo): có nút Xóa (thùng rác đỏ).', '02736 (Đã duyệt): không có nút Xóa.'], 130)
S5.add('Hộp xác nhận xóa', 'P0', [PRE_LIST, B38], [MENU, 'Ở dòng 02738 bấm Xóa.'], '—',
       ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa bản ghi này không?" với nút Xóa (đỏ), Hủy.'], [131, 132])
S5.add('Xóa biên bản Đang tạo', 'P0', PRE_EDIT, [MENU, 'Ở dòng TPE.BBBG.02740 bấm Xóa.', 'Bấm Xóa trong hộp.'], '—',
       ['Báo "Xóa thành công.".', 'Dòng biến mất khỏi danh sách; tổng số giảm 1.'], [133, 139, 140])
S5.add('Hủy xóa', 'P0', PRE_EDIT, [MENU, 'Bấm Xóa ở dòng 02740.', 'Bấm Hủy.'], '—',
       ['Hộp đóng, biên bản vẫn còn.', 'Bấm ra ngoài hộp cũng không xóa; nút Xóa vẫn bấm lại được bình thường.'], 134)
S5.add('Xóa từ màn chi tiết', 'P1', PRE_EDIT, [MENU, 'Bấm TPE.BBBG.02740.', 'Bấm Xóa ở chân màn, xác nhận Xóa.'], '—',
       ['Báo "Xóa thành công.", về danh sách lối "tất cả".'], 133)
S5.add('Không xóa được biên bản đã duyệt', 'P0', [PRE_LIST, B36], [MENU, 'Mở chi tiết 02736.'], '—',
       ['Không có nút Xóa ở dòng và màn chi tiết.'], [135, 137])
S5.add('Xóa biên bản có dòng hàng và file', 'P1', [ACC_K, 'TPE.BBBG.02740 Đang tạo có 1 hàng, 1 dòng chi tiết, 1 file.'],
       [MENU, 'Xóa TPE.BBBG.02740.'], '—',
       ['Xóa được cả biên bản, dòng hàng, dòng chi tiết (không có dữ liệu con chặn xóa).', 'File vẫn giữ trong kho file.'], 136)
S5.add('Biên bản đã bị người khác xóa / đổi trạng thái', 'P1', [PRE_EDIT, 'Tab 2 vừa Lưu và duyệt TPE.BBBG.02740.'],
       ['Ở tab 1 (danh sách cũ) bấm Xóa 02740, xác nhận.'], '—',
       ['Báo ' + CONFLICT + '; danh sách nạp lại, biên bản hiện Đã duyệt.'], 138)
S5.add('Hợp đồng được giải phóng sau xóa', 'P0', PRE_EDIT, [MENU, 'Xóa TPE.BBBG.02740.', 'Bấm Tạo mới, mở popup chọn hợp đồng.'], '—',
       ['HĐ_TPE_HN_KD1_26_1118_2110 xuất hiện lại trong popup, lập được biên bản mới.'], [141, 280])
S5.add('Xóa dòng cuối của trang sau', 'P2', [ACC_K, 'K có 11 biên bản Đang tạo; đang ở trang 2 (1 dòng).'],
       ['Xóa dòng duy nhất ở trang 2.'], '—', ['Danh sách lùi về trang 1, "Hiển thị 1–10 / 10".'], 140)
S5.add('Không phải người tạo không thấy nút Xóa', 'P0', [ACC_V1, DRAFT], ['Đăng nhập V1.', MENU, 'Mở chi tiết 02740 qua đường link.'],
       '—', ['Không có nút Xóa (chỉ người tạo có quyền Tạo).'], [130, 291])

# ============================================================== VI. DUYỆT PHIẾU (LƯU VÀ DUYỆT)
S6 = Sec(6)
S6.add('Nút Lưu và duyệt hiện đúng điều kiện', 'P0', [PRE_EDIT, B36], [MENU, 'Mở màn Tạo.', 'Mở màn Sửa của 02740.', 'Mở chi tiết 02736.'],
       '—', ['Màn Tạo và màn Sửa có nút chính "Lưu và duyệt".', 'Màn chi tiết biên bản Đã duyệt không có nút này.'], 300)
S6.add('Hộp xác nhận Lưu và duyệt', 'P0', PRE_FORM, DUYET + ['Bấm Lưu và duyệt.'], FILE,
       ['Hộp "Xác nhận lưu và duyệt": "Lưu và duyệt biên bản bàn giao nghiệm thu của hợp đồng \'HĐ_TPE_HN_KD1_26_1118_2110\'? Biên '
        'bản đã duyệt không sửa / xóa được nữa." với nút Lưu và duyệt, Hủy.'], [90, 301])
S6.add('Lưu và duyệt từ màn Tạo với dữ liệu đầy đủ', 'P0', PRE_FORM, DUYET + ['Bấm Lưu và duyệt.', 'Bấm Lưu và duyệt trong hộp.'], FILE,
       ['Báo ' + OKC + ', về danh sách.', 'Biên bản mới nhãn xanh lá "Đã duyệt"; không có nút Sửa, Xóa.'], [86, 92, 302, 305])
S6.add('Lưu và duyệt thiếu dữ liệu bắt buộc', 'P0', PRE_FORM, CHON + ['Bấm Lưu và duyệt.'], '—',
       ['NV kỹ thuật ' + REQS + '; Ngày bàn giao ' + REQ + '; File đính kèm ' + FILEMSG + '; SL "Phải bằng số lượng đã xuất (3)".',
        'Thông báo ' + INC + '; không hiện hộp xác nhận.'], [87, 303])
S6.add('Lưu và duyệt thiếu SĐT người nhận (màn Tạo)', 'P0', PRE_FORM, DUYET + ['Bấm × xóa SĐT người nhận.', 'Bấm Lưu và duyệt.'], '—',
       ['Dưới ô SĐT ' + REQ + '; không hiện hộp xác nhận.'], [87, 303])
S6.add('Lưu và duyệt khi SL khác SL đã xuất', 'P0', PRE_FORM, DUYET + ['Sửa SL đã nghiệm thu = 2.', 'Bấm Lưu và duyệt.'], '—',
       ['"Phải bằng số lượng đã xuất (3)"; không hiện hộp xác nhận.'], [88, 304])
S6.add('Lưu và duyệt khi hợp đồng còn hàng chưa xuất hết', 'P0', [ACC_K, 'Hợp đồng X (đang chọn trong form) vừa phát sinh phụ lục bổ '
                                                                   'sung chưa xuất.'],
       ['Nhập đủ dữ liệu, Lưu và duyệt, xác nhận.'], '—',
       ['Dưới ô Hợp đồng "Hợp đồng chưa xuất hết hàng"; dưới hàng tương ứng "Chưa xuất hết hàng"; không lưu.'], 304)
S6.add('Ngày bàn giao ghi lên hợp đồng hãng', 'P0', [PRE_FORM, 'Tài khoản có thể xem hợp đồng ở hệ thống cũ.'],
       DUYET + ['Lưu và duyệt, xác nhận.', 'Mở hợp đồng HĐ_TPE_HN_KD1_26_1118_2110 ở hệ thống cũ.'], '—',
       ['Hợp đồng ghi Ngày bàn giao = ngày bàn giao của biên bản.'], [306, 307])
S6.add('Bấm Hủy trong hộp xác nhận', 'P0', PRE_FORM, DUYET + ['Bấm Lưu và duyệt.', 'Bấm Hủy.'], '—',
       ['Hộp đóng, form giữ nguyên, không lưu, không có biên bản mới.'], [91, 310])
S6.add('Lưu và duyệt từ màn Sửa', 'P0', PRE_EDIT, SUA + ['Chọn NV kỹ thuật, Ngày bàn giao, thêm file.', 'Bấm Lưu và duyệt, xác nhận.'],
       FILE, ['Báo ' + OKE + '; biên bản Đã duyệt.', 'Lịch sử có mốc "Thay đổi trạng thái": Trạng thái Đang tạo sang Đã duyệt.'],
       [86, 305, 312])
S6.add('Lưu và duyệt màn Sửa không bắt buộc SĐT', 'P2', [PRE_EDIT, 'Biên bản 02740 có SĐT người nhận trống.'],
       SUA + ['Nhập đủ NV kỹ thuật, Ngày bàn giao, file.', 'Bấm Lưu và duyệt, xác nhận.'], '—',
       ['Duyệt được dù SĐT trống (giữ như hệ thống cũ).'], 303)
S6.add('Không cần quyền duyệt riêng', 'P1', [ACC_K, 'K chỉ có quyền "Tạo biên bản bàn giao nghiệm thu".'], DUYET + ['Lưu và duyệt, xác nhận.'],
       '—', ['Duyệt được.', 'Lưu ý: giữ như hệ thống cũ (đã chốt 03/11/2026) — không phải lỗi.'], 302)
S6.add('Không gửi thông báo khi duyệt', 'P2', [PRE_FORM, 'Tài khoản NVKD Lê Huy Thắng.'], DUYET + ['Lưu và duyệt, xác nhận.',
       'Đăng nhập Lê Huy Thắng, mở chuông thông báo.'], '—',
       ['Không phát sinh thông báo nào (màn không gửi thông báo, giống hệ thống cũ).'], [308, 309])
S6.add('Bấm Lưu và duyệt liên tục', 'P1', PRE_FORM, DUYET + ['Bấm Lưu và duyệt trong hộp nhiều lần nhanh.'], '—',
       ['Chỉ tạo 1 biên bản.'], 101)
S6.add('Không duyệt lại biên bản đã duyệt', 'P1', [PRE_LIST, B36], [MENU, 'Mở chi tiết 02736.', 'Mở đường link màn Sửa 02736.'],
       '—', ['Không có nút Sửa / Lưu và duyệt; đường link Sửa ra trang không tìm thấy.'], 311)
S6.add('Trường được làm mới sau khi duyệt', 'P2', PRE_FORM, DUYET + ['Lưu và duyệt, xác nhận.', 'Bấm Tạo mới lại.'], '—',
       ['Form mới trống; hợp đồng vừa lập không còn trong popup.'], [89, 91])
S6.add('Người duyệt và thời điểm duyệt', 'P1', PRE_FORM, DUYET + ['Lưu và duyệt, xác nhận.', 'Mở Lịch sử của biên bản.'], '—',
       ['Mốc "Tạo mới" và "Thay đổi trạng thái" (Đang tạo sang Đã duyệt) cùng người thực hiện K, thời điểm vừa lưu.',
        'Cột Người cập nhật = K.'], 312)

# ============================================================== VII. LỊCH SỬ THAY ĐỔI
S7 = Sec(7)
S7.add('Mở cửa sổ lịch sử từ danh sách', 'P0', [PRE_LIST, B36], [MENU, 'Ở dòng 02736 bấm Lịch sử.'], '—',
       ['Mở cửa sổ "Lịch sử thay đổi: TPE.BBBG.02736", nút Bộ lọc, nút Đóng.'], 162)
S7.add('Mở lịch sử ở dòng có Sửa, Xóa', 'P1', [PRE_LIST, B38], [MENU, 'Ở dòng 02738 bấm ba chấm "Hành động khác".', 'Chọn Lịch sử.'],
       '—', ['Menu có In, Lịch sử; chọn Lịch sử mở cửa sổ "Lịch sử thay đổi: TPE.BBBG.02738".'], 162)
S7.add('Thông tin mỗi mốc', 'P0', [PRE_LIST, B36], [MENU, 'Mở lịch sử 02736.'], '—',
       ['Mốc trên: 09/11/2026 14:30 "Thay đổi trạng thái", "Người thực hiện: DNS Admin — HỘI ĐỒNG QUẢN TRỊ", "Trạng thái: Đang tạo sang '
        'Đã duyệt".', 'Mốc dưới: 09/11/2026 14:30 "Tạo mới".'], [163, 164, 165, 166, 167])
S7.add('Nội dung thay đổi cũ sang mới', 'P0', PRE_EDIT, SUA + ['Sửa Ghi chú và SL đã nghiệm thu, Lưu nháp.', 'Mở lịch sử.'], '—',
       ['Mốc "Thay đổi thông tin": Ghi chú cũ sang mới; bảng Hàng hoá ghi SL đã nghiệm thu cũ sang mới.'], 168)
S7.add('Biên bản lập ở hệ thống cũ chưa có lịch sử', 'P2', [PRE_LIST, 'TPSG.BBBG.00494 lập ở hệ thống cũ, chưa có mốc ghi.'],
       [MENU, 'Mở lịch sử TPSG.BBBG.00494.'], '—', ['Cửa sổ báo chưa có lịch sử, không lỗi.'], 173)
S7.add('Lọc theo loại hành động', 'P1', [PRE_LIST, B36],
       [MENU, 'Mở lịch sử 02736.', 'Bấm Bộ lọc, chọn Loại hành động = Tạo mới.', 'Đổi thành Thay đổi thông tin.'], '—',
       ['Bước 3: còn mốc Tạo mới.', 'Bước 4: "Không có lịch sử phù hợp bộ lọc.".',
        'Ô có: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.'], [169, 173, 175])
S7.add('Lọc theo người thực hiện', 'P2', [PRE_LIST, B36], [MENU, 'Mở lịch sử, Bộ lọc, chọn Người thực hiện = DNS Admin.'], '—',
       ['Còn đủ 2 mốc.'], 170)
S7.add('Lọc theo thời gian', 'P2', [PRE_LIST, B36], [MENU, 'Mở lịch sử, Bộ lọc, Từ ngày = Đến ngày = 08/11/2026.'], '—',
       ['"Không có lịch sử phù hợp bộ lọc."; đổi thành 09/11/2026 thì hiện 2 mốc.'], 171)
S7.add('Kết hợp lọc và Làm mới', 'P2', [PRE_LIST, B36], [MENU, 'Mở lịch sử, lọc Loại = Tạo mới và Từ ngày 09/11/2026.', 'Bấm Làm mới.'],
       '—', ['Bước 2: 1 mốc.', 'Bước 3: hiện lại đủ 2 mốc.'], [172, 174])
S7.add('Lịch sử tạo bằng Lưu nháp', 'P1', PRE_FORM, DU + ['Lưu nháp.', 'Mở lịch sử biên bản mới.'], '—', ['Có 1 mốc "Tạo mới".'], 176)
S7.add('Đóng cửa sổ', 'P1', [PRE_LIST, B36], [MENU, 'Sang trang 2, lọc Trạng thái.', 'Mở lịch sử 1 dòng, bấm Đóng.', 'Mở lại, bấm (x).'],
       '—', ['Cửa sổ đóng; danh sách giữ trang, bộ lọc.'], [184, 185])
S7.add('Xem / in không ghi lịch sử', 'P2', [PRE_LIST, B36], [MENU, 'Mở chi tiết 02736, bấm In, đóng.', 'Mở lịch sử.'], '—',
       ['Không có mốc mới.'], 182)

# ============================================================== VIII. XEM CHI TIẾT
S8 = Sec(8)
S8.add('Mở màn chi tiết', 'P0', [PRE_LIST, B36], [MENU, 'Bấm TPE.BBBG.02736.'], '—',
       ['Mở TRANG chi tiết, tiêu đề "Chi tiết biên bản bàn giao nghiệm thu: TPE.BBBG.02736" kèm nhãn xanh "Đã duyệt".'], [186, 187])
S8.add('Đầy đủ trường', 'P0', [PRE_LIST, B36], [MENU, 'Bấm TPE.BBBG.02736.'], '—',
       ['Hợp đồng/đơn hàng (liên kết), Khách hàng, CMT/MST 0111639659, Địa chỉ, NVKD Trần Thị Phương Nhung, Phòng ban "PHÒNG KD VẬT '
        'TƯ THIẾT BỊ BÔI TRƠN", SĐT người nhận 123, Người nhận Ms NHUNG, NV kỹ thuật Nguyễn Thị Cần, Ngày bàn giao 09/11/2026 00:00.',
        'File đính kèm 1 file docx.', 'Bảng Hàng hoá 2 hàng ENEO-640-V5235 (SL 1), ENEO-700-V5252 (SL 3) kèm dòng chi tiết.'], [188, 189])
S8.add('Khớp dữ liệu danh sách', 'P1', [PRE_LIST, B36], [MENU, 'So dòng 02736 và màn chi tiết.'], '—',
       ['Ngày BGNT, số hợp đồng, khách hàng, NVKD, NV kỹ thuật, người tạo, ngày tạo trùng khớp.'], 190)
S8.add('Chế độ chỉ đọc', 'P0', [PRE_LIST, B36], [MENU, 'Bấm TPE.BBBG.02736.'], '—',
       ['Mọi ô khóa, không còn dấu *; không có Lưu nháp / Lưu và duyệt.', 'Chân màn: In, Quay lại.'], [191, 192])
S8.add('Biên bản Đang tạo của mình', 'P1', [PRE_LIST, B38], [MENU, 'Bấm TPE.BBBG.02738.'], '—',
       ['Tiêu đề kèm nhãn xám "Đang tạo".', 'Chân màn: Sửa, In, Xóa, Quay lại.', 'Khối File đính kèm ẩn (chưa có file).'], [193, 194])
S8.add('Khu vực lịch sử', 'P1', [PRE_LIST, B36], [MENU, 'Bấm 02736.', 'Bấm Xem lịch sử.'], '—',
       ['Khối Lịch sử mở rộng, có 2 mốc như cửa sổ lịch sử.'], 195)
S8.add('Quay lại giữ trang và bộ lọc', 'P1', [PRE_LIST, 'Đang lọc Trạng thái = Đã duyệt, ở trang 2.'], ['Bấm một số BBBG.', 'Bấm Quay lại.'],
       '—', ['Về danh sách, vẫn lọc Đã duyệt, đúng trang 2.'], [196, 197])
S8.add('Liên kết hợp đồng', 'P2', [PRE_LIST, B36], ['Bấm 02736.', 'Bấm số hợp đồng.'], '—', ['Mở hợp đồng ở tab mới.'], 188)
S8.add('Biên bản không tồn tại', 'P1', PRE_LIST, ['Mở đường link chi tiết với mã không tồn tại.'], '—',
       ['Chuyển sang trang không tìm thấy, không báo lỗi nổi.'], 196)

# ============================================================== IX. IN PHIẾU
S9 = Sec(9)
S9.add('In biên bản từ danh sách', 'P0', [PRE_LIST, B36], [MENU, 'Ở dòng 02736 bấm In.'], '—',
       ['Cửa sổ "Xem trước biên bản bàn giao nghiệm thu".',
        'Bản in: letterhead "CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT", "BIÊN BẢN BÀN GIAO NGHIỆM THU", "Số: TPE.BBBG.02736", '
        '"Hôm nay, ngày 09 tháng 11 năm 2026, căn cứ hợp đồng/đơn hàng số DHNT_TPE_HN_DAU_26_0239_ML 05.1610.2026.PN…".',
        'Khối BÊN NHẬN (BÊN A), BÊN GIAO (BÊN B), bảng DANH SÁCH HÀNG HOÁ BÀN GIAO 11 cột; chỗ ký "ĐẠI DIỆN BÊN NHẬN" Ms NHUNG, '
        '"ĐẠI DIỆN BÊN GIAO" Nguyễn Thị Cần.'], 6)
S9.add('In biên bản từ dòng có Sửa, Xóa', 'P1', [PRE_LIST, B38], [MENU, 'Ở dòng 02738 bấm ba chấm, chọn In.'], '—',
       ['Mở cửa sổ xem trước 02738; câu mở đầu để "....." vì chưa có Ngày bàn giao.'], 6)
S9.add('In biên bản từ màn chi tiết', 'P1', [PRE_LIST, B36], [MENU, 'Bấm 02736.', 'Bấm In.'], '—', ['Cùng bản xem trước.'], 6)
S9.add('Letterhead theo công ty của biên bản', 'P1', [ACC_V1, 'TPSG.BBBG.00495 thuộc công ty TPSG; V1 thuộc công ty TPE.'],
       ['Đăng nhập V1.', MENU, 'In TPSG.BBBG.00495.'], '—', ['Đầu bản in là letterhead công ty TPSG.'], 6)
S9.add('Bấm In trong cửa sổ', 'P1', [PRE_LIST, B36], ['Mở xem trước 02736.', 'Bấm In.'], '—', ['Mở hộp thoại in của trình duyệt.'], 6)
S9.add('In danh sách theo bộ lọc', 'P0', PRE_LIST, [MENU, 'Nhập "TPE.BBBG.0273", Tìm kiếm.', 'Bấm In danh sách.'], '—',
       ['Cửa sổ "Xem trước danh sách biên bản bàn giao nghiệm thu", tiêu đề "DANH SÁCH BIÊN BẢN BÀN GIAO NGHIỆM THU".',
        'Đúng 8 dòng; cột STT, Số BBBG, Ngày BGNT, Số hợp đồng, Khách hàng, NVKD, NV kỹ thuật, Ngày tạo, Người tạo, Ngày cập nhật, '
        'Người cập nhật, Trạng thái; chỗ ký Người lập.'], [219, 220])
S9.add('In danh sách vượt 2.000 dòng', 'P1', PRE_LIST, [MENU, 'Không lọc gì, bấm In danh sách.'], '—',
       ['Không có bản in, ẩn nút In; hiện "Danh sách có 8,271 dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu '
        'hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài."'], 221)
S9.add('In danh sách khi không có dữ liệu', 'P2', PRE_LIST, [MENU, 'Tìm "ZZZ", bấm In danh sách.'], '—',
       ['Bản in chỉ có tiêu đề và dòng tên cột, không có dòng dữ liệu.'], 222)
S9.add('Đóng cửa sổ xem trước', 'P2', [PRE_LIST, B36], ['Mở xem trước 02736.', 'Bấm (x).'], '—',
       ['Cửa sổ đóng, danh sách giữ nguyên.'], 185)

# ============================================================== X. TÙY CHỈNH CỘT
S10 = Sec(10)
S10.add('Mở cửa sổ Tùy chỉnh cột', 'P0', PRE_LIST, [MENU, 'Bấm nút biểu tượng cột.'], '—',
        ['Cửa sổ "Tuỳ chỉnh cột", dòng hướng dẫn, 13 cột, "Đang chọn 13/13 cột", nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng.'],
        [198, 199])
S10.add('Cột chọn mặc định', 'P1', [PRE_LIST, 'Tài khoản chưa lưu cấu hình.'], ['Mở Tuỳ chỉnh cột.'], '—', ['Cả 13 cột được tích.'], 200)
S10.add('Ẩn cột', 'P0', PRE_LIST, ['Mở Tuỳ chỉnh cột, bỏ tích Người cập nhật, bấm Lưu.'], '—',
        ['Báo "Cập nhật thành công"; bảng không còn cột Người cập nhật.'], [202, 206])
S10.add('Hiện lại cột ẩn', 'P1', 'Đang ẩn cột Người cập nhật.', ['Mở Tuỳ chỉnh cột, tích Người cập nhật, Lưu.'], '—',
        ['Cột hiện lại đúng vị trí.'], 201)
S10.add('Cột khóa không ẩn được', 'P0', PRE_LIST, ['Mở Tuỳ chỉnh cột.'], '—',
        ['STT, Số BBBG, Hành động có biểu tượng ổ khóa, không bỏ tích / kéo được.'], [203, 205])
S10.add('Kéo đổi thứ tự cột', 'P1', PRE_LIST, ['Kéo cột Trạng thái lên sau Số BBBG, Lưu.'], '—', ['Bảng hiện Trạng thái ngay sau Số BBBG.'], 204)
S10.add('Đóng không lưu', 'P1', PRE_LIST, ['Bỏ tích Khách hàng, bấm Đóng.'], '—', ['Bảng vẫn có cột Khách hàng.'], 207)
S10.add('Ghi nhớ sau F5', 'P1', 'Đã ẩn cột Người cập nhật và Lưu.', ['Nhấn F5.'], '—', ['Cột Người cập nhật vẫn ẩn.'], 208)
S10.add('Cấu hình theo tài khoản và lối vào', 'P2', 'Tài khoản A đã ẩn cột NVKD ở lối "tất cả".',
        ['Đăng nhập B, mở màn.', 'A mở lối "theo NV".'], '—', ['B vẫn thấy cột NVKD.', 'Lối "theo NV" của A vẫn có cột NVKD.'], 209)
S10.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', 'Đang lọc Trạng thái = Đang tạo.', ['Ẩn cột Người tạo, Lưu.'], '—',
        ['Vẫn 2 biên bản, bộ lọc giữ nguyên.'], [210, 211])

# ============================================================== XI. XUẤT DANH SÁCH EXCEL
S11 = Sec(11)
S11.add('Mở cửa sổ chọn trường', 'P0', PRE_LIST, [MENU, 'Bấm Xuất Excel.'], '—',
        ['Cửa sổ "Chọn trường xuất file": 11 trường Số BBBG, Ngày BGNT, Số hợp đồng, Khách hàng, NVKD, NV kỹ thuật, Ngày tạo, Người '
         'tạo, Ngày cập nhật, Người cập nhật, Trạng thái; "Đang chọn 11/11 trường".'], [212, 213])
S11.add('Trường chọn mặc định theo cột đang hiện', 'P1', 'Đang ẩn cột Người cập nhật.', ['Bấm Xuất Excel.'], '—',
        ['Người cập nhật không được tích sẵn.'], [214, 215])
S11.add('Xuất tất cả trường', 'P0', [PRE_LIST, 'Đang tìm "TPE.BBBG.0273" (8 biên bản).'], ['Bấm Xuất Excel, Chọn tất cả, Xuất file.'], '—',
        ['Tải "danh_sach_bien_ban_ban_giao_nghiem_thu.xlsx", báo "Xuất Excel thành công.".', 'Đủ 8 dòng, cột STT + 11 cột.'],
        [216, 223, 227])
S11.add('Xuất một số trường', 'P1', PRE_LIST, ['Bỏ chọn hết, tích Số BBBG, Trạng thái, Xuất file.'], '—',
        ['File chỉ có STT, Số BBBG, Trạng thái.'], 217)
S11.add('Không chọn trường', 'P1', PRE_LIST, ['Bấm Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa.'], 218)
S11.add('Xuất theo tìm kiếm', 'P1', PRE_LIST, ['Tìm "TPE.BBBG.0273".', 'Xuất file.'], '—', ['File có 8 dòng 02730–02738 (trừ 02732).'], 219)
S11.add('Xuất theo bộ lọc', 'P0', PRE_LIST, [ADV, 'Chọn Trạng thái = Đang tạo.', 'Xuất file.'], '—', ['File có đúng 2 dòng.'], 220)
S11.add('Xuất nhiều trang', 'P1', [PRE_LIST, 'Đang lọc Ngày tạo tháng 10/2026 (trên 10 dòng).'], ['Đang ở trang 1, Xuất file.'], '—',
        ['File đủ mọi dòng khớp bộ lọc, không chỉ trang đang xem; hiện tiến độ "Đã tải x/y dòng…".'], 221)
S11.add('Danh sách rỗng', 'P1', PRE_LIST, ['Tìm "ZZZ".', 'Xuất file.'], '—', ['Báo "Không có dữ liệu để xuất", không tạo file.'], 222)
S11.add('Cấu trúc file', 'P0', PRE_LIST, ['Xuất tất cả trường.', 'Mở file.'], '—',
        ['Đầu file letterhead công ty người xuất, "DANH SÁCH BIÊN BẢN BÀN GIAO NGHIỆM THU"; trang tính "Biên bản BGNT".',
         'Định dạng .xlsx; dòng tên cột đúng tên trường.'], [224, 225])
S11.add('Thứ tự cột theo kéo thả', 'P1', PRE_LIST, ['Kéo Trạng thái lên đầu, Xuất file.'], '—', ['Cột sau STT là Trạng thái.'], 226)
S11.add('Dữ liệu khớp và định dạng', 'P0', [PRE_LIST, B36], ['Xuất tất cả, tìm dòng 02736.'], '—',
        ['Ngày BGNT "09/11/2026 00:00", Số hợp đồng, Khách hàng "CÔNG TY TNHH MORI LUBRICANTS VIỆT NAM", Trạng thái "Đã duyệt".',
         'Tiếng Việt có dấu hiển thị đúng.'], [228, 229, 230])
S11.add('Xuất ở lối theo NV', 'P2', [PRE_LIST, 'DNS Admin là NVKD của 1 biên bản.'], [MENU_NV, 'Xuất Excel, Xuất file.'], '—',
        ['File chỉ có 1 dòng TPE.BBBG.02737.'], 220)

# ============================================================== XII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S12 = Sec(12)
S12.add('Popup chỉ có hợp đồng đã xuất hết hàng', 'P0', [ACC_K, 'Hợp đồng Z có hiệu lực, còn 1 hàng đã xuất 1/2.'],
        TAO + ['Mở popup, tìm số hợp đồng Z.'], '—',
        ['Không có hợp đồng Z.', 'Sau khi lập Phiếu xuất hàng xuất nốt hàng còn lại, hợp đồng Z xuất hiện trong popup.'], [268, 274])
S12.add('Hợp đồng có hàng: SL theo hợp đồng / đã xuất lấy từ hợp đồng', 'P0', PRE_FORM, CHON, '—',
        ['SL theo hợp đồng 3, đã xuất 3, đã trả 0 đúng với hợp đồng.', 'Hợp đồng có phụ lục giảm thì SL theo hợp đồng đã trừ.'], 269)
S12.add('Hợp đồng chưa có hiệu lực / khác công ty không chọn được', 'P1',
        [ACC_K, 'Hợp đồng W Chờ duyệt; hợp đồng V thuộc công ty TPSG.'], TAO + ['Mở popup, tìm W và V.'], '—',
        ['Không có W, không có V.'], [268, 276])
S12.add('Hàng hóa đã có trên biên bản không xóa được', 'P1', [PRE_LIST, B36],
        ['Vào phân hệ Danh mục dùng chung > "Hàng hoá, vật tư" > "Kho dữ liệu hàng hoá".', 'Xóa hàng ENEO-640-V5235.'], '—',
        ['Hệ thống chặn xóa vì hàng đã được sử dụng.'], 270)
S12.add('Ngày nghiệm thu ở báo cáo công nợ theo NV', 'P1',
        [PRE_FORM, 'Hợp đồng HĐ_TPE_HN_KD1_26_1118_2110 là hợp đồng cần lắp đặt, còn dư nợ.'],
        DUYET + ['Lưu và duyệt, xác nhận.', 'Vào Bán hàng > Báo cáo > Báo cáo công nợ > "Tổng hợp công nợ theo NV".'], '—',
        ['Dòng hợp đồng có Ngày nghiệm thu = Ngày bàn giao của biên bản; Số ngày nợ tính từ ngày đó + 6 ngày.'], [274, 281])
S12.add('Số BBBGNT ở danh sách thiết bị khách hàng', 'P1', [PRE_LIST, B36],
        ['Vào phân hệ CSKH sau bán > "Kiểm tra bảo hành sửa chữa" > "Yêu cầu kiểm tra sửa chữa - bảo hành", Tạo mới.',
         'Chọn khách hàng MORI LUBRICANTS, mở popup chọn thiết bị.'], '—',
        ['Thiết bị ENEO-640-V5235 có cột Số BBBGNT hoặc BBXNCV = TPE.BBBG.02736 (theo hợp đồng của phiếu xuất).'], [274, 282])
S12.add('Số hợp đồng lưu cố định lúc lập', 'P2', [PRE_LIST, B36], ['Đổi số hợp đồng ở màn hợp đồng.', 'Mở 02736.'], '—',
        ['Biên bản vẫn hiện số hợp đồng lúc lập; liên kết vẫn mở đúng hợp đồng.'], [272, 278, 279])
S12.add('Cấp con đúng cấp cha', 'P1', [PRE_LIST, B36], [MENU, 'Mở 02736.'], '—',
        ['Dòng hàng thuộc đúng biên bản; dòng chi tiết thuộc đúng hàng; hàng thuộc hợp đồng của biên bản.'], [283, 285])
S12.add('Tham chiếu giữ khi đổi trạng thái', 'P1', [PRE_LIST, B36], [MENU, 'Mở 02736 (Đã duyệt).'], '—',
        ['Liên kết hợp đồng, dòng hàng, dòng chi tiết, file vẫn đủ.'], 284)
S12.add('Không có biên bản trùng hợp đồng', 'P0', PRE_FORM, ['Lập biên bản cho HĐ_TPE_HN_KD1_26_1118_2110.', 'Lập lần 2 cho cùng hợp đồng.'],
        '—', ['Lần 2: hợp đồng không còn trong popup; lưu qua đường khác cũng bị chặn ' + DUP + '.'], 286)
S12.add('Biên bản gắn hợp đồng HRM', 'P2', [ACC_K, 'Hợp đồng HRM HĐHRM-001 có hiệu lực, không có dòng hàng.'],
        TAO + ['Lọc Loại hợp đồng = Hợp đồng HRM, chọn HĐHRM-001.', 'Lưu nháp.'], '—',
        ['Lưu được; Số hợp đồng ở danh sách mở màn Hợp đồng HRM ở tab mới.',
         'Lưu ý: hợp đồng HRM có hàng hiện chưa có trong popup vì số đã xuất của hợp đồng HRM chưa được ghi.'], [269, 274])
S12.add('Biên bản lập ở hệ thống cũ hiện trên màn', 'P2', PRE_LIST, [MENU, 'Tìm TPSG.BBBG.00494.'], '—',
        ['Hiện đủ thông tin (dữ liệu dùng chung với hệ thống cũ).'], 274)

# ============================================================== XIII. PHÂN QUYỀN (cuối)
S13 = Sec(13)
S13.add('Quyền Xem mức Tổng công ty', 'P0', ACC_V1, ['Đăng nhập V1.', MENU, ADV], '—',
        ['Thấy biên bản của mọi công ty (trừ biên bản Đang tạo của người khác).', 'Có ô lọc Công ty và Phòng ban.'], [287, 299])
S13.add('Quyền Xem mức Công ty', 'P0', [ACC_V2, 'TPSG.BBBG.00495 thuộc TPSG; TPE.BBBG.02736 thuộc TPE.'], ['Đăng nhập V2.', MENU, ADV], '—',
        ['Thấy TPSG.BBBG.00495, KHÔNG thấy TPE.BBBG.02736.', 'Có khối Công ty – Phòng ban (ô Công ty khóa).'], [287, 299])
S13.add('Quyền Xem mức Phòng ban', 'P0', [ACC_V3, 'TPSG.BBBG.00495 do người phòng KV3 lập.'], ['Đăng nhập V3.', MENU, ADV], '—',
        ['Chỉ thấy biên bản do người thuộc phòng KV3 lập (có 00495).', 'Không có khối Công ty – Phòng ban.'], [287, 299])
S13.add('Không có quyền nào', 'P0', ACC_N, ['Đăng nhập N.', MENU], '—',
        ['Menu vẫn hiện, mở được màn.', 'Lối "tất cả" chỉ thấy TPE.BBBG.02741 do N tạo; không có nút Tạo mới.'], [287, 295, 299])
S13.add('Không quyền vẫn xem biên bản mình là NVKD', 'P0', ACC_N, ['Đăng nhập N.', MENU_NV, 'Bấm 1 số BBBG.'], '—',
        ['Lối "theo NV" thấy 2 biên bản N là NVKD; mở chi tiết, in, lịch sử được.'], [287, 288])
S13.add('Quyền Tạo', 'P0', PRE_FORM, ['Đăng nhập K.'] + DU + ['Bấm Lưu nháp.'], '—',
        ['K thấy nút Tạo mới, lập được biên bản và thấy biên bản đó trong danh sách.'], 289)
S13.add('Super admin chưa tích quyền Tạo', 'P1', 'Tài khoản Super admin chưa được tích quyền "Tạo biên bản bàn giao nghiệm thu".',
        ['Đăng nhập.', MENU], '—', ['Không có nút Tạo mới, không có nút Sửa / Xóa (kể cả biên bản mình tạo trước đó).'], [289, 290, 295])
S13.add('Xem chi tiết trong phạm vi', 'P0', [ACC_V2], ['Đăng nhập V2.', MENU, 'Mở TPSG.BBBG.00495.'], '—', ['Xem được đầy đủ.'], 288)
S13.add('Đường link chi tiết ngoài phạm vi', 'P0', [ACC_N, 'N có đường link chi tiết TPE.BBBG.02736.'], ['Đăng nhập N, mở đường link.'], '—',
        ['Chuyển sang trang không tìm thấy; không lộ dữ liệu.'], [288, 296])
S13.add('Sửa / Xóa chỉ dành cho người tạo', 'P0', [ACC_V1, DRAFT], ['Đăng nhập V1.', 'Mở đường link màn Sửa của 02740.'], '—',
        ['Chuyển sang trang không tìm thấy.', 'Chi tiết 02740 (nếu xem được) không có nút Sửa, Xóa.'], [290, 291, 296])
S13.add('Ẩn nút khi thiếu quyền', 'P0', ACC_N, ['Đăng nhập N.', MENU], '—',
        ['Không có nút Tạo mới; dòng TPE.BBBG.02741 (Đã duyệt) chỉ có In, Lịch sử.'], 295)
S13.add('Xuất Excel / In danh sách theo quyền', 'P1', ACC_V2, ['Đăng nhập V2.', 'Xuất Excel, Xuất file.'], '—',
        ['File chỉ có biên bản của công ty TPSG.'], 293)
S13.add('Xem lịch sử theo quyền', 'P1', [ACC_V1, B36], ['Đăng nhập V1.', 'Mở lịch sử 02736.'], '—', ['Xem được các mốc.'], 294)
S13.add('Bị gỡ quyền giữa lúc thao tác', 'P1', [ACC_V1, 'Quản trị gỡ quyền Xem mức Tổng công ty của V1 khi V1 đang ở danh sách.'],
        ['Bấm sang trang 2.'], '—', ['Danh sách chỉ còn biên bản V1 tự tạo (phạm vi kiểm lại ở mỗi lần nạp).'], [297, 298])
S13.add('Bị gỡ quyền Tạo khi đang ở form', 'P0', [PRE_FORM, 'Quản trị gỡ quyền Tạo của K khi K đang ở form.'], DU + ['Bấm Lưu nháp.'], '—',
        ['Hệ thống từ chối, báo không có quyền; không tạo biên bản.'], [297, 298])
S13.add('Đổi công ty đang làm việc', 'P2', [ACC_V2, 'V2 có vai trò ở cả TPSG và TPE.'], ['Đổi công ty đang làm việc sang TPE.', MENU],
        '—', ['Phạm vi tính lại theo công ty mới; không thấy biên bản công ty khác ngoài phạm vi.'], 299)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'CHỈNH SỬA', S4),
    ('V', 'XÓA', S5),
    ('VI', 'DUYỆT PHIẾU (LƯU VÀ DUYỆT)', S6),
    ('VII', 'LỊCH SỬ THAY ĐỔI', S7),
    ('VIII', 'XEM CHI TIẾT BIÊN BẢN BÀN GIAO NGHIỆM THU', S8),
    ('IX', 'IN PHIẾU (IN BIÊN BẢN, IN DANH SÁCH)', S9),
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
                feature_name='Biên bản bàn giao nghiệm thu - Cập nhật ngày 10/11/2026',
                module_name='Biên bản bàn giao nghiệm thu', description_block=DESCRIPTION_BLOCK, sections=SECTIONS,
                loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

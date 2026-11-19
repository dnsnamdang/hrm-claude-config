# -*- coding: utf-8 -*-
"""Testcase màn "Báo cáo tồn kho theo vị trí" (phân hệ Kho › Báo cáo kho) — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026
(tc_chuan.build_chuan, loai='bao_cao').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Khuôn chép: ../bao-cao-ton-kho-chi-tiet-mat-hang/gen_testcase.py (màn anh em 06/11).
Loại 'bao_cao' (đọc code 07/11/2026): màn chỉ đọc, chỉ có API GET (xem / danh mục / danh mục vị trí / in / xuất). Nhóm có mặt: I Hiển thị ·
II Tìm kiếm & lọc (gồm Nhà / Dãy / Khoang / Vị trí, Cài đặt bộ lọc, Chọn hàng hóa) · III Số liệu báo cáo (đối soát) · IV Xem chi tiết
(bung hàng hóa – công ty – lô, ĐVT, hợp đồng) · V Xuất danh sách Excel · VI In báo cáo · VII Ràng buộc · VIII Phân quyền. Không có Tùy
chỉnh cột (bảng cố định) → bỏ nhóm. Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Nguồn hành vi: FE pages/warehouse/stock-location-product/**; BE Modules/Finance StockLocationProduct* + WarehouseStockReportService.
Số liệu mẫu dev-hrm 07/11/2026 (DNS Admin, _capture/doisoat.js, chỉ đọc): kho HP - Hải Phòng (công ty CN Hải Phòng): 8 vị trí còn hàng,
96 mặt hàng, TPE 1 vị trí, TPHP 8 vị trí, tổng SL tồn 8,530; KHOANG1 (Nhà TANG1) 9 mặt hàng, SL tồn 1,634; hàng ENEO-700-V5231 chỉ ở
KHOANG1: TPHP 20, 4 lô 6 / 2 / 6 / 6; Thẻ kho 01/01–07/11/2026: tồn đầu 70, nhập 496, xuất 546, tồn cuối 20.
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
from tc_chuan import build_chuan  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = 'Vào phân hệ Kho > menu "Báo cáo kho" > bấm "Báo cáo tồn kho theo vị trí".'
CN = 'CN HẢI PHÒNG - CÔNG TY CP CÔNG NGHỆ THIẾT BỊ TÂN PHÁT'
CHON_HP = 'Chọn Tồn theo công ty = "%s", Kho = "HP - Hải Phòng".' % CN
V1 = 'Xem báo cáo tồn kho theo tổng công ty'
V2 = 'Xem báo cáo tồn kho theo công ty'
V3 = 'Xem báo cáo tồn kho theo kho'
NOPERM = 'Bạn không có quyền truy cập chức năng này.'
EMPTY = 'Không có vị trí nào khớp bộ lọc.'
CHONKHO = 'Chọn kho để xem báo cáo.'
FILE = 'bao_cao_ton_kho_theo_vi_tri.xlsx'
HANG = 'hàng "Dầu nhớt động cơ Diesel 4 kỳ SAE 20W-50 CF-4 (18L)" (mã ENEO-700-V5231)'
HANG2 = 'hàng "Dầu nhớt động cơ Diesel 4 kỳ SAE 20W-50 CF-4 (200L)" (mã ENEO-800-V5231), ĐVT Lít và Phuy 200L (x200)'
PRE = ('Tài khoản DNS Admin (Super admin, coi như có quyền "%s").\n'
       'Kho HP - Hải Phòng (công ty %s) tính đến 07/11/2026 có 8 vị trí còn hàng, 96 mặt hàng; công ty thuê kho TPE có hàng ở 1 vị trí, '
       'TPHP ở 8 vị trí; tổng SL tồn 8,530.' % (V1, CN))
PRE_H = PRE + ('\n%s chỉ nằm ở vị trí KHOANG1 (Nhà TANG1): công ty TPHP 20 Xô 18L, 4 lô 6 / 2 / 6 / 6; lô thứ 2 thuộc hợp đồng '
               'HĐ_TPHP_HP_KD_26_0183_CD.' % HANG)
OPEN = [MENU, CHON_HP]
ACC_C = 'Tài khoản C: thuộc công ty CN Hải Phòng, chỉ có quyền "%s".' % V2
ACC_K = 'Tài khoản K: thuộc công ty CN Hải Phòng, chỉ có quyền "%s", là thủ kho của kho HP - Hải Phòng (không là thủ kho kho khác).' % V3
ACC_T = 'Tài khoản T: có quyền "%s", thuộc công ty TPE.' % V1
ACC_N = 'Tài khoản N: không có quyền nào trong 3 quyền xem báo cáo tồn kho.'

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
        tid = 'TC_%02d.%s' % (self.idx, self[-1][0])
        for s in (ck if isinstance(ck, (list, tuple)) else [ck]):
            CK[s].append(tid)


DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Xem tại MỘT kho, tính đến hết một ngày, từng vị trí (ô chứa hàng) đang chứa mặt hàng nào, của công ty thuê kho nào, lô nào (kèm '
     'hợp đồng của phiếu nhập) và số lượng. Màn chỉ đọc: không thêm / sửa / xóa; có In (2 kiểu, chọn cột) và Xuất Excel (2 kiểu).'),
    ('2. Đối tượng được tính / hiển thị',
     '- Cặp vị trí – mặt hàng có tổng thay đổi tồn theo vị trí (các công ty thuê kho đang lọc) tới hết ngày Tính đến ngày lớn hơn 0.\n'
     '- Vị trí: có ít nhất 1 cặp như trên.\n- Dòng công ty thuê kho: tổng của chính mặt hàng đó cho công ty lớn hơn 0.\n'
     '- Dòng lô: lô có số lượng tại vị trí (ghi nhận cuối cùng tới hết ngày) lớn hơn 0.\n'
     '- Nguồn số: mọi chứng từ kho ghi tồn theo vị trí (tồn đầu kỳ, nhập kho, nhập lại, xuất kho, xuất điều chỉnh, điều chuyển kho, '
     'điều chuyển vị trí, nhập / xuất điều chỉnh kiểm kê).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Vị trí đã hết hàng; mặt hàng tồn 0 tại vị trí; công ty thuê kho không có hàng của mặt hàng đó; lô đã hết tại vị trí.\n'
     '- Thay đổi tồn sau ngày Tính đến ngày.\n'
     '- Vị trí ngoài các Nhà / Dãy / Khoang / Vị trí đã tick; kho ngoài phạm vi quyền, kho ngừng hoạt động.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô Tính đến ngày (bắt buộc, mặc định hôm nay): cộng thay đổi tồn tới hết 23:59 ngày đó; áp cho cả SL vị trí, Cộng và SL lô.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Dòng TỔNG > Vị trí (I, II…) > Hàng hóa (1, 2…) > Công ty thuê kho (1.1…) > Lô (1.1.1…). Ô chọn cấp bung: Chỉ vị trí / Đến hàng '
     'hóa / Đến công ty thuê kho (mặc định) / Tất cả cấp (đến lô). Phân trang theo vị trí (mặc định 20).'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- SL tồn vị trí = tổng SL mọi mặt hàng tại vị trí theo ĐVT cơ sở (cộng thẳng, không quy đổi).\n'
     '- SL tồn hàng hóa = tổng Cộng các công ty.\n- Cộng = tổng SL các lô của công ty.\n'
     '- 1 mặt hàng có thể nằm ở nhiều vị trí; ô Mặt hàng còn tồn đếm mỗi hàng 1 lần; ô theo công ty thuê kho đếm số vị trí.'),
    ('7. Phân quyền cấp',
     '- %s: chọn mọi công ty, mọi kho (Super admin coi như có quyền này).\n- %s: công ty mình, kho của công ty mình.\n'
     '- %s: công ty mình, chỉ kho mình là thủ kho.\n- Không có quyền nào: không xem được, báo "%s".' % (V1, V2, V3, NOPERM)),
    ('8. Cách tính các ô thống kê',
     '- Ô Vị trí còn hàng = dòng TỔNG = N ở "Hiển thị a–b / N vị trí".\n- Ô Mặt hàng còn tồn = số mặt hàng khác nhau ở các vị trí.\n'
     '- Ô Công ty thuê kho có tồn = số công ty có hàng ở ít nhất 1 vị trí.\n- Ô từng công ty thuê kho = số vị trí công ty đó có hàng.\n'
     '- Đối soát: tổng 1 mặt hàng qua các vị trí = SL tồn ở Báo cáo tồn kho chi tiết theo mặt hàng = Tồn đầu kỳ + Nhập - Xuất (Thẻ kho).'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản: DNS Admin (Super admin), T (tổng công ty), C (theo công ty), K (theo kho), N (không quyền).\n'
     '- Lưu ý: số dòng hàng hóa / công ty / lô quy đổi theo ĐVT chọn ở từng hàng và hiện SỐ NGUYÊN; dòng vị trí, dòng TỔNG, In / Excel '
     'luôn theo ĐVT cơ sở.\n'
     '- Lưu ý: SL tồn dòng vị trí cộng thẳng nhiều loại ĐVT (Lít + Cái…) — đúng thiết kế (giữ như hệ thống cũ).\n'
     '- Lưu ý: màn không có ô tìm nhanh và không sắp xếp theo cột; ô Hợp đồng chỉ áp khi Enter / Tìm kiếm; ô Nhà / Dãy / Khoang / Vị '
     'trí chỉ hiện khi đã chọn kho.\n'
     '- Lưu ý: kho lớn (Liên Ninh ~767 vị trí) xuất Excel có thể mất 40–55 giây; in quá 2.000 dòng bị chặn.'),
]

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', 'Tài khoản DNS Admin, công ty TPE, chưa mở màn trong 10 phút qua.', [MENU], '—',
       ['Mở màn "Báo cáo tồn kho theo vị trí".', 'Tính đến ngày = hôm nay, Tồn theo công ty = công ty của tài khoản, Kho trống.',
        'Bảng hiện "%s", không báo lỗi; chưa có ô Nhà / Dãy / Khoang / Vị trí.' % CHONKHO], [1, 36])
S1.add('Tiêu đề màn hình', 'P1', PRE, [MENU, 'Quan sát thanh tiêu đề và tab trình duyệt.'], '—',
       ['Cả 2 nơi là "Báo cáo tồn kho theo vị trí"; khối lọc có tiêu đề "Bộ lọc báo cáo tồn kho".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE, OPEN + ['Quan sát khối lọc và bảng.'], '—',
       ['Đầu khối lọc: In danh sách, Xuất Excel, Cài đặt bộ lọc, Ẩn tìm kiếm nâng cao.', 'Dưới các ô lọc: Tìm kiếm, Xóa lọc.',
        'Dòng tóm tắt có nút Thu gọn; tiêu đề cột thứ 2 có ô chọn cấp bung.', 'KHÔNG có nút Tạo mới, Sửa, Xóa, Import, Lịch sử.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', PRE, OPEN + ['Đọc tiêu đề cột.'], '—',
       ['Đúng 10 cột: STT, Vị trí / Hàng hóa / Công ty / Lô, Nhà kho, Mã hàng, Model, Thương hiệu, ĐVT, SL tồn, SL, Cộng.',
        'Cột ĐVT, SL tồn, SL, Cộng có biểu tượng chữ i.'], 4)
S1.add('Không có cột ẩn và không có tùy chỉnh cột', 'P2', PRE, OPEN + ['Tìm nút cấu hình cột trên bảng.'], '—',
       ['Không có nút cấu hình cột; bảng luôn đủ 10 cột.'], 5)
S1.add('Dữ liệu dòng vị trí và dòng hàng hóa', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231 ở ô Hàng hóa.'], 'Hàng hóa: ENEO-700-V5231',
       ['Dòng I: vị trí KHOANG1, chữ xám "1 mặt hàng", cột Nhà kho TANG1, SL tồn 20.',
        'Dòng 1: tên "Dầu nhớt động cơ Diesel 4 kỳ SAE 20W-50 CF-4 (18L)", Mã hàng ENEO-700-V5231, Model "CF4 20W50 18L", Thương hiệu ENEOS, '
        'ĐVT "Xô 18L", SL tồn 20.', 'Dòng 1.1: TPHP, cột Cộng 20.'], 6)
S1.add('Vị trí hết hàng không hiện', 'P0', [PRE, 'Vị trí X của kho HP đã xuất hết (tổng nhập vào vị trí = tổng xuất ra).'],
       OPEN + ['Tìm vị trí X trong bảng.'], '—',
       ['Vị trí X không có trong bảng; dòng báo cáo không có trạng thái Khóa / Hoạt động.'], 7)
S1.add('Kho chưa có hàng ở vị trí nào', 'P1', 'Tài khoản DNS Admin; kho "DATD - Kho Dự án trọng điểm" (công ty TPE) không còn hàng.',
       [MENU, 'Chọn Tồn theo công ty = công ty TPE, Kho = "DATD - Kho Dự án trọng điểm".'], 'Kho: DATD',
       ['Khối tổng hợp: Vị trí còn hàng 0, Mặt hàng còn tồn 0; bảng hiện "%s"; ẩn phân trang; không báo lỗi.' % EMPTY], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE, OPEN + ['Gõ "ZZZ999" vào ô Hợp đồng, nhấn Enter.'], 'Hợp đồng: ZZZ999',
       ['Bảng hiện "%s"; khối tổng hợp Vị trí còn hàng 0.' % EMPTY], [9, 40])
S1.add('Số vị trí mặc định mỗi trang', 'P0', 'Tài khoản DNS Admin; kho "LN - Liên Ninh" (công ty TPE) có 767 vị trí còn hàng.',
       [MENU, 'Chọn Kho = "LN - Liên Ninh".'], '—',
       ['Trang 1 có 20 vị trí (I đến XX); dưới bảng "Hiển thị 1–20 / 767 vị trí"; Số dòng/trang = 20.'], [10, 16])
S1.add('Thay đổi số dòng / trang', 'P0', 'Tài khoản DNS Admin; kho LN 767 vị trí.', [MENU, 'Chọn Kho = LN.', 'Sang trang 2.',
       'Đổi Số dòng/trang thành 50.'], 'Số dòng/trang: 50',
       ['Bảng hiện 50 vị trí, về trang 1, "Hiển thị 1–50 / 767 vị trí".', 'Lựa chọn có 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P1', 'Tài khoản DNS Admin; kho LN 767 vị trí.', [MENU, 'Chọn Kho = LN.', 'Bấm ›.', 'Bấm ‹.'], '—',
       ['Bấm › sang trang 2: "Hiển thị 21–40 / 767", STT từ XXI.', 'Bấm ‹ về trang 1.'], 12)
S1.add('Trang đầu / trang cuối', 'P1', 'Tài khoản DNS Admin; kho LN 767 vị trí.', [MENU, 'Chọn Kho = LN.', 'Bấm ».', 'Bấm «.'], '—',
       ['Bấm » tới trang 39: "Hiển thị 761–767 / 767 vị trí".', 'Bấm « về trang 1.'], 13)
S1.add('Trạng thái nút ở trang đầu / cuối', 'P2', 'Tài khoản DNS Admin; kho LN 767 vị trí.',
       [MENU, 'Chọn Kho = LN.', 'Quan sát nút ở trang 1, rồi ở trang cuối.'], '—',
       ['Trang 1: nút « ‹ mờ, không bấm được.', 'Trang cuối: nút › » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P1', 'Tài khoản DNS Admin; kho LN 767 vị trí.', [MENU, 'Chọn Kho = LN.', 'Sang trang 2.'], '—',
       ['Vị trí đầu trang 2 có STT XXI (La Mã nối tiếp trang 1); dòng con đánh 1, 1.1, 1.1.1 trong từng vị trí.'], 15)
S1.add('Về trang 1 khi đổi bộ lọc', 'P1', 'Tài khoản DNS Admin; kho LN 767 vị trí.', [MENU, 'Chọn Kho = LN.', 'Sang trang 3.',
       'Chọn Thương hiệu = ENEOS.'], 'Thương hiệu: ENEOS',
       ['Báo cáo nạp lại từ trang 1; tổng N cập nhật theo bộ lọc.'], [17, 42])
S1.add('Thứ tự mặc định theo tên vị trí', 'P0', PRE, OPEN, '—',
       ['Vị trí xếp theo tên vị trí: KHOANG1, KHOANG2 … KHOANG7, rồi HP-TACH-GHEP (tên "Vị trí tách ghép hàng").',
        'Hàng hóa trong mỗi vị trí theo thứ tự tạo hàng (không theo tên).'], 19)
S1.add('Không sắp xếp theo cột', 'P2', PRE, OPEN + ['Bấm tiêu đề cột Mã hàng, SL tồn.'], '—',
       ['Thứ tự không đổi; tiêu đề cột không có biểu tượng sắp xếp.'], [20, 21, 22, 23])
S1.add('Giữ thứ tự khi chuyển trang', 'P2', 'Tài khoản DNS Admin; kho LN 767 vị trí.', [MENU, 'Chọn Kho = LN.', 'Sang trang 2, quay lại trang 1.'], '—',
       ['Trang 2 tiếp tục thứ tự tên vị trí; quay lại trang 1 đúng 20 vị trí như lúc đầu.'], 24)
S1.add('Thu gọn / mở rộng khối tổng hợp', 'P2', PRE, OPEN + ['Bấm Thu gọn.', 'Bấm Mở rộng.'], '—',
       ['Thu gọn: ẩn các ô Vị trí, Theo công ty thuê kho, còn dòng tóm tắt; chữ nút "Mở rộng".', 'Mở rộng: hiện lại, số không đổi.'], 3)
S1.add('Dòng tóm tắt báo cáo', 'P1', PRE, OPEN + ['Rê chuột vào chữ i cạnh dòng tóm tắt.'], '—',
       ['Dòng "Tồn kho tính đến ngày 07/11/2026 · Kho: HP - Hải Phòng".',
        'Chữ i hiện "BÁO CÁO TỒN KHO THEO VỊ TRÍ", 3 dòng giải thích, dòng cuối "Số liệu tính tại <ngày giờ>".'], 6)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Hợp đồng: khớp chính xác mã', 'P0', PRE_H, OPEN + ['Gõ "HĐ_TPHP_HP_KD_26_0183_CD" vào ô Hợp đồng, nhấn Enter.'],
       'Hợp đồng: HĐ_TPHP_HP_KD_26_0183_CD',
       ['Chỉ còn vị trí có lô thuộc hợp đồng này, trong đó có KHOANG1 với hàng ENEO-700-V5231.', 'Dòng lô chỉ còn lô của hợp đồng đó (SL 2).'], 26)
S2.add('Hợp đồng: khớp một phần mã', 'P0', PRE_H, OPEN + ['Gõ "26_0183" vào ô Hợp đồng, nhấn Enter.'], 'Hợp đồng: 26_0183',
       ['Kết quả như khi gõ đủ mã (khớp một phần).'], 27)
S2.add('Hợp đồng: không phân biệt hoa / thường', 'P1', PRE_H, OPEN + ['Gõ "hđ_tphp_hp_kd_26_0183" vào ô Hợp đồng, nhấn Enter.'],
       'Hợp đồng: hđ_tphp_hp_kd_26_0183', ['Kết quả như khi gõ chữ hoa.'], 28)
S2.add('Hợp đồng: chữ Đ và D khác nhau', 'P2', PRE_H, OPEN + ['Gõ "HD_TPHP_HP_KD_26_0183" (chữ D không gạch), nhấn Enter.'],
       'Hợp đồng: HD_TPHP_HP_KD_26_0183', ['Bảng hiện "%s" — hệ thống phân biệt Đ và D.' % EMPTY], 29)
S2.add('Hợp đồng: mã không tồn tại', 'P1', PRE, OPEN + ['Gõ "KHONGCO-123", nhấn Enter.'], 'Hợp đồng: KHONGCO-123', ['Bảng hiện "%s".' % EMPTY], 30)
S2.add('Hợp đồng: ký tự đặc biệt', 'P2', PRE, OPEN + ['Gõ "%", nhấn Enter.', 'Gõ "<script>", nhấn Enter.'], ['Hợp đồng: %', 'Hợp đồng: <script>'],
       ['Gõ "%": ra mọi vị trí có lô thuộc bất kỳ hợp đồng nào (ký tự % được hiểu là "bất kỳ").',
        'Gõ "<script>": bảng rỗng, không lỗi, không chạy mã.'], 31)
S2.add('Hợp đồng: khoảng trắng đầu / cuối', 'P1', PRE_H, OPEN + ['Gõ "  26_0183  ", nhấn Enter.'], 'Hợp đồng: "  26_0183  "',
       ['Kết quả như gõ "26_0183" (tự bỏ khoảng trắng đầu / cuối).'], 32)
S2.add('Hợp đồng: không giới hạn ký tự', 'P2', PRE, OPEN + ['Gõ chuỗi 300 ký tự "A", nhấn Enter.'], 'Hợp đồng: 300 ký tự',
       ['Ô nhận đủ, không báo lỗi; bảng hiện "%s".' % EMPTY], 33)
S2.add('Xóa chữ ở ô Hợp đồng', 'P1', [PRE, 'Đang lọc Hợp đồng = 26_0183.'], OPEN + ['Xóa hết chữ ô Hợp đồng, nhấn Enter.'], '—',
       ['Báo cáo trở lại 8 vị trí.'], 34)
S2.add('Hợp đồng chỉ áp khi Enter hoặc Tìm kiếm', 'P0', PRE_H, OPEN + ['Gõ "26_0183" nhưng không nhấn Enter.', 'Bấm Tìm kiếm.'], 'Hợp đồng: 26_0183',
       ['Sau bước 3 bảng chưa đổi.', 'Sau bước 4 báo cáo lọc theo hợp đồng, về trang 1.',
        'Bấm vào ô Hợp đồng hiện gợi ý "Gõ mã hợp đồng rồi Enter hoặc bấm Tìm kiếm."'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P0', 'Tài khoản DNS Admin công ty TPE, chưa mở màn trong 10 phút.', [MENU], '—',
       ['Tính đến ngày = hôm nay; Tồn theo công ty = công ty TPE; Kho, Công ty thuê kho, Nhóm, Tính chất, Loại, Thương hiệu, Hãng sản xuất, '
        'Hàng hóa, Hợp đồng trống; khối lọc mở sẵn; chưa có ô Nhà / Dãy / Khoang / Vị trí.'], 36)
S2.add('Thiếu Kho thì báo đỏ', 'P0', 'Tài khoản DNS Admin, công ty TPE (nhiều kho).', [MENU, 'Bấm Tìm kiếm.'], '—',
       ['Ô Kho viền đỏ, chữ "Vui lòng chọn kho"; không nạp báo cáo; bảng "%s".' % CHONKHO], [36, 37])
S2.add('Thiếu Tính đến ngày thì báo đỏ', 'P1', PRE, OPEN + ['Xóa ngày ở Tính đến ngày.', 'Bấm Tìm kiếm.'], '—',
       ['Ô Tính đến ngày chữ đỏ "Vui lòng chọn ngày"; bảng "Chọn ngày để xem báo cáo.".'], 37)
S2.add('Lọc Tính đến ngày quá khứ', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231.', 'Đổi Tính đến ngày = 31/12/2025.'],
       'Tính đến ngày: 31/12/2025', ['Vị trí KHOANG1 SL tồn 70; dòng TPHP Cộng 70; dòng tóm tắt "Tồn kho tính đến ngày 31/12/2025".'], 37)
S2.add('Đổi Tồn theo công ty thì bỏ kho', 'P1', PRE, OPEN + ['Đổi Tồn theo công ty sang công ty TPE.'], '—',
       ['Ô Kho về trống, Công ty thuê kho trống, ô Nhà / Dãy / Khoang / Vị trí ẩn, bảng "%s".' % CHONKHO,
        'Ô Kho chỉ còn kho của công ty TPE.'], 37)
S2.add('Đổi Kho tự chọn công ty thuê kho và nạp vị trí', 'P0', PRE, [MENU, 'Chọn Tồn theo công ty = %s.' % CN, 'Chọn Kho = HP - Hải Phòng.'], 'Kho: HP',
       ['Ô Công ty thuê kho tự tích TPE và TPHP; báo cáo nạp ngay.',
        'Hiện 4 cột Nhà / Dãy / Khoang / Vị trí: cột Nhà có N1 - Nhà 1, TANG1 - Tầng 1, TANG2 - Tầng 2; cột Vị trí có nhóm "Vị trí tự do" với HP-TACH-GHEP.'], 37)
S2.add('Lọc Công ty thuê kho', 'P0', PRE, OPEN + ['Bỏ TPHP ở Công ty thuê kho (còn TPE).'], 'Công ty thuê kho: TPE',
       ['Còn 1 vị trí; khối Theo công ty thuê kho chỉ còn ô TPE 1 vị trí.'], 37)
S2.add('Lọc theo Nhà và Dãy', 'P0', PRE, OPEN + ['Tick Nhà "TANG1 - Tầng 1".', 'Tick Dãy "D1 - Dãy 1".'], 'Nhà: TANG1\nDãy: D1',
       ['Sau bước 3: cột Dãy hiện nhóm "TANG1 - Tầng 1" với D1 - Dãy 1.', 'Sau bước 4: cột Khoang hiện K1 – K7; báo cáo còn 7 vị trí, 95 mặt '
        'hàng (không còn vị trí tự do HP-TACH-GHEP).'], 37)
S2.add('Lọc Khoang và Vị trí, bỏ tick cha', 'P1', PRE, OPEN + ['Tick TANG1, D1, Khoang K1.', 'Tick vị trí KHOANG1.', 'Bỏ tick Nhà TANG1.'], '—',
       ['Sau bước 4: báo cáo chỉ còn vị trí KHOANG1 (1,634).', 'Sau bước 5: các tick Dãy / Khoang / Vị trí con tự bỏ, báo cáo trở lại 8 vị trí.'], 37)
S2.add('Tìm trong cột vị trí và Chọn hết', 'P2', PRE, OPEN + ['Gõ "tầng" vào ô tìm của cột Nhà.', 'Tick "Chọn hết" của cột Nhà.'], 'Tìm: tầng',
       ['Cột Nhà chỉ còn TANG1, TANG2 (khớp một phần tên, không phân biệt hoa / thường).', '"Chọn hết" chỉ tick 2 nhà đang hiện.'], [37, 45])
S2.add('Lọc Nhóm, Tính chất, Loại, Hãng sản xuất', 'P1', PRE, OPEN + ['Lần lượt chọn 1 giá trị ở từng ô, sau mỗi ô bỏ chọn.'], '—',
       ['Mỗi lần chỉ còn vị trí chứa mặt hàng thuộc giá trị đã chọn; bỏ chọn trở lại 8 vị trí.', 'Loại hàng hóa: hàng thuộc ít nhất 1 loại đã chọn.'], 37)
S2.add('Lọc Thương hiệu', 'P1', PRE, OPEN + ['Chọn Thương hiệu = ENEOS.'], 'Thương hiệu: ENEOS', ['Mọi dòng hàng hóa có Thương hiệu ENEOS.'], 37)
S2.add('Kết hợp nhiều ô lọc', 'P0', PRE_H, OPEN + ['Tick Nhà TANG1.', 'Gõ "26_0183" ở Hợp đồng, Enter.'], ['Nhà: TANG1', 'Hợp đồng: 26_0183'],
       ['Chỉ còn vị trí thỏa CẢ 2 điều kiện; có KHOANG1 với hàng ENEO-700-V5231.'], [38, 39])
S2.add('Tổng và phân trang sau lọc', 'P1', PRE, OPEN + ['Chọn Thương hiệu = ENEOS.'], 'Thương hiệu: ENEOS',
       ['Ô Vị trí còn hàng = số ở dòng TỔNG = N ở "Hiển thị 1–x / N"; số trang tính lại theo N.'], [41, 42])
S2.add('Thứ tự sau lọc', 'P2', PRE, OPEN + ['Chọn Thương hiệu = ENEOS.'], '—', ['Kết quả vẫn xếp theo tên vị trí.'], 43)
S2.add('Xóa lọc', 'P0', [PRE, 'Đang lọc kho HP, Nhà TANG1, Hợp đồng 26_0183.'], OPEN + ['Bấm Xóa lọc.'], '—',
       ['Tính đến ngày về hôm nay, Tồn theo công ty về công ty của tài khoản, các ô khác trống (kể cả Kho, Hàng hóa, tick vị trí).',
        'Bảng "%s"; chữ đỏ biến mất; ô Nhà / Dãy / Khoang / Vị trí ẩn.' % CHONKHO], 44)
S2.add('Chuyển màn rồi quay lại', 'P1', [PRE, 'Đang lọc kho HP.'], OPEN + ['Mở màn Thẻ kho.', MENU], '—',
       ['Bộ lọc về mặc định (kho trống).'], 45)
S2.add('Tải lại trang (F5)', 'P0', [PRE, 'Đang lọc kho HP, hàng ENEO-700-V5231, Nhà TANG1.'], OPEN + ['Nhấn F5 trong vòng 10 phút.'], '—',
       ['Giữ nguyên kho HP, tick TANG1, ô Hàng hóa vẫn hiện "ENEO-700-V5231 - Dầu nh…", báo cáo nạp lại.', 'Sau hơn 10 phút F5: bộ lọc về mặc định.'], 46)
S2.add('Mở tab mới', 'P2', [PRE, 'Đang lọc kho HP.'], OPEN + ['Mở màn ở tab mới trong 10 phút.'], '—', ['Tab mới khôi phục bộ lọc kho HP.'], 47)
S2.add('Tài khoản khác cùng trình duyệt', 'P2', [PRE, ACC_C, 'DNS Admin vừa lọc kho HP rồi đăng xuất (trong 10 phút).'],
       ['Đăng nhập C trên cùng trình duyệt.', MENU], '—',
       ['Nếu bộ lọc ghi tạm còn hạn, C thấy kho HP được chọn sẵn (kho HP thuộc công ty C); kho / công ty ngoài phạm vi của C bị bỏ.'], 48)
S2.add('Cài đặt bộ lọc: mở cửa sổ', 'P1', PRE, OPEN + ['Bấm Cài đặt bộ lọc.'], '—',
       ['Cửa sổ "Cài đặt bộ lọc" liệt kê 12 ô lọc có ô tích (gồm "Nhà / Dãy / Khoang / Vị trí"), nút Lưu, Khôi phục mặc định, Đóng.'], 37)
S2.add('Cài đặt bộ lọc: ẩn ô và lưu', 'P1', PRE, OPEN + ['Bấm Cài đặt bộ lọc.', 'Bỏ tích Hãng sản xuất.', 'Bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công"; khối lọc không còn ô Hãng sản xuất; F5 vẫn ẩn.'], 37)
S2.add('Cài đặt bộ lọc: đổi thứ tự, khôi phục, đóng', 'P2', PRE,
       OPEN + ['Bấm Cài đặt bộ lọc.', 'Kéo Hợp đồng lên đầu, bấm Đóng.', 'Mở lại, bấm Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bấm Đóng: thứ tự không đổi.', 'Khôi phục + Lưu: đủ các ô theo thứ tự gốc.'], 37)
S2.add('Chọn hàng hóa: mở cửa sổ', 'P0', 'Tài khoản DNS Admin, công ty TPE, kho LN - Liên Ninh.',
       [MENU, 'Chọn Kho = LN - Liên Ninh.', 'Bấm ô Hàng hóa.'], '—',
       ['Mở cửa sổ "Chọn hàng hóa": dòng công ty TPE, cây catalog, ô tìm, công tắc Còn tồn / Gồm hàng ngoài catalog, bảng hàng, nút Đóng.',
        'Chân cửa sổ ghi "Bấm vào tên hàng để chọn".'], 37)
S2.add('Chọn hàng hóa: chọn 1 hàng', 'P0', PRE_H, OPEN + ['Bấm ô Hàng hóa.', 'Tìm "ENEO-700-V5231", bấm tên hàng.'], 'Hàng hóa: ENEO-700-V5231',
       ['Cửa sổ đóng; ô Hàng hóa hiện thẻ "ENEO-700-V5231 - Dầu nh…" có dấu ×; báo cáo còn 1 vị trí KHOANG1 (nạp 1 lần).'], 37)
S2.add('Chọn hàng hóa: bỏ chọn bằng dấu ×', 'P1', [PRE_H, 'Đang chọn hàng ENEO-700-V5231.'], OPEN + ['Bấm dấu × trên thẻ Hàng hóa.'], '—',
       ['Ô Hàng hóa trống, cửa sổ không mở; báo cáo trở lại 8 vị trí.'], [34, 37])
S2.add('Chọn hàng hóa: đóng không chọn', 'P2', PRE, OPEN + ['Bấm ô Hàng hóa.', 'Bấm Đóng.'], '—', ['Cửa sổ đóng, bộ lọc không đổi.'], 37)
S2.add('Chọn hàng hóa với công ty khác công ty đăng nhập', 'P1', 'Tài khoản DNS Admin đăng nhập công ty TPE.',
       OPEN + ['Bấm ô Hàng hóa.'], '—',
       ['Cửa sổ ghi "Công ty %s".' % CN, 'Cây catalog có số hàng, không báo "Không tải được số lượng"; chọn được hàng.'], 37)

# ============================================================== III. SỐ LIỆU BÁO CÁO
S3 = Sec(3)
S3.add('Khối tổng hợp', 'P0', PRE, OPEN, '—',
       ['Ô Vị trí còn hàng 8 vị trí; Mặt hàng còn tồn 96 mặt hàng; Công ty thuê kho có tồn 2 công ty.',
        'Khối Theo công ty thuê kho: TPE 1 vị trí, TPHP 8 vị trí.'], 6)
S3.add('Dòng TỔNG khớp khối tổng hợp và tổng số', 'P0', PRE, OPEN, '—',
       ['Dòng TỔNG "VỊ TRÍ CÒN HÀNG 8 vị trí" = ô Vị trí còn hàng = N ở "Hiển thị 1–8 / 8 vị trí".',
        'Cột SL tồn dòng TỔNG = 8,530 = tổng SL tồn 8 dòng vị trí.'], [16, 41])
S3.add('Dòng TỔNG và khối tổng hợp không đổi khi sang trang', 'P1', 'Tài khoản DNS Admin; kho LN 767 vị trí.',
       [MENU, 'Chọn Kho = LN.', 'Sang trang 2.'], '—', ['Dòng TỔNG, các ô khối tổng hợp giữ nguyên số của trang 1.'], 16)
S3.add('Ô Công ty thuê kho có tồn ẩn khi bằng 0', 'P2', 'Tài khoản DNS Admin; kho DATD không còn hàng.',
       [MENU, 'Chọn công ty TPE, Kho = DATD.'], '—', ['Chỉ còn ô Vị trí còn hàng 0, Mặt hàng còn tồn 0; không có khối Theo công ty thuê kho.'], 8)
S3.add('Đối soát tổng các vị trí với Thẻ kho', 'P0',
       [PRE_H, 'Thẻ kho của hàng tại kho HP, công ty thuê TPHP, kỳ 01/01/2026–07/11/2026: Tồn đầu kỳ 70, Nhập 496, Xuất 546, Tồn cuối kỳ 20.'],
       ['Mở Thẻ kho, chọn hàng ENEO-700-V5231, kho HP, công ty thuê TPHP, kỳ từ 01/01/2026 đến 07/11/2026; ghi Tồn đầu, Nhập, Xuất, Tồn cuối.',
        MENU, CHON_HP, 'Chọn hàng ENEO-700-V5231, Tính đến ngày 07/11/2026; cộng Cộng của dòng TPHP ở mọi vị trí.'], 'Tính đến ngày: 07/11/2026',
       ['70 + 496 - 546 = 20 = tổng các vị trí (chỉ KHOANG1: 20).'], 6)
S3.add('Đối soát với Báo cáo tồn kho chi tiết theo mặt hàng', 'P0', PRE_H,
       ['Mở Báo cáo tồn kho chi tiết theo mặt hàng, chọn công ty %s, kho HP, ngày 07/11/2026, hàng ENEO-700-V5231.' % CN,
        'Ghi SL tồn của hàng, các lô và tổng số mặt hàng của kho.', MENU, CHON_HP, 'Chọn hàng ENEO-700-V5231.'], '—',
       ['SL tồn bằng nhau (20); 4 lô cùng mã, cùng SL (6, 2, 6, 6) ở vị trí KHOANG1.',
        'Khi bỏ chọn hàng: Mặt hàng còn tồn 96 = số mặt hàng của báo cáo chi tiết theo mặt hàng.'], 6)
S3.add('Đối soát ngày quá khứ', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231, Tính đến ngày 31/12/2025, chọn cấp "Tất cả cấp (đến lô)".'],
       'Tính đến ngày: 31/12/2025',
       ['Vị trí KHOANG1 SL tồn 70 = Tồn đầu kỳ của Thẻ kho kỳ bắt đầu 01/01/2026 = SL tồn ở Báo cáo tồn kho chi tiết theo mặt hàng ngày 31/12/2025.',
        'Các lô là số tại ngày 31/12/2025 (30, 1, 3, 30, 6), tổng 70 = Cộng — số lô CẮT theo ngày.'], 6)
S3.add('Lập chứng từ nhập thì số tăng', 'P0', [PRE_H, 'Lập và hoàn tất 1 Phiếu nhập kho 5 Xô 18L hàng ENEO-700-V5231 vào kho HP, công ty TPHP, vị trí KHOANG2 (môi trường kiểm thử).'],
       OPEN + ['Chọn hàng ENEO-700-V5231, Tính đến ngày hôm nay.'], '—',
       ['Xuất hiện thêm vị trí KHOANG2 SL 5 (lô mới SL 5); KHOANG1 giữ 20.', 'Chọn Tính đến ngày = hôm qua: không có KHOANG2.'], [274, 281])
S3.add('Lập chứng từ xuất thì số giảm', 'P0', [PRE_H, 'Hoàn tất 1 Phiếu xuất kho 2 Xô 18L hàng ENEO-700-V5231 từ kho HP, lô thứ 2 ở KHOANG1 (môi trường kiểm thử).'],
       OPEN + ['Chọn hàng ENEO-700-V5231, chọn cấp "Tất cả cấp".'], '—',
       ['KHOANG1 giảm 2 (20 thành 18); lô thứ 2 hết số lượng nên dòng lô biến mất.'], [274, 281])
S3.add('Dòng hàng hóa bằng tổng các công ty', 'P0', [PRE, 'Kho LN - Liên Ninh: có vị trí chứa hàng của cả TPE và TPSG.'],
       [MENU, 'Chọn công ty TPE, Kho = LN - Liên Ninh.', 'Tìm 1 dòng hàng hóa có 2 dòng công ty.'], '—',
       ['SL tồn dòng hàng hóa = tổng Cộng các dòng công ty bên dưới.'], 283)
S3.add('Cộng bằng tổng các lô', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231, chọn cấp "Tất cả cấp (đến lô)".'], '—',
       ['Dòng TPHP Cộng 20 = 6 + 2 + 6 + 6 (cột SL các lô).'], 283)
S3.add('SL tồn vị trí bằng tổng các hàng hóa', 'P0', PRE, OPEN + ['Chọn cấp "Đến hàng hóa", xem vị trí KHOANG1.'], '—',
       ['SL tồn KHOANG1 = 1,634 = tổng SL tồn 9 dòng hàng hóa bên dưới (khi để ĐVT cơ sở).'], 283)
S3.add('SL vị trí cộng thẳng ĐVT cơ sở', 'P1', [PRE, '%s nằm ở KHOANG1: 600 Lít.' % HANG2],
       OPEN + ['Ở dòng ENEO-800-V5231 chọn ĐVT "Phuy 200L (x200)".'], 'ĐVT: Phuy 200L (x200)',
       ['Dòng hàng hóa còn 3; dòng vị trí KHOANG1 vẫn 1,634 (không quy đổi) — đúng thiết kế, giữ như hệ thống cũ.'], 6)
S3.add('Định dạng số', 'P1', PRE, OPEN, '—',
       ['SL tồn, SL, Cộng căn phải, phân cách hàng nghìn bằng dấu phẩy (vd 1,634; 8,530), số nguyên khi không lẻ.'], 6)
S3.add('Một hàng nằm ở nhiều vị trí', 'P1', [PRE, 'Kho HP: tổng số mặt hàng theo từng vị trí là 97 nhưng chỉ 96 mặt hàng khác nhau.'], OPEN, '—',
       ['Ô Mặt hàng còn tồn 96 (đếm mỗi hàng 1 lần dù nằm ở 2 vị trí).',
        'Ô TPE 1 + TPHP 8 = 9 lớn hơn 8 vị trí (1 vị trí có hàng của 2 công ty).'], 286)

# ============================================================== IV. XEM CHI TIẾT
S4 = Sec(4)
S4.add('Bung chi tiết mặc định tới công ty', 'P0', PRE, OPEN, '—',
       ['Mặc định ô chọn cấp "Đến công ty thuê kho": mỗi vị trí bung dòng hàng hóa và dòng công ty, chưa hiện lô.'], 186)
S4.add('Tiêu đề cột và ô chọn cấp', 'P1', PRE, OPEN + ['Mở ô chọn cấp.'], '—',
       ['Cột thứ 2 "Vị trí / Hàng hóa / Công ty / Lô"; ô chọn cấp có 4 lựa chọn: Chỉ vị trí, Đến hàng hóa, Đến công ty thuê kho, Tất cả cấp (đến lô).'], 187)
S4.add('Chọn cấp Tất cả cấp', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231.', 'Chọn cấp "Tất cả cấp (đến lô)".'], '—',
       ['Hiện: I KHOANG1 20 > 1 hàng ENEO-700-V5231 20 > 1.1 TPHP Cộng 20 > 1.1.1 – 1.1.4 bốn lô SL 6, 2, 6, 6.'], [188, 189])
S4.add('Chọn cấp Chỉ vị trí và Đến hàng hóa', 'P1', PRE, OPEN + ['Chọn cấp "Chỉ vị trí".', 'Chọn cấp "Đến hàng hóa".'], '—',
       ['Chỉ vị trí: chỉ 8 dòng vị trí.', 'Đến hàng hóa: thêm dòng hàng hóa, chưa có công ty.'], 186)
S4.add('Bung / thu riêng một dòng', 'P1', PRE, OPEN + ['Bấm mũi tên ở dòng vị trí I.', 'Bấm lại.'], '—',
       ['Lần 1 thu dòng con của vị trí I, các vị trí khác giữ nguyên; lần 2 bung lại.', 'Rê chuột mũi tên: "Ẩn hàng hóa" / "Hiện hàng hóa".'], 196)
S4.add('Dữ liệu chi tiết khớp danh sách', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231, cấp "Tất cả cấp".'], '—',
       ['Tổng lô = Cộng TPHP = SL hàng hóa = SL vị trí = 20.'], 190)
S4.add('Chi tiết chỉ đọc', 'P1', PRE, OPEN + ['Bấm vào tên hàng, mã lô, số lượng.'], '—',
       ['Không có ô nhập, không có nút Lưu / Sửa / Xóa; bấm chữ không mở màn khác.'], [191, 192, 193])
S4.add('Công ty không còn lô có tồn tại vị trí', 'P2', [PRE, 'Một công ty thuê có hàng > 0 tại vị trí nhưng mọi lô của hàng ở vị trí đó đã về 0.'], OPEN, '—',
       ['Dòng công ty không có mũi tên, kèm chữ xám "Không còn lô có tồn tại vị trí"; Cộng = số cộng dồn của vị trí.'], 193)
S4.add('Đổi ĐVT trên dòng hàng hóa', 'P0', [PRE, '%s tồn 600 Lít tại KHOANG1.' % HANG2],
       OPEN + ['Tìm dòng ENEO-800-V5231.', 'Ở cột ĐVT chọn "Phuy 200L (x200)".'], 'ĐVT: Phuy 200L (x200)',
       ['SL tồn dòng hàng hóa và Cộng dòng công ty đổi thành 3.', 'Các mặt hàng khác và dòng vị trí không đổi.'], 189)
S4.add('Quy đổi làm tròn số nguyên', 'P1', [PRE, 'Hàng Y tồn 13 Cái tại 1 vị trí, có ĐVT Thùng x12.'], OPEN + ['Ở dòng Y chọn ĐVT Thùng.'], 'ĐVT: Thùng (x12)',
       ['SL hiện "1" (13 ÷ 12 = 1,08 làm tròn số nguyên).'], 189)
S4.add('Hàng 1 ĐVT không có ô chọn', 'P2', PRE, OPEN, '—', ['Dòng ENEO-700-V5231 cột ĐVT hiện chữ "Xô 18L", không có ô chọn.'], 191)
S4.add('Xem hợp đồng của lô', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231, cấp "Tất cả cấp".', 'Rê chuột lên mã lô 1.1.2.',
       'Bấm mã "HĐ_TPHP_HP_KD_26_0183_CD" sau chữ "Hợp đồng:" trong ô Lô.'], '—',
       ['Rê chuột hiện mã lô và "Hợp đồng: HĐ_TPHP_HP_KD_26_0183_CD".',
        'Bấm mã mở tab mới xem hợp đồng ở hệ thống cũ; tab báo cáo giữ nguyên.',
        'Lưu ý: mã lô dài có thể che mất chữ "Hợp đồng: …" trong ô — khi đó chỉ xem được bằng rê chuột.'], 186)
S4.add('Giữ trang và bộ lọc khi quay lại', 'P1', [PRE, 'Kho LN, đang ở trang 3, lọc Thương hiệu ENEOS.'], ['Bấm mã hợp đồng mở tab mới, đóng tab đó.'], '—',
       ['Tab báo cáo vẫn ở trang 3, giữ bộ lọc và cấp bung.'], 197)
S4.add('Đổi trang áp lại cấp bung', 'P2', 'Tài khoản DNS Admin; kho LN 767 vị trí.', [MENU, 'Chọn Kho = LN.', 'Thu riêng vị trí I.', 'Sang trang 2 rồi về trang 1.'], '—',
       ['Vị trí I bung lại theo cấp đang chọn (bung / thu riêng lẻ bị bỏ).'], 196)

# ============================================================== V. XUẤT DANH SÁCH EXCEL
S5 = Sec(5)
S5.add('Mở cửa sổ xuất Excel', 'P0', PRE, OPEN + ['Bấm Xuất Excel ở đầu khối lọc.'], '—',
       ['Mở cửa sổ "Xuất Excel báo cáo tồn kho theo vị trí", Kiểu xuất có Đầy đủ (chọn sẵn) và Ngắn gọn, nút Xuất Excel, Hủy.'], [212, 213, 214])
S5.add('Xuất kiểu Đầy đủ', 'P0', PRE, OPEN + ['Bấm Xuất Excel.', 'Giữ Đầy đủ, bấm Xuất Excel trong cửa sổ.'], 'Kiểu xuất: Đầy đủ',
       ['Tải file "%s"; cửa sổ đóng.' % FILE,
        'Cột: STT, Nhà kho, Vị trí, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn, nhóm "Chi tiết tồn theo từng công ty" (Công ty, Lô, SL, Cộng).'],
       [215, 216, 223, 225])
S5.add('Xuất kiểu Ngắn gọn', 'P0', PRE, OPEN + ['Bấm Xuất Excel.', 'Chọn Ngắn gọn, bấm Xuất Excel.'], 'Kiểu xuất: Ngắn gọn',
       ['File chỉ có STT, Nhà kho, Vị trí, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn; mỗi mặt hàng 1 dòng.'], [217, 226])
S5.add('Không có bước chọn trường', 'P2', PRE, OPEN + ['Bấm Xuất Excel.'], '—', ['Cửa sổ không có danh sách chọn cột; luôn xuất đủ cột của kiểu.'], 218)
S5.add('Xuất theo bộ lọc', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231.', 'Xuất Excel kiểu Đầy đủ.'], '—',
       ['File chỉ có vị trí KHOANG1, 1 mặt hàng, 4 dòng lô; Cộng 20; dòng Tổng cộng 20.'], [219, 220])
S5.add('Xuất mọi trang', 'P0', 'Tài khoản DNS Admin; kho LN 767 vị trí.', [MENU, 'Chọn Kho = LN.', 'Đang ở trang 1 (20 vị trí), xuất kiểu Ngắn gọn.'], '—',
       ['File có đủ 767 vị trí (không riêng trang đang xem).'], [221, 227])
S5.add('Xuất khi báo cáo rỗng', 'P1', 'Tài khoản DNS Admin; kho DATD không còn hàng.', [MENU, 'Chọn công ty TPE, Kho = DATD.', 'Xuất Excel kiểu Đầy đủ.'], '—',
       ['Vẫn tải file: letterhead, tiêu đề, Tính đến ngày, Kho, hàng tên cột, 1 dòng "Không có dữ liệu", khối ký.'], 222)
S5.add('Chưa chọn kho thì không xuất', 'P1', 'Tài khoản DNS Admin, công ty TPE.', [MENU, 'Bấm Xuất Excel.'], '—',
       ['Không mở cửa sổ; ô Kho chữ đỏ "Vui lòng chọn kho".'], 222)
S5.add('Định dạng file', 'P1', PRE, OPEN + ['Xuất kiểu Đầy đủ, mở file.'], '—',
       ['File .xlsx mở được; dòng 1 letterhead công ty CN Hải Phòng; tiêu đề "BÁO CÁO TỒN KHO THEO VỊ TRÍ"; "Tính đến ngày: 07/11/2026"; '
        '"Kho: HP - Hải Phòng".', 'Dòng "Tổng cộng" dưới cột SL tồn = 8,530; cuối file khối ký Trưởng kho, Người lập báo cáo kèm ngày.'], 224)
S5.add('Dữ liệu khớp màn hình', 'P0', PRE_H, OPEN + ['Xuất kiểu Đầy đủ, tìm ENEO-700-V5231 trong file.'], '—',
       ['Vị trí KHOANG1, Nhà kho TANG1; Tên, Model, Mã, Thương hiệu, ĐVT "Xô 18L", SL tồn của vị trí 1,634 khớp màn.',
        'Ô Lô thứ 2 ghi kèm "Hợp đồng: HĐ_TPHP_HP_KD_26_0183_CD".'], 228)
S5.add('Số là ô số, theo ĐVT cơ sở', 'P1', [PRE, '%s; trên màn đang chọn ĐVT Phuy.' % HANG2], OPEN + ['Xuất kiểu Ngắn gọn, mở file.'], '—',
       ['Dòng ENEO-800-V5231 ghi ĐVT "Lít", số 600 (ĐVT cơ sở).', 'Ô số có phân cách hàng nghìn, cộng SUM được; số 0 để trống.'], 229)
S5.add('Tiếng Việt và ký tự đặc biệt', 'P2', PRE, OPEN + ['Xuất, mở file.'], '—',
       ['Tên hàng có dấu, ký tự "(", "/", "-" hiển thị đúng, không lỗi phông.'], 230)
S5.add('Hủy xuất', 'P2', PRE, OPEN + ['Bấm Xuất Excel.', 'Bấm Hủy.'], '—', ['Cửa sổ đóng, không tải file; mở lại kiểu về Đầy đủ.'], 212)
S5.add('Đang xuất thì khóa nút', 'P1', 'Tài khoản DNS Admin; kho LN 767 vị trí.', [MENU, 'Chọn Kho LN.', 'Xuất Excel kiểu Đầy đủ, bấm liên tục 2 lần.'], '—',
       ['Nút đổi chữ "Đang xuất…", có vòng xoay, không nhận lần bấm thứ 2; chỉ tải 1 file.'], 221)

# ============================================================== VI. IN BÁO CÁO
S6 = Sec(6)
S6.add('Mở cửa sổ In báo cáo', 'P0', PRE, OPEN + ['Bấm In danh sách.'], '—',
       ['Cửa sổ "In báo cáo": kiểu Đầy đủ chọn sẵn, Ngắn gọn; "Chọn cột in" tích sẵn 12 cột; nút In, Hủy.'], 212)
S6.add('Đổi kiểu in đổi danh sách cột', 'P1', PRE, OPEN + ['Bấm In danh sách.', 'Chọn Ngắn gọn.'], '—',
       ['Danh sách cột còn 8: Nhà kho, Vị trí, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn.'], 213)
S6.add('Bỏ hết cột thì báo lỗi', 'P0', PRE, OPEN + ['Bấm In danh sách.', 'Bỏ tích Chọn tất cả.', 'Bấm In.'], '—',
       ['Chữ đỏ "Vui lòng chọn ít nhất 1 cột để in"; cửa sổ không đóng.'], 218)
S6.add('Xem trước bản in kiểu Đầy đủ', 'P0', PRE, OPEN + ['Bấm In danh sách, bấm In.'], '—',
       ['Mở "Xem trước báo cáo tồn kho theo vị trí" khổ ngang: letterhead CN Hải Phòng, tiêu đề "BÁO CÁO TỒN KHO THEO VỊ TRÍ", Tính đến ngày, '
        'Kho, bảng 8 vị trí gộp ô theo vị trí / hàng / công ty, dòng Tổng cộng 8,530, khối ký Trưởng kho, Người lập báo cáo.'], [219, 221])
S6.add('In theo cột đã chọn', 'P1', PRE, OPEN + ['Bấm In danh sách.', 'Bỏ tích Model và Thương hiệu, bấm In.'], '—',
       ['Bản xem trước không có cột Model, Thương hiệu; cột STT luôn có.'], 217)
S6.add('Bấm In trên bản xem trước', 'P1', PRE, OPEN + ['Mở xem trước, bấm In.'], '—', ['Hộp thoại in của trình duyệt mở, nội dung đúng bản xem trước.'], 219)
S6.add('Vượt mức in tối đa', 'P1', 'Tài khoản DNS Admin; kho LN 767 vị trí, kiểu Đầy đủ hơn 2.000 dòng lô.',
       [MENU, 'Chọn công ty TPE, Kho LN.', 'Bấm In danh sách, giữ Đầy đủ, bấm In.'], '—',
       ['Bản xem trước không có nội dung, hiện "Danh sách có … dòng, vượt mức in tối đa 2.000 dòng nên chưa in được…"; nút In ẩn.'], 221)
S6.add('Chưa chọn kho thì không in', 'P1', 'Tài khoản DNS Admin, công ty TPE.', [MENU, 'Bấm In danh sách.'], '—',
       ['Không mở cửa sổ; ô Kho chữ đỏ "Vui lòng chọn kho".'], 222)
S6.add('Số in theo ĐVT cơ sở', 'P2', [PRE, '%s; trên màn đang chọn ĐVT Phuy.' % HANG2], OPEN + ['In kiểu Ngắn gọn.'], '—',
       ['Bản in ghi 600, ĐVT "Lít".'], 229)
S6.add('Hủy in', 'P2', PRE, OPEN + ['Bấm In danh sách, bấm Hủy.', 'Mở xem trước rồi bấm ×.'], '—', ['Đóng cửa sổ, không in; báo cáo giữ nguyên.'], 196)

# ============================================================== VII. RÀNG BUỘC
S7 = Sec(7)
S7.add('Phiếu điều chuyển kho', 'P0', [PRE_H, 'Hoàn tất phiếu điều chuyển 3 Xô 18L hàng ENEO-700-V5231 từ kho HP sang kho CB (môi trường kiểm thử).'],
       OPEN + ['Chọn hàng ENEO-700-V5231.', 'Đổi Kho = CB - Cát Bà.'], '—',
       ['Kho HP: KHOANG1 giảm 3; kho CB: vị trí nhận tăng 3 (có thêm lô).'], [274, 281, 282])
S7.add('Phiếu điều chuyển vị trí', 'P0', [PRE_H, 'Hoàn tất phiếu điều chuyển vị trí 2 Xô 18L của 1 lô từ KHOANG1 sang KHOANG2 (môi trường kiểm thử).'],
       OPEN + ['Chọn hàng ENEO-700-V5231, cấp "Tất cả cấp".'], '—',
       ['KHOANG1 còn 18; xuất hiện KHOANG2 SL 2 cùng mã lô.', 'Tổng 2 vị trí vẫn 20 = Báo cáo tồn kho chi tiết theo mặt hàng (không đổi).'], [272, 284])
S7.add('Nhập / xuất điều chỉnh kiểm kê', 'P1', [PRE_H, 'Hoàn tất phiếu nhập kho điều chỉnh kiểm kê +1 và phiếu xuất kho điều chỉnh kiểm kê -1 tại KHOANG1 cho hàng này.'],
       OPEN + ['Chọn hàng ENEO-700-V5231 sau mỗi phiếu.'], '—', ['Sau phiếu nhập: KHOANG1 21; sau phiếu xuất: 20.'], 274)
S7.add('Khai báo tồn kho đầu kỳ', 'P1', [PRE, 'Khai báo tồn đầu kỳ 10 Cái hàng Z (chưa từng có ở kho HP) cho công ty TPHP, vị trí KHOANG3.'],
       OPEN + ['Chọn hàng Z.'], '—', ['Hàng Z xuất hiện ở KHOANG3, SL 10, dòng công ty TPHP, lô tồn đầu kỳ.'], 274)
S7.add('Đổi tên hàng ở danh mục', 'P2', [PRE_H, 'Đổi tên hàng ENEO-700-V5231 ở danh mục hàng hóa (môi trường kiểm thử).'], OPEN + ['Chọn hàng ENEO-700-V5231.'], '—',
       ['Báo cáo hiện tên mới, số không đổi.'], [278, 279])
S7.add('Đổi danh mục Nhà / Dãy / Khoang / Vị trí', 'P2', [PRE, 'Thêm vị trí mới KHOANG8 vào Khoang K7 ở danh mục Vị trí (chưa có hàng).'],
       OPEN + ['Tick TANG1, D1, K7.'], '—', ['Cột Vị trí có KHOANG8; báo cáo không có dòng KHOANG8 (chưa có hàng).'], [278, 280])
S7.add('Kho ngừng hoạt động không còn trong ô Kho', 'P1', ['Tài khoản DNS Admin.', 'Kho NM - Nhà máy chuyển sang ngừng hoạt động ở danh mục Kho vật lý.'],
       [MENU, 'Chọn công ty CN Hải Phòng, mở ô Kho.'], '—', ['Ô Kho không còn NM - Nhà máy.'], [276, 285])
S7.add('Đổi công ty thuê kho ở danh mục Kho kế toán', 'P2', [PRE, 'Bỏ gắn công ty TPE khỏi kho HP ở danh mục Kho kế toán.'],
       [MENU, CHON_HP], '—', ['Ô Công ty thuê kho chỉ còn TPHP; khối Theo công ty thuê kho không còn TPE.'], [280, 282])
S7.add('Màn chỉ đọc, không làm đổi dữ liệu', 'P0', PRE, OPEN + ['Thao tác lọc, tick vị trí, bung, đổi ĐVT, in, xuất nhiều lần.', 'Mở Thẻ kho cùng hàng / kho.'], '—',
       ['Không có chứng từ, tồn kho hay lịch sử nào thay đổi; Thẻ kho giữ nguyên số.'], [268, 270, 285])
S7.add('Đối chiếu với Thẻ kho sau khi lập chứng từ', 'P0', [PRE_H, 'Vừa hoàn tất 1 phiếu nhập và 1 phiếu xuất cho hàng này hôm nay.'],
       ['Mở Thẻ kho kỳ 01/01–hôm nay, ghi Tồn cuối kỳ.', MENU, CHON_HP, 'Chọn hàng ENEO-700-V5231.'], '—',
       ['Tồn cuối kỳ Thẻ kho = tổng Cộng dòng TPHP ở mọi vị trí.'], [274, 281])

# ============================================================== VIII. PHÂN QUYỀN
S8 = Sec(8)
S8.add('Quyền theo tổng công ty', 'P0', ACC_T, ['Đăng nhập T.', MENU, 'Mở ô Tồn theo công ty, ô Kho.'], '—',
       ['Ô Tồn theo công ty có mọi công ty đang hoạt động (6 công ty); ô Kho có mọi kho của công ty đang chọn.', 'Xem, in, xuất được.'], [287, 299])
S8.add('Quyền theo công ty', 'P0', ACC_C, ['Đăng nhập C.', MENU, 'Mở ô Tồn theo công ty, ô Kho.'], '—',
       ['Ô Tồn theo công ty chỉ có CN Hải Phòng; ô Kho có CB, HP, KĐN-ALM, NM.', 'Xem, in, xuất được.'], [287, 299])
S8.add('Quyền theo kho', 'P0', ACC_K, ['Đăng nhập K.', MENU], '—',
       ['Ô Kho chỉ có HP - Hải Phòng và được chọn sẵn (1 kho); báo cáo hiện ngay 8 vị trí.'], [287, 299])
S8.add('Không có quyền nào', 'P0', ACC_N, ['Đăng nhập N.', MENU], '—',
       ['Mục menu vẫn hiện; ô Tồn theo công ty, Kho rỗng; bảng "Chọn công ty để xem báo cáo.", không có số liệu.',
        'Bấm In danh sách / Xuất Excel: chữ đỏ dưới ô thiếu, không ra bản in / file.'], [287, 295])
S8.add('Mở trực tiếp đường dẫn khi thiếu quyền', 'P0', ACC_N, ['Đăng nhập N.', 'Dán đường dẫn màn báo cáo vào thanh địa chỉ.'], '—',
       ['Bảng "Chọn công ty để xem báo cáo.", không lộ số liệu, không có danh mục vị trí.'], 296)
S8.add('Kho ngoài phạm vi bị chặn', 'P0', ACC_C, ['Đăng nhập C.', MENU, 'Sửa bộ lọc ghi tạm của trình duyệt cho Kho = LN - Liên Ninh (kho công ty TPE), F5.'], '—',
       ['Kho LN bị bỏ, ô Kho trống, không hiện số và danh mục vị trí của kho LN.'], 299)
S8.add('Xem chi tiết, In, Xuất theo cùng quyền xem', 'P1', ACC_K, ['Đăng nhập K.', MENU, 'Bung chi tiết, In, Xuất Excel.'], '—',
       ['Dùng được cả 3 chức năng, chỉ trên kho HP.'], [288, 293])
S8.add('Không có thao tác ghi', 'P1', ACC_T, ['Đăng nhập T.', MENU, CHON_HP], '—',
       ['Không có nút Thêm mới, Sửa, Xóa, Khóa, Import, Lịch sử ở mọi quyền.'], [289, 290, 291, 292, 294])
S8.add('Đổi quyền giữa thao tác', 'P1', [ACC_C, 'Quản trị gỡ quyền "%s" của C khi C đang mở báo cáo kho HP.' % V2], ['C đổi Thương hiệu = ENEOS.'], '—',
       ['Báo "%s"; bảng giữ số cũ, không nạp số mới.' % NOPERM], 298)
S8.add('Có nhiều quyền lấy quyền cao nhất', 'P1', 'Tài khoản M: có cả "%s" và "%s".' % (V2, V3), ['Đăng nhập M.', MENU, 'Mở ô Kho.'], '—',
       ['Ô Kho có mọi kho của công ty M (theo quyền công ty), không chỉ kho M là thủ kho.'], 299)
S8.add('Super admin', 'P2', 'Tài khoản DNS Admin (Super admin), không gán 3 quyền.', ['Đăng nhập DNS Admin.', MENU], '—',
       ['Như quyền tổng công ty: chọn được mọi công ty, mọi kho.'], 287)
S8.add('Quyền theo kho không là thủ kho kho nào', 'P2', 'Tài khoản K2: có quyền "%s", chưa là thủ kho kho nào.' % V3, ['Đăng nhập K2.', MENU], '—',
       ['Ô Kho rỗng; bảng "%s".' % CHONKHO], 299)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'SỐ LIỆU BÁO CÁO', S3),
    ('IV', 'XEM CHI TIẾT THEO HÀNG HÓA – CÔNG TY THUÊ KHO – LÔ', S4),
    ('V', 'XUẤT DANH SÁCH EXCEL', S5),
    ('VI', 'IN BÁO CÁO', S6),
    ('VII', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S7),
    ('VIII', 'PHÂN QUYỀN', S8),
]
for i, (_, _, s) in enumerate(SECTIONS):
    assert s.idx == i + 1, 'Lệch chỉ số section %d' % s.idx
_ids = ['TC_%02d.%s' % (s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
assert len(_ids) == len(set(_ids)), 'Trùng TC ID'

if __name__ == '__main__':
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='Báo cáo tồn kho theo vị trí - Cập nhật ngày 07/11/2026',
                module_name='Báo cáo tồn kho theo vị trí', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='bao_cao')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

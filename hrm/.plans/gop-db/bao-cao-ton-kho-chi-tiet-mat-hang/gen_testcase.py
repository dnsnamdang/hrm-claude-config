# -*- coding: utf-8 -*-
"""Testcase màn "Báo cáo tồn kho chi tiết theo mặt hàng" (phân hệ Kho › Báo cáo kho) — skill testcase-documenter, KHUÔN CHUẨN
03/11/2026 (tc_chuan.build_chuan, loai='bao_cao').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'bao_cao' (đọc code 06/11/2026): màn chỉ đọc, chỉ có API GET (xem / danh mục / in / xuất). Nhóm có mặt: I Hiển thị · II Tìm kiếm
& lọc (gồm Cài đặt bộ lọc, Chọn hàng hóa) · III Số liệu báo cáo (đối soát) · IV Xem chi tiết (bung công ty – lô – vị trí, ĐVT, hợp
đồng) · V Xuất danh sách Excel · VI In báo cáo · VII Ràng buộc · VIII Phân quyền. Không có Tùy chỉnh cột (bảng cố định) → bỏ nhóm.
Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Nguồn hành vi: FE pages/warehouse/stock-detail-by-product/**; BE Modules/Finance StockDetailByProduct* + WarehouseStockReportService.
Số liệu mẫu dev-hrm 06/11/2026 (DNS Admin, _capture/doisoat.js, chỉ đọc): kho HP - Hải Phòng (công ty CN Hải Phòng): 96 mặt hàng,
TPE 1, TPHP 96; hàng ENEO-700-V5231 tồn 20 Xô 18L, 4 lô ở KHOANG1; Thẻ kho 01/01–06/11/2026: tồn đầu 70, nhập 496, xuất 546, tồn cuối 20.
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
MENU = 'Vào phân hệ Kho > menu "Báo cáo kho" > bấm "Báo cáo tồn kho chi tiết theo mặt hàng".'
CN = 'CN HẢI PHÒNG - CÔNG TY CP CÔNG NGHỆ THIẾT BỊ TÂN PHÁT'
CHON_HP = 'Chọn Tồn theo công ty = "%s", Kho = "HP - Hải Phòng".' % CN
V1 = 'Xem báo cáo tồn kho theo tổng công ty'
V2 = 'Xem báo cáo tồn kho theo công ty'
V3 = 'Xem báo cáo tồn kho theo kho'
NOPERM = 'Bạn không có quyền truy cập chức năng này.'
EMPTY = 'Không có mặt hàng nào khớp bộ lọc.'
CHONKHO = 'Chọn kho để xem báo cáo.'
FILE = 'bao_cao_ton_kho_chi_tiet_mat_hang.xlsx'
HANG = 'hàng "Dầu nhớt động cơ Diesel 4 kỳ SAE 20W-50 CF-4 (18L)" (mã ENEO-700-V5231)'
HANG2 = 'hàng "Dầu bôi trơn hộp số tự động tổng hợp Eneos ATF Multi (Chai 1 lít)" (mã ENEO-410-S4136), ĐVT Can 1L và Thùng 24C-1L (x24)'
PRE = ('Tài khoản DNS Admin (Super admin, coi như có quyền "%s").\n'
       'Kho HP - Hải Phòng (công ty %s) tính đến 06/11/2026 có 96 mặt hàng còn tồn; công ty thuê kho TPE có 1 mặt hàng, TPHP có 96.' % (V1, CN))
PRE_H = PRE + '\n%s tại kho HP: công ty TPHP 20 Xô 18L, 4 lô ở vị trí KHOANG1 (2, 6, 6, 6); lô đầu thuộc hợp đồng HĐ_TPHP_HP_KD_26_0183_CD.' % HANG
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
     'Xem tồn của từng mặt hàng tại MỘT kho, tính đến hết một ngày, chi tiết theo công ty thuê kho, lô (kèm hợp đồng của phiếu nhập) '
     'và vị trí. Màn chỉ đọc: không thêm / sửa / xóa; có In (2 kiểu, chọn cột) và Xuất Excel (2 kiểu).'),
    ('2. Đối tượng được tính / hiển thị',
     '- Mặt hàng có tổng tồn các công ty thuê kho đang lọc khác 0 tại kho đã chọn, tính tới hết ngày Tính đến ngày.\n'
     '- Dòng công ty thuê kho: tồn (phần nguyên) > 0 và có lô ghi nhận tại kho.\n'
     '- Dòng lô: lô còn ít nhất 1 vị trí có số lượng > 0; dòng vị trí: vị trí còn số lượng > 0.\n'
     '- Nguồn số: mọi chứng từ kho đã ghi tồn (tồn đầu kỳ, nhập kho, nhập lại, xuất kho, xuất điều chỉnh, điều chuyển kho, nhập / xuất điều chỉnh kiểm kê).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Mặt hàng có tổng tồn = 0; công ty thuê kho tồn <= 0 hoặc không có lô; lô / vị trí đã hết.\n'
     '- Thay đổi tồn sau ngày Tính đến ngày (riêng số lô / vị trí luôn là số mới nhất).\n'
     '- Kho ngoài phạm vi quyền, kho đã ngừng hoạt động, công ty thuê không gắn với kho.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô Tính đến ngày (bắt buộc, mặc định hôm nay): cộng thay đổi tồn tới hết 23:59 ngày đó. Không áp cho số lượng lô / vị trí (giữ như hệ thống cũ).'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Dòng TỔNG > Mặt hàng (I, II…) > Công ty thuê kho (1, 2…) > Lô (1.1…) > Vị trí (1.1.1…). Ô chọn cấp bung: Chỉ hàng hóa / Đến công ty thuê '
     'kho / Đến lô (mặc định) / Tất cả cấp (đến vị trí). Phân trang theo mặt hàng (mặc định 20).'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- SL công ty = tổng thay đổi tồn (nhập cộng, xuất trừ) của công ty đó tại kho.\n- SL mặt hàng = tổng SL các công ty được hiện.\n'
     '- SL lô = tổng SL vị trí của lô.\n- Mỗi mặt hàng 1 dòng; ô theo công ty thuê kho đếm mặt hàng riêng từng công ty (1 hàng có thể nằm ở 2 ô).'),
    ('7. Phân quyền cấp',
     '- %s: chọn mọi công ty, mọi kho (Super admin coi như có quyền này).\n- %s: công ty mình, kho của công ty mình.\n'
     '- %s: công ty mình, chỉ kho mình là thủ kho.\n- Không có quyền nào: không xem được, báo "%s".' % (V1, V2, V3, NOPERM)),
    ('8. Cách tính các ô thống kê',
     '- Ô Mặt hàng còn tồn = dòng TỔNG = N ở "Hiển thị a–b / N mặt hàng".\n- Ô Công ty thuê kho có tồn = số công ty có ít nhất 1 mặt hàng tồn > 0.\n'
     '- Ô từng công ty thuê kho = số mặt hàng công ty đó còn tồn.\n'
     '- Đối soát: Tồn đầu kỳ + Nhập - Xuất (Thẻ kho) = SL tồn dòng công ty cùng hàng / kho / công ty / ngày.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản: DNS Admin (Super admin), T (tổng công ty), C (theo công ty), K (theo kho), N (không quyền).\n'
     '- Lưu ý: số trên màn quy đổi theo ĐVT chọn ở từng hàng và hiện SỐ NGUYÊN; In / Excel luôn theo ĐVT cơ sở.\n'
     '- Lưu ý: chọn ngày quá khứ thì tổng lô có thể khác SL công ty — đúng thiết kế (giữ như hệ thống cũ).\n'
     '- Lưu ý: màn không có ô tìm nhanh và không sắp xếp theo cột; ô Hợp đồng chỉ áp khi Enter / Tìm kiếm.\n'
     '- Lưu ý: kho lớn (Liên Ninh 4.778 mặt hàng) xuất Excel có thể mất vài chục giây; in quá 2.000 dòng bị chặn.'),
]

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', 'Tài khoản DNS Admin, công ty TPE, chưa mở màn trong 10 phút qua.', [MENU], '—',
       ['Mở màn "Báo cáo tồn kho chi tiết theo mặt hàng".', 'Tính đến ngày = hôm nay, Tồn theo công ty = công ty của tài khoản, Kho trống.',
        'Bảng hiện "%s", không báo lỗi.' % CHONKHO], [1, 36])
S1.add('Tiêu đề màn hình', 'P1', PRE, [MENU, 'Quan sát thanh tiêu đề và tab trình duyệt.'], '—',
       ['Cả 2 nơi là "Báo cáo tồn kho chi tiết theo mặt hàng"; khối lọc có tiêu đề "Bộ lọc báo cáo tồn kho".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE, OPEN + ['Quan sát khối lọc và bảng.'], '—',
       ['Đầu khối lọc: In danh sách, Xuất Excel, Cài đặt bộ lọc, Ẩn tìm kiếm nâng cao.', 'Dưới các ô lọc: Tìm kiếm, Xóa lọc.',
        'Dòng tóm tắt có nút Thu gọn; tiêu đề cột đầu có ô chọn cấp bung.', 'KHÔNG có nút Tạo mới, Sửa, Xóa, Import, Lịch sử.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', PRE, OPEN + ['Đọc tiêu đề cột.'], '—',
       ['Đúng 8 cột: STT, Hàng hóa / Công ty / Lô / Vị trí, Mã hàng, Model, Thương hiệu, ĐVT, Hợp đồng, SL tồn.',
        'Cột ĐVT, Hợp đồng, SL tồn có biểu tượng chữ i.'], 4)
S1.add('Không có cột ẩn và không có tùy chỉnh cột', 'P2', PRE, OPEN + ['Tìm nút cấu hình cột trên bảng.'], '—',
       ['Không có nút cấu hình cột; bảng luôn đủ 8 cột.'], 5)
S1.add('Dữ liệu dòng mặt hàng khớp danh mục hàng', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231 ở ô Hàng hóa.'], 'Hàng hóa: ENEO-700-V5231',
       ['Dòng I: tên "Dầu nhớt động cơ Diesel 4 kỳ SAE 20W-50 CF-4 (18L)", Mã hàng ENEO-700-V5231, Model "CF4 20W50 18L", Thương hiệu ENEOS, '
        'ĐVT "Xô 18L", SL tồn 20.'], 6)
S1.add('Mặt hàng tồn bằng 0 không hiện', 'P0', [PRE, 'Hàng X đã xuất hết tại kho HP (tổng nhập = tổng xuất).'],
       OPEN + ['Chọn hàng X ở ô Hàng hóa.'], 'Hàng hóa: X',
       ['Bảng hiện "%s"; dòng báo cáo không có trạng thái Khóa / Hoạt động.' % EMPTY], 7)
S1.add('Kho chưa có hàng tồn', 'P1', 'Tài khoản DNS Admin; kho "DATD - Kho Dự án trọng điểm" (công ty TPE) không còn mặt hàng tồn.',
       [MENU, 'Chọn Tồn theo công ty = công ty TPE, Kho = "DATD - Kho Dự án trọng điểm".'], 'Kho: DATD',
       ['Khối tổng hợp: Mặt hàng còn tồn 0; bảng hiện "%s"; ẩn phân trang; không báo lỗi.' % EMPTY], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE, OPEN + ['Gõ "ZZZ999" vào ô Hợp đồng, nhấn Enter.'], 'Hợp đồng: ZZZ999',
       ['Bảng hiện "%s"; khối tổng hợp Mặt hàng còn tồn 0.' % EMPTY], [9, 40])
S1.add('Số mặt hàng mặc định mỗi trang', 'P0', PRE, OPEN, '—',
       ['Trang 1 có 20 mặt hàng (I đến XX); dưới bảng "Hiển thị 1–20 / 96 mặt hàng"; Số dòng/trang = 20.'], [10, 16])
S1.add('Thay đổi số dòng / trang', 'P0', PRE, OPEN + ['Sang trang 2.', 'Đổi Số dòng/trang thành 50.'], 'Số dòng/trang: 50',
       ['Bảng hiện 50 mặt hàng, về trang 1, "Hiển thị 1–50 / 96 mặt hàng".', 'Lựa chọn có 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P1', PRE, OPEN + ['Bấm ›.', 'Bấm ‹.'], '—',
       ['Bấm › sang trang 2: "Hiển thị 21–40 / 96", STT từ XXI.', 'Bấm ‹ về trang 1.'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE, OPEN + ['Bấm ».', 'Bấm «.'], '—',
       ['Bấm » tới trang 5: "Hiển thị 81–96 / 96 mặt hàng".', 'Bấm « về trang 1.'], 13)
S1.add('Trạng thái nút ở trang đầu / cuối', 'P2', PRE, OPEN + ['Quan sát nút ở trang 1, rồi ở trang 5.'], '—',
       ['Trang 1: nút « ‹ mờ, không bấm được.', 'Trang 5: nút › » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P1', PRE, OPEN + ['Sang trang 2.'], '—',
       ['Mặt hàng đầu trang 2 có STT XXI (La Mã nối tiếp trang 1); dòng con đánh 1, 1.1, 1.1.1 trong từng mặt hàng.'], 15)
S1.add('Về trang 1 khi đổi bộ lọc', 'P1', PRE, OPEN + ['Sang trang 3.', 'Chọn Thương hiệu = ENEOS.'], 'Thương hiệu: ENEOS',
       ['Báo cáo nạp lại từ trang 1; tổng N cập nhật theo bộ lọc.'], [17, 42])
S1.add('Thứ tự mặc định theo tên hàng', 'P0', PRE, OPEN, '—',
       ['Mặt hàng xếp theo tên A đến Z: I Áo khoác ENEOS, II Áo mưa ENEOS, III Áo phông cao cấp ENEOS…'], 19)
S1.add('Không sắp xếp theo cột', 'P2', PRE, OPEN + ['Bấm tiêu đề cột Mã hàng, SL tồn.'], '—',
       ['Thứ tự không đổi (luôn theo tên hàng); tiêu đề cột không có biểu tượng sắp xếp.'], [20, 21, 22, 23])
S1.add('Giữ thứ tự khi chuyển trang', 'P2', PRE, OPEN + ['Sang trang 2, quay lại trang 1.'], '—',
       ['Trang 2 tiếp tục thứ tự tên hàng; quay lại trang 1 đúng 20 mặt hàng như lúc đầu.'], 24)
S1.add('Thu gọn / mở rộng khối tổng hợp', 'P2', PRE, OPEN + ['Bấm Thu gọn.', 'Bấm Mở rộng.'], '—',
       ['Thu gọn: ẩn các ô Mặt hàng, Theo công ty thuê kho, còn dòng tóm tắt; chữ nút "Mở rộng".', 'Mở rộng: hiện lại, số không đổi.'], 3)
S1.add('Dòng tóm tắt báo cáo', 'P1', PRE, OPEN + ['Rê chuột vào chữ i cạnh dòng tóm tắt.'], '—',
       ['Dòng "Tồn kho tính đến ngày 06/11/2026 · Kho: HP - Hải Phòng".',
        'Chữ i hiện "BÁO CÁO TỒN KHO CHI TIẾT THEO MẶT HÀNG", 3 dòng giải thích, dòng cuối "Số liệu tính tại <ngày giờ>".'], 6)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Hợp đồng: khớp chính xác mã', 'P0', PRE_H, OPEN + ['Gõ "HĐ_TPHP_HP_KD_26_0183_CD" vào ô Hợp đồng, nhấn Enter.'],
       'Hợp đồng: HĐ_TPHP_HP_KD_26_0183_CD',
       ['Chỉ còn mặt hàng có lô thuộc hợp đồng này, trong đó có ENEO-700-V5231.', 'Dòng lô chỉ còn lô của hợp đồng đó.'], 26)
S2.add('Hợp đồng: khớp một phần mã', 'P0', PRE_H, OPEN + ['Gõ "26_0183" vào ô Hợp đồng, nhấn Enter.'], 'Hợp đồng: 26_0183',
       ['Kết quả như khi gõ đủ mã (khớp một phần).'], 27)
S2.add('Hợp đồng: không phân biệt hoa / thường', 'P1', PRE_H, OPEN + ['Gõ "hđ_tphp_hp_kd_26_0183" vào ô Hợp đồng, nhấn Enter.'],
       'Hợp đồng: hđ_tphp_hp_kd_26_0183', ['Kết quả như khi gõ chữ hoa.'], 28)
S2.add('Hợp đồng: chữ Đ và D khác nhau', 'P2', PRE_H, OPEN + ['Gõ "HD_TPHP_HP_KD_26_0183" (chữ D không gạch), nhấn Enter.'],
       'Hợp đồng: HD_TPHP_HP_KD_26_0183', ['Bảng hiện "%s" — hệ thống phân biệt Đ và D.' % EMPTY], 29)
S2.add('Hợp đồng: mã không tồn tại', 'P1', PRE, OPEN + ['Gõ "KHONGCO-123", nhấn Enter.'], 'Hợp đồng: KHONGCO-123', ['Bảng hiện "%s".' % EMPTY], 30)
S2.add('Hợp đồng: ký tự đặc biệt', 'P2', PRE, OPEN + ['Gõ "%", nhấn Enter.', 'Gõ "<script>", nhấn Enter.'], ['Hợp đồng: %', 'Hợp đồng: <script>'],
       ['Gõ "%": ra mọi mặt hàng có lô thuộc bất kỳ hợp đồng nào (ký tự % được hiểu là "bất kỳ").',
        'Gõ "<script>": bảng rỗng, không lỗi, không chạy mã.'], 31)
S2.add('Hợp đồng: khoảng trắng đầu / cuối', 'P1', PRE_H, OPEN + ['Gõ "  26_0183  ", nhấn Enter.'], 'Hợp đồng: "  26_0183  "',
       ['Kết quả như gõ "26_0183" (tự bỏ khoảng trắng đầu / cuối).'], 32)
S2.add('Hợp đồng: không giới hạn ký tự', 'P2', PRE, OPEN + ['Gõ chuỗi 300 ký tự "A", nhấn Enter.'], 'Hợp đồng: 300 ký tự',
       ['Ô nhận đủ, không báo lỗi; bảng hiện "%s".' % EMPTY], 33)
S2.add('Xóa chữ ở ô Hợp đồng', 'P1', [PRE, 'Đang lọc Hợp đồng = 26_0183.'], OPEN + ['Xóa hết chữ ô Hợp đồng, nhấn Enter.'], '—',
       ['Báo cáo trở lại 96 mặt hàng.'], 34)
S2.add('Hợp đồng chỉ áp khi Enter hoặc Tìm kiếm', 'P0', PRE_H, OPEN + ['Gõ "26_0183" nhưng không nhấn Enter.', 'Bấm Tìm kiếm.'], 'Hợp đồng: 26_0183',
       ['Sau bước 2 bảng chưa đổi.', 'Sau bước 3 báo cáo lọc theo hợp đồng, về trang 1.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P0', 'Tài khoản DNS Admin công ty TPE, chưa mở màn trong 10 phút.', [MENU], '—',
       ['Tính đến ngày = hôm nay; Tồn theo công ty = công ty TPE; Kho, Công ty thuê kho, Nhóm, Tính chất, Loại, Thương hiệu, Hãng sản xuất, '
        'Hàng hóa, Hợp đồng trống; khối lọc mở sẵn.'], 36)
S2.add('Thiếu Kho thì báo đỏ', 'P0', 'Tài khoản DNS Admin, công ty TPE (nhiều kho).', [MENU, 'Bấm Tìm kiếm.'], '—',
       ['Ô Kho viền đỏ, chữ "Vui lòng chọn kho"; không nạp báo cáo; bảng "%s".' % CHONKHO], [36, 37])
S2.add('Thiếu Tính đến ngày thì báo đỏ', 'P1', PRE, OPEN + ['Xóa ngày ở Tính đến ngày.', 'Bấm Tìm kiếm.'], '—',
       ['Ô Tính đến ngày chữ đỏ "Vui lòng chọn ngày"; bảng "Chọn ngày để xem báo cáo.".'], 37)
S2.add('Lọc Tính đến ngày quá khứ', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231.', 'Đổi Tính đến ngày = 31/12/2025.'],
       'Tính đến ngày: 31/12/2025', ['SL tồn dòng công ty TPHP = 70; dòng tóm tắt "Tồn kho tính đến ngày 31/12/2025".'], 37)
S2.add('Đổi Tồn theo công ty thì bỏ kho', 'P1', PRE, OPEN + ['Đổi Tồn theo công ty sang công ty TPE.'], '—',
       ['Ô Kho về trống, Công ty thuê kho trống, bảng "%s".' % CHONKHO, 'Ô Kho chỉ còn kho của công ty TPE.'], 37)
S2.add('Đổi Kho tự chọn công ty thuê kho', 'P0', PRE, [MENU, 'Chọn Tồn theo công ty = %s.' % CN, 'Chọn Kho = HP - Hải Phòng.'], 'Kho: HP',
       ['Ô Công ty thuê kho tự tích TPE và TPHP; báo cáo nạp ngay.'], 37)
S2.add('Lọc Công ty thuê kho', 'P0', PRE, OPEN + ['Bỏ TPHP ở Công ty thuê kho (còn TPE).'], 'Công ty thuê kho: TPE',
       ['Còn 1 mặt hàng; khối Theo công ty thuê kho chỉ còn ô TPE 1 mặt hàng.'], 37)
S2.add('Lọc Nhóm, Tính chất, Loại, Hãng sản xuất', 'P1', PRE, OPEN + ['Lần lượt chọn 1 giá trị ở từng ô, sau mỗi ô bỏ chọn.'], '—',
       ['Mỗi lần chỉ còn mặt hàng thuộc giá trị đã chọn; bỏ chọn trở lại 96.', 'Loại hàng hóa: hàng thuộc ít nhất 1 loại đã chọn.'], 37)
S2.add('Lọc Thương hiệu', 'P1', PRE, OPEN + ['Chọn Thương hiệu = ENEOS.'], 'Thương hiệu: ENEOS', ['Mọi dòng mặt hàng có Thương hiệu ENEOS.'], 37)
S2.add('Kết hợp nhiều ô lọc', 'P0', PRE_H, OPEN + ['Chọn Thương hiệu = ENEOS.', 'Gõ "26_0183" ở Hợp đồng, Enter.'], ['Thương hiệu: ENEOS', 'Hợp đồng: 26_0183'],
       ['Chỉ còn mặt hàng thỏa CẢ 2 điều kiện; có ENEO-700-V5231.'], [38, 39])
S2.add('Tổng và phân trang sau lọc', 'P1', PRE, OPEN + ['Chọn Thương hiệu = ENEOS.'], 'Thương hiệu: ENEOS',
       ['Ô Mặt hàng còn tồn = dòng TỔNG = N ở "Hiển thị 1–x / N"; số trang tính lại theo N.'], [41, 42])
S2.add('Thứ tự sau lọc', 'P2', PRE, OPEN + ['Chọn Thương hiệu = ENEOS.'], '—', ['Kết quả vẫn xếp theo tên hàng A đến Z.'], 43)
S2.add('Xóa lọc', 'P0', [PRE, 'Đang lọc kho HP, Thương hiệu ENEOS, Hợp đồng 26_0183.'], OPEN + ['Bấm Xóa lọc.'], '—',
       ['Tính đến ngày về hôm nay, Tồn theo công ty về công ty của tài khoản, các ô khác trống (kể cả Kho, Hàng hóa).',
        'Bảng "%s"; chữ đỏ biến mất.' % CHONKHO], 44)
S2.add('Chuyển màn rồi quay lại', 'P1', [PRE, 'Đang lọc kho HP.'], OPEN + ['Mở màn Thẻ kho.', MENU], '—',
       ['Bộ lọc về mặc định (kho trống).'], 45)
S2.add('Tải lại trang (F5)', 'P0', [PRE, 'Đang lọc kho HP, hàng ENEO-700-V5231.'], OPEN + ['Nhấn F5 trong vòng 10 phút.'], '—',
       ['Giữ nguyên kho HP, ô Hàng hóa vẫn hiện "ENEO-700-V5231 - Dầu nhớt…", báo cáo nạp lại.', 'Sau hơn 10 phút F5: bộ lọc về mặc định.'], 46)
S2.add('Mở tab mới', 'P2', [PRE, 'Đang lọc kho HP.'], OPEN + ['Mở màn ở tab mới trong 10 phút.'], '—', ['Tab mới khôi phục bộ lọc kho HP.'], 47)
S2.add('Tài khoản khác cùng trình duyệt', 'P2', [PRE, ACC_C, 'DNS Admin vừa lọc kho HP rồi đăng xuất (trong 10 phút).'],
       ['Đăng nhập C trên cùng trình duyệt.', MENU], '—',
       ['Nếu bộ lọc ghi tạm còn hạn, C thấy kho HP được chọn sẵn (kho HP thuộc công ty C); kho / công ty ngoài phạm vi của C bị bỏ.'], 48)
S2.add('Cài đặt bộ lọc: mở cửa sổ', 'P1', PRE, OPEN + ['Bấm Cài đặt bộ lọc.'], '—',
       ['Cửa sổ "Cài đặt bộ lọc" liệt kê 11 ô lọc có ô tích, nút Lưu, Khôi phục mặc định, Đóng.'], 37)
S2.add('Cài đặt bộ lọc: ẩn ô và lưu', 'P1', PRE, OPEN + ['Bấm Cài đặt bộ lọc.', 'Bỏ tích Hãng sản xuất.', 'Bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công"; khối lọc không còn ô Hãng sản xuất; F5 vẫn ẩn.'], 37)
S2.add('Cài đặt bộ lọc: đổi thứ tự, khôi phục, đóng', 'P2', PRE,
       OPEN + ['Bấm Cài đặt bộ lọc.', 'Kéo Hợp đồng lên đầu, bấm Đóng.', 'Mở lại, bấm Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bấm Đóng: thứ tự không đổi.', 'Khôi phục + Lưu: đủ 11 ô theo thứ tự gốc.'], 37)
S2.add('Chọn hàng hóa: mở cửa sổ', 'P0', 'Tài khoản DNS Admin, công ty TPE, kho LN - Liên Ninh.',
       [MENU, 'Chọn Kho = LN - Liên Ninh.', 'Bấm ô Hàng hóa.'], '—',
       ['Mở cửa sổ "Chọn hàng hóa": dòng công ty TPE, cây catalog, ô tìm, công tắc Còn tồn / Gồm hàng ngoài catalog, bảng hàng, nút Đóng.',
        'Chân cửa sổ ghi "Bấm vào tên hàng để chọn".'], 37)
S2.add('Chọn hàng hóa: chọn 1 hàng', 'P0', PRE_H, OPEN + ['Bấm ô Hàng hóa.', 'Tìm "ENEO-700-V5231", bấm tên hàng.'], 'Hàng hóa: ENEO-700-V5231',
       ['Cửa sổ đóng; ô Hàng hóa "ENEO-700-V5231 - Dầu nhớt động cơ…"; báo cáo còn 1 mặt hàng (nạp 1 lần).'], 37)
S2.add('Chọn hàng hóa: bỏ chọn bằng dấu ×', 'P1', [PRE_H, 'Đang chọn hàng ENEO-700-V5231.'], OPEN + ['Bấm dấu × trên ô Hàng hóa.'], '—',
       ['Ô Hàng hóa trống, cửa sổ không mở; báo cáo trở lại 96 mặt hàng.'], [34, 37])
S2.add('Chọn hàng hóa: đóng không chọn', 'P2', PRE, OPEN + ['Bấm ô Hàng hóa.', 'Bấm Đóng.'], '—', ['Cửa sổ đóng, bộ lọc không đổi.'], 37)
S2.add('Chọn hàng hóa với công ty khác công ty đăng nhập', 'P1', 'Tài khoản DNS Admin đăng nhập công ty TPE.',
       OPEN + ['Bấm ô Hàng hóa.'], '—',
       ['Cửa sổ ghi "Công ty %s".' % CN, 'Danh sách hàng tải được, không báo "Không tải được danh sách hàng hoá"; chọn được hàng.'], 37)

# ============================================================== III. SỐ LIỆU BÁO CÁO
S3 = Sec(3)
S3.add('Khối tổng hợp', 'P0', PRE, OPEN, '—',
       ['Ô Mặt hàng còn tồn 96 mặt hàng; ô Công ty thuê kho có tồn 2 công ty.', 'Khối Theo công ty thuê kho: TPE 1 mặt hàng, TPHP 96 mặt hàng.'], 6)
S3.add('Dòng TỔNG khớp khối tổng hợp và tổng số', 'P0', PRE, OPEN + ['Sang trang 2.'], '—',
       ['Dòng TỔNG "MẶT HÀNG CÒN TỒN 96 mặt hàng" = ô Mặt hàng còn tồn = N ở "Hiển thị … / 96".',
        'Sang trang 2 dòng TỔNG và khối tổng hợp không đổi; dòng TỔNG không có số lượng.'], [16, 41])
S3.add('Ô Công ty thuê kho có tồn ẩn khi bằng 0', 'P2', 'Tài khoản DNS Admin; kho DATD không còn tồn.',
       [MENU, 'Chọn công ty TPE, Kho = DATD.'], '—', ['Chỉ còn ô Mặt hàng còn tồn 0; không có khối Theo công ty thuê kho.'], 8)
S3.add('Đối soát tồn đầu + nhập - xuất = tồn cuối với Thẻ kho', 'P0',
       [PRE_H, 'Thẻ kho của hàng tại kho HP, công ty thuê TPHP, kỳ 01/01/2026–06/11/2026: Tồn đầu kỳ 70, Nhập 496, Xuất 546, Tồn cuối kỳ 20.'],
       ['Mở Thẻ kho, chọn hàng ENEO-700-V5231, kho HP, công ty thuê TPHP, kỳ từ 01/01/2026 đến 06/11/2026; ghi Tồn đầu, Nhập, Xuất, Tồn cuối.',
        MENU, CHON_HP, 'Chọn hàng ENEO-700-V5231, Tính đến ngày 06/11/2026.'], 'Tính đến ngày: 06/11/2026',
       ['70 + 496 - 546 = 20 = SL tồn dòng công ty TPHP của báo cáo này.', 'SL tồn dòng mặt hàng = 20.'], 6)
S3.add('Đối soát tồn đầu kỳ với ngày quá khứ', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231, Tính đến ngày 31/12/2025.'], 'Tính đến ngày: 31/12/2025',
       ['SL tồn dòng công ty TPHP = 70 = Tồn đầu kỳ của Thẻ kho kỳ bắt đầu 01/01/2026.'], 6)
S3.add('Đối soát với Báo cáo tồn kho tổng hợp theo mặt hàng', 'P0', PRE_H,
       ['Mở Báo cáo tồn kho tổng hợp theo mặt hàng, chọn công ty %s, chỉ kho HP, cùng ngày 06/11/2026.' % CN, 'Ghi SL tồn ENEO-700-V5231 và tổng số mặt hàng.',
        MENU, CHON_HP], '—',
       ['SL tồn ENEO-700-V5231 bằng nhau (20) ở 2 báo cáo.', 'Tổng số mặt hàng bằng nhau (96).'], 6)
S3.add('Lập chứng từ nhập thì số tăng', 'P0', [PRE_H, 'Lập và hoàn tất 1 Phiếu nhập kho 5 Xô 18L hàng ENEO-700-V5231 vào kho HP, công ty TPHP, vị trí KHOANG1 (môi trường kiểm thử).'],
       OPEN + ['Chọn hàng ENEO-700-V5231, Tính đến ngày hôm nay.'], '—',
       ['SL tồn dòng TPHP và dòng mặt hàng tăng 5 (20 thành 25); có thêm dòng lô mới ở KHOANG1 SL 5.',
        'Chọn Tính đến ngày = hôm qua: SL công ty vẫn 20.'], [274, 281])
S3.add('Lập chứng từ xuất thì số giảm', 'P0', [PRE_H, 'Hoàn tất 1 Phiếu xuất kho 2 Xô 18L hàng ENEO-700-V5231 từ kho HP, lô đầu (môi trường kiểm thử).'],
       OPEN + ['Chọn hàng ENEO-700-V5231.'], '—',
       ['SL tồn dòng TPHP và mặt hàng giảm 2; lô đầu hết số lượng thì dòng lô biến mất.'], [274, 281])
S3.add('Dòng mặt hàng bằng tổng các công ty', 'P0', [PRE, 'Kho LN - Liên Ninh: hàng có tồn ở cả TPE và TPSG.'],
       [MENU, 'Chọn công ty TPE, Kho = LN - Liên Ninh.', 'Tìm 1 mặt hàng có 2 dòng công ty.'], '—',
       ['SL tồn dòng mặt hàng = tổng SL tồn các dòng công ty bên dưới.'], 283)
S3.add('Dòng lô bằng tổng các vị trí', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231, chọn cấp "Tất cả cấp (đến vị trí)".'], '—',
       ['Mỗi dòng lô = tổng các dòng vị trí của nó (2, 6, 6, 6); tổng các lô = 20 = dòng công ty (ngày hôm nay).'], 283)
S3.add('Số lô / vị trí không cắt theo ngày', 'P1', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231, Tính đến ngày 31/12/2025, chọn cấp "Tất cả cấp".'], '—',
       ['Dòng công ty TPHP = 70 nhưng các lô / vị trí vẫn là số hiện tại (tổng lô có thể khác 70) — đúng thiết kế, giữ như hệ thống cũ.'], 6)
S3.add('Định dạng số', 'P1', [PRE, 'Kho LN có mặt hàng tồn trên 1.000.'], [MENU, 'Chọn công ty TPE, Kho = LN - Liên Ninh.'], '—',
       ['SL tồn căn phải, phân cách hàng nghìn bằng dấu phẩy (vd 1,232), số nguyên.'], 6)
S3.add('Một hàng nằm ở 2 công ty thuê kho', 'P1', [PRE, 'Kho LN: TPE 4.690 mặt hàng, TPSG 340, TPV 62; tổng 4.778.'],
       [MENU, 'Chọn công ty TPE, Kho = LN - Liên Ninh.'], '—',
       ['Ô TPE 4,690, TPSG 340, TPV 62; ô Mặt hàng còn tồn 4,778 (nhỏ hơn tổng 3 ô vì 1 hàng có thể ở nhiều công ty).'], 286)

# ============================================================== IV. XEM CHI TIẾT
S4 = Sec(4)
S4.add('Bung chi tiết mặc định tới lô', 'P0', PRE, OPEN, '—',
       ['Mặc định ô chọn cấp "Đến lô": mỗi mặt hàng bung dòng công ty và dòng lô, chưa hiện vị trí.'], 186)
S4.add('Tiêu đề cột và ô chọn cấp', 'P1', PRE, OPEN + ['Mở ô chọn cấp.'], '—',
       ['Cột đầu "Hàng hóa / Công ty / Lô / Vị trí"; ô chọn cấp có 4 lựa chọn: Chỉ hàng hóa, Đến công ty thuê kho, Đến lô, Tất cả cấp (đến vị trí).'], 187)
S4.add('Chọn cấp Tất cả cấp', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231.', 'Chọn cấp "Tất cả cấp (đến vị trí)".'], '—',
       ['Hiện: I mặt hàng 20 > 1 TPHP 20 > 1.1 lô TPHP-27/05/2026-… 2 > 1.1.1 KHOANG1 2; 1.2, 1.3, 1.4 mỗi lô 6 ở KHOANG1.'], [188, 189])
S4.add('Chọn cấp Chỉ hàng hóa và Đến công ty', 'P1', PRE, OPEN + ['Chọn cấp "Chỉ hàng hóa".', 'Chọn cấp "Đến công ty thuê kho".'], '—',
       ['Chỉ hàng hóa: chỉ dòng mặt hàng.', 'Đến công ty: thêm dòng công ty, chưa có lô.'], 186)
S4.add('Bung / thu riêng một dòng', 'P1', PRE, OPEN + ['Bấm mũi tên ở dòng mặt hàng I.', 'Bấm lại.'], '—',
       ['Lần 1 thu dòng con của mặt hàng I, các mặt hàng khác giữ nguyên; lần 2 bung lại.', 'Rê chuột mũi tên: "Ẩn / Hiện công ty thuê kho".'], 196)
S4.add('Dữ liệu chi tiết khớp danh sách', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231, cấp "Tất cả cấp".'], '—',
       ['Tổng vị trí của mỗi lô = SL lô; tổng lô = SL công ty = SL mặt hàng = 20.'], 190)
S4.add('Chi tiết chỉ đọc', 'P1', PRE, OPEN + ['Bấm vào tên hàng, mã lô, SL.'], '—',
       ['Không có ô nhập, không có nút Lưu / Sửa / Xóa; bấm chữ không mở màn khác.'], [191, 192, 193])
S4.add('Công ty không còn lô có tồn theo vị trí', 'P2', [PRE, 'Một công ty thuê có tồn > 0 nhưng mọi vị trí của các lô đã về 0.'], OPEN, '—',
       ['Dòng công ty không có mũi tên, kèm chữ xám "Không còn lô có tồn theo vị trí".'], 193)
S4.add('Đổi ĐVT trên dòng mặt hàng', 'P0', [PRE, '%s tồn 24 Can 1L tại kho HP.' % HANG2],
       OPEN + ['Tìm dòng ENEO-410-S4136.', 'Ở cột ĐVT chọn "Thùng 24C-1L (x24)".'], 'ĐVT: Thùng 24C-1L (x24)',
       ['SL tồn của hàng (mặt hàng, công ty, lô) đổi thành 1.', 'Các mặt hàng khác không đổi.'], 189)
S4.add('Quy đổi làm tròn số nguyên', 'P1', [PRE, 'Hàng Y tồn 13 Cái, có ĐVT Thùng x12.'], OPEN + ['Ở dòng Y chọn ĐVT Thùng.'], 'ĐVT: Thùng (x12)',
       ['SL hiện "1" (13 ÷ 12 = 1,08 làm tròn số nguyên).'], 189)
S4.add('Hàng 1 ĐVT không có ô chọn', 'P2', PRE, OPEN, '—', ['Dòng Áo khoác ENEOS cột ĐVT hiện chữ "Cái.", không có ô chọn.'], 191)
S4.add('Mở hợp đồng của lô', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231.', 'Bấm mã "HĐ_TPHP_HP_KD_26_0183_CD" ở dòng lô 1.1.'], '—',
       ['Mở tab mới xem hợp đồng ở hệ thống cũ; tab báo cáo giữ nguyên.', 'Rê chuột lên mã: hiện "Hợp đồng: HĐ_TPHP_HP_KD_26_0183_CD".'], 186)
S4.add('Giữ trang và bộ lọc khi quay lại', 'P1', [PRE, 'Đang ở trang 3, lọc Thương hiệu ENEOS.'], OPEN + ['Bấm mã hợp đồng mở tab mới, đóng tab đó.'], '—',
       ['Tab báo cáo vẫn ở trang 3, giữ bộ lọc và cấp bung.'], 197)
S4.add('Đổi trang áp lại cấp bung', 'P2', PRE, OPEN + ['Thu riêng mặt hàng I.', 'Sang trang 2 rồi về trang 1.'], '—',
       ['Mặt hàng I bung lại theo cấp đang chọn (bung / thu riêng lẻ bị bỏ).'], 196)

# ============================================================== V. XUẤT DANH SÁCH EXCEL
S5 = Sec(5)
S5.add('Mở cửa sổ xuất Excel', 'P0', PRE, OPEN + ['Bấm Xuất Excel ở đầu khối lọc.'], '—',
       ['Mở cửa sổ "Xuất Excel báo cáo tồn kho chi tiết theo mặt hàng", Kiểu xuất có Đầy đủ (chọn sẵn) và Ngắn gọn, nút Xuất Excel, Hủy.'], [212, 213, 214])
S5.add('Xuất kiểu Đầy đủ', 'P0', PRE, OPEN + ['Bấm Xuất Excel.', 'Giữ Đầy đủ, bấm Xuất Excel trong cửa sổ.'], 'Kiểu xuất: Đầy đủ',
       ['Tải file "%s"; cửa sổ đóng.' % FILE,
        'Cột: STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn, nhóm Chi tiết (Công ty, Lô, Vị trí, SL, Cộng).'], [215, 216, 223, 225])
S5.add('Xuất kiểu Ngắn gọn', 'P0', PRE, OPEN + ['Bấm Xuất Excel.', 'Chọn Ngắn gọn, bấm Xuất Excel.'], 'Kiểu xuất: Ngắn gọn',
       ['File chỉ có STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn.'], [217, 226])
S5.add('Không có bước chọn trường', 'P2', PRE, OPEN + ['Bấm Xuất Excel.'], '—', ['Cửa sổ không có danh sách chọn cột; luôn xuất đủ cột của kiểu.'], 218)
S5.add('Xuất theo bộ lọc', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231.', 'Xuất Excel kiểu Đầy đủ.'], '—',
       ['File chỉ có 1 mặt hàng, 4 dòng chi tiết lô / vị trí KHOANG1; Cộng 20.'], [219, 220])
S5.add('Xuất mọi trang', 'P0', PRE, OPEN + ['Đang ở trang 1 (20 mặt hàng), xuất kiểu Ngắn gọn.'], '—',
       ['File có đủ 96 mặt hàng (không riêng trang đang xem).'], [221, 227])
S5.add('Xuất khi báo cáo rỗng', 'P1', 'Tài khoản DNS Admin; kho DATD không còn tồn.', [MENU, 'Chọn công ty TPE, Kho = DATD.', 'Xuất Excel kiểu Đầy đủ.'], '—',
       ['Vẫn tải file, chỉ có letterhead, tiêu đề, Tính đến ngày, Kho, hàng tên cột, khối ký.'], 222)
S5.add('Chưa chọn kho thì không xuất', 'P1', 'Tài khoản DNS Admin, công ty TPE.', [MENU, 'Bấm Xuất Excel.'], '—',
       ['Không mở cửa sổ; ô Kho chữ đỏ "Vui lòng chọn kho".'], 222)
S5.add('Định dạng file', 'P1', PRE, OPEN + ['Xuất kiểu Đầy đủ, mở file.'], '—',
       ['File .xlsx mở được; dòng 1 letterhead công ty CN Hải Phòng; tiêu đề "BÁO CÁO TỒN KHO CHI TIẾT THEO MẶT HÀNG"; "Tính đến ngày: 06/11/2026"; "Kho: HP - Hải Phòng".',
        'Cuối file khối ký Trưởng kho, Người lập báo cáo kèm ngày.'], 224)
S5.add('Dữ liệu khớp màn hình', 'P0', PRE_H, OPEN + ['Xuất kiểu Đầy đủ, tìm ENEO-700-V5231 trong file.'], '—',
       ['Tên, Model, Mã, Thương hiệu, ĐVT "Xô 18L", SL tồn 20 khớp màn; Lô ghi kèm "Hợp đồng: HĐ_TPHP_HP_KD_26_0183_CD".'], 228)
S5.add('Số là ô số, theo ĐVT cơ sở', 'P1', [PRE, '%s; trên màn đang chọn ĐVT Thùng.' % HANG2], OPEN + ['Xuất kiểu Ngắn gọn, mở file.'], '—',
       ['SL tồn hàng ENEO-410-S4136 trong file = 24 (ĐVT cơ sở), ĐVT "Can 1L".', 'Ô số có phân cách hàng nghìn, cộng SUM được; số 0 để trống.'], 229)
S5.add('Tiếng Việt và ký tự đặc biệt', 'P2', PRE, OPEN + ['Xuất, mở file.'], '—',
       ['Tên hàng có dấu, ký tự "(", "/", "-" hiển thị đúng, không lỗi phông.'], 230)
S5.add('Hủy xuất', 'P2', PRE, OPEN + ['Bấm Xuất Excel.', 'Bấm Hủy.'], '—', ['Cửa sổ đóng, không tải file; mở lại kiểu về Đầy đủ.'], 212)
S5.add('Đang xuất thì khóa nút', 'P1', [PRE, 'Kho LN - Liên Ninh 4.778 mặt hàng.'], [MENU, 'Chọn công ty TPE, Kho LN.', 'Xuất Excel kiểu Đầy đủ, bấm liên tục 2 lần.'], '—',
       ['Nút đổi chữ "Đang xuất…", có vòng xoay, không nhận lần bấm thứ 2; chỉ tải 1 file.'], 221)

# ============================================================== VI. IN BÁO CÁO
S6 = Sec(6)
S6.add('Mở cửa sổ In báo cáo', 'P0', PRE, OPEN + ['Bấm In danh sách.'], '—',
       ['Cửa sổ "In báo cáo": kiểu Đầy đủ chọn sẵn, Ngắn gọn; "Chọn cột in" tích sẵn 11 cột; nút In, Hủy.'], 212)
S6.add('Đổi kiểu in đổi danh sách cột', 'P1', PRE, OPEN + ['Bấm In danh sách.', 'Chọn Ngắn gọn.'], '—',
       ['Danh sách cột còn 6: Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn.'], 213)
S6.add('Bỏ hết cột thì báo lỗi', 'P0', PRE, OPEN + ['Bấm In danh sách.', 'Bỏ tích Chọn tất cả.', 'Bấm In.'], '—',
       ['Chữ đỏ "Vui lòng chọn ít nhất 1 cột để in"; cửa sổ không đóng.'], 218)
S6.add('Xem trước bản in kiểu Đầy đủ', 'P0', PRE, OPEN + ['Bấm In danh sách, bấm In.'], '—',
       ['Mở "Xem trước báo cáo tồn kho chi tiết theo mặt hàng" khổ ngang: letterhead CN Hải Phòng, tiêu đề, Tính đến ngày, Kho, bảng 96 mặt hàng gộp ô theo hàng / công ty / lô, khối ký Trưởng kho, Người lập báo cáo.'], [219, 221])
S6.add('In theo cột đã chọn', 'P1', PRE, OPEN + ['Bấm In danh sách.', 'Bỏ tích Model và Thương hiệu, bấm In.'], '—',
       ['Bản xem trước không có cột Model, Thương hiệu; cột STT luôn có.'], 217)
S6.add('Bấm In trên bản xem trước', 'P1', PRE, OPEN + ['Mở xem trước, bấm In.'], '—', ['Hộp thoại in của trình duyệt mở, nội dung đúng bản xem trước.'], 219)
S6.add('Vượt mức in tối đa', 'P1', [PRE, 'Kho LN kiểu Đầy đủ có hơn 2.000 dòng in.'], [MENU, 'Chọn công ty TPE, Kho LN.', 'Bấm In danh sách, giữ Đầy đủ, bấm In.'], '—',
       ['Bản xem trước không có nội dung, hiện "Danh sách có … dòng, vượt mức in tối đa 2.000 dòng nên chưa in được…"; nút In ẩn.'], 221)
S6.add('Chưa chọn kho thì không in', 'P1', 'Tài khoản DNS Admin, công ty TPE.', [MENU, 'Bấm In danh sách.'], '—',
       ['Không mở cửa sổ; ô Kho chữ đỏ "Vui lòng chọn kho".'], 222)
S6.add('Số in theo ĐVT cơ sở', 'P2', [PRE, '%s; trên màn đang chọn ĐVT Thùng.' % HANG2], OPEN + ['In kiểu Ngắn gọn.'], '—',
       ['Bản in ghi 24, ĐVT "Can 1L".'], 229)
S6.add('Hủy in', 'P2', PRE, OPEN + ['Bấm In danh sách, bấm Hủy.', 'Mở xem trước rồi bấm ×.'], '—', ['Đóng cửa sổ, không in; báo cáo giữ nguyên.'], 196)

# ============================================================== VII. RÀNG BUỘC
S7 = Sec(7)
S7.add('Phiếu điều chuyển kho', 'P0', [PRE_H, 'Hoàn tất phiếu điều chuyển 3 Xô 18L hàng ENEO-700-V5231 từ kho HP sang kho CB (môi trường kiểm thử).'],
       OPEN + ['Chọn hàng ENEO-700-V5231.', 'Đổi Kho = CB - Cát Bà.'], '—',
       ['Kho HP giảm 3; kho CB tăng 3 (có thêm lô ở vị trí nhận).'], [274, 281, 282])
S7.add('Phiếu điều chuyển vị trí', 'P1', [PRE_H, 'Hoàn tất phiếu điều chuyển vị trí 2 Xô 18L của lô 1.2 từ KHOANG1 sang KHOANG2.'],
       OPEN + ['Chọn hàng ENEO-700-V5231, cấp "Tất cả cấp".'], '—',
       ['Lô 1.2 có 2 vị trí KHOANG1 4, KHOANG2 2; SL công ty và mặt hàng không đổi (20).'], [272, 284])
S7.add('Nhập / xuất điều chỉnh kiểm kê', 'P1', [PRE_H, 'Hoàn tất phiếu nhập kho điều chỉnh kiểm kê +1 và phiếu xuất kho điều chỉnh kiểm kê -1 cho hàng này.'],
       OPEN + ['Chọn hàng ENEO-700-V5231 sau mỗi phiếu.'], '—', ['Sau phiếu nhập: 21; sau phiếu xuất: 20.'], 274)
S7.add('Khai báo tồn kho đầu kỳ', 'P1', [PRE, 'Khai báo tồn đầu kỳ 10 Cái hàng Z (chưa từng có ở kho HP) cho công ty TPHP.'],
       OPEN + ['Chọn hàng Z.'], '—', ['Hàng Z xuất hiện, SL 10, dòng công ty TPHP, lô tồn đầu kỳ.'], 274)
S7.add('Đổi tên hàng ở danh mục', 'P2', [PRE_H, 'Đổi tên hàng ENEO-700-V5231 ở danh mục hàng hóa (môi trường kiểm thử).'], OPEN + ['Chọn hàng ENEO-700-V5231.'], '—',
       ['Báo cáo hiện tên mới, số không đổi.'], [278, 279])
S7.add('Kho ngừng hoạt động không còn trong ô Kho', 'P1', ['Tài khoản DNS Admin.', 'Kho NM - Nhà máy chuyển sang ngừng hoạt động ở danh mục Kho vật lý.'],
       [MENU, 'Chọn công ty CN Hải Phòng, mở ô Kho.'], '—', ['Ô Kho không còn NM - Nhà máy.'], [276, 285])
S7.add('Đổi công ty thuê kho ở danh mục Kho kế toán', 'P2', [PRE, 'Bỏ gắn công ty TPE khỏi kho HP ở danh mục Kho kế toán.'],
       [MENU, CHON_HP], '—', ['Ô Công ty thuê kho chỉ còn TPHP; khối Theo công ty thuê kho không còn TPE.'], [280, 282])
S7.add('Màn chỉ đọc, không làm đổi dữ liệu', 'P0', PRE, OPEN + ['Thao tác lọc, bung, đổi ĐVT, in, xuất nhiều lần.', 'Mở Thẻ kho cùng hàng / kho.'], '—',
       ['Không có chứng từ, tồn kho hay lịch sử nào thay đổi; Thẻ kho giữ nguyên số.'], [268, 270, 285])
S7.add('Đối chiếu với Thẻ kho sau khi lập chứng từ', 'P0', [PRE_H, 'Vừa hoàn tất 1 phiếu nhập và 1 phiếu xuất cho hàng này hôm nay.'],
       ['Mở Thẻ kho kỳ 01/01–hôm nay, ghi Tồn cuối kỳ.', MENU, CHON_HP, 'Chọn hàng ENEO-700-V5231.'], '—',
       ['Tồn cuối kỳ Thẻ kho = SL tồn dòng công ty TPHP.'], [274, 281])

# ============================================================== VIII. PHÂN QUYỀN
S8 = Sec(8)
S8.add('Quyền theo tổng công ty', 'P0', ACC_T, ['Đăng nhập T.', MENU, 'Mở ô Tồn theo công ty, ô Kho.'], '—',
       ['Ô Tồn theo công ty có mọi công ty đang hoạt động (6 công ty); ô Kho có mọi kho của công ty đang chọn.', 'Xem, in, xuất được.'], [287, 299])
S8.add('Quyền theo công ty', 'P0', ACC_C, ['Đăng nhập C.', MENU, 'Mở ô Tồn theo công ty, ô Kho.'], '—',
       ['Ô Tồn theo công ty chỉ có CN Hải Phòng; ô Kho có CB, HP, KĐN-ALM, NM.', 'Xem, in, xuất được.'], [287, 299])
S8.add('Quyền theo kho', 'P0', ACC_K, ['Đăng nhập K.', MENU], '—',
       ['Ô Kho chỉ có HP - Hải Phòng và được chọn sẵn (1 kho); báo cáo hiện ngay 96 mặt hàng.'], [287, 299])
S8.add('Không có quyền nào', 'P0', ACC_N, ['Đăng nhập N.', MENU], '—',
       ['Mục menu vẫn hiện; mở màn báo "%s".' % NOPERM, 'Ô Tồn theo công ty, Kho rỗng; bảng "Chọn công ty để xem báo cáo.", không có số liệu.', 'Bấm In danh sách / Xuất Excel: chữ đỏ dưới ô thiếu, không ra bản in / file.'], [287, 295])
S8.add('Mở trực tiếp đường dẫn khi thiếu quyền', 'P0', ACC_N, ['Đăng nhập N.', 'Dán đường dẫn màn báo cáo vào thanh địa chỉ.'], '—',
       ['Báo "%s"; bảng "Chọn công ty để xem báo cáo.", không lộ số liệu.' % NOPERM], 296)
S8.add('Kho ngoài phạm vi bị chặn', 'P0', ACC_C, ['Đăng nhập C.', MENU, 'Sửa bộ lọc ghi tạm của trình duyệt cho Kho = LN - Liên Ninh (kho công ty TPE), F5.'], '—',
       ['Kho LN bị bỏ, ô Kho trống, không hiện số kho LN.'], 299)
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
    ('IV', 'XEM CHI TIẾT THEO CÔNG TY THUÊ KHO – LÔ – VỊ TRÍ', S4),
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
                feature_name='Báo cáo tồn kho chi tiết theo mặt hàng - Cập nhật ngày 06/11/2026',
                module_name='Báo cáo tồn kho chi tiết theo mặt hàng', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='bao_cao')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

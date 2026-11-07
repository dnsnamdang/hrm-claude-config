# -*- coding: utf-8 -*-
"""Testcase màn "Báo cáo tồn kho tổng hợp theo mặt hàng" (phân hệ Kho › Báo cáo kho) — skill testcase-documenter, KHUÔN CHUẨN
03/11/2026 (tc_chuan.build_chuan, loai='bao_cao').

Chạy: python gen_testcase.py -> testcase.xlsx (sau đó chạy check_tc ... bao_cao, phải 0 lỗi).
Loại 'bao_cao' (đọc code 07/11/2026): màn chỉ đọc, chỉ có API GET (xem / danh mục / in / xuất). Nhóm có mặt: I Hiển thị · II Tìm kiếm
& lọc (gồm Cài đặt bộ lọc, Chọn hàng hóa) · III Số liệu báo cáo (đối soát) · IV Xem chi tiết (nhóm cột Chi tiết theo công ty thuê kho,
ĐVT) · V Xuất danh sách Excel · VI In báo cáo · VII Ràng buộc · VIII Phân quyền. Không có Tùy chỉnh cột (bảng cố định) → bỏ nhóm.
Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../bao-cao-ton-kho-chi-tiet-mat-hang/gen_testcase.py (06/11, check_tc 0 lỗi).
Nguồn hành vi: FE pages/warehouse/stock-general-product/**; BE Modules/Finance StockGeneralProduct* + WarehouseStockReportService.
Số liệu mẫu dev-hrm 07/11/2026 (DNS Admin, _capture/doisoat.js, chỉ đọc): công ty CN Hải Phòng, 4 kho CB / HP / KĐN-ALM / NM: 96 mặt
hàng, cột Chi tiết TPE / TPHP / TPV, TPE 1 mặt hàng, TPHP 96; ENEO-700-V5231 = 47 (HP 20 + CB 27); chỉ kho HP = 20 = Báo cáo chi tiết =
Báo cáo theo vị trí = Thẻ kho (70 + 496 − 546); 31/12/2025 = 70. Công ty TPE 8 kho: 6.157 mặt hàng; ENEO-640-V5236 kho PTT 3,197 = Thẻ kho
Năm nay (15,141 + 11,404 − 23,348); 31/12/2025 = 15,141. Hợp đồng "%" / "_" ra 3.939 mặt hàng (mọi hàng có chứng từ gắn hợp đồng).
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
MENU = 'Vào phân hệ Kho > menu "Báo cáo kho" > bấm "Báo cáo tồn kho tổng hợp theo mặt hàng".'
CN = 'CN HẢI PHÒNG - CÔNG TY CP CÔNG NGHỆ THIẾT BỊ TÂN PHÁT'
CHON_HP = 'Chọn Tồn theo công ty = "%s" (hệ thống tự chọn đủ 4 kho CB, HP, KĐN-ALM, NM).' % CN
V1 = 'Xem báo cáo tồn kho theo tổng công ty'
V2 = 'Xem báo cáo tồn kho theo công ty'
V3 = 'Xem báo cáo tồn kho theo kho'
NOPERM = 'Bạn không có quyền truy cập chức năng này.'
EMPTY = 'Không có mặt hàng nào khớp bộ lọc.'
CHONKHO = 'Chọn kho để xem báo cáo.'
FILE = 'bao_cao_ton_kho_tong_hop_mat_hang.xlsx'
HANG = 'hàng "Dầu nhớt động cơ Diesel 4 kỳ SAE 20W-50 CF-4 (18L)" (mã ENEO-700-V5231)'
HANG2 = 'hàng "Dầu bôi trơn hộp số tự động tổng hợp Eneos ATF Multi (Chai 1 lít)" (mã ENEO-410-S4136), ĐVT Can 1L và Thùng 24C-1L (x24)'
HANG3 = 'hàng ENEO-640-V5236 "Dầu nhớt bán tổng hợp động cơ ô tô 4 kỳ SP/CF SAE 5W-30 (4Lx6)", ĐVT cơ sở Can 4L'
PRE = ('Tài khoản DNS Admin (Super admin, coi như có quyền "%s").\n'
       'Công ty %s có 4 kho CB, HP, KĐN-ALM, NM; tính đến 07/11/2026 có 96 mặt hàng còn tồn; công ty thuê kho TPE có 1 mặt hàng, TPHP có '
       '96, TPV 0.' % (V1, CN))
PRE_H = PRE + '\n%s: tồn 47 Xô 18L trên 4 kho (HP 20, CB 27), toàn bộ thuộc công ty thuê TPHP.' % HANG
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
     'Xem tồn của từng mặt hàng cộng trên MỘT HOẶC NHIỀU kho của một công ty, tính đến hết một ngày, chia cột theo công ty thuê kho '
     '(nhóm cột Chi tiết). Màn chỉ đọc: không thêm / sửa / xóa; có In (2 kiểu, chọn cột) và Xuất Excel (2 kiểu).'),
    ('2. Đối tượng được tính / hiển thị',
     '- Mặt hàng có tổng tồn các công ty thuê kho đang lọc khác 0 (có thể âm) trên các kho đã chọn, tính tới hết ngày Tính đến ngày.\n'
     '- Cột Chi tiết: mọi công ty thuê kho đang lọc (kể cả cột toàn trống), sắp theo mã công ty.\n'
     '- Nguồn số: mọi chứng từ kho đã ghi tồn (tồn đầu kỳ, nhập kho, nhập lại, xuất kho, xuất điều chỉnh, điều chuyển kho, nhập / xuất điều chỉnh kiểm kê).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Mặt hàng có tổng tồn = 0.\n- Thay đổi tồn sau ngày Tính đến ngày.\n'
     '- Kho ngoài phạm vi quyền, kho khác công ty đang xem, kho đã ngừng hoạt động, công ty thuê không gắn với các kho đang chọn.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô Tính đến ngày (bắt buộc, mặc định hôm nay): cộng thay đổi tồn tới hết 23:59 ngày đó, cho cả SL tồn và các cột công ty.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Bảng phẳng: dòng TỔNG > mỗi mặt hàng 1 dòng (STT 1, 2…). Cột: STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn, nhóm Chi tiết '
     '(chỉ quyền tổng công ty). Phân trang theo mặt hàng (mặc định 20).'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Cột công ty = tổng thay đổi tồn (nhập cộng, xuất trừ) của công ty đó trên mọi kho đang chọn.\n- SL tồn = tổng các cột công ty đang lọc.\n'
     '- Nhiều kho: 1 mặt hàng vẫn 1 dòng, số = tổng các kho.\n- Ô theo công ty thuê kho đếm mặt hàng riêng từng công ty (1 hàng có thể nằm ở 2 ô).'),
    ('7. Phân quyền cấp',
     '- %s: chọn mọi công ty, mọi kho, thấy nhóm cột Chi tiết (Super admin coi như có quyền này).\n- %s: công ty mình, kho của công ty mình.\n'
     '- %s: công ty mình, chỉ kho mình là thủ kho.\n- Không có quyền nào: không xem được, báo "%s".' % (V1, V2, V3, NOPERM)),
    ('8. Cách tính các ô thống kê',
     '- Ô Mặt hàng còn tồn = dòng TỔNG = N ở "Hiển thị a–b / N mặt hàng".\n- Ô Kho đang xem = số kho đang chọn.\n'
     '- Ô Công ty thuê kho có tồn = số công ty có ít nhất 1 mặt hàng tồn > 0; ô từng công ty = số mặt hàng công ty đó còn tồn.\n'
     '- Đối soát: Tồn đầu kỳ + Nhập - Xuất (Thẻ kho) = cột công ty khi chọn đúng 1 kho, cùng hàng / công ty / ngày.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản: DNS Admin (Super admin), T (tổng công ty), C (theo công ty), K (theo kho), N (không quyền).\n'
     '- Lưu ý: số trên màn quy đổi theo ĐVT chọn ở từng hàng, làm tròn 2 số lẻ; In / Excel dùng đúng ĐVT đã chọn.\n'
     '- Lưu ý: quyền theo công ty / theo kho không thấy nhóm cột Chi tiết trên màn nhưng In / Excel kiểu Đầy đủ vẫn có (giữ như hệ thống cũ).\n'
     '- Lưu ý: màn không có ô tìm nhanh và không sắp xếp theo cột; ô Hợp đồng chỉ áp khi Enter / Tìm kiếm.\n'
     '- Lưu ý: dev 07/11 cửa sổ Chọn hàng hóa báo không tải được danh sách hàng khi Tồn theo công ty khác công ty đăng nhập (TC_02.039 — đã báo, chờ xử lý).'),
]

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', 'Tài khoản DNS Admin, công ty TPE, chưa mở màn trong 10 phút qua.', [MENU], '—',
       ['Mở màn "Báo cáo tồn kho tổng hợp theo mặt hàng".',
        'Tính đến ngày = hôm nay, Tồn theo công ty = công ty TPE, ô Xem toàn bộ kho được tích, Kho có đủ 8 kho của công ty TPE.',
        'Báo cáo tự hiện: "Hiển thị 1–20 / 6157 mặt hàng", không báo lỗi.'], [1, 36])
S1.add('Tiêu đề màn hình', 'P1', PRE, [MENU, 'Quan sát thanh tiêu đề và tab trình duyệt.'], '—',
       ['Cả 2 nơi là "Báo cáo tồn kho tổng hợp theo mặt hàng"; khối lọc có tiêu đề "Bộ lọc báo cáo tồn kho".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE, OPEN + ['Quan sát khối lọc và bảng.'], '—',
       ['Đầu khối lọc: In danh sách, Xuất Excel, Cài đặt bộ lọc, Ẩn tìm kiếm nâng cao.', 'Dưới các ô lọc: Tìm kiếm, Xóa lọc.',
        'Dòng tóm tắt có nút Thu gọn.', 'KHÔNG có nút Tạo mới, Sửa, Xóa, Import, Lịch sử.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', PRE, OPEN + ['Đọc tiêu đề cột.'], '—',
       ['7 cột: STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn; sau đó nhóm "Chi tiết" gồm 3 cột TPE, TPHP, TPV.',
        'Cột ĐVT, SL tồn, nhóm Chi tiết có biểu tượng chữ i.'], 4)
S1.add('Không có cột ẩn và không có tùy chỉnh cột', 'P2', PRE, OPEN + ['Tìm nút cấu hình cột trên bảng.'], '—',
       ['Không có nút cấu hình cột; bảng luôn đủ cột như trên.'], 5)
S1.add('Dữ liệu dòng mặt hàng khớp danh mục hàng', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231 ở ô Hàng hóa.'], 'Hàng hóa: ENEO-700-V5231',
       ['Dòng 1: tên "Dầu nhớt động cơ Diesel 4 kỳ SAE 20W-50 CF-4 (18L)", Model "CF4 20W50 18L", Mã hàng ENEO-700-V5231, Thương hiệu ENEOS, '
        'ĐVT "Xô 18L", SL tồn 47, cột TPHP 47, TPE và TPV trống.'], 6)
S1.add('Mặt hàng tồn bằng 0 không hiện', 'P0', [PRE, 'Hàng X đã xuất hết ở cả 4 kho (tổng nhập = tổng xuất).'],
       OPEN + ['Chọn hàng X ở ô Hàng hóa.'], 'Hàng hóa: X',
       ['Bảng hiện "%s"; dòng báo cáo không có trạng thái Khóa / Hoạt động.' % EMPTY], 7)
S1.add('Kho chưa có hàng tồn', 'P1', [PRE, 'Kho KĐN-ALM và NM không còn mặt hàng tồn.'],
       OPEN + ['Bỏ kho CB và HP ở ô Kho (còn KĐN-ALM, NM).'], 'Kho: KĐN-ALM, NM',
       ['Khối tổng hợp: Mặt hàng còn tồn 0; bảng hiện "%s"; ẩn phân trang; không báo lỗi.' % EMPTY], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE, OPEN + ['Gõ "ZZZ999" vào ô Hợp đồng, nhấn Enter.'], 'Hợp đồng: ZZZ999',
       ['Bảng hiện "%s"; khối tổng hợp Mặt hàng còn tồn 0.' % EMPTY], [9, 40])
S1.add('Số mặt hàng mặc định mỗi trang', 'P0', PRE, OPEN, '—',
       ['Trang 1 có 20 mặt hàng (STT 1 đến 20); dưới bảng "Hiển thị 1–20 / 96 mặt hàng"; Số dòng/trang = 20.'], [10, 16])
S1.add('Thay đổi số dòng / trang', 'P0', PRE, OPEN + ['Sang trang 2.', 'Đổi Số dòng/trang thành 50.'], 'Số dòng/trang: 50',
       ['Bảng hiện 50 mặt hàng, về trang 1, "Hiển thị 1–50 / 96 mặt hàng".', 'Lựa chọn có 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P1', PRE, OPEN + ['Bấm ›.', 'Bấm ‹.'], '—',
       ['Bấm › sang trang 2: "Hiển thị 21–40 / 96", STT từ 21.', 'Bấm ‹ về trang 1.'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE, OPEN + ['Bấm ».', 'Bấm «.'], '—',
       ['Bấm » tới trang 5: "Hiển thị 81–96 / 96 mặt hàng".', 'Bấm « về trang 1.'], 13)
S1.add('Trạng thái nút ở trang đầu / cuối', 'P2', PRE, OPEN + ['Quan sát nút ở trang 1, rồi ở trang 5.'], '—',
       ['Trang 1: nút « ‹ mờ, không bấm được.', 'Trang 5: nút › » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P1', PRE, OPEN + ['Sang trang 2.'], '—',
       ['Mặt hàng đầu trang 2 có STT 21 (nối tiếp trang 1).'], 15)
S1.add('Về trang 1 khi đổi bộ lọc', 'P1', PRE, OPEN + ['Sang trang 3.', 'Chọn Thương hiệu = ENEOS.'], 'Thương hiệu: ENEOS',
       ['Báo cáo nạp lại từ trang 1; tổng N cập nhật theo bộ lọc.'], [17, 42])
S1.add('Thứ tự mặc định theo tên hàng', 'P0', PRE, OPEN, '—',
       ['Mặt hàng xếp theo tên A đến Z: 1 Áo khoác ENEOS, 2 Áo mưa ENEOS, 3 Áo phông cao cấp ENEOS, 4 Áo phông ENEOS, 5 Bình giữ nhiệt…'], 19)
S1.add('Không sắp xếp theo cột', 'P2', PRE, OPEN + ['Bấm tiêu đề cột Mã hàng, SL tồn, TPHP.'], '—',
       ['Thứ tự không đổi (luôn theo tên hàng); tiêu đề cột không có biểu tượng sắp xếp.'], [20, 21, 22, 23])
S1.add('Giữ thứ tự khi chuyển trang', 'P2', PRE, OPEN + ['Sang trang 2, quay lại trang 1.'], '—',
       ['Trang 2 tiếp tục thứ tự tên hàng; quay lại trang 1 đúng 20 mặt hàng như lúc đầu.'], 24)
S1.add('Thu gọn / mở rộng khối tổng hợp', 'P2', PRE, OPEN + ['Bấm Thu gọn.', 'Bấm Mở rộng.'], '—',
       ['Thu gọn: ẩn các ô Mặt hàng, Theo công ty thuê kho, còn dòng tóm tắt; chữ nút "Mở rộng".', 'Mở rộng: hiện lại, số không đổi.'], 3)
S1.add('Dòng tóm tắt báo cáo', 'P1', PRE, OPEN + ['Rê chuột vào phần "Kho:" và vào chữ i cạnh dòng tóm tắt.'], '—',
       ['Dòng "Tồn kho tính đến ngày 07/11/2026 · Kho: CB, HP, KĐN-ALM, NM"; rê chuột phần Kho hiện "CB - Cát Bà, HP - Hải Phòng, KĐN-ALM - Kho gửi tại Đồng Nai, NM - Nhà máy".',
        'Chữ i hiện "BÁO CÁO TỒN KHO TỔNG HỢP THEO MẶT HÀNG", dòng cuối "Số liệu tính tại <ngày giờ>".'], 6)
S1.add('Bảng rộng cuộn ngang, tiêu đề dính', 'P2', 'Tài khoản DNS Admin, công ty TPE (5 công ty thuê kho).', [MENU, 'Cuộn bảng xuống và sang phải.'], '—',
       ['Tiêu đề 2 tầng (Chi tiết + mã công ty) dính trên cùng khi cuộn xuống; bảng cuộn ngang khi không đủ chỗ, trang không vỡ.'], 4)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Hợp đồng: khớp chính xác mã', 'P0', [PRE, 'Hợp đồng H có phiếu nhập kho vào kho HP.'], OPEN + ['Gõ đủ mã hợp đồng H vào ô Hợp đồng, nhấn Enter.'],
       'Hợp đồng: mã H', ['Chỉ còn mặt hàng có chứng từ nhập / xuất thuộc hợp đồng H; SL tồn là phần tồn đến từ các chứng từ đó.'], 26)
S2.add('Hợp đồng: khớp một phần mã', 'P0', [PRE, 'Hợp đồng H như trên.'], OPEN + ['Gõ một đoạn giữa của mã H, nhấn Enter.'], 'Hợp đồng: một phần mã H',
       ['Kết quả như khi gõ đủ mã (khớp một phần).'], 27)
S2.add('Hợp đồng: không phân biệt hoa / thường', 'P1', [PRE, 'Hợp đồng H như trên.'], OPEN + ['Gõ mã H bằng chữ thường, nhấn Enter.'],
       'Hợp đồng: mã H chữ thường', ['Kết quả như khi gõ chữ hoa.'], 28)
S2.add('Hợp đồng: chữ Đ và D khác nhau', 'P2', [PRE, 'Mã hợp đồng H bắt đầu bằng "HĐ".'], OPEN + ['Gõ mã H thay "Đ" bằng "D", nhấn Enter.'],
       'Hợp đồng: HD…', ['Bảng hiện "%s" — hệ thống phân biệt Đ và D.' % EMPTY], 29)
S2.add('Hợp đồng: mã không tồn tại', 'P1', PRE, OPEN + ['Gõ "KHONGCO-123", nhấn Enter.'], 'Hợp đồng: KHONGCO-123', ['Bảng hiện "%s".' % EMPTY], 30)
S2.add('Hợp đồng: ký tự đặc biệt', 'P2', 'Tài khoản DNS Admin, công ty TPE (8 kho, 6.157 mặt hàng).',
       [MENU, 'Gõ "%" vào ô Hợp đồng, nhấn Enter.', 'Gõ "_", nhấn Enter.', 'Gõ "<script>", nhấn Enter.'],
       ['Hợp đồng: %', 'Hợp đồng: _', 'Hợp đồng: <script>'],
       ['Gõ "%" hoặc "_": ra 3.939 mặt hàng — mọi hàng có chứng từ gắn bất kỳ hợp đồng nào (ký tự được hiểu là "bất kỳ").',
        'Gõ "<script>": bảng rỗng, không lỗi, không chạy mã.'], 31)
S2.add('Hợp đồng: khoảng trắng đầu / cuối', 'P1', [PRE, 'Hợp đồng H như trên.'], OPEN + ['Gõ "  <mã H>  ", nhấn Enter.'], 'Hợp đồng: mã H có khoảng trắng',
       ['Kết quả như gõ mã H (tự bỏ khoảng trắng đầu / cuối).'], 32)
S2.add('Hợp đồng: không giới hạn ký tự', 'P2', PRE, OPEN + ['Gõ chuỗi 300 ký tự "A", nhấn Enter.'], 'Hợp đồng: 300 ký tự',
       ['Ô nhận đủ, không báo lỗi; bảng hiện "%s".' % EMPTY], 33)
S2.add('Xóa chữ ở ô Hợp đồng', 'P1', [PRE, 'Đang lọc Hợp đồng = mã H.'], OPEN + ['Xóa hết chữ ô Hợp đồng, nhấn Enter.'], '—',
       ['Báo cáo trở lại 96 mặt hàng.'], 34)
S2.add('Hợp đồng chỉ áp khi Enter hoặc Tìm kiếm', 'P0', PRE, OPEN + ['Gõ "ZZZ999" nhưng không nhấn Enter.', 'Bấm Tìm kiếm.'], 'Hợp đồng: ZZZ999',
       ['Sau bước 3 bảng chưa đổi.', 'Sau bước 4 báo cáo lọc theo hợp đồng, về trang 1.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P0', 'Tài khoản DNS Admin công ty TPE, chưa mở màn trong 10 phút.', [MENU], '—',
       ['Tính đến ngày = hôm nay; Tồn theo công ty = công ty TPE; Xem toàn bộ kho tích; Kho = 8 kho CSKH, DATD, KTCN, LN, N10, N9, PTT, SL; '
        'Công ty thuê kho = mọi công ty thuê của các kho; Nhóm, Tính chất, Loại, Thương hiệu, Hãng sản xuất, Hàng hóa, Hợp đồng trống; khối lọc mở sẵn.'], 36)
S2.add('Bỏ tích Xem toàn bộ kho', 'P0', PRE, OPEN + ['Bỏ tích Xem toàn bộ kho.'], '—',
       ['Ô Kho và Công ty thuê kho về trống; bảng "%s"; không báo lỗi.' % CHONKHO], [36, 37])
S2.add('Tích lại Xem toàn bộ kho', 'P1', [PRE, 'Ô Kho đang trống.'], OPEN + ['Bỏ tích rồi tích lại Xem toàn bộ kho.'], '—',
       ['Ô Kho có lại đủ 4 kho; Công ty thuê kho tích TPE, TPHP, TPV; báo cáo nạp lại 96 mặt hàng.'], 37)
S2.add('Bỏ 1 kho thì ô Xem toàn bộ kho tự bỏ tích', 'P1', PRE, OPEN + ['Bấm × ở chip NM trong ô Kho.'], 'Kho: CB, HP, KĐN-ALM',
       ['Ô Xem toàn bộ kho tự bỏ tích; báo cáo nạp lại với 3 kho, dòng tóm tắt "Kho: CB, HP, KĐN-ALM".'], 37)
S2.add('Thiếu Kho thì báo đỏ', 'P0', PRE, OPEN + ['Bỏ tích Xem toàn bộ kho.', 'Bấm Tìm kiếm.'], '—',
       ['Ô Kho viền đỏ, chữ "Vui lòng chọn kho"; không nạp báo cáo; bảng "%s".' % CHONKHO, 'Chọn lại 1 kho: chữ đỏ tự tắt.'], [36, 37])
S2.add('Thiếu Tính đến ngày thì báo đỏ', 'P1', PRE, OPEN + ['Xóa ngày ở Tính đến ngày.', 'Bấm Tìm kiếm.'], '—',
       ['Ô Tính đến ngày chữ đỏ "Vui lòng chọn ngày"; bảng "Chọn ngày để xem báo cáo.".'], 37)
S2.add('Lọc Tính đến ngày quá khứ', 'P0', PRE_H, OPEN + ['Chỉ giữ kho HP.', 'Chọn hàng ENEO-700-V5231.', 'Đổi Tính đến ngày = 31/12/2025.'],
       'Tính đến ngày: 31/12/2025', ['SL tồn = 70, cột TPHP 70; dòng tóm tắt "Tồn kho tính đến ngày 31/12/2025".'], 37)
S2.add('Đổi Tồn theo công ty chọn lại hết kho', 'P1', PRE, OPEN + ['Đổi Tồn theo công ty sang công ty TPE.'], '—',
       ['Ô Kho tự chọn đủ 8 kho của công ty TPE, Xem toàn bộ kho tích; Công ty thuê kho tích mọi công ty thuê của 8 kho; báo cáo nạp lại.'], 37)
S2.add('Đổi Kho tự chọn công ty thuê kho', 'P0', PRE, OPEN + ['Bỏ kho HP, KĐN-ALM, NM (còn CB).'], 'Kho: CB',
       ['Ô Công ty thuê kho chỉ còn công ty thuê của kho CB (TPHP), tự tích; báo cáo nạp ngay; nhóm Chi tiết chỉ còn cột TPHP.'], 37)
S2.add('Lọc Công ty thuê kho', 'P0', PRE, OPEN + ['Bỏ TPHP và TPV ở Công ty thuê kho (còn TPE).'], 'Công ty thuê kho: TPE',
       ['Còn 1 mặt hàng; nhóm Chi tiết chỉ còn cột TPE; khối Theo công ty thuê kho chỉ còn ô TPE 1 mặt hàng.'], 37)
S2.add('Bỏ trống Công ty thuê kho', 'P1', PRE, OPEN + ['Bỏ hết công ty ở ô Công ty thuê kho.'], '—',
       ['Báo cáo tính mọi công ty thuê của các kho: vẫn 96 mặt hàng, nhóm Chi tiết TPE, TPHP, TPV.'], 37)
S2.add('Lọc Nhóm, Tính chất, Loại, Hãng sản xuất', 'P1', PRE, OPEN + ['Lần lượt chọn 1 giá trị ở từng ô, sau mỗi ô bỏ chọn.'], '—',
       ['Mỗi lần chỉ còn mặt hàng thuộc giá trị đã chọn; bỏ chọn trở lại 96.', 'Loại hàng hóa: hàng thuộc ít nhất 1 loại đã chọn.'], 37)
S2.add('Lọc Thương hiệu', 'P1', PRE, OPEN + ['Chọn Thương hiệu = ENEOS.'], 'Thương hiệu: ENEOS', ['Mọi dòng có Thương hiệu ENEOS.'], 37)
S2.add('Kết hợp nhiều ô lọc', 'P0', PRE_H, OPEN + ['Chọn Thương hiệu = ENEOS.', 'Chọn hàng ENEO-700-V5231.'], ['Thương hiệu: ENEOS', 'Hàng hóa: ENEO-700-V5231'],
       ['Chỉ còn 1 mặt hàng thỏa CẢ 2 điều kiện (SL tồn 47).', 'Chọn Thương hiệu khác ENEOS: bảng "%s".' % EMPTY], [38, 39])
S2.add('Tổng và phân trang sau lọc', 'P1', PRE, OPEN + ['Chọn Thương hiệu = ENEOS.'], 'Thương hiệu: ENEOS',
       ['Ô Mặt hàng còn tồn = dòng TỔNG = N ở "Hiển thị 1–x / N"; số trang tính lại theo N.'], [41, 42])
S2.add('Thứ tự sau lọc', 'P2', PRE, OPEN + ['Chọn Thương hiệu = ENEOS.'], '—', ['Kết quả vẫn xếp theo tên hàng A đến Z.'], 43)
S2.add('Xóa lọc', 'P0', [PRE, 'Đang lọc công ty CN Hải Phòng, chỉ kho HP, Thương hiệu ENEOS, Hợp đồng ZZZ.'], OPEN + ['Bấm Xóa lọc.'], '—',
       ['Tính đến ngày về hôm nay, Tồn theo công ty về công ty của tài khoản (TPE), Kho đủ 8 kho, các ô khác trống (kể cả Hàng hóa).',
        'Báo cáo nạp lại trang 1; chữ đỏ biến mất.'], 44)
S2.add('Chuyển màn rồi quay lại', 'P1', [PRE, 'Đang lọc công ty CN Hải Phòng.'], OPEN + ['Mở màn Thẻ kho.', MENU], '—',
       ['Bộ lọc về mặc định (công ty của tài khoản, toàn bộ kho).'], 45)
S2.add('Tải lại trang (F5)', 'P0', [PRE, 'Đang lọc công ty CN Hải Phòng, hàng ENEO-700-V5231.'], OPEN + ['Nhấn F5 trong vòng 10 phút.'], '—',
       ['Giữ nguyên công ty, 4 kho, ô Hàng hóa vẫn hiện "ENEO-700-V5231 - Dầu nhớt…", báo cáo nạp lại.', 'Sau hơn 10 phút F5: bộ lọc về mặc định.'], 46)
S2.add('Mở tab mới', 'P2', [PRE, 'Đang lọc công ty CN Hải Phòng.'], OPEN + ['Mở màn ở tab mới trong 10 phút.'], '—', ['Tab mới khôi phục bộ lọc CN Hải Phòng.'], 47)
S2.add('Tài khoản khác cùng trình duyệt', 'P2', [PRE, ACC_C, 'DNS Admin vừa lọc công ty CN Hải Phòng rồi đăng xuất (trong 10 phút).'],
       ['Đăng nhập C trên cùng trình duyệt.', MENU], '—',
       ['Nếu bộ lọc ghi tạm còn hạn, C thấy 4 kho được chọn sẵn (thuộc công ty C); kho / công ty ngoài phạm vi của C bị bỏ.'], 48)
S2.add('Cài đặt bộ lọc: mở cửa sổ', 'P1', PRE, OPEN + ['Bấm Cài đặt bộ lọc.'], '—',
       ['Cửa sổ "Cài đặt bộ lọc" liệt kê 12 ô lọc có ô tích (gồm Xem toàn bộ kho), nút Lưu, Khôi phục mặc định, Đóng.'], 37)
S2.add('Cài đặt bộ lọc: ẩn ô và lưu', 'P1', PRE, OPEN + ['Bấm Cài đặt bộ lọc.', 'Bỏ tích Hãng sản xuất.', 'Bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công"; khối lọc không còn ô Hãng sản xuất; F5 vẫn ẩn.'], 37)
S2.add('Cài đặt bộ lọc: đổi thứ tự, khôi phục, đóng', 'P2', PRE,
       OPEN + ['Bấm Cài đặt bộ lọc.', 'Kéo Hợp đồng lên đầu, bấm Đóng.', 'Mở lại, bấm Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bấm Đóng: thứ tự không đổi.', 'Khôi phục + Lưu: đủ 12 ô theo thứ tự gốc.'], 37)
S2.add('Chọn hàng hóa: mở cửa sổ', 'P0', 'Tài khoản DNS Admin, công ty TPE.', [MENU, 'Bấm ô Hàng hóa.'], '—',
       ['Mở cửa sổ "Chọn hàng hóa": dòng công ty TPE, cây catalog có số hàng, ô tìm, công tắc Còn tồn / Gồm hàng ngoài catalog, bảng hàng, nút Đóng.',
        'Chân cửa sổ ghi "Bấm vào tên hàng để chọn".'], 37)
S2.add('Chọn hàng hóa: chọn 1 hàng', 'P0', 'Tài khoản DNS Admin, công ty TPE, 8 kho.', [MENU, 'Bấm ô Hàng hóa.', 'Tìm "ENEO-640-V5236", bấm tên hàng.'],
       'Hàng hóa: ENEO-640-V5236',
       ['Cửa sổ đóng; ô Hàng hóa "ENEO-640-V5236 - Dầu nhớt bán tổng hợp…"; báo cáo còn 1 mặt hàng, SL tồn 3,197 (nạp 1 lần).'], 37)
S2.add('Chọn hàng hóa: bỏ chọn bằng dấu ×', 'P1', [PRE_H, 'Đang chọn hàng ENEO-700-V5231.'], OPEN + ['Bấm dấu × trên ô Hàng hóa.'], '—',
       ['Ô Hàng hóa trống, cửa sổ không mở; báo cáo trở lại 96 mặt hàng.'], [34, 37])
S2.add('Chọn hàng hóa: đóng không chọn', 'P2', PRE, OPEN + ['Bấm ô Hàng hóa.', 'Bấm Đóng.'], '—', ['Cửa sổ đóng, bộ lọc không đổi.'], 37)
S2.add('Chọn hàng hóa với công ty khác công ty đăng nhập', 'P1', 'Tài khoản DNS Admin đăng nhập công ty TPE.',
       OPEN + ['Bấm ô Hàng hóa.'], '—',
       ['Cửa sổ ghi "Công ty %s".' % CN, 'Cây catalog có số hàng, danh sách hàng tải được, không báo "Không tải được số lượng" / "Không tải được danh sách hàng hoá"; chọn được hàng.'], 37)

# ============================================================== III. SỐ LIỆU BÁO CÁO
S3 = Sec(3)
S3.add('Khối tổng hợp', 'P0', PRE, OPEN, '—',
       ['Ô Mặt hàng còn tồn 96 mặt hàng; Kho đang xem 4 kho; Công ty thuê kho có tồn 2 công ty.',
        'Khối Theo công ty thuê kho: TPE 1 mặt hàng, TPHP 96 mặt hàng (TPV không có ô vì 0).'], 6)
S3.add('Dòng TỔNG khớp khối tổng hợp và tổng số', 'P0', PRE, OPEN + ['Sang trang 2.'], '—',
       ['Dòng TỔNG "MẶT HÀNG CÒN TỒN 96 mặt hàng" = ô Mặt hàng còn tồn = N ở "Hiển thị … / 96".',
        'Sang trang 2 dòng TỔNG và khối tổng hợp không đổi; dòng TỔNG không có số lượng.'], [16, 41])
S3.add('SL tồn bằng tổng các cột công ty', 'P0', PRE, OPEN + ['Đọc từng dòng trang 1 và trang 2.'], '—',
       ['Mỗi dòng: SL tồn = TPE + TPHP + TPV (vd Áo khoác ENEOS 43 = TPHP 43).', 'Cột công ty bằng 0 để trống; SL tồn bằng 0 không xuất hiện.'], 283)
S3.add('Nhiều kho bằng tổng từng kho', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231, ghi SL tồn (4 kho).', 'Lần lượt chỉ giữ 1 kho HP, CB, KĐN-ALM, NM; ghi SL tồn.'], '—',
       ['4 kho: 47; HP 20; CB 27; KĐN-ALM và NM: "%s".' % EMPTY, '47 = 20 + 27.'], 283)
S3.add('Đối soát tồn đầu + nhập - xuất = tồn cuối với Thẻ kho', 'P0',
       [PRE_H, 'Thẻ kho của hàng tại kho HP, công ty thuê TPHP, kỳ 01/01/2026–07/11/2026: Tồn đầu kỳ 70, Nhập 496, Xuất 546, Tồn cuối kỳ 20.'],
       ['Mở Thẻ kho, chọn hàng ENEO-700-V5231, kho HP, công ty thuê TPHP, kỳ từ 01/01/2026 đến 07/11/2026; ghi Tồn đầu, Nhập, Xuất, Tồn cuối.',
        MENU, CHON_HP, 'Chỉ giữ kho HP, chọn hàng ENEO-700-V5231, Tính đến ngày 07/11/2026.'], 'Tính đến ngày: 07/11/2026',
       ['70 + 496 - 546 = 20 = cột TPHP = SL tồn của báo cáo này.'], 6)
S3.add('Đối soát tồn đầu kỳ với ngày quá khứ', 'P0', PRE_H, OPEN + ['Chỉ giữ kho HP, chọn hàng ENEO-700-V5231, Tính đến ngày 31/12/2025.'], 'Tính đến ngày: 31/12/2025',
       ['SL tồn = cột TPHP = 70 = Tồn đầu kỳ của Thẻ kho kỳ bắt đầu 01/01/2026.'], 6)
S3.add('Đối soát hàng tồn lớn với Thẻ kho', 'P0',
       ['Tài khoản DNS Admin, công ty TPE.', '%s; Thẻ kho kho PTT, kỳ Năm nay: Tồn đầu 15,141, Nhập 11,404, Xuất 23,348, Tồn cuối 3,197.' % HANG3],
       [MENU, 'Chỉ giữ kho PTT, chọn hàng ENEO-640-V5236.', 'Đổi Tính đến ngày = 31/12/2025.'], ['Kho: PTT', 'Tính đến ngày: hôm nay, rồi 31/12/2025'],
       ['Hôm nay: SL tồn 3,197 = cột TPE = 15,141 + 11,404 - 23,348.', '31/12/2025: SL tồn 15,141 = Tồn đầu kỳ của Thẻ kho.',
        'Giữ đủ 8 kho công ty TPE: vẫn 3,197 (hàng chỉ có ở kho PTT).'], 6)
S3.add('Đối soát với Báo cáo tồn kho chi tiết theo mặt hàng', 'P0', PRE_H,
       ['Mở Báo cáo tồn kho chi tiết theo mặt hàng, chọn công ty %s, kho HP, hàng ENEO-700-V5231, cùng ngày.' % CN, 'Ghi SL tồn và SL dòng công ty TPHP.',
        MENU, CHON_HP, 'Chỉ giữ kho HP, chọn hàng ENEO-700-V5231.'], '—',
       ['SL tồn bằng nhau (20); dòng công ty TPHP (20) = cột TPHP.'], 6)
S3.add('Đối soát với Báo cáo tồn kho theo vị trí', 'P1', PRE_H,
       ['Mở Báo cáo tồn kho theo vị trí, kho HP, hàng ENEO-700-V5231; cộng SL hàng ở các vị trí.', MENU, CHON_HP, 'Chỉ giữ kho HP, chọn hàng ENEO-700-V5231.'], '—',
       ['Tổng các vị trí (KHOANG1 20) = SL tồn báo cáo này (20).'], 6)
S3.add('Lập chứng từ nhập thì số tăng', 'P0', [PRE_H, 'Lập và hoàn tất 1 Phiếu nhập kho 5 Xô 18L hàng ENEO-700-V5231 vào kho HP, công ty TPHP (môi trường kiểm thử).'],
       OPEN + ['Chọn hàng ENEO-700-V5231, Tính đến ngày hôm nay.'], '—',
       ['SL tồn và cột TPHP tăng 5 (47 thành 52).', 'Chọn Tính đến ngày = hôm qua: vẫn 47.'], [274, 281])
S3.add('Lập chứng từ xuất thì số giảm', 'P0', [PRE_H, 'Hoàn tất 1 Phiếu xuất kho 2 Xô 18L hàng ENEO-700-V5231 từ kho CB (môi trường kiểm thử).'],
       OPEN + ['Chọn hàng ENEO-700-V5231.'], '—', ['SL tồn và cột TPHP giảm 2.'], [274, 281])
S3.add('Định dạng số', 'P1', 'Tài khoản DNS Admin, công ty TPE (có mặt hàng tồn trên 1.000).', [MENU], '—',
       ['SL tồn và cột công ty căn phải, phân cách hàng nghìn bằng dấu phẩy (vd 3,197); số lẻ hiện tối đa 2 chữ số.'], 6)
S3.add('Một hàng nằm ở nhiều công ty thuê kho', 'P1', 'Tài khoản DNS Admin, công ty TPE, 8 kho: TPE 6.074 mặt hàng, TPHP 2, TPSG 340, TPV 62; tổng 6.157.',
       [MENU], '—',
       ['Ô TPE 6,074, TPHP 2, TPSG 340, TPV 62; ô Mặt hàng còn tồn 6,157 (nhỏ hơn tổng các ô vì 1 hàng có thể ở nhiều công ty).',
        'Cột DTTDETEK có trong nhóm Chi tiết dù không có ô ở khối tổng hợp (không còn mặt hàng tồn).'], 286)

# ============================================================== IV. XEM CHI TIẾT
S4 = Sec(4)
S4.add('Nhóm cột Chi tiết theo công ty thuê kho', 'P0', PRE, OPEN, '—',
       ['Tiêu đề 2 tầng: "Chi tiết" trên, dưới là TPE, TPHP, TPV (sắp theo mã).', 'Rê chuột vào TPHP hiện tên công ty thuê kho.'], [186, 187])
S4.add('Chữ i của nhóm Chi tiết', 'P2', PRE, OPEN + ['Rê chuột vào chữ i cạnh "Chi tiết".'], '—',
       ['Hiện "CHI TIẾT" và "SL tồn của từng công ty thuê kho, tính đến ngày đã chọn, cộng trên các kho đang xem".'], 187)
S4.add('Dữ liệu chi tiết khớp dòng', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231.'], '—',
       ['Cột TPHP 47 = SL tồn 47; TPE, TPV trống.'], [188, 190])
S4.add('Chi tiết chỉ đọc', 'P1', PRE, OPEN + ['Bấm vào tên hàng, số SL tồn, số ở cột TPHP.'], '—',
       ['Không có ô nhập, không có nút Lưu / Sửa / Xóa; bấm số không mở cửa sổ hay màn khác.'], [191, 192, 193])
S4.add('Đổi ĐVT trên dòng mặt hàng', 'P0', [PRE, '%s tồn 24 Can 1L (TPHP).' % HANG2],
       OPEN + ['Tìm dòng ENEO-410-S4136.', 'Ở cột ĐVT chọn "Thùng 24C-1L (x24)".'], 'ĐVT: Thùng 24C-1L (x24)',
       ['SL tồn và cột TPHP của hàng đổi thành 1.', 'Các mặt hàng khác không đổi; không tải lại báo cáo.'], 189)
S4.add('Quy đổi làm tròn 2 số lẻ', 'P1', [PRE, 'Hàng Y tồn 13 Cái, có ĐVT Thùng x12.'], OPEN + ['Ở dòng Y chọn ĐVT Thùng.'], 'ĐVT: Thùng (x12)',
       ['SL hiện "1.08" (13 ÷ 12 làm tròn 2 số lẻ).'], 189)
S4.add('Hàng 1 ĐVT vẫn có ô chọn', 'P2', PRE, OPEN, '—', ['Dòng Áo khoác ENEOS cột ĐVT là ô chọn chỉ có 1 lựa chọn "Cái.".'], 191)
S4.add('ĐVT giữ khi đổi trang', 'P1', [PRE, '%s nằm ở trang 1.' % HANG2], OPEN + ['Đổi ĐVT ENEO-410-S4136 sang Thùng.', 'Sang trang 2 rồi về trang 1.'], '—',
       ['Dòng ENEO-410-S4136 vẫn ĐVT Thùng, SL 1.', 'Nhấn F5: về ĐVT cơ sở Can 1L.'], [196, 197])
S4.add('Giữ trang và bộ lọc khi thao tác trong bảng', 'P2', [PRE, 'Đang ở trang 3, lọc Thương hiệu ENEOS.'], OPEN + ['Đổi ĐVT 1 dòng, rê chuột tiêu đề cột.'], '—',
       ['Vẫn ở trang 3, giữ bộ lọc.'], 197)

# ============================================================== V. XUẤT DANH SÁCH EXCEL
S5 = Sec(5)
S5.add('Mở cửa sổ xuất Excel', 'P0', PRE, OPEN + ['Bấm Xuất Excel ở đầu khối lọc.'], '—',
       ['Mở cửa sổ "Xuất Excel báo cáo tồn kho tổng hợp theo mặt hàng", Kiểu xuất có Đầy đủ (chọn sẵn) và Ngắn gọn, nút Xuất Excel, Hủy.'], [212, 213, 214])
S5.add('Xuất kiểu Đầy đủ', 'P0', PRE, OPEN + ['Bấm Xuất Excel.', 'Giữ Đầy đủ, bấm Xuất Excel trong cửa sổ.'], 'Kiểu xuất: Đầy đủ',
       ['Tải file "%s"; cửa sổ đóng.' % FILE,
        'Cột: STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn, nhóm Chi tiết (TPE, TPHP, TPV).'], [215, 216, 223, 225])
S5.add('Xuất kiểu Ngắn gọn', 'P0', PRE, OPEN + ['Bấm Xuất Excel.', 'Chọn Ngắn gọn, bấm Xuất Excel.'], 'Kiểu xuất: Ngắn gọn',
       ['File chỉ có STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn.'], [217, 226])
S5.add('Không có bước chọn trường', 'P2', PRE, OPEN + ['Bấm Xuất Excel.'], '—', ['Cửa sổ không có danh sách chọn cột; luôn xuất đủ cột của kiểu.'], 218)
S5.add('Xuất theo bộ lọc', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231.', 'Xuất Excel kiểu Đầy đủ.'], '—',
       ['File chỉ có 1 mặt hàng: SL tồn 47, TPHP 47.'], [219, 220])
S5.add('Xuất mọi trang', 'P0', PRE, OPEN + ['Đang ở trang 1 (20 mặt hàng), xuất kiểu Ngắn gọn.'], '—',
       ['File có đủ 96 mặt hàng (không riêng trang đang xem).'], [221, 227])
S5.add('Xuất khi báo cáo rỗng', 'P1', [PRE, 'Kho KĐN-ALM, NM không còn tồn.'], OPEN + ['Chỉ giữ kho KĐN-ALM, NM.', 'Xuất Excel kiểu Đầy đủ.'], '—',
       ['Vẫn tải file: letterhead, tiêu đề, Tính đến ngày, Kho, hàng tên cột, dòng "Không có dữ liệu", khối ký.'], 222)
S5.add('Chưa chọn kho thì không xuất', 'P1', PRE, OPEN + ['Bỏ tích Xem toàn bộ kho.', 'Bấm Xuất Excel.'], '—',
       ['Không mở cửa sổ; ô Kho chữ đỏ "Vui lòng chọn kho".'], 222)
S5.add('Định dạng file', 'P1', PRE, OPEN + ['Xuất kiểu Đầy đủ, mở file.'], '—',
       ['File .xlsx mở được; dòng 1 letterhead công ty CN Hải Phòng; tiêu đề "BÁO CÁO TỒN KHO TỔNG HỢP THEO MẶT HÀNG"; "Tính đến ngày: 07/11/2026"; '
        '"Kho: CB - Cát Bà, HP - Hải Phòng, KĐN-ALM - Kho gửi tại Đồng Nai, NM - Nhà máy".',
        'Bảng 2 tầng tiêu đề (Chi tiết); cuối file khối ký Trưởng kho, Người lập báo cáo kèm ngày.'], 224)
S5.add('Dữ liệu khớp màn hình', 'P0', PRE_H, OPEN + ['Xuất kiểu Đầy đủ, tìm ENEO-700-V5231 trong file.'], '—',
       ['Tên, Model, Mã, Thương hiệu, ĐVT "Xô 18L", SL tồn 47, TPHP 47 khớp màn.'], 228)
S5.add('Số là ô số, theo ĐVT đã chọn', 'P1', [PRE, '%s; trên màn đã đổi ĐVT sang Thùng 24C-1L.' % HANG2], OPEN + ['Xuất kiểu Ngắn gọn, mở file.'], '—',
       ['Hàng ENEO-410-S4136 trong file: ĐVT "Thùng 24C-1L (x24)", SL tồn 1.', 'Ô số có phân cách hàng nghìn, cộng SUM được; số 0 để trống.'], 229)
S5.add('Tiếng Việt và ký tự đặc biệt', 'P2', PRE, OPEN + ['Xuất, mở file.'], '—',
       ['Tên hàng có dấu, ký tự "(", "/", "-" hiển thị đúng, không lỗi phông.'], 230)
S5.add('Hủy xuất', 'P2', PRE, OPEN + ['Bấm Xuất Excel.', 'Bấm Hủy.'], '—', ['Cửa sổ đóng, không tải file; mở lại kiểu về Đầy đủ.'], 212)
S5.add('Đang xuất thì khóa nút', 'P1', 'Tài khoản DNS Admin, công ty TPE (8 kho, 6.157 mặt hàng).', [MENU, 'Xuất Excel kiểu Đầy đủ, bấm liên tục 2 lần.'], '—',
       ['Nút đổi chữ "Đang xuất…", có vòng xoay, không nhận lần bấm thứ 2; chỉ tải 1 file.'], 221)

# ============================================================== VI. IN BÁO CÁO
S6 = Sec(6)
S6.add('Mở cửa sổ In báo cáo', 'P0', PRE, OPEN + ['Bấm In danh sách.'], '—',
       ['Cửa sổ "In báo cáo": kiểu Đầy đủ chọn sẵn, Ngắn gọn; "Chọn cột in" tích sẵn 7 cột (6 cột mặt hàng + Chi tiết theo công ty thuê kho); nút In, Hủy.'], 212)
S6.add('Đổi kiểu in đổi danh sách cột', 'P1', PRE, OPEN + ['Bấm In danh sách.', 'Chọn Ngắn gọn.'], '—',
       ['Danh sách cột còn 6: Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn.'], 213)
S6.add('Bỏ hết cột thì báo lỗi', 'P0', PRE, OPEN + ['Bấm In danh sách.', 'Bỏ tích Chọn tất cả.', 'Bấm In.'], '—',
       ['Chữ đỏ "Vui lòng chọn ít nhất 1 cột để in"; cửa sổ không đóng.'], 218)
S6.add('Xem trước bản in kiểu Đầy đủ', 'P0', PRE, OPEN + ['Bấm In danh sách, bấm In.'], '—',
       ['Mở "Xem trước báo cáo tồn kho tổng hợp theo mặt hàng": letterhead CN Hải Phòng, tiêu đề, Tính đến ngày, Kho, bảng 96 mặt hàng 2 tầng tiêu đề (Chi tiết TPE, TPHP, TPV), khối ký Trưởng kho, Người lập báo cáo.'], [219, 221])
S6.add('In theo cột đã chọn', 'P1', PRE, OPEN + ['Bấm In danh sách.', 'Bỏ tích Model và Thương hiệu, bấm In.'], '—',
       ['Bản xem trước không có cột Model, Thương hiệu; cột STT luôn có.'], 217)
S6.add('Bấm In trên bản xem trước', 'P1', PRE, OPEN + ['Mở xem trước, bấm In.'], '—', ['Hộp thoại in của trình duyệt mở, nội dung đúng bản xem trước.'], 219)
S6.add('Vượt mức in tối đa', 'P1', 'Tài khoản DNS Admin, công ty TPE (8 kho, 6.157 mặt hàng).', [MENU, 'Bấm In danh sách, bấm In.'], '—',
       ['Bản xem trước không có nội dung, hiện "Danh sách có 6157 dòng, vượt mức in tối đa 2.000 dòng nên chưa in được…"; nút In ẩn.'], 221)
S6.add('Chưa chọn kho thì không in', 'P1', PRE, OPEN + ['Bỏ tích Xem toàn bộ kho.', 'Bấm In danh sách.'], '—',
       ['Không mở cửa sổ; ô Kho chữ đỏ "Vui lòng chọn kho".'], 222)
S6.add('Số in theo ĐVT đã chọn', 'P2', [PRE, '%s; trên màn đã đổi ĐVT sang Thùng 24C-1L.' % HANG2], OPEN + ['In kiểu Ngắn gọn.'], '—',
       ['Bản in ghi ĐVT "Thùng 24C-1L (x24)", SL tồn 1.'], 229)
S6.add('Hủy in', 'P2', PRE, OPEN + ['Bấm In danh sách, bấm Hủy.', 'Mở xem trước rồi bấm ×.'], '—', ['Đóng cửa sổ, không in; báo cáo giữ nguyên.'], 196)

# ============================================================== VII. RÀNG BUỘC
S7 = Sec(7)
S7.add('Phiếu điều chuyển kho', 'P0', [PRE_H, 'Hoàn tất phiếu điều chuyển 3 Xô 18L hàng ENEO-700-V5231 từ kho HP sang kho CB (môi trường kiểm thử).'],
       OPEN + ['Chọn hàng ENEO-700-V5231.', 'Lần lượt chỉ giữ kho HP, kho CB, rồi cả 4 kho.'], '—',
       ['Kho HP giảm 3 (17); kho CB tăng 3 (30); cả 4 kho vẫn 47.'], [274, 281, 282])
S7.add('Phiếu điều chuyển vị trí', 'P1', [PRE_H, 'Hoàn tất phiếu điều chuyển vị trí 2 Xô 18L hàng ENEO-700-V5231 từ KHOANG1 sang vị trí khác trong kho HP.'],
       OPEN + ['Chọn hàng ENEO-700-V5231.'], '—',
       ['SL tồn và cột TPHP không đổi (47) — chuyển vị trí trong cùng kho không làm đổi tồn kho.'], [272, 284])
S7.add('Nhập / xuất điều chỉnh kiểm kê', 'P1', [PRE_H, 'Hoàn tất phiếu nhập kho điều chỉnh kiểm kê +1 và phiếu xuất kho điều chỉnh kiểm kê -1 cho hàng này ở kho HP.'],
       OPEN + ['Chọn hàng ENEO-700-V5231 sau mỗi phiếu.'], '—', ['Sau phiếu nhập: 48; sau phiếu xuất: 47.'], 274)
S7.add('Khai báo tồn kho đầu kỳ', 'P1', [PRE, 'Khai báo tồn đầu kỳ 10 Cái hàng Z (chưa từng có ở 4 kho) cho công ty TPHP tại kho HP.'],
       OPEN + ['Chọn hàng Z.'], '—', ['Hàng Z xuất hiện, SL tồn 10, cột TPHP 10.'], 274)
S7.add('Đổi tên hàng ở danh mục', 'P2', [PRE_H, 'Đổi tên hàng ENEO-700-V5231 ở danh mục hàng hóa (môi trường kiểm thử).'], OPEN + ['Chọn hàng ENEO-700-V5231.'], '—',
       ['Báo cáo hiện tên mới, số không đổi.'], [278, 279])
S7.add('Kho ngừng hoạt động không còn trong ô Kho', 'P1', ['Tài khoản DNS Admin.', 'Kho NM - Nhà máy chuyển sang ngừng hoạt động ở danh mục Kho vật lý.'],
       [MENU, 'Chọn công ty CN Hải Phòng, mở ô Kho.'], '—', ['Ô Kho không còn NM; Xem toàn bộ kho chọn 3 kho CB, HP, KĐN-ALM.'], [276, 285])
S7.add('Đổi công ty thuê kho ở danh mục Kho kế toán', 'P2', [PRE, 'Bỏ gắn công ty TPE khỏi kho HP ở danh mục Kho kế toán.'],
       [MENU, CHON_HP], '—', ['Ô Công ty thuê kho không còn TPE (nếu không kho nào khác gắn TPE); nhóm Chi tiết không còn cột TPE.'], [280, 282])
S7.add('Màn chỉ đọc, không làm đổi dữ liệu', 'P0', PRE, OPEN + ['Thao tác lọc, đổi ĐVT, in, xuất nhiều lần.', 'Mở Thẻ kho cùng hàng / kho.'], '—',
       ['Không có chứng từ, tồn kho hay lịch sử nào thay đổi; Thẻ kho giữ nguyên số.'], [268, 270, 285])
S7.add('Đối chiếu với Thẻ kho sau khi lập chứng từ', 'P0', [PRE_H, 'Vừa hoàn tất 1 phiếu nhập và 1 phiếu xuất cho hàng này ở kho HP hôm nay.'],
       ['Mở Thẻ kho kho HP, công ty thuê TPHP, kỳ 01/01–hôm nay, ghi Tồn cuối kỳ.', MENU, CHON_HP, 'Chỉ giữ kho HP, chọn hàng ENEO-700-V5231.'], '—',
       ['Tồn cuối kỳ Thẻ kho = cột TPHP = SL tồn.'], [274, 281])

# ============================================================== VIII. PHÂN QUYỀN
S8 = Sec(8)
S8.add('Quyền theo tổng công ty', 'P0', ACC_T, ['Đăng nhập T.', MENU, 'Mở ô Tồn theo công ty, ô Kho.'], '—',
       ['Ô Tồn theo công ty có mọi công ty đang hoạt động (6 công ty); ô Kho có mọi kho của công ty đang chọn.',
        'Thấy nhóm cột Chi tiết, khối Theo công ty thuê kho; xem, in, xuất được.'], [287, 299])
S8.add('Quyền theo công ty', 'P0', ACC_C, ['Đăng nhập C.', MENU, 'Mở ô Tồn theo công ty, ô Kho.'], '—',
       ['Ô Tồn theo công ty chỉ có CN Hải Phòng; ô Kho có CB, HP, KĐN-ALM, NM (chọn sẵn đủ).',
        'KHÔNG có nhóm cột Chi tiết, khối Theo công ty thuê kho, ô Công ty thuê kho có tồn; SL tồn vẫn đúng như T.'], [287, 299])
S8.add('Quyền theo kho', 'P0', ACC_K, ['Đăng nhập K.', MENU], '—',
       ['Ô Kho chỉ có HP và được chọn sẵn; báo cáo hiện ngay số kho HP; không có nhóm cột Chi tiết.'], [287, 299])
S8.add('In / Xuất kiểu Đầy đủ với quyền không thấy Chi tiết', 'P1', ACC_C, ['Đăng nhập C.', MENU, 'Xuất Excel kiểu Đầy đủ; In kiểu Đầy đủ.'], '—',
       ['File và bản in vẫn có nhóm Chi tiết (TPE, TPHP, TPV) như hệ thống cũ.'], [288, 293])
S8.add('Không có quyền nào', 'P0', ACC_N, ['Đăng nhập N.', MENU], '—',
       ['Mục menu vẫn hiện; mở màn báo "%s".' % NOPERM, 'Ô Tồn theo công ty, Kho rỗng; Xem toàn bộ kho bị khóa; bảng "Chọn công ty để xem báo cáo.", không có số liệu.',
        'Bấm In danh sách / Xuất Excel: chữ đỏ dưới ô thiếu, không ra bản in / file.'], [287, 295])
S8.add('Mở trực tiếp đường dẫn khi thiếu quyền', 'P0', ACC_N, ['Đăng nhập N.', 'Dán đường dẫn màn báo cáo vào thanh địa chỉ.'], '—',
       ['Báo "%s"; bảng "Chọn công ty để xem báo cáo.", không lộ số liệu.' % NOPERM], 296)
S8.add('Kho ngoài phạm vi bị chặn', 'P0', ACC_C, ['Đăng nhập C.', MENU, 'Sửa bộ lọc ghi tạm của trình duyệt cho Kho = PTT (kho công ty TPE), F5.'], '—',
       ['Kho PTT bị bỏ, ô Kho chọn lại đủ kho của CN Hải Phòng; không hiện số kho PTT.'], 299)
S8.add('Không có thao tác ghi', 'P1', ACC_T, ['Đăng nhập T.', MENU, CHON_HP], '—',
       ['Không có nút Thêm mới, Sửa, Xóa, Khóa, Import, Lịch sử ở mọi quyền.'], [289, 290, 291, 292, 294])
S8.add('Đổi quyền giữa thao tác', 'P1', [ACC_C, 'Quản trị gỡ quyền "%s" của C khi C đang mở báo cáo.' % V2], ['C đổi Thương hiệu = ENEOS.'], '—',
       ['Báo "%s"; bảng giữ số cũ, không nạp số mới.' % NOPERM], 298)
S8.add('Có nhiều quyền lấy quyền cao nhất', 'P1', 'Tài khoản M: có cả "%s" và "%s".' % (V2, V3), ['Đăng nhập M.', MENU, 'Mở ô Kho.'], '—',
       ['Ô Kho có mọi kho của công ty M (theo quyền công ty), không chỉ kho M là thủ kho.'], 299)
S8.add('Super admin', 'P2', 'Tài khoản DNS Admin (Super admin), không gán 3 quyền.', ['Đăng nhập DNS Admin.', MENU], '—',
       ['Như quyền tổng công ty: chọn được mọi công ty, mọi kho, thấy nhóm cột Chi tiết.'], 287)
S8.add('Quyền theo kho không là thủ kho kho nào', 'P2', 'Tài khoản K2: có quyền "%s", chưa là thủ kho kho nào.' % V3, ['Đăng nhập K2.', MENU], '—',
       ['Ô Kho rỗng, Xem toàn bộ kho bị khóa; bảng "%s".' % CHONKHO], 299)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'SỐ LIỆU BÁO CÁO', S3),
    ('IV', 'XEM CHI TIẾT THEO CÔNG TY THUÊ KHO VÀ ĐVT', S4),
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
                feature_name='Báo cáo tồn kho tổng hợp theo mặt hàng - Cập nhật ngày 07/11/2026',
                module_name='Báo cáo tồn kho tổng hợp theo mặt hàng', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='bao_cao')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

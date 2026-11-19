# -*- coding: utf-8 -*-
"""Testcase màn "Tổng hợp xuất nhập tồn" (phân hệ Kho › Báo cáo kho) — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026
(tc_chuan.build_chuan, loai='bao_cao').

Chạy: python gen_testcase.py -> testcase.xlsx (sau đó chạy check_tc ... bao_cao, phải 0 lỗi).
Loại 'bao_cao' (đọc code 09/11/2026): màn chỉ đọc, chỉ có lấy dữ liệu (xem / danh mục / cây vị trí / in / xuất). Nhóm có mặt: I Hiển thị ·
II Tìm kiếm & lọc (gồm Lọc Nhà / Dãy / Khoang / Vị trí, Cài đặt bộ lọc, Chọn hàng hóa) · III Số liệu báo cáo (đối soát) · IV Xem chi tiết
(đổi ĐVT trong bảng) · V Xuất danh sách Excel · VI In báo cáo · VII Ràng buộc · VIII Phân quyền. Không có Tùy chỉnh cột > bỏ nhóm.
Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../bao-cao-ton-kho-tong-hop-mat-hang/gen_testcase.py (07/11, check_tc 0 lỗi).
Nguồn hành vi: FE pages/warehouse/change-summary-report/** + ScopePicker; BE Modules/Finance ChangeSummaryReport* + WarehouseStockReportService.
Số liệu mẫu dev-hrm 09/11/2026 (DNS Admin, _capture/doisoat.js + probe_scope.js, chỉ đọc): xem docstring gen_srs.py.
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
MENU = 'Vào phân hệ Kho > menu "Báo cáo kho" > bấm "Tổng hợp xuất nhập tồn".'
CN = 'CN HẢI PHÒNG - CÔNG TY CP CÔNG NGHỆ THIẾT BỊ TÂN PHÁT'
CHON_HP = 'Chọn Tồn theo công ty = "%s" (hệ thống tự chọn đủ 4 kho CB, HP, KĐN-ALM, NM).' % CN
V1 = 'Xem báo cáo tồn kho theo tổng công ty'
V2 = 'Xem báo cáo tồn kho theo công ty'
V3 = 'Xem báo cáo tồn kho theo kho'
NOPERM = 'Bạn không có quyền truy cập chức năng này.'
EMPTY = 'Không có mặt hàng nào khớp bộ lọc.'
CHONKHO = 'Chọn kho để xem báo cáo.'
CHONNGAY = 'Chọn đủ từ ngày và đến ngày để xem báo cáo.'
FILE = 'bao_cao_tong_hop_xuat_nhap_ton_kho.xlsx'
HANG = 'hàng "Dầu nhớt động cơ Diesel 4 kỳ SAE 20W-50 CF-4 (18L)" (mã ENEO-700-V5231, ĐVT Xô 18L)'
HANG2 = 'hàng ENEO-410-S4136 "Dầu bôi trơn hộp số tự động tổng hợp Eneos ATF Multi (Chai 1 lít)", ĐVT Can 1L và Thùng 24C-1L (x24)'
HANG3 = 'hàng ENEO-640-V5236 "Dầu nhớt bán tổng hợp động cơ ô tô 4 kỳ SP/CF SAE 5W-30 (4Lx6)", ĐVT cơ sở Can 4L'
PRE = ('Tài khoản DNS Admin (Super admin, coi như có quyền "%s"), hôm nay 09/11/2026.\n'
       'Công ty %s có 4 kho CB, HP, KĐN-ALM, NM; kỳ Năm nay có 217 mặt hàng có phát sinh (102 có tồn đầu kỳ, 187 có nhập, 200 có xuất, '
       '96 còn tồn cuối kỳ).' % (V1, CN))
PRE_H = PRE + ('\n%s: kho HP năm 2026 Tồn đầu kỳ 70, Nhập 496, Xuất 546, Tồn cuối kỳ 20; kho CB Nhập 27, Tồn cuối kỳ 27; hàng nằm ở vị trí '
               'KHOANG1 (Tầng 1 > Dãy 1 > Khoang 1) kho HP, công ty thuê TPHP.' % HANG)
OPEN = [MENU, CHON_HP]
TPE = 'Tài khoản DNS Admin, công ty TPE (8 kho CSKH, DATD, KTCN, LN, N10, N9, PTT, SL), kỳ Năm nay: 8.441 mặt hàng có phát sinh.'
ACC_C = 'Tài khoản C: thuộc công ty CN Hải Phòng, chỉ có quyền "%s".' % V2
ACC_K = 'Tài khoản K: thuộc công ty CN Hải Phòng, chỉ có quyền "%s", là thủ kho của kho HP - Hải Phòng (không là thủ kho kho khác).' % V3
ACC_T = 'Tài khoản T: có quyền "%s", thuộc công ty TPE.' % V1
ACC_N = 'Tài khoản N: không có quyền nào trong 3 quyền xem báo cáo tồn kho.'
HP_HANG = ['Bỏ kho CB, KĐN-ALM, NM ở ô Kho (còn HP).', 'Chọn hàng ENEO-700-V5231 ở ô Hàng hóa.']

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
     'Xem, với từng mặt hàng trên MỘT HOẶC NHIỀU kho (hoặc một phần kho theo Nhà / Dãy / Khoang / Vị trí) của một công ty, trong một kỳ: '
     'Tồn đầu kỳ, Nhập trong kỳ, Xuất trong kỳ, Tồn cuối kỳ. Màn chỉ đọc: không thêm / sửa / xóa; có In (2 kiểu, chọn cột) và Xuất Excel '
     '(2 kiểu).'),
    ('2. Đối tượng được tính / hiển thị',
     '- Mặt hàng có ít nhất 1 trong 3 số Tồn đầu kỳ / Nhập / Xuất khác 0 tại các vị trí đang xét, công ty thuê đang lọc.\n'
     '- Nguồn số: mọi chứng từ kho đã ghi tồn theo vị trí (tồn đầu kỳ, nhập kho, nhập lại, xuất kho, xuất điều chỉnh sai số liệu, nhập / '
     'xuất điều chỉnh kiểm kê, điều chuyển vị trí).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Mặt hàng không có tồn đầu kỳ, không nhập, không xuất trong kỳ.\n- Thay đổi tồn sau ngày cuối kỳ.\n'
     '- Phiếu điều chuyển vị trí khi chọn Loại báo cáo "Không nhặt phiếu điều chuyển".\n'
     '- Kho ngoài phạm vi quyền, kho khác công ty đang xem, kho ngừng hoạt động, công ty thuê không gắn với các kho đang chọn.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô Kỳ (mặc định Năm nay; Tuần này, Tháng này, Năm trước, Tuỳ chọn): Tồn đầu kỳ cộng mọi thay đổi trước ngày đầu kỳ; Nhập / Xuất cộng '
     'trong kỳ tới hết ngày cuối kỳ.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Bảng phẳng: dòng TỔNG > mỗi mặt hàng 1 dòng (STT 1, 2…). Cột: STT, Tên hàng, Model, Mã hàng, Thương hiệu, Đơn vị, Tồn đầu kỳ, Nhập '
     'trong kỳ, Xuất trong kỳ, Tồn cuối kỳ. Phân trang theo mặt hàng (mặc định 20).'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Tồn cuối kỳ = Tồn đầu kỳ + Nhập - Xuất.\n- Nhiều kho / nhiều vị trí / nhiều công ty thuê: 1 mặt hàng vẫn 1 dòng, số = tổng.\n'
     '- Chuyển hàng giữa 2 vị trí (cùng kho) tính cả Nhập và Xuất khi Loại báo cáo = Tất cả.'),
    ('7. Phân quyền cấp',
     '- %s: chọn mọi công ty, mọi kho (Super admin coi như có quyền này).\n- %s: công ty mình, kho của công ty mình.\n'
     '- %s: công ty mình, chỉ kho mình là thủ kho.\n- Không có quyền nào: không xem được, báo "%s".' % (V1, V2, V3, NOPERM)),
    ('8. Cách tính các ô thống kê',
     '- Ô Mặt hàng có phát sinh = dòng TỔNG = N ở "Hiển thị a–b / N mặt hàng".\n- Ô Kho đang xem = số kho đang chọn.\n'
     '- 4 ô Có tồn đầu kỳ / Có nhập / Có xuất / Còn tồn cuối kỳ = số mặt hàng có cột tương ứng khác 0; ô bằng 0 thì ẩn.\n'
     '- Đối soát: 4 số của 1 hàng / 1 kho / 1 công ty thuê = khối Số lượng của Thẻ kho cùng kỳ; Tồn cuối kỳ = SL tồn của Báo cáo tồn kho '
     'tổng hợp theo mặt hàng.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản: DNS Admin (Super admin), T (tổng công ty), C (theo công ty), K (theo kho), N (không quyền).\n'
     '- Lưu ý: số trên màn quy đổi theo ĐVT chọn ở từng hàng; số 0 để ô trống; cột Xuất hiện số dương.\n'
     '- Lưu ý: lọc Nhà / Dãy / Khoang / Vị trí giữ như hệ thống cũ — tick Nhà / Dãy / Khoang mà không tick Vị trí thì không thu hẹp; có '
     'tick Vị trí thì kho không tick gì bị bỏ (đúng thiết kế, không phải lỗi).\n'
     '- Lưu ý: màn không có ô tìm nhanh, không có ô Hợp đồng, không sắp xếp theo cột; tìm bằng chữ chỉ có ở ô tìm của 4 cột vị trí.\n'
     '- Lưu ý: dev 09/11 cửa sổ Chọn hàng hóa báo không tải được danh sách hàng khi Tồn theo công ty khác công ty đăng nhập (TC_02.050 — '
     'đã báo, chờ xử lý, giống các báo cáo tồn kho khác).'),
]

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', 'Tài khoản DNS Admin, công ty TPE, chưa mở màn trong 10 phút qua.', [MENU], '—',
       ['Mở màn "Tổng hợp xuất nhập tồn".',
        'Kỳ = Năm nay, Loại báo cáo = Tất cả, Tồn theo công ty = công ty TPE, ô Xem toàn bộ kho được tích, Kho có đủ 8 kho của công ty TPE.',
        'Báo cáo tự hiện: dòng tóm tắt "Xuất nhập tồn năm 2026 (01/01/2026 – 31/12/2026)", "Hiển thị 1–20 / 8441 mặt hàng", không báo lỗi.'], [1, 36])
S1.add('Mục cùng tên ở menu Tài chính không phải lối vào', 'P2', 'Tài khoản DNS Admin.',
       ['Vào phân hệ Tài chính, tìm mục "Tổng hợp xuất nhập tồn" trong nhóm báo cáo hàng tồn kho.', 'Bấm mục đó.'], '—',
       ['Mục hiện màu xám (đang phát triển), bấm không mở màn nào — đây là báo cáo kế toán khác, chưa chuyển; lối vào duy nhất là phân hệ Kho.'], 1)
S1.add('Tiêu đề màn hình', 'P1', PRE, [MENU, 'Quan sát thanh tiêu đề và tab trình duyệt.'], '—',
       ['Cả 2 nơi là "Tổng hợp xuất nhập tồn"; khối lọc có tiêu đề "Bộ lọc tổng hợp xuất nhập tồn".'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE, OPEN + ['Quan sát khối lọc và bảng.'], '—',
       ['Đầu khối lọc: In danh sách, Xuất Excel, Cài đặt bộ lọc, Ẩn tìm kiếm nâng cao.', 'Dưới các ô lọc: Tìm kiếm, Xóa lọc.',
        'Dòng tóm tắt có nút Thu gọn.', 'KHÔNG có nút Tạo mới, Sửa, Xóa, Import, Lịch sử.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', PRE, OPEN + ['Đọc tiêu đề cột.'], '—',
       ['10 cột: STT, Tên hàng, Model, Mã hàng, Thương hiệu, Đơn vị, Tồn đầu kỳ, Nhập trong kỳ, Xuất trong kỳ, Tồn cuối kỳ.',
        'Cột Đơn vị và 4 cột số có biểu tượng chữ i.'], 4)
S1.add('Không có cột ẩn và không có tùy chỉnh cột', 'P2', PRE, OPEN + ['Tìm nút cấu hình cột trên bảng.'], '—',
       ['Không có nút cấu hình cột; bảng luôn đủ 10 cột.'], 5)
S1.add('Dữ liệu dòng mặt hàng đúng', 'P0', PRE, OPEN, '—',
       ['Dòng 1: Áo khoác ENEOS, Model AOKHOAC, Mã ENEO-AOKHOAC:01, ENEOS, Cái., Tồn đầu kỳ 93, Nhập trống, Xuất 50, Tồn cuối kỳ 43.',
        'Dòng 4: Áo phông ENEOS 247, 54, 175, 126.', 'Số 0 để ô trống; dòng báo cáo không có trạng thái Khóa / Hoạt động.'], [6, 7])
S1.add('Hàng nhập rồi xuất hết trong kỳ vẫn hiện', 'P0', PRE, OPEN, '—',
       ['Dòng 5 Ba lô ENEOS: Tồn đầu kỳ 2, Xuất 2, Tồn cuối kỳ trống.', 'Dòng 8 "Bộ bơm và xy lanh kết hợp…": Nhập 1, Xuất 1, Tồn đầu và Tồn cuối trống.'], 7)
S1.add('Kho không có phát sinh', 'P1', [PRE, 'Kho KĐN-ALM và NM không có hàng.'], OPEN + ['Bỏ kho CB và HP ở ô Kho (còn KĐN-ALM, NM).'],
       'Kho: KĐN-ALM, NM', ['Khối Mặt hàng có phát sinh 0; bảng hiện "%s"; ẩn phân trang; không báo lỗi.' % EMPTY], 8)
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231.', 'Bỏ TPHP, TPV ở Công ty thuê kho (còn TPE).'],
       'Công ty thuê kho: TPE', ['Bảng hiện "%s"; khối tổng hợp Mặt hàng có phát sinh 0.' % EMPTY], [9, 40])
S1.add('Số mặt hàng mặc định mỗi trang', 'P0', PRE, OPEN, '—',
       ['Trang 1 có 20 mặt hàng (STT 1 đến 20); dưới bảng "Hiển thị 1–20 / 217 mặt hàng"; Số dòng/trang = 20.'], [10, 16])
S1.add('Thay đổi số dòng / trang', 'P0', PRE, OPEN + ['Sang trang 2.', 'Đổi Số dòng/trang thành 50.'], 'Số dòng/trang: 50',
       ['Bảng hiện 50 mặt hàng, về trang 1, "Hiển thị 1–50 / 217 mặt hàng".', 'Lựa chọn có 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P1', PRE, OPEN + ['Bấm ›.', 'Bấm ‹.'], '—',
       ['Bấm › sang trang 2: "Hiển thị 21–40 / 217", STT từ 21.', 'Bấm ‹ về trang 1.'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE, OPEN + ['Bấm ».', 'Bấm «.'], '—',
       ['Bấm » tới trang 11: "Hiển thị 201–217 / 217 mặt hàng".', 'Bấm « về trang 1.'], 13)
S1.add('Trạng thái nút ở trang đầu / cuối', 'P2', PRE, OPEN + ['Quan sát nút ở trang 1, rồi ở trang 11.'], '—',
       ['Trang 1: nút « ‹ mờ, không bấm được.', 'Trang 11: nút › » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P1', PRE, OPEN + ['Sang trang 2.'], '—', ['Mặt hàng đầu trang 2 có STT 21 (nối tiếp trang 1).'], 15)
S1.add('Về trang 1 khi đổi bộ lọc', 'P1', PRE, OPEN + ['Sang trang 3.', 'Chọn Thương hiệu = ENEOS.'], 'Thương hiệu: ENEOS',
       ['Báo cáo nạp lại từ trang 1; tổng N cập nhật theo bộ lọc.'], [17, 42])
S1.add('Thứ tự mặc định theo tên hàng', 'P0', PRE, OPEN, '—',
       ['Mặt hàng xếp theo tên A đến Z: 1 Áo khoác ENEOS, 2 Áo mưa ENEOS, 3 Áo phông cao cấp ENEOS, 4 Áo phông ENEOS, 5 Ba lô ENEOS, 6 BIA 333…'], 19)
S1.add('Không sắp xếp theo cột', 'P2', PRE, OPEN + ['Bấm tiêu đề cột Mã hàng, Tồn đầu kỳ, Tồn cuối kỳ.'], '—',
       ['Thứ tự không đổi (luôn theo tên hàng); tiêu đề cột không có biểu tượng sắp xếp.'], [20, 21, 22, 23])
S1.add('Giữ thứ tự khi chuyển trang', 'P2', PRE, OPEN + ['Sang trang 2, quay lại trang 1.'], '—',
       ['Trang 2 tiếp tục thứ tự tên hàng; quay lại trang 1 đúng 20 mặt hàng như lúc đầu.'], 24)
S1.add('Thu gọn / mở rộng khối tổng hợp', 'P2', PRE, OPEN + ['Bấm Thu gọn.', 'Bấm Mở rộng.'], '—',
       ['Thu gọn: ẩn các ô Mặt hàng, Phát sinh, còn dòng tóm tắt; chữ nút "Mở rộng".', 'Mở rộng: hiện lại, số không đổi.'], 3)
S1.add('Dòng tóm tắt báo cáo', 'P1', PRE, OPEN + ['Rê chuột vào phần "Kho:" và vào chữ i cạnh dòng tóm tắt.'], '—',
       ['Dòng "Xuất nhập tồn năm 2026 (01/01/2026 – 31/12/2026) · Kho: CB, HP, KĐN-ALM, NM"; rê chuột phần Kho hiện "CB - Cát Bà, HP - Hải '
        'Phòng, KĐN-ALM - Kho gửi tại Đồng Nai, NM - Nhà máy".',
        'Chữ i hiện "TỔNG HỢP XUẤT NHẬP TỒN", dòng cuối "Số liệu tính tại <ngày giờ>".'], 6)
S1.add('Chữ i các cột số', 'P2', PRE, OPEN + ['Rê chuột vào chữ i ở tiêu đề Tồn đầu kỳ, Nhập, Xuất, Tồn cuối kỳ.'], '—',
       ['Tồn đầu kỳ: "Tồn tại các vị trí đang xét, trước ngày đầu kỳ".',
        'Nhập / Xuất: "Cộng các lần tăng / giảm tồn tại vị trí trong kỳ (kể cả điều chuyển vào / ra, trừ khi chọn "Không nhặt phiếu điều chuyển")".',
        'Tồn cuối kỳ: "Tồn đầu kỳ + Nhập trong kỳ - Xuất trong kỳ".'], 4)
S1.add('Bảng rộng cuộn ngang, tiêu đề dính', 'P2', PRE, OPEN + ['Ở màn hình rộng 1440px, cuộn bảng xuống và sang phải.'], '—',
       ['Tiêu đề cột dính trên cùng khi cuộn xuống; bảng cuộn ngang để thấy cột Tồn cuối kỳ, trang không vỡ.'], 4)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Ô tìm cột vị trí: khớp chính xác', 'P1', PRE, OPEN + ['Ở cột Nhà, gõ "TANG1" vào ô "Tìm theo mã hoặc tên nhà".'], 'Ô tìm Nhà: TANG1',
       ['Cột Nhà chỉ còn "TANG1 - Tầng 1" (nhóm HP).', 'Báo cáo không đổi (ô tìm chỉ lọc danh sách trong cột).'], [26, 35])
S2.add('Ô tìm cột vị trí: khớp một phần', 'P1', PRE, OPEN + ['Ở cột Nhà, gõ "ANG".'], 'Ô tìm Nhà: ANG',
       ['Còn các nhà có mã / tên chứa "ang": TANG1 - Tầng 1, TANG2 - Tầng 2.'], 27)
S2.add('Ô tìm cột vị trí: không phân biệt hoa / thường', 'P2', PRE, OPEN + ['Ở cột Nhà, gõ "tầng 1".'], 'Ô tìm Nhà: tầng 1',
       ['Kết quả như gõ "Tầng 1": còn TANG1 - Tầng 1.'], 28)
S2.add('Ô tìm cột vị trí: có dấu / không dấu', 'P2', PRE, OPEN + ['Ở cột Nhà, gõ "tang 1".'], 'Ô tìm Nhà: tang 1',
       ['Không còn nhà nào (hệ thống phân biệt "tang" và "tầng"); cột hiện "Không có dữ liệu".'], 29)
S2.add('Ô tìm cột vị trí: không tồn tại', 'P2', PRE, OPEN + ['Ở cột Vị trí, gõ "ZZZ999".'], 'Ô tìm Vị trí: ZZZ999',
       ['Cột Vị trí không còn dòng nào; ô Chọn hết của cột bị khóa; báo cáo không đổi.'], 30)
S2.add('Ô tìm cột vị trí: ký tự đặc biệt', 'P2', PRE, OPEN + ['Ở cột Vị trí, gõ "%", rồi "_", rồi "<script>".'],
       ['Ô tìm Vị trí: %', 'Ô tìm Vị trí: _', 'Ô tìm Vị trí: <script>'],
       ['"%": không còn dòng (hiểu theo nghĩa đen).', '"_": còn các vị trí có dấu gạch dưới trong mã / tên (nếu có).',
        '"<script>": không còn dòng, không lỗi, không chạy mã.'], 31)
S2.add('Ô tìm cột vị trí: khoảng trắng đầu / cuối', 'P2', PRE, OPEN + ['Ở cột Nhà, gõ "  TANG1  ".'], 'Ô tìm Nhà: "  TANG1  "',
       ['Kết quả như gõ "TANG1" (tự bỏ khoảng trắng đầu / cuối).'], 32)
S2.add('Ô tìm cột vị trí: không giới hạn ký tự', 'P2', PRE, OPEN + ['Ở cột Nhà, gõ chuỗi 300 ký tự "A".'], 'Ô tìm Nhà: 300 ký tự',
       ['Ô nhận đủ, không báo lỗi; cột Nhà không còn dòng.'], 33)
S2.add('Ô tìm cột vị trí: xóa nhanh', 'P1', [PRE, 'Ô tìm cột Nhà đang có "TANG1".'], OPEN + ['Bấm dấu × trong ô tìm.'], '—',
       ['Ô tìm trống, cột Nhà hiện lại đủ nhà của 4 kho; các tick giữ nguyên.'], 34)
S2.add('Ô tìm cột vị trí lọc ngay khi gõ', 'P2', PRE, OPEN + ['Gõ "TANG" vào ô tìm cột Nhà, không nhấn Enter.'], 'Ô tìm Nhà: TANG',
       ['Danh sách cột lọc ngay khi gõ, không cần Enter hay Tìm kiếm.'], 35)
S2.add('Giá trị mặc định của bộ lọc', 'P0', 'Tài khoản DNS Admin công ty TPE, chưa mở màn trong 10 phút.', [MENU], '—',
       ['Kỳ = Năm nay; Loại báo cáo = Tất cả; Tồn theo công ty = công ty TPE; Xem toàn bộ kho tích; Kho = 8 kho CSKH, DATD, KTCN, LN, N10, N9, '
        'PTT, SL; Công ty thuê kho = mọi công ty thuê của các kho; Tính chất, Loại, Thương hiệu, Hãng sản xuất, Nhóm, Hàng hóa trống; không tick '
        'Nhà / Dãy / Khoang / Vị trí; khối lọc mở sẵn.'], 36)
S2.add('Lọc Kỳ = Tháng này / Tuần này', 'P1', PRE_H, OPEN + HP_HANG + ['Đổi Kỳ = Tháng này.', 'Đổi Kỳ = Tuần này.'], ['Kỳ: Tháng này', 'Kỳ: Tuần này'],
       ['Tháng này: dòng tóm tắt "Xuất nhập tồn tháng 11/2026 (01/11/2026 – 30/11/2026)"; Tồn đầu kỳ 20, Nhập, Xuất trống, Tồn cuối kỳ 20.',
        'Tuần này: "(09/11/2026 – 15/11/2026)" (thứ Hai đến Chủ nhật), cùng số 20.'], 37)
S2.add('Lọc Kỳ = Năm trước', 'P0', PRE_H, OPEN + HP_HANG + ['Đổi Kỳ = Năm trước.'], 'Kỳ: Năm trước',
       ['Dòng tóm tắt "Xuất nhập tồn năm 2025 (01/01/2025 – 31/12/2025)".', 'Tồn đầu kỳ trống, Nhập 265, Xuất 195, Tồn cuối kỳ 70.'], 37)
S2.add('Lọc Kỳ = Tuỳ chọn', 'P0', PRE, OPEN + ['Đổi Kỳ = Tuỳ chọn.', 'Chọn Thời gian 01/10/2026 – 31/10/2026.'], 'Thời gian: 01/10/2026 – 31/10/2026',
       ['Sau bước 3: ô Thời gian hiện ngay sau ô Kỳ; bảng "%s", chưa tính.' % CHONNGAY,
        'Sau bước 4: dòng tóm tắt "Xuất nhập tồn từ 01/10/2026 đến 31/10/2026"; 109 mặt hàng (95 có tồn đầu, 36 có nhập, 48 có xuất, 96 còn tồn cuối).'], 37)
S2.add('Tuỳ chọn thiếu ngày thì báo đỏ', 'P0', PRE, OPEN + ['Đổi Kỳ = Tuỳ chọn.', 'Bấm Tìm kiếm.'], '—',
       ['Ô Thời gian viền đỏ, chữ "Vui lòng chọn đủ từ ngày và đến ngày"; không nạp báo cáo.'], [36, 37])
S2.add('Tuỳ chọn đến ngày trước từ ngày', 'P1', PRE, OPEN + ['Đổi Kỳ = Tuỳ chọn.', 'Chọn Từ ngày 01/05/2026, Đến ngày 01/01/2026.'], 'Thời gian: 01/05/2026 – 01/01/2026',
       ['Báo "Ngày kết thúc phải sau hoặc bằng ngày bắt đầu" (hoặc ô ngày không cho chọn ngược); không ra số liệu.'], 37)
S2.add('Đổi Kỳ khác Tuỳ chọn thì xóa khoảng ngày', 'P2', [PRE, 'Đang Tuỳ chọn 01/10/2026 – 31/10/2026.'], OPEN + ['Đổi Kỳ = Năm nay.'], '—',
       ['Ô Thời gian ẩn, khoảng ngày bị xóa; báo cáo về năm 2026 (217 mặt hàng).'], 37)
S2.add('Lọc Loại báo cáo = Không nhặt phiếu điều chuyển', 'P0', ['Tài khoản DNS Admin, công ty TPE.', HANG3 + ' kho PTT năm 2026 có 10 phiếu điều chuyển vị trí.'],
       [MENU, 'Chỉ giữ kho PTT, chọn hàng ENEO-640-V5236.', 'Đổi Loại báo cáo = Không nhặt phiếu điều chuyển.'], 'Loại báo cáo: Không nhặt phiếu điều chuyển',
       ['Tất cả: 15,141 / 11,404 / 23,348 / 3,197.', 'Không nhặt phiếu điều chuyển: 15,141 / 7,435 / 19,379 / 3,197 (Nhập và Xuất cùng giảm 3,969, tồn cuối không đổi).'], [37, 38])
S2.add('Bỏ tích Xem toàn bộ kho', 'P0', PRE, OPEN + ['Bỏ tích Xem toàn bộ kho.'], '—',
       ['Ô Kho và Công ty thuê kho về trống; 4 cột Nhà / Dãy / Khoang / Vị trí ẩn; bảng "%s"; không báo lỗi.' % CHONKHO], [36, 37])
S2.add('Tích lại Xem toàn bộ kho', 'P1', [PRE, 'Ô Kho đang trống.'], OPEN + ['Bỏ tích rồi tích lại Xem toàn bộ kho.'], '—',
       ['Ô Kho có lại đủ 4 kho; Công ty thuê kho tích TPE, TPHP, TPV; báo cáo nạp lại 217 mặt hàng.'], 37)
S2.add('Bỏ 1 kho thì ô Xem toàn bộ kho tự bỏ tích', 'P1', PRE, OPEN + ['Bấm × ở chip NM trong ô Kho.'], 'Kho: CB, HP, KĐN-ALM',
       ['Ô Xem toàn bộ kho tự bỏ tích; báo cáo nạp lại với 3 kho, dòng tóm tắt "Kho: CB, HP, KĐN-ALM".'], 37)
S2.add('Thiếu Kho thì báo đỏ', 'P0', PRE, OPEN + ['Bỏ tích Xem toàn bộ kho.', 'Bấm Tìm kiếm.'], '—',
       ['Ô Kho viền đỏ, chữ "Vui lòng chọn kho"; không nạp báo cáo; bảng "%s".' % CHONKHO, 'Chọn lại 1 kho: chữ đỏ tự tắt.'], [36, 37])
S2.add('Đổi Tồn theo công ty chọn lại hết kho', 'P1', PRE, OPEN + ['Đổi Tồn theo công ty sang công ty TPE.'], '—',
       ['Ô Kho tự chọn đủ 8 kho của công ty TPE, Xem toàn bộ kho tích; Công ty thuê kho tích mọi công ty thuê của 8 kho; báo cáo nạp lại 8.441.'], 37)
S2.add('Đổi Kho tự chọn công ty thuê kho và xóa tick vị trí', 'P0', [PRE, 'Đang tick Nhà TANG1 của kho HP.'], OPEN + ['Bỏ kho HP, KĐN-ALM, NM (còn CB).'], 'Kho: CB',
       ['Ô Công ty thuê kho chỉ còn công ty thuê của kho CB, tự tích; các tick vị trí bị xóa, cột Nhà chỉ còn nhà kho CB; báo cáo nạp ngay.'], 37)
S2.add('Lọc Công ty thuê kho', 'P0', PRE_H, OPEN + ['Chỉ giữ kho HP.', 'Bỏ TPE và TPV ở Công ty thuê kho (còn TPHP).'], 'Công ty thuê kho: TPHP',
       ['Hàng ENEO-700-V5231 vẫn 70 / 496 / 546 / 20 (toàn bộ thuộc TPHP).', 'Chỉ còn TPE: hàng không xuất hiện.'], 37)
S2.add('Bỏ trống Công ty thuê kho', 'P1', PRE, OPEN + ['Bỏ hết công ty ở ô Công ty thuê kho.'], '—',
       ['Báo cáo tính mọi công ty thuê của các kho: vẫn 217 mặt hàng.'], 37)
S2.add('Lọc Tính chất, Loại, Hãng sản xuất, Nhóm', 'P1', PRE, OPEN + ['Lần lượt chọn 1 giá trị ở từng ô, sau mỗi ô bỏ chọn.'], '—',
       ['Mỗi lần chỉ còn mặt hàng thuộc giá trị đã chọn; bỏ chọn trở lại 217.', 'Loại hàng hóa: hàng thuộc ít nhất 1 loại đã chọn.'], 37)
S2.add('Lọc Thương hiệu', 'P1', PRE, OPEN + ['Chọn Thương hiệu = ENEOS.'], 'Thương hiệu: ENEOS', ['Mọi dòng có Thương hiệu ENEOS.'], 37)
S2.add('Kết hợp nhiều ô lọc', 'P0', PRE_H, OPEN + ['Chọn Thương hiệu = ENEOS.', 'Chọn hàng ENEO-700-V5231.'], ['Thương hiệu: ENEOS', 'Hàng hóa: ENEO-700-V5231'],
       ['Chỉ còn 1 mặt hàng thỏa CẢ 2 điều kiện (70 / 523 / 546 / 47 trên 4 kho).', 'Chọn Thương hiệu khác ENEOS: bảng "%s".' % EMPTY], [38, 39])
S2.add('Tổng và phân trang sau lọc', 'P1', PRE, OPEN + ['Chọn Thương hiệu = ENEOS.'], 'Thương hiệu: ENEOS',
       ['Ô Mặt hàng có phát sinh = dòng TỔNG = N ở "Hiển thị 1–x / N"; số trang tính lại theo N.'], [41, 42])
S2.add('Thứ tự sau lọc', 'P2', PRE, OPEN + ['Chọn Thương hiệu = ENEOS.'], '—', ['Kết quả vẫn xếp theo tên hàng A đến Z.'], 43)
S2.add('Xóa lọc', 'P0', [PRE, 'Đang lọc công ty CN Hải Phòng, chỉ kho HP, Kỳ Tuỳ chọn, Không nhặt phiếu điều chuyển, Thương hiệu ENEOS, tick Nhà TANG1.'],
       OPEN + ['Bấm Xóa lọc.'], '—',
       ['Kỳ về Năm nay, Loại báo cáo Tất cả, Tồn theo công ty về công ty của tài khoản (TPE), Kho đủ 8 kho, các ô khác trống (kể cả Hàng hóa, tick vị trí).',
        'Báo cáo nạp lại trang 1; chữ đỏ biến mất.'], 44)
S2.add('Chuyển màn rồi quay lại', 'P1', [PRE, 'Đang lọc công ty CN Hải Phòng.'], OPEN + ['Mở màn Thẻ kho.', MENU], '—',
       ['Bộ lọc về mặc định (công ty của tài khoản, toàn bộ kho, Năm nay).'], 45)
S2.add('Tải lại trang (F5)', 'P0', [PRE, 'Đang lọc công ty CN Hải Phòng, kho HP, hàng ENEO-700-V5231, tick vị trí KHOANG1.'], OPEN + ['Nhấn F5 trong vòng 10 phút.'], '—',
       ['Giữ nguyên công ty, kho HP, ô Hàng hóa vẫn hiện "ENEO-700-V5231 - Dầu nhớt…", tick KHOANG1 giữ nguyên, báo cáo nạp lại.',
        'Sau hơn 10 phút F5: bộ lọc về mặc định.'], 46)
S2.add('Mở tab mới', 'P2', [PRE, 'Đang lọc công ty CN Hải Phòng.'], OPEN + ['Mở màn ở tab mới trong 10 phút.'], '—', ['Tab mới khôi phục bộ lọc CN Hải Phòng.'], 47)
S2.add('Tài khoản khác cùng trình duyệt', 'P2', [PRE, ACC_C, 'DNS Admin vừa lọc công ty CN Hải Phòng rồi đăng xuất (trong 10 phút).'],
       ['Đăng nhập C trên cùng trình duyệt.', MENU], '—',
       ['Nếu bộ lọc ghi tạm còn hạn, C thấy 4 kho được chọn sẵn (thuộc công ty C); kho / công ty ngoài phạm vi của C bị bỏ.'], 48)
S2.add('Lọc vị trí: cây Nhà / Dãy / Khoang / Vị trí', 'P1', PRE, OPEN + ['Quan sát 4 cột dưới các ô lọc.'], '—',
       ['Cột Nhà nhóm theo mã kho CB, HP, KĐN-ALM, NM (mỗi nhà "<mã> - <tên>").', 'Cột Vị trí có "Vị trí tự do · CB / HP / KĐN-ALM / NM".',
        'Cột Dãy, Khoang: "Chưa chọn nhà hoặc không có dữ liệu" / "Chưa chọn dãy hoặc không có dữ liệu".'], 37)
S2.add('Lọc vị trí: tick đến Vị trí thì thu hẹp', 'P0', PRE_H, OPEN + HP_HANG + ['Tick Nhà TANG1 > Dãy D1 > Khoang K1 > Vị trí KHOANG1.'], 'Vị trí: KHOANG1',
       ['Sau mỗi tick báo cáo nạp lại; hàng ENEO-700-V5231 = 70 / 496 / 546 / 20 (hàng chỉ nằm ở KHOANG1).',
        'Tick vị trí khác (vd HP-TACH-GHEP) thay cho KHOANG1: bảng "%s".' % EMPTY], 37)
S2.add('Lọc vị trí: tick Nhà không tick Vị trí thì không thu hẹp', 'P0', PRE_H, OPEN + HP_HANG + ['Tick Nhà N1 - Nhà 1 (không chứa hàng này), không tick Vị trí.'],
       'Nhà: N1', ['Số liệu không đổi: 70 / 496 / 546 / 20 (giữ như hệ thống cũ — chỉ tick Vị trí mới thu hẹp).'], 37)
S2.add('Lọc vị trí: kho không tick bị bỏ khi có tick Vị trí', 'P0', PRE_H,
       OPEN + ['Chỉ giữ kho CB và HP.', 'Chọn hàng ENEO-700-V5231 (70 / 523 / 546 / 47).', 'Tick vị trí KHOANG1 của kho HP (qua TANG1 > D1 > K1).'], '—',
       ['Số liệu còn 70 / 496 / 546 / 20 — kho CB (không tick gì) bị bỏ khỏi báo cáo (giữ như hệ thống cũ).', 'Dòng tóm tắt vẫn ghi "Kho: CB, HP".'], [37, 38])
S2.add('Lọc vị trí: bỏ tick cha tự bỏ tick con', 'P1', [PRE_H, 'Đang tick TANG1 > D1 > K1 > KHOANG1.'], OPEN + ['Bỏ tick Nhà TANG1.'], '—',
       ['Tick D1, K1, KHOANG1 tự bỏ; cột Dãy về "Chưa chọn nhà hoặc không có dữ liệu"; báo cáo về cả kho.'], 37)
S2.add('Lọc vị trí: Chọn hết cột và nhóm', 'P2', PRE, OPEN + ['Bấm Chọn hết ở nhóm HP của cột Nhà.', 'Bấm Chọn hết ở đầu cột Nhà.'], '—',
       ['Nhóm HP: tick đủ N1, TANG1, TANG2.', 'Đầu cột: tick mọi nhà đang hiện; báo cáo không thu hẹp vì chưa tick Vị trí.'], 37)
S2.add('Cài đặt bộ lọc: mở cửa sổ', 'P1', PRE, OPEN + ['Bấm Cài đặt bộ lọc.'], '—',
       ['Cửa sổ "Cài đặt bộ lọc" liệt kê 13 mục có ô tích (Kỳ … Công ty thuê kho, Xem toàn bộ kho, Nhà / Dãy / Khoang / Vị trí), nút Lưu, Khôi phục mặc định, Đóng.'], 37)
S2.add('Cài đặt bộ lọc: ẩn ô và lưu', 'P1', PRE, OPEN + ['Bấm Cài đặt bộ lọc.', 'Bỏ tích Hãng sản xuất.', 'Bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công"; khối lọc không còn ô Hãng sản xuất; F5 vẫn ẩn.'], 37)
S2.add('Cài đặt bộ lọc: đổi thứ tự, khôi phục, đóng', 'P2', PRE,
       OPEN + ['Bấm Cài đặt bộ lọc.', 'Kéo Hàng hóa lên đầu, bấm Đóng.', 'Mở lại, bấm Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bấm Đóng: thứ tự không đổi.', 'Khôi phục + Lưu: đủ 13 mục theo thứ tự gốc.'], 37)
S2.add('Chọn hàng hóa: mở cửa sổ', 'P0', 'Tài khoản DNS Admin, công ty TPE.', [MENU, 'Bấm ô Hàng hóa.'], '—',
       ['Mở cửa sổ "Chọn hàng hóa": dòng công ty TPE, cây catalog có số hàng, ô tìm, công tắc Còn tồn / Gồm hàng ngoài catalog, bảng hàng, nút Đóng.',
        'Chân cửa sổ ghi "Bấm vào tên hàng để chọn".'], 37)
S2.add('Chọn hàng hóa: chọn 1 hàng', 'P0', TPE, [MENU, 'Chỉ giữ kho PTT.', 'Bấm ô Hàng hóa.', 'Tìm "ENEO-640-V5236", bấm tên hàng.'],
       'Hàng hóa: ENEO-640-V5236',
       ['Cửa sổ đóng; ô Hàng hóa có thẻ "ENEO-640-V5236 - Dầu nhớt bán tổng hợp…"; báo cáo còn 1 mặt hàng 15,141 / 11,404 / 23,348 / 3,197 (nạp 1 lần).'], 37)
S2.add('Chọn hàng hóa: bỏ chọn bằng dấu ×', 'P1', [PRE_H, 'Đang chọn hàng ENEO-700-V5231.'], OPEN + ['Bấm dấu × trên thẻ hàng ở ô Hàng hóa.'], '—',
       ['Ô Hàng hóa trống, cửa sổ không mở; báo cáo trở lại 217 mặt hàng.'], [34, 37])
S2.add('Chọn hàng hóa: đóng không chọn', 'P2', PRE, OPEN + ['Bấm ô Hàng hóa.', 'Bấm Đóng.'], '—', ['Cửa sổ đóng, bộ lọc không đổi.'], 37)
S2.add('Chọn hàng hóa với công ty khác công ty đăng nhập', 'P1', 'Tài khoản DNS Admin đăng nhập công ty TPE.',
       OPEN + ['Bấm ô Hàng hóa.'], '—',
       ['Cửa sổ ghi "Công ty %s".' % CN, 'Cây catalog có số hàng, danh sách hàng tải được, không báo "Không tải được số lượng" / "Không tải được danh sách hàng hoá"; chọn được hàng.'], 37)

# ============================================================== III. SỐ LIỆU BÁO CÁO
S3 = Sec(3)
S3.add('Khối tổng hợp', 'P0', PRE, OPEN, '—',
       ['Khối Mặt hàng: Mặt hàng có phát sinh 217 mặt hàng; Kho đang xem 4 kho.',
        'Khối Phát sinh: Có tồn đầu kỳ 102, Có nhập trong kỳ 187, Có xuất trong kỳ 200, Còn tồn cuối kỳ 96 mặt hàng.'], 6)
S3.add('Ô bằng 0 thì ẩn', 'P1', PRE, OPEN + ['Đổi Kỳ = Năm trước.'], 'Kỳ: Năm trước',
       ['158 mặt hàng có phát sinh; khối Phát sinh chỉ còn Có nhập 158, Có xuất 153, Còn tồn cuối kỳ 102 — KHÔNG có ô Có tồn đầu kỳ (bằng 0).'], 6)
S3.add('Dòng TỔNG khớp khối tổng hợp và tổng số', 'P0', PRE, OPEN + ['Sang trang 2.'], '—',
       ['Dòng TỔNG "MẶT HÀNG CÓ PHÁT SINH 217 mặt hàng" = ô Mặt hàng có phát sinh = N ở "Hiển thị … / 217".',
        'Sang trang 2 dòng TỔNG và khối tổng hợp không đổi; dòng TỔNG không có số lượng.'], [16, 41])
S3.add('Tồn cuối kỳ = Tồn đầu + Nhập - Xuất từng dòng', 'P0', PRE, OPEN + ['Đọc từng dòng trang 1 (Số dòng/trang 100) và các trang sau.'], '—',
       ['Mọi dòng: Tồn cuối kỳ = Tồn đầu kỳ + Nhập - Xuất (vd Áo phông ENEOS 247 + 54 - 175 = 126; BIA 333 48 + 3,168 - 3,216 = 0 để trống).',
        'Không có dòng nào cả 3 số Tồn đầu, Nhập, Xuất cùng trống.'], 283)
S3.add('Đối soát với Thẻ kho (kỳ tới hôm nay)', 'P0',
       [PRE_H, 'Thẻ kho của hàng tại kho HP, công ty thuê TPHP, kỳ Tuỳ chọn 01/01/2026–09/11/2026: Tồn đầu kỳ 70, Nhập 496, Xuất 546, Tồn cuối kỳ 20.'],
       ['Mở Thẻ kho, chọn hàng ENEO-700-V5231, kho HP, công ty thuê TPHP, kỳ 01/01/2026 – 09/11/2026; ghi 4 số.', MENU, CHON_HP,
        'Chỉ giữ kho HP, Công ty thuê kho TPHP, chọn hàng ENEO-700-V5231, Kỳ Tuỳ chọn cùng khoảng ngày.'], 'Thời gian: 01/01/2026 – 09/11/2026',
       ['Báo cáo: 70 / 496 / 546 / 20 = Thẻ kho; 70 + 496 - 546 = 20.'], 6)
S3.add('Đối soát với Thẻ kho kỳ Năm nay và Tháng 10', 'P0',
       ['Tài khoản DNS Admin, công ty TPE.', '%s; Thẻ kho kho PTT Năm nay: 15,141 / 11,404 / 23,348 / 3,197; tháng 10/2026: 1,595 / 2,472 / 870 / 3,197.' % HANG3],
       [MENU, 'Chỉ giữ kho PTT, chọn hàng ENEO-640-V5236.', 'Đổi Kỳ = Tuỳ chọn 01/10/2026 – 31/10/2026.'], ['Kho: PTT', 'Kỳ: Năm nay, rồi 01/10/2026 – 31/10/2026'],
       ['Năm nay: 15,141 + 11,404 - 23,348 = 3,197 = Thẻ kho.', 'Tháng 10: 1,595 + 2,472 - 870 = 3,197 = Thẻ kho.',
        'Giữ đủ 8 kho công ty TPE: vẫn 3,197 (hàng chỉ có ở kho PTT).'], 6)
S3.add('Đối soát Loại báo cáo với Thẻ kho', 'P1',
       ['Tài khoản DNS Admin, công ty TPE.', '%s; Thẻ kho kho PTT Năm nay, Loại báo cáo "Không nhặt điều chuyển": 15,141 / 7,435 / 19,379 / 3,197.' % HANG3],
       [MENU, 'Chỉ giữ kho PTT, chọn hàng ENEO-640-V5236, Loại báo cáo = Không nhặt phiếu điều chuyển.'], '—',
       ['15,141 / 7,435 / 19,379 / 3,197 = Thẻ kho cùng loại báo cáo.'], 6)
S3.add('Tồn đầu kỳ = Tồn cuối kỳ của kỳ liền trước', 'P0', PRE_H, OPEN + HP_HANG + ['Đổi Kỳ = Năm trước, ghi Tồn cuối kỳ.', 'Đổi Kỳ = Năm nay, ghi Tồn đầu kỳ.'], '—',
       ['Năm trước Tồn cuối kỳ 70 = Năm nay Tồn đầu kỳ 70.', 'Cả 4 kho: Năm trước "Còn tồn cuối kỳ" 102 mặt hàng = Năm nay "Có tồn đầu kỳ" 102 mặt hàng.'], 6)
S3.add('Tồn cuối kỳ khớp Báo cáo tồn kho tổng hợp theo mặt hàng', 'P0', PRE,
       ['Mở Báo cáo tồn kho tổng hợp theo mặt hàng, công ty %s, 4 kho, Tính đến ngày hôm nay; ghi số mặt hàng và SL tồn.' % CN, MENU, CHON_HP], '—',
       ['Ô Còn tồn cuối kỳ 96 mặt hàng = 96 dòng của báo cáo kia; từng hàng Tồn cuối kỳ = SL tồn (vd ENEO-700-V5231 47).'], 6)
S3.add('Tồn cuối kỳ khớp Báo cáo tồn kho chi tiết theo mặt hàng', 'P0', PRE_H,
       ['Mở Báo cáo tồn kho chi tiết theo mặt hàng, công ty %s, kho HP, hàng ENEO-700-V5231, hôm nay; ghi SL tồn.' % CN, MENU, CHON_HP] + HP_HANG, '—',
       ['SL tồn bằng Tồn cuối kỳ (20).'], 6)
S3.add('Nhiều kho bằng tổng từng kho', 'P0', PRE_H, OPEN + ['Chọn hàng ENEO-700-V5231, ghi 4 số (4 kho).', 'Lần lượt chỉ giữ 1 kho HP, CB, KĐN-ALM, NM; ghi 4 số.'], '—',
       ['4 kho: 70 / 523 / 546 / 47; HP 70 / 496 / 546 / 20; CB trống / 27 / trống / 27; KĐN-ALM và NM: "%s".' % EMPTY, 'Nhập 523 = 496 + 27; Tồn cuối 47 = 20 + 27.'], 283)
S3.add('Lập chứng từ nhập thì số Nhập tăng', 'P0', [PRE_H, 'Lập và hoàn tất 1 Phiếu nhập kho 5 Xô 18L hàng ENEO-700-V5231 vào kho HP, công ty TPHP (môi trường kiểm thử).'],
       OPEN + HP_HANG, '—', ['Nhập trong kỳ và Tồn cuối kỳ tăng 5 (501, 25); Tồn đầu kỳ không đổi.', 'Kỳ Năm trước không đổi.'], [274, 281])
S3.add('Lập chứng từ xuất thì số Xuất tăng', 'P0', [PRE_H, 'Hoàn tất 1 Phiếu xuất kho 2 Xô 18L hàng ENEO-700-V5231 từ kho HP (môi trường kiểm thử).'],
       OPEN + HP_HANG, '—', ['Xuất trong kỳ tăng 2, Tồn cuối kỳ giảm 2.'], [274, 281])
S3.add('Kỳ quá khứ không bị ảnh hưởng bởi chứng từ mới', 'P1', [PRE_H, 'Vừa hoàn tất phiếu nhập / xuất hôm nay cho hàng này ở kho HP.'],
       OPEN + HP_HANG + ['Chọn Kỳ = Tuỳ chọn 01/01/2026 – 31/10/2026.'], '—', ['Số liệu như trước khi lập phiếu (phiếu hôm nay nằm ngoài kỳ).'], 281)
S3.add('Định dạng số', 'P1', TPE, [MENU], '—',
       ['4 cột số căn phải, phân cách hàng nghìn bằng dấu phẩy (vd 15,141); số lẻ hiện tối đa 2 chữ số; số 0 để trống; cột Xuất là số dương.'], 6)
S3.add('Cả công ty nhiều kho', 'P1', TPE, [MENU], '—',
       ['Khối tổng hợp: 8,441 mặt hàng, 8 kho; Có tồn đầu kỳ 6,367, Có nhập 4,514, Có xuất 5,707, Còn tồn cuối kỳ 6,158; trả kết quả trong vài giây.',
        'Không nhặt phiếu điều chuyển: Có nhập 3,874, Có xuất 5,164; Có tồn đầu / Còn tồn cuối không đổi.'], 286)

# ============================================================== IV. XEM CHI TIẾT
S4 = Sec(4)
S4.add('Ô chọn ĐVT trên dòng có nhiều ĐVT', 'P0', [PRE, '%s: 120 / 552 / 648 / 24 Can 1L trên 4 kho.' % HANG2],
       OPEN + ['Chọn hàng ENEO-410-S4136.', 'Bấm ô Đơn vị của dòng.'], '—',
       ['Ô Đơn vị là ô chọn, mặc định "Can 1L"; danh sách: Can 1L, Thùng 24C-1L (x24).'], [186, 187, 188])
S4.add('Đổi ĐVT quy đổi cả 4 cột', 'P0', [PRE, '%s: 120 / 552 / 648 / 24 Can 1L.' % HANG2],
       OPEN + ['Chọn hàng ENEO-410-S4136.', 'Ở cột Đơn vị chọn "Thùng 24C-1L (x24)".'], 'Đơn vị: Thùng 24C-1L (x24)',
       ['Dòng đổi thành 5 / 23 / 27 / 1 (chia 24); 5 + 23 - 27 = 1.', 'Không tải lại báo cáo.'], [189, 190])
S4.add('Quy đổi số lẻ', 'P1', PRE, OPEN + ['Ở dòng BIA 333 (48 / 3,168 / 3,216 Lon) chọn ĐVT Thùng 24C-0.8L (x24).'], 'Đơn vị: Thùng 24C-0.8L (x24)',
       ['Dòng hiện 2 / 132 / 134, Tồn cuối kỳ trống.'], 189)
S4.add('Hàng 1 ĐVT hiện chữ', 'P2', PRE, OPEN, '—', ['Dòng Áo khoác ENEOS cột Đơn vị là chữ "Cái." (không có ô chọn).'], 191)
S4.add('Bảng chỉ đọc', 'P0', PRE, OPEN + ['Bấm vào tên hàng, các số Tồn đầu kỳ, Nhập, Xuất, Tồn cuối kỳ.'], '—',
       ['Không có ô nhập, không có nút Lưu / Sửa / Xóa; bấm số không mở cửa sổ hay màn khác (không mở Thẻ kho).'], [191, 192, 193])
S4.add('ĐVT giữ khi đổi trang, mất khi F5', 'P1', [PRE, 'Dòng BIA 333 nằm ở trang 1.'], OPEN + ['Đổi ĐVT BIA 333 sang Thùng.', 'Sang trang 2 rồi về trang 1.', 'Nhấn F5.'], '—',
       ['Sau bước 4: BIA 333 vẫn Thùng 2 / 132 / 134.', 'Sau F5: về ĐVT cơ sở Lon.'], [196, 197])
S4.add('Giữ trang và bộ lọc khi thao tác trong bảng', 'P2', [PRE, 'Đang ở trang 3, lọc Thương hiệu ENEOS.'], OPEN + ['Đổi ĐVT 1 dòng, rê chuột tiêu đề cột.'], '—',
       ['Vẫn ở trang 3, giữ bộ lọc.'], 197)

# ============================================================== V. XUẤT DANH SÁCH EXCEL
S5 = Sec(5)
S5.add('Mở cửa sổ xuất Excel', 'P0', PRE, OPEN + ['Bấm Xuất Excel ở đầu khối lọc.'], '—',
       ['Mở cửa sổ "Xuất Excel tổng hợp xuất nhập tồn", Kiểu xuất có Đầy đủ (chọn sẵn, "Có Model và Thương hiệu.") và Ngắn gọn ("Chỉ tên, mã, đơn vị và số lượng."), nút Xuất Excel, Hủy.'],
       [212, 213, 214])
S5.add('Xuất kiểu Đầy đủ', 'P0', PRE, OPEN + ['Bấm Xuất Excel.', 'Giữ Đầy đủ, bấm Xuất Excel trong cửa sổ.'], 'Kiểu xuất: Đầy đủ',
       ['Tải file "%s"; cửa sổ đóng.' % FILE,
        'Cột: STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, Đơn vị, Tồn đầu kỳ, Nhập trong kỳ, Xuất trong kỳ, Tồn cuối kỳ.'], [215, 216, 223, 225, 226])
S5.add('Xuất kiểu Ngắn gọn', 'P0', PRE, OPEN + ['Bấm Xuất Excel.', 'Chọn Ngắn gọn, bấm Xuất Excel.'], 'Kiểu xuất: Ngắn gọn',
       ['File chỉ có STT, Tên hàng hóa, Mã hàng, Đơn vị, Tồn đầu kỳ, Nhập trong kỳ, Xuất trong kỳ, Tồn cuối kỳ.'], [217, 226])
S5.add('Không có bước chọn trường', 'P2', PRE, OPEN + ['Bấm Xuất Excel.'], '—', ['Cửa sổ không có danh sách chọn cột; luôn xuất đủ cột của kiểu.'], 218)
S5.add('Xuất theo bộ lọc', 'P0', PRE_H, OPEN + HP_HANG + ['Xuất Excel kiểu Đầy đủ.'], '—',
       ['File chỉ có 1 mặt hàng: 70 / 496 / 546 / 20; dòng "Kho: HP - Hải Phòng".'], [219, 220])
S5.add('Xuất mọi trang', 'P0', PRE, OPEN + ['Đang ở trang 1 (20 mặt hàng), xuất kiểu Ngắn gọn.'], '—',
       ['File có đủ 217 mặt hàng (không riêng trang đang xem).'], [221, 227])
S5.add('Xuất khi báo cáo rỗng', 'P1', [PRE, 'Kho KĐN-ALM, NM không có phát sinh.'], OPEN + ['Chỉ giữ kho KĐN-ALM, NM.', 'Xuất Excel kiểu Đầy đủ.'], '—',
       ['Vẫn tải file: letterhead, tiêu đề, Từ ngày – Đến ngày, Kho, hàng tên cột, dòng "Không có dữ liệu", khối ký.'], 222)
S5.add('Chưa chọn kho thì không xuất', 'P1', PRE, OPEN + ['Bỏ tích Xem toàn bộ kho.', 'Bấm Xuất Excel.'], '—',
       ['Không mở cửa sổ; ô Kho chữ đỏ "Vui lòng chọn kho".'], 222)
S5.add('Định dạng file', 'P1', PRE, OPEN + ['Xuất kiểu Đầy đủ, mở file.'], '—',
       ['File .xlsx mở được; dòng 1 letterhead công ty CN Hải Phòng; tiêu đề "BÁO CÁO TỔNG HỢP XUẤT NHẬP TỒN"; "Từ ngày: 01/01/2026 Đến ngày: 31/12/2026"; '
        '"Kho: CB - Cát Bà, HP - Hải Phòng, KĐN-ALM - Kho gửi tại Đồng Nai, NM - Nhà máy".',
        'Bảng 1 tầng tiêu đề; cuối file khối ký Trưởng kho, Người lập báo cáo kèm ngày.'], 224)
S5.add('Dữ liệu khớp màn hình', 'P0', PRE, OPEN + ['Xuất kiểu Đầy đủ, tìm Áo phông ENEOS trong file.'], '—',
       ['Tên, Model AOPHONG, Mã ENEO-AOPHONG, ENEOS, Đơn vị "Cái.", 247 / 54 / 175 / 126 khớp màn; Xuất là số dương.'], 228)
S5.add('Số là ô số, theo ĐVT đã chọn', 'P1', [PRE, '%s; trên màn đã đổi ĐVT sang Thùng 24C-1L.' % HANG2], OPEN + ['Xuất kiểu Ngắn gọn, mở file.'], '—',
       ['Hàng ENEO-410-S4136 trong file: Đơn vị "Thùng 24C-1L (x24)", 5 / 23 / 27 / 1.', 'Ô số có phân cách hàng nghìn, cộng SUM được; số 0 để trống.'], 229)
S5.add('Tiếng Việt và ký tự đặc biệt', 'P2', PRE, OPEN + ['Xuất, mở file.'], '—',
       ['Tên hàng có dấu, ký tự "(", "/", "-", "," hiển thị đúng, không lỗi phông.'], 230)
S5.add('Hủy xuất', 'P2', PRE, OPEN + ['Bấm Xuất Excel.', 'Bấm Hủy.'], '—', ['Cửa sổ đóng, không tải file; mở lại kiểu về Đầy đủ.'], 212)
S5.add('Đang xuất thì khóa nút', 'P1', TPE, [MENU, 'Xuất Excel kiểu Đầy đủ, bấm liên tục 2 lần.'], '—',
       ['Nút đổi chữ "Đang xuất…", có vòng xoay, không nhận lần bấm thứ 2; chỉ tải 1 file 8.441 mặt hàng.'], 221)

# ============================================================== VI. IN BÁO CÁO
S6 = Sec(6)
S6.add('Mở cửa sổ In báo cáo', 'P0', PRE, OPEN + ['Bấm In danh sách.'], '—',
       ['Cửa sổ "In báo cáo": kiểu Đầy đủ chọn sẵn, Ngắn gọn; "Chọn cột in" tích sẵn 9 cột (Tên hàng hóa, Model, Mã hàng, Thương hiệu, Đơn vị, 4 cột số); nút In, Hủy.'], 212)
S6.add('Đổi kiểu in đổi danh sách cột', 'P1', PRE, OPEN + ['Bấm In danh sách.', 'Chọn Ngắn gọn.'], '—',
       ['Danh sách cột còn 7: Tên hàng hóa, Mã hàng, Đơn vị, Tồn đầu kỳ, Nhập trong kỳ, Xuất trong kỳ, Tồn cuối kỳ.'], 213)
S6.add('Bỏ hết cột thì báo lỗi', 'P0', PRE, OPEN + ['Bấm In danh sách.', 'Bỏ tích Chọn tất cả.', 'Bấm In.'], '—',
       ['Chữ đỏ "Vui lòng chọn ít nhất 1 cột để in"; cửa sổ không đóng.'], 218)
S6.add('Xem trước bản in kiểu Đầy đủ', 'P0', PRE, OPEN + ['Bấm In danh sách, bấm In.'], '—',
       ['Mở "Xem trước tổng hợp xuất nhập tồn": letterhead CN Hải Phòng, "BÁO CÁO TỔNG HỢP XUẤT NHẬP TỒN", "Thời gian: Từ ngày 01/01/2026 đến ngày 31/12/2026", Kho, bảng 217 mặt hàng, khối ký Trưởng kho, Người lập báo cáo.'], [219, 221])
S6.add('In theo cột đã chọn', 'P1', PRE, OPEN + ['Bấm In danh sách.', 'Bỏ tích Model và Thương hiệu, bấm In.'], '—',
       ['Bản xem trước không có cột Model, Thương hiệu; cột STT luôn có.'], 217)
S6.add('Bấm In trên bản xem trước', 'P1', PRE, OPEN + ['Mở xem trước, bấm In.'], '—', ['Hộp thoại in của trình duyệt mở, nội dung đúng bản xem trước (khổ ngang).'], 219)
S6.add('Vượt mức in tối đa', 'P0', TPE, [MENU, 'Bấm In danh sách, bấm In.'], '—',
       ['Bản xem trước không có nội dung, hiện "Danh sách có 8441 dòng, vượt mức in tối đa 2.000 dòng nên chưa in được…"; nút In ẩn.'], 221)
S6.add('Chưa chọn kho thì không in', 'P1', PRE, OPEN + ['Bỏ tích Xem toàn bộ kho.', 'Bấm In danh sách.'], '—',
       ['Không mở cửa sổ; ô Kho chữ đỏ "Vui lòng chọn kho".'], 222)
S6.add('Số in theo ĐVT đã chọn', 'P2', [PRE, '%s; trên màn đã đổi ĐVT sang Thùng 24C-1L.' % HANG2], OPEN + ['In kiểu Ngắn gọn.'], '—',
       ['Bản in ghi Đơn vị "Thùng 24C-1L (x24)", 5 / 23 / 27 / 1.'], 229)
S6.add('Hủy in', 'P2', PRE, OPEN + ['Bấm In danh sách, bấm Hủy.', 'Mở xem trước rồi bấm ×.'], '—', ['Đóng cửa sổ, không in; báo cáo giữ nguyên.'], 196)

# ============================================================== VII. RÀNG BUỘC
S7 = Sec(7)
S7.add('Phiếu điều chuyển vị trí', 'P0', [PRE_H, 'Hoàn tất phiếu điều chuyển vị trí 2 Xô 18L hàng ENEO-700-V5231 từ KHOANG1 sang KHOANG2 kho HP (môi trường kiểm thử).'],
       OPEN + HP_HANG, '—',
       ['Loại báo cáo Tất cả: Nhập và Xuất cùng tăng 2, Tồn cuối kỳ không đổi (20).', 'Không nhặt phiếu điều chuyển: Nhập / Xuất như trước phiếu.',
        'Tick riêng vị trí KHOANG1: Xuất tăng 2, Tồn cuối kỳ 18.'], [272, 274, 281, 284])
S7.add('Phiếu điều chuyển giữa 2 kho', 'P1', [PRE_H, 'Hoàn tất điều chuyển 3 Xô 18L hàng ENEO-700-V5231 từ kho HP sang kho CB (môi trường kiểm thử).'],
       OPEN + ['Chọn hàng ENEO-700-V5231.', 'Lần lượt chỉ giữ kho HP, kho CB, rồi cả 4 kho.'], '—',
       ['Kho HP Xuất tăng 3, Tồn cuối 17; kho CB Nhập tăng 3, Tồn cuối 30; cả 4 kho Tồn cuối vẫn 47 (Nhập và Xuất cùng tăng 3).'], [274, 281, 282])
S7.add('Nhập / xuất điều chỉnh kiểm kê', 'P1', [PRE_H, 'Hoàn tất phiếu nhập kho điều chỉnh kiểm kê +1 và phiếu xuất kho điều chỉnh kiểm kê -1 cho hàng này ở kho HP.'],
       OPEN + HP_HANG, '—', ['Nhập tăng 1, Xuất tăng 1; Tồn cuối kỳ: 21 sau phiếu nhập, 20 sau phiếu xuất.'], 274)
S7.add('Khai báo tồn kho đầu kỳ', 'P1', [PRE, 'Khai báo tồn đầu kỳ hôm nay 10 Cái hàng Z (chưa từng có ở 4 kho) cho công ty TPHP tại kho HP.'],
       OPEN + ['Chọn hàng Z.'], '—', ['Hàng Z xuất hiện: Nhập trong kỳ 10, Tồn cuối kỳ 10.'], 274)
S7.add('Đổi tên hàng ở danh mục', 'P2', [PRE_H, 'Đổi tên hàng ENEO-700-V5231 ở danh mục hàng hóa (môi trường kiểm thử).'], OPEN + ['Chọn hàng ENEO-700-V5231.'], '—',
       ['Báo cáo hiện tên mới, số không đổi.'], [278, 279])
S7.add('Kho ngừng hoạt động không còn trong ô Kho', 'P1', ['Tài khoản DNS Admin.', 'Kho NM - Nhà máy chuyển sang ngừng hoạt động ở danh mục Kho vật lý.'],
       [MENU, 'Chọn công ty CN Hải Phòng, mở ô Kho.'], '—', ['Ô Kho không còn NM; Xem toàn bộ kho chọn 3 kho CB, HP, KĐN-ALM.'], [276, 285])
S7.add('Thêm vị trí mới ở danh mục', 'P2', [PRE, 'Thêm vị trí "HP-TEST" vào Khoang K1 kho HP ở danh mục Vị trí.'], [MENU, CHON_HP, 'Tick TANG1 > D1 > K1.'], '—',
       ['Cột Vị trí có thêm "HP-TEST"; tick riêng vị trí này: bảng "%s".' % EMPTY], [280, 282])
S7.add('Màn chỉ đọc, không làm đổi dữ liệu', 'P0', PRE, OPEN + ['Thao tác lọc, tick vị trí, đổi ĐVT, in, xuất nhiều lần.', 'Mở Thẻ kho cùng hàng / kho.'], '—',
       ['Không có chứng từ, tồn kho hay lịch sử nào thay đổi; Thẻ kho giữ nguyên số.'], [268, 270, 285])
S7.add('Đối chiếu với Thẻ kho sau khi lập chứng từ', 'P0', [PRE_H, 'Vừa hoàn tất 1 phiếu nhập và 1 phiếu xuất cho hàng này ở kho HP hôm nay.'],
       ['Mở Thẻ kho kho HP, công ty thuê TPHP, kỳ Năm nay, ghi 4 số.', MENU, CHON_HP] + HP_HANG, '—',
       ['4 số của báo cáo = 4 số khối Số lượng của Thẻ kho.'], [274, 281])

# ============================================================== VIII. PHÂN QUYỀN
S8 = Sec(8)
S8.add('Quyền theo tổng công ty', 'P0', ACC_T, ['Đăng nhập T.', MENU, 'Mở ô Tồn theo công ty, ô Kho.'], '—',
       ['Ô Tồn theo công ty có mọi công ty đang hoạt động (6 công ty); ô Kho có mọi kho của công ty đang chọn; xem, in, xuất được.'], [287, 299])
S8.add('Quyền theo công ty', 'P0', ACC_C, ['Đăng nhập C.', MENU, 'Mở ô Tồn theo công ty, ô Kho.'], '—',
       ['Ô Tồn theo công ty chỉ có CN Hải Phòng; ô Kho có CB, HP, KĐN-ALM, NM (chọn sẵn đủ); số liệu giống T khi cùng bộ lọc (217 mặt hàng).'], [287, 299])
S8.add('Quyền theo kho', 'P0', ACC_K, ['Đăng nhập K.', MENU], '—',
       ['Ô Kho chỉ có HP và được chọn sẵn; cây vị trí chỉ có nhà / vị trí kho HP; báo cáo hiện ngay số kho HP.'], [287, 299])
S8.add('In / Xuất với quyền theo công ty', 'P1', ACC_C, ['Đăng nhập C.', MENU, 'Xuất Excel kiểu Đầy đủ; In kiểu Đầy đủ.'], '—',
       ['File và bản in đủ cột như T, letterhead CN Hải Phòng.'], [288, 293])
S8.add('Không có quyền nào', 'P0', ACC_N, ['Đăng nhập N.', MENU], '—',
       ['Mục menu vẫn hiện; mở màn báo "%s".' % NOPERM, 'Ô Tồn theo công ty, Kho rỗng; Xem toàn bộ kho bị khóa; bảng "Chọn công ty để xem báo cáo.", không có số liệu.',
        'Bấm In danh sách / Xuất Excel: chữ đỏ dưới ô thiếu, không ra bản in / file.'], [287, 295])
S8.add('Mở trực tiếp đường dẫn khi thiếu quyền', 'P0', ACC_N, ['Đăng nhập N.', 'Dán đường dẫn màn báo cáo vào thanh địa chỉ.'], '—',
       ['Báo "%s"; bảng "Chọn công ty để xem báo cáo.", không lộ số liệu.' % NOPERM], 296)
S8.add('Kho ngoài phạm vi bị chặn', 'P0', ACC_C, ['Đăng nhập C.', MENU, 'Sửa bộ lọc ghi tạm của trình duyệt cho Kho = PTT (kho công ty TPE), F5.'], '—',
       ['Kho PTT bị bỏ, ô Kho chọn lại đủ kho của CN Hải Phòng; không hiện số kho PTT.'], [297, 299])
S8.add('Không có thao tác ghi', 'P1', ACC_T, ['Đăng nhập T.', MENU, CHON_HP], '—',
       ['Không có nút Thêm mới, Sửa, Xóa, Khóa, Import, Lịch sử ở mọi quyền.'], [289, 290, 291, 292, 294])
S8.add('Đổi quyền giữa thao tác', 'P1', [ACC_C, 'Quản trị gỡ quyền "%s" của C khi C đang mở báo cáo.' % V2], ['C đổi Thương hiệu = ENEOS.'], '—',
       ['Báo "%s"; bảng giữ số cũ, không nạp số mới.' % NOPERM], 298)
S8.add('Có nhiều quyền lấy quyền cao nhất', 'P1', 'Tài khoản M: có cả "%s" và "%s".' % (V2, V3), ['Đăng nhập M.', MENU, 'Mở ô Kho.'], '—',
       ['Ô Kho có mọi kho của công ty M (theo quyền công ty), không chỉ kho M là thủ kho.'], 299)
S8.add('Super admin', 'P2', 'Tài khoản DNS Admin (Super admin), không gán 3 quyền.', ['Đăng nhập DNS Admin.', MENU], '—',
       ['Như quyền tổng công ty: chọn được mọi công ty, mọi kho.'], 287)
S8.add('Quyền theo kho không là thủ kho kho nào', 'P2', 'Tài khoản K2: có quyền "%s", chưa là thủ kho kho nào.' % V3, ['Đăng nhập K2.', MENU], '—',
       ['Ô Kho rỗng, Xem toàn bộ kho bị khóa; bảng "%s".' % CHONKHO], 299)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'SỐ LIỆU BÁO CÁO', S3),
    ('IV', 'XEM CHI TIẾT THEO ĐƠN VỊ TÍNH', S4),
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
                feature_name='Tổng hợp xuất nhập tồn - Cập nhật ngày 09/11/2026',
                module_name='Tổng hợp xuất nhập tồn', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='bao_cao')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

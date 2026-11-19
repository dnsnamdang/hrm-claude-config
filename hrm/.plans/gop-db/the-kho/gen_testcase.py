# -*- coding: utf-8 -*-
"""Testcase màn "Thẻ kho" (phân hệ Kho › Báo cáo kho) — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026
(tc_chuan.build_chuan, loai='bao_cao').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'bao_cao' (đọc code 06/11/2026): màn chỉ đọc, chỉ có xem / lọc / bung chứng từ / in / xuất Excel — không có Thêm, Sửa, Xóa,
Khóa, Duyệt, Import, Lịch sử, Tùy chỉnh cột (khuôn báo cáo bỏ Cấu hình cột 22/10/2026) → bỏ nhóm TÙY CHỈNH CỘT.
Thứ tự nhóm: I Hiển thị · II Tìm kiếm & lọc (gồm Chọn hàng hóa, "Cài đặt bộ lọc:") · III Số liệu báo cáo (đối soát công thức, lũy kế,
chứng từ nguồn, báo cáo tồn khác) · IV Xem chi tiết chứng từ và lô / vị trí · V Xuất danh sách Excel · VI In báo cáo · VII Ràng buộc ·
VIII Phân quyền. Mỗi case ghi stt checklist nó phủ (tham số ck) — gen_checklist.py đọc CK.
Khuôn: ../kiem-ke-theo-hang-hoa/gen_testcase.py (06/11, check_tc 0 lỗi).
Số liệu mẫu: dev-hrm 06/11/2026 (DNS Admin, đọc bằng _capture/probe*.js — chỉ GET): hàng ENEO-640-V5236 "Dầu nhớt bán tổng hợp động cơ
ô tô 4 kỳ SP/CF SAE 5W-30 (4Lx6)", ĐVT cơ sở Can 4L, công ty TPE; Năm 2026: tồn đầu 15,141 + nhập 11,248 − xuất 23,192 = tồn cuối 3,197;
510 chứng từ (76 nhập, 424 xuất, 10 điều chuyển); Năm 2025 tồn cuối 15,141; kho PTT (mọi công ty thuê) 15,141 / 11,404 / 23,348 / 3,197,
514 chứng từ; Không nhặt điều chuyển 7,279 / 19,223, 500 chứng từ; tháng 10/2026: 1,595 / 2,472 / 870 / 3,197, 30 chứng từ;
PĐCVT-00584 (31/01/2026) 8 lô / vị trí, chuyển 432; PNL-00023 SL tồn 6,619. Báo cáo tồn kho tổng hợp / chi tiết theo mặt hàng kho PTT
tính đến 06/11/2026: TPE 3,197; Tổng hợp xuất nhập tồn kho PTT năm 2026: 15,141 / 11,404 / 23,348 / 3,197.
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
MENU = 'Vào phân hệ Kho > menu "Báo cáo kho" > bấm "Thẻ kho".'
PICK = 'Bấm ô Hàng hóa, gõ "ENEO-640-V5236", Enter, bấm tên hàng.'
Q1 = 'Thủ kho'
V1 = 'Xem báo cáo tồn kho theo tổng công ty'
NOPERM = 'Bạn không có quyền truy cập chức năng này.'
HANG = 'Hàng ENEO-640-V5236 "Dầu nhớt bán tổng hợp động cơ ô tô 4 kỳ SP/CF SAE 5W-30 (4Lx6)", ĐVT cơ sở Can 4L.'
PRE = ('Tài khoản DNS Admin (Super admin), công ty TPE.\n' + HANG + '\n'
       'Năm 2026 tại TPE: tồn đầu 15,141; nhập 11,248; xuất 23,192; tồn cuối 3,197; 510 chứng từ (76 nhập, 424 xuất, 10 điều chuyển vị trí).')
OPEN = [MENU, PICK]
ACC_T = 'Tài khoản T: công ty TPE, có quyền "%s", không có quyền "%s".' % (Q1, V1)
ACC_A = 'Tài khoản A: công ty TPE, có quyền "%s" và "%s".' % (Q1, V1)
ACC_N = 'Tài khoản N: công ty TPE, không có quyền nào của màn.'
ADV = 'Ở khối Bộ lọc thẻ kho (đang mở sẵn).'

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
     'Theo dõi nhập, xuất, tồn của MỘT mặt hàng theo từng chứng từ trong một kỳ, tại các kho / vị trí của một công ty: tồn đầu kỳ, '
     'nhập, xuất, tồn cuối kỳ, SL tồn lũy kế sau từng chứng từ, bung lô / vị trí, mở chứng từ nguồn, in và xuất Excel. Màn chỉ đọc.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Chứng từ đã ghi tồn theo vị trí của hàng: phiếu nhập kho, phiếu xuất kho (từ lúc gửi), phiếu nhập / xuất kho điều chỉnh kiểm kê '
     '(từ lúc gửi), phiếu điều chuyển vị trí (khi Đã chuyển), phiếu nhập lại, phiếu xuất điều chỉnh sai số liệu (khi lập), khai báo tồn '
     'kho đầu kỳ (dòng "Nhập tồn đầu").\n'
     '- Phạm vi: vị trí thuộc kho đang lọc (trống = mọi kho của công ty), công ty ghi nhận = công ty đang xem (không chọn kho) hoặc công '
     'ty thuê kho đã tick (chọn kho).\n- Phiếu bị Không duyệt sau khi gửi vẫn nằm trên thẻ kho (không hoàn tồn).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu nhập / xuất kho còn Đang tạo (chưa gửi); phiếu xuất còn chuyến xe chưa duyệt xuất phát; điều chuyển chưa Đã chuyển.\n'
     '- Vị trí ngoài kho / vị trí đang lọc; tồn ghi cho công ty khác.\n'
     '- Phiếu điều chuyển vị trí khi Loại báo cáo = Không nhặt điều chuyển.\n'
     '- Ô tồn đầu / nhập / xuất / số phiếu bằng 0 bị ẩn ở khối tổng hợp (trừ Tồn cuối kỳ, Tổng chứng từ).'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô Kỳ (Tuần này / Tháng này / Năm nay mặc định 01/01 sang 31/12 / Năm trước / Tuỳ chọn) lọc theo NGÀY GHI TỒN của chứng từ (cột Ngày '
     'chứng từ), lấy trọn hai ngày biên; mọi phát sinh trước ngày đầu kỳ cộng vào Tồn đầu kỳ.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Bảng 2 cấp: Chứng từ (STT La Mã) > Lô / vị trí (STT 1, 2…); dòng TỔNG trên cùng.\n'
     '- Phạm vi vị trí: Kho > Nhà > Dãy > Khoang > Vị trí (lọc theo cấp sâu nhất được tick).'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Gom dòng theo (phiếu, loại chứng từ); mỗi lần khai tồn đầu là 1 chứng từ riêng.\n'
     '- SL tồn = tồn đầu kỳ + cộng dồn thay đổi tới hết chứng từ, theo thời điểm ghi tồn tăng dần.\n'
     '- Chứng từ có lô giảm = chứng từ xuất; điều chuyển: Nhập = tổng chuyển vào, Xuất = tổng chuyển ra.'),
    ('7. Phân quyền cấp',
     '- "%s": điều kiện để mở màn, xem, in, xuất Excel (thiếu: hệ thống báo "%s").\n'
     '- "%s": chọn được mọi công ty ở ô Tồn theo công ty; không có: chỉ công ty mình.\n- Super admin được miễn kiểm.' % (Q1, NOPERM, V1)),
    ('8. Cách tính các ô thống kê',
     '- Tồn cuối kỳ = Tồn đầu kỳ + Nhập trong kỳ - Xuất trong kỳ = SL tồn dòng chứng từ cuối.\n'
     '- Nhập / Xuất trong kỳ tính CẢ điều chuyển vị trí.\n'
     '- Tổng chứng từ = Nhập + Xuất + Điều chuyển vị trí (số phiếu).\n'
     '- Dòng TỔNG: Nhập / Xuất / SL tồn = khối Số lượng; "N chứng từ" = Tổng chứng từ.\n'
     '- "Hiển thị a–b / N chứng từ": N = số dòng chứng từ sau ô Số chứng từ / Diễn giải.'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản: DNS Admin (Super admin), T (Thủ kho, không xem tổng công ty), A (Thủ kho + xem tổng công ty), N (không quyền).\n'
     '- Lưu ý: ô Số chứng từ / Diễn giải chỉ lọc dòng hiển thị, KHÔNG đổi khối tổng hợp, dòng TỔNG, SL tồn.\n'
     '- Lưu ý: chữ ở icon thông tin của dòng TỔNG ghi "không tính điều chuyển vị trí" nhưng số thực tế CÓ tính (khớp khối Số lượng).\n'
     '- Lưu ý: bảng không sắp xếp theo cột, không có Tùy chỉnh cột; phân trang theo chứng từ, mặc định 20.\n'
     '- Số theo ĐVT cơ sở, phân cách hàng nghìn dấu phẩy, tối đa 2 số lẻ.'),
]

# ============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', PRE, ['Đăng nhập DNS Admin.', 'Bấm nút lưới phân hệ, chọn "Kho".', 'Bấm "Báo cáo kho" ở thanh bên.',
                                          'Bấm "Thẻ kho".'], '—',
       ['Nhóm Báo cáo kho có mục "Thẻ kho" đứng đầu.', 'Mở màn Thẻ kho, khối "Bộ lọc thẻ kho" đang mở sẵn.',
        'Bảng hiện "Chọn hàng hóa để xem thẻ kho.".'], [1, 8])
S1.add('Tiêu đề màn hình', 'P1', PRE, [MENU, 'Quan sát thanh tiêu đề và tab trình duyệt.'], '—',
       ['Thanh tiêu đề và tab trình duyệt đều là "Thẻ kho", kèm icon thông tin.'], 2)
S1.add('Các nút chức năng được hiển thị', 'P0', PRE, [MENU, 'Quan sát khối bộ lọc.'], '—',
       ['Đầu khối: In danh sách, Xuất Excel, Cài đặt bộ lọc, Ẩn tìm kiếm nâng cao.', 'Dưới các ô lọc: Tìm kiếm, Xóa lọc.',
        'Không có nút Tạo mới, Import, biểu tượng cấu hình cột.'], 3)
S1.add('Các cột mặc định hiển thị', 'P0', PRE, OPEN + ['Đọc tiêu đề cột của bảng.'], '—',
       ['Đúng 9 cột: STT, Chứng từ / Lô (kèm ô chọn cấp), Ngày chứng từ, Diễn giải, Vị trí, Nhập, Xuất, SL tồn, NVKD.',
        'Cột Nhập, Xuất, SL tồn, NVKD có icon thông tin ở tiêu đề.'], 4)
S1.add('Không có cột ẩn mặc định', 'P2', PRE, OPEN + ['Tìm nút cấu hình cột.'], '—',
       ['Không có nút cấu hình cột; 9 cột luôn hiện, bảng rộng thì cuộn ngang.'], 5)
S1.add('Dữ liệu dòng chứng từ khớp chứng từ nguồn', 'P0', [PRE, 'Phiếu xuất kho PXK-12602 ghi tồn 05/01/2026, diễn giải "PYCXH-15151", '
       'lô tại vị trí PTT-N1-KV7 giảm 6 Can 4L, người lập yêu cầu Lê Hữu Thắng (phòng HN_DAU).'], OPEN + ['Đọc dòng I.'], '—',
       ['Dòng I: Chứng từ "PXK-12602", Ngày "05/01/2026", Diễn giải "PYCXH-15151", Vị trí "PTT-N1-KV7".',
        'Nhập trống, Xuất "6", SL tồn "15,135".', 'NVKD "Lê Hữu Thắng - HN_DAU".'], 6)
S1.add('Dòng báo cáo không có trạng thái', 'P2', PRE, OPEN + ['Quan sát các dòng.'], '—',
       ['Không có cột / nhãn trạng thái; phiếu điều chuyển có chữ nhỏ "Điều chuyển vị trí" sau số chứng từ.'], 7)
S1.add('Hàng không có phát sinh trong kỳ', 'P1', ['Tài khoản DNS Admin.', 'Hàng H0 không có chứng từ nào tại TPE trong năm 2026, tồn đầu 0.'],
       [MENU, 'Chọn hàng H0.'], 'Hàng hóa: H0',
       ['Bảng hiện "Không có chứng từ nào khớp bộ lọc.".', 'Khối Số lượng chỉ hiện Tồn cuối kỳ "0"; khối Chứng từ hiện Tổng chứng từ "0 phiếu".',
        'Không có dòng phân trang.'], [8, 9])
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', PRE, OPEN + ['Nhập "ZZZ999" ở ô Số chứng từ / Diễn giải, Enter.'],
       'Số chứng từ / Diễn giải: ZZZ999', ['Bảng chỉ còn dòng TỔNG và câu "Không có chứng từ nào khớp bộ lọc.".',
                                         'Khối tổng hợp giữ nguyên 510 chứng từ.'], 9)
S1.add('Số dòng mặc định / trang', 'P0', PRE, OPEN, '—',
       ['Trang 1 hiện 20 chứng từ (I sang XX), "Hiển thị 1–20 / 510 chứng từ", Số dòng/trang = 20.'], [10, 16])
S1.add('Thay đổi số dòng / trang', 'P0', PRE, OPEN + ['Sang trang 3.', 'Đổi Số dòng/trang thành 50.'], 'Số dòng/trang: 50',
       ['Về trang 1, hiện 50 chứng từ, "Hiển thị 1–50 / 510 chứng từ".', 'Lựa chọn có: 10, 20, 50, 100.'], [11, 18])
S1.add('Trang trước / trang tiếp theo', 'P0', PRE, OPEN + ['Bấm ›.', 'Bấm ‹.'], '—',
       ['Bước 3: "Hiển thị 21–40 / 510 chứng từ".', 'Bước 4: "Hiển thị 1–20 / 510 chứng từ".'], 12)
S1.add('Trang đầu / trang cuối', 'P1', PRE, OPEN + ['Bấm ».', 'Bấm «.'], '—',
       ['Bước 3: trang 26 "Hiển thị 501–510 / 510 chứng từ"; dòng cuối SL tồn "3,197".', 'Bước 4: về trang 1.'], 13)
S1.add('Trạng thái nút phân trang ở trang đầu / cuối', 'P2', PRE, OPEN + ['Ở trang 1 quan sát « ‹.', 'Ở trang cuối quan sát › ».'], '—',
       ['Trang 1: « và ‹ mờ.', 'Trang cuối: › và » mờ.'], 14)
S1.add('STT liên tục giữa các trang', 'P0', PRE, OPEN + ['Sang trang 2.'], '—', ['Trang 2 đánh STT La Mã XXI sang XL.'], 15)
S1.add('Về trang 1 khi đổi hàng hóa', 'P0', PRE, OPEN + ['Sang trang 3.', 'Chọn hàng khác ENEO-800-V5231.'], 'Hàng hóa: ENEO-800-V5231',
       ['Bảng về trang 1 của hàng mới.'], 17)
S1.add('Giữ trang khi đổi ô lọc khác', 'P2', PRE, OPEN + ['Sang trang 3.', 'Đổi Loại báo cáo = Không nhặt điều chuyển.'], '—',
       ['Vẫn ở trang 3 (vẫn còn đủ 25 trang); nếu số trang mới ít hơn trang đang xem thì về trang cuối.',
        'Lưu ý: màn chỉ tự về trang 1 khi đổi hàng hóa hoặc đổi Số dòng/trang.'], 17)
S1.add('Thứ tự mặc định', 'P0', PRE, OPEN + ['Đọc cột Ngày chứng từ và SL tồn 5 dòng đầu.'], '—',
       ['Dòng xếp theo thời điểm ghi tồn tăng dần: PXK-12602, PXK-12601, PXK-12610, PNK-03764, PNK-03765 (đều 05/01/2026).',
        'SL tồn chạy liên tục: 15,135 sang 15,063 sang 15,051 sang 15,195 sang 15,207.'], 19)
S1.add('Bảng không sắp xếp theo cột', 'P1', PRE, OPEN + ['Bấm tiêu đề Ngày chứng từ, Nhập, Xuất, SL tồn.'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự (thẻ kho luôn theo thời gian để SL tồn lũy kế đúng).'], [20, 21, 22, 23])
S1.add('Thứ tự giữ nguyên khi chuyển trang', 'P1', PRE, OPEN + ['Sang trang 2.'], '—',
       ['Dòng XXI tiếp nối ngày / SL tồn của dòng XX trang 1.'], [24, 25])
S1.add('Thu gọn / mở rộng khối tổng hợp', 'P2', PRE, OPEN + ['Bấm "Thu gọn" ở dòng tiêu đề khối.', 'Bấm "Mở rộng".'], '—',
       ['Bước 3: ẩn 2 khối Số lượng, Chứng từ, chữ đổi "Mở rộng"; bảng không tải lại.', 'Bước 4: hiện lại.'], 3)
S1.add('Icon thông tin mục đích báo cáo', 'P2', PRE, [MENU, 'Rê chuột icon thông tin cạnh "Bộ lọc thẻ kho".'], '—',
       ['Hiện "MỤC ĐÍCH BÁO CÁO" và 3 dòng: Theo dõi nhập, xuất, tồn của 1 mặt hàng theo từng chứng từ trong kỳ; Phạm vi: công ty, kho, '
        'công ty thuê kho, nhà / dãy / khoang / vị trí đang lọc; Mỗi chứng từ bung ra được từng lô / vị trí phát sinh.'], 3)
S1.add('Đang tải lại thì dữ liệu cũ mờ đi', 'P2', PRE, OPEN + ['Đổi Kỳ = Năm trước.'], '—',
       ['Trong lúc tải, khối tổng hợp và bảng mờ đi, không bấm được; tải xong hiện số năm 2025.'], 19)
S1.add('Phiên đăng nhập hết hạn', 'P2', [PRE, 'Phiên đăng nhập đã hết hạn.'], OPEN + ['Đổi Kỳ = Năm trước.'], '—',
       ['Báo "Phiên đăng nhập đã hết hạn", chuyển về màn đăng nhập.'], 1)

# ============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = Sec(2)
S2.add('Giá trị mặc định của bộ lọc', 'P0', ['Tài khoản DNS Admin, công ty TPE, chưa mở màn trong 10 phút qua.'], [MENU], '—',
       ['Kỳ = Năm nay, Hàng hóa trống, Tồn theo công ty = công ty TPE, Kho trống, Công ty thuê kho trống, Loại báo cáo = Tất cả, '
        'Số chứng từ / Diễn giải trống.', 'Không có ô Nhà / Dãy / Khoang / Vị trí (chưa chọn kho).'], 36)
S2.add('Thiếu Hàng hóa thì bị chặn', 'P0', PRE, [MENU, 'Bấm Tìm kiếm.'], '—',
       ['Chữ đỏ "Vui lòng chọn hàng hóa" dưới ô Hàng hóa, khối ô lọc mở.', 'Bảng không tải, vẫn "Chọn hàng hóa để xem thẻ kho.".'], [37, 40])
S2.add('Thiếu Tồn theo công ty thì bị chặn', 'P1', PRE, OPEN + ['Bấm × ở ô Tồn theo công ty.', 'Bấm Tìm kiếm.'], '—',
       ['Chữ đỏ "Vui lòng chọn tồn theo công ty".', 'Bảng hiện "Chọn công ty để xem thẻ kho.".'], 37)
S2.add('Chữ đỏ tự tắt khi chọn đủ', 'P1', PRE, [MENU, 'Bấm Tìm kiếm.', PICK], '—',
       ['Chữ đỏ dưới ô Hàng hóa biến mất ngay khi chọn hàng; báo cáo tự tải.'], 37)
S2.add('Lọc theo Kỳ Năm trước', 'P0', PRE, OPEN + ['Chọn Kỳ = Năm trước.'], 'Kỳ: Năm trước',
       ['Dòng tiêu đề "Thẻ kho năm 2025 (01/01/2025 – 31/12/2025)".', 'Tồn đầu kỳ ẩn (= 0), Nhập 30,312, Xuất 15,171, Tồn cuối kỳ 15,141.',
        '332 chứng từ (86 nhập, 237 xuất, 9 điều chuyển vị trí).'], [37, 41])
S2.add('Lọc theo Kỳ Tuỳ chọn', 'P0', PRE, OPEN + ['Chọn Kỳ = Tuỳ chọn.', 'Chọn Thời gian 01/10/2026 sang 31/10/2026.'],
       ['Kỳ: Tuỳ chọn', 'Thời gian: 01/10/2026 – 31/10/2026'],
       ['Bước 3: hiện ô Thời gian bắt buộc, bảng "Chọn đủ từ ngày và đến ngày để xem thẻ kho.".',
        'Bước 4: Tồn đầu kỳ 1,595, Nhập 2,472, Xuất 870, Tồn cuối kỳ 3,197; 30 chứng từ (9 nhập, 20 xuất, 1 điều chuyển).'], [37, 41])
S2.add('Kỳ Tuỳ chọn thiếu 1 ngày', 'P1', PRE, OPEN + ['Chọn Kỳ = Tuỳ chọn, chỉ chọn Từ ngày 01/10/2026.', 'Bấm Tìm kiếm.'], '—',
       ['Chữ đỏ "Vui lòng chọn đủ từ ngày và đến ngày", không tải.'], 37)
S2.add('Đổi Kỳ khác Tuỳ chọn xóa khoảng ngày', 'P2', PRE, OPEN + ['Chọn Tuỳ chọn 01/10–31/10/2026.', 'Đổi Kỳ = Tháng này.', 'Đổi lại Tuỳ chọn.'],
       '—', ['Bước 4: ô Thời gian trống, phải chọn lại.'], 37)
S2.add('Lọc theo Kỳ Tuần này / Tháng này', 'P1', PRE, OPEN + ['Chọn Kỳ = Tháng này.', 'Chọn Kỳ = Tuần này.'], '—',
       ['Tháng này: tiêu đề "Thẻ kho tháng 11/2026 (01/11/2026 – 30/11/2026)".', 'Tuần này: tiêu đề "Thẻ kho tuần này (<thứ Hai> – <Chủ nhật>)".',
        'Tồn đầu kỳ = tồn cuối ngày trước kỳ.'], 37)
S2.add('Lọc theo Kho', 'P0', PRE, OPEN + ['Chọn Kho = PTT - Phan Trọng Tuệ.'], 'Kho: PTT - Phan Trọng Tuệ',
       ['Công ty thuê kho tự chọn DTTDETEK, TPE, TPHP, TPV; hiện 4 cột Nhà / Dãy / Khoang / Vị trí.',
        'Tồn đầu 15,141, Nhập 11404, Xuất 23348, Tồn cuối 3,197; 514 chứng từ.', 'Dòng tiêu đề "Kho: PTT - Phan Trọng Tuệ".'], [37, 41])
S2.add('Lọc theo Công ty thuê kho', 'P0', PRE, OPEN + ['Chọn Kho = PTT.', 'Bỏ hết công ty thuê, chỉ để TPE.'], 'Công ty thuê kho: TPE',
       ['Nhập 11,248, Xuất 23,192, Tồn cuối 3,197; 510 chứng từ (bỏ 4 chứng từ của công ty thuê khác).'], [37, 38])
S2.add('Bỏ hết công ty thuê = mọi công ty thuê của kho', 'P1', PRE, OPEN + ['Chọn Kho = PTT.', 'Bấm × bỏ hết Công ty thuê kho.'], '—',
       ['Số liệu như khi tick đủ 4 công ty thuê (514 chứng từ).'], 37)
S2.add('Lọc theo Nhà / Vị trí', 'P1', PRE, OPEN + ['Chọn Kho = PTT.', 'Tick Vị trí "PTT-N1-KV7 - Khu vực 7".'], '—',
       ['Chỉ còn chứng từ có lô tại PTT-N1-KV7; Tồn cuối kỳ = tồn của hàng tại vị trí đó.',
        'Tick Nhà "N1 - Nhà 1" mà không tick Dãy con sang lấy mọi vị trí của Nhà 1.'], [37, 38])
S2.add('Lọc theo Loại báo cáo', 'P0', PRE, OPEN + ['Chọn Loại báo cáo = Không nhặt điều chuyển.'], 'Loại báo cáo: Không nhặt điều chuyển',
       ['Nhập 7,279, Xuất 19,223; Tồn đầu 15,141, Tồn cuối 3,197 không đổi.', '500 chứng từ, ô Điều chuyển vị trí ẩn, bảng không còn PĐCVT-….'],
       [37, 41])
S2.add('Tìm theo số chứng từ chính xác', 'P0', PRE, OPEN + ['Nhập "PĐCVT-00584" ở ô Số chứng từ / Diễn giải, Enter.'],
       'Số chứng từ / Diễn giải: PĐCVT-00584', ['Chỉ còn 1 dòng PĐCVT-00584, "Hiển thị 1–1 / 1 chứng từ".',
                                                 'Khối tổng hợp, dòng TỔNG vẫn 510 chứng từ; SL tồn của dòng 12,753.'], [26, 39])
S2.add('Tìm theo một phần số chứng từ', 'P0', PRE, OPEN + ['Nhập "PNL", Enter.'], 'Số chứng từ / Diễn giải: PNL',
       ['Còn 1 dòng PNL-00023, SL tồn 6,619 (giữ nguyên như khi không lọc).'], 27)
S2.add('Tìm theo diễn giải', 'P1', PRE, OPEN + ['Nhập "sai triết khấu", Enter.'], '—',
       ['Còn các dòng diễn giải chứa "sai triết khấu" (vd PNK-03764 "bán trả lại do sai triết khấu").'], 27)
S2.add('Không phân biệt hoa / thường', 'P1', PRE, OPEN + ['Nhập "pxk-12602", Enter.'], '—', ['Ra PXK-12602.'], 28)
S2.add('Có dấu / không dấu', 'P2', PRE, OPEN + ['Nhập "sai triet khau", Enter.'], '—',
       ['Không ra dòng nào: so khớp có dấu (gõ đúng dấu mới khớp).'], 29)
S2.add('Từ khóa không tồn tại', 'P1', PRE, OPEN + ['Nhập "999999999", Enter.'], '—', ['"Không có chứng từ nào khớp bộ lọc.".'], [30, 40])
S2.add('Ký tự đặc biệt', 'P2', PRE, OPEN + ['Nhập "@#$<>", Enter.', 'Nhập "%", Enter.'], '—',
       ['Không lỗi; "@#$<>" không ra dòng nào; "%" chỉ khớp dòng chứa ký tự %.'], 31)
S2.add('Khoảng trắng đầu / cuối', 'P1', PRE, OPEN + ['Nhập "  PXK-12602  ", Enter.'], '—', ['Ra PXK-12602.'], 32)
S2.add('Giới hạn ký tự ô tìm', 'P2', PRE, OPEN + ['Dán chuỗi 300 ký tự, Enter.'], '—',
       ['Ô nhận đủ (không giới hạn), không lỗi, "Không có chứng từ nào khớp bộ lọc.".'], 33)
S2.add('Xóa từ khóa', 'P1', 'Đang tìm "PNL", bảng còn 1 dòng.', ['Bấm × trong ô Số chứng từ / Diễn giải.', 'Bấm Tìm kiếm.'], '—',
       ['Hiện lại đủ 510 chứng từ.'], 34)
S2.add('Áp từ khóa bằng Enter hoặc nút Tìm kiếm', 'P1', PRE, OPEN + ['Nhập "PNL", chưa Enter.', 'Nhấn Enter.', 'Xóa, nhập lại, bấm Tìm kiếm.'],
       '—', ['Bước 3: bảng chưa đổi.', 'Bước 4 và 5: bảng còn PNL-00023.'], 35)
S2.add('Kết hợp nhiều tiêu chí', 'P0', PRE, OPEN + ['Chọn Kỳ Tuỳ chọn 01/10–31/10/2026.', 'Chọn Loại báo cáo = Không nhặt điều chuyển.',
                                                   'Nhập "PNK", Enter.'], '—',
       ['Chỉ còn phiếu nhập kho tháng 10/2026, không có điều chuyển; khối tổng hợp theo tháng 10 không điều chuyển.'], [38, 39])
S2.add('Tổng số và phân trang sau lọc', 'P1', PRE, OPEN + ['Nhập "PNK", Enter.'], '—',
       ['"Hiển thị 1–20 / <số phiếu nhập kho> chứng từ"; phân trang theo số dòng khớp.'], [41, 42])
S2.add('Thứ tự sau lọc', 'P2', PRE, OPEN + ['Nhập "PNK", Enter.'], '—', ['Các dòng vẫn theo ngày tăng dần, SL tồn giữ giá trị lũy kế gốc.'], 43)
S2.add('Xóa lọc', 'P0', PRE, OPEN + ['Chọn Kho PTT, Loại báo cáo = Không nhặt điều chuyển, nhập "PNK".', 'Bấm Xóa lọc.'], '—',
       ['Bộ lọc về mặc định: Năm nay, công ty TPE, Tất cả; Hàng hóa trống.', 'Bảng hiện "Chọn hàng hóa để xem thẻ kho.", khối tổng hợp ẩn.'], 44)
S2.add('Đổi công ty bỏ kho đã chọn', 'P1', [ACC_A, HANG], [MENU, PICK, 'Chọn Kho = PTT.', 'Đổi Tồn theo công ty sang CN Hải Phòng.'], '—',
       ['Ô Kho tự trống, 4 cột vị trí ẩn; danh sách Kho đổi theo kho của CN Hải Phòng.'], 38)
S2.add('Bỏ hết kho ẩn cột vị trí', 'P2', PRE, OPEN + ['Chọn Kho PTT, tick 1 vị trí.', 'Bỏ Kho.'], '—',
       ['4 cột Nhà / Dãy / Khoang / Vị trí ẩn, tick bị xóa, Công ty thuê kho trống.'], 38)
S2.add('Chuyển màn rồi quay lại', 'P1', PRE, OPEN + ['Mở màn khác (Báo cáo tồn theo kho).', MENU], '—',
       ['Bộ lọc về mặc định, Hàng hóa trống (rời màn thì xóa bộ lọc ghi tạm).'], 45)
S2.add('Tải lại trang (F5)', 'P1', PRE, OPEN + ['Chọn Kho PTT.', 'Nhấn F5 trong vòng 10 phút.'], '—',
       ['Khôi phục Hàng hóa ENEO-640-V5236, Kho PTT, tick vị trí còn hợp lệ; báo cáo tự tải.'], 46)
S2.add('Mở tab mới', 'P2', PRE, OPEN + ['Mở tab mới, vào menu Thẻ kho trong 10 phút.'], '—',
       ['Tab mới khôi phục bộ lọc ghi tạm của trình duyệt (cùng hàng hóa).'], 47)
S2.add('Tài khoản khác cùng trình duyệt', 'P2', PRE, OPEN + ['Đăng xuất, đăng nhập T trên cùng trình duyệt trong 10 phút.', MENU], '—',
       ['Bộ lọc ghi tạm theo trình duyệt nên có thể khôi phục hàng hóa đã chọn; công ty luôn về công ty của T (T không có quyền xem công ty khác).'], 48)
S2.add('Chọn hàng hóa: mở cửa sổ', 'P0', PRE, [MENU, 'Bấm ô Hàng hóa.'], '—',
       ['Mở cửa sổ "Chọn hàng hóa", dòng mô tả "Công ty CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT".',
        'Có cây catalog, ô tìm, công tắc Còn tồn, Gồm hàng ngoài catalog (bật), bảng hàng, chân "Bấm vào tên hàng để chọn", nút Đóng.'], 37)
S2.add('Chọn hàng hóa: tìm và chọn', 'P0', PRE, [MENU, 'Bấm ô Hàng hóa.', 'Gõ "ENEO-640-V5236", Enter.', 'Bấm tên hàng.'], '—',
       ['Bước 3: 1 hàng thoả bộ lọc, Tồn bán được "TPE: 2,586 · TPHP: 28 · TPV: 1".',
        'Bước 4: cửa sổ đóng, ô Hàng hóa "ENEO-640-V5236 - Dầu nhớt…", thẻ kho tự tải.'], [37, 26])
S2.add('Chọn hàng hóa: đóng không chọn', 'P1', [PRE, 'Đang xem thẻ kho ENEO-640-V5236.'], ['Bấm ô Hàng hóa.', 'Bấm Đóng (hoặc ×, hoặc click ra ngoài).'],
       '—', ['Cửa sổ đóng, không hỏi xác nhận; ô Hàng hóa và thẻ kho giữ nguyên.'], 37)
S2.add('Chọn hàng hóa: hàng chưa kinh doanh tại công ty', 'P2', [PRE, 'Hàng H2 chưa kinh doanh tại TPE nhưng có tồn đầu kỳ ở TPE.'],
       [MENU, 'Bấm ô Hàng hóa, tìm H2.'], '—', ['H2 vẫn có trong cửa sổ (phạm vi mọi hàng hóa), chọn được và xem thẻ kho.'], 37)
S2.add('Cài đặt bộ lọc: mở cửa sổ', 'P1', PRE, [MENU, 'Bấm Cài đặt bộ lọc.'], '—',
       ['Cửa sổ "Cài đặt bộ lọc" liệt kê 7 ô: Kỳ, Hàng hóa, Tồn theo công ty, Kho, Công ty thuê kho, Loại báo cáo, Số chứng từ / Diễn giải, '
        'tích hết.', 'Có nút Lưu, Khôi phục mặc định, Đóng.'], 36)
S2.add('Cài đặt bộ lọc: ẩn ô và lưu', 'P1', PRE, [MENU, 'Bấm Cài đặt bộ lọc.', 'Bỏ tích "Loại báo cáo", bấm Lưu.'], '—',
       ['Báo "Cập nhật thành công", ô Loại báo cáo ẩn khỏi khối lọc.', 'F5 / đổi trình duyệt vẫn ẩn (lưu theo người dùng).'], 36)
S2.add('Cài đặt bộ lọc: đổi thứ tự, khôi phục, đóng', 'P2', PRE,
       [MENU, 'Bấm Cài đặt bộ lọc.', 'Kéo "Kho" lên đầu, bấm Đóng.', 'Mở lại, bấm Khôi phục mặc định, bấm Lưu.'], '—',
       ['Bước 3: thứ tự không đổi (chưa lưu).', 'Bước 4: về thứ tự khai báo, hiện đủ 7 ô.'], 36)

# ============================================================== III. SỐ LIỆU BÁO CÁO
S3 = Sec(3)
S3.add('Khối Số lượng', 'P0', PRE, OPEN + ['Đọc khối SỐ LƯỢNG.'], '—',
       ['Góc phải "ĐVT Can 4L".', 'Tồn đầu kỳ 15,141; Nhập trong kỳ 11,248; Xuất trong kỳ 23,192; Tồn cuối kỳ 3,197 (kèm "Can 4L").'], 6)
S3.add('Đối soát tồn đầu + nhập - xuất = tồn cuối', 'P0', PRE, OPEN + ['Tính 15,141 + 11,248 - 23,192.'], '—',
       ['Kết quả 3,197 = ô Tồn cuối kỳ = SL tồn dòng TỔNG.'], 6)
S3.add('Tồn cuối kỳ = SL tồn dòng chứng từ cuối', 'P0', PRE, OPEN + ['Bấm » sang trang cuối.', 'Đọc dòng DX (510).'], '—',
       ['Dòng cuối PXK-38052 ngày 21/10/2026, Xuất 6, SL tồn 3,197 = Tồn cuối kỳ.'], 6)
S3.add('SL tồn lũy kế từng dòng', 'P0', PRE, OPEN + ['Đọc 5 dòng đầu.'], '—',
       ['I: 15,141 - 6 = 15,135; II: - 72 = 15,063; III: - 12 = 15,051; IV (PNK-03764, Nhập 144): + 144 = 15,195; V: + 12 = 15,207.',
        'Mỗi dòng: SL tồn = SL tồn dòng trước + Nhập - Xuất.'], 6)
S3.add('Tồn đầu kỳ = tồn cuối kỳ liền trước', 'P0', PRE, OPEN + ['Chọn Kỳ = Năm trước, đọc Tồn cuối kỳ.', 'Chọn Kỳ = Năm nay, đọc Tồn đầu kỳ.'],
       '—', ['Tồn cuối năm 2025 = 15,141 = Tồn đầu năm 2026.'], 6)
S3.add('Đối soát theo tháng', 'P1', PRE, OPEN + ['Chọn Tuỳ chọn 01/10–31/10/2026.'], '—',
       ['1,595 cộng 2,472 trừ 870 bằng 3,197.', 'Kết quả bằng ô Tồn cuối kỳ.'], 6)
S3.add('Khối Chứng từ', 'P0', PRE, OPEN + ['Đọc khối CHỨNG TỪ.'], '—',
       ['Tổng chứng từ 510; Nhập 76; Xuất 424; Điều chuyển vị trí 10 (đơn vị "phiếu").', '76 + 424 + 10 = 510 = N ở "Hiển thị 1–20 / 510 chứng từ".'], 6)
S3.add('Dòng TỔNG', 'P0', PRE, OPEN + ['Đọc dòng TỔNG.'], '—',
       ['"TỔNG" · "PHÁT SINH TRONG KỲ" · "510 chứng từ"; Nhập 11,248, Xuất 23,192, SL tồn 3,197 = khối Số lượng.',
        'Lưu ý: icon thông tin dòng TỔNG ghi "không tính điều chuyển vị trí" nhưng số CÓ tính điều chuyển (khớp khối Số lượng).'], 6)
S3.add('Nhập / Xuất tính cả điều chuyển vị trí', 'P0', PRE, OPEN + ['Ghi Nhập / Xuất ở Loại Tất cả.', 'Chọn Không nhặt điều chuyển.'], '—',
       ['Tất cả: 11,248 / 23,192; Không nhặt: 7,279 / 19,223 — chênh 3,969 = tổng chuyển vào = tổng chuyển ra của 10 phiếu điều chuyển.',
        'Tồn đầu, Tồn cuối không đổi.'], 6)
S3.add('Ô bằng 0 bị ẩn', 'P1', ['Tài khoản DNS Admin.', 'Hàng H3 tại TPE: tồn đầu năm 2026 = 0, chỉ có phiếu nhập, không có điều chuyển.'],
       [MENU, 'Chọn H3.'], '—', ['Ẩn ô Tồn đầu kỳ, Xuất trong kỳ, ô Xuất (phiếu), Điều chuyển vị trí.', 'Tồn cuối kỳ và Tổng chứng từ luôn hiện.'], 6)
S3.add('Cột Nhập / Xuất của dòng chứng từ', 'P0', PRE, OPEN + ['Đọc dòng PNK-03764 và PXK-12602.'], '—',
       ['PNK-03764: Nhập 144, Xuất trống.', 'PXK-12602: Xuất 6, Nhập trống.'], 6)
S3.add('Dòng điều chuyển vị trí', 'P0', PRE, OPEN + ['Nhập "PĐCVT-00584", Enter.'], '—',
       ['Dòng có chữ "Điều chuyển vị trí", Vị trí "8 lô / vị trí", Nhập 432, Xuất 432, SL tồn 12,753 (không đổi so với dòng trước).'], 6)
S3.add('Khớp chứng từ nguồn: phiếu xuất kho', 'P0', [PRE, 'Phiếu xuất kho PXK-15558 (06/02/2026) xuất 2 lô, mỗi lô 6 Can 4L.'],
       OPEN + ['Nhập "PXK-15558", Enter, bung dòng.', 'Bấm số chứng từ, đối chiếu phiếu.'], '—',
       ['Dòng Xuất 12 = 6 + 6; 2 dòng lô tại PTT-N1-D6-K2-T3.', 'Phiếu xuất kho mở ở tab mới có đúng 2 lô, tổng 12 Can 4L.'], 6)
S3.add('Khớp chứng từ nguồn: phiếu nhập kho', 'P0', [PRE, 'Phiếu nhập kho PNK-03764 nhập 144 Can 4L vào PTT-N1-KV7.'],
       OPEN + ['Nhập "PNK-03764", Enter.', 'Bấm số chứng từ.'], '—', ['Dòng Nhập 144, Vị trí PTT-N1-KV7, khớp phiếu nhập kho.'], 6)
S3.add('Lập chứng từ mới thì số liệu tăng / giảm', 'P0', [ACC_A, HANG, 'Ghi lại Nhập / Xuất / Tồn cuối kỳ hiện tại.'],
       ['Ở màn Phiếu nhập kho lập phiếu nhập 10 Can 4L hàng này vào kho PTT, công ty TPE, bấm gửi.', 'Mở lại Thẻ kho, Kỳ Năm nay.'], '—',
       ['Nhập trong kỳ +10, Tồn cuối kỳ +10, Tổng chứng từ +1, Nhập (phiếu) +1.', 'Dòng cuối là phiếu vừa gửi, SL tồn = tồn cũ + 10.'], [6, 274])
S3.add('Khớp Báo cáo tồn kho tổng hợp / chi tiết theo mặt hàng', 'P0', PRE,
       ['Ở Thẻ kho (không chọn kho) đọc Tồn cuối kỳ năm 2026.', 'Mở Báo cáo tồn kho tổng hợp theo mặt hàng: kho PTT, công ty TPE, hàng ENEO-640-V5236, '
        'tính đến ngày hôm nay.', 'Mở Báo cáo tồn kho chi tiết theo mặt hàng cùng điều kiện.'], '—',
       ['Thẻ kho 3,197 = cột TPE ở báo cáo tổng hợp 3,197 = tổng các lô ở báo cáo chi tiết (6 + 1,313 + 6 + 12 + 1,860 = 3,197).'], 6)
S3.add('Khớp Tổng hợp xuất nhập tồn', 'P0', PRE,
       ['Ở Thẻ kho chọn Kho PTT (mọi công ty thuê), Kỳ Năm nay.', 'Mở Tổng hợp xuất nhập tồn: kho PTT, hàng ENEO-640-V5236, Năm nay.'], '—',
       ['Cả 2 màn: Tồn đầu 15,141, Nhập 11404, Xuất 23348, Tồn cuối 3,197.'], 6)
S3.add('Định dạng số', 'P1', PRE, OPEN, '—',
       ['Phân cách hàng nghìn dấu phẩy (15,141), tối đa 2 số lẻ; số 0 ở Nhập / Xuất để trống, SL tồn 0 hiện "0".'], 6)
S3.add('Số liệu theo ĐVT cơ sở', 'P1', [PRE, 'Hàng có 2 ĐVT: Can 4L (hệ số 1), Thùng 6C-4L (hệ số 6).'], OPEN, '—',
       ['Mọi số theo Can 4L; không có ô chọn ĐVT trên bộ lọc.'], 6)
S3.add('Nhập tồn đầu', 'P1', [PRE, 'Hàng H4 có khai báo tồn kho đầu kỳ ngày 05/01/2026 tại TPE: 100.'], [MENU, 'Chọn H4.'], '—',
       ['Dòng "NHAP_TON_DAU_<số>", Diễn giải "Nhập tồn đầu", Nhập 100, NVKD trống, không có liên kết.'], 6)
S3.add('Phiếu bị Không duyệt vẫn trên thẻ kho', 'P1', [PRE, 'Phiếu nhập kho PNK-X đã gửi (ghi tồn) rồi bị Kế toán kho Không duyệt.'],
       OPEN + ['Tìm "PNK-X".'], '—', ['Dòng PNK-X vẫn hiện, số Nhập giữ nguyên (Không duyệt không hoàn tồn).'], 6)
S3.add('Phiếu chưa gửi không lên thẻ kho', 'P1', [PRE, 'Phiếu nhập kho PNK-Y Đang tạo (chưa gửi) cho hàng này.'], OPEN + ['Tìm "PNK-Y".'], '—',
       ['Không có dòng PNK-Y; tổng số không đổi.'], 6)
S3.add('Lọc ô Số chứng từ không đổi tổng', 'P0', PRE, OPEN + ['Nhập "PNL", Enter.'], '—',
       ['Khối tổng hợp vẫn 15,141 / 11,248 / 23,192 / 3,197, 510 chứng từ; dòng TỔNG vẫn "510 chứng từ".'], 6)
S3.add('Dòng tiêu đề khối tổng hợp', 'P1', PRE, OPEN, '—',
       ['Tiêu đề "Thẻ kho năm 2026 (01/01/2026 – 31/12/2026)".', 'Tiếp theo: mã, tên hàng ENEO-640-V5236, "ĐVT Can 4L".',
        'Kho: danh sách 8 kho của công ty TPE (không chọn kho = mọi kho của công ty).'], 6)

# ============================================================== IV. XEM CHI TIẾT CHỨNG TỪ VÀ LÔ / VỊ TRÍ
S4 = Sec(4)
S4.add('Bung một chứng từ', 'P0', PRE, OPEN + ['Bấm mũi tên ở dòng I.'], '—',
       ['Hiện 1 dòng lô STT 1: "TPE-28/11/2025-2715-38465-59-1-18830", Vị trí PTT-N1-KV7, Xuất 6.', 'Ngày, Diễn giải, SL tồn, NVKD dòng lô trống.'],
       [186, 188])
S4.add('Thu chứng từ', 'P1', PRE, OPEN + ['Bấm mũi tên dòng I 2 lần.'], '—', ['Dòng lô ẩn lại, không tải lại.'], 196)
S4.add('Chọn cấp Tất cả cấp', 'P0', PRE, OPEN + ['Ở ô chọn cấp trong tiêu đề cột Chứng từ / Lô chọn "Tất cả cấp (đến Lô / vị trí)".'], '—',
       ['Mọi chứng từ của trang bung lô / vị trí (20 dòng lô ở trang 1).', 'Lựa chọn còn lại: "Chỉ chứng từ" (mặc định).'], 186)
S4.add('Cấp bung áp lại khi đổi trang', 'P1', PRE, OPEN + ['Chọn Tất cả cấp.', 'Sang trang 2.'], '—', ['Trang 2 cũng bung hết; bung không đẩy dòng sang trang khác.'], 197)
S4.add('Dòng lô của điều chuyển', 'P0', PRE, OPEN + ['Nhập "PĐCVT-00584", Enter, bung dòng.'], '—',
       ['8 dòng lô: mỗi lô 1 dòng Xuất tại N1-T2-KV và 1 dòng Nhập tại PTT-N1-KV7 (240, 120, 30, 42).',
        'Tổng Nhập dòng lô 432 = Nhập dòng chứng từ; tổng Xuất 432 = Xuất dòng chứng từ.'], [188, 189])
S4.add('Khớp số dòng lô với dòng chứng từ', 'P0', PRE, OPEN + ['Tìm "PXK-15558", bung.'], '—',
       ['Vị trí dòng chứng từ "2 lô / vị trí" = 2 dòng lô; tổng Xuất 6 + 6 = 12 = Xuất dòng chứng từ.'], 190)
S4.add('Bấm số phiếu xuất kho', 'P0', PRE, OPEN + ['Bấm "PXK-12602".'], '—',
       ['Mở màn chi tiết Phiếu xuất kho PXK-12602 ở TAB MỚI; tab Thẻ kho giữ nguyên bộ lọc, trang.'], [186, 187, 197])
S4.add('Bấm số phiếu nhập kho / điều chuyển', 'P1', PRE, OPEN + ['Bấm "PNK-03764".', 'Bấm "PĐCVT-00584".'], '—',
       ['Mở màn chi tiết Phiếu nhập kho / Phiếu điều chuyển vị trí tương ứng ở tab mới.'], 186)
S4.add('Bấm số phiếu nhập lại', 'P2', PRE, OPEN + ['Tìm "PNL-00023", bấm số chứng từ.'], '—',
       ['Mở màn phiếu nhập lại ở hệ thống cũ (tab mới); không cấu hình địa chỉ hệ thống cũ thì số chứng từ là chữ thường.',
        'Lưu ý: HRM đã có màn Phiếu nhập lại nhưng liên kết vẫn trỏ hệ thống cũ.'], 186)
S4.add('Dòng chỉ đọc, không có nút Lưu', 'P1', PRE, OPEN + ['Bung dòng, quan sát.'], '—',
       ['Không có ô nhập, nút Sửa / Lưu / Xóa / Lịch sử trên bảng.'], [191, 192, 195])
S4.add('Nhập tồn đầu không có liên kết', 'P2', [PRE, 'Hàng H4 có dòng Nhập tồn đầu.'], [MENU, 'Chọn H4, bấm "NHAP_TON_DAU_…".'], '—',
       ['Không mở gì (chữ thường).'], 193)
S4.add('Không có quyền xem chứng từ nguồn', 'P2', [ACC_T, 'T không có quyền xem phiếu xuất kho của phòng khác.'],
       ['Đăng nhập T.', MENU, PICK, 'Bấm "PXK-12602".'], '—', ['Tab mới mở màn phiếu xuất kho, màn đó báo theo quyền của màn (không thấy phiếu).'], 186)

# ============================================================== V. XUẤT DANH SÁCH EXCEL
S5 = Sec(5)
S5.add('Mở cửa sổ xuất Excel', 'P0', PRE, OPEN + ['Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Xuất Excel thẻ kho", nhãn "Kiểu xuất": Đầy đủ (chọn sẵn, "Có cột NVKD (nhân viên lập chứng từ).") và Rút gọn ("Không có cột NVKD.").',
        'Nút Xuất Excel, Hủy.'], [212, 213, 214])
S5.add('Xuất kiểu Đầy đủ', 'P0', PRE, OPEN + ['Bấm Xuất Excel, giữ Đầy đủ, bấm Xuất Excel.'], '—',
       ['Nút đổi "Đang xuất…", tải file "bao_cao_the_kho.xlsx", cửa sổ đóng.',
        'File: logo dòng 1, "Thẻ kho", "Hàng hóa: ENEO-640-V5236 - Dầu nhớt… - Can 4L", Kho, "Từ ngày: 01/01/2026 Đến ngày: 31/12/2026".',
        'Bảng: STT, Ngày chứng từ, Số chứng từ, Diễn giải, Số lượng (Nhập, Xuất), Chi tiết (Lô, Vị trí, SL theo vị trí), SL tồn, NVKD.'],
       [215, 216, 223, 224, 225, 226])
S5.add('Xuất kiểu Rút gọn', 'P1', PRE, OPEN + ['Bấm Xuất Excel, chọn Rút gọn, bấm Xuất Excel.'], '—', ['File không có cột NVKD.'], 217)
S5.add('Không chọn trường', 'P2', PRE, OPEN + ['Bấm Xuất Excel.'], '—',
       ['Excel không cho chọn cột (luôn đủ cột của kiểu); không có trường hợp xuất 0 cột.'], 218)
S5.add('Xuất theo bộ lọc đang hiển thị', 'P0', PRE, OPEN + ['Chọn Loại báo cáo = Không nhặt điều chuyển, nhập "PNK", Enter.', 'Xuất Excel Đầy đủ.'],
       '—', ['File chỉ có phiếu nhập kho, không có điều chuyển; 5 dòng đầu: Tồn đầu 15,141, Nhập 7,279, Xuất 19,223, Tồn cuối 3,197.'], [219, 220])
S5.add('Xuất toàn bộ, không riêng trang', 'P0', PRE, OPEN + ['Đang ở trang 1 (20 chứng từ), Xuất Excel.'], '—',
       ['File có đủ 510 chứng từ (STT 1 sang 510), mỗi chứng từ gộp ô theo số lô.'], [221, 227])
S5.add('Kỳ không có chứng từ', 'P2', ['Hàng H0 không có chứng từ năm 2026.'], [MENU, 'Chọn H0, Xuất Excel.'], '—',
       ['File vẫn tải về, chỉ có 5 dòng tổng hợp (Đơn vị tính, Tồn đầu kỳ, Nhập, Xuất, Tồn cuối kỳ).'], 222)
S5.add('Chưa chọn hàng thì không xuất', 'P1', PRE, [MENU, 'Bấm Xuất Excel.'], '—',
       ['Không mở cửa sổ; chữ đỏ "Vui lòng chọn hàng hóa".'], 222)
S5.add('Dữ liệu file khớp màn hình', 'P0', PRE, OPEN + ['Xuất Excel Đầy đủ, mở file.'], '—',
       ['Dòng 1 PXK-12602: Xuất 6, Lô TPE-28/11/2025-…-18830, Vị trí PTT-N1-KV7, SL theo vị trí 6, SL tồn 15,135, NVKD "Lê Hữu Thắng - HN_DAU".',
        '5 dòng đầu khớp khối Số lượng.'], 228)
S5.add('Định dạng số trong file', 'P1', PRE, OPEN + ['Xuất Excel, mở file.'], '—',
       ['Số lượng là ô số (cộng được), phân cách hàng nghìn; ô 0 để trống trừ dòng tổng hợp và SL tồn; ngày dd/mm/yyyy.'], 229)
S5.add('Tiếng Việt và ký tự đặc biệt', 'P2', PRE, OPEN + ['Xuất Excel, mở file.'], '—',
       ['Diễn giải tiếng Việt có dấu, ký tự &, <, > hiện đúng.'], 230)
S5.add('Bấm Hủy', 'P1', PRE, OPEN + ['Bấm Xuất Excel, bấm Hủy.'], '—', ['Cửa sổ đóng, không tải file.'], 212)
S5.add('Lỗi khi xuất', 'P2', [PRE, 'Máy chủ lỗi khi dựng file.'], OPEN + ['Xuất Excel.'], '—',
       ['Báo "Lỗi khi xuất Excel.", cửa sổ giữ nguyên để bấm lại.'], 222)

# ============================================================== VI. IN BÁO CÁO
S6 = Sec(6)
S6.add('Mở cửa sổ In báo cáo', 'P0', PRE, OPEN + ['Bấm In danh sách.'], '—',
       ['Cửa sổ "In báo cáo": Đầy đủ (chọn sẵn) / Rút gọn; "Chọn cột in": Diễn giải, Nhập, Xuất, Lô, Vị trí, SL theo vị trí, SL tồn, NVKD (tích hết), '
        '"Chọn tất cả"; nút In, Hủy.'], 3)
S6.add('In bản Đầy đủ', 'P0', PRE, OPEN + ['Bấm In danh sách, bấm In.'], '—',
       ['Mở "Xem trước thẻ kho" khổ ngang: letterhead công ty TPE, "BÁO CÁO THẺ KHO", Hàng hóa, Kho, Từ ngày 01/01/2026 Đến ngày 31/12/2026.',
        '5 dòng đầu: Đơn vị tính Can 4L, Tồn đầu 15,141, Nhập 11,248, Xuất 23,192, Tồn cuối 3,197; rồi từng chứng từ.'], 6)
S6.add('In bản Rút gọn', 'P1', PRE, OPEN + ['Bấm In danh sách, chọn Rút gọn, bấm In.'], '—',
       ['Danh sách cột không còn NVKD; bản in không có cột NVKD.'], 3)
S6.add('Chọn bớt cột in', 'P1', PRE, OPEN + ['Bấm In danh sách, bỏ tích Lô, Vị trí, SL theo vị trí, bấm In.'], '—',
       ['Bản in không có nhóm Chi tiết; STT, Ngày chứng từ, Số chứng từ luôn có.'], 3)
S6.add('Bỏ hết cột thì bị chặn', 'P1', PRE, OPEN + ['Bấm In danh sách, bỏ "Chọn tất cả", bấm In.'], '—',
       ['Báo đỏ trong cửa sổ, không đóng, không mở xem trước.'], 3)
S6.add('In theo bộ lọc đang hiển thị', 'P0', PRE, OPEN + ['Nhập "PNL", Enter.', 'In danh sách, In.'], '—',
       ['Bản in chỉ có PNL-00023; 5 dòng đầu vẫn là tổng toàn thẻ kho.'], 6)
S6.add('Vượt trần in', 'P1', ['Tài khoản DNS Admin.', 'Hàng ENEO-408-V5041:01 năm 2026 có 1,526 chứng từ, hơn 2,000 dòng lô.'],
       [MENU, 'Chọn hàng đó.', 'In danh sách, In.'], '—',
       ['Xem trước chỉ hiện "Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc …", không có nút In.'], 6)
S6.add('Chưa chọn hàng thì không in', 'P1', PRE, [MENU, 'Bấm In danh sách.'], '—', ['Không mở cửa sổ; chữ đỏ "Vui lòng chọn hàng hóa".'], 3)
S6.add('Bấm Hủy / đóng xem trước', 'P2', PRE, OPEN + ['In danh sách, bấm Hủy.', 'In danh sách, In, bấm × ở xem trước.'], '—',
       ['Đóng, màn giữ nguyên bộ lọc, trang.'], 3)
S6.add('Bấm In ở xem trước', 'P1', PRE, OPEN + ['In danh sách, In, bấm In ở cửa sổ xem trước.'], '—', ['Mở hộp thoại in của trình duyệt khổ ngang.'], 3)

# ============================================================== VII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S7 = Sec(7)
S7.add('Màn chỉ đọc', 'P0', PRE, OPEN, '—',
       ['Không có Thêm, Sửa, Xóa, Khóa, Import, Lịch sử; mọi thao tác không làm đổi số liệu chứng từ.'], [268, 269, 270])
S7.add('Gửi phiếu xuất kho thì thẻ kho giảm', 'P0', [ACC_A, HANG, 'Ghi lại Tồn cuối kỳ.'],
       ['Ở màn Phiếu xuất kho, lập và gửi phiếu xuất 6 Can 4L hàng này từ kho PTT công ty TPE.', 'Mở lại Thẻ kho.'], '—',
       ['Xuất trong kỳ +6, Tồn cuối kỳ -6, có dòng PXK mới cuối bảng.'], [274, 281])
S7.add('Điều chuyển vị trí: tồn cuối không đổi', 'P0', [ACC_A, HANG, 'Ghi lại số liệu.'],
       ['Ở màn Phiếu điều chuyển vị trí, chuyển 10 Can 4L từ N1-T2-KV sang PTT-N1-KV7 (kho PTT), hoàn tất Đã chuyển.', 'Mở lại Thẻ kho.'], '—',
       ['Nhập +10, Xuất +10, Tồn cuối không đổi; ô Điều chuyển vị trí +1.', 'Chọn Kho PTT và tick riêng vị trí PTT-N1-KV7: tồn tại vị trí đó +10.'],
       [274, 283])
S7.add('Sửa / xóa khai báo tồn đầu kỳ', 'P1', [ACC_A, 'Hàng H4 có khai báo tồn đầu 100.'],
       ['Ở màn Khai báo tồn kho đầu kỳ sửa 100 thành 120.', 'Mở lại Thẻ kho hàng H4.'], '—',
       ['Dòng Nhập tồn đầu 120, SL tồn các dòng sau tăng 20.'], [272, 280])
S7.add('Đổi tên kho / vị trí', 'P2', [ACC_A, HANG], ['Ở danh mục Vị trí đổi tên vị trí PTT-N1-KV7.', 'Mở lại Thẻ kho.'], '—',
       ['Cột Vị trí vẫn theo mã vị trí; 4 cột tick hiện tên mới.'], [278, 279])
S7.add('Kho ngừng hoạt động không còn trong ô Kho', 'P2', [ACC_A, 'Kho K9 của TPE chuyển ngừng hoạt động.'], [MENU, 'Mở ô Kho.'], '—',
       ['Không còn K9 trong ô Kho; khi không chọn kho thì vị trí của K9 cũng không được tính.'], [276, 282])
S7.add('Bộ lọc màn liên quan cập nhật', 'P2', [ACC_A, 'Danh mục kho kế toán thêm công ty thuê TPV cho kho LN.'], [MENU, PICK, 'Chọn Kho LN.'],
       '—', ['Ô Công ty thuê kho có thêm TPV, tự được chọn.'], 282)
S7.add('Phiếu nhập lại cộng lại tồn', 'P1', [PRE, 'Phiếu nhập lại PNL-00023 (06/05/2026).'], OPEN + ['Tìm "PNL".'], '—',
       ['Dòng PNL-00023 ở cột Nhập, SL tồn 6,619; tổng phiếu Nhập có tính phiếu này.'], 274)
S7.add('Không có dữ liệu trùng / mồ côi', 'P2', PRE, OPEN + ['Xuất Excel, kiểm số chứng từ.'], '—',
       ['Mỗi (số chứng từ, loại) chỉ 1 dòng; mọi dòng lô thuộc đúng 1 chứng từ.'], [284, 285, 286])

# ============================================================== VIII. PHÂN QUYỀN
S8 = Sec(8)
S8.add('Quyền "%s": xem công ty mình' % Q1, 'P0', [ACC_T, HANG], ['Đăng nhập T.', MENU, PICK], '—',
       ['Ô Tồn theo công ty chỉ có công ty TPE; xem được thẻ kho 510 chứng từ.', 'In, Xuất Excel dùng được.'], [287, 288, 293, 299])
S8.add('Quyền "%s": chọn công ty khác' % V1, 'P0', [ACC_A, HANG], ['Đăng nhập A.', MENU, PICK, 'Mở ô Tồn theo công ty.'], '—',
       ['Ô có mọi công ty đang hoạt động (6 công ty); chọn CN Hải Phòng thì xem thẻ kho của CN Hải Phòng.'], [287, 299])
S8.add('Không có quyền nào', 'P0', ACC_N, ['Đăng nhập N.', MENU], '—',
       ['Menu Thẻ kho vẫn hiện; mở màn báo "%s", ô Tồn theo công ty không có lựa chọn, bảng không có dữ liệu.' % NOPERM], [287, 295, 296])
S8.add('Không có quyền: In / Xuất bị từ chối', 'P1', ACC_N, ['Đăng nhập N.', MENU, 'Bấm In danh sách, Xuất Excel.'], '—',
       ['Không in / xuất được (chưa có báo cáo; nếu gọi được thì hệ thống báo "%s").' % NOPERM], [293, 295])
S8.add('Không có quyền tổng công ty: không xem được công ty khác', 'P0', [ACC_T, 'Bộ lọc ghi tạm của trình duyệt còn công ty CN Hải Phòng.'],
       ['Đăng nhập T.', MENU, PICK], '—', ['Ô Tồn theo công ty về TPE; số liệu là của TPE, không lộ CN Hải Phòng.'], [297, 299])
S8.add('Kho ngoài công ty bị bỏ qua', 'P1', [ACC_T, 'Đường link / bộ lọc ghi tạm còn kho của công ty khác.'], ['Đăng nhập T.', MENU, PICK], '—',
       ['Kho không thuộc TPE không được tính; không lỗi.'], 297)
S8.add('Đổi quyền giữa thao tác', 'P1', [ACC_T, HANG, 'Quản trị gỡ quyền "%s" của T khi T đang xem thẻ kho.' % Q1],
       ['T đổi Kỳ = Năm trước.'], '—', ['Báo "%s"; giữ số liệu đang hiển thị.' % NOPERM], 298)
S8.add('Không có thao tác Thêm / Sửa / Xóa / Khóa / Lịch sử', 'P1', ACC_A, ['Đăng nhập A.', MENU, PICK], '—',
       ['Không có nút Thêm, Sửa, Xóa, Khóa, Import, Lịch sử ở mọi quyền.'], [289, 290, 291, 292, 294])
S8.add('Super admin', 'P2', 'Tài khoản DNS Admin (Super admin), không gán quyền của màn.', ['Đăng nhập DNS Admin.', MENU], '—',
       ['Mở được, ô Tồn theo công ty có mọi công ty (miễn kiểm 2 quyền).'], 287)

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'SỐ LIỆU BÁO CÁO', S3),
    ('IV', 'XEM CHI TIẾT CHỨNG TỪ VÀ LÔ / VỊ TRÍ', S4),
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
    build_chuan(output_file=OUT, sheet_name='Trang tính1', feature_name='Thẻ kho - Cập nhật ngày 06/11/2026',
                module_name='Thẻ kho', description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai='bao_cao')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))

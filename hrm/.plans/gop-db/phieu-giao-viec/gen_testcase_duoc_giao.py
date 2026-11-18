# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu giao việc được giao" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu').

Chạy: python gen_testcase_duoc_giao.py -> "testcase - Phiếu giao việc được giao.xlsx" (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (xác định từ code 18/11/2026): màn danh sách CHỨNG TỪ có 8 trạng thái (Chờ thực hiện → Đã thanh toán), có Xóa (= chuyển Hủy,
trả số lượng về chứng từ nguồn), Lịch sử thay đổi, In danh sách, Xem chi tiết phiếu — 'danh_muc' không có nhóm IN PHIẾU và trạng thái
phiếu. Màn KHÔNG có Thêm mới / Chỉnh sửa / Khóa / Gửi duyệt / Duyệt / Không duyệt / Hủy riêng / Import → bỏ các nhóm đó. Nút Nhập kết quả
(mở màn Tạo phiếu nhập kết quả, đổi trạng thái phiếu) + nguồn người thực hiện (Phiếu giao công tác) đặt ở RÀNG BUỘC.
Nhóm: I Hiển thị · II Tìm kiếm & lọc (gồm "Cài đặt bộ lọc:") · III Xóa · IV Lịch sử · V Xem chi tiết · VI In phiếu (In danh sách) ·
VII Tùy chỉnh cột · VIII Xuất Excel · IX Ràng buộc (Nhập kết quả, Xem phiếu nhập kết quả, Phiếu giao công tác) · X Phân quyền (cuối).
Mỗi case ghi stt checklist nó phủ (ck) — gen_checklist_duoc_giao.py đọc CK.
Nguồn hành vi (đọc 18/11/2026, nhánh develop): FE pages/customer-care/wr-assign-tasks/**; BE CustomerCare WrAssignTaskService /
Controller / PrintService, WrImportResultStoreService; Assign AssignRequest (ghi người thực hiện khi phiếu công tác đã duyệt).
Số liệu mẫu: dev-hrm 18/11/2026, DNS Admin là người thực hiện của 5 phiếu (đối soát: = Phiếu giao việc lọc Người thực hiện = DNS Admin).
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

OUT = os.path.join(HERE, 'testcase - Phiếu giao việc được giao.xlsx')
MENU = 'Vào phân hệ CSKH sau bán > nhóm "Giao việc" > bấm "Phiếu giao việc được giao".'
ADV = 'Bấm Tìm kiếm nâng cao.'
EMPTY = '"Không có dữ liệu phù hợp."'
CONFLICT = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'
NO_DEL = '"Bạn không có quyền xóa phiếu giao việc này"'

ADMIN = ('Tài khoản DNS Admin là người thực hiện của 5 phiếu giao việc: TPE.PGV.2026018725 (Đang nhập kết quả), TPE.PGV.2026018724 '
         '(Đã nhập kết quả, DNS Admin là thành viên, trưởng nhóm Khúc Ngọc Nghĩa), TPE.PGV.2026018718 và TPE.PGV.2026018713 (Đã duyệt '
         'kết quả), TPE.PGV.2026018712 (Chờ thực hiện, phiếu công tác đã duyệt, chưa có phiếu nhập kết quả).')
P712 = 'Phiếu TPE.PGV.2026018712: Chờ thực hiện, hợp đồng HDDV_TPE_HDQT_26_0003_SHD-20261102_1109_003, khách 29TPHPYE-1, Tổng công 2.00.'
P725 = 'Phiếu TPE.PGV.2026018725: Đang nhập kết quả, có phiếu nhập kết quả TPE.PNKQ.2026009123.'
ACC_A = ('Tài khoản A (kỹ thuật viên, không có quyền nào): là thành viên thực hiện của 3 phiếu (PGV1 Chờ thực hiện, PGV2 Đã nhập kết quả, '
         'PGV3 Đã duyệt kết quả); tạo phiếu PGV4 nhưng không thực hiện.')
ACC_V = 'Tài khoản V: có quyền "Xem phiếu giao việc" mức Tổng công ty, không là người thực hiện của phiếu nào.'
ACC_N = 'Tài khoản N: không có quyền nào, không là người thực hiện của phiếu nào.'

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
     'Màn Phiếu giao việc được giao (CSKH sau bán > Giao việc) là hộp việc của kỹ thuật viên: liệt kê các phiếu giao việc mà người '
     'đăng nhập có tên trong danh sách người thực hiện, để xem chi tiết, Nhập kết quả, Xem phiếu nhập kết quả, xem lịch sử, in và xuất '
     'Excel. Cùng màn với "Phiếu giao việc" nhưng tập phiếu khác.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Phiếu giao việc gốc, trạng thái khác Hủy: Chờ thực hiện, Đang nhập kết quả, Đã nhập kết quả, Đang duyệt kết quả, Đã duyệt kết '
     'quả, Chờ BKS duyệt kết quả, Đang đề nghị thanh toán, Đã thanh toán.\n'
     '- Và người đăng nhập có tên trong danh sách người thực hiện (trưởng nhóm hoặc thành viên).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Hủy (đã xóa).\n- Phiếu mình tạo nhưng không có tên trong người thực hiện.\n'
     '- Phiếu chưa có Phiếu giao công tác đã duyệt (chưa có người thực hiện).\n'
     '- Phiếu ngoài danh sách thực hiện dù có quyền Xem phiếu giao việc mức nào (kể cả Tổng công ty, Super admin).'),
    ('4. Bộ lọc thời gian áp dụng cho',
     '- Ô Thời gian dự kiến: ngày dự kiến bắt đầu từ Từ ngày trở đi và ngày dự kiến kết thúc đến hết Đến ngày.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Chứng từ nguồn (hợp đồng / phiếu bảo hành / yêu cầu lắp đặt / yêu cầu giao việc khác) > phiếu giao việc > người thực hiện.\n'
     '- Phiếu giao việc > phiếu nhập kết quả > duyệt kết quả.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Mỗi phiếu 1 dòng dù có nhiều người thực hiện; cột Người thực hiện hiện trưởng nhóm (không có thì người đầu danh sách).'),
    ('7. Phân quyền cấp',
     '- Màn không cần quyền để mở; dữ liệu theo danh sách người thực hiện.\n'
     '- Xem phiếu giao việc — mức: Phòng ban / Công ty / Tổng công ty: KHÔNG mở rộng màn này, chỉ cho mở màn chi tiết phiếu ngoài danh '
     'sách.\n- Nhập kết quả thực hiện: theo thiết kế cho Nhập kết quả phiếu mình không thực hiện — ở màn này không làm thay đổi gì.\n'
     '- Xóa: người tạo phiếu (không phải quyền).'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a là dòng đầu trang, b là dòng cuối trang, N là tổng số phiếu được giao khớp bộ lọc.\n'
     '- Tổng công định mức: tổng công chính + công phụ, 2 số lẻ.'),
    ('9. Ghi chú đọc bảng',
     '- Bộ lọc chỉ được ghi nhớ khi mở chi tiết phiếu rồi quay lại trong 10 phút; sang màn khác là mất.\n'
     '- Tổng công định mức bằng 0 thì ô để trống (bản in vẫn ghi 0.00).\n'
     '- Nút Xóa rất hiếm khi hiện ở màn này (phiếu có người thực hiện thường đã gắn phiếu công tác) — cần chuẩn bị dữ liệu riêng.\n'
     '- Số hợp đồng / Số phiếu yêu cầu mở ở thẻ trình duyệt mới; một số hợp đồng bán mở hệ thống cũ — chỉ kiểm việc mở đúng.\n'
     '- Lọc Người thực hiện là người khác: chỉ còn phiếu có cả người đó và mình.'),
]

# ===================================================================== I. HIỂN THỊ
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', ADMIN, [MENU], '—',
       ['Mở màn "Phiếu giao việc được giao", tiêu đề trang và tiêu đề bảng "Phiếu giao việc được giao"',
        'Dòng "Hiển thị 1–5 / 5"'], ck=[1, 2])
S1.add('Mục menu nằm đúng nhóm Giao việc', 'P1', ADMIN, ['Vào phân hệ CSKH sau bán.', 'Bấm nhóm "Giao việc" ở menu trái.'], '—',
       ['Nhóm có 4 mục: Phiếu chờ giao việc, Phiếu giao việc, Phiếu giao việc được giao, Phiếu nhập kết quả',
        'Mục "Phiếu giao việc được giao" bấm được, không cần quyền'], ck=[1])
S1.add('Các nút chức năng', 'P1', ADMIN, [MENU], '—',
       ['Khối lọc: ô tìm "Tìm theo số phiếu giao việc", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc',
        'Bảng: nút In danh sách, Xuất Excel, Cấu hình cột hiển thị', 'KHÔNG có nút Tạo mới, Import'], ck=[3])
S1.add('Cột mặc định', 'P0', ADMIN, [MENU], '—',
       ['13 cột: STT, Số phiếu giao việc, Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Người tạo, Người thực hiện, Thời '
        'gian dự kiến, Tổng công định mức, Trạng thái, Ngày tạo, Hành động', 'Không có cột nào bị ẩn mặc định'], ck=[4, 5])
S1.add('Chỉ hiện phiếu mình là người thực hiện', 'P0', ACC_A, ['Đăng nhập tài khoản A.', MENU], '—',
       ['Hiện đúng PGV1, PGV2, PGV3 (N = 3)', 'KHÔNG hiện PGV4 (A tạo nhưng không thực hiện)'], ck=[6])
S1.add('Thành viên (không phải trưởng nhóm) vẫn thấy phiếu', 'P0', ADMIN, [MENU, 'Tìm dòng TPE.PGV.2026018724.'], '—',
       ['Dòng TPE.PGV.2026018724 có trong danh sách', 'Cột Người thực hiện ghi "Khúc Ngọc Nghĩa - 0936078599" (trưởng nhóm), không phải '
        'DNS Admin'], ck=[6])
S1.add('Đối soát số phiếu với màn Phiếu giao việc', 'P0', ADMIN + '\nDNS Admin có quyền Xem phiếu giao việc mức Tổng công ty.',
       [MENU, 'Ghi lại tổng N.', 'Mở "Phiếu giao việc", Tìm kiếm nâng cao, lọc Người thực hiện = DNS Admin.'], 'Người thực hiện: DNS Admin',
       ['Hai màn cùng N = 5', 'Cùng 5 số phiếu'], ck=[6])
S1.add('Trạng thái hiển thị đúng nhãn và màu', 'P0', ADMIN, [MENU], '—',
       ['TPE.PGV.2026018712 nhãn cam "Chờ thực hiện"', 'TPE.PGV.2026018725 nhãn cam "Đang nhập kết quả"',
        'TPE.PGV.2026018724 nhãn xanh lá "Đã nhập kết quả"', 'TPE.PGV.2026018718 nhãn xanh lá "Đã duyệt kết quả"'], ck=[7])
S1.add('Phiếu Hủy không hiện', 'P0', 'Phiếu PGV5 của tài khoản A (người thực hiện) đã bị xóa (trạng thái Hủy).',
       ['Đăng nhập tài khoản A.', MENU, 'Tìm PGV5.'], 'Từ khóa: PGV5', ['Bảng hiện ' + EMPTY], ck=[7])
S1.add('Không là người thực hiện phiếu nào', 'P0', ACC_N, ['Đăng nhập tài khoản N.', MENU], '—',
       ['Bảng hiện ' + EMPTY, 'Chân bảng "Không có phiếu nào."'], ck=[8])
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', ADMIN, [MENU, 'Nhập "ZZZ_KHONG_TON_TAI" vào ô tìm nhanh, bấm Tìm kiếm.'],
       'Từ khóa: ZZZ_KHONG_TON_TAI', ['Bảng hiện ' + EMPTY, 'Dòng tổng 0'], ck=[9])
S1.add('Số dòng mặc định và đổi số dòng', 'P1', 'Tài khoản B là người thực hiện của 25 phiếu.',
       ['Đăng nhập tài khoản B.', MENU, 'Đổi Số dòng/trang sang 20.'], 'Số dòng/trang: 20',
       ['Mặc định 10 dòng, "Hiển thị 1–10 / 25"', 'Sau khi đổi: 20 dòng, về trang 1, "Hiển thị 1–20 / 25"',
        'Lựa chọn: 5, 10, 20, 50, 100'], ck=[10, 11, 18])
S1.add('Chuyển trang trước / sau / đầu / cuối', 'P1', 'Tài khoản B là người thực hiện của 25 phiếu.',
       ['Đăng nhập tài khoản B.', MENU, 'Bấm trang 2, rồi trang cuối, rồi về đầu.'], '—',
       ['Trang 2: "Hiển thị 11–20 / 25", STT từ 11', 'Trang cuối: "Hiển thị 21–25 / 25"',
        'Ở trang đầu nút về đầu / lùi mờ; ở trang cuối nút tiến / về cuối mờ'], ck=[12, 13, 14, 15, 16])
S1.add('Về trang 1 khi đổi bộ lọc', 'P1', 'Tài khoản B là người thực hiện của 25 phiếu, 4 phiếu Chờ thực hiện.',
       ['Đăng nhập tài khoản B.', MENU, 'Bấm trang 2.', ADV, 'Chọn Trạng thái: Chờ thực hiện.'], 'Trạng thái: Chờ thực hiện',
       ['Danh sách về trang 1', '"Hiển thị 1–4 / 4"'], ck=[17])
S1.add('Thứ tự mặc định theo Ngày tạo mới nhất', 'P0', ADMIN, [MENU], '—',
       ['Dòng 1 TPE.PGV.2026018725 (12/11/2026 08:47), dòng 5 TPE.PGV.2026018712 (03/11/2026 22:21)'], ck=[19, 22])
S1.add('Sắp xếp tăng / giảm theo Số phiếu giao việc', 'P1', ADMIN, [MENU, 'Bấm tiêu đề cột Số phiếu giao việc.', 'Bấm lần nữa.'], '—',
       ['Lần 1: tăng dần, dòng 1 TPE.PGV.2026018712', 'Lần 2: giảm dần, dòng 1 TPE.PGV.2026018725'], ck=[20, 21])
S1.add('Sắp xếp Số hợp đồng, Số phiếu yêu cầu, Thời gian dự kiến, Tổng công định mức, Ngày tạo', 'P1', ADMIN,
       [MENU, 'Lần lượt bấm tiêu đề 5 cột.'], '—',
       ['Mỗi cột sắp xếp được tăng / giảm', 'Thời gian dự kiến sắp theo ngày bắt đầu', 'Tổng công định mức: 134.00 đứng cuối khi tăng dần'],
       ck=[20, 21, 22])
S1.add('Cột không hỗ trợ sắp xếp', 'P2', ADMIN, [MENU, 'Bấm tiêu đề cột Khách hàng, Người yêu cầu, Người tạo, Người thực hiện, Trạng thái.'],
       '—', ['Các cột này không có biểu tượng sắp xếp, bấm không đổi thứ tự'], ck=[23])
S1.add('Giữ sắp xếp khi chuyển trang và về trang 1 khi đổi sắp xếp', 'P2', 'Tài khoản B là người thực hiện của 25 phiếu.',
       ['Đăng nhập tài khoản B.', MENU, 'Sắp xếp Tổng công định mức tăng dần.', 'Bấm trang 2.', 'Bấm tiêu đề Ngày tạo.'], '—',
       ['Trang 2 vẫn tăng dần theo Tổng công định mức', 'Đổi sắp xếp sang về trang 1'], ck=[24, 25])
S1.add('Hiển thị cột Tổng công định mức', 'P1', ADMIN + '\nPhiếu PGV0 của A có Tổng công định mức 0.', [MENU], '—',
       ['TPE.PGV.2026018718 ghi "134.00"; các phiếu khác "0.30", "2.00"', 'Phiếu Tổng công bằng 0 để trống ô'], ck=[6])
S1.add('Chuyển sang mục menu Phiếu giao việc rồi quay lại', 'P1', ADMIN + '\nDNS Admin có quyền Xem phiếu giao việc mức Tổng công ty.',
       [MENU, 'Bấm mục "Phiếu giao việc".', 'Bấm lại mục "Phiếu giao việc được giao".'], '—',
       ['Màn Phiếu giao việc hiện nhiều phiếu theo phạm vi quyền (tiêu đề "Phiếu giao việc")',
        'Quay lại: tiêu đề "Phiếu giao việc được giao", đúng 5 phiếu'], ck=[1])

# ===================================================================== II. TÌM KIẾM & LỌC
S2 = Sec(2)
S2.add('Tìm số phiếu chính xác', 'P0', ADMIN, [MENU, 'Nhập "TPE.PGV.2026018712", bấm Tìm kiếm.'], 'Từ khóa: TPE.PGV.2026018712',
       ['Chỉ 1 dòng TPE.PGV.2026018712'], ck=[26, 35])
S2.add('Tìm một phần số phiếu', 'P0', ADMIN, [MENU, 'Nhập "01871", nhấn Enter.'], 'Từ khóa: 01871',
       ['Hiện 3 dòng TPE.PGV.2026018718, 018713, 018712'], ck=[27, 35])
S2.add('Không phân biệt hoa / thường', 'P1', ADMIN, [MENU, 'Nhập "tpe.pgv.2026018725", bấm Tìm kiếm.'], 'Từ khóa: tpe.pgv.2026018725',
       ['Hiện dòng TPE.PGV.2026018725'], ck=[28])
S2.add('Từ khóa có dấu / không dấu', 'P2', ADMIN, [MENU, 'Nhập "Phiếu", bấm Tìm kiếm.'], 'Từ khóa: Phiếu',
       ['Bảng hiện ' + EMPTY + ' (số phiếu không có chữ có dấu)'], ck=[29])
S2.add('Từ khóa không tồn tại', 'P1', ADMIN, [MENU, 'Nhập "PGV999999", bấm Tìm kiếm.'], 'Từ khóa: PGV999999', ['Bảng hiện ' + EMPTY], ck=[30, 40])
S2.add('Ký tự đặc biệt', 'P2', ADMIN, [MENU, 'Nhập "%", bấm Tìm kiếm.', 'Nhập "@#!", bấm Tìm kiếm.'], 'Từ khóa: % ; @#!',
       ['"%" là ký tự đại diện: hiện đủ 5 phiếu', '"@#!" hiện ' + EMPTY + ', không lỗi'], ck=[31])
S2.add('Khoảng trắng đầu / cuối', 'P1', ADMIN, [MENU, 'Nhập "  TPE.PGV.2026018724  ", bấm Tìm kiếm.'], 'Từ khóa có khoảng trắng 2 đầu',
       ['Hiện dòng TPE.PGV.2026018724'], ck=[32])
S2.add('Từ khóa rất dài', 'P2', ADMIN, [MENU, 'Dán chuỗi 300 ký tự, bấm Tìm kiếm.'], 'Chuỗi 300 ký tự "A"',
       ['Ô nhận đủ chuỗi, không báo lỗi', 'Bảng hiện ' + EMPTY], ck=[33])
S2.add('Xóa từ khóa', 'P1', ADMIN, [MENU, 'Tìm "TPE.PGV.2026018712".', 'Xóa hết chữ trong ô, bấm Tìm kiếm.'], '—',
       ['Danh sách hiện lại đủ 5 phiếu'], ck=[34])
S2.add('Giá trị mặc định các ô lọc', 'P1', ADMIN, [MENU, ADV], '—',
       ['8 ô: Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Trạng thái, Người tạo, Người thực hiện, Thời gian dự kiến',
        'Tất cả trống', 'KHÔNG có ô Công ty, Phòng ban'], ck=[36])
S2.add('Lọc Trạng thái', 'P0', ADMIN, [MENU, ADV, 'Chọn Trạng thái: Đã duyệt kết quả.'], 'Trạng thái: Đã duyệt kết quả',
       ['Lọc ngay, hiện 2 dòng TPE.PGV.2026018718, 018713', 'Ô có 8 lựa chọn từ Chờ thực hiện đến Đã thanh toán'], ck=[37, 41])
S2.add('Lọc Số hợp đồng một phần', 'P0', ADMIN, [MENU, ADV, 'Nhập "HDQT" vào Số hợp đồng, bấm Tìm kiếm.'], 'Số hợp đồng: HDQT',
       ['Hiện 2 dòng TPE.PGV.2026018713, 018712', 'Chưa bấm Tìm kiếm thì chưa lọc'], ck=[37])
S2.add('Lọc Số phiếu yêu cầu', 'P0', ADMIN, [MENU, ADV, 'Nhập "YCGVK" vào Số phiếu yêu cầu, nhấn Enter.'], 'Số phiếu yêu cầu: YCGVK',
       ['Hiện 1 dòng TPE.PGV.2026018718 (TPE.YCGVK.2026003065)'], ck=[37])
S2.add('Lọc Khách hàng', 'P1', ADMIN, [MENU, ADV, 'Gõ "TOYOTA" vào Khách hàng, chọn 29TPHPYE-1.'], 'Khách hàng: 29TPHPYE-1',
       ['Gõ dưới 2 ký tự chưa hiện gợi ý', 'Hiện 2 dòng TPE.PGV.2026018713, 018712'], ck=[37])
S2.add('Lọc Người yêu cầu, Người tạo', 'P1', ADMIN, [MENU, ADV, 'Chọn Người yêu cầu: Vũ Tuấn Việt.', 'Làm mới, chọn Người tạo: Nguyễn Thị Thu Hiền.'],
       'Người yêu cầu: Vũ Tuấn Việt\nNgười tạo: Nguyễn Thị Thu Hiền', ['Mỗi lần lọc còn 1 dòng TPE.PGV.2026018725'], ck=[37])
S2.add('Lọc Người thực hiện là người khác', 'P0', ADMIN, [MENU, ADV, 'Chọn Người thực hiện: Khúc Ngọc Nghĩa.'],
       'Người thực hiện: Khúc Ngọc Nghĩa', ['Chỉ còn TPE.PGV.2026018724 (có cả Khúc Ngọc Nghĩa và DNS Admin)',
                                          'Không hiện phiếu của Khúc Ngọc Nghĩa mà DNS Admin không thực hiện'], ck=[37])
S2.add('Lọc Thời gian dự kiến', 'P1', ADMIN, [MENU, ADV, 'Chọn Thời gian dự kiến từ 04/11/2026 đến 07/11/2026.'],
       'Từ 04/11/2026 – Đến 07/11/2026', ['Hiện TPE.PGV.2026018713 (04/11–04/11) và 018712 (04/11–07/11)',
                                           'Hiện cả TPE.PGV.2026018718 (06/11–07/11)',
                                           'Không hiện TPE.PGV.2026018725 (12/11–13/11), 018724 (11/11–13/11)'], ck=[37])
S2.add('Lọc kết hợp nhiều tiêu chí và tìm nhanh', 'P0', ADMIN,
       [MENU, ADV, 'Chọn Trạng thái: Đã duyệt kết quả, Khách hàng 29TPHPYE-1.', 'Nhập "018713" vào ô tìm nhanh, bấm Tìm kiếm.'],
       'Trạng thái: Đã duyệt kết quả\nKhách hàng: 29TPHPYE-1\nTừ khóa: 018713', ['Còn 1 dòng TPE.PGV.2026018713, "Hiển thị 1–1 / 1"'],
       ck=[38, 39, 41])
S2.add('Phân trang và sắp xếp sau lọc', 'P2', 'Tài khoản B là người thực hiện của 25 phiếu, 14 phiếu Đã duyệt kết quả.',
       ['Đăng nhập tài khoản B.', MENU, ADV, 'Chọn Trạng thái: Đã duyệt kết quả.', 'Sắp xếp Ngày tạo tăng dần, bấm trang 2.'], '—',
       ['"Hiển thị 1–10 / 14", 2 trang', 'Trang 2 có 4 dòng, vẫn đúng trạng thái và thứ tự'], ck=[42, 43])
S2.add('Làm mới', 'P0', ADMIN, [MENU, ADV, 'Chọn Trạng thái và nhập ô tìm nhanh.', 'Bấm Làm mới.'], '—',
       ['Mọi ô và ô tìm nhanh về trống, bỏ sắp xếp', 'Danh sách hiện lại đủ 5 phiếu, trang 1'], ck=[44])
S2.add('Giữ bộ lọc khi mở chi tiết rồi quay lại', 'P0', ADMIN,
       [MENU, ADV, 'Chọn Trạng thái: Đã duyệt kết quả.', 'Bấm số phiếu TPE.PGV.2026018718.', 'Bấm Quay lại.'], '—',
       ['Về danh sách vẫn lọc Đã duyệt kết quả (2 dòng), khối lọc vẫn mở'], ck=[45])
S2.add('Sang màn khác thì mất bộ lọc', 'P1', ADMIN, [MENU, ADV, 'Chọn Trạng thái: Đã duyệt kết quả.', 'Bấm menu "Phiếu nhập kết quả".',
                                                    'Bấm lại "Phiếu giao việc được giao".'], '—',
       ['Danh sách đủ 5 phiếu, ô Trạng thái trống (đúng theo code: chỉ giữ khi mở chi tiết)'], ck=[45])
S2.add('Tải lại trang (F5)', 'P2', ADMIN, [MENU, ADV, 'Chọn Trạng thái: Chờ thực hiện.', 'Nhấn F5.'], '—',
       ['Danh sách về đủ 5 phiếu, bộ lọc trống (chưa mở chi tiết nên chưa ghi nhớ)'], ck=[46])
S2.add('Mở tab mới', 'P2', ADMIN, [MENU, 'Lọc Trạng thái: Chờ thực hiện.', 'Mở mục menu ở thẻ trình duyệt mới.'], '—',
       ['Thẻ mới hiện đủ 5 phiếu, không lọc'], ck=[47])
S2.add('Tài khoản khác cùng trình duyệt', 'P2', ADMIN + '\n' + ACC_A,
       [MENU, 'Lọc, mở chi tiết rồi quay lại.', 'Đăng xuất, đăng nhập tài khoản A trong 10 phút, mở màn.'], '—',
       ['Tài khoản A chỉ thấy phiếu của A', 'Bộ lọc ghi nhớ của DNS Admin có thể còn áp lên A (ghi nhớ theo trình duyệt, đúng theo code)'],
       ck=[48])
S2.add('Cài đặt bộ lọc: ẩn ô lọc và lưu', 'P1', ADMIN, [MENU, 'Bấm Cài đặt bộ lọc.', 'Bỏ tích "Người yêu cầu", bấm Lưu.'], '—',
       ['Cửa sổ "Cài đặt bộ lọc" liệt kê 8 mục', 'Thông báo "Cập nhật thành công"', 'Khối lọc không còn ô Người yêu cầu'], ck=[36])
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự, khôi phục mặc định, đóng không lưu', 'P2', ADMIN,
       [MENU, 'Bấm Cài đặt bộ lọc.', 'Kéo "Trạng thái" lên đầu, bấm Lưu.', 'Mở lại, bấm Khôi phục mặc định rồi Đóng.'], '—',
       ['Sau Lưu: Trạng thái đứng đầu khối lọc', 'Khôi phục rồi Đóng: không đổi gì (Trạng thái vẫn đầu)'], ck=[36])
S2.add('Cài đặt bộ lọc riêng với lối vào Phiếu giao việc', 'P2', ADMIN, ['Ẩn ô Người yêu cầu ở màn này.', 'Mở mục "Phiếu giao việc".'],
       '—', ['Màn Phiếu giao việc vẫn có ô Người yêu cầu'], ck=[36])

# ===================================================================== III. XÓA
S3 = Sec(3)
DEL_PRE = ('Tài khoản C tạo phiếu PGV6 (Chờ thực hiện, từ phiếu yêu cầu giao việc khác YCGVK-X đang "Đã giao việc"); phiếu từng gắn phiếu '
           'công tác đã duyệt rồi bị gỡ (cờ phiếu công tác về chưa có) nhưng C vẫn còn trong danh sách người thực hiện.')
S3.add('Điều kiện hiện nút Xóa', 'P0', DEL_PRE + '\n' + ADMIN, ['Đăng nhập tài khoản C, mở màn.', 'Đăng nhập DNS Admin, mở màn.'], '—',
       ['Dòng PGV6 có nút Xóa (thùng rác đỏ)', 'DNS Admin: không dòng nào có nút Xóa (phiếu đã gắn phiếu công tác / không Chờ thực hiện)'],
       ck=[130])
S3.add('Hộp xác nhận xóa', 'P0', DEL_PRE, ['Đăng nhập tài khoản C.', MENU, 'Bấm Xóa ở dòng PGV6.'], '—',
       ['Hộp "Xác nhận xóa", nội dung "Bạn có chắc muốn xóa bản ghi này không?"', 'Nút Xóa (đỏ) và Hủy'], ck=[131, 132])
S3.add('Xóa thành công', 'P0', DEL_PRE, ['Đăng nhập tài khoản C.', MENU, 'Bấm Xóa ở dòng PGV6, bấm Xóa trong hộp.'], '—',
       ['Thông báo "Xóa thành công."', 'PGV6 biến mất khỏi danh sách, tổng giảm 1', 'Phiếu chuyển trạng thái Hủy (không xóa cứng)'],
       ck=[133, 139, 140])
S3.add('Xóa trả lại chứng từ nguồn', 'P0', DEL_PRE, ['Xóa PGV6 như trên.', 'Mở YCGVK-X ở màn Phiếu yêu cầu giao việc khác.',
                                                     'Mở Phiếu chờ giao việc, thẻ Giao việc khác.'], '—',
       ['YCGVK-X về "Chờ giao việc"', 'YCGVK-X xuất hiện lại ở Phiếu chờ giao việc'], ck=[141, 136])
S3.add('Bấm Hủy thì không xóa', 'P0', DEL_PRE, ['Đăng nhập tài khoản C.', MENU, 'Bấm Xóa ở dòng PGV6, bấm Hủy.'], '—',
       ['Hộp đóng, PGV6 vẫn Chờ thực hiện'], ck=[134])
S3.add('Phiếu đã có phiếu công tác / đã đổi trạng thái thì không xóa được', 'P0',
       DEL_PRE + '\nGiữa lúc C mở màn, người khác gắn lại PGV6 vào phiếu công tác.',
       ['Đăng nhập tài khoản C.', MENU, 'Bấm Xóa ở PGV6 (màn chưa tải lại), bấm Xóa.'], '—',
       ['Thông báo ' + CONFLICT, 'Danh sách nạp lại, PGV6 không còn nút Xóa'], ck=[135, 138])
S3.add('Phiếu đã có phiếu nhập kết quả không có nút Xóa', 'P1', ADMIN, [MENU], '—',
       ['TPE.PGV.2026018725, 018724 không có nút Xóa'], ck=[136, 137])
S3.add('Xóa từ màn chi tiết', 'P1', DEL_PRE, ['Đăng nhập tài khoản C.', 'Mở chi tiết PGV6.', 'Bấm Xóa ở cuối trang, bấm Xóa trong hộp.'],
       '—', ['Hộp hỏi "Bạn có chắc muốn xóa phiếu giao việc \'<mã PGV6>\'?"', '"Xóa thành công.", chuyển về màn Phiếu giao việc'], ck=[133])
S3.add('Xóa dòng cuối của trang', 'P2', 'Tài khoản C có 11 phiếu được giao, phiếu thứ 11 đủ điều kiện xóa.',
       ['Đăng nhập tài khoản C.', MENU, 'Bấm trang 2, xóa dòng duy nhất.'], '—', ['Sau khi xóa tự lùi về trang 1, "Hiển thị 1–10 / 10"'],
       ck=[140])

# ===================================================================== IV. LỊCH SỬ
S4 = Sec(4)
S4.add('Mở cửa sổ lịch sử từ danh sách', 'P0', ADMIN + '\n' + P725, [MENU, 'Bấm Lịch sử ở dòng TPE.PGV.2026018725.'], '—',
       ['Cửa sổ "Lịch sử thay đổi: TPE.PGV.2026018725"', 'Mốc 13/11/2026 10:59 "Thay đổi trạng thái", "Người thực hiện: DNS Admin — HỘI '
        'ĐỒNG QUẢN TRỊ"', '"Trạng thái: Chờ thực hiện sang Đang nhập kết quả", kèm "Phiếu nhập kết quả TPE.PNKQ.2026009123"'],
       ck=[162, 163, 165, 166, 167, 168])
S4.add('Mốc mới nhất ở trên', 'P0', 'Phiếu PGV1 của A có mốc Tạo mới, rồi 2 mốc Thay đổi trạng thái (lưu nháp, gửi duyệt phiếu nhập kết quả).',
       ['Đăng nhập tài khoản A.', MENU, 'Bấm Lịch sử ở PGV1.'], '—', ['Thứ tự: Đang nhập kết quả sang Đã nhập kết quả ở trên cùng, Tạo mới dưới cùng'],
       ck=[164, 176])
S4.add('Lọc theo loại hành động, người thực hiện, thời gian', 'P1', 'Phiếu PGV1 như trên.',
       ['Mở Lịch sử PGV1.', 'Bấm Bộ lọc.', 'Chọn Loại hành động: Thay đổi trạng thái.', 'Chọn Người thực hiện, Từ ngày – Đến ngày.'], '—',
       ['Chọn là lọc ngay', 'Chỉ còn mốc khớp điều kiện'], ck=[169, 170, 171, 172, 175])
S4.add('Lọc không có kết quả và Làm mới', 'P2', 'Phiếu PGV1 như trên.', ['Mở Lịch sử PGV1, Bộ lọc.', 'Chọn Từ ngày 01/01/2020 Đến ngày 02/01/2020.',
                                                                      'Bấm Làm mới.'], '—',
       ['"Không có lịch sử phù hợp bộ lọc."', 'Làm mới: hiện lại đủ mốc'], ck=[173, 174])
S4.add('Phiếu lập trước khi chuyển hệ thống chưa có lịch sử', 'P2', ADMIN, [MENU, 'Bấm Lịch sử ở phiếu cũ không có mốc.'], '—',
       ['"Chưa có lịch sử thao tác nào."'], ck=[164])
S4.add('Xóa phiếu ghi mốc', 'P1', DEL_PRE, ['Xóa PGV6.', 'Ở màn Phiếu giao việc (quyền Tổng công ty) không mở được phiếu Hủy — kiểm mốc qua '
                                              'bộ phận quản trị.'], '—', ['Mốc "Thay đổi trạng thái: Chờ thực hiện sang Hủy" của người xóa'],
       ck=[])
S4.add('Xem, in, xuất không ghi mốc', 'P2', ADMIN, [MENU, 'Mở chi tiết, In danh sách, Xuất Excel.', 'Mở Lịch sử TPE.PGV.2026018725.'], '—',
       ['Không thêm mốc mới'], ck=[182])
S4.add('Đóng cửa sổ lịch sử', 'P1', ADMIN, [MENU, 'Bấm trang 1, lọc Trạng thái.', 'Mở Lịch sử, bấm Đóng (hoặc ×).'], '—',
       ['Cửa sổ đóng, danh sách giữ trang và bộ lọc'], ck=[184, 185])
S4.add('Khối Lịch sử ở màn chi tiết', 'P2', ADMIN + '\n' + P725, ['Mở chi tiết TPE.PGV.2026018725.', 'Bấm Xem lịch sử.'], '—',
       ['Khối mở ra cùng nội dung như cửa sổ ở danh sách', 'Có nút Làm mới, Bộ lọc, Thu gọn'], ck=[162])

# ===================================================================== V. XEM CHI TIẾT
S5 = Sec(5)
S5.add('Mở chi tiết từ Số phiếu', 'P0', ADMIN + '\n' + P712, [MENU, 'Bấm số phiếu TPE.PGV.2026018712.'], '—',
       ['Trang "Chi tiết phiếu giao việc: TPE.PGV.2026018712" mở trong cùng thẻ, nhãn "Chờ thực hiện"'], ck=[186, 187])
S5.add('Đủ thông tin và khớp danh sách', 'P0', ADMIN + '\n' + P712, ['Mở chi tiết TPE.PGV.2026018712.'], '—',
       ['Khối Thông tin khách hàng: Số hợp đồng HDDV_TPE_HDQT_26_0003_SHD-20261102_1109_003, Khách hàng 29TPHPYE-1, Người liên hệ, SĐT, '
        'Địa chỉ lắp đặt, Người yêu cầu, Ngày dự kiến 04/11/2026 – 07/11/2026', 'Khối A - DỊCH VỤ SỬA CHỮA BẢO DƯỠNG, C - CÔNG VIỆC PHỤ, '
        'D - TỔNG HỢP (Tổng công định mức được giao 2.00 = cột danh sách)'], ck=[188, 189, 190])
S5.add('Mọi trường chỉ đọc, không có nút Lưu / Sửa', 'P0', ADMIN, ['Mở chi tiết TPE.PGV.2026018712.'], '—',
       ['Mọi ô bị khóa, Ghi chú không sửa được', 'Không có nút Lưu, Sửa; không có nút Thêm dòng', 'Dấu (*) vẫn hiện ở các ô bắt buộc'],
       ck=[191, 192])
S5.add('Nút chân trang theo trạng thái', 'P0', ADMIN + '\n' + P712 + '\n' + P725,
       ['Mở chi tiết TPE.PGV.2026018712.', 'Mở chi tiết TPE.PGV.2026018725.'], '—',
       ['018712: Nhập kết quả, Quay lại', '018725: Xem phiếu nhập kết quả, Quay lại'], ck=[193])
S5.add('Khối Lịch sử ở chi tiết', 'P2', ADMIN, ['Mở chi tiết TPE.PGV.2026018725.'], '—', ['Có khối Lịch sử (thu gọn), số mốc trên nhãn'], ck=[195])
S5.add('Quay lại giữ trang và bộ lọc', 'P0', 'Tài khoản B là người thực hiện của 25 phiếu.',
       ['Đăng nhập tài khoản B.', MENU, 'Lọc Trạng thái: Đã duyệt kết quả, bấm số phiếu ở dòng 1.', 'Bấm Quay lại.'], '—',
       ['Về "Phiếu giao việc được giao", vẫn lọc Đã duyệt kết quả'], ck=[196, 197])
S5.add('Mở chứng từ nguồn từ chi tiết và danh sách', 'P1', ADMIN, ['Ở danh sách bấm số hợp đồng của TPE.PGV.2026018724.',
                                                                    'Bấm số phiếu yêu cầu TPE.YCGVK.2026003065.'], '—',
       ['Mở chi tiết phiếu bảo hành TPE.PBH.2026.008445 ở thẻ mới', 'Mở chi tiết phiếu yêu cầu giao việc khác ở thẻ mới',
        'Danh sách giữ nguyên'], ck=[188])
S5.add('Phiếu không có quyền xem / không tồn tại', 'P1', ACC_N, ['Đăng nhập tài khoản N.', 'Mở thẳng chi tiết TPE.PGV.2026018712 (dán đường '
                                                                 'dẫn được gửi).', 'Mở chi tiết phiếu đã Hủy.'], '—',
       ['Cả 2 trường hợp chuyển trang không tìm thấy, không hiện dữ liệu'], ck=[186])

# ===================================================================== VI. IN
S6 = Sec(6)
S6.add('Mở xem trước in danh sách', 'P0', ADMIN, [MENU, 'Bấm In danh sách.'], '—',
       ['Cửa sổ "Xem trước danh sách phiếu giao việc", khổ ngang', 'Letterhead công ty người in, tiêu đề "DANH SÁCH PHIẾU GIAO VIỆC"',
        '5 dòng, 12 cột (STT … Ngày tạo), Người lập DNS Admin'], ck=[])
S6.add('In theo bộ lọc', 'P1', ADMIN, [MENU, ADV, 'Lọc Trạng thái: Đã duyệt kết quả.', 'Bấm In danh sách.'], '—', ['Bản in 2 dòng'], ck=[])
S6.add('Bấm In và đóng', 'P1', ADMIN, [MENU, 'Bấm In danh sách.', 'Bấm In.', 'Đóng hộp in, bấm ×.'], '—',
       ['Mở hộp thoại in của trình duyệt', 'Bấm × đóng cửa sổ, danh sách giữ nguyên'], ck=[])
S6.add('In danh sách rỗng', 'P2', ACC_N, ['Đăng nhập tài khoản N.', MENU, 'Bấm In danh sách.'], '—', ['Bản in chỉ có dòng tiêu đề cột'], ck=[])
S6.add('Tổng công định mức trên bản in', 'P2', ADMIN, [MENU, 'Bấm In danh sách.'], '—', ['Cột ghi 2 số lẻ: 0.30, 134.00, 2.00'], ck=[])

# ===================================================================== VII. TÙY CHỈNH CỘT
S7 = Sec(7)
S7.add('Mở cửa sổ và danh sách cột', 'P1', ADMIN, [MENU, 'Bấm Cấu hình cột hiển thị.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột", 13 cột tích sẵn, "Đang chọn 13/13 cột"'], ck=[198, 199, 200])
S7.add('Ẩn và hiện cột', 'P0', ADMIN, [MENU, 'Mở Tuỳ chỉnh cột, bỏ tích "Người yêu cầu", Lưu.', 'Mở lại, tích lại, Lưu.'], '—',
       ['"Cập nhật thành công", cột Người yêu cầu ẩn', 'Lần 2 cột hiện lại'], ck=[201, 202, 206])
S7.add('Cột khóa không ẩn được', 'P1', ADMIN, [MENU, 'Mở Tuỳ chỉnh cột, bấm Bỏ chọn hết.'], '—',
       ['STT, Số phiếu giao việc, Hành động vẫn tích, có ổ khóa, không kéo được'], ck=[203, 205])
S7.add('Kéo đổi thứ tự cột', 'P2', ADMIN, [MENU, 'Kéo "Trạng thái" lên sau Số phiếu giao việc, Lưu.'], '—', ['Bảng hiện cột Trạng thái ở vị trí mới'],
       ck=[204])
S7.add('Đóng không lưu', 'P2', ADMIN, [MENU, 'Bỏ tích "Khách hàng", bấm Đóng.'], '—', ['Bảng vẫn có cột Khách hàng'], ck=[207])
S7.add('Ghi nhớ sau tải lại, theo tài khoản, riêng lối vào', 'P1', ADMIN + '\n' + ACC_A,
       ['Ẩn cột Người yêu cầu, Lưu.', 'Nhấn F5.', 'Mở mục "Phiếu giao việc".', 'Đăng nhập tài khoản A, mở màn.'], '—',
       ['Sau F5 vẫn ẩn', 'Màn Phiếu giao việc vẫn có cột Người yêu cầu', 'Tài khoản A thấy đủ 13 cột'], ck=[208, 209])
S7.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', ADMIN, [MENU, 'Lọc Trạng thái: Đã duyệt kết quả.', 'Ẩn cột Trạng thái, Lưu.'], '—',
       ['Vẫn 2 dòng, bộ lọc giữ nguyên'], ck=[210, 211])

# ===================================================================== VIII. XUẤT EXCEL
S8 = Sec(8)
S8.add('Mở cửa sổ chọn trường', 'P1', ADMIN, [MENU, 'Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất file", 11 trường tích sẵn theo cột đang hiện, "Đang chọn 11/11 trường"'], ck=[212, 213, 214])
S8.add('Xuất mặc định', 'P0', ADMIN, [MENU, 'Bấm Xuất Excel, bấm Xuất file.'], '—',
       ['Tải file danh_sach_phieu_giao_viec.xlsx, thông báo "Xuất Excel thành công."',
        'Tiêu đề "DANH SÁCH PHIẾU GIAO VIỆC", cột STT + 11 cột, 5 dòng khớp màn'], ck=[215, 216, 223, 224, 225, 227, 228])
S8.add('Xuất một số trường và đổi thứ tự', 'P1', ADMIN, [MENU, 'Bấm Xuất Excel, Bỏ chọn hết, tích Trạng thái rồi Số phiếu giao việc, kéo '
                                                              'Số phiếu lên trước.', 'Xuất file.'], '—',
       ['File có STT, Số phiếu giao việc, Trạng thái đúng thứ tự'], ck=[217, 226])
S8.add('Không chọn trường', 'P2', ADMIN, [MENU, 'Bấm Xuất Excel, Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa'], ck=[218])
S8.add('Xuất theo tìm kiếm và bộ lọc', 'P0', ADMIN, [MENU, 'Tìm "01871", lọc Trạng thái: Đã duyệt kết quả.', 'Xuất file.'], '—',
       ['File 2 dòng TPE.PGV.2026018718, 018713'], ck=[219, 220])
S8.add('Xuất toàn bộ khi nhiều trang', 'P0', 'Tài khoản B là người thực hiện của 25 phiếu.', ['Đăng nhập tài khoản B.', MENU, 'Xuất file.'],
       '—', ['File đủ 25 dòng (không chỉ trang đang xem)', 'Có dòng tiến độ "Đã tải …", "Đang dựng file …"'], ck=[221, 227])
S8.add('Danh sách rỗng', 'P1', ACC_N, ['Đăng nhập tài khoản N.', MENU, 'Xuất file.'], '—',
       ['Thông báo "Không có dữ liệu để xuất", không tải file (lệch checklist: không ra file rỗng — đúng theo code)'], ck=[222])
S8.add('Định dạng dữ liệu trong file', 'P1', ADMIN, [MENU, 'Xuất file.'], '—',
       ['Ngày tạo dạng dd/mm/yyyy hh:mm', 'Tổng công định mức là ô số (134 cộng được)', 'Tên khách hàng tiếng Việt đúng dấu'],
       ck=[229, 230])

# ===================================================================== IX. RÀNG BUỘC
S9 = Sec(9)
S9.add('Nhập kết quả: điều kiện hiện nút', 'P0', ADMIN, [MENU], '—',
       ['Chỉ TPE.PGV.2026018712 (Chờ thực hiện, phiếu công tác đã duyệt, chưa có phiếu nhập kết quả) có nút Nhập kết quả',
        'Các phiếu khác không có'], ck=[268])
S9.add('Nhập kết quả: mở màn Tạo phiếu nhập kết quả', 'P0', ADMIN + '\n' + P712, [MENU, 'Bấm Nhập kết quả ở TPE.PGV.2026018712.'], '—',
       ['Mở "Tạo phiếu nhập kết quả", ô Phiếu giao việc = TPE.PGV.2026018712', 'Thông tin khách hàng lấy từ phiếu giao việc',
        'Có nút Lưu, Lưu và gửi duyệt, Quay lại'], ck=[269])
S9.add('Nhập kết quả: lưu nháp đổi trạng thái phiếu', 'P0', ACC_A, ['Đăng nhập tài khoản A.', 'Bấm Nhập kết quả ở PGV1.',
                                                                    'Nhập đủ thông tin, bấm Lưu.', 'Quay lại màn.'], '—',
       ['PGV1 chuyển "Đang nhập kết quả"', 'Nút Nhập kết quả biến mất, thay bằng Xem phiếu nhập kết quả',
        'Lịch sử PGV1 có mốc "Thay đổi trạng thái" kèm mã phiếu nhập kết quả'], ck=[281, 274])
S9.add('Nhập kết quả: gửi duyệt đổi trạng thái', 'P0', ACC_A, ['Mở phiếu nhập kết quả của PGV1, bấm Lưu và gửi duyệt.', 'Mở màn.'], '—',
       ['PGV1 chuyển "Đã nhập kết quả" (nhãn xanh lá)'], ck=[281])
S9.add('Xóa phiếu nhập kết quả thì nút Nhập kết quả hiện lại', 'P1', ACC_A, ['Xóa phiếu nhập kết quả nháp của PGV1.', 'Mở màn.'], '—',
       ['PGV1 về "Chờ thực hiện", có lại nút Nhập kết quả'], ck=[280, 284])
S9.add('Phiếu công tác chưa duyệt thì không có nút Nhập kết quả', 'P0',
       'Phiếu PGV7 Chờ thực hiện của tài khoản A, phiếu công tác chứa PGV7 đang Chờ duyệt (A chưa có trong người thực hiện).',
       ['Đăng nhập tài khoản A.', MENU], '—', ['PGV7 KHÔNG có trong danh sách (người thực hiện chỉ ghi khi phiếu công tác đã duyệt)'],
       ck=[283])
S9.add('Duyệt phiếu công tác thì phiếu xuất hiện', 'P0', 'Như trên; người duyệt duyệt phiếu công tác chứa PGV7.',
       ['Đăng nhập tài khoản A.', MENU], '—', ['PGV7 xuất hiện, có nút Nhập kết quả', 'Cột Người thực hiện hiện trưởng nhóm của phiếu công tác'],
       ck=[274, 282])
S9.add('Gỡ khỏi phiếu công tác thì phiếu biến mất', 'P0', 'PGV7 đang hiện ở màn của A; phiếu công tác bị sửa bỏ A khỏi nhân sự rồi duyệt lại.',
       ['Đăng nhập tài khoản A.', MENU], '—', ['PGV7 không còn trong danh sách của A'], ck=[285, 280])
S9.add('Xem phiếu nhập kết quả', 'P0', ADMIN + '\n' + P725, [MENU, 'Bấm Xem phiếu nhập kết quả ở TPE.PGV.2026018725.'], '—',
       ['Mở "Chi tiết phiếu nhập kết quả: TPE.PNKQ.2026009123"', 'Bấm Quay lại về màn trước'], ck=[274])
S9.add('Xem phiếu nhập kết quả: điều kiện hiện nút', 'P0', ADMIN, [MENU], '—',
       ['Có nút ở 018725, 018724, 018718, 018713', 'TPE.PGV.2026018712 (Chờ thực hiện) không có'], ck=[268])
S9.add('Phiếu không trùng dòng khi nhiều người thực hiện', 'P2', ADMIN, [MENU, 'Tìm TPE.PGV.2026018724.'], '—',
       ['Chỉ 1 dòng dù phiếu có 2 người thực hiện'], ck=[286])
S9.add('Xóa phiếu giao việc trả chứng từ về Phiếu chờ giao việc', 'P1', DEL_PRE, ['Xóa PGV6.', 'Mở Phiếu chờ giao việc.'], '—',
       ['Chứng từ nguồn của PGV6 có lại số lượng chờ giao'], ck=[270, 141])

# ===================================================================== X. PHÂN QUYỀN
S10 = Sec(10)
S10.add('Người thực hiện không có quyền nào vẫn xem được', 'P0', ACC_A, ['Đăng nhập tài khoản A.', MENU], '—',
        ['Mở được màn, thấy 3 phiếu PGV1–PGV3'], ck=[287, 299])
S10.add('Có quyền Xem phiếu giao việc mức Tổng công ty nhưng không thực hiện', 'P0', ACC_V, ['Đăng nhập tài khoản V.', MENU], '—',
        ['Danh sách rỗng ' + EMPTY, 'Quyền xem theo cấp KHÔNG mở rộng màn này'], ck=[299])
S10.add('Có quyền xem theo cấp mở được chi tiết phiếu', 'P0', ACC_V + '\nPGV1 thuộc công ty của V.',
        ['Đăng nhập tài khoản V.', 'Mở thẳng chi tiết PGV1.'], '—', ['Xem được chi tiết PGV1 (chỉ đọc)'], ck=[288])
S10.add('Người tạo nhưng không thực hiện', 'P0', ACC_A, ['Đăng nhập tài khoản A.', MENU, 'Tìm PGV4.'], 'Từ khóa: PGV4',
        ['Không thấy PGV4 ở màn này'], ck=[287, 299])
S10.add('Không có quyền nào, không thực hiện', 'P1', ACC_N, ['Đăng nhập tài khoản N.', MENU], '—',
        ['Mở được màn nhưng rỗng', 'Mở thẳng chi tiết phiếu của người khác sang trang không tìm thấy'], ck=[287, 296])
S10.add('Super admin không đặc cách', 'P0', 'Tài khoản S thuộc vai trò Super admin, không là người thực hiện phiếu nào.',
        ['Đăng nhập tài khoản S.', MENU], '—', ['Danh sách rỗng'], ck=[299])
S10.add('Ẩn nút khi không đủ điều kiện', 'P0', ADMIN, [MENU], '—',
        ['Không dòng nào có Xóa (DNS Admin không thỏa điều kiện người tạo + chưa gắn phiếu công tác)',
         'Nhập kết quả chỉ ở phiếu đủ điều kiện', 'Không có nút Tạo mới, Sửa'], ck=[289, 290, 291, 295])
S10.add('Người thực hiện không phải người tạo thì không xóa', 'P0', 'PGV1 do C tạo, A là người thực hiện; PGV1 đủ điều kiện xóa với C.',
        ['Đăng nhập tài khoản A.', MENU], '—', ['Dòng PGV1 không có nút Xóa'], ck=[291])
S10.add('Quyền Nhập kết quả thực hiện', 'P2', 'Tài khoản D có quyền "Nhập kết quả thực hiện", là người thực hiện của PGV8 (Chờ thực hiện, '
                                               'phiếu công tác đã duyệt).',
        ['Đăng nhập tài khoản D.', MENU], '—', ['Danh sách chỉ có phiếu D thực hiện; PGV8 có Nhập kết quả (do là người thực hiện)'],
        ck=[287])
S10.add('Bị gỡ khỏi người thực hiện giữa lúc thao tác', 'P1', 'A đang mở màn thấy PGV1; phiếu công tác đổi nhân sự bỏ A rồi duyệt.',
        ['A bấm Làm mới.', 'A bấm số phiếu PGV1 (dòng cũ trên màn).'], '—',
        ['Sau Làm mới PGV1 biến mất', 'Mở chi tiết (nếu A không phải người tạo, không có quyền xem) sang trang không tìm thấy'], ck=[298, 297])
S10.add('Lịch sử, in, xuất theo tập phiếu được giao', 'P2', ACC_A, ['Đăng nhập tài khoản A.', MENU, 'Mở Lịch sử PGV1, In danh sách, Xuất Excel.'],
        '—', ['Lịch sử mở được', 'Bản in và file chỉ có 3 phiếu của A'], ck=[293, 294])
S10.add('Đổi công ty đang làm việc', 'P2', ACC_A + '\nA làm việc ở 2 công ty.', ['Đăng nhập tài khoản A.', 'Đổi công ty đang làm việc.', MENU],
        '—', ['Danh sách vẫn là phiếu A thực hiện (không phụ thuộc công ty)'], ck=[299])

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'XÓA', S3),
    ('IV', 'LỊCH SỬ THAY ĐỔI', S4),
    ('V', 'XEM CHI TIẾT PHIẾU GIAO VIỆC', S5),
    ('VI', 'IN PHIẾU – IN DANH SÁCH PHIẾU GIAO VIỆC', S6),
    ('VII', 'TÙY CHỈNH CỘT', S7),
    ('VIII', 'XUẤT DANH SÁCH EXCEL', S8),
    ('IX', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC – NHẬP KẾT QUẢ, PHIẾU GIAO CÔNG TÁC', S9),
    ('X', 'PHÂN QUYỀN', S10),
]

if __name__ == '__main__':
    ids = [(s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
    assert len(ids) == len(set(ids)), 'Trùng mã TC'
    total = len(ids)
    p0 = sum(1 for _, _, s in SECTIONS for tc in s if tc[2] == 'P0')
    print('Tong %d TC, P0 %d (%.0f%%)' % (total, p0, 100.0 * p0 / total))
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='Phiếu giao việc được giao - Cập nhật ngày 18/11/2026',
                module_name='Phiếu giao việc được giao', description_block=DESCRIPTION_BLOCK,
                sections=[(r, t, list(s)) for r, t, s in SECTIONS], loai='phieu')

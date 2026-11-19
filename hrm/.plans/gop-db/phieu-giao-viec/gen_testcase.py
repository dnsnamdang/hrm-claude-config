# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu giao việc" (lối vào ?type=all) — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (xác định từ code 19/11/2026): màn CHỨNG TỪ có 8 trạng thái (Chờ thực hiện → Đã thanh toán), có Tạo phiếu (Lưu và duyệt —
lưu là duyệt, ghi sổ tiến độ giao việc + đổi trạng thái chứng từ nguồn), Xóa (= Hủy, trả số lượng), Lịch sử, In danh sách, Xem chi tiết —
'danh_muc' không có nhóm IN PHIẾU và trạng thái phiếu. Màn KHÔNG có Chỉnh sửa / Khóa / Gửi duyệt / Duyệt riêng / Không duyệt / Hủy riêng /
Import → bỏ các nhóm đó; "Lưu và duyệt" nằm trong THÊM MỚI. Nhập kết quả, Phiếu giao công tác, Phiếu chờ giao việc đặt ở RÀNG BUỘC.
Nhóm: I Hiển thị · II Tìm kiếm & lọc (gồm "Cài đặt bộ lọc:") · III Thêm mới · IV Xóa · V Lịch sử · VI Xem chi tiết · VII In phiếu (In danh
sách) · VIII Tùy chỉnh cột · IX Xuất Excel · X Ràng buộc · XI Phân quyền (cuối).
Mỗi case ghi stt checklist nó phủ (ck) — gen_checklist.py đọc CK.
Nguồn hành vi (đọc 19/11/2026, nhánh develop): FE pages/customer-care/wr-assign-tasks/**; BE CustomerCare WrAssignTaskService / SourceService /
StoreService / StoreRequest / Controller / PrintService; Finance CheckDueConfig. Số liệu mẫu: dev-hrm 19/11/2026, DNS Admin (quyền Tổng công ty).
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
MENU = 'Vào phân hệ CSKH sau bán > nhóm "Giao việc" > bấm "Phiếu giao việc".'
CHO = 'Vào phân hệ CSKH sau bán > nhóm "Giao việc" > bấm "Phiếu chờ giao việc".'
ADV = 'Bấm Tìm kiếm nâng cao.'
EMPTY = '"Không có dữ liệu phù hợp."'
CONFLICT = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'
NO_DEL = '"Bạn không có quyền xóa phiếu giao việc này"'
REQ = '"Bắt buộc phải nhập"'

ADMIN = ('Tài khoản DNS Admin có quyền "Xem phiếu giao việc" mức Tổng công ty; danh sách có 9.876 phiếu (Chờ thực hiện 897, Đang nhập kết '
         'quả 6, Đã nhập kết quả 319, Đang duyệt kết quả 4, Đã duyệt kết quả 8.650).')
P712 = 'Phiếu TPE.PGV.2026018712: từ hợp đồng HDDV_TPE_HDQT_26_0003_SHD-20261102_1109_003, Chờ thực hiện, phiếu giao công tác đã duyệt, DNS Admin là người thực hiện, Tổng công 2.00.'
P709 = 'Phiếu TPE.PGV.2026018709: DNS Admin tạo, Chờ thực hiện, chưa gắn phiếu giao công tác (đủ điều kiện Xóa).'
P725 = 'Phiếu TPE.PGV.2026018725: Đang nhập kết quả, có phiếu nhập kết quả TPE.PNKQ.2026009123.'
ACC_C = 'Tài khoản C: quyền "Xem phiếu giao việc" mức Công ty, công ty đang làm việc là công ty 1 (9.096 phiếu do người công ty 1 lập).'
ACC_P = ('Tài khoản P: quyền "Xem phiếu giao việc" mức Phòng ban, quản lý phòng 51 của công ty 1 (3.026 phiếu do người phòng 51 lập); '
         'P tự tạo 2 phiếu khi đang ở phòng khác.')
ACC_N = 'Tài khoản N: không có quyền nào, không tạo phiếu nào, không là người thực hiện phiếu nào.'
ACC_A = 'Tài khoản A: không có quyền Xem; tạo 2 phiếu (PGV1, PGV2) và là người thực hiện của 3 phiếu khác (PGV3, PGV4, PGV5).'
ACC_L = ('Tài khoản L: có quyền "Tạo phiếu giao việc", thuộc phòng tiếp nhận của hợp đồng HĐ-X ("Có hiệu lực", thiết bị Máy nén khí: SL '
         'kỹ thuật 3, đã giao 1, SL còn 2; có 1 dịch vụ SL còn 2, 1 vật tư SL còn 5, 1 vật tư bán thêm SL còn 4).')
SRC = 'Ở tab Hợp đồng, bấm Tạo phiếu giao việc ở dòng HĐ-X.'

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
     'Màn Phiếu giao việc (CSKH sau bán > Giao việc) là màn quản lý phiếu giao việc cho kỹ thuật: xem danh sách theo phạm vi quyền, tạo '
     'phiếu từ chứng từ chờ giao việc (hợp đồng, phụ lục bổ sung, phiếu bảo hành, yêu cầu lắp đặt bàn giao, yêu cầu giao việc khác), xem '
     'chi tiết, xóa (hủy) phiếu, nhập kết quả, xem lịch sử, in và xuất Excel. Cùng màn với "Phiếu giao việc được giao" nhưng khác tập phiếu.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Phiếu giao việc gốc, trạng thái khác Hủy: Chờ thực hiện, Đang nhập kết quả, Đã nhập kết quả, Đang duyệt kết quả, Đã duyệt kết '
     'quả, Chờ BKS duyệt kết quả, Đang đề nghị thanh toán, Đã thanh toán.\n'
     '- Trong phạm vi: Tổng công ty = mọi phiếu; Công ty = phiếu công ty đang làm việc + phiếu mình tạo; Phòng ban = phiếu phòng mình quản '
     'lý + phiếu mình tạo; không có quyền Xem = phiếu mình tạo + phiếu mình là người thực hiện (nếu có).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Hủy (đã xóa).\n- Phiếu ngoài phạm vi quyền.\n- Phiếu duyệt kết quả (phiếu con) không hiện thành dòng riêng.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     '- Ô Thời gian dự kiến: ngày dự kiến bắt đầu từ Từ ngày trở đi và ngày dự kiến kết thúc đến hết Đến ngày.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Chứng từ nguồn > phiếu giao việc > thiết bị > công tháo lắp / dịch vụ / vật tư.\n'
     '- Phiếu giao việc > phiếu giao công tác (người thực hiện) > phiếu nhập kết quả > duyệt kết quả.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Mỗi phiếu 1 dòng dù nhiều người thực hiện; cột Người thực hiện hiện trưởng nhóm.\n'
     '- Một chứng từ lập được nhiều phiếu (giao nhiều lần) đến khi hết số lượng còn.\n'
     '- Khối Tổng hợp gộp số lượng dịch vụ theo dịch vụ, vật tư theo hàng hóa.'),
    ('7. Phân quyền cấp',
     '- Xem phiếu giao việc — mức: Tổng công ty / Công ty / Phòng ban.\n'
     '- Tạo phiếu giao việc: cần khi lập từ hợp đồng, phụ lục bổ sung, phiếu bảo hành (kèm điều kiện phòng tiếp nhận với hợp đồng, phụ lục); '
     'lập từ yêu cầu lắp đặt / giao việc khác chỉ cần thuộc phòng tiếp nhận.\n'
     '- Nhập kết quả thực hiện: theo thiết kế cho nhập kết quả phiếu mình không thực hiện (hiện chưa có tác dụng).\n'
     '- Xóa: người tạo phiếu (không phải quyền). Không đặc cách Super admin.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": N là tổng số phiếu trong phạm vi khớp bộ lọc.\n'
     '- SL tính công khoán (lắp đặt) = làm tròn lên (SL bàn giao / SL người tính công); Tổng công dòng = SL tính công khoán x Định mức công.\n'
     '- Công chính = bảo hành + sửa chữa (dòng có SL giao khác 0) + bảo dưỡng (dịch vụ có SL khác 0) + lắp đặt + dịch vụ đính kèm; Công '
     'phụ = tổng ĐM công công phụ P3; Tổng công định mức = Công chính + Công phụ, 2 số lẻ.'),
    ('9. Ghi chú đọc bảng',
     '- Không có nút Tạo mới trên danh sách: tạo từ Phiếu chờ giao việc (hoặc từ phiếu yêu cầu lắp đặt / giao việc khác).\n'
     '- Lưu và duyệt là lưu luôn ở Chờ thực hiện, không có nháp, không sửa được sau khi lưu.\n'
     '- Số lượng giao vượt SL còn báo đỏ ngay khi gõ, KHÔNG tự sửa về SL còn.\n'
     '- Tổng công định mức bằng 0 thì ô danh sách để trống (bản in ghi 0.00).\n'
     '- In tối đa 2.000 dòng: tài khoản Tổng công ty phải lọc trước khi in.\n'
     '- Số hợp đồng bán của phiếu lắp đặt có thể mở ở hệ thống cũ — chỉ kiểm việc mở đúng.'),
]

# ===================================================================== I. HIỂN THỊ
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', ADMIN, [MENU], '—',
       ['Tiêu đề trang và tiêu đề bảng "Phiếu giao việc"', 'Dòng "Hiển thị 1–10 / 9876"'], ck=[1, 2])
S1.add('Mục menu nằm đúng nhóm Giao việc', 'P1', ADMIN, ['Vào phân hệ CSKH sau bán.', 'Bấm nhóm "Giao việc".'], '—',
       ['Nhóm có 4 mục: Phiếu chờ giao việc, Phiếu giao việc, Phiếu giao việc được giao, Phiếu nhập kết quả',
        'Mục "Phiếu giao việc" bấm được, không cần quyền'], ck=[1])
S1.add('Các nút chức năng', 'P1', ADMIN, [MENU], '—',
       ['Khối lọc: ô tìm "Tìm theo số phiếu giao việc", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc',
        'Bảng: In danh sách, Xuất Excel, Cấu hình cột hiển thị', 'KHÔNG có nút Tạo mới, Import'], ck=[3])
S1.add('Cột mặc định', 'P0', ADMIN, [MENU], '—',
       ['13 cột: STT, Số phiếu giao việc, Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Người tạo, Người thực hiện, Thời '
        'gian dự kiến, Tổng công định mức, Trạng thái, Ngày tạo, Hành động', 'Không có cột nào bị ẩn mặc định'], ck=[4, 5])
S1.add('Dữ liệu dòng khớp chi tiết phiếu', 'P0', ADMIN + '\n' + P712, [MENU, 'Tìm dòng TPE.PGV.2026018712.'], '—',
       ['Số hợp đồng HDDV_TPE_HDQT_26_0003_SHD-20261102_1109_003, Khách hàng "29TPHPYE-1-CÔNG TY TNHH TOYOTA HÀ ĐÔNG"',
        'Thời gian dự kiến "04/11/2026-07/11/2026", Tổng công định mức "2.00", Ngày tạo "03/11/2026 22:21"'], ck=[6])
S1.add('Phiếu giao việc khác: Số hợp đồng trống, có Số phiếu yêu cầu', 'P1', ADMIN, [MENU, 'Tìm dòng TPE.PGV.2026018717.'], '—',
       ['Số hợp đồng trống', 'Số phiếu yêu cầu TPE.YCGVK.2026003064', 'Tổng công định mức "60.00"'], ck=[6])
S1.add('Trạng thái hiển thị đúng nhãn và màu', 'P0', ADMIN, [MENU], '—',
       ['TPE.PGV.2026018712 nhãn cam "Chờ thực hiện"', 'TPE.PGV.2026018725 nhãn cam "Đang nhập kết quả"',
        'TPE.PGV.2026018724 nhãn xanh lá "Đã nhập kết quả"', 'TPE.PGV.2026018718 nhãn xanh lá "Đã duyệt kết quả"'], ck=[7])
S1.add('Phiếu Hủy không hiện', 'P0', 'Phiếu PGV9 của tài khoản A đã bị xóa (trạng thái Hủy).', ['Đăng nhập tài khoản A.', MENU, 'Tìm PGV9.'],
       'Từ khóa: PGV9', ['Bảng hiện ' + EMPTY], ck=[7])
S1.add('Không có phiếu trong phạm vi', 'P0', ACC_N, ['Đăng nhập tài khoản N.', MENU], '—',
       ['Bảng hiện ' + EMPTY, 'Chân bảng "Không có phiếu nào."'], ck=[8])
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', ADMIN, [MENU, 'Nhập "ZZZ_KHONG_TON_TAI" vào ô tìm nhanh, bấm Tìm kiếm.'],
       'Từ khóa: ZZZ_KHONG_TON_TAI', ['Bảng hiện ' + EMPTY, 'Dòng tổng 0'], ck=[9])
S1.add('Số dòng mặc định và đổi số dòng', 'P1', ADMIN, [MENU, 'Đổi Số dòng/trang sang 20.'], 'Số dòng/trang: 20',
       ['Mặc định 10 dòng', 'Sau khi đổi: 20 dòng, về trang 1, "Hiển thị 1–20 / 9876"', 'Lựa chọn: 5, 10, 20, 50, 100'], ck=[10, 11, 18])
S1.add('Chuyển trang trước / sau / đầu / cuối', 'P1', ADMIN, [MENU, 'Bấm trang 2, rồi trang cuối, rồi về đầu.'], '—',
       ['Trang 2: "Hiển thị 11–20 / 9876", STT từ 11', 'Trang cuối: "Hiển thị 9871–9876 / 9876"',
        'Ở trang đầu nút về đầu / lùi mờ; ở trang cuối nút tiến / về cuối mờ'], ck=[12, 13, 14, 15, 16])
S1.add('Về trang 1 khi đổi bộ lọc', 'P1', ADMIN, [MENU, 'Bấm trang 3.', ADV, 'Chọn Trạng thái: Chờ thực hiện.'], 'Trạng thái: Chờ thực hiện',
       ['Danh sách về trang 1', '"Hiển thị 1–10 / 897"'], ck=[17])
S1.add('Thứ tự mặc định theo Ngày tạo mới nhất', 'P0', ADMIN, [MENU], '—',
       ['Dòng 1 TPE.PGV.2026018725 (12/11/2026 08:47), dòng 2 TPE.PGV.2026018724 (11/11/2026 21:18)'], ck=[19, 22])
S1.add('Sắp xếp tăng / giảm theo Số phiếu giao việc', 'P1', ADMIN, [MENU, 'Bấm tiêu đề cột Số phiếu giao việc.', 'Bấm lần nữa.'], '—',
       ['Lần 1: tăng dần theo số phiếu', 'Lần 2: giảm dần, dòng 1 là số phiếu lớn nhất'], ck=[20, 21])
S1.add('Sắp xếp Số hợp đồng, Số phiếu yêu cầu, Thời gian dự kiến, Tổng công định mức, Ngày tạo', 'P1', ADMIN,
       [MENU, 'Lần lượt bấm tiêu đề 5 cột.'], '—',
       ['Mỗi cột sắp xếp được tăng / giảm', 'Thời gian dự kiến sắp theo ngày bắt đầu', 'Bảng không nhảy bố cục khi sắp xếp'],
       ck=[20, 21, 22])
S1.add('Cột không hỗ trợ sắp xếp', 'P2', ADMIN, [MENU, 'Bấm tiêu đề cột Khách hàng, Người yêu cầu, Người tạo, Người thực hiện, Trạng thái.'],
       '—', ['Các cột này không có biểu tượng sắp xếp, bấm không đổi thứ tự'], ck=[23])
S1.add('Giữ sắp xếp khi chuyển trang và về trang 1 khi đổi sắp xếp', 'P2', ADMIN,
       [MENU, 'Sắp xếp Tổng công định mức tăng dần.', 'Bấm trang 2.', 'Bấm tiêu đề Ngày tạo.'], '—',
       ['Trang 2 vẫn tăng dần theo Tổng công định mức', 'Đổi sắp xếp thì về trang 1'], ck=[24, 25])
S1.add('Hiển thị cột Tổng công định mức', 'P1', ADMIN, [MENU], '—',
       ['TPE.PGV.2026018723 ghi "120,000.00", TPE.PGV.2026018718 ghi "134.00"', 'TPE.PGV.2026018715 (tổng 0) để trống ô'], ck=[6])
S1.add('Người thực hiện trống khi chưa có phiếu giao công tác', 'P1', ADMIN + '\n' + P709, [MENU, 'Tìm TPE.PGV.2026018709.'], '—',
       ['Cột Người thực hiện trống'], ck=[6])
S1.add('Chuyển sang mục "Phiếu giao việc được giao" rồi quay lại', 'P1', ADMIN,
       [MENU, 'Bấm mục "Phiếu giao việc được giao".', 'Bấm lại mục "Phiếu giao việc".'], '—',
       ['Màn "Phiếu giao việc được giao" chỉ có phiếu DNS Admin là người thực hiện', 'Quay lại: tiêu đề "Phiếu giao việc", đủ 9.876 phiếu'],
       ck=[1])
S1.add('Mở Số hợp đồng / Số phiếu yêu cầu từ danh sách', 'P1', ADMIN, [MENU, 'Bấm số hợp đồng của TPE.PGV.2026018712.',
                                                                   'Bấm số phiếu yêu cầu của TPE.PGV.2026018717.'], '—',
       ['Mở chi tiết hợp đồng dịch vụ ở thẻ mới', 'Mở chi tiết phiếu yêu cầu giao việc khác ở thẻ mới', 'Danh sách giữ nguyên'], ck=[6])

# ===================================================================== II. TÌM KIẾM & LỌC
S2 = Sec(2)
S2.add('Tìm số phiếu chính xác', 'P0', ADMIN, [MENU, 'Nhập "TPE.PGV.2026018712", bấm Tìm kiếm.'], 'Từ khóa: TPE.PGV.2026018712',
       ['Chỉ 1 dòng TPE.PGV.2026018712'], ck=[26, 35])
S2.add('Tìm một phần số phiếu', 'P0', ADMIN, [MENU, 'Nhập "01871", nhấn Enter.'], 'Từ khóa: 01871',
       ['Hiện các phiếu có "01871" trong số phiếu (TPE.PGV.2026018718, 018717, 018715, 018713, 018712…)'], ck=[27, 35])
S2.add('Không phân biệt hoa / thường', 'P1', ADMIN, [MENU, 'Nhập "tpe.pgv.2026018725", bấm Tìm kiếm.'], 'Từ khóa: tpe.pgv.2026018725',
       ['Hiện dòng TPE.PGV.2026018725'], ck=[28])
S2.add('Từ khóa có dấu / không dấu', 'P2', ADMIN, [MENU, 'Nhập "Phiếu", bấm Tìm kiếm.'], 'Từ khóa: Phiếu',
       ['Bảng hiện ' + EMPTY + ' (số phiếu không có chữ có dấu)'], ck=[29])
S2.add('Từ khóa không tồn tại', 'P1', ADMIN, [MENU, 'Nhập "PGV999999", bấm Tìm kiếm.'], 'Từ khóa: PGV999999', ['Bảng hiện ' + EMPTY], ck=[30, 40])
S2.add('Ký tự đặc biệt', 'P2', ADMIN, [MENU, 'Nhập "@#!", bấm Tìm kiếm.', 'Nhập "%", bấm Tìm kiếm.'], 'Từ khóa: @#! ; %',
       ['"@#!" hiện ' + EMPTY + ', không lỗi', '"%" là ký tự đại diện: hiện toàn bộ 9.876 phiếu'], ck=[31])
S2.add('Khoảng trắng đầu / cuối', 'P1', ADMIN, [MENU, 'Nhập "  TPE.PGV.2026018724  ", bấm Tìm kiếm.'], 'Từ khóa có khoảng trắng 2 đầu',
       ['Hiện dòng TPE.PGV.2026018724'], ck=[32])
S2.add('Từ khóa rất dài', 'P2', ADMIN, [MENU, 'Dán chuỗi 300 ký tự, bấm Tìm kiếm.'], 'Chuỗi 300 ký tự "A"',
       ['Ô nhận đủ chuỗi, không báo lỗi', 'Bảng hiện ' + EMPTY], ck=[33])
S2.add('Xóa từ khóa', 'P1', ADMIN, [MENU, 'Tìm "TPE.PGV.2026018712".', 'Xóa hết chữ trong ô, bấm Tìm kiếm.'], '—',
       ['Danh sách hiện lại đủ 9.876 phiếu'], ck=[34])
S2.add('Giá trị mặc định các ô lọc', 'P1', ADMIN, [MENU, ADV], '—',
       ['10 ô: Công ty, Phòng ban, Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Trạng thái, Người tạo, Người thực hiện, '
        'Thời gian dự kiến', 'Tất cả trống'], ck=[36])
S2.add('Lọc Công ty và Phòng ban', 'P0', ADMIN, [MENU, ADV, 'Chọn Công ty: CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT.',
                                                 'Chọn Phòng ban: HỘI ĐỒNG QUẢN TRỊ.'],
       'Công ty: CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT\nPhòng ban: phòng 51', ['Sau chọn công ty: "Hiển thị 1–10 / 9096"',
                                                                                  'Sau chọn phòng ban: "Hiển thị 1–10 / 3026"',
                                                                                  'Đổi công ty thì ô Phòng ban bị xóa'], ck=[37])
S2.add('Lọc Trạng thái', 'P0', ADMIN, [MENU, ADV, 'Chọn Trạng thái: Đang duyệt kết quả.'], 'Trạng thái: Đang duyệt kết quả',
       ['Lọc ngay, "Hiển thị 1–4 / 4"', 'Ô có 8 lựa chọn từ Chờ thực hiện đến Đã thanh toán'], ck=[37, 41])
S2.add('Lọc Số hợp đồng một phần', 'P0', ADMIN, [MENU, ADV, 'Nhập "HDQT_26_0003" vào Số hợp đồng, bấm Tìm kiếm.'], 'Số hợp đồng: HDQT_26_0003',
       ['Có dòng TPE.PGV.2026018712', 'Chưa bấm Tìm kiếm thì chưa lọc'], ck=[37])
S2.add('Lọc Số phiếu yêu cầu', 'P0', ADMIN, [MENU, ADV, 'Nhập "YCGVK.2026003064" vào Số phiếu yêu cầu, nhấn Enter.'],
       'Số phiếu yêu cầu: YCGVK.2026003064', ['Hiện TPE.PGV.2026018717'], ck=[37])
S2.add('Lọc Khách hàng', 'P1', ADMIN, [MENU, ADV, 'Gõ "TOYOTA HÀ ĐÔNG" vào Khách hàng, chọn 29TPHPYE-1.'], 'Khách hàng: 29TPHPYE-1',
       ['Gõ dưới 2 ký tự chưa hiện gợi ý', 'Chỉ còn phiếu khách 29TPHPYE-1 (TPE.PGV.2026018717, 018713, 018712, 018705…)'], ck=[37])
S2.add('Lọc Người yêu cầu, Người tạo, Người thực hiện', 'P1', ADMIN,
       [MENU, ADV, 'Chọn Người yêu cầu: Vũ Tuấn Việt.', 'Làm mới, chọn Người tạo: Nguyễn Thị Thu Hiền.', 'Làm mới, chọn Người thực hiện: Khúc Ngọc Nghĩa.'],
       'Người yêu cầu: Vũ Tuấn Việt\nNgười tạo: Nguyễn Thị Thu Hiền\nNgười thực hiện: Khúc Ngọc Nghĩa',
       ['Mỗi lần lọc có TPE.PGV.2026018725 (2 lần đầu) / TPE.PGV.2026018724 (lần cuối)',
        'Lọc Người thực hiện lấy cả phiếu người đó là thành viên'], ck=[37])
S2.add('Lọc Thời gian dự kiến', 'P1', ADMIN, [MENU, ADV, 'Chọn Thời gian dự kiến từ 04/11/2026 đến 07/11/2026.'],
       'Từ 04/11/2026 – Đến 07/11/2026', ['Có TPE.PGV.2026018712 (04/11–07/11), 018713 (04/11–04/11)',
                                           'Không có TPE.PGV.2026018725 (12/11–13/11)'], ck=[37])
S2.add('Lọc kết hợp nhiều tiêu chí và tìm nhanh', 'P0', ADMIN,
       [MENU, ADV, 'Chọn Trạng thái: Chờ thực hiện, Khách hàng 29TPHPYE-1.', 'Nhập "018712" vào ô tìm nhanh, bấm Tìm kiếm.'],
       'Trạng thái: Chờ thực hiện\nKhách hàng: 29TPHPYE-1\nTừ khóa: 018712', ['Còn 1 dòng TPE.PGV.2026018712, "Hiển thị 1–1 / 1"'],
       ck=[38, 39, 41])
S2.add('Phân trang và sắp xếp sau lọc', 'P2', ADMIN, [MENU, ADV, 'Chọn Trạng thái: Đã nhập kết quả.', 'Sắp xếp Ngày tạo tăng dần, bấm trang 2.'],
       '—', ['"Hiển thị 1–10 / 319"', 'Trang 2 vẫn đúng trạng thái và thứ tự'], ck=[42, 43])
S2.add('Làm mới', 'P0', ADMIN, [MENU, ADV, 'Chọn Trạng thái, Công ty và nhập ô tìm nhanh.', 'Bấm Làm mới.'], '—',
       ['Mọi ô và ô tìm nhanh về trống, bỏ sắp xếp', 'Danh sách hiện lại đủ 9.876 phiếu, trang 1'], ck=[44])
S2.add('Giữ bộ lọc khi mở chi tiết rồi quay lại', 'P0', ADMIN,
       [MENU, ADV, 'Chọn Trạng thái: Đang duyệt kết quả.', 'Bấm số phiếu ở dòng 1.', 'Bấm Quay lại.'], '—',
       ['Về danh sách vẫn lọc Đang duyệt kết quả (4 dòng), khối lọc vẫn mở'], ck=[45])
S2.add('Sang màn khác thì mất bộ lọc', 'P1', ADMIN, [MENU, ADV, 'Chọn Trạng thái: Đang duyệt kết quả.', 'Bấm menu "Phiếu nhập kết quả".',
                                                    'Bấm lại "Phiếu giao việc".'], '—',
       ['Danh sách đủ 9.876 phiếu, ô Trạng thái trống (đúng theo code: chỉ giữ khi mở chi tiết)'], ck=[45])
S2.add('Tải lại trang (F5)', 'P2', ADMIN, [MENU, ADV, 'Chọn Trạng thái: Chờ thực hiện.', 'Nhấn F5.'], '—',
       ['Danh sách về đủ 9.876 phiếu, bộ lọc trống (chưa mở chi tiết nên chưa ghi nhớ)'], ck=[46])
S2.add('Mở tab mới', 'P2', ADMIN, [MENU, 'Lọc Trạng thái: Chờ thực hiện.', 'Mở mục menu ở thẻ trình duyệt mới.'], '—',
       ['Thẻ mới hiện đủ 9.876 phiếu, không lọc'], ck=[47])
S2.add('Tài khoản khác cùng trình duyệt', 'P2', ADMIN + '\n' + ACC_A,
       [MENU, 'Lọc, mở chi tiết rồi quay lại.', 'Đăng xuất, đăng nhập tài khoản A trong 10 phút, mở màn.'], '—',
       ['Tài khoản A chỉ thấy phiếu trong phạm vi của A', 'Bộ lọc ghi nhớ của DNS Admin có thể còn áp lên A (ghi nhớ theo trình duyệt, đúng theo code)'],
       ck=[48])
S2.add('Cài đặt bộ lọc: ẩn ô lọc và lưu', 'P1', ADMIN, [MENU, 'Bấm Cài đặt bộ lọc.', 'Bỏ tích "Người yêu cầu", bấm Lưu.'], '—',
       ['Cửa sổ "Cài đặt bộ lọc" liệt kê 9 mục (có Công ty – Phòng ban)', 'Thông báo "Cập nhật thành công"', 'Khối lọc không còn ô Người yêu cầu'],
       ck=[36])
S2.add('Cài đặt bộ lọc: kéo đổi thứ tự, khôi phục mặc định, đóng không lưu', 'P2', ADMIN,
       [MENU, 'Bấm Cài đặt bộ lọc.', 'Kéo "Trạng thái" lên đầu, bấm Lưu.', 'Mở lại, bấm Khôi phục mặc định rồi Đóng.'], '—',
       ['Sau Lưu: Trạng thái đứng đầu khối lọc', 'Khôi phục rồi Đóng: không đổi gì'], ck=[36])
S2.add('Cài đặt bộ lọc riêng với lối vào Phiếu giao việc được giao', 'P2', ADMIN, ['Ẩn ô Người yêu cầu ở màn này.',
                                                                                   'Mở mục "Phiếu giao việc được giao".'],
       '—', ['Màn Phiếu giao việc được giao vẫn có ô Người yêu cầu'], ck=[36])

# ===================================================================== III. THÊM MỚI (Tạo phiếu giao việc)
S3 = Sec(3)
S3.add('Mở màn Tạo từ Phiếu chờ giao việc', 'P0', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC], '—',
       ['Mở trang "Tạo phiếu giao việc" trong cùng thẻ', 'Ô Số hợp đồng = HĐ-X, khách hàng, người liên hệ, người yêu cầu điền sẵn, chỉ đọc'],
       ck=[49, 50])
S3.add('Các khối và nút của màn Tạo', 'P0', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC], '—',
       ['Khối: Thông tin khách hàng, A - DỊCH VỤ SỬA CHỮA BẢO DƯỠNG (I, II), B - Danh sách vật tư bán thêm, C - CÔNG VIỆC PHỤ, D - TỔNG HỢP',
        'Nút: Thêm dòng, Lưu và duyệt, Quay lại', 'KHÔNG có Lưu nháp, Lưu và tiếp tục'], ck=[51, 54])
S3.add('Trường bắt buộc có dấu (*)', 'P1', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC], '—',
       ['Dấu (*) đỏ: Số hợp đồng, Khách hàng, Người liên hệ, Ngày dự kiến bắt đầu, Ngày dự kiến kết thúc, cột Tên vật tư, Công phụ tính '
        'P3, ĐM Công'], ck=[52])
S3.add('Giá trị mặc định', 'P0', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC], '—',
       ['Máy nén khí: SL còn trên hợp đồng 2, SL giao lần này 2', 'Dịch vụ SL giao 2, vật tư SL giao 5', 'Vật tư bán thêm: SL còn 4, SL giao 0',
        'Ngày dự kiến trống; Ghi chú = ghi chú của hợp đồng; Định mức công theo lỗi thiết bị'], ck=[53])
S3.add('Tạo thành công đầy đủ thông tin', 'P0', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Chọn ngày bắt đầu hôm nay, kết thúc hôm nay + 3.',
                                                        'Nhập Ghi chú, thêm 1 dòng công phụ P3.', 'Bấm Lưu và duyệt, bấm Lưu và duyệt trong hộp.'],
       'Ghi chú: Giao đợt 2\nCông phụ P3: Vận chuyển máy, ĐM Công 0.5',
       ['Thông báo "Tạo phiếu giao việc thành công."', 'Về danh sách Phiếu giao việc, phiếu mới ở dòng 1, trạng thái "Chờ thực hiện"',
        'Mã dạng <mã công ty>.PGV.<năm><6 số>'], ck=[55, 58, 59, 302, 305])
S3.add('Tạo thành công chỉ với trường bắt buộc', 'P0', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Chỉ chọn 2 ngày dự kiến, bấm Lưu và duyệt, xác nhận.'],
       'Ngày bắt đầu, kết thúc: hôm nay', ['Lưu thành công, phiếu có đủ dòng với SL mặc định'], ck=[56, 57])
S3.add('Giao một phần số lượng', 'P0', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Sửa SL giao Máy nén khí thành 1, chọn ngày, lưu.',
                                                CHO, 'Bấm lại Tạo phiếu giao việc ở HĐ-X.'], 'SL giao lần này: 1',
       ['Phiếu mới có SL 1', 'Lần mở sau: SL còn trên hợp đồng của Máy nén khí là 1', 'HĐ-X vẫn ở tab Hợp đồng của Phiếu chờ giao việc'],
       ck=[58, 306])
S3.add('Giao hết thì chứng từ rời Phiếu chờ giao việc', 'P0', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Giữ SL mặc định cho mọi dòng, lưu.', CHO],
       '—', ['HĐ-X không còn ở tab Hợp đồng (hết số lượng chưa giao)'], ck=[306, 307])
S3.add('Lịch sử ghi mốc Tạo mới', 'P1', ACC_L, ['Tạo phiếu như trên.', 'Ở danh sách bấm Lịch sử ở phiếu mới.'], '—',
       ['Mốc "Tạo mới" của tài khoản L, kèm số phiếu, khách hàng, ngày dự kiến, tổng công định mức, ghi chú'], ck=[60, 312])
S3.add('Thiếu ngày dự kiến thì bị chặn', 'P0', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Để trống 2 ô ngày, bấm Lưu và duyệt.'], '—',
       ['Viền đỏ + ' + REQ + ' dưới 2 ô ngày', 'Thông báo "Bạn chưa nhập đầy đủ thông tin."', 'Không hiện hộp xác nhận, không lưu'],
       ck=[61, 70, 87, 303])
S3.add('Ngày kết thúc trước ngày bắt đầu', 'P0', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Chọn ngày bắt đầu hôm nay + 3.',
                                                        'Mở lịch Ngày dự kiến kết thúc.'], '—',
       ['Lịch khóa các ngày trước hôm nay và trước ngày bắt đầu', 'Nếu đổi ngày bắt đầu sau ngày kết thúc đã chọn rồi lưu: "Ngày kết thúc phải lớn '
        'hơn hoặc bằng ngày hiện tại và ngày bắt đầu"'], ck=[62, 88])
S3.add('Ngày bắt đầu trước hôm nay', 'P1', ACC_L + '\nForm Tạo mở từ hôm trước, ngày bắt đầu chọn = hôm trước.',
       ['Để qua ngày, bấm Lưu và duyệt.'], '—', ['"Ngày bắt đầu phải lớn hơn hoặc bằng ngày hiện tại" dưới ô ngày bắt đầu'], ck=[62])
S3.add('SL giao vượt SL còn', 'P0', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Gõ 3 vào SL giao lần này của Máy nén khí (SL còn 2).'],
       'SL giao lần này: 3', ['Ngay khi gõ: viền đỏ + "Giá trị nhập vào không được vượt quá 2."', 'Ô KHÔNG tự sửa về 2',
                               'Bấm Lưu và duyệt: thông báo "Vui lòng kiểm tra lại thông tin đã nhập", không lưu'], ck=[62, 70, 304])
S3.add('Ô số chặn chữ, dấu trừ, số lẻ', 'P1', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Gõ "abc", "-1", "1.5" vào SL giao Máy nén khí.'],
       'abc ; -1 ; 1.5', ['Không nhận chữ và dấu trừ', 'Cột SL thiết bị chỉ nhận số nguyên', 'Ô SL vật tư nhận tối đa 2 số lẻ'], ck=[63])
S3.add('Công phụ P3 thiếu tên / ĐM công', 'P0', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Chọn ngày, bấm Thêm dòng, để trống, bấm Lưu và duyệt.'],
       '—', [REQ + ' dưới ô Công phụ tính P3 và ô ĐM Công', 'Mọi ô lỗi đỏ cùng lúc, cuộn tới ô lỗi đầu tiên'], ck=[61, 70])
S3.add('Tên công phụ / ghi chú dòng quá 255 ký tự', 'P1', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Dán 256 ký tự vào Ghi chú dòng Máy nén '
                                                                                                    'khí, bấm Lưu và duyệt.'],
       'Chuỗi 256 ký tự', ['"Vui lòng nhập tối đa 255 ký tự." dưới ô', 'Đúng 255 ký tự thì lưu được'], ck=[65, 66])
S3.add('Khoảng trắng ở tên công phụ', 'P2', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Thêm dòng P3 tên "  Vận chuyển  ", ĐM 0.5, lưu.',
                                                    'Mở chi tiết phiếu.'], 'Công phụ P3: "  Vận chuyển  "',
       ['Tên lưu là "Vận chuyển" (bỏ khoảng trắng 2 đầu)', 'Tên chỉ gồm khoảng trắng thì báo ' + REQ], ck=[68, 69])
S3.add('Lỗi biến mất khi sửa đúng', 'P1', ACC_L, ['Gây lỗi vượt SL như trên.', 'Sửa SL giao về 2.', 'Chọn 2 ngày sau khi đã báo thiếu.'], '—',
       ['Lỗi dưới ô SL mất ngay', 'Lỗi ngày mất khi chọn ngày hợp lệ'], ck=[71])
S3.add('Không dưới độ dài tối thiểu, không có trường trùng', 'P2', ACC_L, ['Tạo 2 phiếu liên tiếp cùng ghi chú từ HĐ-X (giao 2 lần, mỗi lần 1).'],
       '—', ['Cả 2 lần đều lưu được (không có ràng buộc trùng; ô chữ không có độ dài tối thiểu)', 'Mã phiếu khác nhau'], ck=[64, 67, 89])
S3.add('Công thức tổng công định mức', 'P0', ACC_L + '\nMáy nén khí ĐM công 0.3; thêm P3 ĐM 0.5.',
       ['Đăng nhập tài khoản L.', CHO, SRC, 'Thêm dòng P3 ĐM 0.5.', 'Sửa SL giao Máy nén khí về 0.'], '—',
       ['Ban đầu: Tổng công định mức (I) 0.3; D - TỔNG HỢP: Công chính 0.30, Công phụ 0.50, Tổng 0.80',
        'SL Máy nén khí = 0: Công chính 0.00, Tổng 0.50 (dòng có SL 0 không tính công)'], ck=[58])
S3.add('Phiếu lắp đặt: SL tính công khoán', 'P0', 'Tài khoản L thuộc phòng tiếp nhận của YC lắp đặt YC-LĐ1: hàng Cầu nâng SL còn 3, SL người '
                                                 'tính công 2, ĐM công 1.3.', ['Đăng nhập tài khoản L.', CHO, 'Tab Lắp đặt bàn giao, Tạo phiếu '
                                                                                                             'giao việc ở YC-LĐ1.'],
       '—', ['SL bàn giao 3, SL tính công khoán 2 (làm tròn lên 3/2), Tổng công định mức dòng 2.6'], ck=[53, 58])
S3.add('Phiếu giao việc khác: nhập Định mức công dịch vụ', 'P1', 'YC giao việc khác YC-K1 (Chờ giao việc, phòng tiếp nhận của L) có 2 dịch vụ.',
       ['Đăng nhập tài khoản L.', CHO, 'Tab Giao việc khác, Tạo phiếu giao việc ở YC-K1.', 'Nhập ĐM công 2 và 3, lưu.'], 'ĐM công: 2 ; 3',
       ['Khối "A - Dịch vụ đính kèm", "B - CÔNG VIỆC PHỤ", "C - TỔNG HỢP"', 'Tổng công định mức 5.00', 'YC-K1 chuyển "Đã giao việc"'],
       ck=[58, 307])
S3.add('Phiếu bảo hành: thông tin và hết sản phẩm', 'P1', 'Phiếu bảo hành TPE.PBH.2026.008226 (Đã duyệt) có 1 thiết bị chưa giao; L có quyền Tạo '
                                                         'phiếu giao việc.',
       ['Đăng nhập tài khoản L.', CHO, 'Tab Phiếu bảo hành, Tạo phiếu giao việc ở TPE.PBH.2026.008226.', 'Lưu đủ, rồi mở lại từ tab đó.'], '—',
       ['Có khối A - BẢO HÀNH với Máy nén thử kín điều hòa 1/2 HP', 'Sau khi lưu: phiếu bảo hành rời tab Phiếu bảo hành'], ck=[58, 307])
S3.add('Hộp xác nhận Lưu và duyệt', 'P0', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Chọn ngày, bấm Lưu và duyệt.'], '—',
       ['Hộp "Xác nhận lưu & duyệt": "Lưu và duyệt phiếu giao việc cho số hợp đồng \'HĐ-X\'? Phiếu sẽ chuyển sang trạng thái Chờ thực hiện."',
        'Nút Lưu và duyệt, Hủy'], ck=[300, 301])
S3.add('Bấm Hủy trong hộp xác nhận', 'P1', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Chọn ngày, bấm Lưu và duyệt, bấm Hủy.'], '—',
       ['Hộp đóng, vẫn ở màn Tạo, dữ liệu giữ nguyên, không có phiếu mới'], ck=[310])
S3.add('Quay lại khi chưa nhập gì', 'P1', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Bấm Quay lại ngay.'], '—',
       ['Về Phiếu chờ giao việc, đúng tab Hợp đồng, không hỏi'], ck=[93, 95])
S3.add('Quay lại khi đã nhập: Thoát / Ở lại', 'P0', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Nhập Ghi chú, bấm Quay lại.', 'Bấm Ở lại.',
                                                           'Bấm Quay lại, bấm Thoát.'], 'Ghi chú: thử',
       ['Hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"', 'Ở lại: vẫn ở màn Tạo, giữ dữ liệu',
        'Thoát: về Phiếu chờ giao việc, không lưu'], ck=[94, 96, 97])
S3.add('Nhập rồi xóa hết / đổi rồi trả lại ban đầu', 'P2', ACC_L, ['Đăng nhập tài khoản L.', CHO, SRC, 'Gõ ghi chú rồi xóa hết, đổi SL rồi trả về như cũ.',
                                                                  'Bấm Quay lại.'], '—',
       ['Không hỏi "Thông tin chưa lưu", về Phiếu chờ giao việc'], ck=[98, 99])
S3.add('Để lâu không thao tác rồi lưu', 'P2', ACC_L + '\nTrong lúc L mở form 30 phút, người khác đã giao hết HĐ-X.',
       ['L chọn ngày, bấm Lưu và duyệt, xác nhận.'], '—',
       ['Báo vượt SL tại đúng ô ("Giá trị nhập vào không được vượt quá 0.") hoặc ' + CONFLICT, 'Không tạo phiếu'], ck=[100, 102])
S3.add('Bấm Lưu và duyệt liên tục', 'P1', ACC_L, ['Mở form, chọn ngày.', 'Bấm Lưu và duyệt trong hộp xác nhận nhiều lần liên tiếp.'], '—',
       ['Nút bị khóa trong lúc lưu', 'Chỉ tạo 1 phiếu'], ck=[101, 311])
S3.add('Hai tài khoản giao cùng chứng từ đồng thời', 'P1', ACC_L + '\nTài khoản L2 cùng phòng, cùng quyền.',
       ['L và L2 cùng mở form từ HĐ-X, giữ SL mặc định.', 'L lưu trước, L2 lưu sau.'], '—',
       ['L lưu thành công', 'L2 bị báo vượt SL còn tại các ô, không tạo phiếu'], ck=[102])
S3.add('Phụ lục giảm chờ duyệt thì không tạo được', 'P1', 'HĐ-Y có phụ lục giảm đang chờ duyệt; L đủ quyền, đúng phòng.',
       ['Đăng nhập tài khoản L.', CHO, 'Bấm Tạo phiếu giao việc ở HĐ-Y.'], '—',
       ['Thông báo "Hợp đồng đang có PL giảm chờ duyệt!"', 'Không mở được form, quay về Phiếu chờ giao việc'], ck=[304])
S3.add('Trưởng phòng có nhân viên còn hàng quá hạn', 'P1', 'Tài khoản TP là trưởng phòng, quản lý phòng có nhân viên còn hàng giữ quá hạn; TP '
                                                         'mở form tạo hợp lệ.', ['TP chọn ngày, bấm Lưu và duyệt, xác nhận.'], '—',
       ['Thông báo "Phòng ban bạn quản lý có nhân viên hàng giữ quá hạn. Không thể thực hiện thao tác này."', 'Không tạo phiếu'], ck=[304])
S3.add('Tạo từ Phiếu yêu cầu lắp đặt mở thẻ mới', 'P2', 'YC-LĐ1 Chờ giao việc, L thuộc phòng tiếp nhận.',
       ['Mở chi tiết YC-LĐ1 ở màn YC lắp đặt, bàn giao.', 'Bấm Tạo phiếu giao việc.'], '—',
       ['Màn Tạo phiếu giao việc mở ở thẻ trình duyệt mới, chứng từ YC-LĐ1 chọn sẵn'], ck=[49])

# ===================================================================== IV. XÓA
S4 = Sec(4)
S4.add('Điều kiện hiện nút Xóa', 'P0', ADMIN + '\n' + P709, [MENU, 'Tìm TPE.PGV.2026018709 và TPE.PGV.2026018712.'], '—',
       ['018709 (DNS Admin tạo, Chờ thực hiện, chưa gắn phiếu giao công tác) có nút Xóa (thùng rác đỏ)',
        '018712 (đã có phiếu giao công tác đã duyệt) KHÔNG có nút Xóa'], ck=[130])
S4.add('Hộp xác nhận xóa', 'P0', ADMIN + '\n' + P709, [MENU, 'Bấm Xóa ở dòng TPE.PGV.2026018709.'], '—',
       ['Hộp "Xác nhận xóa", nội dung "Bạn có chắc muốn xóa bản ghi này không?"', 'Nút Xóa (đỏ) và Hủy'], ck=[131, 132])
S4.add('Xóa thành công', 'P0', ACC_L + '\nL vừa tạo phiếu PGV-L1 từ HĐ-X (Chờ thực hiện).', ['Đăng nhập tài khoản L.', MENU, 'Bấm Xóa ở PGV-L1, bấm Xóa.'],
       '—', ['Thông báo "Xóa thành công."', 'PGV-L1 biến mất khỏi danh sách, tổng giảm 1', 'Phiếu chuyển Hủy (không xóa cứng)'],
       ck=[133, 139, 140])
S4.add('Xóa trả số lượng về chứng từ nguồn', 'P0', ACC_L + '\nPGV-L1 giao 1 Máy nén khí.', ['Xóa PGV-L1.', CHO, 'Bấm Tạo phiếu giao việc ở HĐ-X.'],
       '—', ['SL còn trên hợp đồng của Máy nén khí tăng lại 1', 'HĐ-X có lại ở tab Hợp đồng nếu trước đó đã giao hết'], ck=[141, 136])
S4.add('Xóa phiếu giao việc khác / lắp đặt trả trạng thái yêu cầu', 'P1', 'PGV-L2 lập từ YC-K1 (YC-K1 "Đã giao việc"); PGV-L3 lập từ YC-LĐ1 giao hết.',
       ['L xóa PGV-L2 và PGV-L3.', 'Mở YC-K1, YC-LĐ1.'], '—', ['YC-K1 về "Chờ giao việc"', 'YC-LĐ1 về "Chờ giao việc"'], ck=[141])
S4.add('Bấm Hủy thì không xóa', 'P0', ADMIN + '\n' + P709, [MENU, 'Bấm Xóa ở TPE.PGV.2026018709, bấm Hủy.'], '—',
       ['Hộp đóng, phiếu vẫn Chờ thực hiện'], ck=[134])
S4.add('Phiếu đã gắn phiếu giao công tác / đổi trạng thái thì không xóa được', 'P0',
       ACC_L + '\nPGV-L1 đang hiện nút Xóa; người khác vừa chọn PGV-L1 vào phiếu giao công tác.',
       ['L bấm Xóa ở PGV-L1 (màn chưa tải lại), bấm Xóa.'], '—', ['Thông báo ' + CONFLICT, 'Danh sách nạp lại, PGV-L1 không còn nút Xóa'],
       ck=[135, 138])
S4.add('Phiếu đã có kết quả không có nút Xóa', 'P1', ADMIN, [MENU], '—',
       ['TPE.PGV.2026018725, 018724, 018718 không có nút Xóa'], ck=[136, 137])
S4.add('Xóa từ màn chi tiết', 'P1', ACC_L + '\nPGV-L1 Chờ thực hiện.', ['Mở chi tiết PGV-L1.', 'Bấm Xóa ở cuối trang, bấm Xóa.'],
       '—', ['Hộp hỏi "Bạn có chắc muốn xóa phiếu giao việc \'<mã PGV-L1>\'?"', '"Xóa thành công.", về danh sách Phiếu giao việc'], ck=[133])
S4.add('Xóa dòng cuối của trang', 'P2', 'Tài khoản A (không quyền Xem) có 11 phiếu trong danh sách, phiếu thứ 11 do A tạo, đủ điều kiện xóa.',
       ['Đăng nhập tài khoản A.', MENU, 'Bấm trang 2, xóa dòng duy nhất.'], '—', ['Sau khi xóa tự lùi về trang 1, "Hiển thị 1–10 / 10"'],
       ck=[140])

# ===================================================================== V. LỊCH SỬ
S5 = Sec(5)
S5.add('Mở cửa sổ lịch sử từ danh sách', 'P0', ADMIN + '\n' + P725, [MENU, 'Bấm Lịch sử ở dòng TPE.PGV.2026018725.'], '—',
       ['Cửa sổ "Lịch sử thay đổi: TPE.PGV.2026018725"', 'Mốc 13/11/2026 10:59 "Thay đổi trạng thái", "Người thực hiện: DNS Admin — HỘI '
        'ĐỒNG QUẢN TRỊ"', '"Trạng thái: Chờ thực hiện sang Đang nhập kết quả", kèm "Phiếu nhập kết quả TPE.PNKQ.2026009123"'],
       ck=[162, 163, 165, 166, 167, 168])
S5.add('Mốc Tạo mới và thứ tự mới nhất ở trên', 'P0', 'Phiếu PGV-L1 do L tạo ở HRM, sau đó lưu nháp phiếu nhập kết quả.',
       ['Mở Lịch sử PGV-L1.'], '—', ['Mốc "Thay đổi trạng thái" ở trên, mốc "Tạo mới" ở dưới cùng', 'Mốc Tạo mới có các trường ban đầu'],
       ck=[164, 176])
S5.add('Lọc theo loại hành động, người thực hiện, thời gian', 'P1', 'Phiếu PGV-L1 như trên.',
       ['Mở Lịch sử PGV-L1.', 'Bấm Bộ lọc.', 'Chọn Loại hành động: Thay đổi trạng thái.', 'Chọn Người thực hiện, Từ ngày – Đến ngày.'], '—',
       ['Chọn là lọc ngay', 'Chỉ còn mốc khớp điều kiện'], ck=[169, 170, 171, 172, 175])
S5.add('Lọc không có kết quả và Làm mới', 'P2', 'Phiếu PGV-L1 như trên.', ['Mở Lịch sử PGV-L1, Bộ lọc.', 'Chọn Từ ngày 01/01/2020 Đến ngày 02/01/2020.',
                                                                         'Bấm Làm mới.'], '—',
       ['"Không có lịch sử phù hợp bộ lọc."', 'Làm mới: hiện lại đủ mốc'], ck=[173, 174])
S5.add('Phiếu lập trước khi chuyển hệ thống chưa có lịch sử', 'P2', ADMIN, [MENU, 'Bấm Lịch sử ở một phiếu cũ năm 2025.'], '—',
       ['"Chưa có lịch sử thao tác nào."'], ck=[164])
S5.add('Xóa phiếu ghi mốc', 'P1', ACC_L, ['Tạo PGV-L4, mở Lịch sử ghi nhận mốc Tạo mới.', 'Xóa PGV-L4.'], '—',
       ['Phiếu Hủy không còn mở được; mốc "Thay đổi trạng thái: Chờ thực hiện sang Hủy" được ghi (kiểm qua bộ phận quản trị)'], ck=[183])
S5.add('Xem, in, xuất không ghi mốc', 'P2', ADMIN, [MENU, 'Mở chi tiết, In danh sách, Xuất Excel.', 'Mở Lịch sử TPE.PGV.2026018725.'], '—',
       ['Không thêm mốc mới'], ck=[182])
S5.add('Đóng cửa sổ lịch sử', 'P1', ADMIN, [MENU, 'Bấm trang 2, lọc Trạng thái.', 'Mở Lịch sử, bấm Đóng (hoặc ×).'], '—',
       ['Cửa sổ đóng, danh sách giữ trang và bộ lọc'], ck=[184, 185])

# ===================================================================== VI. XEM CHI TIẾT
S6 = Sec(6)
S6.add('Mở chi tiết từ Số phiếu', 'P0', ADMIN + '\n' + P712, [MENU, 'Bấm số phiếu TPE.PGV.2026018712.'], '—',
       ['Trang "Chi tiết phiếu giao việc: TPE.PGV.2026018712" mở trong cùng thẻ, nhãn "Chờ thực hiện"'], ck=[186, 187])
S6.add('Đủ thông tin và khớp danh sách', 'P0', ADMIN + '\n' + P712, ['Mở chi tiết TPE.PGV.2026018712.'], '—',
       ['Khối Thông tin khách hàng: Số hợp đồng, Khách hàng 29TPHPYE-1, Người liên hệ, SĐT, Địa chỉ lắp đặt, Người yêu cầu, Ngày dự kiến '
        '04/11/2026 – 07/11/2026', 'Khối A, C - CÔNG VIỆC PHỤ, D - TỔNG HỢP; Tổng công định mức được giao 2.00 = cột danh sách'],
       ck=[188, 189, 190])
S6.add('Mọi trường chỉ đọc, không có nút Lưu / Sửa', 'P0', ADMIN, ['Mở chi tiết TPE.PGV.2026018712.'], '—',
       ['Mọi ô bị khóa, Ghi chú không sửa được', 'Không có Lưu, Sửa, Thêm dòng; không có cột SL còn', 'Dấu (*) vẫn hiện ở các ô bắt buộc'],
       ck=[191, 192])
S6.add('Nút chân trang theo trạng thái', 'P0', ADMIN + '\n' + P712 + '\n' + P725 + '\n' + P709,
       ['Mở chi tiết 3 phiếu.'], '—',
       ['018712: Nhập kết quả, Quay lại', '018725: Xem phiếu nhập kết quả, Quay lại', '018709: Xóa, Quay lại'], ck=[193])
S6.add('Chi tiết theo loại nguồn', 'P1', ADMIN, ['Mở chi tiết TPE.PGV.2026018724, 018704, 018717.'], '—',
       ['018724: Số phiếu bảo hành, khối A - BẢO HÀNH', '018704: Phiếu yêu cầu lắp đặt + Hợp đồng, khối A - Lắp đặt bàn giao',
        '018717: Phiếu YC giao việc khác, khối A - Dịch vụ đính kèm, B - CÔNG VIỆC PHỤ, C - TỔNG HỢP'], ck=[188])
S6.add('Khối Lịch sử ở chi tiết', 'P2', ADMIN, ['Mở chi tiết TPE.PGV.2026018725.', 'Bấm Xem lịch sử.'], '—',
       ['Khối mở ra cùng nội dung như cửa sổ ở danh sách', 'Có nút Làm mới, Bộ lọc, Thu gọn'], ck=[195])
S6.add('Quay lại giữ trang và bộ lọc', 'P0', ADMIN, [MENU, 'Lọc Trạng thái: Đang duyệt kết quả, bấm số phiếu ở dòng 1.', 'Bấm Quay lại.'], '—',
       ['Về "Phiếu giao việc", vẫn lọc Đang duyệt kết quả'], ck=[196, 197])
S6.add('Phiếu không có quyền xem / đã Hủy', 'P1', ACC_N, ['Đăng nhập tài khoản N.', 'Mở chi tiết TPE.PGV.2026018712 từ đường dẫn được gửi.',
                                                         'Mở chi tiết phiếu đã Hủy.'], '—',
       ['Cả 2 trường hợp chuyển trang không tìm thấy, không hiện dữ liệu'], ck=[186])

# ===================================================================== VII. IN
S7 = Sec(7)
S7.add('Mở xem trước in danh sách', 'P0', ADMIN, [MENU, 'Nhập "01871" vào ô tìm nhanh, bấm Tìm kiếm.', 'Bấm In danh sách.'], '—',
       ['Cửa sổ "Xem trước danh sách phiếu giao việc", khổ ngang', 'Letterhead công ty người in, tiêu đề "DANH SÁCH PHIẾU GIAO VIỆC"',
        'Các dòng khớp danh sách, 12 cột (STT … Ngày tạo), Người lập DNS Admin'], ck=[])
S7.add('Vượt 2.000 dòng thì không in', 'P0', ADMIN, [MENU, 'Không lọc, bấm In danh sách.'], '—',
       ['Câu "Danh sách có 9,876 dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc…"', 'Không có nút In'], ck=[])
S7.add('Bấm In và đóng', 'P1', ADMIN, [MENU, 'Lọc Trạng thái: Đang duyệt kết quả, bấm In danh sách.', 'Bấm In.', 'Đóng hộp in, bấm ×.'], '—',
       ['Bản in 4 dòng', 'Mở hộp thoại in của trình duyệt', 'Bấm × đóng cửa sổ, danh sách giữ nguyên'], ck=[])
S7.add('In danh sách rỗng', 'P2', ACC_N, ['Đăng nhập tài khoản N.', MENU, 'Bấm In danh sách.'], '—', ['Bản in chỉ có dòng tiêu đề cột'], ck=[])
S7.add('Tổng công định mức trên bản in', 'P2', ADMIN, [MENU, 'Lọc "0187", bấm In danh sách.'], '—',
       ['Cột ghi 2 số lẻ: 134.00, 2.00; phiếu tổng 0 in "0.00"'], ck=[])

# ===================================================================== VIII. TÙY CHỈNH CỘT
S8 = Sec(8)
S8.add('Mở cửa sổ và danh sách cột', 'P1', ADMIN, [MENU, 'Bấm Cấu hình cột hiển thị.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột", 13 cột tích sẵn, "Đang chọn 13/13 cột"'], ck=[198, 199, 200])
S8.add('Ẩn và hiện cột', 'P0', ADMIN, [MENU, 'Mở Tuỳ chỉnh cột, bỏ tích "Người yêu cầu", Lưu.', 'Mở lại, tích lại, Lưu.'], '—',
       ['"Cập nhật thành công", cột Người yêu cầu ẩn', 'Lần 2 cột hiện lại'], ck=[201, 202, 206])
S8.add('Cột khóa không ẩn được', 'P1', ADMIN, [MENU, 'Mở Tuỳ chỉnh cột, bấm Bỏ chọn hết.'], '—',
       ['STT, Số phiếu giao việc, Hành động vẫn tích, có ổ khóa, không kéo được'], ck=[203, 205])
S8.add('Kéo đổi thứ tự cột', 'P2', ADMIN, [MENU, 'Kéo "Trạng thái" lên sau Số phiếu giao việc, Lưu.'], '—', ['Bảng hiện cột Trạng thái ở vị trí mới'],
       ck=[204])
S8.add('Đóng không lưu', 'P2', ADMIN, [MENU, 'Bỏ tích "Khách hàng", bấm Đóng.'], '—', ['Bảng vẫn có cột Khách hàng'], ck=[207])
S8.add('Ghi nhớ sau tải lại, theo tài khoản, riêng lối vào', 'P1', ADMIN + '\n' + ACC_A,
       ['Ẩn cột Người yêu cầu, Lưu.', 'Nhấn F5.', 'Mở mục "Phiếu giao việc được giao".', 'Đăng nhập tài khoản A, mở màn.'], '—',
       ['Sau F5 vẫn ẩn', 'Màn Phiếu giao việc được giao vẫn có cột Người yêu cầu', 'Tài khoản A thấy đủ 13 cột'], ck=[208, 209])
S8.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', ADMIN, [MENU, 'Lọc Trạng thái: Đang duyệt kết quả.', 'Ẩn cột Trạng thái, Lưu.'], '—',
       ['Vẫn 4 dòng, bộ lọc giữ nguyên'], ck=[210, 211])

# ===================================================================== IX. XUẤT EXCEL
S9 = Sec(9)
S9.add('Mở cửa sổ chọn trường', 'P1', ADMIN, [MENU, 'Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất file", 11 trường tích sẵn theo cột đang hiện, "Đang chọn 11/11 trường"'], ck=[212, 213, 214])
S9.add('Xuất mặc định theo bộ lọc', 'P0', ADMIN, [MENU, 'Lọc Trạng thái: Đang duyệt kết quả.', 'Bấm Xuất Excel, bấm Xuất file.'], '—',
       ['Tải file danh_sach_phieu_giao_viec.xlsx, thông báo "Xuất Excel thành công."',
        'Tiêu đề "DANH SÁCH PHIẾU GIAO VIỆC", cột STT + 11 cột, 4 dòng khớp màn'], ck=[215, 216, 220, 223, 224, 225, 227, 228])
S9.add('Xuất một số trường và đổi thứ tự', 'P1', ADMIN, [MENU, 'Bấm Xuất Excel, Bỏ chọn hết, tích Trạng thái rồi Số phiếu giao việc, kéo '
                                                              'Số phiếu lên trước.', 'Xuất file.'], '—',
       ['File có STT, Số phiếu giao việc, Trạng thái đúng thứ tự'], ck=[217, 226])
S9.add('Không chọn trường', 'P2', ADMIN, [MENU, 'Bấm Xuất Excel, Bỏ chọn hết.'], '—', ['Nút Xuất file bị khóa'], ck=[218])
S9.add('Xuất theo tìm kiếm', 'P0', ADMIN, [MENU, 'Tìm "TPE.PGV.2026018712".', 'Xuất file.'], '—', ['File 1 dòng TPE.PGV.2026018712'], ck=[219])
S9.add('Xuất toàn bộ khi nhiều trang', 'P0', ADMIN, [MENU, 'Lọc Trạng thái: Đã nhập kết quả (319 phiếu, 32 trang).', 'Xuất file.'],
       '—', ['File đủ 319 dòng (không chỉ trang đang xem)', 'Có dòng tiến độ "Đã tải …", "Đang dựng file …"'], ck=[221, 227])
S9.add('Danh sách rỗng', 'P1', ACC_N, ['Đăng nhập tài khoản N.', MENU, 'Xuất file.'], '—',
       ['Thông báo "Không có dữ liệu để xuất", không tải file (lệch checklist: không ra file rỗng — đúng theo code)'], ck=[222])
S9.add('Định dạng dữ liệu trong file', 'P1', ADMIN, [MENU, 'Tìm "01871", xuất file.'], '—',
       ['Ngày tạo dạng dd/mm/yyyy hh:mm', 'Tổng công định mức là ô số (134 cộng được)', 'Tên khách hàng tiếng Việt đúng dấu'],
       ck=[229, 230])

# ===================================================================== X. RÀNG BUỘC
S10 = Sec(10)
S10.add('Phiếu chờ giao việc: chỉ chứng từ còn số lượng', 'P0', ACC_L, [CHO, 'Kiểm tra HĐ-X trước và sau khi giao hết.'], '—',
        ['Trước: HĐ-X có ở tab Hợp đồng', 'Sau khi giao hết: HĐ-X biến mất; xóa phiếu thì xuất hiện lại'], ck=[268, 270, 274, 280])
S10.add('Phiếu giao công tác chọn được phiếu mới', 'P0', ACC_L + '\nPGV-L1 vừa tạo (Chờ thực hiện).',
        ['Mở Phiếu giao công tác, thêm phiếu giao việc.'], '—', ['PGV-L1 có trong danh sách chọn', 'Phiếu Hủy không có trong danh sách chọn'],
        ck=[269, 274, 284])
S10.add('Duyệt phiếu giao công tác thì có người thực hiện', 'P0', 'PGV-L1 được chọn vào phiếu giao công tác (nhân sự A trưởng nhóm, B), người '
                                                                  'duyệt duyệt phiếu giao công tác.', [MENU, 'Tìm PGV-L1.'], '—',
        ['Cột Người thực hiện hiện A', 'Không còn nút Xóa', 'A có nút Nhập kết quả ở PGV-L1'], ck=[270, 281, 283])
S10.add('Nhập kết quả: điều kiện hiện nút', 'P0', ADMIN + '\n' + P712, [MENU], '—',
        ['TPE.PGV.2026018712 có nút Nhập kết quả', 'TPE.PGV.2026018717 (Chờ thực hiện, chưa có phiếu giao công tác) không có'], ck=[268])
S10.add('Nhập kết quả: mở màn Tạo phiếu nhập kết quả', 'P0', ADMIN + '\n' + P712, [MENU, 'Bấm Nhập kết quả ở TPE.PGV.2026018712.'], '—',
        ['Mở "Tạo phiếu nhập kết quả", phiếu giao việc chọn sẵn', 'Có nút Lưu, Lưu và gửi duyệt, Quay lại'], ck=[269])
S10.add('Nhập kết quả: lưu nháp, gửi duyệt đổi trạng thái phiếu', 'P0', 'A là người thực hiện của PGV-L1 (phiếu giao công tác đã duyệt).',
        ['A bấm Nhập kết quả ở PGV-L1, nhập đủ, bấm Lưu.', 'Mở lại phiếu nhập kết quả, bấm Lưu và gửi duyệt.', 'Mở màn.'], '—',
        ['Sau Lưu: PGV-L1 "Đang nhập kết quả", nút Nhập kết quả thay bằng Xem phiếu nhập kết quả', 'Sau gửi duyệt: "Đã nhập kết quả"',
         'Lịch sử PGV-L1 có mốc "Thay đổi trạng thái" kèm mã phiếu nhập kết quả'], ck=[281, 274])
S10.add('Xóa phiếu nhập kết quả thì phiếu về Chờ thực hiện', 'P1', 'PGV-L1 Đang nhập kết quả.', ['Xóa phiếu nhập kết quả nháp.', 'Mở màn.'],
        '—', ['PGV-L1 về "Chờ thực hiện", có lại nút Nhập kết quả'], ck=[280, 285])
S10.add('Xem phiếu nhập kết quả', 'P0', ADMIN + '\n' + P725, [MENU, 'Bấm Xem phiếu nhập kết quả ở TPE.PGV.2026018725.'], '—',
        ['Mở "Chi tiết phiếu nhập kết quả: TPE.PNKQ.2026009123"', 'Bấm Quay lại về màn trước'], ck=[274])
S10.add('Báo cáo theo dõi lắp đặt mở chi tiết phiếu', 'P2', ADMIN, ['Mở Báo cáo theo dõi lắp đặt - bàn giao - sửa chữa - bảo dưỡng.',
                                                                    'Bấm mã một phiếu giao việc.'], '—', ['Mở chi tiết đúng phiếu'], ck=[274, 282])
S10.add('Không trùng dòng khi nhiều người thực hiện', 'P2', ADMIN, [MENU, 'Tìm TPE.PGV.2026018724.'], '—',
        ['Chỉ 1 dòng dù phiếu có 2 người thực hiện'], ck=[286])
S10.add('Mã phiếu và khách hàng không đổi theo chứng từ sau khi lưu', 'P2', 'PGV-L1 lập từ HĐ-X; sau đó đổi người liên hệ trên HĐ-X.',
        ['Mở chi tiết PGV-L1.'], '—', ['Người liên hệ trên phiếu giữ giá trị lúc lập', 'Mã phiếu không đổi'], ck=[272, 278, 279])

# ===================================================================== XI. PHÂN QUYỀN
S11 = Sec(11)
S11.add('Quyền Xem mức Tổng công ty', 'P0', ADMIN, [MENU], '—',
        ['Thấy 9.876 phiếu của mọi công ty', 'Có ô lọc Công ty và Phòng ban'], ck=[287, 299])
S11.add('Quyền Xem mức Công ty', 'P0', ACC_C, ['Đăng nhập tài khoản C.', MENU], '—',
        ['Thấy 9.096 phiếu công ty 1 + phiếu C tạo ở công ty khác (nếu có)', 'Không thấy phiếu công ty khác', 'Chỉ có ô Phòng ban (phòng công ty 1)'],
        ck=[287, 299])
S11.add('Quyền Xem mức Phòng ban', 'P0', ACC_P, ['Đăng nhập tài khoản P.', MENU], '—',
        ['Thấy 3.026 phiếu phòng 51 + 2 phiếu P tạo', 'Không thấy phiếu phòng khác', 'Ô Phòng ban chỉ có phòng P quản lý'], ck=[287, 299])
S11.add('Có 2 mức thì áp mức rộng hơn', 'P1', 'Tài khoản M có quyền Xem mức Công ty và mức Phòng ban.', ['Đăng nhập tài khoản M.', MENU], '—',
        ['Thấy đủ phiếu của công ty (như mức Công ty)'], ck=[299])
S11.add('Không quyền Xem nhưng là người thực hiện', 'P0', ACC_A, ['Đăng nhập tài khoản A.', MENU], '—',
        ['Thấy 5 phiếu: PGV1, PGV2 (A tạo), PGV3–PGV5 (A thực hiện)', 'Không có ô Công ty – Phòng ban'], ck=[287, 299])
S11.add('Không có quyền nào', 'P0', ACC_N, ['Đăng nhập tài khoản N.', MENU], '—',
        ['Mở được màn nhưng rỗng ' + EMPTY, 'Mở thẳng chi tiết phiếu người khác sang trang không tìm thấy'], ck=[287, 296])
S11.add('Xem chi tiết theo mức quyền', 'P0', ACC_C, ['Đăng nhập tài khoản C.', 'Mở chi tiết phiếu công ty 1 và phiếu công ty khác (đường dẫn được gửi).'],
        '—', ['Phiếu công ty 1 xem được', 'Phiếu công ty khác sang trang không tìm thấy'], ck=[288, 296])
S11.add('Super admin không đặc cách', 'P0', 'Tài khoản S thuộc vai trò Super admin, không có quyền Xem phiếu giao việc, không tạo / thực hiện phiếu nào.',
        ['Đăng nhập tài khoản S.', MENU], '—', ['Danh sách rỗng'], ck=[299])
S11.add('Tạo phiếu: thiếu quyền Tạo phiếu giao việc', 'P0', 'Tài khoản L3 thuộc phòng tiếp nhận của HĐ-X nhưng không có quyền "Tạo phiếu giao việc".',
        ['Đăng nhập tài khoản L3.', CHO], '—', ['Tab Hợp đồng: dòng HĐ-X không có nút Tạo phiếu giao việc',
                                                'Tab Phiếu bảo hành: bấm Tạo phiếu giao việc báo "Không có quyền!", quay về Phiếu chờ giao việc'],
        ck=[289, 295])
S11.add('Tạo phiếu: khác phòng tiếp nhận', 'P0', 'Tài khoản L4 có quyền "Tạo phiếu giao việc" nhưng không thuộc phòng tiếp nhận của HĐ-X, YC-K1.',
        ['Đăng nhập tài khoản L4.', CHO], '—', ['HĐ-X, YC-K1 không có nút Tạo phiếu giao việc', 'Mở màn Tạo từ đường dẫn được gửi: báo '
                                                                                                    '"Không có quyền!"'], ck=[289, 296])
S11.add('Tạo phiếu từ yêu cầu giao việc khác không cần quyền Tạo', 'P1', 'Tài khoản L3 (không có quyền Tạo) thuộc phòng tiếp nhận của YC-K1.',
        ['Đăng nhập tài khoản L3.', CHO, 'Tab Giao việc khác, Tạo phiếu giao việc ở YC-K1, lưu.'], '—', ['Lưu thành công'], ck=[289])
S11.add('Ẩn nút khi không đủ điều kiện', 'P0', ADMIN, [MENU], '—',
        ['Xóa chỉ ở phiếu DNS Admin tạo, Chờ thực hiện, chưa gắn phiếu giao công tác', 'Nhập kết quả chỉ ở phiếu DNS Admin là người thực hiện',
         'Không có nút Tạo mới, Sửa trên danh sách'], ck=[290, 291, 295])
S11.add('Quản lý không phải người tạo thì không xóa', 'P0', ACC_C + '\nPGV-L1 do L (công ty 1) tạo, Chờ thực hiện, chưa gắn phiếu giao công tác.',
        ['Đăng nhập tài khoản C.', MENU, 'Tìm PGV-L1.'], '—', ['Dòng PGV-L1 không có nút Xóa'], ck=[291])
S11.add('Quản lý không là người thực hiện thì không Nhập kết quả', 'P1', ACC_C + '\nPGV-L1 đủ điều kiện nhập kết quả với A.',
        ['Đăng nhập tài khoản C.', MENU, 'Tìm PGV-L1.'], '—', ['Không có nút Nhập kết quả'], ck=[291])
S11.add('Bị gỡ quyền giữa lúc thao tác', 'P1', ACC_C + '\nC đang mở màn; quản trị gỡ quyền Xem của C.', ['C bấm Làm mới.', 'C mở chi tiết phiếu công ty 1.'],
        '—', ['Sau Làm mới chỉ còn phiếu C tạo / thực hiện', 'Chi tiết phiếu của người khác sang trang không tìm thấy'], ck=[297, 298])
S11.add('Lịch sử, in, xuất theo phạm vi', 'P2', ACC_P, ['Đăng nhập tài khoản P.', MENU, 'Mở Lịch sử 1 phiếu, In danh sách (lọc), Xuất Excel.'],
        '—', ['Lịch sử mở được', 'Bản in và file chỉ có phiếu trong phạm vi của P'], ck=[293, 294])
S11.add('Đổi công ty đang làm việc', 'P1', ACC_C + '\nC làm việc ở công ty 1 và công ty 4, quyền Xem mức Công ty chỉ cấp ở công ty 1.',
        ['Đăng nhập tài khoản C.', 'Đổi công ty đang làm việc sang công ty 4.', MENU], '—',
        ['Quyền tính lại theo công ty 4: chỉ còn phiếu C tạo / thực hiện', 'Không thấy phiếu công ty 1'], ck=[299])

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI – TẠO PHIẾU GIAO VIỆC (LƯU VÀ DUYỆT)', S3),
    ('IV', 'XÓA', S4),
    ('V', 'LỊCH SỬ THAY ĐỔI', S5),
    ('VI', 'XEM CHI TIẾT PHIẾU GIAO VIỆC', S6),
    ('VII', 'IN PHIẾU – IN DANH SÁCH PHIẾU GIAO VIỆC', S7),
    ('VIII', 'TÙY CHỈNH CỘT', S8),
    ('IX', 'XUẤT DANH SÁCH EXCEL', S9),
    ('X', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC – PHIẾU CHỜ GIAO VIỆC, PHIẾU GIAO CÔNG TÁC, NHẬP KẾT QUẢ', S10),
    ('XI', 'PHÂN QUYỀN', S11),
]

if __name__ == '__main__':
    ids = [(s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
    assert len(ids) == len(set(ids)), 'Trùng mã TC'
    total = len(ids)
    p0 = sum(1 for _, _, s in SECTIONS for tc in s if tc[2] == 'P0')
    print('Tong %d TC, P0 %d (%.0f%%)' % (total, p0, 100.0 * p0 / total))
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='Phiếu giao việc - Cập nhật ngày 19/11/2026',
                module_name='Phiếu giao việc', description_block=DESCRIPTION_BLOCK,
                sections=[(r, t, list(s)) for r, t, s in SECTIONS], loai='phieu')

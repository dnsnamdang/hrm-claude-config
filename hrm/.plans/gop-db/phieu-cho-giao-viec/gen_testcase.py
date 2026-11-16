# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu chờ giao việc" — skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu').

Chạy: python gen_testcase.py -> testcase.xlsx (tự chạy check_tc, phải "DAT", 0 lỗi).
Loại 'phieu' (xác định từ code 12/11/2026): màn là HÀNG ĐỢI chứng từ (5 tab) nhưng có thao tác đổi trạng thái chứng từ kèm hộp xác nhận /
lý do bắt buộc — Từ chối tiếp nhận xử lý (≈ KHÔNG DUYỆT PHIẾU: trả chứng từ về người lập, lý do bắt buộc, thông báo), Đóng hợp đồng / Hủy
duyệt hợp đồng (≈ HỦY PHIẾU: chứng từ rời trạng thái hiệu lực), In 1 phiếu yêu cầu lắp đặt (IN PHIẾU), mở chi tiết chứng từ (XEM CHI
TIẾT). 'danh_muc' không có nhóm Không duyệt / Hủy / In nên không khớp. Màn KHÔNG có Thêm mới / Sửa / Xóa / Khóa / Gửi duyệt / Duyệt /
Lịch sử riêng / Import > bỏ các nhóm đó. Tạo phiếu giao việc (mở màn khác, trừ số lượng chờ giao) đặt ở RÀNG BUỘC.
Nhóm: I Hiển thị (5 tab) · II Tìm kiếm & lọc (gồm Cài đặt bộ lọc) · III Không duyệt phiếu (Từ chối tiếp nhận) · IV Hủy phiếu (Đóng / Hủy
duyệt hợp đồng) · V Xem chi tiết · VI In phiếu · VII Tùy chỉnh cột · VIII Xuất Excel · IX Ràng buộc (Tạo phiếu giao việc, số lượng chưa
giao, liên kết hệ thống cũ) · X Phân quyền (cuối). Mỗi case ghi stt checklist nó phủ (ck) — gen_checklist.py đọc CK.
Khuôn: ../bien-ban-ban-giao-nghiem-thu/gen_testcase.py.
Nguồn hành vi (đọc 12/11/2026, nhánh develop): FE pages/customer-care/waiting-assign-tasks/**; BE Modules/Assign WaitingAssignTask*;
CustomerCare WrServiceContractController (từ chối / đóng / hủy duyệt), WrAssignTaskStoreService / RemainingService.
Số liệu mẫu: dev-hrm 12/11/2026, DNS Admin (có quyền Xem mức Tổng công ty, không thuộc phòng tiếp nhận nào): Hợp đồng 463 · PL bổ sung 24 ·
Phiếu bảo hành 560 · Lắp đặt bàn giao 141 · Giao việc khác 931.
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
MENU = 'Vào phân hệ CSKH sau bán > nhóm "Giao việc" > bấm "Phiếu chờ giao việc".'
ADV = 'Bấm Tìm kiếm nâng cao.'
TAB = lambda t: 'Bấm thẻ "%s".' % t  # noqa: E731
EMPTY = '"Không có dữ liệu phù hợp."'
REQ_REJ = '"Bắt buộc phải nhập lý do từ chối tiếp nhận"'
REQ_UN = '"Bắt buộc phải nhập lý do hủy duyệt"'
OK_REJ = '"Từ chối tiếp nhận xử lý thành công."'
OK_CLOSE = '"Đóng hợp đồng thành công."'
OK_UN = '"Hủy duyệt hợp đồng thành công."'
PLG = '"Hợp đồng đang có PL giảm chờ duyệt!"'
NO_CLOSE = '"Không thể đóng hợp đồng này (đã phát sinh chứng từ phía sau hoặc không đủ quyền)"'
NO_UN = '"Không thể hủy duyệt hợp đồng này (đã phát sinh chứng từ phía sau hoặc không đủ quyền)"'
NO_REJ = '"Không thể từ chối tiếp nhận hợp đồng này"'
CONFLICT = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'

ADMIN = ('Tài khoản DNS Admin: có quyền "Xem danh sách phiếu chờ giao việc" mức Tổng công ty, không thuộc phòng tiếp nhận nào. Dữ liệu: '
         'Hợp đồng 463, PL bổ sung 24, Phiếu bảo hành 560, Lắp đặt bàn giao 141, Giao việc khác 931.')
HD1 = ('Hợp đồng HDDV_TPE_HDQT_26_0003_SHD-20261102_1109_003 (Có hiệu lực, khách 29TPHPYE-1 - CÔNG TY TNHH TOYOTA HÀ ĐÔNG, Tổng '
       'thanh toán 5,625,000, DNS Admin tạo 02/11/2026 23:09) đứng đầu tab Hợp đồng.')
ACC_T = ('Tài khoản T: có quyền "Tạo phiếu giao việc", thuộc phòng CSKH HN; hợp đồng HDDV_X (Có hiệu lực, phòng tiếp nhận CSKH HN, '
         'còn 2 công sửa chữa chưa giao, chưa có phiếu giao việc, người lập là L).')
ACC_M = ('Tài khoản M: quản lý phòng KD2 (phòng của hợp đồng HDDV_Y, Có hiệu lực, chưa phát sinh phiếu giao việc / yêu cầu xuất kho / '
         'nhập kho / hạch toán dịch vụ, không còn phụ lục đang sống, người lập là L).')
ACC_N = 'Tài khoản N: không có quyền nào của màn, không quản lý phòng nào, thuộc phòng KD1.'

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
     'Màn Phiếu chờ giao việc (CSKH sau bán > Giao việc) là hàng đợi điều phối: liệt kê chứng từ còn công / dịch vụ / hàng CHƯA giao '
     'việc theo 5 thẻ (Hợp đồng, PL bổ sung, Phiếu bảo hành, Lắp đặt bàn giao, Giao việc khác) để phòng tiếp nhận lập phiếu giao việc; '
     'kèm thao tác Từ chối tiếp nhận xử lý, Đóng hợp đồng, Hủy duyệt hợp đồng, In phiếu yêu cầu lắp đặt, Xuất Excel.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Thẻ Hợp đồng / PL bổ sung: trạng thái Có hiệu lực.\n- Thẻ Phiếu bảo hành: trạng thái Đã duyệt, còn đánh dấu chờ giao việc.\n'
     '- Thẻ Lắp đặt bàn giao / Giao việc khác: trạng thái Chờ giao việc.\n'
     '- Và còn ít nhất 1 dòng có số lượng chưa giao việc lớn hơn 0 (riêng Giao việc khác chỉ xét trạng thái).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Chứng từ đã giao hết số lượng (trên phiếu giao việc đang chạy hoặc đã chốt).\n'
     '- Chứng từ ở trạng thái khác (Đang tạo, Chờ duyệt, Đóng, Không duyệt, Đã giao việc…).\n'
     '- Thẻ Hợp đồng / PL bổ sung / Lắp đặt: chứng từ có phòng tiếp nhận ngoài các phòng mình quản lý (khi không có quyền Xem mức '
     'Tổng công ty).'),
    ('4. Bộ lọc thời gian áp dụng cho',
     '- Ô Ngày tạo (cả 5 thẻ): khoảng từ ngày – đến ngày theo ngày tạo chứng từ, lấy trọn hai ngày biên.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Hợp đồng > phụ lục bổ sung / giảm; chứng từ nguồn > dòng công việc / dịch vụ / hàng > nhiều phiếu giao việc.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Số lượng chưa giao việc = số lượng của dòng - số lượng phụ lục giảm - số lượng đã giao (chốt) - tổng số lượng trên phiếu giao '
     'việc đang chạy (Đang giao, Đang nhập kết quả, Đã nhập kết quả, Đang duyệt kết quả).\n'
     '- Mỗi chứng từ hiện 1 dòng dù có nhiều dòng còn số lượng.'),
    ('7. Phân quyền cấp',
     '- Xem danh sách phiếu chờ giao việc — mức: Tổng công ty (mở rộng thẻ Hợp đồng, PL bổ sung, Lắp đặt ra mọi chứng từ). Mức Công '
     'ty có trong danh mục quyền nhưng màn không dùng (như không có quyền). Không cần quyền để mở màn.\n'
     '- Tạo phiếu giao việc: nút Tạo phiếu giao việc / Từ chối tiếp nhận ở thẻ Hợp đồng, PL bổ sung (cùng điều kiện đúng phòng tiếp nhận).\n'
     '- Xem hợp đồng ẩn giá: ô Tổng thanh toán trống với hợp đồng ngoài phạm vi giá.\n'
     '- Đóng hợp đồng: người lập / quản lý phòng của hợp đồng. Hủy duyệt: quản lý phòng của hợp đồng. Quyết toán: người lập.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Hiển thị a–b / N": a là dòng đầu trang, b là dòng cuối trang, N là tổng chứng từ của thẻ khớp bộ lọc trong phạm vi.'),
    ('9. Ghi chú đọc bảng',
     '- Mỗi thẻ ghi nhớ bộ lọc RIÊNG 10 phút trên trình duyệt (không theo tài khoản).\n'
     '- Ô Trạng thái liệt kê đủ trạng thái nhưng chỉ trạng thái của thẻ mới ra dữ liệu — chọn trạng thái khác luôn rỗng (đúng theo code).\n'
     '- Thẻ Phiếu bảo hành luôn hiện nút Tạo phiếu giao việc kể cả người không có quyền (giữ như hệ thống cũ).\n'
     '- Một số liên kết (Quyết toán, Xuất Excel 1 phiếu lắp đặt, Số phiếu / Số hợp đồng thẻ Lắp đặt) mở hệ thống cũ ở thẻ trình duyệt '
     'mới — chỉ kiểm việc mở đúng.\n- Mã hợp đồng dài tự xuống dòng, không bị cắt.'),
]

# ===================================================================== I. HIỂN THỊ
S1 = Sec(1)
S1.add('Mở màn hình từ menu', 'P0', ADMIN, [MENU],
       '—', ['Mở màn Phiếu chờ giao việc, tiêu đề trang "Phiếu chờ giao việc"', 'Thẻ "Hợp đồng" đang chọn',
             'Bảng tiêu đề "Hợp đồng chờ giao việc", dòng "Hiển thị 1–10 / 463"'], ck=[1, 2])
S1.add('Mục menu nằm đúng nhóm Giao việc', 'P1', ADMIN, ['Vào phân hệ CSKH sau bán.', 'Bấm nhóm "Giao việc" ở menu trái.'], '—',
       ['Nhóm Giao việc có 4 mục: Phiếu chờ giao việc, Phiếu giao việc, Phiếu giao việc được giao, Phiếu nhập kết quả',
        'Mục "Phiếu chờ giao việc" bấm được, không cần quyền'], ck=[1])
S1.add('Các nút chức năng', 'P1', ADMIN, [MENU], '—',
       ['Thanh thẻ: Hợp đồng, PL bổ sung, Phiếu bảo hành, Lắp đặt bàn giao, Giao việc khác',
        'Khối lọc: ô tìm "Tìm theo số hợp đồng", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc',
        'Bảng: nút Xuất Excel, nút Cấu hình cột hiển thị', 'KHÔNG có nút Tạo mới, Import'], ck=[3])
S1.add('Cột mặc định thẻ Hợp đồng và PL bổ sung', 'P0', ADMIN, [MENU, TAB('PL bổ sung')], '—',
       ['Thẻ Hợp đồng 11 cột: STT, Mã phiếu, Tổng thanh toán, Khách hàng, Người liên hệ - SĐT, Người tạo, Ngày tạo, Người duyệt, '
        'Ngày duyệt, Trạng thái, Hành động', 'Thẻ PL bổ sung cùng 11 cột', 'Không có cột nào bị ẩn mặc định'], ck=[4, 5])
S1.add('Cột mặc định thẻ Phiếu bảo hành, Lắp đặt, Giao việc khác','P0', ADMIN,
       [MENU, TAB('Phiếu bảo hành'), TAB('Lắp đặt bàn giao'), TAB('Giao việc khác')], '—',
       ['Phiếu bảo hành 8 cột: STT, Mã phiếu, Khách hàng, Người liên hệ - SĐT, Người tạo, Ngày tạo, Trạng thái, Hành động',
        'Lắp đặt bàn giao / Giao việc khác 8 cột: STT, Số phiếu, Số hợp đồng, Khách hàng, Người tạo, Ngày tạo, Trạng thái, Hành động',
        'Thẻ Lắp đặt: cột Người tạo dạng "Họ tên - SĐT"'], ck=[4])
S1.add('Dữ liệu dòng khớp chứng từ', 'P0', [ADMIN, HD1], [MENU], '—',
       ['Dòng 1: Mã phiếu HDDV_TPE_HDQT_26_0003_SHD-20261102_1109_003 (chữ thường, không bấm được)',
        'Tổng thanh toán 5,625,000; Khách hàng "29TPHPYE-1 - CÔNG TY TNHH TOYOTA HÀ ĐÔNG"; Người liên hệ - SĐT "Nguyen Van A - 0903123002"',
        'Người tạo DNS Admin, Ngày tạo 02/11/2026 23:09, Người duyệt DNS Admin, Ngày duyệt 02/11/2026 23:10',
        'Mã dài xuống dòng, không bị cắt dấu ba chấm'], ck=[6])
S1.add('Trạng thái của từng thẻ', 'P0', ADMIN, [MENU, 'Lần lượt bấm 5 thẻ, xem cột Trạng thái.'], '—',
       ['Hợp đồng / PL bổ sung: mọi dòng nhãn xanh dương "Có hiệu lực"', 'Phiếu bảo hành: mọi dòng nhãn xanh lá "Đã duyệt"',
        'Lắp đặt bàn giao / Giao việc khác: mọi dòng nhãn cam "Chờ giao việc"'], ck=[7])
S1.add('Thẻ không có chứng từ nào', 'P1', ACC_N, [MENU, TAB('Lắp đặt bàn giao')], '—',
       ['Bảng hiện %s' % EMPTY, 'Chân bảng "Không có phiếu nào."', 'Không lỗi, không treo'], ck=[8])
S1.add('Không có dữ liệu phù hợp bộ lọc', 'P1', ADMIN, [MENU, 'Nhập "ZZZ_KHONG_TON_TAI" vào ô tìm nhanh.', 'Bấm Tìm kiếm.'],
       'Từ khóa: ZZZ_KHONG_TON_TAI', ['Bảng hiện %s' % EMPTY, 'Không còn phân trang'], ck=[9, 30])
S1.add('Số dòng mặc định và đổi số dòng', 'P0', ADMIN, [MENU, 'Đổi Số dòng/trang = 20.'], 'Số dòng/trang: 20',
       ['Mặc định 10 dòng, lựa chọn 5 / 10 / 20 / 50 / 100', 'Sau khi đổi: hiện 20 dòng, "Hiển thị 1–20 / 463", về trang 1'],
       ck=[10, 11, 18])
S1.add('Trang trước / tiếp theo', 'P0', ADMIN, [MENU, 'Bấm nút tiến (>).', 'Bấm nút lùi (<).'], '—',
       ['Sau tiến: "Hiển thị 11–20 / 463", trang 2 được tô', 'Sau lùi: về trang 1, "Hiển thị 1–10 / 463"'], ck=[12])
S1.add('Trang đầu / cuối và trạng thái nút', 'P1', ADMIN, [MENU, 'Bấm nút về cuối (>>).', 'Bấm nút về đầu (<<).'], '—',
       ['Trang cuối 47: "Hiển thị 461–463 / 463", nút tiến / về cuối mờ',
        'Trang 1: nút lùi / về đầu mờ'], ck=[13, 14])
S1.add('STT liên tục giữa các trang', 'P1', ADMIN, [MENU, 'Bấm trang 2.'], '—', ['Dòng đầu trang 2 có STT 11, dòng cuối STT 20'], ck=[15])
S1.add('Tổng số bản ghi từng thẻ', 'P0', ADMIN, [MENU, 'Lần lượt bấm 5 thẻ, đọc dòng "Hiển thị".'], '—',
       ['Hợp đồng N = 463; PL bổ sung 24; Phiếu bảo hành 560; Lắp đặt bàn giao 141; Giao việc khác 931',
        'N đúng bằng số chứng từ chờ giao việc của thẻ (đối chiếu dữ liệu nguồn)'], ck=[16])
S1.add('Về trang 1 khi đổi bộ lọc', 'P1', ADMIN, [MENU, 'Bấm trang 3.', ADV, 'Chọn Người tạo = "Cao Xuân Khang".'],
       'Người tạo: Cao Xuân Khang', ['Danh sách nạp lại từ trang 1', 'Chỉ còn hợp đồng do Cao Xuân Khang tạo'], ck=[17, 41, 42])
S1.add('Thứ tự mặc định', 'P0', ADMIN, [MENU], '—',
       ['Dòng xếp theo Ngày tạo mới nhất ở trên (02/11/2026 23:09 > 21/10/2026 10:15 > …)'], ck=[19, 22])
S1.add('Sắp xếp tăng / giảm theo Mã phiếu', 'P1', ADMIN, [MENU, 'Bấm tiêu đề "Mã phiếu".', 'Bấm lại tiêu đề "Mã phiếu".'], '—',
       ['Lần 1: tăng dần (HDDV_TPE_HDQT_26_0003… > HDDV_TPE_HN_CSKH_25_0004… > …)', 'Lần 2: giảm dần',
        'Bố cục bảng không nhảy khi sắp xếp'], ck=[20, 21])
S1.add('Sắp xếp theo Ngày tạo, Ngày duyệt', 'P1', ADMIN, [MENU, 'Bấm tiêu đề "Ngày duyệt".', 'Bấm tiêu đề "Ngày tạo".'], '—',
       ['Ngày duyệt sắp tăng dần đúng', 'Ngày tạo sắp tăng dần đúng', 'Thẻ Phiếu bảo hành / Lắp đặt / Giao việc khác không có Ngày duyệt'],
       ck=[22])
S1.add('Cột không hỗ trợ sắp xếp', 'P2', ADMIN, [MENU, 'Bấm tiêu đề "Khách hàng", "Trạng thái", "Tổng thanh toán".'], '—',
       ['Không có biểu tượng sắp xếp, bấm không đổi thứ tự'], ck=[23])
S1.add('Giữ sắp xếp khi chuyển trang, về trang 1 khi đổi sắp xếp', 'P1', ADMIN,
       [MENU, 'Bấm tiêu đề "Mã phiếu" (tăng dần).', 'Bấm trang 2.', 'Bấm tiêu đề "Ngày tạo".'], '—',
       ['Trang 2 vẫn tăng dần theo Mã phiếu', 'Đổi sắp xếp > về trang 1'], ck=[24, 25])
S1.add('Chuyển thẻ giữ đúng thẻ trên đường dẫn khi tải lại', 'P1', ADMIN, [MENU, TAB('Phiếu bảo hành'), 'Nhấn F5.'], '—',
       ['Sau tải lại vẫn ở thẻ Phiếu bảo hành, "Hiển thị 1–10 / 560"'], ck=[46])
S1.add('Thẻ lạ trên thanh địa chỉ', 'P2', ADMIN, [MENU, 'Sửa tay tên thẻ trên thanh địa chỉ thành "abc", nhấn Enter.'], 'Thẻ: abc',
       ['Màn mở thẻ Hợp đồng, không lỗi, không lộ thêm dữ liệu'], ck=[296])
S1.add('Phiên đăng nhập hết hạn', 'P2', ADMIN, [MENU, 'Để phiên hết hạn, bấm trang 2.'], '—',
       ['Hệ thống báo hết phiên, chuyển về màn đăng nhập'], ck=[])
S1.add('Ẩn giá Tổng thanh toán','P0',
       'Tài khoản G: có quyền "Xem hợp đồng ẩn giá"; hợp đồng HDDV_Z do người khác lập, ngoài phạm vi giá của G, đang chờ giao việc.',
       [MENU, 'Tìm HDDV_Z.'], '—', ['Ô Tổng thanh toán của HDDV_Z trống', 'Các cột khác hiển thị bình thường'], ck=[6])

# ===================================================================== II. TÌM KIẾM & LỌC
S2 = Sec(2)
S2.add('Từ khóa chính xác', 'P0', ADMIN, [MENU, 'Nhập "HDDV_TPE_HN_KD2_26_0411_21.10".', 'Bấm Tìm kiếm.'], 'HDDV_TPE_HN_KD2_26_0411_21.10',
       ['Còn 1 dòng hợp đồng đó', '"Hiển thị 1–1 / 1"'], ck=[26, 35])
S2.add('Từ khóa một phần', 'P0', ADMIN, [MENU, 'Nhập "KD2_26_04".', 'Nhấn Enter.'], 'KD2_26_04',
       ['Chỉ còn hợp đồng có mã chứa "KD2_26_04"', 'Enter cho kết quả như bấm Tìm kiếm'], ck=[27, 35])
S2.add('Không phân biệt hoa / thường', 'P1', ADMIN, [MENU, 'Nhập "hddv_tpe_hn_kd2".', 'Bấm Tìm kiếm.'], 'hddv_tpe_hn_kd2',
       ['Kết quả giống khi nhập chữ hoa'], ck=[28])
S2.add('Có dấu / không dấu', 'P2', ADMIN, [MENU, TAB('Lắp đặt bàn giao'), 'Nhập "ycldbg".', 'Bấm Tìm kiếm.'], 'ycldbg',
       ['Mã phiếu không có dấu: "ycldbg" ra đủ phiếu TPE.YCLDBG…, TPSG.YCLDBG…'], ck=[29])
S2.add('Ký tự đặc biệt', 'P2', ADMIN, [MENU, 'Nhập "_26_".', 'Bấm Tìm kiếm.', 'Nhập "%".', 'Bấm Tìm kiếm.'], '_26_ ; %',
       ['Không lỗi', 'Ký tự % và _ được hiểu là ký tự đại diện (ra nhiều dòng hơn mong đợi) — đúng theo code'], ck=[31])
S2.add('Khoảng trắng đầu / cuối', 'P1', ADMIN, [MENU, 'Nhập "  KD2_26_0411  ".', 'Bấm Tìm kiếm.'], '"  KD2_26_0411  "',
       ['Kết quả như nhập "KD2_26_0411" (bỏ khoảng trắng)'], ck=[32])
S2.add('Từ khóa dài', 'P2', ADMIN, [MENU, 'Dán chuỗi 300 ký tự.', 'Bấm Tìm kiếm.'], 'Chuỗi 300 ký tự',
       ['Ô nhận đủ (không giới hạn ký tự)', 'Kết quả rỗng, không lỗi'], ck=[33])
S2.add('Xóa từ khóa', 'P1', ADMIN, [MENU, 'Tìm "KD2_26_04".', 'Xóa hết chữ trong ô, bấm Tìm kiếm.'], '—',
       ['Danh sách về đủ 463 dòng'], ck=[34])
S2.add('Bộ lọc mặc định', 'P1', ADMIN, [MENU, ADV], '—',
       ['Thẻ Hợp đồng có ô: Người duyệt hợp đồng, Trạng thái, Người tạo, Khách hàng, Ngày tạo, Công ty, Phòng ban, Bộ phận',
        'Mọi ô trống'], ck=[36])
S2.add('Ô lọc theo từng thẻ', 'P1', ADMIN, [MENU, TAB('Phiếu bảo hành'), ADV, TAB('Lắp đặt bàn giao'), TAB('Giao việc khác')], '—',
       ['Phiếu bảo hành: Trạng thái, Khách hàng, Hàng hóa, Ngày tạo, Công ty, Phòng ban, Bộ phận',
        'Lắp đặt: Khách hàng, Số hợp đồng, Người tạo, Ngày tạo, Công ty, Phòng ban (không có Trạng thái)',
        'Giao việc khác: Khách hàng, Số hợp đồng, Người tạo, Trạng thái, Ngày tạo, Công ty, Phòng ban'], ck=[36])
S2.add('Lọc Người duyệt hợp đồng','P0', ADMIN, [MENU, ADV, 'Chọn Người duyệt hợp đồng = "Trần Ngọc Duy".'], 'Trần Ngọc Duy',
       ['Chỉ còn hợp đồng có Người duyệt Trần Ngọc Duy', 'Lọc ngay, không cần bấm Tìm kiếm'], ck=[37, 47])
S2.add('Lọc Trạng thái đúng trạng thái của thẻ', 'P0', ADMIN, [MENU, ADV, 'Chọn Trạng thái = "Có hiệu lực".'], 'Có hiệu lực',
       ['Vẫn 463 dòng (thẻ chỉ có trạng thái này)'], ck=[37])
S2.add('Lọc Trạng thái khác trạng thái của thẻ', 'P1', ADMIN, [MENU, ADV, 'Chọn Trạng thái = "Đang tạo".'], 'Đang tạo',
       ['Bảng hiện %s' % EMPTY, 'Lưu ý: ô liệt kê 9 trạng thái nhưng chỉ "Có hiệu lực" ra dữ liệu — đúng theo code'], ck=[37, 40])
S2.add('Lọc Khách hàng gõ để tìm', 'P0', ADMIN, [MENU, ADV, 'Gõ "TOYOTA" vào ô Khách hàng.', 'Chọn "29TPHPYE-1 - CÔNG TY TNHH TOYOTA HÀ ĐÔNG".'],
       'TOYOTA', ['Gõ 1 ký tự chưa có gợi ý; từ 2 ký tự hiện tối đa 30 khách hàng', 'Chọn xong lọc ngay, còn hợp đồng của khách đó'],
       ck=[37])
S2.add('Lọc Hàng hóa (Phiếu bảo hành)','P0', ADMIN, [MENU, TAB('Phiếu bảo hành'), ADV, 'Nhập "điều hòa" vào ô Hàng hóa.', 'Bấm Tìm kiếm.'],
       'điều hòa', ['Chỉ còn phiếu bảo hành có dòng hàng tên hoặc mã chứa "điều hòa"', 'Ô chữ chỉ lọc khi bấm Tìm kiếm / Enter'], ck=[37, 47])
S2.add('Lọc Số hợp đồng thẻ Lắp đặt (một phần)','P0', ADMIN,
       [MENU, TAB('Lắp đặt bàn giao'), ADV, 'Nhập "KDTM_26_13" vào ô Số hợp đồng.', 'Bấm Tìm kiếm.'], 'KDTM_26_13',
       ['Còn phiếu yêu cầu lắp đặt có số hợp đồng chứa "KDTM_26_13" (vd TPE.YCLDBG.2026001897, 1890)'], ck=[37])
S2.add('Lọc Số hợp đồng thẻ Giao việc khác (khớp đúng)', 'P1', ADMIN,
       [MENU, TAB('Giao việc khác'), ADV, 'Nhập "HĐDA_TPE_HN_DA_26_0098" (thiếu đuôi).', 'Bấm Tìm kiếm.',
        'Nhập đủ "HĐDA_TPE_HN_DA_26_0098_18.TPE-APP".', 'Bấm Tìm kiếm.'], '2 giá trị',
       ['Thiếu đuôi: không ra dòng (khớp đúng, giữ như hệ thống cũ)', 'Đủ số: ra TPE.YCGVK.2026003024'], ck=[37])
S2.add('Lọc Ngày tạo', 'P0', ADMIN, [MENU, ADV, 'Chọn Ngày tạo từ 21/10/2026 đến 21/10/2026.'], '21/10/2026 – 21/10/2026',
       ['Chỉ còn hợp đồng tạo trong ngày 21/10/2026 (gồm 10:15, 08:58, 08:35, 08:13)', 'Lấy trọn 2 ngày biên'], ck=[37])
S2.add('Lọc Ngày tạo thẻ Lắp đặt', 'P1', ADMIN, [MENU, TAB('Lắp đặt bàn giao'), ADV, 'Chọn Ngày tạo từ 19/10/2026 đến 19/10/2026.'],
       '19/10/2026', ['Còn TPE.YCLDBG.2026001890, 1886, 1884 (lọc theo ngày tạo phiếu)'], ck=[37])
S2.add('Lọc Công ty, Phòng ban, Bộ phận', 'P1', ADMIN,
       [MENU, ADV, 'Chọn Công ty = TPSG.', 'Mở ô Phòng ban.', 'Đổi Công ty = TPE.'], 'TPSG > TPE',
       ['Chọn TPSG: còn hợp đồng của công ty TPSG (vd HDDV_TPSG_SG_CSKH_26_0402_12368)', 'Ô Phòng ban chỉ còn phòng của TPSG',
        'Đổi công ty: Phòng ban, Bộ phận bị xóa', 'Mọi người dùng đều chọn được mọi công ty'], ck=[37, 38])
S2.add('Hiện cả đơn vị đã khóa', 'P2', ADMIN, [MENU, ADV, 'Bấm biểu tượng ổ khóa cạnh nhãn Công ty.'], '—',
       ['Chú thích "Hiện cả công ty đã khoá"', 'Danh sách Công ty có thêm công ty đã khóa; bấm lại để ẩn'], ck=[37])
S2.add('Kết hợp tìm kiếm và nhiều tiêu chí', 'P0', ADMIN,
       [MENU, 'Nhập "KD2".', ADV, 'Chọn Người duyệt = "Trần Ngọc Duy", Ngày tạo 21/10/2026.', 'Bấm Tìm kiếm.'], '3 tiêu chí',
       ['Chỉ còn dòng thỏa CẢ 3 điều kiện (vd HDDV_TPE_HN_KD2_26_0411_21.10, 0410, 0409)', 'Tổng N và phân trang cập nhật theo'],
       ck=[38, 39, 41, 42])
S2.add('Sắp xếp sau khi lọc', 'P2', ADMIN, [MENU, 'Lọc Người duyệt = "Trần Ngọc Duy".', 'Bấm tiêu đề "Ngày duyệt".'], '—',
       ['Kết quả lọc được sắp theo Ngày duyệt tăng dần, bộ lọc giữ nguyên'], ck=[43])
S2.add('Làm mới', 'P0', ADMIN, [MENU, 'Nhập "KD2", lọc Người tạo, sắp theo Mã phiếu.', 'Bấm Làm mới.'], '—',
       ['Xóa ô tìm nhanh, mọi ô lọc, bỏ sắp xếp', 'Về trang 1, đủ 463 dòng, vẫn ở thẻ Hợp đồng'], ck=[44])
S2.add('Ghi nhớ bộ lọc khi sang màn khác rồi quay lại (dưới 10 phút)','P0', ADMIN,
       [MENU, 'Lọc Người tạo = "Cao Xuân Khang".', 'Vào màn Phiếu giao việc.', 'Sau 2 phút quay lại Phiếu chờ giao việc.'], '—',
       ['Bộ lọc Người tạo còn nguyên, danh sách đã lọc'], ck=[45])
S2.add('Bộ lọc hết hạn sau 10 phút', 'P2', ADMIN, [MENU, 'Lọc Người tạo.', 'Rời màn 11 phút rồi quay lại.'], '—',
       ['Bộ lọc về trống'], ck=[45])
S2.add('Ghi nhớ khi F5 và mở thẻ trình duyệt mới', 'P1', ADMIN,
       [MENU, 'Lọc Ngày tạo 21/10/2026.', 'Nhấn F5.', 'Mở màn ở thẻ trình duyệt mới.'], '—',
       ['Sau F5 còn bộ lọc', 'Thẻ trình duyệt mới cũng còn bộ lọc (ghi tạm trên trình duyệt, 10 phút)'], ck=[46, 47])
S2.add('Bộ lọc riêng từng thẻ', 'P1', ADMIN, [MENU, 'Lọc Người tạo ở thẻ Hợp đồng.', TAB('PL bổ sung'), TAB('Hợp đồng')], '—',
       ['Thẻ PL bổ sung không mang bộ lọc của thẻ Hợp đồng', 'Quay lại thẻ Hợp đồng còn bộ lọc'], ck=[45])
S2.add('Tài khoản khác cùng trình duyệt', 'P2', ADMIN + '\n' + ACC_N,
       [MENU, 'Lọc Người tạo.', 'Đăng xuất, đăng nhập N trong 10 phút.', 'Mở màn.'], '—',
       ['Bộ lọc vẫn còn (ghi theo trình duyệt, không theo tài khoản) — đúng theo code', 'Dữ liệu vẫn theo phạm vi của N'], ck=[48])
S2.add('Cài đặt bộ lọc: ẩn ô và đổi thứ tự', 'P1', ADMIN,
       [MENU, 'Bấm Cài đặt bộ lọc.', 'Bỏ tích "Người duyệt hợp đồng", kéo "Khách hàng" lên đầu.', 'Bấm Lưu.', ADV], '—',
       ['Cửa sổ "Cài đặt bộ lọc" có 6 mục của thẻ Hợp đồng', 'Thông báo "Cập nhật thành công"',
        'Khối lọc không còn Người duyệt hợp đồng, Khách hàng đứng đầu'], ck=[36])
S2.add('Cài đặt bộ lọc: Khôi phục mặc định, Đóng không lưu', 'P2', ADMIN,
       [MENU, 'Bấm Cài đặt bộ lọc.', 'Bấm Khôi phục mặc định.', 'Bấm Đóng.'], '—',
       ['Khôi phục: tích đủ 6 mục, thứ tự gốc', 'Đóng: không lưu, khối lọc giữ cấu hình cũ'], ck=[36])

# ===================================================================== III. KHÔNG DUYỆT PHIẾU — TỪ CHỐI TIẾP NHẬN
S3 = Sec(3)
S3.add('Điều kiện hiện nút Từ chối tiếp nhận (thẻ Hợp đồng)', 'P0', ACC_T, [MENU, 'Tìm HDDV_X.'], '—',
       ['Cột Hành động có Tạo phiếu giao việc và Từ chối tiếp nhận xử lý (biểu tượng người gạch đỏ)',
        'Hợp đồng có phòng tiếp nhận khác phòng của T: không có 2 nút này'], ck=[313])
S3.add('Ẩn nút khi hợp đồng đã có phiếu giao việc', 'P1', ACC_T + '\nHĐ HDDV_X2 (cùng phòng tiếp nhận) đã có 1 phiếu giao việc Đang giao, '
       'còn số lượng chưa giao.', [MENU, 'Tìm HDDV_X2.'], '—', ['Có nút Tạo phiếu giao việc', 'KHÔNG có nút Từ chối tiếp nhận xử lý'],
       ck=[313, 323])
S3.add('Giao diện hộp Từ chối tiếp nhận', 'P1', ACC_T, [MENU, 'Ở dòng HDDV_X bấm Từ chối tiếp nhận xử lý.'], '—',
       ['Tiêu đề "Từ chối tiếp nhận xử lý"', 'Nội dung "Bạn chắc muốn từ chối tiếp nhận xử lý cho hợp đồng \'HDDV_X\'?"',
        'Ô "Lý do từ chối" có dấu * đỏ, gợi ý "Nhập lý do từ chối"', 'Nút "Từ chối tiếp nhận" (đỏ) và "Hủy"'], ck=[314])
S3.add('Bỏ trống lý do', 'P0', ACC_T, [MENU, 'Bấm Từ chối tiếp nhận xử lý ở HDDV_X.', 'Để trống lý do, bấm "Từ chối tiếp nhận".'], '—',
       ['Ô viền đỏ, dưới ô báo %s' % REQ_REJ, 'Hộp không đóng, hợp đồng không đổi'], ck=[316])
S3.add('Lý do chỉ khoảng trắng', 'P1', ACC_T, [MENU, 'Mở hộp Từ chối ở HDDV_X.', 'Nhập 3 dấu cách, bấm "Từ chối tiếp nhận".'], '"   "',
       ['Báo %s, không gửi' % REQ_REJ], ck=[316, 317])
S3.add('Lý do dài, ký tự đặc biệt', 'P2', ACC_T, [MENU, 'Mở hộp Từ chối ở HDDV_X.', 'Nhập lý do 500 ký tự có "<>&\'".', 'Bấm "Từ chối tiếp nhận".'],
       'Lý do 500 ký tự', ['Lưu được (không giới hạn độ dài)', 'Lý do hiển thị đúng nguyên văn trong lịch sử hợp đồng'], ck=[317, 319])
S3.add('Từ chối tiếp nhận thành công (thẻ Hợp đồng)', 'P0', ACC_T,
       [MENU, 'Mở hộp Từ chối ở HDDV_X.', 'Nhập "Không thuộc khu vực phụ trách".', 'Bấm "Từ chối tiếp nhận".'], 'Lý do: Không thuộc khu vực phụ trách',
       ['Thông báo %s' % OK_REJ, 'HDDV_X rời khỏi thẻ Hợp đồng của T (không còn phòng tiếp nhận)', 'Hợp đồng vẫn trạng thái Có hiệu lực',
        'Màn Hợp đồng dịch vụ: phòng tiếp nhận trống, lý do từ chối lưu đúng'], ck=[315, 318, 319])
S3.add('Thông báo cho người lập hợp đồng', 'P0', ACC_T, ['Từ chối tiếp nhận HDDV_X như case trên.', 'Đăng nhập L, xem chuông thông báo.'], '—',
       ['L nhận thông báo từ chối tiếp nhận của HDDV_X, có lý do', 'Bấm thông báo mở hợp đồng để chọn lại phòng tiếp nhận'], ck=[321])
S3.add('Ghi lịch sử hợp đồng','P0', ACC_T, ['Từ chối tiếp nhận HDDV_X.', 'Mở Lịch sử thay đổi của HDDV_X ở màn Hợp đồng dịch vụ.'], '—',
       ['Có mốc "Thay đổi thông tin" người thực hiện T, thời gian lúc từ chối, phòng tiếp nhận cũ > trống, kèm lý do'], ck=[324])
S3.add('Người có quyền Xem mức Tổng công ty sau khi từ chối', 'P1', ADMIN + '\nHDDV_X vừa bị T từ chối tiếp nhận.', [MENU, 'Tìm HDDV_X.'],
       '—', ['Dòng HDDV_X vẫn hiện (không bó phạm vi)', 'Không có nút Tạo phiếu giao việc / Từ chối tiếp nhận'], ck=[320])
S3.add('Hủy thao tác từ chối', 'P0', ACC_T, [MENU, 'Mở hộp Từ chối ở HDDV_X, nhập lý do.', 'Bấm "Hủy" (hoặc dấu ×).'], '—',
       ['Hộp đóng', 'HDDV_X không đổi, vẫn trong danh sách, vẫn có nút'], ck=[322])
S3.add('Click ra ngoài hộp', 'P2', ACC_T, [MENU, 'Mở hộp Từ chối ở HDDV_X.', 'Bấm ra vùng tối ngoài hộp.'], '—',
       ['Hộp đóng, không thực hiện từ chối'], ck=[322])
S3.add('Hợp đồng vừa có phiếu giao việc ở tab khác', 'P1', ACC_T,
       [MENU, 'Mở hộp Từ chối ở HDDV_X (chưa bấm).', 'Ở thẻ trình duyệt khác lập phiếu giao việc cho HDDV_X.', 'Quay lại nhập lý do, bấm '
        '"Từ chối tiếp nhận".'], '—', ['Báo %s' % NO_REJ, 'Danh sách nạp lại'], ck=[323])
S3.add('Bấm liên tục nút Từ chối tiếp nhận', 'P2', ACC_T, [MENU, 'Mở hộp Từ chối ở HDDV_X, nhập lý do.', 'Bấm nhanh 3 lần.'], '—',
       ['Chỉ gửi 1 lần, 1 thông báo thành công, 1 mốc lịch sử'], ck=[323])
S3.add('Từ chối tiếp nhận PL bổ sung', 'P0', ACC_T + '\nPL bổ sung HDDV_X-PL (Có hiệu lực, phòng tiếp nhận CSKH HN, còn số lượng chưa giao, '
       'người lập P).', [MENU, TAB('PL bổ sung'), 'Ở HDDV_X-PL bấm Từ chối tiếp nhận xử lý.', 'Nhập lý do "Sai phòng", bấm "Từ chối tiếp nhận".'],
       'Lý do: Sai phòng', ['Thông báo %s' % OK_REJ, 'HDDV_X-PL rời thẻ PL bổ sung của T', 'P nhận thông báo "Từ chối" kèm khách hàng, người từ chối, lý do',
                            'Lưu ý: phụ lục KHÔNG ghi lịch sử (đúng theo code)'], ck=[315, 321])
S3.add('PL bổ sung đã đổi trạng thái', 'P1', ACC_T + '\nHDDV_X-PL vừa bị người khác đổi phòng tiếp nhận.',
       [MENU, TAB('PL bổ sung'), 'Mở hộp Từ chối ở HDDV_X-PL (dữ liệu cũ trên màn), nhập lý do, bấm xác nhận.'], '—',
       ['Báo %s' % CONFLICT, 'Danh sách nạp lại'], ck=[323])

# ===================================================================== IV. HỦY PHIẾU — ĐÓNG / HỦY DUYỆT HỢP ĐỒNG
S4 = Sec(4)
S4.add('Điều kiện hiện Đóng / Hủy duyệt', 'P0', ACC_M, [MENU, 'Tìm HDDV_Y.', 'Bấm nút ba chấm "Hành động khác".'], '—',
       ['Menu có "Đóng hợp đồng" và "Hủy duyệt hợp đồng" (đỏ)', 'Người lập L thấy Đóng hợp đồng + Quyết toán, KHÔNG thấy Hủy duyệt',
        'Thẻ PL bổ sung, Phiếu bảo hành, Lắp đặt, Giao việc khác không có 2 nút này'], ck=[])
S4.add('Ẩn Đóng / Hủy duyệt khi đã có chứng từ phía sau', 'P0', ACC_M + '\nHĐ HDDV_Y2 (phòng KD2) đã có 1 yêu cầu xuất kho.', [MENU, 'Tìm HDDV_Y2.'],
       '—', ['Không có Đóng hợp đồng, Hủy duyệt hợp đồng'], ck=[])
S4.add('Giao diện hộp Đóng hợp đồng', 'P1', ACC_M, [MENU, 'Ở HDDV_Y chọn Đóng hợp đồng.'], '—',
       ['Tiêu đề "Đóng hợp đồng"', 'Nội dung "Đóng hợp đồng \'HDDV_Y\'? Các phụ lục của hợp đồng cũng được đóng theo."',
        'Nút "Đóng hợp đồng" và "Hủy"'], ck=[])
S4.add('Đóng hợp đồng thành công', 'P0', ACC_M + '\nHDDV_Y có 1 PL bổ sung Có hiệu lực.', [MENU, 'Ở HDDV_Y chọn Đóng hợp đồng.', 'Bấm "Đóng hợp đồng".'],
       '—', ['Thông báo %s' % OK_CLOSE, 'HDDV_Y rời thẻ Hợp đồng; PL bổ sung của nó rời thẻ PL bổ sung',
             'Màn Hợp đồng dịch vụ: HDDV_Y và phụ lục ở trạng thái Đóng', 'Lịch sử HDDV_Y có mốc "Thay đổi trạng thái" Có hiệu lực > Đóng',
             'Không gửi thông báo'], ck=[])
S4.add('Hủy thao tác Đóng', 'P1', ACC_M, [MENU, 'Ở HDDV_Y chọn Đóng hợp đồng.', 'Bấm "Hủy".'], '—', ['Hộp đóng, hợp đồng không đổi'], ck=[])
S4.add('Đóng khi hợp đồng vừa phát sinh chứng từ', 'P1', ACC_M,
       [MENU, 'Mở hộp Đóng ở HDDV_Y.', 'Ở thẻ khác lập yêu cầu xuất kho cho HDDV_Y.', 'Bấm "Đóng hợp đồng".'], '—',
       ['Báo %s' % NO_CLOSE, 'Hợp đồng không đổi, danh sách nạp lại'], ck=[])
S4.add('Giao diện hộp Hủy duyệt', 'P1', ACC_M, [MENU, 'Ở HDDV_Y chọn Hủy duyệt hợp đồng.'], '—',
       ['Tiêu đề "Hủy duyệt hợp đồng"', 'Nội dung "Hủy duyệt hợp đồng \'HDDV_Y\'? Hợp đồng sẽ về trạng thái Không duyệt."',
        'Ô "Lý do hủy duyệt" có dấu *', 'Nút "Hủy duyệt" (đỏ) và "Hủy"'], ck=[])
S4.add('Hủy duyệt bỏ trống lý do', 'P0', ACC_M, [MENU, 'Mở hộp Hủy duyệt ở HDDV_Y.', 'Bấm "Hủy duyệt" khi ô trống.'], '—',
       ['Dưới ô báo %s, hộp không đóng' % REQ_UN], ck=[])
S4.add('Hủy duyệt thành công', 'P0', ACC_M, [MENU, 'Mở hộp Hủy duyệt ở HDDV_Y.', 'Nhập "Lập sai giá".', 'Bấm "Hủy duyệt".'],
       'Lý do: Lập sai giá', ['Thông báo %s' % OK_UN, 'HDDV_Y rời thẻ Hợp đồng; ở màn Hợp đồng dịch vụ trạng thái Không duyệt, lưu lý do',
                              'Lịch sử có mốc "Thay đổi trạng thái" kèm lý do', 'L nhận thông báo hủy duyệt'], ck=[])
S4.add('Không cho Hủy duyệt khi còn phụ lục đang sống', 'P1', ACC_M + '\nHDDV_Y3 (phòng KD2) có PL bổ sung Đang tạo.', [MENU, 'Tìm HDDV_Y3.'],
       '—', ['Có Đóng hợp đồng', 'KHÔNG có Hủy duyệt hợp đồng'], ck=[])
S4.add('Hủy duyệt khi người khác vừa đóng', 'P2', ACC_M, [MENU, 'Mở hộp Hủy duyệt ở HDDV_Y.', 'Người khác đóng HDDV_Y.', 'Nhập lý do, bấm "Hủy duyệt".'],
       '—', ['Báo %s' % NO_UN, 'Danh sách nạp lại, HDDV_Y không còn'], ck=[])

# ===================================================================== V. XEM CHI TIẾT
S5 = Sec(5)
S5.add('Mở chi tiết Phiếu bảo hành', 'P0', ADMIN, [MENU, TAB('Phiếu bảo hành'), 'Bấm mã TPE.PBH.2026.008226.'], '—',
       ['Mở màn "Chi tiết phiếu bảo hành: TPE.PBH.2026.008226" trong cùng thẻ trình duyệt',
        'Thông tin khớp dòng: khách 14TQUPVI-1 - CÔNG TY TNHH MỘT THÀNH VIÊN TOYOTA QUẢNG NINH, người tạo Cao Đình Hòe',
        'Các ô chỉ đọc, không có nút Lưu'], ck=[186, 187, 188, 189, 190, 191, 192])
S5.add('Mở chi tiết Phiếu yêu cầu giao việc khác', 'P0', ADMIN, [MENU, TAB('Giao việc khác'), 'Bấm số TPE.YCGVK.2026003069.'], '—',
       ['Mở "Chi tiết phiếu yêu cầu giao việc khác: TPE.YCGVK.2026003069" kèm nhãn Chờ giao việc',
        'Khách hàng 15TPHPVI-30 - CÔNG TY TNHH ETECHCAR TIÊN TIẾN, người tạo DNS Admin', 'Có khối Lịch sử của phiếu'],
       ck=[186, 187, 188, 189, 193, 195])
S5.add('Mã phiếu thẻ Hợp đồng / PL không bấm được', 'P1', ADMIN, [MENU, 'Bấm vào mã hợp đồng dòng 1.'], '—',
       ['Không mở màn nào (giữ như hệ thống cũ)'], ck=[186])
S5.add('Quay lại giữ thẻ và bộ lọc', 'P0', ADMIN,
       [MENU, TAB('Phiếu bảo hành'), 'Lọc Ngày tạo 01/10/2026 – 07/10/2026.', 'Bấm mã TPE.PBH.2026.008226.', 'Bấm Quay lại.'], '—',
       ['Về thẻ Phiếu bảo hành', 'Bộ lọc Ngày tạo còn nguyên (trong 10 phút)'], ck=[196, 197])
S5.add('Không có quyền xem ở màn nguồn', 'P2', ACC_N, [MENU, TAB('Phiếu bảo hành'), 'Bấm 1 mã phiếu bảo hành ngoài phạm vi xem của N.'], '—',
       ['Màn nguồn chuyển sang trang không tìm thấy, không lộ dữ liệu'], ck=[288])

# ===================================================================== VI. IN PHIẾU
S6 = Sec(6)
S6.add('In phiếu yêu cầu lắp đặt', 'P0', ADMIN, [MENU, TAB('Lắp đặt bàn giao'), 'Ở dòng TPSG.YCLDBG.2026001899 bấm In (máy in).'], '—',
       ['Mở cửa sổ "Xem trước phiếu yêu cầu lắp đặt bàn giao"', 'Bản in "PHIẾU YÊU CẦU LẮP ĐẶT BÀN GIAO", Số phiếu TPSG.YCLDBG.2026001899, '
        'Ngày 21/10/2026', 'Khách hàng 50TPHPBI-2 - CÔNG TY TNHH Ô TÔ NAM THÁI BÌNH DƯƠNG, Hợp đồng HĐ_TPSG_KV1_26_0248_1408.HD.SCCDH.TP.NTNT',
        'Có bảng "Danh sách thiết bị cần lắp đặt, bàn giao"'], ck=[])
S6.add('Letterhead theo công ty của phiếu', 'P1', ADMIN, [MENU, TAB('Lắp đặt bàn giao'), 'In 1 phiếu TPSG và 1 phiếu TPE.'], '—',
       ['Phiếu TPSG: letterhead công ty TPSG', 'Phiếu TPE: letterhead công ty TPE', 'Không theo công ty người đang đăng nhập'], ck=[])
S6.add('Bấm In trong cửa sổ', 'P1', ADMIN, ['Mở xem trước như case 1.', 'Bấm nút "In".'], '—', ['Hộp thoại in của trình duyệt mở, đúng khổ'], ck=[])
S6.add('Đóng cửa sổ in', 'P2', ADMIN, ['Mở xem trước như case 1.', 'Bấm dấu × (hoặc Esc).'], '—',
       ['Cửa sổ đóng, danh sách giữ nguyên trang, bộ lọc'], ck=[])
S6.add('Thẻ khác không có nút In', 'P2', ADMIN, [MENU, 'Xem cột Hành động thẻ Hợp đồng, Phiếu bảo hành, Giao việc khác.'], '—',
       ['Không có nút In'], ck=[])

# ===================================================================== VII. TÙY CHỈNH CỘT
S7 = Sec(7)
S7.add('Mở cửa sổ Tùy chỉnh cột', 'P0', ADMIN, [MENU, 'Bấm Cấu hình cột hiển thị.'], '—',
       ['Cửa sổ "Tuỳ chỉnh cột", 11 cột thẻ Hợp đồng, "Đang chọn 11/11 cột"', 'STT, Mã phiếu, Hành động có ổ khóa, không bỏ tích được'],
       ck=[198, 199, 200, 203, 205])
S7.add('Ẩn cột và lưu', 'P0', ADMIN, [MENU, 'Mở Tùy chỉnh cột.', 'Bỏ tích "Người duyệt", "Ngày duyệt".', 'Bấm Lưu.'], '—',
       ['Thông báo "Cập nhật thành công"', 'Bảng còn 9 cột', 'Tổng N, bộ lọc không đổi'], ck=[202, 206, 210, 211])
S7.add('Hiện lại cột đã ẩn', 'P1', ADMIN, ['Đã ẩn Người duyệt.', 'Mở Tùy chỉnh cột, tích lại "Người duyệt", bấm Lưu.'], '—',
       ['Cột Người duyệt hiện lại đúng vị trí'], ck=[201])
S7.add('Kéo thả đổi thứ tự', 'P1', ADMIN, [MENU, 'Mở Tùy chỉnh cột.', 'Kéo "Ngày tạo" lên trên "Khách hàng".', 'Bấm Lưu.'], '—',
       ['Cột Ngày tạo đứng trước Khách hàng', 'Cột khóa không kéo được'], ck=[204])
S7.add('Đóng không lưu', 'P1', ADMIN, [MENU, 'Mở Tùy chỉnh cột, bỏ tích "Khách hàng".', 'Bấm Đóng.'], '—',
       ['Bảng vẫn có cột Khách hàng'], ck=[207])
S7.add('Ghi nhớ sau F5, theo tài khoản và theo thẻ', 'P1', ADMIN + '\n' + ACC_N,
       ['Đã ẩn Người duyệt ở thẻ Hợp đồng (DNS Admin).', 'Nhấn F5.', 'Bấm thẻ PL bổ sung.', 'Đăng nhập N, mở thẻ Hợp đồng.'], '—',
       ['Sau F5 vẫn ẩn', 'Thẻ PL bổ sung vẫn đủ cột (cấu hình riêng từng thẻ)', 'N vẫn thấy đủ cột'], ck=[208, 209])

# ===================================================================== VIII. XUẤT EXCEL
S8 = Sec(8)
S8.add('Mở cửa sổ chọn trường', 'P0', ADMIN, [MENU, 'Bấm Xuất Excel.'], '—',
       ['Cửa sổ "Chọn trường xuất file", 9 trường: Mã phiếu, Tổng thanh toán, Khách hàng, Người liên hệ - SĐT, Người tạo, Ngày tạo, '
        'Người duyệt, Ngày duyệt, Trạng thái', 'Tích sẵn trường ứng với cột đang hiện, "Đang chọn 9/9 trường"'], ck=[212, 213, 214])
S8.add('Xuất trường mặc định', 'P0', ADMIN, [MENU, 'Bấm Xuất Excel.', 'Bấm Xuất file.'], '—',
       ['Tải file "phieu_cho_giao_viec_hop_dong.xlsx", báo "Xuất Excel thành công."',
        'File có ảnh tiêu đề rộng bằng bảng, tiêu đề "Phiếu chờ giao việc - Hợp đồng", cột STT + 9 cột', '463 dòng (không phân trang)'],
       ck=[215, 221, 223, 224, 225, 227])
S8.add('Chọn tất cả / Bỏ chọn hết', 'P1', ADMIN, [MENU, 'Bấm Xuất Excel.', 'Bấm Bỏ chọn hết.', 'Bấm Chọn tất cả.'], '—',
       ['Bỏ chọn hết: nút Xuất file khóa', 'Chọn tất cả: tích 9 trường, nút mở'], ck=[216, 218])
S8.add('Xuất một số trường, đổi thứ tự', 'P1', ADMIN, [MENU, 'Bấm Xuất Excel.', 'Chỉ tích Mã phiếu, Khách hàng, Ngày tạo; kéo Ngày tạo lên đầu.', 'Bấm Xuất file.'],
       '—', ['File có STT, Ngày tạo, Mã phiếu, Khách hàng đúng thứ tự'], ck=[217, 226])
S8.add('Xuất theo tìm kiếm và bộ lọc', 'P0', ADMIN, [MENU, 'Tìm "KD2", lọc Người duyệt "Trần Ngọc Duy".', 'Xuất Excel > Xuất file.'], '—',
       ['File chỉ có các dòng đang lọc, cùng thứ tự sắp xếp trên màn'], ck=[219, 220, 228])
S8.add('Xuất danh sách rỗng', 'P1', ADMIN, [MENU, 'Tìm "ZZZ".', 'Xuất Excel > Xuất file.'], '—',
       ['Vẫn tải file chỉ có dòng tên cột, báo "Xuất Excel thành công." (đúng theo code)'], ck=[222])
S8.add('Định dạng dữ liệu trong file', 'P1', ADMIN, ['Xuất thẻ Hợp đồng.', 'Mở file.'], '—',
       ['Ngày dạng dd/mm/yyyy hh:mm', 'Tổng thanh toán là số, có phân cách hàng nghìn', 'Tên khách hàng tiếng Việt có dấu hiển thị đúng'],
       ck=[229, 230])
S8.add('Mỗi thẻ 1 file riêng', 'P1', ADMIN, [MENU, 'Lần lượt ở 4 thẻ còn lại bấm Xuất Excel > Xuất file.'], '—',
       ['File: phieu_cho_giao_viec_pl_bo_sung / _phieu_bao_hanh / _lap_dat_ban_giao / _giao_viec_khac .xlsx',
        'Phiếu bảo hành 6 trường; Lắp đặt / Giao việc khác 6 trường (Số phiếu, Số hợp đồng, Khách hàng, Người tạo, Ngày tạo, Trạng thái)'],
       ck=[213, 223])
S8.add('Ẩn giá trong file', 'P1', 'Tài khoản G có quyền "Xem hợp đồng ẩn giá"; HDDV_Z ngoài phạm vi giá.', ['Xuất thẻ Hợp đồng có HDDV_Z.'], '—',
       ['Ô Tổng thanh toán của HDDV_Z trống trong file'], ck=[228])
S8.add('Đóng cửa sổ không xuất', 'P2', ADMIN, [MENU, 'Bấm Xuất Excel.', 'Bấm Đóng.'], '—', ['Không tải file'], ck=[212])

# ===================================================================== IX. RÀNG BUỘC
S9 = Sec(9)
S9.add('Tạo phiếu giao việc từ thẻ Phiếu bảo hành', 'P0', ADMIN, [MENU, TAB('Phiếu bảo hành'), 'Ở TPE.PBH.2026.008226 bấm Tạo phiếu giao việc.'],
       '—', ['Mở màn "Tạo phiếu giao việc" trong cùng thẻ trình duyệt', 'Số phiếu bảo hành TPE.PBH.2026.008226 và khách hàng điền sẵn',
             'Bảng chỉ có các dòng còn số lượng chưa giao'], ck=[49, 274])
S9.add('Tạo phiếu giao việc từ thẻ Hợp đồng', 'P0', ACC_T, [MENU, 'Ở HDDV_X bấm Tạo phiếu giao việc.'], '—',
       ['Mở màn Tạo phiếu giao việc với HDDV_X chọn sẵn, 2 công sửa chữa còn chưa giao'], ck=[49])
S9.add('Chặn tạo khi có PL giảm chờ duyệt', 'P0', ACC_T + '\nHDDV_X có 1 phụ lục giảm đang Chờ duyệt.', [MENU, 'Ở HDDV_X bấm Tạo phiếu giao việc.'], '—',
       ['Thông báo %s' % PLG, 'Ở lại danh sách, không mở màn Tạo'], ck=[268])
S9.add('Tạo từ thẻ Lắp đặt, Giao việc khác (chỉ xét phòng tiếp nhận)', 'P1',
       'Tài khoản T2: KHÔNG có quyền "Tạo phiếu giao việc", thuộc phòng KT1; phiếu TPE.YCLDBG.A và TPE.YCGVK.B có phòng tiếp nhận KT1.',
       [MENU, TAB('Lắp đặt bàn giao'), 'Ở TPE.YCLDBG.A bấm Tạo phiếu giao việc.', TAB('Giao việc khác'), 'Ở TPE.YCGVK.B bấm Tạo phiếu giao việc.'],
       '—', ['Cả 2 dòng có nút và mở được màn Tạo phiếu giao việc (giữ như hệ thống cũ)'], ck=[269])
S9.add('Giao một phần — chứng từ còn trong thẻ', 'P0', ACC_T,
       ['Từ HDDV_X lập phiếu giao việc giao 1 trong 2 công, Lưu và duyệt.', MENU], 'SL giao: 1/2',
       ['HDDV_X vẫn ở thẻ Hợp đồng', 'Bấm Tạo phiếu giao việc lần nữa: chỉ còn 1 công chưa giao'], ck=[281, 283])
S9.add('Giao hết — chứng từ rời thẻ', 'P0', ACC_T, ['Lập tiếp phiếu giao việc cho công còn lại của HDDV_X.', MENU], 'SL giao: 1 còn lại',
       ['HDDV_X không còn trong thẻ Hợp đồng, tổng N giảm 1'], ck=[281, 286])
S9.add('Giao việc khác chuyển Đã giao việc','P0', 'Phiếu TPE.YCGVK.B Chờ giao việc.', ['Lập phiếu giao việc từ TPE.YCGVK.B.', MENU, TAB('Giao việc khác')],
       '—', ['TPE.YCGVK.B rời thẻ', 'Màn Phiếu yêu cầu giao việc khác: trạng thái Đã giao việc, lịch sử ghi mốc chuyển trạng thái'], ck=[281])
S9.add('Hủy phiếu giao việc — chứng từ quay lại thẻ','P0', 'Phiếu giao việc PGV1 (Đang giao) giao hết HDDV_X.',
       ['Hủy PGV1 ở màn Phiếu giao việc.', MENU], '—', ['HDDV_X xuất hiện lại ở thẻ Hợp đồng với đủ số lượng'], ck=[284, 285])
S9.add('Phiếu bảo hành giao hết rời thẻ','P0', 'Phiếu bảo hành PBH1 Đã duyệt còn 1 thiết bị chưa giao.', ['Lập phiếu giao việc giao hết PBH1.', MENU,
       TAB('Phiếu bảo hành')], '—', ['PBH1 rời thẻ Phiếu bảo hành'], ck=[281])
S9.add('Chứng từ mới duyệt xuất hiện trong thẻ', 'P0', 'Hợp đồng HDDV_N vừa được duyệt (Có hiệu lực), phòng tiếp nhận CSKH HN.',
       [MENU, 'Đăng nhập T, tìm HDDV_N.'], '—', ['HDDV_N có trong thẻ Hợp đồng ngay sau khi duyệt'], ck=[274])
S9.add('Đổi tên khách hàng hiển thị đồng bộ', 'P2', 'Khách hàng của HDDV_X vừa đổi tên ở Danh mục khách hàng.', [MENU, 'Tìm HDDV_X.'], '—',
       ['Cột Khách hàng hiện mã KH + tên khách ghi trên hợp đồng'], ck=[278])
S9.add('Quay lại từ màn Tạo về đúng thẻ', 'P1', ADMIN, [MENU, TAB('Phiếu bảo hành'), 'Bấm Tạo phiếu giao việc ở dòng 1.', 'Bấm Quay lại.'], '—',
       ['Về Phiếu chờ giao việc, thẻ Phiếu bảo hành'], ck=[282])
S9.add('Quyết toán hợp đồng mở hệ thống cũ', 'P1', 'Tài khoản L: người lập HDDV_X.', [MENU, 'Ở HDDV_X bấm ba chấm > Quyết toán hợp đồng.'], '—',
       ['Mở màn tạo quyết toán hợp đồng của hệ thống cũ ở thẻ trình duyệt mới, kèm HDDV_X', 'Người không phải người lập không thấy nút'], ck=[])
S9.add('Liên kết thẻ Lắp đặt mở hệ thống cũ', 'P2', ADMIN, [MENU, TAB('Lắp đặt bàn giao'), 'Bấm số TPSG.YCLDBG.2026001899.',
       'Bấm số hợp đồng HĐ_TPSG_KV1_26_0248_1408.HD.SCCDH.TP.NTNT.', 'Bấm Xuất Excel (biểu tượng file) ở dòng.'], '—',
       ['Mỗi liên kết mở hệ thống cũ ở thẻ trình duyệt mới', 'Màn Phiếu chờ giao việc giữ nguyên'], ck=[])

# ===================================================================== X. PHÂN QUYỀN
S10 = Sec(10)
S10.add('Không có quyền nào vẫn xem được', 'P0', ACC_N, [MENU, 'Lần lượt bấm 5 thẻ.'], '—',
        ['Mở được màn', 'Thẻ Hợp đồng, PL bổ sung, Lắp đặt: rỗng (N không quản lý phòng nào)',
         'Thẻ Phiếu bảo hành 560, Giao việc khác 931 (không bó phạm vi)'], ck=[287, 299])
S10.add('Quyền Xem mức Tổng công ty', 'P0', ADMIN, [MENU], '—', ['Thẻ Hợp đồng 463, PL bổ sung 24, Lắp đặt 141 — mọi công ty'], ck=[287, 299])
S10.add('Quyền Xem mức Công ty','P0', 'Tài khoản V2: quyền "Xem danh sách phiếu chờ giao việc" mức Công ty, quản lý phòng KD2.', [MENU], '—',
        ['Chỉ thấy chứng từ có phòng tiếp nhận KD2 (như không có quyền) — mức Công ty không được màn dùng (đúng theo code)'], ck=[299])
S10.add('Phạm vi theo phòng quản lý', 'P0', 'Tài khoản Q: không có quyền Xem, quản lý phòng CSKH HN (công ty TPE) và KV1 (công ty TPSG).',
        [MENU, 'Xem thẻ Hợp đồng, Lắp đặt bàn giao.'], '—',
        ['Chỉ chứng từ có phòng tiếp nhận CSKH HN hoặc KV1, cả 2 công ty', 'Không thấy chứng từ phòng khác'], ck=[299])
S10.add('Thiếu quyền Tạo phiếu giao việc', 'P0', 'Tài khoản T3: thuộc phòng CSKH HN, KHÔNG có quyền "Tạo phiếu giao việc".', [MENU, 'Tìm HDDV_X.'], '—',
        ['Không có nút Tạo phiếu giao việc, Từ chối tiếp nhận ở thẻ Hợp đồng, PL bổ sung'], ck=[295, 289])
S10.add('Phiếu bảo hành luôn hiện nút Tạo', 'P1', 'Tài khoản T3 như trên.', [MENU, TAB('Phiếu bảo hành'), 'Bấm Tạo phiếu giao việc ở dòng 1.'], '—',
        ['Nút hiện ở mọi dòng (giữ như hệ thống cũ)', 'Màn Tạo phiếu giao việc từ chối vì thiếu quyền, quay về thẻ Phiếu bảo hành'], ck=[295, 296])
S10.add('Bị gỡ quyền giữa lúc thao tác','P0', ACC_T, [MENU, 'Admin gỡ quyền "Tạo phiếu giao việc" của T.', 'T mở hộp Từ chối ở PL bổ sung, nhập lý do, xác nhận.'],
        '—', ['Hệ thống từ chối, báo không có quyền', 'Tải lại danh sách: nút biến mất'], ck=[298, 297])
S10.add('Xuất Excel, Tùy chỉnh cột không cần quyền', 'P1', ACC_N, [MENU, TAB('Giao việc khác'), 'Xuất Excel > Xuất file.'], '—',
        ['Xuất được 931 dòng (theo phạm vi thẻ)'], ck=[293])
S10.add('Đổi công ty đang làm việc', 'P2', 'Tài khoản K: quyền Xem mức Tổng công ty chỉ ở công ty TPE, không ở TPSG.',
        [MENU, 'Đổi công ty đang làm việc sang TPSG.', 'Mở lại màn.'], '—',
        ['Thẻ Hợp đồng / PL / Lắp đặt tính lại theo phòng quản lý (quyền tính ở công ty đang làm việc)'], ck=[299])

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'KHÔNG DUYỆT PHIẾU – TỪ CHỐI TIẾP NHẬN XỬ LÝ', S3),
    ('IV', 'HỦY PHIẾU – ĐÓNG HỢP ĐỒNG, HỦY DUYỆT HỢP ĐỒNG', S4),
    ('V', 'XEM CHI TIẾT CHỨNG TỪ NGUỒN', S5),
    ('VI', 'IN PHIẾU YÊU CẦU LẮP ĐẶT BÀN GIAO', S6),
    ('VII', 'TÙY CHỈNH CỘT', S7),
    ('VIII', 'XUẤT DANH SÁCH EXCEL', S8),
    ('IX', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S9),
    ('X', 'PHÂN QUYỀN', S10),
]

if __name__ == '__main__':
    ids = [(s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
    assert len(ids) == len(set(ids)), 'Trùng mã TC'
    total = len(ids)
    p0 = sum(1 for _, _, s in SECTIONS for tc in s if tc[2] == 'P0')
    print('Tong %d TC, P0 %d (%.0f%%)' % (total, p0, 100.0 * p0 / total))
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='Phiếu chờ giao việc - Cập nhật ngày 12/11/2026',
                module_name='Phiếu chờ giao việc', description_block=DESCRIPTION_BLOCK,
                sections=[(r, t, list(s)) for r, t, s in SECTIONS], loai='phieu')

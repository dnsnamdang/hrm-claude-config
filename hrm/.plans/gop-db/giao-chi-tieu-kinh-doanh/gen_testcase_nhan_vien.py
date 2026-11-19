# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu giao chỉ tiêu kinh doanh theo nhân viên" (#11651) — skill testcase-documenter,
KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu').

Chạy: python gen_testcase_nhan_vien.py -> "testcase - Phiếu giao chỉ tiêu kinh doanh theo nhân viên.xlsx"
(tự chạy check_tc, phải "DAT", 0 lỗi + bộ lọc thuật ngữ "OK - sach").

Nhóm: I Hiển thị (2 lối vào) · II Tìm kiếm & lọc · III Thêm mới · IV Chỉnh sửa · V Gửi duyệt · VI Duyệt + Hủy duyệt
· VII Không duyệt (Từ chối) · VIII Hủy phiếu · IX Lịch sử · X Xem chi tiết · XI In · XII Tùy chỉnh cột · XIII Xuất Excel
(danh sách + 1 phiếu) · XIV Ràng buộc (phiếu phòng ban, phiếu cũ, yêu cầu issue) · XV Phân quyền (cuối).
Nguồn hành vi (đọc 19/11/2026): BE Modules/Finance BusinessTarget* (EmployeeService, Transitions, Access, Numbers,
Controller, Request, print blade), Catalog sale.php; FE components/business-target/*, pages/finance/business-target-employees,
utils/business-target.js, businessTargetActionsMixin.js, businessTargetExcel.js, stickyTheadRows.js (develop), sale-hub.js.
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets'))
from tc_chuan import build_chuan  # noqa: E402

TODAY = '19/11/2026'
OUT = 'testcase - Phiếu giao chỉ tiêu kinh doanh theo nhân viên.xlsx'


def T(no, func, prio, pre, steps, td, exp):
    if isinstance(pre, (list, tuple)):
        pre = '\n'.join(pre)
    if isinstance(td, (list, tuple)):
        td = '\n'.join(td)
    st = '\n'.join('%d. %s' % (i + 1, s) for i, s in enumerate(steps))
    ex = '\n'.join(x if x.startswith('- ') else '- ' + x for x in exp)
    return ('%03d' % no, func, prio, pre, st, td, ex)


class Sec(list):
    def add(self, func, prio, pre, steps, td, exp):
        self.append(T(len(self) + 1, func, prio, pre, steps, td, exp))


# ============================================================================ HẰNG SỐ DÙNG CHUNG
TEN = 'Phiếu giao chỉ tiêu kinh doanh theo nhân viên'
ten = 'phiếu giao chỉ tiêu kinh doanh theo nhân viên'
MENU = 'Vào phân hệ Bán hàng > nhóm "Kế hoạch" > mục "Giao chỉ tiêu kinh doanh" > bấm "Theo nhân viên".'
MENU_PB = 'Vào phân hệ Bán hàng > nhóm "Kế hoạch" > mục "Giao chỉ tiêu kinh doanh" > bấm "Theo phòng ban".'
MENU_CD = 'Vào phân hệ Bán hàng > nhóm "Phê Duyệt" > mục "Kế hoạch & chỉ tiêu" > bấm "Giao chỉ tiêu NV chờ duyệt".'
ADV = 'Bấm Tìm kiếm nâng cao.'
LIST_TITLE = 'Danh sách ' + ten
EMPTY = '"Không có phiếu giao chỉ tiêu nào"'
REQ = '"Bắt buộc phải nhập"'
CHECK = '"Vui lòng kiểm tra lại dữ liệu nhập"'
NOPERM = '"Bạn không có quyền thực hiện thao tác này"'
CHANGED = '"Trạng thái đã bị thay đổi. Vui lòng load lại trang"'
LOCKED = '"Chỉ sửa được phiếu ở trạng thái Đang tạo."'
NO_TARGET = 'Phòng chưa có chỉ tiêu được duyệt cho năm 2027'
NO_REV = '"Phiếu chưa giao chỉ tiêu doanh số cho nhân viên — không gửi được"'
NEED_DS = '"Bắt buộc nhập doanh số vì đã có SL Khách"'
NEED_SL = '"Bắt buộc nhập SL Khách vì đã có doanh số"'
UNSAVED = 'hộp "Thông tin chưa lưu" nội dung "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?", 2 nút Ở lại / Thoát'
Q_VIEW = '"Xem chỉ tiêu"'
Q_CRE = '"Tạo chỉ tiêu kinh doanh theo nhân viên"'
Q_APP = '"Duyệt chỉ tiêu kinh doanh theo nhân viên"'
Q_APP_PB = '"Duyệt chỉ tiêu kinh doanh theo phòng ban"'

# Phiếu mẫu
M = 'TPE_CTKDNV_2027.00071'    # A, KD1, 2027, Đang tạo
P2 = 'TPE_CTKDNV_2027.00072'   # E, KD2, 2027, Chờ duyệt
P3 = 'TPE_CTKDNV_2026.00065'   # A, KD1, 2026, Đã duyệt (B duyệt 10/11/2026)
P4 = 'TPE_CTKDNV_2026.00066'   # A, KD1, 2026, Hủy
P5 = 'TPE_CTKDNV_2026.00067'   # E, KD2, 2026, Đang tạo
P6 = 'TPSG_CTKDNV_2027.00061'  # X, công ty TPSG, Đã duyệt
P7 = 'TPE_CTKDNV_2026.00068'   # F, KD3, 2026, Chờ duyệt
PB = 'TPE_CTKD_2027.00051'     # phiếu phòng ban 2027 Đã duyệt

NV1 = 'Nguyễn Văn Nam - 11010031'
NV2 = 'Lê Thị Hoa - 11010032'
NV3 = 'Phạm Đức Đông - 11010033'
NV4 = 'Hoàng Minh Tuấn - 11020045'

ACC_A = ('Tài khoản A (Trần Văn Bình - 11010021): trưởng phòng Kinh doanh 1 (KD1), công ty TPE; quản lý 2 phòng KD1 và KD3; '
         'có quyền %s, KHÔNG có quyền %s và %s.' % (Q_CRE, Q_VIEW, Q_APP))
ACC_B = 'Tài khoản B (Đỗ Thị Lan - 11000005): công ty TPE, chỉ có quyền %s.' % Q_APP
ACC_E = 'Tài khoản E (Vũ Quang Huy - 11020010): trưởng phòng KD2, công ty TPE, có quyền %s.' % Q_CRE
ACC_D = 'Tài khoản D: nhân viên công ty TPE, không có quyền nào của màn, không quản lý phòng nào.'
ACC_V3 = 'Tài khoản V3: công ty TPE, chỉ có quyền %s mức Công ty.' % Q_VIEW
ACC_V4 = 'Tài khoản V4: công ty TPE, chỉ có quyền %s mức Tổng công ty.' % Q_VIEW
TARGET = ('Phiếu giao chỉ tiêu theo phòng ban %s (công ty TPE, năm 2027, Đã duyệt) có phòng KD1:\n'
          '- Hà Nội, khối Dự án: Khách hãng Hàng hóa SL 6 / Doanh số 3,000,000,000; Khách hãng Dịch vụ 2 / 600,000,000; '
          'Khách khác Hàng hóa 3 / 800,000,000\n'
          '- Hà Nội, khối Dân dụng: Khách hãng Hàng hóa 4 / 2,000,000,000\n'
          '- Hải Phòng, khối Dự án: Khách hãng Hàng hóa 5 / 1,500,000,000; Khách hãng Dịch vụ 1 / 200,000,000\n'
          'Phòng KD2 có chỉ tiêu tại Đà Nẵng; phòng KD3 không có chỉ tiêu năm 2027.' % PB)
TARGET_S = 'Chỉ tiêu 2027 của KD1 (phiếu phòng ban %s Đã duyệt): Hà Nội và Hải Phòng như bộ chuẩn.' % PB
FREE = 'Phòng KD1 chưa có phiếu giao chỉ tiêu theo nhân viên năm 2027 còn hiệu lực.'
DATA = ('Bộ dữ liệu thử (ngoài các phiếu này không còn phiếu theo nhân viên nào):\n'
        '- %s: A lập, KD1, năm 2027, Đang tạo\n- %s: E lập, KD2, năm 2027, Chờ duyệt\n'
        '- %s: A lập, KD1, năm 2026, Đã duyệt (B duyệt 10/11/2026)\n- %s: A lập, KD1, năm 2026, Hủy\n'
        '- %s: E lập, KD2, năm 2026, Đang tạo\n- %s: F lập, KD3, năm 2026, Chờ duyệt\n'
        '- %s: X lập, công ty TPSG, năm 2027, Đã duyệt' % (M, P2, P3, P4, P5, P7, P6))
FILL = ['Hà Nội - dòng 1: Nhân viên %s; Khách hãng Hàng hóa SL 6 / Doanh số 3,000,000,000; Khách khác Hàng hóa 2 / 500,000,000' % NV1,
        'Hà Nội - dòng 2: Nhân viên %s; Khách hãng Hàng hóa 4 / 2,000,000,000; Khách hãng Dịch vụ 2 / 600,000,000' % NV2,
        'Hải Phòng - dòng 1: Nhân viên %s; Khách hãng Hàng hóa 5 / 1,500,000,000' % NV1]
PLAN_M = 'Phiếu M %s (A lập %s, KD1, năm 2027, Đang tạo) đã nhập đúng 3 dòng như bộ chuẩn: %s.' % (M, TODAY, '; '.join(FILL))
OPEN_NEW = [MENU, 'Bấm Tạo mới.', 'Chọn Năm: Năm 2027.']
PEND = 'Phiếu %s của E (KD2, năm 2027, Chờ duyệt), có doanh số giao cho nhân viên.' % P2
APPR = 'Phiếu %s của A (KD1, năm 2026, Đã duyệt do B duyệt 10/11/2026).' % P3
OPEN_P2_B = [MENU_CD, 'Bấm số phiếu %s.' % P2]


# ============================================================================ I. HIỂN THỊ
S1 = Sec()
S1.add('Mở màn hình từ menu (lối vào danh sách)', 'P0', [ACC_A, DATA], [MENU], '—',
       ['Mở màn có tiêu đề trang "%s"' % TEN, 'Bảng có tiêu đề "%s"' % LIST_TITLE,
        'Có đúng 3 phiếu A lập: %s, %s, %s' % (M, P3, P4), 'Không thấy phiếu của E, F, X'])
S1.add('Mục menu nằm đúng nhóm Kế hoạch', 'P1', ACC_D, ['Vào phân hệ Bán hàng.', 'Mở nhóm "Kế hoạch" ở menu trái, mở mục "Giao chỉ tiêu kinh doanh".'], '—',
       ['Mục có 3 màn: "Theo phòng ban", "Theo nhân viên", "Phát triển sản phẩm"',
        'Mục "Theo nhân viên" hiện với mọi tài khoản, kể cả không có quyền nào'])
S1.add('Mở lối vào "Giao chỉ tiêu NV chờ duyệt"', 'P0', [ACC_B, DATA], [MENU_CD], '—',
       ['Tiêu đề trang "%s chờ duyệt"' % TEN, 'Bảng có tiêu đề "%s chờ duyệt"' % LIST_TITLE,
        'Có đúng 2 phiếu Chờ duyệt của công ty TPE: %s, %s' % (P2, P7),
        'KHÔNG có %s (Đã duyệt), %s / %s (Đang tạo), %s (Hủy), %s (công ty TPSG)' % (P3, M, P5, P4, P6)])
S1.add('Mục chờ duyệt chỉ hiện khi có quyền Duyệt', 'P0', ACC_A, ['Vào phân hệ Bán hàng > nhóm "Phê Duyệt" > mở mục "Kế hoạch & chỉ tiêu".'], '—',
       ['KHÔNG có mục "Giao chỉ tiêu NV chờ duyệt"', 'Lý do: A không có quyền %s' % Q_APP])
S1.add('Lối vào chờ duyệt không có Tạo mới và ô lọc Trạng thái', 'P1', ACC_B, [MENU_CD, ADV], '—',
       ['Không có nút Tạo mới', 'Bộ lọc nâng cao không có ô Trạng thái', 'Vẫn có nút Xuất Excel và nút Cấu hình cột hiển thị'])
S1.add('Chuyển từ lối vào chờ duyệt sang lối vào danh sách', 'P0', [ACC_B, DATA], [MENU_CD, MENU], '—',
       ['Lối vào chờ duyệt: 2 phiếu', 'Lối vào danh sách: tiêu đề "%s", có 3 phiếu %s, %s, %s' % (LIST_TITLE, P2, P3, P7),
        'Phạm vi theo lối vào vừa bấm, không giữ phạm vi chờ duyệt'])
S1.add('Đổi bộ lọc rồi mở lối vào khác', 'P0', [ACC_B, DATA], [MENU, ADV, 'Chọn Trạng thái: Đã duyệt, bấm Tìm kiếm.', MENU_CD], 'Trạng thái: Đã duyệt',
       ['Lối vào chờ duyệt vẫn ra đủ 2 phiếu Chờ duyệt, không bị lọc Đã duyệt về 0 phiếu', 'Ô Trạng thái không hiện ở lối vào chờ duyệt'])
S1.add('Bấm Làm mới giữ phạm vi lối vào', 'P1', [ACC_B, DATA], [MENU_CD, 'Gõ "%s" vào ô tìm, bấm Tìm kiếm.' % P2, 'Bấm Làm mới.'], 'Từ khoá: %s' % P2,
       ['Sau tìm: còn 1 dòng %s' % P2, 'Sau Làm mới: ô tìm trống, quay về 2 phiếu chờ duyệt (không chuyển sang 3 phiếu của lối vào danh sách)'])
S1.add('Tham số lối vào trên thanh địa chỉ bị sửa thành giá trị lạ', 'P1', [ACC_B, DATA],
       [MENU_CD, 'Sửa phần tham số lối vào trên thanh địa chỉ thành chữ "abc", nhấn Enter.'], 'Tham số: abc',
       ['Không lỗi trang', 'Màn về lối vào danh sách thường (tiêu đề "%s", 3 phiếu)' % LIST_TITLE, 'Không lộ thêm phiếu nào ngoài phạm vi của B'])
S1.add('Các nút chức năng của danh sách', 'P1', ACC_A, [MENU], '—',
       ['Khối lọc: ô tìm "Tìm theo số phiếu", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao',
        'Trên bảng: nút Tạo mới, Xuất Excel, Cấu hình cột hiển thị', 'KHÔNG có nút Xóa, Import'])
S1.add('Các cột mặc định hiển thị', 'P0', [ACC_A, DATA], [MENU], '—',
       ['Cột theo thứ tự: STT, Số phiếu, Phòng ban, Năm, Người tạo, Ngày tạo, Người duyệt, Trạng thái, Hành động',
        'Cột Ngày duyệt ẩn mặc định'])
S1.add('Dữ liệu dòng khớp phiếu đã lập', 'P0', [ACC_A, APPR], [MENU, 'Bật cột Ngày duyệt.', 'Xem dòng %s.' % P3], '—',
       ['Số phiếu %s, Phòng ban "Kinh doanh 1", Năm 2026' % P3, 'Người tạo "Trần Văn Bình", Ngày tạo dạng dd/mm/yyyy',
        'Người duyệt "Đỗ Thị Lan", Ngày duyệt 10/11/2026, Trạng thái Đã duyệt'])
S1.add('Trạng thái và màu nhãn', 'P1', [ACC_A, DATA, 'A có thêm 1 phiếu Chờ duyệt năm 2028 để đủ 4 trạng thái.'], [MENU], '—',
       ['Đang tạo màu xám, Chờ duyệt màu cam, Đã duyệt màu xanh lá, Hủy màu đỏ', 'Không có trạng thái "Từ chối" riêng (phiếu bị từ chối về Đang tạo)'])
S1.add('Phiếu Đang tạo của người khác không hiện', 'P0', [ACC_V4, DATA], [MENU, 'Tìm "%s" và "%s".' % (M, P5)], '—',
       ['Không thấy %s, %s dù V4 xem được mức Tổng công ty' % (M, P5), 'Phiếu Đang tạo chỉ người lập thấy'])
S1.add('Danh sách chưa có dữ liệu', 'P1', ACC_D, [MENU], '—', ['Bảng hiện %s' % EMPTY, 'Không lỗi trang'])
S1.add('Không có dữ liệu khớp bộ lọc', 'P1', [ACC_A, DATA], [MENU, ADV, 'Chọn Năm 2028, bấm Tìm kiếm.'], 'Năm: 2028',
       ['Bảng hiện %s' % EMPTY, 'Tổng số bằng 0'])
S1.add('Phân trang mặc định 10 dòng', 'P1', 'Tài khoản V4 thấy 25 phiếu (thêm dữ liệu các năm 2023 tới 2028).', [MENU], '—',
       ['Trang 1 có 10 dòng, dòng tổng ghi 1–10 trên 25 phiếu', 'Có 3 trang'])
S1.add('Đổi số dòng / trang về trang 1', 'P1', 'Như trên, đang ở trang 2.', [MENU, 'Sang trang 2.', 'Đổi số dòng/trang thành 20.'], '20 dòng/trang',
       ['Về trang 1, hiện 20 dòng, còn 2 trang'])
S1.add('Trang trước / sau, đầu / cuối và trạng thái nút', 'P2', 'Như trên (25 phiếu, 10 dòng/trang).',
       [MENU, 'Bấm trang sau, trang cuối, trang trước, trang đầu.'], '—',
       ['Mỗi lần bấm đổi đúng trang', 'Ở trang 1 nút trang trước / trang đầu không bấm được; ở trang 3 nút trang sau / trang cuối không bấm được'])
S1.add('STT liên tục giữa các trang', 'P2', 'Như trên.', [MENU, 'Sang trang 2.'], '—', ['Trang 2 có STT từ 11 tới 20'])
S1.add('Sắp xếp mặc định theo Ngày tạo mới trước', 'P0', 'Tài khoản A: 3 phiếu tạo ngày 01/11, 10/11 và %s.' % TODAY, [MENU], '—',
       ['Phiếu tạo %s đứng đầu, phiếu 01/11 đứng cuối' % TODAY])
S1.add('Sắp xếp tăng / giảm theo cột', 'P1', [ACC_V4, DATA], [MENU, 'Bấm tiêu đề cột Số phiếu 2 lần.', 'Bấm tiêu đề cột Năm, Phòng ban, Trạng thái.'], '—',
       ['Số phiếu tăng dần rồi giảm dần', 'Các cột Phòng ban, Năm, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái đều sắp xếp được'])
S1.add('Cột không hỗ trợ sắp xếp', 'P2', ACC_A, [MENU, 'Bấm tiêu đề cột STT, Hành động.'], '—', ['Không đổi thứ tự, không có mũi tên sắp xếp'])
S1.add('Giữ sắp xếp khi chuyển trang, về trang 1 khi đổi sắp xếp', 'P2', 'Tài khoản V4, 25 phiếu.',
       [MENU, 'Sắp Số phiếu tăng dần.', 'Sang trang 2.', 'Bấm sắp Số phiếu giảm dần.'], '—',
       ['Trang 2 vẫn theo Số phiếu tăng dần', 'Đổi sắp xếp thì về trang 1'])
S1.add('Hành động ở dòng thay đổi theo trạng thái', 'P0', [ACC_A, DATA], [MENU, 'Mở biểu tượng ba chấm ở cột Hành động từng dòng.'], '—',
       ['%s (Đang tạo): biểu tượng Sửa; trong ba chấm có Xem, Gửi duyệt, Hủy phiếu, In, Xuất Excel, Lịch sử' % M,
        '%s (Đã duyệt): Xem, In, Xuất Excel, Lịch sử (không Sửa, Gửi duyệt, Hủy phiếu, Hủy duyệt vì A không có quyền Duyệt)' % P3,
        '%s (Hủy): chỉ Xem, Lịch sử' % P4])
S1.add('Hành động của người có quyền Duyệt', 'P0', [ACC_B, DATA], [MENU, 'Mở ba chấm dòng %s và %s.' % (P2, P3)], '—',
       ['%s (Chờ duyệt): Xem, Duyệt, In, Xuất Excel, Lịch sử; KHÔNG có Từ chối ở danh sách' % P2,
        '%s (Đã duyệt): Xem, Hủy duyệt, In, Xuất Excel, Lịch sử' % P3,
        'Bấm Duyệt ở dòng chỉ mở màn Chi tiết của phiếu, không duyệt ngay'])
S1.add('Bấm số phiếu mở màn Chi tiết', 'P1', [ACC_A, DATA], [MENU, 'Bấm số phiếu %s.' % P3], '—',
       ['Mở màn tiêu đề "Chi tiết %s: %s" kèm nhãn trạng thái Đã duyệt' % (ten, P3)])

# ============================================================================ II. TÌM KIẾM & LỌC
S2 = Sec()
S2.add('Tìm đúng số phiếu', 'P0', [ACC_V4, DATA], [MENU, 'Gõ "%s", bấm Tìm kiếm.' % P7], 'Từ khoá: %s' % P7, ['Chỉ còn 1 dòng %s' % P7])
S2.add('Tìm một phần số phiếu', 'P1', [ACC_V4, DATA], [MENU, 'Gõ "00068", bấm Tìm kiếm.'], 'Từ khoá: 00068', ['Ra %s' % P7])
S2.add('Không phân biệt hoa / thường', 'P2', [ACC_V4, DATA], [MENU, 'Gõ "tpsg_ctkdnv", bấm Tìm kiếm.'], 'Từ khoá: tpsg_ctkdnv', ['Ra %s' % P6])
S2.add('Ô tìm nhanh chỉ tìm theo số phiếu', 'P1', [ACC_V4, DATA], [MENU, 'Gõ "Kinh doanh 1", bấm Tìm kiếm.'], 'Từ khoá: Kinh doanh 1',
       ['Bảng hiện %s (ô tìm chỉ theo số phiếu, đúng như gợi ý "Tìm theo số phiếu")' % EMPTY, 'Muốn lọc theo phòng thì dùng ô Phòng ban'])
S2.add('Từ khoá không tồn tại', 'P1', ACC_V4, [MENU, 'Gõ "ZZZ999", bấm Tìm kiếm.'], 'Từ khoá: ZZZ999', ['Bảng hiện %s' % EMPTY])
S2.add('Ký tự đặc biệt', 'P2', ACC_V4, [MENU, 'Lần lượt tìm: %   _   \'   <b>'], "% ; _ ; ' ; <b>",
       ['Không lỗi trang, không treo', 'Tìm "%" hoặc "_" mà ra toàn bộ danh sách thì ghi nhận lỗi'])
S2.add('Khoảng trắng đầu / cuối', 'P2', [ACC_V4, DATA], [MENU, 'Gõ "   %s   ", bấm Tìm kiếm.' % P7], 'Có 3 dấu cách hai đầu', ['Vẫn ra %s' % P7])
S2.add('Từ khoá rất dài', 'P2', ACC_V4, [MENU, 'Dán 300 ký tự vào ô tìm, bấm Tìm kiếm.'], '300 ký tự "a"', ['Không lỗi trang, bảng rỗng'])
S2.add('Xoá từ khoá, Enter và nút Tìm kiếm', 'P1', [ACC_V4, DATA], [MENU, 'Gõ "%s" rồi nhấn Enter.' % P7, 'Xoá hết chữ, bấm nút Tìm kiếm.'], '—',
       ['Nhấn Enter ra 1 dòng %s' % P7, 'Xoá từ khoá rồi Tìm kiếm: quay về đủ 5 phiếu', 'Gõ chưa bấm thì danh sách chưa lọc'])
S2.add('Các ô lọc nâng cao theo quyền', 'P0', [ACC_A, ACC_V4], ['A: %s' % MENU, 'A bấm Tìm kiếm nâng cao.', 'V4 làm tương tự.'], '—',
       ['A: các ô Phòng ban, Năm, Người tạo, Người duyệt, Trạng thái (không có ô Công ty)',
        'V4 (mức Tổng công ty): có thêm ô Công ty đứng đầu', 'Các ô dùng nhãn nổi, không có chữ gợi ý trùng nhãn'])
S2.add('Lọc theo Năm', 'P0', [ACC_V4, DATA], [MENU, ADV, 'Chọn Năm 2027.'], 'Năm: 2027',
       ['Còn %s, %s' % (P2, P6), 'Ô Năm có lựa chọn từ 2028 xuống 2023'])
S2.add('Lọc theo Trạng thái', 'P0', [ACC_V4, DATA], [MENU, ADV, 'Chọn Trạng thái Chờ duyệt.'], 'Trạng thái: Chờ duyệt',
       ['Còn %s, %s' % (P2, P7), 'Ô Trạng thái có 4 lựa chọn: Đang tạo, Chờ duyệt, Đã duyệt, Hủy'])
S2.add('Lọc theo Phòng ban', 'P0', [ACC_V3, DATA], [MENU, ADV, 'Chọn Phòng ban: Kinh doanh 1.'], 'Phòng ban: Kinh doanh 1',
       ['Còn %s, %s' % (P3, P4), 'Ô Phòng ban liệt kê các phòng của công ty TPE'])
S2.add('Ô Phòng ban phụ thuộc ô Công ty', 'P0', [ACC_V4, DATA], [MENU, ADV, 'Chọn Phòng ban: Kinh doanh 1.', 'Chọn Công ty: TPSG.', 'Mở ô Phòng ban.'], 'Công ty: TPSG',
       ['Đổi Công ty sang TPSG thì ô Phòng ban tự xoá "Kinh doanh 1"', 'Ô Phòng ban chỉ còn phòng của TPSG', 'Kết quả chỉ còn %s' % P6])
S2.add('Lọc Người tạo và Người duyệt', 'P1', [ACC_V4, DATA], [MENU, ADV, 'Chọn Người tạo: Trần Văn Bình.', 'Đổi sang Người duyệt: Đỗ Thị Lan.'], '—',
       ['Người tạo Trần Văn Bình: %s, %s' % (P3, P4), 'Người duyệt Đỗ Thị Lan: %s' % P3])
S2.add('Công ty / phòng đã khoá vẫn có trong ô lọc', 'P2', [ACC_V4, 'Phòng KD3 đã bị khoá nhưng còn phiếu %s.' % P7], [MENU, ADV, 'Mở ô Phòng ban.'], '—',
       ['Có "Kinh doanh 3" với biểu tượng ổ khóa trước tên', 'Chọn được và ra %s' % P7])
S2.add('Lọc kết hợp nhiều tiêu chí và từ khoá', 'P1', [ACC_V4, DATA], [MENU, ADV, 'Chọn Năm 2026, Trạng thái Chờ duyệt.', 'Gõ "00068", bấm Tìm kiếm.'],
       'Năm 2026; Chờ duyệt; từ khoá 00068', ['Chỉ còn %s' % P7])
S2.add('Tổng số, phân trang và sắp xếp sau lọc', 'P1', 'Tài khoản V4, 25 phiếu, 12 phiếu Chờ duyệt; đang ở trang 3.',
       [MENU, 'Sang trang 3.', ADV, 'Chọn Trạng thái Chờ duyệt.', 'Sắp Số phiếu tăng dần.'], '—',
       ['Về trang 1, tổng 12 phiếu, 2 trang', '12 phiếu sắp tăng dần, bộ lọc giữ nguyên'])
S2.add('Làm mới xoá điều kiện', 'P1', [ACC_V4, DATA], [MENU, ADV, 'Chọn Năm 2027, gõ từ khoá "TPE".', 'Bấm Làm mới.'], '—',
       ['Mọi ô lọc và ô tìm trống', 'Quay về đủ 5 phiếu, trang 1'])
S2.add('Giữ bộ lọc khi sang màn khác rồi quay lại', 'P1', [ACC_V4, DATA], [MENU, 'Lọc Trạng thái Chờ duyệt.', 'Mở Xem 1 phiếu rồi bấm Quay lại.'], '—',
       ['Bộ lọc Chờ duyệt còn nguyên, danh sách 2 phiếu'])
S2.add('Tải lại trang (F5) và mở thẻ mới', 'P2', [ACC_V4, DATA], [MENU, 'Lọc Chờ duyệt.', 'Nhấn F5.', 'Mở màn ở 1 thẻ trình duyệt mới.'], '—',
       ['Bộ lọc còn trong 10 phút ở cả 2 cách', 'Quá 10 phút thì về mặc định'])
S2.add('Tài khoản khác cùng trình duyệt', 'P2', 'A và V4 dùng chung 1 trình duyệt.', ['V4 lọc Chờ duyệt rồi đăng xuất.', 'A đăng nhập, %s' % MENU], '—',
       ['Danh sách của A vẫn chỉ trong phạm vi của A',
        'Lưu ý: bộ lọc ghi nhớ theo trình duyệt — A có thể thấy ô Trạng thái còn Chờ duyệt, bấm Làm mới thì về 3 phiếu của A'])

# ============================================================================ III. THÊM MỚI
S3 = Sec()
S3.add('Giao diện form Tạo mới', 'P0', [ACC_A, TARGET, FREE], [MENU, 'Bấm Tạo mới.'], '—',
       ['Tiêu đề "Tạo %s"' % ten, 'Khối "Thông tin phiếu": Số phiếu (khoá, gợi ý "Số phiếu tự sinh khi lưu"), Năm (dấu * đỏ), Phòng ban (dấu * đỏ)',
        'Khối "Chi tiết" có 2 thẻ "Giao chỉ tiêu", "Tổng hợp"', 'Chân trang: Lưu, Lưu và gửi, Quay lại',
        'KHÔNG có ô Công ty (công ty = công ty người lập), KHÔNG có nút Lưu nháp, Lưu và tiếp tục'])
S3.add('Năm mặc định và danh sách năm', 'P0', [ACC_A, 'Hôm nay %s.' % TODAY], [MENU, 'Bấm Tạo mới.', 'Mở ô Năm.'], '—',
       ['Năm mặc định "Năm 2026" (năm hiện tại)', 'Ô Năm có từ "Năm 2025" tới "Năm 2036"', 'Không có nút xoá trống ô Năm'])
S3.add('Phòng ban mặc định là phòng của mình', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW, 'Năm 2027',
       ['Ô Phòng ban tự chọn "Kinh doanh 1" (phòng của A) và tự nạp bảng chỉ tiêu', 'Không phải tự chọn lại phòng'])
S3.add('Phòng của mình không có chỉ tiêu thì không chọn sẵn', 'P1',
       'Tài khoản A3: thuộc phòng KD3 (không có chỉ tiêu 2027), quản lý KD1 và KD3, có quyền %s.' % Q_CRE, OPEN_NEW, 'Năm 2027',
       ['Ô Phòng ban để trống, gợi ý "Chọn phòng ban"', 'Khối Chi tiết hiện dòng "Chọn phòng ban để nạp chỉ tiêu"'])
S3.add('Ô Phòng ban chỉ có phòng mình quản lý và có chỉ tiêu', 'P0', [ACC_A, TARGET], OPEN_NEW + ['Mở ô Phòng ban.'], '—',
       ['Chỉ có "Kinh doanh 1"', 'KHÔNG có "Kinh doanh 3" (A quản lý nhưng phòng chưa có chỉ tiêu Đã duyệt năm 2027)',
        'KHÔNG có "Kinh doanh 2" (A không quản lý)'])
S3.add('Có quyền Xem mức Công ty thì chọn được mọi phòng có chỉ tiêu', 'P0',
       ['Tài khoản G: công ty TPE, có quyền %s và %s mức Công ty; không quản lý phòng nào.' % (Q_CRE, Q_VIEW), TARGET], OPEN_NEW + ['Mở ô Phòng ban.'], '—',
       ['Có "Kinh doanh 1" và "Kinh doanh 2"', 'Không có "Kinh doanh 3" (chưa có chỉ tiêu)', 'Không có phòng của công ty khác'])
S3.add('Nạp chỉ tiêu của phòng theo Tỉnh/TP', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW, 'Năm 2027; Phòng ban: Kinh doanh 1',
       ['Bảng có 2 Tỉnh/TP: I "Hà Nội (0 nhân viên)", II "Hải Phòng (0 nhân viên)"; mỗi tỉnh có sẵn 1 dòng chọn nhân viên trống',
        'Dòng "Chỉ tiêu giao" của Hà Nội: Khách hãng Hàng hóa 10 / 5,000,000,000 (= 6 + 4 của 2 khối cùng tỉnh), Khách hãng Dịch vụ 2 / 600,000,000, Khách khác Hàng hóa 3 / 800,000,000',
        'Dòng "Chỉ tiêu giao" của Hải Phòng: Khách hãng Hàng hóa 5 / 1,500,000,000, Dịch vụ 1 / 200,000,000',
        'Ô số bằng 0 ở dòng Chỉ tiêu giao để trống'])
S3.add('Tiêu đề bảng 3 tầng, 12 cột số', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW, '—',
       ['Cột STT và cột "Tỉnh/TP / Nhân viên kinh doanh" (có dấu * đỏ)',
        'Tầng 1: Khách hãng, Khách khác, Tổng cộng; tầng 2: mỗi nhóm có Hàng hóa, Dịch vụ; tầng 3: mỗi cặp có SL khách, Doanh số (đủ 12 cột số)',
        'Nhóm Tổng cộng tự tính, không có ô nhập'])
S3.add('Dòng TỔNG và Chỉ tiêu giao ở đầu bảng', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW, '—',
       ['Ngay dưới tiêu đề có dòng STT "TỔNG", nhãn "2 Tỉnh/TP · 0 nhân viên", các ô số hiện 0',
        'Dòng "Chỉ tiêu giao" của cả phòng: Khách hãng Hàng hóa 15 / 6,500,000,000, Khách hãng Dịch vụ 3 / 800,000,000, Khách khác Hàng hóa 3 / 800,000,000; Tổng cộng Hàng hóa 18 / 7,300,000,000, Dịch vụ 3 / 800,000,000',
        'Góc phải khối Chi tiết ghi "2 Tỉnh/TP · 0 nhân viên"'])
S3.add('Ô "Hiển thị đến cấp"', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Ở tiêu đề cột cây chọn "Chỉ Tỉnh/TP".', 'Bấm mũi tên ở dòng Hà Nội.', 'Chọn lại "Đến Nhân viên".'], '—',
       ['Ô có 2 lựa chọn "Chỉ Tỉnh/TP", "Đến Nhân viên"; mặc định "Đến Nhân viên" (mở hết)',
        '"Chỉ Tỉnh/TP": ẩn dòng nhân viên, còn dòng tỉnh và dòng Chỉ tiêu giao', 'Bấm mũi tên: Hà Nội mở ra', '"Đến Nhân viên": mở hết'])
S3.add('Chọn nhân viên có tìm theo tên không dấu', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW + ['Mở ô chọn nhân viên dòng Hà Nội, gõ "duc dong".'], 'Từ khoá: duc dong',
       ['Ra "%s"' % NV3, 'Nhãn mỗi lựa chọn dạng "Tên - Mã"'])
S3.add('Chọn nhân viên tìm theo mã', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Mở ô chọn nhân viên, gõ "11010032".'], 'Từ khoá: 11010032', ['Ra "%s"' % NV2, 'Chọn xong ô hiện đúng nhãn đó'])
S3.add('Danh sách nhân viên theo công ty', 'P1', [ACC_A, TARGET, FREE, '%s thuộc phòng KD2 cùng công ty TPE; nhân viên Y thuộc công ty TPSG; nhân viên Z đã nghỉ việc.' % NV4],
       OPEN_NEW + ['Mở ô chọn nhân viên, lần lượt tìm Tuấn, Y, Z.'], '—',
       ['Có "%s" (nhân viên khác phòng nhưng cùng công ty)' % NV4, 'Không có Y (công ty khác), không có Z (đã nghỉ việc)'])
S3.add('Nhân viên đã giao trong tỉnh bị loại khỏi ô chọn', 'P0', [ACC_A, TARGET, FREE],
       OPEN_NEW + ['Hà Nội dòng 1 chọn %s.' % NV1, 'Bấm "Thêm Nhân Viên" ở Hà Nội, mở ô chọn của dòng mới.'], '—',
       ['Dòng mới KHÔNG có "%s"' % NV1, 'Không chọn trùng được 1 nhân viên trong cùng 1 tỉnh',
        'Lưu ý: bản hiện tại bỏ hẳn nhân viên khỏi danh sách (bản mẫu ghi hiện mờ "Đã giao tại tỉnh này")'])
S3.add('Cùng nhân viên ở tỉnh khác được chọn', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Hà Nội chọn %s.' % NV1, 'Hải Phòng chọn %s.' % NV1], '—',
       ['Hải Phòng chọn được %s' % NV1, 'Nhãn TỔNG đếm "2 Tỉnh/TP · 1 nhân viên" (1 người ở 2 tỉnh tính 1)'])
S3.add('Bỏ chọn nhân viên', 'P2', [ACC_A, TARGET, FREE], OPEN_NEW + ['Hà Nội chọn %s.' % NV1, 'Bấm dấu x trong ô chọn.'], '—',
       ['Ô về "Chọn nhân viên"', '%s quay lại danh sách chọn của các dòng khác trong Hà Nội' % NV1])
S3.add('Thêm dòng nhân viên', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Bấm "Thêm Nhân Viên" ở Hà Nội 2 lần.'], '—',
       ['Hà Nội có 3 dòng STT 1, 2, 3', 'Liên kết "Thêm Nhân Viên" chỉ nằm dưới dòng cuối của tỉnh'])
S3.add('Xoá dòng có số thì hỏi', 'P0', [ACC_A, TARGET, FREE],
       OPEN_NEW + ['Hà Nội: dòng 1 chọn %s nhập số, thêm dòng 2.' % NV1, 'Bấm biểu tượng thùng rác dòng 1, chọn Hủy.', 'Bấm lại, chọn Xoá.'],
       'Khách hãng Hàng hóa SL 6 / Doanh số 3,000,000,000',
       ['Hộp "Xoá dòng nhân viên", nội dung "Xoá dòng %s tại Hà Nội? Số liệu của dòng sẽ mất.", nút Hủy / Xoá' % NV1,
        'Hủy: dòng còn nguyên', 'Xoá: dòng mất, tổng Hà Nội và dòng TỔNG tính lại'])
S3.add('Xoá dòng chưa có số không hỏi', 'P2', [ACC_A, TARGET, FREE], OPEN_NEW + ['Thêm 1 dòng ở Hà Nội, chọn %s, không nhập số.' % NV2, 'Bấm thùng rác dòng đó.'], '—',
       ['Dòng mất ngay, không hiện hộp xác nhận'])
S3.add('Dòng cuối của tỉnh chỉ làm trống', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Hải Phòng (1 dòng) chọn %s, nhập số.' % NV1, 'Bấm thùng rác, chọn Xoá.'], '—',
       ['Hải Phòng vẫn còn 1 dòng trống (ô "Chọn nhân viên", các ô số trống)', 'Tỉnh Hải Phòng không biến mất khỏi bảng'])
S3.add('Lưu phiếu đầy đủ hợp lệ', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW + ['Nhập 3 dòng theo Test Data.', 'Bấm Lưu.'], FILL,
       ['Báo "Đã lưu TPE_CTKDNV_2027.xxxxx", quay về danh sách', 'Phiếu mới ở đầu danh sách: Phòng ban Kinh doanh 1, Năm 2027, Trạng thái Đang tạo',
        'Số phiếu dạng <mã công ty>_CTKDNV_<năm>.<số thứ tự 5 chữ số>'])
S3.add('Tổng tỉnh, dòng TỔNG và cột Tổng cộng tự tính', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW + ['Nhập 3 dòng theo Test Data (chưa lưu).'], FILL,
       ['Dòng Hà Nội "Hà Nội (2 nhân viên)": Khách hãng Hàng hóa 10 / 5,000,000,000, Dịch vụ 2 / 600,000,000, Khách khác Hàng hóa 2 / 500,000,000',
        'Cột Tổng cộng dòng %s ở Hà Nội: Hàng hóa 8 / 3,500,000,000' % NV1,
        'Dòng TỔNG "2 Tỉnh/TP · 2 nhân viên": Khách hãng Hàng hóa 15 / 6,500,000,000, Dịch vụ 2 / 600,000,000, Khách khác Hàng hóa 2 / 500,000,000, Tổng cộng Hàng hóa 17 / 7,000,000,000',
        'Số hiện dấu phẩy ngăn nghìn dạng 1,234,567'])
S3.add('Giao vượt chỉ tiêu tô cam kèm chênh lệch', 'P0', [ACC_A, TARGET, FREE],
       OPEN_NEW + ['Hà Nội: %s Khách hãng Hàng hóa 6 / 3,000,000,000; %s Khách hãng Hàng hóa 5 / 2,500,000,000.' % (NV1, NV2), 'Rê chuột vào ô Doanh số Khách hãng Hàng hóa dòng Hà Nội.'], '—',
       ['Dòng Hà Nội: ô SL khách (11 > 10) và Doanh số (5,500,000,000 > 5,000,000,000) Khách hãng Hàng hóa tô cam',
        'Rê chuột hiện "Vượt chỉ tiêu giao 500,000,000"; ô SL hiện "Vượt chỉ tiêu giao 1"',
        'Cột Tổng cộng Hàng hóa (11 / 5,500,000,000 so với chỉ tiêu 13 / 5,800,000,000) KHÔNG tô cam; dòng TỔNG không tô cam vì chưa vượt chỉ tiêu cả phòng',
        'Bằng đúng chỉ tiêu thì không tô cam'])
S3.add('Vượt chỉ tiêu vẫn Lưu được', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW + ['Nhập như ca trên (Hà Nội vượt chỉ tiêu).', 'Bấm Lưu.'], '—',
       ['Lưu được, không có cảnh báo chặn', 'Báo "Đã lưu ...", về danh sách'])
S3.add('Ô số không nhận dấu âm và chữ', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Chọn %s ở Hà Nội, gõ lần lượt vào ô SL khách: -5, abc.' % NV1], '-5; abc',
       ['Dấu "-" và chữ không gõ được vào ô', 'Ô chỉ còn số 5 (với -5) hoặc để trống (với abc)'])
S3.add('Ô số không có phần thập phân', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Gõ "2.5" vào ô SL khách dòng Hà Nội.'], '2.5',
       ['Ô không nhận dấu chấm thập phân, chỉ nhận số nguyên',
        'Lưu ý: dấu chấm bị bỏ nên ô hiện 25 — QA kiểm lại con số sau khi gõ (ghi nhận nếu nghiệp vụ muốn báo đỏ thay vì bỏ dấu)'])
S3.add('Dán số có dấu phẩy hoặc dấu chấm ngăn nghìn', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Dán "1,234" vào ô SL khách, dán "1.234" vào ô SL khách khác.'], '1,234 ; 1.234',
       ['Cả 2 ô hiện 1,234', 'Giá trị lưu là 1234'])
S3.add('Ô số vượt 13 chữ số', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Chọn %s ở Hà Nội, gõ 14 chữ số vào ô Doanh số Khách hãng Hàng hóa, SL khách 1.' % NV1, 'Bấm Lưu.'],
       '12345678901234', ['Báo %s' % CHECK, 'Chữ đỏ "Giá trị vượt quá giới hạn cho phép" ngay dưới ô Doanh số đó', 'Không lưu; số đã gõ còn nguyên, không bị tự cắt bớt'])
S3.add('Đúng 13 chữ số thì lưu được', 'P2', [ACC_A, TARGET, FREE], OPEN_NEW + ['Gõ 13 chữ số vào ô Doanh số, SL khách 1.', 'Bấm Lưu.'], '9999999999999',
       ['Lưu được, ô hiện 9,999,999,999,999'])
S3.add('Có số mà chưa chọn nhân viên', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW + ['Dòng Hà Nội không chọn nhân viên, nhập SL khách 6.', 'Bấm Lưu.'], 'Khách hãng Hàng hóa SL khách: 6',
       ['Báo %s' % CHECK, 'Ô chọn nhân viên dòng đó viền đỏ, chữ đỏ %s ngay dưới' % REQ, 'Không lưu, số đã nhập còn nguyên'])
S3.add('Chưa chọn Phòng ban', 'P0', 'Tài khoản A3 như trên (ô Phòng ban trống).', OPEN_NEW + ['Bấm Lưu.'], '—',
       ['Ô Phòng ban viền đỏ, chữ đỏ %s' % REQ, 'Báo %s, không tạo phiếu' % CHECK])
S3.add('Phòng chưa có chỉ tiêu được duyệt', 'P0', ['Tài khoản G (chọn được mọi phòng của công ty).', TARGET, 'Phòng KD2 có chỉ tiêu 2027, không có chỉ tiêu năm 2028.'],
       [MENU, 'Bấm Tạo mới, chọn Năm 2027, Phòng ban Kinh doanh 2.', 'Đổi Năm sang Năm 2028.', 'Bấm Lưu.'], 'Năm 2028',
       ['Ô Phòng ban tự xoá (Kinh doanh 2 không có trong danh sách năm 2028)', 'Khối Chi tiết hiện "Chọn phòng ban để nạp chỉ tiêu"', 'Bấm Lưu: Phòng ban báo %s' % REQ])
S3.add('Lỗi đỏ biến mất khi sửa đúng', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Tạo lỗi có số mà chưa chọn nhân viên, bấm Lưu.', 'Chọn %s ở dòng đó.' % NV1], '—',
       ['Chữ đỏ dưới ô nhân viên mất ngay khi chọn', 'Bấm Lưu lại thì lưu được'])
S3.add('Lỗi ở tỉnh đang thu gọn hoặc ở thẻ khác', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Tạo lỗi ở Hải Phòng (có số, chưa chọn nhân viên).', 'Thu gọn Hải Phòng, chuyển sang thẻ Tổng hợp.', 'Bấm Lưu.'], '—',
       ['Thẻ "Giao chỉ tiêu" có dấu báo lỗi; form tự quay về thẻ này', 'Hải Phòng tự mở ra, cuộn tới ô lỗi đầu tiên'])
S3.add('Dòng trống bị bỏ khi lưu', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Nhập 1 dòng hợp lệ ở Hà Nội, để Hải Phòng và 1 dòng thêm ở Hà Nội trống.', 'Bấm Lưu, mở Xem phiếu.'], '—',
       ['Lưu được, không báo lỗi cho dòng trống', 'Màn Xem: Hà Nội 1 nhân viên; Hải Phòng vẫn hiện dòng tỉnh + Chỉ tiêu giao, 0 nhân viên'])
S3.add('Chỉ chọn nhân viên, không nhập số', 'P2', [ACC_A, TARGET, FREE], OPEN_NEW + ['Hà Nội chọn %s, không nhập số.' % NV1, 'Bấm Lưu.'], '—',
       ['Lưu được (Đang tạo), dòng nhân viên được giữ với số trống', 'Chỉ bị chặn khi gửi duyệt vì doanh số bằng 0 (xem nhóm Gửi duyệt)'])
S3.add('Trùng phiếu của phòng trong năm', 'P0', [ACC_A, TARGET, 'Phòng KD1 đã có phiếu %s năm 2027 Đang tạo.' % M], OPEN_NEW + ['Nhập 1 dòng hợp lệ, bấm Lưu.'], '—',
       ['Ô Phòng ban báo đỏ "Phòng đã có phiếu %s (Đang tạo) cho năm 2027"' % M, 'Không tạo phiếu mới'])
S3.add('Phiếu Hủy không tính trùng', 'P1', [ACC_A, TARGET, 'Phiếu %s đã Hủy, KD1 không còn phiếu 2027 nào khác.' % M], OPEN_NEW + ['Nhập 1 dòng hợp lệ, bấm Lưu.'], '—',
       ['Lưu được phiếu mới cho KD1 năm 2027'])
S3.add('Đổi Năm khi đã nhập thì hỏi', 'P0', [ACC_A, TARGET, FREE, 'KD1 có chỉ tiêu cả năm 2026.'], OPEN_NEW + ['Chọn %s ở Hà Nội, nhập số.' % NV1, 'Chọn Năm 2026, bấm Hủy.', 'Chọn Năm 2026 lần nữa, bấm Đổi.'], '—',
       ['Hộp "Đổi năm", nội dung "Đổi năm? Dữ liệu giao nhân viên đã nhập sẽ mất.", nút Hủy / Đổi',
        'Hủy: ô Năm về Năm 2027, dữ liệu còn', 'Đổi: bảng nạp lại theo chỉ tiêu năm 2026, các dòng nhân viên trống'])
S3.add('Đổi Phòng ban khi đã nhập thì hỏi', 'P0', ['Tài khoản G.', TARGET, FREE], [MENU, 'Bấm Tạo mới, Năm 2027, Phòng ban Kinh doanh 1, nhập 1 dòng.', 'Chọn Phòng ban Kinh doanh 2, bấm Đổi.'], '—',
       ['Hộp "Đổi phòng ban", nội dung "Đổi phòng? Dữ liệu giao nhân viên đã nhập sẽ mất.", nút Hủy / Đổi',
        'Đổi: bảng nạp chỉ tiêu KD2 (Đà Nẵng), dữ liệu KD1 mất'])
S3.add('Đổi Năm / Phòng khi chưa nhập không hỏi', 'P2', [ACC_A, TARGET], OPEN_NEW + ['Chưa chọn nhân viên, chưa nhập số, đổi Năm 2026.'], '—',
       ['Đổi ngay, không hiện hộp hỏi'])
S3.add('Thẻ Tổng hợp theo nhân viên', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW + ['Nhập 3 dòng theo Test Data.', 'Bấm thẻ "Tổng hợp".'], FILL,
       ['Cột: STT, Nhân viên, Tổng doanh số, Tỉnh/TP, Doanh số theo tỉnh',
        'Dòng đầu: "Kinh doanh 1", Tổng doanh số 7,600,000,000',
        '1 %s: Tổng 5,000,000,000; Hà Nội 3,500,000,000, Hải Phòng 1,500,000,000' % NV1,
        '2 %s: Tổng 2,600,000,000; Hà Nội 2,600,000,000' % NV2, 'Doanh số = Doanh số Hàng hóa + Dịch vụ của cả Khách hãng và Khách khác'])
S3.add('Thẻ Tổng hợp khi chưa giao ai', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Bấm thẻ "Tổng hợp".'], '—',
       ['Dòng đầu "Kinh doanh 1", Tổng doanh số 0', 'Dòng "Chưa giao chỉ tiêu cho nhân viên nào"'])
S3.add('Dòng TỔNG và Chỉ tiêu giao không lệch khi cuộn', 'P1', [ACC_A, 'Phòng KD1 có chỉ tiêu 2027 ở 12 Tỉnh/TP, mỗi tỉnh 3 nhân viên.'],
       OPEN_NEW + ['Cuộn bảng xuống cuối rồi cuộn ngang sang cột Tổng cộng.', 'Thu nhỏ / phóng to trình duyệt rồi cuộn lại.'], '—',
       ['Tiêu đề 3 tầng, dòng TỔNG và dòng Chỉ tiêu giao đứng yên ở đầu bảng, nằm khít dưới tầng "SL khách / Doanh số"',
        'Không có khe hở để dòng bên dưới lộ ra, dòng TỔNG không đè lên tiêu đề, viền cam (nếu có) vẫn hiện',
        'Cột STT và cột cây đứng yên khi cuộn ngang; có thanh cuộn ngang ở cả trên và dưới bảng'])
S3.add('Quay lại khi chưa nhập gì', 'P1', [ACC_A, TARGET], [MENU, 'Bấm Tạo mới.', 'Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi'])
S3.add('Quay lại khi đã nhập', 'P0', [ACC_A, TARGET], OPEN_NEW + ['Nhập 1 dòng Hà Nội.', 'Bấm Quay lại, chọn Ở lại.', 'Bấm Quay lại, chọn Thoát.'], '—',
       ['Hiện %s' % UNSAVED, 'Ở lại: dữ liệu còn nguyên', 'Thoát: về danh sách, không có phiếu mới'])
S3.add('Rời trang bằng menu khi đã nhập', 'P1', [ACC_A, TARGET], OPEN_NEW + ['Nhập 1 dòng.', 'Bấm 1 mục menu khác.'], '—', ['Hiện hộp "Thông tin chưa lưu" như trên'])
S3.add('Nhập rồi xoá hết', 'P2', [ACC_A, TARGET], OPEN_NEW + ['Chọn %s, nhập SL khách rồi xoá số và bỏ chọn nhân viên.' % NV1, 'Bấm Quay lại.'], '—',
       ['Không hiện hộp hỏi (form về như lúc mới nạp chỉ tiêu)'])
S3.add('Bấm Lưu liên tục', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Nhập 1 dòng hợp lệ.', 'Bấm Lưu 3 lần thật nhanh.'], '—',
       ['Chỉ tạo 1 phiếu'])
S3.add('Hai thẻ cùng lập phiếu cho 1 phòng', 'P1', [ACC_A, TARGET, FREE], ['Mở 2 thẻ, mỗi thẻ: %s' % MENU, 'Cả 2 thẻ Tạo mới Năm 2027 Kinh doanh 1, nhập 1 dòng.', 'Thẻ 1 bấm Lưu, sau đó thẻ 2 bấm Lưu.'], '—',
       ['Thẻ 1 lưu được', 'Thẻ 2: ô Phòng ban báo "Phòng đã có phiếu <số phiếu thẻ 1> (Đang tạo) cho năm 2027"', 'Chỉ có 1 phiếu KD1 năm 2027'])

# ============================================================================ IV. CHỈNH SỬA
S4 = Sec()
S4.add('Mở Sửa từ danh sách, dữ liệu điền đúng', 'P0', [ACC_A, PLAN_M], [MENU, 'Bấm biểu tượng Sửa (bút chì) ở dòng %s.' % M], '—',
       ['Tiêu đề "Sửa %s: %s"' % (ten, M), 'Số phiếu %s (khoá), Năm 2027, Phòng ban Kinh doanh 1' % M,
        'Hà Nội 2 dòng (%s, %s), Hải Phòng 1 dòng (%s) đúng số đã lưu; ô bằng 0 để trống' % (NV1, NV2, NV1), 'Chân trang: Lưu, Lưu và gửi, Quay lại'])
S4.add('Mở Sửa từ màn Chi tiết', 'P1', [ACC_A, PLAN_M], [MENU, 'Bấm số phiếu %s.' % M, 'Bấm Sửa.'], '—', ['Mở màn Sửa của %s' % M])
S4.add('Sửa số một dòng', 'P0', [ACC_A, PLAN_M], [MENU, 'Mở Sửa %s.' % M, 'Đổi Doanh số Khách hãng Hàng hóa dòng %s ở Hà Nội từ 3,000,000,000 thành 3,500,000,000.' % NV1, 'Bấm Lưu.'], '—',
       ['Báo "Đã lưu %s", về danh sách' % M, 'Mở Xem: tổng Hà Nội Khách hãng Hàng hóa 5,500,000,000 (tô cam vì vượt chỉ tiêu 5,000,000,000)', 'Trạng thái vẫn Đang tạo'])
S4.add('Thêm nhân viên mới và xoá dòng cũ', 'P1', [ACC_A, PLAN_M], [MENU, 'Mở Sửa %s.' % M, 'Hải Phòng: xoá dòng %s (xác nhận Xoá), chọn %s nhập Khách hãng Hàng hóa 5 / 1,500,000,000.' % (NV1, NV3), 'Bấm Lưu, mở Xem.'], '—',
       ['Hải Phòng chỉ còn %s' % NV3, 'Thẻ Tổng hợp: %s còn Hà Nội 3,500,000,000; có thêm %s' % (NV1, NV3)])
S4.add('Đổi Năm khi sửa thì số phiếu đổi theo năm', 'P1', [ACC_A, PLAN_M, 'KD1 có chỉ tiêu Đã duyệt năm 2028, chưa có phiếu 2028.'],
       [MENU, 'Mở Sửa %s.' % M, 'Chọn Năm 2028, bấm Đổi, nhập 1 dòng hợp lệ.', 'Bấm Lưu.'], 'Năm 2028',
       ['Lưu được', 'Số phiếu đổi thành TPE_CTKDNV_2028.00071 (giữ số thứ tự, đổi năm)'])
S4.add('Bỏ chọn nhân viên mà còn số khi sửa', 'P0', [ACC_A, PLAN_M], [MENU, 'Mở Sửa %s.' % M, 'Bấm x bỏ chọn %s ở Hà Nội (giữ số).' % NV2, 'Bấm Lưu.'], '—',
       ['Ô nhân viên đỏ %s, báo %s' % (REQ, CHECK), 'Không lưu, phiếu giữ số cũ'])
S4.add('Nhập vượt giới hạn khi sửa', 'P1', [ACC_A, PLAN_M], [MENU, 'Mở Sửa %s.' % M, 'Gõ 14 chữ số vào 1 ô Doanh số, bấm Lưu.'], '12345678901234',
       ['Chữ đỏ "Giá trị vượt quá giới hạn cho phép" dưới ô', 'Không lưu'])
S4.add('Quay lại khi đã đổi', 'P1', [ACC_A, PLAN_M], [MENU, 'Mở Sửa %s, đổi 1 số.' % M, 'Bấm Quay lại, chọn Ở lại.', 'Bấm Quay lại, chọn Thoát.'], '—',
       ['Hiện %s' % UNSAVED, 'Thoát: phiếu không đổi'])
S4.add('Mở Sửa không đổi gì / đổi rồi trả về ban đầu', 'P2', [ACC_A, PLAN_M], [MENU, 'Mở Sửa %s, bấm Quay lại.' % M, 'Mở lại, đổi 1 số rồi gõ lại số cũ, bấm Quay lại.'], '—',
       ['Cả 2 lần về danh sách ngay, không hỏi'])
S4.add('Mở Sửa phiếu không còn Đang tạo', 'P0', [ACC_E, PEND], ['Mở lại màn Sửa của %s từ trang đã đánh dấu trong trình duyệt.' % P2], '—',
       ['Tự chuyển sang màn Chi tiết của %s, không có ô nhập' % P2])
S4.add('Phiếu vừa được gửi duyệt ở thẻ khác', 'P0', [ACC_A, PLAN_M], ['Thẻ 1: mở Sửa %s.' % M, 'Thẻ 2: gửi duyệt %s.' % M, 'Thẻ 1: đổi số, bấm Lưu.'], '—',
       ['Thẻ 1 báo %s' % LOCKED, 'Phiếu giữ nguyên số liệu lúc gửi'])
S4.add('Phiếu bị Hủy ở thẻ khác', 'P1', [ACC_A, PLAN_M], ['Thẻ 1: mở Sửa %s.' % M, 'Thẻ 2: Hủy phiếu %s.' % M, 'Thẻ 1: bấm Lưu.'], '—', ['Thẻ 1 báo %s' % LOCKED])
S4.add('Hai thẻ cùng sửa', 'P2', [ACC_A, PLAN_M], ['Thẻ 1 và 2 cùng mở Sửa %s.' % M, 'Thẻ 1 đổi số Hà Nội, Lưu.', 'Thẻ 2 đổi số Hải Phòng, Lưu.'], '—',
       ['Lưu sau ghi đè lưu trước: Hà Nội về số cũ, Hải Phòng theo thẻ 2 (ghi nhận nếu nghiệp vụ cần chặn)'])
S4.add('Mở Sửa lấy chỉ tiêu phòng mới nhất', 'P0',
       [ACC_A, PLAN_M, 'Sau khi lập M, phiếu phòng ban %s được Hủy duyệt, sửa chỉ tiêu Hà Nội Khách hãng Hàng hóa thành 12 / 6,000,000,000, thêm Quảng Ninh 2 / 700,000,000, rồi Đã duyệt lại.' % PB],
       [MENU, 'Mở Sửa %s.' % M], '—',
       ['Dòng Chỉ tiêu giao Hà Nội hiện 12 / 6,000,000,000 (chỉ tiêu mới)', 'Có thêm tỉnh Quảng Ninh với 1 dòng nhân viên trống',
        'Số đã giao cho nhân viên giữ nguyên'])
S4.add('Phiếu bị từ chối về Đang tạo sửa được', 'P0', [ACC_E, 'Phiếu %s bị B từ chối, lý do "Thiếu Đà Nẵng dịch vụ".' % P2], [MENU, 'Mở Xem %s.' % P2, 'Bấm Sửa, sửa 1 số, bấm Lưu.'], '—',
       ['Màn Xem có dòng "Lý do từ chối: Thiếu Đà Nẵng dịch vụ"', 'Có nút Sửa, Gửi duyệt, Hủy phiếu', 'Sửa và lưu được'])

# ============================================================================ V. GỬI DUYỆT
S5 = Sec()
S5.add('Điều kiện hiện nút Gửi duyệt', 'P0', [ACC_A, DATA], [MENU, 'Mở ba chấm dòng %s, %s.' % (M, P3), 'Mở Xem %s.' % M], '—',
       ['Chỉ phiếu Đang tạo do chính mình lập (và mình có quyền %s) có Gửi duyệt, ở dòng lẫn chân màn Chi tiết' % Q_CRE, '%s (Đã duyệt) không có' % P3])
S5.add('Hộp xác nhận gửi duyệt', 'P1', [ACC_A, PLAN_M], [MENU, 'Ở dòng %s bấm ba chấm > Gửi duyệt.' % M], '—',
       ['Hộp "Gửi duyệt", nội dung "Gửi duyệt phiếu %s?", nút Hủy / Gửi duyệt' % M])
S5.add('Gửi duyệt thành công', 'P0', [ACC_A, PLAN_M, ACC_B], [MENU, 'Ở dòng %s bấm Gửi duyệt > Gửi duyệt.' % M], '—',
       ['Báo "Đã gửi duyệt %s"' % M, 'Trạng thái Chờ duyệt (màu cam)', 'Hết biểu tượng Sửa và mục Gửi duyệt; còn Hủy phiếu', 'B thấy %s ở lối vào "Giao chỉ tiêu NV chờ duyệt"' % M])
S5.add('Bấm Hủy ở hộp xác nhận', 'P1', [ACC_A, PLAN_M], [MENU, 'Bấm Gửi duyệt ở dòng %s, chọn Hủy.' % M], '—', ['Phiếu vẫn Đang tạo, không có thông báo nào'])
S5.add('Lưu và gửi từ form Tạo mới', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW + ['Nhập 3 dòng theo Test Data.', 'Bấm Lưu và gửi.'], FILL,
       ['Báo "Đã gửi duyệt TPE_CTKDNV_2027.xxxxx", về danh sách', 'Phiếu mới ở trạng thái Chờ duyệt'])
S5.add('Lưu và gửi từ form Sửa', 'P0', [ACC_A, PLAN_M], [MENU, 'Mở Sửa %s, đổi 1 số.' % M, 'Bấm Lưu và gửi.'], '—', ['Lưu số mới và chuyển Chờ duyệt cùng lúc', 'Về danh sách'])
S5.add('Kiểm cặp: có SL khách mà thiếu Doanh số', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW + ['Hà Nội chọn %s, Khách hãng Hàng hóa SL 6, bỏ trống Doanh số.' % NV1, 'Bấm Lưu và gửi.'], 'SL khách 6; Doanh số trống',
       ['Ô Doanh số Khách hãng Hàng hóa dòng đó đỏ %s' % NEED_DS, 'Báo %s, không lưu, không gửi' % CHECK])
S5.add('Kiểm cặp: có Doanh số mà thiếu SL khách', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW + ['Hà Nội chọn %s, Khách khác Dịch vụ Doanh số 300,000,000, bỏ trống SL khách.' % NV1, 'Bấm Lưu và gửi.'], 'Doanh số 300,000,000; SL khách trống',
       ['Ô SL khách Khách khác Dịch vụ đỏ %s' % NEED_SL, 'Không gửi'])
S5.add('Lưu thường không kiểm cặp', 'P1', [ACC_A, TARGET, FREE], OPEN_NEW + ['Nhập như ca trên (thiếu Doanh số).', 'Bấm Lưu.'], '—',
       ['Lưu được (Đang tạo), không báo đỏ cặp SL / Doanh số'])
S5.add('Gửi khi doanh số bằng 0', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW + ['Hà Nội chọn %s, không nhập số nào.' % NV1, 'Bấm Lưu và gửi.', 'Bấm Lưu; ở danh sách bấm Gửi duyệt phiếu vừa lưu.'], '—',
       ['Lưu và gửi: báo %s, không tạo phiếu' % NO_REV, 'Lưu thường được (Đang tạo)', 'Gửi duyệt ở danh sách: báo %s, phiếu vẫn Đang tạo' % NO_REV])
S5.add('Giao vượt chỉ tiêu vẫn gửi được', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW + ['Hà Nội giao tổng Khách hãng Hàng hóa 11 / 5,500,000,000 (vượt chỉ tiêu).', 'Bấm Lưu và gửi.'], '—',
       ['Gửi được, phiếu Chờ duyệt', 'Không có câu chặn "chưa đạt / vượt chỉ tiêu"'])
S5.add('Công ty chưa có ai được quyền Duyệt', 'P1', 'Tài khoản K: công ty TPHN (chưa Vai trò nào có quyền %s), có phiếu Đang tạo hợp lệ.' % Q_APP,
       [MENU, 'Gửi duyệt phiếu đó.'], '—', ['Báo "Chưa phân quyền người duyệt"', 'Phiếu vẫn Đang tạo'])
S5.add('Thông báo tới người có quyền Duyệt', 'P0', [ACC_A, PLAN_M, ACC_B, 'Tài khoản B2: công ty TPE, cũng có quyền %s.' % Q_APP], ['A gửi duyệt %s.' % M, 'B mở chuông thông báo, bấm vào thông báo mới.'], '—',
       ['B và B2 nhận thông báo "[CTKDNV] Gửi duyệt: %s"' % M, 'A không nhận', 'Bấm thông báo mở màn Chi tiết %s' % M])
S5.add('Gửi phiếu đã gửi ở thẻ khác', 'P1', [ACC_A, PLAN_M], ['Thẻ 1 mở Xem %s.' % M, 'Thẻ 2 gửi duyệt %s.' % M, 'Thẻ 1 bấm Gửi duyệt > Gửi duyệt.'], '—',
       ['Thẻ 1 báo %s' % NOPERM, 'Trạng thái giữ Chờ duyệt, không gửi thông báo lần 2'])
S5.add('Gửi lại sau khi bị từ chối', 'P1', [ACC_E, 'Phiếu %s bị từ chối về Đang tạo, lý do "Thiếu Đà Nẵng dịch vụ".' % P2], [MENU, 'Gửi duyệt %s.' % P2, 'Mở Xem %s.' % P2], '—',
       ['Về Chờ duyệt', 'Dòng "Lý do từ chối" không còn hiện'])

# ============================================================================ VI. DUYỆT PHIẾU + HỦY DUYỆT
S6 = Sec()
S6.add('Điều kiện hiện nút Duyệt', 'P0', [ACC_B, DATA], OPEN_P2_B, '—',
       ['Màn Chi tiết %s có nút Duyệt, Từ chối' % P2, 'Ở danh sách, mục Duyệt trong ba chấm chỉ mở màn Chi tiết'])
S6.add('Hộp xác nhận duyệt', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm Duyệt.'], '—',
       ['Hộp "Duyệt phiếu", nội dung "Duyệt phiếu %s? Phiếu đã duyệt không sửa được.", nút Hủy / Duyệt' % P2])
S6.add('Duyệt thành công', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Bấm Duyệt > Duyệt.'], '—',
       ['Báo "Đã duyệt %s"' % P2, 'Trạng thái Đã duyệt (xanh lá); Người duyệt "Đỗ Thị Lan", Ngày duyệt là hôm nay',
        'Phiếu rời lối vào chờ duyệt', 'Theo quy tắc chung: xong thao tác quay về danh sách (lối vào đang đứng)'])
S6.add('Bấm Hủy ở hộp duyệt', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm Duyệt, chọn Hủy.'], '—', ['Phiếu vẫn Chờ duyệt, không có thông báo'])
S6.add('Thông báo người lập khi được duyệt', 'P0', [ACC_E, PEND], ['B duyệt %s.' % P2, 'E mở chuông thông báo, bấm vào thông báo.'], '—',
       ['E nhận "[CTKDNV] Đã duyệt: %s"' % P2, 'Bấm thông báo mở màn Chi tiết %s, trạng thái Đã duyệt' % P2])
S6.add('Chỉ quyền Duyệt theo phòng ban không duyệt được phiếu nhân viên', 'P0',
       ['Tài khoản C: công ty TPE, chỉ có quyền %s.' % Q_APP_PB, PEND], [MENU, 'Vào nhóm "Phê Duyệt" > "Kế hoạch & chỉ tiêu".'], '—',
       ['Không có mục "Giao chỉ tiêu NV chờ duyệt" (chỉ có "Giao chỉ tiêu chờ duyệt" của phiếu phòng ban)',
        'Danh sách phiếu nhân viên của C không có %s, không thấy nút Duyệt' % P2])
S6.add('Có quyền Duyệt nhưng khác công ty', 'P0', ['Tài khoản H: công ty TPSG, có quyền %s.' % Q_APP, PEND], [MENU_CD], '—',
       ['Không thấy %s (công ty TPE)' % P2, 'Chỉ thấy phiếu Chờ duyệt của TPSG'])
S6.add('Không duyệt lại phiếu đã xử lý', 'P0', [ACC_B, 'Tài khoản B2: công ty TPE, có quyền %s.' % Q_APP, PEND], ['B mở Chi tiết %s.' % P2, 'B2 duyệt %s.' % P2, 'B bấm Duyệt > Duyệt.'], '—',
       ['B báo %s' % NOPERM, 'Phiếu giữ Đã duyệt do B2 duyệt, Người duyệt không bị ghi đè'])
S6.add('Người lập có quyền Duyệt tự duyệt phiếu mình', 'P2', 'Tài khoản E2: có cả quyền %s và %s, đã gửi duyệt phiếu của mình.' % (Q_CRE, Q_APP), [MENU_CD, 'Mở phiếu của E2.'], '—',
       ['Có nút Duyệt (quyền Duyệt không loại phiếu mình lập)', 'Ghi nhận nếu nghiệp vụ cần chặn tự duyệt'])
S6.add('Điều kiện hiện nút Hủy duyệt', 'P0', [ACC_B, APPR], [MENU, 'Mở ba chấm dòng %s.' % P3, 'Mở Chi tiết %s.' % P3], '—',
       ['Có Hủy duyệt ở ba chấm và ở chân màn Chi tiết (màu đỏ)', 'A (người lập, không có quyền Duyệt) xem %s không có Hủy duyệt' % P3])
S6.add('Hủy duyệt thành công', 'P0', [ACC_B, APPR], [MENU, 'Mở Chi tiết %s, bấm Hủy duyệt.' % P3, 'Bấm Hủy duyệt ở hộp xác nhận.'], '—',
       ['Hộp "Hủy duyệt phiếu", nội dung "Hủy duyệt phiếu %s? Phiếu trở về Đang tạo để người lập sửa.", nút Hủy / Hủy duyệt' % P3,
        'Báo "Đã hủy duyệt %s"' % P3, 'Phiếu về Đang tạo, Người duyệt / Ngày duyệt trống', 'A nhận thông báo "[CTKDNV] Hủy duyệt: %s", sửa được phiếu' % P3])
S6.add('Sau Hủy duyệt người duyệt không còn thấy phiếu', 'P1', [ACC_B, 'B vừa Hủy duyệt %s.' % P3], [MENU], '—',
       ['%s biến mất khỏi danh sách của B (phiếu Đang tạo chỉ người lập thấy)' % P3])
S6.add('Người có quyền Duyệt khác hủy duyệt được', 'P1', ['Tài khoản B2 (quyền Duyệt, công ty TPE, không phải người đã duyệt).', APPR], [MENU, 'Tìm %s.' % P3], '—',
       ['Lưu ý: B2 không có quyền Xem nên danh sách KHÔNG có %s (chỉ thấy phiếu mình duyệt / phiếu Chờ duyệt)' % P3,
        'Cấp thêm %s mức Công ty cho B2 thì thấy %s và có Hủy duyệt' % (Q_VIEW, P3)])
S6.add('Hủy duyệt khi phiếu vừa bị hủy duyệt ở thẻ khác', 'P2', [ACC_B, APPR], ['Thẻ 1 mở Chi tiết %s.' % P3, 'Thẻ 2 Hủy duyệt %s.' % P3, 'Thẻ 1 bấm Hủy duyệt > Hủy duyệt.'], '—',
       ['Thẻ 1 bị từ chối (báo không có quyền hoặc %s), phiếu giữ Đang tạo' % CHANGED])

# ============================================================================ VII. KHÔNG DUYỆT (TỪ CHỐI)
S7 = Sec()
S7.add('Điều kiện hiện nút Từ chối', 'P0', [ACC_B, DATA], OPEN_P2_B + ['Mở Chi tiết %s.' % P3], '—',
       ['%s (Chờ duyệt) có nút Từ chối (đỏ)' % P2, '%s (Đã duyệt) không có Từ chối' % P3, 'Dòng danh sách không có Từ chối, chỉ từ chối ở màn Chi tiết'])
S7.add('Giao diện hộp Từ chối', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối.'], '—',
       ['Hộp "Từ chối phiếu", nội dung "Từ chối phiếu %s? Phiếu trở về Đang tạo để người lập sửa."' % P2,
        'Ô "Lý do" có dấu * đỏ, gợi ý "Nhập lý do từ chối"', 'Nút Hủy / Từ chối'])
S7.add('Bỏ trống lý do', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối, để trống Lý do, bấm Từ chối.'], '—',
       ['Chữ đỏ %s dưới ô Lý do, hộp không đóng' % REQ, 'Phiếu vẫn Chờ duyệt'])
S7.add('Lý do chỉ có khoảng trắng', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối, gõ 3 dấu cách, bấm Từ chối.'], '3 dấu cách', ['Bị chặn như bỏ trống'])
S7.add('Lý do vượt 1000 ký tự', 'P2', [ACC_B, PEND], OPEN_P2_B + ['Gõ 1001 ký tự, bấm Từ chối.', 'Sửa còn 1000 ký tự, từ chối lại.'], '1001 rồi 1000 ký tự',
       ['1001 ký tự: báo "Vui lòng nhập tối đa 1000 ký tự.", phiếu vẫn Chờ duyệt', '1000 ký tự: từ chối được, lý do lưu đủ'])
S7.add('Từ chối thành công', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối, nhập lý do, bấm Từ chối.'], 'Lý do: Thiếu Đà Nẵng dịch vụ',
       ['Báo "Đã từ chối %s"' % P2, 'Phiếu về Đang tạo, rời lối vào chờ duyệt và rời danh sách của B', 'Màn quay về danh sách'])
S7.add('Người lập thấy lý do và thông báo', 'P0', [ACC_E, 'B vừa từ chối %s, lý do "Thiếu Đà Nẵng dịch vụ".' % P2], ['E mở chuông thông báo, bấm vào thông báo.'], '—',
       ['E nhận "[CTKDNV] Từ chối: %s. Lý do: Thiếu Đà Nẵng dịch vụ"' % P2, 'Màn Chi tiết có dòng "Lý do từ chối: Thiếu Đà Nẵng dịch vụ"', 'Có Sửa, Gửi duyệt, Hủy phiếu'])
S7.add('Bấm Hủy ở hộp Từ chối', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối, gõ lý do, bấm Hủy.'], '—', ['Phiếu vẫn Chờ duyệt, không thông báo'])
S7.add('Không từ chối phiếu đã chuyển trạng thái', 'P1', [ACC_B, 'Tài khoản B2 (quyền Duyệt, TPE).', PEND], ['B mở Chi tiết %s.' % P2, 'B2 duyệt %s.' % P2, 'B bấm Từ chối, nhập lý do, xác nhận.'], '—',
       ['B báo %s' % NOPERM, 'Phiếu giữ Đã duyệt'])

# ============================================================================ VIII. HỦY PHIẾU
S8 = Sec()
S8.add('Điều kiện hiện nút Hủy phiếu', 'P0', [ACC_A, DATA, 'A có thêm phiếu Chờ duyệt TPE_CTKDNV_2028.00080.'], [MENU, 'Mở ba chấm của %s, TPE_CTKDNV_2028.00080, %s, %s.' % (M, P3, P4)], '—',
       ['%s (Đang tạo), TPE_CTKDNV_2028.00080 (Chờ duyệt): có Hủy phiếu' % M, '%s (Đã duyệt), %s (Hủy): không có' % (P3, P4)])
S8.add('Hộp xác nhận hủy', 'P1', [ACC_A, PLAN_M], [MENU, 'Bấm Hủy phiếu ở dòng %s.' % M], '—',
       ['Hộp "Hủy phiếu", nội dung "Hủy phiếu %s? Phiếu Hủy không sửa được; phòng được tạo phiếu khác cho năm 2027.", nút Đóng / Hủy phiếu (đỏ)' % M])
S8.add('Hủy phiếu Đang tạo', 'P0', [ACC_A, PLAN_M], [MENU, 'Bấm Hủy phiếu ở dòng %s > Hủy phiếu.' % M], '—',
       ['Báo "Đã hủy %s"' % M, 'Trạng thái Hủy (đỏ), hết Sửa / Gửi duyệt / In / Xuất Excel'])
S8.add('Hủy phiếu đang Chờ duyệt', 'P0', [ACC_E, PEND, ACC_B], [MENU, 'E hủy phiếu %s.' % P2, 'B mở lối vào "Giao chỉ tiêu NV chờ duyệt".'], '—',
       ['%s chuyển Hủy' % P2, 'Rời lối vào chờ duyệt của B', 'Không có thông báo hủy gửi cho B'])
S8.add('Bấm Đóng ở hộp xác nhận', 'P1', [ACC_A, PLAN_M], [MENU, 'Bấm Hủy phiếu ở dòng %s, chọn Đóng.' % M], '—', ['Phiếu vẫn Đang tạo'])
S8.add('Phiếu Hủy chỉ còn Xem và Lịch sử', 'P0', [ACC_A, 'Phiếu %s đã Hủy.' % P4], [MENU, 'Mở ba chấm dòng %s; mở Chi tiết.' % P4], '—',
       ['Dòng: chỉ Xem, Lịch sử', 'Màn Chi tiết: chỉ nút Quay lại'])
S8.add('Người duyệt không hủy phiếu người khác', 'P1', [ACC_B, PEND], OPEN_P2_B, '—', ['Không có nút Hủy phiếu (chỉ người lập có quyền %s mới hủy)' % Q_CRE])
S8.add('Hủy khi phiếu vừa được duyệt', 'P1', [ACC_E, PEND], ['E mở Chi tiết %s.' % P2, 'B duyệt %s.' % P2, 'E bấm Hủy phiếu > Hủy phiếu.'], '—',
       ['E báo %s' % NOPERM, 'Phiếu giữ Đã duyệt (phiếu đã duyệt phải Hủy duyệt trước)'])

# ============================================================================ IX. LỊCH SỬ
S9 = Sec()
S9.add('Mở lịch sử từ danh sách', 'P1', [ACC_A, PLAN_M], [MENU, 'Ở dòng %s bấm ba chấm > Lịch sử.' % M], '—',
       ['Mở popup lịch sử của Phiếu %s' % M, 'Mỗi dòng có người thực hiện, thời gian, loại thao tác, nội dung đổi; dòng mới nhất ở trên'])
S9.add('Ghi nhận Tạo mới', 'P1', [ACC_A, 'A vừa lưu phiếu M.'], [MENU, 'Mở Lịch sử %s.' % M], '—',
       ['Có dòng "Tạo mới" của Trần Văn Bình, kèm Số phiếu %s, Năm 2027, Phòng ban Kinh doanh 1' % M])
S9.add('Ghi nhận cả luồng trạng thái', 'P0', [ACC_E, 'Phiếu %s đã: tạo, gửi duyệt, B từ chối (lý do "Thiếu Đà Nẵng dịch vụ"), E gửi lại, B duyệt, B hủy duyệt.' % P2],
       [MENU, 'Mở Lịch sử %s.' % P2], '—',
       ['Thứ tự mới trước: Hủy duyệt (Đã duyệt sang Đang tạo) · Duyệt (Chờ duyệt sang Đã duyệt) · Gửi duyệt (Đang tạo sang Chờ duyệt) · '
        'Từ chối (Chờ duyệt sang Đang tạo, ghi chú "Lý do: Thiếu Đà Nẵng dịch vụ") · Gửi duyệt · Tạo mới',
        'Mỗi dòng ghi đúng người thực hiện (E hoặc B) và thời gian'])
S9.add('Ghi nhận Hủy phiếu', 'P1', [ACC_A, 'Phiếu %s vừa bị A hủy khi Đang tạo.' % M], [MENU, 'Mở Lịch sử %s.' % M], '—',
       ['Dòng "Thay đổi trạng thái": Trạng thái Đang tạo sang Hủy'])
S9.add('Lưu mà không đổi gì', 'P2', [ACC_A, PLAN_M], [MENU, 'Mở Sửa %s, không đổi gì, bấm Lưu.' % M, 'Mở Lịch sử.'], '—',
       ['Theo chuẩn: không phát sinh dòng lịch sử mới', 'Lưu ý: bản hiện tại có thể vẫn ghi 1 dòng "Thay đổi thông tin" mỗi lần Lưu — ghi nhận nếu còn'])
S9.add('Lịch sử ở màn Chi tiết và đóng popup', 'P2', [ACC_A, PLAN_M], [MENU, 'Mở Chi tiết %s, cuộn xuống khối thông tin hệ thống.' % M, 'Về danh sách, mở Lịch sử, bấm X.'], '—',
       ['Màn Chi tiết có khối lịch sử khớp popup ở danh sách', 'Đóng popup: danh sách giữ bộ lọc và trang'])

# ============================================================================ X. XEM CHI TIẾT
S10 = Sec()
S10.add('Mở màn Chi tiết phiếu', 'P0', [ACC_A, PLAN_M], [MENU, 'Bấm số phiếu %s.' % M], '—',
        ['Tiêu đề "Chi tiết %s: %s" kèm nhãn trạng thái Đang tạo' % (ten, M),
         'Khối Thông tin phiếu: Số phiếu, Năm (khoá), Phòng ban hiện chữ "Kinh doanh 1" (không phải ô chọn)', 'Dòng người tạo + thời gian tạo ở góc khối'])
S10.add('Bảng ở chế độ chỉ đọc', 'P0', [ACC_A, PLAN_M], [MENU, 'Mở Chi tiết %s.' % M], '—',
        ['Dòng nhân viên hiện chữ "%s", không có ô chọn, nút xoá, liên kết "Thêm Nhân Viên"' % NV1,
         'Ô số là chữ thường, không có ô nhập; ô 0 ở dòng nhân viên để trống', 'Thu / mở tỉnh và ô "Hiển thị đến cấp" vẫn dùng được'])
S10.add('Số liệu Chi tiết khớp lúc lưu', 'P0', [ACC_A, PLAN_M], [MENU, 'Mở Chi tiết %s.' % M, 'Bấm thẻ Tổng hợp.'], '—',
        ['Dòng TỔNG "2 Tỉnh/TP · 2 nhân viên" và số từng tỉnh khớp ca Lưu ở nhóm Thêm mới', 'Thẻ Tổng hợp: Kinh doanh 1 tổng 7,600,000,000'])
S10.add('Chỉ tiêu giao của phiếu đã gửi giữ theo lúc lưu', 'P1',
        [ACC_A, APPR, 'Sau khi %s được duyệt, phiếu phòng ban 2026 bị Hủy duyệt, sửa chỉ tiêu Hà Nội rồi Đã duyệt lại.' % P3],
        [MENU, 'Mở Chi tiết %s.' % P3], '—', ['Dòng Chỉ tiêu giao giữ số lúc lưu phiếu, không đổi theo chỉ tiêu mới (chỉ phiếu Đang tạo mới lấy chỉ tiêu mới nhất)'])
S10.add('Nút chân trang theo trạng thái và vai trò', 'P0', [ACC_A, ACC_B, ACC_E, DATA],
        ['A mở Chi tiết %s, %s.' % (M, P3), 'E mở Chi tiết %s.' % P2, 'B mở Chi tiết %s, %s.' % (P2, P3)], '—',
        ['A - %s: Sửa, Gửi duyệt, Hủy phiếu, Xuất Excel, In, Quay lại' % M, 'A - %s: Xuất Excel, In, Quay lại' % P3,
         'E - %s: Hủy phiếu, Xuất Excel, In, Quay lại' % P2, 'B - %s: Duyệt, Từ chối, Xuất Excel, In, Quay lại' % P2,
         'B - %s: Hủy duyệt, Xuất Excel, In, Quay lại' % P3])
S10.add('Nút ở Chi tiết khớp danh sách', 'P1', [ACC_B, DATA], [MENU, 'So mục trong ba chấm dòng %s với nút chân màn Chi tiết %s.' % (P3, P3)], '—',
        ['Cùng tập thao tác (Hủy duyệt, In, Xuất Excel, Lịch sử), chi tiết chỉ thiếu Xem'])
S10.add('Mở Chi tiết phiếu không còn tồn tại', 'P1', [ACC_A, 'Đường dẫn Chi tiết của 1 phiếu đã bị xoá khỏi cơ sở dữ liệu.'], ['Mở đường dẫn đó.'], '—',
        ['Không lỗi trang, quay về danh sách'])
S10.add('Quay lại giữ trang và bộ lọc', 'P1', 'Tài khoản V4, 25 phiếu.', [MENU, 'Lọc Chờ duyệt, sang trang 2.', 'Mở Chi tiết 1 phiếu, bấm Quay lại.'], '—',
        ['Về trang 2, bộ lọc còn'])
S10.add('Quay lại từ lối vào chờ duyệt về đúng lối vào', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm Quay lại.'], '—',
        ['Về danh sách chờ duyệt (tiêu đề có "chờ duyệt"), không về danh sách thường'])
S10.add('Thao tác ở Chi tiết xong quay về danh sách', 'P0', [ACC_A, PLAN_M], [MENU, 'Mở Chi tiết %s, bấm Gửi duyệt > Gửi duyệt.' % M], '—',
        ['Theo quy tắc chung: sau Gửi duyệt / Duyệt / Từ chối / Hủy duyệt / Hủy phiếu thành công thì quay về danh sách',
         'Lưu ý: nếu màn ở lại Chi tiết và chỉ tải lại phiếu thì ghi nhận lỗi'])

# ============================================================================ XI. IN
S11 = Sec()
S11.add('In từ danh sách', 'P0', [ACC_A, APPR, 'Phiếu %s có Hà Nội 2 nhân viên, Hải Phòng 1 nhân viên.' % P3], [MENU, 'Ở dòng %s bấm ba chấm > In.' % P3], '—',
        ['Popup "Xem trước phiếu: %s", tờ A4 ngang' % P3, 'Góc phải: "Số: %s", "Ngày tạo: dd/mm/yyyy"; đầu trang là letterhead công ty TPE' % P3,
         'Tiêu đề "PHIẾU GIAO CHỈ TIÊU KINH DOANH THEO NHÂN VIÊN"; dòng "Năm: 2026 · Phòng ban: Kinh doanh 1 · Trạng thái: Đã duyệt"'])
S11.add('Nội dung bảng Giao chỉ tiêu trên bản in', 'P0', [ACC_A, APPR], [MENU, 'In %s.' % P3], '—',
        ['Mục "Giao chỉ tiêu": cột STT, Tỉnh/TP, Nhân viên kinh doanh + 12 cột số (Khách hãng / Khách khác / Tổng cộng x Hàng hóa / Dịch vụ x SL / Doanh số)',
         'Đầu bảng "Tổng cộng" 2 dòng: Chỉ tiêu giao, Tổng giao nhân viên', 'Mỗi tỉnh: Chỉ tiêu giao, Tổng giao nhân viên, các dòng nhân viên "Tên - Mã"',
         'Số dạng 1,234,567, ô 0 ở dòng nhân viên để trống'])
S11.add('Mục Tổng hợp theo nhân viên trên bản in', 'P1', [ACC_A, APPR], [MENU, 'In %s, cuộn xuống.' % P3], '—',
        ['Mục "Tổng hợp theo nhân viên": STT, Nhân viên, Tổng doanh số, Tỉnh/TP, Doanh số theo tỉnh; dòng đầu là tên phòng + tổng', 'Số khớp thẻ Tổng hợp ở màn Chi tiết'])
S11.add('Khối ký tên 3 cột', 'P1', [ACC_A, APPR], [MENU, 'In %s.' % P3], '—',
        ['3 cột: Người lập (Trần Văn Bình, Ngày <ngày tạo>), Trưởng phòng (trống), Người duyệt (Đỗ Thị Lan, Ngày 10/11/2026)',
         'Dưới mỗi chức danh có "(Ký, ghi rõ họ tên)"', 'Tên và chữ "Ngày" nằm 2 dòng riêng, không dính'])
S11.add('Nút In ở màn Chi tiết và in phiếu Đang tạo', 'P1', [ACC_A, PLAN_M], [MENU, 'Mở Chi tiết %s, bấm In.' % M], '—',
        ['Mở popup xem trước như trên, Trạng thái: Đang tạo', 'Ô Người duyệt trên khối ký tên trống'])
S11.add('Letterhead theo công ty của phiếu', 'P2', 'Tài khoản V4 đang làm việc ở công ty TPE.', [MENU, 'In %s (công ty TPSG).' % P6], '—',
        ['Đầu trang là letterhead của TPSG, không phải TPE'])
S11.add('Phiếu Hủy không in', 'P1', [ACC_A, 'Phiếu %s đã Hủy.' % P4], [MENU, 'Mở ba chấm dòng %s; mở Chi tiết.' % P4], '—', ['Không có In ở dòng lẫn màn Chi tiết'])

# ============================================================================ XII. TÙY CHỈNH CỘT
S12 = Sec()
S12.add('Mở popup cấu hình cột', 'P1', ACC_V4, [MENU, 'Bấm Cấu hình cột hiển thị.'], '—',
        ['Liệt kê đủ cột: STT, Số phiếu, Phòng ban, Năm, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái, Hành động', 'Cột đang hiện được tick sẵn, Ngày duyệt bỏ tick'])
S12.add('Hiện cột đang ẩn và ẩn cột đang hiện', 'P1', ACC_V4, [MENU, 'Mở cấu hình, tick Ngày duyệt, bỏ tick Người tạo, lưu.'], '—',
        ['Cột Ngày duyệt hiện đúng dữ liệu', 'Cột Người tạo biến mất'])
S12.add('Cột khoá không ẩn được, cột cố định', 'P2', ACC_V4, [MENU, 'Mở cấu hình.', 'Cuộn ngang bảng.'], '—',
        ['STT, Số phiếu, Hành động không bỏ tick được', 'STT và Số phiếu đứng yên khi cuộn ngang'])
S12.add('Kéo thả đổi thứ tự cột', 'P2', ACC_V4, [MENU, 'Kéo cột Trạng thái lên sau Số phiếu, lưu.'], '—', ['Bảng đổi thứ tự đúng'])
S12.add('Đóng không lưu', 'P2', ACC_V4, [MENU, 'Mở cấu hình, đổi vài cột, đóng không lưu.'], '—', ['Bảng giữ như cũ'])
S12.add('Ghi nhớ sau F5 và theo tài khoản', 'P2', 'A và V4 dùng chung trình duyệt.', ['V4 ẩn cột Người duyệt, nhấn F5.', 'Đăng nhập A, mở màn.'], '—',
        ['V4: sau F5 cột vẫn ẩn', 'A: theo cấu hình riêng của A'])
S12.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', ACC_V4, [MENU, 'Lọc Chờ duyệt.', 'Ẩn / hiện cột.'], '—', ['Số phiếu trên bảng và bộ lọc giữ nguyên'])

# ============================================================================ XIII. XUẤT EXCEL
S13 = Sec()
S13.add('Mở popup chọn trường', 'P1', ACC_V4, [MENU, 'Bấm Xuất Excel.'], '—',
        ['Danh sách trường: Số phiếu, Phòng ban, Năm, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái', 'Trường chọn sẵn = các cột đang hiện trên bảng'])
S13.add('Xuất với trường mặc định', 'P0', [ACC_V4, DATA], [MENU, 'Bấm Xuất Excel > Xuất file.'], '—',
        ['Tải file "phieu_giao_chi_tieu_theo_nhan_vien.xlsx", báo "Xuất Excel thành công"',
         'Tiêu đề "DANH SÁCH PHIẾU GIAO CHỈ TIÊU KINH DOANH THEO NHÂN VIÊN", cột STT + các trường đã chọn đúng thứ tự',
         'Có 5 dòng: %s, %s, %s, %s, %s' % (P2, P3, P4, P6, P7)])
S13.add('Xuất tất cả / một số / không trường nào', 'P1', ACC_V4, [MENU, 'Xuất Excel: chọn tất cả, xuất.', 'Lần 2 chỉ chọn Số phiếu, Trạng thái.', 'Lần 3 bỏ hết tick.'], '—',
        ['Lần 1 đủ mọi cột', 'Lần 2 chỉ STT, Số phiếu, Trạng thái', 'Lần 3 không xuất được (nút bị chặn hoặc báo phải chọn trường)'])
S13.add('Xuất theo tìm kiếm và bộ lọc', 'P0', [ACC_V4, DATA], [MENU, 'Lọc Năm 2027.', 'Xuất Excel > Xuất file.'], '—', ['File chỉ có 2 dòng %s, %s' % (P2, P6)])
S13.add('Xuất nhiều trang và danh sách rỗng', 'P1', 'Tài khoản V4, 25 phiếu, đang ở trang 1.', [MENU, 'Xuất Excel > Xuất file.', 'Lọc Năm 2028 không có phiếu, xuất lại.'], '—',
        ['File đủ 25 dòng, STT 1 tới 25; trong lúc xuất có dòng tiến độ "Đã tải …/25 dòng…"', 'Danh sách rỗng: báo "Không có dữ liệu để xuất", không tải file'])
S13.add('Định dạng ngày, chữ trong file danh sách', 'P2', [ACC_V4, DATA], [MENU, 'Xuất Excel đủ trường.'], '—',
        ['Ngày tạo / Ngày duyệt dạng dd/mm/yyyy', 'Tên tiếng Việt có dấu đúng, Trạng thái ghi chữ (Chờ duyệt, Đã duyệt…)'])
S13.add('Xuất từ lối vào chờ duyệt', 'P1', [ACC_B, DATA], [MENU_CD, 'Xuất Excel > Xuất file.'], '—', ['File có đúng 2 phiếu chờ duyệt %s, %s' % (P2, P7)])
S13.add('Xuất Excel 1 phiếu', 'P0', [ACC_A, APPR], [MENU, 'Ở dòng %s bấm ba chấm > Xuất Excel.' % P3, 'Mở Chi tiết %s, bấm Xuất Excel.' % P3], '—',
        ['Tải file "%s.xlsx", báo "Xuất Excel thành công"' % P3, 'File có 2 trang tính: "Giao chỉ tiêu", "Tổng hợp theo nhân viên"',
         'Tiêu đề "PHIẾU GIAO CHỈ TIÊU KINH DOANH THEO NHÂN VIÊN", dòng "Số: %s · Năm: 2026 · Phòng ban: Kinh doanh 1 · Trạng thái: Đã duyệt"' % P3])
S13.add('Excel 1 phiếu: số liệu và định dạng', 'P1', [ACC_A, APPR], ['Mở file vừa xuất.'], '—',
        ['Trang "Giao chỉ tiêu": Tổng cộng (Chỉ tiêu giao, Tổng giao nhân viên), mỗi tỉnh mở hết tới dòng nhân viên; số khớp màn Chi tiết',
         'Ô số là số thật dạng 1,234,567, cộng được bằng hàm tổng', 'Trang "Tổng hợp theo nhân viên" khớp thẻ Tổng hợp'])
S13.add('Phiếu Hủy không xuất Excel', 'P2', [ACC_A, 'Phiếu %s đã Hủy.' % P4], [MENU, 'Mở ba chấm dòng %s.' % P4], '—', ['Không có Xuất Excel'])

# ============================================================================ XIV. RÀNG BUỘC
S14 = Sec()
S14.add('Yêu cầu issue: bỏ nhập chi tiết khách hàng', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW, '—',
        ['KHÔNG còn nút / popup "Thêm / Xem Khách Hàng" ở dòng nhân viên', 'KHÔNG còn ô tick "Khách hàng mới"',
         '8 ô nhập thẳng trên dòng nhân viên: Khách hãng Hàng hóa (SL khách, Doanh số), Khách hãng Dịch vụ, Khách khác Hàng hóa, Khách khác Dịch vụ'])
S14.add('Yêu cầu issue: bỏ "Nhân viên mới"', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW + ['Mở ô chọn nhân viên.'], '—',
        ['KHÔNG có lựa chọn / nút "Nhân viên mới", không có ô gõ tay họ tên', 'Chỉ chọn được nhân viên có trong danh mục'])
S14.add('Chỉ tiêu lấy từ phiếu phòng ban Đã duyệt cùng công ty và năm', 'P0',
        [ACC_A, TARGET, 'Công ty TPSG có phiếu phòng ban 2027 Đã duyệt giao phòng tên "Kinh doanh 1" của TPSG tại Hà Nội.'], OPEN_NEW, '—',
        ['Chỉ tiêu Hà Nội của KD1 (TPE) là 10 / 5,000,000,000, không cộng số của công ty TPSG'])
S14.add('Cộng chỉ tiêu khi phòng ở 2 khối cùng tỉnh', 'P0', [ACC_A, TARGET, FREE], OPEN_NEW, '—',
        ['Hà Nội chỉ có 1 dòng tỉnh, Chỉ tiêu giao Khách hãng Hàng hóa = 6 (khối Dự án) + 4 (khối Dân dụng) = 10, Doanh số 5,000,000,000',
         'Không tách thành 2 dòng Hà Nội'])
S14.add('Phiếu phòng ban Chờ duyệt / Đang tạo không tính', 'P0',
        [ACC_A, 'Năm 2029: phiếu phòng ban của TPE đang Chờ duyệt, có KD1 ở Hà Nội; không có phiếu phòng ban 2029 Đã duyệt.'],
        [MENU, 'Bấm Tạo mới, chọn Năm 2029, mở ô Phòng ban.'], 'Năm 2029',
        ['Ô Phòng ban không có Kinh doanh 1', 'Khối Chi tiết hiện "Chọn phòng ban để nạp chỉ tiêu"'])
S14.add('Phòng chưa có chỉ tiêu: câu báo', 'P1',
        ['Tài khoản G (chọn mọi phòng của công ty).', 'Phiếu phòng ban 2027 Đã duyệt bị Hủy duyệt NGAY sau khi G đã chọn Kinh doanh 1 trên form (form chưa tải lại).'],
        [MENU, 'Bấm Tạo mới, Năm 2027, chọn Kinh doanh 1.', 'Ở thẻ khác Hủy duyệt phiếu phòng ban 2027.', 'Quay lại form, chọn Kinh doanh 2 rồi chọn lại Kinh doanh 1, bấm Lưu.'], '—',
        ['Khối Chi tiết hiện "%s"' % NO_TARGET, 'Ô Phòng ban báo đỏ "%s", không lưu được' % NO_TARGET])
S14.add('Phiếu phòng ban bị chặn Hủy duyệt khi phiếu nhân viên đang dùng', 'P0',
        ['Tài khoản P: có quyền %s.' % Q_APP_PB, TARGET, 'Phiếu nhân viên %s (KD2, năm 2027) đang Chờ duyệt.' % P2],
        [MENU_PB, 'Mở Chi tiết %s, bấm Hủy duyệt > Hủy duyệt.' % PB], '—',
        ['Báo "Đã có phiếu giao chỉ tiêu theo nhân viên %s dùng chỉ tiêu của phiếu này, cần hủy duyệt/từ chối phiếu đó trước"' % P2,
         'Phiếu phòng ban giữ Đã duyệt'])
S14.add('Phiếu nhân viên Đã duyệt cũng chặn Hủy duyệt phiếu phòng ban', 'P1',
        ['Tài khoản P như trên.', 'Phiếu nhân viên KD1 năm 2027 Đã duyệt (P2 đã bị Hủy).'], [MENU_PB, 'Hủy duyệt %s.' % PB], '—',
        ['Bị chặn, câu báo nêu số phiếu nhân viên KD1 2027'])
S14.add('Phiếu nhân viên Đang tạo không chặn, gửi lại thì bị chặn', 'P0',
        ['Tài khoản P như trên.', PLAN_M, 'Không còn phiếu nhân viên 2027 nào Chờ duyệt / Đã duyệt.'],
        [MENU_PB, 'Hủy duyệt %s.' % PB, 'A: %s' % MENU, 'A bấm Gửi duyệt %s.' % M, 'A mở Sửa %s, bấm Lưu.' % M], '—',
        ['Hủy duyệt phiếu phòng ban thành công', 'Gửi duyệt: báo "%s — mở Sửa để kiểm tra lại phiếu", phiếu vẫn Đang tạo' % NO_TARGET,
         'Lưu ở form Sửa: Phòng ban báo đỏ "%s"' % NO_TARGET])
S14.add('Tỉnh bị bỏ khỏi chỉ tiêu phòng khi phiếu nhân viên còn Đang tạo', 'P1',
        [PLAN_M, 'Phiếu phòng ban %s được Hủy duyệt, xoá Hải Phòng của KD1 rồi Đã duyệt lại.' % PB], [MENU, 'A mở Sửa %s.' % M, 'Bấm Lưu, mở Chi tiết.'], '—',
        ['Mở Sửa: Hải Phòng có Chỉ tiêu giao trống', 'Sau Lưu: kiểm Hải Phòng và dòng %s ở Hải Phòng còn hay mất' % NV1,
         'Lưu ý: nếu dòng giao bị bỏ mà không có cảnh báo thì ghi nhận lỗi'])
S14.add('Phiếu cũ có dòng "nhân viên mới" mở Xem', 'P0',
        [ACC_V3, 'Phiếu cũ TPE_CTKDNV_2025.00009 (lập trên hệ thống cũ, Đã duyệt) có dòng nhân viên mới chỉ có họ tên "Nguyễn Văn Test" ở Hà Nội.'],
        [MENU, 'Tìm "TPE_CTKDNV_2025.00009", mở Chi tiết.'], '—',
        ['Dòng nhân viên hiện "Nguyễn Văn Test" (chỉ họ tên, không mã)', 'Đủ 8 số của dòng đó, không lỗi trang', 'Thẻ Tổng hợp có "Nguyễn Văn Test"'])
S14.add('Phiếu cũ có "nhân viên mới" mở Sửa', 'P0',
        ['Phiếu cũ TPE_CTKDNV_2025.00010 do A lập trên hệ thống cũ, Đang tạo, có dòng nhân viên mới "Nguyễn Văn Test" có số.', 'Phiếu phòng ban 2025 Đã duyệt có KD1.'],
        [MENU, 'A mở Sửa phiếu đó.', 'Bấm Lưu.'], '—',
        ['Mở được form, không lỗi trang', 'Ô chọn nhân viên của dòng đó đỏ %s' % REQ, 'Chọn 1 nhân viên trong danh mục thì lưu được'])
S14.add('Phiếu cũ có chi tiết khách hàng hiện đủ số', 'P1',
        [ACC_V3, 'Phiếu cũ TPE_CTKDNV_2025.00009 có chi tiết khách hàng ở hệ thống cũ.'], [MENU, 'Mở Chi tiết phiếu đó.'], '—',
        ['Dòng nhân viên hiện đúng 8 số đã nhập, không có nút xem danh sách khách hàng'])
S14.add('Phiếu nhân viên Đã duyệt dùng cho kế hoạch nhân viên', 'P2', [NV1 + ' có chỉ tiêu trong phiếu nhân viên KD1 năm 2027 vừa Đã duyệt.'],
        ['Nhân viên Nguyễn Văn Nam vào Bán hàng > nhóm "Kế hoạch" > mục "Kế hoạch bán hàng" > bấm "Của nhân viên".', 'Bấm Tạo mới, chọn Năm 2027.'], '—',
        ['Lập được kế hoạch, ô Tỉnh/TP có Hà Nội và Hải Phòng (tỉnh được giao chỉ tiêu)'])

# ============================================================================ XV. PHÂN QUYỀN
S15 = Sec()
S15.add('Không có quyền nào', 'P0', [ACC_D, DATA], [MENU, 'Bấm Tìm kiếm nâng cao.'], '—',
        ['Vào được màn, bảng hiện %s (chỉ thấy phiếu mình lập)' % EMPTY, 'KHÔNG có nút Tạo mới', 'Không có mục "Giao chỉ tiêu NV chờ duyệt" ở nhóm Phê Duyệt'])
S15.add('Quyền %s' % Q_CRE, 'P0', [ACC_A, DATA], [MENU], '—',
        ['Có nút Tạo mới; lập, sửa, gửi duyệt, hủy phiếu của mình', 'Chỉ thấy 3 phiếu mình lập, không thấy phiếu người khác'])
S15.add('Quyền %s' % Q_APP, 'P0', [ACC_B, DATA], [MENU_CD, 'Duyệt %s.' % P2], '—',
        ['Có mục "Giao chỉ tiêu NV chờ duyệt"', 'Danh sách thường thấy phiếu Chờ duyệt của TPE + phiếu mình đã duyệt (%s, %s, %s)' % (P2, P3, P7),
         'Duyệt / Từ chối / Hủy duyệt được phiếu cùng công ty; không có nút Tạo mới'])
S15.add('Quyền %s mức Công ty' % Q_VIEW, 'P0', [ACC_V3, DATA], [MENU], '—',
        ['Thấy 4 phiếu %s, %s, %s, %s (mọi phiếu TPE trừ Đang tạo)' % (P2, P3, P4, P7), 'Không thấy %s (TPSG), %s, %s (Đang tạo)' % (P6, M, P5),
         'Bộ lọc không có ô Công ty'])
S15.add('Quyền %s mức Tổng công ty' % Q_VIEW, 'P0', [ACC_V4, DATA], [MENU, ADV], '—',
        ['Thấy 5 phiếu (thêm %s của TPSG)' % P6, 'Bộ lọc có ô Công ty'])
S15.add('Quyền Xem không mở thao tác', 'P0', [ACC_V4, PEND], [MENU, 'Mở Chi tiết %s.' % P2], '—',
        ['Chỉ có Xuất Excel, In, Quay lại', 'Không có Duyệt, Từ chối, Sửa, Hủy phiếu, Hủy duyệt', 'Không có nút Tạo mới ở danh sách'])
S15.add('Hai vai trò khác mức thì lấy mức lớn hơn', 'P1', ['Tài khoản V5: vai trò 1 cấp %s mức Công ty, vai trò 2 cấp mức Tổng công ty.' % Q_VIEW, DATA], [MENU], '—',
        ['Thấy 5 phiếu như mức Tổng công ty'])
S15.add('Người đã duyệt vẫn thấy phiếu', 'P1', [ACC_B, APPR, 'Sau đó B bị gỡ quyền %s.' % Q_APP], [MENU], '—',
        ['B vẫn thấy %s (phiếu mình đã duyệt), chỉ xem' % P3, 'Không còn thấy phiếu Chờ duyệt của người khác'])
S15.add('Có quyền Duyệt chỉ thấy phiếu Chờ duyệt, không thấy Đang tạo', 'P1', [ACC_B, DATA], [MENU, 'Tìm %s, %s.' % (M, P5)], '—',
        ['Không thấy 2 phiếu Đang tạo', 'Không thấy %s (Hủy) vì B không có quyền Xem' % P4])
S15.add('Không có đặc quyền Super Admin', 'P1', ['Tài khoản SA: Super Admin, không được cấp 3 quyền của màn.', DATA], [MENU], '—',
        ['Chỉ thấy phiếu mình lập (bảng rỗng), không có nút Tạo mới', 'Không có mục "Giao chỉ tiêu NV chờ duyệt"'])
S15.add('Ẩn nút khi không có quyền thao tác', 'P0', [ACC_V4, DATA], [MENU, 'Mở ba chấm các dòng.'], '—',
        ['Không có Sửa, Gửi duyệt, Duyệt, Hủy duyệt, Hủy phiếu ở phiếu người khác', 'Chỉ Xem, In, Xuất Excel, Lịch sử (phiếu Hủy chỉ Xem, Lịch sử)',
         'Nút không dùng được bị ẨN, không hiện xám'])
S15.add('Bị gỡ quyền Tạo thì không sửa / hủy phiếu của mình', 'P0', [ACC_A, PLAN_M, 'Quản trị gỡ quyền %s của A.' % Q_CRE], [MENU, 'Mở ba chấm dòng %s.' % M], '—',
        ['Không có Sửa, Gửi duyệt, Hủy phiếu; không có nút Tạo mới', 'Vẫn Xem, In, Xuất Excel, Lịch sử'])
S15.add('Mở thẳng màn Chi tiết phiếu ngoài phạm vi', 'P0', [ACC_A, 'E gửi cho A đường dẫn màn Chi tiết phiếu %s.' % P2], ['A mở đường dẫn đó.'], '—',
        ['Không hiện dữ liệu phiếu, tự quay về danh sách của A'])
S15.add('Mở thẳng màn Sửa phiếu người khác', 'P0', [ACC_V4, 'A gửi cho V4 đường dẫn màn Sửa %s (Đang tạo).' % M], ['V4 mở đường dẫn đó.'], '—',
        ['Không mở được form, quay về danh sách', 'Phiếu M không đổi'])
S15.add('Mở thẳng màn Tạo mới khi thiếu quyền Tạo', 'P0', [ACC_D, TARGET], ['D mở đường dẫn màn Tạo phiếu (đánh dấu từ trước).', 'Chọn được thì nhập 1 dòng, bấm Lưu.'], '—',
        ['Hệ thống từ chối, báo không có quyền, không tạo phiếu',
         'Lưu ý: nếu màn Tạo mới vẫn mở ra cho nhập (chỉ bị chặn lúc Lưu) thì ghi nhận lệch quy chuẩn'])
S15.add('Mở lối vào chờ duyệt khi thiếu quyền Duyệt', 'P0', ACC_A, ['A mở đường dẫn lối vào "Giao chỉ tiêu NV chờ duyệt" do B gửi.'], '—',
        ['Danh sách chờ duyệt rỗng (%s)' % EMPTY, 'Không thấy phiếu của người khác'])
S15.add('Không lập phiếu cho phòng ngoài phạm vi', 'P0', [ACC_A, TARGET], [MENU, 'Bấm Tạo mới, Năm 2027, mở ô Phòng ban.'], '—',
        ['Không có Kinh doanh 2 trong ô chọn (A không quản lý, không có quyền Xem mức Công ty)',
         'Nếu cố lập cho KD2 (vd đường dẫn có sẵn phòng) thì báo "Bạn không được lập phiếu cho phòng ban này"'])
S15.add('Bị gỡ quyền Duyệt giữa lúc thao tác', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Quản trị gỡ quyền %s của B.' % Q_APP, 'B bấm Duyệt > Duyệt.'], '—',
        ['B báo không có quyền, phiếu vẫn Chờ duyệt', 'Tải lại: mục "Giao chỉ tiêu NV chờ duyệt" biến mất'])
S15.add('Được cấp quyền giữa lúc thao tác', 'P1', ['Tài khoản B3 (công ty TPE, chưa có quyền) đang ở danh sách.'], ['Quản trị cấp quyền %s cho B3.' % Q_APP, 'B3 tải lại trang.'], '—',
        ['Hiện mục "Giao chỉ tiêu NV chờ duyệt"', 'Thấy phiếu Chờ duyệt của TPE và nút Duyệt, Từ chối ở màn Chi tiết'])
S15.add('Đổi công ty đang làm việc', 'P0', ['Tài khoản V6: quyền %s mức Công ty và %s ở công ty TPE; ở TPSG không có quyền.' % (Q_VIEW, Q_APP), DATA],
        [MENU, 'Đổi công ty đang làm việc sang TPSG, mở lại màn.', 'Mở nhóm Phê Duyệt > Kế hoạch & chỉ tiêu.'], '—',
        ['Quyền tính lại theo TPSG: chỉ còn phiếu mình lập', 'Không còn thấy phiếu công ty TPE, không có mục "Giao chỉ tiêu NV chờ duyệt"'])
S15.add('In, Xuất Excel, Lịch sử theo phạm vi xem', 'P1', [ACC_V3, DATA], [MENU, 'Xuất Excel danh sách; In và xem Lịch sử %s.' % P7], '—',
        ['File chỉ có 4 phiếu V3 xem được', 'In và Lịch sử mở được, không cần quyền riêng'])
S15.add('Tên quyền trong màn Vai trò', 'P2', 'Tài khoản quản trị.', ['Mở màn phân quyền Vai trò, tìm nhóm Bán hàng.'], '—',
        ['Có %s với 2 mức Công ty / Tổng công ty (dùng chung phiếu phòng ban và phiếu nhân viên)' % Q_VIEW,
         'Có %s và %s (không có mức)' % (Q_CRE, Q_APP)])

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
    ('III', 'THÊM MỚI', S3),
    ('IV', 'CHỈNH SỬA', S4),
    ('V', 'GỬI DUYỆT', S5),
    ('VI', 'DUYỆT PHIẾU – DUYỆT VÀ HỦY DUYỆT', S6),
    ('VII', 'KHÔNG DUYỆT PHIẾU – TỪ CHỐI', S7),
    ('VIII', 'HỦY PHIẾU', S8),
    ('IX', 'LỊCH SỬ THAY ĐỔI', S9),
    ('X', 'XEM CHI TIẾT PHIẾU', S10),
    ('XI', 'IN PHIẾU', S11),
    ('XII', 'TÙY CHỈNH CỘT', S12),
    ('XIII', 'XUẤT DANH SÁCH EXCEL VÀ XUẤT EXCEL PHIẾU', S13),
    ('XIV', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S14),
    ('XV', 'PHÂN QUYỀN', S15),
]

DESC = [
    ('1. Mục đích tính năng',
     '%s (#11651, phân hệ Bán hàng > Kế hoạch > Giao chỉ tiêu kinh doanh > Theo nhân viên): trưởng phòng chọn Năm + Phòng ban, hệ thống '
     'nạp chỉ tiêu của phòng theo từng Tỉnh/TP (từ phiếu giao chỉ tiêu theo phòng ban Đã duyệt), rồi giao tiếp cho từng nhân viên kinh doanh. '
     'Bỏ phần nhập chi tiết khách hàng và "Khách hàng mới" / "Nhân viên mới" của hệ thống cũ: 8 ô số nhập thẳng trên dòng nhân viên. '
     'Có luồng Gửi duyệt / Duyệt / Từ chối / Hủy duyệt / Hủy phiếu, In A4 ngang, Xuất Excel danh sách và 1 phiếu, Lịch sử.' % TEN),
    ('2. Đối tượng được tính / hiển thị',
     '- Trạng thái: Đang tạo, Chờ duyệt, Đã duyệt, Hủy (Từ chối và Hủy duyệt đưa phiếu về Đang tạo).\n'
     '- Lối vào danh sách ("Theo nhân viên"): phiếu mình lập (mọi trạng thái) + phiếu trong phạm vi quyền Xem chỉ tiêu + phiếu Chờ duyệt cùng công ty '
     'nếu có quyền Duyệt + phiếu mình đã duyệt.\n'
     '- Lối vào "Giao chỉ tiêu NV chờ duyệt" (nhóm Phê Duyệt): chỉ phiếu Chờ duyệt của công ty đang làm việc, cần quyền Duyệt chỉ tiêu kinh doanh theo nhân viên.\n'
     '- Ô Phòng ban ở form: phòng mình quản lý (có quyền Xem chỉ tiêu mức Công ty / Tổng công ty thì mọi phòng của công ty), chỉ phòng có chỉ tiêu '
     'trong phiếu phòng ban Đã duyệt của năm đang chọn.\n- Ô nhân viên: nhân viên đang làm việc của công ty người lập.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác (kể cả với quyền Xem mức Tổng công ty).\n'
     '- Phiếu công ty khác khi không có quyền Xem mức Tổng công ty; phiếu cùng công ty khi không có quyền Xem mức Công ty.\n'
     '- Chỉ tiêu từ phiếu phòng ban Chờ duyệt / Đang tạo / Hủy, phiếu phòng ban của công ty khác.\n'
     '- Ô nhân viên: người đã giao ở dòng khác cùng tỉnh, nhân viên công ty khác, nhân viên đã nghỉ.\n'
     '- Phiếu Hủy không tính khi kiểm "mỗi phòng mỗi năm 1 phiếu".'),
    ('4. Bộ lọc thời gian áp dụng cho',
     '- Ô Năm ở danh sách: năm của phiếu, lựa chọn từ năm nay +2 xuống 2023.\n'
     '- Ô Năm ở form: "Năm 2025" tới "Năm 2036", mặc định năm hiện tại; đổi năm thì nạp lại danh sách phòng và chỉ tiêu của năm đó.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Phiếu (1 công ty · 1 phòng · 1 năm) > Tỉnh/TP > Nhân viên.\n'
     '- Đầu bảng ghim: dòng TỔNG ("<n> Tỉnh/TP · <n> nhân viên") + dòng Chỉ tiêu giao của phòng. Mỗi tỉnh: dòng tỉnh ("<tỉnh> (<n> nhân viên)", STT La Mã) > '
     'dòng Chỉ tiêu giao > các dòng nhân viên (STT 1, 2…).\n'
     '- 12 cột số, tiêu đề 3 tầng: Khách hãng / Khách khác / Tổng cộng x Hàng hóa / Dịch vụ x SL khách / Doanh số. Nhập 8 ô (Khách hãng, Khách khác); Tổng cộng tự tính.\n'
     '- Thẻ "Tổng hợp": STT, Nhân viên, Tổng doanh số, Tỉnh/TP, Doanh số theo tỉnh.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Chỉ tiêu tỉnh của phòng = CỘNG các dòng của phòng ở mọi khối cùng tỉnh trong phiếu phòng ban Đã duyệt (phòng ở 2 khối cùng Hà Nội thì gộp 1 dòng).\n'
     '- Tổng tỉnh = cộng các dòng nhân viên; dòng TỔNG = cộng các tỉnh; Tổng cộng = Khách hãng + Khách khác.\n'
     '- 1 nhân viên chỉ 1 dòng trong 1 tỉnh; 1 người ở nhiều tỉnh vẫn đếm 1 nhân viên ở nhãn TỔNG và gộp 1 nhóm ở thẻ Tổng hợp.\n'
     '- Mỗi phòng mỗi năm chỉ 1 phiếu hiệu lực (Đang tạo, Chờ duyệt, Đã duyệt); phiếu Hủy không tính.\n'
     '- Phiếu Đang tạo luôn lấy chỉ tiêu mới nhất khi mở; phiếu đã gửi giữ chỉ tiêu chụp lúc lưu.'),
    ('7. Phân quyền cấp',
     '- Xem chỉ tiêu — mức: Công ty / Tổng công ty (dùng chung cho phiếu phòng ban và phiếu nhân viên; mức Tổng công ty có thêm ô lọc Công ty). '
     'Không có quyền Xem vẫn vào màn, chỉ thấy phiếu mình lập.\n'
     '- Tạo chỉ tiêu kinh doanh theo nhân viên: hiện nút Tạo mới; lập / sửa / gửi duyệt / hủy phiếu CỦA MÌNH.\n'
     '- Duyệt chỉ tiêu kinh doanh theo nhân viên: duyệt / từ chối / hủy duyệt phiếu cùng công ty đang làm việc; hiện mục "Giao chỉ tiêu NV chờ duyệt". '
     'Người chỉ có "Duyệt chỉ tiêu kinh doanh theo phòng ban" KHÔNG duyệt được phiếu nhân viên.\n'
     '- Quyền tính theo công ty đang làm việc; Super Admin không có đặc quyền riêng.'),
    ('8. Cách tính các ô thống kê',
     '- Nhãn TỔNG / góc khối Chi tiết: "<số Tỉnh/TP> Tỉnh/TP · <số nhân viên khác nhau đã chọn> nhân viên".\n'
     '- Ô tổng (dòng TỔNG, dòng tỉnh) lớn hơn Chỉ tiêu giao cùng cột: tô cam, rê chuột hiện "Vượt chỉ tiêu giao <chênh lệch>"; bằng thì không tô.\n'
     '- Thẻ Tổng hợp: Doanh số = Doanh số Hàng hóa + Dịch vụ của Khách hãng và Khách khác; dòng đầu = tên phòng + tổng doanh số cả phiếu.\n'
     '- Gửi duyệt cần tổng doanh số của phiếu lớn hơn 0.'),
    ('9. Ghi chú đọc bảng',
     '- Số nguyên, dấu phẩy ngăn nghìn 1,234,567; tối đa 13 chữ số; dán "1,234" hoặc "1.234" đều thành 1234; ô 0 ở dòng nhân viên / Chỉ tiêu giao để trống, dòng TỔNG / tỉnh hiện 0.\n'
     '- Lưu ý: ô số bỏ dấu chấm nên gõ "2.5" sẽ thành 25 — QA kiểm lại số sau khi gõ.\n'
     '- Vượt chỉ tiêu CHỈ tô cam, KHÔNG chặn Lưu / Gửi.\n'
     '- Kiểm cặp SL khách / Doanh số chỉ khi bấm Lưu và gửi; Lưu thường không kiểm.\n'
     '- Không có Xóa phiếu (thay bằng Hủy phiếu); phiếu Đã duyệt muốn sửa phải Hủy duyệt.\n'
     '- Phiếu phòng ban không Hủy duyệt được khi phiếu nhân viên cùng năm của phòng trong phiếu đó đang Chờ duyệt / Đã duyệt.\n'
     '- Bộ lọc danh sách ghi nhớ 10 phút theo trình duyệt. Ca 2 thẻ / 2 tài khoản cần chuẩn bị dữ liệu đúng Tiền điều kiện.'),
]

# ============================================================================ KIỂM THUẬT NGỮ (skill)
BANNED = [
    r"`[a-z_]{3,}`", r"\bBE\b", r"\bFE\b", r"\bHTTP\b",
    r"trả (400|403|404|422)", r"\b(400|403|404|422)\b",
    r"permission id", r"/api/v1", r"\bAPI /", r"localStorage",
    r"number_format", r"meta\.", r"sort_by", r"per_page",
    r"role_has_permissions", r"current_company_role",
    r"\bERP\b", r"\bAPI\b", r"https?://", r"\?type=", r"is_can_", r"for-approve",
]


def check_terms():
    blob = [b for _, b in DESC] + [x for _, _, s in SECTIONS for tc in s for x in tc[1:]]
    text_all = '\n'.join(blob)
    found = {p: len(re.findall(p, text_all)) for p in BANNED if re.findall(p, text_all)}
    emo = re.findall(u'[←-⯿☀-➿️\U0001F300-\U0001FAFF]', text_all)
    if emo:
        found['emoji/mui ten'] = sorted(set(emo))
    print('!!! CON THUAT NGU KY THUAT:', found) if found else print('OK - sach')
    return not found


if __name__ == '__main__':
    ids = [(r, tc[0]) for r, _, s in SECTIONS for tc in s]
    assert len(ids) == len(set(ids)), 'Trùng mã TC'
    total = len(ids)
    p0 = sum(1 for _, _, s in SECTIONS for tc in s if tc[2] == 'P0')
    print('==', TEN)
    print('Tong %d TC, P0 %d (%.1f%%)' % (total, p0, 100.0 * p0 / total))
    for r, t, s in SECTIONS:
        print('  %-5s %-50s %3d' % (r, t, len(s)))
    ok = check_terms()
    build_chuan(output_file=os.path.join(HERE, OUT), sheet_name='Trang tính1',
                feature_name='%s - Cập nhật ngày %s' % (TEN, TODAY), module_name='Giao chỉ tiêu KD theo NV',
                description_block=DESC, sections=[(r, t, list(s)) for r, t, s in SECTIONS], loai='phieu')
    sys.exit(0 if ok else 1)

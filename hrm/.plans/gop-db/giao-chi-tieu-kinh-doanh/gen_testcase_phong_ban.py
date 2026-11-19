# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu giao chỉ tiêu kinh doanh theo phòng ban" (#11643) — skill testcase-documenter,
KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu'). Cách viết chép theo
.plans/gop-db/11884-11885-ke-hoach-nhan-vien/gen_testcase.py.

Chạy: python gen_testcase_phong_ban.py -> "testcase - Phiếu giao chỉ tiêu kinh doanh theo phòng ban.xlsx"
(tự chạy check_tc, phải "DAT", 0 lỗi + bộ lọc thuật ngữ "OK - sach").

Nguồn hành vi (đọc 19/11/2026, code gop_db hiện tại): hrm-client pages/finance/business-target-departments/*,
components/business-target/{BusinessTargetList,TargetTreeTable}.vue, utils/business-target.js,
utils/mixins/businessTargetActionsMixin.js, utils/export/businessTargetExcel.js, components/subsystem-menu/sale-hub.js;
hrm-api Modules/Finance BusinessTarget* (Service, Transitions, Access, Controller, Request), bản in
resources/views/prints/finance/business_target_department.blade.php, Catalog sale.php.
Nhóm: I Hiển thị (2 lối vào) · II Tìm kiếm & lọc · III Thêm mới · IV Chỉnh sửa · V Gửi duyệt · VI Duyệt + Hủy duyệt
· VII Không duyệt (Từ chối) · VIII Hủy phiếu · IX Lịch sử · X Xem chi tiết · XI In · XII Tùy chỉnh cột · XIII Xuất Excel
(danh sách + 1 phiếu) · XIV Ràng buộc · XV Phân quyền (cuối).
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
OUT = os.path.join(HERE, 'testcase - Phiếu giao chỉ tiêu kinh doanh theo phòng ban.xlsx')
TEN = 'Phiếu giao chỉ tiêu kinh doanh theo phòng ban'
MODULE = 'Giao chỉ tiêu KD theo phòng ban'


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


# ============================================================================ NHÃN / CÂU NGUYÊN VĂN (theo code)
MENU = 'Vào phân hệ Bán hàng > nhóm "Kế hoạch" > mục "Giao chỉ tiêu kinh doanh" > bấm "Theo phòng ban".'
MENU_CD = 'Vào phân hệ Bán hàng > nhóm "Phê Duyệt" > mục "Kế hoạch & chỉ tiêu" > bấm "Giao chỉ tiêu chờ duyệt".'
MENU_NV = 'Vào phân hệ Bán hàng > nhóm "Kế hoạch" > mục "Giao chỉ tiêu kinh doanh" > bấm "Theo nhân viên".'
ADV = 'Bấm Tìm kiếm nâng cao.'
NEW = 'Bấm Tạo mới.'
LIST_TITLE = 'Danh sách phiếu giao chỉ tiêu kinh doanh theo phòng ban'
EMPTY = '"Không có phiếu giao chỉ tiêu nào"'
CHECK = '"Vui lòng kiểm tra lại dữ liệu nhập"'
REQ = '"Bắt buộc phải nhập"'
NOPERM = '"Bạn không có quyền thực hiện thao tác này"'
LOCKED = '"Chỉ sửa được phiếu ở trạng thái Đang tạo."'
NO_REV = '"Phiếu chưa có chỉ tiêu doanh số — không gửi được"'
NO_APPROVER = '"Chưa phân quyền người duyệt"'
NEED_REV = '"Bắt buộc nhập doanh số vì đã có SL Khách"'
NEED_CUS = '"Bắt buộc nhập SL Khách vì đã có doanh số"'
MAXV = '"Giá trị vượt quá giới hạn cho phép"'
UNSAVED = 'hộp "Thông tin chưa lưu" nội dung "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?", 2 nút Ở lại / Thoát'
QV = '"Xem chỉ tiêu"'
QC = '"Tạo chỉ tiêu kinh doanh theo phòng ban"'
QA = '"Duyệt chỉ tiêu kinh doanh theo phòng ban"'

# Số phiếu mẫu (công ty TPE)
P0 = 'TPE_CTKD_2025.00004'   # lập trên hệ thống cũ, Đã duyệt, có chi tiết khách hàng cũ
P3 = 'TPE_CTKD_2026.00009'   # Đã duyệt (B duyệt) — nguồn "Năm trước" của 2027
P4 = 'TPE_CTKD_2027.00012'   # Hủy
M = 'TPE_CTKD_2027.00015'    # Đang tạo (phiếu M)
P2 = 'TPE_CTKD_2028.00016'   # Chờ duyệt
P5 = 'TPE_CTKD_2029.00017'   # A2 lập, Đang tạo
P6 = 'TPSG_CTKD_2027.00018'  # TPSG, Chờ duyệt
P7 = 'TPSG_CTKD_2026.00011'  # TPSG, Đã duyệt
NV_OK = 'TPE_CTKDNV_2026.00027'   # phiếu theo nhân viên phòng KD1 2026, Đã duyệt
NV_DRAFT = 'TPE_CTKDNV_2026.00028'  # phiếu theo nhân viên phòng KD2 2026, Đang tạo

ACC_A = ('Tài khoản A (Nguyễn Văn A, phòng Kế hoạch kinh doanh, công ty TPE): chỉ có quyền %s.' % QC)
ACC_B = 'Tài khoản B (Trần Văn B, công ty TPE): chỉ có quyền %s.' % QA
ACC_A2 = 'Tài khoản A2 (Lê Thị Hoa, công ty TPE): chỉ có quyền %s.' % QC
ACC_V3 = 'Tài khoản V3 (công ty TPE): chỉ có quyền %s mức Công ty.' % QV
ACC_V4 = 'Tài khoản V4: chỉ có quyền %s mức Tổng công ty.' % QV
ACC_N = 'Tài khoản N (công ty TPE): không có quyền nào của màn, chưa lập phiếu nào.'
ACC_H = 'Tài khoản H (công ty TPSG): chỉ có quyền %s.' % QA
DATA = ('Bộ dữ liệu thử (ngoài các phiếu này không còn phiếu nào):\n'
        '- Công ty TPE: %s (A lập trên hệ thống cũ, Đã duyệt), %s (A, Đã duyệt, B duyệt 05/01/2026), %s (A, Hủy), %s (A, Đang tạo, '
        'phiếu M), %s (A, Chờ duyệt), %s (A2, Đang tạo)\n'
        '- Công ty TPSG: %s (X, Chờ duyệt), %s (X, Đã duyệt)' % (P0, P3, P4, M, P2, P5, P6, P7))
CAT = ('Danh mục công ty TPE: khối kinh doanh "Kinh doanh" (phòng Kinh doanh 1, Kinh doanh 2, Kinh doanh 3) và "Nghiệp vụ" '
       '(phòng Dự án 1); vùng "Đồng bằng sông Hồng" gồm Hà Nội, Hải Phòng, Bắc Ninh; vùng "Duyên hải miền Trung" gồm Đà Nẵng, '
       'Quảng Nam; phòng Kinh doanh 1 có 2 bộ phận Nhóm KD1-1, Nhóm KD1-2.')
FREE_2027 = 'Công ty TPE chưa có phiếu năm 2027 còn hiệu lực (chỉ có %s đã Hủy).' % P4
BEFORE_2026 = ('Phiếu %s (năm 2026, Đã duyệt) khối Kinh doanh, Hà Nội: Khách hãng Hàng hóa 8 / 2,500,000,000, Dịch vụ 2 / 450,000,000; '
               'Khách khác Hàng hóa 4 / 950,000,000, Dịch vụ 1 / 150,000,000.' % P3)
HN_KD1 = ['Hà Nội, phòng Kinh doanh 1:', 'Khách hãng Hàng hóa: SL khách 5, Doanh số 1,500,000,000',
          'Khách hãng Dịch vụ: SL khách 2, Doanh số 300,000,000', 'Khách khác Hàng hóa: SL khách 3, Doanh số 600,000,000',
          'Khách khác Dịch vụ: SL khách 1, Doanh số 150,000,000']
HN_KD2 = ['Hà Nội, phòng Kinh doanh 2:', 'Khách hãng Hàng hóa: 4 / 1,200,000,000', 'Khách hãng Dịch vụ: 1 / 200,000,000',
          'Khách khác Hàng hóa: 2 / 500,000,000']
HP_KD1 = ['Hải Phòng, phòng Kinh doanh 1:', 'Khách hãng Hàng hóa: 2 / 750,000,000', 'Khách khác Hàng hóa: 1 / 250,000,000']
FULL_TD = HN_KD1 + HN_KD2 + HP_KD1
PLAN_M = ('Phiếu M %s của A (năm 2027, Đang tạo, lập 12/11/2026), khối Kinh doanh, vùng Đồng bằng sông Hồng: Hà Nội có phòng Kinh doanh 1 '
          '(Khách hãng Hàng hóa 5 / 1,500,000,000, Dịch vụ 2 / 300,000,000; Khách khác Hàng hóa 3 / 600,000,000, Dịch vụ 1 / 150,000,000) và '
          'phòng Kinh doanh 2 (4 / 1,200,000,000; 1 / 200,000,000; 2 / 500,000,000); Hải Phòng có phòng Kinh doanh 1 (2 / 750,000,000; '
          'Khách khác Hàng hóa 1 / 250,000,000); Bắc Ninh chưa có phòng.' % M)
PEND = 'Phiếu %s của A đang Chờ duyệt (năm 2028, có doanh số).' % P2
APPR = 'Phiếu %s của A đang Đã duyệt (B duyệt 05/01/2026).' % P3
OPEN_P2_B = [MENU_CD, 'Bấm số phiếu %s.' % P2]
OPEN_M = [MENU, 'Bấm biểu tượng Sửa (bút chì) ở dòng %s.' % M]


def make():
    # ======================================================================== I. HIỂN THỊ
    S1 = Sec()
    S1.add('Mở màn hình từ menu (lối vào danh sách)', 'P0', [ACC_A, DATA], [MENU], '—',
           ['Mở màn %s, tiêu đề trang "%s"' % (TEN, TEN), 'Bảng có tiêu đề "%s"' % LIST_TITLE,
            'Có đúng 5 phiếu A lập: %s, %s, %s, %s, %s' % (P2, M, P4, P3, P0), 'Không thấy %s (A2), %s, %s (TPSG)' % (P5, P6, P7)])
    S1.add('Mục menu nằm đúng nhóm Kế hoạch', 'P1', ACC_N, ['Vào phân hệ Bán hàng.', 'Bấm nhóm "Kế hoạch" ở menu trái.'], '—',
           ['Mục "Giao chỉ tiêu kinh doanh" có 3 màn: "Theo phòng ban", "Theo nhân viên", "Phát triển sản phẩm"',
            '"Theo phòng ban" hiện với mọi tài khoản, không cần quyền', '"Phát triển sản phẩm" chưa mở được (chưa chuyển sang hệ thống mới)'])
    S1.add('Mở lối vào "Giao chỉ tiêu chờ duyệt"', 'P0', [ACC_B, DATA], [MENU_CD], '—',
           ['Tiêu đề trang "%s chờ duyệt", bảng "%s chờ duyệt"' % (TEN, LIST_TITLE),
            'Chỉ có 1 phiếu %s (Chờ duyệt, công ty TPE)' % P2,
            'KHÔNG có %s (Đã duyệt), %s (Đang tạo), %s (Chờ duyệt nhưng thuộc TPSG)' % (P3, M, P6)])
    S1.add('Lối vào chờ duyệt không có Tạo mới và ô lọc Trạng thái', 'P1', [ACC_B, 'B được cấp thêm quyền %s.' % QC], [MENU_CD, ADV], '—',
           ['Không có nút Tạo mới (dù B có quyền tạo)', 'Bộ lọc nâng cao không có ô Trạng thái', 'Vẫn có nút Xuất Excel và Cấu hình cột hiển thị'])
    S1.add('Mục chờ duyệt ẩn khi thiếu quyền duyệt', 'P0', ACC_A, ['Vào phân hệ Bán hàng > nhóm "Phê Duyệt" > mục "Kế hoạch & chỉ tiêu".'], '—',
           ['KHÔNG có mục "Giao chỉ tiêu chờ duyệt"', 'Lý do: A không có quyền %s' % QA])
    S1.add('Chuyển từ lối vào chờ duyệt sang lối vào danh sách', 'P0', [ACC_B, DATA], [MENU_CD, MENU], '—',
           ['Lối vào chờ duyệt: 1 phiếu %s' % P2, 'Sang lối vào danh sách: tiêu đề "%s", có 2 phiếu %s (chờ mình duyệt) và %s (mình đã duyệt)' % (LIST_TITLE, P2, P3),
            'Phạm vi theo lối vào mới, không giữ phạm vi chờ duyệt'])
    S1.add('Đổi bộ lọc rồi mở lối vào khác', 'P0', [ACC_B, DATA], [MENU, ADV, 'Chọn Trạng thái: Đã duyệt, bấm Tìm kiếm.', MENU_CD], 'Trạng thái: Đã duyệt',
           ['Lối vào chờ duyệt vẫn ra %s, không bị lọc Đã duyệt về 0' % P2, 'Ô Trạng thái không hiện ở lối vào chờ duyệt'])
    S1.add('Bấm Làm mới giữ phạm vi lối vào', 'P1', [ACC_B, DATA, 'Công ty TPE có thêm phiếu Chờ duyệt TPE_CTKD_2030.00020.'],
           [MENU_CD, 'Gõ "%s" vào ô tìm, bấm Tìm kiếm.' % P2, 'Bấm Làm mới.'], 'Từ khoá: %s' % P2,
           ['Sau tìm: 1 phiếu', 'Sau Làm mới: ô tìm trống, quay về 2 phiếu chờ duyệt (không chuyển sang danh sách thường)'])
    S1.add('Tham số lối vào trên thanh địa chỉ bị sửa thành giá trị lạ', 'P1', [ACC_B, DATA],
           [MENU_CD, 'Sửa phần tham số lối vào trên thanh địa chỉ thành chữ "abc", nhấn Enter.'], 'Tham số: abc',
           ['Không lỗi trang', 'Màn quay về lối vào danh sách thường (tiêu đề "%s", 2 phiếu)' % LIST_TITLE, 'Không lộ thêm phiếu nào ngoài phạm vi của B'])
    S1.add('Các nút chức năng của danh sách', 'P1', ACC_A, [MENU], '—',
           ['Khối lọc: ô tìm "Tìm theo số phiếu", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao',
            'Bảng: nút Tạo mới, Xuất Excel, Cấu hình cột hiển thị (biểu tượng cột)', 'KHÔNG có nút Xóa, Import'])
    S1.add('Nút Tạo mới ẩn khi không có quyền tạo', 'P0', ACC_N, [MENU], '—', ['Không có nút Tạo mới', 'Vẫn có Xuất Excel, Cấu hình cột hiển thị'])
    S1.add('Cột mặc định hiển thị', 'P0', ACC_A, [MENU], '—',
           ['Cột theo thứ tự: STT, Số phiếu, Công ty, Năm, Người tạo, Ngày tạo, Người duyệt, Trạng thái, Hành động',
            'Cột STT và Số phiếu ghim trái khi cuộn ngang'])
    S1.add('Cột ẩn mặc định', 'P1', ACC_A, [MENU, 'Bấm Cấu hình cột hiển thị.'], '—', ['Chỉ cột Ngày duyệt đang bỏ chọn', 'Bật lên thì cột hiện ngày duyệt dạng dd/mm/yyyy'])
    S1.add('Dữ liệu dòng khớp phiếu đã lập', 'P0', [ACC_A, PLAN_M], [MENU, 'Tìm dòng %s.' % M], '—',
           ['Số phiếu %s, Công ty TPE, Năm 2027' % M, 'Người tạo Nguyễn Văn A, Ngày tạo 12/11/2026', 'Người duyệt trống, Trạng thái Đang tạo'])
    S1.add('Người duyệt / Ngày duyệt của phiếu đã duyệt', 'P1', [ACC_A, APPR], [MENU, 'Bật cột Ngày duyệt.', 'Tìm dòng %s.' % P3], '—',
           ['Người duyệt Trần Văn B, Ngày duyệt 05/01/2026', 'Phiếu chưa duyệt để trống 2 cột này (không in dấu gạch)'])
    S1.add('Trạng thái và màu nhãn', 'P1', [ACC_A, DATA], [MENU], '—',
           ['Đang tạo màu xám, Chờ duyệt màu cam, Đã duyệt màu xanh lá, Hủy màu đỏ', 'Chỉ có 4 trạng thái này (không có trạng thái Từ chối riêng)'])
    S1.add('Phiếu Đang tạo của người khác không hiện', 'P0', [ACC_V4, DATA], [MENU, 'Tìm "%s" và "%s".' % (M, P5)], '—',
           ['Không thấy %s, %s dù V4 xem được mọi công ty' % (M, P5), 'Phiếu Đang tạo chỉ người lập thấy'])
    S1.add('Danh sách chưa có dữ liệu', 'P1', ACC_N, [MENU], '—', ['Bảng hiện %s' % EMPTY, 'Không lỗi trang'])
    S1.add('Không có dữ liệu khớp bộ lọc', 'P1', [ACC_A, DATA], [MENU, ADV, 'Chọn Năm 2023, bấm Tìm kiếm.'], 'Năm: 2023',
           ['Bảng hiện %s' % EMPTY, 'Tổng số bằng 0'])
    S1.add('Phân trang mặc định 10 dòng', 'P1', 'Tài khoản V4 (quyền %s mức Tổng công ty), thấy 25 phiếu.' % QV, [MENU], '—',
           ['Trang 1 có 10 dòng, dòng tổng ghi 1–10 trên 25 phiếu', 'Có 3 trang'])
    S1.add('Đổi số dòng / trang về trang 1', 'P1', 'Như trên, đang ở trang 2.', [MENU, 'Sang trang 2.', 'Đổi số dòng/trang thành 25.'], '25 dòng/trang',
           ['Về trang 1, hiện đủ 25 dòng, còn 1 trang'])
    S1.add('Trang trước / sau, đầu / cuối', 'P2', 'Như trên (25 phiếu, 10 dòng/trang).', [MENU, 'Bấm trang sau, trang cuối, trang trước, trang đầu.'], '—',
           ['Mỗi lần bấm đổi đúng trang', 'Ở trang 1 nút trang trước / trang đầu không bấm được; ở trang 3 nút trang sau / trang cuối không bấm được'])
    S1.add('STT liên tục giữa các trang', 'P2', 'Như trên.', [MENU, 'Sang trang 2.'], '—', ['Trang 2 có STT từ 11 tới 20'])
    S1.add('Sắp xếp mặc định theo Ngày tạo mới trước', 'P0', [ACC_A, DATA, 'Ngày tạo: %s 15/11/2026, %s 12/11/2026, %s 02/11/2026, %s 05/01/2026, %s 10/01/2025.' % (P2, M, P4, P3, P0)],
           [MENU], '—', ['Thứ tự: %s, %s, %s, %s, %s' % (P2, M, P4, P3, P0)])
    S1.add('Sắp xếp tăng / giảm theo cột', 'P1', [ACC_A, DATA], [MENU, 'Bấm tiêu đề cột Năm 2 lần.', 'Bấm tiêu đề cột Trạng thái.'], '—',
           ['Năm tăng dần (2025 đầu) rồi giảm dần (2028 đầu)', 'Các cột Số phiếu, Công ty, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái cũng sắp xếp được'])
    S1.add('Cột không hỗ trợ sắp xếp', 'P2', ACC_A, [MENU, 'Bấm tiêu đề cột STT, Hành động.'], '—', ['Không đổi thứ tự, không có biểu tượng sắp xếp'])
    S1.add('Giữ sắp xếp khi chuyển trang, về trang 1 khi đổi sắp xếp', 'P2', 'Tài khoản V4, 25 phiếu.',
           [MENU, 'Sắp Số phiếu tăng dần.', 'Sang trang 2.', 'Bấm sắp Số phiếu giảm dần.'], '—',
           ['Trang 2 vẫn theo Số phiếu tăng dần', 'Đổi sắp xếp thì về trang 1'])
    S1.add('Hành động ở dòng thay đổi theo trạng thái (người lập)', 'P0', [ACC_A, DATA], [MENU, 'Bấm biểu tượng ba chấm ở cột Hành động từng dòng.'], '—',
           ['%s (Đang tạo): biểu tượng Sửa; trong ba chấm có Xem, Gửi duyệt, Hủy phiếu, In, Xuất Excel, Lịch sử' % M,
            '%s (Chờ duyệt): Xem, Hủy phiếu, In, Xuất Excel, Lịch sử (không có Sửa, Gửi duyệt)' % P2,
            '%s (Đã duyệt): Xem, In, Xuất Excel, Lịch sử' % P3, '%s (Hủy): chỉ Xem, Lịch sử' % P4])
    S1.add('Hành động ở dòng với người duyệt', 'P0', [ACC_B, DATA], [MENU, 'Bấm ba chấm dòng %s và %s.' % (P2, P3)], '—',
           ['%s (Chờ duyệt): Xem, Duyệt, In, Xuất Excel, Lịch sử' % P2, '%s (Đã duyệt): Xem, Hủy duyệt, In, Xuất Excel, Lịch sử' % P3,
            'Mục Duyệt ở danh sách chỉ mở màn Xem (duyệt / từ chối tại màn Xem)'])
    S1.add('Bấm số phiếu mở màn Xem', 'P1', ACC_A, [MENU, 'Bấm số phiếu %s.' % P2], '—',
           ['Mở màn "Chi tiết phiếu giao chỉ tiêu kinh doanh theo phòng ban: %s", nhãn trạng thái Chờ duyệt cạnh tiêu đề' % P2])

    # ======================================================================== II. TÌM KIẾM & LỌC
    S2 = Sec()
    S2.add('Tìm đúng số phiếu', 'P0', [ACC_A, DATA], [MENU, 'Gõ "%s", bấm Tìm kiếm.' % P2], 'Từ khoá: %s' % P2, ['Chỉ còn 1 dòng %s' % P2])
    S2.add('Tìm một phần số phiếu', 'P1', [ACC_A, DATA], [MENU, 'Gõ "2027", bấm Tìm kiếm.'], 'Từ khoá: 2027', ['Ra %s, %s (số phiếu chứa 2027)' % (M, P4)])
    S2.add('Không phân biệt hoa / thường', 'P2', [ACC_A, DATA], [MENU, 'Gõ "tpe_ctkd_2028", bấm Tìm kiếm.'], 'Từ khoá: tpe_ctkd_2028', ['Ra %s' % P2])
    S2.add('Ô tìm chỉ tìm theo số phiếu', 'P1', [ACC_A, DATA], [MENU, 'Gõ "Nguyễn Văn A", bấm Tìm kiếm.'], 'Từ khoá: Nguyễn Văn A',
           ['Bảng hiện %s (tìm theo người tạo dùng ô lọc Người tạo)' % EMPTY, 'Gợi ý trong ô ghi "Tìm theo số phiếu"'])
    S2.add('Từ khoá không tồn tại', 'P1', ACC_A, [MENU, 'Gõ "ZZZ999", bấm Tìm kiếm.'], 'Từ khoá: ZZZ999', ['Bảng hiện %s' % EMPTY])
    S2.add('Ký tự đặc biệt', 'P2', ACC_A, [MENU, 'Lần lượt tìm: %   _   \'   <b>'], "% ; _ ; ' ; <b>",
           ['Không lỗi trang, không treo', 'Tìm "_" không được ra toàn bộ danh sách (ra toàn bộ là lỗi, ghi nhận)'])
    S2.add('Khoảng trắng đầu / cuối', 'P2', [ACC_A, DATA], [MENU, 'Gõ "   %s   ", bấm Tìm kiếm.' % P2], 'Có 3 dấu cách hai đầu', ['Vẫn ra %s' % P2])
    S2.add('Từ khoá rất dài', 'P2', ACC_A, [MENU, 'Dán 300 ký tự vào ô tìm, bấm Tìm kiếm.'], '300 ký tự "a"', ['Không lỗi trang, ra danh sách rỗng'])
    S2.add('Xoá từ khoá', 'P2', [ACC_A, DATA], [MENU, 'Tìm "%s".' % P2, 'Xoá hết chữ trong ô tìm, bấm Tìm kiếm.'], '—', ['Quay về đủ 5 phiếu'])
    S2.add('Enter và nút Tìm kiếm', 'P1', [ACC_A, DATA], [MENU, 'Gõ "%s" rồi nhấn Enter.' % P2, 'Gõ lại rồi bấm nút Tìm kiếm.'], '—',
           ['Cả 2 cách đều ra 1 dòng %s' % P2])
    S2.add('Các ô lọc nâng cao', 'P0', ACC_A, [MENU, ADV], '—',
           ['Có 4 ô: Năm, Người tạo, Người duyệt, Trạng thái (nhãn nổi trên ô)', 'Không có ô Công ty (chỉ hiện với quyền %s mức Tổng công ty)' % QV,
            'Ô Năm có lựa chọn từ 2028 xuống 2023', 'Ô Trạng thái có 4 lựa chọn: Đang tạo, Chờ duyệt, Đã duyệt, Hủy'])
    S2.add('Lọc theo Năm', 'P0', [ACC_A, DATA], [MENU, ADV, 'Chọn Năm 2027.'], 'Năm: 2027', ['Còn %s (Đang tạo) và %s (Hủy)' % (M, P4)])
    S2.add('Lọc theo Trạng thái', 'P0', [ACC_A, DATA], [MENU, ADV, 'Chọn Trạng thái Hủy.'], 'Trạng thái: Hủy', ['Chỉ còn %s' % P4])
    S2.add('Lọc theo Người tạo / Người duyệt', 'P1', [ACC_V3, DATA], [MENU, ADV, 'Chọn Người tạo: Nguyễn Văn A.', 'Thêm Người duyệt: Trần Văn B.'], '—',
           ['Chỉ Người tạo: ra %s, %s, %s, %s' % (P0, P3, P4, P2), 'Thêm Người duyệt: chỉ còn %s' % P3])
    S2.add('Lọc theo Công ty (mức Tổng công ty)', 'P1', [ACC_V4, DATA], [MENU, ADV, 'Chọn Công ty TPSG.'], 'Công ty: TPSG',
           ['Có ô Công ty; chọn TPSG còn %s, %s' % (P6, P7), 'Công ty đã khoá mà còn phiếu thì vẫn có trong ô, có biểu tượng ổ khóa trước tên'])
    S2.add('Lọc kết hợp nhiều tiêu chí và từ khoá', 'P1', [ACC_V4, DATA], [MENU, ADV, 'Chọn Năm 2027, Trạng thái Chờ duyệt.', 'Gõ "TPSG", bấm Tìm kiếm.'],
           'Năm 2027; Chờ duyệt; từ khoá TPSG', ['Chỉ còn %s' % P6])
    S2.add('Tổng số và phân trang sau lọc', 'P1', 'Tài khoản V4, 25 phiếu, 12 phiếu Đã duyệt; đang ở trang 3.', [MENU, 'Sang trang 3.', ADV, 'Chọn Trạng thái Đã duyệt.'], '—',
           ['Về trang 1, tổng 12 phiếu, 2 trang', 'Sắp xếp đang chọn vẫn giữ sau khi lọc'])
    S2.add('Bấm Làm mới xoá điều kiện lọc', 'P1', [ACC_A, DATA], [MENU, ADV, 'Chọn Năm 2027, gõ "00015", bấm Tìm kiếm.', 'Bấm Làm mới.'], '—',
           ['Ô tìm và các ô lọc về trống', 'Danh sách về đủ 5 phiếu, trang 1'])
    S2.add('Giữ bộ lọc khi vào Xem rồi quay lại', 'P1', [ACC_A, DATA], [MENU, ADV, 'Chọn Năm 2027.', 'Bấm số phiếu %s, bấm Quay lại.' % M], '—',
           ['Danh sách vẫn lọc Năm 2027 (bộ lọc ghi nhớ 10 phút)', 'Lưu ý: nếu bộ lọc bị xoá về mặc định thì ghi nhận'])
    S2.add('Sang màn khác rồi quay lại / tải lại trang', 'P2', [ACC_A, DATA], [MENU, ADV, 'Chọn Năm 2027.', 'Nhấn F5.', 'Chọn lại Năm 2027, bấm 1 mục menu khác rồi mở lại màn.'], '—',
           ['Không lỗi trang', 'Sang màn khác rồi quay lại: bộ lọc về mặc định'])
    S2.add('Tab mới và tài khoản khác trên cùng trình duyệt', 'P2', [ACC_A, ACC_B], ['A lọc Năm 2027, bấm số phiếu %s.' % M, 'Mở tab mới vào màn danh sách.', 'Đăng xuất, đăng nhập B, mở màn.'], '—',
           ['B KHÔNG nhận bộ lọc Năm 2027 của A', 'Tab mới không lỗi trang'])

    # ======================================================================== III. THÊM MỚI
    S3 = Sec()
    S3.add('Mở form Tạo mới', 'P0', [ACC_A, FREE_2027], [MENU, NEW], '—',
           ['Tiêu đề trang "Tạo phiếu giao chỉ tiêu kinh doanh theo phòng ban"',
            'Khối "Thông tin phiếu": Số phiếu (khoá, gợi ý "Số phiếu tự sinh khi lưu"), Năm (dấu * đỏ), Khối kinh doanh (dấu * đỏ, chọn nhiều, gợi ý "Chọn khối kinh doanh")',
            'Khối "Chi tiết" hiện "Chưa có dữ liệu"', 'Chân trang: Lưu, Lưu và gửi, Quay lại',
            'KHÔNG có ô Công ty (công ty = công ty người lập), KHÔNG có Lưu nháp, Lưu và tiếp tục'])
    S3.add('Năm mặc định và danh sách năm', 'P0', ACC_A, [MENU, NEW, 'Mở ô Năm.'], '—',
           ['Năm mặc định "Năm 2026" (năm hiện tại)', 'Ô Năm có Năm 2025 tới Năm 2036', 'Không có nút xoá trống ô Năm'])
    S3.add('Ô Khối kinh doanh chỉ có khối của công ty', 'P1', [ACC_A, CAT, 'Công ty TPSG có khối "Kinh doanh miền Nam".'], [MENU, NEW, 'Mở ô Khối kinh doanh.'], '—',
           ['Có Kinh doanh, Nghiệp vụ (khối đang hoạt động của TPE)', 'Không có "Kinh doanh miền Nam" của TPSG, không có khối đã ngừng'])
    S3.add('Chọn khối thì sinh tab theo khối', 'P0', [ACC_A, CAT], [MENU, NEW, 'Chọn Khối kinh doanh: Nghiệp vụ, rồi Kinh doanh.'], 'Khối: Nghiệp vụ, Kinh doanh',
           ['Có 3 tab: Kinh doanh, Nghiệp vụ (theo thứ tự danh mục, không theo thứ tự chọn), Tổng hợp',
            'Tab đang mở là khối vừa thêm; mỗi tab khối có ô Khu vực (dấu * đỏ, gợi ý "Chọn khu vực")',
            'Bảng hiện "Chọn khu vực để thêm Tỉnh/TP"', 'Góc phải khối Chi tiết ghi "0 Tỉnh/TP · 0 phòng · 0 bộ phận"'])
    S3.add('Chọn vùng thì thêm các Tỉnh/TP của vùng', 'P0', [ACC_A, CAT], [MENU, NEW, 'Chọn khối Kinh doanh.', 'Ô Khu vực chọn "Đồng bằng sông Hồng".'], '—',
           ['Bảng có 3 dòng tỉnh STT La Mã: I Hà Nội (0 phòng), II Hải Phòng (0 phòng), III Bắc Ninh (0 phòng)',
            'Dưới mỗi tỉnh: dòng "Năm trước" chữ nghiêng (chỉ đọc), rồi 1 dòng phòng trống (ô "Chọn phòng ban" + biểu tượng thùng rác)',
            'Dòng phòng có liên kết "Thêm Phòng Ban" và "Chia Bộ Phận"', 'Dòng TỔNG ghim đầu bảng: "3 Tỉnh/TP · 0 phòng · 0 bộ phận"'])
    S3.add('Chọn thêm vùng không lặp tỉnh đã có', 'P1', [ACC_A, CAT], [MENU, NEW, 'Khối Kinh doanh chọn vùng Đồng bằng sông Hồng, nhập số cho Hà Nội.', 'Chọn thêm vùng Duyên hải miền Trung.'], '—',
           ['Thêm Đà Nẵng, Quảng Nam; Hà Nội giữ nguyên số đã nhập', 'Không có tỉnh nào bị lặp'])
    S3.add('Tiêu đề bảng 12 cột 3 tầng', 'P0', [ACC_A, CAT], [MENU, NEW, 'Chọn khối Kinh doanh, vùng Đồng bằng sông Hồng.'], '—',
           ['Cột trái: STT, "Tỉnh/TP / Phòng ban / Bộ phận" kèm ô chọn cấp hiển thị',
            'Tầng 1: Khách hãng, Khách khác, Tổng cộng (mỗi nhóm 4 cột)', 'Tầng 2: mỗi nhóm có Hàng hóa, Dịch vụ', 'Tầng 3: mỗi cặp có SL khách, Doanh số',
            'Nhóm Tổng cộng chỉ hiển thị (không có ô nhập)', 'KHÔNG có cột / nút khách hàng chi tiết'])
    S3.add('Ô chọn phòng chỉ có phòng thuộc khối', 'P0', [ACC_A, CAT, 'Phòng Kinh doanh 3 đã ngừng hoạt động.'], [MENU, NEW, 'Chọn khối Kinh doanh, vùng Đồng bằng sông Hồng.', 'Mở ô chọn phòng dòng Hà Nội.'], '—',
           ['Chỉ có Kinh doanh 1, Kinh doanh 2 (có ô tìm)', 'Không có Dự án 1 (khối Nghiệp vụ), không có Kinh doanh 3 (đã ngừng)'])
    S3.add('Phòng đã chọn bị loại khỏi dòng khác cùng tỉnh', 'P0', [ACC_A, CAT],
           [MENU, NEW, 'Khối Kinh doanh, vùng Đồng bằng sông Hồng; Hà Nội chọn Kinh doanh 1.', 'Bấm "Thêm Phòng Ban" ở Hà Nội, mở ô chọn phòng dòng mới.', 'Mở ô chọn phòng dòng Hải Phòng.'], '—',
           ['Dòng mới ở Hà Nội chỉ còn Kinh doanh 2', 'Hải Phòng vẫn chọn được Kinh doanh 1 (khác tỉnh)'])
    S3.add('Nhập số và cộng tổng tỉnh, tổng khối', 'P0', [ACC_A, CAT, FREE_2027, BEFORE_2026],
           [MENU, NEW, 'Chọn Năm 2027, khối Kinh doanh, vùng Đồng bằng sông Hồng.', 'Nhập 3 dòng phòng theo Test Data (chưa lưu).'], FULL_TD,
           ['Nhóm Tổng cộng dòng Kinh doanh 1 Hà Nội tự hiện: Hàng hóa 8 / 2,100,000,000, Dịch vụ 3 / 450,000,000',
            'Dòng Hà Nội: "Hà Nội (2 phòng)", Khách hãng Hàng hóa 9 / 2,700,000,000, Dịch vụ 3 / 500,000,000; Khách khác Hàng hóa 5 / 1,100,000,000, Dịch vụ 1 / 150,000,000; Tổng cộng Hàng hóa 14 / 3,800,000,000, Dịch vụ 4 / 650,000,000',
            'Dòng Hải Phòng: Khách hãng Hàng hóa 2 / 750,000,000, Khách khác Hàng hóa 1 / 250,000,000, Tổng cộng Hàng hóa 3 / 1,000,000,000',
            'Dòng TỔNG "3 Tỉnh/TP · 3 phòng · 0 bộ phận": Khách hãng Hàng hóa 11 / 3,450,000,000, Dịch vụ 3 / 500,000,000; Khách khác Hàng hóa 6 / 1,350,000,000, Dịch vụ 1 / 150,000,000; Tổng cộng Hàng hóa 17 / 4,800,000,000, Dịch vụ 4 / 650,000,000'])
    S3.add('Dòng Năm trước lấy từ phiếu năm trước Đã duyệt', 'P0', [ACC_A, FREE_2027, BEFORE_2026], [MENU, NEW, 'Chọn Năm 2027, khối Kinh doanh, vùng Đồng bằng sông Hồng.'], '—',
           ['Dòng Năm trước của Hà Nội: Khách hãng Hàng hóa 8 / 2,500,000,000, Dịch vụ 2 / 450,000,000; Khách khác Hàng hóa 4 / 950,000,000, Dịch vụ 1 / 150,000,000; Tổng cộng Hàng hóa 12 / 3,450,000,000, Dịch vụ 3 / 600,000,000',
            'Năm trước của Hải Phòng, Bắc Ninh để trống (phiếu 2026 không có)', 'Dòng Năm trước chỉ đọc, không cộng vào dòng tỉnh / dòng TỔNG'])
    S3.add('Năm trước theo đúng khối và đổi theo Năm', 'P1', [ACC_A, FREE_2027, BEFORE_2026, 'Phiếu 2026 khối Nghiệp vụ không có Hà Nội.'],
           [MENU, NEW, 'Chọn Năm 2027, khối Kinh doanh và Nghiệp vụ, mỗi khối chọn vùng Đồng bằng sông Hồng.', 'Xem dòng Năm trước Hà Nội ở 2 tab.', 'Đổi Năm sang 2029.'], '—',
           ['Tab Kinh doanh: Năm trước Hà Nội có số như phiếu 2026; tab Nghiệp vụ: trống', 'Đổi sang 2029: Năm trước trống hết (năm 2028 chưa có phiếu Đã duyệt)',
            'Đổi năm không hỏi xác nhận, số đã nhập giữ nguyên'])
    S3.add('Năm trước bỏ qua phiếu chưa duyệt', 'P1', [ACC_A, PEND], [MENU, NEW, 'Chọn Năm 2029, khối Kinh doanh, vùng Đồng bằng sông Hồng.'], '—',
           ['Dòng Năm trước trống (phiếu 2028 %s mới Chờ duyệt)' % P2, 'Phiếu Hủy / Đang tạo năm trước cũng không được lấy'])
    S3.add('Ô chọn Hiển thị đến cấp', 'P1', [ACC_A, PLAN_M, 'Phòng Kinh doanh 1 Hà Nội đã chia 2 bộ phận.'], OPEN_M + ['Ở tiêu đề cột cây lần lượt chọn "Chỉ Tỉnh/TP", "Đến Phòng ban", "Đến Bộ phận".'], '—',
           ['Mặc định "Đến Bộ phận": mở hết', '"Chỉ Tỉnh/TP": chỉ còn dòng tỉnh và dòng Năm trước', '"Đến Phòng ban": hiện dòng phòng, ẩn dòng bộ phận',
            'Ô chọn có đúng 3 lựa chọn Chỉ Tỉnh/TP, Đến Phòng ban, Đến Bộ phận'])
    S3.add('Thu / mở từng dòng bằng mũi tên', 'P2', [ACC_A, PLAN_M], OPEN_M + ['Bấm mũi tên ở dòng Hà Nội 2 lần.'], '—',
           ['Lần 1: Hà Nội thu gọn (gợi ý "Mở rộng"), dòng TỔNG không đổi', 'Lần 2: mở lại (gợi ý "Thu gọn")'])
    S3.add('Thêm dòng phòng', 'P1', [ACC_A, CAT], [MENU, NEW, 'Khối Kinh doanh, vùng Đồng bằng sông Hồng.', 'Bấm "Thêm Phòng Ban" ở Hà Nội 2 lần.'], '—',
           ['Hà Nội có 3 dòng phòng STT 1, 2, 3', 'Liên kết "Thêm Phòng Ban" chỉ hiện ở dòng phòng cuối của tỉnh'])
    S3.add('Xoá dòng phòng đã có số thì hỏi', 'P0', [ACC_A, CAT], [MENU, NEW, 'Hà Nội có 2 dòng phòng, dòng Kinh doanh 1 có số.', 'Bấm thùng rác (Xoá dòng) ở Kinh doanh 1, bấm Hủy.', 'Bấm lại, chọn Xoá.'], '—',
           ['Hộp "Xoá dòng phòng" nội dung "Xoá dòng Kinh doanh 1 tại Hà Nội? Số liệu của dòng sẽ mất.", nút Hủy / Xoá',
            'Hủy: dòng còn nguyên', 'Xoá: dòng mất, dòng tỉnh và dòng TỔNG trừ số tương ứng'])
    S3.add('Xoá dòng phòng chưa có số không hỏi', 'P2', [ACC_A, CAT], [MENU, NEW, 'Hà Nội thêm 1 dòng, chọn Kinh doanh 2, không nhập số.', 'Bấm Xoá dòng.'], '—',
           ['Dòng mất ngay, không hiện hộp xác nhận'])
    S3.add('Dòng phòng cuối của tỉnh chỉ làm trống', 'P0', [ACC_A, CAT], [MENU, NEW, 'Hải Phòng chỉ có 1 dòng Kinh doanh 1 có số.', 'Bấm Xoá dòng, chọn Xoá.'], '—',
           ['Hỏi xác nhận như trên', 'Dòng KHÔNG mất mà về trống (ô "Chọn phòng ban", 8 ô số trống)', 'Tỉnh Hải Phòng vẫn còn trong bảng'])
    S3.add('Chia Bộ Phận chuyển số sang bộ phận đầu', 'P0', [ACC_A, CAT], [MENU, NEW, 'Hà Nội chọn Kinh doanh 1, nhập Khách hãng Hàng hóa 5 / 1,500,000,000.', 'Bấm "Chia Bộ Phận".'], '—',
           ['Dưới dòng phòng có dòng bộ phận STT "1.1" thụt lề, ô "Chọn bộ phận", mang sẵn 5 / 1,500,000,000',
            'Dòng phòng thành chỉ đọc, bằng tổng các bộ phận (5 / 1,500,000,000)', 'Liên kết đổi thành "Thêm Bộ Phận"', 'Dòng tỉnh, dòng TỔNG không đổi'])
    S3.add('Chia Bộ Phận khi chưa chọn phòng', 'P1', [ACC_A, CAT], [MENU, NEW, 'Dòng phòng Hà Nội chưa chọn phòng.', 'Rê chuột và bấm "Chia Bộ Phận".'], '—',
           ['Liên kết màu xám, gợi ý "Chọn phòng trước"', 'Bấm không có tác dụng'])
    S3.add('Chia Bộ Phận khi phòng không có bộ phận', 'P2', [ACC_A, CAT, 'Phòng Kinh doanh 2 không có bộ phận nào trong danh mục.'], [MENU, NEW, 'Hà Nội chọn Kinh doanh 2, bấm "Chia Bộ Phận".'], '—',
           ['Báo "Phòng chưa có bộ phận trong danh mục"', 'Dòng phòng giữ nguyên, vẫn nhập thẳng số'])
    S3.add('Thêm bộ phận và cộng tổng phòng', 'P0', [ACC_A, CAT], [MENU, NEW, 'Kinh doanh 1 Hà Nội đã chia, dòng 1.1 chọn Nhóm KD1-1, sửa thành 3 / 900,000,000.', 'Bấm "Thêm Bộ Phận", dòng 1.2 chọn Nhóm KD1-2, nhập 2 / 600,000,000.'],
           ['Nhóm KD1-1: Khách hãng Hàng hóa 3 / 900,000,000', 'Nhóm KD1-2: Khách hãng Hàng hóa 2 / 600,000,000'],
           ['Dòng phòng Kinh doanh 1 = 5 / 1,500,000,000 (tổng 2 bộ phận)', 'Dòng 1.2 chỉ chọn được Nhóm KD1-2 (không trùng bộ phận trong cùng phòng)',
            'Hết bộ phận: "Thêm Bộ Phận" màu xám, gợi ý "Đã chia hết bộ phận của phòng"', 'Góc phải khối Chi tiết đếm "2 bộ phận"'])
    S3.add('Xoá bộ phận có số thì hỏi', 'P1', [ACC_A, CAT, 'Kinh doanh 1 Hà Nội có 2 bộ phận như trên.'], [MENU, NEW, 'Bấm thùng rác (Xoá bộ phận) ở Nhóm KD1-2, chọn Xoá.'], '—',
           ['Hộp "Xoá bộ phận" nội dung "Xoá dòng Nhóm KD1-2 của Kinh doanh 1? Số liệu của dòng sẽ mất.", nút Hủy / Xoá',
            'Xoá: dòng phòng còn 3 / 900,000,000'])
    S3.add('Xoá bộ phận cuối thì phòng nhập thẳng lại', 'P0', [ACC_A, CAT, 'Kinh doanh 1 Hà Nội chỉ còn bộ phận Nhóm KD1-1 (3 / 900,000,000).'], [MENU, NEW, 'Bấm Xoá bộ phận ở Nhóm KD1-1.'], '—',
           ['Không hỏi xác nhận', 'Dòng bộ phận mất, dòng phòng nhập thẳng lại và nhận số 3 / 900,000,000', 'Liên kết trở lại "Chia Bộ Phận"'])
    S3.add('Đổi phòng khi đã chia bộ phận thì hỏi', 'P0', [ACC_A, CAT, 'Kinh doanh 1 Hà Nội chia 2 bộ phận, tổng 5 / 1,500,000,000.'],
           [MENU, NEW, 'Đổi phòng dòng đó sang Kinh doanh 2, bấm Hủy.', 'Đổi lại sang Kinh doanh 2, bấm Đồng ý.'], '—',
           ['Hộp "Đổi phòng" nội dung "Đổi phòng? Các bộ phận đã chia sẽ bị bỏ.", nút Hủy / Đồng ý', 'Hủy: ô phòng về Kinh doanh 1, bộ phận còn nguyên',
            'Đồng ý: bỏ 2 dòng bộ phận, dòng phòng thành Kinh doanh 2 và giữ số tổng 5 / 1,500,000,000 (nhập thẳng được)'])
    S3.add('Bỏ vùng có số liệu thì hỏi', 'P0', [ACC_A, CAT], [MENU, NEW, 'Khối Kinh doanh chọn 2 vùng; Hà Nội và Hải Phòng có số.', 'Bỏ vùng Đồng bằng sông Hồng, bấm Hủy.', 'Bỏ lại, bấm Bỏ vùng.'], '—',
           ['Hộp "Bỏ khu vực" nội dung "Bỏ vùng Đồng bằng sông Hồng? 2 Tỉnh/TP có số liệu sẽ bị xoá.", nút Hủy / Bỏ vùng',
            'Hủy: vùng vẫn được chọn, số còn nguyên', 'Bỏ vùng: mất Hà Nội, Hải Phòng, Bắc Ninh; còn Đà Nẵng, Quảng Nam'])
    S3.add('Bỏ vùng chưa có số không hỏi', 'P2', [ACC_A, CAT], [MENU, NEW, 'Khối Kinh doanh chọn vùng Duyên hải miền Trung, chưa nhập số.', 'Bỏ vùng đó.'], '—',
           ['Đà Nẵng, Quảng Nam mất ngay, không hỏi'])
    S3.add('Bỏ khối có số liệu thì hỏi', 'P0', [ACC_A, CAT], [MENU, NEW, 'Chọn 2 khối, khối Nghiệp vụ có số ở Hà Nội.', 'Bỏ khối Nghiệp vụ khỏi ô Khối kinh doanh, bấm Hủy.', 'Bỏ lại, bấm Bỏ khối.'], '—',
           ['Hộp "Bỏ khối kinh doanh" nội dung "Bỏ khối Nghiệp vụ? Số liệu đã nhập của khối sẽ mất.", nút Hủy / Bỏ khối',
            'Hủy: khối còn nguyên', 'Bỏ khối: tab Nghiệp vụ mất, tab Tổng hợp không còn số của khối đó'])
    S3.add('Tab Tổng hợp cộng các khối theo tỉnh', 'P0', [ACC_A, CAT, BEFORE_2026],
           [MENU, NEW, 'Năm 2027; khối Kinh doanh nhập theo Test Data; khối Nghiệp vụ vùng Đồng bằng sông Hồng, Hà Nội chọn Dự án 1: Khách hãng Hàng hóa 2 / 800,000,000.', 'Bấm tab Tổng hợp.'],
           FULL_TD, ['Bảng chỉ đọc, cột cây "Tỉnh/TP / Khối"',
                     'Dòng TỔNG "TỔNG CỘNG" ghim đầu: Khách hãng Hàng hóa 13 / 4,250,000,000',
                     'Hà Nội (I): Khách hãng Hàng hóa 11 / 3,500,000,000; dưới có dòng Năm trước (số phiếu 2026), dòng 1 Kinh doanh 9 / 2,700,000,000, dòng 2 Nghiệp vụ 2 / 800,000,000',
                     'Các tỉnh xếp theo thứ tự danh mục Tỉnh/TP, mỗi tỉnh 1 lần dù có ở nhiều khối'])
    S3.add('Lưu phiếu đầy đủ hợp lệ', 'P0', [ACC_A, CAT, FREE_2027], [MENU, NEW, 'Chọn Năm 2027, khối Kinh doanh, vùng Đồng bằng sông Hồng, nhập theo Test Data.', 'Bấm Lưu.'], FULL_TD,
           ['Báo "Đã lưu TPE_CTKD_2027.xxxxx", quay về danh sách', 'Phiếu mới ở đầu danh sách, trạng thái Đang tạo, Năm 2027, Người tạo Nguyễn Văn A',
            'Số phiếu dạng <mã công ty>_CTKD_<năm>.<số thứ tự 5 chữ số>'])
    S3.add('Dữ liệu sau lưu khớp số đã nhập', 'P0', [ACC_A, 'Vừa lưu phiếu ở ca trên.'], [MENU, 'Bấm số phiếu vừa lưu.'], '—',
           ['Năm 2027, Khối Kinh doanh, Khu vực Đồng bằng sông Hồng', 'Đủ 3 dòng phòng với đúng số đã nhập, dòng TỔNG như lúc nhập',
            'Bắc Ninh còn trong bảng với "(0 phòng)"', 'Năm trước Hà Nội như phiếu 2026'])
    S3.add('Chỉ chọn trường bắt buộc rồi lưu', 'P1', [ACC_A, CAT, FREE_2027], [MENU, NEW, 'Chọn Năm 2027, khối Kinh doanh, vùng Đồng bằng sông Hồng, không chọn phòng, không nhập số.', 'Bấm Lưu.'], '—',
           ['Lưu được (Đang tạo)', 'Dòng phòng trống bị bỏ khi lưu, không báo lỗi', 'Chỉ bị chặn khi gửi duyệt (xem nhóm Gửi duyệt)'])
    S3.add('Bỏ trống Khối kinh doanh', 'P0', [ACC_A, FREE_2027], [MENU, NEW, 'Chọn Năm 2027, không chọn khối.', 'Bấm Lưu.'], '—',
           ['Báo %s' % CHECK, 'Ô Khối kinh doanh viền đỏ, chữ đỏ %s ngay dưới' % REQ, 'Không lưu, vẫn ở form'])
    S3.add('Bỏ trống Khu vực của khối', 'P0', [ACC_A, CAT, FREE_2027], [MENU, NEW, 'Chọn Năm 2027, 2 khối Kinh doanh, Nghiệp vụ; chỉ khối Kinh doanh chọn vùng.', 'Đang ở tab Kinh doanh, bấm Lưu.'], '—',
           ['Báo %s' % CHECK, 'Tab Nghiệp vụ có chấm đỏ báo lỗi, màn tự chuyển sang tab Nghiệp vụ', 'Ô Khu vực của khối Nghiệp vụ đỏ %s' % REQ,
            'Lưu nháp cũng bắt buộc Năm, Khối, Khu vực'])
    S3.add('Có số mà chưa chọn phòng', 'P0', [ACC_A, CAT, FREE_2027], [MENU, NEW, 'Năm 2027, khối Kinh doanh, vùng Đồng bằng sông Hồng; dòng Hà Nội không chọn phòng, nhập Khách hãng Hàng hóa 5 / 1,500,000,000.', 'Bấm Lưu.'], '—',
           ['Báo %s' % CHECK, 'Ô chọn phòng dòng đó viền đỏ, chữ đỏ %s ngay dưới' % REQ, 'Không lưu, số đã nhập còn nguyên'])
    S3.add('Bộ phận có số mà chưa chọn bộ phận', 'P1', [ACC_A, CAT, FREE_2027], [MENU, NEW, 'Kinh doanh 1 Hà Nội chia bộ phận; dòng 1.2 không chọn bộ phận, nhập 2 / 600,000,000.', 'Bấm Lưu.'], '—',
           ['Ô "Chọn bộ phận" dòng 1.2 đỏ %s' % REQ, 'Không lưu'])
    S3.add('Lưu không kiểm cặp SL khách / Doanh số', 'P1', [ACC_A, CAT, FREE_2027], [MENU, NEW, 'Hà Nội chọn Kinh doanh 1, chỉ nhập Khách hãng Hàng hóa SL khách 5 (bỏ trống Doanh số).', 'Bấm Lưu.'], 'SL khách: 5',
           ['Lưu được (Đang tạo)', 'Cặp SL khách / Doanh số chỉ kiểm khi gửi duyệt'])
    S3.add('Ô số không nhận số âm và chữ', 'P1', [ACC_A, CAT], [MENU, NEW, 'Hà Nội chọn Kinh doanh 1, gõ lần lượt vào ô SL khách: -5, abc.'], '-5; abc',
           ['Gõ -5: dấu trừ không nhận, ô hiện 5', 'Gõ abc: ô không nhận chữ'])
    S3.add('Ô số không có phần thập phân', 'P1', [ACC_A, CAT], [MENU, NEW, 'Gõ 2.5 vào ô Doanh số.'], '2.5',
           ['Dấu chấm không được nhận làm phần thập phân, ô chỉ chứa số nguyên', 'Lưu ý: ghi rõ ô hiện gì (25 hay 2) vào KQ thực tế để đối chiếu'])
    S3.add('Hiển thị và dán số có dấu ngăn nghìn', 'P1', [ACC_A, CAT], [MENU, NEW, 'Gõ 1500000000 vào ô Doanh số.', 'Dán "1,234" vào ô SL khách khác.', 'Dán "1.234" vào ô SL khách khác nữa.'],
           ['1500000000', '1,234', '1.234'], ['Ô hiện 1,500,000,000', 'Dán "1,234" và "1.234" đều thành 1,234', 'Dòng tỉnh, dòng TỔNG cũng hiện dạng 1,234,567'])
    S3.add('Ô số vượt 13 chữ số', 'P0', [ACC_A, CAT, FREE_2027], [MENU, NEW, 'Hà Nội chọn Kinh doanh 1; ô Khách hãng Hàng hóa SL khách 1, Doanh số gõ 14 chữ số.', 'Bấm Lưu.', 'Sửa Doanh số thành 13 chữ số 9999999999999, bấm Lưu.'],
           ['12345678901234', '9999999999999'], ['Lần 1: ô Doanh số đỏ %s ngay dưới ô, không lưu, số đã gõ giữ nguyên' % MAXV, 'Lần 2: lưu được, ô hiện 9,999,999,999,999'])
    S3.add('Ô số 0 và ô trống', 'P2', [ACC_A, CAT], [MENU, NEW, 'Hà Nội chọn Kinh doanh 1, gõ 0 vào Khách hãng Hàng hóa SL khách, các ô khác để trống.'], '0',
           ['Ở dòng phòng, ô bằng 0 / trống hiển thị trống (không in 0, không in dấu gạch)', 'Dòng tỉnh và dòng TỔNG hiện 0 ở cột không có số'])
    S3.add('Lỗi đỏ biến mất khi sửa đúng', 'P1', [ACC_A, CAT, FREE_2027], [MENU, NEW, 'Tạo lỗi có số mà chưa chọn phòng, bấm Lưu.', 'Chọn phòng Kinh doanh 1 cho dòng đó.'], '—',
           ['Chữ đỏ dưới ô phòng mất ngay khi chọn', 'Bấm Lưu lại thì lưu được'])
    S3.add('Lỗi ở tab khác và nhánh đang thu gọn', 'P1', [ACC_A, CAT, FREE_2027],
           [MENU, NEW, 'Chọn 2 khối; ở tab Nghiệp vụ dòng Hà Nội nhập số nhưng không chọn phòng.', 'Thu gọn Hà Nội ở tab Nghiệp vụ, chuyển sang tab Tổng hợp.', 'Bấm Lưu.'], '—',
           ['Tab Nghiệp vụ có chấm đỏ', 'Tự chuyển về tab Nghiệp vụ, Hà Nội tự mở ra, cuộn tới ô lỗi đầu tiên'])
    S3.add('Trùng phiếu cùng công ty cùng năm', 'P0', [ACC_A, DATA], [MENU, NEW, 'Chọn Năm 2027, khối Kinh doanh, vùng Đồng bằng sông Hồng.', 'Bấm Lưu.'], 'Năm 2027',
           ['Ô Năm đỏ, chữ đỏ ngay dưới: "Công ty đã có phiếu %s (Đang tạo) cho năm 2027"' % M, 'Không tạo phiếu mới'])
    S3.add('Trùng với phiếu Chờ duyệt / Đã duyệt', 'P1', [ACC_A, DATA], [MENU, NEW, 'Chọn Năm 2028, khối, vùng, bấm Lưu.', 'Đổi Năm 2026, bấm Lưu.'], '—',
           ['Năm 2028: "Công ty đã có phiếu %s (Chờ duyệt) cho năm 2028"' % P2, 'Năm 2026: "Công ty đã có phiếu %s (Đã duyệt) cho năm 2026"' % P3])
    S3.add('Phiếu Hủy không tính trùng', 'P0', [ACC_A, FREE_2027], [MENU, NEW, 'Chọn Năm 2027, khối Kinh doanh, vùng Đồng bằng sông Hồng, nhập 1 dòng hợp lệ.', 'Bấm Lưu.'], '—',
           ['Lưu được dù đã có %s năm 2027 (trạng thái Hủy)' % P4])
    S3.add('Công ty khác cùng năm không tính trùng', 'P1', [ACC_A, FREE_2027, 'Công ty TPSG đã có %s năm 2027.' % P6], [MENU, NEW, 'Lập phiếu năm 2027 hợp lệ, bấm Lưu.'], '—',
           ['Lưu được, mỗi công ty mỗi năm 1 phiếu'])
    S3.add('Quay lại khi chưa nhập gì', 'P1', ACC_A, [MENU, NEW, 'Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi'])
    S3.add('Quay lại khi đã nhập', 'P0', [ACC_A, CAT], [MENU, NEW, 'Chọn khối Kinh doanh, vùng, nhập 1 dòng.', 'Bấm Quay lại, chọn Ở lại.', 'Bấm Quay lại, chọn Thoát.'], '—',
           ['Hiện %s' % UNSAVED, 'Ở lại: dữ liệu còn nguyên', 'Thoát: về danh sách, không có phiếu mới'])
    S3.add('Rời trang bằng menu khi đã nhập', 'P1', [ACC_A, CAT], [MENU, NEW, 'Chọn khối Kinh doanh.', 'Bấm 1 mục menu khác.'], '—', ['Hiện hộp "Thông tin chưa lưu" như trên'])
    S3.add('Nhập rồi xoá hết', 'P2', [ACC_A, CAT], [MENU, NEW, 'Chọn khối Kinh doanh rồi bỏ chọn khối.', 'Bấm Quay lại.'], '—', ['Không hiện hộp hỏi (form về như ban đầu)'])
    S3.add('Bấm Lưu liên tục', 'P1', [ACC_A, FREE_2027], [MENU, NEW, 'Nhập phiếu năm 2027 hợp lệ.', 'Bấm Lưu 3 lần thật nhanh.'], '—', ['Chỉ tạo 1 phiếu, không báo trùng với chính nó'])
    S3.add('Hai thẻ cùng lập phiếu cùng năm', 'P1', [ACC_A, FREE_2027], ['Mở 2 thẻ, mỗi thẻ %s' % MENU, 'Cả 2 thẻ bấm Tạo mới, nhập phiếu năm 2027.', 'Thẻ 1 bấm Lưu, rồi thẻ 2 bấm Lưu.'], '—',
           ['Thẻ 1 lưu được', 'Thẻ 2 báo dưới ô Năm "Công ty đã có phiếu <số phiếu thẻ 1> (Đang tạo) cho năm 2027", không tạo phiếu thứ 2'])

    # ======================================================================== IV. CHỈNH SỬA
    S4 = Sec()
    S4.add('Mở Sửa từ danh sách, dữ liệu điền đúng', 'P0', [ACC_A, PLAN_M], OPEN_M, '—',
           ['Tiêu đề "Sửa phiếu giao chỉ tiêu kinh doanh theo phòng ban: %s"' % M, 'Số phiếu %s (khoá), Năm 2027, Khối Kinh doanh, Khu vực Đồng bằng sông Hồng' % M,
            'Đủ 3 dòng phòng đúng số đã lưu; Bắc Ninh có 1 dòng phòng trống', 'Chân trang: Lưu, Lưu và gửi, Quay lại'])
    S4.add('Mở Sửa từ màn Xem', 'P1', [ACC_A, PLAN_M], [MENU, 'Bấm số phiếu %s.' % M, 'Bấm Sửa.'], '—', ['Mở màn Sửa của %s' % M])
    S4.add('Sửa số một dòng', 'P0', [ACC_A, PLAN_M], OPEN_M + ['Đổi Khách hãng Hàng hóa Doanh số dòng Kinh doanh 1 Hà Nội từ 1,500,000,000 thành 1,800,000,000.', 'Bấm Lưu.'], '—',
           ['Báo "Đã lưu %s", về danh sách' % M, 'Mở Xem: dòng Hà Nội Khách hãng Hàng hóa thành 3,000,000,000, dòng TỔNG 3,750,000,000', 'Trạng thái vẫn Đang tạo'])
    S4.add('Sửa nhiều chỗ: thêm khối, thêm tỉnh, xoá phòng', 'P1', [ACC_A, PLAN_M],
           OPEN_M + ['Xoá dòng Kinh doanh 2 Hà Nội (chọn Xoá).', 'Thêm khối Nghiệp vụ, vùng Đồng bằng sông Hồng, Hà Nội chọn Dự án 1: 2 / 800,000,000.', 'Bấm Lưu, mở Xem.'], '—',
           ['Có 2 tab khối + Tổng hợp', 'Hà Nội khối Kinh doanh chỉ còn Kinh doanh 1', 'Tổng hợp cộng đúng theo dòng còn lại'])
    S4.add('Đổi Năm khi sửa thì số phiếu đổi theo năm', 'P1', [ACC_A, PLAN_M], OPEN_M + ['Chọn Năm 2030.', 'Bấm Lưu.'], 'Năm 2030',
           ['Lưu được', 'Số phiếu thành TPE_CTKD_2030.00015 (giữ số thứ tự, đổi năm)', 'Năm trước tính lại theo năm 2029'])
    S4.add('Đổi Năm sang năm đã có phiếu', 'P1', [ACC_A, PLAN_M, PEND], OPEN_M + ['Chọn Năm 2028, bấm Lưu.'], 'Năm 2028',
           ['Ô Năm đỏ "Công ty đã có phiếu %s (Chờ duyệt) cho năm 2028"' % P2, 'Phiếu M giữ năm 2027'])
    S4.add('Bỏ trống bắt buộc khi sửa', 'P0', [ACC_A, PLAN_M], OPEN_M + ['Bỏ hết vùng ở ô Khu vực (xác nhận Bỏ vùng).', 'Bấm Lưu.'], '—',
           ['Ô Khu vực đỏ %s, báo %s' % (REQ, CHECK), 'Không lưu, phiếu giữ số cũ'])
    S4.add('Quay lại khi đã đổi', 'P1', [ACC_A, PLAN_M], OPEN_M + ['Đổi 1 số.', 'Bấm Quay lại, chọn Ở lại.', 'Bấm Quay lại, chọn Thoát.'], '—',
           ['Hiện %s' % UNSAVED, 'Thoát: phiếu không đổi'])
    S4.add('Mở Sửa không đổi gì rồi quay lại', 'P2', [ACC_A, PLAN_M], OPEN_M + ['Bấm Quay lại.'], '—', ['Về ngay, không hỏi'])
    S4.add('Đổi rồi trả về giá trị ban đầu', 'P2', [ACC_A, PLAN_M], OPEN_M + ['Đổi SL khách rồi gõ lại số cũ.', 'Bấm Quay lại.'], '—', ['Không hiện hộp hỏi'])
    S4.add('Mở Sửa phiếu không còn Đang tạo', 'P0', [ACC_A, PEND], ['Mở lại màn Sửa của %s từ trang đã đánh dấu trong trình duyệt.' % P2], '—',
           ['Tự chuyển sang màn Xem của %s, không có ô nhập' % P2])
    S4.add('Phiếu vừa được gửi duyệt ở thẻ khác', 'P0', [ACC_A, PLAN_M], ['Thẻ 1: mở Sửa %s.' % M, 'Thẻ 2: Gửi duyệt %s.' % M, 'Thẻ 1: đổi số, bấm Lưu.'], '—',
           ['Thẻ 1 báo %s' % LOCKED, 'Phiếu giữ nguyên số liệu lúc gửi'])
    S4.add('Phiếu bị Hủy ở thẻ khác', 'P1', [ACC_A, PLAN_M], ['Thẻ 1: mở Sửa %s.' % M, 'Thẻ 2: Hủy phiếu %s.' % M, 'Thẻ 1: bấm Lưu.'], '—', ['Thẻ 1 báo %s' % LOCKED])
    S4.add('Hai thẻ cùng sửa', 'P2', [ACC_A, PLAN_M], ['Thẻ 1 và 2 cùng mở Sửa %s.' % M, 'Thẻ 1 đổi số Hà Nội, Lưu.', 'Thẻ 2 đổi số Hải Phòng, Lưu.'], '—',
           ['Lưu sau ghi đè lưu trước: Hà Nội về số cũ, Hải Phòng theo thẻ 2'])
    S4.add('Phòng đã ngừng hoạt động vẫn hiện khi sửa', 'P1', [ACC_A, PLAN_M, 'Sau khi lập M, phòng Kinh doanh 2 bị chuyển sang ngừng hoạt động.'],
           OPEN_M + ['Mở ô chọn phòng dòng Kinh doanh 2; mở ô chọn phòng của 1 dòng mới.', 'Bấm Lưu.'], '—',
           ['Dòng cũ vẫn hiện đúng tên Kinh doanh 2 và lưu lại được', 'Dòng mới không có Kinh doanh 2'])
    S4.add('Phiếu bị từ chối về Đang tạo sửa được', 'P0', [ACC_A, 'Phiếu %s bị B từ chối, lý do "Thiếu Bắc Ninh".' % M], [MENU, 'Mở Xem %s.' % M, 'Bấm Sửa, nhập thêm dòng Bắc Ninh, Lưu.'], '—',
           ['Màn Xem có dòng "Lý do từ chối: Thiếu Bắc Ninh"', 'Có nút Sửa, Gửi duyệt, Hủy phiếu', 'Sửa và lưu được'])

    # ======================================================================== V. GỬI DUYỆT
    S5 = Sec()
    S5.add('Điều kiện hiện nút Gửi duyệt', 'P0', [ACC_A, DATA], [MENU, 'Mở ba chấm dòng %s, %s.' % (M, P2), 'Mở Xem %s.' % M], '—',
           ['Chỉ phiếu Đang tạo do chính mình lập (và có quyền %s) có Gửi duyệt, ở dòng và ở chân màn Xem' % QC, '%s (Chờ duyệt) không có' % P2])
    S5.add('Hộp xác nhận gửi duyệt', 'P1', [ACC_A, PLAN_M], [MENU, 'Ở dòng %s bấm ba chấm > Gửi duyệt.' % M], '—',
           ['Hộp "Gửi duyệt" nội dung "Gửi duyệt phiếu %s?", nút Hủy / Gửi duyệt' % M])
    S5.add('Gửi duyệt thành công', 'P0', [ACC_A, PLAN_M, ACC_B], [MENU, 'Ở dòng %s bấm Gửi duyệt > Gửi duyệt.' % M], '—',
           ['Báo "Đã gửi duyệt %s"' % M, 'Trạng thái Chờ duyệt (màu cam)', 'Hết Sửa, Gửi duyệt; còn Hủy phiếu', 'B thấy %s ở lối vào "Giao chỉ tiêu chờ duyệt"' % M])
    S5.add('Bấm Hủy ở hộp xác nhận', 'P1', [ACC_A, PLAN_M], [MENU, 'Bấm Gửi duyệt ở dòng %s, chọn Hủy.' % M], '—', ['Phiếu vẫn Đang tạo, không có thông báo nào'])
    S5.add('Lưu và gửi từ form Tạo mới', 'P0', [ACC_A, CAT, FREE_2027], [MENU, NEW, 'Nhập phiếu 2027 theo Test Data.', 'Bấm Lưu và gửi.'], FULL_TD,
           ['Báo "Đã gửi duyệt TPE_CTKD_2027.xxxxx", về danh sách', 'Phiếu mới ở trạng thái Chờ duyệt'])
    S5.add('Lưu và gửi từ form Sửa', 'P0', [ACC_A, PLAN_M], OPEN_M + ['Đổi 1 số.', 'Bấm Lưu và gửi.'], '—', ['Lưu số mới và chuyển Chờ duyệt cùng lúc'])
    S5.add('Lưu và gửi thiếu cặp Doanh số', 'P0', [ACC_A, PLAN_M], OPEN_M + ['Dòng Kinh doanh 1 Hà Nội: xoá Doanh số Khách hãng Hàng hóa (giữ SL khách 5).', 'Bấm Lưu và gửi.'], '—',
           ['Ô Doanh số đó đỏ %s' % NEED_REV, 'Không lưu, không gửi; phiếu vẫn Đang tạo với số cũ'])
    S5.add('Lưu và gửi thiếu cặp SL khách', 'P0', [ACC_A, PLAN_M], OPEN_M + ['Dòng Kinh doanh 1 Hải Phòng: xoá SL khách Khách hãng Hàng hóa (giữ Doanh số 750,000,000).', 'Bấm Lưu và gửi.'], '—',
           ['Ô SL khách đó đỏ %s' % NEED_CUS, 'Không gửi'])
    S5.add('Không gửi được khi tổng doanh số bằng 0', 'P0', [ACC_A, CAT, FREE_2027],
           [MENU, NEW, 'Năm 2027, khối Kinh doanh, vùng Đồng bằng sông Hồng; Hà Nội chọn Kinh doanh 1, không nhập số.', 'Bấm Lưu và gửi.', 'Bấm Lưu; ở danh sách bấm Gửi duyệt phiếu vừa lưu.'], '—',
           ['Lưu và gửi: báo %s, không tạo phiếu' % NO_REV, 'Lưu thường được (Đang tạo)', 'Gửi duyệt ở danh sách: báo %s, phiếu vẫn Đang tạo' % NO_REV])
    S5.add('Khối chưa có phòng nào thì không gửi được', 'P1', [ACC_A, CAT, FREE_2027],
           [MENU, NEW, 'Năm 2027; khối Kinh doanh nhập đủ số; khối Nghiệp vụ chọn vùng nhưng không chọn phòng nào.', 'Bấm Lưu và gửi.'], '—',
           ['Tab Nghiệp vụ chấm đỏ, chữ đỏ %s dưới ô Khu vực' % REQ, 'Không gửi'])
    S5.add('Công ty chưa có người duyệt', 'P1', [ACC_A, PLAN_M, 'Công ty TPE tạm thời không có ai giữ quyền %s.' % QA], [MENU, 'Gửi duyệt %s.' % M], '—',
           ['Báo %s' % NO_APPROVER, 'Phiếu vẫn Đang tạo'])
    S5.add('Thông báo tới người duyệt khi gửi', 'P0', [ACC_A, PLAN_M, ACC_B, 'Tài khoản B2 (công ty TPE) cũng có quyền %s; H (TPSG) có quyền duyệt ở TPSG.' % QA],
           ['A gửi duyệt %s.' % M, 'B mở chuông thông báo, bấm vào thông báo mới.'], '—',
           ['B và B2 nhận thông báo "[CTKD] Gửi duyệt: %s"' % M, 'H (công ty khác) và A không nhận', 'Bấm thông báo mở màn Xem %s' % M])
    S5.add('Gửi phiếu đã gửi ở thẻ khác', 'P1', [ACC_A, PLAN_M], ['Thẻ 1 mở Xem %s.' % M, 'Thẻ 2 gửi duyệt %s.' % M, 'Thẻ 1 bấm Gửi duyệt > Gửi duyệt.'], '—',
           ['Thẻ 1 bị từ chối, báo %s' % NOPERM, 'Trạng thái giữ Chờ duyệt, không gửi 2 lần thông báo'])
    S5.add('Gửi lại sau khi bị từ chối', 'P1', [ACC_A, 'Phiếu %s bị từ chối về Đang tạo, lý do "Thiếu Bắc Ninh".' % M], [MENU, 'Gửi duyệt %s.' % M], '—',
           ['Về Chờ duyệt', 'Dòng "Lý do từ chối" không còn hiện ở màn Xem'])

    # ======================================================================== VI. DUYỆT PHIẾU / HỦY DUYỆT
    S6 = Sec()
    S6.add('Điều kiện hiện nút Duyệt', 'P0', [ACC_B, DATA], OPEN_P2_B, '—',
           ['Màn Xem %s có nút Duyệt, Từ chối' % P2, 'Không có Sửa, Gửi duyệt, Hủy phiếu (B không phải người lập)'])
    S6.add('Hộp xác nhận duyệt', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm Duyệt.'], '—',
           ['Hộp "Duyệt phiếu" nội dung "Duyệt phiếu %s? Phiếu đã duyệt không sửa được.", nút Hủy / Duyệt' % P2])
    S6.add('Duyệt thành công', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Bấm Duyệt > Duyệt.'], '—',
           ['Báo "Đã duyệt %s"' % P2, 'Quay về danh sách chờ duyệt, %s không còn trong đó' % P2,
            'Ở lối vào danh sách: trạng thái Đã duyệt (xanh lá), Người duyệt Trần Văn B, Ngày duyệt là hôm nay',
            'Lưu ý: nếu sau khi duyệt vẫn đứng ở màn Xem thì ghi nhận (quy ước: thao tác xong quay về danh sách)'])
    S6.add('Bấm Hủy ở hộp duyệt', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm Duyệt, chọn Hủy.'], '—', ['Phiếu vẫn Chờ duyệt, không có thông báo'])
    S6.add('Phiếu đã duyệt bị khoá', 'P0', [ACC_A, 'Phiếu %s vừa được B duyệt.' % P2], [MENU, 'Mở ba chấm dòng %s, mở Xem.' % P2], '—',
           ['Không còn Sửa, Gửi duyệt, Hủy phiếu', 'Chỉ còn Xem, In, Xuất Excel, Lịch sử'])
    S6.add('Thông báo cho người lập khi duyệt', 'P1', [ACC_A, 'Phiếu %s vừa được B duyệt.' % P2], ['A mở chuông thông báo.'], '—',
           ['A nhận "[CTKD] Đã duyệt: %s"' % P2, 'Bấm thông báo mở màn Xem %s' % P2])
    S6.add('Duyệt phiếu đã được xử lý ở thẻ khác', 'P0', [ACC_B, PEND], ['Thẻ 1 và 2 cùng mở Xem %s.' % P2, 'Thẻ 2 duyệt.', 'Thẻ 1 bấm Duyệt > Duyệt.'], '—',
           ['Thẻ 1 bị từ chối, báo không có quyền thực hiện', 'Không ghi thêm lần duyệt, không gửi thông báo lần 2'])
    S6.add('Duyệt phiếu bị người lập Hủy giữa chừng', 'P1', [ACC_B, PEND], ['B mở Xem %s.' % P2, 'A hủy phiếu %s.' % P2, 'B bấm Duyệt > Duyệt.'], '—',
           ['B bị từ chối, phiếu giữ trạng thái Hủy'])
    S6.add('Điều kiện hiện Hủy duyệt', 'P0', [ACC_B, APPR], [MENU, 'Mở ba chấm dòng %s.' % P3, 'Mở Xem %s.' % P3], '—',
           ['Có Hủy duyệt ở ba chấm và ở chân màn Xem', 'A (người lập, không có quyền duyệt) không thấy Hủy duyệt'])
    S6.add('Hộp xác nhận hủy duyệt', 'P1', [ACC_B, APPR], [MENU, 'Mở Xem %s, bấm Hủy duyệt.' % P3], '—',
           ['Hộp "Hủy duyệt phiếu" nội dung "Hủy duyệt phiếu %s? Phiếu trở về Đang tạo để người lập sửa.", nút Hủy / Hủy duyệt' % P3])
    S6.add('Hủy duyệt thành công', 'P0', [ACC_B, APPR, 'Chưa có phiếu giao chỉ tiêu theo nhân viên năm 2026 nào Chờ duyệt / Đã duyệt.'], [MENU, 'Mở Xem %s, bấm Hủy duyệt > Hủy duyệt.' % P3], '—',
           ['Báo "Đã hủy duyệt %s"' % P3, 'Phiếu về Đang tạo, cột Người duyệt / Ngày duyệt trống', 'A sửa và gửi lại được; B không còn thấy phiếu (Đang tạo chỉ người lập thấy)',
            'A nhận thông báo "[CTKD] Hủy duyệt: %s"' % P3])
    S6.add('Hủy duyệt bị chặn khi phiếu theo nhân viên đang dùng chỉ tiêu', 'P0', [ACC_B, APPR, 'Phiếu giao chỉ tiêu theo nhân viên %s (phòng Kinh doanh 1, năm 2026) đang Đã duyệt.' % NV_OK],
           [MENU, 'Mở Xem %s, bấm Hủy duyệt > Hủy duyệt.' % P3], '—',
           ['Báo "Đã có phiếu giao chỉ tiêu theo nhân viên %s dùng chỉ tiêu của phiếu này, cần hủy duyệt/từ chối phiếu đó trước"' % NV_OK, 'Phiếu vẫn Đã duyệt'])
    S6.add('Phiếu theo nhân viên Đang tạo không chặn Hủy duyệt', 'P1', [ACC_B, APPR, 'Chỉ có %s (phòng Kinh doanh 2, năm 2026) ở trạng thái Đang tạo.' % NV_DRAFT],
           [MENU, 'Hủy duyệt %s.' % P3], '—', ['Hủy duyệt được, phiếu về Đang tạo'])
    S6.add('Hủy duyệt chỉ trong công ty đang làm', 'P1', [ACC_H, DATA, 'Phiếu %s do H duyệt.' % P7], [MENU, 'Mở ba chấm dòng %s.' % P7], '—',
           ['H thấy %s (Chờ duyệt) và %s (mình đã duyệt, có Hủy duyệt)' % (P6, P7), 'Không thấy %s của TPE nên không Hủy duyệt được phiếu công ty khác' % P3])
    S6.add('Lịch sử ghi người duyệt và thời gian', 'P1', [ACC_B, 'B vừa duyệt %s.' % P2], [MENU, 'Ba chấm dòng %s > Lịch sử.' % P2], '—',
           ['Có dòng "Duyệt" (Chờ duyệt sang Đã duyệt) do Trần Văn B, thời gian đúng lúc duyệt'])

    # ======================================================================== VII. KHÔNG DUYỆT PHIẾU
    S7 = Sec()
    S7.add('Giao diện hộp từ chối', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối.'], '—',
           ['Hộp "Từ chối phiếu" nội dung "Từ chối phiếu %s? Phiếu trở về Đang tạo để người lập sửa."' % P2,
            'Có ô "Lý do" (gợi ý "Nhập lý do từ chối"), nút Hủy / Từ chối (màu đỏ)'])
    S7.add('Từ chối khi bỏ trống lý do', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối, để trống Lý do (hoặc chỉ gõ dấu cách), bấm Từ chối.'], '—',
           ['Ô Lý do đỏ %s, hộp không đóng' % REQ, 'Phiếu vẫn Chờ duyệt'])
    S7.add('Từ chối thành công', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối, nhập Lý do, bấm Từ chối.'], 'Lý do: Thiếu số Bắc Ninh',
           ['Báo "Đã từ chối %s"' % P2, 'Quay về danh sách; phiếu về Đang tạo nên không còn trong danh sách của B',
            'A thấy phiếu Đang tạo, màn Xem có "Lý do từ chối: Thiếu số Bắc Ninh"; sửa / gửi lại được'])
    S7.add('Lý do dài', 'P2', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối, dán lý do 1001 ký tự, bấm Từ chối.', 'Sửa còn 1000 ký tự, bấm Từ chối.'], '1001 ký tự; 1000 ký tự',
           ['1001 ký tự: báo lỗi, phiếu không đổi', '1000 ký tự: từ chối được, lý do hiện đủ'])
    S7.add('Bấm Hủy ở hộp từ chối', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối, nhập lý do, bấm Hủy.'], '—', ['Phiếu vẫn Chờ duyệt, không có thông báo'])
    S7.add('Thông báo cho người lập khi từ chối', 'P1', [ACC_A, 'B vừa từ chối %s, lý do "Thiếu số Bắc Ninh".' % P2], ['A mở chuông thông báo.'], '—',
           ['A nhận "[CTKD] Từ chối: %s" kèm "Lý do: Thiếu số Bắc Ninh"' % P2, 'Bấm thông báo mở màn Xem %s' % P2])
    S7.add('Từ chối phiếu đã được xử lý ở thẻ khác', 'P1', [ACC_B, PEND], ['Thẻ 1 và 2 mở Xem %s.' % P2, 'Thẻ 2 duyệt.', 'Thẻ 1 bấm Từ chối, nhập lý do, bấm Từ chối.'], '—',
           ['Thẻ 1 bị từ chối, báo không có quyền thực hiện', 'Phiếu giữ Đã duyệt'])
    S7.add('Lịch sử ghi lần từ chối', 'P2', [ACC_A, 'B vừa từ chối %s.' % P2], [MENU, 'Ba chấm dòng %s > Lịch sử.' % P2], '—',
           ['Có dòng "Từ chối" (Chờ duyệt sang Đang tạo), ghi "Lý do: Thiếu số Bắc Ninh", người Trần Văn B'])

    # ======================================================================== VIII. HỦY PHIẾU
    S8 = Sec()
    S8.add('Điều kiện hiện Hủy phiếu', 'P0', [ACC_A, DATA], [MENU, 'Mở ba chấm các dòng.'], '—',
           ['Có Hủy phiếu ở %s (Đang tạo) và %s (Chờ duyệt) do A lập' % (M, P2), 'Không có ở %s (Đã duyệt, phải Hủy duyệt trước), %s (Hủy)' % (P3, P4),
            'B (người duyệt) không thấy Hủy phiếu'])
    S8.add('Hộp xác nhận hủy phiếu', 'P1', [ACC_A, PLAN_M], [MENU, 'Ba chấm dòng %s > Hủy phiếu.' % M], '—',
           ['Hộp "Hủy phiếu" nội dung "Hủy phiếu %s? Phiếu Hủy không sửa được; công ty được tạo phiếu khác cho năm 2027.", nút Đóng / Hủy phiếu' % M])
    S8.add('Hủy phiếu Đang tạo', 'P0', [ACC_A, PLAN_M], [MENU, 'Ba chấm dòng %s > Hủy phiếu > Hủy phiếu.' % M], '—',
           ['Báo "Đã hủy %s"' % M, 'Trạng thái Hủy (màu đỏ); dòng chỉ còn Xem, Lịch sử', 'Phiếu vẫn còn trong danh sách (không bị xoá)'])
    S8.add('Hủy phiếu Chờ duyệt', 'P0', [ACC_A, PEND, ACC_B], [MENU, 'Hủy phiếu %s.' % P2, 'B mở lối vào chờ duyệt.'], '—',
           ['Phiếu thành Hủy', 'Không còn ở lối vào "Giao chỉ tiêu chờ duyệt" của B'])
    S8.add('Bấm Đóng ở hộp hủy', 'P1', [ACC_A, PLAN_M], [MENU, 'Ba chấm dòng %s > Hủy phiếu, bấm Đóng.' % M], '—', ['Phiếu vẫn Đang tạo'])
    S8.add('Hủy xong được lập phiếu khác cùng năm', 'P0', [ACC_A, 'Vừa hủy %s (năm 2027).' % M], [MENU, NEW, 'Lập phiếu năm 2027 hợp lệ, bấm Lưu.'], '—',
           ['Lưu được, không báo trùng năm 2027'])
    S8.add('Hủy phiếu đã được duyệt ở thẻ khác', 'P1', [ACC_A, PEND], ['A mở Xem %s.' % P2, 'B duyệt %s.' % P2, 'A bấm Hủy phiếu > Hủy phiếu.'], '—',
           ['A bị từ chối, phiếu giữ Đã duyệt'])
    S8.add('Lịch sử ghi lần hủy', 'P2', [ACC_A, 'Vừa hủy %s.' % M], [MENU, 'Ba chấm dòng %s > Lịch sử.' % M], '—',
           ['Có dòng "Thay đổi trạng thái" từ Đang tạo sang Hủy, người Nguyễn Văn A', 'Hủy phiếu không gửi thông báo cho ai'])

    # ======================================================================== IX. LỊCH SỬ
    S9 = Sec()
    S9.add('Mở popup Lịch sử từ danh sách', 'P1', [ACC_A, PLAN_M], [MENU, 'Ba chấm dòng %s > Lịch sử.' % M], '—',
           ['Popup tiêu đề "Lịch sử thay đổi" kèm số phiếu %s' % M, 'Có cột người thực hiện, thời gian, loại hành động, nội dung', 'Dòng mới nhất ở trên'])
    S9.add('Ghi nhận Tạo mới', 'P0', [ACC_A, 'A vừa lưu phiếu mới năm 2027.'], [MENU, 'Mở Lịch sử phiếu vừa tạo.'], '—',
           ['Có dòng "Tạo mới" do Nguyễn Văn A, kèm Số phiếu và Năm 2027'])
    S9.add('Ghi nhận Sửa', 'P1', [ACC_A, PLAN_M], OPEN_M + ['Đổi 1 số, bấm Lưu.', 'Mở Lịch sử %s.' % M], '—',
           ['Có dòng "Thay đổi thông tin" do Nguyễn Văn A', 'Lưu ý: ghi rõ dòng này có nêu giá trị cũ / mới của ô đã đổi hay chỉ ghi Số phiếu, Năm'])
    S9.add('Lưu mà không đổi gì không ghi lịch sử', 'P2', [ACC_A, PLAN_M], OPEN_M + ['Không đổi gì, bấm Lưu.', 'Mở Lịch sử %s.' % M], '—',
           ['Không phát sinh dòng "Thay đổi thông tin" mới'])
    S9.add('Ghi đủ luồng trạng thái', 'P0', [ACC_A, ACC_B, 'Phiếu %s đi qua: Gửi duyệt, Từ chối (lý do "Thiếu Bắc Ninh"), Gửi duyệt, Duyệt, Hủy duyệt.' % M], [MENU, 'Mở Lịch sử %s.' % M], '—',
           ['Đủ các dòng theo thứ tự mới tới cũ: Hủy duyệt, Duyệt, Gửi duyệt, Từ chối (Lý do: Thiếu Bắc Ninh), Gửi duyệt, Tạo mới',
            'Mỗi dòng ghi trạng thái cũ sang trạng thái mới, đúng người thực hiện (A gửi, B duyệt / từ chối / hủy duyệt)'])
    S9.add('Khối Lịch sử ở màn Xem khớp popup', 'P1', [ACC_A, PLAN_M], [MENU, 'Mở Xem %s, xem khối Lịch sử ở cuối màn.' % M, 'So với popup Lịch sử ở danh sách.'], '—',
           ['Hai nơi hiện giống nhau (cùng số dòng, cùng nội dung)'])
    S9.add('Đóng popup Lịch sử', 'P2', [ACC_A, PLAN_M], [MENU, 'Mở Lịch sử, bấm Đóng (hoặc dấu X).'], '—', ['Popup đóng, danh sách giữ trang và bộ lọc đang có'])

    # ======================================================================== X. XEM CHI TIẾT
    S10 = Sec()
    S10.add('Giao diện màn Xem', 'P0', [ACC_A, PLAN_M], [MENU, 'Bấm số phiếu %s.' % M], '—',
            ['Tiêu đề "Chi tiết phiếu giao chỉ tiêu kinh doanh theo phòng ban: %s" kèm nhãn Đang tạo' % M,
             'Năm, Khối kinh doanh, Khu vực hiện dạng chữ, không sửa được; bảng không có ô nhập, không có thùng rác, liên kết Thêm / Chia',
             'Thu / mở cây và ô Hiển thị đến cấp vẫn dùng được', 'Không có nút Lưu'])
    S10.add('Số liệu màn Xem khớp danh sách và lúc lập', 'P0', [ACC_A, PLAN_M], [MENU, 'Mở Xem %s.' % M], '—',
            ['Dòng TỔNG khối Kinh doanh: Khách hãng Hàng hóa 11 / 3,450,000,000, Tổng cộng Hàng hóa 17 / 4,800,000,000',
             'Ô 0 ở dòng phòng để trống, dòng tỉnh / dòng TỔNG hiện 0', 'Năm, trạng thái khớp cột ở danh sách'])
    S10.add('Nút ở chân màn Xem theo trạng thái (người lập)', 'P0', [ACC_A, DATA], [MENU, 'Lần lượt mở Xem %s, %s, %s, %s.' % (M, P2, P3, P4)], '—',
            ['Đang tạo: Sửa, Gửi duyệt, Hủy phiếu, Xuất Excel, In, Quay lại (không có Lưu, Lưu và gửi)',
             'Chờ duyệt: Hủy phiếu, Xuất Excel, In, Quay lại', 'Đã duyệt: Xuất Excel, In, Quay lại', 'Hủy: chỉ Quay lại'])
    S10.add('Nút ở màn Xem khớp ba chấm ở danh sách', 'P1', [ACC_B, DATA], [MENU, 'So nút ở ba chấm và ở chân màn Xem của %s, %s.' % (P2, P3)], '—',
            ['%s: Duyệt, Từ chối (chỉ ở màn Xem), Xuất Excel, In' % P2, '%s: Hủy duyệt, Xuất Excel, In' % P3, 'Nút ẩn ở danh sách thì cũng ẩn ở màn Xem'])
    S10.add('Quay lại về đúng lối vào', 'P1', [ACC_B, PEND], [MENU_CD, 'Bấm số phiếu %s, bấm Quay lại.' % P2], '—',
            ['Về lối vào "Giao chỉ tiêu chờ duyệt" (không về danh sách thường)'])
    S10.add('Tab Tổng hợp ở màn Xem', 'P1', [ACC_A, PLAN_M], [MENU, 'Mở Xem %s, bấm tab Tổng hợp.' % M], '—',
            ['Dòng TỔNG CỘNG, mỗi tỉnh có Năm trước, dòng từng khối', 'Số khớp tab khối'])
    S10.add('Năm trước ở màn Xem giữ số lúc lưu', 'P1', [ACC_A, PLAN_M, 'Sau khi lưu M, phiếu %s được Hủy duyệt.' % P3], [MENU, 'Mở Xem %s.' % M, 'Mở Sửa %s.' % M], '—',
            ['Màn Xem: Năm trước Hà Nội vẫn là số đã chụp lúc lưu (8 / 2,500,000,000 ...)', 'Màn Sửa: Năm trước tính lại theo hiện tại nên trống (2026 không còn phiếu Đã duyệt)'])
    S10.add('Phiếu có bộ phận ở màn Xem', 'P1', [ACC_A, PLAN_M, 'Kinh doanh 1 Hà Nội chia Nhóm KD1-1 (3 / 900,000,000), Nhóm KD1-2 (2 / 600,000,000).'], [MENU, 'Mở Xem %s.' % M], '—',
            ['Dòng phòng 5 / 1,500,000,000, dưới có dòng 1.1, 1.2 thụt lề đúng tên và số', 'Góc phải khối Chi tiết ghi "3 Tỉnh/TP · 3 phòng · 2 bộ phận"'])
    S10.add('Mở Xem phiếu không tồn tại', 'P1', ACC_A, ['Mở đường dẫn màn Xem với số thứ tự phiếu không có (ví dụ 99999).'], '—',
            ['Không lỗi trang, tự quay về danh sách'])
    S10.add('Phiếu lập trên hệ thống cũ', 'P0', [ACC_A, 'Phiếu %s lập trên hệ thống cũ (Đã duyệt), dòng phòng Hà Nội có nhập chi tiết khách hàng: 2 khách hãng Hàng hóa, doanh số 1,100,000,000.' % P0],
            [MENU, 'Mở Xem %s.' % P0], '—',
            ['Hiện đủ khối, tỉnh, phòng và 8 số như hệ thống cũ (Khách hãng Hàng hóa 2 / 1,100,000,000)', 'Không có nút / popup "Thêm / Xem Khách Hàng"',
             'Nút: Xuất Excel, In, Quay lại'])

    # ======================================================================== XI. IN
    S11 = Sec()
    S11.add('Mở bản in từ danh sách', 'P0', [ACC_A, PLAN_M], [MENU, 'Ba chấm dòng %s > In.' % M], '—',
            ['Mở popup xem trước tiêu đề "Xem trước phiếu: %s", khổ A4 ngang' % M, 'Có nút In để in ra máy in'])
    S11.add('Nội dung đầu bản in', 'P0', [ACC_A, PLAN_M], [MENU, 'Mở In %s.' % M], '—',
            ['Đầu trang: letterhead của công ty TPE (công ty ghi trên phiếu), "Số: %s", "Ngày tạo: 12/11/2026"' % M,
             'Tiêu đề "PHIẾU GIAO CHỈ TIÊU KINH DOANH THEO PHÒNG BAN"', 'Dòng "Năm: 2027 · Trạng thái: Đang tạo"'])
    S11.add('Bảng số trên bản in', 'P0', [ACC_A, PLAN_M, 'Kinh doanh 1 Hà Nội có 2 bộ phận.'], [MENU, 'Mở In %s.' % M], '—',
            ['Mỗi khối 1 bảng "Khối Kinh doanh": cột STT, Tỉnh/TP, Phòng phụ trách + 12 cột 3 tầng (Khách hãng / Khách khác / Tổng cộng; Hàng hóa / Dịch vụ; SL / Doanh số)',
             'Dòng TỔNG CỘNG; mỗi tỉnh có dòng Năm trước, Tổng cộng, các dòng phòng, dòng bộ phận thụt lề', 'Mục "Tổng hợp" cuối với cột Khối thay cho Phòng phụ trách',
             'Số có dấu phẩy ngăn nghìn, khớp màn Xem'])
    S11.add('Chữ ký 3 cột', 'P1', [ACC_A, APPR], [MENU, 'Mở In %s.' % P3], '—',
            ['Cuối bản in có 3 cột: Người lập, Trưởng phòng, Người duyệt, mỗi cột ghi "(Ký, ghi rõ họ tên)"', 'Dưới Người lập ghi Nguyễn Văn A, dưới Người duyệt ghi Trần Văn B'])
    S11.add('In từ màn Xem', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm In.'], '—', ['Mở đúng bản in %s như từ danh sách' % P2])
    S11.add('Phiếu Hủy không in được', 'P1', [ACC_A, DATA], [MENU, 'Ba chấm dòng %s; mở Xem %s.' % (P4, P4)], '—', ['Không có nút In ở cả 2 nơi'])
    S11.add('Phiếu nhiều tỉnh sang trang', 'P2', [ACC_V4, 'Phiếu %s có 30 Tỉnh/TP.' % P7], [MENU, 'Mở In %s, xem trước nhiều trang.' % P7], '—',
            ['Bảng sang trang không mất viền, chữ không bị cắt lề phải'])

    # ======================================================================== XII. TÙY CHỈNH CỘT
    S12 = Sec()
    S12.add('Mở popup Tuỳ chỉnh cột', 'P1', ACC_A, [MENU, 'Bấm Cấu hình cột hiển thị.'], '—',
            ['Popup "Tuỳ chỉnh cột" liệt kê đủ cột của bảng, dòng "Đang chọn 9/10 cột"', 'Nút Chọn tất cả, Bỏ chọn hết, Lưu, Đóng',
             'STT, Số phiếu, Hành động là cột khoá (không bỏ tích, không kéo)'])
    S12.add('Hiện cột ẩn và ẩn cột đang hiện', 'P0', ACC_A, [MENU, 'Mở Tuỳ chỉnh cột, tích Ngày duyệt, bỏ tích Người tạo, bấm Lưu.'], '—',
            ['Bảng có cột Ngày duyệt, mất cột Người tạo', 'Dữ liệu và bộ lọc không đổi'])
    S12.add('Kéo đổi thứ tự cột', 'P2', ACC_A, [MENU, 'Mở Tuỳ chỉnh cột, kéo Trạng thái lên trên Năm, bấm Lưu.'], '—', ['Cột Trạng thái đứng trước cột Năm'])
    S12.add('Đóng không lưu', 'P2', ACC_A, [MENU, 'Mở Tuỳ chỉnh cột, bỏ tích Công ty, bấm Đóng.'], '—', ['Bảng giữ nguyên cột Công ty'])
    S12.add('Ghi nhớ sau F5 và theo tài khoản', 'P1', [ACC_A, ACC_B], ['A ẩn cột Người tạo, Lưu, nhấn F5.', 'Đăng nhập B, mở màn.'], '—',
            ['A sau F5 vẫn ẩn Người tạo', 'B vẫn thấy cột Người tạo (cấu hình theo từng tài khoản)'])
    S12.add('Cấu hình riêng với màn theo nhân viên', 'P2', ACC_A, ['Ở màn này ẩn cột Người tạo, Lưu.', MENU_NV], '—', ['Màn theo nhân viên vẫn hiện cột Người tạo'])

    # ======================================================================== XIII. XUẤT EXCEL
    S13 = Sec()
    S13.add('Mở popup chọn trường xuất', 'P1', ACC_A, [MENU, 'Bấm Xuất Excel trên bảng.'], '—',
            ['Popup "Chọn trường xuất file": Số phiếu, Công ty, Năm, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái',
             'Mặc định tích các cột đang hiện (không tích Ngày duyệt)', 'Nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng'])
    S13.add('Xuất theo trường mặc định', 'P0', [ACC_A, DATA], [MENU, 'Bấm Xuất Excel > Xuất file.'], '—',
            ['Tải file phieu_giao_chi_tieu_theo_phong_ban.xlsx, báo "Xuất Excel thành công"', 'Tiêu đề "DANH SÁCH PHIẾU GIAO CHỈ TIÊU KINH DOANH THEO PHÒNG BAN"',
             'Cột STT + các trường đã chọn đúng thứ tự; 5 dòng khớp danh sách', 'Ngày dạng dd/mm/yyyy, Năm là số'])
    S13.add('Xuất chọn một số trường / bỏ chọn hết', 'P1', [ACC_A, DATA], [MENU, 'Bấm Xuất Excel, bấm Bỏ chọn hết.', 'Tích Số phiếu, Trạng thái, bấm Xuất file.'], '—',
            ['Khi bỏ chọn hết: nút Xuất file không bấm được', 'File chỉ có STT, Số phiếu, Trạng thái'])
    S13.add('Xuất theo bộ lọc và tìm kiếm', 'P0', [ACC_V4, DATA], [MENU, ADV, 'Chọn Công ty TPSG, bấm Tìm kiếm.', 'Bấm Xuất Excel > Xuất file.'], '—',
            ['File chỉ có %s, %s' % (P6, P7), 'Không lẫn phiếu ngoài phạm vi xem'])
    S13.add('Xuất nhiều trang', 'P1', 'Tài khoản V4, 25 phiếu, đang ở trang 1 (10 dòng/trang).', [MENU, 'Bấm Xuất Excel > Xuất file.'], '—',
            ['File có đủ 25 dòng (không chỉ trang đang xem)', 'Khi đang xuất hiện dòng tiến độ "Đã tải ... dòng…"'])
    S13.add('Xuất khi danh sách rỗng', 'P2', ACC_N, [MENU, 'Bấm Xuất Excel > Xuất file.'], '—', ['Báo "Không có dữ liệu để xuất", không tải file'])
    S13.add('Xuất Excel 1 phiếu', 'P0', [ACC_A, PLAN_M], [MENU, 'Ba chấm dòng %s > Xuất Excel.' % M], '—',
            ['Tải file %s.xlsx' % M, 'Mỗi khối 1 sheet tên "1. Kinh doanh"..., thêm sheet "Tổng hợp"',
             'Tiêu đề "PHIẾU GIAO CHỈ TIÊU KINH DOANH THEO PHÒNG BAN — KHỐI KINH DOANH", dòng "Số: %s · Năm: 2027 · Trạng thái: Đang tạo"' % M,
             'Cột STT, Tỉnh/TP, Phòng phụ trách + 12 cột 3 tầng; dòng TỔNG CỘNG, mỗi tỉnh có Năm trước, Tổng cộng, dòng phòng (mở hết, có bộ phận)',
             'Ô số là số thật có dấu phẩy ngăn nghìn (cộng SUM được)'])
    S13.add('Xuất Excel 1 phiếu từ màn Xem, khối có dấu gạch chéo', 'P2', [ACC_A, PLAN_M, 'Phiếu có thêm khối "Chi nhánh/Đơn vị thành viên".'], [MENU, 'Mở Xem %s, bấm Xuất Excel.' % M], '—',
            ['Xuất được, sheet tên "2. Chi nhánh-Đơn vị thành viên" (dấu gạch chéo đổi thành gạch ngang)', 'Không báo lỗi'])
    S13.add('Phiếu Hủy không xuất Excel 1 phiếu', 'P2', [ACC_A, DATA], [MENU, 'Ba chấm dòng %s.' % P4], '—', ['Không có Xuất Excel ở dòng phiếu Hủy'])

    # ======================================================================== XIV. RÀNG BUỘC
    S14 = Sec()
    S14.add('Yêu cầu issue: bỏ chọn chi tiết khách hàng', 'P0', [ACC_A, CAT], [MENU, NEW, 'Chọn khối Kinh doanh, vùng Đồng bằng sông Hồng, chọn phòng ở Hà Nội.'], '—',
            ['Dòng phòng có đủ 8 ô nhập thẳng: Khách hãng (Hàng hóa, Dịch vụ) và Khách khác (Hàng hóa, Dịch vụ), mỗi nhóm có SL khách và Doanh số',
             'KHÔNG có nút / popup "Thêm / Xem Khách Hàng", không có ô tick "Khách hàng mới"', 'Nhóm Tổng cộng tự tính = Khách hãng + Khách khác'])
    S14.add('Phiếu Đã duyệt là nguồn Chỉ tiêu giao của phiếu theo nhân viên', 'P0', [ACC_A, 'Phiếu phòng ban năm 2027 của TPE vừa được duyệt với số như Test Data; A có quyền tạo phiếu theo nhân viên.'],
            [MENU_NV, 'Bấm Tạo mới, chọn Năm 2027, Phòng ban Kinh doanh 1.'], FULL_TD,
            ['Dòng "Chỉ tiêu giao" của Hà Nội = số của phòng Kinh doanh 1 Hà Nội (Khách hãng Hàng hóa 5 / 1,500,000,000 ...)',
             'Hải Phòng có Chỉ tiêu giao 2 / 750,000,000 ...; không có Bắc Ninh (phòng không có chỉ tiêu ở đó)'])
    S14.add('Phòng ở 2 khối cùng tỉnh thì chỉ tiêu được cộng', 'P1', ['Phiếu phòng ban 2027 Đã duyệt: Kinh doanh 1 có ở Hà Nội của khối Kinh doanh (5 / 1,500,000,000) và khối Nghiệp vụ (1 / 200,000,000).'],
            [MENU_NV, 'Bấm Tạo mới, Năm 2027, Phòng ban Kinh doanh 1.'], '—', ['Chỉ tiêu giao Hà Nội Khách hãng Hàng hóa 6 / 1,700,000,000 (1 dòng tỉnh, cộng 2 khối)'])
    S14.add('Phiếu chưa duyệt chưa là nguồn chỉ tiêu', 'P0', ['Phiếu phòng ban năm 2028 (%s) đang Chờ duyệt.' % P2], [MENU_NV, 'Bấm Tạo mới, Năm 2028, mở ô Phòng ban.'], '—',
            ['Không có phòng nào để chọn / báo "Phòng chưa có chỉ tiêu được duyệt cho năm 2028"'])
    S14.add('Phòng có chia bộ phận: phiếu nhân viên nhận tổng phòng', 'P1', ['Phiếu phòng ban 2027 Đã duyệt, Kinh doanh 1 Hà Nội chia Nhóm KD1-1 (3 / 900,000,000), Nhóm KD1-2 (2 / 600,000,000).'],
            [MENU_NV, 'Tạo mới, Năm 2027, Phòng ban Kinh doanh 1.'], '—', ['Chỉ tiêu giao Hà Nội Khách hãng Hàng hóa 5 / 1,500,000,000 (tổng phòng, không tách bộ phận)'])
    S14.add('Hủy duyệt phiếu phòng ban ảnh hưởng phiếu nhân viên Đang tạo', 'P1', ['Phiếu phòng ban 2026 vừa bị Hủy duyệt; %s (Kinh doanh 2, 2026) đang Đang tạo.' % NV_DRAFT],
            [MENU_NV, 'Gửi duyệt %s.' % NV_DRAFT], '—', ['Báo "Phòng chưa có chỉ tiêu được duyệt cho năm 2026 — mở Sửa để kiểm tra lại phiếu", phiếu nhân viên vẫn Đang tạo'])
    S14.add('Duyệt lại thì phiếu nhân viên lấy chỉ tiêu mới', 'P1', ['Phiếu phòng ban 2026 Hủy duyệt, sửa Kinh doanh 2 Hà Nội thành 6 / 1,800,000,000, gửi và duyệt lại.'],
            [MENU_NV, 'Mở Sửa %s.' % NV_DRAFT], '—', ['Chỉ tiêu giao Hà Nội của Kinh doanh 2 là 6 / 1,800,000,000 (số mới)'])
    S14.add('Năm trước lấy đúng công ty và khối', 'P1', [ACC_A, FREE_2027, BEFORE_2026, 'TPSG có %s (2026, Đã duyệt) khối Kinh doanh miền Nam, Hà Nội 9 / 3,000,000,000.' % P7],
            [MENU, NEW, 'Năm 2027, khối Kinh doanh, vùng Đồng bằng sông Hồng.'], '—', ['Năm trước Hà Nội chỉ lấy phiếu của TPE (8 / 2,500,000,000), không cộng số TPSG'])
    S14.add('Mỗi công ty mỗi năm một phiếu hiệu lực', 'P0', [ACC_A2, DATA], ['A2 %s' % MENU, NEW, 'Chọn Năm 2027, nhập hợp lệ, bấm Lưu.'], '—',
            ['Bị chặn dù A2 khác người lập: "Công ty đã có phiếu %s (Đang tạo) cho năm 2027"' % M, 'Trùng tính theo công ty, không theo người lập'])
    S14.add('Danh mục khối / vùng / bộ phận bị ngừng sau khi lập', 'P1', [ACC_A, APPR, 'Sau khi duyệt %s, khối Nghiệp vụ và bộ phận Nhóm KD1-2 bị ngừng hoạt động.' % P3],
            [MENU, 'Mở Xem %s.' % P3, 'In và Xuất Excel %s.' % P3], '—', ['Tab, tên khối, tên bộ phận vẫn hiện đúng tên cũ ở màn Xem, bản in, file Excel'])
    S14.add('Lập phiếu không đổi số của màn khác đang mở', 'P2', [ACC_A, 'Đang mở màn kế hoạch bán hàng của nhân viên ở thẻ khác.'], ['Lưu phiếu phòng ban mới (Đang tạo).'], '—',
            ['Phiếu Đang tạo / Chờ duyệt chưa được màn nào khác dùng làm chỉ tiêu (chỉ phiếu Đã duyệt)'])

    # ======================================================================== XV. PHÂN QUYỀN
    S15 = Sec()
    S15.add('Không có quyền nào', 'P0', [ACC_N, DATA], [MENU], '—',
            ['Vào được màn (menu không đòi quyền), bảng hiện %s' % EMPTY, 'Không có Tạo mới', 'Không thấy phiếu của người khác, kể cả phiếu Chờ duyệt / Đã duyệt cùng công ty'])
    S15.add('Quyền %s' % QC, 'P0', [ACC_A, DATA], [MENU], '—',
            ['Có Tạo mới; thấy 5 phiếu mình lập', 'Sửa / Gửi duyệt / Hủy phiếu được phiếu của mình', 'Không thấy phiếu người khác, không duyệt được'])
    S15.add('Quyền %s' % QA, 'P0', [ACC_B, DATA], [MENU, MENU_CD], '—',
            ['Có mục "Giao chỉ tiêu chờ duyệt" ở nhóm Phê Duyệt', 'Danh sách: phiếu Chờ duyệt của công ty TPE (%s) + phiếu mình đã duyệt (%s)' % (P2, P3),
             'Duyệt / Từ chối / Hủy duyệt được; không có Tạo mới'])
    S15.add('Quyền %s mức Công ty' % QV, 'P0', [ACC_V3, DATA], [MENU], '—',
            ['Thấy 4 phiếu TPE: %s, %s, %s, %s' % (P2, P4, P3, P0), 'Không thấy %s, %s (Đang tạo), phiếu TPSG' % (M, P5), 'Bộ lọc không có ô Công ty'])
    S15.add('Quyền %s mức Tổng công ty' % QV, 'P0', [ACC_V4, DATA], [MENU, ADV], '—',
            ['Thấy 6 phiếu (thêm %s, %s của TPSG)' % (P6, P7), 'Bộ lọc có ô Công ty'])
    S15.add('Quyền xem không mở thao tác', 'P0', [ACC_V4, DATA], [MENU, 'Mở ba chấm các dòng; mở Xem %s.' % P6], '—',
            ['Chỉ có Xem, In, Xuất Excel, Lịch sử', 'Không có Sửa, Gửi duyệt, Duyệt, Từ chối, Hủy duyệt, Hủy phiếu', 'Không thấy mục "Giao chỉ tiêu chờ duyệt"'])
    S15.add('Hai vai trò khác mức thì lấy mức lớn hơn', 'P0', ['Tài khoản V5: vai trò 1 cấp %s mức Công ty, vai trò 2 cấp mức Tổng công ty.' % QV, DATA], [MENU], '—',
            ['Thấy 6 phiếu như mức Tổng công ty, có ô lọc Công ty'])
    S15.add('Người đã duyệt vẫn thấy phiếu', 'P1', [ACC_B, APPR, 'Sau đó B bị gỡ quyền %s.' % QA], [MENU], '—',
            ['B vẫn thấy %s (phiếu mình đã duyệt)' % P3, 'Không còn thấy %s (Chờ duyệt)' % P2])
    S15.add('Mất quyền tạo thì không thao tác phiếu của mình', 'P0', [ACC_A, PLAN_M, 'A bị gỡ quyền %s.' % QC], [MENU, 'Mở ba chấm dòng %s; mở Xem.' % M], '—',
            ['Vẫn thấy phiếu của mình', 'Không còn Tạo mới, Sửa, Gửi duyệt, Hủy phiếu (nút ẩn hẳn, không hiện xám)'])
    S15.add('Ẩn nút khi thiếu quyền ở danh sách và màn Xem', 'P0', [ACC_V3, DATA], [MENU, 'Mở ba chấm dòng %s; mở Xem %s.' % (P2, P2)], '—',
            ['Không có Duyệt, Từ chối, Hủy phiếu ở cả 2 nơi', 'Chân màn Xem chỉ có Xuất Excel, In, Quay lại'])
    S15.add('Mở thẳng màn Xem phiếu ngoài phạm vi', 'P0', [ACC_A, 'X gửi cho A đường dẫn màn Xem phiếu %s (TPSG).' % P6], ['A mở đường dẫn đó.'], '—',
            ['Không hiện dữ liệu phiếu, tự quay về danh sách của A'])
    S15.add('Mở thẳng màn Xem phiếu Đang tạo của người khác', 'P0', [ACC_V4, PLAN_M], ['V4 mở đường dẫn màn Xem %s do A gửi.' % M], '—',
            ['Không hiện dữ liệu, quay về danh sách (phiếu Đang tạo chỉ người lập xem)'])
    S15.add('Mở thẳng màn Sửa phiếu người khác', 'P0', [ACC_B, PLAN_M], ['B mở đường dẫn màn Sửa %s do A gửi.' % M], '—',
            ['Không mở được form, quay về danh sách', 'Phiếu M không đổi'])
    S15.add('Mở thẳng màn Tạo mới khi thiếu quyền tạo', 'P0', [ACC_N], ['N mở màn Tạo phiếu từ trang đã đánh dấu (bookmark).', 'Nhập phiếu năm 2032 hợp lệ, bấm Lưu.'], '—',
            ['Hệ thống từ chối, báo không có quyền, không tạo phiếu', 'Lưu ý: nếu form vẫn mở cho nhập thì ghi nhận (nên chặn ngay khi mở)'])
    S15.add('Mở lối vào chờ duyệt khi thiếu quyền', 'P0', ACC_A, ['A mở đường dẫn lối vào "Giao chỉ tiêu chờ duyệt" do B gửi.'], '—',
            ['Danh sách chờ duyệt rỗng (%s)' % EMPTY, 'Không thấy phiếu của người khác'])
    S15.add('Bị gỡ quyền duyệt giữa lúc thao tác', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Quản trị gỡ quyền %s của B.' % QA, 'B bấm Duyệt > Duyệt.'], '—',
            ['B bị từ chối, báo không có quyền', 'Phiếu vẫn Chờ duyệt', 'Tải lại: mục "Giao chỉ tiêu chờ duyệt" biến mất'])
    S15.add('Được cấp quyền giữa lúc thao tác', 'P1', ['Tài khoản B3 (TPE, chưa có quyền duyệt) đang mở danh sách.'], ['Quản trị cấp quyền %s cho B3.' % QA, 'B3 tải lại trang.'], '—',
            ['Hiện mục "Giao chỉ tiêu chờ duyệt", thấy %s' % P2])
    S15.add('Không có đặc quyền quản trị cao nhất', 'P1', ['Tài khoản SA thuộc vai trò quản trị cao nhất nhưng không được cấp 3 quyền của màn.', DATA], [MENU], '—',
            ['SA chỉ thấy phiếu mình lập, không có Tạo mới, không có mục chờ duyệt'])
    S15.add('Đổi công ty đang làm việc', 'P0', ['Tài khoản V6: quyền %s mức Công ty và %s ở công ty TPE; ở TPSG không có quyền.' % (QV, QA), DATA],
            [MENU, 'Đổi công ty đang làm việc sang TPSG, mở lại màn.'], '—',
            ['Quyền tính lại theo TPSG: chỉ còn phiếu mình lập / mình đã duyệt', 'Không còn thấy phiếu TPE, không còn mục chờ duyệt'])
    S15.add('Quyền duyệt chỉ trong công ty đang làm', 'P0', [ACC_H, DATA], [MENU_CD], '—',
            ['H chỉ thấy %s (TPSG)' % P6, 'Không thấy %s của TPE dù cũng Chờ duyệt' % P2])

    sections = [
        ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
        ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
        ('III', 'THÊM MỚI', S3),
        ('IV', 'CHỈNH SỬA', S4),
        ('V', 'GỬI DUYỆT', S5),
        ('VI', 'DUYỆT PHIẾU / HỦY DUYỆT', S6),
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

    desc = [
        ('1. Mục đích tính năng',
         '%s (#11643, phân hệ Bán hàng > Kế hoạch > Giao chỉ tiêu kinh doanh): công ty giao chỉ tiêu năm cho từng phòng (tuỳ chọn chia '
         'tới bộ phận) theo khối kinh doanh, vùng, Tỉnh/TP; mỗi chỉ tiêu gồm SL khách và Doanh số, tách Khách hãng / Khách khác, '
         'Hàng hóa / Dịch vụ. Phiếu được duyệt là nguồn "Chỉ tiêu giao" của phiếu giao chỉ tiêu theo nhân viên. Bỏ phần nhập chi tiết '
         'khách hàng của hệ thống cũ: 8 ô số nhập thẳng trên dòng.' % TEN),
        ('2. Đối tượng được tính / hiển thị',
         '- Trạng thái: Đang tạo, Chờ duyệt, Đã duyệt, Hủy (Từ chối và Hủy duyệt đưa phiếu về Đang tạo).\n'
         '- Lối vào danh sách ("Theo phòng ban"): phiếu mình lập (mọi trạng thái) + phiếu trong phạm vi quyền %s + phiếu Chờ duyệt của '
         'công ty đang làm (nếu có quyền %s) + phiếu mình đã duyệt.\n'
         '- Lối vào "Giao chỉ tiêu chờ duyệt" (nhóm Phê Duyệt): chỉ phiếu Chờ duyệt của công ty đang làm, cần quyền %s.\n'
         '- Phiếu lập trên hệ thống cũ (Đã duyệt, có chi tiết khách hàng cũ) vẫn hiện đủ số.' % (QV, QA, QA)),
        ('3. Đối tượng bị ẩn / không tính',
         '- Phiếu Đang tạo của người khác (kể cả với quyền xem mức Tổng công ty).\n'
         '- Phiếu công ty khác khi quyền xem chỉ mức Công ty; mọi phiếu người khác khi không có quyền xem.\n'
         '- Ô chọn: khối của công ty khác / đã ngừng; phòng không thuộc khối / đã ngừng / đã chọn ở dòng khác cùng tỉnh; bộ phận đã ngừng / đã chọn trong cùng phòng.\n'
         '- Kiểm trùng năm: phiếu Hủy không tính. Năm trước: chỉ lấy phiếu Đã duyệt.\n'
         '- Dòng phòng / bộ phận trống (chưa chọn, không có số) bị bỏ khi lưu.'),
        ('4. Bộ lọc thời gian áp dụng cho',
         '- Ô Năm ở danh sách: năm của phiếu, lựa chọn từ năm nay +2 (2028) xuống 2023.\n'
         '- Ô Năm ở form: 2025 tới 2036 (nới thêm nếu năm của phiếu nằm ngoài), mặc định năm hiện tại.\n'
         '- Năm trước = phiếu năm liền trước Đã duyệt cùng công ty, cùng khối.'),
        ('5. Cấu trúc dữ liệu / cây phân cấp',
         '- Phiếu (1 công ty, 1 năm) > Khối kinh doanh (mỗi khối 1 tab) > Khu vực (vùng, bung ra các Tỉnh/TP) > Tỉnh/TP > Phòng ban > Bộ phận (tuỳ chọn).\n'
         '- Mỗi Tỉnh/TP: dòng tỉnh (STT La Mã, "<tỉnh> (n phòng)") > dòng Năm trước (chỉ đọc, nghiêng) > dòng phòng (1, 2...) > dòng bộ phận (1.1, 1.2...).\n'
         '- 12 cột 3 tầng: Khách hãng / Khách khác / Tổng cộng × Hàng hóa / Dịch vụ × SL khách / Doanh số; nhóm Tổng cộng tự tính.\n'
         '- Tab Tổng hợp: Tỉnh/TP > Năm trước, các khối.'),
        ('6. Quy tắc cộng dồn / deduplicate',
         '- Tổng cộng = Khách hãng + Khách khác. Phòng đã chia bộ phận = tổng các bộ phận (8 ô chỉ đọc). Tỉnh = tổng các phòng. TỔNG khối = tổng các tỉnh.\n'
         '- Tổng hợp: mỗi tỉnh 1 dòng = cộng các khối có tỉnh đó.\n'
         '- Mỗi công ty mỗi năm chỉ 1 phiếu hiệu lực (Đang tạo / Chờ duyệt / Đã duyệt).\n'
         '- Phiếu theo nhân viên lấy chỉ tiêu phòng = cộng các dòng của phòng đó trong cùng tỉnh (ở mọi khối) của phiếu Đã duyệt.'),
        ('7. Phân quyền cấp',
         '- %s — mức: Công ty / Tổng công ty (dùng chung cho phiếu theo phòng ban và theo nhân viên; mức Tổng công ty có thêm ô lọc Công ty).\n'
         '- %s: Tạo mới; Sửa / Gửi duyệt / Hủy phiếu phiếu do chính mình lập.\n'
         '- %s: Duyệt / Từ chối / Hủy duyệt phiếu của công ty đang làm; hiện mục "Giao chỉ tiêu chờ duyệt".\n'
         '- Không có quyền nào: vẫn mở được màn, chỉ thấy phiếu mình lập. Không có đặc quyền cho vai trò quản trị cao nhất; quyền tính theo công ty đang làm việc.'
         % (QV, QC, QA)),
        ('8. Cách tính các ô thống kê',
         '- Góc phải khối Chi tiết và dòng TỔNG của khối: "<n> Tỉnh/TP · <n> phòng · <n> bộ phận" (chỉ đếm dòng đã chọn phòng / bộ phận).\n'
         '- Dòng tỉnh: "<tỉnh> (<số phòng đã chọn> phòng)".\n'
         '- Điều kiện gửi duyệt: tổng Doanh số (Hàng hóa + Dịch vụ, cả Khách hãng lẫn Khách khác) của phiếu > 0.\n'
         '- Danh sách: dòng tổng "a–b trên N phiếu"; Người duyệt / Ngày duyệt = lần duyệt gần nhất.'),
        ('9. Ghi chú đọc bảng',
         '- Số nguyên, dấu phẩy ngăn nghìn 1,234,567; ô 0 ở dòng phòng / bộ phận / Năm trước để trống, dòng tỉnh và dòng TỔNG hiện 0.\n'
         '- Mỗi ô tối đa 13 chữ số; không nhận dấu trừ, chữ; dán "1,234" hoặc "1.234" đều thành 1,234.\n'
         '- Lưu chỉ bắt buộc Năm, Khối, Khu vực; cặp SL khách / Doanh số và "mỗi khối có ít nhất 1 phòng" chỉ kiểm khi Lưu và gửi.\n'
         '- Không có Xóa phiếu (thay bằng Hủy phiếu ở Đang tạo / Chờ duyệt); phiếu Đã duyệt muốn sửa phải Hủy duyệt trước.\n'
         '- Hủy duyệt bị chặn khi đã có phiếu giao chỉ tiêu theo nhân viên Chờ duyệt / Đã duyệt dùng chỉ tiêu của phiếu.\n'
         '- Năm trước ở màn Xem là số chụp lúc lưu; ở form Tạo / Sửa luôn tính lại theo phiếu năm trước hiện tại.\n'
         '- Các ca có 2 thẻ / 2 tài khoản cần chuẩn bị dữ liệu như Tiền điều kiện; dữ liệu mẫu dùng số phiếu minh hoạ, thay bằng số thật khi chạy.'),
    ]
    return desc, sections


# ============================================================================ KIỂM THUẬT NGỮ (skill)
BANNED = [
    r"`[a-z_]{3,}`", r"\bBE\b", r"\bFE\b", r"\bHTTP\b",
    r"trả (400|403|404|422)", r"\b(400|403|404|422)\b",
    r"permission id", r"/api/v1", r"\bAPI /", r"localStorage",
    r"number_format", r"meta\.", r"sort_by", r"per_page",
    r"role_has_permissions", r"current_company_role",
    r"\bERP\b", r"\bAPI\b", r"https?://", r"\?type=", r"is_can_", r"for-approve", r"Super Admin",
]


def check_terms(desc, sections):
    blob = [b for _, b in desc] + [x for _, _, s in sections for tc in s for x in tc[1:]]
    text_all = '\n'.join(blob)
    found = {p: len(re.findall(p, text_all)) for p in BANNED if re.findall(p, text_all)}
    emo = re.findall(u'[←-⯿☀-➿️\U0001F300-\U0001FAFF]', text_all)
    if emo:
        found['emoji/mui ten'] = sorted(set(emo))
    print('!!! CON THUAT NGU KY THUAT:', found) if found else print('OK - sach')
    return not found


if __name__ == '__main__':
    desc, sections = make()
    ids = [(r, tc[0]) for r, _, s in sections for tc in s]
    assert len(ids) == len(set(ids)), 'Trùng mã TC'
    total = len(ids)
    p0 = sum(1 for _, _, s in sections for tc in s if tc[2] == 'P0')
    print('==', TEN)
    print('Tong %d TC, P0 %d (%.1f%%)' % (total, p0, 100.0 * p0 / total))
    for r, t, s in sections:
        print('  %-5s %-55s %3d' % (r, t, len(s)))
    ok = check_terms(desc, sections)
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='%s - Cập nhật ngày %s' % (TEN, TODAY), module_name=MODULE,
                description_block=desc, sections=[(r, t, list(s)) for r, t, s in sections], loai='phieu')
    sys.exit(0 if ok else 1)

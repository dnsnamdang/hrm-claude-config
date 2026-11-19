# -*- coding: utf-8 -*-
"""Testcase 2 màn "Kế hoạch bán hàng của nhân viên" (#11884) + "Kế hoạch phát triển thị trường của nhân viên" (#11885)
— skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu'). Mỗi màn 1 file.

Chạy: python gen_testcase.py -> 2 file "testcase - Ke hoach ... .xlsx" (tự chạy check_tc, phải "DAT", 0 lỗi + bộ lọc thuật ngữ).
Hai màn dùng chung khung (danh sách / form 3 tab / luồng duyệt / lấy dữ liệu chéo) => 1 hàm make(P) có tham số theo kế hoạch,
gọi 2 lần. Cột số khác nhau: KHBH (DS tiêu chuẩn quyết toán, Doanh số xuất hàng, SL khách, HĐ hàng hóa / dịch vụ: SL HĐ + DS
tiêu chuẩn), KHTT (SL khách, Báo giá hàng hóa / dịch vụ: SL + Giá trị).
Nhóm: I Hiển thị (2 lối vào) · II Tìm kiếm & lọc · III Thêm mới · IV Chỉnh sửa · V Gửi duyệt · VI Duyệt phiếu (TP duyệt + Gửi BGĐ)
· VII Không duyệt (Từ chối) · VIII Hủy phiếu · IX Lịch sử · X Xem chi tiết (3 tab, phiếu cũ) · XI In · XII Tùy chỉnh cột · XIII Xuất
Excel (danh sách + 1 phiếu) · XIV Ràng buộc (chỉ tiêu, lấy dữ liệu chéo, nhân viên mới, yêu cầu issue) · XV Phân quyền (cuối).
Nguồn hành vi (đọc 18/11/2026, nhánh feat/ke-hoach-nhan-vien = develop): BE Modules/Finance EmployeePlan* (Entity, Service,
Converter, TargetService, BaseController, Request), Catalog sale.php; FE components/employee-plan/*, utils/employee-plan.js,
utils/mixins/employeePlanActionsMixin.js, utils/export/employeePlanExcel.js, pages/finance/{sale,market}-plan-employees, sale-hub.js.
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

TODAY = '18/11/2026'

# ============================================================================ CẤU HÌNH THEO KẾ HOẠCH
COMMON = dict(
    MENU_HUB='Vào phân hệ Bán hàng > nhóm "Kế hoạch"',
    ADV='Bấm Tìm kiếm nâng cao.',
)

KINDS = {
    'sale': dict(
        file='testcase - Kế hoạch bán hàng của nhân viên.xlsx',
        TEN='Kế hoạch bán hàng của nhân viên', ten='kế hoạch bán hàng của nhân viên', kh='kế hoạch bán hàng',
        UP='KẾ HOẠCH BÁN HÀNG CỦA NHÂN VIÊN', issue='#11884', module='KH bán hàng của NV',
        MUC='Kế hoạch bán hàng', MAN='Của nhân viên', SIB='"Của nhân viên", "Của phòng ban", "Của công ty"',
        CD='KH bán hàng chờ duyệt',
        OTHER='KH phát triển thị trường', OTHER_TEN='Kế hoạch phát triển thị trường của nhân viên',
        OTHER_MENU='Vào phân hệ Bán hàng > nhóm "Kế hoạch" > mục "Kế hoạch phát triển thị trường" > bấm "Theo nhân viên".',
        PFX='KHBHNV', base=700, LEGACY='TPE_KHBHNV_STT-01076', LEGACY_NEW='TPE_KHBHNV_STT-01050',
        Q_VIEW='Xem danh sách kế hoạch bán hàng', Q_APP='Trưởng phòng duyệt kế hoạch bán hàng nhân viên',
        Q_VIEW_OTHER='Xem danh sách lập kế hoạch thị trường',
        Q_APP_OTHER='Trưởng phòng duyệt kế hoạch thị trường nhân viên',
        FORM_COLS=['STT', 'Tháng / Tỉnh/TP (có dấu * đỏ)', 'DS tiêu chuẩn quyết toán', 'Doanh số xuất hàng', 'SL khách (có dấu * đỏ)',
                   'Nhóm "Hợp đồng hàng hóa": SL HĐ, DS tiêu chuẩn', 'Nhóm "Hợp đồng dịch vụ": SL HĐ, DS tiêu chuẩn',
                   'Nhóm "Tổng cộng": SL HĐ, DS tiêu chuẩn (tự tính, không nhập)'],
        LIST_NUM='SL khách, SL HĐ, DS tiêu chuẩn', LIST_HID='DSTC quyết toán, DS xuất hàng',
        HN=['Tháng 11 - dòng Hà Nội:', 'DS tiêu chuẩn quyết toán: 1,200,000,000', 'Doanh số xuất hàng: 1,000,000,000', 'SL khách: 5',
            'Hợp đồng hàng hóa: SL HĐ 3, DS tiêu chuẩn 1,500,000,000', 'Hợp đồng dịch vụ: SL HĐ 2, DS tiêu chuẩn 300,000,000'],
        HP=['Tháng 12 - dòng Hải Phòng:', 'SL khách: 2', 'Hợp đồng hàng hóa: SL HĐ 1, DS tiêu chuẩn 450,000,000'],
        HN_TOT='Cột Tổng cộng dòng Hà Nội tự hiện SL HĐ 5, DS tiêu chuẩn 1,800,000,000',
        M_TOT='SL khách 7, SL HĐ 6, DS tiêu chuẩn 2,250,000,000 (DSTC quyết toán 1,200,000,000, DS xuất hàng 1,000,000,000)',
        M_LIST='SL khách 7, SL HĐ 6, DS tiêu chuẩn 2,250,000,000',
        M_ROW_TOT='Dòng TỔNG: SL khách 7, Hợp đồng hàng hóa SL HĐ 4 / DS tiêu chuẩn 1,950,000,000, Hợp đồng dịch vụ 2 / 300,000,000, '
                  'Tổng cộng 6 / 2,250,000,000, DS tiêu chuẩn quyết toán 1,200,000,000, Doanh số xuất hàng 1,000,000,000',
        KHACH=7, M11='Tháng 11 (5 khách)', M12='Tháng 12 (2 khách)',
        Q1='SL HĐ của nhóm Hợp đồng hàng hóa', V1='DS tiêu chuẩn của nhóm Hợp đồng hàng hóa',
        Q2='SL HĐ của nhóm Hợp đồng dịch vụ', V2='DS tiêu chuẩn của nhóm Hợp đồng dịch vụ',
        NO_SEND='Phiếu chưa có DS tiêu chuẩn hợp đồng — không gửi được', SEND_COL='DS tiêu chuẩn',
        ONLY_KHACH='Tháng 11 - Hà Nội: SL khách 5, các ô khác để trống',
        TARGET_TAB=[
            'Ngay dưới dòng TỔNG có dòng "Chỉ tiêu giao" (ghim cùng tiêu đề): SL khách 10, DS tiêu chuẩn Hợp đồng hàng hóa 3,100,000,000, '
            'Hợp đồng dịch vụ 700,000,000, Tổng cộng DS tiêu chuẩn 3,800,000,000; các ô còn lại để trống',
            'Mỗi Tỉnh/TP có dòng "Chỉ tiêu giao" ngay dưới: Hà Nội SL khách 6, DS hàng hóa 2,000,000,000, DS dịch vụ 500,000,000, tổng '
            '2,500,000,000; Hải Phòng 3 / 800,000,000 / 200,000,000 / 1,000,000,000',
            'Dòng Tỉnh/TP: 1 Hà Nội (số của tháng 11), con 1.1 "Tháng 11"; 2 Hải Phòng, con 2.1 "Tháng 12"; 3 Quảng Ninh (chỉ có dòng Chỉ '
            'tiêu giao SL khách 1, DS hàng hóa 300,000,000, chưa có tháng)',
            'KHÔNG có 4 cột chỉ tiêu bên phải (cột này chỉ có ở kế hoạch phát triển thị trường)'],
        UNDER=('Phiếu M lập DS tiêu chuẩn Hà Nội 1,800,000,000, thấp hơn chỉ tiêu giao Hà Nội 2,500,000,000.'),
        CV_SRC=('Phiếu kế hoạch phát triển thị trường TT1 của A (TPE_KHTTNV_2026.00660, TP đã duyệt 10/11/2026, năm 2026): Tháng 11 Hà Nội '
                'SL khách 15, Báo giá hàng hóa SL 9 / Giá trị 4,500,000,000, Báo giá dịch vụ SL 6 / Giá trị 900,000,000; Tháng 12 Hải Phòng '
                'SL khách 6, Báo giá hàng hóa SL 3 / Giá trị 1,350,000,000.'),
        CV_SRC_CODE='TPE_KHTTNV_2026.00660',
        CV_RESULT=['Tháng 11 Hà Nội: SL khách 5 (= SL HĐ hàng hóa 3 + dịch vụ 2), Hợp đồng hàng hóa SL HĐ 3 / DS tiêu chuẩn 1,500,000,000, '
                   'Hợp đồng dịch vụ 2 / 300,000,000, DS tiêu chuẩn quyết toán 1,800,000,000, Doanh số xuất hàng 1,800,000,000',
                   'Tháng 12 Hải Phòng: SL khách 1, Hợp đồng hàng hóa SL HĐ 1 / DS tiêu chuẩn 450,000,000, DS tiêu chuẩn quyết toán '
                   '450,000,000, Doanh số xuất hàng 450,000,000',
                   'Bảng xem trước có cột Tháng, Tỉnh/TP, SL khách, SL HĐ, DS tiêu chuẩn, DS quyết toán, DS xuất hàng; dòng Tổng: 6, 6, '
                   '2,250,000,000, 2,250,000,000, 2,250,000,000'],
        CV_HINT='chia cho hệ số: SL HĐ = SL báo giá ÷ hệ số; DS tiêu chuẩn = Giá trị báo giá ÷ hệ số',
        CV_ROUND_PRE=('Phiếu kế hoạch phát triển thị trường TT2 của A (TP đã duyệt, 2026): Tháng 12 Quảng Ninh SL khách 3, Báo giá hàng hóa '
                      'SL 1 / Giá trị 2,000,000, Báo giá dịch vụ SL 4 / Giá trị 1,000.'),
        CV_ROUND_EXP=['Hợp đồng hàng hóa: SL HĐ 1 (1 ÷ 3 làm tròn ra 0 nhưng tối thiểu 1 khi có báo giá), DS tiêu chuẩn 667,000 '
                      '(2,000,000 ÷ 3 làm tròn tới nghìn)',
                      'Hợp đồng dịch vụ: SL HĐ 1 (4 ÷ 3 = 1.33 làm tròn 1), DS tiêu chuẩn 1,000 (1,000 ÷ 3 làm tròn ra 0 nhưng tối thiểu 1,000)',
                      'SL khách 2 (= 1 + 1), DS tiêu chuẩn quyết toán = Doanh số xuất hàng = 668,000'],
        ISSUE_COLS=('Bảng nhập trên dòng Tỉnh/TP có đủ: SL khách, SL HĐ (hàng hóa / dịch vụ / tổng), DS tiêu chuẩn hợp đồng (hàng hóa / '
                    'dịch vụ / tổng), DS tiêu chuẩn quyết toán, Doanh số xuất hàng'),
        GIA_TRI_HD=True,
    ),
    'market': dict(
        file='testcase - Kế hoạch phát triển thị trường của nhân viên.xlsx',
        TEN='Kế hoạch phát triển thị trường của nhân viên', ten='kế hoạch phát triển thị trường của nhân viên',
        kh='kế hoạch phát triển thị trường', UP='KẾ HOẠCH PHÁT TRIỂN THỊ TRƯỜNG CỦA NHÂN VIÊN', issue='#11885',
        module='KH phát triển thị trường của NV',
        MUC='Kế hoạch phát triển thị trường', MAN='Theo nhân viên', SIB='"Theo nhân viên", "Theo phòng ban", "Theo công ty"',
        CD='KH PTTT chờ duyệt',
        OTHER='KH bán hàng', OTHER_TEN='Kế hoạch bán hàng của nhân viên',
        OTHER_MENU='Vào phân hệ Bán hàng > nhóm "Kế hoạch" > mục "Kế hoạch bán hàng" > bấm "Của nhân viên".',
        PFX='KHTTNV', base=650, LEGACY='TPE_KHTTNV_STT-01007', LEGACY_NEW='TPE_KHTTNV_STT-00980',
        Q_VIEW='Xem danh sách lập kế hoạch thị trường', Q_APP='Trưởng phòng duyệt kế hoạch thị trường nhân viên',
        Q_VIEW_OTHER='Xem danh sách kế hoạch bán hàng',
        Q_APP_OTHER='Trưởng phòng duyệt kế hoạch bán hàng nhân viên',
        FORM_COLS=['STT', 'Tháng / Tỉnh/TP (có dấu * đỏ)', 'SL khách (có dấu * đỏ)', 'Nhóm "Báo giá hàng hóa": SL, Giá trị',
                   'Nhóm "Báo giá dịch vụ": SL, Giá trị', 'Nhóm "Tổng cộng": SL, Giá trị (tự tính, không nhập)'],
        LIST_NUM='SL khách, SL báo giá, Giá trị báo giá', LIST_HID='',
        HN=['Tháng 11 - dòng Hà Nội:', 'SL khách: 15', 'Báo giá hàng hóa: SL 9, Giá trị 4,500,000,000',
            'Báo giá dịch vụ: SL 6, Giá trị 950,000,000'],
        HP=['Tháng 12 - dòng Hải Phòng:', 'SL khách: 6', 'Báo giá hàng hóa: SL 3, Giá trị 1,350,000,000'],
        HN_TOT='Cột Tổng cộng dòng Hà Nội tự hiện SL 15, Giá trị 5,450,000,000',
        M_TOT='SL khách 21, SL báo giá 18, Giá trị báo giá 6,800,000,000',
        M_LIST='SL khách 21, SL báo giá 18, Giá trị báo giá 6,800,000,000',
        M_ROW_TOT='Dòng TỔNG: SL khách 21, Báo giá hàng hóa SL 12 / Giá trị 5,850,000,000, Báo giá dịch vụ 6 / 950,000,000, '
                  'Tổng cộng 18 / 6,800,000,000',
        KHACH=21, M11='Tháng 11 (15 khách)', M12='Tháng 12 (6 khách)',
        Q1='SL của nhóm Báo giá hàng hóa', V1='Giá trị của nhóm Báo giá hàng hóa',
        Q2='SL của nhóm Báo giá dịch vụ', V2='Giá trị của nhóm Báo giá dịch vụ',
        NO_SEND='Phiếu chưa có giá trị báo giá — không gửi được', SEND_COL='Giá trị báo giá',
        ONLY_KHACH='Tháng 11 - Hà Nội: SL khách 15, các ô báo giá để trống',
        TARGET_TAB=[
            'Bên phải bảng có thêm 4 cột: "Chỉ tiêu giao — Hàng hóa" (SL khách, Doanh số) và "Chỉ tiêu giao — Dịch vụ" (SL khách, Doanh số)',
            'Dòng TỔNG ở 4 cột chỉ tiêu: 7 / 3,100,000,000 / 3 / 700,000,000',
            'Hà Nội: 4 / 2,000,000,000 / 2 / 500,000,000; Hải Phòng: 2 / 800,000,000 / 1 / 200,000,000; Quảng Ninh: 1 / 300,000,000 / 0 / 0',
            'Dòng Tỉnh/TP: 1 Hà Nội (số của tháng 11), con 1.1 "Tháng 11"; 2 Hải Phòng, con 2.1 "Tháng 12"; 3 Quảng Ninh (số kế hoạch '
            'bằng 0, không có tháng)',
            'KHÔNG có dòng "Chỉ tiêu giao" xen giữa các dòng (cách hiển thị đó chỉ có ở kế hoạch bán hàng)'],
        UNDER=('Phiếu M lập 15 khách ở Hà Nội; chỉ tiêu giao Hà Nội 6 khách (4 hàng hóa + 2 dịch vụ), giá trị báo giá cao hơn doanh số chỉ '
               'tiêu — số kế hoạch và chỉ tiêu lệch nhau tuỳ ý.'),
        CV_SRC=('Phiếu kế hoạch bán hàng BH1 của A (TPE_KHBHNV_2026.00710, TP đã duyệt 10/11/2026, năm 2026): Tháng 11 Hà Nội SL khách 5, '
                'Hợp đồng hàng hóa SL HĐ 3 / DS tiêu chuẩn 1,500,000,000, Hợp đồng dịch vụ 2 / 300,000,000; Tháng 12 Hải Phòng SL khách '
                '2, Hợp đồng hàng hóa 1 / 450,000,000.'),
        CV_SRC_CODE='TPE_KHBHNV_2026.00710',
        CV_RESULT=['Tháng 11 Hà Nội: SL khách 15 (= 5 × 3), Báo giá hàng hóa SL 9 / Giá trị 4,500,000,000, Báo giá dịch vụ SL 6 / '
                   'Giá trị 900,000,000',
                   'Tháng 12 Hải Phòng: SL khách 6, Báo giá hàng hóa SL 3 / Giá trị 1,350,000,000',
                   'Bảng xem trước có cột Tháng, Tỉnh/TP, SL khách, SL báo giá, Giá trị báo giá; dòng Tổng: 21, 18, 6,750,000,000'],
        CV_HINT='nhân với hệ số: SL báo giá = SL HĐ × hệ số; Giá trị = DS tiêu chuẩn × hệ số',
        CV_ROUND_PRE=('Phiếu kế hoạch bán hàng BH2 của A (TP đã duyệt, 2026): Tháng 12 Quảng Ninh SL khách 1, Hợp đồng hàng hóa SL HĐ 2 / '
                      'DS tiêu chuẩn 150,000,000.'),
        CV_ROUND_EXP=['Hệ số 7: SL khách 7, Báo giá hàng hóa SL 14 / Giá trị 1,050,000,000 (nhân thẳng, không làm tròn)',
                      'Báo giá dịch vụ để trống (nguồn bằng 0)'],
        ISSUE_COLS='Bảng nhập trên dòng Tỉnh/TP có đủ: SL khách, SL báo giá (hàng hóa / dịch vụ / tổng), Giá trị báo giá (hàng hóa / dịch vụ / tổng)',
        GIA_TRI_HD=False,
    ),
}


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


def make(P):
    P = dict(COMMON, **P)
    MENU = '%s > mục "%s" > bấm "%s".' % (P['MENU_HUB'], P['MUC'], P['MAN'])
    MENU_CD = 'Vào phân hệ Bán hàng > nhóm "Phê Duyệt" > mục "Kế hoạch & chỉ tiêu" > bấm "%s".' % P['CD']
    ADV = P['ADV']
    TEN, ten, kh, PFX = P['TEN'], P['ten'], P['kh'], P['PFX']
    LIST_TITLE = 'Danh sách ' + ten
    EMPTY = '"Không có %s nào"' % kh
    QV, QA = '"%s"' % P['Q_VIEW'], '"%s"' % P['Q_APP']

    def C(n):  # số phiếu mẫu
        return 'TPE_%s_2026.%05d' % (PFX, P['base'] + n)

    M, P2, P3, P4, P5, P6, P7, P8 = (C(1), C(2), C(3), C(4), C(5), C(6), C(7), C(8))
    BLOCK_TITLE = '"Chưa thể lập %s"' % kh
    BLOCK_MSG = ('"Tài khoản của bạn chưa có phiếu giao chỉ tiêu kinh doanh Đã duyệt cho năm 2026 trở đi nên chưa thể lập %s. Vui lòng '
                 'liên hệ trưởng phòng để được giao chỉ tiêu."' % kh)
    NOPERM = '"Bạn không có quyền thực hiện thao tác này"'
    LOCKED = '"Chỉ sửa được phiếu ở trạng thái Đang tạo."'
    CHECK = '"Vui lòng kiểm tra lại dữ liệu nhập"'
    REQ = '"Bắt buộc phải nhập"'
    UNSAVED = 'hộp "Thông tin chưa lưu" với nội dung "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?", 2 nút Ở lại / Thoát'

    ACC_A = ('Tài khoản A (Nguyễn Văn A): nhân viên phòng Kinh doanh 1 (KD1), bộ phận Nhóm KD1-1, công ty TPE; không có quyền nào '
             'của màn.\nA có phiếu giao chỉ tiêu kinh doanh theo nhân viên Đã duyệt năm 2026 gồm 3 tỉnh: Hà Nội (hàng hóa 4 khách / '
             '2,000,000,000, dịch vụ 2 khách / 500,000,000), Hải Phòng (2 / 800,000,000, 1 / 200,000,000), Quảng Ninh (1 / '
             '300,000,000, dịch vụ 0); và phiếu Đã duyệt năm 2027 gồm Hà Nội.')
    ACC_A_S = 'Tài khoản A (nhân viên phòng KD1, có chỉ tiêu Đã duyệt 2026: Hà Nội, Hải Phòng, Quảng Ninh; 2027: Hà Nội).'
    ACC_B = ('Tài khoản B (Trần Văn B): trưởng phòng quản lý phòng KD1, có quyền %s; B có chỉ tiêu Đã duyệt năm 2026 tỉnh Đà Nẵng.' % QA)
    ACC_C = ('Tài khoản C: nhân viên phòng KD1, chỉ có phiếu giao chỉ tiêu Đã duyệt năm 2025; năm 2026 có phiếu giao chỉ tiêu đang Chờ '
             'duyệt (chưa Đã duyệt).')
    ACC_D = 'Tài khoản D: trưởng bộ phận quản lý bộ phận Nhóm KD1-1 (phòng KD1), không có quyền nào của màn.'
    ACC_G = 'Tài khoản G: nhân viên phòng KD1 (KHÔNG quản lý phòng), có quyền %s.' % QA
    ACC_H = 'Tài khoản H: trưởng phòng quản lý phòng KD2, có quyền %s.' % QA
    DATA = ('Bộ dữ liệu thử năm 2026 (ngoài các phiếu này không còn phiếu nào năm 2026):\n'
            '- Phòng KD1: %s (A, Đang tạo, phiếu M), %s (A, Chờ TP duyệt), %s (A, TP đã duyệt), %s (A2 bộ phận Nhóm KD1-2, Chờ TP '
            'duyệt), %s (A2, Đang tạo), %s (B tự lập, Chờ BGĐ duyệt)\n'
            '- Phòng KD2: %s (E, Chờ TP duyệt)\n- Công ty TPSG: %s (X, TP đã duyệt)' % (M, P2, P3, P4, P5, P6, P7, P8))
    PLAN_M = ('Phiếu M %s của A (năm 2026, Đang tạo, lập %s): %s; %s.' %
              (M, TODAY, ' '.join(P['HN']), ' '.join(P['HP'])))
    PEND = 'Phiếu %s của A đang Chờ TP duyệt, %s.' % (P2, P['M_LIST'])
    HAPP = 'Phiếu %s của A đang TP đã duyệt (B duyệt 12/11/2026).' % P3
    OPEN_P2_B = [MENU_CD, 'Bấm số phiếu %s.' % P2]

    # ======================================================================== I. HIỂN THỊ
    S1 = Sec()
    S1.add('Mở màn hình từ menu (lối vào danh sách)', 'P0', [ACC_A_S, DATA], [MENU], '—',
           ['Mở màn %s, tiêu đề trang "%s"' % (TEN, TEN), 'Bảng có tiêu đề "%s"' % LIST_TITLE,
            'Có đúng 3 phiếu của A: %s, %s, %s' % (M, P2, P3), 'Không thấy phiếu của A2, B, E, X'])
    S1.add('Mục menu nằm đúng nhóm Kế hoạch', 'P1', ACC_A_S, ['Vào phân hệ Bán hàng.', 'Bấm nhóm "Kế hoạch" ở menu trái.'], '—',
           ['Mục "%s" có 3 màn: %s' % (P['MUC'], P['SIB']), 'Chỉ "%s" mở màn; 2 màn còn lại báo đang phát triển' % P['MAN'],
            'Mục "%s" hiện với mọi tài khoản, không cần quyền' % P['MAN']])
    S1.add('Mở lối vào "%s" của trưởng phòng' % P['CD'], 'P0', [ACC_B, DATA], [MENU_CD], '—',
           ['Tiêu đề trang "%s chờ duyệt", bảng "%s chờ duyệt"' % (TEN, LIST_TITLE),
            'Có đúng 3 phiếu: %s, %s (Chờ TP duyệt), %s (TP đã duyệt) của phòng KD1' % (P2, P4, P3),
            'KHÔNG có %s (B tự lập), %s / %s (Đang tạo), %s (phòng KD2), %s (công ty khác)' % (P6, M, P5, P7, P8)])
    S1.add('Lối vào chờ duyệt không có Tạo mới và ô lọc Trạng thái', 'P1', ACC_B, [MENU_CD, ADV], '—',
           ['Không có nút Tạo mới', 'Bộ lọc nâng cao không có ô Trạng thái', 'Vẫn có nút Xuất Excel và Cấu hình cột hiển thị'])
    S1.add('Mục chờ duyệt ẩn khi thiếu quyền duyệt', 'P0', ACC_A_S,
           ['Vào phân hệ Bán hàng > nhóm "Phê Duyệt" > mục "Kế hoạch & chỉ tiêu".'], '—',
           ['KHÔNG có mục "%s"' % P['CD'], 'Lý do: A không có quyền %s' % QA])
    S1.add('Chuyển từ lối vào chờ duyệt sang lối vào danh sách', 'P0', [ACC_B, DATA], [MENU_CD, MENU], '—',
           ['Lối vào chờ duyệt: 3 phiếu', 'Sang lối vào danh sách: tiêu đề "%s", có 4 phiếu %s, %s, %s, %s' % (LIST_TITLE, P2, P3, P4, P6),
            'Phạm vi theo lối vào mới, không giữ phạm vi chờ duyệt'])
    S1.add('Đổi bộ lọc rồi mở lối vào khác', 'P0', [ACC_B, DATA],
           [MENU, ADV, 'Chọn Trạng thái: Chờ BGĐ duyệt, bấm Tìm kiếm.', MENU_CD], 'Trạng thái: Chờ BGĐ duyệt',
           ['Lối vào chờ duyệt vẫn ra đủ 3 phiếu (Chờ TP duyệt + TP đã duyệt), không bị lọc Chờ BGĐ duyệt về 0',
            'Ô Trạng thái không hiện ở lối vào chờ duyệt'])
    S1.add('Bấm Làm mới giữ phạm vi lối vào', 'P1', [ACC_B, DATA], [MENU_CD, 'Gõ "%s" vào ô tìm, bấm Tìm kiếm.' % P2, 'Bấm Làm mới.'],
           'Từ khoá: %s' % P2, ['Sau tìm: 1 phiếu', 'Sau Làm mới: ô tìm trống, quay về 3 phiếu chờ duyệt (không chuyển sang 4 phiếu của lối vào danh sách)'])
    S1.add('Tham số lối vào trên thanh địa chỉ bị sửa thành giá trị lạ', 'P1', [ACC_B, DATA],
           [MENU_CD, 'Sửa phần tham số lối vào trên thanh địa chỉ thành chữ "abc", nhấn Enter.'], 'Tham số: abc',
           ['Không lỗi trang', 'Màn quay về lối vào danh sách thường (tiêu đề "%s", 4 phiếu)' % LIST_TITLE, 'Không lộ thêm phiếu nào ngoài phạm vi của B'])
    S1.add('Các nút chức năng của danh sách', 'P1', ACC_A_S, [MENU], '—',
           ['Khối lọc: ô tìm "Tìm theo số phiếu, nhân viên", nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao',
            'Bảng: nút Tạo mới, Xuất Excel, Cấu hình cột hiển thị', 'KHÔNG có nút Xóa, Import'])
    S1.add('Cột mặc định với nhân viên chỉ xem phiếu của mình', 'P0', ACC_A_S, [MENU], '—',
           ['Cột hiện: STT, Số phiếu, Năm, %s, Ngày lập, Người duyệt, Trạng thái, Hành động' % P['LIST_NUM'],
            'Không hiện cột Nhân viên, Bộ phận (người chỉ thấy phiếu mình thì hiện Năm thay cho Nhân viên)'])
    S1.add('Cột mặc định với cấp trên', 'P0', ACC_B, [MENU], '—',
           ['Cột hiện: STT, Số phiếu, Nhân viên, %s, Ngày lập, Người duyệt, Trạng thái, Hành động' % P['LIST_NUM'],
            'Cột Năm và Bộ phận ẩn mặc định', 'Cột Nhân viên dạng "Họ tên - Mã phòng"'])
    hid = 'Bộ phận, Phòng ban, Người lập, Ngày duyệt' + (', ' + P['LIST_HID'] if P['LIST_HID'] else '')
    S1.add('Các cột ẩn mặc định', 'P1', ACC_B, [MENU, 'Bấm Cấu hình cột hiển thị.'], '—',
           ['Các cột đang bỏ chọn: %s, Năm' % hid, 'Bật lên thì cột hiện đúng dữ liệu'])
    S1.add('Dữ liệu dòng khớp phiếu đã lập', 'P0', [ACC_A_S, PLAN_M], [MENU, 'Tìm dòng %s.' % M], '—',
           ['Số phiếu %s, Năm 2026, %s' % (M, P['M_LIST']), 'Ngày lập %s, Người duyệt trống, Trạng thái Đang tạo' % TODAY,
            'Số có dấu phẩy ngăn nghìn (1,234,567), ô bằng 0 hiện 0 ở cột số'])
    S1.add('Người duyệt / Ngày duyệt là lần duyệt gần nhất', 'P1', [ACC_A_S, HAPP], [MENU, 'Bật cột Ngày duyệt.', 'Tìm dòng %s.' % P3], '—',
           ['Người duyệt "Trần Văn B - KD1", Ngày duyệt 12/11/2026', 'Khi có BGĐ duyệt thì hiện người / ngày BGĐ duyệt thay cho TP'])
    S1.add('Trạng thái và màu nhãn', 'P1', [ACC_A_S, 'A có đủ 6 phiếu ở 6 trạng thái.'], [MENU], '—',
           ['Đang tạo màu xám, Chờ TP duyệt màu cam, TP đã duyệt màu xanh dương, Chờ BGĐ duyệt màu cam, BGĐ đã duyệt màu xanh lá, Hủy màu đỏ'])
    S1.add('Phiếu Đang tạo của người khác không hiện', 'P0', [ACC_B, DATA], [MENU, 'Tìm "%s" và "%s".' % (M, P5)], '—',
           ['Không thấy %s, %s dù thuộc phòng KD1 B quản lý' % (M, P5), 'Phiếu Đang tạo chỉ người lập thấy'])
    S1.add('Danh sách chưa có dữ liệu', 'P1', 'Tài khoản N: nhân viên mới, chưa lập phiếu, không quản lý ai, không có quyền.', [MENU], '—',
           ['Bảng hiện %s' % EMPTY, 'Không lỗi trang'])
    S1.add('Không có dữ liệu khớp bộ lọc', 'P1', ACC_A_S, [MENU, ADV, 'Chọn Năm 2030, bấm Tìm kiếm.'], 'Năm: 2030',
           ['Bảng hiện %s' % EMPTY, 'Tổng số bằng 0'])
    S1.add('Phân trang mặc định 10 dòng', 'P1', 'Tài khoản V4 (quyền %s mức Tổng công ty), thấy 25 phiếu.' % QV, [MENU], '—',
           ['Trang 1 có 10 dòng, dòng tổng ghi 1–10 trên 25 phiếu', 'Có 3 trang'])
    S1.add('Đổi số dòng / trang về trang 1', 'P1', 'Như trên, đang ở trang 2.', [MENU, 'Sang trang 2.', 'Đổi số dòng/trang thành 20.'], '20 dòng/trang',
           ['Về trang 1, hiện 20 dòng, còn 2 trang'])
    S1.add('Trang trước / sau, đầu / cuối', 'P2', 'Như trên (25 phiếu, 10 dòng/trang).', [MENU, 'Bấm trang sau, trang cuối, trang trước, trang đầu.'], '—',
           ['Mỗi lần bấm đổi đúng trang', 'Ở trang 1 nút trang trước / trang đầu không bấm được; ở trang 3 nút trang sau / trang cuối không bấm được'])
    S1.add('STT liên tục giữa các trang', 'P2', 'Như trên.', [MENU, 'Sang trang 2.'], '—', ['Trang 2 có STT từ 11 tới 20'])
    S1.add('Sắp xếp mặc định theo Ngày lập mới trước', 'P0', 'Tài khoản A: 3 phiếu lập 01/11, 10/11, %s.' % TODAY, [MENU], '—',
           ['Phiếu lập %s đứng đầu, 01/11 cuối' % TODAY])
    S1.add('Sắp xếp tăng / giảm theo cột', 'P1', 'Như trên.', [MENU, 'Bấm tiêu đề cột Số phiếu 2 lần.', 'Bấm tiêu đề cột SL khách.'], '—',
           ['Số phiếu tăng dần rồi giảm dần', 'Cột số sắp theo giá trị số (không theo chữ)', 'Các cột Năm, Nhân viên, Ngày lập, Người duyệt, Trạng thái cũng sắp xếp được'])
    S1.add('Cột không hỗ trợ sắp xếp', 'P2', ACC_A_S, [MENU, 'Bấm tiêu đề cột STT, Hành động.'], '—', ['Không đổi thứ tự, không có mũi tên sắp xếp'])
    S1.add('Giữ sắp xếp khi chuyển trang, về trang 1 khi đổi sắp xếp', 'P2', 'Tài khoản V4, 25 phiếu.',
           [MENU, 'Sắp Số phiếu tăng dần.', 'Sang trang 2.', 'Bấm sắp Số phiếu giảm dần.'], '—',
           ['Trang 2 vẫn theo Số phiếu tăng dần', 'Đổi sắp xếp thì về trang 1'])
    S1.add('Phiếu lập trên hệ thống cũ hiện trên danh sách', 'P0',
           [ACC_A_S, 'Phiếu cũ %s do A lập năm 2026, BGĐ đã duyệt, có 2 dòng Tỉnh/TP (Hà Nội 4 khách, Hải Phòng 3 khách khác nhau).' % P['LEGACY']],
           [MENU, 'Tìm "%s".' % P['LEGACY']], '—',
           ['Dòng hiện bình thường, trạng thái BGĐ đã duyệt', 'SL khách = 7 (cộng số khách khác nhau của từng dòng Tỉnh/TP)',
            'Hành động chỉ có Xem, In (3 kiểu), Xuất Excel, Lịch sử'])
    S1.add('Hành động ở dòng thay đổi theo trạng thái', 'P0', [ACC_A_S, DATA], [MENU, 'Bấm biểu tượng ba chấm ở cột Hành động từng dòng.'], '—',
           ['%s (Đang tạo): biểu tượng Sửa, Xem, Gửi duyệt, Hủy phiếu, In chi tiết, In theo thị trường, In theo tháng, Xuất Excel, Lịch sử' % M,
            '%s (Chờ TP duyệt): Xem, Hủy phiếu, 3 kiểu In, Xuất Excel, Lịch sử (không có Sửa, Gửi duyệt)' % P2,
            '%s (TP đã duyệt): Xem, 3 kiểu In, Xuất Excel, Lịch sử' % P3])
    S1.add('Bấm số phiếu mở màn Xem', 'P1', ACC_A_S, [MENU, 'Bấm số phiếu %s.' % P2], '—',
           ['Mở màn "Chi tiết %s: %s"' % (ten, P2)])

    # ======================================================================== II. TÌM KIẾM & LỌC
    S2 = Sec()
    S2.add('Tìm đúng số phiếu', 'P0', [ACC_B, DATA], [MENU, 'Gõ "%s", bấm Tìm kiếm.' % P4], 'Từ khoá: %s' % P4, ['Chỉ còn 1 dòng %s' % P4])
    S2.add('Tìm một phần số phiếu', 'P1', [ACC_B, DATA], [MENU, 'Gõ "%s", bấm Tìm kiếm.' % P4[-5:]], 'Từ khoá: %s' % P4[-5:], ['Ra %s' % P4])
    S2.add('Tìm theo tên nhân viên', 'P0', [ACC_B, DATA, 'A2 tên Lê Thị Hoa.'], [MENU, 'Gõ "Lê Thị Hoa", bấm Tìm kiếm.'], 'Từ khoá: Lê Thị Hoa',
           ['Ra %s (A2, Chờ TP duyệt); không ra %s vì Đang tạo' % (P4, P5)])
    S2.add('Không phân biệt hoa / thường', 'P2', [ACC_B, DATA], [MENU, 'Gõ "lê thị hoa".'], 'Từ khoá: lê thị hoa', ['Kết quả như tìm "Lê Thị Hoa"'])
    S2.add('Gõ không dấu', 'P2', [ACC_B, DATA], [MENU, 'Gõ "le thi hoa".'], 'Từ khoá: le thi hoa', ['Ra %s như tìm có dấu' % P4])
    S2.add('Từ khoá không tồn tại', 'P1', ACC_B, [MENU, 'Gõ "ZZZ999", bấm Tìm kiếm.'], 'Từ khoá: ZZZ999', ['Bảng hiện %s' % EMPTY])
    S2.add('Ký tự đặc biệt', 'P2', ACC_B, [MENU, 'Lần lượt tìm: %   _   \'   <b>'], "% ; _ ; ' ; <b>",
           ['Không lỗi trang, không treo', 'Tìm "%" chỉ ra phiếu có chứa ký tự % (ra toàn bộ danh sách là lỗi, ghi nhận)'])
    S2.add('Khoảng trắng đầu / cuối', 'P2', [ACC_B, DATA], [MENU, 'Gõ "   %s   ", bấm Tìm kiếm.' % P4], 'Có 3 dấu cách hai đầu', ['Vẫn ra %s' % P4])
    S2.add('Từ khoá rất dài', 'P2', ACC_B, [MENU, 'Dán 300 ký tự vào ô tìm, bấm Tìm kiếm.'], '300 ký tự "a"', ['Không lỗi trang, ra danh sách rỗng'])
    S2.add('Xoá từ khoá', 'P2', [ACC_B, DATA], [MENU, 'Tìm "%s".' % P4, 'Xoá hết chữ trong ô tìm, bấm Tìm kiếm.'], '—', ['Quay về đủ 4 phiếu'])
    S2.add('Enter và nút Tìm kiếm', 'P1', [ACC_B, DATA], [MENU, 'Gõ "%s" rồi nhấn Enter.' % P2, 'Gõ lại rồi bấm nút Tìm kiếm.'], '—',
           ['Cả 2 cách đều ra 1 dòng %s' % P2, 'Gõ chưa bấm thì danh sách chưa lọc'])
    S2.add('Ô lọc với nhân viên chỉ xem phiếu mình', 'P0', ACC_A_S, [MENU, ADV], '—',
           ['Chỉ có 3 ô: Năm, Người duyệt, Trạng thái', 'Không có ô Công ty, Phòng ban, Bộ phận, Nhân viên'])
    S2.add('Ô lọc với cấp trên', 'P0', ACC_B, [MENU, ADV], '—',
           ['Có 6 ô: Phòng ban, Bộ phận, Nhân viên, Năm, Người duyệt, Trạng thái',
            'Không có ô Công ty (chỉ hiện với quyền xem mức Tổng công ty)'])
    S2.add('Lọc theo Năm', 'P0', [ACC_A_S, 'A có 3 phiếu 2026 và 1 phiếu 2027 (TPE_%s_2027.00720, Đang tạo).' % PFX],
           [MENU, ADV, 'Chọn Năm 2027, bấm Tìm kiếm.'], 'Năm: 2027', ['Chỉ còn phiếu năm 2027', 'Ô Năm có lựa chọn từ 2030 xuống 2023'])
    S2.add('Lọc theo Trạng thái', 'P0', [ACC_B, DATA], [MENU, ADV, 'Chọn Trạng thái Chờ TP duyệt.'], 'Trạng thái: Chờ TP duyệt',
           ['Còn %s, %s' % (P2, P4), 'Ô Trạng thái có đủ 6 lựa chọn: Đang tạo, Chờ TP duyệt, TP đã duyệt, Chờ BGĐ duyệt, BGĐ đã duyệt, Hủy'])
    S2.add('Lọc theo Người duyệt', 'P1', [ACC_A_S, HAPP], [MENU, ADV, 'Chọn Người duyệt: Trần Văn B.'], 'Người duyệt: Trần Văn B',
           ['Ra %s' % P3, 'Phiếu BGĐ đã duyệt thì lọc theo người BGĐ duyệt, không theo TP'])
    S2.add('Lọc Phòng ban rồi Bộ phận', 'P1', 'Tài khoản V3 (quyền %s mức Công ty).' % QV,
           [MENU, ADV, 'Chọn Phòng ban KD1.', 'Mở ô Bộ phận.', 'Chọn Bộ phận Nhóm KD1-2.'], 'Phòng ban: KD1; Bộ phận: Nhóm KD1-2',
           ['Ô Bộ phận chỉ còn bộ phận của KD1', 'Kết quả chỉ còn %s' % P4, 'Đổi Phòng ban sang KD2 thì ô Bộ phận tự xoá'])
    S2.add('Lọc theo Nhân viên', 'P1', [ACC_B, DATA], [MENU, ADV, 'Chọn Nhân viên: Nguyễn Văn A.'], 'Nhân viên: Nguyễn Văn A', ['Còn %s, %s' % (P2, P3)])
    S2.add('Lọc theo Công ty (mức Tổng công ty)', 'P1', 'Tài khoản V4 (quyền %s mức Tổng công ty).' % QV,
           [MENU, ADV, 'Chọn Công ty TPSG.'], 'Công ty: TPSG',
           ['Có ô Công ty, chọn TPSG chỉ còn %s' % P8, 'Ô Phòng ban chỉ còn phòng của TPSG', 'Công ty đã khoá mà còn phiếu thì vẫn có trong ô, có biểu tượng ổ khóa trước tên'])
    S2.add('Lọc kết hợp nhiều tiêu chí và từ khoá', 'P1', [ACC_B, DATA], [MENU, ADV, 'Chọn Năm 2026, Trạng thái Chờ TP duyệt.', 'Gõ "Nguyễn Văn A", bấm Tìm kiếm.'],
           'Năm 2026; Chờ TP duyệt; từ khoá Nguyễn Văn A', ['Chỉ còn %s' % P2])
    S2.add('Tổng số và phân trang sau lọc', 'P1', 'Tài khoản V4, 25 phiếu, 12 phiếu Chờ TP duyệt; đang ở trang 3.',
           [MENU, 'Sang trang 3.', ADV, 'Chọn Trạng thái Chờ TP duyệt.'], '—', ['Về trang 1, tổng 12 phiếu, 2 trang'])
    S2.add('Sắp xếp sau lọc', 'P2', 'Như trên.', [MENU, 'Lọc Chờ TP duyệt.', 'Sắp Số phiếu tăng dần.'], '—', ['12 phiếu sắp tăng dần, bộ lọc giữ nguyên'])
    S2.add('Làm mới xoá điều kiện', 'P1', [ACC_B, DATA], [MENU, ADV, 'Chọn Trạng thái Chờ TP duyệt, gõ từ khoá "A".', 'Bấm Làm mới.'], '—',
           ['Mọi ô lọc và ô tìm trống', 'Quay về 4 phiếu, trang 1'])
    S2.add('Giữ bộ lọc khi sang màn khác rồi quay lại', 'P1', [ACC_B, DATA], [MENU, 'Lọc Trạng thái Chờ TP duyệt.', 'Bấm Xem 1 phiếu rồi bấm Quay lại.'], '—',
           ['Bộ lọc Chờ TP duyệt còn nguyên, danh sách 2 phiếu'])
    S2.add('Tải lại trang (F5)', 'P2', [ACC_B, DATA], [MENU, 'Lọc Chờ TP duyệt.', 'Nhấn F5.'], '—',
           ['Bộ lọc còn trong 10 phút', 'Quá 10 phút thì về mặc định'])
    S2.add('Mở thẻ trình duyệt mới', 'P2', [ACC_B, DATA], [MENU, 'Lọc Chờ TP duyệt.', 'Mở màn ở thẻ mới.'], '—', ['Thẻ mới dùng lại bộ lọc đang ghi nhớ (trong 10 phút)'])
    S2.add('Tài khoản khác cùng trình duyệt', 'P2', 'A và B dùng chung 1 trình duyệt.', ['B lọc Chờ TP duyệt rồi đăng xuất.', 'A đăng nhập, %s' % MENU], '—',
           ['Danh sách của A vẫn chỉ trong phạm vi của A (3 phiếu nếu bỏ lọc)', 'Lưu ý: bộ lọc ghi nhớ theo trình duyệt, không theo tài khoản — A có thể thấy ô Trạng thái còn Chờ TP duyệt'])

    # ======================================================================== III. THÊM MỚI
    S3 = Sec()
    S3.add('Chặn Tạo mới khi chưa có chỉ tiêu Đã duyệt', 'P0', ACC_C, [MENU, 'Bấm Tạo mới.'], '—',
           ['Hiện hộp tiêu đề %s, nội dung %s' % (BLOCK_TITLE, BLOCK_MSG), 'Hai nút Đóng / Đã hiểu', 'Không mở form, vẫn ở danh sách'])
    S3.add('Phiếu giao chỉ tiêu chưa Đã duyệt không mở khoá Tạo mới', 'P0', ACC_C, [MENU, 'Bấm Tạo mới.'], '—',
           ['Vẫn bị chặn như trên dù năm 2026 có phiếu giao chỉ tiêu đang Chờ duyệt', 'Chỉ phiếu giao chỉ tiêu theo nhân viên ở trạng thái Đã duyệt mới tính'])
    S3.add('Mở thẳng màn Lập phiếu khi chưa có chỉ tiêu', 'P1', ACC_C, ['Mở lại màn Lập %s từ trang đã đánh dấu (bookmark) của trình duyệt.' % kh], '—',
           ['Hiện hộp chặn như trên', 'Bấm Đã hiểu thì quay về danh sách, không còn form'])
    S3.add('Giao diện form Tạo mới', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.'], '—',
           ['Tiêu đề "Lập %s"' % ten, 'Khối "Thông tin phiếu": Số phiếu (khoá, gợi ý "Số phiếu tự sinh khi lưu"), Năm (dấu * đỏ), Nhân viên (khoá, sẵn "Nguyễn Văn A - KD1 ...")',
            'Khối "Chi tiết": 3 thẻ Chi tiết theo tháng, Theo thị trường, Theo tháng',
            'Chân trang: Lưu, Lưu và gửi, Lấy dữ liệu từ %s, Quay lại' % P['OTHER'],
            'KHÔNG có ô chọn nhân viên khác / phòng ban, KHÔNG có nút Lưu nháp, Lưu và tiếp tục'])
    S3.add('Năm mặc định và danh sách năm', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.', 'Mở ô Năm.'], '—',
           ['Năm mặc định "Năm 2026" (năm sớm nhất từ năm nay có chỉ tiêu)', 'Ô Năm có Năm 2026, 2027, 2028, 2029, 2030 (năm nay tới +4)', 'Không có nút xoá trống ô Năm'])
    S3.add('Tháng theo năm hiện tại', 'P0', ACC_A + '\nHôm nay %s.' % TODAY, [MENU, 'Bấm Tạo mới.'], 'Năm 2026',
           ['Bảng có 2 tháng: I "Tháng 11 (0 khách)", II "Tháng 12 (0 khách)" (từ tháng lập tới tháng 12)', 'Mỗi tháng có sẵn 1 dòng Tỉnh/TP trống + liên kết "+ Thêm Tỉnh/TP"'])
    S3.add('Năm sau có đủ 12 tháng', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.', 'Chọn Năm 2027.'], 'Năm 2027',
           ['Bảng có đủ Tháng 1 tới Tháng 12 (I tới XII)', 'Ô Tỉnh/TP chỉ có Hà Nội (chỉ tiêu 2027)'])
    S3.add('Năm chưa có chỉ tiêu', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.', 'Chọn Năm 2028.', 'Bấm Lưu.'], 'Năm 2028',
           ['Bảng thay bằng dòng "Chưa có phiếu giao chỉ tiêu Đã duyệt cho năm 2028 — không có Tỉnh/TP để lập kế hoạch"',
            'Nút Lấy dữ liệu từ %s ẩn' % P['OTHER'], 'Bấm Lưu báo "Chưa có chỉ tiêu được giao cho năm 2028 — không lưu được", không tạo phiếu'])
    S3.add('Các cột của bảng nhập', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.'], '—',
           ['Tiêu đề cột theo thứ tự: ' + '; '.join(P['FORM_COLS']), 'KHÔNG có cột Khách hàng, Người liên hệ, Phân loại khách'])
    S3.add('Ô Tỉnh/TP chỉ có tỉnh trong chỉ tiêu', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.', 'Mở ô Tỉnh/TP dòng Tháng 11.'], '—',
           ['Chỉ có Hà Nội, Hải Phòng, Quảng Ninh', 'Không có Bắc Ninh hay tỉnh nào ngoài chỉ tiêu 2026 của A'])
    S3.add('Tỉnh đã chọn bị loại khỏi dòng khác cùng tháng', 'P0', ACC_A,
           [MENU, 'Bấm Tạo mới.', 'Tháng 11 chọn Hà Nội.', 'Bấm "+ Thêm Tỉnh/TP" ở Tháng 11, mở ô Tỉnh/TP dòng mới.'], '—',
           ['Dòng mới chỉ còn Hải Phòng, Quảng Ninh', 'Không chọn trùng được Hà Nội trong cùng tháng'])
    S3.add('Cùng tỉnh ở tháng khác được chọn', 'P1', ACC_A, [MENU, 'Bấm Tạo mới.', 'Tháng 11 chọn Hà Nội.', 'Tháng 12 chọn Hà Nội.'], '—',
           ['Tháng 12 chọn được Hà Nội', 'Lưu được, tab Theo thị trường gộp Hà Nội có 2 tháng con'])
    S3.add('Thêm dòng Tỉnh/TP', 'P1', ACC_A, [MENU, 'Bấm Tạo mới.', 'Bấm "+ Thêm Tỉnh/TP" ở Tháng 11 hai lần.'], '—',
           ['Tháng 11 có 3 dòng STT 1, 2, 3', 'Liên kết "+ Thêm Tỉnh/TP" chuyển xuống dưới dòng cuối'])
    S3.add('Xoá dòng đã có số thì hỏi', 'P1', ACC_A, [MENU, 'Bấm Tạo mới.', 'Tháng 11 chọn Hà Nội, nhập SL khách.', 'Bấm biểu tượng thùng rác (Xoá dòng).', 'Bấm Hủy, rồi bấm Xoá dòng lần nữa và chọn Xoá.'],
           'SL khách: 5', ['Hộp "Xoá dòng Tỉnh/TP", nội dung "Xoá dòng Hà Nội của Tháng 11? Số liệu của dòng sẽ mất.", nút Hủy / Xoá',
                           'Bấm Hủy: dòng còn nguyên', 'Bấm Xoá: dòng mất; nếu là dòng duy nhất của tháng thì thay bằng 1 dòng trống'])
    S3.add('Xoá dòng chưa có số không hỏi', 'P2', ACC_A, [MENU, 'Bấm Tạo mới.', 'Thêm 1 dòng ở Tháng 11, chọn Hải Phòng, không nhập số.', 'Bấm Xoá dòng.'], '—',
           ['Dòng mất ngay, không hiện hộp xác nhận'])
    S3.add('Lưu phiếu đầy đủ hợp lệ', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.', 'Nhập 2 dòng theo Test Data.', 'Bấm Lưu.'], P['HN'] + P['HP'],
           ['Báo "Đã lưu TPE_%s_2026.xxxxx", quay về danh sách' % PFX, 'Phiếu mới ở đầu danh sách, trạng thái Đang tạo, %s' % P['M_LIST'],
            'Số phiếu dạng <mã công ty>_%s_<năm>.<số thứ tự 5 chữ số>' % PFX])
    S3.add('Tổng dòng, tổng tháng và tổng phiếu tự tính', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.', 'Nhập 2 dòng theo Test Data (chưa lưu).'], P['HN'] + P['HP'],
           [P['HN_TOT'], 'Dòng tháng: "%s", "%s", số của tháng = cộng các dòng Tỉnh/TP' % (P['M11'], P['M12']),
            'Dòng TỔNG ghim đầu bảng: "Nguyễn Văn A - KD1 ... - %d khách - 2 thị trường"' % P['KHACH'], P['M_ROW_TOT']])
    S3.add('Chỉ nhập trường bắt buộc', 'P1', ACC_A, [MENU, 'Bấm Tạo mới.', 'Nhập theo Test Data.', 'Bấm Lưu.'], P['ONLY_KHACH'],
           ['Lưu được (Đang tạo)', 'Chỉ bị chặn khi Gửi duyệt (xem nhóm Gửi duyệt)'])
    if P['GIA_TRI_HD']:
        S3.add('DS tiêu chuẩn quyết toán và Doanh số xuất hàng không bắt buộc', 'P1', ACC_A, [MENU, 'Bấm Tạo mới.', 'Tháng 11 Hà Nội nhập SL khách 5, Hợp đồng hàng hóa SL HĐ 3 / DS tiêu chuẩn 1,500,000,000, để trống 2 ô DS tiêu chuẩn quyết toán, Doanh số xuất hàng.', 'Bấm Lưu.'],
               '—', ['Lưu được, 2 ô để trống thành 0 (hiện trống ở dòng Tỉnh/TP)', '2 ô này không đi cặp với ô nào'])
    else:
        S3.add('Chỉ nhập báo giá hàng hóa, bỏ trống dịch vụ', 'P1', ACC_A, [MENU, 'Bấm Tạo mới.', 'Tháng 11 Hà Nội nhập SL khách 15, Báo giá hàng hóa SL 9 / Giá trị 4,500,000,000, để trống nhóm Báo giá dịch vụ.', 'Bấm Lưu.'],
               '—', ['Lưu được', 'Tổng cộng SL 9, Giá trị 4,500,000,000'])
    S3.add('Có số mà chưa chọn Tỉnh/TP', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.', 'Dòng Tháng 11 không chọn Tỉnh/TP, nhập SL khách 5.', 'Bấm Lưu.'], 'SL khách: 5',
           ['Báo %s' % CHECK, 'Ô Tỉnh/TP dòng đó viền đỏ, chữ đỏ %s ngay dưới' % REQ, 'Không lưu, dữ liệu đã nhập còn nguyên'])
    S3.add('Đã chọn Tỉnh/TP mà thiếu SL khách', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.', 'Tháng 11 chọn Hà Nội, nhập %s, bỏ trống SL khách.' % P['V1'].split(' của')[0], 'Bấm Lưu.'],
           '%s: 3; %s: 1,500,000,000' % (P['Q1'], P['V1']), ['Ô SL khách đỏ %s' % REQ, 'Không lưu'])
    S3.add('SL khách bằng 0', 'P1', ACC_A, [MENU, 'Bấm Tạo mới.', 'Tháng 11 chọn Hà Nội, SL khách gõ 0.', 'Bấm Lưu.'], 'SL khách: 0',
           ['Ô SL khách đỏ %s (0 coi như chưa nhập)' % REQ])
    S3.add('Có SL mà thiếu giá trị (cặp hàng hóa)', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.', 'Tháng 11 Hà Nội: SL khách 5, nhập %s = 3, bỏ trống %s.' % (P['Q1'], P['V1']), 'Bấm Lưu.'],
           '%s: 3' % P['Q1'], ['Ô %s đỏ %s' % (P['V1'], REQ), 'SL và giá trị trong cùng nhóm phải đi cặp'])
    S3.add('Có giá trị mà thiếu SL (cặp dịch vụ)', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.', 'Tháng 11 Hà Nội: SL khách 5, nhập %s = 300,000,000, bỏ trống %s.' % (P['V2'], P['Q2']), 'Bấm Lưu.'],
           '%s: 300,000,000' % P['V2'], ['Ô %s đỏ %s' % (P['Q2'], REQ), 'Không lưu'])
    S3.add('Ô số chỉ nhận số nguyên không âm', 'P1', ACC_A, [MENU, 'Bấm Tạo mới.', 'Gõ lần lượt vào ô SL khách: -5, abc, 2.5'], '-5; abc; 2.5',
           ['Không nhập được dấu âm và chữ', 'Không có phần thập phân (số nguyên)'])
    S3.add('Hiển thị số có dấu phẩy ngăn nghìn', 'P1', ACC_A, [MENU, 'Bấm Tạo mới.', 'Gõ 1500000000 vào 1 ô giá trị.'], '1500000000',
           ['Ô hiện 1,500,000,000', 'Dòng tháng và dòng TỔNG cũng hiện dạng 1,500,000,000'])
    S3.add('Vượt 15 chữ số', 'P2', ACC_A, [MENU, 'Bấm Tạo mới.', 'Tháng 11 Hà Nội SL khách 5, gõ 16 chữ số vào %s + SL tương ứng.' % P['V1'], 'Bấm Lưu.'],
           '1234567890123456', ['Báo đỏ tại ô vượt giới hạn hoặc không gõ thêm được quá 15 chữ số', 'Không lưu số sai'])
    S3.add('Lỗi đỏ biến mất khi sửa đúng', 'P1', ACC_A, [MENU, 'Bấm Tạo mới.', 'Tạo lỗi thiếu SL khách, bấm Lưu.', 'Nhập SL khách 5.'], 'SL khách: 5',
           ['Chữ đỏ dưới ô SL khách mất ngay khi nhập', 'Bấm Lưu lại thì lưu được'])
    S3.add('Lỗi ở tháng đang thu gọn hoặc ở thẻ khác', 'P1', ACC_A, [MENU, 'Bấm Tạo mới.', 'Tạo lỗi thiếu SL khách ở Tháng 12.', 'Thu gọn Tháng 12, chuyển sang thẻ Theo tháng.', 'Bấm Lưu.'], '—',
           ['Tự chuyển về thẻ Chi tiết theo tháng (thẻ có dấu báo lỗi)', 'Tháng 12 tự mở ra, cuộn tới ô lỗi đầu tiên'])
    S3.add('Dòng trống và tháng trống bị bỏ khi lưu', 'P1', ACC_A, [MENU, 'Bấm Tạo mới.', 'Chỉ nhập Tháng 11 Hà Nội (hợp lệ), Tháng 12 để trống, thêm 1 dòng trống ở Tháng 11.', 'Bấm Lưu.', 'Mở Xem phiếu vừa lưu.'], '—',
           ['Lưu được, không báo lỗi cho dòng trống', 'Màn Xem chỉ có Tháng 11 với 1 dòng Hà Nội'])
    S3.add('Đổi Năm khi đã nhập số thì hỏi', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.', 'Nhập dòng Hà Nội Tháng 11.', 'Chọn Năm 2027, bấm Hủy.', 'Chọn Năm 2027 lần nữa, bấm Đổi.'], 'Năm 2027',
           ['Hộp "Đổi năm" nội dung "Đổi năm? Số liệu theo tháng đã nhập sẽ mất.", nút Hủy / Đổi',
            'Hủy: ô Năm về 2026, dữ liệu còn', 'Đổi: bảng dựng lại 12 tháng trống của 2027'])
    S3.add('Đổi Năm khi chưa nhập không hỏi', 'P2', ACC_A, [MENU, 'Bấm Tạo mới.', 'Chọn Năm 2027.'], '—', ['Đổi ngay, không hiện hộp hỏi'])
    S3.add('Một nhân viên lập nhiều phiếu cùng năm', 'P0', [ACC_A_S, 'A đã có phiếu M năm 2026.'], [MENU, 'Bấm Tạo mới, chọn Năm 2026, nhập 1 dòng hợp lệ, bấm Lưu.'], '—',
           ['Lưu được phiếu thứ 2 năm 2026 với số phiếu mới', 'Không báo trùng nhân viên / năm'])
    S3.add('Ô chọn cấp hiển thị và thu / mở tháng', 'P2', ACC_A, [MENU, 'Bấm Tạo mới.', 'Ở tiêu đề cột Tháng / Tỉnh/TP chọn "Chỉ Tháng".', 'Bấm mũi tên ở Tháng 11.', 'Chọn lại "Đến Tỉnh/TP".'], '—',
           ['"Chỉ Tháng": mọi tháng thu gọn, chỉ còn dòng tháng', 'Bấm mũi tên: Tháng 11 mở ra', '"Đến Tỉnh/TP": mở hết'])
    S3.add('Quay lại khi chưa nhập gì', 'P1', ACC_A, [MENU, 'Bấm Tạo mới.', 'Bấm Quay lại.'], '—', ['Về danh sách ngay, không hỏi'])
    S3.add('Quay lại khi đã nhập', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.', 'Nhập dòng Hà Nội.', 'Bấm Quay lại, chọn Ở lại.', 'Bấm Quay lại, chọn Thoát.'], '—',
           ['Hiện %s' % UNSAVED, 'Ở lại: dữ liệu còn nguyên', 'Thoát: về danh sách, không có phiếu mới'])
    S3.add('Rời trang bằng menu khi đã nhập', 'P1', ACC_A, [MENU, 'Bấm Tạo mới, nhập dòng Hà Nội.', 'Bấm 1 mục menu khác.'], '—', ['Hiện hộp "Thông tin chưa lưu" như trên'])
    S3.add('Nhập rồi xoá hết', 'P2', ACC_A, [MENU, 'Bấm Tạo mới.', 'Chọn Hà Nội, nhập SL khách rồi xoá số và bỏ chọn tỉnh.', 'Bấm Quay lại.'], '—',
           ['Không hiện hộp hỏi (form về như ban đầu)'])
    S3.add('Bấm Lưu liên tục', 'P1', ACC_A, [MENU, 'Bấm Tạo mới, nhập 1 dòng hợp lệ.', 'Bấm Lưu 3 lần thật nhanh.'], '—', ['Chỉ tạo 1 phiếu'])
    S3.add('Hai thẻ cùng lập phiếu', 'P2', ACC_A, ['Mở 2 thẻ, mỗi thẻ %s' % MENU, 'Cả 2 thẻ bấm Tạo mới, nhập dữ liệu giống nhau, bấm Lưu.'], '—',
           ['Tạo 2 phiếu khác số phiếu (được phép nhiều phiếu / năm)'])

    # ======================================================================== IV. CHỈNH SỬA
    S4 = Sec()
    S4.add('Mở Sửa từ danh sách, dữ liệu điền đúng', 'P0', [ACC_A_S, PLAN_M], [MENU, 'Bấm biểu tượng Sửa (bút chì) ở dòng %s.' % M], '—',
           ['Tiêu đề "Sửa %s: %s"' % (ten, M), 'Năm 2026, Nhân viên của A, Số phiếu %s (khoá)' % M,
            'Tháng 11 dòng Hà Nội, Tháng 12 dòng Hải Phòng đúng số đã lưu; ô bằng 0 để trống', 'Chân trang: Lưu, Lưu và gửi, Lấy dữ liệu từ %s, Quay lại' % P['OTHER']])
    S4.add('Mở Sửa từ màn Xem', 'P1', [ACC_A_S, PLAN_M], [MENU, 'Bấm số phiếu %s.' % M, 'Bấm Sửa.'], '—', ['Mở màn Sửa của %s' % M])
    S4.add('Trường không sửa được', 'P1', [ACC_A_S, PLAN_M], [MENU, 'Mở Sửa %s.' % M], '—', ['Số phiếu và Nhân viên bị khoá', 'Năm và bảng số sửa được'])
    S4.add('Sửa số một dòng', 'P0', [ACC_A_S, PLAN_M], [MENU, 'Mở Sửa %s.' % M, 'Đổi SL khách dòng Hà Nội từ %s thành %s.' % ((5, 8) if P['GIA_TRI_HD'] else (15, 18)), 'Bấm Lưu.'], '—',
           ['Báo "Đã lưu %s", về danh sách' % M, 'Cột SL khách của %s tăng thêm 3' % M, 'Trạng thái vẫn Đang tạo'])
    S4.add('Thêm tỉnh mới và xoá tỉnh cũ', 'P1', [ACC_A_S, PLAN_M], [MENU, 'Mở Sửa %s.' % M, 'Tháng 12 xoá dòng Hải Phòng (xác nhận Xoá), thêm Quảng Ninh SL khách 1.' % (), 'Bấm Lưu, mở Xem.'], '—',
           ['Tháng 12 chỉ còn Quảng Ninh', 'Tổng phiếu tính lại theo dòng còn lại'])
    S4.add('Tháng khi sửa tính theo ngày lập phiếu', 'P1', [ACC_A_S, 'Phiếu %s của A năm 2026 lập 05/10/2026, Đang tạo, có số ở Tháng 10.' % C(9)],
           [MENU, 'Mở Sửa %s (hôm nay %s).' % (C(9), TODAY)], '—', ['Bảng có Tháng 10, 11, 12 (tính từ tháng lập phiếu, không phải tháng hiện tại)'])
    S4.add('Đổi Năm khi sửa thì số phiếu đổi theo năm', 'P1', [ACC_A_S, PLAN_M], [MENU, 'Mở Sửa %s.' % M, 'Chọn Năm 2027, bấm Đổi, nhập Tháng 1 Hà Nội hợp lệ.', 'Bấm Lưu.'], 'Năm 2027',
           ['Lưu được', 'Số phiếu đổi thành TPE_%s_2027.%05d (giữ số thứ tự, đổi năm)' % (PFX, P['base'] + 1)])
    S4.add('Bỏ trống bắt buộc khi sửa', 'P0', [ACC_A_S, PLAN_M], [MENU, 'Mở Sửa %s.' % M, 'Xoá SL khách dòng Hà Nội.', 'Bấm Lưu.'], '—',
           ['Ô SL khách đỏ %s, báo %s' % (REQ, CHECK), 'Không lưu, phiếu giữ số cũ'])
    S4.add('Sửa cặp SL / giá trị sai khi sửa', 'P1', [ACC_A_S, PLAN_M], [MENU, 'Mở Sửa %s.' % M, 'Xoá %s dòng Hà Nội (giữ SL).' % P['V1'], 'Bấm Lưu.'], '—',
           ['Ô %s đỏ %s' % (P['V1'], REQ)])
    S4.add('Quay lại khi đã đổi', 'P1', [ACC_A_S, PLAN_M], [MENU, 'Mở Sửa %s, đổi 1 số.' % M, 'Bấm Quay lại, chọn Ở lại.', 'Bấm Quay lại, chọn Thoát.'], '—',
           ['Hiện %s' % UNSAVED, 'Thoát: phiếu không đổi'])
    S4.add('Mở Sửa không đổi gì rồi quay lại', 'P2', [ACC_A_S, PLAN_M], [MENU, 'Mở Sửa %s.' % M, 'Bấm Quay lại.'], '—', ['Về ngay, không hỏi'])
    S4.add('Đổi rồi trả về giá trị ban đầu', 'P2', [ACC_A_S, PLAN_M], [MENU, 'Mở Sửa %s, đổi SL khách rồi gõ lại số cũ.' % M, 'Bấm Quay lại.'], '—', ['Không hiện hộp hỏi'])
    S4.add('Mở Sửa phiếu không còn Đang tạo', 'P0', [ACC_A_S, PEND], ['Mở lại màn Sửa của %s từ trang đã đánh dấu trong trình duyệt.' % P2], '—',
           ['Tự chuyển sang màn Xem của %s, không có ô nhập' % P2])
    S4.add('Phiếu vừa được gửi duyệt ở thẻ khác', 'P0', [ACC_A_S, PLAN_M], ['Thẻ 1: mở Sửa %s.' % M, 'Thẻ 2: Gửi duyệt %s.' % M, 'Thẻ 1: đổi số, bấm Lưu.'], '—',
           ['Thẻ 1 báo %s' % LOCKED, 'Phiếu giữ nguyên số liệu lúc gửi'])
    S4.add('Phiếu bị Hủy ở thẻ khác', 'P1', [ACC_A_S, PLAN_M], ['Thẻ 1: mở Sửa %s.' % M, 'Thẻ 2: Hủy phiếu %s.' % M, 'Thẻ 1: bấm Lưu.'], '—', ['Thẻ 1 báo %s' % LOCKED])
    S4.add('Hai thẻ cùng sửa', 'P2', [ACC_A_S, PLAN_M], ['Thẻ 1 và 2 cùng mở Sửa %s.' % M, 'Thẻ 1 đổi SL khách Hà Nội, Lưu.', 'Thẻ 2 đổi SL khách Hải Phòng, Lưu.'], '—',
           ['Lưu sau ghi đè lưu trước: Hà Nội về số cũ, Hải Phòng theo thẻ 2 (đã chấp nhận)'])
    S4.add('Tỉnh cũ ngoài chỉ tiêu vẫn hiện khi sửa', 'P1', [ACC_A_S, PLAN_M, 'Sau khi lập M, phiếu giao chỉ tiêu được sửa bỏ Hải Phòng rồi duyệt lại.'],
           [MENU, 'Mở Sửa %s.' % M, 'Mở ô Tỉnh/TP dòng Hải Phòng Tháng 12; mở ô Tỉnh/TP của 1 dòng mới.'], '—',
           ['Dòng Hải Phòng cũ vẫn hiện và lưu lại được', 'Dòng mới không có Hải Phòng'])
    S4.add('Năm của phiếu không còn chỉ tiêu', 'P1', [ACC_A_S, PLAN_M, 'Phiếu giao chỉ tiêu 2026 của A bị Hủy duyệt sau khi lập M.'], [MENU, 'Mở Sửa %s.' % M, 'Bấm Lưu.'], '—',
           ['Bảng hiện "Chưa có phiếu giao chỉ tiêu Đã duyệt cho năm 2026 — không có Tỉnh/TP để lập kế hoạch"',
            'Lưu báo "Chưa có chỉ tiêu được giao cho năm 2026 — không lưu được"', 'Phiếu M giữ nguyên số cũ (xem được ở màn Xem)'])
    S4.add('Phiếu bị từ chối về Đang tạo sửa được', 'P0', [ACC_A_S, 'Phiếu %s bị B từ chối, lý do "Thiếu Hải Phòng".' % P2], [MENU, 'Mở Xem %s.' % P2, 'Bấm Sửa, nhập thêm dòng, Lưu.' % ()], '—',
           ['Màn Xem có dòng "Lý do từ chối: Thiếu Hải Phòng"', 'Có nút Sửa, Gửi duyệt, Hủy phiếu', 'Sửa và lưu được'])

    # ======================================================================== V. GỬI DUYỆT
    S5 = Sec()
    S5.add('Điều kiện hiện nút Gửi duyệt', 'P0', [ACC_A_S, DATA], [MENU, 'Mở ba chấm dòng %s, %s.' % (M, P2), 'Mở Xem %s.' % M], '—',
           ['Chỉ phiếu Đang tạo do chính mình lập có Gửi duyệt (ở dòng và ở chân màn Xem)', '%s (Chờ TP duyệt) không có' % P2])
    S5.add('Hộp xác nhận gửi duyệt', 'P1', [ACC_A_S, PLAN_M], [MENU, 'Ở dòng %s bấm ba chấm > Gửi duyệt.' % M], '—',
           ['Hộp "Gửi duyệt", nội dung "Gửi duyệt phiếu %s?", nút Hủy / Gửi duyệt' % M])
    S5.add('Gửi duyệt thành công', 'P0', [ACC_A_S, PLAN_M, ACC_B], [MENU, 'Ở dòng %s bấm Gửi duyệt > Gửi duyệt.' % M], '—',
           ['Báo "Đã gửi duyệt %s"' % M, 'Trạng thái Chờ TP duyệt (màu cam)', 'Hết nút Sửa, Gửi duyệt; còn Hủy phiếu', 'B thấy %s ở lối vào "%s"' % (M, P['CD'])])
    S5.add('Bấm Hủy ở hộp xác nhận', 'P1', [ACC_A_S, PLAN_M], [MENU, 'Bấm Gửi duyệt ở dòng %s, chọn Hủy.' % M], '—', ['Phiếu vẫn Đang tạo, không có thông báo nào'])
    S5.add('Lưu và gửi từ form Tạo mới', 'P0', ACC_A, [MENU, 'Bấm Tạo mới, nhập theo Test Data.', 'Bấm Lưu và gửi.'], P['HN'] + P['HP'],
           ['Báo "Đã gửi duyệt TPE_%s_2026.xxxxx", về danh sách' % PFX, 'Phiếu mới ở trạng thái Chờ TP duyệt'])
    S5.add('Lưu và gửi từ form Sửa', 'P0', [ACC_A_S, PLAN_M], [MENU, 'Mở Sửa %s, đổi 1 số.' % M, 'Bấm Lưu và gửi.'], '—', ['Lưu số mới và chuyển Chờ TP duyệt cùng lúc'])
    S5.add('Lưu và gửi khi thiếu bắt buộc', 'P0', ACC_A, [MENU, 'Bấm Tạo mới, Tháng 11 chọn Hà Nội, bỏ trống SL khách.', 'Bấm Lưu và gửi.'], '—',
           ['Ô SL khách đỏ %s, báo %s' % (REQ, CHECK), 'Không tạo phiếu, không gửi'])
    S5.add('Không gửi được khi tổng %s bằng 0' % P['SEND_COL'], 'P0', ACC_A,
           [MENU, 'Bấm Tạo mới, nhập theo Test Data.', 'Bấm Lưu và gửi.', 'Bấm Lưu; ở danh sách bấm Gửi duyệt phiếu vừa lưu.'], P['ONLY_KHACH'],
           ['Lưu và gửi: báo "%s", không lưu' % P['NO_SEND'], 'Lưu thường được (Đang tạo)', 'Gửi duyệt ở danh sách: báo "%s", phiếu vẫn Đang tạo' % P['NO_SEND']])
    S5.add('Phiếu trưởng phòng lập gửi thẳng Chờ BGĐ duyệt', 'P0', ACC_B,
           [MENU, 'Đăng nhập B, bấm Tạo mới, Tháng 11 chọn Đà Nẵng, nhập số hợp lệ.', 'Bấm Lưu và gửi.'], '—',
           ['Phiếu chuyển thẳng Chờ BGĐ duyệt (bỏ qua Chờ TP duyệt)', 'Phiếu không hiện ở lối vào "%s" của B hay G (TP không tự duyệt phiếu mình)' % P['CD']])
    S5.add('Thông báo tới trưởng phòng khi gửi', 'P0', [ACC_A_S, PLAN_M, ACC_B, ACC_G], ['A gửi duyệt %s.' % M, 'B mở chuông thông báo, bấm vào thông báo mới.'], '—',
           ['B (và G — cùng phòng, có quyền duyệt) nhận thông báo "[%s] Gửi duyệt: %s"' % (PFX, M), 'A không nhận', 'Bấm thông báo mở màn Xem %s' % M])
    S5.add('Trưởng phòng gửi phiếu của mình không báo ai', 'P2', ACC_B, ['B Lưu và gửi phiếu của B.'], '—',
           ['Không có thông báo gửi duyệt cho ai (BGĐ chưa có màn duyệt, sẽ bổ sung đợt sau)'])
    S5.add('Gửi phiếu đã gửi ở thẻ khác', 'P1', [ACC_A_S, PLAN_M], ['Thẻ 1 mở Xem %s.' % M, 'Thẻ 2 gửi duyệt %s.' % M, 'Thẻ 1 bấm Gửi duyệt > Gửi duyệt.'], '—',
           ['Thẻ 1 báo %s' % NOPERM, 'Trạng thái giữ Chờ TP duyệt, không gửi 2 lần thông báo'])
    S5.add('Gửi lại sau khi bị từ chối', 'P1', [ACC_A_S, 'Phiếu %s bị từ chối về Đang tạo.' % P2], [MENU, 'Gửi duyệt %s.' % P2], '—',
           ['Về Chờ TP duyệt', 'Dòng "Lý do từ chối" không còn hiện'])

    # ======================================================================== VI. DUYỆT PHIẾU
    S6 = Sec()
    S6.add('Điều kiện hiện nút Duyệt', 'P0', [ACC_B, DATA], OPEN_P2_B, '—',
           ['Màn Xem %s có nút Duyệt, Từ chối' % P2, 'Ở danh sách, mục Duyệt trong ba chấm chỉ mở màn Xem (duyệt tại màn Xem)'])
    S6.add('Hộp xác nhận duyệt', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm Duyệt.'], '—',
           ['Hộp "Duyệt phiếu", nội dung "Duyệt phiếu %s của Nguyễn Văn A - KD1?", nút Hủy / Duyệt' % P2])
    S6.add('Duyệt thành công', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Bấm Duyệt > Duyệt.'], '—',
           ['Báo "Đã duyệt %s", về danh sách chờ duyệt' % P2, 'Trạng thái TP đã duyệt (xanh dương)',
            'Cột Người duyệt "Trần Văn B - KD1", Ngày duyệt là hôm nay', 'Phiếu vẫn ở lối vào chờ duyệt (chờ Gửi BGĐ)'])
    S6.add('Bấm Hủy ở hộp duyệt', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm Duyệt, chọn Hủy.'], '—', ['Phiếu vẫn Chờ TP duyệt, không có thông báo'])
    S6.add('Trưởng phòng không duyệt phiếu mình lập', 'P0', [ACC_B, 'Phiếu %s của B Chờ BGĐ duyệt.' % P6], [MENU, 'Mở Xem %s.' % P6], '—',
           ['Không có nút Duyệt, Từ chối, Gửi BGĐ'])
    S6.add('Người cùng phòng có quyền duyệt cũng duyệt được', 'P1', [ACC_G, PEND], [MENU_CD, 'Mở Xem %s, bấm Duyệt > Duyệt.' % P2], '—',
           ['G thấy mục "%s" và duyệt được %s (luật giữ như hệ thống cũ: có quyền duyệt và cùng phòng)' % (P['CD'], P2)])
    S6.add('Phiếu hiện ở lối vào chờ duyệt thì mở xem được', 'P1', [ACC_G, HAPP], [MENU_CD, 'Bấm số phiếu %s, bấm Gửi BGĐ.' % P3], '—',
           ['Mở được màn Xem %s, có nút Gửi BGĐ và gửi được' % P3, 'Lưu ý: nếu bị đẩy về danh sách / báo không có quyền thì ghi nhận lỗi'])
    S6.add('Có quyền duyệt nhưng khác phòng', 'P0', [ACC_H, PEND], [MENU_CD], '—',
           ['Lối vào chờ duyệt của H không có %s (phòng KD1)' % P2, 'Chỉ có %s của phòng KD2' % P7])
    S6.add('Quản lý phòng nhưng không có quyền duyệt', 'P0', ['Tài khoản B2: trưởng phòng KD1, KHÔNG có quyền %s.' % QA, PEND], [MENU, 'Mở Xem %s.' % P2], '—',
           ['Xem được %s nhưng không có nút Duyệt, Từ chối' % P2, 'Không có mục "%s" ở menu' % P['CD']])
    S6.add('Không duyệt lại phiếu đã xử lý', 'P0', [ACC_B, ACC_G, PEND], ['B mở Xem %s.' % P2, 'G duyệt %s.' % P2, 'B bấm Duyệt > Duyệt.'], '—',
           ['B báo %s' % NOPERM, 'Phiếu giữ TP đã duyệt do G duyệt, Người duyệt không bị ghi đè'])
    S6.add('Thông báo người lập khi được duyệt', 'P0', [ACC_A_S, PEND], ['B duyệt %s.' % P2, 'A mở chuông thông báo, bấm vào thông báo.'], '—',
           ['A nhận "[%s] Đã duyệt: %s"' % (PFX, P2), 'Bấm thông báo mở màn Xem %s, trạng thái TP đã duyệt' % P2])
    S6.add('Điều kiện hiện nút Gửi BGĐ', 'P0', [ACC_B, HAPP], [MENU_CD, 'Mở Xem %s.' % P3], '—',
           ['Có nút Gửi BGĐ (chỉ phiếu TP đã duyệt, với trưởng phòng của phiếu)', 'A (người lập) xem %s không có nút này' % P3])
    S6.add('Gửi BGĐ thành công', 'P0', [ACC_B, HAPP], [MENU_CD, 'Mở Xem %s, bấm Gửi BGĐ.' % P3, 'Bấm Gửi BGĐ ở hộp xác nhận.'], '—',
           ['Hộp "Gửi BGĐ duyệt", nội dung "Gửi phiếu %s lên Ban giám đốc duyệt?", nút Hủy / Gửi BGĐ' % P3,
            'Báo "Đã gửi BGĐ %s"' % P3, 'Trạng thái Chờ BGĐ duyệt, phiếu rời lối vào chờ duyệt của B'])
    S6.add('Gửi BGĐ ngay từ dòng danh sách', 'P1', [ACC_B, HAPP], [MENU_CD, 'Ở dòng %s bấm ba chấm > Gửi BGĐ > Gửi BGĐ.' % P3], '—',
           ['Gửi được, danh sách tải lại còn 2 phiếu'])
    S6.add('Thông báo khi gửi BGĐ', 'P1', [ACC_A_S, HAPP], ['B gửi BGĐ %s.' % P3], '—',
           ['A nhận "[%s] Gửi BGĐ: %s"' % (PFX, P3), 'Ban giám đốc CHƯA nhận thông báo (màn BGĐ duyệt làm đợt sau)'])
    S6.add('Phiếu Chờ BGĐ duyệt không còn thao tác duyệt', 'P1', [ACC_B, 'Phiếu %s Chờ BGĐ duyệt.' % P3], [MENU, 'Mở Xem %s.' % P3], '—',
           ['Chỉ còn Xuất Excel, In, Quay lại', 'Không có Duyệt, Từ chối, Gửi BGĐ, Hủy phiếu (BGĐ duyệt làm đợt sau)'])

    # ======================================================================== VII. KHÔNG DUYỆT (TỪ CHỐI)
    S7 = Sec()
    S7.add('Điều kiện hiện nút Từ chối', 'P0', [ACC_B, DATA], OPEN_P2_B + ['Mở Xem %s.' % P3], '—',
           ['%s (Chờ TP duyệt) có nút Từ chối (đỏ)' % P2, '%s (TP đã duyệt) không có Từ chối' % P3, 'Dòng danh sách không có Từ chối — chỉ từ chối ở màn Xem'])
    S7.add('Giao diện hộp Từ chối', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối.'], '—',
           ['Hộp "Từ chối phiếu", nội dung "Từ chối phiếu %s? Phiếu trở về Đang tạo để người lập sửa."' % P2,
            'Ô "Lý do" bắt buộc, gợi ý "Nhập lý do từ chối"', 'Nút Hủy / Từ chối'])
    S7.add('Bỏ trống lý do', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối, để trống Lý do, bấm Từ chối.'], '—',
           ['Báo đỏ %s dưới ô Lý do, hộp không đóng' % REQ, 'Phiếu vẫn Chờ TP duyệt'])
    S7.add('Lý do chỉ có khoảng trắng', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối, gõ 3 dấu cách, bấm Từ chối.'], '3 dấu cách', ['Bị chặn như bỏ trống'])
    S7.add('Giới hạn 255 ký tự', 'P2', [ACC_B, PEND], OPEN_P2_B + ['Gõ 256 ký tự, bấm Từ chối.', 'Sửa còn 255 ký tự, bấm Từ chối.'], '256 rồi 255 ký tự',
           ['256 ký tự: báo "Vui lòng nhập tối đa 255 ký tự."', '255 ký tự: từ chối được, lý do lưu đủ'])
    S7.add('Từ chối thành công', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối, nhập lý do, bấm Từ chối.'], 'Lý do: Thiếu Hải Phòng',
           ['Báo "Đã từ chối %s", về danh sách chờ duyệt' % P2, 'Phiếu về Đang tạo, rời lối vào chờ duyệt và rời danh sách của B (Đang tạo chỉ người lập thấy)'])
    S7.add('Người lập thấy lý do và sửa gửi lại', 'P0', [ACC_A_S, 'B vừa từ chối %s, lý do "Thiếu Hải Phòng".' % P2], [MENU, 'Mở Xem %s.' % P2], '—',
           ['Có dòng "Lý do từ chối: Thiếu Hải Phòng"', 'Có Sửa, Gửi duyệt, Hủy phiếu', 'Người duyệt / Ngày duyệt trên danh sách để trống'])
    S7.add('Thông báo người lập khi bị từ chối', 'P0', [ACC_A_S, PEND], ['B từ chối %s, lý do "Thiếu Hải Phòng".' % P2, 'A mở chuông thông báo.'], '—',
           ['A nhận "[%s] Từ chối: %s. Lý do: Thiếu Hải Phòng"' % (PFX, P2), 'Bấm mở màn Xem %s' % P2])
    S7.add('Bấm Hủy ở hộp Từ chối', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm Từ chối, gõ lý do, bấm Hủy.'], '—', ['Phiếu vẫn Chờ TP duyệt, không thông báo'])
    S7.add('Không từ chối phiếu đã chuyển trạng thái', 'P1', [ACC_B, ACC_G, PEND], ['B mở Xem %s.' % P2, 'G duyệt %s.' % P2, 'B bấm Từ chối, nhập lý do, xác nhận.'], '—',
           ['B báo %s' % NOPERM, 'Phiếu giữ TP đã duyệt'])
    S7.add('Không từ chối phiếu đã bị người lập hủy', 'P2', [ACC_B, PEND], ['B mở Xem %s.' % P2, 'A hủy %s.' % P2, 'B bấm Từ chối, xác nhận.'], '—',
           ['B báo %s, phiếu giữ Hủy' % NOPERM])

    # ======================================================================== VIII. HỦY PHIẾU
    S8 = Sec()
    S8.add('Điều kiện hiện nút Hủy phiếu', 'P0', [ACC_A_S, DATA], [MENU, 'Mở ba chấm của %s, %s, %s.' % (M, P2, P3)], '—',
           ['%s (Đang tạo), %s (Chờ TP duyệt): có Hủy phiếu' % (M, P2), '%s (TP đã duyệt): không có' % P3])
    S8.add('Không hủy phiếu Chờ BGĐ duyệt / đã Hủy', 'P0', [ACC_B, 'Phiếu %s của B Chờ BGĐ duyệt; phiếu %s của B đã Hủy.' % (P6, C(10))], [MENU, 'Mở ba chấm 2 dòng.'], '—',
           ['Không có Hủy phiếu ở cả 2'])
    S8.add('Hộp xác nhận hủy', 'P1', [ACC_A_S, PLAN_M], [MENU, 'Bấm Hủy phiếu ở dòng %s.' % M], '—',
           ['Hộp "Hủy phiếu", nội dung "Hủy phiếu %s? Phiếu Hủy không sửa được.", nút Đóng / Hủy phiếu (đỏ)' % M])
    S8.add('Hủy phiếu Đang tạo', 'P0', [ACC_A_S, PLAN_M], [MENU, 'Bấm Hủy phiếu ở dòng %s > Hủy phiếu.' % M], '—',
           ['Báo "Đã hủy %s"' % M, 'Trạng thái Hủy (đỏ), hết Sửa / Gửi duyệt'])
    S8.add('Hủy phiếu đang Chờ TP duyệt', 'P0', [ACC_A_S, PEND, ACC_B], [MENU, 'Hủy phiếu %s.' % P2, 'B mở lối vào "%s".' % P['CD']], '—',
           ['%s chuyển Hủy' % P2, 'Rời lối vào chờ duyệt của B'])
    S8.add('Bấm Đóng ở hộp xác nhận', 'P1', [ACC_A_S, PLAN_M], [MENU, 'Bấm Hủy phiếu ở dòng %s, chọn Đóng.' % M], '—', ['Phiếu vẫn Đang tạo'])
    S8.add('Phiếu Hủy chỉ còn Xem và Lịch sử', 'P0', [ACC_A_S, 'Phiếu %s đã Hủy.' % M], [MENU, 'Mở ba chấm dòng %s; mở Xem.' % M], '—',
           ['Dòng: chỉ Xem, Lịch sử (không In, không Xuất Excel)', 'Màn Xem: chỉ nút Quay lại'])
    S8.add('Trưởng phòng không hủy phiếu nhân viên', 'P1', [ACC_B, PEND], OPEN_P2_B, '—', ['Không có nút Hủy phiếu (chỉ người lập hủy)'])
    S8.add('Hủy khi phiếu vừa được duyệt', 'P1', [ACC_A_S, PEND], ['A mở Xem %s.' % P2, 'B duyệt %s.' % P2, 'A bấm Hủy phiếu > Hủy phiếu.'], '—',
           ['A báo %s' % NOPERM, 'Phiếu giữ TP đã duyệt'])
    S8.add('Hủy không gửi thông báo', 'P2', [ACC_A_S, PEND, ACC_B], ['A hủy %s.' % P2, 'B mở chuông thông báo.'], '—',
           ['B không nhận thông báo hủy (theo code hiện tại; nếu nghiệp vụ cần báo TP thì ghi nhận)'])

    # ======================================================================== IX. LỊCH SỬ
    S9 = Sec()
    S9.add('Mở lịch sử từ danh sách', 'P1', [ACC_A_S, PLAN_M], [MENU, 'Ở dòng %s bấm ba chấm > Lịch sử.' % M], '—',
           ['Mở popup lịch sử thay đổi của phiếu %s' % M, 'Mỗi dòng có người thực hiện, thời gian, loại thao tác, nội dung đổi'])
    S9.add('Ghi nhận Tạo mới', 'P1', [ACC_A_S, 'A vừa lưu phiếu M.'], [MENU, 'Mở Lịch sử %s.' % M], '—',
           ['Có dòng "Tạo mới" của Nguyễn Văn A, kèm Số phiếu %s, Năm 2026' % M])
    S9.add('Ghi nhận sửa', 'P1', [ACC_A_S, PLAN_M], [MENU, 'Sửa SL khách %s, Lưu.' % M, 'Mở Lịch sử.'], '—', ['Có thêm dòng "Thay đổi thông tin" ở trên cùng'])
    S9.add('Ghi nhận cả luồng trạng thái', 'P0', [ACC_A_S, 'Phiếu %s đã: tạo, gửi duyệt, B từ chối (lý do "Thiếu Hải Phòng"), A gửi lại, B duyệt, B gửi BGĐ.' % P2],
           [MENU, 'Mở Lịch sử %s.' % P2], '—',
           ['Thứ tự mới trước: Thay đổi trạng thái (TP đã duyệt sang Chờ BGĐ duyệt) · Duyệt (Chờ TP duyệt sang TP đã duyệt) · Gửi duyệt (Đang tạo sang Chờ TP duyệt) · '
            'Từ chối (Chờ TP duyệt sang Đang tạo, ghi chú "Lý do: Thiếu Hải Phòng") · Gửi duyệt · Tạo mới',
            'Mỗi dòng ghi đúng người thực hiện (A hoặc B) và thời gian'])
    S9.add('Ghi nhận Hủy phiếu', 'P1', [ACC_A_S, 'Phiếu %s vừa bị A hủy khi Chờ TP duyệt.' % P2], [MENU, 'Mở Lịch sử.'], '—',
           ['Dòng "Thay đổi trạng thái": Trạng thái Chờ TP duyệt sang Hủy'])
    S9.add('Phiếu trưởng phòng lập gửi thẳng BGĐ', 'P2', [ACC_B, 'B vừa Lưu và gửi phiếu của B.'], [MENU, 'Mở Lịch sử phiếu đó.'], '—',
           ['Dòng "Gửi duyệt": Đang tạo sang Chờ BGĐ duyệt'])
    S9.add('Lưu mà không đổi gì', 'P2', [ACC_A_S, PLAN_M], [MENU, 'Mở Sửa %s, không đổi gì, bấm Lưu.' % M, 'Mở Lịch sử.'], '—',
           ['Theo chuẩn: không phát sinh dòng lịch sử mới', 'Lưu ý: bản hiện tại vẫn ghi 1 dòng "Thay đổi thông tin" (Số phiếu, Năm) mỗi lần Lưu — ghi nhận nếu còn'])
    S9.add('Lịch sử ở màn Xem', 'P2', [ACC_A_S, PLAN_M], [MENU, 'Mở Xem %s, cuộn xuống cuối.' % M], '—', ['Có khối thông tin hệ thống / lịch sử của phiếu, khớp popup ở danh sách'])
    S9.add('Đóng popup lịch sử', 'P2', [ACC_A_S, PLAN_M], [MENU, 'Lọc Năm 2026, sang trang 1.', 'Mở Lịch sử 1 phiếu, bấm X.'], '—', ['Popup đóng, danh sách giữ bộ lọc và trang'])

    # ======================================================================== X. XEM CHI TIẾT
    S10 = Sec()
    S10.add('Mở màn Xem phiếu', 'P0', [ACC_A_S, PLAN_M], [MENU, 'Bấm số phiếu %s.' % M], '—',
            ['Tiêu đề "Chi tiết %s: %s" kèm nhãn trạng thái Đang tạo' % (ten, M), 'Khối Thông tin phiếu: Số phiếu, Năm (không còn dấu *), Nhân viên — đều khoá',
             'Dòng người lập + thời gian lập ở góc khối'])
    S10.add('Thẻ Chi tiết theo tháng ở màn Xem', 'P1', [ACC_A_S, PLAN_M], [MENU, 'Mở Xem %s.' % M], '—',
            ['Chỉ có tháng có dữ liệu: I "%s" (dòng 1 Hà Nội), II "%s" (dòng 1 Hải Phòng)' % (P['M11'], P['M12']),
             'Không có ô nhập, ô chọn Tỉnh/TP, nút xoá, liên kết Thêm Tỉnh/TP', 'Dòng TỔNG "Nguyễn Văn A - %d khách - 2 thị trường"' % P['KHACH']])
    S10.add('Thẻ Theo thị trường so với chỉ tiêu', 'P0', [ACC_A, PLAN_M], [MENU, 'Mở Xem %s, bấm thẻ Theo thị trường.' % M], '—',
            ['Cột cây "Tỉnh/TP / Tháng", chỉ xem'] + P['TARGET_TAB'])
    S10.add('So chỉ tiêu chỉ hiển thị, không chặn', 'P0', [ACC_A_S, P['UNDER']], [MENU, 'Mở Sửa %s, bấm Lưu và gửi.' % M], '—',
            ['Lưu và gửi được dù số kế hoạch lệch chỉ tiêu', 'Không có cảnh báo chặn "chưa đạt chỉ tiêu"'])
    S10.add('Thẻ Theo tháng', 'P1', [ACC_A_S, PLAN_M, 'Tháng 11 có thêm dòng Quảng Ninh nhập trước dòng Hà Nội.'], [MENU, 'Mở Xem %s, bấm thẻ Theo tháng.' % M], '—',
            ['Cây "Tháng / Tỉnh/TP": 1 Tháng 11 > 1.1 Hà Nội, 1.2 Quảng Ninh (xếp theo thứ tự tỉnh, không theo thứ tự nhập); 2 Tháng 12 > 2.1 Hải Phòng',
             'Số dòng tháng = cộng các tỉnh'])
    S10.add('Dòng TỔNG ghim khi cuộn', 'P2', [ACC_A_S, 'Phiếu 2027 có 12 tháng x 1 tỉnh.'], [MENU, 'Mở Xem phiếu, cuộn bảng xuống và sang ngang.'], '—',
            ['Hàng tiêu đề + dòng TỔNG (và dòng Chỉ tiêu giao ở thẻ Theo thị trường) đứng yên', 'Cột STT và cột cây đứng yên khi cuộn ngang'])
    S10.add('Số liệu màn Xem khớp danh sách', 'P1', [ACC_A_S, PLAN_M], [MENU, 'So dòng %s với dòng TỔNG ở màn Xem.' % M], '—', ['Khớp %s' % P['M_LIST']])
    S10.add('Nút chân trang theo trạng thái và vai trò', 'P0', [ACC_A_S, ACC_B, DATA], ['A mở Xem %s, %s.' % (M, P2), 'B mở Xem %s, %s.' % (P2, P3)], '—',
            ['A - %s: Sửa, Gửi duyệt, Hủy phiếu, Xuất Excel, In, Quay lại' % M, 'A - %s: Hủy phiếu, Xuất Excel, In, Quay lại' % P2,
             'B - %s: Duyệt, Từ chối, Xuất Excel, In, Quay lại' % P2, 'B - %s: Gửi BGĐ, Xuất Excel, In, Quay lại' % P3])
    S10.add('Phiếu lập trên hệ thống cũ chỉ xem', 'P0', [ACC_A_S, 'Phiếu cũ %s (BGĐ đã duyệt, có dòng khách hàng).' % P['LEGACY']], [MENU, 'Mở Xem %s.' % P['LEGACY']], '—',
            ['Dưới Thông tin phiếu có dòng ghi chú: phiếu lập trên hệ thống cũ (có chi tiết khách hàng) — chỉ xem; SL khách = số khách hàng của từng dòng Tỉnh/TP',
             'Bảng hiện theo dòng Tỉnh/TP, không có dòng khách hàng; SL khách mỗi dòng = số khách khác nhau' + ('; Doanh số xuất hàng = 0' if P['GIA_TRI_HD'] else ''),
             'Chân trang chỉ còn Xuất Excel, In, Quay lại'])
    S10.add('Phiếu cũ Đang tạo cũng không sửa được', 'P1', [ACC_A_S, 'Phiếu cũ do A lập trên hệ thống cũ, trạng thái Đang tạo.'], [MENU, 'Mở ba chấm dòng phiếu; mở Xem.'], '—',
            ['Không có Sửa, Gửi duyệt, Hủy phiếu ở dòng lẫn màn Xem'])
    S10.add('Phiếu cũ lập cho "Nhân viên mới"', 'P1', [ACC_B, 'Phiếu cũ %s do B lập trên hệ thống cũ cho "Nhân viên mới 2" (không gắn tài khoản), TP đã duyệt.' % P['LEGACY_NEW']],
            [MENU, 'Tìm "%s", mở Xem.' % P['LEGACY_NEW']], '—', ['Cột Nhân viên và ô Nhân viên hiện "Nhân viên mới 2"', 'Chỉ xem, không có Gửi BGĐ'])
    S10.add('Quay lại giữ trang và bộ lọc', 'P1', 'Tài khoản V4, 25 phiếu.', [MENU, 'Lọc Chờ TP duyệt, sang trang 2.', 'Mở Xem 1 phiếu, bấm Quay lại.'], '—',
            ['Về trang 2, bộ lọc còn'])
    S10.add('Quay lại từ lối vào chờ duyệt về đúng lối vào', 'P1', [ACC_B, PEND], OPEN_P2_B + ['Bấm Quay lại.'], '—',
            ['Về danh sách chờ duyệt (tiêu đề có "chờ duyệt"), không về danh sách thường'])

    # ======================================================================== XI. IN
    S11 = Sec()
    S11.add('In chi tiết từ danh sách', 'P0', [ACC_A_S, 'Phiếu %s (A, TP đã duyệt) có số như phiếu M.' % P3], [MENU, 'Ở dòng %s bấm ba chấm > In chi tiết.' % P3], '—',
            ['Popup xem trước "Xem trước phiếu: %s — chi tiết", khổ A4 ngang' % P3, 'Góc phải: "Số: %s", "Ngày lập: dd/mm/yyyy"' % P3,
             'Tiêu đề "%s"; dòng "Năm: 2026 · Nhân viên: Nguyễn Văn A · Phòng ban: Kinh doanh 1 · Trạng thái: TP đã duyệt"' % P['UP'],
             'Bảng cây Tháng > Tỉnh/TP, dòng "TỔNG — Nguyễn Văn A", số dạng 1,234,567'])
    S11.add('In theo thị trường kèm chỉ tiêu', 'P1', [ACC_A_S, 'Như trên.'], [MENU, 'Bấm In theo thị trường.'], '—',
            ['Popup "… — theo thị trường"', 'Cây Tỉnh/TP > Tháng, có chỉ tiêu giao như thẻ Theo thị trường ở màn Xem (gồm Quảng Ninh chưa lập)'])
    S11.add('In theo tháng', 'P1', [ACC_A_S, 'Như trên.'], [MENU, 'Bấm In theo tháng.'], '—', ['Popup "… — theo tháng", cây Tháng > Tỉnh/TP theo thứ tự tỉnh'])
    S11.add('Nút In ở màn Xem in theo thẻ đang chọn', 'P1', [ACC_A_S, 'Như trên.'], [MENU, 'Mở Xem %s, bấm thẻ Theo thị trường, bấm In.' % P3], '—', ['Bản in kiểu theo thị trường'])
    S11.add('Khối ký tên', 'P1', [ACC_A_S, 'Như trên (B duyệt 12/11/2026).'], [MENU, 'In chi tiết %s.' % P3], '—',
            ['3 cột ký: Người lập (Nguyễn Văn A, Ngày lập), Trưởng phòng (Trần Văn B, Ngày 12/11/2026), Ban giám đốc (trống)', 'Tên và chữ "Ngày" nằm 2 dòng riêng, không dính'])
    S11.add('Letterhead theo công ty của phiếu', 'P2', 'Tài khoản V4 đang làm việc ở công ty TPE.', [MENU, 'In chi tiết %s (công ty TPSG).' % P8], '—',
            ['Đầu trang là letterhead của TPSG, không phải TPE'])
    S11.add('Phiếu Hủy không in', 'P1', [ACC_A_S, 'Phiếu %s đã Hủy.' % M], [MENU, 'Mở ba chấm dòng %s; mở Xem.' % M], '—', ['Không có mục In nào'])
    S11.add('In phiếu lập trên hệ thống cũ', 'P2', [ACC_A_S, 'Phiếu cũ %s.' % P['LEGACY']], [MENU, 'In chi tiết phiếu cũ.'], '—', ['In được theo dòng Tỉnh/TP, SL khách đúng như màn Xem'])

    # ======================================================================== XII. TÙY CHỈNH CỘT
    S12 = Sec()
    S12.add('Mở popup cấu hình cột', 'P1', ACC_B, [MENU, 'Bấm Cấu hình cột hiển thị.'], '—',
            ['Liệt kê đủ cột: STT, Số phiếu, Năm, Nhân viên, Bộ phận, Phòng ban, %s%s, Người lập, Ngày lập, Người duyệt, Ngày duyệt, Trạng thái, Hành động'
             % (P['LIST_NUM'], (', ' + P['LIST_HID']) if P['LIST_HID'] else ''), 'Cột đang hiện được tick sẵn'])
    S12.add('Hiện cột đang ẩn', 'P1', ACC_B, [MENU, 'Mở cấu hình, tick Phòng ban, Người lập, lưu.'], '—', ['2 cột hiện ra với đúng dữ liệu'])
    S12.add('Ẩn cột đang hiện', 'P1', ACC_B, [MENU, 'Mở cấu hình, bỏ tick Người duyệt, lưu.'], '—', ['Cột Người duyệt biến mất'])
    S12.add('Cột khoá không ẩn được', 'P2', ACC_B, [MENU, 'Mở cấu hình.'], '—', ['STT, Số phiếu, Hành động không bỏ tick được', 'STT và Số phiếu đứng yên khi cuộn ngang'])
    S12.add('Kéo thả đổi thứ tự cột', 'P2', ACC_B, [MENU, 'Kéo cột Trạng thái lên sau Số phiếu, lưu.'], '—', ['Bảng đổi thứ tự đúng'])
    S12.add('Đóng không lưu', 'P2', ACC_B, [MENU, 'Mở cấu hình, đổi vài cột, đóng không lưu.'], '—', ['Bảng giữ như cũ'])
    S12.add('Ghi nhớ sau F5 và theo tài khoản', 'P2', 'A và B dùng chung trình duyệt.', ['B ẩn cột Người duyệt, nhấn F5.', 'Đăng nhập A, mở màn.'], '—',
            ['B: sau F5 cột vẫn ẩn', 'A: cấu hình riêng của A'])
    S12.add('Không ảnh hưởng dữ liệu và bộ lọc', 'P2', ACC_B, [MENU, 'Lọc Chờ TP duyệt.', 'Ẩn / hiện cột.'], '—', ['Số phiếu và bộ lọc giữ nguyên'])

    # ======================================================================== XIII. XUẤT EXCEL
    S13 = Sec()
    S13.add('Mở popup chọn trường', 'P1', ACC_B, [MENU, 'Bấm Xuất Excel.'], '—',
            ['Danh sách trường: Số phiếu, Năm, Nhân viên, Bộ phận, Phòng ban, %s%s, Người lập, Ngày lập, Người duyệt, Ngày duyệt, Trạng thái'
             % (P['LIST_NUM'], (', ' + P['LIST_HID']) if P['LIST_HID'] else ''), 'Trường chọn sẵn = các cột đang hiện trên bảng'])
    S13.add('Xuất với trường mặc định', 'P0', [ACC_B, DATA], [MENU, 'Bấm Xuất Excel > Xuất file.'], '—',
            ['Tải file "%s"' % ('ke_hoach_ban_hang_nhan_vien.xlsx' if P['GIA_TRI_HD'] else 'ke_hoach_phat_trien_thi_truong_nhan_vien.xlsx'),
             'Tiêu đề "DANH SÁCH %s", cột STT + các trường đã chọn đúng thứ tự' % P['UP'], 'Có 4 dòng (%s, %s, %s, %s), báo "Xuất Excel thành công"' % (P2, P3, P4, P6)])
    S13.add('Xuất tất cả / một số trường', 'P1', ACC_B, [MENU, 'Xuất Excel: chọn tất cả, xuất.', 'Xuất lần 2 chỉ chọn Số phiếu, Trạng thái.'], '—',
            ['Lần 1 đủ mọi cột', 'Lần 2 chỉ STT, Số phiếu, Trạng thái'])
    S13.add('Không chọn trường nào', 'P2', ACC_B, [MENU, 'Xuất Excel, bỏ hết tick.'], '—', ['Không xuất được (nút Xuất bị chặn hoặc báo phải chọn trường)'])
    S13.add('Xuất theo tìm kiếm và bộ lọc', 'P0', [ACC_B, DATA], [MENU, 'Lọc Trạng thái Chờ TP duyệt, gõ "Nguyễn Văn A".', 'Xuất Excel > Xuất file.'], '—',
            ['File chỉ có 1 dòng %s' % P2])
    S13.add('Xuất nhiều trang', 'P1', 'Tài khoản V4, 25 phiếu, đang ở trang 1 (10 dòng).', [MENU, 'Xuất Excel > Xuất file.'], '—',
            ['File có đủ 25 dòng, STT 1 tới 25', 'Trong lúc xuất có dòng tiến độ "Đã tải …/25 dòng…"'])
    S13.add('Danh sách rỗng', 'P1', ACC_A_S, [MENU, 'Lọc Năm 2030.', 'Xuất Excel > Xuất file.'], '—', ['Báo "Không có dữ liệu để xuất", không tải file'])
    S13.add('Định dạng số, ngày, tiếng Việt', 'P1', [ACC_B, DATA], [MENU, 'Xuất Excel đủ trường.'], '—',
            ['Cột số là số thật, cộng được bằng hàm tổng', 'Ngày lập dạng dd/mm/yyyy', 'Tên tiếng Việt có dấu đúng, Trạng thái ghi chữ (Chờ TP duyệt…)'])
    S13.add('Xuất từ lối vào chờ duyệt', 'P1', [ACC_B, DATA], [MENU_CD, 'Xuất Excel > Xuất file.'], '—', ['File có đúng 3 phiếu chờ duyệt'])
    S13.add('Xuất Excel 1 phiếu', 'P0', [ACC_A_S, 'Phiếu %s (TP đã duyệt) số như phiếu M.' % P3], [MENU, 'Ở dòng %s bấm ba chấm > Xuất Excel.' % P3, 'Mở Xem %s, bấm Xuất Excel.' % P3], '—',
            ['Tải file "%s.xlsx", báo "Xuất Excel thành công"' % P3, 'File có 3 trang tính: Chi tiết theo tháng, Theo thị trường, Theo tháng',
             'Mỗi trang có tiêu đề "%s" và dòng "Số: %s · Năm: 2026 · Nhân viên: Nguyễn Văn A · Phòng ban: Kinh doanh 1 · Trạng thái: TP đã duyệt"' % (P['UP'], P3)])
    S13.add('Excel 1 phiếu: số liệu và định dạng', 'P1', [ACC_A_S, 'Như trên.'], ['Mở file vừa xuất.'], '—',
            ['Số khớp 3 thẻ màn Xem (kể cả chỉ tiêu ở trang Theo thị trường)', 'Ô số là số thật dạng 1,234,567', 'Trang in khổ ngang'])

    # ======================================================================== XIV. RÀNG BUỘC
    S14 = Sec()
    S14.add('Yêu cầu issue: bỏ cột khách hàng, nhập số theo Tỉnh/TP', 'P0', ACC_A, [MENU, 'Bấm Tạo mới.'], '—',
            ['KHÔNG còn cột Khách hàng, Người liên hệ, Phân loại khách', P['ISSUE_COLS']]
            + (['Lưu ý: issue có nhắc "giá trị HĐ" nhưng bản chốt của khách chỉ giữ SL HĐ + DS tiêu chuẩn — màn không có cột Giá trị HĐ riêng'] if P['GIA_TRI_HD'] else []))
    S14.add('Chỉ lập kế hoạch của chính nhân viên', 'P0', ACC_B, [MENU, 'Bấm Tạo mới.'], '—',
            ['Ô Nhân viên khoá, luôn là tài khoản đang đăng nhập', 'Không có ô chọn Bộ phận / Phòng ban / Công ty để lập kế hoạch cấp đơn vị',
             'Số liệu bộ phận / phòng / công ty chỉ tổng hợp lên báo cáo (không lập ở màn này)'])
    S14.add('Chỉ tiêu lấy từ phiếu giao chỉ tiêu theo nhân viên Đã duyệt', 'P0', [ACC_A_S, 'Năm 2026 A có thêm 1 phiếu giao chỉ tiêu Chờ duyệt gồm Bắc Ninh.'],
            [MENU, 'Bấm Tạo mới, mở ô Tỉnh/TP.'], '—', ['Không có Bắc Ninh (phiếu giao chỉ tiêu chưa Đã duyệt không tính)'])
    S14.add('Chỉ tiêu cộng khách hãng và khách khác', 'P1',
            'Chỉ tiêu Hà Nội của A trên phiếu giao chỉ tiêu: hàng hóa khách hãng 3 khách / 1,500,000,000 + khách khác 1 khách / 500,000,000; dịch vụ khách hãng 2 / 500,000,000.',
            [MENU, 'Mở Xem phiếu M, thẻ Theo thị trường.'], '—', ['Chỉ tiêu Hà Nội hàng hóa = 4 khách / 2,000,000,000 (cộng 2 loại khách), dịch vụ 2 / 500,000,000'])
    S14.add('Chỉ tiêu vừa được duyệt mở khoá Tạo mới ngay', 'P1', ACC_C, ['Trưởng phòng duyệt phiếu giao chỉ tiêu 2026 của C.', 'C %s' % MENU, 'Bấm Tạo mới.'], '—',
            ['Mở được form, Tỉnh/TP theo chỉ tiêu vừa duyệt'])
    S14.add('Mở popup Lấy dữ liệu từ %s' % P['OTHER'], 'P0', [ACC_A_S, P['CV_SRC']], [MENU, 'Bấm Tạo mới (Năm 2026).', 'Bấm "Lấy dữ liệu từ %s".' % P['OTHER']], '—',
            ['Popup "Lấy dữ liệu từ %s", dòng gợi ý "Chỉ phiếu đã duyệt (TP đã duyệt / BGĐ đã duyệt) của bạn, năm 2026."' % P['OTHER'],
             'Ô "Phiếu nguồn" (bắt buộc) dạng "%s · TP đã duyệt · Duyệt 10/11/2026 · 2 tháng · 2 dòng tỉnh · …"' % P['CV_SRC_CODE'],
             'Ô "Hệ số chuyển đổi (báo giá ÷ hệ số = hợp đồng)" bắt buộc, mặc định 3, có icon giải thích', 'Nút Áp dụng (hiện khi có số để điền), Hủy'])
    S14.add('Chỉ phiếu nguồn đã duyệt, của mình, cùng năm', 'P0',
            [ACC_A_S, 'A có phiếu %s: 1 TP đã duyệt 2026, 1 BGĐ đã duyệt 2026, 1 Chờ TP duyệt 2026, 1 TP đã duyệt 2027; E có 1 phiếu TP đã duyệt 2026.' % P['OTHER']],
            [MENU, 'Tạo mới Năm 2026, mở popup lấy dữ liệu, mở ô Phiếu nguồn.'], '—',
            ['Chỉ có 2 phiếu (TP đã duyệt + BGĐ đã duyệt năm 2026 của A), phiếu mới duyệt đứng trước', 'Không có phiếu Chờ TP duyệt, phiếu 2027, phiếu của E'])
    S14.add('Chưa có phiếu nguồn', 'P1', 'Tài khoản E2: có chỉ tiêu 2026, chưa có phiếu %s nào được duyệt.' % P['OTHER'], [MENU, 'Tạo mới, bấm Lấy dữ liệu.'], '—',
            ['Popup ghi "Chưa có phiếu %s đã duyệt năm 2026", không có nút Áp dụng' % P['OTHER']])
    S14.add('Quy đổi theo hệ số 3', 'P0', [ACC_A_S, P['CV_SRC']], [MENU, 'Tạo mới Năm 2026, mở popup lấy dữ liệu.', 'Chọn phiếu nguồn %s, giữ hệ số 3.' % P['CV_SRC_CODE'], 'Bấm Áp dụng.'],
            'Hệ số: 3', ['Dòng tóm tắt "Sẽ điền 2 tháng · 2 dòng tỉnh — %s"' % P['CV_HINT']] + P['CV_RESULT']
            + ['Áp dụng: báo "Đã lấy dữ liệu từ %s (hệ số 3)", bảng điền đúng số, đứng ở thẻ Chi tiết theo tháng' % P['CV_SRC_CODE']])
    S14.add('Quy tắc làm tròn khi quy đổi', 'P1', [ACC_A_S, P['CV_ROUND_PRE']], [MENU, 'Tạo mới 2026, lấy dữ liệu từ phiếu nguồn trên.'],
            'Hệ số: %s' % ('3' if P['GIA_TRI_HD'] else '7'), P['CV_ROUND_EXP'])
    S14.add('Hệ số 0 báo đỏ', 'P0', [ACC_A_S, P['CV_SRC']], [MENU, 'Mở popup lấy dữ liệu, chọn phiếu nguồn.', 'Xoá hệ số, gõ 0.'], 'Hệ số: 0',
            ['Báo đỏ "Hệ số là số nguyên từ 1 đến 99" dưới ô', 'Bảng xem trước của hệ số cũ biến mất, nút Áp dụng ẩn', 'Không tự sửa số 0 thành 1'])
    S14.add('Hệ số sai định dạng', 'P1', [ACC_A_S, P['CV_SRC']], [MENU, 'Mở popup lấy dữ liệu, lần lượt gõ hệ số: trống, abc, 1.5, 100.'], 'trống; abc; 1.5; 100',
            ['Mỗi giá trị đều báo đỏ "Hệ số là số nguyên từ 1 đến 99" (ô chỉ gõ tối đa 2 ký tự)', 'Gõ 99 thì hợp lệ, bảng xem trước tính lại'])
    S14.add('Ghi đè dữ liệu đang nhập', 'P0', [ACC_A_S, P['CV_SRC']], [MENU, 'Tạo mới, nhập dòng Quảng Ninh Tháng 11.', 'Lấy dữ liệu, bấm Áp dụng, chọn Hủy.', 'Áp dụng lại, chọn Ghi đè.'], '—',
            ['Hộp "Ghi đè dữ liệu", nội dung "Ghi đè dữ liệu đang nhập? Số liệu theo tháng hiện có sẽ được thay bằng dữ liệu lấy từ %s.", nút Hủy / Ghi đè' % P['CV_SRC_CODE'],
             'Hủy: bảng giữ dòng Quảng Ninh', 'Ghi đè: thay TOÀN BỘ bảng, dòng Quảng Ninh mất'])
    S14.add('Bỏ tháng trước tháng bắt đầu và tỉnh ngoài chỉ tiêu', 'P1',
            [ACC_A_S, 'Phiếu nguồn của A (đã duyệt, 2026) có Tháng 10 Hà Nội, Tháng 11 Hà Nội và Bắc Ninh (Bắc Ninh không có trong chỉ tiêu của A); hôm nay %s.' % TODAY],
            [MENU, 'Tạo mới 2026, lấy dữ liệu từ phiếu đó.'], '—',
            ['Dòng cảnh báo "Bỏ 1 tháng trước tháng 11, bỏ 1 dòng tỉnh ngoài chỉ tiêu"', 'Chỉ điền Tháng 11 Hà Nội',
             'Thông báo sau áp dụng có thêm "— bỏ 1 tháng trước tháng 11, bỏ 1 dòng tỉnh ngoài chỉ tiêu"'])
    S14.add('Không còn gì để điền', 'P2', [ACC_A_S, 'Phiếu nguồn chỉ có Tháng 10 (hôm nay tháng 11).'], [MENU, 'Tạo mới 2026, lấy dữ liệu từ phiếu đó.'], '—',
            ['Ghi "Không còn tháng / tỉnh nào để điền (Bỏ 1 tháng trước tháng 11)"', 'Không có nút Áp dụng'])
    S14.add('Áp dụng xong vẫn sửa tay và lưu', 'P1', [ACC_A_S, P['CV_SRC']], [MENU, 'Tạo mới, lấy dữ liệu hệ số 3, Áp dụng.', 'Sửa SL khách Hà Nội, bấm Lưu.', 'Mở lại phiếu nguồn.'], '—',
            ['Lưu theo số đã sửa tay', 'Phiếu nguồn không đổi, phiếu mới không ghi lại phiếu nguồn / hệ số'])
    S14.add('Phiếu nguồn lập trên hệ thống cũ', 'P2', [ACC_A_S, 'A có phiếu %s cũ (lập trên hệ thống cũ) năm 2026, BGĐ đã duyệt, có dòng Tháng 12 Hà Nội.' % P['OTHER']],
            [MENU, 'Tạo mới 2026, lấy dữ liệu từ phiếu cũ đó.'], '—', ['Có trong ô Phiếu nguồn, quy đổi theo số ở dòng Tỉnh/TP'])
    S14.add('Lấy dữ liệu ở form Sửa', 'P1', [ACC_A_S, PLAN_M, P['CV_SRC']], [MENU, 'Mở Sửa %s, bấm Lấy dữ liệu, Áp dụng > Ghi đè, Lưu.' % M], '—',
            ['Thay toàn bộ bảng của %s theo phiếu nguồn, số phiếu giữ nguyên' % M])
    S14.add('Phiếu vừa duyệt thành phiếu nguồn của kế hoạch kia', 'P1', [ACC_A_S, 'Phiếu %s của A vừa được TP duyệt.' % P3], [P['OTHER_MENU'], 'Tạo mới 2026, bấm "Lấy dữ liệu từ %s".' % P['kh'].replace('kế hoạch', 'KH').replace('KH phát triển thị trường', 'KH phát triển thị trường')], '—',
            ['Ô Phiếu nguồn có %s' % P3])
    S14.add('Nhân viên mới: chỉ tiêu dự kiến gắn vào tài khoản trưởng phòng', 'P0',
            [ACC_B, 'Phiếu giao chỉ tiêu 2026 phòng KD1 có dòng chỉ tiêu dự kiến cho nhân viên mới (chưa có người) ở Hải Phòng; B sửa phiếu giao chỉ tiêu, gắn dòng đó vào tài khoản B, phiếu được Đã duyệt.'],
            [MENU, 'B bấm Tạo mới, mở ô Tỉnh/TP.', 'Nhập Hải Phòng hợp lệ, bấm Lưu và gửi.'], '—',
            ['Ô Tỉnh/TP của B có Đà Nẵng và Hải Phòng', 'Phiếu của B gửi thẳng Chờ BGĐ duyệt'])
    S14.add('Dòng chỉ tiêu nhân viên mới chưa gắn tài khoản', 'P1', 'Phiếu giao chỉ tiêu 2026 có dòng nhân viên mới ở Quảng Trị chưa gắn tài khoản nào.',
            ['A, B lần lượt Tạo mới, mở ô Tỉnh/TP.'], '—', ['Không ai có Quảng Trị (phần chỉ tiêu chưa gắn người thì chưa lập kế hoạch được)'])
    S14.add('Có nhân viên mới: trưởng phòng giao lại, nhân viên mới tự lập', 'P0',
            'Tài khoản N2: nhân viên mới vào phòng KD1. B sửa phiếu giao chỉ tiêu 2026, chuyển chỉ tiêu Hải Phòng từ B sang N2, phiếu được Đã duyệt lại.',
            ['N2 %s, bấm Tạo mới, lập Hải Phòng, Lưu và gửi.' % P['OTHER_MENU'], 'N2 %s, bấm Tạo mới, lập Hải Phòng, Lưu và gửi.' % MENU, 'B mở lối vào "%s".' % P['CD']], '—',
            ['N2 lập được cả kế hoạch phát triển thị trường và kế hoạch bán hàng với Hải Phòng', 'Cả 2 phiếu Chờ TP duyệt, B thấy ở lối vào chờ duyệt và duyệt được',
             'Tạo mới của B không còn Hải Phòng'])
    S14.add('Phiếu trưởng phòng lập trước khi giao lại giữ nguyên', 'P1', 'Như trên, B đã có phiếu (Đang tạo) có dòng Hải Phòng trước khi chuyển chỉ tiêu cho N2.',
            [MENU, 'B mở Sửa phiếu đó.'], '—', ['Dòng Hải Phòng cũ vẫn hiện, sửa / lưu được', 'Dòng mới không chọn được Hải Phòng'])
    S14.add('Người lập chuyển phòng', 'P2', [PEND, 'Sau khi gửi, A chuyển sang phòng KD2 (trưởng phòng H).'], ['B mở lối vào "%s".' % P['CD'], 'H mở lối vào "%s".' % P['CD']], '—',
            ['%s vẫn thuộc phòng KD1 lúc lập: B duyệt, H không thấy' % P2])
    S14.add('Menu ở hệ thống cũ mở màn mới', 'P2', ACC_A_S, ['Đăng nhập hệ thống cũ, mở menu Kế hoạch, bấm mục danh sách kế hoạch nhân viên tương ứng.'], '—',
            ['Mở %s trên hệ thống mới ở thẻ trình duyệt mới' % ten, 'Hệ thống cũ không còn màn lập / sửa / chờ duyệt kế hoạch nhân viên'])

    # ======================================================================== XV. PHÂN QUYỀN
    S15 = Sec()
    S15.add('Không có quyền nào', 'P0', [ACC_A_S, DATA], [MENU], '—',
            ['Vào được màn, thấy 3 phiếu mình lập', 'Lập được phiếu (có chỉ tiêu), sửa / gửi / hủy phiếu của mình', 'Không thấy phiếu người khác'])
    S15.add('Quyền %s mức Phòng ban' % QV, 'P0', ['Tài khoản V2: thuộc phòng KD2, có quyền %s mức Phòng ban.' % QV, DATA], [MENU], '—',
            ['Thấy %s (phòng KD2)' % P7, 'Không thấy phiếu phòng KD1, công ty TPSG'])
    S15.add('Quyền %s mức Công ty' % QV, 'P0', ['Tài khoản V3: công ty TPE, quyền %s mức Công ty.' % QV, DATA], [MENU], '—',
            ['Thấy 5 phiếu %s, %s, %s, %s, %s' % (P2, P3, P4, P6, P7), 'Không thấy %s (TPSG), %s, %s (Đang tạo)' % (P8, M, P5)])
    S15.add('Quyền %s mức Tổng công ty' % QV, 'P0', ['Tài khoản V4: quyền %s mức Tổng công ty.' % QV, DATA], [MENU, ADV], '—',
            ['Thấy 6 phiếu (thêm %s của TPSG)' % P8, 'Bộ lọc có ô Công ty'])
    S15.add('Quyền xem không mở thao tác', 'P0', ['Tài khoản V4 như trên.', PEND], [MENU, 'Mở Xem %s.' % P2], '—',
            ['Chỉ có Xuất Excel, In, Quay lại', 'Không có Duyệt, Từ chối, Sửa, Hủy phiếu', 'Không thấy mục "%s"' % P['CD']])
    S15.add('Quyền %s' % QA, 'P0', [ACC_B, DATA], [MENU_CD, 'Duyệt %s.' % P2], '—',
            ['Có mục "%s" ở nhóm Phê Duyệt' % P['CD'], 'Duyệt / Từ chối / Gửi BGĐ được phiếu phòng KD1'])
    S15.add('Trưởng phòng quản lý phòng thấy phiếu phòng', 'P0', ['Tài khoản B2: trưởng phòng KD1, không có quyền nào của màn.', DATA], [MENU], '—',
            ['Thấy %s, %s, %s, %s (mọi phiếu KD1 trừ Đang tạo)' % (P2, P3, P4, P6), 'Bộ lọc và cột như cấp trên (có Nhân viên)', 'Chỉ xem'])
    S15.add('Trưởng bộ phận thấy phiếu bộ phận, chỉ xem', 'P0', [ACC_D, DATA], [MENU, 'Mở Xem %s.' % P2], '—',
            ['Thấy %s, %s (A thuộc Nhóm KD1-1)' % (P2, P3), 'Không thấy %s (Nhóm KD1-2)' % P4, 'Màn Xem chỉ có Xuất Excel, In, Quay lại'])
    S15.add('Người đã duyệt vẫn thấy phiếu', 'P1', [ACC_B, HAPP, 'Sau đó B chuyển sang quản lý phòng KD3 và bị gỡ quyền duyệt.'], [MENU], '—',
            ['B vẫn thấy %s (phiếu mình đã duyệt)' % P3, 'Không còn thấy các phiếu KD1 khác'])
    S15.add('Hai vai trò khác mức thì lấy mức lớn hơn', 'P0', ['Tài khoản V5: vai trò 1 cấp %s mức Phòng ban, vai trò 2 cấp mức Công ty.' % QV, DATA], [MENU], '—',
            ['Thấy 5 phiếu như mức Công ty'])
    S15.add('Ẩn nút khi không có quyền thao tác', 'P0', ['Tài khoản V4 (mức Tổng công ty).', DATA], [MENU, 'Mở ba chấm các dòng.'], '—',
            ['Không có Sửa, Gửi duyệt, Duyệt, Gửi BGĐ, Hủy phiếu ở phiếu người khác', 'Chỉ Xem, In, Xuất Excel, Lịch sử'])
    S15.add('Mở thẳng màn Xem phiếu ngoài phạm vi', 'P0', [ACC_A_S, 'E gửi cho A đường dẫn màn Xem phiếu %s.' % P7], ['A mở đường dẫn đó.'], '—',
            ['Không hiện dữ liệu phiếu, tự quay về danh sách của A'])
    S15.add('Mở thẳng màn Sửa phiếu người khác', 'P0', [ACC_B, 'A gửi cho B đường dẫn màn Sửa %s (Đang tạo).' % M], ['B mở đường dẫn đó.'], '—',
            ['Không mở được form, quay về danh sách', 'Phiếu M không đổi'])
    S15.add('Mở lối vào chờ duyệt khi thiếu quyền', 'P0', ACC_A_S, ['A mở đường dẫn lối vào "%s" do B gửi.' % P['CD']], '—',
            ['Danh sách chờ duyệt rỗng (%s)' % EMPTY, 'Không thấy phiếu của người khác'])
    S15.add('Bị gỡ quyền duyệt giữa lúc thao tác', 'P0', [ACC_B, PEND], OPEN_P2_B + ['Quản trị gỡ quyền %s của B.' % QA, 'B bấm Duyệt > Duyệt.'], '—',
            ['B báo %s' % NOPERM, 'Phiếu vẫn Chờ TP duyệt', 'Tải lại: mục "%s" biến mất' % P['CD']])
    S15.add('Được cấp quyền giữa lúc thao tác', 'P1', ['Tài khoản B2 (trưởng phòng KD1, chưa có quyền duyệt) đang mở Xem %s.' % P2], ['Quản trị cấp quyền %s cho B2.' % QA, 'B2 tải lại trang.'], '—',
            ['Hiện nút Duyệt, Từ chối và mục "%s"' % P['CD']])
    S15.add('Đổi công ty đang làm việc', 'P0', ['Tài khoản V6: quyền %s mức Công ty ở công ty TPE; ở TPSG không có quyền.' % QV, DATA], [MENU, 'Đổi công ty đang làm việc sang TPSG, mở lại màn.'], '—',
            ['Quyền tính lại theo TPSG: chỉ còn phiếu mình lập / mình quản lý', 'Không còn thấy phiếu công ty TPE'])
    S15.add('Ban giám đốc không có chỉ tiêu bấm Tạo mới', 'P1', 'Tài khoản BGĐ: quyền %s mức Tổng công ty, không có chỉ tiêu.' % QV, [MENU, 'Bấm Tạo mới.'], '—',
            ['Nút Tạo mới vẫn hiện nhưng bấm thì hiện hộp %s' % BLOCK_TITLE])
    S15.add('Xuất Excel, In, Lịch sử theo phạm vi xem', 'P1', [ACC_D, DATA], [MENU, 'Xuất Excel danh sách; In và xem Lịch sử %s.' % P2], '—',
            ['File chỉ có 2 phiếu D xem được', 'In và Lịch sử mở được, không cần quyền riêng'])
    S15.add('Quyền của kế hoạch kia không tác dụng ở màn này', 'P1', ['Tài khoản V7: chỉ có quyền "%s" mức Tổng công ty và "%s".' % (P['Q_VIEW_OTHER'], P['Q_APP_OTHER']), DATA],
            [MENU, 'Mở nhóm Phê Duyệt > Kế hoạch & chỉ tiêu.'], '—', ['Màn này chỉ thấy phiếu V7 tự lập', 'Không có mục "%s"' % P['CD']])
    S15.add('Tên quyền trong màn Vai trò', 'P2', 'Tài khoản quản trị.', ['Mở màn phân quyền Vai trò, tìm nhóm Bán hàng > %s.' % ('Kế hoạch bán hàng' if P['GIA_TRI_HD'] else 'Kế hoạch phát triển thị trường')], '—',
            ['Có quyền %s với các mức Phòng ban / Công ty / Tổng công ty' % QV, 'Có quyền %s (không có mức)' % QA])

    sections = [
        ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
        ('II', 'TÌM KIẾM & LỌC DANH SÁCH', S2),
        ('III', 'THÊM MỚI', S3),
        ('IV', 'CHỈNH SỬA', S4),
        ('V', 'GỬI DUYỆT', S5),
        ('VI', 'DUYỆT PHIẾU – TRƯỞNG PHÒNG DUYỆT VÀ GỬI BGĐ', S6),
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

    cols_txt = '; '.join(P['FORM_COLS'])
    desc = [
        ('1. Mục đích tính năng',
         '%s (%s, phân hệ Bán hàng > Kế hoạch): mỗi nhân viên tự lập kế hoạch theo tháng và Tỉnh/TP trong phạm vi chỉ tiêu được giao; '
         'trưởng phòng duyệt, gửi Ban giám đốc. Bỏ tầng khách hàng của hệ thống cũ — nhập số thẳng trên dòng Tỉnh/TP. Có 3 cách xem '
         '(Chi tiết theo tháng / Theo thị trường so chỉ tiêu / Theo tháng), In 3 kiểu A4 ngang, Xuất Excel, Lấy dữ liệu từ %s theo hệ số.'
         % (TEN, P['issue'], P['OTHER'])),
        ('2. Đối tượng được tính / hiển thị',
         '- Trạng thái: Đang tạo, Chờ TP duyệt, TP đã duyệt, Chờ BGĐ duyệt, BGĐ đã duyệt, Hủy.\n'
         '- Lối vào danh sách ("%s"): phiếu mình lập (mọi trạng thái) + phiếu trong phạm vi quyền xem / phòng mình quản lý / bộ phận mình '
         'quản lý / phiếu mình đã duyệt + phiếu Chờ TP duyệt mình duyệt được.\n'
         '- Lối vào "%s": phiếu Chờ TP duyệt và TP đã duyệt của phòng mình duyệt được, không phải mình lập, không phải phiếu hệ thống cũ.\n'
         '- Phiếu lập trên hệ thống cũ (có dòng khách hàng) vẫn hiện, chỉ Xem / In / Xuất Excel.' % (P['MAN'], P['CD'])),
        ('3. Đối tượng bị ẩn / không tính',
         '- Phiếu Đang tạo của người khác (kể cả với trưởng phòng / quyền xem Tổng công ty).\n'
         '- Phiếu ngoài phạm vi: phòng / bộ phận / công ty khác khi không có quyền tương ứng.\n'
         '- Ô Tỉnh/TP: tỉnh ngoài chỉ tiêu được giao của năm phiếu; tỉnh đã chọn ở dòng khác cùng tháng.\n'
         '- Phiếu nguồn để lấy dữ liệu: phiếu chưa duyệt (Đang tạo / Chờ TP duyệt / Chờ BGĐ duyệt / Hủy), phiếu của người khác, phiếu khác năm.'),
        ('4. Bộ lọc thời gian áp dụng cho',
         '- Ô Năm (danh sách): năm của phiếu kế hoạch, lựa chọn từ năm nay +4 xuống 2023.\n'
         '- Ô Năm (form): năm nay tới năm nay +4; mặc định năm sớm nhất có chỉ tiêu. Năm = năm hiện tại thì có tháng lập phiếu tới tháng 12; '
         'năm sau có đủ 12 tháng. Khi Sửa, tháng tính theo ngày lập phiếu.'),
        ('5. Cấu trúc dữ liệu / cây phân cấp',
         '- Phiếu > Tháng > Tỉnh/TP. Cột số: %s.\n- Thẻ Theo thị trường: Tỉnh/TP > Tháng (kèm chỉ tiêu giao). Thẻ Theo tháng: Tháng > Tỉnh/TP.' % cols_txt),
        ('6. Quy tắc cộng dồn / deduplicate',
         '- Tổng cộng = hàng hóa + dịch vụ (tự tính). Số của tháng = cộng các dòng Tỉnh/TP; số của phiếu = cộng các tháng.\n'
         '- 1 Tỉnh/TP chỉ 1 dòng trong 1 tháng; cùng tỉnh ở nhiều tháng thì thẻ Theo thị trường gộp lại.\n'
         '- Chỉ tiêu theo tỉnh = cộng khách hãng + khách khác của các phiếu giao chỉ tiêu theo nhân viên Đã duyệt cùng năm.\n'
         '- Phiếu hệ thống cũ: SL khách = số khách hàng khác nhau của từng dòng Tỉnh/TP, cộng lại.\n'
         '- Một nhân viên được lập nhiều phiếu trong cùng 1 năm.'),
        ('7. Phân quyền cấp',
         '- %s — mức: Phòng ban / Công ty / Tổng công ty (mức Tổng công ty có thêm ô lọc Công ty).\n'
         '- %s: duyệt / từ chối / gửi BGĐ phiếu của phòng mình (phải có quyền VÀ quản lý phòng của phiếu hoặc ngồi cùng phòng; '
         'không duyệt phiếu mình lập); hiện mục "%s".\n'
         '- Không cần quyền để mở màn và lập phiếu: chỉ cần có phiếu giao chỉ tiêu theo nhân viên Đã duyệt từ năm nay trở đi. Trưởng phòng '
         'thấy phiếu phòng mình quản lý, trưởng bộ phận thấy phiếu bộ phận mình quản lý (chỉ xem), người đã duyệt thấy phiếu mình duyệt.'
         % (P['Q_VIEW'], P['Q_APP'], P['CD'])),
        ('8. Cách tính các ô thống kê',
         '- Dòng TỔNG: "<tên nhân viên> - <tổng SL khách> khách - <số Tỉnh/TP khác nhau> thị trường".\n'
         '- Dòng tháng: "Tháng N (<SL khách> khách)".\n- Cột danh sách: %s = tổng của phiếu.\n'
         '- Người duyệt / Ngày duyệt = lần duyệt gần nhất (BGĐ nếu có, không thì TP).\n'
         '- Lấy dữ liệu: %s.' % (P['LIST_NUM'], P['CV_HINT'])),
        ('9. Ghi chú đọc bảng',
         '- Số nguyên, dấu phẩy ngăn nghìn 1,234,567; ô 0 ở dòng Tỉnh/TP để trống.\n'
         '- So chỉ tiêu CHỈ hiển thị ở thẻ Theo thị trường, KHÔNG chặn lưu / gửi.\n'
         '- Phiếu trưởng phòng lập: Gửi duyệt đi thẳng Chờ BGĐ duyệt. Màn BGĐ duyệt chưa làm (phiếu dừng ở Chờ BGĐ duyệt, BGĐ chưa nhận thông báo).\n'
         '- Từ chối bắt buộc lý do, phiếu về Đang tạo. Không có Xóa phiếu (thay bằng Hủy); không có Hủy duyệt.\n'
         '- Dòng ghi chú của phiếu hệ thống cũ có ghi tên hệ thống cũ (nguyên văn trên màn).\n'
         '- Bộ lọc ghi nhớ 10 phút theo trình duyệt. Các ca có 2 thẻ / 2 tài khoản cần chuẩn bị dữ liệu như Tiền điều kiện.'
         + ('\n- Issue nhắc "giá trị HĐ" nhưng bản chốt của khách chỉ giữ SL HĐ + DS tiêu chuẩn — không có cột Giá trị HĐ.' if P['GIA_TRI_HD'] else '')),
    ]
    return desc, sections


# ============================================================================ KIỂM THUẬT NGỮ (skill)
BANNED = [
    r"`[a-z_]{3,}`", r"\bBE\b", r"\bFE\b", r"\bHTTP\b",
    r"trả (400|403|404|422)", r"\b(400|403|404|422)\b",
    r"permission id", r"/api/v1", r"\bAPI /", r"localStorage",
    r"number_format", r"meta\.", r"sort_by", r"per_page",
    r"role_has_permissions", r"current_company_role",
    r"\bERP\b", r"\bAPI\b", r"https?://", r"\?type=", r"is_can_", r"form_version",
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
    ok_all = True
    for kind in ('sale', 'market'):
        P = KINDS[kind]
        desc, sections = make(P)
        ids = [(r, tc[0]) for r, _, s in sections for tc in s]
        assert len(ids) == len(set(ids)), 'Trùng mã TC'
        total = len(ids)
        p0 = sum(1 for _, _, s in sections for tc in s if tc[2] == 'P0')
        print('==', P['TEN'])
        print('Tong %d TC, P0 %d (%.1f%%)' % (total, p0, 100.0 * p0 / total))
        for r, t, s in sections:
            print('  %-5s %-55s %3d' % (r, t, len(s)))
        ok_all &= check_terms(desc, sections)
        build_chuan(output_file=os.path.join(HERE, P['file']), sheet_name='Trang tính1',
                    feature_name='%s - Cập nhật ngày %s' % (P['TEN'], TODAY), module_name=P['module'],
                    description_block=desc, sections=[(r, t, list(s)) for r, t, s in sections], loai='phieu')
    sys.exit(0 if ok_all else 1)

# -*- coding: utf-8 -*-
"""Testcase màn "Bảng cân đối phát sinh công nợ nhân viên" (HRM: phân hệ Tài chính > Kế toán công nợ > nhóm Nhân viên; port ERP
Kế toán > Kế toán Công nợ > Nhân viên). Kiểu ĐỐI CHIẾU CHÉO hệ thống cũ (ERP TanPhatDev) <-> hệ thống mới (HRM), 2 hệ thống dùng
CHUNG dữ liệu. Bản 06/11/2026.

Khuôn: skill testcase-documenter (chuẩn 03/11/2026) -> assets/tc_chuan.py `build_chuan(loai='bao_cao')`: nhóm chuẩn theo thứ tự,
PHÂN QUYỀN là nhóm cuối, mã TC_NN.NNN, không có nhóm TC-ROLE. `check_tc.py` CẤM chữ "ERP" / "API" / "E2E" / "gọi thẳng" trong ô
testcase -> trong case gọi "hệ thống cũ" (ERP) và "hệ thống mới" (HRM); mục 1 của khối mô tả định nghĩa 2 cụm này.

Nguồn đã đọc (06/11/2026):
  - Spec: docs/superpowers/specs/gop-db/2026-11-03-bang-can-doi-cong-no-nhan-vien-design.md (+ 2026-11-02 Sổ chi tiết công nợ NV),
    .plans/gop-db/bang-can-doi-cong-no-nv/{design,plan}.md
  - HRM FE: hrm-client/pages/finance/employee-debt-balances/{index.vue, components/constants.js},
    pages/finance/employee-debt-details/{index.vue, components/constants.js} (đích drill-down), components/subsystem-menu/finance.js
    (dòng 440-454), components/V2BaseCompanyDepartmentFilter.vue, utils/filterRequiredErrors.js, utils/mixins/{filterStateMixin,
    reportPrintPreviewMixin}.js, plugins/axios.js (câu báo 403), pages/finance/bill-adjust-depts/** (Phiếu kế toán dùng lập số liệu)
  - HRM BE: Modules/Finance/Http/Controllers/V1/EmployeeDebtBalanceController.php, Concerns/ValidatesAccountDebtFilters.php,
    Services/EmployeeDebt/EmployeeDebtBalanceService.php, Services/AccountDebt/Concerns/AccountDebtCommon.php, Routes/api.php
    (1951-1958), Tests/Feature/EmployeeDebtBalance{Api,Service}Test.php; Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
    (2014-2022)
  - ERP: app/Http/Controllers/Accounting/AccountDetailController.php (balanceDebtEmployee / searchDataBalanceEmployee),
    app/Model/Accounting/AccountDetail.php (searchByFilterData nhánh balance-employee 587-665, filterAccountDetail, mapDataBalanceDebt
    826-846, filterMoneyBalance 853-886), resources/views/accounting/account_details/balance-debt-employee.blade.php,
    layouts/topmenubar.blade.php (1187), routes/web.php (5076-5077); chứng từ ghi công nợ NV: BillPayment.php (saveAccountsDetail,
    saveAccountsDetailEmployee), BillPaymentAuthorization.php (33481), BillIncome.php (dòng chi tiết có nhân viên), BillAdjustDept.
  - DB gộp 06/11/2026: bút toán có nhân viên nhiều nhất ở 35241, 3351, 33481, 1411 (1411 chủ yếu từ hạch toán chuyến xe);
    TK 334 có con 3341, 3348 và cháu 33481; danh mục Loại tiền có 2 mục cùng tên "USD".
  - Mẫu: .plans/gop-db/hach-toan-cpvc-nhanh/testcase/gen_testcase_hach-toan-cpvc-nhanh.py,
    .plans/gop-db/finance-declare-debt-beginning/testcase/gen_testcase_cong-no-dau-ky-kh-hd.py
Chạy: PYTHONIOENCODING=utf-8 python3 gen_testcase_bang-can-doi-cong-no-nv.py
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '.claude', 'skills',
                                                'testcase-documenter', 'assets')))
from tc_chuan import build_chuan  # noqa: E402

NGAY = '06/11/2026'
TEN = 'Bảng cân đối phát sinh công nợ nhân viên'
MODULE = 'Bảng cân đối CN nhân viên'
OUT = os.path.join(HERE, 'testcase - Bang can doi phat sinh cong no nhan vien.xlsx')
SHEET = 'Trang tính1'


def L_(*lines):
    return '\n'.join(lines)


def C(func, prio, pre, steps, data, exp):
    """1 case: tiền điều kiện / test data nhận chuỗi hoặc list (mỗi phần tử 1 dòng); bước tự đánh số;
    expected mỗi ý 1 dòng "-  …"."""
    pre = pre if isinstance(pre, str) else L_(*pre)
    steps = [steps] if isinstance(steps, str) else steps
    exp = [exp] if isinstance(exp, str) else exp
    data = data if isinstance(data, str) else L_(*data)
    return (func, prio, pre,
            L_(*['%d. %s' % (i, s) for i, s in enumerate(steps, 1)]),
            data,
            L_(*['-  ' + e for e in exp]))


# ------------------------------------------------------------------ đường bấm, tên quyền, câu chữ trên màn
MENU = 'phân hệ Tài chính > Kế toán công nợ > nhóm "Nhân viên" > "Bảng cân đối phát sinh công nợ nhân viên"'
E_MENU = 'menu Kế toán > "Kế toán Công nợ" > nhóm "Nhân viên" > "Bảng cân đối phát sinh công nợ nhân viên"'
SCT = 'phân hệ Tài chính > Kế toán công nợ > nhóm "Nhân viên" > "Sổ chi tiết công nợ nhân viên"'
PKT = 'phân hệ Tài chính > Sổ tổng hợp > "Phiếu kế toán"'
Q_ALL = 'Xem bảng cân đối phát sinh công nợ nhân viên của tổng công ty'
Q_CTY = 'Xem bảng cân đối phát sinh công nợ nhân viên của công ty'
QS_ALL = 'Xem sổ chi tiết công nợ nhân viên của tổng công ty'
QS_CTY = 'Xem sổ chi tiết công nợ nhân viên của công ty'
TK = '141 - Tạm ứng'
KY = '01/10/2026 – 31/10/2026'
EMPTY = 'Không có dữ liệu phù hợp bộ lọc.'
NHAC = 'Chọn tài khoản và thời gian để xem bảng cân đối.'
KHONG_QUYEN = 'Bạn không có quyền thực hiện thao tác này'
CHOT = 'Khác biệt đã chốt, không ghi lỗi'
LOC = 'Tài khoản = ' + TK + ', Thời gian = ' + KY
DUYET = 'bấm "Lưu và duyệt" > "Duyệt" (ghi sổ)'
TIEU_DE_VND = ('STT, Mã nhân viên, Tên nhân viên, Loại tiền, rồi nhóm "VNĐ" gồm Dư đầu kỳ (Nợ, Có), Phát sinh (Nợ, Có), '
               'Dư cuối kỳ (Nợ, Có)')

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt (môi trường khác thì ghi mã thật vào cột Ghi chú):',
    '- TK-ALL: có "' + Q_ALL + '" + "' + QS_ALL + '". TK-CTY: thuộc công ty TPE, có "' + Q_CTY + '" + "' + QS_CTY + '".',
    '- TK-BC: chỉ có "' + Q_ALL + '" (không có quyền Sổ chi tiết). TK-Z: không có quyền nào của 2 màn. TK-KT: lập và duyệt được Phiếu kế toán.',
    '- Mỗi tài khoản dùng được ở CẢ 2 hệ thống, cùng quyền ở 2 bên.',
    '- Phòng PB-TEST (công ty TPE) chỉ có 2 nhân viên NV-A, NV-E, chưa có bút toán nào trên tài khoản 141 và các tài khoản con.',
    '- NV-B (công ty TPE) chưa có bút toán 141. NV-C thuộc công ty B (khác TPE).',
    '- Số liệu lập bằng Phiếu kế toán (' + PKT + '): mỗi phiếu 2 dòng định khoản, dòng 1411 chọn đối tượng Nhân viên; '
    'Lưu và duyệt = ghi sổ.',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Quy ước gọi tên trong tài liệu:',
        '- "Hệ thống cũ" = phần mềm ERP đang chạy song song.',
        '- "Hệ thống mới" = HRM.',
        '- 2 hệ thống dùng CHUNG dữ liệu: chứng từ lập ở bên nào thì bảng cân đối 2 bên đều đọc cùng một sổ.',
        'Kế toán xem SỐ DƯ CÔNG NỢ của từng nhân viên theo từng loại tiền trên một tài khoản theo dõi công nợ (141 Tạm ứng, '
        '1388, 334, 3348…): dư đầu kỳ, phát sinh trong kỳ, dư cuối kỳ (Nợ / Có); bấm mã nhân viên mở Sổ chi tiết công nợ nhân viên '
        'cùng bộ lọc. Màn CHỈ XEM.',
        'Lối vào hệ thống mới: ' + MENU + '. Lối vào hệ thống cũ: ' + E_MENU + '. Mỗi hệ thống chỉ có 1 lối vào.',
        'Chức năng: Tìm nhanh, Tìm kiếm nâng cao (bộ lọc), Làm mới, phân trang, In, Xuất Excel, bấm mã nhân viên sang Sổ chi tiết.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Mọi bút toán trên sổ CÓ GẮN NHÂN VIÊN, thuộc tài khoản đang chọn hoặc tài khoản CON TRỰC TIẾP của nó, có ngày hạch toán '
        'tới hết "Đến ngày" (kể cả trước "Từ ngày").',
        'Chứng từ sinh bút toán công nợ nhân viên: Phiếu chi (chi tạm ứng, chi thu nhập nhân viên), Phiếu ủy nhiệm chi (trả thu nhập '
        'nhân viên kinh doanh - 33481), Phiếu thu (dòng chi tiết chọn nhân viên - thu hoàn ứng), Phiếu kế toán (dòng định khoản chọn '
        'đối tượng Nhân viên), hạch toán chuyến xe (tạm ứng vận chuyển 1411), quyết toán hoa hồng / kết chuyển chi phí phải trả (3351)…',
        'Chỉ bút toán ĐÃ GHI SỔ mới lên bảng (Phiếu kế toán đã duyệt, phiếu chi / phiếu thu đã hạch toán).',
        '1 dòng = 1 nhân viên x 1 loại tiền (nhân viên có VNĐ và USD thì 2 dòng liền nhau).',
        'Phạm vi xem:',
        '- "' + Q_ALL + '": mọi công ty; khu vực lọc có ô Công ty.',
        '- "' + Q_CTY + '": bút toán của nhân viên thuộc công ty đang làm việc của người xem, CỘNG bút toán của chính người xem; '
        'không có ô Công ty.',
        '- Super Admin có cả 2 quyền.',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '- Bút toán KHÔNG gắn nhân viên.',
        '- Bút toán của tài khoản CHÁU trở xuống (vd chọn 334 thì lấy 334, 3341, 3348 nhưng KHÔNG lấy 33481).',
        '- Bút toán có ngày hạch toán SAU "Đến ngày".',
        '- Chứng từ chưa ghi sổ: Phiếu kế toán Lưu nháp, phiếu chi / phiếu thu chờ duyệt hoặc đã Hủy phiếu.',
        '- Bút toán ngoài phạm vi quyền; không có 1 trong 2 quyền thì không xem được gì.',
        '- Nhân viên có số dư bằng 0 và không phát sinh VẪN hiện (cả dòng để trống) - giống hệ thống cũ.',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô "Thời gian" (Từ - Đến, BẮT BUỘC) xét NGÀY HẠCH TOÁN của bút toán, không xét ngày tạo phiếu:',
        '- Ngày hạch toán TRƯỚC "Từ ngày": cộng vào Dư đầu kỳ.',
        '- Từ "Từ ngày" tới hết "Đến ngày" (tính cả 2 đầu mút): cộng vào Phát sinh Nợ / Có.',
        '- SAU "Đến ngày": không tính.',
        'Đổi kỳ sang tháng sau thì phát sinh tháng trước chuyển thành Dư đầu kỳ.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Bảng phẳng, không có cây. Tiêu đề 3 tầng.',
        '- Mẫu VNĐ (mặc định): ' + TIEU_DE_VND + '.',
        '- Mẫu Ngoại tệ: thêm nhóm "Nguyên tệ" (6 cột cùng cấu trúc) TRƯỚC nhóm "VNĐ"; nhóm Nguyên tệ chỉ có số ở dòng khác VNĐ.',
        'Dòng "Tổng": mỗi loại tiền 1 dòng, đặt ĐẦU bảng, hiện ở mọi trang, tính trên TOÀN BỘ dòng khớp bộ lọc (không chỉ trang đang xem).',
        'Sắp xếp cố định: Mã nhân viên tăng dần, rồi loại tiền (VNĐ trước); nhân viên không có hồ sơ (mã trống) ở cuối. Không bấm tiêu đề để sắp xếp.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '- Cộng TẤT CẢ bút toán của 1 nhân viên x 1 loại tiền trên tài khoản chọn + tài khoản con trực tiếp thành 1 dòng (không tách theo tài khoản con).',
        '- Dư đầu kỳ ròng = tổng Nợ - tổng Có trước "Từ ngày"; dương hiện cột Nợ, âm hiện cột Có (giá trị tuyệt đối).',
        '- Phát sinh Nợ / Có = tổng Nợ / tổng Có trong kỳ, hiện thẳng (không bù trừ).',
        '- Dư cuối kỳ ròng = Dư đầu kỳ ròng + Phát sinh Nợ - Phát sinh Có; tách Nợ / Có theo dấu như dư đầu kỳ.',
        '- Tính cho cả số nguyên tệ và số quy đổi VNĐ, MỌI loại tiền.',
        '- Dòng Tổng: dư đầu / dư cuối = cộng số RÒNG các dòng rồi tách theo dấu tổng (nhân viên dư Nợ và nhân viên dư Có bù trừ nhau); phát sinh = cộng thẳng.',
    )),
    ('7. Phân quyền cấp', L_(
        '- "' + Q_ALL + '": xem mọi công ty, có ô Công ty.',
        '- "' + Q_CTY + '": xem công ty đang làm việc + công nợ của chính mình.',
        '- Không có quyền nào: mục menu VẪN hiện (giống hệ thống cũ) nhưng không xem / In / Xuất được.',
        '- Bấm mã nhân viên sang Sổ chi tiết cần quyền RIÊNG của Sổ chi tiết: "' + QS_ALL + '" / "' + QS_CTY + '"; không có thì mã nhân viên là chữ thường.',
        '- Quyền gán ở màn Phân quyền, nhóm "Bảng cân đối phát sinh công nợ nhân viên" (và nhóm "Sổ chi tiết công nợ nhân viên").',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Ví dụ NV-A, tài khoản 141, kỳ 01/10/2026 – 31/10/2026: trước kỳ tạm ứng 8,000,000 và hoàn ứng 1,500,000; trong kỳ tạm ứng '
        '5,000,000 và thanh toán tạm ứng 2,300,000:',
        '- Dư đầu kỳ Nợ = 8,000,000 - 1,500,000 = 6,500,000.',
        '- Phát sinh Nợ 5,000,000; Phát sinh Có 2,300,000.',
        '- Dư cuối kỳ Nợ = 6,500,000 + 5,000,000 - 2,300,000 = 9,200,000.',
        'Chân bảng "Hiển thị a–b / N dòng": a, b là dòng đầu / cuối trang đang xem; N = số dòng nhân viên x loại tiền khớp bộ lọc '
        '(KHÔNG đếm dòng Tổng). Mặc định 10 dòng/trang, chọn 10 / 20 / 50 / 100.',
        'Ô "Chỉ tiêu" + "Số tiền từ / đến": lọc trên số VNĐ ĐÃ CỘNG của dòng (Dư nợ đầu kỳ = dư đầu ròng; Dư có đầu kỳ = âm dư đầu ròng; '
        'Phát sinh nợ; Phát sinh có; Dư nợ cuối kỳ = dư cuối ròng; Dư có cuối kỳ = âm dư cuối ròng). Số tiền từ / đến CÒN lọc từng bút '
        'toán theo số VNĐ trước khi cộng (giống hệ thống cũ). Số tiền = 0 coi như bỏ trống.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        'KHÁC BIỆT ĐÃ CHỐT giữa 2 hệ thống (gặp thì ghi "' + CHOT + '"):',
        '- K1. Phạm vi "' + Q_CTY + '": hệ thống mới = nhân viên công ty mình + công nợ CỦA CHÍNH MÌNH (thống nhất với Sổ chi tiết); '
        'hệ thống cũ = nhân viên công ty mình + bút toán của hợp đồng DO MÌNH TẠO.',
        '- K2. Hệ thống mới có In và Xuất Excel; hệ thống cũ không có (2 nút bị ẩn).',
        '- K3. Dòng Tổng ở ĐẦU bảng (hệ thống cũ ở cuối). Phân trang 10 dòng (hệ thống cũ hiện hết 1 trang). Sắp xếp mã nhân viên + loại tiền.',
        '- K4. Số chuẩn 1,234,567.89 (tối đa 2 số lẻ), ô bằng 0 để TRỐNG; hệ thống cũ làm tròn số nguyên và in "-".',
        '- K5. Nhãn: hệ thống mới "VNĐ", "Dư đầu kỳ", "Phát sinh", "Dư cuối kỳ", Mẫu "VNĐ" / "Ngoại tệ", Chỉ tiêu "…cuối kỳ"; hệ thống cũ '
        '"VND", "Số dư đầu kỳ", "Phát sinh trong kỳ", "Số dư cuối kỳ", "Mẫu VNĐ" / "Mẫu Ngoại tệ", "…cuối kì". Câu rỗng: "' + EMPTY + '" '
        '(cũ "Chưa có dữ liệu").',
        '- K6. Chọn ô dạng chọn là tự tải khi đủ Tài khoản + Thời gian; hệ thống cũ phải bấm nút tìm kiếm. Hệ thống mới thêm ô tìm nhanh '
        'mã / tên nhân viên. Thiếu ô bắt buộc: mới báo đỏ "Vui lòng chọn tài khoản" / "Vui lòng chọn thời gian"; cũ "Bắt buộc chọn" + "Chưa chọn đủ điều kiện bắt buộc".',
        '- K7. Không quyền: hệ thống mới vẫn mở màn nhưng báo "' + KHONG_QUYEN + '", ô Tài khoản không có lựa chọn; hệ thống cũ mở trang không tìm thấy.',
        'HỆ THỐNG MỚI SỬA LỖI hệ thống cũ (ghi kết quả đúng theo hệ thống mới; hiện tượng ở hệ thống cũ chỉ để tham chiếu):',
        '- V1. Dòng NGOẠI TỆ: hệ thống mới tính Dư đầu kỳ (nguyên tệ và VNĐ) nên Dư đầu + Phát sinh = Dư cuối; hệ thống cũ để "-" ở cả 2 nhóm '
        'đầu kỳ của dòng ngoại tệ, dòng Tổng ngoại tệ đầu kỳ "-", và lọc Chỉ tiêu "Dư nợ / Dư có đầu kỳ" làm rơi mất dòng ngoại tệ.',
        '- V2. Bấm mã nhân viên ở dòng ngoại tệ: hệ thống mới mở Sổ chi tiết lọc đúng loại tiền của dòng; hệ thống cũ không truyền loại tiền nên ra mọi loại tiền.',
        '- V3. Làm mới đưa Mẫu về VNĐ; hệ thống cũ xoá trắng Mẫu làm bảng nhảy sang hiện cả nhóm Nguyên tệ.',
        '- V4. Người không có quyền không lấy được số liệu bằng bất kỳ cách nào; hệ thống cũ chỉ chặn trang, phần tra cứu số liệu để hở '
        '(nhóm kiểm này dành cho tester kỹ thuật, không viết case).',
        'Lưu ý khác: danh mục Loại tiền đang có 2 mục cùng tên "USD" - chọn đúng mục đã dùng trên phiếu. Ngày lập chứng từ mẫu phải nằm '
        'trong kỳ chưa khoá sổ; nếu kỳ 10/2026 đã khoá thì dời toàn bộ ngày sang kỳ mở và giữ nguyên số tiền. Cột KQ thực tế, DNS check để trống cho tester điền.',
    )),
]

# =============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S_HIEN_THI = [
    C('Mở màn hình từ menu', 'P0', 'TK-ALL đã đăng nhập hệ thống mới.',
      ['Đăng nhập TK-ALL', 'Vào ' + MENU, 'Đọc tiêu đề, các nút, khu vực tìm kiếm và bảng'], '',
      ['Tiêu đề "' + TEN + '", cạnh tiêu đề có biểu tượng chữ i; rê chuột hiện giải thích "Số dư công nợ của từng nhân viên theo từng loại tiền…"',
       'Có 2 nút In, Xuất Excel; khu vực tìm kiếm có ô tìm nhanh, nút Tìm kiếm, Làm mới, Ẩn tìm kiếm nâng cao, Cài đặt bộ lọc',
       'Ô Tài khoản và ô Thời gian có dấu bắt buộc; Mẫu mặc định "VNĐ"',
       'Bảng chưa tải số liệu, hiện "' + NHAC + '"; không có chân bảng phân trang']),
    C('Mở màn hình ở hệ thống cũ cùng tài khoản', 'P1', 'TK-ALL có cùng quyền ở 2 hệ thống.',
      ['Đăng nhập hệ thống cũ bằng TK-ALL', 'Vào ' + E_MENU, 'So các ô lọc với hệ thống mới'], '',
      ['Hệ thống cũ mở cùng tên màn, cùng các ô lọc: Công ty, Phòng ban, Bộ phận, Nhân viên, Tài khoản, ngày bắt đầu / kết thúc, Loại tiền, Mẫu, Chỉ tiêu, Số tiền từ / đến',
       'Hệ thống cũ KHÔNG có nút In / Xuất Excel và ô tìm nhanh: ' + CHOT + ' (K2, K6)']),
    C('Tiêu đề bảng mẫu VNĐ', 'P0', 'Đã chọn ' + LOC + ', Mẫu VNĐ.',
      ['Đọc tiêu đề bảng từ trái sang phải, cả 3 tầng'], 'Mẫu: VNĐ',
      ['Đúng thứ tự: ' + TIEU_DE_VND,
       'Không có nhóm "Nguyên tệ"',
       'Hệ thống cũ ghi "VND", "Số dư đầu kỳ", "Phát sinh trong kỳ", "Số dư cuối kỳ": ' + CHOT + ' (K5)']),
    C('Tiêu đề bảng mẫu Ngoại tệ', 'P0', 'Đang xem mẫu VNĐ với ' + LOC + '.',
      ['Ô Mẫu chọn "Ngoại tệ"', 'Đọc tiêu đề bảng và quan sát biểu tượng tải'], 'Mẫu: Ngoại tệ',
      ['Thêm nhóm "Nguyên tệ" 6 cột (Dư đầu kỳ Nợ / Có, Phát sinh Nợ / Có, Dư cuối kỳ Nợ / Có) đứng TRƯỚC nhóm "VNĐ"',
       'Đổi Mẫu chỉ đổi cột hiển thị, KHÔNG tải lại dữ liệu; tổng N dưới bảng giữ nguyên',
       'Dòng VNĐ: 6 ô nhóm Nguyên tệ để trống']),
    C('Dòng dữ liệu khớp chứng từ đã ghi sổ', 'P0',
      'NV-A đã có 4 Phiếu kế toán ghi sổ như mục 8 (8,000,000 ngày 15/09, 1,500,000 ngày 25/09, 5,000,000 ngày 05/10, 2,300,000 ngày 20/10/2026).',
      ['Chọn ' + LOC, 'Gõ mã NV-A vào ô tìm nhanh, nhấn Enter', 'Đọc dòng của NV-A'],
      ['Tài khoản: ' + TK, 'Thời gian: ' + KY],
      ['1 dòng: Mã, Tên của NV-A, Loại tiền "VNĐ"',
       'Dư đầu kỳ Nợ 6,500,000, Dư đầu kỳ Có trống; Phát sinh Nợ 5,000,000, Phát sinh Có 2,300,000; Dư cuối kỳ Nợ 9,200,000, Dư cuối kỳ Có trống']),
    C('Định dạng số và ô bằng 0', 'P1', 'NV-K có phiếu kế toán USD Nợ 1411 20.5 USD tỷ giá 26,000 ngày 09/10/2026; không có số dư đầu kỳ.',
      ['Chọn ' + LOC + ', Mẫu Ngoại tệ', 'Đọc các ô số của NV-K', 'Mở cùng bộ lọc ở hệ thống cũ'], '',
      ['Nguyên tệ Phát sinh Nợ "20.5"; VNĐ Phát sinh Nợ "533,000" (dấu phẩy ngăn nghìn)',
       'Ô bằng 0 để TRỐNG (không in 0, không in "-")',
       'Hệ thống cũ in "-" và làm tròn "21": ' + CHOT + ' (K4)']),
    C('Nhân viên có 2 loại tiền hiện 2 dòng liền nhau', 'P1',
      'NV-B có phiếu kế toán VNĐ Nợ 1411 1,000,000 ngày 08/10/2026 và các phiếu USD ở nhóm III.',
      ['Chọn ' + LOC + ', Mẫu Ngoại tệ', 'Tìm nhanh mã NV-B'], '',
      ['2 dòng cùng mã NV-B: dòng VNĐ trước, dòng USD sau',
       'Mỗi dòng có STT riêng, số không lẫn sang nhau']),
    C('Nhân viên số dư 0, không phát sinh vẫn hiện', 'P2',
      'NV-G có tạm ứng 3,000,000 và hoàn ứng đủ 3,000,000 trước 01/10/2026, không có bút toán trong kỳ.',
      ['Chọn ' + LOC, 'Tìm nhanh mã NV-G', 'Làm tương tự ở hệ thống cũ'], '',
      ['Vẫn có dòng NV-G, cả 6 ô số để trống',
       'Hệ thống cũ cũng hiện dòng NV-G (các ô "-")']),
    C('Dòng Tổng ở đầu bảng, mỗi loại tiền 1 dòng', 'P0', 'Kết quả lọc có cả dòng VNĐ và dòng USD, nhiều hơn 1 trang.',
      ['Chọn ' + LOC, 'Đọc các dòng đầu bảng', 'Sang trang 2, đọc lại'], '',
      ['Trên cùng là các dòng "Tổng" (in đậm, nền xám), cột Loại tiền ghi VNĐ / USD; KHÔNG có STT, không đếm vào N',
       'Sang trang 2 các dòng Tổng vẫn ở đầu, số KHÔNG đổi (tính trên toàn bộ dòng khớp lọc)',
       'Hệ thống cũ đặt dòng Tổng ở cuối bảng: ' + CHOT + ' (K3)']),
    C('Chưa chọn đủ ô bắt buộc thì không tải', 'P0', 'Vừa mở màn, chưa chọn gì.',
      ['Chỉ chọn Tài khoản = ' + TK, 'Quan sát bảng', 'Chọn thêm Thời gian = ' + KY], '',
      ['Bước 2: bảng vẫn hiện "' + NHAC + '", không tải, không báo lỗi',
       'Bước 3: bảng tự tải ngay (không cần bấm Tìm kiếm), có chân bảng "Hiển thị 1–10 / N dòng"']),
    C('Không có dữ liệu khớp bộ lọc', 'P1', 'Tài khoản 1388 không có bút toán gắn nhân viên trong phạm vi.',
      ['Chọn Tài khoản 1388, Thời gian ' + KY, 'Quan sát bảng'], 'Tài khoản: 1388',
      ['Bảng hiện "' + EMPTY + '", không có dòng Tổng, không có chân bảng phân trang',
       'Nút In, Xuất Excel vẫn hiện; không báo lỗi']),
    C('Phân trang: mặc định, chuyển trang, STT liên tục', 'P0', 'Chọn Tài khoản 33481, Thời gian 01/01/2026 – 31/10/2026 (hơn 30 dòng).',
      ['Đọc chân bảng', 'Bấm › rồi ‹', 'Bấm » rồi «', 'Quan sát STT và trạng thái nút'], 'Tài khoản: 33481',
      ['Mặc định 10 dòng/trang, "Hiển thị 1–10 / N dòng"',
       '› sang trang 2 "Hiển thị 11–20 / N dòng", STT bắt đầu 11; » tới trang cuối, STT dòng cuối = N',
       'Ở trang 1 nút « và ‹ mờ; ở trang cuối nút › và » mờ',
       'Dữ liệu các trang không lặp, không thiếu (cộng số dòng mọi trang = N)']),
    C('Đổi số dòng mỗi trang thì về trang 1', 'P1', 'Đang ở trang 3, 10 dòng/trang.',
      ['Ô "Số dòng/trang" chọn 50', 'Đọc chân bảng'], 'Số dòng/trang: 50',
      ['Ô chọn có 10, 20, 50, 100', 'Về trang 1, hiện tối đa 50 dòng, "Hiển thị 1–50 / N dòng"; N không đổi; dòng Tổng không đổi']),
    C('Thứ tự dòng cố định theo mã nhân viên', 'P1', 'Kết quả có hơn 10 dòng, có nhân viên chưa có hồ sơ (mã trống).',
      ['Đọc cột Mã nhân viên từ trên xuống, qua các trang', 'Bấm tiêu đề cột Mã nhân viên, Tên nhân viên'], '',
      ['Mã nhân viên tăng dần; cùng nhân viên thì VNĐ trước ngoại tệ; dòng mã trống ở cuối danh sách',
       'Bấm tiêu đề không đổi thứ tự (không có sắp xếp theo cột)',
       'Hệ thống cũ thứ tự không cố định: ' + CHOT + ' (K3)']),
    C('Tiêu đề bảng dính khi cuộn', 'P2', 'Chọn 100 dòng/trang.',
      ['Cuộn bảng xuống cuối', 'Cuộn ngang sang nhóm VNĐ (mẫu Ngoại tệ)'], '',
      ['Tiêu đề 3 tầng luôn hiện trên cùng khi cuộn dọc', 'Cuộn ngang trong khung bảng, trang không vỡ bố cục']),
    C('Mở lại màn bằng đường dẫn đã lưu', 'P2', 'Đã lưu dấu trang màn này; đường dẫn có thêm tham số lạ do sửa tay.',
      ['Dán đường dẫn đã lưu lên thanh địa chỉ, Enter', 'Dán đường dẫn đã thêm tham số lạ, Enter'], '',
      ['Cả 2 lần mở đúng màn ở trạng thái mặc định (chưa chọn Tài khoản, Thời gian), không lỗi',
       'Tham số lạ bị bỏ qua, không lọc ngầm, không lộ thêm dữ liệu']),
]

# =============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S_LOC = [
    C('Tìm nhanh theo mã nhân viên', 'P0', 'Đã chọn ' + LOC + '; NV-A có dòng.',
      ['Gõ mã NV-A vào ô tìm nhanh (chưa nhấn gì)', 'Nhấn Enter', 'Gõ một phần mã, bấm Tìm kiếm'], 'Từ khóa: mã NV-A',
      ['Placeholder "Tìm theo mã hoặc tên nhân viên"', 'Đang gõ bảng chưa đổi; nhấn Enter mới lọc',
       'Ra dòng của NV-A (mọi loại tiền); tìm một phần mã ra mọi nhân viên có mã chứa chuỗi',
       'Dòng Tổng tính lại chỉ trên các dòng tìm được']),
    C('Tìm nhanh theo tên, không phân biệt hoa thường', 'P1', 'NV-A tên "Nguyễn Văn An" (ghi tên thật vào Ghi chú).',
      ['Gõ "nguyễn văn" bấm Tìm kiếm', 'Gõ "NGUYỄN VĂN" bấm Tìm kiếm', 'Gõ "   Nguyễn Văn   " bấm Tìm kiếm'],
      ['nguyễn văn', 'NGUYỄN VĂN', '"   Nguyễn Văn   "'],
      ['Cả 3 lần ra CÙNG tập dòng, đều chứa NV-A', 'Khoảng trắng 2 đầu bị bỏ qua']),
    C('Tìm với từ khóa không tồn tại, ký tự đặc biệt, chuỗi dài', 'P2', 'Đã chọn ' + LOC + '.',
      ['Gõ "zzzkhongco999", Enter', 'Gõ "%_\'\\", Enter', 'Dán chuỗi 500 ký tự, Enter'],
      ['zzzkhongco999', '%_\'\\', '"abcde" lặp 100 lần'],
      ['Cả 3 lần: "' + EMPTY + '", không báo lỗi hệ thống, không treo',
       'Ký tự % và _ được tìm đúng nghĩa chữ, không ra toàn bộ danh sách']),
    C('Xóa từ khóa thì danh sách quay lại đầy đủ', 'P1', 'Đang tìm theo mã NV-A; khi chưa tìm có N dòng.',
      ['Xóa hết ô tìm nhanh', 'Nhấn Enter'], '',
      ['Chân bảng quay lại "Hiển thị 1–10 / N dòng", về trang 1, dòng Tổng như trước khi tìm']),
    C('Thiếu Tài khoản hoặc Thời gian khi bấm Tìm kiếm', 'P0', 'Vừa bấm Làm mới; khu vực tìm kiếm nâng cao đang ẩn.',
      ['Bấm Tìm kiếm', 'Chọn Tài khoản = ' + TK, 'Chọn Thời gian = ' + KY], '',
      ['Bước 1: khu vực tìm kiếm nâng cao tự mở; dưới ô Tài khoản báo đỏ "Vui lòng chọn tài khoản", dưới ô Thời gian "Vui lòng chọn thời gian"; bảng không tải',
       'Chọn xong ô nào thì chữ đỏ ô đó tự tắt; đủ 2 ô thì bảng tự tải',
       'Hệ thống cũ báo "Bắt buộc chọn" và "Chưa chọn đủ điều kiện bắt buộc": ' + CHOT + ' (K6)']),
    C('Danh sách Tài khoản chỉ gồm tài khoản theo dõi công nợ', 'P1', 'Đang ở màn hình.',
      ['Mở ô Tài khoản', 'Gõ "141"', 'So danh sách với ô tài khoản của hệ thống cũ'], 'Từ khóa: 141',
      ['Mỗi mục dạng "số hiệu - tên" (vd "' + TK + '", "1411 - Tạm ứng ngắn hạn")',
       'Chỉ có tài khoản theo dõi công nợ đang hoạt động; không có tài khoản đã khóa',
       'Cùng tập tài khoản với hệ thống cũ']),
    C('Tài khoản cha lấy cả tài khoản con trực tiếp', 'P0',
      'NV-A có bút toán ghi sổ trên 1411 (tài khoản con của 141); không có bút toán ghi thẳng 141.',
      ['Chọn ' + LOC + ', tìm nhanh NV-A, ghi số', 'Đổi Tài khoản = 1411, ghi số', 'Làm 2 bước trên ở hệ thống cũ'],
      ['Tài khoản: 141 rồi 1411'],
      ['Chọn 141 và chọn 1411 ra CÙNG số cho NV-A (bút toán 1411 được tính vào 141)',
       '1 nhân viên vẫn chỉ 1 dòng / loại tiền, không tách theo tài khoản con', 'Hệ thống cũ ra cùng số']),
    C('Không lấy tài khoản cháu', 'P0', 'Có nhân viên có bút toán trên 33481 (cháu của 334, con của 3348).',
      ['Chọn Tài khoản 3348, Thời gian 01/01/2026 – 31/10/2026, ghi N và dòng Tổng', 'Đổi Tài khoản = 334, ghi lại', 'So với hệ thống cũ cùng bộ lọc'],
      ['Tài khoản: 3348 rồi 334'],
      ['Chọn 3348: có bút toán 33481 (con trực tiếp)',
       'Chọn 334: KHÔNG tính bút toán 33481 (cháu) - số khác bước 1, có thể "' + EMPTY + '"',
       'Hai hệ thống ra cùng kết quả ở cả 2 lần']),
    C('Lọc theo Loại tiền', 'P1', 'NV-B có dòng VNĐ và dòng USD trên 141 trong kỳ.',
      ['Chọn ' + LOC, 'Ô Loại tiền chọn USD', 'Xóa Loại tiền'], 'Loại tiền: USD',
      ['Chọn là lọc ngay; chỉ còn dòng USD, chỉ còn dòng "Tổng" USD',
       'Xóa Loại tiền thì về đủ các loại tiền',
       'Lưu ý: danh mục có 2 mục "USD" - chọn đúng mục đã dùng trên phiếu, mục còn lại ra rỗng là đúng']),
    C('Đổi Mẫu không lọc dữ liệu', 'P1', 'Đã chọn ' + LOC + ', có cả dòng VNĐ và USD.',
      ['Ghi N và số dòng mỗi loại tiền', 'Đổi Mẫu VNĐ sang Ngoại tệ rồi về VNĐ'], 'Mẫu: Ngoại tệ / VNĐ',
      ['N, các dòng và dòng Tổng không đổi; chỉ thêm / bớt nhóm cột Nguyên tệ',
       'Mẫu VNĐ vẫn hiện dòng USD (số quy đổi VNĐ)']),
    C('Lọc theo Công ty / Phòng ban / Bộ phận', 'P0', 'Đăng nhập TK-ALL. Phòng PB-TEST chỉ có NV-A, NV-E.',
      ['Chọn ' + LOC, 'Ô Công ty chọn TPE', 'Ô Phòng ban chọn PB-TEST', 'Đổi Công ty sang công ty B'], '',
      ['Mỗi ô chọn xong là lọc ngay',
       'Phòng ban = PB-TEST: chỉ còn NV-A, NV-E; dòng Tổng chỉ cộng 2 người',
       'Phòng ban, Bộ phận chỉ liệt kê đơn vị thuộc cấp trên đang chọn; đổi Công ty thì Phòng ban, Bộ phận, Nhân viên tự xóa']),
    C('Lọc theo Nhân viên', 'P1', 'Đang lọc ' + LOC + '.',
      ['Ô Nhân viên chọn NV-A', 'Đổi sang NV-B'], 'Nhân viên: NV-A / NV-B',
      ['Chỉ còn dòng của nhân viên chọn (NV-B có 2 dòng VNĐ, USD)', 'Dòng Tổng bằng đúng số của nhân viên đó']),
    C('Lọc phòng ban theo phòng ghi trên bút toán', 'P1',
      'NV-D chuyển từ phòng P1 sang phòng P2 ngày 01/10/2026; tạm ứng 4,000,000 ngày 20/09 (lúc ở P1) và 2,000,000 ngày 10/10 (ở P2).',
      ['Chọn ' + LOC + ', Phòng ban = P1, tìm NV-D', 'Đổi Phòng ban = P2', 'Bỏ Phòng ban', 'Làm tương tự ở hệ thống cũ'], '',
      ['P1: dòng NV-D chỉ có Dư đầu kỳ Nợ 4,000,000', 'P2: dòng NV-D chỉ có Phát sinh Nợ 2,000,000',
       'Bỏ lọc: 1 dòng NV-D đủ cả 2 bút toán, Dư cuối kỳ Nợ 6,000,000', 'Hệ thống cũ ra cùng số ở cả 3 lần']),
    C('Chỉ tiêu Dư nợ cuối kỳ / Dư có cuối kỳ', 'P0',
      'Đã có số liệu PB-TEST như nhóm III: NV-A Dư cuối kỳ Nợ 9,200,000; NV-E Dư cuối kỳ Có 1,500,000.',
      ['Chọn ' + LOC + ', Phòng ban PB-TEST', 'Chỉ tiêu = "Dư nợ cuối kỳ", Số tiền từ 1,000,000, bấm Tìm kiếm',
       'Đổi Chỉ tiêu = "Dư có cuối kỳ"', 'Làm cùng bộ lọc ở hệ thống cũ'],
      ['Chỉ tiêu: Dư nợ cuối kỳ / Dư có cuối kỳ', 'Số tiền từ: 1,000,000'],
      ['Danh sách Chỉ tiêu: Dư nợ đầu kỳ, Dư có đầu kỳ, Phát sinh nợ, Phát sinh có, Dư nợ cuối kỳ, Dư có cuối kỳ',
       'Dư nợ cuối kỳ từ 1,000,000: chỉ NV-A', 'Dư có cuối kỳ từ 1,000,000: chỉ NV-E',
       'Hệ thống cũ ra cùng nhân viên (nhãn "…cuối kì": ' + CHOT + ' K5)']),
    C('Chỉ tiêu Phát sinh nợ / Phát sinh có với khoảng tiền', 'P1', 'Số liệu PB-TEST như trên (NV-A PS Nợ 5,000,000, PS Có 2,300,000; NV-E PS Nợ 2,000,000, PS Có 3,500,000).',
      ['Phòng ban PB-TEST, Chỉ tiêu "Phát sinh nợ", Số tiền từ 3,000,000, Enter', 'Đổi Chỉ tiêu "Phát sinh có", Số tiền đến 3,000,000, xóa Số tiền từ, Enter'],
      ['Số tiền từ: 3,000,000', 'Số tiền đến: 3,000,000'],
      ['Lần 1: chỉ NV-A (NV-E chỉ còn khoản Có 3,500,000 nên Phát sinh nợ = 0)',
       'Lần 2: cả NV-A (Phát sinh Có 2,300,000) và NV-E: khoản Có 3,500,000 của NV-E bị loại ngay từ bút toán vì lớn hơn 3,000,000, '
       'nên Phát sinh Có của NV-E = 0, vẫn thỏa "không quá 3,000,000"',
       'Lưu ý: Số tiền từ / đến lọc cả TỪNG bút toán lẫn số đã cộng (giống hệ thống cũ) - đối chiếu hệ thống cũ phải ra cùng kết quả']),
    C('Số tiền lọc từng bút toán trước khi cộng', 'P0', 'Số liệu NV-A, NV-E như nhóm III. Chưa chọn Chỉ tiêu.',
      ['Phòng ban PB-TEST, ' + LOC, 'Số tiền từ 3,000,000, bấm Tìm kiếm', 'Đọc dòng NV-A, NV-E', 'Làm cùng ở hệ thống cũ'],
      'Số tiền từ: 3,000,000',
      ['Chỉ bút toán từ 3,000,000 trở lên được cộng:',
       'NV-A: Dư đầu kỳ Nợ 8,000,000 (bỏ khoản hoàn ứng 1,500,000), Phát sinh Nợ 5,000,000, Phát sinh Có trống (bỏ 2,300,000), Dư cuối kỳ Nợ 13,000,000',
       'NV-E: chỉ còn Phát sinh Có 3,500,000, Dư cuối kỳ Có 3,500,000',
       'Hệ thống cũ ra cùng số (giữ đúng cách lọc 2 lớp của hệ thống cũ)']),
    C('Chọn Chỉ tiêu nhưng bỏ trống số tiền, nhập số tiền bằng 0', 'P2', 'Đang lọc PB-TEST.',
      ['Chọn Chỉ tiêu "Dư nợ cuối kỳ", không nhập số tiền', 'Nhập Số tiền từ 0, Enter'], ['Chỉ tiêu: Dư nợ cuối kỳ', 'Số tiền từ: 0'],
      ['Cả 2 lần không lọc gì: vẫn đủ NV-A, NV-E (Số tiền 0 coi như bỏ trống, giống hệ thống cũ)']),
    C('Số tiền từ lớn hơn Số tiền đến', 'P2', 'Đang lọc ' + LOC + '.',
      ['Số tiền từ 5,000,000, Số tiền đến 1,000,000, bấm Tìm kiếm'], ['Số tiền từ: 5,000,000', 'Số tiền đến: 1,000,000'],
      ['Bảng "' + EMPTY + '", không báo lỗi hệ thống', 'Ô Số tiền chỉ nhận số, gõ chữ không được']),
    C('Ô gõ chờ Enter, ô chọn lọc ngay', 'P1', 'Đã chọn ' + LOC + '.',
      ['Gõ Số tiền từ 2,000,000 (chưa Enter), quan sát', 'Chọn Loại tiền VNĐ, quan sát', 'Nhấn Enter ở ô Số tiền'], '',
      ['Gõ Số tiền chưa lọc', 'Chọn Loại tiền lọc ngay, lúc này Số tiền gõ dở CŨNG được áp',
       'Lưu ý: chọn lại 1 ô chọn bất kỳ là áp toàn bộ ô đang có trên khung lọc']),
    C('Lọc kết hợp nhiều điều kiện', 'P0', 'TK-ALL; có dữ liệu PB-TEST.',
      ['Chọn ' + LOC + ', Công ty TPE, Phòng ban PB-TEST, Loại tiền VNĐ, Chỉ tiêu "Dư nợ cuối kỳ", Số tiền từ 1,000,000', 'Bấm Tìm kiếm', 'So với hệ thống cũ cùng điều kiện'], '',
      ['Chỉ còn NV-A, mọi dòng thỏa ĐỒNG THỜI các điều kiện; "Hiển thị 1–1 / 1 dòng"', 'Dòng Tổng VNĐ = đúng số của NV-A',
       'Hệ thống cũ ra cùng nhân viên, cùng số']),
    C('Đổi bộ lọc khi đang ở trang giữa thì về trang 1', 'P1', 'Đang ở trang 3.',
      ['Chọn Loại tiền VNĐ'], '', ['Bảng về trang 1, N cập nhật theo bộ lọc mới']),
    C('Làm mới', 'P0', 'Đang lọc nhiều ô, Mẫu Ngoại tệ, đang có chữ đỏ ở ô bắt buộc.',
      ['Bấm Làm mới', 'Quan sát các ô, bảng', 'Bấm Làm mới ở hệ thống cũ khi Mẫu đang "Mẫu VNĐ"'], '',
      ['Mọi ô lọc và ô tìm nhanh xóa trắng; Mẫu về "VNĐ"; chữ đỏ tắt',
       'Bảng về "' + NHAC + '"',
       'Hệ thống cũ xoá trắng cả Mẫu, bảng hiện thêm nhóm Nguyên tệ: hệ thống mới đã sửa (V3)']),
    C('Ẩn / hiện tìm kiếm nâng cao', 'P2', 'Đang ở màn hình.',
      ['Bấm "Ẩn tìm kiếm nâng cao"', 'Bấm "Tìm kiếm nâng cao"'], '',
      ['Khối ô lọc ẩn đi, nút đổi chữ thành "Tìm kiếm nâng cao"; bấm lại thì hiện, giá trị đã chọn còn nguyên']),
    C('Bộ lọc khi chuyển màn rồi quay lại, khi tải lại trang', 'P1', 'Đang lọc ' + LOC + ', Phòng ban PB-TEST.',
      ['Vào màn khác qua menu rồi quay lại màn này', 'Chọn lại bộ lọc, nhấn F5'], '',
      ['Cả 2 lần màn về trạng thái mặc định (chưa chọn Tài khoản, Thời gian), bảng hiện "' + NHAC + '"',
       'Lưu ý: bấm mã nhân viên mở tab mới nên tab bảng cân đối giữ nguyên bộ lọc']),
]

# =============================================================== III. SỐ LIỆU BÁO CÁO
S_SO_LIEU = [
    C('Ghi số nền trước khi lập chứng từ', 'P0', 'PB-TEST chưa có bút toán 141. TK-ALL ở cả 2 hệ thống.',
      ['Ở hệ thống mới chọn ' + LOC + ', Phòng ban PB-TEST', 'Ở hệ thống cũ chọn cùng điều kiện, bấm tìm kiếm', 'Chụp 2 màn'], '',
      ['Cả 2 hệ thống: "' + EMPTY + '" (cũ "Chưa có dữ liệu")', 'Ghi lại dòng Tổng VNĐ của toàn tài khoản 141 (bỏ lọc Phòng ban) làm số nền']),
    C('Tạm ứng trước kỳ vào Dư đầu kỳ Nợ', 'P0', 'Có số nền.',
      ['TK-KT vào ' + PKT + ', lập phiếu ngày hạch toán 15/09/2026: Nợ 1411 (đối tượng Nhân viên NV-A) / Có 1111, 8,000,000; ' + DUYET,
       'Mở lại bảng cân đối ' + LOC + ', PB-TEST, ở cả 2 hệ thống'],
      ['Ngày hạch toán: 15/09/2026', 'Số tiền: 8,000,000'],
      ['Có dòng NV-A VNĐ: Dư đầu kỳ Nợ 8,000,000; Phát sinh trống; Dư cuối kỳ Nợ 8,000,000',
       'Bút toán trước "Từ ngày" vẫn được tính (vào đầu kỳ)', 'Hệ thống cũ ra cùng số']),
    C('Hoàn ứng trước kỳ làm giảm Dư đầu kỳ', 'P0', 'Đã làm TC trước.',
      ['Lập phiếu kế toán ngày 25/09/2026: Nợ 1111 / Có 1411 (NV-A), 1,500,000; ' + DUYET, 'Mở lại bảng ở 2 hệ thống'],
      'Số tiền: 1,500,000',
      ['NV-A: Dư đầu kỳ Nợ 6,500,000 (= 8,000,000 - 1,500,000), Dư cuối kỳ Nợ 6,500,000', 'Hai hệ thống cùng số']),
    C('Tạm ứng trong kỳ vào Phát sinh Nợ', 'P0', 'Đã làm TC trước.',
      ['Lập phiếu kế toán ngày 05/10/2026: Nợ 1411 (NV-A) / Có 1111, 5,000,000; ' + DUYET, 'Mở lại bảng ở 2 hệ thống'],
      'Số tiền: 5,000,000',
      ['NV-A: Dư đầu kỳ Nợ 6,500,000 (không đổi); Phát sinh Nợ 5,000,000; Dư cuối kỳ Nợ 11,500,000',
       'Dòng Tổng VNĐ của tài khoản 141: Phát sinh Nợ tăng đúng 5,000,000 so với số nền', 'Hai hệ thống cùng số']),
    C('Thanh toán tạm ứng trong kỳ vào Phát sinh Có', 'P0', 'Đã làm TC trước.',
      ['Lập phiếu kế toán ngày 20/10/2026: Nợ 6422 / Có 1411 (NV-A), 2,300,000; ' + DUYET, 'Mở lại bảng ở 2 hệ thống'],
      'Số tiền: 2,300,000',
      ['NV-A: Phát sinh Có 2,300,000; Dư cuối kỳ Nợ 9,200,000 (= 6,500,000 + 5,000,000 - 2,300,000)',
       'Dư đầu kỳ + Phát sinh Nợ - Phát sinh Có = Dư cuối kỳ', 'Hai hệ thống cùng số']),
    C('Bút toán đúng ngày Từ ngày / Đến ngày', 'P1', 'NV-F chưa có bút toán 141.',
      ['Lập 2 phiếu kế toán Nợ 1411 (NV-F): 1,000,000 ngày 01/10/2026 và 2,000,000 ngày 31/10/2026; ' + DUYET, 'Mở bảng ' + LOC + ', tìm NV-F'],
      ['01/10/2026: 1,000,000', '31/10/2026: 2,000,000'],
      ['Cả 2 vào Phát sinh Nợ = 3,000,000 (tính cả 2 đầu mút, kể cả bút toán cuối ngày 31/10)', 'Dư đầu kỳ trống']),
    C('Chứng từ sau Đến ngày không lên', 'P0', 'NV-A Dư cuối kỳ Nợ 9,200,000 như trên.',
      ['Lập phiếu kế toán ngày 05/11/2026: Nợ 1111 / Có 1411 (NV-A), 3,000,000; ' + DUYET, 'Mở lại bảng kỳ ' + KY + ' ở 2 hệ thống'],
      'Ngày hạch toán: 05/11/2026',
      ['Dòng NV-A KHÔNG đổi: đầu kỳ 6,500,000, PS Nợ 5,000,000, PS Có 2,300,000, cuối kỳ Nợ 9,200,000', 'Hai hệ thống cùng số']),
    C('Đổi kỳ: phát sinh kỳ trước chuyển vào Dư đầu kỳ', 'P0', 'Đã làm TC trước.',
      ['Đổi Thời gian = 01/11/2026 – 30/11/2026', 'Đọc dòng NV-A ở 2 hệ thống'], 'Thời gian: 01/11/2026 – 30/11/2026',
      ['Dư đầu kỳ Nợ 9,200,000 (= cuối kỳ tháng 10)', 'Phát sinh Có 3,000,000; Phát sinh Nợ trống',
       'Dư cuối kỳ Nợ 6,200,000', 'Hai hệ thống cùng số']),
    C('Kỳ dài gộp mọi phát sinh', 'P1', 'Đã làm các TC trên.',
      ['Đổi Thời gian = 01/09/2026 – 30/11/2026', 'Đọc dòng NV-A'], 'Thời gian: 01/09/2026 – 30/11/2026',
      ['Dư đầu kỳ trống; Phát sinh Nợ 13,000,000 (8,000,000 + 5,000,000); Phát sinh Có 6,800,000 (1,500,000 + 2,300,000 + 3,000,000)',
       'Dư cuối kỳ Nợ 6,200,000 - bằng cuối kỳ của TC trước']),
    C('Phiếu kế toán Lưu nháp không lên bảng', 'P0', 'NV-A Dư cuối kỳ Nợ 9,200,000 (kỳ ' + KY + ').',
      ['Lập phiếu kế toán ngày 12/10/2026 Nợ 1411 (NV-A) 7,000,000, chỉ bấm "Lưu nháp"', 'Mở lại bảng kỳ ' + KY + ' ở 2 hệ thống',
       'Xóa phiếu nháp đó'], 'Số tiền: 7,000,000',
      ['Bước 2: dòng NV-A KHÔNG đổi (chưa ghi sổ)', 'Bước 3: vẫn không đổi']),
    C('Phiếu chi chờ duyệt / đã Hủy phiếu không lên bảng', 'P1', 'Có đề nghị thanh toán tạm ứng cho NV-A 2,000,000.',
      ['Vào phân hệ Tài chính > Quản lý tiền > nhóm "Thanh toán tiền mặt" > "Phiếu chi", lập phiếu chi tạm ứng NV-A 2,000,000 ngày 15/10/2026, để chờ duyệt',
       'Mở bảng cân đối', 'Bấm "Hủy phiếu" phiếu chi đó, mở lại bảng'], 'Số tiền: 2,000,000',
      ['Cả 2 lần dòng NV-A không đổi', 'Chỉ khi phiếu chi được duyệt hạch toán thì Phát sinh Nợ mới tăng 2,000,000 (ghi Ghi chú nếu thử nhánh này)']),
    C('Dư cuối kỳ âm chuyển sang cột Có', 'P0', 'NV-E chưa có bút toán 141.',
      ['Lập phiếu kế toán ngày 01/10/2026 Nợ 1411 (NV-E) 2,000,000; ' + DUYET,
       'Lập phiếu kế toán ngày 15/10/2026 Nợ 1111 / Có 1411 (NV-E) 3,500,000 (nhân viên nộp lại thừa); ' + DUYET, 'Mở bảng ' + LOC + ' ở 2 hệ thống'],
      ['Nợ 2,000,000', 'Có 3,500,000'],
      ['NV-E: Dư đầu kỳ trống; Phát sinh Nợ 2,000,000, Phát sinh Có 3,500,000',
       'Dư cuối kỳ Có 1,500,000, Dư cuối kỳ Nợ TRỐNG (số âm hiện bằng giá trị tuyệt đối ở cột Có)', 'Hai hệ thống cùng số']),
    C('Dư đầu kỳ âm hiện cột Có', 'P1', 'Đã làm TC trước.',
      ['Đổi Thời gian = 01/11/2026 – 30/11/2026, tìm NV-E'], '',
      ['NV-E: Dư đầu kỳ Có 1,500,000, Dư đầu kỳ Nợ trống; Dư cuối kỳ Có 1,500,000']),
    C('Dòng Tổng bù trừ nhân viên dư Nợ và dư Có', 'P0', 'PB-TEST: NV-A Dư cuối kỳ Nợ 9,200,000, NV-E Dư cuối kỳ Có 1,500,000 (kỳ ' + KY + ').',
      ['Chọn ' + LOC + ', Phòng ban PB-TEST', 'Đọc dòng "Tổng" VNĐ ở 2 hệ thống'], '',
      ['Tổng: Dư đầu kỳ Nợ 6,500,000; Phát sinh Nợ 7,000,000; Phát sinh Có 5,800,000',
       'Dư cuối kỳ Nợ 7,700,000 (= 9,200,000 - 1,500,000), Dư cuối kỳ Có TRỐNG - dư được bù trừ, KHÔNG hiện riêng 9,200,000 Nợ và 1,500,000 Có',
       'Hai hệ thống cùng số (vị trí dòng Tổng khác: ' + CHOT + ' K3)']),
    C('Dòng Tổng tính trên toàn bộ, không theo trang', 'P1', 'Kết quả hơn 10 dòng, chỉ có VNĐ.',
      ['Chọn 10 dòng/trang, ghi dòng Tổng', 'Chọn 100 dòng/trang, cộng tay cột Phát sinh Nợ mọi dòng'], '',
      ['Dòng Tổng giữ nguyên khi đổi số dòng/trang', 'Phát sinh Nợ của Tổng = cộng tay Phát sinh Nợ mọi dòng']),
    C('Đảo chứng từ bằng bút toán ngược thì số dư trở lại', 'P0',
      'NV-H chưa có bút toán 141; đã lập và duyệt phiếu kế toán ngày 05/10/2026 Nợ 1411 (NV-H) / Có 1111, 5,000,000 (lập nhầm).',
      ['Mở bảng ' + LOC + ', tìm NV-H, ghi số',
       'Lập phiếu kế toán ngày 06/10/2026 đảo khoản trên: Nợ 1111 / Có 1411 (NV-H), 5,000,000; ' + DUYET, 'Mở lại bảng ở 2 hệ thống'],
      'Số tiền: 5,000,000',
      ['Bước 1: NV-H Phát sinh Nợ 5,000,000, Dư cuối kỳ Nợ 5,000,000',
       'Bước 3: Phát sinh Nợ VẪN 5,000,000; Phát sinh Có 5,000,000; Dư cuối kỳ Nợ và Có đều TRỐNG (số dư trở về 0, dòng vẫn hiện)',
       'Lưu ý: bút toán đảo làm tăng cả 2 cột phát sinh, chỉ SỐ DƯ trở lại - không phải lỗi', 'Hai hệ thống cùng số']),
    C('Dòng ngoại tệ: số nguyên tệ và VNĐ', 'P0', 'NV-B chưa có bút toán 141 bằng USD.',
      ['Lập phiếu kế toán Loại tiền USD, ngày 20/09/2026, tỷ giá 25,500: Nợ 1411 (NV-B) 100 USD; ' + DUYET,
       'Lập phiếu USD ngày 12/10/2026, tỷ giá 26,000: Nợ 1411 (NV-B) 200 USD; ' + DUYET,
       'Lập phiếu USD ngày 28/10/2026, tỷ giá 26,100: Có 1411 (NV-B) 50 USD; ' + DUYET,
       'Mở bảng ' + LOC + ', Mẫu Ngoại tệ, tìm NV-B'],
      ['100 USD x 25,500 = 2,550,000', '200 USD x 26,000 = 5,200,000', '50 USD x 26,100 = 1,305,000'],
      ['Dòng NV-B Loại tiền USD:',
       'Nguyên tệ: Dư đầu kỳ Nợ 100; Phát sinh Nợ 200, Có 50; Dư cuối kỳ Nợ 250',
       'VNĐ: Dư đầu kỳ Nợ 2,550,000; Phát sinh Nợ 5,200,000, Có 1,305,000; Dư cuối kỳ Nợ 6,445,000',
       'Dư đầu + Phát sinh Nợ - Phát sinh Có = Dư cuối ở cả 2 nhóm']),
    C('Dòng ngoại tệ ở hệ thống cũ thiếu số đầu kỳ', 'P1', 'Đã làm TC trước.',
      ['Mở hệ thống cũ cùng bộ lọc, Mẫu Ngoại tệ, đọc dòng NV-B USD và dòng Tổng USD'], '',
      ['Hệ thống cũ: 2 ô Dư đầu kỳ (Nguyên tệ và VND) hiện "-"; Dư cuối kỳ vẫn 250 / 6,445,000 nên đầu + phát sinh KHÁC cuối',
       'Dòng Tổng USD ở hệ thống cũ cũng "-" ở đầu kỳ',
       'Hệ thống mới đã sửa (V1): ghi kết quả đúng theo TC trước; phát sinh và dư cuối 2 bên phải bằng nhau']),
    C('Dòng Tổng ngoại tệ', 'P1', 'Trong kỳ chỉ NV-B có bút toán USD trên 141.',
      ['Chọn ' + LOC + ', Mẫu Ngoại tệ, đọc dòng "Tổng" USD', 'Đổi Mẫu VNĐ, đọc lại'], '',
      ['Mẫu Ngoại tệ: Tổng USD có đủ nhóm Nguyên tệ (100 / 200 / 50 / 250) và nhóm VNĐ (2,550,000 / 5,200,000 / 1,305,000 / 6,445,000)',
       'Mẫu VNĐ: Tổng USD chỉ còn nhóm VNĐ, cùng số',
       'Dòng Tổng VNĐ: nhóm Nguyên tệ để trống']),
    C('Bút toán không gắn nhân viên không tính', 'P1', 'Có phiếu kế toán ngày 10/10/2026 ghi Nợ 1411 3,000,000 KHÔNG chọn đối tượng nhân viên.',
      ['Ghi dòng Tổng VNĐ trước khi duyệt phiếu', 'Duyệt phiếu, mở lại bảng ' + LOC], '',
      ['Dòng Tổng và mọi dòng nhân viên KHÔNG đổi']),
    C('Phát sinh từ các loại chứng từ khác cũng lên bảng', 'P1',
      'Tài khoản 33481 có bút toán từ Phiếu chi thu nhập nhân viên và Phiếu ủy nhiệm chi; 1411 có bút toán từ hạch toán chuyến xe.',
      ['Chọn Tài khoản 3348, Thời gian 01/07/2026 – 31/07/2026, đọc 3 nhân viên bất kỳ', 'Chọn Tài khoản 141 cùng kỳ, đọc 3 nhân viên',
       'So từng dòng với hệ thống cũ'], '',
      ['Mọi dòng 2 hệ thống cùng Dư đầu kỳ, Phát sinh Nợ / Có, Dư cuối kỳ (VNĐ)', 'Dòng Tổng VNĐ 2 bên bằng nhau']),
    C('Đối chiếu toàn bảng 2 hệ thống', 'P0', 'TK-ALL; cùng bộ lọc 2 bên, chỉ VNĐ.',
      ['Ở 2 hệ thống chọn Tài khoản 33481, Thời gian 01/01/2026 – 31/10/2026, Mẫu VNĐ',
       'Hệ thống mới chọn 100 dòng/trang, so từng dòng với hệ thống cũ theo mã nhân viên', 'So dòng Tổng VNĐ'], '',
      ['Cùng số nhân viên (N bằng số dòng hệ thống cũ)', 'Từng nhân viên cùng 6 ô số VNĐ (hệ thống cũ làm tròn số nguyên: ' + CHOT + ' K4)',
       'Dòng Tổng cùng số', 'Lệch thì kiểm quyền / phạm vi 2 bên trước khi ghi lỗi']),
    C('Đối chiếu phạm vi công ty 2 hệ thống', 'P1', 'TK-CTY (công ty TPE) có cùng quyền 2 bên.',
      ['Đăng nhập TK-CTY ở 2 hệ thống, chọn Tài khoản 33481, Thời gian 01/01/2026 – 31/10/2026', 'So danh sách nhân viên'], '',
      ['Nhân viên công ty TPE: 2 bên cùng số',
       'Có thể lệch vài dòng: hệ thống mới có thêm công nợ của chính TK-CTY; hệ thống cũ có thêm bút toán của hợp đồng do TK-CTY tạo: ' + CHOT + ' (K1)']),
    C('Kỳ dài, tài khoản nhiều bút toán không treo', 'P1', 'Tài khoản 35241 có hơn 200,000 bút toán gắn nhân viên.',
      ['Chọn Tài khoản 35241, Thời gian 01/01/2025 – 31/10/2026', 'Đo thời gian tới khi bảng hiện', 'Chuyển trang 2, 3'], '',
      ['Bảng hiện trong vài giây, không báo lỗi máy chủ, không treo trình duyệt', 'Chuyển trang nhanh, dòng Tổng không đổi']),
]

# =============================================================== IV. XEM CHI TIẾT (bấm mã nhân viên sang Sổ chi tiết)
S_CT = [
    C('Bấm mã nhân viên mở Sổ chi tiết đúng bộ lọc', 'P0', 'TK-ALL; NV-A kỳ ' + KY + ': đầu kỳ Nợ 6,500,000, PS Nợ 5,000,000, PS Có 2,300,000, cuối kỳ Nợ 9,200,000.',
      ['Chọn ' + LOC + ', tìm NV-A', 'Bấm vào mã NV-A'], '',
      ['Mở TAB MỚI màn "Sổ chi tiết công nợ nhân viên", tự tải ngay',
       'Ô lọc đã điền: Tài khoản ' + TK + ', Thời gian ' + KY + ', Nhân viên NV-A, Loại tiền VNĐ, Mẫu VNĐ',
       'Sổ chi tiết: Số dư đầu kỳ Nợ 6,500,000; Tổng phát sinh Nợ 5,000,000, Có 2,300,000; Số dư cuối kỳ Nợ 9,200,000',
       'Có đúng 2 dòng chứng từ (phiếu ngày 05/10 và 20/10/2026)']),
    C('Số dư cuối kỳ khớp Sổ chi tiết với nhân viên dư Có', 'P0', 'NV-E Dư cuối kỳ Có 1,500,000.',
      ['Bấm mã NV-E'], '', ['Sổ chi tiết: Số dư cuối kỳ Có 1,500,000, bằng dòng NV-E trên bảng cân đối']),
    C('Dòng ngoại tệ mở Sổ chi tiết đúng loại tiền', 'P0', 'NV-B có 2 dòng VNĐ và USD.',
      ['Mẫu Ngoại tệ, bấm mã NV-B ở dòng USD', 'Quay lại, bấm mã NV-B ở dòng VNĐ', 'Làm tương tự ở hệ thống cũ'], '',
      ['Dòng USD: Sổ chi tiết lọc Loại tiền USD, Mẫu Ngoại tệ; Số dư cuối kỳ (VNĐ) 6,445,000 = dòng USD',
       'Dòng VNĐ: Sổ chi tiết lọc Loại tiền VNĐ, cuối kỳ bằng dòng VNĐ',
       'Hệ thống cũ mở Sổ chi tiết không lọc loại tiền (ra tổng mọi loại tiền): hệ thống mới đã sửa (V2)']),
    C('Bộ lọc phạm vi và số tiền được mang sang', 'P1', 'TK-ALL.',
      ['Chọn ' + LOC + ', Công ty TPE, Phòng ban PB-TEST, Số tiền từ 3,000,000, bấm Tìm kiếm', 'Bấm mã NV-A'], 'Số tiền từ: 3,000,000',
      ['Sổ chi tiết có Công ty TPE, Phòng ban PB-TEST, Số tiền từ 3,000,000',
       'Số dư cuối kỳ Nợ 13,000,000 - bằng dòng NV-A khi đang lọc số tiền']),
    C('Ô Số tiền gõ dở chưa áp không lọt sang Sổ chi tiết', 'P1', 'Đã tải bảng ' + LOC + ', không lọc số tiền.',
      ['Gõ Số tiền từ 3,000,000 nhưng KHÔNG nhấn Enter / Tìm kiếm', 'Bấm mã NV-A'], '',
      ['Sổ chi tiết KHÔNG có Số tiền từ; số dư cuối kỳ Nợ 9,200,000, đúng dòng đang hiện trên bảng']),
    C('Không có quyền Sổ chi tiết thì mã nhân viên là chữ thường', 'P0', 'TK-BC chỉ có "' + Q_ALL + '".',
      ['Đăng nhập TK-BC, chọn ' + LOC, 'Rê chuột và bấm vào mã nhân viên'], 'Tài khoản TK-BC',
      ['Mã nhân viên là chữ thường, không gạch chân, bấm không mở gì', 'Số liệu bảng cân đối vẫn xem đầy đủ']),
    C('Quyền 2 màn khác cấp', 'P2', 'TK-X có "' + Q_ALL + '" nhưng Sổ chi tiết chỉ có "' + QS_CTY + '" (công ty TPE).',
      ['Đăng nhập TK-X, chọn ' + LOC, 'Bấm mã NV-C (công ty B)'], '',
      ['Sổ chi tiết mở nhưng KHÔNG có bút toán của NV-C (ngoài phạm vi Sổ chi tiết) - số không khớp dòng bảng cân đối',
       'Giống hệ thống cũ (2 bộ quyền riêng): ' + CHOT]),
    C('Bấm lại mã nhân viên khi Sổ chi tiết đã lưu bộ lọc khác', 'P2', 'Tab Sổ chi tiết vừa lọc Nhân viên NV-E 5 phút trước.',
      ['Ở bảng cân đối bấm mã NV-A'], '',
      ['Tab mới chỉ dùng bộ lọc mang từ bảng cân đối (NV-A), không dính ô cũ của lần lọc trước']),
]

# =============================================================== V. XUẤT DANH SÁCH EXCEL
S_XUAT = [
    C('Xuất Excel mẫu VNĐ', 'P0', 'Đang xem ' + LOC + ', Phòng ban PB-TEST, Mẫu VNĐ.',
      ['Bấm Xuất Excel', 'Mở file tải về'], '',
      ['Cạnh nút hiện tiến độ "Đang chuẩn bị dữ liệu…"; xong báo "Xuất Excel thành công"',
       'File "bang_can_doi_phat_sinh_cong_no_nhan_vien.xlsx", tiêu đề "BẢNG CÂN ĐỐI PHÁT SINH CÔNG NỢ NHÂN VIÊN (TỪ NGÀY 01/10/2026 ĐẾN NGÀY 31/10/2026)"',
       'Cột: STT, Mã nhân viên, Tên nhân viên, Loại tiền, VNĐ - Dư đầu kỳ Nợ, VNĐ - Dư đầu kỳ Có, VNĐ - Phát sinh Nợ, VNĐ - Phát sinh Có, VNĐ - Dư cuối kỳ Nợ, VNĐ - Dư cuối kỳ Có',
       'Dòng Tổng ở đầu (cột Tên nhân viên ghi "Tổng"), rồi NV-A, NV-E; số trùng màn hình']),
    C('Xuất Excel mẫu Ngoại tệ', 'P1', 'Đang xem ' + LOC + ', Mẫu Ngoại tệ (đã tải lại sau khi chọn Mẫu), có dòng USD của NV-B.',
      ['Bấm Xuất Excel', 'Mở file'], '',
      ['Thêm 6 cột "Nguyên tệ - Dư đầu kỳ Nợ" … "Nguyên tệ - Dư cuối kỳ Có" TRƯỚC 6 cột VNĐ',
       'Dòng NV-B USD: nhóm Nguyên tệ 100 / 200 / 50 / 250; dòng VNĐ: nhóm Nguyên tệ trống']),
    C('Excel đúng bộ lọc đang áp, kể cả tìm nhanh', 'P0', 'Đã tìm nhanh mã NV-A và lọc Loại tiền VNĐ.',
      ['Bấm Xuất Excel', 'So file với màn'], '',
      ['File chỉ có dòng Tổng + dòng NV-A, đúng số trên màn', 'Không có nhân viên ngoài bộ lọc / ngoài phạm vi quyền']),
    C('Ô số trong Excel là số, ô 0 để trống', 'P1', 'File vừa xuất.',
      ['Bấm vào ô Dư cuối kỳ Nợ của NV-A', 'Chọn cả cột Phát sinh Nợ, xem tổng ở thanh trạng thái Excel'], '',
      ['Ô là SỐ (9200000), cộng được; không phải chữ', 'Ô bằng 0 để trống', 'Tổng cột (trừ dòng Tổng) bằng ô Phát sinh Nợ của dòng Tổng']),
    C('Xuất khi thiếu Tài khoản / Thời gian', 'P0', 'Vừa bấm Làm mới.',
      ['Bấm Xuất Excel'], '',
      ['Báo "Vui lòng chọn tài khoản và thời gian"; ô bắt buộc báo đỏ, khung lọc mở; không tải file']),
    C('Xuất khi không có dữ liệu', 'P2', 'Đã chọn Tài khoản 1388, Thời gian ' + KY + ' (bảng rỗng).',
      ['Bấm Xuất Excel'], '', ['Báo "Không có dữ liệu để xuất", không tải file rỗng']),
    C('Xuất nhiều dòng, bấm 2 lần liên tiếp', 'P2', 'Tài khoản 33481, Thời gian 01/01/2025 – 31/10/2026 (hơn 150 dòng).',
      ['Bấm Xuất Excel 2 lần thật nhanh'], '',
      ['Chỉ tải 1 file; trong lúc xuất nút mờ, hiện tiến độ "Đã tải x/y dòng…"', 'Số dòng file = N + số dòng Tổng']),
    C('Hệ thống cũ không có Xuất Excel', 'P2', 'Mở màn ở hệ thống cũ.',
      ['Tìm nút Xuất Excel'], '', ['Không có nút: ' + CHOT + ' (K2); đối chiếu số Excel hệ thống mới với màn hệ thống cũ thay thế']),
]

# =============================================================== VI. IN BÁO CÁO
S_IN = [
    C('In bảng cân đối mẫu VNĐ', 'P0', 'TK-ALL công ty TPE; đang xem ' + LOC + ', Phòng ban PB-TEST.',
      ['Bấm In', 'Đọc bản xem trước'], '',
      ['Mở popup "Xem trước bảng cân đối phát sinh công nợ nhân viên", khổ ngang',
       'Đầu trang có tiêu đề in sẵn của công ty người xem; tiêu đề "BẢNG CÂN ĐỐI PHÁT SINH CÔNG NỢ NHÂN VIÊN"',
       'Dòng thông tin: Công ty: Tất cả; Phòng ban: PB-TEST; Tài khoản: ' + TK + '; Mẫu: VNĐ; Từ ngày: 01/10/2026; Đến ngày: 31/10/2026',
       'Bảng tiêu đề 2 tầng (nhóm VNĐ: Dư đầu kỳ Nợ … Dư cuối kỳ Có), dòng Tổng in đậm ở đầu, rồi NV-A, NV-E đúng số màn hình',
       'Cuối trang: "Ngày … tháng … năm …", 2 ô ký Người lập, Kế toán trưởng (Ký, họ tên)']),
    C('In mẫu Ngoại tệ', 'P1', 'Đã chọn Mẫu Ngoại tệ rồi bấm Tìm kiếm; có dòng USD.',
      ['Bấm In'], '',
      ['Dòng thông tin "Mẫu: Ngoại tệ"; bảng có nhóm Nguyên tệ trước VNĐ', 'Dòng USD của NV-B đúng 100 / 200 / 50 / 250 và số VNĐ']),
    C('Đổi Mẫu sau khi tải rồi In / Xuất ngay', 'P1', 'Đã tải bảng mẫu VNĐ.',
      ['Đổi Mẫu sang Ngoại tệ (không bấm Tìm kiếm)', 'Bấm In', 'Bấm Xuất Excel'], 'Mẫu: Ngoại tệ',
      ['Bản in và file Excel theo Mẫu ĐANG HIỆN trên màn (có nhóm Nguyên tệ), dòng thông tin ghi "Mẫu: Ngoại tệ"',
       'Lưu ý: nếu bản in / file vẫn ra mẫu VNĐ thì ghi Failed, kèm ảnh màn và bản in']),
    C('In đúng bộ lọc đang áp, kể cả tìm nhanh', 'P0', 'Đã tìm nhanh mã NV-A.',
      ['Bấm In'], '', ['Bản in chỉ có dòng Tổng và NV-A; số bằng màn hình']),
    C('In khi thiếu Tài khoản / Thời gian', 'P0', 'Vừa bấm Làm mới.',
      ['Bấm In'], '', ['Báo "Vui lòng chọn tài khoản và thời gian"; ô bắt buộc báo đỏ; không mở popup']),
    C('In khi không có dữ liệu', 'P2', 'Đã chọn Tài khoản 1388, Thời gian ' + KY + '.',
      ['Bấm In'], '',
      ['Không báo lỗi hệ thống; popup có tiêu đề và bảng không có dòng nhân viên',
       'Lưu ý: ghi Ghi chú nếu nghiệp vụ muốn báo "Không có dữ liệu để in" thay vì in bảng rỗng']),
    C('Vượt trần 2,000 dòng thì không in', 'P2', 'Môi trường có bộ lọc ra hơn 2,000 dòng nhân viên x loại tiền (khó dựng trên dữ liệu hiện tại - bỏ qua nếu không có).',
      ['Bấm In'], '',
      ['Popup hiện "Danh sách có … dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc…"; không có nút in']),
    C('Hệ thống cũ không có In', 'P2', 'Mở màn ở hệ thống cũ.',
      ['Tìm nút In'], '', ['Không có nút: ' + CHOT + ' (K2)']),
]

# =============================================================== VII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S_RB = [
    C('Số dư cuối kỳ từng nhân viên bằng Sổ chi tiết cùng kỳ', 'P0', 'TK-ALL; Tài khoản 33481, Thời gian 01/07/2026 – 31/07/2026.',
      ['Chọn 3 nhân viên bất kỳ trên bảng cân đối, ghi Dư cuối kỳ', 'Mở ' + SCT + ' (từ menu), lọc cùng Tài khoản, Thời gian, Nhân viên, Loại tiền VNĐ'], '',
      ['Mỗi nhân viên: Số dư cuối kỳ Sổ chi tiết = Dư cuối kỳ bảng cân đối; Số dư đầu kỳ cũng bằng nhau',
       'Tổng phát sinh Nợ / Có Sổ chi tiết = Phát sinh Nợ / Có của dòng']),
    C('Tổng 3 số của cả tài khoản bằng Sổ chi tiết', 'P0', 'TK-ALL; Tài khoản 141, Thời gian 01/01/2026 – 31/10/2026, chỉ có VNĐ.',
      ['Ghi dòng Tổng VNĐ của bảng cân đối', 'Mở Sổ chi tiết cùng Tài khoản, Thời gian, không lọc nhân viên, đọc 3 dòng tổng'], '',
      ['Số dư đầu kỳ, Tổng phát sinh Nợ / Có, Số dư cuối kỳ của Sổ chi tiết = dòng Tổng bảng cân đối (số ròng)']),
    C('Chứng từ mới lập hiện ngay ở cả 2 màn và 2 hệ thống', 'P0', 'NV-F kỳ ' + KY + ' có Phát sinh Nợ 3,000,000.',
      ['Ở HỆ THỐNG CŨ lập phiếu kế toán ngày 18/10/2026 Nợ 1111 / Có 1411 (NV-F) 1,200,000, duyệt', 'Tải lại bảng cân đối hệ thống mới', 'Bấm mã NV-F'],
      'Số tiền: 1,200,000',
      ['Bảng cân đối hệ thống mới: NV-F Phát sinh Có 1,200,000, Dư cuối kỳ Nợ 1,800,000 (không cần chờ đồng bộ)',
       'Sổ chi tiết có thêm dòng chứng từ 18/10/2026, cuối kỳ 1,800,000']),
    C('Đổi phòng ban nhân viên không đổi số đã ghi sổ', 'P1', 'NV-A đang ở PB-TEST, có số liệu tháng 10.',
      ['Ở màn hồ sơ nhân sự chuyển NV-A sang phòng P2 từ 01/11/2026', 'Mở bảng cân đối kỳ ' + KY + ', Phòng ban PB-TEST'], '',
      ['NV-A vẫn nằm trong PB-TEST với đủ số tháng 10 (lọc theo phòng ghi trên bút toán)', 'Chuyển phòng xong rồi trả lại như cũ sau TC']),
    C('Tài khoản bị khóa', 'P2', 'Có tài khoản theo dõi công nợ đang có bút toán nhân viên, quản trị khóa tài khoản đó trong danh mục.',
      ['Mở lại màn, mở ô Tài khoản'], '',
      ['Tài khoản đã khóa không còn trong danh sách chọn', 'Mở lại tài khoản sau TC']),
    C('Hai người cùng xem khi có người lập chứng từ', 'P2',
      'TK-ALL đang mở bảng ' + LOC + ' (hơn 1 trang); TK-KT duyệt thêm phiếu kế toán Nợ 1411 (NV-F) 1,000,000 ngày 22/10/2026.',
      ['TK-ALL chuyển trang rồi quay lại trang 1', 'TK-ALL bấm Tìm kiếm'], '',
      ['Chuyển trang: dòng Tổng giữ số cũ (chỉ tải lại dòng của trang)',
       'Bấm Tìm kiếm: dòng NV-F Phát sinh Nợ và dòng Tổng VNĐ Phát sinh Nợ cùng tăng 1,000,000']),
    C('Màn chỉ xem, không thay đổi dữ liệu', 'P1', 'Đang ở màn.',
      ['Tìm nút Thêm / Sửa / Xóa trên màn và trên từng dòng'], '',
      ['Không có thao tác thêm / sửa / xóa; In, Xuất, bấm mã nhân viên không làm đổi số liệu nơi khác']),
]

# =============================================================== VIII. PHÂN QUYỀN
S_PQ = [
    C('Không có quyền nào', 'P0', 'TK-Z không có "' + Q_ALL + '" và "' + Q_CTY + '".',
      ['Đăng nhập TK-Z, mở phân hệ Tài chính > Kế toán công nợ > nhóm "Nhân viên"', 'Bấm "' + TEN + '"', 'Mở ô Tài khoản; bấm In, Xuất Excel',
       'Đăng nhập TK-Z ở hệ thống cũ, vào ' + E_MENU], 'Tài khoản TK-Z',
      ['Mục menu VẪN hiện (giống hệ thống cũ)',
       'Vào màn báo "' + KHONG_QUYEN + '"; ô Tài khoản không có lựa chọn; bảng "' + NHAC + '"; không xem / In / Xuất được số liệu nào',
       'Hệ thống cũ mở trang không tìm thấy: ' + CHOT + ' (K7)']),
    C('Quyền "' + Q_ALL + '"', 'P0', 'TK-ALL có quyền này.',
      ['Đăng nhập TK-ALL, vào màn', 'Mở khu vực tìm kiếm nâng cao', 'Chọn Tài khoản 33481, Thời gian 01/01/2026 – 31/10/2026, so N với hệ thống cũ'], 'Tài khoản TK-ALL',
      ['Có ô Công ty, Phòng ban, Bộ phận, Nhân viên', 'Thấy nhân viên của MỌI công ty (có NV-C công ty B)', 'N bằng hệ thống cũ cùng tài khoản']),
    C('Quyền "' + Q_CTY + '"', 'P0', 'TK-CTY thuộc công ty TPE.',
      ['Đăng nhập TK-CTY, vào màn', 'Mở khu vực tìm kiếm nâng cao', 'Chọn Tài khoản 141, Thời gian 01/01/2026 – 31/10/2026'], 'Tài khoản TK-CTY',
      ['KHÔNG có ô Công ty; có Phòng ban, Bộ phận, Nhân viên (chỉ đơn vị / nhân viên công ty TPE)',
       'Chỉ thấy nhân viên công ty TPE; KHÔNG thấy NV-C (công ty B)']),
    C('Quyền công ty vẫn thấy công nợ của chính mình', 'P0',
      'TK-CTY (đang ở công ty TPE) có bút toán 141 của chính mình được ghi nhận thuộc công ty B (lập khi còn ở công ty B).',
      ['Đăng nhập TK-CTY, chọn Tài khoản 141, Thời gian 01/01/2026 – 31/10/2026', 'Tìm nhanh mã của TK-CTY', 'Làm tương tự ở hệ thống cũ'], '',
      ['Hệ thống mới có dòng của chính TK-CTY với đủ bút toán ghi ở công ty B',
       'Hệ thống cũ không có dòng này (trừ khi TK-CTY tạo hợp đồng của bút toán): ' + CHOT + ' (K1)']),
    C('Có cả 2 quyền thì theo quyền tổng công ty', 'P1', 'TK-2Q có cả "' + Q_ALL + '" và "' + Q_CTY + '".',
      ['Đăng nhập TK-2Q, vào màn'], '', ['Có ô Công ty, thấy mọi công ty (giống TK-ALL)']),
    C('Super Admin', 'P1', 'TK-SA thuộc nhóm Super Admin, không gán quyền lẻ.',
      ['Đăng nhập TK-SA, vào màn, chọn ' + LOC], '', ['Xem đủ mọi công ty, có ô Công ty, In / Xuất được, mã nhân viên bấm được sang Sổ chi tiết']),
    C('Bị bỏ quyền trong lúc đang xem', 'P0', 'TK-CTY đang mở bảng có số liệu.',
      ['Quản trị bỏ "' + Q_CTY + '" của TK-CTY', 'TK-CTY bấm Tìm kiếm', 'TK-CTY bấm In, Xuất Excel', 'TK-CTY tải lại trang'], '',
      ['Bấm Tìm kiếm: báo "' + KHONG_QUYEN + '", bảng thành "' + EMPTY + '"',
       'In / Xuất: không ra bản in, không tải file', 'Tải lại trang: như TK-Z (không xem được gì)', 'Gán lại quyền sau TC']),
    C('Được cấp quyền thì xem được ngay', 'P1', 'TK-Z chưa có quyền.',
      ['Quản trị gán "' + Q_CTY + '" cho TK-Z ở màn Phân quyền, nhóm "' + TEN + '"', 'TK-Z đăng nhập lại, vào màn'], '',
      ['Ô Tài khoản có lựa chọn, xem được số liệu công ty của TK-Z', 'Gỡ quyền sau TC']),
    C('Mở đường dẫn màn trực tiếp khi không có quyền', 'P0', 'TK-Z đã sao chép đường dẫn màn từ TK-ALL.',
      ['Đăng nhập TK-Z, dán đường dẫn lên thanh địa chỉ, Enter'], '',
      ['Giống mở từ menu: báo "' + KHONG_QUYEN + '", không có số liệu']),
    C('Mở đường dẫn Sổ chi tiết lấy từ mã nhân viên khi không có quyền Sổ chi tiết', 'P1',
      'TK-ALL đã sao chép đường dẫn của mã NV-A (mở Sổ chi tiết). TK-BC không có quyền Sổ chi tiết.',
      ['Đăng nhập TK-BC, dán đường dẫn đó lên thanh địa chỉ'], '',
      ['Sổ chi tiết báo không có quyền, không hiện bút toán của NV-A']),
    C('Tên quyền và nhóm quyền ở màn Phân quyền', 'P2', 'Quản trị mở màn Phân quyền.',
      ['Tìm nhóm "' + TEN + '"'], '',
      ['Nhóm có đúng 2 quyền: "' + Q_ALL + '", "' + Q_CTY + '" (cùng tên như hệ thống cũ)',
       'Quyền Sổ chi tiết nằm nhóm riêng "Sổ chi tiết công nợ nhân viên"']),
]

GROUPS = [
    ('HIỂN THỊ TRANG & TRUY CẬP', S_HIEN_THI),
    ('TÌM KIẾM & LỌC DANH SÁCH', S_LOC),
    ('SỐ LIỆU BÁO CÁO - KIỂM SỐ THEO LUỒNG PHÁT SINH VÀ ĐỐI CHIẾU HỆ THỐNG CŨ - HỆ THỐNG MỚI', S_SO_LIEU),
    ('XEM CHI TIẾT SỔ CHI TIẾT CÔNG NỢ NHÂN VIÊN (BẤM MÃ NHÂN VIÊN)', S_CT),
    ('XUẤT DANH SÁCH EXCEL', S_XUAT),
    ('IN BÁO CÁO', S_IN),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S_RB),
    ('PHÂN QUYỀN', S_PQ),
]
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
SECTIONS = [(ROMAN[i], title, [('%03d' % (k + 1),) + tc for k, tc in enumerate(tcs)])
            for i, (title, tcs) in enumerate(GROUPS)]


def tu_kiem():
    """Kiểm thêm ngoài bộ kiểm khuôn: chữ cấm trong ô case + khối mô tả (trừ dòng định nghĩa mục 1)."""
    cam = [r'\bERP\b', r'\bAPI\b', r'\bE2E\b', r'gọi thẳng', r'Postman', r'\bHRM\b']
    loi = []
    for roman, title, tcs in SECTIONS:
        for tc in tcs:
            txt = '\n'.join(tc[1:])
            for p in cam:
                if re.search(p, txt):
                    loi.append('%s.%s: "%s"' % (roman, tc[0], p))
    for label, body in DESCRIPTION_BLOCK:
        for line in body.split('\n'):
            if line.startswith('- "Hệ thống cũ" = phần mềm ERP') or line.startswith('- "Hệ thống mới" = HRM'):
                continue
            for p in cam:
                if re.search(p, line):
                    loi.append('Mô tả %s: "%s"' % (label[:3], p))
    print('Tu kiem chu cam:', 'OK' if not loi else loi)


if __name__ == '__main__':
    for roman, title, tcs in SECTIONS:
        print('%-5s %-40s %3d case, P0 %d' % (roman, title[:40], len(tcs), sum(1 for t in tcs if t[2] == 'P0')))
    tu_kiem()
    build_chuan(OUT, SHEET, TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, SECTIONS, loai='bao_cao')

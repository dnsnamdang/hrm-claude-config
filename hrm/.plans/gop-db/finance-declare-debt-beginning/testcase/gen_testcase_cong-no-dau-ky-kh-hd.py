# -*- coding: utf-8 -*-
"""Testcase màn "Công nợ đầu kỳ theo khách hàng - hợp đồng" (= màn "Khai báo đầu kỳ công nợ" khách hàng) —
bản 04/11/2026, kiểu ĐỐI CHIẾU CHÉO hệ thống cũ (ERP TanPhatDev) <-> hệ thống mới (HRM). Chỉ phần KHÁCH HÀNG.

Khuôn: skill testcase-documenter (chuẩn 03/11/2026) -> assets/tc_chuan.py `build_chuan(loai='phieu')`:
nhóm chuẩn theo thứ tự, PHÂN QUYỀN là nhóm cuối, mã TC_NN.NNN, không còn nhóm TC-ROLE.
`check_tc.py` CẤM chữ "ERP" / "API" / "E2E" trong ô testcase -> trong case gọi "hệ thống cũ" (ERP) và
"hệ thống mới" (HRM); mục 1 của khối mô tả định nghĩa 2 cụm này.

Tái dùng: docs/kh/gen_testcase.py (03/11, khuôn chuẩn, chưa có đối chiếu chéo) + gen_testcase.py (02/10, khuôn cũ,
có "Đối chiếu ERP"). Đã đối chiếu lại code ngày 04/11/2026:
  - HRM FE: hrm-client/components/finance/declare-debt/{DeclareDebtList,DeclareDebtForm,DeclareDebtContractPicker,
    ContractCodeLink}.vue, utils/finance/declareDebtConfigs.js, pages/finance/declare-debt-beginnings/**,
    components/subsystem-menu/finance.js (dòng 79-94 + 386-412: 2 lối vào), components/V2BaseImportModal.vue,
    utils/mixins/CatalogImportMixin.js
  - HRM BE: Modules/Finance/Http/Controllers/V1/{Abstract,}DeclareDebt*Controller.php,
    Http/Requests/DeclareDebt/DeclareDebtRequest.php, Services/DeclareDebt/*.php, Entities/Contract/DeclareDebtBeginning.php
    + Concerns/DeclareDebtCommon.php, Services/CustomerDebt/CustomerDebtAggregator.php, app/Support/CatalogImportOutcome.php
  - ERP: app/Http/Controllers/Accounting/DeclareDebtBeginningController.php (13/10/2026: chặn trùng HĐ theo công ty),
    app/ExcelImports/DeclareDebtBeginningImport.php, app/Model/Accounting/DeclareDebtBeginning.php,
    resources/views/accounting/declare-debt-beginning/index.blade.php, layouts/topmenubar.blade.php (dòng 952, 1171)
Chạy: PYTHONIOENCODING=utf-8 python3 gen_testcase_cong-no-dau-ky-kh-hd.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '.claude', 'skills',
                                                'testcase-documenter', 'assets')))
from tc_chuan import build_chuan  # noqa: E402

NGAY = '04/11/2026'
TEN = 'Công nợ đầu kỳ theo khách hàng - hợp đồng'
MODULE = 'Công nợ đầu kỳ KH - HĐ'
OUT = os.path.join(HERE, 'testcase - Cong no dau ky theo khach hang - hop dong.xlsx')
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


# ------------------------------------------------------------------ đường bấm + dữ liệu mẫu
MENU = 'phân hệ Tài chính > nhóm "Khai báo đầu kỳ" > "Khai báo đầu kỳ công nợ"'
MENU2 = 'phân hệ Tài chính > Kế toán công nợ > nhóm "Khách hàng" > "Công nợ đầu kỳ theo khách hàng - hợp đồng"'
E_MENU = 'hệ thống cũ: menu Kế toán > "Khai báo đầu kỳ" > "Khai báo đầu kỳ công nợ"'
E_MENU2 = 'hệ thống cũ: menu Kế toán > "Kế toán Công nợ" > nhóm "Khách hàng" > "Công nợ đầu kỳ theo khách hàng - hợp đồng"'
BC = 'phân hệ Bán hàng > Báo cáo > nhóm "Báo cáo công nợ" > "Chi tiết công nợ KH"'
BC_NV = 'phân hệ Bán hàng > Báo cáo > nhóm "Báo cáo công nợ" > "Tổng hợp công nợ theo NV"'
BC_DC = 'phân hệ Bán hàng > Báo cáo > nhóm "Báo cáo công nợ" > "Đối chiếu công nợ 1 KH"'
CAU_HINH = 'phân hệ Tài chính > "Khai Quy chế – Cấu hình" > tab "Theo công ty" > trường "Ngày khai báo đầu kỳ"'
KH = '75TPHXCH-2 - CÔNG TY CỔ PHẦN KIM LONG MOTORS HUẾ'
HD1 = 'HĐ_TPE_HN_KD3_26_0826_PO2610-1710'
HD2 = '57/2026/HĐCCLĐ/KLM-EG'
TK = '1311 - Phải thu của khách hàng ngắn hạn'
TK2 = '1312 - Phải thu khách hàng dài hạn'
QUYEN = 'Quản lý công nợ đầu kỳ'
Q_ALL = 'Xem tất cả công nợ đầu kỳ'
Q_CTY = 'Xem tất cả công nợ đầu kỳ của công ty'
Q_PB = 'Xem tất cả công nợ đầu kỳ của phòng ban'
Q_BP = 'Xem tất cả công nợ đầu kỳ của bộ phận'
EMPTY = 'Không có dữ liệu phù hợp bộ lọc.'
UNSAVED = 'Hiện hộp "Thông tin chưa lưu": "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?" với 2 nút Thoát, Ở lại'
USED = 'Khai báo đã phát sinh chứng từ, không được sửa / xóa.'
DUP = 'Đã khai báo đầu kỳ cho tài khoản này'
DUP_IMP = 'Hợp đồng đã được khai báo công nợ đầu kỳ cho tài khoản này'
DUP_ERP = 'Hợp đồng này đã được khai báo công nợ đầu kỳ trong công ty'
CHUA_DU = 'Bạn chưa nhập đầy đủ thông tin.'
CHOT = 'Khác biệt đã chốt, không ghi lỗi'
CHUA_CHOT = 'Lưu ý: lệch CHƯA CHỐT giữa 2 hệ thống — ghi Pending, chụp màn 2 bên, báo BA quyết định'
NGAY_DK = '31/12/2025'

DU_LIEU = L_(
    'Dữ liệu mẫu dùng xuyên suốt (môi trường test khác thì ghi mã thật vào cột Ghi chú):',
    '- TK-A: nhân viên công ty TPE, có "' + QUYEN + '" + "' + Q_CTY + '". TK-ALL: có "' + QUYEN + '" + "' + Q_ALL + '".',
    '- TK-F: chỉ có "' + QUYEN + '" (không quyền phạm vi). TK-Z: KHÔNG có "' + QUYEN + '". Mỗi tài khoản dùng được ở CẢ 2 hệ thống.',
    '- Khách hàng KH-1: ' + KH + '; HĐ-1: ' + HD1 + ' (hợp đồng hãng, Có hiệu lực); HĐ-2: ' + HD2 + ' (hợp đồng đầu kỳ); cả 2 chưa khai báo.',
    '- Khai báo Z: TK-A lập cho KH-1 + HĐ-1 + tài khoản ' + TK + ', Dư nợ 1,500,000, chưa có chứng từ công nợ.',
    '- Khai báo Y: khai báo đã có phiếu thu / phiếu kế toán ghi sổ trên cùng khách hàng + hợp đồng + tài khoản.',
    '- "Ngày khai báo đầu kỳ" của công ty TPE (' + CAU_HINH + ') = ' + NGAY_DK + '.',
)

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng', L_(
        'Khai báo SỐ DƯ CÔNG NỢ ĐẦU KỲ của khách hàng theo từng hợp đồng × tài khoản — số mở đầu cho sổ công nợ phải thu và '
        'các báo cáo công nợ khách hàng. Mỗi dòng lưu thành 1 khai báo (1 mã phiếu, 1 bút toán), có hiệu lực ngay, KHÔNG qua duyệt.',
        'Màn có 2 LỐI VÀO, cùng một màn, cùng dữ liệu: (1) ' + MENU + '; (2) ' + MENU2 + '.',
        'Bộ testcase này ĐỐI CHIẾU CHÉO: "hệ thống cũ" = ERP Tân Phát (' + E_MENU.replace('hệ thống cũ: ', '') + ', và lối thứ 2 ' +
        E_MENU2.replace('hệ thống cũ: ', '') + '); "hệ thống mới" = HRM. Hai hệ thống dùng CHUNG dữ liệu: khai báo lập / sửa / '
        'xóa / import ở bên này thì bên kia thấy ngay; báo cáo công nợ hai bên đọc cùng bút toán.',
        'Chức năng: Xem danh sách, Tìm kiếm / lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới, Sửa, Xem chi tiết, Xóa, Lịch sử, '
        'In danh sách, Xuất Excel, Import Excel.',
        DU_LIEU,
    )),
    ('2. Đối tượng được tính / hiển thị', L_(
        'Phạm vi xem (xét lần lượt, gặp quyền nào trước thì dùng quyền đó — giống hệ thống cũ):',
        '- "' + Q_ALL + '": mọi công ty; khu vực lọc có ô Công ty, Phòng ban, Bộ phận.',
        '- "' + Q_CTY + '": công ty đang làm việc; có ô Phòng ban, Bộ phận.',
        '- "' + Q_PB + '" / "' + Q_BP + '": các phòng ban / bộ phận được giao quản lý.',
        '- Không có quyền phạm vi nào: chỉ khai báo do chính mình tạo.',
        'Công ty / phòng ban / bộ phận của khai báo = của NGƯỜI LẬP HỢP ĐỒNG (không phải người lập khai báo).',
        'Cửa sổ "Chọn hợp đồng / đơn hàng" chỉ hiện hợp đồng THUỘC khách hàng đang chọn: hợp đồng bán Đã duyệt / Có hiệu lực, '
        'hợp đồng hãng Có hiệu lực (không gồm hợp đồng nguyên tắc của hãng), hợp đồng gói dịch vụ và hợp đồng dự án (khác trạng thái 3), '
        'hợp đồng đầu kỳ, 3 loại hợp đồng mua.',
        'Tài khoản chọn được: mọi tài khoản CHI TIẾT (không có tài khoản con) đang hoạt động.',
    )),
    ('3. Đối tượng bị ẩn / không tính', L_(
        '- Khai báo ngoài phạm vi xem: không hiện; mở đường dẫn trực tiếp thì sang trang "Không tìm thấy".',
        '- Cửa sổ chọn hợp đồng: hợp đồng đã có khai báo của khách hàng này hiện mờ, Tình trạng "Đã khai báo", không chọn được; '
        'hợp đồng đã có trên trang ghi "Đã chọn".',
        '- Nút Sửa / Xóa ẨN HẲN khi khai báo ĐÃ PHÁT SINH CHỨNG TỪ CÔNG NỢ: cùng khách hàng + hợp đồng + tài khoản đã có phiếu thu, '
        'phiếu chi, phiếu báo có, ủy nhiệm chi hoặc phiếu kế toán ghi sổ, hoặc có chứng từ thu / chi thẳng vào khai báo.',
        '- Phiếu xuất / nhập hàng, hạch toán dịch vụ trên cùng hợp đồng KHÔNG làm khai báo bị khóa.',
        '- Tài khoản đang khóa: không chọn mới được; khai báo cũ đang dùng tài khoản đó vẫn hiện tài khoản kèm biểu tượng khóa.',
        '- Báo cáo công nợ khách hàng chỉ đọc bút toán tài khoản 131 và các tài khoản con trực tiếp (1311, 1312…).',
    )),
    ('4. Bộ lọc thời gian áp dụng cho', L_(
        'Ô "Ngày tạo" (Từ – Đến): ngày lập khai báo, tính cả 2 đầu mút. Ô "Ngày BGNT" (Từ – Đến): ngày bàn giao nghiệm thu.',
        'NGÀY HẠCH TOÁN của khai báo = "Ngày khai báo đầu kỳ" cấu hình theo công ty của NGƯỜI LẬP KHAI BÁO (' + CAU_HINH +
        '), chụp lại lúc lưu; không hiện trên màn, không phải ô lọc.',
        'Ở báo cáo công nợ: ngày hạch toán TRƯỚC "Từ ngày" thì vào Số dư đầu kỳ; nằm TRONG kỳ thì Dư nợ vào cột Hàng hóa/Dịch vụ, '
        'Dư có vào cột Đã thanh toán; SAU "Đến ngày" thì không tính.',
        'Bộ lọc danh sách được ghi nhớ 10 phút khi vào trang chi tiết / sửa rồi quay lại.',
    )),
    ('5. Cấu trúc dữ liệu / cây phân cấp', L_(
        'Một lần lập = 1 khách hàng × nhiều hợp đồng; mỗi dòng thành 1 khai báo, mã <mã công ty>.CNĐKHĐ.<5 chữ số>.',
        'Khai báo gồm: Mã phiếu, Khách hàng, Loại hợp đồng, Số hợp đồng, Tài khoản, Loại dư, Công nợ, Quá hạn, Ngày BGNT, '
        'Người tạo / Ngày tạo, Người cập nhật / Ngày cập nhật.',
        'Trang Sửa và Chi tiết chỉ có 1 dòng; Mã phiếu, Khách hàng, hợp đồng không đổi được.',
        'Trạng thái do hệ thống tự xác định (không có cột riêng): Chưa phát sinh chứng từ (Sửa, Xóa được) chuyển Đã phát sinh '
        '(chỉ xem); chứng từ bị xóa / hủy ghi sổ thì khai báo trở lại Chưa phát sinh.',
    )),
    ('6. Quy tắc cộng dồn / deduplicate', L_(
        '- Hệ thống mới chặn trùng theo khách hàng + hợp đồng + tài khoản (trên cùng trang, khi Sửa đổi tài khoản và khi import).',
        '- Công nợ phải lớn hơn 0. Dư nợ ghi Nợ, Dư có ghi Có tài khoản.',
        '- Chỉ Dư nợ được đánh dấu Quá hạn; Quá hạn thì Ngày BGNT bắt buộc, không lớn hơn hôm nay. Đổi sang Dư có thì tự bỏ Quá hạn.',
        '- Hợp đồng phải thuộc khách hàng đang chọn (cả trang thêm và import).',
        '- Lưu / Sửa / Xóa khai báo thì bút toán trên sổ công nợ tạo / đổi / mất theo, ngay lập tức.',
    )),
    ('7. Phân quyền cấp', L_(
        '- "' + QUYEN + '": thấy CẢ 2 mục menu, vào màn, xem, thêm, sửa, xóa, import, in, xuất (1 quyền cho cả màn — giống hệ thống cũ).',
        '- 4 quyền phạm vi: "' + Q_ALL + '", "' + Q_CTY + '", "' + Q_PB + '", "' + Q_BP + '" (dùng chung với màn nhà cung cấp).',
        '- Quyền gán ở màn Phân quyền, nhóm "Khai báo đầu kỳ công nợ". Cùng một tài khoản phải có cùng quyền ở 2 hệ thống.',
    )),
    ('8. Cách tính các ô thống kê', L_(
        'Chân bảng "Hiển thị a–b / N": a, b là dòng đầu / cuối trang đang xem, N = tổng khai báo khớp bộ lọc và phạm vi quyền.',
        'Cột "Dư nợ" chỉ có số khi Loại dư = Dư nợ, cột "Dư có" chỉ có số khi Loại dư = Dư có; cột còn lại để TRỐNG.',
        'Báo cáo Chi tiết công nợ KH: Số dư đầu kỳ = tổng Nợ - tổng Có các bút toán có ngày hạch toán trước "Từ ngày"; '
        'Đã thanh toán = Có của phiếu thu, phiếu báo có VÀ khai báo đầu kỳ; Hàng hóa/Dịch vụ gồm phần Nợ của khai báo đầu kỳ.',
    )),
    ('9. Ghi chú đọc bảng', L_(
        'KHÁC BIỆT ĐÃ CHỐT giữa 2 hệ thống (gặp thì ghi "' + CHOT + '"):',
        '- K1. Thêm / Sửa ở hệ thống cũ là cửa sổ nổi trên danh sách; hệ thống mới là trang riêng (Thêm, Sửa, Chi tiết).',
        '- K2. Danh sách mới ẩn sẵn 4 cột Tài khoản, Loại hợp đồng, Người cập nhật, Ngày cập nhật (bật ở Cấu hình cột); hệ thống cũ '
        'hiện đủ 14 cột, nhãn "Mã" / "Mã hợp đồng" / "Người sửa" / "Ngày sửa". Người tạo mới ghi "Họ tên - Mã phòng ban", ngày giờ không có giây.',
        '- K3. Khai báo ĐÃ PHÁT SINH chứng từ công nợ: hệ thống mới ẩn Sửa / Xóa và chặn; hệ thống cũ vẫn cho sửa / xóa.',
        '- K4. Câu báo theo chuẩn mới ("Thêm mới thành công.", "Cập nhật thành công.", "Xóa thành công."); cũ "Thêm công nợ thành công!"…',
        '- K5. Mã phiếu mới = số lớn nhất + 1; cũ đánh theo số thứ tự bản ghi. Cùng tiền tố, lập xen kẽ không được trùng.',
        '- K6. Import mới: kiểm từng dòng trên bảng xem trước, nhập dòng hợp lệ, trả bảng dòng bị bỏ; cột Loại hợp đồng BẮT BUỘC; '
        'Loại dư trống = Dư nợ; file mẫu 1 dòng tiêu đề. Cũ: 1 dòng lỗi là không nhập dòng nào; Loại hợp đồng trống thì tự nhận; Loại dư trống báo lỗi.',
        '- K7. Xuất Excel mới cho chọn trường, file khai_bao_dau_ky_cong_no.xlsx; cũ cố định 14 cột, file danh_sach_cong_no_dau_ky_khach_hang_hop_dong.xlsx.',
        '- K8. Lịch sử thay đổi chỉ ghi thao tác làm trên hệ thống mới (hệ thống cũ không có lịch sử).',
        'HỆ THỐNG MỚI SỬA LỖI hệ thống cũ (ghi kết quả đúng theo hệ thống mới; hiện tượng ở hệ thống cũ chỉ để tham chiếu):',
        '- V1. Cửa sổ chọn hợp đồng để trống Loại hợp đồng: mới gộp mọi nguồn; cũ chỉ ra hợp đồng bán.',
        '- V2. Hợp đồng mua lọc đúng khách hàng; hợp đồng dự án / đầu kỳ / mua trong nước hiện mọi hợp đồng của khách (cũ chỉ hợp đồng mình tạo).',
        '- V3. Lọc "Mã hợp đồng" ra đủ mọi loại hợp đồng (cũ không ra khai báo gắn hợp đồng gói dịch vụ, dự án, dịch vụ BH - SC…).',
        '- V4. Import kiểm hợp đồng phải thuộc khách hàng của dòng và tài khoản phải là tài khoản chi tiết đang hoạt động (cũ không kiểm).',
        '- V5. Sửa tài khoản: sổ cập nhật cả số hiệu tài khoản mới (cũ giữ số hiệu cũ). V6. Bấm Lưu 2 lần không sinh 2 khai báo trùng.',
        'LỆCH CHƯA CHỐT (ghi Pending, báo BA): L1. Từ 13/10/2026 hệ thống cũ chặn 1 hợp đồng chỉ khai báo 1 lần trong 1 công ty '
        '(bất kể tài khoản, câu "' + DUP_ERP + '"); hệ thống mới chặn theo khách hàng + hợp đồng + tài khoản. '
        'L2. Import mã HDHNTDA / HDDV: hệ thống cũ từ chối hợp đồng không "Có hiệu lực" và hợp đồng nguyên tắc của hãng; hệ thống mới chưa kiểm.',
        'Khác: số theo chuẩn 1,500,000 · 2,750,000.5; bản in tối đa 2,000 dòng; tiêu đề cửa sổ Lịch sử dùng MÃ PHIẾU; '
        'màn KHÔNG có Khóa / Gửi duyệt / Duyệt / Hủy phiếu. Cột KQ thực tế, DNS check để trống cho tester điền.',
    )),
]

# =============================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S_HIEN_THI = [
    C('Mở màn hình từ lối vào "Khai báo đầu kỳ công nợ"', 'P0', 'TK-A đã đăng nhập hệ thống mới; phạm vi của TK-A có N khai báo (đếm sẵn).',
      ['Đăng nhập bằng TK-A', 'Vào ' + MENU, 'Đọc tiêu đề, các nút và dòng tổng dưới bảng'], '',
      ['Tiêu đề trang và tiêu đề bảng "Khai báo đầu kỳ công nợ"; bảng tự tải, không cần bấm Tìm kiếm',
       'Có các nút: Tạo mới, Import Excel, Xuất Excel, In danh sách và nút Cấu hình cột hiển thị',
       'Khu vực tìm kiếm có ô tìm nhanh, nút Tìm kiếm, Làm mới, Tìm kiếm nâng cao, Cài đặt bộ lọc',
       'Dòng tổng "Hiển thị 1–10 / N"; ô số dòng/trang cho chọn 5 / 10 / 20 / 50 / 100']),
    C('Mở màn hình từ lối vào "Công nợ đầu kỳ theo khách hàng - hợp đồng"', 'P0', 'TK-A vừa mở màn từ lối vào thứ nhất, ghi lại N và 5 mã phiếu đầu.',
      ['Vào ' + MENU2, 'So với danh sách vừa mở ở lối vào thứ nhất'], '',
      ['Mở CÙNG màn "Khai báo đầu kỳ công nợ": cùng tiêu đề, cùng các nút, cùng ô lọc',
       'Cùng tổng N và cùng 5 mã phiếu đầu theo đúng thứ tự']),
    C('Hai lối vào dùng chung dữ liệu', 'P0', 'TK-A có quyền như Test data; KH-1 + HĐ-2 chưa khai báo.',
      ['Vào màn từ lối vào thứ nhất, Tạo mới khai báo KH-1 + HĐ-2 + 1311, Dư nợ 2,000,000', 'Vào màn từ lối vào thứ hai, tìm khai báo vừa tạo',
       'Ở lối vào thứ hai bấm Xóa khai báo đó', 'Quay lại lối vào thứ nhất, tìm lại'],
      ['Khách hàng: KH-1', 'Hợp đồng: HĐ-2', 'Công nợ: 2,000,000'],
      ['Bước 2: thấy ngay khai báo vừa tạo, đúng số liệu', 'Bước 4: khai báo không còn ở lối vào thứ nhất; tổng N trở về như trước bước 1']),
    C('Đang lọc ở lối vào này rồi bấm lối vào kia', 'P1', 'Đang ở màn mở từ lối vào thứ nhất, đã lọc Loại dư = Dư có.',
      ['Bấm mục ' + MENU2, 'Quan sát khối tìm kiếm và bảng'], 'Loại dư: Dư có',
      ['Vẫn ở đúng màn Khai báo đầu kỳ công nợ, không báo lỗi, không mở thêm trang',
       'Danh sách khớp ĐÚNG các điều kiện đang hiện trên khối tìm kiếm (không có điều kiện lọc ngầm nào không thấy ô)']),
    C('Hai lối vào ở hệ thống cũ cùng số liệu với hệ thống mới', 'P0', 'TK-A có cùng quyền ở 2 hệ thống. Chưa lọc gì.',
      ['Ở hệ thống cũ lần lượt vào ' + E_MENU + ' và ' + E_MENU2.replace('hệ thống cũ: ', '') + ', đọc tổng số dòng',
       'Ở hệ thống mới vào ' + MENU + ', đọc N', 'So sánh'], 'Tài khoản TK-A',
      ['Hai lối vào ở hệ thống cũ mở cùng một màn, cùng tổng',
       'Tổng ở hệ thống cũ BẰNG N ở hệ thống mới (cùng tài khoản, cùng phạm vi)',
       'Lệch thì kiểm quyền 2 bên trước khi ghi lỗi']),
    C('Kiểm tra các cột mặc định hiển thị', 'P0', 'Tài khoản chưa từng tùy chỉnh cột ở màn này.',
      ['Mở màn hình', 'Đọc tên từng tiêu đề cột từ trái sang phải', 'Mở màn ở hệ thống cũ để so'], '',
      ['Đúng thứ tự: STT, Mã phiếu, Khách hàng, Số hợp đồng, Dư nợ, Dư có, Quá hạn, Ngày BGNT, Người tạo, Ngày tạo, Hành động',
       'Tài khoản, Loại hợp đồng, Người cập nhật, Ngày cập nhật không hiện nhưng có trong Cấu hình cột (chưa tích)',
       'KHÔNG có cột "Ngày tính công nợ"',
       'Hệ thống cũ hiện đủ 14 cột với nhãn "Mã", "Mã hợp đồng", "Người sửa", "Ngày sửa": ' + CHOT + ' (K2)']),
    C('Dữ liệu trên dòng khớp với khai báo đã tạo', 'P0', 'Vừa tạo khai báo Z như Test data.',
      ['Tìm Z theo mã phiếu', 'Bật cột Tài khoản, Loại hợp đồng', 'Đối chiếu từng ô với dữ liệu đã nhập'],
      ['Khách hàng: ' + KH, 'Hợp đồng: ' + HD1, 'Tài khoản: ' + TK, 'Loại dư: Dư nợ, Công nợ: 1,500,000'],
      ['Khách hàng "' + KH + '", Số hợp đồng "' + HD1 + '", Loại hợp đồng "Hợp đồng hãng", Tài khoản "' + TK + '"',
       'Dư nợ 1,500,000; Dư có để trống; Quá hạn "Không"; Ngày BGNT trống',
       'Người tạo là TK-A dạng "Họ tên - Mã phòng ban", Ngày tạo đúng thời điểm lưu']),
    C('Định dạng số, ngày và ô trống', 'P1', 'Có khai báo Dư có 2,750,000.5 và khai báo Dư nợ quá hạn, Ngày BGNT 30/09/2026.',
      ['Tìm 2 khai báo trên', 'Đọc cột Dư nợ, Dư có, Quá hạn, Ngày BGNT, Ngày tạo'], '',
      ['Dư có hiện "2,750,000.5", cột Dư nợ cùng dòng để TRỐNG (không 0, không gạch)',
       'Quá hạn "Có" / "Không"; không quá hạn thì Ngày BGNT trống; quá hạn thì Ngày BGNT "30/09/2026"',
       'Ngày tạo dạng dd/mm/yyyy HH:mm (hệ thống cũ có thêm giây: ' + CHOT + ')']),
    C('Mã phiếu và Số hợp đồng là đường dẫn', 'P1', 'Có khai báo Z (hợp đồng hãng) và khai báo gắn hợp đồng mua.',
      ['Bấm vào mã phiếu Z', 'Quay lại, chuột phải vào mã phiếu Z', 'Bấm vào số hợp đồng của 2 dòng'], '',
      ['Bấm trái mã phiếu mở "Chi tiết khai báo đầu kỳ công nợ: <mã Z>"; chuột phải có "Mở liên kết trong tab mới"',
       'Số hợp đồng mở tab mới tới trang xem hợp đồng; hợp đồng chưa có trang xem thì là chữ thường, không bấm được']),
    C('Khai báo đã phát sinh chứng từ thì ẩn nút Sửa, Xóa', 'P0', 'Có khai báo Y (đã phát sinh) và khai báo Z (chưa phát sinh).',
      ['Tìm 2 dòng Y và Z, quan sát cột Hành động', 'Mở cùng 2 dòng ở hệ thống cũ'], '',
      ['Dòng Y chỉ còn Lịch sử (trong menu ba chấm), KHÔNG có Sửa / Xóa (ẩn hẳn, không hiện xám)', 'Dòng Z có Sửa, Xóa, Lịch sử',
       'Hệ thống cũ vẫn hiện Sửa / Xóa ở dòng Y: ' + CHOT + ' (K3)']),
    C('Phiếu xuất hàng không làm khóa khai báo', 'P0',
      'Hợp đồng H đã có phiếu xuất hàng ghi sổ tài khoản 1311, chưa có phiếu thu / phiếu chi / phiếu kế toán; vừa tạo khai báo trên H.',
      ['Mở danh sách, tìm khai báo vừa tạo'], '',
      ['Dòng vẫn có nút Sửa, Xóa (chỉ chứng từ công nợ mới khóa khai báo)']),
    C('Hiển thị khi không có dữ liệu', 'P1', 'TK-F chưa tạo khai báo nào. Danh sách của TK-A có dữ liệu.',
      ['Đăng nhập TK-F, vào màn', 'Đăng nhập TK-A, gõ "zzzkhongtontai999" vào ô tìm nhanh, nhấn Enter'], 'Từ khóa: zzzkhongtontai999',
      ['Cả 2 trường hợp: bảng hiện "' + EMPTY + '", dòng dưới bảng "Không có khai báo nào."',
       'Không báo lỗi; nút Tạo mới, Import Excel vẫn dùng được']),
    C('Phân trang: số thứ tự, đổi số dòng, nút chuyển trang', 'P0', 'Phạm vi có N khai báo, nhiều hơn 5 trang. Đang ở trang 1.',
      ['Bấm › rồi ‹', 'Bấm » rồi «', 'Sang trang 3, đổi số dòng/trang sang 50', 'Quan sát STT, dòng tổng và trạng thái nút'], 'Số dòng/trang: 50',
      ['› sang trang 2 "Hiển thị 11–20 / N", STT bắt đầu 11; ‹ về "Hiển thị 1–10 / N"',
       '» tới trang cuối, STT dòng cuối = N; « về trang 1',
       'Ở trang 1 nút « và ‹ mờ; ở trang cuối nút › và » mờ',
       'Đổi 50 dòng: về trang 1, đúng 50 dòng, "Hiển thị 1–50 / N"; dữ liệu các trang không lặp, không thiếu']),
    C('Thứ tự mặc định khi mở màn', 'P1', 'Vừa tạo khai báo Z. Chưa bấm sắp xếp cột nào.',
      ['Vào ' + MENU, 'Đọc các dòng đầu'], '',
      ['Khai báo Z vừa tạo ở dòng đầu, STT = 1; các dòng xếp theo thời điểm tạo, mới nhất ở trên (giống hệ thống cũ)']),
    C('Sắp xếp theo Mã phiếu, Ngày tạo, Ngày cập nhật', 'P1', 'Có hơn 20 khai báo; đã bật cột Ngày cập nhật.',
      ['Bấm tiêu đề Mã phiếu 2 lần, đọc 5 dòng đầu mỗi lần', 'Làm tương tự với Ngày tạo, Ngày cập nhật'], '',
      ['Lần 1 tăng dần (mũi tên lên), lần 2 giảm dần (mũi tên xuống)', 'Giá trị cột đang sắp xếp tăng / giảm đều, không lộn xộn',
       'STT, Khách hàng, Số hợp đồng, Dư nợ, Dư có, Quá hạn, Ngày BGNT, Người tạo, Hành động KHÔNG có mũi tên, bấm không đổi thứ tự']),
    C('Sắp xếp giữ khi chuyển trang, đổi sắp xếp thì về trang 1', 'P1', 'Có hơn 3 trang; đang sắp xếp giảm dần theo Mã phiếu, ở trang 1.',
      ['Sang trang 2, so dòng đầu trang 2 với dòng cuối trang 1', 'Sang trang 3, bấm tiêu đề Ngày tạo'], '',
      ['Thứ tự nối tiếp liền mạch, mũi tên vẫn ở Mã phiếu', 'Bấm Ngày tạo: bảng về trang 1, N không đổi']),
]

# =============================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S_LOC = [
    C('Tìm nhanh theo mã phiếu, số hợp đồng, mã / tên khách hàng', 'P0', 'Có khai báo Z của KH-1.',
      ['Gõ "KIM LONG" vào ô tìm nhanh (chưa bấm gì)', 'Nhấn Enter', 'Lần lượt tìm theo mã phiếu Z, theo số hợp đồng HĐ-1',
       'Gõ "75tphx", bấm Tìm kiếm; rồi gõ "75TPHX", bấm Tìm kiếm'],
      ['Từ khóa: KIM LONG', 'Từ khóa: 75tphx / 75TPHX'],
      ['Placeholder: "Tìm theo mã phiếu, số hợp đồng, mã hoặc tên khách hàng"', 'Đang gõ thì bảng chưa đổi; nhấn Enter mới lọc',
       'Ra đúng khai báo của khách hàng có tên chứa từ khóa; tìm theo mã phiếu / số hợp đồng ra đúng khai báo chứa chuỗi đó',
       'Tìm một phần, chữ hoa hay thường đều ra CÙNG tập kết quả']),
    C('Tìm với ký tự đặc biệt, khoảng trắng, chuỗi dài', 'P2', 'Đang ở màn danh sách.',
      ['Gõ "@#$^&*", bấm Tìm kiếm', 'Gõ "/2026/HĐ", bấm Tìm kiếm', 'Gõ "   KIM LONG   ", bấm Tìm kiếm', 'Dán chuỗi 500 ký tự, bấm Tìm kiếm'],
      ['@#$^&*', '/2026/HĐ', '"   KIM LONG   "', '"abcde" lặp 100 lần'],
      ['"@#$^&*" và chuỗi 500 ký tự: "' + EMPTY + '", không báo lỗi hệ thống, không treo',
       '"/2026/HĐ": ra khai báo có số hợp đồng chứa đúng chuỗi (vd ' + HD2 + ')',
       'Có khoảng trắng 2 đầu: kết quả giống "KIM LONG"']),
    C('Xóa từ khóa thì danh sách quay về đầy đủ', 'P0', 'Đang tìm với từ khóa "KIM LONG"; phạm vi có N khai báo.',
      ['Xóa hết nội dung ô tìm nhanh', 'Nhấn Enter'], '',
      ['Dòng tổng quay lại "Hiển thị 1–10 / N", bảng về trang 1']),
    C('Lọc theo Khách hàng', 'P0', 'KH-1 có khai báo.',
      ['Mở Tìm kiếm nâng cao', 'Ô Khách hàng gõ 1 ký tự, rồi gõ "75TPHXCH-2"', 'Chọn khách hàng trong gợi ý'], 'Khách hàng: 75TPHXCH-2',
      ['Gõ 1 ký tự: báo cần gõ thêm, chưa tìm', 'Gợi ý dạng "Mã - Tên"', 'Chọn xong bảng tự lọc ngay, chỉ còn khai báo của KH-1']),
    C('Lọc theo Tài khoản và Loại hợp đồng', 'P1', 'Có khai báo tài khoản 1311 và 1312; có khai báo gắn hợp đồng đầu kỳ.',
      ['Ô Tài khoản chọn "' + TK + '"', 'Xóa, ô Loại hợp đồng mở danh sách, chọn "Hợp đồng đầu kỳ"', 'Bật cột Tài khoản, Loại hợp đồng để kiểm'],
      ['Tài khoản: 1311', 'Loại hợp đồng: Hợp đồng đầu kỳ'],
      ['Chọn là lọc ngay', 'Mọi dòng đúng tài khoản / đúng loại hợp đồng đã chọn',
       'Danh sách Loại hợp đồng có: Hợp đồng bán, Hợp đồng hãng / dự án, Hợp đồng gói dịch vụ, Hợp đồng dự án, Hợp đồng đầu kỳ, '
       'Hợp đồng mua nước ngoài, Hợp đồng mua ngoài, Hợp đồng mua trong nước, Hợp đồng dịch vụ BH - SC',
       'Lưu ý: nếu thấy 2 mục cùng tên "Hợp đồng mua trong nước" thì ghi lỗi hiển thị (không phân biệt được 2 loại)']),
    C('Lọc theo Mã hợp đồng ra đủ mọi loại hợp đồng', 'P1', 'Có khai báo gắn hợp đồng đầu kỳ, hợp đồng hãng và hợp đồng dịch vụ BH - SC có số chứa "26_08".',
      ['Ô Mã hợp đồng gõ "26_08"', 'Nhấn Enter', 'Lọc cùng chuỗi ở hệ thống cũ'], 'Mã hợp đồng: 26_08',
      ['Chờ Enter mới lọc; ra MỌI khai báo có số hợp đồng chứa chuỗi, đủ cả 3 loại hợp đồng',
       'Hệ thống cũ có thể thiếu khai báo gắn hợp đồng dịch vụ BH - SC / dự án: hệ thống mới đã sửa (V3), ghi kết quả theo hệ thống mới']),
    C('Lọc theo Loại dư', 'P0', 'Có cả khai báo Dư nợ và Dư có.',
      ['Ô Loại dư chọn "Dư nợ"', 'Đổi sang "Dư có"'], 'Loại dư: Dư nợ / Dư có',
      ['Chọn là lọc ngay', 'Dư nợ: mọi dòng chỉ có số ở cột Dư nợ', 'Dư có: mọi dòng chỉ có số ở cột Dư có']),
    C('Lọc theo khoảng Số tiền', 'P1', 'Có khai báo Dư nợ 1,500,000, Dư có 5,250,000 và Dư nợ 10,125,000.',
      ['Ô Số tiền nhập Từ 1,000,000, Đến 5,250,000', 'Nhấn Enter'], 'Số tiền từ 1,000,000 đến 5,250,000',
      ['Ra khai báo 1,500,000 và 5,250,000 (tính cả 2 đầu, cả Dư nợ lẫn Dư có)', 'Không có khai báo 10,125,000']),
    C('Lọc theo Quá hạn và Ngày BGNT', 'P1', 'Có khai báo quá hạn, Ngày BGNT 30/10/2023 và khai báo không quá hạn.',
      ['Ô Quá hạn chọn "Có"', 'Ô Ngày BGNT chọn 01/10/2023 – 31/10/2023', 'Ô Quá hạn đổi "Không", xóa Ngày BGNT'], 'Quá hạn: Có / Không',
      ['Bước 1: mọi dòng Quá hạn "Có"', 'Bước 2: chỉ còn khai báo có Ngày BGNT trong tháng 10/2023',
       'Bước 3: mọi dòng "Không", Ngày BGNT trống (chọn "Không" là có lọc, không bị coi là bỏ trống)']),
    C('Lọc theo Người tạo, Người cập nhật, Ngày tạo', 'P1', 'TK-A tạo khai báo ngày 15/10/2026 lúc 23:50; TK-ALL sửa một khai báo khác.',
      ['Ô Người tạo chọn TK-A', 'Xóa, ô Người cập nhật chọn TK-ALL', 'Xóa, ô Ngày tạo chọn 15/10/2026 – 15/10/2026'], '',
      ['Chỉ còn khai báo do người đó tạo / cập nhật lần cuối', 'Ngày tạo ra đủ khai báo trong ngày, kể cả lúc 23:50']),
    C('Lọc theo Công ty / Phòng ban / Bộ phận', 'P1', 'Đăng nhập TK-ALL.',
      ['Ô Công ty chọn TPE', 'Ô Phòng ban chọn một phòng', 'Đổi Công ty'], '',
      ['Mỗi ô chọn xong là lọc ngay (theo công ty / phòng của NGƯỜI LẬP HỢP ĐỒNG)', 'Phòng ban, Bộ phận chỉ mở sau khi chọn cấp trên',
       'Đổi Công ty thì Phòng ban, Bộ phận tự xóa']),
    C('Lọc kết hợp nhiều tiêu chí và từ khóa', 'P0', 'KH-1 có M khai báo, trong đó K khai báo Dư nợ tài khoản 1311.',
      ['Gõ "75TPHXCH-2" vào ô tìm nhanh, nhấn Enter, đọc dòng tổng', 'Chọn thêm Loại dư = Dư nợ, Tài khoản = 1311', 'Đọc lại dòng tổng'],
      ['Từ khóa: 75TPHXCH-2', 'Loại dư: Dư nợ', 'Tài khoản: ' + TK],
      ['Bước 1: "… / M"', 'Bước 3: "… / K", mọi dòng thỏa ĐỒNG THỜI 3 điều kiện', 'Số dòng trên bảng khớp dòng tổng']),
    C('Kết quả lọc khớp với hệ thống cũ', 'P0', 'TK-A cùng quyền ở 2 hệ thống.',
      ['Ở hệ thống mới lọc Khách hàng = KH-1, Tài khoản = 1311, Quá hạn = Có, đọc dòng tổng',
       'Ở hệ thống cũ lọc cùng Khách hàng, Tài khoản, Quá hạn, đọc tổng', 'So từng mã phiếu'], '',
      ['Hai hệ thống ra CÙNG số dòng và cùng danh sách mã phiếu, cùng Dư nợ / Dư có từng dòng']),
    C('Áp dụng bộ lọc khi đang ở trang giữa thì về trang 1', 'P0', 'Đang ở trang 3. Bộ lọc mới cho ra nhiều hơn 1 trang.',
      ['Chọn Loại dư = Dư nợ', 'Quan sát bảng, phân trang, rồi chuyển sang trang 2'], '',
      ['Bảng về trang 1, "Hiển thị 1–10 / <số sau lọc>"', 'Trang 2 vẫn chỉ gồm khai báo Dư nợ']),
    C('Nút Làm mới xóa hết tiêu chí và tải lại', 'P0', 'Đang lọc Loại dư = Dư nợ và từ khóa "KIM LONG". Phạm vi có N khai báo.',
      ['Bấm Làm mới', 'Quan sát các ô lọc, bảng và dòng tổng'], '',
      ['Mọi ô lọc và ô tìm nhanh về trống', 'Bảng tải lại ngay, "Hiển thị 1–10 / N"; phạm vi xem không đổi']),
    C('Cài đặt bộ lọc', 'P2', 'Đang ở màn danh sách.',
      ['Bấm Cài đặt bộ lọc', 'Bỏ tích "Người cập nhật", kéo "Loại dư" lên đầu, bấm Lưu', 'Tải lại trang (F5)', 'Mở lại, bấm Khôi phục mặc định'], '',
      ['Cửa sổ liệt kê các ô lọc kèm số thứ tự', 'Sau Lưu và F5: ô Người cập nhật ẩn, Loại dư đứng đầu', 'Khôi phục mặc định đưa về như ban đầu']),
    C('Vào trang chi tiết rồi quay lại thì giữ bộ lọc', 'P1', 'Đang lọc Khách hàng = KH-1, Loại dư = Dư có, ở trang 2.',
      ['Bấm vào một mã phiếu', 'Bấm Quay lại'], '',
      ['Bộ lọc còn Khách hàng = KH-1 (ô hiện đúng tên) và Loại dư = Dư có', 'Kết quả giống trước khi vào chi tiết']),
    C('Rời màn, F5, tab mới, tài khoản khác thì bộ lọc về mặc định', 'P2', 'TK-A đang lọc từ khóa "KIM LONG", Loại dư = Dư nợ.',
      ['Sang màn khác trên menu rồi quay lại', 'Lọc lại, nhấn F5', 'Lọc lại, mở màn ở tab mới', 'Đăng xuất, đăng nhập TK-ALL, vào màn'],
      'Từ khóa: KIM LONG; Loại dư: Dư nợ',
      ['Cả 4 trường hợp: ô tìm nhanh và ô lọc trống, bảng hiện toàn bộ phạm vi ở trang 1, 10 dòng/trang',
       'Tab cũ vẫn giữ bộ lọc của nó; bộ lọc của TK-A không mang sang TK-ALL']),
]

# =============================================================== III. THÊM MỚI
S_THEM = [
    C('Mở trang thêm mới', 'P0', 'TK-A đang ở màn danh sách.',
      ['Bấm Tạo mới', 'Quan sát trang'], '',
      ['Tiêu đề "Thêm khai báo đầu kỳ công nợ"; góc phải khối Thông tin chung "<tên TK-A> - <ngày giờ hiện tại>"',
       'Ô Khách hàng (*), placeholder "Nhập mã/tên khách hàng"; KHÔNG có ô "Ngày tính công nợ"',
       'Khối "Danh sách hợp đồng" có nút "Chọn hợp đồng", bảng ghi "Chưa chọn hợp đồng nào — bấm "Chọn hợp đồng" để thêm."',
       'Cột: STT, Loại hợp đồng, Số hợp đồng, Tài khoản *, Loại dư *, Công nợ *, Quá hạn, Ngày BGNT *, nút xóa dòng',
       'Chân trang: Lưu, Lưu và tiếp tục, Quay lại (hệ thống cũ là cửa sổ nổi: ' + CHOT + ' K1)']),
    C('Chưa chọn khách hàng thì không mở được cửa sổ chọn hợp đồng', 'P0', 'Đang ở trang thêm mới, ô Khách hàng trống.',
      ['Bấm "Chọn hợp đồng"'], '',
      ['Không mở cửa sổ', 'Báo đỏ dưới ô Khách hàng: "Chọn khách hàng trước khi chọn hợp đồng"']),
    C('Cửa sổ chọn hợp đồng: danh sách và tình trạng', 'P0', 'KH-1 có hợp đồng đầu kỳ 11/2026/HĐCCCLD/KLM đã khai báo.',
      ['Chọn KH-1 (gõ tối thiểu 2 ký tự, gợi ý "Mã - Tên")', 'Bấm "Chọn hợp đồng"'], '',
      ['Tiêu đề "Chọn hợp đồng / đơn hàng", dòng phụ "Khách hàng: ' + KH + '"',
       'Cột: STT, Loại hợp đồng, Số hợp đồng, Tổng thanh toán, Người tạo, Ngày tạo, Tình trạng',
       'Hợp đồng đã khai báo: dòng mờ, Tình trạng "Đã khai báo"',
       'Có ô Loại hợp đồng, Số hợp đồng, nút Tìm kiếm, Làm mới; chân "Hiển thị 1–10 / N" kèm Số dòng/trang']),
    C('Bấm vào dòng là thêm hợp đồng ngay', 'P0', 'Đang mở cửa sổ chọn hợp đồng của KH-1.',
      ['Bấm dòng HĐ-1', 'Bấm dòng HĐ-2', 'Bấm lại dòng HĐ-1', 'Bấm một dòng "Đã khai báo"', 'Đóng cửa sổ'], '',
      ['Mỗi lần bấm hiện "Đã thêm hợp đồng <số hợp đồng>", cửa sổ vẫn mở',
       'Dòng đã chọn chuyển "Đã chọn", bấm lại không thêm trùng; dòng "Đã khai báo" bấm không có tác dụng',
       'Bảng có đúng 2 dòng: Loại hợp đồng, Số hợp đồng tự điền (không sửa được), Loại dư mặc định "Dư nợ", Quá hạn chưa tích']),
    C('Cửa sổ chọn hợp đồng gộp đủ nguồn, đúng khách hàng', 'P0',
      'KH-1 có hợp đồng bán Đã duyệt, hợp đồng hãng Có hiệu lực, hợp đồng đầu kỳ do NGƯỜI KHÁC tạo, 1 hợp đồng mua của KH-1.',
      ['Mở cửa sổ, để trống Loại hợp đồng', 'Lần lượt chọn từng Loại hợp đồng', 'Mở cửa sổ tương ứng ở hệ thống cũ, để trống Loại hợp đồng'], '',
      ['Danh sách Loại: Hợp đồng hãng, Hợp đồng, Đơn hàng, Hợp đồng nguyên tắc, Hợp đồng thúc đẩy bán, Đơn hàng thúc đẩy bán, '
       'Phụ lục bổ sung, Phụ lục HĐNT, Hợp đồng gói dịch vụ, Hợp đồng dự án, Hợp đồng đầu kỳ, Hợp đồng mua nước ngoài, '
       'Hợp đồng mua ngoài, Hợp đồng mua trong nước',
       'Để trống Loại: gộp mọi nguồn, có cả hợp đồng đầu kỳ do người khác tạo và hợp đồng mua của KH-1; mọi dòng thuộc KH-1',
       'Hệ thống cũ để trống chỉ ra hợp đồng bán: hệ thống mới đã sửa (V1, V2), ghi kết quả theo hệ thống mới']),
    C('Cửa sổ chọn hợp đồng không hiện hợp đồng hết hiệu lực', 'P1',
      'KH-1 có 1 hợp đồng bán Đang tạo, 1 hợp đồng hãng đã thanh lý, 1 hợp đồng nguyên tắc của hãng.',
      ['Mở cửa sổ chọn hợp đồng, để trống Loại hợp đồng'], '',
      ['Không thấy 3 hợp đồng trên']),
    C('Lọc và phân trang trong cửa sổ chọn hợp đồng', 'P1', 'KH-1 có hơn 10 hợp đồng.',
      ['Ô Loại hợp đồng chọn "Hợp đồng đầu kỳ"', 'Ô Số hợp đồng gõ "KLM", nhấn Enter', 'Bấm Làm mới', 'Sang trang 2, đổi Số dòng/trang'], '',
      ['Chỉ còn hợp đồng đúng loại / chứa chuỗi', 'Làm mới về toàn bộ hợp đồng của khách hàng',
       'STT trang 2 nối tiếp trang 1; đổi số dòng về trang 1; không có kết quả thì ghi "Không có dữ liệu phù hợp."']),
    C('Thêm mới thành công với nhiều hợp đồng', 'P0', 'Đã chọn HĐ-1, HĐ-2 của KH-1.',
      ['Dòng 1: Tài khoản 1311, Dư nợ, Công nợ 1,500,000, tích Quá hạn, Ngày BGNT 30/09/2026',
       'Dòng 2: Tài khoản đã tự điền theo dòng 1, đổi Dư có, Công nợ 5', 'Bấm Lưu'],
      ['Dòng 1: ' + TK + ' / Dư nợ / 1,500,000 / Quá hạn / 30/09/2026', 'Dòng 2: ' + TK + ' / Dư có / 5'],
      ['Thông báo "Thêm mới thành công.", quay về danh sách (hệ thống cũ báo "Thêm công nợ thành công!": ' + CHOT + ' K4)',
       'Có 2 khai báo mới, mã dạng TPE.CNĐKHĐ.<5 chữ số> nối tiếp; dòng 1 Quá hạn "Có", Ngày BGNT 30/09/2026',
       'Lịch sử mỗi khai báo có 1 dòng "Tạo mới" của TK-A']),
    C('Thêm mới chỉ nhập trường bắt buộc', 'P0', 'Đã chọn HĐ-2 của KH-1, không tích Quá hạn.',
      ['Chọn Tài khoản, nhập Công nợ, giữ Loại dư mặc định', 'Bấm Lưu'], ['Tài khoản: ' + TK, 'Công nợ: 2,000,000'],
      ['"Thêm mới thành công."; khai báo mới Dư nợ 2,000,000, Quá hạn "Không", Ngày BGNT trống']),
    C('Chưa chọn hợp đồng hoặc bỏ trống trường bắt buộc thì bị chặn', 'P0', 'Đã chọn KH-1.',
      ['Chưa chọn hợp đồng nào, bấm Lưu', 'Chọn 2 hợp đồng, không nhập Tài khoản, Công nợ, bấm Lưu'], '',
      ['Bước 1: "' + CHUA_DU + '"; dưới bảng hợp đồng báo đỏ "Phải chọn ít nhất 1 hợp đồng"',
       'Bước 2: "' + CHUA_DU + '"; dưới ô Tài khoản và Công nợ của TỪNG dòng báo "Bắt buộc phải nhập", cùng một lượt',
       'Màn cuộn tới ô lỗi đầu tiên; dữ liệu đã nhập còn nguyên; không tạo khai báo nào']),
    C('Công nợ phải là số lớn hơn 0', 'P0', 'Đã chọn 1 hợp đồng, đã chọn Tài khoản.',
      ['Gõ chữ "abc" và dấu âm "-100" vào ô Công nợ', 'Gõ 1500000.5', 'Đổi thành 0, bấm Lưu'], '',
      ['Không gõ được chữ và dấu âm', 'Số tự hiện "1,500,000.5"', 'Công nợ 0: dưới ô báo "Phải lớn hơn 0.", không tạo khai báo']),
    C('Thông báo lỗi mất ngay khi nhập lại đúng', 'P1', 'Vừa bấm Lưu, ô Tài khoản và Công nợ dòng 1, dòng 2 đang báo đỏ.',
      ['Chọn Tài khoản dòng 1', 'Nhập Công nợ 1,000,000 dòng 1'], '',
      ['Lỗi dưới từng ô của dòng 1 mất ngay, không cần bấm Lưu lại', 'Lỗi của dòng 2 vẫn giữ']),
    C('Quá hạn và Ngày BGNT', 'P0', 'Đã chọn 1 hợp đồng.',
      ['Loại dư = Dư có, thử tích Quá hạn', 'Đổi Dư nợ, tích Quá hạn', 'Mở ô Ngày BGNT, thử chọn ngày mai',
       'Bỏ trống Ngày BGNT, bấm Lưu', 'Chọn 30/09/2026, đổi Loại dư sang Dư có'], '',
      ['Bước 1: ô Quá hạn khóa khi Dư có', 'Bước 2: hiện ô Ngày BGNT', 'Bước 3: ngày sau hôm nay không chọn được',
       'Bước 4: dưới ô Ngày BGNT "Bắt buộc phải nhập", thông báo "' + CHUA_DU + '"', 'Bước 5: tự bỏ tích Quá hạn và xóa Ngày BGNT']),
    C('Tài khoản dòng sau lấy theo dòng trên', 'P2', 'Đã chọn HĐ-1, dòng 1 chọn tài khoản 1311.',
      ['Mở cửa sổ, chọn thêm HĐ-2', 'Đóng cửa sổ'], '',
      ['Dòng 2 có sẵn Tài khoản 1311, Loại dư Dư nợ, Công nợ trống']),
    C('Xóa dòng và đổi khách hàng', 'P1', 'Đã chọn 3 hợp đồng của KH-1, dòng 3 đang báo lỗi.',
      ['Bấm nút xóa ở dòng 1', 'Đổi ô Khách hàng sang khách hàng khác'], '',
      ['Bước 1: còn 2 dòng, lỗi vẫn nằm đúng dòng (nay là dòng 2); hợp đồng vừa xóa chọn lại được',
       'Bước 2: bảng hợp đồng về trống, ghi "Chưa chọn hợp đồng nào — bấm "Chọn hợp đồng" để thêm."']),
    C('Lưu và tiếp tục', 'P1', 'Đã chọn HĐ-2 của KH-1, nhập đủ.',
      ['Bấm "Lưu và tiếp tục"', 'Bấm Quay lại ngay, chưa nhập gì thêm', 'Thử lại với 1 dòng thiếu Công nợ'], '',
      ['"Thêm mới thành công."; ở lại trang thêm mới, ô Khách hàng và bảng về trống; danh sách có khai báo vừa lưu',
       'Quay lại ngay: về danh sách, KHÔNG hỏi "Thông tin chưa lưu"',
       'Thiếu Công nợ: "' + CHUA_DU + '", dưới ô "Bắt buộc phải nhập", không tạo khai báo']),
    C('Quay lại khi chưa nhập và khi đã nhập', 'P1', 'Vừa mở trang thêm mới.',
      ['Bấm Quay lại khi chưa nhập gì', 'Mở lại, chọn KH-1 và 1 hợp đồng, nhập Công nợ, bấm Quay lại', 'Bấm Ở lại', 'Bấm Quay lại lần nữa, bấm Thoát'], '',
      ['Chưa nhập: về danh sách ngay, không hỏi', 'Đã nhập: ' + UNSAVED,
       'Ở lại: vẫn ở trang, dữ liệu giữ nguyên', 'Thoát: về danh sách, không lưu khai báo nào']),
    C('Bấm Lưu liên tục', 'P1', 'Đã chọn HĐ-2 của KH-1, nhập đủ.',
      ['Bấm Lưu 3 lần liền thật nhanh', 'Thử lại khi còn bỏ trống Công nợ, bấm Lưu 3 lần'], '',
      ['Dữ liệu hợp lệ: chỉ tạo ĐÚNG 1 khai báo, 1 thông báo "Thêm mới thành công."',
       'Còn lỗi: chỉ còn 1 thông báo "' + CHUA_DU + '" trên màn, không xếp chồng 3 cái']),
    C('Hai người cùng khai báo trùng hợp đồng và tài khoản', 'P0', '2 người cùng mở trang thêm mới, cùng chọn HĐ-1 + tài khoản 1311 của KH-1.',
      ['Người thứ nhất bấm Lưu', 'Người thứ hai bấm Lưu'], '',
      ['Người thứ nhất lưu thành công',
       'Người thứ hai: dưới ô Tài khoản "' + DUP + '", không lưu dòng nào trong lần đó']),
    C('Khai báo lập ở hệ thống mới hiện đúng ở hệ thống cũ', 'P0', 'Vừa lập ở hệ thống mới 2 khai báo như case "Thêm mới thành công với nhiều hợp đồng".',
      ['Mở ' + E_MENU, 'Lọc Khách hàng = KH-1', 'Đối chiếu từng cột của 2 dòng'], '',
      ['Có 2 dòng với cùng Mã, Tài khoản ' + TK + ', Khách hàng "' + KH + '", Loại hợp đồng, Mã hợp đồng',
       'Dòng 1: Dư nợ 1,500,000, Quá hạn "Có", Ngày BGNT 30/09/2026; dòng 2: Dư có 5',
       'Người tạo là TK-A, Ngày tạo cùng thời điểm (cũ có giây)', 'Mở Sửa ở hệ thống cũ: ô Quá hạn đã tích, Ngày BGNT đúng ngày']),
    C('Khai báo lập ở hệ thống cũ hiện đúng ở hệ thống mới', 'P0', 'KH-1 có HĐ-3 chưa khai báo.',
      ['Ở hệ thống cũ thêm khai báo KH-1 + HĐ-3 + 1311, Dư nợ 3,750,000, quá hạn, Ngày BGNT 15/09/2026', 'Ở hệ thống mới tìm theo Mã vừa sinh',
       'Mở chi tiết, bật cột Tài khoản, Loại hợp đồng'], ['Công nợ: 3,750,000', 'Ngày BGNT: 15/09/2026'],
      ['Dòng có đủ: Khách hàng, Số hợp đồng HĐ-3, Loại hợp đồng, Tài khoản ' + TK + ', Dư nợ 3,750,000, Quá hạn "Có", Ngày BGNT 15/09/2026',
       'Người tạo đúng người lập ở hệ thống cũ; nút Sửa, Xóa có (chưa phát sinh)',
       'Cửa sổ chọn hợp đồng của KH-1 ở hệ thống mới: HĐ-3 hiện "Đã khai báo"']),
    C('Lập xen kẽ ở 2 hệ thống không trùng mã phiếu', 'P0', 'Cùng công ty TPE; KH-1 còn 4 hợp đồng chưa khai báo.',
      ['Lập 1 khai báo ở hệ thống mới', 'Lập 1 khai báo ở hệ thống cũ', 'Lập tiếp 1 ở hệ thống mới, 1 ở hệ thống cũ', 'Lọc KH-1 ở cả 2 hệ thống'], '',
      ['4 khai báo có 4 mã khác nhau, cùng tiền tố TPE.CNĐKHĐ.', 'Không lần lưu nào báo lỗi trùng mã',
       'Số sau tiền tố có thể không liền nhau (mỗi hệ thống đánh số một cách): ' + CHOT + ' K5']),
    C('Ngày hạch toán khai báo theo cấu hình công ty người lập', 'P1',
      'Công ty TPE cấu hình Ngày khai báo đầu kỳ ' + NGAY_DK + '; công ty khác (vd ETEK GREEN) cấu hình 30/06/2025; TK-A thuộc TPE, TK-B thuộc ETEK GREEN.',
      ['TK-A lập khai báo X ở hệ thống mới', 'TK-B lập khai báo W ở hệ thống cũ', 'Mở ' + BC + ', Thời gian 01/01/2025 – 31/12/2025 cho khách của X và W'], '',
      ['X được tính theo ngày ' + NGAY_DK + ', W theo ngày 30/06/2025 (cùng nguyên tắc ở 2 hệ thống)',
       'Đổi cấu hình một công ty không làm đổi ngày của khai báo công ty kia']),
]

# =============================================================== IV. CHỈNH SỬA
S_SUA = [
    C('Mở trang sửa', 'P0', 'Khai báo Z chưa phát sinh chứng từ.',
      ['Bấm Sửa ở dòng Z', 'Quan sát trang'], '',
      ['Tiêu đề "Sửa khai báo đầu kỳ công nợ"; mọi ô điền sẵn đúng dữ liệu hiện tại của Z',
       'Mã phiếu, Khách hàng, Loại hợp đồng, Số hợp đồng khóa; Tài khoản, Loại dư, Công nợ, Quá hạn, Ngày BGNT sửa được',
       'Bảng đúng 1 dòng; KHÔNG có nút Chọn hợp đồng, nút xóa dòng, Lưu và tiếp tục; chân trang Lưu, Quay lại']),
    C('Sửa Công nợ và lưu thành công', 'P0', 'Khai báo Z Dư nợ 1,500,000.',
      ['Mở trang sửa Z', 'Đổi Công nợ thành 1,800,000', 'Bấm Lưu'], 'Công nợ: 1,800,000',
      ['"Cập nhật thành công.", về danh sách; dòng Z Dư nợ 1,800,000',
       'Người cập nhật = người sửa, Ngày cập nhật = lúc lưu; Người tạo, Ngày tạo giữ nguyên']),
    C('Sửa nhiều trường cùng lúc', 'P0', 'Khai báo Z Dư nợ 1,500,000, Quá hạn, Ngày BGNT 30/09/2026.',
      ['Mở trang sửa Z', 'Đổi Loại dư sang Dư có, Công nợ 2,750,000.5', 'Bấm Lưu'], ['Loại dư: Dư có', 'Công nợ: 2,750,000.5'],
      ['"Cập nhật thành công."; danh sách: Dư có 2,750,000.5, Dư nợ trống', 'Quá hạn tự về "Không", Ngày BGNT trống']),
    C('Giữ nguyên dữ liệu rồi bấm Lưu', 'P1', 'Khai báo Z có 2 dòng lịch sử.',
      ['Mở trang sửa Z, không đổi gì, bấm Lưu'], '',
      ['"Cập nhật thành công.", dữ liệu không đổi, không bị chặn vì "trùng" với chính nó', 'Lịch sử của Z vẫn 2 dòng']),
    C('Để trống hoặc nhập 0 ở Công nợ khi sửa', 'P0', 'Đang ở trang sửa Z.',
      ['Xóa trống Công nợ, bấm Lưu', 'Nhập 0, bấm Lưu'], '',
      ['Trống: "' + CHUA_DU + '", dưới ô "Bắt buộc phải nhập"', 'Bằng 0: dưới ô "Phải lớn hơn 0."', 'Không lưu; lỗi mất ngay khi nhập lại số hợp lệ']),
    C('Sửa sang tài khoản đã khai báo cho cùng hợp đồng', 'P1', 'HĐ-1 của KH-1 có khai báo Z (1311) và khai báo Z2 (1312, lập bằng Import).',
      ['Sửa Z2, đổi Tài khoản sang 1311', 'Bấm Lưu'], '',
      ['Dưới ô Tài khoản: "' + DUP + '"', 'Không lưu']),
    C('Tích Quá hạn khi sửa mà bỏ trống Ngày BGNT', 'P1', 'Khai báo Z Dư nợ, chưa quá hạn.',
      ['Tích Quá hạn, bấm Lưu', 'Chọn Ngày BGNT 30/09/2026, bấm Lưu'], '',
      ['Bước 1: dưới ô Ngày BGNT "Bắt buộc phải nhập", không lưu', 'Bước 2: lưu được, Quá hạn "Có", Ngày BGNT 30/09/2026']),
    C('Quay lại khi chưa đổi, đổi rồi trả lại, và khi đã đổi', 'P1', 'Khai báo Z Công nợ 1,500,000.',
      ['Mở trang sửa, không đổi gì, bấm Quay lại', 'Mở lại, đổi Công nợ 2,000,000 rồi đổi về 1,500,000, bấm Quay lại',
       'Mở lại, đổi Công nợ, bấm Quay lại, bấm Ở lại', 'Bấm Quay lại, bấm Thoát'], '',
      ['Hai lần đầu: về ngay, không hỏi', 'Đã đổi: ' + UNSAVED + '; Ở lại thì giá trị đang sửa còn nguyên',
       'Thoát: Công nợ của Z vẫn 1,500,000, Lịch sử không có dòng mới']),
    C('Vào thẳng trang sửa của khai báo đã phát sinh chứng từ', 'P0', 'Khai báo Y đã phát sinh chứng từ.',
      ['Dán đường dẫn trang sửa của Y lên thanh địa chỉ'], '',
      ['Thông báo "Khai báo đã phát sinh chứng từ hoặc bạn không có quyền sửa."', 'Tự chuyển về trang chi tiết của Y']),
    C('Khai báo vừa phát sinh chứng từ trong lúc đang sửa', 'P1', 'A đang mở trang sửa Z; B lập phiếu thu ghi sổ cho KH-1 + HĐ-1 + 1311.',
      ['A đổi Công nợ, bấm Lưu'], '',
      ['A bị chặn, báo "' + USED + '"', 'Dữ liệu Z không đổi']),
    C('Sửa khai báo đã bị người khác xóa', 'P1', 'A đang mở trang sửa Z; B xóa Z.',
      ['A đổi Công nợ, bấm Lưu', 'A quay lại danh sách'], '',
      ['A nhận thông báo lỗi, không lưu được, không tạo lại Z', 'Danh sách không còn Z']),
    C('Sửa ở hệ thống mới thì hệ thống cũ thấy đúng', 'P0', 'Khai báo Z Dư nợ 1,500,000, tài khoản 1311.',
      ['Ở hệ thống mới sửa Z: Tài khoản 1312, Công nợ 1,800,000, bấm Lưu', 'Ở hệ thống cũ tìm Z theo Mã', 'Mở Sửa Z ở hệ thống cũ (không lưu)'],
      ['Tài khoản: ' + TK2, 'Công nợ: 1,800,000'],
      ['Hệ thống cũ: Tài khoản "' + TK2 + '", Dư nợ 1,800,000; Người sửa, Ngày sửa đúng người và lúc sửa ở hệ thống mới',
       'Cửa sổ Sửa ở hệ thống cũ hiện đúng giá trị mới']),
    C('Sửa ở hệ thống cũ thì hệ thống mới thấy đúng', 'P0', 'Khai báo Z chưa phát sinh, Dư nợ 1,500,000.',
      ['Ở hệ thống cũ sửa Z: Loại dư Dư có, Công nợ 7,350,000', 'Ở hệ thống mới tải lại danh sách, tìm Z', 'Mở chi tiết và Lịch sử của Z'],
      ['Loại dư: Dư có', 'Công nợ: 7,350,000'],
      ['Dòng Z: Dư có 7,350,000, Dư nợ trống, Quá hạn "Không"; Người cập nhật là người sửa ở hệ thống cũ',
       'Lịch sử KHÔNG có dòng cho lần sửa ở hệ thống cũ: ' + CHOT + ' K8']),
    C('Hệ thống cũ vẫn sửa được khai báo đã phát sinh', 'P1', 'Khai báo Y đã phát sinh (hệ thống mới không có Sửa).',
      ['Ở hệ thống cũ mở Sửa Y, đổi Công nợ, lưu', 'Ở hệ thống mới tải lại, xem Y'], '',
      ['Hệ thống cũ cho lưu: ' + CHOT + ' (K3)', 'Hệ thống mới hiện giá trị mới của Y, vẫn KHÔNG có Sửa / Xóa']),
]

# =============================================================== V. XÓA
S_XOA = [
    C('Hộp xác nhận xóa và nút Hủy', 'P0', 'Khai báo Z chưa phát sinh chứng từ.',
      ['Bấm Xóa ở dòng Z', 'Đọc nội dung hộp', 'Bấm Hủy'], '',
      ['Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa bản ghi này không?", 2 nút Xóa và Hủy',
       'Bấm Hủy: hộp đóng, Z vẫn còn, tổng không đổi']),
    C('Xóa thành công khai báo chưa phát sinh', 'P0', 'Khai báo Z chưa phát sinh. Phạm vi có N khai báo.',
      ['Bấm Xóa ở dòng Z, bấm Xóa trong hộp', 'Đọc dòng tổng'], '',
      ['"Xóa thành công.", dòng Z biến mất', 'Dòng tổng "… / N-1"',
       'Làm lại với khai báo Z2 từ trang chi tiết (nút Xóa ở chân trang): "Xóa thành công.", về danh sách, Z2 không còn']),
    C('Không xóa được khai báo đã phát sinh chứng từ', 'P0', 'Khai báo Y đã phát sinh.',
      ['Tìm dòng Y ở danh sách', 'Mở chi tiết Y'], '',
      ['Không có nút Xóa ở cả 2 nơi']),
    C('Khai báo vừa phát sinh chứng từ khi đang xóa', 'P1', 'A đang thấy nút Xóa của Z; B lập phiếu thu ghi sổ cho KH-1 + HĐ-1 + 1311.',
      ['A bấm Xóa ở dòng Z, xác nhận'], '',
      ['A nhận thông báo "' + USED + '"', 'Z vẫn còn']),
    C('Xóa khai báo đã bị người khác xóa', 'P1', 'A và B cùng mở danh sách thấy Z.',
      ['B xóa Z', 'A (chưa tải lại) bấm Xóa ở dòng Z, xác nhận', 'A tải lại trang'], '',
      ['A nhận thông báo lỗi, không xóa thêm bản ghi nào khác', 'Sau tải lại, Z không còn']),
    C('Xóa ở hệ thống mới thì hệ thống cũ mất theo', 'P0', 'Khai báo Z chưa phát sinh, đang hiện ở cả 2 hệ thống.',
      ['Xóa Z ở hệ thống mới', 'Ở hệ thống cũ tìm theo Mã của Z', 'Ở hệ thống mới tạo mới, chọn KH-1, mở cửa sổ chọn hợp đồng'], '',
      ['Hệ thống cũ không còn Z', 'HĐ-1 không còn "Đã khai báo", chọn lại được']),
    C('Xóa ở hệ thống cũ thì hệ thống mới mất theo', 'P0', 'Khai báo W lập ở hệ thống mới, chưa phát sinh.',
      ['Ở hệ thống cũ xóa W ("Xóa công nợ thành công!")', 'Ở hệ thống mới tải lại danh sách, tìm W', 'Dán đường dẫn chi tiết W cũ'], '',
      ['Danh sách không còn W, tổng giảm 1', 'Đường dẫn cũ sang trang "Không tìm thấy", không treo']),
]

# =============================================================== VI. LỊCH SỬ THAY ĐỔI
S_LS = [
    C('Mở cửa sổ Lịch sử từ danh sách', 'P0', 'Khai báo Z đã được sửa ít nhất 1 lần.',
      ['Ở danh sách, mở menu ba chấm của dòng Z, bấm Lịch sử'], '',
      ['Cửa sổ "Lịch sử thay đổi: <mã Z>"', 'Có nút Bộ lọc và nút Đóng']),
    C('Lịch sử ngay sau khi tạo mới', 'P0', 'Vừa tạo khai báo Z, chưa sửa lần nào.',
      ['Mở Lịch sử của Z'], '',
      ['Có đúng 1 dòng "Tạo mới" kèm người thực hiện và thời điểm']),
    C('Mỗi dòng nêu đủ thông tin, mới nhất ở trên', 'P0', 'Z được sửa 3 lần; lần cuối đổi Công nợ 1,500,000 thành 1,800,000.',
      ['Mở Lịch sử của Z', 'Đọc thứ tự và dòng trên cùng'], '',
      ['Dòng trên cùng là lần sửa MỚI NHẤT, "Tạo mới" dưới cùng',
       'Dòng trên cùng: trường Công nợ, cũ 1,500,000.00 (đỏ), mới 1,800,000.00 (xanh), "Người thực hiện: <họ tên> — <phòng ban>", thời điểm tới phút']),
    C('Sửa nhiều trường chỉ sinh một dòng', 'P0', 'Khai báo Z Dư nợ 1,500,000.',
      ['Sửa Z: Loại dư Dư có, Công nợ 2,750,000.5, bấm Lưu', 'Mở Lịch sử, đọc dòng trên cùng'], '',
      ['Chỉ MỘT dòng "Thay đổi thông tin" liệt kê: Loại dư Dư nợ thành Dư có; Công nợ 1,500,000.00 thành 2,750,000.50']),
    C('Bộ lọc trong cửa sổ Lịch sử', 'P1', 'Z có dòng Tạo mới (TK-A) và Thay đổi thông tin (TK-ALL) ở nhiều ngày.',
      ['Bấm Bộ lọc', 'Chọn Loại hành động "Thay đổi thông tin"', 'Thêm Người thực hiện TK-A', 'Bấm Làm mới, rồi lọc Từ ngày – Đến ngày = ngày sửa gần nhất'], '',
      ['Có ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày', 'Lọc loại: chỉ còn dòng "Thay đổi thông tin"',
       'Kết hợp không có kết quả: báo không có dữ liệu, không lỗi', 'Làm mới về toàn bộ; lọc ngày chỉ còn dòng trong khoảng']),
    C('Lịch sử của khai báo import và khai báo lập ở hệ thống cũ', 'P1', 'Có khai báo W vừa import ở hệ thống mới và khai báo V lập ở hệ thống cũ.',
      ['Mở Lịch sử của W', 'Mở Lịch sử của V'], '',
      ['W: có dòng "Tạo mới", người thực hiện là tài khoản import',
       'V: không có dòng nào (hệ thống cũ không ghi lịch sử): ' + CHOT + ' K8']),
    C('Lịch sử xem ở trang chi tiết và đóng cửa sổ', 'P1', 'Danh sách đang lọc Loại dư = Dư nợ, ở trang 2; Z có ít nhất 2 dòng lịch sử.',
      ['Mở Lịch sử 1 dòng rồi bấm Đóng', 'Mở chi tiết Z, ở khối Lịch sử bấm "Xem lịch sử"'], '',
      ['Đóng: danh sách giữ bộ lọc và trang 2', 'Khối Lịch sử ở chi tiết đang thu gọn, bấm mới hiện, nội dung giống cửa sổ Lịch sử']),
]

# =============================================================== VII. XEM CHI TIẾT KHAI BÁO
S_CT = [
    C('Mở trang chi tiết bằng mã phiếu', 'P0', 'Có khai báo Z.',
      ['Bấm vào mã phiếu Z'], '',
      ['Tiêu đề "Chi tiết khai báo đầu kỳ công nợ: <mã Z>"; góc phải "<người tạo> - <ngày giờ tạo>"',
       'Khối Thông tin chung: Mã phiếu, Khách hàng; bảng đúng 1 dòng: Loại hợp đồng, Số hợp đồng, Tài khoản, Loại dư, Công nợ, Quá hạn, Ngày BGNT',
       'Mọi ô khóa; KHÔNG có Lưu, Lưu và tiếp tục, Chọn hợp đồng, nút xóa dòng; có khối "Lịch sử" thu gọn']),
    C('Dữ liệu chi tiết khớp danh sách và hệ thống cũ', 'P0', 'Khai báo Z như Test data, quá hạn, Ngày BGNT 30/09/2026.',
      ['Bật cột Tài khoản, Loại hợp đồng ở danh sách, đọc dòng Z', 'Mở chi tiết Z', 'Mở Sửa Z ở hệ thống cũ (không lưu)'],
      ['Khách hàng: ' + KH, 'Hợp đồng: ' + HD1, 'Tài khoản: ' + TK, 'Dư nợ 1,500,000'],
      ['Mã phiếu, Khách hàng, Loại hợp đồng, Số hợp đồng, Tài khoản, Loại dư, Công nợ, Quá hạn, Ngày BGNT trùng khớp ở cả 3 nơi']),
    C('Nút ở chân trang chi tiết theo tình trạng chứng từ', 'P0', 'Khai báo Z chưa phát sinh, khai báo Y đã phát sinh.',
      ['Mở chi tiết Z, xem chân trang', 'Mở chi tiết Y, xem chân trang'], '',
      ['Z: Sửa, Xóa, Quay lại — giống nút ở dòng danh sách', 'Y: chỉ Quay lại; dữ liệu vẫn xem đầy đủ']),
    C('Quay lại từ trang chi tiết giữ bộ lọc', 'P1', 'Danh sách đang lọc Loại dư = Dư nợ.',
      ['Bấm mã phiếu một dòng', 'Bấm Quay lại'], '',
      ['Danh sách vẫn giữ Loại dư = Dư nợ và kết quả cũ']),
]

# =============================================================== VIII. IN PHIẾU (IN DANH SÁCH)
S_IN = [
    C('In danh sách theo bộ lọc, cùng mẫu với hệ thống cũ', 'P0', 'Đang lọc từ khóa "75TPHXCH-2" (12 khai báo, 2 trang).',
      ['Bấm In danh sách', 'Đọc bản xem trước', 'Bấm In', 'In cùng bộ lọc ở hệ thống cũ để so'], '',
      ['Cửa sổ "Xem trước khai báo đầu kỳ công nợ" khổ ngang, tiêu đề công ty người đăng nhập, tiêu đề in đậm "Công nợ đầu kỳ theo khách hàng - hợp đồng"',
       'Đủ 12 dòng (mọi trang), đúng các cột đang hiện, không có Hành động; số lẻ giữ phần lẻ (2,750,000.5)',
       'Cùng biểu mẫu với bản in hệ thống cũ, cùng số dòng; In mở hộp in của trình duyệt',
       'Bật thêm cột Tài khoản rồi in lại: bản in có thêm cột Tài khoản, đúng thứ tự cột như trên bảng']),
    C('In danh sách quá 2,000 dòng', 'P1', 'TK-ALL, không lọc gì, phạm vi hơn 2,000 khai báo.',
      ['Bấm In danh sách'], '',
      ['Không in; báo "Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được…" kèm gợi ý thu hẹp bộ lọc']),
]

# =============================================================== IX. TÙY CHỈNH CỘT
S_COT = [
    C('Mở cửa sổ Tuỳ chỉnh cột', 'P1', 'Tài khoản chưa từng tùy chỉnh cột.',
      ['Bấm nút Cấu hình cột hiển thị cạnh In danh sách'], '',
      ['Cửa sổ "Tuỳ chỉnh cột" liệt kê 15 cột, tích sẵn 11 cột mặc định, ghi "Đang chọn 11/15 cột"', 'Có nút Lưu, Đóng']),
    C('Bật / tắt cột và cột bắt buộc', 'P1', 'Đang mở cửa sổ Tuỳ chỉnh cột.',
      ['Tích Tài khoản, Loại hợp đồng; bỏ tích Người tạo; kéo Dư có lên trên Dư nợ; bấm Lưu', 'Mở lại, thử bỏ tích STT, Mã phiếu, Hành động',
       'Cuộn ngang bảng sang phải'], '',
      ['Bảng hiện thêm Tài khoản, Loại hợp đồng với dữ liệu đúng; Người tạo biến mất; Dư có đứng trước Dư nợ',
       'STT, Mã phiếu, Hành động có biểu tượng khóa, không bỏ tích được', 'STT và Mã phiếu luôn đứng yên bên trái khi cuộn']),
    C('Ghi nhớ cấu hình, đóng không lưu, riêng từng tài khoản', 'P2', 'TK-A đã bật cột Tài khoản và Lưu; TK-ALL chưa tùy chỉnh.',
      ['TK-A nhấn F5, rời màn rồi vào lại', 'TK-A mở cửa sổ, bỏ tích Người tạo, bấm Đóng', 'Đăng nhập TK-ALL, vào màn'], '',
      ['TK-A vẫn thấy cột Tài khoản; bấm Đóng thì Người tạo vẫn hiện', 'TK-ALL thấy bộ cột mặc định',
       'Đổi cấu hình cột không làm đổi bộ lọc, tổng số hay dữ liệu']),
]

# =============================================================== X. XUẤT DANH SÁCH EXCEL
S_XUAT = [
    C('Mở cửa sổ chọn trường xuất file', 'P0', 'Đang ở màn danh sách, chưa tùy chỉnh cột.',
      ['Bấm Xuất Excel'], '',
      ['Cửa sổ "Chọn trường xuất file" liệt kê 13 trường: Mã phiếu, Khách hàng, Tài khoản, Loại hợp đồng, Số hợp đồng, Dư nợ, '
       'Dư có, Quá hạn, Ngày BGNT, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật',
       'Trường đang hiện trên bảng được tích sẵn, ghi "Đang chọn x/13 trường"; có Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng']),
    C('Xuất file theo bộ lọc, đủ mọi trang', 'P0', 'Đang lọc Loại dư = Dư có, Tài khoản 1311: 35 khai báo (4 trang), đang ở trang 1.',
      ['Bấm Xuất Excel, Xuất file', 'Mở file tải về'], '',
      ['Cạnh nút có dòng tiến độ; xong báo "Xuất Excel thành công"',
       'File khai_bao_dau_ky_cong_no.xlsx, tiêu đề "DANH SÁCH CÔNG NỢ ĐẦU KỲ THEO KHÁCH HÀNG - HỢP ĐỒNG"',
       'Đủ 35 dòng (không chỉ trang đang xem), chỉ khai báo Dư có 1311, cột Dư nợ trống ở mọi dòng']),
    C('Chọn tất cả, bỏ tích, kéo đổi thứ tự trường', 'P1', 'Đang mở cửa sổ chọn trường.',
      ['Bấm Chọn tất cả, Xuất file', 'Mở lại, bỏ tích Người tạo, kéo Dư có lên trên Dư nợ, Xuất file', 'Bấm Bỏ chọn hết'], '',
      ['File 1 đủ 13 cột', 'File 2 không có Người tạo, Dư có đứng trước Dư nợ', 'Bỏ chọn hết: "Đang chọn 0/13 trường", nút Xuất file mờ',
       'Lọc từ khóa "KHONG-TON-TAI" rồi xuất: báo "Không có dữ liệu để xuất", không tải file']),
    C('Dữ liệu trong file khớp hệ thống và file của hệ thống cũ', 'P0', 'Lọc KH-1: có khai báo Dư có 2,750,000.5 và khai báo quá hạn.',
      ['Xuất file đủ trường ở hệ thống mới', 'Xuất cùng bộ lọc ở hệ thống cũ', 'Đối chiếu từng ô'], '',
      ['Giá trị từng ô khớp danh sách; tên tiếng Việt, ký tự đặc biệt trong số hợp đồng hiện đúng',
       'Dư nợ / Dư có là SỐ (cộng tổng được), dạng 1,234,567; ô không có số để trống; Ngày BGNT dd/mm/yyyy',
       'Cùng số dòng, cùng số tiền với file hệ thống cũ; khác tên file, khác cột chọn được: ' + CHOT + ' K7']),
]

# =============================================================== XI. IMPORT TỪ FILE EXCEL
S_IMP = [
    C('Mở cửa sổ Import và tải file mẫu', 'P0', 'TK-A đang ở màn danh sách.',
      ['Bấm Import Excel', 'Bấm "Tải file mẫu", mở file'], '',
      ['Cửa sổ "Import khai báo đầu kỳ công nợ" có Tải file mẫu, ô chọn file, nút "Load lên bảng"',
       'File Mau_import_cong_no_dau_ky_khach_hang.xlsx: STT, Mã khách hàng *, Mã hợp đồng *, Loại hợp đồng *, Số tài khoản *, Loại dư, '
       'Công nợ *, Công nợ quá hạn, Ngày bàn giao nghiệm thu',
       'Hàng 1 là tiêu đề, KHÔNG có dòng mô tả; Loại hợp đồng và Loại dư bấm ra danh sách chọn',
       'File mẫu hệ thống cũ có 3 dòng tiêu đề, Loại hợp đồng không bắt buộc: ' + CHOT + ' K6']),
    C('Tải lên file sai định dạng hoặc không hợp lệ', 'P1', 'Có file .pdf, file .csv, file chỉ có tiêu đề, file 501 dòng.',
      ['Lần lượt chọn từng file, bấm "Load lên bảng"'], '',
      ['.pdf / .csv: "Vui lòng chọn file .xlsx hoặc .xls"', 'Chỉ tiêu đề: "Không có dòng dữ liệu hợp lệ."',
       '501 dòng: "File có 501 dòng dữ liệu, vượt quá giới hạn 500 dòng mỗi lần import. Vui lòng tách file và import nhiều lần."']),
    C('Tải lên file đúng mẫu, có dòng trống xen giữa', 'P1', 'File đúng mẫu 3 dòng hợp lệ, giữa dòng 1 và 2 có 1 dòng trống.',
      ['Chọn file, bấm "Load lên bảng"'], '',
      ['Bảng xem trước đủ 3 dòng, đúng cột; dòng trống bị bỏ qua', 'Nút Validate, Bỏ dòng lỗi, Import hiện khi có dữ liệu']),
    C('Kiểm tra dữ liệu: bỏ trống và sai định dạng', 'P0', 'File 4 dòng: 1 đúng, 1 sai mọi cột, 1 trống Mã khách hàng, 1 quá hạn thiếu ngày bàn giao nghiệm thu.',
      ['Load lên bảng', 'Bấm Validate'], '',
      ['"Validate xong: 1 hợp lệ, 3 không hợp lệ"; dòng đúng tô xanh, khóa',
       'Dòng sai: "Khách hàng – Mã không tồn tại trong hệ thống", "Loại hợp đồng – Chỉ nhận HDMNN / HDMN / HDMTN / HDDK / HDHNTDA / HDDV", '
       '"Số tài khoản – Không tồn tại trong hệ thống", "Loại dư – Chỉ nhận "Dư nợ" hoặc "Dư có"", "Công nợ – Phải lớn hơn 0."',
       'Trống mã: "Khách hàng – Bắt buộc phải nhập"; dòng quá hạn: "Ngày bàn giao nghiệm thu – Bắt buộc phải nhập"']),
    C('Kiểm tra dữ liệu: hợp đồng không tồn tại hoặc không thuộc khách hàng', 'P0',
      'File: 1 dòng mã hợp đồng không có thật; 1 dòng mã hợp đồng của khách hàng khác (đúng loại).',
      ['Load, Validate', 'Import cùng file ở hệ thống cũ (tham chiếu)'], '',
      ['"Mã hợp đồng – Không tồn tại trong hệ thống"', '"Mã hợp đồng – Không thuộc khách hàng này"',
       'Hệ thống cũ không kiểm hợp đồng thuộc khách hàng: hệ thống mới đã sửa (V4), ghi kết quả theo hệ thống mới']),
    C('Kiểm tra dữ liệu: tài khoản không phải tài khoản chi tiết', 'P1', 'File: 1 dòng Số tài khoản 131 (có tài khoản con), 1 dòng tài khoản đang khóa.',
      ['Load, Validate'], '',
      ['Cả 2 dòng: "Số tài khoản – Không được khai báo công nợ (tài khoản khoá hoặc không phải tài khoản chi tiết)"']),
    C('Kiểm tra dữ liệu: trùng trong file và trùng khai báo đã có', 'P1', 'File có 2 dòng cùng KH-1 + HĐ-2 + 1311 và 1 dòng KH-1 + HĐ-1 + 1311 (đã có khai báo Z).',
      ['Load, Validate'], '',
      ['Dòng thứ hai của cặp trùng: "Trùng với dòng 1 trong file"', 'Dòng HĐ-1: "' + DUP_IMP + '"']),
    C('Kiểm tra dữ liệu: mã loại hợp đồng, Loại dư để trống', 'P1', 'File dùng lần lượt HDDK, HDHNTDA, HDDV, HDMNN, HDMN, HDMTN và mã "ABC"; 1 dòng hợp lệ để trống Loại dư.',
      ['Load, Validate', 'Import dòng để trống Loại dư'], '',
      ['6 mã hợp lệ được nhận; "ABC" báo "Loại hợp đồng – Chỉ nhận …"',
       'Dòng trống Loại dư hợp lệ, sau Import là Dư nợ (hệ thống cũ báo lỗi: ' + CHOT + ' K6)']),
    C('Kiểm tra dữ liệu: cột quá hạn và ngày bàn giao nghiệm thu', 'P1',
      'File: dòng Dư có + quá hạn 2; dòng quá hạn 2 + 31/12/2099; dòng quá hạn "x"; dòng quá hạn 2 + 31/02/2026; dòng quá hạn 2 + 30/09/2026.',
      ['Load, Validate', 'Import dòng hợp lệ'], '',
      ['"Công nợ quá hạn – Chỉ công nợ "Dư nợ" mới được đánh dấu quá hạn"', '"Ngày bàn giao nghiệm thu – Không được lớn hơn ngày hiện tại"',
       '"Công nợ quá hạn – Chỉ nhận 1 (không) hoặc 2 (có)"', '"Ngày bàn giao nghiệm thu – Ngày không hợp lệ (dd/mm/yyyy)"',
       'Dòng cuối hợp lệ; sau Import khai báo Quá hạn "Có", Ngày BGNT 30/09/2026']),
    C('Kiểm tra dữ liệu: chữ thường, khoảng trắng, sửa dòng lỗi trên bảng', 'P2', 'File có mã khách hàng " 75tphxch-2 " và 1 dòng Công nợ 0.',
      ['Load, Validate', 'Sửa ô Công nợ dòng lỗi thành 1000000 trên bảng', 'Bấm Validate lại'], '',
      ['Mã có chữ thường / khoảng trắng 2 đầu được nhận là 75TPHXCH-2', 'Sau sửa, dòng Công nợ chuyển hợp lệ, số Hợp lệ / Lỗi cập nhật']),
    C('Import khi có cả dòng đúng và dòng sai', 'P0', 'Sau Validate file 4 dòng (1 đúng, 3 lỗi).',
      ['Quan sát nút Import', 'Bấm "Bỏ dòng lỗi"', 'Bấm Import', 'Import cùng file ở hệ thống cũ (tham chiếu)'], '',
      ['Còn dòng lỗi: nút Import mờ', 'Bỏ dòng lỗi: bảng chỉ còn dòng hợp lệ',
       'Import: "Import thành công 1 khai báo."; cửa sổ đóng, danh sách tải lại; khai báo mới có mã nối tiếp, lịch sử "Tạo mới"',
       'Hệ thống cũ có dòng lỗi thì không nhập dòng nào: ' + CHOT + ' K6']),
    C('Import khi tất cả dòng hợp lệ', 'P0', 'File 3 dòng hợp lệ (KH-1, HĐ-2 / HĐ-4 / HĐ-5, Dư nợ 3,000,000 / 1,250,000 / Dư có 750,000); phạm vi có N khai báo.',
      ['Load, Validate', 'Bấm Import'], '',
      ['"Import thành công 3 khai báo."', 'Danh sách tự tải lại, tổng N+3, 3 khai báo mới đứng đầu']),
    C('Dòng bị người khác khai báo trùng sau khi kiểm tra', 'P1', '2 tài khoản cùng Validate xong 1 file 3 dòng có KH-1 + HĐ-2 + 1311.',
      ['Người thứ nhất bấm Import', 'Người thứ hai bấm Import', 'Người thứ hai bấm Sao chép ở bảng kết quả'], '',
      ['Người thứ hai: "Import thành công 2/3 khai báo. 1 dòng lỗi bị bỏ qua."; cửa sổ KHÔNG đóng',
       'Bảng kết quả "Import xong: 2 dòng thành công, 1 dòng lỗi bị bỏ qua", cột Dòng trong file, mã, lý do "' + DUP_IMP + '"',
       'Sao chép được nội dung bảng; danh sách vẫn tải lại với 2 dòng đã nhập']),
    C('Import ở hệ thống cũ thì hệ thống mới thấy đúng', 'P0', 'File mẫu hệ thống cũ 2 dòng hợp lệ của KH-1 (HĐ-6 Dư nợ 1,250,000; HĐ-7 Dư có 625,000).',
      ['Import file ở hệ thống cũ ("Import thành công 2 bản ghi")', 'Ở hệ thống mới lọc KH-1', 'Mở cửa sổ chọn hợp đồng của KH-1 ở trang Tạo mới'], '',
      ['Có 2 khai báo mới đúng Số hợp đồng, Tài khoản, Dư nợ 1,250,000 / Dư có 625,000, Người tạo là người import',
       'HĐ-6, HĐ-7 hiện "Đã khai báo" trong cửa sổ chọn hợp đồng']),
    C('Import ở hệ thống mới thì hệ thống cũ thấy đúng', 'P1', 'Vừa import ở hệ thống mới 3 dòng như case "Import khi tất cả dòng hợp lệ".',
      ['Ở hệ thống cũ lọc KH-1', 'Đối chiếu Mã, Mã hợp đồng, Tài khoản, Dư nợ / Dư có, Quá hạn'], '',
      ['Đủ 3 dòng, cùng mã phiếu và cùng số liệu với hệ thống mới']),
    C('Cùng hợp đồng khai báo thêm tài khoản khác', 'P1', 'HĐ-1 của KH-1 đã có khai báo Z (tài khoản 1311).',
      ['Ở hệ thống mới import 1 dòng KH-1 + HĐ-1 + tài khoản 1312, Dư nợ 500,000', 'Ở hệ thống cũ thêm khai báo cùng HĐ-1 + 1312'], '',
      ['Hệ thống mới: dòng hợp lệ, import được (chặn trùng theo khách hàng + hợp đồng + tài khoản)',
       'Hệ thống cũ: báo "' + DUP_ERP + '"', CHUA_CHOT + ' (L1)']),
    C('Import hợp đồng hãng không còn hiệu lực hoặc hợp đồng nguyên tắc của hãng', 'P1',
      'KH-1 có 1 hợp đồng hãng đã thanh lý và 1 hợp đồng nguyên tắc của hãng, cả 2 chưa khai báo.',
      ['Import 2 dòng mã loại HDHNTDA cho 2 hợp đồng trên ở hệ thống mới', 'Import cùng file ở hệ thống cũ'], '',
      ['Hệ thống cũ từ chối: "Hợp đồng không ở trạng thái "Có hiệu lực" — chỉ được khai báo công nợ đầu kỳ cho hợp đồng đang có hiệu lực" '
       'và "Không khai báo công nợ đầu kỳ cho Hợp đồng nguyên tắc (HĐNT)"',
       'Hệ thống mới PHẢI báo lỗi 2 dòng và không nhập (cửa sổ chọn hợp đồng cũng không cho chọn 2 hợp đồng này)',
       CHUA_CHOT + ' (L2) — nếu hệ thống mới nhập được thì ghi Failed']),
]

# =============================================================== XII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S_RB = [
    C('Kỳ báo cáo sau ngày khai báo đầu kỳ: vào Số dư đầu kỳ', 'P0',
      'Ngày khai báo đầu kỳ của TPE = ' + NGAY_DK + '. HĐ-2 của KH-1 chưa khai báo, chưa có chứng từ.',
      ['Mở ' + BC + ', Thời gian 01/01/2026 – 31/10/2026, Khách hàng KH-1, ghi số dòng HĐ-2', 'Lập khai báo HĐ-2 + 1311 Dư nợ 1,500,000', 'Tải lại báo cáo'],
      ['Thời gian: 01/01/2026 – 31/10/2026', 'Công nợ: 1,500,000'],
      ['Dòng HĐ-2: Số dư đầu kỳ TĂNG 1,500,000; Số dư cuối kỳ tăng 1,500,000',
       'Hàng hóa/Dịch vụ và Đã thanh toán của HĐ-2 KHÔNG đổi']),
    C('Kỳ báo cáo chứa ngày khai báo đầu kỳ: vào phát sinh trong kỳ', 'P0',
      'Khai báo HĐ-2 Dư nợ 1,500,000 (từ case trước) và khai báo HĐ-3 Dư có 625,000 của KH-1.',
      ['Mở ' + BC + ', Thời gian 01/12/2025 – 31/12/2025, Khách hàng KH-1'], 'Thời gian: 01/12/2025 – 31/12/2025',
      ['HĐ-2: Hàng hóa/Dịch vụ có 1,500,000, Số dư đầu kỳ không gồm khoản này',
       'HĐ-3: Đã thanh toán có 625,000', 'Kỳ 01/11/2025 – 30/11/2025 (trước ngày khai báo): không có 2 khoản này']),
    C('Sửa, xóa khai báo thì báo cáo cập nhật, khớp báo cáo hệ thống cũ', 'P0', 'Khai báo HĐ-2 Dư nợ 1,500,000; báo cáo kỳ 01/01/2026 – 31/10/2026.',
      ['Sửa Công nợ thành 1,800,000, tải lại báo cáo', 'Mở báo cáo chi tiết công nợ khách hàng ở hệ thống cũ cùng kỳ, cùng khách', 'Xóa khai báo, tải lại cả 2 báo cáo'], '',
      ['Sau sửa: Số dư đầu kỳ HĐ-2 = 1,800,000 ở cả 2 hệ thống', 'Sau xóa: HĐ-2 không còn số dư đầu kỳ ở cả 2 hệ thống']),
    C('Đổi Loại dư, đổi tài khoản thì số dư chuyển theo', 'P1', 'Khai báo Z Dư nợ 1,500,000 tài khoản 1311; báo cáo kỳ 01/01/2026 – 31/10/2026.',
      ['Sửa Z sang Dư có 1,500,000, tải lại báo cáo', 'Sửa Z sang tài khoản không thuộc nhóm 131 (vd 3388), tải lại báo cáo'], '',
      ['Dư có: Số dư đầu kỳ HĐ-1 giảm 3,000,000 so với lúc Dư nợ (từ +1,500,000 thành -1,500,000)',
       'Tài khoản ngoài nhóm 131: khoản này KHÔNG còn trên báo cáo công nợ khách hàng']),
    C('Báo cáo Tổng hợp theo NV và Đối chiếu 1 KH cũng đổi theo', 'P1', 'Vừa lập khai báo HĐ-2 Dư nợ 1,500,000; NVKD của HĐ-2 là nhân viên E.',
      ['Mở ' + BC_NV + ', kỳ 01/01/2026 – 31/10/2026', 'Mở ' + BC_DC + ', khách KH-1, cùng kỳ'], '',
      ['Theo NV: dòng nhân viên E tăng số dư đầu kỳ 1,500,000', 'Đối chiếu 1 KH: số dư đầu kỳ của KH-1 tăng 1,500,000']),
    C('Thu tiền thì khai báo bị khóa, hủy ghi sổ thì mở lại', 'P0', 'Khai báo HĐ-2 + 1311 Dư nợ 1,500,000 chưa phát sinh.',
      ['Lập phiếu thu cho HĐ-2 ghi sổ tài khoản 1311, quay lại danh sách khai báo', 'Mở báo cáo ' + BC + ' kỳ 01/01/2026 – 31/10/2026',
       'Xóa / hủy ghi sổ phiếu thu đó, quay lại danh sách'], 'Phiếu thu: 600,000',
      ['Bước 1: dòng khai báo không còn Sửa, Xóa; chi tiết chỉ còn Quay lại',
       'Bước 2: Đã thanh toán của HĐ-2 có 600,000, Số dư cuối kỳ = 1,500,000 - 600,000 = 900,000',
       'Bước 3: khai báo có lại Sửa, Xóa']),
    C('Chứng từ khác tài khoản không khóa khai báo', 'P1', 'Khai báo Z (HĐ-1, tài khoản 1311) chưa phát sinh.',
      ['Lập phiếu kế toán ghi sổ cho KH-1 + HĐ-1 nhưng tài khoản 1312', 'Quay lại danh sách khai báo'], '',
      ['Z vẫn có Sửa, Xóa (chỉ khóa khi trùng cả khách hàng + hợp đồng + tài khoản)']),
    C('Hợp đồng đã khai báo không chọn lại được ở lần lập sau', 'P0', 'Vừa lưu khai báo cho KH-1 + HĐ-2 (ở hệ thống mới hoặc cũ).',
      ['Tạo mới, chọn KH-1, mở cửa sổ chọn hợp đồng'], '',
      ['HĐ-2 hiện mờ, Tình trạng "Đã khai báo", bấm không thêm được']),
]

# =============================================================== XIII. PHÂN QUYỀN
S_PQ = [
    C('Không có quyền "' + QUYEN + '" thì không thấy màn ở cả 2 lối vào', 'P0', 'TK-Z không có quyền "' + QUYEN + '".',
      ['Đăng nhập TK-Z', 'Mở phân hệ Tài chính, nhóm "Khai báo đầu kỳ" và Kế toán công nợ > nhóm "Khách hàng"',
       'Dán đường dẫn màn danh sách, trang thêm mới lên thanh địa chỉ', 'Đăng nhập TK-Z ở hệ thống cũ, mở 2 mục menu'], 'Tài khoản TK-Z',
      ['Không có mục "Khai báo đầu kỳ công nợ" lẫn "Công nợ đầu kỳ theo khách hàng - hợp đồng"',
       'Dán đường dẫn: sang trang "Không tìm thấy", không lộ dữ liệu, không tạo được gì', 'Hệ thống cũ cũng chặn cả màn với TK-Z']),
    C('Có quyền "' + QUYEN + '" thì dùng đủ chức năng', 'P0', 'TK-A có "' + QUYEN + '" + "' + Q_CTY + '".',
      ['Đăng nhập TK-A', 'Vào màn từ từng lối vào'], 'Tài khoản TK-A',
      ['Thấy CẢ 2 mục menu; có Tạo mới, Import Excel, Xuất Excel, In danh sách, Cấu hình cột hiển thị',
       'Khai báo chưa phát sinh có Sửa, Xóa, Lịch sử; đã phát sinh chỉ có Lịch sử']),
    C('Bị bỏ quyền trong lúc đang thao tác', 'P1', 'TK-A đang mở trang thêm mới, đã nhập đủ. Quản trị bỏ quyền "' + QUYEN + '" của TK-A.',
      ['TK-A bấm Lưu', 'TK-A tải lại màn danh sách'], '',
      ['Không lưu được, không tạo khai báo nào (hệ thống báo "Bạn không có quyền thực hiện chức năng này.")',
       'Tải lại: menu không còn 2 mục, vào màn sang trang "Không tìm thấy"']),
    C('Phạm vi xem: "' + Q_ALL + '"', 'P0', 'TK-ALL có "' + QUYEN + '" + "' + Q_ALL + '".',
      ['Đăng nhập TK-ALL, vào màn', 'Bấm Tìm kiếm nâng cao', 'So tổng với hệ thống cũ cùng tài khoản'], '',
      ['Thấy khai báo của MỌI công ty; có ô Công ty, Phòng ban, Bộ phận (cấp dưới khóa tới khi chọn cấp trên)', 'Tổng bằng hệ thống cũ']),
    C('Phạm vi xem: "' + Q_CTY + '"', 'P0', 'TK-A thuộc công ty TPE.',
      ['Đăng nhập TK-A, vào màn', 'Bấm Tìm kiếm nâng cao, lọc Phòng ban = HN_KD3'], '',
      ['Chỉ thấy khai báo công ty TPE (công ty của NGƯỜI LẬP HỢP ĐỒNG); không có ô Công ty, có Phòng ban, Bộ phận',
       'Lọc Phòng ban ra khai báo của hợp đồng do nhân viên HN_KD3 lập']),
    C('Phạm vi xem: "' + Q_PB + '" và "' + Q_BP + '"', 'P1',
      ['TK-PB có "' + QUYEN + '" + "' + Q_PB + '", được giao quản lý phòng HN_KD3.',
       'TK-BP có "' + QUYEN + '" + "' + Q_BP + '", được giao quản lý 1 bộ phận.'],
      ['Đăng nhập TK-PB, vào màn, đọc tổng', 'Đăng nhập TK-BP, vào màn, đọc tổng', 'So tổng với hệ thống cũ cùng tài khoản'], '',
      ['TK-PB chỉ thấy khai báo thuộc phòng ban được giao quản lý (theo người lập hợp đồng); có ô Phòng ban, Bộ phận',
       'TK-BP chỉ thấy khai báo thuộc bộ phận được giao quản lý; chỉ có ô Bộ phận', 'Tổng mỗi tài khoản bằng hệ thống cũ']),
    C('Không có quyền phạm vi nào thì chỉ thấy khai báo mình tạo', 'P0', 'TK-F có "' + QUYEN + '", không quyền phạm vi; TK-F đã tạo khai báo Z.',
      ['Đăng nhập TK-F, vào màn', 'Dán đường dẫn chi tiết một khai báo do người khác tạo'], '',
      ['Chỉ hiện khai báo do TK-F tạo; khu vực lọc KHÔNG có ô Công ty / Phòng ban / Bộ phận',
       'Khai báo của người khác: trang "Không tìm thấy"']),
]

GROUPS = [
    ('HIỂN THỊ TRANG & TRUY CẬP', S_HIEN_THI),
    ('TÌM KIẾM & LỌC DANH SÁCH', S_LOC),
    ('THÊM MỚI', S_THEM),
    ('CHỈNH SỬA', S_SUA),
    ('XÓA', S_XOA),
    ('LỊCH SỬ THAY ĐỔI', S_LS),
    ('XEM CHI TIẾT KHAI BÁO', S_CT),
    ('IN PHIẾU (IN DANH SÁCH KHAI BÁO)', S_IN),
    ('TÙY CHỈNH CỘT', S_COT),
    ('XUẤT DANH SÁCH EXCEL', S_XUAT),
    ('IMPORT TỪ FILE EXCEL', S_IMP),
    ('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S_RB),
    ('PHÂN QUYỀN', S_PQ),
]
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
SECTIONS = [(ROMAN[i], title, [('%03d' % (k + 1),) + tc for k, tc in enumerate(tcs)])
            for i, (title, tcs) in enumerate(GROUPS)]

if __name__ == '__main__':
    for roman, title, tcs in SECTIONS:
        print('%-5s %-36s %3d case, P0 %d' % (roman, title, len(tcs), sum(1 for t in tcs if t[2] == 'P0')))
    build_chuan(OUT, SHEET, TEN + ' - Cập nhật ngày ' + NGAY, MODULE, DESCRIPTION_BLOCK, SECTIONS, loai='phieu')

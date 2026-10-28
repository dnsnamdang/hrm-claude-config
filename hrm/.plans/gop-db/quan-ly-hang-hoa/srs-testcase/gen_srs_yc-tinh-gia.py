# -*- coding: utf-8 -*-
"""Sinh SRS - Yeu cau tinh gia (luong Chuyen doi hang hoa, man 4/5) — form chuan 2026-09-24.

Pham vi: man "YC tinh gia" (Ban hang > Yeu cau > Hang hoa > YC tinh gia) gom danh sach, loc, cau hinh cot, Tao YCTG tu nhom
(lối vào: nut Lap YCTG o YCHG / nut Tao moi + popup Chon nhom), tab Hang hoa + tab Chi phi, Sua, Chi tiet, Xoa, Gui tinh gia,
KTMH Tu choi, KTMH Tinh gia (mo lap PTG) / Xem phieu tinh gia, Chi tiet ket qua (gia ban moi), In phieu.

Nguon doi chieu code: worktree wt-chuyen-doi-hang-hoa nhanh feat/chuyen-doi-hang-hoa (hrm-api 39c4a91fe, hrm-client 5c14659e8)
— doc ngay 16/10/2026.
  BE: Modules/MasterData/Routes/api.php (nhom price-calculate-requests: xem KHONG gate route — service doi 1663|1664|1092;
      store/update/destroy gate 1663; reject gate 1664), Http/Controllers/V1/PriceCalculation/PriceCalculateRequestController,
      Services/PriceCalculation/{PriceCalculateRequestAccess, PriceCalculateRequestService, PriceCalculateRequestWriter,
      PriceCalculateRequestNotifier, PriceAskingAccess, XnkAssignmentResolver, PriceResultReader, PriceCalculateWriter (YCTG 2->1,
      xoa PTG 1->2), PriceCalculateFinalizer (YCTG 6 / 1 / 4), PriceCalculateAccess::canCalculate, PriceCalculationPrintService},
      Entities/PriceCalculation/{PriceCalculateRequest, PriceAskingRequestGroup}, Entities/InternalPricePolicy/InternalPricePolicy.
  FE: pages/sale/price-calculate-requests/{index, add, _id/index, _id/edit}.vue, components/sale/price-calculate/
      {PriceCalculateRequestForm, PriceInputGoodsTable, PriceInputCostsTable, PolicyCell, PendingGroupPickerModal}.vue,
      utils/mixins/priceInputRowsMixin.js, components/sale/price-asking/{PriceResultDrill, PriceAskingReasonModal}.vue,
      components/subsystem-menu/sale-hub.js (muc "YC tinh gia" isShow 1663 | 1664 | 1092).

Anh chup: Playwright MCP 1440x900, cong 3031 (worktree, DB hrm_erp_giacty), tai khoan E2E Assign (Cty 1, co san 1092 1652 1657
1658). Tao role tam TMP_SRS_YCTG_1663_1664 (id 129857, quyen 1663 + 1664 Cty 1) de chup THAT nut Tao moi + popup chon nhom —
DA GO + cache:forget; dem roles/rhp/ehr ve 130/20967/1718. Moi lenh ghi bi chan tren trinh duyet (route.fulfill / abort) — DB
khong doi (YCTG Cty 1 van 3:4 · 4:2285 · 5:19 · 1:1).
  - THAT: 00-menu, 01 (2.305 YCTG Cty 1), 02, 03, 05 (popup rong — tai khoan khong duoc phan cong XNK), 14..18 (PYCTG-03162 Da
    tinh gia, EURO 30,927.74, 3 chi phi, PTG-03178, ban in), 19 (PYCTG-01939 ENEOS 2 DVT Thung/Tuyp), 20 (PYCTG-02786 Khong
    duyet), 21 (PYCTG-01403 nhom Huy duyet), 22 (PYCTG-00177 Dang tinh gia, PTG nhap nguoi khac khong lo so), 23 (nhap PYCTG-02874
    cua nguoi khac -> trang 404).
  - MINH HOA (sua phan hoi tren trinh duyet, khong ghi DB): 01b (dong Dang tao cua minh + dong Cho tinh gia), 05b (popup co 2 nhom
    that CARLEO / BESITA Cho lap YCTG), 06..13 (form Tao dung dong hang x DVT that cua PYCTG-02257 ENEOS; nhap lieu / loi / xac nhan
    la hanh vi that cua man, 0 request ghi), 24..26 (PYCTG-02786 gia lam Cho tinh gia de hien Tinh gia / Tu choi), 27 (gia lam
    nguoi lap de mo man Sua), 28 (gia lam Dang tao de hien Xoa), 29/30 (o Chinh sach gia noi bo — DB dev chi co chinh sach do Cty 1
    ban ra, YCTG Cty 1 toan hang cua chinh Cty 1), 31 (tra loi khong quyen xem). DB dev KHONG co YCTG nao Cho tinh gia / Cho duyet gia.
  - icon_phanhe / icon_rail_yeucau / icon_nhom_hanghoa / icon_lapyctg + 04a: dung lai cua bo YC hoi gia (cung phan tu giao dien).

Chay:  python3 .plans/gop-db/quan-ly-hang-hoa/srs-testcase/gen_srs_yc-tinh-gia.py   (Word dang mo -> update_fields=False)
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
HRM = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(HRM, '.claude', 'skills', 'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(HERE, 'yc-tinh-gia_shots')
OUT = os.path.join(HERE, 'SRS - Yêu cầu tính giá.docx')


def shot(name):
    return os.path.join(SHOTS, name)


A_XNK = 'XNK lập yêu cầu tính giá'
A_KTMH = 'Kế toán mua hàng (KTMH)'
A_XEM = 'Người xem yêu cầu tính giá'
MENU = 'Phân hệ Bán hàng => Yêu cầu => Hàng hóa => YC tính giá'
MENU_YCHG = 'Phân hệ Bán hàng => Yêu cầu => Hàng hóa => YC hỏi giá => Lập YCTG'
SCREEN = 'Yêu cầu tính giá'

d = SrsDoc(out=OUT, menu=MENU, route='/sale/price-calculate-requests',
           full_url='http://hrm/sale/price-calculate-requests', img_prefix='yctg_')
d.set_menu_icons({k: shot(v) for k, v in {
    'Phân hệ Bán hàng': 'icon_phanhe.png',
    'Yêu cầu': 'icon_rail_yeucau.png',
    'Hàng hóa': 'icon_nhom_hanghoa.png',
    'YC tính giá': 'icon_yctg.png',
    'Lập YCTG': 'icon_lapyctg.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cấu hình cột': 'icon_cauhinhcot.png',
    'Tạo mới': 'icon_taomoi.png',
    'Sửa': 'icon_row_sua.png',
    'Xóa': 'icon_row_xoa.png',
    'Xử lý': 'icon_row_xuly.png',
    'Tính giá': 'icon_tinhgia.png',
    'Xem phiếu tính giá': 'icon_xemptg_footer.png',
    'Từ chối': 'icon_tuchoi.png',
    'In': 'icon_row_in.png',
    'Lưu nháp': 'icon_luunhap.png',
    'Lưu và gửi duyệt': 'icon_guiduyet.png',
    '+ Thêm chi phí': 'icon_themchiphi.png',
    'Chi tiết kết quả': 'icon_chitietketqua.png',
}.items()})

Q1 = 'XNK xử lý yêu cầu hỏi giá'
Q2 = 'Tính giá bán hàng hoá'
Q3 = 'Xem giá vốn hàng hoá'
MSG_NOPERM = 'Bạn không có quyền thực hiện chức năng này'
MSG_NO_VIEW = 'Bạn không có quyền xem yêu cầu tính giá'
MSG_NOTFOUND = 'Không tìm thấy yêu cầu tính giá'
MSG_GROUP_NF = 'Không tìm thấy nhóm hàng của yêu cầu hỏi giá'
MSG_CONFLICT = 'Trạng thái đã bị thay đổi. Vui lòng load lại trang'
MSG_NOT_XNK = 'Bạn không phải XNK phụ trách nhóm này.'
MSG_CLOSED = 'Nhóm hàng đã đóng, yêu cầu tính giá chỉ còn xem.'
MSG_CLOSED_NOTE = 'Nhóm hàng đã kết thúc (<trạng thái nhóm>) — yêu cầu tính giá chỉ còn xem.'
MSG_404PAGE = 'Không tìm thấy hoặc không được cấp quyền truy cập trang'
MSG_REQ = 'Bắt buộc phải nhập'
MSG_NO_UNIT = 'Nhóm không còn hàng hoá nào có đơn vị tính'
MSG_MAX = 'Không được lớn hơn 999,999,999,999.'

# ============================================================== TRANG DAU
d.title_block(SCREEN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Yêu cầu tính giá (phân hệ Bán hàng) — chứng từ thứ hai của luồng tính '
    'giá bán (YCHG → YCTG → Phiếu tính giá → giá áp), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng trạng thái của Yêu cầu tính giá (YCTG).',
    'Làm rõ YCTG CÓ phân quyền xem (khác YCHG): phải có 1 trong 3 quyền “' + Q1 + '”, “' + Q2 + '”, “' + Q3 + '” tại công '
    'ty đang làm việc; không có quyền nào thì không thấy menu, không mở được phiếu.',
    'Làm rõ ai làm gì: XNK được phân công phụ trách hãng lập YCTG cho 1 nhóm Thương hiệu — Hãng đã duyệt của YCHG, nhập giá nhà '
    'cung cấp, tiền tệ, tỉ giá, thuế nhập khẩu, chi phí rồi gửi; Kế toán mua hàng (quyền “' + Q2 + '”) Từ chối trả về XNK hoặc '
    'bấm Tính giá để lập Phiếu tính giá.',
    'Làm rõ phần GIÁ: YCTG chỉ chứa số đầu vào (giá NCC, tỉ giá, thuế, chi phí — máy chủ tự tính lại đơn giá VNĐ, thành tiền sau '
    'thuế, thành tiền chi phí); YCTG KHÔNG ghi giá bán nào. Quyền “' + Q3 + '” chỉ quyết định có thấy giá vốn công ty quản lý '
    'trong cột Chính sách giá nội bộ hay không. Giá bán mới (6 loại giá × ĐVT + ĐMGG) chỉ có sau khi Phiếu tính giá được áp giá, '
    'xem ở “Chi tiết kết quả”.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('YCTG', 'Yêu cầu tính giá — số phiếu PYCTG-xxxxx (nối dãy số của ERP), sinh khi lưu lần đầu.'),
    ('YCHG', 'Yêu cầu hỏi giá — chứng từ gốc; mỗi nhóm Thương hiệu — Hãng của YCHG có tối đa 1 YCTG.'),
    ('Nhóm hàng', '1 cặp Thương hiệu — Hãng sản xuất trong YCHG. YCTG lập cho đúng 1 nhóm, mang theo mọi hàng của nhóm.'),
    ('Công ty phiếu', 'Công ty của YCHG = công ty đang làm việc. YCTG, PTG, giá áp đều thuộc công ty này.'),
    ('XNK phụ trách', 'Người mua đang được phân công (màn Phân công nhân viên phụ trách) cho Thương hiệu × Hãng × công ty phiếu, có '
     'quyền “' + Q1 + '”.'),
    ('KTMH', 'Kế toán mua hàng — người có quyền “' + Q2 + '” tại công ty phiếu.'),
    ('PTG', 'Phiếu tính giá — KTMH lập từ YCTG (1 YCTG – 1 PTG), ra giá bán mới (đặc tả ở SRS Phiếu tính giá).'),
    ('Dòng hàng × ĐVT', 'Mỗi dòng của YCTG = 1 hàng × 1 đơn vị tính đã khai của hàng; ĐVT cơ bản đứng trước, ĐVT khác hiện “↳ cùng mã”.'),
    ('Giá NCC', 'Giá nhà cung cấp theo đơn vị tiền tệ của phiếu (cột “Giá NCC (<tiền tệ>)”), tối đa 2 số thập phân.'),
    ('Tỉ giá', 'Số VNĐ cho 1 đơn vị tiền tệ của phiếu; VNĐ thì tỉ giá = 1 và bị khoá.'),
    ('Chi phí', 'Danh mục 7 chi phí giá hàng hoá (Cước vận tải quốc tế, Chi phí vận chuyển nội địa, Phí kiểm định, Chi phí bốc vác, '
     'Thuế nhập khẩu, Chi phí khác, Bảo hiểm hàng hóa); mỗi dòng hàng × ĐVT có thể có nhiều chi phí, nhập theo Tỉ lệ (%) của Giá NCC.'),
    ('Chính sách giá nội bộ', 'Cách công ty quản lý hàng bán lại cho công ty phiếu (Theo giá vốn / Theo giá bán + tỷ lệ Nhập khẩu, '
     'Tồn kho). Ở YCTG chỉ để tham khảo.'),
    ('Kết quả tính giá / Giá bán mới', 'Bản chụp giá bán lúc PTG được áp giá: 6 loại giá (Bán lẻ, Theo lô, Đại lý cấp 1, 2, 3, TMĐT) '
     '× ĐVT + ĐMGG (định mức giảm giá tối đa %).'),
], widths=[1.6, 4.4])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Mọi quyền xét TẠI công ty đang làm việc (= công ty phiếu; phiếu công ty khác coi như không tồn tại). Super admin không được '
    'miễn: thiếu quyền là không thấy menu / nút và bị hệ thống từ chối khi gọi thẳng chức năng. Có ÍT NHẤT 1 trong 3 quyền dưới đây '
    'mới xem được YCTG; không có quyền nào → menu “YC tính giá” ẩn, mọi chức năng báo “' + MSG_NO_VIEW + '”, mở thẳng phiếu ra '
    'trang “' + MSG_404PAGE + '”.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1, [
        '- Xem danh sách / chi tiết / in YCTG.',
        '- Thấy nút Tạo mới (popup chỉ liệt kê nhóm MÌNH đang được phân công) và nút Lập YCTG ở YCHG.',
        '- Lập YCTG chỉ khi ĐỒNG THỜI là XNK được phân công hiện hành của Thương hiệu × Hãng × công ty phiếu; có Q1 mà không được '
        'phân công → popup rỗng, gọi thẳng báo “' + MSG_NOT_XNK + '”.',
        '- Sửa / gửi / xoá YCTG do CHÍNH MÌNH lập (không xét lại phân công).']),
    ('Q2', Q2, [
        '- Xem danh sách / chi tiết / in YCTG.',
        '- Từ chối YCTG Chờ tính giá (nút Từ chối ở Chi tiết, Xử lý ở danh sách) — mọi YCTG của công ty, không xét phân công hãng.',
        '- Tính giá: lập Phiếu tính giá từ YCTG Chờ tính giá chưa có PTG.',
        '- Nhận thông báo “[YCTG] Chờ duyệt …” khi XNK gửi.']),
    ('Q3', Q3, [
        '- Xem danh sách / chi tiết / in YCTG (không thao tác ghi).',
        '- Thấy giá vốn công ty quản lý trong cột Chính sách giá nội bộ (chính sách Theo giá vốn); không có Q3 ô này hiện “—”, máy chủ '
        'không trả số.']),
], widths=[0.7, 1.9, 3.4])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (KHÔNG phải quyền gán — phạm vi tính theo dữ liệu phiếu, áp cho người đã có Q1/Q2/Q3):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Người lập YCTG', 'Thấy YCTG Đang tạo (nháp) của chính mình; YCTG Đang tạo của người khác không hiện ở danh sách, mở thẳng → '
     'trang “' + MSG_404PAGE + '”.'),
    ('V2', 'Người có Q1 / Q2 / Q3 trong công ty', 'Thấy mọi YCTG đã gửi (Chờ tính giá, Không duyệt, Đang tính giá, Chờ duyệt giá, Đã tính '
     'giá) của công ty đang làm việc. Không phân quyền theo phòng ban / bộ phận / cấp quản lý.'),
    ('V3', 'Công ty khác', 'Không thấy, không thao tác được YCTG của công ty khác (hệ thống báo “' + MSG_NOTFOUND + '”). Đổi công ty đang '
     'làm việc thì danh sách đổi theo.'),
], widths=[0.7, 1.9, 3.4])

d.h2('2 Ma trận phân quyền')
d.p('✅ = được, ❌ = không được. Cột Q1 tính cho người ĐÃ được phân công XNK của nhóm (có Q1 mà không được phân công thì như cột Q3 '
    'ở các dòng Tạo).')
d.table(['Chức năng', 'Q1 (+ phân công)', 'Q2', 'Q3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách YCTG', '✅', '✅', '✅', '❌ (menu ẩn)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '✅', '❌'),
    ('FR-04 Tạo YCTG (Lưu nháp)', '✅ chỉ nhóm mình được phân công', '❌', '❌', '❌'),
    ('FR-05 Chọn nhóm cần lập YCTG (popup)', '✅', '❌ (không có nút Tạo mới)', '❌', '❌'),
    ('FR-06 Nhập chi phí (tab Chi phí)', '✅ khi tạo / sửa', '❌ (chỉ xem)', '❌ (chỉ xem)', '❌'),
    ('FR-07 Sửa YCTG', '✅ chỉ người lập, Đang tạo / Không duyệt', '❌', '❌', '❌'),
    ('FR-08 Xem chi tiết YCTG', '✅', '✅', '✅', '❌ (trang 404)'),
    ('FR-09 Xoá YCTG', '✅ chỉ người lập, Đang tạo', '❌', '❌', '❌'),
    ('FR-10 Gửi tính giá (Lưu và gửi duyệt)', '✅ chỉ người lập', '❌', '❌', '❌'),
    ('FR-11 KTMH từ chối YCTG', '❌', '✅ YCTG Chờ tính giá', '❌', '❌'),
    ('FR-12 Tính giá / Xem phiếu tính giá', '✅ chỉ Xem PTG', '✅ Tính giá + Xem PTG', '✅ chỉ Xem PTG', '❌'),
    ('FR-13 Xem giá bán mới (Chi tiết kết quả)', '✅', '✅', '✅', '❌'),
    ('FR-14 In YCTG', '✅', '✅', '✅', '❌'),
], widths=[2.1, 1.2, 1.1, 0.8, 0.8])
d.p('Lưu ý: giá vốn ở cột Chính sách giá nội bộ chỉ hiện với Q3 — kể cả KTMH (Q2) không có Q3 cũng chỉ thấy “—”.')

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_XNK, [0, 1, 2, 3, 4, 7, 8]), (A_KTMH, [0, 5, 6, 7, 8]), (A_XEM, [0, 7, 8])],
    [('FR-01', 'Xem danh sách YCTG', 'view'),              # 0
     ('FR-04', 'Tạo YCTG', 'crud'),                         # 1
     ('FR-07', 'Sửa YCTG', 'crud'),                         # 2
     ('FR-09', 'Xoá YCTG', 'action'),                       # 3
     ('FR-10', 'Gửi tính giá', 'action'),                   # 4
     ('FR-11', 'KTMH từ chối YCTG', 'action'),              # 5
     ('FR-12', 'Tính giá / Xem phiếu tính giá', 'action'),  # 6
     ('FR-13', 'Xem giá bán mới', 'view'),                  # 7
     ('FR-14', 'In YCTG', 'io')],                           # 8
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-05', 'Chọn nhóm cần lập YCTG', 'crud', 'extend', [1], None),
     ('FR-06', 'Nhập chi phí', 'crud', 'extend', [1, 2], None),
     ('FR-08', 'Xem chi tiết YCTG', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Yêu cầu tính giá')

d.h2('2 Đặc tả chi tiết từng chức năng')

LIST_RULE = ('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn '
             'Yêu cầu tính giá tại phần mô tả chi tiết.')
CREATE_RULE = ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu tính giá '
               'tại phần mô tả chi tiết.')
NOTICE_RULE = '- Thông báo và Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu tính giá tại phần mô tả chi tiết.'
DETAIL_RULE = '- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu tính giá tại phần mô tả chi tiết.'

VALIDATE = [
    '– Đơn vị tiền tệ trống → “' + MSG_REQ + '”; tiền tệ đã ngừng dùng → “Không tồn tại”.',
    '– (ngoại tệ) Tỉ giá trống → “' + MSG_REQ + '”; ≤ 0 → “Phải lớn hơn 0”; quá lớn → “Không hợp lệ” (màn hình) / “' + MSG_MAX + '” (máy chủ).',
    '– Ghi chú > 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”',
    '– Giá NCC âm / không phải số → “Không hợp lệ”; quá lớn → như Tỉ giá.',
    '– Thuế NK (%) ngoài 0–100 → “Phải từ 0 đến 100”.',
    '– Dòng chi phí chưa chọn tên → “' + MSG_REQ + '”; trùng tên trong cùng dòng hàng → “Chi phí đã có trong dòng này”; Tỉ lệ (%) '
    'ngoài 0–100 → “Phải từ 0 đến 100”; chi phí quá lớn → “Chi phí vượt giới hạn lưu trữ”.',
    '– Mọi lỗi báo cùng lúc, dưới đúng ô; tab có lỗi gắn chấm đỏ, tự chuyển sang tab có lỗi và cuộn tới lỗi đầu tiên; không lưu gì.',
]
VALIDATE_SEND = [
    '– (chỉ Lưu và gửi duyệt) Mọi dòng hàng × ĐVT phải có Giá NCC: trống → “' + MSG_REQ + '”; bằng 0 → “Phải lớn hơn 0”.',
]

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách YCTG')
d.p('2.1.1 Giới thiệu')
d.rule_ref(LIST_RULE, anchor='list')
d.intro_table(
    ten='Xem danh sách yêu cầu tính giá',
    mota='Hiển thị các YCTG của CÔNG TY ĐANG LÀM VIỆC dạng bảng phẳng (1 YCTG = 1 dòng = 1 nhóm Thương hiệu — Hãng). Từ danh sách '
         'mở Chi tiết, Sửa, Xoá, Xử lý (KTMH), Tính giá, Xem phiếu tính giá, In.',
    tacnhan=A_XNK + '; ' + A_KTMH + '; ' + A_XEM + '; Người dùng đã đăng nhập',
    dieukien='Người dùng có 1 trong 3 quyền ' + Q1 + ' / ' + Q2 + ' / ' + Q3 + ' tại công ty đang làm việc.',
    chinh='1. Người dùng vào Phân hệ Bán hàng › Yêu cầu › Hàng hóa › YC tính giá.\n'
          '2. Hệ thống lấy YCTG của công ty đang làm việc: mọi YCTG đã gửi + YCTG Đang tạo của chính người dùng; mới tạo lên trước, '
          '10 dòng / trang.\n'
          '3. Bấm số phiếu → màn Chi tiết (mục 2.8); bấm số YCHG → màn Chi tiết YCHG.',
    phu='• Không có quyền nào trong 3 quyền: không thấy mục menu; mở thẳng màn → bảng rỗng kèm thông báo “' + MSG_NO_VIEW + '”.\n'
        '• Không có YCTG nào / không khớp bộ lọc → “Không có dữ liệu phù hợp”.\n'
        '• YCTG Đang tạo của người khác không hiện (DB dev: 4 phiếu nháp của người khác ở Cty 1 không hiện).\n'
        '• Lỗi tải khác → thông báo “Lỗi khi tải dữ liệu”.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('00-menu.png'),
         shot_caption='Menu Bán hàng › Yêu cầu › Hàng hóa › YC tính giá — ngay sau YC hỏi giá (dữ liệu thật)')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Danh sách YCTG công ty 1 — 2.305 phiếu tài khoản E2E Assign nhìn thấy (dữ liệu thật)')
d.layout(menu=MENU, shot=shot('01b-danh-sach-hanh-dong.png'),
         shot_caption='Cột Hành động: dòng 1 Đang tạo của mình (Sửa · Xóa · In), dòng 2 Chờ tính giá với KTMH (Xử lý · Tính giá · In) '
                      '(minh hoạ — sửa phản hồi trên trình duyệt)')
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang / khối', 'Label', 'Hiển thị', '–', 'Yêu cầu tính giá', 'Tiêu đề thanh đầu trang và khối bảng.'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền', [
        '- Chỉ hiện với người có quyền ' + Q1 + '.',
        '- Bấm → popup Chọn nhóm cần lập yêu cầu tính giá (mục 2.5).']),
    ('Nút Cấu hình cột', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Tooltip “Cấu hình cột hiển thị” → mục 2.3.'),
    ('Bảng yêu cầu tính giá', 'Table/Grid', 'Read-only', '10 cột', 'Theo dữ liệu', [
        '- Mỗi YCTG 1 dòng; cột STT, Số phiếu dính trái khi cuộn ngang.',
        '- Mặc định sắp Ngày tạo mới → cũ; sắp được theo Số phiếu, Ngày tạo (bấm tiêu đề cột).']),
    ('Cột STT', 'Text', 'Read-only', 'Số nguyên', 'Theo dữ liệu', 'Số thứ tự liên tục qua các trang.'),
    ('Cột Số phiếu', 'Text', 'Read-only', 'PYCTG-xxxxx', 'Theo dữ liệu', [
        '- Số phiếu là link → bấm mở màn Chi tiết (mục 2.8).',
        '- Dòng dưới (chữ xám): Ghi chú của YCTG khi có.']),
    ('Cột Yêu cầu hỏi giá', 'Text', 'Read-only', 'PYCHG-xxxxx', 'Theo dữ liệu', '- Số YCHG gốc là link → bấm mở Chi tiết YCHG.'),
    ('Cột Thương hiệu – Hãng sản xuất', 'Text', 'Read-only', '–', 'Theo dữ liệu', '“<Thương hiệu> — <Hãng sản xuất>” của nhóm.'),
    ('Cột Số mã hàng', 'Number', 'Read-only', '≥ 1', 'Theo dữ liệu', 'Số mã hàng KHÁC NHAU của YCTG (1 hàng 2 ĐVT vẫn tính 1).'),
    ('Cột Tiền tệ', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Tên tiền tệ (VNĐ, USD, EURO…).',
        '- Dòng dưới “tỉ giá <số>” khi tỉ giá khác 1 (vd “tỉ giá 30,927.74”).']),
    ('Cột Người tạo', 'Text', 'Read-only', '–', 'Theo dữ liệu', '“<Họ tên> - <mã phòng> - <mã NV>” của XNK lập YCTG.'),
    ('Cột Ngày tạo', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Ngày lập YCTG.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 6 giá trị', 'Theo dữ liệu', [
        '- Đang tạo (xám) · Chờ tính giá (cam) · Không duyệt (đỏ) · Đang tính giá (xanh dương) · Chờ duyệt giá (tím) · Đã tính giá (xanh lá).']),
    ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo cờ quyền', [
        '- Sửa (bút): người lập, YCTG Đang tạo / Không duyệt, nhóm chưa đóng → màn Sửa (mục 2.7).',
        '- Xóa (thùng rác đỏ): người lập, YCTG Đang tạo → hộp xác nhận (mục 2.9).',
        '- Xử lý (dấu tích tròn): KTMH, YCTG Chờ tính giá → mở màn Chi tiết để Từ chối / Tính giá.',
        '- Tính giá (máy tính): KTMH, YCTG Chờ tính giá chưa có PTG → màn Tạo phiếu tính giá (mục 2.12).',
        '- Xem phiếu tính giá (tờ giấy): YCTG đã có PTG mà người xem được thấy → Chi tiết PTG.',
        '- In (máy in): luôn hiện → mục 2.14.']),
    ('Chân bảng', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', '10 dòng / trang', [
        '- “Hiển thị a–b / N”: a–b là thứ tự dòng đầu–cuối của trang, N = tổng YCTG khớp bộ lọc.',
        '- Đổi số dòng → về trang 1.']),
    ('Trạng thái rỗng / lỗi', 'Label / Toast / Alert', 'Hiển thị', '–', 'Ẩn', [
        '- Không có dữ liệu: “Không có dữ liệu phù hợp”.',
        '- Thiếu cả 3 quyền: thông báo “' + MSG_NO_VIEW + '”.',
        '- Lỗi khác: “Lỗi khi tải dữ liệu”.']),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm người dùng có 1 trong 3 quyền ' + Q1 + ' / ' + Q2 + ' / ' + Q3 + ' tại công ty đang làm việc; không có → “' +
     MSG_NO_VIEW + '”, bảng rỗng.\n'
     'During:\n– Lấy YCTG có công ty = công ty đang làm việc (lấy từ phiên làm việc, không nhận từ màn hình).\n'
     '– Bỏ YCTG Đang tạo của người khác.\n'
     '– Tính cờ nút từng dòng ở máy chủ (Sửa / Xóa / Xử lý / Tính giá / Xem PTG) — màn hình chỉ hiện theo cờ.\n'
     'After:\n– Trang 1, 10 dòng, sắp Ngày tạo mới → cũ.'),
    ('Bấm tiêu đề cột Số phiếu / Ngày tạo', 'Click', 'After:\n– Sắp tăng / giảm; bỏ sắp → Ngày tạo giảm dần; về trang 1.'),
    ('Đổi trang / số dòng', 'Click / Change', 'After:\n– Tải lại; đổi số dòng thì về trang 1.'),
    ('Bấm Xử lý / Tính giá / Xem phiếu tính giá', 'Click',
     'After:\n– Xử lý → màn Chi tiết YCTG.\n– Tính giá → màn Tạo phiếu tính giá của YCTG (Quay lại về danh sách YCTG).\n'
     '– Xem phiếu tính giá → Chi tiết PTG.'),
    ('Đổi công ty đang làm việc', 'System', 'After:\n– Danh sách tải lại theo công ty mới; YCTG công ty cũ biến mất.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu tính giá tại phần mô tả chi '
           'tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc yêu cầu tính giá',
    mota='Thu hẹp danh sách theo số YCTG / số YCHG / mã / tên hàng, trạng thái, thương hiệu, hãng, người tạo và khoảng ngày tạo.',
    tacnhan=A_XEM + '; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách YCTG.',
    chinh='1. Gõ từ khoá vào ô tìm nhanh rồi nhấn Enter hoặc bấm Tìm kiếm.\n'
          '2. Bấm Tìm kiếm nâng cao để mở các ô lọc; chọn giá trị — mỗi lần chọn là lọc ngay.\n'
          '3. Hệ thống tải lại danh sách từ trang 1.',
    phu='• Bấm Làm mới → xoá mọi điều kiện, sắp lại theo Ngày tạo giảm dần.\n'
        '• Hệ thống ghi nhớ bộ lọc trong 10 phút khi quay lại màn từ màn Chi tiết / Sửa.\n'
        '• Không có kết quả → “Không có dữ liệu phù hợp”.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-loc-nang-cao.png'),
         shot_caption='Khối bộ lọc khi mở Tìm kiếm nâng cao (dữ liệu thật)')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
        '- Placeholder “Tìm theo số phiếu, số yêu cầu hỏi giá, mã hoặc tên hàng hoá”.',
        '- Tìm gần đúng trên số YCTG, số YCHG gốc, mã hàng và tên hàng ghi trong YCTG.']),
    ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     ['- Tìm kiếm: chạy theo từ khoá + ô lọc, về trang 1.', '- Làm mới: xoá mọi ô lọc, về sắp xếp mặc định.']),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Đóng',
     ['- Mặc định khối ô lọc đang đóng.', '- Bấm để mở / đóng (“Ẩn tìm kiếm nâng cao”).']),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 6 giá trị', 'Không', 'Trống', [
        '- Mặc định: trống (mọi trạng thái).',
        '- Đang tạo · Chờ tính giá · Không duyệt · Đang tính giá · Chờ duyệt giá · Đã tính giá.',
        '- Lọc Đang tạo chỉ ra YCTG nháp của chính người dùng.']),
    ('Thương hiệu', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Mặc định: trống.', '- Chỉ liệt kê thương hiệu có trong YCTG của công ty, xếp A → Z.']),
    ('Hãng sản xuất', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', ['- Mặc định: trống.', '- Như Thương hiệu, theo hãng.']),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Mặc định: trống.', '- “<Họ tên> - <phòng> - <mã NV>” của người đã lập YCTG trong công ty, xếp theo tên.']),
    ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống',
     'Khoảng ngày lập YCTG, tính trọn cả ngày đầu và ngày cuối.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Nhấn Enter / bấm Tìm kiếm', 'Keypress / Click', 'After:\n– Tải lại từ trang 1 theo từ khoá + ô lọc.'),
    ('Chọn giá trị ô lọc', 'Change', 'After:\n– Lọc ngay, về trang 1.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, sắp theo Ngày tạo giảm dần, tải lại trang 1.'),
    ('Quay lại màn danh sách', 'System', 'After:\n– Khôi phục bộ lọc + trạng thái đóng / mở khối lọc trong 10 phút.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Cài đặt bộ lọc và tuỳ chỉnh cột')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu tính giá tại phần mô tả chi tiết.',
           anchor='excel')
d.intro_table(
    ten='Cài đặt bộ lọc và tuỳ chỉnh cột',
    mota='Ẩn / hiện, đổi thứ tự các ô lọc và các cột của bảng danh sách; cấu hình lưu theo người dùng.',
    tacnhan=A_XEM + '; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách YCTG.',
    chinh='1. Bấm nút Cấu hình cột (hoặc Cài đặt bộ lọc).\n2. Tích / bỏ tích, kéo thả để đổi thứ tự.\n3. Bấm Lưu.',
    phu='• Bấm Đóng → không lưu.\n• Cột STT, Số phiếu, Hành động bị khoá (luôn hiện).')
d.p('2.3.2 Layout màn hình')
d.layout(menu=MENU + ' => Cấu hình cột', shot=shot('03-cau-hinh-cot.png'), shot_caption='Popup Tuỳ chỉnh cột (dữ liệu thật)')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', 'Câu dẫn “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '10 cột', 'Không', 'Theo cấu hình đã lưu', [
        '- STT · Số phiếu · Yêu cầu hỏi giá · Thương hiệu – Hãng sản xuất · Số mã hàng · Tiền tệ · Người tạo · Ngày tạo · Trạng thái · Hành động.',
        '- Khoá (không bỏ tích được): STT, Số phiếu, Hành động.',
        '- Kéo thả để đổi thứ tự.']),
    ('Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ chọn hết vẫn giữ các cột khoá.'),
    ('Dòng đếm', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn <n>/10 cột” — n = số cột đang tích.'),
    ('Nút Lưu / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Lưu: áp ngay và lưu theo người dùng.', '- Đóng: bỏ thay đổi.']),
])
d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cấu hình cột', 'Click', 'After:\n– Mở popup với cấu hình đã lưu của người dùng.'),
    ('Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình theo người dùng; bảng hiện đúng các cột, đúng thứ tự.'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Tạo YCTG')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo YCTG', 'crud', actor=A_XNK, caption='Biểu đồ Use Case — FR-04 Tạo YCTG')
d.p('2.4.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Tạo yêu cầu tính giá',
    mota='XNK phụ trách lập YCTG cho 1 nhóm Thương hiệu — Hãng đã được XNK duyệt (nhóm Chờ lập YCTG) của 1 YCHG Đang hỏi giá. Form '
         'bung sẵn mọi hàng của nhóm × mọi ĐVT; XNK chọn tiền tệ, tỉ giá, nhập Giá NCC, Thuế NK, chi phí rồi Lưu nháp hoặc Lưu và gửi '
         'duyệt (mục 2.10).',
    tacnhan=A_XNK,
    dieukien='Có quyền ' + Q1 + ' tại công ty phiếu VÀ đang được phân công XNK của Thương hiệu × Hãng của nhóm; nhóm Chờ lập YCTG, '
             'chưa có YCTG; YCHG Đang hỏi giá.',
    chinh='1. Mở form bằng 1 trong 2 lối vào: nút Lập YCTG ở dòng nhóm của YCHG (Chi tiết YCHG hoặc danh sách YCHG); hoặc nút Tạo '
          'mới ở danh sách YCTG → chọn nhóm trong popup (mục 2.5).\n'
          '2. Form “Tạo yêu cầu tính giá” hiện Thông tin chung (YCHG, Thương hiệu – Hãng, Người hỏi giá: chỉ đọc) và tab Hàng hoá đã '
          'bung đủ dòng hàng × ĐVT.\n'
          '3. Chọn Đơn vị tiền tệ (tỉ giá tự điền theo danh mục tiền tệ, sửa được; VNĐ thì tỉ giá 1 và bị khoá).\n'
          '4. Nhập Giá NCC từng dòng (nhập ở ĐVT cơ bản thì ĐVT khác tự gợi ý = giá × hệ số quy đổi), sửa Thuế NK nếu cần.\n'
          '5. (Tuỳ chọn) tab Chi phí: thêm chi phí cho từng dòng (mục 2.6).\n'
          '6. Bấm Lưu nháp → YCTG Đang tạo; thông báo “Đã lưu nháp yêu cầu tính giá”; về danh sách YCTG.',
    phu='• Người dùng không phải XNK phụ trách nhóm (hoặc thiếu quyền) mở form → trang “' + MSG_404PAGE + '”.\n'
        '• Nhóm vừa được người khác lập YCTG / không còn Chờ lập YCTG → thông báo “' + MSG_CONFLICT + '”, về danh sách YCTG.\n'
        '• Lỗi nhập liệu → báo đỏ dưới ô, tab có lỗi gắn chấm đỏ (xem 2.4.5).\n'
        '• Bấm Quay lại khi đã nhập → hộp “Thông tin chưa lưu”; vào từ YCHG thì Quay lại về đúng màn YCHG.\n'
        '• Lưu (nháp hoặc gửi) xong: nhóm của YCHG chuyển “Đang tính giá”, nút Lập YCTG / Huỷ duyệt ở YCHG biến mất.',
    dacbiet='Không có ô tick chọn dòng: mọi dòng hàng × ĐVT của nhóm đều nằm trong YCTG. Hàng tạm (Hàng tạm / Hàng tạm đã duyệt / '
            'Hàng tạm không duyệt) không đi sang YCTG. Máy chủ TÍNH LẠI mọi số tiền khi lưu (BR-07), không lấy số trên màn.')
d.p('2.4.3 Layout màn hình')
d.p('Đường dẫn màn hình (2 lối vào mở cùng 1 form Tạo):')
d.layout(menu=MENU_YCHG, shot=shot('04a-ychg-lap-yctg.png'),
         shot_caption='Lối vào 1: nút Lập YCTG ở dòng nhóm Chờ lập YCTG của YCHG (ảnh của bộ SRS YC hỏi giá — minh hoạ)')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('06-tao-moi.png'),
         shot_caption='Form Tạo yêu cầu tính giá: nhóm ENEOS 14 dòng hàng × ĐVT, “↳ cùng mã” là ĐVT thứ 2 (minh hoạ — dòng hàng thật '
                      'của PYCTG-02257, phản hồi dựng trên trình duyệt)')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('08-nhap-gia-goi-y.png'),
         shot_caption='Chọn USD → tỉ giá 26,180; gõ 10 ở Tuýp → Thùng 20C-0.4Kg tự gợi ý 200; Đơn giá VNĐ 261,800 / 5,236,000 (minh hoạ, '
                      'phép tính thật của màn)')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('09-thue-thanh-tien.png'),
         shot_caption='Thuế NK 5% → Thành tiền sau thuế 2,350,310 (= 2,238,390 × 1,05) (minh hoạ)')
d.layout(menu=MENU + ' => Lưu và gửi duyệt', shot=shot('07-loi-gui-trong.png'),
         shot_caption='Bấm Lưu và gửi duyệt khi trống: 15 lỗi báo cùng lúc, tab Hàng hoá gắn chấm đỏ, 0 yêu cầu gửi lên máy chủ (minh hoạ)')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('13-roi-man-chua-luu.png'),
         shot_caption='Bấm Quay lại khi đã nhập → hộp Thông tin chưa lưu (minh hoạ)')
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Dòng người lập', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', '“<Tên người lập> - <dd/mm/yyyy hh:mm>” góc phải khối Thông tin chung '
     '(màn Tạo: tên người đăng nhập + giờ hiện tại).'),
    ('Yêu cầu hỏi giá', 'Text', 'Read-only', 'PYCHG-xxxxx', '–', 'Theo dữ liệu', '- Số YCHG gốc, gạch chân nét đứt; bấm → Chi tiết YCHG.'),
    ('Thương hiệu – Hãng sản xuất', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', '“<Thương hiệu> — <Hãng>” của nhóm.'),
    ('Người hỏi giá', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', 'Người lập YCHG “<Họ tên> - <phòng> - <mã NV>”.'),
    ('Trạng thái', 'Badge', 'Read-only', '–', '–', 'Đang tạo', 'Màn Tạo luôn “Đang tạo”.'),
    ('Đơn vị tiền tệ', 'Dropdown', 'Enable', 'Danh sách 11 giá trị', 'Có', 'Trống', [
        '- Mặc định: trống, placeholder “Chọn đơn vị tiền tệ”.',
        '- VNĐ · USD · EURO · JPY · RUPEE · CHF · IDR · AUD · CNY · KWR · GBP (tiền tệ đang dùng).',
        '- Chọn → Tỉ giá tự điền tỉ giá của danh mục tiền tệ (vd USD 26,180); tên tiền tệ hiện ở tiêu đề cột “Giá NCC (<tiền tệ>)”.',
        '- Trống khi lưu → “' + MSG_REQ + '”.']),
    ('Tỉ giá', 'Number', 'Enable / Disable', '> 0, 2 số thập phân', 'Có khi tiền tệ khác VNĐ', 'Theo tiền tệ', [
        '- Placeholder “Nhập tỉ giá”, dấu phẩy ngăn nghìn.',
        '- VNĐ: = 1, bị khoá.',
        '- Trống → “' + MSG_REQ + '”; ≤ 0 → “Phải lớn hơn 0”; quá 999,999,999,999 → “Không hợp lệ”.']),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', ['- Placeholder “Nhập ghi chú”.', '- > 255 → “Vui lòng nhập tối đa 255 ký tự.”']),
    ('Thanh tab Hàng hoá / Chi phí', 'Button', 'Enable', '2 tab', '–', 'Hàng hoá', [
        '- Mặc định mở tab Hàng hoá.',
        '- Tab có lỗi gắn chấm đỏ; bấm Lưu mà lỗi nằm ở tab khác → tự chuyển sang tab đó.']),
    ('Bảng Hàng hoá', 'Table/Grid', 'Enable', '10 cột', '–', 'Theo dữ liệu', [
        '- Mỗi dòng = 1 hàng × 1 ĐVT đã khai; ĐVT cơ bản đứng đầu.',
        '- Dòng ĐVT thứ 2 trở đi: STT, Tên, Model trống, cột Mã hàng ghi “↳ cùng mã”.',
        '- Cuộn ngang khi hẹp màn.']),
    ('Cột STT / Tên hàng hoá / Mã hàng / Model', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
     'STT đánh theo HÀNG (không theo dòng); tên / mã / model chỉ ở dòng đầu của hàng.'),
    ('Cột ĐVT', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', 'Tên ĐVT của dòng (vd Tuýp, Thùng 20C-0.4Kg).'),
    ('Cột Chính sách giá nội bộ', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', [
        '- Chỉ ở dòng đầu của hàng; chỉ để tham khảo, không vào công thức YCTG.',
        '- Hàng của chính công ty phiếu: “Hàng hoá của <mã công ty> — không có giá mua nội bộ” (vd TPE).',
        '- Hàng công ty khác, chưa cấu hình: nhãn cam “Chưa cấu hình” + “<mã công ty> chưa khai chính sách cho hãng này”.',
        '- Có chính sách: nhãn “Theo giá vốn” / “Theo giá bán” + “Nhập khẩu <x>% · Tồn kho <y>%”.',
        '- Theo giá vốn: “Giá vốn <mã công ty>: <số>” — chỉ hiện số khi người xem có quyền ' + Q3 + ', không có hiện “—”.',
        '- Luôn có “Giá bán lẻ: <số>” = giá Bán lẻ của công ty quản lý hàng.']),
    ('Cột Giá NCC (<tiền tệ>)', 'Number', 'Enable', '≥ 0, 2 số thập phân', 'Có khi Lưu và gửi duyệt', 'Trống', [
        '- Tiêu đề có dấu *; placeholder “Nhập giá NCC”; chưa chọn tiền tệ thì tiêu đề “Giá NCC (ngoại tệ)”.',
        '- Nhập ở ĐVT cơ bản → các ĐVT khác của cùng hàng (đang trống / đang là số gợi ý) tự điền = giá × hệ số quy đổi; gõ tay vào '
        'ĐVT khác thì giữ số đã gõ.',
        '- Gửi mà trống → “' + MSG_REQ + '”; gửi mà = 0 → “Phải lớn hơn 0”; quá lớn → “Không hợp lệ”.']),
    ('Cột Đơn giá VNĐ', 'Number', 'Read-only', '≥ 0', '–', '0', '- = Giá NCC × Tỉ giá, hiện làm tròn tới đồng, dấu phẩy ngăn nghìn.'),
    ('Cột Thuế NK (%)', 'Number', 'Enable', '0 – 100', 'Không', 'Thuế nhập khẩu khai ở hàng', [
        '- Mặc định: thuế nhập khẩu đã khai ở thông tin hàng (không khai → 0).',
        '- Ngoài 0–100 → “Phải từ 0 đến 100”.']),
    ('Cột Thành tiền sau thuế', 'Number', 'Read-only', '≥ 0', '–', '0', '- = Đơn giá VNĐ × (1 + Thuế NK / 100), làm tròn tới đồng.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Lưu YCTG Đang tạo; không bắt buộc Giá NCC (mục này).'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bắt buộc đủ Giá NCC mọi dòng, hỏi xác nhận rồi gửi (mục 2.10).'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', [
        '- Về nơi đã đi vào (Chi tiết / danh sách YCHG) hoặc danh sách YCTG.',
        '- Đã nhập mà chưa lưu → hộp “Thông tin chưa lưu”: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” nút Thoát / Ở lại.']),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
        '- Thành công: “Đã lưu nháp yêu cầu tính giá”.',
        '- Lỗi: câu của máy chủ (vd “' + MSG_CONFLICT + '”) hoặc “Lưu thất bại, vui lòng thử lại.”']),
])
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở form Tạo', 'System',
     'Before:\n– Kiểm 1 trong 3 quyền xem; nhóm thuộc công ty đang làm việc (không → “' + MSG_GROUP_NF + '”).\n'
     '– Nhóm đã có YCTG / không còn Chờ lập YCTG → “' + MSG_CONFLICT + '”, về danh sách.\n'
     '– Không có ' + Q1 + ' hoặc không phải XNK phân công hiện hành → “' + MSG_NOT_XNK + '” → trang “' + MSG_404PAGE + '”.\n'
     'During:\n– Bung dòng = mọi hàng của nhóm (bỏ hàng tạm) × mọi ĐVT đã khai, ĐVT cơ bản trước; Thuế NK = thuế đã khai ở hàng; '
     'chi phí mặc định theo hãng (nếu hãng có khai).\nAfter:\n– Hiện form, tab Hàng hoá.'),
    ('Chọn Đơn vị tiền tệ', 'Change', 'After:\n– Tỉ giá = tỉ giá của tiền tệ trong danh mục; VNĐ → 1 và khoá ô Tỉ giá.\n'
     '– Tính lại Đơn giá VNĐ, Thành tiền sau thuế, Thành tiền chi phí của mọi dòng.'),
    ('Nhập Giá NCC ở ĐVT cơ bản', 'Change', 'After:\n– ĐVT khác của cùng hàng đang trống / đang là số gợi ý → điền giá × hệ số quy đổi '
     '(vd 10 USD × 20 = 200 cho Thùng 20C-0.4Kg).'),
    ('Bấm Lưu nháp', 'Click',
     'Before:\n– Máy chủ kiểm quyền ' + Q1 + ' (thiếu → “' + MSG_NOPERM + '”) và XNK phân công hiện hành của nhóm.\n'
     'During:\n' + '\n'.join(VALIDATE) + '\n– Nếu có lỗi validate → không thực hiện bước After.\n'
     'After:\n– Tạo YCTG Đang tạo, số PYCTG-xxxxx; máy chủ tính lại mọi số tiền (BR-07).\n'
     '– Nhóm của YCHG → Đang tính giá.\n– Không ghi lịch sử, không gửi thông báo.\n'
     '– Thông báo “Đã lưu nháp yêu cầu tính giá”, về danh sách YCTG.'),
    ('Bấm Quay lại', 'Click', 'After:\n– Có thay đổi chưa lưu → hộp “Thông tin chưa lưu”; Thoát → rời màn, Ở lại → giữ nguyên.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Chọn nhóm cần lập YCTG')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chọn nhóm cần lập YCTG', 'crud', actor=A_XNK, caption='Biểu đồ Use Case — FR-05 Chọn nhóm cần lập YCTG')
d.p('2.5.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Chọn nhóm cần lập yêu cầu tính giá',
    mota='Popup mở từ nút Tạo mới ở danh sách YCTG: liệt kê các nhóm Chờ lập YCTG (chưa có YCTG, YCHG Đang hỏi giá) mà CHÍNH người '
         'đăng nhập đang được phân công XNK ở công ty đang làm việc. Chọn 1 nhóm → mở form Tạo của nhóm đó.',
    tacnhan=A_XNK,
    dieukien='Có quyền ' + Q1 + ' (không có thì không thấy nút Tạo mới).',
    chinh='1. Bấm Tạo mới ở danh sách YCTG.\n2. Popup “Chọn nhóm cần lập yêu cầu tính giá” tải danh sách nhóm.\n'
          '3. Bấm Chọn ở dòng nhóm → popup đóng, mở form Tạo YCTG của nhóm (mục 2.4).',
    phu='• Không có nhóm nào → “Không có nhóm nào đang chờ bạn lập YCTG” (vd có ' + Q1 + ' nhưng không được phân công hãng nào).\n'
        '• Lỗi tải → “Không tải được danh sách nhóm, vui lòng thử lại.”\n• Bấm Đóng / ✕ → đóng popup.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', modal='Chọn nhóm cần lập yêu cầu tính giá', shot=shot('05b-popup-chon-nhom.png'),
         shot_caption='Popup có 2 nhóm Chờ lập YCTG CARLEO (PYCHG-04223, 7 mã) và BESITA (PYCHG-04282) (minh hoạ — nhóm thật, phản hồi '
                      'dựng trên trình duyệt)')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('05-popup-chon-nhom-rong.png'),
         shot_caption='Tài khoản có quyền ' + Q1 + ' nhưng không được phân công hãng nào: popup rỗng (dữ liệu thật)')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Chọn nhóm cần lập yêu cầu tính giá', 'Kèm biểu tượng cây; nút ✕ đóng.'),
    ('Bảng nhóm', 'Table/Grid', 'Read-only', '6 cột', '–', 'Theo dữ liệu', [
        '- Không phân trang; YCHG mới nhất lên trước.',
        '- Cột Yêu cầu hỏi giá: số YCHG (chữ thường, không bấm được).',
        '- Cột Thương hiệu – Hãng sản xuất: “<TH> — <Hãng>”.',
        '- Cột Số mã hàng: số mã hàng khác nhau của nhóm, không tính hàng tạm.',
        '- Cột Người hỏi giá: người lập YCHG.',
        '- Cột Ngày tạo: ngày lập YCHG (dd/mm/yyyy).']),
    ('Nút Chọn', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mỗi dòng 1 nút xanh; bấm → mở form Tạo của nhóm.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '“Không có nhóm nào đang chờ bạn lập YCTG”.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng popup, không làm gì.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tạo mới', 'Click',
     'Before:\n– Kiểm 1 trong 3 quyền xem; không có ' + Q1 + ' → trả danh sách rỗng.\n'
     'During:\n– Lấy nhóm Chờ lập YCTG của công ty đang làm việc, YCHG Đang hỏi giá, chưa có YCTG; giữ nhóm mà người đăng nhập là XNK '
     'phân công HIỆN HÀNH.\nAfter:\n– Hiện popup.'),
    ('Bấm Chọn', 'Click', 'After:\n– Đóng popup, mở form Tạo YCTG của nhóm (mục 2.4); máy chủ kiểm lại điều kiện khi mở form.'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Nhập chi phí')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Nhập chi phí', 'crud', actor=A_XNK, caption='Biểu đồ Use Case — FR-06 Nhập chi phí')
d.p('2.6.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Nhập chi phí (tab Chi phí)',
    mota='Ở form Tạo / Sửa, tab Chi phí cho mỗi dòng hàng × ĐVT nhập nhiều chi phí (vận chuyển, bảo hiểm…). Mỗi chi phí nhập theo Tỉ '
         'lệ (%) của Giá NCC hoặc nhập thẳng Đơn giá (ngoại tệ) — 2 ô ràng nhau; Thành tiền (VNĐ) tự tính.',
    tacnhan=A_XNK,
    dieukien='Đang ở form Tạo / Sửa YCTG.',
    chinh='1. Bấm tab Chi phí.\n2. Ở dòng hàng × ĐVT, bấm “+ Thêm chi phí” — dòng chi phí mới tự chọn chi phí đầu tiên chưa dùng, tỉ lệ 0.\n'
          '3. Chọn Tên chi phí, nhập Tỉ lệ (%) hoặc Đơn giá.\n4. Bấm thùng rác để bỏ 1 dòng chi phí (không hỏi lại).\n'
          '5. Lưu YCTG như mục 2.4 / 2.10.',
    phu='• Dòng chưa có chi phí → “Chưa có chi phí”.\n'
        '• Giá NCC của dòng đang trống / 0 → ô Đơn giá bị khoá (chỉ nhập được Tỉ lệ).\n'
        '• Nhập Đơn giá lớn hơn Giá NCC → tỉ lệ > 100%, khi lưu báo “Phải từ 0 đến 100” (màn không tự kéo số về).\n'
        '• Màn Chi tiết: tab Chi phí chỉ xem, không có “+ Thêm chi phí”, không có cột Hành động.')
d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => + Thêm chi phí', shot=shot('10-tab-chi-phi.png'),
         shot_caption='Tab Chi phí: Tuýp 10 USD — Cước vận tải quốc tế 10% = 1 USD = 26,180 VNĐ; Chi phí vận chuyển nội địa gõ Đơn giá 15 '
                      '→ tỉ lệ 150 (minh hoạ)')
d.layout(menu=MENU + ' => Tạo mới => Lưu nháp', shot=shot('11-loi-ti-le-chi-phi.png'),
         shot_caption='Bấm Lưu nháp: “Phải từ 0 đến 100” dưới Tỉ lệ 150, tab Chi phí gắn chấm đỏ, 0 yêu cầu gửi lên máy chủ (minh hoạ)')
d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Bảng Chi phí', 'Table/Grid', 'Enable', '7 cột', '–', 'Theo dữ liệu', [
        '- Cột Hàng hoá “<mã> — <tên>” + link “+ Thêm chi phí”; cột ĐVT; gộp dòng theo số chi phí của dòng hàng × ĐVT.',
        '- Cột Hành động chỉ ở form Tạo / Sửa.']),
    ('Link + Thêm chi phí', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Thêm 1 dòng chi phí, tự chọn chi phí đầu tiên chưa có trong dòng, Tỉ lệ 0.'),
    ('Tên chi phí', 'Dropdown', 'Enable', 'Danh sách 7 giá trị', 'Có', 'Chi phí đầu tiên chưa dùng', [
        '- Cước vận tải quốc tế · Chi phí vận chuyển nội địa · Phí kiểm định · Chi phí bốc vác · Thuế nhập khẩu · Chi phí khác · Bảo hiểm hàng hóa.',
        '- Trống → “' + MSG_REQ + '”; trùng trong cùng dòng hàng × ĐVT → “Chi phí đã có trong dòng này”.']),
    ('Tỉ lệ (%)', 'Number', 'Enable', '0 – 100, 2 số thập phân', 'Không', '0', [
        '- Giá trị được LƯU (đơn giá, thành tiền máy chủ tính lại).',
        '- Ngoài 0–100 → “Phải từ 0 đến 100”.']),
    ('Đơn giá (<tiền tệ>)', 'Number', 'Enable / Disable', '≥ 0', 'Không', '= Tỉ lệ × Giá NCC', [
        '- = Tỉ lệ / 100 × Giá NCC, làm tròn 2 số thập phân.',
        '- Gõ Đơn giá → Tỉ lệ = Đơn giá / Giá NCC × 100.',
        '- Khoá khi Giá NCC trống / 0.']),
    ('Thành tiền (VNĐ)', 'Number', 'Read-only', '≥ 0', '–', '0', '- = Đơn giá × Tỉ giá, làm tròn tới đồng.'),
    ('Nút Xoá dòng chi phí', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Thùng rác, tooltip “Xoá dòng chi phí”; bỏ ngay, không hỏi lại.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu', '“Chưa có chi phí”.'),
])
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm + Thêm chi phí', 'Click', 'After:\n– Thêm dòng chi phí (chi phí đầu tiên chưa dùng, Tỉ lệ 0).'),
    ('Nhập Tỉ lệ / Đơn giá', 'Change', 'After:\n– Ô còn lại và Thành tiền (VNĐ) tính lại ngay; xoá chữ lỗi của ô.'),
    ('Bấm Lưu', 'Click', 'During:\n– Kiểm chi phí như 2.4.5; máy chủ tính lại Đơn giá = Tỉ lệ × Giá NCC, Thành tiền = Đơn giá × Tỉ giá.'),
])

# ------------------------------------------------------------------ 2.7
d.h3('2.7 Sửa YCTG')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Sửa YCTG', 'crud', actor=A_XNK, caption='Biểu đồ Use Case — FR-07 Sửa YCTG')
d.p('2.7.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Sửa yêu cầu tính giá',
    mota='Người lập sửa YCTG Đang tạo hoặc Không duyệt (bị KTMH từ chối): tiền tệ, tỉ giá, ghi chú, Giá NCC, Thuế NK, chi phí. Danh '
         'sách dòng hàng × ĐVT dựng lại theo nhóm hiện tại.',
    tacnhan=A_XNK,
    dieukien='Là người lập YCTG, còn quyền ' + Q1 + '; YCTG Đang tạo / Không duyệt; nhóm chưa đóng.',
    chinh='1. Bấm Sửa ở danh sách hoặc chân màn Chi tiết.\n2. Form “Sửa yêu cầu tính giá: <số phiếu>” nạp dữ liệu đã lưu; YCTG Không '
          'duyệt hiện dòng “Lý do không duyệt: <lý do>”.\n3. Sửa các ô như mục 2.4 / 2.6.\n'
          '4. Bấm Lưu nháp → YCTG Đang tạo; hoặc Lưu và gửi duyệt → Chờ tính giá (mục 2.10).\n5. Về danh sách YCTG.',
    phu='• Mở thẳng màn Sửa của YCTG không sửa được (người khác, đã gửi, nhóm đóng) → tự chuyển sang màn Chi tiết.\n'
        '• YCTG vừa bị đổi trạng thái ở nơi khác → “' + MSG_CONFLICT + '”.\n'
        '• Nhóm đã đóng → “' + MSG_CLOSED + '”.\n'
        '• Lưu ý: Lưu nháp YCTG Không duyệt sẽ đưa YCTG về Đang tạo (dòng lý do không duyệt không còn hiện, người khác không còn thấy '
        'YCTG, nút Xóa xuất hiện).',
    dacbiet='Không xét lại phân công XNK khi sửa: YCTG thuộc người lập; muốn đổi người thì dùng Bàn giao công việc.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('27-sua-khong-duyet.png'),
         shot_caption='Form Sửa PYCTG-02786 Không duyệt có dòng “Lý do không duyệt: .” (minh hoạ — giả làm người lập trên trình duyệt)')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–', 'Sửa yêu cầu tính giá: <số phiếu>', '–'),
    ('Dòng Lý do không duyệt', 'Text', 'Read-only', '–', '–', 'Ẩn', '- Chỉ khi YCTG Không duyệt: “Lý do không duyệt: <lý do KTMH ghi>”.'),
    ('Các ô Thông tin chung, tab Hàng hoá, tab Chi phí', 'Như mục 2.4 / 2.6', 'Enable', 'Như mục 2.4', 'Như mục 2.4', 'Theo dữ liệu',
     '- Dữ liệu đã lưu; Trạng thái hiện đúng trạng thái hiện tại (Đang tạo / Không duyệt).'),
    ('Nút Lưu nháp / Lưu và gửi duyệt / Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Như mục 2.4; Quay lại về danh sách YCTG.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     ['- “Đã lưu nháp yêu cầu tính giá” / “Đã gửi yêu cầu tính giá”.', '- Lỗi: câu của máy chủ.']),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Sửa', 'System', 'Before:\n– YCTG không nhìn thấy → trang “' + MSG_404PAGE + '”.\n– Không sửa được → chuyển màn Chi tiết.'),
    ('Bấm Lưu nháp', 'Click',
     'Before:\n– Quyền ' + Q1 + ' (thiếu → “' + MSG_NOPERM + '”); khoá YCTG + nhóm; nhóm đóng → “' + MSG_CLOSED + '”.\n'
     '– Không phải người lập / không còn Đang tạo, Không duyệt → “' + MSG_CONFLICT + '”.\n'
     'During:\n' + '\n'.join(VALIDATE) + '\nAfter:\n– Ghi lại toàn bộ dòng + chi phí; YCTG → Đang tạo; thông báo “Đã lưu nháp yêu cầu tính giá”.'),
])

# ------------------------------------------------------------------ 2.8
d.h3('2.8 Xem chi tiết YCTG')
d.p('2.8.1 Giới thiệu')
d.rule_ref(DETAIL_RULE, anchor='detail')
d.intro_table(
    ten='Xem chi tiết yêu cầu tính giá',
    mota='Xem YCTG ở chế độ chỉ đọc: Thông tin chung, tab Hàng hoá (cả cột Chính sách giá nội bộ), tab Chi phí, giá bán mới (mục 2.13), '
         'Ghi chú duyệt & lịch sử của nhóm; chân màn có các nút theo quyền.',
    tacnhan=A_XNK + '; ' + A_KTMH + '; ' + A_XEM,
    dieukien='Có 1 trong 3 quyền xem; YCTG thuộc công ty đang làm việc; YCTG Đang tạo thì phải là người lập.',
    chinh='1. Bấm số phiếu ở danh sách (hoặc Xử lý, link YCTG ở YCHG / PTG, thông báo [YCTG]).\n'
          '2. Màn “Chi tiết yêu cầu tính giá: <số phiếu>” hiện dữ liệu chỉ đọc.\n3. Bấm Quay lại → về danh sách YCTG.',
    phu='• YCTG của công ty khác / nháp người khác / thiếu quyền → trang “' + MSG_404PAGE + '”.\n'
        '• Nhóm đã đóng (Đã tính giá / Không có giá / Huỷ duyệt) → dòng xám có ổ khoá “' + MSG_CLOSED_NOTE + '”; không còn nút ghi.\n'
        '• YCTG Không duyệt → dòng “Lý do không duyệt: <lý do>”.\n'
        '• YCTG đã có PTG nhưng PTG đang nháp của người khác → không hiện nút Xem phiếu tính giá (không lộ số PTG).')
d.p('2.8.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('14-chi-tiet-da-tinh-gia.png'),
         shot_caption='Chi tiết PYCTG-03162 Đã tính giá: EURO tỉ giá 30,927.74, dòng “Nhóm hàng đã kết thúc (Đã tính giá)”, chân màn Xem '
                      'phiếu tính giá · In (dữ liệu thật)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('17-chi-tiet-tab-chi-phi.png'),
         shot_caption='Tab Chi phí chỉ xem: 3 chi phí của PYCTG-03162 (dữ liệu thật)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('16-lich-su.png'),
         shot_caption='Khối Ghi chú duyệt & lịch sử của nhóm: XNK duyệt → Lập yêu cầu tính giá → Duyệt tính giá (dữ liệu thật)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('20-chi-tiet-khong-duyet.png'),
         shot_caption='PYCTG-02786 Không duyệt: dòng Lý do không duyệt; người xem không phải người lập chỉ có In (dữ liệu thật)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('21-nhom-da-dong.png'),
         shot_caption='PYCTG-01403 Không duyệt thuộc nhóm Huỷ duyệt (“Chuyển hệ thống”): chỉ còn xem (dữ liệu thật)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('22-dang-tinh-gia-ptg-nhap-nguoi-khac.png'),
         shot_caption='PYCTG-00177 Đang tính giá, PTG đang là nháp của người khác: không có nút Xem phiếu tính giá (dữ liệu thật)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('29-chinh-sach-co-1092.png'),
         shot_caption='Cột Chính sách giá nội bộ đủ 3 kiểu — người xem CÓ quyền ' + Q3 + ': “Giá vốn TPE: 2,310,000” (minh hoạ — DB dev '
                      'chưa có chính sách cho công ty mua)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('30-chinh-sach-khong-1092.png'),
         shot_caption='Cùng phiếu, người xem KHÔNG có quyền ' + Q3 + ': “Giá vốn TPE: —”, Giá bán lẻ vẫn hiện (minh hoạ)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('23-nhap-nguoi-khac-404.png'),
         shot_caption='Mở thẳng PYCTG-02874 Đang tạo của người khác → trang 404 (dữ liệu thật)')
d.p('2.8.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Chi tiết yêu cầu tính giá: <số phiếu>', '–'),
    ('Dòng nhóm đã kết thúc', 'Text', 'Hiển thị', '–', 'Ẩn',
     ['- Chỉ khi nhóm Đã tính giá / Không có giá / Huỷ duyệt.', '- “' + MSG_CLOSED_NOTE + '”, nền xám, biểu tượng ổ khoá.']),
    ('Thông tin chung', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Dòng người lập “<tên> - <dd/mm/yyyy hh:mm>”.',
        '- Yêu cầu hỏi giá (link) · Thương hiệu – Hãng · Người hỏi giá · Trạng thái (nhãn màu) · Đơn vị tiền tệ · Tỉ giá · Ghi chú.',
        '- Không có dấu * ở nhãn.']),
    ('Dòng Lý do không duyệt', 'Text', 'Read-only', '–', 'Ẩn', '- Chỉ khi YCTG Không duyệt: “Lý do không duyệt: <lý do>”.'),
    ('Tab Hàng hoá / Chi phí', 'Table/Grid', 'Read-only', 'Như mục 2.4 / 2.6', 'Theo dữ liệu', [
        '- Cùng bộ cột như form, ô nhập bị khoá.',
        '- Số tiền hiện là số tính từ Giá NCC × Tỉ giá × Thuế / Tỉ lệ chi phí (BR-07).',
        '- Cột Chính sách giá nội bộ: như mục 2.4; giá vốn chỉ hiện với quyền ' + Q3 + '.']),
    ('Dòng “Giá bán mới áp ngày …” + nút Chi tiết kết quả', 'Text / Button', 'Hiển thị / Ẩn', '–', 'Ẩn', '- Chỉ khi YCTG đã có kết quả → mục 2.13.'),
    ('Khối Ghi chú duyệt & lịch sử', 'Table/Grid', 'Read-only', '4 cột', 'Theo dữ liệu', [
        '- Cột Người thực hiện · Hành động · Nội dung · Thời gian (dd/mm/yyyy hh:mm), mới → cũ.',
        '- Là dòng thời gian của NHÓM: gồm bước YCHG (XNK duyệt…), YCTG (Lập yêu cầu tính giá, KTMH không duyệt) và PTG (Lập phiếu tính '
        'giá, Gửi duyệt giá, Giá bị từ chối, Duyệt tính giá, Xoá phiếu tính giá).',
        '- Chưa có dòng nào → “Chưa có lịch sử”.']),
    ('Chân màn', 'Button', 'Enable / Ẩn', '–', 'Theo cờ quyền', [
        '- Tính giá (xanh): KTMH, YCTG Chờ tính giá chưa có PTG (mục 2.12).',
        '- Xem phiếu tính giá: YCTG đã có PTG người xem thấy được.',
        '- Sửa: người lập, Đang tạo / Không duyệt (mục 2.7).',
        '- Từ chối (đỏ): KTMH, Chờ tính giá (mục 2.11).',
        '- Xóa (đỏ): người lập, Đang tạo (mục 2.9).',
        '- In: luôn hiện (mục 2.14). Quay lại: về danh sách YCTG.']),
], required=False)
d.p('2.8.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Chi tiết', 'System',
     'Before:\n– Thiếu cả 3 quyền → “' + MSG_NO_VIEW + '”; YCTG công ty khác / nháp người khác / không có → “' + MSG_NOTFOUND +
     '”. Cả 2 trường hợp màn hình chuyển trang “' + MSG_404PAGE + '”.\n'
     'During:\n– Tính cờ nút ở máy chủ; giá vốn công ty quản lý chỉ trả khi có ' + Q3 + '.\nAfter:\n– Hiện dữ liệu chỉ đọc.'),
    ('Bấm số YCHG / Xem phiếu tính giá', 'Click', 'After:\n– Mở Chi tiết YCHG / Chi tiết PTG.'),
])

# ------------------------------------------------------------------ 2.9
d.h3('2.9 Xoá YCTG')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Xoá YCTG', 'action', actor=A_XNK, caption='Biểu đồ Use Case — FR-09 Xoá YCTG')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xoá. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu tính giá tại phần mô tả chi tiết.',
           anchor='delete')
d.intro_table(
    ten='Xoá yêu cầu tính giá',
    mota='Người lập xoá hẳn YCTG Đang tạo (kèm dòng hàng, chi phí). Nhóm của YCHG quay về Chờ lập YCTG để lập lại.',
    tacnhan=A_XNK,
    dieukien='Có quyền ' + Q1 + '; là người lập; YCTG Đang tạo; nhóm chưa đóng.',
    chinh='1. Bấm Xóa ở danh sách hoặc chân màn Chi tiết.\n'
          '2. Hộp “Xác nhận xóa”: “Xóa yêu cầu tính giá <số phiếu>? Nhóm hàng sẽ về \"Chờ lập YCTG\".”\n3. Bấm Xóa.\n'
          '4. Thông báo “Đã xoá yêu cầu tính giá”; danh sách tải lại / về danh sách.',
    phu='• Bấm Hủy / ✕ → không xoá.\n• YCTG vừa được gửi ở nơi khác → “' + MSG_CONFLICT + '”.\n'
        '• YCTG Không duyệt KHÔNG xoá được (chỉ sửa rồi gửi lại).',
    dacbiet='Xoá cứng, không hoàn tác; số phiếu đã dùng không cấp lại; không ghi lịch sử, không thông báo.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', shot=shot('28-xac-nhan-xoa.png'),
         shot_caption='Hộp Xác nhận xóa (minh hoạ — PYCTG-02786 giả làm Đang tạo của mình trên trình duyệt; bấm Hủy, không xoá)')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xóa', 'Icon Button', 'Enable / Ẩn', 'Ẩn khi không đủ điều kiện', 'Thùng rác đỏ ở danh sách; nút đỏ “Xóa” ở chân màn Chi tiết.'),
    ('Hộp xác nhận', 'Modal', 'Hiển thị', 'Ẩn', ['- Tiêu đề “Xác nhận xóa”.',
     '- “Xóa yêu cầu tính giá <số phiếu>? Nhóm hàng sẽ về \"Chờ lập YCTG\".”', '- Nút đỏ “Xóa” / “Hủy”.']),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     ['- Thành công: “Đã xoá yêu cầu tính giá”.', '- Lỗi: câu của máy chủ hoặc “Xóa thất bại”.']),
], required=False, scope=False)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xóa trong hộp xác nhận', 'Click',
     'Before:\n– Thiếu ' + Q1 + ' → “' + MSG_NOPERM + '”; YCTG không nhìn thấy → “' + MSG_NOTFOUND + '”; nhóm đóng → “' + MSG_CLOSED + '”.\n'
     '– Không phải người lập / không còn Đang tạo → “' + MSG_CONFLICT + '”.\n'
     'After:\n– Xoá chi phí, dòng hàng, YCTG.\n– Nhóm Đang tính giá → Chờ lập YCTG (Lập YCTG / Huỷ duyệt hiện lại ở YCHG).\n'
     '– Thông báo “Đã xoá yêu cầu tính giá”, tải lại danh sách.'),
])

# ------------------------------------------------------------------ 2.10
d.h3('2.10 Gửi tính giá')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Gửi tính giá', 'action', actor=A_XNK, caption='Biểu đồ Use Case — FR-10 Gửi tính giá')
d.p('2.10.2 Giới thiệu')
d.rule_ref(NOTICE_RULE, anchor='notice')
d.intro_table(
    ten='Gửi yêu cầu tính giá (Lưu và gửi duyệt)',
    mota='Từ form Tạo / Sửa, XNK bấm Lưu và gửi duyệt: lưu YCTG và chuyển Chờ tính giá; mọi KTMH của công ty nhận thông báo.',
    tacnhan=A_XNK,
    dieukien='Như Tạo (mục 2.4) hoặc Sửa (mục 2.7); mọi dòng hàng × ĐVT có Giá NCC > 0.',
    chinh='1. Ở form Tạo / Sửa, bấm Lưu và gửi duyệt.\n2. Hộp “Gửi yêu cầu tính giá”: “Gửi yêu cầu tính giá <số phiếu | mới> (<n> dòng '
          'hàng × ĐVT) cho Kế toán mua hàng tính giá?”\n3. Bấm Lưu và gửi duyệt.\n'
          '4. Thông báo “Đã gửi yêu cầu tính giá”; về danh sách YCTG; YCTG Chờ tính giá.',
    phu='• Còn dòng chưa có Giá NCC / Giá NCC = 0 → báo đỏ, không mở hộp xác nhận.\n• Bấm Hủy → không gửi, giữ form.\n'
        '• Gửi lại YCTG Không duyệt → Chờ tính giá, KTMH nhận thông báo lần nữa.',
    dacbiet='Gửi không đổi trạng thái hàng và không ghi giá (trạng thái hàng chỉ đổi khi lưu Phiếu tính giá).')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Lưu và gửi duyệt', shot=shot('12-xac-nhan-gui.png'),
         shot_caption='Hộp xác nhận gửi (14 dòng hàng × ĐVT) — bấm Hủy, không gửi (minh hoạ)')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Nút xanh biểu tượng máy bay giấy ở chân form Tạo / Sửa.'),
    ('Hộp xác nhận', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', [
        '- Tiêu đề “Gửi yêu cầu tính giá”.',
        '- “Gửi yêu cầu tính giá <số phiếu> (<n> dòng hàng × ĐVT) cho Kế toán mua hàng tính giá?” — YCTG chưa lưu ghi “mới”; n = số dòng.',
        '- Nút “Lưu và gửi duyệt” / “Hủy”.']),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- Thành công: “Đã gửi yêu cầu tính giá”.', '- Lỗi: câu của máy chủ.']),
])
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu và gửi duyệt', 'Click',
     'Before:\n– Kiểm trên màn: tiền tệ, tỉ giá, ghi chú, mọi Giá NCC > 0, thuế, chi phí; có lỗi → báo đỏ, dừng.\n– Hộp xác nhận.'),
    ('Bấm Lưu và gửi duyệt trong hộp', 'Click',
     'Before:\n– Quyền ' + Q1 + ' (thiếu → “' + MSG_NOPERM + '”); Tạo: XNK phân công hiện hành; Sửa: người lập, Đang tạo / Không duyệt, '
     'nhóm chưa đóng.\nDuring:\n' + '\n'.join(VALIDATE + VALIDATE_SEND) + '\n– Nhóm không còn hàng có ĐVT → “' + MSG_NO_UNIT + '”.\n'
     'After:\n– Lưu dòng + chi phí (máy chủ tính lại số); YCTG → Chờ tính giá; nhóm → Đang tính giá (khi tạo).\n'
     '– Ghi lịch sử nhóm “Lập yêu cầu tính giá”, nội dung = số phiếu.\n'
     '– Gửi thông báo tới mọi người có quyền ' + Q2 + ' tại công ty phiếu: “[YCTG] Chờ duyệt: <số phiếu>. Nhóm: <TH> — <Hãng>”.\n'
     '– Thông báo “Đã gửi yêu cầu tính giá”, về danh sách YCTG.'),
])

# ------------------------------------------------------------------ 2.11
d.h3('2.11 KTMH từ chối YCTG')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'KTMH từ chối YCTG', 'action', actor=A_KTMH, caption='Biểu đồ Use Case — FR-11 KTMH từ chối YCTG')
d.p('2.11.2 Giới thiệu')
d.rule_ref(NOTICE_RULE, anchor='notice')
d.intro_table(
    ten='Từ chối yêu cầu tính giá',
    mota='KTMH trả YCTG Chờ tính giá về XNK kèm lý do bắt buộc (giá NCC / chi phí chưa đúng); YCTG thành Không duyệt, XNK sửa rồi gửi lại.',
    tacnhan=A_KTMH,
    dieukien='Có quyền ' + Q2 + ' tại công ty phiếu; YCTG Chờ tính giá; nhóm chưa đóng.',
    chinh='1. Mở Chi tiết (thông báo “[YCTG] Chờ duyệt”, nút Xử lý hoặc số phiếu).\n2. Bấm Từ chối ở chân màn.\n'
          '3. Popup “Từ chối yêu cầu tính giá” (dòng phụ “<số phiếu> — trả về XNK sửa giá NCC / chi phí”): nhập Lý do từ chối.\n'
          '4. Bấm Từ chối.\n5. Thông báo “Đã từ chối yêu cầu tính giá”; về danh sách YCTG.',
    phu='• Lý do trống → “' + MSG_REQ + '”, popup không đóng.\n• Lý do > 255 → “Vui lòng nhập tối đa 255 ký tự.”\n'
        '• YCTG vừa được người khác xử lý → “' + MSG_CONFLICT + '”, màn Chi tiết tải lại.\n• Bấm Đóng / ✕ → không từ chối.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xử lý', shot=shot('24-cho-tinh-gia-ktmh.png'),
         shot_caption='Chi tiết YCTG Chờ tính giá với KTMH: chân màn Tính giá · Từ chối · In (minh hoạ — PYCTG-02786 giả làm Chờ tính giá)')
d.layout(menu=MENU + ' => Xử lý => Từ chối', shot=shot('25-popup-tu-choi.png'), shot_caption='Popup Từ chối yêu cầu tính giá (minh hoạ)')
d.layout(menu=MENU + ' => Xử lý => Từ chối', shot=shot('26-tu-choi-thieu-ly-do.png'),
         shot_caption='Bấm Từ chối khi chưa nhập lý do: “Bắt buộc phải nhập”, popup giữ nguyên, 0 yêu cầu gửi lên máy chủ (minh hoạ)')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Từ chối (chân màn)', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn', '- Nút đỏ, chỉ với KTMH khi YCTG Chờ tính giá, nhóm chưa đóng.'),
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Từ chối yêu cầu tính giá', 'Dòng phụ “<số phiếu> — trả về XNK sửa giá NCC / chi phí”.'),
    ('Lý do từ chối', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống', [
        '- Nhãn có dấu *; placeholder “Nhập lý do từ chối”.',
        '- Trống → “' + MSG_REQ + '”; > 255 → “Vui lòng nhập tối đa 255 ký tự.”',
        '- Cắt khoảng trắng đầu / cuối.']),
    ('Nút Từ chối / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Từ chối (đỏ): gửi.\n- Đóng: đóng popup.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- Thành công: “Đã từ chối yêu cầu tính giá”.', '- Lỗi: câu của máy chủ.']),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Từ chối trong popup', 'Click',
     'Before:\n– Quyền ' + Q2 + ' tại công ty phiếu (thiếu → “' + MSG_NOPERM + '”); YCTG không nhìn thấy → “' + MSG_NOTFOUND + '”; nhóm đóng → “' +
     MSG_CLOSED + '”.\n– YCTG không còn Chờ tính giá → “' + MSG_CONFLICT + '”.\n'
     'During:\n– Lý do trống → “' + MSG_REQ + '”; > 255 → “Vui lòng nhập tối đa 255 ký tự.” (hiện dưới ô, popup giữ nguyên).\n'
     'After:\n– YCTG → Không duyệt; ghi lý do, người từ chối, thời điểm.\n'
     '– Lịch sử nhóm “KTMH không duyệt”, nội dung “<số phiếu>. <lý do>”.\n'
     '– Thông báo cho người lập YCTG: “[YCTG] Yêu cầu làm lại: <số phiếu>. Lý do: <lý do>”.\n'
     '– Thông báo “Đã từ chối yêu cầu tính giá”, về danh sách.'),
])

# ------------------------------------------------------------------ 2.12
d.h3('2.12 Tính giá / Xem phiếu tính giá')
d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Tính giá / Xem phiếu tính giá', 'action', actor=A_KTMH,
            caption='Biểu đồ Use Case — FR-12 Tính giá / Xem phiếu tính giá')
d.p('2.12.2 Giới thiệu')
d.rule_ref(DETAIL_RULE, anchor='detail')
d.intro_table(
    ten='Tính giá (mở lập Phiếu tính giá) / Xem phiếu tính giá',
    mota='KTMH chấp nhận YCTG bằng cách bấm Tính giá → mở màn Tạo phiếu tính giá kế thừa YCTG. Khi PTG được lưu, YCTG chạy theo PTG: '
         'Đang tính giá → Chờ duyệt giá → Đã tính giá. YCTG đã có PTG có nút Xem phiếu tính giá.',
    tacnhan=A_KTMH + '; ' + A_XEM,
    dieukien='Tính giá: quyền ' + Q2 + ', YCTG Chờ tính giá, chưa có PTG, nhóm chưa đóng. Xem PTG: YCTG đã có PTG không phải nháp của người khác.',
    chinh='1. Ở danh sách (icon máy tính) hoặc chân màn Chi tiết, bấm Tính giá.\n'
          '2. Mở màn Tạo phiếu tính giá của YCTG (đặc tả ở SRS Phiếu tính giá); Quay lại về đúng nơi đã bấm.\n'
          '3. KTMH lưu PTG → YCTG Đang tính giá; nút Tính giá biến mất, nút Xem phiếu tính giá xuất hiện.',
    phu='• Bấm Tính giá không có hộp xác nhận (chỉ điều hướng); chưa lưu PTG thì YCTG vẫn Chờ tính giá.\n'
        '• PTG gửi duyệt giá → YCTG Chờ duyệt giá; có dòng giá bị từ chối → YCTG về Đang tính giá; mọi dòng được duyệt (hoặc công ty '
        'tắt duyệt giá) → YCTG Đã tính giá, nhóm Đã tính giá.\n'
        '• Xoá PTG nháp → YCTG về Chờ tính giá.\n'
        '• 2 KTMH cùng lập PTG cho 1 YCTG → người sau nhận “' + MSG_CONFLICT + '”.')
d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Xử lý => Tính giá', shot=shot('24-cho-tinh-gia-ktmh.png'),
         shot_caption='Nút Tính giá ở chân màn Chi tiết YCTG Chờ tính giá (minh hoạ)')
d.layout(menu=MENU + ' => Xem phiếu tính giá', shot=shot('14-chi-tiet-da-tinh-gia.png'),
         shot_caption='YCTG Đã tính giá có nút Xem phiếu tính giá (PTG-03178) (dữ liệu thật)')
d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Tính giá', 'Button / Icon Button', 'Enable / Ẩn', '–', 'Ẩn', [
        '- Chân màn Chi tiết: nút xanh “Tính giá” (máy tính).',
        '- Danh sách: icon máy tính, tooltip “Tính giá”.',
        '- Hiện khi: quyền ' + Q2 + ' · YCTG Chờ tính giá · chưa có PTG · nhóm chưa đóng.']),
    ('Nút Xem phiếu tính giá', 'Button / Icon Button', 'Enable / Ẩn', '–', 'Ẩn', [
        '- Hiện khi YCTG đã có PTG không phải nháp của người khác.',
        '- Bấm → Chi tiết PTG.']),
    ('Nhãn trạng thái YCTG', 'Badge', 'Read-only', '6 giá trị', 'Theo dữ liệu', '- Đang tính giá (xanh dương) · Chờ duyệt giá (tím) · Đã tính giá (xanh lá) đổi theo PTG.'),
], required=False)
d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tính giá', 'Click', 'After:\n– Mở màn Tạo phiếu tính giá của YCTG (máy chủ kiểm lại quyền ' + Q2 + ', YCTG Chờ tính giá, chưa có PTG).'),
    ('PTG được lưu / gửi duyệt / duyệt / xoá', 'System',
     'After:\n– Lưu PTG: YCTG → Đang tính giá; hàng Chờ tính giá bán → Đang tính giá.\n– Gửi duyệt giá: YCTG → Chờ duyệt giá.\n'
     '– Có dòng giá bị từ chối: YCTG → Đang tính giá.\n– Mọi dòng áp giá: YCTG → Đã tính giá, ghi người / thời điểm duyệt; nhóm Đã tính giá; sinh kết quả.\n'
     '– Xoá PTG: YCTG → Chờ tính giá.'),
])

# ------------------------------------------------------------------ 2.13
d.h3('2.13 Xem giá bán mới')
d.p('2.13.1 Biểu đồ Usecase')
d.uc_figure('FR-13', 'Xem giá bán mới', 'view', actor=A_XEM, caption='Biểu đồ Use Case — FR-13 Xem giá bán mới')
d.p('2.13.2 Giới thiệu')
d.rule_ref(DETAIL_RULE, anchor='detail')
d.intro_table(
    ten='Xem giá bán mới (Chi tiết kết quả)',
    mota='Ở Chi tiết YCTG đã có kết quả, bật “Chi tiết kết quả” để xem giá bán mới dưới từng dòng hàng × ĐVT: 6 loại giá + ĐMGG. CHỈ có '
         'giá bán — không ai cần quyền Xem giá vốn để xem.',
    tacnhan=A_XEM + '; ' + A_KTMH + '; ' + A_XNK,
    dieukien='Thấy được YCTG; YCTG đã có kết quả (PTG đã áp giá).',
    chinh='1. Mở Chi tiết YCTG Đã tính giá.\n2. Góc phải khối Chi tiết: “Giá bán mới áp ngày <dd/mm/yyyy>” và nút Chi tiết kết quả.\n'
          '3. Bấm Chi tiết kết quả → dưới mỗi dòng hiện bảng giá mới; nút đổi thành “Ẩn chi tiết kết quả”.\n'
          '4. Bấm ✕ ở 1 bảng để ẩn riêng dòng đó; link “▸ Hiện giá mới” dưới ĐVT để hiện lại.',
    phu='• Chưa có kết quả → không có dòng “Giá bán mới áp ngày” và nút Chi tiết kết quả.\n'
        '• Bấm lại nút → tắt toàn bộ, đặt lại các dòng đã ẩn.\n'
        '• Mở từ thông báo / link có bật sẵn kết quả → bảng giá hiện ngay.\n'
        '• Giá đang áp dụng có thể khác bảng này nếu sau đó giá được sửa ở màn Cập nhật giá bán (bảng là bản chụp lúc áp).')
d.p('2.13.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Chi tiết kết quả', shot=shot('15-chi-tiet-ket-qua.png'),
         shot_caption='PYCTG-03162 MLER-AMAT8574091 (Bộ): Bán lẻ … Đại lý cấp 3 22,500,000 ĐMGG 5%, TMĐT 29,250,000 (dữ liệu thật)')
d.layout(menu=MENU + ' => Xem chi tiết => Chi tiết kết quả', shot=shot('19-ket-qua-nhieu-dvt.png'),
         shot_caption='PYCTG-01939 ENEOS: mỗi ĐVT (Thùng, Tuýp) 1 bảng giá mới (dữ liệu thật)')
d.p('2.13.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Dòng “Giá bán mới áp ngày …”', 'Text', 'Read-only', 'dd/mm/yyyy', 'Ẩn', '- Chữ xanh lá, biểu tượng tích; ngày PTG được áp giá.'),
    ('Nút Chi tiết kết quả / Ẩn chi tiết kết quả', 'Button', 'Enable / Ẩn', '–', 'Ẩn (mặc định tắt)', '- Chỉ khi có ít nhất 1 dòng có kết quả.'),
    ('Bảng giá mới (dưới dòng hàng × ĐVT)', 'Table/Grid', 'Read-only', '7 cột', 'Theo dữ liệu', [
        '- Viền trái xanh lá, nền xanh rất nhạt; ghim lề trái khi cuộn ngang.',
        '- Cột: Bán lẻ · Theo lô · Đại lý cấp 1 · Đại lý cấp 2 · Đại lý cấp 3 · TMĐT · nút ✕.',
        '- Ô giá: giá mới (dấu phẩy ngăn nghìn) + dòng phụ “ĐMGG <x>%”; loại giá không có trong kết quả để trống.']),
    ('Nút ✕ / link ▸ Hiện giá mới', 'Icon Button', 'Enable', '–', 'Hiển thị',
     ['- ✕ (tooltip “Ẩn giá mới của dòng này”): ẩn bảng của dòng đó.', '- “▸ Hiện giá mới” dưới cột ĐVT: hiện lại.']),
], required=False)
d.p('2.13.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở Chi tiết', 'System', 'During:\n– Lấy kết quả của YCTG: CHỈ giá bán + ĐMGG theo hàng × ĐVT, ngày áp, người tính giá, số PTG.\n'
     'After:\n– Có kết quả → hiện dòng ngày áp + nút.'),
    ('Bấm Chi tiết kết quả', 'Click', 'After:\n– Bật / tắt bảng giá mới mọi dòng; đặt lại các dòng đã ẩn.'),
])

# ------------------------------------------------------------------ 2.14
d.h3('2.14 In YCTG')
d.p('2.14.1 Biểu đồ Usecase')
d.uc_figure('FR-14', 'In YCTG', 'io', actor=A_XEM, caption='Biểu đồ Use Case — FR-14 In YCTG')
d.p('2.14.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột (phần In). Chỉ bổ sung các quy tắc riêng của màn Yêu cầu tính giá tại phần mô tả '
           'chi tiết.', anchor='excel')
d.intro_table(
    ten='In phiếu yêu cầu tính giá',
    mota='Xem trước rồi in “PHIẾU YÊU CẦU TÍNH GIÁ”: thông tin chung + bảng dòng hàng × ĐVT với giá NCC, đơn giá VNĐ, thuế, sau thuế, '
         'tổng chi phí + khối ký XNK lập / Kế toán mua hàng. Letterhead theo công ty phiếu.',
    tacnhan=A_XEM + '; Người dùng đã đăng nhập',
    dieukien='Thấy được YCTG (1 trong 3 quyền xem).',
    chinh='1. Bấm In (hành động dòng ở danh sách / chân màn Chi tiết).\n'
          '2. Popup “Xem trước yêu cầu tính giá <số phiếu>” hiện bản in.\n3. Bấm In trong popup → hộp thoại in của trình duyệt.',
    phu='• YCTG không nhìn thấy / thiếu quyền → báo lỗi, không có bản in.\n• Bấm ✕ → đóng popup.')
d.p('2.14.3 Layout màn hình')
d.layout(menu=MENU + ' => In', shot=shot('18-in-phieu.png'),
         shot_caption='Bản xem trước PHIẾU YÊU CẦU TÍNH GIÁ PYCTG-03162 (dữ liệu thật; local không có letterhead do môi trường)')
d.p('2.14.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In', 'Icon Button / Button', 'Enable', '–', 'Hiển thị', 'Máy in ở danh sách; nút “In” ở chân màn Chi tiết.'),
    ('Bản in', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Tiêu đề “PHIẾU YÊU CẦU TÍNH GIÁ”, Số phiếu, Ngày tạo.',
        '- Khối: Yêu cầu hỏi giá · Thương hiệu – Hãng · Người hỏi giá · Tiền tệ / tỉ giá · Người lập · Trạng thái · Ghi chú (trống → “.....”).',
        '- Bảng 9 cột: STT · Mã hàng · Tên hàng hoá · ĐVT · Giá NCC (<tiền tệ>) · Đơn giá VNĐ · Thuế NK (%) · Sau thuế · Chi phí (tổng VNĐ của dòng).',
        '- Không có hàng → “Không có hàng hoá”.',
        '- Khối ký: XNK lập · Kế toán mua hàng.',
        '- Không in giá vốn, không in chính sách giá nội bộ.']),
    ('Popup xem trước', 'Modal', 'Hiển thị', '–', 'Ẩn', 'Nút In (mở hộp thoại in) và ✕.'),
], required=False)
d.p('2.14.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In', 'Click', 'Before:\n– Kiểm quyền xem + YCTG nhìn thấy được.\nAfter:\n– Dựng bản in ở máy chủ, hiện trong popup xem trước.'),
    ('Bấm In trong popup', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt.'),
])

# ========================================================= PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('chỉ ghi các quy tắc đặc thù của Yêu cầu tính giá; quy tắc dùng chung không nhắc lại.',
           anchor='list', head='Quy tắc áp dụng', lead='Ngoài SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi = công ty phiếu',
     ['– YCTG thuộc công ty của YCHG = công ty đang làm việc; công ty lấy từ phiên làm việc, không nhận từ màn hình.',
      '– YCTG công ty khác: không hiện, không mở, không thao tác được — “' + MSG_NOTFOUND + '”.',
      '– Mọi quyền xét tại công ty phiếu; super admin không được miễn.'], ['Mọi chức năng']),
    ('BR-02', 'Quyền xem = 1 trong 3 quyền',
     ['– Xem danh sách / chi tiết / in / chọn nhóm cần có ' + Q1 + ' HOẶC ' + Q2 + ' HOẶC ' + Q3 + '.',
      '– Không có quyền nào: menu ẩn; gọi chức năng → “' + MSG_NO_VIEW + '”; mở thẳng phiếu → trang 404.',
      '– Không phân quyền theo phòng ban / cấp quản lý.'], ['Xem danh sách', 'Xem chi tiết', 'In']),
    ('BR-03', 'Nháp chỉ người lập thấy',
     ['– YCTG Đang tạo chỉ người lập thấy (danh sách, chi tiết, in); người khác mở thẳng → trang 404.',
      '– Các trạng thái khác: mọi người có quyền xem trong công ty thấy.'], ['Xem danh sách', 'Xem chi tiết']),
    ('BR-04', 'Lập YCTG từ nhóm',
     ['– Chỉ từ nhóm Chờ lập YCTG của YCHG Đang hỏi giá, nhóm chưa có YCTG; 1 nhóm – 1 YCTG.',
      '– Người lập phải có ' + Q1 + ' VÀ là XNK được phân công HIỆN HÀNH của Thương hiệu × Hãng × công ty phiếu; không → “' + MSG_NOT_XNK + '”.',
      '– Nhóm đã có YCTG / đổi trạng thái → “' + MSG_CONFLICT + '”; 2 người lập cùng lúc chỉ 1 người thành công.',
      '– Lưu (nháp hay gửi) → nhóm Đang tính giá; xoá YCTG → nhóm về Chờ lập YCTG.'], ['Tạo', 'Chọn nhóm', 'Xoá']),
    ('BR-05', 'Dòng hàng × mọi ĐVT',
     ['– Dòng = mọi hàng của nhóm × mọi ĐVT đã khai; ĐVT cơ bản trước; hàng tạm không đi sang YCTG.',
      '– Không có ô tick: mọi dòng phải có Giá NCC > 0 khi gửi; Lưu nháp cho phép để trống.',
      '– Thuế NK mặc định = thuế nhập khẩu khai ở hàng; chi phí mặc định theo hãng (nếu hãng có khai).',
      '– Sửa: dòng dựng lại theo nhóm hiện tại; số gửi lên ghép theo hàng + ĐVT, dòng lạ bỏ qua.'], ['Tạo', 'Sửa']),
    ('BR-06', 'Gợi ý giá theo ĐVT',
     ['– Nhập Giá NCC ở ĐVT cơ bản → ĐVT khác của cùng hàng đang trống / đang là số gợi ý = giá × hệ số quy đổi (vd 10 × 20 = 200).',
      '– Gõ tay vào ĐVT khác thì giữ nguyên, lần sau không gợi ý đè.'], ['Tạo', 'Sửa']),
    ('BR-07', 'GIÁ — Công thức số tiền, máy chủ tính lại',
     ['– Đơn giá VNĐ = Giá NCC × Tỉ giá.',
      '– Thành tiền sau thuế = Đơn giá VNĐ × (1 + Thuế NK / 100).',
      '– Đơn giá chi phí (ngoại tệ) = Tỉ lệ / 100 × Giá NCC; Thành tiền chi phí (VNĐ) = Đơn giá chi phí × Tỉ giá.',
      '– Làm tròn 2 số thập phân khi lưu; màn hình hiện tới đồng. Vd: 10 USD × 26,180 = 261,800; 85.5 × 26,180 = 2,238,390, thuế 5% '
      '→ 2,350,310; chi phí 10% của 10 USD = 1 USD = 26,180.',
      '– Máy chủ TÍNH LẠI mọi số khi lưu, không lấy số màn hình gửi (khác ERP).'], ['Tạo', 'Sửa', 'Nhập chi phí', 'Xem chi tiết', 'In']),
    ('BR-08', 'Tiền tệ và tỉ giá',
     ['– Tiền tệ bắt buộc (cả khi Lưu nháp); chỉ tiền tệ đang dùng.',
      '– VNĐ: tỉ giá = 1, khoá. Ngoại tệ: tỉ giá mặc định của danh mục tiền tệ, sửa được, > 0, tối đa 999,999,999,999, 2 số thập phân.'],
     ['Tạo', 'Sửa']),
    ('BR-09', 'Kiểm dữ liệu báo đồng thời',
     ['– Câu lỗi: “' + MSG_REQ + '” · “Không tồn tại” · “Phải lớn hơn 0” · “Không hợp lệ” · “' + MSG_MAX + '” · “Vui lòng nhập tối đa 255 ký '
      'tự.” · “Phải từ 0 đến 100” · “Chi phí đã có trong dòng này” · “Chi phí vượt giới hạn lưu trữ” · “' + MSG_NO_UNIT + '”.',
      '– Mọi lỗi báo cùng lúc dưới đúng ô; tab có lỗi gắn chấm đỏ, tự chuyển tab, cuộn tới lỗi đầu tiên.',
      '– Rời form có thay đổi → “Thông tin chưa lưu”.'], ['Tạo', 'Sửa', 'Nhập chi phí', 'Gửi tính giá']),
    ('BR-10', 'Trạng thái YCTG',
     ['– Đang tạo → (gửi) Chờ tính giá → (KTMH từ chối) Không duyệt → (sửa, gửi lại) Chờ tính giá.',
      '– Chờ tính giá → (lưu PTG) Đang tính giá → (PTG gửi duyệt giá) Chờ duyệt giá → (mọi dòng giá duyệt) Đã tính giá; có dòng giá bị '
      'từ chối → Đang tính giá; công ty tắt duyệt giá → Đã tính giá ngay khi PTG Lưu và duyệt; xoá PTG → Chờ tính giá.',
      '– Lưu nháp YCTG Không duyệt → Đang tạo.'], ['Mọi chức năng']),
    ('BR-11', 'Sửa / xoá',
     ['– Sửa: người lập, còn ' + Q1 + ', YCTG Đang tạo / Không duyệt, nhóm chưa đóng; không xét lại phân công.',
      '– Xoá: người lập, YCTG Đang tạo, nhóm chưa đóng; Không duyệt không xoá được.',
      '– Không đủ điều kiện → không có nút; gọi thẳng → “' + MSG_CONFLICT + '”; mở thẳng màn Sửa → chuyển màn Chi tiết.'],
     ['Sửa', 'Xoá']),
    ('BR-12', 'Nhóm đã đóng chỉ còn xem',
     ['– Nhóm Đã tính giá / Không có giá / Huỷ duyệt: YCTG chỉ xem, dòng “' + MSG_CLOSED_NOTE + '”.',
      '– Gọi thẳng Sửa / Gửi / Xoá / Từ chối → “' + MSG_CLOSED + '”.'], ['Xem chi tiết', 'Sửa', 'Xoá', 'Từ chối']),
    ('BR-13', 'KTMH từ chối',
     ['– Quyền ' + Q2 + ' tại công ty phiếu; mọi YCTG Chờ tính giá của công ty, không xét phân công hãng.',
      '– Lý do bắt buộc, tối đa 255 ký tự; ghi người / thời điểm từ chối; hiện “Lý do không duyệt: <lý do>”.'], ['Từ chối']),
    ('BR-14', 'Tính giá / xem PTG',
     ['– Nút Tính giá: quyền ' + Q2 + ' + YCTG Chờ tính giá + chưa có PTG + nhóm chưa đóng; chỉ điều hướng sang màn Tạo PTG.',
      '– 1 YCTG – 1 PTG. PTG nháp của người khác: vẫn tính là đã có PTG (ẩn Tính giá) nhưng không hiện số PTG / nút Xem.'],
     ['Tính giá / Xem PTG']),
    ('BR-15', 'GIÁ — Giá vốn và chính sách giá nội bộ',
     ['– Cột Chính sách giá nội bộ chỉ để tham khảo, không vào công thức YCTG.',
      '– Hàng của chính công ty phiếu: “Hàng hoá của <mã cty> — không có giá mua nội bộ”; công ty khác chưa cấu hình: “Chưa cấu hình”.',
      '– Có chính sách: cách tính + tỷ lệ Nhập khẩu / Tồn kho + Giá bán lẻ công ty quản lý (ai xem cũng thấy).',
      '– Theo giá vốn: “Giá vốn <mã cty>: <số>” CHỈ với quyền ' + Q3 + '; không có → “—”, máy chủ không trả số (kể cả KTMH).',
      '– Giá NCC, tỉ giá, thuế, chi phí không bị ẩn với người có quyền xem YCTG.'], ['Tạo', 'Sửa', 'Xem chi tiết']),
    ('BR-16', 'GIÁ — YCTG không ghi giá bán; giá bán mới',
     ['– Lập / gửi / từ chối YCTG KHÔNG ghi giá nào, không đổi trạng thái hàng.',
      '– Giá bán mới chỉ sinh khi PTG được áp giá; là bản chụp: 6 loại giá × ĐVT + ĐMGG (vd PYCTG-03162: Bán lẻ 22,500,000 ĐMGG 5%, '
      'TMĐT 29,250,000 = Bán lẻ × hệ số TMĐT 1,3 của công ty).',
      '– Chỉ giá bán (không giá vốn) ⇒ ai thấy YCTG đều xem được.',
      '– Giá đang áp dụng có thể khác bản chụp nếu sau đó sửa ở màn Cập nhật giá bán.'], ['Xem giá bán mới']),
    ('BR-17', 'Thông báo [YCTG]',
     ['– Gửi (kể cả gửi lại) → mọi người có ' + Q2 + ' tại công ty phiếu: “[YCTG] Chờ duyệt: <số phiếu>. Nhóm: <TH> — <Hãng>”.',
      '– Từ chối → người lập YCTG: “[YCTG] Yêu cầu làm lại: <số phiếu>. Lý do: <lý do>”.',
      '– Bấm thông báo → Chi tiết YCTG. Lưu nháp / xoá không báo. Tên ≤ 50, cả câu ≤ 120 ký tự; lỗi gửi không làm hỏng thao tác.'],
     ['Gửi tính giá', 'Từ chối']),
    ('BR-18', 'Lịch sử theo nhóm',
     ['– Ghi vào dòng thời gian của NHÓM (chung với YCHG / PTG): “Lập yêu cầu tính giá” (mỗi lần gửi, nội dung = số phiếu), “KTMH không '
      'duyệt” (“<số phiếu>. <lý do>”), các bước PTG.',
      '– Lưu nháp và xoá không ghi; xem ở Chi tiết, mới → cũ.'], ['Xem chi tiết']),
    ('BR-19', 'Danh sách',
     ['– 10 dòng / trang (tối đa 100), sắp Ngày tạo giảm dần; sắp được Số phiếu, Ngày tạo.',
      '– Tìm nhanh: số YCTG, số YCHG, mã / tên hàng; ô lọc Trạng thái (6), Thương hiệu, Hãng, Người tạo, Ngày tạo.'],
     ['Xem danh sách', 'Tìm kiếm và lọc']),
    ('BR-20', 'Thao tác đồng thời',
     ['– Mọi thao tác ghi khoá YCTG + nhóm rồi kiểm lại trạng thái trong 1 giao dịch.',
      '– Người sau nhận “' + MSG_CONFLICT + '” (màn Chi tiết tải lại).'], ['Tạo', 'Sửa', 'Xoá', 'Từ chối', 'Tính giá']),
])

# update_fields=False: Word dang mo tren may user — buoc cap nhat muc luc tren macOS se dong Word.
d.save(update_fields=os.environ.get('SRS_UPDATE_TOC') == '1')
print('OK ->', OUT)

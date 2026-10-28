# -*- coding: utf-8 -*-
"""Sinh SRS - Phieu tinh gia (luong Chuyen doi hang hoa, man 5/5) — form chuan 2026-09-24.

Pham vi: man "Phieu tinh gia" (Tai chinh > Quan ly gia - CTKM > Gia ban > Phieu tinh gia; menu isShow 1663 | 1664 | 1092) gom
danh sach, loc, cau hinh cot, Lap PTG tu YCTG Cho tinh gia (loi vao: nut Tinh gia o YCTG / nut Tao moi + popup Chon YCTG), tab
Hang hoa + Chi phi (KTMH sua so XNK), tab Tinh gia (chi phi khac, gia nhap kho, 6 loai gia, DMGG, gia hieu luc), popup Tam tinh,
Sua (Dang tao / Gia bi tu choi), Chi tiet, Xoa, Luu va duyet (ap gia ngay), Luu va gui duyet (sang man Duyet gia ban + bao nguoc),
Xem gia ban moi, In phieu / In ket qua.

Nguon doi chieu code: worktree wt-chuyen-doi-hang-hoa nhanh feat/chuyen-doi-hang-hoa (hrm-api 39c4a91fe, hrm-client 5c14659e8)
— doc ngay 16/10/2026.
  BE: Modules/MasterData/Routes/api.php (nhom price-calculates: xem KHONG gate route — service doi 1663|1664|1092; store/update/
      destroy gate 1664), Http/Controllers/V1/PriceCalculation/PriceCalculateController, Services/PriceCalculation/{PriceCalculateAccess,
      PriceCalculateService (paginate, filterOptions, pendingRequests, draftFromRequest, show, payload, estimate, policySnapshot),
      PriceCalculateWriter (create/update/delete/submit/validate/compute), PriceCalculateFinalizer (settle/finalize/copyAppliedPrices/
      writeResult/notify), PriceCalculateNotifier, PriceAskingNotifier::groupPriced, PriceCalculationPrintService::calculate/result,
      PriceCalculateRequestAccess (hasCalculate/hasCost/canView, MSG_NO_VIEW)}, Services/ProductPrice/{ProductPriceWriter::apply/
      resolvePrices/ecomCoefficient, ProductPriceApprovalSubmitter::submit, ProductPriceListService::approvalRule/needsApproval,
      ProductPriceNotifier::submittedFromCalculate}, Entities/PriceCalculation/{PriceCalculate, PriceCalculateProduct}.
  FE: pages/finance/price-calculates/{index, add, _id/index, _id/edit}.vue, components/finance/price-calculate/{PriceCalculateForm,
      PriceSellTable, PolicyEstimateModal, RequestPickerModal}.vue, components/sale/price-calculate/{PriceInputGoodsTable,
      PriceInputCostsTable, PolicyCell}.vue, utils/productPriceModel.js (Calc), utils/mixins/priceInputRowsMixin.js,
      components/subsystem-menu/finance.js (muc "Phieu tinh gia" nhom Gia ban, isShow 1663 | 1664 | 1092).

Anh chup: Playwright MCP 1440x900, cong 3031 (worktree, DB hrm_erp_giacty), tai khoan E2E Assign (Cty 1, co san 1092 1657 1658).
Tao role tam TMP_SRS_PTG_1664 (id 129858, chi quyen 1664 Cty 1) de chup THAT nut Tao moi + popup Chon YCTG rong — DA GO +
cache:forget; dem roles/rhp/ehr ve 130/20967/1718. Moi lenh ghi bi chan tren trinh duyet (route.fulfill) — DB khong doi
(PTG Cty 1 van 1:2285 · 3:1; YCTG Cty 1 van 3:4 · 4:2285 · 5:19 · 1:1). Cong ty dev deu TAT duyet gia (is_company_price = 0).
  - THAT: 00-menu, 01 (2.285 PTG Cty 1, co 1664), 01c (khong 1664 — khong co Tao moi), 02/02b/03, 04 (popup rong — DB dev khong
    co YCTG Cho tinh gia), 05..10 (PTG-03178 EURO 31,900, 3 chi phi, ban in + in ket qua), 11 (Xem gia ban moi -> PYCHG-04283),
    12 (PTG-00215 nhap nguoi khac -> 404), 13 (PTG-01959 2 DVT Thung/Tuyp), 14 (PTG-02618 TMDT 2 dong gia hieu luc).
  - MINH HOA (sua phan hoi tren trinh duyet, khong ghi DB): 01b (dong Dang tao / Cho duyet gia / Gia bi tu choi), 15/15b (popup co
    YCTG), 16..24 (form Lap dung tu PTG-01959 that: he so dang ap dung, phep tinh that cua man; Luu bi chan: tra "Da ap gia ban"),
    21..23 (cong ty gia lam BAT quy che duyet gia), 25/25b (PTG-03170 gia lam Cho duyet gia), 26/27 (gia lam Gia bi tu choi), 28/29
    (PTG-03178 gia lam Dang tao cua minh — bam Huy), 30..34 (chinh sach + Tam tinh TPSG gia lap — DB dev khong co chinh sach cho
    hang cong ty khac), 35 (loi chan cheo tra tu may chu gia lap), 36 (tra loi khong quyen xem), 37 (PTG-02618 gia lam Dang tao).
  - icon_phanhe / icon_rail_quanlygia / icon_nhom_giaban: dung lai cua bo Cap nhat gia ban; icon_tinhgia + 04a: bo YC tinh gia.

Chay:  python3 .plans/gop-db/quan-ly-hang-hoa/srs-testcase/gen_srs_phieu-tinh-gia.py   (Word dang mo -> update_fields=False)
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

SHOTS = os.path.join(HERE, 'phieu-tinh-gia_shots')
OUT = os.path.join(HERE, 'SRS - Phiếu tính giá.docx')


def shot(name):
    return os.path.join(SHOTS, name)


A_KTMH = 'Kế toán mua hàng (KTMH)'
A_XEM = 'Người xem phiếu tính giá'
MENU = 'Phân hệ Tài chính => Quản lý giá - CTKM => Giá bán => Phiếu tính giá'
MENU_YCTG = 'Phân hệ Bán hàng => Yêu cầu => Hàng hóa => YC tính giá => Tính giá'
SCREEN = 'Phiếu tính giá'

d = SrsDoc(out=OUT, menu=MENU, route='/finance/price-calculates',
           full_url='http://hrm/finance/price-calculates', img_prefix='ptg_')
d.set_menu_icons({k: shot(v) for k, v in {
    'Phân hệ Tài chính': 'icon_phanhe.png',
    'Quản lý giá - CTKM': 'icon_rail_quanlygia.png',
    'Giá bán': 'icon_nhom_giaban.png',
    'Phiếu tính giá': 'icon_phieutinhgia.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cấu hình cột': 'icon_cauhinhcot.png',
    'Tạo mới': 'icon_taomoi.png',
    'Chọn': 'icon_chon.png',
    'Tính giá': 'icon_tinhgia.png',
    'Sửa': 'icon_sua.png',
    'Xóa': 'icon_xoa.png',
    'Lưu nháp': 'icon_luunhap.png',
    'Lưu và duyệt': 'icon_luuvaduyet.png',
    'Lưu và gửi duyệt': 'icon_luuvaguiduyet.png',
    'Giá hiệu lực': 'icon_giahieuluc.png',
    'Tạm tính': 'icon_tamtinh.png',
    'Xem giá bán mới': 'icon_xemgiabanmoi.png',
    'In': 'icon_in.png',
    'In kết quả': 'icon_inketqua.png',
}.items()})

Q1 = 'XNK xử lý yêu cầu hỏi giá'
Q2 = 'Tính giá bán hàng hoá'
Q3 = 'Xem giá vốn hàng hoá'
Q_DUYET = 'Duyệt giá bán hàng hoá'
MSG_NOPERM = 'Bạn không có quyền thực hiện chức năng này'
MSG_NO_VIEW = 'Bạn không có quyền xem yêu cầu tính giá'
MSG_NOTFOUND = 'Không tìm thấy phiếu tính giá'
MSG_REQ_NOTFOUND = 'Không tìm thấy yêu cầu tính giá'
MSG_NO_CALC = 'Bạn không có quyền Tính giá bán hàng hoá'
MSG_CONFLICT = 'Trạng thái đã bị thay đổi. Vui lòng load lại trang'
MSG_CLOSED = 'Nhóm hàng đã đóng, yêu cầu tính giá chỉ còn xem.'
MSG_CLOSED_NOTE = 'Nhóm hàng đã kết thúc (<trạng thái nhóm>) — phiếu tính giá chỉ còn xem.'
MSG_404PAGE = 'Không tìm thấy hoặc không được cấp quyền truy cập trang'
MSG_REQ = 'Bắt buộc phải nhập'
MSG_MAX = 'Không được lớn hơn 999,999,999,999.'
MSG_SAVED = 'Đã lưu phiếu tính giá'
MSG_APPLIED = 'Đã áp giá bán'
MSG_SUBMITTED = 'Đã gửi giá sang màn Duyệt giá bán'
MSG_PENDING_G4 = 'Đang có yêu cầu duyệt giá ở màn Cập nhật giá bán'
MSG_PENDING_PTG = 'Giá đang chờ duyệt ở <số phiếu tính giá khác>'
MSG_NO_ROWS = 'Yêu cầu tính giá không có dòng hàng hoá nào'
CTY = '<tên công ty phiếu>'

# ============================================================== TRANG DAU
d.title_block(SCREEN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu tính giá (phân hệ Tài chính) — chứng từ cuối của luồng tính giá bán '
    '(YCHG → YCTG → Phiếu tính giá → giá áp), nơi Kế toán mua hàng chốt giá nhập kho và 6 loại giá bán cho hàng hoá, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền, phép tính giá và luồng trạng thái của Phiếu tính giá (PTG).',
    'Làm rõ ai làm gì: XEM cần 1 trong 3 quyền “' + Q1 + '”, “' + Q2 + '”, “' + Q3 + '” tại công ty đang làm việc; LẬP / SỬA / XOÁ / '
    'DUYỆT chỉ người có quyền “' + Q2 + '” (KTMH), và chỉ trên phiếu do chính mình lập.',
    'Làm rõ phần GIÁ — trọng tâm của màn: giá nhập kho = thành tiền sau thuế + tổng chi phí + chi phí khác (máy chủ tính lại); giá bán '
    '= hệ số × giá nhập kho làm tròn trăm (sửa tay được); Bán lẻ lan sang 4 loại giá; TMĐT = Bán lẻ × hệ số TMĐT của công ty; giá hiệu '
    'lực tương lai; giá nào được GHI vào bộ giá của công ty phiếu và khi nào.',
    'Làm rõ 2 nhánh chốt giá theo quy chế duyệt giá của CÔNG TY PHIẾU × hãng: công ty tắt duyệt → “Lưu và duyệt” áp giá ngay (cả giá '
    'vốn = giá nhập kho); công ty bật duyệt → “Lưu và gửi duyệt” sinh yêu cầu ở màn Duyệt giá bán, kết quả duyệt từng dòng báo ngược '
    'về phiếu (Đã duyệt / Giá bị từ chối).',
    'Làm rõ quyền “' + Q3 + '”: chỉ quyết định có thấy giá vốn của CÔNG TY QUẢN LÝ hàng (khối Chính sách giá nội bộ, popup Tạm tính) '
    'hay không; máy chủ không trả số khi thiếu quyền.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('PTG', 'Phiếu tính giá — số phiếu PTG-xxxxx (nối dãy số của ERP), sinh khi lưu lần đầu. 1 YCTG có tối đa 1 PTG.'),
    ('YCTG', 'Yêu cầu tính giá — XNK lập, KTMH bấm Tính giá để lập PTG (đặc tả ở SRS Yêu cầu tính giá).'),
    ('YCHG / Nhóm hàng', 'Yêu cầu hỏi giá gốc; nhóm = 1 cặp Thương hiệu — Hãng sản xuất. PTG kế thừa đúng 1 nhóm qua YCTG.'),
    ('Công ty phiếu', 'Công ty của YCTG = công ty đang làm việc khi lập PTG (“Công ty tính giá” trên form). Mọi giá của PTG ghi vào bộ '
     'giá của công ty này, không đụng công ty khác.'),
    ('KTMH', 'Kế toán mua hàng — người có quyền “' + Q2 + '” tại công ty phiếu.'),
    ('Dòng hàng × ĐVT', 'Mỗi dòng PTG = 1 hàng × 1 đơn vị tính (giống YCTG); ĐVT thứ 2 trở đi hiện “↳ cùng mã”.'),
    ('Giá nhập kho', 'Thành tiền sau thuế + Tổng chi phí (VNĐ) + Chi phí khác của dòng — làm “giá vốn” để tính giá bán; khi giá được '
     'áp, số này ghi thành giá vốn của ĐVT tại công ty phiếu.'),
    ('Hệ số', 'Hệ số nhân trên giá nhập kho cho từng loại giá (0 đến dưới 100, 2 số thập phân).'),
    ('Giá công thức', 'Giá nhập kho × Hệ số (làm tròn đồng; TMĐT làm tròn nghìn) — chỉ để tham chiếu, không lưu.'),
    ('6 loại giá', 'Bán lẻ · Giá bán theo lô · Đại lý cấp 1 · Đại lý cấp 2 · Đại lý cấp 3 · Giá bán thương mại điện tử (online) — TMĐT.'),
    ('ĐMGG', 'Định mức giảm giá tối đa (%) của từng loại giá, 0 – 100.'),
    ('Giá hiệu lực', 'Giá sẽ áp dụng từ 1 ngày tương lai (“↳ giá sẽ áp dụng”), tối đa 1 dòng / loại giá.'),
    ('Hệ số TMĐT', 'Cấu hình của công ty phiếu (dev: 1,3). TMĐT = Bán lẻ × hệ số TMĐT.'),
    ('Quy chế duyệt giá', 'Cấu hình công ty: bật duyệt giá + áp mọi hãng hoặc danh sách hãng. Bật ⇒ giá phải qua màn Duyệt giá bán.'),
    ('Chính sách giá nội bộ', 'Cách công ty quản lý hàng bán lại cho công ty phiếu (Theo giá vốn + % / Theo giá bán − %) với 2 tỷ lệ Nhập '
     'khẩu nguyên lô, Tồn kho — chỉ để tham khảo.'),
    ('Kết quả tính giá / Giá bán mới', 'Bản chụp giá đã áp (6 loại × ĐVT + ĐMGG + giá hiệu lực) sinh khi PTG Đã duyệt; xem ở YCHG.'),
], widths=[1.6, 4.4])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Mọi quyền xét TẠI công ty đang làm việc (= công ty phiếu; phiếu công ty khác coi như không tồn tại). Super admin không được '
    'miễn. Có ÍT NHẤT 1 trong 3 quyền dưới đây mới xem được PTG; không có quyền nào → menu “Phiếu tính giá” ẩn, mọi chức năng báo '
    '“' + MSG_NO_VIEW + '” (nguyên văn máy chủ), mở thẳng phiếu ra trang “' + MSG_404PAGE + '”.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1, [
        '- Chỉ XEM: danh sách, chi tiết, in phiếu / in kết quả, popup Tạm tính, Xem giá bán mới.',
        '- Không thấy nút Tạo mới, Sửa, Xóa, Lưu nháp, Lưu và duyệt / gửi duyệt.']),
    ('Q2', Q2, [
        '- Xem như Q1.',
        '- Thấy nút Tạo mới (popup liệt kê MỌI YCTG Chờ tính giá của công ty, không xét phân công hãng) và nút Tính giá ở YCTG.',
        '- Lập PTG; Sửa / Xóa / Lưu và duyệt / Lưu và gửi duyệt PTG do CHÍNH MÌNH lập (người lập mất Q2 thì cũng mất các nút này).',
        '- Nhận thông báo “[PTG] Đã duyệt / Từ chối” cho phiếu mình lập.']),
    ('Q3', Q3, [
        '- Xem như Q1.',
        '- Thấy giá vốn của công ty quản lý hàng (chính sách Theo giá vốn) ở ô Mã hàng / cột Chính sách giá nội bộ và trong popup Tạm tính '
        '(kể cả giá mua suy từ giá vốn). Thiếu Q3 → các ô này hiện “—”, máy chủ không trả số.',
        '- KHÔNG che Giá NCC, Đơn giá VNĐ, Giá nhập kho, giá bán của chính PTG.']),
], widths=[0.7, 1.9, 3.4])
d.p('Quyền liên quan ở màn khác (không gán trên màn này): “' + Q_DUYET + '” — người duyệt các dòng giá PTG gửi sang màn Duyệt giá '
    'bán và nhận thông báo “[GIA] Chờ duyệt”.')
d.p('Nhóm quyền quyết định phạm vi dữ liệu (KHÔNG phải quyền gán — phạm vi tính theo dữ liệu phiếu, áp cho người đã có Q1/Q2/Q3):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Người lập PTG', 'Thấy PTG Đang tạo (nháp) của chính mình; PTG Đang tạo của người khác không hiện ở danh sách, mở thẳng → '
     'trang “' + MSG_404PAGE + '” (DB dev: PTG-00215 nháp của người khác).'),
    ('V2', 'Người có Q1 / Q2 / Q3 trong công ty', 'Thấy mọi PTG Chờ duyệt giá, Giá bị từ chối, Đã duyệt của công ty đang làm việc. '
     'Không phân quyền theo phòng ban / bộ phận / cấp quản lý.'),
    ('V3', 'Công ty khác', 'Không thấy, không thao tác được PTG của công ty khác (“' + MSG_NOTFOUND + '”). Đổi công ty đang làm việc '
     'thì danh sách đổi theo.'),
], widths=[0.7, 1.9, 3.4])

d.h2('2 Ma trận phân quyền')
d.p('✅ = được, ❌ = không được. Cột Q2 tính cho người lập phiếu ở các dòng Sửa / Xóa / Lưu và duyệt / gửi duyệt.')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách PTG', '✅', '✅', '✅', '❌ (menu ẩn)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '✅', '❌'),
    ('FR-04 Lập PTG (Lưu nháp)', '❌', '✅', '❌', '❌'),
    ('FR-05 Chọn YCTG cần tính giá (popup)', '❌ (không có nút)', '✅', '❌', '❌'),
    ('FR-06 Kiểm tra / sửa số đầu vào', '❌ (chỉ xem)', '✅ khi lập / sửa', '❌ (chỉ xem)', '❌'),
    ('FR-07 Tính giá bán (tab Tính giá)', '❌ (chỉ xem)', '✅ khi lập / sửa', '❌ (chỉ xem)', '❌'),
    ('FR-08 Tạm tính giá mua nội bộ', '✅ (giá vốn “—”)', '✅ (giá vốn “—” nếu thiếu Q3)', '✅ có giá vốn', '❌'),
    ('FR-09 Sửa PTG', '❌', '✅ người lập, Đang tạo / Giá bị từ chối', '❌', '❌'),
    ('FR-10 Xem chi tiết PTG', '✅', '✅', '✅', '❌ (trang 404)'),
    ('FR-11 Xoá PTG', '❌', '✅ người lập, Đang tạo', '❌', '❌'),
    ('FR-12 Lưu và duyệt (áp giá ngay)', '❌', '✅ người lập, công ty tắt duyệt', '❌', '❌'),
    ('FR-13 Lưu và gửi duyệt / gửi lại', '❌', '✅ người lập, công ty bật duyệt', '❌', '❌'),
    ('FR-14 Xem giá bán mới', '✅', '✅', '✅', '❌'),
    ('FR-15 In phiếu / In kết quả', '✅', '✅', '✅', '❌'),
], widths=[2.1, 1.0, 1.4, 0.8, 0.7])
d.p('Lưu ý: giá vốn công ty quản lý chỉ hiện với Q3 — kể cả KTMH (Q2) không có Q3 cũng chỉ thấy “—”. Giá nhập kho của PTG (sẽ thành '
    'giá vốn của công ty phiếu khi áp) KHÔNG bị che theo Q3.')

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_KTMH, [0, 1, 2, 3, 4, 5, 6, 7]), (A_XEM, [0, 6, 7])],
    [('FR-01', 'Xem danh sách PTG', 'view'),                   # 0
     ('FR-04', 'Lập PTG', 'crud'),                              # 1
     ('FR-09', 'Sửa PTG', 'crud'),                              # 2
     ('FR-11', 'Xoá PTG', 'action'),                            # 3
     ('FR-12', 'Lưu và duyệt (áp giá ngay)', 'action'),         # 4
     ('FR-13', 'Lưu và gửi duyệt / gửi lại', 'action'),         # 5
     ('FR-14', 'Xem giá bán mới', 'view'),                      # 6
     ('FR-15', 'In phiếu / In kết quả', 'io')],                 # 7
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-05', 'Chọn YCTG cần tính giá', 'crud', 'extend', [1], None),
     ('FR-06', 'Kiểm tra / sửa số đầu vào', 'crud', 'extend', [1, 2], None),
     ('FR-07', 'Tính giá bán', 'crud', 'extend', [1, 2], None),
     ('FR-08', 'Tạm tính giá mua nội bộ', 'view', 'extend', [1, 2], None),
     ('FR-10', 'Xem chi tiết PTG', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu tính giá')

d.h2('2 Đặc tả chi tiết từng chức năng')

LIST_RULE = ('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn '
             'Phiếu tính giá tại phần mô tả chi tiết.')
CREATE_RULE = ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn Phiếu tính giá '
               'tại phần mô tả chi tiết.')
NOTICE_RULE = '- Thông báo và Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn Phiếu tính giá tại phần mô tả chi tiết.'
DETAIL_RULE = '- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Phiếu tính giá tại phần mô tả chi tiết.'

VALIDATE_FMT = [
    '– (ngoại tệ, không phải Giá bị từ chối) Tỉ giá trống → “' + MSG_REQ + '”; ≤ 0 → “Phải lớn hơn 0”; quá lớn → “Không hợp lệ” '
    '(màn hình) / “' + MSG_MAX + '” (máy chủ).',
    '– Ghi chú > 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”; Ghi chú dòng phiếu > 1000 → “Vui lòng nhập tối đa 1000 ký tự.”',
    '– Giá NCC âm / không phải số → “Không hợp lệ”; Thuế NK ngoài 0–100 → “Phải từ 0 đến 100”.',
    '– Dòng chi phí chưa chọn tên → “' + MSG_REQ + '”; trùng → “Chi phí đã có trong dòng này”; Tỉ lệ ngoài 0–100 → “Phải từ 0 đến 100”; '
    'chi phí quá lớn → “Chi phí vượt giới hạn lưu trữ”.',
    '– Chi phí khác âm → “Không hợp lệ”; giá nhập kho > 999,999,999,999 → “Giá nhập kho vượt giới hạn lưu trữ”.',
    '– Hệ số ngoài khoảng → “Phải từ 0 đến dưới 100”; Giá bán quá lớn → “Không hợp lệ”; ĐMGG ngoài 0–100 → “Phải từ 0 đến 100”.',
    '– Giá hiệu lực: giá trống → “' + MSG_REQ + '”; hệ số trống → “' + MSG_REQ + '”, ngoài 0–99 → “Phải từ 0 đến 99”; ngày trống → '
    '“Bắt buộc phải chọn”, không phải ngày tương lai → “Phải chọn ngày tương lai”; > 1 dòng → “Chỉ được 1 giá hiệu lực”.',
    '– Mọi lỗi báo cùng lúc, dưới đúng ô; tab có lỗi gắn chấm đỏ, tự chuyển sang tab lỗi đầu tiên (Hàng hoá → Chi phí → Tính giá) và '
    'cuộn tới ô lỗi; không lưu gì.',
]
VALIDATE_SEND = [
    '– (chỉ Lưu và duyệt / Lưu và gửi duyệt) Mọi dòng có thể sửa: Giá NCC trống → “' + MSG_REQ + '”, = 0 → “Phải lớn hơn 0”; Hệ số '
    'trống → “' + MSG_REQ + '”; Giá bán trống → “' + MSG_REQ + '”, = 0 → “Phải lớn hơn 0” (5 loại giá, TMĐT máy chủ tự tính).',
]

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách PTG')
d.p('2.1.1 Giới thiệu')
d.rule_ref(LIST_RULE, anchor='list')
d.intro_table(
    ten='Xem danh sách phiếu tính giá',
    mota='Hiển thị các PTG của CÔNG TY ĐANG LÀM VIỆC dạng bảng phẳng (1 PTG = 1 dòng = 1 nhóm Thương hiệu — Hãng). Từ danh sách mở '
         'Chi tiết, Sửa, Xóa, Xem giá bán mới, In; KTMH bấm Tạo mới để lập PTG.',
    tacnhan=A_KTMH + '; ' + A_XEM + '; Người dùng đã đăng nhập',
    dieukien='Người dùng có 1 trong 3 quyền ' + Q1 + ' / ' + Q2 + ' / ' + Q3 + ' tại công ty đang làm việc.',
    chinh='1. Người dùng vào Phân hệ Tài chính › Quản lý giá - CTKM › Giá bán › Phiếu tính giá (mục đầu tiên của nhóm Giá bán).\n'
          '2. Hệ thống lấy PTG của công ty đang làm việc: mọi PTG đã qua nháp + PTG Đang tạo của chính người dùng; mới lập lên trước, '
          '10 dòng / trang.\n'
          '3. Bấm số phiếu → màn Chi tiết (mục 2.10); bấm số YCTG / YCHG → màn Chi tiết YCTG / YCHG.',
    phu='• Không có quyền nào trong 3 quyền: không thấy mục menu; mở thẳng màn → bảng “Không có dữ liệu phù hợp” kèm thông báo “' +
        MSG_NO_VIEW + '” (hiện 2 lần).\n'
        '• Không có PTG nào / không khớp bộ lọc → “Không có dữ liệu phù hợp”.\n'
        '• PTG Đang tạo của người khác không hiện (DB dev: PTG-00215).\n'
        '• Lỗi tải khác → thông báo “Lỗi khi tải dữ liệu”.')
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('00-menu.png'),
         shot_caption='Menu Tài chính › Quản lý giá - CTKM › Giá bán: Phiếu tính giá đứng đầu nhóm (dữ liệu thật)')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Danh sách PTG công ty 1 — 2.285 phiếu Đã duyệt; tài khoản có quyền ' + Q2 + ' nên thấy Tạo mới (dữ liệu thật)')
d.layout(menu=MENU, shot=shot('01c-khong-co-1664.png'),
         shot_caption='Cùng danh sách với tài khoản chỉ có ' + Q3 + ': không có nút Tạo mới (dữ liệu thật)')
d.layout(menu=MENU, shot=shot('01b-danh-sach-hanh-dong.png'),
         shot_caption='Cột Hành động theo trạng thái: Đang tạo của mình (Sửa · Xóa · In), Chờ duyệt giá (In), Giá bị từ chối (Sửa · In), '
                      'Đã duyệt (Xem giá bán mới · In) (minh hoạ — sửa phản hồi trên trình duyệt)')
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang / khối', 'Label', 'Hiển thị', '–', 'Phiếu tính giá', 'Tiêu đề thanh đầu trang và khối bảng.'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền', [
        '- Chỉ hiện với người có quyền ' + Q2 + ' tại công ty đang làm việc.',
        '- Bấm → popup Chọn yêu cầu tính giá (mục 2.5).']),
    ('Nút Cấu hình cột', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Tooltip “Cấu hình cột hiển thị” → mục 2.3.'),
    ('Bảng phiếu tính giá', 'Table/Grid', 'Read-only', '10 cột', 'Theo dữ liệu', [
        '- Mỗi PTG 1 dòng; cột STT, Số phiếu dính trái khi cuộn ngang.',
        '- Mặc định sắp Ngày lập mới → cũ; sắp được theo Số phiếu, Ngày lập (bấm tiêu đề cột).']),
    ('Cột STT', 'Text', 'Read-only', 'Số nguyên', 'Theo dữ liệu', 'Số thứ tự liên tục qua các trang.'),
    ('Cột Số phiếu', 'Text', 'Read-only', 'PTG-xxxxx', 'Theo dữ liệu', '- Số phiếu là link → bấm mở màn Chi tiết (mục 2.10).'),
    ('Cột Yêu cầu tính giá', 'Text', 'Read-only', 'PYCTG-xxxxx', 'Theo dữ liệu', '- Số YCTG gốc là link → bấm mở Chi tiết YCTG.'),
    ('Cột Yêu cầu hỏi giá', 'Text', 'Read-only', 'PYCHG-xxxxx', 'Theo dữ liệu', '- Số YCHG gốc là link → bấm mở Chi tiết YCHG.'),
    ('Cột Thương hiệu – Hãng sản xuất', 'Text', 'Read-only', '–', 'Theo dữ liệu', '“<Thương hiệu> — <Hãng sản xuất>” của nhóm.'),
    ('Cột Số mã hàng', 'Number', 'Read-only', '≥ 1', 'Theo dữ liệu', 'Số mã hàng KHÁC NHAU của PTG (1 hàng 2 ĐVT vẫn tính 1; vd '
     'PTG-03170: 6).'),
    ('Cột Người lập', 'Text', 'Read-only', '–', 'Theo dữ liệu', '“<Họ tên> - <mã phòng> - <mã NV>” của KTMH lập PTG.'),
    ('Cột Ngày lập', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Ngày lập PTG.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 4 giá trị', 'Theo dữ liệu', [
        '- Đang tạo (xám) · Chờ duyệt giá (tím) · Giá bị từ chối (đỏ) · Đã duyệt (xanh lá).']),
    ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo cờ quyền', [
        '- Sửa (bút): người lập còn quyền ' + Q2 + ', PTG Đang tạo / Giá bị từ chối, nhóm chưa đóng → màn Sửa (mục 2.9).',
        '- Xóa (thùng rác đỏ): người lập còn quyền ' + Q2 + ', PTG Đang tạo, nhóm chưa đóng → hộp xác nhận (mục 2.11).',
        '- Xem giá bán mới (nhãn giá): PTG đã có kết quả (Đã duyệt) → Chi tiết YCHG mở sẵn kết quả của nhóm (mục 2.14).',
        '- In (máy in): luôn hiện → mục 2.15.']),
    ('Chân bảng', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', '10 dòng / trang', [
        '- “Hiển thị a–b / N”: a–b là thứ tự dòng đầu–cuối của trang, N = tổng PTG khớp bộ lọc (vd “Hiển thị 1–10 / 2285”).',
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
     'During:\n– Lấy PTG có công ty = công ty đang làm việc (lấy từ phiên làm việc, không nhận từ màn hình); bỏ PTG Đang tạo của người khác.\n'
     '– Tính cờ nút từng dòng ở máy chủ (Sửa / Xóa / có kết quả) — màn hình chỉ hiện theo cờ; Tạo mới theo cờ quyền ' + Q2 + '.\n'
     'After:\n– Trang 1, 10 dòng, sắp Ngày lập mới → cũ.'),
    ('Bấm tiêu đề cột Số phiếu / Ngày lập', 'Click', 'After:\n– Sắp tăng / giảm; bỏ sắp → Ngày lập giảm dần; về trang 1.'),
    ('Đổi trang / số dòng', 'Click / Change', 'After:\n– Tải lại; đổi số dòng thì về trang 1.'),
    ('Bấm Xem giá bán mới', 'Click', 'After:\n– Mở Chi tiết YCHG của phiếu, bung sẵn “Chi tiết kết quả” của đúng nhóm.'),
    ('Đổi công ty đang làm việc', 'System', 'After:\n– Danh sách tải lại theo công ty mới; PTG công ty cũ biến mất.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của màn Phiếu tính giá tại phần mô tả chi '
           'tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc phiếu tính giá',
    mota='Thu hẹp danh sách theo số PTG / số YCTG / số YCHG / mã / tên hàng, trạng thái, thương hiệu, hãng, người lập và khoảng ngày lập.',
    tacnhan=A_XEM + '; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách PTG.',
    chinh='1. Gõ từ khoá vào ô tìm nhanh rồi nhấn Enter hoặc bấm Tìm kiếm.\n'
          '2. Bấm Tìm kiếm nâng cao để mở các ô lọc; chọn giá trị — mỗi lần chọn là lọc ngay.\n'
          '3. Hệ thống tải lại danh sách từ trang 1.',
    phu='• Bấm Làm mới → xoá mọi điều kiện, sắp lại theo Ngày lập giảm dần.\n'
        '• Hệ thống ghi nhớ bộ lọc trong 10 phút khi quay lại màn từ màn Chi tiết / Sửa.\n'
        '• Không có kết quả → “Không có dữ liệu phù hợp”.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-loc-nang-cao.png'),
         shot_caption='Khối bộ lọc khi mở Tìm kiếm nâng cao (dữ liệu thật)')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02b-loc-trang-thai.png'),
         shot_caption='Ô Trạng thái: 4 giá trị Đang tạo · Chờ duyệt giá · Giá bị từ chối · Đã duyệt (dữ liệu thật)')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
        '- Placeholder “Tìm theo số phiếu, số yêu cầu tính giá, số yêu cầu hỏi giá, mã hoặc tên hàng hoá”.',
        '- Tìm gần đúng trên số PTG, số YCTG, số YCHG, mã hàng và tên hàng ghi trong PTG.']),
    ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     ['- Tìm kiếm: chạy theo từ khoá + ô lọc, về trang 1.', '- Làm mới: xoá mọi ô lọc, về sắp xếp mặc định.']),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Đóng',
     ['- Mặc định khối ô lọc đang đóng.', '- Bấm để mở / đóng (“Ẩn tìm kiếm nâng cao”).']),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', 'Trống', [
        '- Mặc định: trống (mọi trạng thái).',
        '- Đang tạo · Chờ duyệt giá · Giá bị từ chối · Đã duyệt.',
        '- Lọc Đang tạo chỉ ra PTG nháp của chính người dùng.']),
    ('Thương hiệu', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Mặc định: trống.', '- Chỉ liệt kê thương hiệu có trong PTG của công ty, xếp A → Z.']),
    ('Hãng sản xuất', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', ['- Mặc định: trống.', '- Như Thương hiệu, theo hãng.']),
    ('Người lập', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Mặc định: trống.', '- “<Họ tên> - <phòng> - <mã NV>” của người đã lập PTG trong công ty, xếp theo tên.']),
    ('Ngày lập', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống',
     'Khoảng ngày lập PTG, tính trọn cả ngày đầu và ngày cuối.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Nhấn Enter / bấm Tìm kiếm', 'Keypress / Click', 'After:\n– Tải lại từ trang 1 theo từ khoá + ô lọc.'),
    ('Chọn giá trị ô lọc', 'Change', 'After:\n– Lọc ngay, về trang 1.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, sắp theo Ngày lập giảm dần, tải lại trang 1.'),
    ('Quay lại màn danh sách', 'System', 'After:\n– Khôi phục bộ lọc + trạng thái đóng / mở khối lọc trong 10 phút.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Cài đặt bộ lọc và tuỳ chỉnh cột')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Phiếu tính giá tại phần mô tả chi tiết.',
           anchor='excel')
d.intro_table(
    ten='Cài đặt bộ lọc và tuỳ chỉnh cột',
    mota='Ẩn / hiện, đổi thứ tự các ô lọc và các cột của bảng danh sách; cấu hình lưu theo người dùng.',
    tacnhan=A_XEM + '; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách PTG.',
    chinh='1. Bấm nút Cấu hình cột (hoặc Cài đặt bộ lọc).\n2. Tích / bỏ tích, kéo thả để đổi thứ tự.\n3. Bấm Lưu.',
    phu='• Bấm Đóng → không lưu.\n• Cột STT, Số phiếu, Hành động bị khoá (luôn hiện).')
d.p('2.3.2 Layout màn hình')
d.layout(menu=MENU + ' => Cấu hình cột', shot=shot('03-cau-hinh-cot.png'), shot_caption='Popup Tuỳ chỉnh cột (dữ liệu thật)')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', 'Câu dẫn “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '10 cột', 'Không', 'Theo cấu hình đã lưu', [
        '- STT · Số phiếu · Yêu cầu tính giá · Yêu cầu hỏi giá · Thương hiệu – Hãng sản xuất · Số mã hàng · Người lập · Ngày lập · '
        'Trạng thái · Hành động.',
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
d.h3('2.4 Lập PTG')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Lập PTG', 'crud', actor=A_KTMH, caption='Biểu đồ Use Case — FR-04 Lập PTG')
d.p('2.4.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Lập phiếu tính giá (Lưu nháp)',
    mota='KTMH lập PTG từ 1 YCTG Chờ tính giá của công ty: form kế thừa tiền tệ, tỉ giá, mọi dòng hàng × ĐVT, giá NCC, thuế, chi phí của '
         'YCTG; hệ số mỗi loại giá nạp sẵn hệ số ĐANG ÁP DỤNG của hàng tại công ty phiếu nên giá bán gợi ý có ngay. KTMH chỉnh số '
         '(mục 2.6, 2.7) rồi Lưu nháp, hoặc chốt luôn bằng Lưu và duyệt / Lưu và gửi duyệt (mục 2.12, 2.13).',
    tacnhan=A_KTMH,
    dieukien='Có quyền ' + Q2 + ' tại công ty phiếu; YCTG Chờ tính giá, chưa có PTG, nhóm chưa đóng.',
    chinh='1. Mở form bằng 1 trong 2 lối vào: nút Tính giá ở Chi tiết / danh sách YCTG; hoặc nút Tạo mới ở danh sách PTG → Chọn YCTG '
          'trong popup (mục 2.5).\n'
          '2. Form “Lập phiếu tính giá” hiện Thông tin chung (YCTG, YCHG, Thương hiệu – Hãng, Người hỏi giá, Đơn vị tiền tệ, Công ty tính '
          'giá: chỉ đọc; Tỉ giá, Ghi chú: sửa được) và mở sẵn tab Tính giá.\n'
          '3. KTMH kiểm / sửa số đầu vào (tab Hàng hoá, Chi phí), nhập Chi phí khác, hệ số / giá bán / ĐMGG / giá hiệu lực (tab Tính giá).\n'
          '4. Bấm Lưu nháp → PTG Đang tạo, số PTG-xxxxx; thông báo “' + MSG_SAVED + '”; về danh sách PTG.',
    phu='• Thiếu quyền ' + Q2 + ' → “' + MSG_NO_CALC + '” → trang “' + MSG_404PAGE + '”.\n'
        '• YCTG không thấy / công ty khác → “' + MSG_REQ_NOTFOUND + '” → trang 404.\n'
        '• YCTG đã có PTG / không còn Chờ tính giá → thông báo “' + MSG_CONFLICT + '”, về danh sách PTG; nhóm đã đóng → “' + MSG_CLOSED + '”.\n'
        '• 2 KTMH cùng lưu PTG cho 1 YCTG → người sau nhận “' + MSG_CONFLICT + '”.\n'
        '• Lỗi nhập liệu → báo đỏ dưới ô, tab có lỗi gắn chấm đỏ (2.4.5).\n'
        '• Bấm Quay lại khi đã nhập → hộp “Thông tin chưa lưu”; vào từ YCTG thì Quay lại về đúng màn YCTG.\n'
        '• Lưu nháp xong: YCTG → Đang tính giá; hàng Chờ tính giá bán → Đang tính giá; nhóm ghi lịch sử “Lập phiếu tính giá”.',
    dacbiet='Lưu nháp KHÔNG ghi giá nào vào bộ giá công ty. Máy chủ TÍNH LẠI Đơn giá VNĐ, sau thuế, chi phí, giá nhập kho, TMĐT khi '
            'lưu (BR-06, BR-08); giá bán 5 loại lấy đúng số KTMH chốt. Số trên PTG là bản riêng — sửa ở PTG không đổi YCTG.')
d.p('2.4.3 Layout màn hình')
d.p('Đường dẫn màn hình (2 lối vào mở cùng 1 form Lập):')
d.layout(menu=MENU_YCTG, shot=shot('04a-yctg-tinh-gia.png'),
         shot_caption='Lối vào 1: nút Tính giá ở YCTG Chờ tính giá (ảnh của bộ SRS Yêu cầu tính giá — minh hoạ)')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('16-form-lap.png'),
         shot_caption='Form Lập phiếu tính giá từ PYCTG-01939 (ENEOS, VNĐ — tỉ giá 1 khoá), mở sẵn tab Tính giá; chân form “Lưu và '
                      'duyệt sẽ áp giá ngay cho …” (minh hoạ — khung dựng từ PTG-01959 thật trên trình duyệt)')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('24-roi-man-chua-luu.png'),
         shot_caption='Bấm Quay lại khi đã nhập → hộp Thông tin chưa lưu (minh hoạ)')
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Dòng người lập', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', '“<Tên người lập> - <dd/mm/yyyy hh:mm>” góc phải khối Thông tin '
     'chung (màn Lập: người đăng nhập + giờ hiện tại).'),
    ('Yêu cầu tính giá', 'Text', 'Read-only', 'PYCTG-xxxxx', '–', 'Theo dữ liệu', '- Số YCTG, gạch chân nét đứt; bấm → Chi tiết YCTG.'),
    ('Yêu cầu hỏi giá', 'Text', 'Read-only', 'PYCHG-xxxxx', '–', 'Theo dữ liệu', '- Số YCHG; bấm → Chi tiết YCHG.'),
    ('Thương hiệu – Hãng sản xuất', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', '“<Thương hiệu> — <Hãng>” của nhóm.'),
    ('Người hỏi giá', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', 'Người lập YCHG “<Họ tên> - <phòng> - <mã NV>”.'),
    ('Đơn vị tiền tệ', 'Text', 'Read-only', '–', '–', 'Theo YCTG', '- Tiền tệ của YCTG, KHÔNG đổi được ở PTG.'),
    ('Tỉ giá', 'Number', 'Enable / Disable', '> 0, 2 số thập phân', 'Có khi tiền tệ khác VNĐ', 'Tỉ giá của YCTG', [
        '- Mặc định: tỉ giá XNK nhập ở YCTG (vd PYCTG-03162 30,927.74; KTMH sửa thành 31,900 ở PTG-03178).',
        '- VNĐ: = 1, bị khoá. PTG Giá bị từ chối: bị khoá.',
        '- Trống → “' + MSG_REQ + '”; ≤ 0 → “Phải lớn hơn 0”; quá 999,999,999,999 → “Không hợp lệ”.',
        '- Đổi tỉ giá → mọi số VNĐ, giá nhập kho và giá bán chưa sửa tay tính lại.']),
    ('Công ty tính giá', 'Text', 'Read-only', '–', '–', 'Công ty phiếu', 'Tên đầy đủ công ty phiếu — nơi giá sẽ được ghi.'),
    ('Trạng thái', 'Badge', 'Read-only', '–', '–', 'Đang tạo', [
        '- Màn Lập luôn “Đang tạo”.',
        '- Kèm nhãn tím “Bật quy chế duyệt giá” khi công ty phiếu bật duyệt cho hãng của nhóm (mục 2.13).']),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', ['- Placeholder “Nhập ghi chú”.', '- > 255 → “Vui lòng nhập tối đa 255 ký tự.”']),
    ('Thanh tab Hàng hoá / Chi phí / Tính giá', 'Button', 'Enable', '3 tab', '–', 'Tính giá', [
        '- Màn Lập mở sẵn tab Tính giá; màn Sửa / Chi tiết mở tab Hàng hoá (Chờ duyệt giá / Giá bị từ chối mở tab Tính giá).',
        '- Tab có lỗi gắn chấm đỏ; bấm Lưu mà lỗi nằm ở tab khác → tự chuyển sang tab đó.']),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Lưu PTG Đang tạo; chỉ kiểm định dạng, không bắt buộc Giá NCC / hệ số / giá bán.'),
    ('Nút Lưu và duyệt / Lưu và gửi duyệt', 'Button', 'Enable', '–', '–', 'Theo quy chế', [
        '- “Lưu và duyệt” (dấu tích) khi công ty phiếu tắt duyệt giá cho hãng → mục 2.12.',
        '- “Lưu và gửi duyệt” (máy bay giấy) khi bật → mục 2.13.']),
    ('Dòng nhắc chân form', 'Text', 'Read-only', '–', '–', 'Theo quy chế', [
        '- Tắt duyệt: “Lưu và duyệt sẽ áp giá ngay cho ' + CTY + '”.',
        '- Bật duyệt: “' + CTY + ' bật quy chế duyệt giá — giá sẽ gửi sang màn Duyệt giá bán”.']),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', [
        '- Về nơi đã đi vào (Chi tiết YCTG) hoặc danh sách PTG.',
        '- Đã nhập mà chưa lưu → hộp “Thông tin chưa lưu”: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” nút Thoát / Ở lại.']),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
        '- Thành công: “' + MSG_SAVED + '”.',
        '- Lỗi: câu của máy chủ (vd “' + MSG_CONFLICT + '”) hoặc “Lưu thất bại, vui lòng thử lại.”; tải form lỗi: “Không tải được phiếu tính '
        'giá, vui lòng thử lại.”']),
])
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở form Lập', 'System',
     'Before:\n– Kiểm 1 trong 3 quyền xem; thiếu ' + Q2 + ' → “' + MSG_NO_CALC + '” → trang 404.\n'
     '– YCTG không thuộc công ty / nháp người khác → “' + MSG_REQ_NOTFOUND + '” → trang 404; nhóm đóng → “' + MSG_CLOSED + '”, về danh sách.\n'
     '– YCTG không còn Chờ tính giá / đã có PTG → “' + MSG_CONFLICT + '”, về danh sách PTG.\n'
     'During:\n– Dòng = dòng YCTG (hàng × ĐVT) kèm giá NCC, thuế, chi phí XNK đã nhập; Chi phí khác = 0.\n'
     '– Hệ số + ĐMGG mỗi loại giá = hệ số / ĐMGG đang áp dụng của ĐVT tại công ty phiếu; giá bán = tròn trăm(hệ số × giá nhập kho).\n'
     '– Chính sách giá nội bộ đọc mới nhất; giá vốn công ty quản lý chỉ trả khi có ' + Q3 + '.\n'
     'After:\n– Hiện form, tab Tính giá.'),
    ('Bấm Lưu nháp', 'Click',
     'Before:\n– Thiếu ' + Q2 + ' → “' + MSG_NOPERM + '”.\nDuring:\n' + '\n'.join(VALIDATE_FMT) + '\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Khoá YCTG, kiểm lại Chờ tính giá + chưa có PTG; tạo PTG Đang tạo (số PTG-xxxxx), công ty = công ty YCTG.\n'
     '– Máy chủ tính lại số tiền từng dòng (BR-06), TMĐT (BR-08); chụp chính sách giá nội bộ.\n'
     '– YCTG → Đang tính giá; hàng Chờ tính giá bán → Đang tính giá; lịch sử nhóm “Lập phiếu tính giá” (nội dung = số PTG).\n'
     '– Thông báo “' + MSG_SAVED + '”, về danh sách PTG.'),
    ('Bấm Quay lại', 'Click', 'After:\n– Có thay đổi chưa lưu → hộp Thông tin chưa lưu; không → về nơi đã đi vào.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Chọn YCTG cần tính giá')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chọn YCTG cần tính giá', 'crud', actor=A_KTMH, caption='Biểu đồ Use Case — FR-05 Chọn YCTG cần tính giá')
d.p('2.5.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Chọn yêu cầu tính giá (popup)',
    mota='Popup liệt kê các YCTG Chờ tính giá của công ty đang làm việc chưa có PTG, nhóm chưa đóng — để KTMH chọn 1 YCTG mở form Lập.',
    tacnhan=A_KTMH,
    dieukien='Có quyền ' + Q2 + ' (mới thấy nút Tạo mới).',
    chinh='1. Bấm Tạo mới ở danh sách PTG.\n2. Popup “Chọn yêu cầu tính giá” tải danh sách (không phân trang, mới → cũ).\n'
          '3. Bấm Chọn ở 1 dòng → đóng popup, mở form Lập (mục 2.4).',
    phu='• Không có YCTG nào chờ → “Không có yêu cầu tính giá nào đang chờ tính giá” (DB dev hiện là như vậy).\n'
        '• Lỗi tải → “Không tải được danh sách yêu cầu tính giá, vui lòng thử lại.”\n• Bấm Đóng / ✕ → đóng popup.',
    dacbiet='KHÔNG lọc theo phân công hãng: mọi KTMH có quyền ' + Q2 + ' thấy mọi YCTG Chờ tính giá của công ty.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('04-popup-rong.png'),
         shot_caption='Popup Chọn yêu cầu tính giá khi không có YCTG chờ (dữ liệu thật — DB dev không có YCTG Chờ tính giá)')
d.layout(menu=MENU + ' => Tạo mới => Chọn', shot=shot('15-popup-chon-yctg.png'),
         shot_caption='Popup có 2 YCTG chờ — ở 1440px nút Chọn nằm khuất bên phải, phải cuộn ngang (minh hoạ — danh sách dựng trên trình duyệt)')
d.layout(menu=MENU + ' => Tạo mới => Chọn', shot=shot('15b-popup-cuon-ngang.png'),
         shot_caption='Cuộn ngang bảng trong popup mới thấy cột Ngày lập và nút Chọn (minh hoạ)')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Chọn yêu cầu tính giá', 'Kèm biểu tượng danh sách; nút ✕ đóng.'),
    ('Bảng YCTG chờ', 'Table/Grid', 'Read-only', '7 cột', '–', 'Theo dữ liệu', [
        '- Yêu cầu tính giá · Yêu cầu hỏi giá · Thương hiệu – Hãng sản xuất · Số mã hàng · Người lập (XNK) · Ngày lập · nút Chọn.',
        '- Không phân trang; rộng hơn khung popup → cuộn ngang.']),
    ('Nút Chọn', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng popup, mở form Lập phiếu tính giá của YCTG đó.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '“Không có yêu cầu tính giá nào đang chờ tính giá”.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng popup.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tạo mới', 'Click', 'Before:\n– Kiểm quyền xem; thiếu ' + Q2 + ' → danh sách rỗng.\nDuring:\n– Lấy YCTG Chờ tính giá của công ty, '
     'chưa có PTG, nhóm chưa đóng.\nAfter:\n– Hiện popup.'),
    ('Bấm Chọn', 'Click', 'After:\n– Mở form Lập (mục 2.4); máy chủ kiểm lại điều kiện khi mở form.'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Kiểm tra / sửa số đầu vào')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Kiểm tra / sửa số đầu vào', 'crud', actor=A_KTMH, caption='Biểu đồ Use Case — FR-06 Kiểm tra / sửa số đầu vào')
d.p('2.6.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Kiểm tra / sửa số đầu vào (tab Hàng hoá, tab Chi phí)',
    mota='Tab Hàng hoá và Chi phí dùng chung khuôn của YCTG. KTMH được sửa lại số XNK đã nhập (Giá NCC, Thuế NK, chi phí theo tỉ lệ, tỉ '
         'giá) như ERP; YCTG giữ nguyên số cũ.',
    tacnhan=A_KTMH,
    dieukien='Đang ở form Lập / Sửa (dòng còn sửa được).',
    chinh='1. Mở tab Hàng hoá: xem Chính sách giá nội bộ, sửa Giá NCC (<tiền tệ>), Thuế NK (%).\n'
          '2. Mở tab Chi phí: thêm / sửa / xoá dòng chi phí, nhập Tỉ lệ (%) của Giá NCC.\n'
          '3. Đơn giá VNĐ, Thành tiền sau thuế, Thành tiền chi phí, Giá nhập kho ở tab Tính giá tự tính lại.',
    phu='• PTG Giá bị từ chối: chỉ dòng bị từ chối mở sửa; dòng đã duyệt chỉ xem.\n'
        '• Nhập Giá NCC ở ĐVT cơ bản → ĐVT khác của cùng hàng tự gợi ý = giá × hệ số quy đổi (như YCTG).\n'
        '• Lỗi nhập liệu → báo đỏ dưới ô (câu như YCTG, xem 2.4.5).',
    dacbiet='Màn Chi tiết TÍNH LẠI chi phí từ tỉ lệ (không lấy số đã lưu) ⇒ phiếu cũ của ERP có thể lệch vài đồng so với giá vốn đã áp '
            '(vd PTG-03178 Bảo hiểm 0,04%: màn 4,147 / đã lưu 4,466).')
d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('05-chi-tiet.png'),
         shot_caption='Tab Hàng hoá của PTG-03178: Giá NCC 316 EURO, Đơn giá VNĐ 10,080,400 (= 316 × 31,900) (dữ liệu thật)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('06-tab-chi-phi.png'),
         shot_caption='Tab Chi phí của PTG-03178: Cước vận tải quốc tế 15% → 1,512,060; Vận chuyển nội địa 5% → 504,020; Bảo hiểm 0,04% '
                      '→ 4,147 (dữ liệu thật)')
d.layout(menu=MENU + ' => Lưu và gửi duyệt', shot=shot('22-loi-gui-trong.png'),
         shot_caption='Bấm Lưu và gửi duyệt khi Giá NCC / hệ số trống: 22 lỗi báo cùng lúc, tự chuyển tab Hàng hoá, 0 yêu cầu gửi lên máy chủ (minh hoạ)')
d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Bảng Hàng hoá', 'Table/Grid', 'Enable', '10 cột', '–', 'Theo YCTG', [
        '- STT · Tên hàng hoá · Mã hàng · Model · ĐVT · Chính sách giá nội bộ · Giá NCC (<tiền tệ>) · Đơn giá VNĐ · Thuế NK (%) · '
        'Thành tiền sau thuế.',
        '- Dòng ĐVT thứ 2 trở đi: cột Mã hàng ghi “↳ cùng mã”.']),
    ('Cột Chính sách giá nội bộ', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', [
        '- Hàng của chính công ty phiếu: “Hàng hoá của <mã công ty> — không có giá mua nội bộ” (vd TPE).',
        '- Công ty khác chưa cấu hình: nhãn cam “Chưa cấu hình” + “<mã công ty> chưa khai chính sách cho hãng này”.',
        '- Có chính sách: nhãn “Theo giá vốn” / “Theo giá bán” + “Nhập khẩu <x>% · Tồn kho <y>%” + “Giá vốn <mã cty>: <số>” (chỉ với '
        'quyền ' + Q3 + ', thiếu → “—”) + “Giá bán lẻ: <số>”.',
        '- Màn Lập / Sửa: đọc chính sách mới nhất; PTG đã khoá (Chờ duyệt giá / Đã duyệt): hiện bản chụp lúc lưu cuối.']),
    ('Cột Giá NCC (<tiền tệ>)', 'Number', 'Enable / Disable', '≥ 0, 2 số thập phân', 'Có khi Lưu và duyệt / gửi duyệt', 'Theo YCTG', [
        '- Placeholder “Nhập giá NCC”.',
        '- Gửi mà trống → “' + MSG_REQ + '”; = 0 → “Phải lớn hơn 0”; quá lớn → “Không hợp lệ”.']),
    ('Cột Đơn giá VNĐ', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', '- = Giá NCC × Tỉ giá (vd 316 × 31,900 = 10,080,400).'),
    ('Cột Thuế NK (%)', 'Number', 'Enable / Disable', '0 – 100', 'Không', 'Theo YCTG', '- Ngoài 0–100 → “Phải từ 0 đến 100”.'),
    ('Cột Thành tiền sau thuế', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', '- = Đơn giá VNĐ × (1 + Thuế NK / 100) (vd 10,080,400 × 1,1 = 11,088,440).'),
    ('Bảng Chi phí', 'Table/Grid', 'Enable', '6 cột', '–', 'Theo YCTG', [
        '- Hàng hoá · ĐVT · Tên chi phí · Tỉ lệ (%) · Đơn giá (<tiền tệ>) · Thành tiền (VNĐ).',
        '- Đơn giá = Tỉ lệ / 100 × Giá NCC (2 số lẻ); Thành tiền = Đơn giá × Tỉ giá.',
        '- Tên chi phí: 7 chi phí giá hàng hoá (Cước vận tải quốc tế, Chi phí vận chuyển nội địa, Phí kiểm định, Chi phí bốc vác, Thuế '
        'nhập khẩu, Chi phí khác, Bảo hiểm hàng hóa); trùng trong dòng → “Chi phí đã có trong dòng này”.',
        '- Nút + Thêm chi phí / Xoá dòng chi phí khi dòng còn sửa được.']),
])
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Sửa Giá NCC / Thuế NK / Tỉ giá / chi phí', 'Change',
     'After:\n– Tính lại Đơn giá VNĐ, sau thuế, chi phí, Giá nhập kho của dòng.\n'
     '– Giá bán CHƯA sửa tay của dòng chạy lại theo hệ số × giá nhập kho mới (BR-09); giá đã gõ tay giữ nguyên.\n– Xoá lỗi của ô vừa sửa.'),
    ('Lưu (mọi kiểu)', 'Click', 'During:\n' + '\n'.join(VALIDATE_FMT[2:4]) + '\nAfter:\n– Máy chủ tính lại mọi số tiền, không lấy số màn hình gửi.'),
])

# ------------------------------------------------------------------ 2.7
d.h3('2.7 Tính giá bán')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Tính giá bán', 'crud', actor=A_KTMH, caption='Biểu đồ Use Case — FR-07 Tính giá bán')
d.p('2.7.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Tính giá bán (tab Tính giá)',
    mota='Mỗi dòng hàng × ĐVT là 1 khối: số đầu vào + Chi phí khác (nhập) + Giá nhập kho, và 6 loại giá (Hệ số · Giá công thức · Giá bán · '
         'ĐMGG · Ngày hiệu lực). KTMH chốt hệ số / giá bán / ĐMGG từng loại, thêm giá hiệu lực tương lai nếu cần.',
    tacnhan=A_KTMH,
    dieukien='Đang ở form Lập / Sửa (dòng còn sửa được).',
    chinh='1. Nhập Chi phí khác (VNĐ) → Giá nhập kho = Thành tiền sau thuế + Tổng chi phí + Chi phí khác.\n'
          '2. Nhập Hệ số của Bán lẻ → Giá bán Bán lẻ = tròn trăm(hệ số × giá nhập kho); hệ số + giá lan sang Giá bán theo lô, Đại lý cấp 1–3; '
          'TMĐT = Bán lẻ × hệ số TMĐT.\n'
          '3. (Tuỳ chọn) sửa riêng hệ số / giá bán / ĐMGG từng loại 2–5 (sau Bán lẻ).\n'
          '4. (Tuỳ chọn) bấm + Giá hiệu lực ở 1 loại giá → nhập hệ số / giá / ĐMGG / ngày tương lai.\n'
          '5. Lưu nháp hoặc Lưu và duyệt / gửi duyệt.',
    phu='• Ví dụ thật (PYCTG-01939, VNĐ): Thùng giá nhập kho 465,360, hệ số đang áp dụng 1,61 → giá bán gợi ý 749,200 (công thức 749,230); '
        'nhập Chi phí khác 34,640 → giá nhập kho 500,000 → giá 805,000; đổi hệ số Bán lẻ 1,8 → 900,000 cho 5 loại, TMĐT 1,170,000 (hệ số 2,34). '
        'Tuýp 19,390 × 1 → 19,400; TMĐT 25,220.\n'
        '• Gõ thẳng Giá bán → giữ số đã gõ (sửa tay); đổi giá nhập kho sau đó không ghi đè.\n'
        '• Dòng TMĐT không nhập được (khoá) — luôn theo Bán lẻ.\n'
        '• Bấm ✕ ở dòng giá hiệu lực → bỏ dòng đó.',
    dacbiet='Giá bán lưu ĐÚNG số KTMH chốt (máy chủ chỉ kiểm > 0 và ≤ 999,999,999,999, không ép lại tròn trăm). TMĐT (giá, hệ số, giá hiệu '
            'lực) máy chủ tự tính lại từ Bán lẻ theo hệ số TMĐT của công ty phiếu.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('07c-tab-tinh-gia-cuoi.png'),
         shot_caption='Tab Tính giá PTG-03178: giá nhập kho 13,108,667; Bán lẻ hệ số 1,7 → công thức 22,284,734, giá đã chốt 22,500,000; TMĐT '
                      '29,250,000 (hệ số 2,21) (dữ liệu thật)')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('17-nhap-he-so.png'),
         shot_caption='Chi phí khác 34,640 → giá nhập kho 500,000; hệ số Bán lẻ 1,8 lan 4 loại → 900,000; TMĐT 1,170,000; Tuýp 19,400 / 25,220 '
                      '(minh hoạ, phép tính thật của màn)')
d.layout(menu=MENU + ' => Tạo mới => Giá hiệu lực', shot=shot('18-loi-gia-hieu-luc.png'),
         shot_caption='+ Giá hiệu lực ở Bán lẻ: dòng “↳ giá sẽ áp dụng” chép hệ số / giá hiện tại; chưa chọn ngày mà bấm Lưu và duyệt → '
                      '“Bắt buộc phải chọn”, tab Tính giá gắn chấm đỏ (minh hoạ)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('13-nhieu-dvt.png'),
         shot_caption='PTG-01959: 1 hàng 2 ĐVT (Thùng / Tuýp) — mỗi ĐVT có bộ giá riêng (dữ liệu thật)')
d.layout(menu=MENU + ' => Sửa', shot=shot('37-tmdt-2-dong-gia-hieu-luc.png'),
         shot_caption='PTG-02618 có giá hiệu lực TMĐT đã lưu: dòng TMĐT hiện 2 dòng “↳ giá sẽ áp dụng”, dòng đầu nhập được (lỗi — xem '
                      'progress) (dữ liệu thật, giả làm Đang tạo để mở màn Sửa)')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Bảng Tính giá', 'Table/Grid', 'Enable', '16 cột', '–', 'Theo dữ liệu', [
        '- Mỗi dòng hàng × ĐVT là 1 khối (gộp dòng) gồm 6 dòng giá + các dòng giá hiệu lực; khối cách nhau đường kẻ đậm.',
        '- Rộng ~2.060px → cuộn ngang trong khung bảng.']),
    ('Cột STT / Tên hàng hoá / ĐVT', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', 'STT theo HÀNG; tên chỉ ở dòng đầu của hàng.'),
    ('Cột Mã hàng', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', [
        '- Mã hàng (“↳ cùng mã” với ĐVT khác) + “Mã vạch: <mã>” khi có.',
        '- Khối chính sách gọn (như cột Chính sách giá nội bộ, mục 2.6).',
        '- Link “Tạm tính” (biểu tượng máy tính) khi hàng có chính sách → popup mục 2.8.',
        '- Ô “Ghi chú dòng phiếu” (≤ 1000 ký tự).',
        '- Lỗi chặn chéo hiện ngay dưới ô này (BR-17).']),
    ('Cột Đơn giá VNĐ / Thành tiền sau thuế', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', 'Như tab Hàng hoá.'),
    ('Cột Tổng chi phí', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', '- Tổng Thành tiền (VNĐ) các chi phí của dòng (vd 1,512,060 + '
     '504,020 + 4,147 = 2,020,227).'),
    ('Cột Chi phí khác', 'Number', 'Enable / Disable', '≥ 0, số nguyên', 'Không', '0', [
        '- VNĐ, dấu phẩy ngăn nghìn; âm → “Không hợp lệ”.',
        '- Cộng thẳng vào Giá nhập kho.']),
    ('Cột Giá nhập kho', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', [
        '- = Thành tiền sau thuế + Tổng chi phí + Chi phí khác (chữ xanh ngọc), vd 11,088,440 + 2,020,227 + 0 = 13,108,667.',
        '- Là “giá vốn” để tính giá bán; khi giá được áp sẽ ghi thành giá vốn của ĐVT tại công ty phiếu.',
        '- Không bị che theo quyền ' + Q3 + '.']),
    ('Cột Kết quả duyệt', 'Badge', 'Read-only', '–', '–', 'Ẩn', [
        '- Chỉ hiện khi PTG Chờ duyệt giá / Giá bị từ chối / Đã duyệt và có dòng qua duyệt.',
        '- “Chờ duyệt” (cam) · “Đã duyệt” (xanh) · “Bị từ chối” (đỏ) + “Lý do: <lý do>”; dòng áp thẳng của PTG Đã duyệt: “Áp ngay”.']),
    ('Cột Loại', 'Text', 'Read-only', '6 loại', '–', 'Theo dữ liệu', [
        '- Bán lẻ (dòng phụ “sửa là áp cho 4 loại dưới” khi còn sửa được) · Giá bán theo lô · Đại lý cấp 1 · 2 · 3 · Giá bán thương mại '
        'điện tử ( online) (dòng phụ “= Bán lẻ × <hệ số TMĐT>”).',
        '- Dòng giá hiệu lực: “↳ giá sẽ áp dụng”.']),
    ('Cột Hệ số', 'Number', 'Enable / Disable', '0 đến dưới 100, 2 số lẻ', 'Có khi Lưu và duyệt / gửi duyệt', 'Hệ số đang áp dụng', [
        '- Mặc định (PTG mới): hệ số đang áp dụng của ĐVT tại công ty phiếu (chưa có giá → trống).',
        '- Gõ hệ số → Giá bán = tròn trăm(hệ số × giá nhập kho), bỏ cờ sửa tay; Bán lẻ lan hệ số + giá sang 4 loại.',
        '- TMĐT: khoá, = hệ số Bán lẻ × hệ số TMĐT (2 số lẻ).',
        '- Lỗi: trống khi gửi → “' + MSG_REQ + '”; ngoài khoảng → “Phải từ 0 đến dưới 100”.']),
    ('Cột Giá công thức', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', [
        '- = Giá nhập kho × Hệ số, làm tròn đồng (TMĐT làm tròn nghìn) — chỉ tham chiếu, không lưu.',
        '- Vd 13,108,667 × 1,7 = 22,284,734; TMĐT 13,108,667 × 2,21 → 28,970,000.']),
    ('Cột Giá bán', 'Number', 'Enable / Disable', '> 0, ≤ 999,999,999,999', 'Có khi Lưu và duyệt / gửi duyệt', 'Theo hệ số', [
        '- Gõ tay → giữ đúng số đã gõ (đổi giá nhập kho sau đó không ghi đè); Bán lẻ lan giá sang 4 loại.',
        '- Giá đã lưu khi mở lại = số đã chốt (không chạy lại theo hệ số).',
        '- TMĐT: khoá, = làm tròn đồng (giá Bán lẻ × hệ số TMĐT).',
        '- Lỗi: trống khi gửi → “' + MSG_REQ + '”; = 0 khi gửi → “Phải lớn hơn 0”; quá lớn → “Không hợp lệ”.']),
    ('Cột ĐMGG (%)', 'Number', 'Enable / Disable', '0 – 100', 'Không', 'ĐMGG đang áp dụng', [
        '- Bán lẻ lan sang 4 loại; TMĐT luôn 0 (khoá).', '- Ngoài 0–100 → “Phải từ 0 đến 100” (không tự kẹp).']),
    ('Cột Ngày hiệu lực', 'Text / Button', 'Enable / Ẩn', '–', '–', 'Theo dữ liệu', [
        '- Dòng giá hiện tại: “Đang áp dụng: <giá đang áp dụng tại công ty phiếu>” hoặc “Chưa có giá”.',
        '- Nút “+ Giá hiệu lực” khi loại giá chưa có dòng hiệu lực (không có ở TMĐT).']),
    ('Dòng giá hiệu lực', 'Number / Datepicker', 'Enable / Disable', 'Ngày > hôm nay', 'Có (giá, hệ số, ngày)', 'Chép từ giá hiện tại', [
        '- Hệ số → giá = hệ số × giá nhập kho làm tròn ĐỒNG (không tròn trăm).',
        '- Ngày chỉ chọn được từ ngày mai; nút ✕ “Bỏ giá hiệu lực”.',
        '- TMĐT: dòng chỉ đọc suy từ giá hiệu lực Bán lẻ × hệ số TMĐT, cùng ngày.',
        '- Lỗi: “' + MSG_REQ + '” · “Phải từ 0 đến 99” · “Bắt buộc phải chọn” · “Phải chọn ngày tương lai” · “Chỉ được 1 giá hiệu lực”.']),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Nhập Chi phí khác / đổi số đầu vào', 'Change',
     'After:\n– Giá nhập kho tính lại; giá bán chưa sửa tay của dòng = tròn trăm(hệ số × giá nhập kho mới); TMĐT theo Bán lẻ.'),
    ('Nhập Hệ số', 'Change',
     'After:\n– Giá bán loại đó = tròn trăm(hệ số × giá nhập kho), bỏ cờ sửa tay.\n– Bán lẻ: ghi đè hệ số + giá 4 loại 2–5; TMĐT tính lại.'),
    ('Nhập Giá bán', 'Change', 'After:\n– Đánh dấu sửa tay; Bán lẻ ghi đè giá 4 loại 2–5 (cũng thành sửa tay); TMĐT tính lại.'),
    ('Nhập ĐMGG', 'Change', 'After:\n– Bán lẻ ghi đè ĐMGG 4 loại; TMĐT giữ 0.'),
    ('Bấm + Giá hiệu lực / ✕', 'Click', 'After:\n– Thêm 1 dòng (chép hệ số / giá / ĐMGG đang có) hoặc bỏ dòng.'),
    ('Lưu (mọi kiểu)', 'Click',
     'During:\n' + '\n'.join(VALIDATE_FMT[4:7]) + '\n' + VALIDATE_SEND[0] + '\n'
     'After:\n– Máy chủ lưu giá bán 5 loại đúng số gửi; TMĐT = round(Bán lẻ × hệ số TMĐT công ty), hệ số TMĐT = hệ số Bán lẻ × hệ số TMĐT, '
     'ĐMGG 0; giá hiệu lực TMĐT = giá hiệu lực Bán lẻ × hệ số TMĐT.'),
])

# ------------------------------------------------------------------ 2.8
d.h3('2.8 Tạm tính giá mua nội bộ')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Tạm tính giá mua nội bộ', 'view', actor=A_KTMH, caption='Biểu đồ Use Case — FR-08 Tạm tính giá mua nội bộ')
d.p('2.8.2 Giới thiệu')
d.rule_ref(DETAIL_RULE, anchor='detail')
d.intro_table(
    ten='Tạm tính giá mua từ công ty quản lý (popup)',
    mota='Với hàng do CÔNG TY KHÁC quản lý có chính sách giá nội bộ cho công ty phiếu, popup cho biết giá mua tham khảo theo 2 tỷ lệ Nhập khẩu '
         'nguyên lô / Tồn kho — để KTMH so với giá nhập kho đang tính. Chỉ tham khảo, không ghi bảng giá.',
    tacnhan=A_KTMH + '; ' + A_XEM,
    dieukien='Thấy được PTG; dòng hàng có chính sách (link “Tạm tính” chỉ hiện khi có).',
    chinh='1. Bấm “Tạm tính” ở ô Mã hàng (tab Tính giá).\n2. Popup tải số mới nhất của công ty quản lý cho đúng hàng × ĐVT.\n'
          '3. Đọc bảng giá mua suy ra; bấm Đóng.',
    phu='• Theo giá vốn: Giá mua = tròn trăm(giá vốn công ty quản lý × (1 + %)), vd giá vốn 450,000, Nhập khẩu 5% → 472,500, Tồn kho 8% → 486,000.\n'
        '• Theo giá bán: mỗi loại giá mua = tròn trăm(giá bán công ty quản lý × (1 − %)), vd Bán lẻ 796,000 → 756,200 / 732,300.\n'
        '• Thiếu quyền ' + Q3 + ': giá vốn và giá mua suy từ giá vốn hiện “—” (máy chủ không trả số).\n'
        '• Hàng của chính công ty: “Hàng hoá của chính công ty đang làm việc — không có giá mua nội bộ.”; chưa cấu hình: nhãn “Chưa cấu hình”.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Tạm tính', shot=shot('30-chinh-sach-co-1092.png'),
         shot_caption='Ô Mã hàng có chính sách Theo giá vốn TPSG, người có quyền ' + Q3 + ' thấy “Giá vốn TPSG: 450,000” (minh hoạ)')
d.layout(menu=MENU + ' => Tạo mới => Tạm tính', shot=shot('33-chinh-sach-khong-1092.png'),
         shot_caption='Cùng ô với người thiếu quyền ' + Q3 + ': “Giá vốn TPSG: —” (minh hoạ)')
d.layout(menu=MENU + ' => Tạo mới => Tạm tính', shot=shot('31-tam-tinh-gia-von.png'),
         shot_caption='Popup Tạm tính — Theo giá vốn: 450,000 → 472,500 / 486,000 (minh hoạ — DB dev không có chính sách cho hàng công ty khác)')
d.layout(menu=MENU + ' => Tạo mới => Tạm tính', shot=shot('32-tam-tinh-gia-ban.png'),
         shot_caption='Popup Tạm tính — Theo giá bán: 6 loại giá TPSG và giá mua − 5% / − 8% (minh hoạ)')
d.layout(menu=MENU + ' => Tạo mới => Tạm tính', shot=shot('34-tam-tinh-khong-1092.png'),
         shot_caption='Popup Tạm tính — Theo giá vốn, người thiếu quyền ' + Q3 + ': mọi ô “—” (minh hoạ)')
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Tạm tính giá mua từ công ty quản lý', 'Biểu tượng máy tính; nút ✕.'),
    ('Dòng hàng', 'Text', 'Read-only', '–', 'Theo dữ liệu', '“Hàng hoá: <mã> — <tên> · ĐVT: <ĐVT>”.'),
    ('Dòng công ty quản lý', 'Text', 'Read-only', '–', 'Theo dữ liệu', '“Công ty quản lý: <mã cty>” + nhãn cách tính + “Nhập khẩu nguyên lô <x>% · Tồn kho <y>%”.'),
    ('Bảng Theo giá vốn', 'Table/Grid', 'Read-only', '4 cột', 'Theo dữ liệu', [
        '- Giá · Giá vốn <mã cty> · Giá mua — Nhập khẩu nguyên lô · Giá mua — Tồn kho; 1 dòng “Theo giá vốn (+ %)”.',
        '- Cả 3 số chỉ hiện với quyền ' + Q3 + '; thiếu → “—”.']),
    ('Bảng Theo giá bán', 'Table/Grid', 'Read-only', '4 cột × 6 loại giá', 'Theo dữ liệu', [
        '- Loại giá · Giá bán <mã cty> · Giá mua — Nhập khẩu nguyên lô · Giá mua — Tồn kho.', '- Ai xem cũng thấy (không phải giá vốn).']),
    ('Dòng chú thích', 'Text', 'Read-only', '–', 'Hiển thị', '“Số tạm tính để tham khảo — làm tròn trăm đồng, không ghi vào bảng giá.”'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng popup.'),
], required=False)
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tạm tính', 'Click', 'Before:\n– Kiểm quyền xem PTG.\nDuring:\n– Đọc chính sách + giá công ty quản lý cho hàng × ĐVT tại công ty đang '
     'làm việc; giá vốn chỉ trả khi có ' + Q3 + '.\nAfter:\n– Hiện popup; không ghi gì.'),
])

# ------------------------------------------------------------------ 2.9
d.h3('2.9 Sửa PTG')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Sửa PTG', 'crud', actor=A_KTMH, caption='Biểu đồ Use Case — FR-09 Sửa PTG')
d.p('2.9.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Sửa phiếu tính giá',
    mota='Người lập sửa PTG Đang tạo (mọi dòng, mọi ô) hoặc PTG Giá bị từ chối (CHỈ dòng bị từ chối; tỉ giá khoá; dòng đã duyệt giữ nguyên '
         'giá đã áp) rồi Lưu nháp / Lưu và duyệt / Lưu và gửi duyệt.',
    tacnhan=A_KTMH,
    dieukien='Là người lập, còn quyền ' + Q2 + '; PTG Đang tạo hoặc Giá bị từ chối; nhóm chưa đóng.',
    chinh='1. Bấm Sửa ở danh sách hoặc chân màn Chi tiết.\n2. Form “Sửa phiếu tính giá: <số phiếu>” nạp số đã lưu (giá bán đã lưu giữ nguyên, '
          'không chạy lại theo hệ số).\n3. Sửa như mục 2.6, 2.7.\n4. Bấm Lưu nháp → “' + MSG_SAVED + '”; về danh sách.',
    phu='• Không đủ điều kiện → không có nút Sửa; mở thẳng màn Sửa → tự chuyển màn Chi tiết.\n'
        '• PTG Giá bị từ chối: banner vàng “Giá bị từ chối ở màn Duyệt giá bán: <lý do>. Sửa các dòng bị từ chối rồi Lưu và gửi duyệt lại — '
        'dòng đã duyệt giữ nguyên.”; dòng đã duyệt khoá.\n'
        '• PTG vừa đổi trạng thái ở nơi khác → “' + MSG_CONFLICT + '”.',
    dacbiet='Mỗi lần lưu khi còn sửa được, chính sách giá nội bộ được chụp lại. Lưu nháp PTG Giá bị từ chối vẫn giữ trạng thái Giá bị từ chối.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('26-gia-bi-tu-choi-chi-tiet.png'),
         shot_caption='PTG Giá bị từ chối: banner lý do, nút Sửa ở chân (minh hoạ — PTG-03170 giả làm Giá bị từ chối)')
d.layout(menu=MENU + ' => Sửa', shot=shot('27-sua-dong-bi-tu-choi.png'),
         shot_caption='Màn Sửa: dòng “Đã duyệt” khoá, dòng “Bị từ chối” + lý do mở sửa (đo: 42/144 ô nhập mở — đúng 2 dòng bị từ chối), tỉ giá khoá (minh hoạ)')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu', '“Sửa phiếu tính giá: <số phiếu>”.'),
    ('Banner Giá bị từ chối', 'Label', 'Hiển thị / Ẩn', '–', '–', 'Ẩn', '- Chỉ PTG Giá bị từ chối; lý do = các lý do từ chối khác nhau nối “; ”.'),
    ('Các ô nhập', 'Textbox / Number', 'Enable / Disable', 'Như mục 2.4–2.7', 'Như mục 2.4–2.7', 'Số đã lưu', [
        '- Đang tạo: mọi ô mở.',
        '- Giá bị từ chối: chỉ dòng “Bị từ chối” mở; Tỉ giá khoá; dòng “Đã duyệt” khoá.']),
    ('Nút Lưu nháp / Lưu và duyệt / Lưu và gửi duyệt / Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Như màn Lập (mục 2.4, 2.12, 2.13).'),
])
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Sửa', 'System', 'Before:\n– Không thấy PTG → trang 404; không đủ điều kiện sửa → chuyển màn Chi tiết.\nAfter:\n– Nạp số đã lưu, '
     'dòng không sửa được khoá.'),
    ('Bấm Lưu nháp', 'Click',
     'Before:\n– Thiếu ' + Q2 + ' → “' + MSG_NOPERM + '”; nhóm đóng → “' + MSG_CLOSED + '”; không còn sửa được → “' + MSG_CONFLICT + '”.\n'
     'During:\n– Kiểm như 2.4.5; Giá bị từ chối chỉ kiểm + ghi các dòng bị từ chối, tỉ giá giữ số cũ.\n'
     'After:\n– Ghi đè dòng theo hàng × ĐVT (giữ kết quả duyệt dòng đã duyệt); chụp lại chính sách.\n– Thông báo “' + MSG_SAVED + '”, về danh sách.'),
])

# ------------------------------------------------------------------ 2.10
d.h3('2.10 Xem chi tiết PTG')
d.p('2.10.1 Giới thiệu')
d.rule_ref(DETAIL_RULE, anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu tính giá',
    mota='Màn “Chi tiết phiếu tính giá: <số phiếu>” chỉ đọc: thông tin chung, 3 tab Hàng hoá / Chi phí / Tính giá, banner theo trạng thái, '
         'khối Lịch sử của nhóm và nút thao tác theo quyền.',
    tacnhan=A_KTMH + '; ' + A_XEM + '; Người dùng đã đăng nhập',
    dieukien='Có 1 trong 3 quyền xem; PTG thuộc công ty đang làm việc; không phải nháp của người khác.',
    chinh='1. Bấm số phiếu ở danh sách (hoặc nút Xem phiếu tính giá ở YCTG, thông báo [PTG]).\n'
          '2. Hệ thống hiện màn Chi tiết, mở tab Hàng hoá (Chờ duyệt giá / Giá bị từ chối: tab Tính giá).\n3. Bấm Quay lại → danh sách.',
    phu='• Nháp người khác / công ty khác / không tồn tại → trang “' + MSG_404PAGE + '” (vd PTG-00215).\n'
        '• Nhóm đã kết thúc → banner xám “' + MSG_CLOSED_NOTE + '” (mọi PTG Đã duyệt đều có, vì nhóm “Đã tính giá”).\n'
        '• Chờ duyệt giá → banner tím “Giá đang chờ duyệt ở màn Duyệt giá bán của ' + CTY + ' — hàng sang Đang kinh doanh và có kết quả tính '
        'giá khi mọi dòng giá được duyệt.”')
d.p('2.10.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('05-chi-tiet.png'),
         shot_caption='Chi tiết PTG-03178 Đã duyệt: banner nhóm đã kết thúc, nút Xem giá bán mới · In · In kết quả · Quay lại (dữ liệu thật)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('08-lich-su.png'), shot_caption='Khối Lịch sử của nhóm (dữ liệu thật)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('25-cho-duyet-gia.png'),
         shot_caption='PTG Chờ duyệt giá: banner tím, chỉ còn In · Quay lại (minh hoạ — PTG-03170 giả làm Chờ duyệt giá)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('28-chi-tiet-dang-tao.png'),
         shot_caption='PTG Đang tạo của chính mình: chân màn có Sửa · Xóa · In (minh hoạ — PTG-03178 giả làm Đang tạo)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('12-nhap-nguoi-khac-404.png'),
         shot_caption='Mở thẳng PTG-00215 (nháp của người khác) → trang 404 (dữ liệu thật)')
d.p('2.10.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Chi tiết phiếu tính giá: <số phiếu>”.'),
    ('Banner trạng thái', 'Label', 'Hiển thị / Ẩn', '–', 'Theo dữ liệu', [
        '- Nhóm đã đóng: xám “' + MSG_CLOSED_NOTE + '”.',
        '- Chờ duyệt giá: tím (câu ở 2.10.1).',
        '- Giá bị từ chối: vàng (câu ở mục 2.9).']),
    ('Khối Thông tin chung', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Như màn Lập, mọi ô chỉ đọc; dòng người lập “<tên> - dd/mm/yyyy hh:mm”.',
        '- Trạng thái: Đang tạo · Chờ duyệt giá · Giá bị từ chối · Đã duyệt (+ “Bật quy chế duyệt giá” khi có).']),
    ('3 tab Hàng hoá / Chi phí / Tính giá', 'Table/Grid', 'Read-only', '–', 'Hàng hoá', [
        '- Như mục 2.6, 2.7, mọi ô khoá.',
        '- Số tiền tính lại từ số đầu vào đã lưu (chi phí theo tỉ lệ).',
        '- Cột Kết quả duyệt hiện khi có dòng qua duyệt.']),
    ('Khối Lịch sử', 'Table/Grid', 'Read-only', '4 cột', 'Theo dữ liệu', [
        '- Người thực hiện · Hành động · Nội dung · Thời gian; mới → cũ; rỗng → “Chưa có lịch sử”.',
        '- Là dòng thời gian của NHÓM: bước YCHG (PTKD duyệt, XNK duyệt…), YCTG (Lập yêu cầu tính giá…) và PTG (Lập phiếu tính giá, Gửi duyệt '
        'giá “<số PTG>. <n> dòng giá”, Giá bị từ chối “<số PTG>. <lý do>”, Duyệt tính giá, Xoá phiếu tính giá).']),
    ('Nút chân màn', 'Button', 'Enable / Ẩn', '–', 'Theo cờ quyền', [
        '- Sửa: người lập + ' + Q2 + ', Đang tạo / Giá bị từ chối, nhóm chưa đóng (mục 2.9).',
        '- Xem giá bán mới: PTG có kết quả (mục 2.14).',
        '- Xóa (đỏ): người lập + ' + Q2 + ', Đang tạo (mục 2.11).',
        '- In: luôn hiện khi đã có số phiếu; In kết quả: PTG có kết quả (mục 2.15).',
        '- Quay lại.']),
], required=False)
d.p('2.10.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở Chi tiết', 'System', 'Before:\n– Kiểm quyền xem; PTG thuộc công ty, không phải nháp người khác; không → trang 404.\n'
     'During:\n– Tính cờ Sửa / Xóa / có kết quả ở máy chủ; chính sách: số chụp (PTG đã khoá) hoặc số mới nhất (còn sửa được); giá vốn '
     'công ty quản lý chỉ trả khi có ' + Q3 + '.\nAfter:\n– Hiện màn chỉ đọc.'),
    ('Bấm số YCTG / YCHG', 'Click', 'After:\n– Mở Chi tiết YCTG / YCHG.'),
])

# ------------------------------------------------------------------ 2.11
d.h3('2.11 Xoá PTG')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Xoá PTG', 'action', actor=A_KTMH, caption='Biểu đồ Use Case — FR-11 Xoá PTG')
d.p('2.11.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xoá. Chỉ bổ sung các quy tắc riêng của màn Phiếu tính giá tại phần mô tả chi tiết.', anchor='delete')
d.intro_table(
    ten='Xoá phiếu tính giá',
    mota='Người lập xoá hẳn PTG Đang tạo (kèm dòng, chi phí, giá, giá hiệu lực). YCTG quay về Chờ tính giá để lập lại.',
    tacnhan=A_KTMH,
    dieukien='Có quyền ' + Q2 + '; là người lập; PTG Đang tạo; nhóm chưa đóng.',
    chinh='1. Bấm Xóa ở danh sách hoặc chân màn Chi tiết.\n'
          '2. Hộp “Xác nhận xóa”: “Xóa phiếu tính giá <số phiếu>? Yêu cầu tính giá sẽ về \"Chờ tính giá\".”\n3. Bấm Xóa.\n'
          '4. Thông báo “Đã xoá phiếu tính giá”; danh sách tải lại / về danh sách.',
    phu='• Bấm Hủy / ✕ → không xoá.\n• PTG đã gửi / áp ở nơi khác → “' + MSG_CONFLICT + '”.\n'
        '• PTG Chờ duyệt giá / Giá bị từ chối / Đã duyệt KHÔNG xoá được (đã sinh yêu cầu duyệt hoặc đã áp giá).',
    dacbiet='Xoá cứng, không hoàn tác; số phiếu đã dùng không cấp lại; ghi lịch sử nhóm “Xoá phiếu tính giá”; không thông báo.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', shot=shot('29-xac-nhan-xoa.png'),
         shot_caption='Hộp Xác nhận xóa (minh hoạ — PTG-03178 giả làm Đang tạo của mình; bấm Hủy, không xoá)')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xóa', 'Icon Button', 'Enable / Ẩn', 'Ẩn khi không đủ điều kiện', 'Thùng rác đỏ ở danh sách; nút đỏ “Xóa” ở chân màn Chi tiết.'),
    ('Hộp xác nhận', 'Modal', 'Hiển thị', 'Ẩn', ['- Tiêu đề “Xác nhận xóa”.',
     '- “Xóa phiếu tính giá <số phiếu>? Yêu cầu tính giá sẽ về \"Chờ tính giá\".”', '- Nút đỏ “Xóa” / “Hủy”.']),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn', ['- Thành công: “Đã xoá phiếu tính giá”.', '- Lỗi: câu của máy chủ hoặc “Xóa thất bại”.']),
], required=False, scope=False)
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xóa trong hộp xác nhận', 'Click',
     'Before:\n– Thiếu ' + Q2 + ' → “' + MSG_NOPERM + '”; PTG không nhìn thấy → “' + MSG_NOTFOUND + '”; nhóm đóng → “' + MSG_CLOSED + '”.\n'
     '– Không phải người lập / không còn Đang tạo → “' + MSG_CONFLICT + '”.\n'
     'After:\n– Ghi lịch sử nhóm “Xoá phiếu tính giá”; xoá giá hiệu lực, giá, chi phí, dòng, PTG.\n'
     '– YCTG Đang tính giá → Chờ tính giá (nút Tính giá hiện lại ở YCTG).\n'
     '– Hàng Đang tính giá → Chờ tính giá bán nếu không còn nằm trong PTG dở nào khác của công ty.\n'
     '– Thông báo “Đã xoá phiếu tính giá”, tải lại danh sách.'),
])

# ------------------------------------------------------------------ 2.12
d.h3('2.12 Lưu và duyệt (áp giá ngay)')
d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Lưu và duyệt (áp giá ngay)', 'action', actor=A_KTMH, caption='Biểu đồ Use Case — FR-12 Lưu và duyệt (áp giá ngay)')
d.p('2.12.2 Giới thiệu')
d.rule_ref(NOTICE_RULE, anchor='notice')
d.intro_table(
    ten='Lưu và duyệt — áp giá ngay cho công ty phiếu',
    mota='Khi công ty phiếu TẮT quy chế duyệt giá cho hãng của nhóm (dev: cả 8 công ty đều tắt), KTMH bấm Lưu và duyệt: hệ thống lưu PTG và '
         'GHI NGAY bộ giá của từng ĐVT vào công ty phiếu — 6 loại giá, hệ số, ĐMGG, giá hiệu lực, giá vốn = giá nhập kho — rồi chốt PTG Đã duyệt.',
    tacnhan=A_KTMH,
    dieukien='Như Lập / Sửa; công ty phiếu tắt duyệt giá (hoặc bật nhưng hãng không thuộc danh sách phải duyệt).',
    chinh='1. Bấm Lưu và duyệt.\n2. Kiểm dữ liệu (đủ Giá NCC > 0, hệ số, giá bán > 0 mọi dòng).\n'
          '3. Hộp xác nhận “Duyệt phiếu tính giá <số phiếu | mới>? Giá bán áp ngay cho ' + CTY + ', hàng mới sang Đang kinh doanh.”\n'
          '4. Bấm Lưu và duyệt → thông báo “' + MSG_APPLIED + '”; về danh sách; PTG Đã duyệt, có “Xem giá bán mới”.',
    phu='• Bấm Hủy → không lưu.\n'
        '• Hàng × ĐVT đang có yêu cầu duyệt giá mở (từ màn Cập nhật giá bán / PTG khác) → báo đỏ dưới ô Mã hàng (BR-17), không lưu gì.\n'
        '• ĐVT không còn thuộc hàng → “Đơn vị tính không còn thuộc hàng hoá”.\n'
        '• Lỗi khác: câu của máy chủ hoặc “Lưu thất bại, vui lòng thử lại.”',
    dacbiet='Toàn bộ trong 1 giao dịch: lỗi ở 1 dòng thì không dòng nào được ghi. Người lập tự duyệt nên KHÔNG có thông báo “[PTG] Đã duyệt” '
            'cho chính mình; người lập YCHG + XNK nhận “[YCHG] Đã duyệt …”.')
d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Lưu và duyệt', shot=shot('19-xac-nhan-luu-va-duyet.png'),
         shot_caption='Hộp xác nhận Lưu và duyệt (minh hoạ, câu chữ thật của màn)')
d.layout(menu=MENU + ' => Lưu và duyệt', shot=shot('20-ap-gia-thanh-cong.png'),
         shot_caption='Sau khi bấm: thông báo “Đã áp giá bán”, về danh sách (minh hoạ — yêu cầu lưu bị chặn trên trình duyệt, trả câu thật của máy chủ)')
d.layout(menu=MENU + ' => Lưu và duyệt', shot=shot('35-chan-cheo-cho-duyet.png'),
         shot_caption='Máy chủ chặn chéo: “Đang có yêu cầu duyệt giá ở màn Cập nhật giá bán” / “Giá đang chờ duyệt ở PTG-03170” dưới ô Mã hàng (minh hoạ)')
d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Lưu và duyệt', 'Button', 'Enable / Ẩn', 'Theo quy chế', '- Nút xanh, biểu tượng dấu tích; chỉ hiện khi công ty phiếu không phải duyệt hãng này.'),
    ('Hộp xác nhận', 'Modal', 'Hiển thị', 'Ẩn', ['- Tiêu đề “Lưu và duyệt”.',
     '- “Duyệt phiếu tính giá <số phiếu>? Giá bán áp ngay cho ' + CTY + ', hàng mới sang Đang kinh doanh.” (PTG chưa có số: “… phiếu tính giá mới?”)',
     '- Nút “Lưu và duyệt” / “Hủy”.']),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn', ['- Thành công: “' + MSG_APPLIED + '”.', '- Lỗi theo dòng: chữ đỏ dưới ô Mã hàng (tab Tính giá).']),
], required=False, scope=False)
d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu và duyệt (xác nhận)', 'Click',
     'Before:\n– Thiếu ' + Q2 + ' → “' + MSG_NOPERM + '”; điều kiện Lập / Sửa như 2.4.5, 2.9.5.\n'
     'During:\n' + '\n'.join(VALIDATE_FMT) + '\n' + VALIDATE_SEND[0] + '\n'
     '– Mỗi dòng: hàng × ĐVT × công ty đang có yêu cầu duyệt mở không thuộc PTG này → “' + MSG_PENDING_G4 + '” / “' + MSG_PENDING_PTG + '” '
     '(báo cùng lúc mọi dòng vướng).\n– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Lưu PTG (như Lưu nháp).\n'
     '– Mỗi dòng: ghi 6 loại giá (TMĐT máy chủ tính), hệ số, ĐMGG, giá hiệu lực vào ĐVT tại CÔNG TY PHIẾU; giá vốn ĐVT = Giá nhập kho; lý do '
     'sửa giá = “Phiếu tính giá <số PTG>”; xoá đề nghị duyệt cũ của ĐVT; ghi 1 dòng lịch sử giá.\n'
     '– Chép giá thực áp + giá hiệu lực vào dòng PTG (“Áp ngay”).\n'
     '– Chốt (BR-18): PTG Đã duyệt; YCTG Đã tính giá; nhóm Đã tính giá; sinh Kết quả tính giá; YCHG Đã tính giá / Không có giá nếu mọi nhóm '
     'đã đóng; hàng Chờ tính giá bán / Đang tính giá → Đang kinh doanh (khi MỌI ĐVT của hàng trong PTG đã xong).\n'
     '– Lịch sử nhóm “Duyệt tính giá”; thông báo [YCHG] cho người lập YCHG + người lập YCTG; “' + MSG_APPLIED + '”.'),
])

# ------------------------------------------------------------------ 2.13
d.h3('2.13 Lưu và gửi duyệt / gửi lại')
d.p('2.13.1 Biểu đồ Usecase')
d.uc_figure('FR-13', 'Lưu và gửi duyệt / gửi lại', 'action', actor=A_KTMH, caption='Biểu đồ Use Case — FR-13 Lưu và gửi duyệt / gửi lại')
d.p('2.13.2 Giới thiệu')
d.rule_ref(NOTICE_RULE, anchor='notice')
d.intro_table(
    ten='Lưu và gửi duyệt — giá sang màn Duyệt giá bán (và gửi lại dòng bị từ chối)',
    mota='Khi công ty phiếu BẬT quy chế duyệt giá cho hãng của nhóm, KTMH bấm Lưu và gửi duyệt: mỗi dòng sinh / ghi đè 1 yêu cầu duyệt giá '
         '(hàng × ĐVT × công ty) ở màn Duyệt giá bán; giá đang áp dụng chưa đổi. Người duyệt duyệt / không duyệt từng dòng, kết quả báo ngược '
         'về PTG. Dòng bị từ chối được sửa rồi gửi lại.',
    tacnhan=A_KTMH,
    dieukien='Như Lập / Sửa; công ty phiếu bật duyệt giá và (áp mọi hãng hoặc hãng của nhóm thuộc danh sách phải duyệt).',
    chinh='1. Bấm Lưu và gửi duyệt (form có nhãn “Bật quy chế duyệt giá”).\n2. Kiểm dữ liệu như Lưu và duyệt.\n'
          '3. Hộp xác nhận “Gửi giá của phiếu tính giá <số phiếu | mới> sang màn Duyệt giá bán của ' + CTY + '?”\n'
          '4. Bấm Lưu và gửi duyệt → “' + MSG_SUBMITTED + '”; PTG Chờ duyệt giá; YCTG Chờ duyệt giá; người có quyền “' + Q_DUYET + '” '
          'nhận “[GIA] Chờ duyệt: <số PTG>. <n> dòng giá. Người đề nghị: <tên>”.\n'
          '5. Người duyệt xử lý từng dòng ở màn Duyệt giá bán → dòng PTG “Đã duyệt” (chép GIÁ THỰC ÁP, gồm giá người duyệt sửa) hoặc “Bị từ '
          'chối” + lý do.\n'
          '6. Mọi dòng đã duyệt → PTG Đã duyệt (chốt như 2.12), người lập nhận “[PTG] Đã duyệt: <số PTG>. Giá bán đã được áp”.',
    phu='• Không còn dòng chờ mà có dòng bị từ chối → PTG Giá bị từ chối, YCTG Đang tính giá; người lập nhận “[PTG] Từ chối: <số PTG>. Lý do: '
        '<lý do>”; lịch sử “Giá bị từ chối”.\n'
        '• Gửi lại: Sửa PTG Giá bị từ chối (chỉ dòng bị từ chối) → Lưu và gửi duyệt → chỉ các dòng đó gửi lại; dòng đã duyệt giữ giá đã áp.\n'
        '• Dòng có giá đề nghị TRÙNG giá đang áp dụng → không sinh yêu cầu, coi như Đã duyệt ngay; mọi dòng như vậy → PTG Đã duyệt ngay, '
        'thông báo “' + MSG_APPLIED + '”.\n'
        '• Chặn chéo như 2.12 (BR-17). Hàng mới vẫn Đang tính giá tới khi mọi ĐVT được duyệt.',
    dacbiet='Không gửi “[GIA] Đã duyệt / Từ chối” từng dòng cho yêu cầu sinh từ PTG — thay bằng thông báo mức PTG. Giá vốn đề nghị = Giá nhập '
            'kho của dòng.')
d.p('2.13.3 Layout màn hình')
d.layout(menu=MENU + ' => Lưu và gửi duyệt', shot=shot('21-quy-che-duyet.png'),
         shot_caption='Công ty bật quy chế: nhãn “Bật quy chế duyệt giá”, nút “Lưu và gửi duyệt”, dòng nhắc chân form (minh hoạ — dev mọi công '
                      'ty đều tắt duyệt giá)')
d.layout(menu=MENU + ' => Lưu và gửi duyệt', shot=shot('23-xac-nhan-gui-duyet.png'), shot_caption='Hộp xác nhận Lưu và gửi duyệt (minh hoạ)')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('25b-ket-qua-duyet.png'),
         shot_caption='Cột Kết quả duyệt theo dòng: Đã duyệt / Chờ duyệt (minh hoạ — PTG-03170 giả làm Chờ duyệt giá)')
d.p('2.13.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nhãn Bật quy chế duyệt giá', 'Badge', 'Hiển thị / Ẩn', 'Ẩn', '- Nhãn tím cạnh Trạng thái khi có dòng phải duyệt.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable / Ẩn', 'Theo quy chế', '- Nút xanh, biểu tượng máy bay giấy.'),
    ('Hộp xác nhận', 'Modal', 'Hiển thị', 'Ẩn', ['- Tiêu đề “Lưu và gửi duyệt”.',
     '- “Gửi giá của phiếu tính giá <số phiếu> sang màn Duyệt giá bán của ' + CTY + '?”', '- Nút “Lưu và gửi duyệt” / “Hủy”.']),
    ('Cột Kết quả duyệt', 'Badge', 'Read-only', 'Ẩn', '- Chờ duyệt (cam) · Đã duyệt (xanh) · Bị từ chối (đỏ) + “Lý do: …”.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn', ['- “' + MSG_SUBMITTED + '” (còn dòng chờ) hoặc “' + MSG_APPLIED + '” (không dòng nào phải chờ).']),
], required=False, scope=False)
d.p('2.13.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu và gửi duyệt (xác nhận)', 'Click',
     'Before / During:\n– Như 2.12.5.\nAfter:\n– Lưu PTG; dòng cần gửi = mọi dòng (Đang tạo) hoặc dòng bị từ chối (Giá bị từ chối).\n'
     '– Mỗi dòng: giá đề nghị khác giá đang áp dụng → tạo / ghi đè yêu cầu duyệt (kèm số PTG, giá vốn đề nghị = Giá nhập kho, lý do “Phiếu tính '
     'giá <số PTG>”), dòng “Chờ duyệt”, ghi lịch sử giá “gửi duyệt”; trùng → dòng “Đã duyệt” + chép giá đang áp dụng.\n'
     '– Có dòng chờ → lịch sử nhóm “Gửi duyệt giá” (“<số PTG>. <n> dòng giá”); PTG Chờ duyệt giá; YCTG Chờ duyệt giá; thông báo gộp [GIA].\n'
     '– Thông báo “' + MSG_SUBMITTED + '”.'),
    ('Người duyệt Duyệt 1 dòng (màn Duyệt giá bán)', 'System',
     'After:\n– Áp giá (người duyệt có thể đã sửa) cho công ty phiếu; dòng PTG “Đã duyệt” + chép giá thực áp; xét lại PTG: hết dòng chờ và '
     'không dòng từ chối → chốt Đã duyệt (như 2.12).'),
    ('Người duyệt Không duyệt 1 dòng', 'System',
     'After:\n– Dòng PTG “Bị từ chối” + lý do; hết dòng chờ → PTG Giá bị từ chối, YCTG Đang tính giá, thông báo “[PTG] Từ chối …”.'),
])

# ------------------------------------------------------------------ 2.14
d.h3('2.14 Xem giá bán mới')
d.p('2.14.1 Giới thiệu')
d.rule_ref(DETAIL_RULE, anchor='detail')
d.intro_table(
    ten='Xem giá bán mới (kết quả tính giá)',
    mota='Từ PTG Đã duyệt mở Chi tiết YCHG với khối “Chi tiết kết quả” của nhóm bung sẵn: 6 loại giá × ĐVT + ĐMGG đã áp, dòng “Giá bán mới '
         'áp ngày <dd/mm/yyyy> · <người tính giá> · <số PTG>”, nút In kết quả.',
    tacnhan=A_KTMH + '; ' + A_XEM + '; Người dùng đã đăng nhập',
    dieukien='PTG đã có kết quả (Đã duyệt).',
    chinh='1. Bấm Xem giá bán mới (nhãn giá) ở danh sách hoặc chân màn Chi tiết.\n2. Chuyển sang Chi tiết YCHG, bung kết quả của đúng nhóm.',
    phu='• PTG chưa Đã duyệt → không có nút.\n• Giá đang áp dụng có thể khác bản chụp nếu sau đó sửa ở màn Cập nhật giá bán.')
d.p('2.14.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem giá bán mới', shot=shot('11-xem-gia-ban-moi.png'),
         shot_caption='PYCHG-04283 bung kết quả nhóm MULLER: Bán lẻ … Đại lý cấp 3 22,500,000 ĐMGG 5%, TMĐT 29,250,000 (dữ liệu thật)')
d.p('2.14.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xem giá bán mới', 'Icon Button / Button', 'Enable / Ẩn', '–', 'Ẩn', 'Nhãn giá ở danh sách; nút “Xem giá bán mới” ở chân Chi tiết.'),
    ('Khối Chi tiết kết quả (ở YCHG)', 'Table/Grid', 'Read-only', '6 loại giá × ĐVT', 'Theo dữ liệu', [
        '- Mỗi ĐVT 1 dòng: Bán lẻ · Theo lô · Đại lý cấp 1 · 2 · 3 · TMĐT, mỗi ô giá + “ĐMGG <x>%”.',
        '- Chỉ giá bán (không có giá vốn) ⇒ ai thấy YCHG đều xem được.']),
], required=False)
d.p('2.14.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xem giá bán mới', 'Click', 'After:\n– Mở Chi tiết YCHG (kèm nhóm, bung kết quả).'),
])

# ------------------------------------------------------------------ 2.15
d.h3('2.15 In phiếu / In kết quả')
d.p('2.15.1 Biểu đồ Usecase')
d.uc_figure('FR-15', 'In phiếu / In kết quả', 'io', actor=A_XEM, caption='Biểu đồ Use Case — FR-15 In phiếu / In kết quả')
d.p('2.15.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột (phần In). Chỉ bổ sung các quy tắc riêng của màn Phiếu tính giá tại phần mô tả chi tiết.',
           anchor='excel')
d.intro_table(
    ten='In phiếu tính giá / In kết quả tính giá',
    mota='Xem trước rồi in “PHIẾU TÍNH GIÁ” (thông tin chung + bảng dòng hàng × ĐVT với giá NCC, VNĐ, thuế, sau thuế, chi phí, giá nhập kho, giá '
         'bán lẻ + khối ký Người lập / Người duyệt) hoặc “KẾT QUẢ TÍNH GIÁ” (6 loại giá mới × ĐVT + ĐMGG, khối ký Người tính giá). Letterhead theo '
         'công ty phiếu.',
    tacnhan=A_XEM + '; Người dùng đã đăng nhập',
    dieukien='In phiếu: thấy được PTG. In kết quả: PTG có kết quả và người dùng xem được YCHG gốc.',
    chinh='1. Bấm In (máy in ở danh sách / chân màn Chi tiết) hoặc In kết quả.\n'
          '2. Popup “Xem trước phiếu tính giá <số phiếu>” / “Xem trước kết quả tính giá <số phiếu>” hiện bản in.\n'
          '3. Bấm In trong popup → hộp thoại in của trình duyệt.',
    phu='• Không thấy PTG / thiếu quyền → báo lỗi, không có bản in.\n• PTG chưa có kết quả → “Phiếu tính giá chưa có kết quả”.\n• Bấm ✕ → đóng popup.')
d.p('2.15.3 Layout màn hình')
d.layout(menu=MENU + ' => In', shot=shot('09-in-phieu.png'),
         shot_caption='Xem trước PHIẾU TÍNH GIÁ PTG-03178 (dữ liệu thật; local không có letterhead do môi trường)')
d.layout(menu=MENU + ' => In kết quả', shot=shot('10-in-ket-qua.png'),
         shot_caption='Xem trước KẾT QUẢ TÍNH GIÁ PTG-03178: 6 loại giá, ngày áp giá 14/09/2026 (dữ liệu thật)')
d.p('2.15.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In / In kết quả', 'Icon Button / Button', 'Enable / Ẩn', '–', 'Theo dữ liệu', 'In luôn hiện khi đã có số phiếu; In kết quả khi có kết quả.'),
    ('Bản in Phiếu tính giá', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Tiêu đề “PHIẾU TÍNH GIÁ”, Số phiếu, Ngày tạo.',
        '- Khối: Yêu cầu tính giá · Yêu cầu hỏi giá · Thương hiệu – Hãng · Tiền tệ / tỉ giá · Người lập · Trạng thái · Ghi chú (trống → “.....”).',
        '- Bảng 11 cột: STT · Mã hàng · Tên hàng hoá · ĐVT · Giá NCC (<tiền tệ>) · Đơn giá VNĐ · Thuế NK (%) · Sau thuế · Chi phí · Giá nhập kho · Giá bán lẻ.',
        '- Khối ký: Người lập · Người duyệt.',
        '- Không in giá vốn công ty quản lý, không in chính sách giá nội bộ.']),
    ('Bản in Kết quả tính giá', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Tiêu đề “KẾT QUẢ TÍNH GIÁ”; khối Phiếu tính giá · Yêu cầu tính giá · Yêu cầu hỏi giá · Thương hiệu – Hãng · Người hỏi giá · Ngày áp giá.',
        '- Bảng: STT · Hàng hoá · ĐVT · Loại giá · Giá mới · ĐMGG (%); 6 dòng / ĐVT theo thứ tự Bán lẻ, Giá bán theo lô, Đại lý cấp 1–3, TMĐT.',
        '- Khối ký: Người tính giá.']),
    ('Popup xem trước', 'Modal', 'Hiển thị', '–', 'Ẩn', 'Nút In (mở hộp thoại in) và ✕.'),
], required=False)
d.p('2.15.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In', 'Click', 'Before:\n– Kiểm quyền xem + PTG nhìn thấy được.\nAfter:\n– Dựng bản in ở máy chủ (số tiền tính lại từ số đầu vào), hiện popup.'),
    ('Bấm In kết quả', 'Click', 'Before:\n– Kiểm người dùng xem được YCHG gốc; PTG có kết quả.\nAfter:\n– Dựng bản in kết quả, hiện popup.'),
    ('Bấm In trong popup', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt.'),
])

# ========================================================= PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('chỉ ghi các quy tắc đặc thù của Phiếu tính giá; quy tắc dùng chung không nhắc lại.',
           anchor='list', head='Quy tắc áp dụng', lead='Ngoài SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi = công ty phiếu',
     ['– PTG thuộc công ty của YCTG = công ty đang làm việc; công ty lấy từ phiên làm việc, không nhận từ màn hình.',
      '– PTG công ty khác: không hiện, không mở, không thao tác được — “' + MSG_NOTFOUND + '”.',
      '– Mọi quyền xét tại công ty phiếu; super admin không được miễn.'], ['Mọi chức năng']),
    ('BR-02', 'Quyền xem = 1 trong 3 quyền',
     ['– Xem danh sách / chi tiết / in / tạm tính cần ' + Q1 + ' HOẶC ' + Q2 + ' HOẶC ' + Q3 + '.',
      '– Không có quyền nào: menu ẩn; gọi chức năng → “' + MSG_NO_VIEW + '”; mở thẳng phiếu → trang 404.',
      '– Không phân quyền theo phòng ban / cấp quản lý.'], ['Xem danh sách', 'Xem chi tiết', 'In']),
    ('BR-03', 'Nháp chỉ người lập thấy',
     ['– PTG Đang tạo chỉ người lập thấy (danh sách, chi tiết, in); người khác mở thẳng → trang 404.',
      '– Các trạng thái khác: mọi người có quyền xem trong công ty thấy.'], ['Xem danh sách', 'Xem chi tiết']),
    ('BR-04', 'Lập PTG từ YCTG Chờ tính giá',
     ['– Chỉ ' + Q2 + '; chỉ YCTG Chờ tính giá của công ty, chưa có PTG, nhóm chưa đóng; 1 YCTG – 1 PTG.',
      '– Không xét phân công hãng (mọi KTMH của công ty).',
      '– 2 người lập cùng lúc chỉ 1 người thành công, người sau nhận “' + MSG_CONFLICT + '”.',
      '– Lưu lần đầu (kể cả nháp): YCTG → Đang tính giá; hàng Chờ tính giá bán → Đang tính giá.'], ['Lập', 'Chọn YCTG']),
    ('BR-05', 'Kế thừa YCTG, KTMH sửa được số đầu vào',
     ['– Dòng = dòng YCTG (hàng × ĐVT); tiền tệ khoá; tỉ giá, Giá NCC, Thuế NK, chi phí sửa được trên PTG (như ERP).',
      '– Sửa trên PTG không đổi YCTG.'], ['Lập', 'Sửa', 'Kiểm tra số đầu vào']),
    ('BR-06', 'GIÁ — Giá nhập kho, máy chủ tính lại',
     ['– Đơn giá VNĐ = Giá NCC × Tỉ giá; Sau thuế = Đơn giá VNĐ × (1 + Thuế NK / 100).',
      '– Chi phí (ngoại tệ) = Tỉ lệ / 100 × Giá NCC (2 số lẻ); Chi phí VNĐ = Chi phí × Tỉ giá.',
      '– Giá nhập kho = Sau thuế + Σ Chi phí VNĐ + Chi phí khác.',
      '– Vd PTG-03178: 316 EURO × 31,900 = 10,080,400; thuế 10% → 11,088,440; chi phí 15% / 5% / 0,04% → 1,512,060 / 504,020 / 4,147; giá '
      'nhập kho 13,108,667.',
      '– Máy chủ TÍNH LẠI khi lưu, không lấy số màn hình gửi; làm tròn 2 số lẻ.'], ['Lập', 'Sửa', 'Tính giá bán', 'In']),
    ('BR-07', 'GIÁ — Hệ số → Giá bán (làm tròn trăm)',
     ['– PTG mới: hệ số + ĐMGG mỗi loại = số đang áp dụng của ĐVT tại công ty phiếu.',
      '– Giá bán = làm tròn TRĂM (hệ số × giá nhập kho); vd 1,61 × 465,360 = 749,229.6 → 749,200; 1,8 × 500,000 = 900,000.',
      '– Giá công thức = giá nhập kho × hệ số làm tròn đồng (TMĐT tròn nghìn) — tham chiếu, không lưu.',
      '– Máy chủ không ép lại tròn trăm; chỉ kiểm giá > 0 và ≤ 999,999,999,999 khi gửi.'], ['Tính giá bán']),
    ('BR-08', 'GIÁ — Bán lẻ lan 4 loại; TMĐT theo Bán lẻ',
     ['– Sửa Hệ số / Giá / ĐMGG của Bán lẻ → ghi đè đúng trường đó cho Giá bán theo lô, Đại lý cấp 1, 2, 3; sửa riêng phải sửa SAU Bán lẻ.',
      '– TMĐT luôn khoá: Giá = làm tròn đồng (Bán lẻ × hệ số TMĐT công ty phiếu), Hệ số = hệ số Bán lẻ × hệ số TMĐT (2 số lẻ), ĐMGG = 0.',
      '– Máy chủ tự tính lại TMĐT khi lưu (cả giá hiệu lực TMĐT = giá hiệu lực Bán lẻ × hệ số TMĐT, cùng ngày).',
      '– Vd Bán lẻ 900,000 → TMĐT 1,170,000, hệ số 2,34; Bán lẻ 22,500,000 → 29,250,000.'], ['Tính giá bán']),
    ('BR-09', 'GIÁ — Giá gõ tay giữ nguyên',
     ['– Giá bán chưa gõ tay chạy lại theo hệ số mỗi khi giá nhập kho đổi (đổi tỉ giá, giá NCC, thuế, chi phí, chi phí khác).',
      '– Gõ Giá bán → đánh dấu sửa tay, không bị ghi đè; gõ lại Hệ số → bỏ sửa tay, giá về công thức.',
      '– Mở lại PTG đã lưu: giá đã lưu là số đã chốt, không chạy lại.'], ['Tính giá bán', 'Sửa']),
    ('BR-10', 'GIÁ — Giá hiệu lực',
     ['– Tối đa 1 giá hiệu lực / loại giá / ĐVT; ngày phải sau hôm nay.',
      '– Hệ số giá hiệu lực → giá = hệ số × giá nhập kho, làm tròn ĐỒNG (không tròn trăm như BR-07).',
      '– Giá hiệu lực TMĐT không nhập riêng: suy từ Bán lẻ.',
      '– Khi áp: ghi thành giá hiệu lực của ĐVT tại công ty phiếu; đến ngày, tác vụ tự động hằng đêm chuyển thành giá hiện tại.'],
     ['Tính giá bán']),
    ('BR-11', 'Kiểm dữ liệu báo đồng thời',
     ['– Lưu nháp: chỉ định dạng (tỉ giá > 0, số ≥ 0, thuế / chi phí / ĐMGG 0–100, hệ số 0 đến dưới 100, giá hiệu lực đủ ô + ngày tương lai).',
      '– Lưu và duyệt / gửi duyệt: thêm bắt buộc Giá NCC > 0, Hệ số và Giá bán > 0 cho 5 loại giá của mọi dòng còn sửa được.',
      '– Câu lỗi: “' + MSG_REQ + '” · “Phải lớn hơn 0” · “Không hợp lệ” · “' + MSG_MAX + '” · “Phải từ 0 đến 100” · “Phải từ 0 đến dưới 100” · '
      '“Phải từ 0 đến 99” · “Bắt buộc phải chọn” · “Phải chọn ngày tương lai” · “Chỉ được 1 giá hiệu lực” · “Vui lòng nhập tối đa 255 / 1000 '
      'ký tự.” · “Chi phí đã có trong dòng này” · “Chi phí vượt giới hạn lưu trữ” · “Giá nhập kho vượt giới hạn lưu trữ” · “' + MSG_NO_ROWS + '”.',
      '– Mọi lỗi báo cùng lúc dưới đúng ô; tab có lỗi gắn chấm đỏ, tự chuyển tab, cuộn tới lỗi; rời form có thay đổi → “Thông tin chưa lưu”.'],
     ['Lập', 'Sửa', 'Lưu và duyệt', 'Lưu và gửi duyệt']),
    ('BR-12', 'GIÁ — Quy chế duyệt giá của công ty phiếu',
     ['– Đọc cấu hình của CÔNG TY PHIẾU (không phải công ty tạo hàng): bật duyệt giá và (áp mọi hãng hoặc hãng sản xuất của hàng thuộc danh '
      'sách phải duyệt).',
      '– Phải duyệt → nhãn “Bật quy chế duyệt giá”, nút “Lưu và gửi duyệt”; không → nút “Lưu và duyệt”.',
      '– Quy chế xét lại tại thời điểm bấm lưu.'], ['Lưu và duyệt', 'Lưu và gửi duyệt']),
    ('BR-13', 'GIÁ — Lưu và duyệt ghi gì vào bộ giá',
     ['– Mỗi ĐVT tại CÔNG TY PHIẾU: 6 loại giá + hệ số + ĐMGG + giá hiệu lực; giá vốn = Giá nhập kho; lý do sửa giá = “Phiếu tính giá <số>”.',
      '– Xoá đề nghị duyệt cũ của ĐVT; ghi lịch sử giá; không đụng công ty khác.',
      '– Dòng PTG chép lại giá thực áp; 1 giao dịch — lỗi 1 dòng thì không ghi dòng nào.'], ['Lưu và duyệt']),
    ('BR-14', 'GIÁ — Lưu và gửi duyệt',
     ['– Mỗi dòng: giá đề nghị khác giá đang áp dụng → yêu cầu duyệt (tối đa 1 yêu cầu mở / hàng × ĐVT × công ty, gửi lại = ghi đè), giá vốn '
      'đề nghị = Giá nhập kho; giá đang áp dụng chưa đổi.',
      '– Trùng giá đang áp dụng → coi như Đã duyệt ngay (không sinh yêu cầu).',
      '– Thông báo gộp “[GIA] Chờ duyệt: <số PTG>. <n> dòng giá. Người đề nghị: <tên>” tới người có ' + Q_DUYET + ' tại công ty phiếu.'],
     ['Lưu và gửi duyệt']),
    ('BR-15', 'GIÁ — Kết quả duyệt báo ngược',
     ['– Duyệt 1 dòng ở màn Duyệt giá bán → dòng PTG “Đã duyệt” + chép GIÁ THỰC ÁP (gồm giá người duyệt sửa); Không duyệt → “Bị từ chối” + lý do.',
      '– Còn dòng chờ → PTG Chờ duyệt giá; hết chờ mà có dòng từ chối → Giá bị từ chối (YCTG Đang tính giá); mọi dòng xong → Đã duyệt.'],
     ['Lưu và gửi duyệt', 'Xem chi tiết']),
    ('BR-16', 'Giá bị từ chối — chỉ sửa dòng bị từ chối',
     ['– Chỉ dòng “Bị từ chối” mở sửa và được gửi lại; dòng đã duyệt giữ giá đã áp; tỉ giá khoá.',
      '– Banner hiện lý do từ chối (nhiều lý do nối “; ”).'], ['Sửa', 'Lưu và gửi duyệt']),
    ('BR-17', 'Chặn chéo yêu cầu duyệt đang mở',
     ['– Hàng × ĐVT × công ty có yêu cầu duyệt mở từ màn Cập nhật giá bán → dòng PTG báo “' + MSG_PENDING_G4 + '”.',
      '– Có yêu cầu mở của PTG khác → “' + MSG_PENDING_PTG + '”.',
      '– Ngược lại, màn Cập nhật giá bán không lưu được ĐVT đang chờ duyệt từ PTG (“Giá đang chờ duyệt ở <số PTG>.”).'],
     ['Lưu và duyệt', 'Lưu và gửi duyệt']),
    ('BR-18', 'Trạng thái và chứng từ liên quan',
     ['– PTG: (Lưu nháp) Đang tạo → (Lưu và duyệt) Đã duyệt; (gửi duyệt) Chờ duyệt giá → Đã duyệt / Giá bị từ chối → (gửi lại) Chờ duyệt giá.',
      '– YCTG: Chờ tính giá → (lưu PTG) Đang tính giá → (gửi duyệt) Chờ duyệt giá → Đã tính giá; từ chối → Đang tính giá; xoá PTG → Chờ tính giá.',
      '– Đã duyệt: nhóm Đã tính giá; sinh Kết quả tính giá (1 / PTG); YCHG Đã tính giá (có nhóm có giá) / Không có giá khi mọi nhóm đóng.',
      '– Hàng: Chờ tính giá bán → Đang tính giá (lưu PTG) → Đang kinh doanh khi MỌI ĐVT của hàng trong PTG xong (kèm đủ bộ giá mọi ĐVT tại công '
      'ty phiếu); hàng đang KD / ngừng KD giữ trạng thái.'], ['Mọi chức năng']),
    ('BR-19', 'GIÁ — Giá vốn công ty quản lý và Tạm tính',
     ['– Chính sách giá nội bộ chỉ tham khảo, không vào công thức PTG.',
      '– Giá vốn công ty quản lý (khối chính sách, popup Tạm tính, giá mua suy từ giá vốn) CHỈ với quyền ' + Q3 + '; thiếu → “—”, máy chủ không trả số.',
      '– Tạm tính: Theo giá vốn = tròn trăm(giá vốn × (1 + %)); Theo giá bán = tròn trăm(giá bán × (1 − %)); không ghi bảng giá.',
      '– PTG đã khoá hiện chính sách theo bản chụp lúc lưu cuối; còn sửa được hiện số mới nhất.',
      '– Giá NCC, giá nhập kho, giá bán của PTG không bị che theo ' + Q3 + '.'], ['Kiểm tra số đầu vào', 'Tạm tính', 'Xem chi tiết']),
    ('BR-20', 'Sửa / xoá; nhóm đóng chỉ còn xem',
     ['– Sửa: người lập còn ' + Q2 + ', PTG Đang tạo / Giá bị từ chối, nhóm chưa đóng.',
      '– Xoá: người lập còn ' + Q2 + ', PTG Đang tạo, nhóm chưa đóng; Chờ duyệt giá / Giá bị từ chối / Đã duyệt không xoá được.',
      '– Không đủ điều kiện → không có nút; gọi thẳng → “' + MSG_CONFLICT + '”; mở thẳng màn Sửa → chuyển Chi tiết.',
      '– Nhóm Đã tính giá / Không có giá / Huỷ duyệt → chỉ xem; gọi thẳng → “' + MSG_CLOSED + '”.'], ['Sửa', 'Xoá']),
    ('BR-21', 'Thông báo',
     ['– “[PTG] Đã duyệt: <số PTG>. Giá bán đã được áp” → người lập (không gửi khi người lập tự Lưu và duyệt).',
      '– “[PTG] Từ chối: <số PTG>. Lý do: <lý do>” → người lập. Bấm → Chi tiết PTG.',
      '– “[GIA] Chờ duyệt …” (BR-14); “[YCHG] Đã duyệt: <số YCHG>. Nhóm <TH — Hãng>: đã có giá bán mới” (hoặc “Đã tính giá xong a/b nhóm”) '
      '→ người lập YCHG + người lập YCTG.',
      '– Lưu nháp / xoá không báo; gửi sau khi lưu xong, lỗi gửi không làm hỏng thao tác.'], ['Lưu và duyệt', 'Lưu và gửi duyệt']),
    ('BR-22', 'Lịch sử theo nhóm',
     ['– Ghi vào dòng thời gian của NHÓM (chung YCHG / YCTG): “Lập phiếu tính giá”, “Gửi duyệt giá” (“<số>. <n> dòng giá”), “Giá bị từ chối” '
      '(“<số>. <lý do>”), “Duyệt tính giá”, “Xoá phiếu tính giá”.', '– Xem ở Chi tiết, mới → cũ.'], ['Xem chi tiết']),
    ('BR-23', 'Danh sách',
     ['– 10 dòng / trang (tối đa 100), sắp Ngày lập giảm dần; sắp được Số phiếu, Ngày lập.',
      '– Tìm nhanh: số PTG, YCTG, YCHG, mã / tên hàng; ô lọc Trạng thái (4), Thương hiệu, Hãng, Người lập, Ngày lập.'],
     ['Xem danh sách', 'Tìm kiếm và lọc']),
    ('BR-24', 'Kết quả tính giá',
     ['– 1 kết quả / PTG, sinh khi PTG Đã duyệt; chép giá thực áp từ dòng PTG (6 loại × ĐVT + ĐMGG + giá hiệu lực).',
      '– Chỉ giá bán ⇒ xem / in kết quả theo quyền xem YCHG.'], ['Xem giá bán mới', 'In kết quả']),
    ('BR-25', 'Thao tác đồng thời',
     ['– Mọi thao tác ghi khoá PTG + YCTG + nhóm (và dòng giá) rồi kiểm lại trạng thái trong 1 giao dịch.',
      '– Người sau nhận “' + MSG_CONFLICT + '”.'], ['Lập', 'Sửa', 'Xoá', 'Lưu và duyệt', 'Lưu và gửi duyệt']),
])

# update_fields=False: Word dang mo tren may user — buoc cap nhat muc luc tren macOS se dong Word.
d.save(update_fields=os.environ.get('SRS_UPDATE_TOC') == '1')
print('OK ->', OUT)

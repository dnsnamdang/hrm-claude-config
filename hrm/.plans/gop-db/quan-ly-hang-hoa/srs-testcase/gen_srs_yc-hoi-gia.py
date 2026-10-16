# -*- coding: utf-8 -*-
"""Sinh SRS - Yeu cau hoi gia (luong Chuyen doi hang hoa, man 3/5) — form chuan 2026-09-24.

Pham vi: man "YC hoi gia" (Ban hang > Yeu cau > Hang hoa > YC hoi gia) gom danh sach, tao / sua / chi tiet, xoa,
popup Chon hang hoa, popup Them / Sua hang tam, PTKD Duyet / Tu choi phieu, PTKD duyet tung hang tam (form rieng),
XNK Duyet nhom / Khong co gia / Huy duyet / Lap YCTG, xem gia ban moi (Chi tiet ket qua), In phieu + In ket qua.
Loi vao phu: nut "Lap yeu cau hoi gia" o man Hang hoa nhap thong tin / Hang dang kinh doanh / Hang tam, link YCHG o
YCTG / PTG, thong bao [YCHG].

Nguon doi chieu code: worktree wt-chuyen-doi-hang-hoa nhanh feat/chuyen-doi-hang-hoa
(hrm-api 39c4a91fe, hrm-client 5c14659e8) — doc ngay 16/10/2026.
  BE: Modules/MasterData/Routes/api.php (nhom price-asking-requests: lap/xem KHONG gate, approve/reject + temp-products
      gate 1662, groups/* gate 1663), Http/Controllers/V1/PriceCalculation/PriceAskingRequestController,
      Services/PriceCalculation/{PriceAskingAccess, PriceAskingRequestService, PriceAskingRequestWriter,
      PriceAskingProductReader, PriceAskingNotifier, XnkAssignmentResolver, PriceResultReader, PriceCalculateFinalizer,
      PriceCalculationPrintService}, Entities/PriceCalculation/{PriceAskingRequest, PriceAskingRequestGroup},
      Entities/Product/ProductCompany (trang thai hang x cong ty).
  FE: pages/sale/price-asking-requests/{index, add, _id/index, _id/edit, _id/temp/_productId}.vue,
      components/sale/price-asking/{PriceAskingRequestForm, PriceAskingProductPickerModal, PriceAskingReasonModal,
      PriceResultDrill}.vue, pages/assign/quotations/components/QuotationProductSearchModal.vue (mode ychg),
      components/product/form/ProductForm.vue (mode temp-approve), components/product/ProductListPage.vue +
      utils/product-list-screens.js (co priceAsking), components/subsystem-menu/sale-hub.js.

Anh chup: Playwright MCP 1440x900, cong 3031 (worktree, DB hrm_erp_giacty), tai khoan E2E Assign (Cty 1, co 1092 1652 1657
1658 — KHONG co 1662/1663/1664). Tao role tam TMP_SRS_YCHG_1662 (id 129856, chi quyen 1662 Cty 1) de chup THAT nut PTKD
o PYCHG-04280, DA GO + cache:forget; dem roles/rhp/ehr ve 130/20967/1718. Moi lenh ghi bi chan tren trinh duyet
(route.abort / route.fulfill) — DB khong doi (doi chieu lai 4280/4282/4287 sau khi chup).
  - THAT: 00-menu, 00b, 01, 02, 03, 04, 05 (khong letterhead do moi truong local), 08..20 (form tao + popup + man hang hoa,
    du lieu hang that SULI / TELWIN / FOFEN / TORIN), 21..23 (PTKD that voi role tam), 25..28 (PYCHG-04283 da tinh gia,
    PTG-03178 that), 38 (phieu Khong duyet cua nguoi khac -> trang 404).
  - MINH HOA (sua phan hoi tren trinh duyet, khong ghi DB): 06/07 (danh dau 1 dong la Dang tao cua minh de hien Sua / Xoa),
    24 (tra "thanh cong" cho lenh Duyet), 29..33 (bat co nut XNK — tai khoan khong phai XNK phan cong), 34 (phieu 4282 gia lam
    Khong duyet cua minh de mo man Sua), 35..37 (dong hang that gia lam hang tam; DB dev khong co hang tam, cay Loai SP rong).

Chay:  python3 .plans/gop-db/quan-ly-hang-hoa/srs-testcase/gen_srs_yc-hoi-gia.py
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

SHOTS = os.path.join(HERE, 'yc-hoi-gia_shots')
OUT = os.path.join(HERE, 'SRS - Yêu cầu hỏi giá.docx')


def shot(name):
    return os.path.join(SHOTS, name)


A_LAP = 'Người lập yêu cầu (mọi nhân viên)'
A_PTKD = 'PTKD duyệt yêu cầu'
A_XNK = 'XNK phụ trách hãng'
MENU = 'Phân hệ Bán hàng => Yêu cầu => Hàng hóa => YC hỏi giá'
MENU_TRADING = 'Phân hệ Danh mục => Hàng hoá => Hàng hoá, vật tư => Hàng đang kinh doanh => Lập yêu cầu hỏi giá'
MENU_ENTERING = 'Phân hệ Danh mục => Hàng hoá => Hàng hoá, vật tư => Hàng hoá nhập thông tin => Lập yêu cầu hỏi giá'
SCREEN = 'Yêu cầu hỏi giá'

d = SrsDoc(out=OUT, menu=MENU, route='/sale/price-asking-requests',
           full_url='http://hrm/sale/price-asking-requests', img_prefix='ychg_')
d.set_menu_icons({k: shot(v) for k, v in {
    'Phân hệ Bán hàng': 'icon_phanhe.png',
    'Yêu cầu': 'icon_rail_yeucau.png',
    'Hàng hóa': 'icon_nhom_hanghoa.png',
    'YC hỏi giá': 'icon_ychg.png',
    'Phân hệ Danh mục': 'icon_phanhe_danhmuc.png',
    'Hàng hoá': 'icon_rail_hanghoa.png',
    'Hàng hoá, vật tư': 'icon_nhom_hanghoavattu.png',
    'Hàng đang kinh doanh': 'icon_hangdangkinhdoanh.png',
    'Hàng hoá nhập thông tin': 'icon_hanghoanhapthongtin.png',
    'Lập yêu cầu hỏi giá': 'icon_lapychg.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cấu hình cột': 'icon_cauhinhcot.png',
    'Tạo mới': 'icon_taomoi.png',
    'Sửa': 'icon_sua.png',
    'Xóa': 'icon_xoa.png',
    'Xử lý': 'icon_xuly.png',
    'In': 'icon_in.png',
    'Chọn hàng hoá': 'icon_chonhang.png',
    'Thêm hàng tạm': 'icon_themhangtam.png',
    'Lưu nháp': 'icon_luunhap.png',
    'Lưu và gửi duyệt': 'icon_guiduyet.png',
    'Duyệt': 'icon_duyet.png',
    'Từ chối': 'icon_tuchoi.png',
    'Duyệt hàng tạm': 'icon_duyet_hangtam.png',
    'Duyệt nhóm': 'icon_xnk_duyet.png',
    'Không có giá': 'icon_khongcogia.png',
    'Lập YCTG': 'icon_lapyctg.png',
    'Huỷ duyệt': 'icon_huyduyet.png',
    'Chi tiết kết quả': 'icon_chitietketqua.png',
    'In kết quả': 'icon_inketqua.png',
}.items()})

Q1 = 'PTKD duyệt yêu cầu hỏi giá'
Q2 = 'XNK xử lý yêu cầu hỏi giá'
Q3 = 'Tính giá bán hàng hoá'
Q4 = 'Xem giá vốn hàng hoá'
Q5 = 'Xây dựng thông tin hàng hoá'
MSG_NOPERM = 'Bạn không có quyền thực hiện chức năng này'
MSG_CONFLICT = 'Trạng thái đã bị thay đổi. Vui lòng load lại trang'
MSG_NOTFOUND = 'Không tìm thấy yêu cầu hỏi giá'
MSG_NOT_XNK = 'Bạn không phải XNK phụ trách nhóm này.'
MSG_NOT_PTKD = 'Bạn không có quyền PTKD duyệt yêu cầu hỏi giá ở công ty của phiếu.'
MSG_404PAGE = 'Không tìm thấy hoặc không được cấp quyền truy cập trang'
MSG_NO_ROW = 'Vui lòng chọn ít nhất 1 hàng hoá'
MSG_NO_XNK = 'Nhóm <Thương hiệu> — <Hãng> chưa có XNK phụ trách tại công ty, chưa gửi được.'
MSG_REQ = 'Bắt buộc phải nhập'

INFO_PTKD = ('Chỉ duyệt được khi mọi hàng tạm đã có quyết định. Duyệt xong: hàng Đồng ý sang Chờ tính giá bán, hàng Không '
             'duyệt nằm lại phiếu và không đi tiếp. Sau bước này không đổi được quyết định.')
INFO_TEMP6 = ('Mở form kiểm tra, bổ sung thông tin hàng tạm. Chọn Đồng ý hoặc Không duyệt cho từng hàng trước khi duyệt '
              'phiếu.')
INFO_TEMP78 = 'Mở lại form để đổi quyết định Đồng ý ↔ Không duyệt. Đổi được tới khi bấm Duyệt phiếu.'
INFO_SAVE = 'Lưu thông tin, chưa ghi quyết định. Nếu hàng đang "Đã duyệt" sẽ quay về chờ duyệt lại.'
INFO_AGREE = 'Hàng chuyển "Hàng tạm đã duyệt". Khi duyệt phiếu, hàng sẽ sang Chờ tính giá bán.'
INFO_REJECT = 'Bắt buộc nhập lý do. Hàng nằm lại phiếu, không đi tiếp. Người lập sửa rồi đưa vào YCHG khác.'

# ============================================================== TRANG DAU
d.title_block(SCREEN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Yêu cầu hỏi giá (phân hệ Bán hàng) — chứng từ đầu tiên của luồng '
    'tính giá bán trong đợt Chuyển đổi hàng hoá sang hệ thống mới, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng trạng thái của Yêu cầu hỏi giá (YCHG).',
    'Làm rõ YCHG KHÔNG cần quyền để lập / xem: ai cũng lập được, ai trong công ty cũng xem được phiếu đã gửi; phiếu Đang '
    'tạo / Không duyệt chỉ người lập thấy. Chỉ 2 bước duyệt cần quyền: PTKD duyệt cả phiếu, XNK phụ trách hãng xử lý '
    'từng nhóm hàng.',
    'Làm rõ hàng được gom nhóm theo Thương hiệu — Hãng sản xuất, mỗi nhóm đi tới đúng XNK được phân công phụ trách hãng '
    'tại công ty; nhóm chưa có XNK phụ trách thì không gửi được.',
    'Làm rõ phần GIÁ BÁN: YCHG không tự đổi giá; trạng thái hàng × công ty đổi theo từng bước; giá bán mới chỉ xuất hiện '
    'khi Phiếu tính giá của nhóm được áp giá (trực tiếp hoặc qua màn Duyệt giá bán) và hiện ở “Chi tiết kết quả” của '
    'YCHG — chỉ giá bán, không lộ giá mua / chi phí / giá vốn.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('YCHG', 'Yêu cầu hỏi giá — số phiếu dạng PYCHG-xxxxx, sinh khi lưu lần đầu.'),
    ('Công ty phiếu', 'Công ty đang làm việc của người lập lúc tạo phiếu. Cả luồng (YCHG → YCTG → PTG → giá áp) thuộc công ty '
     'này; giá áp cho đúng công ty này, không ảnh hưởng công ty khác.'),
    ('Nhóm hàng', '1 cặp Thương hiệu — Hãng sản xuất trong phiếu, đánh số La Mã I, II, III…; hàng trong nhóm đánh 1, 2, 3…'),
    ('PTKD', 'Người có quyền “' + Q1 + '” tại công ty phiếu — duyệt / từ chối CẢ phiếu.'),
    ('XNK phụ trách', 'Người mua (Phòng XNK) đang được phân công phụ trách cặp Thương hiệu × Hãng × công ty phiếu (màn Phân '
     'công nhân viên phụ trách), có quyền “' + Q2 + '”.'),
    ('YCTG', 'Yêu cầu tính giá — XNK lập cho 1 nhóm đã duyệt (1 nhóm – 1 YCTG).'),
    ('PTG', 'Phiếu tính giá — Kế toán mua hàng lập từ YCTG, ra giá bán mới.'),
    ('Kết quả tính giá', 'Bản chụp giá bán mới lúc được áp (6 loại giá × mọi ĐVT + ĐMGG) — xem ở “Chi tiết kết quả”.'),
    ('Giá bán lẻ hiện hành', 'Giá Bán lẻ đang áp dụng của ĐVT cơ bản tại công ty phiếu, đọc lúc mở màn.'),
    ('Trạng thái hàng', 'Trạng thái của hàng TẠI công ty phiếu: Đang nhập thông tin · Chờ tính giá bán · Đang tính giá · Đang '
     'kinh doanh · Ngừng kinh doanh · Hàng tạm · Hàng tạm đã duyệt · Hàng tạm không duyệt.'),
    ('Hàng tạm', 'Hàng do người lập tạo ngay trong YCHG (popup Thêm hàng tạm); PTKD phải duyệt từng hàng tạm trước khi duyệt '
     'phiếu.'),
    ('ĐMGG', 'Định mức giảm giá tối đa (%) của loại giá.'),
], widths=[1.6, 4.4])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Lập, sửa, gửi, xoá, xem YCHG KHÔNG cần quyền. Mọi quyền dưới đây xét tại CÔNG TY PHIẾU (= công ty đang làm việc; '
    'phiếu công ty khác coi như không tồn tại). Super admin không được miễn: thiếu quyền là không thấy nút và bị hệ thống '
    'từ chối khi gọi thẳng chức năng.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1,
     'Thấy nút Duyệt / Từ chối ở chân màn Chi tiết của MỌI phiếu Chờ PTKD duyệt trong công ty (không xét phân công hãng), '
     'nút Xử lý ở danh sách; duyệt từng hàng tạm (form Duyệt hàng tạm). Người có Q1 tại công ty là người NHẬN thông báo '
     '“[YCHG] Chờ duyệt … Người lập”.'),
    ('Q2', Q2,
     'Chỉ có tác dụng khi người dùng ĐỒNG THỜI là XNK được phân công hiện hành của nhóm: thấy Duyệt / Không có giá ở nhóm Chờ '
     'XNK duyệt; Lập YCTG / Huỷ duyệt ở nhóm Chờ lập YCTG chưa có YCTG; nút Xử lý nhóm / Lập YCTG ở danh sách. Có Q2 mà '
     'không phải XNK phân công → không có nút, gọi thẳng bị từ chối. Q2 cũng mở link số YCTG.'),
    ('Q3', Q3, 'Ở màn này chỉ có tác dụng mở link số YCTG trên dòng nhóm (không có thì số YCTG là chữ thường).'),
    ('Q4', Q4, 'Ở màn này chỉ có tác dụng mở link số YCTG. KHÔNG cần để xem giá bán mới (Chi tiết kết quả chỉ có giá bán).'),
    ('Q5', Q5, 'Sửa được hàng tạm do NGƯỜI KHÁC tạo trong form YCHG (người tạo hàng tạm luôn sửa được hàng của mình).'),
], widths=[0.7, 1.9, 3.4])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (KHÔNG phải quyền gán — phạm vi tính theo dữ liệu phiếu):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Người lập phiếu (không cần quyền)',
     'Thấy, sửa, xoá phiếu Đang tạo / Không duyệt CỦA CHÍNH MÌNH. Phiếu Đang tạo / Không duyệt của người khác không hiện ở danh '
     'sách; mở thẳng → trang “' + MSG_404PAGE + '”.'),
    ('V2', 'Mọi nhân viên của công ty (không cần quyền)',
     'Thấy mọi phiếu ĐÃ GỬI (Chờ PTKD duyệt, Đang hỏi giá, Đã tính giá, Không có giá, Huỷ duyệt) của công ty đang làm việc, '
     'kể cả giá bán mới trong Chi tiết kết quả. Không phân quyền theo phòng ban / bộ phận / cấp quản lý.'),
    ('V3', 'Công ty khác', 'Không thấy, không thao tác được phiếu của công ty khác (hệ thống báo “' + MSG_NOTFOUND + '”, không '
     'lộ là phiếu có tồn tại). Đổi công ty đang làm việc thì danh sách đổi theo.'),
], widths=[0.7, 1.9, 3.4])

d.h2('2 Ma trận phân quyền')
d.p('Cột “Không có quyền nào” = nhân viên bình thường của công ty (V1/V2). ✅ = được, ❌ = không được.')
d.table(['Chức năng', 'Q1', 'Q2 (+ phân công)', 'Q3 / Q4', 'Q5', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách YCHG', '✅', '✅', '✅', '✅', '✅ (V1 + V2)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tạo YCHG (Lưu nháp / Lưu và gửi duyệt)', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Chọn hàng hoá (popup)', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 Thêm / sửa hàng tạm (popup)', '✅', '✅', '✅', '✅ sửa cả hàng tạm người khác tạo', '✅ (sửa: chỉ hàng tạm mình tạo)'),
    ('FR-07 Sửa YCHG', '✅ chỉ người lập', '✅ chỉ người lập', '✅ chỉ người lập', '✅ chỉ người lập',
     '✅ chỉ người lập, phiếu Đang tạo / Không duyệt'),
    ('FR-08 Xem chi tiết YCHG', '✅', '✅', '✅ + mở link YCTG', '✅', '✅ (V1 + V2; số YCTG là chữ thường)'),
    ('FR-09 Xoá YCHG', '✅ chỉ người lập', '✅ chỉ người lập', '✅ chỉ người lập', '✅ chỉ người lập',
     '✅ chỉ người lập, phiếu Đang tạo / Không duyệt'),
    ('FR-10 PTKD duyệt phiếu', '✅ (phiếu Chờ PTKD duyệt)', '❌', '❌', '❌', '❌ (hệ thống từ chối khi gọi thẳng)'),
    ('FR-11 PTKD từ chối phiếu', '✅ (phiếu Chờ PTKD duyệt)', '❌', '❌', '❌', '❌ (hệ thống từ chối khi gọi thẳng)'),
    ('FR-12 PTKD duyệt hàng tạm', '✅ (phiếu Chờ PTKD duyệt)', '❌', '❌', '❌', '❌ (form báo không tìm thấy trang)'),
    ('FR-13 XNK duyệt nhóm / Lập YCTG', '❌', '✅ chỉ nhóm mình được phân công', '❌', '❌', '❌'),
    ('FR-14 XNK không có giá / Huỷ duyệt nhóm', '❌', '✅ chỉ nhóm mình được phân công', '❌', '❌', '❌'),
    ('FR-15 Xem giá bán mới (Chi tiết kết quả)', '✅', '✅', '✅', '✅', '✅ (ai thấy phiếu đều xem)'),
    ('FR-16 In phiếu / In kết quả', '✅', '✅', '✅', '✅', '✅ (ai thấy phiếu đều in)'),
], widths=[1.9, 0.9, 1.0, 0.8, 0.8, 1.0])

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_LAP, [0, 1, 2, 3, 9, 10]), (A_PTKD, [0, 4, 5, 6]), (A_XNK, [0, 7, 8])],
    [('FR-01', 'Xem danh sách YCHG', 'view'),            # 0
     ('FR-04', 'Tạo YCHG', 'crud'),                       # 1
     ('FR-07', 'Sửa YCHG', 'crud'),                       # 2
     ('FR-09', 'Xoá YCHG', 'action'),                     # 3
     ('FR-10', 'PTKD duyệt phiếu', 'action'),             # 4
     ('FR-11', 'PTKD từ chối phiếu', 'action'),           # 5
     ('FR-12', 'PTKD duyệt hàng tạm', 'action'),          # 6
     ('FR-13', 'XNK duyệt nhóm / Lập YCTG', 'action'),   # 7
     ('FR-14', 'XNK không có giá / Huỷ duyệt', 'action'),  # 8
     ('FR-15', 'Xem giá bán mới', 'view'),                # 9
     ('FR-16', 'In phiếu / In kết quả', 'io')],          # 10
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-05', 'Chọn hàng hoá', 'crud', 'extend', [1, 2], None),
     ('FR-06', 'Thêm / sửa hàng tạm', 'crud', 'extend', [1, 2], None),
     ('FR-08', 'Xem chi tiết YCHG', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Yêu cầu hỏi giá')

d.h2('2 Đặc tả chi tiết từng chức năng')

LIST_RULE = ('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn '
             'Yêu cầu hỏi giá tại phần mô tả chi tiết.')
CREATE_RULE = ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu hỏi giá '
               'tại phần mô tả chi tiết.')
NOTICE_RULE = '- Thông báo và Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu hỏi giá tại phần mô tả chi tiết.'
DETAIL_RULE = '- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu hỏi giá tại phần mô tả chi tiết.'
VALIDATE_SEND = [
    '– Không có hàng → “' + MSG_NO_ROW + '” (dưới tiêu đề khối Hàng hoá hỏi giá).',
    '– Ghi chú > 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.” (dưới ô Ghi chú).',
    '– (chỉ khi gửi) Nhóm chưa có XNK phụ trách → mỗi nhóm 1 dòng đỏ “' + MSG_NO_XNK + '”.',
    '– Hàng không còn chọn được → dòng đỏ dưới tên hàng “<mã>: <lý do>” (lý do xem BR-04); hàng không tồn tại → “Không tồn tại”.',
    '– Mọi lỗi báo cùng lúc; cuộn tới lỗi đầu tiên; không lưu gì.',
]

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách YCHG')
d.p('2.1.1 Giới thiệu')
d.rule_ref(LIST_RULE, anchor='list')
d.intro_table(
    ten='Xem danh sách yêu cầu hỏi giá',
    mota='Hiển thị các YCHG của CÔNG TY ĐANG LÀM VIỆC dạng bảng 2 tầng: dòng phiếu ▸ bấm mũi tên để bung các dòng nhóm '
         'Thương hiệu — Hãng (XNK phụ trách, trạng thái nhóm, số YCTG). Danh sách chỉ để tra cứu và điều hướng: mọi thao tác '
         'duyệt nằm ở màn Chi tiết.',
    tacnhan=A_LAP + '; ' + A_PTKD + '; ' + A_XNK + '; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và đã chọn công ty đang làm việc. Không cần quyền.',
    chinh='1. Người dùng vào Phân hệ Bán hàng › Yêu cầu › Hàng hóa › YC hỏi giá.\n'
          '2. Hệ thống lấy phiếu của công ty đang làm việc: mọi phiếu đã gửi + phiếu Đang tạo / Không duyệt của chính người '
          'dùng; mới tạo lên trước, 10 phiếu / trang.\n'
          '3. Mỗi phiếu 1 dòng; bấm nút mũi tên ở cột STT để bung / thu các dòng nhóm.\n'
          '4. Bấm số phiếu → màn Chi tiết (mục 2.8).',
    phu='• Không có phiếu nào / không khớp bộ lọc → “Không có dữ liệu phù hợp”.\n'
        '• Phiếu Đang tạo / Không duyệt của người khác không hiện.\n'
        '• Người dùng có việc cần làm (PTKD với phiếu Chờ PTKD duyệt, XNK phụ trách với nhóm Chờ XNK duyệt / Chờ lập YCTG) thấy '
        'nút Xử lý / Lập YCTG.\n'
        '• Lỗi tải → thông báo “Lỗi khi tải dữ liệu”.')
d.p('2.1.2 Layout màn hình')
d.p('Đường dẫn màn hình (1 lối vào menu; các lối vào khác mở thẳng màn Tạo / Chi tiết — xem mục 2.4, 2.8):')
d.layout(menu=MENU, shot=shot('00-menu.png'), shot_caption='Menu Bán hàng › Yêu cầu › Hàng hóa › YC hỏi giá (dữ liệu thật)')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Danh sách YCHG công ty 1 — 2.560 phiếu tài khoản E2E Assign nhìn thấy (dữ liệu thật)')
d.layout(menu=MENU, shot=shot('02-danh-sach-bung-nhom.png'),
         shot_caption='Bung dòng nhóm của 3 phiếu: Chờ XNK duyệt, Đã tính giá (PYCTG-03162), phiếu Chờ PTKD duyệt (dữ liệu thật)')
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang / khối', 'Label', 'Hiển thị', '–', 'Yêu cầu hỏi giá', 'Tiêu đề thanh đầu trang và khối bảng.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị', ['- Luôn hiện (không cần quyền).', '- Bấm → màn Tạo YCHG (mục 2.4).']),
    ('Nút Cấu hình cột', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Tooltip “Cấu hình cột hiển thị” → mục 2.3.'),
    ('Bảng yêu cầu hỏi giá', 'Table/Grid', 'Read-only', '9 cột', 'Theo dữ liệu', [
        '- Bảng 2 tầng: dòng phiếu (nền trắng) và dòng nhóm (nền xanh nhạt, vạch xanh bên trái).',
        '- Cột STT, Số phiếu dính trái khi cuộn ngang.',
        '- Mặc định sắp Ngày tạo mới → cũ; sắp được theo Số phiếu, Ngày tạo, PTKD duyệt (bấm tiêu đề cột).']),
    ('Cột STT', 'Text', 'Read-only', 'Số nguyên', 'Theo dữ liệu', [
        '- Dòng phiếu: nút tròn mũi tên + số thứ tự liên tục qua các trang.',
        '- Bấm mũi tên → bung / thu các dòng nhóm của phiếu (tooltip “Xem các nhóm hàng” / “Thu gọn”).',
        '- Dòng nhóm: ký hiệu “└”.']),
    ('Cột Số phiếu', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Dòng phiếu: số phiếu là link → bấm mở màn Chi tiết (mục 2.8); dòng dưới là Ghi chú phiếu (chữ xám) khi có.',
        '- Dòng nhóm: “<Thương hiệu> — <Hãng sản xuất>” + nhãn “<n> mã hàng”.']),
    ('Cột Số mã hàng', 'Number', 'Read-only', '≥ 1', 'Theo dữ liệu', 'Dòng phiếu: số mã hàng khác nhau của phiếu; dòng nhóm để trống.'),
    ('Cột Nhóm Thương hiệu — Hãng', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Dòng phiếu: “<a>/<b> nhóm đã tính giá” — a = số nhóm Đã tính giá, b = tổng số nhóm.',
        '- Dòng nhóm: “XNK: <tên - phòng - mã NV>” — nhóm chưa có YCTG hiện người đang được phân công HIỆN HÀNH, nhóm đã có YCTG '
        'hiện người đã xử lý.']),
    ('Cột Người tạo', 'Text', 'Read-only', '–', 'Theo dữ liệu', '“<Họ tên> - <mã phòng> - <mã NV>”; dòng nhóm để trống.'),
    ('Cột Ngày tạo', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Ngày lập phiếu; dòng nhóm để trống.'),
    ('Cột PTKD duyệt', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', [
        '- Dòng phiếu: người PTKD đã xử lý (duyệt hoặc từ chối) + thời điểm (chữ xám); chưa xử lý để trống.',
        '- Dòng nhóm: số YCTG của nhóm, hoặc “chưa có YCTG” khi nhóm đã qua PTKD mà chưa có YCTG.']),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách', 'Theo dữ liệu', [
        '- Dòng phiếu: Đang tạo (xám) · Chờ PTKD duyệt (cam) · Không duyệt (đỏ) · Đang hỏi giá (xanh dương) · Đã tính giá '
        '(xanh lá) · Không có giá (đỏ) · Huỷ duyệt (đỏ, chỉ phiếu cũ ERP).',
        '- Dòng nhóm: Chờ XNK duyệt (cam) · Chờ lập YCTG (xanh trời) · Đang tính giá (xanh dương) · Đã tính giá (xanh lá) · '
        'Không có giá (đỏ) · Huỷ duyệt (đỏ); nhóm của phiếu chưa qua PTKD không có nhãn.']),
    ('Cột Hành động (dòng phiếu)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo cờ quyền', [
        '- Sửa (bút): chỉ người lập, phiếu Đang tạo / Không duyệt → màn Sửa (mục 2.7).',
        '- Xóa (thùng rác đỏ): như Sửa → mục 2.9.',
        '- Xử lý (dấu tích tròn): PTKD với phiếu Chờ PTKD duyệt, hoặc XNK có nhóm cần xử lý → mở màn Chi tiết.',
        '- In (máy in): luôn hiện → mục 2.16.']),
    ('Cột Hành động (dòng nhóm)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo cờ quyền', [
        '- Lập YCTG (dấu cộng tròn): XNK phụ trách, nhóm Chờ lập YCTG chưa có YCTG → mở màn Tạo YCTG của nhóm.',
        '- Xử lý nhóm (dấu tích tròn): XNK phụ trách, nhóm Chờ XNK duyệt → mở Chi tiết, cuộn tới đúng nhóm.',
        '- Người khác: chữ xám “Chờ <tên XNK> duyệt” / “Chờ <tên XNK> lập YCTG”.']),
    ('Chân bảng', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', '10 dòng / trang', [
        '- “Hiển thị a–b / N yêu cầu”: N = tổng số phiếu khớp bộ lọc (dòng nhóm không tính).',
        '- Đổi số dòng → về trang 1.']),
    ('Trạng thái rỗng / đang tải', 'Label / Loading', 'Hiển thị', '–', 'Ẩn',
     ['- Không có dữ liệu: “Không có dữ liệu phù hợp”.', '- Lỗi tải: thông báo “Lỗi khi tải dữ liệu”.']),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Không kiểm quyền (YCHG không cần quyền xem).\n'
     'During:\n– Lấy phiếu có công ty = công ty đang làm việc (lấy từ phiên làm việc, không nhận từ màn hình).\n'
     '– Bỏ phiếu Đang tạo / Không duyệt của người khác.\n'
     '– Tính cờ nút từng dòng ở máy chủ (Sửa / Xóa / Xử lý / Lập YCTG) — màn hình chỉ hiện theo cờ.\n'
     'After:\n– Trang 1, 10 phiếu, sắp Ngày tạo mới → cũ; các dòng nhóm thu gọn.'),
    ('Bấm mũi tên ở cột STT', 'Click', 'After:\n– Bung / thu dòng nhóm của phiếu ngay tại chỗ (không tải lại).'),
    ('Bấm tiêu đề cột Số phiếu / Ngày tạo / PTKD duyệt', 'Click',
     'After:\n– Sắp tăng / giảm theo cột; bỏ sắp → về Ngày tạo giảm dần; về trang 1.'),
    ('Đổi trang / số dòng', 'Click / Change', 'After:\n– Tải lại; đổi số dòng thì về trang 1.'),
    ('Bấm Xử lý / Xử lý nhóm / Lập YCTG', 'Click',
     'After:\n– Xử lý → màn Chi tiết phiếu.\n– Xử lý nhóm → màn Chi tiết, nhóm được tô nền xanh và cuộn vào giữa màn.\n'
     '– Lập YCTG → màn Tạo YCTG của nhóm (đặc tả ở SRS Yêu cầu tính giá).'),
    ('Đổi công ty đang làm việc', 'System', 'After:\n– Danh sách tải lại theo công ty mới; phiếu công ty cũ biến mất.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu hỏi giá tại phần mô tả chi '
           'tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc yêu cầu hỏi giá',
    mota='Thu hẹp danh sách theo số phiếu / mã / tên hàng, trạng thái, thương hiệu, hãng, người tạo, người PTKD xử lý, XNK '
         'tiếp nhận và khoảng ngày tạo.',
    tacnhan=A_LAP + '; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách YCHG.',
    chinh='1. Gõ từ khoá vào ô tìm nhanh rồi nhấn Enter hoặc bấm Tìm kiếm.\n'
          '2. Bấm Tìm kiếm nâng cao để mở các ô lọc; chọn giá trị — mỗi lần chọn là lọc ngay.\n'
          '3. Hệ thống tải lại danh sách từ trang 1.',
    phu='• Bấm Làm mới → xoá mọi điều kiện, sắp lại theo Ngày tạo giảm dần.\n'
        '• Hệ thống ghi nhớ bộ lọc trong 10 phút khi quay lại màn từ màn Chi tiết / Sửa.\n'
        '• Không có kết quả → “Không có dữ liệu phù hợp”.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('03-loc-nang-cao.png'),
         shot_caption='Khối bộ lọc khi mở Tìm kiếm nâng cao (dữ liệu thật)')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
        '- Placeholder “Tìm theo số phiếu, mã hoặc tên hàng hoá”.',
        '- Tìm gần đúng trên số phiếu, mã hàng và tên hàng ghi trong phiếu (tên lúc lập).',
        '- KHÔNG tìm theo tên người tạo / PTKD / XNK — dùng ô chọn ở bộ lọc nâng cao.']),
    ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     ['- Tìm kiếm: chạy theo từ khoá + ô lọc, về trang 1.', '- Làm mới: xoá mọi ô lọc, về sắp xếp mặc định.']),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Đóng',
     ['- Mặc định khối ô lọc đang đóng.', '- Bấm để mở / đóng (“Ẩn tìm kiếm nâng cao”).']),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 7 giá trị', 'Không', 'Trống', [
        '- Đang tạo · Chờ PTKD duyệt · Không duyệt · Đang hỏi giá · Đã tính giá · Không có giá · Huỷ duyệt.',
        '- “Đang hỏi giá” gồm cả các phiếu cũ của ERP đang ở bước XNK / tính giá.',
        '- Lọc Đang tạo / Không duyệt chỉ ra phiếu của chính người dùng.']),
    ('Thương hiệu', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Chỉ liệt kê thương hiệu có trong nhóm của các phiếu công ty; lọc phiếu có ít nhất 1 nhóm thuộc thương hiệu.'),
    ('Hãng sản xuất', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Như Thương hiệu, theo hãng sản xuất.'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', '“<Họ tên> - <phòng> - <mã NV>”, xếp theo tên.'),
    ('PTKD duyệt', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Người PTKD đã xử lý phiếu (cả người DUYỆT lẫn người TỪ CHỐI).'),
    ('XNK tiếp nhận', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', [
        '- Người XNK đã ghi trên nhóm (lúc gửi phiếu / lúc PTKD duyệt / lúc XNK xử lý).',
        '- Lưu ý: cột XNK ở dòng nhóm chưa có YCTG hiện người phân công HIỆN HÀNH — đổi phân công sau khi gửi thì 2 bên có '
        'thể khác nhau.']),
    ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống',
     'Khoảng ngày lập phiếu, tính cả ngày đầu và ngày cuối.'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Nhấn Enter / bấm Tìm kiếm', 'Keypress / Click', 'After:\n– Tải lại từ trang 1 theo từ khoá + ô lọc.'),
    ('Chọn giá trị ô lọc', 'Change', 'After:\n– Lọc ngay, về trang 1 (1 lần tải cho mỗi lần đổi).'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, sắp theo Ngày tạo giảm dần, tải lại trang 1.'),
    ('Quay lại màn danh sách', 'System', 'After:\n– Khôi phục bộ lọc + trạng thái đóng / mở khối lọc trong 10 phút.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Cài đặt bộ lọc và tuỳ chỉnh cột')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu hỏi giá tại phần mô tả chi tiết.',
           anchor='excel')
d.intro_table(
    ten='Cài đặt bộ lọc và tuỳ chỉnh cột',
    mota='Ẩn / hiện, đổi thứ tự các ô lọc và các cột của bảng danh sách; cấu hình lưu theo người dùng.',
    tacnhan=A_LAP + '; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách YCHG.',
    chinh='1. Bấm nút Cấu hình cột (hoặc Cài đặt bộ lọc).\n2. Tích / bỏ tích, kéo thả để đổi thứ tự.\n3. Bấm Lưu.',
    phu='• Bấm Đóng → không lưu.\n• Cột STT, Số phiếu, Hành động bị khoá (luôn hiện).')
d.p('2.3.2 Layout màn hình')
d.layout(menu=MENU + ' => Cấu hình cột', shot=shot('04-cau-hinh-cot.png'), shot_caption='Popup Tuỳ chỉnh cột (dữ liệu thật)')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', 'Câu dẫn “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '9 cột', 'Không', 'Theo cấu hình đã lưu', [
        '- STT · Số phiếu · Số mã hàng · Nhóm Thương hiệu — Hãng · Người tạo · Ngày tạo · PTKD duyệt · Trạng thái · Hành động.',
        '- Khoá (không bỏ tích được): STT, Số phiếu, Hành động.',
        '- Kéo thả để đổi thứ tự.']),
    ('Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ chọn hết vẫn giữ các cột khoá.'),
    ('Dòng đếm', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn <n>/9 cột”.'),
    ('Nút Lưu / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu: áp ngay và lưu theo người dùng. Đóng: bỏ thay đổi.'),
])
d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cấu hình cột', 'Click', 'After:\n– Mở popup với cấu hình đã lưu của người dùng.'),
    ('Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình theo người dùng; bảng hiện đúng các cột, đúng thứ tự.'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Tạo YCHG')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo YCHG', 'crud', actor=A_LAP, caption='Biểu đồ Use Case — FR-04 Tạo YCHG')
d.p('2.4.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Tạo yêu cầu hỏi giá',
    mota='Lập phiếu hỏi giá cho 1 hay nhiều hàng của công ty đang làm việc. Hàng tự gom nhóm Thương hiệu — Hãng; mỗi nhóm '
         'hiện XNK phụ trách. Lưu nháp (Đang tạo) hoặc Lưu và gửi duyệt (Chờ PTKD duyệt).',
    tacnhan=A_LAP + '; Người dùng đã đăng nhập',
    dieukien='Đã chọn công ty đang làm việc. Không cần quyền.',
    chinh='1. Mở màn Tạo bằng 1 trong các lối vào ở mục 2.4.3.\n'
          '2. (Tuỳ chọn) nhập Ghi chú.\n'
          '3. Bấm Chọn hàng hoá (mục 2.5) hoặc Thêm hàng tạm (mục 2.6); hàng hiện ngay theo nhóm.\n'
          '4. Bấm Lưu nháp → phiếu Đang tạo; hoặc Lưu và gửi duyệt → hộp xác nhận → phiếu Chờ PTKD duyệt.\n'
          '5. Thông báo “Đã lưu nháp yêu cầu hỏi giá” / “Đã gửi yêu cầu hỏi giá”; quay về danh sách YCHG.',
    phu='• Vào từ màn hàng hoá có tick hàng → form nạp sẵn hàng đã tick; hàng không lập YCHG được bị loại kèm thông báo “Bỏ <n> '
        'hàng không lập yêu cầu hỏi giá được: <mã> (<lý do>)”.\n'
        '• Nhóm chưa có XNK phụ trách: dòng nhóm hiện cảnh báo nâu “Chưa có XNK phụ trách tại công ty — chưa gửi được”; Lưu nháp '
        'vẫn được, Lưu và gửi duyệt bị chặn (chữ đỏ, không gửi).\n'
        '• Hàng Đang kinh doanh đang nằm trong YCHG mở khác → cảnh báo “Đang được hỏi giá ở <mã phiếu>”, KHÔNG chặn.\n'
        '• Bỏ hàng bằng nút thùng rác trên dòng (không hỏi lại); nhóm hết hàng tự mất.\n'
        '• Bấm Quay lại khi đã nhập → hộp “Thông tin chưa lưu”.\n'
        '• Gửi duyệt: hàng Đang nhập thông tin chuyển “Chờ tính giá bán”; hàng Đang kinh doanh giữ nguyên trạng thái và giá.',
    dacbiet='Không có nút “Lưu và tiếp tục” (phiếu lập theo bộ hàng đã chọn rồi gửi). Không chọn ĐVT: phiếu hỏi giá cho MỌI '
            'ĐVT đã khai của hàng.')
d.p('2.4.3 Layout màn hình')
d.p('Đường dẫn màn hình (3 lối vào mở cùng 1 form Tạo):')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('08-tao-moi.png'), shot_caption='Form Tạo yêu cầu hỏi giá trống (dữ liệu thật)')
d.layout(menu=MENU_TRADING, shot=shot('18-man-hang-hoa-tick.png'),
         shot_caption='Màn Hàng đang kinh doanh: tick 2 hàng rồi bấm “Lập yêu cầu hỏi giá” ở đầu bảng (dữ liệu thật)')
d.layout(menu=MENU_ENTERING, shot=shot('19-nap-san-tu-man-hang.png'),
         shot_caption='Form Tạo nạp sẵn 2 hàng TORIN đã tick, gom 1 nhóm, XNK tiếp nhận Nguyễn Thị Thu Thủy (dữ liệu thật)')
d.bullets([
    'Màn Hàng tạm (Danh mục › Hàng hoá › Hàng hoá, vật tư › Hàng tạm): hành động dòng “Lập yêu cầu hỏi giá” hoặc tick nhiều hàng '
    'tạm → form Tạo nạp sẵn (chỉ hàng tạm chưa nằm trong YCHG mở).',
    'Không tick hàng nào mà bấm “Lập yêu cầu hỏi giá” ở màn hàng hoá → form Tạo trống. Nút Quay lại về đúng màn hàng hoá đã đi '
    'vào; lưu xong luôn về danh sách YCHG.',
])
d.layout(menu=MENU + ' => Tạo mới', shot=shot('12-nhieu-nhom.png'),
         shot_caption='4 hàng của 3 hãng gom 3 nhóm La Mã; nhóm FOFEN chưa có XNK phụ trách (dữ liệu thật)')
d.layout(menu=MENU + ' => Tạo mới => Lưu và gửi duyệt', shot=shot('13-nhom-thieu-xnk.png'),
         shot_caption='Bấm Lưu và gửi duyệt khi còn nhóm thiếu XNK: chữ đỏ, không gửi (dữ liệu thật, 0 lệnh ghi)')
d.layout(menu=MENU + ' => Tạo mới => Lưu và gửi duyệt', shot=shot('09-loi-chua-chon-hang.png'),
         shot_caption='Gửi khi chưa có hàng: “Vui lòng chọn ít nhất 1 hàng hoá” (dữ liệu thật)')
d.layout(menu=MENU + ' => Tạo mới => Lưu và gửi duyệt', shot=shot('14-xac-nhan-gui.png'),
         shot_caption='Hộp xác nhận gửi khi mọi nhóm đã có XNK (dữ liệu thật — bấm Hủy, không gửi)')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('20-loai-hang-khong-chon-duoc.png'),
         shot_caption='Nạp sẵn hàng chưa dùng ở công ty: hàng bị loại kèm thông báo (dữ liệu thật)')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('15-roi-man-chua-luu.png'),
         shot_caption='Bấm Quay lại khi chưa lưu: hộp “Thông tin chưa lưu” (dữ liệu thật)')
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Dòng người tạo', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', '“<Tên người đang đăng nhập> - <dd/mm/yyyy hh:mm>” góc phải khối Thông tin chung.'),
    ('Số phiếu', 'Textbox', 'Disable', '–', '–', 'Trống', 'Placeholder “Tự sinh khi lưu”; sinh dạng PYCHG-xxxxx nối tiếp dãy số của ERP.'),
    ('Công ty', 'Textbox', 'Disable', '–', '–', 'Công ty đang làm việc', 'Công ty phiếu — không đổi được; muốn hỏi giá cho công ty khác thì đổi công ty đang làm việc.'),
    ('Người tạo', 'Textbox', 'Disable', '–', '–', 'Người đang đăng nhập', '–'),
    ('Trạng thái', 'Badge', 'Read-only', '–', '–', 'Đang tạo', 'Nhãn xám “Đang tạo” khi chưa lưu.'),
    ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     ['- Placeholder “Nhập ghi chú”.', '- > 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.” (báo ngay khi gõ).']),
    ('Nút Thêm hàng tạm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đứng trái nút Chọn hàng hoá → mục 2.6.'),
    ('Nút Chọn hàng hoá', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở popup Chọn hàng hoá → mục 2.5.'),
    ('Bảng Hàng hoá hỏi giá', 'Table/Grid', 'Enable', '8 cột', '–', 'Trống', [
        '- Cột: STT · Mã hàng · Tên hàng hoá · Model · ĐVT · Trạng thái hàng · Giá bán lẻ hiện hành · Hành động.',
        '- Rỗng: “Chưa có hàng hoá nào. Bấm "Chọn hàng hoá" để thêm.”']),
    ('Dòng nhóm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', [
        '- Số La Mã + “<Thương hiệu> — <Hãng>” + nhãn “<n> mã hàng”.',
        '- Có phân công: “XNK tiếp nhận: <tên - phòng - mã NV>” (người mua phân công hiện hành của thương hiệu × hãng × công ty).',
        '- Không có: cảnh báo nâu “Chưa có XNK phụ trách tại công ty — chưa gửi được”.',
        '- Nhóm sắp theo tên thương hiệu + hãng (A → Z).']),
    ('Cột Mã hàng / Tên hàng hoá / Model', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', [
        '- Dưới tên: “Đang được hỏi giá ở <mã phiếu>” (nâu) khi hàng đang nằm trong YCHG mở khác.',
        '- Hàng tạm sinh từ dòng BOM / báo giá: “Lập từ <mã dòng> · BOM <mã> / báo giá <mã>” (xám).',
        '- Lỗi của máy chủ cho riêng hàng: chữ đỏ dưới tên “<mã>: <lý do>”.']),
    ('Cột ĐVT', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', 'Mọi ĐVT đã khai của hàng, nối bằng “ · ” (ĐVT cơ bản đứng đầu).'),
    ('Cột Trạng thái hàng', 'Badge', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Trạng thái của hàng TẠI công ty phiếu (Đang nhập thông tin / Đang kinh doanh / Hàng tạm…).'),
    ('Cột Giá bán lẻ hiện hành', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', [
        '- Giá Bán lẻ ĐANG ÁP DỤNG của ĐVT cơ bản tại công ty phiếu, dấu phẩy ngăn nghìn (vd 22,500,000).',
        '- Hàng chưa có dòng giá: để trống (khác giá 0 — có dòng giá bằng 0 thì hiện “0”).',
        '- Chỉ để tham khảo, không sửa ở màn này.']),
    ('Cột Hành động', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', [
        '- Thùng rác (tooltip “Bỏ hàng khỏi phiếu”; hàng tạm: “Bỏ khỏi phiếu — hàng tạm vẫn giữ ở màn Hàng tạm”) → bỏ ngay, không hỏi.',
        '- Bút “Sửa hàng tạm”: chỉ với hàng tạm do người dùng tạo, hoặc người có quyền ' + Q5 + ' → mục 2.6.']),
    ('Lỗi khối hàng', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     ['- “' + MSG_NO_ROW + '”.', '- Mỗi nhóm thiếu XNK: “' + MSG_NO_XNK + '”.']),
    ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu trạng thái Đang tạo; khoá trong lúc đang lưu.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Kiểm lỗi → hộp xác nhận → gửi PTKD.'),
    ('Hộp xác nhận gửi', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', [
        '- Tiêu đề “Gửi yêu cầu hỏi giá”.',
        '- “Gửi yêu cầu hỏi giá <số phiếu | mới> (<n> mã hàng, <m> nhóm) cho PTKD duyệt? Hàng đang nhập thông tin sẽ chuyển sang '
        '"Chờ tính giá bán".”',
        '- Nút “Lưu và gửi duyệt” / “Hủy”.']),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     ['- Về màn đã đi vào (màn hàng hoá) hoặc danh sách YCHG.', '- Có thay đổi chưa lưu → hộp “Thông tin chưa lưu” (Thoát / Ở lại).']),
])
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Tạo', 'System',
     'After:\n– Công ty = công ty đang làm việc.\n– Có danh sách hàng tick sẵn → lấy dòng hàng, loại hàng không chọn được + thông báo '
     '“Bỏ <n> hàng không lập yêu cầu hỏi giá được: <mã> (<lý do>); …”.'),
    ('Thêm / bỏ hàng', 'Change', 'After:\n– Gom lại nhóm theo Thương hiệu × Hãng ngay trên màn; xoá lỗi cũ của máy chủ.'),
    ('Bấm Lưu nháp', 'Click',
     'Before:\n– Không kiểm quyền.\nDuring:\n' + '\n'.join(VALIDATE_SEND[:2] + VALIDATE_SEND[3:]) + '\n'
     'After:\n– Lưu phiếu Đang tạo, sinh số PYCHG-xxxxx; gom nhóm; nhóm chưa ghi XNK.\n– Trạng thái hàng KHÔNG đổi.\n'
     '– Thông báo “Đã lưu nháp yêu cầu hỏi giá”; về danh sách YCHG.'),
    ('Bấm Lưu và gửi duyệt', 'Click',
     'Before:\n– Không kiểm quyền.\nDuring:\n' + '\n'.join(VALIDATE_SEND) + '\n– Hỏi xác nhận; Hủy → không gửi.\n'
     '– Máy chủ khoá các hàng × công ty trước khi kiểm: 2 phiếu gửi cùng lúc chứa cùng 1 hàng Đang nhập thông tin → chỉ 1 phiếu '
     'thành công, phiếu sau báo “<mã>: Hàng đang được hỏi giá ở <mã phiếu>”.\n'
     'After:\n– Phiếu Chờ PTKD duyệt, ghi thời điểm gửi; mỗi nhóm ghi XNK phụ trách lúc gửi.\n'
     '– Hàng Đang nhập thông tin → Chờ tính giá bán (tại công ty phiếu); hàng Đang kinh doanh giữ nguyên.\n'
     '– Ghi lịch sử “Lập phiếu yêu cầu hỏi giá”.\n'
     '– Gửi “[YCHG] Chờ duyệt: <số phiếu>. Người lập: <tên>” tới mọi người có quyền ' + Q1 + ' tại công ty phiếu.\n'
     '– Thông báo “Đã gửi yêu cầu hỏi giá”; về danh sách YCHG.'),
    ('Bấm Quay lại', 'Click', 'Before:\n– Có thay đổi chưa lưu → hộp “Thông tin chưa lưu”; Ở lại → giữ nguyên form.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Chọn hàng hoá')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chọn hàng hoá', 'crud', actor=A_LAP, caption='Biểu đồ Use Case — FR-05 Chọn hàng hoá')
d.p('2.5.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Popup Chọn hàng hoá',
    mota='Tìm và tick nhiều hàng của công ty đang làm việc để đưa vào phiếu. Chỉ liệt kê hàng ĐƯỢC hỏi giá.',
    tacnhan=A_LAP,
    dieukien='Đang ở form Tạo / Sửa YCHG.',
    chinh='1. Bấm Chọn hàng hoá.\n2. Gõ mã / tên / model để tìm (tự tìm sau 0,3 giây).\n'
          '3. Tick các hàng cần hỏi giá (giữ tick qua các trang).\n4. Bấm Chọn → hàng vào bảng, gom nhóm.',
    phu='• Hàng đã có trên phiếu không hiện trong popup (tổng số đếm đúng).\n'
        '• Hàng Đang kinh doanh đang nằm trong YCHG mở khác vẫn chọn được, kèm “Đang được hỏi giá ở <mã phiếu>”.\n'
        '• Không có hàng phù hợp → “Không có hàng hoá phù hợp”; lỗi tải → “Không tải được danh sách hàng hoá, vui lòng thử lại.”\n'
        '• Chưa tick → nút Chọn bị khoá. Bấm Đóng / ✕ → không thêm gì.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Chọn hàng hoá', shot=shot('10-popup-chon-hang.png'),
         shot_caption='Popup Chọn hàng hoá: tìm “SULI-0-”, tick 2 hàng (dữ liệu thật)')
d.layout(menu=MENU + ' => Tạo mới => Chọn hàng hoá', shot=shot('11-tao-moi-da-chon.png'),
         shot_caption='2 hàng SULI vào nhóm I, XNK tiếp nhận Đinh Hà Duyên (dữ liệu thật)')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Chọn hàng hoá', '–'),
    ('Ô tìm', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     ['- Placeholder “Tìm theo mã, tên hoặc model hàng hoá”.', '- Tìm gần đúng mã, tên, tên model; tự chạy sau khi ngừng gõ 0,3 giây.']),
    ('Bảng hàng', 'Table/Grid', 'Enable', '6 cột', '–', 'Theo dữ liệu', [
        '- Ô tick · Mã hàng · Tên hàng hoá · Model · Thương hiệu — Hãng · Trạng thái hàng; xếp theo mã hàng.',
        '- Chỉ hàng Đang nhập thông tin / Đang kinh doanh tại công ty, hoặc hàng tạm (Hàng tạm / Hàng tạm không duyệt) chưa nằm '
        'trong YCHG mở; không có hàng đã xoá.']),
    ('Phân trang', 'Pagination', 'Enable', '10 / 20 / 50 / 100', '–', '10 dòng / trang', 'Tick giữ nguyên khi đổi trang / đổi từ khoá.'),
    ('Dòng đếm đã chọn', 'Text', 'Read-only', '≥ 0', '–', 'Đã chọn: 0', '“Đã chọn: <n>” ở chân popup.'),
    ('Nút Chọn', 'Button', 'Enable / Disable', '–', '–', 'Disable', 'Khoá khi chưa tick; bấm → đóng popup, thêm hàng vào phiếu.'),
    ('Nút Đóng / ✕', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không thêm.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở popup', 'Click', 'After:\n– Xoá tick + từ khoá cũ; tải trang 1, loại hàng đã có trên phiếu.'),
    ('Gõ từ khoá', 'Keypress', 'After:\n– Sau 0,3 giây tìm lại từ trang 1 (chỉ lấy kết quả của lần gõ cuối).'),
    ('Bấm Chọn', 'Click', 'After:\n– Thêm các hàng đã tick (bỏ trùng); gom nhóm; xoá lỗi cũ.'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Thêm / sửa hàng tạm')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Thêm / sửa hàng tạm', 'crud', actor=A_LAP, caption='Biểu đồ Use Case — FR-06 Thêm / sửa hàng tạm')
d.p('2.6.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Popup Thêm hàng tạm / Sửa hàng tạm',
    mota='Tạo nhanh hàng chưa có trong danh mục (hàng tạm) ngay trong YCHG, hoặc dùng lại dòng tạm của BOM / báo giá dự án; '
         'hàng tạm vừa tạo vào phiếu như hàng chọn thường. PTKD sẽ duyệt từng hàng tạm (mục 2.12).',
    tacnhan=A_LAP,
    dieukien='Đang ở form Tạo / Sửa YCHG. Danh mục Loại sản phẩm + Đặc tính phải có dữ liệu.',
    chinh='1. Bấm Thêm hàng tạm → popup 2 tab.\n'
          '2. Tab “Chọn từ kho hàng tạm (Tái sử dụng)”: chọn 1 dòng tạm BOM / báo giá → “Dùng hàng này” → điền sẵn tab nhập.\n'
          '3. Tab “Thêm mới thủ công”: nhập đủ ô bắt buộc.\n'
          '4. Bấm Lưu (đóng popup) hoặc Lưu và tiếp tục (form trống, tạo tiếp).\n'
          '5. Thông báo “Đã thêm hàng tạm <mã> vào phiếu”; hàng tạm vào bảng, gom nhóm.',
    phu='• Thiếu ô bắt buộc → báo đồng thời mọi ô + thông báo “Vui lòng kiểm tra lại dữ liệu nhập”.\n'
        '• Sửa hàng tạm (bút trên dòng): popup “Sửa hàng tạm · <mã>”, không có tab Tái sử dụng, không đổi được ĐVT; hàng đã '
        'được PTKD Đồng ý / Không duyệt mà sửa → “Đã lưu — hàng trở về "Hàng tạm" (chờ PTKD duyệt lại)”.\n'
        '• Bấm ra ngoài popup KHÔNG đóng; bấm Đóng / ✕ → không lưu.\n'
        '• Bỏ hàng tạm khỏi phiếu → hàng tạm vẫn còn ở màn Hàng tạm.',
    dacbiet='Hàng tạm được tạo NGAY khi bấm Lưu trong popup (trước khi lưu phiếu). Lưu phiếu sau đó mới gắn hàng tạm vào phiếu.')
d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Thêm hàng tạm', shot=shot('16-hang-tam-tai-su-dung.png'),
         shot_caption='Tab Chọn từ kho hàng tạm (Tái sử dụng) (dữ liệu thật — tài khoản không có dòng tạm dự án)')
d.layout(menu=MENU + ' => Tạo mới => Thêm hàng tạm', shot=shot('17-hang-tam-thu-cong-loi.png'),
         shot_caption='Tab Thêm mới thủ công: bấm Lưu khi trống — báo đồng thời 12 ô (dữ liệu thật, lệnh lưu bị chặn)')
d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề', 'Label', 'Hiển thị', '–', '–', 'Thêm hàng tạm', '“Thêm hàng tạm” / “Sửa hàng tạm · <mã>”.'),
    ('Tab Tái sử dụng – bảng', 'Table/Grid', 'Enable', '9 cột', 'Không', 'Theo dữ liệu', [
        '- Ô chọn 1 dòng · Mã hàng · Tên hàng · Model · Thương hiệu · Xuất xứ · ĐVT · Nguồn (BOM / Báo giá) · Dự án.',
        '- Ô tìm “Tìm nhanh theo mã / tên hàng tạm...”; rỗng: “Không có hàng tạm phù hợp.”',
        '- Gợi ý: “Chỉ hiện dòng tạm BOM / báo giá CHƯA thành hàng hoá, trong các dự án bạn được xem. Chọn 1 dòng ⇒ điền sẵn Tên, '
        'ĐVT, Thương hiệu, Xuất xứ, Model, TSKT; lưu xong mọi dòng cùng gốc được gắn mã hàng mới.”',
        '- Nút “Dùng hàng này” (khoá khi chưa chọn) / “Đóng”.']),
    ('Dải điền sẵn', 'Text', 'Hiển thị', '–', '–', 'Ẩn', '“Điền sẵn từ <mã> (<BOM | Báo giá> · <dự án>) — nhập nốt các ô còn trống.” + link “Bỏ điền sẵn”.'),
    ('Tên hàng hoá', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', 'Trống → “Bắt buộc phải nhập”.'),
    ('Đơn vị tính', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Có', 'Trống',
     ['- Chỉ ĐVT được làm ĐVT cơ bản; thành ĐVT cơ bản hệ số 1.', '- Sửa hàng tạm: chỉ đọc.', '- Trống → “Bắt buộc phải chọn”.']),
    ('Model / Thương hiệu / Xuất xứ', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống',
     ['- Ô chọn tìm theo từ khoá; dấu ⊕ để thêm nhanh danh mục.', '- Trống → “Bắt buộc phải chọn”.']),
    ('Hãng sản xuất / % VAT / Loại sản phẩm / Đặc tính', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống', 'Trống → “Bắt buộc phải chọn”.'),
    ('Tính chất / Nhóm chức năng / Nhóm sản phẩm', 'Textbox', 'Disable', '–', 'Có', 'Trống', [
        '- Placeholder “Tự hiện theo Loại sản phẩm”.',
        '- Chưa chọn Loại sản phẩm → “Chưa có tính chất — chọn Loại sản phẩm” / “Chưa có nhóm chức năng — chọn Loại sản phẩm” / '
        '“Chưa có nhóm sản phẩm — chọn Loại sản phẩm”.']),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
    ('Đặc điểm / Thông số kỹ thuật', 'Textarea', 'Enable', 'Văn bản định dạng', 'Không', 'Trống', 'Trình soạn thảo có định dạng.'),
    ('Nút Lưu / Lưu và tiếp tục / Đóng', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Lưu: tạo hàng tạm + đóng.', '- Lưu và tiếp tục: tạo + form trống (không có khi Sửa).', '- Khoá trong lúc đang lưu.']),
])
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu / Lưu và tiếp tục', 'Click',
     'During:\n– Kiểm đồng thời 9 ô bắt buộc + 3 ô cây phân loại; lỗi → chữ đỏ dưới ô + “Vui lòng kiểm tra lại dữ liệu nhập”.\n'
     '– Máy chủ kiểm lại; lỗi riêng ô → chữ đỏ dưới ô.\n'
     'After:\n– Tạo hàng tạm trạng thái Hàng tạm tại công ty đang làm việc; dòng BOM / báo giá cùng gốc được gắn mã mới.\n'
     '– Thông báo “Đã thêm hàng tạm <mã> vào phiếu”; hàng vào bảng YCHG.'),
    ('Bấm Lưu khi Sửa', 'Click', 'After:\n– “Đã lưu hàng tạm” hoặc “Đã lưu — hàng trở về "Hàng tạm" (chờ PTKD duyệt lại)”; dòng trên phiếu cập nhật (có thể đổi nhóm).'),
])

# ------------------------------------------------------------------ 2.7
d.h3('2.7 Sửa YCHG')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Sửa YCHG', 'crud', actor=A_LAP, caption='Biểu đồ Use Case — FR-07 Sửa YCHG')
d.p('2.7.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Sửa yêu cầu hỏi giá',
    mota='Người lập sửa Ghi chú và danh sách hàng của phiếu Đang tạo hoặc Không duyệt (PTKD đã từ chối), rồi Lưu nháp hoặc '
         'Lưu và gửi duyệt lại.',
    tacnhan=A_LAP,
    dieukien='Người dùng là người lập; phiếu Đang tạo hoặc Không duyệt; đang ở đúng công ty phiếu.',
    chinh='1. Bấm Sửa ở danh sách hoặc ở chân màn Chi tiết.\n2. Form nạp phiếu: Ghi chú + hàng theo nhóm (dữ liệu hàng mới nhất).\n'
          '3. Thêm / bỏ hàng, sửa ghi chú.\n4. Lưu nháp hoặc Lưu và gửi duyệt như mục 2.4.\n5. Về danh sách YCHG.',
    phu='• Người khác / phiếu đã gửi mở thẳng màn Sửa → tự chuyển sang màn Chi tiết (phiếu nhìn thấy được) hoặc trang “' +
        MSG_404PAGE + '” (phiếu không nhìn thấy).\n'
        '• Phiếu vừa bị đổi trạng thái (gửi ở tab khác) mà bấm Lưu → “' + MSG_CONFLICT + '”.\n'
        '• Gửi lại phiếu Không duyệt: xoá người / thời điểm / ghi chú PTKD cũ ở phần đầu (lịch sử vẫn giữ); nhóm gom lại từ đầu.\n'
        '• Form Sửa KHÔNG hiện lý do PTKD từ chối — người lập xem lý do ở màn Chi tiết / thông báo.',
    dacbiet='Mỗi lần lưu, hệ thống xoá và gom lại toàn bộ nhóm theo hàng hiện có.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('06-dong-dang-tao.png'),
         shot_caption='Dòng phiếu của người lập có nút Sửa / Xóa (minh hoạ — 1 dòng được đánh dấu Đang tạo trên trình duyệt)')
d.layout(menu=MENU + ' => Sửa', shot=shot('34-sua.png'),
         shot_caption='Form Sửa phiếu Không duyệt (minh hoạ — PYCHG-04282 được giả làm phiếu Không duyệt của người dùng)')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–', 'Sửa yêu cầu hỏi giá: <số phiếu>', '–'),
    ('Số phiếu / Công ty / Người tạo', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu', 'Không đổi được.'),
    ('Trạng thái', 'Badge', 'Read-only', '–', '–', 'Theo dữ liệu', 'Đang tạo (xám) / Không duyệt (đỏ).'),
    ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Theo dữ liệu', '> 255 → “Vui lòng nhập tối đa 255 ký tự.”'),
    ('Bảng hàng + nút Chọn hàng hoá / Thêm hàng tạm', 'Table/Grid', 'Enable', '8 cột', 'Có ≥ 1 hàng', 'Theo dữ liệu',
     'Như mục 2.4; hàng của chính phiếu này không bị coi là “đang được hỏi giá ở phiếu khác”.'),
    ('Nút Lưu nháp / Lưu và gửi duyệt / Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Như mục 2.4.'),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Sửa', 'System',
     'Before:\n– Phiếu công ty khác / nháp của người khác → trang “' + MSG_404PAGE + '”.\n'
     '– Phiếu nhìn thấy nhưng không sửa được → chuyển màn Chi tiết.\nAfter:\n– Nạp dòng hàng mới nhất (trạng thái, giá bán lẻ hiện hành).'),
    ('Bấm Lưu nháp / Lưu và gửi duyệt', 'Click',
     'Before:\n– Máy chủ khoá phiếu; không phải người lập hoặc phiếu không còn Đang tạo / Không duyệt → “' + MSG_CONFLICT + '”.\n'
     'During:\n' + '\n'.join(VALIDATE_SEND) + '\n'
     'After:\n– Như mục 2.4; hàng tạm Không duyệt đưa vào phiếu này → về trạng thái Hàng tạm và được gỡ khỏi YCHG cũ (nhóm cũ hết '
     'hàng thì đóng Huỷ duyệt, lý do “Mọi hàng tạm không được duyệt”, báo người lập phiếu cũ).'),
])

# ------------------------------------------------------------------ 2.8
d.h3('2.8 Xem chi tiết YCHG')
d.p('2.8.1 Giới thiệu')
d.rule_ref(DETAIL_RULE, anchor='detail')
d.intro_table(
    ten='Xem chi tiết yêu cầu hỏi giá',
    mota='Xem phiếu ở chế độ chỉ đọc: thông tin chung, các nhóm (XNK, trạng thái nhóm, số YCTG, lý do đóng / ghi chú XNK), từng '
         'hàng, ghi chú PTKD và lịch sử duyệt. Nút thao tác ở chân màn và trên dòng nhóm hiện theo vai của người xem.',
    tacnhan=A_LAP + '; ' + A_PTKD + '; ' + A_XNK + '; Người dùng đã đăng nhập',
    dieukien='Phiếu thuộc công ty đang làm việc; phiếu đã gửi, hoặc phiếu Đang tạo / Không duyệt của chính người dùng.',
    chinh='1. Bấm số phiếu ở danh sách (hoặc Xử lý, link YCHG ở YCTG / PTG, thông báo [YCHG]).\n'
          '2. Hệ thống hiện phiếu; tiêu đề “Chi tiết yêu cầu hỏi giá: <số phiếu>”.\n'
          '3. Mở từ thông báo / Xử lý nhóm → nhóm liên quan được tô nền xanh và cuộn vào giữa màn.',
    phu='• Phiếu không nhìn thấy (nháp người khác, công ty khác, không tồn tại) → trang “' + MSG_404PAGE + '”.\n'
        '• Lỗi tải khác → “Không tải được yêu cầu hỏi giá, vui lòng thử lại.”\n'
        '• Số YCTG trên nhóm là link chỉ khi người xem có ' + Q2 + ' / ' + Q3 + ' / ' + Q4 + '; không có thì là chữ thường.\n'
        '• Chưa có lịch sử → “Chưa có lịch sử”.')
d.p('2.8.2 Layout màn hình')
d.layout(menu=MENU + ' => Xử lý', shot=shot('21-chi-tiet-cho-ptkd.png'),
         shot_caption='Chi tiết PYCHG-04280 Chờ PTKD duyệt — người có quyền PTKD thấy Duyệt / Từ chối (dữ liệu thật, role tạm 1662)')
d.layout(menu=MENU + ' => Xử lý', shot=shot('25-chi-tiet-da-tinh-gia.png'),
         shot_caption='Chi tiết PYCHG-04283 Đã tính giá: nhóm MULLER, PYCTG-03162, dòng “Giá bán mới áp ngày …” (dữ liệu thật)')
d.layout(menu=MENU + ' => Xử lý', shot=shot('38-phieu-nguoi-khac-404.png'),
         shot_caption='Mở thẳng phiếu Không duyệt của người khác (PYCHG-04277) → trang không tìm thấy (dữ liệu thật)')
d.p('2.8.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Thông tin chung', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Dòng “<người tạo> - <dd/mm/yyyy hh:mm>” góc phải.',
        '- Số phiếu · Công ty · Người tạo · Trạng thái (nhãn màu) · Ghi chú — đều chỉ đọc.']),
    ('Dòng nhóm', 'Label', 'Read-only', '–', 'Theo dữ liệu', [
        '- Số La Mã + “<Thương hiệu> — <Hãng>” + “<n> mã hàng” + “XNK tiếp nhận: <tên>” + nhãn trạng thái nhóm.',
        '- Số YCTG (link khi có quyền xem YCTG) hoặc “chưa có YCTG”.',
        '- Nút XNK (mục 2.13, 2.14) hoặc chữ xám “Chờ <tên> duyệt” / “Chờ <tên> lập YCTG”.',
        '- “Giá bán mới áp ngày <dd/mm/yyyy> · <người tính giá> · <số PTG>” + nút In kết quả khi nhóm đã có giá (mục 2.15).',
        '- “Lý do: <lý do>” khi nhóm bị đóng; “Ghi chú XNK: <ghi chú>” khi XNK duyệt có ghi chú.']),
    ('Dòng hàng', 'Table/Grid', 'Read-only', '7 cột', 'Theo dữ liệu', [
        '- STT · Mã hàng · Tên hàng hoá · Model · ĐVT · Trạng thái hàng · Giá bán lẻ hiện hành (như mục 2.4).',
        '- Hàng tạm không duyệt: chữ mờ, gạch ngang tên, dòng đỏ “Không đi tiếp — lý do: <lý do>”.',
        '- PTKD xem phiếu Chờ PTKD duyệt có hàng tạm: thêm cột Hành động (mục 2.12).']),
    ('Nút Chi tiết kết quả', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Chỉ hiện khi có ít nhất 1 hàng đã có giá bán mới → mục 2.15.'),
    ('Khối Ghi chú duyệt & lịch sử', 'Table/Grid', 'Read-only', '4 cột', 'Theo dữ liệu', [
        '- “Ghi chú PTKD: <ghi chú / lý do từ chối>” khi có.',
        '- Bảng Người thực hiện · Hành động · Nội dung · Thời gian, mới → cũ.',
        '- Hành động: Lập phiếu yêu cầu hỏi giá · PTKD duyệt · PTKD không duyệt · XNK duyệt · XNK không duyệt (= không có giá) · Huỷ duyệt; '
        'phiếu có YCTG / PTG có thêm “Lập yêu cầu tính giá”, “Duyệt tính giá”…; nội dung nhóm ghi “Nhóm <TH> — <Hãng>. <ghi chú>”.']),
    ('Chân màn', 'Button', 'Enable / Ẩn', '–', 'Theo cờ quyền', [
        '- Sửa, Xóa: người lập, phiếu Đang tạo / Không duyệt.',
        '- Duyệt, Từ chối: người có quyền ' + Q1 + ', phiếu Chờ PTKD duyệt.',
        '- In: luôn hiện. Quay lại: về danh sách.']),
], required=False)
d.p('2.8.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Chi tiết', 'System',
     'Before:\n– Không kiểm quyền xem; phiếu không nhìn thấy → trang “' + MSG_404PAGE + '”.\n'
     'During:\n– Tính cờ nút theo người xem: người lập (Sửa / Xóa), ' + Q1 + ' (Duyệt / Từ chối), XNK phân công + ' + Q2 +
     ' (nút nhóm), quyền xem YCTG (link YCTG).\n'
     'After:\n– Có tham số nhóm → tô + cuộn tới nhóm; có tham số xem kết quả → bật Chi tiết kết quả.'),
    ('Bấm số YCTG', 'Click', 'After:\n– Mở màn Chi tiết YCTG (chỉ khi là link).'),
])

# ------------------------------------------------------------------ 2.9
d.h3('2.9 Xoá YCHG')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Xoá YCHG', 'action', actor=A_LAP, caption='Biểu đồ Use Case — FR-09 Xoá YCHG')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xoá. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu hỏi giá tại phần mô tả chi tiết.',
           anchor='delete')
d.intro_table(
    ten='Xoá yêu cầu hỏi giá',
    mota='Người lập xoá hẳn phiếu Đang tạo hoặc Không duyệt (kèm dòng hàng, nhóm, lịch sử của phiếu).',
    tacnhan=A_LAP,
    dieukien='Người lập; phiếu Đang tạo / Không duyệt.',
    chinh='1. Bấm Xóa ở danh sách hoặc chân màn Chi tiết.\n2. Hộp “Xác nhận xóa”.\n3. Bấm Xóa.\n'
          '4. Thông báo “Đã xoá yêu cầu hỏi giá”; danh sách tải lại / về danh sách.',
    phu='• Bấm Hủy / ✕ → không xoá.\n• Phiếu vừa được gửi ở nơi khác → “' + MSG_CONFLICT + '”, màn Chi tiết tải lại.\n'
        '• Trạng thái hàng không đổi (phiếu nháp chưa đổi trạng thái hàng; phiếu Không duyệt đã trả hàng về Đang nhập thông tin '
        'lúc PTKD từ chối).',
    dacbiet='Xoá cứng, không hoàn tác; số phiếu đã dùng không cấp lại.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', shot=shot('07-xac-nhan-xoa.png'),
         shot_caption='Hộp Xác nhận xóa (minh hoạ — dòng được đánh dấu Đang tạo trên trình duyệt; bấm Hủy, không xoá)')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xóa', 'Icon Button', 'Enable / Ẩn', 'Ẩn khi không phải người lập', 'Thùng rác đỏ ở danh sách; nút đỏ “Xóa” ở chân màn Chi tiết.'),
    ('Hộp xác nhận', 'Modal', 'Hiển thị', 'Ẩn',
     ['- Tiêu đề “Xác nhận xóa”.', '- “Xóa yêu cầu hỏi giá <số phiếu>? Thao tác không hoàn tác được.”', '- Nút đỏ “Xóa” / “Hủy”.']),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     ['- Thành công: “Đã xoá yêu cầu hỏi giá”.', '- Lỗi: câu của máy chủ (vd “' + MSG_CONFLICT + '”) hoặc “Xóa thất bại”.']),
], required=False, scope=False)
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xóa trong hộp xác nhận', 'Click',
     'Before:\n– Phiếu không nhìn thấy → “' + MSG_NOTFOUND + '”.\n– Không phải người lập / không còn Đang tạo, Không duyệt → “' +
     MSG_CONFLICT + '”.\nAfter:\n– Xoá dòng hàng, nhóm, lịch sử, phiếu.\n– Thông báo “Đã xoá yêu cầu hỏi giá”, tải lại danh sách.'),
])

# ------------------------------------------------------------------ 2.10
PTKD_APPROVE_AFTER = [
    '– Phiếu → Đang hỏi giá; ghi người duyệt, thời điểm, ghi chú PTKD.',
    '– Mỗi nhóm → Chờ XNK duyệt, ghi XNK phân công hiện hành lúc duyệt.',
    '– Nhóm mà mọi hàng là hàng tạm Không duyệt → đóng Huỷ duyệt, lý do “Mọi hàng tạm không được duyệt”, báo người lập.',
    '– Hàng tạm đã Đồng ý → Chờ tính giá bán; hàng tạm Không duyệt giữ nguyên, nằm lại phiếu.',
    '– Ghi lịch sử “PTKD duyệt” (nội dung = ghi chú).',
    '– Mỗi nhóm gửi “[YCHG] Chờ duyệt: <số phiếu>. Nhóm: <TH> — <Hãng>” tới XNK của nhóm.',
]
d.h3('2.10 PTKD duyệt phiếu')
d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'PTKD duyệt phiếu', 'action', actor=A_PTKD, caption='Biểu đồ Use Case — FR-10 PTKD duyệt phiếu')
d.p('2.10.2 Giới thiệu')
d.rule_ref(NOTICE_RULE, anchor='notice')
d.intro_table(
    ten='PTKD duyệt yêu cầu hỏi giá',
    mota='Người có quyền ' + Q1 + ' duyệt CẢ phiếu Chờ PTKD duyệt (không theo nhóm, không xét phân công hãng); các nhóm chuyển '
         'tới XNK phụ trách.',
    tacnhan=A_PTKD,
    dieukien='Có quyền ' + Q1 + ' tại công ty phiếu; phiếu Chờ PTKD duyệt; mọi hàng tạm đã có quyết định.',
    chinh='1. Mở Chi tiết (thông báo “[YCHG] Chờ duyệt”, nút Xử lý hoặc số phiếu).\n2. Bấm Duyệt ở chân màn.\n'
          '3. Popup “Duyệt yêu cầu hỏi giá”: nhập Ghi chú duyệt (tuỳ chọn).\n4. Bấm Duyệt.\n'
          '5. Thông báo “Đã duyệt yêu cầu hỏi giá”; về danh sách.',
    phu='• Còn hàng tạm chưa duyệt → nút Duyệt bị khoá, rê chuột thấy “Còn <n> hàng tạm chưa duyệt”; gọi thẳng thì máy chủ báo '
        'cùng câu.\n'
        '• Phân công XNK của 1 nhóm bị gỡ sau khi gửi → “Nhóm <TH> — <Hãng> chưa có XNK phụ trách tại công ty, chưa duyệt được.”, '
        'không duyệt gì.\n'
        '• Người khác vừa xử lý phiếu → “' + MSG_CONFLICT + '”, màn tải lại.\n'
        '• Bấm Đóng / ✕ → không duyệt.',
    dacbiet='Duyệt xong không đổi được quyết định hàng tạm. Thông báo gửi sau khi ghi xong; lỗi gửi thông báo không làm hỏng thao tác.')
d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xử lý => Duyệt', shot=shot('22-ptkd-duyet.png'),
         shot_caption='Popup Duyệt yêu cầu hỏi giá (dữ liệu thật, role tạm 1662)')
d.layout(menu=MENU + ' => Xử lý => Duyệt', shot=shot('24-ptkd-duyet-thanh-cong.png'),
         shot_caption='Thông báo sau khi duyệt, về danh sách (minh hoạ — lệnh duyệt trả “thành công” trên trình duyệt, không ghi DB)')
d.layout(menu=MENU + ' => Xử lý => Duyệt', shot=shot('35-ptkd-con-hang-tam.png'),
         shot_caption='Phiếu còn 1 hàng tạm chưa duyệt: nút Duyệt khoá, tooltip “Còn 1 hàng tạm chưa duyệt” (minh hoạ)')
d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Duyệt (chân màn)', 'Button', 'Enable / Disable / Ẩn', '–', '–', 'Ẩn khi thiếu quyền', [
        '- Nút xanh, dấu tích; chỉ hiện với ' + Q1 + ' + phiếu Chờ PTKD duyệt.',
        '- Khoá khi còn hàng tạm chưa duyệt; tooltip “Còn <n> hàng tạm chưa duyệt”.',
        '- Phiếu có hàng tạm: cạnh nút có icon thông tin.',
        '- Icon ⓘ: “' + INFO_PTKD + '”']),
    ('Popup – tiêu đề + câu dẫn', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', [
        '- “Duyệt yêu cầu hỏi giá”.',
        '- “<số phiếu> — <m> nhóm sẽ chuyển tới XNK phụ trách”; có hàng tạm thêm “; hàng tạm đã duyệt sang "Chờ tính giá bán", '
        'hàng tạm không duyệt giữ nguyên (không gửi XNK)”.']),
    ('Ghi chú duyệt', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     ['- Placeholder “Nhập ghi chú duyệt”.', '- > 255 → “Vui lòng nhập tối đa 255 ký tự.”']),
    ('Nút Duyệt / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Duyệt: gửi. Đóng: đóng popup, không duyệt.'),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     ['- “Đã duyệt yêu cầu hỏi giá”.', '- Lỗi nhóm thiếu XNK / còn hàng tạm: chữ đỏ dưới ô trong popup, popup giữ nguyên.']),
])
d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Duyệt ở popup', 'Click',
     'Before:\n– Kiểm quyền ' + Q1 + ' tại công ty đang làm việc; không có → “' + MSG_NOPERM + '”.\n'
     '– Phiếu không nhìn thấy → “' + MSG_NOTFOUND + '”; không còn Chờ PTKD duyệt → “' + MSG_CONFLICT + '”.\n'
     'During:\n– Ghi chú > 255 → “Vui lòng nhập tối đa 255 ký tự.”\n– Còn hàng tạm chưa quyết định → “Còn <n> hàng tạm chưa duyệt”.\n'
     '– Tra lại XNK phân công từng nhóm; thiếu → “Nhóm <TH> — <Hãng> chưa có XNK phụ trách tại công ty, chưa duyệt được.”\n'
     'After:\n' + '\n'.join(PTKD_APPROVE_AFTER) + '\n– Thông báo “Đã duyệt yêu cầu hỏi giá”, về danh sách.'),
])

# ------------------------------------------------------------------ 2.11
d.h3('2.11 PTKD từ chối phiếu')
d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'PTKD từ chối phiếu', 'action', actor=A_PTKD, caption='Biểu đồ Use Case — FR-11 PTKD từ chối phiếu')
d.p('2.11.2 Giới thiệu')
d.rule_ref(NOTICE_RULE, anchor='notice')
d.intro_table(
    ten='PTKD từ chối yêu cầu hỏi giá',
    mota='Trả cả phiếu về người lập kèm lý do bắt buộc; phiếu chuyển Không duyệt, người lập sửa và gửi lại được.',
    tacnhan=A_PTKD,
    dieukien='Có quyền ' + Q1 + ' tại công ty phiếu; phiếu Chờ PTKD duyệt.',
    chinh='1. Ở Chi tiết, bấm Từ chối.\n2. Popup “Từ chối yêu cầu hỏi giá”: nhập Lý do từ chối.\n3. Bấm Từ chối.\n'
          '4. Thông báo “Đã từ chối yêu cầu hỏi giá”; về danh sách.',
    phu='• Lý do trống → “' + MSG_REQ + '”, popup không đóng.\n• Lý do > 255 → “Vui lòng nhập tối đa 255 ký tự.”\n'
        '• Người khác vừa xử lý → “' + MSG_CONFLICT + '”.')
d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xử lý => Từ chối', shot=shot('23-ptkd-tu-choi-thieu-ly-do.png'),
         shot_caption='Popup Từ chối khi chưa nhập lý do: “Bắt buộc phải nhập” (dữ liệu thật, role tạm 1662, không gửi)')
d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Từ chối (chân màn)', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi thiếu quyền', 'Nút đỏ, dấu ✕ tròn; điều kiện như nút Duyệt.'),
    ('Popup – câu dẫn', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', [
        '- “<số phiếu> — hàng đang nhập thông tin sẽ trở về "Đang nhập thông tin"”.',
        '- Có hàng tạm thêm “; hàng tạm đã duyệt trở về "Hàng tạm", hàng tạm không duyệt giữ nguyên”.']),
    ('Lý do từ chối', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     ['- Nhãn có dấu *; placeholder “Nhập lý do từ chối”.', '- Trống → “' + MSG_REQ + '”; > 255 → “Vui lòng nhập tối đa 255 ký tự.”', '- Cắt khoảng trắng đầu / cuối.']),
    ('Nút Từ chối / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Từ chối (đỏ): gửi. Đóng: không gửi.'),
])
d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Từ chối ở popup', 'Click',
     'Before:\n– Kiểm quyền ' + Q1 + '; không có → “' + MSG_NOPERM + '”.\n– Phiếu không còn Chờ PTKD duyệt → “' + MSG_CONFLICT + '”.\n'
     'During:\n– Lý do trống → “' + MSG_REQ + '”; > 255 → “Vui lòng nhập tối đa 255 ký tự.”\n'
     'After:\n– Phiếu → Không duyệt; ghi người, thời điểm, lý do (hiện “Ghi chú PTKD”).\n'
     '– Hàng Chờ tính giá bán / Đang tính giá của phiếu → Đang nhập thông tin; hàng tạm Đồng ý → Hàng tạm; hàng Đang kinh doanh giữ nguyên.\n'
     '– Ghi lịch sử “PTKD không duyệt”.\n– Gửi “[YCHG] Từ chối: <số phiếu>. Lý do: <lý do>” tới người lập.\n'
     '– Thông báo “Đã từ chối yêu cầu hỏi giá”, về danh sách.'),
])

# ------------------------------------------------------------------ 2.12
d.h3('2.12 PTKD duyệt hàng tạm')
d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'PTKD duyệt hàng tạm', 'action', actor=A_PTKD, caption='Biểu đồ Use Case — FR-12 PTKD duyệt hàng tạm')
d.p('2.12.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='PTKD duyệt từng hàng tạm',
    mota='Với phiếu Chờ PTKD duyệt có hàng tạm, PTKD mở form Duyệt hàng tạm (khuôn form hàng hoá) để kiểm tra, bổ sung thông '
         'tin và khai tab Quản trị của công ty phiếu, rồi Đồng ý hoặc Không duyệt TỪNG hàng trước khi duyệt phiếu.',
    tacnhan=A_PTKD,
    dieukien='Có quyền ' + Q1 + ' tại công ty phiếu; phiếu Chờ PTKD duyệt; hàng là hàng tạm của phiếu.',
    chinh='1. Ở Chi tiết, dòng hàng tạm có nút Duyệt (hàng Hàng tạm) hoặc Sửa (hàng đã có quyết định).\n'
          '2. Form “Duyệt hàng tạm: <mã>” mở: tab Thông tin hàng hoá + tab Quản trị hàng hoá.\n'
          '3. Bổ sung thông tin; bấm Đồng ý (hỏi xác nhận) hoặc Không duyệt (popup lý do) hoặc Lưu.\n'
          '4. Về màn Chi tiết YCHG.',
    phu='• Đồng ý → “Hàng tạm đã duyệt”; khi PTKD duyệt phiếu sẽ sang Chờ tính giá bán.\n'
        '• Không duyệt (lý do bắt buộc ≤ 255) → “Hàng tạm không duyệt”, nằm lại phiếu, không đi tiếp.\n'
        '• Lưu hàng đã Đồng ý → về “Hàng tạm” (phải duyệt lại); thông báo “Đã lưu — hàng <mã> trở về "Hàng tạm" (chờ duyệt lại)”.\n'
        '• Đổi ý được tới khi bấm Duyệt phiếu. Thiếu quyền / không phải hàng của phiếu → trang “' + MSG_404PAGE + '”.\n'
        '• Hàng đã Đồng ý ẩn nút Đồng ý; hàng đã Không duyệt ẩn nút Không duyệt và hiện “Đã không duyệt — lý do: <lý do>. Bấm Đồng '
        'ý để duyệt lại.”',
    dacbiet='Thương hiệu / Hãng sản xuất chỉ đọc. Ô bắt buộc báo đồng thời ở cả 2 tab. Chi tiết từng ô của form xem SRS Hàng '
            'hoá nhập thông tin (mục Tạo / Sửa hàng hoá).')
d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Xử lý => Duyệt hàng tạm', shot=shot('35-ptkd-con-hang-tam.png'),
         shot_caption='Dòng hàng tạm trên phiếu Chờ PTKD duyệt: nút Duyệt + icon ⓘ (minh hoạ — hàng thật giả làm hàng tạm)')
d.layout(menu=MENU + ' => Xử lý => Duyệt hàng tạm', shot=shot('36-form-duyet-hang-tam.png'),
         shot_caption='Form Duyệt hàng tạm: Lưu · Đồng ý · Không duyệt · Hủy (minh hoạ — dữ liệu form của hàng thật)')
d.layout(menu=MENU + ' => Xử lý => Duyệt hàng tạm', shot=shot('37-khong-duyet-hang-tam.png'),
         shot_caption='Popup Không duyệt hàng tạm (minh hoạ, không gửi)')
d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Duyệt / Sửa trên dòng hàng tạm', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi thiếu quyền', [
        '- Hàng tạm chưa quyết định: nút xanh “Duyệt”; Icon ⓘ: “' + INFO_TEMP6 + '”',
        '- Hàng đã Đồng ý / Không duyệt: nút “Sửa”; Icon ⓘ: “' + INFO_TEMP78 + '”']),
    ('Đầu form', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
     '“<mã hàng>” + nhãn trạng thái + “thuộc YCHG <số phiếu (link về Chi tiết)>” + “· người lập <tên>”.'),
    ('Dải Quản trị', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
     '“Dữ liệu của công ty <tên> (công ty phiếu <số phiếu>) — mỗi công ty tự khai, không ảnh hưởng công ty khác.”'),
    ('Các ô thông tin hàng', 'Textbox / Dropdown', 'Enable', 'Theo form hàng hoá', 'Theo form hàng hoá', 'Theo dữ liệu',
     'Như form Sửa hàng hoá; Thương hiệu, Hãng sản xuất chỉ đọc; Tiểu mục catalog không bắt buộc.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Icon ⓘ: “' + INFO_SAVE + '”'),
    ('Nút Đồng ý', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', [
        '- Hỏi “Đồng ý hàng tạm <mã>? Hàng chuyển "Hàng tạm đã duyệt" và sang "Chờ tính giá bán" khi duyệt phiếu <số phiếu>.”',
        '- Icon ⓘ: “' + INFO_AGREE + '”']),
    ('Nút Không duyệt', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', [
        '- Popup “Không duyệt hàng tạm”: “<mã> — hàng giữ trong phiếu nhưng không đi tiếp (không gửi XNK)” (+ “. Các thay đổi chưa '
        'lưu trên form sẽ không được lưu.” khi đang sửa dở).',
        '- Ô Lý do không duyệt bắt buộc, ≤ 255 ký tự.',
        '- Icon ⓘ: “' + INFO_REJECT + '”']),
    ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn Chi tiết YCHG (hỏi nếu có thay đổi chưa lưu).'),
])
d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở form', 'System',
     'Before:\n– Phiếu không nhìn thấy → trang không tìm thấy; thiếu ' + Q1 + ' → “' + MSG_NOT_PTKD + '” (trang không tìm thấy); '
     'hàng không thuộc phiếu → “Hàng hoá không thuộc yêu cầu hỏi giá này”.'),
    ('Bấm Đồng ý / Lưu', 'Click',
     'Before:\n– Phiếu không còn Chờ PTKD duyệt / hàng không còn là hàng tạm → “' + MSG_CONFLICT + '”.\n'
     'During:\n– Kiểm đồng thời ô bắt buộc ở 2 tab; lỗi → chữ đỏ + mở tab có lỗi đầu tiên.\n'
     'After:\n– Ghi thông tin chung + tab Quản trị cho công ty phiếu.\n– Đồng ý: → Hàng tạm đã duyệt; “Đã đồng ý hàng tạm <mã>”.\n'
     '– Lưu: giữ trạng thái (hàng đã Đồng ý → về Hàng tạm); “Đã lưu hàng tạm <mã>”.'),
    ('Bấm Không duyệt ở popup', 'Click',
     'During:\n– Lý do trống → “' + MSG_REQ + '”; > 255 → “Vui lòng nhập tối đa 255 ký tự.”\n'
     'After:\n– → Hàng tạm không duyệt; ghi lý do (hiện ở dòng hàng “Không đi tiếp — lý do: …” và màn Hàng tạm).\n'
     '– “Đã không duyệt hàng tạm <mã>”; về Chi tiết YCHG.'),
])

# ------------------------------------------------------------------ 2.13
d.h3('2.13 XNK duyệt nhóm / Lập YCTG')
d.p('2.13.1 Biểu đồ Usecase')
d.uc_figure('FR-13', 'XNK duyệt nhóm / Lập YCTG', 'action', actor=A_XNK, caption='Biểu đồ Use Case — FR-13 XNK duyệt nhóm / Lập YCTG')
d.p('2.13.2 Giới thiệu')
d.rule_ref(NOTICE_RULE, anchor='notice')
d.intro_table(
    ten='XNK duyệt nhóm hàng và lập yêu cầu tính giá',
    mota='XNK đang được phân công phụ trách Thương hiệu × Hãng của nhóm nhận hỏi giá: Duyệt nhóm (ghi chú tuỳ chọn) → nhóm Chờ '
         'lập YCTG; sau đó bấm Lập YCTG để lập Yêu cầu tính giá cho nhóm.',
    tacnhan=A_XNK,
    dieukien='Có quyền ' + Q2 + ' tại công ty phiếu VÀ là người mua phân công HIỆN HÀNH của Thương hiệu × Hãng × công ty phiếu; '
             'phiếu Đang hỏi giá; nhóm Chờ XNK duyệt (Duyệt) hoặc Chờ lập YCTG chưa có YCTG (Lập YCTG).',
    chinh='1. Mở thông báo “[YCHG] Chờ duyệt: <số phiếu>. Nhóm: …” (hoặc nút Xử lý nhóm) → Chi tiết cuộn tới nhóm.\n'
          '2. Bấm Duyệt trên dòng nhóm → popup “Duyệt nhóm hàng” → (tuỳ chọn) Ghi chú → Duyệt.\n'
          '3. Thông báo “Đã duyệt nhóm hàng”; nhóm Chờ lập YCTG.\n'
          '4. Bấm Lập YCTG (trên dòng nhóm ở Chi tiết hoặc danh sách) → màn Tạo YCTG của nhóm.',
    phu='• Có quyền ' + Q2 + ' nhưng phân công hãng là người khác → không có nút; gọi thẳng → “' + MSG_NOT_XNK + '”.\n'
        '• Phân công đổi sang người khác sau khi gửi → người mới thấy nút, người cũ mất nút.\n'
        '• Nhóm vừa được xử lý ở nơi khác → “' + MSG_CONFLICT + '”.\n'
        '• Duyệt nhóm KHÔNG gửi thông báo.',
    dacbiet='Lập YCTG chỉ điều hướng sang màn YCTG (đặc tả ở SRS Yêu cầu tính giá); khi YCTG được lưu nhóm chuyển Đang tính giá.')
d.p('2.13.3 Layout màn hình')
d.layout(menu=MENU + ' => Xử lý => Duyệt nhóm', shot=shot('29-xnk-cho-duyet-nhom.png'),
         shot_caption='Nhóm TORIN Chờ XNK duyệt có nút Duyệt / Không có giá (minh hoạ — bật cờ nút trên trình duyệt)')
d.layout(menu=MENU + ' => Xử lý => Duyệt nhóm', shot=shot('30-xnk-duyet-nhom.png'),
         shot_caption='Popup Duyệt nhóm hàng (minh hoạ, không gửi)')
d.layout(menu=MENU + ' => Xử lý => Lập YCTG', shot=shot('32-xnk-cho-lap-yctg.png'),
         shot_caption='Nhóm BESITA Chờ lập YCTG có nút Lập YCTG / Huỷ duyệt (minh hoạ)')
d.p('2.13.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Duyệt (dòng nhóm)', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không phải XNK phân công', 'Nhóm Chờ XNK duyệt.'),
    ('Popup Duyệt nhóm hàng', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', '“<số phiếu> — nhóm <TH> — <Hãng>”.'),
    ('Ghi chú', 'Textarea', 'Enable', '0–1000 ký tự', 'Không', 'Trống',
     ['- Placeholder “Nhập ghi chú”.', '- > 1000 → “Vui lòng nhập tối đa 1000 ký tự.”', '- Hiện ở Chi tiết: “Ghi chú XNK: <ghi chú>”.']),
    ('Nút Lập YCTG', 'Button / Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
     ['- Dòng nhóm Chi tiết: nút xanh “Lập YCTG”.', '- Danh sách: icon dấu cộng tròn, tooltip “Lập YCTG”.', '- Nhóm Chờ lập YCTG, chưa có YCTG, XNK phân công.']),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '“Đã duyệt nhóm hàng”.'),
])
d.p('2.13.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Duyệt ở popup', 'Click',
     'Before:\n– Thiếu quyền ' + Q2 + ' → “' + MSG_NOPERM + '”.\n– Không phải XNK phân công hiện hành → “' + MSG_NOT_XNK + '”.\n'
     '– Nhóm không thuộc phiếu → “Không tìm thấy nhóm hàng của yêu cầu hỏi giá”; nhóm không còn Chờ XNK duyệt → “' + MSG_CONFLICT + '”.\n'
     'During:\n– Ghi chú > 1000 → “Vui lòng nhập tối đa 1000 ký tự.”\n'
     'After:\n– Nhóm → Chờ lập YCTG; ghi XNK = người duyệt, ghi chú, thời điểm.\n– Lịch sử “XNK duyệt” (“Nhóm <TH> — <Hãng>. <ghi chú>”).\n'
     '– Thông báo “Đã duyệt nhóm hàng”, về danh sách.'),
    ('Bấm Lập YCTG', 'Click', 'After:\n– Mở màn Tạo YCTG của nhóm; Quay lại về đúng nơi đã bấm.'),
])

# ------------------------------------------------------------------ 2.14
d.h3('2.14 XNK không có giá / Huỷ duyệt nhóm')
d.p('2.14.1 Biểu đồ Usecase')
d.uc_figure('FR-14', 'XNK không có giá / Huỷ duyệt', 'action', actor=A_XNK,
            caption='Biểu đồ Use Case — FR-14 XNK không có giá / Huỷ duyệt nhóm')
d.p('2.14.2 Giới thiệu')
d.rule_ref(NOTICE_RULE, anchor='notice')
d.intro_table(
    ten='XNK báo nhóm không có giá / Huỷ duyệt nhóm',
    mota='Đóng 1 nhóm kèm lý do bắt buộc: “Không có giá” khi nhóm Chờ XNK duyệt; “Huỷ duyệt” khi nhóm Chờ lập YCTG mà chưa có '
         'YCTG. Nhóm đã đóng không gửi lại được — muốn hỏi lại thì lập YCHG mới.',
    tacnhan=A_XNK,
    dieukien='Như mục 2.13 (quyền ' + Q2 + ' + phân công hiện hành); phiếu Đang hỏi giá.',
    chinh='1. Bấm Không có giá (nhóm Chờ XNK duyệt) hoặc Huỷ duyệt (nhóm Chờ lập YCTG).\n2. Popup: nhập Lý do (bắt buộc).\n'
          '3. Bấm Không có giá / Huỷ duyệt.\n4. Thông báo “Đã báo nhóm hàng không có giá” / “Đã huỷ duyệt nhóm hàng”; về danh sách.',
    phu='• Lý do trống → “' + MSG_REQ + '”; > 1000 → “Vui lòng nhập tối đa 1000 ký tự.”\n'
        '• Nhóm đã có YCTG → không còn nút Huỷ duyệt; gọi thẳng → “' + MSG_CONFLICT + '”.\n'
        '• Nhóm cuối cùng của phiếu đóng → phiếu Đã tính giá (nếu có nhóm khác đã có giá) hoặc Không có giá.')
d.p('2.14.3 Layout màn hình')
d.layout(menu=MENU + ' => Xử lý => Không có giá', shot=shot('31-xnk-khong-co-gia.png'),
         shot_caption='Popup Nhóm hàng không có giá khi chưa nhập lý do (minh hoạ, không gửi)')
d.layout(menu=MENU + ' => Xử lý => Huỷ duyệt', shot=shot('33-xnk-huy-duyet.png'),
         shot_caption='Popup Huỷ duyệt nhóm hàng (minh hoạ, không gửi)')
d.p('2.14.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Không có giá', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn', 'Nút đỏ, nhóm Chờ XNK duyệt.'),
    ('Nút Huỷ duyệt', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn', 'Nút đỏ, nhóm Chờ lập YCTG chưa có YCTG.'),
    ('Popup – tiêu đề + câu dẫn', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', [
        '- “Nhóm hàng không có giá” / “Huỷ duyệt nhóm hàng”.',
        '- “<số phiếu> — nhóm <TH> — <Hãng> — nhóm sẽ đóng, không gửi lại được”.']),
    ('Lý do / Lý do huỷ duyệt', 'Textarea', 'Enable', '1–1000 ký tự', 'Có', 'Trống',
     ['- Trống → “' + MSG_REQ + '”.', '- > 1000 → “Vui lòng nhập tối đa 1000 ký tự.”', '- Hiện ở Chi tiết: “Lý do: <lý do>”.']),
    ('Nút xác nhận / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '“Không có giá” / “Huỷ duyệt” (đỏ) · “Đóng”.'),
])
d.p('2.14.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Không có giá / Huỷ duyệt ở popup', 'Click',
     'Before:\n– Như mục 2.13 (quyền, phân công, trạng thái nhóm).\n'
     'During:\n– Lý do trống → “' + MSG_REQ + '”; > 1000 → “Vui lòng nhập tối đa 1000 ký tự.”\n'
     'After:\n– Nhóm → Không có giá / Huỷ duyệt; ghi lý do, người, thời điểm đóng.\n'
     '– Hàng của nhóm đang Chờ tính giá bán / Đang tính giá → Đang nhập thông tin (hàng Đang kinh doanh giữ nguyên; hàng tạm không duyệt không đổi).\n'
     '– Mọi nhóm đã đóng → phiếu Đã tính giá (có nhóm có giá) / Không có giá.\n'
     '– Lịch sử “XNK không duyệt” / “Huỷ duyệt”.\n'
     '– Gửi người lập: “[YCHG] Từ chối: <số phiếu>. Nhóm <TH> — <Hãng> không có giá: <lý do>” / “[YCHG] Hủy: <số phiếu>. Nhóm '
     '<TH> — <Hãng>. Lý do: <lý do>”.'),
])

# ------------------------------------------------------------------ 2.15
d.h3('2.15 Xem giá bán mới (Chi tiết kết quả)')
d.p('2.15.1 Giới thiệu')
d.rule_ref(DETAIL_RULE, anchor='detail')
d.intro_table(
    ten='Xem giá bán mới của YCHG',
    mota='Khi nhóm đã được áp giá (Phiếu tính giá duyệt thẳng, hoặc mọi dòng giá được duyệt ở màn Duyệt giá bán), YCHG hiện '
         'giá bán mới ngay dưới từng mã hàng: mỗi ĐVT 1 dòng, 6 loại giá + ĐMGG. Không có màn / menu kết quả riêng.',
    tacnhan=A_LAP + '; Người dùng đã đăng nhập',
    dieukien='Thấy được phiếu (mục 2.8); ít nhất 1 nhóm đã có kết quả tính giá. KHÔNG cần quyền Xem giá vốn.',
    chinh='1. Mở Chi tiết YCHG (thông báo “[YCHG] Đã duyệt …: đã có giá bán mới” tự bật chế độ này).\n'
          '2. Bấm “Chi tiết kết quả” ở khối Hàng hoá hỏi giá.\n'
          '3. Dưới mỗi hàng đã có giá hiện bảng giá mới; bấm ✕ để ẩn riêng 1 hàng, “▸ Hiện giá mới” để hiện lại.\n'
          '4. Bấm “Ẩn chi tiết kết quả” để tắt.',
    phu='• Chưa nhóm nào có giá → không có nút Chi tiết kết quả.\n'
        '• Hàng của nhóm chưa có giá (đang tính, không có giá) → không có bảng giá.\n'
        '• Cột Giá bán lẻ hiện hành vẫn là giá ĐANG áp dụng — có thể khác giá mới nếu sau đó giá được sửa ở màn Cập nhật giá bán.')
d.p('2.15.2 Layout màn hình')
d.layout(menu=MENU + ' => Xử lý => Chi tiết kết quả', shot=shot('26-chi-tiet-ket-qua.png'),
         shot_caption='PYCHG-04283: giá mới MLER-AMAT8574091 (Bộ) — Bán lẻ … Đại lý cấp 3 22,500,000 ĐMGG 5%, TMĐT 29,250,000 (dữ liệu thật)')
d.layout(menu=MENU + ' => Xử lý => Chi tiết kết quả', shot=shot('27-an-gia-moi-dong.png'),
         shot_caption='Ẩn giá mới của 1 hàng: hiện link “▸ Hiện giá mới” (dữ liệu thật)')
d.p('2.15.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Chi tiết kết quả / Ẩn chi tiết kết quả', 'Button', 'Enable / Ẩn', '–', 'Ẩn (mặc định tắt)', [
        '- Chỉ ở màn Chi tiết, chỉ khi có hàng đã có giá mới.',
        '- Mở từ thông báo “đã có giá bán mới” / link “Xem giá bán mới” của PTG → bật sẵn.']),
    ('Dòng “Giá bán mới áp ngày …” (dòng nhóm)', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
     '“Giá bán mới áp ngày <ngày áp> · <người tính giá> · <số PTG>” + nút In kết quả (mục 2.16).'),
    ('Bảng giá mới (dưới mã hàng)', 'Table/Grid', 'Read-only', '8 cột', 'Theo dữ liệu', [
        '- Viền trái xanh lá, nền xanh rất nhạt.',
        '- Cột: ĐVT · Bán lẻ · Theo lô · Đại lý cấp 1 · Đại lý cấp 2 · Đại lý cấp 3 · TMĐT · nút ✕.',
        '- Mỗi ĐVT đã áp giá 1 dòng; ô giá: giá mới (dấu phẩy ngăn nghìn) + dòng phụ “ĐMGG <x>%”.',
        '- Loại giá không có trong kết quả: ô trống.']),
    ('Nút ✕ / link ▸ Hiện giá mới', 'Icon Button', 'Enable', '–', 'Hiển thị',
     ['- ✕ (tooltip “Ẩn giá mới của dòng này”): ẩn bảng của hàng đó.', '- “▸ Hiện giá mới” dưới cột Giá bán lẻ hiện hành: hiện lại.']),
], required=False)
d.p('2.15.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở Chi tiết', 'System',
     'During:\n– Lấy kết quả tính giá của YCTG từng nhóm: CHỈ giá bán + ĐMGG (không giá NCC, chi phí, giá vốn, giá nhập kho).\n'
     'After:\n– Có ít nhất 1 hàng có kết quả → hiện nút Chi tiết kết quả.'),
    ('Bấm Chi tiết kết quả', 'Click', 'After:\n– Bật / tắt bảng giá mới của mọi hàng; đặt lại các hàng đã ẩn.'),
])

# ------------------------------------------------------------------ 2.16
d.h3('2.16 In phiếu / In kết quả')
d.p('2.16.1 Biểu đồ Usecase')
d.uc_figure('FR-16', 'In phiếu / In kết quả', 'io', actor=A_LAP, caption='Biểu đồ Use Case — FR-16 In phiếu / In kết quả')
d.p('2.16.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột (phần In). Chỉ bổ sung các quy tắc riêng của màn Yêu cầu hỏi giá tại phần mô tả '
           'chi tiết.', anchor='excel')
d.intro_table(
    ten='In phiếu yêu cầu hỏi giá / In kết quả tính giá',
    mota='Xem trước bản in rồi in: “PHIẾU YÊU CẦU HỎI GIÁ” (theo nhóm, có Giá bán lẻ hiện hành) và “KẾT QUẢ TÍNH GIÁ” của 1 nhóm '
         '(6 loại giá × ĐVT + ĐMGG). Letterhead theo công ty phiếu.',
    tacnhan=A_LAP + '; Người dùng đã đăng nhập',
    dieukien='Thấy được phiếu. In kết quả: nhóm đã có kết quả. Không cần quyền.',
    chinh='1. Bấm In (hành động dòng ở danh sách / chân màn Chi tiết) hoặc In kết quả (dòng nhóm).\n'
          '2. Popup “Xem trước yêu cầu hỏi giá <số phiếu>” / “Xem trước kết quả tính giá <số PTG>” hiện bản in.\n'
          '3. Bấm In trong popup → hộp thoại in của trình duyệt.',
    phu='• Phiếu không nhìn thấy → “' + MSG_NOTFOUND + '”.\n• PTG chưa có kết quả → “Phiếu tính giá chưa có kết quả”.\n'
        '• Bấm ✕ → đóng popup.')
d.p('2.16.3 Layout màn hình')
d.layout(menu=MENU + ' => In', shot=shot('05-in-phieu.png'),
         shot_caption='Xem trước PHIẾU YÊU CẦU HỎI GIÁ PYCHG-04283 (dữ liệu thật; máy dev không có letterhead do cấu hình môi trường)')
d.layout(menu=MENU + ' => Xử lý => In kết quả', shot=shot('28-in-ket-qua.png'),
         shot_caption='Xem trước KẾT QUẢ TÍNH GIÁ PTG-03178 (dữ liệu thật)')
d.p('2.16.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In / In kết quả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'In: luôn hiện. In kết quả: dòng nhóm đã có giá.'),
    ('Bản in phiếu', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', [
        '- Tiêu đề “PHIẾU YÊU CẦU HỎI GIÁ”, Số phiếu, Ngày tạo; khối Người lập · Trạng thái · Ghi chú.',
        '- Bảng STT · Mã hàng · Tên hàng hoá · Model · ĐVT · Giá bán lẻ hiện hành; dòng nhóm “<La Mã> <TH> — <Hãng> · XNK: <tên> · <trạng thái nhóm>”.',
        '- Hàng chưa có giá: “—”. Khối ký Người lập / PTKD duyệt.']),
    ('Bản in kết quả', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', [
        '- Tiêu đề “KẾT QUẢ TÍNH GIÁ”; khối Phiếu tính giá · Yêu cầu tính giá · Yêu cầu hỏi giá · Thương hiệu – Hãng · Người hỏi giá · Ngày áp giá.',
        '- Bảng STT · Hàng hoá · ĐVT · Loại giá · Giá mới · ĐMGG (%) — 6 dòng loại giá mỗi ĐVT (Bán lẻ, Giá bán theo lô, Đại lý cấp 1, 2, 3, Thương mại điện tử).',
        '- Chỉ giá bán. Khối ký Người tính giá.']),
    ('Popup xem trước', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', 'Nút In (mở hộp thoại in) và ✕.'),
])
d.p('2.16.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In / In kết quả', 'Click',
     'Before:\n– Kiểm phiếu nhìn thấy được (không cần quyền).\nAfter:\n– Dựng bản in ở máy chủ, hiện trong popup xem trước.'),
    ('Bấm In trong popup', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt.'),
])

# ========================================================= PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('chỉ ghi các quy tắc đặc thù của Yêu cầu hỏi giá; quy tắc dùng chung không nhắc lại.',
           anchor='list', head='Quy tắc áp dụng', lead='Ngoài SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi = công ty phiếu',
     ['– Phiếu thuộc công ty đang làm việc của người lập; công ty lấy từ phiên làm việc, không nhận từ màn hình.',
      '– Phiếu công ty khác: không hiện, không mở, không thao tác được — hệ thống báo “' + MSG_NOTFOUND + '” (không lộ là có phiếu).',
      '– Mọi quyền (Q1, Q2, …) xét tại công ty phiếu; super admin không được miễn.'], ['Mọi chức năng']),
    ('BR-02', 'Ai thấy phiếu — không cần quyền xem',
     ['– Phiếu Đang tạo / Không duyệt: chỉ người lập thấy (danh sách, chi tiết, in).',
      '– Phiếu đã gửi (Chờ PTKD duyệt, Đang hỏi giá, Đã tính giá, Không có giá, Huỷ duyệt): mọi nhân viên của công ty thấy.',
      '– Không phân quyền theo phòng ban / cấp quản lý.'], ['Xem danh sách', 'Xem chi tiết', 'In']),
    ('BR-03', 'Lập / sửa / xoá',
     ['– Không cần quyền; chỉ người lập sửa / xoá; chỉ phiếu Đang tạo hoặc Không duyệt.',
      '– Trạng thái khác / người khác → “' + MSG_CONFLICT + '”; mở thẳng màn Sửa → chuyển màn Chi tiết.'],
     ['Tạo', 'Sửa', 'Xoá']),
    ('BR-04', 'Hàng được hỏi giá',
     ['– Chọn được: hàng Đang nhập thông tin / Đang kinh doanh TẠI công ty phiếu; hàng tạm (Hàng tạm, Hàng tạm không duyệt) chưa '
      'nằm trong YCHG mở khác (kể cả nháp).',
      '– Không chọn được (lý do nguyên văn): “Hàng đang được hỏi giá ở <mã>” (Chờ tính giá bán / Đang tính giá) · “Hàng ngừng kinh '
      'doanh tại công ty” · “Hàng chưa dùng ở công ty” · “Hàng hoá đã bị xoá” · “Hàng tạm đã được duyệt, đang chờ duyệt phiếu yêu '
      'cầu hỏi giá” · “Hàng tạm đang nằm trong yêu cầu hỏi giá <mã>”.',
      '– Kiểm lại ở máy chủ mỗi lần lưu.'], ['Tạo', 'Sửa', 'Chọn hàng hoá']),
    ('BR-05', 'Cảnh báo đang hỏi giá ở phiếu khác',
     ['– Hàng Đang kinh doanh nằm trong YCHG khác đang mở (Chờ PTKD duyệt / Đang hỏi giá, nhóm chưa đóng) → “Đang được hỏi giá ở '
      '<mã phiếu>”, KHÔNG chặn (giống ERP).'], ['Tạo', 'Sửa', 'Chọn hàng hoá', 'Xem chi tiết']),
    ('BR-06', 'Gom nhóm Thương hiệu × Hãng',
     ['– Mỗi cặp Thương hiệu × Hãng sản xuất của hàng = 1 nhóm, sắp theo tên A → Z, đánh La Mã; gom lại mỗi lần lưu.',
      '– Không chọn ĐVT: phiếu hỏi giá cho mọi ĐVT đã khai (YCTG / PTG tự bung đủ ĐVT).'], ['Tạo', 'Sửa']),
    ('BR-07', 'Gửi phải đủ XNK phụ trách',
     ['– Mỗi nhóm phải có người mua phân công hiện hành của (thương hiệu × hãng × công ty phiếu); thiếu → “' + MSG_NO_XNK +
      '”, không gửi nhóm nào.',
      '– Phải có ≥ 1 hàng (“' + MSG_NO_ROW + '”); Ghi chú ≤ 255 ký tự. Lưu nháp không kiểm XNK.',
      '– PTKD duyệt tra lại phân công; phân công bị gỡ → “Nhóm … chưa có XNK phụ trách tại công ty, chưa duyệt được.”'],
     ['Tạo', 'Sửa', 'PTKD duyệt']),
    ('BR-08', 'GIÁ — Trạng thái hàng × công ty theo luồng',
     ['– Gửi phiếu: Đang nhập thông tin → Chờ tính giá bán. Hàng Đang kinh doanh GIỮ Đang kinh doanh suốt luồng.',
      '– PTKD từ chối / XNK Không có giá / Huỷ duyệt: Chờ tính giá bán / Đang tính giá → Đang nhập thông tin.',
      '– Phiếu tính giá lưu: Chờ tính giá bán → Đang tính giá; mọi ĐVT của hàng được áp giá → Đang kinh doanh.',
      '– Chỉ đổi trạng thái tại công ty phiếu.'], ['Gửi duyệt', 'PTKD từ chối', 'XNK đóng nhóm', 'Xem giá bán mới']),
    ('BR-09', 'GIÁ — YCHG không đổi giá; Giá bán lẻ hiện hành',
     ['– Lập / gửi / duyệt YCHG KHÔNG ghi giá nào.',
      '– Cột Giá bán lẻ hiện hành = giá Bán lẻ đang áp dụng của ĐVT cơ bản tại công ty phiếu, đọc lúc mở màn (không phải giá lúc lập); '
      'chưa có dòng giá → trống (bản in “—”).',
      '– Hàng chỉ nằm trong YCHG vẫn sửa giá được ở màn Cập nhật giá bán; chỉ bị chặn khi giá đang chờ duyệt ở Phiếu tính giá.'],
     ['Tạo', 'Sửa', 'Xem chi tiết', 'In']),
    ('BR-10', 'GIÁ — Giá bán mới (kết quả tính giá)',
     ['– Sinh khi nhóm được áp giá: PTG Lưu & duyệt ở công ty tắt duyệt giá, hoặc mọi dòng giá của PTG được Duyệt ở màn Duyệt giá bán.',
      '– Là bản chụp lúc áp: 6 loại giá (Bán lẻ, Theo lô, Đại lý cấp 1, 2, 3, TMĐT) × mọi ĐVT + ĐMGG; vd PYCHG-04283: Bán lẻ '
      '22,500,000 ĐMGG 5%, TMĐT 29,250,000 (= Bán lẻ × hệ số TMĐT 1,3 của công ty).',
      '– CHỈ giá bán: không giá NCC, chi phí, giá nhập kho, giá vốn ⇒ ai thấy phiếu đều xem / in được, không cần quyền Xem giá vốn.',
      '– Giá đang áp dụng có thể khác bản chụp nếu sau đó được sửa ở màn Cập nhật giá bán.'],
     ['Xem giá bán mới', 'In kết quả']),
    ('BR-11', 'GIÁ — Trạng thái nhóm và phiếu',
     ['– Nhóm: (chưa qua PTKD) → Chờ XNK duyệt → Chờ lập YCTG → Đang tính giá (có YCTG) → Đã tính giá (giá áp); đóng: Không có giá / Huỷ duyệt.',
      '– Phiếu: Đang tạo → Chờ PTKD duyệt → Đang hỏi giá → (mọi nhóm đóng) Đã tính giá nếu ≥ 1 nhóm có giá, ngược lại Không có giá; '
      'Chờ PTKD duyệt → Không duyệt → sửa, gửi lại.',
      '– Nhóm đã đóng không mở lại; hỏi lại thì lập YCHG mới.',
      '– Phiếu cũ ERP đang dở hiện “Đang hỏi giá”; phiếu cũ huỷ hiện “Huỷ duyệt”.'], ['Mọi chức năng']),
    ('BR-12', 'PTKD duyệt cả phiếu',
     ['– Quyền ' + Q1 + ' tại công ty phiếu; duyệt MỌI phiếu Chờ PTKD duyệt trong công ty, không theo nhóm / phân công hãng.',
      '– Ghi chú tuỳ chọn ≤ 255; còn hàng tạm chưa quyết định → “Còn <n> hàng tạm chưa duyệt”.',
      '– Nhóm toàn hàng tạm Không duyệt → đóng Huỷ duyệt “Mọi hàng tạm không được duyệt”.'], ['PTKD duyệt']),
    ('BR-13', 'PTKD từ chối',
     ['– Lý do bắt buộc ≤ 255; phiếu Không duyệt; hàng mới về Đang nhập thông tin; hàng tạm Đồng ý về Hàng tạm.',
      '– Gửi lại: xoá người / thời điểm / ghi chú PTKD ở phần đầu, lịch sử giữ.'], ['PTKD từ chối', 'Sửa']),
    ('BR-14', 'XNK xử lý theo phân công hiện hành',
     ['– Cần quyền ' + Q2 + ' VÀ là người mua đang được phân công của thương hiệu × hãng × công ty phiếu (theo màn Phân công nhân viên phụ trách).',
      '– Không phải → không có nút; gọi thẳng → “' + MSG_NOT_XNK + '”. Đổi phân công thì người mới xử lý.',
      '– Duyệt nhóm: ghi chú ≤ 1000. Không có giá / Huỷ duyệt: lý do bắt buộc ≤ 1000. Huỷ duyệt chỉ khi chưa có YCTG.'],
     ['XNK duyệt nhóm', 'XNK đóng nhóm', 'Lập YCTG']),
    ('BR-15', 'XNK hiển thị',
     ['– Nhóm chưa có YCTG (chưa qua PTKD, Chờ XNK duyệt, Chờ lập YCTG): hiện người phân công HIỆN HÀNH.',
      '– Nhóm đã có YCTG / đã đóng: hiện người đã ghi trên nhóm. Ô lọc XNK tiếp nhận lọc theo người đã ghi.'],
     ['Xem danh sách', 'Xem chi tiết', 'Tìm kiếm và lọc']),
    ('BR-16', 'Hàng tạm',
     ['– Tạo trong popup Thêm hàng tạm (9 ô bắt buộc + cây phân loại theo Loại sản phẩm); hàng tạm chỉ nằm trong 1 YCHG mở.',
      '– PTKD duyệt từng hàng: Đồng ý (Hàng tạm đã duyệt) / Không duyệt (lý do ≤ 255, nằm lại phiếu) — đổi ý được tới khi duyệt phiếu.',
      '– Sửa hàng tạm đã có quyết định → về Hàng tạm. Sửa hàng tạm người khác tạo cần quyền ' + Q5 + '.',
      '– Hàng tạm Không duyệt đưa sang YCHG mới → gỡ khỏi YCHG cũ.'], ['Thêm / sửa hàng tạm', 'PTKD duyệt hàng tạm']),
    ('BR-17', 'Thao tác đồng thời',
     ['– Mọi thao tác đổi trạng thái khoá phiếu / nhóm rồi kiểm lại trạng thái trong 1 giao dịch.',
      '– 2 người cùng xử lý: 1 người thành công, người sau nhận “' + MSG_CONFLICT + '” (màn Chi tiết tải lại).',
      '– 2 phiếu gửi cùng 1 hàng Đang nhập thông tin: chỉ 1 phiếu gửi được.'], ['Gửi', 'PTKD', 'XNK', 'Xoá']),
    ('BR-18', 'Thông báo [YCHG]',
     ['– Gửi phiếu → mọi người có ' + Q1 + ' tại công ty: “[YCHG] Chờ duyệt: <số phiếu>. Người lập: <tên>”.',
      '– PTKD duyệt → XNK từng nhóm: “[YCHG] Chờ duyệt: <số phiếu>. Nhóm: <TH> — <Hãng>” (mở Chi tiết, cuộn tới nhóm).',
      '– PTKD từ chối → người lập: “[YCHG] Từ chối: <số phiếu>. Lý do: <lý do>”.',
      '– XNK không có giá → người lập: “[YCHG] Từ chối: <số phiếu>. Nhóm <…> không có giá: <lý do>”; Huỷ duyệt: “[YCHG] Hủy: <số phiếu>. Nhóm <…>. Lý do: <lý do>”.',
      '– Nhóm được áp giá → người lập YCHG + XNK lập YCTG: “[YCHG] Đã duyệt: <số phiếu>. Nhóm <…>: đã có giá bán mới” (nhóm cuối: '
      '“Đã tính giá xong <a>/<b> nhóm”), mở Chi tiết bật sẵn giá mới.',
      '– XNK duyệt nhóm không báo. Tên ≤ 50, cả câu ≤ 120 ký tự; lỗi gửi không làm hỏng thao tác; chỉ trong công ty phiếu.'],
     ['Gửi', 'PTKD', 'XNK', 'Xem giá bán mới']),
    ('BR-19', 'Lịch sử phiếu',
     ['– Ghi: Lập phiếu yêu cầu hỏi giá · PTKD duyệt · PTKD không duyệt · XNK duyệt · XNK không duyệt · Huỷ duyệt (+ các bước YCTG / PTG).',
      '– Dòng của nhóm ghi “Nhóm <TH> — <Hãng>. <ghi chú / lý do>”; xem ở Chi tiết, mới → cũ.'], ['Xem chi tiết']),
    ('BR-20', 'Danh sách',
     ['– Mặc định 10 phiếu / trang (tối đa 100), sắp Ngày tạo giảm dần; sắp được Số phiếu, Ngày tạo, PTKD duyệt.',
      '– Tìm nhanh: số phiếu, mã hàng, tên hàng ghi trong phiếu; người tạo / PTKD / XNK là ô chọn.',
      '– Danh sách chỉ điều hướng: Xử lý / Lập YCTG mở màn khác, không duyệt tại chỗ.'], ['Xem danh sách', 'Tìm kiếm và lọc']),
    ('BR-21', 'Lối vào từ màn hàng hoá',
     ['– Nút “Lập yêu cầu hỏi giá” ở Hàng hoá nhập thông tin, Hàng đang kinh doanh, Hàng tạm (không cần quyền).',
      '– Tick hàng → form nạp sẵn, loại hàng không chọn được kèm câu “Bỏ <n> hàng không lập yêu cầu hỏi giá được: …”.',
      '– Quay lại về màn hàng hoá; lưu xong về danh sách YCHG.'], ['Tạo']),
    ('BR-22', 'Validate báo đồng thời, cảnh báo chưa lưu',
     ['– Bấm Lưu: mọi lỗi (ghi chú, danh sách hàng, từng hàng, từng nhóm) báo cùng lúc, cuộn tới lỗi đầu tiên.',
      '– Popup lý do: lỗi hiện dưới ô, popup giữ nguyên.',
      '– Rời form Tạo / Sửa / Duyệt hàng tạm khi có thay đổi → “Thông tin chưa lưu”.'], ['Tạo', 'Sửa', 'PTKD', 'XNK']),
])

# update_fields=False: Word dang mo tren may user — buoc cap nhat muc luc tren macOS se dong Word.
d.save(update_fields=os.environ.get('SRS_UPDATE_TOC') == '1')
print('OK ->', OUT)

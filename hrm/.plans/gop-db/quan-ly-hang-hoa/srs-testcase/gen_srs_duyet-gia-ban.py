# -*- coding: utf-8 -*-
"""Sinh SRS - Duyet gia ban (luong Chuyen doi hang hoa) — form chuan 2026-09-24.

Pham vi: man "Duyet gia ban" (Tai chinh > Quan ly gia - CTKM > Gia ban > Duyet gia ban, quyen 1658; loi phu Tai chinh >
Cho duyet > Gia ban cho duyet > Hang hoa cho duyet gia ban; deep-link tu thong bao [GIA] Cho duyet; ERP Cho duyet >
Duyet gia ban (HRM) mo tab moi). Xem yeu cau cho duyet cua cong ty dang lam, sua gia de nghi truoc khi duyet, Duyet /
Khong duyet tung yeu cau va hang loat, Xuat Excel, popup Lich su gia. Tap trung quy tac GIA BAN (gia nguoi duyet sua,
gia hieu luc doi ve ngay mai, gia dang chay da doi, gia von de nghi, quyen Xem gia von che gia von + he so, PTG).

Nguon doi chieu code: worktree wt-chuyen-doi-hang-hoa nhanh feat/chuyen-doi-hang-hoa
(hrm-api 39c4a91fe, hrm-client 5c14659e8) — doc ngay 16/10/2026.
  BE: Modules/MasterData/Routes/api.php (nhom product-price-approvals, gate 1658), ProductPriceApprovalController,
      Services/ProductPrice/{ProductPriceApprovalService, ProductPriceNotifier, ProductPriceHistoryService},
      Services/PriceCalculation/PriceCalculateFinalizer (bao nguoc PTG), Exports/ProductPriceApprovalExport
  FE: pages/finance/product-price-approvals/index.vue, components/product/price/{ProductPriceApprovalTable,
      ProductPriceHistoryModal}.vue, utils/productPriceModel.js (approvalRowsFromApi, validateApproval, coefToPrice),
      components/subsystem-menu/finance.js (2 loi vao)
  ERP (nhanh feat/2d1-erp-khong-loi): topmenubar "Duyet gia ban (HRM)", middleware ProductMovedToHrm 'price-approve'.

Anh chup: Playwright MCP 1440x900, cong 3031 (worktree, DB hrm_erp_giacty), tai khoan E2E Assign (co san 1658 + 1092 +
1657 tai Cty 1 — KHONG tao role tam). DB dev KHONG co yeu cau duyet nao (8 cong ty deu tat duyet gia) nen:
  - 14-trong, 16-lich-su-gia, 00-menu-*: du lieu THAT (API that tra 0 yeu cau / lich su rong).
  - 01..13, 15, 17..20: MINH HOA — chan API danh sach tren trinh duyet (route.fulfill) tra 3 yeu cau dung bo cuc may chu
    (hang that TEWI-AQUA / SULI-IN-2716-WHEEL-NO14 / -NO12 voi gia von, gia dang chay that cua Cty 1; gia de nghi tu dat).
    Moi lenh Duyet / Khong duyet bi chan tren trinh duyet (0 request toi may chu). 17: bat co "khong co quyen Xem gia
    von" o phan hoi. 20: tra dung phan hoi may chu cho ly do > 2000 ky tu (da do bang yeu cau id khong ton tai — chi
    validate, khong ghi).
  - 16b: anh THAT popup Lich su gia luc kiem G4 (cung component, man Cap nhat gia ban) de thay bo cuc timeline.

Chay:  python3 .plans/gop-db/quan-ly-hang-hoa/srs-testcase/gen_srs_duyet-gia-ban.py
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

SHOTS = os.path.join(HERE, 'duyet-gia-ban_shots')
OUT = os.path.join(HERE, 'SRS - Duyệt giá bán.docx')


def shot(name):
    return os.path.join(SHOTS, name)


ACTOR = 'Người duyệt giá bán'
MENU = 'Phân hệ Tài chính => Quản lý giá - CTKM => Giá bán => Duyệt giá bán'
MENU2 = 'Phân hệ Tài chính => Chờ duyệt => Giá bán chờ duyệt => Hàng hoá chờ duyệt giá bán'
SCREEN = 'Duyệt giá bán'

d = SrsDoc(out=OUT, menu=MENU, route='/finance/product-price-approvals',
           full_url='http://hrm/finance/product-price-approvals', img_prefix='dgb_')
d.set_menu_icons({k: shot(v) for k, v in {
    'Phân hệ Tài chính': 'icon_phanhe.png',
    'Quản lý giá - CTKM': 'icon_rail_quanlygia.png',
    'Giá bán': 'icon_nhom_giaban.png',
    'Duyệt giá bán': 'icon_duyetgiaban.png',
    'Chờ duyệt': 'icon_rail_choduyet.png',
    'Giá bán chờ duyệt': 'icon_nhom_giabanchoduyet.png',
    'Hàng hoá chờ duyệt giá bán': 'icon_hanghoachoduyet.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Duyệt': 'icon_duyet.png',
    'Không duyệt': 'icon_khongduyet.png',
    'Chọn yêu cầu': 'icon_tick.png',
    'Bỏ chọn': 'icon_bochon.png',
    'Xuất Excel': 'icon_xuatexcel.png',
    'Lịch sử giá': 'icon_lichsu.png',
}.items()})

MSG_NOPERM = 'Bạn không có quyền thực hiện chức năng này.'
MSG_GONE = 'Yêu cầu duyệt đã được xử lý.'
Q1 = 'Duyệt giá bán hàng hoá'
Q2 = 'Xem giá vốn hàng hoá'
Q3 = 'Cập nhật giá bán hàng hoá'

# ============================================================== TRANG DAU
d.title_block(SCREEN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Duyệt giá bán (phân hệ Tài chính) thuộc luồng Chuyển đổi hàng hoá '
    'sang hệ thống mới, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn Duyệt giá bán.',
    'Làm rõ YÊU CẦU DUYỆT GIÁ THEO CÔNG TY: mỗi yêu cầu là 1 hàng × 1 đơn vị tính × 1 công ty (công ty của bộ giá); người '
    'duyệt chỉ thấy và chỉ xử lý yêu cầu của công ty đang làm việc.',
    'Làm rõ người duyệt được SỬA giá đề nghị (hệ số, giá, ĐMGG, ngày hiệu lực) trước khi duyệt và hệ thống áp đúng giá '
    'đã sửa; giá vốn đề nghị áp nguyên văn.',
    'Làm rõ kết quả của Duyệt và Không duyệt lên bộ giá của công ty, lên trạng thái hàng hoá, lên Phiếu tính giá (khi yêu '
    'cầu sinh từ phiếu) và thông báo gửi người đề nghị.',
    'Làm rõ quyền Xem giá vốn hàng hoá: không có quyền này thì màn không hiện giá vốn và hệ số, không sửa được hệ số.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Công ty đang làm việc', 'Công ty người dùng đang chọn ở góc trên màn hình. Quyền, danh sách yêu cầu, bộ giá được ghi '
     'khi duyệt và lịch sử đều xét theo công ty này.'),
    ('Yêu cầu duyệt giá', '1 đề nghị giá đang chờ của 1 hàng × 1 ĐVT tại 1 công ty, gồm giá vốn đề nghị và các dòng giá '
     'đổi. Mỗi hàng × ĐVT × công ty tối đa 1 yêu cầu đang mở (gửi lại là ghi đè).'),
    ('Người đề nghị', 'Người bấm Gửi duyệt ở màn Cập nhật giá bán, hoặc người lập Phiếu tính giá gửi duyệt (cột Người cập nhật).'),
    ('Dòng giá', '1 loại giá trong yêu cầu (Bán lẻ, Giá bán theo lô, Đại lý cấp 1, 2, 3, Thương mại điện tử) — dòng “đang áp '
     'dụng” (giá hiện tại) hoặc dòng “Giá hiệu lực” (giá đặt trước cho 1 ngày).'),
    ('Giá cũ', 'Giá đang áp dụng của loại giá TẠI THỜI ĐIỂM người đề nghị gửi.'),
    ('Giá đang chạy', 'Giá đang áp dụng LÚC NÀY. Có thể khác Giá cũ nếu sau khi gửi đề nghị, Phiếu tính giá hoặc tác vụ áp giá '
     'hiệu lực hằng đêm đã đổi giá.'),
    ('Giá mới', 'Giá đề nghị; người duyệt sửa được trước khi bấm Duyệt.'),
    ('Giá vốn đề nghị', 'Giá vốn người đề nghị gửi kèm; khi Duyệt được ghi vào giá vốn của ĐVT tại công ty. Màn này không sửa.'),
    ('ĐMGG', 'Định mức giảm giá tối đa (%) của loại giá, 0 – 100.'),
    ('PTG', 'Phiếu tính giá — phiếu ra giá bán cho hàng mới; khi gửi duyệt sinh các yêu cầu duyệt giá trên màn này.'),
    ('Đang kinh doanh', 'Trạng thái của hàng TẠI một công ty; hàng mới chỉ chuyển sang trạng thái này sau khi giá được duyệt.'),
    ('Hàng loạt', 'Tick chọn nhiều yêu cầu rồi bấm Duyệt / Không duyệt trên thanh hàng loạt.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Mọi quyền xét theo CÔNG TY ĐANG LÀM VIỆC — có quyền ở công ty khác không được tính. Super admin không được miễn: '
    'thiếu quyền là không vào được màn.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1,
     'Thấy 2 mục menu Duyệt giá bán và Hàng hoá chờ duyệt giá bán; mở được màn; xem yêu cầu của công ty; sửa giá đề nghị; '
     'Duyệt / Không duyệt từng yêu cầu và hàng loạt; Xuất Excel; xem Lịch sử giá. Là quyền BẮT BUỘC của mọi chức năng; '
     'người có Q1 tại công ty là người NHẬN thông báo “[GIA] Chờ duyệt”.'),
    ('Q2', Q2,
     'Chỉ có tác dụng khi đã có Q1: thấy cột Giá vốn và cột Hệ số, sửa được hệ số (giá tự tính theo hệ số), Excel có 2 cột '
     'Giá vốn + Hệ số, lịch sử hiện dòng Giá vốn và hệ số. Không có Q2: hệ thống KHÔNG gửi giá vốn và hệ số về màn hình '
     '(giá ÷ hệ số suy ra được giá vốn), khi Duyệt hệ số giữ nguyên bản đề nghị. Chỉ có Q2 không có Q1 thì không vào được màn.'),
    ('Q3', Q3,
     'Không mở được màn này. Chỉ có 1 tác dụng phụ: người có Q1 + Q3 nhưng KHÔNG có Q2 vẫn thấy dòng Giá vốn và hệ số trong '
     'popup Lịch sử giá (vì Q3 đã được xem giá vốn ở màn Cập nhật giá bán), dù bảng duyệt vẫn ẩn 2 cột đó.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn không phân quyền theo cấp dữ liệu (công ty / phòng ban / bộ phận). Phạm vi dữ liệu cố định: yêu cầu duyệt giá '
    'CỦA CÔNG TY ĐANG LÀM VIỆC (công ty của bộ giá), của mọi người đề nghị.')
d.p('Quy định duyệt giá của công ty (bật duyệt giá / phạm vi hãng) chỉ quyết định khi người đề nghị bấm lưu sẽ ra yêu cầu '
    'duyệt hay áp thẳng (xem SRS Cập nhật giá bán); màn Duyệt KHÔNG đọc quy định này — yêu cầu đã có vẫn hiện và duyệt '
    'được kể cả khi công ty vừa tắt duyệt giá.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách yêu cầu chờ duyệt', '✅', '❌ (chỉ thêm cột khi có Q1)', '❌',
     '❌ (không thấy menu; mở thẳng màn không hiện gì, không tải dữ liệu)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '❌', '❌', '❌'),
    ('FR-03 Sửa giá đề nghị', '✅ (giá, ĐMGG, ngày hiệu lực)', '✅ thêm hệ số (khi có Q1)', '❌', '❌'),
    ('FR-04 Duyệt giá bán', '✅', '❌', '❌', '❌ (hệ thống từ chối khi gọi thẳng chức năng)'),
    ('FR-05 Không duyệt giá bán', '✅', '❌', '❌', '❌ (hệ thống từ chối khi gọi thẳng chức năng)'),
    ('FR-06 Duyệt / Không duyệt hàng loạt', '✅', '❌', '❌', '❌'),
    ('FR-07 Xuất Excel', '✅', '✅ thêm cột Giá vốn, Hệ số (khi có Q1)', '❌', '❌'),
    ('FR-08 Xem lịch sử giá', '✅', '✅ thêm Giá vốn, hệ số (khi có Q1)', '✅ thêm Giá vốn, hệ số (khi có Q1)', '❌'),
], widths=[2.0, 1.0, 1.1, 1.0, 1.0])

# ========================================================= PHAN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR, [0, 1, 2, 3, 4, 5])],
    [('FR-01', 'Xem danh sách yêu cầu chờ duyệt', 'view'),
     ('FR-03', 'Sửa giá đề nghị', 'crud'),
     ('FR-04', 'Duyệt giá bán', 'action'),
     ('FR-05', 'Không duyệt giá bán', 'action'),
     ('FR-06', 'Duyệt / Không duyệt hàng loạt', 'action'),
     ('FR-07', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-08', 'Xem lịch sử giá', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Duyệt giá bán')

d.h2('2 Đặc tả chi tiết từng chức năng')

LIST_RULE = ('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn '
             'Duyệt giá bán tại phần mô tả chi tiết.')
CREATE_RULE = ('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng của màn Duyệt giá bán '
               'tại phần mô tả chi tiết.')
NOTICE_RULE = ('- Thông báo và Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn Duyệt giá bán tại phần mô tả chi tiết.')

APPROVE_AFTER = [
    '– Với mỗi dòng giá đang áp dụng: ghi Giá / Hệ số / ĐMGG NGƯỜI DUYỆT GỬI (đã sửa hoặc giữ nguyên đề nghị) thành giá '
    'đang áp dụng của loại giá TẠI CÔNG TY CỦA YÊU CẦU; xoá cờ Chờ duyệt.',
    '– Với mỗi dòng giá hiệu lực: ghi giá / hệ số / ĐMGG / ngày; ngày trước ngày mai → dời về ngày mai; giá hiệu lực đã bị '
    'xoá hoặc đã được áp trước đó → bỏ qua dòng.',
    '– Không có quyền Xem giá vốn hàng hoá: hệ số giữ nguyên bản đề nghị (không nhận hệ số từ màn hình).',
    '– Giá vốn của ĐVT tại công ty = giá vốn đề nghị; xoá “Lý do không duyệt” cũ.',
    '– Hàng mới đang chờ duyệt (trạng thái cũ của ERP) và công ty của yêu cầu là công ty quản lý hàng → hàng chuyển Đang '
    'kinh doanh tại công ty đó, kèm đủ bộ giá mọi ĐVT.',
    '– Yêu cầu sinh từ Phiếu tính giá → ghi kết quả “đã duyệt” + giá thực áp lên dòng của phiếu, rồi chốt phiếu (xem BR-17).',
    '– Ghi 1 dòng lịch sử “Duyệt giá” (chỉ ô thực sự đổi); xoá hẳn yêu cầu khỏi danh sách chờ.',
    '– Gửi “[GIA] Đã duyệt: <mã> – <tên>. Giá mới áp dụng từ <ngày>” cho người đề nghị (yêu cầu từ Phiếu tính giá: báo ở '
    'mức phiếu “[PTG] Đã duyệt”).',
]
REJECT_AFTER = [
    '– Giá đang áp dụng GIỮ NGUYÊN; các ô đang Chờ duyệt của yêu cầu (giá vốn, giá, hệ số, ĐMGG, giá hiệu lực) chuyển cờ '
    'Không duyệt.',
    '– Ghi “Lý do không duyệt” + thời điểm vào ĐVT tại công ty (màn Cập nhật giá bán hiện “Lý do không duyệt: <lý do>”).',
    '– Hàng mới đang chờ duyệt và công ty của yêu cầu là công ty quản lý hàng → hàng chuyển trạng thái Không duyệt (trạng '
    'thái cũ của ERP).',
    '– Yêu cầu sinh từ Phiếu tính giá → dòng của phiếu ghi “bị từ chối” + lý do; phiếu chuyển Giá bị từ chối (xem BR-17).',
    '– Ghi 1 dòng lịch sử “Không duyệt giá” kèm “Lý do không duyệt: <lý do>”; xoá hẳn yêu cầu khỏi danh sách chờ.',
    '– Gửi “[GIA] Từ chối: <mã> – <tên>. Lý do: <lý do>” cho người đề nghị (yêu cầu từ Phiếu tính giá: “[PTG] Từ chối”).',
]

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách yêu cầu chờ duyệt')
d.p('2.1.1 Giới thiệu')
d.rule_ref(LIST_RULE, anchor='list')
d.intro_table(
    ten='Xem danh sách yêu cầu chờ duyệt giá bán',
    mota='Hiển thị các yêu cầu duyệt giá đang chờ CỦA CÔNG TY ĐANG LÀM VIỆC, mỗi yêu cầu là 1 khối (hàng × ĐVT) gồm giá vốn '
         'đề nghị, các dòng giá đổi (giá cũ → giá mới, hệ số, ĐMGG cũ → mới, hiệu lực), người cập nhật, thời gian, mã hàng. '
         'Bảng là bảng nhập liệu tại chỗ: người duyệt sửa được giá rồi Duyệt / Không duyệt ngay trên dòng.',
    tacnhan=ACTOR + '; Người dùng đã đăng nhập',
    dieukien='Người dùng có quyền ' + Q1 + ' tại công ty đang làm việc.',
    chinh='1. Người dùng vào màn qua 1 trong các lối vào ở mục 2.1.2.\n'
          '2. Hệ thống lấy các yêu cầu đang chờ của công ty đang làm việc, mới cập nhật lên trước, 20 yêu cầu / trang.\n'
          '3. Mỗi yêu cầu hiện các dòng giá theo thứ tự Bán lẻ, Giá bán theo lô, Đại lý cấp 1, 2, 3, TMĐT; giá hiệu lực nằm '
          'ngay dưới loại giá của nó.\n'
          '4. Có quyền ' + Q2 + ' → hiện thêm cột Giá vốn và Hệ số.',
    phu='• Không có yêu cầu nào → “Không có yêu cầu duyệt giá nào”.\n'
        '• Đang lọc / mở từ thông báo mà không có kết quả → “Không có dữ liệu phù hợp”.\n'
        '• Mở từ thông báo “[GIA] Chờ duyệt” → chỉ hiện đúng yêu cầu đó; yêu cầu đã được xử lý → cảnh báo “Yêu cầu đã được '
        'xử lý”, bảng rỗng.\n'
        '• Yêu cầu chỉ đổi giá vốn → khối có 1 dòng “Chỉ đổi giá vốn — không đổi giá bán”.\n'
        '• Không có quyền tại công ty đang làm việc → không thấy menu; mở thẳng màn thì màn trống, không tải dữ liệu.\n'
        '• Lỗi tải → thông báo “Lỗi khi tải dữ liệu”.')
d.p('2.1.2 Layout màn hình')
d.p('Đường dẫn màn hình (4 lối vào, CÙNG một màn, CÙNG phạm vi dữ liệu = yêu cầu chờ duyệt của công ty đang làm việc):')
d.layout(menu=MENU, shot=shot('00-menu-quan-ly-gia.png'),
         shot_caption='Lối vào chính: Quản lý giá - CTKM › Giá bán › Duyệt giá bán (dữ liệu thật)')
d.layout(menu=MENU2, shot=shot('00-menu-cho-duyet.png'),
         shot_caption='Lối vào phụ: Chờ duyệt › Giá bán chờ duyệt › Hàng hoá chờ duyệt giá bán (dữ liệu thật)')
d.bullets([
    'Thông báo “[GIA] Chờ duyệt: <mã> – <tên>. Người đề nghị: <tên>” trên chuông → mở màn chỉ hiện đúng yêu cầu đó. Thông '
    'báo “[GIA] Chờ duyệt: <mã phiếu tính giá>. <n> dòng giá. Người đề nghị: <tên>” → mở màn với toàn bộ danh sách.',
    'Hệ thống ERP: menu Chờ duyệt › “Duyệt giá bán (HRM)” mở màn này ở tab mới; đường vào màn duyệt giá cũ của ERP được '
    'chuyển sang màn này.',
])
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn Duyệt giá bán có 3 yêu cầu (minh hoạ — dữ liệu dev không có yêu cầu chờ)')
d.layout(menu=MENU, shot=shot('02-cot-ben-phai.png'),
         shot_caption='Phần bên phải bảng: ĐMGG cũ / mới, Hiệu lực (có dòng “Duyệt sẽ dời về …”), Người cập nhật, Thời gian, Mã hàng hoá')
d.layout(menu=MENU, shot=shot('03-chi-doi-gia-von.png'),
         shot_caption='Yêu cầu chỉ đổi giá vốn (“Cũ: 2,915,000”) và yêu cầu có giá đang chạy đã đổi (minh hoạ)')
d.layout(menu=MENU, shot=shot('14-trong.png'), shot_caption='Không có yêu cầu nào (dữ liệu thật)')
d.layout(menu=MENU, shot=shot('17-khong-quyen-gia-von.png'),
         shot_caption='Người duyệt không có quyền Xem giá vốn hàng hoá: không có cột Giá vốn, Hệ số (minh hoạ)')
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Duyệt giá bán', 'Tiêu đề trên thanh đầu trang và tiêu đề khối bảng.'),
    ('Dòng đếm cạnh tiêu đề', 'Text', 'Read-only', '≥ 0', 'Theo dữ liệu', [
        '- Mẫu: “· N yêu cầu chờ duyệt tại <tên công ty đang làm việc>”.',
        '- N = tổng số yêu cầu khớp bộ lọc (không phải số dòng trên trang).',
        '- Không đọc được tên công ty thì ghi “công ty đang làm việc”.']),
    ('Bảng yêu cầu', 'Table/Grid', 'Enable', '15 cột (13 khi không có quyền Xem giá vốn)', 'Theo dữ liệu', [
        '- Tiêu đề 1 dòng, dính trên khi cuộn dọc; bảng có vùng cuộn riêng (dọc + ngang).',
        '- 3 cột ô tick, #, Tên hàng hoá dính trái khi cuộn ngang.',
        '- Mỗi yêu cầu là 1 khối nhiều dòng: các cột của yêu cầu gộp dọc, mỗi dòng giá đổi 1 dòng.',
        '- Không sắp xếp theo cột; thứ tự cố định: yêu cầu cập nhật gần nhất lên trước.']),
    ('Cột ô tick', 'Checkbox', 'Enable', '–', 'Không tick', [
        '- Ô ở tiêu đề: chọn / bỏ chọn tất cả yêu cầu ĐANG HIỆN; tick một phần thì ô ở trạng thái nửa (gạch ngang).',
        '- Tooltip ô tiêu đề: “Chọn tất cả yêu cầu đang hiện”. Không có yêu cầu thì bị khoá.',
        '- Tick ≥ 1 → hiện thanh hàng loạt (mục 2.6).']),
    ('Cột #', 'Text', 'Read-only', 'Số nguyên', 'Theo dữ liệu', 'Số thứ tự liên tục qua các trang.'),
    ('Cột Tên hàng hoá', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Dòng 1: tên hàng; dòng 2: mã hàng (chữ xám).',
        '- “Lý do sửa giá: <lý do>”: hiện khi người đề nghị có nhập lý do.',
        '- Nút “Duyệt” (xanh) → mục 2.4; nút “Không duyệt” (đỏ) → mục 2.5; nút đồng hồ (tooltip “Lịch sử giá”) → mục 2.8.',
        '- Đang xử lý 1 thao tác thì nút Duyệt / Không duyệt tạm khoá.']),
    ('Cột ĐVT', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Đơn vị tính của yêu cầu (mỗi ĐVT là 1 yêu cầu riêng).'),
    ('Cột Giá vốn', 'Number', 'Read-only / Ẩn', '≥ 0', 'Ẩn khi thiếu quyền', [
        '- Giá vốn ĐỀ NGHỊ (dấu phẩy ngăn nghìn); không sửa ở màn này.',
        '- “Cũ: <giá vốn đang chạy của công ty>”: chỉ hiện khi khác giá vốn đề nghị.',
        '- Chỉ hiện với người có quyền ' + Q2 + '.',
        '- Icon ⓘ: “Giá vốn người đề nghị gửi kèm — áp vào công ty khi Duyệt (không sửa ở màn này).”']),
    ('Cột Loại giá', 'Text', 'Read-only', 'Danh sách 6 giá trị', 'Theo dữ liệu', [
        '- Tên loại giá; rê chuột dòng TMĐT thấy tên đầy đủ “Giá bán thương mại điện tử ( online)”.',
        '- Dòng giá hiệu lực: “└ Giá hiệu lực” (chữ xám) dưới loại giá của nó.',
        '- Chỉ có các loại giá có thay đổi; yêu cầu chỉ đổi giá vốn: 1 dòng “Chỉ đổi giá vốn — không đổi giá bán”.']),
    ('Cột Giá cũ', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu', [
        '- Giá đang áp dụng lúc người đề nghị gửi.',
        '- Dòng giá hiệu lực: để trống.']),
    ('Cột Hệ số', 'Number', 'Enable / Ẩn', '0 – < 100, tối đa 2 số lẻ', 'Hệ số đề nghị', [
        '- Ô nhập; gõ hệ số → Giá mới tự tính = làm tròn trăm (hệ số × giá vốn đề nghị) (mục 2.3).',
        '- Chỉ hiện với người có quyền ' + Q2 + '.']),
    ('Cột Giá mới', 'Number', 'Enable', '0 – 999.999.999.999', 'Giá đề nghị', [
        '- Ô nhập số tiền, dấu phẩy ngăn nghìn, không số lẻ.',
        '- Dưới ô: chênh lệch so với Giá cũ — “+<số>” chữ xanh lá khi tăng, “−<số>” chữ cam khi giảm, trống khi bằng.',
        '- Dòng giá hiệu lực: không hiện chênh lệch.']),
    ('Cột ĐMGG cũ', 'Number', 'Read-only', '0 – 100', 'Theo dữ liệu', 'ĐMGG lúc gửi; dòng giá hiệu lực để trống.'),
    ('Cột ĐMGG mới', 'Number', 'Enable', '0 – 100, tối đa 2 số lẻ', 'ĐMGG đề nghị', 'Ô nhập; bỏ trống được (duyệt ghi 0).'),
    ('Cột Hiệu lực', 'Text / Datepicker', 'Read-only / Enable', 'dd/mm/yyyy', 'Theo dữ liệu', [
        '- Dòng giá đang áp dụng: chữ xanh “Đang áp dụng”.',
        '- Dòng giá hiệu lực: ô chọn ngày (không xoá trắng được).',
        '- Ngày trước ngày mai → chữ cam “Duyệt sẽ dời về <ngày mai>” ngay dưới ô.']),
    ('Cột Người cập nhật', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     '- “<mã phòng ban lúc gửi> - <họ tên người đề nghị>”, vd “HN_KD2 - E2E Assign”.'),
    ('Cột Thời gian', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Lần gửi / gửi lại đề nghị gần nhất.'),
    ('Cột Mã hàng hoá', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Mã hàng là link: bấm → mở màn Xem chi tiết hàng hoá ở TAB MỚI (không mất giá đang sửa).',
        '- “Ghi chú: <ghi chú hàng hoá>” chỉ đọc, hiện khi có.']),
    ('Chân bảng', 'Pagination', 'Enable', '10 / 20 / 50', '20 dòng / trang', [
        '- “Hiển thị a–b / N yêu cầu”: a, b là yêu cầu đầu / cuối trang; N là tổng số yêu cầu khớp bộ lọc.',
        '- Ô “Số dòng/trang” 10 / 20 / 50; đổi → về trang 1.',
        '- Đổi trang KHÔNG mất ô đã tick và giá đã sửa.']),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', [
        '- Chưa lọc: “Không có yêu cầu duyệt giá nào”.',
        '- Đang lọc / mở từ thông báo: “Không có dữ liệu phù hợp”.']),
    ('Đang tải', 'Loading', 'Hiển thị', '–', 'Ẩn', '“Đang tải…” trong bảng. Lỗi tải: thông báo “Lỗi khi tải dữ liệu”.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền ' + Q1 + ' tại công ty đang làm việc.\n'
     '– Không có quyền → màn không hiển thị và không tải dữ liệu; gọi thẳng chức năng thì hệ thống báo “' + MSG_NOPERM + '”.\n'
     'During:\n– Lấy yêu cầu chờ duyệt của công ty đang làm việc (công ty lấy từ phiên làm việc, không nhận từ màn hình).\n'
     '– Mở từ thông báo: chỉ lấy đúng yêu cầu trong thông báo.\n'
     '– Không có quyền ' + Q2 + ': không lấy giá vốn, hệ số.\n'
     'After:\n– Hiện trang 1 (20 yêu cầu). Mở từ thông báo mà yêu cầu không còn → cảnh báo “Yêu cầu đã được xử lý”.'),
    ('Đổi trang / số dòng mỗi trang', 'Click / Change',
     'After:\n– Tải lại dữ liệu; đổi số dòng thì về trang 1; cuộn bảng lên đầu.\n– Giữ nguyên ô đã tick và giá đã sửa.'),
    ('Bấm Mã hàng hoá', 'Click', 'After:\n– Mở màn Xem chi tiết hàng hoá ở tab mới.'),
    ('Đổi công ty đang làm việc', 'System',
     'After:\n– Danh sách tải lại theo công ty mới; không còn thấy yêu cầu của công ty cũ.'),
    ('Rời màn khi đã sửa giá chưa duyệt', 'System',
     'After:\n– Hộp thoại “Thông tin chưa lưu”: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” — “Thoát” / “Ở lại”.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown. Chỉ bổ sung các quy tắc riêng của màn Duyệt giá bán tại phần mô tả chi tiết.',
           anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc yêu cầu chờ duyệt',
    mota='Thu hẹp danh sách theo từ khoá, cây phân loại hàng hoá, hãng sản xuất và người cập nhật (người đề nghị).',
    tacnhan=ACTOR,
    dieukien='Đang ở màn Duyệt giá bán.',
    chinh='1. Người dùng gõ từ khoá vào ô tìm nhanh rồi nhấn Enter hoặc bấm Tìm kiếm.\n'
          '2. Muốn lọc thêm: bấm Tìm kiếm nâng cao để mở các ô lọc, chọn giá trị — mỗi lần chọn là lọc ngay.\n'
          '3. Hệ thống tải lại danh sách từ trang 1.',
    phu='• Bấm Làm mới → xoá toàn bộ điều kiện lọc (kể cả lọc mở từ thông báo), về trang 1.\n'
        '• Đổi cấp trên của cây phân loại → các cấp dưới bị xoá trắng.\n'
        '• Lọc lại KHÔNG bỏ ô đã tick, KHÔNG bỏ giá đã sửa; yêu cầu đã tick bị bộ lọc ẩn vẫn được tính trong thanh hàng loạt.\n'
        '• Không có kết quả → “Không có dữ liệu phù hợp”.')
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('04-loc-nang-cao.png'),
         shot_caption='Khối bộ lọc khi mở Tìm kiếm nâng cao (minh hoạ)')
d.layout(menu=MENU, shot=shot('06-chon-giu-qua-loc.png'),
         shot_caption='Lọc theo từ khoá vẫn giữ 2 yêu cầu đã tick: “Đã chọn 2 yêu cầu (1 đang ẩn do bộ lọc)” (minh hoạ)')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề khối', 'Label', 'Hiển thị', '–', 'Không', 'Bộ lọc danh sách', 'Tiêu đề khối lọc.'),
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
        '- Placeholder: “Tìm theo mã / tên / model hàng hoá”.',
        '- Tìm gần đúng trên mã, tên hàng (cả mã / tên lúc gửi và mã / tên hiện tại) và tên model.',
        '- Chỉ chạy khi nhấn Enter hoặc bấm Tìm kiếm; có nút ✕ xoá nhanh.']),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chạy tìm theo từ khoá + các ô lọc, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá mọi điều kiện lọc (kể cả lọc mở từ thông báo), về trang 1.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Đóng',
     ['- Mặc định khối ô lọc đang đóng.', '- Bấm để mở / đóng các ô lọc; bảng tự co giãn chiều cao theo.']),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở popup ẩn / hiện và đổi thứ tự ô lọc; cấu hình lưu theo người dùng.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ở đầu khối lọc — xem mục 2.7.'),
    ('Tính chất', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Cấp 1 của cây phân loại hàng hoá.', '- Đổi → xoá trắng Nhóm công nghệ, Nhóm sản phẩm, Loại sản phẩm.']),
    ('Nhóm công nghệ', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Chỉ liệt kê nhóm thuộc Tính chất đã chọn.', '- Đổi → xoá trắng 2 cấp dưới.']),
    ('Nhóm sản phẩm', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Chỉ liệt kê nhóm thuộc Nhóm công nghệ đã chọn.', '- Đổi → xoá trắng Loại sản phẩm.']),
    ('Loại sản phẩm', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Chỉ liệt kê loại thuộc Nhóm sản phẩm đã chọn.', '- Loại đã khoá có biểu tượng ổ khoá trước tên.',
      '- Lọc theo loại sản phẩm HIỆN TẠI của hàng.']),
    ('Hãng sản xuất', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- CHỈ liệt kê các hãng có trong yêu cầu chờ duyệt của công ty (không phải mọi hãng).',
      '- Lọc theo hãng lúc gửi đề nghị.']),
    ('Người cập nhật', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- CHỈ liệt kê người đã gửi yêu cầu đang chờ của công ty, dạng “<mã phòng> - <họ tên>”, xếp theo tên.']),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Nhấn Enter ở ô tìm nhanh / bấm Tìm kiếm', 'Keypress / Click',
     'After:\n– Bỏ lọc theo yêu cầu của thông báo (nếu có), tải lại từ trang 1; giữ ô đã tick + giá đã sửa.'),
    ('Chọn giá trị ở 1 ô lọc', 'Change',
     'After:\n– Lọc ngay, về trang 1; đổi cấp cây phân loại → xoá trắng các cấp dưới trong cùng 1 lần tải.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xoá mọi ô lọc + lọc của thông báo, tải lại trang 1.'),
    ('Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở / đóng khối ô lọc; bảng đo lại chiều cao vùng cuộn.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Sửa giá đề nghị')
d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Sửa giá đề nghị', 'crud', actor=ACTOR, caption='Biểu đồ Use Case — FR-03 Sửa giá đề nghị')
d.p('2.3.2 Giới thiệu')
d.rule_ref(CREATE_RULE, anchor='create')
d.intro_table(
    ten='Sửa giá đề nghị trước khi duyệt',
    mota='Người duyệt sửa Hệ số, Giá mới, ĐMGG mới, ngày hiệu lực của từng dòng giá ngay trên bảng; khi bấm Duyệt hệ thống áp '
         'ĐÚNG giá đã sửa. Giá đã sửa chỉ nằm trên màn (không lưu riêng) cho tới khi bấm Duyệt.',
    tacnhan=ACTOR,
    dieukien='Có quyền ' + Q1 + ' tại công ty đang làm việc; sửa Hệ số cần thêm quyền ' + Q2 + '.',
    chinh='1. Người duyệt gõ hệ số → Giá mới tự tính = làm tròn trăm (hệ số × giá vốn đề nghị); chênh lệch tính lại.\n'
          '2. Hoặc gõ thẳng Giá mới / ĐMGG mới; chọn lại ngày cho dòng giá hiệu lực.\n'
          '3. Bấm Duyệt (mục 2.4) hoặc Duyệt hàng loạt (mục 2.6) để áp.',
    phu='• Sửa 1 dòng KHÔNG lan sang dòng khác: sửa Bán lẻ không đổi Giá bán theo lô, Đại lý, TMĐT (khác màn Cập nhật giá bán).\n'
        '• Sửa giá không tính ngược hệ số; muốn hệ số khớp thì sửa hệ số.\n'
        '• Ngày hiệu lực trước ngày mai → không báo lỗi, hiện “Duyệt sẽ dời về <ngày mai>”.\n'
        '• Lọc lại / đổi trang → giá đã sửa còn nguyên; người đề nghị gửi lại đề nghị mới → giá đã sửa bị bỏ, hiện bản mới.\n'
        '• Rời màn khi còn giá đã sửa → hỏi “Thông tin chưa lưu”.',
    dacbiet='Ô sai được kiểm khi bấm Duyệt (báo đồng thời mọi ô của mọi yêu cầu được duyệt) — xem mục 2.4.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU, shot=shot('12-sua-he-so.png'),
         shot_caption='Sửa hệ số Bán lẻ 1,7 → 1,75: Giá mới 342,982,100, chênh lệch +1,982,100; các loại giá khác giữ nguyên (minh hoạ)')
d.layout(menu=MENU, shot=shot('15-roi-man-chua-luu.png'),
         shot_caption='Rời màn khi còn giá đã sửa: hộp thoại “Thông tin chưa lưu” (minh hoạ)')
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Hệ số', 'Number', 'Enable / Ẩn', '0 – < 100, tối đa 2 số lẻ', 'Có', 'Hệ số đề nghị', [
        '- Chỉ có khi có quyền ' + Q2 + '.',
        '- Gõ hệ số → Giá mới = làm tròn TRĂM (hệ số × giá vốn đề nghị), áp cả cho dòng giá hiệu lực.',
        '- Vd giá vốn 195,989,760 × 1,75 → 342,982,100.',
        '- Trống → “Bắt buộc phải nhập”; ≥ 100 → “Không được vượt quá 2 chữ số trước dấu phẩy”.']),
    ('Giá mới', 'Number', 'Enable', '0 – 999.999.999.999', 'Có', 'Giá đề nghị', [
        '- Số nguyên; trống → “Bắt buộc phải nhập”; > 12 chữ số → “Không được vượt quá 12 chữ số”.',
        '- Chênh lệch dưới ô = Giá mới − Giá cũ: “+” xanh lá khi tăng, “−” cam khi giảm.']),
    ('ĐMGG mới', 'Number', 'Enable', '0 – 100, tối đa 2 số lẻ', 'Không', 'ĐMGG đề nghị',
     ['- Bỏ trống được (duyệt ghi 0).', '- Ngoài 0 – 100 → “Phải từ 0 đến 100”.']),
    ('Ngày hiệu lực', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có (dòng giá hiệu lực)', 'Ngày đề nghị', [
        '- Placeholder “dd/mm/yyyy”; không xoá trắng được.',
        '- Ngày trước ngày mai → “Duyệt sẽ dời về <ngày mai>” (không phải lỗi).',
        '- Trống → “Bắt buộc phải chọn”; sai định dạng → “Ngày không hợp lệ”.']),
    ('Lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     ['- Chữ đỏ ngay dưới ô sai + viền đỏ.', '- Sửa ô nào thì lỗi ô đó mất, lỗi ô khác giữ nguyên.']),
    ('Hộp thoại Thông tin chưa lưu', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     ['- “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”', '- Nút “Thoát” (bỏ giá đã sửa, rời màn) / “Ở lại”.']),
])
d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Gõ Hệ số', 'Change',
     'After:\n– Giá mới = làm tròn trăm (hệ số × giá vốn đề nghị); chênh lệch tính lại.\n– Xoá lỗi của ô Hệ số và ô Giá mới cùng dòng.'),
    ('Gõ Giá mới / ĐMGG mới', 'Change', 'After:\n– Cập nhật giá đã sửa; chênh lệch tính lại; xoá lỗi của đúng ô vừa sửa.'),
    ('Chọn ngày hiệu lực', 'Change',
     'After:\n– Ngày trước ngày mai → hiện “Duyệt sẽ dời về <ngày mai>”; xoá lỗi của ô ngày.'),
    ('Danh sách tải lại', 'System',
     'After:\n– Yêu cầu không đổi → giữ giá đã sửa.\n– Yêu cầu vừa được người đề nghị gửi lại (khác bản cũ) → bỏ giá đã sửa, hiện bản mới.'),
    ('Rời màn', 'System', 'Before:\n– Còn giá đã sửa → hỏi “Thông tin chưa lưu”; Ở lại → ở lại màn.'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Duyệt giá bán')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Duyệt giá bán', 'action', actor=ACTOR, caption='Biểu đồ Use Case — FR-04 Duyệt giá bán')
d.p('2.4.2 Giới thiệu')
d.rule_ref(NOTICE_RULE, anchor='notice')
d.intro_table(
    ten='Duyệt giá bán (1 yêu cầu)',
    mota='Áp giá đề nghị (đã sửa nếu có) thành giá đang áp dụng của công ty, ghi giá vốn đề nghị, xoá yêu cầu khỏi danh sách '
         'chờ và báo người đề nghị.',
    tacnhan=ACTOR,
    dieukien='Có quyền ' + Q1 + ' tại công ty đang làm việc; yêu cầu còn đang chờ.',
    chinh='1. Bấm “Duyệt” ở ô Tên hàng hoá của yêu cầu.\n'
          '2. Hệ thống kiểm tra mọi ô của yêu cầu; sai → báo đỏ, dừng.\n'
          '3. Hiện popup “Duyệt giá bán” gọi tên “<mã> – <tên> (<ĐVT>)”, nhắc giá hiệu lực sẽ dời ngày và giá đang chạy đã đổi '
          '(nếu có).\n'
          '4. Bấm “Duyệt” ở popup.\n'
          '5. Hệ thống áp giá (BR-07 … BR-12), ghi lịch sử, gửi thông báo.\n'
          '6. Thông báo “Đã duyệt 1 yêu cầu giá bán.”; yêu cầu biến khỏi danh sách.',
    phu='• Bấm Hủy / ✕ → không duyệt, giữ giá đã sửa.\n'
        '• Giá đang chạy đã đổi sau khi đề nghị → vẫn duyệt theo giá trên màn, thông báo thêm “Có n dòng giá đang chạy đã đổi '
        'trước khi duyệt.”.\n'
        '• Yêu cầu vừa được người khác xử lý / người đề nghị gỡ hàng → “' + MSG_GONE + '”, danh sách tải lại.\n'
        '• Hàng đã bị khoá / Ngừng kinh doanh ở công ty sau khi gửi đề nghị → VẪN duyệt được và giá vẫn áp (hệ thống không kiểm '
        'trạng thái hàng ở bước duyệt — đang chờ nghiệp vụ xác nhận).',
    dacbiet='Một lần duyệt chạy trọn trong 1 giao dịch: lỗi giữa chừng thì không ghi gì. Hai người cùng duyệt 1 yêu cầu: người '
            'sau nhận “' + MSG_GONE + '”.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Duyệt', shot=shot('13-loi-o-nhap.png'),
         shot_caption='Bấm Duyệt khi có ô sai: báo đồng thời mọi ô, không mở popup (minh hoạ)')
d.layout(menu=MENU + ' => Duyệt', shot=shot('07-xac-nhan-duyet-hang-loat.png'),
         shot_caption='Popup xác nhận Duyệt: danh sách hàng, giá hiệu lực dời ngày, giá đang chạy đã đổi (minh hoạ, bản hàng loạt)')
d.layout(menu=MENU + ' => Duyệt', shot=shot('08-duyet-thanh-cong.png'),
         shot_caption='Thông báo sau khi duyệt (minh hoạ — lệnh duyệt bị chặn trên trình duyệt, không ghi dữ liệu)')
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Duyệt (trên dòng)', 'Button', 'Enable / Disable', '–', 'Hiển thị',
     ['- Nút xanh, biểu tượng dấu tích.', '- Tạm khoá khi đang xử lý 1 thao tác khác.']),
    ('Popup – tiêu đề', 'Modal', 'Hiển thị', '–', 'Ẩn', '“Duyệt giá bán” (1 yêu cầu) / “Duyệt giá bán hàng loạt” (nhiều).'),
    ('Popup – danh sách', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- 1 yêu cầu: “Duyệt giá bán cho:” + “<mã> – <tên> (<ĐVT>)”.',
        '- Câu: “Giá mới (đã sửa trên màn này, nếu có) áp dụng ngay; giá vốn đề nghị ghi vào công ty <tên công ty>.”']),
    ('Popup – giá hiệu lực dời ngày', 'Text', 'Read-only / Ẩn', '–', 'Ẩn', [
        '- Chỉ hiện khi có dòng giá hiệu lực ngày trước ngày mai.',
        '- “Giá hiệu lực có ngày trước ngày mai sẽ dời về <ngày mai>:” + “<mã>: <ngày cũ> → <ngày mai>”.']),
    ('Popup – giá đang chạy đã đổi', 'Text', 'Read-only / Ẩn', '–', 'Ẩn', [
        '- Chữ nâu, chỉ hiện khi Giá cũ ≠ giá đang chạy.',
        '- “Giá đang chạy đã đổi sau khi đề nghị (phiếu tính giá / cron) — vẫn duyệt theo giá trên màn này:” + '
        '“<mã>: giá đang chạy <giá> (lúc đề nghị <giá>)”.']),
    ('Popup – nút Duyệt', 'Button', 'Enable', '–', 'Hiển thị', 'Xác nhận duyệt.'),
    ('Popup – nút Hủy / ✕', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng popup, không duyệt.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', [
        '- “Đã duyệt <n> yêu cầu giá bán.”',
        '- Thêm “ Có <w> dòng giá đang chạy đã đổi trước khi duyệt.” khi có.',
        '- Thêm “ <s> yêu cầu đã được người khác xử lý.” khi có (hàng loạt).',
        '- Ô sai: “<n> yêu cầu có ô chưa hợp lệ — sửa chữ đỏ rồi duyệt lại”.',
        '- Không còn yêu cầu: “' + MSG_GONE + '”.']),
], required=False)
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Duyệt trên dòng', 'Click',
     'Before:\n– Đang xử lý thao tác khác → bỏ qua.\n'
     'During:\n– Kiểm đồng thời mọi ô của yêu cầu: Giá mới trống → “Bắt buộc phải nhập”; > 12 chữ số → “Không được vượt quá 12 chữ số”.\n'
     '– Hệ số (khi có quyền Xem giá vốn) trống → “Bắt buộc phải nhập”; ≥ 100 → “Không được vượt quá 2 chữ số trước dấu phẩy”.\n'
     '– ĐMGG ngoài 0 – 100 → “Phải từ 0 đến 100”.\n'
     '– Ngày hiệu lực trống → “Bắt buộc phải chọn”; sai định dạng → “Ngày không hợp lệ”.\n'
     '– Có lỗi → thông báo “1 yêu cầu có ô chưa hợp lệ — sửa chữ đỏ rồi duyệt lại”, cuộn tới ô sai đầu tiên, không mở popup.\n'
     'After:\n– Mở popup xác nhận Duyệt giá bán.'),
    ('Bấm Duyệt ở popup', 'Click',
     'Before:\n– Kiểm quyền ' + Q1 + ' tại công ty đang làm việc; không có → “' + MSG_NOPERM + '”.\n'
     'During:\n– Kiểm lại các ô như trên (máy chủ); sai → chữ đỏ dưới ô.\n'
     '– Yêu cầu không còn hoặc thuộc công ty khác → “' + MSG_GONE + '”, danh sách tải lại.\n'
     '– Khoá yêu cầu trong lúc ghi: người khác vừa xử lý → bỏ qua yêu cầu đó.\n'
     'After:\n' + '\n'.join(APPROVE_AFTER) + '\n– Hiển thị “Đã duyệt 1 yêu cầu giá bán.”, tải lại danh sách.'),
    ('Bấm Hủy / ✕ ở popup', 'Click', 'After:\n– Đóng popup, giữ nguyên giá đã sửa.'),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Không duyệt giá bán')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Không duyệt giá bán', 'action', actor=ACTOR, caption='Biểu đồ Use Case — FR-05 Không duyệt giá bán')
d.p('2.5.2 Giới thiệu')
d.rule_ref(NOTICE_RULE, anchor='notice')
d.intro_table(
    ten='Không duyệt giá bán (1 yêu cầu)',
    mota='Từ chối đề nghị kèm lý do BẮT BUỘC: giá đang áp dụng giữ nguyên, ô đề nghị chuyển cờ Không duyệt, người đề nghị '
         'nhận lý do và thấy nhãn “Không duyệt” ở màn Cập nhật giá bán.',
    tacnhan=ACTOR,
    dieukien='Có quyền ' + Q1 + ' tại công ty đang làm việc; yêu cầu còn đang chờ.',
    chinh='1. Bấm “Không duyệt” ở ô Tên hàng hoá.\n'
          '2. Hiện popup “Không duyệt giá bán”: “Danh sách mã hàng hoá không duyệt: <mã>” và ô Lý do không duyệt.\n'
          '3. Nhập lý do, bấm “Không duyệt”.\n'
          '4. Hệ thống ghi từ chối (BR-13), ghi lịch sử, gửi thông báo.\n'
          '5. Thông báo “Đã không duyệt 1 yêu cầu.”; yêu cầu biến khỏi danh sách.',
    phu='• Lý do trống / chỉ có dấu cách → chữ đỏ “Vui lòng nhập lý do không duyệt”, popup không đóng.\n'
        '• Bấm Hủy / ✕ → không gửi.\n'
        '• Giá đã sửa trên màn KHÔNG được dùng khi Không duyệt (lịch sử ghi giá đề nghị gốc).\n'
        '• Yêu cầu vừa được người khác xử lý → “' + MSG_GONE + '”.\n'
        '• Lý do > 2000 ký tự → hệ thống từ chối; hiện tại popup đã đóng và thông báo hiện chữ tiếng Anh “The given data was '
        'invalid.” (lỗi của màn, xem mục ghi nhận).',
    dacbiet='Giá sửa trên màn Duyệt bị bỏ sau khi Không duyệt.')
d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Không duyệt', shot=shot('09-khong-duyet.png'),
         shot_caption='Popup Không duyệt giá bán (minh hoạ)')
d.layout(menu=MENU + ' => Không duyệt', shot=shot('10-khong-duyet-thieu-ly-do.png'),
         shot_caption='Bấm Không duyệt khi chưa nhập lý do: “Vui lòng nhập lý do không duyệt” (minh hoạ)')
d.layout(menu=MENU + ' => Không duyệt', shot=shot('11-khong-duyet-thanh-cong.png'),
         shot_caption='Thông báo “Đã không duyệt 1 yêu cầu.” (minh hoạ — lệnh bị chặn trên trình duyệt)')
d.layout(menu=MENU + ' => Không duyệt', shot=shot('20-ly-do-qua-dai.png'),
         shot_caption='Lý do > 2000 ký tự: thông báo tiếng Anh “The given data was invalid.” (phản hồi đúng của máy chủ, minh hoạ)')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Không duyệt (trên dòng)', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Nút đỏ, biểu tượng dấu ✕ tròn.', '- Tạm khoá khi đang xử lý thao tác khác.']),
    ('Popup – tiêu đề', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', '“Không duyệt giá bán” (1) / “Không duyệt giá bán hàng loạt” (nhiều).'),
    ('Popup – câu dẫn', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', [
        '- “Danh sách mã hàng hoá không duyệt: <mã 1>, <mã 2>…” (in đậm).',
        '- Hàng loạt: “Một lý do dùng chung cho cả <n> yêu cầu.”',
        '- “Giá đang áp dụng giữ nguyên; màn Cập nhật giá hiện badge "Không duyệt" kèm lý do.”']),
    ('Lý do không duyệt', 'Textarea', 'Enable', '1–2000 ký tự', 'Có', 'Trống', [
        '- Nhãn “Lý do không duyệt *”.',
        '- Trống → “Vui lòng nhập lý do không duyệt”; khoảng trắng đầu / cuối bị cắt.',
        '- > 2000 ký tự → máy chủ báo “Không được vượt quá 2000 ký tự” (màn hiện chưa hiện câu này — xem 2.5.2).']),
    ('Popup – nút Không duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Nút đỏ; xác nhận.'),
    ('Popup – nút Hủy / ✕', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng popup, không gửi.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     ['- “Đã không duyệt <n> yêu cầu.”', '- Không còn yêu cầu: “' + MSG_GONE + '”.']),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Không duyệt trên dòng', 'Click', 'Before:\n– Đang xử lý thao tác khác → bỏ qua.\nAfter:\n– Mở popup Không duyệt giá bán.'),
    ('Bấm Không duyệt ở popup', 'Click',
     'Before:\n– Lý do trống → “Vui lòng nhập lý do không duyệt”, giữ popup.\n'
     '– Kiểm quyền ' + Q1 + ' tại công ty đang làm việc; không có → “' + MSG_NOPERM + '”.\n'
     'During:\n– Lý do trống → “Vui lòng nhập lý do không duyệt”; > 2000 ký tự → “Không được vượt quá 2000 ký tự”.\n'
     '– Yêu cầu không còn / thuộc công ty khác → “' + MSG_GONE + '”.\n'
     'After:\n' + '\n'.join(REJECT_AFTER) + '\n– Hiển thị “Đã không duyệt 1 yêu cầu.”, tải lại danh sách.'),
    ('Bấm Hủy / ✕ ở popup', 'Click', 'After:\n– Đóng popup, không gửi.'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Duyệt / Không duyệt hàng loạt')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Duyệt / Không duyệt hàng loạt', 'action', actor=ACTOR,
            caption='Biểu đồ Use Case — FR-06 Duyệt / Không duyệt hàng loạt')
d.p('2.6.2 Giới thiệu')
d.rule_ref(NOTICE_RULE, anchor='notice')
d.intro_table(
    ten='Duyệt / Không duyệt hàng loạt',
    mota='Tick nhiều yêu cầu (kể cả ở nhiều trang, nhiều lần lọc) rồi Duyệt hoặc Không duyệt một lần. Duyệt hàng loạt áp '
         'ĐÚNG giá đã sửa của TỪNG yêu cầu; Không duyệt hàng loạt dùng 1 lý do chung.',
    tacnhan=ACTOR,
    dieukien='Có quyền ' + Q1 + ' tại công ty đang làm việc; đã tick ≥ 1 yêu cầu.',
    chinh='1. Tick ô đầu các yêu cầu (hoặc ô tiêu đề để chọn cả trang).\n'
          '2. Thanh hàng loạt hiện “Đã chọn <n> yêu cầu” + nút Duyệt, Không duyệt, Bỏ chọn.\n'
          '3. Bấm Duyệt → kiểm tra mọi ô của mọi yêu cầu đã chọn → popup “Duyệt giá bán hàng loạt” → bấm Duyệt.\n'
          '4. Hoặc bấm Không duyệt → popup “Không duyệt giá bán hàng loạt” → nhập 1 lý do → bấm Không duyệt.\n'
          '5. Hệ thống xử lý từng yêu cầu như mục 2.4 / 2.5 trong 1 giao dịch; thông báo kết quả; bỏ chọn các yêu cầu đã xử lý.',
    phu='• Yêu cầu đã chọn đang bị bộ lọc ẩn vẫn được xử lý; thanh hàng loạt ghi “(<k> đang ẩn do bộ lọc)”, popup ghi “(gồm cả '
        'yêu cầu đang ẩn do bộ lọc)”.\n'
        '• 1 yêu cầu có ô sai → không gửi yêu cầu nào; thông báo “<n> yêu cầu có ô chưa hợp lệ — sửa chữ đỏ rồi duyệt lại”.\n'
        '• Một số yêu cầu vừa được người khác xử lý → bỏ qua các yêu cầu đó, duyệt phần còn lại; thông báo “… <s> yêu cầu đã '
        'được người khác xử lý.” (Không duyệt hàng loạt không ghi số bị bỏ qua).\n'
        '• Bấm Bỏ chọn → bỏ tick mọi yêu cầu, ẩn thanh hàng loạt.',
    dacbiet='Khác ERP cũ: duyệt hàng loạt áp đúng giá đã sửa của từng yêu cầu (ERP cũ áp sai giá giữa các yêu cầu).')
d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Chọn yêu cầu', shot=shot('05-chon-hang-loat.png'),
         shot_caption='Tick 2 yêu cầu: thanh hàng loạt “Đã chọn 2 yêu cầu”, ô tiêu đề ở trạng thái nửa (minh hoạ)')
d.layout(menu=MENU + ' => Duyệt', shot=shot('07-xac-nhan-duyet-hang-loat.png'),
         shot_caption='Popup “Duyệt giá bán hàng loạt” (minh hoạ)')
d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Thanh hàng loạt', 'Label', 'Enable / Ẩn', '–', '–', 'Ẩn', [
        '- Bên phải tiêu đề bảng, chỉ hiện khi tick ≥ 1.',
        '- “Đã chọn <n> yêu cầu”; thêm “(<k> đang ẩn do bộ lọc)” khi có yêu cầu đã chọn không nằm trên trang / bộ lọc đang xem.']),
    ('Nút Duyệt (hàng loạt)', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Duyệt mọi yêu cầu đã chọn; khoá khi đang xử lý.'),
    ('Nút Không duyệt (hàng loạt)', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Không duyệt mọi yêu cầu đã chọn, 1 lý do chung.'),
    ('Nút Bỏ chọn', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tick tất cả (kể cả yêu cầu đang ẩn).'),
    ('Popup Duyệt hàng loạt', 'Modal', 'Hiển thị', '–', '–', 'Ẩn', [
        '- “Duyệt <n> yêu cầu giá bán đã chọn[ (gồm cả yêu cầu đang ẩn do bộ lọc)]:” + danh sách “<mã> – <tên> (<ĐVT>)”.',
        '- Cùng các khối nhắc giá hiệu lực dời ngày / giá đang chạy đã đổi như mục 2.4.']),
    ('Popup Không duyệt hàng loạt', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     ['- “Danh sách mã hàng hoá không duyệt: <mã>, <mã>…” + “Một lý do dùng chung cho cả <n> yêu cầu.”', '- Ô Lý do như mục 2.5.']),
    ('Lý do không duyệt (hàng loạt)', 'Textarea', 'Enable', '1–2000 ký tự', 'Có', 'Trống', 'Như mục 2.5.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
        '- “Đã duyệt <n> yêu cầu giá bán.” (+ số dòng giá đang chạy đã đổi, + số yêu cầu người khác đã xử lý).',
        '- “Đã không duyệt <n> yêu cầu.”']),
])
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Tick / bỏ tick 1 yêu cầu, ô tiêu đề', 'Change',
     'After:\n– Thêm / bớt yêu cầu khỏi danh sách đã chọn (giữ qua lọc, đổi trang); hiện / ẩn thanh hàng loạt.'),
    ('Bấm Duyệt (hàng loạt)', 'Click',
     'Before:\n– Chưa chọn → “Vui lòng chọn hàng hoá để duyệt”.\n'
     'During:\n– Kiểm đồng thời mọi ô của MỌI yêu cầu đã chọn (luật như mục 2.4); sai → “<n> yêu cầu có ô chưa hợp lệ — sửa chữ đỏ rồi duyệt lại”, 0 yêu cầu được gửi.\n'
     'After:\n– Popup xác nhận → Duyệt: mỗi yêu cầu áp đúng giá đã sửa của nó (mục 2.4); yêu cầu người khác vừa xử lý bị bỏ qua.\n'
     '– Không còn yêu cầu nào để duyệt → “' + MSG_GONE + '”.'),
    ('Bấm Không duyệt (hàng loạt)', 'Click',
     'Before:\n– Chưa chọn → “Vui lòng chọn hàng hoá để không duyệt”.\n'
     'After:\n– Popup lý do → Không duyệt: mỗi yêu cầu xử lý như mục 2.5 với cùng lý do.'),
    ('Bấm Bỏ chọn', 'Click', 'After:\n– Bỏ mọi tick; ẩn thanh hàng loạt.'),
])

# ------------------------------------------------------------------ 2.7
d.h3('2.7 Xuất Excel')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xuất Excel', 'io', actor=ACTOR, caption='Biểu đồ Use Case — FR-07 Xuất Excel')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Duyệt giá bán tại phần mô tả chi tiết.',
           anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách hàng chờ duyệt giá bán',
    mota='Tải file Excel “DANH SÁCH HÀNG CHỜ DUYỆT GIÁ BÁN” gồm MỌI yêu cầu khớp bộ lọc đang chọn (không theo trang), tối đa '
         '5.000 yêu cầu, có letterhead của công ty đang làm việc.',
    tacnhan=ACTOR,
    dieukien='Có quyền ' + Q1 + ' tại công ty đang làm việc.',
    chinh='1. Bấm “Xuất Excel” ở đầu khối bộ lọc.\n'
          '2. Trình duyệt tải trực tiếp file “danh_sach_hang_cho_duyet_gia_ban.xlsx”.',
    phu='• Không có yêu cầu → file chỉ có tiêu đề + dòng tên cột.\n'
        '• Không có quyền ' + Q2 + ' → file không có cột Giá vốn, Hệ số.\n'
        '• File ghi GIÁ ĐỀ NGHỊ gốc, không ghi giá người duyệt đang sửa trên màn.',
    dacbiet='Tải trực tiếp từ máy chủ (không qua bộ nhớ tạm của trình duyệt) để Safari / ứng dụng di động nhận đúng tên và '
            'đuôi file.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('04-loc-nang-cao.png'),
         shot_caption='Nút Xuất Excel ở đầu khối bộ lọc (minh hoạ)')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xuất Excel', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Viền xanh lá, biểu tượng Excel; xuất theo bộ lọc đang chọn.'),
    ('File – tiêu đề', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
     ['- Letterhead công ty đang làm việc ở đầu sheet.', '- Tiêu đề “DANH SÁCH HÀNG CHỜ DUYỆT GIÁ BÁN”.']),
    ('File – cột', 'Table/Grid', 'Read-only', '18 cột (16 khi không có quyền Xem giá vốn)', '–', 'Theo dữ liệu', [
        '- STT · Mã hàng hoá · Tên hàng hoá · ĐVT · Model · Hãng sản xuất · Loại sản phẩm · Giá vốn* · Loại giá · Giá cũ · Hệ số* · '
        'Giá mới · ĐMGG cũ (%) · ĐMGG mới (%) · Ngày hiệu lực · Lý do sửa giá · Người cập nhật · Thời gian (* chỉ khi có quyền '
        + Q2 + ').',
        '- Mỗi yêu cầu 1 khối, các cột của yêu cầu gộp dọc theo số dòng giá.',
        '- Dòng giá hiệu lực: Loại giá “<loại> — giá hiệu lực”, Giá cũ + ĐMGG cũ trống, Ngày hiệu lực dd/mm/yyyy; dòng giá hiện '
        'tại ghi “Đang áp dụng”.',
        '- Yêu cầu chỉ đổi giá vốn: Loại giá “Chỉ đổi giá vốn”.',
        '- Tiền là số thật có dấu ngăn nghìn; giá / ĐMGG bằng 0 vẫn ghi 0.']),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Kiểm quyền ' + Q1 + ' tại công ty đang làm việc; không có → hệ thống từ chối.\n'
     'During:\n– Lấy mọi yêu cầu của công ty khớp từ khoá + ô lọc (+ lọc theo thông báo nếu có), mới cập nhật lên trước, tối đa 5.000.\n'
     'After:\n– Trả file “danh_sach_hang_cho_duyet_gia_ban.xlsx”.'),
])

# ------------------------------------------------------------------ 2.8
d.h3('2.8 Xem lịch sử giá')
d.p('2.8.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn Duyệt giá bán tại phần mô tả chi tiết.',
           anchor='history')
d.intro_table(
    ten='Xem lịch sử giá bán',
    mota='Popup xem các lần thay đổi bộ giá của hàng TẠI CÔNG TY ĐANG LÀM VIỆC (mọi ĐVT): Cập nhật giá, Gửi duyệt giá, Duyệt '
         'giá, Không duyệt giá — dùng chung popup với màn Cập nhật giá bán.',
    tacnhan=ACTOR,
    dieukien='Có quyền ' + Q1 + ' tại công ty đang làm việc.',
    chinh='1. Bấm nút Lịch sử giá (biểu tượng đồng hồ) ở ô Tên hàng hoá.\n'
          '2. Hệ thống mở popup “Lịch sử giá bán: <tên hàng>”, các lần thay đổi xếp mới → cũ.\n'
          '3. (Tuỳ chọn) bấm Bộ lọc để lọc theo loại hành động, người thực hiện, khoảng ngày.',
    phu='• Chưa có lần thay đổi nào → “Chưa có lịch sử thao tác nào.”.\n'
        '• Không có quyền ' + Q2 + ' và cũng không có quyền ' + Q3 + ' → không có dòng Giá vốn và hệ số trong lịch sử.\n'
        '• Lịch sử của công ty khác KHÔNG hiện.')
d.p('2.8.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử giá', shot=shot('16-lich-su-gia.png'),
         shot_caption='Popup Lịch sử giá bán mở từ màn Duyệt giá bán (dữ liệu thật — hàng chưa có lịch sử)')
d.layout(menu=MENU + ' => Lịch sử giá', shot=shot('16b-lich-su-gia-g4.png'),
         shot_caption='Cùng popup khi đã có lịch sử (ảnh thật chụp lúc kiểm thử 10/10/2026 ở màn Cập nhật giá bán)')
d.p('2.8.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Lịch sử giá bán: <tên hàng>', 'Chỉ tên hàng, không kèm mã.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Đóng', [
        '- Mở các ô lọc, chọn là lọc luôn.',
        '- Loại hành động: Tạo mới / Thay đổi thông tin / Thay đổi trạng thái (Duyệt / Không duyệt thuộc Thay đổi trạng thái).',
        '- Người thực hiện: nhân sự của công ty đang làm việc.',
        '- Từ ngày / Đến ngày.']),
    ('Mỗi lần thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
        '- Thời điểm dd/mm/yyyy hh:mm; nhãn hành động “Cập nhật giá”, “Gửi duyệt giá”, “Duyệt giá” (xanh lá), “Không duyệt '
        'giá” (đỏ).',
        '- “Người thực hiện: <tên> — <phòng ban>”.',
        '- Ghi chú “Lý do không duyệt: <lý do>” ở lần Không duyệt.']),
    ('Chi tiết thay đổi', 'Text', 'Read-only', '–', 'Theo dữ liệu', [
        '- Dòng giá đặt tên “<Loại giá> (<ĐVT>)”, “Giá vốn (<ĐVT>)”, “<Loại giá> · giá hiệu lực (<ĐVT>)”; “giá trị cũ → giá trị mới”.',
        '- Lần Duyệt: giá trước → giá sau khi áp. Lần Không duyệt: giá đang áp dụng → giá đề nghị bị từ chối.',
        '- Không có quyền Xem giá vốn (và không có quyền Cập nhật giá bán): bỏ hẳn dòng Giá vốn và trường Hệ số.']),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thao tác nào.” / “Không có lịch sử phù hợp bộ lọc.”'),
    ('Nút Đóng / ✕', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng popup, không ảnh hưởng giá đang sửa trên bảng.'),
], required=False)
d.p('2.8.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Lịch sử giá', 'Click',
     'Before:\n– Kiểm quyền ' + Q1 + '; không có → “' + MSG_NOPERM + '”.\n'
     'During:\n– Lấy lịch sử của hàng × công ty đang làm việc; công ty chưa dùng hàng → rỗng.\n'
     '– Không có cả quyền ' + Q2 + ' lẫn ' + Q3 + ' → bỏ giá vốn và hệ số khỏi lịch sử.\n'
     'After:\n– Hiện timeline mới → cũ.'),
    ('Chọn ô lọc trong popup', 'Change', 'After:\n– Lọc ngay danh sách lịch sử.'),
    ('Bấm Đóng', 'Click', 'After:\n– Đóng popup.'),
])

# ========================================================= PHAN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('chỉ ghi các quy tắc đặc thù của duyệt giá bán theo công ty; quy tắc dùng chung không nhắc lại.',
           anchor='list', head='Quy tắc áp dụng', lead='Ngoài SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi màn = yêu cầu của công ty đang làm việc',
     ['– Chỉ yêu cầu duyệt giá đang chờ có công ty bộ giá = công ty đang làm việc, của mọi người đề nghị.',
      '– Công ty lấy từ phiên làm việc, không nhận từ màn hình; yêu cầu của công ty khác không hiện, không duyệt được (hệ '
      'thống trả “' + MSG_GONE + '”, không lộ là có yêu cầu).',
      '– Mới cập nhật lên trước; 20 yêu cầu / trang (tối đa 50).'], ['Mọi chức năng']),
    ('BR-02', 'Quyền xét theo công ty đang làm việc',
     ['– Mọi chức năng cần quyền ' + Q1 + ' ĐƯỢC GÁN Ở công ty đang làm việc.',
      '– Không có quyền: ẩn 2 mục menu, màn không hiển thị và không tải dữ liệu; gọi thẳng chức năng bị từ chối.',
      '– Super admin không được miễn.'], ['Mọi chức năng']),
    ('BR-03', 'Bốn lối vào cùng phạm vi',
     ['– Tài chính › Quản lý giá - CTKM › Giá bán › Duyệt giá bán; Tài chính › Chờ duyệt › Giá bán chờ duyệt › Hàng hoá chờ duyệt '
      'giá bán; thông báo “[GIA] Chờ duyệt”; ERP Chờ duyệt › Duyệt giá bán (HRM).',
      '– Cùng 1 màn, cùng phạm vi; riêng thông báo của 1 yêu cầu lọc sẵn đúng yêu cầu đó (bỏ khi Tìm kiếm / lọc / Làm mới).'],
     ['Xem danh sách']),
    ('BR-04', 'GIÁ — Quyền Xem giá vốn che giá vốn + hệ số',
     ['– Không có quyền ' + Q2 + ': hệ thống KHÔNG gửi giá vốn đề nghị, giá vốn cũ, hệ số cũ / mới về màn hình và file Excel '
      '(hệ số × giá vốn = giá → suy ngược được giá vốn); bảng ẩn cột Giá vốn, Hệ số.',
      '– Khi duyệt, hệ số giữ nguyên bản đề nghị (không nhận hệ số từ màn hình) kể cả khi người duyệt sửa giá.',
      '– Quyền Cập nhật giá bán hàng hoá KHÔNG mở cột giá vốn ở màn này (chỉ mở giá vốn trong popup Lịch sử).'],
     ['Xem danh sách', 'Sửa giá đề nghị', 'Duyệt', 'Xuất Excel', 'Lịch sử']),
    ('BR-05', 'GIÁ — Người duyệt được sửa giá đề nghị',
     ['– Sửa được Giá mới, ĐMGG mới, ngày hiệu lực (và Hệ số khi có quyền Xem giá vốn) của từng dòng giá.',
      '– Không sửa được giá vốn đề nghị, không thêm / bớt dòng giá.',
      '– Sửa 1 dòng không lan sang dòng khác (khác màn Cập nhật giá bán: không có Bán lẻ lan, không tự tính TMĐT).'],
     ['Sửa giá đề nghị']),
    ('BR-06', 'GIÁ — Hệ số → Giá (làm tròn trăm)',
     ['– Gõ hệ số → Giá mới = làm tròn tới trăm của (hệ số × GIÁ VỐN ĐỀ NGHỊ), áp cho cả dòng giá hiệu lực.',
      '– Vd giá vốn 195.989.760, hệ số 1,75 → 342.982.100; giá vốn 1.457.500, hệ số 2,2 → 3.206.500.',
      '– Lưu ý: màn Cập nhật giá bán tính giá hiệu lực làm tròn tới ĐỒNG; cùng hệ số nhưng duyệt có sửa hệ số sẽ ra số tròn trăm.'],
     ['Sửa giá đề nghị']),
    ('BR-07', 'GIÁ — Duyệt áp giá người duyệt gửi',
     ['– Mỗi dòng giá đang áp dụng: Giá / Hệ số / ĐMGG trên màn (đã sửa hoặc nguyên đề nghị) thành giá đang áp dụng của loại '
      'giá tại công ty của yêu cầu; ĐMGG trống → 0; xoá cờ Chờ duyệt.',
      '– Chỉ ghi dòng giá của đúng công ty yêu cầu; không đụng giá công ty khác.',
      '– Duyệt hàng loạt: mỗi yêu cầu áp đúng giá của nó (sửa lỗi ERP cũ).'], ['Duyệt', 'Hàng loạt']),
    ('BR-08', 'GIÁ — Giá hiệu lực khi duyệt',
     ['– Ngày hiệu lực trước ngày mai (hôm nay hoặc đã qua) → dời về NGÀY MAI; màn nhắc trước dưới ô và trong popup.',
      '– Giá hiệu lực đã bị xoá / đã được áp trước lúc duyệt → bỏ qua dòng đó, các dòng khác vẫn áp.',
      '– Ngày áp dụng ghi trong thông báo Đã duyệt: hôm nay nếu có dòng giá hiện tại, ngược lại là ngày hiệu lực sớm nhất.'],
     ['Duyệt', 'Hàng loạt']),
    ('BR-09', 'GIÁ — Giá đang chạy đã đổi sau khi đề nghị',
     ['– Giá cũ (lúc đề nghị) ≠ giá đang chạy (Phiếu tính giá / tác vụ hằng đêm đã đổi) → VẪN duyệt theo giá trên màn.',
      '– Popup cảnh báo “<mã>: giá đang chạy <giá> (lúc đề nghị <giá>)”; thông báo kết quả thêm “Có n dòng giá đang chạy đã '
      'đổi trước khi duyệt.”.',
      '– Chênh lệch dưới ô Giá mới luôn so với Giá cũ (lúc đề nghị), không so với giá đang chạy.'], ['Duyệt', 'Hàng loạt']),
    ('BR-10', 'GIÁ — Giá vốn đề nghị',
     ['– Duyệt → giá vốn của ĐVT tại công ty = giá vốn đề nghị (kể cả khi người duyệt không thấy giá vốn).',
      '– Yêu cầu chỉ đổi giá vốn hiện 1 dòng “Chỉ đổi giá vốn — không đổi giá bán”; “Cũ: <giá vốn đang chạy>” khi khác.',
      '– Không đổi hệ số quy đổi của ĐVT.'], ['Xem danh sách', 'Duyệt']),
    ('BR-11', 'Trạng thái hàng khi duyệt / không duyệt',
     ['– Chỉ khi công ty của yêu cầu là công ty quản lý hàng VÀ hàng đang ở trạng thái chờ duyệt cũ của ERP: Duyệt → hàng chuyển '
      'Đang kinh doanh tại công ty đó (kèm đủ bộ giá mọi ĐVT); Không duyệt → trạng thái Không duyệt.',
      '– Hàng đang kinh doanh / ngừng kinh doanh: không đổi trạng thái.',
      '– Lưu ý: duyệt KHÔNG kiểm trạng thái hàng — hàng bị khoá / Ngừng kinh doanh sau khi gửi đề nghị vẫn được áp giá.'],
     ['Duyệt', 'Không duyệt']),
    ('BR-12', 'Kiểm tra ô báo đồng thời',
     ['– Bấm Duyệt (đơn / hàng loạt): mọi ô sai của mọi yêu cầu được chọn báo đỏ cùng lúc, cuộn tới ô sai đầu tiên, không gửi.',
      '– Câu chữ: “Bắt buộc phải nhập”, “Không hợp lệ”, “Không được vượt quá 12 chữ số”, “Không được vượt quá 2 chữ số trước '
      'dấu phẩy”, “Phải từ 0 đến 100”, “Bắt buộc phải chọn”, “Ngày không hợp lệ”.',
      '– Máy chủ kiểm lại cùng luật (bỏ qua dòng không thuộc yêu cầu).'], ['Duyệt', 'Hàng loạt']),
    ('BR-13', 'Không duyệt — lý do bắt buộc',
     ['– Lý do bắt buộc (cắt khoảng trắng đầu / cuối), tối đa 2000 ký tự; hàng loạt dùng 1 lý do chung.',
      '– Giá đang áp dụng giữ nguyên; ô đang Chờ duyệt chuyển cờ Không duyệt; ghi “Lý do không duyệt” + thời điểm vào ĐVT tại '
      'công ty; giá sửa trên màn Duyệt không được dùng.',
      '– Màn Cập nhật giá bán hiện nhãn “Không duyệt” + “Lý do không duyệt: <lý do>”.'], ['Không duyệt', 'Hàng loạt']),
    ('BR-14', 'Xử lý xong là xoá yêu cầu',
     ['– Duyệt / Không duyệt xong → xoá hẳn yêu cầu khỏi danh sách chờ (vết còn ở lịch sử giá).',
      '– Yêu cầu không còn (đã xử lý, người đề nghị lưu thẳng, gỡ / xoá hàng) → “' + MSG_GONE + '”; mở từ thông báo cũ → cảnh '
      'báo “Yêu cầu đã được xử lý”.'], ['Duyệt', 'Không duyệt', 'Xem danh sách']),
    ('BR-15', 'Thao tác đồng thời',
     ['– Mỗi lần duyệt / không duyệt chạy trong 1 giao dịch, khoá yêu cầu đang xử lý.',
      '– Hai người cùng xử lý 1 yêu cầu: người sau nhận “' + MSG_GONE + '” (đơn) hoặc yêu cầu bị bỏ qua (hàng loạt — “<s> yêu cầu '
      'đã được người khác xử lý.”).',
      '– Người đề nghị gửi lại đề nghị mới trong lúc người duyệt đang sửa → lần tải lại sau sẽ bỏ giá đã sửa, hiện bản mới.'],
     ['Duyệt', 'Không duyệt', 'Hàng loạt']),
    ('BR-16', 'Thông báo 2 chiều',
     ['– Gửi đề nghị → “[GIA] Chờ duyệt: <mã> – <tên>. Người đề nghị: <tên>” tới mọi người có quyền ' + Q1 + ' TẠI công ty bộ giá.',
      '– Duyệt → “[GIA] Đã duyệt: <mã> – <tên>. Giá mới áp dụng từ <ngày>” tới người đề nghị; mở ra màn Cập nhật giá bán lọc '
      'đúng hàng.',
      '– Không duyệt → “[GIA] Từ chối: <mã> – <tên>. Lý do: <lý do>”; mở ra màn Cập nhật giá bán lọc Không duyệt.',
      '– Tên hàng tối đa 50 ký tự, cả câu tối đa 120 ký tự (cắt phần ghi chú trước). Lỗi gửi thông báo không làm hỏng thao tác.'],
     ['Duyệt', 'Không duyệt']),
    ('BR-17', 'Yêu cầu sinh từ Phiếu tính giá',
     ['– Phiếu tính giá gửi duyệt → 1 thông báo gộp “[GIA] Chờ duyệt: <mã phiếu>. <n> dòng giá. Người đề nghị: <tên>”; các yêu '
      'cầu hiện trên màn như yêu cầu thường.',
      '– Duyệt 1 dòng → dòng của phiếu ghi “đã duyệt” + giá thực áp; Không duyệt → “bị từ chối” + lý do.',
      '– Mọi dòng của phiếu đã duyệt → phiếu Đã duyệt, hàng mới chuyển Đang kinh doanh (khi đủ mọi ĐVT), báo “[PTG] Đã duyệt”; '
      'có dòng bị từ chối và không còn dòng chờ → phiếu Giá bị từ chối, báo “[PTG] Từ chối”.',
      '– Không gửi “[GIA] Đã duyệt / Từ chối” từng dòng cho yêu cầu của phiếu.'], ['Duyệt', 'Không duyệt']),
    ('BR-18', 'Quy định duyệt giá không ảnh hưởng màn Duyệt',
     ['– Bật / tắt duyệt giá, phạm vi hãng chỉ quyết định lúc gửi (màn Cập nhật giá bán).',
      '– Công ty tắt duyệt giá khi còn yêu cầu chờ: yêu cầu vẫn hiện và duyệt được; nếu người đề nghị lưu thẳng ở màn Cập nhật '
      'giá bán thì yêu cầu bị đóng.'], ['Xem danh sách', 'Duyệt']),
    ('BR-19', 'Ô tick giữ qua lọc và đổi trang',
     ['– Ô đã tick và giá đã sửa giữ nguyên khi lọc lại, Tìm kiếm, Làm mới, đổi trang.',
      '– Hàng loạt xử lý cả yêu cầu đang bị bộ lọc ẩn và báo rõ số yêu cầu ẩn.'], ['Hàng loạt', 'Tìm kiếm và lọc']),
    ('BR-20', 'Cảnh báo chưa lưu',
     ['– Có giá đã sửa khác bản đề nghị mà rời màn → hỏi “Thông tin chưa lưu” (Thoát / Ở lại); tải lại / đóng tab → hộp thoại '
      'của trình duyệt.'], ['Sửa giá đề nghị']),
    ('BR-21', 'Lịch sử giá',
     ['– Duyệt ghi “Duyệt giá” (giá trước → giá sau); Không duyệt ghi “Không duyệt giá” (giá đang áp dụng → giá đề nghị) + lý do.',
      '– Chỉ xem được lịch sử của công ty đang làm việc; giá vốn + hệ số trong lịch sử ẩn khi không có cả quyền ' + Q2 + ' lẫn '
      + Q3 + '.'], ['Lịch sử']),
    ('BR-22', 'Xuất Excel',
     ['– Mọi yêu cầu khớp bộ lọc (không theo trang), tối đa 5.000; giá đề nghị gốc; letterhead công ty đang làm việc.',
      '– Không có quyền ' + Q2 + ' → bỏ cột Giá vốn, Hệ số.'], ['Xuất Excel']),
])

# update_fields=False: may dang mo Microsoft Word cua user — buoc cap nhat muc luc tren macOS se dong Word.
# Muc luc cap nhat bang tay: chuot phai -> Update Field.
d.save(update_fields=os.environ.get('SRS_UPDATE_TOC') == '1')
print('OK ->', OUT)

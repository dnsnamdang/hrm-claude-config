# -*- coding: utf-8 -*-
"""SRS màn "Thẻ kho" (phân hệ Kho › Báo cáo kho) — màn BÁO CÁO chỉ đọc, form chuẩn, chuẩn 04/11/2026.

Chạy: python gen_srs.py  → SRS - Thẻ kho.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc
  ../kiem-ke-theo-hang-hoa/gen_srs.py (06/11, Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột) và cách viết màn báo cáo
  ../report-limit-debts/gen_srs.py (2.x.6 Cách lấy dữ liệu, bảng popup, Mục đích thiết kế popup).
Nguồn đọc 06/11/2026 (nhánh develop cả 2 repo):
  BE  Modules/Finance/{Services/StockCardReportService.php, Services/StockCardPrintService.php, Services/WarehouseStockReportService.php
      (period / positionIdsOf / structureOf), Http/Controllers/V1/StockCardController.php, Exports/StockCardExport.php,
      Resources/views/{exports/stock_card, prints/stock-card}.blade.php, Routes/api.php (nhóm stock-card, không gắn middleware)},
      PhysicalStockWriter + các nơi gọi (WarehouseImportWriteService, Assign WarehouseExportService, PositionTransferWriteService,
      WarehouseReExportService, WarehouseInventory{Import,Export}WriteService, Assign WarehouseReImport, BeginningStockService),
      PermissionsTableSeeder (nhóm "Báo cáo kho": Thủ kho, Xem báo cáo tồn kho theo tổng công ty).
  FE  pages/warehouse/stock-card/{index.vue, components/{StockCardSummary, StockCardTable, ExportModeModal}.vue, format.js,
      voucher-link.js}, V2BaseSmartFilterPanel + filter-customization-modal, V2ProductPickerModal, V2BaseReportPrintModal,
      ReportPrintPreviewModal + reportPrintPreviewMixin, ScopePicker, filterStateMixin, components/subsystem-menu/warehouse.js.
  Bối cảnh: design.md, plan.md (Phase 1, Phase 2, Fix sau duyệt, #11866), spec docs/superpowers/specs/gop-db/2026-10-22-the-kho-design.md.
Ảnh: ./tk_shots — dev-hrm 06/11/2026, DNS Admin (_capture/capture.js chặn mọi yêu cầu ghi: 0 yêu cầu ghi). Hàng ENEO-640-V5236,
  công ty TPE, Kỳ Năm nay. Ảnh màn chính / bung lô / điều chuyển chụp khung 1920px để thấy đủ 9 cột. Không giả trạng thái nào.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
HRM = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(HRM, '.claude', 'skills', 'srs-documenter', 'assets'))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from srs_docx_lib import SrsDoc  # noqa: E402
from srs_split_rows import split_ui_rows  # noqa: E402

TEN = 'Thẻ kho'
SHOTS = os.path.join(HERE, 'tk_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Kho => Báo cáo kho => Thẻ kho'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Thẻ kho.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
Q1 = 'Thủ kho'
V1 = 'Xem báo cáo tồn kho theo tổng công ty'
NOPERM = '“Bạn không có quyền truy cập chức năng này.”'
M_PRODUCT = '“Vui lòng chọn hàng hóa”'
M_COMPANY = '“Vui lòng chọn tồn theo công ty”'
M_RANGE = '“Vui lòng chọn đủ từ ngày và đến ngày”'
M_RANGE_BE = '“Vui lòng chọn đủ Từ ngày và Đến ngày”'
M_RANGE_ORDER = '“Ngày kết thúc phải sau hoặc bằng ngày bắt đầu”'
E_NOPRODUCT = '“Chọn hàng hóa để xem thẻ kho.”'
E_NOCOMPANY = '“Chọn công ty để xem thẻ kho.”'
E_NORANGE = '“Chọn đủ từ ngày và đến ngày để xem thẻ kho.”'
E_EMPTY = '“Không có chứng từ nào khớp bộ lọc.”'
E_LOAD = '“Lỗi khi tải dữ liệu.”'
E_LOADING = '“Đang tải dữ liệu...”'
M_NOPRINT = '“Không có dữ liệu để in”'
M_EXPORT_ERR = '“Lỗi khi xuất Excel.”'
M_LIMIT = ('“Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, '
           'trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.”')
TIP_PURPOSE = ('MỤC ĐÍCH BÁO CÁO • Theo dõi nhập, xuất, tồn của 1 mặt hàng theo từng chứng từ trong kỳ • Phạm vi: công ty, kho, '
               'công ty thuê kho, nhà / dãy / khoang / vị trí đang lọc • Mỗi chứng từ bung ra được từng lô / vị trí phát sinh')
TIP_GOAL = ('THẺ KHO • Nhập, xuất, tồn của 1 mặt hàng theo từng chứng từ trong kỳ, tại các kho / vị trí đang lọc • Số lượng quy '
            'theo ĐVT đang chọn ở bộ lọc • Số liệu tính tại <ngày giờ>')
TIP_QTY = ('SỐ LƯỢNG • Tồn đầu kỳ: tổng thay đổi tồn theo vị trí trước ngày đầu kỳ • Nhập / Xuất trong kỳ: tính cả điều chuyển vị '
           'trí (như ERP); Loại báo cáo "Không nhặt điều chuyển" thì bỏ • Tồn cuối kỳ = Tồn đầu kỳ + Nhập trong kỳ - Xuất trong kỳ')
TIP_VOUCHER = ('CHỨNG TỪ • Đếm số chứng từ phát sinh trong kỳ (mỗi phiếu 1 lần) • Nhập: phiếu nhập kho, nhập tồn đầu, nhập lại, '
               'nhập điều chỉnh kiểm kê • Xuất: phiếu xuất kho, xuất lại, xuất điều chỉnh kiểm kê')
TIP_TOTAL = ('TỔNG PHÁT SINH • Nhập / Xuất: tổng trong kỳ, không tính điều chuyển vị trí (như ERP) • SL tồn: tồn cuối kỳ • Tính '
             'trên toàn thẻ kho đã lọc, không theo trang')
TIP_IMP = 'NHẬP • Dòng chứng từ: tổng nhập của phiếu (điều chuyển: tổng chuyển vào) • Dòng lô: số nhập vào vị trí'
TIP_EXP = 'XUẤT • Dòng chứng từ: tổng xuất của phiếu (điều chuyển: tổng chuyển ra) • Dòng lô: số xuất khỏi vị trí'
TIP_SL = 'SL TỒN • Tồn đầu kỳ + cộng dồn mọi thay đổi tới hết chứng từ này'
TIP_NVKD = 'NVKD • Người lập yêu cầu của chứng từ - mã phòng ban'
H_KY = 'Lọc theo ngày phát sinh của chứng từ (ngày ghi nhận vào thẻ kho).'
H_KHO = 'Bỏ trống = toàn bộ kho của công ty'
H_RENTAL = 'Chọn kho trước. Bỏ trống = mọi công ty thuê của các kho đã chọn'
H_KW = 'Gõ rồi Enter hoặc bấm Tìm kiếm. Chỉ lọc dòng trong bảng — khối tổng hợp và SL tồn giữ nguyên.'

A_TK = 'Thủ kho'
TN = ('Người dùng có quyền thực hiện chức năng: “%s” (hoặc Super admin); chọn được công ty khác ở ô Tồn theo công ty khi có thêm '
      'quyền “%s”.' % (Q1, V1))
DK = ('1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền “%s” (hoặc là Super admin).\n'
      '3. Người dùng đang ở màn Thẻ kho (phân hệ Kho › Báo cáo kho).' % Q1)
DK_REPORT = DK + '\n4. Đã chọn Hàng hóa và Tồn theo công ty, kỳ hợp lệ — bảng đang hiển thị thẻ kho.'

d = SrsDoc(out=OUT, menu=MENU, route='/warehouse/stock-card', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Kho': 'menu_phanhe', 'Báo cáo kho': 'menu_nhom', 'Thẻ kho': 'menu_muc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Hàng hóa': 'o_hanghoa',
    'Bung chứng từ': 'btn_caret', 'Số chứng từ': 'link_sochungtu', 'In danh sách': 'btn_in_list', 'Xuất Excel': 'btn_xuatexcel',
}.items()})

UI_OVER = {}
UI_EXPLICIT = {}


def uc(code, name, group, actor):
    """Biểu đồ Use Case 1 chức năng theo khổ mẫu quốc gia (actor + 1 use case)."""
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None, extra=None):
    """Một chức năng 2.x: (Biểu đồ Usecase) · Giới thiệu · Layout · Mô tả giao diện · Event. Trả số mục con kế tiếp."""
    d.h3('2.%d %s' % (no, title))
    k = 1
    if usecase:
        d.p('2.%d.%d Biểu đồ Usecase' % (no, k))
        uc(*usecase)
        k += 1
    d.p('2.%d.%d Giới thiệu' % (no, k))
    tail, anchor = rule
    d.rule_ref(tail + ' ' + RIENG, anchor=anchor)
    d.intro_table(**intro)
    k += 1
    d.p('2.%d.%d Layout màn hình' % (no, k))
    d.layout(**layout)
    for img, cap in (extra or []):
        d.figure(img, cap, width_in=6.2)
    k += 1
    assert ui and ev, 'Thiếu bảng giao diện / event ở 2.%d' % no
    d.p('2.%d.%d Mô tả chi tiết giao diện' % (no, k))
    d.ui_table(split_ui_rows(ui, UI_OVER, UI_EXPLICIT), **(ui_kw or {}))
    k += 1
    d.p('2.%d.%d Danh sách event và xử lý event' % (no, k))
    d.event_table(ev)
    return k + 1


# ============================================================== TRANG ĐẦU
d.title_block(TEN)
d.doc.add_page_break()  # Mục lục sang trang riêng như bản Drive đã chuẩn hoá
d.h2('Mục lục')
d.doc.paragraphs[-1].alignment = 1  # căn giữa chữ 'Mục lục'
d.toc()

# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Thẻ kho thuộc phân hệ Kho, nhóm Báo cáo kho (chuyển từ hệ thống ERP: Kho › '
    'Báo cáo kho › Thẻ kho), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu báo cáo theo dõi nhập, xuất, tồn của MỘT mặt hàng theo từng chứng từ trong một kỳ, tại các kho / vị trí '
    'của một công ty: tồn đầu kỳ, nhập trong kỳ, xuất trong kỳ, tồn cuối kỳ và số lượng tồn lũy kế sau từng chứng từ.',
    'Ghi rõ công thức, nguồn dữ liệu từng cột, điều kiện chứng từ được tính và các điểm KHÁC hệ thống ERP có chủ đích, để người '
    'nghiệm thu đối soát được từng con số với chứng từ nguồn và với các báo cáo tồn kho khác.',
])
d.p('Phạm vi chức năng (7 chức năng, đặc tả ở Phần 3):')
d.bullets([
    'Xem thẻ kho: khối tổng hợp (Số lượng, Chứng từ) + bảng chi tiết báo cáo 2 cấp Chứng từ ▸ Lô / vị trí, dòng TỔNG, phân trang.',
    'Tìm kiếm và lọc: Kỳ (Tuần này / Tháng này / Năm nay / Năm trước / Tuỳ chọn), Hàng hóa (bắt buộc), Tồn theo công ty (bắt buộc), '
    'Kho, Công ty thuê kho, Loại báo cáo, Số chứng từ / Diễn giải, Nhà / Dãy / Khoang / Vị trí; Cài đặt bộ lọc.',
    'Chọn hàng hóa qua cửa sổ “Chọn hàng hóa” dùng chung.',
    'Xem chi tiết chứng từ và lô / vị trí: bung từng chứng từ hoặc chọn cấp bung cho cả bảng; bấm Số chứng từ mở màn chứng từ nguồn ở '
    'tab mới.',
    'In thẻ kho (Đầy đủ / Rút gọn, chọn cột) và Xuất Excel (Đầy đủ / Rút gọn).',
    'Không thuộc màn này: màn chỉ đọc — không có Thêm mới, Chỉnh sửa, Xóa, Duyệt / Không duyệt, Khóa / Mở khóa, Import Excel, '
    'Lịch sử thay đổi và không có Tùy chỉnh cột (khuôn báo cáo đã bỏ, người dùng chốt 22/10/2026). Số liệu thay đổi do các chứng từ '
    'kho ở màn khác (Phần 5).',
])
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Thủ kho / kế toán kho tra lịch sử biến động của một mặt hàng: chứng từ nào nhập, chứng từ nào xuất, vào ngày nào, lô nào, vị trí '
    'nào, ai lập yêu cầu, còn tồn bao nhiêu sau mỗi chứng từ.',
    'Đối chiếu tồn sổ sách với tồn thực tế khi kiểm kê; truy nguyên chênh lệch bằng cách bấm số chứng từ mở chứng từ nguồn.',
    'In / xuất file thẻ kho để lưu hồ sơ, gửi kiểm toán hoặc đối chiếu với nhà cung cấp, khách hàng.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Nguồn số liệu là nhật ký thay đổi tồn kho theo VỊ TRÍ của hàng (mỗi lần một chứng từ cộng / trừ tồn tại một vị trí ghi một '
    'dòng). Chứng từ chỉ lên thẻ kho khi đã ghi tồn (phiếu nhập / xuất kho từ lúc gửi, điều chuyển vị trí khi Đã chuyển…), không xét '
    'trạng thái duyệt sau đó.',
    'Tồn cuối kỳ = Tồn đầu kỳ + Nhập trong kỳ − Xuất trong kỳ; SL tồn từng dòng = tồn đầu kỳ + cộng dồn mọi thay đổi tới hết chứng từ.',
    'Nhập / Xuất trong kỳ TÍNH CẢ điều chuyển vị trí (khớp số hệ thống ERP, người dùng chốt 22/10/2026); Loại báo cáo “Không nhặt '
    'điều chuyển” thì bỏ hẳn dòng điều chuyển.',
    'Một nguồn số cho màn hình, bản in và file Excel. Mọi số lượng theo đơn vị tính (ĐVT) cơ sở của hàng.',
    'Phải có quyền “%s” mới xem được; không có quyền “%s” thì chỉ xem công ty của mình.' % (Q1, V1),
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Thẻ kho', 'Báo cáo biến động nhập – xuất – tồn của 1 mặt hàng theo từng chứng từ trong kỳ, tại phạm vi kho / vị trí đã lọc.'),
    ('Chứng từ', 'Phiếu làm thay đổi tồn kho: phiếu nhập kho, phiếu xuất kho, phiếu điều chuyển vị trí, phiếu nhập lại, phiếu xuất '
                 'điều chỉnh sai số liệu (xuất lại), phiếu nhập / xuất kho điều chỉnh kiểm kê, khai báo tồn kho đầu kỳ.'),
    ('Nhập tồn đầu', 'Dòng tồn do khai báo tồn kho đầu kỳ; số chứng từ hiển thị dạng NHAP_TON_DAU_<số>, diễn giải “Nhập tồn đầu”, '
                     'không có liên kết.'),
    ('Lô / vị trí', 'Một lần thay đổi tồn của một lô hàng (số lô) tại một vị trí kho (mã vị trí). Một chứng từ có 1 hoặc nhiều lô / '
                    'vị trí.'),
    ('Tồn đầu kỳ', 'Tổng mọi thay đổi tồn của hàng trong phạm vi lọc xảy ra TRƯỚC ngày đầu kỳ.'),
    ('Nhập / Xuất trong kỳ', 'Tổng thay đổi dương / tổng trị tuyệt đối thay đổi âm trong kỳ, gồm cả chuyển vào / chuyển ra của điều '
                             'chuyển vị trí.'),
    ('Tồn cuối kỳ', 'Tồn đầu kỳ + Nhập trong kỳ − Xuất trong kỳ = SL tồn của chứng từ cuối cùng trong kỳ.'),
    ('SL tồn (lũy kế)', 'Số tồn sau khi cộng dồn tới hết từng chứng từ, theo thứ tự thời điểm ghi nhận.'),
    ('Kỳ', 'Khoảng ngày báo cáo: Tuần này, Tháng này, Năm nay (mặc định, 01/01 → 31/12), Năm trước, Tuỳ chọn (Từ ngày → Đến ngày).'),
    ('Tồn theo công ty', 'Công ty có tồn cần xem. Không chọn kho → chỉ tính tồn ghi nhận cho chính công ty này.'),
    ('Công ty thuê kho', 'Công ty có kho kế toán gắn với kho vật lý đã chọn; tồn của hàng được ghi nhận theo từng công ty thuê kho.'),
    ('Điều chuyển vị trí', 'Chứng từ chuyển hàng giữa các vị trí trong kho: mỗi lô có 1 dòng chuyển ra (âm) và 1 dòng chuyển vào '
                           '(dương); dòng chứng từ hiện tổng chuyển vào ở cột Nhập, tổng chuyển ra ở cột Xuất.'),
    ('Không nhặt điều chuyển', 'Giá trị ô Loại báo cáo: bỏ mọi dòng điều chuyển vị trí khỏi số liệu và bảng.'),
    ('NVKD', 'Người lập yêu cầu của chứng từ, kèm mã phòng ban (“Họ tên - Mã phòng ban”).'),
    ('ĐVT cơ sở', 'Đơn vị tính có hệ số nhỏ nhất của hàng (vd Can 4L); mọi số lượng trên màn, bản in, Excel quy theo đơn vị này.'),
    ('Trạng thái bản ghi', 'Dòng thẻ kho không có trạng thái riêng (không Hoạt động / Khóa). Chứng từ nguồn có trạng thái riêng ở màn '
                           'của nó; thẻ kho không hiển thị trạng thái đó.'),
    ('Cấu trúc phân cấp', 'Hàng hóa > Chứng từ (cấp 0, đánh số La Mã I, II…) > Lô / vị trí (cấp 1, đánh số 1, 2…). Phạm vi kho: Kho > '
                          'Nhà > Dãy > Khoang > Vị trí.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Quyền khai trong nhóm “Báo cáo kho” (tên giữ y hệ thống ERP, người dùng chốt 22/10/2026). Máy chủ kiểm quyền ở mọi chức năng '
    'của màn (lấy danh mục, xem báo cáo, cấu trúc vị trí, in, xuất Excel); mục menu Thẻ kho hiện với mọi người dùng vào được phân hệ '
    'Kho. Super admin được miễn kiểm cả 2 quyền.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1, 'Mở màn và dùng mọi chức năng: xem thẻ kho, tìm kiếm và lọc, cài đặt bộ lọc, chọn hàng hóa, bung chứng từ, in, xuất '
               'Excel. Thiếu quyền: máy chủ từ chối mọi chức năng, báo ' + NOPERM),
], widths=[0.8, 1.9, 3.3])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', V1, 'Ô Tồn theo công ty liệt kê mọi công ty đang hoạt động; xem thẻ kho của công ty bất kỳ.'),
    ('—', '(Không có V1)', 'Ô Tồn theo công ty chỉ có công ty làm việc của người dùng; máy chủ bỏ qua công ty gửi lên và luôn lấy công '
                          'ty của người dùng. Tài khoản chưa gắn công ty → ô trống, không xem được.'),
], widths=[0.8, 2.3, 2.9])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q1 + V1', 'Không có quyền nào'], [
    ('FR-01 Xem thẻ kho', '✅ (công ty mình)', '✅ (mọi công ty)', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅ (đổi được Tồn theo công ty)', '❌'),
    ('FR-03 Chọn hàng hóa', '✅', '✅', '❌ (mở được cửa sổ nhưng không xem được báo cáo)'),
    ('FR-04 Cài đặt bộ lọc', '✅', '✅', '✅ (cấu hình riêng người dùng, không có dữ liệu)'),
    ('FR-05 Xem chi tiết chứng từ và lô / vị trí', '✅', '✅', '❌'),
    ('FR-06 In thẻ kho', '✅', '✅', '❌'),
    ('FR-07 Xuất Excel', '✅', '✅', '❌'),
], widths=[2.4, 1.1, 1.3, 1.2])
d.p('Màn không có chức năng Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Import Excel, Lịch sử thay đổi, Duyệt / Không duyệt nên ma '
    'trận không có các dòng tương ứng. In và Xuất Excel không gắn quyền riêng ngoài Q1. Mở màn chứng từ nguồn từ Số chứng từ theo '
    'quyền của màn đó.')
d.p('Trường hợp không có quyền:')
d.bullets([
    'Mở màn khi thiếu Q1: hệ thống báo ' + NOPERM + ', ô Tồn theo công ty không có lựa chọn, bảng không có dữ liệu; mọi lần tải báo '
    'cáo, in, xuất đều bị từ chối với cùng thông báo.',
    'Có Q1 nhưng không có V1: chỉ xem được công ty mình; sửa tay công ty khác (bỏ qua giao diện) máy chủ vẫn trả thẻ kho công ty mình.',
    'Kho gửi lên không thuộc công ty đang xem: máy chủ bỏ qua kho đó.',
    'Quyền bị thu hồi khi đang mở màn: lần tải / in / xuất tiếp theo bị từ chối, báo ' + NOPERM,
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Nút / thao tác', 'Hiện khi', 'Vị trí'], [
    ('In danh sách, Xuất Excel', 'Luôn hiện; chưa có báo cáo (thiếu ô bắt buộc) thì bấm sẽ bật chữ đỏ dưới ô thiếu; Xuất Excel khóa '
                                 'trong lúc đang xuất', 'Đầu khối Bộ lọc thẻ kho'),
    ('Cài đặt bộ lọc, Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Luôn hiện', 'Đầu khối Bộ lọc thẻ kho'),
    ('Tìm kiếm, Xóa lọc', 'Khi khối ô lọc đang mở', 'Dưới các ô lọc'),
    ('Ô Nhà / Dãy / Khoang / Vị trí', 'Chỉ khi đã chọn ít nhất 1 Kho', 'Cuối khối ô lọc'),
    ('Ô Thời gian', 'Chỉ khi Kỳ = Tuỳ chọn', 'Ngay sau ô Kỳ'),
    ('Khối tổng hợp, dòng TỔNG, phân trang', 'Khi đã có báo cáo', 'Thân màn'),
    ('Liên kết Số chứng từ', 'Chứng từ có màn xem (trừ Nhập tồn đầu)', 'Cột Chứng từ / Lô'),
], widths=[2.2, 2.6, 1.6])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_TK, [0, 1, 2])],
    [('FR-01', 'Xem thẻ kho', 'view'),
     ('FR-06', 'In thẻ kho', 'io'),
     ('FR-07', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Chọn hàng hóa', 'view', 'extend', [0], None),
     ('FR-04', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-05', 'Xem chi tiết chứng từ và lô / vị trí', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Thẻ kho')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
k = fr(1, 'Xem thẻ kho',
       rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang.', 'list'),
       intro=dict(
           ten='Truy cập màn Thẻ kho và xem thẻ kho của một mặt hàng',
           mota='Mở màn Thẻ kho và hiển thị biến động nhập – xuất – tồn của một mặt hàng trong kỳ đã chọn, tại các kho / vị trí của '
                'một công ty: khối tổng hợp Số lượng (Tồn đầu kỳ, Nhập, Xuất, Tồn cuối kỳ) và Chứng từ (Tổng, Nhập, Xuất, Điều chuyển '
                'vị trí), bảng chi tiết báo cáo mỗi chứng từ một dòng kèm SL tồn lũy kế, dòng TỔNG và phân trang theo chứng từ. Màn '
                'chỉ đọc; phạm vi theo quyền ở Phần 2.',
           tacnhan=TN, dieukien=DK,
           chinh='1. Người dùng vào menu theo đường dẫn ở mục Layout.\n'
                 '2. Hệ thống mở màn “Thẻ kho”, khối Bộ lọc thẻ kho đang mở sẵn; nếu người dùng vừa tải lại trang (F5) trong 10 phút '
                 'thì khôi phục bộ lọc đã ghi tạm (kể cả hàng hóa đã chọn), không thì bộ lọc về mặc định: Kỳ Năm nay, Tồn theo công '
                 'ty = công ty của người dùng, Loại báo cáo Tất cả.\n'
                 '3. Hệ thống kiểm tra quyền “' + Q1 + '”, nạp danh mục công ty, kho, công ty thuê kho cho bộ lọc.\n'
                 '4. Chưa chọn Hàng hóa → bảng hiện ' + E_NOPRODUCT + ', không tải báo cáo.\n'
                 '5. Người dùng chọn Hàng hóa (mục 2.3); hệ thống tự tải báo cáo: tính tồn đầu kỳ, gom nhật ký tồn trong kỳ thành '
                 'dòng chứng từ, cộng dồn SL tồn, đếm chứng từ.\n'
                 '6. Hệ thống hiển thị dòng tiêu đề “Thẻ kho <kỳ> (<từ ngày> – <đến ngày>)”, khối tổng hợp, dòng TỔNG và trang 1 '
                 '(20 chứng từ) xếp theo thời điểm ghi nhận tăng dần, kèm “Hiển thị a–b / N chứng từ”.',
           phu='• Thiếu quyền “' + Q1 + '” → hiển thị ' + NOPERM + ', bảng không có dữ liệu.\n'
               '• Chưa chọn Tồn theo công ty → bảng hiện ' + E_NOCOMPANY + '\n'
               '• Kỳ Tuỳ chọn chưa đủ 2 ngày → bảng hiện ' + E_NORANGE + '\n'
               '• Không có chứng từ nào trong kỳ → bảng hiện ' + E_EMPTY + ', khối tổng hợp vẫn hiện Tồn cuối kỳ = Tồn đầu kỳ.\n'
               '• Đang tải lần đầu → ' + E_LOADING + '; tải lại khi đổi lọc → dữ liệu cũ mờ đi tới khi có kết quả mới.\n'
               '• Lỗi tải → giữ báo cáo đang hiển thị (nếu có), hiện thông báo lỗi của máy chủ hoặc ' + E_LOAD + '\n'
               '• Phiên đăng nhập hết hạn → hiển thị “Phiên đăng nhập đã hết hạn”, chuyển về màn đăng nhập.',
           dacbiet='Bảng không có sắp xếp theo cột và không có Tùy chỉnh cột (khuôn báo cáo). Thứ tự cố định theo thời điểm ghi nhận. '
                   'Phân trang thực hiện trên trình duyệt theo dòng chứng từ: mặc định 20, lựa chọn 10 / 20 / 50 / 100; máy chủ trả '
                   'trọn thẻ kho trong kỳ để SL tồn lũy kế luôn đúng.'),
       layout=dict(menu=MENU, shot=shot('02_main'),
                   shot_caption='Màn Thẻ kho — hàng ENEO-640-V5236, công ty TPE, Kỳ Năm nay (bộ lọc thu gọn)',
                   note='Lối vào duy nhất (phân hệ Kho). Không màn báo cáo nào khác mở sang Thẻ kho. Hiển thị: thẻ kho của hàng đã '
                        'chọn tại công ty đang xem.'),
       extra=[(shot('00_menu'), 'Mục Thẻ kho trong menu Báo cáo kho của phân hệ Kho'),
              (shot('01_empty'), 'Màn Thẻ kho lúc mới vào, chưa chọn hàng hóa')],
       ui_kw=dict(required=False),
       ui=[
           ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '“Thẻ kho”',
            ['- Ở thanh trên cùng, cũng là tiêu đề tab trình duyệt',
             '- Icon ⓘ: “Theo dõi nhập, xuất, tồn của một mặt hàng theo từng chứng từ trong kỳ, tại các kho / vị trí đã chọn của '
             'một công ty.”']),
           ('Dòng tiêu đề khối tổng hợp', 'Label', 'Read-only', '–', 'Theo dữ liệu',
            ['- “Thẻ kho <kỳ> (<từ ngày> – <đến ngày>)”, vd “Thẻ kho năm 2026 (01/01/2026 – 31/12/2026)”',
             '- Tiếp theo: mã - tên hàng · ĐVT <ĐVT cơ sở> · Kho: <các kho đang lọc> (không chọn kho: mọi kho của công ty)',
             '- Icon ⓘ: “' + TIP_GOAL + '”']),
           ('Nút Thu gọn / Mở rộng', 'Button', 'Enable', '–', '“Thu gọn”',
            ['- Góc phải dòng tiêu đề khối tổng hợp', '- Bấm → ẩn 2 khối Số lượng, Chứng từ; chữ đổi thành “Mở rộng”',
             '- Chỉ là cách xem, không tải lại']),
           ('Khối Số lượng', 'Label', 'Read-only', '–', 'Theo dữ liệu',
            ['- Tiêu đề “SỐ LƯỢNG”, góc phải “ĐVT <ĐVT cơ sở>”', '- Icon ⓘ: “' + TIP_QTY + '”', '- Số KHÔNG bấm được (không mở popup)']),
           ('Ô Tồn đầu kỳ', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Tồn trước ngày đầu kỳ, kèm ĐVT', '- Ẩn khi bằng 0', '- Số phân cách hàng nghìn bằng dấu phẩy, tối đa 2 số lẻ']),
           ('Ô Nhập trong kỳ', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Tổng nhập trong kỳ (gồm chuyển vào của điều chuyển vị trí)', '- Ẩn khi bằng 0']),
           ('Ô Xuất trong kỳ', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Tổng xuất trong kỳ (gồm chuyển ra của điều chuyển vị trí)', '- Ẩn khi bằng 0']),
           ('Ô Tồn cuối kỳ', 'Label', 'Read-only', 'Số', 'Theo dữ liệu',
            ['- Tồn đầu kỳ + Nhập − Xuất', '- Ô tổng của khối, luôn hiện (0 vẫn hiện “0”)']),
           ('Khối Chứng từ', 'Label', 'Read-only', '–', 'Theo dữ liệu',
            ['- Tiêu đề “CHỨNG TỪ”', '- Icon ⓘ: “' + TIP_VOUCHER + '”', '- Số KHÔNG bấm được']),
           ('Ô Tổng chứng từ', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Số chứng từ trong kỳ, đơn vị “phiếu”', '- Ô tổng, luôn hiện']),
           ('Ô Nhập (phiếu)', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu', ['- Số chứng từ nhập', '- Ẩn khi bằng 0']),
           ('Ô Xuất (phiếu)', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu', ['- Số chứng từ xuất', '- Ẩn khi bằng 0']),
           ('Ô Điều chuyển vị trí (phiếu)', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Số phiếu điều chuyển vị trí', '- Ẩn khi bằng 0 hoặc khi Loại báo cáo “Không nhặt điều chuyển”']),
           ('Bảng chi tiết báo cáo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- 9 cột: STT, Chứng từ / Lô, Ngày chứng từ, Diễn giải, Vị trí, Nhập, Xuất, SL tồn, NVKD',
             '- Tiêu đề cột dính khi cuộn; bảng rộng hơn màn hình thì cuộn ngang',
             '- Không sắp xếp theo cột, không Tùy chỉnh cột']),
           ('Ô chọn cấp bung', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Chỉ chứng từ',
            ['- Nằm trong tiêu đề cột Chứng từ / Lô', '- Mặc định: Chỉ chứng từ', '- Lựa chọn: Chỉ chứng từ',
             '- Lựa chọn: Tất cả cấp (đến Lô / vị trí)', '- Chi tiết ở mục 2.5']),
           ('Dòng TỔNG', 'Label', 'Read-only', '–', 'Theo dữ liệu',
            ['- Nền cam, trên cùng bảng: “TỔNG” · “PHÁT SINH TRONG KỲ” · “<N> chứng từ”',
             '- Nhập = Nhập trong kỳ, Xuất = Xuất trong kỳ, SL tồn = Tồn cuối kỳ (0 hiện “0”)',
             '- Tính trên toàn thẻ kho, không theo trang',
             '- Icon ⓘ: “' + TIP_TOTAL + '”']),
           ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Dòng chứng từ: số La Mã I, II… liên tục giữa các trang', '- Dòng lô: 1, 2… trong chứng từ']),
           ('Cột Chứng từ / Lô', 'Link', 'Read-only', '–', 'Theo dữ liệu',
            ['- Dòng chứng từ: mũi tên bung + Số chứng từ (chữ xanh gạch chân khi có màn xem)',
             '- Bấm Số chứng từ → mở màn chứng từ nguồn ở TAB MỚI (mục 2.5)',
             '- Nhập tồn đầu: “NHAP_TON_DAU_<số>”, chữ thường không bấm được',
             '- Điều chuyển: kèm chữ nhỏ “Điều chuyển vị trí”', '- Dòng lô: số lô']),
           ('Cột Ngày chứng từ', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
            ['- Ngày chứng từ được ghi nhận vào thẻ kho (ngày ghi tồn)', '- Dòng lô để trống']),
           ('Cột Diễn giải', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Ghi chú của chứng từ; Nhập tồn đầu: “Nhập tồn đầu”', '- Dài thì cắt “…”, rê chuột xem đủ', '- Dòng lô để trống']),
           ('Cột Vị trí', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Dòng chứng từ 1 lô / vị trí: mã vị trí', '- Nhiều lô / vị trí: chữ xám “<n> lô / vị trí”',
             '- Dòng lô: mã vị trí của lô']),
           ('Cột Nhập', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Dòng chứng từ nhập: tổng nhập; điều chuyển: tổng chuyển vào', '- Dòng lô: số nhập vào vị trí',
             '- Trống khi 0 / không phải nhập', '- Icon ⓘ: “' + TIP_IMP + '”']),
           ('Cột Xuất', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Dòng chứng từ xuất: tổng xuất; điều chuyển: tổng chuyển ra', '- Dòng lô: số xuất khỏi vị trí',
             '- Trống khi 0 / không phải xuất', '- Icon ⓘ: “' + TIP_EXP + '”']),
           ('Cột SL tồn', 'Table/Grid', 'Read-only', 'Số', 'Theo dữ liệu',
            ['- Dòng chứng từ: tồn lũy kế sau chứng từ (0 hiện “0”)', '- Dòng lô để trống', '- Icon ⓘ: “' + TIP_SL + '”']),
           ('Cột NVKD', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- “Họ tên - Mã phòng ban” người lập yêu cầu', '- Nhập tồn đầu / không có người lập: trống',
             '- Icon ⓘ: “' + TIP_NVKD + '”']),
           ('Dòng “Hiển thị a–b / N chứng từ”', 'Label', 'Read-only', '–', 'Theo dữ liệu',
            ['- a–b: khoảng STT chứng từ của trang', '- N: số dòng chứng từ sau ô Số chứng từ / Diễn giải', '- Ẩn khi không có dòng']),
           ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', '20',
            ['- Mặc định: 20', '- Lựa chọn: 10, 20, 50, 100', '- Đổi → về trang 1, không tải lại máy chủ']),
           ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
            ['- « ‹ số trang › »; trang đầu « ‹ mờ, trang cuối › » mờ', '- Bung / thu lô không đẩy dòng sang trang khác']),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
            ['- Chưa chọn hàng: ' + E_NOPRODUCT, '- Chưa chọn công ty: ' + E_NOCOMPANY, '- Tuỳ chọn thiếu ngày: ' + E_NORANGE,
             '- Không có chứng từ: ' + E_EMPTY, '- Đang tải lần đầu: ' + E_LOADING]),
           ('Thông báo lỗi tải dữ liệu', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
            ['- Thiếu quyền: ' + NOPERM, '- Lỗi khác: câu lỗi của máy chủ, không có thì ' + E_LOAD,
             '- Hết phiên: “Phiên đăng nhập đã hết hạn”']),
       ],
       ev=[('Mở màn hình', 'System',
            'Before:\n– Kiểm tra quyền “' + Q1 + '” (Super admin miễn kiểm).\n'
            '– Nếu không có quyền → hiển thị ' + NOPERM + ' và dừng xử lý.\n'
            '– Có bộ lọc ghi tạm dưới 10 phút → khôi phục; không → Kỳ Năm nay, công ty mặc định của người dùng.\n'
            'During:\n– Nạp danh mục công ty (theo V1), kho, công ty thuê kho; Kỳ Năm nay = 01/01 → 31/12 năm hiện tại.\n'
            '– Chưa có Hàng hóa / Tồn theo công ty / đủ ngày Tuỳ chọn → không tải báo cáo, hiện câu nhắc tương ứng.\n'
            '– Có đủ → tính tồn đầu kỳ, gom chứng từ, cộng dồn SL tồn, đếm chứng từ.\n'
            'After:\n– Hiển thị khối tổng hợp, dòng TỔNG, trang 1 (20 chứng từ).\n– Lỗi → giữ dữ liệu cũ, hiện thông báo lỗi.'),
           ('Chọn hàng hóa / đổi ô lọc', 'Change',
            'Before:\n– Áp cho Hàng hóa, Kỳ, Thời gian (đủ 2 ngày), Tồn theo công ty, Kho, Công ty thuê kho, Loại báo cáo, Nhà / Dãy / '
            'Khoang / Vị trí.\n'
            'During:\n– Gom các thay đổi liên tiếp trong 0,3 giây thành 1 lần tải; ghi tạm bộ lọc.\n'
            '– Đổi sang hàng khác → về trang 1.\n'
            'After:\n– Tải lại báo cáo; trang hiện tại lớn hơn số trang mới thì về trang cuối.'),
           ('Bấm Thu gọn / Mở rộng khối tổng hợp', 'Click',
            'Before:\n– Khối tổng hợp đang hiện.\nDuring:\n– Ẩn / hiện 2 khối Số lượng, Chứng từ.\n'
            'After:\n– Không tải lại; dòng tiêu đề vẫn hiện.'),
           ('Bấm số trang hoặc nút tiến lùi', 'Click',
            'Before:\n– Giữ nguyên bộ lọc và cấp bung đang chọn.\nDuring:\n– Cắt dòng chứng từ của trang được chọn trên trình duyệt.\n'
            'After:\n– Hiện trang mới, STT La Mã tiếp tục, “Hiển thị a–b / N chứng từ” cập nhật; cấp bung áp lại cho trang mới.'),
           ('Đổi Số dòng/trang', 'Change',
            'Before:\n– Chọn 1 trong 10, 20, 50, 100.\nDuring:\n– Ghi nhận số dòng mới.\n'
            'After:\n– Về trang 1, hiện theo số dòng mới (không tải lại máy chủ).'),
           ('Rê chuột vào icon ⓘ', 'Hover',
            'Before:\n– Icon ở tiêu đề trang, dòng tiêu đề khối, khối Số lượng / Chứng từ, dòng TỔNG, cột Nhập / Xuất / SL tồn / NVKD.\n'
            'During:\n– Hiện ô giải thích.\nAfter:\n– Rời chuột → ẩn ô giải thích.'),
           ('Phiên đăng nhập hết hạn khi thao tác', 'System',
            'Before:\n– Áp cho mọi lần tải báo cáo.\nDuring:\n– Máy chủ từ chối yêu cầu.\n'
            'After:\n– Hiển thị “Phiên đăng nhập đã hết hạn”, chuyển về màn đăng nhập.')])

d.p('2.1.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('“Tập dữ liệu” là các dòng nhật ký thay đổi tồn kho theo vị trí của hàng đã chọn, tại các vị trí thuộc kho đang lọc (không chọn kho '
    '= mọi kho của công ty; có tick Nhà / Dãy / Khoang / Vị trí thì theo cấp sâu nhất được tick), ghi nhận cho công ty thuê kho đang '
    'chọn (không chọn kho = chính công ty đang xem; chọn kho mà không tick công ty thuê = mọi công ty thuê của các kho đó), sau khi bỏ '
    'dòng điều chuyển nếu Loại báo cáo “Không nhặt điều chuyển”. “Trong kỳ” = thời điểm ghi nhận từ 00:00 ngày đầu kỳ tới hết ngày '
    'cuối kỳ. Mọi số theo ĐVT cơ sở. Một chứng từ được tính khi đã ghi tồn: phiếu nhập kho và phiếu xuất kho từ lúc gửi (Chờ duyệt; '
    'phiếu xuất còn chuyến xe chưa duyệt xuất phát thì chưa trừ), phiếu nhập / xuất kho điều chỉnh kiểm kê từ lúc gửi, phiếu điều '
    'chuyển vị trí khi Đã chuyển, phiếu nhập lại và phiếu xuất điều chỉnh sai số liệu khi lập, khai báo tồn đầu kỳ khi lưu; phiếu bị '
    'Không duyệt sau đó KHÔNG hoàn tồn nên vẫn nằm trên thẻ kho.')
d.data_table([
    ('Dòng tiêu đề khối tổng hợp', 'Kỳ: Tuần này = thứ Hai → Chủ nhật tuần hiện tại; Tháng này = ngày 1 → ngày cuối tháng; Năm nay = '
                                   '01/01 → 31/12; Năm trước; Tuỳ chọn = Từ ngày → Đến ngày. “Số liệu tính tại” = thời điểm máy chủ '
                                   'tính báo cáo.', TIP_GOAL),
    ('Ô Tồn đầu kỳ', 'Tổng thay đổi (nhập dương, xuất âm) của tập dữ liệu có thời điểm ghi nhận TRƯỚC ngày đầu kỳ. Ẩn khi = 0.',
     '(dùng chung ⓘ của khối) ' + TIP_QTY),
    ('Ô Nhập trong kỳ', 'Tổng các thay đổi DƯƠNG trong kỳ, gồm cả dòng chuyển vào của điều chuyển vị trí. Ẩn khi = 0.',
     '(dùng chung ⓘ của khối)'),
    ('Ô Xuất trong kỳ', 'Trị tuyệt đối tổng các thay đổi ÂM trong kỳ, gồm cả dòng chuyển ra của điều chuyển vị trí. Ẩn khi = 0.',
     '(dùng chung ⓘ của khối)'),
    ('Ô Tồn cuối kỳ', 'SL tồn của dòng chứng từ cuối cùng trong kỳ (không có chứng từ = Tồn đầu kỳ). Luôn bằng Tồn đầu kỳ + Nhập '
                      'trong kỳ − Xuất trong kỳ. Luôn hiện.', '(dùng chung ⓘ của khối)'),
    ('Ô Tổng chứng từ', 'Số dòng chứng từ trong kỳ: nhật ký gom theo (phiếu, loại chứng từ); mỗi lần khai tồn đầu là 1 chứng từ riêng. '
                        'Tính trên toàn thẻ kho, KHÔNG theo ô Số chứng từ / Diễn giải. Luôn hiện.',
     '(dùng chung ⓘ của khối) ' + TIP_VOUCHER),
    ('Ô Nhập / Xuất / Điều chuyển vị trí (phiếu)', 'Điều chuyển vị trí: chứng từ điều chuyển. Xuất: chứng từ khác có ít nhất 1 lô / vị '
                                                    'trí giảm. Nhập: còn lại. Tổng 3 ô = Tổng chứng từ. Ô = 0 thì ẩn.',
     '(dùng chung ⓘ của khối)'),
    ('Dòng TỔNG', 'Nhập = ô Nhập trong kỳ; Xuất = ô Xuất trong kỳ (CẢ điều chuyển); SL tồn = Tồn cuối kỳ; “N chứng từ” = Tổng chứng từ. '
                  'Không theo trang, không theo ô Số chứng từ / Diễn giải. Lưu ý: chữ ⓘ ghi “không tính điều chuyển vị trí” nhưng số '
                  'thực tế CÓ tính (lệch chữ ⓘ, xem ghi chú cuối mục).', TIP_TOTAL),
    ('Cột Nhập (dòng chứng từ)', 'Chứng từ nhập: tổng thay đổi các lô / vị trí của chứng từ. Điều chuyển: tổng các dòng chuyển vào. '
                                 'Chứng từ xuất: trống.', TIP_IMP),
    ('Cột Xuất (dòng chứng từ)', 'Chứng từ xuất: trị tuyệt đối tổng thay đổi của chứng từ. Điều chuyển: tổng các dòng chuyển ra. '
                                 'Chứng từ nhập: trống.', TIP_EXP),
    ('Cột Nhập / Xuất (dòng lô)', 'Thay đổi của lô tại vị trí: dương → cột Nhập, âm → cột Xuất (trị tuyệt đối).', '(như 2 dòng trên)'),
    ('Cột SL tồn', 'Tồn đầu kỳ + cộng dồn thay đổi của mọi chứng từ từ đầu kỳ tới hết chứng từ đang xét, theo thứ tự hiển thị. SL '
                   'tồn dòng sau = SL tồn dòng trước + Nhập − Xuất của dòng sau. Giữ nguyên khi lọc Số chứng từ / Diễn giải.', TIP_SL),
    ('Cột Ngày chứng từ', 'Ngày của dòng nhật ký đầu tiên của chứng từ (ngày ghi tồn), không phải ngày lập phiếu.', '—'),
    ('Cột NVKD', 'Người lập yêu cầu ghi trên chứng từ + mã phòng ban của người đó.', TIP_NVKD),
    ('Thứ tự dòng', 'Theo thời điểm ghi nhận tăng dần, cùng thời điểm theo thứ tự ghi; chứng từ đứng ở vị trí lần ghi đầu tiên.', '—'),
    ('Ràng buộc khớp số', 'Tồn đầu kỳ + Nhập − Xuất = Tồn cuối kỳ = SL tồn dòng chứng từ cuối; Tồn đầu kỳ này = Tồn cuối kỳ liền '
                          'trước (vd Năm trước tồn cuối 15,141 = Năm nay tồn đầu 15,141); Tổng chứng từ = N của dòng “Hiển thị” khi '
                          'không lọc Số chứng từ / Diễn giải. Không chọn kho: Tồn cuối kỳ = tồn của công ty ở Báo cáo tồn kho tổng hợp '
                          '/ chi tiết theo mặt hàng tính tới hết kỳ. Chọn kho: Tồn đầu / Nhập / Xuất / Tồn cuối khớp Tổng hợp xuất '
                          'nhập tồn cùng kho, cùng kỳ.', '—'),
])
d.p('Ghi chú lệch chữ ⓘ (báo người phụ trách, SRS ghi theo cách tính thật): (1) ⓘ dòng TỔNG ghi “không tính điều chuyển vị trí” — '
    'thực tế Nhập / Xuất dòng TỔNG bằng ô Nhập / Xuất trong kỳ, CÓ tính điều chuyển; (2) ⓘ dòng tiêu đề ghi “Số lượng quy theo ĐVT '
    'đang chọn ở bộ lọc” — bộ lọc đã bỏ ô ĐVT (27/10/2026), số luôn theo ĐVT cơ sở.')
k += 1
d.p('2.1.%d Danh sách popup mở từ số liệu' % k)
d.popup_table([
    ('Số ở khối Số lượng, khối Chứng từ, dòng TỔNG', 'Không mở popup — số không bấm được (người dùng chốt 22/10/2026)',
     'Xem nhanh tổng nhập / xuất / tồn và số chứng từ', 'Số tổng của toàn thẻ kho đã lọc'),
    ('Số chứng từ ở cột Chứng từ / Lô (dòng chứng từ có liên kết)',
     'Không phải popup — mở màn chi tiết chứng từ nguồn ở tab mới (mục 2.5)',
     'Chứng từ này nhập / xuất gì, của ai, đang ở trạng thái nào', 'Màn chi tiết của phiếu nhập kho / xuất kho / điều chuyển vị trí / '
                                                                     'xuất điều chỉnh sai số liệu / xuất kho điều chỉnh kiểm kê; 2 '
                                                                     'loại còn lại mở hệ thống ERP'),
    ('Mũi tên bung ở dòng chứng từ, ô chọn cấp bung', 'Không phải popup — bung dòng Lô / vị trí ngay trong bảng (mục 2.5)',
     'Chứng từ thay đổi tồn ở lô nào, vị trí nào', 'Các lô / vị trí của chứng từ; tổng khớp cột Nhập / Xuất của dòng chứng từ'),
    ('Ô Hàng hóa ở bộ lọc', 'Cửa sổ Chọn hàng hóa (mục 2.3)', 'Chọn đúng mặt hàng cần xem thẻ kho',
     'Hàng hóa của công ty đang xem, kể cả hàng chưa kinh doanh tại công ty'),
])

# ------------------------------------------------------------ 2.2
k = fr(2, 'Tìm kiếm và lọc',
       rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
       intro=dict(ten='Tìm kiếm và lọc thẻ kho',
                  mota='Chọn phạm vi thẻ kho bằng khối “Bộ lọc thẻ kho”: Kỳ, Thời gian (khi Tuỳ chọn), Hàng hóa (bắt buộc), Tồn theo '
                       'công ty (bắt buộc), Kho, Công ty thuê kho, Loại báo cáo, Số chứng từ / Diễn giải và 4 cột tick Nhà / Dãy / '
                       'Khoang / Vị trí (khi đã chọn kho). Ô chọn áp ngay khi đổi; ô Số chứng từ / Diễn giải áp khi Enter hoặc bấm Tìm '
                       'kiếm; Xóa lọc về mặc định.',
                  tacnhan=TN, dieukien=DK,
                  chinh='1. Người dùng mở / giữ mở khối ô lọc (nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao).\n'
                        '2. Người dùng chọn Kỳ; chọn Tuỳ chọn thì hiện ô Thời gian, chọn đủ Từ ngày và Đến ngày.\n'
                        '3. Người dùng chọn Hàng hóa (mục 2.3), Tồn theo công ty (nếu có quyền “' + V1 + '”).\n'
                        '4. Tùy chọn: chọn Kho (hệ thống tự chọn hết Công ty thuê kho của các kho đó, hiện 4 cột Nhà / Dãy / Khoang / '
                        'Vị trí), bỏ bớt công ty thuê, tick vị trí, chọn Loại báo cáo.\n'
                        '5. Mỗi lần đổi ô chọn, hệ thống ghi tạm bộ lọc và tải lại báo cáo.\n'
                        '6. Người dùng gõ Số chứng từ / Diễn giải rồi Enter hoặc bấm Tìm kiếm → bảng chỉ còn dòng khớp.\n'
                        '7. Bấm Xóa lọc → bộ lọc về mặc định, bỏ hàng hóa đã chọn.',
                  phu='• Bấm Tìm kiếm khi thiếu Hàng hóa → chữ đỏ ' + M_PRODUCT + ' dưới ô, khối ô lọc tự mở, không tải.\n'
                      '• Thiếu Tồn theo công ty → chữ đỏ ' + M_COMPANY + '.\n'
                      '• Kỳ Tuỳ chọn thiếu ngày → chữ đỏ ' + M_RANGE + ', bảng hiện ' + E_NORANGE + '\n'
                      '• Đổi Tồn theo công ty → bỏ hết Kho đã chọn (kho của công ty cũ).\n'
                      '• Đổi Kỳ khác Tuỳ chọn → xóa Từ ngày / Đến ngày.\n'
                      '• Bỏ hết Kho → ẩn 4 cột vị trí, xóa tick vị trí, xóa Công ty thuê kho.\n'
                      '• Không chứng từ nào khớp → ' + E_EMPTY + '\n'
                      '• Rời sang màn khác → bộ lọc ghi tạm bị xóa; tải lại trang (F5) trong 10 phút → khôi phục.\n'
                      '• Gọi thẳng chức năng với Đến ngày nhỏ hơn Từ ngày → ' + M_RANGE_ORDER + '.',
                  dacbiet='Ô Số chứng từ / Diễn giải khớp MỘT PHẦN, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối, không giới '
                          'hạn số ký tự; chỉ lọc dòng hiển thị, KHÔNG đổi khối tổng hợp, dòng TỔNG và SL tồn lũy kế. Các ô chọn khớp '
                          'CHÍNH XÁC. Khối ô lọc mở sẵn khi vào màn.'),
       layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('07_filter_kho'),
                   shot_caption='Khối Bộ lọc thẻ kho khi đã chọn Kho PTT — Công ty thuê kho tự chọn hết, hiện 4 cột Nhà / Dãy / Khoang / Vị trí'),
       extra=[(shot('01b_required'), 'Bấm Tìm kiếm khi chưa chọn Hàng hóa — chữ đỏ dưới ô'),
              (shot('08_period_custom'), 'Kỳ Tuỳ chọn — hiện ô Thời gian bắt buộc')],
       ui=[('Tiêu đề khối', 'Label', 'Hiển thị', '–', '–', '“Bộ lọc thẻ kho”',
            ['- Kèm biểu tượng phễu', '- Icon ⓘ: “' + TIP_PURPOSE + '”']),
           ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', '“Ẩn tìm kiếm nâng cao”',
            ['- Mặc định khối ô lọc đang mở', '- Bấm → thu gọn / mở khối ô lọc; giá trị đã chọn vẫn áp dụng']),
           ('Kỳ', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Có', 'Năm nay',
            ['- Mặc định: Năm nay', '- Lựa chọn: Tuần này', '- Lựa chọn: Tháng này', '- Lựa chọn: Năm nay', '- Lựa chọn: Năm trước',
             '- Lựa chọn: Tuỳ chọn (hiện ô Thời gian)', '- Không có nút × bỏ chọn', '- Icon ⓘ: “' + H_KY + '”']),
           ('Thời gian', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy', 'Có khi Kỳ = Tuỳ chọn', 'Trống',
            ['- Chỉ hiện khi Kỳ = Tuỳ chọn', '- 1 ô gồm Từ ngày → Đến ngày', '- Thiếu 1 bên: chữ đỏ ' + M_RANGE + ' khi bấm Tìm kiếm']),
           ('Hàng hóa', 'Textbox', 'Enable', '1 hàng', 'Có', 'Trống',
            ['- Ô chỉ đọc, bấm → mở cửa sổ Chọn hàng hóa (mục 2.3)', '- Hiện “Mã - Tên”, dài thì cắt “…”, rê chuột xem đủ',
             '- Thiếu: chữ đỏ ' + M_PRODUCT]),
           ('Tồn theo công ty', 'Dropdown', 'Enable', 'Danh sách công ty', 'Có', 'Công ty của người dùng',
            ['- Mặc định: công ty làm việc của người dùng', '- Có quyền “' + V1 + '”: mọi công ty đang hoạt động',
             '- Không có: chỉ công ty mình', '- Có nút × bỏ chọn; thiếu: chữ đỏ ' + M_COMPANY,
             '- Đổi công ty → bỏ hết Kho đã chọn']),
           ('Kho', 'Dropdown', 'Enable', 'Chọn nhiều', 'Không', 'Trống',
            ['- Kho vật lý đang hoạt động mà công ty có kho kế toán, dạng “Mã - Tên”', '- Mặc định: trống = toàn bộ kho của công ty',
             '- Đổi → tự chọn hết Công ty thuê kho, xóa tick vị trí, nạp lại 4 cột vị trí', '- Icon ⓘ: “' + H_KHO + '”']),
           ('Công ty thuê kho', 'Dropdown', 'Enable', 'Chọn nhiều', 'Không', 'Trống',
            ['- Lựa chọn: công ty có kho kế toán tại các kho đã chọn (hiện mã công ty, mỗi công ty 1 lần)',
             '- Chưa chọn kho: không có lựa chọn', '- Bỏ trống = mọi công ty thuê của các kho đã chọn', '- Icon ⓘ: “' + H_RENTAL + '”']),
           ('Loại báo cáo', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Có', 'Tất cả',
            ['- Mặc định: Tất cả', '- Lựa chọn: Tất cả', '- Lựa chọn: Không nhặt điều chuyển (bỏ mọi dòng điều chuyển vị trí)',
             '- Không có nút × bỏ chọn']),
           ('Số chứng từ / Diễn giải', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
            ['- Khớp một phần số chứng từ hoặc diễn giải', '- Áp khi Enter hoặc bấm Tìm kiếm', '- Icon ⓘ: “' + H_KW + '”']),
           ('Nhà / Dãy / Khoang / Vị trí', 'Checkbox', 'Enable / Ẩn', 'Danh sách', 'Không', 'Ẩn',
            ['- Chỉ hiện khi đã chọn Kho', '- 4 cột tick, mỗi cột có ô tìm + “Chọn hết”; mã có tiền tố kho khi chọn nhiều kho',
             '- Không tick = mọi vị trí của các kho', '- Lọc theo cấp sâu nhất được tick']),
           ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
            ['- Kiểm ô bắt buộc; thiếu → chữ đỏ, mở khối ô lọc', '- Đủ → ghi tạm bộ lọc, tải lại báo cáo']),
           ('Nút Xóa lọc', 'Button', 'Enable', '–', '–', 'Hiển thị',
            ['- Về mặc định: Kỳ Năm nay, công ty mặc định, Loại báo cáo Tất cả', '- Bỏ hàng hóa, kho, vị trí, chữ tìm; tắt chữ đỏ',
             '- Xóa bộ lọc ghi tạm, bảng hiện ' + E_NOPRODUCT]),
           ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
            ['- ' + M_PRODUCT, '- ' + M_COMPANY, '- ' + M_RANGE, '- Chọn đủ giá trị → chữ đỏ tự tắt'])],
       ev=[('Đổi giá trị một ô chọn', 'Change',
            'Before:\n– Áp cho Kỳ, Thời gian, Hàng hóa, Tồn theo công ty, Kho, Công ty thuê kho, Loại báo cáo, tick vị trí.\n'
            '– Chưa có quyền xem công ty khác → ô Tồn theo công ty chỉ có công ty mình.\n'
            'During:\n– Đổi công ty → bỏ Kho; đổi Kỳ khác Tuỳ chọn → xóa ngày; đổi Kho → chọn hết công ty thuê, xóa tick, nạp lại cây vị trí.\n'
            '– Ghi tạm bộ lọc; gom thay đổi trong 0,3 giây.\n' + ERR + '\n'
            'After:\n– Tải lại báo cáo theo toàn bộ điều kiện; thiếu ô bắt buộc thì hiện câu nhắc trong bảng.'),
           ('Bấm Tìm kiếm hoặc Enter ở ô Số chứng từ / Diễn giải', 'Click',
            'Before:\n– Kiểm Hàng hóa, Tồn theo công ty, Thời gian (khi Tuỳ chọn).\n'
            'During:\n– Thiếu → chữ đỏ ' + M_PRODUCT + ' / ' + M_COMPANY + ' / ' + M_RANGE + ', mở khối ô lọc, dừng.\n'
            '– Đủ → máy chủ lọc dòng chứng từ có số chứng từ hoặc diễn giải chứa chuỗi gõ SAU khi cộng dồn SL tồn.\n' + ERR + '\n'
            'After:\n– Bảng chỉ còn dòng khớp, “Hiển thị a–b / N” theo số dòng khớp; khối tổng hợp, dòng TỔNG không đổi.'),
           ('Bấm Xóa lọc', 'Click',
            'Before:\n– Không hỏi xác nhận.\n'
            'During:\n– Đặt lại bộ lọc mặc định, bỏ hàng hóa, cây vị trí, chữ đỏ; xóa bộ lọc ghi tạm.\n'
            'After:\n– Bảng hiện ' + E_NOPRODUCT + ', khối tổng hợp ẩn.'),
           ('Bấm Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Click',
            'Before:\n– Khối ô lọc đang mở (mặc định) hoặc thu gọn.\nDuring:\n– Thu gọn / mở khối ô lọc.\n'
            'After:\n– Giá trị đã chọn vẫn áp dụng; trạng thái mở / thu gọn ghi tạm cùng bộ lọc.'),
           ('Tick Nhà / Dãy / Khoang / Vị trí', 'Change',
            'Before:\n– Chỉ có khi đã chọn Kho.\n'
            'During:\n– Mỗi kho: không tick gì → mọi vị trí; tick Nhà không tick Dãy con → mọi vị trí của Nhà; tương tự Dãy, Khoang; '
            'tick Vị trí → đúng vị trí đó.\n'
            'After:\n– Tải lại báo cáo theo các vị trí đã xác định.'),
           ('Rời màn hoặc tải lại trang', 'System',
            'Before:\n– Bộ lọc ghi tạm 10 phút trên trình duyệt.\n'
            'During:\n– Chuyển sang màn khác → xóa ghi tạm; F5 trong 10 phút → khôi phục (kể cả hàng hóa, tick vị trí còn hợp lệ).\n'
            'After:\n– Vào lại bằng menu → bộ lọc mặc định.')])
d.p('2.2.%d Cách lấy dữ liệu của ô lọc' % k)
d.p('Bảng dưới giải thích cách hệ thống áp từng ô lọc (chép nguyên văn chữ icon ⓘ trên ô).')
d.data_table([
    ('Kỳ / Thời gian', 'Lọc nhật ký theo thời điểm ghi nhận vào thẻ kho từ 00:00 ngày đầu tới hết ngày cuối kỳ; trước ngày đầu kỳ cộng '
                       'vào Tồn đầu kỳ.', H_KY),
    ('Hàng hóa', 'Đúng một mặt hàng (kể cả hàng chưa kinh doanh tại công ty).', '—'),
    ('Tồn theo công ty', 'Xác định danh sách kho (kho có kho kế toán của công ty) và, khi không chọn kho, công ty ghi nhận tồn.', '—'),
    ('Kho', 'Chỉ vị trí thuộc các kho đã chọn; trống = mọi kho của công ty.', H_KHO),
    ('Công ty thuê kho', 'Chọn kho: chỉ tồn ghi nhận cho các công ty thuê đã tick; không tick = mọi công ty thuê của các kho đã chọn. '
                         'Không chọn kho: không áp, lấy chính công ty đang xem.', H_RENTAL),
    ('Loại báo cáo', 'Tất cả: mọi chứng từ. Không nhặt điều chuyển: bỏ dòng điều chuyển vị trí khỏi Tồn đầu kỳ, Nhập, Xuất, bảng và số '
                     'chứng từ.', '—'),
    ('Số chứng từ / Diễn giải', 'Lọc dòng chứng từ có số chứng từ hoặc diễn giải chứa chuỗi gõ, sau khi cộng dồn SL tồn.', H_KW),
    ('Nhà / Dãy / Khoang / Vị trí', 'Hợp các vị trí theo cấp sâu nhất được tick trong từng kho; kho không tick gì lấy mọi vị trí.', '—'),
])

# ------------------------------------------------------------ 2.3
k = fr(3, 'Chọn hàng hóa',
       rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
       intro=dict(ten='Chọn hàng hóa cần xem thẻ kho',
                  mota='Bấm vào ô Hàng hóa mở cửa sổ “Chọn hàng hóa” dùng chung của hệ thống để tìm và chọn đúng 1 mặt hàng. Cửa sổ '
                       'lấy theo công ty ở ô Tồn theo công ty, gồm mọi hàng hóa kể cả hàng chưa kinh doanh tại công ty (giữ ý hệ '
                       'thống ERP tìm cả hàng đã ngừng); bấm tên hàng là chọn và đóng cửa sổ.',
                  tacnhan=TN, dieukien=DK,
                  chinh='1. Người dùng bấm vào ô Hàng hóa.\n'
                        '2. Hệ thống mở cửa sổ “Chọn hàng hóa” (cây catalog bên trái, bảng hàng bên phải, trang 1).\n'
                        '3. Người dùng gõ mã / tên / model / barcode / mã đặt hàng vào ô tìm, hoặc chọn nhánh catalog, bật / tắt Còn tồn.\n'
                        '4. Người dùng bấm vào tên hàng cần xem.\n'
                        '5. Hệ thống điền “Mã - Tên” vào ô Hàng hóa, đóng cửa sổ, tắt chữ đỏ (nếu có) và tải thẻ kho của hàng đó.',
                  phu='• Không hàng nào khớp → bảng của cửa sổ hiện “Không có hàng hoá nào thoả bộ lọc”.\n'
                      '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, giữ hàng đang chọn trước đó, không hỏi xác nhận.\n'
                      '• Chọn hàng khác hàng đang xem → bảng về trang 1.\n'
                      '• Chưa chọn công ty → cửa sổ lấy công ty làm việc của người dùng.',
                  dacbiet='Cửa sổ dùng chung toàn hệ thống: chế độ chọn 1 hàng (không có nút Thêm), không có cột Giá. Cấu hình cột của '
                          'cửa sổ là cấu hình riêng của cửa sổ dùng chung.'),
       layout=dict(menu=MENU + ' => Hàng hóa', shot=shot('03b_picker_search'),
                   shot_caption='Cửa sổ Chọn hàng hóa — tìm “ENEO-640-V5236”',
                   modal='Chọn hàng hóa'),
       extra=[(shot('03_picker'), 'Cửa sổ Chọn hàng hóa lúc mới mở')],
       ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Chọn hàng hóa”', '- Kèm biểu tượng kính lúp'),
           ('Nút Phóng to / Thu nhỏ', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → cửa sổ toàn màn hình / về cỡ cũ'),
           ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng cửa sổ, không chọn'),
           ('Dòng mô tả công ty', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu',
            ['- “Công ty <tên công ty>”', '- Icon ⓘ: “Gồm mọi hàng hoá, kể cả hàng chưa kinh doanh tại công ty này; ẩn hàng tạm và hàng '
             'làm dịch vụ.”']),
           ('Cây catalog', 'Table/Grid', 'Enable', '–', '–', 'Tất cả hàng hoá',
            ['- Nhánh catalog kinh doanh kèm số hàng; “Chưa xếp catalog”', '- Có ô tìm trong cây, nút ẩn / hiện cây',
             '- Bấm nhánh → lọc bảng theo nhánh']),
           ('Ô tìm hàng', 'Textbox', 'Enable', 'Không giới hạn', 'Không', 'Trống',
            ['- Gợi ý “Tìm theo mã, tên hàng hoá, model, barcode, mã đặt hàng”', '- Enter → lọc bảng']),
           ('Công tắc Còn tồn', 'Checkbox', 'Enable', '–', 'Không', 'Tắt', '- Bật → chỉ hàng còn tồn bán được'),
           ('Công tắc Gồm hàng ngoài catalog', 'Checkbox', 'Enable', '–', 'Không', 'Bật',
            '- Bật sẵn vì phạm vi gồm mọi hàng hóa'),
           ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Mở thêm ô lọc nâng cao của cửa sổ'),
           ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Xóa điều kiện tìm của cửa sổ'),
           ('Bảng hàng hóa', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
            ['- Cột: STT, Ảnh, Mã hàng, Tên hàng hoá, Model, Thương hiệu, Loại sản phẩm, ĐVT, Tồn bán được…',
             '- Tồn bán được theo từng công ty, vd “TPE: 2,586 · TPHP: 28 · TPV: 1”']),
           ('Liên kết Tên hàng hoá', 'Link', 'Enable', '–', '–', 'Theo dữ liệu',
            '- Bấm → chọn hàng, đóng cửa sổ, tải thẻ kho'),
           ('Dòng “Hiển thị a–b / N” + phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1',
            ['- Số dòng/trang mặc định 20', '- Không có hàng: “Không có hàng hoá nào thoả bộ lọc”']),
           ('Dòng nhắc chân cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Bấm vào tên hàng để chọn”', '- Góc trái chân cửa sổ'),
           ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng cửa sổ, giữ hàng đang chọn trước đó')],
       ev=[('Bấm ô Hàng hóa', 'Click',
            'Before:\n– Lấy công ty ở ô Tồn theo công ty (trống → công ty làm việc).\n'
            'During:\n– Mở cửa sổ, nạp cây catalog và trang 1 hàng hóa (mọi hàng, kể cả chưa kinh doanh).\n'
            'After:\n– Cửa sổ hiện trên màn Thẻ kho; bộ lọc phía sau giữ nguyên.'),
           ('Gõ ô tìm hàng rồi Enter', 'Change',
            'Before:\n– Chuỗi tìm theo mã, tên, model, barcode, mã đặt hàng.\n'
            'During:\n– Lọc bảng hàng, cập nhật số đếm ở cây catalog.\n'
            'After:\n– Hiện kết quả từ trang 1; không có → “Không có hàng hoá nào thoả bộ lọc”.'),
           ('Bấm tên hàng hoá', 'Click',
            'Before:\n– Chế độ chọn 1 hàng.\n'
            'During:\n– Ghi “Mã - Tên” vào ô Hàng hóa, ghi tạm cùng bộ lọc.\n'
            'After:\n– Đóng cửa sổ, tải thẻ kho của hàng (về trang 1 nếu khác hàng cũ).'),
           ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
            'Before:\n– Không hỏi xác nhận (cửa sổ chỉ chọn, không nhập liệu).\nDuring:\n– Không đổi ô Hàng hóa.\n'
            'After:\n– Đóng cửa sổ; thẻ kho đang hiển thị giữ nguyên.')])
d.p('2.3.%d Mục đích thiết kế popup' % k)
d.bullets([
    'Trả lời câu hỏi: “mặt hàng tôi cần xem thẻ kho là mã nào?” — tìm được theo mã, tên, model, barcode, catalog, thấy tồn bán được '
    'từng công ty để chọn đúng hàng có phát sinh.',
    'Là cửa sổ nổi để giữ nguyên các ô lọc khác (Kỳ, công ty, kho, vị trí) — chọn xong là thẻ kho tải ngay, không phải chuyển màn. '
    'Dùng chung cửa sổ chọn hàng của hệ thống (người dùng chốt 22/10/2026) thay cho ô gõ tìm.',
    'Ràng buộc: chỉ chọn 1 hàng; phạm vi theo công ty ở ô Tồn theo công ty; hàng đã chọn là hàng của Dòng tiêu đề khối tổng hợp.',
    'Người dùng làm tiếp: tìm, lọc theo catalog, bật Còn tồn; mỗi lần mở là cửa sổ mới (không giữ chữ tìm lần trước).',
])
k += 1
d.p('2.3.%d Các biến thể theo con số bấm' % k)
d.popup_variant_table([
    ('Bấm ô Hàng hóa khi chưa chọn hàng', 'Mọi hàng hóa của công ty đang xem (gồm hàng chưa kinh doanh), trang 1', '“Chọn hàng hóa”',
     'Gồm hàng ngoài catalog bật sẵn; không có cột Giá'),
    ('Bấm ô Hàng hóa khi đã chọn hàng', 'Như trên; hàng đang chọn không bị đánh dấu riêng', '“Chọn hàng hóa”', 'Như trên'),
])

# ------------------------------------------------------------ 2.4
fr(4, 'Cài đặt bộ lọc',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị của màn Thẻ kho',
              mota='Người dùng chọn ô lọc nào hiện trong khối Bộ lọc thẻ kho và thứ tự của chúng; cấu hình lưu theo từng người dùng và '
                   'từng màn hình, không đổi dữ liệu báo cáo. Ô Nhà / Dãy / Khoang / Vị trí không nằm trong danh sách (chỉ hiện khi đã '
                   'chọn kho).',
              tacnhan=TN, dieukien=DK,
              chinh='1. Người dùng bấm Cài đặt bộ lọc ở đầu khối Bộ lọc thẻ kho.\n'
                    '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 7 ô theo thứ tự đang áp dụng: Kỳ, Hàng hóa, Tồn theo công ty, Kho, '
                    'Công ty thuê kho, Loại báo cáo, Số chứng từ / Diễn giải.\n'
                    '3. Người dùng tích / bỏ tích, kéo biểu tượng ⠿ để đổi thứ tự.\n'
                    '4. Bấm Lưu → hệ thống ghi cấu hình, đóng cửa sổ, hiện “Cập nhật thành công”, vẽ lại khối ô lọc; ô bị ẩn được '
                    'xóa giá trị.',
              phu='• Bấm Khôi phục mặc định → trả về thứ tự khai báo ban đầu, hiện hết (chưa lưu cho tới khi bấm Lưu).\n'
                  '• Bấm Đóng / (x) / click ra ngoài → bỏ thay đổi chưa lưu, không hỏi xác nhận.\n'
                  '• Lưu lỗi → hiện “Thao tác thất bại”, cửa sổ giữ nguyên.\n'
                  '• Ẩn ô bắt buộc (Hàng hóa, Tồn theo công ty) → không chọn được, báo cáo không tải; bật lại bằng cửa sổ này.',
              dacbiet='Cấu hình lưu trên máy chủ theo người dùng nên giữ khi tải lại trang, đổi trình duyệt.'),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               modal='Cài đặt bộ lọc'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Cài đặt bộ lọc”', '- Kèm biểu tượng bánh răng'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách ô lọc', 'Checkbox', 'Enable', 'Danh sách 7 giá trị', 'Không', 'Theo cấu hình đã lưu',
        ['- Kỳ', '- Hàng hóa', '- Tồn theo công ty', '- Kho', '- Công ty thuê kho', '- Loại báo cáo', '- Số chứng từ / Diễn giải',
         '- Mặc định: tích hết']),
       ('Biểu tượng kéo ⠿', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi thứ tự ô'),
       ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Ghi cấu hình; khóa trong lúc đang lưu'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về thứ tự ban đầu, tích hết; chưa lưu'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, bỏ thay đổi chưa lưu'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Như nút Đóng'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '“Màn hình này chưa khai báo trường lọc.” (không xảy ra với màn này)'),
       ('Khối ô lọc sau khi lưu', 'Label', 'Hiển thị', '–', '–', 'Theo cấu hình đã lưu', '- Ô bị ẩn không hiện, giá trị bị xóa')],
   ev=[('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Cấu hình đã nạp khi mở màn.\nDuring:\n– Liệt kê ô theo cấu hình đang áp dụng.\nAfter:\n– Mở cửa sổ “Cài đặt bộ lọc”.'),
       ('Kéo biểu tượng ⠿', 'Drag',
        'Before:\n– Mọi ô đều kéo được.\nDuring:\n– Đổi thứ tự trong cửa sổ.\nAfter:\n– Chưa áp tới khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình gắn với người dùng và màn Thẻ kho; không cần quyền riêng.\n'
        'During:\n– Ghi cấu hình; lỗi → “Thao tác thất bại”.\n' + ERR + '\n'
        'After:\n– Hiện “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối ô lọc; ô bị ẩn xóa giá trị và tải lại báo cáo.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Đặt lại thứ tự khai báo, tích hết.\nAfter:\n– Chưa lưu; phải bấm Lưu để áp dụng.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Bỏ thay đổi chưa lưu.\nAfter:\n– Đóng cửa sổ; lần mở sau hiện cấu hình đang áp dụng.')])

# ------------------------------------------------------------ 2.5
k = fr(5, 'Xem chi tiết chứng từ và lô / vị trí',
       rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
       intro=dict(ten='Bung lô / vị trí của chứng từ và mở chứng từ nguồn',
                  mota='Trong bảng chi tiết báo cáo, người dùng bung một chứng từ (mũi tên) hoặc chọn cấp bung cho cả trang để xem '
                       'từng lô / vị trí phát sinh; bấm Số chứng từ để mở màn chi tiết của chứng từ nguồn ở tab mới. Chỉ là cách xem, '
                       'không tải lại báo cáo.',
                  tacnhan=TN, dieukien=DK_REPORT,
                  chinh='1. Người dùng bấm mũi tên ở đầu ô Chứng từ / Lô của một dòng chứng từ.\n'
                        '2. Hệ thống hiện ngay dưới dòng đó các dòng Lô / vị trí (STT 1, 2…): số lô, vị trí, số nhập hoặc xuất.\n'
                        '3. Hoặc chọn ô cấp bung “Tất cả cấp (đến Lô / vị trí)” → bung mọi chứng từ của trang; “Chỉ chứng từ” → thu hết.\n'
                        '4. Người dùng bấm Số chứng từ (chữ xanh) → hệ thống mở màn chi tiết chứng từ nguồn ở tab mới.\n'
                        '5. Đóng tab chứng từ, quay lại tab Thẻ kho vẫn giữ nguyên bộ lọc, trang, cấp bung.',
                  phu='• Nhập tồn đầu (NHAP_TON_DAU_…) không có liên kết.\n'
                      '• Phiếu nhập lại, phiếu nhập kho điều chỉnh kiểm kê: liên kết mở màn ở hệ thống ERP; không cấu hình địa chỉ ERP '
                      'thì hiện chữ thường.\n'
                      '• Không có quyền xem chứng từ ở màn nguồn → màn nguồn báo theo quy tắc của màn đó.\n'
                      '• Đổi trang / đổi bộ lọc → áp lại cấp bung đang chọn cho dữ liệu mới (bung lẻ từng dòng bị bỏ).',
                  dacbiet=None),
       layout=dict(menu=MENU + ' => Bung chứng từ', shot=shot('06_transfer'),
                   shot_caption='Chứng từ điều chuyển vị trí PĐCVT-00584 bung 8 dòng lô / vị trí (chuyển ra N1-T2-KV, chuyển vào PTT-N1-KV7)'),
       extra=[(shot('05_level_all'), 'Ô chọn cấp bung = Tất cả cấp (đến Lô / vị trí)'),
              (shot('04_expand'), 'Bung 1 chứng từ PXK-12602')],
       ui_kw=dict(required=False),
       ui=[('Mũi tên bung / thu', 'Icon Button', 'Enable', '–', 'Thu',
            ['- Đầu ô Chứng từ / Lô của dòng chứng từ', '- Chữ gợi ý “Hiện lô / vị trí” / “Ẩn lô / vị trí”', '- Bấm → bung / thu dòng lô']),
           ('Ô chọn cấp bung', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Chỉ chứng từ',
            ['- Mặc định: Chỉ chứng từ', '- Lựa chọn: Chỉ chứng từ', '- Lựa chọn: Tất cả cấp (đến Lô / vị trí)', '- Áp cho trang đang xem']),
           ('Liên kết Số chứng từ', 'Link', 'Enable', '–', 'Theo dữ liệu',
            ['- Phiếu nhập kho (PNK-…) → màn chi tiết Phiếu nhập kho', '- Phiếu xuất kho (PXK-…) → màn chi tiết Phiếu xuất kho',
             '- Điều chuyển vị trí (PĐCVT-…) → màn chi tiết Phiếu điều chuyển vị trí',
             '- Phiếu xuất điều chỉnh sai số liệu → màn chi tiết Phiếu xuất điều chỉnh sai số liệu',
             '- Phiếu xuất kho điều chỉnh kiểm kê → màn chi tiết Phiếu xuất kho điều chỉnh kiểm kê',
             '- Phiếu nhập lại (PNL-…), Phiếu nhập kho điều chỉnh kiểm kê → mở hệ thống ERP',
             '- Luôn mở TAB MỚI']),
           ('Dòng Lô / vị trí — cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- 1, 2… trong chứng từ'),
           ('Dòng Lô / vị trí — cột Chứng từ / Lô', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Số lô, vd “TPE-28/11/2025-2715-38465-59-1-18830”', '- Thụt lề, vạch cấp bên trái']),
           ('Dòng Lô / vị trí — cột Vị trí', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Mã vị trí của lô'),
           ('Dòng Lô / vị trí — cột Nhập', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', '- Số nhập vào vị trí (thay đổi dương)'),
           ('Dòng Lô / vị trí — cột Xuất', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', '- Số xuất khỏi vị trí (thay đổi âm)'),
           ('Dòng Lô / vị trí — cột Ngày, Diễn giải, SL tồn, NVKD', 'Table/Grid', 'Read-only', '–', 'Trống', '- Để trống ở dòng lô'),
           ('Dòng chứng từ điều chuyển', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Chữ nhỏ “Điều chuyển vị trí” sau số chứng từ', '- Nhập = tổng chuyển vào, Xuất = tổng chuyển ra',
             '- Mỗi lô 2 dòng: chuyển ra (Xuất) tại vị trí cũ, chuyển vào (Nhập) tại vị trí mới']),
           ('Ô Vị trí của dòng chứng từ nhiều lô', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Chữ xám “<n> lô / vị trí”'),
           ('Màn chứng từ nguồn', 'Link', 'Hiển thị', '–', 'Theo dữ liệu',
            '- Mở ở tab mới; nút Quay lại bên đó về danh sách của màn nguồn')],
       ev=[('Bấm mũi tên ở dòng chứng từ', 'Click',
            'Before:\n– Dòng chứng từ thuộc trang đang xem.\nDuring:\n– Đảo trạng thái bung của riêng dòng đó.\n'
            'After:\n– Hiện / ẩn các dòng Lô / vị trí; không tải lại, không đổi phân trang.'),
           ('Đổi ô chọn cấp bung', 'Change',
            'Before:\n– Chọn khác giá trị đang có.\nDuring:\n– Tất cả cấp: bung mọi chứng từ của trang; Chỉ chứng từ: thu hết.\n'
            'After:\n– Áp lại mỗi khi đổi trang / tải lại dữ liệu.'),
           ('Bấm Số chứng từ', 'Click',
            'Before:\n– Chứng từ có màn xem (không phải Nhập tồn đầu).\n– Quyền xem chứng từ do màn nguồn kiểm.\n'
            'During:\n– Xác định màn theo loại chứng từ (HRM hoặc hệ thống ERP).\n'
            'After:\n– Mở màn chi tiết chứng từ ở tab mới; tab Thẻ kho giữ nguyên.'),
           ('Đổi trang khi đang bung', 'Click',
            'Before:\n– Có dòng đang bung lẻ.\nDuring:\n– Áp lại cấp bung đang chọn cho trang mới.\n'
            'After:\n– Dòng bung lẻ của trang cũ không được giữ.')])
d.p('2.5.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('“Tập dữ liệu” là các dòng nhật ký tồn theo vị trí của chứng từ đang bung, trong phạm vi lọc của báo cáo (mục 2.1.6).')
d.data_table([
    ('Dòng Lô / vị trí', 'Mỗi dòng nhật ký: một lô tại một vị trí, thứ tự ghi.', '—'),
    ('Cột Nhập / Xuất (dòng lô)', 'Thay đổi dương → Nhập; âm → Xuất (trị tuyệt đối).', TIP_IMP + ' / ' + TIP_EXP),
    ('Khớp số', 'Chứng từ nhập: tổng Nhập các dòng lô = Nhập dòng chứng từ; chứng từ xuất: tổng Xuất các dòng lô = Xuất dòng chứng từ '
                '(nếu chứng từ vừa có lô tăng vừa có lô giảm thì Xuất dòng chứng từ = trị tuyệt đối tổng thay đổi); điều chuyển: tổng '
                'Nhập = tổng chuyển vào, tổng Xuất = tổng chuyển ra.', '—'),
    ('Số lô / vị trí', '“<n> lô / vị trí” ở dòng chứng từ = số dòng bung ra.', '—'),
])

# ------------------------------------------------------------ 2.6
k = fr(6, 'In thẻ kho', usecase=('FR-06', 'In thẻ kho', 'io', A_TK),
       rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
       intro=dict(ten='In thẻ kho',
                  mota='Người dùng bấm In danh sách, chọn bản in Đầy đủ (có cột NVKD) hoặc Rút gọn và các cột cần in, xem trước rồi in. '
                       'Bản in dùng đúng bộ lọc của báo cáo đang hiển thị, toàn bộ chứng từ trong kỳ (không riêng trang đang xem), '
                       'tiêu đề 2 tầng và 5 dòng tổng hợp như hệ thống ERP, letterhead theo công ty ở ô Tồn theo công ty.',
                  tacnhan=TN, dieukien=DK_REPORT,
                  chinh='1. Người dùng bấm In danh sách.\n'
                        '2. Hệ thống mở cửa sổ “In báo cáo”: chọn sẵn Đầy đủ, tích hết các cột.\n'
                        '3. Người dùng chọn bản in, bỏ / tích cột (STT, Ngày chứng từ, Số chứng từ luôn in), bấm In.\n'
                        '4. Hệ thống đóng cửa sổ chọn, mở cửa sổ “Xem trước thẻ kho” (khổ ngang), dựng bản in: letterhead, tiêu đề '
                        '“THẺ KHO”, Hàng hóa, Kho, Thời gian, bảng (Đơn vị tính, Tồn đầu kỳ, Nhập trong kỳ, Xuất trong kỳ, Tồn cuối kỳ, '
                        'rồi từng chứng từ gộp ô theo lô), chỗ ký Người lập.\n'
                        '5. Người dùng bấm In trên cửa sổ xem trước → hộp thoại in của trình duyệt.',
                  phu='• Chưa có báo cáo (thiếu ô bắt buộc) → không mở cửa sổ, bật chữ đỏ dưới ô thiếu.\n'
                      '• Bỏ tích hết cột rồi bấm In → báo đỏ trong cửa sổ, không đóng.\n'
                      '• Tổng số dòng lô vượt 2.000 → cửa sổ xem trước chỉ hiện ' + M_LIMIT + ', ẩn nút In.\n'
                      '• Không có dữ liệu → ' + M_NOPRINT + '\n'
                      '• Thiếu quyền → ' + NOPERM + '\n'
                      '• Bấm Hủy / (x) / click ra ngoài cửa sổ chọn → đóng, không in.',
                  dacbiet='Trần in 2.000 dòng lô (mỗi chứng từ ít nhất 1 dòng). Dùng mẫu in “Báo cáo thẻ kho” của hệ thống nếu đã '
                          'soạn, chưa soạn thì dùng mẫu dựng sẵn cùng bố cục.'),
       layout=dict(menu=MENU + ' => In danh sách', shot=shot('09_print_modal'), shot_caption='Cửa sổ In báo cáo — chọn bản in và cột in',
                   modal='In báo cáo'),
       extra=[(shot('10_print_preview'), 'Cửa sổ Xem trước thẻ kho (bản Đầy đủ)')],
       ui=[('Nút In danh sách', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đầu khối Bộ lọc thẻ kho, biểu tượng máy in'),
           ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“In báo cáo”', '- Có nút (x) đóng'),
           ('Lựa chọn bản in', 'Radio', 'Enable', 'Danh sách 2 giá trị', 'Có', 'Đầy đủ',
            ['- Mặc định: Đầy đủ — “Có cột NVKD (nhân viên lập chứng từ).”', '- Lựa chọn: Rút gọn — “Không có cột NVKD.”',
             '- Đổi bản in → danh sách cột đổi theo, tích lại hết']),
           ('Chọn cột in', 'Checkbox', 'Enable', 'Danh sách 8 giá trị', 'Có (≥ 1 cột)', 'Tích hết',
            ['- Diễn giải, Nhập, Xuất, Lô, Vị trí, SL theo vị trí, SL tồn, NVKD (NVKD chỉ ở Đầy đủ)',
             '- Icon ⓘ: “Cột STT, Ngày chứng từ, Số chứng từ luôn được in.”', '- “Chọn tất cả” ở góc, bán chọn khi tích 1 phần']),
           ('Thông báo chưa chọn cột', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- Chữ đỏ khi bỏ hết cột mà bấm In'),
           ('Nút In (cửa sổ chọn)', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Mở cửa sổ xem trước'),
           ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không in'),
           ('Cửa sổ Xem trước thẻ kho', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
            ['- Tiêu đề “Xem trước thẻ kho”, khổ ngang', '- Đang tải: “Đang tải dữ liệu in…”']),
           ('Nội dung bản in', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
            ['- Letterhead công ty ở ô Tồn theo công ty', '- “BÁO CÁO THẺ KHO” / “THẺ KHO”, Hàng hóa: mã - tên, Kho, Từ ngày / Đến ngày',
             '- Tiêu đề 2 tầng: Số lượng (Nhập, Xuất), Chi tiết (Lô, Vị trí, SL theo vị trí)',
             '- 5 dòng đầu: Đơn vị tính, Tồn đầu kỳ, Nhập trong kỳ, Xuất trong kỳ, Tồn cuối kỳ',
             '- Mỗi chứng từ gộp ô STT, Ngày, Số chứng từ, Diễn giải, SL tồn, NVKD theo số lô']),
           ('Nút In (xem trước)', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
            '- Khóa khi đang tải / vượt trần; bấm → hộp thoại in của trình duyệt'),
           ('Thông báo vượt trần / rỗng', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + M_LIMIT, '- ' + M_NOPRINT]),
           ('Nút (x) cửa sổ xem trước', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng xem trước')],
       ev=[('Bấm In danh sách', 'Click',
            'Before:\n– Kiểm tra đã có báo cáo; chưa có → bật chữ đỏ ô bắt buộc, dừng.\n'
            'During:\n– Mở cửa sổ In báo cáo, chọn Đầy đủ, tích hết cột.\nAfter:\n– Chờ người dùng chọn.'),
           ('Đổi bản in / tích cột', 'Change',
            'Before:\n– Cửa sổ In báo cáo đang mở.\nDuring:\n– Đổi bản in → nạp bộ cột của bản đó, tích hết.\n'
            'After:\n– Đã tích ≥ 1 cột thì tắt chữ đỏ.'),
           ('Bấm In (cửa sổ chọn)', 'Click',
            'Before:\n– Kiểm tra quyền “' + Q1 + '”.\n– Nếu không có quyền → hiển thị ' + NOPERM + ' và dừng xử lý.\n'
            '– Bỏ hết cột → chữ đỏ, không đóng.\n'
            'During:\n– Lấy bộ lọc của báo cáo đang hiển thị + bản in + cột; máy chủ tính lại toàn bộ thẻ kho, đếm dòng lô.\n'
            '– Vượt 2.000 dòng → không dựng bản in, trả lời nhắc thu hẹp bộ lọc.\n' + ERR + '\n'
            'After:\n– Mở “Xem trước thẻ kho” với bản in; vượt trần hiện ' + M_LIMIT + '; rỗng hiện ' + M_NOPRINT + '.'),
           ('Bấm In (xem trước)', 'Click',
            'Before:\n– Bản in đã tải xong.\nDuring:\n– Gửi nội dung sang trình duyệt in (khổ ngang).\nAfter:\n– Hộp thoại in của trình duyệt.'),
           ('Bấm Hủy, (x) hoặc click ra ngoài cửa sổ', 'Click',
            'Before:\n– Không hỏi xác nhận.\nDuring:\n– Đóng cửa sổ.\nAfter:\n– Màn Thẻ kho giữ nguyên bộ lọc, trang.')])
d.p('2.6.%d Mục đích thiết kế popup' % k)
d.bullets([
    'Trả lời câu hỏi: “in thẻ kho này theo mẫu nào, những cột nào?” — cùng một thẻ kho có bản Đầy đủ (kèm NVKD) để lưu hồ sơ nội bộ và '
    'bản Rút gọn để gửi bên ngoài.',
    'Là cửa sổ nổi để giữ nguyên bộ lọc và trang đang xem; xem trước trước khi in tránh in nhầm.',
    'Ràng buộc khớp số: bản in dùng đúng bộ lọc của báo cáo đang hiển thị (cả ô Số chứng từ / Diễn giải), 5 dòng đầu = khối tổng hợp, '
    'SL tồn từng chứng từ = cột SL tồn trên màn.',
    'Người dùng làm tiếp: đổi bản in / cột rồi in lại; mỗi lần mở cửa sổ về mặc định Đầy đủ, tích hết.',
])
k += 1
d.p('2.6.%d Các biến thể theo con số bấm' % k)
d.popup_variant_table([
    ('Bản in Đầy đủ', 'Mọi chứng từ của báo cáo đang hiển thị, có cột NVKD', '“Xem trước thẻ kho”', 'Cột STT, Ngày chứng từ, Số chứng từ cố định'),
    ('Bản in Rút gọn', 'Như trên, không có cột NVKD', '“Xem trước thẻ kho”', 'Như trên; không có NVKD trong danh sách cột'),
])

# ------------------------------------------------------------ 2.7
fr(7, 'Xuất Excel', usecase=('FR-07', 'Xuất Excel', 'io', A_TK),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Xuất thẻ kho ra Excel',
              mota='Người dùng bấm Xuất Excel, chọn kiểu Đầy đủ / Rút gọn rồi tải file “bao_cao_the_kho.xlsx” gồm TOÀN BỘ chứng từ của '
                   'báo cáo đang hiển thị (không riêng trang đang xem). File có letterhead theo công ty ở ô Tồn theo công ty, tiêu đề '
                   '“Thẻ kho”, Hàng hóa (mã - tên - ĐVT), Kho, Từ ngày / Đến ngày và bảng 2 tầng như bản in; luôn đủ cột của kiểu.',
              tacnhan=TN, dieukien=DK_REPORT,
              chinh='1. Người dùng bấm Xuất Excel ở đầu khối Bộ lọc thẻ kho.\n'
                    '2. Hệ thống mở cửa sổ “Xuất Excel thẻ kho”, chọn sẵn Đầy đủ.\n'
                    '3. Người dùng chọn kiểu, bấm Xuất Excel.\n'
                    '4. Hệ thống khóa nút, đổi chữ “Đang xuất…” kèm biểu tượng quay và thanh tải, máy chủ tính lại thẻ kho theo bộ lọc '
                    'đang hiển thị, dựng file.\n'
                    '5. Trình duyệt tải file “bao_cao_the_kho.xlsx”, cửa sổ đóng.',
              phu='• Chưa có báo cáo (thiếu ô bắt buộc) → không mở cửa sổ, bật chữ đỏ dưới ô thiếu.\n'
                  '• Lỗi khi xuất → hiện ' + M_EXPORT_ERR + ', cửa sổ giữ nguyên để bấm lại.\n'
                  '• Thiếu quyền → ' + NOPERM + ' (không hiện thêm “Lỗi khi xuất Excel.”).\n'
                  '• Kỳ không có chứng từ → file vẫn tải về, chỉ có 5 dòng tổng hợp.\n'
                  '• Bấm Hủy / (x) / click ra ngoài → đóng, không xuất; đang xuất thì bấm lại Xuất không có tác dụng.',
              dacbiet='Excel không qua bước chọn cột (luôn đủ cột của kiểu). Số lượng là ô số thật, phân cách hàng nghìn, tối đa 2 số '
                      'lẻ; ô 0 để trống trừ dòng tổng hợp và cột SL tồn.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('11_export'), shot_caption='Cửa sổ Xuất Excel thẻ kho', modal='Xuất Excel thẻ kho'),
   ui=[('Nút Xuất Excel (khối lọc)', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Viền xanh lá, biểu tượng Excel', '- Đang xuất: “Đang xuất…”, khóa']),
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Xuất Excel thẻ kho”', '- Có nút (x)'),
       ('Nhãn Kiểu xuất', 'Label', 'Hiển thị', '–', '–', '“Kiểu xuất”', '–'),
       ('Kiểu xuất', 'Radio', 'Enable', 'Danh sách 2 giá trị', 'Có', 'Đầy đủ',
        ['- Mặc định: Đầy đủ — “Có cột NVKD (nhân viên lập chứng từ).”', '- Lựa chọn: Rút gọn — “Không có cột NVKD.”',
         '- Mở lại cửa sổ → về Đầy đủ']),
       ('Nút Xuất Excel (cửa sổ)', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → tải file', '- Đang xuất: “Đang xuất…”, biểu tượng quay, khóa']),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng cửa sổ, không xuất'),
       ('File Excel — tên', 'Label', 'Hiển thị', '–', '–', '“bao_cao_the_kho.xlsx”', '–'),
       ('File Excel — phần đầu', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu',
        ['- Dòng 1: logo / letterhead rộng bằng bảng', '- “Thẻ kho”; “Hàng hóa: mã - tên - ĐVT”; “Kho: …”; “Từ ngày: … Đến ngày: …”']),
       ('File Excel — bảng', 'Table/Grid', 'Hiển thị', '–', '–', 'Theo dữ liệu',
        ['- STT, Ngày chứng từ, Số chứng từ, Diễn giải, Số lượng (Nhập, Xuất), Chi tiết (Lô, Vị trí, SL theo vị trí), SL tồn, NVKD (Đầy đủ)',
         '- 5 dòng tổng hợp đầu bảng', '- Chứng từ gộp ô theo lô']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + M_EXPORT_ERR, '- ' + NOPERM]),
       ('Thanh tải trang', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- Chạy trong lúc đang xuất')],
   ev=[('Bấm Xuất Excel (khối lọc)', 'Click',
        'Before:\n– Kiểm tra đã có báo cáo; chưa có → bật chữ đỏ ô bắt buộc, dừng.\n'
        'During:\n– Mở cửa sổ “Xuất Excel thẻ kho”, chọn Đầy đủ.\nAfter:\n– Chờ người dùng chọn kiểu.'),
       ('Bấm Xuất Excel (cửa sổ)', 'Click',
        'Before:\n– Kiểm tra quyền “' + Q1 + '”.\n– Nếu không có quyền → hiển thị ' + NOPERM + ' và dừng xử lý.\n'
        '– Đang xuất → bỏ qua lần bấm.\n'
        'During:\n– Lấy bộ lọc của báo cáo đang hiển thị + kiểu xuất; máy chủ tính lại toàn bộ thẻ kho, dựng file.\n'
        '– Lỗi → hiển thị ' + M_EXPORT_ERR + ', giữ cửa sổ.\n' + ERR + '\n'
        'After:\n– Tải file “bao_cao_the_kho.xlsx”, đóng cửa sổ, mở khóa nút.'),
       ('Đổi Kiểu xuất', 'Change',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Ghi nhận kiểu.\nAfter:\n– Áp cho lần xuất kế tiếp.'),
       ('Bấm Hủy, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Đóng cửa sổ.\nAfter:\n– Không xuất; màn giữ nguyên.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Thẻ kho; không lặp lại các quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng', lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Nguồn số liệu và chứng từ được tính', [
        '– Nhật ký thay đổi tồn theo vị trí của hàng; mỗi chứng từ lên thẻ kho khi đã ghi tồn: phiếu nhập kho / xuất kho / nhập, xuất '
        'kho điều chỉnh kiểm kê từ lúc gửi; điều chuyển vị trí khi Đã chuyển; phiếu nhập lại, phiếu xuất điều chỉnh sai số liệu khi '
        'lập; tồn đầu kỳ khi khai báo.',
        '– Không duyệt phiếu sau đó không hoàn tồn → vẫn trên thẻ kho.'], ['Xem thẻ kho', 'In', 'Xuất Excel']),
    ('BR-02', 'Phạm vi công ty / kho / vị trí', [
        '– Không chọn kho: mọi vị trí thuộc kho của công ty, chỉ tồn ghi nhận cho công ty đó.',
        '– Chọn kho: vị trí của các kho đã chọn, tồn ghi nhận cho công ty thuê đã tick (không tick = mọi công ty thuê của kho đó).',
        '– Nhà / Dãy / Khoang / Vị trí: theo cấp sâu nhất được tick.'], ['Tìm kiếm và lọc', 'Xem thẻ kho']),
    ('BR-03', 'Công thức tồn', [
        '– Tồn đầu kỳ = tổng thay đổi trước ngày đầu kỳ.',
        '– Nhập / Xuất trong kỳ = tổng thay đổi dương / trị tuyệt đối tổng thay đổi âm trong kỳ, gồm cả điều chuyển vị trí.',
        '– Tồn cuối kỳ = Tồn đầu kỳ + Nhập − Xuất = SL tồn dòng cuối; Tồn đầu kỳ này = Tồn cuối kỳ liền trước.'],
     ['Xem thẻ kho', 'In', 'Xuất Excel']),
    ('BR-04', 'Gom dòng chứng từ và SL tồn lũy kế', [
        '– Gom theo (phiếu, loại chứng từ); mỗi lần khai tồn đầu là 1 chứng từ “NHAP_TON_DAU_<số>”.',
        '– Có lô giảm → chứng từ xuất (Xuất = trị tuyệt đối tổng); không → nhập; điều chuyển: tổng chuyển vào / ra.',
        '– SL tồn = tồn đầu kỳ + cộng dồn thay đổi tới hết chứng từ, theo thời điểm ghi nhận tăng dần.'], ['Xem thẻ kho']),
    ('BR-05', 'Loại báo cáo “Không nhặt điều chuyển”', [
        '– Bỏ mọi dòng điều chuyển vị trí khỏi tồn đầu kỳ, nhập, xuất, bảng và đếm chứng từ.',
        '– Điều chuyển trong cùng phạm vi lọc có tổng = 0 nên tồn đầu / tồn cuối không đổi, chỉ Nhập / Xuất giảm.'],
     ['Tìm kiếm và lọc', 'Xem thẻ kho']),
    ('BR-06', 'Ô Số chứng từ / Diễn giải chỉ lọc hiển thị', [
        '– Lọc sau khi cộng dồn: khối tổng hợp, dòng TỔNG, SL tồn từng dòng giữ nguyên; “Hiển thị a–b / N” theo số dòng khớp.',
        '– Khớp một phần, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối.'], ['Tìm kiếm và lọc', 'In', 'Xuất Excel']),
    ('BR-07', 'Ô bắt buộc và kỳ', [
        '– Hàng hóa, Tồn theo công ty bắt buộc; Kỳ Tuỳ chọn bắt buộc đủ Từ ngày / Đến ngày, Đến ngày ≥ Từ ngày.',
        '– Thiếu thì không tải báo cáo, không in / xuất.',
        '– Năm nay = 01/01 → 31/12 (hệ thống ERP: 01/01 → hôm nay; số liệu như nhau).'], ['Tìm kiếm và lọc']),
    ('BR-08', 'Phân quyền', [
        '– “' + Q1 + '”: điều kiện cho mọi chức năng; thiếu → ' + NOPERM,
        '– “' + V1 + '”: chọn mọi công ty; không có → luôn công ty của người dùng (máy chủ bỏ qua công ty gửi lên).',
        '– Super admin được miễn.'], ['Mọi chức năng']),
    ('BR-09', 'Đơn vị tính và định dạng số', [
        '– Mọi số theo ĐVT cơ sở của hàng (bỏ ô ĐVT 27/10/2026, như hệ thống ERP).',
        '– Phân cách hàng nghìn dấu phẩy, làm tròn 2 số lẻ; ô 0 để trống trừ Tồn cuối kỳ, SL tồn, dòng tổng hợp.'],
     ['Xem thẻ kho', 'In', 'Xuất Excel']),
    ('BR-10', 'In / Excel cùng nguồn số', [
        '– In và Excel dùng bộ lọc của báo cáo đang hiển thị, toàn bộ chứng từ, cùng cách tính với màn.',
        '– In: trần 2.000 dòng lô; Excel không trần, tên file “bao_cao_the_kho.xlsx”; letterhead theo công ty ở ô Tồn theo công ty.'],
     ['In thẻ kho', 'Xuất Excel']),
    ('BR-11', 'Liên kết chứng từ nguồn', [
        '– Phiếu nhập kho, xuất kho, điều chuyển vị trí, xuất điều chỉnh sai số liệu, xuất kho điều chỉnh kiểm kê → màn HRM ở tab mới.',
        '– Phiếu nhập lại, nhập kho điều chỉnh kiểm kê → hệ thống ERP; Nhập tồn đầu không có liên kết.'],
     ['Xem chi tiết chứng từ và lô / vị trí']),
    ('BR-12', 'Ghi nhớ bộ lọc', [
        '– Bộ lọc (kể cả hàng hóa, tick vị trí) ghi tạm 10 phút trên trình duyệt; F5 khôi phục; rời màn hoặc Xóa lọc → xóa.',
        '– Cài đặt bộ lọc lưu trên máy chủ theo người dùng.'], ['Tìm kiếm và lọc', 'Cài đặt bộ lọc']),
    ('BR-13', 'Không ghi dữ liệu, không lịch sử', [
        '– Màn chỉ đọc: không thêm / sửa / xóa / khóa, không ghi lịch sử; dòng thẻ kho không có trạng thái, không có khóa / trùng.',
        '– Muốn đổi số liệu phải sửa / lập chứng từ ở màn nguồn (Phần 5).'], ['Xem thẻ kho']),
    ('BR-14', 'Khác hệ thống ERP (có chủ đích)', [
        '– Lọc Nhà / Dãy / Khoang đúng cấp sâu nhất được tick; SL tồn chia theo ĐVT; tồn cuối gồm mọi thay đổi trong phạm vi lọc.',
        '– Dòng điều chuyển xếp Nhập / Xuất theo dấu; bản in / Excel gom theo (phiếu, loại) như màn; thêm ô Kỳ, ô Số chứng từ / Diễn '
        'giải, phân trang, letterhead theo công ty đang xem.'], ['Xem thẻ kho', 'In', 'Xuất Excel']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây ghi dữ liệu mà Thẻ kho đọc (chứng từ làm thay đổi tồn theo vị trí, danh mục phạm vi) hoặc đọc cùng nguồn tồn '
    'kho dùng để đối chiếu số với Thẻ kho; không màn nào mở sang Thẻ kho. Thẻ kho chỉ đọc, không ghi ngược màn nào.')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', 'Phiếu nhập kho (ghi tồn khi gửi phiếu → dòng chứng từ Nhập; Số chứng từ mở màn này)', 'Kho -> Nhập kho'),
    ('2', 'Tài chính', 'Phiếu xuất kho (trừ tồn khi gửi phiếu → dòng chứng từ Xuất; Số chứng từ mở màn này)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('3', 'Kho', 'Phiếu điều chuyển vị trí (khi Đã chuyển → dòng điều chuyển chuyển ra / chuyển vào; Số chứng từ mở màn này)',
     'Kho -> Điều chuyển'),
    ('4', 'Kho', 'Phiếu xuất điều chỉnh sai số liệu (xuất lại → dòng Xuất; Số chứng từ mở màn này)', 'Kho -> Xuất kho'),
    ('5', 'Kho', 'Phiếu xuất kho điều chỉnh kiểm kê (trừ tồn khi gửi → dòng Xuất; Số chứng từ mở màn này)', 'Kho -> Xuất kho'),
    ('6', 'Kho', 'Phiếu nhập kho điều chỉnh kiểm kê (cộng tồn khi gửi → dòng Nhập; Số chứng từ hiện mở hệ thống ERP)', 'Kho -> Nhập kho'),
    ('7', 'Tài chính', 'Phiếu nhập lại (cộng lại tồn đã xuất → dòng Nhập; Số chứng từ hiện mở hệ thống ERP)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('8', 'Kho', 'Khai báo tồn kho đầu kỳ (dòng “Nhập tồn đầu”; sửa / xóa khai báo đổi tồn đầu và SL tồn lũy kế)', 'Kho -> Tồn kho đầu kỳ'),
    ('9', 'Kho', 'Kho vật lý, Kho kế toán (danh sách ô Kho, Công ty thuê kho)', 'Kho -> Danh mục'),
    ('10', 'Kho', 'Nhà kho, Dãy, Khoang, Vị trí (4 cột tick vị trí; mã vị trí ở cột Vị trí)', 'Kho -> Danh mục'),
    ('11', 'Hệ thống ERP', 'Danh mục hàng hóa (mã, tên, ĐVT và hệ số ĐVT của hàng)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
    ('12', 'Kho', 'Tổng hợp xuất nhập tồn (đọc cùng nguồn — cùng kho, cùng kỳ: tồn đầu / nhập / xuất / tồn cuối khớp Thẻ kho)',
     'Kho -> Báo cáo kho'),
    ('13', 'Kho', 'Báo cáo tồn kho chi tiết theo mặt hàng, Báo cáo tồn kho tổng hợp theo mặt hàng (đối chiếu tồn cuối kỳ của công ty)',
     'Kho -> Báo cáo kho'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)

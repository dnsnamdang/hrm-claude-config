# -*- coding: utf-8 -*-
"""SRS màn "Báo cáo tồn kho tổng hợp theo mặt hàng" (phân hệ Kho › Báo cáo kho) — form chuẩn + quy định màn BÁO CÁO (bảng Cách lấy
dữ liệu, bảng popup, Mục đích thiết kế popup) + chuẩn 04/11 (Mục lục trang riêng căn giữa, Phần 5 bảng 4 cột).

Chạy: python gen_srs.py  → SRS - Báo cáo tồn kho tổng hợp theo mặt hàng.docx
Khuôn chép: ../bao-cao-ton-kho-chi-tiet-mat-hang/gen_srs.py (06/11) + ../bao-cao-ton-kho-theo-vi-tri/gen_srs.py (07/11) — cùng 3 quyền,
  cùng nguồn tồn.
Nguồn đọc 07/11/2026 (nhánh develop cả 2 repo):
  FE  pages/warehouse/stock-general-product/{index.vue, components/StockGeneralSummary.vue, components/StockGeneralTable.vue},
      pages/warehouse/stock-card/components/{ExportModeModal.vue, format.js}, components/report/V2BaseReportPrintModal.vue,
      components/print/ReportPrintPreviewModal.vue, V2ProductPickerModal, V2BasePickerField, V2BaseSmartFilterPanel,
      utils/filterRequiredErrors.js, utils/mixins/filterStateMixin.js, components/subsystem-menu/warehouse.js.
  BE  Modules/Finance/{Services/StockGeneralProductReportService.php, Services/WarehouseStockReportService.php,
      Services/StockGeneralProductPrintService.php, Http/Controllers/V1/StockGeneralProductController.php,
      Exports/StockGeneralProductExport.php, Resources/views/{exports/stock_general_product, prints/stock-general-product}.blade.php,
      Routes/api.php (nhóm stock-general-product, chỉ GET)}.
  Tài liệu: design.md, plan.md (#11874), spec docs/superpowers/specs/gop-db/2026-10-23-bao-cao-ton-kho-tong-hop-mat-hang-design.md.
Ảnh: ./bctkth_shots — dev-hrm 07/11/2026, DNS Admin (_capture/capture.js, chặn mọi yêu cầu ghi: 0 lọt). Bộ lọc mẫu công ty CN Hải
  Phòng, toàn bộ 4 kho (CB, HP, KĐN-ALM, NM), nạp qua bộ nhớ trình duyệt như F5. Ảnh popup Chọn hàng hóa chụp với công ty TPE (với CN
  Hải Phòng dev báo lỗi 403). Không bật cờ giả nào.
Đối soát số dev 07/11 (_capture/doisoat.js, chỉ GET): ENEO-700-V5231, kho HP, công ty thuê TPHP = 20 = Báo cáo tồn kho chi tiết theo mặt
  hàng (20) = Báo cáo tồn kho theo vị trí (KHOANG1 20) = Thẻ kho 01/01–07/11/2026 (70 + 496 − 546 = 20); 4 kho CN Hải Phòng = 47 (HP 20 +
  CB 27). ENEO-640-V5236, kho PTT, TPE = 3,197 = chi tiết = vị trí = Thẻ kho Năm nay (15,141 + 11,404 − 23,348); 31/12/2025 = 15,141.
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

TEN = 'Báo cáo tồn kho tổng hợp theo mặt hàng'
SHOTS = os.path.join(HERE, 'bctkth_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Kho => Báo cáo kho => Báo cáo tồn kho tổng hợp theo mặt hàng'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Báo cáo tồn kho tổng hợp theo mặt hàng.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
V1 = 'Xem báo cáo tồn kho theo tổng công ty'
V2 = 'Xem báo cáo tồn kho theo công ty'
V3 = 'Xem báo cáo tồn kho theo kho'
NOPERM = '“Bạn không có quyền truy cập chức năng này.”'
M_LOADERR = '“Lỗi khi tải dữ liệu.”'
M_KHO = '“Vui lòng chọn kho”'
M_NGAY = '“Vui lòng chọn ngày”'
M_CTY = '“Vui lòng chọn tồn theo công ty”'
M_EMPTY = '“Không có mặt hàng nào khớp bộ lọc.”'
M_CHONKHO = '“Chọn kho để xem báo cáo.”'
M_XLS_ERR = '“Lỗi khi xuất Excel.”'
M_NOCOL = '“Vui lòng chọn ít nhất 1 cột để in”'
M_NOPRINT = '“Không có dữ liệu để in”'
M_LIMIT = ('“Danh sách có N dòng, vượt mức in tối đa 2.000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng '
           'thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.”')
FILE = 'bao_cao_ton_kho_tong_hop_mat_hang.xlsx'

A = 'Thủ kho / Kế toán kho'
TN = ('Người dùng có quyền thực hiện chức năng: có ít nhất 1 trong 3 quyền “%s”, “%s”, “%s” (hoặc là Super admin); phạm vi kho theo '
      'quyền cao nhất (Phần 2).' % (V1, V2, V3))
DK = ('1. Người dùng đăng nhập thành công.\n'
      '2. Người dùng có 1 trong 3 quyền xem báo cáo tồn kho (hoặc là Super admin).\n'
      '3. Có ít nhất 1 kho đang hoạt động trong phạm vi quyền thuộc công ty đang xem.')
TIP_PURPOSE = ('MỤC ĐÍCH BÁO CÁO • Xem tồn của từng mặt hàng trên 1 hoặc nhiều kho, tính đến ngày đã chọn • Chia theo công ty thuê kho '
               '• Lọc thêm theo nhóm, tính chất, loại, thương hiệu, hãng sản xuất, hàng hóa, hợp đồng')
TIP_TITLE = 'Tồn của từng mặt hàng trên các kho đã chọn tính đến ngày đã chọn, chia theo công ty thuê kho.'
TIP_GOAL = ('BÁO CÁO TỒN KHO TỔNG HỢP THEO MẶT HÀNG • Tồn của từng mặt hàng trên các kho đang chọn, tính đến hết ngày đã chọn • Chia '
            'theo công ty thuê kho • Số liệu tính tại <ngày giờ>')
TIP_MH = ('MẶT HÀNG • Mặt hàng còn tồn: tổng tồn các công ty thuê kho đang lọc khác 0 • Kho đang xem: số kho đang chọn ở bộ lọc • Công '
          'ty thuê kho có tồn: số công ty còn ít nhất 1 mặt hàng tồn (dòng này chỉ có với quyền tổng công ty)')
TIP_CT = 'THEO CÔNG TY THUÊ KHO • Số mặt hàng mỗi công ty thuê kho còn tồn, tính đến ngày đã chọn'
TIP_TONG = ('TỔNG • Số mặt hàng còn tồn trên các kho đang chọn, tính đến ngày đã chọn • Không cộng số lượng vì mỗi mặt hàng một đơn '
            'vị tính')
TIP_DVT = ('ĐVT • Chọn ĐVT riêng từng mặt hàng — số lượng của hàng đó quy đổi theo hệ số, In / Xuất Excel theo ĐVT đã chọn')
TIP_SL = 'SL TỒN • Tổng tồn các công ty thuê kho đang lọc, trên mọi kho đang chọn, tính đến hết ngày đã chọn'
TIP_CHITIET = 'CHI TIẾT • SL tồn của từng công ty thuê kho, tính đến ngày đã chọn, cộng trên các kho đang xem'
TIP_THUE = 'Chọn kho trước. Bỏ trống = mọi công ty thuê của các kho'
TIP_HDONG = 'Gõ mã hợp đồng rồi Enter hoặc bấm Tìm kiếm.'

d = SrsDoc(out=OUT, menu=MENU, route='/warehouse/stock-general-product', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Kho': 'menu_phanhe', 'Báo cáo kho': 'menu_nhom', 'Báo cáo tồn kho tổng hợp theo mặt hàng': 'menu_muc',
    'Ẩn tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Hàng hóa': 'o_hanghoa',
    'ĐVT': 'o_dvt', 'In danh sách': 'btn_inds', 'Xuất Excel': 'btn_xuatexcel',
}.items()})

UI_OVER = {}
UI_EXPLICIT = {}


def uc(code, name, group, actor):
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None):
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
    extra = layout.pop('extra', [])
    d.layout(**layout)
    for s, cap in extra:
        d.figure(s, cap, width_in=6.2)
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Báo cáo tồn kho tổng hợp theo mặt hàng thuộc phân hệ Kho, nhóm Báo cáo kho '
    '(chuyển từ hệ thống ERP: Kho › Báo cáo kho), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu báo cáo cho biết tồn của TỪNG mặt hàng, cộng trên MỘT HOẶC NHIỀU kho của một công ty, tính đến hết một ngày, '
    'chia cột theo công ty thuê kho (nhóm cột Chi tiết).',
    'Ghi rõ cách tính từng con số (khối tổng hợp, dòng TỔNG, cột SL tồn, các cột công ty thuê kho) để người nghiệm thu đối soát được với '
    'Báo cáo tồn kho chi tiết theo mặt hàng, Báo cáo tồn kho theo vị trí và Thẻ kho.',
    'Ghi rõ các điểm GIỮ Y HỆT hệ thống ERP (nhóm cột Chi tiết chỉ hiện trên màn với quyền tổng công ty, ĐVT chọn riêng từng hàng và áp '
    'cho In / Excel) và các điểm khác ERP có chủ đích (có In xem trước, Excel tải thẳng, chặn kho ngoài phạm vi quyền).',
])
d.p('Phạm vi chức năng (7 chức năng, đặc tả ở Phần 3):')
d.bullets([
    'Xem báo cáo (khối tổng hợp + bảng phẳng mỗi mặt hàng 1 dòng, phân trang theo mặt hàng); Tìm kiếm và lọc (12 ô lọc gồm ô tích “Xem '
    'toàn bộ kho”, 3 ô bắt buộc); Cài đặt bộ lọc; Chọn hàng hóa (cửa sổ chọn 1 hàng); Xem tồn theo công ty thuê kho và đổi ĐVT; In báo '
    'cáo (2 kiểu, chọn cột, xem trước); Xuất Excel (2 kiểu).',
    'Không thuộc màn này: màn CHỈ ĐỌC — không có Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Duyệt / Không duyệt, Import Excel, Lịch sử '
    'thay đổi, không có Tùy chỉnh cột (bảng cố định 7 cột + nhóm Chi tiết; chọn cột chỉ có ở bản in) và không có số bấm mở cửa sổ chi '
    'tiết. Số liệu sinh ra từ các chứng từ kho ở Phần 5.',
])
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Kế toán kho / thủ kho xem nhanh mỗi mặt hàng còn bao nhiêu trên toàn bộ (hoặc một nhóm) kho của công ty vào một ngày, thuộc công '
    'ty thuê kho nào, để lập kế hoạch mua, điều chuyển, đối chiếu sổ sách.',
    'Đối soát với Báo cáo tồn kho chi tiết theo mặt hàng (chọn 1 kho thì SL tồn khớp), Báo cáo tồn kho theo vị trí (tổng các vị trí của '
    '1 hàng) và Thẻ kho (tồn cuối kỳ).',
    'Bản in / file Excel dùng để ký xác nhận (Trưởng kho, Người lập báo cáo) hoặc gửi đối chiếu.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Bắt buộc chọn Tính đến ngày, Tồn theo công ty và ít nhất 1 Kho; mặc định chọn TOÀN BỘ kho của công ty nên vào màn là có số ngay (BR-01).',
    'SL tồn của 1 công ty thuê kho = tổng mọi thay đổi tồn (nhập +, xuất −) ghi cho công ty đó trên các kho đang chọn tới HẾT ngày Tính '
    'đến ngày; SL tồn mặt hàng = tổng các công ty thuê kho đang lọc; chỉ hiện hàng có SL tồn khác 0 (BR-02, BR-03).',
    'Nhóm cột Chi tiết (mỗi công ty thuê kho 1 cột) và khối Theo công ty thuê kho chỉ hiện trên màn với quyền tổng công ty; bản in / Excel '
    'kiểu Đầy đủ luôn có nhóm Chi tiết (giữ y ERP — BR-04).',
    'Phạm vi kho theo 1 trong 3 quyền xem báo cáo tồn kho; không có quyền nào thì không xem được (BR-05).',
    'Màn không ghi dữ liệu nào; không có lịch sử thay đổi (BR-12).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Tồn kho (SL tồn)', 'Số lượng hàng còn trong các kho đang chọn, tính theo ĐVT cơ sở của hàng rồi quy đổi theo ĐVT đang chọn ở dòng '
                         'mặt hàng.'),
    ('Tính đến ngày', 'Ngày chốt số liệu: cộng mọi thay đổi tồn tới hết 23:59 của ngày này. Mặc định hôm nay.'),
    ('Tồn theo công ty', 'Công ty đang xem; quyết định danh sách kho chọn được và letterhead bản in / Excel.'),
    ('Kho', 'Kho vật lý đang hoạt động, thuộc công ty đang xem và trong phạm vi quyền; chọn được nhiều kho, ô hiện MÃ kho.'),
    ('Xem toàn bộ kho', 'Ô tích cạnh ô Kho: tích = chọn hết kho của công ty, bỏ tích = xóa kho để tự chọn. Tự tích khi ô Kho đang có đủ '
                        'kho của công ty.'),
    ('Công ty thuê kho', 'Công ty có kho kế toán gắn với kho đã chọn; tồn ghi nhận theo từng công ty này. Bỏ trống = mọi công ty thuê '
                         'của các kho.'),
    ('Nhóm cột Chi tiết', 'Các cột số đứng sau SL tồn, mỗi công ty thuê kho đang lọc 1 cột (tiêu đề là mã công ty, rê chuột xem tên).'),
    ('ĐVT cơ sở / hệ số', 'Đơn vị nhỏ nhất của hàng (hệ số 1); ĐVT khác có hệ số quy đổi (vd Thùng 24C-1L = 24 Can 1L).'),
    ('Kiểu Đầy đủ / Ngắn gọn', 'Kiểu in / xuất Excel: Đầy đủ có nhóm Chi tiết (mỗi công ty thuê kho 1 cột); Ngắn gọn chỉ thông tin mặt '
                               'hàng và SL tồn.'),
    ('Trạng thái bản ghi', 'Dòng báo cáo không có trạng thái (không Khóa / Hoạt động); mặt hàng chỉ xuất hiện khi tổng tồn các công ty '
                           'thuê kho đang lọc khác 0.'),
    ('Cấu trúc phân cấp', 'Không phân cấp: bảng phẳng, mỗi mặt hàng 1 dòng (khác Báo cáo tồn kho chi tiết theo mặt hàng dạng cây).'),
], widths=[2.0, 4.0])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn dùng 3 quyền tên y hệ thống ERP, nhóm “Báo cáo kho” (dùng chung với Báo cáo tồn kho chi tiết theo mặt hàng, Báo cáo tồn kho '
    'theo vị trí, Báo cáo tồn theo kho, Tổng hợp xuất nhập tồn). Có 1 trong 3 quyền là vào được màn và dùng MỌI chức năng; quyền cao '
    'nhất quyết định phạm vi kho và việc thấy nhóm cột Chi tiết. Hệ thống kiểm quyền ở máy chủ cho mọi lần lấy dữ liệu, in, xuất; mục '
    'menu không ẩn theo quyền.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('—', '(Không có quyền thao tác riêng)', 'Xem báo cáo, tìm kiếm và lọc, cài đặt bộ lọc, chọn hàng hóa, đổi ĐVT, In, Xuất Excel: '
                                            'ai có 1 trong 3 quyền V1 / V2 / V3 đều dùng được.'),
], widths=[0.8, 1.9, 3.3])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', V1, 'Ô Tồn theo công ty chọn được mọi công ty đang hoạt động; ô Kho gồm mọi kho đang hoạt động của công ty đang chọn; THẤY '
               'nhóm cột Chi tiết và khối Theo công ty thuê kho. Super admin được coi như có V1.'),
    ('V2', V2, 'Ô Tồn theo công ty chỉ có công ty của người dùng; ô Kho gồm các kho thuộc công ty đó; không thấy nhóm cột Chi tiết.'),
    ('V3', V3, 'Ô Tồn theo công ty chỉ có công ty của người dùng; ô Kho chỉ gồm kho người dùng là thủ kho (thuộc công ty đó); không thấy '
               'nhóm cột Chi tiết.'),
], widths=[0.8, 2.3, 2.9])
d.p('Có nhiều quyền: lấy quyền cao nhất theo thứ tự V1 > V2 > V3. Người không có V1 gửi công ty khác (gọi thẳng chức năng) vẫn bị khóa '
    'về công ty mình; kho ngoài phạm vi hoặc không thuộc công ty đang xem bị bỏ, không còn kho nào thì báo ' + M_KHO + '. V2 / V3 vẫn in / '
    'xuất được kiểu Đầy đủ có nhóm Chi tiết (giữ y ERP).')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'V1', 'V2', 'V3', 'Không có quyền nào'], [
    ('FR-01 Xem báo cáo', '✅ mọi công ty', '✅ công ty mình', '✅ kho mình là thủ kho', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '❌'),
    ('FR-04 Chọn hàng hóa', '✅', '✅', '✅', '❌'),
    ('FR-05 Xem tồn theo công ty thuê kho, đổi ĐVT', '✅ có nhóm Chi tiết', '✅ chỉ đổi ĐVT', '✅ chỉ đổi ĐVT', '❌'),
    ('FR-06 In báo cáo', '✅', '✅', '✅', '❌'),
    ('FR-07 Xuất Excel', '✅', '✅', '✅', '❌'),
], widths=[2.6, 0.9, 0.9, 0.9, 0.7])
d.p('Màn không có Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Import Excel, Lịch sử thay đổi, Duyệt nên ma trận không có các dòng đó.')
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có quyền nào trong 3 quyền: mục menu vẫn hiện; mở màn thì hệ thống báo ' + NOPERM + ', ô Tồn theo công ty và Kho rỗng, '
    'bảng hiện “Chọn công ty để xem báo cáo.”; In / Xuất Excel không thực hiện được (báo chữ đỏ dưới ô thiếu).',
    'Mở thẳng đường dẫn màn khi thiếu quyền: như trên, không lộ số liệu.',
    'Có quyền V3 nhưng không là thủ kho kho nào: ô Kho rỗng, ô Xem toàn bộ kho bị khóa, bảng hiện ' + M_CHONKHO,
    'Bị gỡ quyền khi đang mở màn: lần lọc / in / xuất kế tiếp báo ' + NOPERM + ', bảng giữ số liệu cũ đang hiện.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút In danh sách, Xuất Excel', 'Luôn hiện ở đầu khối bộ lọc', 'Chưa có báo cáo → bấm thì báo đỏ dưới ô thiếu, không mở cửa sổ'),
    ('Nút Cài đặt bộ lọc, Ẩn / Tìm kiếm nâng cao', 'Luôn hiện', 'Khối nâng cao mở sẵn khi vào màn'),
    ('Ô Tồn theo công ty', 'Luôn hiện, bắt buộc', 'V2 / V3: chỉ 1 lựa chọn (công ty mình)'),
    ('Ô tích Xem toàn bộ kho', 'Luôn hiện', 'Khóa khi công ty không có kho nào trong phạm vi quyền'),
    ('Nhóm cột Chi tiết, khối Theo công ty thuê kho, ô Công ty thuê kho có tồn', 'Chỉ quyền V1 (hoặc Super admin)',
     'Có ít nhất 1 công ty thuê kho đang lọc'),
    ('Ô chọn ĐVT trên dòng mặt hàng', 'Hàng đã khai ĐVT', 'Hiện cả khi hàng chỉ có 1 ĐVT; hàng chưa khai ĐVT để trống'),
], widths=[2.0, 2.0, 2.0])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A, [0, 1, 2])],
    [('FR-01', 'Xem báo cáo tồn kho tổng hợp theo mặt hàng', 'view'),
     ('FR-06', 'In báo cáo', 'io'),
     ('FR-07', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Chọn hàng hóa', 'view', 'extend', [0], None),
     ('FR-05', 'Xem tồn theo công ty thuê kho, đổi ĐVT', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Báo cáo tồn kho tổng hợp theo mặt hàng')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
k = fr(1, 'Xem báo cáo tồn kho tổng hợp theo mặt hàng',
       rule=('- Màn Danh sách, Phân trang và Báo cáo.', 'list'),
       intro=dict(
           ten='Truy cập màn Báo cáo tồn kho tổng hợp theo mặt hàng và xem báo cáo',
           mota='Mở màn và hiển thị tồn của từng mặt hàng cộng trên các kho đã chọn, tính đến hết ngày đã chọn: dòng tóm tắt (ngày, mã '
                'các kho), khối tổng hợp (Mặt hàng còn tồn, Kho đang xem, Công ty thuê kho có tồn, số mặt hàng theo từng công ty thuê '
                'kho), bảng phẳng mỗi mặt hàng 1 dòng kèm dòng TỔNG và nhóm cột Chi tiết theo công ty thuê kho, phân trang theo mặt '
                'hàng. Màn chỉ đọc; phạm vi kho theo quyền.',
           tacnhan=TN, dieukien=DK,
           chinh='1. Người dùng vào menu theo đường dẫn ở mục Layout.\n'
                 '2. Hệ thống kiểm quyền, nạp danh mục bộ lọc theo phạm vi quyền (công ty, kho, công ty thuê của từng kho) và danh mục '
                 'hàng hóa (nhóm, tính chất, loại, thương hiệu, hãng sản xuất).\n'
                 '3. Có bộ lọc ghi tạm dưới 10 phút → khôi phục (kể cả hàng hóa đã chọn; kho không còn trong phạm vi bị bỏ); không có → '
                 'Tính đến ngày = hôm nay, Tồn theo công ty = công ty của người dùng, Kho = TOÀN BỘ kho của công ty (tích sẵn Xem toàn '
                 'bộ kho), Công ty thuê kho = mọi công ty thuê của các kho.\n'
                 '4. Hệ thống tính tồn mọi mặt hàng trên các kho tới hết ngày, theo từng công ty thuê kho, giữ mặt hàng có tổng khác 0, '
                 'sắp theo tên hàng; dựng khối tổng hợp trên TOÀN tập; trả 20 mặt hàng của trang 1.\n'
                 '5. Hệ thống hiển thị dòng tóm tắt, khối tổng hợp, bảng, dòng “Hiển thị 1–20 / N mặt hàng”.',
           phu='• Thiếu ô bắt buộc (bỏ hết kho) → không tính, bảng hiện ' + M_CHONKHO + ' (tương tự “Chọn công ty để xem báo cáo.”, '
               '“Chọn ngày để xem báo cáo.”).\n'
               '• Không có mặt hàng nào còn tồn → khối tổng hợp hiện 0, bảng hiện ' + M_EMPTY + ', ẩn phân trang.\n'
               '• Không có quyền → báo ' + NOPERM + ', danh mục bộ lọc rỗng, bảng hiện “Chọn công ty để xem báo cáo.”.\n'
               '• Đổi bộ lọc khi đang có báo cáo → giữ số cũ làm mờ cho tới khi có số mới; lỗi tải thì giữ số cũ, báo lỗi.\n'
               '• Bấm Thu gọn → ẩn các ô của khối tổng hợp, còn dòng tóm tắt; bấm Mở rộng để hiện lại.\n'
               '• Bấm số trang / đổi Số dòng/trang → nạp lại đúng trang; dòng TỔNG và khối tổng hợp không đổi.\n'
               '• Phiên đăng nhập hết hạn → chuyển về màn đăng nhập.',
           dacbiet='Bảng cố định 7 cột: STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn + nhóm Chi tiết (V1) — không có cột '
                   'ẩn, không có Tùy chỉnh cột, không sắp xếp theo cột (luôn theo tên hàng). Phân trang theo MẶT HÀNG (mặc định 20; 10 / '
                   '20 / 50 / 100). Không cộng SL ở dòng TỔNG vì mỗi hàng một ĐVT. Kho lớn (vài nghìn mặt hàng) có thể mất vài giây.'),
       layout=dict(menu=MENU, shot=shot('01_list'),
                   shot_caption='Màn Báo cáo tồn kho tổng hợp theo mặt hàng — công ty CN Hải Phòng, 4 kho, tính đến 07/11/2026',
                   note='Lối vào duy nhất (phân hệ Kho, nhóm Báo cáo kho). Hiển thị: mặt hàng còn tồn trên các kho trong phạm vi quyền.',
                   extra=[(shot('00_menu'), 'Mục Báo cáo tồn kho tổng hợp theo mặt hàng trong nhóm Báo cáo kho của phân hệ Kho'),
                          (shot('01a_default'), 'Mở màn lần đầu: công ty mặc định, toàn bộ kho của công ty, báo cáo tự tải'),
                          (shot('01b_empty'), 'Bỏ tích Xem toàn bộ kho: ô Kho trống, bảng chờ chọn kho')]),
       ui_kw=dict(required=False),
       ui=[
           ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '“Báo cáo tồn kho tổng hợp theo mặt hàng”',
            ['- Ở thanh trên cùng, cũng là tiêu đề tab trình duyệt', '- Icon ⓘ: “' + TIP_TITLE + '”']),
           ('Dòng tóm tắt', 'Label', 'Read-only', '–', 'Theo dữ liệu',
            ['- “Tồn kho tính đến ngày dd/mm/yyyy · Kho: <mã các kho, cách bằng dấu phẩy>”', '- Rê chuột vào phần Kho: mã - tên từng kho',
             '- Icon ⓘ: “' + TIP_GOAL + '”', '- Chỉ hiện khi đã có báo cáo']),
           ('Nút Thu gọn', 'Button', 'Enable', '–', 'Hiển thị',
            ['- Góc phải dòng tóm tắt', '- Bấm → ẩn các ô khối tổng hợp, chữ đổi thành “Mở rộng”', '- Không gọi lại dữ liệu']),
           ('Khối Mặt hàng', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Ô Mặt hàng còn tồn: “N mặt hàng” — luôn hiện', '- Ô Kho đang xem: “N kho”',
             '- Ô Công ty thuê kho có tồn: “N công ty” — chỉ V1 và khi > 0', '- Icon ⓘ: “' + TIP_MH + '”',
             '- Số KHÔNG bấm được (không mở cửa sổ)']),
           ('Khối Theo công ty thuê kho', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Chỉ V1: mỗi công ty thuê kho có tồn 1 ô: mã công ty + “N mặt hàng”', '- Ẩn cả khối khi không công ty nào có tồn',
             '- Icon ⓘ: “' + TIP_CT + '”', '- Số không bấm được']),
           ('Bảng báo cáo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- 7 cột + nhóm Chi tiết, mỗi cột mô tả ở 1 dòng bên dưới', '- Tiêu đề 2 tầng (khi có nhóm Chi tiết) dính khi cuộn',
             '- Cuộn ngang khi bảng rộng hơn màn hình (mỗi công ty thuê kho thêm 90px)']),
           ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Dòng TỔNG: “TỔNG”', '- Mặt hàng: 1, 2… liên tục giữa các trang (trang 2 cỡ 20 bắt đầu từ 21)']),
           ('Cột Tên hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Tên hàng, dài cắt “…”, rê chuột xem đủ']),
           ('Cột Model', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Model của hàng', '- Trống khi hàng chưa khai model']),
           ('Cột Mã hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Dài cắt “…”, rê chuột xem đủ']),
           ('Cột Thương hiệu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Trống khi chưa khai']),
           ('Cột ĐVT', 'Dropdown', 'Enable', 'Danh sách ĐVT của hàng', 'ĐVT cơ sở',
            ['- Ô chọn trên MỌI dòng có ĐVT (kể cả hàng 1 ĐVT), dạng “<tên> (x<hệ số>)”; hàng chưa khai ĐVT để trống',
             '- Mặc định: ĐVT cơ sở', '- Icon ⓘ: “' + TIP_DVT + '”', '- Đổi ĐVT → mục 2.5']),
           ('Cột SL tồn', 'Table/Grid', 'Read-only', 'Số, tối đa 2 số lẻ', 'Theo dữ liệu',
            ['- Căn phải, phân cách hàng nghìn bằng dấu phẩy, quy đổi theo ĐVT đang chọn, làm tròn 2 số lẻ',
             '- = 0 sau quy đổi hiện “0”; có thể âm khi xuất vượt nhập', '- Icon ⓘ: “' + TIP_SL + '”']),
           ('Nhóm cột Chi tiết', 'Table/Grid', 'Read-only', 'Số, tối đa 2 số lẻ', 'Theo dữ liệu',
            ['- Chỉ V1; mỗi công ty thuê kho đang lọc 1 cột, tiêu đề mã công ty (rê chuột xem tên), sắp theo mã',
             '- Số 0 để trống', '- Icon ⓘ: “' + TIP_CHITIET + '”']),
           ('Dòng TỔNG', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Nền cam, đầu bảng: “MẶT HÀNG CÒN TỒN · N mặt hàng” (toàn tập đã lọc, không theo trang)',
             '- Không cộng số lượng', '- Icon ⓘ: “' + TIP_TONG + '”']),
           ('Dòng “Hiển thị a–b / N mặt hàng”', 'Label', 'Read-only', '–', 'Theo dữ liệu',
            ['- a–b: thứ tự mặt hàng của trang đang xem', '- N: tổng mặt hàng còn tồn khớp bộ lọc']),
           ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', '20',
            ['- Mặc định: 20', '- Lựa chọn: 10, 20, 50, 100 (mặt hàng)', '- Đổi giá trị → về trang 1, nạp lại']),
           ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
            ['- Nút «, ‹, số trang, ›, »; ở trang đầu nút « ‹ mờ, trang cuối › » mờ', '- Ẩn khi không có mặt hàng',
             '- Giữ bộ lọc và ĐVT đã chọn khi đổi trang']),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
            ['- Chưa chọn kho: ' + M_CHONKHO, '- Không có hàng: ' + M_EMPTY, '- Đang tải lần đầu: “Đang tải dữ liệu...”']),
           ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
            ['- Thiếu quyền: ' + NOPERM, '- Lỗi khác: câu máy chủ trả hoặc ' + M_LOADERR,
             '- Hết phiên đăng nhập: chuyển về màn đăng nhập']),
       ],
       ev=[('Mở màn hình', 'System',
            'Before:\n– Kiểm tra 1 trong 3 quyền xem báo cáo tồn kho; không có → hiển thị ' + NOPERM + ' và dừng xử lý.\n'
            '– Có bộ lọc ghi tạm dưới 10 phút → khôi phục; công ty / kho đã ghi không còn trong phạm vi → bỏ.\n'
            'During:\n– Nạp danh mục công ty, kho, công ty thuê kho theo phạm vi quyền; ngày mặc định hôm nay; chưa có kho → chọn hết kho '
            'của công ty và mọi công ty thuê của các kho.\n'
            'After:\n– Hiển thị khối tổng hợp, bảng trang 1 (20 mặt hàng), dòng “Hiển thị 1–20 / N”.'),
           ('Bấm Thu gọn hoặc Mở rộng', 'Click',
            'Before:\n– Chỉ có khi đã có báo cáo.\nDuring:\n– Ẩn / hiện các ô khối tổng hợp, không gọi lại dữ liệu.\n'
            'After:\n– Chữ nút đổi “Thu gọn” ↔ “Mở rộng”.'),
           ('Bấm số trang hoặc nút tiến lùi', 'Click',
            'Before:\n– Giữ nguyên bộ lọc, ĐVT đã chọn.\n'
            'During:\n– Lấy lại báo cáo cho trang mới; trang vượt quá số trang → về trang cuối.\n'
            'After:\n– Hiển thị trang mới, STT tiếp tục, dòng “Hiển thị a–b / N” cập nhật; dòng TỔNG, khối tổng hợp không đổi.'),
           ('Đổi Số dòng/trang', 'Change',
            'Before:\n– Chọn 10, 20, 50 hoặc 100.\nDuring:\n– Ghi nhận số dòng mới (tối đa 100 mặt hàng / trang).\n'
            'After:\n– Về trang 1 và nạp lại.'),
           ('Rê chuột vào tiêu đề cột công ty thuê kho', 'Hover',
            'Before:\n– Có nhóm Chi tiết (V1).\nDuring:\n– Lấy tên công ty.\nAfter:\n– Hiện tên đầy đủ của công ty thuê kho.'),
           ('Phiên đăng nhập hết hạn khi thao tác', 'System',
            'Before:\n– Áp cho mọi lần nạp báo cáo, in, xuất.\nDuring:\n– Máy chủ từ chối yêu cầu.\n'
            'After:\n– Chuyển về màn đăng nhập, không hiện dữ liệu.')])

d.p('2.1.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('Bảng dưới mô tả cách hệ thống tính từng chỉ tiêu, từng cột số liệu và nội dung icon ⓘ (nguyên văn trên giao diện). “Tập dữ liệu” '
    'là các mặt hàng có thay đổi tồn tại CÁC KHO đã chọn, ghi nhận cho các công ty thuê kho đang lọc (bỏ trống = mọi công ty thuê của các '
    'kho), tới hết ngày Tính đến ngày, sau khi áp các ô lọc hàng hóa và hợp đồng, trong phạm vi quyền. Nguồn thay đổi tồn: mọi chứng từ '
    'kho đã ghi tồn (nhập kho, xuất kho, nhập lại, xuất điều chỉnh, điều chuyển kho, nhập / xuất điều chỉnh kiểm kê, tồn kho đầu kỳ — '
    'Phần 5).')
d.data_table([
    ('Dòng tóm tắt', 'Ngày = Tính đến ngày (dd/mm/yyyy); Kho = mã các kho đã chọn (rê chuột: mã - tên); ⓘ ghi giờ máy chủ tính số liệu.',
     TIP_GOAL),
    ('Ô Mặt hàng còn tồn', 'Đếm mặt hàng KHÁC NHAU của tập dữ liệu có tổng tồn các công ty thuê kho đang lọc ≠ 0 (kể cả âm). Tính trên '
                           'toàn tập, không theo trang. = N ở dòng “Hiển thị a–b / N” = số ở dòng TỔNG.', TIP_MH),
    ('Ô Kho đang xem', 'Số kho đang chọn ở bộ lọc sau khi bỏ kho ngoài phạm vi quyền / khác công ty.', '(dùng chung ⓘ của khối)'),
    ('Ô Công ty thuê kho có tồn', 'Chỉ V1. Đếm công ty thuê kho đang lọc có ít nhất 1 mặt hàng tồn > 0. Ẩn khi = 0.',
     '(dùng chung ⓘ của khối)'),
    ('Ô của từng công ty (khối Theo công ty thuê kho)', 'Chỉ V1. Số mặt hàng có tồn của RIÊNG công ty đó > 0. Một mặt hàng có tồn ở 2 công '
                                                         'ty được đếm ở cả 2 ô, nên tổng các ô có thể lớn hơn Ô Mặt hàng còn tồn.', TIP_CT),
    ('Dòng TỔNG', 'Số mặt hàng còn tồn (= Ô Mặt hàng còn tồn). Không cộng SL vì mỗi hàng một ĐVT.', TIP_TONG),
    ('Cột công ty thuê kho (nhóm Chi tiết)', 'Tổng mọi thay đổi tồn (nhập +, xuất −) ghi cho công ty đó trên MỌI kho đang chọn, từ đầu tới '
                                             'hết ngày Tính đến ngày. Có cột cho mọi công ty thuê kho đang lọc, kể cả cột toàn trống. '
                                             'Chọn 1 kho = SL tồn dòng công ty ở Báo cáo tồn kho chi tiết theo mặt hàng = Tồn cuối kỳ '
                                             'của Thẻ kho cùng hàng, kho, công ty, ngày.', TIP_CHITIET),
    ('Cột SL tồn', 'Tổng các cột công ty thuê kho đang lọc (kể cả khi người dùng V2 / V3 không thấy nhóm Chi tiết). Nhiều kho = tổng SL '
                   'tồn của từng kho (vd 4 kho CN Hải Phòng: 47 = HP 20 + CB 27). Chọn 1 kho = SL tồn của hàng ở Báo cáo tồn kho chi '
                   'tiết theo mặt hàng = tổng các vị trí ở Báo cáo tồn kho theo vị trí.', TIP_SL),
    ('Quy đổi ĐVT', 'Mọi số của hàng (SL tồn, các cột công ty) = số theo ĐVT cơ sở ÷ hệ số ĐVT đang chọn, làm tròn 2 số lẻ (vd 24 Can 1L → '
                    'Thùng 24C-1L x24 = 1). In / Excel dùng đúng ĐVT đã chọn từng hàng.', TIP_DVT),
    ('Thứ tự dòng', 'Mặt hàng theo tên hàng (A→Z theo cách so chữ của cơ sở dữ liệu), trùng tên theo thứ tự tạo hàng; cột công ty theo '
                    'mã công ty.', '—'),
    ('Ràng buộc khớp số', 'Tồn đầu kỳ + Nhập − Xuất = Tồn cuối kỳ của Thẻ kho = cột công ty (cùng hàng / kho / công ty / ngày); SL tồn = '
                          'tổng các cột công ty; Ô Mặt hàng còn tồn = dòng TỔNG = N.', '—'),
])
k += 1
d.p('2.1.%d Danh sách popup mở từ số liệu' % k)
d.popup_table([
    ('Số ở khối tổng hợp, dòng TỔNG, cột SL tồn, các cột công ty', 'Không có popup — số không bấm được',
     'Báo cáo tổng hợp; xem chi tiết lô / vị trí dùng Báo cáo tồn kho chi tiết theo mặt hàng, từng chứng từ dùng Thẻ kho',
     'Con số đọc trực tiếp trên bảng (mục 2.1.6)'),
    ('Ô chọn ĐVT trên dòng mặt hàng', 'Không phải popup — ô chọn ngay trong bảng (mục 2.5)',
     'Xem số của hàng theo đơn vị lớn (thùng, hộp…)', 'Danh sách ĐVT của chính mặt hàng'),
    ('Ô Hàng hóa trong bộ lọc', 'Chọn hàng hóa (mục 2.4)', 'Thu hẹp báo cáo về đúng 1 mặt hàng',
     'Danh sách hàng hóa theo công ty đang xem; chọn 1 hàng thì báo cáo còn tối đa 1 mặt hàng'),
])

# ------------------------------------------------------------ 2.2
k = fr(2, 'Tìm kiếm và lọc',
       rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
       intro=dict(ten='Tìm kiếm và lọc báo cáo tồn kho tổng hợp theo mặt hàng',
                  mota='Chọn ngày chốt số, công ty, một hoặc nhiều kho (3 ô bắt buộc; ô tích Xem toàn bộ kho chọn nhanh mọi kho) và thu '
                       'hẹp tập mặt hàng theo công ty thuê kho, nhóm, tính chất, loại, thương hiệu, hãng sản xuất, 1 hàng hóa cụ thể hoặc '
                       'mã hợp đồng. Màn không có ô tìm nhanh; các ô chọn áp ngay khi đổi, ô Hợp đồng áp khi Enter / Tìm kiếm.',
                  tacnhan=TN, dieukien=DK,
                  chinh='1. Người dùng chọn Tính đến ngày, Tồn theo công ty (hệ thống chọn sẵn mọi kho của công ty).\n'
                        '2. Người dùng bỏ / thêm kho ở ô Kho, hoặc bỏ tích Xem toàn bộ kho để tự chọn.\n'
                        '3. Hệ thống tự tích mọi công ty thuê của các kho đang chọn vào ô Công ty thuê kho.\n'
                        '4. Người dùng chọn thêm các ô lọc hàng hóa (chọn nhiều) hoặc chọn 1 hàng qua cửa sổ Chọn hàng hóa (mục 2.4).\n'
                        '5. Mỗi lần đổi ô chọn, hệ thống gom các thay đổi trong 0,3 giây thành 1 lần tính, về trang 1, nạp lại báo cáo, '
                        'ghi tạm bộ lọc trên trình duyệt (10 phút).\n'
                        '6. Người dùng gõ mã hợp đồng rồi Enter hoặc bấm Tìm kiếm → hệ thống nạp lại theo hợp đồng.',
                  phu='• Bỏ tích Xem toàn bộ kho → xóa mọi kho (và công ty thuê), bảng hiện ' + M_CHONKHO + '; tích lại → chọn hết kho.\n'
                      '• Bấm Tìm kiếm / In danh sách / Xuất Excel khi thiếu ô bắt buộc → chữ đỏ dưới ô thiếu (' + M_NGAY + ', ' + M_KHO +
                      '), khối lọc tự mở, không nạp.\n'
                      '• Đổi Tồn theo công ty → chọn lại HẾT kho của công ty mới và mọi công ty thuê của chúng.\n'
                      '• Đổi Kho → tích lại toàn bộ công ty thuê của các kho đang chọn; bỏ 1 kho bằng dấu × → ô Xem toàn bộ kho tự bỏ tích.\n'
                      '• Bỏ trống Công ty thuê kho → tính mọi công ty thuê của các kho.\n'
                      '• Bấm Xóa lọc → về công ty mặc định + hôm nay + toàn bộ kho, bỏ mọi ô khác (kể cả hàng hóa), xóa bộ lọc ghi tạm, '
                      'nạp lại.\n'
                      '• Không có kết quả → ' + M_EMPTY + '\n'
                      '• Rời sang màn khác → xóa bộ lọc ghi tạm; F5 / tab mới trong 10 phút → khôi phục.',
                  dacbiet='Kiểu khớp: Hợp đồng khớp MỘT PHẦN mã hợp đồng (chứa chuỗi gõ), không giới hạn số ký tự; ký tự % và _ được hiểu '
                          'là ký tự đại diện (gõ “%” ra mọi hàng có chứng từ gắn hợp đồng). Các ô chọn khớp CHÍNH XÁC; Loại hàng hóa khớp '
                          'khi hàng thuộc ít nhất 1 loại đã chọn. Kết hợp nhiều ô = thỏa đồng thời (VÀ); trong 1 ô chọn nhiều = HOẶC.'),
       layout=dict(menu=MENU + ' => Ẩn tìm kiếm nâng cao', shot=shot('02_filter'),
                   shot_caption='Khối Bộ lọc báo cáo tồn kho (mở sẵn khi vào màn)',
                   extra=[(shot('01c_required'), 'Bấm Tìm kiếm khi ô Kho trống: chữ đỏ “Vui lòng chọn kho”'),
                          (shot('02b_kho_opts'), 'Ô Kho liệt kê mã kho của công ty đang chọn trong phạm vi quyền')]),
       ui=[('Tiêu đề khối', 'Label', 'Hiển thị', '–', '–', '“Bộ lọc báo cáo tồn kho”', ['- Kèm biểu tượng phễu', '- Icon ⓘ: “' + TIP_PURPOSE + '”']),
           ('Tính đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Hôm nay',
            ['- Mặc định: hôm nay', '- Thiếu → ' + M_NGAY, '- Đổi → nạp lại']),
           ('Tồn theo công ty', 'Dropdown', 'Enable', 'Danh sách theo quyền', 'Có', 'Công ty của người dùng',
            ['- Mặc định: công ty của người dùng', '- V1: mọi công ty đang hoạt động; V2 / V3: chỉ công ty mình', '- Không có nút × bỏ chọn',
             '- Đổi → chọn hết kho của công ty mới']),
           ('Xem toàn bộ kho', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Tích',
            ['- Tích: chọn hết kho của công ty', '- Bỏ tích: xóa mọi kho để tự chọn', '- Tự tích / bỏ tích theo ô Kho',
             '- Khóa khi công ty không có kho trong phạm vi']),
           ('Kho', 'Dropdown', 'Enable', 'Danh sách theo quyền', 'Có', 'Toàn bộ kho',
            ['- Chọn nhiều, hiện MÃ kho (vd CB, HP, KĐN-ALM, NM)', '- Lựa chọn: kho đang hoạt động của công ty đang chọn trong phạm vi quyền',
             '- Thiếu → ' + M_KHO, '- Đổi → tích sẵn mọi công ty thuê của các kho']),
           ('Công ty thuê kho', 'Dropdown', 'Enable', 'Công ty thuê của các kho', 'Không', 'Mọi công ty thuê của các kho',
            ['- Chọn nhiều, hiện mã công ty, mỗi công ty 1 lần', '- Icon ⓘ: “' + TIP_THUE + '”', '- Bỏ trống = mọi công ty thuê']),
           ('Nhóm hàng hóa', 'Dropdown', 'Enable', 'Danh mục nhóm', 'Không', 'Trống', ['- Chọn nhiều', '- Mặc định: trống (tất cả)']),
           ('Tính chất hàng hóa', 'Dropdown', 'Enable', 'Danh mục tính chất', 'Không', 'Trống', ['- Chọn nhiều', '- Mặc định: trống']),
           ('Loại hàng hóa', 'Dropdown', 'Enable', 'Danh mục loại', 'Không', 'Trống', ['- Chọn nhiều', '- Hàng thuộc ít nhất 1 loại đã chọn']),
           ('Thương hiệu', 'Dropdown', 'Enable', 'Danh mục thương hiệu', 'Không', 'Trống', ['- Chọn nhiều', '- Mặc định: trống']),
           ('Hãng sản xuất', 'Dropdown', 'Enable', 'Danh mục hãng', 'Không', 'Trống', ['- Chọn nhiều', '- Mặc định: trống']),
           ('Hàng hóa', 'Textbox', 'Read-only', '1 hàng', 'Không', 'Trống',
            ['- Bấm ô → mở cửa sổ Chọn hàng hóa (mục 2.4)', '- Đã chọn: “<mã> - <tên>” (dài cắt “…”), dấu × riêng để bỏ chọn',
             '- Chỉ giữ 1 hàng']),
           ('Hợp đồng', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
            ['- Icon ⓘ: “' + TIP_HDONG + '”', '- Khớp một phần mã hợp đồng', '- Chỉ áp khi Enter hoặc bấm Tìm kiếm']),
           ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
            ['- Kiểm 3 ô bắt buộc; thiếu → chữ đỏ dưới ô, mở khối lọc', '- Đủ → về trang 1, nạp lại (kèm ô Hợp đồng)']),
           ('Nút Xóa lọc', 'Button', 'Enable', '–', '–', 'Hiển thị',
            ['- Về công ty mặc định + hôm nay + toàn bộ kho, bỏ mọi ô khác', '- Xóa bộ lọc ghi tạm, tắt chữ đỏ, nạp lại']),
           ('Nút Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
            ['- Thu gọn / mở khối ô lọc', '- Khi thu gọn nhãn là “Tìm kiếm nâng cao”', '- Mặc định mở']),
           ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
           ('Chữ lỗi dưới ô bắt buộc', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
            ['- ' + M_NGAY, '- ' + M_KHO, '- ' + M_CTY, '- Chỉ hiện sau lần bấm Tìm kiếm / In / Xuất đầu tiên; chọn lại là tự tắt']),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + M_EMPTY, '- ' + M_CHONKHO])],
       ev=[('Đổi một ô chọn', 'Change',
            'Before:\n– Áp cho Tính đến ngày, công ty, kho, công ty thuê, 5 ô danh mục, Hàng hóa.\n'
            '– Đổi công ty → chọn hết kho công ty mới; đổi kho → tích mọi công ty thuê của các kho.\n'
            'During:\n– Ghi tạm bộ lọc; gom các thay đổi trong 0,3 giây; thiếu ô bắt buộc → không gọi máy chủ, bảng chờ chọn.\n'
            '– Máy chủ kiểm ngày đúng định dạng, công ty trong danh mục được xem, bỏ kho ngoài phạm vi / khác công ty; không còn kho → '
            'báo lỗi tại ô.\n' + ERR + '\n'
            'After:\n– Về trang 1, hiển thị báo cáo mới; lỗi thì giữ báo cáo cũ.'),
           ('Tích / bỏ tích Xem toàn bộ kho', 'Change',
            'Before:\n– Công ty có kho trong phạm vi.\nDuring:\n– Tích → chọn hết kho; bỏ tích → xóa kho và công ty thuê.\n'
            'After:\n– Tích: nạp lại báo cáo; bỏ tích: bảng hiện ' + M_CHONKHO + ', không gọi máy chủ.'),
           ('Gõ ô Hợp đồng rồi Enter hoặc bấm Tìm kiếm', 'Click',
            'Before:\n– Gõ chữ chưa nạp lại; đủ 3 ô bắt buộc mới tính.\n'
            'During:\n– Chỉ cộng thay đổi tồn từ lô nhập / lô xuất thuộc phiếu gắn hợp đồng có mã chứa chuỗi gõ.\n' + ERR + '\n'
            'After:\n– Về trang 1, nạp lại, ghi tạm bộ lọc.'),
           ('Bấm Tìm kiếm khi thiếu ô bắt buộc', 'Click',
            'Before:\n– Bật chế độ hiện lỗi.\nDuring:\n– Ô thiếu viền đỏ, chữ ' + M_NGAY + ' / ' + M_KHO + '; mở khối lọc.\n'
            'After:\n– Không nạp, không ghi tạm.'),
           ('Bấm Xóa lọc', 'Click',
            'Before:\n– Không hỏi xác nhận.\n'
            'During:\n– Đặt lại: công ty mặc định, hôm nay, toàn bộ kho, mọi công ty thuê; các ô khác trống; xóa bộ lọc ghi tạm; tắt chữ đỏ.\n'
            'After:\n– Nạp lại báo cáo trang 1.'),
           ('Bấm Ẩn / Tìm kiếm nâng cao', 'Click',
            'Before:\n– Khối đang mở / thu gọn.\nDuring:\n– Đổi trạng thái khối.\nAfter:\n– Giá trị đã chọn vẫn áp dụng; trạng thái ghi tạm cùng bộ lọc.'),
           ('Rời màn hoặc tải lại trang', 'System',
            'Before:\n– Bộ lọc ghi tạm 10 phút trên trình duyệt.\n'
            'During:\n– Chuyển sang màn khác → xóa bộ lọc ghi tạm; F5 / tab mới trong 10 phút → khôi phục.\n'
            'After:\n– Vào lại bằng menu sau khi rời màn → bộ lọc mặc định.')])
d.p('2.2.%d Cách lấy dữ liệu của ô lọc' % k)
d.p('Bảng dưới giải thích cách hệ thống áp từng ô lọc lên tập dữ liệu (mục 2.1.6).')
d.data_table([
    ('Tính đến ngày', 'Lấy thay đổi tồn ghi nhận trước 00:00 của ngày hôm sau (tức tới hết ngày đã chọn). Ngày quá khứ = tồn tại thời '
                      'điểm đó (vd 31/12/2025 = Tồn đầu kỳ năm 2026 của Thẻ kho).', '—'),
    ('Tồn theo công ty', 'Quyết định danh sách kho chọn được và letterhead; không lọc theo công ty ghi nhận tồn.', '—'),
    ('Kho', 'Một hoặc nhiều kho; chỉ giữ kho thuộc phạm vi quyền và thuộc công ty đang chọn (kho lạ bị bỏ, không còn kho nào → '
            + M_KHO + ').', '—'),
    ('Công ty thuê kho', 'Chỉ cộng thay đổi tồn ghi cho các công ty đã tích (trong số công ty thuê của các kho); bỏ trống = mọi công ty '
                         'thuê của các kho; các kho không có công ty thuê nào → rỗng.', TIP_THUE),
    ('Nhóm / Tính chất / Thương hiệu / Hãng sản xuất', 'Hàng có thuộc tính tương ứng bằng 1 trong các giá trị đã chọn.', '—'),
    ('Loại hàng hóa', 'Hàng có danh sách loại chứa ít nhất 1 loại đã chọn.', '—'),
    ('Hàng hóa', 'Đúng 1 mặt hàng đã chọn (gồm cả hàng đã ngừng kinh doanh).', '—'),
    ('Hợp đồng', 'Chỉ cộng thay đổi tồn của lô nhập / lô xuất thuộc phiếu nhập / phiếu xuất gắn hợp đồng bán có mã chứa chuỗi gõ (bỏ '
                 'khoảng trắng đầu / cuối) — SL tồn khi lọc hợp đồng là phần tồn đến từ chứng từ của hợp đồng đó.', TIP_HDONG),
])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị',
              mota='Cho phép mỗi người dùng tự chọn các ô lọc muốn thấy ở khối Bộ lọc báo cáo tồn kho và sắp xếp lại thứ tự. Cấu hình '
                   'lưu theo người dùng cho riêng màn này (12 ô: Tính đến ngày, Tồn theo công ty, Xem toàn bộ kho, Kho, Công ty thuê kho, '
                   'Nhóm hàng hóa, Tính chất hàng hóa, Loại hàng hóa, Thương hiệu, Hãng sản xuất, Hàng hóa, Hợp đồng).',
              tacnhan=TN, dieukien=DK,
              chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
                    '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 12 ô kèm ô tích, theo cấu hình đang lưu.\n'
                    '3. Người dùng tích / bỏ tích và kéo thả để đổi thứ tự.\n'
                    '4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình cho người dùng, hiển thị “Cập nhật thành công” và áp ngay lên khối lọc.',
              phu='• Bấm Khôi phục mặc định → tích lại đủ 12 ô theo thứ tự gốc; phải bấm Lưu mới có hiệu lực.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không lưu thay đổi.\n'
                  '• Lưu thất bại → hiển thị thông báo lỗi.\n'
                  '• Lưu ý: ẩn 3 ô bắt buộc (Tính đến ngày, Tồn theo công ty, Kho) vẫn giữ giá trị đang có; nên giữ hiện 3 ô này.',
              dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('07_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Cài đặt bộ lọc”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách ô lọc', 'Table/Grid', 'Enable', '12 ô', 'Không', 'Theo cấu hình đã lưu',
        ['- Tính đến ngày, Tồn theo công ty, Xem toàn bộ kho, Kho, Công ty thuê kho, Nhóm hàng hóa, Tính chất hàng hóa, Loại hàng hóa, '
         'Thương hiệu, Hãng sản xuất, Hàng hóa, Hợp đồng', '- Mỗi mục đánh số thứ tự']),
       ('Ô tích của ô lọc', 'Checkbox', 'Enable', '–', 'Không', 'Theo cấu hình đã lưu', ['- Tích: ô hiện ở khối lọc', '- Bỏ tích: ẩn']),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo để đổi thứ tự ô lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình cho người dùng hiện tại, đóng cửa sổ, áp ngay.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích lại đủ 12 ô, thứ tự gốc; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ; thay đổi chưa lưu bị bỏ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Đóng.'),
       ('Khối lọc sau khi lưu', 'Label', 'Hiển thị', '–', '–', 'Theo cấu hình', '- Chỉ còn các ô được tích, đúng thứ tự đã kéo'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- Thành công: “Cập nhật thành công”', '- Thất bại: thông báo lỗi'])],
   ev=[('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Nút luôn hiện ở đầu khối lọc; không cần quyền riêng.\nDuring:\n– Nạp cấu hình đang lưu của người dùng cho màn.\n'
        'After:\n– Mở cửa sổ “Cài đặt bộ lọc”.'),
       ('Kéo đổi vị trí ô lọc', 'Drag',
        'Before:\n– Kéo bằng tay nắm của dòng.\nDuring:\n– Đổi thứ tự trong cửa sổ.\nAfter:\n– Chưa áp lên màn hình cho tới khi bấm Lưu.'),
       ('Bỏ tích một ô lọc', 'Change',
        'Before:\n– Áp cho mọi ô.\nDuring:\n– Ghi nhận trạng thái tích trong cửa sổ.\nAfter:\n– Chưa áp cho tới khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình gắn với người dùng đang đăng nhập và màn này.\n'
        'During:\n– Ghi cấu hình; lỗi → hiển thị thông báo lỗi.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”; khối lọc cập nhật ngay.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Tích lại toàn bộ ô, thứ tự gốc.\nAfter:\n– Chưa lưu; phải bấm Lưu.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Bỏ mọi thay đổi chưa lưu.\nAfter:\n– Đóng cửa sổ, khối lọc giữ nguyên.')])

# ------------------------------------------------------------ 2.4
k = fr(4, 'Chọn hàng hóa',
       rule=('- Popup chọn dữ liệu, Bộ lọc.', 'search'),
       intro=dict(ten='Chọn 1 hàng hóa để lọc báo cáo qua cửa sổ Chọn hàng hóa',
                  mota='Bấm ô Hàng hóa của bộ lọc để mở cửa sổ “Chọn hàng hóa” dùng chung (cây catalog + bảng hàng hóa có tìm kiếm, '
                       'lọc), phạm vi mọi hàng hóa kể cả hàng chưa kinh doanh tại công ty đang xem. Bấm tên 1 hàng để chọn; báo cáo chỉ '
                       'còn hàng đó (cộng trên mọi kho đang chọn).',
                  tacnhan=TN, dieukien=DK + '\n4. Đã chọn Tồn theo công ty (cửa sổ tra hàng theo công ty đang xem).',
                  chinh='1. Người dùng bấm ô Hàng hóa.\n'
                        '2. Hệ thống mở cửa sổ “Chọn hàng hóa”: dòng công ty đang xem, cây catalog (số hàng mỗi nhánh), ô tìm theo mã, '
                        'tên, model, barcode, mã đặt hàng, công tắc Còn tồn / Gồm hàng ngoài catalog, bảng hàng hóa.\n'
                        '3. Người dùng tìm / lọc rồi bấm vào tên hàng.\n'
                        '4. Hệ thống đóng cửa sổ, ô Hàng hóa hiện “<mã> - <tên>”, ghi tạm bộ lọc, về trang 1 và nạp lại báo cáo (1 lần).',
                  phu='• Bấm Đóng / (x) → đóng, giữ hàng đã chọn trước đó.\n'
                      '• Bấm dấu × trên ô Hàng hóa → bỏ chọn, báo cáo nạp lại mọi hàng (không mở cửa sổ).\n'
                      '• Hàng đã chọn không có tồn ở các kho → bảng ' + M_EMPTY + '\n'
                      '• Tồn theo công ty khác công ty của tài khoản mà tài khoản không có quyền tra hàng ở công ty đó → cửa sổ báo “Không '
                      'tải được số lượng — Thử lại” và “Không tải được danh sách hàng hoá — Máy chủ báo lỗi (mã 403)”, không chọn được hàng '
                      '(hành vi hiện tại của cửa sổ dùng chung).\n'
                      '• F5 trong 10 phút → ô Hàng hóa vẫn hiện tên hàng đã chọn.',
                  dacbiet='Chỉ chọn được 1 hàng (giữ y ERP); cửa sổ có nút Phóng to toàn màn hình.'),
       layout=dict(menu=MENU + ' => Hàng hóa', shot=shot('04b_picker_tpe'), shot_caption='Cửa sổ Chọn hàng hóa (công ty TPE)',
                   note='Modal Chọn hàng hóa được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.',
                   extra=[(shot('04_picker'), 'Tồn theo công ty CN Hải Phòng trên tài khoản công ty TPE: cửa sổ báo lỗi 403'),
                          (shot('04c_one'), 'Đã chọn 1 hàng: báo cáo còn 1 mặt hàng (ENEO-700-V5231 — 47 trên 4 kho)')]),
       ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Chọn hàng hóa”', ['- Kèm nút Phóng to toàn màn hình và nút (x)']),
           ('Dòng công ty', 'Label', 'Read-only', '–', '–', 'Công ty đang xem', ['- “Công ty <tên công ty>”',
            '- Icon ⓘ: “Gồm mọi hàng hoá, kể cả hàng chưa kinh doanh tại công ty này; ẩn hàng tạm và hàng làm dịch vụ.”']),
           ('Cây catalog', 'Table/Grid', 'Enable', '–', 'Không', 'Tất cả hàng hoá', ['- Tất cả hàng hoá, Chưa xếp catalog, các nhánh '
            'catalog kèm số hàng', '- Ô tìm trong cây']),
           ('Ô tìm hàng', 'Textbox', 'Enable', '–', 'Không', 'Trống', '- Gợi ý “Tìm theo mã, tên hàng hoá, model, barcode, mã đặt hàng”'),
           ('Công tắc Còn tồn', 'Checkbox', 'Enable', '–', 'Không', 'Tắt', '- Bật: chỉ hàng còn tồn bán được'),
           ('Công tắc Gồm hàng ngoài catalog', 'Checkbox', 'Enable', '–', 'Không', 'Bật', '- Bật: gồm cả hàng chưa xếp catalog'),
           ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở thêm ô lọc của cửa sổ.'),
           ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa điều kiện tìm trong cửa sổ.'),
           ('Bảng hàng hóa', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
            ['- Cột STT, Ảnh, Mã hàng, Tên hàng hoá, Model, Thương hiệu, Loại sản phẩm, ĐVT, Tồn bán được, Hãng sản xuất, Xuất xứ',
             '- Bấm tên hàng → chọn và đóng cửa sổ']),
           ('Dòng gợi ý chân cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Bấm vào tên hàng để chọn”'),
           ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không đổi hàng đã chọn.'),
           ('Ô Hàng hóa sau khi chọn', 'Textbox', 'Read-only', '–', '–', 'Trống', ['- “<mã> - <tên>”', '- Dấu × bỏ chọn']),
           ('Thông báo lỗi tải', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
            ['- “Không tải được số lượng — Thử lại”', '- “Không tải được danh sách hàng hoá”', '- Nút Thử lại'])],
       ev=[('Bấm ô Hàng hóa', 'Click',
            'Before:\n– Lấy công ty đang chọn ở ô Tồn theo công ty.\nDuring:\n– Mở cửa sổ, nạp cây catalog và danh sách hàng.\n'
            'After:\n– Cửa sổ hiển thị trên màn báo cáo.'),
           ('Bấm tên hàng trong bảng', 'Click',
            'Before:\n– Chỉ chọn 1 hàng.\nDuring:\n– Ghi tên hàng rồi mã hàng vào bộ lọc (để chỉ nạp 1 lần), ghi tạm bộ lọc.\n'
            'After:\n– Đóng cửa sổ, về trang 1, nạp lại báo cáo.'),
           ('Bấm dấu × trên ô Hàng hóa', 'Click',
            'Before:\n– Ô đang có hàng.\nDuring:\n– Xóa hàng khỏi bộ lọc, không mở cửa sổ.\nAfter:\n– Nạp lại báo cáo mọi hàng.'),
           ('Bấm Đóng hoặc (x)', 'Click',
            'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không đổi bộ lọc.\nAfter:\n– Đóng cửa sổ.'),
           ('Tìm / lọc trong cửa sổ', 'Change',
            'Before:\n– Áp cho ô tìm, cây catalog, công tắc.\nDuring:\n– Nạp lại bảng hàng.\n' + ERR + '\nAfter:\n– Bảng cập nhật; lỗi → nút Thử lại.')])
d.p('2.4.%d Mục đích thiết kế popup' % k)
d.bullets([
    'Trả lời câu hỏi: tồn của RIÊNG một mặt hàng (tìm theo mã / tên / model / barcode) trên các kho đang chọn là bao nhiêu, thuộc công ty '
    'thuê kho nào — khi công ty có hàng nghìn mặt hàng.',
    'Là cửa sổ nổi để giữ nguyên ngữ cảnh báo cáo (ngày, kho, các ô lọc khác); cây catalog + tìm kiếm cần chỗ rộng nên không nhét vào '
    'ô chọn thả xuống.',
    'Ràng buộc khớp số: sau khi chọn, báo cáo còn tối đa 1 mặt hàng, SL tồn = SL của hàng đó khi không lọc hàng; Tồn bán được trong cửa '
    'sổ là số của công ty, KHÔNG phải tồn trên các kho đang xem.',
    'Người dùng làm tiếp: đổi ĐVT (mục 2.5), In / Xuất Excel đúng 1 hàng; mỗi lần mở là cửa sổ mới.',
])
k += 1
d.p('2.4.%d Các biến thể theo con số bấm' % k)
d.popup_variant_table([
    ('Ô Hàng hóa khi chưa chọn hàng', 'Mọi hàng hóa của công ty đang xem (kể cả chưa kinh doanh)', '“Chọn hàng hóa”',
     'Không ẩn ô nào; chỉ chọn 1 hàng'),
    ('Ô Hàng hóa khi đã có hàng', 'Như trên; hàng cũ được thay khi chọn hàng mới', '“Chọn hàng hóa”', 'Không ẩn ô nào'),
])

# ------------------------------------------------------------ 2.5
k = fr(5, 'Xem tồn theo công ty thuê kho và đổi ĐVT',
       rule=('- Màn Xem chi tiết và Báo cáo.', 'detail'),
       intro=dict(ten='Xem tồn của mặt hàng theo từng công ty thuê kho và đổi ĐVT từng hàng',
                  mota='Ngay trong bảng báo cáo: nhóm cột Chi tiết cho biết SL tồn của từng công ty thuê kho (V1); ô ĐVT trên mỗi dòng cho '
                       'đổi đơn vị hiển thị riêng từng mặt hàng (SL tồn và các cột công ty quy đổi theo hệ số). Chỉ đổi cách hiển thị, '
                       'không tính lại số; ĐVT đã chọn được dùng cho In / Xuất Excel.',
                  tacnhan=TN, dieukien=DK + '\n4. Báo cáo đã có ít nhất 1 mặt hàng.',
                  chinh='1. Người dùng (V1) đọc nhóm cột Chi tiết: mỗi công ty thuê kho đang lọc 1 cột, rê chuột vào mã công ty để xem tên.\n'
                        '2. Người dùng bấm ô ĐVT ở dòng mặt hàng → danh sách ĐVT của hàng “<tên> (x<hệ số>)”.\n'
                        '3. Người dùng chọn ĐVT khác.\n'
                        '4. Hệ thống chia SL tồn và mọi cột công ty của hàng đó cho hệ số, làm tròn 2 số lẻ, hiển thị lại (không gọi máy chủ).',
                  phu='• V2 / V3: không có nhóm cột Chi tiết, chỉ đổi ĐVT.\n'
                      '• Hàng chỉ 1 ĐVT → ô chọn chỉ 1 lựa chọn; hàng chưa khai ĐVT → ô trống.\n'
                      '• Đổi trang / đổi bộ lọc → ĐVT đã chọn được giữ theo từng hàng (không ghi tạm khi F5).\n'
                      '• Công ty thuê kho không có tồn của hàng → ô trống.',
                  dacbiet='Đổi ĐVT không gọi lại máy chủ. In / Excel gửi kèm ĐVT đã chọn từng hàng (hàng chưa đổi dùng ĐVT cơ sở).'),
       layout=dict(menu=MENU + ' => ĐVT', shot=shot('03_detail'),
                   shot_caption='Bảng với nhóm cột Chi tiết TPE / TPHP / TPV (khối lọc thu gọn)',
                   note='Thao tác ngay trên bảng của màn báo cáo theo đường dẫn ở trên.',
                   extra=[(shot('03c_unit'), 'Ô chọn ĐVT của hàng ENEO-410-S4136 (Can 1L / Thùng 24C-1L x24)'),
                          (shot('03d_unit_after'), 'Đổi sang Thùng 24C-1L (x24): 24 Can 1L → 1 ở SL tồn và cột TPHP')]),
       ui=[('Nhóm tiêu đề Chi tiết', 'Label', 'Hiển thị', '–', '–', 'Theo quyền',
            ['- Chỉ V1, tầng trên gộp các cột công ty', '- Icon ⓘ: “' + TIP_CHITIET + '”']),
           ('Tiêu đề cột công ty thuê kho', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu',
            ['- Mã công ty, sắp theo mã', '- Rê chuột: tên công ty']),
           ('Ô số của cột công ty', 'Table/Grid', 'Read-only', 'Số, tối đa 2 số lẻ', '–', 'Theo dữ liệu',
            ['- Căn phải, dấu phẩy hàng nghìn', '- Số 0 để trống']),
           ('Ô chọn ĐVT', 'Dropdown', 'Enable', 'ĐVT của hàng', 'Không', 'ĐVT cơ sở',
            ['- Mặc định: ĐVT cơ sở (hệ số nhỏ nhất)', '- Lựa chọn “<tên> (x<hệ số>)”; hệ số 1 chỉ hiện tên',
             '- Không có nút × bỏ chọn', '- Đổi → quy đổi SL tồn và các cột công ty của hàng']),
           ('Cột SL tồn sau quy đổi', 'Table/Grid', 'Read-only', 'Số, tối đa 2 số lẻ', '–', 'Theo dữ liệu',
            ['- = số theo ĐVT cơ sở ÷ hệ số, làm tròn 2 số lẻ', '- Vd 24 Can 1L → Thùng x24 = 1']),
           ('Icon ⓘ cột ĐVT', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “' + TIP_DVT + '”')],
       ev=[('Đổi ĐVT dòng mặt hàng', 'Change',
            'Before:\n– Bỏ qua giá trị rỗng / trùng ĐVT đang chọn.\nDuring:\n– Ghi ĐVT chọn cho hàng; lấy hệ số, chia SL tồn và các cột '
            'công ty, làm tròn 2 số lẻ.\nAfter:\n– Dòng hiển thị số mới; không gọi máy chủ; In / Excel dùng ĐVT này.'),
           ('Rê chuột vào mã công ty ở tiêu đề', 'Hover',
            'Before:\n– Có nhóm Chi tiết (V1).\nDuring:\n– Lấy tên công ty.\nAfter:\n– Hiện tên đầy đủ.'),
           ('Đổi trang hoặc bộ lọc', 'System',
            'Before:\n– Có dữ liệu mới.\nDuring:\n– Áp lại ĐVT đã chọn cho hàng có trong trang mới.\nAfter:\n– Hàng đã đổi ĐVT vẫn hiện '
            'theo ĐVT đó; ĐVT không còn thuộc hàng → về ĐVT cơ sở.')])
d.p('2.5.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('“Tập dữ liệu” là các mặt hàng của trang đang xem (mục 2.1.6).')
d.data_table([
    ('Cột công ty thuê kho', 'Tổng thay đổi tồn ghi cho công ty đó trên mọi kho đang chọn tới hết Tính đến ngày (theo ĐVT cơ sở rồi quy '
                             'đổi).', TIP_CHITIET),
    ('Cột SL tồn', 'Tổng các cột công ty thuê kho đang lọc.', TIP_SL),
    ('ĐVT', 'Danh sách ĐVT của hàng, ĐVT cơ sở (hệ số nhỏ nhất) đứng đầu; số = ĐVT cơ sở ÷ hệ số, làm tròn 2 số lẻ.', TIP_DVT),
])

# ------------------------------------------------------------ 2.6
fr(6, 'In báo cáo', usecase=('FR-06', 'In báo cáo', 'io', A),
   rule=('- Quy tắc In và Báo cáo.', 'list'),
   intro=dict(ten='In báo cáo tồn kho tổng hợp theo mặt hàng (xem trước rồi in)',
              mota='Chọn kiểu in Đầy đủ (có nhóm Chi tiết: mỗi công ty thuê kho 1 cột) hoặc Ngắn gọn (chỉ thông tin mặt hàng và SL tồn), '
                   'chọn cột in, xem trước bản in gồm letterhead công ty đang xem, tiêu đề, Tính đến ngày, Kho, bảng TOÀN BỘ mặt hàng theo '
                   'bộ lọc đang hiển thị (không riêng trang đang xem), theo ĐVT đã chọn từng hàng, khối ký Trưởng kho / Người lập báo cáo; '
                   'bấm In.',
              tacnhan=TN, dieukien=DK + '\n4. Đã có báo cáo (đủ 3 ô bắt buộc).',
              chinh='1. Người dùng bấm In danh sách.\n'
                    '2. Hệ thống mở cửa sổ “In báo cáo”: kiểu Đầy đủ được chọn, tích sẵn mọi cột của kiểu.\n'
                    '3. Người dùng chọn kiểu, tích / bỏ tích cột, bấm In.\n'
                    '4. Hệ thống kiểm quyền, lấy toàn bộ mặt hàng theo bộ lọc của báo cáo đang hiển thị, quy đổi theo ĐVT đã chọn; đếm '
                    'số dòng in (mỗi mặt hàng 1 dòng).\n'
                    '5. Hệ thống mở cửa sổ “Xem trước báo cáo tồn kho tổng hợp theo mặt hàng”; người dùng bấm In → hộp thoại in của '
                    'trình duyệt.',
              phu='• Chưa có báo cáo (thiếu ô bắt buộc) → không mở cửa sổ, chữ đỏ dưới ô thiếu.\n'
                  '• Bỏ tích hết cột → ' + M_NOCOL + ', cửa sổ không đóng.\n'
                  '• Vượt 2.000 mặt hàng → bản xem trước không có nội dung, hiện ' + M_LIMIT + ', ẩn nút In.\n'
                  '• Báo cáo rỗng → bản in có dòng “Không có dữ liệu”.\n'
                  '• Bấm Hủy / (x) → đóng, không in. Lỗi → “Không tải được dữ liệu in” hoặc câu máy chủ trả.',
              dacbiet='STT luôn được in; số theo ĐVT đã chọn, làm tròn 2 số lẻ, số 0 để trống. Letterhead theo công ty ĐANG XEM (ô Tồn '
                      'theo công ty). Kiểu Đầy đủ in nhóm Chi tiết cho MỌI người có quyền xem (kể cả V2 / V3 — giữ y ERP).'),
   layout=dict(menu=MENU + ' => In danh sách', shot=shot('05_print'), shot_caption='Cửa sổ In báo cáo (kiểu Đầy đủ, chọn cột in)',
               note='Modal In báo cáo và Xem trước được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.',
               extra=[(shot('05b_preview'), 'Xem trước bản in kiểu Đầy đủ — CN Hải Phòng, 4 kho'),
                      (shot('05c_print_err'), 'Bỏ tích hết cột rồi bấm In: “Vui lòng chọn ít nhất 1 cột để in”')]),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“In báo cáo”', 'Kèm nút (x) đóng.'),
       ('Kiểu in', 'Radio', 'Enable', '2 giá trị', 'Có', 'Đầy đủ',
        ['- Mặc định: Đầy đủ', '- Đầy đủ: “Có nhóm Chi tiết: mỗi công ty thuê kho 1 cột.”', '- Ngắn gọn: “Chỉ thông tin mặt hàng và SL tồn.”',
         '- Đổi kiểu → danh sách cột đổi theo']),
       ('Tiêu đề Chọn cột in', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- Icon ⓘ: “Cột STT luôn được in. Số lượng theo ĐVT đang chọn của từng hàng.”'),
       ('Ô Chọn tất cả', 'Checkbox', 'Enable', '–', 'Không', 'Tích', ['- Tích / bỏ tích mọi cột', '- Bán chọn khi tích 1 phần']),
       ('Danh sách cột', 'Checkbox', 'Enable', '7 hoặc 6 cột', 'Ít nhất 1', 'Tích hết',
        ['- Đầy đủ: Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn, Chi tiết theo công ty thuê kho',
         '- Ngắn gọn: 6 cột đầu']),
       ('Chữ lỗi chọn cột', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + M_NOCOL),
       ('Nút In (cửa sổ In báo cáo)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Kiểm ≥ 1 cột rồi mở xem trước.'),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không in.'),
       ('Cửa sổ Xem trước', 'Popup', 'Read-only', '–', '–', 'Ẩn',
        ['- Tiêu đề “Xem trước báo cáo tồn kho tổng hợp theo mặt hàng”', '- Letterhead, “BÁO CÁO TỒN KHO TỔNG HỢP THEO MẶT HÀNG”, Tính '
         'đến ngày, Kho (mã - tên các kho), bảng (Đầy đủ: 2 tầng tiêu đề, nhóm “Chi tiết”), khối ký Trưởng kho / Người lập báo cáo']),
       ('Nút In (cửa sổ Xem trước)', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Mở hộp thoại in của trình duyệt', '- Ẩn khi vượt trần dòng']),
       ('Nút (x) cửa sổ Xem trước', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng xem trước.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Vượt trần: ' + M_LIMIT, '- Không có nội dung: ' + M_NOPRINT, '- Lỗi: “Không tải được dữ liệu in”'])],
   ev=[('Bấm In danh sách', 'Click',
        'Before:\n– Chưa có báo cáo (thiếu ô bắt buộc) → chữ đỏ dưới ô thiếu, mở khối lọc, dừng.\n'
        'During:\n– Mở cửa sổ In báo cáo, kiểu Đầy đủ, tích hết cột.\nAfter:\n– Chờ người dùng chọn.'),
       ('Đổi kiểu in', 'Change',
        'Before:\n– Đầy đủ / Ngắn gọn.\nDuring:\n– Đổi danh sách cột theo kiểu, tích hết.\nAfter:\n– Ô Chọn tất cả cập nhật.'),
       ('Bấm In (cửa sổ In báo cáo)', 'Click',
        'Before:\n– Kiểm tra quyền xem báo cáo tồn kho; không có → ' + NOPERM + ' và dừng.\n'
        '– Bỏ hết cột → ' + M_NOCOL + ', không đóng.\n'
        'During:\n– Lấy toàn bộ mặt hàng theo bộ lọc của báo cáo đang hiển thị, quy đổi theo ĐVT đã chọn từng hàng; cột lạ bị bỏ (rỗng = '
        'đủ cột).\n– Đếm dòng in; > 2.000 → không dựng nội dung, báo vượt trần.\n' + ERR + '\n'
        'After:\n– Mở cửa sổ Xem trước, letterhead công ty đang xem.'),
       ('Bấm In (cửa sổ Xem trước)', 'Click',
        'Before:\n– Bản xem trước đã tải xong.\nDuring:\n– In qua khung ẩn, giữ đúng mẫu.\nAfter:\n– Hộp thoại in của trình duyệt mở.'),
       ('Bấm Hủy hoặc (x)', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không in.\nAfter:\n– Đóng cửa sổ; báo cáo giữ nguyên.')])

# ------------------------------------------------------------ 2.7
fr(7, 'Xuất Excel', usecase=('FR-07', 'Xuất Excel', 'io', A),
   rule=('- Quy tắc Excel.', 'excel'),
   intro=dict(ten='Xuất báo cáo tồn kho tổng hợp theo mặt hàng ra Excel',
              mota='Chọn kiểu Đầy đủ hoặc Ngắn gọn rồi tải file Excel gồm TOÀN BỘ mặt hàng theo bộ lọc của báo cáo đang hiển thị (không '
                   'riêng trang đang xem), đủ cột của kiểu đã chọn (Excel không có bước chọn cột), theo ĐVT đã chọn từng hàng.',
              tacnhan=TN, dieukien=DK + '\n4. Đã có báo cáo (đủ 3 ô bắt buộc).',
              chinh='1. Người dùng bấm Xuất Excel ở đầu khối bộ lọc.\n'
                    '2. Hệ thống mở cửa sổ “Xuất Excel báo cáo tồn kho tổng hợp theo mặt hàng”, kiểu Đầy đủ được chọn.\n'
                    '3. Người dùng chọn kiểu, bấm Xuất Excel trong cửa sổ.\n'
                    '4. Hệ thống khóa nút (chữ “Đang xuất…”, vòng xoay), kiểm quyền, lấy toàn bộ mặt hàng, dựng file.\n'
                    '5. Trình duyệt tải file “' + FILE + '”; cửa sổ đóng.',
              phu='• Chưa có báo cáo → không mở cửa sổ, chữ đỏ dưới ô thiếu.\n'
                  '• Bấm Hủy / (x) → đóng, không xuất.\n'
                  '• Lỗi → ' + M_XLS_ERR + ' (thiếu quyền: báo không có quyền), giữ cửa sổ để bấm lại.\n'
                  '• Báo cáo rỗng → vẫn tải file, bảng có dòng “Không có dữ liệu”.',
              dacbiet='Luôn tải thẳng, không gửi mail (ERP gửi mail khi ≥ 500 mặt hàng). Cấu trúc file: dòng 1 letterhead công ty đang xem '
                      '(rộng bằng bảng); tiêu đề “BÁO CÁO TỒN KHO TỔNG HỢP THEO MẶT HÀNG”; “Tính đến ngày: dd/mm/yyyy”; “Kho: <mã - tên '
                      'các kho>”; bảng (Đầy đủ: 2 tầng tiêu đề, nhóm “Chi tiết” mỗi công ty thuê kho 1 cột — có cho mọi người xem, kể cả '
                      'V2 / V3); khối ký Trưởng kho / Người lập báo cáo kèm ngày. Số lượng là ô số có dấu phân cách hàng nghìn (cộng '
                      'được), số 0 để trống. Vài nghìn mặt hàng có thể mất vài chục giây.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('06_export'), shot_caption='Cửa sổ Xuất Excel — chọn kiểu xuất',
               note='Modal Xuất Excel được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Xuất Excel báo cáo tồn kho tổng hợp theo mặt hàng”', 'Kèm biểu tượng Excel, nút (x).'),
       ('Nhãn Kiểu xuất', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Kiểu xuất”'),
       ('Kiểu xuất', 'Radio', 'Enable', '2 giá trị', 'Có', 'Đầy đủ',
        ['- Mặc định: Đầy đủ (mỗi lần mở về Đầy đủ)', '- Đầy đủ: “Có nhóm Chi tiết: mỗi công ty thuê kho 1 cột.”',
         '- Ngắn gọn: “Chỉ thông tin mặt hàng và SL tồn.”']),
       ('Nút Xuất Excel (cửa sổ)', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → tải file', '- Khóa khi đang xuất, chữ “Đang xuất…”']),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Hủy.'),
       ('Nút Xuất Excel (đầu khối lọc)', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Nền xanh lá nhạt', '- Khi đang xuất: chữ “Đang xuất…”, vòng xoay, khóa']),
       ('File tải về', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Tên “' + FILE + '”', '- Đầy đủ: STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn, Chi tiết (mỗi công ty thuê kho 1 cột)',
         '- Ngắn gọn: STT + 6 cột mặt hàng', '- ĐVT ghi “<tên> (x<hệ số>)” theo ĐVT đã chọn']),
       ('Thanh tải trang', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- Chạy trên đầu trang trong lúc xuất'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + M_XLS_ERR, '- Thiếu quyền: báo không có quyền'])],
   ev=[('Bấm Xuất Excel (đầu khối lọc)', 'Click',
        'Before:\n– Chưa có báo cáo → chữ đỏ dưới ô thiếu, dừng.\nDuring:\n– Mở cửa sổ, kiểu Đầy đủ.\nAfter:\n– Chờ chọn kiểu.'),
       ('Chọn kiểu xuất', 'Change',
        'Before:\n– Đầy đủ / Ngắn gọn.\nDuring:\n– Ghi nhận kiểu.\nAfter:\n– Chưa xuất cho tới khi bấm Xuất Excel.'),
       ('Bấm Xuất Excel (cửa sổ)', 'Click',
        'Before:\n– Kiểm tra quyền xem báo cáo tồn kho; không có → báo không có quyền và dừng.\n– Chặn bấm lặp khi đang xuất.\n'
        'During:\n– Lấy toàn bộ mặt hàng theo bộ lọc của báo cáo đang hiển thị, theo ĐVT đã chọn; dựng file theo kiểu.\n' + ERR + '\n'
        'After:\n– Tải “' + FILE + '”, đóng cửa sổ, mở khóa nút. Lỗi → ' + M_XLS_ERR + ', giữ cửa sổ.'),
       ('Bấm Hủy, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không xuất.\nAfter:\n– Đóng cửa sổ; lần mở sau về Đầy đủ.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Báo cáo tồn kho tổng hợp theo mặt hàng; không lặp lại các quy tắc đã có '
           'trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Ô bắt buộc và mặc định', [
        '– Bắt buộc Tính đến ngày, Tồn theo công ty, ít nhất 1 Kho; thiếu thì không tính, báo chữ đỏ khi bấm Tìm kiếm / In / Xuất.',
        '– Mặc định: hôm nay, công ty của người dùng, TOÀN BỘ kho của công ty (Xem toàn bộ kho tích), mọi công ty thuê của các kho.',
        '– Đổi công ty chọn lại hết kho; đổi kho tích mọi công ty thuê của các kho.'],
     ['Tìm kiếm và lọc', 'In báo cáo', 'Xuất Excel']),
    ('BR-02', 'SL tồn của công ty thuê kho', [
        '– = tổng thay đổi tồn (nhập +, xuất −) ghi cho công ty trên các kho đang chọn tới hết Tính đến ngày, từ mọi chứng từ kho (Phần 5).',
        '– Khớp Tồn cuối kỳ của Thẻ kho cùng hàng / kho / công ty / ngày (Tồn đầu kỳ + Nhập − Xuất).'],
     ['Xem báo cáo', 'In báo cáo', 'Xuất Excel']),
    ('BR-03', 'Mặt hàng lên báo cáo', [
        '– Mặt hàng có tổng tồn các công ty thuê kho đang lọc ≠ 0 (có thể âm); SL tồn = tổng các cột công ty.',
        '– Sắp theo tên hàng; phân trang theo mặt hàng (mặc định 20, tối đa 100).',
        '– Khối tổng hợp, dòng TỔNG tính trên toàn tập, không theo trang.'],
     ['Xem báo cáo']),
    ('BR-04', 'Nhóm cột Chi tiết theo quyền', [
        '– Màn hình: nhóm cột Chi tiết, khối Theo công ty thuê kho, ô Công ty thuê kho có tồn chỉ hiện với V1 (hoặc Super admin).',
        '– In / Excel kiểu Đầy đủ luôn có nhóm Chi tiết cho mọi người có quyền xem (giữ y ERP).'],
     ['Xem báo cáo', 'In báo cáo', 'Xuất Excel']),
    ('BR-05', 'Phạm vi theo quyền', [
        '– Có 1 trong 3 quyền xem báo cáo tồn kho mới xem được; quyền cao nhất thắng.',
        '– Tổng công ty: mọi công ty / kho; công ty: kho của công ty mình; kho: kho mình là thủ kho.',
        '– Máy chủ khóa công ty với người không có quyền tổng công ty; kho ngoài phạm vi bị bỏ, hết kho → “Vui lòng chọn kho”.'],
     ['Mọi chức năng']),
    ('BR-06', 'Quy đổi ĐVT', [
        '– Số trên màn = số ĐVT cơ sở ÷ hệ số ĐVT chọn riêng từng hàng, làm tròn 2 số lẻ.',
        '– In / Excel dùng đúng ĐVT đã chọn trên màn (hàng chưa đổi: ĐVT cơ sở).'],
     ['Xem tồn theo công ty thuê kho', 'In báo cáo', 'Xuất Excel']),
    ('BR-07', 'Lọc hợp đồng', [
        '– Chỉ cộng thay đổi tồn của lô nhập / lô xuất thuộc phiếu gắn hợp đồng bán có mã chứa chuỗi gõ (khớp một phần).',
        '– Ký tự % và _ là ký tự đại diện (không được hiểu theo nghĩa đen).'],
     ['Tìm kiếm và lọc']),
    ('BR-08', 'Chuẩn hóa dữ liệu lọc', [
        '– Ngày nhận dd/mm/yyyy; sai định dạng → “Vui lòng chọn ngày”.',
        '– Ô chọn khớp chính xác; nhiều giá trị trong 1 ô = HOẶC; nhiều ô = VÀ; Hợp đồng bỏ khoảng trắng đầu / cuối.',
        '– Công ty thuê ngoài danh sách của các kho bị bỏ qua.'],
     ['Tìm kiếm và lọc']),
    ('BR-09', 'Ghi nhớ bộ lọc', [
        '– Bộ lọc (kể cả hàng đã chọn) ghi tạm 10 phút trên trình duyệt; F5 / tab mới khôi phục.',
        '– Rời sang màn khác hoặc bấm Xóa lọc → xóa. Cấu hình ô lọc (Cài đặt bộ lọc) lưu theo người dùng.'],
     ['Tìm kiếm và lọc', 'Cài đặt bộ lọc']),
    ('BR-10', 'In và xuất', [
        '– Theo bộ lọc của báo cáo đang hiển thị, toàn bộ mặt hàng; letterhead theo công ty đang xem.',
        '– In tối đa 2.000 mặt hàng; vượt thì không in, báo thu hẹp bộ lọc.',
        '– Excel không giới hạn, tải thẳng, tên “' + FILE + '”.'],
     ['In báo cáo', 'Xuất Excel']),
    ('BR-11', 'Tính duy nhất', [
        '– Mỗi mặt hàng 1 dòng (cộng mọi kho); mỗi công ty thuê kho 1 cột; không có cấp cha – con.'],
     ['Xem báo cáo']),
    ('BR-12', 'Chỉ đọc, không ghi lịch sử', [
        '– Màn không tạo / sửa / xóa dữ liệu, không có lịch sử thay đổi; số liệu đổi theo chứng từ kho ở Phần 5.'],
     ['Mọi chức năng']),
    ('BR-13', 'Khác hệ thống ERP (có chủ đích)', [
        '– Có In xem trước (ERP ẩn nút In); Excel không gửi mail; số 0 để trống (ERP in “-”).',
        '– Kho ngoài phạm vi / khác công ty bị bỏ; các kho không có công ty thuê nào → rỗng (ERP lỗi).'],
     ['Xem báo cáo', 'In báo cáo', 'Xuất Excel']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Báo cáo tồn kho tổng hợp theo mặt hàng chỉ đọc, không ghi dữ liệu và không màn nào mở sang báo cáo này. Các màn hình dưới đây ghi '
    'các thay đổi tồn mà báo cáo cộng (nhập +, xuất −, theo công ty thuê kho), cung cấp danh mục cho bộ lọc, hoặc đọc cùng nguồn tồn dùng '
    'để đối chiếu số.')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', 'Khai báo tồn kho đầu kỳ (tồn đầu kỳ — cộng vào SL tồn)', 'Kho -> Tồn kho đầu kỳ'),
    ('2', 'Kho', 'Phiếu nhập kho (cộng tồn; hợp đồng của phiếu là điều kiện ô lọc Hợp đồng)', 'Kho -> Nhập kho'),
    ('3', 'Kho', 'Phiếu nhập kho điều chỉnh kiểm kê (cộng tồn phần thừa sau kiểm kê)', 'Kho -> Nhập kho'),
    ('4', 'Tài chính', 'Phiếu xuất kho (trừ tồn; hợp đồng của phiếu xuất dùng cho ô lọc Hợp đồng)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('5', 'Tài chính', 'Phiếu nhập lại (cộng lại tồn hàng đã xuất)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('6', 'Kho', 'Phiếu xuất điều chỉnh sai số liệu (trừ tồn)', 'Kho -> Xuất kho'),
    ('7', 'Kho', 'Phiếu xuất kho điều chỉnh kiểm kê (trừ tồn phần thiếu sau kiểm kê)', 'Kho -> Xuất kho'),
    ('8', 'Kho', 'Điều chuyển kho (trừ tồn kho đi, cộng tồn kho đến; chọn cả 2 kho thì SL tồn không đổi)', 'Kho -> Điều chuyển'),
    ('9', 'Kho', 'Kiểm kê theo vị trí, Kiểm kê theo hàng hóa (kết quả kiểm kê sinh phiếu nhập / xuất điều chỉnh kiểm kê ở dòng 3, 7)',
     'Kho -> Theo vị trí'),
    ('10', 'Hệ thống ERP', 'Phiếu nhập lại điều chỉnh sai số liệu (cộng tồn — chưa chuyển sang HRM)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
    ('11', 'Hệ thống ERP', 'Hợp đồng bán (mã hợp đồng dùng cho ô lọc Hợp đồng)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
    ('12', 'Kho', 'Kho vật lý, Kho kế toán (danh sách ô Kho, Công ty thuê kho — cột của nhóm Chi tiết)', 'Kho -> Danh mục'),
    ('13', 'Kho', 'Báo cáo tồn kho chi tiết theo mặt hàng (cùng 3 quyền, cùng cách cộng tồn: chọn 1 kho thì SL tồn và cột công ty khớp)',
     'Kho -> Báo cáo kho'),
    ('14', 'Kho', 'Báo cáo tồn kho theo vị trí (cùng nguồn tồn: tổng các vị trí của 1 hàng tại 1 kho = SL tồn khi chọn kho đó)',
     'Kho -> Báo cáo kho'),
    ('15', 'Kho', 'Thẻ kho (Tồn cuối kỳ của 1 hàng / kho / công ty thuê = cột công ty; đối soát từng chứng từ)', 'Kho -> Báo cáo kho'),
    ('16', 'Kho', 'Báo cáo tồn theo kho, Tổng hợp xuất nhập tồn (cùng 3 quyền và phạm vi kho)', 'Kho -> Báo cáo kho'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()

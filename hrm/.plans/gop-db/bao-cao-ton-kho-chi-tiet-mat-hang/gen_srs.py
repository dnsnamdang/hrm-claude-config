# -*- coding: utf-8 -*-
"""SRS màn "Báo cáo tồn kho chi tiết theo mặt hàng" (phân hệ Kho › Báo cáo kho) — form chuẩn + quy định màn BÁO CÁO
(bảng Cách lấy dữ liệu, bảng popup, Mục đích thiết kế popup) + chuẩn 04/11 (Mục lục trang riêng căn giữa, Phần 5 bảng 4 cột).

Chạy: python gen_srs.py  → SRS - Báo cáo tồn kho chi tiết theo mặt hàng.docx
Khung: srs-documenter (SrsDoc) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc ../kiem-ke-theo-hang-hoa/gen_srs.py
  (06/11) + cách viết màn báo cáo ../report-limit-debts/gen_srs.py.
Nguồn đọc 06/11/2026 (nhánh develop cả 2 repo):
  FE  pages/warehouse/stock-detail-by-product/{index.vue, components/StockDetailSummary.vue, components/StockDetailTable.vue},
      pages/warehouse/stock-card/components/{ExportModeModal.vue, format.js} (dùng chung), components/report/V2BaseReportPrintModal.vue,
      components/print/ReportPrintPreviewModal.vue + utils/mixins/reportPrintPreviewMixin.js, V2ProductPickerModal, V2BaseSmartFilterPanel,
      modal/filter-customization-modal.vue, utils/mixins/filterStateMixin.js, utils/contract-link.js, components/subsystem-menu/warehouse.js.
  BE  Modules/Finance/{Services/StockDetailByProductReportService.php, Services/WarehouseStockReportService.php,
      Services/StockDetailByProductPrintService.php, Http/Controllers/V1/StockDetailByProductController.php,
      Exports/StockDetailByProductExport.php, Resources/views/{exports/stock_detail_by_product, prints/stock-detail-by-product}.blade.php,
      Routes/api.php (nhóm stock-detail-by-product, chỉ GET)}, PermissionsTableSeeder (nhóm "Báo cáo kho").
  Tài liệu: design.md, plan.md (#11868 #11869 #11872), spec docs/superpowers/specs/gop-db/2026-10-22-bao-cao-ton-kho-chi-tiet-mat-hang-design.md.
Ảnh: ./bctkct_shots — dev-hrm 06/11/2026, DNS Admin (_capture/capture.js, chặn mọi yêu cầu ghi: 0). Bộ lọc mẫu kho HP - Hải Phòng
  (công ty CN Hải Phòng) nạp qua bộ nhớ trình duyệt như F5. Ảnh popup Chọn hàng hóa chụp với công ty TPE (với CN Hải Phòng dev báo
  lỗi 403 — ghi ở báo cáo). Không bật cờ giả nào.
Đối soát số dev 06/11 (_capture/doisoat.js): hàng ENEO-700-V5231, kho HP, công ty thuê TPHP: tồn 31/12/2025 = 70; Thẻ kho 01/01–06/11/2026
  nhập 496, xuất 546, tồn cuối 20 = cột SL tồn báo cáo này = Báo cáo tồn kho tổng hợp theo mặt hàng (20).
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

TEN = 'Báo cáo tồn kho chi tiết theo mặt hàng'
SHOTS = os.path.join(HERE, 'bctkct_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Kho => Báo cáo kho => Báo cáo tồn kho chi tiết theo mặt hàng'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Báo cáo tồn kho chi tiết theo mặt hàng.'
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
FILE = 'bao_cao_ton_kho_chi_tiet_mat_hang.xlsx'

A = 'Thủ kho / Kế toán kho'
TN = ('Người dùng có quyền thực hiện chức năng: có ít nhất 1 trong 3 quyền “%s”, “%s”, “%s” (hoặc là Super admin); phạm vi kho theo '
      'quyền cao nhất (Phần 2).' % (V1, V2, V3))
DK = ('1. Người dùng đăng nhập thành công.\n'
      '2. Người dùng có 1 trong 3 quyền xem báo cáo tồn kho (hoặc là Super admin).\n'
      '3. Có ít nhất 1 kho đang hoạt động trong phạm vi quyền thuộc công ty đang xem.')
TIP_PURPOSE = ('MỤC ĐÍCH BÁO CÁO • Xem tồn của từng mặt hàng tại 1 kho, tính đến ngày đã chọn • Chi tiết theo công ty thuê kho, lô '
               '(hợp đồng) và vị trí • Lọc thêm theo nhóm, tính chất, loại, thương hiệu, hãng sản xuất, hàng hóa, hợp đồng')
TIP_GOAL = ('BÁO CÁO TỒN KHO CHI TIẾT THEO MẶT HÀNG • Tồn của từng mặt hàng tại 1 kho, tính đến hết ngày đã chọn • Chi tiết theo công '
            'ty thuê kho, lô và vị trí • Số liệu tính tại <ngày giờ>')
TIP_MH = ('MẶT HÀNG • Mặt hàng còn tồn: tổng tồn các công ty thuê kho đang lọc khác 0 • Công ty thuê kho có tồn: số công ty còn ít nhất '
          '1 mặt hàng tồn')
TIP_CT = 'THEO CÔNG TY THUÊ KHO • Số mặt hàng mỗi công ty thuê kho còn tồn, tính đến ngày đã chọn'
TIP_TONG = 'TỔNG • Số mặt hàng còn tồn tại kho đang chọn, tính đến ngày đã chọn • Không cộng số lượng vì mỗi mặt hàng một đơn vị tính'
TIP_DVT = 'ĐVT • Chọn ĐVT riêng từng mặt hàng — số lượng của hàng đó quy đổi theo hệ số'
TIP_HD = 'HỢP ĐỒNG • Hợp đồng của phiếu nhập tạo ra lô'
TIP_SL = ('SL TỒN • Hàng hóa: tổng các công ty thuê kho bên dưới • Công ty: tồn tính đến ngày đã chọn (cột "Cộng" của ERP) • Lô / vị '
          'trí: SL mới nhất tại vị trí (như ERP, không cắt theo ngày)')
TIP_THUE = 'Chọn kho trước. Bỏ trống = mọi công ty thuê của kho'
TIP_HDONG = 'Gõ mã hợp đồng rồi Enter hoặc bấm Tìm kiếm.'

d = SrsDoc(out=OUT, menu=MENU, route='/warehouse/stock-detail-by-product', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Kho': 'menu_phanhe', 'Báo cáo kho': 'menu_nhom', 'Báo cáo tồn kho chi tiết theo mặt hàng': 'menu_muc',
    'Ẩn tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Hàng hóa': 'o_hanghoa',
    'Chọn cấp muốn bung': 'o_capbung', 'In danh sách': 'btn_inds', 'Xuất Excel': 'btn_xuatexcel',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Báo cáo tồn kho chi tiết theo mặt hàng thuộc phân hệ Kho, nhóm Báo cáo kho '
    '(chuyển từ hệ thống ERP: Kho › Báo cáo kho), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu báo cáo cho biết tồn của TỪNG mặt hàng tại MỘT kho, tính đến hết một ngày, chi tiết theo công ty thuê kho, '
    'lô (kèm hợp đồng của phiếu nhập tạo ra lô) và vị trí trong kho.',
    'Ghi rõ cách tính từng con số (khối tổng hợp, dòng TỔNG, cột SL tồn ở từng cấp) để người nghiệm thu đối soát được với Thẻ kho và '
    'Báo cáo tồn kho tổng hợp theo mặt hàng.',
    'Ghi rõ các điểm GIỮ Y HỆT hệ thống ERP theo quyết định của người dùng (22/10/2026) — SL theo lô / vị trí lấy số mới nhất, không cắt '
    'theo ngày — và các điểm khác ERP có chủ đích (hiện hợp đồng của lô, có In, Excel tải thẳng).',
])
d.p('Phạm vi chức năng (7 chức năng, đặc tả ở Phần 3):')
d.bullets([
    'Xem báo cáo (khối tổng hợp + bảng 4 cấp Hàng hóa › Công ty thuê kho › Lô › Vị trí, phân trang theo mặt hàng); Tìm kiếm và lọc '
    '(11 ô lọc, 3 ô bắt buộc); Cài đặt bộ lọc; Chọn hàng hóa (cửa sổ chọn 1 hàng); Xem chi tiết theo công ty thuê kho – lô – vị trí '
    '(bung / thu từng dòng, ô chọn cấp bung, đổi ĐVT từng hàng, mở hợp đồng); In báo cáo (2 kiểu, chọn cột, xem trước); Xuất Excel '
    '(2 kiểu).',
    'Không thuộc màn này: màn CHỈ ĐỌC — không có Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Duyệt / Không duyệt, Import Excel, Lịch sử '
    'thay đổi và không có Tùy chỉnh cột (bảng cố định 8 cột; chọn cột chỉ có ở bản in). Số liệu sinh ra từ các chứng từ kho ở Phần 5.',
])
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Thủ kho / kế toán kho xem nhanh còn bao nhiêu hàng tại một kho vào một ngày, của công ty thuê kho nào, nằm ở lô nào, vị trí nào để '
    'soạn hàng, kiểm kê, đối chiếu với sổ sách.',
    'Đối soát với Thẻ kho (từng chứng từ nhập / xuất của 1 hàng) và Báo cáo tồn kho tổng hợp theo mặt hàng (tồn nhiều kho).',
    'Bản in / file Excel dùng để ký xác nhận (Trưởng kho, Người lập báo cáo) hoặc gửi đối chiếu.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Báo cáo chỉ xem 1 kho mỗi lần; bắt buộc chọn Tính đến ngày, Tồn theo công ty, Kho (BR-01).',
    'SL tồn của công ty thuê kho = tổng mọi thay đổi tồn (nhập +, xuất −) của công ty đó tại kho tới HẾT ngày Tính đến ngày (BR-02); '
    'SL tồn mặt hàng = tổng các công ty được hiện (BR-03).',
    'SL lô / vị trí là số MỚI NHẤT tại vị trí, không cắt theo ngày — chọn ngày quá khứ thì tổng lô có thể khác SL công ty (BR-04, giữ y ERP).',
    'Phạm vi kho theo 1 trong 3 quyền xem báo cáo tồn kho; không có quyền nào thì không vào được màn (BR-05).',
    'Màn không ghi dữ liệu nào; không có lịch sử thay đổi (BR-12).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Tồn kho (SL tồn)', 'Số lượng hàng còn trong kho, tính theo ĐVT cơ sở của hàng rồi quy đổi theo ĐVT đang chọn ở dòng mặt hàng.'),
    ('Tính đến ngày', 'Ngày chốt số liệu: cộng mọi thay đổi tồn tới hết 23:59 của ngày này. Mặc định hôm nay.'),
    ('Tồn theo công ty', 'Công ty đang xem; quyết định danh sách kho chọn được và letterhead bản in / Excel.'),
    ('Kho', 'Kho vật lý (mã - tên) đang hoạt động, thuộc công ty đang xem và trong phạm vi quyền.'),
    ('Công ty thuê kho', 'Công ty có kho kế toán gắn với kho đã chọn; tồn được ghi nhận theo từng công ty này. Bỏ trống = mọi công ty '
                         'thuê của kho.'),
    ('Lô', 'Lô hàng sinh ra khi nhập kho (mã lô dạng <công ty>-<ngày>-…); một lô có thể nằm ở nhiều vị trí.'),
    ('Vị trí', 'Ô chứa hàng trong kho (vd KHOANG1); SL vị trí = số mới nhất ghi nhận tại vị trí đó của lô.'),
    ('Hợp đồng (của lô)', 'Hợp đồng bán gắn với phiếu nhập kho tạo ra lô; mở xem ở Hệ thống ERP.'),
    ('ĐVT cơ sở / hệ số', 'Đơn vị nhỏ nhất của hàng (hệ số 1); ĐVT khác có hệ số quy đổi (vd Thùng 24C-1L = 24 Can 1L).'),
    ('Cấp bung', 'Mức hiển thị sẵn của bảng: Chỉ hàng hóa / Đến công ty thuê kho / Đến lô / Tất cả cấp (đến vị trí).'),
    ('Kiểu Đầy đủ / Ngắn gọn', 'Kiểu in / xuất Excel: Đầy đủ có khối Chi tiết (Công ty, Lô, Vị trí, SL, Cộng); Ngắn gọn chỉ thông tin '
                               'mặt hàng và SL tồn.'),
    ('Trạng thái bản ghi', 'Dòng báo cáo không có trạng thái (không Khóa / Hoạt động); mặt hàng chỉ xuất hiện khi tổng tồn các công ty '
                           'thuê kho đang lọc khác 0.'),
    ('Cấu trúc phân cấp', 'Mặt hàng (cấp I, II…) › Công ty thuê kho (1, 2…) › Lô (1.1…) › Vị trí (1.1.1…).'),
], widths=[2.0, 4.0])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn dùng 3 quyền tên y hệ thống ERP, nhóm “Báo cáo kho” (dùng chung với Báo cáo tồn kho tổng hợp theo mặt hàng, Báo cáo tồn kho '
    'theo vị trí, Báo cáo tồn theo kho, Tổng hợp xuất nhập tồn). Có 1 trong 3 quyền là vào được màn và dùng MỌI chức năng; quyền cao '
    'nhất quyết định phạm vi kho. Hệ thống kiểm quyền ở máy chủ cho mọi lần lấy dữ liệu, in, xuất; mục menu không ẩn theo quyền.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('—', '(Không có quyền thao tác riêng)', 'Xem báo cáo, tìm kiếm và lọc, cài đặt bộ lọc, chọn hàng hóa, xem chi tiết, In, Xuất Excel: '
                                            'ai có 1 trong 3 quyền V1 / V2 / V3 đều dùng được.'),
], widths=[0.8, 1.9, 3.3])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', V1, 'Ô Tồn theo công ty chọn được mọi công ty đang hoạt động; ô Kho gồm mọi kho đang hoạt động của công ty đang chọn. Super '
               'admin được coi như có V1.'),
    ('V2', V2, 'Ô Tồn theo công ty chỉ có công ty của người dùng; ô Kho gồm các kho thuộc công ty đó.'),
    ('V3', V3, 'Ô Tồn theo công ty chỉ có công ty của người dùng; ô Kho chỉ gồm kho người dùng là thủ kho (thuộc công ty đó).'),
], widths=[0.8, 2.3, 2.9])
d.p('Có nhiều quyền: lấy quyền cao nhất theo thứ tự V1 > V2 > V3. Người không có V1 gửi công ty khác (gọi thẳng chức năng) vẫn bị khóa '
    'về công ty mình; kho ngoài phạm vi hoặc không thuộc công ty đang xem bị báo ' + M_KHO + '.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'V1', 'V2', 'V3', 'Không có quyền nào'], [
    ('FR-01 Xem báo cáo', '✅ mọi công ty', '✅ công ty mình', '✅ kho mình là thủ kho', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '❌'),
    ('FR-04 Chọn hàng hóa', '✅', '✅', '✅', '❌'),
    ('FR-05 Xem chi tiết theo công ty thuê kho – lô – vị trí', '✅', '✅', '✅', '❌'),
    ('FR-06 In báo cáo', '✅', '✅', '✅', '❌'),
    ('FR-07 Xuất Excel', '✅', '✅', '✅', '❌'),
], widths=[2.6, 0.9, 0.9, 0.9, 0.7])
d.p('Màn không có Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Import Excel, Lịch sử thay đổi, Duyệt nên ma trận không có các dòng đó.')
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có quyền nào trong 3 quyền: mục menu vẫn hiện; mở màn thì hệ thống báo ' + NOPERM + ', ô Tồn theo công ty và Kho rỗng, '
    'bảng hiện “Chọn công ty để xem báo cáo.”; In / Xuất Excel không thực hiện được (báo chữ đỏ dưới ô thiếu).',
    'Mở thẳng đường dẫn màn khi thiếu quyền: như trên, không lộ số liệu.',
    'Có quyền V3 nhưng không là thủ kho kho nào: ô Kho rỗng, bảng hiện ' + M_CHONKHO,
    'Bị gỡ quyền khi đang mở màn: lần lọc / in / xuất kế tiếp báo ' + NOPERM + ', bảng giữ số liệu cũ đang hiện.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút In danh sách, Xuất Excel', 'Luôn hiện ở đầu khối bộ lọc', 'Chưa đủ 3 ô bắt buộc → bấm thì báo đỏ dưới ô thiếu, không mở cửa sổ'),
    ('Nút Cài đặt bộ lọc, Ẩn / Tìm kiếm nâng cao', 'Luôn hiện', 'Khối nâng cao mở sẵn khi vào màn'),
    ('Ô Tồn theo công ty', 'Luôn hiện, bắt buộc', 'V2 / V3: chỉ 1 lựa chọn (công ty mình)'),
    ('Liên kết mã hợp đồng', 'Dòng lô có hợp đồng của phiếu nhập', 'Mở Hệ thống ERP ở tab mới'),
    ('Ô chọn ĐVT trên dòng mặt hàng', 'Hàng có từ 2 ĐVT', 'Hàng 1 ĐVT hiện chữ'),
], widths=[2.0, 2.0, 2.0])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A, [0, 1, 2])],
    [('FR-01', 'Xem báo cáo tồn kho chi tiết theo mặt hàng', 'view'),
     ('FR-06', 'In báo cáo', 'io'),
     ('FR-07', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Chọn hàng hóa', 'view', 'extend', [0], None),
     ('FR-05', 'Xem chi tiết công ty – lô – vị trí', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Báo cáo tồn kho chi tiết theo mặt hàng')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
k = fr(1, 'Xem báo cáo tồn kho chi tiết theo mặt hàng',
       rule=('- Màn Danh sách, Phân trang và Báo cáo.', 'list'),
       intro=dict(
           ten='Truy cập màn Báo cáo tồn kho chi tiết theo mặt hàng và xem báo cáo',
           mota='Mở màn và hiển thị tồn của từng mặt hàng tại kho đã chọn, tính đến hết ngày đã chọn: dòng tóm tắt (ngày, kho), khối '
                'tổng hợp (Mặt hàng còn tồn, Công ty thuê kho có tồn, số mặt hàng theo từng công ty thuê kho), bảng 4 cấp Hàng hóa › '
                'Công ty thuê kho › Lô › Vị trí kèm dòng TỔNG, phân trang theo mặt hàng. Màn chỉ đọc; phạm vi kho theo quyền.',
           tacnhan=TN, dieukien=DK,
           chinh='1. Người dùng vào menu theo đường dẫn ở mục Layout.\n'
                 '2. Hệ thống kiểm quyền, nạp danh mục bộ lọc theo phạm vi quyền (công ty, kho, công ty thuê của từng kho) và danh mục '
                 'hàng hóa (nhóm, tính chất, loại, thương hiệu, hãng sản xuất).\n'
                 '3. Có bộ lọc ghi tạm dưới 10 phút → khôi phục (kể cả hàng hóa đã chọn); không có → Tính đến ngày = hôm nay, Tồn theo '
                 'công ty = công ty của người dùng, Kho trống (công ty chỉ có 1 kho trong phạm vi thì chọn sẵn kho đó và tích sẵn mọi công '
                 'ty thuê kho của nó).\n'
                 '4. Đủ 3 ô bắt buộc → hệ thống tính tồn mọi mặt hàng của kho tới hết ngày, theo từng công ty thuê kho, giữ mặt hàng có '
                 'tổng khác 0, sắp theo tên hàng; dựng khối tổng hợp trên TOÀN tập; dựng chi tiết công ty – lô – vị trí cho 20 mặt hàng '
                 'của trang 1.\n'
                 '5. Hệ thống hiển thị dòng tóm tắt, khối tổng hợp, bảng bung sẵn tới cấp Lô, dòng “Hiển thị 1–20 / N mặt hàng”.',
           phu='• Chưa chọn kho → không tính, bảng hiện ' + M_CHONKHO + ' (tương tự “Chọn công ty để xem báo cáo.”, “Chọn ngày để xem '
               'báo cáo.”).\n'
               '• Không có mặt hàng nào còn tồn → khối tổng hợp hiện 0, bảng hiện ' + M_EMPTY + ', ẩn phân trang.\n'
               '• Không có quyền → báo ' + NOPERM + ', danh mục bộ lọc rỗng, bảng hiện “Chọn công ty để xem báo cáo.”.\n'
               '• Đổi bộ lọc khi đang có báo cáo → giữ số cũ làm mờ cho tới khi có số mới; lỗi tải thì giữ số cũ, báo lỗi.\n'
               '• Bấm Thu gọn → ẩn các ô của khối tổng hợp, còn dòng tóm tắt; bấm Mở rộng để hiện lại.\n'
               '• Bấm số trang / đổi Số dòng/trang → nạp lại đúng trang; dòng TỔNG và khối tổng hợp không đổi.\n'
               '• Phiên đăng nhập hết hạn → chuyển về màn đăng nhập.',
           dacbiet='Bảng cố định 8 cột: STT, Hàng hóa / Công ty / Lô / Vị trí, Mã hàng, Model, Thương hiệu, ĐVT, Hợp đồng, SL tồn — '
                   'không có cột ẩn, không có Tùy chỉnh cột, không sắp xếp theo cột (luôn theo tên hàng). Phân trang theo MẶT HÀNG '
                   '(mặc định 20; 10 / 20 / 50 / 100) để dòng con không bị cắt sang trang khác. Không cộng SL ở dòng TỔNG vì mỗi hàng '
                   'một ĐVT.'),
       layout=dict(menu=MENU, shot=shot('01_list'),
                   shot_caption='Màn Báo cáo tồn kho chi tiết theo mặt hàng — kho HP - Hải Phòng, tính đến 06/11/2026',
                   note='Lối vào duy nhất (phân hệ Kho, nhóm Báo cáo kho). Hiển thị: mặt hàng còn tồn tại 1 kho trong phạm vi quyền.',
                   extra=[(shot('00_menu'), 'Mục Báo cáo tồn kho chi tiết theo mặt hàng trong nhóm Báo cáo kho của phân hệ Kho'),
                          (shot('01b_empty'), 'Mở màn lần đầu: chưa chọn kho, bảng chờ chọn kho')]),
       ui_kw=dict(required=False),
       ui=[
           ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '“Báo cáo tồn kho chi tiết theo mặt hàng”',
            ['- Ở thanh trên cùng, cũng là tiêu đề tab trình duyệt',
             '- Icon ⓘ: “Tồn của từng mặt hàng tại một kho tính đến ngày đã chọn, chi tiết theo công ty thuê kho, lô và vị trí.”']),
           ('Dòng tóm tắt', 'Label', 'Read-only', '–', 'Theo dữ liệu',
            ['- “Tồn kho tính đến ngày dd/mm/yyyy · Kho: <mã> - <tên kho>”',
             '- Icon ⓘ: “' + TIP_GOAL + '”', '- Chỉ hiện khi đã có báo cáo']),
           ('Nút Thu gọn', 'Button', 'Enable', '–', 'Hiển thị',
            ['- Góc phải dòng tóm tắt', '- Bấm → ẩn các ô khối tổng hợp, chữ đổi thành “Mở rộng”', '- Không gọi lại dữ liệu']),
           ('Khối Mặt hàng', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Ô Mặt hàng còn tồn: “N mặt hàng” — luôn hiện', '- Ô Công ty thuê kho có tồn: “N công ty” — chỉ hiện khi > 0',
             '- Icon ⓘ: “' + TIP_MH + '”', '- Số KHÔNG bấm được (không mở cửa sổ)']),
           ('Khối Theo công ty thuê kho', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Mỗi công ty thuê kho có tồn 1 ô: mã công ty + “N mặt hàng”', '- Ẩn cả khối khi không công ty nào có tồn',
             '- Icon ⓘ: “' + TIP_CT + '”', '- Số không bấm được']),
           ('Bảng chi tiết báo cáo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- 8 cột, mỗi cột mô tả ở 1 dòng bên dưới', '- Tiêu đề cột dính khi cuộn; cuộn ngang khi màn hẹp hơn 1.240px']),
           ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Dòng TỔNG: “TỔNG”', '- Mặt hàng: số La Mã I, II… liên tục giữa các trang', '- Công ty: 1, 2…; Lô: 1.1…; Vị trí: 1.1.1…']),
           ('Cột Hàng hóa / Công ty / Lô / Vị trí', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Mặt hàng: tên hàng (dài cắt “…”, rê chuột xem đủ); Công ty: mã công ty thuê kho; Lô: mã lô; Vị trí: mã vị trí',
             '- Thụt lề theo cấp, có mũi tên bung / thu ở dòng có cấp con (mục 2.5)',
             '- Công ty không còn lô có tồn theo vị trí: kèm chữ xám “Không còn lô có tồn theo vị trí”',
             '- Tiêu đề cột có ô chọn cấp bung (mục 2.5)']),
           ('Cột Mã hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Chỉ ở dòng mặt hàng', '- Dài cắt “…”, rê chuột xem đủ']),
           ('Cột Model', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Model của hàng, chỉ ở dòng mặt hàng', '- Trống khi hàng chưa khai model']),
           ('Cột Thương hiệu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Chỉ ở dòng mặt hàng', '- Trống khi chưa khai']),
           ('Cột ĐVT', 'Dropdown', 'Enable', 'Danh sách ĐVT của hàng', 'ĐVT cơ sở',
            ['- Hàng có từ 2 ĐVT: ô chọn ngay trên dòng, dạng “<tên> (x<hệ số>)”; hàng 1 ĐVT: hiện chữ',
             '- Mặc định: ĐVT cơ sở', '- Icon ⓘ: “' + TIP_DVT + '”', '- Đổi ĐVT → mục 2.5']),
           ('Cột Hợp đồng', 'Link', 'Read-only', '–', 'Theo dữ liệu',
            ['- Chỉ ở dòng lô có hợp đồng của phiếu nhập; chữ xanh, kèm tên khách hàng nếu có', '- Rê chuột: hợp đồng, khách hàng, ngày '
             'đặt hàng, ngày trả hàng', '- Bấm mã → mở hợp đồng ở Hệ thống ERP, tab mới', '- Icon ⓘ: “' + TIP_HD + '”']),
           ('Cột SL tồn', 'Table/Grid', 'Read-only', '≥ 0, số nguyên', 'Theo dữ liệu',
            ['- Căn phải, phân cách hàng nghìn bằng dấu phẩy, làm tròn số nguyên sau khi quy đổi ĐVT',
             '- Mặt hàng: tổng các công ty; Công ty: tồn tới hết ngày; Lô: tổng vị trí; Vị trí: SL mới nhất',
             '- Icon ⓘ: “' + TIP_SL + '”']),
           ('Dòng TỔNG', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Nền cam, đầu bảng: “MẶT HÀNG CÒN TỒN · N mặt hàng” (toàn tập đã lọc, không theo trang)',
             '- Không cộng số lượng', '- Icon ⓘ: “' + TIP_TONG + '”']),
           ('Dòng “Hiển thị a–b / N mặt hàng”', 'Label', 'Read-only', '–', 'Theo dữ liệu',
            ['- a–b: thứ tự mặt hàng của trang đang xem', '- N: tổng mặt hàng còn tồn khớp bộ lọc']),
           ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', '20',
            ['- Mặc định: 20', '- Lựa chọn: 10, 20, 50, 100 (mặt hàng)', '- Đổi giá trị → về trang 1, nạp lại']),
           ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
            ['- Nút «, ‹, số trang, ›, »; ở trang đầu nút « ‹ mờ, trang cuối › » mờ', '- Ẩn khi không có mặt hàng',
             '- Giữ bộ lọc và cấp bung khi đổi trang']),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
            ['- Chưa chọn kho: ' + M_CHONKHO, '- Không có hàng: ' + M_EMPTY, '- Đang tải lần đầu: “Đang tải dữ liệu...”']),
           ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
            ['- Thiếu quyền: ' + NOPERM, '- Lỗi khác: câu máy chủ trả hoặc ' + M_LOADERR,
             '- Hết phiên đăng nhập: chuyển về màn đăng nhập']),
       ],
       ev=[('Mở màn hình', 'System',
            'Before:\n– Kiểm tra 1 trong 3 quyền xem báo cáo tồn kho; không có → hiển thị ' + NOPERM + ' và dừng xử lý.\n'
            '– Có bộ lọc ghi tạm dưới 10 phút → khôi phục; công ty / kho đã ghi không còn trong phạm vi → bỏ.\n'
            'During:\n– Nạp danh mục công ty, kho, công ty thuê kho theo phạm vi quyền; ngày mặc định hôm nay; công ty chỉ có 1 kho → chọn sẵn.\n'
            '– Thiếu ô bắt buộc → không tính, bảng chờ chọn.\n'
            'After:\n– Đủ ô bắt buộc → hiển thị khối tổng hợp, bảng trang 1 (20 mặt hàng) bung tới cấp Lô, dòng “Hiển thị 1–20 / N”.'),
           ('Bấm Thu gọn hoặc Mở rộng', 'Click',
            'Before:\n– Chỉ có khi đã có báo cáo.\nDuring:\n– Ẩn / hiện các ô khối tổng hợp, không gọi lại dữ liệu.\n'
            'After:\n– Chữ nút đổi “Thu gọn” ↔ “Mở rộng”.'),
           ('Bấm số trang hoặc nút tiến lùi', 'Click',
            'Before:\n– Giữ nguyên bộ lọc, cấp bung, ĐVT đã chọn.\n'
            'During:\n– Lấy lại báo cáo cho trang mới; trang vượt quá số trang → về trang cuối.\n'
            'After:\n– Hiển thị trang mới, STT La Mã tiếp tục, dòng “Hiển thị a–b / N” cập nhật; dòng TỔNG, khối tổng hợp không đổi.'),
           ('Đổi Số dòng/trang', 'Change',
            'Before:\n– Chọn 10, 20, 50 hoặc 100.\nDuring:\n– Ghi nhận số dòng mới (tối đa 100 mặt hàng / trang).\n'
            'After:\n– Về trang 1 và nạp lại.'),
           ('Bấm mã hợp đồng ở dòng lô', 'Click',
            'Before:\n– Dòng lô có hợp đồng bán của phiếu nhập.\nDuring:\n– Dựng đường dẫn xem hợp đồng ở Hệ thống ERP.\n'
            'After:\n– Mở tab mới; màn báo cáo giữ nguyên.'),
           ('Phiên đăng nhập hết hạn khi thao tác', 'System',
            'Before:\n– Áp cho mọi lần nạp báo cáo, in, xuất.\nDuring:\n– Máy chủ từ chối yêu cầu.\n'
            'After:\n– Chuyển về màn đăng nhập, không hiện dữ liệu.')])

d.p('2.1.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('Bảng dưới mô tả cách hệ thống tính từng chỉ tiêu, từng cột số liệu và nội dung icon ⓘ (nguyên văn trên giao diện). “Tập dữ liệu” '
    'là các mặt hàng có thay đổi tồn tại KHO đã chọn, ghi nhận cho các công ty thuê kho đang lọc (bỏ trống = mọi công ty thuê của kho), '
    'tới hết ngày Tính đến ngày, sau khi áp các ô lọc hàng hóa và hợp đồng, trong phạm vi quyền. Nguồn thay đổi tồn: mọi chứng từ kho '
    'đã ghi tồn (nhập kho, xuất kho, nhập lại, xuất điều chỉnh, điều chuyển kho, nhập / xuất điều chỉnh kiểm kê, tồn kho đầu kỳ — Phần 5).')
d.data_table([
    ('Dòng tóm tắt', 'Ngày = Tính đến ngày (dd/mm/yyyy); Kho = mã - tên kho đã chọn; ⓘ ghi giờ máy chủ tính số liệu.', TIP_GOAL),
    ('Ô Mặt hàng còn tồn', 'Đếm mặt hàng KHÁC NHAU của tập dữ liệu có tổng tồn các công ty thuê kho đang lọc ≠ 0. Tính trên toàn tập, '
                           'không theo trang. = N ở dòng “Hiển thị a–b / N” = số ở dòng TỔNG.', TIP_MH),
    ('Ô Công ty thuê kho có tồn', 'Đếm công ty thuê kho đang lọc có ít nhất 1 mặt hàng tồn > 0 (theo phần nguyên). Ẩn khi = 0.',
     '(dùng chung ⓘ của khối)'),
    ('Ô của từng công ty (khối Theo công ty thuê kho)', 'Số mặt hàng có tồn của RIÊNG công ty đó > 0. Một mặt hàng có tồn ở 2 công ty '
                                                         'được đếm ở cả 2 ô, nên tổng các ô có thể lớn hơn Ô Mặt hàng còn tồn.', TIP_CT),
    ('Dòng TỔNG', 'Số mặt hàng còn tồn (= Ô Mặt hàng còn tồn). Không cộng SL vì mỗi hàng một ĐVT.', TIP_TONG),
    ('Cột SL tồn — dòng công ty thuê kho', 'Tổng mọi thay đổi tồn (nhập +, xuất −) ghi cho công ty đó tại kho, từ đầu tới hết ngày '
                                           'Tính đến ngày. Dòng công ty chỉ hiện khi phần nguyên > 0 VÀ công ty có nhật ký lô tại kho. '
                                           '= Tồn cuối kỳ của Thẻ kho cùng hàng, kho, công ty thuê kho, đến cùng ngày.', TIP_SL),
    ('Cột SL tồn — dòng mặt hàng', 'Tổng SL tồn các dòng công ty được hiện bên dưới. = SL tồn của hàng ở Báo cáo tồn kho tổng hợp theo '
                                  'mặt hàng khi chọn đúng 1 kho đó, cùng công ty thuê kho và ngày.', '(dùng chung ⓘ của cột)'),
    ('Cột SL tồn — dòng lô', 'Tổng SL các vị trí của lô bên dưới.', '(dùng chung ⓘ của cột)'),
    ('Cột SL tồn — dòng vị trí', 'Số lượng MỚI NHẤT ghi nhận tại vị trí của lô (KHÔNG cắt theo Tính đến ngày — giữ y ERP); chỉ vị trí còn '
                                 '> 0; lô không còn vị trí nào bị bỏ. Ngày quá khứ: tổng lô có thể khác SL công ty.',
     '(dùng chung ⓘ của cột)'),
    ('Quy đổi ĐVT', 'Mọi số của hàng (kể cả công ty, lô, vị trí) = số theo ĐVT cơ sở ÷ hệ số ĐVT đang chọn, làm tròn 2 số lẻ rồi hiển thị '
                    'SỐ NGUYÊN (vd 13 Cái → Thùng x12 = 1,08 → “1”); số 0 hiện “0”. Bản in / Excel luôn theo ĐVT cơ sở.', TIP_DVT),
    ('Cột Hợp đồng', 'Hợp đồng bán gắn với phiếu nhập kho tạo ra lô; khách hàng lấy từ thông tin đơn của hợp đồng (nếu có).', TIP_HD),
    ('Thứ tự dòng', 'Mặt hàng theo tên hàng (A→Z), trùng tên theo thứ tự tạo hàng; công ty theo thứ tự công ty thuê kho; lô theo thứ tự '
                    'ghi nhận.', '—'),
    ('Ràng buộc khớp số', 'Tồn đầu kỳ + Nhập − Xuất = Tồn cuối kỳ của Thẻ kho = SL tồn dòng công ty (cùng hàng / kho / công ty / ngày); '
                          'dòng mặt hàng = tổng dòng công ty; Ô Mặt hàng còn tồn = dòng TỔNG = N.', '—'),
])
k += 1
d.p('2.1.%d Danh sách popup mở từ số liệu' % k)
d.popup_table([
    ('Số ở khối tổng hợp, dòng TỔNG, cột SL tồn (mọi cấp)', 'Không có popup — số không bấm được',
     'Báo cáo đã chi tiết tới vị trí ngay trong bảng; xem từng chứng từ của 1 hàng dùng Thẻ kho',
     'Con số đọc trực tiếp trên bảng (mục 2.1.6)'),
    ('Mũi tên bung / thu và ô chọn cấp bung', 'Không phải popup — bung / thu dòng con ngay trong bảng (mục 2.5)',
     'Xem công ty thuê kho, lô, vị trí của hàng mà không rời bảng', 'Dòng con của mặt hàng đang xem'),
    ('Mã hợp đồng ở cột Hợp đồng (dòng lô)', 'Không phải popup — mở hợp đồng ở Hệ thống ERP, tab mới',
     'Lô thuộc hợp đồng bán nào, của khách nào', 'Màn hợp đồng của Hệ thống ERP'),
    ('Ô Hàng hóa trong bộ lọc', 'Chọn hàng hóa (mục 2.4)', 'Thu hẹp báo cáo về đúng 1 mặt hàng',
     'Danh sách hàng hóa theo công ty đang xem; chọn 1 hàng thì báo cáo còn tối đa 1 mặt hàng'),
])

# ------------------------------------------------------------ 2.2
k = fr(2, 'Tìm kiếm và lọc',
       rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
       intro=dict(ten='Tìm kiếm và lọc báo cáo tồn kho chi tiết theo mặt hàng',
                  mota='Chọn ngày chốt số, công ty, kho (3 ô bắt buộc) và thu hẹp tập mặt hàng theo công ty thuê kho, nhóm, tính chất, '
                       'loại, thương hiệu, hãng sản xuất, 1 hàng hóa cụ thể hoặc mã hợp đồng. Màn không có ô tìm nhanh; các ô chọn áp '
                       'ngay khi đổi, ô Hợp đồng áp khi Enter / Tìm kiếm.',
                  tacnhan=TN, dieukien=DK,
                  chinh='1. Người dùng chọn Tính đến ngày, Tồn theo công ty, Kho.\n'
                        '2. Hệ thống tự tích mọi công ty thuê của kho vừa chọn vào ô Công ty thuê kho.\n'
                        '3. Người dùng chọn thêm các ô lọc hàng hóa (chọn nhiều) hoặc chọn 1 hàng qua cửa sổ Chọn hàng hóa (mục 2.4).\n'
                        '4. Mỗi lần đổi ô chọn, hệ thống gom các thay đổi trong 0,3 giây thành 1 lần tính, về trang 1, nạp lại báo cáo, '
                        'ghi tạm bộ lọc trên trình duyệt (10 phút).\n'
                        '5. Người dùng gõ mã hợp đồng rồi Enter hoặc bấm Tìm kiếm → hệ thống nạp lại theo hợp đồng.',
                  phu='• Bấm Tìm kiếm / In danh sách / Xuất Excel khi thiếu ô bắt buộc → chữ đỏ dưới ô thiếu (' + M_NGAY + ', ' + M_KHO +
                      '), khối lọc tự mở, không nạp.\n'
                      '• Đổi Tồn theo công ty → bỏ kho đã chọn (kho của công ty cũ), bảng chờ chọn kho.\n'
                      '• Đổi Kho → tích lại toàn bộ công ty thuê của kho mới.\n'
                      '• Bỏ trống Công ty thuê kho → tính mọi công ty thuê của kho.\n'
                      '• Bấm Xóa lọc → về công ty mặc định + hôm nay, bỏ mọi ô khác (kể cả kho, hàng hóa), xóa bộ lọc ghi tạm.\n'
                      '• Không có kết quả → ' + M_EMPTY + '\n'
                      '• Rời sang màn khác → xóa bộ lọc ghi tạm; F5 / tab mới trong 10 phút → khôi phục.',
                  dacbiet='Kiểu khớp: Hợp đồng khớp MỘT PHẦN mã hợp đồng (chứa chuỗi gõ), không giới hạn số ký tự; các ô chọn khớp '
                          'CHÍNH XÁC giá trị; Loại hàng hóa khớp khi hàng thuộc ít nhất 1 loại đã chọn. Kết hợp nhiều ô = thỏa đồng '
                          'thời (VÀ); trong 1 ô chọn nhiều = HOẶC.'),
       layout=dict(menu=MENU + ' => Ẩn tìm kiếm nâng cao', shot=shot('02_filter'),
                   shot_caption='Khối Bộ lọc báo cáo tồn kho (mở sẵn khi vào màn)',
                   extra=[(shot('01c_required'), 'Bấm Tìm kiếm khi chưa chọn Kho: chữ đỏ “Vui lòng chọn kho”'),
                          (shot('02b_kho_opts'), 'Ô Kho chỉ liệt kê kho của công ty đang chọn trong phạm vi quyền')]),
       ui=[('Tiêu đề khối', 'Label', 'Hiển thị', '–', '–', '“Bộ lọc báo cáo tồn kho”', ['- Kèm biểu tượng phễu', '- Icon ⓘ: “' + TIP_PURPOSE + '”']),
           ('Tính đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Hôm nay',
            ['- Mặc định: hôm nay', '- Thiếu → ' + M_NGAY, '- Đổi → nạp lại']),
           ('Tồn theo công ty', 'Dropdown', 'Enable', 'Danh sách theo quyền', 'Có', 'Công ty của người dùng',
            ['- Mặc định: công ty của người dùng', '- V1: mọi công ty đang hoạt động; V2 / V3: chỉ công ty mình', '- Không có nút × bỏ chọn',
             '- Đổi → bỏ kho đã chọn']),
           ('Kho', 'Dropdown', 'Enable', 'Danh sách theo quyền', 'Có', 'Trống',
            ['- Mặc định: trống (công ty chỉ có 1 kho → chọn sẵn)', '- Lựa chọn “<mã> - <tên>” kho thuộc công ty đang chọn', '- Thiếu → ' + M_KHO,
             '- Đổi → tích sẵn mọi công ty thuê của kho']),
           ('Công ty thuê kho', 'Dropdown', 'Enable', 'Công ty thuê của kho', 'Không', 'Mọi công ty thuê của kho',
            ['- Chọn nhiều, hiện mã công ty', '- Icon ⓘ: “' + TIP_THUE + '”', '- Bỏ trống = mọi công ty thuê của kho']),
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
            ['- Về công ty mặc định + hôm nay, bỏ kho và mọi ô khác', '- Xóa bộ lọc ghi tạm, tắt chữ đỏ', '- Bảng chờ chọn kho']),
           ('Nút Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
            ['- Thu gọn / mở khối ô lọc', '- Khi thu gọn nhãn là “Tìm kiếm nâng cao”', '- Mặc định mở']),
           ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
           ('Chữ lỗi dưới ô bắt buộc', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
            ['- ' + M_NGAY, '- ' + M_KHO, '- ' + M_CTY + ' (máy chủ trả khi công ty không hợp lệ)', '- Chỉ hiện sau lần bấm Tìm kiếm / In / '
             'Xuất đầu tiên']),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + M_EMPTY, '- ' + M_CHONKHO])],
       ev=[('Đổi một ô chọn', 'Change',
            'Before:\n– Áp cho Tính đến ngày, công ty, kho, công ty thuê, 5 ô danh mục, Hàng hóa.\n'
            '– Đổi công ty → bỏ kho; đổi kho → tích mọi công ty thuê của kho.\n'
            'During:\n– Ghi tạm bộ lọc; gom các thay đổi trong 0,3 giây; thiếu ô bắt buộc → không gọi máy chủ, bảng chờ chọn.\n'
            '– Máy chủ kiểm ngày đúng định dạng, công ty trong danh mục được xem, kho thuộc phạm vi quyền và thuộc công ty; sai → báo lỗi '
            'tại ô.\n' + ERR + '\n'
            'After:\n– Về trang 1, hiển thị báo cáo mới; lỗi thì giữ báo cáo cũ.'),
           ('Gõ ô Hợp đồng rồi Enter hoặc bấm Tìm kiếm', 'Click',
            'Before:\n– Gõ chữ chưa nạp lại; đủ 3 ô bắt buộc mới tính.\n'
            'During:\n– Giữ mặt hàng có thay đổi tồn từ lô nhập / lô xuất thuộc phiếu gắn hợp đồng có mã chứa chuỗi gõ; dòng lô chỉ còn '
            'lô nhập của hợp đồng đó.\n' + ERR + '\n'
            'After:\n– Về trang 1, nạp lại, ghi tạm bộ lọc.'),
           ('Bấm Tìm kiếm khi thiếu ô bắt buộc', 'Click',
            'Before:\n– Bật chế độ hiện lỗi.\nDuring:\n– Ô thiếu viền đỏ, chữ ' + M_NGAY + ' / ' + M_KHO + '; mở khối lọc.\n'
            'After:\n– Không nạp, không ghi tạm.'),
           ('Bấm Xóa lọc', 'Click',
            'Before:\n– Không hỏi xác nhận.\n'
            'During:\n– Đặt lại bộ lọc: công ty mặc định, hôm nay, các ô khác trống; xóa bộ lọc ghi tạm; tắt chữ đỏ.\n'
            'After:\n– Bảng hiện ' + M_CHONKHO + ' (trừ khi công ty chỉ có 1 kho).'),
           ('Bấm Ẩn / Tìm kiếm nâng cao', 'Click',
            'Before:\n– Khối đang mở / thu gọn.\nDuring:\n– Đổi trạng thái khối.\nAfter:\n– Giá trị đã chọn vẫn áp dụng; trạng thái ghi tạm cùng bộ lọc.'),
           ('Rời màn hoặc tải lại trang', 'System',
            'Before:\n– Bộ lọc ghi tạm 10 phút trên trình duyệt.\n'
            'During:\n– Chuyển sang màn khác → xóa bộ lọc ghi tạm; F5 / tab mới trong 10 phút → khôi phục.\n'
            'After:\n– Vào lại bằng menu sau khi rời màn → bộ lọc mặc định.')])
d.p('2.2.%d Cách lấy dữ liệu của ô lọc' % k)
d.p('Bảng dưới giải thích cách hệ thống áp từng ô lọc lên tập dữ liệu (mục 2.1.6).')
d.data_table([
    ('Tính đến ngày', 'Lấy thay đổi tồn ghi nhận trước 00:00 của ngày hôm sau (tức tới hết ngày đã chọn). Không ảnh hưởng SL lô / vị trí '
                      '(luôn số mới nhất).', '—'),
    ('Tồn theo công ty', 'Chỉ quyết định danh sách kho chọn được và letterhead; không lọc theo công ty ghi nhận tồn.', '—'),
    ('Kho', 'Đúng 1 kho; phải thuộc phạm vi quyền và thuộc công ty đang chọn.', '—'),
    ('Công ty thuê kho', 'Chỉ cộng thay đổi tồn ghi cho các công ty đã tích (trong số công ty thuê của kho); bỏ trống = mọi công ty thuê '
                         'của kho; kho không có công ty thuê nào → rỗng.', TIP_THUE),
    ('Nhóm / Tính chất / Thương hiệu / Hãng sản xuất', 'Hàng có thuộc tính tương ứng bằng 1 trong các giá trị đã chọn.', '—'),
    ('Loại hàng hóa', 'Hàng có danh sách loại chứa ít nhất 1 loại đã chọn.', '—'),
    ('Hàng hóa', 'Đúng 1 mặt hàng đã chọn (gồm cả hàng đã ngừng kinh doanh).', '—'),
    ('Hợp đồng', 'Chỉ cộng thay đổi tồn của lô nhập / lô xuất thuộc phiếu nhập / phiếu xuất gắn hợp đồng bán có mã chứa chuỗi gõ; dòng lô '
                 'chỉ còn lô nhập của hợp đồng đó (có thể không còn dòng con).', TIP_HDONG),
])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị',
              mota='Cho phép mỗi người dùng tự chọn các ô lọc muốn thấy ở khối Bộ lọc báo cáo tồn kho và sắp xếp lại thứ tự. Cấu hình '
                   'lưu theo người dùng cho riêng màn này (11 ô: Tính đến ngày, Tồn theo công ty, Kho, Công ty thuê kho, Nhóm hàng hóa, '
                   'Tính chất hàng hóa, Loại hàng hóa, Thương hiệu, Hãng sản xuất, Hàng hóa, Hợp đồng).',
              tacnhan=TN, dieukien=DK,
              chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
                    '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 11 ô kèm ô tích, theo cấu hình đang lưu.\n'
                    '3. Người dùng tích / bỏ tích và kéo thả để đổi thứ tự.\n'
                    '4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình cho người dùng, hiển thị “Cập nhật thành công” và áp ngay lên khối lọc.',
              phu='• Bấm Khôi phục mặc định → tích lại đủ 11 ô theo thứ tự gốc; phải bấm Lưu mới có hiệu lực.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không lưu thay đổi.\n'
                  '• Lưu thất bại → hiển thị thông báo lỗi.\n'
                  '• Lưu ý: ẩn 3 ô bắt buộc (Tính đến ngày, Tồn theo công ty, Kho) vẫn giữ giá trị đang có; nên giữ hiện 3 ô này.',
              dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('07_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Cài đặt bộ lọc”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách ô lọc', 'Table/Grid', 'Enable', '11 ô', 'Không', 'Theo cấu hình đã lưu',
        ['- Tính đến ngày, Tồn theo công ty, Kho, Công ty thuê kho, Nhóm hàng hóa, Tính chất hàng hóa, Loại hàng hóa, Thương hiệu, Hãng '
         'sản xuất, Hàng hóa, Hợp đồng', '- Mỗi mục đánh số thứ tự']),
       ('Ô tích của ô lọc', 'Checkbox', 'Enable', '–', 'Không', 'Theo cấu hình đã lưu', ['- Tích: ô hiện ở khối lọc', '- Bỏ tích: ẩn']),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo để đổi thứ tự ô lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình cho người dùng hiện tại, đóng cửa sổ, áp ngay.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích lại đủ 11 ô, thứ tự gốc; chưa lưu.'),
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
                       'còn hàng đó.',
                  tacnhan=TN, dieukien=DK + '\n4. Đã chọn Tồn theo công ty (cửa sổ tra hàng theo công ty đang xem).',
                  chinh='1. Người dùng bấm ô Hàng hóa.\n'
                        '2. Hệ thống mở cửa sổ “Chọn hàng hóa”: dòng công ty đang xem, cây catalog (số hàng mỗi nhánh), ô tìm theo mã, '
                        'tên, model, barcode, mã đặt hàng, công tắc Còn tồn / Gồm hàng ngoài catalog, bảng hàng hóa.\n'
                        '3. Người dùng tìm / lọc rồi bấm vào tên hàng.\n'
                        '4. Hệ thống đóng cửa sổ, ô Hàng hóa hiện “<mã> - <tên>”, ghi tạm bộ lọc, về trang 1 và nạp lại báo cáo (1 lần).',
                  phu='• Bấm Đóng / (x) → đóng, giữ hàng đã chọn trước đó.\n'
                      '• Bấm dấu × trên ô Hàng hóa → bỏ chọn, báo cáo nạp lại mọi hàng (không mở cửa sổ).\n'
                      '• Hàng đã chọn không có tồn tại kho → bảng ' + M_EMPTY + '\n'
                      '• Danh sách không tải được → cửa sổ báo “Không tải được danh sách hàng hoá”, nút Thử lại.\n'
                      '• F5 trong 10 phút → ô Hàng hóa vẫn hiện tên hàng đã chọn.',
                  dacbiet='Chỉ chọn được 1 hàng (giữ y ERP); cửa sổ có nút Phóng to toàn màn hình.'),
       layout=dict(menu=MENU + ' => Hàng hóa', shot=shot('04b_picker_tpe'), shot_caption='Cửa sổ Chọn hàng hóa',
                   note='Modal Chọn hàng hóa được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'),
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
           ('Thông báo lỗi tải', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- “Không tải được danh sách hàng hoá”', '- Nút Thử lại'])],
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
    'Trả lời câu hỏi: tồn của RIÊNG một mặt hàng (tìm theo mã / tên / model / barcode) tại kho này đang ở công ty thuê nào, lô nào, vị '
    'trí nào — khi kho có hàng nghìn mặt hàng.',
    'Là cửa sổ nổi để giữ nguyên ngữ cảnh báo cáo (ngày, kho, các ô lọc khác); cây catalog + tìm kiếm cần chỗ rộng nên không nhét vào '
    'ô chọn thả xuống.',
    'Ràng buộc khớp số: sau khi chọn, báo cáo còn tối đa 1 mặt hàng, SL tồn = SL của hàng đó khi không lọc hàng; Tồn bán được trong cửa '
    'sổ là số của công ty, KHÔNG phải tồn tại kho đang xem.',
    'Người dùng làm tiếp: xem chi tiết lô / vị trí (mục 2.5), In / Xuất Excel đúng 1 hàng; mỗi lần mở là cửa sổ mới.',
])
k += 1
d.p('2.4.%d Các biến thể theo con số bấm' % k)
d.popup_variant_table([
    ('Ô Hàng hóa khi chưa chọn hàng', 'Mọi hàng hóa của công ty đang xem (kể cả chưa kinh doanh)', '“Chọn hàng hóa”',
     'Không ẩn ô nào; chỉ chọn 1 hàng'),
    ('Ô Hàng hóa khi đã có hàng', 'Như trên; hàng cũ được thay khi chọn hàng mới', '“Chọn hàng hóa”', 'Không ẩn ô nào'),
])

# ------------------------------------------------------------ 2.5
k = fr(5, 'Xem chi tiết theo công ty thuê kho – lô – vị trí',
       rule=('- Màn Xem chi tiết và Báo cáo dạng cây.', 'detail'),
       intro=dict(ten='Xem chi tiết tồn của mặt hàng theo công ty thuê kho, lô, vị trí và đổi ĐVT',
                  mota='Ngay trong bảng báo cáo: bung / thu từng dòng bằng mũi tên, chọn cấp bung sẵn cho cả trang (Chỉ hàng hóa / Đến '
                       'công ty thuê kho / Đến lô / Tất cả cấp), đổi ĐVT riêng từng mặt hàng để xem số quy đổi, mở hợp đồng của lô. Chỉ '
                       'đổi cách hiển thị, không tính lại số.',
                  tacnhan=TN, dieukien=DK + '\n4. Báo cáo đã có ít nhất 1 mặt hàng.',
                  chinh='1. Người dùng chọn cấp ở ô chọn cấp trong tiêu đề cột Hàng hóa / Công ty / Lô / Vị trí (mặc định “Đến lô”).\n'
                        '2. Hệ thống bung sẵn mọi dòng của trang tới cấp đã chọn.\n'
                        '3. Người dùng bấm mũi tên ở một dòng để bung / thu riêng dòng đó.\n'
                        '4. Người dùng đổi ĐVT ở dòng mặt hàng có nhiều ĐVT → mọi số của hàng đó (công ty, lô, vị trí) quy đổi theo hệ '
                        'số, làm tròn số nguyên.\n'
                        '5. Người dùng bấm mã hợp đồng ở dòng lô → mở hợp đồng ở Hệ thống ERP, tab mới.',
                  phu='• Đổi trang / đổi bộ lọc → bảng bung lại theo cấp đang chọn (bung / thu riêng lẻ bị bỏ).\n'
                      '• Công ty không còn lô có tồn theo vị trí → dòng công ty không có mũi tên, kèm chữ “Không còn lô có tồn theo vị trí”.\n'
                      '• Hàng 1 ĐVT → không có ô chọn ĐVT.\n'
                      '• Số quy đổi < 0,5 → hiện “0”.\n'
                      '• Lô không có hợp đồng → cột Hợp đồng trống.',
                  dacbiet='Chọn cấp, bung / thu, đổi ĐVT không gọi lại máy chủ. ĐVT chọn giữ khi đổi trang (theo từng hàng) nhưng không '
                          'ghi tạm khi F5. Bản in / Excel luôn theo ĐVT cơ sở.'),
       layout=dict(menu=MENU + ' => Chọn cấp muốn bung', shot=shot('03_detail'),
                   shot_caption='Lọc 1 hàng, chọn cấp “Tất cả cấp (đến vị trí)”: công ty TPHP › 4 lô › vị trí KHOANG1',
                   note='Thao tác ngay trên bảng của màn báo cáo theo đường dẫn ở trên.',
                   extra=[(shot('03b_level'), 'Ô chọn cấp bung: 4 lựa chọn'),
                          (shot('03c_unit'), 'Ô chọn ĐVT trên dòng mặt hàng có 2 ĐVT (Can 1L / Thùng 24C-1L x24)')]),
       ui=[('Ô chọn cấp bung', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', 'Đến lô',
            ['- Mặc định: Đến lô', '- Chỉ hàng hóa', '- Đến công ty thuê kho', '- Đến lô', '- Tất cả cấp (đến vị trí)',
             '- Rê chuột: “Chọn cấp muốn bung sẵn trong bảng”']),
           ('Mũi tên bung / thu dòng mặt hàng', 'Icon Button', 'Enable', '–', '–', 'Theo cấp',
            ['- Chỉ có khi hàng có công ty thuê kho', '- Rê chuột: “Hiện / Ẩn công ty thuê kho”']),
           ('Mũi tên bung / thu dòng công ty', 'Icon Button', 'Enable', '–', '–', 'Theo cấp',
            ['- Chỉ có khi công ty còn lô', '- Rê chuột: “Hiện / Ẩn lô”']),
           ('Mũi tên bung / thu dòng lô', 'Icon Button', 'Enable', '–', '–', 'Theo cấp', '- Rê chuột: “Hiện / Ẩn vị trí”'),
           ('Dòng công ty thuê kho', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
            ['- STT 1, 2…; mã công ty; SL tồn của công ty', '- “Không còn lô có tồn theo vị trí” khi không có lô']),
           ('Dòng lô', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
            ['- STT 1.1…; mã lô (rê chuột xem đủ); Hợp đồng; SL = tổng vị trí']),
           ('Dòng vị trí', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', ['- STT 1.1.1…; mã vị trí chữ xám; SL mới nhất']),
           ('Ô chọn ĐVT', 'Dropdown', 'Enable', 'ĐVT của hàng', 'Không', 'ĐVT cơ sở',
            ['- Mặc định: ĐVT cơ sở', '- Lựa chọn “<tên> (x<hệ số>)”', '- Đổi → quy đổi mọi số của hàng']),
           ('Liên kết mã hợp đồng', 'Link', 'Enable', '–', '–', 'Theo dữ liệu',
            ['- Bấm → mở hợp đồng ở Hệ thống ERP, tab mới', '- Rê chuột: hợp đồng, khách hàng, ngày đặt, ngày trả']),
           ('Cột SL tồn sau quy đổi', 'Table/Grid', 'Read-only', 'Số nguyên', '–', 'Theo dữ liệu',
            ['- = số theo ĐVT cơ sở ÷ hệ số, làm tròn', '- Vd 24 Can 1L → Thùng x24 = 1'])],
       ev=[('Chọn cấp bung', 'Change',
            'Before:\n– Giá trị mới khác giá trị đang chọn.\nDuring:\n– Bung mọi dòng của trang có độ sâu nhỏ hơn cấp đã chọn.\n'
            'After:\n– Bảng hiển thị lại; không gọi máy chủ.'),
           ('Bấm mũi tên một dòng', 'Click',
            'Before:\n– Dòng có cấp con.\nDuring:\n– Đảo trạng thái bung / thu riêng dòng đó.\nAfter:\n– Hiện / ẩn dòng con; các dòng khác giữ nguyên.'),
           ('Đổi ĐVT dòng mặt hàng', 'Change',
            'Before:\n– Hàng có từ 2 ĐVT; bỏ qua giá trị rỗng / trùng.\nDuring:\n– Lấy hệ số ĐVT, chia mọi số của hàng, làm tròn số nguyên.\n'
            'After:\n– Dòng mặt hàng, công ty, lô, vị trí của hàng đó hiển thị số mới.'),
           ('Bấm mã hợp đồng', 'Click',
            'Before:\n– Lô có hợp đồng bán; có địa chỉ Hệ thống ERP.\nDuring:\n– Dựng đường dẫn xem hợp đồng.\n'
            'After:\n– Mở tab mới; thiếu địa chỉ ERP → hiện chữ trơn.'),
           ('Đổi trang hoặc bộ lọc', 'System',
            'Before:\n– Có dữ liệu mới.\nDuring:\n– Áp lại cấp bung đang chọn.\nAfter:\n– Bung / thu riêng lẻ trước đó bị bỏ; ĐVT đã chọn giữ theo hàng.')])
d.p('2.5.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('“Tập dữ liệu” là các mặt hàng của trang đang xem (mục 2.1.6). Chi tiết lô / vị trí lấy từ nhật ký tồn theo vị trí của kho.')
d.data_table([
    ('Dòng công ty thuê kho', 'Công ty thuê kho đang lọc có tồn (phần nguyên) > 0 và có nhật ký lô tại kho; SL = tồn tới hết Tính đến ngày.',
     '(dùng chung ⓘ cột SL tồn)'),
    ('Dòng lô', 'Lô có vị trí ghi nhận trước ngày chọn của công ty đang lọc; giữ lô còn ít nhất 1 vị trí > 0; SL = tổng vị trí.',
     '(dùng chung ⓘ cột SL tồn)'),
    ('Dòng vị trí', 'SL = dòng nhật ký MỚI NHẤT của vị trí trong lô (không cắt theo ngày); chỉ vị trí > 0.', '(dùng chung ⓘ cột SL tồn)'),
    ('Hợp đồng', 'Hợp đồng bán của phiếu nhập kho tạo ra lô; khách hàng từ thông tin đơn của hợp đồng.', TIP_HD),
    ('ĐVT', 'Danh sách ĐVT của hàng, ĐVT cơ sở (hệ số nhỏ nhất) đứng đầu.', TIP_DVT),
])

# ------------------------------------------------------------ 2.6
fr(6, 'In báo cáo', usecase=('FR-06', 'In báo cáo', 'io', A),
   rule=('- Quy tắc In và Báo cáo.', 'list'),
   intro=dict(ten='In báo cáo tồn kho chi tiết theo mặt hàng (xem trước rồi in)',
              mota='Chọn kiểu in Đầy đủ (có khối Chi tiết: Công ty, Lô, Vị trí, SL, Cộng) hoặc Ngắn gọn (chỉ thông tin mặt hàng và SL tồn), '
                   'chọn cột in, xem trước bản in khổ ngang gồm letterhead công ty đang xem, tiêu đề, Tính đến ngày, Kho, bảng TOÀN BỘ '
                   'mặt hàng theo bộ lọc đang hiển thị (không riêng trang đang xem), khối ký Trưởng kho / Người lập báo cáo; bấm In.',
              tacnhan=TN, dieukien=DK + '\n4. Đã có báo cáo (đủ 3 ô bắt buộc).',
              chinh='1. Người dùng bấm In danh sách.\n'
                    '2. Hệ thống mở cửa sổ “In báo cáo”: kiểu Đầy đủ được chọn, tích sẵn mọi cột của kiểu.\n'
                    '3. Người dùng chọn kiểu, tích / bỏ tích cột, bấm In.\n'
                    '4. Hệ thống kiểm quyền, lấy toàn bộ mặt hàng theo bộ lọc của báo cáo đang hiển thị, theo ĐVT cơ sở; đếm số dòng in '
                    '(kiểu Đầy đủ: mỗi vị trí 1 dòng).\n'
                    '5. Hệ thống mở cửa sổ “Xem trước báo cáo tồn kho chi tiết theo mặt hàng”; người dùng bấm In → hộp thoại in của trình '
                    'duyệt.',
              phu='• Chưa đủ ô bắt buộc → không mở cửa sổ, chữ đỏ dưới ô thiếu.\n'
                  '• Bỏ tích hết cột → ' + M_NOCOL + ', cửa sổ không đóng.\n'
                  '• Vượt 2.000 dòng in → bản xem trước không có nội dung, hiện ' + M_LIMIT + ', ẩn nút In.\n'
                  '• Báo cáo rỗng → bản in chỉ có tiêu đề và hàng tên cột.\n'
                  '• Bấm Hủy / (x) → đóng, không in. Lỗi → “Không tải được dữ liệu in” hoặc câu máy chủ trả.',
              dacbiet='STT luôn được in; số theo ĐVT cơ sở, số 0 để trống. Letterhead theo công ty ĐANG XEM (ô Tồn theo công ty). Kiểu Đầy '
                      'đủ gộp ô theo Hàng › Công ty › Lô, mã lô kèm “Hợp đồng: …” trong ô Lô.'),
   layout=dict(menu=MENU + ' => In danh sách', shot=shot('05_print'), shot_caption='Cửa sổ In báo cáo (kiểu Đầy đủ, chọn cột in)',
               note='Modal In báo cáo và Xem trước được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.',
               extra=[(shot('05b_preview'), 'Xem trước bản in kiểu Đầy đủ — kho HP - Hải Phòng'),
                      (shot('05c_print_err'), 'Bỏ tích hết cột rồi bấm In: “Vui lòng chọn ít nhất 1 cột để in”')]),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“In báo cáo”', 'Kèm nút (x) đóng.'),
       ('Kiểu in', 'Radio', 'Enable', '2 giá trị', 'Có', 'Đầy đủ',
        ['- Mặc định: Đầy đủ', '- Đầy đủ: “Có khối Chi tiết: Công ty, Lô, Vị trí, SL, Cộng.”', '- Ngắn gọn: “Chỉ thông tin mặt hàng và SL tồn.”',
         '- Đổi kiểu → danh sách cột đổi theo']),
       ('Tiêu đề Chọn cột in', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- Icon ⓘ: “Cột STT luôn được in. Số lượng theo ĐVT cơ sở của từng hàng.”'),
       ('Ô Chọn tất cả', 'Checkbox', 'Enable', '–', 'Không', 'Tích', ['- Tích / bỏ tích mọi cột', '- Bán chọn khi tích 1 phần']),
       ('Danh sách cột', 'Checkbox', 'Enable', '11 hoặc 6 cột', 'Ít nhất 1', 'Tích hết',
        ['- Đầy đủ: Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn, Công ty, Lô, Vị trí, SL, Cộng',
         '- Ngắn gọn: 6 cột đầu']),
       ('Chữ lỗi chọn cột', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + M_NOCOL),
       ('Nút In (cửa sổ In báo cáo)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Kiểm ≥ 1 cột rồi mở xem trước.'),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không in.'),
       ('Cửa sổ Xem trước', 'Popup', 'Read-only', '–', '–', 'Ẩn',
        ['- Tiêu đề “Xem trước báo cáo tồn kho chi tiết theo mặt hàng”', '- Khổ ngang: letterhead, “BÁO CÁO TỒN KHO CHI TIẾT THEO MẶT '
         'HÀNG”, Tính đến ngày, Kho, bảng, khối ký Trưởng kho / Người lập báo cáo']),
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
        'During:\n– Lấy toàn bộ mặt hàng theo bộ lọc của báo cáo đang hiển thị, theo ĐVT cơ sở; cột lạ bị bỏ (rỗng = đủ cột).\n'
        '– Đếm dòng in; > 2.000 → không dựng nội dung, báo vượt trần.\n' + ERR + '\n'
        'After:\n– Mở cửa sổ Xem trước khổ ngang, letterhead công ty đang xem.'),
       ('Bấm In (cửa sổ Xem trước)', 'Click',
        'Before:\n– Bản xem trước đã tải xong.\nDuring:\n– In qua khung ẩn, giữ đúng mẫu.\nAfter:\n– Hộp thoại in của trình duyệt mở.'),
       ('Bấm Hủy hoặc (x)', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không in.\nAfter:\n– Đóng cửa sổ; báo cáo giữ nguyên.')])

# ------------------------------------------------------------ 2.7
fr(7, 'Xuất Excel', usecase=('FR-07', 'Xuất Excel', 'io', A),
   rule=('- Quy tắc Excel.', 'excel'),
   intro=dict(ten='Xuất báo cáo tồn kho chi tiết theo mặt hàng ra Excel',
              mota='Chọn kiểu Đầy đủ hoặc Ngắn gọn rồi tải file Excel gồm TOÀN BỘ mặt hàng theo bộ lọc của báo cáo đang hiển thị (không '
                   'riêng trang đang xem), đủ cột của kiểu đã chọn (Excel không có bước chọn cột), theo ĐVT cơ sở.',
              tacnhan=TN, dieukien=DK + '\n4. Đã có báo cáo (đủ 3 ô bắt buộc).',
              chinh='1. Người dùng bấm Xuất Excel ở đầu khối bộ lọc.\n'
                    '2. Hệ thống mở cửa sổ “Xuất Excel báo cáo tồn kho chi tiết theo mặt hàng”, kiểu Đầy đủ được chọn.\n'
                    '3. Người dùng chọn kiểu, bấm Xuất Excel trong cửa sổ.\n'
                    '4. Hệ thống khóa nút (chữ “Đang xuất…”, vòng xoay), kiểm quyền, lấy toàn bộ mặt hàng, dựng file.\n'
                    '5. Trình duyệt tải file “' + FILE + '”; cửa sổ đóng.',
              phu='• Chưa đủ ô bắt buộc → không mở cửa sổ, chữ đỏ dưới ô thiếu.\n'
                  '• Bấm Hủy / (x) → đóng, không xuất.\n'
                  '• Lỗi → ' + M_XLS_ERR + ' (thiếu quyền: báo không có quyền), giữ cửa sổ để bấm lại.\n'
                  '• Báo cáo rỗng → vẫn tải file, chỉ có tiêu đề và hàng tên cột.',
              dacbiet='Luôn tải thẳng, không gửi mail (ERP gửi mail khi ≥ 150 mặt hàng). Cấu trúc file: dòng 1 letterhead công ty đang xem '
                      '(rộng bằng bảng); tiêu đề “BÁO CÁO TỒN KHO CHI TIẾT THEO MẶT HÀNG”; “Tính đến ngày: dd/mm/yyyy”; “Kho: <mã> - '
                      '<tên>”; bảng (Đầy đủ: 2 tầng tiêu đề, nhóm “Chi tiết”, gộp ô); khối ký Trưởng kho / Người lập báo cáo kèm ngày. '
                      'Số lượng là ô số có dấu phân cách hàng nghìn (cộng được), số 0 để trống. Kho lớn có thể mất vài chục giây.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('06_export'), shot_caption='Cửa sổ Xuất Excel — chọn kiểu xuất',
               note='Modal Xuất Excel được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Xuất Excel báo cáo tồn kho chi tiết theo mặt hàng”', 'Kèm biểu tượng Excel, nút (x).'),
       ('Nhãn Kiểu xuất', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Kiểu xuất”'),
       ('Kiểu xuất', 'Radio', 'Enable', '2 giá trị', 'Có', 'Đầy đủ',
        ['- Mặc định: Đầy đủ (mỗi lần mở về Đầy đủ)', '- Đầy đủ: “Có khối Chi tiết: Công ty, Lô, Vị trí, SL, Cộng.”',
         '- Ngắn gọn: “Chỉ thông tin mặt hàng và SL tồn.”']),
       ('Nút Xuất Excel (cửa sổ)', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → tải file', '- Khóa khi đang xuất, chữ “Đang xuất…”']),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Hủy.'),
       ('Nút Xuất Excel (đầu khối lọc)', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Nền xanh lá nhạt', '- Khi đang xuất: chữ “Đang xuất…”, vòng xoay, khóa']),
       ('File tải về', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Tên “' + FILE + '”', '- Đầy đủ: STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn, Chi tiết (Công ty, Lô, Vị trí, SL, Cộng)',
         '- Ngắn gọn: STT + 6 cột mặt hàng']),
       ('Thanh tải trang', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- Chạy trên đầu trang trong lúc xuất'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + M_XLS_ERR, '- Thiếu quyền: báo không có quyền'])],
   ev=[('Bấm Xuất Excel (đầu khối lọc)', 'Click',
        'Before:\n– Chưa có báo cáo → chữ đỏ dưới ô thiếu, dừng.\nDuring:\n– Mở cửa sổ, kiểu Đầy đủ.\nAfter:\n– Chờ chọn kiểu.'),
       ('Chọn kiểu xuất', 'Change',
        'Before:\n– Đầy đủ / Ngắn gọn.\nDuring:\n– Ghi nhận kiểu.\nAfter:\n– Chưa xuất cho tới khi bấm Xuất Excel.'),
       ('Bấm Xuất Excel (cửa sổ)', 'Click',
        'Before:\n– Kiểm tra quyền xem báo cáo tồn kho; không có → báo không có quyền và dừng.\n– Chặn bấm lặp khi đang xuất.\n'
        'During:\n– Lấy toàn bộ mặt hàng theo bộ lọc của báo cáo đang hiển thị, theo ĐVT cơ sở; dựng file theo kiểu.\n' + ERR + '\n'
        'After:\n– Tải “' + FILE + '”, đóng cửa sổ, mở khóa nút. Lỗi → ' + M_XLS_ERR + ', giữ cửa sổ.'),
       ('Bấm Hủy, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không xuất.\nAfter:\n– Đóng cửa sổ; lần mở sau về Đầy đủ.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Báo cáo tồn kho chi tiết theo mặt hàng; không lặp lại các quy tắc đã có '
           'trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Ô bắt buộc và mặc định', [
        '– Bắt buộc Tính đến ngày, Tồn theo công ty, Kho (1 kho); thiếu thì không tính, báo chữ đỏ khi bấm Tìm kiếm / In / Xuất.',
        '– Mặc định: hôm nay, công ty của người dùng; công ty chỉ có 1 kho trong phạm vi → chọn sẵn kho.',
        '– Đổi công ty bỏ kho; đổi kho tích mọi công ty thuê của kho.'],
     ['Tìm kiếm và lọc', 'In báo cáo', 'Xuất Excel']),
    ('BR-02', 'SL tồn của công ty thuê kho', [
        '– = tổng thay đổi tồn (nhập +, xuất −) ghi cho công ty tại kho tới hết Tính đến ngày, từ mọi chứng từ kho (Phần 5).',
        '– Công ty chỉ hiện khi phần nguyên > 0 và có nhật ký lô tại kho.',
        '– Khớp Tồn cuối kỳ của Thẻ kho cùng hàng / kho / công ty / ngày (Tồn đầu kỳ + Nhập − Xuất).'],
     ['Xem báo cáo', 'In báo cáo', 'Xuất Excel']),
    ('BR-03', 'Mặt hàng lên báo cáo', [
        '– Mặt hàng có tổng tồn các công ty thuê kho đang lọc ≠ 0; SL tồn = tổng các công ty được hiện.',
        '– Sắp theo tên hàng; phân trang theo mặt hàng (mặc định 20, tối đa 100).',
        '– Khối tổng hợp, dòng TỔNG tính trên toàn tập, không theo trang.'],
     ['Xem báo cáo']),
    ('BR-04', 'SL lô / vị trí giữ y ERP', [
        '– SL vị trí = số mới nhất tại vị trí, KHÔNG cắt theo ngày; chỉ vị trí > 0; lô không còn vị trí bị bỏ.',
        '– Chọn ngày quá khứ: tổng lô có thể khác SL công ty (người dùng chốt 22/10/2026).'],
     ['Xem chi tiết', 'In báo cáo', 'Xuất Excel']),
    ('BR-05', 'Phạm vi theo quyền', [
        '– Có 1 trong 3 quyền xem báo cáo tồn kho mới vào được; quyền cao nhất thắng.',
        '– Tổng công ty: mọi công ty / kho; công ty: kho của công ty mình; kho: kho mình là thủ kho.',
        '– Máy chủ khóa công ty với người không có quyền tổng công ty; kho ngoài phạm vi báo “Vui lòng chọn kho”.'],
     ['Mọi chức năng']),
    ('BR-06', 'Quy đổi ĐVT', [
        '– Số trên màn = số ĐVT cơ sở ÷ hệ số ĐVT chọn riêng từng hàng, làm tròn 2 số lẻ rồi hiện số nguyên.',
        '– In / Excel luôn theo ĐVT cơ sở.'],
     ['Xem chi tiết', 'In báo cáo', 'Xuất Excel']),
    ('BR-07', 'Lọc hợp đồng', [
        '– Giữ thay đổi tồn của lô nhập / lô xuất thuộc phiếu gắn hợp đồng bán có mã chứa chuỗi gõ (khớp một phần).',
        '– Lô hiện ra chỉ là lô nhập của hợp đồng đó; hợp đồng mở ở Hệ thống ERP.'],
     ['Tìm kiếm và lọc']),
    ('BR-08', 'Chuẩn hóa dữ liệu lọc', [
        '– Ngày nhận dd/mm/yyyy; sai định dạng → “Vui lòng chọn ngày”.',
        '– Ô chọn khớp chính xác; nhiều giá trị trong 1 ô = HOẶC; nhiều ô = VÀ; Hợp đồng bỏ khoảng trắng đầu / cuối.',
        '– Công ty thuê ngoài danh sách của kho bị bỏ qua.'],
     ['Tìm kiếm và lọc']),
    ('BR-09', 'Ghi nhớ bộ lọc', [
        '– Bộ lọc (kể cả hàng đã chọn) ghi tạm 10 phút trên trình duyệt; F5 / tab mới khôi phục.',
        '– Rời sang màn khác hoặc bấm Xóa lọc → xóa. Cấu hình ô lọc (Cài đặt bộ lọc) lưu theo người dùng.'],
     ['Tìm kiếm và lọc', 'Cài đặt bộ lọc']),
    ('BR-10', 'In và xuất', [
        '– Theo bộ lọc của báo cáo đang hiển thị, toàn bộ mặt hàng; letterhead theo công ty đang xem.',
        '– In tối đa 2.000 dòng (Đầy đủ: mỗi vị trí 1 dòng); vượt thì không in, báo thu hẹp bộ lọc.',
        '– Excel không giới hạn, tải thẳng, tên “' + FILE + '”.'],
     ['In báo cáo', 'Xuất Excel']),
    ('BR-11', 'Tính duy nhất và cấp cha – con', [
        '– Mỗi mặt hàng 1 dòng; mỗi công ty thuê kho tối đa 1 dòng dưới mặt hàng; lô, vị trí không lặp.',
        '– Mặt hàng › công ty thuê kho › lô › vị trí; dòng cha = tổng dòng con trực tiếp (trừ BR-04).'],
     ['Xem báo cáo', 'Xem chi tiết']),
    ('BR-12', 'Chỉ đọc, không ghi lịch sử', [
        '– Màn không tạo / sửa / xóa dữ liệu, không có lịch sử thay đổi; số liệu đổi theo chứng từ kho ở Phần 5.'],
     ['Mọi chức năng']),
    ('BR-13', 'Khác hệ thống ERP (có chủ đích)', [
        '– Hiện hợp đồng của lô (ERP không bao giờ hiện); có In xem trước (ERP ẩn nút In); Excel không gửi mail.',
        '– Kho không có công ty thuê nào → rỗng (ERP lỗi); giao diện dạng cây bung / thu thay bảng gộp ô.'],
     ['Xem báo cáo', 'In báo cáo', 'Xuất Excel']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Báo cáo tồn kho chi tiết theo mặt hàng chỉ đọc, không ghi dữ liệu. Các màn hình dưới đây ghi các thay đổi tồn mà báo cáo cộng '
    '(nhập +, xuất −, theo công ty thuê kho, lô, vị trí) hoặc dùng chung nguồn / quyền với báo cáo.')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', 'Khai báo tồn kho đầu kỳ (tồn đầu kỳ theo lô / vị trí — cộng vào SL tồn)', 'Kho -> Tồn kho đầu kỳ'),
    ('2', 'Kho', 'Phiếu nhập kho (tạo lô + vị trí, cộng tồn; hợp đồng của phiếu là cột Hợp đồng và điều kiện ô lọc Hợp đồng)',
     'Kho -> Nhập kho'),
    ('3', 'Kho', 'Phiếu nhập kho điều chỉnh kiểm kê (cộng tồn phần thừa sau kiểm kê)', 'Kho -> Nhập kho'),
    ('4', 'Tài chính', 'Phiếu xuất kho (trừ tồn theo lô / vị trí; hợp đồng của phiếu xuất dùng cho ô lọc Hợp đồng)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('5', 'Tài chính', 'Phiếu nhập lại (cộng lại tồn hàng đã xuất)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('6', 'Kho', 'Phiếu xuất điều chỉnh sai số liệu (trừ tồn)', 'Kho -> Xuất kho'),
    ('7', 'Kho', 'Phiếu xuất kho điều chỉnh kiểm kê (trừ tồn phần thiếu sau kiểm kê)', 'Kho -> Xuất kho'),
    ('8', 'Kho', 'Điều chuyển kho (trừ tồn kho đi, cộng tồn kho đến)', 'Kho -> Điều chuyển'),
    ('9', 'Kho', 'Phiếu điều chuyển vị trí (đổi SL vị trí của lô, tổng tồn kho không đổi)', 'Kho -> Điều chuyển'),
    ('10', 'Hệ thống ERP', 'Phiếu nhập lại điều chỉnh sai số liệu (cộng tồn — chưa chuyển sang HRM)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
    ('11', 'Hệ thống ERP', 'Hợp đồng bán (mở từ mã hợp đồng ở dòng lô)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
    ('12', 'Kho', 'Thẻ kho (cùng nguồn tồn: Tồn cuối kỳ của 1 hàng / kho / công ty thuê = SL tồn dòng công ty; dùng để đối soát từng '
                  'chứng từ)', 'Kho -> Báo cáo kho'),
    ('13', 'Kho', 'Báo cáo tồn kho tổng hợp theo mặt hàng (cùng 3 quyền, cùng cách cộng tồn; chọn 1 kho thì SL tồn khớp dòng mặt hàng)',
     'Kho -> Báo cáo kho'),
    ('14', 'Kho', 'Báo cáo tồn kho theo vị trí, Báo cáo tồn theo kho, Tổng hợp xuất nhập tồn (cùng 3 quyền và phạm vi kho)',
     'Kho -> Báo cáo kho'),
    ('15', 'Kho', 'Kho vật lý, Kho kế toán (danh sách kho, công ty thuê kho của ô lọc), Vị trí (mã vị trí)', 'Kho -> Danh mục'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()

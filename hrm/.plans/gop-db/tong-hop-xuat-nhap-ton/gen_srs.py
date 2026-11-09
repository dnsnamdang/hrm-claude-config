# -*- coding: utf-8 -*-
"""SRS màn "Tổng hợp xuất nhập tồn" (phân hệ Kho › Báo cáo kho) — form chuẩn + quy định màn BÁO CÁO (bảng Cách lấy dữ liệu, bảng
popup, Mục đích thiết kế popup) + chuẩn 04/11 (Mục lục trang riêng căn giữa, Phần 5 bảng 4 cột).

Chạy: python gen_srs.py  → SRS - Tổng hợp xuất nhập tồn.docx
Khuôn chép: ../bao-cao-ton-kho-tong-hop-mat-hang/gen_srs.py (07/11) + ../the-kho/gen_srs.py (06/11) — cùng 3 quyền / cùng nguồn
  nhật ký tồn vị trí với Thẻ kho.
Nguồn đọc 09/11/2026 (nhánh develop — con của gop_db — cả 2 repo):
  FE  pages/warehouse/change-summary-report/{index.vue, components/ChangeSummarySummary.vue, components/ChangeSummaryTable.vue},
      pages/finance/position-inventories/components/ScopePicker.vue, pages/warehouse/stock-card/components/{ExportModeModal.vue, format.js},
      components/report/V2BaseReportPrintModal.vue, components/print/ReportPrintPreviewModal.vue, V2ProductPickerModal, V2BasePickerField,
      V2BaseSmartFilterPanel, utils/filterRequiredErrors.js, utils/mixins/filterStateMixin.js, components/subsystem-menu/{warehouse,finance}.js.
  BE  Modules/Finance/{Services/ChangeSummaryReportService.php, Services/WarehouseStockReportService.php,
      Services/ChangeSummaryReportPrintService.php, Http/Controllers/V1/ChangeSummaryReportController.php,
      Exports/ChangeSummaryReportExport.php, Resources/views/{exports/change_summary_report, prints/change-summary-report}.blade.php,
      Routes/api.php (nhóm change-summary-report, chỉ GET)}.
  Tài liệu: plan.md, spec docs/superpowers/specs/gop-db/2026-10-24-tong-hop-xuat-nhap-ton-design.md (design.md còn placeholder).
Ảnh: ./thxnt_shots — dev-hrm 09/11/2026, DNS Admin (_capture/capture.js, chặn mọi yêu cầu ghi: 0 lọt). Bộ lọc mẫu công ty CN Hải Phòng,
  toàn bộ 4 kho, Năm nay, nạp qua bộ nhớ trình duyệt như F5. Popup Chọn hàng hóa chụp với công ty TPE (CN Hải Phòng dev báo 403).
Đối soát số dev 09/11 (_capture/doisoat.js + probe_scope.js, chỉ GET): ENEO-700-V5231 kho HP / TPHP 01/01–09/11/2026 = 70 + 496 − 546 = 20
  = Thẻ kho = Báo cáo tồn kho tổng hợp / chi tiết theo mặt hàng (20); 4 kho CN HP = 70 + 523 − 546 = 47 (HP 20 + CB 27); Năm trước
  0 + 265 − 195 = 70 = tồn đầu 2026. ENEO-640-V5236 kho PTT Năm nay = 15,141 + 11,404 − 23,348 = 3,197 = Thẻ kho; Không nhặt phiếu
  điều chuyển 15,141 + 7,435 − 19,379 = 3,197 = Thẻ kho cùng loại. CN HP Năm nay: 217 mặt hàng có phát sinh, 96 còn tồn cuối kỳ =
  96 dòng Báo cáo tồn kho tổng hợp theo mặt hàng, khớp từng hàng.
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

TEN = 'Tổng hợp xuất nhập tồn'
SHOTS = os.path.join(HERE, 'thxnt_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Kho => Báo cáo kho => Tổng hợp xuất nhập tồn'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Tổng hợp xuất nhập tồn.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
V1 = 'Xem báo cáo tồn kho theo tổng công ty'
V2 = 'Xem báo cáo tồn kho theo công ty'
V3 = 'Xem báo cáo tồn kho theo kho'
NOPERM = '“Bạn không có quyền truy cập chức năng này.”'
M_LOADERR = '“Lỗi khi tải dữ liệu.”'
M_KHO = '“Vui lòng chọn kho”'
M_CTY = '“Vui lòng chọn tồn theo công ty”'
M_TG = '“Vui lòng chọn đủ từ ngày và đến ngày”'
M_NGUOC = '“Ngày kết thúc phải sau hoặc bằng ngày bắt đầu”'
M_EMPTY = '“Không có mặt hàng nào khớp bộ lọc.”'
M_CHONKHO = '“Chọn kho để xem báo cáo.”'
M_CHONCTY = '“Chọn công ty để xem báo cáo.”'
M_CHONNGAY = '“Chọn đủ từ ngày và đến ngày để xem báo cáo.”'
M_XLS_ERR = '“Lỗi khi xuất Excel.”'
M_NOCOL = '“Vui lòng chọn ít nhất 1 cột để in”'
M_NOPRINT = '“Không có dữ liệu để in”'
M_LIMIT = ('“Danh sách có N dòng, vượt mức in tối đa 2.000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng '
           'thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.”')
FILE = 'bao_cao_tong_hop_xuat_nhap_ton_kho.xlsx'

A = 'Thủ kho / Kế toán kho'
TN = ('Người dùng có quyền thực hiện chức năng: có ít nhất 1 trong 3 quyền “%s”, “%s”, “%s” (hoặc là Super admin); phạm vi kho theo '
      'quyền cao nhất (Phần 2).' % (V1, V2, V3))
DK = ('1. Người dùng đăng nhập thành công.\n'
      '2. Người dùng có 1 trong 3 quyền xem báo cáo tồn kho (hoặc là Super admin).\n'
      '3. Có ít nhất 1 kho đang hoạt động trong phạm vi quyền thuộc công ty đang xem.')
TIP_PURPOSE = ('MỤC ĐÍCH BÁO CÁO • Xem tồn đầu kỳ, nhập, xuất trong kỳ và tồn cuối kỳ của từng mặt hàng trên 1 hoặc nhiều kho • Thu '
               'hẹp theo Nhà / Dãy / Khoang / Vị trí, công ty thuê kho • Lọc thêm theo nhóm, tính chất, loại, thương hiệu, hãng sản xuất, '
               'hàng hóa')
TIP_TITLE = 'Tồn đầu kỳ, nhập, xuất trong kỳ và tồn cuối kỳ của từng mặt hàng trên các kho đã chọn.'
TIP_GOAL = ('TỔNG HỢP XUẤT NHẬP TỒN • Tồn đầu kỳ, nhập, xuất trong kỳ và tồn cuối kỳ của từng mặt hàng trên các kho / vị trí đang chọn '
            '• Số liệu tính tại <ngày giờ>')
TIP_MH = ('MẶT HÀNG • Mặt hàng có phát sinh: có tồn đầu kỳ, nhập hoặc xuất trong kỳ khác 0 • Kho đang xem: số kho đang chọn ở bộ lọc')
TIP_PS = 'PHÁT SINH • Số mặt hàng có số lượng khác 0 ở từng cột của bảng'
TIP_TONG = ('TỔNG • Số mặt hàng có tồn đầu kỳ, nhập hoặc xuất trong kỳ khác 0 • Không cộng số lượng vì mỗi mặt hàng một đơn vị tính')
TIP_DVT = 'ĐƠN VỊ • Chọn ĐVT riêng từng mặt hàng — số lượng của hàng đó quy đổi theo hệ số, In / Xuất Excel theo ĐVT đã chọn'
TIP_DAU = 'TỒN ĐẦU KỲ • Tồn tại các vị trí đang xét, trước ngày đầu kỳ'
TIP_NHAP = ('NHẬP TRONG KỲ • Cộng các lần tăng tồn tại vị trí trong kỳ (kể cả điều chuyển vào, trừ khi chọn “Không nhặt phiếu điều '
            'chuyển”)')
TIP_XUAT = ('XUẤT TRONG KỲ • Cộng các lần giảm tồn tại vị trí trong kỳ (kể cả điều chuyển ra, trừ khi chọn “Không nhặt phiếu điều '
            'chuyển”)')
TIP_CUOI = 'TỒN CUỐI KỲ • Tồn đầu kỳ + Nhập trong kỳ − Xuất trong kỳ'
TIP_KY = 'Tồn đầu kỳ tính tới trước ngày đầu kỳ; nhập / xuất cộng trong kỳ.'
TIP_THUE = 'Chọn kho trước. Bỏ trống = mọi công ty thuê của các kho'

d = SrsDoc(out=OUT, menu=MENU, route='/warehouse/change-summary-report', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Kho': 'menu_phanhe', 'Báo cáo kho': 'menu_nhom', 'Tổng hợp xuất nhập tồn': 'menu_muc',
    'Ẩn tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Hàng hóa': 'o_hanghoa',
    'Đơn vị': 'o_dvt', 'In danh sách': 'btn_inds', 'Xuất Excel': 'btn_xuatexcel', 'Nhà / Dãy / Khoang / Vị trí': 'o_nha',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Tổng hợp xuất nhập tồn thuộc phân hệ Kho, nhóm Báo cáo kho (chuyển từ hệ thống ERP: '
    'Kho › Báo cáo kho › Tổng hợp xuất nhập tồn), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu báo cáo cho biết, với TỪNG mặt hàng trên MỘT HOẶC NHIỀU kho (hoặc một phần kho: Nhà / Dãy / Khoang / Vị trí) '
    'của một công ty, trong một kỳ: Tồn đầu kỳ, Nhập trong kỳ, Xuất trong kỳ và Tồn cuối kỳ.',
    'Ghi rõ cách tính từng con số (khối tổng hợp, dòng TỔNG, 4 cột số lượng) để người nghiệm thu đối soát được với Thẻ kho (cùng hàng, '
    'kho, công ty thuê, kỳ) và với Báo cáo tồn kho tổng hợp / chi tiết theo mặt hàng (tồn cuối kỳ).',
    'Ghi rõ các điểm GIỮ Y HỆT hệ thống ERP (cách lọc Nhà / Dãy / Khoang / Vị trí — kể cả 2 hiện tượng lạ, Loại báo cáo “Không nhặt '
    'phiếu điều chuyển”, ĐVT chọn riêng từng hàng) và các điểm khác ERP có chủ đích (ô Kỳ, In xem trước, Excel tải thẳng, kiểm quyền ở '
    'mọi lần lấy dữ liệu).',
])
d.p('Phạm vi chức năng (8 chức năng, đặc tả ở Phần 3):')
d.bullets([
    'Xem báo cáo (khối tổng hợp + bảng phẳng mỗi mặt hàng 1 dòng, phân trang theo mặt hàng); Tìm kiếm và lọc (Kỳ, Loại báo cáo, 6 ô hàng '
    'hóa, Tồn theo công ty, ô tích “Xem toàn bộ kho”, Kho, Công ty thuê kho); Lọc theo Nhà / Dãy / Khoang / Vị trí; Cài đặt bộ lọc; Chọn '
    'hàng hóa (cửa sổ chọn 1 hàng); Đổi đơn vị tính từng hàng; In báo cáo (2 kiểu, chọn cột, xem trước); Xuất Excel (2 kiểu).',
    'Không thuộc màn này: màn CHỈ ĐỌC — không có Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Duyệt / Không duyệt, Import Excel, Lịch sử '
    'thay đổi, không có Tùy chỉnh cột (bảng cố định 10 cột; chọn cột chỉ có ở bản in), không có ô tìm nhanh, không có ô Hợp đồng và không '
    'có số bấm mở cửa sổ chi tiết hay mở Thẻ kho. Số liệu sinh ra từ các chứng từ kho ở Phần 5.',
    'Mục “Tổng hợp xuất nhập tồn” trong menu Tài chính (nhóm báo cáo hàng tồn kho của kế toán) là báo cáo KHÁC (có giá trị tiền), hiện chưa '
    'có liên kết — KHÔNG phải lối vào của màn này.',
])
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Thủ kho / kế toán kho xem trong một kỳ mỗi mặt hàng đầu kỳ còn bao nhiêu, nhập thêm bao nhiêu, xuất đi bao nhiêu và cuối kỳ còn bao '
    'nhiêu trên các kho (vị trí) đang phụ trách; dùng để chốt sổ tháng / năm, rà hàng tồn lâu không xuất.',
    'Đối soát với Thẻ kho (từng chứng từ của 1 hàng): 4 số của dòng hàng = 4 số khối tổng hợp của Thẻ kho cùng kho / công ty thuê / kỳ / '
    'Loại báo cáo; Tồn cuối kỳ = SL tồn của Báo cáo tồn kho tổng hợp / chi tiết theo mặt hàng tại ngày cuối kỳ.',
    'Bản in / file Excel dùng để ký xác nhận (Trưởng kho, Người lập báo cáo) hoặc gửi đối chiếu.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Bắt buộc Tồn theo công ty và ít nhất 1 Kho; Kỳ mặc định Năm nay; chọn Tuỳ chọn thì bắt buộc đủ Từ ngày – Đến ngày. Mặc định chọn '
    'TOÀN BỘ kho của công ty nên vào màn là có số ngay (BR-01).',
    'Tồn đầu kỳ = tổng thay đổi tồn TRƯỚC ngày đầu kỳ; Nhập / Xuất = tổng thay đổi tăng / giảm trong kỳ (tới hết ngày cuối kỳ); Tồn cuối kỳ '
    '= Tồn đầu kỳ + Nhập − Xuất. Chỉ hiện mặt hàng có ít nhất 1 trong 3 số Tồn đầu / Nhập / Xuất khác 0 (BR-02, BR-03).',
    'Số tính theo nhật ký tồn TẠI VỊ TRÍ: chuyển hàng giữa 2 vị trí (phiếu điều chuyển vị trí) được tính cả Nhập lẫn Xuất, trừ khi chọn '
    'Loại báo cáo “Không nhặt phiếu điều chuyển” (BR-04).',
    'Lọc Nhà / Dãy / Khoang / Vị trí giữ y hệ thống ERP: chỉ thu hẹp khi có tick ít nhất 1 Vị trí; khi đó kho không tick gì bị bỏ (BR-05).',
    'Phạm vi kho theo 1 trong 3 quyền xem báo cáo tồn kho; không có quyền nào thì không xem được. Màn không ghi dữ liệu nào (BR-06, BR-12).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Kỳ', 'Khoảng thời gian báo cáo: Tuần này (thứ Hai → Chủ nhật), Tháng này, Năm nay (mặc định, 01/01 → 31/12), Năm trước, Tuỳ chọn '
           '(tự chọn Từ ngày – Đến ngày).'),
    ('Tồn đầu kỳ', 'Số lượng còn tại các vị trí đang xét ngay TRƯỚC 00:00 ngày đầu kỳ.'),
    ('Nhập / Xuất trong kỳ', 'Tổng các lần tăng / giảm tồn tại vị trí từ 00:00 ngày đầu kỳ tới hết 23:59 ngày cuối kỳ. Xuất hiển thị số '
                             'dương.'),
    ('Tồn cuối kỳ', 'Tồn đầu kỳ + Nhập trong kỳ − Xuất trong kỳ.'),
    ('Loại báo cáo', '“Tất cả” (mặc định) hoặc “Không nhặt phiếu điều chuyển” — bỏ các lần chuyển hàng giữa 2 vị trí khỏi số liệu.'),
    ('Tồn theo công ty', 'Công ty đang xem; quyết định danh sách kho chọn được và letterhead bản in / Excel.'),
    ('Kho / Xem toàn bộ kho', 'Kho vật lý đang hoạt động của công ty trong phạm vi quyền, chọn được nhiều kho (ô hiện MÃ kho). Ô tích Xem '
                              'toàn bộ kho: tích = chọn hết kho, bỏ tích = xóa kho để tự chọn.'),
    ('Công ty thuê kho', 'Công ty có kho kế toán gắn với kho đã chọn; mỗi thay đổi tồn ghi nhận cho 1 công ty. Bỏ trống = mọi công ty.'),
    ('Nhà / Dãy / Khoang / Vị trí', 'Cấp chia nhỏ của kho; vị trí là nơi hàng nằm thật. “Vị trí tự do” là vị trí không thuộc khoang nào.'),
    ('ĐVT cơ sở / hệ số', 'Đơn vị nhỏ nhất của hàng (hệ số 1); ĐVT khác có hệ số quy đổi (vd Thùng 24C-1L = 24 Can 1L).'),
    ('Kiểu Đầy đủ / Ngắn gọn', 'Kiểu in / xuất Excel: Đầy đủ có Model và Thương hiệu; Ngắn gọn chỉ tên, mã, đơn vị và 4 cột số lượng.'),
    ('Trạng thái bản ghi', 'Dòng báo cáo không có trạng thái (không Khóa / Hoạt động).'),
    ('Cấu trúc phân cấp', 'Không phân cấp: bảng phẳng, mỗi mặt hàng 1 dòng (cộng mọi kho / vị trí đang xét).'),
], widths=[2.0, 4.0])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn dùng 3 quyền tên y hệ thống ERP, nhóm “Báo cáo kho” (dùng chung với Báo cáo tồn kho chi tiết / tổng hợp theo mặt hàng, Báo '
    'cáo tồn kho theo vị trí, Báo cáo tồn theo kho). Có 1 trong 3 quyền là vào được màn và dùng MỌI chức năng; quyền cao nhất quyết định '
    'phạm vi công ty / kho. Hệ thống kiểm quyền ở máy chủ cho mọi lần lấy danh mục, lấy cây vị trí, lấy số liệu, in, xuất; mục menu không '
    'ẩn theo quyền.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('—', '(Không có quyền thao tác riêng)', 'Xem báo cáo, tìm kiếm và lọc, lọc vị trí, cài đặt bộ lọc, chọn hàng hóa, đổi ĐVT, In, Xuất '
                                            'Excel: ai có 1 trong 3 quyền V1 / V2 / V3 đều dùng được, các cột hiển thị như nhau.'),
], widths=[0.8, 1.9, 3.3])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', V1, 'Ô Tồn theo công ty chọn được mọi công ty đang hoạt động; ô Kho gồm mọi kho đang hoạt động của công ty đang chọn. Super '
               'admin được coi như có V1.'),
    ('V2', V2, 'Ô Tồn theo công ty chỉ có công ty của người dùng; ô Kho gồm các kho thuộc công ty đó.'),
    ('V3', V3, 'Ô Tồn theo công ty chỉ có công ty của người dùng; ô Kho chỉ gồm kho người dùng là thủ kho (thuộc công ty đó).'),
], widths=[0.8, 2.3, 2.9])
d.p('Có nhiều quyền: lấy quyền cao nhất theo thứ tự V1 > V2 > V3. Người không có V1 gửi công ty khác vẫn bị khóa về công ty mình; kho '
    'ngoài phạm vi hoặc không thuộc công ty đang xem bị bỏ, không còn kho nào thì báo ' + M_KHO + '.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'V1', 'V2', 'V3', 'Không có quyền nào'], [
    ('FR-01 Xem báo cáo', '✅ mọi công ty', '✅ công ty mình', '✅ kho mình là thủ kho', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '❌'),
    ('FR-03 Lọc theo Nhà / Dãy / Khoang / Vị trí', '✅', '✅', '✅ kho mình', '❌'),
    ('FR-04 Cài đặt bộ lọc', '✅', '✅', '✅', '❌'),
    ('FR-05 Chọn hàng hóa', '✅', '✅', '✅', '❌'),
    ('FR-06 Đổi đơn vị tính', '✅', '✅', '✅', '❌'),
    ('FR-07 In báo cáo', '✅', '✅', '✅', '❌'),
    ('FR-08 Xuất Excel', '✅', '✅', '✅', '❌'),
], widths=[2.6, 0.9, 0.9, 0.9, 0.7])
d.p('Màn không có Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Import Excel, Lịch sử thay đổi, Duyệt nên ma trận không có các dòng đó.')
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có quyền nào trong 3 quyền: mục menu vẫn hiện; mở màn thì hệ thống báo ' + NOPERM + ', ô Tồn theo công ty và Kho rỗng, bảng '
    'hiện ' + M_CHONCTY + '; In / Xuất Excel không thực hiện được (báo chữ đỏ dưới ô thiếu).',
    'Mở thẳng đường dẫn màn khi thiếu quyền: như trên, không lộ số liệu.',
    'Có quyền V3 nhưng không là thủ kho kho nào: ô Kho rỗng, ô Xem toàn bộ kho bị khóa, bảng hiện ' + M_CHONKHO,
    'Bị gỡ quyền khi đang mở màn: lần lọc / in / xuất kế tiếp báo ' + NOPERM + ', bảng giữ số liệu cũ đang hiện.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút In danh sách, Xuất Excel', 'Luôn hiện ở đầu khối bộ lọc', 'Chưa có báo cáo → bấm thì báo đỏ dưới ô thiếu, không mở cửa sổ'),
    ('Nút Cài đặt bộ lọc, Ẩn / Tìm kiếm nâng cao', 'Luôn hiện', 'Khối nâng cao mở sẵn khi vào màn'),
    ('Ô Thời gian (Từ ngày – Đến ngày)', 'Chỉ khi Kỳ = Tuỳ chọn', 'Bắt buộc đủ 2 ngày'),
    ('Ô tích Xem toàn bộ kho', 'Luôn hiện', 'Khóa khi công ty không có kho nào trong phạm vi quyền'),
    ('4 cột tick Nhà / Dãy / Khoang / Vị trí', 'Khi ô Kho có ít nhất 1 kho', 'Bỏ hết kho → ẩn và xóa các tick'),
    ('Ô chọn ĐVT trên dòng mặt hàng', 'Hàng có từ 2 ĐVT trở lên', 'Hàng 1 ĐVT hiện tên ĐVT dạng chữ'),
], widths=[2.0, 2.0, 2.0])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A, [0, 1, 2])],
    [('FR-01', 'Xem báo cáo tổng hợp xuất nhập tồn', 'view'),
     ('FR-07', 'In báo cáo', 'io'),
     ('FR-08', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Lọc theo Nhà / Dãy / Khoang / Vị trí', 'view', 'extend', [0], None),
     ('FR-04', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-05', 'Chọn hàng hóa', 'view', 'extend', [0], None),
     ('FR-06', 'Đổi đơn vị tính', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Tổng hợp xuất nhập tồn')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
k = fr(1, 'Xem báo cáo tổng hợp xuất nhập tồn',
       rule=('- Màn Danh sách, Phân trang và Báo cáo.', 'list'),
       intro=dict(
           ten='Truy cập màn Tổng hợp xuất nhập tồn và xem báo cáo',
           mota='Mở màn và hiển thị, với từng mặt hàng có phát sinh trên các kho (vị trí) đã chọn trong kỳ đã chọn: Tồn đầu kỳ, Nhập '
                'trong kỳ, Xuất trong kỳ, Tồn cuối kỳ. Gồm dòng tóm tắt (kỳ, khoảng ngày, mã các kho), khối tổng hợp (Mặt hàng có phát '
                'sinh, Kho đang xem; số mặt hàng có tồn đầu kỳ / có nhập / có xuất / còn tồn cuối kỳ), bảng phẳng mỗi mặt hàng 1 dòng kèm '
                'dòng TỔNG, phân trang theo mặt hàng. Màn chỉ đọc; phạm vi kho theo quyền.',
           tacnhan=TN, dieukien=DK,
           chinh='1. Người dùng vào menu theo đường dẫn ở mục Layout.\n'
                 '2. Hệ thống kiểm quyền, nạp danh mục bộ lọc theo phạm vi quyền (công ty, kho, công ty thuê của từng kho) và danh mục '
                 'hàng hóa (nhóm, tính chất, loại, thương hiệu, hãng sản xuất).\n'
                 '3. Có bộ lọc ghi tạm dưới 10 phút → khôi phục (kể cả hàng hóa, các tick vị trí còn hợp lệ; kho không còn trong phạm vi '
                 'bị bỏ); không có → Kỳ = Năm nay, Loại báo cáo = Tất cả, Tồn theo công ty = công ty của người dùng, Kho = TOÀN BỘ kho '
                 'của công ty (tích sẵn Xem toàn bộ kho), Công ty thuê kho = mọi công ty thuê của các kho, không tick vị trí nào.\n'
                 '4. Hệ thống nạp cây Nhà / Dãy / Khoang / Vị trí của các kho, cộng nhật ký tồn tại các vị trí đang xét theo từng mặt '
                 'hàng, giữ mặt hàng có tồn đầu / nhập / xuất khác 0, sắp theo tên hàng; dựng khối tổng hợp trên TOÀN tập; trả 20 mặt hàng '
                 'của trang 1.\n'
                 '5. Hệ thống hiển thị dòng tóm tắt, khối tổng hợp, bảng, dòng “Hiển thị 1–20 / N mặt hàng”.',
           phu='• Thiếu ô bắt buộc (bỏ hết kho / chưa có công ty / Tuỳ chọn thiếu ngày) → không tính, bảng hiện ' + M_CHONKHO + ' (tương '
               'tự ' + M_CHONCTY + ', ' + M_CHONNGAY + ').\n'
               '• Không có mặt hàng nào có phát sinh → bảng hiện ' + M_EMPTY + ', ẩn phân trang; khối tổng hợp hiện Mặt hàng có phát sinh 0.\n'
               '• Không có quyền → báo ' + NOPERM + ', danh mục bộ lọc rỗng, bảng hiện ' + M_CHONCTY + '\n'
               '• Đổi bộ lọc khi đang có báo cáo → giữ số cũ làm mờ cho tới khi có số mới; lỗi tải thì giữ số cũ, báo lỗi.\n'
               '• Bấm Thu gọn → ẩn các ô của khối tổng hợp, còn dòng tóm tắt; bấm Mở rộng để hiện lại.\n'
               '• Bấm số trang / đổi Số dòng/trang → nạp lại đúng trang; dòng TỔNG và khối tổng hợp không đổi; trang vượt quá → về '
               'trang cuối.\n'
               '• Phiên đăng nhập hết hạn → chuyển về màn đăng nhập.',
           dacbiet='Bảng cố định 10 cột: STT, Tên hàng, Model, Mã hàng, Thương hiệu, Đơn vị, Tồn đầu kỳ, Nhập trong kỳ, Xuất trong kỳ, '
                   'Tồn cuối kỳ — không có cột ẩn, không có Tùy chỉnh cột, không sắp xếp theo cột (luôn theo tên hàng). Số 0 để ô trống. '
                   'Phân trang theo MẶT HÀNG (mặc định 20; 10 / 20 / 50 / 100). Không cộng số lượng ở dòng TỔNG vì mỗi hàng một ĐVT. Cả '
                   'công ty nhiều kho (hàng nghìn mặt hàng) có thể mất vài giây.'),
       layout=dict(menu=MENU, shot=shot('03_detail'),
                   shot_caption='Màn Tổng hợp xuất nhập tồn — công ty CN Hải Phòng, 4 kho, Năm nay (khối lọc thu gọn)',
                   note='Lối vào duy nhất (phân hệ Kho, nhóm Báo cáo kho). Hiển thị: mặt hàng có phát sinh trên các kho trong phạm vi quyền.',
                   extra=[(shot('00_menu'), 'Mục Tổng hợp xuất nhập tồn trong nhóm Báo cáo kho của phân hệ Kho'),
                          (shot('01a_default'), 'Mở màn lần đầu: công ty mặc định, toàn bộ kho của công ty, Năm nay, báo cáo tự tải'),
                          (shot('01b_empty'), 'Bỏ tích Xem toàn bộ kho: ô Kho trống, bảng chờ chọn kho')]),
       ui_kw=dict(required=False),
       ui=[
           ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '“Tổng hợp xuất nhập tồn”',
            ['- Ở thanh trên cùng, cũng là tiêu đề tab trình duyệt', '- Icon ⓘ: “' + TIP_TITLE + '”']),
           ('Dòng tóm tắt', 'Label', 'Read-only', '–', 'Theo dữ liệu',
            ['- “Xuất nhập tồn <kỳ> (dd/mm/yyyy – dd/mm/yyyy) · Kho: <mã các kho>”, vd “Xuất nhập tồn năm 2026 (01/01/2026 – 31/12/2026)”',
             '- Rê chuột vào phần Kho: mã - tên từng kho', '- Icon ⓘ: “' + TIP_GOAL + '”', '- Chỉ hiện khi đã có báo cáo']),
           ('Nút Thu gọn', 'Button', 'Enable', '–', 'Hiển thị',
            ['- Góc phải dòng tóm tắt', '- Bấm → ẩn các ô khối tổng hợp, chữ đổi thành “Mở rộng”', '- Không gọi lại dữ liệu']),
           ('Khối Mặt hàng', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Ô Mặt hàng có phát sinh: “N mặt hàng” — luôn hiện', '- Ô Kho đang xem: “N kho”', '- Icon ⓘ: “' + TIP_MH + '”',
             '- Số KHÔNG bấm được (không mở cửa sổ)']),
           ('Khối Phát sinh', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- 4 ô: Có tồn đầu kỳ, Có nhập trong kỳ, Có xuất trong kỳ, Còn tồn cuối kỳ — “N mặt hàng”',
             '- Ô bằng 0 thì ẩn (vd Năm trước không có ô Có tồn đầu kỳ); 4 ô đều 0 thì ẩn cả khối', '- Icon ⓘ: “' + TIP_PS + '”',
             '- Số không bấm được']),
           ('Bảng báo cáo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- 10 cột, mỗi cột mô tả ở 1 dòng bên dưới', '- Tiêu đề dính khi cuộn dọc',
             '- Cuộn ngang khi bảng rộng hơn màn hình (bảng tối thiểu 1.370px)']),
           ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Dòng TỔNG: “TỔNG”', '- Mặt hàng: 1, 2… liên tục giữa các trang (trang 2 cỡ 20 bắt đầu từ 21)']),
           ('Cột Tên hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Tên hàng, dài cắt “…”, rê chuột xem đủ']),
           ('Cột Model', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Model của hàng, dài cắt “…”', '- Trống khi hàng chưa khai']),
           ('Cột Mã hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Dài cắt “…”, rê chuột xem đủ']),
           ('Cột Thương hiệu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Trống khi chưa khai']),
           ('Cột Đơn vị', 'Dropdown', 'Enable', 'Danh sách ĐVT của hàng', 'ĐVT cơ sở',
            ['- Hàng từ 2 ĐVT: ô chọn dạng “<tên> (x<hệ số>)”; hàng 1 ĐVT: chữ tên ĐVT',
             '- Mặc định: ĐVT cơ sở', '- Icon ⓘ: “' + TIP_DVT + '”', '- Đổi ĐVT → mục 2.6']),
           ('Cột Tồn đầu kỳ', 'Table/Grid', 'Read-only', 'Số, tối đa 2 số lẻ', 'Theo dữ liệu',
            ['- Căn phải, dấu phẩy phân cách hàng nghìn, quy đổi theo ĐVT đang chọn', '- Số 0 để trống; có thể âm',
             '- Icon ⓘ: “' + TIP_DAU + '”']),
           ('Cột Nhập trong kỳ', 'Table/Grid', 'Read-only', 'Số, tối đa 2 số lẻ', 'Theo dữ liệu',
            ['- Căn phải, số 0 để trống', '- Icon ⓘ: “' + TIP_NHAP + '”']),
           ('Cột Xuất trong kỳ', 'Table/Grid', 'Read-only', 'Số, tối đa 2 số lẻ', 'Theo dữ liệu',
            ['- Hiện số DƯƠNG (lượng đã xuất), căn phải, số 0 để trống', '- Icon ⓘ: “' + TIP_XUAT + '”']),
           ('Cột Tồn cuối kỳ', 'Table/Grid', 'Read-only', 'Số, tối đa 2 số lẻ', 'Theo dữ liệu',
            ['- = Tồn đầu kỳ + Nhập − Xuất', '- Số 0 để trống (hàng đã xuất hết)', '- Icon ⓘ: “' + TIP_CUOI + '”']),
           ('Dòng TỔNG', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Nền cam, đầu bảng: “MẶT HÀNG CÓ PHÁT SINH · N mặt hàng” (toàn tập đã lọc, không theo trang)',
             '- Không cộng số lượng', '- Icon ⓘ: “' + TIP_TONG + '”']),
           ('Dòng “Hiển thị a–b / N mặt hàng”', 'Label', 'Read-only', '–', 'Theo dữ liệu',
            ['- a–b: thứ tự mặt hàng của trang đang xem', '- N: tổng mặt hàng có phát sinh khớp bộ lọc']),
           ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', '20',
            ['- Mặc định: 20', '- Lựa chọn: 10, 20, 50, 100 (mặt hàng)', '- Đổi giá trị → về trang 1, nạp lại']),
           ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
            ['- Nút «, ‹, số trang, ›, »; ở trang đầu nút « ‹ mờ, trang cuối › » mờ', '- Ẩn khi không có mặt hàng',
             '- Giữ bộ lọc và ĐVT đã chọn khi đổi trang']),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
            ['- Chưa chọn kho: ' + M_CHONKHO, '- Chưa có công ty: ' + M_CHONCTY, '- Tuỳ chọn thiếu ngày: ' + M_CHONNGAY,
             '- Không có hàng: ' + M_EMPTY, '- Đang tải lần đầu: “Đang tải dữ liệu...”']),
           ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
            ['- Thiếu quyền: ' + NOPERM, '- Lỗi khác: câu máy chủ trả hoặc ' + M_LOADERR,
             '- Hết phiên đăng nhập: chuyển về màn đăng nhập']),
       ],
       ev=[('Mở màn hình', 'System',
            'Before:\n– Kiểm tra 1 trong 3 quyền xem báo cáo tồn kho; không có → hiển thị ' + NOPERM + ' và dừng xử lý.\n'
            '– Có bộ lọc ghi tạm dưới 10 phút → khôi phục; công ty / kho đã ghi không còn trong phạm vi → bỏ.\n'
            'During:\n– Nạp danh mục công ty, kho, công ty thuê kho theo phạm vi quyền; Kỳ mặc định Năm nay; chưa có kho → chọn hết kho '
            'của công ty và mọi công ty thuê của các kho; nạp cây Nhà / Dãy / Khoang / Vị trí.\n'
            'After:\n– Hiển thị dòng tóm tắt, khối tổng hợp, bảng trang 1 (20 mặt hàng), dòng “Hiển thị 1–20 / N”.'),
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
           ('Rê chuột vào biểu tượng ⓘ', 'Hover',
            'Before:\n– Ở tiêu đề khối lọc, dòng tóm tắt, khối tổng hợp, dòng TỔNG, tiêu đề 5 cột Đơn vị / Tồn đầu kỳ / Nhập / Xuất / Tồn '
            'cuối kỳ.\nDuring:\n– Lấy nội dung giải thích.\nAfter:\n– Hiện khung giải thích (nguyên văn ở mục 2.1.5).'),
           ('Phiên đăng nhập hết hạn khi thao tác', 'System',
            'Before:\n– Áp cho mọi lần nạp báo cáo, in, xuất.\nDuring:\n– Máy chủ từ chối yêu cầu.\n'
            'After:\n– Chuyển về màn đăng nhập, không hiện dữ liệu.')])

d.p('2.1.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('Bảng dưới mô tả cách hệ thống tính từng chỉ tiêu, từng cột số liệu và nội dung icon ⓘ (nguyên văn trên giao diện). “Tập dữ liệu” '
    'là các lần thay đổi tồn TẠI CÁC VỊ TRÍ đang xét (mọi vị trí của các kho đã chọn, hoặc các vị trí theo tick ở mục 2.3), ghi nhận cho '
    'các công ty thuê kho đang lọc (bỏ trống = mọi công ty thuê của các kho), sau khi áp các ô lọc hàng hóa, trong phạm vi quyền. Nguồn '
    'thay đổi tồn: mọi chứng từ kho đã ghi tồn theo vị trí (tồn kho đầu kỳ, nhập kho, nhập lại, xuất kho, xuất điều chỉnh sai số liệu, '
    'nhập / xuất điều chỉnh kiểm kê, điều chuyển vị trí — Phần 5). Mỗi mặt hàng 1 dòng, cộng mọi kho / vị trí / công ty thuê đang xét.')
d.data_table([
    ('Dòng tóm tắt', 'Kỳ = nhãn kỳ (vd “năm 2026”, “tháng 11/2026”, “tuần này”, “từ 01/10/2026 đến 31/10/2026”) + khoảng ngày; Kho = mã '
                     'các kho đã chọn (rê chuột: mã - tên); ⓘ ghi giờ máy chủ tính số liệu.', TIP_GOAL),
    ('Cột Tồn đầu kỳ', 'Tổng mọi thay đổi tồn (nhập +, xuất −) của hàng ghi nhận TRƯỚC 00:00 ngày đầu kỳ. = Tồn cuối kỳ của kỳ liền trước '
                       '(vd Năm trước của ENEO-700-V5231 kho HP: 0 + 265 − 195 = 70 = Tồn đầu kỳ năm 2026).', TIP_DAU),
    ('Cột Nhập trong kỳ', 'Tổng các thay đổi DƯƠNG từ 00:00 ngày đầu kỳ tới hết ngày cuối kỳ (phiếu nhập kho, nhập lại, nhập điều chỉnh '
                          'kiểm kê, khai báo tồn đầu kỳ, và hàng chuyển VÀO vị trí bởi phiếu điều chuyển vị trí).', TIP_NHAP),
    ('Cột Xuất trong kỳ', 'Tổng các thay đổi ÂM trong kỳ, hiển thị số dương (phiếu xuất kho, xuất điều chỉnh sai số liệu, xuất điều chỉnh '
                          'kiểm kê, hàng chuyển RA khỏi vị trí bởi phiếu điều chuyển vị trí).', TIP_XUAT),
    ('Cột Tồn cuối kỳ', 'Tồn đầu kỳ + Nhập − Xuất (= tồn tại hết ngày cuối kỳ). Với kỳ chứa hôm nay = SL tồn của Báo cáo tồn kho tổng '
                        'hợp theo mặt hàng tính đến hôm nay (cùng kho, không tick vị trí).', TIP_CUOI),
    ('Loại báo cáo “Không nhặt phiếu điều chuyển”', 'Bỏ mọi thay đổi do phiếu điều chuyển vị trí: Nhập và Xuất cùng giảm đúng phần điều '
                                                     'chuyển, Tồn đầu / cuối kỳ thường không đổi khi xét cả kho (vd ENEO-640-V5236 kho '
                                                     'PTT: Tất cả 11,404 / 23,348; Không nhặt 7,435 / 19,379; tồn cuối vẫn 3,197).', '—'),
    ('Ô Mặt hàng có phát sinh / dòng TỔNG', 'Đếm mặt hàng có ít nhất 1 trong 3 số Tồn đầu kỳ / Nhập / Xuất khác 0 (hàng nhập rồi xuất hết '
                                             'trong kỳ vẫn tính). Toàn tập, không theo trang. = N ở “Hiển thị a–b / N”.', TIP_MH),
    ('Ô Kho đang xem', 'Số kho đang chọn sau khi bỏ kho ngoài phạm vi quyền / khác công ty.', '(dùng chung ⓘ của khối)'),
    ('4 ô khối Phát sinh', 'Có tồn đầu kỳ / Có nhập / Có xuất / Còn tồn cuối kỳ = số mặt hàng có cột tương ứng khác 0 (kể cả âm). Ô bằng 0 '
                           'thì ẩn. Còn tồn cuối kỳ = số dòng của Báo cáo tồn kho tổng hợp theo mặt hàng (vd CN Hải Phòng 4 kho: 96).',
     TIP_PS),
    ('Quy đổi ĐVT', 'Mọi số của hàng = số theo ĐVT cơ sở ÷ hệ số ĐVT đang chọn (vd 24 Can 1L → Thùng 24C-1L x24 = 1). In / Excel dùng '
                    'đúng ĐVT đã chọn từng hàng, làm tròn 2 số lẻ.', TIP_DVT),
    ('Thứ tự dòng', 'Mặt hàng theo tên hàng (A→Z theo cách so chữ của cơ sở dữ liệu), trùng tên theo thứ tự tạo hàng.', '—'),
    ('Ràng buộc khớp số', 'Chọn đúng 1 kho + 1 công ty thuê + 1 hàng: 4 số = khối Số lượng của Thẻ kho cùng kỳ, cùng Loại báo cáo. Nhiều '
                          'kho = tổng từng kho (ENEO-700-V5231: 4 kho 70 + 523 − 546 = 47 = HP 20 + CB 27).', '—'),
])
k += 1
d.p('2.1.%d Danh sách popup mở từ số liệu' % k)
d.popup_table([
    ('Số ở khối tổng hợp, dòng TỔNG, 4 cột số lượng', 'Không có popup — số không bấm được, không mở Thẻ kho',
     'Báo cáo tổng hợp theo kỳ; xem từng chứng từ của 1 hàng dùng Thẻ kho (mở từ menu)',
     'Con số đọc trực tiếp trên bảng (mục 2.1.5)'),
    ('Ô chọn ĐVT trên dòng mặt hàng', 'Không phải popup — ô chọn ngay trong bảng (mục 2.6)',
     'Xem số của hàng theo đơn vị lớn (thùng, hộp…)', 'Danh sách ĐVT của chính mặt hàng'),
    ('Ô Hàng hóa trong bộ lọc', 'Chọn hàng hóa (mục 2.5)', 'Thu hẹp báo cáo về đúng 1 mặt hàng',
     'Danh sách hàng hóa theo công ty đang xem; chọn 1 hàng thì báo cáo còn tối đa 1 mặt hàng'),
])

# ------------------------------------------------------------ 2.2
k = fr(2, 'Tìm kiếm và lọc',
       rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
       intro=dict(ten='Tìm kiếm và lọc báo cáo tổng hợp xuất nhập tồn',
                  mota='Chọn kỳ (5 lựa chọn, Tuỳ chọn thì tự chọn khoảng ngày), loại báo cáo (có / không nhặt phiếu điều chuyển), công ty, '
                       'một hoặc nhiều kho (2 ô bắt buộc; ô tích Xem toàn bộ kho chọn nhanh mọi kho), công ty thuê kho và thu hẹp tập mặt '
                       'hàng theo tính chất, loại, thương hiệu, hãng sản xuất, nhóm hoặc 1 hàng hóa cụ thể. Màn không có ô tìm nhanh bằng '
                       'chữ; mọi ô là ô chọn, áp ngay khi đổi.',
                  tacnhan=TN, dieukien=DK,
                  chinh='1. Người dùng chọn Kỳ (Tuỳ chọn → chọn Từ ngày – Đến ngày ở ô Thời gian hiện ngay sau).\n'
                        '2. Người dùng chọn Loại báo cáo, Tồn theo công ty (hệ thống chọn sẵn mọi kho của công ty).\n'
                        '3. Người dùng bỏ / thêm kho ở ô Kho, hoặc bỏ tích Xem toàn bộ kho để tự chọn.\n'
                        '4. Hệ thống tự tích mọi công ty thuê của các kho đang chọn, xóa các tick vị trí, nạp lại cây vị trí.\n'
                        '5. Người dùng chọn thêm các ô lọc hàng hóa (chọn nhiều) hoặc chọn 1 hàng qua cửa sổ Chọn hàng hóa (mục 2.5).\n'
                        '6. Mỗi lần đổi ô, hệ thống gom các thay đổi trong 0,3 giây thành 1 lần tính, về trang 1, nạp lại báo cáo, ghi tạm '
                        'bộ lọc trên trình duyệt (10 phút).',
                  phu='• Bỏ tích Xem toàn bộ kho → xóa mọi kho (và công ty thuê), ẩn 4 cột vị trí, bảng hiện ' + M_CHONKHO + '; tích lại → '
                      'chọn hết kho.\n'
                      '• Bấm Tìm kiếm / In danh sách / Xuất Excel khi thiếu ô bắt buộc → chữ đỏ dưới ô thiếu (' + M_KHO + ', ' + M_TG +
                      ', ' + M_CTY + '), khối lọc tự mở, không nạp.\n'
                      '• Kỳ Tuỳ chọn mà Đến ngày trước Từ ngày → máy chủ báo ' + M_NGUOC + '.\n'
                      '• Đổi Kỳ từ Tuỳ chọn sang kỳ khác → xóa khoảng ngày đã chọn, ẩn ô Thời gian.\n'
                      '• Đổi Tồn theo công ty → chọn lại HẾT kho của công ty mới và mọi công ty thuê của chúng.\n'
                      '• Bỏ 1 kho bằng dấu × → ô Xem toàn bộ kho tự bỏ tích; công ty thuê tích lại theo các kho còn lại.\n'
                      '• Bỏ trống Công ty thuê kho → tính mọi công ty thuê của các kho.\n'
                      '• Bấm Xóa lọc → về công ty mặc định + Năm nay + Tất cả + toàn bộ kho, bỏ mọi ô khác (kể cả hàng hóa, tick vị trí), '
                      'xóa bộ lọc ghi tạm, nạp lại.\n'
                      '• Không có kết quả → ' + M_EMPTY + '\n'
                      '• Rời sang màn khác → xóa bộ lọc ghi tạm; F5 / tab mới trong 10 phút → khôi phục.',
                  dacbiet='Các ô chọn khớp CHÍNH XÁC; Loại hàng hóa khớp khi hàng thuộc ít nhất 1 loại đã chọn. Kết hợp nhiều ô = thỏa đồng '
                          'thời (VÀ); trong 1 ô chọn nhiều = HOẶC. Màn không có ô Hợp đồng / Model (giữ y ERP) nên không có tình huống ký '
                          'tự đặc biệt “%”, “_”.'),
       layout=dict(menu=MENU + ' => Ẩn tìm kiếm nâng cao', shot=shot('02_filter'),
                   shot_caption='Khối Bộ lọc tổng hợp xuất nhập tồn (mở sẵn khi vào màn)',
                   extra=[(shot('01c_required'), 'Bấm Tìm kiếm khi ô Kho trống: chữ đỏ “Vui lòng chọn kho”'),
                          (shot('02f_ky_opts'), 'Ô Kỳ: Tuần này, Tháng này, Năm nay, Năm trước, Tuỳ chọn'),
                          (shot('02d_custom'), 'Kỳ Tuỳ chọn 01/10/2026 – 31/10/2026: ô Thời gian hiện ngay sau ô Kỳ'),
                          (shot('02b_kho_opts'), 'Ô Kho liệt kê mã kho của công ty đang chọn trong phạm vi quyền')]),
       ui=[('Tiêu đề khối', 'Label', 'Hiển thị', '–', '–', '“Bộ lọc tổng hợp xuất nhập tồn”',
            ['- Kèm biểu tượng phễu', '- Icon ⓘ: “' + TIP_PURPOSE + '”']),
           ('Kỳ', 'Dropdown', 'Enable', '5 giá trị', 'Có', 'Năm nay',
            ['- Lựa chọn: Tuần này, Tháng này, Năm nay, Năm trước, Tuỳ chọn', '- Không có nút × bỏ chọn',
             '- Icon ⓘ: “' + TIP_KY + '”', '- Đổi → nạp lại']),
           ('Thời gian', 'Datepicker', 'Enable', 'dd/mm/yyyy – dd/mm/yyyy', 'Có', 'Trống',
            ['- Chỉ hiện khi Kỳ = Tuỳ chọn, ngay sau ô Kỳ', '- Thiếu 1 trong 2 ngày → ' + M_TG + ', bảng ' + M_CHONNGAY,
             '- Đến ngày trước Từ ngày → ' + M_NGUOC]),
           ('Loại báo cáo', 'Dropdown', 'Enable', '2 giá trị', 'Không', 'Tất cả',
            ['- Tất cả: tính cả phiếu điều chuyển vị trí', '- Không nhặt phiếu điều chuyển: bỏ các lần chuyển hàng giữa 2 vị trí',
             '- Không có nút × bỏ chọn']),
           ('Tính chất hàng hóa', 'Dropdown', 'Enable', 'Danh mục tính chất', 'Không', 'Trống', ['- Chọn nhiều', '- Mặc định: trống (tất cả)']),
           ('Loại hàng hóa', 'Dropdown', 'Enable', 'Danh mục loại', 'Không', 'Trống', ['- Chọn nhiều', '- Hàng thuộc ít nhất 1 loại đã chọn']),
           ('Thương hiệu', 'Dropdown', 'Enable', 'Danh mục thương hiệu', 'Không', 'Trống', ['- Chọn nhiều', '- Mặc định: trống']),
           ('Hãng sản xuất', 'Dropdown', 'Enable', 'Danh mục hãng', 'Không', 'Trống', ['- Chọn nhiều', '- Mặc định: trống']),
           ('Nhóm hàng hóa', 'Dropdown', 'Enable', 'Danh mục nhóm', 'Không', 'Trống', ['- Chọn nhiều', '- Mặc định: trống']),
           ('Hàng hóa', 'Textbox', 'Read-only', '1 hàng', 'Không', 'Trống',
            ['- Bấm ô → mở cửa sổ Chọn hàng hóa (mục 2.5)', '- Đã chọn: thẻ “<mã> - <tên>” (dài cắt “…”) có dấu × để bỏ chọn',
             '- Chỉ giữ 1 hàng']),
           ('Tồn theo công ty', 'Dropdown', 'Enable', 'Danh sách theo quyền', 'Có', 'Công ty của người dùng',
            ['- V1: mọi công ty đang hoạt động; V2 / V3: chỉ công ty mình', '- Không có nút × bỏ chọn',
             '- Đổi → chọn hết kho của công ty mới']),
           ('Xem toàn bộ kho', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Tích',
            ['- Tích: chọn hết kho của công ty', '- Bỏ tích: xóa mọi kho để tự chọn', '- Tự tích / bỏ tích theo ô Kho',
             '- Khóa khi công ty không có kho trong phạm vi']),
           ('Kho', 'Dropdown', 'Enable', 'Danh sách theo quyền', 'Có', 'Toàn bộ kho',
            ['- Chọn nhiều, hiện MÃ kho (vd CB, HP, KĐN-ALM, NM)', '- Thiếu → ' + M_KHO,
             '- Đổi → tích sẵn mọi công ty thuê của các kho, xóa tick vị trí']),
           ('Công ty thuê kho', 'Dropdown', 'Enable', 'Công ty thuê của các kho', 'Không', 'Mọi công ty thuê của các kho',
            ['- Chọn nhiều, hiện mã công ty, mỗi công ty 1 lần', '- Icon ⓘ: “' + TIP_THUE + '”', '- Bỏ trống = mọi công ty thuê']),
           ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
            ['- Kiểm ô bắt buộc; thiếu → chữ đỏ dưới ô, mở khối lọc', '- Đủ → về trang 1, nạp lại, ghi tạm bộ lọc']),
           ('Nút Xóa lọc', 'Button', 'Enable', '–', '–', 'Hiển thị',
            ['- Về công ty mặc định + Năm nay + Tất cả + toàn bộ kho, bỏ mọi ô khác', '- Xóa bộ lọc ghi tạm, tắt chữ đỏ, nạp lại']),
           ('Nút Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
            ['- Thu gọn / mở khối ô lọc', '- Khi thu gọn nhãn là “Tìm kiếm nâng cao”', '- Mặc định mở']),
           ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (mục 2.4).'),
           ('Chữ lỗi dưới ô bắt buộc', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
            ['- ' + M_KHO, '- ' + M_TG, '- ' + M_CTY, '- Chỉ hiện sau lần bấm Tìm kiếm / In / Xuất đầu tiên; chọn lại là tự tắt']),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + M_EMPTY, '- ' + M_CHONKHO, '- ' + M_CHONNGAY])],
       ev=[('Đổi một ô chọn', 'Change',
            'Before:\n– Áp cho Kỳ, Thời gian, Loại báo cáo, công ty, kho, công ty thuê, 5 ô danh mục, Hàng hóa.\n'
            '– Đổi công ty → chọn hết kho công ty mới; đổi kho → tích mọi công ty thuê của các kho, xóa tick vị trí.\n'
            'During:\n– Ghi tạm bộ lọc; gom các thay đổi trong 0,3 giây; thiếu ô bắt buộc → không gọi máy chủ, bảng chờ chọn.\n'
            '– Máy chủ kiểm công ty trong danh mục được xem, bỏ kho ngoài phạm vi / khác công ty, kiểm khoảng ngày; sai → báo lỗi tại ô.\n'
            + ERR + '\nAfter:\n– Về trang 1, hiển thị báo cáo mới; lỗi thì giữ báo cáo cũ.'),
           ('Chọn Kỳ = Tuỳ chọn', 'Change',
            'Before:\n– Ô Thời gian chưa có.\nDuring:\n– Hiện ô Thời gian ngay sau ô Kỳ; chưa đủ 2 ngày thì chưa tính.\n'
            'After:\n– Bảng hiện ' + M_CHONNGAY + ' cho tới khi chọn đủ Từ ngày – Đến ngày, rồi tự nạp.'),
           ('Tích / bỏ tích Xem toàn bộ kho', 'Change',
            'Before:\n– Công ty có kho trong phạm vi.\nDuring:\n– Tích → chọn hết kho; bỏ tích → xóa kho, công ty thuê và tick vị trí.\n'
            'After:\n– Tích: nạp lại báo cáo; bỏ tích: bảng hiện ' + M_CHONKHO + ', không gọi máy chủ.'),
           ('Bấm Tìm kiếm khi thiếu ô bắt buộc', 'Click',
            'Before:\n– Bật chế độ hiện lỗi.\nDuring:\n– Ô thiếu viền đỏ, chữ ' + M_KHO + ' / ' + M_TG + '; mở khối lọc.\n'
            'After:\n– Không nạp, không ghi tạm.'),
           ('Bấm Xóa lọc', 'Click',
            'Before:\n– Không hỏi xác nhận.\n'
            'During:\n– Đặt lại: công ty mặc định, Năm nay, Tất cả, toàn bộ kho, mọi công ty thuê; các ô khác trống; xóa tick vị trí, bộ lọc '
            'ghi tạm; tắt chữ đỏ.\nAfter:\n– Nạp lại cây vị trí và báo cáo trang 1.'),
           ('Bấm Ẩn / Tìm kiếm nâng cao', 'Click',
            'Before:\n– Khối đang mở / thu gọn.\nDuring:\n– Đổi trạng thái khối.\nAfter:\n– Giá trị đã chọn vẫn áp dụng; trạng thái ghi tạm cùng bộ lọc.'),
           ('Rời màn hoặc tải lại trang', 'System',
            'Before:\n– Bộ lọc ghi tạm 10 phút trên trình duyệt.\n'
            'During:\n– Chuyển sang màn khác → xóa bộ lọc ghi tạm; F5 / tab mới trong 10 phút → khôi phục.\n'
            'After:\n– Vào lại bằng menu sau khi rời màn → bộ lọc mặc định.')])
d.p('2.2.%d Cách lấy dữ liệu của ô lọc' % k)
d.p('Bảng dưới giải thích cách hệ thống áp từng ô lọc lên tập dữ liệu (mục 2.1.5).')
d.data_table([
    ('Kỳ', 'Tuần này: thứ Hai → Chủ nhật tuần hiện tại; Tháng này: ngày 1 → ngày cuối tháng; Năm nay: 01/01 → 31/12 năm hiện tại; Năm '
           'trước: 01/01 → 31/12 năm trước; Tuỳ chọn: Từ ngày → Đến ngày. Ngày cuối kỳ ở tương lai không làm đổi số (chưa có phát sinh).',
     TIP_KY),
    ('Loại báo cáo', 'Không nhặt phiếu điều chuyển → bỏ mọi thay đổi tồn do phiếu điều chuyển vị trí (cả 3 cột Tồn đầu, Nhập, Xuất).', '—'),
    ('Tồn theo công ty', 'Quyết định danh sách kho chọn được và letterhead; không lọc theo công ty ghi nhận tồn.', '—'),
    ('Kho', 'Một hoặc nhiều kho; chỉ giữ kho thuộc phạm vi quyền và thuộc công ty đang chọn (kho lạ bị bỏ, không còn kho nào → '
            + M_KHO + '). Không tick vị trí = mọi vị trí của các kho (vị trí trong khoang + vị trí tự do).', '—'),
    ('Công ty thuê kho', 'Chỉ cộng thay đổi tồn ghi cho các công ty đã tích (trong số công ty thuê của các kho); bỏ trống = mọi công ty '
                         'thuê của các kho; các kho không có công ty thuê nào → rỗng.', TIP_THUE),
    ('Tính chất / Thương hiệu / Hãng sản xuất / Nhóm', 'Hàng có thuộc tính tương ứng bằng 1 trong các giá trị đã chọn.', '—'),
    ('Loại hàng hóa', 'Hàng có danh sách loại chứa ít nhất 1 loại đã chọn.', '—'),
    ('Hàng hóa', 'Đúng 1 mặt hàng đã chọn (gồm cả hàng đã ngừng kinh doanh).', '—'),
])

# ------------------------------------------------------------ 2.3
k = fr(3, 'Lọc theo Nhà / Dãy / Khoang / Vị trí',
       rule=('- Bộ lọc và Dropdown.', 'search'),
       intro=dict(ten='Thu hẹp báo cáo theo Nhà / Dãy / Khoang / Vị trí của các kho đang chọn',
                  mota='Dưới các ô lọc là 4 cột tick Nhà → Dãy → Khoang → Vị trí của các kho đang chọn (nhóm theo mã kho). Cột con chỉ '
                       'liệt kê con của các cha đang tick; cột Vị trí luôn có nhóm “Vị trí tự do · <mã kho>”. Cách các tick thu hẹp số liệu '
                       'GIỮ Y HỆT hệ thống ERP (người dùng đã chốt 24/10/2026), kể cả 2 hiện tượng: tick Nhà / Dãy / Khoang mà không tick '
                       'Vị trí thì không thu hẹp gì; có tick Vị trí thì kho không tick gì bị bỏ khỏi báo cáo.',
                  tacnhan=TN, dieukien=DK + '\n4. Ô Kho có ít nhất 1 kho (4 cột chỉ hiện khi đã chọn kho).',
                  chinh='1. Người dùng tick Nhà ở cột Nhà (có ô tìm theo mã / tên, “Chọn hết” cả cột và “Chọn hết” theo từng kho).\n'
                        '2. Hệ thống hiện các Dãy của Nhà đã tick ở cột Dãy (nhóm “<mã kho> | <mã nhà> - <tên nhà>”); người dùng tick Dãy.\n'
                        '3. Tương tự với Khoang, rồi Vị trí (nhóm “<mã nhà> | <mã dãy> | <mã khoang>”).\n'
                        '4. Mỗi lần tick, hệ thống nạp lại báo cáo (trang 1): có ít nhất 1 Vị trí được tick → chỉ cộng các vị trí đã tick + '
                        'vị trí của các Nhà / Dãy / Khoang tick mà không tick cấp con; không tick Vị trí nào → mọi vị trí của các kho.',
                  phu='• Bỏ tick cấp cha → các tick cấp con không còn hợp lệ tự bỏ.\n'
                      '• Tick Vị trí của 1 kho khi đang chọn nhiều kho → các kho còn lại (không tick gì) bị bỏ khỏi số liệu (vd ENEO-700-'
                      'V5231 2 kho HP + CB: không tick 47; tick vị trí KHOANG1 kho HP → 20).\n'
                      '• Tick Nhà / Dãy / Khoang mà không tick Vị trí → số liệu như không tick (vd tick Nhà N1 kho HP, nơi không có hàng '
                      'ENEO-700-V5231 → vẫn 20).\n'
                      '• Đổi Kho / bỏ tích Xem toàn bộ kho / Xóa lọc → xóa mọi tick, nạp lại cây.\n'
                      '• F5 trong 10 phút → giữ các tick còn thuộc cây vị trí hiện tại.',
                  dacbiet='Khác Thẻ kho và Báo cáo tồn kho theo vị trí (2 màn đó thu hẹp theo cấp sâu nhất đã tick). Hai hiện tượng trên là '
                          'đúng theo hệ thống ERP, không phải lỗi. Vị trí đang khóa vẫn hiện để tick.'),
       layout=dict(menu=MENU + ' => Nhà / Dãy / Khoang / Vị trí', shot=shot('02h_scope_full'),
                   shot_caption='Kho HP, hàng ENEO-700-V5231: tick Tầng 1 → Dãy 1 → Khoang 1 → vị trí KHOANG1',
                   note='4 cột tick nằm trong khối Bộ lọc của màn báo cáo theo đường dẫn ở trên.',
                   extra=[(shot('01_list'), 'Nhiều kho: cột Nhà nhóm theo mã kho (CB, HP, KĐN-ALM…), cột Vị trí có Vị trí tự do từng kho')]),
       ui=[('Cột Nhà', 'Checkbox', 'Enable', 'Nhà của các kho', 'Không', 'Không tick',
            ['- Nhóm theo mã kho (in đậm), mỗi nhà “<mã> - <tên>”', '- Ô tìm “Tìm theo mã hoặc tên nhà”', '- “Chọn hết” cả cột và từng kho']),
           ('Cột Dãy', 'Checkbox', 'Enable', 'Dãy của Nhà đã tick', 'Không', 'Không tick',
            ['- Nhóm “<mã kho> | <mã nhà> - <tên nhà>”', '- Chưa tick Nhà: “Chưa chọn nhà hoặc không có dữ liệu”']),
           ('Cột Khoang', 'Checkbox', 'Enable', 'Khoang của Dãy đã tick', 'Không', 'Không tick',
            ['- Nhóm “<mã nhà> | <mã dãy>”', '- Chưa tick Dãy: “Chưa chọn dãy hoặc không có dữ liệu”']),
           ('Cột Vị trí', 'Checkbox', 'Enable', 'Vị trí tự do + vị trí của Khoang đã tick', 'Không', 'Không tick',
            ['- Nhóm “Vị trí tự do · <mã kho>” luôn có', '- Nhóm “<mã nhà> | <mã dãy> | <mã khoang>”',
             '- Có ít nhất 1 tick ở cột này mới thu hẹp số liệu']),
           ('Ô tìm của từng cột', 'Textbox', 'Enable', 'Không giới hạn', 'Không', 'Trống',
            ['- Lọc danh sách trong cột theo mã hoặc tên (không phân biệt hoa / thường)', '- Có chữ thì hiện × xóa nhanh',
             '- Chỉ lọc hiển thị, không đổi tick']),
           ('Ô Chọn hết của cột', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Không tick',
            ['- Tick / bỏ mọi dòng đang hiện của cột', '- Khóa khi cột trống']),
           ('Ô Chọn hết của nhóm', 'Checkbox', 'Enable', '–', 'Không', 'Không tick', ['- Tick / bỏ các dòng đang hiện của nhóm']),
           ('Dòng mục (nhà / dãy / khoang / vị trí)', 'Checkbox', 'Enable', '–', 'Không', 'Không tick',
            ['- Nhãn “<mã> - <tên>”', '- Bỏ tick cha → tự bỏ tick con']),
           ('Dòng tóm tắt sau lọc', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Vẫn ghi mã các kho đang chọn (không ghi vị trí)']),
           ('Bảng sau lọc', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
            ['- 4 cột số chỉ cộng các vị trí đang xét', '- Về trang 1']),
           ('Thông báo trống cột', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu',
            ['- “Chưa chọn kho vật lý” khi kho không có cây vị trí', '- “Không có dữ liệu” khi cột Nhà trống'])],
       ev=[('Tick / bỏ tick 1 dòng', 'Change',
            'Before:\n– Bỏ qua sự kiện lặp mang đúng trạng thái hiện tại.\nDuring:\n– Ghi tick; bỏ cha thì loại các con không còn hợp lệ; ghi '
            'tạm bộ lọc.\n– Máy chủ đổi tick thành danh sách vị trí theo quy tắc ERP (mục 2.3.5).\n' + ERR + '\n'
            'After:\n– Về trang 1, nạp lại báo cáo; cột con cập nhật.'),
           ('Bấm Chọn hết (cột hoặc nhóm)', 'Change',
            'Before:\n– Có dòng đang hiện.\nDuring:\n– Tick / bỏ mọi dòng đang hiện (theo ô tìm).\nAfter:\n– Nạp lại báo cáo.'),
           ('Gõ ô tìm của cột', 'Change',
            'Before:\n– Không gọi máy chủ.\nDuring:\n– Lọc các dòng chứa chuỗi gõ trong mã hoặc tên.\nAfter:\n– Danh sách cột thu hẹp; tick '
            'giữ nguyên.'),
           ('Đổi kho', 'System',
            'Before:\n– Ô Kho đổi.\nDuring:\n– Xóa mọi tick, nạp lại cây vị trí của các kho mới.\nAfter:\n– 4 cột hiện cây mới; bỏ hết kho '
            'thì ẩn 4 cột.')])
d.p('2.3.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('Cách hệ thống đổi các tick thành tập vị trí cộng số liệu (giữ y hệ thống ERP).')
d.data_table([
    ('Không tick Vị trí nào', 'Lấy mọi vị trí của các kho đang chọn (vị trí trong khoang qua Nhà của kho + vị trí tự do), cộng thêm vị '
                              'trí của các Nhà / Dãy / Khoang “lá” (đã thuộc kho) → kết quả = cả kho. Tick Nhà / Dãy / Khoang không thu hẹp.',
     '—'),
    ('Có tick ít nhất 1 Vị trí', 'CHỈ lấy các vị trí đã tick + mọi vị trí của các Nhà tick mà không tick Dãy nào, Dãy tick mà không tick '
                                 'Khoang nào, Khoang tick mà không tick Vị trí nào. Kho không có tick nào bị bỏ hẳn.', '—'),
    ('Vị trí tự do', 'Tick vị trí tự do của kho tính như tick Vị trí.', '—'),
    ('Đối chiếu', 'Tick đúng các vị trí có hàng (theo Báo cáo tồn kho theo vị trí) → Tồn cuối kỳ = tổng SL các vị trí đó (vd KHOANG1 kho '
                  'HP = 20).', '—'),
])

# ------------------------------------------------------------ 2.4
fr(4, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị',
              mota='Cho phép mỗi người dùng tự chọn các ô lọc muốn thấy ở khối Bộ lọc tổng hợp xuất nhập tồn và sắp xếp lại thứ tự. Cấu '
                   'hình lưu theo người dùng cho riêng màn này (13 mục: Kỳ, Loại báo cáo, Tính chất hàng hóa, Loại hàng hóa, Thương hiệu, '
                   'Hãng sản xuất, Nhóm hàng hóa, Hàng hóa, Tồn theo công ty, Xem toàn bộ kho, Kho, Công ty thuê kho, Nhà / Dãy / Khoang / '
                   'Vị trí).',
              tacnhan=TN, dieukien=DK,
              chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
                    '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 13 mục kèm ô tích, theo cấu hình đang lưu.\n'
                    '3. Người dùng tích / bỏ tích và kéo thả để đổi thứ tự.\n'
                    '4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình cho người dùng, hiển thị “Cập nhật thành công” và áp ngay lên khối lọc.',
              phu='• Bấm Khôi phục mặc định → tích lại đủ 13 mục theo thứ tự gốc; phải bấm Lưu mới có hiệu lực.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không lưu thay đổi.\n'
                  '• Lưu thất bại → hiển thị thông báo lỗi.\n'
                  '• Lưu ý: ẩn ô bắt buộc (Tồn theo công ty, Kho) vẫn giữ giá trị đang có; ô Thời gian đi theo ô Kỳ (chỉ hiện khi Tuỳ chọn).',
              dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('07_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Cài đặt bộ lọc”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách ô lọc', 'Table/Grid', 'Enable', '13 mục', 'Không', 'Theo cấu hình đã lưu',
        ['- Kỳ, Loại báo cáo, Tính chất hàng hóa, Loại hàng hóa, Thương hiệu, Hãng sản xuất, Nhóm hàng hóa, Hàng hóa, Tồn theo công ty, '
         'Xem toàn bộ kho, Kho, Công ty thuê kho, Nhà / Dãy / Khoang / Vị trí', '- Mỗi mục đánh số thứ tự']),
       ('Ô tích của ô lọc', 'Checkbox', 'Enable', '–', 'Không', 'Theo cấu hình đã lưu', ['- Tích: ô hiện ở khối lọc', '- Bỏ tích: ẩn']),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo để đổi thứ tự ô lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình cho người dùng hiện tại, đóng cửa sổ, áp ngay.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích lại đủ 13 mục, thứ tự gốc; chưa lưu.'),
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
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Tích lại toàn bộ mục, thứ tự gốc.\nAfter:\n– Chưa lưu; phải bấm Lưu.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Bỏ mọi thay đổi chưa lưu.\nAfter:\n– Đóng cửa sổ, khối lọc giữ nguyên.')])

# ------------------------------------------------------------ 2.5
k = fr(5, 'Chọn hàng hóa',
       rule=('- Popup chọn dữ liệu, Bộ lọc.', 'search'),
       intro=dict(ten='Chọn 1 hàng hóa để lọc báo cáo qua cửa sổ Chọn hàng hóa',
                  mota='Bấm ô Hàng hóa của bộ lọc để mở cửa sổ “Chọn hàng hóa” dùng chung (cây catalog + bảng hàng hóa có tìm kiếm, '
                       'lọc), phạm vi mọi hàng hóa kể cả hàng chưa kinh doanh tại công ty đang xem. Bấm tên 1 hàng để chọn; báo cáo chỉ '
                       'còn hàng đó (cộng trên mọi kho / vị trí đang xét).',
                  tacnhan=TN, dieukien=DK + '\n4. Đã chọn Tồn theo công ty (cửa sổ tra hàng theo công ty đang xem).',
                  chinh='1. Người dùng bấm ô Hàng hóa.\n'
                        '2. Hệ thống mở cửa sổ “Chọn hàng hóa”: dòng công ty đang xem, cây catalog (số hàng mỗi nhánh), ô tìm theo mã, '
                        'tên, model, barcode, mã đặt hàng, công tắc Còn tồn / Gồm hàng ngoài catalog, bảng hàng hóa.\n'
                        '3. Người dùng tìm / lọc rồi bấm vào tên hàng.\n'
                        '4. Hệ thống đóng cửa sổ, ô Hàng hóa hiện thẻ “<mã> - <tên>”, ghi tạm bộ lọc, về trang 1 và nạp lại báo cáo (1 lần).',
                  phu='• Bấm Đóng / (x) → đóng, giữ hàng đã chọn trước đó.\n'
                      '• Bấm dấu × trên thẻ hàng → bỏ chọn, báo cáo nạp lại mọi hàng (không mở cửa sổ).\n'
                      '• Hàng đã chọn không có phát sinh trong kỳ ở các kho → bảng ' + M_EMPTY + '\n'
                      '• Tồn theo công ty khác công ty của tài khoản mà tài khoản không có quyền tra hàng ở công ty đó → cửa sổ báo “Không '
                      'tải được số lượng — Thử lại” và “Không tải được danh sách hàng hoá — Máy chủ báo lỗi (mã 403)”, không chọn được hàng '
                      '(hành vi hiện tại của cửa sổ dùng chung — giống các màn báo cáo tồn kho anh em).\n'
                      '• F5 trong 10 phút → ô Hàng hóa vẫn hiện hàng đã chọn.',
                  dacbiet='Chỉ chọn được 1 hàng (giữ y ERP); cửa sổ có nút Phóng to toàn màn hình.'),
       layout=dict(menu=MENU + ' => Hàng hóa', shot=shot('04b_picker_tpe'), shot_caption='Cửa sổ Chọn hàng hóa (công ty TPE)',
                   note='Modal Chọn hàng hóa được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.',
                   extra=[(shot('04_picker'), 'Tồn theo công ty CN Hải Phòng trên tài khoản công ty TPE: cửa sổ báo lỗi 403'),
                          (shot('04c_one'), 'Đã chọn ENEO-640-V5236, kho PTT: 15,141 + 11,404 − 23,348 = 3,197')]),
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
           ('Ô Hàng hóa sau khi chọn', 'Textbox', 'Read-only', '–', '–', 'Trống', ['- Thẻ “<mã> - <tên>”', '- Dấu × bỏ chọn']),
           ('Thông báo lỗi tải', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
            ['- “Không tải được số lượng — Thử lại”', '- “Không tải được danh sách hàng hoá”', '- Nút Thử lại'])],
       ev=[('Bấm ô Hàng hóa', 'Click',
            'Before:\n– Lấy công ty đang chọn ở ô Tồn theo công ty.\nDuring:\n– Mở cửa sổ, nạp cây catalog và danh sách hàng.\n'
            'After:\n– Cửa sổ hiển thị trên màn báo cáo.'),
           ('Bấm tên hàng trong bảng', 'Click',
            'Before:\n– Chỉ chọn 1 hàng.\nDuring:\n– Ghi tên hàng rồi mã hàng vào bộ lọc (để chỉ nạp 1 lần), ghi tạm bộ lọc.\n'
            'After:\n– Đóng cửa sổ, về trang 1, nạp lại báo cáo.'),
           ('Bấm dấu × trên thẻ hàng', 'Click',
            'Before:\n– Ô đang có hàng.\nDuring:\n– Xóa hàng khỏi bộ lọc, không mở cửa sổ.\nAfter:\n– Nạp lại báo cáo mọi hàng.'),
           ('Bấm Đóng hoặc (x)', 'Click',
            'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không đổi bộ lọc.\nAfter:\n– Đóng cửa sổ.'),
           ('Tìm / lọc trong cửa sổ', 'Change',
            'Before:\n– Áp cho ô tìm, cây catalog, công tắc.\nDuring:\n– Nạp lại bảng hàng.\n' + ERR + '\nAfter:\n– Bảng cập nhật; lỗi → nút Thử lại.')])
d.p('2.5.%d Mục đích thiết kế popup' % k)
d.bullets([
    'Trả lời câu hỏi: trong kỳ, RIÊNG một mặt hàng (tìm theo mã / tên / model / barcode) đầu kỳ còn bao nhiêu, nhập / xuất bao nhiêu, '
    'cuối kỳ còn bao nhiêu trên các kho đang chọn — khi công ty có hàng nghìn mặt hàng.',
    'Là cửa sổ nổi để giữ nguyên ngữ cảnh báo cáo (kỳ, kho, vị trí, các ô lọc khác); cây catalog + tìm kiếm cần chỗ rộng nên không nhét '
    'vào ô chọn thả xuống.',
    'Ràng buộc khớp số: sau khi chọn, báo cáo còn tối đa 1 mặt hàng, 4 số = 4 số của hàng đó khi không lọc hàng; Tồn bán được trong cửa '
    'sổ là số của công ty, KHÔNG phải tồn trên các kho đang xem.',
    'Người dùng làm tiếp: đối chiếu với Thẻ kho cùng hàng / kho / kỳ, đổi ĐVT (mục 2.6), In / Xuất Excel đúng 1 hàng.',
])
k += 1
d.p('2.5.%d Các biến thể theo con số bấm' % k)
d.popup_variant_table([
    ('Ô Hàng hóa khi chưa chọn hàng', 'Mọi hàng hóa của công ty đang xem (kể cả chưa kinh doanh)', '“Chọn hàng hóa”',
     'Không ẩn ô nào; chỉ chọn 1 hàng'),
    ('Ô Hàng hóa khi đã có hàng', 'Như trên; hàng cũ được thay khi chọn hàng mới', '“Chọn hàng hóa”', 'Không ẩn ô nào'),
])

# ------------------------------------------------------------ 2.6
k = fr(6, 'Đổi đơn vị tính từng mặt hàng',
       rule=('- Màn Xem chi tiết và Báo cáo.', 'detail'),
       intro=dict(ten='Xem số lượng của mặt hàng theo đơn vị tính khác',
                  mota='Ngay trong bảng báo cáo: ô Đơn vị trên mỗi dòng có từ 2 ĐVT cho đổi đơn vị hiển thị riêng từng mặt hàng — cả 4 cột '
                       'Tồn đầu kỳ, Nhập, Xuất, Tồn cuối kỳ quy đổi theo hệ số. Chỉ đổi cách hiển thị, không tính lại số; ĐVT đã chọn được '
                       'dùng cho In / Xuất Excel.',
                  tacnhan=TN, dieukien=DK + '\n4. Báo cáo đã có ít nhất 1 mặt hàng có từ 2 ĐVT.',
                  chinh='1. Người dùng bấm ô Đơn vị ở dòng mặt hàng → danh sách ĐVT của hàng “<tên> (x<hệ số>)”.\n'
                        '2. Người dùng chọn ĐVT khác.\n'
                        '3. Hệ thống chia 4 số của hàng đó cho hệ số, hiển thị lại (không gọi máy chủ).\n'
                        '4. Khi In / Xuất Excel, hệ thống gửi kèm ĐVT đã chọn của từng hàng.',
                  phu='• Hàng chỉ 1 ĐVT → hiện tên ĐVT dạng chữ, không có ô chọn.\n'
                      '• Đổi trang / đổi bộ lọc → ĐVT đã chọn được giữ theo từng hàng (không ghi tạm khi F5).\n'
                      '• Số sau quy đổi bằng 0 → ô trống.',
                  dacbiet='Đổi ĐVT không gọi lại máy chủ. In / Excel làm tròn 2 số lẻ; hàng chưa đổi dùng ĐVT cơ sở.'),
       layout=dict(menu=MENU + ' => Đơn vị', shot=shot('03c_unit'),
                   shot_caption='Ô chọn ĐVT của hàng ENEO-410-S4136 (Can 1L / Thùng 24C-1L x24)',
                   note='Thao tác ngay trên bảng của màn báo cáo theo đường dẫn ở trên.',
                   extra=[(shot('03d_unit_after'), 'Đổi sang Thùng 24C-1L (x24): 120 / 552 / 648 / 24 Can → 5 / 23 / 27 / 1 Thùng')]),
       ui=[('Ô chọn ĐVT', 'Dropdown', 'Enable', 'ĐVT của hàng', 'Không', 'ĐVT cơ sở',
            ['- Chỉ ở hàng có từ 2 ĐVT', '- Mặc định: ĐVT cơ sở (hệ số nhỏ nhất)', '- Lựa chọn “<tên> (x<hệ số>)”; hệ số 1 chỉ hiện tên',
             '- Không có nút × bỏ chọn']),
           ('Chữ ĐVT', 'Label', 'Read-only', '–', '–', 'ĐVT duy nhất', ['- Hàng 1 ĐVT: tên ĐVT, vd “Xô 18L”']),
           ('Cột Tồn đầu kỳ sau quy đổi', 'Table/Grid', 'Read-only', 'Số, tối đa 2 số lẻ', '–', 'Theo dữ liệu', ['- = số ĐVT cơ sở ÷ hệ số']),
           ('Cột Nhập trong kỳ sau quy đổi', 'Table/Grid', 'Read-only', 'Số, tối đa 2 số lẻ', '–', 'Theo dữ liệu', ['- = số ĐVT cơ sở ÷ hệ số']),
           ('Cột Xuất trong kỳ sau quy đổi', 'Table/Grid', 'Read-only', 'Số, tối đa 2 số lẻ', '–', 'Theo dữ liệu', ['- Số dương ÷ hệ số']),
           ('Cột Tồn cuối kỳ sau quy đổi', 'Table/Grid', 'Read-only', 'Số, tối đa 2 số lẻ', '–', 'Theo dữ liệu',
            ['- Vd 24 Can 1L → Thùng x24 = 1']),
           ('Icon ⓘ cột Đơn vị', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “' + TIP_DVT + '”')],
       ev=[('Đổi ĐVT dòng mặt hàng', 'Change',
            'Before:\n– Bỏ qua giá trị rỗng / trùng ĐVT đang chọn.\nDuring:\n– Ghi ĐVT chọn cho hàng; lấy hệ số, chia 4 số của hàng.\n'
            'After:\n– Dòng hiển thị số mới; không gọi máy chủ; In / Excel dùng ĐVT này.'),
           ('Đổi trang hoặc bộ lọc', 'System',
            'Before:\n– Có dữ liệu mới.\nDuring:\n– Áp lại ĐVT đã chọn cho hàng có trong trang mới.\nAfter:\n– Hàng đã đổi ĐVT vẫn hiện '
            'theo ĐVT đó; ĐVT không còn thuộc hàng → về ĐVT cơ sở.'),
           ('Tải lại trang (F5)', 'System',
            'Before:\n– ĐVT đã chọn không ghi tạm.\nDuring:\n– Nạp lại báo cáo.\nAfter:\n– Mọi hàng về ĐVT cơ sở.')])
d.p('2.6.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('“Tập dữ liệu” là các mặt hàng của trang đang xem (mục 2.1.5).')
d.data_table([
    ('ĐVT', 'Danh sách ĐVT của hàng, ĐVT cơ sở (hệ số nhỏ nhất) đứng đầu.', TIP_DVT),
    ('4 cột số sau quy đổi', 'Số theo ĐVT cơ sở ÷ hệ số ĐVT đang chọn. Quan hệ Tồn đầu + Nhập − Xuất = Tồn cuối giữ nguyên sau quy đổi '
                             '(5 + 23 − 27 = 1).', '—'),
])

# ------------------------------------------------------------ 2.7
fr(7, 'In báo cáo', usecase=('FR-07', 'In báo cáo', 'io', A),
   rule=('- Quy tắc In và Báo cáo.', 'list'),
   intro=dict(ten='In báo cáo tổng hợp xuất nhập tồn (xem trước rồi in)',
              mota='Chọn kiểu in Đầy đủ (có Model và Thương hiệu) hoặc Ngắn gọn (chỉ tên, mã, đơn vị và số lượng), chọn cột in, xem trước '
                   'bản in gồm letterhead công ty đang xem, tiêu đề “BÁO CÁO TỔNG HỢP XUẤT NHẬP TỒN”, Thời gian (Từ ngày … đến ngày …), '
                   'Kho, bảng TOÀN BỘ mặt hàng theo bộ lọc đang hiển thị (không riêng trang đang xem), theo ĐVT đã chọn từng hàng, khối ký '
                   'Trưởng kho / Người lập báo cáo; bấm In.',
              tacnhan=TN, dieukien=DK + '\n4. Đã có báo cáo (đủ ô bắt buộc).',
              chinh='1. Người dùng bấm In danh sách.\n'
                    '2. Hệ thống mở cửa sổ “In báo cáo”: kiểu Đầy đủ được chọn, tích sẵn mọi cột của kiểu.\n'
                    '3. Người dùng chọn kiểu, tích / bỏ tích cột, bấm In.\n'
                    '4. Hệ thống kiểm quyền, lấy toàn bộ mặt hàng theo bộ lọc của báo cáo đang hiển thị, quy đổi theo ĐVT đã chọn; đếm '
                    'số dòng in (mỗi mặt hàng 1 dòng).\n'
                    '5. Hệ thống mở cửa sổ “Xem trước tổng hợp xuất nhập tồn”; người dùng bấm In → hộp thoại in của trình duyệt.',
              phu='• Chưa có báo cáo (thiếu ô bắt buộc) → không mở cửa sổ, chữ đỏ dưới ô thiếu.\n'
                  '• Bỏ tích hết cột → ' + M_NOCOL + ', cửa sổ không đóng.\n'
                  '• Vượt 2.000 mặt hàng (vd công ty TPE 8 kho Năm nay: 8.441) → bản xem trước không có nội dung, hiện ' + M_LIMIT +
                  ', ẩn nút In.\n'
                  '• Báo cáo rỗng → bản in có dòng “Không có dữ liệu”.\n'
                  '• Bấm Hủy / (x) → đóng, không in. Lỗi → “Không tải được dữ liệu in” hoặc câu máy chủ trả.',
              dacbiet='STT luôn được in; số theo ĐVT đã chọn, làm tròn 2 số lẻ, số 0 để trống, cột Xuất in số dương. Letterhead theo '
                      'công ty ĐANG XEM (ô Tồn theo công ty). Bản in A4 ngang. Hệ thống ERP không có nút In (thêm có chủ đích).'),
   layout=dict(menu=MENU + ' => In danh sách', shot=shot('05_print'), shot_caption='Cửa sổ In báo cáo (kiểu Đầy đủ, chọn cột in)',
               note='Modal In báo cáo và Xem trước được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.',
               extra=[(shot('05b_preview'), 'Xem trước bản in kiểu Đầy đủ — CN Hải Phòng, 4 kho, Năm nay'),
                      (shot('05c_print_err'), 'Bỏ tích hết cột rồi bấm In: “Vui lòng chọn ít nhất 1 cột để in”')]),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“In báo cáo”', 'Kèm nút (x) đóng.'),
       ('Kiểu in', 'Radio', 'Enable', '2 giá trị', 'Có', 'Đầy đủ',
        ['- Mặc định: Đầy đủ', '- Đầy đủ: “Có Model và Thương hiệu.”', '- Ngắn gọn: “Chỉ tên, mã, đơn vị và số lượng.”',
         '- Đổi kiểu → danh sách cột đổi theo']),
       ('Tiêu đề Chọn cột in', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- Icon ⓘ: “Cột STT luôn được in. Số lượng theo ĐVT đang chọn của từng hàng.”'),
       ('Ô Chọn tất cả', 'Checkbox', 'Enable', '–', 'Không', 'Tích', ['- Tích / bỏ tích mọi cột', '- Bán chọn khi tích 1 phần']),
       ('Danh sách cột', 'Checkbox', 'Enable', '9 hoặc 7 cột', 'Ít nhất 1', 'Tích hết',
        ['- Đầy đủ: Tên hàng hóa, Model, Mã hàng, Thương hiệu, Đơn vị, Tồn đầu kỳ, Nhập trong kỳ, Xuất trong kỳ, Tồn cuối kỳ',
         '- Ngắn gọn: Tên hàng hóa, Mã hàng, Đơn vị + 4 cột số']),
       ('Chữ lỗi chọn cột', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + M_NOCOL),
       ('Nút In (cửa sổ In báo cáo)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Kiểm ≥ 1 cột rồi mở xem trước.'),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không in.'),
       ('Cửa sổ Xem trước', 'Popup', 'Read-only', '–', '–', 'Ẩn',
        ['- Tiêu đề “Xem trước tổng hợp xuất nhập tồn”', '- Letterhead, “BÁO CÁO TỔNG HỢP XUẤT NHẬP TỒN”, “Thời gian: Từ ngày dd/mm/yyyy '
         'đến ngày dd/mm/yyyy”, “Kho: <mã - tên các kho>”, bảng, khối ký Trưởng kho / Người lập báo cáo']),
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

# ------------------------------------------------------------ 2.8
fr(8, 'Xuất Excel', usecase=('FR-08', 'Xuất Excel', 'io', A),
   rule=('- Quy tắc Excel.', 'excel'),
   intro=dict(ten='Xuất báo cáo tổng hợp xuất nhập tồn ra Excel',
              mota='Chọn kiểu Đầy đủ hoặc Ngắn gọn rồi tải file Excel gồm TOÀN BỘ mặt hàng theo bộ lọc của báo cáo đang hiển thị (không '
                   'riêng trang đang xem), đủ cột của kiểu đã chọn (Excel không có bước chọn cột), theo ĐVT đã chọn từng hàng.',
              tacnhan=TN, dieukien=DK + '\n4. Đã có báo cáo (đủ ô bắt buộc).',
              chinh='1. Người dùng bấm Xuất Excel ở đầu khối bộ lọc.\n'
                    '2. Hệ thống mở cửa sổ “Xuất Excel tổng hợp xuất nhập tồn”, kiểu Đầy đủ được chọn.\n'
                    '3. Người dùng chọn kiểu, bấm Xuất Excel trong cửa sổ.\n'
                    '4. Hệ thống khóa nút (chữ “Đang xuất…”, vòng xoay), kiểm quyền, lấy toàn bộ mặt hàng, dựng file.\n'
                    '5. Trình duyệt tải file “' + FILE + '”; cửa sổ đóng.',
              phu='• Chưa có báo cáo → không mở cửa sổ, chữ đỏ dưới ô thiếu.\n'
                  '• Bấm Hủy / (x) → đóng, không xuất.\n'
                  '• Lỗi → ' + M_XLS_ERR + ' (thiếu quyền: báo không có quyền), giữ cửa sổ để bấm lại.\n'
                  '• Báo cáo rỗng → vẫn tải file, bảng có dòng “Không có dữ liệu”.',
              dacbiet='Luôn tải thẳng, không gửi mail (ERP gửi mail khi trên 7.000 mặt hàng). Cấu trúc file: dòng 1 letterhead công ty '
                      'đang xem (rộng bằng bảng); tiêu đề “BÁO CÁO TỔNG HỢP XUẤT NHẬP TỒN”; “Từ ngày: dd/mm/yyyy Đến ngày: dd/mm/yyyy”; '
                      '“Kho: <mã - tên các kho>”; bảng 1 tầng tiêu đề; khối ký Trưởng kho / Người lập báo cáo kèm ngày. Số lượng là ô số '
                      'có dấu phân cách hàng nghìn (cộng được), số 0 để trống, Xuất là số dương. Vài nghìn mặt hàng có thể mất vài chục giây.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('06_export'), shot_caption='Cửa sổ Xuất Excel — chọn kiểu xuất',
               note='Modal Xuất Excel được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Xuất Excel tổng hợp xuất nhập tồn”', 'Kèm biểu tượng Excel, nút (x).'),
       ('Nhãn Kiểu xuất', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Kiểu xuất”'),
       ('Kiểu xuất', 'Radio', 'Enable', '2 giá trị', 'Có', 'Đầy đủ',
        ['- Mặc định: Đầy đủ (mỗi lần mở về Đầy đủ)', '- Đầy đủ: “Có Model và Thương hiệu.”',
         '- Ngắn gọn: “Chỉ tên, mã, đơn vị và số lượng.”']),
       ('Nút Xuất Excel (cửa sổ)', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → tải file', '- Khóa khi đang xuất, chữ “Đang xuất…”']),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Hủy.'),
       ('Nút Xuất Excel (đầu khối lọc)', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Nền xanh lá nhạt', '- Khi đang xuất: chữ “Đang xuất…”, vòng xoay, khóa']),
       ('File tải về', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Tên “' + FILE + '”', '- Đầy đủ: STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, Đơn vị, Tồn đầu kỳ, Nhập trong kỳ, Xuất trong '
         'kỳ, Tồn cuối kỳ', '- Ngắn gọn: STT, Tên hàng hóa, Mã hàng, Đơn vị + 4 cột số', '- Đơn vị ghi “<tên> (x<hệ số>)” theo ĐVT đã chọn']),
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
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Tổng hợp xuất nhập tồn; không lặp lại các quy tắc đã có trong SRS quy tắc '
           'chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Ô bắt buộc và mặc định', [
        '– Bắt buộc Tồn theo công ty, ít nhất 1 Kho; Kỳ Tuỳ chọn bắt buộc đủ Từ ngày – Đến ngày (Đến ngày không trước Từ ngày).',
        '– Mặc định: Năm nay, Tất cả, công ty của người dùng, TOÀN BỘ kho của công ty, mọi công ty thuê của các kho, không tick vị trí.',
        '– Đổi công ty chọn lại hết kho; đổi kho tích mọi công ty thuê của các kho và xóa tick vị trí.'],
     ['Tìm kiếm và lọc', 'In báo cáo', 'Xuất Excel']),
    ('BR-02', 'Công thức 4 cột', [
        '– Tồn đầu kỳ = tổng thay đổi tồn trước ngày đầu kỳ; Nhập = tổng thay đổi dương trong kỳ; Xuất = tổng thay đổi âm trong kỳ (hiện '
        'số dương); Tồn cuối kỳ = Tồn đầu + Nhập − Xuất.',
        '– Cộng theo nhật ký tồn tại các vị trí đang xét, công ty thuê đang lọc; khớp Thẻ kho cùng hàng / kho / công ty / kỳ / loại báo cáo.'],
     ['Xem báo cáo', 'In báo cáo', 'Xuất Excel']),
    ('BR-03', 'Mặt hàng lên báo cáo', [
        '– Mặt hàng có ít nhất 1 trong 3 số Tồn đầu / Nhập / Xuất khác 0 (kể cả hàng nhập rồi xuất hết trong kỳ, Tồn cuối kỳ trống).',
        '– Sắp theo tên hàng; phân trang theo mặt hàng (mặc định 20, tối đa 100).',
        '– Khối tổng hợp, dòng TỔNG tính trên toàn tập, không theo trang; không cộng số lượng.'],
     ['Xem báo cáo']),
    ('BR-04', 'Phiếu điều chuyển vị trí', [
        '– Loại báo cáo Tất cả: hàng chuyển vào vị trí tính Nhập, chuyển ra tính Xuất (kể cả chuyển trong cùng kho).',
        '– Không nhặt phiếu điều chuyển: bỏ các lần đó khỏi cả 3 số; tồn cuối của cả kho thường không đổi.'],
     ['Tìm kiếm và lọc', 'Xem báo cáo']),
    ('BR-05', 'Lọc vị trí giữ y hệ thống ERP', [
        '– Không tick Vị trí nào → mọi vị trí của các kho (tick Nhà / Dãy / Khoang không thu hẹp).',
        '– Có tick Vị trí → chỉ vị trí đã tick + vị trí của các cấp tick mà không tick cấp con; kho không tick gì bị bỏ.'],
     ['Lọc theo Nhà / Dãy / Khoang / Vị trí']),
    ('BR-06', 'Phạm vi theo quyền', [
        '– Có 1 trong 3 quyền xem báo cáo tồn kho mới xem được; quyền cao nhất thắng.',
        '– Tổng công ty: mọi công ty / kho; công ty: kho của công ty mình; kho: kho mình là thủ kho.',
        '– Máy chủ khóa công ty với người không có quyền tổng công ty; kho ngoài phạm vi bị bỏ, hết kho → “Vui lòng chọn kho”.'],
     ['Mọi chức năng']),
    ('BR-07', 'Quy đổi ĐVT', [
        '– Số trên màn = số ĐVT cơ sở ÷ hệ số ĐVT chọn riêng từng hàng.',
        '– In / Excel dùng đúng ĐVT đã chọn trên màn (hàng chưa đổi: ĐVT cơ sở), làm tròn 2 số lẻ.'],
     ['Đổi đơn vị tính', 'In báo cáo', 'Xuất Excel']),
    ('BR-08', 'Chuẩn hóa dữ liệu lọc', [
        '– Ô chọn khớp chính xác; nhiều giá trị trong 1 ô = HOẶC; nhiều ô = VÀ.',
        '– Công ty thuê ngoài danh sách của các kho bị bỏ qua; kỳ cuối ở tương lai không đổi số.'],
     ['Tìm kiếm và lọc']),
    ('BR-09', 'Ghi nhớ bộ lọc', [
        '– Bộ lọc (kể cả hàng đã chọn, tick vị trí) ghi tạm 10 phút trên trình duyệt; F5 / tab mới khôi phục.',
        '– Rời sang màn khác hoặc bấm Xóa lọc → xóa. Cấu hình ô lọc (Cài đặt bộ lọc) lưu theo người dùng.'],
     ['Tìm kiếm và lọc', 'Cài đặt bộ lọc']),
    ('BR-10', 'In và xuất', [
        '– Theo bộ lọc của báo cáo đang hiển thị, toàn bộ mặt hàng; letterhead theo công ty đang xem.',
        '– In tối đa 2.000 mặt hàng; vượt thì không in, báo thu hẹp bộ lọc.',
        '– Excel không giới hạn, tải thẳng, tên “' + FILE + '”.'],
     ['In báo cáo', 'Xuất Excel']),
    ('BR-11', 'Tính duy nhất', [
        '– Mỗi mặt hàng 1 dòng (cộng mọi kho / vị trí / công ty thuê đang xét); không có cấp cha – con.'],
     ['Xem báo cáo']),
    ('BR-12', 'Chỉ đọc, không ghi lịch sử', [
        '– Màn không tạo / sửa / xóa dữ liệu, không có lịch sử thay đổi; số liệu đổi theo chứng từ kho ở Phần 5.'],
     ['Mọi chức năng']),
    ('BR-13', 'Khác hệ thống ERP (có chủ đích)', [
        '– Ô Kỳ thay Từ ngày / Đến ngày (mặc định Năm nay, số như nhau); có In xem trước (ERP ẩn nút In); Excel không gửi mail.',
        '– Kiểm quyền ở mọi lần lấy dữ liệu; số 0 để trống (ERP màn “-”, Excel “0”); dòng Kho trên Excel có giá trị; ĐVT In / Excel theo ĐVT '
        'đang chọn.'],
     ['Xem báo cáo', 'In báo cáo', 'Xuất Excel']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Tổng hợp xuất nhập tồn chỉ đọc, không ghi dữ liệu và không màn nào mở sang báo cáo này. Các màn hình dưới đây ghi các thay đổi tồn '
    'theo vị trí mà báo cáo cộng (nhập +, xuất −, theo công ty thuê kho), cung cấp danh mục cho bộ lọc, hoặc đọc cùng nguồn tồn dùng để '
    'đối chiếu số.')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', 'Khai báo tồn kho đầu kỳ (tồn đầu — vào Nhập trong kỳ hoặc Tồn đầu kỳ tùy ngày khai báo)', 'Kho -> Tồn kho đầu kỳ'),
    ('2', 'Kho', 'Phiếu nhập kho (cộng tồn → Nhập trong kỳ)', 'Kho -> Nhập kho'),
    ('3', 'Kho', 'Phiếu nhập kho điều chỉnh kiểm kê (cộng tồn phần thừa sau kiểm kê → Nhập)', 'Kho -> Nhập kho'),
    ('4', 'Tài chính', 'Phiếu xuất kho (trừ tồn → Xuất trong kỳ)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('5', 'Tài chính', 'Phiếu nhập lại (cộng lại tồn hàng đã xuất → Nhập)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('6', 'Kho', 'Phiếu xuất điều chỉnh sai số liệu (trừ tồn → Xuất)', 'Kho -> Xuất kho'),
    ('7', 'Kho', 'Phiếu xuất kho điều chỉnh kiểm kê (trừ tồn phần thiếu sau kiểm kê → Xuất)', 'Kho -> Xuất kho'),
    ('8', 'Kho', 'Phiếu điều chuyển vị trí (vị trí đến → Nhập, vị trí đi → Xuất; bỏ khi chọn “Không nhặt phiếu điều chuyển”)',
     'Kho -> Điều chuyển'),
    ('9', 'Kho', 'Kiểm kê theo vị trí, Kiểm kê theo hàng hóa (kết quả kiểm kê sinh phiếu nhập / xuất điều chỉnh kiểm kê ở dòng 3, 7)',
     'Kho -> Theo vị trí'),
    ('10', 'Kho', 'Kho vật lý, Kho kế toán (danh sách ô Kho, Công ty thuê kho)', 'Kho -> Danh mục'),
    ('11', 'Kho', 'Nhà kho, Dãy, Khoang, Vị trí (4 cột tick Nhà / Dãy / Khoang / Vị trí)', 'Kho -> Danh mục'),
    ('12', 'Hệ thống ERP', 'Danh mục hàng hóa (tên, mã, model, thương hiệu, ĐVT và hệ số ĐVT của hàng)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
    ('13', 'Kho', 'Thẻ kho (cùng nguồn nhật ký tồn vị trí: 1 hàng / kho / công ty thuê / kỳ → 4 số khớp; đối soát từng chứng từ)',
     'Kho -> Báo cáo kho'),
    ('14', 'Kho', 'Báo cáo tồn kho tổng hợp theo mặt hàng, Báo cáo tồn kho chi tiết theo mặt hàng (Tồn cuối kỳ = SL tồn tại ngày cuối kỳ)',
     'Kho -> Báo cáo kho'),
    ('15', 'Kho', 'Báo cáo tồn kho theo vị trí (tổng SL các vị trí đã tick = Tồn cuối kỳ khi tick đúng vị trí đó)', 'Kho -> Báo cáo kho'),
    ('16', 'Kho', 'Báo cáo tồn theo kho (cùng 3 quyền và phạm vi kho)', 'Kho -> Báo cáo kho'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)

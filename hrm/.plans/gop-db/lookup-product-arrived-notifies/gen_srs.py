# -*- coding: utf-8 -*-
"""SRS màn "Phiếu báo hàng về" (phân hệ Thông báo, 3 tab Nhập khẩu / Trong nước / Mua ngoài) — form chuẩn Danh mục
quốc gia + checklist "Mẫu tài liệu.xlsx" (03/11/2026).

Chạy: python gen_srs.py  → SRS - Phiếu báo hàng về.docx
Khung: srs-documenter (SrsDoc) + ../phieu-theo-form-quoc-gia/CHECKLIST.md. Khuôn thư mục: finance-addition-accounting-request.
Nguồn đọc 03/11/2026 (nhánh develop, cả 2 repo):
  FE  pages/lookup/product-arrived-notifies/{index.vue, tabConfigs.js, detailPageMixin.js, components/ArrivedNotifyList.vue,
      import|inland|outside/_id.vue}, components/subsystem-menu/lookup.js, components/subsystems.js (phân hệ "Thông báo"),
      V2BaseSmartFilterPanel, V2BaseDataTable, V2BaseRowActions, export-fields-modal, column-customization-modal,
      filter-customization-modal, ReportPrintPreviewModal + reportPrintPreviewMixin, plugins/axios (hết phiên), pages/extras/404.
  BE  Modules/Finance/{Services/ProductArrivedNotifySummaryService.php, Services/ProductArrivedNotifyImportPrintService.php,
      Http/Controllers/V1/ProductArrivedNotifySummaryController.php, Exports/ProductArrivedNotify2Export.php,
      Resources/views/exports/product_arrived_notify2.blade.php, Routes/api.php}, app/ExcelExport/{DynamicExport,
      ExportColumnRegistry}, resources/views/exports/dynamic.blade.php, ProductImportRequestService (markSourceUsed,
      partnerOptions), PermissionsTableSeeder (quyền 1709–1711).
  Spec docs/superpowers/specs/gop-db/2026-10-14-lookup-product-arrived-notifies-design.md (ưu tiên code khi lệch).
Ảnh: ./pbhv_shots (dev-hrm 03/11/2026, DNS Admin, script pbhv_shots/_capture/capture.js). DNS Admin không có phiếu nhập
  khẩu tự tạo → nút Xóa / Tạo phân bổ chi phí bật tạm cờ trên trình duyệt (không ghi dữ liệu). DB dùng chung không có phiếu
  Trong nước nào → ảnh màn chi tiết Trong nước là bố cục rỗng (phản hồi giả rỗng trên trình duyệt).
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

TEN = 'Phiếu báo hàng về'
SHOTS = os.path.join(HERE, 'pbhv_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # sơ đồ Use Case; HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Thông báo => Thông báo => Phiếu báo hàng về'
M_IMP = MENU + ' => Nhập khẩu'
M_INL = MENU + ' => Trong nước'
M_OUT = MENU + ' => Mua ngoài'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Phiếu báo hàng về.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')

A_ND = 'Người dùng'
A_TAO = 'Người tạo phiếu'
TN_XEM = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được phân hệ Thông báo (màn không gắn quyền xem riêng). '
          'Tab Nhập khẩu giới hạn phạm vi theo quyền Xem phiếu báo hàng về mua nhập khẩu theo tổng công ty / theo công ty / '
          'theo phòng ban (Phần 2); tab Trong nước và Mua ngoài không giới hạn.')
TN_IMP = ('Người dùng có quyền thực hiện chức năng: người xem được phiếu ở tab Nhập khẩu — có một trong các quyền Xem phiếu báo '
          'hàng về mua nhập khẩu theo tổng công ty / theo công ty / theo phòng ban, hoặc không có quyền nào (khi đó chỉ phiếu mình '
          'tạo và phiếu có hàng thuộc thương hiệu mình đang phụ trách mua).')
TN_TAO = ('Người dùng có quyền thực hiện chức năng: Người tạo phiếu — chức năng không gắn quyền riêng, chỉ chính người đã tạo '
          'phiếu thực hiện được, khi phiếu đang ở trạng thái Đã gửi.')
DK_XEM = ('1. Người dùng đăng nhập thành công.\n'
          '2. Người dùng vào được phân hệ Thông báo (không cần quyền riêng để mở màn).\n'
          '3. Người dùng đang ở màn Phiếu báo hàng về.')
DK_IMP = ('1. Người dùng đăng nhập thành công.\n'
          '2. Phiếu nằm trong phạm vi xem tab Nhập khẩu của người dùng (Phần 2).\n'
          '3. Người dùng đang ở tab Nhập khẩu hoặc màn chi tiết phiếu nhập khẩu.')
DK_TAO = ('1. Người dùng đăng nhập thành công.\n'
          '2. Người dùng là người tạo phiếu.\n'
          '3. Phiếu đang ở trạng thái Đã gửi.')

M_404 = '“Không tìm thấy trang yêu cầu” kèm dòng “Không tìm thấy hoặc không được cấp quyền truy cập trang” và nút Về trang chủ'
DEL_TITLE = '“Xác nhận xóa”'
DEL_MSG = '“Bạn có chắc muốn xóa bản ghi này không?”'
MSG_409 = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
STATUS_LIST = ['- Đã gửi: nhãn vàng (phiếu đã báo, chưa lập yêu cầu nhập hàng)',
               '- Đã yêu cầu nhập hàng: nhãn xanh lá (đã lập phiếu yêu cầu nhập hàng / phân bổ chi phí từ phiếu)']
PAGE_ROWS = lambda tab: [  # noqa: E731
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     ['- Góc trái dưới bảng', '- a–b: khoảng số thứ tự của trang đang xem',
      '- N: tổng số phiếu khớp phạm vi và bộ lọc của tab %s (không phải toàn hệ thống)' % tab]),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', '10',
     ['- Mặc định: 10', '- Lựa chọn: 5, 10, 20, 50, 100', '- Đổi giá trị → về trang 1, nạp lại']),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
     ['- Nút về đầu «, lùi ‹, số trang, tiến ›, về cuối »', '- Ở trang đầu nút « ‹ mờ; ở trang cuối nút › » mờ',
      '- Giữ nguyên bộ lọc và sắp xếp khi đổi trang']),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     ['- Trong bảng: “Không có dữ liệu phù hợp.”', '- Dưới bảng: “Không có phiếu nào.” thay cho dòng Hiển thị']),
    ('Thông báo lỗi tải dữ liệu', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
     ['- “Lỗi khi tải dữ liệu” khi máy chủ lỗi', '- Hết phiên đăng nhập: “Phiên đăng nhập đã hết hạn”, chuyển về màn đăng nhập']),
]

d = SrsDoc(out=OUT, menu=MENU, route='/lookup/product-arrived-notifies', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Thông báo': 'menu_phanhe', 'Thông báo': 'menu_thongbao', 'Phiếu báo hàng về': 'menu_muc',
    'Nhập khẩu': 'tab_nhapkhau', 'Trong nước': 'tab_trongnuoc', 'Mua ngoài': 'tab_muangoai',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Xuất Excel': 'btn_xuatexcel', 'Xem chi tiết': 'link_ma', 'Xóa': 'btn_xoa_row', 'In': 'btn_in_row',
    'Xuất Excel phiếu': 'btn_xuat_row', 'Tạo phân bổ chi phí': 'btn_phanbo',
    'Tạo phiếu yêu cầu nhập hàng': 'btn_taoycnh', 'Tạo yêu cầu nhập hàng': 'btn_taoycnh_inland',
}.items()})

UI_OVER = {}
UI_EXPLICIT = {}


def uc(code, name, group, actor):
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None):
    """Một chức năng 2.x: (Biểu đồ Usecase) · Giới thiệu · Layout · Mô tả giao diện · Event.
    layout: dict(menu, shot, shot_caption, note, extra=[(shot, caption)]) hoặc dict(entries=[(menu, ghi chú)], ...)."""
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
    if 'entries' in layout:
        d.p('Đường dẫn màn hình:')
        for m, note in layout['entries']:
            d._menu_para(m)
            d.p(note)
        d.figure(layout['shot'], layout['shot_caption'], width_in=6.2)
    else:
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


# ============================================================== TRANG ĐẦU
d.title_block(TEN)
d.doc.add_page_break()  # Mục lục sang trang riêng như bản Drive đã chuẩn hoá
d.h2('Mục lục')
d.doc.paragraphs[-1].alignment = 1  # căn giữa chữ 'Mục lục'
d.toc()

# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu báo hàng về (mã phiếu PBHV-NNNNN) thuộc phân hệ Thông báo, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng tra cứu, phạm vi dữ liệu và các thao tác trên phiếu báo hàng về.',
    'Làm rõ 3 loại phiếu báo hàng về hiển thị ở 3 tab: Nhập khẩu (hàng mua nước ngoài theo invoice), Trong nước (hàng mua '
    'trong nước theo hợp đồng mới), Mua ngoài (hàng mua ngoài theo hợp đồng / phụ lục hợp đồng mua trong nước).',
    'Làm rõ phạm vi xem của tab Nhập khẩu theo 3 quyền và điều kiện của các thao tác do người tạo phiếu thực hiện.',
])
d.p('Phạm vi chức năng (15 chức năng, đặc tả ở Phần 3):')
d.bullets([
    'Tra cứu danh sách: Xem danh sách 3 tab Nhập khẩu, Trong nước, Mua ngoài; Tìm kiếm và lọc; Cài đặt bộ lọc; Tùy chỉnh cột; '
    'Xuất Excel danh sách.',
    'Xem chi tiết: màn chi tiết riêng cho từng loại phiếu (Nhập khẩu, Trong nước, Mua ngoài), chỉ đọc.',
    'Thao tác trên phiếu Nhập khẩu: Xóa (người tạo, phiếu Đã gửi), In phiếu, Xuất Excel một phiếu, Tạo phân bổ chi phí.',
    'Thao tác trên phiếu Trong nước / Mua ngoài: Tạo yêu cầu nhập hàng (Trong nước, mở hệ thống ERP) và Tạo phiếu yêu cầu '
    'nhập hàng (Mua ngoài, mở màn Thêm phiếu yêu cầu nhập hàng của hệ thống) — chỉ người tạo phiếu, phiếu Đã gửi.',
    'Không thuộc màn này: phiếu báo hàng về được LẬP ở nơi khác (hệ thống ERP), màn này không có Thêm mới, Chỉnh sửa, Duyệt, '
    'Không duyệt, Khóa / Mở khóa, Import Excel và không có Lịch sử thay đổi; nội dung form Phân bổ chi phí, Yêu cầu nhập hàng '
    'theo SRS của màn tương ứng.',
])
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Bộ phận mua hàng, kho, kinh doanh tra cứu hàng sắp về kho: phiếu nào, của invoice / hợp đồng nào, nhà cung cấp nào, về kho nào, '
    'dự kiến ngày nào, hàng dành cho khách / đơn đặt hàng nào.',
    'Phiếu Đã gửi là chứng từ nguồn để lập phiếu yêu cầu nhập hàng (Mua ngoài, Trong nước) hoặc phân bổ chi phí nhập khẩu '
    '(Nhập khẩu); lập xong phiếu chuyển sang Đã yêu cầu nhập hàng.',
    'Bản in và file Excel một phiếu nhập khẩu dùng để gửi kho chuẩn bị nhận hàng.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Màn chủ yếu chỉ đọc; mọi liên kết tới invoice, hợp đồng, đơn đặt hàng mở màn tương ứng của hệ thống ERP ở tab mới.',
    'Tab Nhập khẩu bị giới hạn phạm vi theo quyền; phiếu Đã yêu cầu nhập hàng ở tab này chỉ người tạo thấy.',
    'Chỉ người tạo phiếu, khi phiếu đang Đã gửi, mới Xóa (tab Nhập khẩu) hoặc lập chứng từ tiếp theo từ phiếu.',
    'Xóa phiếu nhập khẩu xóa luôn toàn bộ dòng hàng của phiếu và trả invoice về trạng thái chưa báo hàng về.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu báo hàng về', 'Phiếu thông báo hàng mua sắp về kho, mã PBHV-NNNNN (NNNNN = số thứ tự, đủ 5 chữ số). Lập ở hệ thống '
                          'ERP; màn này dùng để tra cứu và thao tác tiếp.'),
    ('Phiếu nhập khẩu (tab Nhập khẩu)', 'Phiếu báo hàng về của hàng mua nước ngoài, gắn với 1 invoice; hợp đồng là hợp đồng mua '
                                        'nước ngoài của invoice.'),
    ('Phiếu trong nước (tab Trong nước)', 'Phiếu báo hàng về theo hợp đồng mua trong nước (mẫu hợp đồng mới).'),
    ('Phiếu mua ngoài (tab Mua ngoài)', 'Phiếu báo hàng về theo hợp đồng mua trong nước hoặc phụ lục của hợp đồng đó.'),
    ('Invoice', 'Hóa đơn thương mại của lô hàng nhập khẩu; một invoice đã có phiếu báo hàng về được đánh dấu “đã báo hàng về”.'),
    ('Trạng thái Đã gửi', 'Phiếu đã báo, chưa lập chứng từ tiếp theo. Người tạo xóa được (tab Nhập khẩu) và lập phân bổ chi phí '
                          '/ yêu cầu nhập hàng được. Nhãn vàng.'),
    ('Trạng thái Đã yêu cầu nhập hàng', 'Đã lập phiếu yêu cầu nhập hàng / phân bổ chi phí từ phiếu. Không xóa, không lập lại '
                                        'được. Nhãn xanh lá.'),
    ('Kho / Kho nhận / Kho nhập', 'Kho hàng về, hiển thị “Mã kho - Tên kho”. Phiếu nhập khẩu “Nhập thẳng” không có kho nhận.'),
    ('Nhập thẳng / Nhập xuất thẳng', 'Hàng giao thẳng, không qua kho (tab Nhập khẩu / tab Mua ngoài); hiện là ô tích chỉ đọc.'),
    ('PI, Model, Code đặt hàng', 'Số và ngày Proforma Invoice, model, mã đặt hàng (barcode) của dòng hàng nhập khẩu.'),
    ('Dòng chi tiết khách', 'Phần số lượng của một dòng hàng dành cho 1 khách hàng / đơn đặt hàng, hoặc “Tồn kho” / “Tồn kho '
                            'công ty”.'),
    ('Cấu trúc phân cấp', 'Phiếu > dòng hàng hóa > dòng chi tiết khách (khách hàng, đơn đặt hàng, SL). Phiếu nhập khẩu còn hiển '
                          'thị Khuyến mại, Hàng bảo hành, Hàng thừa thiếu của invoice; phiếu mua ngoài có bảng Khuyến mại.'),
    ('Phạm vi xem tab Nhập khẩu', 'Tập phiếu người dùng thấy ở tab Nhập khẩu theo quyền tổng công ty / công ty / phòng ban; không '
                                  'quyền thì phiếu mình tạo và phiếu có hàng thuộc thương hiệu mình đang phụ trách mua.'),
    ('NCC / HĐ / YCNH', 'Nhà cung cấp / Hợp đồng / Yêu cầu nhập hàng.'),
    ('Hệ thống ERP', 'Hệ thống quản trị cũ dùng chung cơ sở dữ liệu; các màn chưa chuyển sang được mở ở tab mới.'),
], widths=[2.1, 3.9])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn không gắn quyền xem riêng: ai vào được phân hệ Thông báo đều mở được màn. Quyền chỉ quyết định phạm vi dữ liệu của '
    'tab Nhập khẩu. Các thao tác ghi gắn với người tạo phiếu, không gắn quyền.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('—', '(Không có quyền thao tác riêng)', 'Xem, tìm kiếm, xuất Excel danh sách, xem chi tiết, in, xuất Excel một phiếu: mọi '
                                            'người dùng trong phạm vi xem. Xóa, Tạo phân bổ chi phí, Tạo (phiếu) yêu cầu nhập '
                                            'hàng: chỉ người tạo phiếu, phiếu Đã gửi.'),
], widths=[0.8, 1.9, 3.3])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (chỉ áp cho tab Nhập khẩu; xét từ trên xuống, có cấp nào áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu báo hàng về mua nhập khẩu theo tổng công ty', 'Toàn bộ phiếu nhập khẩu.'),
    ('V2', 'Xem phiếu báo hàng về mua nhập khẩu theo công ty', 'Phiếu thuộc công ty người dùng đang chọn làm việc; chưa chọn '
                                                             'công ty thì không thấy phiếu nào.'),
    ('V3', 'Xem phiếu báo hàng về mua nhập khẩu theo phòng ban', 'Phiếu thuộc các phòng ban người dùng quản lý.'),
    ('—', '(không có quyền nào)', 'Phiếu mình tạo, cộng phiếu có hàng hóa / hàng bảo hành / hàng khuyến mại thuộc cặp thương hiệu '
                                  '– hãng mà mình đang phụ trách mua ở công ty đang chọn.'),
], widths=[0.8, 2.4, 2.8])
d.p('Mọi cấp: phiếu nhập khẩu ở trạng thái Đã yêu cầu nhập hàng chỉ người tạo thấy. Tab Trong nước và Mua ngoài không giới hạn '
    'phạm vi: ai vào màn cũng thấy toàn bộ phiếu.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người tạo phiếu', 'V1', 'V2', 'V3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách tab Nhập khẩu', '✅', '✅ (tất cả)', '✅ (công ty)', '✅ (phòng ban)', '✅ (của mình + thương hiệu phụ trách)'),
    ('FR-02 Xem danh sách tab Trong nước', '✅', '✅', '✅', '✅', '✅ (tất cả)'),
    ('FR-03 Xem danh sách tab Mua ngoài', '✅', '✅', '✅', '✅', '✅ (tất cả)'),
    ('FR-04 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 Tùy chỉnh cột hiển thị', '✅', '✅', '✅', '✅', '✅'),
    ('FR-07 Xuất Excel danh sách', '✅', '✅', '✅', '✅', '✅ (trong phạm vi)'),
    ('FR-08 Xem chi tiết phiếu nhập khẩu', '✅', '✅', '✅', '✅', '✅ (trong phạm vi)'),
    ('FR-09 Xem chi tiết phiếu trong nước', '✅', '✅', '✅', '✅', '✅'),
    ('FR-10 Xem chi tiết phiếu mua ngoài', '✅', '✅', '✅', '✅', '✅'),
    ('FR-11 Xóa phiếu nhập khẩu', '✅ (Đã gửi)', '❌', '❌', '❌', '❌'),
    ('FR-12 In phiếu nhập khẩu', '✅', '✅', '✅', '✅', '✅ (trong phạm vi)'),
    ('FR-13 Xuất Excel một phiếu nhập khẩu', '✅', '✅', '✅', '✅', '✅ (trong phạm vi)'),
    ('FR-14 Tạo phân bổ chi phí', '✅ (Đã gửi)', '❌', '❌', '❌', '❌'),
    ('FR-15 Tạo phiếu yêu cầu nhập hàng', '✅ (Đã gửi)', '❌', '❌', '❌', '❌'),
], widths=[2.0, 0.9, 0.7, 0.8, 0.8, 1.2])
d.p('Màn không có chức năng Thêm mới, Chỉnh sửa, Duyệt / Không duyệt, Khóa / Mở khóa, Import Excel và Lịch sử thay đổi nên ma '
    'trận không có các dòng tương ứng. Xuất Excel, In, Xem chi tiết không gắn quyền riêng: ai xem được phiếu thì dùng được.')
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có quyền V1–V3: tab Nhập khẩu chỉ hiện phiếu mình tạo và phiếu có hàng thuộc thương hiệu mình đang phụ trách mua; '
    '2 tab còn lại vẫn thấy toàn bộ.',
    'Nút không đủ điều kiện thì ẩn hẳn, không hiện xám (Xóa, Tạo phân bổ chi phí, Tạo (phiếu) yêu cầu nhập hàng).',
    'Mở thẳng đường dẫn màn chi tiết của phiếu nhập khẩu ngoài phạm vi, hoặc phiếu không tồn tại → chuyển sang trang ' + M_404 + '.',
    'Gọi thẳng chức năng Xóa bỏ qua giao diện khi không phải người tạo hoặc phiếu không còn Đã gửi → hệ thống từ chối với thông '
    'báo ' + MSG_409 + ', phiếu giữ nguyên.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Nút / thao tác', 'Hiện khi', 'Vị trí'], [
    ('Xuất Excel, Cấu hình cột hiển thị', 'Luôn hiện ở cả 3 tab', 'Thanh công cụ của bảng'),
    ('Cột Hành động (Xóa, In, Xuất Excel)', 'Chỉ tab Nhập khẩu', 'Cuối mỗi dòng'),
    ('Xóa', 'Người đăng nhập là người tạo phiếu và phiếu Đã gửi', 'Cột Hành động, chân màn chi tiết Nhập khẩu'),
    ('In, Xuất Excel một phiếu', 'Luôn hiện với phiếu nhập khẩu xem được', 'Cột Hành động, chân màn chi tiết Nhập khẩu'),
    ('Tạo phân bổ chi phí', 'Người tạo phiếu, phiếu nhập khẩu Đã gửi', 'Chân màn chi tiết Nhập khẩu'),
    ('Tạo yêu cầu nhập hàng', 'Người tạo phiếu, phiếu trong nước Đã gửi', 'Chân màn chi tiết Trong nước'),
    ('Tạo phiếu yêu cầu nhập hàng', 'Người tạo phiếu, phiếu mua ngoài Đã gửi', 'Chân màn chi tiết Mua ngoài'),
], widths=[1.8, 2.8, 1.8])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_ND, [0, 1, 2, 3, 4, 5]), (A_TAO, [0, 6, 7, 8])],
    [('FR-01', 'Xem danh sách tab Nhập khẩu', 'view'),
     ('FR-02', 'Xem danh sách tab Trong nước', 'view'),
     ('FR-03', 'Xem danh sách tab Mua ngoài', 'view'),
     ('FR-07', 'Xuất Excel danh sách', 'io'),
     ('FR-12', 'In phiếu nhập khẩu', 'io'),
     ('FR-13', 'Xuất Excel một phiếu', 'io'),
     ('FR-11', 'Xóa phiếu nhập khẩu', 'action'),
     ('FR-14', 'Tạo phân bổ chi phí', 'action'),
     ('FR-15', 'Tạo phiếu yêu cầu nhập hàng', 'action')],
    [('FR-04', 'Tìm kiếm và lọc', 'view', 'extend', [0, 1, 2], None),
     ('FR-05', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-06', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-08', 'Xem chi tiết phiếu nhập khẩu', 'view', 'extend', [0], None),
     ('FR-09', 'Xem chi tiết phiếu trong nước', 'view', 'extend', [1], None),
     ('FR-10', 'Xem chi tiết phiếu mua ngoài', 'view', 'extend', [2], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu báo hàng về')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách tab Nhập khẩu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập màn Phiếu báo hàng về và xem danh sách tab Nhập khẩu',
       mota='Mở màn Phiếu báo hàng về (mặc định ở tab Nhập khẩu) và hiển thị bảng phiếu báo hàng về của hàng mua nước ngoài '
            'nằm trong phạm vi xem của người đăng nhập, kèm phân trang, sắp xếp và tổng số phiếu khớp bộ lọc. Mỗi dòng là một '
            'phiếu gắn với 1 invoice; cuối dòng có cột Hành động (Xóa, In, Xuất Excel).',
       tacnhan=TN_IMP,
       dieukien='1. Người dùng đăng nhập thành công.\n'
                '2. Người dùng vào được phân hệ Thông báo (không cần quyền riêng để mở màn).\n'
                '3. Phạm vi dữ liệu tab Nhập khẩu xác định theo quyền V1 → V2 → V3 (Phần 2).',
       chinh='1. Người dùng vào menu theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống mở màn “Phiếu báo hàng về”, chọn tab Nhập khẩu (hoặc đúng tab đang ghi trên đường dẫn trình duyệt).\n'
             '3. Hệ thống xác định phạm vi xem theo thứ tự V1 → V2 → V3; không có cấp nào thì lấy phiếu mình tạo và phiếu có hàng '
             'thuộc thương hiệu mình đang phụ trách mua.\n'
             '4. Hệ thống loại bỏ phiếu Đã yêu cầu nhập hàng của người khác.\n'
             '5. Hệ thống khôi phục bộ lọc của tab đã dùng trong 10 phút gần nhất (nếu có) và cấu hình cột của người dùng.\n'
             '6. Hệ thống trả về trang 1, phiếu tạo gần nhất xếp trên, kèm tổng số phiếu; dòng “Hiển thị a–b / N” hiện đúng '
             'khoảng và tổng.',
       phu='• Không có phiếu nào trong phạm vi → bảng hiện “Không có dữ liệu phù hợp.”, dưới bảng “Không có phiếu nào.”.\n'
           '• Người dùng có quyền V2 nhưng chưa chọn công ty làm việc → bảng rỗng.\n'
           '• Bấm tab Trong nước / Mua ngoài → chuyển tab (mục 2.2, 2.3); đường dẫn trình duyệt ghi tab đang chọn nên tải lại '
           'trang (F5) vẫn đúng tab.\n'
           '• Bấm mã invoice / mã hợp đồng → mở màn invoice / hợp đồng mua nước ngoài của hệ thống ERP ở tab mới.\n'
           '• Máy chủ lỗi → hiển thị “Lỗi khi tải dữ liệu”.\n'
           '• Phiên đăng nhập hết hạn → hiển thị “Phiên đăng nhập đã hết hạn”, điều hướng về màn đăng nhập.',
       dacbiet='Cột mặc định hiển thị (10): STT, Mã, Ngày tạo, Kho, Nhà cung cấp, Invoice, Hợp đồng, Người tạo, Trạng thái, '
               'Hành động. Không có cột mặc định ẩn. Cột bắt buộc: STT, Mã (ghim trái, không ẩn, không đổi vị trí), Hành động '
               '(không ẩn, kéo đổi vị trí được). Mặc định 10 dòng/trang, phiếu tạo gần nhất xếp trên. Bảng cuộn ngang khi màn '
               'hẹp, cột STT và Mã đứng yên.'),
   layout=dict(entries=[
       (M_IMP, 'Hiển thị: tiêu đề bảng “Phiếu báo hàng về nhập khẩu”; phiếu nhập khẩu trong phạm vi quyền (Phần 2). Đây là tab '
               'MẶC ĐỊNH khi vào màn từ menu.')],
       shot=shot('01_list'), shot_caption='Màn Phiếu báo hàng về — tab Nhập khẩu'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '“Phiếu báo hàng về”', '- Ở thanh trên cùng, cũng là tiêu đề tab trình duyệt'),
       ('Thanh tab', 'Button', 'Enable', 'Danh sách 3 tab', 'Nhập khẩu',
        ['- Mặc định: Nhập khẩu', '- Nhập khẩu (biểu tượng tàu)', '- Trong nước (biểu tượng xe tải)', '- Mua ngoài (biểu tượng giỏ hàng)',
         '- Tab đang chọn nền xanh nhạt', '- Bấm tab → nạp danh sách của tab đó, mỗi tab bộ cột, bộ lọc, cấu hình riêng']),
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', '“Phiếu báo hàng về nhập khẩu”', '- Đầu khối bảng, kèm biểu tượng tài liệu'),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.7)', '- Khóa trong lúc đang xuất']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
        ['- Biểu tượng cột, chữ gợi ý “Cấu hình cột hiển thị”', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.6)']),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Số thứ tự liên tục giữa các trang', '- Ghim bên trái; khóa trong Tùy chỉnh cột']),
       ('Cột Mã', 'Table/Grid', 'Read-only', 'PBHV-NNNNN', 'Theo dữ liệu',
        ['- Bấm mã → mở màn chi tiết phiếu nhập khẩu (mục 2.8); chuột phải mở được ở tab mới', '- Sắp xếp được',
         '- Ghim bên trái; khóa trong Tùy chỉnh cột']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
        ['- Thời điểm tạo phiếu', '- Sắp xếp được; mặc định phiếu mới xếp trên']),
       ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Kho nhận dạng “Mã kho - Tên kho”', '- Trống khi phiếu Nhập thẳng', '- Tối đa 2 dòng, rê chuột xem đủ', '- Không sắp xếp']),
       ('Cột Nhà cung cấp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Nhà cung cấp của invoice, dạng “Mã - Tên”', '- Trống khi phiếu chưa gắn invoice hoặc invoice chưa có nhà cung cấp',
         '- Tối đa 2 dòng, rê chuột xem đủ', '- Không sắp xếp']),
       ('Cột Invoice', 'Link', 'Read-only', '–', 'Theo dữ liệu',
        ['- Mã invoice của phiếu', '- Bấm → mở màn invoice của hệ thống ERP ở tab mới', '- Không sắp xếp']),
       ('Cột Hợp đồng', 'Link', 'Read-only', '–', 'Theo dữ liệu',
        ['- Mã hợp đồng mua nước ngoài của invoice', '- Bấm → mở hợp đồng ở hệ thống ERP, tab mới', '- Không sắp xếp']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Họ tên người tạo phiếu', '- Không sắp xếp']),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu', STATUS_LIST + ['- Không sắp xếp']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo người tạo và trạng thái',
        ['- Nút Xóa (thùng rác đỏ): chỉ hiện với người tạo, phiếu Đã gửi; bấm → hộp Xác nhận xóa (mục 2.11)',
         '- Nút In (máy in): luôn hiện; bấm → cửa sổ xem trước bản in (mục 2.12)',
         '- Nút Xuất Excel (biểu tượng Excel): luôn hiện, tải file của phiếu (mục 2.13)',
         '- Nút không dùng được thì ẩn hẳn', '- Chỉ có ở tab Nhập khẩu; không bỏ tích được trong Tùy chỉnh cột']),
   ] + PAGE_ROWS('Nhập khẩu'),
   ev=[('Mở màn hình', 'System',
        'Before:\n– Đọc tab trên đường dẫn trình duyệt; không có hoặc giá trị lạ thì chọn tab Nhập khẩu.\n'
        '– Xác định cấp quyền xem theo thứ tự V1 → V2 → V3; không có cấp nào thì giới hạn ở phiếu mình tạo và phiếu có hàng '
        'thuộc thương hiệu mình phụ trách mua.\n'
        'During:\n– Khôi phục bộ lọc của tab Nhập khẩu đã lưu trong 10 phút gần nhất (nếu có), nạp cấu hình cột, danh mục Kho, '
        'Trạng thái.\n'
        '– Áp phạm vi dữ liệu; loại bỏ phiếu Đã yêu cầu nhập hàng của người khác.\n'
        'After:\n– Trả về trang 1, sắp xếp theo ngày tạo giảm dần, kèm tổng số phiếu.\n'
        '– Lỗi máy chủ → hiển thị “Lỗi khi tải dữ liệu”.'),
       ('Bấm tab Trong nước hoặc Mua ngoài', 'Click',
        'Before:\n– Bấm đúng tab đang chọn thì không làm gì.\n'
        'During:\n– Ghi tab mới lên đường dẫn trình duyệt (thay thế, không thêm lịch sử).\n'
        'After:\n– Dựng lại danh sách của tab mới với bộ cột, bộ lọc, cấu hình cột riêng của tab đó (mục 2.2, 2.3).'),
       ('Bấm mã phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem (đã lọc ở bước nạp danh sách).\n'
        'During:\n– Chuột phải cho phép mở ở tab mới.\n'
        'After:\n– Mở màn chi tiết phiếu nhập khẩu (mục 2.8).'),
       ('Bấm mã Invoice hoặc mã Hợp đồng', 'Click',
        'Before:\n– Ô có mã; ô trống không bấm được.\n'
        'During:\n– Xác định màn invoice / hợp đồng mua nước ngoài của hệ thống ERP.\n'
        'After:\n– Mở màn đó ở tab trình duyệt mới; màn danh sách giữ nguyên.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ 2 cột Mã, Ngày tạo sắp xếp được.\n'
        'During:\n– Đổi chiều sắp xếp tăng / giảm; giữ nguyên bộ lọc; ghi nhớ chiều sắp xếp cùng bộ lọc.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Bấm số trang hoặc nút tiến lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng; bấm đúng trang đang xem thì không nạp lại.\n'
        'During:\n– Nạp dữ liệu của trang được chọn.\n'
        'After:\n– Hiển thị trang mới, STT tiếp tục liên tục, dòng “Hiển thị a–b / N” cập nhật.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Chọn 1 trong 5, 10, 20, 50, 100.\nDuring:\n– Ghi nhận số dòng mới.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách theo số dòng mới.')])

# ------------------------------------------------------------ 2.2
fr(2, 'Xem danh sách tab Trong nước',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Xem danh sách phiếu báo hàng về trong nước',
       mota='Hiển thị toàn bộ phiếu báo hàng về theo hợp đồng mua trong nước (mẫu hợp đồng mới). Tab không giới hạn phạm vi '
            'theo quyền như hệ thống ERP: ai vào màn cũng thấy toàn bộ phiếu. Tab chỉ đọc, không có cột Hành động; thao tác '
            'tiếp với phiếu làm ở màn chi tiết (mục 2.9).',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm tab Trong nước.\n'
             '2. Hệ thống khôi phục bộ lọc riêng của tab đã dùng trong 10 phút gần nhất (nếu có) và cấu hình cột riêng của tab.\n'
             '3. Hệ thống lấy toàn bộ phiếu trong nước khớp bộ lọc, không áp phạm vi quyền.\n'
             '4. Hệ thống trả về trang 1, phiếu tạo gần nhất xếp trên, kèm tổng số phiếu.',
       phu='• Chưa có phiếu trong nước nào (hiện trạng dữ liệu 03/11/2026) → bảng “Không có dữ liệu phù hợp.”, dưới bảng “Không '
           'có phiếu nào.”.\n'
           '• Bấm mã hợp đồng → mở hợp đồng mua trong nước của hệ thống ERP ở tab mới.\n'
           '• Bộ lọc tab này không có ô Ngày tạo (như hệ thống ERP).\n'
           '• Máy chủ lỗi → “Lỗi khi tải dữ liệu”; hết phiên → “Phiên đăng nhập đã hết hạn”, về màn đăng nhập.',
       dacbiet='Cột mặc định hiển thị (7): STT, Mã, Ngày tạo, Hợp đồng, Nhà cung cấp, Kho, Trạng thái. Không có cột ẩn. Cột bắt '
               'buộc: STT, Mã. Sắp xếp được: Mã, Ngày tạo. Mặc định 10 dòng/trang.'),
   layout=dict(menu=M_INL, shot=shot('01b_list_inland'), shot_caption='Tab Trong nước — chưa có phiếu nào',
               note='Hiển thị: tiêu đề bảng “Phiếu báo hàng về trong nước”; toàn bộ phiếu trong nước, không giới hạn theo quyền.'),
   ui_kw=dict(required=False),
   ui=[
       ('Tab Trong nước', 'Button', 'Enable', '–', 'Hiển thị', ['- Biểu tượng xe tải', '- Đang chọn: nền xanh nhạt']),
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', '“Phiếu báo hàng về trong nước”', '- Đầu khối bảng'),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', ['- Bấm → cửa sổ Chọn trường xuất file, 6 trường (mục 2.7)']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', ['- Bấm → cửa sổ Tuỳ chỉnh cột của tab (mục 2.6)']),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Liên tục giữa các trang', '- Ghim trái, khóa']),
       ('Cột Mã', 'Table/Grid', 'Read-only', 'PBHV-NNNNN', 'Theo dữ liệu',
        ['- Bấm mã → màn chi tiết phiếu trong nước (mục 2.9)', '- Sắp xếp được', '- Ghim trái, khóa']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', ['- Sắp xếp được; mặc định mới nhất trên']),
       ('Cột Hợp đồng', 'Link', 'Read-only', '–', 'Theo dữ liệu',
        ['- Mã hợp đồng mua trong nước của phiếu', '- Bấm → mở hợp đồng ở hệ thống ERP, tab mới']),
       ('Cột Nhà cung cấp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Nhà cung cấp của phiếu, dạng “Mã - Tên”', '- Tối đa 2 dòng']),
       ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- “Mã kho - Tên kho”', '- Tối đa 2 dòng']),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu', STATUS_LIST),
   ] + PAGE_ROWS('Trong nước'),
   ev=[('Bấm tab Trong nước', 'Click',
        'Before:\n– Không giới hạn phạm vi theo quyền.\n'
        'During:\n– Khôi phục bộ lọc riêng của tab (trong 10 phút), nạp cấu hình cột của tab, nạp dữ liệu.\n'
        'After:\n– Hiển thị trang 1, sắp xếp ngày tạo giảm dần; rỗng → “Không có dữ liệu phù hợp.”.'),
       ('Bấm mã phiếu', 'Click',
        'Before:\n– Mọi phiếu trong nước đều xem được.\nDuring:\n– Chuột phải mở được ở tab mới.\n'
        'After:\n– Mở màn chi tiết phiếu trong nước (mục 2.9).'),
       ('Bấm mã Hợp đồng', 'Click',
        'Before:\n– Ô có mã hợp đồng.\nDuring:\n– Xác định màn hợp đồng mua trong nước của hệ thống ERP.\n'
        'After:\n– Mở ở tab trình duyệt mới.'),
       ('Bấm tiêu đề cột Mã hoặc Ngày tạo', 'Click',
        'Before:\n– Chỉ 2 cột này sắp xếp được.\nDuring:\n– Đổi chiều tăng / giảm, giữ bộ lọc.\n'
        'After:\n– Về trang 1, nạp lại.'),
       ('Đổi trang hoặc Số dòng/trang', 'Click',
        'Before:\n– Giữ bộ lọc, sắp xếp.\nDuring:\n– Nạp trang được chọn (đổi số dòng thì về trang 1).\n'
        'After:\n– Cập nhật bảng và dòng “Hiển thị a–b / N”.')])

# ------------------------------------------------------------ 2.3
fr(3, 'Xem danh sách tab Mua ngoài',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Xem danh sách phiếu báo hàng về mua ngoài',
       mota='Hiển thị toàn bộ phiếu báo hàng về theo hợp đồng mua trong nước hoặc theo phụ lục của hợp đồng đó. Tab không giới '
            'hạn phạm vi theo quyền như hệ thống ERP; cột Hợp đồng hiện mã phụ lục khi phiếu lập theo phụ lục. Tab chỉ đọc, '
            'không có cột Hành động; lập phiếu yêu cầu nhập hàng làm ở màn chi tiết (mục 2.10, 2.15).',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm tab Mua ngoài.\n'
             '2. Hệ thống khôi phục bộ lọc riêng của tab (trong 10 phút) và cấu hình cột riêng của tab.\n'
             '3. Hệ thống lấy toàn bộ phiếu mua ngoài khớp bộ lọc, không áp phạm vi quyền.\n'
             '4. Hệ thống trả về trang 1, phiếu tạo gần nhất xếp trên, kèm tổng số phiếu.',
       phu='• Phiếu theo phụ lục: cột Hợp đồng hiện mã phụ lục, bấm mở phụ lục; phiếu theo hợp đồng: hiện mã hợp đồng.\n'
           '• Không có phiếu khớp → “Không có dữ liệu phù hợp.”.\n'
           '• Phiếu Đã yêu cầu nhập hàng của mọi người đều hiện (khác tab Nhập khẩu).\n'
           '• Máy chủ lỗi → “Lỗi khi tải dữ liệu”; hết phiên → “Phiên đăng nhập đã hết hạn”, về màn đăng nhập.',
       dacbiet='Cột mặc định hiển thị (7): STT, Mã, Ngày tạo, Kho, Hợp đồng, Nhà cung cấp, Trạng thái. Không có cột ẩn. Cột bắt '
               'buộc: STT, Mã. Sắp xếp được: Mã, Ngày tạo. Mặc định 10 dòng/trang.'),
   layout=dict(menu=M_OUT, shot=shot('01c_list_outside'), shot_caption='Tab Mua ngoài',
               note='Hiển thị: tiêu đề bảng “Phiếu báo hàng về mua ngoài”; toàn bộ phiếu mua ngoài, không giới hạn theo quyền.'),
   ui_kw=dict(required=False),
   ui=[
       ('Tab Mua ngoài', 'Button', 'Enable', '–', 'Hiển thị', ['- Biểu tượng giỏ hàng', '- Đang chọn: nền xanh nhạt']),
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', '“Phiếu báo hàng về mua ngoài”', '- Đầu khối bảng'),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', ['- Bấm → cửa sổ Chọn trường xuất file, 6 trường (mục 2.7)']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', ['- Bấm → cửa sổ Tuỳ chỉnh cột của tab (mục 2.6)']),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Liên tục giữa các trang', '- Ghim trái, khóa']),
       ('Cột Mã', 'Table/Grid', 'Read-only', 'PBHV-NNNNN', 'Theo dữ liệu',
        ['- Bấm mã → màn chi tiết phiếu mua ngoài (mục 2.10)', '- Sắp xếp được', '- Ghim trái, khóa']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', ['- Sắp xếp được; mặc định mới nhất trên']),
       ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- “Mã kho - Tên kho”', '- Trống khi phiếu chưa chọn kho']),
       ('Cột Hợp đồng', 'Link', 'Read-only', '–', 'Theo dữ liệu',
        ['- Mã phụ lục (phiếu theo phụ lục) hoặc mã hợp đồng mua trong nước', '- Bấm → mở phụ lục / hợp đồng ở hệ thống ERP, tab mới']),
       ('Cột Nhà cung cấp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Dạng “<mã hợp đồng hoặc phụ lục> - <tên nhà cung cấp ghi trên hợp đồng>”', '- Tối đa 2 dòng']),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu', STATUS_LIST),
   ] + PAGE_ROWS('Mua ngoài'),
   ev=[('Bấm tab Mua ngoài', 'Click',
        'Before:\n– Không giới hạn phạm vi theo quyền.\n'
        'During:\n– Khôi phục bộ lọc riêng của tab (trong 10 phút), nạp cấu hình cột của tab, nạp dữ liệu.\n'
        'After:\n– Hiển thị trang 1, sắp xếp ngày tạo giảm dần, tổng số phiếu.'),
       ('Bấm mã phiếu', 'Click',
        'Before:\n– Mọi phiếu mua ngoài đều xem được.\nDuring:\n– Chuột phải mở được ở tab mới.\n'
        'After:\n– Mở màn chi tiết phiếu mua ngoài (mục 2.10).'),
       ('Bấm mã Hợp đồng', 'Click',
        'Before:\n– Ô có mã.\nDuring:\n– Phiếu theo phụ lục → màn phụ lục; ngược lại → màn hợp đồng mua trong nước (hệ thống ERP).\n'
        'After:\n– Mở ở tab trình duyệt mới.'),
       ('Bấm tiêu đề cột Mã hoặc Ngày tạo', 'Click',
        'Before:\n– Chỉ 2 cột này sắp xếp được.\nDuring:\n– Đổi chiều tăng / giảm, giữ bộ lọc.\nAfter:\n– Về trang 1, nạp lại.'),
       ('Đổi trang hoặc Số dòng/trang', 'Click',
        'Before:\n– Giữ bộ lọc, sắp xếp.\nDuring:\n– Nạp trang được chọn (đổi số dòng thì về trang 1).\n'
        'After:\n– Cập nhật bảng và dòng “Hiển thị a–b / N”.')])

# ------------------------------------------------------------ 2.4
fr(4, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(ten='Tìm kiếm và lọc danh sách phiếu báo hàng về',
              mota='Thu hẹp danh sách của tab đang xem theo mã phiếu (ô tìm nhanh) và các tiêu chí của khối Tìm kiếm nâng cao. '
                   'Mỗi tab có bộ tiêu chí riêng đúng như hệ thống ERP: Nhập khẩu 10 tiêu chí, Trong nước 6 tiêu chí, Mua ngoài '
                   '9 tiêu chí (Công ty, Phòng ban, Bộ phận tính riêng). Kết quả luôn nằm trong phạm vi xem của tab.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng nhập mã phiếu vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
                    '2. Hoặc bấm Tìm kiếm nâng cao để mở khối tiêu chí, chọn / nhập giá trị một hoặc nhiều tiêu chí.\n'
                    '3. Ô dạng chọn (Nhà cung cấp, Kho, Người tạo, Trạng thái, Công ty, Phòng ban, Bộ phận, Ngày tạo) lọc ngay khi '
                    'đổi giá trị.\n'
                    '4. Ô gõ tay (Invoice, Hợp đồng, Tên, mã hàng, Tên hàng, Mã hàng, Model, Barcode) chỉ lọc khi bấm Tìm kiếm '
                    'hoặc Enter trong ô.\n'
                    '5. Hệ thống quay về trang 1 và nạp lại danh sách; bộ lọc của tab được ghi nhớ 10 phút trên trình duyệt.',
              phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh và chiều sắp xếp, nạp lại từ trang 1.\n'
                  '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
                  '• Ô Nhà cung cấp: gõ từ 1 ký tự mới gợi ý, tối đa 30 đối tác đang hoạt động khớp mã hoặc tên.\n'
                  '• Tab Mua ngoài: đổi Công ty → xóa Phòng ban, Bộ phận đang chọn; mọi người chọn được mọi công ty.\n'
                  '• Tiêu chí bị tắt trong Cài đặt bộ lọc → không hiện ở khối nâng cao.\n'
                  '• Bộ lọc nhớ RIÊNG từng tab; trong 10 phút kể từ lần đổi cuối, vào lại màn (kể cả tải lại trang, sang màn '
                  'khác rồi quay lại, mở tab trình duyệt mới) vẫn giữ bộ lọc, chiều sắp xếp, trạng thái mở khối nâng cao.',
              dacbiet='Kiểu khớp: ô tìm nhanh (mã phiếu) và mọi ô gõ tay khớp MỘT PHẦN (chuỗi chứa), không phân biệt hoa / thường, '
                      'tự bỏ khoảng trắng đầu / cuối; ký tự % và _ được hiểu là ký tự đại diện. Ô dạng chọn khớp CHÍNH XÁC. Các ô '
                      'gõ không giới hạn số ký tự. Ô Ngày tạo lấy trọn 2 ngày biên. Bộ lọc ghi nhớ theo trình duyệt, không theo '
                      'tài khoản.'),
   layout=dict(menu=M_IMP + ' => Tìm kiếm nâng cao', shot=shot('02_filter'), shot_caption='Khối Bộ lọc danh sách — tab Nhập khẩu',
               extra=[(shot('02b_filter_inland'), 'Khối Bộ lọc danh sách — tab Trong nước'),
                      (shot('02c_filter_outside'), 'Khối Bộ lọc danh sách — tab Mua ngoài')]),
   ui=[('Tiêu đề khối', 'Label', 'Hiển thị', '–', '–', '“Bộ lọc danh sách”', '- Kèm biểu tượng phễu lọc'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo mã phiếu”', '- Tìm theo một phần mã phiếu', '- Chỉ lọc khi bấm Tìm kiếm hoặc Enter',
         '- Có nút × xóa nhanh khi đã nhập']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp giá trị ô tìm nhanh và các ô gõ tay, về trang 1, nạp lại.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Xóa toàn bộ tiêu chí kể cả ô tìm nhanh, nhà cung cấp đã chọn, chiều sắp xếp', '- Nạp lại từ trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Mở / thu gọn khối tiêu chí', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc của tab (mục 2.5).'),
       ('Nhà cung cấp', 'Dropdown', 'Enable', 'Gõ tối thiểu 1 ký tự', 'Không', 'Trống',
        ['- Có ở cả 3 tab', '- Gợi ý dạng “Mã - Tên”, tối đa 30 đối tác đang hoạt động',
         '- Nhập khẩu: lọc theo nhà cung cấp của invoice; Trong nước: nhà cung cấp của phiếu; Mua ngoài: nhà cung cấp của phụ lục '
         '(phiếu theo phụ lục) hoặc của hợp đồng']),
       ('Invoice', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Chỉ tab Nhập khẩu', '- Một phần mã invoice', '- Lọc khi bấm Tìm kiếm / Enter']),
       ('Hợp đồng', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Có ở cả 3 tab, khớp một phần mã hợp đồng', '- Nhập khẩu: hợp đồng của invoice',
         '- Mua ngoài: mã hợp đồng gốc (kể cả phiếu lập theo phụ lục)', '- Lọc khi bấm Tìm kiếm / Enter']),
       ('Tên, mã hàng', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Tab Nhập khẩu và Mua ngoài', '- Phiếu có ít nhất 1 dòng hàng có tên hoặc mã chứa chuỗi gõ']),
       ('Tên hàng', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống', ['- Chỉ tab Trong nước', '- Một phần tên hàng của dòng hàng']),
       ('Mã hàng', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống', ['- Chỉ tab Trong nước', '- Một phần mã hàng của dòng hàng']),
       ('Kho', 'Dropdown', 'Enable', 'Danh sách kho', 'Không', 'Trống',
        ['- Có ở cả 3 tab', '- Mặc định: trống (tất cả)', '- Lựa chọn: mọi kho, dạng “Mã - Tên”, xếp theo mã kho']),
       ('Model', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống', ['- Chỉ tab Nhập khẩu', '- Một phần model của dòng hàng']),
       ('Barcode', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Chỉ tab Nhập khẩu', '- Một phần Code đặt hàng của dòng hàng']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Chỉ tab Nhập khẩu', '- Mặc định: trống (tất cả)', '- Chọn 1 nhân viên']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
        ['- Có ở cả 3 tab', '- Mặc định: trống (tất cả)', '- Đã yêu cầu nhập hàng', '- Đã gửi']),
       ('Công ty', 'Dropdown', 'Enable', 'Danh sách công ty', 'Không', 'Trống',
        ['- Chỉ tab Mua ngoài', '- Mặc định: trống, gợi ý “Chọn công ty”', '- Mọi người chọn được mọi công ty',
         '- Đổi giá trị → xóa Phòng ban, Bộ phận đang chọn']),
       ('Phòng ban', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Không', 'Trống',
        ['- Chỉ tab Mua ngoài', '- Mặc định: trống, gợi ý “Chọn phòng ban”', '- Chọn Công ty thì chỉ còn phòng ban của công ty đó']),
       ('Bộ phận', 'Dropdown', 'Enable', 'Danh sách bộ phận', 'Không', 'Trống',
        ['- Chỉ tab Mua ngoài', '- Mặc định: trống, gợi ý “Chọn bộ phận”', '- Bộ phận của phòng ban đang chọn']),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Tab Nhập khẩu và Mua ngoài (tab Trong nước không có)', '- 1 ô gồm 2 lịch Từ ngày → Đến ngày',
         '- Lấy trọn cả 2 ngày biên']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện “Không có dữ liệu phù hợp.” khi không có kết quả.')],
   ev=[('Đổi giá trị ô dạng chọn', 'Change',
        'Before:\n– Áp cho Nhà cung cấp, Kho, Người tạo, Trạng thái, Công ty, Phòng ban, Bộ phận, Ngày tạo.\n'
        'During:\n– Ghi nhận giá trị mới vào bộ lọc của tab; ghi nhớ bộ lọc trên trình duyệt (10 phút).\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí đang có.'),
       ('Bấm Tìm kiếm hoặc Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh và các ô gõ tay đang nhập.\n'
        'During:\n– Gộp với các tiêu chí đang chọn; máy chủ bỏ khoảng trắng đầu / cuối.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Không hỏi xác nhận.\n'
        'During:\n– Đặt lại toàn bộ tiêu chí về trống, bỏ nhà cung cấp đã chọn, bỏ chiều sắp xếp.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Gõ ô Nhà cung cấp', 'Change',
        'Before:\n– Gợi ý khi gõ từ 1 ký tự.\n'
        'During:\n– Tìm đối tác đang hoạt động có mã hoặc tên chứa chuỗi gõ (tối đa 30).\n'
        'After:\n– Hiển thị gợi ý “Mã - Tên”; chọn 1 dòng thì lọc ngay, ghi nhớ tên đã chọn.'),
       ('Đổi Công ty (tab Mua ngoài)', 'Change',
        'Before:\n– Chỉ tab Mua ngoài.\nDuring:\n– Xóa Phòng ban, Bộ phận đang chọn.\n'
        'After:\n– Nạp danh sách phòng ban của công ty mới và nạp lại danh sách phiếu.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối tiêu chí đang thu gọn.\nDuring:\n– Mở khối, nhãn nút đổi thành “Ẩn tìm kiếm nâng cao”.\n'
        'After:\n– Ghi nhớ trạng thái mở / thu gọn cùng bộ lọc của tab.')])

# ------------------------------------------------------------ 2.5
fr(5, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị',
              mota='Cho phép mỗi người dùng tự chọn những tiêu chí lọc muốn thấy ở khối Tìm kiếm nâng cao và sắp xếp lại thứ '
                   'tự của chúng. Cấu hình lưu theo người dùng và RIÊNG từng tab (Nhập khẩu 10 tiêu chí, Trong nước 6, Mua ngoài 7 '
                   'mục — khối Công ty – Phòng ban – Bộ phận tính là 1 mục).',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
                    '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê các tiêu chí của tab kèm ô tích, theo cấu hình đang lưu.\n'
                    '3. Người dùng tích / bỏ tích và kéo thả để đổi thứ tự.\n'
                    '4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình cho người dùng, hiển thị “Cập nhật thành công” và áp ngay lên khối Tìm kiếm nâng cao.',
              phu='• Bấm Khôi phục mặc định → tích lại đủ tiêu chí theo thứ tự gốc; phải bấm Lưu mới có hiệu lực.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không lưu thay đổi.\n'
                  '• Lưu thất bại → hiển thị “Thao tác thất bại”.\n'
                  '• Tắt bớt còn ≤ 3 ô (tính cả ô tìm nhanh) → các ô bày thẳng trên 1 hàng, nút Tìm kiếm nâng cao ẩn; nút Cài '
                  'đặt bộ lọc vẫn còn để bật lại.',
              dacbiet=None),
   layout=dict(menu=M_IMP + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc — tab Nhập khẩu',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Cài đặt bộ lọc”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách tiêu chí', 'Table/Grid', 'Enable', 'Theo tab', 'Không', 'Theo cấu hình đã lưu',
        ['- Nhập khẩu: Nhà cung cấp, Invoice, Hợp đồng, Tên, mã hàng, Kho, Model, Barcode, Người tạo, Trạng thái, Ngày tạo',
         '- Trong nước: Hợp đồng, Tên hàng, Mã hàng, Nhà cung cấp, Kho, Trạng thái',
         '- Mua ngoài: Hợp đồng, Tên, mã hàng, Kho, Nhà cung cấp, Trạng thái, Công ty – Phòng ban – Bộ phận, Ngày tạo',
         '- Mỗi mục đánh số thứ tự 1, 2, 3…']),
       ('Ô tích của tiêu chí', 'Checkbox', 'Enable', '–', 'Không', 'Theo cấu hình đã lưu',
        ['- Tích: tiêu chí hiện ở khối Tìm kiếm nâng cao', '- Bỏ tích: ẩn tiêu chí']),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo để đổi thứ tự tiêu chí.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình cho người dùng hiện tại, đóng cửa sổ, áp ngay.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích lại đủ tiêu chí, thứ tự gốc; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ; thay đổi chưa lưu bị bỏ.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”'])],
   ev=[('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Nút hiện khi khối lọc có nhiều hơn 3 ô hoặc đang có tiêu chí bị ẩn.\n'
        'During:\n– Nạp cấu hình đang lưu của người dùng cho tab đang xem.\n'
        'After:\n– Mở cửa sổ “Cài đặt bộ lọc”.'),
       ('Kéo đổi vị trí tiêu chí', 'Drag',
        'Before:\n– Kéo bằng tay nắm của dòng.\nDuring:\n– Đổi thứ tự trong cửa sổ.\n'
        'After:\n– Chưa áp lên màn hình cho tới khi bấm Lưu.'),
       ('Bỏ tích một tiêu chí', 'Change',
        'Before:\n– Áp cho mọi tiêu chí.\nDuring:\n– Ghi nhận trạng thái tích trong cửa sổ.\n'
        'After:\n– Chưa áp lên màn hình cho tới khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình gắn với người dùng đang đăng nhập và tab đang xem.\n'
        'During:\n– Ghi cấu hình; lỗi → hiển thị “Thao tác thất bại”.\n'
        'After:\n– Hiển thị “Cập nhật thành công”; khối Tìm kiếm nâng cao cập nhật ngay.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Tích lại toàn bộ tiêu chí, đưa thứ tự về thiết kế gốc.\n'
        'After:\n– Chưa lưu; phải bấm Lưu mới có hiệu lực.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Bỏ mọi thay đổi chưa lưu.\nAfter:\n– Đóng cửa sổ, khối lọc giữ nguyên.')])

# ------------------------------------------------------------ 2.6
fr(6, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Tùy chỉnh cột của bảng danh sách',
              mota='Cho phép mỗi người dùng bật / tắt và kéo sắp xếp các cột của bảng. Mỗi tab có cấu hình riêng (Nhập khẩu 10 cột, '
                   'Trong nước 7 cột, Mua ngoài 7 cột), lưu theo người dùng. Hai cột STT, Mã bị khóa; cột Hành động (tab Nhập khẩu) '
                   'luôn hiện nhưng kéo đổi vị trí được.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
                    '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê các cột của tab kèm ô tích theo cấu hình đang áp dụng.\n'
                    '3. Người dùng tích / bỏ tích, kéo biểu tượng ba gạch để đổi thứ tự.\n'
                    '4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình, hiển thị “Cập nhật thành công”, vẽ lại bảng.',
              phu='• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, danh sách cột trả về cấu hình đang áp dụng.\n'
                  '• Cột khóa (STT, Mã): ô tích xám, không bỏ tích, không kéo được; di chuột hiện “Cột bắt buộc — không thể ẩn hoặc '
                  'đổi vị trí”.\n'
                  '• Cột Hành động: ô tích xám, không bỏ tích được nhưng vẫn kéo đổi vị trí (“Cột bắt buộc — không thể ẩn, kéo để '
                  'đổi vị trí”).\n'
                  '• Lưu thất bại → hiển thị “Thao tác thất bại”.\n'
                  '• Cấu hình lưu trên máy chủ theo tài khoản: giữ sau khi tải lại (F5), đổi trình duyệt / máy khác vẫn giữ; tài '
                  'khoản khác không bị ảnh hưởng.\n'
                  '• Đổi cột không làm thay đổi dữ liệu, tổng số phiếu, bộ lọc đang áp.',
              dacbiet='Không có cột mặc định ẩn: lần đầu mọi cột đều tích. Cột STT, Mã ghim trái khi cuộn ngang.'),
   layout=dict(menu=M_IMP + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột — tab Nhập khẩu',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Tuỳ chỉnh cột”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Tích chọn cột cần hiển thị, kéo ≡ để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Theo tab', '–', 'Theo cấu hình',
        ['- Nhập khẩu: STT, Mã (khóa), Ngày tạo, Kho, Nhà cung cấp, Invoice, Hợp đồng, Người tạo, Trạng thái, Hành động',
         '- Trong nước: STT, Mã (khóa), Ngày tạo, Hợp đồng, Nhà cung cấp, Kho, Trạng thái',
         '- Mua ngoài: STT, Mã (khóa), Ngày tạo, Kho, Hợp đồng, Nhà cung cấp, Trạng thái']),
       ('Ô tích của cột', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Theo cấu hình',
        ['- Tích: cột hiện trên bảng', '- Cột STT, Mã, Hành động: ô tích xám, không bỏ được']),
       ('Biểu tượng ba gạch', 'Icon Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Kéo để đổi vị trí cột', '- Cột STT, Mã hiện biểu tượng ổ khóa, không kéo được']),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi cột (trừ cột khóa).'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi cột (trừ cột khóa / bắt buộc).'),
       ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn n/10 cột” (tab Nhập khẩu), n/7 ở 2 tab còn lại.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình, đóng cửa sổ, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ; thay đổi chưa lưu bị bỏ.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”'])],
   ev=[('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Cấu hình của tab đã nạp lúc mở tab.\nDuring:\n– Liệt kê các cột theo cấu hình đang áp dụng.\n'
        'After:\n– Mở cửa sổ “Tuỳ chỉnh cột”.'),
       ('Kéo biểu tượng ba gạch', 'Drag',
        'Before:\n– Cột STT, Mã không kéo được.\nDuring:\n– Đổi thứ tự cột trong cửa sổ.\n'
        'After:\n– Chưa áp lên bảng cho tới khi bấm Lưu.'),
       ('Bỏ tích một cột', 'Change',
        'Before:\n– Cột STT, Mã, Hành động không cho bỏ tích.\nDuring:\n– Ghi nhận trạng thái trong cửa sổ, cập nhật dòng đếm.\n'
        'After:\n– Chưa áp lên bảng cho tới khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình gắn với người dùng và tab đang xem.\n'
        'During:\n– Ghi cấu hình; lỗi → hiển thị “Thao tác thất bại”.\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng theo cấu hình mới.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Bỏ thay đổi chưa lưu.\n'
        'After:\n– Đóng cửa sổ; lần mở sau hiện lại đúng cấu hình đang áp dụng.')])

# ------------------------------------------------------------ 2.7
fr(7, 'Xuất Excel danh sách', usecase=('FR-07', 'Xuất Excel danh sách', 'io', A_ND),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Xuất danh sách phiếu báo hàng về ra Excel',
              mota='Người dùng chọn trường và thứ tự cột trong cửa sổ “Chọn trường xuất file” rồi tải file Excel gồm TOÀN BỘ phiếu '
                   'của tab đang xem khớp bộ lọc và phạm vi (không riêng trang đang xem). Mỗi tab xuất bộ trường và tên file riêng.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm Xuất Excel trên thanh công cụ của bảng.\n'
                    '2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn đúng các cột đang hiện trên bảng (Nhập khẩu 8 trường, '
                    'Trong nước 6, Mua ngoài 6).\n'
                    '3. Người dùng tích / bỏ tích, kéo đổi thứ tự, bấm Xuất file.\n'
                    '4. Hệ thống đóng cửa sổ, lấy toàn bộ phiếu theo bộ lọc + phạm vi của tab, dựng file.\n'
                    '5. Hệ thống tải file (vd “phieu_bao_hang_ve_nhap_khau.xlsx”), hiển thị “Xuất Excel thành công.”.',
              phu='• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → không xuất.\n'
                  '• Không có phiếu khớp bộ lọc → vẫn tải file gồm logo, tiêu đề, hàng tên cột, không có dòng dữ liệu.\n'
                  '• Lỗi → hiển thị “Lỗi khi xuất Excel”, mở khóa nút.',
              dacbiet='Cấu trúc file: dòng 1 logo công ty (ảnh cố định của hệ thống); dòng 2 tiêu đề “Phiếu báo hàng về nhập khẩu” '
                      '/ “… trong nước” / “… mua ngoài”; dòng 3 tên cột gồm STT rồi các trường đã chọn đúng thứ tự; dữ liệu từ dòng '
                      '4; cuối file khối ký “Ngày ..., tháng ..., năm ... / Người lập / (Ký, họ tên)”. Ngày dạng dd/mm/yyyy hh:mm, '
                      'Trạng thái ghi tên nghiệp vụ. Tên file: phieu_bao_hang_ve_nhap_khau.xlsx, phieu_bao_hang_ve_trong_nuoc.xlsx, '
                      'phieu_bao_hang_ve_mua_ngoai.xlsx. Không giới hạn số dòng. Khóa nút Xuất Excel trong lúc chờ file.'),
   layout=dict(menu=M_IMP + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file — tab Nhập khẩu',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Chọn trường xuất file”', 'Kèm nút (x) đóng.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Tích chọn trường cần xuất, kéo ≡ để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Theo tab', 'Ít nhất 1', 'Theo cột đang hiện',
        ['- Nhập khẩu (8): Mã, Ngày tạo, Kho, Nhà cung cấp, Invoice, Hợp đồng, Người tạo, Trạng thái',
         '- Trong nước (6): Mã, Ngày tạo, Hợp đồng, Nhà cung cấp, Kho, Trạng thái',
         '- Mua ngoài (6): Mã, Ngày tạo, Kho, Hợp đồng, Nhà cung cấp, Trạng thái',
         '- Mặc định tích đúng các cột đang hiện trên bảng']),
       ('Ô tích của trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Theo cột đang hiện', 'Tích: trường có trong file.'),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Chữ gợi ý “Kéo để đổi vị trí cột trong file”', '- Thứ tự trong danh sách = thứ tự cột trong file']),
       ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn n/8 trường” (Nhập khẩu), n/6 ở 2 tab còn lại.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi trường.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Khóa khi chưa tích trường nào hoặc đang xuất', '- Bấm → đóng cửa sổ, tải file']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Xuất Excel thành công.”', '- Lỗi: “Lỗi khi xuất Excel”'])],
   ev=[('Bấm Xuất Excel trên thanh công cụ', 'Click',
        'Before:\n– Nút khóa khi đang có lượt xuất chạy.\n'
        'During:\n– Lấy danh sách trường của tab, tích sẵn các cột đang hiện.\n'
        'After:\n– Mở cửa sổ “Chọn trường xuất file”.'),
       ('Kéo tay nắm', 'Drag',
        'Before:\n– Áp cho mọi trường.\nDuring:\n– Đổi thứ tự trường.\nAfter:\n– Thứ tự mới là thứ tự cột trong file.'),
       ('Bấm Chọn tất cả hoặc Bỏ chọn hết', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Tích / bỏ tích mọi trường.\n'
        'After:\n– Cập nhật dòng đếm; bỏ hết thì khóa nút Xuất file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Ít nhất 1 trường được tích; khóa nút Xuất Excel trong lúc chờ.\n'
        'During:\n– Đóng cửa sổ; lấy toàn bộ phiếu theo bộ lọc + phạm vi của tab (bỏ phân trang).\n'
        '– Dựng file: logo, tiêu đề theo tab, STT + các cột đúng thứ tự đã chọn.\n' + ERR + '\n'
        'After:\n– Tải file theo tên của tab; hiển thị “Xuất Excel thành công.”.\n'
        '– Lỗi → “Lỗi khi xuất Excel”; mở khóa nút.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không xuất.\nAfter:\n– Đóng cửa sổ.')])

# ------------------------------------------------------------ 2.8
DETAIL_FOOT = [
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', ['- Góc phải chân màn', '- Bấm → về danh sách, đúng tab của phiếu']),
    ('Trang không tìm thấy', 'Label', 'Hiển thị', '–', 'Ẩn',
     ['- Phiếu không tồn tại hoặc ngoài phạm vi xem', '- Hiện ' + M_404]),
    ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Lỗi khi tải dữ liệu”: lỗi khác khi nạp phiếu'),
]
fr(8, 'Xem chi tiết phiếu nhập khẩu', usecase=('FR-08', 'Xem chi tiết phiếu nhập khẩu', 'view', A_ND),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(ten='Xem chi tiết phiếu báo hàng về nhập khẩu',
              mota='Xem toàn bộ thông tin một phiếu nhập khẩu ở chế độ chỉ đọc: Thông tin chung (invoice, hợp đồng, nhập thẳng, kho '
                   'nhận, dự kiến về kho, ghi chú) và khối Chi tiết gồm 4 tab Hàng hóa, Khuyến mại, Hàng bảo hành, Hàng thừa thiếu '
                   '(3 tab sau lấy theo invoice). Chân màn có In, Xuất Excel và các nút của người tạo phiếu.',
              tacnhan=TN_IMP, dieukien=DK_IMP,
              chinh='1. Người dùng bấm mã phiếu ở tab Nhập khẩu.\n'
                    '2. Hệ thống kiểm tra phiếu tồn tại và nằm trong phạm vi xem tab Nhập khẩu.\n'
                    '3. Hệ thống mở màn “Chi tiết phiếu báo hàng về: <mã>”, hiện Thông tin chung và tab Hàng hóa.\n'
                    '4. Người dùng bật ô Chi tiết để xem thêm Tên khách, Ngày cần, Ghi chú của từng dòng khách; chuyển các tab '
                    'Khuyến mại, Hàng bảo hành, Hàng thừa thiếu.\n'
                    '5. Hệ thống hiện nút chân màn theo người tạo và trạng thái phiếu.',
              phu='• Phiếu ngoài phạm vi hoặc không tồn tại / vừa bị xóa → chuyển trang ' + M_404 + '.\n'
                  '• Lỗi khác → “Lỗi khi tải dữ liệu”.\n'
                  '• Phiếu Nhập thẳng: ô Nhập thẳng được tích, không có ô Kho nhận.\n'
                  '• Bấm mã invoice / hợp đồng / đơn đặt hàng → mở màn tương ứng của hệ thống ERP ở tab mới.\n'
                  '• Tab không có dòng → “Không có dữ liệu”.\n'
                  '• Bấm Quay lại → về tab Nhập khẩu; bộ lọc, sắp xếp được giữ nếu quay lại trong 10 phút, danh sách về trang 1.',
              dacbiet='Màn chi tiết là trang riêng (không phải cửa sổ nổi), mọi ô chỉ đọc, không có nút lưu, không hiện nhãn trạng '
                      'thái. Tổng SL của dòng hàng = tổng SL các dòng chi tiết khách. Ô SL ở tab Khuyến mại / Hàng bảo hành / Hàng '
                      'thừa thiếu hiện số lượng kèm dòng “Hợp đồng:” và “Phụ lục <mã>:” không kèm số (giống hệ thống ERP).'),
   layout=dict(menu=M_IMP + ' => Xem chi tiết', shot=shot('17_detail_import'), shot_caption='Màn chi tiết phiếu nhập khẩu',
               extra=[(shot('17a_detail_import_expand'), 'Màn chi tiết phiếu nhập khẩu — bật ô Chi tiết')]),
   ui_kw=dict(required=False),
   ui=[('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Chi tiết phiếu báo hàng về: <mã phiếu>”, cũng là tiêu đề tab trình duyệt.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '“<Người tạo> - dd/mm/yyyy hh:mm” ở góc phải khối Thông tin chung.'),
       ('Số Invoice', 'Link', 'Read-only', '–', 'Theo dữ liệu',
        ['- Nhãn có dấu * như hệ thống ERP', '- Bấm mã → mở invoice ở hệ thống ERP, tab mới']),
       ('Hợp đồng', 'Link', 'Read-only', '–', 'Theo dữ liệu', '- Mã hợp đồng mua nước ngoài của invoice; bấm → mở ở hệ thống ERP'),
       ('Nhập thẳng', 'Checkbox', 'Disable', '–', 'Theo dữ liệu', '- Tích khi hàng nhập thẳng, không sửa được'),
       ('Kho nhận', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', ['- “Mã kho - Tên kho”, nhãn có dấu *', '- Ẩn khi Nhập thẳng']),
       ('Dự kiến về kho', 'Textbox', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '- Nhãn có dấu *'),
       ('Ghi chú', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '- 2 dòng, cùng hàng với Dự kiến về kho'),
       ('Ô Chi tiết', 'Checkbox', 'Enable', '–', 'Không tích',
        ['- Góc phải khối Chi tiết', '- Tích → mỗi dòng khách hiện thêm Tên khách, Ngày cần, Ghi chú (nhãn in đậm)']),
       ('Tab Hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột STT, PI (Số PI, Ngày PI), Model, Code đặt hàng, Hàng hóa (tên, Tên TV, Mã hàng), ĐVT, Tổng SL, Khách hàng, SL',
         '- Khách hàng: mã khách + mã đơn đặt hàng “<mã> - <người tạo> - <mã phòng>” (bấm mở ở hệ thống ERP) hoặc “Tồn kho”',
         '- Mỗi dòng khách 1 hàng; các ô của dòng hàng gộp dọc', '- Rỗng: “Không có dữ liệu”']),
       ('Tab Khuyến mại', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Hàng khuyến mại của invoice: STT, Hàng hóa, ĐVT, SL', '- Rỗng: “Không có dữ liệu”']),
       ('Tab Hàng bảo hành', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Hàng bảo hành của invoice, cùng bộ cột', '- Rỗng: “Không có dữ liệu”']),
       ('Tab Hàng thừa thiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Hàng thừa thiếu của invoice, cùng bộ cột', '- Rỗng: “Không có dữ liệu”']),
       ('Nút Tạo phân bổ chi phí', 'Button', 'Enable / Ẩn', '–', 'Ẩn', ['- Người tạo, phiếu Đã gửi', '- Bấm → mục 2.14']),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ xem trước bản in (mục 2.12).'),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', ['- Tải file Excel của phiếu (mục 2.13)', '- Khóa khi đang xuất']),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', ['- Màu đỏ; người tạo, phiếu Đã gửi', '- Bấm → hộp Xác nhận xóa (mục 2.11)']),
   ] + DETAIL_FOOT,
   ev=[('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phiếu tồn tại và nằm trong phạm vi xem tab Nhập khẩu (phiếu Đã yêu cầu nhập hàng chỉ người tạo xem).\n'
        '– Không thỏa → chuyển trang ' + M_404 + '.\n'
        'During:\n– Nạp Thông tin chung, dòng hàng + dòng chi tiết khách, khuyến mại / bảo hành / thừa thiếu của invoice.\n'
        '– Tính cờ người tạo + Đã gửi để hiện Xóa, Tạo phân bổ chi phí.\n'
        'After:\n– Hiển thị màn chỉ đọc, tab Hàng hóa; lỗi khác → “Lỗi khi tải dữ liệu”.'),
       ('Tích ô Chi tiết', 'Change',
        'Before:\n– Chỉ đổi cách hiển thị, không gọi máy chủ.\nDuring:\n– Bật / tắt phần thêm của dòng khách.\n'
        'After:\n– Hiện / ẩn Tên khách, Ngày cần, Ghi chú.'),
       ('Bấm tab Khuyến mại, Hàng bảo hành, Hàng thừa thiếu', 'Click',
        'Before:\n– Dữ liệu đã nạp cùng phiếu.\nDuring:\n– Chuyển tab.\nAfter:\n– Hiển thị bảng tương ứng; rỗng → “Không có dữ liệu”.'),
       ('Bấm mã invoice, hợp đồng, đơn đặt hàng', 'Click',
        'Before:\n– Ô có mã.\nDuring:\n– Xác định màn tương ứng của hệ thống ERP.\nAfter:\n– Mở ở tab trình duyệt mới.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– Màn chỉ đọc, không hỏi xác nhận.\nDuring:\n– Chuyển màn.\n'
        'After:\n– Về màn danh sách tab Nhập khẩu, khôi phục bộ lọc của tab (trong 10 phút).')])

# ------------------------------------------------------------ 2.9
fr(9, 'Xem chi tiết phiếu trong nước', usecase=('FR-09', 'Xem chi tiết phiếu trong nước', 'view', A_ND),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(ten='Xem chi tiết phiếu báo hàng về trong nước',
              mota='Xem một phiếu trong nước ở chế độ chỉ đọc: Thông tin chung (Hợp đồng, Nhà cung cấp, Kho nhận, Ghi chú) và bảng '
                   'Hàng hóa có phần Chi tiết theo yêu cầu đặt hàng / khách / SL về. Chỉ hiện dòng hàng và dòng chi tiết có số lượng '
                   'lớn hơn 0 như hệ thống ERP.',
              tacnhan=TN_XEM,
              dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu trong nước tồn tại (tab này không giới hạn phạm vi).\n'
                       '3. Người dùng đang ở tab Trong nước.',
              chinh='1. Người dùng bấm mã phiếu ở tab Trong nước.\n'
                    '2. Hệ thống mở màn “Chi tiết phiếu báo hàng về: <mã>”.\n'
                    '3. Hệ thống hiện Thông tin chung và bảng Hàng hóa (chỉ dòng có SL > 0).\n'
                    '4. Hệ thống hiện nút Tạo yêu cầu nhập hàng nếu người dùng là người tạo và phiếu Đã gửi.',
              phu='• Phiếu không tồn tại → chuyển trang ' + M_404 + '.\n'
                  '• Dòng chi tiết thuộc tồn kho công ty → cột Yêu cầu hiện “Tồn kho công ty”.\n'
                  '• Bấm mã hợp đồng / yêu cầu đặt hàng → mở ở hệ thống ERP, tab mới.\n'
                  '• Bấm Quay lại → về tab Trong nước.',
              dacbiet='Hiện trạng dữ liệu 03/11/2026: chưa có phiếu trong nước nào; ảnh mục Layout là bố cục màn khi chưa có dữ liệu. '
                      'Nhãn các ô không có dấu * (giống hệ thống ERP).'),
   layout=dict(menu=M_INL + ' => Xem chi tiết', shot=shot('17e_detail_inland'),
               shot_caption='Bố cục màn chi tiết phiếu trong nước (chưa có phiếu trên hệ thống)'),
   ui_kw=dict(required=False),
   ui=[('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Chi tiết phiếu báo hàng về: <mã phiếu>”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '“<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Hợp đồng', 'Link', 'Read-only', '–', 'Theo dữ liệu', '- Mã hợp đồng mua trong nước; bấm → mở ở hệ thống ERP, tab mới'),
       ('Nhà cung cấp', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '- Tên nhà cung cấp của phiếu'),
       ('Kho nhận', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '- “Mã kho - Tên kho”'),
       ('Ghi chú', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '- Rộng hết dòng, 2 dòng'),
       ('Bảng Hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột STT, Tên hàng hóa, Mã, Model, ĐVT, SL, Dự kiến hàng về', '- Chỉ dòng hàng có SL > 0']),
       ('Cột nhóm Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Yêu cầu: mã yêu cầu đặt hàng “<mã> - <người tạo> - <mã phòng>” (bấm mở ở hệ thống ERP) hoặc “Tồn kho công ty”',
         '- Khách hàng: tên khách', '- SL về: số lượng của dòng chi tiết (> 0)']),
       ('Trạng thái rỗng bảng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu”.'),
       ('Nút Tạo yêu cầu nhập hàng', 'Button', 'Enable / Ẩn', '–', 'Ẩn', ['- Người tạo, phiếu Đã gửi', '- Bấm → mục 2.15']),
   ] + DETAIL_FOOT,
   ev=[('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phiếu tồn tại (không áp phạm vi quyền); không có → trang ' + M_404 + '.\n'
        'During:\n– Nạp thông tin chung, dòng hàng và dòng chi tiết có SL > 0.\n'
        'After:\n– Hiển thị màn chỉ đọc; hiện nút Tạo yêu cầu nhập hàng nếu đủ điều kiện.'),
       ('Bấm mã hợp đồng hoặc yêu cầu đặt hàng', 'Click',
        'Before:\n– Ô có mã.\nDuring:\n– Xác định màn của hệ thống ERP.\nAfter:\n– Mở ở tab mới.'),
       ('Bấm Tạo yêu cầu nhập hàng', 'Click',
        'Before:\n– Người tạo, phiếu Đã gửi.\nDuring:\n– Ghép đường dẫn form tạo yêu cầu nhập hàng của hệ thống ERP kèm phiếu.\n'
        'After:\n– Mở form đó ở tab mới (mục 2.15).'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Chuyển màn.\nAfter:\n– Về tab Trong nước, khôi phục bộ lọc (trong 10 phút).')])

# ------------------------------------------------------------ 2.10
fr(10, 'Xem chi tiết phiếu mua ngoài', usecase=('FR-10', 'Xem chi tiết phiếu mua ngoài', 'view', A_ND),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(ten='Xem chi tiết phiếu báo hàng về mua ngoài',
              mota='Xem một phiếu mua ngoài ở chế độ chỉ đọc: Thông tin chung (Số hợp đồng hoặc phụ lục, Kho nhập, Nhập xuất '
                   'thẳng, Dự kiến về kho, Ghi chú) và khối Chi tiết gồm tab Hàng hóa (theo khách / đơn đặt hàng, SL, SL nhập kho, '
                   'Chênh lệch) và tab Khuyến mại.',
              tacnhan=TN_XEM,
              dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu mua ngoài tồn tại (tab này không giới hạn phạm vi).\n'
                       '3. Người dùng đang ở tab Mua ngoài.',
              chinh='1. Người dùng bấm mã phiếu ở tab Mua ngoài.\n'
                    '2. Hệ thống mở màn “Chi tiết phiếu báo hàng về: <mã>”.\n'
                    '3. Hệ thống hiện Thông tin chung và tab Hàng hóa; người dùng bật ô Chi tiết để xem Tên khách, Ngày cần, Ghi chú.\n'
                    '4. Hệ thống hiện nút Tạo phiếu yêu cầu nhập hàng nếu người dùng là người tạo và phiếu Đã gửi.',
              phu='• Phiếu không tồn tại → chuyển trang ' + M_404 + '.\n'
                  '• Phiếu lập theo phụ lục: ô Số hợp đồng hiện mã phụ lục, bấm mở phụ lục ở hệ thống ERP.\n'
                  '• Chênh lệch = SL − SL nhập kho, làm tròn 2 chữ số.\n'
                  '• Bấm Quay lại → về tab Mua ngoài.',
              dacbiet='Nhãn Số hợp đồng, Kho nhập, Dự kiến về kho có dấu * như hệ thống ERP. Ô Nhập xuất thẳng chỉ đọc, tích khi '
                      'phiếu là loại nhập xuất thẳng.'),
   layout=dict(menu=M_OUT + ' => Xem chi tiết', shot=shot('17d_detail_outside'), shot_caption='Màn chi tiết phiếu mua ngoài'),
   ui_kw=dict(required=False),
   ui=[('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Chi tiết phiếu báo hàng về: <mã phiếu>”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '“<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Số hợp đồng', 'Link', 'Read-only', '–', 'Theo dữ liệu',
        ['- Mã phụ lục hoặc mã hợp đồng mua trong nước, nhãn có dấu *', '- Bấm → mở ở hệ thống ERP, tab mới']),
       ('Kho nhập', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '- “Mã kho - Tên kho”, nhãn có dấu *'),
       ('Nhập xuất thẳng', 'Checkbox', 'Disable', '–', 'Theo dữ liệu', '- Tích khi phiếu nhập xuất thẳng'),
       ('Dự kiến về kho', 'Textbox', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '- Nhãn có dấu *'),
       ('Ghi chú', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '- 2 dòng'),
       ('Ô Chi tiết', 'Checkbox', 'Enable', '–', 'Không tích', '- Tích → dòng khách hiện thêm Tên khách, Ngày cần, Ghi chú'),
       ('Tab Hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột STT, Tên hàng, Mã hàng, ĐVT, Tổng SL, Khách hàng, SL, SL nhập kho, Chênh lệch',
         '- Khách hàng: mã khách + mã đơn đặt hàng “<mã> - <người tạo> - <mã phòng>” (bấm mở ở hệ thống ERP)',
         '- Rỗng: “Không có dữ liệu”']),
       ('Tab Khuyến mại', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột STT, Tên hàng, Mã hàng, ĐVT, SL, SL nhập kho, Chênh lệch', '- Rỗng: “Không có dữ liệu”']),
       ('Nút Tạo phiếu yêu cầu nhập hàng', 'Button', 'Enable / Ẩn', '–', 'Ẩn', ['- Người tạo, phiếu Đã gửi', '- Bấm → mục 2.15']),
   ] + DETAIL_FOOT,
   ev=[('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phiếu tồn tại (không áp phạm vi quyền); không có → trang ' + M_404 + '.\n'
        'During:\n– Nạp thông tin chung, dòng hàng + dòng khách (đơn đặt hàng qua nhóm người mua), khuyến mại.\n'
        'After:\n– Hiển thị màn chỉ đọc, tab Hàng hóa; nút Tạo phiếu yêu cầu nhập hàng theo điều kiện.'),
       ('Tích ô Chi tiết', 'Change',
        'Before:\n– Không gọi máy chủ.\nDuring:\n– Bật / tắt phần thêm của dòng khách.\nAfter:\n– Hiện / ẩn Tên khách, Ngày cần, Ghi chú.'),
       ('Bấm tab Khuyến mại', 'Click',
        'Before:\n– Dữ liệu đã nạp.\nDuring:\n– Chuyển tab.\nAfter:\n– Hiện bảng khuyến mại; rỗng → “Không có dữ liệu”.'),
       ('Bấm mã hợp đồng hoặc đơn đặt hàng', 'Click',
        'Before:\n– Ô có mã.\nDuring:\n– Phụ lục → màn phụ lục; hợp đồng → màn hợp đồng (hệ thống ERP).\nAfter:\n– Mở ở tab mới.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Chuyển màn.\nAfter:\n– Về tab Mua ngoài, khôi phục bộ lọc (trong 10 phút).')])

# ------------------------------------------------------------ 2.11
fr(11, 'Xóa phiếu nhập khẩu', usecase=('FR-11', 'Xóa phiếu nhập khẩu', 'action', A_TAO),
   rule=('- Quy tắc Xóa và Thông báo.', 'delete'),
   intro=dict(ten='Xóa phiếu báo hàng về nhập khẩu',
              mota='Người tạo xóa hẳn phiếu nhập khẩu đang ở trạng thái Đã gửi cùng toàn bộ dòng hàng, dòng chi tiết khách, hàng '
                   'khuyến mại, hàng bảo hành của phiếu; invoice của phiếu trở về trạng thái chưa báo hàng về để lập lại phiếu '
                   'được. Thao tác mở từ cột Hành động hoặc chân màn chi tiết, luôn qua hộp xác nhận.',
              tacnhan=TN_TAO, dieukien=DK_TAO,
              chinh='1. Người dùng bấm Xóa ở cột Hành động (tab Nhập khẩu) hoặc ở chân màn chi tiết phiếu nhập khẩu.\n'
                    '2. Hệ thống hiển thị hộp “Xác nhận xóa”.\n'
                    '3. Người dùng bấm Xóa.\n'
                    '4. Hệ thống khóa phiếu, kiểm tra lại người tạo và trạng thái Đã gửi.\n'
                    '5. Hệ thống bỏ đánh dấu “đã báo hàng về” của invoice, ghi nhận hành động “Xóa” vào nhật ký xử lý của phiếu '
                    '(dùng chung với hệ thống ERP), xóa dòng chi tiết khách, dòng hàng, khuyến mại, bảo hành rồi xóa phiếu.\n'
                    '6. Hệ thống hiển thị “Xóa thành công.”: ở danh sách thì nạp lại bảng; ở màn chi tiết thì về tab Nhập khẩu.',
              phu='• Bấm Hủy / (x) / click ra ngoài hộp → không xóa.\n'
                  '• Phiếu không còn đủ điều kiện (người khác vừa lập yêu cầu nhập hàng, phiếu đã bị xóa…) → ' + MSG_409 + '; ở '
                  'danh sách thì nạp lại bảng cho khớp hiện trạng.\n'
                  '• Lỗi khác → “Xóa không thành công”.\n'
                  '• Bấm Xóa liên tiếp khi đang xử lý → bỏ qua lần bấm sau.',
              dacbiet='Ràng buộc dữ liệu cấp con: dòng hàng, dòng chi tiết khách, khuyến mại, bảo hành là của chính phiếu nên bị xóa '
                      'theo, không chặn. Ràng buộc đang sử dụng: phiếu đã lập yêu cầu nhập hàng / phân bổ chi phí (Đã yêu cầu nhập '
                      'hàng) không xóa được (nút ẩn, máy chủ chặn). Màn không có trạng thái Khóa. Khuyến mại / bảo hành / thừa thiếu '
                      'của invoice không bị xóa.'),
   layout=dict(menu=M_IMP + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp xác nhận xóa phiếu',
               note='Modal Xác nhận xóa được mở ngay trên màn hình danh sách tab Nhập khẩu hoặc màn hình chi tiết phiếu nhập khẩu '
                    'theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Xóa trên dòng', 'Icon Button', 'Enable / Ẩn', 'Ẩn',
        ['- Cột Hành động tab Nhập khẩu, biểu tượng thùng rác đỏ', '- Chỉ hiện với người tạo, phiếu Đã gửi']),
       ('Nút Xóa ở màn chi tiết', 'Button', 'Enable / Ẩn', 'Ẩn', ['- Chân màn chi tiết, màu đỏ', '- Cùng điều kiện; khóa khi đang xóa']),
       ('Biểu tượng cảnh báo', 'Icon Button', 'Hiển thị', 'Hiển thị', '- Dấu chấm than đỏ cạnh tiêu đề hộp'),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', DEL_TITLE, 'Kèm nút (x) đóng.'),
       ('Nội dung', 'Label', 'Hiển thị', DEL_MSG, '- Không ghi mã phiếu trong câu hỏi'),
       ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', '- Màu đỏ, xác nhận xóa phiếu'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không xóa.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        ['- Thành công: “Xóa thành công.”', '- Không còn đủ điều kiện: ' + MSG_409, '- Lỗi khác: “Xóa không thành công”'])],
   ev=[('Bấm Xóa ở cột Hành động hoặc màn chi tiết', 'Click',
        'Before:\n– Nút chỉ hiện với người tạo, phiếu Đã gửi.\n'
        'During:\n– Ghi nhận phiếu cần xóa.\n'
        'After:\n– Hiển thị hộp ' + DEL_TITLE + ' nội dung ' + DEL_MSG + '.'),
       ('Bấm Xóa trong hộp xác nhận', 'Click',
        'Before:\n– Khóa phiếu; kiểm tra phiếu còn tồn tại, người đăng nhập là người tạo, phiếu Đã gửi.\n'
        '– Không đủ điều kiện → hiển thị ' + MSG_409 + ' và dừng xử lý.\n'
        'During:\n– Bỏ đánh dấu “đã báo hàng về” của invoice.\n' + ERR + '\n'
        'After:\n– Ghi nhận hành động “Xóa” vào nhật ký xử lý của phiếu (người ghi là người tạo phiếu).\n'
        '– Xóa dòng chi tiết khách, dòng hàng, khuyến mại, bảo hành và phiếu.\n'
        '– Hiển thị “Xóa thành công.”; ở danh sách nạp lại bảng, ở màn chi tiết về tab Nhập khẩu.'),
       ('Bấm Hủy, (x) hoặc click ra ngoài hộp', 'Click',
        'Before:\n– Hộp đang mở.\nDuring:\n– Không gọi máy chủ.\nAfter:\n– Đóng hộp, phiếu giữ nguyên.'),
       ('Máy chủ báo trạng thái đã thay đổi', 'System',
        'Before:\n– Người khác đã lập yêu cầu nhập hàng / đã xóa phiếu.\nDuring:\n– Hiển thị ' + MSG_409 + '.\n'
        'After:\n– Ở danh sách: nạp lại bảng cho khớp hiện trạng; ở màn chi tiết: giữ nguyên màn.')])

# ------------------------------------------------------------ 2.12
fr(12, 'In phiếu nhập khẩu', usecase=('FR-12', 'In phiếu nhập khẩu', 'io', A_ND),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(ten='In phiếu báo hàng về nhập khẩu',
              mota='Xem trước bản in của một phiếu nhập khẩu ngay trên màn hình (không mở tab mới) rồi in. Bản in dựng theo mẫu in '
                   '“Phiếu báo hàng về” của hệ thống (khổ ngang), đầu trang là letterhead của công ty ghi trên phiếu, gồm thông tin '
                   'chung và các khối Hàng hóa, Khuyến mại, Bảo hành, Thừa thiếu.',
              tacnhan=TN_IMP, dieukien=DK_IMP,
              chinh='1. Người dùng bấm In ở cột Hành động hoặc chân màn chi tiết.\n'
                    '2. Hệ thống mở cửa sổ “Xem trước phiếu báo hàng về”, hiện “Đang tải dữ liệu in…”.\n'
                    '3. Hệ thống kiểm tra phạm vi xem, dựng bản in và hiển thị.\n'
                    '4. Người dùng bấm In; hệ thống mở hộp thoại in của trình duyệt (khổ A4 ngang).',
              phu='• Bấm (x) / click ra ngoài cửa sổ → đóng.\n'
                  '• Phiếu ngoài phạm vi / không tồn tại → “Không tìm thấy dữ liệu” trong cửa sổ.\n'
                  '• Thiếu mẫu in trên hệ thống → “Không tìm thấy mẫu in "Phiếu báo hàng về"”.\n'
                  '• Bản in rỗng → “Không có dữ liệu để in”; lỗi khác → “Không tải được dữ liệu in”.',
              dacbiet='Letterhead lấy theo công ty ghi trên phiếu (không theo người đang đăng nhập). Ô “Số Invoice” ghi mã invoice '
                      '(hệ thống ERP ghi nhầm mã hợp đồng). Khối rỗng không in. In không ghi dữ liệu, không ghi lịch sử.'),
   layout=dict(menu=M_IMP + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu báo hàng về',
               note='Modal Xem trước được mở ngay trên màn hình danh sách tab Nhập khẩu hoặc màn hình chi tiết phiếu nhập khẩu theo '
                    'đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[('Nút In trên dòng', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Cột Hành động tab Nhập khẩu, biểu tượng máy in'),
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '“Xem trước phiếu báo hàng về”', '- Có nút (x) đóng'),
       ('Nút In', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Cạnh tiêu đề cửa sổ', '- Khóa khi đang tải hoặc chưa có bản in', '- Bấm → hộp thoại in của trình duyệt, khổ A4 ngang']),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu in…” trong lúc dựng bản in.'),
       ('Đầu bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Letterhead của công ty ghi trên phiếu', '- Tiêu đề “PHIẾU BÁO HÀNG VỀ”, dòng “Ngày dd Tháng mm Năm yyyy” (ngày in)']),
       ('Thông tin chung bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Số Invoice, Kho nhận, Số hợp đồng', '- Dự kiến về kho, Ghi chú']),
       ('Khối I. HÀNG HÓA', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột STT, PI, Model, Code đặt hàng, Hàng hóa, ĐVT, Tổng SL, Khách hàng, SL',
         '- Khách hàng: mã khách, đơn đặt hàng, Tên khách']),
       ('Khối Khuyến mại, Bảo hành, Thừa thiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Đánh số La Mã tiếp theo (II, III, IV)', '- Chỉ in khối có dòng; ô SL kèm dòng “Hợp đồng: <SL>”']),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Theo mẫu', '“Ngày … Tháng … Năm …” và “NGƯỜI LẬP PHIẾU”.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- “Không tìm thấy dữ liệu”', '- “Không tìm thấy mẫu in "Phiếu báo hàng về"”', '- “Không có dữ liệu để in”',
         '- “Không tải được dữ liệu in”'])],
   ev=[('Bấm In ở cột Hành động hoặc màn chi tiết', 'Click',
        'Before:\n– Kiểm tra phiếu tồn tại và nằm trong phạm vi xem tab Nhập khẩu; sai → “Không tìm thấy dữ liệu” trong cửa sổ.\n'
        'During:\n– Mở cửa sổ xem trước, hiện “Đang tải dữ liệu in…”; dựng bản in theo mẫu “Phiếu báo hàng về”, letterhead theo '
        'công ty của phiếu.\n'
        '– Thiếu mẫu in → “Không tìm thấy mẫu in "Phiếu báo hàng về"”.\n' + ERR + '\n'
        'After:\n– Hiển thị bản in khổ ngang; mở khóa nút In. Không ghi dữ liệu.'),
       ('Bấm In trong cửa sổ', 'Click',
        'Before:\n– Bản in đã tải xong.\nDuring:\n– Dựng trang in ẩn với đúng nội dung xem trước, khổ A4 ngang.\n'
        'After:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Dọn trang in ẩn.\nAfter:\n– Đóng cửa sổ xem trước, màn đứng nguyên.'),
       ('Máy chủ lỗi khi dựng bản in', 'System',
        'Before:\n– Đang tải bản in.\nDuring:\n– Nhận thông báo lỗi.\n'
        'After:\n– Hiện câu lỗi trong cửa sổ (“Không tải được dữ liệu in” hoặc câu máy chủ trả), nút In khóa.')])

# ------------------------------------------------------------ 2.13
fr(13, 'Xuất Excel một phiếu nhập khẩu', usecase=('FR-13', 'Xuất Excel một phiếu', 'io', A_ND),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Xuất Excel chứng từ một phiếu báo hàng về nhập khẩu',
              mota='Tải file Excel chứng từ của một phiếu nhập khẩu từ nút Xuất Excel ở cột Hành động hoặc chân màn chi tiết. File '
                   'có letterhead công ty ghi trên phiếu, tiêu đề “PHIẾU BÁO HÀNG VỀ”, thông tin chung và các bảng hàng như bản in.',
              tacnhan=TN_IMP, dieukien=DK_IMP,
              chinh='1. Người dùng bấm Xuất Excel ở cột Hành động hoặc chân màn chi tiết.\n'
                    '2. Hệ thống kiểm tra phiếu nằm trong phạm vi xem.\n'
                    '3. Hệ thống dựng file chứng từ của phiếu.\n'
                    '4. Hệ thống tải file “phieu_bao_hang_ve_<mã phiếu>.xlsx”, hiển thị “Xuất Excel thành công.”.',
              phu='• Phiếu ngoài phạm vi / không tồn tại → không tải, hiển thị “Lỗi khi xuất Excel”.\n'
                  '• Bấm liên tiếp khi đang xuất → bỏ qua lần bấm sau (nút ở màn chi tiết khóa).\n'
                  '• Lỗi máy chủ → “Lỗi khi xuất Excel”.',
              dacbiet='Cấu trúc file: letterhead công ty ghi trên phiếu; “PHIẾU BÁO HÀNG VỀ”; “Ngày dd Tháng mm Năm yyyy” (ngày xuất); '
                      '3 dòng thông tin 2 cặp nhãn – giá trị: Số invoice – Kho nhập, Dự kiến về kho – Số hợp đồng, Người tạo – Ngày '
                      'tạo; dòng Ghi chú; khối I. HÀNG HÓA 9 cột (STT, PI, Model, Code đặt hàng, Hàng hóa, ĐVT, Tổng SL, Khách hàng, '
                      'SL) và các khối Khuyến mại / Bảo hành / Thừa thiếu nếu có; chỗ ký “Người lập phiếu (Ký, họ tên)”. Số lượng '
                      'là ô số định dạng #,##0 (cộng được). Phiếu không có dòng hàng thì file dùng bố cục 4 cột.'),
   layout=dict(menu=M_IMP + ' => Xuất Excel phiếu', shot=shot('01_list'), shot_caption='Nút Xuất Excel ở cột Hành động tab Nhập khẩu',
               note='Không mở cửa sổ: bấm nút là tải file ngay, từ màn hình danh sách tab Nhập khẩu hoặc màn hình chi tiết phiếu.'),
   ui_kw=dict(required=False),
   ui=[('Nút Xuất Excel trên dòng', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Cột Hành động tab Nhập khẩu, biểu tượng Excel'),
       ('Nút Xuất Excel ở màn chi tiết', 'Button', 'Enable / Disable', '–', 'Hiển thị', ['- Chân màn chi tiết', '- Khóa khi đang xuất']),
       ('Tên file', 'Label', 'Read-only', '–', 'Theo dữ liệu', '“phieu_bao_hang_ve_<mã phiếu>.xlsx”.'),
       ('Đầu file', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Letterhead công ty ghi trên phiếu', '- “PHIẾU BÁO HÀNG VỀ”, “Ngày … Tháng … Năm …” (ngày xuất)']),
       ('Thông tin chung trong file', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Số invoice, Kho nhập', '- Dự kiến về kho, Số hợp đồng', '- Người tạo, Ngày tạo (dd/mm/yyyy)', '- Ghi chú']),
       ('Khối I. HÀNG HÓA', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- 9 cột như bản in', '- Tổng SL, SL là ô số #,##0']),
       ('Khối Khuyến mại, Bảo hành, Thừa thiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Chỉ có khi invoice có dòng', '- Ô Hàng hóa gộp rộng; SL kèm dòng “Hợp đồng: <SL>”']),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Theo mẫu', '“Ngày .... Tháng .... Năm ....”, “Người lập phiếu”, “(Ký, họ tên)”.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- Thành công: “Xuất Excel thành công.”', '- Lỗi: “Lỗi khi xuất Excel”'])],
   ev=[('Bấm Xuất Excel của một phiếu', 'Click',
        'Before:\n– Bỏ qua nếu đang có lượt xuất chạy.\n– Kiểm tra phiếu tồn tại và nằm trong phạm vi xem tab Nhập khẩu; sai → '
        'không tải, hiển thị “Lỗi khi xuất Excel”.\n'
        'During:\n– Dựng file chứng từ (letterhead công ty ghi trên phiếu, nội dung như bản in).\n' + ERR + '\n'
        'After:\n– Tải file “phieu_bao_hang_ve_<mã phiếu>.xlsx”; hiển thị “Xuất Excel thành công.”.'),
       ('Máy chủ lỗi khi dựng file', 'System',
        'Before:\n– Đang xuất.\nDuring:\n– Nhận lỗi “Xuất Excel không thành công”.\n'
        'After:\n– Hiển thị “Lỗi khi xuất Excel”, mở khóa nút.'),
       ('Mở file đã tải', 'System',
        'Before:\n– File đã tải về máy.\nDuring:\n– Excel hiển thị letterhead, thông tin chung, các khối hàng.\n'
        'After:\n– Số lượng là ô số, cộng được bằng hàm SUM.'),
       ('Bấm lại nút khi đang xuất', 'Click',
        'Before:\n– Lượt xuất trước chưa xong.\nDuring:\n– Bỏ qua lần bấm.\nAfter:\n– Chỉ tải 1 file.')])

# ------------------------------------------------------------ 2.14
fr(14, 'Tạo phân bổ chi phí', usecase=('FR-14', 'Tạo phân bổ chi phí', 'action', A_TAO),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(ten='Tạo phân bổ chi phí từ phiếu báo hàng về nhập khẩu',
              mota='Từ màn chi tiết phiếu nhập khẩu, người tạo phiếu mở form Tạo phân bổ chi phí nhập khẩu của hệ thống ERP với phiếu '
                   'báo hàng về đã chọn sẵn, để phân bổ chi phí lô hàng và lập yêu cầu nhập kho. Màn đích chưa chuyển sang hệ '
                   'thống mới nên mở ở tab mới.',
              tacnhan=TN_TAO,
              dieukien=DK_TAO + '\n4. Người dùng đang ở màn chi tiết phiếu nhập khẩu.',
              chinh='1. Người dùng mở màn chi tiết phiếu nhập khẩu do mình tạo, phiếu Đã gửi.\n'
                    '2. Hệ thống hiện nút Tạo phân bổ chi phí ở chân màn.\n'
                    '3. Người dùng bấm Tạo phân bổ chi phí.\n'
                    '4. Hệ thống mở form tạo phân bổ chi phí của hệ thống ERP ở tab trình duyệt mới, kèm phiếu báo hàng về.\n'
                    '5. Người dùng lập và lưu phân bổ chi phí trên hệ thống ERP (theo tài liệu màn đó).',
              phu='• Không phải người tạo hoặc phiếu Đã yêu cầu nhập hàng → nút ẩn.\n'
                  '• Trình duyệt chặn mở tab mới → người dùng cho phép cửa sổ bật lên rồi bấm lại.\n'
                  '• Chưa đăng nhập hệ thống ERP → hệ thống ERP yêu cầu đăng nhập trước.',
              dacbiet='Màn này không ghi dữ liệu khi bấm nút; trạng thái phiếu đổi theo nghiệp vụ của màn phân bổ chi phí.'),
   layout=dict(menu=M_IMP + ' => Xem chi tiết => Tạo phân bổ chi phí', shot=shot('17b_detail_import_owner'),
               shot_caption='Màn chi tiết phiếu nhập khẩu của người tạo — có nút Tạo phân bổ chi phí và Xóa'),
   ui_kw=dict(required=False),
   ui=[('Nút Tạo phân bổ chi phí', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
        ['- Nút xanh đầu cụm nút chân màn, biểu tượng tài liệu thêm', '- Chỉ hiện với người tạo, phiếu Đã gửi',
         '- Bấm → mở form Tạo phân bổ chi phí của hệ thống ERP ở tab mới']),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Cùng cụm, mục 2.12'),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', '- Cùng cụm, mục 2.13'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', '- Cùng điều kiện với Tạo phân bổ chi phí, mục 2.11'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về tab Nhập khẩu'),
       ('Form đích (hệ thống ERP)', 'Link', 'Enable', '–', '–', '- Form tạo phân bổ chi phí với phiếu báo hàng về đã chọn sẵn')],
   ev=[('Mở màn chi tiết phiếu nhập khẩu', 'System',
        'Before:\n– Kiểm tra người đăng nhập là người tạo và phiếu Đã gửi.\nDuring:\n– Tính cờ hiện nút.\n'
        'After:\n– Hiện / ẩn nút Tạo phân bổ chi phí.'),
       ('Bấm Tạo phân bổ chi phí', 'Click',
        'Before:\n– Nút chỉ hiện khi đủ điều kiện; không có hộp xác nhận.\n'
        'During:\n– Ghép đường dẫn form tạo phân bổ chi phí của hệ thống ERP kèm mã phiếu báo hàng về.\n'
        'After:\n– Mở form ở tab trình duyệt mới; màn chi tiết giữ nguyên, không ghi dữ liệu.'),
       ('Lưu phân bổ chi phí ở hệ thống ERP', 'System',
        'Before:\n– Theo nghiệp vụ màn phân bổ chi phí của hệ thống ERP.\nDuring:\n– Ngoài phạm vi màn này.\n'
        'After:\n– Quay lại màn chi tiết, tải lại trang để thấy trạng thái mới của phiếu.')])

# ------------------------------------------------------------ 2.15
fr(15, 'Tạo phiếu yêu cầu nhập hàng', usecase=('FR-15', 'Tạo phiếu yêu cầu nhập hàng', 'action', A_TAO),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(ten='Tạo phiếu yêu cầu nhập hàng từ phiếu báo hàng về mua ngoài / trong nước',
              mota='Từ màn chi tiết phiếu mua ngoài, người tạo phiếu bấm Tạo phiếu yêu cầu nhập hàng để mở màn “Thêm phiếu yêu cầu '
                   'nhập hàng” của hệ thống với loại Nhập hàng mua ngoài và phiếu báo hàng về chọn sẵn. Với phiếu trong nước, nút Tạo '
                   'yêu cầu nhập hàng mở form của hệ thống ERP ở tab mới (loại yêu cầu này hệ thống mới chưa hỗ trợ).',
              tacnhan=TN_TAO,
              dieukien=DK_TAO + '\n4. Người dùng đang ở màn chi tiết phiếu mua ngoài hoặc phiếu trong nước.',
              chinh='1. Người dùng mở màn chi tiết phiếu mua ngoài do mình tạo, phiếu Đã gửi.\n'
                    '2. Người dùng bấm Tạo phiếu yêu cầu nhập hàng.\n'
                    '3. Hệ thống mở màn “Thêm phiếu yêu cầu nhập hàng”: Loại yêu cầu = Nhập hàng mua ngoài, Phiếu báo hàng về = mã '
                    'phiếu, tự điền Hợp đồng, Nhà cung cấp, bảng Hàng hoá theo phiếu.\n'
                    '4. Người dùng nhập các trường còn thiếu (Kho nhập, Vận chuyển…) và lưu theo SRS màn Phiếu yêu cầu nhập hàng.\n'
                    '5. Khi phiếu yêu cầu nhập hàng được lưu, hệ thống chuyển phiếu báo hàng về sang Đã yêu cầu nhập hàng.',
              phu='• Phiếu trong nước: bấm Tạo yêu cầu nhập hàng → mở form của hệ thống ERP ở tab mới.\n'
                  '• Không phải người tạo hoặc phiếu Đã yêu cầu nhập hàng → nút ẩn.\n'
                  '• Rời màn Thêm phiếu yêu cầu nhập hàng khi chưa lưu → hỏi xác nhận theo màn đó.\n'
                  '• Phiếu báo hàng về đã chuyển Đã yêu cầu nhập hàng thì không chọn lại được ở màn yêu cầu nhập hàng.',
              dacbiet='Bấm nút không ghi dữ liệu; trạng thái phiếu báo hàng về chỉ đổi khi phiếu yêu cầu nhập hàng được lưu.'),
   layout=dict(menu=M_OUT + ' => Xem chi tiết => Tạo phiếu yêu cầu nhập hàng', shot=shot('21_ycnh_create'),
               shot_caption='Màn Thêm phiếu yêu cầu nhập hàng mở từ phiếu mua ngoài (loại và phiếu nguồn chọn sẵn)',
               note='Lối vào phiếu trong nước: ' + M_INL + ' => Xem chi tiết => Tạo yêu cầu nhập hàng (mở hệ thống ERP).'),
   ui_kw=dict(required=False),
   ui=[('Nút Tạo phiếu yêu cầu nhập hàng', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
        ['- Chân màn chi tiết phiếu mua ngoài, nút xanh', '- Chỉ hiện với người tạo, phiếu Đã gửi']),
       ('Nút Tạo yêu cầu nhập hàng', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
        ['- Chân màn chi tiết phiếu trong nước', '- Chỉ hiện với người tạo, phiếu Đã gửi', '- Bấm → form của hệ thống ERP, tab mới']),
       ('Tiêu đề màn đích', 'Label', 'Hiển thị', '–', '“Thêm phiếu yêu cầu nhập hàng”', '- Màn của phân hệ Tài chính'),
       ('Loại yêu cầu', 'Dropdown', 'Enable', 'Danh sách loại yêu cầu', 'Nhập hàng mua ngoài', '- Chọn sẵn theo nút đã bấm'),
       ('Phiếu báo hàng về', 'Textbox', 'Enable', '–', 'Mã phiếu nguồn', '- Điền sẵn mã phiếu, có nút × bỏ chọn'),
       ('Hợp đồng', 'Textbox', 'Read-only', '–', 'Theo phiếu', '- Hợp đồng mua của phiếu báo hàng về'),
       ('Nhà cung cấp', 'Textbox', 'Read-only', '–', 'Theo hợp đồng', '- Nhà cung cấp của hợp đồng mua'),
       ('Bảng Hàng hoá', 'Table/Grid', 'Read-only', '–', 'Theo phiếu', '- Dòng hàng theo SL thực về của phiếu, không sửa số lượng'),
       ('Các nút lưu của màn đích', 'Button', 'Enable', '–', 'Hiển thị', '- Lưu nháp, Lưu và gửi duyệt, Lưu và tiếp tục, Quay lại')],
   ev=[('Bấm Tạo phiếu yêu cầu nhập hàng (phiếu mua ngoài)', 'Click',
        'Before:\n– Nút chỉ hiện với người tạo, phiếu Đã gửi; không hỏi xác nhận.\n'
        'During:\n– Chuyển sang màn Thêm phiếu yêu cầu nhập hàng kèm loại Nhập hàng mua ngoài và mã phiếu nguồn.\n'
        'After:\n– Màn đích chọn sẵn loại, nạp phiếu nguồn, tự điền hợp đồng, nhà cung cấp, hàng hoá.'),
       ('Bấm Tạo yêu cầu nhập hàng (phiếu trong nước)', 'Click',
        'Before:\n– Nút chỉ hiện với người tạo, phiếu Đã gửi.\n'
        'During:\n– Ghép đường dẫn form tạo yêu cầu nhập hàng của hệ thống ERP kèm phiếu.\n'
        'After:\n– Mở ở tab mới; màn chi tiết giữ nguyên.'),
       ('Lưu phiếu yêu cầu nhập hàng', 'System',
        'Before:\n– Kiểm tra theo SRS màn Phiếu yêu cầu nhập hàng.\nDuring:\n– Lưu phiếu yêu cầu nhập hàng.\n' + ERR + '\n'
        'After:\n– Chuyển phiếu báo hàng về sang Đã yêu cầu nhập hàng; nút tạo trên màn chi tiết không còn hiện.'),
       ('Rời màn Thêm phiếu yêu cầu nhập hàng chưa lưu', 'Click',
        'Before:\n– Có thay đổi chưa lưu.\nDuring:\n– Hỏi xác nhận theo màn đó.\nAfter:\n– Không lưu thì phiếu báo hàng về giữ Đã gửi.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu báo hàng về; không lặp lại các quy tắc đã có trong SRS quy tắc '
           'chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi xem tab Nhập khẩu', [
        '– Xét quyền theo thứ tự V1 (tất cả) → V2 (công ty đang chọn làm việc; chưa chọn thì rỗng) → V3 (phòng ban mình quản lý).',
        '– Không có quyền nào: phiếu mình tạo hoặc phiếu có hàng hóa / hàng bảo hành / hàng khuyến mại thuộc cặp thương hiệu – hãng '
        'mình đang phụ trách mua ở công ty đang chọn.',
        '– Mọi cấp: phiếu Đã yêu cầu nhập hàng chỉ người tạo thấy.',
        '– Phạm vi xem chi tiết, in, xuất Excel một phiếu = phạm vi danh sách.'],
     ['Xem danh sách tab Nhập khẩu', 'Xem chi tiết', 'In', 'Xuất Excel']),
    ('BR-02', 'Tab Trong nước, Mua ngoài không giới hạn', [
        '– Ai vào màn cũng thấy toàn bộ phiếu (như hệ thống ERP).',
        '– Ô Công ty / Phòng ban / Bộ phận tab Mua ngoài chọn được mọi công ty, lọc theo tổ chức ghi trên phiếu.'],
     ['Xem danh sách', 'Tìm kiếm và lọc', 'Xem chi tiết']),
    ('BR-03', 'Trạng thái phiếu', [
        '– Đã gửi: phiếu đã báo, chưa lập chứng từ tiếp theo.',
        '– Đã yêu cầu nhập hàng: đã lập phiếu yêu cầu nhập hàng / phân bổ chi phí từ phiếu; trạng thái cuối trên màn này.',
        '– Màn này không đổi trạng thái; trạng thái đổi khi lưu phiếu yêu cầu nhập hàng (hệ thống) hoặc phân bổ chi phí (hệ thống ERP).'],
     ['Xem danh sách', 'Tạo phân bổ chi phí', 'Tạo phiếu yêu cầu nhập hàng']),
    ('BR-04', 'Điều kiện thao tác của người tạo', [
        '– Xóa (tab Nhập khẩu), Tạo phân bổ chi phí, Tạo (phiếu) yêu cầu nhập hàng: chỉ người tạo phiếu, phiếu Đã gửi.',
        '– Không đủ điều kiện thì nút ẩn hẳn; máy chủ kiểm lại khi Xóa.'],
     ['Xóa', 'Tạo phân bổ chi phí', 'Tạo phiếu yêu cầu nhập hàng']),
    ('BR-05', 'Điều kiện xóa và dữ liệu đi kèm', [
        '– Kiểm lại người tạo + Đã gửi trong lúc khóa phiếu; không thỏa → “Trạng thái đã bị thay đổi. Vui lòng load lại trang”.',
        '– Xóa phiếu xóa luôn dòng hàng, dòng chi tiết khách, khuyến mại, bảo hành của phiếu; không để dòng mồ côi.',
        '– Invoice của phiếu được bỏ đánh dấu “đã báo hàng về” để lập lại phiếu báo hàng về được.',
        '– Khuyến mại / bảo hành / thừa thiếu của invoice không bị xóa.'],
     ['Xóa']),
    ('BR-06', 'Hiển thị đối tác và hợp đồng theo tab', [
        '– Nhập khẩu: Nhà cung cấp = nhà cung cấp của invoice (“Mã - Tên”); Hợp đồng = hợp đồng mua nước ngoài của invoice.',
        '– Trong nước: Nhà cung cấp, Hợp đồng của phiếu.',
        '– Mua ngoài: Hợp đồng = mã phụ lục (phiếu theo phụ lục) hoặc mã hợp đồng; Nhà cung cấp = “<mã> - <tên NCC trên hợp đồng>”.'],
     ['Xem danh sách', 'Xem chi tiết', 'Xuất Excel']),
    ('BR-07', 'Liên kết sang hệ thống ERP', [
        '– Mã invoice, hợp đồng, phụ lục, đơn đặt hàng, yêu cầu đặt hàng mở màn của hệ thống ERP ở tab mới.',
        '– Tạo phân bổ chi phí (Nhập khẩu) và Tạo yêu cầu nhập hàng (Trong nước) mở form của hệ thống ERP ở tab mới.'],
     ['Xem danh sách', 'Xem chi tiết', 'Tạo phân bổ chi phí', 'Tạo phiếu yêu cầu nhập hàng']),
    ('BR-08', 'Bản in và file Excel một phiếu', [
        '– Letterhead theo công ty ghi trên phiếu, không theo người đang đăng nhập.',
        '– Mẫu in “Phiếu báo hàng về” khổ ngang; ô Số Invoice ghi mã invoice.',
        '– Excel: số lượng là ô số #,##0; khối hàng rỗng không xuất.'],
     ['In', 'Xuất Excel một phiếu']),
    ('BR-09', 'Tạo phiếu yêu cầu nhập hàng từ phiếu mua ngoài', [
        '– Mở màn Thêm phiếu yêu cầu nhập hàng với loại Nhập hàng mua ngoài và phiếu nguồn chọn sẵn.',
        '– Lưu phiếu yêu cầu nhập hàng → phiếu báo hàng về chuyển Đã yêu cầu nhập hàng; không lập phiếu thứ hai từ cùng phiếu.'],
     ['Tạo phiếu yêu cầu nhập hàng']),
    ('BR-10', 'Ghi nhớ bộ lọc', [
        '– Mỗi tab nhớ bộ lọc, chiều sắp xếp, trạng thái mở khối nâng cao riêng trên trình duyệt; hết hạn sau 10 phút không đổi.',
        '– Trong hạn: tải lại trang, sang màn khác rồi quay lại, mở tab trình duyệt mới đều giữ bộ lọc; không phân biệt tài khoản.',
        '– Làm mới xóa toàn bộ bộ lọc của tab.'],
     ['Tìm kiếm và lọc', 'Xem danh sách']),
    ('BR-11', 'Tính duy nhất', [
        '– Mã phiếu PBHV-NNNNN do nơi lập phiếu (hệ thống ERP) sinh, duy nhất trong từng loại phiếu; màn này không tạo, không sửa mã.',
        '– Mỗi invoice có tối đa 1 phiếu báo hàng về nhập khẩu còn hiệu lực (invoice được đánh dấu đã báo hàng về).'],
     ['Xem danh sách', 'Xóa']),
    ('BR-12', 'Chuẩn hóa dữ liệu tìm kiếm', [
        '– Ô gõ tự bỏ khoảng trắng đầu / cuối; khớp một phần; không phân biệt hoa / thường; ký tự % và _ là ký tự đại diện.',
        '– Ô chọn khớp chính xác; Ngày tạo lấy trọn ngày biên; không giới hạn số ký tự.'],
     ['Tìm kiếm và lọc']),
    ('BR-13', 'Liên kết cha – con', [
        '– Phiếu > dòng hàng hóa > dòng chi tiết khách; Tổng SL dòng hàng (Nhập khẩu) = tổng SL các dòng chi tiết.',
        '– Phiếu trong nước chỉ hiện dòng hàng / dòng chi tiết có SL > 0.',
        '– Phiếu mua ngoài: Chênh lệch = SL − SL nhập kho.'],
     ['Xem chi tiết', 'Xóa']),
    ('BR-14', 'Không ghi lịch sử thay đổi', [
        '– Màn chỉ đọc nên không có Lịch sử thay đổi.',
        '– Riêng Xóa ghi một dòng “Xóa” vào nhật ký xử lý của phiếu (dùng chung với hệ thống ERP, người ghi là người tạo phiếu).'],
     ['Xóa']),
    ('BR-15', 'Sửa so với hệ thống ERP (có chủ đích)', [
        '– Lọc Nhà cung cấp tab Nhập khẩu dùng danh sách đối tác (hệ thống ERP lấy nhầm danh sách kho).',
        '– Lọc Nhà cung cấp, Tên, mã hàng tab Mua ngoài đọc qua hợp đồng / dòng hàng (hệ thống ERP luôn ra 0).',
        '– Xóa được kiểm lại ở máy chủ; “Người lập” đổi thành “Người tạo”; “Đã gửi” màu vàng.'],
     ['Tìm kiếm và lọc', 'Xóa', 'Xem danh sách']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc dùng dữ liệu do Phiếu báo hàng về ghi ra (phiếu, dòng hàng thực về, hợp đồng mua và invoice của phiếu). Phiếu đã lập yêu cầu nhập hàng / phân bổ chi phí không xóa được (BR-05, BR-09).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Tài chính', 'Yêu cầu nhập hàng (loại Nhập hàng mua ngoài lấy phiếu báo hàng về mua ngoài làm chứng từ nguồn)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Nhập hàng'),
    ('2', 'Tài chính', 'Phiếu nhập kho (lọc theo số hợp đồng mua của phiếu báo hàng về)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Nhập hàng'),
    ('3', 'Tài chính', 'Phiếu báo có (tra hợp đồng mua của phiếu nhập hàng mua ngoài)', 'Tài chính -> Quản lý tiền -> Thanh toán tiền mặt'),
    ('4', 'Hệ thống ERP', 'Phân bổ chi phí nhập khẩu (lập từ phiếu tab Nhập khẩu)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
    ('5', 'Hệ thống ERP', 'Invoice nhập khẩu (invoice đã có phiếu báo hàng về không lập phiếu thứ 2)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)

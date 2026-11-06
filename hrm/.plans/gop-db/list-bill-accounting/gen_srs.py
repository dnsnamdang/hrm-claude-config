# -*- coding: utf-8 -*-
"""SRS màn "Danh sách loại phiếu hạch toán" (màn DANH MỤC CHỈ XEM: danh sách + tìm / lọc + Tùy chỉnh cột + Xuất Excel) — form chuẩn
Danh mục quốc gia, chuẩn 04/11/2026 (Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn).

Chạy: python gen_srs.py  → SRS - Danh sách loại phiếu hạch toán.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc ../benefit-rates/gen_srs.py
  (06/11/2026, màn danh mục cùng nhóm menu).
Nguồn đọc 06/11/2026 (nhánh develop, checkout từ gop_db, cả 2 repo):
  BE  Modules/Finance/{Entities/ListBillAccounting.php (TYPES 1..9), Services/ListBillAccountingService.php (index / exportRows / types),
      Http/Controllers/V1/ListBillAccountingController.php, Transformers/ListBillAccountingResource/ListBillAccountingResource.php,
      Routes/api.php (/list-bill-accountings — KHÔNG gắn checkPermission)}, app/Helper/FormatHelper.php::escapeLikeKeyword
  FE  pages/admin/list-bill-accountings/index.vue (file duy nhất — không có popup Thêm / Sửa / Xem / Xóa / Lịch sử),
      components/subsystem-menu/sale-hub.js (Bán hàng › Quy chế - Thiết lập › Thiết lập), components/V2BaseSmartFilterPanel.vue
      (bộ lọc gọn ≤ 3 ô: không có Tìm kiếm nâng cao / Cài đặt bộ lọc), components/V2BaseDataTable.vue, utils/export/listExportFile.js,
      utils/mixins/{filterStateMixin,columnCustomizationMixin,exportFieldsMixin}.js
  Bối cảnh: design.md, plan.md, spec docs/superpowers/specs/gop-db/2026-10-13-list-bill-accounting-design.md
  Màn đọc ngược: grep list_bill_accountings / ListBillAccounting toàn hrm-api + hrm-client + ERP (D:/laragon/www/erp) và cột *bill_accounting*
  trong cơ sở dữ liệu gộp → KHÔNG màn HRM nào đọc; chỉ màn gốc của hệ thống ERP đọc cùng bảng.
Ảnh: ./dslpht_shots — dev-hrm 06/11/2026 (_capture/capture.js, chặn mọi yêu cầu ghi — 0 yêu cầu), DỮ LIỆU THẬT (105 loại phiếu cố định).
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

TEN = 'Danh sách loại phiếu hạch toán'
SHOTS = os.path.join(HERE, 'dslpht_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Bán hàng => Quy chế - Thiết lập => Thiết lập => Danh sách loại phiếu hạch toán'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Danh sách loại phiếu hạch toán.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
EMPTY = '“Không có dữ liệu phù hợp bộ lọc.”'
LOADERR = '“Lỗi khi tải dữ liệu”'
TYPES = 'Đề nghị xuất, Đề nghị nhập, Xuất hàng, Nhập hàng, Thu, Chi, Phiếu kế toán, Dịch vụ, Khác'

A_ND = 'Người dùng tra cứu loại phiếu'
TN = ('Người dùng có quyền thực hiện chức năng: mọi người dùng đã được cấp tài khoản (màn không gắn quyền riêng, giữ như hệ thống '
      'cũ); xem được toàn bộ loại phiếu, không giới hạn theo công ty.')
DK = ('1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn Danh sách loại phiếu hạch toán.\n'
      '3. Danh sách đã nạp xong (105 loại phiếu cấu hình sẵn).')

d = SrsDoc(out=OUT, menu=MENU, route='/admin/list-bill-accountings', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Bán hàng': 'menu_phanhe', 'Quy chế - Thiết lập': 'menu_nhom', 'Thiết lập': 'menu_nhom2',
    'Danh sách loại phiếu hạch toán': 'menu_muc',
    'Cấu hình cột': 'btn_cauhinhcot', 'Xuất Excel': 'btn_xuatexcel',
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
    """Một chức năng 2.x: (Biểu đồ Usecase) · Giới thiệu · Layout · Mô tả giao diện · Event."""
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


# ============================================================== TRANG ĐẦU
d.title_block(TEN)
d.doc.add_page_break()  # Mục lục sang trang riêng như bản Drive đã chuẩn hoá
d.h2('Mục lục')
d.doc.paragraphs[-1].alignment = 1  # căn giữa chữ 'Mục lục'
d.toc()

# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình tra cứu Danh sách loại phiếu hạch toán, chuyển từ hệ thống cũ (Quản trị hệ thống '
    '› Cấu hình ERP) sang phân hệ Bán hàng, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phạm vi dữ liệu và luồng xử lý của màn hình.',
    'Làm rõ danh mục các loại phiếu hạch toán của hệ thống (105 loại phiếu cấu hình sẵn), mỗi loại thuộc một trong 9 Phân loại và '
    'có hay không “Hạch toán riêng”.',
    'Làm rõ màn chỉ dùng để TRA CỨU: không thêm, sửa, xóa, khóa trên giao diện — giữ đúng như hệ thống cũ.',
])
d.p('Phạm vi chức năng: Xem danh sách (sắp xếp, phân trang), Tìm kiếm và lọc theo Phân loại, Tùy chỉnh cột, Xuất Excel danh sách. Màn '
    'KHÔNG có Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Xem chi tiết, Lịch sử thay đổi, Import Excel, In (hệ thống cũ cũng chỉ có '
    'danh sách; nút Thêm mới / Xuất Excel của hệ thống cũ đã bị tắt). Bộ lọc có 2 ô nên chạy chế độ gọn: không có nút Tìm kiếm nâng '
    'cao và Cài đặt bộ lọc.')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Giúp kế toán, quản trị tra cứu nhanh tên chuẩn của từng loại phiếu (đề nghị xuất / nhập, phiếu xuất / nhập hàng, thu, chi, phiếu '
    'kế toán, dịch vụ…) và loại nào được hạch toán riêng.',
    'Dữ liệu là cấu hình cố định của hệ thống; trong phần mềm mới chưa có màn nào khác đọc ngược danh mục này (Phần 5) — các phiếu '
    'không lưu liên kết tới loại phiếu hạch toán.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Màn không gắn quyền và không giới hạn phạm vi: mọi người dùng đăng nhập đều xem được đủ 105 loại phiếu (BR-01).',
    'Không có thao tác ghi dữ liệu trên màn; mọi thay đổi danh mục chỉ do quản trị hệ thống thực hiện ngoài giao diện (BR-02).',
    'Thứ tự mặc định giữ đúng thứ tự cấu hình của hệ thống cũ (các loại phiếu đã xếp sẵn theo nhóm) (BR-05).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Loại phiếu hạch toán', 'Một dòng của danh mục: tên loại phiếu (vd “PXH - Xuất bán hàng”, “PC - Chi trả nhà cung cấp”), Phân '
                             'loại và cờ Hạch toán riêng. Màn không có mã loại phiếu; tên là trường định danh hiển thị.'),
    ('Phân loại', 'Nhóm lớn của loại phiếu, 9 giá trị cố định theo thứ tự: ' + TYPES + '.'),
    ('Hạch toán riêng', 'Cờ Có / Không: loại phiếu được hạch toán riêng thì cột hiện dấu ✓ (file Excel ghi “Có”), không thì để trống. '
                        'Hiện có 94 loại Có, 11 loại Không (các dòng tổng như “Phiếu xuất hàng”, “Phiếu thu”, “Phiếu kế toán”…).'),
    ('PXH / PNH / PT / PC', 'Viết tắt trong tên loại phiếu: Phiếu xuất hàng / Phiếu nhập hàng / Phiếu thu / Phiếu chi.'),
    ('Trạng thái bản ghi', 'Màn KHÔNG có trạng thái (không có Hoạt động / Khóa): mọi loại phiếu trong danh mục đều có hiệu lực.'),
    ('Cấu trúc phân cấp', 'Phân loại > Loại phiếu (một – nhiều). Không có cấp con khác; tên các dòng đã ngầm nhóm (dòng tổng “Phiếu '
                          'nhập hàng” rồi các dòng “PNH - …”).'),
    ('Bộ lọc gọn', 'Bộ lọc có ≤ 3 ô (ô tìm nhanh + ô Phân loại) nên bày thẳng trên một hàng, không có khối Tìm kiếm nâng cao.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn KHÔNG gắn quyền riêng (giữ như hệ thống cũ — user chốt 13/10/2026): menu luôn hiện, mọi chức năng Xem / Tìm kiếm / Tùy chỉnh '
    'cột / Xuất Excel không kiểm quyền. Dữ liệu không bó theo công ty, phòng ban hay người tạo.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('—', 'Không có quyền riêng (mọi người dùng đã đăng nhập)', 'Thấy menu và màn; dùng được Tìm kiếm, Làm mới, lọc Phân loại, sắp xếp, '
                                                               'Xuất Excel, Cấu hình cột.'),
], widths=[0.8, 2.2, 3.0])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('—', 'Không áp dụng', 'Mọi người dùng thấy cùng một danh mục 105 loại phiếu (dữ liệu cấu hình dùng chung toàn hệ thống).'),
], widths=[0.8, 2.2, 3.0])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người dùng đã đăng nhập', 'Phạm vi', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', 'Toàn bộ 105 loại phiếu', '✅ (không cần quyền)'),
    ('FR-02 Tìm kiếm và lọc', '✅', 'Toàn bộ', '✅'),
    ('FR-03 Tùy chỉnh cột', '✅', 'Cấu hình riêng từng người', '✅'),
    ('FR-04 Xuất Excel', '✅', 'Theo bộ lọc đang áp', '✅'),
    ('Thêm, Sửa, Xóa, Khóa / Mở khóa, Xem chi tiết, Lịch sử, Import, In', '—', '—', '— (màn không có chức năng này)'),
], widths=[1.9, 1.5, 1.6, 1.0])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Màn không có quyền riêng nên không có trường hợp “thiếu quyền” — người dùng nào đăng nhập cũng vào được và thấy cùng dữ liệu.',
    'Chưa đăng nhập / phiên hết hạn → hệ thống chuyển về màn đăng nhập (quy tắc chung).',
    'Không có nút nào bị ẩn theo quyền; không có nút ghi dữ liệu để ẩn.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Xuất Excel, Cấu hình cột', 'Luôn hiện', 'Không gắn quyền; Xuất Excel bị khóa trong lúc đang xuất'),
    ('Ô tìm nhanh, ô Phân loại, Tìm kiếm, Làm mới', 'Luôn hiện trên một hàng', 'Bộ lọc gọn (2 ô ≤ 3)'),
    ('Nút Tìm kiếm nâng cao, Cài đặt bộ lọc', 'Không hiện', 'Bộ lọc gọn không cần'),
    ('Nút Thêm mới, Import, cột Hành động', 'Không có', 'Màn chỉ xem (như hệ thống cũ)'),
], widths=[2.2, 2.3, 1.5])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_ND, [0, 1])],
    [('FR-01', 'Xem danh sách loại phiếu', 'view'),
     ('FR-04', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Tùy chỉnh cột', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Danh sách loại phiếu hạch toán')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách loại phiếu hạch toán',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách loại phiếu hạch toán',
       mota='Hiển thị bảng toàn bộ loại phiếu hạch toán của hệ thống (105 dòng cấu hình sẵn): tên loại phiếu, phân loại, dấu ✓ khi '
            'hạch toán riêng, kèm dòng tổng số và phân trang. Màn chỉ để tra cứu: không có cột Hành động, không có nút Thêm mới, không '
            'mở được chi tiết từng dòng.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng vào màn từ menu phân hệ Bán hàng.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống nạp cấu hình cột đã lưu của người dùng và danh sách 9 Phân loại cho ô lọc.\n'
             '3. Hệ thống lấy toàn bộ loại phiếu (không giới hạn theo công ty), giữ thứ tự cấu hình của hệ thống cũ (dòng tổng “Đề nghị '
             'xuất kho” đứng đầu, “Khác thu, chi, nhập, xuất” cuối).\n'
             '4. Hệ thống hiển thị trang 1, 10 dòng/trang, dòng “Hiển thị 1–10 / 105” và phân trang 11 trang.\n'
             '5. Người dùng bấm tiêu đề cột Loại phiếu hoặc Phân loại để sắp xếp, bấm số trang hoặc đổi Số dòng/trang để xem tiếp.',
       phu='• Đang nạp → trong bảng hiện “Đang tải dữ liệu...”.\n'
           '• Máy chủ lỗi khi nạp danh sách → thông báo ' + LOADERR + ', bảng trống.\n'
           '• Bộ lọc không khớp dòng nào → trong bảng hiện ' + EMPTY + '.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó (ẩn Phân loại / Hạch toán riêng nếu đã tắt).\n'
           '• Phiên đăng nhập hết hạn khi đang thao tác → thông báo hết phiên, chuyển về màn đăng nhập.',
       dacbiet='Cột mặc định hiện: cả 4 cột (STT, Loại phiếu, Phân loại, Hạch toán riêng); không có cột ẩn mặc định. Cột khóa (không ẩn, '
               'không đổi vị trí): STT, Loại phiếu; STT ghim trái khi cuộn ngang. Sắp xếp được: Loại phiếu (theo chữ cái), Phân loại '
               '(theo THỨ TỰ 9 phân loại Đề nghị xuất → Khác, không theo chữ cái); cùng giá trị thì giữ thứ tự cấu hình. Đổi sắp xếp / '
               'bộ lọc / số dòng đều về trang 1. Bộ lọc, sắp xếp không được ghi nhớ khi rời màn hay tải lại trang.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn Danh sách loại phiếu hạch toán'),
   extra=[(shot('00_menu'), 'Vị trí mục menu: phân hệ Bán hàng › Quy chế - Thiết lập › Thiết lập'),
          (shot('03_sort'), 'Danh sách đang sắp xếp giảm dần theo Phân loại')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- “Danh sách loại phiếu hạch toán” trên thanh tiêu đề trang, tiêu đề bảng và tab trình duyệt']),
       ('Khối Bộ lọc danh sách', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- Ô tìm nhanh, ô Phân loại, nút Tìm kiếm, Làm mới trên một hàng', '- Chi tiết ở mục 2.2']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Luôn hiện (không gắn quyền)', '- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.4)', '- Khóa trong lúc đang xuất']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
        ['- Biểu tượng cột, rê chuột: “Cấu hình cột hiển thị”', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.3)']),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Đánh số liên tục theo trang (trang 2 bắt đầu 11)', '- Cột khóa, ghim trái']),
       ('Cột Loại phiếu', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Tên loại phiếu, xuống dòng khi dài', '- Không bấm được (màn không có chi tiết)', '- Sắp xếp được theo chữ cái', '- Cột khóa']),
       ('Cột Phân loại', 'Table/Grid', 'Read-only', '9 giá trị', 'Hiển thị',
        ['- Một trong: ' + TYPES, '- Sắp xếp được theo thứ tự phân loại (Đề nghị xuất trước, Khác sau)']),
       ('Cột Hạch toán riêng', 'Table/Grid', 'Read-only', 'Có hoặc Không', 'Hiển thị',
        ['- Căn giữa', '- Có: dấu ✓ màu xanh, rê chuột hiện “Có”', '- Không: ô trống (không in số 0)', '- Không sắp xếp']),
       ('Trạng thái đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- Trong bảng: “Đang tải dữ liệu...” khi đang nạp.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', ['- Trong bảng: ' + EMPTY, '- Chỉ hiện khi N = 0']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự dòng đầu – cuối của trang đang xem', '- N: tổng loại phiếu khớp bộ lọc (không lọc: 105)']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5, 10, 20, 50, 100', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5 / 10 / 20 / 50 / 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
        ['- Nút « ‹ số trang … › »', '- Ở trang đầu « ‹ mờ; ở trang cuối › » mờ']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- ' + LOADERR + ' khi máy chủ lỗi.'),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Không kiểm quyền (màn không gắn quyền).\n– Không giới hạn phạm vi theo công ty / phòng ban.\n'
        'During:\n– Nạp cấu hình cột của người dùng, danh sách 9 Phân loại cho ô lọc.\n'
        '– Lấy loại phiếu theo thứ tự cấu hình (thứ tự hệ thống cũ).\n– Máy chủ lỗi → hiển thị ' + LOADERR + '.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, “Hiển thị 1–10 / 105”; bộ lọc trống, chưa cột nào sắp xếp.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ Loại phiếu và Phân loại hỗ trợ sắp xếp.\n'
        'During:\n– Loại phiếu: theo chữ cái (không phân biệt hoa / thường). Phân loại: theo thứ tự 9 phân loại.\n'
        'After:\n– Lần 1 tăng dần (mũi tên lên), lần 2 giảm dần (mũi tên xuống); nạp lại từ trang 1, giữ bộ lọc; cùng giá trị giữ '
        'thứ tự cấu hình.'),
       ('Bấm số trang hoặc nút « ‹ › »', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1 và nạp lại một lần theo số dòng mới (vd 100 dòng → 2 trang).'),
       ('Rời màn rồi quay lại / tải lại trang', 'System',
        'Before:\n– Màn không có trang con nên bộ lọc không được ghi nhớ.\n'
        'After:\n– Bộ lọc, ô tìm nhanh, sắp xếp, trang về mặc định; cấu hình cột vẫn giữ (lưu theo người dùng).'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc loại phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách loại phiếu hạch toán',
       mota='Thu hẹp danh sách theo tên loại phiếu (ô tìm nhanh) và Phân loại (ô chọn 9 giá trị). Bộ lọc chỉ có 2 ô nên bày thẳng trên '
            'một hàng cạnh nút Tìm kiếm, Làm mới; không có khối Tìm kiếm nâng cao và nút Cài đặt bộ lọc.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập chữ vào ô tìm nhanh “Tìm theo loại phiếu...” rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc người dùng chọn một giá trị ở ô Phân loại.\n'
             '3. Hệ thống lọc ngay khi ô Phân loại đổi giá trị, về trang 1; ô tìm nhanh chỉ áp khi bấm Tìm kiếm / Enter.\n'
             '4. Hệ thống nạp lại danh sách theo mọi điều kiện (kiểu VÀ), cập nhật dòng “Hiển thị a–b / N” và phân trang.\n'
             '5. Người dùng bấm Làm mới để xóa toàn bộ điều kiện và xem lại đủ 105 loại phiếu.',
       phu='• Bấm Làm mới → xóa ô tìm nhanh, ô Phân loại, bỏ sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → bảng hiện ' + EMPTY + '.\n'
           '• Bấm × trong ô tìm nhanh → xóa chữ; danh sách chỉ đổi khi bấm Tìm kiếm / Enter.\n'
           '• Bấm × trong ô Phân loại → bỏ lọc phân loại, danh sách nạp lại ngay.\n'
           '• Đã gõ chữ nhưng chưa bấm Tìm kiếm mà đổi Phân loại / sắp xếp / sang trang → chữ đang gõ cũng được áp theo.',
       dacbiet='Ô tìm nhanh khớp MỘT PHẦN tên loại phiếu, không phân biệt hoa / thường và không phân biệt dấu (theo cách so sánh chữ của '
               'cơ sở dữ liệu: “xuat thang” ra cùng 16 dòng như “xuất thẳng”); bỏ khoảng trắng đầu / cuối; không giới hạn số ký tự; '
               'ký tự % và _ được tìm đúng nghĩa đen. Bộ lọc KHÔNG được ghi nhớ khi rời màn / tải lại trang.'),
   layout=dict(menu=MENU + ' => Bộ lọc danh sách', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách: tìm “PT” và Phân loại = Thu'),
   extra=[(shot('02b_filter_full'), 'Kết quả lọc: 3 loại phiếu thu “PT - …”'),
          (shot('04_empty'), 'Không có loại phiếu phù hợp bộ lọc')],
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo loại phiếu...”', '- Khớp một phần tên Loại phiếu', '- Áp khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút × trong ô tìm nhanh', 'Icon Button', 'Enable', '–', '–', 'Ẩn',
        ['- Chỉ hiện khi ô có chữ', '- Bấm → xóa chữ, chưa nạp lại danh sách']),
       ('Ô Phân loại', 'Dropdown', 'Enable', '9 giá trị', 'Không', 'Trống', [
           '- Mặc định: trống (gợi ý “Phân loại”)', '- Lựa chọn: ' + TYPES, '- Chọn một giá trị → lọc ngay, về trang 1',
           '- Có giá trị thì nhãn “Phân loại” nổi lên viền trên ô']),
       ('Nút × trong ô Phân loại', 'Icon Button', 'Enable', '–', '–', 'Ẩn', ['- Chỉ hiện khi đã chọn', '- Bấm → bỏ lọc, nạp lại ngay']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Bấm → xóa ô tìm nhanh và ô Phân loại', '- Bỏ sắp xếp, nạp lại từ trang 1']),
       ('Kết quả lọc', 'Table/Grid', 'Read-only', '–', '–', 'Theo kết quả', '- Bảng cập nhật theo tiêu chí, STT đánh lại từ 1.'),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', '–', 'Theo kết quả',
        ['- N = số loại phiếu khớp bộ lọc', '- Vd Phân loại = Thu: “Hiển thị 1–5 / 5”']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- Trong bảng: ' + EMPTY),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + LOADERR + ' khi máy chủ lỗi.'),
   ],
   ev=[
       ('Chọn giá trị ô Phân loại', 'Change',
        'Before:\n– Bỏ qua khi giá trị không đổi.\n'
        'During:\n– Lấy loại phiếu thuộc phân loại đã chọn (kết hợp chữ đang có trong ô tìm nhanh).\n'
        'After:\n– Về trang 1, nạp lại danh sách một lần, cập nhật tổng số.'),
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, bỏ khoảng trắng đầu / cuối.\n'
        'During:\n– Tìm loại phiếu có tên chứa chuỗi nhập (không phân biệt hoa / thường, dấu); % và _ hiểu đúng nghĩa đen.\n'
        '– Máy chủ lỗi → ' + LOADERR + '.\n'
        'After:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số; không khớp → ' + EMPTY + '.'),
       ('Gõ vào ô tìm nhanh (chưa bấm Tìm kiếm)', 'Change',
        'Before:\n– Chỉ đổi chữ trong ô tìm nhanh.\nAfter:\n– Danh sách chưa đổi cho tới khi bấm Tìm kiếm / Enter (hoặc đổi Phân '
        'loại / sắp xếp / trang).'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\nAfter:\n– Xóa ô tìm nhanh, ô Phân loại, bỏ sắp xếp, nạp lại từ trang 1 '
        '(“Hiển thị 1–10 / 105”).'),
       ('Bấm × trong ô Phân loại', 'Click',
        'Before:\n– Ô Phân loại đang có giá trị.\nAfter:\n– Bỏ lọc phân loại, về trang 1, nạp lại ngay.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 4 cột của bảng danh sách. Hai cột STT, Loại phiếu bị khóa; cấu hình lưu '
            'riêng theo người dùng trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, bộ lọc hay tổng số.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị (biểu tượng cột cạnh Xuất Excel).\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 4 cột theo cấu hình đang lưu, dòng “Đang chọn 4/4 cột”.\n'
             '3. Người dùng tích / bỏ tích Phân loại, Hạch toán riêng; kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa (2 cột khóa luôn tích); chưa lưu.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”, cấu hình cũ giữ nguyên.\n'
           '• Cột đã ẩn thì cũng không được tích sẵn ở cửa sổ Xuất Excel.',
       dacbiet='Mặc định hiện đủ 4 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ nguyên sau khi tải lại trang, đăng nhập '
               'lại, đổi trình duyệt; người dùng khác không bị ảnh hưởng. Cột đang hiện quyết định trường tích sẵn ở cửa sổ Xuất Excel.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 4 cột', '–', 'Theo cấu hình đã lưu',
        ['- STT, Loại phiếu, Phân loại, Hạch toán riêng']),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', ['- Phân loại, Hạch toán riêng', '- Bỏ tích → cột ẩn khỏi bảng']),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Loại phiếu', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → bỏ tích mọi cột không khóa (còn 2/4).'),
       ('Dòng “Đang chọn n/4 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '- n = số cột đang tích.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình cột đang lưu của người dùng (chưa lưu lần nào → đủ 4 cột).'),
       ('Kéo biểu tượng kéo thả', 'Drag',
        'Before:\n– Cột khóa không đổi được vị trí.\nAfter:\n– Đổi thứ tự cột trong danh sách; chưa áp lên bảng.'),
       ('Tích / bỏ tích một cột', 'Change', 'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/4 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách cột đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng; dữ liệu, bộ lọc, tổng số giữ nguyên.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ đúng cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.4 Xuất Excel
fr(4, 'Xuất Excel danh sách', usecase=('FR-04', 'Xuất Excel', 'io', A_ND),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất Excel danh sách loại phiếu hạch toán',
       mota='Xuất danh sách loại phiếu theo bộ lọc và thứ tự sắp xếp đang áp ra file Excel; người dùng chọn trường và thứ tự cột. File '
            'dựng theo khuôn chung các màn danh sách: letterhead công ty người xuất, tiêu đề, bảng, khối ký.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Danh sách loại phiếu hạch toán.',
       chinh='1. Người dùng lọc / sắp xếp danh sách theo nhu cầu rồi bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất file” liệt kê 3 trường Loại phiếu, Phân loại, Hạch toán riêng, tích sẵn các trường '
             'đang hiện trên bảng (mặc định đủ 3, “Đang chọn 3/3 trường”).\n'
             '3. Người dùng tích / bỏ tích, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống tải MỌI loại phiếu khớp bộ lọc (không theo trang đang xem), đúng thứ tự sắp xếp đang áp.\n'
             '5. Hệ thống tạo file danh_sach_loai_phieu_hach_toan.xlsx (trang “Loai phieu hach toan”): letterhead công ty người xuất, '
             'tiêu đề “DANH SÁCH LOẠI PHIẾU HẠCH TOÁN”, cột STT + các trường đã chọn đúng thứ tự, khối ký “Ngày ..., tháng ..., năm '
             '...” / “Người lập”.\n'
             '6. Hệ thống tải file về và hiển thị “Xuất Excel thành công.”.',
       phu='• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Danh sách theo bộ lọc rỗng → thông báo “Không có dữ liệu để xuất”, KHÔNG tạo file.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài cửa sổ chọn trường → không xuất.\n'
           '• Lỗi khi xuất → thông báo “Lỗi khi xuất Excel”, không tải file.',
       dacbiet='Hạch toán riêng ghi chữ “Có” hoặc để trống (không ghi 0). Hàng tiêu đề cột không gắn nút lọc (user yêu cầu 15/10/2026). '
               'Letterhead trải bằng bề rộng bảng. Nút Xuất Excel khóa trong lúc đang xuất (chống bấm kép). Xuất không ghi lịch sử.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất file”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 3 trường', '–', 'Theo cột đang hiện',
        ['- Loại phiếu, Phân loại, Hạch toán riêng', '- Cột STT luôn có trong file (không nằm trong danh sách)']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích',
        ['- Mặc định tích các trường đang hiện trên bảng (cấu hình mặc định: cả 3)', '- Bỏ tích → trường không có trong file']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích cả 3 trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/3 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Khóa khi chưa tích trường nào hoặc đang xuất', '- Bấm → tải file danh sách']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng cửa sổ, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('File Excel', 'Table/Grid', 'Read-only', '.xlsx', '–', '–',
        ['- Tên danh_sach_loai_phieu_hach_toan.xlsx', '- Letterhead công ty người xuất trải bằng bề rộng bảng',
         '- Tiêu đề, STT + trường đã chọn đúng thứ tự, khối ký “Người lập”', '- Hàng tiêu đề cột không có nút lọc']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Xuất Excel thành công.”', '- “Không có dữ liệu để xuất”', '- “Lỗi khi xuất Excel”']),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Không cần quyền riêng; bỏ qua nếu đang có lượt xuất chạy.\n– Lấy bộ lọc + sắp xếp đang áp.\n'
        'After:\n– Mở cửa sổ chọn trường, tích sẵn các cột đang hiện.'),
       ('Tích / bỏ tích, kéo thả trường', 'Change',
        'Before:\n– Trong cửa sổ chọn trường.\nAfter:\n– Cập nhật “Đang chọn n/3 trường”; 0 trường → khóa Xuất file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Ít nhất 1 trường được tích; khóa nút Xuất Excel trong lúc xuất.\n'
        'During:\n– Tải tuần tự mọi trang dữ liệu khớp bộ lọc, theo thứ tự sắp xếp đang áp; 0 dòng → “Không có dữ liệu để xuất”, '
        'dừng, không tạo file.\n– Lấy letterhead công ty của người đăng nhập.\n– Lỗi → “Lỗi khi xuất Excel”.\n'
        'After:\n– Dựng file (STT + trường đã chọn, Hạch toán riêng ghi “Có” / trống), tải về, hiển thị “Xuất Excel thành công.”; '
        'mở lại nút Xuất Excel; không ghi lịch sử.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Danh sách loại phiếu hạch toán; không lặp lại các quy tắc đã có trong '
           'SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Không gắn quyền, không giới hạn phạm vi', [
        '– Ai đăng nhập cũng vào màn và dùng mọi chức năng (giữ như hệ thống cũ, user chốt 13/10/2026).',
        '– Mọi người dùng thấy cùng 105 loại phiếu, không bó theo công ty / phòng ban / người tạo.'],
     ['Xem danh sách', 'Tìm kiếm và lọc', 'Xuất Excel']),
    ('BR-02', 'Dữ liệu cấu hình cố định, chỉ xem', [
        '– Màn không có Thêm / Sửa / Xóa / Khóa / Import; danh mục chép nguyên từ hệ thống cũ.',
        '– Không có trạng thái, người tạo, ngày tạo; mọi loại phiếu đều có hiệu lực.'],
     ['Xem danh sách']),
    ('BR-03', 'Phân loại', [
        '– 9 giá trị cố định theo thứ tự: ' + TYPES + '.',
        '– Số loại phiếu hiện có: Đề nghị xuất 20, Đề nghị nhập 23, Xuất hàng 21, Nhập hàng 24, Thu 5, Chi 8, Phiếu kế toán 1, Dịch '
        'vụ 2, Khác 1.'],
     ['Xem danh sách', 'Tìm kiếm và lọc']),
    ('BR-04', 'Hạch toán riêng', [
        '– Có: dấu ✓ trên bảng, chữ “Có” trong file Excel; Không: để trống (không hiện 0).',
        '– Hiện có 94 loại Có, 11 loại Không.'],
     ['Xem danh sách', 'Xuất Excel']),
    ('BR-05', 'Thứ tự và sắp xếp', [
        '– Mặc định giữ thứ tự cấu hình của hệ thống cũ (đã xếp theo nhóm phiếu).',
        '– Loại phiếu sắp theo chữ cái; Phân loại sắp theo thứ tự 9 phân loại (không theo chữ cái); cùng giá trị giữ thứ tự cấu hình.'],
     ['Xem danh sách', 'Xuất Excel']),
    ('BR-06', 'Tìm kiếm', [
        '– Khớp một phần tên loại phiếu, không phân biệt hoa / thường, dấu; bỏ khoảng trắng đầu / cuối; % và _ đúng nghĩa đen.',
        '– Kết hợp với Phân loại theo kiểu VÀ; bộ lọc không được ghi nhớ khi rời màn.'],
     ['Tìm kiếm và lọc']),
    ('BR-07', 'Quy tắc ghi lịch sử', [
        '– Màn không có thao tác ghi dữ liệu nên không có lịch sử thay đổi; xem / lọc / xuất không ghi lịch sử.'],
     ['Xem danh sách', 'Xuất Excel']),
    ('BR-08', 'Xuất Excel', [
        '– Xuất mọi loại phiếu khớp bộ lọc và đúng thứ tự sắp xếp, không giới hạn; rỗng → không tạo file.',
        '– Letterhead theo công ty người xuất; không gắn nút lọc ở hàng tiêu đề.'],
     ['Xuất Excel']),
    ('BR-09', 'Sử dụng ở màn khác', [
        '– Không màn nào của phần mềm mới đọc danh mục này; phiếu không lưu liên kết tới loại phiếu hạch toán.',
        '– Màn gốc của hệ thống ERP đọc cùng dữ liệu (Phần 5).'],
     ['Xem danh sách']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Danh sách loại phiếu hạch toán (105 loại phiếu cấu hình sẵn). Trong phần mềm '
    'mới không có màn nào khác đọc danh mục này.')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Hệ thống ERP', 'Danh sách loại phiếu hạch toán (màn gốc ở Quản trị hệ thống › Cấu hình ERP — chỉ đọc cùng danh mục, không '
                          'sửa; danh mục không có thao tác ghi nên không ảnh hưởng ngược)',
     'Hệ thống ERP -> Quản trị hệ thống -> Cấu hình ERP'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)

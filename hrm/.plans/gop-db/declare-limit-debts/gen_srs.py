# -*- coding: utf-8 -*-
"""SRS màn "Khai báo hạn mức công nợ KH" (danh sách cây Khách hàng → dòng theo công ty, sửa thẳng trong bảng + Lưu từng khách)
— form chuẩn Danh mục quốc gia, chuẩn 04/11/2026 (Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột STT | Nhóm | Màn hình |
Đường dẫn).

Chạy: python gen_srs.py  → SRS - Khai báo hạn mức công nợ KH.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc ../benefit-rates/gen_srs.py
  (06/11/2026); đường dẫn menu Tài chính theo ../phieu-xuat-hang-dieu-chinh-kiem-ke/gen_srs.py; tên gọi cột thống nhất với
  ../report-limit-debts (Báo cáo hạn mức công nợ khách hàng).
Nguồn đọc 18/11/2026 (nhánh develop, con của gop_db, cả 2 repo):
  BE  Modules/Finance/{Services/CustomerDebt/DeclareLimitDebtService.php (phạm vi, dòng hiện, lưu xoá-ghi lại, lịch sử changedRows,
      exportRows), Http/Controllers/V1/DeclareLimitDebtController.php (validate + câu lỗi), Routes/api.php (/declare-limit-debts: 4 route
      xem KHÔNG gate, PUT gate finance.khai_bao_han_muc_cong_no_khach_hang.manage)}, app/Support/Permissions/Catalog/finance.php,
      app/Services/CatalogHistoryService.php (khoá ảo customer_limit_debts), app/Http/Middleware/CheckPermission.php.
      Nơi đọc hạn mức: Services/CustomerDebt/ReportLimitDebtService.php, Modules/Assign/Services/ProductExportOverLimitService.php,
      Services/BorrowSellRequest/BorrowSellRequestService.php::isOverLimit (+ BorrowSellRequestCalculator::isOverLimitDebt).
  FE  pages/finance/declare-limit-debts/index.vue (1 file), components/subsystem-menu/finance.js (Kế toán công nợ › Khách hàng),
      V2BaseSmartFilterPanel (≤ 3 ô → hiện thẳng, không có Cài đặt bộ lọc / Tìm kiếm nâng cao), V2BaseDataTable (cellSpan, phân trang),
      utils/mixins/{filterStateMixin, unsavedChangesMixin, exportFieldsMixin, columnCustomizationMixin}.js, components/modal/
      {CatalogHistoryModal, export-fields-modal, column-customization-modal}.vue, utils/export/listExportFile.js, plugins/axios.js.
  Bối cảnh: design.md, plan.md (Phase 1–6, #11717, #11775, #11900), spec docs/superpowers/specs/gop-db/2026-10-14-declare-limit-debts-design.md.
Ảnh: ./kbhmcn_shots — dev-hrm 18/11/2026 (_capture/capture.js, DNS Admin, chặn mọi yêu cầu ghi: 0 yêu cầu ghi). Dữ liệu thật của dev
  (khách 43TPHDKH có hạn mức + lịch sử). Riêng 10b_validate: lỗi dưới ô GIẢ LẬP trên trình duyệt (gán đúng câu lỗi của code, không bấm Lưu).
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

TEN = 'Khai báo hạn mức công nợ KH'
SHOTS = os.path.join(HERE, 'kbhmcn_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Tài chính => Kế toán công nợ => Khách hàng => Khai báo hạn mức công nợ KH'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Khai báo hạn mức công nợ KH.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
Q_VIEW = 'Xem khai báo hạn mức công nợ khách hàng'
Q_MAN = 'Quản lý khai báo hạn mức công nợ khách hàng'
NOPERM_ROW = '“Bạn không có quyền sửa hạn mức của khách hàng này.”'
NOPERM = '“Bạn không có quyền thực hiện chức năng này”'
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
SYS = '“Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”'
CHECK = '“Vui lòng kiểm tra lại dữ liệu nhập”'
TYPE_REQ = '“Vui lòng chọn cách tính lãi”'
MAXE = '“Không được lớn hơn 999,999,999,999,999”'
OK = '“Cập nhật thành công.”'

A_ND = 'Kế toán công nợ (quyền Quản lý)'
A_XEM = 'Người dùng xem hạn mức'
TN_XEM = ('Người dùng có quyền thực hiện chức năng: mọi người dùng đã được cấp tài khoản (màn không chặn quyền xem, giữ như hệ thống '
          'cũ). Quyền “%s” / “%s” chỉ quyết định thấy dòng của công ty nào.' % (Q_VIEW, Q_MAN))
TN_SUA = ('Người dùng có quyền thực hiện chức năng: “%s” — chỉ sửa được dòng hạn mức của CÔNG TY người đăng nhập.' % Q_MAN)
DK = ('1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn Khai báo hạn mức công nợ KH.\n'
      '3. Có ít nhất 1 khách hàng trong danh mục Khách hàng.')

d = SrsDoc(out=OUT, menu=MENU, route='/finance/declare-limit-debts', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Kế toán công nợ': 'menu_ketoancongno', 'Khách hàng': 'menu_nhom_kh',
    'Khai báo hạn mức công nợ KH': 'menu_muc',
    'Tìm kiếm': 'btn_timkiem', 'Cấu hình cột': 'btn_cauhinhcot', 'Lưu': 'btn_luu_row',
    'Lịch sử': 'btn_lichsu_row', 'Xuất Excel': 'btn_xuatexcel',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Khai báo hạn mức công nợ KH (tiêu đề trên màn: “Khai báo hạn mức công nợ khách '
    'hàng”), chuyển từ hệ thống cũ (Kế toán › Kế toán Công nợ › Khách hàng) sang phân hệ Tài chính, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phạm vi dữ liệu và luồng xử lý của màn hình.',
    'Làm rõ cách mỗi công ty khai cho từng khách hàng: Cách tính lãi, Hạn mức công nợ tính lãi và Hạn mức công nợ xuất hàng — sửa '
    'thẳng trên bảng danh sách và bấm Lưu theo từng khách (giữ như hệ thống cũ).',
    'Làm rõ ai thấy dòng của công ty nào, ai sửa được dòng nào, và hai hành vi lưu / hiện dòng được giữ nguyên như hệ thống cũ.',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Tùy chỉnh cột, Khai báo / chỉnh sửa hạn mức (sửa trong bảng + Lưu từng khách, '
    'cảnh báo rời màn khi chưa lưu), Xem lịch sử thay đổi, Xuất Excel danh sách. Màn KHÔNG có Thêm mới, Xóa, Khóa / Mở khóa, Xem chi '
    'tiết, Import Excel, In (hệ thống cũ cũng không có): dữ liệu gắn theo khách hàng có sẵn ở danh mục Khách hàng.')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Hạn mức công nợ xuất hàng là ngưỡng dư nợ được phép của khách với công ty: khi gửi duyệt Yêu cầu xuất hàng (loại Xuất bán hàng, '
    'Xuất bán SC - BD) hoặc Yêu cầu xuất bán hàng mượn, công nợ của khách + giá trị phiếu vượt hạn mức thì phiếu phải qua Trưởng phòng '
    '/ Ban giám đốc duyệt.',
    'Hạn mức công nợ tính lãi và Hạn mức công nợ xuất hàng được đọc ở Báo cáo hạn mức công nợ khách hàng (chỉ dòng của công ty người '
    'xem, có ít nhất một hạn mức > 0).',
    'Cách tính lãi hiện chỉ được lưu, hiển thị, xuất Excel và ghi lịch sử — trên hệ thống mới chưa màn nào dùng để tính lãi.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Xem không cần quyền; quyền Xem / Quản lý quyết định thấy dòng của công ty nào (BR-01).',
    'Chỉ người có quyền Quản lý mới sửa được, và chỉ dòng của công ty mình (BR-03).',
    'Khách đã có dòng hạn mức thì chỉ hiện các dòng đã có; chưa có dòng nào mới hiện đủ các công ty (BR-02, giữ như hệ thống cũ).',
    'Lưu = xoá hết dòng hạn mức của khách rồi ghi lại các dòng đang hiện với người lưu (BR-04, giữ như hệ thống cũ).',
    'Có Hạn mức công nợ tính lãi thì bắt buộc chọn Cách tính lãi; hạn mức là số nguyên 0 – 999,999,999,999,999 (BR-05).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Dòng khách hàng', 'Nhóm ô STT, Mã khách hàng, Tên khách hàng, MST/CMND và Hành động — gộp dọc trên tất cả dòng công ty của khách.'),
    ('Dòng công ty (dòng hạn mức)', 'Một dòng của bảng: hạn mức khai cho khách tại MỘT công ty (cột Khai báo theo công ty). Mỗi khách × '
                                    'công ty tối đa 1 dòng.'),
    ('Cách tính lãi', 'Danh sách 2 giá trị: Theo vượt hạn mức công nợ / Theo thời gian thanh toán. Để trống được, trừ khi có Hạn mức '
                      'công nợ tính lãi.'),
    ('Hạn mức công nợ tính lãi', 'Số tiền (VNĐ, số nguyên ≥ 0, tối đa 999,999,999,999,999). Để trống = chưa khai.'),
    ('Hạn mức công nợ xuất hàng', 'Số tiền (VNĐ, số nguyên ≥ 0, tối đa 999,999,999,999,999); ngưỡng kiểm vượt hạn mức khi gửi duyệt '
                                   'phiếu xuất. Trống hoặc 0 = không kiểm.'),
    ('MST/CMND', 'Mã số thuế của khách; khách không có mã số thuế thì hiện số CMND.'),
    ('Công ty mình', 'Công ty của người đăng nhập (công ty đang làm việc). Chỉ dòng công ty mình mới sửa được.'),
    ('Đang sửa dở', 'Khách có giá trị trong ô nhập khác giá trị đã lưu, chưa bấm Lưu.'),
    ('Trạng thái bản ghi', 'Màn KHÔNG có trạng thái (không có Hoạt động / Khóa, không có duyệt): dòng hạn mức có giá trị là có hiệu lực '
                           'ngay; để trống là chưa khai.'),
    ('Cấu trúc phân cấp', 'Khách hàng > các dòng hạn mức theo công ty (một – nhiều; mỗi công ty tối đa 1 dòng).'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn KHÔNG chặn quyền xem (giữ như hệ thống cũ — user chốt 14/10/2026): menu luôn hiện, ai đăng nhập cũng vào được và thấy dòng '
    'hạn mức của mọi công ty. Hai quyền dưới đây (phân hệ Tài chính, chức năng Khách hàng) chỉ thay đổi phạm vi dòng và quyền sửa.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q_VIEW, 'Thấy dòng hạn mức của MỌI công ty (chỉ có tác dụng khi đi cùng Q2 — không có Q2 thì vốn đã thấy mọi công ty). '
                   'Không cho sửa.'),
    ('Q2', Q_MAN, 'Sửa được Cách tính lãi, 2 hạn mức ở dòng công ty mình; hiện nút Lưu của khách. Không có Q1 thì chỉ thấy dòng công ty '
                  'mình.'),
], widths=[0.8, 2.2, 3.0])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Không có quyền nào / chỉ Q1 / Q1 + Q2', 'Mọi khách hàng; dòng hạn mức của mọi công ty.'),
    ('V2', 'Chỉ Q2 (không có Q1)', 'Mọi khách hàng; chỉ dòng hạn mức của công ty mình (khách chưa có dòng công ty mình thì hiện 1 dòng '
                                   'trống của công ty mình — xem BR-02).'),
], widths=[0.8, 2.2, 3.0])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ mọi công ty', '✅ (không có Q1: chỉ công ty mình)', '✅ mọi công ty'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅'),
    ('FR-03 Tùy chỉnh cột', '✅', '✅', '✅'),
    ('FR-04 Khai báo / chỉnh sửa hạn mức', '❌ (chỉ xem)', '✅ dòng công ty mình', '❌ (chỉ xem)'),
    ('FR-05 Xem lịch sử thay đổi', '✅', '✅', '✅'),
    ('FR-06 Xuất Excel', '✅ mọi công ty', '✅ theo phạm vi dòng đang thấy', '✅ mọi công ty'),
    ('Thêm mới, Xóa, Khóa / Mở khóa, Xem chi tiết, Import, In', '—', '—', '— (màn không có chức năng này)'),
], widths=[2.1, 1.2, 1.6, 1.1])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có Q2 → mọi ô hạn mức hiện dạng chữ, không có nút Lưu; vẫn xem, lọc, xem lịch sử, xuất Excel được.',
    'Gửi lưu khi không có Q2 (vd quyền vừa bị thu hồi trong lúc đang mở màn) → hệ thống từ chối, báo ' + NOPERM + '.',
    'Có Q2 nhưng khách không có dòng công ty mình đang hiện → hệ thống từ chối, báo ' + NOPERM_ROW,
    'Tài khoản Super admin KHÔNG được đặc cách: quyền tính theo vai trò được cấp như người dùng khác.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Ô nhập Cách tính lãi, 2 ô hạn mức', 'Có Q2 + dòng là công ty mình', 'Dòng khác hiện chữ (Read-only)'),
    ('Nút Lưu (đĩa mềm) của khách', 'Khách có dòng công ty mình sửa được', 'Khóa trong lúc đang lưu'),
    ('Nút Lịch sử (đồng hồ)', 'Mọi khách', 'Không cần quyền'),
    ('Nút Xuất Excel, Cấu hình cột', 'Luôn hiện', 'Không cần quyền'),
    ('Nút Cài đặt bộ lọc, Tìm kiếm nâng cao', 'Không hiện', 'Bộ lọc chỉ có ô tìm nhanh + ô Khách hàng (≤ 3 ô) nên hiện thẳng'),
], widths=[2.2, 2.3, 1.5])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_ND, [0, 1, 2]), (A_XEM, [0, 2])],
    [('FR-01', 'Xem danh sách hạn mức', 'view'),
     ('FR-04', 'Khai báo / chỉnh sửa hạn mức', 'crud'),
     ('FR-06', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Tùy chỉnh cột', 'view', 'extend', [0], None),
     ('FR-05', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Khai báo hạn mức công nợ KH')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách hạn mức công nợ khách hàng',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách hạn mức công nợ theo khách hàng',
       mota='Hiển thị mọi khách hàng trong danh mục Khách hàng dạng 2 tầng: mỗi khách một nhóm dòng, mỗi dòng là hạn mức khai cho '
            'khách tại một công ty (Cách tính lãi, Hạn mức công nợ tính lãi, Hạn mức công nợ xuất hàng). Ô STT, Mã, Tên, MST/CMND, '
            'Hành động gộp dọc theo khách. Dòng công ty mình hiện ô nhập nếu người dùng có quyền Quản lý.',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng vào màn từ menu phân hệ Tài chính.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống xác định quyền Xem / Quản lý và công ty của người đăng nhập.\n'
             '3. Hệ thống lấy mọi khách hàng, khách tạo gần nhất ở trên; trang 1, 10 khách/trang.\n'
             '4. Với mỗi khách, hệ thống lấy các dòng hạn mức trong phạm vi được thấy; khách chưa có dòng nào thì dựng sẵn mỗi công ty '
             'một dòng trống (BR-02).\n'
             '5. Hệ thống nạp danh sách Cách tính lãi, cấu hình cột đã lưu và khôi phục bộ lọc đã dùng trong 10 phút gần nhất.\n'
             '6. Hệ thống hiển thị bảng, dòng “Hiển thị a–b / N” và phân trang.',
       phu='• Không có khách nào khớp → trong bảng hiện “Không có dữ liệu phù hợp.”, dưới bảng hiện “Không có khách hàng nào.”.\n'
           '• Máy chủ lỗi khi nạp danh sách → thông báo “Lỗi khi tải dữ liệu”, bảng trống.\n'
           '• Người dùng không có quyền Quản lý → mọi ô là chữ, không có nút Lưu.\n'
           '• Khách đã có dòng nhưng không có dòng công ty mình → không có ô nhập, không có nút Lưu ở khách đó (giữ như hệ thống cũ).\n'
           '• Phiên đăng nhập hết hạn khi đang thao tác → thông báo hết phiên, chuyển về màn đăng nhập.',
       dacbiet='Cột mặc định hiện: cả 9 cột; không có cột ẩn mặc định. Cột khóa (không ẩn, không đổi vị trí): STT, Mã khách hàng, Hành '
               'động; STT và Mã khách hàng ghim trái khi cuộn ngang. Sắp xếp được: Mã khách hàng, Tên khách hàng. Đổi sắp xếp / bộ lọc '
               '/ số dòng / trang thì phần đang sửa dở bị bỏ, không hỏi (giữ như hệ thống cũ). Nền xám nhạt xen kẽ theo KHÁCH.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn Khai báo hạn mức công nợ khách hàng'),
   extra=[(shot('00_menu_panel'), 'Vị trí mục menu: phân hệ Tài chính › Kế toán công nợ › Khách hàng')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- “Khai báo hạn mức công nợ khách hàng” trên thanh tiêu đề trang, tiêu đề bảng và tab trình duyệt',
         '- Mục menu ghi gọn “Khai báo hạn mức công nợ KH”']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Luôn hiện (không cần quyền)', '- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.6)', '- Khóa trong lúc đang xuất']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.3).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Đánh số theo KHÁCH, liên tục giữa các trang', '- Gộp dọc trên các dòng công ty của khách', '- Cột khóa, ghim trái']),
       ('Cột Mã khách hàng', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Mã trong danh mục Khách hàng; gộp dọc theo khách', '- Sắp xếp được', '- Cột khóa, ghim trái']),
       ('Cột Tên khách hàng', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Tên đầy đủ, xuống dòng khi dài; gộp dọc theo khách', '- Sắp xếp được']),
       ('Cột MST/CMND', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Mã số thuế; không có thì số CMND; không có cả hai thì trống', '- Không sắp xếp']),
       ('Cột Khai báo theo công ty', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Tên công ty của dòng hạn mức', '- Khách chưa có dòng nào: liệt kê mọi công ty trong hệ thống, thứ tự theo công ty',
         '- Không sắp xếp']),
       ('Cột Cách tính lãi', 'Dropdown', 'Enable / Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu',
        ['- Dòng công ty mình + có quyền Quản lý: ô chọn, gợi ý “Chọn cách tính lãi”, có nút × để bỏ chọn',
         '- Lựa chọn: Theo vượt hạn mức công nợ / Theo thời gian thanh toán', '- Mặc định: giá trị đã lưu (chưa khai: trống)',
         '- Dòng khác: chữ, trống khi chưa khai']),
       ('Cột Hạn mức công nợ tính lãi', 'Textbox', 'Enable / Read-only', '0 – 999,999,999,999,999', 'Theo dữ liệu',
        ['- Dòng sửa được: ô số, gợi ý “Nhập hạn mức công nợ tính lãi”, tự thêm dấu phẩy ngăn nghìn, không nhận số lẻ',
         '- Dòng khác: chữ căn phải dạng 1,234,567; chưa khai thì trống (hệ thống cũ in 0)']),
       ('Cột Hạn mức công nợ xuất hàng', 'Textbox', 'Enable / Read-only', '0 – 999,999,999,999,999', 'Theo dữ liệu',
        ['- Như cột Hạn mức công nợ tính lãi, gợi ý “Nhập hạn mức công nợ xuất hàng”']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Gộp dọc theo khách', '- Nút Lưu (đĩa mềm, màu xanh ngọc, chú thích “Lưu”): chỉ ở khách có dòng sửa được → mục 2.4',
           '- Nút Lịch sử (đồng hồ, chú thích “Lịch sử”): mọi khách → cửa sổ Lịch sử thay đổi (mục 2.5)',
           '- Cột khóa trong Tùy chỉnh cột']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- Trong bảng: “Không có dữ liệu phù hợp.”', '- Dưới bảng: “Không có khách hàng nào.”', '- Chỉ hiện khi N = 0']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự KHÁCH đầu – cuối của trang', '- N: tổng số khách hàng khớp bộ lọc (không đếm dòng công ty)']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5, 10, 20, 50, 100', '10',
        ['- Mặc định: 10 (khách)', '- Lựa chọn: 5 / 10 / 20 / 50 / 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
        ['- Nút « ‹ số trang › »', '- Ở trang đầu « ‹ mờ; ở trang cuối › » mờ']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Lỗi khi tải dữ liệu” khi máy chủ lỗi.'),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Không kiểm quyền xem (màn không chặn quyền).\n– Xác định Q1 / Q2 và công ty người đăng nhập để tính phạm vi dòng.\n'
        'During:\n– Lấy khách hàng theo bộ lọc còn nhớ (≤ 10 phút), khách mới nhất trước; dựng dòng theo BR-02.\n'
        '– Nạp danh sách Cách tính lãi, cấu hình cột.\n– Máy chủ lỗi → hiển thị “Lỗi khi tải dữ liệu”.\n'
        'After:\n– Hiển thị trang 1, 10 khách, dòng “Hiển thị a–b / N”; dòng công ty mình hiện ô nhập nếu có Q2.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ Mã khách hàng, Tên khách hàng hỗ trợ sắp xếp.\n'
        'During:\n– Bỏ mọi giá trị đang sửa dở (không hỏi).\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc; cùng giá trị thì khách mới hơn ở trên.'),
       ('Bấm số trang hoặc nút « ‹ › »', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nDuring:\n– Bỏ mọi giá trị đang sửa dở (không hỏi, giữ như hệ thống cũ).\n'
        'After:\n– Nạp khách của trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1 và nạp lại theo số khách mới; bỏ phần đang sửa dở.'),
       ('Rời màn khi còn khách đang sửa dở', 'System',
        'Before:\n– Có ít nhất 1 khách có giá trị nhập khác giá trị đã lưu.\n'
        'After:\n– Hiện hộp “Thông tin chưa lưu” (mục 2.4); tải lại / đóng tab → trình duyệt hỏi xác nhận rời trang.'),
       ('Rời màn rồi quay lại / tải lại trang', 'System',
        'Before:\n– Bộ lọc được ghi nhớ trên trình duyệt 10 phút; sang màn khác thì xoá.\n'
        'After:\n– Tải lại trang (F5) trong 10 phút: giữ bộ lọc, sắp xếp; sang màn khác rồi quay lại: bộ lọc về mặc định. Cấu hình cột '
        'luôn giữ (lưu theo người dùng).'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc khách hàng',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách khách hàng',
       mota='Thu hẹp danh sách theo số điện thoại / mã số thuế / CMND của khách (ô tìm nhanh) và theo một khách cụ thể (ô Khách hàng). '
            'Hai ô nằm thẳng trên hàng tìm nhanh (bộ lọc gọn, không có Tìm kiếm nâng cao / Cài đặt bộ lọc). Lọc chỉ thu hẹp tập '
            'KHÁCH, không lọc dòng công ty.',
       tacnhan=TN_XEM, dieukien=DK,
       chinh='1. Người dùng nhập số điện thoại, mã số thuế hoặc CMND vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc người dùng gõ ít nhất 2 ký tự vào ô Khách hàng và chọn một khách trong gợi ý.\n'
             '3. Hệ thống lọc ngay khi ô Khách hàng đổi giá trị; ô tìm nhanh chỉ áp khi bấm Tìm kiếm / Enter; luôn về trang 1.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang, ghi nhớ bộ lọc 10 phút.',
       phu='• Bấm Làm mới → xóa ô tìm nhanh, ô Khách hàng và sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Gõ dưới 2 ký tự ở ô Khách hàng → chưa có gợi ý.\n'
           '• Bấm × trong ô tìm nhanh → xóa chữ (danh sách đổi khi bấm Tìm kiếm); bấm × trong ô Khách hàng → bỏ lọc khách, nạp lại ngay.\n'
           '• Đang có khách sửa dở mà lọc → phần sửa dở bị bỏ, không hỏi.',
       dacbiet='Ô tìm nhanh khớp MỘT PHẦN số điện thoại, mã số thuế hoặc CMND (không tìm theo mã / tên — đã có ô Khách hàng, Redmine '
               '#11717); bỏ khoảng trắng đầu / cuối; không giới hạn số ký tự; ký tự % và _ được tìm đúng nghĩa đen. Ô Khách hàng gợi ý '
               'tối đa 20 khách theo mã / tên (gõ số điện thoại từ 8 chữ số thì tìm theo số điện thoại), xếp theo tên. Hai điều kiện kết '
               'hợp kiểu VÀ.'),
   layout=dict(menu=MENU + ' => Tìm kiếm', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách — ô Khách hàng đang gợi ý'),
   extra=[(shot('02b_filtered'), 'Danh sách sau khi lọc một khách hàng')],
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo SĐT hoặc MST/CMND khách hàng”', '- Khớp một phần SĐT / MST / CMND', '- Áp khi bấm Tìm kiếm / nhấn Enter',
         '- Có nút × khi đã nhập']),
       ('Ô Khách hàng', 'Dropdown', 'Enable', 'Danh sách khách hàng', 'Không', 'Trống',
        ['- Mặc định: trống (gợi ý “Gõ để tìm khách hàng...”, nhãn nổi “Khách hàng”)', '- Gõ ≥ 2 ký tự → gợi ý dạng “Mã - Tên”',
         '- Chọn → lọc ngay; nút × bỏ chọn']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Bấm → xóa ô tìm nhanh, ô Khách hàng', '- Bỏ sắp xếp, xoá bộ lọc đã nhớ, nạp lại từ trang 1']),
       ('Kết quả lọc', 'Table/Grid', 'Read-only', '–', '–', 'Theo kết quả',
        ['- Bảng + dòng “Hiển thị a–b / N” cập nhật theo tiêu chí', '- Rỗng: “Không có dữ liệu phù hợp.” / “Không có khách hàng nào.”']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Lỗi khi tải dữ liệu” khi máy chủ lỗi.'),
   ],
   ev=[
       ('Chọn / bỏ chọn ô Khách hàng', 'Change',
        'Before:\n– Gõ ≥ 2 ký tự để có gợi ý.\n'
        'During:\n– Bỏ phần đang sửa dở.\n'
        'After:\n– Về trang 1, nạp lại danh sách theo khách đã chọn (một lần); ghi nhớ bộ lọc.'),
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, bỏ khoảng trắng đầu / cuối.\n'
        'During:\n– Tìm khách có SĐT, MST hoặc CMND chứa chuỗi nhập.\n'
        'After:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số khách.'),
       ('Gõ vào ô tìm nhanh (chưa bấm Tìm kiếm)', 'Change',
        'Before:\n– Chỉ đổi chữ trong ô.\nAfter:\n– Danh sách chưa đổi cho tới khi bấm Tìm kiếm / Enter.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\nAfter:\n– Xóa mọi tiêu chí, bỏ sắp xếp, xoá bộ lọc đã nhớ, nạp lại từ trang 1.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 9 cột của bảng. Ba cột STT, Mã khách hàng, Hành động bị khóa; cấu hình lưu '
            'riêng theo người dùng trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, bộ lọc hay tổng số.',
       tacnhan=TN_XEM, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 9 cột theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng ba gạch để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ 9 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ nguyên sau khi tải lại trang, đăng nhập lại, '
               'đổi trình duyệt. Cột đang hiện quyết định trường tích sẵn ở cửa sổ Xuất Excel.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn cột cần hiển thị, kéo ☰ để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 9 cột', '–', 'Theo cấu hình đã lưu',
        ['- STT, Mã khách hàng, Tên khách hàng, MST/CMND, Khai báo theo công ty',
         '- Cách tính lãi, Hạn mức công nợ tính lãi, Hạn mức công nợ xuất hàng, Hành động']),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → cột ẩn khỏi bảng.'),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Mã khách hàng (biểu tượng ổ khóa), Hành động', '- Không ẩn được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/9 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '- n = số cột đang tích.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Không cần quyền.\nAfter:\n– Mở cửa sổ, nạp cấu hình cột đang lưu của người dùng (chưa lưu lần nào → đủ 9 cột).'),
       ('Kéo biểu tượng kéo thả', 'Drag',
        'Before:\n– Kéo bằng biểu tượng ba gạch.\nAfter:\n– Đổi thứ tự cột trong danh sách; chưa áp lên bảng.'),
       ('Tích / bỏ tích một cột', 'Change', 'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/9 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách cột đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng; dữ liệu, bộ lọc, tổng số giữ nguyên.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ đúng cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.4 Khai báo / sửa
fr(4, 'Khai báo / chỉnh sửa hạn mức (Lưu từng khách)', usecase=('FR-04', 'Khai báo / chỉnh sửa hạn mức', 'crud', A_ND),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Khai báo / chỉnh sửa hạn mức công nợ của một khách tại công ty mình',
       mota='Người có quyền Quản lý sửa thẳng trên bảng 3 ô của dòng công ty mình (Cách tính lãi, Hạn mức công nợ tính lãi, Hạn mức công '
            'nợ xuất hàng) rồi bấm Lưu ở khách đó. Khai báo lần đầu (khách chưa có hạn mức) và sửa hạn mức đã có cùng một thao tác. '
            'Lưu theo cách của hệ thống cũ: xoá hết dòng hạn mức của khách rồi ghi lại các dòng đang hiện (BR-04).',
       tacnhan=TN_SUA,
       dieukien=DK + '\n4. Người dùng có quyền “%s”.\n5. Khách có dòng của công ty người đăng nhập đang hiện trên bảng.' % Q_MAN,
       chinh='1. Người dùng tìm khách (mục 2.2).\n'
             '2. Ở dòng công ty mình, người dùng chọn Cách tính lãi, nhập Hạn mức công nợ tính lãi, Hạn mức công nợ xuất hàng.\n'
             '3. Người dùng bấm Lưu (đĩa mềm) ở cột Hành động của khách.\n'
             '4. Hệ thống kiểm trên màn: hạn mức ≤ 999,999,999,999,999; có Hạn mức công nợ tính lãi thì phải có Cách tính lãi.\n'
             '5. Hệ thống kiểm lại ở máy chủ: quyền Quản lý, khách còn tồn tại, khách có dòng công ty mình, dữ liệu hợp lệ.\n'
             '6. Hệ thống dựng lại các dòng đang hiện với người lưu từ dữ liệu đã lưu, thay dòng công ty mình bằng giá trị vừa nhập.\n'
             '7. Có thay đổi → xoá hết dòng hạn mức của khách, ghi lại các dòng đó (người tạo / người cập nhật = người lưu).\n'
             '8. Hệ thống ghi một dòng lịch sử “Thay đổi thông tin” của khách, chỉ gồm công ty có giá trị đổi (cũ → mới).\n'
             '9. Hệ thống hiển thị ' + OK + ', thay dữ liệu khách trên bảng bằng dữ liệu vừa lưu; ô nhập về trạng thái đã lưu.',
       phu='• Lỗi kiểm trên màn → chữ đỏ dưới ô (viền đỏ), thông báo ' + CHECK + ', không gửi đi; lỗi “thiếu cách tính lãi” từ lần bấm Lưu '
           'đầu tiên trở đi cập nhật ngay khi gõ.\n'
           '• Máy chủ báo lỗi dữ liệu → chữ đỏ dưới đúng ô của khách + thông báo ' + CHECK + '.\n'
           '• Không đổi gì mà bấm Lưu → vẫn báo ' + OK + ', không ghi dữ liệu, không ghi lịch sử.\n'
           '• Không còn quyền Quản lý → ' + NOPERM + '; khách không có dòng công ty mình → ' + NOPERM_ROW + '\n'
           '• Khách vừa bị xóa khỏi danh mục → ' + CONFLICT + ', danh sách nạp lại.\n'
           '• Lỗi máy chủ → ' + SYS + '\n'
           '• Rời màn khi còn khách sửa dở → hộp “Thông tin chưa lưu”: Thoát (bỏ thay đổi, rời màn) / Ở lại / (x).\n'
           '• Đổi trang / lọc / sắp xếp / số dòng khi đang sửa dở → bỏ thay đổi, không hỏi (giữ như hệ thống cũ).',
       dacbiet='Không có nút Thêm mới / Lưu và tiếp tục / Xóa: khai lần đầu = nhập vào dòng trống; xoá hạn mức = xoá trắng ô rồi Lưu (dòng '
               'vẫn còn, giá trị trống). Mỗi khách lưu riêng; nút Lưu khóa trong lúc đang lưu (chú thích “Đang lưu...”) để tránh bấm '
               'liên tục. Không có trường duy nhất (mỗi khách × công ty tối đa 1 dòng do hệ thống tự quản).'),
   layout=dict(menu=MENU + ' => Lưu', shot=shot('10_edit'),
               shot_caption='Dòng công ty mình có ô nhập; nút Lưu và Lịch sử ở cột Hành động',
               note='Các ô nhập nằm ngay trên bảng danh sách theo đường dẫn ở trên (không có popup).'),
   extra=[(shot('10b_validate'), 'Lỗi dưới ô khi thiếu Cách tính lãi và hạn mức vượt trần'),
          (shot('10d_unsaved'), 'Hộp “Thông tin chưa lưu” khi rời màn lúc còn khách sửa dở')],
   ui=[
       ('Ô Cách tính lãi (dòng công ty mình)', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Có khi nhập Hạn mức công nợ tính lãi',
        'Theo dữ liệu',
        ['- Mặc định: giá trị đã lưu; chưa khai: trống, gợi ý “Chọn cách tính lãi”', '- Lựa chọn: Theo vượt hạn mức công nợ',
         '- Lựa chọn: Theo thời gian thanh toán', '- Nút × bỏ chọn', '- Thiếu khi có hạn mức tính lãi: ' + TYPE_REQ]),
       ('Ô Hạn mức công nợ tính lãi', 'Textbox', 'Enable', '0 – 999,999,999,999,999', 'Không', 'Theo dữ liệu',
        ['- Chỉ nhận chữ số, số nguyên; tự thêm dấu phẩy ngăn nghìn', '- Gợi ý “Nhập hạn mức công nợ tính lãi”',
         '- Vượt trần: ' + MAXE + ' (báo ngay khi gõ, không tự kéo về trần)', '- Để trống = chưa khai']),
       ('Ô Hạn mức công nợ xuất hàng', 'Textbox', 'Enable', '0 – 999,999,999,999,999', 'Không', 'Theo dữ liệu',
        ['- Như ô Hạn mức công nợ tính lãi, gợi ý “Nhập hạn mức công nợ xuất hàng”',
         '- Không bắt buộc kèm Cách tính lãi']),
       ('Dòng công ty khác', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '- Hiện chữ, không sửa được.'),
       ('Nút Lưu (đĩa mềm)', 'Icon Button', 'Enable / Disable', '–', '–', 'Ẩn khi thiếu quyền',
        ['- Chỉ ở khách có dòng công ty mình sửa được', '- Chú thích “Lưu”; khi đang lưu: “Đang lưu...”, khóa',
         '- Bấm → kiểm, lưu riêng khách đó']),
       ('Thông báo lỗi dưới ô', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Chữ đỏ có biểu tượng cảnh báo, viền ô đỏ', '- Lỗi hạn mức mất ngay khi sửa đúng', '- Lỗi Cách tính lãi mất khi chọn giá trị']),
       ('Thông báo kiểm tra', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + CHECK + ' khi có lỗi dữ liệu.'),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + OK),
       ('Thông báo từ chối / lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- ' + NOPERM, '- ' + NOPERM_ROW, '- ' + CONFLICT, '- ' + SYS]),
       ('Hộp Thông tin chưa lưu', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Tiêu đề “Thông tin chưa lưu”', '- Nội dung “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”',
         '- Nút Thoát (đỏ): rời màn, bỏ thay đổi', '- Nút Ở lại / (x): ở lại màn, giữ giá trị đang nhập']),
   ],
   ev=[
       ('Chọn Cách tính lãi', 'Change',
        'Before:\n– Dòng công ty mình, có quyền Quản lý.\nAfter:\n– Ghi nhận giá trị trên màn; xoá lỗi dưới ô Cách tính lãi; khách thành '
        '“đang sửa dở” nếu khác giá trị đã lưu.'),
       ('Nhập hạn mức', 'Change',
        'Before:\n– Ô chỉ nhận chữ số.\nDuring:\n– Vượt 999,999,999,999,999 → ' + MAXE + ' ngay dưới ô.\n'
        '– Đã bấm Lưu ít nhất 1 lần: có hạn mức tính lãi mà thiếu Cách tính lãi → ' + TYPE_REQ + '.\n'
        'After:\n– Khách thành “đang sửa dở” nếu khác giá trị đã lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Kiểm quyền “' + Q_MAN + '”; không có → ' + NOPERM + ' và dừng xử lý.\n'
        '– Kiểm trên màn: hạn mức vượt trần → ' + MAXE + '; có hạn mức tính lãi, thiếu Cách tính lãi → ' + TYPE_REQ + '; có lỗi → ' +
        CHECK + ', dừng.\n'
        'During:\n– Khách không còn trong danh mục → ' + CONFLICT + ', nạp lại danh sách.\n'
        '– Khách không có dòng công ty mình trong tập dòng đang hiện → ' + NOPERM_ROW + '\n'
        '– Máy chủ kiểm lại: Cách tính lãi chỉ 2 giá trị (“Cách tính lãi không hợp lệ.”), hạn mức số nguyên (“Phải là số nguyên.”), '
        '≥ 0 (“Không được nhỏ hơn 0.”), ≤ trần (“Không được lớn hơn 999,999,999,999,999.”), thiếu cách tính lãi (“Vui lòng chọn cách '
        'tính lãi.”).\n' + ERR + '\n'
        'After:\n– Khoá các dòng của khách, dựng lại dòng đang hiện, thay dòng công ty mình; không đổi gì → không ghi.\n'
        '– Có đổi: xoá hết dòng của khách, ghi lại các dòng đó; ghi một dòng lịch sử “Thay đổi thông tin” chỉ với công ty có giá trị '
        'đổi (cũ → mới).\n– Hiển thị ' + OK + ', thay dữ liệu khách trên bảng, ô nhập về trạng thái đã lưu.'),
       ('Rời màn khi còn khách sửa dở', 'System',
        'Before:\n– So giá trị nhập với giá trị đã lưu của từng khách.\n'
        'During:\n– Chuyển sang màn khác → hộp “Thông tin chưa lưu”; tải lại / đóng tab → trình duyệt hỏi xác nhận.\n'
        'After:\n– Thoát → rời màn, không lưu. Ở lại / (x) → ở lại, giữ nguyên giá trị đang nhập.'),
       ('Đổi trang / lọc / sắp xếp khi đang sửa dở', 'System',
        'Before:\n– Có khách đang sửa dở.\nAfter:\n– Nạp lại danh sách, bỏ toàn bộ phần sửa dở và lỗi, không hỏi (giữ như hệ thống cũ).'),
   ])

# ------------------------------------------------------------ 2.5 Lịch sử
fr(5, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi hạn mức của một khách hàng',
       mota='Hiển thị các lần lưu có thay đổi hạn mức của một khách: thời điểm, người thực hiện, phòng ban và với từng công ty có giá trị '
            'đổi thì Cách tính lãi, Hạn mức công nợ tính lãi, Hạn mức công nợ xuất hàng trước → sau; lọc được theo loại hành động, '
            'người thực hiện, khoảng ngày.',
       tacnhan=TN_XEM, dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách, khách hiện trên bảng.',
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động của khách.\n'
             '2. Hệ thống nạp các mốc lịch sử của khách.\n'
             '3. Hệ thống hiển thị cửa sổ “Lịch sử thay đổi: <Mã khách hàng> - <Tên khách hàng>”, mốc mới nhất ở trên.\n'
             '4. Người dùng bấm Bộ lọc để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.\n'
             '5. Người dùng bấm Đóng để về danh sách.',
       phu='• Khách chưa lưu hạn mức lần nào (hoặc chỉ lưu trước khi có ghi lịch sử) → “Chưa có lịch sử thao tác nào.”.\n'
           '• Lọc không ra mốc → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Lỗi nạp → dòng lỗi đỏ + nút Thử lại.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài → đóng; danh sách giữ nguyên trang, bộ lọc và giá trị đang sửa dở.',
       dacbiet='Chỉ có mốc “Thay đổi thông tin” (kể cả lần khai đầu: trống → giá trị); không có mốc Tạo mới / Xóa. Lưu không đổi gì không '
               'ghi. Dòng công ty khác bị mất do cách lưu ở BR-04 hiện là sửa từ giá trị cũ → (trống).'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('16b_history_filter'), 'Cửa sổ Lịch sử thay đổi đang mở Bộ lọc')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Lịch sử thay đổi: <Mã khách hàng> - <Tên khách hàng>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, hành động “Thay đổi thông tin” (xanh dương)',
           '- “Người thực hiện: <tên> — <phòng ban>”',
           '- Khối “Hạn mức theo công ty sửa thông tin”: mỗi công ty đổi một mục “- <Tên công ty>:”',
           '- Từng trường Cách tính lãi / Hạn mức công nợ tính lãi / Hạn mức công nợ xuất hàng: cũ (đỏ) → mới (xanh), trống ghi “(trống)”',
           '- Mới nhất ở trên']),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', '- Mở / thu gọn khối ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Trống',
        ['- Mặc định: trống', '- Lựa chọn: Tạo mới / Thay đổi thông tin / Thay đổi trạng thái', '- Chọn là lọc ngay']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống',
        ['- Dạng “Tên - Mã phòng - Mã NV”', '- Chọn là lọc ngay']),
       ('Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc từ ngày này.'),
       ('Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc đến hết ngày này.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', '- Xóa điều kiện lọc lịch sử.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- “Chưa có lịch sử thao tác nào.”', '- “Không có lịch sử phù hợp bộ lọc.”']),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Giống nút Đóng.'),
   ],
   ev=[
       ('Bấm Lịch sử', 'Click',
        'Before:\n– Không cần quyền.\n'
        'During:\n– Nạp các mốc + danh mục ô lọc; chưa có → “Chưa có lịch sử thao tác nào.”.\nAfter:\n– Hiển thị, mới nhất trên.'),
       ('Đổi điều kiện Bộ lọc', 'Change',
        'Before:\n– Không có nút Tìm kiếm.\nAfter:\n– Lọc lại danh sách mốc; không khớp → “Không có lịch sử phù hợp bộ lọc.”.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Có điều kiện lọc.\nAfter:\n– Xóa điều kiện, hiện lại đủ mốc.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng; danh sách giữ nguyên trang, bộ lọc, giá trị đang sửa dở.'),
   ])

# ------------------------------------------------------------ 2.6 Xuất Excel
fr(6, 'Xuất Excel danh sách', usecase=('FR-06', 'Xuất Excel', 'io', A_ND),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất Excel danh sách hạn mức công nợ khách hàng',
       mota='Xuất mọi khách khớp bộ lọc đang áp (không theo trang đang xem) ra file Excel, mỗi dòng công ty một dòng file, ô STT / Mã / '
            'Tên / MST gộp theo khách như trên màn; người dùng chọn trường và thứ tự cột. File dựng theo khuôn chung các màn danh '
            'sách: letterhead công ty, tiêu đề, bảng, khối ký.',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn danh sách.',
       chinh='1. Người dùng lọc danh sách theo nhu cầu rồi bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất file” liệt kê 7 trường, tích sẵn các trường đang hiện trên bảng (mặc định đủ 7).\n'
             '3. Người dùng tích / bỏ tích, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống tải lần lượt mọi khách khớp bộ lọc, hiện tiến độ cạnh nút “Đang chuẩn bị dữ liệu…”, “Đã tải x/y dòng…”, '
             '“Đang dựng file x/y dòng…”.\n'
             '5. Hệ thống tạo file khai-bao-han-muc-cong-no-khach-hang.xlsx (trang “Han muc cong no KH”): letterhead công ty người '
             'xuất, tiêu đề “KHAI BÁO HẠN MỨC CÔNG NỢ KHÁCH HÀNG”, cột STT + các trường đã chọn, khối ký “Ngày ..., tháng ..., năm ...” '
             '/ “Người lập” / “(Ký, họ tên)”.\n'
             '6. Hệ thống tải file về và hiển thị “Xuất Excel thành công.”.',
       phu='• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Danh sách theo bộ lọc rỗng → thông báo “Không có dữ liệu để xuất”, KHÔNG tạo file.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài cửa sổ chọn trường → không xuất.\n'
           '• Lỗi khi xuất → “Lỗi khi xuất Excel”.',
       dacbiet='Phạm vi dòng giống màn (BR-01, BR-02). STT đánh theo khách; 2 hạn mức là ô SỐ định dạng #,##0, chưa khai thì trống. '
               'Xuất không giới hạn số dòng, không ghi lịch sử. Không lọc thì file rất lớn (mỗi khách nhiều dòng công ty — hơn 13 nghìn '
               'khách trên dữ liệu thử) nên nên lọc trước khi xuất.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất file”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 7 trường', '–', 'Theo cột đang hiện',
        ['- Mã khách hàng, Tên khách hàng, MST/CMND, Khai báo theo công ty',
         '- Cách tính lãi, Hạn mức công nợ tính lãi, Hạn mức công nợ xuất hàng', '- Cột STT luôn có trong file (không nằm trong danh sách)']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích',
        ['- Mặc định tích các trường đang hiện trên bảng (cấu hình mặc định: cả 7)', '- Bỏ tích → trường không có trong file']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích cả 7 trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/7 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Khóa khi chưa tích trường nào hoặc đang xuất', '- Bấm → tải file']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng cửa sổ, không xuất.'),
       ('Dòng tiến độ', 'Label', 'Read-only', '–', '–', 'Ẩn',
        ['- Cạnh nút Xuất Excel: “Đang chuẩn bị dữ liệu…”, “Đã tải x/y dòng…”, “Đang dựng file x/y dòng…”']),
       ('File Excel', 'Table/Grid', 'Read-only', '.xlsx', '–', '–',
        ['- Tên khai-bao-han-muc-cong-no-khach-hang.xlsx', '- Mỗi dòng công ty 1 dòng; STT, Mã, Tên, MST/CMND gộp ô theo khách',
         '- Letterhead công ty người xuất, tiêu đề, khối ký']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Xuất Excel thành công.”', '- “Không có dữ liệu để xuất”', '- “Lỗi khi xuất Excel”']),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Không cần quyền; lấy bộ lọc đang áp.\nAfter:\n– Mở cửa sổ chọn trường, tích sẵn các cột đang hiện.'),
       ('Tích / bỏ tích, kéo thả trường', 'Change',
        'Before:\n– Trong cửa sổ chọn trường.\nAfter:\n– Cập nhật “Đang chọn n/7 trường”; 0 trường → khóa Xuất file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Ít nhất 1 trường được tích; khóa nút Xuất Excel trong lúc xuất.\n'
        'During:\n– Tải tuần tự mọi khách khớp bộ lọc theo phạm vi dòng của người xuất; 0 dòng → “Không có dữ liệu để xuất”, dừng.\n'
        '– Lỗi → “Lỗi khi xuất Excel”.\n'
        'After:\n– Dựng file, gộp ô theo khách, tải về, hiển thị “Xuất Excel thành công.”; không ghi lịch sử.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Khai báo hạn mức công nợ KH; không lặp lại các quy tắc đã có trong '
           'SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi xem theo quyền', [
        '– Không chặn quyền xem: ai đăng nhập cũng vào màn, thấy mọi khách hàng (giữ như hệ thống cũ).',
        '– Có “' + Q_MAN + '” mà không có “' + Q_VIEW + '” → chỉ thấy dòng công ty mình; các trường hợp khác thấy dòng mọi công ty.',
        '– Super admin không được đặc cách.'],
     ['Xem danh sách', 'Tìm kiếm và lọc', 'Xuất Excel']),
    ('BR-02', 'Dòng hiện của một khách (giữ như hệ thống cũ)', [
        '– Khách đã có dòng hạn mức (trong phạm vi được thấy) → CHỈ hiện các dòng đó; không tự thêm dòng cho công ty khác.',
        '– Khách chưa có dòng nào → mỗi công ty trong hệ thống 1 dòng trống (chỉ có Quản lý, không có Xem: chỉ công ty mình).',
        '– Hệ quả: khách đã khai ở công ty A thì công ty B không có dòng để khai thêm (user chốt 14/10/2026 giữ như hệ thống cũ).'],
     ['Xem danh sách', 'Khai báo / chỉnh sửa', 'Xuất Excel']),
    ('BR-03', 'Ai sửa được dòng nào', [
        '– Có “' + Q_MAN + '” VÀ dòng là công ty người đăng nhập → ô nhập + nút Lưu; còn lại chỉ đọc.',
        '– Máy chủ chỉ nhận giá trị gửi lên cho dòng công ty mình; giá trị gửi cho công ty khác bị bỏ qua.'],
     ['Khai báo / chỉnh sửa']),
    ('BR-04', 'Cách lưu (giữ như hệ thống cũ)', [
        '– Lưu = xoá MỌI dòng hạn mức của khách rồi ghi lại các dòng đang hiện với người lưu (dòng công ty mình lấy giá trị mới, dòng '
        'khác lấy giá trị đã lưu).',
        '– Người chỉ có Quản lý (không có Xem) bấm Lưu → dòng hạn mức của công ty khác bị XOÁ (user chốt 14/10/2026 giữ như hệ thống cũ).',
        '– Khai lần đầu: mọi dòng trống đang hiện cũng được ghi thành dòng (giá trị trống). Không có gì thay đổi → không ghi.'],
     ['Khai báo / chỉnh sửa']),
    ('BR-05', 'Dữ liệu hợp lệ và chuẩn hóa', [
        '– Cách tính lãi: Theo vượt hạn mức công nợ / Theo thời gian thanh toán, để trống được.',
        '– 2 hạn mức: số nguyên 0 – 999,999,999,999,999, để trống được; dấu phẩy ngăn nghìn chỉ để hiển thị.',
        '– Có Hạn mức công nợ tính lãi thì bắt buộc Cách tính lãi (lệch hệ thống cũ — Redmine #11900); Hạn mức xuất hàng không bắt '
        'buộc kèm.', '– Người tạo / người cập nhật của dòng = người bấm Lưu.'], ['Khai báo / chỉnh sửa']),
    ('BR-06', 'Lưu đồng thời', [
        '– Khi lưu, hệ thống khoá các dòng của khách: hai người cùng lưu thì người sau dựng lại dòng từ dữ liệu người trước vừa ghi.',
        '– Giá trị công ty mình của người sau ghi đè; mỗi lần có đổi đều ghi lịch sử.'], ['Khai báo / chỉnh sửa']),
    ('BR-07', 'Quy tắc ghi lịch sử', [
        '– Mỗi lần Lưu có đổi ghi 1 mốc “Thay đổi thông tin” của khách, chỉ gồm công ty có giá trị đổi; dòng không tồn tại coi như trống.',
        '– Không có mốc Tạo mới / Xóa; lưu không đổi, xem, xuất không ghi. Hiển thị mới nhất ở trên.'],
     ['Khai báo / chỉnh sửa', 'Lịch sử']),
    ('BR-08', 'Sử dụng ở màn khác', [
        '– Báo cáo hạn mức công nợ khách hàng: đọc 2 hạn mức của công ty người xem, chỉ dòng có ít nhất 1 hạn mức > 0.',
        '– Yêu cầu xuất hàng (Xuất bán hàng, Xuất bán SC - BD): gửi duyệt mà công nợ của khách trên hợp đồng do người lập tạo + giá trị '
        'phiếu > Hạn mức công nợ xuất hàng của công ty người lập → hỏi xác nhận, phiếu sang “Đợi TP duyệt”.',
        '– Yêu cầu xuất bán hàng mượn: vượt Hạn mức công nợ xuất hàng → phiếu chờ Trưởng phòng duyệt.',
        '– Hạn mức xuất hàng trống / 0 → không kiểm vượt. Sửa hạn mức chỉ ảnh hưởng lần gửi duyệt sau.'],
     ['Khai báo / chỉnh sửa']),
    ('BR-09', 'Không có Thêm / Xóa / Khóa / Import / Chi tiết', [
        '– Danh sách khách lấy từ danh mục Khách hàng (chỉ khách hàng, không gồm nhà cung cấp); khách mới tạo hiện ngay, khách bị xóa '
        'biến mất.', '– Xoá hạn mức = xoá trắng ô rồi Lưu; màn không có trạng thái nên không có Khóa / Mở khóa.'],
     ['Xem danh sách', 'Khai báo / chỉnh sửa']),
    ('BR-10', 'Xuất Excel', [
        '– Xuất mọi khách khớp bộ lọc theo phạm vi BR-01 / BR-02, không giới hạn; rỗng → không tạo file.',
        '– Mỗi dòng công ty 1 dòng file, gộp ô thông tin khách; letterhead theo công ty người xuất.'], ['Xuất Excel']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc cung cấp dữ liệu cho Khai báo hạn mức công nợ KH (Cách tính lãi, Hạn mức công nợ tính lãi, Hạn mức '
    'công nợ xuất hàng theo khách × công ty).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Tài chính', 'Báo cáo hạn mức công nợ khách hàng (đọc Hạn mức tính lãi / Hạn mức xuất hàng của công ty người xem, chỉ dòng có '
                       'hạn mức > 0; sửa ở màn này thì báo cáo đổi ngay)', 'Tài chính -> Kế toán công nợ -> Khách hàng'),
    ('2', 'Tài chính', 'Yêu cầu xuất hàng (gửi duyệt phiếu Xuất bán hàng / Xuất bán SC - BD: công nợ + giá trị phiếu vượt Hạn mức công nợ '
                       'xuất hàng → hỏi xác nhận, phiếu sang Đợi TP duyệt)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('3', 'Tài chính', 'Yêu cầu xuất bán hàng mượn (vượt Hạn mức công nợ xuất hàng → phiếu chờ Trưởng phòng duyệt)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Mượn hàng'),
    ('4', 'Bán hàng', 'YC xuất hàng, YC xuất bán hàng mượn (cùng màn ở dòng 2, 3, lối vào từ phân hệ Bán hàng)',
     'Bán hàng -> Yêu cầu -> Hàng hóa'),
    ('5', 'Danh mục dùng chung', 'Khách hàng (nguồn danh sách khách của màn: mã, tên, mã số thuế, CMND, số điện thoại; khách mới hiện '
                                 'ngay, khách bị xóa biến mất cùng hạn mức không còn hiện)', 'Danh mục dùng chung -> Đối tác'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)

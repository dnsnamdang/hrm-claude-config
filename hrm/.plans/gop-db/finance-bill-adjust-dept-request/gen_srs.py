# -*- coding: utf-8 -*-
"""SRS màn "Phiếu yêu cầu điều chỉnh công nợ" (mã {cty}.DNDCCN{mmyy}.NNNNN) — form chuẩn Danh mục quốc gia.

Chạy: python gen_srs.py  → SRS - Phiếu yêu cầu điều chỉnh công nợ.docx
Khung: srs-documenter (SrsDoc) + checklist ../phieu-theo-form-quoc-gia/CHECKLIST.md. Khuôn thư mục: bank-account-catalog.
Độ chi tiết bám SRS_MAU (../finance-bill-income-request/gen_srs.py) — nâng 31/10/2026.
Nguồn đọc 30–31/10/2026 (nhánh develop, cả 2 repo):
  BE  Modules/Finance/{Entities/BillAdjustDeptRequest/*, Services/BillAdjustDeptRequest*Service.php,
      Services/BillAdjustDeptFastPickService.php, Http/Controllers/V1/BillAdjustDeptRequestController.php,
      Http/Requests/BillAdjustDeptRequest/*, Exports/BillAdjustDeptRequestListExport.php,
      Resources/views/prints/bill-adjust-dept-request.blade.php}
  FE  pages/finance/bill-adjust-dept-requests/** (index, _id/index, create, _id/edit, components/*),
      components/{V2BaseDataTable, V2BaseSmartFilterPanel, modal/*, modals/ChooseErpCustomerModal, print/*},
      pages/finance/bill-income-requests/components/{SupplierSearchModal, ContractSearchModal}, plugins/axios.js,
      utils/mixins/{unsavedChangesMixin, saveAndContinueMixin, reportPrintPreviewMixin}
  Spec docs/superpowers/specs/gop-db/2026-08-17-finance-bill-adjust-dept-request-design.md (một phần đã cũ — ưu tiên code)
Ảnh: ./dcbn_shots (dev-hrm 30/10/2026, tài khoản DNS Admin, script dcbn_shots/_capture/capture.js).
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
from srs_split_rows import split_ui_rows  # noqa: E402  (tách dòng gộp: mỗi đối tượng 1 hàng)

TEN = 'Phiếu yêu cầu điều chỉnh công nợ'
SHOTS = os.path.join(HERE, 'dcbn_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # sơ đồ Use Case; HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = ('Phân hệ Tài chính => Khởi tạo => Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi => '
        'Phiếu yêu cầu điều chỉnh công nợ')
MENU_CD = ('Phân hệ Tài chính => Chờ duyệt => Phê duyệt - Công nợ - Thu - Chi => '
           'Phiếu yêu cầu điều chỉnh công nợ chờ duyệt')
MENU_SALE = 'Phân hệ Bán hàng => Yêu cầu => Công nợ - Thu - Chi => YC điều chỉnh công nợ'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Phiếu yêu cầu điều chỉnh công nợ.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')

A_LAP = 'Người lập phiếu'
A_KT = 'Kế toán thanh toán'
TN_MOI = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn danh sách (lập phiếu không gắn quyền '
          'riêng); người lập là người đang đăng nhập.')
TN_XEM = ('Người dùng có quyền thực hiện chức năng: người lập phiếu; người đã xử lý phiếu; Kế toán thanh toán cùng '
          'công ty (phiếu Chờ tạo phiếu kế toán); người có một trong các quyền Xem tất cả phiếu yêu cầu điều chỉnh của '
          'tổng công ty / của công ty / của phòng ban / của bộ phận (V1–V4).')
TN_SUA = 'Người dùng có quyền thực hiện chức năng: người lập phiếu (không cần quyền riêng).'
TN_KT = 'Người dùng có quyền thực hiện chức năng: Kế toán thanh toán (Q1), cùng công ty ghi trên phiếu.'
DK_XEM = ('1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Phiếu yêu cầu điều chỉnh công nợ '
          '(một trong 3 lối vào ở mục 2.1).\n3. Phiếu cần thao tác nằm trong phạm vi xem của người dùng (Phần 2).')
DK_SUA = ('1. Người dùng đăng nhập thành công.\n2. Người dùng là người lập phiếu.\n'
          '3. Phiếu đang ở trạng thái Đang tạo hoặc Từ chối.')
DK_KT = ('1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán thanh toán, cùng công ty ghi trên phiếu.\n'
         '3. Phiếu đang ở trạng thái Chờ tạo phiếu kế toán.')
# Thông báo khi gọi thao tác mà BE chặn quyền (HTTP 403 → hệ thống hiện nguyên văn câu BE trả).
NO_VIEW = '“Bạn không có quyền xem phiếu này”'
SESSION = ('• Phiên đăng nhập hết hạn → hiển thị “Phiên đăng nhập đã hết hạn” và chuyển về màn đăng nhập.')

d = SrsDoc(out=OUT, menu=MENU, route='/finance/bill-adjust-dept-requests', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Khởi tạo': 'menu_khoitao',
    'Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi': 'menu_nhom_khoitao', 'Phiếu yêu cầu điều chỉnh công nợ': 'menu_muc',
    'Chờ duyệt': 'menu_choduyet', 'Phê duyệt - Công nợ - Thu - Chi': 'menu_nhom_pheduyet',
    'Phiếu yêu cầu điều chỉnh công nợ chờ duyệt': 'menu_muc_choduyet',
    'Phân hệ Bán hàng': 'menu_phanhe_banhang', 'Yêu cầu': 'menu_yeucau', 'Công nợ - Thu - Chi': 'menu_congno',
    'YC điều chỉnh công nợ': 'menu_muc_sale',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Sửa': 'btn_sua_row', 'Xóa': 'btn_xoa_row', 'Gửi duyệt': 'btn_guiduyet_detail',
    'Từ chối': 'btn_tuchoi', 'Tạo phiếu kế toán': 'btn_taopktoan', 'In phiếu': 'btn_in', 'Xuất Excel': 'btn_xuatexcel',
    'Lịch sử': 'item_lichsu',
}.items()})


# Bảng giao diện viết sẵn mỗi đối tượng 1 hàng; split_ui_rows vẫn chạy để chặn dòng gộp lọt vào.
UI_OVER = {}
UI_EXPLICIT = {}
# Tên có sẵn dấu " / " nhưng là MỘT đối tượng (nhãn thật trên màn).
KEEP = {'Ô Khách hàng / Nhà cung cấp', 'Ô Khách hàng / Nhà cung cấp (bên “từ”)', 'Ô Khách hàng / Nhà cung cấp (bên “đến”)',
        'Ô Hợp đồng/Đơn hàng (bên “từ”)', 'Ô Hợp đồng/Đơn hàng (bên “đến”)', 'Cột Số dư cuối kỳ / Số dư (bên “từ”)',
        'Cột Số dư cuối kỳ / Số dư (bên “đến”)', 'Cột NVKD / Nhân viên (bên “từ”)', 'Cột NVKD / Nhân viên (bên “đến”)',
        'Ô Khách hàng / Nhà cung cấp (popup)', 'Cột Đơn hàng/ Hợp đồng'}


def uc(code, name, group, actor):
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None):
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
    if 'entries' in layout:     # màn nhiều lối vào: mỗi lối vào 1 dòng Menu + phạm vi hiển thị
        d.p('Đường dẫn màn hình:')
        for m, note in layout['entries']:
            d._menu_para(m)
            d.p(note)
        d.figure(layout['shot'], layout['shot_caption'], width_in=6.2)
    else:
        d.layout(**layout)
    k += 1
    assert ui and ev, 'Thiếu bảng giao diện / event ở 2.%d' % no
    d.p('2.%d.%d Mô tả chi tiết giao diện' % (no, k))
    d.ui_table(split_ui_rows(ui, UI_OVER, UI_EXPLICIT, keep=KEEP), **(ui_kw or {}))
    k += 1
    d.p('2.%d.%d Danh sách event và xử lý event' % (no, k))
    d.event_table(ev)


# ============================================================== TRANG ĐẦU
d.title_block(TEN)
d.h2('Mục lục')
d.toc()

# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu yêu cầu điều chỉnh công nợ (mã phiếu …DNDCCN…), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng duyệt của màn hình.',
    'Làm rõ cách đề nghị chuyển công nợ từ khách hàng / nhà cung cấp, hợp đồng này sang khách hàng / nhà cung cấp, '
    'hợp đồng khác (bảng chi tiết 2 cấp “Điều chỉnh từ” → “Điều chỉnh đến”).',
    'Làm rõ các điều kiện chặn khi gửi duyệt (khớp tổng tiền, không trùng hợp đồng, bắt buộc hợp đồng bên “đến”).',
    'Làm rõ vai trò Kế toán thanh toán: từ chối hoặc tạo phiếu kế toán điều chỉnh công nợ từ phiếu yêu cầu.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu yêu cầu điều chỉnh công nợ', 'Phiếu của màn này, mã dạng <mã công ty>.DNDCCN<tháng năm>.NNNNN.'),
    ('Loại phiếu', '“Điều chỉnh công nợ khách hàng” (mặc định) hoặc “Điều chỉnh công nợ nhà cung cấp”.'),
    ('Điều chỉnh từ', 'Dòng ghi khách hàng / nhà cung cấp, hợp đồng và số tiền công nợ bị chuyển đi.'),
    ('Điều chỉnh đến', 'Các dòng con của mỗi dòng “từ”: nơi nhận công nợ (khách hàng / NCC, hợp đồng, số tiền).'),
    ('Số dư cuối kỳ / Số dư', 'Công nợ còn lại của hợp đồng (khách hàng: phải thu; NCC: phải trả), hệ thống tự tính.'),
    ('Phiếu báo có', 'Phiếu ghi nhận tiền về ngân hàng; phiếu tạo từ phiếu báo có thì dòng “từ” bị khóa theo phiếu báo có.'),
    ('Phiếu kế toán', 'Phiếu kế toán điều chỉnh công nợ do Kế toán thanh toán lập từ phiếu yêu cầu để ghi sổ.'),
    ('Đang tạo / Chờ tạo phiếu kế toán / Đã tạo phiếu kế toán / Đã duyệt phiếu kế toán / Hủy / Từ chối',
     'Các trạng thái của phiếu.'),
], widths=[2.1, 3.9])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Lập phiếu không cần quyền riêng. Sửa / Xóa / Gửi duyệt: chỉ người lập, khi phiếu Đang tạo hoặc Từ chối.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Kế toán thanh toán',
     'Thấy mục menu “Phiếu yêu cầu điều chỉnh công nợ chờ duyệt”; với phiếu Chờ tạo phiếu kế toán của người lập cùng '
     'công ty: nút Tạo phiếu kế toán và Từ chối; nhận thông báo khi có phiếu gửi duyệt.'),
], widths=[0.8, 1.6, 3.6])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (xét từ trên xuống, có cấp nào áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem tất cả phiếu yêu cầu điều chỉnh của tổng công ty', 'Toàn bộ phiếu.'),
    ('V2', 'Xem tất cả phiếu yêu cầu điều chỉnh của công ty', 'Phiếu thuộc công ty của người đăng nhập.'),
    ('V3', 'Xem tất cả phiếu yêu cầu điều chỉnh của phòng ban', 'Phiếu phòng ban mình quản lý + phiếu mình lập.'),
    ('V4', 'Xem tất cả phiếu yêu cầu điều chỉnh của bộ phận', 'Phiếu bộ phận mình quản lý + phiếu mình lập.'),
    ('—', '(không có quyền nào)', 'Phiếu mình lập.'),
], widths=[0.8, 2.4, 2.8])
d.p('Phiếu Đang tạo chỉ người lập thấy. Người duyệt phiếu và Super admin luôn xem được chi tiết phiếu.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người lập', 'Q1', 'V1–V4', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '✅ (+ màn chờ duyệt)', '✅ (theo cấp)', '✅ (phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅', '✅', '✅'),
    ('FR-05 Lập phiếu', '✅', '✅', '✅', '✅'),
    ('FR-06 Chọn khách hàng / nhà cung cấp', '✅', '✅', '✅', '✅'),
    ('FR-07 Chọn hợp đồng', '✅', '✅', '✅', '✅'),
    ('FR-08 Chỉnh sửa', '✅ (Đang tạo, Từ chối)', '❌', '❌', '❌'),
    ('FR-09 Gửi duyệt', '✅ (Đang tạo, Từ chối)', '❌', '❌', '❌'),
    ('FR-10 Xóa', '✅ (Đang tạo, Từ chối)', '❌', '❌', '❌'),
    ('FR-11 Xem chi tiết', '✅', '✅', '✅ (trong phạm vi)', '✅ (phiếu của mình)'),
    ('FR-12 Từ chối', '❌', '✅ (Chờ tạo phiếu kế toán)', '❌', '❌'),
    ('FR-13 Tạo phiếu kế toán', '❌', '✅ (Chờ tạo phiếu kế toán)', '❌', '❌'),
    ('FR-14 In phiếu', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-15 Xuất Excel', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-16 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅ (phiếu của mình)'),
], widths=[2.0, 1.2, 1.3, 1.0, 1.0])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_LAP, [0, 1, 2, 3, 4, 7, 8]), (A_KT, [0, 5, 6, 7, 8])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Lập phiếu', 'crud'),
     ('FR-08', 'Chỉnh sửa phiếu', 'crud'),
     ('FR-09', 'Gửi duyệt', 'action'),
     ('FR-10', 'Xóa phiếu', 'action'),
     ('FR-12', 'Từ chối phiếu', 'action'),
     ('FR-13', 'Tạo phiếu kế toán', 'action'),
     ('FR-14', 'In phiếu', 'io'),
     ('FR-15', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-11', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
     ('FR-16', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-06', 'Chọn khách hàng / NCC', 'crud', 'extend', [1, 2], None),
     ('FR-07', 'Chọn hợp đồng', 'crud', 'extend', [1, 2], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu yêu cầu điều chỉnh công nợ')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ dùng chung cho màn Tạo (2.5) và Sửa (2.8)
FORM_UI = [
    ('Dòng người lập – ngày giờ', 'Label', 'Read-only', 'dd/mm/yyyy hh:mm', '–', 'Theo người lập', [
        '- Góc phải đầu khối Thông tin chung, dạng “<Người lập> - <ngày giờ lập>”',
        '- Màn Tạo: người đang đăng nhập + thời điểm hiện tại; màn Sửa / Chi tiết: theo phiếu']),
    ('Ô Loại phiếu', 'Dropdown', 'Enable / Disable', 'Danh sách 2 giá trị', 'Có', 'Điều chỉnh công nợ khách hàng', [
        '- Mặc định: Điều chỉnh công nợ khách hàng',
        '- Lựa chọn: Điều chỉnh công nợ khách hàng',
        '- Lựa chọn: Điều chỉnh công nợ nhà cung cấp',
        '- Bị khóa ở màn Sửa, và khi phiếu tạo từ phiếu báo có (dòng chú thích “Loại phiếu lấy theo phiếu báo có, không đổi được”)',
        '- Đổi loại: giữ nguyên bảng chi tiết, đổi nhãn cột theo loại; sang loại NCC thì hiện Tiền tệ, Tỷ giá',
        '- Bỏ trống khi lưu: “Vui lòng chọn loại phiếu”']),
    ('Ô Mã phiếu', 'Textbox', 'Read-only', '–', '–', 'Hệ thống sinh khi lưu', [
        '- Chỉ hiện ở màn Sửa / Chi tiết', '- Dạng <mã công ty>.DNDCCN<tháng năm>.NNNNN (BR-08)']),
    ('Ô Người tạo', 'Textbox', 'Read-only', '–', '–', 'Theo người lập', 'Họ tên người lập phiếu (tự điền).'),
    ('Ô Phòng ban', 'Textbox', 'Read-only', '–', '–', 'Theo người lập', 'Phòng ban của người lập phiếu (tự điền).'),
    ('Ô Tiền tệ', 'Dropdown', 'Enable / Ẩn', 'Danh mục tiền tệ', 'Có (loại NCC, khi gửi duyệt)', 'VNĐ', [
        '- Chỉ hiện với loại Điều chỉnh công nợ nhà cung cấp',
        '- Mặc định: VNĐ (tạo từ phiếu báo có: theo tiền tệ của phiếu báo có)',
        '- Đổi tiền tệ → tự điền Tỷ giá theo danh mục tiền tệ; ngoại tệ thì bảng thêm cột VNĐ']),
    ('Ô Tỷ giá', 'Textbox', 'Enable / Disable', '> 0', 'Có khi tiền tệ khác VNĐ', '1', [
        '- Chỉ hiện với loại NCC; gợi ý “Nhập tỷ giá”',
        '- VNĐ: luôn là 1 và bị khóa',
        '- Ngoại tệ, gửi duyệt mà ≤ 0: “Vui lòng nhập tỷ giá lớn hơn 0”']),
    ('Ô Số phiếu báo có', 'Textbox', 'Read-only', '–', '–', 'Ẩn', [
        '- Chỉ hiện khi phiếu được tạo từ nút “Tạo phiếu yêu cầu điều chỉnh công nợ” ở màn chi tiết Phiếu báo có',
        '- Người dùng không tự chọn phiếu báo có']),
    ('Ô Diễn giải', 'Textarea', 'Enable', 'Văn bản nhiều dòng', 'Có khi gửi duyệt', 'Trống', [
        '- Gợi ý “Nhập diễn giải”', '- Lưu nháp được để trống',
        '- Gửi duyệt mà trống: “Vui lòng nhập diễn giải”']),
    ('Nút Thêm dòng (+)', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', [
        '- Ở góc phải tiêu đề bảng Chi tiết', '- Bấm → thêm 1 nhóm “Điều chỉnh từ” kèm sẵn 1 dòng “Điều chỉnh đến” trống',
        '- Ẩn khi phiếu tạo từ phiếu báo có']),
    ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', 'Có khi gửi duyệt', '“Chưa có dòng điều chỉnh nào.”', [
        '- Tiêu đề 2 khối: “Điều chỉnh từ” | “Điều chỉnh đến *”',
        '- Mỗi nhóm: dòng “từ” (gộp dòng) → các dòng “đến” → dòng “Số tiền còn lại” → dòng nút',
        '- Chưa có nhóm nào: hiện “Chưa có dòng điều chỉnh nào.”',
        '- Gửi duyệt mà bảng rỗng: “Phải có ít nhất một dòng điều chỉnh”']),
    ('Ô Khách hàng / Nhà cung cấp (bên “từ”)', 'Textbox', 'Enable / Read-only', 'Danh sách khách hàng / NCC', 'Có khi gửi duyệt (loại KH)', 'Trống', [
        '- Nhãn “Khách hàng” (loại KH) hoặc “Nhà cung cấp” (loại NCC)',
        '- Bấm ô → mở popup Chọn khách hàng / Chọn nhà cung cấp (mục 2.6); nút × bỏ chọn kèm hợp đồng',
        '- Loại KH, gửi duyệt mà trống: “Bắt buộc phải nhập”',
        '- Phiếu từ phiếu báo có: chỉ đọc; NCC chưa rõ thì điền sẵn KHÁCH KHÔNG RÕ']),
    ('Ô Hợp đồng/Đơn hàng (bên “từ”)', 'Textbox', 'Enable / Disable', 'Hợp đồng của đối tượng đã chọn', 'Không', 'Trống', [
        '- Loại NCC có nhãn “Hợp đồng mua”',
        '- Bị khóa khi chưa chọn đối tượng; rê chuột hiện “Vui lòng chọn khách hàng trước” (NCC: “… nhà cung cấp trước”)',
        '- Bấm ô → mở popup Chọn đơn hàng/hợp đồng (mục 2.7); nút × bỏ hợp đồng, số dư, NVKD']),
    ('Cột Số dư cuối kỳ / Số dư (bên “từ”)', 'Table/Grid', 'Read-only', 'Số, có thể âm', '–', '0', [
        '- Loại KH: “Số dư cuối kỳ” = công nợ còn lại của hợp đồng; loại NCC: “Số dư” của hợp đồng mua',
        '- Tự điền khi chọn hợp đồng; số âm tô đỏ', '- NCC ngoại tệ: thêm cột “Số dư (VNĐ)”']),
    ('Cột NVKD / Nhân viên (bên “từ”)', 'Table/Grid', 'Read-only', '–', '–', 'Trống', [
        '- Loại KH: “NVKD”; loại NCC: “Nhân viên”', '- Người tạo hợp đồng, tự điền khi chọn hợp đồng']),
    ('Ô Số tiền (bên “từ”)', 'Textbox', 'Enable / Read-only', '> 0', 'Có khi gửi duyệt', '0', [
        '- Gợi ý “Nhập số tiền”; tự thêm dấu phẩy ngăn nghìn',
        '- NCC ngoại tệ: nhập nguyên tệ, cột “Số tiền (VNĐ)” bên cạnh = số tiền × tỷ giá',
        '- Gửi duyệt mà ≤ 0: “Phải lớn hơn 0” (lỗi tự ẩn khi sửa lại số > 0)',
        '- Phiếu từ phiếu báo có: lấy theo dòng phiếu báo có, chỉ đọc']),
    ('Nút Xóa nhóm điều chỉnh', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', [
        '- Thùng rác đỏ ở cột cuối của nhóm', '- Bấm → xóa cả nhóm “từ” và các dòng “đến”, không hỏi xác nhận',
        '- Ẩn khi phiếu tạo từ phiếu báo có']),
    ('Ô Khách hàng / Nhà cung cấp (bên “đến”)', 'Textbox', 'Enable', 'Danh sách khách hàng / NCC', 'Có khi gửi duyệt', 'Trống', [
        '- Bấm ô → mở popup chọn (mục 2.6); nút × bỏ chọn kèm hợp đồng',
        '- Gửi duyệt mà trống: “Bắt buộc phải nhập”']),
    ('Ô Hợp đồng/Đơn hàng (bên “đến”)', 'Textbox', 'Enable / Disable', 'Hợp đồng của đối tượng đã chọn', 'Có khi gửi duyệt', 'Trống', [
        '- Có dấu * ở tiêu đề cột; khóa khi chưa chọn đối tượng',
        '- Gửi duyệt mà trống: “Bắt buộc chọn hợp đồng/đơn hàng” (NCC: “Bắt buộc chọn hợp đồng mua”)',
        '- Loại NCC: được để trống khi Nhà cung cấp “đến” là KHÁCH KHÔNG RÕ']),
    ('Cột Số dư cuối kỳ / Số dư (bên “đến”)', 'Table/Grid', 'Read-only', 'Số, có thể âm', '–', '0',
     ['- Như cột cùng tên bên “từ”', '- Tự điền theo hợp đồng “đến”']),
    ('Cột NVKD / Nhân viên (bên “đến”)', 'Table/Grid', 'Read-only', '–', '–', 'Trống', 'Người tạo hợp đồng “đến”, tự điền.'),
    ('Ô Số tiền (bên “đến”)', 'Textbox', 'Enable', '> 0', 'Có khi gửi duyệt', '0', [
        '- Gợi ý “Nhập số tiền”', '- Gửi duyệt mà ≤ 0: “Phải lớn hơn 0”',
        '- Dưới dòng “đến” cuối của nhóm lệch tiền: “Tổng số tiền điều chỉnh đến phải bằng số tiền điều chỉnh từ (còn thiếu X)” hoặc “(thừa X)”, X = chênh lệch']),
    ('Nút Xóa dòng điều chỉnh đến', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', [
        '- Bấm → xóa dòng “đến” đó', '- Nhóm chỉ còn 1 dòng “đến” thì bấm không xóa']),
    ('Dòng Số tiền còn lại', 'Table/Grid', 'Read-only', 'Số', '–', '0', [
        '- = Số tiền bên “từ” − tổng Số tiền các dòng “đến” của nhóm', '- Khác 0 thì tô đỏ (chưa chia hết)']),
    ('Nút Thêm điều chỉnh', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thêm 1 dòng “Điều chỉnh đến” trống vào nhóm.'),
    ('Nút Chọn nhanh hợp đồng', 'Button', 'Enable', '–', '–', 'Hiển thị',
     '- Mở popup Chọn nhanh hợp đồng (mục 2.7) để chia tiền cho nhiều hợp đồng “đến” trong 1 lần'),
    ('Dòng Tổng cộng', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Ẩn', [
        '- Hiện khi bảng có ít nhất 1 nhóm', '- Tổng Số tiền bên “từ” và tổng Số tiền bên “đến”',
        '- Tổng “đến” khác tổng “từ” thì tô đỏ']),
    ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', [
        '- Lưu ở trạng thái Đang tạo; chỉ bắt buộc Loại phiếu', '- Khóa trong lúc đang lưu']),
    ('Nút Gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', [
        '- Lưu và chuyển trạng thái Chờ tạo phiếu kế toán; kiểm đủ luật (BR-01 → BR-04)', '- Khóa trong lúc đang lưu']),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', [
        '- Về màn danh sách (vào từ Phiếu báo có thì về đúng màn đó)',
        '- Có thay đổi chưa lưu → hỏi xác nhận “Thông tin chưa lưu”']),
    ('Hộp Thông tin chưa lưu', 'Popup', 'Hiển thị', '–', '–', 'Ẩn', [
        '- Nội dung: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”',
        '- Nút Thoát: rời màn, bỏ dữ liệu vừa nhập', '- Nút Ở lại: đóng hộp, giữ nguyên form']),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
        '- Chữ đỏ ngay dưới ô sai, ô viền đỏ', '- Chỉ hiện sau lần bấm Lưu / Gửi duyệt đầu tiên; mọi ô sai báo cùng một lượt',
        '- Lỗi chung của bảng (khớp tiền, trùng đối tượng) hiện dưới bảng Chi tiết']),
    ('Toast kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
        '- Lưu nháp: “Lưu phiếu yêu cầu điều chỉnh công nợ thành công”',
        '- Gửi duyệt: “Gửi duyệt phiếu yêu cầu điều chỉnh công nợ thành công”',
        '- Lỗi đã hiện dưới ô: “Vui lòng kiểm tra dữ liệu nhập”; lỗi không có ô (vd quyền): nguyên văn thông báo của hệ thống']),
]

SAVE_DURING = (
    'During:\n'
    '– Lưu nháp: chỉ bắt Loại phiếu → trống thì “Vui lòng chọn loại phiếu”.\n'
    '– Gửi duyệt: Diễn giải trống → “Vui lòng nhập diễn giải”; NCC ngoại tệ mà Tỷ giá ≤ 0 → “Vui lòng nhập tỷ giá lớn hơn 0”.\n'
    '– Gửi duyệt: bảng rỗng → “Phải có ít nhất một dòng điều chỉnh”; nhóm không có dòng “đến” → “Mỗi dòng "Điều chỉnh từ" '
    'phải có ít nhất một dòng "Điều chỉnh đến"”.\n'
    '– Gửi duyệt: đối tượng trống (KH bên “từ”, mọi bên “đến”) → “Bắt buộc phải nhập”; Số tiền ≤ 0 → “Phải lớn hơn 0”; '
    'hợp đồng bên “đến” trống → “Bắt buộc chọn hợp đồng/đơn hàng” (NCC: “Bắt buộc chọn hợp đồng mua”, trừ “đến” là '
    'KHÁCH KHÔNG RÕ).\n'
    '– Các lỗi trên báo cùng một lượt dưới từng ô.\n'
    '– Gửi duyệt: tổng “đến” khác Số tiền “từ” của một nhóm → “Tổng số tiền điều chỉnh đến phải bằng số tiền điều chỉnh '
    'từ (dòng n)”; NCC tạo từ phiếu báo có: tổng “đến” lớn hơn “từ” → “Với phiếu NCC tạo từ báo có, tổng số tiền điều '
    'chỉnh đến không được lớn hơn số tiền điều chỉnh từ”.\n'
    '– Cả nháp lẫn gửi duyệt: “đến” trùng “từ” → “Hợp đồng điều chuyển đến trùng với điều chuyển từ” / “Khách hàng điều '
    'chỉnh đến trùng với khách hàng điều chỉnh từ” / “Phiếu yêu cầu xuất hàng điều chuyển đến trùng với điều chuyển từ” '
    '/ “Hợp đồng mua điều chuyển đến trùng với điều chuyển từ” / “Nhà cung cấp điều chỉnh đến trùng với nhà cung cấp '
    'điều chỉnh từ”.\n' + ERR + '\n')

SAVE_AFTER_NOTIFY = ('– Gửi duyệt: ghi Ngày nhận = thời điểm gửi; gửi thông báo “[DCCN] Chờ duyệt: <mã phiếu>” (kèm số '
                     'phiếu báo có, số tiền, người lập, diễn giải) cho mọi người có quyền Kế toán thanh toán cùng công '
                     'ty của phiếu.\n')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu yêu cầu điều chỉnh công nợ',
       mota='Hiển thị bảng phiếu yêu cầu điều chỉnh công nợ nằm trong phạm vi dữ liệu của người đăng nhập, kèm phân '
            'trang, sắp xếp và tổng số phiếu khớp bộ lọc. Cùng một màn có 2 chế độ theo lối vào: danh sách chung '
            '(người lập theo dõi phiếu) và danh sách chờ duyệt (Kế toán thanh toán xử lý phiếu Chờ tạo phiếu kế toán).',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng vào phân hệ Tài chính hoặc Bán hàng.\n'
                '3. Lối vào chờ duyệt: người dùng có quyền Kế toán thanh toán và có công ty trên hồ sơ nhân sự.',
       chinh='1. Người dùng vào một trong 3 lối vào ở mục Layout.\n'
             '2. Hệ thống xác định chế độ theo lối vào (chung / chờ duyệt) và khôi phục bộ lọc đã dùng trong 10 phút gần '
             'nhất của đúng chế độ đó, cùng cấu hình cột đã lưu của người dùng.\n'
             '3. Chế độ chung: hệ thống xác định cấp quyền xem theo thứ tự V1 → V2 → V3 → V4 (Super admin như V1); '
             'không có cấp nào thì chỉ lấy phiếu do chính người đó lập.\n'
             '4. Hệ thống loại bỏ phiếu Đang tạo của người khác (kể cả với V1).\n'
             '5. Chế độ chờ duyệt: chỉ lấy phiếu Chờ tạo phiếu kế toán của người lập cùng công ty với kế toán.\n'
             '6. Hệ thống trả trang 1, 10 dòng/trang, phiếu tạo gần nhất lên trước, kèm tổng số phiếu.\n'
             '7. Bảng hiển thị dữ liệu; dòng “Hiển thị a–b / N” cho biết khoảng đang xem và tổng.',
       phu='• Không có phiếu nào trong phạm vi → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”, dưới bảng “Không có phiếu nào.”.\n'
           '• Lối vào chờ duyệt mà không có quyền Kế toán thanh toán → danh sách rỗng; lối vào này không có nút Tạo mới.\n'
           '• Đã lưu cấu hình cột riêng → bảng dựng thẳng theo cấu hình đó.\n'
           '• Rời màn quá 10 phút rồi vào lại → bộ lọc trở về mặc định.\n'
           '• Lỗi máy chủ khi nạp → hiển thị “Lỗi khi tải dữ liệu”.\n' + SESSION,
       dacbiet=None),
   layout=dict(entries=[
       (MENU, 'Hiển thị: tiêu đề “Phiếu yêu cầu điều chỉnh công nợ”; phiếu trong phạm vi quyền (Phần 2) — đây là '
              'phạm vi mặc định.'),
       (MENU_SALE, 'Hiển thị: giống lối vào trên (cùng màn, cùng phạm vi).'),
       (MENU_CD, 'Hiển thị: tiêu đề “Phiếu yêu cầu điều chỉnh công nợ chờ duyệt”; chỉ người có quyền Kế toán thanh toán; '
                 'phiếu Chờ tạo phiếu kế toán của người lập cùng công ty.')],
       shot=shot('01_list'), shot_caption='Màn danh sách Phiếu yêu cầu điều chỉnh công nợ'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Phiếu yêu cầu điều chỉnh công nợ', [
           '- Lối vào chờ duyệt: “Phiếu yêu cầu điều chỉnh công nợ chờ duyệt”', '- Cũng là tiêu đề tab trình duyệt']),
       ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', [
           '- Bấm → mở màn Tạo phiếu (mục 2.5)', '- Không gắn quyền riêng', '- Ẩn ở lối vào chờ duyệt']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', [
           '- Bấm → tải file Excel toàn bộ kết quả theo bộ lọc đang áp (mục 2.15)',
           '- Trong lúc xuất: chữ đổi “Đang xuất...” và nút bị khóa']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
        '- Bấm → mở cửa sổ Tùy chỉnh cột (mục 2.4)'),
       ('Cột STT', 'Table/Grid', 'Read-only', '≥ 1', 'Theo dữ liệu', [
           '- Đánh số liên tục qua các trang', '- Ghim trái; khóa trong Tùy chỉnh cột (không ẩn, không đổi vị trí)']),
       ('Cột Mã phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Liên kết: bấm → màn chi tiết (mục 2.11); chuột phải mở được ở tab mới', '- Sắp xếp được',
           '- Ghim trái; khóa trong Tùy chỉnh cột']),
       ('Cột Loại phiếu', 'Table/Grid', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu', [
           '- Điều chỉnh công nợ khách hàng', '- Điều chỉnh công nợ nhà cung cấp']),
       ('Cột Số phiếu báo có', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Liên kết: bấm → mở chi tiết Phiếu báo có ở tab mới', '- Phiếu lập tay: để trống']),
       ('Cột KH / NCC', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Loại KH: khách hàng bên “đến” của dòng “đến” đầu tiên', '- Loại NCC: nhà cung cấp bên “từ” của nhóm đầu tiên',
           '- Dạng “mã - tên”, tự xuống dòng khi dài']),
       ('Cột Số tiền', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', [
           '- Tổng tiền phiếu đã quy đổi VNĐ, định dạng 1,234,567, canh phải', '- Không kèm đơn vị tiền tệ',
           '- Sắp xếp được']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Sắp xếp được.'),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Người lập phiếu.'),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', [
           '- Thời điểm sửa / đổi trạng thái gần nhất', '- Sắp xếp được']),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Người sửa / đổi trạng thái gần nhất.'),
       ('Cột Phòng ban', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Phòng ban của người lập; tự xuống dòng khi dài.'),
       ('Cột Ngày nhận', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', [
           '- Thời điểm gửi duyệt gần nhất; phiếu chưa gửi để trống', '- Sắp xếp được']),
       ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Kế toán thanh toán đã xử lý (từ chối) phiếu.'),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 6 giá trị', 'Theo dữ liệu', [
           '- Nhãn đỏ: Đang tạo, Chờ tạo phiếu kế toán, Hủy, Từ chối',
           '- Nhãn xanh: Đã tạo phiếu kế toán, Đã duyệt phiếu kế toán']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo quyền và trạng thái', [
           '- Nút Sửa, Xóa: người lập, phiếu Đang tạo / Từ chối',
           '- Nút Tạo phiếu kế toán, Từ chối: Kế toán thanh toán cùng công ty, phiếu Chờ tạo phiếu kế toán (Từ chối mở màn chi tiết)',
           '- Nút ba chấm: In phiếu, Xuất Excel, Lịch sử (luôn có)',
           '- Nút không dùng được thì ẩn hẳn; khóa trong Tùy chỉnh cột, luôn ở cuối']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả', [
           '- a–b = khoảng dòng đang xem; N = tổng số phiếu khớp bộ lọc', '- N = 0: hiện “Không có phiếu nào.”']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', '10', [
           '- Mặc định: 10', '- Lựa chọn: 5, 10, 20, 50, 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Nút về đầu / lùi / số trang / tiến / về cuối.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', 'Hiện “Không có dữ liệu phù hợp bộ lọc.” khi N = 0.'),
       ('Dòng Đang tải', 'Label', 'Hiển thị', '–', 'Hiển thị khi mở màn', 'Hiện “Đang tải dữ liệu...” trong lúc nạp.'),
       ('Toast lỗi tải', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', [
           '- Lỗi máy chủ: “Lỗi khi tải dữ liệu”', '- Hết phiên: “Phiên đăng nhập đã hết hạn”, chuyển về màn đăng nhập']),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Xác định chế độ theo lối vào: chung hoặc chờ duyệt.\n'
        '– Chế độ chung: xác định cấp quyền xem V1 → V2 → V3 → V4; không có cấp nào → chỉ phiếu do người dùng lập.\n'
        '– Chế độ chờ duyệt: kiểm tra quyền Kế toán thanh toán và công ty của người dùng; thiếu → trả danh sách rỗng.\n'
        'During:\n– Khôi phục bộ lọc đã dùng trong 10 phút gần nhất của đúng chế độ và cấu hình cột của người dùng.\n'
        '– Áp phạm vi; loại phiếu Đang tạo của người khác; chế độ chờ duyệt chỉ giữ phiếu Chờ tạo phiếu kế toán của '
        'người lập cùng công ty.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, phiếu tạo gần nhất lên trước; dòng “Hiển thị a–b / N”.\n'
        '– Lỗi máy chủ → “Lỗi khi tải dữ liệu”; hết phiên → “Phiên đăng nhập đã hết hạn”, về màn đăng nhập.'),
       ('Chuyển lối vào trên menu', 'System',
        'Before:\n– Người dùng đang ở màn, bấm mục menu của chế độ còn lại (chung ↔ chờ duyệt).\n'
        'During:\n– Lấy bộ lọc đã lưu riêng của chế độ mới (không mang bộ lọc của chế độ cũ sang).\n'
        'After:\n– Đổi tiêu đề, hiện / ẩn nút Tạo mới, về trang 1 và nạp lại danh sách.'),
       ('Bấm Mã phiếu', 'Click',
        'Before:\n– Phiếu đang hiển thị trên lưới (đã nằm trong phạm vi xem).\n'
        'After:\n– Mở màn chi tiết phiếu (mục 2.11); chuột phải cho phép mở ở tab mới.'),
       ('Bấm Số phiếu báo có', 'Click',
        'Before:\n– Chỉ là liên kết khi phiếu được tạo từ phiếu báo có.\n'
        'After:\n– Mở màn chi tiết Phiếu báo có ở tab mới; danh sách giữ nguyên.'),
       ('Bấm tiêu đề cột sắp xếp được', 'Click',
        'Before:\n– Chỉ 5 cột Mã phiếu, Số tiền, Ngày tạo, Ngày cập nhật, Ngày nhận hỗ trợ sắp xếp.\n'
        '– Giữ nguyên bộ lọc đang áp.\n'
        'After:\n– Đổi chiều tăng / giảm, về trang 1 và nạp lại; phiếu cùng giá trị xếp theo phiếu mới hơn trước.'),
       ('Bấm số trang / nút tiến lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp.\n'
        'After:\n– Nạp trang mới; STT tiếp nối liên tục; dòng “Hiển thị a–b / N” cập nhật.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1, nạp lại theo số dòng mới.'),
       ('Bấm nút trong cột Hành động', 'Click',
        'Before:\n– Nút chỉ hiện khi đúng vai và trạng thái (xem dòng Cột Hành động); không đủ điều kiện thì không hiện.\n'
        'After:\n– Sửa → màn Sửa (mục 2.8); Xóa → hộp Xác nhận xóa (mục 2.10).\n'
        '– Tạo phiếu kế toán → màn Tạo phiếu kế toán (mục 2.13); Từ chối → màn chi tiết để nhập lý do (mục 2.12).\n'
        '– Ba chấm → In phiếu (mục 2.14), Xuất Excel (mục 2.15), Lịch sử (mục 2.16).'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu',
       mota='Thu hẹp danh sách phiếu theo ô tìm nhanh (mã phiếu) và 11 ô lọc nâng cao: tổ chức, loại phiếu, trạng '
            'thái, phiếu báo có, đối tượng, hợp đồng hai bên, người tạo, người duyệt, khoảng tiền và khoảng ngày tạo. '
            'Kết quả lọc vẫn nằm trong phạm vi quyền của người dùng.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng nhập mã phiếu vào ô tìm nhanh, bấm Tìm kiếm (hoặc Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc.\n'
             '3. Người dùng chọn / nhập tiêu chí; mỗi lần đổi ô lọc nâng cao hệ thống tự nạp lại từ trang 1.\n'
             '4. Hệ thống kết hợp mọi tiêu chí (đồng thời thỏa) với phạm vi quyền và trả kết quả.\n'
             '5. Hệ thống lưu bộ lọc để vào lại trong 10 phút vẫn còn.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí (kể cả ô tìm nhanh), về trang 1.\n'
           '• Không có phiếu khớp → “Không có dữ liệu phù hợp bộ lọc.”.\n'
           '• Đổi Công ty → Phòng ban, Bộ phận đã chọn bị xóa; đổi Phòng ban → Bộ phận bị xóa.\n'
           '• Ô Khách hàng / Nhà cung cấp gõ dưới 2 ký tự → chưa gợi ý.\n'
           '• Ẩn một ô lọc ở Cài đặt bộ lọc → giá trị của ô đó bị xóa, không lọc ngầm.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'), shot_caption='Khối Bộ lọc danh sách đang mở'),
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Bộ lọc danh sách', 'Đầu khối bộ lọc.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
           '- Gợi ý “Tìm theo mã phiếu...”', '- Tìm mã phiếu chứa chuỗi nhập',
           '- Chỉ áp khi bấm Tìm kiếm hoặc Enter; nút × xóa nhanh chữ đã gõ']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp ô tìm nhanh cùng các ô lọc, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi tiêu chí, nạp lại từ trang 1.'),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị', [
           '- Bấm → mở khối ô lọc nâng cao; chữ đổi thành “Ẩn tìm kiếm nâng cao”', '- Bấm lần nữa → thu gọn']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Trống', [
           '- Chỉ hiện với người có quyền V1', '- Đổi Công ty → xóa Phòng ban, Bộ phận đã chọn']),
       ('Ô Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban', 'Không', 'Trống', [
           '- Hiện với V1, V2, V3', '- Chỉ còn phòng ban của Công ty đã chọn', '- Đổi Phòng ban → xóa Bộ phận']),
       ('Ô Bộ phận', 'Dropdown', 'Enable / Disable', 'Danh sách bộ phận', 'Không', 'Trống', [
           '- Hiện với V1–V4; chỉ chọn được khi có quyền V4', '- Chỉ còn bộ phận của Phòng ban đã chọn']),
       ('Ô Loại phiếu', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống', [
           '- Mặc định: trống (mọi loại)', '- Lựa chọn: Điều chỉnh công nợ khách hàng',
           '- Lựa chọn: Điều chỉnh công nợ nhà cung cấp']),
       ('Ô Trạng thái', 'Dropdown', 'Enable', 'Danh sách 6 giá trị', 'Không', 'Trống', [
           '- Mặc định: trống (mọi trạng thái)',
           '- Lựa chọn: Đang tạo, Chờ tạo phiếu kế toán, Đã tạo phiếu kế toán, Đã duyệt phiếu kế toán, Hủy, Từ chối']),
       ('Ô Số phiếu báo có', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Số phiếu báo có chứa chuỗi nhập.'),
       ('Ô Khách hàng / Nhà cung cấp', 'Dropdown', 'Enable', 'Gõ tối thiểu 2 ký tự', 'Không', 'Trống', [
           '- Gợi ý “Gõ mã hoặc tên khách hàng / nhà cung cấp”',
           '- Một ô chung cho cả khách hàng và nhà cung cấp',
           '- Lọc phiếu có đối tượng này ở bên “từ” hoặc bên “đến”']),
       ('Ô Hợp đồng điều chỉnh từ', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
           '- Gợi ý “Nhập mã hợp đồng điều chỉnh từ”', '- Mã hợp đồng (bán hoặc mua) bên “từ” chứa chuỗi nhập']),
       ('Ô Hợp đồng điều chỉnh đến', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
           '- Gợi ý “Nhập mã hợp đồng điều chỉnh đến”', '- Mã hợp đồng bên “đến” chứa chuỗi nhập']),
       ('Ô Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', 'Lọc theo người lập phiếu.'),
       ('Ô Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', 'Lọc theo Kế toán thanh toán đã xử lý.'),
       ('Ô Số tiền từ', 'Textbox', 'Enable', '≥ 0', 'Không', 'Trống', [
           '- Gợi ý “Nhập số tiền từ”', '- Tổng tiền phiếu (VNĐ) ≥ giá trị nhập; Enter để tìm']),
       ('Ô Số tiền đến', 'Textbox', 'Enable', '≥ 0', 'Không', 'Trống', [
           '- Gợi ý “Nhập số tiền đến”', '- Tổng tiền phiếu (VNĐ) ≤ giá trị nhập']),
       ('Ô Ngày tạo từ', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Ngày tạo ≥ ngày chọn (tính cả ngày đó).'),
       ('Ô Ngày tạo đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Ngày tạo ≤ ngày chọn (tính cả ngày đó).'),
   ],
   ev=[
       ('Nhập ô tìm nhanh, bấm Tìm kiếm / Enter', 'Click',
        'Before:\n– Gõ ô tìm nhanh chưa lọc ngay; chỉ áp khi bấm Tìm kiếm hoặc Enter.\n'
        'During:\n– Kết hợp mã phiếu với các ô lọc đang có giá trị và phạm vi quyền.\n'
        'After:\n– Về trang 1, nạp lại; lưu bộ lọc 10 phút.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối ô lọc đang thu gọn hoặc đang mở.\nAfter:\n– Mở / thu gọn khối; trạng thái mở được nhớ cùng bộ lọc.'),
       ('Đổi ô lọc nâng cao', 'Change',
        'Before:\n– Ô lọc nằm trong danh sách đang bật ở Cài đặt bộ lọc.\n'
        'During:\n– Đổi Công ty → xóa Phòng ban, Bộ phận; đổi Phòng ban → xóa Bộ phận.\n'
        'After:\n– Tự về trang 1 và nạp lại danh sách (không cần bấm Tìm kiếm).'),
       ('Gõ ô Khách hàng / Nhà cung cấp', 'Change',
        'Before:\n– Cần tối thiểu 2 ký tự.\nAfter:\n– Gợi ý khách hàng và nhà cung cấp khớp mã / tên; chọn 1 dòng → nạp lại danh sách.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\n'
        'After:\n– Xóa mọi tiêu chí và ô tìm nhanh, về trang 1, nạp lại; thứ tự sắp xếp về mặc định.'),
       ('Vào lại màn sau khi rời đi', 'System',
        'Before:\n– Kiểm tra bộ lọc đã lưu của đúng chế độ còn trong hạn 10 phút.\n'
        'After:\n– Còn hạn → điền lại tiêu chí và trạng thái mở khối lọc; quá hạn → bộ lọc mặc định.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị',
       mota='Cho người dùng bật / tắt và sắp thứ tự 11 ô lọc của khối Tìm kiếm nâng cao. Cấu hình lưu theo từng người '
            'dùng cho màn này, áp cho cả 2 lối vào.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm Cài đặt bộ lọc trên khối bộ lọc.\n2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” với các ô lọc theo '
             'cấu hình hiện tại.\n3. Người dùng tích / bỏ tích, kéo biểu tượng ⋮⋮ để đổi thứ tự.\n4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, đóng cửa sổ, vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → danh sách và thứ tự về ban đầu (chưa lưu cho tới khi bấm Lưu).\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, thay đổi chưa lưu bị bỏ (không hỏi xác nhận).\n'
           '• Bỏ tích ô đang có giá trị → giá trị đó bị xóa khỏi bộ lọc.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', '–'),
       ('Danh sách ô lọc', 'Table/Grid', 'Enable', '11 mục', '–', 'Theo cấu hình đã lưu', [
           '- Công ty – Phòng ban – Bộ phận, Loại phiếu, Trạng thái, Số phiếu báo có, Khách hàng / Nhà cung cấp',
           '- Hợp đồng điều chỉnh từ, Hợp đồng điều chỉnh đến, Người tạo, Người duyệt, Số tiền, Ngày tạo']),
       ('Ô tích từng ô lọc', 'Checkbox', 'Enable', '–', 'Không', 'Theo cấu hình', 'Tích = hiện ô lọc; bỏ tích = ẩn và xóa giá trị.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Rê chuột hiện “Kéo để sắp xếp”; kéo để đổi thứ tự.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Trả danh sách và thứ tự về cấu hình ban đầu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ; thay đổi chưa lưu bị bỏ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Đóng.')],
   ev=[('Bấm Cài đặt bộ lọc', 'Click', 'Before:\n– Khối bộ lọc đang hiển thị.\nAfter:\n– Mở cửa sổ với cấu hình hiện tại của người dùng.'),
       ('Tích / bỏ tích ô lọc', 'Change', 'Before:\n– Cửa sổ đang mở.\nAfter:\n– Cập nhật danh sách tạm; chưa áp ra màn khi chưa bấm Lưu.'),
       ('Kéo đổi vị trí', 'Drag', 'Before:\n– Kéo bằng biểu tượng ⋮⋮.\nAfter:\n– Đổi thứ tự trong danh sách tạm.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Lưu cấu hình theo người dùng cho màn này.\n' + ERR + '\n'
        'After:\n– Đóng cửa sổ; khối lọc vẽ lại theo thứ tự mới; ô bị ẩn được xóa giá trị và danh sách nạp lại.'),
       ('Bấm Khôi phục mặc định', 'Click', 'Before:\n– Cửa sổ đang mở.\nAfter:\n– Danh sách tạm về 11 ô lọc theo thứ tự ban đầu.'),
       ('Bấm Đóng / (x) / click ra ngoài', 'Click', 'Before:\n– Cửa sổ đang mở.\nAfter:\n– Đóng cửa sổ, bỏ thay đổi chưa lưu.')])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho người dùng bật / tắt và kéo sắp thứ tự 15 cột của bảng danh sách. Cấu hình lưu theo người dùng, dùng '
            'chung cho cả lối vào chung và chờ duyệt; 3 cột STT, Mã phiếu, Hành động bị khóa.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị trên thanh công cụ.\n2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” theo '
             'cấu hình đang áp.\n3. Người dùng tích / bỏ tích, kéo biểu tượng ba gạch để đổi thứ tự.\n4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu theo người dùng, đóng cửa sổ, vẽ lại bảng.',
       phu='• Cột khóa (STT, Mã phiếu, Hành động): xám, không bỏ tích, không kéo; rê chuột hiện “Cột bắt buộc — không thể '
           'ẩn hoặc đổi vị trí”.\n'
           '• Bấm Đóng / (x) / click ra ngoài → đóng, danh sách trả về cấu hình đang áp (không hỏi xác nhận).\n'
           '• Chưa từng lưu → mặc định hiện đủ 15 cột.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', '–'),
       ('Danh sách cột', 'Table/Grid', 'Enable', '15 cột', '–', 'Theo cấu hình đã lưu', [
           '- STT, Mã phiếu, Loại phiếu, Số phiếu báo có, KH / NCC, Số tiền, Ngày tạo, Người tạo',
           '- Ngày cập nhật, Người cập nhật, Phòng ban, Ngày nhận, Người duyệt, Trạng thái, Hành động']),
       ('Ô tích từng cột', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Theo cấu hình', [
           '- Tích = hiện cột', '- STT, Mã phiếu, Hành động: luôn tích, bị khóa']),
       ('Biểu tượng ba gạch', 'Icon Button', 'Enable / Disable', '–', '–', 'Hiển thị', [
           '- Kéo để đổi vị trí cột', '- Cột khóa không kéo được (ổ khóa thay cho ba gạch)']),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi cột.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi cột trừ cột khóa.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ; trả về cấu hình đang áp.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Đóng.')],
   ev=[('Bấm Cấu hình cột hiển thị', 'Click', 'Before:\n– Cấu hình cột của người dùng đã nạp xong.\nAfter:\n– Mở cửa sổ đúng thứ tự cột đang áp.'),
       ('Tích / bỏ tích cột', 'Change', 'Before:\n– Cột không phải cột khóa.\nAfter:\n– Cập nhật danh sách tạm.'),
       ('Kéo biểu tượng ba gạch', 'Drag', 'Before:\n– Cột không phải cột khóa.\nAfter:\n– Đổi thứ tự cột trong danh sách tạm.'),
       ('Bấm Chọn tất cả / Bỏ chọn hết', 'Click', 'Before:\n– Cửa sổ đang mở.\nAfter:\n– Tích / bỏ tích hàng loạt; cột khóa giữ nguyên.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cửa sổ đang mở.\nDuring:\n– Lưu cấu hình theo người dùng cho màn này (dùng chung 2 lối vào).\n' + ERR + '\n'
        'After:\n– Đóng cửa sổ, vẽ lại bảng theo cột và thứ tự mới; vào lại màn vẫn giữ.'),
       ('Bấm Đóng / (x) / click ra ngoài', 'Click', 'Before:\n– Cửa sổ đang mở.\nAfter:\n– Đóng, bỏ thay đổi, bảng giữ nguyên.')])

# ------------------------------------------------------------ 2.5
fr(5, 'Lập phiếu yêu cầu điều chỉnh công nợ', usecase=('FR-05', 'Lập phiếu', 'crud', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Lập phiếu yêu cầu điều chỉnh công nợ',
       mota='Người lập đề nghị chuyển công nợ từ khách hàng / nhà cung cấp, hợp đồng này sang khách hàng / nhà cung '
            'cấp, hợp đồng khác. Phiếu gồm thông tin chung và bảng chi tiết 2 cấp “Điều chỉnh từ” → “Điều chỉnh đến”; '
            'lưu nháp để làm tiếp hoặc gửi duyệt cho Kế toán thanh toán.',
       tacnhan=TN_MOI,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách (lối vào chung) hoặc màn chi tiết '
                'Phiếu báo có.\n3. Đối tượng và hợp đồng cần điều chỉnh đã có trong danh mục.',
       chinh='1. Người dùng bấm Tạo mới (hoặc “Tạo phiếu yêu cầu điều chỉnh công nợ” ở màn chi tiết Phiếu báo có).\n'
             '2. Hệ thống mở màn “Tạo phiếu yêu cầu điều chỉnh công nợ”: Loại phiếu mặc định khách hàng, Người tạo / '
             'Phòng ban theo người đăng nhập.\n'
             '3. Người dùng chọn Loại phiếu; loại NCC chọn thêm Tiền tệ (Tỷ giá tự điền), nhập Diễn giải.\n'
             '4. Người dùng bấm Thêm dòng; ở dòng “từ” chọn khách hàng / NCC (mục 2.6), hợp đồng (mục 2.7), nhập Số tiền.\n'
             '5. Ở dòng “đến” chọn đối tượng, hợp đồng, nhập Số tiền; bấm Thêm điều chỉnh hoặc Chọn nhanh hợp đồng để '
             'chia cho nhiều nơi, tới khi dòng Số tiền còn lại = 0.\n'
             '6. Người dùng bấm Lưu nháp hoặc Gửi duyệt.\n'
             '7. Hệ thống kiểm tra dữ liệu (BR-01 → BR-04), sinh mã phiếu, lưu phiếu với công ty / phòng ban / bộ phận '
             'của người lập.\n'
             '8. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của phiếu.\n'
             '9. Gửi duyệt: hệ thống ghi Ngày nhận và gửi thông báo cho Kế toán thanh toán cùng công ty.\n'
             '10. Hệ thống hiện thông báo thành công và quay về màn danh sách (hoặc màn đã mở form).',
       phu='• Lỗi kiểm tra → báo đỏ tại từng ô cùng một lượt, toast “Vui lòng kiểm tra dữ liệu nhập”, cuộn tới ô lỗi '
           'đầu tiên; phiếu chưa được lưu.\n'
           '• Bấm Lưu và tiếp tục → lưu nháp rồi mở form trống để lập phiếu kế tiếp.\n'
           '• Tạo từ phiếu báo có → dòng “từ” điền sẵn theo các dòng phiếu báo có đã chọn và bị khóa; Loại phiếu khóa theo '
           'loại thu của phiếu báo có; NCC chưa rõ điền KHÁCH KHÔNG RÕ.\n'
           '• Bấm Quay lại / rời màn khi đã nhập → hộp “Thông tin chưa lưu”: Thoát thì bỏ dữ liệu, Ở lại thì giữ form.\n'
           '• Không tải được dòng phiếu báo có → “Không tải được chi tiết phiếu báo có”.\n' + SESSION,
       dacbiet='Tổng tiền phiếu lưu theo VNĐ (NCC ngoại tệ = số tiền × tỷ giá). Nút Lưu nháp / Gửi duyệt / Lưu và tiếp '
               'tục bị khóa trong lúc đang lưu để không tạo trùng phiếu.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10c_filled'), shot_caption='Màn Tạo phiếu yêu cầu điều chỉnh công nợ đã nhập dữ liệu'),
   ui=[('Tiêu đề màn', 'Label', 'Hiển thị', '–', '–', 'Tạo phiếu yêu cầu điều chỉnh công nợ', 'Tiêu đề trang và tab trình duyệt.')]
      + FORM_UI
      + [('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', [
          '- Chỉ ở màn Tạo; rê chuột hiện “Lưu nháp phiếu này rồi tiếp tục lập phiếu mới”',
          '- Lưu nháp xong ở lại, form trống để lập phiếu kế tiếp'])],
   ev=[
       ('Mở màn Tạo', 'System',
        'Before:\n– Người dùng bấm Tạo mới ở lối vào chung, hoặc nút tạo ở màn chi tiết Phiếu báo có (mang theo các dòng đã tích).\n'
        'During:\n– Nạp danh mục Loại phiếu, Tiền tệ, người lập; có dòng phiếu báo có thì nạp và khóa Loại phiếu, bên “từ”.\n'
        'After:\n– Hiện form; Loại phiếu = Điều chỉnh công nợ khách hàng; chốt mốc để nhận biết thay đổi chưa lưu.'),
       ('Đổi Loại phiếu', 'Change',
        'Before:\n– Chỉ đổi được ở màn Tạo, khi phiếu không tạo từ phiếu báo có.\n'
        'After:\n– Giữ nguyên bảng chi tiết, đổi nhãn cột (Khách hàng ↔ Nhà cung cấp, Hợp đồng/Đơn hàng ↔ Hợp đồng mua…).\n'
        '– Sang NCC: hiện Tiền tệ (mặc định VNĐ, hoặc theo phiếu báo có), Tỷ giá; về KH: bỏ Tiền tệ, Tỷ giá.'),
       ('Đổi Tiền tệ', 'Change',
        'Before:\n– Loại phiếu NCC.\n'
        'After:\n– Tỷ giá tự điền theo danh mục tiền tệ (VNĐ = 1 và khóa); ngoại tệ thì bảng thêm cột Số dư (VNĐ), Số tiền (VNĐ).'),
       ('Bấm Thêm dòng / Thêm điều chỉnh', 'Click',
        'Before:\n– Thêm dòng chỉ có khi phiếu không tạo từ phiếu báo có.\n'
        'After:\n– Thêm 1 nhóm “từ” kèm 1 dòng “đến” trống, hoặc thêm 1 dòng “đến” vào nhóm.'),
       ('Bấm ô đối tượng / hợp đồng', 'Click',
        'Before:\n– Ô hợp đồng khóa khi dòng chưa có đối tượng → hiện “Vui lòng chọn khách hàng trước” (NCC: “Vui lòng chọn nhà cung cấp trước”).\n'
        'After:\n– Mở popup chọn tương ứng (mục 2.6, 2.7); bấm × thì bỏ giá trị và số liệu ăn theo.'),
       ('Bấm Xóa nhóm / Xóa dòng điều chỉnh đến', 'Click',
        'Before:\n– Nhóm “từ” chỉ xóa được khi phiếu không tạo từ phiếu báo có; dòng “đến” chỉ xóa khi nhóm còn ≥ 2 dòng.\n'
        'After:\n– Xóa ngay trên form (chưa lưu); dòng Số tiền còn lại và Tổng cộng tính lại.'),
       ('Nhập Số tiền', 'Change',
        'Before:\n– Ô cho gõ số, tự thêm dấu phẩy ngăn nghìn.\n'
        'After:\n– Tính lại Số tiền còn lại của nhóm, Tổng cộng, cột VNĐ (ngoại tệ); đã gửi duyệt lỗi thì cập nhật dòng lệch tiền ngay.'),
       ('Bấm Lưu nháp / Gửi duyệt / Lưu và tiếp tục', 'Click',
        'Before:\n– Lập phiếu không gắn quyền riêng; nút bị khóa nếu đang có lượt lưu chưa xong.\n' + SAVE_DURING +
        'After:\n– Sinh mã <mã công ty>.DNDCCN<mmyy>.NNNNN; lưu phiếu, các dòng “từ”, “đến”; công ty / phòng ban / bộ phận '
        'theo người lập; trạng thái Đang tạo (nháp) hoặc Chờ tạo phiếu kế toán (gửi duyệt).\n'
        '– Ghi một dòng lịch sử “Tạo mới” (kèm bảng chi tiết).\n' + SAVE_AFTER_NOTIFY +
        '– Hiển thị “Lưu phiếu yêu cầu điều chỉnh công nợ thành công” / “Gửi duyệt phiếu yêu cầu điều chỉnh công nợ thành '
        'công”; về màn danh sách (Lưu và tiếp tục: ở lại với form trống).'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu form với mốc lúc mở.\n'
        'During:\n– Có thay đổi chưa lưu → hộp “Thông tin chưa lưu”: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”.\n'
        'After:\n– Thoát → về màn danh sách (hoặc màn đã mở form); Ở lại → giữ nguyên form.'),
   ])

# ------------------------------------------------------------ 2.6
fr(6, 'Chọn khách hàng / nhà cung cấp', usecase=('FR-06', 'Chọn khách hàng / NCC', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(
       ten='Chọn khách hàng / nhà cung cấp cho dòng điều chỉnh',
       mota='Popup tìm và chọn đối tượng cho bên “Điều chỉnh từ” hoặc “Điều chỉnh đến”: loại KH mở popup “Chọn khách '
            'hàng” (đủ khách hàng, không giới hạn phạm vi quyền); loại NCC mở popup “Chọn nhà cung cấp”. Đổi sang đối '
            'tượng khác thì hợp đồng cũ của dòng bị xóa để không ghép nhầm hợp đồng của người khác.',
       tacnhan=TN_MOI,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn Tạo hoặc Sửa phiếu.\n'
                '3. Bảng chi tiết đã có dòng; ô đối tượng không bị khóa (không phải bên “từ” của phiếu từ phiếu báo có).',
       chinh='1. Người dùng bấm ô Khách hàng (Nhà cung cấp) của dòng.\n'
             '2. Hệ thống mở popup, ô tìm trống, nạp trang 1 (10 dòng).\n'
             '3. Người dùng nhập điều kiện (KH: tên / mã, MST, SĐT; NCC: mã hoặc tên), bấm Tìm kiếm hoặc Enter.\n'
             '4. Người dùng bấm vào dòng cần chọn.\n'
             '5. Hệ thống điền “mã - tên” vào ô; nếu khác đối tượng cũ thì xóa hợp đồng, số dư, NVKD của dòng.\n'
             '6. Hệ thống đóng popup (KH: hiện “Chọn khách hàng thành công”).',
       phu='• Không có kết quả → KH: “Không có dữ liệu phù hợp bộ lọc”; NCC: “Không có nhà cung cấp phù hợp.”.\n'
           '• Khách hàng cá nhân đang được Sales khác đăng ký còn hạn → báo lỗi “Đã có người đăng ký nên bạn không được '
           'phép chọn” (hoặc thông báo riêng của khách đó), không chọn.\n'
           '• Bấm Đóng / (x) / click ra ngoài → đóng popup, dòng giữ nguyên.\n'
           '• Chọn lại đúng đối tượng cũ → giữ nguyên hợp đồng đã chọn.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('11_customer'), shot_caption='Cửa sổ Chọn khách hàng',
               note='Modal Chọn khách hàng (Chọn nhà cung cấp với loại NCC) được mở ngay trên màn hình Tạo / Sửa phiếu theo đường dẫn ở trên.'),
   ui=[('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Chọn khách hàng', 'Loại NCC: “Chọn nhà cung cấp”.'),
       ('Ô Tên hoặc mã khách hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
           '- Gợi ý “Nhập tên / mã khách hàng”', '- Enter để tìm']),
       ('Ô Mã số thuế', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '- Gợi ý “Nhập mã số thuế”; Enter để tìm'),
       ('Ô Số điện thoại', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '- Gợi ý “Nhập số điện thoại”; Enter để tìm'),
       ('Ô Mã hoặc tên nhà cung cấp', 'Textbox', 'Enable / Ẩn', '0–255 ký tự', 'Không', 'Trống', [
           '- Chỉ ở popup Chọn nhà cung cấp', '- Gợi ý “Nhập mã hoặc tên nhà cung cấp”']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp điều kiện, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa điều kiện, nạp lại trang 1.'),
       ('Bảng khách hàng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', [
           '- Cột: STT, Mã KH - Tên khách hàng, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP',
           '- Bấm một dòng → chọn khách hàng đó']),
       ('Bảng nhà cung cấp', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', [
           '- Cột: STT, Mã nhà cung cấp (sắp xếp được), Tên nhà cung cấp (sắp xếp được)', '- Bấm một dòng → chọn']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', '10', [
           '- Mặc định: 10', '- Lựa chọn: 10, 20, 50, 100']),
       ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1', 'Chuyển trang giữ nguyên điều kiện tìm.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', [
           '- KH: “Không có dữ liệu phù hợp bộ lọc”', '- NCC: “Không có nhà cung cấp phù hợp.”']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng popup, không chọn.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Đóng.'),
       ('Toast kết quả chọn', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
           '- Chọn KH thành công: “Chọn khách hàng thành công”',
           '- KH đang được Sales khác đăng ký: “Đã có người đăng ký nên bạn không được phép chọn”'])],
   ev=[('Mở popup', 'System',
        'Before:\n– Loại phiếu quyết định popup: KH → Chọn khách hàng, NCC → Chọn nhà cung cấp.\n'
        'After:\n– Xóa điều kiện tìm của lần trước, nạp trang 1 (10 dòng).'),
       ('Bấm Tìm kiếm / Enter', 'Click',
        'Before:\n– Điều kiện có thể để trống (lấy tất cả).\nAfter:\n– Về trang 1, nạp kết quả khớp điều kiện.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Popup đang mở.\nAfter:\n– Xóa điều kiện, nạp lại trang 1.'),
       ('Bấm một dòng', 'Click',
        'Before:\n– KH cá nhân đang được Sales khác đăng ký còn hạn → “Đã có người đăng ký nên bạn không được phép chọn”, dừng.\n'
        'During:\n– So với đối tượng đang có ở dòng: khác → xóa hợp đồng, số dư, NVKD của dòng.\n'
        'After:\n– Điền “mã - tên” vào ô; KH hiện “Chọn khách hàng thành công”; đóng popup.'),
       ('Đổi trang / Số dòng/trang', 'Click', 'Before:\n– Giữ nguyên điều kiện tìm.\nAfter:\n– Nạp trang mới.'),
       ('Bấm Đóng / (x) / click ra ngoài', 'Click', 'Before:\n– Popup đang mở.\nAfter:\n– Đóng popup, dòng giữ nguyên.')])

# ------------------------------------------------------------ 2.7
fr(7, 'Chọn hợp đồng', usecase=('FR-07', 'Chọn hợp đồng', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(
       ten='Chọn đơn hàng/hợp đồng (hợp đồng mua với loại NCC) cho dòng điều chỉnh',
       mota='Có 2 cách gắn hợp đồng: (1) bấm ô Hợp đồng/Đơn hàng của một dòng → popup “Chọn đơn hàng/hợp đồng” liệt kê '
            'hợp đồng của đúng đối tượng đã chọn kèm giá trị và số tiền còn nợ; (2) bấm “Chọn nhanh hợp đồng” của một '
            'nhóm → popup chia Số tiền “từ” cho nhiều hợp đồng “đến” trong 1 lần.',
       tacnhan=TN_MOI,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn Tạo hoặc Sửa phiếu.\n'
                '3. Cách 1: dòng đã chọn khách hàng / NCC. Cách 2: nhóm đã có Số tiền “từ” > 0.',
       chinh='1. Người dùng bấm ô Hợp đồng/Đơn hàng của dòng.\n'
             '2. Hệ thống mở popup “Chọn đơn hàng/hợp đồng” (NCC: “Chọn hợp đồng mua”), dòng phụ ghi tên đối tượng.\n'
             '3. Người dùng tìm theo số hợp đồng, bấm vào dòng hợp đồng.\n'
             '4. Hệ thống điền mã hợp đồng, Số dư cuối kỳ (Số dư), NVKD (Nhân viên) vào dòng và đóng popup.\n'
             '5. Hoặc: bấm Chọn nhanh hợp đồng, chọn đối tượng, nhập Số tiền điều chỉnh đến cho từng hợp đồng, bấm Áp dụng.\n'
             '6. Hệ thống thêm các dòng “đến” tương ứng vào nhóm và đóng popup.',
       phu='• Chưa chọn đối tượng → ô hợp đồng bị khóa, rê chuột hiện “Vui lòng chọn khách hàng trước”.\n'
           '• Đối tượng không có hợp đồng → “Không có hợp đồng phù hợp.”.\n'
           '• Chọn nhanh: tổng số tiền vượt Số tiền “từ” → dòng vượt báo “Tổng số tiền vượt quá số tiền điều chỉnh từ”, '
           'không áp dụng.\n'
           '• Chọn nhanh lại cùng khách hàng (KH) / cùng hợp đồng mua (NCC) → dòng cũ được thay bằng dòng mới.\n'
           '• Bấm Đóng / (x) / click ra ngoài → đóng popup, dòng giữ nguyên.',
       dacbiet='Nguồn hợp đồng bán: hợp đồng trên HRM, hợp đồng bán ERP, hợp đồng bán đầu kỳ, hợp đồng dịch vụ BH-SC; chỉ '
               'hợp đồng do chính người lập tạo, hợp đồng bảo dưỡng bỏ trạng thái Hủy / Đang tạo / Chờ duyệt.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('12_contract'), shot_caption='Cửa sổ Chọn đơn hàng/hợp đồng',
               note='Modal Chọn đơn hàng/hợp đồng và modal Chọn nhanh hợp đồng được mở ngay trên màn hình Tạo / Sửa phiếu theo đường dẫn ở trên.'),
   ui=[('Tiêu đề popup chọn hợp đồng', 'Label', 'Hiển thị', '–', '–', 'Chọn đơn hàng/hợp đồng', [
           '- Loại NCC: “Chọn hợp đồng mua”', '- Dòng phụ: tên khách hàng / NCC của dòng']),
       ('Ô Số đơn hàng/Hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
           '- Gợi ý “Nhập số hợp đồng”', '- Enter để tìm']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp điều kiện, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa điều kiện, nạp lại trang 1.'),
       ('Bảng hợp đồng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', [
           '- Cột: STT, Số đơn hàng/Hợp đồng (sắp xếp được), Ngày lập (sắp xếp được), Giá trị hợp đồng, Số tiền còn nợ',
           '- Bấm số hợp đồng → xem hợp đồng ở tab mới', '- Bấm phần còn lại của dòng → chọn hợp đồng']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', '10', ['- Mặc định: 10', '- Lựa chọn: 10, 20, 50, 100']),
       ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1', 'Giữ điều kiện tìm khi chuyển trang.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '“Không có hợp đồng phù hợp.”'),
       ('Tiêu đề popup chọn nhanh', 'Label', 'Hiển thị', '–', '–', 'Hợp đồng', [
           '- Loại NCC: “Hợp đồng mua”', '- Dòng phụ: “Tổng số tiền điều chỉnh từ” = Số tiền “từ” của nhóm (trần phân bổ)']),
       ('Ô Khách hàng / Nhà cung cấp (popup)', 'Dropdown', 'Enable', 'Gõ để tìm', 'Có', 'Trống', [
           '- Gợi ý “Chọn khách hàng” (NCC: “Chọn nhà cung cấp”)', '- Chọn xong tự nạp danh sách hợp đồng']),
       ('Ô Hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
           '- NCC: nhãn “Hợp đồng mua”; gợi ý “Nhập mã hợp đồng”', '- Nút × xóa chữ và tìm lại']),
       ('Bảng hợp đồng chọn nhanh', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu', [
           '- Cột: STT, Đơn hàng/ Hợp đồng (NCC: Hợp đồng mua), Giá trị hợp đồng, Còn nợ (NCC: Số dư), Số tiền điều chỉnh đến',
           '- Ngoại tệ: thêm cột VNĐ quy đổi',
           '- Chưa chọn đối tượng: “Chọn khách hàng để xem danh sách hợp đồng”; không có: “Không có hợp đồng phù hợp”']),
       ('Ô Số tiền điều chỉnh đến', 'Textbox', 'Enable', '≥ 0', 'Không', 'Trống', [
           '- Gợi ý “0”; bỏ trống / 0 = không lấy hợp đồng đó',
           '- Dòng làm tổng vượt trần: “Tổng số tiền vượt quá số tiền điều chỉnh từ”']),
       ('Nút Áp dụng', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Thêm các hợp đồng có số tiền > 0 thành dòng “đến” của nhóm.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng popup, không thay đổi dòng.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Đóng.'),
       ('Toast cảnh báo chọn nhanh', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
           '- “Chưa chọn khách hàng” (NCC: “Chưa chọn nhà cung cấp”)', '- “Số tiền điều chỉnh từ không hợp lệ”',
           '- “Tổng số tiền điều chỉnh đến không được lớn hơn số tiền điều chỉnh từ”',
           '- “Chưa nhập số tiền điều chỉnh cho hợp đồng nào”'])],
   ev=[('Bấm ô Hợp đồng/Đơn hàng', 'Click',
        'Before:\n– Dòng chưa có đối tượng → ô khóa, cảnh báo “Vui lòng chọn khách hàng trước” (NCC: “… nhà cung cấp trước”).\n'
        'After:\n– Mở popup Chọn đơn hàng/hợp đồng, lọc theo đúng đối tượng của dòng.'),
       ('Bấm một dòng hợp đồng', 'Click',
        'Before:\n– Bấm vào chữ số hợp đồng là mở hợp đồng ở tab mới, không chọn.\n'
        'During:\n– Tra thêm người tạo hợp đồng và số dư chính xác; tra lỗi thì để trống NVKD, vẫn lưu được.\n'
        'After:\n– Điền mã hợp đồng, Số dư cuối kỳ (Số dư), NVKD (Nhân viên); đóng popup.'),
       ('Bấm Chọn nhanh hợp đồng', 'Click', 'Before:\n– Bấm ở dòng nút của đúng nhóm.\nAfter:\n– Mở popup, dòng phụ ghi Số tiền “từ” của nhóm.'),
       ('Chọn đối tượng / bấm Tìm kiếm (chọn nhanh)', 'Change',
        'Before:\n– Chưa chọn đối tượng mà bấm Tìm kiếm → “Chưa chọn khách hàng” (NCC: “Chưa chọn nhà cung cấp”).\n'
        'After:\n– Nạp hợp đồng của đối tượng (lọc theo mã hợp đồng nếu có); lỗi → “Không tải được danh sách hợp đồng”.'),
       ('Bấm Áp dụng', 'Click',
        'Before:\n– Số tiền “từ” của nhóm ≤ 0 → “Số tiền điều chỉnh từ không hợp lệ”, dừng.\n'
        'During:\n– Cộng dần theo thứ tự dòng; dòng làm tổng vượt trần → báo dưới ô “Tổng số tiền vượt quá số tiền điều chỉnh từ” '
        'và toast “Tổng số tiền điều chỉnh đến không được lớn hơn số tiền điều chỉnh từ”.\n'
        '– Không dòng nào có số tiền > 0 → “Chưa nhập số tiền điều chỉnh cho hợp đồng nào”.\n' + ERR + '\n'
        'After:\n– KH: xóa các dòng “đến” cùng khách hàng rồi thêm dòng mới; NCC: xóa dòng trùng hợp đồng mua rồi thêm.\n'
        '– Đóng popup; Số tiền còn lại và Tổng cộng tính lại (chưa lưu phiếu).'),
       ('Bấm Làm mới (chọn nhanh)', 'Click', 'Before:\n– Popup chọn nhanh đang mở.\nAfter:\n– Xóa đối tượng, mã hợp đồng và bảng; không nạp lại.'),
       ('Bấm Đóng / (x) / click ra ngoài', 'Click', 'Before:\n– Popup đang mở.\nAfter:\n– Đóng popup, dòng giữ nguyên.')])

# ------------------------------------------------------------ 2.8
fr(8, 'Chỉnh sửa phiếu', usecase=('FR-08', 'Chỉnh sửa phiếu', 'crud', A_LAP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Chỉnh sửa phiếu yêu cầu điều chỉnh công nợ',
       mota='Người lập sửa phiếu còn ở trạng thái Đang tạo hoặc bị Kế toán thanh toán từ chối, rồi lưu nháp hoặc gửi '
            'duyệt lại. Quy tắc nhập liệu giống màn Tạo; Loại phiếu bị khóa.',
       tacnhan=TN_SUA, dieukien=DK_SUA,
       chinh='1. Người dùng bấm Sửa ở cột Hành động hoặc ở màn chi tiết.\n'
             '2. Hệ thống mở màn “Sửa phiếu yêu cầu điều chỉnh công nợ: <mã>” với dữ liệu phiếu; Người tạo / Phòng ban '
             'theo người lập.\n'
             '3. Người dùng sửa thông tin và bảng chi tiết (quy tắc như mục 2.5).\n'
             '4. Người dùng bấm Lưu nháp hoặc Gửi duyệt.\n'
             '5. Hệ thống kiểm tra quyền sửa (người lập, phiếu Đang tạo / Từ chối) và dữ liệu.\n'
             '6. Hệ thống lưu phiếu, thay toàn bộ bảng chi tiết theo form.\n'
             '7. Hệ thống ghi nhận hành động “Thay đổi thông tin” trong lịch sử của phiếu (giá trị cũ → mới).\n'
             '8. Gửi duyệt: chuyển Chờ tạo phiếu kế toán, xóa lý do từ chối cũ, ghi Ngày nhận, gửi thông báo cho Kế toán '
             'thanh toán cùng công ty.\n'
             '9. Hệ thống hiện thông báo thành công và về màn danh sách.',
       phu='• Không phải người lập hoặc phiếu đã sang trạng thái khác → “Bạn không có quyền sửa phiếu này”, không lưu.\n'
           '• Lỗi kiểm tra → báo đỏ tại từng ô cùng một lượt như mục 2.5.\n'
           '• Phiếu Từ chối → màn chi tiết hiện ô Ghi chú không duyệt (lý do) để người lập biết cần sửa gì.\n'
           '• Bấm Quay lại khi đã sửa → hộp “Thông tin chưa lưu”.\n'
           '• Không tải được phiếu → “Không tải được dữ liệu phiếu”.\n' + SESSION,
       dacbiet='Màn Sửa không có nút Lưu và tiếp tục. Nút lưu bị khóa trong lúc đang xử lý.'),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('19_edit'), shot_caption='Màn Sửa phiếu yêu cầu điều chỉnh công nợ'),
   ui=[('Tiêu đề màn', 'Label', 'Hiển thị', '–', '–', 'Sửa phiếu yêu cầu điều chỉnh công nợ: <mã>', 'Tiêu đề trang và tab trình duyệt.')]
      + FORM_UI,
   ev=[('Mở màn Sửa', 'System',
        'Before:\n– Nút Sửa chỉ hiện với người lập, phiếu Đang tạo / Từ chối.\n– Phiếu ngoài phạm vi xem → ' + NO_VIEW + '.\n'
        'During:\n– Nạp phiếu, danh mục; Loại phiếu khóa.\n'
        'After:\n– Hiện form có dữ liệu; chốt mốc để nhận biết thay đổi chưa lưu.'),
       ('Sửa thông tin, bảng chi tiết', 'Change',
        'Before:\n– Quy tắc từng ô như mục 2.5 (Đổi Tiền tệ, Thêm / Xóa dòng, chọn đối tượng, hợp đồng).\n'
        'After:\n– Số tiền còn lại, Tổng cộng tính lại ngay.'),
       ('Bấm Lưu nháp / Gửi duyệt', 'Click',
        'Before:\n– Kiểm tra người dùng là người lập và phiếu Đang tạo / Từ chối.\n'
        '– Nếu không → hiển thị “Bạn không có quyền sửa phiếu này” và dừng xử lý.\n' + SAVE_DURING +
        'After:\n– Lưu đầu phiếu, thay bảng chi tiết; Người cập nhật / Ngày cập nhật = người, thời điểm sửa.\n'
        '– Ghi một dòng lịch sử “Thay đổi thông tin” (loại phiếu, phiếu báo có, diễn giải, tiền tệ, tỷ giá, tổng tiền, '
        'bảng chi tiết cũ → mới).\n'
        '– Gửi duyệt: trạng thái Chờ tạo phiếu kế toán, xóa lý do từ chối cũ.\n' + SAVE_AFTER_NOTIFY +
        '– Hiển thị “Lưu phiếu yêu cầu điều chỉnh công nợ thành công” / “Gửi duyệt phiếu yêu cầu điều chỉnh công nợ '
        'thành công”; về màn danh sách.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu form với mốc lúc mở.\n'
        'During:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\nAfter:\n– Thoát → về danh sách; Ở lại → giữ form.')])

# ------------------------------------------------------------ 2.9
fr(9, 'Gửi duyệt phiếu', usecase=('FR-09', 'Gửi duyệt', 'action', A_LAP),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Gửi duyệt phiếu từ màn chi tiết',
       mota='Người lập gửi phiếu Đang tạo / Từ chối cho Kế toán thanh toán ngay ở màn chi tiết mà không mở form Sửa. Hệ '
            'thống kiểm lại dữ liệu ĐÃ LƯU của phiếu với cùng luật như khi gửi duyệt ở form.',
       tacnhan=TN_SUA, dieukien=DK_SUA,
       chinh='1. Người dùng mở màn chi tiết phiếu, bấm Gửi duyệt ở chân màn.\n'
             '2. Hệ thống kiểm tra cặp trạng thái hợp lệ (Đang tạo / Từ chối → Chờ tạo phiếu kế toán) và người lập.\n'
             '3. Hệ thống kiểm tra dữ liệu đã lưu: diễn giải, tỷ giá, dòng, đối tượng, hợp đồng, số tiền, khớp tổng tiền.\n'
             '4. Hệ thống chuyển phiếu sang Chờ tạo phiếu kế toán, ghi Ngày nhận, xóa lý do từ chối cũ.\n'
             '5. Hệ thống ghi nhận hành động “Thay đổi trạng thái” trong lịch sử của phiếu.\n'
             '6. Hệ thống gửi thông báo cho Kế toán thanh toán cùng công ty của phiếu.\n'
             '7. Hệ thống hiện “Gửi duyệt phiếu yêu cầu điều chỉnh công nợ thành công” và tải lại màn chi tiết.',
       phu='• Dữ liệu chưa đủ → hiện nguyên văn lỗi đầu tiên (vd “Dòng 1 chưa có dòng "Điều chỉnh đến" nào”), phiếu giữ '
           'trạng thái cũ.\n'
           '• Phiếu đã được gửi / xử lý ở nơi khác → “Không thể chuyển phiếu từ trạng thái hiện tại sang trạng thái này”.\n'
           '• Không phải người lập → nút không hiện; gọi thẳng thì “Bạn không có quyền gửi duyệt phiếu này”.\n' + SESSION,
       dacbiet='Nút Gửi duyệt bị khóa trong lúc đang xử lý (chặn bấm 2 lần).'),
   layout=dict(menu=MENU + ' => Xem chi tiết => Gửi duyệt', shot=shot('19_edit'),
               shot_caption='Phiếu Đang tạo — nút Gửi duyệt ở chân màn'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Gửi duyệt', 'Button', 'Enable / Ẩn', 'Ẩn', [
           '- Ở chân màn chi tiết; chỉ hiện với người lập, phiếu Đang tạo / Từ chối',
           '- Khóa trong lúc đang xử lý; danh sách không có nút này']),
       ('Lớp tải toàn trang', 'Label', 'Hiển thị', 'Ẩn', 'Che màn trong lúc gửi để người dùng không thao tác thêm.'),
       ('Toast thành công', 'Toast / Alert', 'Hiển thị', 'Ẩn', '“Gửi duyệt phiếu yêu cầu điều chỉnh công nợ thành công”'),
       ('Toast lỗi', 'Toast / Alert', 'Hiển thị', 'Ẩn', [
           '- Nguyên văn lỗi đầu tiên hệ thống trả, vd “Vui lòng nhập diễn giải trước khi gửi duyệt”',
           '- “Tổng số tiền điều chỉnh đến phải bằng số tiền điều chỉnh từ (dòng n)”',
           '- Không rõ lỗi: “Cập nhật thất bại”'])],
   ev=[('Bấm Gửi duyệt', 'Click',
        'Before:\n– Kiểm tra cặp trạng thái: chỉ Đang tạo / Từ chối → Chờ tạo phiếu kế toán; sai → “Không thể chuyển phiếu từ '
        'trạng thái hiện tại sang trạng thái này”.\n'
        '– Kiểm tra người lập; nếu không → hiển thị “Bạn không có quyền gửi duyệt phiếu này” và dừng xử lý.\n'
        'During:\n– Diễn giải trống → “Vui lòng nhập diễn giải trước khi gửi duyệt”; NCC ngoại tệ, tỷ giá ≤ 0 → “Vui lòng nhập '
        'tỷ giá lớn hơn 0 trước khi gửi duyệt”.\n'
        '– Không có dòng → “Phiếu chưa có dòng điều chỉnh nào”; dòng n không có “đến” → “Dòng n chưa có dòng "Điều chỉnh đến" nào”.\n'
        '– KH “từ” trống → “Dòng n chưa chọn khách hàng điều chỉnh từ”; “đến” thiếu đối tượng / hợp đồng → “Dòng n có dòng '
        '"Điều chỉnh đến" chưa chọn khách hàng (nhà cung cấp / hợp đồng/đơn hàng / hợp đồng mua)”.\n'
        '– Số tiền ≤ 0 → “Dòng n có số tiền điều chỉnh từ (đến) chưa lớn hơn 0”; lệch tổng → “Tổng số tiền điều chỉnh đến '
        'phải bằng số tiền điều chỉnh từ (dòng n)”.\n' + ERR + '\n'
        'After:\n– Trạng thái Chờ tạo phiếu kế toán; Ngày nhận = thời điểm gửi; xóa lý do từ chối cũ.\n'
        '– Ghi một dòng lịch sử “Thay đổi trạng thái” (Đang tạo / Từ chối → Chờ tạo phiếu kế toán).\n'
        '– Gửi thông báo “[DCCN] Chờ duyệt: <mã phiếu>” cho Kế toán thanh toán cùng công ty.\n'
        '– Hiển thị “Gửi duyệt phiếu yêu cầu điều chỉnh công nợ thành công”, tải lại màn chi tiết (nút đổi theo trạng thái mới).')])

# ------------------------------------------------------------ 2.10
fr(10, 'Xóa phiếu', usecase=('FR-10', 'Xóa phiếu', 'action', A_LAP),
   rule=('- Quy tắc Xóa, Thông báo và Quy tắc ghi lịch sử.', 'delete'),
   intro=dict(
       ten='Xóa phiếu yêu cầu điều chỉnh công nợ',
       mota='Người lập xóa hẳn phiếu Đang tạo hoặc Từ chối cùng toàn bộ dòng “Điều chỉnh từ” và “Điều chỉnh đến”. Dữ liệu '
            'không khôi phục được; lịch sử vẫn giữ một dòng ghi nhận việc xóa kèm nội dung phiếu trước khi xóa.',
       tacnhan=TN_SUA, dieukien=DK_SUA,
       chinh='1. Người dùng bấm Xóa ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống hiện hộp “Xác nhận xóa” kèm mã phiếu.\n3. Người dùng bấm Xóa.\n'
             '4. Hệ thống kiểm tra người lập và trạng thái phiếu.\n'
             '5. Hệ thống ghi nhận hành động “Xóa” trong lịch sử của phiếu (kèm nội dung phiếu).\n'
             '6. Hệ thống xóa các dòng chi tiết và phiếu.\n'
             '7. Hệ thống hiện “Xóa thành công”: ở danh sách thì nạp lại, ở màn chi tiết thì về danh sách.',
       phu='• Bấm Hủy / (x) / click ra ngoài → đóng hộp, phiếu giữ nguyên.\n'
           '• Không phải người lập hoặc phiếu vừa đổi trạng thái → “Bạn không có quyền xóa phiếu này”; ở danh sách thì nạp '
           'lại cho khớp hiện trạng.\n'
           '• Lỗi khác → “Xóa thất bại” (hoặc thông báo của hệ thống).\n' + SESSION,
       dacbiet='Mã phiếu đã dùng không được cấp lại cho phiếu mới.'),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp xác nhận xóa phiếu',
               note='Modal Xác nhận xóa được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Tiêu đề hộp', 'Label', 'Hiển thị', 'Xác nhận xóa', '–'),
       ('Nội dung xác nhận', 'Label', 'Hiển thị', '–', '“Bạn có chắc muốn xóa phiếu yêu cầu điều chỉnh công nợ \'<mã>\'?” — đúng mã của dòng đang thao tác.'),
       ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Màu đỏ; thực hiện xóa phiếu.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không xóa.'),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', 'Như nút Hủy.'),
       ('Toast kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn', [
           '- Thành công: “Xóa thành công”', '- Không đủ điều kiện: “Bạn không có quyền xóa phiếu này”',
           '- Lỗi khác: “Xóa thất bại”'])],
   ev=[('Bấm nút Xóa (dòng / chân màn chi tiết)', 'Click',
        'Before:\n– Nút chỉ hiện với người lập, phiếu Đang tạo / Từ chối.\nAfter:\n– Mở hộp Xác nhận xóa kèm mã phiếu.'),
       ('Bấm Xóa trong hộp xác nhận', 'Click',
        'Before:\n– Kiểm tra người dùng là người lập và phiếu còn Đang tạo / Từ chối.\n'
        '– Nếu không → hiển thị “Bạn không có quyền xóa phiếu này” và dừng xử lý; ở danh sách nạp lại.\n'
        'During:\n– Xóa trong một giao dịch: lỗi giữa chừng thì không xóa gì.\n' + ERR + '\n'
        'After:\n– Ghi một dòng lịch sử “Xóa” kèm nội dung phiếu và bảng chi tiết trước khi xóa.\n'
        '– Xóa toàn bộ dòng “đến”, dòng “từ” rồi xóa phiếu.\n'
        '– Hiển thị “Xóa thành công”; danh sách nạp lại, màn chi tiết về danh sách.'),
       ('Bấm Hủy / (x) / click ra ngoài', 'Click', 'Before:\n– Hộp đang mở.\nAfter:\n– Đóng hộp, không thay đổi dữ liệu.')])

# ------------------------------------------------------------ 2.11
fr(11, 'Xem chi tiết phiếu', usecase=('FR-11', 'Xem chi tiết phiếu', 'view', A_LAP),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết phiếu yêu cầu điều chỉnh công nợ',
       mota='Xem phiếu ở chế độ chỉ đọc với đúng bố cục màn Sửa (khối Thông tin chung + bảng Chi tiết), kèm khối Lịch sử '
            'thay đổi và các nút thao tác ở chân màn hiện theo vai trò và trạng thái phiếu.',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu nằm trong phạm vi xem: người lập, người đã xử lý, Super '
                'admin, V1–V4 theo cấp, hoặc Kế toán thanh toán cùng công ty với phiếu Chờ tạo phiếu kế toán.\n'
                '3. Phiếu Đang tạo chỉ người lập (và Super admin) xem được.',
       chinh='1. Người dùng bấm Mã phiếu trên danh sách (hoặc mở từ thông báo).\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở màn “Chi tiết phiếu yêu cầu điều chỉnh công nợ: <mã>”, mọi ô chỉ đọc.\n'
             '4. Hệ thống hiện các nút ở chân màn theo điều kiện từng nút.',
       phu='• Ngoài phạm vi → ' + NO_VIEW + '.\n'
           '• Phiếu Từ chối → hiện thêm ô Ghi chú không duyệt (lý do).\n'
           '• Phiếu tạo tay → không có ô Số phiếu báo có.\n'
           '• Không tải được → “Không tải được dữ liệu phiếu”.\n' + SESSION,
       dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn chi tiết phiếu Chờ tạo phiếu kế toán'),
   ui_kw=dict(required=False),
   ui=[('Tiêu đề màn', 'Label', 'Hiển thị', '–', 'Chi tiết phiếu yêu cầu điều chỉnh công nợ: <mã>', 'Tiêu đề trang và tab trình duyệt.'),
       ('Dòng người lập – ngày giờ', 'Label', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Góc phải khối Thông tin chung.'),
       ('Ô Loại phiếu', 'Label', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu', '–'),
       ('Ô Mã phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu', '–'),
       ('Ô Người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Người lập phiếu (không phải người đang xem).'),
       ('Ô Phòng ban', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Phòng ban của người lập.'),
       ('Ô Tiền tệ', 'Label', 'Read-only', '–', 'Ẩn', 'Chỉ phiếu NCC.'),
       ('Ô Tỷ giá', 'Label', 'Read-only', '> 0', 'Ẩn', 'Chỉ phiếu NCC.'),
       ('Ô Số phiếu báo có', 'Label', 'Read-only', '–', 'Ẩn', 'Chỉ khi phiếu tạo từ phiếu báo có.'),
       ('Ô Diễn giải', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
       ('Ô Ghi chú không duyệt', 'Textarea', 'Read-only', '–', 'Ẩn', 'Lý do từ chối, chỉ hiện khi có.'),
       ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Như màn Tạo nhưng không có ô nhập, nút thêm / xóa', '- Có dòng Số tiền còn lại từng nhóm và dòng Tổng cộng']),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', 'Bấm tiêu đề để mở; nội dung như mục 2.16.'),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Người lập, phiếu Đang tạo / Từ chối → mở màn Sửa (mục 2.8).'),
       ('Nút Gửi duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Người lập, phiếu Đang tạo / Từ chối (mục 2.9).'),
       ('Nút Tạo phiếu kế toán', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Kế toán thanh toán cùng công ty, phiếu Chờ tạo phiếu kế toán (mục 2.13).'),
       ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Màu đỏ; cùng điều kiện nút Tạo phiếu kế toán → mở cửa sổ Từ chối (mục 2.12).'),
       ('Nút In phiếu', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ xem trước bản in (mục 2.14).'),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Tải file Excel của phiếu (mục 2.15).'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Màu đỏ; người lập, phiếu Đang tạo / Từ chối (mục 2.10).'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.')],
   ev=[('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → hiển thị ' + NO_VIEW + ' và dừng xử lý.\n'
        'During:\n– Nạp phiếu, bảng chi tiết, số dư hiện tại của hợp đồng; nạp cờ được sửa / gửi duyệt / từ chối / tạo phiếu kế toán / xóa.\n'
        'After:\n– Hiển thị dữ liệu chỉ đọc; nút ở chân màn hiện theo cờ, nút không dùng được thì ẩn.'),
       ('Bấm Sửa', 'Click', 'Before:\n– Nút chỉ hiện với người lập, phiếu Đang tạo / Từ chối.\nAfter:\n– Mở màn Sửa của phiếu.'),
       ('Bấm Tạo phiếu kế toán', 'Click', 'Before:\n– Nút chỉ hiện với Kế toán thanh toán cùng công ty, phiếu Chờ tạo phiếu kế toán.\n'
        'After:\n– Mở màn Tạo phiếu kế toán với phiếu này chọn sẵn (mục 2.13).'),
       ('Bấm mở khối Lịch sử', 'Click', 'Before:\n– Khối đang thu gọn.\nAfter:\n– Mở khối, hiện các mốc mới nhất trên cùng.'),
       ('Bấm Quay lại', 'Click', 'Before:\n– Màn chỉ đọc, không có dữ liệu chưa lưu.\nAfter:\n– Về màn danh sách.')])

# ------------------------------------------------------------ 2.12
fr(12, 'Từ chối phiếu', usecase=('FR-12', 'Từ chối phiếu', 'action', A_KT),
   rule=('- Quy tắc đổi trạng thái, Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Từ chối phiếu yêu cầu điều chỉnh công nợ',
       mota='Kế toán thanh toán không chấp nhận một phiếu Chờ tạo phiếu kế toán, bắt buộc nhập lý do. Phiếu chuyển sang Từ '
            'chối và quay lại cho người lập sửa, gửi duyệt lại; người lập nhận thông báo kèm lý do.',
       tacnhan=TN_KT, dieukien=DK_KT,
       chinh='1. Người dùng mở màn chi tiết phiếu (từ danh sách chờ duyệt, hoặc nút Từ chối trên dòng), bấm Từ chối.\n'
             '2. Hệ thống mở cửa sổ “Từ chối phiếu yêu cầu điều chỉnh công nợ”, dòng phụ “Phiếu: <mã>”, ô lý do trống.\n'
             '3. Người dùng nhập Lý do từ chối, bấm Từ chối.\n'
             '4. Hệ thống kiểm tra quyền, trạng thái và lý do.\n'
             '5. Hệ thống chuyển phiếu sang Từ chối, lưu lý do, ghi người xử lý vào Người duyệt.\n'
             '6. Hệ thống ghi nhận hành động “Thay đổi trạng thái” kèm lý do trong lịch sử của phiếu.\n'
             '7. Hệ thống gửi thông báo cho người lập.\n'
             '8. Hệ thống hiện “Từ chối phiếu yêu cầu điều chỉnh công nợ thành công”, đóng cửa sổ, về màn danh sách.',
       phu='• Lý do trống (hoặc chỉ khoảng trắng) → báo đỏ dưới ô “Vui lòng nhập lý do từ chối”, cửa sổ không đóng.\n'
           '• Không phải Kế toán thanh toán cùng công ty → nút không hiện; gọi thẳng thì “Bạn không có quyền từ chối phiếu này”.\n'
           '• Phiếu vừa được kế toán khác xử lý → “Không thể chuyển phiếu từ trạng thái hiện tại sang trạng thái này”; cửa '
           'sổ giữ nguyên lý do vừa nhập.\n'
           '• Bấm Hủy / (x) / click ra ngoài → đóng cửa sổ, phiếu không đổi; mở lại thì ô lý do trống.',
       dacbiet='Màn này không có nút Duyệt: việc chấp nhận là bấm Tạo phiếu kế toán (mục 2.13). Nút Từ chối bị khóa trong '
               'lúc đang xử lý.'),
   layout=dict(menu=MENU_CD + ' => Xem chi tiết => Từ chối', shot=shot('15_reject'), shot_caption='Cửa sổ Từ chối phiếu',
               note='Modal Từ chối phiếu yêu cầu điều chỉnh công nợ được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Từ chối phiếu yêu cầu điều chỉnh công nợ', 'Dòng phụ “Phiếu: <mã phiếu>”.'),
       ('Ô Lý do từ chối', 'Textarea', 'Enable', '1–1000 ký tự', 'Có', 'Trống', [
           '- Gợi ý “Nhập lý do từ chối”; con trỏ đặt sẵn vào ô khi mở', '- Trống: “Vui lòng nhập lý do từ chối”',
           '- Lý do lưu vào phiếu, hiện ở ô Ghi chú không duyệt và trong lịch sử, thông báo']),
       ('Nút Từ chối', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', ['- Màu đỏ', '- Khóa trong lúc đang xử lý']),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không thay đổi phiếu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Hủy.'),
       ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Chữ đỏ, ô viền đỏ dưới ô Lý do từ chối.'),
       ('Toast kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
           '- Thành công: “Từ chối phiếu yêu cầu điều chỉnh công nợ thành công”',
           '- Lỗi: nguyên văn thông báo hệ thống, không rõ lỗi: “Cập nhật thất bại”'])],
   ev=[('Bấm Từ chối ở màn chi tiết', 'Click',
        'Before:\n– Nút chỉ hiện với Kế toán thanh toán cùng công ty, phiếu Chờ tạo phiếu kế toán.\n'
        'After:\n– Mở cửa sổ, ô lý do trống, xóa lỗi cũ, đặt con trỏ vào ô.'),
       ('Bấm Từ chối trong cửa sổ', 'Click',
        'Before:\n– Kiểm tra cặp trạng thái: chỉ Chờ tạo phiếu kế toán → Từ chối; sai → “Không thể chuyển phiếu từ trạng thái '
        'hiện tại sang trạng thái này”.\n'
        '– Kiểm tra quyền Kế toán thanh toán cùng công ty của phiếu; nếu không → hiển thị “Bạn không có quyền từ chối phiếu '
        'này” và dừng xử lý.\n'
        'During:\n– Lý do trống / chỉ khoảng trắng → “Vui lòng nhập lý do từ chối”, không gửi, cửa sổ không đóng.\n'
        '– Lý do quá 1000 ký tự → báo lỗi độ dài.\n' + ERR + '\n'
        'After:\n– Trạng thái Từ chối; lưu lý do; Người duyệt = người từ chối.\n'
        '– Ghi một dòng lịch sử “Thay đổi trạng thái” Chờ tạo phiếu kế toán → Từ chối, kèm lý do.\n'
        '– Gửi thông báo “[DCCN] Từ chối: <mã phiếu>” (kèm người từ chối, lý do) cho người lập.\n'
        '– Hiển thị “Từ chối phiếu yêu cầu điều chỉnh công nợ thành công”, đóng cửa sổ, về màn danh sách.'),
       ('Bấm Hủy / (x) / click ra ngoài', 'Click', 'Before:\n– Cửa sổ đang mở.\nAfter:\n– Đóng cửa sổ, không gửi; phiếu không đổi.')])

# ------------------------------------------------------------ 2.13
fr(13, 'Tạo phiếu kế toán', usecase=('FR-13', 'Tạo phiếu kế toán', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Tạo phiếu kế toán điều chỉnh công nợ từ phiếu yêu cầu',
       mota='Cách Kế toán thanh toán chấp nhận phiếu: mở màn Tạo phiếu kế toán điều chỉnh công nợ với phiếu yêu cầu điền '
            'sẵn đầu phiếu và các dòng định khoản. Trạng thái phiếu yêu cầu đổi theo phiếu kế toán (lưu, duyệt, xóa) và '
            'mỗi lần đổi đều ghi lịch sử.',
       tacnhan=TN_KT, dieukien=DK_KT,
       chinh='1. Người dùng bấm Tạo phiếu kế toán ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống mở màn “Tạo phiếu kế toán” với phiếu yêu cầu chọn sẵn, nạp đầu phiếu và các dòng.\n'
             '3. Kế toán kiểm tra, lưu phiếu kế toán (đặc tả ở SRS màn Phiếu kế toán điều chỉnh công nợ).\n'
             '4. Hệ thống chuyển phiếu yêu cầu sang Đã tạo phiếu kế toán và ghi nhận “Thay đổi trạng thái” trong lịch sử '
             'của phiếu yêu cầu (ghi chú “Phiếu kế toán <mã>”).\n'
             '5. Duyệt phiếu kế toán → phiếu yêu cầu sang Đã duyệt phiếu kế toán, ghi lịch sử tương tự.',
       phu='• Thoát màn phiếu kế toán không lưu → phiếu yêu cầu giữ Chờ tạo phiếu kế toán.\n'
           '• Xóa phiếu kế toán đã lập → phiếu yêu cầu trở về Chờ tạo phiếu kế toán (ghi lịch sử).\n'
           '• Không phải Kế toán thanh toán cùng công ty → nút không hiện.\n' + SESSION,
       dacbiet='Bấm nút chỉ điều hướng, chưa ghi dữ liệu nên không hỏi xác nhận.'),
   layout=dict(menu=MENU_CD + ' => Tạo phiếu kế toán', shot=shot('21_accounting_create'),
               shot_caption='Màn Tạo phiếu kế toán mở từ phiếu yêu cầu'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Tạo phiếu kế toán (dòng)', 'Icon Button', 'Enable / Ẩn', 'Ẩn', [
           '- Trong cột Hành động của danh sách', '- Kế toán thanh toán cùng công ty, phiếu Chờ tạo phiếu kế toán']),
       ('Nút Tạo phiếu kế toán (chi tiết)', 'Button', 'Enable / Ẩn', 'Ẩn', '- Ở chân màn chi tiết, cùng điều kiện'),
       ('Màn Tạo phiếu kế toán', 'Label', 'Hiển thị', 'Ẩn', [
           '- Mở sẵn phiếu yêu cầu đã chọn; đầu phiếu và dòng định khoản điền theo phiếu yêu cầu',
           '- Các ô, nút của màn này đặc tả ở SRS Phiếu kế toán điều chỉnh công nợ']),
       ('Cột Trạng thái (sau khi lập)', 'Table/Grid', 'Read-only', 'Theo dữ liệu', [
           '- Lưu phiếu kế toán: Đã tạo phiếu kế toán (nhãn xanh)', '- Duyệt phiếu kế toán: Đã duyệt phiếu kế toán (nhãn xanh)',
           '- Xóa phiếu kế toán: trở về Chờ tạo phiếu kế toán'])],
   ev=[('Bấm Tạo phiếu kế toán', 'Click',
        'Before:\n– Nút chỉ hiện với người có quyền Kế toán thanh toán cùng công ty của phiếu, phiếu Chờ tạo phiếu kế toán.\n'
        'After:\n– Mở màn Tạo phiếu kế toán kèm phiếu yêu cầu; chưa ghi dữ liệu, chưa đổi trạng thái.'),
       ('Lưu phiếu kế toán', 'System',
        'Before:\n– Phiếu kế toán gắn với phiếu yêu cầu này được lưu thành công ở màn Phiếu kế toán.\n'
        'During:\n– So trạng thái cũ và mới của phiếu yêu cầu; không đổi thì không ghi gì thêm.\n'
        'After:\n– Phiếu yêu cầu sang Đã tạo phiếu kế toán.\n'
        '– Ghi một dòng lịch sử “Thay đổi trạng thái” Chờ tạo phiếu kế toán → Đã tạo phiếu kế toán, ghi chú “Phiếu kế toán <mã>” '
        '(lưu lại nhiều lần mà trạng thái không đổi thì không ghi).'),
       ('Duyệt phiếu kế toán', 'System',
        'Before:\n– Phiếu kế toán gắn với phiếu yêu cầu được duyệt.\n'
        'During:\n– Đổi trạng thái phiếu yêu cầu ngay trong lượt duyệt phiếu kế toán.\n'
        'After:\n– Phiếu yêu cầu sang Đã duyệt phiếu kế toán; ghi lịch sử “Thay đổi trạng thái” kèm mã phiếu kế toán.'),
       ('Xóa phiếu kế toán', 'System',
        'Before:\n– Phiếu kế toán gắn với phiếu yêu cầu bị xóa.\n'
        'During:\n– Đổi trạng thái phiếu yêu cầu ngay trong lượt xóa phiếu kế toán.\n'
        'After:\n– Phiếu yêu cầu trở về Chờ tạo phiếu kế toán để kế toán lập lại; ghi lịch sử “Thay đổi trạng thái”.')])

# ------------------------------------------------------------ 2.14
fr(14, 'In phiếu', usecase=('FR-14', 'In phiếu', 'io', A_LAP),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In phiếu yêu cầu điều chỉnh công nợ',
       mota='Xem trước và in một phiếu ngay tại chỗ (không mở tab mới) theo mẫu khổ A4 ngang, gồm đầu trang công ty ghi '
            'trên phiếu, thông tin chung, bảng “Điều chỉnh từ” → “Điều chỉnh đến” và khối chữ ký.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm In phiếu trong menu ba chấm của dòng hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem phiếu.\n'
             '3. Hệ thống mở cửa sổ “Xem trước phiếu <mã>”, hiện “Đang tải dữ liệu in…” rồi hiện bản in.\n'
             '4. Người dùng bấm In.\n5. Hệ thống mở hộp thoại in của trình duyệt với đúng nội dung bản xem trước.',
       phu='• Ngoài phạm vi xem → ' + NO_VIEW + ' hiện trong cửa sổ.\n'
           '• Lỗi tải → “Không tải được dữ liệu in”; mẫu rỗng → “Không có dữ liệu để in”.\n'
           '• Bấm (x) / click ra ngoài → đóng cửa sổ.',
       dacbiet='Đầu bản in lấy logo / letterhead theo công ty ghi trên phiếu (không theo người đang đăng nhập). Phiếu NCC '
               'ngoại tệ in tới 14 cột nên dùng khổ ngang.'),
   layout=dict(menu=MENU + ' => In phiếu', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Xem trước phiếu <mã>', '–'),
       ('Nút In', 'Button', 'Enable / Disable', '–', 'Hiển thị', [
           '- Cạnh tiêu đề cửa sổ', '- Khóa cho tới khi bản in tải xong', '- Bấm → mở hộp thoại in']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
       ('Dòng Đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu in…” trong lúc nạp.'),
       ('Đầu trang công ty', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Letterhead của công ty ghi trên phiếu.'),
       ('Tiêu đề bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu', [
           '- “PHIẾU YÊU CẦU ĐIỀU CHỈNH CÔNG NỢ”', '- Dòng “Ngày dd Tháng mm Năm yyyy”']),
       ('Khối thông tin chung', 'Label', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mã phiếu, Mã phiếu báo có', '- Người tạo, Phòng ban', '- Diễn giải']),
       ('Bảng điều chỉnh', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- 2 khối cột “Điều chỉnh từ” | “Điều chỉnh đến”, dòng “từ” gộp theo nhóm',
           '- Cột tiền canh phải, không xuống dòng; ngoại tệ 2 số lẻ']),
       ('Khối chữ ký', 'Label', 'Read-only', '–', 'Theo dữ liệu', [
           '- Dòng ngày ký', '- BAN GIAM ĐỐC, KẾ TOÁN TRƯỞNG, NGƯỜI NỘP TIỀN, NGƯỜI LẬP PHIẾU, NGƯỜI NỘP TIỀN (giữ đúng mẫu ERP)',
           '- Khối giữ trọn trong 1 trang']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', [
           '- Chữ đỏ trong cửa sổ: thông báo của hệ thống hoặc “Không tải được dữ liệu in”', '- “Không có dữ liệu để in”'])],
   ev=[('Bấm In phiếu', 'Click',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → hiển thị ' + NO_VIEW + ' và dừng xử lý.\n'
        'During:\n– Dựng bản in theo mẫu khổ ngang, letterhead theo công ty của phiếu.\n'
        '– Lỗi tải → “Không tải được dữ liệu in”; mẫu rỗng → “Không có dữ liệu để in”.\n'
        'After:\n– Hiện bản xem trước trong cửa sổ; mở nút In.'),
       ('Bấm In', 'Click', 'Before:\n– Bản in đã tải xong (nút hết khóa).\n'
        'After:\n– Mở hộp thoại in của trình duyệt với đúng nội dung xem trước; không mở tab mới.'),
       ('Bấm (x) / click ra ngoài', 'Click', 'Before:\n– Cửa sổ đang mở.\nAfter:\n– Đóng cửa sổ, dọn khung in; danh sách / chi tiết giữ nguyên.')])

# ------------------------------------------------------------ 2.15
fr(15, 'Xuất Excel', usecase=('FR-15', 'Xuất Excel', 'io', A_LAP),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách / một phiếu ra Excel',
       mota='Hai kiểu xuất: (1) cả danh sách theo đúng bộ lọc và lối vào đang xem, tối đa 5.000 dòng, 12 cột cố định; '
            '(2) một phiếu, gồm thông tin chung và bảng chi tiết như bản in. File có letterhead công ty ở đầu.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Danh sách: người dùng bấm Xuất Excel trên thanh công cụ.\n'
             '2. Hệ thống lấy toàn bộ phiếu khớp bộ lọc + phạm vi quyền (không chỉ trang đang xem), tối đa 5.000 dòng.\n'
             '3. Hệ thống tải file “Danh-sach-yeu-cau-dieu-chinh-cong-no-<yyyy-mm-dd>.xlsx”.\n'
             '4. Một phiếu: người dùng bấm Xuất Excel trong menu ba chấm của dòng hoặc ở chân màn chi tiết.\n'
             '5. Hệ thống kiểm tra phạm vi xem, tải file “Yeu-cau-dieu-chinh-cong-no-<mã>.xlsx”.\n'
             '6. Hệ thống hiện “Xuất Excel thành công”.',
       phu='• Lỗi khi xuất danh sách → “Lỗi khi xuất Excel danh sách”; lỗi xuất một phiếu → “Lỗi khi xuất Excel”.\n'
           '• Phiếu ngoài phạm vi xem → ' + NO_VIEW + '.\n'
           '• Kết quả lọc rỗng → vẫn tải file có letterhead, tiêu đề và hàng tên cột.\n'
           '• Kết quả quá 5.000 dòng → file chỉ chứa 5.000 dòng đầu theo thứ tự đang sắp; cần lọc hẹp lại.',
       dacbiet='Màn chưa có cửa sổ chọn trường xuất: file danh sách luôn xuất đủ 12 cột theo thứ tự cố định, không theo '
               'Tùy chỉnh cột. Nút Xuất Excel danh sách bị khóa trong lúc đang xuất. Danh sách lấy letterhead theo công '
               'ty của người đang đăng nhập; file một phiếu lấy theo công ty ghi trên phiếu.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export_toolbar'), shot_caption='Nút Xuất Excel trên thanh công cụ'),
   ui_kw=dict(required=False),
   ui=[('Nút Xuất Excel (danh sách)', 'Button', 'Enable / Disable', '–', 'Hiển thị', [
           '- Rê chuột hiện “Xuất Excel danh sách theo bộ lọc hiện tại”', '- Trong lúc xuất: chữ “Đang xuất...”, nút khóa']),
       ('Mục Xuất Excel (một phiếu)', 'Button', 'Enable', '–', 'Hiển thị', 'Trong menu ba chấm của dòng và ở chân màn chi tiết.'),
       ('File danh sách – Tiêu đề', 'Label', 'Read-only', '–', 'Theo dữ liệu', [
           '- Letterhead công ty ở dòng 1', '- “DANH SÁCH PHIẾU YÊU CẦU ĐIỀU CHỈNH CÔNG NỢ”, in đậm, gộp ô, canh giữa']),
       ('File danh sách – Bảng', 'Table/Grid', 'Read-only', '≤ 5.000 dòng', 'Theo dữ liệu', [
           '- 12 cột: STT, Mã phiếu, Loại phiếu, Số phiếu báo có, KH / NCC, Số tiền, Ngày tạo, Người tạo',
           '- Phòng ban, Ngày nhận, Người duyệt, Trạng thái',
           '- Hàng tên cột in đậm; kẻ viền toàn bảng']),
       ('File danh sách – Cột Số tiền', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', [
           '- Ô số thật, định dạng #,##0 (cộng SUM được)', '- Tổng tiền phiếu theo VNĐ']),
       ('File một phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Letterhead công ty ghi trên phiếu', '- Thông tin chung + bảng “Điều chỉnh từ” → “Điều chỉnh đến” như bản in']),
       ('Toast kết quả', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', [
           '- Thành công: “Xuất Excel thành công”', '- Lỗi danh sách: “Lỗi khi xuất Excel danh sách”',
           '- Lỗi một phiếu: “Lỗi khi xuất Excel”'])],
   ev=[('Bấm Xuất Excel (danh sách)', 'Click',
        'Before:\n– Nút đang không khóa (không có lượt xuất nào đang chạy).\n'
        '– Phạm vi dữ liệu theo quyền xem và lối vào đang xem (chung / chờ duyệt).\n'
        'During:\n– Lấy toàn bộ phiếu khớp bộ lọc + sắp xếp đang áp, bỏ phân trang, tối đa 5.000 dòng.\n' + ERR + '\n'
        'After:\n– Tải file .xlsx 12 cột có letterhead; hiển thị “Xuất Excel thành công”; lỗi → “Lỗi khi xuất Excel danh sách”.'),
       ('Bấm Xuất Excel (một phiếu)', 'Click',
        'Before:\n– Kiểm tra phạm vi xem phiếu; ngoài phạm vi → hiển thị ' + NO_VIEW + ' và dừng xử lý.\n'
        'During:\n– Dựng file theo dữ liệu phiếu, letterhead theo công ty ghi trên phiếu.\n' + ERR + '\n'
        'After:\n– Tải file “Yeu-cau-dieu-chinh-cong-no-<mã>.xlsx”; hiển thị “Xuất Excel thành công”; lỗi → “Lỗi khi xuất Excel”.')])

# ------------------------------------------------------------ 2.16
fr(16, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của phiếu',
       mota='Hiển thị các mốc tác động lên phiếu, mới nhất trên cùng: Tạo mới, Thay đổi thông tin (giá trị cũ → mới, cả '
            'bảng chi tiết), Thay đổi trạng thái (gửi duyệt, từ chối kèm lý do, đổi theo phiếu kế toán) và Xóa.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm Lịch sử trong menu ba chấm của dòng, hoặc mở khối Lịch sử ở màn chi tiết.\n'
             '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <mã phiếu>”.\n'
             '3. Hệ thống hiển thị các mốc mới nhất trên cùng, mỗi mốc có loại hành động, người thực hiện, thời điểm và '
             'nội dung thay đổi.\n'
             '4. Người dùng bấm Bộ lọc để lọc theo loại hành động, người thực hiện, khoảng ngày.',
       phu='• Phiếu chưa có mốc nào → “Chưa có lịch sử thao tác nào.”.\n'
           '• Lọc không khớp → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Bấm Đóng / (x) / click ra ngoài → đóng cửa sổ.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Lịch sử thay đổi: <mã phiếu>', '–'),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở / đóng các ô lọc; vùng lọc ghim đầu khối khi cuộn.'),
       ('Ô Loại hành động', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', [
           '- Gợi ý “Chọn loại hành động”', '- Lựa chọn lấy theo các loại hành động đã có của phiếu (Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Xóa)']),
       ('Ô Người thực hiện', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', [
           '- Gợi ý “Chọn người thực hiện”', '- Dạng “Tên - Mã phòng - Mã NV”']),
       ('Ô Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Gợi ý “Từ ngày”.'),
       ('Ô Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Gợi ý “Đến ngày”; chọn giá trị là lọc ngay, không có nút Tìm kiếm.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: loại hành động, “Người thực hiện: …”, thời điểm',
           '- Thay đổi thông tin: loại phiếu, phiếu báo có, diễn giải, tiền tệ, tỷ giá, tổng tiền, bảng chi tiết “Trước” / “Sau”',
           '- Thay đổi trạng thái: trạng thái cũ → mới; từ chối kèm lý do; đổi theo phiếu kế toán kèm “Phiếu kế toán <mã>”']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', [
           '- Chưa có mốc: “Chưa có lịch sử thao tác nào.”', '- Lọc không khớp: “Không có lịch sử phù hợp bộ lọc.”']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Đóng.')],
   ev=[('Bấm Lịch sử', 'Click',
        'Before:\n– Mục luôn có trong menu ba chấm của dòng (phiếu đã nằm trong phạm vi xem).\n'
        'After:\n– Mở cửa sổ, nạp các mốc của phiếu, mới nhất trên cùng.'),
       ('Bấm Bộ lọc', 'Click', 'Before:\n– Cửa sổ đang mở.\nAfter:\n– Mở / đóng vùng ô lọc.'),
       ('Đổi ô lọc lịch sử', 'Change',
        'Before:\n– Danh sách người thực hiện, loại hành động lấy theo dữ liệu thật của phiếu.\n'
        'After:\n– Lọc ngay theo các ô đang có giá trị; không khớp → “Không có lịch sử phù hợp bộ lọc.”.'),
       ('Bấm Đóng / (x) / click ra ngoài', 'Click', 'Before:\n– Cửa sổ đang mở.\nAfter:\n– Đóng cửa sổ; danh sách giữ nguyên.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu yêu cầu điều chỉnh công nợ; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Cấu trúc 2 cấp', ['– Phiếu có ít nhất 1 dòng “Điều chỉnh từ”, mỗi dòng có ít nhất 1 dòng “Điều chỉnh đến” (bắt buộc khi gửi duyệt).',
                                  '– Số tiền mọi dòng > 0 khi gửi duyệt; lưu nháp chỉ bắt buộc Loại phiếu.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Gửi duyệt']),
    ('BR-02', 'Khớp tổng tiền', ['– Gửi duyệt: tổng “đến” của mỗi nhóm bằng số tiền “từ” (áp cho cả loại khách hàng).',
                                 '– Loại NCC tạo từ phiếu báo có: tổng “đến” không lớn hơn “từ”.',
                                 '– Chọn nhanh hợp đồng không cho tổng “đến” vượt số tiền “từ”.'],
     ['Lập phiếu', 'Chọn hợp đồng', 'Gửi duyệt']),
    ('BR-03', 'Không điều chỉnh vào chính mình', ['– Hợp đồng, hợp đồng mua, phiếu yêu cầu xuất hàng bên “đến” không trùng bên “từ”.',
                                                  '– Không gắn hợp đồng: khách hàng / NCC bên “đến” không trùng bên “từ”.',
                                                  '– Kiểm cả khi lưu nháp.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Gửi duyệt']),
    ('BR-04', 'Đối tượng và hợp đồng bắt buộc', ['– Gửi duyệt: đối tượng bên “đến” bắt buộc; loại KH bắt buộc cả khách hàng bên “từ”.',
                                                 '– Hợp đồng bên “đến” bắt buộc khi gửi duyệt; loại NCC miễn khi “đến” là KHÁCH KHÔNG RÕ.',
                                                 '– Chỉ chọn hợp đồng sau khi đã chọn đối tượng; đổi đối tượng thì xóa hợp đồng cũ của dòng.'],
     ['Lập phiếu', 'Chọn khách hàng / NCC', 'Chọn hợp đồng', 'Gửi duyệt']),
    ('BR-05', 'Loại phiếu và ngoại tệ', ['– Đổi loại phiếu giữ nguyên bảng chi tiết, chỉ đổi nhãn cột và tiền tệ / tỷ giá.',
                                         '– Loại phiếu khóa khi sửa và khi tạo từ phiếu báo có (theo loại thu của phiếu báo có).',
                                         '– Loại NCC có Tiền tệ, Tỷ giá; VNĐ tỷ giá luôn 1; ngoại tệ tỷ giá > 0; tổng tiền phiếu lưu theo VNĐ.'],
     ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-06', 'Vòng đời trạng thái', ['– Lưu nháp → Đang tạo; Gửi duyệt → Chờ tạo phiếu kế toán.',
                                      '– Chỉ cho chuyển: Đang tạo / Từ chối → Chờ tạo phiếu kế toán; Chờ tạo phiếu kế toán → Từ chối.',
                                      '– Lưu phiếu kế toán → Đã tạo; duyệt → Đã duyệt phiếu kế toán; xóa phiếu kế toán → về Chờ tạo phiếu kế toán.',
                                      '– Sửa / Xóa / Gửi duyệt: người lập, phiếu Đang tạo hoặc Từ chối; Hủy chỉ hiển thị cho dữ liệu cũ.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Gửi duyệt', 'Xóa', 'Từ chối', 'Tạo phiếu kế toán']),
    ('BR-07', 'Kế toán thanh toán xử lý', ['– Từ chối / Tạo phiếu kế toán: người có quyền Kế toán thanh toán, cùng công ty ghi trên phiếu.',
                                           '– Màn chờ duyệt chỉ liệt kê phiếu Chờ tạo phiếu kế toán của người lập cùng công ty.',
                                           '– Từ chối bắt buộc lý do (tối đa 1000 ký tự); gửi lại thì lý do cũ bị xóa.'],
     ['Xem danh sách', 'Từ chối', 'Tạo phiếu kế toán']),
    ('BR-08', 'Mã phiếu', ['– <mã công ty>.DNDCCN<tháng năm>.NNNNN, sinh khi lưu lần đầu, chạy chung dãy với ERP.',
                           '– Mã đã dùng không cấp lại kể cả khi phiếu bị xóa.'], ['Lập phiếu', 'Xóa']),
    ('BR-09', 'Thông báo', ['– Gửi duyệt → mọi người có quyền Kế toán thanh toán cùng công ty: “[DCCN] Chờ duyệt: <mã>”.',
                            '– Từ chối → người lập: “[DCCN] Từ chối: <mã>” kèm người từ chối, lý do.',
                            '– Bấm thông báo mở màn chi tiết phiếu; lỗi gửi thông báo không làm hỏng thao tác chính.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Gửi duyệt', 'Từ chối']),
    ('BR-10', 'Thao tác xong quay về danh sách', ['– Lưu, Gửi duyệt ở form, Xóa ở màn chi tiết, Từ chối thành công đều quay về màn danh sách.',
                                                  '– Gửi duyệt ở màn chi tiết thì tải lại chính màn chi tiết.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Gửi duyệt', 'Xóa', 'Từ chối']),
    ('BR-11', 'Phạm vi xem phiếu', ['– Xét quyền xem V1 → V4 từ trên xuống, có cấp nào áp cấp đó; không có thì chỉ phiếu mình lập.',
                                    '– Phiếu Đang tạo chỉ người lập thấy (kể cả với V1); người đã xử lý phiếu và Super admin luôn xem được chi tiết.',
                                    '– In, Xuất Excel, Lịch sử dùng cùng phạm vi xem.'],
     ['Xem danh sách', 'Tìm kiếm và lọc', 'Xem chi tiết', 'In phiếu', 'Xuất Excel']),
    ('BR-12', 'Phiếu tạo từ phiếu báo có', ['– Dòng “từ” lấy theo các dòng phiếu báo có đã tích, bị khóa (không thêm / xóa nhóm, không sửa tiền).',
                                            '– NCC chưa rõ điền KHÁCH KHÔNG RÕ; tiền tệ, tỷ giá theo phiếu báo có.'],
     ['Lập phiếu']),
    ('BR-13', 'Giới hạn xuất danh sách', ['– Xuất toàn bộ kết quả lọc (không chỉ trang đang xem), tối đa 5.000 dòng.',
                                          '– Kết quả rỗng vẫn xuất file có letterhead và tên cột.'], ['Xuất Excel']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc dữ liệu do màn Phiếu yêu cầu điều chỉnh công nợ ghi ra.')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kế toán công nợ', 'Phiếu kế toán điều chỉnh công nợ — lập từ phiếu yêu cầu Chờ tạo phiếu kế toán, cập nhật trạng thái '
     'phiếu yêu cầu', 'Phân hệ Tài chính => Sổ tổng hợp => Phiếu kế toán'),
], widths=[0.45, 1.0, 2.6, 2.4])

d.save()
print('Đã ghi', OUT)

# -*- coding: utf-8 -*-
"""SRS màn "Phiếu yêu cầu điều chỉnh công nợ" (mã {cty}.DNDCCN{mmyy}.NNNNN) — form chuẩn Danh mục quốc gia (30/10/2026).

Chạy: python gen_srs.py  → SRS - Phiếu yêu cầu điều chỉnh công nợ.docx
Khung: srs-documenter (SrsDoc) + checklist ../phieu-theo-form-quoc-gia/CHECKLIST.md. Khuôn thư mục: bank-account-catalog.
Nguồn đọc 30/10/2026 (nhánh develop, cả 2 repo):
  BE  Modules/Finance/{Entities/BillAdjustDeptRequest/*, Services/BillAdjustDeptRequest*Service.php,
      Http/Controllers/V1/BillAdjustDeptRequestController.php, Http/Requests/BillAdjustDeptRequest/*}
  FE  pages/finance/bill-adjust-dept-requests/**, components/subsystem-menu/{finance,sale-hub}.js
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
TN_MOI = 'Người dùng có quyền thực hiện chức năng: mọi người dùng đã đăng nhập (không cần quyền riêng).'
TN_XEM = ('Người dùng có quyền thực hiện chức năng: người lập phiếu; người duyệt phiếu; người có một trong các quyền '
          'Xem tất cả phiếu yêu cầu điều chỉnh của tổng công ty / của công ty / của phòng ban / của bộ phận.')
TN_SUA = 'Người dùng có quyền thực hiện chức năng: người lập phiếu (không cần quyền riêng).'
TN_KT = 'Người dùng có quyền thực hiện chức năng: Kế toán thanh toán (cùng công ty với người lập phiếu).'
DK_XEM = '1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Phiếu yêu cầu điều chỉnh công nợ.'
DK_SUA = ('1. Người dùng đăng nhập thành công.\n2. Người dùng là người lập phiếu.\n'
          '3. Phiếu đang ở trạng thái Đang tạo hoặc Từ chối.')
DK_KT = ('1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán thanh toán, cùng công ty với người lập.\n'
         '3. Phiếu đang ở trạng thái Chờ tạo phiếu kế toán.')

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


# Mô tả riêng cho hàng sau khi tách dòng gộp (srs_split_rows) — mỗi đối tượng 1 hàng.
UI_OVER = {
    'Người tạo': 'Người lập phiếu (tự điền).',
    'Phòng ban': 'Phòng ban của người lập (tự điền).',
    'Cột STT': 'Cột khóa, đánh số liên tục theo trang.',
    'Cột Mã phiếu': ['- Cột khóa', '- Bấm Mã phiếu → màn chi tiết (FR-11)'],
    'Cột Ngày tạo': 'Sắp xếp được.',
    'Cột Ngày cập nhật': ['- Thời điểm sửa phiếu gần nhất', '- Sắp xếp được'],
    'Cột Ngày nhận': ['- Thời điểm gửi duyệt', '- Sắp xếp được'],
    'Cột Người tạo': 'Người lập phiếu.',
    'Cột Người cập nhật': 'Người sửa phiếu gần nhất.',
    'Cột Phòng ban': 'Phòng ban của người lập lúc lập phiếu.',
    'Cột Người duyệt': 'Kế toán thanh toán đã xử lý phiếu.',
    'Công ty': {'scope': 'Danh sách công ty', 'desc': 'Chỉ hiện với V1.'},
    ('Công ty / Phòng ban / Bộ phận', 'Phòng ban'): {'scope': 'Danh sách phòng ban', 'desc': [
        '- Hiện theo cấp quyền xem', '- Chỉ còn phòng ban của Công ty đã chọn', '- Đổi Công ty thì bị xóa']},
    ('Công ty / Phòng ban / Bộ phận', 'Bộ phận'): {'scope': 'Danh sách bộ phận', 'desc': [
        '- Hiện theo cấp quyền xem', '- Chỉ còn bộ phận của Phòng ban đã chọn', '- Đổi Phòng ban thì bị xóa']},
    'Hợp đồng điều chỉnh từ': 'Mã hợp đồng trên dòng “Điều chỉnh từ” chứa chuỗi nhập.',
    'Hợp đồng điều chỉnh đến': 'Mã hợp đồng trên dòng “Điều chỉnh đến” chứa chuỗi nhập.',
    ('Người tạo / Người duyệt', 'Người tạo'): 'Người lập phiếu.',
    ('Người tạo / Người duyệt', 'Người duyệt'): 'Kế toán thanh toán đã xử lý phiếu.',
    ('Nút Xóa / Hủy', 'Nút Xóa'): 'Xác nhận xóa phiếu.',
    'Thông tin chung': 'Loại phiếu, Mã phiếu, Người tạo, Phòng ban, (Tiền tệ, Tỷ giá), Số phiếu báo có, Diễn giải — chỉ đọc.',
    'Bảng chi tiết': 'Bảng “Điều chỉnh từ” → “Điều chỉnh đến” gộp dòng như màn Tạo, chỉ đọc; dòng Tổng cộng.',
    ('Nút Sửa / Gửi duyệt / Xóa', 'Nút Sửa'): 'Mở màn Sửa; người lập, phiếu Đang tạo / Từ chối.',
    ('Nút Sửa / Gửi duyệt / Xóa', 'Nút Gửi duyệt'): 'Gửi Kế toán thanh toán (FR-09); người lập, phiếu Đang tạo / Từ chối.',
    ('Nút Sửa / Gửi duyệt / Xóa', 'Nút Xóa'): 'Mở hộp Xác nhận xóa; người lập, phiếu Đang tạo / Từ chối.',
    'Nút Tạo phiếu kế toán': 'Mở màn Tạo phiếu kế toán (FR-13); Kế toán thanh toán cùng công ty, phiếu Chờ tạo phiếu kế toán.',
    ('Nút Tạo phiếu kế toán / Từ chối', 'Nút Từ chối'): 'Mở cửa sổ Từ chối (FR-12); cùng điều kiện nút Tạo phiếu kế toán.',
    'Nút In phiếu': 'Mở cửa sổ xem trước bản in (FR-14).',
    'Nút Xuất Excel': 'Tải file Excel của phiếu (FR-15).',
    ('Nút Từ chối / Hủy', 'Nút Từ chối'): 'Xác nhận từ chối (màu đỏ).',
}
_TB = lambda n, desc: (n, 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', desc)  # noqa: E731
UI_EXPLICIT = {
    'Tên / Mã khách hàng, Mã số thuế, Số điện thoại': [
        _TB('Ô Tên hoặc mã khách hàng', 'Tìm theo tên hoặc mã khách hàng chứa chuỗi nhập.'),
        _TB('Ô Mã số thuế', 'Tìm theo mã số thuế chứa chuỗi nhập.'),
        _TB('Ô Số điện thoại', 'Tìm theo số điện thoại chứa chuỗi nhập.'),
    ],
}


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
    d.ui_table(split_ui_rows(ui, UI_OVER, UI_EXPLICIT), **(ui_kw or {}))
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

FORM_UI = [
    ('Người lập – Ngày lập', 'Label', 'Read-only', '–', '–', 'Người đăng nhập – thời điểm hiện tại', 'Góc phải khối Thông tin chung.'),
    ('Loại phiếu', 'Dropdown', 'Enable', 'Điều chỉnh công nợ khách hàng / nhà cung cấp', 'Có', 'Điều chỉnh công nợ khách hàng',
     ['- Đổi loại khi bảng đã có dòng → hỏi xác nhận, đồng ý thì xóa sạch bảng chi tiết',
      '- Loại nhà cung cấp hiện thêm Tiền tệ, Tỷ giá']),
    ('Mã phiếu', 'Textbox', 'Read-only', '–', '–', 'Hệ thống sinh khi lưu', 'Hiện ở màn Sửa / Chi tiết.'),
    ('Người tạo / Phòng ban', 'Textbox', 'Read-only', '–', '–', 'Theo người lập', '–'),
    ('Tiền tệ', 'Dropdown', 'Enable / Ẩn', 'Danh mục tiền tệ', 'Có (loại NCC)', 'VNĐ', 'Chỉ loại nhà cung cấp.'),
    ('Tỷ giá', 'Textbox', 'Enable / Ẩn', '> 0', 'Có khi tiền tệ khác VNĐ', 'Trống',
     ['- Gợi ý “Nhập tỷ giá”', '- Gửi duyệt thiếu: “Vui lòng nhập tỷ giá lớn hơn 0 trước khi gửi duyệt”']),
    ('Số phiếu báo có', 'Textbox', 'Read-only', '–', '–', 'Trống', 'Có giá trị khi phiếu được tạo từ phiếu báo có.'),
    ('Diễn giải', 'Textarea', 'Enable', '–', 'Có khi gửi duyệt', 'Trống',
     ['- Gợi ý “Nhập diễn giải”', '- Gửi duyệt thiếu: “Vui lòng nhập diễn giải trước khi gửi duyệt”']),
    ('Nút Thêm dòng (+)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thêm 1 nhóm “Điều chỉnh từ” vào bảng.'),
    ('Bên Điều chỉnh từ', 'Table/Grid', 'Enable', '–', 'Có', '“Chưa có dòng điều chỉnh nào.”', [
        '- Khách hàng / Nhà cung cấp (bắt buộc, bấm ô mở popup FR-06)',
        '- Hợp đồng/Đơn hàng (loại NCC: Hợp đồng mua; bấm ô mở popup FR-07, khóa khi chưa chọn khách hàng)',
        '- Số dư cuối kỳ (NCC: Số dư), NVKD (NCC: Nhân viên): tự điền',
        '- Số tiền (bắt buộc, > 0, gợi ý “Nhập số tiền”)', '- Nút Xóa nhóm điều chỉnh']),
    ('Bên Điều chỉnh đến', 'Table/Grid', 'Enable', '–', 'Có', '1 dòng', [
        '- Mỗi nhóm có 1 hoặc nhiều dòng; nút “Thêm dòng điều chỉnh” / “Xóa dòng điều chỉnh đến”',
        '- Khách hàng / NCC (bắt buộc), Hợp đồng/Đơn hàng (bắt buộc khi gửi duyệt; lỗi “Bắt buộc chọn hợp đồng/đơn hàng”)',
        '- Số tiền (bắt buộc, > 0)', '- Dòng “Số tiền còn lại” = Số tiền “từ” trừ tổng “đến” của nhóm']),
    ('Loại NCC ngoại tệ', 'Table/Grid', 'Enable / Ẩn', '–', '–', 'Ẩn', 'Thêm cột Số dư (VNĐ) và Số tiền (VNĐ) mỗi bên.'),
    ('Dòng Tổng cộng', 'Table/Grid', 'Read-only', '≥ 0', '–', '0', 'Tổng tiền bên “từ” và bên “đến”.'),
    ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu ở trạng thái Đang tạo.'),
    ('Nút Gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu ở trạng thái Chờ tạo phiếu kế toán.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn danh sách; hỏi xác nhận nếu có thay đổi chưa lưu.'),
]

SAVE_EV = [
    ('Đổi Loại phiếu', 'Change', 'Before:\n– Bảng chi tiết có dòng → hỏi xác nhận.\nAfter:\n– Xóa sạch bảng chi tiết, đổi tên cột theo loại.'),
    ('Bấm Lưu nháp / Gửi duyệt', 'Click',
     'Before:\n– Sửa: chỉ người lập, phiếu Đang tạo / Từ chối; sai → “Bạn không có quyền sửa phiếu này”.\n'
     'During:\n– Các ô thiếu được báo cùng một lượt dưới từng ô: Khách hàng / NCC, Số tiền (“Phải lớn hơn 0”).\n'
     '– Chỉ khi Gửi duyệt: Diễn giải bắt buộc; Tỷ giá > 0 (ngoại tệ); có ít nhất 1 dòng “từ”, mỗi dòng có ít nhất 1 dòng '
     '“đến”; hợp đồng bên “đến” bắt buộc (trừ NCC “đến” là KHÁCH KHÔNG RÕ).\n'
     '– Gửi duyệt: tổng “đến” phải bằng số tiền “từ” của từng nhóm (“Tổng số tiền điều chỉnh đến phải bằng số tiền điều '
     'chỉnh từ (dòng n)”); NCC tạo từ phiếu báo có: tổng “đến” không lớn hơn “từ”.\n'
     '– Không trùng: “Hợp đồng điều chuyển đến trùng với điều chuyển từ”, “Khách hàng điều chỉnh đến trùng với khách hàng '
     'điều chỉnh từ”, “Phiếu yêu cầu xuất hàng điều chuyển đến trùng với điều chuyển từ”, “Hợp đồng mua điều chuyển đến '
     'trùng với điều chuyển từ”, “Nhà cung cấp điều chỉnh đến trùng với nhà cung cấp điều chỉnh từ”.\n' + ERR + '\n'
     'After:\n– Lập mới: sinh mã <mã công ty>.DNDCCN<mmyy>.NNNNN; công ty, phòng ban, bộ phận theo người lập.\n'
     '– Ghi nhận trong lịch sử (Tạo mới / Thay đổi thông tin; gửi duyệt ghi Thay đổi trạng thái).\n'
     '– Gửi duyệt: báo Kế toán thanh toán; xóa lý do từ chối cũ.\n'
     '– Báo “Lưu phiếu yêu cầu điều chỉnh công nợ thành công” / “Gửi duyệt phiếu yêu cầu điều chỉnh công nợ thành công”, '
     'về màn danh sách.'),
    ('Bấm Quay lại / rời màn', 'Click', 'Before:\n– Có thay đổi chưa lưu → hỏi xác nhận rời trang.\nAfter:\n– Về màn danh sách.'),
]

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu yêu cầu điều chỉnh công nợ',
       mota='Hiển thị phiếu trong phạm vi quyền. Có 2 chế độ: danh sách chung và danh sách chờ duyệt của Kế toán thanh toán.',
       tacnhan=TN_XEM, dieukien='1. Người dùng đăng nhập thành công.',
       chinh='1. Người dùng vào một trong các lối vào ở mục Layout.\n'
             '2. Hệ thống xác định chế độ và áp phạm vi dữ liệu.\n3. Hệ thống hiển thị trang đầu, mới tạo xếp trên.',
       phu='• Chế độ chờ duyệt: không có quyền Kế toán thanh toán → danh sách rỗng; không có nút Tạo mới.\n'
           '• Phiếu Đang tạo của người khác không hiện.',
       dacbiet=None),
   layout=dict(entries=[
       (MENU, 'Hiển thị: tiêu đề “Phiếu yêu cầu điều chỉnh công nợ”; phiếu trong phạm vi quyền (Phần 2).'),
       (MENU_SALE, 'Hiển thị: giống lối vào trên (cùng màn, cùng phạm vi).'),
       (MENU_CD, 'Hiển thị: tiêu đề “Phiếu yêu cầu điều chỉnh công nợ chờ duyệt”; chỉ người có quyền Kế toán thanh toán; '
                 'phiếu Chờ tạo phiếu kế toán của người lập cùng công ty.')],
       shot=shot('01_list'), shot_caption='Màn danh sách Phiếu yêu cầu điều chỉnh công nợ'),
   ui_kw=dict(required=False),
   ui=[
       ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', 'Ẩn ở chế độ chờ duyệt.'),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', 'Xuất danh sách theo bộ lọc (FR-15).'),
       ('Nút Cấu hình cột hiển thị', 'Button', 'Enable', '–', 'Hiển thị', 'FR-04.'),
       ('Cột STT / Mã phiếu', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Cột khóa', '- Bấm Mã phiếu → màn chi tiết (FR-11)']),
       ('Cột Loại phiếu', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Điều chỉnh công nợ khách hàng / nhà cung cấp.'),
       ('Cột Số phiếu báo có', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '–'),
       ('Cột KH / NCC', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Khách hàng / nhà cung cấp của phiếu.'),
       ('Cột Số tiền', 'Table/Grid', 'Read-only', '≥ 0', 'Hiển thị', 'Định dạng 1,234,567; sắp xếp được.'),
       ('Cột Ngày tạo / Ngày cập nhật / Ngày nhận', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        ['- Sắp xếp được', '- Ngày nhận: thời điểm gửi duyệt']),
       ('Cột Người tạo / Người cập nhật / Phòng ban / Người duyệt', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '–'),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Đang tạo, Chờ tạo phiếu kế toán, Hủy, Từ chối: nhãn đỏ', '- Đã tạo / Đã duyệt phiếu kế toán: nhãn xanh']),
       ('Cột Hành động', 'Table/Grid', 'Read-only', '–', 'Hiển thị', [
           '- Sửa, Xóa: người lập, phiếu Đang tạo / Từ chối',
           '- Tạo phiếu kế toán, Từ chối: Kế toán thanh toán, phiếu Chờ tạo phiếu kế toán (Từ chối mở màn chi tiết)',
           '- Nút ba chấm: In phiếu, Xuất Excel, Lịch sử']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Dòng “Hiển thị a–b / N” và ô Số dòng/trang.'),
   ],
   ev=[
       ('Mở màn hình', 'System', 'Before:\n– Xác định chế độ (chung / chờ duyệt) theo lối vào.\nAfter:\n– Hiển thị trang 1, mới tạo xếp trên.'),
       ('Bấm Mã phiếu', 'Click', 'After:\n– Mở màn chi tiết.'),
       ('Bấm tiêu đề cột sắp xếp được', 'Click', 'After:\n– Sắp xếp lại, về trang 1.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(ten='Tìm kiếm và lọc danh sách phiếu', mota='Thu hẹp danh sách theo 12 tiêu chí.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Nhập mã phiếu vào ô tìm nhanh, bấm Tìm kiếm; hoặc bấm Tìm kiếm nâng cao.\n2. Chọn / nhập tiêu chí.\n'
                    '3. Hệ thống nạp lại danh sách.',
              phu='• Làm mới → xóa mọi tiêu chí.', dacbiet=None),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'), shot_caption='Khối Bộ lọc danh sách'),
   ui=[
       ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Gợi ý “Tìm theo mã phiếu...”.'),
       ('Công ty / Phòng ban / Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Theo quyền', 'Không', 'Trống', 'Hiện theo cấp quyền xem.'),
       ('Loại phiếu', 'Dropdown', 'Enable', 'Khách hàng / Nhà cung cấp', 'Không', 'Trống', '–'),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách trạng thái', 'Không', 'Trống', '–'),
       ('Số phiếu báo có', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
       ('Khách hàng / Nhà cung cấp', 'Dropdown', 'Enable', 'Gõ để tìm', 'Không', 'Trống', 'Tìm chung cả khách hàng và NCC.'),
       ('Hợp đồng điều chỉnh từ / đến', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Mã hợp đồng trên dòng “từ” / “đến”.'),
       ('Người tạo / Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', '–'),
       ('Số tiền', 'Textbox', 'Enable', 'Từ – đến, ≥ 0', 'Không', 'Trống', 'Khoảng tổng tiền phiếu.'),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Từ ngày → đến ngày.'),
   ],
   ev=[('Đổi ô lọc nâng cao', 'Change', 'After:\n– Về trang 1, nạp lại danh sách.'),
       ('Bấm Tìm kiếm', 'Click', 'After:\n– Áp ô tìm nhanh (mã phiếu).'),
       ('Bấm Làm mới', 'Click', 'After:\n– Xóa mọi tiêu chí, nạp lại.')])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị', mota='Bật / tắt, sắp thứ tự ô lọc; lưu theo người dùng.',
              tacnhan=TN_XEM, dieukien=DK_XEM, chinh='1. Bấm Cài đặt bộ lọc.\n2. Tích / bỏ tích, kéo đổi thứ tự.\n3. Bấm Lưu.',
              phu='• Khôi phục mặc định / Đóng.', dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Danh sách ô lọc', 'Table/Grid', 'Enable', '11 mục', '–', 'Theo cấu hình',
        'Công ty – Phòng ban – Bộ phận, Loại phiếu, Trạng thái, Số phiếu báo có, Khách hàng / Nhà cung cấp, Hợp đồng điều '
        'chỉnh từ, Hợp đồng điều chỉnh đến, Người tạo, Người duyệt, Số tiền, Ngày tạo.'),
       ('Nút Lưu / Khôi phục mặc định / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–')],
   ev=[('Kéo đổi vị trí', 'Drag', 'After:\n– Đổi thứ tự.'), ('Bấm Lưu', 'Click', 'After:\n– Lưu theo người dùng.')])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Tùy chỉnh cột của bảng danh sách', mota='Bật / tắt, kéo sắp xếp 15 cột; STT, Mã phiếu, Hành động khóa.',
              tacnhan=TN_XEM, dieukien=DK_XEM, chinh='1. Bấm Cấu hình cột hiển thị.\n2. Tích / bỏ tích, kéo đổi thứ tự.\n3. Bấm Lưu.',
              phu='• Đóng → bỏ thay đổi.', dacbiet=None),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Danh sách cột', 'Table/Grid', 'Enable', '15 cột', '–', 'Theo cấu hình',
        'STT, Mã phiếu, Loại phiếu, Số phiếu báo có, KH / NCC, Số tiền, Ngày tạo, Người tạo, Ngày cập nhật, Người cập nhật, '
        'Phòng ban, Ngày nhận, Người duyệt, Trạng thái, Hành động.'),
       ('Nút Chọn tất cả / Bỏ chọn hết / Lưu / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–')],
   ev=[('Kéo biểu tượng ba gạch', 'Drag', 'After:\n– Đổi thứ tự cột.'), ('Bấm Lưu', 'Click', 'After:\n– Lưu, vẽ lại bảng.')])

# ------------------------------------------------------------ 2.5
fr(5, 'Lập phiếu yêu cầu điều chỉnh công nợ', usecase=('FR-05', 'Lập phiếu', 'crud', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Lập phiếu yêu cầu điều chỉnh công nợ',
       mota='Chọn loại phiếu, nhập diễn giải, dựng bảng “Điều chỉnh từ” → “Điều chỉnh đến”; lưu nháp hoặc gửi duyệt.',
       tacnhan=TN_MOI, dieukien='1. Người dùng đăng nhập thành công.',
       chinh='1. Bấm Tạo mới.\n2. Hệ thống mở màn “Tạo phiếu yêu cầu điều chỉnh công nợ”.\n3. Chọn Loại phiếu, nhập Diễn giải.\n'
             '4. Bấm Thêm dòng; với dòng “từ” chọn khách hàng (FR-06), hợp đồng (FR-07), nhập Số tiền.\n'
             '5. Ở bên “đến” chọn khách hàng, hợp đồng, nhập Số tiền; thêm dòng “đến” nếu chia cho nhiều nơi.\n'
             '6. Bấm Lưu nháp hoặc Gửi duyệt.\n7. Hệ thống kiểm tra, sinh mã, lưu, ghi lịch sử; gửi duyệt thì báo Kế toán thanh toán.\n'
             '8. Hệ thống báo thành công, về màn danh sách.',
       phu='• Lỗi kiểm tra → báo đỏ tại từng ô cùng một lượt.\n• Lưu và tiếp tục → lưu nháp rồi mở form trống.\n'
           '• Tạo từ phiếu báo có → dòng “từ” điền sẵn theo các dòng phiếu báo có đã chọn và bị khóa.',
       dacbiet='Tổng tiền phiếu lưu theo VNĐ (ngoại tệ nhân tỷ giá).'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10c_filled'), shot_caption='Màn Tạo phiếu yêu cầu điều chỉnh công nợ đã nhập dữ liệu'),
   ui=FORM_UI + [('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Chỉ ở màn Tạo.')],
   ev=SAVE_EV)

# ------------------------------------------------------------ 2.6
fr(6, 'Chọn khách hàng / nhà cung cấp', usecase=('FR-06', 'Chọn khách hàng / NCC', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(ten='Chọn khách hàng / nhà cung cấp cho dòng điều chỉnh',
              mota='Cửa sổ tìm và chọn khách hàng (loại KH) hoặc nhà cung cấp (loại NCC) cho bên “từ” hoặc “đến”.',
              tacnhan=TN_MOI, dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo / Sửa, bảng đã có dòng.',
              chinh='1. Bấm ô Khách hàng (Nhà cung cấp).\n2. Hệ thống mở cửa sổ “Chọn khách hàng”.\n3. Tìm theo tên / mã, MST, SĐT; '
                    'bấm dòng cần chọn.\n4. Hệ thống điền ô, xóa hợp đồng cũ của dòng đó.',
              phu='• Bấm Đóng → không chọn.', dacbiet=None),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('11_customer'), shot_caption='Cửa sổ Chọn khách hàng',
               note='Modal Chọn khách hàng được mở ngay trên màn hình Tạo / Sửa phiếu theo đường dẫn ở trên.'),
   ui=[('Tên / Mã khách hàng, Mã số thuế, Số điện thoại', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Ô tìm kiếm.'),
       ('Bảng khách hàng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        'STT, Mã KH - Tên khách hàng, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP.'),
       ('Nút Tìm kiếm / Làm mới / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–')],
   ev=[('Bấm một dòng', 'Click', 'After:\n– Điền khách hàng vào dòng; tự tra Số dư, NVKD theo hợp đồng khi đã chọn hợp đồng.')])

# ------------------------------------------------------------ 2.7
fr(7, 'Chọn hợp đồng', usecase=('FR-07', 'Chọn hợp đồng', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(ten='Chọn đơn hàng/hợp đồng (hợp đồng mua với loại NCC)',
              mota='Cửa sổ liệt kê hợp đồng của khách hàng / NCC đã chọn kèm giá trị và số tiền còn nợ.',
              tacnhan=TN_MOI, dieukien='1. Người dùng đăng nhập thành công.\n2. Dòng đã chọn khách hàng / NCC.',
              chinh='1. Bấm ô Hợp đồng/Đơn hàng.\n2. Hệ thống mở cửa sổ “Chọn đơn hàng/hợp đồng <khách hàng>”.\n'
                    '3. Bấm dòng hợp đồng.\n4. Hệ thống điền hợp đồng, Số dư cuối kỳ, NVKD.',
              phu='• Chưa chọn khách hàng → ô bị khóa, gợi ý “Vui lòng chọn khách hàng trước”.\n'
                  '• Khách hàng không có hợp đồng → “Không có hợp đồng phù hợp.”.',
              dacbiet='Nguồn hợp đồng bán: hợp đồng trên HRM, hợp đồng bán ERP, hợp đồng bán đầu kỳ, hợp đồng dịch vụ BH-SC.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('12_contract'), shot_caption='Cửa sổ Chọn đơn hàng/hợp đồng',
               note='Modal Chọn đơn hàng/hợp đồng được mở ngay trên màn hình Tạo / Sửa phiếu theo đường dẫn ở trên.'),
   ui=[('Số đơn hàng/Hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Ô tìm kiếm.'),
       ('Bảng hợp đồng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        'STT, Số đơn hàng/Hợp đồng, Ngày lập, Giá trị hợp đồng, Số tiền còn nợ.'),
       ('Nút Tìm kiếm / Làm mới / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Phân trang', 'Pagination', 'Enable', '10 / 20 / 50 / 100', '–', 'Trang 1, 10 dòng', '–')],
   ev=[('Bấm một dòng', 'Click', 'After:\n– Điền hợp đồng, Số dư cuối kỳ, NVKD vào dòng; đóng cửa sổ.')])

# ------------------------------------------------------------ 2.8
fr(8, 'Chỉnh sửa phiếu', usecase=('FR-08', 'Chỉnh sửa phiếu', 'crud', A_LAP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(ten='Chỉnh sửa phiếu yêu cầu điều chỉnh công nợ', mota='Người lập sửa phiếu Đang tạo / Từ chối.',
              tacnhan=TN_SUA, dieukien=DK_SUA,
              chinh='1. Bấm Sửa ở cột Hành động hoặc màn chi tiết.\n2. Hệ thống mở màn “Sửa phiếu yêu cầu điều chỉnh công nợ: <mã>”.\n'
                    '3. Sửa thông tin (quy tắc như FR-05).\n4. Bấm Lưu nháp hoặc Gửi duyệt.\n'
                    '5. Hệ thống lưu, ghi Thay đổi thông tin trong lịch sử, về danh sách.',
              phu='• Phiếu Từ chối hiện ô Ghi chú không duyệt (lý do) chỉ đọc.', dacbiet=None),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('19_edit'), shot_caption='Màn Sửa phiếu yêu cầu điều chỉnh công nợ'),
   ui=FORM_UI + [('Ghi chú không duyệt', 'Textarea', 'Read-only', '–', '–', 'Ẩn', 'Lý do từ chối, hiện khi phiếu Từ chối.')],
   ev=SAVE_EV)

# ------------------------------------------------------------ 2.9
fr(9, 'Gửi duyệt phiếu', usecase=('FR-09', 'Gửi duyệt', 'action', A_LAP),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(ten='Gửi duyệt phiếu từ màn chi tiết', mota='Người lập gửi phiếu Đang tạo / Từ chối cho Kế toán thanh toán mà không mở form Sửa.',
              tacnhan=TN_SUA, dieukien=DK_SUA,
              chinh='1. Mở chi tiết phiếu, bấm Gửi duyệt.\n2. Hệ thống kiểm tra như khi Gửi duyệt ở form.\n'
                    '3. Phiếu sang Chờ tạo phiếu kế toán, ghi Ngày nhận, lịch sử, báo Kế toán thanh toán.\n'
                    '4. Hiện “Gửi duyệt phiếu yêu cầu điều chỉnh công nợ thành công”.',
              phu='• Thiếu dữ liệu → báo lỗi, phiếu giữ trạng thái cũ.', dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết => Gửi duyệt', shot=shot('19_edit'),
               shot_caption='Phiếu Đang tạo — nút Gửi duyệt ở chân màn'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Gửi duyệt', 'Button', 'Enable / Ẩn', 'Ẩn', 'Người lập, phiếu Đang tạo / Từ chối.')],
   ev=[('Bấm Gửi duyệt', 'Click',
        'Before:\n– Kiểm tra người lập và trạng thái; sai → “Bạn không có quyền gửi duyệt phiếu này”.\n'
        'During:\n– Kiểm tra như FR-05 (Diễn giải, Tỷ giá, dòng, hợp đồng “đến”, khớp tổng tiền).\n' + ERR + '\n'
        'After:\n– Chờ tạo phiếu kế toán; ghi Thay đổi trạng thái; báo Kế toán thanh toán.')])

# ------------------------------------------------------------ 2.10
fr(10, 'Xóa phiếu', usecase=('FR-10', 'Xóa phiếu', 'action', A_LAP),
   rule=('- Quy tắc Xóa và Thông báo.', 'delete'),
   intro=dict(ten='Xóa phiếu yêu cầu điều chỉnh công nợ', mota='Người lập xóa phiếu Đang tạo / Từ chối.',
              tacnhan=TN_SUA, dieukien=DK_SUA,
              chinh='1. Bấm Xóa ở cột Hành động hoặc màn chi tiết.\n2. Hệ thống hiện hộp “Xác nhận xóa”.\n3. Bấm Xóa.\n'
                    '4. Hệ thống xóa phiếu, ghi lịch sử, báo “Xóa phiếu yêu cầu điều chỉnh công nợ thành công”.',
              phu='• Bấm Hủy → không xóa.\n• Không phải người lập → “Bạn không có quyền xóa phiếu này”.', dacbiet=None),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp xác nhận xóa phiếu',
               note='Modal Xác nhận xóa được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nội dung', 'Label', 'Hiển thị', '–', '“Bạn có chắc muốn xóa phiếu yêu cầu điều chỉnh công nợ \'<mã>\'?”'),
       ('Nút Xóa / Hủy', 'Button', 'Enable', 'Hiển thị', 'Xác nhận / đóng hộp.')],
   ev=[('Bấm Xóa', 'Click', 'Before:\n– Kiểm tra người lập và trạng thái.\n' + ERR + '\nAfter:\n– Xóa phiếu và các dòng; báo thành công.')])

# ------------------------------------------------------------ 2.11
fr(11, 'Xem chi tiết phiếu', usecase=('FR-11', 'Xem chi tiết phiếu', 'view', A_LAP),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(ten='Xem chi tiết phiếu yêu cầu điều chỉnh công nợ', mota='Xem phiếu ở chế độ chỉ đọc, kèm nút theo quyền.',
              tacnhan=TN_XEM, dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu trong phạm vi xem.',
              chinh='1. Bấm Mã phiếu.\n2. Hệ thống mở màn “Chi tiết phiếu yêu cầu điều chỉnh công nợ: <mã>”.',
              phu='• Ngoài phạm vi → “Bạn không có quyền xem phiếu này”.', dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn chi tiết phiếu Chờ tạo phiếu kế toán'),
   ui_kw=dict(required=False),
   ui=[('Thông tin chung / Bảng chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Như màn Tạo, mọi ô chỉ đọc.'),
       ('Ghi chú không duyệt', 'Textarea', 'Read-only', '–', 'Ẩn', 'Hiện khi phiếu Từ chối.'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', 'Xem lịch sử (FR-16).'),
       ('Nút Sửa / Gửi duyệt / Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Người lập, phiếu Đang tạo / Từ chối.'),
       ('Nút Tạo phiếu kế toán / Từ chối', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Kế toán thanh toán cùng công ty, phiếu Chờ tạo phiếu kế toán.'),
       ('Nút In phiếu / Xuất Excel / Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '–')],
   ev=[('Mở màn chi tiết', 'System', 'Before:\n– Kiểm tra phạm vi xem.\nAfter:\n– Hiển thị dữ liệu và nút theo điều kiện.')])

# ------------------------------------------------------------ 2.12
fr(12, 'Từ chối phiếu', usecase=('FR-12', 'Từ chối phiếu', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(ten='Từ chối phiếu yêu cầu điều chỉnh công nợ', mota='Kế toán thanh toán không duyệt, bắt buộc lý do.',
              tacnhan=TN_KT, dieukien=DK_KT,
              chinh='1. Mở chi tiết, bấm Từ chối (nút Từ chối trên dòng mở màn chi tiết).\n'
                    '2. Hệ thống mở cửa sổ “Từ chối phiếu yêu cầu điều chỉnh công nợ”.\n3. Nhập lý do, bấm Từ chối.\n'
                    '4. Phiếu sang Từ chối, lưu lý do, ghi lịch sử, báo người lập, về danh sách.',
              phu='• Lý do trống → “Vui lòng nhập lý do từ chối”.\n• Bấm Hủy → đóng cửa sổ.',
              dacbiet='Người lập sửa và gửi duyệt lại được.'),
   layout=dict(menu=MENU_CD + ' => Xem chi tiết => Từ chối', shot=shot('15_reject'), shot_caption='Cửa sổ Từ chối phiếu',
               note='Modal Từ chối phiếu yêu cầu điều chỉnh công nợ được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
   ui=[('Lý do từ chối', 'Textarea', 'Enable', '–', 'Có', 'Trống', ['- Gợi ý “Nhập lý do từ chối”', '- Lỗi: “Vui lòng nhập lý do từ chối”']),
       ('Nút Từ chối / Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', '–')],
   ev=[('Bấm Từ chối', 'Click',
        'Before:\n– Kiểm tra Kế toán thanh toán cùng công ty, phiếu Chờ tạo phiếu kế toán; sai → “Bạn không có quyền từ chối phiếu này”.\n'
        'During:\n– Lý do trống → báo lỗi.\n' + ERR + '\n'
        'After:\n– Phiếu Từ chối; ghi Thay đổi trạng thái kèm lý do; báo người lập; hiện “Từ chối phiếu yêu cầu điều chỉnh công nợ thành công”.')])

# ------------------------------------------------------------ 2.13
fr(13, 'Tạo phiếu kế toán', usecase=('FR-13', 'Tạo phiếu kế toán', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(ten='Tạo phiếu kế toán điều chỉnh công nợ từ phiếu yêu cầu',
              mota='Kế toán thanh toán mở màn Tạo phiếu kế toán với phiếu yêu cầu điền sẵn để ghi sổ.',
              tacnhan=TN_KT, dieukien=DK_KT,
              chinh='1. Bấm Tạo phiếu kế toán ở cột Hành động hoặc màn chi tiết.\n'
                    '2. Hệ thống mở màn “Tạo phiếu kế toán” điền sẵn phiếu yêu cầu và các dòng.\n'
                    '3. Kế toán lưu phiếu kế toán (đặc tả ở SRS màn Phiếu kế toán điều chỉnh công nợ).\n'
                    '4. Phiếu yêu cầu chuyển Đã tạo phiếu kế toán; duyệt phiếu kế toán thì sang Đã duyệt phiếu kế toán.',
              phu='• Thoát màn phiếu kế toán không lưu → phiếu yêu cầu giữ Chờ tạo phiếu kế toán.', dacbiet=None),
   layout=dict(menu=MENU_CD + ' => Tạo phiếu kế toán', shot=shot('21_accounting_create'),
               shot_caption='Màn Tạo phiếu kế toán mở từ phiếu yêu cầu'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Tạo phiếu kế toán', 'Button', 'Enable / Ẩn', 'Ẩn', 'Kế toán thanh toán cùng công ty, phiếu Chờ tạo phiếu kế toán.')],
   ev=[('Bấm Tạo phiếu kế toán', 'Click', 'After:\n– Mở màn Tạo phiếu kế toán với phiếu yêu cầu chọn sẵn (chưa ghi dữ liệu).')])

# ------------------------------------------------------------ 2.14
fr(14, 'In phiếu', usecase=('FR-14', 'In phiếu', 'io', A_LAP),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(ten='In phiếu yêu cầu điều chỉnh công nợ', mota='Xem trước và in phiếu.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Bấm In phiếu (menu ba chấm trên dòng hoặc màn chi tiết).\n2. Hệ thống mở cửa sổ xem trước.\n3. Bấm In.',
              phu='• Bấm Đóng (×) → đóng cửa sổ.', dacbiet='Đầu bản in lấy logo, tên công ty ghi trên phiếu.'),
   layout=dict(menu=MENU + ' => In phiếu', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[('Bản in', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
       '- Tiêu đề “PHIẾU YÊU CẦU ĐIỀU CHỈNH CÔNG NỢ”, ngày, mã phiếu, số phiếu báo có, người tạo, phòng ban, diễn giải',
       '- Bảng Điều chỉnh từ / Điều chỉnh đến gộp dòng', '- Chỗ ký: Ban giám đốc, Kế toán trưởng, Người nộp tiền, Người lập phiếu']),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Mở hộp thoại in.')],
   ev=[('Bấm In', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt.')])

# ------------------------------------------------------------ 2.15
fr(15, 'Xuất Excel', usecase=('FR-15', 'Xuất Excel', 'io', A_LAP),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Xuất danh sách / một phiếu ra Excel', mota='Xuất danh sách theo bộ lọc đang áp, hoặc xuất riêng một phiếu.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Danh sách: bấm Xuất Excel trên thanh công cụ → tải file theo bộ lọc đang áp.\n'
                    '2. Một phiếu: bấm Xuất Excel trong menu ba chấm của dòng hoặc ở màn chi tiết.\n3. Hệ thống báo “Xuất Excel thành công”.',
              phu='• Lỗi → “Lỗi khi xuất Excel danh sách” / “Lỗi khi xuất Excel”.',
              dacbiet='Màn chưa có cửa sổ chọn trường xuất: file danh sách xuất đủ các cột của bảng.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export_toolbar'), shot_caption='Nút Xuất Excel trên thanh công cụ'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Xuất Excel (danh sách)', 'Button', 'Enable / Disable', 'Hiển thị', 'Khóa trong lúc đang xuất.'),
       ('Mục Xuất Excel (một phiếu)', 'Button', 'Enable', 'Hiển thị', 'Trong menu ba chấm và ở màn chi tiết.')],
   ev=[('Bấm Xuất Excel', 'Click', 'During:\n– Lấy dữ liệu theo bộ lọc + phạm vi quyền.\n' + ERR + '\nAfter:\n– Tải file .xlsx.')])

# ------------------------------------------------------------ 2.16
fr(16, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(ten='Xem lịch sử thay đổi của phiếu', mota='Các mốc Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Xóa.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Bấm Lịch sử trong menu ba chấm, hoặc Xem lịch sử ở màn chi tiết.\n2. Hệ thống hiển thị các mốc, mới nhất trên.',
              phu='• Bộ lọc theo loại hành động, người thực hiện, khoảng ngày.', dacbiet=None),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
       '- Thay đổi thông tin: loại phiếu, phiếu báo có, diễn giải, tiền tệ, tỷ giá, tổng tiền, tóm tắt bảng chi tiết cũ → mới',
       '- Thay đổi trạng thái: trạng thái cũ → mới; từ chối kèm lý do']),
       ('Nút Bộ lọc / Đóng', 'Button', 'Enable', '–', 'Hiển thị', '–')],
   ev=[('Mở lịch sử', 'Click', 'Before:\n– Kiểm tra quyền xem.\nAfter:\n– Hiển thị các mốc.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu yêu cầu điều chỉnh công nợ; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Cấu trúc 2 cấp', ['– Phiếu có ít nhất 1 dòng “Điều chỉnh từ”, mỗi dòng có ít nhất 1 dòng “Điều chỉnh đến” (bắt buộc khi gửi duyệt).',
                                  '– Số tiền mọi dòng > 0.'], ['Lập phiếu', 'Chỉnh sửa', 'Gửi duyệt']),
    ('BR-02', 'Khớp tổng tiền', ['– Gửi duyệt: tổng “đến” của mỗi nhóm bằng số tiền “từ”.',
                                 '– Loại NCC tạo từ phiếu báo có: tổng “đến” không lớn hơn “từ”.'], ['Lập phiếu', 'Gửi duyệt']),
    ('BR-03', 'Không điều chỉnh vào chính mình', ['– Khách hàng / NCC, hợp đồng, phiếu yêu cầu xuất hàng bên “đến” không trùng bên “từ”.'],
     ['Lập phiếu', 'Gửi duyệt']),
    ('BR-04', 'Hợp đồng bên “đến”', ['– Bắt buộc khi gửi duyệt (nháp để trống được).', '– Loại NCC: miễn khi “đến” là KHÁCH KHÔNG RÕ.'],
     ['Lập phiếu', 'Gửi duyệt']),
    ('BR-05', 'Loại phiếu và ngoại tệ', ['– Đổi loại phiếu xóa sạch bảng chi tiết.',
                                         '– Loại NCC có Tiền tệ, Tỷ giá; tổng tiền phiếu lưu theo VNĐ.'], ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-06', 'Vòng đời trạng thái', ['– Lưu nháp → Đang tạo; Gửi duyệt → Chờ tạo phiếu kế toán.',
                                      '– Kế toán thanh toán từ chối → Từ chối; tạo phiếu kế toán → Đã tạo, rồi Đã duyệt phiếu kế toán.',
                                      '– Sửa / Xóa / Gửi duyệt: người lập, phiếu Đang tạo hoặc Từ chối; trạng thái Hủy chỉ hiển thị cho dữ liệu cũ.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Gửi duyệt', 'Từ chối', 'Tạo phiếu kế toán']),
    ('BR-07', 'Kế toán thanh toán xử lý', ['– Chỉ phiếu của người lập cùng công ty với kế toán.',
                                           '– Màn chờ duyệt chỉ liệt kê phiếu Chờ tạo phiếu kế toán.'], ['Xem danh sách', 'Từ chối', 'Tạo phiếu kế toán']),
    ('BR-08', 'Mã phiếu', ['– <mã công ty>.DNDCCN<tháng năm>.NNNNN, chạy chung dãy với ERP.'], ['Lập phiếu']),
    ('BR-09', 'Thông báo', ['– Gửi duyệt → Kế toán thanh toán; Từ chối → người lập kèm lý do.'], ['Gửi duyệt', 'Từ chối']),
    ('BR-10', 'Thao tác xong quay về danh sách', ['– Lưu, Gửi duyệt, Xóa, Từ chối thành công đều quay về màn danh sách.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Xóa', 'Từ chối']),
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

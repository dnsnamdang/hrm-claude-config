# -*- coding: utf-8 -*-
"""SRS màn "Phiếu yêu cầu hạch toán bổ sung" (mã PYCHTBS-NNNNNN) — form chuẩn Danh mục quốc gia (30/10/2026).

Chạy: python gen_srs.py  → SRS - Phiếu yêu cầu hạch toán bổ sung.docx
Khung: srs-documenter (SrsDoc) + checklist ../phieu-theo-form-quoc-gia/CHECKLIST.md. Khuôn thư mục: bank-account-catalog.
Nguồn đọc 30/10/2026 (nhánh develop, cả 2 repo):
  BE  Modules/Finance/{Entities/AdditionAccountingRequest/*, Services/AdditionAccountingRequest*Service.php,
      Http/Controllers/V1/AdditionAccountingRequestController.php, Http/Requests/AdditionAccountingRequest/*}
  FE  pages/finance/addition-accounting-requests/**, components/subsystem-menu/{finance,sale-hub}.js
  Spec docs/superpowers/specs/gop-db/2026-08-25-finance-addition-accounting-request-design.md (ưu tiên code khi lệch)
Ảnh: ./htbs_shots (dev-hrm 30/10/2026, DNS Admin, script htbs_shots/_capture/capture.js). Dev không có phiếu Đang tạo →
  ảnh Sửa / Xóa / Gửi duyệt chụp trên phiếu Chờ duyệt với cờ hiển thị bật tạm trên trình duyệt (không ghi dữ liệu).
31/10/2026: nâng độ chi tiết theo SRS_MAU (Đề nghị thu tiền) — đối chiếu lại code: index.vue, _id/index.vue, create/edit.vue,
  components/{AdditionAccountingRequestForm, AdditionDetailTable, AttachmentSection, RecordSearchModal, CustomerSearchModal,
  RejectModal, CoordinationDetail}.vue, bill-income-requests/components/{Supplier,Contract}SearchModal.vue, mixin unsaved*,
  saveAndContinue*, reportPrintPreviewMixin; BE StoreRequest/UpdateRequest/ChangeStatusRequest, WriteService (validate*,
  changeStatus), NotifyService, PrintService, BillAdjustDeptSourceService (đổi trạng thái khi lập / duyệt / xóa phiếu kế toán).
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

TEN = 'Phiếu yêu cầu hạch toán bổ sung'
SHOTS = os.path.join(HERE, 'htbs_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # sơ đồ Use Case; HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = ('Phân hệ Tài chính => Khởi tạo => Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi => '
        'Phiếu yêu cầu hạch toán bổ sung')
MENU_CD = ('Phân hệ Tài chính => Chờ duyệt => Phê duyệt - Công nợ - Thu - Chi => '
           'Phiếu yêu cầu hạch toán bổ sung chờ duyệt')
MENU_SALE = 'Phân hệ Bán hàng => Yêu cầu => Công nợ - Thu - Chi => YC hạch toán bổ sung'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Phiếu yêu cầu hạch toán bổ sung.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')

A_LAP = 'Người lập phiếu'
A_KT = 'Kế toán'
TN_MOI = ('Người dùng có quyền thực hiện chức năng: Người lập phiếu — chức năng không gắn quyền riêng, mọi nhân viên vào '
          'được màn danh sách đều lập được phiếu của mình.')
TN_XEM = ('Người dùng có quyền thực hiện chức năng: Người lập phiếu (phiếu của mình); người có một trong các quyền Xem '
          'phiếu yêu cầu hạch toán bổ sung - tổng công ty, - công ty, - phòng ban, - bộ phận (theo phạm vi ở Phần 2); '
          'Kế toán thanh toán; Kế toán.')
TN_SUA = 'Người dùng có quyền thực hiện chức năng: Người lập phiếu (chỉ chính người lập, không cần quyền riêng).'
TN_KT = ('Người dùng có quyền thực hiện chức năng: Kế toán thanh toán (mọi loại yêu cầu trừ Phối hợp kinh doanh); '
         'Kế toán thuộc công ty của phòng hỗ trợ (loại Phối hợp kinh doanh).')
DK_XEM = ('1. Người dùng đăng nhập thành công.\n'
          '2. Người dùng có quyền xem phiếu theo phạm vi ở Phần 2 (không có quyền nào thì chỉ thấy phiếu mình lập).\n'
          '3. Người dùng đang ở màn danh sách Phiếu yêu cầu hạch toán bổ sung.')
DK_SUA = ('1. Người dùng đăng nhập thành công.\n2. Người dùng là người lập phiếu.\n'
          '3. Phiếu đang ở trạng thái Đang tạo (mới lưu nháp, hoặc bị kế toán từ chối trả về).')
DK_KT = ('1. Người dùng đăng nhập thành công.\n'
         '2. Người dùng có quyền Kế toán thanh toán (phiếu thuộc công ty mình) hoặc quyền Kế toán thuộc công ty của phòng '
         'hỗ trợ (loại Phối hợp kinh doanh).\n3. Phiếu đang ở trạng thái Chờ duyệt.')

# Thông báo nguyên văn từ code (FE + BE).
M_REQ = '“Bắt buộc phải nhập”'
M_NOPERM_VIEW = '“Bạn không có quyền xem phiếu này”'
M_NOTFOUND = '“Không tìm thấy dữ liệu”'
TOAST_422 = '“Vui lòng kiểm tra lại dữ liệu nhập”'
DEL_MSG = "“Bạn có chắc muốn xóa phiếu yêu cầu hạch toán bổ sung '<số phiếu>'?”"
SEND_MSG = ('“Gửi duyệt phiếu yêu cầu hạch toán bổ sung "<số phiếu>"? Sau khi gửi, phiếu không sửa được nữa cho tới '
            'khi bị từ chối.”')
UNSAVED = ['- Tiêu đề “Thông tin chưa lưu”', '- Nội dung “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”',
           '- Nút Thoát: bỏ thay đổi, rời màn', '- Nút Ở lại: đóng hộp, giữ nguyên dữ liệu đang nhập']
TYPE_LIST = ['- Điều chỉnh công nợ khách hàng', '- Điều chỉnh công nợ nhà cung cấp', '- Hạch toán công nợ NCC bảo hành',
             '- Hạch toán công nợ NCC thiếu hàng', '- NCC hỗ trợ phát triển thị trường', '- Khác', '- Phối hợp kinh doanh']

d = SrsDoc(out=OUT, menu=MENU, route='/finance/addition-accounting-requests', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Khởi tạo': 'menu_khoitao',
    'Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi': 'menu_nhom_khoitao', 'Phiếu yêu cầu hạch toán bổ sung': 'menu_muc',
    'Chờ duyệt': 'menu_choduyet', 'Phê duyệt - Công nợ - Thu - Chi': 'menu_nhom_pheduyet',
    'Phiếu yêu cầu hạch toán bổ sung chờ duyệt': 'menu_muc_choduyet',
    'Phân hệ Bán hàng': 'menu_phanhe_banhang', 'Yêu cầu': 'menu_yeucau', 'Công nợ - Thu - Chi': 'menu_congno',
    'YC hạch toán bổ sung': 'menu_muc_sale',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Sửa': 'btn_sua_row', 'Xóa': 'btn_xoa_row', 'Gửi duyệt': 'btn_guiduyet_detail',
    'Từ chối': 'btn_tuchoi', 'Lập phiếu kế toán': 'btn_lappktoan', 'In phiếu': 'btn_in', 'Xuất Excel': 'btn_xuatexcel',
    'Lịch sử': 'item_lichsu',
}.items()})


# 31/10/2026: các bảng giao diện viết sẵn mỗi đối tượng 1 hàng (không còn dòng gộp "A / B") nên 2 bảng phụ của
# split_ui_rows để trống; vẫn gọi split_ui_rows trong fr() làm lưới chặn dòng gộp lọt vào.
UI_OVER = {}
UI_EXPLICIT = {}


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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu yêu cầu hạch toán bổ sung (mã phiếu PYCHTBS-NNNNNN), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng duyệt của màn hình.',
    'Làm rõ 7 loại yêu cầu và các trường riêng của từng loại.',
    'Làm rõ ai từ chối / lập phiếu kế toán theo từng loại (Kế toán thanh toán với mọi loại trừ Phối hợp kinh doanh, '
    'Kế toán của công ty phòng hỗ trợ với loại Phối hợp kinh doanh).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu yêu cầu hạch toán bổ sung', 'Phiếu đề nghị kế toán hạch toán bổ sung một khoản công nợ, mã PYCHTBS-NNNNNN '
                                        '(NNNNNN = số thứ tự phiếu, đủ 6 chữ số).'),
    ('Loại yêu cầu', 'Điều chỉnh công nợ khách hàng · Điều chỉnh công nợ nhà cung cấp · Hạch toán công nợ NCC bảo hành · '
                     'Hạch toán công nợ NCC thiếu hàng · NCC hỗ trợ phát triển thị trường · Khác · Phối hợp kinh doanh.'),
    ('Chi tiết hạch toán', 'Bảng dòng (Khách hàng / NCC, Hợp đồng, Số tiền, Ghi chú) của 2 loại Điều chỉnh công nợ; số tiền '
                           'phiếu = tổng các dòng.'),
    ('Phiếu xác nhận bảo hành / Phiếu xử lý hàng thiếu', 'Chứng từ nguồn của loại Hạch toán công nợ NCC bảo hành / thiếu hàng.'),
    ('Phiếu kế toán', 'Phiếu kế toán điều chỉnh công nợ do kế toán lập từ phiếu yêu cầu để ghi sổ.'),
    ('Đang tạo / Chờ duyệt / Đang duyệt / Đã duyệt', 'Các trạng thái của phiếu. Từ chối đưa phiếu về Đang tạo kèm Ghi chú duyệt.'),
    ('NCC', 'Nhà cung cấp.'),
], widths=[2.1, 3.9])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Lập phiếu không cần quyền riêng. Sửa / Xóa / Gửi duyệt: chỉ người lập, khi phiếu Đang tạo.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Kế toán thanh toán', 'Màn chờ duyệt; với phiếu Chờ duyệt trong phạm vi công ty: Từ chối; Lập phiếu kế toán '
                                 '(mọi loại trừ Phối hợp kinh doanh).'),
    ('Q2', 'Kế toán', 'Màn chờ duyệt; với phiếu Phối hợp kinh doanh Chờ duyệt có phòng hỗ trợ thuộc công ty mình: '
                      'Lập phiếu kế toán.'),
    ('Q3', 'Kế toán kho', 'Nhận thông báo khi có phiếu gửi duyệt (cùng công ty với phiếu).'),
], widths=[0.8, 1.6, 3.6])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (xét từ trên xuống, có cấp nào áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu yêu cầu hạch toán bổ sung - tổng công ty', 'Toàn bộ phiếu.'),
    ('V2', 'Xem phiếu yêu cầu hạch toán bổ sung - công ty',
     'Phiếu thuộc công ty mình; riêng loại Phối hợp kinh doanh: phiếu có phòng hỗ trợ thuộc công ty mình.'),
    ('V3', 'Xem phiếu yêu cầu hạch toán bổ sung - phòng ban', 'Phiếu phòng ban mình quản lý.'),
    ('V4', 'Xem phiếu yêu cầu hạch toán bổ sung - bộ phận', 'Phiếu bộ phận mình quản lý.'),
    ('—', '(không có quyền nào)', 'Phiếu mình lập.'),
], widths=[0.8, 2.4, 2.8])
d.p('Mọi cấp: phiếu Đang tạo của người khác bị ẩn.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người lập', 'Q1', 'Q2', 'V1–V4', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '✅ (+ chờ duyệt)', '✅ (+ chờ duyệt)', '✅ (theo cấp)', '✅ (phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Lập phiếu', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 Chọn đối tượng và chứng từ', '✅', '✅', '✅', '✅', '✅'),
    ('FR-07 Chỉnh sửa', '✅ (Đang tạo)', '❌', '❌', '❌', '❌'),
    ('FR-08 Gửi duyệt', '✅ (Đang tạo)', '❌', '❌', '❌', '❌'),
    ('FR-09 Xóa', '✅ (Đang tạo)', '❌', '❌', '❌', '❌'),
    ('FR-10 Xem chi tiết', '✅', '✅', '✅', '✅ (trong phạm vi)', '✅ (phiếu của mình)'),
    ('FR-11 Từ chối', '❌', '✅ (Chờ duyệt)', '❌', '❌', '❌'),
    ('FR-12 Lập phiếu kế toán', '❌', '✅ (trừ Phối hợp kinh doanh)', '✅ (Phối hợp kinh doanh)', '❌', '❌'),
    ('FR-13 In phiếu', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-14 Xuất Excel', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-15 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
], widths=[1.9, 0.9, 1.0, 0.9, 0.8, 0.9])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_LAP, [0, 1, 2, 3, 4, 7, 8]), (A_KT, [0, 5, 6, 7, 8])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Lập phiếu', 'crud'),
     ('FR-07', 'Chỉnh sửa phiếu', 'crud'),
     ('FR-08', 'Gửi duyệt', 'action'),
     ('FR-09', 'Xóa phiếu', 'action'),
     ('FR-11', 'Từ chối phiếu', 'action'),
     ('FR-12', 'Lập phiếu kế toán', 'action'),
     ('FR-13', 'In phiếu', 'io'),
     ('FR-14', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-10', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
     ('FR-15', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-06', 'Chọn đối tượng và chứng từ', 'crud', 'extend', [1, 2], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu yêu cầu hạch toán bổ sung')

d.h2('2 Đặc tả chi tiết từng chức năng')


# ------------------------------------------------------------ Form Tạo / Sửa (dùng chung 2.5 + 2.7)
def form_ui(edit):
    """Bảng giao diện màn Tạo (edit=False) / Sửa (edit=True) — 8 cột, mỗi đối tượng 1 hàng."""
    rows = [
        ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–',
         '“Sửa phiếu yêu cầu hạch toán bổ sung: <số phiếu>”' if edit else '“Tạo phiếu yêu cầu hạch toán bổ sung”',
         ['- Cũng là tiêu đề tab trình duyệt',
          '- Màn Sửa ghép số phiếu sau khi nạp xong phiếu' if edit else '- Không có ô Số phiếu: mã sinh khi lưu']),
        ('Dòng người lập', 'Label', 'Read-only', '–', '–',
         'Người lập – ngày giờ lập' if edit else 'Người đăng nhập – thời điểm hiện tại',
         ['- Góc phải tiêu đề khối Thông tin chung',
          '- Màn Sửa: người lập và ngày giờ lập của phiếu' if edit else '- Màn Tạo: người đang đăng nhập',
          '- Không sửa được']),
        ('Loại yêu cầu', 'Dropdown', 'Enable', 'Danh sách 7 giá trị', 'Có', 'Trống',
         ['- Mặc định: trống, gợi ý “Chọn loại yêu cầu”'] + TYPE_LIST + [
             '- Có nút × xóa nhanh', '- Đổi loại → xóa sạch trường phụ thuộc loại cũ, không hỏi xác nhận (BR-01)',
             '- Trống khi Lưu nháp hoặc Gửi duyệt → ' + M_REQ]),
        ('Phiếu xác nhận bảo hành', 'Textbox', 'Enable / Ẩn', '–', 'Có (loại Hạch toán công nợ NCC bảo hành)', 'Trống',
         ['- Chỉ hiện với loại Hạch toán công nợ NCC bảo hành', '- Gợi ý “Chọn phiếu xác nhận bảo hành...”',
          '- Bấm ô → mở cửa sổ Chọn phiếu xác nhận bảo hành (mục 2.6)',
          '- Chọn xong tự điền Nhà cung cấp và Số tiền theo phiếu',
          '- Nút × bỏ chọn: xóa luôn Nhà cung cấp, Số tiền về 0']),
        ('Phiếu xử lý hàng thiếu', 'Textbox', 'Enable / Ẩn', '–', 'Có (loại Hạch toán công nợ NCC thiếu hàng)', 'Trống',
         ['- Chỉ hiện với loại Hạch toán công nợ NCC thiếu hàng', '- Gợi ý “Chọn phiếu xử lý hàng thiếu...”',
          '- Bấm ô → mở cửa sổ Chọn phiếu xử lý hàng thiếu (mục 2.6)',
          '- Chọn xong tự điền Số tiền; phiếu có 1 nhà cung cấp thì tự điền Nhà cung cấp',
          '- Nút × bỏ chọn: xóa Số tiền về 0 và Nhà cung cấp']),
        ('Ô chọn Nhà cung cấp của phiếu xử lý hàng thiếu', 'Dropdown', 'Enable / Ẩn', 'Danh sách NCC của phiếu nguồn',
         'Có', 'Trống',
         ['- Chỉ hiện khi phiếu xử lý hàng thiếu đã chọn có từ 2 nhà cung cấp', '- Mặc định: trống, gợi ý “Chọn nhà cung cấp”',
          '- Lựa chọn: các nhà cung cấp của phiếu, dạng “Mã - Tên”']),
        ('Đối tượng', 'Dropdown', 'Enable / Ẩn', 'Danh sách 3 giá trị', 'Có (loại Khác)', 'Trống',
         ['- Chỉ hiện với loại Khác', '- Mặc định: trống, gợi ý “Chọn đối tượng”', '- Nhà cung cấp', '- Khách hàng',
          '- Nhân viên', '- Đổi giá trị → xóa đối tượng đã chọn ở ô bên cạnh']),
        ('Ô đối tượng đầu phiếu', 'Textbox', 'Enable / Disable', '–', 'Có (tự điền ở loại NCC bảo hành)', 'Trống',
         ['- Nhãn “Nhà cung cấp” với loại NCC bảo hành, NCC thiếu hàng, NCC hỗ trợ phát triển thị trường',
          '- Loại Khác: nhãn “Nhà cung cấp”, “Khách hàng” hoặc “Nhân viên” theo ô Đối tượng',
          '- Bấm ô → mở cửa sổ Chọn nhà cung cấp / Chọn khách hàng / Chọn nhân viên (mục 2.6); hiện “Mã - Tên”',
          '- Loại NCC bảo hành và NCC thiếu hàng (1 nhà cung cấp): tự điền theo chứng từ, khóa không bấm được',
          '- Ẩn với 2 loại Điều chỉnh công nợ và loại Phối hợp kinh doanh',
          '- Trống khi Gửi duyệt → ' + M_REQ]),
        ('Số tiền', 'Textbox', 'Enable / Ẩn', '> 0', 'Có', '0',
         ['- Gợi ý “Nhập số tiền”, nhập số', '- Loại NCC bảo hành, NCC thiếu hàng: tự điền theo chứng từ, vẫn sửa được',
          '- Ẩn với 2 loại Điều chỉnh công nợ (Số tiền phiếu = dòng Tổng cộng)',
          '- Trống → ' + M_REQ + '; nhập 0 hoặc âm → “Số tiền phải lớn hơn 0”']),
        ('Loại tiền', 'Dropdown', 'Enable', 'Danh mục loại tiền đang hoạt động', 'Có',
         'Theo phiếu' if edit else 'Loại tiền đầu danh mục (VNĐ)',
         ['- Mặc định màn Tạo: loại tiền đầu tiên của danh mục (VNĐ)',
          '- Loại tiền đã khóa mà phiếu đang dùng vẫn hiện, kèm biểu tượng 🔒',
          '- Đổi giá trị → tự điền Tỷ giá của loại tiền đó', '- Trống khi Gửi duyệt → ' + M_REQ]),
        ('Tỷ giá', 'Textbox', 'Enable', '> 0', 'Có', 'Theo loại tiền',
         ['- Gợi ý “Nhập tỷ giá”', '- Tự điền khi đổi Loại tiền, vẫn sửa được',
          '- Trống → ' + M_REQ + '; nhập 0 hoặc âm → “Tỷ giá phải lớn hơn 0”']),
        ('Diễn giải', 'Textarea', 'Enable / Ẩn', '–', 'Có', 'Trống',
         ['- Gợi ý “Nhập diễn giải”, 2 dòng', '- Ẩn với 2 loại Điều chỉnh công nợ (ghi chú nằm ở từng dòng chi tiết)',
          '- Trống khi Gửi duyệt → ' + M_REQ]),
        ('Ghi chú duyệt', 'Textarea', 'Read-only', '–', '–', 'Ẩn',
         ['- Chỉ hiện khi phiếu từng bị từ chối: lý do từ chối của kế toán',
          '- Gửi duyệt lại thì lý do cũ bị xóa']),
        ('Nút Thêm dòng', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
         ['- Ở tiêu đề khối Chi tiết hạch toán, chỉ có với 2 loại Điều chỉnh công nợ',
          '- Bấm → thêm 1 dòng trống (Số tiền 0) ở cuối bảng']),
        ('Bảng Chi tiết hạch toán', 'Table/Grid', 'Enable / Ẩn', '≥ 1 dòng khi Gửi duyệt', 'Có (2 loại Điều chỉnh công nợ)',
         '“Chưa có dòng chi tiết nào.”',
         ['- Chỉ hiện với loại Điều chỉnh công nợ khách hàng và Điều chỉnh công nợ nhà cung cấp',
          '- Tiêu đề cột dính khi cuộn; bảng cuộn dọc khi nhiều dòng',
          '- Gửi duyệt khi chưa có dòng → ' + M_REQ + ' ngay dưới bảng']),
        ('Cột STT của dòng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', 'Đánh số liên tục, tự đánh lại khi xóa dòng.'),
        ('Cột Đối tượng của dòng', 'Textbox', 'Enable', '–', 'Có', 'Trống',
         ['- Tiêu đề “Khách hàng” (Điều chỉnh công nợ khách hàng) hoặc “Nhà cung cấp” (Điều chỉnh công nợ nhà cung cấp)',
          '- Bấm ô → mở cửa sổ Chọn khách hàng hoặc Chọn nhà cung cấp (mục 2.6); hiện “Mã - Tên”',
          '- Đổi đối tượng → xóa hợp đồng đã chọn của dòng', '- Nút × bỏ chọn: xóa cả hợp đồng của dòng',
          '- Trống khi Gửi duyệt → ' + M_REQ]),
        ('Cột Hợp đồng của dòng', 'Textbox', 'Enable', '–', 'Có', 'Trống',
         ['- Tiêu đề “Hợp đồng bán” (khách hàng) hoặc “Hợp đồng mua” (nhà cung cấp)',
          '- Bấm ô khi dòng chưa có đối tượng → báo “Vui lòng chọn đối tượng trước”',
          '- Bấm ô khi đã có đối tượng → mở cửa sổ chọn hợp đồng của đúng đối tượng đó (mục 2.6)',
          '- Trống khi Gửi duyệt → ' + M_REQ,
          '- Trùng cặp đối tượng – hợp đồng với dòng trước → “Hợp đồng này đã có ở dòng <n> với cùng đối tượng”']),
        ('Cột Số tiền của dòng', 'Textbox', 'Enable', '> 0', 'Có', '0',
         ['- Gợi ý “Nhập số tiền”', '- Nhập → tính lại dòng Tổng cộng và Số tiền của phiếu',
          '- Trống → ' + M_REQ + '; 0 hoặc âm → “Số tiền phải lớn hơn 0”']),
        ('Cột Ghi chú của dòng', 'Textbox', 'Enable', '–', 'Có', 'Trống',
         ['- Gợi ý “Nhập ghi chú”', '- Trống khi Gửi duyệt → ' + M_REQ]),
        ('Nút Xóa dòng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
         ['- Biểu tượng thùng rác đỏ, chữ gợi ý “Xóa dòng”', '- Bấm → xóa dòng ngay, không hỏi xác nhận; tính lại tổng']),
        ('Dòng Tổng cộng', 'Label', 'Read-only', '≥ 0', '–', '0',
         ['- Tổng cột Số tiền của mọi dòng', '- Chỉ hiện khi bảng có ít nhất 1 dòng',
          '- Bằng Số tiền của phiếu khi lưu']),
        ('Nút Thêm tài liệu', 'Button', 'Enable', '–', '–', 'Hiển thị',
         ['- Ở tiêu đề khối File đính kèm',
          '- Chữ gợi ý “Chấp nhận pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip — tối đa 20MB/file”',
          '- Bấm → thêm 1 dòng có nút Chọn tệp']),
        ('Nút Chọn tệp', 'Button', 'Enable', '9 đuôi file, ≤ 20MB', '–', 'Hiển thị',
         ['- Chọn file từ máy → tải lên ngay, hiện “Đang tải lên <tên file>...”',
          '- Sai đuôi → “File "<tên file>" không thuộc định dạng cho phép”',
          '- Quá 20MB → “File "<tên file>" vượt quá 20MB”']),
        ('Bảng File đính kèm', 'Table/Grid', 'Enable', 'Nhiều file',
         'Có (≥ 1 file khi Gửi duyệt)' if not edit else 'Có (phiếu chưa có file thì ≥ 1 file khi Gửi duyệt)',
         'Theo phiếu' if edit else 'Chưa có file',
         ['- Cột STT, cột “Upload / File” (biểu tượng loại file + tên file), cột Dung lượng',
          '- Bấm tên file → mở cửa sổ xem trước file',
          '- Gửi duyệt khi chưa có file → ' + M_REQ + ' ngay dưới khối']),
        ('Nút Thay đổi file', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
         ['- Chữ gợi ý “Thay đổi”', '- Chọn file khác thay vào đúng vị trí',
          '- File đã lưu chỉ được thay thật khi bấm Lưu nháp / Gửi duyệt']),
        ('Nút Xóa file', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
         ['- Chữ gợi ý “Xóa”; khóa khi file đang tải lên', '- File chưa lưu: bỏ khỏi danh sách ngay',
          '- File đã lưu: hỏi “Bạn có chắc muốn xóa file đính kèm này?” (Xóa / Hủy); Xóa → xóa hẳn file, '
          'báo “Xóa file thành công”']),
        ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
         ['- Lưu phiếu ở trạng thái Đang tạo', '- Chỉ bắt buộc Loại yêu cầu (BR-02)', '- Khóa trong lúc đang lưu']),
        ('Nút Gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
         ['- Lưu phiếu ở trạng thái Chờ duyệt, không hỏi xác nhận', '- Kiểm tra đủ trường bắt buộc theo loại (BR-02)',
          '- Khóa trong lúc đang lưu']),
    ]
    if not edit:
        rows.append(('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
                     ['- Chỉ có ở màn Tạo; chữ gợi ý “Lưu nháp phiếu này rồi tiếp tục lập phiếu mới”',
                      '- Lưu nháp như nút Lưu nháp rồi mở lại form trống, ở lại màn Tạo']))
    rows += [
        ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
         ['- Về màn danh sách', '- Có thay đổi chưa lưu → hộp Thông tin chưa lưu']),
        ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         ['- Chữ đỏ ngay dưới ô, ô đổi viền đỏ',
          '- Lưu nháp chỉ báo ô Loại yêu cầu; Gửi duyệt báo mọi ô thiếu / sai',
          '- Tự cuộn tới ô lỗi đầu tiên']),
        ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         ['- Thành công: “Lưu thành công” (Lưu nháp) hoặc “Gửi duyệt thành công”',
          '- Thiếu / sai dữ liệu: ' + TOAST_422,
          '- Lỗi nghiệp vụ máy chủ trả: hiện nguyên văn câu đó' + (' (vd “Bạn không có quyền sửa phiếu này”)' if edit else ''),
          '- Lỗi khác: “Lưu thất bại”']),
        ('Hộp Thông tin chưa lưu', 'Popup', 'Hiển thị', '–', '–', 'Ẩn', UNSAVED),
    ]
    return rows


def save_ev(edit):
    """Bảng event màn Tạo / Sửa."""
    if edit:
        ev = [('Mở màn Sửa', 'System',
               'Before:\n– Kiểm tra người đăng nhập là người lập và phiếu đang ở trạng thái Đang tạo.\n'
               '– Phiếu không sửa được → hiển thị “Phiếu này không sửa được” và chuyển sang màn chi tiết phiếu.\n'
               'During:\n– Nạp danh mục Loại yêu cầu, Đối tượng, Loại tiền và dữ liệu phiếu (kể cả loại tiền đã khóa).\n'
               '– Mã phiếu không tồn tại → hiển thị ' + M_NOTFOUND + '; ngoài phạm vi xem → ' + M_NOPERM_VIEW +
               '; cả hai đều quay về màn danh sách.\n'
               'After:\n– Hiển thị form với dữ liệu phiếu; tiêu đề “Sửa phiếu yêu cầu hạch toán bổ sung: <số phiếu>”.\n'
               '– Chốt mốc “chưa đổi gì” để so khi rời màn.')]
    else:
        ev = [('Bấm nút Tạo mới', 'Click',
               'Before:\n– Chức năng không gắn quyền riêng; nút ẩn ở lối vào chờ duyệt.\n'
               'During:\n– Nạp danh mục Loại yêu cầu (7 loại), Đối tượng (3 giá trị), Loại tiền đang hoạt động và tên '
               'người đăng nhập.\n'
               'After:\n– Mở màn “Tạo phiếu yêu cầu hạch toán bổ sung”: Loại yêu cầu trống, Loại tiền = loại tiền đầu '
               'danh mục (VNĐ), Tỷ giá theo loại tiền đó, chưa có file đính kèm.')]
    ev += [
        ('Đổi Loại yêu cầu', 'Change',
         'Before:\n– Áp cả khi bấm × xóa nhanh ô Loại yêu cầu.\n'
         'During:\n– Xóa sạch trường phụ thuộc loại cũ: Phiếu xác nhận bảo hành, Phiếu xử lý hàng thiếu, Đối tượng, '
         'Nhà cung cấp, Khách hàng, Nhân viên, Số tiền (về 0), Diễn giải, bảng Chi tiết hạch toán; xóa lỗi máy chủ đang hiện.\n'
         '– Giữ nguyên Loại tiền, Tỷ giá, Ghi chú duyệt và file đính kèm.\n'
         'After:\n– Ẩn / hiện các trường theo loại mới (BR-01); không hỏi xác nhận.'),
        ('Đổi Đối tượng (loại Khác)', 'Change',
         'Before:\n– Chỉ có với loại Khác.\nDuring:\n– Xóa nhà cung cấp, khách hàng, nhân viên đã chọn.\n'
         'After:\n– Hiện ô đối tượng với nhãn Nhà cung cấp / Khách hàng / Nhân viên tương ứng.'),
        ('Đổi Loại tiền', 'Change',
         'Before:\n– Danh sách chỉ gồm loại tiền đang hoạt động (cộng loại tiền đã khóa phiếu đang dùng).\n'
         'During:\n– Lấy tỷ giá khai trong danh mục của loại tiền vừa chọn.\n'
         'After:\n– Điền Tỷ giá; người dùng vẫn sửa được.'),
        ('Bấm Thêm dòng', 'Click',
         'Before:\n– Chỉ có với 2 loại Điều chỉnh công nợ.\nDuring:\n– Thêm 1 dòng trống: đối tượng, hợp đồng, ghi '
         'chú trống, Số tiền 0.\nAfter:\n– Tính lại dòng Tổng cộng và Số tiền phiếu.'),
        ('Bấm Xóa dòng', 'Click',
         'Before:\n– Không hỏi xác nhận.\nDuring:\n– Bỏ dòng khỏi bảng, đánh số lại STT.\n'
         'After:\n– Tính lại dòng Tổng cộng và Số tiền phiếu; bảng hết dòng thì hiện “Chưa có dòng chi tiết nào.”.'),
        ('Nhập Số tiền của dòng', 'Change',
         'Before:\n– Chỉ nhận số.\nDuring:\n– Cộng lại cột Số tiền của mọi dòng.\n'
         'After:\n– Cập nhật dòng Tổng cộng và Số tiền của phiếu.'),
        ('Chọn tệp đính kèm', 'Change',
         'Before:\n– Chỉ nhận pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip; tối đa 20MB/file.\n'
         'During:\n– Sai đuôi → hiển thị “File "<tên file>" không thuộc định dạng cho phép”.\n'
         '– Quá dung lượng → hiển thị “File "<tên file>" vượt quá 20MB”.\n' + ERR + '\n'
         'After:\n– Tải file lên kho lưu trữ ngay, hiện tên file và dung lượng; file chỉ gắn vào phiếu khi bấm '
         'Lưu nháp / Gửi duyệt.'),
    ]
    if edit:
        ev.append(('Bấm Xóa file đã lưu', 'Click',
                   'Before:\n– Kiểm tra người lập, phiếu Đang tạo; sai → “Bạn không có quyền sửa phiếu này”.\n'
                   '– Hiển thị hộp “Xác nhận xóa” nội dung “Bạn có chắc muốn xóa file đính kèm này?”; bấm Hủy → dừng.\n'
                   'During:\n– File không thuộc phiếu → “File không thuộc phiếu này”.\n' + ERR + '\n'
                   'After:\n– Xóa file khỏi phiếu và khỏi kho lưu trữ (không cần bấm Lưu).\n'
                   '– Ghi một dòng lịch sử “Thay đổi thông tin” (file đính kèm đã xóa).\n'
                   '– Hiển thị “Xóa file thành công”.'))
    perm = ('Before:\n– Kiểm tra người đăng nhập là người lập, phiếu Đang tạo.\n'
            '– Không đủ điều kiện → hiển thị “Bạn không có quyền sửa phiếu này” và dừng xử lý.\n') if edit else \
           'Before:\n– Phiếu mới: không cần quyền riêng; khóa nút trong lúc đang lưu.\n'
    log_draft = ('– Ghi một dòng lịch sử “Thay đổi thông tin” chỉ với trường, dòng chi tiết, file đã đổi.\n' if edit else
                 '– Sinh mã PYCHTBS-NNNNNN; công ty, phòng ban, bộ phận theo người lập.\n'
                 '– Ghi một dòng lịch sử “Tạo mới” của phiếu.\n')
    log_send = ('– Ghi một dòng lịch sử “Thay đổi thông tin” (trường đã đổi) và một dòng “Thay đổi trạng thái” '
                'Đang tạo → Chờ duyệt; xóa Ghi chú duyệt cũ.\n' if edit else
                '– Sinh mã PYCHTBS-NNNNNN; công ty, phòng ban, bộ phận theo người lập.\n'
                '– Ghi một dòng lịch sử “Tạo mới” của phiếu.\n')
    ev += [
        ('Bấm Lưu nháp', 'Click', perm +
         'During:\n– Loại yêu cầu trống → hiển thị ' + M_REQ + ' dưới ô, không gửi lên máy chủ.\n'
         '– Các trường khác được để trống; Số tiền, Tỷ giá, số tiền dòng nếu nhập thì không được âm '
         '(“Không được nhỏ hơn 0.”).\n' + ERR + '\n'
         'After:\n– Lưu phiếu ở trạng thái Đang tạo.\n' + log_draft +
         '– Hiển thị “Lưu thành công” và quay về màn danh sách.'),
        ('Bấm Gửi duyệt', 'Click', perm + '– Không hỏi xác nhận trước khi gửi.\n'
         'During:\n– Loại tiền, Tỷ giá, Số tiền, Diễn giải trống → hiển thị ' + M_REQ + ' dưới từng ô.\n'
         '– Số tiền ≤ 0 → “Số tiền phải lớn hơn 0”; Tỷ giá ≤ 0 → “Tỷ giá phải lớn hơn 0”.\n'
         '– Thiếu chứng từ / đối tượng theo loại (Phiếu xác nhận bảo hành, Phiếu xử lý hàng thiếu, Nhà cung cấp, Đối tượng, '
         'Khách hàng, Nhân viên) → ' + M_REQ + '.\n'
         '– Loại Điều chỉnh công nợ: bảng chưa có dòng → ' + M_REQ + ' dưới bảng; dòng thiếu đối tượng / hợp đồng / ghi '
         'chú → ' + M_REQ + ' đúng ô; trùng cặp đối tượng – hợp đồng → “Hợp đồng này đã có ở dòng <n> với cùng đối tượng”.\n'
         '– Chưa có file đính kèm → ' + M_REQ + ' dưới khối File đính kèm.\n'
         '– Có lỗi → hiển thị ' + TOAST_422 + ', cuộn tới ô lỗi đầu tiên.\n' + ERR + '\n'
         'After:\n– Lưu phiếu ở trạng thái Chờ duyệt, ghi Ngày gửi.\n' + log_send +
         '– Gửi thông báo “[HTBS] Chờ duyệt: <số phiếu>” tới người có quyền Kế toán kho cùng công ty với phiếu, kèm '
         'loại yêu cầu, đối tượng, số tiền, người lập, ghi chú.\n'
         '– Hiển thị “Gửi duyệt thành công” và quay về màn danh sách.'),
    ]
    if not edit:
        ev.append(('Bấm Lưu và tiếp tục', 'Click',
                   'Before:\n– Chỉ có ở màn Tạo; khóa nút trong lúc đang lưu.\n'
                   'During:\n– Kiểm tra như Lưu nháp (chỉ bắt buộc Loại yêu cầu).\n' + ERR + '\n'
                   'After:\n– Lưu phiếu Đang tạo, ghi lịch sử “Tạo mới”, hiển thị “Lưu thành công”.\n'
                   '– Ở lại màn Tạo, mở lại form trống như lúc mới vào.'))
    ev.append(('Bấm Quay lại hoặc rời màn', 'Click',
               'Before:\n– So dữ liệu hiện tại với mốc lúc mở màn (bỏ qua số phiếu, ghi chú duyệt).\n'
               'During:\n– Có thay đổi chưa lưu → hiển thị hộp “Thông tin chưa lưu” nội dung “Bạn có thông tin chưa lưu. '
               'Có chắc chắn muốn thoát?”.\n'
               'After:\n– Bấm Thoát: bỏ thay đổi, rời màn; bấm Ở lại: giữ nguyên dữ liệu.\n'
               '– Không có thay đổi: về màn danh sách ngay.'))
    return ev


# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu yêu cầu hạch toán bổ sung',
       mota='Hiển thị bảng phiếu yêu cầu hạch toán bổ sung nằm trong phạm vi dữ liệu của người đăng nhập, kèm phân trang, '
            'sắp xếp và tổng số phiếu khớp bộ lọc. Màn có 2 chế độ theo lối vào: danh sách chung (mọi trạng thái trong '
            'phạm vi) và danh sách chờ duyệt (chỉ phiếu Chờ duyệt) dành cho kế toán.',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.\n'
                '2. Người dùng vào một trong các lối vào ở mục Layout (không cần quyền riêng để vào màn).',
       chinh='1. Người dùng vào một trong các lối vào ở mục Layout.\n'
             '2. Hệ thống xác định chế độ theo lối vào: danh sách chung hoặc chờ duyệt.\n'
             '3. Hệ thống xác định phạm vi xem theo thứ tự V1 → V2 → V3 → V4; không có cấp nào thì chỉ lấy phiếu do '
             'chính người đó lập.\n'
             '4. Hệ thống loại bỏ phiếu Đang tạo của người khác.\n'
             '5. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu có) và cấu hình cột của người dùng.\n'
             '6. Hệ thống trả về trang 1, phiếu lập gần nhất xếp trên, kèm tổng số phiếu; dòng “Hiển thị a–b / N” hiện '
             'đúng khoảng và tổng.',
       phu='• Chế độ chờ duyệt: chỉ phiếu Chờ duyệt; Kế toán thanh toán / Kế toán thấy phiếu thuộc công ty mình hoặc có '
           'phòng hỗ trợ thuộc công ty mình; người khác chỉ thấy phiếu Chờ duyệt của mình; không có nút Tạo mới.\n'
           '• Không có phiếu nào trong phạm vi → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng dựng thẳng theo cấu hình đó.\n'
           '• Mỗi chế độ nhớ bộ lọc riêng; đổi lối vào trên menu thì nạp lại theo bộ lọc của chế độ mới.\n'
           '• Máy chủ lỗi → hiển thị “Lỗi khi tải dữ liệu”.\n'
           '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
       dacbiet=None),
   layout=dict(entries=[
       (MENU, 'Hiển thị: tiêu đề “Phiếu yêu cầu hạch toán bổ sung”; phiếu trong phạm vi quyền (Phần 2).'),
       (MENU_SALE, 'Hiển thị: giống lối vào trên.'),
       (MENU_CD, 'Hiển thị: tiêu đề “Phiếu yêu cầu hạch toán bổ sung chờ duyệt”; phiếu Chờ duyệt — Kế toán thanh toán / Kế '
                 'toán thấy theo công ty hoặc phòng hỗ trợ, người khác chỉ thấy phiếu của mình.')],
       shot=shot('01_list'), shot_caption='Màn danh sách Phiếu yêu cầu hạch toán bổ sung'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '“Phiếu yêu cầu hạch toán bổ sung”',
        ['- Lối vào chờ duyệt: “Phiếu yêu cầu hạch toán bổ sung chờ duyệt”', '- Là tiêu đề bảng và tiêu đề tab trình duyệt']),
       ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Hiển thị',
        ['- Không gắn quyền riêng', '- Ẩn ở lối vào chờ duyệt',
         '- Bấm → mở màn Tạo phiếu yêu cầu hạch toán bổ sung (mục 2.5)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Chữ gợi ý “Xuất Excel danh sách theo bộ lọc hiện tại”',
         '- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.14)',
         '- Đang xuất: nhãn đổi thành “Đang xuất...” và khóa nút']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
        ['- Biểu tượng cột, chữ gợi ý “Cấu hình cột hiển thị”', '- Bấm → mở cửa sổ Tùy chỉnh cột (mục 2.4)']),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Số thứ tự liên tục giữa các trang', '- Ghim bên trái; khóa trong Tùy chỉnh cột']),
       ('Cột Số phiếu', 'Table/Grid', 'Read-only', 'PYCHTBS-NNNNNN', 'Theo dữ liệu',
        ['- Bấm số phiếu → mở màn chi tiết (mục 2.10); chuột phải mở được ở tab mới', '- Sắp xếp được',
         '- Ghim bên trái; khóa trong Tùy chỉnh cột']),
       ('Cột Loại yêu cầu', 'Table/Grid', 'Read-only', 'Danh sách 7 giá trị', 'Theo dữ liệu',
        ['- Tên loại yêu cầu của phiếu', '- Không sắp xếp']),
       ('Cột KH / NCC', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Đối tượng ở đầu phiếu dạng “Mã - Tên” (nhà cung cấp, khách hàng hoặc nhân viên)',
         '- 2 loại Điều chỉnh công nợ: đối tượng của dòng chi tiết đầu tiên', '- Tự xuống dòng khi dài']),
       ('Cột Số tiền', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
        ['- Số tiền nguyên tệ, dấu phẩy ngăn nghìn, căn phải', '- Kèm mã loại tiền phía sau', '- Sắp xếp được']),
       ('Cột Diễn giải', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Ghi chú của dòng chi tiết đầu tiên; không có thì lấy Diễn giải đầu phiếu', '- Tự xuống dòng khi dài']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Người lập phiếu, dạng “Tên nhân viên - Mã phòng”.'),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
        ['- Thời điểm lập phiếu', '- Sắp xếp được; mặc định phiếu mới xếp trên']),
       ('Cột Phòng ban', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Phòng ban hiện tại của người lập phiếu.'),
       ('Cột Ngày gửi', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
        ['- Thời điểm gửi duyệt gần nhất', '- Trống khi phiếu chưa gửi', '- Sắp xếp được']),
       ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Kế toán đã từ chối phiếu, hoặc đã duyệt phiếu kế toán lập từ phiếu này', '- Trống khi chưa có ai xử lý']),
       ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
        ['- Thời điểm kế toán từ chối / duyệt phiếu kế toán', '- Sắp xếp được']),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 4 giá trị', 'Theo dữ liệu',
        ['- Đang tạo: nhãn xám', '- Chờ duyệt: nhãn vàng', '- Đang duyệt: nhãn vàng', '- Đã duyệt: nhãn xanh',
         '- Không sắp xếp']),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Ẩn',
        ['- Thời điểm sửa phiếu gần nhất', '- Sắp xếp được', '- Ẩn mặc định; bật trong Tùy chỉnh cột']),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Ẩn',
        ['- Người sửa phiếu gần nhất, dạng “Tên nhân viên - Mã phòng”', '- Ẩn mặc định; bật trong Tùy chỉnh cột']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo quyền và trạng thái',
        ['- Nút Sửa: chỉ hiện với người lập, phiếu Đang tạo; bấm → màn Sửa (mục 2.7)',
         '- Nút Xóa (đỏ): cùng điều kiện; bấm → hộp Xác nhận xóa (mục 2.9)',
         '- Nút Lập phiếu kế toán: chỉ hiện với kế toán đủ điều kiện (mục 2.12)',
         '- Nút In phiếu: luôn hiện; bấm → cửa sổ xem trước bản in (mục 2.13)',
         '- Nút Xuất Excel: luôn hiện, tải file của phiếu (mục 2.14)', '- Nút Lịch sử: luôn hiện (mục 2.15)',
         '- Hiện tối đa 3 nút; dòng có hơn 3 nút thì 2 nút đầu hiện trực tiếp, các nút còn lại nằm trong nút “…”',
         '- Nút không dùng được thì ẩn hẳn, không hiện xám', '- Khóa trong Tùy chỉnh cột']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- a–b: khoảng số thứ tự của trang đang xem', '- N: tổng số phiếu khớp phạm vi và bộ lọc, không phải tổng toàn hệ thống']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5, 10, 20, 50, 100', '- Đổi giá trị → về trang 1, nạp lại']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
        ['- Nút về đầu, lùi, số trang, tiến, về cuối', '- Giữ nguyên bộ lọc và sắp xếp khi đổi trang']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', 'Hiện “Không có dữ liệu phù hợp bộ lọc.” khi N = 0.'),
       ('Thông báo lỗi tải dữ liệu', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- “Lỗi khi tải dữ liệu” khi máy chủ lỗi', '- Lỗi thiếu quyền không hiện thông báo này']),
   ],
   ev=[('Mở màn hình', 'System',
        'Before:\n– Xác định chế độ theo lối vào (danh sách chung hoặc chờ duyệt).\n'
        '– Xác định cấp quyền xem theo thứ tự V1 → V2 → V3 → V4; không có cấp nào thì giới hạn ở phiếu do chính người '
        'dùng lập.\n'
        'During:\n– Nạp cấu hình cột đã lưu trước, sau đó nạp dữ liệu.\n'
        '– Áp phạm vi dữ liệu; loại bỏ phiếu Đang tạo của người khác; chế độ chờ duyệt chỉ lấy phiếu Chờ duyệt.\n'
        '– Khôi phục bộ lọc của chế độ hiện tại đã lưu trong 10 phút gần nhất (nếu có).\n'
        'After:\n– Trả về trang 1, sắp xếp theo ngày tạo giảm dần, kèm tổng số phiếu.\n'
        '– Hiện / ẩn ô lọc Công ty, Phòng ban theo cấp quyền xem.'),
       ('Bấm số phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem (đã lọc ở bước nạp danh sách).\n'
        'During:\n– Chuột phải cho phép mở ở tab mới.\n'
        'After:\n– Mở màn chi tiết của phiếu tương ứng (mục 2.10).'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ 6 cột Số phiếu, Số tiền, Ngày tạo, Ngày gửi, Ngày duyệt, Ngày cập nhật sắp xếp được.\n'
        'During:\n– Đổi chiều sắp xếp tăng / giảm; giữ nguyên bộ lọc.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Bấm số trang hoặc nút tiến lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
        'During:\n– Nạp dữ liệu của trang được chọn.\n'
        'After:\n– Hiển thị trang mới, số thứ tự tiếp tục liên tục, dòng “Hiển thị a–b / N” cập nhật.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Chọn 1 trong 5, 10, 20, 50, 100.\n'
        'During:\n– Ghi nhận số dòng mới.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách theo số dòng mới.'),
       ('Bấm Tạo mới', 'Click',
        'Before:\n– Nút chỉ có ở danh sách chung, không gắn quyền.\n'
        'During:\n– Chuyển màn.\n'
        'After:\n– Mở màn Tạo phiếu yêu cầu hạch toán bổ sung (mục 2.5).')])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(ten='Tìm kiếm và lọc danh sách phiếu',
              mota='Thu hẹp danh sách phiếu theo số phiếu (ô tìm nhanh) và 9 tiêu chí của khối Tìm kiếm nâng cao: Công ty – '
                   'Phòng ban, Loại yêu cầu, Trạng thái, Khách hàng / Nhà cung cấp, Diễn giải, Phiếu xác nhận bảo hành, '
                   'Người tạo, Người duyệt, Ngày tạo. Kết quả luôn nằm trong phạm vi quyền xem của người dùng.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng nhập số phiếu vào ô tìm nhanh rồi bấm Tìm kiếm.\n'
                    '2. Hoặc bấm Tìm kiếm nâng cao để mở khối tiêu chí, chọn / nhập giá trị một hoặc nhiều tiêu chí.\n'
                    '3. Ô dạng chọn (Công ty, Phòng ban, Loại yêu cầu, Trạng thái, Khách hàng / Nhà cung cấp, Người tạo, '
                    'Người duyệt, Ngày tạo) lọc ngay khi đổi giá trị.\n'
                    '4. Ô gõ tay (số phiếu, Diễn giải, Phiếu xác nhận bảo hành) chỉ lọc khi bấm Tìm kiếm.\n'
                    '5. Hệ thống quay về trang 1, nạp lại danh sách và ghi nhớ bộ lọc trong 10 phút.',
              phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, nạp lại từ trang 1.\n'
                  '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”.\n'
                  '• Đổi Công ty → xóa giá trị Phòng ban đang chọn, danh sách phòng ban chỉ còn của công ty mới.\n'
                  '• Ô Khách hàng / Nhà cung cấp gõ dưới 2 ký tự → chưa gợi ý.\n'
                  '• Tiêu chí bị tắt trong Cài đặt bộ lọc → giá trị của tiêu chí đó bị xóa, không lọc ngầm.\n'
                  '• Bộ lọc của màn chờ duyệt nhớ riêng, không dùng chung với danh sách chung.',
              dacbiet=None),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'), shot_caption='Khối Bộ lọc danh sách'),
   ui=[('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số phiếu...”', '- Tìm theo một phần số phiếu', '- Chỉ lọc khi bấm nút Tìm kiếm']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
        'Áp giá trị ô tìm nhanh và các ô gõ tay, về trang 1, nạp lại.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa toàn bộ tiêu chí kể cả ô tìm nhanh, nạp lại từ trang 1.'),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Mở / thu gọn khối tiêu chí', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Trống',
        ['- Chỉ hiện với quyền V1', '- Mặc định: trống (tất cả), gợi ý “Chọn công ty”',
         '- Đổi giá trị → xóa Phòng ban đang chọn']),
       ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban', 'Không', 'Trống',
        ['- Hiện với quyền V1, V2, V3', '- Mặc định: trống (tất cả), gợi ý “Chọn phòng ban”',
         '- Chỉ liệt kê phòng ban của Công ty đang chọn']),
       ('Loại yêu cầu', 'Dropdown', 'Enable', 'Danh sách 7 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (tất cả)'] + TYPE_LIST),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (tất cả)', '- Đang tạo', '- Chờ duyệt', '- Đang duyệt', '- Đã duyệt']),
       ('Khách hàng / Nhà cung cấp', 'Dropdown', 'Enable', 'Gõ tối thiểu 2 ký tự', 'Không', 'Trống',
        ['- Gợi ý “Gõ mã hoặc tên khách hàng / nhà cung cấp”', '- Gợi ý dạng “Mã - Tên”, gồm cả khách hàng và nhà cung cấp',
         '- Khớp đối tượng đầu phiếu hoặc đối tượng của các dòng chi tiết']),
       ('Diễn giải', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Khớp Diễn giải đầu phiếu hoặc ghi chú các dòng chi tiết', '- Chỉ lọc khi bấm Tìm kiếm']),
       ('Phiếu xác nhận bảo hành', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập số phiếu xác nhận bảo hành”', '- Tìm theo một phần số phiếu', '- Chỉ lọc khi bấm Tìm kiếm']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống (tất cả)', '- Chọn nhân viên đã lập phiếu']),
       ('Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống (tất cả)', '- Chọn kế toán đã xử lý phiếu']),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- 1 ô gồm 2 lịch Từ ngày → Đến ngày', '- Lấy trọn cả 2 ngày biên']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện “Không có dữ liệu phù hợp bộ lọc.” khi không có kết quả.')],
   ev=[('Đổi giá trị ô dạng chọn', 'Change',
        'Before:\n– Áp cho Công ty, Phòng ban, Loại yêu cầu, Trạng thái, Khách hàng / Nhà cung cấp, Người tạo, Người '
        'duyệt, Ngày tạo.\n'
        'During:\n– Ghi nhận giá trị mới và ghi nhớ bộ lọc trong 10 phút.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí đang có.'),
       ('Bấm nút Tìm kiếm', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, Diễn giải, Phiếu xác nhận bảo hành đang nhập.\n'
        'During:\n– Gộp với các tiêu chí đang chọn.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Bấm nút Làm mới', 'Click',
        'Before:\n– Không hỏi xác nhận.\n'
        'During:\n– Đặt lại toàn bộ tiêu chí về trống, xóa đối tượng đã chọn ở ô Khách hàng / Nhà cung cấp.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Đổi Công ty', 'Change',
        'Before:\n– Chỉ có với quyền V1.\n'
        'During:\n– Xóa giá trị Phòng ban đang chọn.\n'
        'After:\n– Nạp danh sách phòng ban của công ty mới và nạp lại danh sách phiếu.'),
       ('Gõ ô Khách hàng / Nhà cung cấp', 'Change',
        'Before:\n– Chỉ gợi ý khi gõ từ 2 ký tự trở lên.\n'
        'During:\n– Tìm khách hàng và nhà cung cấp có mã hoặc tên chứa chuỗi gõ.\n'
        'After:\n– Hiển thị gợi ý dạng “Mã - Tên”; chọn 1 dòng thì lọc ngay.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối tiêu chí đang thu gọn.\n'
        'During:\n– Mở khối, nhãn nút đổi thành “Ẩn tìm kiếm nâng cao”.\n'
        'After:\n– Ghi nhớ trạng thái mở / thu gọn cùng bộ lọc.')])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị',
              mota='Cho phép mỗi người dùng tự chọn những tiêu chí lọc muốn thấy ở khối Tìm kiếm nâng cao và sắp xếp lại '
                   'thứ tự của chúng. Cấu hình lưu riêng theo người dùng cho màn Phiếu yêu cầu hạch toán bổ sung; 9 tiêu chí '
                   'là Công ty – Phòng ban, Loại yêu cầu, Trạng thái, Khách hàng / Nhà cung cấp, Diễn giải, Phiếu xác nhận '
                   'bảo hành, Người tạo, Người duyệt, Ngày tạo.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
                    '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 9 tiêu chí kèm ô tích, theo cấu hình đang lưu.\n'
                    '3. Người dùng tích / bỏ tích và kéo thả để đổi thứ tự.\n'
                    '4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình cho người dùng, hiển thị “Cập nhật thành công” và áp ngay lên khối Tìm kiếm '
                    'nâng cao.',
              phu='• Bấm Khôi phục mặc định → tích lại đủ 9 tiêu chí theo thứ tự gốc; phải bấm Lưu mới có hiệu lực.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không lưu thay đổi.\n'
                  '• Bỏ tích một tiêu chí đang có giá trị lọc → giá trị đó bị xóa sau khi lưu.\n'
                  '• Lưu thất bại → hiển thị “Thao tác thất bại”.',
              dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Cài đặt bộ lọc”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Danh sách tiêu chí', 'Table/Grid', 'Enable', 'Danh sách 9 tiêu chí', 'Không', 'Theo cấu hình đã lưu',
        ['- Công ty – Phòng ban', '- Loại yêu cầu', '- Trạng thái', '- Khách hàng / Nhà cung cấp', '- Diễn giải',
         '- Phiếu xác nhận bảo hành', '- Người tạo', '- Người duyệt', '- Ngày tạo']),
       ('Ô tích của tiêu chí', 'Checkbox', 'Enable', '–', 'Không', 'Theo cấu hình đã lưu',
        ['- Tích: tiêu chí hiện ở khối Tìm kiếm nâng cao', '- Bỏ tích: ẩn tiêu chí và xóa giá trị lọc của nó khi lưu']),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo để đổi thứ tự tiêu chí.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình cho người dùng hiện tại, đóng cửa sổ, áp ngay.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
        'Tích lại đủ 9 tiêu chí, thứ tự gốc; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ; thay đổi chưa lưu bị bỏ.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”'])],
   ev=[('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Nút hiện khi khối lọc có nhiều tiêu chí.\n'
        'During:\n– Nạp cấu hình đang lưu của người dùng.\n'
        'After:\n– Mở cửa sổ “Cài đặt bộ lọc”.'),
       ('Kéo đổi vị trí tiêu chí', 'Drag',
        'Before:\n– Kéo bằng tay nắm của dòng.\n'
        'During:\n– Đổi thứ tự trong cửa sổ.\n'
        'After:\n– Chưa áp lên màn hình cho tới khi bấm Lưu.'),
       ('Bỏ tích một tiêu chí', 'Change',
        'Before:\n– Áp cho mọi tiêu chí.\n'
        'During:\n– Ghi nhận trạng thái tích trong cửa sổ.\n'
        'After:\n– Chưa áp lên màn hình cho tới khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình gắn với người dùng đang đăng nhập.\n'
        'During:\n– Ghi cấu hình; lỗi → hiển thị “Thao tác thất bại”.\n'
        'After:\n– Hiển thị “Cập nhật thành công”; khối Tìm kiếm nâng cao cập nhật ngay.\n'
        '– Tiêu chí vừa bỏ tích: xóa giá trị đang lọc của tiêu chí đó, nạp lại danh sách.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\n'
        'During:\n– Tích lại toàn bộ 9 tiêu chí, đưa thứ tự về thiết kế gốc.\n'
        'After:\n– Chưa lưu; phải bấm Lưu mới có hiệu lực.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\n'
        'During:\n– Bỏ mọi thay đổi chưa lưu.\n'
        'After:\n– Đóng cửa sổ, khối lọc giữ nguyên.')])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Tùy chỉnh cột của bảng danh sách',
              mota='Cho phép mỗi người dùng bật / tắt và kéo sắp xếp 16 cột của bảng danh sách phiếu. Cấu hình lưu theo '
                   'người dùng và dùng chung cho cả danh sách chung lẫn danh sách chờ duyệt. Ba cột STT, Số phiếu, Hành động '
                   'bị khóa: luôn hiện, không đổi vị trí.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
                    '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 16 cột kèm ô tích theo cấu hình đang áp dụng.\n'
                    '3. Người dùng tích / bỏ tích, kéo biểu tượng ba gạch để đổi thứ tự.\n'
                    '4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình, hiển thị “Cập nhật thành công”, vẽ lại bảng.',
              phu='• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, danh sách cột trả về cấu hình đang áp dụng.\n'
                  '• Cột khóa: ô tích xám, không bỏ tích, không kéo được; di chuột hiện “Cột bắt buộc — không thể ẩn '
                  'hoặc đổi vị trí”.\n'
                  '• Lưu thất bại → hiển thị “Thao tác thất bại”.',
              dacbiet='Mặc định ẩn 2 cột Ngày cập nhật, Người cập nhật.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Tuỳ chỉnh cột”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Danh sách cột', 'Table/Grid', 'Enable', '16 cột', '–', 'Theo cấu hình',
        ['- STT, Số phiếu (khóa)', '- Loại yêu cầu, KH / NCC, Số tiền, Diễn giải, Người tạo, Ngày tạo, Phòng ban',
         '- Ngày gửi, Người duyệt, Ngày duyệt, Trạng thái',
         '- Ngày cập nhật, Người cập nhật (mặc định bỏ tích)', '- Hành động (khóa, luôn cuối bảng)']),
       ('Ô tích của cột', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Theo cấu hình',
        ['- Tích: cột hiện trên bảng', '- Cột khóa: ô tích xám, không bỏ được']),
       ('Biểu tượng ba gạch', 'Icon Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Kéo để đổi vị trí cột', '- Cột khóa hiện biểu tượng ổ khóa, không kéo được']),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi cột (trừ cột khóa).'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi cột (trừ cột khóa).'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình, đóng cửa sổ, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ; thay đổi chưa lưu bị bỏ.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”'])],
   ev=[('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Cấu hình đã nạp lúc mở màn.\n'
        'During:\n– Liệt kê 16 cột theo cấu hình đang áp dụng.\n'
        'After:\n– Mở cửa sổ “Tuỳ chỉnh cột”.'),
       ('Kéo biểu tượng ba gạch', 'Drag',
        'Before:\n– Cột khóa không kéo được.\n'
        'During:\n– Đổi thứ tự cột trong cửa sổ.\n'
        'After:\n– Chưa áp lên bảng cho tới khi bấm Lưu.'),
       ('Bỏ tích một cột', 'Change',
        'Before:\n– Cột khóa không cho bỏ tích.\n'
        'During:\n– Ghi nhận trạng thái trong cửa sổ.\n'
        'After:\n– Chưa áp lên bảng cho tới khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình gắn với người dùng, dùng chung 2 chế độ danh sách.\n'
        'During:\n– Ghi cấu hình; lỗi → hiển thị “Thao tác thất bại”.\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng theo cấu hình mới.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\n'
        'During:\n– Bỏ thay đổi chưa lưu.\n'
        'After:\n– Đóng cửa sổ; lần mở sau hiện lại đúng cấu hình đang áp dụng.')])

# ------------------------------------------------------------ 2.5
fr(5, 'Lập phiếu yêu cầu hạch toán bổ sung', usecase=('FR-05', 'Lập phiếu', 'crud', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Lập phiếu yêu cầu hạch toán bổ sung',
       mota='Tạo một phiếu yêu cầu kế toán hạch toán bổ sung công nợ. Người dùng chọn 1 trong 7 loại yêu cầu, nhập các '
            'trường theo loại (chứng từ nguồn, đối tượng, số tiền, diễn giải hoặc bảng Chi tiết hạch toán), loại tiền, tỷ '
            'giá, đính kèm file; sau đó lưu nháp hoặc gửi duyệt cho kế toán.',
       tacnhan=TN_MOI,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách chung (không phải lối vào chờ '
                'duyệt).\n3. Chức năng không gắn quyền riêng.',
       chinh='1. Người dùng bấm Tạo mới; hệ thống mở màn “Tạo phiếu yêu cầu hạch toán bổ sung”, chọn sẵn loại tiền đầu '
             'danh mục.\n'
             '2. Người dùng chọn Loại yêu cầu; hệ thống hiện các trường theo loại (BR-01).\n'
             '3. Loại Điều chỉnh công nợ: bấm Thêm dòng, chọn đối tượng, hợp đồng (mục 2.6), nhập Số tiền, Ghi chú từng '
             'dòng. Loại khác: chọn chứng từ / đối tượng (mục 2.6), nhập Số tiền, Diễn giải.\n'
             '4. Người dùng kiểm tra Loại tiền, Tỷ giá; bấm Thêm tài liệu để đính kèm file.\n'
             '5. Người dùng bấm Lưu nháp, Gửi duyệt hoặc Lưu và tiếp tục.\n'
             '6. Hệ thống kiểm tra dữ liệu theo nút được bấm (BR-02), sinh mã PYCHTBS-NNNNNN, lưu phiếu, dòng chi tiết, '
             'file; công ty / phòng ban / bộ phận theo người lập.\n'
             '7. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của phiếu.\n'
             '8. Gửi duyệt: hệ thống gửi thông báo “[HTBS] Chờ duyệt: <số phiếu>” cho người có quyền Kế toán kho cùng '
             'công ty.\n'
             '9. Hệ thống hiển thị “Lưu thành công” hoặc “Gửi duyệt thành công” và quay về màn danh sách.',
       phu='• Lưu nháp khi chưa chọn Loại yêu cầu → ' + M_REQ + ' dưới ô, không gửi máy chủ.\n'
           '• Gửi duyệt thiếu / sai dữ liệu → báo đỏ dưới từng ô, hiển thị ' + TOAST_422 + ', cuộn tới ô lỗi đầu tiên, '
           'giữ nguyên dữ liệu đã nhập.\n'
           '• Đổi Loại yêu cầu → xóa sạch trường phụ thuộc loại cũ, không hỏi xác nhận.\n'
           '• Bấm ô hợp đồng khi dòng chưa có đối tượng → “Vui lòng chọn đối tượng trước”.\n'
           '• Lưu và tiếp tục → lưu nháp rồi mở lại form trống, ở lại màn Tạo.\n'
           '• Rời màn khi đã nhập dở → hộp “Thông tin chưa lưu” (Thoát / Ở lại).\n'
           '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
       dacbiet='Lưu nháp chỉ bắt buộc Loại yêu cầu; Gửi duyệt bắt buộc đủ trường theo loại và ít nhất 1 file đính kèm. '
               'Loại Phối hợp kinh doanh thường do màn Quyết toán hợp đồng bán sinh ra; nhập tay chỉ còn phần chung '
               '(Số tiền, Loại tiền, Tỷ giá, Diễn giải). Khóa các nút lưu trong lúc đang xử lý.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10e_filled'),
               shot_caption='Màn Tạo phiếu — loại Điều chỉnh công nợ khách hàng đã thêm dòng'),
   ui=form_ui(False), ev=save_ev(False))

# ------------------------------------------------------------ 2.6
fr(6, 'Chọn đối tượng và chứng từ', usecase=('FR-06', 'Chọn đối tượng và chứng từ', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(ten='Chọn khách hàng, nhà cung cấp, nhân viên, hợp đồng và chứng từ nguồn',
              mota='Các cửa sổ chọn dùng ở màn Tạo / Sửa phiếu: Chọn khách hàng, Chọn nhà cung cấp, Chọn nhân viên, Chọn '
                   'đơn hàng/hợp đồng (hợp đồng bán) hoặc Chọn hợp đồng mua, Chọn phiếu xác nhận bảo hành, Chọn phiếu xử lý '
                   'hàng thiếu. Chọn xong hệ thống điền ô và các ô phụ thuộc (nhà cung cấp, số tiền) theo chứng từ.',
              tacnhan=TN_MOI,
              dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn Tạo hoặc Sửa phiếu (người lập, phiếu '
                       'Đang tạo).\n3. Đã chọn Loại yêu cầu có ô cần chọn.',
              chinh='1. Người dùng bấm vào ô cần chọn (ô đối tượng đầu phiếu, ô đối tượng / hợp đồng của dòng, ô chứng từ).\n'
                    '2. Hệ thống mở cửa sổ tương ứng, nạp trang 1 dữ liệu hợp lệ.\n'
                    '3. Người dùng nhập điều kiện tìm, bấm Tìm kiếm hoặc Enter.\n'
                    '4. Người dùng bấm vào một dòng.\n'
                    '5. Hệ thống điền ô, đóng cửa sổ; chứng từ nguồn thì lấy thêm nhà cung cấp, số tiền.',
              phu='• Bấm ô hợp đồng khi dòng chưa có đối tượng → “Vui lòng chọn đối tượng trước”, không mở cửa sổ.\n'
                  '• Không có dữ liệu → câu rỗng riêng từng cửa sổ (vd “Không có hợp đồng phù hợp.”).\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không chọn, ô giữ nguyên.\n'
                  '• Chọn khách hàng → báo “Chọn khách hàng thành công”.\n'
                  '• Lỗi tải danh sách → “Lỗi khi tải dữ liệu” / “Lỗi khi tải danh sách nhà cung cấp” / “Lỗi khi tải danh '
                  'sách hợp đồng”.',
              dacbiet='Hợp đồng bán gồm hợp đồng HRM, hợp đồng dịch vụ bảo hành – sửa chữa, hợp đồng bán đầu kỳ; lọc theo '
                      'đối tượng của dòng. Phiếu xác nhận bảo hành: chỉ phiếu đã duyệt; phiếu xử lý hàng thiếu: đã duyệt, '
                      'có hạch toán. Nhân viên: chỉ nhân viên đang làm.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('11_customer'), shot_caption='Cửa sổ Chọn khách hàng',
               note='Các cửa sổ chọn được mở ngay trên màn hình Tạo / Sửa phiếu theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Theo cửa sổ',
        ['- “Chọn khách hàng”', '- “Chọn nhà cung cấp”', '- “Chọn nhân viên”',
         '- “Chọn đơn hàng/hợp đồng” (khách hàng) hoặc “Chọn hợp đồng mua” (nhà cung cấp)',
         '- “Chọn phiếu xác nhận bảo hành”', '- “Chọn phiếu xử lý hàng thiếu”']),
       ('Ô Tên hoặc mã khách hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Cửa sổ Chọn khách hàng, nhãn “Tên / Mã khách hàng”', '- Gợi ý “Nhập tên / mã khách hàng”',
         '- Enter = bấm Tìm kiếm']),
       ('Ô Mã số thuế', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Cửa sổ Chọn khách hàng', '- Gợi ý “Nhập mã số thuế”; tìm mã số thuế bắt đầu bằng chuỗi nhập']),
       ('Ô Số điện thoại', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Cửa sổ Chọn khách hàng', '- Gợi ý “Nhập số điện thoại”']),
       ('Bảng khách hàng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột STT, Mã KH - Tên khách hàng, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP',
         '- Gồm mọi khách hàng đang hoạt động', '- Bấm dòng → chọn, báo “Chọn khách hàng thành công”, đóng cửa sổ',
         '- Rỗng: “Không có khách hàng phù hợp bộ lọc”']),
       ('Ô Mã hoặc tên nhà cung cấp', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Cửa sổ Chọn nhà cung cấp, nhãn “Mã / Tên nhà cung cấp”', '- Gợi ý “Nhập mã hoặc tên nhà cung cấp”',
         '- Enter = bấm Tìm kiếm']),
       ('Bảng nhà cung cấp', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột STT, Mã nhà cung cấp (sắp xếp được), Tên nhà cung cấp (sắp xếp được)', '- Bấm dòng → chọn, đóng cửa sổ',
         '- Rỗng: “Không có nhà cung cấp phù hợp.”']),
       ('Ô Mã hoặc tên nhân viên', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Cửa sổ Chọn nhân viên, nhãn “Mã / Tên nhân viên”', '- Gợi ý “Nhập mã hoặc tên nhân viên”']),
       ('Bảng nhân viên', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột STT, Mã nhân viên, Tên nhân viên (đều sắp xếp được)', '- Chỉ nhân viên đang làm',
         '- Bấm dòng → chọn, đóng cửa sổ', '- Rỗng: “Không có nhân viên phù hợp.”']),
       ('Ô Số đơn hàng/Hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Cửa sổ chọn hợp đồng', '- Gợi ý “Nhập số hợp đồng”; tìm số hợp đồng chứa chuỗi nhập',
         '- Đầu cửa sổ ghi đối tượng của dòng đang chọn']),
       ('Bảng hợp đồng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột STT, Số đơn hàng/Hợp đồng, Ngày lập, Giá trị hợp đồng, Số tiền còn nợ',
         '- Chỉ hợp đồng của đối tượng của dòng', '- Bấm dòng → điền hợp đồng của dòng, đóng cửa sổ',
         '- Rỗng: “Không có hợp đồng phù hợp.”']),
       ('Ô Mã phiếu xác nhận bảo hành', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Cửa sổ Chọn phiếu xác nhận bảo hành, nhãn “Mã phiếu”', '- Gợi ý “Nhập mã phiếu”']),
       ('Ô Người tạo phiếu xác nhận bảo hành', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Cửa sổ Chọn phiếu xác nhận bảo hành, nhãn “Người tạo”', '- Mặc định: trống, gợi ý “Chọn người tạo”',
         '- Chọn / bỏ chọn là lọc lại luôn']),
       ('Bảng phiếu xác nhận bảo hành', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột STT, Mã phiếu, Nhà cung cấp, Người tạo', '- Chỉ phiếu đã duyệt',
         '- Bấm dòng → điền phiếu, Nhà cung cấp, Số tiền; đóng cửa sổ',
         '- Rỗng: “Không có phiếu xác nhận bảo hành đã duyệt nào.”']),
       ('Ô Số phiếu xử lý hàng thiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Cửa sổ Chọn phiếu xử lý hàng thiếu, nhãn “Số phiếu”', '- Gợi ý “Nhập số phiếu”']),
       ('Ô Phiếu nhập kho', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Cửa sổ Chọn phiếu xử lý hàng thiếu', '- Gợi ý “Nhập số phiếu nhập kho”']),
       ('Bảng phiếu xử lý hàng thiếu', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột STT, Số phiếu, Phiếu nhập kho, Yêu cầu nhập, Số hợp đồng', '- Chỉ phiếu đã duyệt, có hạch toán',
         '- Bấm dòng → điền phiếu, Số tiền, Nhà cung cấp (1 NCC tự điền, nhiều NCC hiện ô chọn)',
         '- Rỗng: “Không có phiếu xử lý hàng thiếu nào đang chờ hạch toán bổ sung.”']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp điều kiện tìm, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa điều kiện tìm, nạp lại từ trang 1.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không chọn.'),
       ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1', ['- Dòng “Hiển thị a–b / N”, Số dòng/trang',
                                                                     '- Mặc định 10 dòng/trang']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Vui lòng chọn đối tượng trước”: bấm ô hợp đồng khi dòng chưa có đối tượng',
         '- “Lỗi khi lấy dữ liệu phiếu xác nhận bảo hành” / “Lỗi khi lấy dữ liệu phiếu xử lý hàng thiếu”: '
         'không lấy được dữ liệu chứng từ vừa chọn'])],
   ev=[('Bấm ô cần chọn', 'Click',
        'Before:\n– Màn chi tiết (chỉ đọc) và ô tự điền theo chứng từ không bấm được.\n'
        '– Ô hợp đồng của dòng: dòng chưa có đối tượng → hiển thị “Vui lòng chọn đối tượng trước” và dừng.\n'
        'During:\n– Ô đối tượng đầu phiếu mở Chọn nhà cung cấp / Chọn khách hàng / Chọn nhân viên theo loại và ô '
        'Đối tượng; ô đối tượng của dòng mở Chọn khách hàng (Điều chỉnh công nợ khách hàng) hoặc Chọn nhà cung cấp.\n'
        'After:\n– Mở cửa sổ, nạp trang 1 dữ liệu hợp lệ.'),
       ('Bấm Tìm kiếm hoặc Enter', 'Click',
        'Before:\n– Lấy điều kiện ở các ô tìm của cửa sổ.\n'
        'During:\n– Tìm theo chuỗi chứa (mã số thuế: bắt đầu bằng).\n'
        'After:\n– Về trang 1, hiển thị kết quả hoặc câu rỗng của cửa sổ.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Xóa điều kiện tìm.\nAfter:\n– Nạp lại từ trang 1.'),
       ('Bấm một dòng đối tượng', 'Click',
        'Before:\n– Cửa sổ Chọn khách hàng, Chọn nhà cung cấp hoặc Chọn nhân viên.\n'
        'During:\n– Ghi đối tượng vào ô đang chọn; ô đối tượng của dòng thì xóa hợp đồng cũ của dòng đó.\n'
        'After:\n– Đóng cửa sổ; ô hiện “Mã - Tên”; chọn khách hàng thì báo “Chọn khách hàng thành công”.'),
       ('Bấm một dòng hợp đồng', 'Click',
        'Before:\n– Cửa sổ đang lọc theo đối tượng của dòng.\n'
        'During:\n– Ghi số hợp đồng và loại hợp đồng vào dòng.\n'
        'After:\n– Đóng cửa sổ, ô hợp đồng của dòng hiện số hợp đồng.'),
       ('Bấm một dòng chứng từ nguồn', 'Click',
        'Before:\n– Cửa sổ Chọn phiếu xác nhận bảo hành hoặc Chọn phiếu xử lý hàng thiếu.\n'
        'During:\n– Lấy dữ liệu hạch toán của chứng từ; lỗi → “Lỗi khi lấy dữ liệu phiếu xác nhận bảo hành” / “Lỗi khi '
        'lấy dữ liệu phiếu xử lý hàng thiếu”.\n'
        'After:\n– Phiếu xác nhận bảo hành: điền số phiếu, Nhà cung cấp, Số tiền.\n'
        '– Phiếu xử lý hàng thiếu: điền số phiếu, Số tiền; 1 nhà cung cấp thì tự điền, nhiều nhà cung cấp thì hiện ô chọn.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không ghi gì vào form.\nAfter:\n– Đóng cửa sổ, ô giữ nguyên.')])

# ------------------------------------------------------------ 2.7
fr(7, 'Chỉnh sửa phiếu', usecase=('FR-07', 'Chỉnh sửa phiếu', 'crud', A_LAP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(ten='Chỉnh sửa phiếu yêu cầu hạch toán bổ sung',
              mota='Người lập sửa phiếu đang ở trạng thái Đang tạo, gồm phiếu mới lưu nháp và phiếu bị kế toán từ chối trả '
                   'về. Màn Sửa dùng chung bố cục và quy tắc kiểm tra với màn Tạo (mục 2.5); thêm được, thay hoặc xóa file '
                   'đã lưu; lưu nháp hoặc gửi duyệt lại.',
              tacnhan=TN_SUA, dieukien=DK_SUA,
              chinh='1. Người dùng bấm Sửa ở cột Hành động hoặc ở màn chi tiết.\n'
                    '2. Hệ thống kiểm tra người lập, trạng thái; mở màn “Sửa phiếu yêu cầu hạch toán bổ sung: <số phiếu>” '
                    'với dữ liệu phiếu.\n'
                    '3. Người dùng sửa các trường (quy tắc như mục 2.5), thêm / thay / xóa file.\n'
                    '4. Người dùng bấm Lưu nháp hoặc Gửi duyệt.\n'
                    '5. Hệ thống kiểm tra quyền và dữ liệu (BR-02), lưu phiếu.\n'
                    '6. Hệ thống ghi nhận hành động “Thay đổi thông tin” trong lịch sử của phiếu (chỉ trường đã đổi); gửi '
                    'duyệt thì ghi thêm “Thay đổi trạng thái” Đang tạo → Chờ duyệt và xóa Ghi chú duyệt cũ.\n'
                    '7. Gửi duyệt: hệ thống gửi thông báo “[HTBS] Chờ duyệt: <số phiếu>” cho người có quyền Kế toán kho '
                    'cùng công ty.\n'
                    '8. Hệ thống hiển thị “Lưu thành công” / “Gửi duyệt thành công”, quay về màn danh sách.',
              phu='• Phiếu không sửa được (không phải người lập hoặc đã gửi duyệt) → “Phiếu này không sửa được”, chuyển '
                  'sang màn chi tiết.\n'
                  '• Phiếu không tồn tại → ' + M_NOTFOUND + '; ngoài phạm vi → ' + M_NOPERM_VIEW + '; về danh sách.\n'
                  '• Phiếu đổi trạng thái giữa chừng (người khác vừa xử lý) → “Bạn không có quyền sửa phiếu này”.\n'
                  '• Phiếu bị từ chối hiện Ghi chú duyệt (lý do) ở khối Thông tin chung.\n'
                  '• Rời màn khi chưa lưu → hộp “Thông tin chưa lưu”.',
              dacbiet='Phiếu đã có file thì lần sửa không bắt buộc đính kèm thêm. Xóa file đã lưu có hiệu lực ngay (không cần '
                      'bấm Lưu); thay file đã lưu chỉ áp khi lưu phiếu.'),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('19_edit'), shot_caption='Màn Sửa phiếu yêu cầu hạch toán bổ sung'),
   ui=form_ui(True), ev=save_ev(True))

# ------------------------------------------------------------ 2.8
fr(8, 'Gửi duyệt phiếu', usecase=('FR-08', 'Gửi duyệt', 'action', A_LAP),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(ten='Gửi duyệt từ màn chi tiết',
              mota='Người lập gửi phiếu Đang tạo sang kế toán ngay từ màn chi tiết mà không mở form Sửa. Hệ thống kiểm tra '
                   'phiếu đã đủ điều kiện gửi duyệt (có dòng chi tiết với 2 loại Điều chỉnh công nợ, số tiền > 0, có file '
                   'đính kèm) rồi chuyển phiếu sang Chờ duyệt và báo cho kế toán.',
              tacnhan=TN_SUA, dieukien=DK_SUA,
              chinh='1. Người dùng mở màn chi tiết phiếu, bấm Gửi duyệt ở chân màn.\n'
                    '2. Hệ thống hiển thị hộp “Xác nhận gửi duyệt”.\n'
                    '3. Người dùng bấm Gửi duyệt trong hộp.\n'
                    '4. Hệ thống kiểm tra người lập, trạng thái và dữ liệu phiếu.\n'
                    '5. Hệ thống chuyển phiếu sang Chờ duyệt, ghi Ngày gửi, xóa Ghi chú duyệt cũ.\n'
                    '6. Hệ thống ghi nhận hành động “Thay đổi trạng thái” Đang tạo → Chờ duyệt trong lịch sử của phiếu.\n'
                    '7. Hệ thống gửi thông báo “[HTBS] Chờ duyệt: <số phiếu>” cho người có quyền Kế toán kho cùng công ty.\n'
                    '8. Hệ thống hiển thị “Gửi duyệt thành công” và nạp lại màn chi tiết (nút Sửa / Gửi duyệt / Xóa ẩn đi).',
              phu='• Bấm Hủy / (x) / click ra ngoài hộp → đóng hộp, không gửi.\n'
                  '• Phiếu chưa đủ điều kiện → báo lỗi (vd “Phiếu chưa có file đính kèm”), phiếu giữ Đang tạo.\n'
                  '• Không phải người lập / phiếu đã đổi trạng thái → “Bạn không có quyền gửi duyệt phiếu này” hoặc '
                  '“Không thể chuyển phiếu từ trạng thái hiện tại sang trạng thái này”.',
              dacbiet='Khóa nút trong lúc đang gửi để tránh gửi 2 lần.'),
   layout=dict(menu=MENU + ' => Xem chi tiết => Gửi duyệt', shot=shot('19_edit'), shot_caption='Phiếu Đang tạo — nút Gửi duyệt ở chân màn'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Gửi duyệt', 'Button', 'Enable / Ẩn', 'Ẩn',
        ['- Chân màn chi tiết', '- Chỉ hiện với người lập, phiếu Đang tạo', '- Khóa trong lúc đang gửi',
         '- Bấm → hộp Xác nhận gửi duyệt']),
       ('Hộp Xác nhận gửi duyệt', 'Popup', 'Hiển thị', 'Ẩn', ['- Tiêu đề “Xác nhận gửi duyệt”', '- Có nút (x) đóng']),
       ('Nội dung hộp xác nhận', 'Label', 'Hiển thị', '–', SEND_MSG),
       ('Nút Gửi duyệt của hộp', 'Button', 'Enable', 'Hiển thị', 'Xác nhận gửi phiếu.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không gửi.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        ['- Thành công: “Gửi duyệt thành công”',
         '- Lỗi: câu máy chủ trả, vd “Phiếu chưa có dòng chi tiết nào, không gửi duyệt được”, “Số tiền của phiếu phải lớn '
         'hơn 0”, “Phiếu chưa có file đính kèm”, “Bạn không có quyền gửi duyệt phiếu này”',
         '- Lỗi khác: “Cập nhật thất bại”'])],
   ev=[('Bấm Gửi duyệt', 'Click',
        'Before:\n– Nút chỉ hiện với người lập, phiếu Đang tạo.\n'
        'During:\n– Hiển thị hộp “Xác nhận gửi duyệt” nội dung ' + SEND_MSG + '.\n'
        'After:\n– Bấm Gửi duyệt trong hộp → chuyển sang bước xác nhận; bấm Hủy → dừng.'),
       ('Bấm Gửi duyệt trong hộp xác nhận', 'Click',
        'Before:\n– Kiểm tra trạng thái hiện tại cho phép chuyển sang Chờ duyệt; sai → “Không thể chuyển phiếu từ trạng '
        'thái hiện tại sang trạng thái này”.\n'
        '– Kiểm tra người lập; sai → “Bạn không có quyền gửi duyệt phiếu này” và dừng xử lý.\n'
        'During:\n– 2 loại Điều chỉnh công nợ chưa có dòng → “Phiếu chưa có dòng chi tiết nào, không gửi duyệt được”.\n'
        '– Số tiền ≤ 0 → “Số tiền của phiếu phải lớn hơn 0”.\n'
        '– Chưa có file → “Phiếu chưa có file đính kèm”.\n' + ERR + '\n'
        'After:\n– Phiếu chuyển Chờ duyệt, ghi Ngày gửi, xóa Ghi chú duyệt cũ.\n'
        '– Ghi một dòng lịch sử “Thay đổi trạng thái” Đang tạo → Chờ duyệt.\n'
        '– Gửi thông báo “[HTBS] Chờ duyệt: <số phiếu>” cho người có quyền Kế toán kho cùng công ty với phiếu.\n'
        '– Hiển thị “Gửi duyệt thành công”, nạp lại màn chi tiết.'),
       ('Bấm Hủy, (x) hoặc click ra ngoài hộp', 'Click',
        'Before:\n– Hộp xác nhận đang mở.\nDuring:\n– Không gọi máy chủ.\nAfter:\n– Đóng hộp, phiếu giữ Đang tạo.')])

# ------------------------------------------------------------ 2.9
fr(9, 'Xóa phiếu', usecase=('FR-09', 'Xóa phiếu', 'action', A_LAP),
   rule=('- Quy tắc Xóa và Thông báo.', 'delete'),
   intro=dict(ten='Xóa phiếu yêu cầu hạch toán bổ sung',
              mota='Người lập xóa hẳn phiếu đang ở trạng thái Đang tạo cùng toàn bộ dòng chi tiết. Thao tác mở được từ cột '
                   'Hành động của màn danh sách hoặc chân màn chi tiết, luôn qua hộp xác nhận; phiếu đã gửi duyệt không '
                   'xóa được.',
              tacnhan=TN_SUA, dieukien=DK_SUA,
              chinh='1. Người dùng bấm Xóa ở cột Hành động hoặc ở màn chi tiết.\n'
                    '2. Hệ thống hiển thị hộp “Xác nhận xóa” kèm số phiếu.\n'
                    '3. Người dùng bấm Xóa.\n'
                    '4. Hệ thống kiểm tra người lập, trạng thái.\n'
                    '5. Hệ thống ghi nhận hành động “Xóa” trong lịch sử của phiếu (kèm dòng chi tiết, file), sau đó xóa '
                    'phiếu và dòng chi tiết.\n'
                    '6. Hệ thống hiển thị “Xóa thành công”: ở danh sách thì nạp lại bảng; ở màn chi tiết thì về danh sách.',
              phu='• Bấm Hủy / (x) / click ra ngoài hộp → không xóa.\n'
                  '• Không phải người lập hoặc phiếu đã đổi trạng thái → “Bạn không có quyền xóa phiếu này”; ở danh sách '
                  'thì nạp lại bảng cho khớp hiện trạng.\n'
                  '• Lỗi khác → “Xóa thất bại”.',
              dacbiet=None),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp xác nhận xóa phiếu',
               note='Modal Xác nhận xóa được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Xóa trên dòng', 'Icon Button', 'Enable / Ẩn', 'Ẩn',
        ['- Cột Hành động (đỏ) hoặc chân màn chi tiết', '- Chỉ hiện với người lập, phiếu Đang tạo']),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', '“Xác nhận xóa”', 'Kèm nút (x) đóng.'),
       ('Nội dung', 'Label', 'Hiển thị', '–', DEL_MSG),
       ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Xác nhận xóa phiếu.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không xóa.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        ['- Thành công: “Xóa thành công”', '- Không đủ điều kiện: “Bạn không có quyền xóa phiếu này”',
         '- Lỗi khác: “Xóa thất bại”'])],
   ev=[('Bấm Xóa ở cột Hành động hoặc màn chi tiết', 'Click',
        'Before:\n– Nút chỉ hiện với người lập, phiếu Đang tạo.\n'
        'During:\n– Ghi nhận phiếu cần xóa.\n'
        'After:\n– Hiển thị hộp “Xác nhận xóa” nội dung ' + DEL_MSG + '.'),
       ('Bấm Xóa trong hộp xác nhận', 'Click',
        'Before:\n– Kiểm tra người đăng nhập là người lập, phiếu Đang tạo.\n'
        '– Không đủ điều kiện → hiển thị “Bạn không có quyền xóa phiếu này” và dừng xử lý.\n'
        'During:\n– Phiếu không còn tồn tại (vừa bị xóa) → báo lỗi, không xóa.\n' + ERR + '\n'
        'After:\n– Ghi một dòng lịch sử “Xóa” (kèm dòng chi tiết, file đính kèm).\n'
        '– Xóa phiếu và toàn bộ dòng chi tiết.\n'
        '– Hiển thị “Xóa thành công”; ở danh sách nạp lại bảng, ở màn chi tiết quay về danh sách.'),
       ('Bấm Hủy, (x) hoặc click ra ngoài hộp', 'Click',
        'Before:\n– Hộp đang mở.\nDuring:\n– Không gọi máy chủ.\nAfter:\n– Đóng hộp, phiếu giữ nguyên.')])

# ------------------------------------------------------------ 2.10
fr(10, 'Xem chi tiết phiếu', usecase=('FR-10', 'Xem chi tiết phiếu', 'view', A_LAP),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(ten='Xem chi tiết phiếu yêu cầu hạch toán bổ sung',
              mota='Xem toàn bộ thông tin một phiếu ở chế độ chỉ đọc, bố cục theo loại yêu cầu (dùng lại đúng bố cục màn Sửa; '
                   'riêng loại Phối hợp kinh doanh có bố cục riêng), kèm khối Lịch sử. Chân màn hiện các nút thao tác theo '
                   'vai trò và trạng thái phiếu, cùng điều kiện với cột Hành động ở danh sách.',
              tacnhan=TN_XEM,
              dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu nằm trong phạm vi xem của người dùng (Phần 2).\n'
                       '3. Phiếu Đang tạo chỉ người lập xem được.',
              chinh='1. Người dùng bấm số phiếu ở danh sách (hoặc mở từ thông báo).\n'
                    '2. Hệ thống kiểm tra phạm vi xem.\n'
                    '3. Hệ thống mở màn “Chi tiết phiếu yêu cầu hạch toán bổ sung: <số phiếu>”, hiện thông tin theo loại.\n'
                    '4. Hệ thống hiện nút ở chân màn theo vai trò và trạng thái.',
              phu='• Ngoài phạm vi → ' + M_NOPERM_VIEW + ', về danh sách.\n'
                  '• Phiếu không tồn tại / vừa bị xóa → ' + M_NOTFOUND + ', về danh sách.\n'
                  '• Lỗi khác → “Lỗi khi tải phiếu”.\n'
                  '• Bấm số hợp đồng của dòng chi tiết → mở hợp đồng ở tab mới.',
              dacbiet='Loại Phối hợp kinh doanh hiển thị khối riêng: Thông tin chung (Loại yêu cầu, Khách hàng, Phòng thực '
                      'hiện, Số hợp đồng, Loại tiền, Tỷ giá, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Diễn giải, Ghi chú '
                      'duyệt), bảng Nội dung quyết toán, bảng Đối tượng hạch toán theo phòng hỗ trợ / nhân viên.'),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn chi tiết phiếu Chờ duyệt — loại Điều chỉnh công nợ khách hàng'),
   ui_kw=dict(required=False),
   ui=[('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '“Chi tiết phiếu yêu cầu hạch toán bổ sung: <số phiếu>”.'),
       ('Khối Thông tin chung', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Người tạo – ngày giờ tạo ở góc phải', '- Loại yêu cầu và các trường theo loại như màn Sửa, nền xám chỉ đọc',
         '- Loại tiền, Tỷ giá, Diễn giải', '- Ghi chú duyệt: chỉ hiện khi phiếu từng bị từ chối',
         '- Không hiện nhãn trạng thái, không có ô Số phiếu']),
       ('Bảng Chi tiết hạch toán', 'Table/Grid', 'Read-only', '–', 'Ẩn',
        ['- Chỉ với 2 loại Điều chỉnh công nợ', '- Cột STT, Khách hàng (Nhà cung cấp), Hợp đồng bán (Hợp đồng mua), Số tiền, '
         'Ghi chú; dòng Tổng cộng',
         '- Bấm số hợp đồng → mở hợp đồng ở tab mới', '- Rỗng: “Chưa có dòng chi tiết nào.”']),
       ('Bảng File đính kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột STT, Upload File (tên file), Dung lượng', '- Bấm tên file → xem trước']),
       ('Bảng Nội dung quyết toán', 'Table/Grid', 'Read-only', '–', 'Ẩn',
        ['- Chỉ loại Phối hợp kinh doanh', '- Cột STT, Nội dung, Số tiền', '- Rỗng: “Không có dữ liệu.”']),
       ('Bảng Đối tượng hạch toán', 'Table/Grid', 'Read-only', '–', 'Ẩn',
        ['- Chỉ loại Phối hợp kinh doanh', '- Cột STT, Phòng hỗ trợ, Đối tượng hạch toán, Số tiền, Vụ việc',
         '- Rỗng: “Không có dữ liệu.”']),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
        ['- Nút “Xem lịch sử” / “Thu gọn”', '- Nội dung như mục 2.15']),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
        ['- Người lập, phiếu Đang tạo', '- Bấm → màn Sửa (mục 2.7)']),
       ('Nút Gửi duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
        ['- Người lập, phiếu Đang tạo', '- Bấm → hộp Xác nhận gửi duyệt (mục 2.8)']),
       ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
        ['- Màu đỏ', '- Kế toán thanh toán, phiếu Chờ duyệt trong phạm vi', '- Bấm → cửa sổ Từ chối (mục 2.11)']),
       ('Nút Lập phiếu kế toán', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
        ['- Điều kiện như mục 2.12', '- Bấm → màn Tạo phiếu kế toán']),
       ('Nút In phiếu', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ xem trước bản in (mục 2.13).'),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Tải file Excel của phiếu (mục 2.14).'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
        ['- Màu đỏ; người lập, phiếu Đang tạo', '- Bấm → hộp Xác nhận xóa (mục 2.9)']),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- ' + M_NOPERM_VIEW + ': ngoài phạm vi', '- ' + M_NOTFOUND + ': phiếu không tồn tại',
         '- “Lỗi khi tải phiếu”: lỗi khác'])],
   ev=[('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phiếu tồn tại và nằm trong phạm vi xem; phiếu Đang tạo chỉ người lập xem.\n'
        '– Ngoài phạm vi → hiển thị ' + M_NOPERM_VIEW + ' và quay về danh sách.\n'
        'During:\n– Không tồn tại → ' + M_NOTFOUND + ', quay về danh sách.\n'
        '– Xác định bố cục theo loại: Phối hợp kinh doanh dùng bố cục riêng, loại khác dùng bố cục màn Sửa ở chế độ chỉ đọc.\n'
        'After:\n– Hiển thị thông tin, khối Lịch sử thu gọn; nút chân màn theo vai trò và trạng thái.'),
       ('Bấm số hợp đồng của dòng chi tiết', 'Click',
        'Before:\n– Dòng có số hợp đồng.\nDuring:\n– Xác định màn hợp đồng tương ứng (hợp đồng HRM hoặc hợp đồng cũ).\n'
        'After:\n– Mở hợp đồng ở tab mới.'),
       ('Bấm tên file đính kèm', 'Click',
        'Before:\n– File đã lưu của phiếu.\nDuring:\n– Lấy đường dẫn file.\nAfter:\n– Mở cửa sổ xem trước file.'),
       ('Bấm Xem lịch sử', 'Click',
        'Before:\n– Khối Lịch sử đang thu gọn.\nDuring:\n– Nạp các mốc lịch sử của phiếu.\n'
        'After:\n– Mở khối, nhãn nút đổi thành “Thu gọn” (mục 2.15).'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– Màn chỉ đọc, không hỏi xác nhận.\nDuring:\n– Chuyển màn.\nAfter:\n– Về màn danh sách.')])

# ------------------------------------------------------------ 2.11
fr(11, 'Từ chối phiếu', usecase=('FR-11', 'Từ chối phiếu', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(ten='Từ chối phiếu yêu cầu hạch toán bổ sung',
              mota='Kế toán thanh toán trả phiếu Chờ duyệt về trạng thái Đang tạo, bắt buộc nhập lý do. Lý do được lưu vào '
                   'Ghi chú duyệt để người lập xem, ghi vào lịch sử của phiếu và gửi thông báo cho người lập; hệ thống ghi '
                   'nhận người và thời điểm từ chối vào cột Người duyệt / Ngày duyệt.',
              tacnhan='Người dùng có quyền thực hiện chức năng: Kế toán thanh toán (phiếu thuộc phạm vi công ty mình; loại '
                      'Phối hợp kinh doanh theo công ty của phòng hỗ trợ).',
              dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán thanh toán, phiếu thuộc phạm vi '
                       'công ty mình.\n3. Phiếu đang ở trạng thái Chờ duyệt.',
              chinh='1. Kế toán mở chi tiết phiếu, bấm Từ chối.\n'
                    '2. Hệ thống mở cửa sổ “Từ chối phiếu yêu cầu hạch toán bổ sung”, con trỏ đặt sẵn ở ô lý do.\n'
                    '3. Kế toán nhập Lý do từ chối, bấm Từ chối.\n'
                    '4. Hệ thống kiểm tra quyền, trạng thái, lý do.\n'
                    '5. Hệ thống đưa phiếu về Đang tạo, lưu lý do vào Ghi chú duyệt, ghi Người duyệt / Ngày duyệt.\n'
                    '6. Hệ thống ghi nhận hành động “Thay đổi trạng thái” Chờ duyệt → Đang tạo kèm lý do trong lịch sử của '
                    'phiếu.\n'
                    '7. Hệ thống gửi thông báo “[HTBS] Từ chối: <số phiếu>” cho người lập, kèm loại yêu cầu, người từ chối, '
                    'lý do.\n'
                    '8. Hệ thống hiển thị “Từ chối phiếu thành công”, đóng cửa sổ, nạp lại màn chi tiết.',
              phu='• Lý do trống → ' + M_REQ + ' dưới ô, không gửi.\n'
                  '• Bấm Hủy / (x) / click ra ngoài cửa sổ → đóng, không từ chối (nội dung đã nhập bị bỏ, không hỏi xác '
                  'nhận).\n'
                  '• Không đủ quyền / sai phạm vi → “Bạn không có quyền từ chối phiếu này”; phiếu đã đổi trạng thái → '
                  '“Không thể chuyển phiếu từ trạng thái hiện tại sang trạng thái này”.',
              dacbiet='Lý do tối đa 1.000 ký tự. Người lập sửa và gửi lại được; khi gửi lại, Ghi chú duyệt cũ bị xóa.'),
   layout=dict(menu=MENU_CD + ' => Xem chi tiết => Từ chối', shot=shot('15_reject'), shot_caption='Cửa sổ Từ chối phiếu',
               note='Modal Từ chối phiếu yêu cầu hạch toán bổ sung được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
   ui=[('Nút Từ chối ở chân màn', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
        ['- Màu đỏ', '- Chỉ hiện với Kế toán thanh toán, phiếu Chờ duyệt trong phạm vi', '- Bấm → mở cửa sổ Từ chối']),
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Từ chối phiếu yêu cầu hạch toán bổ sung”',
        ['- Dòng phụ “Phiếu: <số phiếu>”', '- Có nút (x) đóng']),
       ('Lý do từ chối', 'Textarea', 'Enable', '1–1.000 ký tự', 'Có', 'Trống',
        ['- Gợi ý “Nhập lý do từ chối”, 3 dòng', '- Con trỏ đặt sẵn khi mở cửa sổ',
         '- Trống (kể cả chỉ có dấu cách) → ' + M_REQ + ', viền đỏ']),
       ('Nút Từ chối', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Màu đỏ', '- Khóa trong lúc đang xử lý', '- Bấm → kiểm tra lý do rồi gửi']),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không từ chối.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Từ chối phiếu thành công”', '- Không đủ quyền: “Bạn không có quyền từ chối phiếu này”',
         '- Lỗi khác: “Cập nhật thất bại”'])],
   ev=[('Bấm Từ chối ở chân màn', 'Click',
        'Before:\n– Nút chỉ hiện với Kế toán thanh toán, phiếu Chờ duyệt trong phạm vi.\n'
        'During:\n– Xóa lý do cũ, tắt báo lỗi.\n'
        'After:\n– Mở cửa sổ Từ chối, đặt con trỏ vào ô lý do.'),
       ('Bấm Từ chối trong cửa sổ', 'Click',
        'Before:\n– Kiểm tra quyền Kế toán thanh toán và phạm vi công ty; sai → “Bạn không có quyền từ chối phiếu này” và '
        'dừng xử lý.\n'
        '– Kiểm tra phiếu đang Chờ duyệt; sai → “Không thể chuyển phiếu từ trạng thái hiện tại sang trạng thái này”.\n'
        'During:\n– Lý do trống → hiển thị ' + M_REQ + '.\n'
        '– Lý do quá 1.000 ký tự → “Vui lòng nhập tối đa 1000 ký tự.”.\n' + ERR + '\n'
        'After:\n– Phiếu về Đang tạo; lưu lý do vào Ghi chú duyệt; ghi Người duyệt, Ngày duyệt.\n'
        '– Ghi một dòng lịch sử “Thay đổi trạng thái” Chờ duyệt → Đang tạo kèm lý do.\n'
        '– Gửi thông báo “[HTBS] Từ chối: <số phiếu>” cho người lập.\n'
        '– Hiển thị “Từ chối phiếu thành công”, đóng cửa sổ, nạp lại màn chi tiết.'),
       ('Bấm Hủy, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả đã nhập lý do.\nDuring:\n– Không gọi máy chủ.\n'
        'After:\n– Đóng cửa sổ, phiếu giữ Chờ duyệt.')])

# ------------------------------------------------------------ 2.12
fr(12, 'Lập phiếu kế toán', usecase=('FR-12', 'Lập phiếu kế toán', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(ten='Lập phiếu kế toán từ phiếu yêu cầu',
              mota='Kế toán mở màn Tạo phiếu kế toán với phiếu yêu cầu hạch toán bổ sung chọn sẵn để ghi sổ. Trạng thái phiếu '
                   'yêu cầu đi theo phiếu kế toán: lưu phiếu kế toán → Đang duyệt; duyệt phiếu kế toán → Đã duyệt; xóa phiếu '
                   'kế toán → trở lại Chờ duyệt.',
              tacnhan=TN_KT, dieukien=DK_KT,
              chinh='1. Kế toán bấm Lập phiếu kế toán ở cột Hành động hoặc chân màn chi tiết.\n'
                    '2. Hệ thống mở màn “Tạo phiếu kế toán” với phiếu yêu cầu chọn sẵn, dữ liệu điền sẵn theo phiếu yêu cầu.\n'
                    '3. Kế toán hoàn thiện và lưu phiếu kế toán (theo SRS màn Phiếu kế toán).\n'
                    '4. Hệ thống chuyển phiếu yêu cầu sang Đang duyệt.\n'
                    '5. Khi phiếu kế toán được duyệt: phiếu yêu cầu chuyển Đã duyệt, ghi Người duyệt / Ngày duyệt, gửi '
                    'thông báo cho người lập phiếu yêu cầu.',
              phu='• Thoát màn Tạo phiếu kế toán không lưu → phiếu yêu cầu giữ Chờ duyệt.\n'
                  '• Xóa phiếu kế toán đã lập → phiếu yêu cầu trở lại Chờ duyệt.\n'
                  '• Không đủ điều kiện → nút không hiện.',
              dacbiet='Loại Phối hợp kinh doanh: chỉ người có quyền Kế toán thuộc công ty của phòng hỗ trợ ghi trên phiếu.'),
   layout=dict(menu=MENU_CD + ' => Lập phiếu kế toán', shot=shot('21_accounting_create'), shot_caption='Màn Tạo phiếu kế toán mở từ phiếu yêu cầu'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Lập phiếu kế toán trên dòng', 'Icon Button', 'Enable / Ẩn', 'Ẩn',
        ['- Cột Hành động, biểu tượng tờ giấy có dấu +', '- Chỉ hiện với phiếu Chờ duyệt',
         '- Mọi loại trừ Phối hợp kinh doanh: Kế toán thanh toán, phiếu thuộc phạm vi công ty',
         '- Phối hợp kinh doanh: Kế toán, công ty mình có phòng hỗ trợ của phiếu']),
       ('Nút Lập phiếu kế toán ở chân màn', 'Button', 'Enable / Ẩn', 'Ẩn',
        ['- Màn chi tiết, cùng điều kiện với nút trên dòng', '- Bấm → màn Tạo phiếu kế toán']),
       ('Màn Tạo phiếu kế toán', 'Label', 'Hiển thị', 'Ẩn',
        ['- Phiếu yêu cầu chọn sẵn, dữ liệu điền sẵn', '- Bố cục và quy tắc theo SRS màn Phiếu kế toán'])],
   ev=[('Bấm Lập phiếu kế toán', 'Click',
        'Before:\n– Kiểm tra phiếu Chờ duyệt.\n'
        '– Phối hợp kinh doanh: kiểm tra quyền Kế toán và công ty của phòng hỗ trợ; loại khác: kiểm tra quyền Kế toán '
        'thanh toán và phạm vi công ty. Không đủ điều kiện thì nút không hiện.\n'
        'During:\n– Chuyển sang màn Tạo phiếu kế toán, gửi kèm phiếu yêu cầu.\n'
        'After:\n– Màn Tạo phiếu kế toán tự nạp dữ liệu của phiếu yêu cầu; chưa ghi dữ liệu nào.'),
       ('Lưu phiếu kế toán', 'System',
        'Before:\n– Phiếu kế toán gắn với phiếu yêu cầu.\nDuring:\n– Lưu phiếu kế toán theo SRS màn Phiếu kế toán.\n'
        'After:\n– Phiếu yêu cầu chuyển Đang duyệt.'),
       ('Duyệt phiếu kế toán', 'System',
        'Before:\n– Phiếu kế toán gắn với phiếu yêu cầu.\nDuring:\n– Duyệt phiếu kế toán.\n'
        'After:\n– Phiếu yêu cầu chuyển Đã duyệt, ghi Người duyệt, Ngày duyệt.\n'
        '– Gửi thông báo cho người lập phiếu yêu cầu.'),
       ('Xóa phiếu kế toán', 'System',
        'Before:\n– Phiếu kế toán gắn với phiếu yêu cầu.\nDuring:\n– Xóa phiếu kế toán.\n'
        'After:\n– Phiếu yêu cầu trở lại Chờ duyệt.')])

# ------------------------------------------------------------ 2.13
fr(13, 'In phiếu', usecase=('FR-13', 'In phiếu', 'io', A_LAP),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(ten='In phiếu yêu cầu hạch toán bổ sung',
              mota='Xem trước bản in của một phiếu ngay trên màn hình (không mở tab mới) rồi in. Bản in dựng theo mẫu in '
                   '“Yêu cầu hạch toán bổ sung” của hệ thống, đầu trang là letterhead của công ty ghi trên phiếu, nội dung '
                   'theo loại yêu cầu.',
              tacnhan=TN_XEM, dieukien=DK_XEM.replace('3. Người dùng đang ở màn danh sách Phiếu yêu cầu hạch toán bổ sung.',
                                                       '3. Người dùng đang ở màn danh sách hoặc màn chi tiết phiếu.'),
              chinh='1. Người dùng bấm In phiếu ở cột Hành động hoặc chân màn chi tiết.\n'
                    '2. Hệ thống kiểm tra phạm vi xem, mở cửa sổ “Xem trước phiếu yêu cầu hạch toán bổ sung <số phiếu>”, '
                    'hiện “Đang tải dữ liệu in…”.\n'
                    '3. Hệ thống dựng bản in và hiển thị.\n'
                    '4. Người dùng bấm In; hệ thống mở hộp thoại in của trình duyệt.',
              phu='• Bấm (x) / click ra ngoài cửa sổ → đóng.\n'
                  '• Ngoài phạm vi → ' + M_NOPERM_VIEW + ' hiện trong cửa sổ.\n'
                  '• Thiếu mẫu in trên hệ thống → “Không tìm thấy mẫu in "Yêu cầu hạch toán bổ sung" trên hệ thống”.\n'
                  '• Bản in rỗng → “Không có dữ liệu để in”; lỗi khác → “Không tải được dữ liệu in”.',
              dacbiet='Letterhead lấy theo công ty ghi trên phiếu (không theo người đang đăng nhập). Ô ký người lập ghi '
                      '“Người tạo”.'),
   layout=dict(menu=MENU + ' => In phiếu', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
        ['- Từ danh sách: “Xem trước phiếu yêu cầu hạch toán bổ sung <số phiếu>”',
         '- Từ màn chi tiết: “Xem trước phiếu yêu cầu hạch toán bổ sung”', '- Có nút (x) đóng']),
       ('Nút In', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Cạnh tiêu đề cửa sổ', '- Khóa khi đang tải hoặc chưa có bản in', '- Bấm → mở hộp thoại in của trình duyệt']),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '“Đang tải dữ liệu in…” trong lúc dựng bản in.'),
       ('Đầu bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Letterhead của công ty ghi trên phiếu', '- Số phiếu, Ngày lập (dd/mm/yyyy), Loại yêu cầu']),
       ('Thân bản in', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- 2 loại Điều chỉnh công nợ: bảng Khách hàng (Nhà cung cấp), Hợp đồng bán (Hợp đồng mua), Số tiền, Ghi chú; tổng tiền',
         '- Loại Phối hợp kinh doanh: các dòng quyết toán theo phòng hỗ trợ',
         '- Loại khác: tối đa 5 dòng thông tin (đối tượng, chứng từ, số tiền, diễn giải…)']),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Theo mẫu', 'Theo mẫu in của hệ thống; ô ký người lập ghi “Người tạo”.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- ' + M_NOPERM_VIEW, '- “Không tìm thấy mẫu in "Yêu cầu hạch toán bổ sung" trên hệ thống”',
         '- “Không có dữ liệu để in”', '- “Không tải được dữ liệu in”'])],
   ev=[('Bấm In phiếu', 'Click',
        'Before:\n– Kiểm tra phiếu nằm trong phạm vi xem; sai → hiển thị ' + M_NOPERM_VIEW + ' trong cửa sổ.\n'
        'During:\n– Mở cửa sổ xem trước, hiện “Đang tải dữ liệu in…”; dựng bản in theo mẫu “Yêu cầu hạch toán bổ sung”, '
        'letterhead theo công ty của phiếu.\n'
        '– Thiếu mẫu in → “Không tìm thấy mẫu in "Yêu cầu hạch toán bổ sung" trên hệ thống”.\n' + ERR + '\n'
        'After:\n– Hiển thị bản in; mở khóa nút In. Không ghi dữ liệu, không ghi lịch sử.'),
       ('Bấm In', 'Click',
        'Before:\n– Bản in đã tải xong.\nDuring:\n– Dựng trang in ẩn với đúng nội dung xem trước.\n'
        'After:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Dọn trang in ẩn.\nAfter:\n– Đóng cửa sổ xem trước.')])

# ------------------------------------------------------------ 2.14
fr(14, 'Xuất Excel', usecase=('FR-14', 'Xuất Excel', 'io', A_LAP),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Xuất danh sách hoặc một phiếu ra Excel',
              mota='Xuất danh sách: người dùng chọn trường và thứ tự cột trong cửa sổ “Chọn trường xuất file” rồi tải file '
                   'gồm toàn bộ phiếu khớp bộ lọc và phạm vi (không riêng trang đang xem). Xuất một phiếu: tải file Excel '
                   'chứng từ của phiếu từ nút Xuất Excel ở cột Hành động (hoặc trong nút “…”) hoặc ở màn chi tiết.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm Xuất Excel trên thanh công cụ của bảng.\n'
                    '2. Hệ thống mở cửa sổ “Chọn trường xuất file” với 15 trường, tích sẵn đúng các cột đang hiện trên bảng.\n'
                    '3. Người dùng tích / bỏ tích, kéo đổi thứ tự, bấm Xuất file.\n'
                    '4. Hệ thống đóng cửa sổ, lấy toàn bộ phiếu theo bộ lọc + phạm vi quyền (chế độ chờ duyệt xuất đúng '
                    'phạm vi chờ duyệt), dựng file với letterhead công ty.\n'
                    '5. Hệ thống tải file “Danh-sach-yeu-cau-hach-toan-bo-sung-<ngày>.xlsx”, hiển thị “Xuất Excel thành công”.',
              phu='• Một phiếu: nút Xuất Excel ở cột Hành động (hoặc trong nút “…”) hoặc ở màn chi tiết → tải '
                  '“Yeu-cau-hach-toan-bo-sung-<số phiếu>.xlsx”.\n'
                  '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → không xuất.\n'
                  '• Không có phiếu khớp bộ lọc → vẫn xuất file có tiêu đề cột.\n'
                  '• Lỗi → “Lỗi khi xuất Excel danh sách” / “Lỗi khi xuất Excel”; một phiếu ngoài phạm vi → không tải.',
              dacbiet='Khóa nút Xuất Excel (nhãn “Đang xuất...”) trong lúc chờ file để tránh bấm liên tiếp.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Chọn trường xuất file”', 'Kèm nút (x) đóng.'),
       ('Danh sách trường', 'Table/Grid', 'Enable', '15 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        ['- Số phiếu, Loại yêu cầu, KH/NCC, Số tiền, Loại tiền, Diễn giải', '- Người tạo, Phòng ban, Ngày tạo, Ngày gửi',
         '- Người duyệt, Ngày duyệt, Trạng thái, Người cập nhật, Ngày cập nhật',
         '- Mặc định tích đúng các cột đang hiện trên bảng']),
       ('Ô tích của trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Theo cột đang hiện', 'Tích: trường có trong file.'),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Chữ gợi ý “Kéo để đổi vị trí cột trong file”', '- Thứ tự trong danh sách = thứ tự cột trong file']),
       ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn n/15 trường”.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi trường.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Khóa khi chưa tích trường nào hoặc đang xuất', '- Bấm → đóng cửa sổ, tải file']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
       ('Nút Xuất Excel của một phiếu', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Cột Hành động (hoặc trong nút “…”) hoặc chân màn chi tiết', '- Bấm → tải ngay file của phiếu, không mở cửa sổ chọn trường']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Xuất Excel thành công”', '- Lỗi danh sách: “Lỗi khi xuất Excel danh sách”',
         '- Lỗi một phiếu: “Lỗi khi xuất Excel”'])],
   ev=[('Bấm Xuất Excel trên thanh công cụ', 'Click',
        'Before:\n– Nút khóa khi đang có lượt xuất chạy.\n'
        'During:\n– Lấy danh sách 15 trường từ máy chủ, tích sẵn các cột đang hiện.\n'
        'After:\n– Mở cửa sổ “Chọn trường xuất file”.'),
       ('Kéo tay nắm', 'Drag',
        'Before:\n– Áp cho mọi trường.\nDuring:\n– Đổi thứ tự trường.\nAfter:\n– Thứ tự mới là thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Ít nhất 1 trường được tích; khóa nút Xuất Excel, nhãn “Đang xuất...”.\n'
        'During:\n– Đóng cửa sổ; lấy toàn bộ phiếu theo bộ lọc + phạm vi quyền + chế độ (bỏ phân trang).\n'
        '– Dựng file với letterhead công ty của người xuất, các cột đúng thứ tự đã chọn.\n' + ERR + '\n'
        'After:\n– Tải file “Danh-sach-yeu-cau-hach-toan-bo-sung-<ngày>.xlsx”; hiển thị “Xuất Excel thành công”.\n'
        '– Lỗi → “Lỗi khi xuất Excel danh sách”; mở khóa nút.'),
       ('Bấm Xuất Excel của một phiếu', 'Click',
        'Before:\n– Kiểm tra phiếu nằm trong phạm vi xem; ngoài phạm vi → không tải.\n'
        'During:\n– Dựng file chứng từ của phiếu (letterhead công ty ghi trên phiếu, nội dung như bản in).\n' + ERR + '\n'
        'After:\n– Tải file “Yeu-cau-hach-toan-bo-sung-<số phiếu>.xlsx”; hiển thị “Xuất Excel thành công”.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không xuất.\nAfter:\n– Đóng cửa sổ.')])

# ------------------------------------------------------------ 2.15
fr(15, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(ten='Xem lịch sử thay đổi của phiếu',
              mota='Xem các mốc thao tác trên một phiếu: Tạo mới, Thay đổi thông tin (trường cũ → mới, dòng chi tiết thêm / '
                   'bỏ, file đính kèm), Thay đổi trạng thái (gửi duyệt, từ chối kèm lý do), Xóa; mỗi mốc ghi người thực hiện '
                   'và thời điểm. Mở được từ nút Lịch sử ở cột Hành động hoặc khối Lịch sử ở màn chi tiết.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm nút Lịch sử ở cột Hành động (hoặc trong nút “…”), hoặc bấm Xem lịch sử ở màn chi tiết.\n'
                    '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <số phiếu>” (hoặc mở khối Lịch sử).\n'
                    '3. Hệ thống hiển thị các mốc, mới nhất trên cùng.\n'
                    '4. Người dùng bấm Bộ lọc để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.',
              phu='• Phiếu cũ tạo trước khi bật lịch sử → “Chưa có lịch sử thao tác nào.”.\n'
                  '• Lỗi tải → hiện câu lỗi kèm nút Thử lại.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng.',
              dacbiet=None),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', ['- “Lịch sử thay đổi: <số phiếu>”', '- Có nút (x) đóng']),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Mới nhất trên cùng', '- Mỗi mốc: nhãn hành động, thời điểm, “Người thực hiện: <tên>”']),
       ('Mốc Tạo mới', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Ghi khi lưu phiếu lần đầu (Lưu nháp hoặc Gửi duyệt).'),
       ('Mốc Thay đổi thông tin', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Trường đã đổi: giá trị cũ → mới', '- Dòng chi tiết thêm (+) / bỏ (-)', '- File đính kèm thêm / thay / xóa']),
       ('Mốc Thay đổi trạng thái', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Trạng thái cũ → mới', '- Từ chối: kèm lý do từ chối']),
       ('Mốc Xóa', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Ghi khi người lập xóa phiếu.'),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Mở / thu gọn vùng ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách', 'Trống',
        ['- Mặc định: trống (tất cả), gợi ý “Chọn loại hành động”', '- Lựa chọn: các hành động đã có của phiếu']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách', 'Trống',
        ['- Mặc định: trống (tất cả), gợi ý “Chọn người thực hiện”', '- Dạng “Tên - Mã phòng - Mã NV”']),
       ('Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', 'Gợi ý “Từ ngày”.'),
       ('Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', 'Gợi ý “Đến ngày”.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', 'Xóa các ô lọc lịch sử.'),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thao tác nào.”')],
   ev=[('Mở lịch sử', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem.\n'
        'During:\n– Nạp các mốc lịch sử và danh mục ô lọc (loại hành động, người thực hiện).\n'
        'After:\n– Hiển thị các mốc, mới nhất trên cùng; không có mốc → “Chưa có lịch sử thao tác nào.”.'),
       ('Đổi ô lọc lịch sử', 'Change',
        'Before:\n– Vùng ô lọc đang mở.\nDuring:\n– Lọc theo loại hành động, người thực hiện, khoảng ngày.\n'
        'After:\n– Hiển thị lại các mốc khớp điều kiện.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Xóa các ô lọc.\nAfter:\n– Hiển thị lại toàn bộ mốc.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không ghi gì.\nAfter:\n– Đóng cửa sổ.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu yêu cầu hạch toán bổ sung; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Trường theo loại yêu cầu', [
        '– Điều chỉnh công nợ khách hàng / nhà cung cấp: bảng Chi tiết hạch toán (≥ 1 dòng khi gửi duyệt); không có ô Số '
        'tiền, Diễn giải đầu phiếu; Số tiền phiếu = tổng dòng.',
        '– Hạch toán công nợ NCC bảo hành: chọn Phiếu xác nhận bảo hành, Nhà cung cấp và Số tiền tự điền.',
        '– Hạch toán công nợ NCC thiếu hàng: chọn Phiếu xử lý hàng thiếu, Số tiền tự điền; nhiều NCC thì chọn 1.',
        '– NCC hỗ trợ phát triển thị trường: chọn Nhà cung cấp.',
        '– Khác: chọn Đối tượng (Nhà cung cấp / Khách hàng / Nhân viên) rồi chọn đối tượng.',
        '– Phối hợp kinh doanh: chỉ phần chung (Số tiền, Loại tiền, Tỷ giá, Diễn giải).',
        '– Đổi loại xóa sạch các trường phụ thuộc loại, giữ Loại tiền, Tỷ giá, file.'], ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-02', 'Lưu nháp và Gửi duyệt', [
        '– Lưu nháp chỉ bắt buộc Loại yêu cầu; số nhập vào không được âm.',
        '– Gửi duyệt bắt buộc đủ trường theo loại, Loại tiền, Tỷ giá > 0, Số tiền > 0, ≥ 1 file đính kèm (màn Sửa: phiếu '
        'đã có file thì không bắt buộc thêm).',
        '– Gửi duyệt từ màn chi tiết kiểm lại: có dòng chi tiết (2 loại Điều chỉnh công nợ), Số tiền > 0, có file.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Gửi duyệt']),
    ('BR-03', 'Vòng đời trạng thái', [
        '– Lưu nháp → Đang tạo; Gửi duyệt → Chờ duyệt (ghi Ngày gửi).', '– Từ chối → về Đang tạo kèm Ghi chú duyệt.',
        '– Lưu phiếu kế toán → Đang duyệt; duyệt phiếu kế toán → Đã duyệt; xóa phiếu kế toán → về Chờ duyệt.',
        '– Chỉ 2 bước chuyển do màn này thực hiện: Đang tạo → Chờ duyệt, Chờ duyệt → Đang tạo.',
        '– Sửa / Xóa / Gửi duyệt: người lập, phiếu Đang tạo.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Gửi duyệt', 'Từ chối', 'Lập phiếu kế toán']),
    ('BR-04', 'Người xử lý theo loại', [
        '– Từ chối: Kế toán thanh toán, phiếu thuộc công ty mình (Phối hợp kinh doanh: công ty của phòng hỗ trợ).',
        '– Lập phiếu kế toán, mọi loại trừ Phối hợp kinh doanh: Kế toán thanh toán trong phạm vi công ty.',
        '– Lập phiếu kế toán loại Phối hợp kinh doanh: Kế toán của công ty có phòng hỗ trợ của phiếu.'],
     ['Từ chối', 'Lập phiếu kế toán']),
    ('BR-05', 'Phạm vi xem', ['– Xét quyền theo thứ tự V1 → V2 → V3 → V4; không có quyền nào thì chỉ phiếu mình lập.',
                              '– V2: theo công ty phiếu; Phối hợp kinh doanh theo công ty phòng hỗ trợ.',
                              '– Màn chờ duyệt luôn chỉ phiếu Chờ duyệt; người không có quyền kế toán chỉ thấy phiếu mình.',
                              '– Phiếu Đang tạo của người khác luôn ẩn.'],
     ['Xem danh sách', 'Xem chi tiết', 'In phiếu', 'Xuất Excel']),
    ('BR-06', 'Thông báo', ['– Gửi duyệt → người có quyền Kế toán kho cùng công ty với phiếu (“[HTBS] Chờ duyệt: <số phiếu>”).',
                            '– Từ chối → người lập kèm người từ chối, lý do (“[HTBS] Từ chối: <số phiếu>”).',
                            '– Duyệt phiếu kế toán → người lập phiếu yêu cầu.'],
     ['Gửi duyệt', 'Từ chối', 'Lập phiếu kế toán']),
    ('BR-07', 'Điều hướng sau thao tác', [
        '– Lưu nháp, Gửi duyệt từ form: về màn danh sách; Lưu và tiếp tục: ở lại màn Tạo với form trống.',
        '– Gửi duyệt, Từ chối từ màn chi tiết: ở lại, nạp lại màn chi tiết.',
        '– Xóa từ danh sách: nạp lại danh sách; Xóa từ màn chi tiết: về danh sách.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Gửi duyệt', 'Xóa', 'Từ chối']),
    ('BR-08', 'Không trùng dòng chi tiết', [
        '– Khi gửi duyệt, 2 dòng không được trùng cặp đối tượng – hợp đồng (“Hợp đồng này đã có ở dòng <n> với cùng '
        'đối tượng”).',
        '– Hợp đồng của dòng chỉ chọn được sau khi chọn đối tượng; đổi đối tượng xóa hợp đồng.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Chọn đối tượng và chứng từ']),
    ('BR-09', 'File đính kèm', [
        '– Chỉ nhận pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip; tối đa 20MB/file.',
        '– File tải lên ngay khi chọn nhưng chỉ gắn vào phiếu khi lưu; xóa file đã lưu có hiệu lực ngay và ghi lịch sử.'],
     ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-10', 'Chứng từ nguồn chọn được', [
        '– Phiếu xác nhận bảo hành: chỉ phiếu đã duyệt.', '– Phiếu xử lý hàng thiếu: chỉ phiếu đã duyệt, có hạch toán.',
        '– Nhân viên: chỉ nhân viên đang làm; khách hàng: mọi khách hàng đang hoạt động.'],
     ['Chọn đối tượng và chứng từ']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc dữ liệu do màn Phiếu yêu cầu hạch toán bổ sung ghi ra.')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Sổ tổng hợp', 'Phiếu kế toán — lập từ phiếu yêu cầu Chờ duyệt, cập nhật trạng thái phiếu yêu cầu',
     'Phân hệ Tài chính => Sổ tổng hợp => Phiếu kế toán'),
], widths=[0.45, 1.0, 2.6, 2.4])

d.save()
print('Đã ghi', OUT)

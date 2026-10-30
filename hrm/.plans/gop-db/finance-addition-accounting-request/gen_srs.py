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
TN_MOI = 'Người dùng có quyền thực hiện chức năng: mọi người dùng đã đăng nhập (không cần quyền riêng).'
TN_XEM = ('Người dùng có quyền thực hiện chức năng: người lập phiếu; người có một trong các quyền Xem phiếu yêu cầu hạch '
          'toán bổ sung - tổng công ty / - công ty / - phòng ban / - bộ phận; Kế toán thanh toán; Kế toán.')
TN_SUA = 'Người dùng có quyền thực hiện chức năng: người lập phiếu (không cần quyền riêng).'
TN_KT = 'Người dùng có quyền thực hiện chức năng: Kế toán thanh toán (loại 1–6); Kế toán của công ty phòng hỗ trợ (loại 7).'
DK_XEM = '1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Phiếu yêu cầu hạch toán bổ sung.'
DK_SUA = '1. Người dùng đăng nhập thành công.\n2. Người dùng là người lập phiếu.\n3. Phiếu đang ở trạng thái Đang tạo.'
DK_KT = ('1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán thanh toán (loại 1–6) hoặc Kế toán của công '
         'ty phòng hỗ trợ (loại 7), cùng phạm vi công ty.\n3. Phiếu đang ở trạng thái Chờ duyệt.')

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


# Mô tả riêng cho hàng sau khi tách dòng gộp (srs_split_rows) — mỗi đối tượng 1 hàng.
UI_OVER = {
    'Nút Xuất Excel': 'Mở cửa sổ Chọn trường xuất file (FR-14).',
    'Nút Cấu hình cột hiển thị': 'Mở cửa sổ Tùy chỉnh cột (FR-04).',
    'Cột STT': 'Cột khóa, đánh số liên tục theo trang.',
    'Cột Số phiếu': ['- Cột khóa', '- Bấm Số phiếu → màn chi tiết (FR-10)', '- Sắp xếp được'],
    'Cột Người tạo': 'Người lập phiếu, dạng “Họ tên - Mã phòng ban”.',
    'Cột Phòng ban': 'Phòng ban của người lập lúc lập phiếu.',
    'Cột Người duyệt': 'Kế toán đã từ chối / lập phiếu kế toán.',
    'Cột Người cập nhật': {'init': 'Ẩn', 'desc': ['- Người sửa phiếu gần nhất', '- Ẩn mặc định; bật trong Tùy chỉnh cột']},
    'Cột Ngày tạo': 'Sắp xếp được.',
    'Cột Ngày gửi': ['- Thời điểm gửi duyệt', '- Sắp xếp được'],
    'Cột Ngày duyệt': ['- Thời điểm kế toán xử lý', '- Sắp xếp được'],
    'Cột Ngày cập nhật': {'init': 'Ẩn', 'desc': ['- Thời điểm sửa phiếu gần nhất', '- Sắp xếp được',
                                                '- Ẩn mặc định; bật trong Tùy chỉnh cột']},
    'Công ty': {'scope': 'Danh sách công ty', 'desc': 'Chỉ hiện với V1.'},
    ('Công ty / Phòng ban', 'Phòng ban'): {'scope': 'Danh sách phòng ban', 'desc': [
        '- Hiện theo cấp quyền xem', '- Chỉ còn phòng ban của Công ty đã chọn', '- Đổi Công ty thì bị xóa']},
    ('Người tạo / Người duyệt', 'Người tạo'): 'Người lập phiếu.',
    ('Người tạo / Người duyệt', 'Người duyệt'): 'Kế toán đã xử lý phiếu.',
    ('Nút Xóa / Hủy', 'Nút Xóa'): 'Xác nhận xóa phiếu.',
    'Thông tin chung': 'Loại yêu cầu và các trường theo loại, Loại tiền, Tỷ giá, Diễn giải, Ghi chú duyệt — chỉ đọc.',
    'Chi tiết hạch toán': 'Với 2 loại Điều chỉnh công nợ: STT, đối tượng, hợp đồng, Số tiền, Ghi chú, dòng Tổng cộng — chỉ đọc.',
    'File đính kèm': 'STT, tên file (xem / tải), Dung lượng.',
    ('Nút Sửa / Gửi duyệt / Xóa', 'Nút Sửa'): 'Mở màn Sửa; người lập, phiếu Đang tạo.',
    ('Nút Sửa / Gửi duyệt / Xóa', 'Nút Gửi duyệt'): 'Gửi kế toán (FR-08); người lập, phiếu Đang tạo.',
    ('Nút Sửa / Gửi duyệt / Xóa', 'Nút Xóa'): 'Mở hộp Xác nhận xóa; người lập, phiếu Đang tạo.',
    'Nút In phiếu': 'Mở cửa sổ xem trước bản in (FR-13).',
    ('Nút In phiếu / Xuất Excel / Quay lại', 'Nút Xuất Excel'): 'Tải file Excel của phiếu (FR-14).',
    ('Nút Từ chối / Hủy', 'Nút Từ chối'): 'Xác nhận từ chối (màu đỏ).',
    ('Nút Chọn tất cả / Bỏ chọn hết / Xuất file / Đóng', 'Nút Đóng'): 'Đóng cửa sổ, không xuất.',
}
_TB = lambda n, desc: (n, 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', desc)  # noqa: E731
_GR = lambda n, desc: (n, 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', desc)  # noqa: E731
UI_EXPLICIT = {
    'Ô tìm kiếm': [
        _TB('Ô Tên hoặc mã khách hàng', 'Cửa sổ Chọn khách hàng: tìm theo tên hoặc mã chứa chuỗi nhập.'),
        _TB('Ô Mã số thuế', 'Cửa sổ Chọn khách hàng: tìm theo mã số thuế.'),
        _TB('Ô Số điện thoại', 'Cửa sổ Chọn khách hàng: tìm theo số điện thoại.'),
        _TB('Ô Số đơn hàng/Hợp đồng', 'Cửa sổ Chọn hợp đồng: tìm theo số hợp đồng chứa chuỗi nhập.'),
    ],
    'Bảng kết quả': [
        _GR('Bảng khách hàng', 'Mã KH - Tên khách hàng, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP; bấm dòng để chọn.'),
        _GR('Bảng hợp đồng', 'Số đơn hàng/Hợp đồng, Ngày lập, Giá trị hợp đồng, Số tiền còn nợ; bấm dòng để chọn.'),
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu yêu cầu hạch toán bổ sung (mã phiếu PYCHTBS-NNNNNN), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng duyệt của màn hình.',
    'Làm rõ 7 loại yêu cầu và các trường riêng của từng loại.',
    'Làm rõ ai từ chối / lập phiếu kế toán theo từng loại (Kế toán thanh toán với loại 1–6, Kế toán của công ty phòng hỗ trợ '
    'với loại 7 Phối hợp kinh doanh).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu yêu cầu hạch toán bổ sung', 'Phiếu đề nghị kế toán hạch toán bổ sung một khoản công nợ, mã PYCHTBS-NNNNNN.'),
    ('Loại yêu cầu', 'Điều chỉnh công nợ khách hàng · Điều chỉnh công nợ nhà cung cấp · Hạch toán công nợ NCC bảo hành · '
                     'Hạch toán công nợ NCC thiếu hàng · NCC hỗ trợ phát triển thị trường · Khác · Phối hợp kinh doanh.'),
    ('Chi tiết hạch toán', 'Bảng dòng (Khách hàng / NCC, Hợp đồng, Số tiền, Ghi chú) của 2 loại Điều chỉnh công nợ; số tiền '
                           'phiếu = tổng các dòng.'),
    ('Phiếu xác nhận bảo hành / Phiếu xử lý hàng thiếu', 'Chứng từ nguồn của loại Hạch toán công nợ NCC bảo hành / thiếu hàng.'),
    ('Phiếu kế toán', 'Phiếu kế toán điều chỉnh công nợ do kế toán lập từ phiếu yêu cầu để ghi sổ.'),
    ('Đang tạo / Chờ duyệt / Đang duyệt / Đã duyệt', 'Các trạng thái của phiếu. Từ chối đưa phiếu về Đang tạo kèm Ghi chú duyệt.'),
], widths=[2.1, 3.9])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Lập phiếu không cần quyền riêng. Sửa / Xóa / Gửi duyệt: chỉ người lập, khi phiếu Đang tạo.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Kế toán thanh toán', 'Màn chờ duyệt; với phiếu loại 1–6 Chờ duyệt trong phạm vi công ty: Từ chối, Lập phiếu kế toán.'),
    ('Q2', 'Kế toán', 'Màn chờ duyệt; với phiếu loại 7 Chờ duyệt có phòng hỗ trợ thuộc công ty mình: Lập phiếu kế toán.'),
    ('Q3', 'Kế toán kho', 'Nhận thông báo khi có phiếu gửi duyệt.'),
], widths=[0.8, 1.6, 3.6])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (xét từ trên xuống, có cấp nào áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu yêu cầu hạch toán bổ sung - tổng công ty', 'Toàn bộ phiếu.'),
    ('V2', 'Xem phiếu yêu cầu hạch toán bổ sung - công ty',
     'Phiếu loại 1–6 thuộc công ty mình; phiếu loại 7 có phòng hỗ trợ thuộc công ty mình.'),
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
    ('FR-12 Lập phiếu kế toán', '❌', '✅ (loại 1–6)', '✅ (loại 7)', '❌', '❌'),
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

FORM_UI = [
    ('Người lập – Ngày lập', 'Label', 'Read-only', '–', '–', 'Người đăng nhập – thời điểm hiện tại', 'Góc phải khối Thông tin chung.'),
    ('Loại yêu cầu', 'Dropdown', 'Enable', '7 loại', 'Có', 'Trống', [
        '- Gợi ý “Chọn loại yêu cầu”', '- Đổi loại → xóa sạch các trường phụ thuộc loại (Đối tượng, chứng từ, bảng chi tiết)']),
    ('Phiếu xác nhận bảo hành', 'Textbox', 'Enable / Ẩn', '–', 'Có (loại Hạch toán công nợ NCC bảo hành)', 'Trống',
     'Bấm ô → popup chọn phiếu; chọn xong tự điền Nhà cung cấp và Số tiền (chỉ đọc).'),
    ('Phiếu xử lý hàng thiếu', 'Textbox', 'Enable / Ẩn', '–', 'Có (loại Hạch toán công nợ NCC thiếu hàng)', 'Trống',
     'Bấm ô → popup chọn phiếu; 1 NCC tự điền, nhiều NCC thì chọn trong danh sách.'),
    ('Nhà cung cấp', 'Dropdown', 'Enable / Ẩn', '–', 'Có (loại NCC hỗ trợ / thiếu hàng)', 'Trống', 'Gợi ý “Chọn nhà cung cấp”.'),
    ('Đối tượng', 'Dropdown', 'Enable / Ẩn', 'Nhà cung cấp / Khách hàng / Nhân viên', 'Có (loại Khác)', 'Trống',
     'Chọn xong hiện ô chọn đối tượng tương ứng (popup).'),
    ('Số tiền', 'Textbox', 'Enable / Ẩn', '> 0', 'Có (loại 1, 3, 4, 5)', 'Trống',
     ['- Gợi ý “Nhập số tiền”', '- Ẩn với 2 loại Điều chỉnh công nợ (lấy tổng bảng chi tiết)']),
    ('Loại tiền', 'Dropdown', 'Enable', 'Danh mục tiền tệ', 'Có', 'VNĐ', '–'),
    ('Tỷ giá', 'Textbox', 'Enable', '> 0', 'Có', '1', 'Gợi ý “Nhập tỷ giá”.'),
    ('Diễn giải', 'Textarea', 'Enable / Ẩn', '–', 'Có (loại 1, 3, 4, 5)', 'Trống',
     ['- Gợi ý “Nhập diễn giải”', '- Ẩn với 2 loại Điều chỉnh công nợ (ghi chú ở từng dòng)']),
    ('Bảng Chi tiết hạch toán', 'Table/Grid', 'Enable / Ẩn', '–', 'Có (2 loại Điều chỉnh công nợ)', '“Chưa có dòng”', [
        '- Nút Thêm dòng; cột STT, Khách hàng / Nhà cung cấp, Hợp đồng bán / Hợp đồng mua, Số tiền, Ghi chú, Xóa dòng',
        '- Bấm ô đối tượng / hợp đồng → popup chọn (FR-06); hợp đồng khóa khi chưa chọn đối tượng',
        '- Dòng Tổng cộng']),
    ('File đính kèm', 'Table/Grid', 'Enable', 'Nhiều file', 'Có (≥ 1 file khi gửi duyệt)', 'Chưa có file',
     ['- Nút Thêm tài liệu; bảng STT, Upload / File, Dung lượng', '- Gửi duyệt thiếu: “Phiếu chưa có file đính kèm”']),
    ('Ghi chú duyệt', 'Textarea', 'Read-only', '–', '–', 'Ẩn', 'Lý do từ chối lần trước, hiện khi có.'),
    ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu Đang tạo; chỉ bắt buộc Loại yêu cầu.'),
    ('Nút Gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu Chờ duyệt; kiểm tra đủ bắt buộc.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về danh sách; hỏi xác nhận nếu có thay đổi chưa lưu.'),
]

SAVE_EV = [
    ('Đổi Loại yêu cầu', 'Change', 'After:\n– Ẩn / hiện trường theo loại; xóa sạch giá trị của các trường phụ thuộc loại cũ.'),
    ('Bấm Lưu nháp / Gửi duyệt', 'Click',
     'Before:\n– Sửa: chỉ người lập, phiếu Đang tạo; sai → “Bạn không có quyền sửa phiếu này”.\n'
     'During:\n– Lưu nháp: chỉ bắt buộc Loại yêu cầu (số tiền không được âm).\n'
     '– Gửi duyệt: ô trống → “Bắt buộc phải nhập” tại từng ô (Loại tiền, Tỷ giá, Số tiền, Diễn giải, chứng từ / đối tượng '
     'theo loại); Số tiền, Tỷ giá phải > 0.\n'
     '– Loại Điều chỉnh công nợ: “Phiếu chưa có dòng chi tiết nào, không gửi duyệt được”; mỗi dòng bắt buộc đối tượng, hợp '
     'đồng, số tiền > 0, ghi chú.\n'
     '– “Số tiền của phiếu phải lớn hơn 0”, “Phiếu chưa có file đính kèm”.\n' + ERR + '\n'
     'After:\n– Lập mới: sinh mã PYCHTBS-NNNNNN; công ty, phòng ban, bộ phận theo người lập.\n'
     '– Ghi nhận trong lịch sử (Tạo mới / Thay đổi thông tin; gửi duyệt ghi Thay đổi trạng thái).\n'
     '– Gửi duyệt: ghi Ngày gửi, báo “[HTBS] Chờ duyệt: <số phiếu>” cho Kế toán kho.\n'
     '– Báo “Lưu thành công” / “Gửi duyệt thành công”, về màn danh sách.'),
    ('Bấm Quay lại / rời màn', 'Click', 'Before:\n– Có thay đổi chưa lưu → hỏi xác nhận rời trang.\nAfter:\n– Về màn danh sách.'),
]

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu yêu cầu hạch toán bổ sung',
       mota='Hiển thị phiếu trong phạm vi quyền. Có 2 chế độ: danh sách chung và danh sách chờ duyệt.',
       tacnhan=TN_XEM, dieukien='1. Người dùng đăng nhập thành công.',
       chinh='1. Vào một trong các lối vào ở mục Layout.\n2. Hệ thống xác định chế độ, áp phạm vi dữ liệu.\n'
             '3. Hiển thị trang đầu, mới tạo xếp trên.',
       phu='• Chế độ chờ duyệt: luôn chỉ phiếu Chờ duyệt; không có nút Tạo mới; không có quyền kế toán thì chỉ phiếu của mình.\n'
           '• Phiếu Đang tạo của người khác không hiện.',
       dacbiet=None),
   layout=dict(entries=[
       (MENU, 'Hiển thị: tiêu đề “Phiếu yêu cầu hạch toán bổ sung”; phiếu trong phạm vi quyền (Phần 2).'),
       (MENU_SALE, 'Hiển thị: giống lối vào trên.'),
       (MENU_CD, 'Hiển thị: tiêu đề “Phiếu yêu cầu hạch toán bổ sung chờ duyệt”; phiếu Chờ duyệt — Kế toán thanh toán / Kế '
                 'toán thấy theo công ty hoặc phòng hỗ trợ, người khác chỉ thấy phiếu của mình.')],
       shot=shot('01_list'), shot_caption='Màn danh sách Phiếu yêu cầu hạch toán bổ sung'),
   ui_kw=dict(required=False),
   ui=[
       ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', 'Ẩn ở chế độ chờ duyệt.'),
       ('Nút Xuất Excel / Cấu hình cột hiển thị', 'Button', 'Enable', '–', 'Hiển thị', 'FR-14 / FR-04.'),
       ('Cột STT / Số phiếu', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Cột khóa', '- Bấm Số phiếu → màn chi tiết']),
       ('Cột Loại yêu cầu', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Tên loại.'),
       ('Cột KH / NCC', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Đối tượng của phiếu (loại có bảng chi tiết: đối tượng các dòng).'),
       ('Cột Số tiền', 'Table/Grid', 'Read-only', '≥ 0', 'Hiển thị', 'Kèm đơn vị tiền; sắp xếp được.'),
       ('Cột Diễn giải', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '–'),
       ('Cột Người tạo / Phòng ban / Người duyệt / Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Người cập nhật ẩn mặc định.'),
       ('Cột Ngày tạo / Ngày gửi / Ngày duyệt / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        'Sắp xếp được; Ngày cập nhật ẩn mặc định.'),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Đang tạo: xám', '- Chờ duyệt, Đang duyệt: vàng', '- Đã duyệt: xanh']),
       ('Cột Hành động', 'Table/Grid', 'Read-only', '–', 'Hiển thị', [
           '- Sửa, Xóa: người lập, phiếu Đang tạo', '- Lập phiếu kế toán: kế toán đủ điều kiện (FR-12)',
           '- In phiếu; nút ba chấm: Xuất Excel, Lịch sử']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Dòng “Hiển thị a–b / N”, Số dòng/trang.'),
   ],
   ev=[('Mở màn hình', 'System', 'Before:\n– Xác định chế độ theo lối vào.\nAfter:\n– Hiển thị trang 1, mới tạo xếp trên.'),
       ('Bấm Số phiếu', 'Click', 'After:\n– Mở màn chi tiết.'),
       ('Bấm tiêu đề cột sắp xếp được', 'Click', 'After:\n– Sắp xếp lại, về trang 1.')])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(ten='Tìm kiếm và lọc danh sách phiếu', mota='Thu hẹp danh sách theo 9 tiêu chí.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Nhập số phiếu vào ô tìm nhanh, bấm Tìm kiếm; hoặc Tìm kiếm nâng cao.\n2. Chọn / nhập tiêu chí.\n3. Nạp lại danh sách.',
              phu='• Làm mới → xóa mọi tiêu chí.', dacbiet=None),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'), shot_caption='Khối Bộ lọc danh sách'),
   ui=[('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Gợi ý “Tìm theo số phiếu...”.'),
       ('Công ty / Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Theo quyền', 'Không', 'Trống', 'Hiện theo cấp quyền xem.'),
       ('Loại yêu cầu', 'Dropdown', 'Enable', '7 loại', 'Không', 'Trống', '–'),
       ('Trạng thái', 'Dropdown', 'Enable', 'Đang tạo, Chờ duyệt, Đang duyệt, Đã duyệt', 'Không', 'Trống', '–'),
       ('Khách hàng / Nhà cung cấp', 'Dropdown', 'Enable', 'Gõ để tìm', 'Không', 'Trống', 'Khớp đối tượng phiếu hoặc đối tượng các dòng.'),
       ('Diễn giải', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Khớp diễn giải phiếu hoặc ghi chú các dòng.'),
       ('Phiếu xác nhận bảo hành', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
       ('Người tạo / Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', '–'),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Từ ngày → đến ngày.')],
   ev=[('Đổi ô lọc nâng cao', 'Change', 'After:\n– Về trang 1, nạp lại.'), ('Bấm Tìm kiếm', 'Click', 'After:\n– Áp ô tìm nhanh.'),
       ('Bấm Làm mới', 'Click', 'After:\n– Xóa mọi tiêu chí.')])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị', mota='Bật / tắt, sắp thứ tự ô lọc; lưu theo người dùng.',
              tacnhan=TN_XEM, dieukien=DK_XEM, chinh='1. Bấm Cài đặt bộ lọc.\n2. Tích / bỏ tích, kéo đổi thứ tự.\n3. Bấm Lưu.',
              phu='• Khôi phục mặc định / Đóng.', dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Danh sách ô lọc', 'Table/Grid', 'Enable', '9 mục', '–', 'Theo cấu hình',
        'Công ty – Phòng ban, Loại yêu cầu, Trạng thái, Khách hàng / Nhà cung cấp, Diễn giải, Phiếu xác nhận bảo hành, '
        'Người tạo, Người duyệt, Ngày tạo.'),
       ('Nút Lưu / Khôi phục mặc định / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–')],
   ev=[('Kéo đổi vị trí', 'Drag', 'After:\n– Đổi thứ tự.'), ('Bấm Lưu', 'Click', 'After:\n– Lưu theo người dùng.')])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Tùy chỉnh cột của bảng danh sách', mota='Bật / tắt, kéo sắp xếp 16 cột; STT, Số phiếu, Hành động khóa.',
              tacnhan=TN_XEM, dieukien=DK_XEM, chinh='1. Bấm Cấu hình cột hiển thị.\n2. Tích / bỏ tích, kéo.\n3. Bấm Lưu.',
              phu='• Đóng → bỏ thay đổi.', dacbiet='Mặc định ẩn Ngày cập nhật, Người cập nhật.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Danh sách cột', 'Table/Grid', 'Enable', '16 cột', '–', 'Theo cấu hình',
        'STT, Số phiếu, Loại yêu cầu, KH / NCC, Số tiền, Diễn giải, Người tạo, Ngày tạo, Phòng ban, Ngày gửi, Người duyệt, '
        'Ngày duyệt, Trạng thái, Ngày cập nhật, Người cập nhật, Hành động.'),
       ('Nút Chọn tất cả / Bỏ chọn hết / Lưu / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–')],
   ev=[('Kéo biểu tượng ba gạch', 'Drag', 'After:\n– Đổi thứ tự cột.'), ('Bấm Lưu', 'Click', 'After:\n– Lưu, vẽ lại bảng.')])

# ------------------------------------------------------------ 2.5
fr(5, 'Lập phiếu yêu cầu hạch toán bổ sung', usecase=('FR-05', 'Lập phiếu', 'crud', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Lập phiếu yêu cầu hạch toán bổ sung',
       mota='Chọn loại yêu cầu, nhập các trường theo loại, đính kèm file; lưu nháp hoặc gửi duyệt.',
       tacnhan=TN_MOI, dieukien='1. Người dùng đăng nhập thành công.',
       chinh='1. Bấm Tạo mới.\n2. Hệ thống mở màn “Tạo phiếu yêu cầu hạch toán bổ sung”.\n3. Chọn Loại yêu cầu.\n'
             '4. Nhập trường theo loại: loại Điều chỉnh công nợ thêm dòng ở bảng Chi tiết hạch toán; loại khác chọn chứng từ / '
             'đối tượng, nhập Số tiền, Diễn giải.\n5. Chọn Loại tiền, Tỷ giá; đính kèm file.\n6. Bấm Lưu nháp hoặc Gửi duyệt.\n'
             '7. Hệ thống kiểm tra, sinh mã, lưu, ghi lịch sử; gửi duyệt thì báo Kế toán kho.\n8. Báo thành công, về danh sách.',
       phu='• Lỗi kiểm tra → báo đỏ tại từng ô.\n• Lưu và tiếp tục → lưu nháp rồi mở form trống.',
       dacbiet='Loại Phối hợp kinh doanh thường do màn Quyết toán hợp đồng bán sinh ra; phiếu nhập tay vẫn dùng chung bố cục chi tiết.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10e_filled'),
               shot_caption='Màn Tạo phiếu — loại Điều chỉnh công nợ khách hàng đã thêm dòng'),
   ui=FORM_UI + [('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Chỉ ở màn Tạo.')],
   ev=SAVE_EV)

# ------------------------------------------------------------ 2.6
fr(6, 'Chọn đối tượng và chứng từ', usecase=('FR-06', 'Chọn đối tượng và chứng từ', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(ten='Chọn khách hàng / nhà cung cấp / nhân viên, hợp đồng và chứng từ nguồn',
              mota='Các cửa sổ chọn: Khách hàng, Nhà cung cấp, Nhân viên, Hợp đồng bán / mua, Phiếu xác nhận bảo hành, Phiếu xử lý hàng thiếu.',
              tacnhan=TN_MOI, dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo / Sửa phiếu.',
              chinh='1. Bấm vào ô cần chọn.\n2. Hệ thống mở cửa sổ tương ứng.\n3. Tìm, bấm dòng cần chọn.\n4. Hệ thống điền ô và các ô phụ thuộc.',
              phu='• Ô hợp đồng khi chưa chọn đối tượng → bị khóa.\n• Không có dữ liệu → “Không có hợp đồng phù hợp.”.\n• Bấm Đóng → không chọn.',
              dacbiet='Hợp đồng bán: hợp đồng HRM, hợp đồng dịch vụ BH-SC, hợp đồng bán đầu kỳ. Phiếu xác nhận bảo hành: trạng thái đã xác nhận; '
                      'phiếu xử lý hàng thiếu: đã duyệt, có hạch toán.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('11_customer'), shot_caption='Cửa sổ Chọn khách hàng',
               note='Các cửa sổ chọn được mở ngay trên màn hình Tạo / Sửa phiếu theo đường dẫn ở trên.'),
   ui=[('Ô tìm kiếm', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Khách hàng: Tên / Mã, MST, SĐT; hợp đồng: Số đơn hàng/Hợp đồng.'),
       ('Bảng kết quả', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', [
           '- Khách hàng: Mã KH - Tên, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP',
           '- Hợp đồng: Số đơn hàng/Hợp đồng, Ngày lập, Giá trị hợp đồng, Số tiền còn nợ']),
       ('Nút Tìm kiếm / Làm mới / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1', '–')],
   ev=[('Bấm một dòng', 'Click', 'After:\n– Điền ô; chứng từ nguồn thì tự điền NCC và Số tiền; đổi đối tượng thì xóa hợp đồng cũ.')])

# ------------------------------------------------------------ 2.7
fr(7, 'Chỉnh sửa phiếu', usecase=('FR-07', 'Chỉnh sửa phiếu', 'crud', A_LAP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(ten='Chỉnh sửa phiếu yêu cầu hạch toán bổ sung', mota='Người lập sửa phiếu Đang tạo (kể cả phiếu bị từ chối trả về).',
              tacnhan=TN_SUA, dieukien=DK_SUA,
              chinh='1. Bấm Sửa ở cột Hành động hoặc màn chi tiết.\n2. Hệ thống mở màn “Sửa phiếu yêu cầu hạch toán bổ sung: <số phiếu>”.\n'
                    '3. Sửa (quy tắc như FR-05).\n4. Lưu nháp hoặc Gửi duyệt.\n5. Ghi Thay đổi thông tin trong lịch sử, về danh sách.',
              phu='• Phiếu bị từ chối hiện Ghi chú duyệt (lý do).', dacbiet=None),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('19_edit'), shot_caption='Màn Sửa phiếu yêu cầu hạch toán bổ sung'),
   ui=FORM_UI, ev=SAVE_EV)

# ------------------------------------------------------------ 2.8
fr(8, 'Gửi duyệt phiếu', usecase=('FR-08', 'Gửi duyệt', 'action', A_LAP),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(ten='Gửi duyệt từ màn chi tiết', mota='Người lập gửi phiếu Đang tạo mà không mở form Sửa.',
              tacnhan=TN_SUA, dieukien=DK_SUA,
              chinh='1. Mở chi tiết, bấm Gửi duyệt.\n2. Hệ thống kiểm tra như FR-05.\n3. Phiếu Chờ duyệt, ghi Ngày gửi, lịch sử, báo Kế toán kho.\n'
                    '4. Hiện “Gửi duyệt thành công”.',
              phu='• Thiếu dữ liệu → báo lỗi, phiếu giữ Đang tạo.', dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết => Gửi duyệt', shot=shot('19_edit'), shot_caption='Phiếu Đang tạo — nút Gửi duyệt ở chân màn'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Gửi duyệt', 'Button', 'Enable / Ẩn', 'Ẩn', 'Người lập, phiếu Đang tạo.')],
   ev=[('Bấm Gửi duyệt', 'Click', 'Before:\n– Kiểm tra người lập, trạng thái; sai → “Bạn không có quyền gửi duyệt phiếu này”.\n'
        'During:\n– Kiểm tra như FR-05.\n' + ERR + '\nAfter:\n– Chờ duyệt; ghi Thay đổi trạng thái; báo Kế toán kho.')])

# ------------------------------------------------------------ 2.9
fr(9, 'Xóa phiếu', usecase=('FR-09', 'Xóa phiếu', 'action', A_LAP),
   rule=('- Quy tắc Xóa và Thông báo.', 'delete'),
   intro=dict(ten='Xóa phiếu yêu cầu hạch toán bổ sung', mota='Người lập xóa phiếu Đang tạo.',
              tacnhan=TN_SUA, dieukien=DK_SUA,
              chinh='1. Bấm Xóa ở cột Hành động hoặc màn chi tiết.\n2. Hộp “Xác nhận xóa”.\n3. Bấm Xóa.\n4. Xóa phiếu, ghi lịch sử, báo “Xóa thành công”.',
              phu='• Bấm Hủy → không xóa.\n• Không phải người lập → “Bạn không có quyền xóa phiếu này”.', dacbiet=None),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp xác nhận xóa phiếu',
               note='Modal Xác nhận xóa được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nội dung', 'Label', 'Hiển thị', '–', '“Bạn có chắc muốn xóa phiếu yêu cầu hạch toán bổ sung \'<số phiếu>\'?”'),
       ('Nút Xóa / Hủy', 'Button', 'Enable', 'Hiển thị', 'Xác nhận / đóng hộp.')],
   ev=[('Bấm Xóa', 'Click', 'Before:\n– Kiểm tra người lập, trạng thái.\n' + ERR + '\nAfter:\n– Xóa phiếu, dòng chi tiết; báo thành công.')])

# ------------------------------------------------------------ 2.10
fr(10, 'Xem chi tiết phiếu', usecase=('FR-10', 'Xem chi tiết phiếu', 'view', A_LAP),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(ten='Xem chi tiết phiếu yêu cầu hạch toán bổ sung', mota='Xem phiếu chỉ đọc; bố cục theo loại yêu cầu.',
              tacnhan=TN_XEM, dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu trong phạm vi xem.',
              chinh='1. Bấm Số phiếu.\n2. Hệ thống mở màn “Chi tiết phiếu yêu cầu hạch toán bổ sung: <số phiếu>”.',
              phu='• Ngoài phạm vi → “Bạn không có quyền xem phiếu này”.',
              dacbiet='Loại Phối hợp kinh doanh hiển thị khối riêng: Khách hàng, Phòng thực hiện, Phòng hỗ trợ, Gửi tới công ty, '
                      'Số hợp đồng, Nội dung quyết toán, Số lượng hạch toán theo phòng ban / nhân viên.'),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn chi tiết phiếu Chờ duyệt — loại Điều chỉnh công nợ khách hàng'),
   ui_kw=dict(required=False),
   ui=[('Thông tin chung / Chi tiết hạch toán / File đính kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Như màn Tạo, chỉ đọc.'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', 'Xem lịch sử (FR-15).'),
       ('Nút Sửa / Gửi duyệt / Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Người lập, phiếu Đang tạo.'),
       ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Kế toán thanh toán, phiếu Chờ duyệt.'),
       ('Nút Lập phiếu kế toán', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Theo FR-12.'),
       ('Nút In phiếu / Xuất Excel / Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '–')],
   ev=[('Mở màn chi tiết', 'System', 'Before:\n– Kiểm tra phạm vi.\nAfter:\n– Hiển thị theo loại, nút theo điều kiện.')])

# ------------------------------------------------------------ 2.11
fr(11, 'Từ chối phiếu', usecase=('FR-11', 'Từ chối phiếu', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(ten='Từ chối phiếu yêu cầu hạch toán bổ sung', mota='Kế toán thanh toán trả phiếu về Đang tạo, bắt buộc lý do.',
              tacnhan='Người dùng có quyền thực hiện chức năng: Kế toán thanh toán.', dieukien=DK_KT,
              chinh='1. Mở chi tiết, bấm Từ chối.\n2. Cửa sổ “Từ chối phiếu yêu cầu hạch toán bổ sung”.\n3. Nhập lý do, bấm Từ chối.\n'
                    '4. Phiếu về Đang tạo, lưu Ghi chú duyệt, người / thời điểm từ chối, ghi lịch sử, báo người lập.\n'
                    '5. Hiện “Từ chối phiếu thành công”.',
              phu='• Lý do trống → “Bắt buộc phải nhập”.\n• Bấm Hủy → đóng.', dacbiet='Người lập sửa và gửi lại được.'),
   layout=dict(menu=MENU_CD + ' => Xem chi tiết => Từ chối', shot=shot('15_reject'), shot_caption='Cửa sổ Từ chối phiếu',
               note='Modal Từ chối phiếu yêu cầu hạch toán bổ sung được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
   ui=[('Lý do từ chối', 'Textarea', 'Enable', '–', 'Có', 'Trống', 'Gợi ý “Nhập lý do từ chối”.'),
       ('Nút Từ chối / Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', '–')],
   ev=[('Bấm Từ chối', 'Click', 'Before:\n– Kiểm tra quyền, trạng thái; sai → “Bạn không có quyền từ chối phiếu này”.\n'
        'During:\n– Lý do trống → báo lỗi.\n' + ERR + '\nAfter:\n– Phiếu về Đang tạo; ghi Thay đổi trạng thái kèm lý do; báo “[HTBS] Từ chối: <số phiếu>” cho người lập.')])

# ------------------------------------------------------------ 2.12
fr(12, 'Lập phiếu kế toán', usecase=('FR-12', 'Lập phiếu kế toán', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(ten='Lập phiếu kế toán từ phiếu yêu cầu', mota='Mở màn Tạo phiếu kế toán với phiếu yêu cầu điền sẵn.',
              tacnhan=TN_KT, dieukien=DK_KT,
              chinh='1. Bấm Lập phiếu kế toán ở cột Hành động hoặc màn chi tiết.\n2. Hệ thống mở màn “Tạo phiếu kế toán” điền sẵn dữ liệu.\n'
                    '3. Kế toán lưu phiếu kế toán (SRS màn Phiếu kế toán).\n4. Phiếu yêu cầu chuyển Đang duyệt / Đã duyệt theo phiếu kế toán.',
              phu='• Thoát không lưu → phiếu yêu cầu giữ Chờ duyệt.', dacbiet=None),
   layout=dict(menu=MENU_CD + ' => Lập phiếu kế toán', shot=shot('21_accounting_create'), shot_caption='Màn Tạo phiếu kế toán mở từ phiếu yêu cầu'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nút Lập phiếu kế toán', 'Button', 'Enable / Ẩn', 'Ẩn',
        ['- Loại 1–6: Kế toán thanh toán, trong phạm vi công ty', '- Loại 7: Kế toán, công ty mình có phòng hỗ trợ của phiếu'])],
   ev=[('Bấm Lập phiếu kế toán', 'Click', 'After:\n– Mở màn Tạo phiếu kế toán với phiếu yêu cầu chọn sẵn (chưa ghi dữ liệu).')])

# ------------------------------------------------------------ 2.13
fr(13, 'In phiếu', usecase=('FR-13', 'In phiếu', 'io', A_LAP),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(ten='In phiếu yêu cầu hạch toán bổ sung', mota='Xem trước và in phiếu.', tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Bấm In phiếu ở cột Hành động hoặc màn chi tiết.\n2. Cửa sổ xem trước.\n3. Bấm In.', phu='• Đóng (×).',
              dacbiet='Đầu bản in theo công ty ghi trên phiếu; nhãn đối tượng đúng theo loại (NCC / KH).'),
   layout=dict(menu=MENU + ' => In phiếu', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[('Bản in', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Tiêu đề “YÊU CẦU HẠCH TOÁN BỔ SUNG”, số phiếu, ngày', '- Loại yêu cầu, bảng chi tiết / đối tượng, tổng tiền',
         '- Chỗ ký Người duyệt, Người lập']),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Mở hộp thoại in.')],
   ev=[('Bấm In', 'Click', 'After:\n– Mở hộp thoại in.')])

# ------------------------------------------------------------ 2.14
fr(14, 'Xuất Excel', usecase=('FR-14', 'Xuất Excel', 'io', A_LAP),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Xuất danh sách / một phiếu ra Excel',
              mota='Danh sách: chọn trường, thứ tự rồi xuất theo bộ lọc. Một phiếu: xuất từ menu ba chấm hoặc màn chi tiết.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Bấm Xuất Excel trên thanh công cụ.\n2. Cửa sổ “Chọn trường xuất file” (15 trường).\n3. Tích, kéo đổi thứ tự, bấm Xuất file.\n'
                    '4. Tải file, báo thành công.',
              phu='• Một phiếu: nút ba chấm → Xuất Excel, hoặc nút Xuất Excel ở màn chi tiết.\n• Bấm Đóng → không xuất.',
              dacbiet='Mặc định tích 12/15 trường (bỏ Loại tiền, Người cập nhật, Ngày cập nhật).'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Danh sách trường', 'Table/Grid', 'Enable', '15 trường', 'Ít nhất 1', '12 trường',
        'Số phiếu, Loại yêu cầu, KH/NCC, Số tiền, Diễn giải, Người tạo, Ngày tạo, Phòng ban, Ngày gửi, Người duyệt, Ngày duyệt, '
        'Trạng thái, Loại tiền, Người cập nhật, Ngày cập nhật.'),
       ('Nút Chọn tất cả / Bỏ chọn hết / Xuất file / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–')],
   ev=[('Kéo ba gạch', 'Drag', 'After:\n– Đổi thứ tự trường.'),
       ('Bấm Xuất file', 'Click', 'During:\n– Lấy dữ liệu theo bộ lọc + phạm vi quyền.\n' + ERR + '\nAfter:\n– Tải file .xlsx.')])

# ------------------------------------------------------------ 2.15
fr(15, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(ten='Xem lịch sử thay đổi của phiếu', mota='Các mốc Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Xóa.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Nút ba chấm → Lịch sử, hoặc Xem lịch sử ở màn chi tiết.\n2. Hiển thị các mốc, mới nhất trên.',
              phu='• Phiếu cũ (tạo trước khi bật lịch sử) → “Chưa có lịch sử thao tác nào.”.', dacbiet=None),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Thay đổi thông tin: trường cũ → mới, dòng chi tiết, file', '- Thay đổi trạng thái: cũ → mới; từ chối kèm lý do']),
       ('Nút Bộ lọc / Đóng', 'Button', 'Enable', '–', 'Hiển thị', '–')],
   ev=[('Mở lịch sử', 'Click', 'Before:\n– Kiểm tra quyền xem.\nAfter:\n– Hiển thị các mốc.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu yêu cầu hạch toán bổ sung; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Trường theo loại yêu cầu', [
        '– Điều chỉnh công nợ KH / NCC: bảng Chi tiết hạch toán (≥ 1 dòng); Số tiền phiếu = tổng dòng.',
        '– NCC bảo hành: chọn Phiếu xác nhận bảo hành, NCC và Số tiền tự điền.',
        '– NCC thiếu hàng: chọn Phiếu xử lý hàng thiếu, chọn NCC.', '– NCC hỗ trợ phát triển thị trường: chọn NCC.',
        '– Khác: chọn Đối tượng (NCC / KH / Nhân viên) rồi chọn đối tượng.',
        '– Đổi loại xóa sạch các trường phụ thuộc loại.'], ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-02', 'Lưu nháp và Gửi duyệt', [
        '– Lưu nháp chỉ bắt buộc Loại yêu cầu.',
        '– Gửi duyệt bắt buộc đủ trường theo loại, Loại tiền, Tỷ giá > 0, Số tiền > 0, ≥ 1 file đính kèm.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Gửi duyệt']),
    ('BR-03', 'Vòng đời trạng thái', [
        '– Lưu nháp → Đang tạo; Gửi duyệt → Chờ duyệt.', '– Từ chối → về Đang tạo kèm Ghi chú duyệt.',
        '– Lập / duyệt phiếu kế toán → Đang duyệt / Đã duyệt.',
        '– Sửa / Xóa / Gửi duyệt: người lập, phiếu Đang tạo.'], ['Lập phiếu', 'Chỉnh sửa', 'Gửi duyệt', 'Từ chối', 'Lập phiếu kế toán']),
    ('BR-04', 'Người xử lý theo loại', [
        '– Loại 1–6: Kế toán thanh toán trong phạm vi công ty.',
        '– Loại 7 Phối hợp kinh doanh: Kế toán của công ty có phòng hỗ trợ của phiếu.'], ['Từ chối', 'Lập phiếu kế toán']),
    ('BR-05', 'Phạm vi xem', ['– V2: loại 1–6 theo công ty phiếu, loại 7 theo công ty phòng hỗ trợ.',
                              '– Màn chờ duyệt luôn chỉ phiếu Chờ duyệt.', '– Phiếu Đang tạo của người khác luôn ẩn.'],
     ['Xem danh sách', 'Xem chi tiết']),
    ('BR-06', 'Thông báo', ['– Gửi duyệt → Kế toán kho; Từ chối → người lập kèm lý do.'], ['Gửi duyệt', 'Từ chối']),
    ('BR-07', 'Thao tác xong quay về danh sách', ['– Lưu, Gửi duyệt, Xóa, Từ chối thành công đều quay về màn danh sách.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Xóa', 'Từ chối']),
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

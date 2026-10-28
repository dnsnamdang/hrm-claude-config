# -*- coding: utf-8 -*-
"""Vá SRS "Phiếu báo có" (+ màn Tổng hợp tiền về ngân hàng) — bản Drive 28/10 — theo FORM "Danh mục quốc gia".

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/SRS - Phiếu báo có.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Luôn đọc bản Drive gốc. Khuôn: finance-product-import-direct-transfer/form_qg/patch_srs.py (màn 27) và
finance-bill-payment-authorization/form_qg_163/patch_srs.py (cùng kiểu Heading4 cho mục con 2.x.y).
"""
import copy, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..', '.claude', 'skills', 'srs-documenter', 'assets'))
import docx  # noqa: E402
from formqg_lib import *  # noqa: E402,F401
import formqg_lib as L  # noqa: E402
import docxlib  # noqa: E402

SRC = os.path.join(HERE, 'drive_0710', 'SRS_Drive.docx')
OUT_DIR = os.path.join(HERE, 'out')
NAME = 'SRS - Phiếu báo có'
OUT = os.path.join(OUT_DIR, NAME + '.docx')
UML = os.path.join(HERE, 'uml')
SHOTS = os.path.join(HERE, 'hdsd_shots')


def _is_sub(e):
    return e.tag == W('p') and style_of(e) == 'Heading4' and re.match(r'^\d+\.\d+\.\d+ ', txt(e))


L.is_sub = _is_sub  # tài liệu này: mục con 2.x.y là Heading4

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'Phiếu báo có'
# finance.js: hubGroup 'Quản lý tiền' > nhóm 'Thanh toán tiền mặt' > 2 mục màn
MENU = 'Phân hệ Tài chính => Quản lý tiền => Thanh toán tiền mặt => Phiếu báo có'
SUM_MENU = 'Phân hệ Tài chính => Quản lý tiền => Thanh toán tiền mặt => Tổng hợp tiền về ngân hàng'
TAIL = ' Chỉ bổ sung quy tắc riêng của %s.' % SCREEN
TAIL_SUM = ' Chỉ bổ sung quy tắc riêng của màn Tổng hợp tiền về ngân hàng.'
UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: nếu chưa nhập hoặc thay đổi gì thì rời màn '
           'ngay; nếu đã nhập dữ liệu thì hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” '
           '(Thoát / Ở lại).')
UNSAVED_EV = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
              '– Đã nhập dữ liệu → hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”; '
              'bấm Thoát thì rời màn và bỏ thay đổi, bấm Ở lại thì giữ nguyên màn.']

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Phạm vi phiếu nhìn thấy theo quyền Xem tất cả phiếu báo có của tổng công ty (V1) hoặc '
              'của công ty (V2); không có quyền nào thì chỉ thấy phiếu do mình lập.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (V1, V2); không có quyền nào vẫn xem được phiếu do chính mình lập.')
COND_LIST3 = COND_LIST + '\n3. Đang ở màn danh sách phiếu báo có.'
ACTOR_Q1 = 'Người dùng có quyền thực hiện chức năng: quyền Quản lý phiếu báo có (Q1).'
ACTOR_OWNER = 'Người lập phiếu có quyền thực hiện chức năng: quyền Quản lý phiếu báo có (Q1).'
COND_OWNER = ('1. Đăng nhập thành công.\n'
              '2. Có quyền Quản lý phiếu báo có (Q1) và là người lập phiếu.\n'
              '3. Phiếu đang ở trạng thái Đang tạo.')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người lập phiếu, hoặc người có quyền Xem tất cả phiếu báo có của '
               'tổng công ty (V1) / của công ty (V2) trong phạm vi được giao.')
COND_SCOPE = ('1. Đăng nhập thành công.\n'
              '2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu nằm trong phạm vi dữ liệu của người dùng; phiếu Đang tạo chỉ người lập xem được.')
ACTOR_SUM = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn Tổng hợp tiền về ngân hàng '
             '(màn không gắn quyền riêng); dữ liệu luôn giới hạn theo công ty của người đăng nhập.')
COND_SUM = ('1. Đăng nhập thành công.\n'
            '2. Xác định được công ty của người đăng nhập.')

# Mục 2.x: regex -> (vế sau link, đuôi, Tác nhân, Điều kiện ban đầu)
SECTIONS = {
    r'^2\.1 ': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', TAIL, ACTOR_LIST, COND_LIST),
    r'^2\.2 ': ('Kịch bản tìm kiếm, Bộ lọc và Dropdown.', TAIL, ACTOR_LIST, COND_LIST3),
    r'^2\.3 ': ('Bộ lọc và Cài đặt bộ lọc.', TAIL, ACTOR_LIST, COND_LIST3),
    r'^2\.4 ': ('Cấu hình cột.', TAIL, ACTOR_LIST, COND_LIST3),
    r'^2\.5 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', TAIL, ACTOR_Q1,
                '1. Đăng nhập thành công.\n2. Có quyền Quản lý phiếu báo có (Q1); không có quyền thì nút Tạo mới '
                'bị ẩn.'),
    r'^2\.6 ': ('Popup tra cứu dữ liệu, Kịch bản tìm kiếm và Phân trang.', TAIL, ACTOR_Q1,
                '1. Đăng nhập thành công.\n2. Có quyền Quản lý phiếu báo có (Q1).\n'
                '3. Đang ở màn Tạo mới hoặc Sửa phiếu báo có.'),
    r'^2\.7 ': ('Màn Chỉnh sửa, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', TAIL, ACTOR_OWNER,
                COND_OWNER),
    r'^2\.8 ': ('Màn Xem chi tiết và Phân quyền.', TAIL, ACTOR_SCOPE, COND_SCOPE),
    r'^2\.9 ': ('Hộp xác nhận thao tác, Thông báo và Quy tắc ghi lịch sử.', TAIL, ACTOR_Q1,
                '1. Đăng nhập thành công.\n2. Có quyền Quản lý phiếu báo có (Q1).\n'
                '3. Phiếu đang ở trạng thái Đang tạo (phiếu Đang tạo chỉ người lập nhìn thấy).'),
    r'^2\.10 ': ('Quy tắc xóa, Thông báo và Quy tắc ghi lịch sử.', TAIL, ACTOR_OWNER, COND_OWNER),
    r'^2\.11 ': ('Thông báo, UI/UX và Quy tắc ghi lịch sử.', TAIL, ACTOR_Q1,
                 '1. Đăng nhập thành công.\n2. Có quyền Quản lý phiếu báo có (Q1) và xem được phiếu.\n'
                 '3. Phiếu loại Thu bán hàng hoặc Thu khác (phiếu Thu nhà cung cấp không có khối này).'),
    r'^2\.12 ': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', TAIL, ACTOR_SCOPE, COND_SCOPE),
    r'^2\.13 ': ('Quy tắc Import Excel, Thông báo và Quy tắc ghi lịch sử.', TAIL, ACTOR_Q1,
                 '1. Đăng nhập thành công.\n2. Có quyền Quản lý phiếu báo có (Q1); không có quyền thì nút Import '
                 'Excel bị ẩn.\n3. Có file sao kê điền theo đúng file mẫu.'),
    r'^2\.14 ': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang, Bộ lọc và Cấu hình cột.', TAIL_SUM, ACTOR_SUM,
                 COND_SUM),
    r'^2\.15 ': ('Quy tắc Excel.', TAIL_SUM, ACTOR_SUM, COND_SUM + '\n3. Đang ở màn Tổng hợp tiền về ngân hàng.'),
    r'^2\.16 ': ('Thông báo và UI/UX.', TAIL_SUM, ACTOR_SUM,
                 COND_SUM + '\n3. Có ít nhất một dòng chi tiết còn tiền chưa điều chỉnh.'),
}

MENU_LINES = {  # regex mục -> (dòng Menu, câu popup hoặc None)
    r'^2\.2 ': ('Menu: %s => Tìm kiếm nâng cao' % MENU, None),
    r'^2\.3 ': ('Menu: %s => Cài đặt bộ lọc' % MENU,
                'Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.4 ': ('Menu: %s => Tùy chỉnh cột (biểu tượng cột cạnh nút Import Excel)' % MENU,
                'Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.5 ': ('Menu: %s => Tạo mới' % MENU,
                'Modal Xác nhận lưu và duyệt (nút Lưu và duyệt) được mở ngay trên màn hình Tạo mới phiếu theo '
                'đường dẫn ở trên.'),
    r'^2\.6 ': ('Menu: %s => Tạo mới / Sửa => bấm ô Khách hàng, Nhà cung cấp, Số đơn hàng/Hợp đồng, Phiếu xuất '
                'hàng hoặc Phiếu YC xuất hàng trên dòng Chi tiết' % MENU,
                'Modal Chọn khách hàng, Chọn nhà cung cấp, Chọn đơn hàng/hợp đồng, Chọn phiếu xuất hàng và Chọn '
                'phiếu yêu cầu xuất hàng được mở ngay trên màn hình Tạo mới hoặc Sửa phiếu theo đường dẫn ở trên.'),
    r'^2\.7 ': ('Menu: %s => Sửa (trên dòng phiếu) / bấm Mã phiếu => Sửa' % MENU, None),
    r'^2\.8 ': ('Menu: %s => bấm Mã phiếu' % MENU, None),
    r'^2\.9 ': ('Menu: %s => Duyệt (menu “…” trên dòng phiếu) / bấm Mã phiếu => Duyệt' % MENU,
                'Modal Xác nhận duyệt được mở ngay trên màn hình danh sách (mục Duyệt trên dòng phiếu) hoặc màn hình '
                'chi tiết phiếu (nút Duyệt) theo đường dẫn ở trên.'),
    r'^2\.10 ': ('Menu: %s => Xóa (trên dòng phiếu) / bấm Mã phiếu => Xóa' % MENU,
                 'Modal Xác nhận xóa được mở ngay trên màn hình danh sách (biểu tượng Xóa trên dòng) hoặc màn hình '
                 'chi tiết phiếu (nút Xóa) theo đường dẫn ở trên.'),
    r'^2\.11 ': ('Menu: %s => bấm Mã phiếu => khối Đánh dấu không báo tiền về' % MENU, None),
    r'^2\.12 ': ('Menu: %s => Lịch sử (trên dòng phiếu) / bấm Mã phiếu => Xem lịch sử' % MENU,
                 'Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối Lịch sử '
                 'nằm cuối màn hình chi tiết phiếu.'),
    r'^2\.13 ': ('Menu: %s => Import Excel' % MENU,
                 'Modal Import phiếu báo có được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.14 ': ('Menu: %s' % SUM_MENU, None),
    r'^2\.15 ': ('Menu: %s => Xuất Excel' % SUM_MENU,
                 'Modal Chọn trường xuất file được mở ngay trên màn hình Tổng hợp tiền về ngân hàng theo đường dẫn '
                 'ở trên.'),
    r'^2\.16 ': ('Menu: %s => tích dòng => Tạo mới điều chỉnh công nợ; hoặc %s => bấm Mã phiếu => Tạo phiếu yêu '
                 'cầu điều chỉnh công nợ' % (SUM_MENU, MENU), None),
}

USECASES = {  # mục -> (actor, mã, tên, nhóm)
    r'^2\.5 ': ('Kế toán', 'FR-05', 'Tạo mới phiếu báo có', 'crud'),
    r'^2\.6 ': ('Kế toán', 'FR-06', 'Chọn đối tượng từ popup', 'crud'),
    r'^2\.7 ': ('Người lập phiếu', 'FR-07', 'Chỉnh sửa phiếu báo có', 'crud'),
    r'^2\.8 ': ('Người dùng có quyền', 'FR-08', 'Xem chi tiết phiếu báo có', 'view'),
    r'^2\.9 ': ('Kế toán', 'FR-09', 'Duyệt phiếu báo có', 'action'),
    r'^2\.10 ': ('Người lập phiếu', 'FR-10', 'Xóa phiếu báo có', 'action'),
    r'^2\.11 ': ('Kế toán', 'FR-11', 'Đánh dấu không báo tiền về', 'action'),
    r'^2\.13 ': ('Kế toán', 'FR-13', 'Import Excel sao kê', 'io'),
    r'^2\.15 ': ('Kế toán', 'FR-15', 'Xuất Excel màn tổng hợp', 'io'),
    r'^2\.16 ': ('Kế toán', 'FR-16', 'Tạo phiếu yêu cầu điều chỉnh công nợ', 'action'),
}

# Ảnh thay mới (chụp DEV 28/10): regex chú thích CŨ -> (ảnh, chú thích mới hoặc None)
IMAGES = [
    (r'Màn Danh sách phiếu báo có lúc mới truy cập', '01_list', None),
    (r'Phần bên phải của bảng: cột Trạng thái', '01b_list_right',
     'Phần bên phải của bảng: cột Trạng thái và cột Hành động (dòng 1 là phiếu Đang tạo)'),
    (r'Bảng tìm kiếm nâng cao của màn Phiếu báo có', '02_filter', None),
    (r'Cửa sổ Cài đặt bộ lọc', '26_filtercfg', None),
    (r'Cửa sổ Tuỳ chỉnh cột', '25_colcfg', None),
    (r'Form Tạo mới phiếu báo có', '10_create', None),
    (r'Phần bên phải bảng Chi tiết', '10d_create_right', None),
    (r'Form khi chọn loại thu Thu nhà cung cấp', '10b_supplier', None),
    (r'Form khi chọn loại thu Thu khác', '10c_other', None),
    (r'Cửa sổ Chọn khách hàng', '11_customer', None),
    (r'Cửa sổ Chọn đơn hàng/hợp đồng', '11b_contract', None),
    (r'Cửa sổ Chọn nhà cung cấp', '11c_supplier', None),
    (r'Màn Sửa phiếu báo có', '12_edit', 'Màn Sửa phiếu báo có'),
    (r'Màn Chi tiết phiếu báo có', '17_detail', None),
    (r'Hộp xác nhận duyệt phiếu báo có', '14_approve', None),
    (r'Hộp xác nhận xóa phiếu báo có', '13_delete', None),
    (r'Khối Đánh dấu không báo tiền về', '18_notreport', None),
    (r'Cửa sổ Lịch sử thay đổi', '16_history', 'Cửa sổ Lịch sử thay đổi của phiếu'),
    (r'Khối Lịch sử ở màn chi tiết', '17b_detail_history', None),
    (r'Cửa sổ Import phiếu báo có', '32_import_validated',
     'Cửa sổ Import phiếu báo có sau khi Validate: ô Tổng / Hợp lệ / Lỗi và lý do lỗi dưới từng dòng'),
    (r'Màn Tổng hợp tiền về ngân hàng', '40_summary', None),
    (r'Phần bên phải: Số tiền chưa điều chỉnh', '40b_summary_right', None),
    (r'Bảng tìm kiếm nâng cao của màn Tổng hợp', '41_sumfilter', None),
    (r'Cửa sổ Chọn trường xuất file', '42_export', None),
    (r'Ô tích Điều chỉnh công nợ trên từng dòng', '40b_summary_right', None),
]

IMPORT_COLS = [  # STT | Tên cột | Bắt buộc | Mô tả — theo BillIncomeReportImportService::COLUMNS + templateSampleRow
    ('1', 'Số tiền *', 'Có', 'Số lớn hơn 0; chấp nhận dấu phẩy hoặc dấu chấm ngăn cách nghìn. Ví dụ: 1,000,000.'),
    ('2', 'Diễn giải', 'Không', 'Dùng làm diễn giải của phiếu và của dòng chi tiết. Ví dụ: Cong ty A thanh toan HD 123.'),
    ('3', 'Ngày hạch toán *', 'Có', 'Định dạng dd/mm/yyyy hoặc yyyy-mm-dd, phải là ngày có thật (31/02 là lỗi). '
     'Ví dụ: 28/10/2026.'),
    ('4', 'Mã ngân hàng *', 'Có', 'Mã ngân hàng có trong danh mục Ngân hàng. Ví dụ: VIETINBANK.'),
    ('5', 'Số tài khoản *', 'Có', 'Số tài khoản ngân hàng của công ty đã khai trong danh mục. Ví dụ: 116000142872.'),
    ('6', 'Tên chi nhánh *', 'Có', 'Tên chi nhánh ngân hàng có trong danh mục. Ví dụ: CN Ha Noi.'),
    ('7', 'Loại tiền *', 'Có', 'Mã loại tiền có trong danh mục tiền tệ. Ví dụ: VNĐ.'),
    ('8', 'Tỷ giá', 'Không', 'Số lớn hơn 0; bỏ trống thì lấy tỷ giá của loại tiền. Ví dụ: 1.'),
]

PART5 = [  # STT | Nhóm | Màn hình | Đường dẫn — grep code hrm-api/hrm-client 28/10
    ('1', 'Tài chính', 'Phiếu yêu cầu điều chỉnh công nợ (lập từ dòng chi tiết phiếu báo có còn tiền chưa điều '
     'chỉnh; số tiền đã điều chỉnh ghi ngược lại dòng báo có)',
     'Tài chính -> Khởi tạo -> Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi -> Phiếu yêu cầu điều chỉnh công nợ'),
    ('2', 'Tài chính', 'Phiếu kế toán (điều chỉnh công nợ gắn dòng chi tiết phiếu báo có)',
     'Tài chính -> Sổ tổng hợp -> Phiếu kế toán'),
    ('3', 'Tài chính', 'Khai báo đầu kỳ công nợ (khách hàng đã có phiếu báo có ghi sổ thì khai báo đầu kỳ bị khóa)',
     'Tài chính -> Khai báo đầu kỳ -> Khai báo đầu kỳ công nợ'),
    ('4', 'Bán hàng', 'Đối chiếu công nợ 1 KH, Tổng hợp công nợ theo NV, Chi tiết công nợ KH (phiếu báo có đã duyệt '
     'tính vào tiền khách đã trả)', 'Bán hàng -> Báo cáo công nợ'),
    ('5', 'Bán hàng', 'Báo cáo theo dõi giữ hàng (phiếu báo có tính vào Tổng thanh toán của hợp đồng)',
     'Bán hàng -> Hàng giữ -> Báo cáo theo dõi giữ hàng'),
    ('6', 'Tài chính', 'Yêu cầu xuất giữ (tiền đã thu theo phiếu báo có dùng để xét tuyến duyệt)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Giữ hàng'),
    ('7', 'Bán hàng', 'Hợp đồng bán (ngày đặt cọc lần đầu lấy theo ngày hạch toán sớm nhất của phiếu thu / phiếu '
     'báo có / phiếu kế toán gắn hợp đồng)', 'Bán hàng -> Hợp đồng'),
    ('8', 'Danh mục', 'Danh mục tài khoản, Danh mục tiền tệ, Ngân hàng, Chi nhánh ngân hàng (chặn xóa khi đang dùng '
     'trên phiếu báo có)', 'Tài chính -> Danh mục; Danh mục dùng chung -> Ngân hàng'),
]


# ============================================================== TIỆN ÍCH
def lines_replace(lines, old_regex, new):
    out, hit = [], False
    for l in lines:
        if re.search(old_regex, l):
            hit = True
            if new is not None:
                out.extend(new if isinstance(new, list) else [new])
        else:
            out.append(l)
    assert hit, 'Không thấy dòng: ' + old_regex
    return out


def kv_edit(kv, key, old_regex, new):
    write_cell(kv_row(kv, key), lines_replace(kv_get(kv, key), old_regex, new))


def kv_append(kv, key, extra):
    write_cell(kv_row(kv, key), kv_get(kv, key) + (extra if isinstance(extra, list) else [extra]))


def ev_cell(ev, event_regex):
    return cells(find_row(ev, 1, event_regex))[3]


def ev_edit(ev, event_regex, old_regex, new, rid=None):
    tc = ev_cell(ev, event_regex)
    write_cell(tc, lines_replace(cell_lines(tc), old_regex, new), rid)


def ui_set(ui, name_regex, col, new):
    set_col(ui, header_index(ui, col), name_regex, new)


def no_bookmarks(el):
    for tag in ('bookmarkStart', 'bookmarkEnd'):
        for b in list(el.iter(W(tag))):
            b.getparent().remove(b)
    return el


def set_caption(cap, text):
    m = re.match(r'^(Hình \d+:\s*)', txt(cap))
    set_runs_text(cap, (m.group(1) if m else 'Hình 0: ') + text)


def part_heading(doc, n):
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1' and re.match(r'^Phần %d\b' % n, txt(e)):
            return e
    raise KeyError(n)


# ============================================================== XỬ LÝ
def fix_unstyled_subheadings(doc):
    tpl = next(e for e in items(doc) if e.tag == W('p') and style_of(e) == 'Heading4')
    n = 0
    for e in items(doc):
        if e.tag == W('p') and not style_of(e) and re.match(r'^\d+\.\d+\.\d+ \S', txt(e)):
            h = no_bookmarks(strip_ids(copy.deepcopy(tpl)))
            set_runs_text(h, txt(e).strip())
            e.addprevious(h)
            e.getparent().remove(e)
            n += 1
            log('Đặt Heading4 cho tiêu đề: ' + txt(h))
    assert n == 1, 'Mong 1 tiêu đề chưa đặt heading (2.13.2), thấy %d' % n


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)

    fix_unstyled_subheadings(doc)

    for rx, (tail, tail2, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + tail2)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    for rx, (menu, popup) in MENU_LINES.items():
        sec = section(doc, rx)
        p = sec_par(sec, r'^Menu:')
        set_runs_text(p, menu)
        nxt = p.getnext()
        is_old = nxt is not None and nxt.tag == W('p') and re.search(r'được mở', txt(nxt))
        if popup and is_old:
            set_runs_text(nxt, popup)
        elif popup:
            strip_ids(docxlib.clone_par_after(p, p, popup))

    patch_sections(doc, rid)
    replace_images(doc)
    add_import_template_table(doc)
    patch_part4(doc)
    add_part5(doc)

    for rx, (actor, code, name, grp) in USECASES.items():
        png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
        draw_usecase_qg(png, actor, code, name, grp)
        sec = section(doc, rx)
        blk = usecase_block(sec)
        cap = 'Biểu đồ Use Case — %s %s' % (code, name)
        if blk is None:
            add_usecase(doc, sec, section(doc, r'^2\.9 '), png, cap)
        else:
            set_image(doc, blk[1], png)
            set_caption(blk[2], cap)
    draw_overview(doc)

    renumber_subheadings(doc)
    nfig = renumber_figures(doc)
    log('Số Hình sau khi đánh lại: %d' % nfig)

    doc.save(OUT)
    print('Đã ghi', OUT)
    for m in L.LOG:
        print(' -', m)
    if '--no-word' not in sys.argv:
        word_finalize(OUT, os.path.join(OUT_DIR, NAME + '.pdf'))


def draw_overview(doc):
    import srs_uml_render as U
    png = os.path.join(UML, 'overview_srs.png')
    mains = [('FR-01', 'Xem danh sách phiếu báo có', 'view'), ('FR-05', 'Tạo mới phiếu báo có', 'crud'),
             ('FR-07', 'Chỉnh sửa phiếu báo có', 'crud'), ('FR-09', 'Duyệt phiếu báo có', 'action'),
             ('FR-10', 'Xóa phiếu báo có', 'action'), ('FR-11', 'Đánh dấu không báo tiền về', 'action'),
             ('FR-13', 'Import Excel sao kê', 'io'), ('FR-14', 'Xem Tổng hợp tiền về ngân hàng', 'view'),
             ('FR-15', 'Xuất Excel màn tổng hợp', 'io'), ('FR-16', 'Tạo phiếu YC điều chỉnh công nợ', 'action')]
    subs = [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
            ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
            ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
            ('FR-08', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
            ('FR-12', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
            ('FR-06', 'Chọn đối tượng từ popup', 'crud', 'extend', [1, 2], None)]
    actors = [('Kế toán (Quản lý phiếu báo có)', list(range(10))),
              ('Người có quyền xem phiếu báo có', [0, 7, 8, 9])]
    U.draw_overview2(png, actors, mains, subs)
    sec_h = next(e for e in items(doc) if e.tag == W('p') and style_of(e) == 'Heading2'
                 and 'Sơ đồ UML tổng quan' in txt(e))
    img = sec_h.getnext()
    while not list(img.iter(A_NS + 'blip')):
        img = img.getnext()
    set_image(doc, img, png)
    log('Vẽ lại sơ đồ Use Case tổng quan (không tiêu đề hệ thống)')


def replace_images(doc):
    used = set()
    for cap_rx, shot, new_cap in IMAGES:
        path = os.path.join(SHOTS, shot + '.png')
        hit = None
        for e in items(doc):
            if e.tag == W('p') and re.match(r'^Hình \d+:\s*' + cap_rx, txt(e)) and id(e) not in used:
                hit = e
                break
        assert hit is not None, 'Không thấy chú thích ' + cap_rx
        used.add(id(hit))
        img = hit.getprevious()
        assert list(img.iter(A_NS + 'blip')), 'đoạn trước chú thích không phải ảnh: ' + txt(hit)
        set_image(doc, img, path)
        if new_cap:
            set_caption(hit, new_cap)
        log('Thay ảnh %s → %s' % (txt(hit)[:55], shot))


def fix_ui_shift_223(ui):
    """2.2.3: bảng lệch 1 cột (thiếu ô Bắt buộc), chữ thừa ở cột cuối — dồn lại đúng cột."""
    merge = {r'^Ô Người tạo$': 'Lọc theo người tạo phiếu (người lập).',
             r'^Ô Ngày tạo': 'Lọc theo ngày tạo phiếu, lấy cả hai đầu mốc.'}
    for tr in rows(ui)[1:]:
        cs = cells(tr)
        v = [txt(c) for c in cs]
        name = v[1]
        desc = v[6]
        for rx, d in merge.items():
            if re.search(rx, name):
                desc = d
        # ô cuối vốn trống (rPr nhỏ) → lấy đoạn của ô Mô tả cũ làm khuôn chữ
        for p in cs[7].findall(W('p')):
            cs[7].remove(p)
        cs[7].append(copy.deepcopy(cs[6].find(W('p'))))
        write_cell(cs[5], ['Không'])
        write_cell(cs[6], [v[5]])
        write_cell(cs[7], [desc])
    # chia lại bề rộng cột (giữ tổng) cho STT / Bắt buộc không bị gãy chữ
    grid = ui.find(W('tblGrid')).findall(W('gridCol'))
    total = sum(int(g.get(W('w'))) for g in grid)
    ratios = [0.055, 0.14, 0.11, 0.105, 0.12, 0.105, 0.10]
    widths = [int(total * r) for r in ratios]
    widths.append(total - sum(widths))
    for g, w in zip(grid, widths):
        g.set(W('w'), str(w))
    for tr in rows(ui):
        for tc, w in zip(cells(tr), widths):
            tcpr = tc.find(W('tcPr'))
            if tcpr is not None and tcpr.find(W('tcW')) is not None:
                tcpr.find(W('tcW')).set(W('w'), str(w))
                tcpr.find(W('tcW')).set(W('type'), 'dxa')
    log('2.2.3: dồn lại bảng lệch 1 cột, bỏ chữ thừa ở cột cuối')


def patch_sections(doc, rid):
    # ---------- 2.1 Xem danh sách
    s = section(doc, r'^2\.1 ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^1\. Người dùng vào menu', '1. Người dùng vào menu %s.' % MENU)
    ui = sec_ui(s)
    ui_set(ui, r'^Cột Tổng PS$', 'Mô tả', 'Tổng số tiền nguyên tệ của phiếu, căn phải, có dấu phẩy ngăn cách nghìn '
                                          'và 2 chữ số thập phân; sắp xếp được.')
    ui_set(ui, r'^Cột Ngày tạo$', 'Mô tả', 'Ngày giờ tạo phiếu; sắp xếp được.')
    ui_set(ui, r'^Cột Người tạo$', 'Mô tả', 'Người lập phiếu, dạng “Tên - Mã phòng ban”.')
    ui_set(ui, r'^Cột Ngày cập nhật$', 'Mô tả', 'Ngày giờ cập nhật phiếu gần nhất.')
    ui_set(ui, r'^Cột Người cập nhật$', 'Mô tả', 'Người cập nhật phiếu gần nhất.')
    ui_set(ui, r'^Cột Trạng thái$', 'Loại', 'Table/Grid')
    ui_set(ui, r'^Cột Hành động$', 'Loại', 'Table/Grid')
    ui_set(ui, r'^Cột Hành động$', 'Mô tả', 'Phiếu Đang tạo của mình: biểu tượng Sửa, Xóa và nút “…” (Hành động '
                                            'khác) chứa Duyệt, Lịch sử. Phiếu Đã duyệt: chỉ biểu tượng Lịch sử. '
                                            'Nút không dùng được thì ẩn hẳn.')

    # ---------- 2.2 Tìm kiếm
    s = section(doc, r'^2\.2 ')
    ui = sec_ui(s)
    fix_ui_shift_223(ui)
    tr = find_row(ui, 1, r'^Ô Hạch toán từ')
    write_cell(cells(tr)[1], ['Ô Ngày hạch toán'])
    write_cell(cells(tr)[4], ['dd/mm/yyyy → dd/mm/yyyy'])
    write_cell(cells(tr)[7], ['Một ô gồm hai lịch Từ ngày → Đến ngày; lọc theo ngày hạch toán, lấy cả hai đầu mốc.'])
    tr = find_row(ui, 1, r'^Ô Ngày tạo từ')
    write_cell(cells(tr)[1], ['Ô Ngày tạo'])
    write_cell(cells(tr)[4], ['dd/mm/yyyy → dd/mm/yyyy'])
    write_cell(cells(tr)[7], ['Một ô gồm hai lịch Từ ngày → Đến ngày; lọc theo ngày tạo phiếu, lấy cả hai đầu mốc.'])
    ev = sec_ev(s)
    write_cell(cells(find_row(ev, 1, r'^Bấm Tìm kiếm$'))[1], ['Bấm Tìm kiếm hoặc nhấn Enter ở ô tìm nhanh'])

    # ---------- 2.3 Cài đặt bộ lọc
    s = section(doc, r'^2\.3 ')
    kv_append(sec_kv(s), 'Dòng sự kiện phụ', '• Bấm Đóng / (x) → đóng cửa sổ, giữ nguyên cấu hình cũ.')
    ui = sec_ui(s)
    ui_set(ui, r'^Danh sách tiêu chí lọc', 'Loại', 'Checkbox')
    ui_set(ui, r'^Tay cầm kéo thả', 'Loại', 'Icon')
    ev = sec_ev(s)
    clone_row_after(ev, r'^Bỏ tích một tiêu chí', [None, 'Kéo tay cầm đổi thứ tự tiêu chí', 'Drag',
                                                    ['After:', '– Cập nhật thứ tự tạm trong cửa sổ; áp dụng khi bấm '
                                                     'Lưu.']])

    # ---------- 2.4 Tùy chỉnh cột
    s = section(doc, r'^2\.4 ')
    kv_append(sec_kv(s), 'Dòng sự kiện phụ', '• Bấm Đóng / (x) → đóng cửa sổ, giữ nguyên cấu hình cũ.')
    ui = sec_ui(s)
    ui_set(ui, r'^Danh sách cột$', 'Loại', 'Checkbox')
    ev = sec_ev(s)
    clone_row_after(ev, r'^Bấm Chọn tất cả', [None, 'Kéo biểu tượng ☰ đổi thứ tự cột', 'Drag',
                                              ['During:', '– Cột bắt buộc (STT, Mã phiếu, Hành động) không kéo được.',
                                               'After:', '– Cập nhật thứ tự tạm trong cửa sổ; áp dụng khi bấm Lưu.']])

    # ---------- 2.5 Tạo mới
    s = section(doc, r'^2\.5 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^8\. ', [
        '8. Ghi nhận hành động Tạo mới (kèm Duyệt nếu bấm Lưu và duyệt) trong lịch sử của phiếu.',
        '9. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Rời màn khi đã nhập', UNSAVED)
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Không có quyền Quản lý phiếu báo có',
            '• Không có quyền Quản lý phiếu báo có → nút Tạo mới không hiển thị; gọi thẳng chức năng lưu thì hệ thống '
            'kiểm tra dữ liệu nhập trước, hợp lệ rồi mới báo “Bạn không có quyền lập phiếu báo có” và không lưu.')
    ui = sec_ui(s)
    ui_set(ui, r'^Tỷ giá \(VND\)', 'Loại', 'Textbox')
    ui_set(ui, r'^Cột Tên tài khoản', 'Loại', 'Label')
    ui_set(ui, r'^Cột Hợp đồng mua', 'Loại', 'Label')
    ui_set(ui, r'^Cột NVKD', 'Loại', 'Label')
    ui_set(ui, r'^Cột Số tiền$', 'Loại', 'Textbox')
    ui_set(ui, r'^Cột Số tiền \(VND\)', 'Loại', 'Label')
    ui_set(ui, r'^Nút Quay lại', 'Mô tả', 'Về màn danh sách; đã nhập mà chưa lưu thì hỏi “Bạn có thông tin chưa lưu. '
                                         'Có chắc chắn muốn thoát?” (Thoát / Ở lại).')
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm Lưu$', r'^Before:$', None)
    ev_edit(ev, r'^Bấm Lưu$', r'^– Kiểm tra quyền Quản lý phiếu báo có; không có quyền', None)
    ev_edit(ev, r'^Bấm Lưu$', r'^– Hợp đồng nguyên tắc, không tích dư nợ', [
        '– Hợp đồng nguyên tắc, không tích dư nợ đầu kì mà chưa chọn phiếu yêu cầu xuất hàng → “Bắt buộc chọn”.',
        '– Dữ liệu hợp lệ nhưng không có quyền Quản lý phiếu báo có → báo “Bạn không có quyền lập phiếu báo có”.'])
    add_err_line(ev, r'^Bấm Lưu$', rid)
    ev_edit(ev, r'^Bấm Lưu và duyệt$', r'^– Ghi dòng lịch sử “Thay đổi trạng thái',
            '– Ghi lịch sử “Tạo mới” và “Thay đổi trạng thái: Đang tạo → Đã duyệt” kèm ghi chú đã ghi bút toán.')
    ev_edit(ev, r'^Bấm Lưu và duyệt$', r'^– Hiển thị hộp xác nhận lưu và duyệt',
            '– Hiển thị hộp “Xác nhận lưu và duyệt” với câu “Bạn đồng ý lưu và duyệt?” (Xác nhận / Hủy); bấm Hủy thì '
            'không làm gì.')
    add_err_line(ev, r'^Bấm Lưu và duyệt$', rid)
    clone_row_after(ev, r'^Bấm Lưu và duyệt$',
                    [None, 'Bấm Lưu và tiếp tục', 'Click',
                     ['During:', '– Kiểm tra dữ liệu như nút Lưu.', 'After:',
                      '– Lưu phiếu ở trạng thái Đang tạo và ghi lịch sử “Tạo mới”.',
                      '– Hiển thị thông báo thành công, ở lại màn Tạo mới với form trống để lập phiếu kế tiếp.']])
    add_err_line(ev, r'^Bấm Lưu và tiếp tục$', rid)
    tr = find_row(ev, 1, r'^Bấm Quay lại')
    write_cell(cells(tr)[1], ['Bấm Quay lại / chọn menu khác / đóng tab trình duyệt'])
    write_cell(cells(tr)[3], UNSAVED_EV)

    # ---------- 2.6 Chọn đối tượng từ popup
    s = section(doc, r'^2\.6 ')
    kv_append(sec_kv(s), 'Dòng sự kiện phụ',
              '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận; dòng chi tiết giữ '
              'nguyên giá trị cũ.')
    ui = sec_ui(s)
    for rx in (r'^Cửa sổ Chọn khách hàng', r'^Cửa sổ Chọn nhà cung cấp', r'^Cửa sổ Chọn đơn hàng',
               r'^Cửa sổ Chọn phiếu xuất hàng', r'^Cửa sổ Chọn phiếu yêu cầu'):
        ui_set(ui, rx, 'Loại', 'Table/Grid')
    ui_set(ui, r'^Cửa sổ Chọn khách hàng', 'Mô tả',
           'Có ba ô tìm kiếm: Tên / Mã khách hàng, Mã số thuế, Số điện thoại; bảng hiển thị Mã KH - Tên khách hàng, '
           'Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP.')
    ui_set(ui, r'^Cửa sổ Chọn đơn hàng', 'Mô tả',
           'Dòng mô tả dưới tiêu đề là mã và tên khách hàng đang chọn; ô tìm theo Số đơn hàng/Hợp đồng; bảng hiển '
           'thị Số đơn hàng/Hợp đồng, Ngày lập, Giá trị hợp đồng, Số tiền còn nợ.')
    clone_row_after(ui, r'^Phân trang trong cửa sổ',
                    [None, 'Nút Đóng / (x)', 'Button', 'Enable', '–', '–', 'Hiển thị',
                     'Đóng cửa sổ, không chọn gì.'])

    # ---------- 2.7 Chỉnh sửa
    s = section(doc, r'^2\.7 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống kiểm tra dữ liệu, ghi lại toàn bộ dòng chi tiết và cập nhật hai ô tổng tiền.',
        '6. Ghi nhận các thay đổi (theo từng trường và từng dòng chi tiết; kèm Duyệt nếu bấm Lưu và duyệt) trong '
        'lịch sử của phiếu.',
        '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu đã duyệt hoặc không phải của mình',
            '• Phiếu đã duyệt hoặc không phải của mình → nút Sửa không hiển thị; vào thẳng bằng đường dẫn thì hệ '
            'thống chuyển sang màn chi tiết phiếu.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Rời màn khi đã sửa', UNSAVED)
    ui = sec_ui(s)
    ui_set(ui, r'^Các ô thông tin chung còn lại', 'Loại', 'Dropdown / Datepicker / Textbox')
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm Lưu$', r'^– Kiểm tra quyền Quản lý phiếu báo có; thiếu quyền',
            '– Kiểm tra dữ liệu nhập trước (như màn Tạo mới); dữ liệu hợp lệ mới kiểm tra quyền Quản lý phiếu báo có, '
            'thiếu quyền thì báo “Bạn không có quyền sửa phiếu báo có”.')
    add_err_line(ev, r'^Bấm Lưu$', rid)
    write_cell(ev_cell(ev, r'^Bấm Lưu và duyệt$'),
               ['Before:', '– Hiển thị hộp “Xác nhận lưu và duyệt” (Xác nhận / Hủy).', 'During:',
                '– Kiểm tra như nút Lưu.', ERR_LINE, 'After:',
                '– Lưu như nút Lưu rồi chuyển trạng thái sang Đã duyệt, ghi bút toán vào sổ cái.',
                '– Ghi lịch sử phần thay đổi và “Thay đổi trạng thái: Đang tạo → Đã duyệt”, gửi thông báo, quay về '
                'màn danh sách.'], rid)
    clone_row_after(ev, r'^Bấm Lưu và duyệt$',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # ---------- 2.8 Xem chi tiết
    s = section(doc, r'^2\.8 ')
    kv_append(sec_kv(s), 'Dòng sự kiện phụ', '• Phiếu loại Thu nhà cung cấp → không hiển thị khối Đánh dấu không '
                                             'báo tiền về.')
    ui = sec_ui(s)
    ui_set(ui, r'^Khối Đánh dấu không báo tiền về', 'Mô tả',
           'Gồm STT, Đối tượng, Hợp đồng, Số tiền (VND), Chưa điều chỉnh, Diễn giải và ô tích; ô tích bị khóa khi '
           'người dùng không có quyền Quản lý phiếu báo có. Không hiển thị với phiếu Thu nhà cung cấp.')

    # ---------- 2.9 Duyệt
    s = section(doc, r'^2\.9 ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống sinh bút toán và ghi vào sổ cái.',
        '6. Ghi nhận hành động Duyệt trong lịch sử của phiếu và gửi thông báo cho người có quyền Quản lý phiếu báo có '
        'cùng công ty.',
        '7. Hệ thống báo “Duyệt phiếu báo có thành công.”, nạp lại danh sách (duyệt từ màn chi tiết thì quay về màn '
        'danh sách).'])
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm Duyệt$', r'^– Hiển thị “Duyệt phiếu báo có thành công.”',
            '– Hiển thị “Duyệt phiếu báo có thành công.” và nạp lại danh sách; duyệt từ màn chi tiết thì quay về màn '
            'danh sách.')
    add_err_line(ev, r'^Bấm Duyệt$', rid)

    # ---------- 2.10 Xóa
    s = section(doc, r'^2\.10 ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^4\. ', [
        '4. Hệ thống ghi nhận hành động Xóa trong lịch sử, xóa các dòng chi tiết rồi xóa phiếu.',
        '5. Hệ thống báo “Xóa thành công.” và nạp lại danh sách (xóa từ màn chi tiết thì quay về màn danh sách).'])
    add_err_line(sec_ev(s), r'^Bấm Xóa$', rid)

    # ---------- 2.11 Không báo tiền về
    s = section(doc, r'^2\.11 ')
    kv_append(sec_kv(s), 'Dòng sự kiện phụ', '• Phiếu loại Thu nhà cung cấp → màn chi tiết không có khối này.')
    add_err_line(sec_ev(s), r'^Tích / bỏ tích', rid)

    # ---------- 2.12 Lịch sử
    s = section(doc, r'^2\.12 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu chưa có thao tác nào',
            '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → hiện “Chưa có lịch sử thao tác '
            'nào.”')
    ui = sec_ui(s)
    ui_set(ui, r'^Tiêu đề cửa sổ', 'Giá trị ban đầu', 'Lịch sử thay đổi: <mã phiếu>')
    ui_set(ui, r'^Nút Bộ lọc', 'Mô tả', 'Hiện khi phiếu đã có lịch sử; lọc theo nhóm thao tác và khoảng thời gian.')
    ui_set(ui, r'^Trạng thái rỗng', 'Mô tả', 'Hiện “Chưa có lịch sử thao tác nào.” với phiếu lập từ hệ thống cũ, '
                                             'chưa có thao tác nào trên hệ thống mới.')

    # ---------- 2.13 Import
    s = section(doc, r'^2\.13 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ',
            '5. Người dùng sửa các dòng lỗi ngay trên bảng rồi bấm Validate lại, hoặc bấm “Bỏ dòng lỗi” để loại các '
            'dòng lỗi.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. ',
            '6. Khi không còn dòng lỗi, người dùng bấm “Import”; hệ thống kiểm tra lại toàn bộ rồi tạo phiếu cho các '
            'dòng.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^7\. ', [
        '7. Ghi nhận hành động Import trong lịch sử của từng phiếu được tạo.',
        '8. Hệ thống báo số phiếu tạo thành công (và số dòng lỗi nếu có), đóng cửa sổ và nạp lại danh sách.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Không dòng nào hợp lệ', [
        '• Còn dòng lỗi hoặc không dòng nào hợp lệ → nút Import bị khóa.',
        '• Sau Validate, ô Tổng / Hợp lệ / Lỗi hiện số dòng tương ứng; dòng lỗi tô đỏ và liệt kê lý do ngay dưới dòng; '
        'dòng hợp lệ bị khóa không sửa được (muốn sửa thì bấm “Xoá trạng thái validate”).'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Một dòng lỗi khi ghi',
            '• Một dòng lỗi phát sinh lúc ghi ở máy chủ → chỉ dòng đó thất bại, các dòng còn lại vẫn được tạo.')
    kv_append(kv, 'Dòng sự kiện phụ', '• Bấm Đóng / (x) → đóng cửa sổ, không tạo phiếu nào; bấm Làm mới → xóa file và '
                                      'bảng xem trước để chọn lại từ đầu.')
    ui = sec_ui(s)
    ui_set(ui, r'^Nút Tải file mẫu', 'Mô tả', 'Tải file Mau_import_phieu_bao_co.xlsx (sheet Data) gồm dòng tiêu đề '
                                              'và một dòng ví dụ; cấu trúc cột xem mục Cấu trúc file mẫu bên dưới.')
    ui_set(ui, r'^Nút Load lên bảng', 'Giá trị ban đầu', 'Mờ khi chưa chọn file')
    ui_set(ui, r'^Nút Validate', 'Giá trị ban đầu', 'Mờ khi chưa có dữ liệu')
    ui_set(ui, r'^Nút Import$', 'Giá trị ban đầu', 'Mờ khi chưa Validate')
    ui_set(ui, r'^Nút Import$', 'Mô tả', 'Chỉ bấm được khi đã Validate, có ít nhất một dòng hợp lệ và không còn dòng '
                                         'lỗi. Tạo phiếu cho các dòng.')
    tr = find_row(ui, 1, r'^Nút Chỉ dòng lỗi')
    vals = ['Nút Bỏ dòng lỗi', 'Button', 'Enable', '–', '–', 'Hiển thị khi có dữ liệu',
            'Loại khỏi bảng các dòng lỗi sau khi Validate để có thể Import phần còn lại.']
    for tc, v in zip(cells(tr)[1:], vals):
        write_cell(tc, [v])
    clone_row_after(ui, r'^Nút Bỏ dòng lỗi', [None, 'Nút Xoá trạng thái validate', 'Button', 'Enable', '–', '–',
                                             'Hiển thị khi có dữ liệu',
                                             'Bỏ kết quả kiểm tra để sửa lại cả dòng hợp lệ, sau đó Validate lại.'])
    ui_set(ui, r'^Ô thông báo kết quả', 'Loại', 'Label')
    ui_set(ui, r'^Ô thông báo kết quả', 'Mô tả', 'Ô Tổng luôn hiện số dòng đang xem trước; sau Validate hiện thêm ô '
                                                 'Hợp lệ, Lỗi và dòng “Kiểm tra xong: X dòng hợp lệ, Y dòng lỗi”.')
    clone_row_after(ui, r'^Ô thông báo kết quả', [None, 'Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
                                                  'Xóa file và bảng xem trước để chọn lại từ đầu.'])
    clone_row_after(ui, r'^Nút Làm mới$', [None, 'Nút Đóng / (x)', 'Button', 'Enable', '–', '–', 'Hiển thị',
                                           'Đóng cửa sổ, không tạo phiếu nào.'])
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm Import$', r'^– Kiểm tra lại toàn bộ dòng ở máy chủ',
            '– Nút chỉ bấm được khi không còn dòng lỗi; máy chủ vẫn kiểm tra lại toàn bộ dòng, dòng nào lỗi phát '
            'sinh lúc ghi thì bỏ qua dòng đó.')
    add_err_line(ev, r'^Bấm Validate$', rid)
    add_err_line(ev, r'^Bấm Import$', rid)

    # ---------- 2.14 Tổng hợp tiền về ngân hàng
    s = section(doc, r'^2\.14 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^1\. Người dùng vào menu', '1. Người dùng vào menu %s.' % SUM_MENU)
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Dòng đã điều chỉnh hết',
            '• Dòng đã điều chỉnh hết công nợ → ô ở cột Điều chỉnh công nợ để trống, không chọn được.')
    ui = sec_ui(s)
    ui_set(ui, r'^Ô lọc Ghi chú', 'Tên đối tượng', 'Ô lọc Diễn giải')
    ui_set(ui, r'^Ô lọc Người lập', 'Tên đối tượng', 'Ô lọc Người tạo')
    ui_set(ui, r'^Ô lọc Lọc phiếu', 'Tên đối tượng', 'Ô lọc Trạng thái')
    tr = find_row(ui, 1, r'^Ô lọc Số tiền')
    write_cell(cells(tr)[1], ['Ô lọc Số tiền'])
    write_cell(cells(tr)[2], ['Textbox'])
    write_cell(cells(tr)[6], ['Một ô gồm hai ô nhập Từ → Đến; lọc theo số tiền quy đổi của dòng.'])
    tr = find_row(ui, 1, r'^Ô lọc Hạch toán')
    write_cell(cells(tr)[1], ['Ô lọc Ngày hạch toán'])
    write_cell(cells(tr)[6], ['Một ô gồm hai lịch Từ ngày → Đến ngày; lọc theo ngày hạch toán của phiếu cha.'])
    ui_set(ui, r'^Cột Số báo có', 'Mô tả', 'Là đường dẫn mở màn chi tiết phiếu báo có; cột cố định; sắp xếp được.')
    ui_set(ui, r'^Cột Ngày hạch toán', 'Mô tả', 'Sắp xếp được.')
    ui_set(ui, r'^Cột Người lập', 'Tên đối tượng', 'Cột Người tạo')
    ui_set(ui, r'^Cột Ngân hàng / STK', 'Mô tả', 'Hai cột riêng; cột Ngân hàng sắp xếp được.')
    ui_set(ui, r'^Cột Số tiền chưa điều chỉnh', 'Mô tả', 'Bằng Số tiền trừ đi phần đã điều chỉnh công nợ; sắp xếp '
                                                         'được.')
    ui_set(ui, r'^Cột Trạng thái', 'Loại', 'Table/Grid')
    ui_set(ui, r'^Cột Điều chỉnh công nợ', 'Mô tả', 'Chỉ dòng còn tiền chưa điều chỉnh mới có ô tích; dòng khác để '
                                                    'trống.')
    clone_row_after(ui, r'^Nút Xuất Excel', [None, 'Nút Cài đặt bộ lọc / Cấu hình cột hiển thị', 'Button', 'Enable',
                                             '–', 'Hiển thị', 'Chọn ô lọc / cột hiển thị và thứ tự, lưu theo người '
                                             'dùng (như màn Phiếu báo có).'])

    # ---------- 2.15 Xuất Excel
    s = section(doc, r'^2\.15 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^3\. ', '3. Người dùng tích / bỏ tích các trường, kéo biểu tượng ☰ để đổi '
                                               'thứ tự cột trong file.')
    kv_append(kv, 'Dòng sự kiện phụ', ['• Kết quả lọc rỗng → vẫn xuất file gồm logo, tiêu đề, dòng tên cột và dòng '
                                       '“Không có dữ liệu phù hợp”.',
                                       '• Không giới hạn số dòng: file lấy toàn bộ dòng khớp bộ lọc.'])
    ui = sec_ui(s)
    ui_set(ui, r'^Danh sách Trường xuất', 'Loại', 'Checkbox')
    tr = find_row(ui, 1, r'^Dòng thứ tự cột')
    write_cell(cells(tr)[1], ['Biểu tượng kéo ☰'])
    write_cell(cells(tr)[2], ['Icon'])
    write_cell(cells(tr)[3], ['Enable'])
    write_cell(cells(tr)[7], ['Kéo để đổi vị trí trường; thứ tự cột trong file đúng bằng thứ tự trong danh sách.'])
    clone_row_after(ui, r'^Biểu tượng kéo', [None, 'Số trường đang chọn', 'Label', 'Read-only', '–', '–',
                                             'Đang chọn 10/10 trường', 'Góc trái cuối cửa sổ, cập nhật khi tích / bỏ '
                                             'tích.'])
    add_err_line(sec_ev(s), r'^Bấm Xuất file', rid)


def add_import_template_table(doc):
    """2.13: thêm mục 'Cấu trúc file mẫu import' (STT | Tên cột | Bắt buộc | Mô tả) trước mục event."""
    s = section(doc, r'^2\.13 ')
    ev_head = next(e for e in s[1] if _is_sub(e) and 'Danh sách event' in txt(e))
    h = no_bookmarks(strip_ids(copy.deepcopy(ev_head)))
    set_runs_text(h, '0.0.0 Cấu trúc file mẫu import')
    ev_head.addprevious(h)
    intro = strip_ids(docxlib.clone_par_after(h, sec_par(s, r'^Đường dẫn màn hình'),
                                              'File mẫu: bấm nút Tải file mẫu trong cửa sổ Import → tải file '
                                              'Mau_import_phieu_bao_co.xlsx, sheet Data. Dòng 1 là tên cột (cột có '
                                              'dấu * là bắt buộc), từ dòng 2 trở đi mỗi dòng là một khoản tiền về; '
                                              'một lần import tối đa 500 dòng.'))
    tpl = sec_ev(s)
    total = sum(int(gc.get(W('w'))) for gc in tpl.find(W('tblGrid')).findall(W('gridCol')))
    widths = [int(total * r) for r in (0.08, 0.22, 0.13)]
    widths.append(total - sum(widths))
    new_table_like(tpl, intro, ['STT', 'Tên cột', 'Bắt buộc', 'Mô tả'], IMPORT_COLS, widths)
    log('2.13: thêm bảng cấu trúc file mẫu import (%d cột)' % len(IMPORT_COLS))


def patch_part4(doc):
    h = part_heading(doc, 4)
    intro = h.getnext()
    set_rule_head(intro, 'Quy tắc áp dụng: Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
    set_rule_tail(intro, '. Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc đã có trong SRS '
                         'quy tắc chung.' % SCREEN)
    tbl = intro.getnext()
    while tbl.tag != W('tbl'):
        tbl = tbl.getnext()

    def desc(code, old_regex, new):
        tc = cells(find_row(tbl, 1, '^%s$' % code))[3]
        write_cell(tc, lines_replace(cell_lines(tc), old_regex, new))

    desc('BR-03', r'^– Duyệt: phiếu ở trạng thái Đang tạo',
         '– Duyệt: phiếu ở trạng thái Đang tạo và người dùng có quyền Quản lý phiếu báo có; hệ thống không bắt buộc là '
         'người lập, nhưng phiếu Đang tạo chỉ người lập nhìn thấy nên thực tế người duyệt là người lập.')
    desc('BR-10', r'^– Trạng thái của dòng được tính',
         '– Trạng thái của dòng được tính tại thời điểm xem: còn tiền chưa điều chỉnh là “Chưa điều chỉnh hết công '
         'nợ”, ngược lại là “Đã điều chỉnh hết công nợ”.')
    desc('BR-12', r'^– Toàn bộ dòng được kiểm tra trước khi ghi',
         '– Toàn bộ dòng được kiểm tra trước khi ghi; nút Import chỉ bấm được khi không còn dòng lỗi (sửa rồi Validate '
         'lại, hoặc Bỏ dòng lỗi). Lỗi phát sinh lúc ghi chỉ làm hỏng dòng đó, dòng khác vẫn được tạo.')
    for i, tr in enumerate(rows(tbl)[1:], 1):
        assert txt(cells(tr)[1]).strip() == 'BR-%02d' % i, 'Mã BR không liên tục ở dòng %d' % i


def add_part5(doc):
    h4 = part_heading(doc, 4)
    anchor = doc.element.body[-1].getprevious()
    h5 = clone_heading(h4, 'Phần 5. Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    no_bookmarks(h5)
    intro = docxlib.clone_par_after(h5, h4.getnext(), 'Các màn hình dưới đây đọc dữ liệu do %s ghi ra (phiếu, dòng chi '
                                    'tiết và bút toán sổ kế toán sinh ra khi phiếu được duyệt).' % SCREEN)
    strip_ids(intro)
    tpl = sec_ev(section(doc, r'^2\.1 '))
    total = sum(int(gc.get(W('w'))) for gc in tpl.find(W('tblGrid')).findall(W('gridCol')))
    widths = [int(total * r) for r in (0.08, 0.15, 0.44)]
    widths.append(total - sum(widths))
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], PART5, widths)
    log('Thêm Phần 5 (%d màn tham chiếu)' % len(PART5))


if __name__ == '__main__':
    main()

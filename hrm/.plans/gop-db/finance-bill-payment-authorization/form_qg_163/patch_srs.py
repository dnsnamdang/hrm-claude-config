# -*- coding: utf-8 -*-
"""Vá SRS "Phiếu ủy nhiệm chi" (bản Drive 28/10) theo FORM "Danh mục quốc gia" (TPE Pass).

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/SRS - Phiếu ủy nhiệm chi.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Luôn đọc bản Drive gốc. Khuôn: finance-product-import-direct-transfer/form_qg/patch_srs.py.
Khác màn 27: tài liệu này dùng Heading4 cho mục con 2.x.y (màn 27 là đoạn in đậm thường) nên ghi đè
`is_sub` của formqg_lib.
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
NAME = 'SRS - Phiếu ủy nhiệm chi'
OUT = os.path.join(OUT_DIR, NAME + '.docx')
UML = os.path.join(HERE, 'uml')
SHOTS = os.path.join(HERE, 'hdsd_shots')


def _is_sub(e):
    return e.tag == W('p') and style_of(e) == 'Heading4' and re.match(r'^\d+\.\d+\.\d+ ', txt(e))


L.is_sub = _is_sub  # tài liệu này: mục con 2.x.y là Heading4

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'Phiếu ủy nhiệm chi'
# finance.js: hubGroup 'Quản lý tiền' > nhóm 'Thanh toán tiền mặt' > mục màn
MENU = 'Phân hệ Tài chính => Quản lý tiền => Thanh toán tiền mặt => Phiếu ủy nhiệm chi'
TAIL = ' Chỉ bổ sung quy tắc riêng của %s.' % SCREEN
UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: nếu chưa nhập hoặc thay đổi gì thì rời màn '
           'ngay; nếu đã nhập dữ liệu thì hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” '
           '(Thoát / Ở lại).')
UNSAVED_EV = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
              '– Đã nhập dữ liệu → hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”; '
              'bấm Thoát thì rời màn và bỏ thay đổi, bấm Ở lại thì giữ nguyên màn.']

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Phạm vi phiếu nhìn thấy theo quyền Xem tất cả phiếu ủy nhiệm chi của tổng công ty (V1) '
              'hoặc của công ty (V2); không có quyền nào thì chỉ thấy phiếu do mình lập hoặc mình duyệt.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (V1, V2); không có quyền nào vẫn xem được phiếu do chính mình lập hoặc duyệt.')
ACTOR_Q1 = 'Người dùng có quyền thực hiện chức năng: quyền Kế toán thanh toán (Q1).'
ACTOR_OWNER = 'Người lập phiếu có quyền thực hiện chức năng: quyền Kế toán thanh toán (Q1).'
COND_OWNER = ('1. Đăng nhập thành công.\n'
              '2. Có quyền Kế toán thanh toán (Q1) và là người lập phiếu.\n'
              '3. Phiếu đang ở trạng thái Đang tạo.')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người lập phiếu, người duyệt phiếu, hoặc người có quyền Xem tất cả '
               'phiếu ủy nhiệm chi của tổng công ty (V1) / của công ty (V2) trong phạm vi được giao.')
COND_SCOPE = ('1. Đăng nhập thành công.\n'
              '2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu nằm trong phạm vi dữ liệu của người dùng; phiếu Đang tạo chỉ người lập xem được.')
COND_Q1 = ('1. Đăng nhập thành công.\n'
           '2. Có quyền Kế toán thanh toán (Q1). Nút Tạo mới hiển thị với mọi người vào được màn, nhưng không có Q1 '
           'thì không chọn được phiếu đề nghị, không lấy được số liệu thu nhập và không lưu được phiếu.')

# Mục 2.x SAU KHI TÁCH (số mục mới): regex -> (vế sau link, Tác nhân, Điều kiện ban đầu)
SECTIONS = {
    r'^2\.1 ': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 ': ('Màn Danh sách và Tìm kiếm, lọc dữ liệu.', ACTOR_LIST, COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.3 ': ('Bộ lọc và Cài đặt bộ lọc.', ACTOR_LIST, COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.4 ': ('Cấu hình cột.', ACTOR_LIST, COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.5 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_Q1,
                COND_Q1 + '\n3. Có phiếu đề nghị thanh toán ở trạng thái “Chờ tạo phiếu chi”, hình thức chuyển khoản.'),
    r'^2\.6 ': ('Popup tra cứu dữ liệu, Tìm kiếm và Phân trang.', ACTOR_Q1,
                '1. Đăng nhập thành công.\n2. Có quyền Kế toán thanh toán (Q1).\n'
                '3. Đang ở màn Tạo mới hoặc Sửa phiếu.'),
    r'^2\.7 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_Q1,
                COND_Q1 + '\n3. Xác định được công ty của người đăng nhập.'),
    r'^2\.8 ': ('Màn Chỉnh sửa, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.9 ': ('Hộp xác nhận thao tác, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', ACTOR_Q1,
                '1. Đăng nhập thành công.\n2. Có quyền Kế toán thanh toán (Q1); ở màn Sửa phải là người lập phiếu.\n'
                '3. Phiếu đang lập mới, hoặc đang ở trạng thái Đang tạo.'),
    r'^2\.10 ': ('Màn Xem chi tiết và Phân quyền.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.11 ': ('Quy tắc xóa và Thông báo.', ACTOR_OWNER, COND_OWNER),
    r'^2\.12 ': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_SCOPE, COND_SCOPE),
}

MENU_LINES = {
    r'^2\.3 ': ('Menu: %s => Cài đặt bộ lọc' % MENU,
                'Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.4 ': ('Menu: %s => Tùy chỉnh cột (biểu tượng cột cạnh nút Tạo mới)' % MENU,
                'Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.6 ': ('Menu: %s => Tạo mới / Sửa => bấm ô Số phiếu đề nghị' % MENU,
                'Modal Chọn phiếu đề nghị chi được mở ngay trên màn hình Tạo mới hoặc Sửa phiếu theo đường dẫn ở trên.'),
    r'^2\.9 ': ('Menu: %s => Tạo mới / Sửa => Lưu và duyệt' % MENU,
                'Modal Xác nhận lưu và duyệt được mở ngay trên màn hình Tạo mới hoặc Sửa phiếu theo đường dẫn ở trên.'),
    r'^2\.10 ': ('Menu: %s => bấm Mã phiếu' % MENU, None),
    r'^2\.11 ': ('Menu: %s => Xóa (trên dòng phiếu) / bấm Mã phiếu => Xóa' % MENU,
                 'Modal Xác nhận xóa được mở ngay trên màn hình danh sách (biểu tượng Xóa trên dòng) hoặc màn hình '
                 'chi tiết phiếu (nút Xóa) theo đường dẫn ở trên.'),
    r'^2\.12 ': ('Menu: %s => Lịch sử (trên dòng phiếu) / bấm Mã phiếu => Xem lịch sử' % MENU,
                 'Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối Lịch sử '
                 'nằm cuối màn hình chi tiết phiếu.'),
}

USECASES = {  # mục mới -> (actor, mã, tên, nhóm)
    r'^2\.5 ': ('Kế toán thanh toán', 'FR-05', 'Tạo mới phiếu ủy nhiệm chi', 'crud'),
    r'^2\.6 ': ('Kế toán thanh toán', 'FR-06', 'Chọn phiếu đề nghị chi', 'crud'),
    r'^2\.7 ': ('Kế toán thanh toán', 'FR-07', 'Tạo phiếu Chi thu nhập cho nhân viên', 'crud'),
    r'^2\.8 ': ('Người lập phiếu', 'FR-08', 'Chỉnh sửa phiếu ủy nhiệm chi', 'crud'),
    r'^2\.9 ': ('Kế toán thanh toán', 'FR-09', 'Lưu và duyệt phiếu ủy nhiệm chi', 'action'),
    r'^2\.10 ': ('Người dùng có quyền', 'FR-10', 'Xem chi tiết phiếu ủy nhiệm chi', 'view'),
    r'^2\.11 ': ('Người lập phiếu', 'FR-11', 'Xóa phiếu ủy nhiệm chi', 'action'),
}

# Ảnh thay mới (chụp DEV 28/10): regex chú thích CŨ -> (ảnh, chú thích mới hoặc None)
IMAGES = [
    (r'Màn Danh sách phiếu ủy nhiệm chi', '01_list', None),
    (r'Khối “Tìm kiếm nâng cao”', '02_filter', 'Khối “Tìm kiếm nâng cao” đang mở với đủ 10 ô lọc'),
    (r'Form Tạo mới phiếu ủy nhiệm chi khi vừa mở', '10_create', None),
    (r'Form sau khi chọn phiếu đề nghị', '10b_filled', None),
    (r'Cửa sổ Chọn phiếu đề nghị chi', '11_request', None),
    (r'Form khi chọn Loại chi', '12_income', None),
    (r'Tab “Chi tiết vụ việc”', '12b_vuviec', None),
    (r'Màn Sửa phiếu ủy nhiệm chi', '15_edit', 'Màn Sửa phiếu ủy nhiệm chi'),
    (r'Hộp “Xác nhận lưu và duyệt”', '14_approve', None),
    (r'Màn chi tiết phiếu đã hạch toán', '17_detail', 'Màn chi tiết phiếu đã hạch toán'),
    (r'Màn chi tiết phiếu “Đang tạo”', '17c_draft', None),
    (r'Hộp “Xác nhận xóa”', '13_delete', 'Hộp “Xác nhận xóa” mở từ màn danh sách'),
    (r'Cửa sổ “Lịch sử thay đổi”', '16_history', 'Cửa sổ “Lịch sử thay đổi” của phiếu'),
]

PART5 = [  # STT | Nhóm | Màn hình | Đường dẫn
    ('1', 'Tài chính', 'Đề nghị thanh toán (số tiền duyệt chi của phiếu đề nghị lấy theo phiếu ủy nhiệm chi đã '
     'lập; nút “Tạo phiếu ủy nhiệm chi” trên dòng phiếu đề nghị; số đã thanh toán chi phí vận chuyển NCC)',
     'Tài chính -> Quản lý tiền -> Đề nghị -> Đề nghị thanh toán'),
    ('2', 'Tài chính', 'Khai báo đầu kỳ công nợ (khách hàng / nhà cung cấp đã phát sinh phiếu ủy nhiệm chi thì '
     'khai báo đầu kỳ bị khóa)', 'Tài chính -> Khai báo đầu kỳ -> Khai báo đầu kỳ công nợ'),
    ('3', 'Bán hàng', 'Đối chiếu công nợ 1 KH (phiếu ủy nhiệm chi trả lại khách hàng là chứng từ hoàn tiền trên '
     'báo cáo)', 'Bán hàng -> Báo cáo công nợ -> Đối chiếu công nợ 1 KH'),
    ('4', 'Tài chính', 'Danh mục tài khoản, Danh mục tiền tệ (chặn xóa tài khoản / loại tiền đang dùng trên phiếu '
     'ủy nhiệm chi)', 'Tài chính -> Danh mục -> Danh mục tài khoản / Danh mục tiền tệ'),
    ('5', 'Danh mục dùng chung', 'Ngân hàng (chặn xóa ngân hàng đang là Ngân hàng chuyển của phiếu ủy nhiệm chi)',
     'Danh mục dùng chung -> Ngân hàng'),
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


def ui_type(ui, name_regex, new):
    set_col(ui, header_index(ui, 'Loại'), name_regex, new)


def ui_desc(ui, name_regex, new):
    set_col(ui, header_index(ui, 'Mô tả'), name_regex, new)


def no_bookmarks(el):
    for tag in ('bookmarkStart', 'bookmarkEnd'):
        for b in list(el.iter(W(tag))):
            b.getparent().remove(b)
    return el


def heading3s(doc):
    return [e for e in items(doc) if e.tag == W('p') and style_of(e) == 'Heading3']


def find_h3(doc, title_regex):
    for e in heading3s(doc):
        if re.search(title_regex, txt(e)):
            return e
    raise KeyError(title_regex)


def sec_by_title(doc, title_regex):
    return section(doc, r'^\d+\.\d+ ' + title_regex)


def set_caption(cap, text):
    m = re.match(r'^(Hình \d+:\s*)', txt(cap))
    set_runs_text(cap, (m.group(1) if m else 'Hình 0: ') + text)


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
    assert n == 5, 'Mong 5 tiêu đề chưa đặt heading, thấy %d' % n


def renumber_fr(doc):
    """FR-04..FR-11 -> FR-05..FR-12 (tách FR-03 thành 2). Chạy TRƯỚC khi ghi FR-04 mới."""
    n = 0
    for t in doc.element.body.iter(W('t')):
        if t.text and re.search(r'FR-\d\d', t.text):
            new = re.sub(r'FR-(\d\d)', lambda m: 'FR-%02d' % (int(m.group(1)) + (1 if int(m.group(1)) >= 4 else 0)),
                         t.text)
            if new != t.text:
                t.text = new
                n += 1
    log('Đánh lại mã FR (tách FR-03): %d chỗ' % n)


def split_fr03(doc):
    """2.3 'Cài đặt bộ lọc và Tuỳ chỉnh cột' -> 2.3 Cài đặt bộ lọc + 2.4 Tùy chỉnh cột hiển thị."""
    sec = section(doc, r'^2\.3 ')
    remove_usecase(doc, sec)
    sec = section(doc, r'^2\.3 ')
    els = [sec[0]] + sec[1]
    clones = [no_bookmarks(strip_ids(copy.deepcopy(e))) for e in els]
    anchor = els[-1]
    for c in clones:
        anchor.addnext(c)
        anchor = c
    set_runs_text(sec[0], '2.3 Cài đặt bộ lọc')
    set_runs_text(clones[0], '2.4 Tùy chỉnh cột hiển thị')

    # ---- 2.3 Cài đặt bộ lọc
    s = section(doc, r'^2\.3 ')
    kv = sec_kv(s)
    kv_set(kv, 'Tên chức năng', 'Cài đặt bộ lọc hiển thị')
    kv_set(kv, 'Mô tả', 'Chọn ô lọc nào hiển thị trong khối Tìm kiếm nâng cao và thứ tự của chúng. Cấu hình được '
                        'ghi nhớ riêng cho từng người dùng.')
    kv_set(kv, 'Dòng sự kiện chính', '1. Người dùng bấm nút “Cài đặt bộ lọc”.\n'
           '2. Hệ thống mở cửa sổ liệt kê 10 ô lọc kèm ô tích và tay nắm kéo.\n'
           '3. Người dùng tích / bỏ tích, kéo đổi thứ tự.\n4. Người dùng bấm Lưu.\n'
           '5. Hệ thống ghi nhớ cấu hình cho người dùng đó và vẽ lại khối lọc ngay.')
    kv_set(kv, 'Dòng sự kiện phụ', '• Bấm “Khôi phục mặc định” → đưa về đủ 10 ô lọc theo thứ tự ban đầu.\n'
           '• Bỏ tích một ô lọc đang có giá trị → hệ thống xóa luôn giá trị đó để không lọc ngầm bằng ô không nhìn thấy.\n'
           '• Bấm Đóng / (x) → đóng cửa sổ, giữ nguyên cấu hình cũ.')
    ui = sec_ui(s)
    write_cell(cells(find_row(ui, 1, r'^Tiêu đề cửa sổ'))[header_index(ui, 'Giá trị ban đầu')], ['Cài đặt bộ lọc'])
    write_cell(cells(find_row(ui, 1, r'^Tiêu đề cửa sổ'))[header_index(ui, 'Mô tả')], ['–'])
    ui_type(ui, r'^Danh sách mục lọc', 'Checkbox')
    ui_desc(ui, r'^Danh sách mục lọc', 'Mã phiếu, Mã phiếu đề nghị chi, Loại chi, Trạng thái, Người lập, Người đề '
                                       'nghị, Công ty, Phòng ban, Bộ phận, Ngày lập.')
    ui_type(ui, r'^Tay nắm kéo', 'Icon')
    ui_desc(ui, r'^Tay nắm kéo', 'Kéo thả để đổi thứ tự ô lọc.')
    ui_desc(ui, r'^Nút Khôi phục mặc định', 'Đưa danh sách ô lọc về cấu hình ban đầu.')
    for rx in (r'^Danh sách cột', r'^Ô tích của cột bắt buộc', r'^Nút Chọn tất cả', r'^Nút Bỏ chọn hết',
               r'^Số cột đang chọn'):
        delete_row(ui, rx)
    ev = sec_ev(s)
    write_cell(cells(find_row(ev, 1, r'^Bỏ tích một mục'))[3],
               ['After:', '– Ô lọc được đánh dấu tắt trong cửa sổ; nếu ô đang có giá trị lọc thì giá trị đó bị xóa '
                'khi bấm Lưu.'])
    set_col(ev, 2, r'^Kéo đổi thứ tự', 'Drag')
    write_cell(cells(find_row(ev, 1, r'^Kéo đổi thứ tự'))[3], ['After:', '– Cập nhật thứ tự tạm trong cửa sổ.'])
    delete_row(ev, r'^Bấm Chọn tất cả')
    write_cell(cells(find_row(ev, 1, r'^Bấm Lưu'))[3],
               ['After:', '– Ghi nhớ cấu hình cho riêng người dùng, vẽ lại khối lọc và đóng cửa sổ.',
                '– Cấu hình vẫn còn sau khi tải lại trang hoặc đăng nhập lại.'])

    # ---- 2.4 Tùy chỉnh cột hiển thị
    s = section(doc, r'^2\.4 ')
    kv = sec_kv(s)
    kv_set(kv, 'Tên chức năng', 'Tùy chỉnh cột hiển thị của danh sách')
    kv_set(kv, 'Mô tả', 'Chọn cột nào hiển thị trên bảng danh sách và thứ tự cột. Cấu hình được ghi nhớ riêng cho '
                        'từng người dùng.')
    kv_set(kv, 'Dòng sự kiện chính', '1. Người dùng bấm biểu tượng Cấu hình cột hiển thị cạnh nút Tạo mới.\n'
           '2. Hệ thống mở cửa sổ Tùy chỉnh cột với danh sách 13 cột kèm ô tích và tay nắm kéo.\n'
           '3. Người dùng tích / bỏ tích, kéo đổi thứ tự.\n4. Người dùng bấm Lưu.\n'
           '5. Hệ thống ghi nhớ cấu hình cho người dùng đó và vẽ lại bảng ngay.')
    kv_set(kv, 'Dòng sự kiện phụ', '• Cột bắt buộc (STT, Mã phiếu, Hành động) → không bỏ tích và không kéo được.\n'
           '• Hai cột Số tiền duyệt chi và Ngày hạch toán mặc định tắt.\n'
           '• Bấm Đóng / (x) → đóng cửa sổ, giữ nguyên cấu hình cũ.')
    ui = sec_ui(s)
    write_cell(cells(find_row(ui, 1, r'^Tiêu đề cửa sổ'))[header_index(ui, 'Giá trị ban đầu')], ['Tuỳ chỉnh cột'])
    write_cell(cells(find_row(ui, 1, r'^Tiêu đề cửa sổ'))[header_index(ui, 'Mô tả')], ['–'])
    delete_row(ui, r'^Danh sách mục lọc')
    delete_row(ui, r'^Nút Khôi phục mặc định')
    ui_type(ui, r'^Danh sách cột', 'Checkbox')
    ui_type(ui, r'^Ô tích của cột bắt buộc', 'Checkbox')
    ui_type(ui, r'^Tay nắm kéo', 'Icon')
    ui_desc(ui, r'^Nút Chọn tất cả', 'Nằm phía trên danh sách cột. Tích tất cả các cột; chưa áp dụng lên bảng cho '
                                     'tới khi bấm Lưu.')
    ui_desc(ui, r'^Nút Bỏ chọn hết', 'Bỏ tích tất cả các cột không bắt buộc; cột bắt buộc (có biểu tượng ổ khóa) '
                                     'vẫn luôn hiển thị.')
    ui_desc(ui, r'^Số cột đang chọn', 'Góc trái cuối cửa sổ, cập nhật ngay khi tích / bỏ tích hoặc bấm Chọn tất cả '
                                      '/ Bỏ chọn hết.')
    ev = sec_ev(s)
    write_cell(cells(find_row(ev, 1, r'^Bỏ tích một mục'))[1], ['Bỏ tích một cột'])
    write_cell(cells(find_row(ev, 1, r'^Bỏ tích một cột'))[3],
               ['During:', '– Cột bắt buộc → không cho bỏ tích, hiện chú thích “Cột bắt buộc — không thể ẩn hoặc đổi '
                'vị trí”.', 'After:', '– Cột được đánh dấu tắt trong cửa sổ, chưa áp dụng lên bảng.'])
    set_col(ev, 2, r'^Kéo đổi thứ tự', 'Drag')
    write_cell(cells(find_row(ev, 1, r'^Bấm Lưu'))[3],
               ['After:', '– Ghi nhớ cấu hình cho riêng người dùng, vẽ lại bảng và đóng cửa sổ.',
                '– Cấu hình vẫn còn sau khi tải lại trang hoặc đăng nhập lại.'])

    # ---- Ma trận phân quyền: tách dòng FR-03
    mt = None
    for t in doc.element.body.iter(W('tbl')):
        if txt(cells(rows(t)[0])[0]).strip() == 'Chức năng':
            mt = t
            break
    tr = find_row(mt, 0, r'^FR-03')
    write_cell(cells(tr)[0], ['FR-03 Cài đặt bộ lọc'])
    new = strip_ids(copy.deepcopy(tr))
    tr.addnext(new)
    write_cell(cells(new)[0], ['FR-04 Tùy chỉnh cột hiển thị'])
    log('Tách FR-03 thành FR-03 Cài đặt bộ lọc + FR-04 Tùy chỉnh cột hiển thị (bỏ Use Case)')


def renumber_headings(doc):
    k = 0
    in_p3 = False
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1':
            in_p3 = txt(e).startswith('Phần 3')
        if in_p3 and e.tag == W('p') and style_of(e) == 'Heading3':
            k += 1
            new = re.sub(r'^\d+\.\d+', '2.%d' % k, txt(e))
            if new != txt(e):
                set_runs_text(e, new)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)

    fix_unstyled_subheadings(doc)
    renumber_fr(doc)
    split_fr03(doc)
    renumber_headings(doc)

    # Quy tắc chung / Tác nhân / Điều kiện ban đầu
    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    # Dòng Menu + câu popup (ngay sau dòng Menu đầu tiên của mục)
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

    replace_in_texts(doc.element.body, '=> Xem chi tiết (phiếu nháp)', '=> bấm Mã phiếu (phiếu nháp)')
    patch_sections(doc, rid)
    replace_images(doc)
    patch_part4(doc)
    add_part5(doc)

    # Use Case: vẽ lại kiểu quốc gia, thêm cho Xem chi tiết
    for rx, (actor, code, name, grp) in USECASES.items():
        png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
        draw_usecase_qg(png, actor, code, name, grp)
        sec = section(doc, rx)
        blk = usecase_block(sec)
        cap = 'Biểu đồ Use Case — %s %s' % (code, name)
        if blk is None:
            add_usecase(doc, sec, section(doc, r'^2\.11 '), png, cap)
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
    mains = [('FR-01', 'Xem danh sách', 'view'), ('FR-05', 'Tạo mới phiếu', 'crud'),
             ('FR-08', 'Chỉnh sửa phiếu', 'crud'), ('FR-10', 'Xem chi tiết phiếu', 'view')]
    subs = [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
            ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
            ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
            ('FR-12', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
            ('FR-06', 'Chọn phiếu đề nghị chi', 'crud', 'include', [1, 2], None),
            ('FR-07', 'Chi thu nhập cho nhân viên', 'crud', 'extend', [1], None),
            ('FR-09', 'Lưu và duyệt', 'action', 'extend', [2, 1], None),
            ('FR-11', 'Xóa phiếu', 'action', 'extend', [3], None)]
    actors = [('Kế toán thanh toán', [0, 1, 2, 3]), ('Người có quyền xem phiếu ủy nhiệm chi', [0, 3])]
    U.draw_overview2(png, actors, mains, subs)
    sec_h = next(e for e in items(doc) if e.tag == W('p') and style_of(e) == 'Heading2'
                 and 'Sơ đồ UML tổng quan' in txt(e))
    img = sec_h.getnext()
    while not list(img.iter(A_NS + 'blip')):
        img = img.getnext()
    set_image(doc, img, png)
    log('Vẽ lại sơ đồ Use Case tổng quan (mã FR mới)')


def replace_images(doc):
    for cap_rx, shot, new_cap in IMAGES:
        path = os.path.join(SHOTS, shot + '.png')
        hit = None
        for e in items(doc):
            if e.tag == W('p') and re.match(r'^Hình \d+:\s*' + cap_rx, txt(e)):
                hit = e
                break
        assert hit is not None, 'Không thấy chú thích ' + cap_rx
        if not os.path.exists(path):
            log('THIẾU ảnh %s — giữ ảnh cũ ở "%s"' % (shot, txt(hit)))
            continue
        img = hit.getprevious()
        assert list(img.iter(A_NS + 'blip')), 'đoạn trước chú thích không phải ảnh: ' + txt(hit)
        set_image(doc, img, path)
        if new_cap:
            set_caption(hit, new_cap)
        log('Thay ảnh %s → %s' % (txt(hit)[:50], shot))
    # Mục tách đôi: 2.3 dùng ảnh Cài đặt bộ lọc, 2.4 giữ ảnh Tùy chỉnh cột
    for rx, shot, cap in ((r'^2\.3 ', '26_filtercfg', 'Cửa sổ “Cài đặt bộ lọc”'),
                          (r'^2\.4 ', '25_colcfg', 'Cửa sổ “Tùy chỉnh cột” — cột bắt buộc có biểu tượng ổ khoá')):
        s = section(doc, rx)
        capp = sec_par(s, r'^Hình \d+:')
        set_image(doc, capp.getprevious(), os.path.join(SHOTS, shot + '.png'))
        set_caption(capp, cap)


def patch_sections(doc, rid):
    # ---------- 2.1 Xem danh sách
    s = section(doc, r'^2\.1 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^1\. Người dùng vào menu', '1. Người dùng vào menu %s.' % MENU)
    ui = sec_ui(s)
    ui_type(ui, r'^Cột Trạng thái$', 'Table/Grid')
    delete_row(ui, r'^Vòng quay chờ')
    ui_desc(ui, r'^Nút Tạo mới$',
            'Luôn hiển thị với mọi người vào được màn (nút không gắn quyền). Người không có quyền Kế toán thanh toán '
            'vẫn mở được màn Thêm mới nhưng không chọn được phiếu đề nghị, không lấy được số liệu thu nhập nhân viên; '
            'bấm Lưu nháp / Lưu và duyệt thì hệ thống kiểm tra dữ liệu nhập trước, hợp lệ rồi mới báo “Bạn không có '
            'quyền lập phiếu ủy nhiệm chi” và không lưu.')
    ui_desc(ui, r'^Cột Mã phiếu đề nghị chi',
            'Liên kết mở màn Chi tiết Phiếu đề nghị thanh toán ở thẻ mới. Phiếu Chi thu nhập cho nhân viên (không '
            'có phiếu đề nghị) để trống ô này.')

    # ---------- 2.2 Tìm kiếm
    s = section(doc, r'^2\.2 ')
    ui = sec_ui(s)
    tr = find_row(ui, 1, r'^Ngày lập từ')
    write_cell(cells(tr)[1], ['Ngày lập'])
    write_cell(cells(tr)[header_index(ui, 'Phạm vi')], ['dd/mm/yyyy → dd/mm/yyyy'])
    write_cell(cells(tr)[header_index(ui, 'Mô tả')],
               ['Một ô gồm hai lịch Từ ngày → Đến ngày. Lọc theo NGÀY TẠO PHIẾU, lấy cả ngày đầu mút.'])
    delete_row(ui, r'^Ngày lập đến')
    ev = sec_ev(s)
    tr = find_row(ev, 1, r'^Nhấn Enter hoặc bấm Tìm kiếm')
    write_cell(cells(tr)[1], ['Bấm Tìm kiếm hoặc nhấn Enter ở ô gõ tay'])
    write_cell(cells(tr)[2], ['Click'])

    # ---------- 2.5 Tạo mới (lập từ phiếu đề nghị)
    s = section(doc, r'^2\.5 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^7\. ', [
        '7. Hệ thống kiểm tra dữ liệu, sinh mã phiếu và lưu phiếu ở trạng thái “Đang tạo”.',
        '8. Ghi nhận hành động Tạo mới trong lịch sử của phiếu.',
        '9. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Không có quyền Kế toán thanh toán',
            '• Không có quyền Kế toán thanh toán → nút Tạo mới vẫn hiển thị và màn Thêm mới vẫn mở; bấm ô Số phiếu đề '
            'nghị thì báo “Bạn không có quyền xem danh sách phiếu đề nghị chi”; bấm Lưu nháp / Lưu và duyệt thì hệ '
            'thống kiểm tra dữ liệu nhập trước, hợp lệ rồi mới báo “Bạn không có quyền lập phiếu ủy nhiệm chi” và '
            'không lưu.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Rời màn khi đã sửa', [
        UNSAVED,
        '• Bấm Lưu và tiếp tục → lưu nháp như nút Lưu nháp, rồi ở lại màn Thêm mới với form trống để lập phiếu tiếp.',
        '• Mở từ nút “Tạo phiếu ủy nhiệm chi” trên dòng phiếu ở màn Đề nghị thanh toán → form nạp sẵn phiếu đề nghị '
        'đó; màn mở theo cách này không có nút Lưu và tiếp tục.'])
    ui = sec_ui(s)
    ui_type(ui, r'^Tỷ giá \(VND\)', 'Textbox')
    ui_type(ui, r'^Ô Số tiền duyệt chi trên dòng', 'Textbox')
    clone_row_after(ui, r'^Nút Lưu và duyệt',
                    [None, 'Nút Lưu và tiếp tục', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
                     'Lưu nháp rồi ở lại màn Thêm mới với form trống. Chỉ có ở màn Thêm mới mở từ danh sách; không có '
                     'ở màn Sửa và khi mở từ màn Đề nghị thanh toán.'])
    ev = sec_ev(s)
    set_col(ev, 2, r'^Nhập Số tiền duyệt chi', 'Change')
    tc = ev_cell(ev, r'^Bấm Lưu nháp')
    old = cell_lines(tc)
    after = old[old.index('After:'):]
    write_cell(tc, ['Before:',
                    '– Kiểm tra Số tiền duyệt chi từng dòng không vượt Số tiền đề nghị chi; vượt thì báo nêu rõ số thứ '
                    'tự dòng sai và không gửi dữ liệu.',
                    'During:',
                    '– Loại chi trống → hiển thị “Bắt buộc chọn loại chi”.',
                    '– Các ô bắt buộc khác được bỏ qua ở đường lưu nháp.',
                    '– Không có quyền Kế toán thanh toán → hiển thị “Bạn không có quyền lập phiếu ủy nhiệm chi”.']
               + after, rid)
    add_err_line(ev, r'^Bấm Lưu nháp', rid)
    clone_row_after(ev, r'^Bấm Lưu nháp',
                    [None, 'Bấm Lưu và tiếp tục', 'Click',
                     ['Before:', '– Kiểm tra như nút Lưu nháp.', 'After:',
                      '– Lưu phiếu ở trạng thái “Đang tạo” và ghi nhận hành động Tạo mới trong lịch sử.',
                      '– Hiển thị thông báo thành công, ở lại màn Thêm mới với form trống.']])
    tr = find_row(ev, 1, r'^Bấm Quay lại')
    write_cell(cells(tr)[1], ['Bấm Quay lại / chọn menu khác / đóng tab trình duyệt'])
    write_cell(cells(tr)[3], UNSAVED_EV)

    # ---------- 2.6 Chọn phiếu đề nghị
    s = section(doc, r'^2\.6 ')
    kv_edit(sec_kv(s), 'Dòng sự kiện phụ', r'^• Bấm “Đóng”',
            '• Bấm Đóng / (x) → cửa sổ đóng ngay, không hỏi xác nhận; phiếu đề nghị đang chọn trước đó (nếu có) '
            'giữ nguyên.')

    # ---------- 2.7 Chi thu nhập cho nhân viên
    s = section(doc, r'^2\.7 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^7\. ', [
        '7. Người dùng bấm “Lưu nháp” hoặc “Lưu và duyệt”.',
        '8. Hệ thống kiểm tra dữ liệu và lưu phiếu (Lưu nháp: trạng thái Đang tạo; Lưu và duyệt: trạng thái Đã hạch '
        'toán, ghi bút toán theo BR-04).',
        '9. Ghi nhận hành động Tạo mới (kèm chuyển trạng thái nếu bấm Lưu và duyệt) trong lịch sử của phiếu.',
        '10. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_append(kv, 'Dòng sự kiện phụ', UNSAVED)
    ui = sec_ui(s)
    ui_type(ui, r'^Tỷ giá \(VND\)', 'Textbox')
    ui_type(ui, r'^Ô tích Cần thanh toán', 'Checkbox')
    ui_type(ui, r'^Ô Số tiền chi', 'Textbox')
    ui_type(ui, r'^Ô 5 khoản', 'Textbox')
    ev = sec_ev(s)
    set_col(ev, 2, r'^Nhập Số tiền chi', 'Change')
    tc = ev_cell(ev, r'^Bấm Lưu và duyệt')
    write_cell(tc, lines_replace(cell_lines(tc), r'^– Ghi phiếu ở trạng thái “Đã hạch toán”', [
        '– Ghi phiếu ở trạng thái “Đã hạch toán”, ghi bút toán theo từng khoản của từng nhân viên cùng hai bút toán '
        'tổng.',
        '– Ghi nhận hành động Tạo mới và chuyển trạng thái trong lịch sử của phiếu.',
        '– Hiển thị “Duyệt phiếu ủy nhiệm chi thành công!” và quay về danh sách.']))
    add_err_line(ev, r'^Bấm Lưu và duyệt', rid)

    # ---------- 2.8 Chỉnh sửa
    s = section(doc, r'^2\.8 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống kiểm tra điều kiện sửa và dữ liệu, ghi lại phiếu.',
        '6. Ghi nhận các thay đổi (giá trị cũ → giá trị mới của từng ô, từng dòng chi tiết; kèm chuyển trạng thái nếu '
        'bấm Lưu và duyệt) trong lịch sử của phiếu.',
        '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Rời màn khi đã sửa', UNSAVED)
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Lưu nháp ở màn Sửa', rid)
    clone_row_after(ev, r'^Bấm Lưu nháp ở màn Sửa',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # ---------- 2.9 Lưu và duyệt
    s = section(doc, r'^2\.9 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^8\. ', [
        '8. Ghi nhận nội dung thay đổi và hành động chuyển trạng thái sang Đã hạch toán trong lịch sử của phiếu.',
        '9. Hệ thống hiển thị “Duyệt phiếu ủy nhiệm chi thành công!” và quay về màn danh sách.'])
    add_err_line(sec_ev(s), r'^Bấm Xác nhận trong hộp', rid)

    # ---------- 2.11 Xóa
    s = section(doc, r'^2\.11 ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^5\. ',
            '5. Ghi nhận hành động Xóa trong lịch sử, hiển thị thông báo thành công và tải lại danh sách (xóa từ màn '
            'chi tiết thì quay về màn danh sách).')
    add_err_line(sec_ev(s), r'^Bấm Xóa trong hộp xác nhận', rid)

    # ---------- 2.12 Lịch sử
    s = section(doc, r'^2\.12 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu chưa từng bị thay đổi',
            '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → hiện “Chưa có lịch sử thao tác nào.”')
    ui = sec_ui(s)
    tr = find_row(ui, 1, r'^Tiêu đề cửa sổ')
    write_cell(cells(tr)[header_index(ui, 'Giá trị ban đầu')], ['Lịch sử thay đổi: <mã phiếu>'])
    write_cell(cells(tr)[header_index(ui, 'Mô tả')], ['–'])
    ui_desc(ui, r'^Trạng thái rỗng', 'Hiện “Chưa có lịch sử thao tác nào.” với phiếu lập từ hệ thống cũ, chưa có '
                                     'thao tác nào trên hệ thống mới.')


def part_heading(doc, n):
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1' and re.match(r'^Phần %d\b' % n, txt(e)):
            return e
    raise KeyError(n)


def patch_part4(doc):
    h = part_heading(doc, 4)
    intro = h.getnext()
    set_rule_head(intro, 'Quy tắc áp dụng: Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
    set_rule_tail(intro, '. Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc đã có trong SRS '
                         'quy tắc chung.' % SCREEN)
    tbl = intro.getnext()
    while tbl.tag != W('tbl'):
        tbl = tbl.getnext()
    for i, tr in enumerate(rows(tbl)[1:], 1):
        assert txt(cells(tr)[1]).strip() == 'BR-%02d' % i, 'Mã BR không liên tục ở dòng %d' % i


def add_part5(doc):
    h4 = part_heading(doc, 4)
    anchor = doc.element.body[-1].getprevious()
    h5 = clone_heading(h4, 'Phần 5. Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    no_bookmarks(h5)
    intro = docxlib.clone_par_after(h5, h4.getnext(), 'Các màn hình dưới đây đọc dữ liệu do %s ghi ra (phiếu, dòng '
                                    'chi tiết và bút toán sổ kế toán sinh ra khi phiếu được duyệt).' % SCREEN)
    strip_ids(intro)
    tpl = sec_ev(section(doc, r'^2\.1 '))
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], PART5, [700, 1500, 3900, 2750])
    log('Thêm Phần 5 (%d màn tham chiếu)' % len(PART5))


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""Vá SRS "Yêu cầu điều chuyển hàng giữ" (STT 33, bản Drive tải 28/10) theo FORM "Danh mục quốc gia" (TPE Pass).

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/SRS - Yêu cầu điều chuyển hàng giữ.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Luôn đọc bản Drive gốc, chạy lại bao nhiêu lần cũng được. Khuôn: finance-product-import-direct-transfer/form_qg.
Khác màn 27: mục con 2.x.y của bản Drive là Heading4 (vài mục còn là đoạn thường) → is_sub / renumber riêng ở đây.
Ảnh màn hình thay bằng bộ ảnh HDSD chụp trên dev (hdsd_shots/, capture.js — dev chưa có phiếu nào nên phiếu minh họa).
"""
import copy, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
import docx  # noqa: E402
from formqg_lib import *  # noqa: E402,F401
import formqg_lib as L  # noqa: E402
import docxlib  # noqa: E402

SRC = os.path.join(HERE, 'drive_0710', 'SRS_Drive.docx')
OUT_DIR = os.path.join(HERE, 'out')
OUT = os.path.join(OUT_DIR, 'SRS - Yêu cầu điều chuyển hàng giữ.docx')
UML = os.path.join(HERE, 'uml')
SHOTS = os.path.join(HERE, 'hdsd_shots')

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'Yêu cầu điều chuyển hàng giữ'
# finance.js: hubGroup 'Hàng hoá - Dịch vụ - Vận chuyển' > nhóm 'Giữ hàng' > mục 'Phiếu Yêu cầu điều chuyển hàng giữ'
MENU = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng => Phiếu Yêu cầu điều chuyển hàng giữ'
TAIL = ' Chỉ bổ sung quy tắc riêng của màn %s.' % SCREEN
UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: chưa nhập hoặc thay đổi gì thì rời màn ngay; '
           'đã nhập dữ liệu thì hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” (Thoát / Ở lại).')
UNSAVED_EV = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
              '– Đã nhập dữ liệu → hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”; bấm Thoát '
              'thì rời màn và bỏ thay đổi, bấm Ở lại thì giữ nguyên màn.']
DUE_SELF = ('• Người lập còn hàng quá hạn theo cấu hình chặn của thao tác “Điều chuyển hàng giữ” → hệ thống báo lý do '
            'và không cho gửi phiếu (mở màn Tạo mới thì quay về danh sách). Super Admin không bị chặn.')

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy cập '
              'riêng). Phạm vi phiếu nhìn thấy theo quyền Xem phiếu hàng giữ theo tổng công ty / công ty / phòng ban '
              '(V1–V3) và quyền duyệt (Q1–Q3); không có quyền nào thì chỉ thấy phiếu của mình và phiếu đang chờ mình duyệt.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (V1–V3, Q1–Q3); không có quyền nào vẫn xem được phiếu do chính mình lập.')
ACTOR_OWNER = 'Người lập phiếu — người dùng có quyền thực hiện chức năng: chỉ người đã lập phiếu (chức năng không gắn quyền riêng).'
COND_OWNER = ('1. Đăng nhập thành công.\n'
              '2. Là người lập phiếu (chức năng không gắn quyền riêng).\n'
              '3. Phiếu đang ở trạng thái Không duyệt.')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người lập phiếu; người có quyền duyệt (Q1–Q3) cùng công ty; hoặc người có '
               'quyền Xem phiếu hàng giữ theo tổng công ty / công ty / phòng ban (V1–V3) trong phạm vi được giao.')
COND_SCOPE = ('1. Đăng nhập thành công.\n'
              '2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu nằm trong phạm vi dữ liệu của người dùng; phiếu Không duyệt chỉ người lập xem được.')
ACTOR_APPROVE = ('Người dùng có quyền Trưởng phòng duyệt hàng giữ (Q1), Ban giám đốc duyệt hàng giữ (Q2) hoặc Kế toán '
                 'duyệt hàng giữ (Q3), cùng công ty với phiếu.')
COND_APPROVE = ('1. Đăng nhập thành công.\n'
                '2. Có quyền duyệt đúng cấp phiếu đang chờ (Q1 / Q2 / Q3) và cùng công ty với phiếu; Trưởng phòng còn '
                'phải quản lý phòng ban của NGƯỜI NHẬN.\n'
                '3. Phiếu đang ở trạng thái Chờ TP duyệt / Chờ BGĐ duyệt / Chờ KT duyệt tương ứng.')

SECTIONS = {
    r'^2\.1 ': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 ': ('Kịch bản tìm kiếm, Bộ lọc và Dropdown.', ACTOR_LIST, COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.3 ': ('Bộ lọc và lưu cấu hình theo người dùng.', ACTOR_LIST, COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.4 ': ('Cấu hình cột hiển thị.', ACTOR_LIST, COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.5 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
                'Người lập phiếu — người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (chức năng '
                'lập phiếu không gắn quyền riêng).',
                '1. Đăng nhập thành công.\n'
                '2. Vào được màn Yêu cầu điều chuyển hàng giữ (lập phiếu không gắn quyền riêng).\n'
                '3. Người lập đang giữ ít nhất một lô hàng còn hàng, chưa hết hạn giữ, và không bị chặn do còn hàng '
                'quá hạn.'),
    r'^2\.6 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.7 ': ('Màn Xem chi tiết và Phân quyền.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.8 ': ('Thông báo, Quy tắc ghi lịch sử và UI/UX của thao tác đổi trạng thái.', ACTOR_APPROVE, COND_APPROVE),
    r'^2\.9 ': ('Thông báo, Quy tắc ghi lịch sử và UI/UX của thao tác đổi trạng thái.', ACTOR_APPROVE, COND_APPROVE),
    r'^2\.10 ': ('Quy tắc xóa, Thông báo và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.11 ': ('Quy tắc màn In và bố cục bản in.', ACTOR_SCOPE,
                 '1. Đăng nhập thành công.\n2. Có quyền xem phiếu như mục Tác nhân.\n'
                 '3. In phiếu: phiếu nằm trong phạm vi dữ liệu của người dùng; In danh sách: đang ở màn danh sách.'),
    r'^2\.12 ': ('Quy tắc Excel và Cấu hình cột.', ACTOR_LIST, COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.13 ': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_SCOPE, COND_SCOPE),
}

MENU_LINES = {
    r'^2\.1 ': [(MENU, None)],
    r'^2\.2 ': [(MENU + ' => Tìm kiếm nâng cao', None)],
    r'^2\.3 ': [(MENU + ' => Cài đặt bộ lọc',
                 'Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.')],
    r'^2\.4 ': [(MENU + ' => Tùy chỉnh cột (biểu tượng Cấu hình cột hiển thị)',
                 'Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.')],
    r'^2\.5 ': [(MENU + ' => Tạo mới', None),
                (MENU + ' => Tạo mới / Chỉnh sửa => Thêm hàng hóa',
                 'Modal Hàng bạn đang giữ được mở ngay trên màn hình Tạo mới hoặc Chỉnh sửa phiếu theo đường dẫn ở '
                 'trên; cửa sổ Chọn lô hàng giữ (nút tìm ở ô Từ xuất giữ) và Chọn hợp đồng (nút tìm ở ô Hợp đồng) mở '
                 'ngay trên cùng màn hình đó.')],
    r'^2\.6 ': [(MENU + ' => Chỉnh sửa', None)],
    r'^2\.7 ': [(MENU + ' => Xem chi tiết (bấm Mã phiếu)', None)],
    r'^2\.8 ': [(MENU + ' => Xem chi tiết => TP duyệt / BGĐ duyệt / KT duyệt',
                 'Modal Xác nhận duyệt được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.')],
    r'^2\.9 ': [(MENU + ' => Xem chi tiết => Từ chối',
                 'Modal Từ chối yêu cầu điều chuyển hàng giữ được mở ngay trên màn hình chi tiết phiếu theo đường dẫn '
                 'ở trên.'),
                (MENU + ' => Chỉnh sửa (phiếu Không duyệt)', None)],
    r'^2\.10 ': [(MENU + ' => Xóa (trên dòng phiếu) / Xem chi tiết => Xóa',
                  'Modal Xác nhận xóa được mở ngay trên màn hình danh sách (biểu tượng Xóa trên dòng) hoặc màn hình chi '
                  'tiết phiếu (nút Xóa) theo đường dẫn ở trên.')],
    r'^2\.11 ': [(MENU + ' => In (trên dòng phiếu hoặc trong menu ba chấm) / Xem chi tiết => In',
                  'Cửa sổ Xem trước bản in phiếu được mở ngay trên màn hình danh sách hoặc màn hình chi tiết phiếu theo '
                  'đường dẫn ở trên.'),
                 (MENU + ' => In (thanh công cụ danh sách)',
                  'Cửa sổ Xem trước danh sách được mở ngay trên màn hình danh sách theo đường dẫn ở trên.')],
    r'^2\.12 ': [(MENU + ' => Xuất Excel',
                  'Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.')],
    r'^2\.13 ': [(MENU + ' => Lịch sử (trên dòng phiếu hoặc menu ba chấm) / Xem chi tiết => Xem lịch sử',
                  'Modal Lịch sử yêu cầu điều chuyển hàng giữ được mở ngay trên màn hình danh sách theo đường dẫn ở '
                  'trên; khối Lịch sử thay đổi nằm cuối màn hình chi tiết phiếu.')],
}

USECASES = {
    r'^2\.5 ': ('Người lập phiếu', 'FR-05', 'Tạo mới phiếu', 'crud'),
    r'^2\.6 ': ('Người lập phiếu', 'FR-06', 'Chỉnh sửa phiếu', 'crud'),
    r'^2\.7 ': ('Người dùng có quyền', 'FR-07', 'Xem chi tiết phiếu', 'view'),
    r'^2\.8 ': ('TP / BGĐ / Kế toán', 'FR-08', 'Duyệt phiếu', 'action'),
    r'^2\.9 ': ('TP / BGĐ / Kế toán', 'FR-09', 'Từ chối phiếu', 'action'),
    r'^2\.10 ': ('Người lập phiếu', 'FR-10', 'Xóa phiếu', 'action'),
    r'^2\.11 ': ('Người dùng có quyền', 'FR-11', 'In phiếu và in danh sách', 'io'),
    r'^2\.12 ': ('Người dùng có quyền', 'FR-12', 'Xuất Excel danh sách', 'io'),
}

# Ảnh: chụp dev 28/10/2026 (dev chưa có phiếu điều chuyển nào → danh sách / chi tiết / duyệt / sửa / xóa / lịch sử là
# phiếu minh họa bật tạm trên trình duyệt, xem capture.js). Ảnh bản in giữ ảnh Drive (bố cục bản in không đổi).
IMAGES = [
    (r'lúc mới truy cập', '01_list', None),
    (r'Bảng lọc nâng cao', '02_filter', None),
    (r'Cửa sổ Cài đặt bộ lọc', '26_filtercfg', None),
    (r'Cửa sổ Tùy chỉnh cột', '25_colcfg', None),
    (r'Màn lập phiếu', '10_create', None),
    (r'Popup Hàng bạn đang giữ', '11_stock', 'Cửa sổ Hàng bạn đang giữ'),
    (r'Màn sửa phiếu bị trả về', '12_edit', None),
    (r'Màn chi tiết phiếu ở chế độ chỉ đọc', '17_detail', None),
    (r'Nút duyệt của cấp hiện tại', '14_detail_approve', None),
    (r'Cửa sổ Từ chối', '15_reject', None),
    (r'Phiếu sau khi bị từ chối', '12_edit', None),
    (r'Hộp thoại Xác nhận xóa', '13_delete', None),
    (r'Chọn trường xuất Excel', '20_export', None),
    (r'Khối Lịch sử thay đổi', '16_history', 'Cửa sổ Lịch sử yêu cầu điều chuyển hàng giữ'),
]

TEXT_FIX = [
    ('Hiện với mọi người dùng đã đăng nhập.', 'Hiện với mọi người dùng vào được màn hình.'),
    ('Người tạo bản ghi / Ngày giờ tạo bản ghi. Cột Ngày tạo sắp xếp được.',
     'Người lập phiếu / Ngày giờ lập phiếu. Cột Ngày tạo sắp xếp được.'),
    ('Lọc theo ngày tạo bản ghi. Lọc theo khoảng ngày lập phiếu.', 'Lọc theo khoảng ngày lập phiếu.'),
    ('Tài chính → Giữ hàng → Phiếu Yêu cầu điều chuyển hàng giữ',
     'Tài chính → Hàng hoá - Dịch vụ - Vận chuyển → Giữ hàng → Phiếu Yêu cầu điều chuyển hàng giữ'),
]

PART5 = [  # màn THẬT SỰ đọc dữ liệu phiếu điều chuyển (grep hrm-api / hrm-client 28/10/2026)
    ('1', 'Tài chính', 'Danh sách hàng giữ — cửa sổ lịch sử biến động của lô hiện dòng chuyển đi / nhận về kèm mã phiếu '
     'điều chuyển', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Giữ hàng'),
    ('2', 'Tài chính', 'Hàng sắp hết hạn giữ — cửa sổ lịch sử biến động của lô (cùng nguồn dữ liệu như trên)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Giữ hàng'),
    ('3', 'Danh mục', 'Hàng hoá — chặn xóa hàng hóa đã có trên dòng phiếu điều chuyển hàng giữ', 'Danh mục -> Hàng hoá'),
]


# ============================================================== tiện ích riêng (mục con Heading4)
def _is_sub(e):
    return (e.tag == W('p') and style_of(e) in ('', None, 'Heading4')
            and re.match(r'^\d+\.\d+\.\d+ ', txt(e)) is not None)


L.is_sub = _is_sub  # usecase_block / remove_usecase / add_usecase dùng bản này


def fix_heading_styles(doc):
    """Mục con 2.x.y còn là đoạn thường (sửa tay trên Drive) → đặt style Heading4 như các mục khác.
    Tiêu đề 2.1. (có dấu chấm) → 2.1 cho đồng bộ."""
    tpl = next(e for e in items(doc) if e.tag == W('p') and style_of(e) == 'Heading4')
    n = 0
    for e in items(doc):
        if e.tag != W('p'):
            continue
        if style_of(e) == 'Heading2' and re.match(r'^\d+\s', txt(e)):
            set_runs_text(e, re.sub(r"^(\d+)\s", lambda m: m.group(1) + ". ", txt(e)))
        if style_of(e) == 'Heading3' and re.match(r'^\d+\.\d+\.\s', txt(e)):
            set_runs_text(e, re.sub(r'^(\d+\.\d+)\.\s', r'\1 ', txt(e)))
        if not style_of(e) and re.match(r'^\d+\.\d+\.\d+ ', txt(e)):
            old = e.find(W('pPr'))
            if old is not None:
                e.remove(old)
            e.insert(0, copy.deepcopy(tpl.find(W('pPr'))))
            r0 = tpl.find('.//' + W('r'))
            set_runs_text(e, txt(e))
            if r0 is not None and r0.find(W('rPr')) is not None:
                r = e.find('.//' + W('r'))
                old_rpr = r.find(W('rPr'))
                if old_rpr is not None:
                    r.remove(old_rpr)
                r.insert(0, copy.deepcopy(r0.find(W('rPr'))))
            n += 1
    log('Đặt style Heading4 cho %d mục con còn là đoạn thường' % n)


def renumber_subs(doc):
    cur, k = None, 0
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading3':
            m = re.match(r'^(\d+\.\d+)\s', txt(e))
            cur, k = (m.group(1) if m else None), 0
        elif cur and _is_sub(e):
            k += 1
            new = '%s.%d %s' % (cur, k, re.sub(r'^\d+\.\d+\.\d+\s+', '', txt(e)))
            if new != txt(e):
                log('Đánh lại mục con: %s → %s' % (txt(e), new))
                set_runs_text(e, new)


def set_menus(doc, rx, lines):
    sec = section(doc, rx)
    for e in sec[1]:  # câu popup cũ (đặt sau ảnh, câu chữ cũ)
        if e.tag == W('p') and re.search(r'(được mở ngay trên|theo đường dẫn ở trên)', txt(e)) and not txt(e).startswith('Menu:'):
            e.getparent().remove(e)
    menus = [e for e in section(doc, rx)[1] if e.tag == W('p') and txt(e).startswith('Menu:')]
    assert len(menus) == len(lines), (rx, len(menus))
    for p, (menu, popup) in zip(menus, lines):
        set_runs_text(p, 'Menu: ' + menu)
        if popup:
            strip_ids(docxlib.clone_par_after(p, p, popup))


def replace_images(doc):
    its = items(doc)
    for rx, shot, newcap in IMAGES:
        hit = [i for i, e in enumerate(its) if e.tag == W('p') and re.match(r'^Hình \d+: .*' + rx, txt(e))]
        assert len(hit) == 1, (rx, len(hit))
        cap = its[hit[0]]
        img = its[hit[0] - 1]
        assert list(img.iter(L.A_NS + 'blip')), rx
        set_image(doc, img, os.path.join(SHOTS, shot + '.png'))
        if newcap:
            set_runs_text(cap, re.match(r'^(Hình \d+: )', txt(cap)).group(1) + newcap)
    log('Thay %d ảnh màn hình bằng ảnh chụp dev 28/10/2026' % len(IMAGES))


def lines_replace(lines, old_regex, new):
    out, hit = [], False
    for l in lines:
        if re.search(old_regex, l):
            hit = True
            if new is not None:
                out.extend(new if isinstance(new, list) else [new])
        else:
            out.append(l)
    assert hit, 'không thấy dòng: ' + old_regex
    return out


def kv_edit(kv, key, old_regex, new):
    write_cell(kv_row(kv, key), lines_replace(kv_get(kv, key), old_regex, new))


def kv_add(kv, key, new_lines):
    write_cell(kv_row(kv, key), kv_get(kv, key) + new_lines)


def ev_edit(ev, event_regex, old_regex, new, rid=None):
    tc = cells(find_row(ev, 1, event_regex))[3]
    write_cell(tc, lines_replace(cell_lines(tc), old_regex, new), rid)


def ui_set(ui, name_regex, col_name, value):
    set_col(ui, header_index(ui, col_name), name_regex, value)


def ui_row(ui, name_regex, values):
    """values: {tên cột: chữ}"""
    tr = find_row(ui, 1, name_regex)
    for k, v in values.items():
        write_cell(cells(tr)[header_index(ui, k)], v.split('\n'))


def keep_image_with_caption(doc):
    """Đoạn ảnh + chú thích “Hình N” liền sau: gắn keepNext cho đoạn ảnh để chú thích không rơi sang trang sau."""
    its = items(doc)
    n = 0
    for e, nxt in zip(its, its[1:]):
        if e.tag == W('p') and list(e.iter(L.A_NS + 'blip')) and nxt.tag == W('p') and txt(nxt).startswith('Hình '):
            ppr = e.find(W('pPr'))
            if ppr is None:
                ppr = L._el('pPr')
                e.insert(0, ppr)
            if ppr.find(W('keepNext')) is None:
                ppr.insert(0, L._el('keepNext'))
                n += 1
    log('Gắn keepNext cho %d đoạn ảnh (chú thích không tách ảnh)' % n)


# ============================================================== XỬ LÝ
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)
    body = doc.element.body

    fix_heading_styles(doc)
    for old, new in TEXT_FIX:
        log('Sửa chữ "%s…": %d chỗ' % (old[:30], replace_in_texts(body, old, new)))

    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    for rx, lines in MENU_LINES.items():
        set_menus(doc, rx, lines)

    patch_sections(doc, rid)
    patch_part2(doc)
    patch_part4(doc)
    add_part5(doc)
    replace_images(doc)

    # Use Case: bỏ ở Cài đặt bộ lọc + Tùy chỉnh cột, thêm Xem chi tiết, vẽ lại kiểu quốc gia
    remove_usecase(doc, section(doc, r'^2\.3 '))
    remove_usecase(doc, section(doc, r'^2\.4 '))
    for rx, (actor, code, name, grp) in USECASES.items():
        png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
        draw_usecase_qg(png, actor, code, name, grp)
        sec = section(doc, rx)
        blk = usecase_block(sec)
        if blk is None:
            add_usecase(doc, sec, section(doc, r'^2\.8 '), png, 'Biểu đồ Use Case — %s %s' % (code, name))
            # tiêu đề mục con nhân bản từ mẫu → giữ Heading4
        else:
            set_image(doc, blk[1], png)
    renumber_subs(doc)
    keep_image_with_caption(doc)
    nfig = renumber_figures(doc)
    log('Số Hình sau khi đánh lại: %d' % nfig)

    doc.save(OUT)
    print('Đã ghi', OUT)
    for m in L.LOG:
        print(' -', m)
    if '--no-word' not in sys.argv:
        word_finalize(OUT, os.path.join(OUT_DIR, 'SRS - Yêu cầu điều chuyển hàng giữ.pdf'))


def patch_sections(doc, rid):
    # 2.1 Xem danh sách
    s = section(doc, r'^2\.1 ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^1\. ', '1. Người dùng vào menu %s.' % MENU.replace('Phân hệ ', ''))
    ui = sec_ui(s)
    ui_set(ui, r'^Cột Trạng thái$', 'Loại', 'Table/Grid')
    ui_row(ui, r'^Nút In$', {'Mô tả': 'Mở cửa sổ xem trước bản in danh sách (khổ A4 ngang) theo đúng bộ lọc đang áp.'})
    ui_row(ui, r'^Cột Hành động$', {'Mô tả': 'Cột cố định cuối bảng, chứa các nút thao tác của dòng. Mỗi dòng hiện tối '
                                              'đa 3 nút; nhiều hơn thì 2 nút đầu hiện thẳng, các nút còn lại nằm trong '
                                              'menu ba chấm (Hành động khác). Từ chối chỉ có ở màn chi tiết.'})
    ui_row(ui, r'^Nút In / Lịch sử$', {'Mô tả': 'In mở cửa sổ xem trước bản in phiếu; Lịch sử mở cửa sổ lịch sử thay '
                                                 'đổi của phiếu.'})
    delete_row(ui, r'^Vòng quay chờ')

    # 2.2 Tìm kiếm
    s = section(doc, r'^2\.2 ')
    ui = sec_ui(s)
    ui_row(ui, r'^Người tạo / Người duyệt$', {'Mô tả': 'Lọc theo người lập phiếu / người duyệt gần nhất.'})
    ui_row(ui, r'^Ngày tạo từ / Ngày tạo đến$', {'Tên đối tượng': 'Ngày tạo',
                                                 'Mô tả': 'Một ô chọn khoảng ngày (từ ngày → đến ngày); lọc theo khoảng '
                                                          'ngày lập phiếu.'})
    ev_edit(sec_ev(s), r'^Bấm nút Tìm kiếm$', r'.', ['After:', '– Áp thêm nội dung ô tìm nhanh, về trang 1 và nạp lại '
                                                          'danh sách. Nhấn Enter trong ô tìm nhanh cho kết quả tương tự.'])

    # 2.3 Cài đặt bộ lọc
    s = section(doc, r'^2\.3 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^2\. ', '2. Hệ thống mở cửa sổ liệt kê 10 ô lọc của màn (Công ty – Phòng ban '
                                               'tính là một ô), kèm ô tích và tay kéo.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bấm Đóng', '• Bấm Đóng / (x) → đóng cửa sổ ngay, giữ nguyên cấu hình cũ, '
                                                   'không lưu thay đổi.')
    kv_set(kv, 'Yêu cầu đặc biệt', 'Cấu hình chỉ ảnh hưởng tới người dùng hiện tại, không ảnh hưởng người khác.')
    ui_row(sec_ui(s), r'^Danh sách ô lọc$', {'Phạm vi': '10 mục'})

    # 2.4 Tùy chỉnh cột
    s = section(doc, r'^2\.4 ')
    ui_set(sec_ui(s), r'^Cột bị khóa$', 'Loại', 'Label')

    # 2.5 Tạo mới
    s = section(doc, r'^2\.5 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^2\. ', '2. Người dùng chọn Người nhận và Khách hàng nhận, nhập Ghi chú và đính '
                                               'kèm tệp nếu cần (bấm Thêm tài liệu).')
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ', '4. Với mỗi dòng, người dùng bấm nút tìm ở ô “Từ xuất giữ” để chọn lô '
                                               'nguồn và nhập Số lượng chuyển.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. ', '6. Người dùng bấm Gửi duyệt (hoặc Lưu và tiếp tục để gửi duyệt rồi lập '
                                               'tiếp phiếu khác).')
    kv_edit(kv, 'Dòng sự kiện chính', r'^7\. ', [
        '7. Hệ thống kiểm tra dữ liệu, sinh mã phiếu, ghi phiếu ở trạng thái Chờ TP duyệt và gửi thông báo cho Trưởng '
        'phòng quản lý phòng ban của người nhận.',
        '8. Ghi nhận hành động Tạo phiếu trong lịch sử của phiếu.'])
    kv_edit(kv, 'Dòng sự kiện chính', r'^8\. Hệ thống hiển thị', '9. Hệ thống hiển thị thông báo thành công và quay về '
                                                                 'màn danh sách.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Rời màn khi', [UNSAVED, DUE_SELF])
    ui = sec_ui(s)
    ui_set(ui, r'^Ghi chú$', 'Loại', 'Textarea')
    ui_row(ui, r'^Chọn tệp đính kèm$', {'Tên đối tượng': 'Nút Thêm tài liệu (khối File đính kèm)',
                                        'Mô tả': 'Chọn tệp từ máy; tệp tải lên ngay và hiện trong lưới STT · Upload/File · '
                                                 'Dung lượng, mỗi tệp có Xem trước · Tải xuống · Thay đổi · Xóa.'})
    ui_row(ui, r'^Cột Từ xuất giữ$', {'Loại': 'Textbox', 'Phạm vi': 'Lô hàng giữ của người lập, còn hàng',
                                      'Mô tả': 'Ô chỉ đọc hiển thị dạng số lượng – hạn giữ; bấm nút tìm bên cạnh để chọn '
                                               'lô trong cửa sổ Chọn lô hàng giữ.'})
    ui_set(ui, r'^Cột Chuyển$', 'Loại', 'Textbox')
    ui_row(ui, r'^Cột Hợp đồng$', {'Mô tả': 'Ô chỉ đọc; bấm nút tìm bên cạnh để chọn đơn hàng / hợp đồng, nút (x) để '
                                            'bỏ hợp đồng đã chọn.'})
    ui_row(ui, r'^Nút Lưu và tiếp tục$', {'Mô tả': 'Chỉ có ở màn Tạo mới: gửi duyệt phiếu rồi ở lại để lập phiếu kế '
                                                    'tiếp.'})
    ui_set(ui, r'^Thông báo lỗi tại ô$', 'Loại', 'Label')
    ev = sec_ev(s)
    tr = find_row(ev, 1, r'^Chọn lô ở ô Từ xuất giữ$')
    write_cell(cells(tr)[1], ['Bấm nút tìm ở ô Từ xuất giữ, chọn lô'])
    write_cell(cells(tr)[2], ['Click'])
    ev_edit(ev, r'^Bấm nút tìm ở ô Từ xuất giữ', r'^– Chỉ liệt kê', '– Mở cửa sổ Chọn lô hàng giữ, chỉ liệt kê lô do '
                                                                   'chính người lập đang giữ, còn hàng.')
    set_col(ev, 2, r'^Nhập Số lượng chuyển', 'Change')
    ev_edit(ev, r'^Bấm Gửi duyệt$', r'^– Ghi một dòng lịch sử', '– Ghi nhận hành động Tạo phiếu trong lịch sử của phiếu.')
    add_err_line(ev, r'^Bấm Gửi duyệt$', rid)
    clone_row_after(ev, r'^Bấm Gửi duyệt$', [None, 'Bấm Lưu và tiếp tục', 'Click',
                                             ['After:', '– Kiểm tra và gửi duyệt như nút Gửi duyệt, rồi làm mới màn để lập '
                                                        'phiếu kế tiếp, không quay về danh sách.']])
    clone_row_after(ev, r'^Bấm Lưu và tiếp tục$',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # 2.6 Chỉnh sửa
    s = section(doc, r'^2\.6 ')
    kv = sec_kv(s)
    ui_set(sec_ui(s), r'^Trạng thái$', 'Loại', 'Label')
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống đặt lại toàn bộ các bước duyệt, đưa phiếu về Chờ TP duyệt và gửi thông báo cho Trưởng phòng của '
        'người nhận.',
        '6. Ghi nhận “Thay đổi thông tin” trong lịch sử của phiếu, nêu rõ giá trị cũ → mới.',
        '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu đang chờ duyệt',
            '• Phiếu đang chờ duyệt hoặc đã duyệt → nút Sửa không hiển thị; mở thẳng bằng đường dẫn thì hệ thống báo '
            '“Phiếu đang chờ duyệt hoặc không thuộc quyền sửa của bạn.” và chuyển sang màn chi tiết.')
    kv_add(kv, 'Dòng sự kiện phụ', [UNSAVED, DUE_SELF])
    ev = sec_ev(s)
    ev_edit(ev, r'^Mở màn Sửa$', r'^– Nếu không → ', '– Nếu không → báo “Phiếu đang chờ duyệt hoặc không thuộc quyền sửa '
                                                       'của bạn.” và chuyển sang màn chi tiết phiếu.')
    ev_edit(ev, r'^Bấm Gửi duyệt$', r'^– Ghi một dòng lịch sử',
            '– Ghi nhận “Thay đổi thông tin” trong lịch sử, nêu rõ những giá trị đã thay đổi.')
    add_err_line(ev, r'^Bấm Gửi duyệt$', rid)
    clone_row_after(ev, r'^Bấm Gửi duyệt$',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # 2.7 Xem chi tiết
    s = section(doc, r'^2\.7 ')
    ui = sec_ui(s)
    ui_row(ui, r'^Khối File đính kèm$', {'Loại': 'Table/Grid',
                                         'Mô tả': 'Lưới tệp đính kèm STT · Upload/File · Dung lượng; mỗi tệp xem trước / '
                                                  'tải xuống được; không có tệp thì lưới trống.'})
    ui_row(ui, r'^Khối Lịch sử duyệt$', {'Mô tả': 'Các cột Cấp duyệt, Người duyệt, Thời gian và Ghi chú; hiển thị đủ '
                                                   'mọi dòng đã duyệt kể cả khi không có ghi chú; dòng của cấp đã từ chối '
                                                   'có chữ “(không duyệt)” cạnh tên cấp.'})
    ui_row(ui, r'^Khối Lịch sử thay đổi$', {'Mô tả': 'Mặc định thu gọn; số mốc thay đổi hiện ngay cạnh tiêu đề khi vào '
                                                      'màn. Bấm Xem lịch sử để mở, Thu gọn để đóng, Làm mới để nạp lại.'})
    ev_edit(sec_ev(s), r'^Bấm Xem lịch sử', r'^– Nạp', '– Mở khối và hiển thị danh sách mốc thay đổi (đã nạp sẵn khi '
                                                       'vào màn), mới nhất trước.')

    # 2.8 Duyệt
    s = section(doc, r'^2\.8 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^3\. ', '3. Người duyệt bấm nút duyệt của cấp mình và xác nhận ở hộp “Xác nhận '
                                               'duyệt”.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống chuyển phiếu sang bước tiếp theo (Kế toán duyệt thì đổi chủ hàng giữ) và gửi thông báo cho cấp '
        'duyệt kế tiếp và cho người lập.',
        '6. Ghi nhận hành động Trưởng phòng / Ban giám đốc / Kế toán duyệt trong lịch sử của phiếu.'])
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. Hệ thống hiển thị', '7. Hệ thống hiển thị thông báo thành công và quay về '
                                                                 'màn danh sách.')
    kv_add(kv, 'Dòng sự kiện phụ', [
        '• Bấm Hủy ở hộp Xác nhận duyệt → đóng hộp, không duyệt.',
        '• Phòng ban người duyệt quản lý còn nhân viên có hàng quá hạn theo cấu hình chặn của thao tác “Duyệt điều '
        'chuyển hàng giữ” → hệ thống báo lý do, không duyệt. Super Admin không bị chặn.'])
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm nút duyệt', r'^– Ghi một dòng lịch sử',
            '– Ghi nhận hành động duyệt của cấp đó trong lịch sử của phiếu; gửi thông báo cho cấp duyệt kế tiếp và cho '
            'người lập.')
    add_err_line(ev, r'^Bấm nút duyệt', rid)

    # 2.9 Từ chối
    s = section(doc, r'^2\.9 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ', '4. Người duyệt bấm Xác nhận từ chối.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống chuyển phiếu sang trạng thái Không duyệt, ghi lý do và gửi thông báo cho người lập.',
        '6. Ghi nhận hành động Không duyệt kèm lý do trong lịch sử của phiếu.',
        '7. Hệ thống báo “Đã từ chối yêu cầu điều chuyển hàng giữ.” và quay về màn danh sách.'])
    kv_add(kv, 'Dòng sự kiện phụ', ['• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận '
                                    'kể cả khi đã nhập lý do; phiếu giữ nguyên.'])
    ui = sec_ui(s)
    ui_row(ui, r'^Lý do$', {'Tên đối tượng': 'Lý do từ chối',
                            'Mô tả': 'Gợi ý “Nhập lý do trả lại phiếu cho người lập...”. Bắt buộc nhập.'})
    ui_row(ui, r'^Nút xác nhận$', {'Tên đối tượng': 'Nút Xác nhận từ chối'})
    ui_row(ui, r'^Nút đóng cửa sổ$', {'Tên đối tượng': 'Nút Đóng'})
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm xác nhận từ chối$', r'^– Ghi một dòng lịch sử',
            '– Ghi nhận hành động Không duyệt kèm lý do trong lịch sử của phiếu; gửi thông báo cho người lập phiếu.')
    ev_edit(ev, r'^Bấm xác nhận từ chối$', r'^– Hiển thị thông báo thành công',
            '– Hiển thị “Đã từ chối yêu cầu điều chuyển hàng giữ.” và quay về màn danh sách.')
    write_cell(cells(find_row(ev, 1, r'^Bấm xác nhận từ chối$'))[1], ['Bấm Xác nhận từ chối'])
    add_err_line(ev, r'^Bấm Xác nhận từ chối$', rid)

    # 2.10 Xóa
    s = section(doc, r'^2\.10 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ', [
        '4. Hệ thống xóa phiếu cùng các dòng hàng và ghi nhận hành động Xóa phiếu trong lịch sử.',
        '5. Xóa từ danh sách thì nạp lại danh sách, xóa từ màn chi tiết thì quay về danh sách.'])
    ev = sec_ev(s)
    ev_edit(ev, r'^Xác nhận Xóa$', r'^– Xóa phiếu', '– Xóa phiếu cùng các dòng hàng; ghi nhận hành động Xóa phiếu trong '
                                                   'lịch sử.')
    ev_edit(ev, r'^Xác nhận Xóa$', r'^– Hiển thị', '– Hiển thị “Xóa thành công.”; ở danh sách thì nạp lại danh sách, ở '
                                                  'màn chi tiết thì quay về danh sách.')
    add_err_line(ev, r'^Xác nhận Xóa$', rid)

    # 2.11 In
    s = section(doc, r'^2\.11 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^2\. ', '2. Hệ thống mở cửa sổ xem trước bản in ngay trên màn hình đang đứng.')
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm nút In ở dòng', r'^– Mở tab mới', '– Mở cửa sổ xem trước bản in của đúng phiếu đó.')
    ev_edit(ev, r'^Bấm nút In ở thanh công cụ', r'^– Mở tab mới', '– Mở cửa sổ xem trước bản in danh sách theo đúng bộ '
                                                                 'lọc đang áp dụng.')

    # 2.12 Xuất Excel
    s = section(doc, r'^2\.12 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^3\. ', '3. Người dùng bỏ tích các trường không cần, kéo biểu tượng ☰ để đổi thứ '
                                               'tự cột.')
    kv_add(kv, 'Dòng sự kiện phụ', ['• Kết quả lọc rỗng → vẫn xuất tệp gồm tiêu đề và dòng tên cột, không có dòng dữ '
                                    'liệu.'])
    ui = sec_ui(s)
    ui_row(ui, r'^Ô chọn trường xuất$', {'Tên đối tượng': 'Danh sách trường xuất', 'Loại': 'Checkbox chọn nhiều',
                                         'Mô tả': 'Mã phiếu, Người tạo, Ngày tạo, Người nhận, Khách nhận, Trạng thái, '
                                                  'Người duyệt, Ngày duyệt, Người cập nhật, Ngày cập nhật, Phòng ban, Ghi '
                                                  'chú, Lý do không duyệt. Tích chọn, kéo ☰ để đổi thứ tự cột trong tệp.'})
    ui_row(ui, r'^Dòng xem trước thứ tự cột$', {'Tên đối tượng': 'Số trường đang chọn',
                                                'Giá trị ban đầu': 'Đang chọn 13/13 trường',
                                                'Mô tả': 'Góc trái cuối cửa sổ, cập nhật ngay khi tích / bỏ tích.'})
    ev_edit(sec_ev(s), r'^Bấm Xuất file$', r'^– Dựng tệp Excel', '– Dựng tệp Excel với đúng các trường đã tích, theo '
                                                                 'đúng thứ tự trong danh sách, và tải về máy.')

    # 2.13 Lịch sử
    s = section(doc, r'^2\.13 ')
    kv = sec_kv(s)
    kv_set(kv, 'Mô tả', 'Hiển thị các mốc thao tác đã thực hiện trên phiếu: Tạo phiếu, Thay đổi thông tin, Trưởng phòng '
                        '/ Ban giám đốc / Kế toán duyệt, Không duyệt, Xóa phiếu, kèm người thực hiện, thời điểm và giá '
                        'trị cũ → mới.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu chưa có thao tác',
            '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → hiện dòng “Chưa có lịch sử thao tác '
            'nào.”')
    kv_add(kv, 'Dòng sự kiện phụ', ['• Cửa sổ Lịch sử có nút Bộ lọc để lọc theo Loại hành động, Người thực hiện, Từ '
                                    'ngày, Đến ngày; bấm Đóng để đóng cửa sổ.'])
    ui = sec_ui(s)
    ui_row(ui, r'^Nút Xem lịch sử / Thu gọn$', {'Mô tả': 'Dữ liệu nạp sẵn khi vào màn (để hiện số mốc); bấm để mở / '
                                                         'thu gọn khối.'})
    ui_row(ui, r'^Trạng thái rỗng$', {'Mô tả': 'Hiện “Chưa có lịch sử thao tác nào.” với phiếu lập từ hệ thống cũ, chưa '
                                                'có thao tác nào trên hệ thống mới.'})
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm Xem lịch sử$', r'^– Nạp', '– Mở khối, hiển thị danh sách mốc thay đổi (đã nạp sẵn), mới nhất trước.')
    clone_row_after(ev, r'^Bấm Làm mới$', [None, 'Bấm biểu tượng Lịch sử trên dòng phiếu (hoặc trong menu ba chấm)',
                                           'Click', ['After:', '– Mở cửa sổ Lịch sử yêu cầu điều chuyển hàng giữ, các mốc '
                                                               'xếp mới nhất trước.']])


def part_heading(doc, n):
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1' and txt(e).startswith('Phần %d' % n):
            return e
    raise KeyError(n)


def patch_part2(doc):
    """Phần 2: câu 'đã đăng nhập' → nói theo quyền."""
    n = replace_in_texts(doc.element.body, 'mọi người dùng đã đăng nhập đều lập được phiếu',
                         'mọi người dùng vào được màn hình đều lập được phiếu')
    log('Phần 2: sửa câu tác nhân lập phiếu (%d)' % n)


def patch_part4(doc):
    h = part_heading(doc, 4)
    intro = h.getnext()
    set_rule_head(intro, 'Quy tắc áp dụng: Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
    set_rule_tail(intro, '. Phần này chỉ ghi các quy tắc đặc thù của màn %s; không lặp lại các quy tắc đã có trong SRS '
                         'quy tắc chung.' % SCREEN)
    tbl = intro.getnext()
    while tbl.tag != W('tbl'):
        tbl = tbl.getnext()
    clone_row_after(tbl, r'^BR-13$', [None, 'BR-14', 'Chặn khi còn hàng quá hạn', [
        '– Lập / gửi lại phiếu (tạo mới và sửa): người lập còn hàng quá hạn theo cấu hình chặn của thao tác “Điều '
        'chuyển hàng giữ” thì bị chặn; mở màn Tạo mới cũng bị đưa về danh sách.',
        '– Duyệt (mọi cấp): phòng ban người duyệt quản lý còn nhân viên có hàng quá hạn theo cấu hình của thao tác '
        '“Duyệt điều chuyển hàng giữ” thì bị chặn.',
        '– Super Admin không bị chặn.'], ['Tạo mới', 'Chỉnh sửa', 'Duyệt']])
    clone_row_after(tbl, r'^BR-14$', [None, 'BR-15', 'Thông báo theo luồng duyệt', [
        '– Gửi duyệt (tạo mới hoặc sửa gửi lại): báo Trưởng phòng quản lý phòng ban của người nhận.',
        '– Trưởng phòng / Ban giám đốc duyệt: báo cấp duyệt kế tiếp và báo người lập.',
        '– Kế toán duyệt: báo người lập phiếu đã được duyệt.',
        '– Từ chối: báo người lập kèm lý do.'], ['Tạo mới', 'Chỉnh sửa', 'Duyệt', 'Từ chối']])
    for i, tr in enumerate(rows(tbl)[1:], 1):
        assert txt(cells(tr)[1]).strip() == 'BR-%02d' % i, 'Mã BR không liên tục ở dòng %d' % i


def add_part5(doc):
    h4 = part_heading(doc, 4)
    anchor = doc.element.body[-1].getprevious()
    h5 = clone_heading(h4, 'Phần 5. Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    intro = docxlib.clone_par_after(h5, h4.getnext(), 'Các màn hình dưới đây đọc dữ liệu do màn %s ghi ra (phiếu, dòng '
                                    'hàng và nhật ký biến động tồn hàng giữ ghi khi Kế toán duyệt).' % SCREEN)
    strip_ids(intro)
    tpl = sec_ev(section(doc, r'^2\.1 '))
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], PART5, [850, 1500, 3600, 2900])
    log('Thêm Phần 5 (%d màn tham chiếu)' % len(PART5))


if __name__ == '__main__':
    main()

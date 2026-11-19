# -*- coding: utf-8 -*-
"""Vá SRS "Phiếu xuất giữ" (STT 188, bản Drive 28/10) theo FORM "Danh mục quốc gia" (TPE Pass).

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/SRS - Phiếu xuất giữ.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Chạy lại bao nhiêu lần cũng được: luôn đọc bản Drive gốc. Khuôn: finance-product-import-direct-transfer/form_qg.
Mục con 2.x.y của bản Drive là Heading4 (vài mục còn là đoạn thường) → `is_sub` / `renumber_subheadings` riêng.
"""
import copy, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia')
sys.path.insert(0, LIB)
import docx  # noqa: E402
from formqg_lib import *  # noqa: E402,F401
import formqg_lib as L  # noqa: E402
import docxlib  # noqa: E402

SRC = os.path.join(HERE, 'drive_0710', 'SRS_Drive.docx')
OUT_DIR = os.path.join(HERE, 'out')
NAME = 'SRS - Phiếu xuất giữ'
OUT = os.path.join(OUT_DIR, NAME + '.docx')
UML = os.path.join(HERE, 'uml')
SHOTS = os.path.join(HERE, 'hdsd_shots')

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'Phiếu xuất giữ'
OLD_MENU = 'Phân hệ Tài chính => Giữ hàng => '
# finance.js: hubGroup 'Hàng hoá - Dịch vụ - Vận chuyển' > nhóm 'Giữ hàng' > mục 'Phiếu xuất giữ'
MENU = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng => Phiếu xuất giữ'
YC_MENU = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng => Yêu cầu xuất giữ'
TAIL = ' Chỉ bổ sung quy tắc riêng của %s.' % SCREEN
UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: nếu chưa nhập hoặc thay đổi gì thì rời màn '
           'ngay; nếu đã nhập dữ liệu thì hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” '
           '(Thoát / Hủy).')
UNSAVED_EV = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
              '– Đã nhập dữ liệu → hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”; '
              'bấm Thoát thì rời màn và bỏ thay đổi, bấm Hủy thì giữ nguyên màn.']

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Phạm vi phiếu nhìn thấy theo quyền Xem phiếu hàng giữ theo tổng công ty / công ty / '
              'phòng ban (V1–V3) và quyền Kế toán duyệt hàng giữ (Q1 — xem mọi phiếu trong công ty mình); không có '
              'quyền nào thì chỉ thấy phiếu của mình.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (Q1, V1–V3); không có quyền nào vẫn xem được phiếu do chính mình lập.')
COND_LIST_ON = COND_LIST + '\n3. Đang ở màn danh sách phiếu.'
ACTOR_KT = 'Người dùng có quyền Kế toán duyệt hàng giữ (Q1), cùng công ty với yêu cầu nguồn.'
ACTOR_OWNER = ('Người lập phiếu (Kế toán) — người dùng có quyền thực hiện chức năng: chỉ người đã lập phiếu (chức năng '
               'không gắn quyền riêng; người có vai trò quản trị hệ thống cũng thao tác được).')
COND_OWNER = ('1. Đăng nhập thành công.\n'
              '2. Là người lập phiếu (chức năng không gắn quyền riêng).\n'
              '3. Phiếu đang ở trạng thái Đang tạo.')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người lập phiếu; người có quyền Kế toán duyệt hàng giữ (Q1) cùng công '
               'ty; hoặc người có quyền Xem phiếu hàng giữ theo tổng công ty / công ty / phòng ban (V1–V3) trong phạm '
               'vi được giao.')
COND_SCOPE = ('1. Đăng nhập thành công.\n'
              '2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu nằm trong phạm vi dữ liệu của người dùng; phiếu Đang tạo chỉ người lập xem được.')

SECTIONS = {
    r'^2\.1 ': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 ': ('Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.', ACTOR_LIST, COND_LIST_ON),
    r'^2\.3 ': ('Bộ lọc và lưu cấu hình theo người dùng.', ACTOR_LIST, COND_LIST_ON),
    r'^2\.4 ': ('Cấu hình cột hiển thị và lưu cấu hình theo người dùng.', ACTOR_LIST, COND_LIST_ON),
    r'^2\.5 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_KT,
                '1. Đăng nhập thành công.\n'
                '2. Có quyền Kế toán duyệt hàng giữ (Q1) và cùng công ty với yêu cầu nguồn.\n'
                '3. Yêu cầu xuất giữ nguồn đang ở trạng thái Chờ KT duyệt và chưa có phiếu xuất giữ.'),
    r'^2\.6 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.7 ': ('Màn Xem chi tiết và Phân quyền.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.8 ': ('Thông báo, Quy tắc ghi lịch sử và UI/UX của thao tác đổi trạng thái.',
                'Người lập phiếu có quyền Kế toán duyệt hàng giữ (Q1), cùng công ty với yêu cầu nguồn.',
                '1. Đăng nhập thành công.\n'
                '2. Có quyền Kế toán duyệt hàng giữ (Q1); là người lập phiếu (hoặc đang lập phiếu mới).\n'
                '3. Phiếu đang ở trạng thái Đang tạo (hoặc chưa lưu).'),
    r'^2\.9 ': ('Quy tắc xóa, Thông báo và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.10 ': ('Quy tắc màn In và bố cục bản in.', ACTOR_SCOPE,
                 '1. Đăng nhập thành công.\n2. Có quyền xem phiếu như mục Tác nhân.\n'
                 '3. In phiếu: phiếu nằm trong phạm vi dữ liệu của người dùng; In danh sách: đang ở màn danh sách.'),
    r'^2\.11 ': ('Quy tắc Excel và Cấu hình cột.', ACTOR_LIST, COND_LIST_ON),
    r'^2\.12 ': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_SCOPE, COND_SCOPE),
}

MENU_LINES = {
    r'^2\.3 ': ('Menu: %s => Cài đặt bộ lọc' % MENU,
                'Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.4 ': ('Menu: %s => Cấu hình cột hiển thị' % MENU,
                'Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.5 ': ('Menu: %s => Xem chi tiết yêu cầu (Chờ KT duyệt) => Lập phiếu xuất giữ (nút Lập từ yêu cầu ở màn '
                'Phiếu xuất giữ chỉ chuyển sang màn Yêu cầu xuất giữ)' % YC_MENU, None),
    r'^2\.6 ': ('Menu: %s => Sửa (trên dòng phiếu) / Xem chi tiết => Sửa' % MENU, None),
    r'^2\.8 ': ('Menu: %s => Xem chi tiết yêu cầu => Lập phiếu xuất giữ => Duyệt giữ hàng (hoặc màn Sửa phiếu xuất '
                'giữ => Duyệt giữ hàng)' % YC_MENU,
                'Modal Xác nhận duyệt giữ hàng được mở ngay trên màn hình lập (hoặc sửa) phiếu xuất giữ theo đường dẫn '
                'ở trên.'),
    r'^2\.9 ': ('Menu: %s => Xóa (trên dòng phiếu) / Xem chi tiết => Xóa' % MENU,
                'Modal Xác nhận xóa được mở ngay trên màn hình danh sách (biểu tượng Xóa trên dòng) hoặc màn hình chi '
                'tiết phiếu (nút Xóa) theo đường dẫn ở trên.'),
    r'^2\.10 ': ('Menu: %s => In (in danh sách, hoặc biểu tượng In trên dòng phiếu) / Xem chi tiết => In' % MENU,
                 'Cửa sổ Xem trước bản in được mở ngay trên màn hình danh sách hoặc màn hình chi tiết phiếu theo '
                 'đường dẫn ở trên.'),
    r'^2\.11 ': ('Menu: %s => Xuất Excel' % MENU,
                 'Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.12 ': ('Menu: %s => Lịch sử (biểu tượng trên dòng phiếu) / Xem chi tiết => Xem lịch sử' % MENU,
                 'Modal Lịch sử phiếu xuất giữ được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối Lịch '
                 'sử thay đổi nằm cuối màn hình chi tiết phiếu.'),
}

USECASES = {
    r'^2\.5 ': ('Kế toán', 'FR-05', 'Lập phiếu xuất giữ', 'crud'),
    r'^2\.6 ': ('Người lập phiếu', 'FR-06', 'Chỉnh sửa phiếu nháp', 'crud'),
    r'^2\.7 ': ('Người dùng có quyền', 'FR-07', 'Xem chi tiết phiếu', 'view'),
    r'^2\.8 ': ('Kế toán', 'FR-08', 'Duyệt giữ hàng', 'action'),
    r'^2\.9 ': ('Người lập phiếu', 'FR-09', 'Xóa phiếu', 'action'),
    r'^2\.10 ': ('Người dùng có quyền', 'FR-10', 'In phiếu và In danh sách', 'io'),
    r'^2\.11 ': ('Người dùng có quyền', 'FR-11', 'Xuất Excel danh sách', 'io'),
}

SHOTS_REPLACE = [
    (r'^Hình \d+: Màn Phiếu xuất giữ lúc mới truy cập', '01_list', None),
    (r'^Hình \d+: Bảng lọc nâng cao đang mở', '02_filter', None),
    (r'^Hình \d+: Cửa sổ Cài đặt bộ lọc', '26_filtercfg', None),
    (r'^Hình \d+: Cửa sổ Tuỳ chỉnh cột', '25_colcfg', None),
    (r'^Hình \d+: Màn lập phiếu xuất giữ, dữ liệu nạp sẵn', '10_create', None),
    (r'^Hình \d+: Màn sửa phiếu xuất giữ còn nháp', '12_edit', None),
    (r'^Hình \d+: Màn chi tiết phiếu đã duyệt', '17_detail', None),
    (r'^Hình \d+: Nút Duyệt giữ hàng nằm ở cuối màn lập phiếu', '11_approve',
     'Hộp thoại Xác nhận duyệt giữ hàng, mở ngay trên màn lập phiếu'),
    (r'^Hình \d+: Hộp thoại Xác nhận xóa phiếu', '13_delete', None),
    (r'^Hình \d+: Cửa sổ Xem trước phiếu xuất giữ', '18_print', None),
    (r'^Hình \d+: Cửa sổ Chọn trường xuất Excel', '20_export', None),
    (r'^Hình \d+: Khối Lịch sử thay đổi', '16_history', 'Cửa sổ Lịch sử phiếu xuất giữ'),
]

G = 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Giữ hàng'
PART5 = [  # STT | Nhóm (phân hệ) | Màn hình | Đường dẫn (menu cha)
    ('1', 'Tài chính', 'Yêu cầu xuất giữ (trạng thái Đang xuất giữ / Đã duyệt, người duyệt và ngày duyệt của yêu cầu '
     'cập nhật theo phiếu xuất giữ; xóa phiếu nháp đưa yêu cầu về Chờ KT duyệt)', G),
    ('2', 'Tài chính', 'Danh sách hàng giữ và Hàng sắp hết hạn giữ (lô hàng giữ do phiếu sinh ra khi Duyệt giữ hàng; '
     'cột phiếu giữ gốc trỏ về phiếu xuất giữ)', G),
    ('3', 'Tài chính', 'Yêu cầu gia hạn hàng giữ (chọn lô hàng giữ; hợp đồng của lô lần ngược qua phiếu xuất giữ)', G),
    ('4', 'Tài chính', 'Yêu cầu hủy hàng giữ, Phiếu hủy hàng giữ, Phiếu huỷ hàng giữ kế toán (trừ số lượng trên lô '
     'hàng giữ do phiếu sinh ra)', G),
    ('5', 'Tài chính', 'Phiếu Yêu cầu điều chuyển hàng giữ (đổi người giữ của lô; hợp đồng của lô lần ngược qua phiếu '
     'xuất giữ)', G),
    ('6', 'Bán hàng', 'Báo cáo theo dõi giữ hàng (cột Phiếu giữ gốc trỏ về phiếu xuất giữ)', 'Bán hàng -> Báo cáo -> '
     'Hàng giữ'),
]


# ============================================================== HÀM RIÊNG (mục con Heading4)
def is_sub(e):
    return e.tag == W('p') and style_of(e) in ('', None, 'Heading4') and re.match(r'^\d+\.\d+\.\d+ ', txt(e))


L.is_sub = is_sub  # usecase_block / remove_usecase / add_usecase của thư viện dùng hàm này


def set_style(p, sid):
    ppr = p.find(W('pPr'))
    if ppr is None:
        ppr = L._el('pPr')
        p.insert(0, ppr)
    ps = ppr.find(W('pStyle'))
    if ps is None:
        ps = L._el('pStyle')
        ppr.insert(0, ps)
    ps.set(W('val'), sid)


def renumber_subheadings(doc):
    """2.x.1..2.x.n liên tục trong từng mục, đặt style Heading4 đồng loạt (bản Drive còn vài mục là đoạn thường)."""
    cur, k = None, 0
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading3':
            m = re.match(r'^(\d+\.\d+)\s', txt(e))
            cur, k = (m.group(1) if m else None), 0
        elif cur and is_sub(e):
            k += 1
            title = re.sub(r'^\d+\.\d+\.\d+\s+', '', txt(e))
            new = '%s.%d %s' % (cur, k, title)
            if style_of(e) != 'Heading4':
                log('Đặt style Heading4 cho mục con: ' + txt(e))
                set_style(e, 'Heading4')
            if new != txt(e):
                log('Đánh lại mục con: %s → %s' % (txt(e), new))
                set_runs_text(e, new)


def sec_pars(sec, regex):
    return [e for e in sec[1] if e.tag == W('p') and re.search(regex, txt(e))]


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


def ev_edit(ev, event_regex, old_regex, new, rid=None):
    tc = cells(find_row(ev, 1, event_regex))[3]
    write_cell(tc, lines_replace(cell_lines(tc), old_regex, new), rid)


def ui_set(ui, name_regex, values):
    """values: {chỉ số cột: chữ mới}."""
    tr = find_row(ui, 1, name_regex)
    for i, v in values.items():
        write_cell(cells(tr)[i], v if isinstance(v, list) else [v])


def col(ui, name):
    return header_index(ui, name)


def replace_shot(doc, cap_regex, png, new_cap=None):
    its = items(doc)
    for i, e in enumerate(its):
        if e.tag == W('p') and re.match(cap_regex, txt(e)):
            img = its[i - 1]
            assert list(img.iter(L.A_NS + 'blip')), 'Không có ảnh trước: ' + txt(e)
            set_image(doc, img, os.path.join(SHOTS, png + '.png'))
            if new_cap:
                set_runs_text(e, re.match(r'^Hình \d+:', txt(e)).group(0) + ' ' + new_cap)
            return
    raise KeyError(cap_regex)


def fit_tall_image(doc, max_in=7.6):
    """Ảnh màn dài: giới hạn chiều cao để không tràn trang (thu cả bề rộng theo tỉ lệ)."""
    for ext in doc.element.body.iter(L.WP_NS + 'extent'):
        cx, cy = int(ext.get('cx')), int(ext.get('cy'))
        lim = int(max_in * L.EMU)
        if cy > lim:
            ncx = int(cx * lim / cy)
            ext.set('cx', str(ncx))
            ext.set('cy', str(lim))
            for x in ext.getparent().iter(L.A_NS + 'ext'):
                if x.get('cx'):
                    x.set('cx', str(ncx))
                    x.set('cy', str(lim))


def part_heading(doc, n):
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1' and txt(e).startswith('Phần %d' % n):
            return e
    raise KeyError(n)




def ev_append(ev, event_regex, extra):
    tc = cells(find_row(ev, 1, event_regex))[3]
    write_cell(tc, cell_lines(tc) + (extra if isinstance(extra, list) else [extra]))


def drop_blank_after_toc(doc):
    """Mục lục vừa kín trang 1 -> đoạn trống sau mục lục bị đẩy sang trang 2, rồi Phần 1 (Heading1 ngắt trang
    trước) sang trang 3 => trang 2 trắng. Bỏ đoạn trống đó và thu nhỏ đoạn kết field của mục lục."""
    sdt = doc.element.body.find(W('sdt'))
    nxt = sdt.getnext()
    while nxt is not None and nxt.tag == W('p') and not txt(nxt).strip() and not list(nxt.iter(L.A_NS + 'blip')):
        rm, nxt = nxt, nxt.getnext()
        rm.getparent().remove(rm)
    ps = sdt.findall('.//' + W('p'))
    last = ps[-1]
    if not txt(last).strip() and len(ps) > 1:
        # đoạn cuối chỉ chứa dấu kết field: chuyển run đó lên cuối dòng mục lục trước rồi bỏ đoạn trống
        prev = ps[-2]
        for r in list(last.findall(W('r'))):
            prev.append(r)
        last.getparent().remove(last)


# ============================================================== XỬ LÝ
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)
    body = doc.element.body

    n = replace_in_texts(body, OLD_MENU, MENU.rsplit('=> ', 1)[0] + '=> ')
    log('Đổi đường dẫn menu: %d chỗ' % n)

    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    for rx, (menu, popup) in MENU_LINES.items():
        sec = section(doc, rx)
        p = sec_par(sec, r'^Menu:')
        if menu:
            set_runs_text(p, menu)
        if popup:
            strip_ids(docxlib.clone_par_after(p, p, popup))

    patch_sections(doc, rid)
    patch_part4(doc)
    add_part5(doc)
    drop_blank_after_toc(doc)

    for cap, png, new_cap in SHOTS_REPLACE:
        replace_shot(doc, cap, png, new_cap)
    fit_tall_image(doc)

    remove_usecase(doc, section(doc, r'^2\.3 '))
    remove_usecase(doc, section(doc, r'^2\.4 '))
    for rx, (actor, code, name, grp) in USECASES.items():
        png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
        draw_usecase_qg(png, actor, code, name, grp)
        sec = section(doc, rx)
        blk = usecase_block(sec)
        if blk is None:
            add_usecase(doc, sec, section(doc, r'^2\.8 '), png, 'Biểu đồ Use Case — %s %s' % (code, name))
        else:
            set_image(doc, blk[1], png)
    renumber_subheadings(doc)
    nfig = renumber_figures(doc)
    log('Số Hình sau khi đánh lại: %d' % nfig)

    doc.save(OUT)
    print('Đã ghi', OUT)
    for m in L.LOG:
        print(' -', m)
    if '--no-word' not in sys.argv:
        pdf = os.path.join(OUT_DIR, NAME + '.pdf')
        word_finalize(OUT, pdf)
        fix_blank_page2(pdf)


def fix_blank_page2(pdf):
    """Mục lục kín trang 1 -> Word đẩy đoạn kết field sang trang 2 rồi Phần 1 (Heading1 ngắt trang trước) sang
    trang 3 => trang 2 trắng. Khi gặp thì tắt ngắt-trang-trước của riêng tiêu đề Phần 1 và cho Word chạy lại."""
    import pymupdf
    with pymupdf.open(pdf) as p:
        blank = len(p) > 2 and not p[1].get_text().strip() and not p[1].get_images()
    if not blank:
        return
    doc = docx.Document(OUT)
    h = part_heading(doc, 1)
    ppr = h.find(W('pPr'))
    pb = L._el('pageBreakBefore')
    pb.set(W('val'), '0')
    ppr.find(W('pStyle')).addnext(pb)
    doc.save(OUT)
    log('Trang 2 trắng -> bỏ ngắt trang trước ở tiêu đề Phần 1')
    import time
    time.sleep(5)
    try:
        word_finalize(OUT, pdf)
    except RuntimeError:  # lỗi RPC lúc mở/đóng Word liền nhau -> thử lại 1 lần (BRIEF mục Word COM)
        time.sleep(10)
        word_finalize(OUT, pdf)


def common_list_sections(doc):
    # 2.1
    s = section(doc, r'^2\.1 ')
    ui = sec_ui(s)
    set_col(ui, col(ui, 'Loại'), r'^Cột Trạng thái$', 'Table/Grid')
    delete_row(ui, r'^Vòng quay chờ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^1\. Người dùng vào menu', '1. Người dùng vào menu %s.' % MENU)
    # 2.2
    s = section(doc, r'^2\.2 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Ngày tạo từ / Ngày tạo đến$', {
        1: 'Ngày tạo', col(ui, 'Phạm vi'): 'dd/mm/yyyy → dd/mm/yyyy',
        col(ui, 'Mô tả'): 'Một ô chọn khoảng ngày (từ ngày → đến ngày) theo ngày tạo phiếu; không phải ngày duyệt '
                          'và không phải hạn giữ.'})
    ev = sec_ev(s)
    write_cell(cells(find_row(ev, 1, r'^Bấm nút Tìm kiếm$'))[1], ['Bấm nút Tìm kiếm hoặc nhấn Enter trong ô tìm nhanh'])
    # 2.3
    s = section(doc, r'^2\.3 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Danh sách ô lọc$', {col(ui, 'Phạm vi'): '10 mục'})
    clone_row_after(sec_ev(s), r'^Bấm Lưu$', [None, 'Kéo thả một ô lọc', 'Drag',
                                             ['After:', '– Đổi thứ tự ô lọc trong cửa sổ; chưa ghi cho tới khi bấm Lưu.']])
    kv_edit(sec_kv(s), 'Dòng sự kiện phụ', r'^• Bấm Đóng', '• Bấm Đóng / (x) → đóng cửa sổ ngay, giữ nguyên cấu hình cũ.')
    # 2.4
    s = section(doc, r'^2\.4 ')
    ui = sec_ui(s)
    set_col(ui, col(ui, 'Loại'), r'^Cột bị khóa$', 'Label')
    ui_set(ui, r'^Danh sách cột$', {col(ui, 'Phạm vi'): '16 cột'})
    clone_row_after(sec_ev(s), r'^Bấm Lưu$', [None, 'Kéo thả một cột', 'Drag',
                                             ['After:', '– Đổi thứ tự cột trong cửa sổ; chưa ghi cho tới khi bấm Lưu.']])


ATTACH = {'name': 'Khối File đính kèm (nút Thêm tài liệu)',
          'desc': 'Bấm Thêm tài liệu để thêm một dòng rồi chọn tệp (PDF, ảnh, Word, Excel; tối đa 13 MB mỗi tệp); tệp '
                  'tải lên ngay. Mỗi dòng có Xem trước, Tải xuống, Thay đổi, Xóa và cột Dung lượng.'}


def patch_sections(doc, rid):
    common_list_sections(doc)

    # 2.5 Lập phiếu xuất giữ
    s = section(doc, r'^2\.5 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', '5. Kế toán bấm Lưu nháp, Không duyệt (cũng chỉ lưu nháp) hoặc Duyệt '
                                                'giữ hàng.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^7\. ', [
        '7. Ghi nhận hành động Tạo phiếu (kèm Duyệt giữ hàng nếu bấm Duyệt) trong lịch sử của phiếu và của yêu cầu '
        'nguồn.',
        '8. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_append(kv, 'Dòng sự kiện phụ', UNSAVED)
    ui = sec_ui(s)
    C = col(ui, 'Loại')
    ui_set(ui, r'^Chọn tệp đính kèm$', {1: ATTACH['name'], C: 'Table/Grid', col(ui, 'Phạm vi'): '–',
                                        col(ui, 'Giá trị ban đầu'): 'Theo yêu cầu nguồn', col(ui, 'Mô tả'): ATTACH['desc']})
    set_col(ui, C, r'^Cột SL xuất giữ$', 'Textbox')
    set_col(ui, C, r'^Thông báo lỗi tại ô$', 'Label')
    ev = sec_ev(s)
    set_col(ev, 2, r'^Nhập SL xuất giữ$', 'Change')
    ev_append(ev, r'^Bấm Lưu nháp hoặc Không duyệt$', '– Hiển thị “Phiếu đã được lưu.” và quay về màn danh sách.')
    add_err_line(ev, r'^Bấm Lưu nháp hoặc Không duyệt$', rid)
    add_err_line(ev, r'^Bấm Duyệt giữ hàng$', rid)
    clone_row_after(ev, r'^Bấm Duyệt giữ hàng$',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # 2.6 Chỉnh sửa phiếu nháp
    s = section(doc, r'^2\.6 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ', [
        '4. Người dùng bấm Lưu nháp, Không duyệt (cũng chỉ lưu nháp) hoặc Duyệt giữ hàng.',
        '5. Hệ thống kiểm tra dữ liệu và lưu phiếu.',
        '6. Ghi nhận các thay đổi (kèm Duyệt giữ hàng nếu bấm Duyệt) trong lịch sử của phiếu.',
        '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_append(kv, 'Dòng sự kiện phụ', UNSAVED)
    ev = sec_ev(s)
    write_cell(cells(find_row(ev, 1, r'^Bấm Lưu nháp$'))[1], ['Bấm Lưu nháp hoặc Không duyệt'])
    ev_append(ev, r'^Bấm Lưu nháp hoặc Không duyệt$', '– Hiển thị “Phiếu đã được lưu.” và quay về màn danh sách.')
    add_err_line(ev, r'^Bấm Lưu nháp hoặc Không duyệt$', rid)
    add_err_line(ev, r'^Bấm Duyệt giữ hàng$', rid)
    clone_row_after(ev, r'^Bấm Duyệt giữ hàng$',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # 2.7 Xem chi tiết
    s = section(doc, r'^2\.7 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Khối File đính kèm$', {col(ui, 'Loại'): 'Table/Grid', col(ui, 'Mô tả'):
           'Lưới tệp đính kèm (STT, tệp, Dung lượng); bấm để xem trước hoặc tải xuống.'})
    ui_set(ui, r'^Khối Lịch sử thay đổi$', {col(ui, 'Mô tả'):
           'Thu gọn sẵn; số mốc thay đổi hiện ngay cạnh tiêu đề. Bấm Xem lịch sử để mở danh sách.'})
    ev_edit(sec_ev(s), r'^Bấm Xem lịch sử', r'^– Nạp và hiển thị',
            '– Mở danh sách mốc thay đổi của phiếu (đã nạp sẵn khi vào màn), mới nhất trước.')

    # 2.8 Duyệt giữ hàng
    s = section(doc, r'^2\.8 ')
    kv = sec_kv(s)
    kv_append(kv, 'Dòng sự kiện chính', [
        '8. Ghi nhận hành động Duyệt giữ hàng trong lịch sử của phiếu và của yêu cầu nguồn, nêu rõ số lô đã ghi tồn.',
        '9. Hệ thống báo “Đã duyệt giữ hàng và cập nhật tồn hàng giữ.” và quay về màn danh sách.'])
    ui = sec_ui(s)
    set_col(ui, col(ui, 'Loại'), r'^Hộp thoại xác nhận$', 'Label')
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm Duyệt giữ hàng$', r'^– Có bất kỳ lỗi nào thì KHÔNG thực hiện bước After', None)
    add_err_line(ev, r'^Bấm Duyệt giữ hàng$', rid)
    clone_row_after(ev, r'^Bấm Duyệt giữ hàng$', [None, 'Bấm Hủy trong hộp thoại xác nhận', 'Click',
                                                 ['After:', '– Đóng hộp thoại, phiếu và tồn hàng giữ giữ nguyên.']])

    # 2.9 Xóa
    s = section(doc, r'^2\.9 ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^4\. ', [
        '4. Hệ thống xóa phiếu, đưa yêu cầu nguồn về Chờ KT duyệt và ghi nhận hành động Xóa trong lịch sử.',
        '5. Hệ thống báo “Xóa thành công.”: xóa từ danh sách thì nạp lại danh sách, xóa từ màn chi tiết thì quay về '
        'màn danh sách.'])
    add_err_line(sec_ev(s), r'^Xác nhận Xóa$', rid)

    # 2.11 Xuất Excel
    s = section(doc, r'^2\.11 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Ô chọn trường xuất$', {1: 'Danh sách trường xuất', col(ui, 'Loại'): 'Checkbox',
           col(ui, 'Mô tả'): 'Mỗi trường một ô tích kèm tay kéo đổi thứ tự: Mã phiếu, Yêu cầu xuất giữ, Người yêu cầu, '
                             'Phòng yêu cầu, Người tạo, Ngày tạo, Khách hàng, Giữ đến ngày, Trạng thái, Người duyệt, '
                             'Ngày duyệt, Người cập nhật, Ngày cập nhật, Ghi chú.'})
    ui_set(ui, r'^Dòng xem trước thứ tự cột$', {1: 'Số trường đang chọn', col(ui, 'Giá trị ban đầu'): 'Đang chọn 14/14 '
           'trường', col(ui, 'Mô tả'): 'Góc trái cuối cửa sổ; thứ tự cột trong tệp theo đúng thứ tự trong danh sách.'})
    kv_append(sec_kv(s), 'Dòng sự kiện phụ', '• Kết quả lọc rỗng → vẫn xuất tệp gồm tiêu đề và dòng tên cột, không có '
                                             'dòng dữ liệu.')
    clone_row_after(sec_ev(s), r'^Bấm Xuất file$', [None, 'Kéo thả một trường', 'Drag',
                                                   ['After:', '– Đổi thứ tự cột sẽ có trong tệp.']])

    # 2.12 Lịch sử
    s = section(doc, r'^2\.12 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu chưa có thao tác',
            '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → hiện dòng “Chưa có lịch sử thao tác '
            'nào.”')
    kv_append(kv, 'Dòng sự kiện phụ', '• Bấm Bộ lọc → lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.')
    ui = sec_ui(s)
    ui_set(ui, r'^Nút Xem lịch sử / Thu gọn$', {col(ui, 'Mô tả'): 'Ở màn chi tiết: thu gọn sẵn, bấm để mở / đóng '
                                                                  'danh sách.'})
    clone_row_after(ui, r'^Nút Làm mới$', [None, 'Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị',
                                            'Mở hàng lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.'])
    clone_row_after(ui, r'^Nút Bộ lọc$', [None, 'Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị',
                                           'Chỉ có ở Modal mở từ màn danh sách; đóng cửa sổ.'])
    ui_set(ui, r'^Trạng thái rỗng$', {col(ui, 'Mô tả'): 'Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống '
                                                         'mới: Modal hiện “Chưa có lịch sử thay đổi.”, khối ở màn chi '
                                                         'tiết hiện “Chưa có lịch sử thao tác nào.”.'})
    clone_row_after(sec_ev(s), r'^Bấm Xem lịch sử$', [None, 'Bấm biểu tượng Lịch sử ở cột Hành động', 'Click',
                                                     ['After:', '– Mở Modal Lịch sử phiếu xuất giữ của phiếu, mới nhất '
                                                      'trước.']])


def patch_part4(doc):
    h = part_heading(doc, 4)
    tbl = h.getnext()
    while tbl.tag != W('tbl'):
        tbl = tbl.getnext()

    def desc(code, old_regex, new):
        tc = cells(find_row(tbl, 1, '^%s$' % code))[3]
        write_cell(tc, lines_replace(cell_lines(tc), old_regex, new))

    desc('BR-10', r'^– Nút không dùng được thì ẩn', None)
    last = rows(tbl)[-1]
    tr = strip_ids(copy.deepcopy(last))
    tbl.append(tr)
    cs = cells(tr)
    write_cell(cs[1], ['BR-13'])
    write_cell(cs[2], ['Sau mỗi thao tác đưa người dùng về danh sách'])
    write_cell(cs[3], ['– Lưu nháp, Không duyệt, Duyệt giữ hàng và Xóa ở màn chi tiết xong đều đưa người dùng về màn '
                       'danh sách Phiếu xuất giữ.'])
    write_cell(cs[4], ['Toàn màn hình'])
    renumber_stt(tbl)
    for i, tr in enumerate(rows(tbl)[1:], 1):
        assert txt(cells(tr)[1]).strip() == 'BR-%02d' % i, 'Mã BR không liên tục ở dòng %d' % i


def add_part5(doc):
    h4 = part_heading(doc, 4)
    anchor = doc.element.body[-1].getprevious()
    h5 = clone_heading(h4, 'Phần 5: Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    intro = strip_ids(docxlib.clone_par_after(h5, h4.getnext(), 'Các màn hình dưới đây đọc dữ liệu do %s ghi ra '
                                              '(trạng thái của yêu cầu nguồn và lô hàng giữ sinh ra khi Duyệt giữ hàng '
                                              '— Phiếu xuất giữ là nơi DUY NHẤT sinh lô hàng giữ).' % SCREEN))
    tpl = sec_ev(section(doc, r'^2\.1 '))
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], PART5, [850, 1500, 3600, 2900])
    log('Thêm Phần 5 (%d màn tham chiếu)' % len(PART5))


if __name__ == '__main__':
    main()

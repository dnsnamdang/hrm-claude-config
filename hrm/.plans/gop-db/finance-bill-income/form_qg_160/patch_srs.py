# -*- coding: utf-8 -*-
"""Vá SRS "Phiếu thu tiền" (bản Drive 28/10) theo FORM "Danh mục quốc gia" (TPE Pass).

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/SRS - Phiếu thu tiền.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Chạy lại bao nhiêu lần cũng được: luôn đọc bản Drive gốc, không đọc file out.
Khuôn chép từ màn 27 (finance-product-import-direct-transfer/form_qg/patch_srs.py); phần hàm nằm ở
../../phieu-theo-form-quoc-gia/formqg_lib.py.
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
OUT = os.path.join(OUT_DIR, 'SRS - Phiếu thu tiền.docx')
UML = os.path.join(HERE, 'uml')
SHOTS = os.path.join(HERE, 'hdsd_shots')

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'Phiếu thu tiền'
# finance.js: hubGroup 'Quản lý tiền' > nhóm 'Thanh toán tiền mặt' > mục 'Phiếu thu' (đã đúng ở bản Drive)
MENU = 'Phân hệ Tài chính => Quản lý tiền => Thanh toán tiền mặt => Phiếu thu'
TAIL = ' Chỉ bổ sung quy tắc riêng của %s.' % SCREEN
UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: nếu chưa nhập hoặc thay đổi gì thì rời màn '
           'ngay; nếu đã nhập dữ liệu thì hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” '
           '(Thoát / Ở lại).')
UNSAVED_EV = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
              '– Đã nhập dữ liệu → hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”; '
              'bấm Thoát thì rời màn và bỏ thay đổi, bấm Ở lại thì giữ nguyên màn.']

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Phạm vi phiếu nhìn thấy theo quyền Xem tất cả phiếu thu của tổng công ty (V1) và Xem tất '
              'cả phiếu thu của công ty (V2); không có quyền nào thì chỉ thấy phiếu của mình.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (V1, V2); không có quyền nào vẫn xem được phiếu do chính mình lập.')
ACTOR_Q1 = 'Người dùng có quyền Kế toán thanh toán (Q1).'
ACTOR_Q2 = 'Người dùng có quyền Thủ quỹ duyệt phiếu thu (Q2).'
COND_Q2 = ('1. Đăng nhập thành công.\n2. Có quyền Thủ quỹ duyệt phiếu thu (Q2).\n'
           '3. Phiếu đang ở trạng thái Chờ duyệt.')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người lập phiếu; người đã duyệt phiếu; người có quyền Xem tất cả '
               'phiếu thu của tổng công ty (V1); hoặc người có quyền Xem tất cả phiếu thu của công ty (V2) cùng công '
               'ty với phiếu.')
COND_SCOPE = ('1. Đăng nhập thành công.\n'
              '2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu ở trạng thái Đang tạo chỉ người lập xem được.')
ACTOR_OWNER = ('Người lập phiếu — người dùng có quyền thực hiện chức năng: chỉ người đã lập phiếu '
               '(chức năng không gắn quyền riêng).')
COND_OWNER = ('1. Đăng nhập thành công.\n'
              '2. Là người lập phiếu (chức năng không gắn quyền riêng).\n'
              '3. Phiếu đang ở trạng thái Đang tạo.')
LIST3 = '\n3. Đang ở màn danh sách phiếu.'

# Mục 2.x: regex tiêu đề -> vế sau link "Quy tắc chung", Tác nhân, Điều kiện ban đầu
SECTIONS = {
    r'^2\.1 Xem danh sách': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 Tìm kiếm': ('Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.', ACTOR_LIST, COND_LIST + LIST3),
    r'^2\.3 Tuỳ chỉnh': ('Bộ lọc, Cấu hình cột và lưu cấu hình theo người dùng.', ACTOR_LIST, COND_LIST + LIST3),
    r'^2\.4 Tạo mới': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_Q1,
                       '1. Đăng nhập thành công.\n2. Có quyền Kế toán thanh toán (Q1).\n'
                       '3. Có ít nhất một phiếu đề nghị thu tiền ở trạng thái Chờ KT duyệt và chưa lập phiếu thu.'),
    r'^2\.5 Chọn phiếu': ('Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.', ACTOR_Q1,
                          '1. Đăng nhập thành công.\n2. Có quyền Kế toán thanh toán (Q1).\n'
                          '3. Đang ở màn Tạo mới hoặc Sửa phiếu thu.'),
    r'^2\.6 Sửa': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_Q1,
                   '1. Đăng nhập thành công.\n2. Có quyền Kế toán thanh toán (Q1).\n'
                   '3. Phiếu đang ở trạng thái Đang tạo.'),
    r'^2\.7 Xem chi tiết': ('Màn Xem chi tiết và Phân quyền.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.8 Duyệt': ('Thông báo, Validate dữ liệu, Quy tắc ghi lịch sử và UI/UX của thao tác đổi trạng thái.',
                     ACTOR_Q2, COND_Q2),
    r'^2\.9 Hủy': ('Thông báo, Validate dữ liệu, Quy tắc ghi lịch sử và UI/UX của thao tác đổi trạng thái.',
                   ACTOR_Q2, COND_Q2),
    r'^2\.10 Xóa': ('Quy tắc xóa và Thông báo.', ACTOR_OWNER, COND_OWNER),
    r'^2\.11 In': ('Quy tắc màn In và bố cục bản in.', ACTOR_SCOPE,
                   '1. Đăng nhập thành công.\n2. Có quyền xem phiếu như mục Tác nhân.\n'
                   '3. Phiếu không thuộc loại thu “Thu khác”.'),
    r'^2\.12 Xuất Excel': ('Quy tắc Excel.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.13 Xem lịch sử': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_SCOPE, COND_SCOPE),
}

POPUP_RX = r'được mở|mở từ menu|nằm ngay|mở ngay|Cửa sổ Lịch sử mở'
# Dòng "Menu:" + câu popup đặt ngay sau dòng Menu (None = giữ câu cũ / không thêm)
MENU_LINES = {
    r'^2\.3 ': ('Menu: %s => Cài đặt bộ lọc / Tùy chỉnh cột' % MENU,
                'Modal Cài đặt bộ lọc và Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.4 ': ('Menu: %s => Tạo mới' % MENU,
                'Modal Xác nhận lưu và gửi duyệt được mở ngay trên màn hình Thêm phiếu thu tiền theo đường dẫn ở trên.'),
    r'^2\.5 ': ('Menu: %s => Tạo mới / Sửa => ô Số phiếu đề nghị' % MENU,
                'Modal Chọn phiếu đề nghị thu được mở ngay trên màn hình Thêm phiếu thu tiền hoặc Sửa phiếu thu tiền '
                'theo đường dẫn ở trên.'),
    r'^2\.6 ': ('Menu: %s => Sửa (trên dòng phiếu) / Xem chi tiết => Sửa' % MENU,
                'Modal Xác nhận lưu và gửi duyệt được mở ngay trên màn hình Sửa phiếu thu tiền theo đường dẫn ở trên.'),
    r'^2\.7 ': ('Menu: %s => Mã phiếu (mở màn chi tiết)' % MENU, None),
    r'^2\.8 ': ('Menu: %s => Xem chi tiết => Duyệt phiếu thu' % MENU,
                'Ô nhập Số tiền thực thu và khối Phân bổ nằm ngay trên màn hình chi tiết phiếu. Modal Xác nhận duyệt '
                'được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
    r'^2\.9 ': ('Menu: %s => Xem chi tiết => Hủy phiếu thu' % MENU,
                'Modal Hủy phiếu thu tiền được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
    r'^2\.10 ': ('Menu: %s => Xóa (trên dòng phiếu) / Xem chi tiết => Xóa' % MENU,
                 'Modal Xác nhận xóa được mở ngay trên màn hình danh sách (biểu tượng Xóa trên dòng) hoặc màn hình '
                 'chi tiết phiếu (nút Xóa) theo đường dẫn ở trên.'),
    r'^2\.11 ': ('Menu: %s => In (cột Hành động của dòng phiếu) / Xem chi tiết => In' % MENU,
                 'Modal Xem trước phiếu thu được mở ngay trên màn hình danh sách hoặc màn hình chi tiết phiếu theo '
                 'đường dẫn ở trên.'),
    r'^2\.12 ': ('Menu: %s => Xuất Excel (cột Hành động của dòng phiếu) / Xem chi tiết => Xuất Excel' % MENU,
                 'Không có cửa sổ riêng: bấm nút là tệp Excel của phiếu được tải về máy.'),
    r'^2\.13 ': ('Menu: %s => Lịch sử (cột Hành động của dòng phiếu) / Xem chi tiết => Xem lịch sử' % MENU,
                 'Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối Lịch sử '
                 'thay đổi nằm cuối màn hình chi tiết phiếu.'),
}

# Use Case từng chức năng thao tác: regex mục -> (actor, mã, tên, nhóm màu)
USECASES = {
    r'^2\.4 ': ('Kế toán thanh toán', 'FR-04', 'Tạo mới phiếu thu', 'crud'),
    r'^2\.5 ': ('Kế toán thanh toán', 'FR-05', 'Chọn phiếu đề nghị thu', 'crud'),
    r'^2\.6 ': ('Kế toán thanh toán', 'FR-06', 'Sửa phiếu thu', 'crud'),
    r'^2\.7 ': ('Người dùng có quyền', 'FR-07', 'Xem chi tiết phiếu thu', 'view'),
    r'^2\.8 ': ('Thủ quỹ', 'FR-08', 'Duyệt phiếu thu', 'action'),
    r'^2\.9 ': ('Thủ quỹ', 'FR-09', 'Hủy phiếu thu', 'action'),
    r'^2\.10 ': ('Người lập phiếu', 'FR-10', 'Xóa phiếu thu', 'action'),
    r'^2\.11 ': ('Người dùng có quyền', 'FR-11', 'In phiếu thu', 'io'),
    r'^2\.12 ': ('Người dùng có quyền', 'FR-12', 'Xuất Excel một phiếu', 'io'),
}

PART5 = [  # STT | Nhóm (phân hệ) | Màn hình | Đường dẫn (menu cha)
    ('1', 'Tài chính', 'Đề nghị thu tiền (trạng thái Đã tạo phiếu thu / Đã hạch toán / Hủy và số tiền thực thu từng '
     'dòng do phiếu thu ghi ngược về)', 'Tài chính -> Quản lý tiền -> Đề nghị (và Khởi tạo -> Khởi tạo phiếu yêu cầu '
     '- Công nợ - Thu - Chi)'),
    ('2', 'Tài chính', 'Khai báo đầu kỳ công nợ (khai báo bị khóa sửa/xóa khi hợp đồng đã có phiếu thu được hạch '
     'toán)', 'Tài chính -> Khai báo đầu kỳ; Tài chính -> Kế toán công nợ -> Khách hàng'),
    ('3', 'Tài chính', 'Yêu cầu xuất giữ, Yêu cầu gia hạn hàng giữ, Phiếu yêu cầu điều chuyển hàng giữ (tiền đã thu '
     'theo hợp đồng quyết định phiếu có phải qua Ban giám đốc duyệt)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Giữ hàng'),
    ('4', 'Danh mục', 'Danh mục tài khoản (chặn xóa tài khoản đã dùng làm Tài khoản nợ / Số tài khoản có trên '
     'phiếu thu)', 'Tài chính -> Danh mục'),
    ('5', 'Bán hàng', 'Báo cáo công nợ: Đối chiếu công nợ 1 KH, Tổng hợp công nợ theo NV, Chi tiết công nợ KH '
     '(số tiền đã thu từ bút toán phiếu thu)', 'Bán hàng -> Báo cáo -> Báo cáo công nợ'),
    ('6', 'Bán hàng', 'Báo cáo theo dõi giữ hàng (cột Tổng thanh toán tính cả phiếu thu)',
     'Bán hàng -> Báo cáo -> Hàng giữ'),
    ('7', 'Bán hàng', 'Hợp đồng (Ngày hiệu lực theo điều kiện “đặt cọc lần đầu” lấy ngày hạch toán phiếu thu sớm '
     'nhất)', 'Bán hàng -> Bán hàng -> Hợp đồng bán hàng'),
]

# Loại đối tượng chuẩn hóa (checklist): bỏ Number / Text / Badge / Toast / Alert
def norm_type(name, loai, trang_thai):
    n = name.strip()
    if loai == 'Badge':
        return 'Table/Grid'
    if loai == 'Toast / Alert':
        return 'Label'
    if loai == 'Number':
        if n.startswith('Cột') and 'Enable' not in trang_thai:
            return 'Table/Grid'
        return 'Textbox'
    if loai == 'Text':
        if n.startswith('Cột'):
            return 'Table/Grid'
        if n.startswith('Khối'):
            return 'Label'
        return 'Textbox'
    return None


# ============================================================== TIỆN ÍCH
def lines_replace(lines, old_regex, new):
    out = []
    for l in lines:
        if re.search(old_regex, l):
            if new is not None:
                out.extend(new if isinstance(new, list) else [new])
        else:
            out.append(l)
    return out


def kv_edit(kv, key, old_regex, new):
    write_cell(kv_row(kv, key), lines_replace(kv_get(kv, key), old_regex, new))


def kv_lines(kv, key, lines):
    write_cell(kv_row(kv, key), lines)


def ev_cell(ev, event_regex, col=3):
    return cells(find_row(ev, 1, event_regex))[col]


def ev_edit(ev, event_regex, old_regex, new):
    tc = ev_cell(ev, event_regex)
    write_cell(tc, lines_replace(cell_lines(tc), old_regex, new))


def ev_set(ev, event_regex, lines, rid=None):
    write_cell(ev_cell(ev, event_regex), lines, rid)


def ui_desc(ui, name_regex, text):
    write_cell(cells(find_row(ui, 1, name_regex))[-1], [text])


def ui_set(ui, name_regex, col_name, text):
    write_cell(cells(find_row(ui, 1, name_regex))[header_index(ui, col_name)], [text])


def fix_types(doc):
    n = 0
    for e in items(doc):
        if e.tag != W('tbl'):
            continue
        hdr = [txt(c).strip() for c in cells(rows(e)[0])]
        if 'Tên đối tượng' not in hdr or 'Loại' not in hdr:
            continue
        il, it = hdr.index('Loại'), hdr.index('Trạng thái') if 'Trạng thái' in hdr else None
        for tr in rows(e)[1:]:
            cs = cells(tr)
            new = norm_type(txt(cs[1]), txt(cs[il]).strip(), txt(cs[it]) if it is not None else '')
            if new:
                write_cell(cs[il], [new])
                n += 1
    log('Chuẩn hóa cột Loại: %d dòng' % n)


def fit_width(img_par, png):
    """Ảnh hộp thoại nhỏ (rộng < 1100px) thì thu khung theo tỷ lệ ảnh/1100 để chữ không phóng to quá cỡ."""
    from PIL import Image
    w, h = Image.open(png).size
    if w >= 1100:
        return
    ext = next(img_par.iter(L.WP_NS + 'extent'))
    cx = int(int(ext.get('cx')) * max(w, 550) / 1100.0)
    cy = int(cx * h / w)
    ext.set('cx', str(cx)); ext.set('cy', str(cy))
    for x in img_par.iter(L.A_NS + 'ext'):
        if x.get('cx'):
            x.set('cx', str(cx)); x.set('cy', str(cy))


def add_image_after(doc, cap_par, png, caption):
    """Nhân bản cặp (đoạn ảnh, chú thích) ngay trước cap_par rồi đặt sau cap_par, thay ảnh + chú thích."""
    img_par = cap_par.getprevious()
    new_img = strip_ids(copy.deepcopy(img_par))
    new_cap = strip_ids(copy.deepcopy(cap_par))
    cap_par.addnext(new_img)
    new_img.addnext(new_cap)
    nid = max_docpr(doc) + 1
    for dp in new_img.iter(L.WP_NS + 'docPr'):
        dp.set('id', str(nid))
        dp.set('name', 'Hinh %d' % nid)
    set_image(doc, new_img, png)
    fit_width(new_img, png)
    set_runs_text(new_cap, 'Hình 0: ' + caption)
    log('Thêm ảnh: ' + caption)
    return new_cap


def replace_image(doc, sec, cap_regex, png, caption=None):
    cap = sec_par(sec, cap_regex)
    img = cap.getprevious()
    set_image(doc, img, png)
    fit_width(img, png)
    if caption:
        set_runs_text(cap, 'Hình 0: ' + caption)
    log('Thay ảnh: ' + txt(cap))
    return cap


def para_set(doc, regex, text):
    for e in items(doc):
        if e.tag == W('p') and re.search(regex, txt(e)):
            set_runs_text(e, text)
            return e
    raise KeyError(regex)


def term_set(doc, term, text):
    for e in items(doc):
        if e.tag == W('tbl') and txt(cells(rows(e)[0])[0]).strip() == 'Thuật ngữ':
            for tr in rows(e)[1:]:
                if txt(cells(tr)[0]).strip() == term:
                    write_cell(cells(tr)[1], [text])
                    return
    raise KeyError(term)


def keep_with_next(doc):
    """Ảnh liền chú thích 'Hình n', tiêu đề mục con / Heading3 liền đoạn sau (không rơi cuối trang)."""
    n = 0
    els = items(doc)
    for i, e in enumerate(els[:-1]):
        if e.tag != W('p'):
            continue
        nxt = els[i + 1]
        is_img = bool(list(e.iter(L.A_NS + 'blip'))) and nxt.tag == W('p') and txt(nxt).startswith('Hình ')
        is_head = is_sub(e) or style_of(e) == 'Heading3' or (txt(e).strip() in ('Đường dẫn màn hình:',))
        if is_img or is_head:
            ppr = e.find(W('pPr'))
            if ppr is None:
                ppr = L._el('pPr')
                e.insert(0, ppr)
            if ppr.find(W('keepNext')) is None:
                kn = L._el('keepNext')
                ps = ppr.find(W('pStyle'))
                (ps.addnext(kn) if ps is not None else ppr.insert(0, kn))
                n += 1
    log('keepNext: %d đoạn' % n)


def shot(name):
    p = os.path.join(SHOTS, name + '.png')
    assert os.path.exists(p), 'Thiếu ảnh ' + p
    return p


# ============================================================== XỬ LÝ
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)

    # 1. Từng mục 2.x: dòng Quy tắc chung, Tác nhân, Điều kiện ban đầu
    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        p = sec_par(sec, r'^Quy tắc (chung|áp dụng):')
        set_rule_tail(p, ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    # 2. Dòng Menu + câu popup
    for rx, (menu, popup) in MENU_LINES.items():
        sec = section(doc, rx)
        p = sec_par(sec, r'^Menu:')
        set_runs_text(p, menu)
        nxt = p.getnext()
        is_old_popup = nxt is not None and nxt.tag == W('p') and re.search(POPUP_RX, txt(nxt))
        if popup and is_old_popup:
            set_runs_text(nxt, popup)
        elif popup:
            strip_ids(docxlib.clone_par_after(p, p, popup))

    patch_part1_2(doc)
    patch_sections(doc, rid)
    fix_types(doc)
    patch_part4(doc)
    add_part5(doc)

    # 3. Use Case: bỏ ở FR-03, thêm FR-07, vẽ lại các sơ đồ còn lại (actor + 1 use case)
    remove_usecase(doc, section(doc, r'^2\.3 '))
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
    leftover(doc)
    keep_with_next(doc)

    doc.save(OUT)
    print('Đã ghi', OUT)
    for m in L.LOG:
        print(' -', m)
    if '--no-word' not in sys.argv:
        word_finalize(OUT, os.path.join(OUT_DIR, 'SRS - Phiếu thu tiền.pdf'))


TECH = r'endpoint|fail-closed|khóa dòng|KHÓA DÒNG|khoá dòng|render|resolve|\blog\b|giao dịch|select\b|cổng cũ|\bgate\b|' \
       r'phía máy chủ|phía giao diện|truy vấn|bí danh|phép so'


def leftover(doc):
    for e in doc.element.body.iter(W('t')):
        if e.text and re.search(TECH, e.text):
            log('CÒN THUẬT NGỮ KỸ THUẬT: ' + e.text[:160])


def patch_part1_2(doc):
    term_set(doc, 'Phiếu đề nghị thu tiền', 'Chứng từ do người kinh doanh lập trước đó. Một phiếu đề nghị chỉ lập được '
             'đúng một phiếu thu; hai người bấm lưu cùng lúc vẫn chỉ tạo được một phiếu thu.')
    # Phần 2 — bảng quyền
    for e in items(doc):
        if e.tag == W('tbl') and txt(cells(rows(e)[0])[0]).strip() == 'Ký hiệu':
            for tr in rows(e)[1:]:
                cs = cells(tr)
                k = txt(cs[0]).strip()
                if k == 'Q1':
                    write_cell(cs[2], ['Mở được cửa sổ chọn phiếu đề nghị; lập và sửa phiếu thu. Hệ thống kiểm tra '
                                       'quyền ngay khi lưu, không chỉ dựa vào việc ẩn nút trên màn hình.'])
                if k == 'V2':
                    write_cell(cs[2], ['Phiếu thu thuộc công ty của người đăng nhập. Không xác định được công ty thì '
                                       'chỉ thấy phiếu do chính mình lập.'])
    para_set(doc, r'^Không xác định được người đăng nhập thì danh sách rỗng',
             'Không xác định được người đăng nhập thì danh sách rỗng.')


def patch_sections(doc, rid):
    # ---------------- 2.1 Xem danh sách
    s = section(doc, r'^2\.1 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^1\. Người dùng vào menu', '1. Người dùng vào menu %s.' % MENU)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. Hệ thống trả về',
            '4. Hệ thống hiển thị trang đầu tiên, sắp xếp theo Ngày tạo giảm dần, kèm tổng số phiếu.')
    kv_edit(kv, 'Mô tả', r'ô lọc Người lập', 'Hiển thị bảng phiếu thu nằm trong phạm vi dữ liệu của người đăng nhập, kèm '
            'phân trang và ô thống kê tổng số phiếu khớp bộ lọc. Chỉ có một mục menu trỏ vào màn này; ba cách xem trước '
            'đây (“của tôi”, “chờ duyệt”, “đã duyệt”) nay là ô lọc Người tạo và ô lọc Trạng thái.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'danh sách rỗng tuyệt đối', '• Không xác định được người đăng nhập → danh sách rỗng.')
    ui = sec_ui(s)
    ui_desc(ui, r'^Nút Tạo mới$', 'Luôn hiển thị; người không có quyền Kế toán thanh toán (Q1) bấm lưu sẽ nhận '
            'thông báo “Bạn không có quyền lập phiếu thu”.')
    ui_desc(ui, r'^Cột Loại thu$', 'Thu bán hàng / Thu nhà cung cấp / Thu khác, lấy theo phiếu đề nghị.')
    ui_desc(ui, r'^Cột Khách hàng$', 'Mã và tên khách hàng của dòng chi tiết đầu tiên; phiếu thu nhà cung cấp để '
            'trống ô này.')
    ui_desc(ui, r'^Cột Hành động$', 'Luôn hiển thị, không tắt được. Gồm Sửa, Xóa, Duyệt (mở màn chi tiết), In, Xuất '
            'Excel, Lịch sử; nút không dùng được với phiếu thì ẩn. Tối đa 2–3 nút hiện trực tiếp, phần còn lại trong '
            'menu ba chấm.')
    ui_desc(ui, r'^Cột Trạng thái$', 'Nhãn đỏ với Đang tạo / Chờ duyệt / Hủy; nhãn xanh với Đã duyệt.')
    ev = sec_ev(s)
    ev_set(ev, r'^Mở màn hình$', ['Before:', '– Khôi phục bộ lọc đã lưu nếu còn trong 10 phút.',
                                   '– Xác định cấp quyền xem cao nhất của người dùng.', 'During:',
                                   '– Lọc phiếu theo phạm vi dữ liệu của cấp quyền.',
                                   '– Loại bỏ phiếu Đang tạo của người khác.', 'After:',
                                   '– Hiển thị trang 1 sắp xếp theo Ngày tạo giảm dần, kèm tổng số phiếu.'])
    ev_set(ev, r'^Bấm tiêu đề cột sắp xếp$', ['Before:', '– Chỉ bốn cột sắp xếp được: Mã phiếu, Số tiền, Ngày tạo, '
                                               'Ngày cập nhật.', 'After:',
                                               '– Đảo chiều sắp xếp, đưa về trang 1, giữ nguyên bộ lọc.'])

    # ---------------- 2.2 Tìm kiếm
    s = section(doc, r'^2\.2 ')
    kv = sec_kv(s)
    kv_lines(kv, 'Dòng sự kiện chính', [
        '1. Người dùng nhập mã phiếu vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter); hoặc bấm Tìm kiếm nâng cao '
        'rồi đặt điều kiện ở các ô lọc.',
        '2. Với ô tìm nhanh: hệ thống chỉ tìm khi bấm Tìm kiếm hoặc nhấn Enter, không tự tìm khi đang gõ.',
        '3. Với các ô lọc nâng cao: hệ thống lọc lại ngay khi giá trị thay đổi.',
        '4. Hệ thống áp bộ lọc bên trong phạm vi dữ liệu theo quyền, đưa về trang 1 và hiển thị kết quả.',
        '5. Hệ thống lưu bộ lọc trong 10 phút để khôi phục khi quay lại màn.'])
    kv_lines(kv, 'Dòng sự kiện phụ', [
        '• Không kết quả → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”',
        '• Bấm Làm mới → xoá mọi điều kiện, về trang 1, phạm vi quyền giữ nguyên.',
        '• Người dùng không có V1 lẫn V2 → không hiển thị ô Công ty / Phòng ban / Bộ phận.'])
    ui = sec_ui(s)
    ui_desc(ui, r'^Ô tìm nhanh$', 'Dòng gợi ý “Tìm theo mã phiếu...”. Không tự tìm khi gõ — bấm nút Tìm kiếm hoặc '
            'nhấn Enter.')
    ui_desc(ui, r'^Nhóm ô Công ty', 'Chỉ hiển thị khi người dùng có V1 hoặc V2. Lọc theo đơn vị ghi trên phiếu đề nghị.')
    tr = find_row(ui, 1, r'^Ô lọc Người lập$')
    write_cell(cells(tr)[1], ['Ô lọc Người tạo'])
    write_cell(cells(tr)[-1], ['Lọc theo người tạo phiếu thu.'])
    ui_desc(ui, r'^Ô lọc Khách hàng$', 'Phải gõ từ 2 ký tự trở lên mới hiện gợi ý. Danh sách khách hàng dùng chung '
            'với phiếu đề nghị.')
    tr = find_row(ui, 1, r'^Ô lọc Số tiền')
    write_cell(cells(tr)[1], ['Ô lọc Số tiền (từ → đến)'])
    tr = find_row(ui, 1, r'^Ô lọc Ngày lập')
    write_cell(cells(tr)[1], ['Ô lọc Ngày lập (từ → đến)'])
    replace_image(doc, s, r'^Hình \d+: Khối Tìm kiếm nâng cao', shot('02_filter'))
    ev = sec_ev(s)
    delete_row(ev, r'^Gõ vào ô tìm nhanh')
    write_cell(cells(find_row(ev, 1, r'^Bấm nút Tìm kiếm$'))[1], ['Bấm nút Tìm kiếm hoặc nhấn Enter trong ô tìm nhanh'])
    ev_set(ev, r'^Đổi giá trị một ô lọc', ['During:', '– Cộng dồn với các điều kiện đang có (quan hệ VÀ).',
                                           '– Ba ô đơn vị tổ chức và ô Loại thu lọc theo thông tin ghi trên phiếu đề nghị.',
                                           'After:', '– Đưa về trang 1, nạp lại danh sách, lưu bộ lọc trong 10 phút.'])

    # ---------------- 2.3 Tuỳ chỉnh bộ lọc / cột
    s = section(doc, r'^2\.3 ')
    kv_lines(sec_kv(s), 'Yêu cầu đặc biệt', [
        'Dòng “Công ty – Phòng ban – Bộ phận” luôn có trong cửa sổ Cài đặt bộ lọc, nhưng các ô đó chỉ hiển thị trên '
        'màn khi người dùng có quyền V1 hoặc V2.'])
    kv_edit(sec_kv(s), 'Dòng sự kiện phụ', r'^• Bấm Đóng',
            '• Bấm Đóng / (x) / click ra ngoài cửa sổ → thoát ngay, không lưu thay đổi, không hỏi xác nhận.')
    ev = sec_ev(s)
    clone_row_after(ev, r'^Bỏ tích một mục', [None, 'Kéo thả một dòng', 'Drag',
                                              ['After:', '– Đổi thứ tự ô lọc / cột theo vị trí thả; áp dụng khi bấm Lưu.']])

    # ---------------- 2.4 Tạo mới
    s = section(doc, r'^2\.4 ')
    kv = sec_kv(s)
    kv_lines(kv, 'Dòng sự kiện chính', [
        '1. Người dùng bấm nút Tạo mới.',
        '2. Hệ thống mở màn Thêm phiếu thu tiền, chọn sẵn tài khoản nợ mặc định và điền tỷ giá bằng 1.',
        '3. Người dùng chọn phiếu đề nghị; hệ thống kéo về loại thu, loại tiền, người đề nghị, phòng ban, lý do thu và '
        'toàn bộ dòng chi tiết.',
        '4. Người dùng nhập Người nộp, chỉnh số tiền duyệt thu và ghi chú từng dòng nếu cần.',
        '5. Người dùng bấm Lưu (trạng thái Đang tạo), Lưu và tiếp tục (lưu nháp rồi mở lại màn Thêm mới trống) hoặc '
        'Lưu và gửi duyệt (trạng thái Chờ duyệt, có hộp xác nhận “Xác nhận lưu và gửi duyệt”).',
        '6. Hệ thống kiểm tra dữ liệu, kiểm tra phiếu đề nghị chưa có phiếu thu nào, sinh mã tự động, lưu phiếu cùng '
        'các dòng chi tiết và tính tổng số tiền duyệt thu.',
        '7. Nếu gửi duyệt: phiếu đề nghị chuyển sang “Đã tạo phiếu thu” và hệ thống gửi thông báo cho mọi thủ quỹ cùng '
        'công ty với phiếu.',
        '8. Ghi nhận hành động Tạo mới trong lịch sử của phiếu.',
        '9. Hệ thống hiển thị thông báo thành công và quay về màn danh sách (Lưu và tiếp tục: ở lại màn Thêm mới).'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bấm Quay lại', UNSAVED)
    ui = sec_ui(s)
    ui_set(ui, r'^Người nộp$', 'Phạm vi', '1–255 ký tự')
    clone_row_after(ui, r'^Nút Lưu$', [None, 'Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', 'Hiển thị',
                                       'Chỉ có ở màn Tạo mới. Lưu ở trạng thái Đang tạo rồi mở lại màn Thêm mới trống '
                                       'để lập phiếu khác.'])
    ui_desc(ui, r'^Nút Lưu và gửi duyệt$', 'Mở hộp xác nhận “Xác nhận lưu và gửi duyệt” trước khi lưu ở trạng thái '
            'Chờ duyệt.')
    ui_desc(ui, r'^Nút Quay lại$', 'Về màn danh sách; hỏi xác nhận nếu có thay đổi chưa lưu.')
    ev = sec_ev(s)
    write_cell(cells(find_row(ev, 1, r'^Bấm Lưu / Lưu và gửi duyệt'))[1],
               ['Bấm Lưu / Lưu và tiếp tục / Lưu và gửi duyệt'])
    ev_set(ev, r'^Bấm Lưu / Lưu và tiếp tục', [
        'Before:',
        '– Với Lưu và gửi duyệt: mở hộp xác nhận “Xác nhận lưu và gửi duyệt”, chỉ tiếp tục khi người dùng bấm Xác nhận.',
        'During:',
        '– Chưa chọn phiếu đề nghị → hiển thị “Bắt buộc nhập”.',
        '– Chưa chọn Tài khoản nợ → hiển thị “Bắt buộc nhập”; tài khoản không tồn tại → “Không tồn tại”.',
        '– Chưa nhập Người nộp → hiển thị “Bắt buộc nhập”.',
        '– Chưa nhập Tỷ giá → hiển thị “Bắt buộc nhập”; không phải số → “Phải là số”.',
        '– Bảng chi tiết rỗng → hiển thị “Bắt buộc nhập”.',
        '– Dòng thiếu Số tài khoản có → hiển thị “Bắt buộc nhập”.',
        '– Dòng thiếu Số tiền duyệt thu → hiển thị “Bắt buộc nhập”; không phải số → “Phải là số”.',
        '– Ghi chú vượt 1.000 ký tự → báo lỗi.',
        '– Không có quyền Q1 → hiển thị “Bạn không có quyền lập phiếu thu”.',
        '– Phiếu đề nghị đã có phiếu thu khác (kể cả do người khác vừa lưu cùng lúc) → hiển thị “Đề nghị thu tiền đã '
        'lập phiếu thu tiền”.',
        'After:',
        '– Sinh mã phiếu tự động, không trùng kể cả khi hai người lưu cùng lúc; lưu phiếu và các dòng chi tiết, tính '
        'tổng số tiền duyệt thu.',
        '– Ghi công ty / phòng ban / bộ phận theo hồ sơ người lập.',
        '– Nếu trạng thái là Chờ duyệt: cập nhật phiếu đề nghị sang “Đã tạo phiếu thu”, ghi nhận vào lịch sử của phiếu '
        'đề nghị và gửi thông báo tới mọi thủ quỹ cùng công ty.',
        '– Ghi nhận hành động Tạo mới trong lịch sử của phiếu thu.',
        '– Hiển thị thông báo “Thêm phiếu thu tiền thành công!” (lưu nháp) hoặc “Phiếu thu tiền tạo thành công! Phiếu '
        'thu tiền cần được duyệt trước khi có hiệu lực, vui lòng theo dõi thông báo” (gửi duyệt), rồi quay về danh '
        'sách; Lưu và tiếp tục thì ở lại màn Thêm mới trống.'])
    add_err_line(ev, r'^Bấm Lưu / Lưu và tiếp tục', rid)
    clone_row_after(ev, r'^Bấm Lưu / Lưu và tiếp tục',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])
    replace_image(doc, s, r'^Hình \d+: Màn Thêm phiếu thu tiền khi vừa mở', shot('10_create'))
    replace_image(doc, s, r'^Hình \d+: Màn Thêm phiếu thu tiền sau khi chọn', shot('10b_filled'))
    cap = sec_par(s, r'^Hình \d+: Màn Thêm phiếu thu tiền sau khi chọn')
    add_image_after(doc, cap, shot('14_sendapprove'), 'Hộp xác nhận lưu và gửi duyệt')

    # ---------------- 2.5 Chọn phiếu đề nghị
    s = section(doc, r'^2\.5 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^2\. Hệ thống kiểm tra quyền Q1',
            '2. Hệ thống mở cửa sổ, liệt kê phiếu đề nghị đang ở trạng thái Chờ KT duyệt VÀ chưa có phiếu thu nào, sắp '
            'xếp mới nhất trước.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bấm Đóng',
            '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận; ô Số phiếu đề nghị giữ '
            'nguyên giá trị cũ.')
    kv_lines(kv, 'Yêu cầu đặc biệt', [
        'Cửa sổ này cố ý không áp phạm vi xem của màn Phiếu đề nghị thu tiền — mọi người có quyền Kế toán thanh toán '
        '(Q1) đều chọn được mọi phiếu đề nghị đủ điều kiện; việc nạp dữ liệu phiếu đề nghị về form cũng chỉ kiểm tra '
        'quyền Q1.'])
    ui = sec_ui(s)
    ui_desc(ui, r'^Tiêu đề cửa sổ$', 'Phụ đề ghi “Chỉ phiếu Chờ duyệt và chưa lập phiếu thu”.')
    ev = sec_ev(s)
    ev_set(ev, r'^Bấm vào ô Số phiếu đề nghị', ['Before:', '– Không có quyền Q1 → hiển thị “Bạn không có quyền xem danh '
                                                 'sách phiếu đề nghị thu”, danh sách trống.', 'After:',
                                                 '– Mở cửa sổ và nạp danh sách phiếu đề nghị đủ điều kiện.'])
    ev_edit(ev, r'^Bấm vào một dòng phiếu', r'endpoint kéo dữ liệu',
            '– Kiểm tra lại quyền Q1 khi nạp dữ liệu phiếu đề nghị; không có quyền → “Bạn không có quyền xem phiếu đề '
            'nghị thu”.')

    # ---------------- 2.6 Sửa
    s = section(doc, r'^2\.6 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^2\. Hệ thống kiểm tra quyền',
            '2. Hệ thống kiểm tra trạng thái phiếu; phiếu không còn Đang tạo thì chuyển sang màn chi tiết.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. ', [
        '6. Ghi nhận các thay đổi (theo từng trường và từng dòng chi tiết) trong lịch sử của phiếu; trạng thái đổi thì '
        'ghi thêm một dòng đổi trạng thái.',
        '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bấm Quay lại', UNSAVED)
    ui = sec_ui(s)
    ui_desc(ui, r'^Nút Quay lại$', 'Về màn danh sách; hỏi xác nhận nếu có thay đổi chưa lưu.')
    ui_desc(ui, r'^Nút Lưu và gửi duyệt$', 'Mở hộp xác nhận “Xác nhận lưu và gửi duyệt”; chuyển phiếu sang Chờ duyệt.')
    ev = sec_ev(s)
    ev_set(ev, r'^Bấm nút Sửa$', [
        'Before:', '– Nút chỉ hiển thị khi phiếu ở trạng thái Đang tạo.',
        '– Mở màn Sửa của phiếu không còn ở Đang tạo (ví dụ vào thẳng bằng đường dẫn) → chuyển sang màn chi tiết phiếu.',
        'After:', '– Mở màn Sửa và nạp dữ liệu đã lưu, kèm tài khoản đã khóa (nếu có) để ô chọn hiện đúng tên.'])
    ev_set(ev, r'^Bấm Lưu / Lưu và gửi duyệt', [
        'Before:', '– Với Lưu và gửi duyệt: mở hộp xác nhận “Xác nhận lưu và gửi duyệt”, chỉ tiếp tục khi bấm Xác nhận.',
        'During:', '– Áp toàn bộ quy tắc kiểm tra như màn Tạo mới.',
        '– Không có quyền Q1 → hiển thị “Bạn không có quyền sửa phiếu thu”.',
        '– Phiếu không còn ở Đang tạo → hiển thị “Phiếu thu đã gửi duyệt hoặc đã duyệt, không sửa được”.',
        '– Kiểm tra ràng buộc một phiếu đề nghị một phiếu thu, bỏ qua chính phiếu đang sửa.',
        'After:', '– Lưu lại phiếu, thay toàn bộ dòng chi tiết theo dữ liệu mới, tính lại tổng số tiền duyệt thu, cập '
                  'nhật người sửa gần nhất.',
        '– Nếu chuyển sang Chờ duyệt: cập nhật phiếu đề nghị sang “Đã tạo phiếu thu” và gửi thông báo cho thủ quỹ cùng '
        'công ty.',
        '– Ghi nhận thay đổi trong lịch sử; nếu trạng thái đổi thì ghi thêm một dòng đổi trạng thái bằng TÊN trạng thái.',
        '– Hiển thị “Cập nhật phiếu thu tiền thành công!” và quay về danh sách.'])
    add_err_line(ev, r'^Bấm Lưu / Lưu và gửi duyệt', rid)
    clone_row_after(ev, r'^Bấm Lưu / Lưu và gửi duyệt',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # ---------------- 2.7 Xem chi tiết
    s = section(doc, r'^2\.7 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ',
            '4. Hệ thống hiển thị nội dung và các nút Sửa, Duyệt phiếu thu, Hủy phiếu thu, In, Xuất Excel, Xóa theo '
            'quyền và trạng thái phiếu (giống các nút trên dòng phiếu ở màn danh sách).')
    kv_lines(kv, 'Dòng sự kiện phụ', [
        '• Không đủ quyền xem → từ chối với thông báo “Bạn không có quyền xem phiếu thu này” và quay về màn danh sách.',
        '• Phiếu không tồn tại hoặc không tải được → báo lỗi và quay về màn danh sách.',
        '• Phiếu Đang tạo của người khác → không xem được (quyền theo cấp không mở phiếu nháp của người khác).',
        '• Hợp đồng của một dòng đã bị xoá → ô Số đơn hàng/Hợp đồng của dòng đó để trống, các dòng khác vẫn hiển thị '
        'bình thường.'])
    ui = sec_ui(s)
    ui_desc(ui, r'^Nút Duyệt phiếu thu$', 'Chỉ hiện với phiếu Chờ duyệt và người xem có quyền Q2. Bấm nút thì hiện hộp '
            'xác nhận “Xác nhận duyệt”.')
    ui_desc(ui, r'^Nút Quay lại$', 'Về danh sách, giữ nguyên bộ lọc đã lưu.')
    ev = sec_ev(s)
    ev_set(ev, r'^Mở màn chi tiết$', [
        'Before:', '– Nạp phiếu kèm dòng chi tiết, đối tượng thu, hợp đồng, phiếu đề nghị và người liên quan.',
        '– Kiểm tra quyền xem: là người lập, hoặc là người đã duyệt, hoặc là quản trị hệ thống, hoặc có V1, hoặc có V2 '
        'và cùng công ty. Phiếu Đang tạo của người khác luôn bị chặn.',
        '– Không đủ quyền → hiển thị “Bạn không có quyền xem phiếu thu này”.',
        'During:', '– Dòng có hợp đồng đã bị xoá → để trống ô hợp đồng của dòng đó, không ảnh hưởng các dòng khác.',
        'After:', '– Hiển thị nội dung và các nút theo quyền và trạng thái phiếu.'])
    ev_edit(ev, r'^Gõ vào ô Số tiền thực thu', r'^– Nút Duyệt bị chặn',
            '– Còn ô lỗi thì bấm Duyệt phiếu thu bị dừng, không mở hộp xác nhận.')

    # ---------------- 2.8 Duyệt
    s = section(doc, r'^2\.8 ')
    kv = sec_kv(s)
    kv_lines(kv, 'Dòng sự kiện chính', [
        '1. Thủ quỹ mở màn chi tiết phiếu đang Chờ duyệt.',
        '2. Thủ quỹ nhập số tiền thực thu cho từng dòng, hoặc nhập Số tiền phân bổ rồi bấm Phân bổ để điền hộ.',
        '3. Thủ quỹ bấm nút Duyệt phiếu thu; hệ thống kiểm tra các ô Số tiền thực thu và hiện hộp xác nhận “Xác nhận '
        'duyệt”.',
        '4. Thủ quỹ bấm Duyệt trong hộp xác nhận.',
        '5. Hệ thống kiểm tra lại quyền và trạng thái phiếu, ghi số thực thu vào từng dòng, chuyển phiếu sang Đã duyệt, '
        'ghi ngày hạch toán và người duyệt.',
        '6. Hệ thống chuyển phiếu đề nghị sang “Đã hạch toán”, ghi bút toán vào sổ kế toán và cập nhật số thực thu về '
        'các dòng tương ứng của phiếu đề nghị.',
        '7. Ghi nhận hành động Duyệt (kèm số thực thu từng dòng, ngày hạch toán) trong lịch sử của phiếu thu và của '
        'phiếu đề nghị.',
        '8. Hệ thống báo duyệt thành công và quay về màn danh sách.'])
    kv_lines(kv, 'Dòng sự kiện phụ', [
        '• Bấm Hủy ở hộp xác nhận → không duyệt, phiếu giữ nguyên.',
        '• Thiếu quyền Q2 → từ chối với thông báo “Bạn không có quyền duyệt phiếu thu”.',
        '• Phiếu không còn ở trạng thái Chờ duyệt (người khác vừa duyệt hoặc hủy) → thông báo “Phiếu thu tiền đã được '
        'duyệt!” và tải lại màn chi tiết.',
        '• Số thực thu vượt số duyệt thu của dòng → hiển thị “Không được lớn hơn số tiền duyệt thu ({số duyệt thu})” '
        'ngay dưới ô, không duyệt.',
        '• Số thực thu âm → hiển thị “Không được âm”.',
        '• Bấm nút nhiều lần liên tiếp → chỉ ghi nhận một lần.',
        '• Bước 5–7 được thực hiện trọn vẹn cùng lúc: có lỗi ở bất kỳ bước nào thì phiếu giữ nguyên, không ghi bút '
        'toán.'])
    ui = sec_ui(s)
    ui_desc(ui, r'^Nút Duyệt phiếu thu$', 'Kiểm tra các ô Số tiền thực thu rồi mở hộp xác nhận. Bị khoá trong lúc '
            'đang xử lý để chống bấm nhiều lần.')
    clone_row_after(ui, r'^Nút Duyệt phiếu thu$', [None, 'Hộp xác nhận “Xác nhận duyệt”', 'Label', 'Hiển thị', '–', '–',
                                                   'Ẩn', 'Nội dung “Bạn có chắc muốn duyệt phiếu thu "{mã phiếu}"?”; '
                                                   'nút Duyệt thực hiện duyệt, nút Hủy đóng hộp thoại.'])
    ev = sec_ev(s)
    ev_set(ev, r'^Bấm nút Duyệt phiếu thu$', [
        'Before:', '– Bỏ qua nếu đang có một lần duyệt chưa xử lý xong.',
        '– Kiểm tra các ô Số tiền thực thu trên màn hình; có ô lỗi thì dừng và báo đỏ ngay dưới ô.',
        'After:', '– Mở hộp xác nhận “Xác nhận duyệt”.'])
    clone_row_after(ev, r'^Bấm nút Duyệt phiếu thu$', [None, 'Bấm Duyệt trong hộp xác nhận', 'Click', [
        'Before:', '– Đọc lại trạng thái mới nhất của phiếu (hai thủ quỹ bấm duyệt cùng lúc chỉ một người thành công).',
        '– Không có quyền Q2 → hiển thị “Bạn không có quyền duyệt phiếu thu” và dừng xử lý.',
        '– Phiếu không còn ở Chờ duyệt → hiển thị “Phiếu thu tiền đã được duyệt!”, tải lại màn chi tiết và dừng xử lý.',
        'During:', '– Số thực thu của một dòng vượt số duyệt thu của chính dòng đó → hiển thị “Không được lớn hơn số '
                   'tiền duyệt thu” ngay dưới ô.',
        '– Số thực thu âm → hiển thị “Không được âm”; không phải số → “Phải là số”.',
        'After:', '– Ghi số thực thu vào từng dòng chi tiết.',
        '– Chuyển phiếu sang Đã duyệt, ghi ngày hạch toán (ngày duyệt) và người duyệt.',
        '– Chuyển phiếu đề nghị sang “Đã hạch toán” và ghi nhận vào lịch sử của phiếu đề nghị.',
        '– Ghi bút toán vào sổ kế toán cho từng dòng có số thực thu lớn hơn 0.',
        '– Cập nhật số thực thu về các dòng tương ứng của phiếu đề nghị.',
        '– KHÔNG tính lại tổng số tiền của phiếu (xem BR-08).',
        '– Ghi hai dòng lịch sử: một dòng thay đổi thông tin (số thực thu từng dòng, ngày hạch toán), một dòng đổi '
        'trạng thái kèm ghi chú đã ghi bút toán.',
        '– Hiển thị “Duyệt phiếu thu thành công!” và quay về danh sách.']])
    add_err_line(ev, r'^Bấm Duyệt trong hộp xác nhận', rid)
    cap = sec_par(s, r'^Hình \d+: Màn chi tiết phiếu Chờ duyệt')
    replace_image(doc, s, r'^Hình \d+: Màn chi tiết phiếu Chờ duyệt', shot('15_approve'))
    add_image_after(doc, cap, shot('15b_confirm'), 'Hộp xác nhận duyệt phiếu thu')

    # ---------------- 2.9 Hủy
    s = section(doc, r'^2\.9 ')
    kv = sec_kv(s)
    kv_lines(kv, 'Dòng sự kiện chính', [
        '1. Thủ quỹ mở màn chi tiết phiếu đang Chờ duyệt.',
        '2. Thủ quỹ bấm nút Hủy phiếu thu; hệ thống mở cửa sổ nhập lý do.',
        '3. Thủ quỹ nhập lý do hủy và bấm Xác nhận.',
        '4. Hệ thống kiểm tra lại quyền và trạng thái phiếu.',
        '5. Hệ thống chuyển phiếu sang Hủy và ghi lý do vào ô Ghi chú của phiếu.',
        '6. Hệ thống chuyển phiếu đề nghị sang Hủy và ghi nhận kèm lý do vào lịch sử của phiếu đề nghị.',
        '7. Ghi nhận hành động Hủy kèm lý do trong lịch sử của phiếu thu.',
        '8. Hệ thống báo hủy thành công, đóng cửa sổ và quay về màn danh sách.'])
    kv_lines(kv, 'Dòng sự kiện phụ', [
        '• Lý do hủy để trống → hiển thị “Lý do hủy – Bắt buộc nhập” ngay dưới ô; cửa sổ không đóng.',
        '• Lý do hủy vượt 1.000 ký tự → hiển thị “Tối đa 1000 ký tự”.',
        '• Thiếu quyền Q2 → từ chối với thông báo “Bạn không có quyền hủy phiếu thu”.',
        '• Phiếu không còn ở Chờ duyệt → thông báo “Phiếu thu tiền đã được duyệt!”, đóng cửa sổ và tải lại màn chi tiết.',
        '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận kể cả khi đã nhập lý do; '
        'phiếu giữ nguyên trạng thái.'])
    ui = sec_ui(s)
    ui_desc(ui, r'^Lỗi inline của Lý do hủy$', 'Chữ đỏ “Lý do hủy – Bắt buộc nhập” ngay dưới ô; tự mất khi người dùng '
            'gõ nội dung.')
    ev = sec_ev(s)
    ev_set(ev, r'^Bấm Xác nhận trong cửa sổ hủy', [
        'Before:', '– Bỏ qua nếu đang có một lần xử lý chưa xong.',
        '– Lý do hủy để trống → hiển thị “Lý do hủy – Bắt buộc nhập” ngay dưới ô và dừng.',
        'During:', '– Đọc lại trạng thái mới nhất của phiếu; không có quyền Q2 → “Bạn không có quyền hủy phiếu thu”; '
                   'phiếu không còn Chờ duyệt → “Phiếu thu tiền đã được duyệt!”.',
        '– Lý do hủy vượt 1.000 ký tự → hiển thị “Tối đa 1000 ký tự”.',
        'After:', '– Chuyển phiếu sang Hủy và ghi lý do vào ô Ghi chú của phiếu.',
        '– Ghi nhận hành động Hủy kèm lý do trong lịch sử của phiếu thu.',
        '– Chuyển phiếu đề nghị sang Hủy và ghi nhận kèm lý do vào lịch sử của phiếu đề nghị.',
        '– KHÔNG ghi bút toán nào vào sổ kế toán.',
        '– Hiển thị “Hủy phiếu thu thành công!”, đóng cửa sổ và quay về màn danh sách.'])
    add_err_line(ev, r'^Bấm Xác nhận trong cửa sổ hủy', rid)
    clone_row_after(ev, r'^Bấm Xác nhận trong cửa sổ hủy', [None, 'Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
                                                            ['After:', '– Đóng cửa sổ ngay, không hỏi xác nhận; phiếu '
                                                             'giữ nguyên trạng thái.']])
    replace_image(doc, s, r'^Hình \d+: Cửa sổ Hủy phiếu thu', shot('16_cancel'))

    # ---------------- 2.10 Xóa
    s = section(doc, r'^2\.10 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ',
            '4. Hệ thống kiểm tra lại trạng thái và người lập rồi xoá phiếu cùng toàn bộ dòng chi tiết.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Ghi nhận hành động Xóa (kèm nội dung phiếu) trong lịch sử.',
        '6. Hệ thống hiển thị thông báo “Xóa thành công”: xóa từ màn danh sách thì nạp lại danh sách, xóa từ màn chi '
        'tiết thì quay về màn danh sách.'])
    ui = sec_ui(s)
    write_cell(cells(find_row(ui, 1, r'^Nội dung hộp thoại$'))[header_index(ui, 'Giá trị ban đầu')],
               ['Bạn có chắc muốn xóa phiếu thu tiền \'{mã phiếu}\'?'])
    ev = sec_ev(s)
    ev_set(ev, r'^Bấm Xóa trong hộp xác nhận$', [
        'Before:', '– Kiểm tra lại phiếu ở Đang tạo; không thoả → hiển thị “Phiếu thu đã gửi duyệt hoặc đã duyệt, không '
                   'xóa được” và nạp lại danh sách.',
        '– Kiểm tra người lập; không phải người lập và không phải quản trị hệ thống → hiển thị “Bạn không có quyền xóa '
        'phiếu thu này”.',
        'After:', '– Ghi nhận hành động Xóa kèm nội dung phiếu và bảng chi tiết vào lịch sử.',
        '– Xoá phiếu cùng toàn bộ dòng chi tiết.',
        '– Hiển thị “Xóa thành công”; ở màn danh sách thì nạp lại danh sách, ở màn chi tiết thì quay về danh sách.'])
    add_err_line(ev, r'^Bấm Xóa trong hộp xác nhận$', rid)
    replace_image(doc, s, r'^Hình \d+: Hộp xác nhận xóa', shot('13_delete'))

    # ---------------- 2.11 In
    s = section(doc, r'^2\.11 ')
    kv = sec_kv(s)
    kv_lines(kv, 'Mô tả', ['Mở cửa sổ xem trước bản in của phiếu ngay trên màn hình, gồm đủ 2 liên, kèm ảnh tiêu đề '
                           'thư của công ty ghi trên phiếu; bấm In để in.'])
    kv_lines(kv, 'Dòng sự kiện chính', [
        '1. Người dùng bấm In ở cột Hành động của dòng phiếu, hoặc nút In trên màn chi tiết.',
        '2. Hệ thống kiểm tra quyền xem phiếu, chọn mẫu in theo loại thu và số dòng chi tiết rồi điền dữ liệu phiếu vào '
        'mẫu.',
        '3. Hệ thống mở cửa sổ “Xem trước phiếu thu {mã phiếu}” hiển thị bản in 2 liên.',
        '4. Người dùng bấm In để mở hộp thoại in của trình duyệt, hoặc đóng cửa sổ.'])
    kv_lines(kv, 'Dòng sự kiện phụ', [
        '• Không đủ quyền xem → cửa sổ báo “Bạn không có quyền xem phiếu thu này”.',
        '• Phiếu thuộc loại thu “Thu khác” → không có mẫu in; nút In bị ẩn ở cả danh sách lẫn màn chi tiết.',
        '• Không tìm thấy mẫu in → cửa sổ báo “Không tìm thấy mẫu in phiếu thu trên hệ thống”.'])
    ui = sec_ui(s)
    tr = find_row(ui, 1, r'^Nút In trên trang in$')
    write_cell(cells(tr)[1], ['Nút In trong cửa sổ xem trước'])
    write_cell(cells(tr)[-1], ['Mở hộp thoại in của trình duyệt để in bản xem trước.'])
    ui_set(ui, r'^Ảnh tiêu đề thư$', 'Loại', 'Image')
    ui_desc(ui, r'^Ảnh tiêu đề thư$', 'Lấy theo công ty ghi trên phiếu: logo, tên công ty, địa chỉ, điện thoại, email, '
            'website.')
    ev = sec_ev(s)
    ev_set(ev, r'^Bấm nút In$', ['Before:', '– Nút chỉ hiển thị khi phiếu không thuộc loại thu “Thu khác”.',
                                 'After:', '– Mở cửa sổ Xem trước phiếu thu ngay trên màn hình đang đứng.'])
    tr = find_row(ev, 1, r'^Mở trang in$')
    write_cell(cells(tr)[1], ['Nạp bản xem trước'])
    write_cell(cells(tr)[3], ['Before:', '– Kiểm tra quyền xem phiếu như chức năng Xem chi tiết; không đủ quyền → '
                                         'hiển thị “Bạn không có quyền xem phiếu thu này”.',
                              'During:', '– Chọn mẫu in theo loại thu và số dòng chi tiết rồi điền dữ liệu phiếu vào '
                                         'mẫu; không có mẫu → báo “Không tìm thấy mẫu in phiếu thu trên hệ thống”.',
                              'After:', '– Hiển thị bản in 2 liên trong cửa sổ; không ghi bất kỳ thay đổi nào lên '
                                        'phiếu.'])
    clone_row_after(ev, r'^Nạp bản xem trước$', [None, 'Bấm In trong cửa sổ xem trước', 'Click',
                                                ['After:', '– Mở hộp thoại in của trình duyệt với bản in 2 liên.']])
    replace_image(doc, s, r'^Hình \d+: Bản in phiếu thu', shot('18_print'), 'Cửa sổ Xem trước phiếu thu — đủ 2 liên')

    # ---------------- 2.12 Xuất Excel
    s = section(doc, r'^2\.12 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^3\. ', '3. Hệ thống dựng tệp từ dữ liệu phiếu và tải về máy.')
    kv_lines(kv, 'Dòng sự kiện phụ', [
        '• Không đủ quyền xem → báo “Lỗi khi xuất Excel phiếu thu”, không tải tệp.',
        '• Xuất thành công → báo “Xuất Excel thành công”.',
        '• Nút bị khoá trong lúc đang dựng tệp để tránh tải trùng.'])
    kv_lines(kv, 'Yêu cầu đặc biệt', [
        'Khác nút In, chức năng này dùng được cả với phiếu thuộc loại thu “Thu khác” vì không phụ thuộc mẫu in. Tên '
        'tệp dạng Phieu-thu-tien-{mã phiếu}.xlsx (dấu chấm trong mã đổi thành gạch ngang).'])
    ev = sec_ev(s)
    ev_set(ev, r'^Bấm nút Xuất Excel$', [
        'Before:', '– Kiểm tra quyền xem phiếu; không đủ quyền → báo “Lỗi khi xuất Excel phiếu thu” và dừng xử lý.',
        'After:', '– Dựng tệp Phieu-thu-tien-{mã phiếu}.xlsx từ dữ liệu của đúng phiếu đó, tải về máy và báo “Xuất '
                  'Excel thành công”.'])

    # ---------------- 2.13 Lịch sử
    s = section(doc, r'^2\.13 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu chưa từng thao tác',
            '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → hiện dòng “Chưa có lịch sử thao tác '
            'nào.”')
    kv_lines(kv, 'Yêu cầu đặc biệt', ['Đổi trạng thái luôn là một dòng lịch sử riêng, tách khỏi dòng thay đổi thông '
                                      'tin.'])
    ui = sec_ui(s)
    ui_desc(ui, r'^Trạng thái rỗng$', 'Hiện “Chưa có lịch sử thao tác nào.” với phiếu lập từ hệ thống cũ, chưa có '
            'thao tác nào trên hệ thống mới.')
    ui_desc(ui, r'^Nút Bộ lọc$', 'Lọc các mốc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.')
    ev = sec_ev(s)
    ev_set(ev, r'^Bấm Lịch sử / Xem lịch sử$', ['After:', '– Nạp các mốc lịch sử của đúng phiếu đó, sắp xếp mới nhất '
                                                'trước; khối Lịch sử ở màn chi tiết chỉ nạp khi bấm Xem lịch sử lần '
                                                'đầu.'])
    write_cell(cells(find_row(ev, 1, r'^Chọn nhóm thao tác'))[1], ['Chọn điều kiện trong Bộ lọc'])


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

    def desc(code, old_regex, new):
        tc = cells(find_row(tbl, 1, '^%s$' % code))[3]
        write_cell(tc, lines_replace(cell_lines(tc), old_regex, new))

    def name(code, new):
        write_cell(cells(find_row(tbl, 1, '^%s$' % code))[2], [new])

    desc('BR-01', r'danh sách rỗng tuyệt đối', '– Không xác định được người đăng nhập thì danh sách rỗng.')
    desc('BR-04', r'^– Mọi kiểm tra đều thực hiện', '– Hệ thống kiểm tra lại các điều kiện này ngay khi lưu, không chỉ '
         'dựa vào việc ẩn nút trên màn hình.')
    desc('BR-05', r'KHÓA DÒNG', '– Khi lưu, hệ thống kiểm tra lại phiếu đề nghị ngay tại thời điểm ghi, nên hai người '
         'bấm lưu cùng lúc vẫn chỉ tạo được một phiếu thu; người sau nhận thông báo “Đề nghị thu tiền đã lập phiếu thu '
         'tiền”.')
    desc('BR-07', r'^– Ngoại lệ', '– Ngoại lệ: phiếu đang gắn tài khoản đã bị khóa thì tài khoản đó vẫn hiện đúng tên '
         'trong ô chọn, tránh việc người dùng vô tình lưu đè mất giá trị cũ.')
    desc('BR-08', r'cổng cũ', '– Quy tắc này giữ cho số liệu khớp với hệ thống ERP cũ.')
    desc('BR-10', r'cổng cũ', '– Sổ kế toán dùng chung với hệ thống ERP cũ nên bút toán ghi loại chứng từ đúng như ERP '
         'để hai hệ thống đọc được của nhau.')
    desc('BR-10', r'giao dịch', '– Bước duyệt được thực hiện trọn vẹn: hoặc phiếu đổi trạng thái và bút toán được ghi '
         'đầy đủ, hoặc không có gì thay đổi.')
    name('BR-11', 'Chặn duyệt trùng và tạo trùng')
    write_cell(cells(find_row(tbl, 1, '^BR-11$'))[3], [
        '– Trước khi duyệt hoặc hủy, hệ thống đọc lại trạng thái mới nhất của phiếu; phiếu đã rời trạng thái Chờ duyệt '
        'thì từ chối với thông báo “Phiếu thu tiền đã được duyệt!”.',
        '– Nhờ vậy hai thủ quỹ bấm duyệt cùng lúc không thể ghi trùng bút toán.',
        '– Nút bấm bị khoá trong lúc xử lý để tránh bấm nhiều lần; hệ thống vẫn kiểm tra lại khi lưu.',
        '– Mã phiếu sinh tự động không bị trùng kể cả khi hai người lưu cùng lúc.'])
    desc('BR-12', r'^– Ba điểm hở', '– Ba điểm hở kế thừa từ hệ thống ERP cũ, đã chốt GIỮ NGUYÊN: xóa phiếu thu nháp '
         'không trả trạng thái phiếu đề nghị về; hủy phiếu thu là ngõ cụt; lưu nháp phiếu thu không đổi trạng thái '
         'phiếu đề nghị nên phiếu đề nghị vẫn hiện “Chờ KT duyệt” dù đã có phiếu thu nháp.')
    desc('BR-09', r'phía máy chủ', '– Không được âm và KHÔNG được lớn hơn số tiền duyệt thu của chính dòng đó; kiểm '
         'tra ngay khi nhập và kiểm tra lại khi duyệt.')
    desc('BR-14', r'gán đè vô điều kiện', '– Công ty, phòng ban và bộ phận của phiếu lấy theo hồ sơ của NGƯỜI LẬP tại '
         'thời điểm tạo; người dùng không chọn được.')
    desc('BR-15', r'endpoint in', '– Phiếu loại “Thu khác” KHÔNG có mẫu in: nút In bị ẩn ở cả danh sách lẫn màn chi '
         'tiết.')
    name('BR-16', 'Nội dung lịch sử riêng của phiếu')
    desc('BR-16', r'^– (Ghi một dòng lịch sử khi|Đổi trạng thái luôn là)', None)
    for i, tr in enumerate(rows(tbl)[1:], 1):
        assert txt(cells(tr)[1]).strip() == 'BR-%02d' % i, 'Mã BR không liên tục ở dòng %d' % i


def add_part5(doc):
    h4 = part_heading(doc, 4)
    last = doc.element.body[-1]  # sectPr
    anchor = last.getprevious()
    h5 = clone_heading(h4, 'Phần 5. Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    intro = docxlib.clone_par_after(h5, h4.getnext(), 'Các màn hình dưới đây đọc dữ liệu do %s ghi ra (trạng thái '
                                    'và số thực thu ghi ngược về phiếu đề nghị, bút toán ghi vào sổ kế toán khi phiếu '
                                    'được duyệt, tài khoản dùng trên phiếu).' % SCREEN)
    strip_ids(intro)
    tpl = sec_ev(section(doc, r'^2\.1 '))
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], PART5, [850, 1300, 3800, 2900])
    log('Thêm Phần 5 (%d màn tham chiếu)' % len(PART5))


if __name__ == '__main__':
    main()

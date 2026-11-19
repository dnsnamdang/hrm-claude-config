# -*- coding: utf-8 -*-
"""Hàm dùng chung cho patch_srs.py của 2 màn hàng giữ (form_qg_32 Yêu cầu hủy, form_qg_191 Phiếu hủy).

Bổ sung cho ../phieu-theo-form-quoc-gia/formqg_lib.py (KHÔNG sửa thư viện chung đó):
  - Bản Drive của 2 màn này để tiêu đề 2.x.y là Heading4 (32) hoặc đoạn thường (191) -> chuẩn hóa hết về
    Heading4 và cho `is_sub` nhận cả 2 kiểu.
  - Thay ảnh có co giãn theo kích thước ảnh (popup nhỏ không bị kéo to bằng khổ trang).
"""
import copy
import os
import re

from formqg_lib import *  # noqa: F401,F403
import formqg_lib as L
import docxlib

UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: nếu chưa nhập hoặc thay đổi gì thì rời màn '
           'ngay; nếu đã nhập dữ liệu thì hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” '
           '(Thoát / Ở lại).')
UNSAVED_EV = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
              '– Đã nhập dữ liệu → hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”; bấm Thoát '
              'thì rời màn và bỏ thay đổi, bấm Ở lại thì giữ nguyên màn.']
SUB_RX = r'^\d+\.\d+\.\d+ '


def is_sub(e):
    return e.tag == W('p') and style_of(e) in ('', 'Heading4') and re.match(SUB_RX, txt(e))


L.is_sub = is_sub  # các hàm của formqg_lib (remove_usecase, renumber_subheadings…) dùng bản này


def set_style(p, style):
    ppr = p.find(W('pPr'))
    if ppr is None:
        ppr = docxlib._el('pPr')
        p.insert(0, ppr)
    ps = ppr.find(W('pStyle'))
    if ps is None:
        ps = docxlib._el('pStyle')
        ppr.insert(0, ps)
    ps.set(W('val'), style)


def normalize_subheadings(doc):
    """Mọi tiêu đề 2.x.y -> style Heading4 (bản Drive lẫn lộn đoạn thường / Heading4)."""
    n = 0
    in_part3 = False
    for e in items(doc):
        if e.tag != W('p'):
            continue
        st = style_of(e)
        if st == 'Heading1':
            in_part3 = txt(e).startswith('Phần 3')
        if in_part3 and st == '' and re.match(SUB_RX, txt(e)):
            set_style(e, 'Heading4')
            n += 1
    if n:
        log('Đặt style Heading4 cho %d tiêu đề 2.x.y đang là đoạn thường' % n)


# ------------------------------------------------------------------ sửa ô bảng
def lines_replace(lines, old_regex, new):
    out = []
    for ln in lines:
        if re.search(old_regex, ln):
            if new is not None:
                out.extend(new if isinstance(new, list) else [new])
        else:
            out.append(ln)
    return out


def kv_edit(kv, key, old_regex, new):
    before = kv_get(kv, key)
    after = lines_replace(before, old_regex, new)
    assert before != after or new is None and not any(re.search(old_regex, x) for x in before), \
        'kv_edit không khớp: %s / %s' % (key, old_regex)
    write_cell(kv_row(kv, key), after)


def ev_edit(ev, event_regex, old_regex, new):
    tc = cells(find_row(ev, 1, event_regex))[3]
    before = cell_lines(tc)
    after = lines_replace(before, old_regex, new)
    assert before != after, 'ev_edit không khớp: %s / %s' % (event_regex, old_regex)
    write_cell(tc, after)


def ev_set(ev, event_regex, lines):
    write_cell(cells(find_row(ev, 1, event_regex))[3], lines)


def ui_set(tbl, name_regex, values):
    tr = find_row(tbl, 1, name_regex)
    for col, val in values.items():
        write_cell(cells(tr)[header_index(tbl, col)], val if isinstance(val, list) else val.split('\n'))


def table_by_header(doc, first):
    for t in doc.element.body.iter(W('tbl')):
        if txt(cells(rows(t)[0])[0]).strip() == first:
            return t
    raise KeyError(first)


# ------------------------------------------------------------------ Layout
def drop_pars(doc, regexes):
    for e in items(doc):
        if e.tag == W('p') and any(re.search(r, txt(e)) for r in regexes):
            log('Bỏ câu đặt sai chỗ: ' + txt(e)[:70])
            e.getparent().remove(e)


def menu_pars(sec):
    """Dòng đường dẫn menu của mục: 'Menu: …' hoặc dòng 'Phân hệ …' (bản 191 thiếu chữ 'Menu:')."""
    return [e for e in sec[1] if e.tag == W('p') and re.match(r'^\s*(Menu:|Phân hệ |=> )', txt(e))]


def apply_menu_lines(doc, menu_lines):
    for (rx, k), (menu, popup) in menu_lines.items():
        sec = section(doc, rx)
        ps = menu_pars(sec)
        p = ps[k]
        set_runs_text(p, menu)
        nxt = p.getnext()
        if popup:
            if nxt is not None and nxt.tag == W('p') and re.search(r'được mở ngay', txt(nxt)):
                set_runs_text(nxt, popup)
            else:
                strip_ids(docxlib.clone_par_after(p, p, popup))


# ------------------------------------------------------------------ ảnh
def fit_image(img_par, png_path, max_w_in=6.2, max_h_in=7.6, px_per_in=135):
    from PIL import Image
    w, h = Image.open(png_path).size
    wi = min(max_w_in, w / float(px_per_in))
    hi = wi * h / w
    if hi > max_h_in:
        wi, hi = wi * max_h_in / hi, max_h_in
    cx, cy = int(wi * EMU), int(hi * EMU)
    next(img_par.iter(WP_NS + 'extent')).set('cx', str(cx))
    next(img_par.iter(WP_NS + 'extent')).set('cy', str(cy))
    for x in img_par.iter(A_NS + 'ext'):
        if x.get('cx'):
            x.set('cx', str(cx))
            x.set('cy', str(cy))


def caption_par(doc, regex):
    for e in items(doc):
        if e.tag == W('p') and re.match(r'^Hình \d+: ', txt(e)) and re.search(regex, txt(e)):
            return e
    raise KeyError(regex)


def replace_images(doc, images, shots):
    for regex, name, new_cap in images:
        cap = caption_par(doc, regex)
        img = cap.getprevious()
        assert list(img.iter(A_NS + 'blip')), 'trước chú thích không phải ảnh: ' + regex
        png = os.path.join(shots, name + '.png')
        set_image(doc, img, png)
        fit_image(img, png)
        if new_cap:
            num = re.match(r'^(Hình \d+: )', txt(cap)).group(1)
            set_runs_text(cap, num + new_cap)
        log('Thay ảnh "%s" bằng %s.png' % (txt(cap)[:60], name))


def redraw_usecases(doc, usecases, uml_dir, tpl_rx):
    for rx, (actor, code, name, grp) in usecases.items():
        png = os.path.join(uml_dir, 'uc_%s.png' % code.replace('-', ''))
        draw_usecase_qg(png, actor, code, name, grp)
        cap_text = 'Biểu đồ Use Case — %s %s' % (code, name)
        sec = section(doc, rx)
        blk = usecase_block(sec)
        if blk is None:
            add_usecase(doc, sec, section(doc, tpl_rx), png, cap_text)
        else:
            set_image(doc, blk[1], png)
            set_runs_text(blk[2], 'Hình 0: ' + cap_text)


# ------------------------------------------------------------------ Phần 4 / 5
def part_heading(doc, n):
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1' and txt(e).startswith('Phần %d' % n):
            return e
    raise KeyError(n)


def part4_intro(doc, screen):
    h = part_heading(doc, 4)
    intro = h.getnext()
    set_rule_head(intro, 'Quy tắc áp dụng: Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
    set_rule_tail(intro, '. Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc đã có trong SRS '
                         'quy tắc chung.' % screen)
    tbl = intro.getnext()
    while tbl.tag != W('tbl'):
        tbl = tbl.getnext()
    return tbl


def br_desc(tbl, code, old_regex, new):
    tc = cells(find_row(tbl, 1, '^%s$' % code))[3]
    before = cell_lines(tc)
    after = lines_replace(before, old_regex, new)
    assert before != after, 'br_desc không khớp %s %s' % (code, old_regex)
    write_cell(tc, after)


def check_br(tbl):
    for i, tr in enumerate(rows(tbl)[1:], 1):
        assert txt(cells(tr)[1]).strip() == 'BR-%02d' % i, 'Mã BR không liên tục ở dòng %d' % i


def add_part5(doc, part5, intro_text):
    h4 = part_heading(doc, 4)
    anchor = doc.element.body[-1].getprevious()
    h5 = clone_heading(h4, 'Phần 5: Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    intro = strip_ids(docxlib.clone_par_after(h5, h4.getnext(), intro_text))
    tpl = sec_ev(section(doc, r'^2\.1 '))
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], part5, [850, 1500, 3600, 2900])
    log('Thêm Phần 5 (%d màn tham chiếu)' % len(part5))


def drop_empty_before_h1(doc):
    """Đoạn trống ngay trước tiêu đề Phần (Heading1 tự sang trang) -> dễ đẻ 1 trang trắng khi trang trước vừa kín."""
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1':
            prev = e.getprevious()
            while prev is not None and prev.tag == W('p') and not txt(prev).strip() and not style_of(prev)                     and not list(prev.iter(A_NS + 'blip')) and prev.find('.//' + W('sectPr')) is None:
                nxt = prev.getprevious()
                prev.getparent().remove(prev)
                log('Bỏ đoạn trống trước "%s"' % txt(e)[:30])
                prev = nxt


# ------------------------------------------------------------------ kiểm
OK_TYPES = {'Label', 'Button', 'Icon Button', 'Table/Grid', 'Textbox', 'Textarea', 'Dropdown', 'Datepicker',
            'Checkbox', 'Pagination', 'Icon', 'Radio', 'Click', 'Change', 'System', 'Drag'}


def check_types(doc):
    for t in doc.element.body.iter(W('tbl')):
        hdr = [txt(c).strip() for c in cells(rows(t)[0])]
        for col in ('Loại', 'Loại event'):
            if col in hdr:
                i = hdr.index(col)
                for tr in rows(t)[1:]:
                    v = txt(cells(tr)[i]).strip()
                    if v not in OK_TYPES:
                        log('CẢNH BÁO loại lạ "%s" ở dòng "%s"' % (v, txt(cells(tr)[1])[:40]))

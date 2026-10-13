# Hàm vá docx tại chỗ (giữ định dạng có sẵn của tài liệu tester đã sửa tay).
import copy, re, unicodedata
from docx.oxml.ns import qn

W = lambda t: qn('w:' + t)


def nfc(s):
    return unicodedata.normalize('NFC', s or '')


def txt(e):
    return nfc(''.join(x.text or '' for x in e.iter(W('t'))))


def style_of(p):
    pp = p.find(W('pPr'))
    if pp is None or pp.find(W('pStyle')) is None:
        return ''
    return pp.find(W('pStyle')).get(W('val'))


def cells(tr):
    return tr.findall(W('tc'))


def _first_rpr(el):
    r = el.find('.//' + W('r'))
    if r is not None and r.find(W('rPr')) is not None:
        return copy.deepcopy(r.find(W('rPr')))
    return None


def _make_run(text, rpr):
    r = copy.deepcopy(rpr) if False else None
    run = _el('r')
    if rpr is not None:
        run.append(copy.deepcopy(rpr))
    t = _el('t')
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    run.append(t)
    return run


def _el(tag):
    from docx.oxml import OxmlElement
    return OxmlElement('w:' + tag)


def set_par_text(p, text, rpr=None):
    """Thay toàn bộ chữ của đoạn p, giữ pPr và rPr của run đầu."""
    if rpr is None:
        rpr = _first_rpr(p)
    for ch in list(p):
        if ch.tag != W('pPr'):
            p.remove(ch)
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if i:
            br = _el('r')
            if rpr is not None:
                br.append(copy.deepcopy(rpr))
            br.append(_el('br'))
            p.append(br)
        p.append(_make_run(line, rpr))


def set_cell_text(tc, text):
    """Ghi lại chữ 1 ô: mỗi dòng (\\n) thành 1 đoạn, nhân bản đoạn đầu của ô."""
    ps = tc.findall(W('p'))
    first = ps[0]
    rpr = _first_rpr(tc)
    for p in ps[1:]:
        tc.remove(p)
    lines = text.split('\n')
    set_par_text(first, lines[0], rpr)
    prev = first
    for line in lines[1:]:
        np_ = copy.deepcopy(first)
        set_par_text(np_, line, rpr)
        prev.addnext(np_)
        prev = np_


def clone_par_after(anchor, template_p, text, bold=None):
    np_ = copy.deepcopy(template_p)
    set_par_text(np_, text)
    if bold is not None:
        for r in np_.findall(W('r')):
            rpr = r.find(W('rPr'))
            if rpr is None:
                rpr = _el('rPr')
                r.insert(0, rpr)
            b = rpr.find(W('b'))
            if bold and b is None:
                rpr.insert(0, _el('b'))
            if not bold and b is not None:
                rpr.remove(b)
    anchor.addnext(np_)
    return np_


def clone_table_after(anchor, template_tbl, header, rows):
    """Bảng mới cùng khuôn template_tbl (cùng số cột): hàng tiêu đề + các hàng dữ liệu."""
    tbl = copy.deepcopy(template_tbl)
    trs = tbl.findall(W('tr'))
    hdr_tr, data_tr = trs[0], trs[1]
    for tr in trs:
        tbl.remove(tr)
    h = copy.deepcopy(hdr_tr)
    for tc, v in zip(cells(h), header):
        set_cell_text(tc, v)
    tbl.append(h)
    for row in rows:
        r = copy.deepcopy(data_tr)
        for tc, v in zip(cells(r), row):
            set_cell_text(tc, v)
        tbl.append(r)
    anchor.addnext(tbl)
    return tbl


def body_items(doc):
    return list(doc.element.body.iterchildren())


def find_section(doc, heading_regex):
    """Trả (start_idx, end_idx) của mục Heading3 khớp regex tới Heading1-3 kế tiếp."""
    items = body_items(doc)
    start = None
    for i, e in enumerate(items):
        if e.tag == W('p') and style_of(e).startswith('Heading') and re.search(heading_regex, txt(e), re.I):
            start = i
            lvl = style_of(e)
            break
    if start is None:
        return None, None, items
    end = len(items)
    for j in range(start + 1, len(items)):
        e = items[j]
        if e.tag == W('p') and style_of(e).startswith('Heading') and style_of(e) <= lvl:
            end = j
            break
    return start, end, items


def txt_br(e):
    out = []
    for x in e.iter():
        if x.tag == W('t'):
            out.append(x.text or '')
        elif x.tag in (W('br'), W('cr')):
            out.append('\n')
        elif x.tag == W('p') and out:
            out.append('\n')
    return nfc(''.join(out))

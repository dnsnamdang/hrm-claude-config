# -*- coding: utf-8 -*-
"""Hàm dùng chung để vá SRS (bản Drive, giữ định dạng người khác sửa tay) theo FORM "Danh mục quốc gia".

Dùng cho cả 16 màn: mỗi màn chỉ viết 1 file `form_qg/patch_srs.py` khai báo DỮ LIỆU (tác nhân, đường dẫn
menu, vế quy tắc chung...) rồi gọi các hàm ở đây. Xem mẫu: finance-product-import-direct-transfer/form_qg.

Quy ước tài liệu Drive (Google Docs xuất ra):
  - Mục 2.x là Heading3; mục con "2.x.y ..." là đoạn thường in đậm (không có style).
  - Ô bảng = 1 đoạn, 1 run, các dòng ngăn bằng <w:br/>.
  - Dòng "Quy tắc chung:" = run chữ + <w:hyperlink> "SRS_Các quy tắc chung_VN_1.0" + run đuôi.
"""
import copy, io, os, re, subprocess, sys

LIB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(LIB_DIR, '..', 'srs-tc-feedback-0710'))
from docxlib import W, txt, style_of, cells, _el  # noqa: E402

R_NS = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
A_NS = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
WP_NS = '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}'
W14 = '{http://schemas.microsoft.com/office/word/2010/wordml}'
LINK_TEXT = 'SRS_Các quy tắc chung_VN_1.0'
ERR_LINE = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung {LINK}, '
            'không thực hiện bước After.')
EMU = 914400

LOG = []


def log(msg):
    LOG.append(msg)


def items(doc):
    return list(doc.element.body.iterchildren())


def strip_ids(el):
    """Bỏ w14:paraId/textId của khối nhân bản để Word không thấy trùng id."""
    for e in el.iter():
        for a in (W14 + 'paraId', W14 + 'textId'):
            if a in e.attrib:
                del e.attrib[a]
    return el


# ------------------------------------------------------------------ đoạn văn

def set_runs_text(p, text):
    """Ghi lại chữ của đoạn (giữ pPr + rPr của run đầu), bỏ mọi run khác."""
    r0 = p.find('.//' + W('r'))
    rpr = copy.deepcopy(r0.find(W('rPr'))) if r0 is not None and r0.find(W('rPr')) is not None else None
    for ch in list(p):
        if ch.tag != W('pPr'):
            p.remove(ch)
    p.append(make_run(text, rpr))


def make_run(text, rpr):
    r = _el('r')
    if rpr is not None:
        r.append(copy.deepcopy(rpr))
    t = _el('t')
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r.append(t)
    return r


def set_bold(p, on=True):
    for r in p.iter(W('r')):
        rpr = r.find(W('rPr'))
        if rpr is None:
            rpr = _el('rPr')
            r.insert(0, rpr)
        for tag in ('b', 'bCs'):
            e = rpr.find(W(tag))
            if on and e is None:
                e = _el(tag)
                e.set(W('val'), '1')
                rpr.insert(0, e)
            elif e is not None:
                e.set(W('val'), '1' if on else '0')


def replace_in_texts(root, old, new):
    """Thay chuỗi trong từng <w:t> (chuỗi phải nằm gọn trong 1 run)."""
    n = 0
    for t in root.iter(W('t')):
        if t.text and old in t.text:
            t.text = t.text.replace(old, new)
            n += 1
    return n


def set_rule_tail(p, tail):
    """Dòng 'Quy tắc chung: ... [link] <tail>' — giữ nguyên phần trước + hyperlink, thay phần đuôi."""
    hl = p.find(W('hyperlink'))
    if hl is None:
        raise RuntimeError('Dòng quy tắc chung không có hyperlink: ' + txt(p))
    after = False
    rpr = None
    for ch in list(p):
        if ch is hl:
            after = True
            continue
        if ch.tag == W('r') and rpr is None and ch.find(W('rPr')) is not None:
            rpr = copy.deepcopy(ch.find(W('rPr')))
        if after:
            p.remove(ch)
    hl.addnext(make_run(tail, rpr))


def set_rule_head(p, head):
    """Thay phần chữ TRƯỚC hyperlink."""
    hl = p.find(W('hyperlink'))
    rpr = None
    for ch in list(p):
        if ch is hl:
            break
        if ch.tag == W('r'):
            if rpr is None and ch.find(W('rPr')) is not None:
                rpr = copy.deepcopy(ch.find(W('rPr')))
            p.remove(ch)
    hl.addprevious(make_run(head, rpr))


def link_rid(doc):
    for e in doc.element.body.iter(W('hyperlink')):
        if txt(e).strip() == LINK_TEXT and e.get(R_NS + 'id'):
            return e.get(R_NS + 'id')
    raise RuntimeError('Không tìm thấy hyperlink ' + LINK_TEXT)


# ------------------------------------------------------------------ ô bảng (1 đoạn, dòng ngăn bằng br)

def cell_lines(tc):
    out, cur = [], ''
    for e in tc.iter():
        if e.tag == W('t'):
            cur += e.text or ''
        elif e.tag in (W('br'), W('cr')):
            out.append(cur)
            cur = ''
        elif e.tag == W('p') and (out or cur):
            out.append(cur)
            cur = ''
    out.append(cur)
    return [x for x in out] if any(out) else ['']


def write_cell(tc, lines, rid=None):
    """Ghi lại ô thành 1 đoạn: run + br giữa các dòng. '{LINK}' trong dòng → hyperlink quy tắc chung."""
    ps = tc.findall(W('p'))
    p = ps[0]
    for x in ps[1:]:
        tc.remove(x)
    r0 = p.find('.//' + W('r'))
    rpr = copy.deepcopy(r0.find(W('rPr'))) if r0 is not None and r0.find(W('rPr')) is not None else None
    if rpr is None:  # ô trống: lấy rPr của dấu đoạn
        ppr = p.find(W('pPr'))
        if ppr is not None and ppr.find(W('rPr')) is not None:
            rpr = copy.deepcopy(ppr.find(W('rPr')))
    for ch in list(p):
        if ch.tag != W('pPr'):
            p.remove(ch)
    for i, line in enumerate(lines):
        if i:
            br = _el('r')
            if rpr is not None:
                br.append(copy.deepcopy(rpr))
            br.append(_el('br'))
            p.append(br)
        parts = line.split('{LINK}')
        for k, part in enumerate(parts):
            if k:
                hl = _el('hyperlink')
                hl.set(R_NS + 'id', rid)
                lrpr = copy.deepcopy(rpr) if rpr is not None else _el('rPr')
                col = _el('color')
                col.set(W('val'), '1155cc')
                u = _el('u')
                u.set(W('val'), 'single')
                lrpr.append(col)
                lrpr.append(u)
                hl.append(make_run(LINK_TEXT, lrpr))
                p.append(hl)
            if part:
                p.append(make_run(part, rpr))


def rows(tbl):
    return tbl.findall(W('tr'))


def kv_row(tbl, key):
    for tr in rows(tbl):
        cs = cells(tr)
        if cs and txt(cs[0]).strip() == key:
            return cs[1]
    raise KeyError(key)


def kv_set(tbl, key, text):
    write_cell(kv_row(tbl, key), text.split('\n'))


def kv_get(tbl, key):
    return cell_lines(kv_row(tbl, key))


def find_row(tbl, col, regex):
    for tr in rows(tbl)[1:]:
        cs = cells(tr)
        if len(cs) > col and re.search(regex, txt(cs[col])):
            return tr
    raise KeyError(regex)


def set_col(tbl, col, regex, new, name_col=1):
    tr = find_row(tbl, name_col, regex)
    write_cell(cells(tr)[col], [new])


def header_index(tbl, name):
    for i, tc in enumerate(cells(rows(tbl)[0])):
        if txt(tc).strip() == name:
            return i
    raise KeyError(name)


def renumber_stt(tbl):
    for i, tr in enumerate(rows(tbl)[1:], 1):
        write_cell(cells(tr)[0], [str(i)])


def delete_row(tbl, regex, col=1):
    tbl.remove(find_row(tbl, col, regex))
    renumber_stt(tbl)


def clone_row_after(tbl, ref_regex, values, col=1):
    ref = find_row(tbl, col, ref_regex)
    new = strip_ids(copy.deepcopy(ref))
    ref.addnext(new)
    for tc, v in zip(cells(new), values):
        if v is not None:
            write_cell(tc, v if isinstance(v, list) else v.split('\n'))
    renumber_stt(tbl)
    return new


def add_err_line(tbl, event_regex, rid):
    """Event Lưu/Duyệt/Từ chối/Xóa: thêm câu lỗi chuẩn vào cuối khối During (tạo During nếu chưa có)."""
    tc = cells(find_row(tbl, 1, event_regex))[3]
    lines = [l for l in cell_lines(tc) if 'không thực hiện bước After' not in l]
    line = ERR_LINE
    if 'During:' in lines:
        i = lines.index('After:') if 'After:' in lines else len(lines)
        lines.insert(i, line)
    else:
        i = lines.index('After:') if 'After:' in lines else len(lines)
        lines[i:i] = ['During:', line]
    write_cell(tc, lines, rid)


# ------------------------------------------------------------------ mục 2.x

def section(doc, heading_regex):
    """(heading, [phần tử thuộc mục]) — mục Heading3 khớp regex tới heading cấp ≤3 kế tiếp."""
    its = items(doc)
    for i, e in enumerate(its):
        if e.tag == W('p') and style_of(e) == 'Heading3' and re.search(heading_regex, txt(e)):
            out = []
            for f in its[i + 1:]:
                if f.tag == W('p') and style_of(f) in ('Heading1', 'Heading2', 'Heading3'):
                    break
                out.append(f)
            return e, out
    raise KeyError(heading_regex)


def sec_par(sec, regex):
    for e in sec[1]:
        if e.tag == W('p') and re.search(regex, txt(e)):
            return e
    raise KeyError(regex)


def sec_tables(sec):
    return [e for e in sec[1] if e.tag == W('tbl')]


def sec_kv(sec):
    for t in sec_tables(sec):
        if txt(cells(rows(t)[0])[0]).strip() == 'Mục':
            return t
    raise KeyError('bảng Mục | Nội dung')


def sec_ui(sec):
    for t in sec_tables(sec):
        if 'Tên đối tượng' in [txt(c).strip() for c in cells(rows(t)[0])]:
            return t
    raise KeyError('bảng mô tả giao diện')


def sec_ev(sec):
    for t in sec_tables(sec):
        if 'Loại event' in [txt(c).strip() for c in cells(rows(t)[0])]:
            return t
    raise KeyError('bảng event')


def is_sub(e):
    return e.tag == W('p') and not style_of(e) and re.match(r'^\d+\.\d+\.\d+ ', txt(e))


def renumber_subheadings(doc):
    """Đánh lại 2.x.1..2.x.n liên tục trong từng mục và in đậm đồng loạt."""
    cur, k = None, 0
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading3':
            m = re.match(r'^(\d+\.\d+)\s', txt(e))
            cur, k = (m.group(1) if m else None), 0
        elif cur and is_sub(e):
            k += 1
            title = re.sub(r'^\d+\.\d+\.\d+\s+', '', txt(e))
            new = '%s.%d %s' % (cur, k, title)
            if new != txt(e):
                log('Đánh lại mục con: %s → %s' % (txt(e), new))
                set_runs_text(e, new)
            set_bold(e, True)


def renumber_figures(doc):
    n = 0
    for e in items(doc):
        if e.tag == W('p') and re.match(r'^Hình \d+:', txt(e)):
            n += 1
            old = txt(e)
            new = re.sub(r'^Hình \d+:', 'Hình %d:' % n, old)
            if new != old:
                for t in e.iter(W('t')):
                    if t.text and re.match(r'^Hình \d+:', t.text):
                        t.text = re.sub(r'^Hình \d+:', 'Hình %d:' % n, t.text)
                        break
    return n


# ------------------------------------------------------------------ ảnh

def max_docpr(doc):
    return max([int(e.get('id')) for e in doc.element.body.iter(WP_NS + 'docPr')] + [0])


def set_image(doc, img_par, png_path):
    """Thay ảnh của đoạn bằng file PNG mới, giữ bề rộng khung, tính lại chiều cao, bỏ quan hệ ảnh cũ."""
    from PIL import Image
    blip = next(img_par.iter(A_NS + 'blip'))
    old = blip.get(R_NS + 'embed')
    rid, _ = doc.part.get_or_add_image(png_path)
    blip.set(R_NS + 'embed', rid)
    w, h = Image.open(png_path).size
    ext = next(img_par.iter(WP_NS + 'extent'))
    cx = int(ext.get('cx'))
    cy = int(cx * h / w)
    ext.set('cy', str(cy))
    for x in img_par.iter(A_NS + 'ext'):
        if x.get('cx'):
            x.set('cx', str(cx))
            x.set('cy', str(cy))
    if old != rid and not any(b.get(R_NS + 'embed') == old for b in doc.element.body.iter(A_NS + 'blip')):
        doc.part.drop_rel(old)


def remove_usecase(doc, sec):
    """Bỏ mục con 'Biểu đồ Usecase' + đoạn ảnh + chú thích của 1 mục 2.x."""
    els = sec[1]
    for i, e in enumerate(els):
        if is_sub(e) and 'Biểu đồ Usecase' in txt(e):
            img, cap = els[i + 1], els[i + 2]
            assert list(img.iter(A_NS + 'blip')) and txt(cap).startswith('Hình '), 'khối usecase lạ'
            rid = next(img.iter(A_NS + 'blip')).get(R_NS + 'embed')
            for x in (e, img, cap):
                x.getparent().remove(x)
            if not any(b.get(R_NS + 'embed') == rid for b in doc.element.body.iter(A_NS + 'blip')):
                doc.part.drop_rel(rid)
            log('Bỏ sơ đồ Use Case của mục: ' + txt(sec[0]))
            return
    raise KeyError('mục không có Biểu đồ Usecase')


def usecase_block(sec):
    els = sec[1]
    for i, e in enumerate(els):
        if is_sub(e) and 'Biểu đồ Usecase' in txt(e):
            return e, els[i + 1], els[i + 2]
    return None


def add_usecase(doc, sec, tpl_sec, png_path, caption):
    """Chèn khối 'Biểu đồ Usecase' (nhân bản từ mục mẫu tpl_sec) lên đầu mục sec."""
    sub, img, cap = [strip_ids(copy.deepcopy(x)) for x in usecase_block(tpl_sec)]
    first = sec[1][0]
    for x in (sub, img, cap):
        first.addprevious(x)
    set_runs_text(sub, '0.0.0 Biểu đồ Usecase')  # số đánh lại ở renumber_subheadings
    nid = max_docpr(doc) + 1
    for dp in img.iter(WP_NS + 'docPr'):
        dp.set('id', str(nid))
        dp.set('name', 'Usecase %d' % nid)
    for dp in img.iter('{http://schemas.openxmlformats.org/drawingml/2006/picture}cNvPr'):
        dp.set('id', '0')
        dp.set('name', 'usecase_%d.png' % nid)
    set_image(doc, img, png_path)
    set_runs_text(cap, 'Hình 0: ' + caption)
    log('Thêm sơ đồ Use Case cho mục: ' + txt(sec[0]))


def draw_usecase_qg(out_path, actor_name, code, name, group, target_w=1700):
    """Sơ đồ Use Case 1 chức năng theo đúng khổ ảnh của mẫu quốc gia (1700×540, chữ to):
    chỉ actor + 1 use case, không include/extend. Dùng lại hàm vẽ của srs_uml_render
    (draw_usecase gốc vẽ khung 1350×240 nên chèn vào khổ 6,2 inch chữ rất nhỏ)."""
    sys.path.insert(0, os.path.join(LIB_DIR, '..', '..', '..', '.claude', 'skills', 'srs-documenter', 'assets'))
    import srs_uml_render as U
    from PIL import Image, ImageDraw
    S = U.S
    W, H = 850 * S, 270 * S
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    cy = H / 2
    ax, ay = U._actor(d, int(W * 0.17), int(cy - 70 * S), actor_name, U._f(U.F_BOLD, 15), scale=1.15)
    left, _ = U._usecase(d, int(W * 0.64), cy, int(W * 0.27), int(H * 0.27), '%s %s' % (code, name), group,
                         U._f(U.F_REG, 17))
    d.line([(ax + int(6 * S), ay), (left - int(4 * S), cy)], fill=(148, 163, 184), width=max(2, int(1.4 * S)))
    return U._finish(img, out_path, target_w, kind='usecase')


# ------------------------------------------------------------------ heading / bảng mới

def clone_heading(src_heading, text, after):
    h = strip_ids(copy.deepcopy(src_heading))
    for bs in h.iter(W('bookmarkStart')):
        bs.set(W('name'), '_heading=h.formqg' + re.sub(r'\W', '', text.split(':')[0].split('.')[0])[:20])
        bs.set(W('id'), str(90000 + len(text)))
    for be in h.iter(W('bookmarkEnd')):
        be.set(W('id'), str(90000 + len(text)))
    set_runs_text(h, text)
    after.addnext(h)
    return h


def new_table_like(tpl_tbl, after, header, data_rows, widths_twips):
    """Bảng mới nhân bản khuôn tpl_tbl (cùng số cột), đặt lại độ rộng cột."""
    tbl = strip_ids(copy.deepcopy(tpl_tbl))
    trs = rows(tbl)
    hdr, body = trs[0], trs[1]
    for tr in trs:
        tbl.remove(tr)
    grid = tbl.find(W('tblGrid'))
    for gc, wd in zip(grid.findall(W('gridCol')), widths_twips):
        gc.set(W('w'), str(wd))

    def fill(tr, vals):
        for tc, v, wd in zip(cells(tr), vals, widths_twips):
            tcpr = tc.find(W('tcPr'))
            if tcpr is not None and tcpr.find(W('tcW')) is not None:
                tcpr.find(W('tcW')).set(W('w'), str(wd))
                tcpr.find(W('tcW')).set(W('type'), 'dxa')
            write_cell(tc, v.split('\n'))
        return tr
    tbl.append(fill(copy.deepcopy(hdr), header))
    for r in data_rows:
        tbl.append(fill(copy.deepcopy(body), r))
    after.addnext(tbl)
    return tbl


# ------------------------------------------------------------------ Word thật (mục lục, số trang, PDF)

def word_finalize(docx_path, pdf_path=None):
    ps1 = os.path.join(LIB_DIR, 'word_finalize.ps1')
    args = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps1, '-Docx', os.path.abspath(docx_path)]
    if pdf_path:
        args += ['-Pdf', os.path.abspath(pdf_path)]
    r = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(r.stdout.strip())
    d, b = os.path.split(os.path.abspath(docx_path))
    lock = os.path.join(d, '~$' + b[2:])  # file khoá Word bỏ lại khi tiến trình bị dọn
    if os.path.exists(lock):
        os.remove(lock)
    if r.returncode:
        raise RuntimeError(r.stderr)

# -*- coding: utf-8 -*-
"""Cập nhật phần Tùy chỉnh cột trong HDSD tải từ Drive:
   1) thay ảnh cửa sổ (đoạn ảnh ngay trên chú thích "Hình N: Cửa sổ Tùy chỉnh cột…") bằng ảnh mới;
   2) chèn bước/câu về 2 nút Chọn tất cả / Bỏ chọn hết, đánh lại số Bước phía sau.
python3 edit.py <id> [<id>…]   -> out/<id>.docx
"""
import copy, io, json, os, re, sys, zipfile
from lxml import etree
from PIL import Image

S = os.path.dirname(os.path.abspath(__file__))
ICONS = '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/catalog-docs-v2/icons/'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture'}
W = '{%s}' % NS['w']
R = '{%s}' % NS['r']
RELNS = 'http://schemas.openxmlformats.org/package/2006/relationships'
IMGREL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'
CAP_RE = re.compile(r'^\s*Hình\s*\d+\s*[:.]\s*Cửa sổ\s*(Tùy|Tuỳ|Tuy)\s*chỉnh cột', re.I)
MAP = json.load(open(S + '/map.json'))


def text(p):
    return ''.join(t.text or '' for t in p.iter(W + 't'))


def embeds(p):
    return p.findall('.//a:blip', NS)


def is_heading(p):
    st = p.find('w:pPr/w:pStyle', NS)
    sv = st.get(W + 'val') if st is not None else ''
    t = text(p).strip()
    return bool(re.search(r'(?i)heading|^\d$', sv)) or bool(re.match(r'^(PHẦN\s+\d+|\d+(\.\d+)*\.\s+\S)', t))


class Doc:
    def __init__(self, path):
        self.z = zipfile.ZipFile(path)
        self.files = {n: self.z.read(n) for n in self.z.namelist()}
        self.doc = etree.fromstring(self.files['word/document.xml'])
        self.rels = etree.fromstring(self.files['word/_rels/document.xml.rels'])
        self.body = self.doc.find('w:body', NS)
        ids = [int(x) for x in self.doc.xpath('//wp:docPr/@id', namespaces=NS) if x.isdigit()]
        self.next_docpr = max(ids + [1000]) + 1
        self.media_n = 0

    def add_image(self, png_bytes):
        self.media_n += 1
        name = 'media/colcfg_%d.png' % self.media_n
        while 'word/' + name in self.files:
            self.media_n += 1
            name = 'media/colcfg_%d.png' % self.media_n
        self.files['word/' + name] = png_bytes
        rid_n = max(int(x.get('Id')[3:]) for x in self.rels if x.get('Id', '').startswith('rId') and x.get('Id')[3:].isdigit()) + 1
        rid = 'rId%d' % rid_n
        el = etree.SubElement(self.rels, '{%s}Relationship' % RELNS)
        el.set('Id', rid); el.set('Type', IMGREL); el.set('Target', name)
        ct = self.files['[Content_Types].xml'].decode()
        if 'Extension="png"' not in ct:
            ct = ct.replace('<Default ', '<Default Extension="png" ContentType="image/png"/><Default ', 1)
            self.files['[Content_Types].xml'] = ct.encode()
        return rid

    def set_blip(self, p, png_path, keep='cx'):
        """Đổi ảnh LỚN NHẤT trong p (đoạn có thể chứa cả icon lẫn ảnh màn hình): giữ chiều rộng (cx)
        hoặc chiều cao (cy), tính lại chiều kia theo tỉ lệ ảnh mới."""
        data = open(png_path, 'rb').read()
        w, h = Image.open(io.BytesIO(data)).size
        rid = self.add_image(data)
        drs = p.findall('.//w:drawing', NS)
        dr = max(drs, key=lambda x: int(x.find('.//wp:extent', NS).get('cx')))
        dr.find('.//a:blip', NS).set(R + 'embed', rid)
        for ext in dr.xpath('.//wp:extent | .//a:xfrm/a:ext', namespaces=NS):
            cx, cy = int(ext.get('cx')), int(ext.get('cy'))
            if keep == 'cx':
                ext.set('cy', str(int(cx * h / w)))
            else:
                ext.set('cx', str(int(cy * w / h)))
        for dp in dr.xpath('.//wp:docPr', namespaces=NS):
            dp.set('id', str(self.next_docpr)); self.next_docpr += 1
        return rid

    def save(self, out):
        self.files['word/document.xml'] = etree.tostring(self.doc, xml_declaration=True, encoding='UTF-8', standalone=True)
        self.files['word/_rels/document.xml.rels'] = etree.tostring(self.rels, xml_declaration=True, encoding='UTF-8', standalone=True)
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zo:
            for n in self.z.namelist():
                zo.writestr(n, self.files[n])
            for n in self.files:
                if n not in self.z.namelist():
                    zo.writestr(n, self.files[n])


def set_runs_text(p, segments, d):
    """Viết lại nội dung đoạn p theo segments: chuỗi hoặc ('img', path). Giữ pPr + rPr của run chữ đầu,
    run ảnh nhân bản từ run ảnh đầu tiên của p (nếu có)."""
    runs = p.findall('w:r', NS)
    txt_run = next((r for r in runs if r.find('w:t', NS) is not None), None)
    img_run = next((r for r in runs if r.find('.//a:blip', NS) is not None), None)
    for r in list(p):
        if r.tag != W + 'pPr':
            p.remove(r)
    for seg in segments:
        if isinstance(seg, tuple):
            nr = copy.deepcopy(img_run)
            d.set_blip(nr, seg[1], keep='cy')
        else:
            nr = copy.deepcopy(txt_run) if txt_run is not None else etree.Element(W + 'r')
            for c in list(nr):
                if c.tag != W + 'rPr':
                    nr.remove(c)
            t = etree.SubElement(nr, W + 't'); t.text = seg
            t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        p.append(nr)


def renumber(p, delta=1):
    """'Bước N' -> 'Bước N+delta' trong w:t đầu tiên chứa nó."""
    for t in p.iter(W + 't'):
        if t.text and re.search(r'Bước\s*\d+', t.text):
            t.text = re.sub(r'Bước\s*(\d+)', lambda m: 'Bước %d' % (int(m.group(1)) + delta), t.text, count=1)
            return True
    return False


def process(id):
    d = Doc(S + '/orig/%s.docx' % id)
    route = MAP[id]
    shot = S + '/shots/' + route.replace('/', '__') + '.png'
    ps = list(d.body.iter(W + 'p'))
    caps = [i for i, p in enumerate(ps) if i > 1 and CAP_RE.match(text(p)) and (embeds(ps[i - 1]) or embeds(ps[i - 2]))]
    if not caps:
        return None, 'KHÔNG THẤY CHÚ THÍCH'
    c = caps[-1]
    m = next(k for k in (c - 1, c - 2, c) if embeds(ps[k]))
    d.set_blip(ps[m], shot, keep='cx')

    # phạm vi phần: từ heading trước ảnh tới heading sau chú thích
    s = max([k for k in range(0, m) if is_heading(ps[k])] or [m - 1])
    e = next((k for k in range(c + 1, len(ps)) if is_heading(ps[k])), min(len(ps), c + 12))
    sec = [k for k in range(s + 1, e) if k not in (m, c)]

    gon = any(re.match(r'\s*Bước\s*\d+\s*:\s*Bấm', text(ps[k])) and embeds(ps[k]) for k in sec)
    tich = next((k for k in sec if re.search(r'(?i)\btích', text(ps[k]))), None)
    if gon:
        # Bước 2: Tích… -> chèn Bước 3 (icon Chọn tất cả) + dòng Hoặc (icon Bỏ chọn hết)
        luu = next(k for k in sec if re.match(r'\s*Bước\s*\d+\s*:\s*Bấm', text(ps[k])) and embeds(ps[k]))
        hoac = next((k for k in sec if k > luu and text(ps[k]).strip().startswith('Hoặc') and embeds(ps[k])), None)
        for k in sec:
            if k > tich and re.match(r'\s*Bước\s*\d+', text(ps[k])):
                renumber(ps[k])
        n = int(re.search(r'Bước\s*(\d+)', text(ps[tich])).group(1)) + 1
        step = copy.deepcopy(ps[luu])
        set_runs_text(step, ['Bước %d: Bấm ' % n, ('img', ICONS + 'btn_chontatca.png'), ' để hiện tất cả các cột.'], d)
        ps[tich].addnext(step)
        if hoac is not None:
            sub = copy.deepcopy(ps[hoac])
            set_runs_text(sub, ['Hoặc bấm ', ('img', ICONS + 'btn_bochonhet.png'), ' để ẩn tất cả các cột (trừ các cột bắt buộc).'], d)
            step.addnext(sub)
        return d, 'GỌN: thay ảnh + chèn Bước %d' % n

    # Khuôn cũ: câu chữ thường, cùng kiểu đoạn với đoạn mô tả
    after = tich
    if after is None:
        nxt = [k for k in sec if k > c and text(ps[k]).strip()]
        after = nxt[0] if nxt else c
    tpl_k = after if after != c else max([k for k in sec if k < m and text(ps[k]).strip()] or [c])
    newp = copy.deepcopy(ps[tpl_k])
    t0 = text(ps[tpl_k])
    msg = ('Bấm “Chọn tất cả” để hiện tất cả các cột, bấm “Bỏ chọn hết” để ẩn tất cả các cột '
           '(các cột có biểu tượng ổ khóa vẫn luôn hiển thị). Cuối cửa sổ hiển thị số cột đang chọn.')
    mb = re.match(r'\s*Bước\s*(\d+)\s*:', t0)
    if mb and after == tich:
        for k in sec:
            if k > tich and re.match(r'\s*Bước\s*\d+', text(ps[k])):
                renumber(ps[k])
        msg = 'Bước %d: %s' % (int(mb.group(1)) + 1, msg)
    for dr in newp.findall('.//w:drawing', NS):
        dr.getparent().getparent().remove(dr.getparent())
    set_runs_text(newp, [msg], d)
    ps[after].addnext(newp)
    return d, 'CŨ: thay ảnh + chèn câu sau đoạn %d «%s»' % (after, text(ps[after])[:60])


if __name__ == '__main__':
    os.makedirs(S + '/out', exist_ok=True)
    for id in sys.argv[1:] or MAP:
        try:
            d, msg = process(id)
            if d is not None:
                d.save(S + '/out/%s.docx' % id)
        except Exception as ex:
            import traceback; traceback.print_exc()
            msg = 'LỖI ' + repr(ex)
        print(id, MAP[id], msg)

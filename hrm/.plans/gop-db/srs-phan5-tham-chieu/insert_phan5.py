# -*- coding: utf-8 -*-
"""Chèn "Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu danh mục" vào cuối SRS danh mục.

Khuôn theo bản QA "SRS - Danh mục quốc gia" (bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn).
Làm trên BẢN ĐANG NẰM TRÊN DRIVE (drive/) để giữ nguyên phần tester sửa tay — không sinh lại từ generator.
Heading + bảng nhân bản từ chính Phần 4 của file → cùng style, font, màu.

    python3 insert_phan5.py            # drive/*.docx + refs/<slug>.json -> out/*.docx
"""
import copy
import json
import os
import sys

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Inches

HERE = os.path.dirname(os.path.abspath(__file__))
TITLE = 'Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu danh mục'
HEAD = ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn']
WIDTHS = [0.65, 1.2, 2.45, 2.2]          # inch — tổng 6.5 như bảng Phần 4


def txt(el):
    return ''.join(t.text or '' for t in el.iter(qn('w:t'))).strip()


def set_cell_text(tc, text):
    """Giữ định dạng run/đoạn đầu tiên của ô, thay chữ (xuống dòng = đoạn mới)."""
    ps = tc.findall(qn('w:p'))
    tpl = ps[0]
    for p in ps[1:]:
        tc.remove(p)
    runs = tpl.findall(qn('w:r'))
    rpr = runs[0].find(qn('w:rPr')) if runs else None
    for r in list(tpl):
        if r.tag != qn('w:pPr'):
            tpl.remove(r)
    lines = str(text).split('\n')
    for i, line in enumerate(lines):
        p = tpl if i == 0 else copy.deepcopy(tpl)
        if i:
            for r in list(p):
                if r.tag != qn('w:pPr'):
                    p.remove(r)
            tc.append(p)
        r = p.makeelement(qn('w:r'), {})
        if rpr is not None:
            r.append(copy.deepcopy(rpr))
        t = r.makeelement(qn('w:t'), {qn('xml:space') if False else '{http://www.w3.org/XML/1998/namespace}space': 'preserve'})
        t.text = line
        r.append(t)
        p.append(r)


def set_width(tc, inch):
    tcPr = tc.find(qn('w:tcPr'))
    if tcPr is None:
        tcPr = tc.makeelement(qn('w:tcPr'), {})
        tc.insert(0, tcPr)
    w = tcPr.find(qn('w:tcW'))
    if w is None:
        w = tcPr.makeelement(qn('w:tcW'), {})
        tcPr.insert(0, w)
    w.set(qn('w:w'), str(int(inch * 1440)))
    w.set(qn('w:type'), 'dxa')


def build(src, rows, dst):
    d = Document(src)
    body = d.element.body
    kids = list(body.iterchildren())
    i4 = max(i for i, c in enumerate(kids) if c.tag == qn('w:p') and txt(c).startswith('Phần 4'))
    if any(c.tag == qn('w:p') and txt(c).startswith('Phần 5') for c in kids):
        raise RuntimeError('%s đã có Phần 5' % src)
    h4 = kids[i4]
    t4 = next(c for c in kids[i4:] if c.tag == qn('w:tbl'))
    if [txt(tc) for tc in t4.find(qn('w:tr')).findall(qn('w:tc'))] != \
            ['STT', 'Mã quy tắc', 'Tên quy tắc', 'Mô tả', 'Phạm vi áp dụng']:
        raise RuntimeError('%s: bảng Phần 4 không đúng khuôn' % src)

    # Heading
    h5 = copy.deepcopy(h4)
    runs = h5.findall(qn('w:r'))
    for r in runs[1:]:
        h5.remove(r)
    for t in runs[0].findall(qn('w:t')):
        runs[0].remove(t)
    t = runs[0].makeelement(qn('w:t'), {})
    t.text = TITLE
    runs[0].append(t)
    for b in h5.findall(qn('w:bookmarkStart')) + h5.findall(qn('w:bookmarkEnd')):
        h5.remove(b)

    # Bảng: nhân bản bảng Phần 4, bỏ cột cuối, giữ 1 dòng tiêu đề + 1 dòng mẫu
    t5 = copy.deepcopy(t4)
    grid = t5.find(qn('w:tblGrid'))
    gcols = grid.findall(qn('w:gridCol'))
    grid.remove(gcols[-1])
    for g, w in zip(grid.findall(qn('w:gridCol')), WIDTHS):
        g.set(qn('w:w'), str(int(w * 1440)))
    trs = t5.findall(qn('w:tr'))
    head_tr, body_tpl = trs[0], copy.deepcopy(trs[1])
    for tr in trs[1:]:
        t5.remove(tr)
    for tr in (head_tr, body_tpl):
        tcs = tr.findall(qn('w:tc'))
        tr.remove(tcs[-1])
    for tc, text, w in zip(head_tr.findall(qn('w:tc')), HEAD, WIDTHS):
        set_cell_text(tc, text)
        set_width(tc, w)
    for k, row in enumerate(rows, 1):
        tr = copy.deepcopy(body_tpl)
        vals = [k, row['nhom'], row['man_hinh'], row['duong_dan']]
        for tc, text, w in zip(tr.findall(qn('w:tc')), vals, WIDTHS):
            set_cell_text(tc, text)
            set_width(tc, w)
        t5.append(tr)

    # Bảng dài sang trang: lặp dòng tiêu đề, không cắt ngang 1 dòng
    for k, tr in enumerate(t5.findall(qn('w:tr'))):
        trPr = tr.find(qn('w:trPr'))
        if trPr is None:
            trPr = tr.makeelement(qn('w:trPr'), {})
            tr.insert(0, trPr)
        # Bản qua Google Docs gắn sẵn <w:tblHeader w:val="0"/> cho MỌI dòng → phải xoá rồi gắn lại
        for tag in ('w:tblHeader', 'w:cantSplit'):
            for el in trPr.findall(qn(tag)):
                trPr.remove(el)
        for tag in (['w:tblHeader'] if k == 0 else []) + ['w:cantSplit']:
            trPr.append(trPr.makeelement(qn(tag), {}))

    # Chèn ngay sau bảng Phần 4 (+ đoạn trống sau nó nếu có), trước sectPr
    anchor = t4
    nxt = anchor.getnext()
    if nxt is not None and nxt.tag == qn('w:p') and not txt(nxt):
        anchor = nxt
    anchor.addnext(h5)
    h5.addnext(t5)
    d.save(dst)


def main():
    cfg = json.load(open(os.path.join(HERE, 'targets.json'), encoding='utf-8'))
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    only = set(sys.argv[1:])
    for slug, meta in cfg.items():
        if only and slug not in only:
            continue
        ref = json.load(open(os.path.join(HERE, 'refs_final', slug + '.json'), encoding='utf-8'))
        rows = ref['rows']
        src = os.path.join(HERE, 'drive', meta['file'])
        dst = os.path.join(HERE, 'out', meta['file'])
        build(src, rows, dst)
        print('OK %-45s %2d dòng' % (meta['file'], len(rows)))


if __name__ == '__main__':
    main()

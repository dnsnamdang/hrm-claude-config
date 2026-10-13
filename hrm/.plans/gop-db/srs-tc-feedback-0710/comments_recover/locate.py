# Định vị chỗ gắn lại từng nhận xét trên bản HIỆN TẠI -> post_plan.json
import json, re, os, glob, unicodedata, sys
import docx
from docx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.abspath(os.path.join(HERE, '..', '..'))   # .plans/gop-db
W = lambda t: qn('w:' + t)


def N(s):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', s or '')).strip()


def ptext(p):
    out = []
    for x in p.iter():
        if x.tag == W('t'):
            out.append(x.text or '')
        elif x.tag in (W('br'), W('tab')):
            out.append(' ')
    return N(''.join(out))


def style(p):
    pp = p.find(W('pPr'))
    if pp is None or pp.find(W('pStyle')) is None:
        return ''
    return pp.find(W('pStyle')).get(W('val'))


def units(path):
    """Danh sách đoạn theo thứ tự tài liệu: {text, cell, heading, rowkey}"""
    d = docx.Document(path)
    out = []
    head = ''

    def walk(el, rowkey=None, celltext=None):
        nonlocal head
        for ch in el.iterchildren():
            if ch.tag == W('p'):
                t = ptext(ch)
                if style(ch).startswith('Heading') and t:
                    head = re.sub(r'^[\d.\s]+', '', t)
                out.append({'text': t, 'cell': celltext if celltext is not None else t, 'heading': head, 'rowkey': rowkey})
            elif ch.tag == W('tbl'):
                for tr in ch.findall(W('tr')):
                    tcs = tr.findall(W('tc'))
                    cells = [N(' '.join(ptext(p) for p in tc.iter(W('p')))) for tc in tcs]
                    rk = ' | '.join(cells[:2])[:120]
                    rowtext = ' '.join(cells)
                    for ci, (tc, ct) in enumerate(zip(tcs, cells)):
                        n0 = len(out)
                        walk(tc, rk, ct)
                        for u in out[n0:]:
                            u['row'] = rowtext
                            u['ci'] = ci
            elif ch.tag in (W('sdt'), W('sdtContent'), W('body')):
                walk(ch, rowkey, celltext)
    walk(d.element.body)
    return out


def occ(us, s):
    """Mọi lần xuất hiện (không phân biệt hoa thường) theo thứ tự: [(unit_idx)]"""
    s2 = s.casefold()
    res = []
    for i, u in enumerate(us):
        t = u['text'].casefold()
        start = 0
        while s2 and True:
            k = t.find(s2, start)
            if k < 0:
                break
            res.append(i)
            start = k + 1
    return res


def find_old(us, a):
    """tìm anchor trong bản cũ: theo đoạn, rồi theo ô (anchor nhiều dòng)"""
    o = occ(us, a)
    if o:
        return o
    a2 = a.casefold()
    return [i for i, u in enumerate(us) if a2 and a2 in u['cell'].casefold() and (i == 0 or us[i - 1]['cell'] != u['cell'])]


def candidates(fname, fid):
    c = [os.path.join(G, 'srs-phan5-tham-chieu/drive2', fname),
         os.path.join(G, 'srs-tc-feedback-0710/drive', fid + '.docx')]
    c += glob.glob(os.path.join(G, 'catalog-docs-v2/*/out', fname))
    for sub in ('geo-catalogs-docs', 'finance-account-catalog', 'device-error-catalog-docs', 'finance-currency-catalog',
                'srs-phan5-tham-chieu/ref', 'catalog-docs-v2/templates'):
        c.append(os.path.join(G, sub, fname))
    return [p for p in c if os.path.exists(p)]


def main():
    plan = json.load(open(os.path.join(HERE, 'plan.json')))
    cache = {}
    out = []
    for c in plan:
        fid, fname, a = c['id'], c['file'], N(c['anchor'])
        if fid not in cache:
            cache[fid] = {'cur': units(os.path.join(HERE, 'cur', fid + '.docx')),
                          'old': [(p, units(p)) for p in candidates(fname, fid)]}
        cur, olds = cache[fid]['cur'], cache[fid]['old']
        oc = occ(cur, a) if a else []
        ctx = None
        for p, ou in olds:
            fo = find_old(ou, a) if a else []
            if len(fo) == 1:
                ctx = ou[fo[0]]
                break
        if ctx is None:
            for p, ou in olds:
                fo = find_old(ou, a) if a else []
                if fo:
                    ctx = dict(ou[fo[0]], ambiguous_old=len(fo))
                    break
        target, idx, how = None, None, None
        if len(oc) == 1:
            target, idx, how = a, 1, 'chính xác'
        elif len(oc) > 1:
            pick = None
            if ctx:
                for n, ui in enumerate(oc):
                    u = cur[ui]
                    if u['heading'] == ctx['heading'] and (ctx['rowkey'] is None or u['rowkey'] == ctx['rowkey']):
                        pick = n
                        break
                if pick is None:
                    for n, ui in enumerate(oc):
                        if cur[ui]['heading'] == ctx['heading']:
                            pick = n
                            break
            if pick is not None and not (ctx or {}).get('ambiguous_old'):
                target, idx, how = a, pick + 1, 'chính xác (theo mục/dòng bảng)'
            else:
                target, idx, how = a, (pick or 0) + 1, 'gần đúng (đoạn trùng nhiều chỗ)'
        if target is None and ctx:
            # đoạn đã đổi: gắn vào ô tên của đúng dòng bảng, hoặc tiêu đề mục
            row = [i for i, u in enumerate(cur) if u['heading'] == ctx['heading'] and ctx['rowkey'] and u['rowkey'] == ctx['rowkey']]
            if not row and ctx['rowkey']:
                name = ctx['rowkey'].split(' | ')[-1]
                row = [i for i, u in enumerate(cur) if u['heading'] == ctx['heading'] and u['rowkey'] and u['rowkey'].split(' | ')[-1] == name]
            cand = None
            if row:
                for i in row:
                    if cur[i]['text'] and len(cur[i]['text']) >= 2:
                        cand = cur[i]['text'][:60]
                        break
                how = 'dòng bảng chứa đoạn cũ'
            if not cand:
                h = [i for i, u in enumerate(cur) if u['heading'] == ctx['heading'] and u['text'] and re.sub(r'^[\d.\s]+', '', u['text']) == ctx['heading']]
                if h:
                    cand = cur[h[0]]['text'][:60]
                    how = 'tiêu đề mục chứa đoạn cũ'
            if cand:
                o2 = occ(cur, cand)
                if o2:
                    first_row = row[0] if row else None
                    want = first_row if first_row is not None else h[0]
                    n = o2.index(want) + 1 if want in o2 else 1
                    target, idx = cand, n
        if target is None:
            target, idx, how = None, None, 'không xác định được vị trí'
        out.append({**c, 'target': target, 'occ_index': idx, 'occ_total': len(occ(cur, target)) if target else 0,
                    'how': how, 'old_heading': (ctx or {}).get('heading')})
    json.dump(out, open(os.path.join(HERE, 'post_plan.json'), 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter(x['how'] for x in out))
    for f in sorted(set(x['file'] for x in out)):
        print(f, Counter(x['how'] for x in out if x['file'] == f))


if __name__ == '__main__':
    main()

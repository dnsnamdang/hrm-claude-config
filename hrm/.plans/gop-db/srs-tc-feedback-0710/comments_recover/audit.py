# Đánh giá vị trí đã gắn + tìm vị trí gốc + đề xuất chuỗi bôi đen DUY NHẤT (khớp kiểu Docs: bỏ dấu, không phân biệt hoa thường)
import json, os, re, sys, unicodedata, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from locate import units, candidates, N

H = os.path.dirname(os.path.abspath(__file__))


def S(s):
    s = unicodedata.normalize('NFD', (s or '').casefold())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').replace('đ', 'd')
    return re.sub(r'\s+', ' ', s)


def docs_hits(us, target):
    """Các lần khớp kiểu Docs theo thứ tự: [(unit_idx, char_pos)]"""
    t = S(target)
    out = []
    for i, u in enumerate(us):
        x = S(u['text'])
        st = 0
        while t:
            k = x.find(t, st)
            if k < 0:
                break
            out.append((i, k))
            st = k + 1
    return out


def unique_span(us, ui, start, length):
    """Mở rộng [start,start+length) trong đoạn ui cho tới khi chuỗi là duy nhất trong tài liệu (kiểu Docs)."""
    txt = us[ui]['text']
    a, b = start, start + length
    for _ in range(200):
        cand = txt[a:b].strip()
        if cand and len(docs_hits(us, cand)) == 1:
            return cand
        # mở rộng sang phải trước, rồi trái, theo từ
        if b < len(txt):
            nb = txt.find(' ', b + 1)
            b = len(txt) if nb < 0 else nb
        elif a > 0:
            na = txt.rfind(' ', 0, a - 1)
            a = 0 if na < 0 else na + 1
        else:
            break
    cand = txt.strip()
    return cand if cand and len(docs_hits(us, cand)) == 1 else None


def old_occurrences(fname, fid, anchor):
    res = []
    for p in candidates(fname, fid):
        ou = units(p)
        for (ui, pos) in docs_hits(ou, anchor):
            u = ou[ui]
            res.append({'doc': os.path.basename(os.path.dirname(p)) + '/' + os.path.basename(p), 'heading': u['heading'],
                        'rowkey': u['rowkey'], 'para': u['text'], 'cell': u['cell']})
        if res:
            return res   # bản cũ đầu tiên có đoạn này (mới nhất)
        # đoạn bôi cả dòng bảng (nhiều ô)
        seen = set()
        for ui, u in enumerate(ou):
            r = u.get('row')
            if r and S(anchor) in S(r) and r not in seen:
                seen.add(r)
                res.append({'doc': os.path.basename(os.path.dirname(p)) + '/' + os.path.basename(p), 'heading': u['heading'],
                            'rowkey': u['rowkey'], 'para': u['text'], 'cell': r, 'rowspan': True})
        if res:
            return res
    return res


def best_current(cur, occ):
    """Tìm đoạn trong bản hiện tại giống nhất với vị trí cũ (cùng mục + dòng bảng, chữ gần nhất)."""
    best, score = None, 0
    for i, u in enumerate(cur):
        if not u['text']:
            continue
        sc = 0
        if u['heading'] == occ['heading']:
            sc += 3
        if occ['rowkey'] and u['rowkey'] == occ['rowkey']:
            sc += 3
        elif occ['rowkey'] and u['rowkey'] and u['rowkey'].split(' | ')[-1] == occ['rowkey'].split(' | ')[-1]:
            sc += 2
        sc += 4 * difflib.SequenceMatcher(None, S(u['text'])[:300], S(occ['para'])[:300]).ratio()
        if sc > score:
            best, score = i, sc
    return best, round(score, 2)


def main():
    items = json.load(open(os.path.join(H, 'items_todo.json')))
    plan = {x['n']: x for x in json.load(open(os.path.join(H, 'post_plan.json')))} if False else {}
    P = {i: x for i, x in enumerate(json.load(open(os.path.join(H, 'post_plan.json'))))}
    cache = {}
    out = []
    for it in items:
        src = P[it['n']]
        cur = cache.setdefault(it['id'], units(os.path.join(H, 'cur', it['id'] + '.docx')))
        hits = docs_hits(cur, it['target'])
        landed = hits[it['k'] - 1][0] if 0 < it['k'] <= len(hits) else None
        occ = old_occurrences(it['file'], it['id'], src['anchor'])
        rec = {'n': it['n'], 'file': it['file'], 'anchor': src['anchor'], 'comment': src['posts'][0][2],
               'author': src['posts'][0][0], 'landed_para': cur[landed]['text'][:160] if landed is not None else None,
               'landed_heading': cur[landed]['heading'] if landed is not None else None,
               'old_occ': [{k: (v[:200] if isinstance(v, str) else v) for k, v in o.items()} for o in occ]}
        out.append(rec)
    json.dump(out, open(os.path.join(H, 'audit.json'), 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter(min(len(r['old_occ']), 2) for r in out))


if __name__ == '__main__':
    main()

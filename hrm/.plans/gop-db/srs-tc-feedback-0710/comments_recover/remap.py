# Tính vị trí MỚI (chuỗi bôi đen duy nhất) cho từng nhận xét + so với chỗ đã gắn -> moves.json
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from locate import units
from audit import S, docs_hits, unique_span, best_current

H = os.path.dirname(os.path.abspath(__file__))


def main():
    A = {r['n']: r for r in json.load(open(os.path.join(H, 'audit.json')))}
    C = {c['n']: c for c in json.load(open(os.path.join(H, 'choices.json')))} if os.path.exists(os.path.join(H, 'choices.json')) else {}
    items = json.load(open(os.path.join(H, 'items_todo.json')))
    cache = {}
    out = []
    for it in items:
        r = A[it['n']]
        cur = cache.setdefault(it['id'], units(os.path.join(H, 'cur', it['id'] + '.docx')))
        hits = docs_hits(cur, it['target'])
        landed = hits[it['k'] - 1][0] if 0 < it['k'] <= len(hits) else None
        anchor = r['anchor']
        ch = C.get(it['n'], {})
        tu = None
        conf = 'cao'
        if ch.get('cur_u') is not None:
            tu = ch['cur_u']
            conf = ch.get('confidence', 'vừa')
        else:
            occ = None
            if len(r['old_occ']) == 1:
                occ = r['old_occ'][0]
            elif ch.get('old_i') is not None and ch['old_i'] < len(r['old_occ']):
                occ = r['old_occ'][ch['old_i']]
                conf = ch.get('confidence', 'vừa')
            if occ:
                tu, sc = best_current(cur, occ)
                if sc < 3:
                    conf = 'thấp'
        if tu is None:
            out.append({**it, 'new_target': None, 'move': False, 'conf': 'không xác định', 'landed_u': landed})
            continue
        ptxt = cur[tu]['text']
        k = S(ptxt).find(S(anchor)) if anchor else -1
        if k >= 0:
            span = unique_span(cur, tu, k, len(anchor))
            exact = True
        else:
            e = ptxt.find(' ', 20)
            span = unique_span(cur, tu, 0, len(ptxt) if e < 0 else e)
            exact = False
        if not span and cur[tu].get('rowkey'):
            # ô có chữ trùng khắp nơi -> bôi ô khác cùng dòng bảng (ưu tiên ô mô tả = ô cuối)
            same = [i for i, u in enumerate(cur) if u.get('rowkey') == cur[tu]['rowkey'] and u['heading'] == cur[tu]['heading'] and u['text']]
            for i in sorted(same, key=lambda i: -cur[i].get('ci', 0)):
                e = cur[i]['text'].find(' ', 20)
                sp = unique_span(cur, i, 0, len(cur[i]['text']) if e < 0 else e)
                if sp:
                    span, tu, ptxt = sp, i, cur[i]['text']
                    break
        new_k = 1
        if not span:
            # câu lặp nguyên văn nhiều nơi -> dùng thứ tự lần xuất hiện (đếm kiểu Docs)
            span = anchor if k >= 0 else ptxt[:80].rsplit(' ', 1)[0] if len(ptxt) > 80 else ptxt
            hs = docs_hits(cur, span)
            pos = [j for j, (ui, _) in enumerate(hs) if ui == tu]
            if not pos:
                out.append({**it, 'new_target': None, 'move': False, 'conf': 'không định vị được', 'landed_u': landed, 'target_u': tu})
                continue
            new_k = pos[0] + 1
        new_total = len(docs_hits(cur, span))
        move = (landed != tu)
        out.append({**it, 'new_target': span, 'new_k': new_k, 'new_total': new_total, 'new_exact': exact, 'target_u': tu, 'landed_u': landed, 'move': move, 'conf': conf,
                    'target_para': ptxt[:150], 'landed_para': cur[landed]['text'][:150] if landed is not None else None})
    json.dump(out, open(os.path.join(H, 'moves.json'), 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print('cần chuyển chỗ:', sum(1 for x in out if x['move']), '/', len(out))
    print(Counter(x['conf'] for x in out))
    print(Counter((x['file'][14:34], x['move']) for x in out))


if __name__ == '__main__':
    main()

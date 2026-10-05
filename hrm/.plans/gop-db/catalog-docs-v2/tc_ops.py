"""python3 tc_ops.py <slug> [expand-only]
Dựng script Playwright sửa tab testcase của danh mục theo CFG['tc']:
  tab       tên tab (đúng như index.json)
  hdr_row   1 hàng TIÊU ĐỀ NHÓM có sẵn (vd "VII. LỊCH SỬ THAY ĐỔI") để chép định dạng cho nhóm mới
  edits     [(ref, giá trị mới)] — sửa thẳng ô CÓ SẴN, ref theo SỐ HÀNG GỐC (trước khi chèn)
  clear_k   [số hàng gốc] — hàng đã sửa → xoá trống ô K "DNS check lần 1"
  blocks    list khối chèn, số hàng theo HÀNG GỐC (script tự chèn từ dưới lên nên không lệch):
    {'after': R, 'groups': [(La Mã, tiêu đề, chỉ số TC, 'export'|'import'|[case6...])]}
        → nhóm MỚI (dòng tiêu đề nhóm + case), TC ID tự đánh TC_<chỉ số>.001…
    {'after': R, 'cases': [(TC ID, Chức năng, Priority, Tiền điều kiện, Bước, Test data, Expected)],
     'merge_from': hàng đầu của nhóm cũ}
        → case mới chèn vào CUỐI nhóm có sẵn (R = case cuối nhóm), gộp lại cột A:B từ merge_from
Ghi ra HRM/.playwright-mcp/sh_<slug>.js
"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', '_catalog_docs_lib'))
from catalog_v2 import load_cfg
from tc_gen import export_cases, import_cases, group_rows, to_tsv

slug = sys.argv[1]
cfg = load_cfg(slug)
t = cfg['tc']
ops = [{'op': 'expand'}]
# 1) sửa ô có sẵn (theo số hàng gốc) — làm TRƯỚC khi chèn
for ref, val in t.get('edits', []):
    ops.append({'op': 'paste', 'ref': ref, 'tsv': to_tsv([[val]])})
if t.get('clear_k'):
    ops.append({'op': 'clear', 'refs': ['K%d' % x for x in t['clear_k']]})
# 2) chèn từ dưới lên
summary = []
for b in sorted(t.get('blocks', []), key=lambda b: -b['after']):
    after = b['after']
    rows, hdr, merges = [], [], []
    r = after + 1
    if 'groups' in b:
        for no, title, idx, kind in b['groups']:
            cases = export_cases(cfg) if kind == 'export' else import_cases(cfg) if kind == 'import' else kind
            g = group_rows(cfg['ten'], no, title, idx, cases)
            hdr.append(r)
            if len(cases) > 1:
                merges += ['A%d:A%d' % (r + 1, r + len(cases)), 'B%d:B%d' % (r + 1, r + len(cases))]
            rows += g
            r += len(g)
    else:
        for c in b['cases']:
            rows.append(['', ''] + list(c))
        last = after + len(rows)
        merges += ['A%d:A%d' % (b['merge_from'], last), 'B%d:B%d' % (b['merge_from'], last)]
    ops.append({'op': 'insert', 'after': after, 'n': len(rows)})
    ops.append({'op': 'paste', 'ref': 'A%d' % (after + 1), 'tsv': to_tsv(rows)})
    for hr in hdr:
        ops.append({'op': 'fmt', 'src': '%d:%d' % (t['hdr_row'], t['hdr_row']), 'dst': '%d:%d' % (hr, hr)})
    for m in merges:
        ops.append({'op': 'merge', 'ref': m})
    summary.append((after, len(rows), hdr, merges))
ops.append({'op': 'shot', 'name': 'sh_%s_a.png' % slug, 'ref': 'A18'})
if len(sys.argv) > 2:
    ops = [ops[0], {'op': 'shot', 'name': 'sh_%s_x.png' % slug}]
P = {'tab': t['tab'], 'ops': ops}
tpl = open(os.path.join(H, '..', '_catalog_docs_lib', 'sheet_tpl.js')).read()
out = '/Users/manhcuong/Desktop/dns/HRM/.playwright-mcp/sh_%s.js' % slug
open(out, 'w').write(tpl.replace('__PARAMS__', json.dumps(P, ensure_ascii=False)))
print(out)
for s in summary:
    print('  chèn sau hàng %d: %d hàng, tiêu đề nhóm %s, gộp %s' % s)

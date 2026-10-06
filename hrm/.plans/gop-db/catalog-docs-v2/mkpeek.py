"""python3 mkpeek.py <slug> → .playwright-mcp/peek_run.js đọc các ô mốc (hàng chèn, ô sửa, hàng tiêu đề) để đối chiếu dump trước khi sửa."""
import json, sys
sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/_catalog_docs_lib')
from catalog_v2 import load_cfg
t = load_cfg(sys.argv[1])['tc']
refs = []
for b in t.get('blocks', []):
    refs += ['C%d' % b['after'], 'C%d' % (b['after'] + 1)]
    if b.get('merge_from'):
        refs.append('A%d' % b['merge_from'])
refs += sorted({'C%s' % ''.join(ch for ch in e[0] if ch.isdigit()) for e in t.get('edits', []) if e[0][0] != 'B'})[:12]
refs += [e[0] for e in t.get('edits', []) if e[0][0] == 'B'] + ['C%d' % t['hdr_row']]
H = '/Users/manhcuong/Desktop/dns/HRM/.playwright-mcp/'
s = open(H + 'sh_peek.js').read().replace('__TAB__', json.dumps(t['tab'].strip())).replace('__REFS__', json.dumps(refs))
open(H + 'peek_run.js', 'w').write(s)
print(refs)

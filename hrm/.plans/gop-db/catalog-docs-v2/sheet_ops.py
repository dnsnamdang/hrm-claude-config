"""python3 sheet_ops.py '<tab>' '<json ops>' → .playwright-mcp/sh_fix.js (chạy lệnh lẻ trên sheet, vd gộp lại ô bị lỗi)."""
import json, sys
tpl = open('/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/_catalog_docs_lib/sheet_tpl.js').read()
P = {'tab': sys.argv[1], 'ops': json.loads(sys.argv[2])}
open('/Users/manhcuong/Desktop/dns/HRM/.playwright-mcp/sh_fix.js', 'w').write(tpl.replace('__PARAMS__', json.dumps(P, ensure_ascii=False)))

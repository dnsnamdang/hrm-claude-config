"""Rà prefix thông báo chưa khai nhãn ở NotificationMeta::OBJECT_LABELS.

Chạy từ thư mục HRM/:  python3 .claude/skills/notification-convention/scripts/check_prefix_labels.py [đường dẫn hrm-api]
In ra mỗi prefix thiếu nhãn + file dùng nó; RỖNG = đủ. Prefix thiếu nhãn → push ra màn khoá chỉ còn "Từ chối"
(nhóm Khác) hoặc tên phân hệ, không nói được là phiếu gì.
"""
import re, os, sys

# Bắt nhầm từ tên biến / chuỗi không phải prefix — bỏ qua.
NOISE = {'.', 'CHỜ DUYỆT', 'EMPLOYEEINFO', 'TYPE', 'VIEC'}
root=sys.argv[1] if len(sys.argv) > 1 else "hrm-api"
meta=open(os.path.join(root,'app/Support/NotificationMeta.php')).read()
block=meta[meta.index('OBJECT_LABELS = ['):]
block=block[:block.index('];')]
known={k.upper() for k in re.findall(r"'([^']+)'\s*=>",block)}
found={}
pats=[r"NOTIFY_PREFIX\s*=\s*'\[?([^'\]]+)\]?'",
      r"NotificationMeta::build\(\s*[^,]+,\s*'([^']+)'",
      r"['\"]\[([A-ZĐ][A-ZĐ0-9_-]{1,11})\]\s"]
for d in ['app','Modules']:
    for dp,_,fs in os.walk(os.path.join(root,d)):
        if '/vendor' in dp or 'Tests' in dp: continue
        for f in fs:
            if not f.endswith('.php') or f.endswith('.blade.php'): continue
            p=os.path.join(dp,f); s=open(p,errors='ignore').read()
            if 'Notification' not in s and 'sendNotification' not in s and 'NOTIFY' not in s: continue
            for pat in pats:
                for m in re.finditer(pat,s):
                    k=m.group(1).strip().upper()
                    found.setdefault(k,set()).add(os.path.relpath(p,root))
for k in sorted(found):
    if k not in known and k not in NOISE: print(k, '|', ', '.join(sorted(found[k]))[:160])

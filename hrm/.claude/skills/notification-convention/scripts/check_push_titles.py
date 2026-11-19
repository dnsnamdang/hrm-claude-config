"""Rà tiêu đề màn hình chờ (push) tự đặt trong code — phải ≤ 28 ký tự (NotificationMeta::PUSH_TITLE_MAX).

Chạy từ thư mục HRM/:  python3 .claude/skills/notification-convention/scripts/check_push_titles.py [đường dẫn hrm-api]
In ra mỗi `'push_title' => '…'` vượt trần (chỉ đo phần chữ cố định; phần ghép biến thì tự đếm thêm) và nhãn
OBJECT_LABELS dài quá 25 ký tự (không đứng một mình làm tiêu đề được). RỖNG = đạt.
Vượt 28 thì push() BỎ tiêu đề riêng, quay về câu khuôn — người viết tưởng đã đặt tiêu đề mà không thấy hiện.
"""
import re, os, sys

root = sys.argv[1] if len(sys.argv) > 1 else "hrm-api"
MAX_TITLE, MAX_LABEL = 28, 25
for d in ['app', 'Modules']:
    for dp, _, fs in os.walk(os.path.join(root, d)):
        if '/vendor' in dp:
            continue
        for f in fs:
            if not f.endswith('.php'):
                continue
            p = os.path.join(dp, f)
            for i, line in enumerate(open(p, errors='ignore'), 1):
                for m in re.finditer(r"'push_title'\s*=>\s*'([^']*)'", line):
                    if len(m.group(1)) > MAX_TITLE:
                        print(f"TITLE {len(m.group(1))} | {m.group(1)} | {os.path.relpath(p, root)}:{i}")
meta = open(os.path.join(root, 'app/Support/NotificationMeta.php')).read()
block = meta[meta.index('OBJECT_LABELS = ['):]
block = block[:block.index('];')]
for k, v in re.findall(r"'([^']+)'\s*=>\s*'([^']+)'", block):
    if len(v) > MAX_LABEL:
        print(f"LABEL {len(v)} | {k} => {v}")

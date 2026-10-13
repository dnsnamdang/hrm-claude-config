# Tách email thông báo nhận xét Google Docs (raw/*.txt) -> comments.json (gộp theo tài liệu + chuỗi nhận xét)
import glob, json, re, os, unicodedata
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
HDR = re.compile(r'^\t?(.+?) • (\d{1,2}:\d{2}, \d{1,2} thg \d{1,2}) \(GMT\+07:00\)(Tạo mới)?$')
SKIP = ('Mở', 'Nhận xét', '', 'Trả lời', 'Chuyển tiếp')


def parse_email(lines):
    """Trả (tên file, [chuỗi]) cho 1 email; chuỗi = {'anchor','posts':[(author,time,text)]}"""
    out = []
    i = 0
    fname = None
    while i < len(lines):
        if re.match(r'^(Hoạt động mới trong tài liệu sau|.+ trong tài liệu dưới đây|.+ vào tài liệu dưới đây|.+ tài liệu dưới đây\.?)$', lines[i].strip()):
            fname = lines[i + 1].strip()
            i += 2
            break
        i += 1
    if not fname:
        return None, []
    cur = None
    pending_anchor = None
    while i < len(lines):
        l = lines[i]
        s = l.strip()
        if s.startswith('Google LLC') or s.startswith('Bạn nhận được email này'):
            break
        m = HDR.match(l.rstrip())
        if m:
            if cur is None or pending_anchor is not None:
                cur = {'anchor': pending_anchor or '', 'posts': []}
                out.append(cur)
                pending_anchor = None
            author, time = m.group(1).strip(), m.group(2)
            # nội dung = các dòng sau tới header kế/“Mở”
            j = i + 1
            body = []
            while j < len(lines):
                t = lines[j].rstrip()
                if HDR.match(t) or t.strip() == 'Mở':
                    break
                body.append(t.strip())
                j += 1
            text = '\n'.join(b for b in body if b)
            cur['posts'].append((author, time, text))
            i = j
            continue
        if s == 'Mở':
            cur = None
            i += 1
            continue
        if re.match(r'^\t?(\d+ nhận xét|Đã giải quyết \d+)$', l) or s in SKIP:
            i += 1
            continue
        # dòng trích đoạn chữ được nhận xét
        pending_anchor = s if pending_anchor is None else pending_anchor + ' ' + s
        i += 1
    return fname, out


def main():
    docs = OrderedDict()
    for f in sorted(glob.glob(os.path.join(HERE, 'raw', '*.txt'))):
        txt = unicodedata.normalize('NFC', open(f).read())
        # tách từng email trong chuỗi: mỗi email bắt đầu bằng dòng người gửi <comments-noreply@...>
        chunks = re.split(r'\n[^\n]*<comments-noreply@docs\.google\.com>\n', txt)
        for ch in chunks[1:]:
            fname, threads = parse_email(ch.split('\n'))
            if not fname:
                continue
            d = docs.setdefault(fname, OrderedDict())
            for th in threads:
                if not th['posts']:
                    continue
                a0, t0, x0 = th['posts'][0]
                key = (a0, t0, x0)
                cur = d.setdefault(key, {'anchor': th['anchor'], 'posts': []})
                if len(th['anchor']) > len(cur['anchor']):
                    cur['anchor'] = th['anchor']
                for p in th['posts']:
                    if list(p) not in cur['posts']:
                        cur['posts'].append(list(p))
                cur['posts'].sort(key=lambda p: (int(re.search(r'(\d+) thg (\d+)', p[1]).group(2)), int(re.search(r', (\d+) thg', p[1]).group(1)), p[1].split(',')[0].zfill(5)))
    out = []
    for fname, d in docs.items():
        items = []
        for c in d.values():
            status = 'Đang mở'
            for a, t, x in c['posts']:
                if x.startswith('Được đánh dấu là đã giải quyết'):
                    status = 'Đã giải quyết'
                elif 'Đã mở lại' in x:
                    status = 'Mở lại'
            items.append({**c, 'status': status})
        out.append({'file': fname, 'comments': items})
    json.dump(out, open(os.path.join(HERE, 'comments.json'), 'w'), ensure_ascii=False, indent=1)
    for d in out:
        st = {}
        for c in d['comments']:
            st[c['status']] = st.get(c['status'], 0) + 1
        print(d['file'], len(d['comments']), st)


if __name__ == '__main__':
    main()

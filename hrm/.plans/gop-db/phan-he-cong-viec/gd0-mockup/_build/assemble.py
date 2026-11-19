import json, re, base64, os, sys, urllib.request, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from retab import retab
sys.path.insert(0, '/private/tmp/claude-501/-Users-dnsnamdang-Documents-DNSMEDIA-websites-ERP-HRM/43cb6d96-4200-4584-8e7b-fb55417d2759/scratchpad/mk')
from sb import add_sidebar, add_apptop, add_kpis
NOCSS = os.environ.get('NOCSS') == '1'

CAP = '/private/tmp/claude-501/-Users-dnsnamdang-Documents-DNSMEDIA-websites-ERP-HRM/43cb6d96-4200-4584-8e7b-fb55417d2759/scratchpad/cap/'
MK = '/private/tmp/claude-501/-Users-dnsnamdang-Documents-DNSMEDIA-websites-ERP-HRM/43cb6d96-4200-4584-8e7b-fb55417d2759/scratchpad/mk/'
OUT = '/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-claude-config/hrm/.plans/gop-db/phan-he-cong-viec/gd0-mockup/'
DEV = 'http://127.0.0.1:3000'
os.makedirs(OUT + 'screens', exist_ok=True)

def load(f):
    s = open(CAP + f, encoding='utf-8').read()
    return json.loads(s) if s.startswith('"') else s

_cache = {}
def fetch(url):
    if url not in _cache:
        with urllib.request.urlopen(url, timeout=30) as r:
            _cache[url] = r.read()
    return _cache[url]

def b64(data, mime):
    return 'data:%s;base64,%s' % (mime, base64.b64encode(data).decode())

MIME = {'woff2': 'font/woff2', 'woff': 'font/woff', 'png': 'image/png', 'jpg': 'image/jpeg', 'svg': 'image/svg+xml', 'gif': 'image/gif'}

# ---------- CSS ----------
if NOCSS:
    MARK = '\n/* ===== mockup additions ===== */\n'
    old = open(OUT + 'mockup.css', encoding='utf-8').read()
    open(OUT + 'mockup.css', 'w', encoding='utf-8').write(old.split(MARK)[0] + MARK + open(MK + 'mk.css', encoding='utf-8').read())
else:
    blocks, seen = [], set()
    for f in ['css-tasks.css', 'css-solution.css', 'css-projitems.css']:
        for b in load(f).split('\n/*@@STYLE@@*/\n'):
            b = b.strip()
            if not b or b.startswith('/* LINK') or b in seen:
                continue
            seen.add(b); blocks.append(b)
    css = '\n'.join(blocks)
    css = re.sub(r'/\*# sourceMappingURL=[^*]*\*/', '', css)
    css = re.sub(r'@import url\(https://fonts\.googleapis\.com[^;]*;', '', css)

    def repl_url(m):
        u = m.group(2)
        ext = u.rsplit('.', 1)[-1].lower()
        if (ext in ('eot', 'ttf', 'svg') or (ext == 'woff' and u.replace('.woff', '') + '.woff2' in ALL)) and '/fonts/' in u:
            return 'url(about:blank)'
        if ext not in MIME:
            return m.group(0)
        try:
            return 'url(%s)' % b64(fetch(DEV + u), MIME[ext])
        except Exception:
            return 'url(about:blank)'
    ALL = set(re.findall(r'(/_nuxt/[^)"\'?#]+)', css))
    css = re.sub(r'url\((["\']?)(/_nuxt/[^)"\'?#]+)[^)]*\)', repl_url, css)

    # remixicon 4.3.0 (CDN in app) — woff2 only
    rx = open(MK + 'fonts/remixicon.css', encoding='utf-8').read()
    rxw = b64(open(MK + 'fonts/remixicon.woff2', 'rb').read(), 'font/woff2')
    rx = re.sub(r'@font-face\s*{[^}]*}', '@font-face{font-family:"remixicon";src:url(%s) format("woff2");font-display:block}' % rxw, rx, count=1)

    # Roboto — latin, latin-ext, vietnamese subsets
    rb = open(MK + 'fonts/roboto.css', encoding='utf-8').read()
    faces = []
    for m in re.finditer(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*{[^}]*})', rb):
        if m.group(1) in ('latin', 'latin-ext', 'vietnamese'):
            face = m.group(2)
            url = re.search(r'url\(([^)]+)\)', face).group(1)
            faces.append(face.replace(url, b64(fetch(url), 'font/woff2')))
    roboto = '\n'.join(faces)

    mkcss = open(MK + 'mk.css', encoding='utf-8').read()
    open(OUT + 'mockup.css', 'w', encoding='utf-8').write(roboto + '\n' + rx + '\n' + css + '\n/* ===== mockup additions ===== */\n' + mkcss)


# ---------- screens ----------
def clean_body(s):
    s = re.sub(r'<script\b[^>]*>.*?</script>', '', s, flags=re.S)
    s = re.sub(r'<audio\b[^>]*>(</audio>)?', '', s)
    def img(m):
        u = m.group(1)
        if u.startswith('/_nuxt/'):
            ext = u.rsplit('.', 1)[-1].lower()
            try:
                return 'src="%s"' % b64(fetch(DEV + u), MIME.get(ext, 'image/png'))
            except Exception:
                return 'src=""'
        return m.group(0)
    s = re.sub(r'src="(/_nuxt/[^"]+)"', img, s)
    s = re.sub(r'href="/(?!/)[^"]*"', 'href="javascript:void(0)"', s)
    return s

SCREENS = [
    ('01-danh-sach-khong-gian', 'Danh sách không gian làm việc của tôi', 'mk-s-space-list.html', None, None),
    ('02-phong-tong-quan', 'Phòng làm việc · Tổng quan', 'mk-s-room-overview.html', None, ('room', 'overview')),
    ('03-phong-nhiem-vu', 'Phòng làm việc · Nhiệm vụ', 'mk-s-room-tasks.html', None, ('room', 'tasks')),
    ('04-phong-trao-doi', 'Phòng làm việc · Trao đổi', 'mk-s-room-chat.html', None, ('room', 'chat')),
    ('05-phong-thanh-vien', 'Phòng làm việc · Thành viên', 'mk-s-room-members.html', None, ('room', 'members')),
    ('06-phong-du-an-noi-bo', 'Phòng làm việc · Dự án nội bộ', 'mk-s-room-groups.html', None, ('room', 'projects')),
    ('07-popup-tao-du-an-trong-phong', 'Popup Tạo dự án nội bộ trong phòng', 'mk-s-room-groups.html', 'mk-s-modal-group.html', ('room', 'projects')),
    ('08-du-an-noi-bo-kin-trao-doi', 'Dự án nội bộ Kín · Trao đổi', 'mk-s-group-chat.html', None, ('iproj', 'chat')),
    ('09-giai-phap-thanh-vien', 'Dự án KH · Giải pháp · Thành viên', 'mk-s-gp-members.html', None, ('gp', 'members')),
    ('10-tkt-van-de', 'Dự án KH · Tiền khả thi · Vấn đề', 'mk-s-tkt-issues.html', None, ('tkt', 'issues')),
    ('11-tao-phong-theo-phong-ban', 'Tạo không gian làm việc · Phòng làm việc theo phòng ban', 'mk-s-space-list.html', 'mk-s-modal-room-dept.html', None),
    ('12-tao-phong-tu-chon', 'Tạo không gian làm việc · Phòng làm việc tự chọn', 'mk-s-space-list.html', 'mk-s-modal-room-custom.html', None),
    ('13-tao-du-an-noi-bo', 'Tạo không gian làm việc · Dự án nội bộ', 'mk-s-space-list.html', 'mk-s-modal-project.html', None),
    ('14-tkt-menu-them', 'Dự án KH · Tiền khả thi · menu Thêm đang mở', 'mk-s-tkt-issues.html', None, ('tkt', 'issues', True)),
]
SCREENS += [
    ('16-du-an-noi-bo-nhiem-vu-gon', 'Dự án nội bộ · Nhiệm vụ (thanh công cụ gọn)', 'mk-s-iproj-tasks.html', None, ('iproj', 'tasks')),
    ('17-du-an-noi-bo-nhiem-vu-dang-loc', 'Dự án nội bộ · Nhiệm vụ đang lọc, popover Lọc mở', 'mk-s-iproj-tasks.html', None, ('iproj', 'tasks')),
]
SCREENS += [
    ('19-phong-van-de', 'Phòng làm việc · Vấn đề', 'mk-s-room-issues.html', None, ('room', 'issues')),
    ('20-phong-file', 'Phòng làm việc · File', 'mk-s-room-files.html', None, ('room', 'files')),
    ('21-phong-cau-hinh', 'Phòng làm việc · Cấu hình', 'mk-s-room-settings.html', None, ('room', 'settings')),
    ('22-giai-phap-tong-quan', 'Dự án KH · Giải pháp · Tổng quan', 'mk-s-gp-overview.html', None, ('gp', 'overview')),
    ('23-giai-phap-hang-muc', 'Dự án KH · Giải pháp · Hạng mục', 'mk-s-gp-modules.html', None, ('gp', 'modules')),
]
SCREENS.append(('24-sidebar-chuyen-nhanh', 'Sidebar · chuyển nhanh không gian làm việc', 'mk-s-room-overview.html', None, ('room', 'overview')))
SCREENS.append(('18-bo-cuc-chu-thich', 'Bố cục có chú thích · Dự án nội bộ · Nhiệm vụ', 'mk-s-iproj-tasks.html', None, ('iproj', 'tasks')))
ANNOT_JS = '<script>window.__MK_ANNOT=' + open(MK + 'annot.json', encoding='utf-8').read() + ';</script><script>' + open(MK + 'annot.js', encoding='utf-8').read() + '</script>'
BODYCLS = {'17-du-an-noi-bo-nhiem-vu-dang-loc': 'mk-filtered mk-filter-open', '18-bo-cuc-chu-thich': 'mk-filtered'}
FILTER_JS = ('<script>(function(){var b=document.body,btn=document.querySelector(".mk-filter-btn"),pop=document.querySelector(".mk-filter-pop");if(!btn)return;'
  'btn.addEventListener("click",function(e){e.stopPropagation();b.classList.toggle("mk-filter-open");});'
  'document.addEventListener("click",function(e){if(Date.now()-(window.__mkRz||0)<400)return;if(pop&&!pop.contains(e.target))b.classList.remove("mk-filter-open");});'
  'pop.querySelectorAll(".mk-fp-ft button").forEach(function(x){x.addEventListener("click",function(e){e.stopPropagation();b.classList.toggle("mk-filtered",/Áp dụng/.test(x.textContent));window.__mkRenumber&&window.__mkRenumber();b.classList.remove("mk-filter-open");});});'
  'document.querySelectorAll(".mk-af i,.mk-af-clear").forEach(function(x){x.addEventListener("click",function(){b.classList.remove("mk-filtered");window.__mkRenumber&&window.__mkRenumber();});});})();</script>')
if os.path.exists(CAP + 'mk-s-room-meetings.html'):
    SCREENS.append(('15-phong-meeting', 'Phòng làm việc · Meeting', 'mk-s-room-meetings.html', None, ('room', 'meetings')))
NOSORT = {'stt', 'hành động', 'thao tác', ''}
def sortify(body):
    def th(m):
        attrs, inner = m.group(1), m.group(2)
        if 'sortable-header' in inner: return m.group(0)
        label = re.sub(r'<[^>]+>', '', inner).strip().lower()
        if label in NOSORT: return m.group(0)
        dv = ' '.join(re.findall(r'(data-v-[0-9a-f]+="")', attrs))
        return '<th%s><span %s class="sortable-header">%s <i %s class="ri-arrow-up-down-line mk-sort"></i></span></th>' % (attrs, dv, inner.strip(), dv)
    def thead(m):
        return re.sub(r'<th\b([^>]*)>(.*?)</th>', th, m.group(0), flags=re.S)
    return re.sub(r'<thead\b.*?</thead>', thead, body, flags=re.S)
SORT_JS = '<script>' + open(MK + 'sort.js', encoding='utf-8').read() + '</script>'
import time
CSSV = str(int(time.time()))
for key, title, f, modal, tabs in SCREENS:
    body = clean_body(load(f))
    if tabs:
        body = retab(body, tabs[0], tabs[1], len(tabs) > 2)
        if len(tabs) > 2:
            body = re.sub(r'<body([^>]*)>', lambda m: '<body class="mk-menu-open"' + m.group(1) + '>', body, count=1)
    if f == 'mk-s-space-list.html':
        body = re.sub(r'<body([^>]*)>', lambda m: '<body class="mk-hub"' + m.group(1) + '>', body, count=1)
    body = add_sidebar(body, key, f == 'mk-s-space-list.html')
    body = add_apptop(body, key)
    body = add_kpis(body)
    body = sortify(body)
    if 'mk-st-nav' in body:
        body = body.replace('</body>', '<script>' + open(MK + 'st.js', encoding='utf-8').read() + '</script></body>')
    if '<thead' in body:
        body = body.replace('</body>', SORT_JS + '</body>')
    if '<table' in body:
        body = body.replace('</body>', '<script>' + open(MK + 'hs.js', encoding='utf-8').read() + '</script></body>')
    if key in BODYCLS:
        body = re.sub(r'<body([^>]*)>', lambda m: '<body class="%s"' % BODYCLS[key] + m.group(1) + '>', body, count=1)
    if 'mk-filter-btn' in body:
        body = body.replace('</body>', FILTER_JS + '<script>' + open(MK + 'rz.js', encoding='utf-8').read() + '</script></body>')
    if key == '24-sidebar-chuyen-nhanh':
        body = body.replace('</body>', '<script>window.__mkWsOpen&&window.__mkWsOpen(true);</script></body>')
    if key == '18-bo-cuc-chu-thich':
        body = body.replace('</body>', ANNOT_JS + '</body>')
    if modal:
        m = clean_body(load(modal))
        body = body.replace('</body>', m + '<div class="modal-backdrop show" style="z-index:1039"></div></body>')
    if key in ('04-phong-trao-doi', '08-du-an-noi-bo-kin-trao-doi'):  # chat demo tương tác (04/11)
        body = body.replace('</head>', '</head>')
        body = body.replace('</body>', '<style>' + open(MK + 'chatx.css', encoding='utf-8').read() + '</style><script>window.__CX_SPACE=%s;</script><script>' % ('"iproj"' if key.startswith('08') else '"room"') + open(MK + 'chatx.js', encoding='utf-8').read() + '</script></body>')
    if key in ('03-phong-nhiem-vu', '19-phong-van-de'):  # U19 thử: Danh sách nhóm · Bảng
        body = body.replace('</body>', '<script>' + open(MK + 'lv.js', encoding='utf-8').read() + '</script></body>')
        body = body.replace('</body>', '<script>' + open(MK + 'td.js', encoding='utf-8').read() + '</script></body>')
        body = body.replace('</body>', '<script>' + open(MK + 'flt.js', encoding='utf-8').read() + '</script></body>')
    body = body.replace('</body>', '<script src="../present-notes.js"></script><script>' + open(MK + 'present.js', encoding='utf-8').read() + '</script></body>')
    doc = ('<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
           '<title>%s</title><link rel="stylesheet" href="../mockup.css?v=%s"></head>%s</html>') % (html.escape(title), CSSV, body)
    # U16: tên Phòng theo phòng ban = tên phòng ban; DB lưu IN HOA ⇒ hiển thị viết hoa chữ đầu mỗi từ (user chọn 03/11)
    doc = doc.replace('Phòng Nhân sự Hành chính', 'Phòng Nhân Sự Hành Chính').replace('Phòng Hành chính', 'Phòng Nhân Sự Hành Chính').replace('Phòng Kỹ thuật công nghệ', 'Phòng Kỹ Thuật Công Nghệ')
    open(OUT + 'screens/' + key + '.html', 'w', encoding='utf-8').write(doc)

print('css MB', round(os.path.getsize(OUT + 'mockup.css') / 1e6, 2))
for key, *_ in SCREENS:
    print(key, round(os.path.getsize(OUT + 'screens/' + key + '.html') / 1e3), 'KB')

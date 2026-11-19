# Sidebar truy cập nhanh không gian làm việc (U14) — gắn vào rail hub thật (SaleHubSidebar) của phân hệ Công việc.
import html, os, re
MK = os.path.dirname(os.path.abspath(__file__)) + '/'
DV = 'data-v-6f8d4d6a=""'
RAIL = open(MK + 'rail.html', encoding='utf-8').read()

ROOM, IPROJ, KH = '#0EA5E9', '#7C3AED', '#D97706'
# id: (tên, loại, icon, màu, mô tả, chưa đọc, quá hạn, link, kín)
S = {
    'room-hc':  ('Phòng Nhân Sự Hành Chính', 'Phòng làm việc', 'ri-community-line', ROOM, 'Theo phòng ban · P. NSHC · 18 thành viên', 12, 1, '02-phong-tong-quan.html', 0),
    'room-ht':  ('Hỗ trợ phần mềm', 'Phòng làm việc', 'ri-customer-service-2-line', ROOM, 'Tự chọn · 4 phòng ban · 9 thành viên', 5, 0, '', 0),
    'room-kt':  ('Phòng Kỹ Thuật Công Nghệ', 'Phòng làm việc', 'ri-team-line', ROOM, 'Theo phòng ban · P. KTCN · 27 thành viên', 0, 0, '', 0),
    'ip-ms':    ('Mua sắm đồng phục sơ mi 2027', 'Dự án nội bộ', 'ri-folders-line', IPROJ, 'Thuộc Phòng Nhân Sự Hành Chính · đến 15/12/2026', 4, 0, '', 0),
    'ip-hn':    ('Tổ chức hội nghị công đoàn 2027', 'Dự án nội bộ', 'ri-folders-line', IPROJ, 'Thuộc Phòng Nhân Sự Hành Chính · đến 20/01/2027', 2, 0, '16-du-an-noi-bo-nhiem-vu-gon.html', 1),
    'ip-qt':    ('Chuẩn hoá quy trình hỗ trợ 2027', 'Dự án nội bộ', 'ri-folders-line', IPROJ, 'Thuộc Hỗ trợ phần mềm · đến 28/02/2027', 0, 0, '', 0),
    'ip-cv':    ('Triển khai phân hệ Công việc 2027', 'Dự án nội bộ', 'ri-folders-line', IPROJ, 'Độc lập · đến 31/03/2027', 0, 0, '', 0),
    'da010':    ('DA010 - Tính toán lại khoảng cách lắp bộ 3D koisu với cầu Gaochang', 'Dự án KH · Tiền khả thi', 'ri-briefcase-4-line', KH, 'Gaochang Việt Nam · liên kết GP40', 0, 0, '10-tkt-van-de.html', 0),
    'gp40':     ('GP40 - Tính toán lại khoảng cách lắp bộ 3D koisu với cầu Gaochang', 'Dự án KH · Giải pháp', 'ri-lightbulb-flash-line', KH, 'Cty TNHH Gaochang Việt Nam · liên kết DA010', 6, 0, '22-giai-phap-tong-quan.html', 0),
    'da025':    ('DA025 - Hệ thống đường ống bộ trà khô Matit', 'Dự án KH · Tiền khả thi', 'ri-briefcase-4-line', KH, 'Cty TNHH Trà Matit · liên kết GP32', 3, 0, '', 0),
    'gp30':     ('GP30 - 2S Vinfast', 'Dự án KH · Giải pháp', 'ri-lightbulb-flash-line', KH, 'VinFast Hải Phòng · liên kết DA006', 0, 2, '', 0),
    'tp0123':   ('TP-2026-0123 - Thiết bị xưởng 3S Ford Hưng Yên', 'Dự án KH · Hợp đồng', 'ri-file-paper-2-line', KH, 'Ford Việt Nam · Hợp đồng bán', 1, 0, '', 0),
}
ARCH = [
    ('Kiểm kê tài sản quý III', 'Dự án nội bộ', 'ri-folders-line', IPROJ, 'Thuộc Phòng Nhân Sự Hành Chính · đóng 30/09/2026'),
    ('Tổng kết cuối năm 2025', 'Dự án nội bộ', 'ri-folders-line', IPROJ, 'Thuộc Phòng Nhân Sự Hành Chính · đóng 15/01/2026'),
    ('Ban dự án ERP 2025', 'Phòng làm việc', 'ri-team-line', ROOM, 'Tự chọn · lưu trữ 20/12/2025'),
    ('DA006 - Nhà xưởng VinFast giai đoạn 1', 'Dự án KH · Tiền khả thi', 'ri-briefcase-4-line', KH, 'VinFast Hải Phòng · đã chuyển GP30'),
    ('TP-2025-0871 - Bảo trì hệ thống PCCC Matit', 'Dự án KH · Hợp đồng', 'ri-file-paper-2-line', KH, 'Cty TNHH Trà Matit · đã thanh lý'),
]
PINS = ['room-hc', 'ip-hn', 'gp40', 'da025']
RECENT = ['room-hc', 'gp40', 'ip-hn', 'room-ht', 'da010', 'ip-cv']
ROOMS = [('room-hc', ['ip-ms', 'ip-hn']), ('room-ht', ['ip-qt']), ('room-kt', [])]
IPROJS = ['ip-ms', 'ip-hn', 'ip-qt', 'ip-cv']
KHS = [('Tiền khả thi', ['da010', 'da025']), ('Giải pháp', ['gp40', 'gp30']), ('Hợp đồng', ['tp0123'])]
RAIL_COL = {ROOM: '#38bdf8', IPROJ: '#b79cf0', KH: '#f5a524'}

CUR = {}
for k in ['02-phong-tong-quan', '03-phong-nhiem-vu', '04-phong-trao-doi', '05-phong-thanh-vien', '06-phong-du-an-noi-bo',
          '07-popup-tao-du-an-trong-phong', '15-phong-meeting', '24-sidebar-chuyen-nhanh', '19-phong-van-de', '20-phong-file', '21-phong-cau-hinh']:
    CUR[k] = 'room-hc'
for k in ['08-du-an-noi-bo-kin-trao-doi', '16-du-an-noi-bo-nhiem-vu-gon', '17-du-an-noi-bo-nhiem-vu-dang-loc', '18-bo-cuc-chu-thich']:
    CUR[k] = 'ip-hn'
for k in ['09-giai-phap-thanh-vien', '22-giai-phap-tong-quan', '23-giai-phap-hang-muc']:
    CUR[k] = 'gp40'
for k in ['10-tkt-van-de', '14-tkt-menu-them']:
    CUR[k] = 'da010'

e = html.escape
def href(link):
    return link or 'javascript:void(0)'

def short(n):
    return n.split(' - ', 1)[0] + ' - ' + n.split(' - ', 1)[1] if ' - ' in n else n

def rail_pin(i, cur):
    n, t, ic, col, *_ = S[i]
    un = S[i][5]
    b = '<b class="mk-pin-n">%d</b>' % un if un else ''
    c = '<em class="mk-pin-c">%d</em>' % un if un else ''
    return ('<a %s href="%s" class="cat cat-nav mk-pin%s" data-id="%s" title="%s · %s" style="--ic: %s;">'
            '<i %s class="cat-ic cat-ic-font mk-pin-ic %s">%s</i> <span %s>%s</span>%s</a>') % (
        DV, href(S[i][7]), ' on' if i == cur else '', i, e(n), e(t), RAIL_COL[col], DV, ic, b, DV, e(n), c)

def build_rail(cur, in_space):
    r = RAIL
    ws = ('<a %s class="cat mk-ws-cat%s" style="--ic: #4fd0c0;" title="Không gian làm việc (Ctrl K)"><i %s class="cat-ic cat-ic-font ri-layout-masonry-line"></i> '
          '<span %s>Không gian làm việc</span> <svg %s class="cat-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></a>') % (DV, ' on' if in_space and cur not in PINS else '', DV, DV, DV)
    pins = '<div class="mk-pin-h"><span>Đã ghim</span></div>' + ''.join(rail_pin(i, cur) for i in PINS) + '<div %s class="cat-div"></div>' % DV
    anchor = '<span data-v-6f8d4d6a="">Tổng quan</span></a>'
    assert anchor in r
    r = r.replace(anchor, anchor + ' ' + ws + pins, 1)
    return r

def row(i, cur, kid=False, pinned=None):
    n, t, ic, col, desc, un, od, link, kin = S[i]
    pinned = (i in PINS) if pinned is None else pinned
    tags = ''
    if kin: tags += '<span class="mk-wr-tag"><i class="ri-lock-line"></i>Kín</span>'
    if i == cur: tags += '<span class="mk-wr-cur">Đang mở</span>'
    meta = ''
    if od: meta += '<span class="mk-wr-od" title="Nhiệm vụ quá hạn"><i class="ri-alarm-warning-line"></i>%d</span>' % od
    if un: meta += '<span class="mk-wr-un" title="Tin chưa đọc">%d</span>' % un
    q = (n + ' ' + t + ' ' + desc).lower()
    return ('<a href="%s" class="mk-wr%s%s" data-id="%s" data-q="%s"><i class="mk-wr-ic %s" style="--t:%s"></i>'
            '<span class="mk-wr-tx"><span class="mk-wr-nm">%s%s</span><small>%s · %s</small></span>'
            '<span class="mk-wr-meta">%s</span><span class="mk-wr-pin%s" title="%s">%s</span></a>') % (
        href(link), ' mk-wr-kid' if kid else '', ' on' if i == cur else '', i, e(q), ic, col, e(n), tags, e(t), e(desc), meta,
        ' on' if pinned else '', 'Bỏ ghim' if pinned else 'Ghim lên thanh bên', '<i class="ri-pushpin-fill"></i>' if pinned else '<i class="ri-pushpin-line"></i>')

def sub(title, inner, count=None, hint=''):
    c = '<span class="c">%s</span>' % count if count is not None else ''
    h = '<span class="mk-sub-hint">%s</span>' % hint if hint else ''
    return '<div class="sub"><div class="sub__t">%s%s%s</div>%s</div>' % (title, h, c, inner)

def build_panel(cur):
    home = sub('Đã ghim', ''.join(row(i, cur) for i in PINS), len(PINS), 'hiện cả trên thanh bên')
    rec = [i for i in RECENT if i not in PINS]
    home += sub('Mở gần đây', ''.join(row(i, cur) for i in rec), len(rec))
    rooms = ''.join(row(r, cur) + ''.join(row(k, cur, kid=True) for k in kids) for r, kids in ROOMS)
    rooms = sub('Phòng làm việc', rooms, len(ROOMS), 'kèm Dự án nội bộ thuộc phòng')
    ip = sub('Dự án nội bộ', ''.join(row(i, cur) for i in IPROJS), len(IPROJS))
    kh = ''.join(sub(t, ''.join(row(i, cur) for i in ids), len(ids)) for t, ids in KHS)
    arch = ''.join('<a href="javascript:void(0)" class="mk-wr mk-wr-arch" data-q="%s"><i class="mk-wr-ic %s" style="--t:%s"></i><span class="mk-wr-tx"><span class="mk-wr-nm">%s</span><small>%s · %s</small></span><span class="mk-wr-meta"></span><span class="mk-wr-pin" style="visibility:hidden"></span></a>' % (
        e((n + ' ' + t + ' ' + d).lower()), ic, col, e(n), e(t), e(d)) for n, t, ic, col, d in ARCH)
    arch = sub('Lưu trữ', arch, len(ARCH), 'chỉ xem, không nhận thông báo')
    allr = ''.join(row(i, cur) for i in S)
    nkh = sum(len(x[1]) for x in KHS)
    nun = sum(1 for v in S.values() if v[5])
    pages = [('home', 'Ghim & gần đây', 'ri-pushpin-line', None, home),
             ('room', 'Phòng làm việc', 'ri-community-line', len(ROOMS), rooms),
             ('ip', 'Dự án nội bộ', 'ri-folders-line', len(IPROJS), ip),
             ('kh', 'Dự án khách hàng', 'ri-briefcase-4-line', nkh, kh),
             ('arch', 'Lưu trữ', 'ri-archive-line', len(ARCH), arch)]
    scats = ''.join('<a %s class="scat%s" data-p="%s"><span %s class="scat-ic"><i class="%s"></i></span><span %s class="scat-nm">%s</span>%s</a>' % (
        DV, ' on' if k == 'home' else '', k, DV, ic, DV, t, ('<span %s class="c">%d</span>' % (DV, c)) if c is not None else '') for k, t, ic, c, _ in pages)
    scats += ('<div class="mk-ws-foot"><a href="01-danh-sach-khong-gian.html"><i class="ri-list-check-3"></i>Xem danh sách đầy đủ</a>'
              '<span>Ghim tối đa 5 không gian lên thanh bên</span></div>')
    det = ''.join('<div class="mk-ws-page%s" data-p="%s">%s</div>' % (' on' if k == 'home' else '', k, body) for k, _, _, _, body in pages)
    det += '<div class="mk-ws-page" data-p="search"><div class="sub"><div class="sub__t">Kết quả tìm <span class="c mk-ws-cnt">0</span></div>%s<div class="mk-ws-empty">Không tìm thấy không gian làm việc phù hợp.</div></div></div>' % allr
    return ('<div class="mk-ws-bd"></div>'
            '<div %s class="misa-detail mk-ws" style="--acc: #1E8A63; --acc2: #38AD7A;">'
            '<div %s class="dtop"><span %s class="dhead">Không gian làm việc</span><span %s class="dsub">%d đang tham gia · %d có tin chưa đọc</span><span %s class="dclose" title="Đóng (Esc)">✕</span></div>'
            '<div class="mk-ws-bar"><div class="mk-ws-q"><i class="ri-search-line"></i><input type="text" placeholder="Tìm theo tên, mã dự án, khách hàng…"><kbd class="mk-kbd">Ctrl K</kbd></div>'
            '<a href="11-tao-phong-theo-phong-ban.html" class="v2-btn v2-btn--sm v2-btn--primary mk-ws-new"><i class="ri-add-line"></i> Tạo không gian làm việc</a></div>'
            '<div %s class="navwrap"><div %s class="subcats">%s</div><div %s class="subdetail">%s</div></div></div>') % (
        DV, DV, DV, DV, len(S), nun, DV, DV, DV, scats, DV, det)

def add_sidebar(body, key, hub):
    cur = CUR.get(key)
    rail = build_rail(cur, bool(cur))
    panel = build_panel(cur)
    js = '<script>' + open(MK + 'sb.js', encoding='utf-8').read() + '</script>'
    if hub:
        i = body.find('<div data-v-6f8d4d6a="" class="left-side-menu sale-cats"')
        assert i >= 0
        body = body[:i] + rail + body[i + len(RAIL):]
        body = body.replace('</body>', '<div class="sale-theme mk-sb-host">' + panel + '</div>' + js + '</body>')
    else:
        body = body.replace('</body>', '<div class="sale-theme mk-sb-host">' + rail + panel + '</div>' + js + '</body>')
        body = re.sub(r'<body\b', '<body data-sidebar-size="condensed"', body, count=1)
    return body


# ---- U15 (thử): header không gian nằm luôn trong topbar của phần mềm ----
import json as _json
APPTOP = set(CUR)

def _balanced(s, i, tag):
    depth = 0
    for m in re.finditer(r'<(/?)%s\b[^>]*>' % tag, s[i:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return i + m.end()
    raise ValueError(tag)

def _navbar():
    s = _json.load(open(MK + '../cap/mk-s-space-list.html', encoding='utf-8'))
    i = s.rfind('<div', 0, s.find('class="navbar-custom"'))
    return s[i:_balanced(s, i, 'div')]

def add_apptop(body, key):
    if key not in APPTOP:
        return body
    i = body.find('<header')
    while i >= 0 and 'class="topbar' not in body[i:i + 200]:
        i = body.find('<header', i + 1)
    j = _balanced(body, i, 'header')
    hd = body[i:j]
    ic = re.search(r'class="(ri-[\w-]+)"', hd).group(1)
    col = re.search(r'color: (rgb\([^)]*\))', hd).group(1)
    name = re.sub(r'<[^>]+>', '', re.search(r'<h1\b.*?</h1>', hd, re.S).group(0)).strip()
    pills = []
    for m in re.finditer(r'<span[^>]*class="pill ([^"]*)"', hd):
        k = m.start(); inner = hd[k:_balanced(hd, k, 'span')]
        inner = re.sub(r'^<span[^>]*>|</span>$', '', inner)
        inner = re.sub(r' data-v-[0-9a-f]+=""', '', inner)
        pills.append(('mk-ntb-brand' if 'thành viên' in re.sub(r'<[^>]+>', '', inner) else '', inner))
    # Luật gộp (U15d/U16): chỉ giữ thông tin KHÔNG trùng tên; phần còn lại vào tooltip
    meta, tip, links, kin = [], [], [], False
    by_dept = any('theo phòng ban' in re.sub(r'<[^>]+>', '', p).lower() for _, p in pills)
    for c, p in pills:
        if c: continue
        t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', p)).strip()
        if 'ri-links-line' in p: links.append(t); continue
        if 'theo phòng ban' in t.lower(): meta.append('Theo phòng ban'); continue
        if by_dept and 'ri-building' in p: tip.append(t); continue      # phòng ban = chính tên phòng
        if '›' in t: a, b2 = [x.strip() for x in t.split('›', 1)]; meta.append('%s · thuộc %s' % (b2, a)); continue
        if t == 'Kín': kin = True; continue
        if t.startswith('Dự án KH · '): meta.append(t[len('Dự án KH · '):]); continue
        if t.startswith('KH: '): meta.append(t[4:]); continue
        if re.match(r'^\d\d/\d\d/\d{4}', t): meta.append(t); continue
        tip.append(t)
    def pill(c, p):
        if c:
            n = re.sub(r'<[^>]+>', '', p).strip()
            av = ''.join('<i class="mk-av" style="background:%s">%s</i>' % (b, a) for a, b in AV)
            return '<a href="05-phong-thanh-vien.html" class="mk-ntb-mem" title="Xem thành viên"><span class="mk-avs">%s</span><b>%s</b><i class="ri-arrow-right-s-line mk-mem-go"></i></a>' % (av, n)
        return ''
    GRAD = {'rgb(14, 165, 233)': ('#38bdf8', '#2563eb'), 'rgb(124, 58, 237)': ('#c084fc', '#6d28d9'), 'rgb(217, 119, 6)': ('#fbbf24', '#ea580c')}
    g1, g2 = GRAD.get(col, ('#5eead4', '#0d9488'))
    AV = [('NH', '#f472b6'), ('TM', '#60a5fa'), ('LT', '#fbbf24')]
    kin_html = '<span class="mk-ntb-kin" title="Dự án Kín"><i class="ri-lock-line"></i>Kín</span>' if kin else ''
    meta_html = '<span class="mk-ntb-sep"></span><span class="mk-ntb-meta">%s</span>' % ' · '.join(html.escape(m) for m in meta) if meta else ''
    link_html = ''.join('<a href="javascript:void(0)" class="mk-ntb-link" title="Sang không gian liên kết"><i class="ri-links-line"></i>%s</a>' % html.escape(l) for l in links)
    title = ' · '.join([name] + meta + tip)
    dv = 'data-v-04b9b2ac=""'
    t = ('<div class="mk-ntb" style="--g1:%s;--g2:%s"><a href="01-danh-sach-khong-gian.html" class="mk-ntb-back" title="Quay lại danh sách không gian làm việc"><i class="ri-arrow-left-line"></i></a>'
         '<span class="mk-ntb-id" title="%s"><span class="mk-ntb-ic"><i class="%s"></i></span><h5 %s class="topbar-page-title mb-0 mk-ntb-nm">%s</h5>%s%s</span>%s%s</div>') % (
        g1, g2, html.escape(title), ic, dv, html.escape(name), kin_html, meta_html, link_html, ''.join(pill(c, p) for c, p in pills))
    nb = re.sub(r'<h5 data-v-04b9b2ac="" class="topbar-page-title mb-0">.*?</h5>', t, _navbar(), count=1, flags=re.S)
    body = body[:i] + body[j:]
    return body.replace('<div class="sale-theme mk-sb-host">', '<div class="sale-theme mk-sb-host">' + nb, 1)


# ---- U17: 5 thẻ số liệu Tổng quan → dải ô gọn (~60px) ----
def add_kpis(body):
    k = body.find('class="alert-card"')
    if k < 0:
        return body
    i = body.rfind('<div', 0, body.rfind('class="row"', 0, k) + 20)
    i = body.rfind('<div', 0, body.find('class="row"', body.rfind('class="row"', 0, k) - 5) + 1)
    j = _balanced(body, i, 'div')
    row = body[i:j]
    tiles = []
    for m in re.finditer(r'<div[^>]*class="alert-card"', row):
        c = row[m.start():_balanced(row, m.start(), 'div')]
        tone = re.search(r'alert-strip (tone-[\w-]+)', c).group(1)
        ic = re.search(r'<i[^>]*class="(ri-[\w-]+)', c).group(1)
        txt = lambda cls: re.sub(r'<[^>]+>', '', re.search(r'class="%s[^"]*"[^>]*>(.*?)</div>' % cls, c, re.S).group(1)).strip()
        t, v, d = txt('title'), txt('value'), txt('desc')
        tiles.append('<a href="javascript:void(0)" class="mk-kpi %s" title="%s — %s"><span class="mk-kpi-ic"><i class="%s"></i></span><b class="mk-kpi-v">%s</b>'
                     '<span class="mk-kpi-tx"><span class="mk-kpi-t">%s</span><span class="mk-kpi-d">%s</span></span><i class="ri-arrow-right-s-line mk-kpi-go"></i></a>' % (
                         tone, html.escape(t), html.escape(d), ic, html.escape(v), html.escape(t), html.escape(d)))
    return body[:i] + '<div class="mk-kpis">' + ''.join(tiles) + '</div>' + body[j:]

# Dựng 5 màn thao tác của không gian GP40 từ 5 màn Phòng Nhân Sự Hành Chính.
import re, sys, os
ROOT = '/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-claude-config/hrm/.plans/gop-db/phan-he-cong-viec/gd0-mockup/'
S = ROOT + 'screens/'
GP = open(S + '22-giai-phap-tong-quan.html', encoding='utf-8').read()

def balanced(s, start, tag='div'):
    """trả về vị trí kết thúc của thẻ <tag> mở tại start (đếm lồng nhau)"""
    depth, i = 0, start
    rx = re.compile(r'<(/?)' + tag + r'\b[^>]*>')
    for m in rx.finditer(s, start):
        depth += -1 if m.group(1) else 1
        if depth == 0: return m.end()
    raise Exception('unbalanced')

def seg(s, start_mark, end_mark):
    i = s.find(start_mark); j = s.find(end_mark, i); assert i >= 0 and j > i, (start_mark, end_mark)
    return i, j + len(end_mark)

# ---- khối chrome lấy từ màn 22 ----
i = GP.find('<div class="mk-ntb"'); GP_NTB = GP[i:balanced(GP, i)]
a, b = seg(GP, '<div data-v-b87c17de="" data-v-efc08788="" class="tabs-nav">', '<!--/mk-tabs-->'); GP_TABS = GP[a:b]

# ---- bộ dữ liệu GP40 (thay theo thứ tự, chuỗi dài trước) ----
COMMON = [
    ('TPE.TASK.NB.26.', 'TPE.TASK.GP.26.'),
    ('Giao ban tuần 45 — Phòng Nhân Sự Hành Chính', 'Họp tiến độ GP40 tuần 45'), ('Giao ban tuần 44 — Phòng Nhân Sự Hành Chính', 'Họp tiến độ GP40 tuần 44'),
    ('due: col(/^Hạn/)', 'due: col(/^Hạn(?!g)/)'), ('/^(Hạn|Ngày tạo)/', '/^(Hạn(?!g)|Ngày tạo)/'),  # “Hạng mục” cũng bắt đầu bằng “Hạn”
    ('sortable-header">Dự án <i', 'sortable-header">Hạng mục <i'), ('/^Dự án$/', '/^Hạng mục$/'), ('/^Dự án/', '/^Hạng mục/'), ('Dự án / Nhóm', 'Hạng mục'),
    ('>Dự án<', '>Hạng mục<'), ("'Dự án'", "'Hạng mục'"), ('Dự án: ', 'Hạng mục: '), ('"Dự án"', '"Hạng mục"'),
    # người (mã trước, tên sau)
    ('21410105 - Nguyễn Thị Hằng', '21410621 - Nguyễn Văn Hiếu'), ('21410210 - Lê Thu Trang', '21410177 - Đặng Minh Khoa'),
    ('21410133 - Trần Văn Minh', '21410188 - Lê Quang Vinh'), ('21410301 - Đỗ Mai Anh', '21410502 - Trịnh Đức Anh'),
    ('21410322 - Vũ Hoàng Long', '21410199 - Hoàng Minh Tâm'), ('21410415 - Phạm Quốc Huy', '21410176 - Phạm Thu Hà'),
    ('Nguyễn Thị Hằng', 'Nguyễn Văn Hiếu'), ('Lê Thu Trang', 'Đặng Minh Khoa'), ('Trần Văn Minh', 'Lê Quang Vinh'),
    ('Phạm Quốc Huy', 'Phạm Thu Hà'), ('Vũ Hoàng Long', 'Hoàng Minh Tâm'), ('Phạm Văn Tú', 'Trịnh Đức Anh'),
    # dự án nội bộ của phòng -> hạng mục của giải pháp
    ('Mua sắm đồng phục sơ mi 2027', 'Thiết kế bộ 3D koisu'), ('Tổ chức hội nghị công đoàn 2027', 'Kết cấu chân đế'),
    ('Kiểm kê tài sản quý III', 'Khảo sát mặt bằng & đo đạc'), ('— Việc chung của phòng', '— Việc chung của giải pháp'),
    ('Việc chung của phòng', 'Việc chung của giải pháp'),
    # nhiệm vụ
    ('Gia hạn hợp đồng vệ sinh toà nhà', 'Đo lại cao độ mố cầu phía Bắc'), ('Báo giá may đồng phục 3 nhà cung cấp', 'Vẽ bản vẽ lắp đặt bộ 3D koisu'),
    ('Đặt hội trường hội nghị', 'Tính tải trọng chân đế theo khoảng cách mới'), ('Cập nhật nội quy văn phòng 2027', 'Đối chiếu bản vẽ cũ của cầu Gaochang'),
    ('Chốt danh sách size sơ mi toàn công ty', 'Chốt kích thước chân đế với kinh doanh'), ('Kiểm kê bàn ghế tầng 2', 'Khảo sát hiện trạng cầu Gaochang'),
    ('Kiểm kê tài sản tầng 4', 'Xuất BOM thép hình bản V1'),
    # vấn đề
    ('Điều hoà phòng họp nhỏ không mát', 'Bản vẽ koisu thiếu kích thước chân đế'), ('Máy in tầng 3 kẹt giấy liên tục', 'Số liệu khảo sát lệch 12 cm so với hồ sơ cũ'),
    ('Nhà cung cấp B giao thiếu size XL', 'Khách đổi vị trí lắp đặt sang trụ T3'), ('Thiếu phòng họp cho hội nghị ngày 15/01', 'Thiếu thông số tải trọng cầu từ chủ đầu tư'),
    ('Sai lệch số liệu kiểm kê bàn ghế tầng 2', 'Sai mã thép trong BOM bản nháp'),
    # nhãn
    ("tags: ['Hợp đồng']", "tags: ['Hiện trường']"), ("tags: ['Mua sắm']", "tags: ['Bản vẽ']"), ("tags: ['Sự kiện']", "tags: ['Tính toán']"), ("tags: ['Thiết bị']", "tags: ['Bản vẽ']"),
]
MEET = [
    ('Giao ban tuần 45 — Phòng Nhân Sự Hành Chính', 'Họp tiến độ GP40 tuần 45'), ('Giao ban tuần 44 — Phòng Nhân Sự Hành Chính', 'Họp tiến độ GP40 tuần 44'),
    ('Chốt mẫu đồng phục sơ mi 2027', 'Rà soát bản vẽ bộ 3D koisu'), ('Làm việc NCC may Việt Tiến', 'Làm việc với Gaochang tại hiện trường'),
    ('Rà soát hợp đồng thuê văn phòng chi nhánh HCM', 'Chốt phương án kết cấu chân đế'), ('Họp nội bộ phòng ban', 'Họp nội bộ dự án'),
    ('>18 người<', '>7 người<'), ('>17 người<', '>6 người<'),
]
FILES = [
    ('Bao_gia_dong_phuc_3_NCC.xlsx', 'Bang_tinh_tai_trong_chan_de.xlsx'), ('Noi_quy_van_phong_2027_v2.docx', 'Thuyet_minh_tinh_toan_chan_de.docx'),
    ('May_in_tang3_loi.png', 'Hien_truong_tru_T3.png'), ('Mau_so_mi_xanh_navy.jpg', 'Anh_cau_Gaochang_phia_Bac.jpg'),
    ('Bien_ban_giao_ban_tuan_44.pdf', 'Bien_ban_hop_tien_do_tuan_44.pdf'), ('Danh_muc_tai_san_quy_III.xlsx', 'So_lieu_khao_sat_cao_do.xlsx'),
]

def chrome(s, active, title):
    s = re.sub(r'<title>.*?</title>', '<title>' + title + '</title>', s, 1)
    # header
    i = s.find('<div class="mk-ntb"'); assert i > 0
    s = s[:i] + GP_NTB + s[balanced(s, i):]
    # thanh tab của GP40, đặt tab đang chọn
    a, b = seg(s, '<div data-v-b87c17de="" data-v-efc08788="" class="tabs-nav">', '<!--/mk-tabs-->')
    t = GP_TABS.replace('tab-btn-root active" data-key="overview"', 'tab-btn-root" data-key="overview"')
    k = 'tab-btn-root" data-key="%s"' % active; assert k in t, active
    t = t.replace(k, 'tab-btn-root active" data-key="%s"' % active, 1)
    s = s[:a] + t + s[b:]
    # mục đang ở: GP40 thay cho Phòng NSHC (rail + bảng Không gian làm việc)
    s = s.replace('mk-pin on" data-id="room-hc"', 'mk-pin" data-id="room-hc"').replace('mk-pin" data-id="gp40"', 'mk-pin on" data-id="gp40"')
    s = s.replace('class="mk-wr on" data-id="room-hc"', 'class="mk-wr" data-id="room-hc"').replace('class="mk-wr" data-id="gp40"', 'class="mk-wr on" data-id="gp40"')
    return s

def data_regions(s):
    """vùng được thay dữ liệu: nội dung (content-page → mk-sb-host) + script dữ liệu (không đụng sb.js, script trình bày)"""
    regs = [(s.find('class="content-page"'), s.find('mk-sb-host'))]
    for m in re.finditer(r'<script>', s):
        e = s.find('</script>', m.end()); body = s[m.end():e]
        if 'mk-sb-host' in body[:200] or 'Bản trình bày' in body[:120] or 'var STORY' in body: continue
        regs.append((m.end(), e))
    return regs

def subst(s, pairs):
    regs = sorted(data_regions(s), reverse=True)
    for a, b in regs:
        part = s[a:b]
        for x, y in pairs: part = part.replace(x, y)
        s = s[:a] + part + s[b:]
    return s

JOBS = [
    ('03-phong-nhiem-vu', '25-gp-nhiem-vu', 'tasks', 'Dự án KH · Giải pháp · Nhiệm vụ', COMMON),
    ('19-phong-van-de', '26-gp-van-de', 'issues', 'Dự án KH · Giải pháp · Vấn đề', COMMON),
    ('15-phong-meeting', '27-gp-meeting', 'meetings', 'Dự án KH · Giải pháp · Meeting', MEET + COMMON),
    ('20-phong-file', '28-gp-file', 'files', 'Dự án KH · Giải pháp · File', FILES + COMMON),
    ('04-phong-trao-doi', '29-gp-trao-doi', 'chat', 'Dự án KH · Giải pháp · Trao đổi', []),
]
if __name__ == '__main__':
    for src, dst, act, title, pairs in JOBS:
        s = open(S + src + '.html', encoding='utf-8', newline='').read()
        s = chrome(s, act, title)
        if pairs: s = subst(s, pairs)
        open(S + dst + '.html', 'w', encoding='utf-8', newline='').write(s)
        print('built', dst, len(s))

# ================= bước 2: panel chi tiết + chat =================
SCR = os.path.dirname(os.path.abspath(__file__)) + '/'
GP_DETAIL = open(SCR + 'gp_detail.js', encoding='utf-8').read().rstrip()
GP_CHAT = r"""SP === 'gp' ? {
    title: 'GP40 - Tính toán lại khoảng cách lắp bộ 3D koisu', kin: false, total: 7, ctx: 'Giải pháp',
    sub: 'Dự án KH · Giải pháp · Cty TNHH Gaochang Việt Nam · 7 thành viên · đội kinh doanh gửi vấn đề vào đây',
    people: [['Nguyễn Văn Hiếu', 'PM làm giải pháp', 'HN_GP', '21410621', 1], ['Đặng Minh Khoa', 'Trưởng hạng mục', 'HN_GP', '21410177', 1], ['Lê Quang Vinh', 'Thành viên', 'HN_GP', '21410188', 0],
      ['Phạm Thu Hà', 'Thành viên', 'HN_GP', '21410176', 1], ['Đỗ Mai Anh', 'Thành viên', 'HN_GP', '21410301', 1], ['Hoàng Minh Tâm', 'Thành viên', 'HN_GP', '21410199', 0],
      ['Trịnh Đức Anh', 'Kinh doanh (gửi vấn đề)', 'HN_KD1', '21410502', 1]],
    joiner: ['Ngô Đức Thịnh', 'Thành viên', 'HN_GP', '21410391', 1],
    objs: {
      T118: { k: 't', code: 'TPE.TASK.GP.26.0118', n: 'Đo lại cao độ mố cầu phía Bắc', st: 'Đang thực hiện', as: 'Đặng Minh Khoa', ap: 'Nguyễn Văn Hiếu', due: '01/11/2026', pct: 70, hrs: 4, pr: 'Cao' },
      T141: { k: 't', code: 'TPE.TASK.GP.26.0141', n: 'Vẽ bản vẽ lắp đặt bộ 3D koisu', st: 'Đang thực hiện', as: ME, ap: 'Nguyễn Văn Hiếu', due: '07/11/2026', pct: 50, hrs: 12 },
      T142: { k: 't', code: 'TPE.TASK.GP.26.0142', n: 'Chốt kích thước chân đế với kinh doanh', st: 'Chờ bắt đầu', as: ME, ap: 'Nguyễn Văn Hiếu', due: '14/11/2026', pct: 0, hrs: 6 },
      T127: { k: 't', code: 'TPE.TASK.GP.26.0127', n: 'Đối chiếu bản vẽ cũ của cầu Gaochang', st: 'Hoàn thành', as: 'Đặng Minh Khoa', ap: 'Nguyễn Văn Hiếu', due: '31/10/2026', pct: 100, hrs: 5 },
      T155: { k: 't', code: 'TPE.TASK.GP.26.0155', n: 'Xuất BOM thép hình bản V1', st: 'Hoàn thành - Chờ duyệt', as: 'Phạm Thu Hà', ap: ME, due: '03/11/2026', pct: 100, hrs: 8 },
      I07: { k: 'i', code: 'ISS-202611-0007', n: 'Trụ T3 có đường điện ngầm chưa có trong hồ sơ', st: 'Đã phân công', as: 'Phạm Thu Hà', rp: ME, due: '04/11/2026', pr: 'Cao' },
      I09: { k: 'i', code: 'ISS-202611-0009', n: 'Bản vẽ koisu thiếu kích thước chân đế', st: 'Đang xử lý', as: 'Hoàng Minh Tâm', rp: 'Trịnh Đức Anh', due: '05/11/2026' },
      TX: { k: 't', code: 'TPE.TASK.KD.26.0149', n: 'Lập báo giá sơ bộ cho Gaochang', st: 'Đang thực hiện', as: 'Trịnh Đức Anh', ap: 'Trịnh Đức Anh', due: '10/11/2026', lock: 'Tiền khả thi DA010' }
    },
    msgs: [
      { d: 'Hôm qua', w: 'Nguyễn Văn Hiếu', t: '16:20', x: 'Mọi người ơi, khách Gaochang chốt tăng khoảng cách 2 trụ lên **18,6 m**. Mình đã cập nhật trọng số hạng mục, mọi người bám theo nhé.' },
      { d: 'Hôm qua', sys: 'member', h: '<b>Nguyễn Văn Hiếu</b> đã cập nhật hạng mục <a>Thiết kế bộ 3D koisu</a> · trọng số 35%', t: '16:21', ic: ['ri-node-tree', '#d97706'] },
      { d: 'Hôm qua', w: 'Nguyễn Văn Hiếu', t: '16:35', x: '@{Đỗ Mai Anh} em lo phần bản vẽ lắp đặt nhé, thứ 6 gửi anh. #{T141}', rc: { '👍': ['Đặng Minh Khoa', 'Lê Quang Vinh'] } },
      { d: 'Hôm qua', sys: 'assign', o: 'T141', h: '<b>Nguyễn Văn Hiếu</b> đã giao nhiệm vụ {o} cho <b>Đỗ Mai Anh</b>', t: '16:35' },
      { d: 'Hôm qua', w: 'Nguyễn Văn Hiếu', t: '17:02', x: 'Bản vẽ hiện trạng cầu Gaochang, mọi người xem trước buổi họp tiến độ nhé.', f: [['Ban_ve_hien_trang_cau.pdf', 219136]], pin: 1 },
      { d: 'Hôm nay', w: 'Trịnh Đức Anh', t: '08:42', x: '@{Đặng Minh Khoa} khách báo cao độ mố cầu phía Bắc lệch so với hồ sơ cũ, mình đo lại chưa anh?', made: ['T118'] },
      { d: 'Hôm nay', sys: 'assign', o: 'T118', h: '<b>Đặng Minh Khoa</b> đã tạo nhiệm vụ {o} từ tin nhắn của <b>Trịnh Đức Anh</b>', t: '08:49', card: 1 },
      { d: 'Hôm nay', w: 'Đặng Minh Khoa', t: '08:50', x: 'Anh đang làm rồi em, chờ bên Gaochang mở rào công trường.', re: 5 },
      { d: 'Hôm nay', w: 'Phạm Thu Hà', t: '09:05', x: 'Em xuất xong BOM thép hình bản V1, gửi file và ảnh mẫu thép. @{Đỗ Mai Anh} duyệt giúp em nhé #{T155}', f: [['BOM_thep_hinh_V1.xlsx', 86016], ['Anh_mau_thep_I250.jpg', 640000, svgImg('Anh_mau_thep_I250.jpg', '#64748b', '#0ea5e9', 'shelf')]] },
      { d: 'Hôm nay', sys: 'submit', o: 'T155', h: '<b>Phạm Thu Hà</b> đã báo hoàn thành nhiệm vụ {o} · chờ <b>Đỗ Mai Anh</b> duyệt', t: '09:06' },
      { d: 'Hôm nay', w: ME, t: '09:12', x: 'Cảm ơn chị Hà. Trụ T3 có đường điện ngầm chưa có trong hồ sơ, em báo vấn đề luôn: #{I07}', seen: 6 },
      { d: 'Hôm nay', sys: 'assign', o: 'I07', h: 'Vấn đề {o} đã phân công cho <b>Phạm Thu Hà</b>', t: '09:13' },
      { d: 'Hôm nay', w: 'Trịnh Đức Anh', t: '09:30', x: 'Phần báo giá anh làm bên không gian Tiền khả thi DA010 rồi nhé: #{TX}' },
      { d: 'Hôm nay', sys: 'done', o: 'T127', h: 'Nhiệm vụ {o} đã <b>hoàn thành</b> · <b>Nguyễn Văn Hiếu</b> duyệt', t: '09:35' },
      { d: 'Hôm nay', w: 'Hoàng Minh Tâm', t: '09:41', x: 'Bản vẽ koisu thiếu kích thước chân đế, em đang bổ sung, chiều xong. #{I09}', rc: { '🙏': ['Nguyễn Văn Hiếu'] }, unread: 1 },
      { d: 'Hôm nay', w: 'Nguyễn Văn Hiếu', t: '09:44', x: '@{all} 14h chiều nay họp tiến độ GP40 ở phòng họp 1 nhé.', pin: 1 }
    ]
  } : """
CHAT_DEMO = [
    ("'Phạm Quốc Huy báo đã xử lý vấn đề máy chấm công'", "'Phạm Thu Hà báo đã xử lý vấn đề đường điện ngầm trụ T3'"),
    ("typing('Phạm Quốc Huy', 1400", "typing('Phạm Thu Hà', 1400"),
    ("'<b>Phạm Quốc Huy</b> đã xử lý xong vấn đề {o}", "'<b>Phạm Thu Hà</b> đã xử lý xong vấn đề {o}"),
    ("addMsg({ w: 'Phạm Quốc Huy', segs: ['Em thay đầu đọc vân tay rồi, chị thử lại giúp em nhé.'] })", "addMsg({ w: 'Phạm Thu Hà', segs: ['Chị làm việc với điện lực rồi, đường điện ngầm dời sang phải trụ T3, em kiểm tra lại giúp chị nhé.'] })"),
    ("'Nguyễn Thị Hằng giao việc mới cho bạn'", "'Nguyễn Văn Hiếu giao việc mới cho bạn'"),
    ("typing('Nguyễn Thị Hằng', 1400", "typing('Nguyễn Văn Hiếu', 1400"),
    ("code: 'TPE.TASK.NB.26.0170', n: 'Lập kế hoạch khám sức khoẻ định kỳ 2027', st: 'Chờ bắt đầu', as: ME, ap: 'Nguyễn Thị Hằng'", "code: 'TPE.TASK.GP.26.0170', n: 'Lập dự toán lắp đặt bộ 3D koisu', st: 'Chờ bắt đầu', as: ME, ap: 'Nguyễn Văn Hiếu'"),
    ("addMsg({ w: 'Nguyễn Thị Hằng', segs: [{ m: ME }, ' em lên kế hoạch khám sức khoẻ năm sau giúp chị nhé '] })", "addMsg({ w: 'Nguyễn Văn Hiếu', segs: [{ m: ME }, ' em lập dự toán lắp đặt giúp anh nhé '] })"),
    ("'<b>Nguyễn Thị Hằng</b> đã giao nhiệm vụ {o} cho <b>bạn</b>'", "'<b>Nguyễn Văn Hiếu</b> đã giao nhiệm vụ {o} cho <b>bạn</b>'"),
    ("'Lê Thu Trang báo hoàn thành “Gia hạn hợp đồng vệ sinh”'", "'Đặng Minh Khoa báo hoàn thành “Đo lại cao độ mố cầu”'"),
    ("'<b>Lê Thu Trang</b> đã báo hoàn thành nhiệm vụ {o} · chờ <b>Nguyễn Thị Hằng</b> duyệt'", "'<b>Đặng Minh Khoa</b> đã báo hoàn thành nhiệm vụ {o} · chờ <b>Nguyễn Văn Hiếu</b> duyệt'"),
    ("'<b>Nguyễn Thị Hằng</b> đã duyệt kết quả · nhiệm vụ {o} <b>hoàn thành</b>'", "'<b>Nguyễn Văn Hiếu</b> đã duyệt kết quả · nhiệm vụ {o} <b>hoàn thành</b>'"),
    ("'Ngô Đức Thịnh vào phòng (đồng bộ phòng ban)'", "'Ngô Đức Thịnh được thêm vào giải pháp'"),
    ("'<b>Ngô Đức Thịnh</b> đã vào phòng · đồng bộ từ phòng ban Nhân Sự Hành Chính'", "'<b>Nguyễn Văn Hiếu</b> đã thêm <b>Ngô Đức Thịnh</b> vào giải pháp · hạng mục Kết cấu chân đế'"),
    ("var w = room ? 'Bùi Thanh Tâm' : 'Lê Thu Trang';", "var w = room ? 'Lê Quang Vinh' : 'Lê Thu Trang';"),
    ("' chị ơi file này em cần ký trước 16h nhé'", "' chị ơi bản vẽ này em cần chốt trước 16h nhé'"),
    ("(D.kin ? 'dự án' : 'phòng')", "(D.kin ? 'dự án' : (SP === 'gp' ? 'giải pháp' : 'phòng'))"),
    ("'Gồm đồng bộ theo phòng ban'", "'Gồm thêm / bớt thành viên giải pháp'"),
]

def chrome2(s, active, title):
    """như chrome() nhưng đặt active được cả nút Trao đổi (class mk-chat-btn)"""
    s = re.sub(r'<title>.*?</title>', '<title>' + title + '</title>', s, count=1)
    i = s.find('<div class="mk-ntb"'); s = s[:i] + GP_NTB + s[balanced(s, i):]
    a, b = seg(s, '<div data-v-b87c17de="" data-v-efc08788="" class="tabs-nav">', '<!--/mk-tabs-->')
    t = re.sub(r'(tab-btn-root[^"]*?) active" data-key="', r'\1" data-key="', GP_TABS)
    t, n = re.subn(r'(tab-btn-root[^"]*?)" data-key="%s"' % active, r'\1 active" data-key="%s"' % active, t, count=1); assert n == 1, active
    s = s[:a] + t + s[b:]
    s = s.replace('mk-pin on" data-id="room-hc"', 'mk-pin" data-id="room-hc"').replace('mk-pin" data-id="gp40"', 'mk-pin on" data-id="gp40"')
    s = s.replace('class="mk-wr on" data-id="room-hc"', 'class="mk-wr" data-id="room-hc"').replace('class="mk-wr" data-id="gp40"', 'class="mk-wr on" data-id="gp40"')
    return s

def build_all():
    for src, dst, act, title, pairs in JOBS:
        s = open(S + src + '.html', encoding='utf-8', newline='').read()
        s = chrome2(s, act, title)
        # dữ liệu demo chỉ dành cho Phòng (dòng .mk-room-only + khối /*ROOM-EXTRA*/) — GP40 không lấy
        s = re.sub(r'<tr [^>]*class="mk-room-only">.*?</tr>', '', s, flags=re.S)
        s = re.sub(r'    /\*ROOM-EXTRA\*/.*?/\*/ROOM-EXTRA\*/\n', '', s, flags=re.S)
        s = s.replace('Hiển thị 1–22 / 22', 'Hiển thị 1–6 / 6')
        if pairs: s = subst(s, pairs)
        if dst in ('25-gp-nhiem-vu', '26-gp-van-de'):
            i = s.find('var DETAIL = {'); j = s.find('\n  };', i) + len('\n  };'); assert i > 0
            s = s[:i] + GP_DETAIL + s[j:]
        if dst == '29-gp-trao-doi':
            s = s.replace('window.__CX_SPACE="room";', 'window.__CX_SPACE="gp";', 1)
            k = "  var D = SP === 'iproj' ? {"; assert k in s
            s = s.replace(k, "  var D = " + GP_CHAT + "SP === 'iproj' ? {", 1)
            for x, y in CHAT_DEMO:
                assert x in s, x[:50]
                s = s.replace(x, y, 1) if "D.kin ? 'dự án' : 'phòng'" not in x else s.replace(x, y)
        open(S + dst + '.html', 'w', encoding='utf-8', newline='').write(s)
        print('built', dst, len(s))

# ================= bước 3: Cấu hình GP40 (từ 21) =================
CFG = [
    ('Tên phòng làm việc', 'Tên giải pháp'), ('Lấy theo tên phòng ban, không sửa được.', 'Lấy theo Giải pháp GP40, sửa ở màn Thông tin giải pháp.'),
    ('tự đổi theo khi phòng ban đổi tên', 'tự đổi theo khi giải pháp đổi tên'),
    ('Phòng Nhân Sự Hành Chính', 'GP40 - Tính toán lại khoảng cách lắp bộ 3D koisu với cầu Gaochang'),
    ('Phạm vi công việc của phòng.', 'Phạm vi của giải pháp.'), ('placeholder="Phạm vi công việc của phòng"', 'placeholder="Phạm vi của giải pháp"'),
    ('Hành chính, mua sắm, tài sản, sự kiện nội bộ của văn phòng Hà Nội.', 'Tính toán lại khoảng cách lắp bộ 3D koisu cho cầu Gaochang theo yêu cầu điều chỉnh của khách; gồm 4 hạng mục.'),
    ('<b>Theo phòng ban</b> · PHÒNG NHÂN SỰ HÀNH CHÍNH', '<b>Theo phân công giải pháp</b> · PM + nhân sự hạng mục'),
    ('18 nhân sự · tự đồng bộ', '6 nhân sự đồng bộ theo phân công · + 1 kinh doanh (Xem)'),
    ('Trưởng / phó phòng ban luôn là Quản lý, không gỡ được.', 'PM làm giải pháp luôn là Quản lý, không gỡ được.'),
    ('21410105 - Nguyễn Thị Hằng (Trưởng phòng ban)', '21410621 - Nguyễn Văn Hiếu (PM làm giải pháp)'),
    ('21410133 - Trần Văn Minh (Phó phòng ban)', '21410177 - Đặng Minh Khoa (Trưởng hạng mục)'),
    ('Tạo Dự án nội bộ thuộc phòng', 'Nhận vấn đề từ đội kinh doanh'),
    ('Quản lý phòng luôn xem được mọi dự án thuộc phòng.', 'Đội kinh doanh của Tiền khả thi DA010 gửi vấn đề sang; người gửi chỉ xem vấn đề mình gửi.'),
    ('for="mkq20">Chỉ Quản lý</label>', 'for="mkq20">Nhận</label>'), ('for="mkq21">Quản lý và Thành viên</label>', 'for="mkq21">Không nhận</label>'),
    ('Sự kiện nào tự gửi tin hệ thống vào nhóm chat của phòng. Việc của Dự án nội bộ Kín không báo ra chat phòng.', 'Sự kiện nào tự gửi tin hệ thống vào nhóm chat của giải pháp.'),
    ('Thành viên &amp; dự án', 'Thành viên &amp; hạng mục'), ('Dự án nội bộ mới / đóng', 'Hạng mục mới / đổi trọng số'),
    ('Lưu trữ phòng làm việc', 'Lưu trữ giải pháp'),
    ('Chuyển vào mục Lưu trữ: chỉ đọc, không nhận việc / tin mới. Mở lại được.', 'Tự lưu trữ khi giải pháp đóng hoặc huỷ: chỉ đọc, không nhận việc / tin mới.'),
] + COMMON

def build_cfg():
    s = open(S + '21-phong-cau-hinh.html', encoding='utf-8', newline='').read()
    s = chrome2(s, 'more', 'Dự án KH · Giải pháp · Cấu hình')
    # nút "Thêm" hiển thị thành "Cấu hình" (khuôn của màn 21 / 23 / 09)
    a, b = seg(s, '<div data-v-b87c17de="" data-v-efc08788="" class="tabs-nav">', '<!--/mk-tabs-->')
    t = s[a:b]; k = t.find('data-key="more"')
    t2 = t[k:].replace('ri-apps-2-line tab-icon', 'ri-settings-3-line tab-icon', 1).replace('class="tab-label">Thêm</span>', 'class="tab-label">Cấu hình</span>', 1)
    s = s[:a] + t[:k] + t2 + s[b:]
    for x, y in CFG[:21]:
        c0 = s.find('class="content-page"'); e0 = s.find('mk-sb-host')
        assert x in s[c0:e0], x
    s = subst(s, CFG)
    open(S + '30-gp-cau-hinh.html', 'w', encoding='utf-8', newline='').write(s)
    print('built 30-gp-cau-hinh', len(s))

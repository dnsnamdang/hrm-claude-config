// 10/11 [U] §4.6 — Chat cá nhân 1–1, bố cục tham khảo Zalo PC (user 10/11: "tham khảo zalo để làm cho chuẩn"), giữ màu / component phần mềm.
// Tab Trao đổi: cột Hội thoại (chat nhóm + nhắn riêng thành viên) · Màn Tin nhắn (window.__DM_HUB): mọi hội thoại, xếp theo tin mới nhất.
// Nhắn được mọi NV đang làm việc của mọi công ty (Danh bạ). Chat 1–1 với A là 1 luồng duy nhất.
(function () {
  // 10/11 [U] phương án 1: tab nằm TRONG hội thoại — mọi màn nhóm có cột hội thoại chung bên trái (window.__DM_LISTONLY), khung phải = đầu nhóm + tab của nhóm.
  var LIST = !!window.__DM_LISTONLY, wrap = document.querySelector('.cx-wrap'); if (!LIST && !wrap) return;
  var HUB = !!window.__DM_HUB, ALL = HUB || LIST, SPK = window.__CX_SPACE || 'room', ME = 'Đỗ Mai Anh';
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var PAL = ['#f472b6', '#60a5fa', '#fbbf24', '#34d399', '#a78bfa', '#f87171', '#2dd4bf', '#fb923c', '#818cf8'];
  function avc(n) { var h = 0; for (var i = 0; i < n.length; i++) h = (h * 31 + n.charCodeAt(i)) >>> 0; return PAL[h % PAL.length]; }
  function ini(n) { var p = n.trim().split(/\s+/); return ((p[p.length - 2] ? p[p.length - 2][0] : '') + p[p.length - 1][0]).toUpperCase(); }
  function nrm(s) { return String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[đĐ]/g, 'd').toLowerCase(); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function now() { var d = new Date(); return pad(d.getHours()) + ':' + pad(d.getMinutes()); }
  function av(n, on, sz) { return '<span class="dm-av' + (sz ? ' ' + sz : '') + '" style="background:' + avc(n) + '">' + esc(ini(n)) + (on ? '<i class="on"></i>' : '') + '</span>'; }
  function gav(s) { if (s.kh) return '<span class="dm-av grp kh"><i class="' + (s.ic || 'ri-briefcase-4-line') + '"></i></span>'; return '<span class="dm-av mos">' + s.mem.slice(0, 4).map(function (n) { return '<i style="background:' + avc(n) + '">' + esc(ini(n)[0]) + '</i>'; }).join('') + '</span>'; }
  function toast(m) { var t = document.querySelector('.mk-p-toast'); if (!t) { t = document.createElement('div'); t.className = 'mk-p-toast'; document.body.appendChild(t); } t.innerHTML = m; t.classList.add('on'); clearTimeout(t._t); t._t = setTimeout(function () { t.classList.remove('on'); }, 2200); }

  // ---- dữ liệu mô phỏng ----
  var P = {
    'Nguyễn Thị Hằng': ['HN_NSHC', '21410105', 1], 'Trần Văn Minh': ['HN_NSHC', '21410133', 1], 'Lê Thu Trang': ['HN_NSHC', '21410210', 0],
    'Phạm Quốc Huy': ['HN_NSHC', '21410288', 1], 'Vũ Hoàng Long': ['HN_NSHC', '21410322', 1], 'Bùi Thanh Tâm': ['HN_NSHC', '21410340', 0],
    'Đặng Minh Khoa': ['HN_KTCN', '21410177', 1], 'Trịnh Đức Anh': ['HN_KD1', '21410550', 0], 'Phạm Văn Tú': ['HN_QTTT', '21410402', 1],
    'Nguyễn Văn Hiếu': ['HN_KTCN', '21410621', 1], 'Hoàng Thị Lan': ['HN_KT', '21410415', 0], 'Ngô Quang Vinh': ['HN_KD2', '21410588', 1],
    'Lâm Thị Ngọc': ['HCM_KD1', '31420118', 1, 'Tân Phát HCM'], 'Trương Văn Phúc': ['HCM_KT', '31420207', 0, 'Tân Phát HCM'], 'Huỳnh Minh Tâm': ['HCM_KTCN', '31420311', 1, 'Tân Phát HCM']
  };
  var CO = 'Tân Phát'; function coOf(n) { return (P[n] && P[n][3]) || CO; }
  var DEPN = { HN_NSHC: 'Phòng Nhân sự Hành chính', HN_KTCN: 'Phòng Kỹ thuật công nghệ', HN_KD1: 'Phòng Kinh doanh 1', HN_KD2: 'Phòng Kinh doanh 2', HN_QTTT: 'Phòng Quản trị thông tin', HN_KT: 'Phòng Kế toán', HCM_KD1: 'Phòng Kinh doanh 1 (HCM)', HCM_KT: 'Phòng Kế toán (HCM)', HCM_KTCN: 'Phòng Kỹ thuật (HCM)' };
  var SP = {
    room: { n: 'Phòng Nhân Sự Hành Chính', s: 'Nhóm trao đổi · 18 thành viên', un: 12, href: '04-phong-trao-doi.html', last: 'Trần Văn Minh: @Tất cả 14h chiều nay họp giao ban…', t: '10:05', o: 1005, pin: 1,
      mem: ['Nguyễn Thị Hằng', 'Trần Văn Minh', 'Lê Thu Trang', 'Phạm Quốc Huy', 'Vũ Hoàng Long', 'Bùi Thanh Tâm'] },
    iproj: { n: 'Tổ chức hội nghị công đoàn 2027', s: 'Nhóm trao đổi · hạn 20/01/2027', un: 2, href: '08-du-an-noi-bo-kin-trao-doi.html', last: 'Vũ Hoàng Long: Hội trường tầng 5 trùng lịch…', t: '09:12', o: 912,
      mem: ['Trần Văn Minh', 'Lê Thu Trang', 'Vũ Hoàng Long', 'Nguyễn Thị Hằng'] },
    tkt: { n: 'DA010 - Tính toán lại khoảng cách lắp bộ 3D koisu với cầu Gaochang', s: 'Dự án KH · Tiền khả thi', kh: 1, ic: 'ri-briefcase-4-line', un: 3, href: '10-tkt-van-de.html', last: 'Trịnh Đức Anh: Khách hẹn khảo sát lại thứ Sáu', t: 'Hôm qua', o: 450,
      mem: ['Trịnh Đức Anh', 'Phạm Văn Tú', 'Ngô Quang Vinh'] },
    gp: { n: 'GP40 - Tính toán lại khoảng cách lắp bộ 3D koisu', s: 'Dự án KH · Giải pháp', kh: 1, ic: 'ri-lightbulb-flash-line', un: 6, href: '29-gp-trao-doi.html', last: 'Phạm Văn Tú: Đã cập nhật bảng tính tải trọng', t: 'Hôm qua', o: 500, mute: 1,
      mem: ['Phạm Văn Tú', 'Đặng Minh Khoa', 'Nguyễn Văn Hiếu', 'Trịnh Đức Anh'] }
  };
  // 10/11 đang mở chat của chính nhóm này ⇒ coi như đã đọc: đầu nhóm + dòng nhóm trong danh sách không còn số chưa đọc
  if (LIST) { var a0 = document.querySelector('.surface-hd .tabs-root .tab-btn-root.active'); if (!a0 || a0.getAttribute('data-key') === 'chat') SP[SPK].un = 0; }
  // tin: [người, nội dung, giờ, thẻ?, 'file'?] · ['d', ngày]
  var DM = {
    'Lê Thu Trang': { un: 2, t: '08:52', o: 852, pin: 1, m: [['d', 'Hôm qua'], ['Lê Thu Trang', 'Chị Mai Anh ơi, em gửi bản dự trù kinh phí hội nghị rồi ạ.', '17:20'], [ME, 'Ok em, sáng mai chị xem.', '17:31'],
      ['d', 'Hôm nay'], ['Lê Thu Trang', 'Chị xem giúp em dự trù kinh phí trước 10h nhé, anh Minh cần chốt để đặt cọc hội trường.', '08:50', ['t', 'Dự trù kinh phí hội nghị', 'Hoàn thành - Chờ duyệt', '#D97706', 'Duyệt: Đỗ Mai Anh · Hạn 05/11']], ['Lê Thu Trang', 'Em để file chi tiết trong nhiệm vụ rồi ạ 🙏', '08:51'], ['Lê Thu Trang', '📎 Du_tru_kinh_phi_HN2027.xlsx · 48 KB', '08:52', null, 'file']], pinned: 'Chị xem giúp em dự trù kinh phí trước 10h nhé…', pinnedFrom: 'Lê Thu Trang' },
    'Nguyễn Thị Hằng': { un: 1, t: '09:40', o: 940, m: [['d', 'Hôm nay'], ['Nguyễn Thị Hằng', 'Chiều nay em qua phòng chị ký biên bản bàn giao tài sản nhé.', '09:40']] },
    'Trần Văn Minh': { un: 0, t: 'Hôm qua', o: 400, m: [['d', 'Hôm qua'], ['Trần Văn Minh', 'Backdrop bản 1 chữ hơi nhỏ, em chỉnh lại giúp anh.', '15:02'], [ME, 'Dạ em gửi backdrop bản 2 rồi ạ.', '16:40']] },
    'Đặng Minh Khoa': { un: 0, t: '07/11', o: 300, m: [['d', '07/11/2026'], [ME, 'Anh Khoa ơi, anh hỗ trợ em cài máy chiếu hội trường tầng 5 hôm 15/01 được không ạ?', '10:12'], ['Đặng Minh Khoa', 'Ok em, gần ngày nhắc anh nhé.', '10:30']] },
    'Lâm Thị Ngọc': { un: 0, t: '05/11', o: 200, m: [['d', '05/11/2026'], ['Lâm Thị Ngọc', 'Chị Mai Anh ơi, bên HCM xin mẫu quy chế khen thưởng công đoàn năm nay với ạ.', '14:05'], [ME, 'Chị gửi em qua mail rồi nhé.', '14:20']] }
  };
  var qs = /[?&]to=([^&]+)/.exec(location.search);
  var cur = (qs && decodeURIComponent(qs[1])) || window.__DM_OPEN || null, flt = 'all', info = false, replyTo = null;

  // ---- khung ----
  var col = document.createElement('div'); col.className = 'dm-col';
  col.innerHTML = '<div class="dm-col-hd"><button type="button" class="dm-ib dm-mini-b" data-mini="1" title="Thu gọn / mở rộng danh sách hội thoại"><i class="ri-side-bar-line"></i></button><div class="dm-q"><i class="ri-search-line"></i><input placeholder="Tìm kiếm"></div>' +
    '<button type="button" class="dm-ib" data-new="1" title="Tin nhắn mới — chọn người trong Danh bạ (mọi công ty)"><i class="ri-chat-new-line"></i></button>' +
    '<button type="button" class="dm-ib" data-grp="1" title="Tạo nhóm chat"><i class="ri-group-line"></i></button></div>' +
    '<div class="dm-flt">' + [['all', 'Tất cả'], ['un', 'Chưa đọc'], ['grp', 'Nhóm'], ['dm', 'Cá nhân']].map(function (f) { return '<span data-f="' + f[0] + '" class="' + (f[0] === 'all' ? 'on' : '') + '">' + f[1] + '</span>'; }).join('') + '</div>' +
    '<div class="dm-ls"></div>';
  if (LIST) { var surf = document.querySelector('.surface.main-wrap'), row = document.createElement('div'); row.className = 'ws-row'; surf.parentElement.insertBefore(row, surf); row.appendChild(col); row.appendChild(surf); col.classList.add('ws-list'); }
  else wrap.insertBefore(col, wrap.firstChild);
  try { if (localStorage.getItem('dm-mini') === '1') col.classList.add('mini'); } catch (e) {}
  var pane = document.createElement('div'); pane.className = 'dm-pane';
  var side = document.createElement('div'); side.className = 'dm-info';
  if (!LIST) { wrap.appendChild(pane); wrap.appendChild(side); }
  var ls = col.querySelector('.dm-ls'), q = col.querySelector('.dm-q input');
  var menu = document.createElement('div'); menu.className = 'dm-menu'; document.body.appendChild(menu);
  function closeMenu() { menu.classList.remove('on'); }
  document.addEventListener('mousedown', function (e) { if (!menu.contains(e.target)) closeMenu(); if (!e.target.closest('.dm-tools, .dm-dot, .dm-menu')) [].forEach.call(document.querySelectorAll('.dm-tools.keep'), function (x) { x.classList.remove('keep'); x.closest('.dm-row').classList.remove('tools-on'); }); });

  // ---- danh sách hội thoại ----
  function realMsgs(n) { return DM[n] ? DM[n].m.filter(function (x) { return x[0] !== 'd'; }) : []; }
  function lastOf(n) { var m = realMsgs(n).pop(); if (!m) return null; return (m[0] === ME ? 'Bạn: ' : '') + (m.rec ? 'Tin nhắn đã thu hồi' : m[1]); }
  function talked() { return Object.keys(DM).filter(function (n) { return realMsgs(n).length || n === cur; }); }
  function convs() {
    var L = [];
    if (ALL) Object.keys(SP).forEach(function (g) { L.push({ g: g, o: SP[g].o, pin: SP[g].pin }); });
    else L.push({ g: SPK, o: 9999, pin: 1, here: 1 });
    var people = ALL ? talked() : SP[SPK].mem.filter(function (n) { return n !== ME; }).concat(talked().filter(function (n) { return SP[SPK].mem.indexOf(n) < 0; }));
    people.forEach(function (n) { L.push({ p: n, o: DM[n] ? DM[n].o : 0, pin: DM[n] && DM[n].pin }); });
    return L.sort(function (a, b) { return (b.pin ? 1 : 0) - (a.pin ? 1 : 0) || b.o - a.o; });
  }
  function itHtml(c) {
    if (c.g) {
      var s = SP[c.g], on = LIST ? c.g === SPK : (!cur && !HUB);
      return '<div class="dm-it' + (on ? ' on' : '') + (s.un ? ' un' : '') + '" data-g="' + c.g + '">' + gav(s) +
        '<div class="dm-tx"><div class="dm-nm"><span>' + esc(s.n) + '</span><em>' + esc(s.t) + '</em></div><div class="dm-last"><span>' + esc(c.here ? 'Chat của nhóm này · ' + s.s.split(' · ')[1] : s.last) + '</span>' +
        (s.mute ? '<i class="ri-notification-off-line dm-mute" title="Đã tắt thông báo"></i>' : '') + (c.pin && !c.here ? '<i class="ri-pushpin-2-fill dm-pin" title="Đã ghim"></i>' : '') + (s.un ? '<b class="dm-n' + (s.mute ? ' mute' : '') + '">' + (s.un > 99 ? '99+' : s.un) + '</b>' : '') + '</div></div>' +
        '<button class="dm-more" data-m="g:' + c.g + '" title="Thêm"><i class="ri-more-fill"></i></button></div>';
    }
    var n = c.p, p = P[n] || ['', '', 0], d = DM[n], last = lastOf(n);
    return '<div class="dm-it' + (cur === n ? ' on' : '') + (d && d.un ? ' un' : '') + '" data-p="' + esc(n) + '">' + av(n, p[2], 'l') +
      '<div class="dm-tx"><div class="dm-nm"><span>' + esc(n) + '</span>' + (coOf(n) !== CO ? '<span class="dm-tag co">' + esc(coOf(n)) + '</span>' : '') + (d && realMsgs(n).length ? '<em>' + esc(d.t) + '</em>' : '') + '</div>' +
      '<div class="dm-last"><span>' + esc(last || (p[2] ? 'Đang hoạt động · bấm để nhắn' : DEPN[p[0]] || p[0])) + '</span>' +
      (d && d.mute ? '<i class="ri-notification-off-line dm-mute"></i>' : '') + (d && d.pin ? '<i class="ri-pushpin-2-fill dm-pin" title="Đã ghim"></i>' : '') + (d && d.un ? '<b class="dm-n">' + d.un + '</b>' : '') + '</div></div>' +
      '<button class="dm-more" data-m="p:' + esc(n) + '" title="Thêm"><i class="ri-more-fill"></i></button></div>';
  }
  function render() {
    var k = nrm(q.value.trim()), h = '';
    if (k) {
      var all = Object.keys(P).filter(function (n) { return n !== ME && nrm(n + ' ' + P[n][0] + ' ' + P[n][1]).indexOf(k) >= 0; });
      var grps = Object.keys(SP).filter(function (g) { return nrm(SP[g].n).indexOf(k) >= 0; });
      var inG = HUB ? [] : all.filter(function (n) { return SP[SPK].mem.indexOf(n) >= 0; }), rest = all.filter(function (n) { return inG.indexOf(n) < 0; });
      var same = rest.filter(function (n) { return coOf(n) === CO; }), other = rest.filter(function (n) { return coOf(n) !== CO; });
      if (grps.length) h += '<div class="dm-sec">Nhóm</div>' + grps.map(function (g) { return itHtml({ g: g }); }).join('');
      if (inG.length) h += '<div class="dm-sec">Thành viên nhóm</div>' + inG.map(function (n) { return itHtml({ p: n }); }).join('');
      if (same.length) h += '<div class="dm-sec">Cùng công ty<small>' + CO + '</small></div>' + same.map(function (n) { return itHtml({ p: n }); }).join('');
      if (other.length) h += '<div class="dm-sec">Công ty khác</div>' + other.map(function (n) { return itHtml({ p: n }); }).join('');
      if (!h) h = '<div class="dm-empty">Không tìm thấy. Thử <a class="mk-link" data-new="1" style="cursor:pointer">mở Danh bạ</a>.</div>';
    } else {
      var L = convs().filter(function (c) {
        if (flt === 'grp') return !!c.g; if (flt === 'dm') return !!c.p;
        if (flt === 'un') return c.g ? SP[c.g].un : DM[c.p] && DM[c.p].un; return true;
      });
      // 10/11 [U] "phân chia rõ khu vực ghim và khu vực phía dưới": hội thoại đã ghim gom vào 1 khối nền xám nhạt có tiêu đề + vạch ngăn
      var PZ = L.filter(function (c) { return c.pin && !c.here; });
      L = L.filter(function (c) { return PZ.indexOf(c) < 0; });
      if (PZ.length) h = '<div class="dm-pinz"><div class="dm-sec"><span><i class="ri-pushpin-2-fill"></i>Đã ghim</span><small>' + PZ.length + '</small></div>' + PZ.map(itHtml).join('') + '</div>';
      if (!ALL && flt === 'all') {
        var g = L.filter(function (c) { return c.g; }), p = L.filter(function (c) { return c.p; });
        h += (PZ.length && g.length ? '<div class="dm-sec">Nhóm này</div>' : '') + g.map(itHtml).join('') + (p.length ? '<div class="dm-sec">Nhắn riêng<small>thành viên nhóm + người đã nhắn</small></div>' + p.map(itHtml).join('') : '');
      } else h += L.length ? (PZ.length ? '<div class="dm-sec">' + (flt === 'un' ? 'Chưa đọc' : flt === 'grp' ? 'Nhóm' : flt === 'dm' ? 'Cá nhân' : 'Tất cả hội thoại') + '<small>' + L.length + '</small></div>' : '') + L.map(itHtml).join('') : (PZ.length ? '' : '<div class="dm-empty">Không có hội thoại ' + (flt === 'un' ? 'chưa đọc' : '') + '.</div>');
    }
    ls.innerHTML = h;
    var tot = Object.keys(DM).reduce(function (s, n) { return s + (DM[n].un || 0); }, 0) + (ALL ? Object.keys(SP).reduce(function (s, g) { return s + (SP[g].mute ? 0 : SP[g].un); }, 0) : 0);
    col.querySelector('[data-f="un"]').innerHTML = 'Chưa đọc' + (tot ? ' <b>' + tot + '</b>' : '');
  }

  // ---- khung chat 1–1 ----
  function cardHtml(c) { return '<div class="dm-card"><i class="' + (c[0] === 't' ? 'ri-task-line' : 'ri-bug-line') + '"></i><div><b>' + esc(c[1]) + '</b><span class="mk-badge" style="--c:' + c[3] + '">' + esc(c[2]) + '</span><small>' + esc(c[4]) + '</small></div></div>'; }
  function bodyHtml(n) {
    var M = DM[n].m, h = '', p = P[n] || ['', '', 0];
    if (!M.length) return '<div class="dm-hello">' + av(n, p[2], 'xl') + '<b>' + esc(n) + '</b><span>' + esc(DEPN[p[0]] || p[0]) + ' · ' + esc(coOf(n)) + '</span><small>Chưa có tin nhắn. Gửi lời chào để bắt đầu — chỉ bạn và ' + esc(n) + ' thấy cuộc trò chuyện này.</small><div class="dm-hi">' + ['Chào ' + n.split(' ').pop() + ' 👋', 'Bạn rảnh trao đổi chút không?'].map(function (x) { return '<span data-hi="' + esc(x) + '">' + esc(x) + '</span>'; }).join('') + '</div></div>';
    var lastMine = -1; M.forEach(function (m, i) { if (m[0] === ME) lastMine = i; });
    M.forEach(function (m, i) {
      if (m[0] === 'd') { h += '<div class="dm-day"><span>' + esc(m[1]) + '</span></div>'; return; }
      var prev = M[i - 1], next = M[i + 1], first = !prev || prev[0] !== m[0], lastG = !next || next[0] !== m[0], me = m[0] === ME;
      h += '<div class="dm-row' + (me ? ' me' : '') + (first ? ' first' : '') + '" data-i="' + i + '">' + (me ? '' : (first ? av(m[0], 0) : '<span class="dm-av sp"></span>')) +
        '<div class="dm-m">' + (m.rep ? '<div class="dm-quote"><b>' + esc(m.rep[0] === ME ? 'Bạn' : m.rep[0]) + '</b>' + esc(m.rep[1]) + '</div>' : '') +
        '<div class="bb' + (m[4] === 'file' ? ' file' : '') + (m.rec ? ' rec' : '') + '">' + (m.rec ? '<i>Tin nhắn đã thu hồi</i>' : (m[4] === 'file' ? '<i class="ri-file-excel-2-line"></i>' + esc(m[1].replace('📎 ', '')) : esc(m[1]))) +
        (m[3] && !m.rec ? cardHtml(m[3]) : '') + (lastG ? '<span class="tm">' + esc(m[2]) + '</span>' : '') + '</div>' +
        (m.rc ? '<span class="dm-rc">' + m.rc + ' 1</span>' : '') +
        (!m.rec ? '<button class="dm-dot' + (me ? ' l' : '') + '" data-t="dot" title="Thao tác"><i class="ri-more-fill"></i></button><div class="dm-tools' + (me ? ' l' : '') + '"><button data-t="rep" title="Trả lời"><i class="ri-reply-line"></i></button><button data-t="rc" title="Thả cảm xúc">👍</button><button data-t="more" title="Thêm"><i class="ri-more-fill"></i></button></div>' : '') + '</div></div>';
      if (i === lastMine) h += '<div class="dm-seen">' + (DM[n].seen ? 'Đã xem ' + av(n, 0, 'xs') : 'Đã gửi') + '</div>';
    });
    return h;
  }
  function openDM(n) {
    if (LIST) { location.href = '31-tin-nhan.html?to=' + encodeURIComponent(n); return; }
    cur = n; replyTo = null; if (!DM[n]) DM[n] = { un: 0, t: '', o: 0, m: [] }; DM[n].un = 0; DM[n].seen = 1;
    var p = P[n] || ['', '', 0], d = DM[n];
    pane.innerHTML = '<div class="dm-hd">' + av(n, p[2], 'm') + '<div class="dm-hd-t"><b>' + esc(n) + '</b><small>' + (p[2] ? '<i></i>Đang hoạt động' : 'Truy cập 2 giờ trước') + ' · ' + esc((DEPN[p[0]] || p[0]) + (coOf(n) !== CO ? ' · ' + coOf(n) : '')) + '</small></div>' +
      '<div class="r"><button class="dm-ib" data-a="search" title="Tìm tin nhắn"><i class="ri-search-line"></i></button><button class="dm-ib" data-a="grp" title="Tạo nhóm chat với ' + esc(n) + '"><i class="ri-group-line"></i></button><button class="dm-ib' + (info ? ' on' : '') + '" data-a="info" title="Thông tin hội thoại"><i class="ri-layout-right-line"></i></button></div></div>' +
      // 10/11 thanh tin ghim + khung soạn tin dùng chung khuôn với chat nhóm (nền vàng nhạt · ô nhập trên, công cụ dưới)
      (d.pinned ? '<div class="dm-pinbar"><span class="bar"></span><i class="ri-pushpin-2-fill"></i><div class="tx"><b>' + esc(d.pinnedFrom === ME ? 'Bạn' : (d.pinnedFrom || n)) + ':</b> ' + esc(d.pinned) + '</div><button class="x" data-a="unpinmsg" title="Bỏ ghim tin này"><i class="ri-close-line"></i></button></div>' : '') +
      '<div class="dm-body">' + bodyHtml(n) + '</div><div class="dm-typing"></div>' +
      '<div class="dm-comp"><div class="dm-reply" hidden></div>' +
        '<div class="dm-inrow"><textarea rows="1" placeholder="Nhập tin nhắn tới ' + esc(n) + '… gõ # để chèn nhiệm vụ / vấn đề"></textarea></div>' +
        '<div class="dm-tb"><div class="ic"><button class="dm-ib" data-a="x" title="Gửi hình ảnh"><i class="ri-image-line"></i></button><button class="dm-ib" data-a="x" title="Đính kèm file"><i class="ri-attachment-2"></i></button>' +
        '<button class="dm-ib" data-a="x" title="Chèn nhiệm vụ / vấn đề" style="font-weight:700;font-size:15px">#</button><button class="dm-ib" data-a="x" title="Tạo nhiệm vụ giao cho ' + esc(n) + '"><i class="ri-task-line"></i></button><button class="dm-ib" data-a="x" title="Biểu cảm"><i class="ri-emotion-line"></i></button></div>' +
        '<button type="button" class="v2-btn v2-btn--sm v2-btn--primary v2-btn--primary-info v2-btn--prefix-sm" data-a="send"><div class="v2-btn__prefix--sm"><i class="ri-send-plane-2-line" style="margin-right:3px"></i></div> Gửi</button></div></div>';
    wrap.classList.add('dm-on'); wrap.classList.toggle('dm-info-on', info); renderInfo(); render();
    var b = pane.querySelector('.dm-body'); b.scrollTop = b.scrollHeight; pane.querySelector('textarea').focus();
  }
  function refreshBody() { var b = pane.querySelector('.dm-body'); b.innerHTML = bodyHtml(cur); b.scrollTop = b.scrollHeight; }
  function renderInfo() {
    if (!cur) { side.innerHTML = ''; return; }
    var n = cur, p = P[n] || ['', '', 0], d = DM[n];
    var cards = d.m.filter(function (m) { return m[3]; }), files = d.m.filter(function (m) { return m[4] === 'file'; });
    function sec(t, cnt, body, open) { return '<div class="dm-is' + (open ? ' on' : '') + '"><div class="dm-is-h" data-is="1">' + t + (cnt != null ? ' <small>' + cnt + '</small>' : '') + '<i class="ri-arrow-down-s-line"></i></div><div class="dm-is-b">' + body + '</div></div>'; }
    side.innerHTML = '<div class="dm-info-hd">Thông tin hội thoại</div><div class="dm-info-sc">' +
      '<div class="dm-prof">' + av(n, p[2], 'xl') + '<b>' + esc(n) + '</b><span>' + esc(n + ' - ' + p[0] + ' - ' + p[1]) + '</span><span>' + esc(coOf(n)) + '</span>' +
      '<div class="dm-acts"><button data-a="mute" class="' + (d.mute ? 'on' : '') + '"><i class="' + (d.mute ? 'ri-notification-off-line' : 'ri-notification-3-line') + '"></i>' + (d.mute ? 'Bật thông báo' : 'Tắt thông báo') + '</button>' +
      '<button data-a="pinconv" class="' + (d.pin ? 'on' : '') + '"><i class="ri-pushpin-2-line"></i>' + (d.pin ? 'Bỏ ghim' : 'Ghim hội thoại') + '</button><button data-a="grp"><i class="ri-group-line"></i>Tạo nhóm chat</button></div></div>' +
      sec('Tin nhắn đã ghim', d.pinned ? 1 : 0, d.pinned ? '<div class="dm-li"><i class="ri-pushpin-2-line"></i><span>' + esc(d.pinned) + '</span></div>' : '<div class="dm-none">Chưa có tin ghim</div>', 1) +
      sec('Nhiệm vụ / vấn đề được nhắc', cards.length, cards.length ? cards.map(function (m) { return '<div class="dm-li"><i class="ri-task-line"></i><span>' + esc(m[3][1]) + '<small>' + esc(m[3][2]) + '</small></span></div>'; }).join('') : '<div class="dm-none">Chưa có</div>', 1) +
      sec('Ảnh / Video', 0, '<div class="dm-none">Chưa có ảnh được chia sẻ</div>') +
      sec('File', files.length, files.length ? files.map(function (m) { return '<div class="dm-li"><i class="ri-file-excel-2-line" style="color:#16a34a"></i><span>' + esc(m[1].replace('📎 ', '')) + '<small>' + esc(m[0]) + ' · ' + esc(m[2]) + '</small></span></div>'; }).join('') : '<div class="dm-none">Chưa có file</div>', 1) +
      '<div class="dm-is"><div class="dm-danger" data-a="clear"><i class="ri-delete-bin-6-line"></i>Xoá lịch sử trò chuyện (chỉ phía bạn)</div></div></div>';
  }
  function closeDM() { cur = null; wrap.classList.remove('dm-on', 'dm-info-on'); render(); }
  function push(who, text, extra) {
    var c = DM[cur]; if (!c.m.some(function (x) { return x[0] === 'd' && x[1] === 'Hôm nay'; })) c.m.push(['d', 'Hôm nay']);
    var m = [who, text, now()]; if (extra) for (var k in extra) m[k] = extra[k]; c.m.push(m); c.t = now(); c.o = 2400; return m;
  }
  function send(text) {
    var ta = pane.querySelector('textarea'), v = (text || ta.value).trim(); if (!v || !cur) return;
    push(ME, v, replyTo ? { rep: replyTo } : null); ta.value = ''; ta.style.height = ''; setReply(null); DM[cur].seen = 0; refreshBody(); render(); renderInfo();
    var n = cur, ty = pane.querySelector('.dm-typing');
    setTimeout(function () { if (cur !== n) return; DM[n].seen = 1; refreshBody(); ty.innerHTML = '<span class="dots"><i></i><i></i><i></i></span>' + esc(n) + ' đang soạn tin…'; }, 900);
    setTimeout(function () { if (cur !== n) return; ty.innerHTML = ''; push(n, 'Dạ em nhận được rồi ạ, cảm ơn chị!'); refreshBody(); render(); }, 2600);
  }
  function setReply(m) {
    replyTo = m ? [m[0], m[1]] : null; var r = pane.querySelector('.dm-reply'); if (!r) return;
    r.hidden = !m; r.innerHTML = m ? '<i class="ri-reply-line"></i><div><b>Trả lời ' + esc(m[0] === ME ? 'chính bạn' : m[0]) + '</b><span>' + esc(m[1]) + '</span></div><button class="dm-ib" data-a="norep"><i class="ri-close-line"></i></button>' : '';
  }
  function showMenu(anchor, items, on) {
    menu.innerHTML = items.map(function (x) { return x === '-' ? '<hr>' : '<button data-v="' + x[2] + '"' + (x[3] ? ' class="dg"' : '') + '><i class="' + x[0] + '"></i>' + x[1] + '</button>'; }).join('');
    menu.classList.add('on'); var r = anchor.getBoundingClientRect(); menu.style.top = Math.min(innerHeight - menu.offsetHeight - 8, r.bottom + 4) + 'px'; menu.style.left = Math.max(8, Math.min(innerWidth - menu.offsetWidth - 8, r.right - menu.offsetWidth)) + 'px';
    menu.onclick = function (e) { var b = e.target.closest('[data-v]'); if (!b) return; closeMenu(); on(b.dataset.v); };
  }

  // ---- sự kiện ----
  ls.addEventListener('click', function (e) {
    var mb = e.target.closest('.dm-more');
    if (mb) {
      e.stopPropagation(); var key = mb.dataset.m, isG = key[0] === 'g', id = key.slice(2), o = isG ? SP[id] : (DM[id] = DM[id] || { un: 0, t: '', o: 0, m: [] });
      return showMenu(mb, [['ri-pushpin-2-line', o.pin ? 'Bỏ ghim hội thoại' : 'Ghim hội thoại', 'pin'], ['ri-mail-unread-line', o.un ? 'Đánh dấu đã đọc' : 'Đánh dấu chưa đọc', 'un'], [o.mute ? 'ri-notification-3-line' : 'ri-notification-off-line', o.mute ? 'Bật thông báo' : 'Tắt thông báo', 'mute']].concat(isG ? [] : ['-', ['ri-user-line', 'Xem thông tin', 'prof']]),
        function (v) { if (v === 'pin') o.pin = !o.pin; if (v === 'un') o.un = o.un ? 0 : 1; if (v === 'mute') o.mute = !o.mute; if (v === 'prof') { info = true; openDM(id); } render(); if (cur && !isG && id === cur) renderInfo(); });
    }
    var it = e.target.closest('.dm-it'); if (!it) return;
    if (it.dataset.g) { var tg = SP[it.dataset.g].href; if (LIST && location.pathname.indexOf(tg) >= 0) return; if (ALL || it.dataset.g !== SPK) { location.href = tg; return; } q.value = ''; closeDM(); return; }
    q.value = ''; openDM(it.dataset.p);
  });
  q.addEventListener('input', render);
  col.querySelector('.dm-flt').addEventListener('click', function (e) { var f = e.target.closest('[data-f]'); if (!f) return; flt = f.dataset.f; col.querySelectorAll('[data-f]').forEach(function (x) { x.classList.toggle('on', x === f); }); render(); });
  col.addEventListener('click', function (e) { if (e.target.closest('[data-mini]')) { var mi = col.classList.toggle('mini'); if (!col.classList.contains('auto')) { try { localStorage.setItem('dm-mini', mi ? '1' : '0'); } catch (x) {} } return; } if (e.target.closest('[data-new]')) bkShow(); if (e.target.closest('[data-grp]')) toast('<i class="ri-information-line"></i> Tạo nhóm chat tự lập: chọn nhiều người trong Danh bạ — làm ở giai đoạn sau'); });
  pane.addEventListener('click', function (e) {
    var hi = e.target.closest('[data-hi]'); if (hi) return send(hi.dataset.hi);
    var t = e.target.closest('[data-t]');
    if (t) {
      var row = t.closest('.dm-row'), m = DM[cur].m[+row.dataset.i];
      if (t.dataset.t === 'dot') { var tb = row.querySelector('.dm-tools'), was = tb.classList.contains('keep'); pane.querySelectorAll('.dm-tools.keep').forEach(function (x) { x.classList.remove('keep'); x.closest('.dm-row').classList.remove('tools-on'); }); if (!was) { tb.classList.add('keep'); row.classList.add('tools-on'); } return; }
      pane.querySelectorAll('.dm-tools.keep').forEach(function (x) { if (t.dataset.t !== 'more') { x.classList.remove('keep'); x.closest('.dm-row').classList.remove('tools-on'); } });
      if (t.dataset.t === 'rep') { setReply(m); pane.querySelector('textarea').focus(); }
      if (t.dataset.t === 'rc') { m.rc = m.rc ? null : '👍'; refreshBody(); }
      if (t.dataset.t === 'more') {
        var mine = m[0] === ME;
        showMenu(t, [['ri-pushpin-2-line', 'Ghim tin nhắn', 'pin'], ['ri-file-copy-line', 'Sao chép', 'copy'], ['ri-task-line', 'Tạo nhiệm vụ từ tin này', 'task']].concat(mine ? ['-', ['ri-arrow-go-back-line', 'Thu hồi (trong 24 giờ)', 'rec', 1]] : []), function (v) {
          if (v === 'pin') { DM[cur].pinned = m[1]; DM[cur].pinnedFrom = m[0]; openDM(cur); }
          if (v === 'copy') toast('<i class="ri-file-copy-line"></i> Đã sao chép');
          if (v === 'task') toast('<i class="ri-task-line"></i> Mở form Tạo nhiệm vụ — mô tả = nội dung tin, người làm gợi ý ' + esc(cur));
          if (v === 'rec') { m.rec = 1; refreshBody(); render(); }
        });
      }
      return;
    }
    var a = e.target.closest('[data-a]'); if (!a) return;
    var v = a.dataset.a;
    if (v === 'send') send();
    else if (v === 'info') { info = !info; wrap.classList.toggle('dm-info-on', info); a.classList.toggle('on', info); }
    else if (v === 'norep') setReply(null);
    else if (v === 'unpinmsg') { DM[cur].pinned = null; openDM(cur); }
    else if (v === 'grp') toast('<i class="ri-group-line"></i> Tạo nhóm chat với ' + esc(cur) + ' — làm ở giai đoạn sau');
    else toast('<i class="ri-information-line"></i> Mockup: ' + esc(a.title));
  });
  side.addEventListener('click', function (e) {
    var h = e.target.closest('[data-is]'); if (h) { h.parentElement.classList.toggle('on'); return; }
    var a = e.target.closest('[data-a]'); if (!a || !cur) return; var d = DM[cur];
    if (a.dataset.a === 'mute') { d.mute = !d.mute; toast(d.mute ? '<i class="ri-notification-off-line"></i> Đã tắt thông báo hội thoại này' : '<i class="ri-notification-3-line"></i> Đã bật thông báo'); }
    if (a.dataset.a === 'pinconv') d.pin = !d.pin;
    if (a.dataset.a === 'grp') return toast('<i class="ri-group-line"></i> Tạo nhóm chat — làm ở giai đoạn sau');
    if (a.dataset.a === 'clear') { d.m = []; d.pinned = null; openDM(cur); return toast('<i class="ri-delete-bin-6-line"></i> Đã xoá lịch sử trò chuyện ở phía bạn'); }
    renderInfo(); render();
  });
  pane.addEventListener('keydown', function (e) { if (e.target.tagName === 'TEXTAREA' && e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } });
  pane.addEventListener('input', function (e) { if (e.target.tagName === 'TEXTAREA') { e.target.style.height = 'auto'; e.target.style.height = Math.min(120, e.target.scrollHeight) + 'px'; } });

  // ---- popup Danh bạ (Tin nhắn mới) — mọi NV đang làm việc của mọi công ty ----
  var bk = document.createElement('div'); bk.className = 'dm-bk'; document.body.appendChild(bk);
  var bkCo = CO, bkOpen = {};
  function bkRender() {
    var k = nrm((bk.querySelector('.dm-bk-q input') || {}).value || '');
    var names = Object.keys(P).filter(function (n) { return n !== ME && (bkCo === '*' || coOf(n) === bkCo) && (!k || nrm(n + ' ' + P[n][0] + ' ' + P[n][1] + ' ' + (DEPN[P[n][0]] || '')).indexOf(k) >= 0); });
    var by = {}; names.forEach(function (n) { var d = P[n][0]; (by[d] = by[d] || []).push(n); });
    var deps = Object.keys(by).sort();
    bk.querySelector('.dm-bk-ls').innerHTML = deps.length ? deps.map(function (d) {
      var open = k || bkOpen[d] !== false;
      return '<div class="dm-bk-g' + (open ? ' on' : '') + '"><div class="dm-bk-gh" data-dep="' + d + '"><i class="ri-arrow-right-s-line"></i><b>' + esc(DEPN[d] || d) + '</b><span>' + esc(d) + ' · ' + by[d].length + ' người' + (bkCo === '*' ? ' · ' + esc(coOf(by[d][0])) : '') + '</span></div>' +
        (open ? by[d].map(function (n) { var p = P[n]; return '<div class="dm-bk-p" data-pick="' + esc(n) + '">' + av(n, p[2]) + '<div class="dm-tx"><div class="dm-nm"><span>' + esc(n) + '</span></div><div class="dm-last"><span>' + esc(n + ' - ' + p[0] + ' - ' + p[1]) + '</span></div></div>' + (DM[n] && realMsgs(n).length ? '<span class="dm-tag">Đã nhắn</span>' : '') + '<i class="ri-chat-3-line dm-bk-go"></i></div>'; }).join('') : '') + '</div>';
    }).join('') : '<div class="dm-empty">Không tìm thấy nhân viên đang làm việc' + (bkCo === '*' ? '' : ' của ' + esc(bkCo) + ' — thử chọn "Tất cả công ty"') + '.</div>';
  }
  function bkShow() {
    bk.innerHTML = '<div class="dm-bk-bd" data-bkx="1"></div><div class="dm-bk-m" role="dialog"><div class="dm-bk-h"><span class="dm-bk-ic"><i class="ri-contacts-book-line"></i></span><div><b>Tin nhắn mới</b><small>Chọn người để nhắn riêng — mọi nhân viên đang làm việc, không cần chung nhóm</small></div><button type="button" class="dm-ib" data-bkx="1"><i class="ri-close-line"></i></button></div>' +
      '<div class="dm-bk-tb"><div class="dm-q dm-bk-q"><i class="ri-search-line"></i><input placeholder="Tìm theo tên, mã nhân viên, phòng ban"></div><div class="dm-seg">' + [[CO, CO], ['Tân Phát HCM', 'Tân Phát HCM'], ['*', 'Tất cả công ty']].map(function (c) { return '<button type="button" data-co="' + c[0] + '" class="' + (bkCo === c[0] ? 'on' : '') + '">' + c[1] + '</button>'; }).join('') + '</div></div>' +
      '<div class="dm-bk-ls"></div><div class="dm-bk-ft"><span><i class="ri-information-line"></i> Chọn nhiều người để lập nhóm chat — làm ở giai đoạn sau.</span></div></div>';
    bk.classList.add('on'); bkRender(); bk.querySelector('.dm-bk-q input').focus();
  }
  bk.addEventListener('click', function (e) {
    if (e.target.closest('[data-bkx]')) { bk.classList.remove('on'); return; }
    var c = e.target.closest('[data-co]'); if (c) { bkCo = c.dataset.co; bk.querySelectorAll('[data-co]').forEach(function (b) { b.classList.toggle('on', b === c); }); bkRender(); return; }
    var g = e.target.closest('[data-dep]'); if (g) { bkOpen[g.dataset.dep] = bkOpen[g.dataset.dep] === false; bkRender(); return; }
    var p = e.target.closest('[data-pick]'); if (p) { bk.classList.remove('on'); q.value = ''; openDM(p.dataset.pick); }
  });
  bk.addEventListener('input', bkRender);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { if (bk.classList.contains('on')) bk.classList.remove('on'); closeMenu(); } });

  // ===== 10/11 [U] MINITAB — mẫu tab nhỏ dùng chung: kính trong + sáng bóng (Apple) + chuyển động lò xo như V2BaseTabNavigation / V2BaseSegmented =====
  // root: khối chứa các mục; mục = [data-mt]; mục đang chọn có class "on"; màu mục lấy từ biến CSS --tc. Trả về { go(key, done) }.
  // Chuyển động (giống hệt V2Base): viên chọn GIÃN phủ từ mục cũ tới mục mới 160ms rồi CO về kiểu lò xo cubic-bezier(.34,1.36,.64,1) 400ms;
  // rê chuột: viên nền trắng trượt theo, nở 2px mỗi bên bằng width thật (KHÔNG scale chữ — chữ nhoè); rê lên mục đang chọn thì viên chọn nở 2px.
  function miniTab(root, opt) {
    opt = opt || {}; var GROW = 2, RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches, tmr;
    root.classList.add('mtab');
    var hov = document.createElement('span'), th = document.createElement('span'); hov.className = 'mtab-hov'; th.className = 'mtab-thumb';
    root.insertBefore(th, root.firstChild); root.insertBefore(hov, root.firstChild);
    function items() { return [].slice.call(root.querySelectorAll('[data-mt]')); }
    function on() { return root.querySelector('[data-mt].on'); }
    function place(l, b, g) { if (!b) { l.style.opacity = '0'; return; } g = g || 0; l.style.opacity = ''; l.style.width = (b.offsetWidth + g * 2) + 'px'; l.style.transform = 'translateX(' + (b.offsetLeft - g) + 'px)'; l.classList.toggle('is-grow', g > 0); if (l === th) th.style.setProperty('--tc', getComputedStyle(b).getPropertyValue('--tc')); }
    function jump(l, b) { l.classList.add('no-anim'); place(l, b); void l.offsetWidth; l.classList.remove('no-anim'); }
    function stretch(from, to, done) {
      clearTimeout(tmr);
      if (!from || !to || from === to || RM) { place(th, to); if (done) setTimeout(done, RM ? 0 : 420); return; }
      var L = Math.min(from.offsetLeft, to.offsetLeft), R = Math.max(from.offsetLeft + from.offsetWidth, to.offsetLeft + to.offsetWidth);
      th.classList.add('is-stretch'); th.style.width = (R - L) + 'px'; th.style.transform = 'translateX(' + L + 'px)';
      tmr = setTimeout(function () { th.classList.remove('is-stretch'); place(th, to); if (done) setTimeout(done, 300); }, 160);
    }
    root.addEventListener('mouseover', function (e) { var b = e.target.closest('[data-mt]'); if (!b || !root.contains(b)) return; var act = b.classList.contains('on'); place(hov, b, GROW); hov.style.opacity = act ? '0' : ''; place(th, on(), act ? GROW : 0); });
    root.addEventListener('mouseleave', function () { place(hov, on()); hov.style.opacity = '0'; place(th, on()); });
    // vào trang: nếu vừa bấm từ mục khác (mockup mỗi mục là 1 trang) thì viên chọn trượt từ mục cũ sang — nhìn như 1 tab liền mạch
    var cur = on(), fromK = null; try { fromK = sessionStorage.getItem('mtab-from:' + (opt.id || '')); sessionStorage.removeItem('mtab-from:' + (opt.id || '')); } catch (x) {}
    var from = fromK && root.querySelector('[data-mt="' + fromK + '"]');
    if (cur && from && from !== cur) { jump(th, from); requestAnimationFrame(function () { stretch(from, cur); }); }
    else if (cur) { th.classList.add('no-anim', 'is-pop'); place(th, cur); void th.offsetWidth; th.classList.remove('no-anim'); requestAnimationFrame(function () { th.classList.remove('is-pop'); }); }
    else th.style.opacity = '0';
    window.addEventListener('resize', function () { jump(th, on()); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { if (!th.classList.contains('is-stretch')) place(th, on()); });   // font tải xong mới đo đúng bề rộng
    return {
      go: function (key, done) {
        var to = root.querySelector('[data-mt="' + key + '"]'), fr = on();
        try { if (fr) sessionStorage.setItem('mtab-from:' + (opt.id || ''), fr.getAttribute('data-mt')); } catch (x) {}
        items().forEach(function (b) { b.classList.toggle('on', b === to); });
        hov.style.opacity = '0';
        if (!fr && to) { th.classList.add('no-anim', 'is-pop'); place(th, to); void th.offsetWidth; th.classList.remove('no-anim'); requestAnimationFrame(function () { th.classList.remove('is-pop'); }); if (done) setTimeout(done, 380); return; }
        if (!to) { th.style.opacity = '0'; if (done) setTimeout(done, 180); return; }
        stretch(fr, to, done);
      }
    };
  }
  if (HUB) {
    document.body.classList.add('dm-hub');
    var ntb = document.querySelector('.mk-ntb');
    if (ntb) ntb.outerHTML = '<h5 class="topbar-page-title mb-0 ws-title">Tin nhắn</h5>';   // 10/11 trung tâm chat có tên riêng
  }
  if (LIST) {
    // 10/11 [U] hướng A: bỏ tab Trao đổi — bấm TÊN NHÓM là về chat; các mục còn lại là NÚT CÔNG CỤ bên phải (icon + chữ + số đếm)
    var ntb0 = document.querySelector('.mk-ntb'), surf2 = document.querySelector('.surface.main-wrap'), shd = surf2 && surf2.querySelector('.surface-hd');
    if (ntb0 && surf2 && shd) {
      var li = ntb0.parentElement, sp = SP[SPK];
      var CNT = { room: { tasks: 22, meetings: 2, issues: 3, files: 12 }, iproj: { tasks: 5, meetings: 1 }, gp: { tasks: 18, meetings: 3, issues: 4, files: 27 }, tkt: { tasks: 6, meetings: 2, issues: 5, files: 9 } }[SPK] || {};
      var ICO = { tasks: 'ri-task-line', meetings: 'ri-calendar-event-line', issues: 'ri-bug-line', files: 'ri-folder-3-line' }, CLR = { tasks: '#2563EB', meetings: '#7C3AED', issues: '#D97706', files: '#0EA5E9' };
      var orig = [].slice.call(shd.querySelectorAll('.tabs-root .tab-btn-root'));
      var byKey = {}; orig.forEach(function (b) { byKey[b.getAttribute('data-key')] = b; });
      var act = shd.querySelector('.tabs-root .tab-btn-root.active'), actKey = act ? act.getAttribute('data-key') : 'chat';
      // 10/11 [U] mở Nhiệm vụ / Meeting / Vấn đề / File (và mục ⋮) ⇒ cột hội thoại TỰ THU GỌN còn cột avatar, nhường chỗ cho bảng việc.
      // Về chat (bấm tên nhóm) ⇒ trả lại trạng thái người dùng đã chọn. Bấm nút thu gọn ở các mục này chỉ mở tạm, không ghi nhớ.
      if (actKey !== 'chat') { col.classList.add('mini', 'auto'); var mb0 = col.querySelector('[data-mini]'); if (mb0) mb0.title = 'Mở rộng danh sách hội thoại (tự thu gọn khi làm Nhiệm vụ / Meeting / Vấn đề / File)'; }
      var meta = (ntb0.querySelector('.mk-ntb-meta') || {}).textContent || sp.s, memTx = (ntb0.querySelector('.mk-ntb-mem b') || {}).textContent || '';
      var link = ntb0.querySelector('.mk-ntb-link');
      var hd = document.createElement('div'); hd.className = 'ws-ghd';
      hd.innerHTML = '<a class="ws-gname' + (actKey === 'chat' ? ' on' : '') + '" data-go="chat" title="' + esc(((ntb0.querySelector('.mk-ntb-id') || {}).title || sp.n)) + ' — bấm để về Trao đổi">' + gav(sp) +
          '<span class="ws-gtx"><b>' + esc((ntb0.querySelector('.mk-ntb-nm') || {}).textContent || sp.n) + (sp.un ? '<em class="ws-gun" title="' + sp.un + ' tin chưa đọc trong Trao đổi">' + sp.un + '</em>' : '') + '</b>' +
          '<small>' + esc(meta) + (memTx ? ' · <u data-mem="1" title="Xem thành viên">' + esc(memTx) + '</u>' : '') + (link ? ' · <u data-lnk="1">' + esc(link.textContent.trim()) + '</u>' : '') + '</small></span></a>' +
        '<div class="ws-tools"><div class="ws-seg">' + ['tasks', 'meetings', 'issues', 'files'].filter(function (k) { return byKey[k]; }).map(function (k) {
          var lb = byKey[k].querySelector('.tab-label').textContent.trim();
          return '<button type="button" class="ws-tool' + (actKey === k ? ' on' : '') + '" data-mt="' + k + '" data-go="' + k + '" title="' + esc(lb) + '" style="--tc:' + CLR[k] + '"><i class="' + ICO[k] + '"></i><span>' + esc(lb) + '</span>' + (CNT[k] ? '<em>' + CNT[k] + '</em>' : '') + '</button>';
        }).join('') + '</div>' +
        '<button type="button" class="ws-tool more' + (actKey === 'more' ? ' on' : '') + '" data-more="1" title="Thành viên, Cấu hình' + (SPK === 'gp' || SPK === 'tkt' ? ', mục nghiệp vụ' : '') + '"><i class="ri-more-2-fill"></i>' + (actKey === 'more' ? '<span>' + esc(act.querySelector('.tab-label').textContent.trim()) + '</span>' : '') + '</button>' +
        '<span class="ws-sep"></span><button type="button" class="dm-ib" data-max="1"></button></div>';
      surf2.insertBefore(hd, surf2.firstChild);
      var MT = miniTab(hd.querySelector('.ws-seg'), { id: 'ws-' + SPK });
      // 10/11 [U] gộp cụm icon của khung chat (mô phỏng · tìm · thông báo · tự báo · cột phải) lên đầu nhóm, bỏ hàng riêng
      var chr = actKey === 'chat' && document.querySelector('.cx-hd .cx-hd-r');
      if (chr) { var ca = document.createElement('div'); ca.className = 'ws-chat-acts'; ca.appendChild(chr); var tl = hd.querySelector('.ws-tools'); tl.insertBefore(ca, tl.firstChild); ca.insertAdjacentHTML('afterend', '<span class="ws-sep"></span>'); document.body.classList.add('ws-chat-merged'); }
      shd.classList.add('ws-hidden-tabs');
      var mm = shd.querySelector('.mk-more-menu'); if (mm) { document.body.appendChild(mm); mm.classList.add('ws-more-menu'); }
      li.insertAdjacentHTML('afterbegin', '<h5 class="topbar-page-title mb-0 ws-title">Không gian làm việc</h5>');
      hd.addEventListener('click', function (e) {
        var mb = e.target.closest('[data-more]');
        if (mb && mm) { e.stopPropagation(); var on = mm.style.display !== 'block'; mm.style.display = on ? 'block' : 'none'; if (on) { var r = mb.getBoundingClientRect(); mm.style.position = 'fixed'; mm.style.top = (r.bottom + 4) + 'px'; mm.style.left = Math.max(8, r.right - mm.offsetWidth) + 'px'; } return; }
        if (e.target.closest('[data-mem]')) { e.preventDefault(); var mem = document.querySelector('.mk-ntb-mem'); if (mem) mem.click(); return; }
        if (e.target.closest('[data-lnk]')) { e.preventDefault(); if (link) link.click(); return; }
        var g = e.target.closest('[data-go]'); if (!g) return; e.preventDefault();
        var k = g.getAttribute('data-go'); if (k === actKey) return; if (!byKey[k]) return;
        MT.go(k === 'chat' ? null : k, function () { byKey[k].click(); });   // chạy xong chuyển động rồi mới sang mục mới
      });
      document.addEventListener('mousedown', function (e) { if (mm && mm.style.display === 'block' && !mm.contains(e.target) && !e.target.closest('[data-more]')) mm.style.display = 'none'; });
      var idc = ntb0.querySelector('.mk-ntb-id'); if (idc) { idc.style.cursor = 'pointer'; idc.addEventListener('click', function () { if (actKey !== 'chat' && byKey.chat) byKey.chat.click(); }); }
      var mbtn = hd.querySelector('[data-max]');
      var setMax = function (on) {
        document.body.classList.toggle('ws-max', on);
        mbtn.innerHTML = '<i class="' + (on ? 'ri-fullscreen-exit-line' : 'ri-fullscreen-line') + '"></i>';
        mbtn.title = on ? 'Thu nhỏ — hiện lại danh sách hội thoại' : 'Phóng to — làm việc toàn màn với nhóm (tên nhóm lên topbar)';
        try { localStorage.setItem('ws-max', on ? '1' : '0'); } catch (x) {}
        window.dispatchEvent(new Event('resize'));
      };
      mbtn.addEventListener('click', function () { setMax(!document.body.classList.contains('ws-max')); });
      var m0 = false; try { m0 = localStorage.getItem('ws-max') === '1'; } catch (x) {}
      setMax(m0);
    }
    document.body.classList.add('ws-shell');
    // khung phải hẹp hơn (có cột hội thoại) ⇒ giữ popover Lọc nằm trong khung
    var pop = document.querySelector('.mk-filter-pop');
    if (pop) {
      var fit = function () { var par = pop.offsetParent || pop.parentElement; if (!par) return; var W = par.clientWidth, w = Math.min(pop.offsetWidth, W - 16), l = parseFloat(pop.style.left) || 0; if (w < pop.offsetWidth) pop.style.width = w + 'px'; if (l + w > W - 8) pop.style.left = Math.max(8, W - w - 8) + 'px'; };
      new MutationObserver(function () { requestAnimationFrame(fit); }).observe(document.body, { attributes: true, attributeFilter: ['class'] });
      window.addEventListener('resize', fit); setTimeout(fit, 50);
    }
  }
  render();
  if (cur || HUB) openDM(cur || 'Lê Thu Trang');
})();

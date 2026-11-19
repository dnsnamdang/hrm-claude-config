// Sidebar phương án đề xuất (04/11/2026) — rail sáng, phẳng, đơn sắc + popover cấp 2/3 trắng.
// Menu lấy NGUYÊN VĂN từ hrm-client/components/menu-sidebar.js (menuItemsAssign, nhánh gop_db) +
// menu mới của phân hệ Công việc (Không gian làm việc, Đã ghim).
// Giữ nguyên các nút sẵn có của rail (Yêu thích, Gần đây, Không gian làm việc, mục ghim) để sb.js
// (panel chuyển nhanh, ghim/bỏ ghim) chạy như cũ — chỉ dựng lại thứ tự + các nhóm nghiệp vụ.
(function () {
  var rail = document.querySelector('.sale-cats'); if (!rail) return;
  var list = rail.querySelector('.cats-list'); if (!list) return;
  document.body.classList.add('sb2');
  var DV = 'data-v-6f8d4d6a';

  var ERP = { erp: 1 };
  function L(n, o) { var x = { n: n }; if (o) for (var k in o) x[k] = o[k]; return x; }
  // ---- Menu nghiệp vụ (menuItemsAssign) ----
  var GROUPS = [
    { k: 'overview', n: 'Tổng quan', ic: 'ri-dashboard-line', go: 1 },
    { k: 'gp', n: 'Làm giải pháp', ic: 'ri-lightbulb-line', items: [
      L('Quản lý giải pháp'), L('Hạng mục giải pháp'), L('Hàng tạm dự án'), L('BOM Giải pháp'), L('BOM mẫu')] },
    { k: 'task', n: 'Nhiệm vụ', ic: 'ri-list-check-3', items: [
      L('Nhiệm vụ'), L('Vấn đề'), L('Phiếu bàn giao'), L('Tạo bàn giao'), L('Chờ tiếp nhận bàn giao'), L('Cập nhật tiến độ nhiệm vụ')] },
    { k: 'recv', n: 'Tiếp nhận công việc', ic: 'ri-inbox-archive-line', items: [
      L('Dịch vụ kỹ thuật: yêu cầu thiết kế,... (YCGVK)', ERP), L('YC Lắp đặt bàn giao', ERP), L('YC kiểm tra SC - BD', ERP), L('Phiếu xử lý', ERP),
      L('Phiếu cung cấp thông tin làm BG', ERP), L('Phiếu Bảo hành', ERP), L('Phiếu giao việc kỹ thuật', ERP)] },
    { k: 'assign', n: 'Phân công công việc', ic: 'ri-briefcase-4-line', items: [
      L('Việc chờ giao công tác (ERP)'), L('Phiếu đề xuất công việc'), L('Phiếu giao việc tại công ty'), L('Phiếu đề xuất công tác (nghiệp vụ)'),
      L('Phiếu giao công tác'), L('Danh sách gia hạn, kết thúc sớm')] },
    { k: 'result', n: 'Kết quả công việc', ic: 'ri-clipboard-line', items: [
      L('Phiếu nhập KQ công việc (tại công ty)'), L('Phiếu duyệt KQ công việc (tại công ty)'), L('Phiếu nhập KQ công tác (nghiệp vụ)'),
      L('Phiếu duyệt KQ công tác (nghiệp vụ)'), L('Biên bản bàn giao nghiệm thu'), L('Hồ sơ thanh toán'), L('Phiếu công tác chờ lập DNTT'),
      L('Đề nghị thanh toán công tác phí'), L('Quyết toán công khoán theo hợp đồng')] },
    { k: 'report', n: 'Báo cáo', ic: 'ri-bar-chart-box-line', items: [
      L('BC công được hưởng theo phiếu công tác'), L('Thực hiện công việc theo PB - Khách hàng'), L('Hiệu suất làm việc theo dự án'),
      L('Hiệu suất làm việc theo Giải pháp'), L('Theo dõi chỉ số hoàn thành GP theo version'), L('Phân bổ nguồn lực theo nhân viên'),
      L('Báo cáo kế hoạch & kết quả làm việc theo nhân viên')] },
    { k: 'approve', n: 'Phê duyệt', ic: 'ri-check-double-line', subs: [
      { n: 'Giải pháp - Dự án', ic: 'ri-lightbulb-flash-line', items: [L('Yêu cầu làm giải pháp'), L('Báo giá chờ duyệt'), L('Gia hạn dự án TKT')] },
      { n: 'Đề xuất', ic: 'ri-clipboard-line', items: [L('Phiếu đề xuất công tác cần duyệt'), L('Phiếu đề xuất công việc cần duyệt')] },
      { n: 'Giao việc', ic: 'ri-user-shared-line', items: [L('Phiếu giao việc cần duyệt'), L('Phiếu chờ duyệt kết quả giao việc tại công ty'), L('Phiếu duyệt kết quả giao việc tại công ty', ERP)] },
      { n: 'Công tác', ic: 'ri-suitcase-line', items: [L('Phiếu giao công tác cần duyệt'), L('Phiếu chờ duyệt kết quả công tác (nghiệp vụ)'), L('Phiếu duyệt kết quả công tác (nghiệp vụ)', ERP), L('Đề nghị thanh toán công tác phí')] },
      { n: 'Bàn giao - Lắp đặt', ic: 'ri-exchange-box-line', items: [L('Bàn giao công việc'), L('Phiếu yêu cầu lắp đặt, bàn giao chờ duyệt', ERP)] }] },
    { k: 'setup', n: 'Thiết lập', ic: 'ri-settings-3-line', foot: 1, items: [
      L('Phương tiện đi lại'), L('Định mức công đi lại'), L('Cấu hình chung (Quy chế thu nhập kỹ thuật - công nghệ)'), L('Khai Quy chế – Cấu hình')] }
  ];
  var FAV = ['Nhiệm vụ', 'Phiếu giao công tác', 'Báo giá chờ duyệt'];
  var RECENT = ['Nhiệm vụ', 'Phiếu giao việc tại công ty', 'Hiệu suất làm việc theo dự án', 'Quản lý giải pháp', 'Phiếu nhập KQ công tác (nghiệp vụ)'];

  // chỉ mục tìm kiếm: mọi chức năng kèm đường dẫn
  var ALL = [];
  GROUPS.forEach(function (g) {
    (g.items || []).forEach(function (it) { ALL.push({ it: it, path: g.n }); });
    (g.subs || []).forEach(function (s) { s.items.forEach(function (it) { ALL.push({ it: it, path: g.n + ' › ' + s.n }); }); });
  });
  function byName(n) { for (var i = 0; i < ALL.length; i++) if (ALL[i].it.n === n) return ALL[i]; return null; }

  // ---- dựng lại rail ----
  var kids = [].slice.call(list.children);
  function find(t) { for (var i = 0; i < kids.length; i++) { var s = kids[i].querySelector && kids[i].querySelector('span'); if (s && s.textContent.trim() === t && !kids[i].classList.contains('mk-pin')) return kids[i]; } return null; }
  var fav = find('Yêu thích'), rec = find('Gần đây'), todo = find('Lịch làm việc của tôi'), job = find('Công việc của tôi');
  var ws = list.querySelector('.mk-ws-cat'), pinH = list.querySelector('.mk-pin-h'), pins = [].slice.call(list.querySelectorAll('.mk-pin'));
  function el(tag, cls, html) { var e = document.createElement(tag); e.setAttribute(DV, ''); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function div() { return el('div', 'cat-div'); }
  function grpBtn(g) {
    var a = el('a', 'cat sb2-g' + (g.go ? ' cat-nav' : ''));
    a.setAttribute('data-g', g.k); a.title = g.n;
    a.innerHTML = '<i ' + DV + '="" class="cat-ic cat-ic-font ' + g.ic + '"></i> <span ' + DV + '="">' + g.n + '</span>' + (g.go ? '' : '<i class="ri-arrow-right-s-line sb2-car"></i>');
    return a;
  }
  [].slice.call(list.children).forEach(function (c) { c.remove(); });
  // 04/11 bản 2: Tổng quan lên đầu khối 2; "Lịch làm việc của tôi" bỏ chữ "của tôi"
  if (todo) { todo.querySelector('span').textContent = 'Lịch làm việc'; todo.title = 'Lịch làm việc'; }
  if (job) { job.querySelector('span').textContent = 'Việc của tôi'; job.title = 'Việc của tôi'; }
  var ov = grpBtn(GROUPS[0]);
  // 10/11 [U] §4.6 — mục Tin nhắn (chat nhóm + nhắn riêng 1–1), ngay dưới Không gian làm việc
  var dm = el('a', 'cat cat-nav mk-dm-cat'); dm.href = '31-tin-nhan.html'; dm.style.setProperty('--ic', '#60a5fa'); dm.title = 'Tin nhắn (chat nhóm + nhắn riêng)';
  dm.innerHTML = '<i ' + DV + '="" class="cat-ic cat-ic-font ri-message-3-line"><b class="mk-dm-dot"></b></i> <span ' + DV + '="">Tin nhắn</span><em class="mk-dm-n">3</em>';
  if (/31-tin-nhan/.test(location.pathname)) dm.classList.add('mk-ws-on');
  [fav, rec, div(), ov, todo, ws, dm, job].forEach(function (x) { if (x) list.appendChild(x); });
  // 10/11 [U] "bỏ việc ghim hội thoại ở menu" — chat thiết kế như 1 phần mềm chat nằm trong ERP (mục Tin nhắn + lối tắt topbar);
  // thanh bên không còn khối Đã ghim, panel Không gian làm việc bỏ nút ghim / khối Đã ghim.
  if (pinH) pinH.remove(); pins.forEach(function (p) { p.remove(); });
  [].slice.call(document.querySelectorAll('.mk-wr-pin')).forEach(function (x) { x.remove(); });
  [].slice.call(document.querySelectorAll('.mk-ws-page .sub')).forEach(function (s) { var h = s.querySelector('.sub__t'); if (h && /^Đã ghim/.test(h.textContent.trim())) s.remove(); });
  [].slice.call(document.querySelectorAll('.scat[data-p="home"]')).forEach(function (s) { var n = s.querySelector('.scat-nm'), i = s.querySelector('.scat-ic i'); if (n) n.textContent = 'Gần đây'; if (i) i.className = 'ri-history-line'; });
  [].slice.call(document.querySelectorAll('.mk-ws-foot span')).forEach(function (s) { if (/[Gg]him/.test(s.textContent)) s.remove(); });
  // 10/11 [U] lối tắt vào trung tâm chat trên topbar, giữa nút Phóng to toàn màn hình và nút chọn phân hệ
  (function () {
    var on = /3[12]-/.test(location.pathname);
    [].slice.call(document.querySelectorAll('[data-toggle="fullscreen"]')).forEach(function (fs) {   // trang có 2 bản topbar
      var li0 = fs.closest('li'); if (!li0 || (li0.nextElementSibling && li0.nextElementSibling.classList.contains('mk-tb-chat'))) return;
      var li = document.createElement('li');
      li.className = 'dropdown d-none d-lg-inline-block notification-list mk-tb-chat' + (on ? ' on' : '');
      li.innerHTML = '<a href="31-tin-nhan.html" class="nav-link arrow-none waves-effect waves-light" title="Tin nhắn — trung tâm chat (chat nhóm + nhắn riêng)"><i class="fe-message-square noti-icon"></i><span class="badge badge-danger rounded-circle noti-icon-badge">3</span></a>';
      li0.parentNode.insertBefore(li, li0.nextSibling);
    });
    var st = document.createElement('style'); st.textContent = '.mk-p-bar.mk-p-min{right:auto!important;left:9px!important;bottom:62px!important}.mk-tb-chat>a{position:relative}.mk-tb-chat.on>a::after{content:"";position:absolute;left:50%;bottom:8px;width:16px;height:3px;margin-left:-8px;border-radius:2px;background:#1abc9c}';
    document.head.appendChild(st);
  })();
  list.appendChild(div());
  GROUPS.forEach(function (g) { if (!g.foot && !g.go) list.appendChild(grpBtn(g)); });
  var foot = el('div', 'sb2-foot');
  GROUPS.forEach(function (g) { if (g.foot) foot.appendChild(grpBtn(g)); });
  rail.appendChild(foot);

  // ---- popover cấp 2 / cấp 3 ----
  var bd = el('div', 'sb2-bd'), pan = el('div', 'sb2-pan');
  document.body.appendChild(bd); document.body.appendChild(pan);
  var cur = null, sub = 0, favs = FAV.slice();
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function row(it, path) {
    var on = favs.indexOf(it.n) >= 0;
    return '<a class="sb2-row' + (it.erp ? ' is-erp' : '') + '" data-n="' + esc(it.n) + '"><span class="sb2-rn">' + esc(it.n) +
      (path ? '<small>' + esc(path) + '</small>' : '') + '</span>' +
      (it.erp ? '<em class="sb2-erp" title="Màn còn ở ERP, chưa chuyển sang">ERP</em>' : '') +
      '<b class="sb2-star' + (on ? ' on' : '') + '" title="' + (on ? 'Bỏ yêu thích' : 'Thêm vào Yêu thích') + '"><i class="' + (on ? 'ri-star-fill' : 'ri-star-line') + '"></i></b></a>';
  }
  function head(t, s) { return '<div class="sb2-hd"><b>' + esc(t) + '</b><span>' + esc(s) + '</span><a class="sb2-x" title="Đóng (Esc)"><i class="ri-close-line"></i></a></div>'; }
  function rows(arr, two) { return '<div class="sb2-rows' + (two ? ' two' : '') + '">' + arr.join('') + '</div>'; }
  function render() {
    var h = '', w = 320;
    if (cur === 'fav') {
      h = head('Yêu thích', favs.length + ' chức năng') + (favs.length ? rows(favs.map(function (n) { var x = byName(n); return row(x.it, x.path); })) : '<div class="sb2-empty">Chưa có chức năng yêu thích. Rê chuột vào 1 chức năng và bấm ☆.</div>');
    } else if (cur === 'recent') {
      h = head('Gần đây', RECENT.length + ' chức năng vừa mở') + rows(RECENT.map(function (n) { var x = byName(n); return row(x.it, x.path); }));
    } else if (cur === 'search') {
      var v = q.value.trim().toLowerCase(), r = ALL.filter(function (x) { return x.it.n.toLowerCase().indexOf(v) >= 0 || x.path.toLowerCase().indexOf(v) >= 0; });
      w = 380;
      h = head('Kết quả tìm kiếm', r.length + ' chức năng khớp “' + q.value.trim() + '”') + (r.length ? rows(r.map(function (x) { return row(x.it, x.path); })) : '<div class="sb2-empty">Không tìm thấy chức năng phù hợp.</div>');
    } else {
      var g = GROUPS.filter(function (x) { return x.k === cur; })[0]; if (!g) return;
      if (g.subs) {
        var tot = g.subs.reduce(function (a, s) { return a + s.items.length; }, 0); w = 600;
        h = head(g.n, g.subs.length + ' nhóm · ' + tot + ' chức năng') + '<div class="sb2-nav"><div class="sb2-subs">' +
          g.subs.map(function (s, i) { return '<a class="sb2-sub' + (i === sub ? ' on' : '') + '" data-s="' + i + '"><i class="' + s.ic + '"></i><span>' + esc(s.n) + '</span><em>' + s.items.length + '</em></a>'; }).join('') +
          '</div>' + rows(g.subs[sub].items.map(function (it) { return row(it); })) + '</div>';
      } else {
        var two = g.items.length > 7; w = two ? 560 : 320;
        h = head(g.n, g.items.length + ' chức năng') + rows(g.items.map(function (it) { return row(it); }), two);
      }
    }
    pan.style.width = w + 'px'; pan.innerHTML = h;
  }
  function place() {
    var top = 0;
    [].slice.call(document.querySelectorAll('.navbar-custom')).forEach(function (nb) { if (getComputedStyle(nb).display !== 'none') top = Math.max(top, Math.round(nb.getBoundingClientRect().bottom)); });
    var l = Math.round(rail.getBoundingClientRect().width);
    [pan, bd].forEach(function (x) { x.style.left = l + 'px'; x.style.top = top + 'px'; });
  }
  function mark() { [].slice.call(rail.querySelectorAll('.sb2-g, .cat')).forEach(function (a) { a.classList.toggle('sb2-open', (a.getAttribute('data-g') || a.getAttribute('data-sb2')) === cur && cur !== null); }); }
  function open(k) {
    var wc = document.querySelector('.mk-ws .dclose'); if (wc && document.body.classList.contains('mk-ws-open')) wc.click();
    cur = k; sub = 0; render(); mark();
    rail.classList.add('is-held'); document.body.classList.add('sb2-on');
    place(); [60, 180, 360].forEach(function (t) { setTimeout(place, t); });
  }
  function close() { cur = null; mark(); document.body.classList.remove('sb2-on'); if (!document.body.classList.contains('mk-ws-open')) rail.classList.remove('is-held'); }
  window.__sb2Close = close;
  if (fav) { fav.setAttribute('data-sb2', 'fav'); fav.addEventListener('click', function () { cur === 'fav' ? close() : open('fav'); }); }
  if (rec) { rec.setAttribute('data-sb2', 'recent'); rec.addEventListener('click', function () { cur === 'recent' ? close() : open('recent'); }); }
  if (ws) ws.addEventListener('click', function () { if (cur) close(); rail.classList.add('is-held'); }, true);
  [].slice.call(rail.querySelectorAll('.sb2-g')).forEach(function (a) {
    a.addEventListener('click', function () { var k = a.getAttribute('data-g'); if (k === 'overview') { close(); return; } cur === k ? close() : open(k); });
  });
  bd.addEventListener('click', close);
  pan.addEventListener('click', function (e) {
    var t = e.target;
    if (t.closest('.sb2-x')) { close(); return; }
    var s = t.closest('.sb2-sub'); if (s) { sub = +s.getAttribute('data-s'); render(); return; }
    var st = t.closest('.sb2-star'); if (st) { e.preventDefault(); var n = st.closest('.sb2-row').getAttribute('data-n'), i = favs.indexOf(n); if (i >= 0) favs.splice(i, 1); else favs.push(n); render(); return; }
    if (t.closest('.sb2-row')) close();
  });
  // Rê chuột vào nhóm cấp 2 (Phê duyệt) cũng đổi nội dung — đỡ phải bấm
  pan.addEventListener('mouseover', function (e) { var s = e.target.closest('.sb2-sub'); if (s && +s.getAttribute('data-s') !== sub) { sub = +s.getAttribute('data-s'); render(); } });
  // Tìm chức năng
  var q = rail.querySelector('.cats-search input');
  if (q) q.addEventListener('input', function () { if (q.value.trim()) open('search'); else close(); setTimeout(function () { q.focus(); }, 0); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && cur) close(); });
  // Panel Không gian làm việc: dòng mô tả thứ 2 ẩn đi → đưa vào tooltip; ô tìm gọn chữ
  [].slice.call(document.querySelectorAll('.mk-ws .mk-wr')).forEach(function (r) {
    var nm = r.querySelector('.mk-wr-nm'), sm = r.querySelector('small');
    if (nm && sm) r.title = nm.firstChild.nodeValue.trim() + '\n' + sm.textContent.trim();
  });
  var wq = document.querySelector('.mk-ws .mk-ws-q input'); if (wq) wq.placeholder = 'Tìm không gian làm việc';
  // 04/11: khách CHỐT popover nền navy giống sidebar
  document.body.classList.add('sb2-navy');
  window.addEventListener('resize', function () { if (cur) place(); });
})();

// 11/11 [U] "ở các màn hình đều ghim Agent hỏi đáp ở đầu danh sách liên hệ": mọi màn có cột Hội thoại (dm.js) đều có dòng
// TPE SMART AGENT ghim trên cùng khối "Đã ghim"; bấm → màn 33. Màn 33 tự lo (ai.js, window.__AI_OPEN) nên bỏ qua ở đó.
(function () {
  if (window.__AI_OPEN) return;
  var TB = '#2B59A7';
  var HEAD = '<svg viewBox="0 0 64 64" aria-hidden="true" style="width:86%;height:86%;margin-top:6%"><line x1="32" y1="14" x2="32" y2="7" stroke="' + TB + '" stroke-width="3" stroke-linecap="round"/><circle cx="32" cy="6" r="4" fill="#FBBF24"/>' +
    '<rect x="5" y="27" width="8" height="15" rx="4" fill="' + TB + '"/><rect x="51" y="27" width="8" height="15" rx="4" fill="' + TB + '"/>' +
    '<rect x="10" y="13" width="44" height="40" rx="17" fill="#fff" stroke="' + TB + '" stroke-width="2.6"/>' +
    '<ellipse cx="32" cy="31" rx="17.5" ry="10.5" fill="' + TB + '" transform="rotate(-6 32 31)"/>' +
    '<rect x="22" y="25.5" width="6" height="9" rx="3" fill="#fff"/><rect x="36" y="24.5" width="6" height="9" rx="3" fill="#fff"/>' +
    '<path d="M28.5 37.2q3.8 2.8 7.6 -0.6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/>' +
    '<circle cx="17" cy="44" r="2.6" fill="#F9A8D4"/><circle cx="47" cy="44" r="2.6" fill="#F9A8D4"/></svg>';
  var css = document.createElement('style');
  css.textContent = '.aip-av{width:44px;height:44px;flex:0 0 44px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;overflow:hidden;' +
    'background:radial-gradient(120% 120% at 30% 15%,#fff 0%,#e3ecfa 55%,#c4d6f3 100%);box-shadow:0 3px 10px -4px rgba(43,89,167,.55),inset 0 0 0 1px rgba(43,89,167,.18)}' +
    '.aip-tag{display:inline-flex;align-items:center;height:16px;padding:0 6px;border-radius:999px;font:700 9.5px/16px Roboto,sans-serif;letter-spacing:.06em;color:#fff;background:linear-gradient(90deg,#2B59A7,#4f86d9);margin-left:2px;flex:0 0 auto}' +
    '.aip-it .dm-nm span:first-child{letter-spacing:.02em}.aip-it .dm-last span{color:#6b7280}';
  document.head.appendChild(css);
  function item() {
    return '<div class="dm-it aip-it" data-aip="1" title="TPE SMART AGENT — trợ lý AI trả lời theo quyền của bạn">' +
      '<span class="aip-av">' + HEAD + '</span><div class="dm-tx"><div class="dm-nm"><span>TPE SMART AGENT</span><span class="aip-tag">AI</span></div>' +
      '<div class="dm-last"><span>Hỏi về việc, lịch họp, chấm công, lương…</span></div></div></div>';
  }
  function inject(ls) {
    var q = document.querySelector('.dm-col .dm-q input');
    var f = document.querySelector('.dm-flt .on');
    if ((q && q.value.trim()) || (f && f.getAttribute('data-f') !== 'all') || ls.querySelector('[data-aip]')) return;
    var pz = ls.querySelector('.dm-pinz');
    if (pz) {
      var sec = pz.querySelector('.dm-sec');
      if (sec) { sec.insertAdjacentHTML('afterend', item()); var sm = sec.querySelector('small'); if (sm) sm.textContent = (+sm.textContent || 0) + 1; }
      else pz.insertAdjacentHTML('afterbegin', item());
    } else ls.insertAdjacentHTML('afterbegin', '<div class="dm-pinz"><div class="dm-sec"><span><i class="ri-pushpin-2-fill"></i>Đã ghim</span><small>1</small></div>' + item() + '</div>');
  }
  function start() {
    var ls = document.querySelector('.dm-ls'); if (!ls) return false;
    inject(ls);
    new MutationObserver(function () { inject(ls); }).observe(ls, { childList: true });
    ls.addEventListener('click', function (e) { if (e.target.closest('[data-aip]')) { e.stopPropagation(); location.href = '33-tro-ly-erp.html'; } }, true);
    return true;
  }
  if (!start()) {
    var tries = 0, iv = setInterval(function () { if (start() || ++tries > 40) clearInterval(iv); }, 50);
  }
})();

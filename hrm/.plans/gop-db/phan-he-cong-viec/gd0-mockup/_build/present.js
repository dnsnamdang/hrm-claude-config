// Bản trình bày: nối các màn bấm được như phần mềm thật + thanh điều khiển người thuyết trình.
// Chỉ hiện thanh điều khiển khi mở màn trực tiếp (không nằm trong iframe của index dev).
(function () {
  var STORY = [
    ['g', 'Vào phân hệ'],
    ['01-danh-sach-khong-gian', 'Danh sách không gian làm việc', 'list'],
    ['24-sidebar-chuyen-nhanh', 'Chuyển nhanh giữa các không gian', 'room'],
    ['g', 'Tạo không gian làm việc'],
    ['11-tao-phong-theo-phong-ban', 'Tạo Phòng làm việc theo phòng ban', 'list'],
    ['12-tao-phong-tu-chon', 'Tạo Phòng làm việc tự chọn', 'list'],
    ['13-tao-du-an-noi-bo', 'Tạo Dự án nội bộ', 'list'],
    ['g', 'Phòng làm việc'],
    ['02-phong-tong-quan', 'Tổng quan phòng', 'room'],
    ['03-phong-nhiem-vu', 'Nhiệm vụ của phòng', 'room'],
    ['19-phong-van-de', 'Vấn đề của phòng', 'room'],
    ['15-phong-meeting', 'Meeting của phòng', 'room'],
    ['20-phong-file', 'File của phòng', 'room'],
    ['04-phong-trao-doi', 'Trao đổi (nhóm chat của phòng)', 'room'],
    ['05-phong-thanh-vien', 'Thành viên', 'room'],
    ['06-phong-du-an-noi-bo', 'Dự án nội bộ của phòng', 'room'],
    ['07-popup-tao-du-an-trong-phong', 'Tạo dự án nội bộ trong phòng', 'room'],
    ['21-phong-cau-hinh', 'Cấu hình phòng', 'room'],
    ['g', 'Dự án nội bộ'],
    ['16-du-an-noi-bo-nhiem-vu-gon', 'Nhiệm vụ của dự án nội bộ', 'iproj'],
    ['17-du-an-noi-bo-nhiem-vu-dang-loc', 'Đang lọc nâng cao', 'iproj'],
    ['18-bo-cuc-chu-thich', 'Giải thích bố cục màn hình', 'iproj'],
    ['08-du-an-noi-bo-kin-trao-doi', 'Trao đổi trong dự án Kín', 'iproj'],
    ['g', 'Dự án khách hàng'],
    ['10-tkt-van-de', 'Dự án Tiền khả thi · Vấn đề', 'tkt'],
    ['14-tkt-menu-them', 'Menu “Thêm” của Tiền khả thi', 'tkt'],
    ['22-giai-phap-tong-quan', 'Dự án Giải pháp · Tổng quan', 'gp'],
    ['23-giai-phap-hang-muc', 'Giải pháp · Hạng mục', 'gp'],
    ['09-giai-phap-thanh-vien', 'Giải pháp · Thành viên', 'gp'],
    ['25-gp-nhiem-vu', 'Giải pháp · Nhiệm vụ', 'gp'],
    ['26-gp-van-de', 'Giải pháp · Vấn đề', 'gp'],
    ['27-gp-meeting', 'Giải pháp · Meeting', 'gp'],
    ['28-gp-file', 'Giải pháp · File', 'gp'],
    ['29-gp-trao-doi', 'Giải pháp · Trao đổi', 'gp'],
    ['30-gp-cau-hinh', 'Giải pháp · Cấu hình', 'gp']
  ];
  var TAB = {
    room: { 'Tổng quan': '02-phong-tong-quan', 'Nhiệm vụ': '03-phong-nhiem-vu', 'Vấn đề': '19-phong-van-de', 'Meeting': '15-phong-meeting', 'File': '20-phong-file', 'Trao đổi': '04-phong-trao-doi', 'Thành viên': '05-phong-thanh-vien', 'Dự án nội bộ': '06-phong-du-an-noi-bo', 'Cấu hình': '21-phong-cau-hinh' },
    iproj: { 'Nhiệm vụ': '16-du-an-noi-bo-nhiem-vu-gon', 'Trao đổi': '08-du-an-noi-bo-kin-trao-doi' },
    gp: { 'Tổng quan': '22-giai-phap-tong-quan', 'Nhiệm vụ': '25-gp-nhiem-vu', 'Vấn đề': '26-gp-van-de', 'Meeting': '27-gp-meeting', 'File': '28-gp-file', 'Trao đổi': '29-gp-trao-doi', 'Hạng mục': '23-giai-phap-hang-muc', 'Thành viên': '09-giai-phap-thanh-vien', 'Cấu hình': '30-gp-cau-hinh' },
    tkt: { 'Vấn đề': '10-tkt-van-de' }
  };
  var LINK = { 'Phòng Nhân Sự Hành Chính': '02-phong-tong-quan', 'Tổ chức hội nghị công đoàn 2027': '16-du-an-noi-bo-nhiem-vu-gon', 'Tiền khả thi DA010': '10-tkt-van-de', 'Giải pháp GP40': '22-giai-phap-tong-quan' };
  var KPI = {
    '02-phong-tong-quan': ['03-phong-nhiem-vu', '03-phong-nhiem-vu', '04-phong-trao-doi', '19-phong-van-de', '06-phong-du-an-noi-bo'],
    '24-sidebar-chuyen-nhanh': ['03-phong-nhiem-vu', '03-phong-nhiem-vu', '04-phong-trao-doi', '19-phong-van-de', '06-phong-du-an-noi-bo'],
    '22-giai-phap-tong-quan': ['23-giai-phap-hang-muc', '23-giai-phap-hang-muc', '25-gp-nhiem-vu', '26-gp-van-de', '29-gp-trao-doi']
  };
  var MODAL = { // [đóng về, nút tạo → màn, toast]
    '07-popup-tao-du-an-trong-phong': ['06-phong-du-an-noi-bo', '06-phong-du-an-noi-bo', 'Đã tạo dự án (mô phỏng)'],
    '11-tao-phong-theo-phong-ban': ['01-danh-sach-khong-gian', '02-phong-tong-quan', 'Đã tạo Phòng làm việc (mô phỏng)'],
    '12-tao-phong-tu-chon': ['01-danh-sach-khong-gian', '01-danh-sach-khong-gian', 'Đã tạo Phòng làm việc (mô phỏng)'],
    '13-tao-du-an-noi-bo': ['01-danh-sach-khong-gian', '16-du-an-noi-bo-nhiem-vu-gon', 'Đã tạo dự án nội bộ (mô phỏng)']
  };
  var CREATE_RADIO = { 'Phòng làm việc': '11-tao-phong-theo-phong-ban', 'Dự án nội bộ': '13-tao-du-an-noi-bo', 'Theo phòng ban': '11-tao-phong-theo-phong-ban', 'Tự chọn': '12-tao-phong-tu-chon' };

  var key = decodeURIComponent(location.pathname.split('/').pop()).replace(/\.html$/, '');
  var items = STORY.filter(function (s) { return s[0] !== 'g'; });
  var idx = items.findIndex(function (s) { return s[0] === key; });
  if (idx < 0) return;
  var cur = items[idx], type = cur[2];
  var NOTE = (window.MK_NOTES || {})[key] || '';   // thuyết minh: viết sau, sửa ở file present-notes.js
  var embedded = window.top !== window;
  var LS = 'mk-present';
  function st() { try { return JSON.parse(localStorage.getItem(LS)) || {}; } catch (e) { return {}; } }
  function save(o) { try { var s = st(); for (var k in o) s[k] = o[k]; localStorage.setItem(LS, JSON.stringify(s)); } catch (e) {} }
  function go(k, msg) { if (msg) save({ toast: msg }); location.href = k + '.html'; }
  function txt(e) { return (e.textContent || '').replace(/\s+/g, ' ').trim(); }

  // ---- toast ----
  var tw = document.createElement('div'); tw.className = 'mk-p-toast'; document.body.appendChild(tw);
  var tt;
  function toast(m) { tw.innerHTML = m; tw.classList.add('on'); clearTimeout(tt); tt = setTimeout(function () { tw.classList.remove('on'); }, 2200); }
  var pend = st().toast; if (pend) { save({ toast: '' }); setTimeout(function () { toast('<i class="ri-checkbox-circle-line"></i> ' + pend); }, 250); }
  function miss() { toast('<i class="ri-information-line"></i> Màn này không nằm trong bản trình bày'); }

  // ---- nối màn ----
  function mark(el, k) { if (!el) return; el.setAttribute('data-mk-go', k || ''); }
  var tabs = TAB[type] || {};
  document.querySelectorAll('.tabs-root .tab-btn-root:not(.mk-more-btn), .mk-more-it, .mk-chat-btn').forEach(function (b) {
    var label = txt(b).replace(/\d+$/, '').trim();
    mark(b, tabs[label] || '');
    b.addEventListener('click', function (e) {
      var t = tabs[label]; e.preventDefault(); e.stopPropagation();
      if (t === key) return; t ? go(t) : miss();
    }, true);
  });
  document.querySelectorAll('.mk-kpi').forEach(function (a, i) {
    var t = (KPI[key] || [])[i]; mark(a, t || '');
    a.addEventListener('click', function (e) { e.preventDefault(); t ? go(t) : miss(); });
  });
  document.querySelectorAll('a.mk-link, .content-page a, .mk-ntb-link').forEach(function (a) {
    if (a.closest('.mk-ws, .sale-cats, .mk-more-menu, .mk-lv, .mk-td') || a.classList.contains('mk-kpi')) return;
    var h = a.getAttribute('href') || ''; if (/\.html$/.test(h)) { mark(a, h); return; }
    var n = txt(a), t = LINK[n] || (/DA010/.test(n) ? '10-tkt-van-de' : /GP40/.test(n) ? '22-giai-phap-tong-quan' : null);
    if (!a.classList.contains('mk-link') && !a.classList.contains('mk-ntb-link') && !t) return;
    mark(a, t || '');
    a.addEventListener('click', function (e) { e.preventDefault(); t ? go(t) : miss(); });
  });
  var mem = document.querySelector('.mk-ntb-mem');
  if (mem) { var mt = type === 'room' ? '05-phong-thanh-vien' : type === 'gp' ? '09-giai-phap-thanh-vien' : null; mem.href = 'javascript:void(0)'; mark(mem, mt || ''); mem.addEventListener('click', function (e) { e.preventDefault(); mt ? go(mt) : miss(); }); }
  document.querySelectorAll('button').forEach(function (b) {
    var n = txt(b);
    if (n === 'Tạo không gian làm việc' && !b.closest('.mk-ws')) { mark(b, '11-tao-phong-theo-phong-ban'); b.addEventListener('click', function () { go('11-tao-phong-theo-phong-ban'); }); }
    if (n === 'Tạo dự án' && key === '06-phong-du-an-noi-bo') { mark(b, '07-popup-tao-du-an-trong-phong'); b.addEventListener('click', function () { go('07-popup-tao-du-an-trong-phong'); }); }
  });
  var md = MODAL[key], modal = document.querySelector('.modal.show');
  if (md && modal) {
    modal.querySelectorAll('button').forEach(function (b) {
      var n = txt(b);
      if (n === '×' || n === 'Đóng') { mark(b, md[0]); b.addEventListener('click', function (e) { e.preventDefault(); go(md[0]); }); }
      if (/^Tạo (phòng|dự án)$/.test(n)) { mark(b, md[1]); b.addEventListener('click', function (e) { e.preventDefault(); go(md[1], md[2]); }); }
    });
    if (key !== '07-popup-tao-du-an-trong-phong') modal.querySelectorAll('.custom-control-label').forEach(function (l) {
      var t = CREATE_RADIO[txt(l)]; if (!t) return; mark(l, t);
      l.addEventListener('click', function (e) { e.preventDefault(); if (t !== key) go(t); });
    });
    var bd = document.querySelector('.modal-backdrop'); if (bd) bd.addEventListener('click', function () { go(md[0]); });
  }
  document.querySelectorAll('.sale-cats .cat').forEach(function (c) {
    if (c.classList.contains('mk-ws-cat') || c.classList.contains('mk-pin')) return;
    var n = txt(c), t = n === 'Tổng quan' ? '01-danh-sach-khong-gian' : null;
    c.addEventListener('click', function (e) { e.preventDefault(); t ? go(t) : miss(); });
  });
  document.querySelectorAll('.due-pill').forEach(function (p) {
    var row = p.parentElement; if (!row || !row.closest('.mk-tb-chips')) return;
    p.style.cursor = 'pointer';
    p.addEventListener('click', function () { row.querySelectorAll('.due-pill').forEach(function (x) { x.classList.toggle('mk-chip-on', x === p); }); });
  });
  // menu thả "Gửi vấn đề cho" (Tạo vấn đề): đóng sẵn, bấm nút mới mở
  document.querySelectorAll('.mk-dd').forEach(function (dd) {
    var host = dd.parentElement, btn = host && [].slice.call(host.querySelectorAll('button')).find(function (b) { return /^Tạo /.test(txt(b)); });
    if (!btn || document.body.classList.contains('mk-menu-open')) return;
    dd.style.display = 'none'; mark(btn, 'dd');
    btn.addEventListener('click', function (e) { e.stopPropagation(); dd.style.display = dd.style.display === 'none' ? '' : 'none'; });
    document.addEventListener('click', function (e) { if (!dd.contains(e.target) && e.target !== btn) dd.style.display = 'none'; });
    dd.querySelectorAll('.mk-dd-i').forEach(function (it) { it.style.cursor = 'pointer'; it.addEventListener('click', function () { dd.style.display = 'none'; miss(); }); });
  });
  if (embedded) return;

  // ---- thanh điều khiển người thuyết trình ----
  var S = st();
  var bar = document.createElement('div'); bar.className = 'mk-p-bar' + (S.hide !== false ? ' mk-p-min' : '');
  var groupOf = function (k) { var g = ''; for (var i = 0; i < STORY.length; i++) { if (STORY[i][0] === 'g') g = STORY[i][1]; if (STORY[i][0] === k) return g; } return ''; };
  bar.innerHTML =
    '<button class="mk-p-b" data-a="list" title="Danh sách màn (L)"><i class="ri-layout-grid-line"></i></button>' +
    '<button class="mk-p-b" data-a="prev" title="Màn trước (←)"' + (idx === 0 ? ' disabled' : '') + '><i class="ri-arrow-left-s-line"></i></button>' +
    '<div class="mk-p-t"><small>' + (idx + 1) + ' / ' + items.length + ' · ' + groupOf(key) + '</small><b>' + cur[1] + '</b></div>' +
    '<button class="mk-p-b" data-a="next" title="Màn tiếp (→)"' + (idx === items.length - 1 ? ' disabled' : '') + '><i class="ri-arrow-right-s-line"></i></button>' +
    '<span class="mk-p-sep"></span>' +
    (NOTE ? '<button class="mk-p-b' + (S.notes !== false ? ' on' : '') + '" data-a="notes" title="Thuyết minh (N)"><i class="ri-chat-quote-line"></i></button>' : '') +
    '<button class="mk-p-b" data-a="hint" title="Gợi ý chỗ bấm được (H)"><i class="ri-cursor-line"></i></button>' +
    '<button class="mk-p-b" data-a="full" title="Toàn màn hình (F)"><i class="ri-fullscreen-line"></i></button>' +
    '<a class="mk-p-b" href="../present.html" title="Trang bìa"><i class="ri-home-4-line"></i></a>' +
    '<button class="mk-p-b" data-a="min" title="Thu gọn thanh (P)"><i class="ri-arrow-down-s-line"></i></button>' +
    '<button class="mk-p-handle" data-a="min" title="Hiện thanh điều khiển (P)"><i class="ri-slideshow-3-line"></i></button>';
  document.body.appendChild(bar);
  var note = document.createElement('div'); note.className = 'mk-p-note' + (NOTE && S.notes !== false && S.hide === false ? ' on' : '');
  note.innerHTML = '<div class="mk-p-nh"><span>' + groupOf(key) + '</span><b>' + cur[1] + '</b><i class="ri-close-line" data-a="notes"></i></div><div class="mk-p-nb">' + NOTE + '</div>';
  document.body.appendChild(note);
  var list = document.createElement('div'); list.className = 'mk-p-list';
  var h = '<div class="mk-p-lh"><b>Các màn trong bản trình bày</b><i class="ri-close-line" data-a="list"></i></div><div class="mk-p-lg"><div class="mk-p-grp"><div class="mk-p-gt">Tài liệu</div><a href="../thuyet-minh.html" target="_blank"><em><i class="ri-book-open-line"></i></em>Thuyết minh logic</a>', n = 1;
  STORY.forEach(function (s) {
    if (s[0] === 'g') { h += (n ? '</div>' : '') + '<div class="mk-p-grp"><div class="mk-p-gt">' + s[1] + '</div>'; n++; return; }
    var i = items.indexOf(s);
    h += '<a href="' + s[0] + '.html" class="' + (s[0] === key ? 'on' : '') + '"><em>' + (i + 1) + '</em>' + s[1] + '</a>';
  });
  list.innerHTML = h + '</div></div>';
  document.body.appendChild(list);

  function act(a) {
    if (a === 'prev' && idx > 0) go(items[idx - 1][0]);
    if (a === 'next' && idx < items.length - 1) go(items[idx + 1][0]);
    if (a === 'notes') { if (!NOTE) return; var on = !note.classList.contains('on'); note.classList.toggle('on', on); bar.querySelector('[data-a=notes]').classList.toggle('on', on); save({ notes: on }); }
    if (a === 'list') list.classList.toggle('on');
    if (a === 'hint') hint();
    if (a === 'full') { if (!document.fullscreenElement) document.documentElement.requestFullscreen && document.documentElement.requestFullscreen(); else document.exitFullscreen(); }
    if (a === 'min') { var m = !bar.classList.contains('mk-p-min'); bar.classList.toggle('mk-p-min', m); if (m) { note.classList.remove('on'); list.classList.remove('on'); } else if (NOTE && st().notes !== false) note.classList.add('on'); save({ hide: m }); }
  }
  [bar, note, list].forEach(function (x) { x.addEventListener('click', function (e) { var t = e.target.closest('[data-a]'); if (t) { e.preventDefault(); e.stopPropagation(); act(t.getAttribute('data-a')); } }); });

  var HOT = '[data-mk-go], a[href$=".html"], .mk-filter-btn, .mk-more-btn, .mk-ws-cat, .mk-pin, .sortable-header, .mk-st-nav a, .mk-wr-pin, .mk-tb-chips .due-pill';
  var ht;
  function hint() { document.body.classList.add('mk-p-hint'); clearTimeout(ht); ht = setTimeout(function () { document.body.classList.remove('mk-p-hint'); }, 1600); }
  // Bỏ: bấm chỗ trống nháy viền mọi vùng bấm (gây rối). Gợi ý chỗ bấm chỉ bật bằng nút ⌖ trên thanh trình bày hoặc phím H.
  document.addEventListener('keydown', function (e) {
    if (document.body.classList.contains('mk-td-open')) return;
    var tg = e.target; if (tg && (tg.tagName === 'INPUT' || tg.tagName === 'TEXTAREA' || tg.isContentEditable) || e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key;
    if (k === 'ArrowRight' || k === 'PageDown') act('next');
    else if (k === 'ArrowLeft' || k === 'PageUp') act('prev');
    else if (k === 'n' || k === 'N') act('notes');
    else if (k === 'l' || k === 'L') act('list');
    else if (k === 'h' || k === 'H') act('hint');
    else if (k === 'f' || k === 'F') act('full');
    else if (k === 'p' || k === 'P') act('min');
    else if (k === 'Escape') list.classList.remove('on');
  });
})();

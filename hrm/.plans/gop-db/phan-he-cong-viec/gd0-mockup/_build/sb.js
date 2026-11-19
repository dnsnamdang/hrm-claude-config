(function () {
  var b = document.body, host = document.querySelector('.mk-sb-host'); if (!host) return;
  var pan = host.querySelector('.mk-ws'), bd = host.querySelector('.mk-ws-bd'), rail = document.querySelector('.sale-cats');
  var btn = rail.querySelector('.mk-ws-cat'), q = pan.querySelector('.mk-ws-q input');
  var scats = [].slice.call(pan.querySelectorAll('.scat')), pages = [].slice.call(pan.querySelectorAll('.mk-ws-page'));
  function place() {
    var top = 0;
    [].slice.call(document.querySelectorAll('.navbar-custom')).forEach(function (nb) { if (getComputedStyle(nb).display !== 'none') top = Math.max(top, Math.round(nb.getBoundingClientRect().bottom)); });
    var l = Math.round(rail.getBoundingClientRect().width);
    [pan, bd].forEach(function (x) { x.style.left = l + 'px'; x.style.top = top + 'px'; });
  }
  function show(p) {
    scats.forEach(function (s) { s.classList.toggle('on', s.getAttribute('data-p') === p); });
    pages.forEach(function (x) { x.classList.toggle('on', x.getAttribute('data-p') === p); });
  }
  function open(noFocus) { rail.classList.add('is-held'); b.classList.add('mk-ws-open'); place(); [60, 180, 360].forEach(function (t) { setTimeout(place, t); }); btn.classList.add('mk-ws-on'); if (noFocus !== true) setTimeout(function () { q.focus(); }, 30); }
  function close() { b.classList.remove('mk-ws-open'); rail.classList.remove('is-held'); btn.classList.remove('mk-ws-on'); }
  window.__mkWsOpen = open;
  btn.addEventListener('click', function () { b.classList.contains('mk-ws-open') ? close() : open(false); });
  bd.addEventListener('click', close);
  pan.querySelector('.dclose').addEventListener('click', close);
  scats.forEach(function (s) { s.addEventListener('click', function () { q.value = ''; show(s.getAttribute('data-p')); }); });
  var last = 'home';
  q.addEventListener('input', function () {
    var v = q.value.trim().toLowerCase();
    if (!v) { show(last); return; }
    if (!pan.querySelector('.mk-ws-page[data-p="search"].on')) { var on = pan.querySelector('.scat.on'); last = on ? on.getAttribute('data-p') : 'home'; }
    show('search');
    var sp = pan.querySelector('.mk-ws-page[data-p="search"]'), n = 0;
    sp.querySelectorAll('.mk-wr').forEach(function (r) { var ok = r.getAttribute('data-q').indexOf(v) >= 0; r.style.display = ok ? '' : 'none'; if (ok) n++; });
    sp.querySelector('.mk-ws-cnt').textContent = n;
    sp.querySelector('.mk-ws-empty').style.display = n ? 'none' : '';
  });
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) { e.preventDefault(); open(false); }
    else if (e.key === 'Escape' && b.classList.contains('mk-ws-open')) close();
  });
  // Ghim / bỏ ghim: đồng bộ mọi dòng cùng id + rail
  pan.addEventListener('click', function (e) {
    var p = e.target.closest('.mk-wr-pin'); if (!p || p.style.visibility === 'hidden') return;
    e.preventDefault(); e.stopPropagation();
    var r = p.closest('.mk-wr'), id = r.getAttribute('data-id'), on = !p.classList.contains('on');
    var pins = rail.querySelectorAll('.mk-pin');
    if (on && pins.length >= 5) { p.classList.add('mk-shake'); setTimeout(function () { p.classList.remove('mk-shake'); }, 500); p.title = 'Đã đủ 5 không gian ghim — bỏ ghim bớt trước'; return; }
    pan.querySelectorAll('.mk-wr[data-id="' + id + '"] .mk-wr-pin').forEach(function (x) {
      x.classList.toggle('on', on); x.title = on ? 'Bỏ ghim' : 'Ghim lên thanh bên';
      x.innerHTML = on ? '<i class="ri-pushpin-fill"></i>' : '<i class="ri-pushpin-line"></i>';
    });
    var ex = rail.querySelector('.mk-pin[data-id="' + id + '"]');
    if (!on && ex) ex.remove();
    if (on && !ex) {
      var tpl = pins[0], a = tpl.cloneNode(true), ic = r.querySelector('.mk-wr-ic'), nm = r.querySelector('.mk-wr-nm').firstChild.nodeValue;
      a.setAttribute('data-id', id); a.classList.remove('on'); if (r.classList.contains('on')) a.classList.add('on');
      a.href = r.getAttribute('href'); a.title = nm;
      var col = { 'rgb(14, 165, 233)': '#38bdf8', 'rgb(124, 58, 237)': '#b79cf0', 'rgb(217, 119, 6)': '#f5a524' }[getComputedStyle(ic).color] || '#9fb0c6';
      a.style.setProperty('--ic', col);
      var ai = a.querySelector('.mk-pin-ic'); ai.className = ai.className.replace(/ri-[\w-]+/g, '').trim() + ' ' + (ic.className.match(/ri-[\w-]+/) || [''])[0];
      var un = r.querySelector('.mk-wr-un'); ai.innerHTML = un ? '<b class="mk-pin-n">' + un.textContent + '</b>' : '';
      a.querySelector('span').textContent = nm;
      var em = a.querySelector('.mk-pin-c'); if (em) em.remove(); if (un) { em = document.createElement('em'); em.className = 'mk-pin-c'; em.textContent = un.textContent; a.appendChild(em); }
      (pins.length ? pins[pins.length - 1] : rail.querySelector('.mk-pin-h')).after(a);
    }
    var cnt = pan.querySelector('.mk-ws-page[data-p="home"] .sub__t .c');
    if (cnt) cnt.textContent = rail.querySelectorAll('.mk-pin').length;
  }, true);
  window.addEventListener('resize', place);
})();

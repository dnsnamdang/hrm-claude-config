(function () {
  var A = window.__MK_ANNOT || [];
  var host = document.querySelector('main .overflow-auto');
  var lg = document.createElement('div');
  lg.className = 'mk-legend';
  var h = '<h6>Chú thích bố cục — màn Nhiệm vụ của Dự án nội bộ (số đỏ trên màn ↔ số trong bảng). Menu Thêm, Lọc vẫn bấm được.</h6><div class="mk-legend-g">';
  var n = 0, items = [];
  A.forEach(function (a) {
    if (!a[1]) { h += '<div class="mk-legend-sec">' + a[0] + '</div>'; return; }
    var el;
    if (a[0].indexOf('ALL:') === 0) {
      var els = [].slice.call(document.querySelectorAll(a[0].slice(4)));
      if (!els.length) return;
      el = { offsetParent: true, getBoundingClientRect: function () {
        var rs = els.map(function (e) { return e.getBoundingClientRect(); });
        var l = Math.min.apply(null, rs.map(function (r) { return r.left; })), t = Math.min.apply(null, rs.map(function (r) { return r.top; }));
        var rr = Math.max.apply(null, rs.map(function (r) { return r.right; })), b = Math.max.apply(null, rs.map(function (r) { return r.bottom; }));
        return { left: l, top: t, width: rr - l, height: b - t };
      } };
    } else { el = document.querySelector(a[0]); }
    if (!el) return;
    n++; items.push([n, el]);
    h += '<div><span class="n">' + n + '</span><div><b>' + a[1] + '</b> — ' + a[2] + '</div></div>';
  });
  lg.innerHTML = h + '</div>';
  host.appendChild(lg);
  var layer = document.createElement('div');
  document.body.appendChild(layer);
  function draw() {
    layer.innerHTML = '';
    items.forEach(function (it) {
      var r = it[1].getBoundingClientRect();
      if (!r.width || !it[1].offsetParent) return;
      var bx = document.createElement('div');
      bx.className = 'mk-an-box';
      bx.style.left = (r.left - 3) + 'px'; bx.style.top = (r.top - 3) + 'px';
      bx.style.width = (r.width + 6) + 'px'; bx.style.height = (r.height + 6) + 'px';
      var no = document.createElement('div');
      no.className = 'mk-an-no';
      no.textContent = it[0];
      no.style.left = Math.max(2, r.left - 10) + 'px'; no.style.top = Math.max(2, r.top - 12) + 'px';
      layer.appendChild(bx); layer.appendChild(no);
    });
  }
  layer.style.cssText = 'position:fixed;left:0;top:0;width:0;height:0;z-index:2000';
  draw();
  window.addEventListener('resize', draw);
  host.addEventListener('scroll', draw);
  document.addEventListener('click', function () { setTimeout(draw, 30); }, true);
})();

// 10/11 [U] "các chip lọc nhanh: Tất cả / Của tôi /... đổi thành select có con số + màu sắc cho gọn".
// Giữ nguyên cụm chip gốc (ẩn đi) để bộ lọc cũ vẫn đếm + lọc; ô chọn chỉ đọc nhãn/số từ chip và bấm hộ chip.
(function () {
  var RED = '#DC2626', BLUE = '#2563EB', AMB = '#D97706', TEAL = '#1abc9c', PUR = '#7C3AED', SKY = '#0EA5E9', GRAY = '#6B7280', ORG = '#EA580C';
  var CLR = { 'Tất cả': GRAY, 'Của tôi': BLUE, 'Tôi chủ trì': BLUE, 'Tôi phụ trách': BLUE, 'Quá hạn': RED, 'Chậm tiến độ': RED, 'Chưa có biên bản': RED, 'Có tin chưa đọc': RED,
    'Chờ tôi duyệt': AMB, 'Chờ duyệt hồ sơ': AMB, 'Đang mở': TEAL, 'Sắp diễn ra': TEAL, 'Đang hoạt động': TEAL, 'Từ giải pháp': PUR, 'Từ trao đổi': PUR,
    'Tài liệu': SKY, 'Hình ảnh': TEAL, 'Quản lý': AMB, 'Thành viên': BLUE, 'Xem': GRAY, 'Đã khoá': GRAY, 'Nhóm trao đổi': BLUE, 'Dự án khách hàng': ORG, 'Lưu trữ': GRAY };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  document.querySelectorAll('.mk-tb-chips').forEach(function (box) {
    var pills = function () { return [].slice.call(box.querySelectorAll('.due-pill')); };
    if (!pills().length) return;
    var qs = document.createElement('div'); qs.className = 'mk-qs';
    box.parentNode.insertBefore(qs, box.nextSibling); box.classList.add('mk-qs-hide');
    var open = false;
    function info(p) {
      var tx = p.textContent.trim(), m = /^(.*?):\s*(\d+)\s*$/.exec(tx), l = m ? m[1].trim() : tx, n = m ? +m[2] : null;
      return { p: p, l: l, n: n, on: p.classList.contains('mk-chip-on'), c: CLR[l] || (p.classList.contains('st-overdue') ? RED : TEAL), t: p.getAttribute('title') || '' };
    }
    function cnt(o) { return o.n === null ? '' : '<span class="mk-qs-n' + (o.n ? '' : ' z') + '">' + o.n + '</span>'; }
    function draw() {
      var L = pills().map(info), a = L.filter(function (o) { return o.on; })[0] || L[0];
      qs.innerHTML = '<button type="button" class="mk-qs-b' + (a !== L[0] ? ' sel' : '') + (open ? ' open' : '') + '" style="--qc:' + a.c + '" title="Lọc nhanh: ' + esc(a.l) + '"><span class="mk-qs-d"></span>' + esc(a.l) + cnt(a) + '<i class="ri-arrow-down-s-line"></i></button>' +
        '<div class="mk-qs-m' + (open ? ' on' : '') + '">' + L.map(function (o, i) {
          return '<div class="mk-qs-o' + (o === a ? ' on' : '') + '" data-i="' + i + '" style="--qc:' + o.c + '" title="' + esc(o.t) + '"><span class="mk-qs-d"></span>' + esc(o.l) + cnt(o) + '<i class="ri-check-line mk-qs-ck"></i></div>';
        }).join('') + '</div>';
    }
    qs.addEventListener('click', function (e) {
      e.stopPropagation();
      var o = e.target.closest('.mk-qs-o');
      if (o) { var p = pills()[+o.getAttribute('data-i')]; open = false; if (p && !p.classList.contains('mk-chip-on')) p.click(); draw(); return; }
      if (e.target.closest('.mk-qs-b')) { open = !open; draw(); }
    });
    document.addEventListener('mousedown', function (e) { if (open && !qs.contains(e.target)) { open = false; draw(); } });
    document.addEventListener('keydown', function (e) { if (open && e.key === 'Escape') { open = false; draw(); } });
    new MutationObserver(function () { draw(); }).observe(box, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ['class'] });
    draw();
  });
})();

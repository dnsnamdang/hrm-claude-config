// U18: bảng có nội dung bị ẩn ⇒ luôn có thanh cuộn ngang ở CẢ trên và dưới, 2 thanh đồng bộ; vừa khung thì ẩn cả 2.
(function () {
  function scroller(t) { var e = t.parentElement; while (e && e !== document.body) { var o = getComputedStyle(e).overflowX; if (o === 'auto' || o === 'scroll') return e; e = e.parentElement; } return null; }
  var seen = [];
  [].slice.call(document.querySelectorAll('table')).forEach(function (t) {
    var sc = scroller(t); if (!sc || seen.indexOf(sc) >= 0) return; seen.push(sc);
    sc.classList.add('mk-hs');
    var top = sc.previousElementSibling;
    if (!top || !top.classList.contains('table-top-scroll')) {
      top = document.createElement('div'); top.className = 'table-top-scroll mk-hs-top';
      top.appendChild(document.createElement('div')).className = 'table-top-scroll-inner';
      sc.parentNode.insertBefore(top, sc);
    }
    top.classList.add('mk-hs');
    var inner = top.firstElementChild, lock = 0;
    function upd() {
      sc.style.overflowX = '';
      var over = sc.scrollWidth > sc.clientWidth + 1;
      if (!over) sc.style.overflowX = 'hidden';   // dư < 1px: không hiện thanh cuộn rỗng
      top.style.display = over ? '' : 'none';
      sc.classList.toggle('mk-hs-over', over);
      inner.style.width = sc.scrollWidth + 'px';
      top.scrollLeft = sc.scrollLeft;
    }
    top.addEventListener('scroll', function () { if (lock === 2) { lock = 0; return; } lock = 1; sc.scrollLeft = top.scrollLeft; });
    sc.addEventListener('scroll', function () { if (lock === 1) { lock = 0; return; } lock = 2; top.scrollLeft = sc.scrollLeft; });
    if (window.ResizeObserver) { var ro = new ResizeObserver(upd); ro.observe(sc); ro.observe(t); }
    window.addEventListener('resize', upd); upd();
  });
})();

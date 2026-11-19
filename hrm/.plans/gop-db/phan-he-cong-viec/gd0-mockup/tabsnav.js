// Thanh tab chính — hiệu ứng rê chuột GIỐNG PHẦN MỀM (04/11/2026).
// Chép logic của hrm-client/components/V2BaseTabNavigation.vue (onHover / onLeave / place / syncLayers):
// - 2 lớp nền riêng: viên chọn `.tabs-thumb` (xanh ngọc) + viên hover `.tabs-hover` (trắng), trượt theo tab bằng
//   translateX + width (CSS lò xo 0,4s của component đã có sẵn trong mockup.css);
// - rê vào tab: viên hover trượt tới và nở 2px mỗi bên; rê vào tab đang chọn: ẩn viên hover, viên chọn nở 2px;
// - rời thanh tab: cả 2 co về tab đang chọn.
// Mockup trước đây tắt 2 lớp này bằng CSS (chỉ tô nền cứng cho tab đang chọn) vì chưa có JS điều khiển.
(function () {
  var GROW = 2;
  function place(layer, btn, grow) {
    if (!layer) return;
    if (!btn) { layer.style.opacity = '0'; return; }
    grow = grow || 0;
    layer.style.width = (btn.offsetWidth + grow * 2) + 'px';
    layer.style.transform = 'translateX(' + (btn.offsetLeft - grow) + 'px)';
    layer.classList.toggle('is-grow', grow > 0);
  }
  [].slice.call(document.querySelectorAll('.tabs-root')).forEach(function (root) {
    var hover = root.querySelector('.tabs-hover'), thumb = root.querySelector('.tabs-thumb'), hoverKey = null;
    function active() { return root.querySelector('.tab-btn-root.active'); }
    function sync() {
      place(thumb, active(), hoverKey && active() && hoverKey === active().getAttribute('data-key') ? GROW : 0);
      if (!hoverKey) { place(hover, active()); }
    }
    // đặt ngay vị trí, không cho chạy hiệu ứng trượt lúc vừa mở màn
    [thumb, hover].forEach(function (l) { if (l) l.style.transition = 'none'; });
    if (thumb) thumb.style.opacity = '';
    if (hover) hover.style.opacity = '';
    sync();
    requestAnimationFrame(function () { requestAnimationFrame(function () { [thumb, hover].forEach(function (l) { if (l) l.style.transition = ''; }); }); });
    root.addEventListener('mouseover', function (e) {
      var btn = e.target.closest && e.target.closest('.tab-btn-root'); if (!btn || !root.contains(btn)) return;
      var key = btn.getAttribute('data-key'); if (key === hoverKey) return;
      hoverKey = key;
      var act = active(), onActive = act && key === act.getAttribute('data-key');
      place(hover, btn, GROW);
      if (hover) hover.style.opacity = onActive ? '0' : '';
      place(thumb, act, onActive ? GROW : 0);
    });
    root.addEventListener('mouseleave', function () {
      hoverKey = null;
      if (hover) hover.style.opacity = '';
      place(hover, active()); place(thumb, active());
    });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(sync);
    window.addEventListener('resize', sync);
  });
})();

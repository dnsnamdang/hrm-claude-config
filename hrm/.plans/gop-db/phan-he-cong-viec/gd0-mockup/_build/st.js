(function () {
  var nav = document.querySelector('.mk-st-nav'); if (!nav) return;
  var sc = document.querySelector('main .overflow-auto');
  var links = [].slice.call(nav.querySelectorAll('a')), lock = 0;
  function sec(a) { return document.getElementById(a.getAttribute('data-t')); }
  function setOn(a) { links.forEach(function (x) { x.classList.toggle('on', x === a); }); }
  links.forEach(function (a) {
    a.addEventListener('click', function () {
      var t = sec(a); if (!t) return;
      var y = t.getBoundingClientRect().top - sc.getBoundingClientRect().top + sc.scrollTop - 8;
      lock = Date.now() + 900; setOn(a);
      sc.scrollTo({ top: y, behavior: 'smooth' });
    });
  });
  function spy() {
    if (Date.now() < lock) return;
    var atBottom = sc.scrollTop + sc.clientHeight >= sc.scrollHeight - 4, best = links[0];
    if (atBottom) best = links[links.length - 1];
    else links.forEach(function (a) { var t = sec(a); if (t && t.getBoundingClientRect().top - sc.getBoundingClientRect().top < 140) best = a; });
    setOn(best);
  }
  sc.addEventListener('scroll', spy); spy();
})();

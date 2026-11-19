// U24: Bộ lọc chạy thật trên dữ liệu (Danh sách + Bảng): tìm khi gõ · chip lọc nhanh có số đếm · Lọc nâng cao (ô chọn thật) · hàng điều kiện đang lọc.
(function () {
  var L = window.__MKLV, tb = document.querySelector('.mk-tb'), pop = document.querySelector('.mk-filter-pop'), afl = document.querySelector('.mk-afl');
  if (!L || !tb || !pop) return;
  var isI = L.isIssue, N = L.NOUN, esc = L.esc, b = document.body;
  document.querySelectorAll('tr.mk-fx').forEach(function (tr) { tr.classList.remove('mk-fx'); }); b.classList.remove('mk-filtered');
  var F = { who: '', cr: '', st: '', pri: '', proj: '', from: '', to: '' }, A = JSON.parse(JSON.stringify(F)), Q = '', CHIP = 'all';
  var LBL = { who: isI ? 'Người xử lý' : 'Người thực hiện', cr: isI ? 'Người tạo' : 'Người giao', st: 'Trạng thái', pri: 'Mức độ ưu tiên', proj: 'Dự án', due: isI ? 'Hạn xử lý' : 'Hạn hoàn thành' };
  function uniq(fn) { var o = []; L.items.forEach(function (it) { if (it.deleted) return; var v = fn(it); if (v && o.indexOf(v) < 0) o.push(v); }); return o.sort(function (a, b) { return a === 'Bạn' ? -1 : b === 'Bạn' ? 1 : a.localeCompare(b, 'vi'); }); }
  function projOf(it) { return it.common ? 'Việc chung của phòng' : it.proj; }
  // ---- thay ô chọn tĩnh trong popover bằng ô chọn thật ----
  pop.querySelectorAll('.form-row > div').forEach(function (d) {
    var lab = (d.querySelector('.ff__text') || d.querySelector('.v2-label__text') || d).textContent.trim(), k = null;
    if (/^Người (thực hiện|xử lý|làm)/.test(lab)) k = 'who'; else if (/^Người (giao|tạo)/.test(lab)) k = 'cr'; else if (/^Trạng thái/.test(lab)) k = 'st';
    else if (/^Mức độ ưu tiên/.test(lab)) k = 'pri'; else if (/^(Hạn|Ngày tạo)/.test(lab)) k = 'due'; else if (/^Dự án/.test(lab)) k = 'proj';
    if (!k) return;
    // giữ khung trường thật (.ff + nhãn nổi .ff__label), chỉ thay phần điều khiển tĩnh trong .ff__control
    var t = d.querySelector('.ff__text') || d.querySelector('.v2-label__text'); if (t) t.textContent = LBL[k];
    var ctl = d.querySelector('.ff__control');
    if (!ctl) { ctl = document.createElement('div'); ctl.className = 'ff__control'; (d.querySelector('.ff') || d).appendChild(ctl); }
    ctl.innerHTML = k === 'due' ? '<div class="mk-frange"><input type="date" class="form-control form-control-sm mk-nctl" data-fk="from" title="Từ ngày"><span>→</span><input type="date" class="form-control form-control-sm mk-nctl" data-fk="to" title="Đến ngày"></div>'
      : '<select class="form-control form-control-sm mk-nctl" data-fk="' + k + '"></select>';
    d.classList.add('mk-ffld');
  });
  function fillSelects() {
    var src = { who: uniq(function (it) { return it.who; }), cr: uniq(function (it) { return it.cr; }), st: L.items.filter(function (it) { return !it.deleted; }).map(function (it) { return it.st; }).filter(function (v, i, a) { return a.indexOf(v) === i; }), pri: uniq(function (it) { return it.pri.t; }), proj: uniq(projOf) };
    pop.querySelectorAll('select[data-fk]').forEach(function (sel) { var k = sel.getAttribute('data-fk'); sel.innerHTML = '<option value="">Tất cả</option>' + (src[k] || []).map(function (v) { return '<option' + (v === F[k] ? ' selected' : '') + '>' + esc(v) + '</option>'; }).join(''); });
    pop.querySelectorAll('input[data-fk]').forEach(function (i) { i.value = F[i.getAttribute('data-fk')] || ''; });
  }
  // ---- điều kiện ----
  function iso(d) { return d ? d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0') : ''; }
  function passF(it) {
    if (A.who && it.who !== A.who) return false; if (A.cr && it.cr !== A.cr) return false; if (A.st && it.st !== A.st) return false;
    if (A.pri && it.pri.t !== A.pri) return false; if (A.proj && projOf(it) !== A.proj) return false;
    if (A.from && (!it.d || iso(it.d) < A.from)) return false; if (A.to && (!it.d || iso(it.d) > A.to)) return false;
    if (Q) { var h = (it.name + ' ' + (it.x.code || '') + ' ' + projOf(it) + ' ' + it.who).toLowerCase(); if (h.indexOf(Q) < 0) return false; }
    return true;
  }
  function chipOf(txt) { return /^Tất cả/.test(txt) ? 'all' : /^Của tôi/.test(txt) ? 'mine' : /^Quá hạn/.test(txt) ? 'od' : /^Chờ tôi duyệt/.test(txt) ? 'appr' : /^Đang mở/.test(txt) ? 'open' : null; }
  function passC(it, c) {
    if (c === 'mine') return it.who === 'Bạn' || (isI && it.cr === 'Bạn');   // Vấn đề: tôi xử lý hoặc tôi báo
    if (c === 'od') return L.dueCls(it) === 'od';
    if (c === 'appr') return (it.st === 'Hoàn thành - Chờ duyệt' || it.st === 'Đã xử lý xong') && it.rv === 'Bạn';
    if (c === 'open') return !L.done(it) && it.st !== 'Đã xử lý xong';
    return true;
  }
  var ft = pop.querySelector('.mk-fp-ft');
  if (ft) {
    var dv = [].slice.call((ft.querySelector('button') || ft).attributes).filter(function (x) { return /^data-v-/.test(x.name); }).map(function (x) { return x.name + '=""'; }).join(' ');
    ft.innerHTML = '<button type="button" ' + dv + ' class="v2-btn v2-btn--sm v2-btn--primary v2-btn--primary-info v2-btn--prefix-sm" data-fa="search"><div class="v2-btn__prefix--sm"><i class="ri-search-line"></i></div> Tìm kiếm</button>' +
      '<button type="button" ' + dv + ' class="v2-btn v2-btn--sm v2-btn--tertiary v2-btn--tertiary-info v2-btn--prefix-sm" data-fa="reset"><div class="v2-btn__prefix--sm"><i class="ri-refresh-line"></i></div> Làm mới</button>';
  }
  window.__mkPass = function (it) { return !it.deleted && passF(it) && passC(it, CHIP); };
  function nActive() { var n = 0; ['who', 'cr', 'st', 'pri', 'proj'].forEach(function (k) { if (A[k]) n++; }); if (A.from || A.to) n++; return n; }
  // ---- vẽ lại mọi thứ ----
  var chips = [].slice.call(tb.querySelectorAll('.mk-tb-chips .due-pill'));
  function refresh() {
    var n = nActive(); window.__mkFiltering = !!(n || Q || CHIP !== 'all');
    chips.forEach(function (p) { var c = chipOf(p.getAttribute('data-l') || p.textContent.trim()); if (!c) return; if (!p.getAttribute('data-l')) p.setAttribute('data-l', p.textContent.split(':')[0].trim());
      var cnt = L.items.filter(function (it) { return !it.deleted && passF(it) && passC(it, c); }).length; p.textContent = p.getAttribute('data-l') + ': ' + cnt; p.classList.toggle('mk-chip-on', c === CHIP); });
    var fc = tb.querySelector('.mk-fcount'); if (fc) { fc.textContent = n; fc.style.display = n ? '' : 'none'; }
    b.classList.toggle('mk-filtered', n > 0);
    if (afl) {
      var parts = [];
      ['who', 'cr', 'st', 'pri', 'proj'].forEach(function (k) { if (A[k]) parts.push('<span class="mk-af" data-rm="' + k + '">' + LBL[k] + ': <b>' + esc(A[k]) + '</b><i class="ri-close-line"></i></span>'); });
      if (A.from || A.to) parts.push('<span class="mk-af" data-rm="due">' + LBL.due + ': <b>' + (A.from ? A.from.split('-').reverse().join('/') : '…') + ' → ' + (A.to ? A.to.split('-').reverse().join('/') : '…') + '</b><i class="ri-close-line"></i></span>');
      afl.innerHTML = parts.join('') + (parts.length ? '<span class="mk-af-clear" data-rm="all"><i class="ri-refresh-line"></i> Làm mới</span>' : '');
    }
    // bảng: ẩn dòng không khớp + đánh lại STT + chân bảng
    var shown = 0;
    L.items.forEach(function (it) { if (!it.tr || !it.tr.parentNode) return; var ok = window.__mkPass(it); it.tr.style.display = ok ? '' : 'none'; if (ok) { shown++; it.tr.children[0].textContent = shown; } });
    var tbody = document.querySelector('.mk-flat tbody'), emp = document.querySelector('.mk-tbl-empty');
    if (tbody && !shown && !emp) { var tr = document.createElement('tr'); tr.className = 'mk-tbl-empty'; tr.innerHTML = '<td colspan="20">Không có ' + N + ' phù hợp với điều kiện lọc.</td>'; tbody.appendChild(tr); }
    if (emp && shown) emp.remove();
    var foot = document.querySelector('.mk-flat .tp-small-text'); if (foot) foot.textContent = shown ? 'Hiển thị 1–' + shown + ' / ' + shown + (window.__mkFiltering ? ' (đang lọc)' : '') : 'Không có dữ liệu';
    L.render();
  }
  // ---- sự kiện ----
  var qi = tb.querySelector('.quick-search input'); if (qi) qi.addEventListener('input', function () { Q = qi.value.trim().toLowerCase(); refresh(); });
  chips.forEach(function (p) { p.style.cursor = 'pointer'; p.addEventListener('click', function (e) { e.stopImmediatePropagation(); var c = chipOf(p.getAttribute('data-l') || p.textContent); CHIP = CHIP === c && c !== 'all' ? 'all' : c; refresh(); }, true); });
  pop.addEventListener('change', function (e) { var x = e.target.closest('[data-fk]'); if (x) F[x.getAttribute('data-fk')] = x.value; });
  pop.addEventListener('click', function (e) {
    var btn = e.target.closest('.mk-fp-ft button'); if (!btn) return;
    e.stopPropagation(); e.preventDefault();
    if (btn.getAttribute('data-fa') === 'search') { pop.querySelectorAll('[data-fk]').forEach(function (x) { F[x.getAttribute('data-fk')] = x.value; }); A = JSON.parse(JSON.stringify(F)); }
    else { F = { who: '', cr: '', st: '', pri: '', proj: '', from: '', to: '' }; A = JSON.parse(JSON.stringify(F)); fillSelects(); }
    b.classList.remove('mk-filter-open'); refresh();
    L.toast('<i class="ri-filter-3-line"></i> ' + (nActive() ? 'Đang lọc ' + nActive() + ' điều kiện' : 'Đã làm mới bộ lọc'));
  }, true);
  if (afl) afl.addEventListener('click', function (e) {
    var x = e.target.closest('[data-rm]'); if (!x) return; e.stopImmediatePropagation();
    var k = x.getAttribute('data-rm');
    if (k === 'all') { F = { who: '', cr: '', st: '', pri: '', proj: '', from: '', to: '' }; }
    else if (k === 'due') { F.from = ''; F.to = ''; } else F[k] = '';
    A = JSON.parse(JSON.stringify(F)); fillSelects(); refresh();
  }, true);
  // mở popover: nạp lại lựa chọn theo dữ liệu hiện tại (có việc mới tạo)
  var fbtn = tb.querySelector('.mk-filter-btn'); if (fbtn) fbtn.addEventListener('click', function () { F = JSON.parse(JSON.stringify(A)); fillSelects(); }, true);
  fillSelects(); refresh();
})();

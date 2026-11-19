// U19b: Nhiệm vụ / Vấn đề — Danh sách nhóm (mặc định) · Bảng.
// Dữ liệu lấy từ chính các dòng của bảng + phần bổ sung (mã, tiến độ, bình luận, file…) ở EXTRA.
// Đổi trạng thái mô phỏng theo getAllowedNextStatuses() của BE, người xem = "Bạn".
(function () {
  var sec = document.querySelector('.mk-flat'), table = sec && sec.querySelector('table'), tb = document.querySelector('.mk-tb');
  if (!sec || !table || !tb) return;
  var key = decodeURIComponent(location.pathname.split('/').pop()).replace(/\.html$/, '');
  var ths = [].slice.call(table.querySelectorAll('thead th')).map(function (t) { return t.textContent.trim(); });
  function col(re) { for (var i = 0; i < ths.length; i++) if (re.test(ths[i])) return i; return -1; }
  var C = { name: col(/^Tên/), proj: col(/^Dự án$/), st: col(/^Trạng thái/), pri: col(/^Ưu tiên/), who: col(/^Người (làm|xử lý)/), rv: col(/^Người duyệt/), cr: col(/^Người tạo/), due: col(/^Hạn/), ck: col(/^Checklist/) };
  var isIssue = /vấn đề/i.test(ths[C.name] || '');
  var NOUN = isIssue ? 'vấn đề' : 'nhiệm vụ';
  var SC = { 'Nháp': '#94a3b8', 'Chờ phê duyệt triển khai': '#8b5cf6', 'Chờ bắt đầu': '#64748b', 'Đang thực hiện': '#2563eb', 'Tạm dừng': '#f59e0b', 'Hoàn thành - Chờ duyệt': '#d97706',
    'Từ chối kết quả': '#dc2626', 'Hoàn thành': '#16a34a', 'Huỷ': '#94a3b8', 'Từ chối triển khai': '#dc2626',
    'Mới ghi nhận': '#64748b', 'Đã phân công': '#0ea5e9', 'Đang xử lý': '#2563eb', 'Đã xử lý xong': '#16a34a', 'Đã đóng': '#475569', 'Mở lại': '#d97706', 'Từ chối': '#dc2626' };
  var ORDER = isIssue ? ['Mở lại', 'Đang xử lý', 'Đã phân công', 'Mới ghi nhận', 'Đã xử lý xong', 'Hoàn thành', 'Đã đóng', 'Từ chối']
    : ['Đang thực hiện', 'Hoàn thành - Chờ duyệt', 'Từ chối kết quả', 'Tạm dừng', 'Chờ bắt đầu', 'Chờ phê duyệt triển khai', 'Nháp', 'Hoàn thành', 'Từ chối triển khai', 'Huỷ'];
  var DONE = isIssue ? ['Hoàn thành', 'Đã đóng'] : ['Hoàn thành', 'Huỷ', 'Từ chối triển khai'];
  var SUBMITTED = ['Đã xử lý xong', 'Hoàn thành - Chờ duyệt'];
  var ICON = { 'Nháp': 'ri-draft-line', 'Chờ phê duyệt triển khai': 'ri-hourglass-line', 'Chờ bắt đầu': 'ri-checkbox-blank-circle-line', 'Đang thực hiện': 'ri-contrast-2-line',
    'Tạm dừng': 'ri-pause-circle-line', 'Hoàn thành - Chờ duyệt': 'ri-time-line', 'Từ chối kết quả': 'ri-arrow-go-back-line', 'Hoàn thành': 'ri-checkbox-circle-fill',
    'Huỷ': 'ri-close-circle-line', 'Từ chối triển khai': 'ri-close-circle-line', 'Mới ghi nhận': 'ri-checkbox-blank-circle-line', 'Đã phân công': 'ri-user-follow-line',
    'Đang xử lý': 'ri-contrast-2-line', 'Đã xử lý xong': 'ri-check-double-line', 'Đã đóng': 'ri-checkbox-circle-fill', 'Mở lại': 'ri-refresh-line', 'Từ chối': 'ri-close-circle-line' };
  // Phần bổ sung mà bảng không có cột (khi code: API danh sách trả sẵn)
  var EXTRA = {
    'Báo giá may đồng phục 3 nhà cung cấp': { code: 'TPE.TASK.NB.26.0141', start: '28/10', pct: 50, cmt: 4, file: 3, upd: '2 giờ trước', tags: ['Mua sắm'] },
    'Chốt danh sách size sơ mi toàn công ty': { code: 'TPE.TASK.NB.26.0142', start: '05/11', pct: 0, cmt: 1, file: 1, upd: 'Hôm qua' },
    'Đặt hội trường hội nghị': { code: 'TPE.TASK.NB.26.0150', start: '01/11', pct: 40, cmt: 6, file: 2, upd: '30 phút trước', tags: ['Sự kiện'] },
    'Gia hạn hợp đồng vệ sinh toà nhà': { code: 'TPE.TASK.NB.26.0118', start: '20/10', pct: 70, cmt: 2, file: 1, upd: '3 giờ trước', tags: ['Hợp đồng'] },
    'Cập nhật nội quy văn phòng 2027': { code: 'TPE.TASK.NB.26.0127', start: '25/10', pct: 100, cmt: 3, file: 1, upd: 'Hôm qua' },
    'Kiểm kê bàn ghế tầng 2': { code: 'TPE.TASK.NB.26.0096', start: '15/09', pct: 100, cmt: 5, file: 4, upd: '28/09' },
    'Máy in tầng 3 kẹt giấy liên tục': { code: 'ISS-202611-0004', cmt: 3, file: 2, upd: '1 giờ trước', tags: ['Thiết bị'] },
    'Điều hoà phòng họp nhỏ không mát': { code: 'ISS-202610-0031', cmt: 5, file: 1, upd: 'Hôm qua', tags: ['Thiết bị'] },
    'Nhà cung cấp B giao thiếu size XL': { code: 'ISS-202611-0006', cmt: 2, file: 3, upd: '20 phút trước', tags: ['Mua sắm'] },
    'Thiếu phòng họp cho hội nghị ngày 15/01': { code: 'ISS-202611-0007', cmt: 0, file: 0, upd: '2 giờ trước' },
    'Sai lệch số liệu kiểm kê bàn ghế tầng 2': { code: 'ISS-202609-0018', cmt: 4, file: 2, upd: '29/09' }
  };
  var TODAY = new Date(2026, 10, 3);
  function cell(tr, i) { return i >= 0 ? tr.children[i] : null; }
  function tx(e) { return e ? e.textContent.replace(/\s+/g, ' ').trim() : ''; }
  function badge(td) { var b = td && td.querySelector('[class*=badge]'); return b ? { t: tx(b), c: getComputedStyle(b).color } : { t: tx(td), c: '#64748b' }; }
  function pd(s) { var m = /(\d\d)\/(\d\d)\/(\d{4})/.exec(s); return m ? new Date(+m[3], m[2] - 1, +m[1]) : null; }
  function person(s) { return s.replace(/^\d+\s*-\s*/, ''); }
  var items = [].slice.call(table.querySelectorAll('tbody tr')).map(function (tr) {
    var nm = cell(tr, C.name), a = nm && nm.querySelector('a'), name = tx(nm);
    return { tr: tr, a: a, name: name, x: EXTRA[name] || {}, proj: tx(cell(tr, C.proj)).replace(/^—\s*/, ''), common: /^—/.test(tx(cell(tr, C.proj))),
      st: tx(cell(tr, C.st)), pri: badge(cell(tr, C.pri)), who: person(tx(cell(tr, C.who))), rv: person(tx(cell(tr, C.rv))), cr: person(tx(cell(tr, C.cr))),
      due: tx(cell(tr, C.due)), d: pd(tx(cell(tr, C.due))), ck: tx(cell(tr, C.ck)) };
  });
  function initials(n) { if (n === 'Bạn') return 'B'; var p = n.split(' ').filter(Boolean); return (p.length > 1 ? p[p.length - 2][0] + p[p.length - 1][0] : (p[0] || '?').slice(0, 2)).toUpperCase(); }
  var AVC = ['#f472b6', '#60a5fa', '#34d399', '#fbbf24', '#a78bfa', '#fb923c', '#22d3ee'];
  function avc(n) { var h = 0; for (var i = 0; i < n.length; i++) h = (h * 31 + n.charCodeAt(i)) % 997; return n === 'Bạn' ? '#1abc9c' : AVC[h % AVC.length]; }
  function done(it) { return DONE.indexOf(it.st) >= 0; }
  function settled(it) { return done(it) || SUBMITTED.indexOf(it.st) >= 0; }
  function diffDays(it) { return it.d ? Math.round((it.d - TODAY) / 864e5) : null; }
  function dueCls(it) { var d = diffDays(it); if (d === null || settled(it)) return ''; return d < 0 ? 'od' : d <= 3 ? 'soon' : ''; }
  function dueSub(it) { var d = diffDays(it); if (d === null || settled(it)) return ''; return d < 0 ? 'Quá ' + (-d) + ' ngày' : d === 0 ? 'Hôm nay' : 'Còn ' + d + ' ngày'; }
  // ---- luật đổi trạng thái (mô phỏng getAllowedNextStatuses, người xem = Bạn) ----
  function nexts(it) {
    var me = 'Bạn', A = it.as ? it.as === 'who' : it.who === me, Cr = it.as ? it.as === 'cr' : it.cr === me, R = it.as ? it.as === 'rv' : it.rv === me, hasRv = !!it.rv && it.rv !== '—';
    if (!isIssue) switch (it.st) {
      case 'Nháp': return Cr ? ['Chờ bắt đầu', 'Chờ phê duyệt triển khai', 'Đang thực hiện'] : [];
      case 'Chờ bắt đầu': return (A ? ['Đang thực hiện'] : []).concat(A || Cr ? ['Tạm dừng'] : []);
      case 'Đang thực hiện': return (A || Cr ? ['Tạm dừng'] : []).concat(A ? [hasRv ? 'Hoàn thành - Chờ duyệt' : 'Hoàn thành'] : []);
      case 'Tạm dừng': return A || Cr ? ['Đang thực hiện', 'Chờ bắt đầu'] : [];
      case 'Hoàn thành - Chờ duyệt': return R ? ['Hoàn thành', 'Từ chối kết quả'] : [];
      case 'Từ chối kết quả': return A ? ['Đang thực hiện', 'Tạm dừng'] : [];
      case 'Hoàn thành': return Cr ? ['Từ chối kết quả'] : [];
      default: return [];
    }
    switch (it.st) {
      case 'Mới ghi nhận': return (Cr ? ['Đã phân công'] : []).concat(A ? ['Đang xử lý'] : []).concat(A || Cr ? ['Đã đóng'] : []);
      case 'Đã phân công': return (A ? ['Đang xử lý'] : []).concat(A || Cr ? ['Đã đóng'] : []);
      case 'Đang xử lý': return (A ? ['Đã xử lý xong'] : []).concat(A || Cr ? ['Đã đóng'] : []);
      case 'Đã xử lý xong': return (R ? ['Hoàn thành', 'Từ chối'] : []).concat(A || Cr ? ['Đã đóng'] : []);
      case 'Từ chối': return (A ? ['Đang xử lý'] : []).concat(A || Cr ? ['Đã đóng'] : []);
      case 'Hoàn thành': return A || Cr ? ['Mở lại'] : [];
      case 'Mở lại': return (Cr ? ['Đã phân công'] : []).concat(A ? ['Đang xử lý'] : []).concat(A || Cr ? ['Đã đóng'] : []);
      default: return [];
    }
  }
  // nút hành động chính theo ngữ cảnh (chỉ hiện khi người xem làm được)
  function primary(it) {
    var n = nexts(it);
    var P = isIssue ? [['Đang xử lý', 'Nhận xử lý', 'ri-play-line'], ['Đã xử lý xong', 'Báo đã xử lý', 'ri-check-double-line'], ['Mở lại', 'Mở lại', 'ri-refresh-line']]
      : [['Chờ bắt đầu', 'Giao việc', 'ri-send-plane-2-line'], ['Đang thực hiện', 'Bắt đầu', 'ri-play-line'], ['Hoàn thành - Chờ duyệt', 'Báo kết quả', 'ri-send-plane-line'], ['Hoàn thành', it.st === 'Hoàn thành - Chờ duyệt' ? 'Duyệt' : 'Hoàn thành', 'ri-check-line']];
    for (var i = 0; i < P.length; i++) if (n.indexOf(P[i][0]) >= 0) return P[i];
    return null;
  }
  // trường phụ cấu hình hiện / ẩn (mặc định: dưới tên chỉ Người giao + Cập nhật)
  var FIELDS = [['code', 'Mã ' + NOUN, 'Cạnh tên', 0], ['tags', 'Tag', 'Cạnh tên', 1], ['cr', isIssue ? 'Người báo' : 'Người giao', 'Dưới tên', 1], ['upd', 'Thời gian cập nhật', 'Dưới tên', 1],
    ['proj', 'Dự án', 'Dưới tên', 0], ['rv', 'Người duyệt', 'Dưới tên', 0], ['file', 'Số file đính kèm', 'Dưới tên', 0]];
  if (isIssue) FIELDS = FIELDS.filter(function (f) { return f[0] !== 'rv'; });
  var SHOW = {}; FIELDS.forEach(function (f) { SHOW[f[0]] = !!f[3]; });
  try { var sv = JSON.parse(localStorage.getItem('mk-lvf-' + (isIssue ? 'iss' : 'task')) || 'null'); if (sv) for (var k0 in sv) if (k0 in SHOW) SHOW[k0] = sv[k0]; } catch (e) {}
  var spaceName = (document.querySelector('.mk-ntb-nm') || {}).textContent || 'không gian này';
  var SCOPE = 'Phạm vi: ' + NOUN + ' của ' + spaceName + ' và các dự án nội bộ thuộc phòng mà bạn được xem; tính theo ô tìm, chip và bộ lọc đang áp dụng.';
  var WHY = isIssue ? {
    'Mới ghi nhận': ['Vấn đề vừa được báo, chưa có ai nhận xử lý.', 'Người báo phân công người xử lý, hoặc người xử lý bấm Nhận xử lý.'],
    'Đã phân công': ['Đã có người xử lý nhưng người đó chưa bắt đầu.', 'Người xử lý bấm Nhận xử lý → Đang xử lý.'],
    'Đang xử lý': ['Người xử lý đang xử lý, chưa báo xong.', 'Người xử lý báo Đã xử lý xong (có người duyệt) hoặc Hoàn thành (không có người duyệt).'],
    'Đã xử lý xong': ['Người xử lý đã báo xong, đang chờ người duyệt xác nhận. Không tính quá hạn.', 'Người duyệt chọn Hoàn thành hoặc Từ chối.'],
    'Từ chối': ['Người duyệt không chấp nhận kết quả xử lý.', 'Người xử lý xử lý lại → Đang xử lý.'],
    'Mở lại': ['Vấn đề đã hoàn thành nhưng được mở lại vì chưa ổn.', 'Người báo phân công lại, hoặc người xử lý nhận xử lý tiếp.'],
    'Hoàn thành': ['Đã xử lý xong và được xác nhận (hoặc không cần người duyệt).', 'Người báo / người xử lý có thể Mở lại nếu phát sinh lại.'],
    'Đã đóng': ['Vấn đề đã đóng, không xử lý nữa.', 'Không chuyển tiếp được.']
  } : {
    'Nháp': ['Người tạo đang soạn, chưa giao chính thức.', 'Người tạo gửi đi: Chờ bắt đầu, Chờ phê duyệt triển khai hoặc Đang thực hiện.'],
    'Chờ phê duyệt triển khai': ['Nhiệm vụ cần được duyệt trước khi làm.', 'Quản lý phòng ban của người làm (có quyền duyệt triển khai) duyệt → Chờ bắt đầu, hoặc Từ chối triển khai.'],
    'Từ chối triển khai': ['Không được duyệt triển khai.', 'Người tạo chỉnh lại và gửi duyệt lại.'],
    'Chờ bắt đầu': ['Đã giao, người làm chưa bấm Bắt đầu.', 'Người làm bấm Bắt đầu → Đang thực hiện.'],
    'Đang thực hiện': ['Người làm đã bắt đầu, chưa báo kết quả. Việc quá hạn vẫn nằm ở nhóm này (tô đỏ).', 'Người làm Báo kết quả → Hoàn thành - Chờ duyệt (có người duyệt) hoặc Hoàn thành (không có người duyệt).'],
    'Tạm dừng': ['Người làm hoặc người giao tạm dừng.', 'Người làm / người giao cho làm tiếp → Đang thực hiện.'],
    'Hoàn thành - Chờ duyệt': ['Người làm đã báo kết quả, đang chờ người duyệt. Không tính quá hạn.', 'Người duyệt chọn Duyệt → Hoàn thành, hoặc Từ chối kết quả.'],
    'Từ chối kết quả': ['Người duyệt trả lại kết quả.', 'Người làm làm tiếp → Đang thực hiện.'],
    'Hoàn thành': ['Đã được duyệt kết quả (hoặc không cần duyệt).', 'Người giao có thể trả lại nếu cần làm thêm.'],
    'Huỷ': ['Nhiệm vụ đã huỷ.', 'Không làm tiếp.']
  };
  var WHY_DUE = {
    'Hôm nay': ['Hạn hoàn thành là hôm nay, chưa xong.', ''],
    'Quá hạn': ['Hạn hoàn thành trước hôm nay, chưa xong và chưa nộp kết quả.', ''],
    '7 ngày tới': ['Hạn trong 7 ngày tới (từ ngày mai), chưa xong.', ''],
    'Sau đó': ['Hạn sau 7 ngày nữa, chưa xong.', ''],
    'Không có hạn': ['Chưa đặt hạn hoàn thành.', ''],
    'Chờ duyệt / chờ đóng': ['Đã nộp kết quả (' + (isIssue ? 'Đã xử lý xong' : 'Hoàn thành - Chờ duyệt') + '), đang chờ người khác xác nhận — không tính quá hạn.', ''],
    'Đã xong': ['Đã hoàn thành' + (isIssue ? ' hoặc đã đóng.' : ', huỷ hoặc từ chối triển khai.'), '']
  };
  function whyHtml(by, k) {
    var w = by === 'st' ? WHY[k] : by === 'due' ? WHY_DUE[k] : by === 'who' ? ['Các ' + NOUN + ' có ' + (isIssue ? 'người xử lý' : 'người làm') + ' là ' + k + '.', ''] :
      [k === 'Việc chung của phòng' ? 'Các ' + NOUN + ' gắn thẳng vào phòng, không thuộc dự án nội bộ nào.' : 'Các ' + NOUN + ' thuộc dự án nội bộ ' + k + '.', ''];
    if (!w) return '';
    return '<b>' + esc(k) + '</b><p>' + esc(w[0]) + '</p>' + (w[1] ? '<p class="nx"><i class="ri-arrow-right-line"></i>' + esc(w[1]) + '</p>' : '') + '<p class="sc">' + esc(SCOPE) + '</p>';
  }
  var tip = document.createElement('div'); tip.className = 'mk-ltip'; document.body.appendChild(tip);
  function showTip(el) {
    var g = el.closest('.mk-lg'), fk = g.getAttribute('data-k'), i = fk.indexOf(':');
    tip.innerHTML = whyHtml(fk.slice(0, i), fk.slice(i + 1)); tip.classList.add('on');
    var r = el.getBoundingClientRect(), top = r.bottom + 8;
    if (top + tip.offsetHeight > innerHeight - 8) top = r.top - tip.offsetHeight - 8;
    tip.style.left = Math.min(Math.max(8, r.left - 16), innerWidth - tip.offsetWidth - 8) + 'px'; tip.style.top = top + 'px';
  }
  document.addEventListener('mouseover', function (e) { var el = e.target.closest && e.target.closest('.mk-lg-info'); if (el) showTip(el); else if (!e.target.closest || !e.target.closest('.mk-ltip')) tip.classList.remove('on'); });
  window.addEventListener('scroll', function () { tip.classList.remove('on'); }, true);
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
  function rowHtml(it, i) {
    var x = it.x, hi = /Cao|Khẩn cấp/.test(it.pri.t), ck = /^(\d+)\/(\d+)$/.exec(it.ck), sc = SC[it.st] || '#64748b', p = primary(it), canSt = nexts(it).length;
    var meta = [];
    if (SHOW.cr && it.cr) meta.push('<span title="' + (isIssue ? 'Người báo' : 'Người giao') + '"><i class="ri-user-add-line"></i>' + (isIssue ? 'Báo: ' : 'Giao: ') + esc(it.cr) + '</span>');
    if (SHOW.rv && !isIssue && it.rv && it.rv !== '—') meta.push('<span title="Người duyệt kết quả"><i class="ri-shield-check-line"></i>Duyệt: ' + esc(it.rv) + '</span>');
    if (SHOW.proj) meta.push('<span class="mk-m-pj' + (it.common ? ' mk-m-common' : '') + '" title="Dự án"><i class="' + (it.common ? 'ri-community-line' : 'ri-folders-line') + '"></i>' + esc(it.proj) + '</span>');
    if (SHOW.file && x.file) meta.push('<span title="File đính kèm"><i class="ri-attachment-2"></i>' + x.file + '</span>');
    if (SHOW.upd && x.upd) meta.push('<span class="mk-m-upd" title="Cập nhật gần nhất"><i class="ri-time-line"></i>' + esc(x.upd) + '</span>');
    var tags = (SHOW.tags ? x.tags || [] : []).map(function (t) { return '<span class="mk-lr-tag">' + esc(t) + '</span>'; }).join('');
    var pct = x.pct != null ? x.pct : null;
    return '<div class="mk-lr' + (it.tr.classList.contains('mk-fx') ? ' mk-fx' : '') + (done(it) ? ' mk-lr-done' : '') + '" data-i="' + i + '" style="--sc:' + sc + '">' +
      '<button type="button" class="mk-lr-st' + (canSt ? '' : ' ro') + '" title="' + esc(it.st) + (canSt ? ' — bấm để đổi trạng thái' : ' — bạn không đổi được trạng thái') + '"><i class="' + (ICON[it.st] || 'ri-checkbox-blank-circle-line') + '"></i></button>' +
      '<div class="mk-lr-main"><div class="mk-lr-l1">' + (SHOW.code && x.code ? '<span class="mk-lr-code">' + esc(x.code) + '</span>' : '') +
        '<a href="javascript:void(0)" class="mk-link mk-lr-title">' + esc(it.name) + '</a>' +
        (hi ? '<span class="mk-lr-pri" style="--pc:' + it.pri.c + '"><i class="ri-flag-2-fill"></i>' + esc(it.pri.t) + '</span>' : '') + tags + '</div>' +
        (meta.length ? '<div class="mk-lr-l2">' + meta.join('<i class="mk-dot"></i>') + '</div>' : '') + '</div>' +
      '<div class="mk-lr-who" title="' + (isIssue ? 'Người xử lý' : 'Người làm') + ': ' + esc(it.who) + '"><i class="mk-lr-av" style="background:' + avc(it.who) + '">' + esc(initials(it.who)) + '</i><span>' + esc(it.who) + '</span></div>' +
      (pct != null ? '<div class="mk-lr-pct" title="Tiến độ · checklist"><div><b style="--p:' + pct + '%"></b><span>' + pct + '%</span></div>' +
          (ck ? '<small><i class="ri-checkbox-line"></i>' + it.ck + ' việc con</small>' : '<small class="mk-lr-none">Không có checklist</small>') + '</div>' :
        '<div class="mk-lr-pct"><span class="mk-lr-stx" style="color:' + sc + '">' + esc(it.st) + '</span></div>') +
      '<div class="mk-lr-due ' + dueCls(it) + (it.due ? '' : ' none') + '" title="Bấm để ' + (it.as ? it.as === 'cr' : it.cr === 'Bạn') + '"><span><i class="ri-calendar-line"></i>' + (it.due ? (x.start ? esc(x.start) + ' → ' : '') + esc(it.due.slice(0, 5)) : 'Chưa có hạn') + '<i class="ri-pencil-line mk-due-ed"></i></span>' +
        (it.ext ? '<small class="mk-due-ext"><i class="ri-hourglass-line"></i>Đề nghị → ' + esc(it.ext.to.slice(0, 5)) + '</small>' : dueSub(it) ? '<small>' + dueSub(it) + '</small>' : '') + '</div>' +
      '<div class="mk-lr-act">' + (p ? '<button type="button" class="mk-act-p" data-to="' + esc(p[0]) + '" data-tip="' + p[1] + '" aria-label="' + p[1] + '"><i class="' + p[2] + '"></i></button>' : '<span class="mk-act-gap"></span>') +
        '<button type="button" class="mk-act-i" data-a="cmt" data-tip="Bình luận' + (x.cmt ? ' (' + x.cmt + ')' : '') + '" aria-label="Bình luận"><i class="ri-chat-3-line"></i>' + (x.cmt ? '<em>' + x.cmt + '</em>' : '') + '</button>' +
        '<button type="button" class="mk-act-i" data-a="more" data-tip="Thao tác khác" aria-label="Thao tác khác"><i class="ri-more-2-fill"></i></button></div></div>';
  }
  var GB = { st: 'Trạng thái', who: isIssue ? 'Người xử lý' : 'Người làm', due: 'Hạn', proj: 'Dự án' };
  function groups(by) {
    var g = {}, order = [];
    function put(k, it, meta) { if (!g[k]) { g[k] = { k: k, items: [], meta: meta || {} }; order.push(k); } g[k].items.push(it); }
    items.forEach(function (it) {
      if (it.deleted) return;
      if (by === 'st') put(it.st, it, { c: SC[it.st], ic: ICON[it.st], fold: DONE.indexOf(it.st) >= 0 });
      else if (by === 'who') put(it.who, it, { av: it.who, c: avc(it.who) });
      else if (by === 'proj') put(it.common ? 'Việc chung của phòng' : it.proj, it, { ic: it.common ? 'ri-community-line' : 'ri-folders-line', c: it.common ? '#0ea5e9' : '#7c3aed' });
      else {
        var d = diffDays(it), k = done(it) ? 'Đã xong' : SUBMITTED.indexOf(it.st) >= 0 ? 'Chờ duyệt / chờ đóng' : d === null ? 'Không có hạn' : d < 0 ? 'Quá hạn' : d === 0 ? 'Hôm nay' : d <= 7 ? '7 ngày tới' : 'Sau đó';
        put(k, it, { c: { 'Hôm nay': '#0EA5E9', 'Quá hạn': '#dc2626', '7 ngày tới': '#d97706', 'Sau đó': '#2563eb', 'Không có hạn': '#94a3b8', 'Chờ duyệt / chờ đóng': '#d97706', 'Đã xong': '#16a34a' }[k],
          ic: { 'Hôm nay': 'ri-sun-line', 'Quá hạn': 'ri-alarm-warning-line', '7 ngày tới': 'ri-calendar-event-line', 'Sau đó': 'ri-calendar-line', 'Không có hạn': 'ri-calendar-todo-line', 'Chờ duyệt / chờ đóng': 'ri-time-line', 'Đã xong': 'ri-checkbox-circle-line' }[k], fold: k === 'Đã xong' });
      }
    });
    // 04/11: nhóm “Hôm nay” luôn có (kể cả trống) và đứng đầu; “Quá hạn” xuống cuối
    if (by === 'due' && !g['Hôm nay']) { g['Hôm nay'] = { k: 'Hôm nay', items: [], meta: { c: '#0EA5E9', ic: 'ri-sun-line' } }; order.push('Hôm nay'); }
    var ord = by === 'st' ? ORDER : by === 'due' ? ['Hôm nay', '7 ngày tới', 'Sau đó', 'Không có hạn', 'Chờ duyệt / chờ đóng', 'Đã xong', 'Quá hạn'] : by === 'who' ? ['Bạn'] : ['Việc chung của phòng'];
    order.sort(function (a, b) { var ia = ord.indexOf(a), ib = ord.indexOf(b); return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib) || a.localeCompare(b, 'vi'); });
    return order.map(function (k) { return g[k]; });
  }
  // ---- toast + menu nổi dùng chung ----
  function toast(m) { var t = document.querySelector('.mk-p-toast'); if (!t) { t = document.createElement('div'); t.className = 'mk-p-toast'; document.body.appendChild(t); } t.innerHTML = m; t.classList.add('on'); clearTimeout(toast.t); toast.t = setTimeout(function () { t.classList.remove('on'); }, 2200); }
  var pop = document.createElement('div'); pop.className = 'mk-lpop'; document.body.appendChild(pop);
  function showPop(anchor, html) {
    pop.innerHTML = html; pop.classList.add('on');
    var r = anchor.getBoundingClientRect(), w = pop.offsetWidth, h = pop.offsetHeight;
    var left = Math.min(Math.max(8, r.right - w), innerWidth - w - 8), top = r.bottom + 4;
    if (top + h > innerHeight - 8) top = r.top - h - 4;
    pop.style.left = left + 'px'; pop.style.top = top + 'px';
  }
  function hidePop() { pop.classList.remove('on', 'mk-lpop-cfg'); }
  document.addEventListener('click', function (e) { if (!document.contains(e.target)) return; if (!pop.contains(e.target) && !e.target.closest('.mk-lr-st, .mk-act-i, .mk-lg-add') && !(cfgBtn && cfgBtn.contains(e.target))) hidePop(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') hidePop(); });
  window.addEventListener('scroll', hidePop, true);
  // ---- khung danh sách ----
  var lv = document.createElement('div'); lv.className = 'mk-lv';
  var shell = sec.querySelector('.table-shell'); sec.insertBefore(lv, shell);
  var folded = {}, by = 'st';
  var SORTS = [['due', 'Hạn hoàn thành', 'ri-calendar-line', 'asc'], ['pri', 'Mức độ ưu tiên', 'ri-flag-2-line', 'desc'], ['upd', 'Cập nhật gần nhất', 'ri-time-line', 'desc'],
    ['pct', 'Tiến độ', 'ri-line-chart-line', 'asc'], ['name', 'Tên ' + NOUN, 'ri-sort-alphabet-asc', 'asc'], ['who', isIssue ? 'Người xử lý' : 'Người làm', 'ri-user-line', 'asc']];
  if (isIssue) SORTS = SORTS.filter(function (x) { return x[0] !== 'pct'; });
  var SK = 'mk-sort-' + key, sort = { f: 'due', d: 'asc' };
  try { var sv0 = JSON.parse(localStorage.getItem(SK) || 'null'); if (sv0 && sv0.f) sort = sv0; } catch (e) {}
  var PRANK = { 'Khẩn cấp': 4, 'Cao': 3, 'Trung bình': 2, 'Bình thường': 1, 'Thấp': 0 };
  function ago(t) { t = (t || '').toLowerCase(); var m;
    if (!t) return 1e9; if (t === 'vừa xong') return 0; if ((m = /(\d+) phút/.exec(t))) return +m[1]; if ((m = /(\d+) giờ/.exec(t))) return +m[1] * 60; if (/hôm qua/.test(t)) return 1440;
    if ((m = /(\d+) ngày/.exec(t))) return +m[1] * 1440; if ((m = /(\d\d)\/(\d\d)/.exec(t))) return Math.round((TODAY - new Date(2026, m[2] - 1, +m[1])) / 6e4); return 1e8; }
  function cmp(a, b) {
    var f = sort.f, r = 0;
    if (f === 'due') { if (!a.d && !b.d) r = 0; else if (!a.d) return 1; else if (!b.d) return -1; else r = a.d - b.d; }   // không có hạn luôn xuống cuối
    else if (f === 'pri') r = (PRANK[a.pri.t] || 0) - (PRANK[b.pri.t] || 0);
    else if (f === 'upd') r = ago(b.x.upd) - ago(a.x.upd);            // "tăng dần" = cũ → mới
    else if (f === 'pct') r = (a.x.pct || 0) - (b.x.pct || 0);
    else if (f === 'name') r = a.name.localeCompare(b.name, 'vi');
    else if (f === 'who') r = (a.who || '').localeCompare(b.who || '', 'vi');
    r = sort.d === 'asc' ? r : -r;
    return r || a.name.localeCompare(b.name, 'vi');
  }
  function sortLabel() { var x = SORTS.filter(function (q) { return q[0] === sort.f; })[0] || SORTS[0]; return x[1].replace('Hạn hoàn thành', 'Hạn').replace('Mức độ ưu tiên', 'Ưu tiên').replace('Cập nhật gần nhất', 'Cập nhật'); }
  function render() {
    var filt = !!window.__mkFiltering, h = '', total = 0;
    groups(by).forEach(function (g) {
      var vis = g.items.filter(function (it) { return !window.__mkPass || window.__mkPass(it); });
      if (!vis.length && !(by === 'due' && g.k === 'Hôm nay')) return; total += vis.length;
      var fk = by + ':' + g.k, fold = fk in folded ? folded[fk] : !!g.meta.fold;
      var od = vis.filter(function (it) { return dueCls(it) === 'od'; }).length;
      var lead = g.meta.av ? '<i class="mk-lr-av" style="background:' + avc(g.meta.av) + '">' + esc(initials(g.meta.av)) + '</i>' : '<i class="' + (g.meta.ic || 'ri-checkbox-blank-circle-line') + ' mk-lg-ic"></i>';
      h += '<section class="mk-lg' + (fold ? ' fold' : '') + '" data-k="' + esc(fk) + '" style="--gc:' + (g.meta.c || '#64748b') + '"><header class="mk-lg-h"><i class="ri-arrow-down-s-line mk-lg-car"></i>' + lead +
        '<b>' + esc(g.k) + '</b><span class="mk-lg-c">' + vis.length + '</span><i class="ri-information-line mk-lg-info" aria-label="Giải thích nhóm"></i>' + (od && by !== 'due' ? '<span class="mk-lg-od"><i class="ri-alarm-warning-line"></i>' + od + ' quá hạn</span>' : '') +
        '<button type="button" class="mk-lg-add" title="Thêm ' + NOUN + ' vào nhóm này"><i class="ri-add-line"></i>Thêm ' + NOUN + '</button></header><div class="mk-lg-b">' +
        (vis.length ? vis.slice().sort(cmp).map(function (it) { return rowHtml(it, items.indexOf(it)); }).join('') : '<div class="mk-lg-empty"><i class="ri-checkbox-circle-line"></i>Không có ' + NOUN + ' đến hạn hôm nay.</div>') + '</div></section>';
    });
    var qa = ''; // 04/11: bỏ ô thêm nhanh trên bảng
    if (!total) h = '<div class="mk-lv-empty"><i class="ri-search-eye-line"></i><b>Không có ' + NOUN + ' phù hợp</b><span>Thử bỏ bớt điều kiện lọc hoặc đổi từ khoá tìm.</span></div>';
    lv.innerHTML = qa + h + '<div class="mk-lv-ft">' + total + ' ' + NOUN + (filt ? ' (đang lọc)' : '') + ' · gom theo ' + GB[by].toLowerCase() + ' · sắp xếp theo ' + sortLabel().toLowerCase() + (sort.d === 'asc' ? ' tăng dần' : ' giảm dần') + '</div>';
  }
  lv.addEventListener('click', function (e) {
    var t = e.target, row = t.closest('.mk-lr'), it = row && items[+row.getAttribute('data-i')];
    if (t.closest('.mk-lg-add')) { e.stopPropagation(); var gk = t.closest('.mk-lg').getAttribute('data-k'); window.MKTD && MKTD.create({ by: by, k: gk.slice(gk.indexOf(':') + 1) }); return; }
    if (t.closest('.mk-lg-info')) { e.stopPropagation(); showTip(t.closest('.mk-lg-info')); return; }
    if (t.closest('.mk-lg-h')) { var g = t.closest('.mk-lg'), fk = g.getAttribute('data-k'); folded[fk] = !g.classList.contains('fold'); g.classList.toggle('fold', folded[fk]); return; }
    if (!it) return;
    var dc = t.closest('.mk-lr-due'); if (dc && window.MKTD) { e.stopPropagation(); MKTD.due(it, dc); return; }
    if (t.closest('.mk-lr-title')) { e.preventDefault(); window.MKTD && MKTD.open(it, 'detail'); return; }
    var stb = t.closest('.mk-lr-st');
    if (stb) {
      e.stopPropagation(); var n = nexts(it);
      if (!n.length) { showPop(stb, '<div class="mk-lpop-h">' + esc(it.st) + '</div><div class="mk-lpop-note">Bạn không đổi được trạng thái ' + NOUN + ' này' + (it.st === 'Hoàn thành - Chờ duyệt' ? ' — chỉ người duyệt (' + esc(it.rv) + ')' : '') + '.</div>'); return; }
      showPop(stb, '<div class="mk-lpop-h">Chuyển trạng thái</div>' + n.map(function (s) { return '<a data-to="' + esc(s) + '"><i class="' + ICON[s] + '" style="color:' + SC[s] + '"></i>' + esc(s) + '</a>'; }).join('') + '<div class="mk-lpop-note">Theo quyền của bạn trên ' + NOUN + ' này</div>');
      pop.onclick = function (ev) { var a = ev.target.closest('[data-to]'); if (!a) return; hidePop(); (window.MKTD ? MKTD.go : go)(it, a.getAttribute('data-to')); };
      return;
    }
    var pb = t.closest('.mk-act-p'); if (pb) { (window.MKTD ? MKTD.go : go)(it, pb.getAttribute('data-to')); return; }
    var ib = t.closest('.mk-act-i');
    if (ib && ib.getAttribute('data-a') === 'cmt') { window.MKTD && MKTD.open(it, 'cmt'); return; }
    if (ib) {
      e.stopPropagation(); var me = 'Bạn', isCr = it.as ? it.as === 'cr' : it.cr === me, isWho = it.as ? it.as === 'who' : it.who === me, canEdit = isCr, canDel = isCr && it.st === 'Nháp';
      var M = [['ri-eye-line', 'Xem chi tiết'], canEdit ? ['ri-edit-line', 'Sửa'] : null, canEdit ? ['ri-calendar-event-line', 'Đổi hạn'] : isWho && !settled(it) ? ['ri-calendar-event-line', 'Đề nghị gia hạn'] : null, isCr ? ['ri-user-shared-line', isIssue ? 'Giao người xử lý khác' : 'Giao người làm khác'] : null,
        [it.follow ? 'ri-eye-off-line' : 'ri-eye-2-line', it.follow ? 'Bỏ theo dõi' : 'Theo dõi'], ['ri-links-line', 'Sao chép liên kết'], ['ri-history-line', 'Lịch sử thay đổi'], canDel ? ['ri-delete-bin-line', 'Xoá', 'danger'] : null].filter(Boolean);
      showPop(ib, M.map(function (m) { return '<a class="' + (m[2] || '') + '" data-m="' + m[1] + '"><i class="' + m[0] + '"></i>' + m[1] + '</a>'; }).join(''));
      pop.onclick = function (ev) { var a = ev.target.closest('[data-m]'); if (!a) return; hidePop(); menu(it, a.getAttribute('data-m'), ib); };
    }
  });
  function go(it, s) {
    if (window.MKTD && (s === 'Hoàn thành - Chờ duyệt' || s === 'Đã xử lý xong' || (s === 'Hoàn thành' && it.st !== 'Hoàn thành - Chờ duyệt' && it.st !== 'Đã xử lý xong'))) return MKTD.result(it, s);
    if (window.MKTD && (s === 'Từ chối kết quả' || s === 'Từ chối' || s === 'Tạm dừng' || s === 'Mở lại')) return MKTD.reason(it, s);
    if (window.MKTD && (it.st === 'Hoàn thành - Chờ duyệt' || it.st === 'Đã xử lý xong') && s === 'Hoàn thành') return MKTD.open(it, 'res');
    setSt(it, s);
  }
  var PEOPLE = ['Bạn', 'Nguyễn Thị Hằng', 'Trần Văn Minh', 'Lê Thu Trang', 'Phạm Quốc Huy', 'Đỗ Mai Anh', 'Vũ Hoàng Long'];
  function log(it, ic, t) { (it.his = it.his || []).unshift({ ic: ic, t: t, who: 'Bạn', ago: 'Vừa xong' }); }
  function menu(it, m, anchor) {
    if (m === 'Xem chi tiết') return MKTD.open(it, 'detail');
    if (m === 'Lịch sử thay đổi') return MKTD.open(it, 'his');
    if (m === 'Sửa') return MKTD.edit(it);
    if (m === 'Sửa toàn bộ') return MKTD.edit(it);
    if (m === 'Theo dõi' || m === 'Bỏ theo dõi') { it.follow = m === 'Theo dõi'; log(it, 'ri-eye-2-line', it.follow ? 'theo dõi ' + NOUN : 'bỏ theo dõi'); toast('<i class="ri-eye-2-line"></i> ' + (it.follow ? 'Đã theo dõi — bạn sẽ nhận thông báo khi ' + NOUN + ' thay đổi' : 'Đã bỏ theo dõi')); return; }
    if (m === 'Sao chép liên kết') { toast('<i class="ri-links-line"></i> Đã sao chép liên kết ' + NOUN); return; }
    if ((m === 'Đổi hạn' || m === 'Đề nghị gia hạn') && window.MKTD) return MKTD.due(it, anchor);
    if (m === 'Đổi hạn') {
      var cur = it.due.replace(/(\d\d)\/(\d\d)\/(\d{4})/, '$3-$2-$1');
      showPop(anchor, '<div class="mk-lpop-h">Đổi hạn hoàn thành</div><div class="mk-lpop-form"><input type="date" class="form-control form-control-sm" value="' + cur + '"><textarea class="form-control form-control-sm" rows="2" placeholder="Lý do đổi hạn (gửi cho người giao)"></textarea><div class="mk-lpop-btns"><button type="button" class="v2-btn v2-btn--sm v2-btn--primary" data-ok="1">Lưu</button><button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" data-x="1">Huỷ</button></div></div>');
      pop.onclick = function (ev) { if (ev.target.closest('[data-x]')) return hidePop(); if (!ev.target.closest('[data-ok]')) return; var v = pop.querySelector('input').value; if (!v) return; var p = v.split('-'); var old = it.due; it.due = p[2] + '/' + p[1] + '/' + p[0]; it.d = new Date(+p[0], p[1] - 1, +p[2]); log(it, 'ri-calendar-event-line', 'đổi hạn ' + old.slice(0, 5) + ' → ' + it.due.slice(0, 5)); hidePop(); render(); toast('<i class="ri-calendar-check-line"></i> Đã đổi hạn sang ' + it.due); };
      return;
    }
    if (/^Giao /.test(m)) {
      showPop(anchor, '<div class="mk-lpop-h">' + m + '</div>' + PEOPLE.filter(function (p) { return p !== it.who; }).map(function (p) { return '<a data-p="' + p + '"><i class="mk-lr-av" style="background:' + avc(p) + '">' + initials(p) + '</i>' + p + '</a>'; }).join(''));
      pop.onclick = function (ev) { var a = ev.target.closest('[data-p]'); if (!a) return; var old = it.who; it.who = a.getAttribute('data-p'); log(it, 'ri-user-shared-line', 'giao lại ' + old + ' → ' + it.who); hidePop(); render(); toast('<i class="ri-user-shared-line"></i> Đã giao cho ' + it.who + ' — người mới nhận thông báo'); };
      return;
    }
    if (m === 'Xoá') return MKTD.confirmDel(it);
  }
  function setSt(it, s) {
    var old = it.st; it.st = s; if (it.x && s === 'Hoàn thành') it.x.pct = 100; log(it, ICON[s] || 'ri-exchange-line', 'chuyển trạng thái ' + old + ' → ' + s);
    render(); if (window.MKTD) MKTD.refresh();
    toast('<i class="ri-checkbox-circle-line"></i> ' + esc(it.name.slice(0, 40)) + ': ' + esc(old) + ' → <b>' + esc(s) + '</b>');
    var row = lv.querySelector('.mk-lr[data-i="' + items.indexOf(it) + '"]'); if (row) { row.classList.add('mk-lr-flash'); var g = row.closest('.mk-lg'); if (g && g.classList.contains('fold')) { g.classList.remove('fold'); } row.scrollIntoView({ block: 'nearest' }); }
  }
  window.__MKLV = { items: items, isIssue: isIssue, NOUN: NOUN, SC: SC, ICON: ICON, PEOPLE: PEOPLE, nexts: nexts, primary: primary, setSt: setSt, go: go, log: log, render: function () { if (view === 'list') render(); },
    avc: avc, initials: initials, dueCls: dueCls, dueSub: dueSub, done: done, settled: settled, toast: toast, esc: esc, spaceName: spaceName, menu: menu };
  // bảng: bấm tên mở panel chi tiết (chặn handler cũ)
  items.forEach(function (it) { if (it.a) it.a.addEventListener('click', function (e) { e.preventDefault(); e.stopImmediatePropagation(); window.MKTD && MKTD.open(it, 'detail'); }, true); });
  var mkNew = [].slice.call(tb.querySelectorAll('.mk-tb-right button')).find(function (b) { return /Tạo mới|Tạo vấn đề/.test(b.textContent); });
  if (mkNew) mkNew.addEventListener('click', function (e) { if (!window.MKTD) return; e.preventDefault(); e.stopImmediatePropagation(); MKTD.create({}); }, true);
  lv.addEventListener('keydown', function (e) { var q = e.target.closest && e.target.closest('[data-qa]'); if (!q || e.key !== 'Enter' || !q.value.trim() || !window.MKTD) return; MKTD.quick(q.value.trim()); });
  new MutationObserver(function () { if (view === 'list') render(); }).observe(document.body, { attributes: true, attributeFilter: ['class'] });
  // ---- công tắc cách xem + Gom theo ----
  var right = tb.querySelector('.mk-tb-right');
  var ctl = document.createElement('div'); ctl.className = 'mk-vctl';
  ctl.innerHTML = '<div class="mk-gb"><button type="button" class="mk-gb-btn" title="Gom nhóm danh sách"><i class="ri-stack-line"></i><span>' + GB.st + '</span><i class="ri-arrow-down-s-line"></i></button><div class="mk-gb-menu">' +
    Object.keys(GB).map(function (k) { return '<a data-g="' + k + '" class="' + (k === 'st' ? 'on' : '') + '"><i class="ri-check-line"></i>' + GB[k] + '</a>'; }).join('') + '</div></div>' +
    '<div class="mk-gb mk-srt"><button type="button" class="mk-gb-btn mk-srt-btn" title="Sắp xếp trong mỗi nhóm"><i class="ri-arrow-up-down-line"></i><span></span><i class="mk-srt-dir"></i></button><div class="mk-gb-menu mk-srt-menu"></div></div>' +
    '<div class="mk-vt" role="tablist"><button type="button" data-v="list" title="Danh sách"><i class="ri-list-check-2"></i>Danh sách</button><button type="button" data-v="table" title="Bảng"><i class="ri-table-line"></i>Bảng</button></div>';
  tb.insertBefore(ctl, right);
  var gbBtn = ctl.querySelector('.mk-gb:not(.mk-srt) .mk-gb-btn'), gbMenu = ctl.querySelector('.mk-gb:not(.mk-srt) .mk-gb-menu');
  var sBtn = ctl.querySelector('.mk-srt-btn'), sMenu = ctl.querySelector('.mk-srt-menu');
  function paintSort() {
    sBtn.querySelector('span').textContent = sortLabel(); sBtn.querySelector('.mk-srt-dir').className = 'mk-srt-dir ' + (sort.d === 'asc' ? 'ri-arrow-up-line' : 'ri-arrow-down-line');
    sMenu.innerHTML = '<div class="mk-srt-h">Sắp xếp trong mỗi nhóm</div>' + SORTS.map(function (x) { return '<a data-sf="' + x[0] + '" class="' + (x[0] === sort.f ? 'on' : '') + '"><i class="ri-check-line"></i><i class="' + x[2] + ' mk-srt-ic"></i>' + x[1] + '</a>'; }).join('') +
      '<div class="mk-srt-dirs"><button type="button" data-sd="asc" class="' + (sort.d === 'asc' ? 'on' : '') + '"><i class="ri-arrow-up-line"></i>' + (sort.f === 'due' ? 'Sớm trước' : sort.f === 'pri' ? 'Thấp trước' : sort.f === 'upd' ? 'Cũ trước' : sort.f === 'pct' ? 'Ít trước' : 'A → Z') + '</button><button type="button" data-sd="desc" class="' + (sort.d === 'desc' ? 'on' : '') + '"><i class="ri-arrow-down-line"></i>' + (sort.f === 'due' ? 'Muộn trước' : sort.f === 'pri' ? 'Cao trước' : sort.f === 'upd' ? 'Mới trước' : sort.f === 'pct' ? 'Nhiều trước' : 'Z → A') + '</button></div>' +
      '<div class="mk-srt-ft">Mỗi màn nhớ cách sắp riêng · <a data-sreset="1">Về mặc định</a></div>';
  }
  function setSort(f, d) { sort = { f: f, d: d }; try { localStorage.setItem(SK, JSON.stringify(sort)); } catch (e) {} paintSort(); render(); }
  sBtn.addEventListener('click', function (e) { e.stopPropagation(); gbMenu.classList.remove('on'); sMenu.classList.toggle('on'); });
  sMenu.addEventListener('click', function (e) {
    e.stopPropagation(); var a;
    if ((a = e.target.closest('[data-sf]'))) { var f = a.getAttribute('data-sf'), def = SORTS.filter(function (x) { return x[0] === f; })[0][3]; setSort(f, f === sort.f ? sort.d : def); }
    else if ((a = e.target.closest('[data-sd]'))) setSort(sort.f, a.getAttribute('data-sd'));
    else if (e.target.closest('[data-sreset]')) setSort('due', 'asc');
  });
  document.addEventListener('click', function () { sMenu.classList.remove('on'); });
  paintSort();
  gbBtn.addEventListener('click', function (e) { e.stopPropagation(); sMenu.classList.remove('on'); gbMenu.classList.toggle('on'); });
  document.addEventListener('click', function () { gbMenu.classList.remove('on'); });
  gbMenu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { by = a.getAttribute('data-g'); gbMenu.querySelectorAll('a').forEach(function (x) { x.classList.toggle('on', x === a); }); gbBtn.querySelector('span').textContent = GB[by]; render(); }); });
  var cfgBtn = right && [].slice.call(right.querySelectorAll('button')).find(function (b) { return /Cấu hình cột/.test(b.title || ''); });
  if (cfgBtn) cfgBtn.addEventListener('click', function (e) {
    if (view !== 'list') return;
    e.preventDefault(); e.stopPropagation();
    var grp = '', h = '<div class="mk-lpop-h">Hiển thị trên mỗi dòng</div>';
    FIELDS.forEach(function (f) { if (f[2] !== grp) { grp = f[2]; h += '<div class="mk-lpop-sub">' + grp + ' ' + NOUN + '</div>'; } h += '<label class="mk-lpop-ck"><input type="checkbox" data-f="' + f[0] + '"' + (SHOW[f[0]] ? ' checked' : '') + '><span>' + f[1] + '</span></label>'; });
    h += '<div class="mk-lpop-note">Tên, ưu tiên (Cao / Khẩn cấp), người làm, tiến độ, thời hạn luôn hiện. Lưu theo người dùng.</div><a class="mk-lpop-reset" data-reset="1"><i class="ri-arrow-go-back-line"></i>Về mặc định</a>';
    showPop(cfgBtn, h); pop.classList.add('mk-lpop-cfg');
    pop.onclick = function (ev) {
      if (ev.target.closest('[data-reset]')) { FIELDS.forEach(function (f) { SHOW[f[0]] = !!f[3]; }); pop.querySelectorAll('input[data-f]').forEach(function (i) { i.checked = SHOW[i.getAttribute('data-f')]; }); }
      else { var i = ev.target.closest('input[data-f]'); if (!i) return; SHOW[i.getAttribute('data-f')] = i.checked; }
      try { localStorage.setItem('mk-lvf-' + (isIssue ? 'iss' : 'task'), JSON.stringify(SHOW)); } catch (e2) {}
      render();
    };
  }, true);
  var cfgTitle = cfgBtn && cfgBtn.title;
  var LS = 'mk-view-' + key, view = 'list';
  try { view = localStorage.getItem(LS) || 'list'; } catch (e) {}
  function setView(v) {
    view = v; sec.classList.toggle('mk-view-list', v === 'list'); ctl.classList.toggle('mk-view-list', v === 'list');
    ctl.querySelectorAll('.mk-vt button').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-v') === v); });
    if (v === 'list') render();
    if (cfgBtn) cfgBtn.title = v === 'list' ? 'Chọn thông tin hiển thị' : cfgTitle;
    try { localStorage.setItem(LS, v); } catch (e) {}
    window.dispatchEvent(new Event('resize'));
  }
  ctl.querySelectorAll('.mk-vt button').forEach(function (b) { b.addEventListener('click', function () { setView(b.getAttribute('data-v')); }); });
  setView(view);
})();

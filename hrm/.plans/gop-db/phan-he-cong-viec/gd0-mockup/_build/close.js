// 05/11 [U] §3.11 — Đóng / mở lại Dự án nội bộ (màn 06). Menu ⋮ trên dòng → popup Đóng: Kết quả Hoàn thành / Dừng giữa chừng + lý do, liệt kê việc dở sẽ tự huỷ.
(function () {
  var DATA = {
    'Mua sắm đồng phục sơ mi 2027': { t: [['Báo giá may đồng phục 3 nhà cung cấp', 'Đang thực hiện', 'Đỗ Mai Anh'], ['Chốt danh sách size sơ mi toàn công ty', 'Chờ bắt đầu', 'Đỗ Mai Anh'], ['Ký hợp đồng may', 'Nháp', 'Nguyễn Thị Hằng'], ['Tổng hợp ý kiến mẫu áo của các phòng', 'Hoàn thành - Chờ duyệt', 'Bùi Thanh Tâm'], ['Nhận hàng đợt 1', 'Chờ bắt đầu', 'Phạm Quốc Huy'], ['Phát áo cho các phòng', 'Chờ bắt đầu', 'Lê Thu Trang']], i: [['Nhà cung cấp B giao thiếu size XL', 'Đang xử lý', 'Đỗ Mai Anh']] },
    'Tổ chức hội nghị công đoàn 2027': { t: [['Đặt hội trường hội nghị', 'Đang thực hiện', 'Vũ Hoàng Long'], ['Thiết kế backdrop, phông nền hội nghị', 'Đang thực hiện', 'Đỗ Mai Anh'], ['Dự trù kinh phí hội nghị', 'Hoàn thành - Chờ duyệt', 'Lê Thu Trang'], ['Gửi giấy mời đại biểu', 'Chờ bắt đầu', 'Đỗ Mai Anh'], ['Chuẩn bị quà tặng đại biểu', 'Chờ bắt đầu', 'Trần Văn Minh']], i: [['Hội trường tầng 5 trùng lịch ngày 15/01', 'Đang xử lý', 'Trần Văn Minh']] },
    'Kiểm kê tài sản quý III': { t: [], i: [], closed: { r: 'Hoàn thành', why: 'Đã kiểm kê xong 4 tầng, biên bản đã ký.', at: '30/09/2026', by: 'Lê Thu Trang' } }
  };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var md = document.createElement('div'); md.className = 'mk-tdm-wrap'; document.body.appendChild(md);
  var tw = document.createElement('div'); tw.className = 'mk-cl-toast'; document.body.appendChild(tw); var tt;
  function toast(h) { tw.innerHTML = h; tw.classList.add('on'); clearTimeout(tt); tt = setTimeout(function () { tw.classList.remove('on'); }, 3200); }
  function closeModal() { md.classList.remove('on'); md.innerHTML = ''; }
  function modal(h, on) { md.innerHTML = '<div class="mk-tdm-bd"></div><div class="mk-tdm mk-cl" role="dialog">' + h + '</div>'; md.classList.add('on'); md.onclick = function (e) { if (e.target.classList.contains('mk-tdm-bd') || e.target.closest('[data-mx]')) return closeModal(); on(e); }; }
  function head(ic, t, sub, danger) { return '<div class="mk-tdm-h mk-cl-h"><span class="mk-cl-ic' + (danger ? ' d' : '') + '"><i class="' + ic + '"></i></span><div><b>' + t + '</b><small>' + sub + '</small></div><button type="button" class="mk-td-ic" data-mx="1"><i class="ri-close-line"></i></button></div>'; }
  var menu = null;
  function closeMenu() { if (menu) { menu.remove(); menu = null; } }
  document.addEventListener('mousedown', function (e) { if (menu && !menu.contains(e.target)) closeMenu(); });
  function rowName(tr) { var a = tr.querySelector('a.mk-link'); return a ? a.textContent.trim() : ''; }
  function setRow(tr, closed) {
    var b = tr.children[2].querySelector('.mk-badge'), d = DATA[rowName(tr)];
    if (closed) { b.textContent = 'Đã đóng · ' + closed.r; b.style.setProperty('--c', '#6B7280'); b.title = closed.why || ''; tr.children[7].textContent = '0 / ' + (tr.children[7].textContent.split('/')[1] || '').trim(); tr.children[9].textContent = '—'; }
    else { b.textContent = 'Đang thực hiện'; b.style.setProperty('--c', '#2563EB'); b.title = ''; }
    d.closed = closed || null;
  }
  // gắn nhãn kết quả cho dòng đã đóng sẵn
  [].forEach.call(document.querySelectorAll('.data-table tbody tr'), function (tr) { var d = DATA[rowName(tr)]; if (d && d.closed) setRow(tr, d.closed); });
  document.addEventListener('click', function (e) {
    var dot = e.target.closest('.data-table tbody td:last-child'); if (!dot) return;
    var tr = dot.closest('tr'), name = rowName(tr), d = DATA[name]; if (!d) return;
    closeMenu(); menu = document.createElement('div'); menu.className = 'mk-cl-menu';
    var items = d.closed ? [['ri-eye-line', 'Xem dự án', 'view'], ['ri-history-line', 'Lịch sử', 'his'], '-', ['ri-refresh-line', 'Mở lại dự án', 'reopen']]
      : [['ri-eye-line', 'Xem dự án', 'view'], ['ri-edit-line', 'Sửa thông tin', 'edit'], ['ri-history-line', 'Lịch sử', 'his'], '-', ['ri-archive-line', 'Đóng dự án', 'close', 1]];
    menu.innerHTML = items.map(function (x) { return x === '-' ? '<hr>' : '<button type="button" data-v="' + x[2] + '" class="' + (x[3] ? 'dg' : '') + '"><i class="' + x[0] + '"></i>' + x[1] + '</button>'; }).join('') +
      '<small>' + (d.closed ? 'Mở lại: Quản lý dự án hoặc Quản lý phòng' : 'Đóng: Quản lý dự án hoặc Quản lý phòng') + '</small>';
    document.body.appendChild(menu); var r = dot.getBoundingClientRect(); menu.style.top = (r.bottom + 2) + 'px'; menu.style.left = Math.max(8, r.right - menu.offsetWidth) + 'px';
    menu.onclick = function (ev) { var b = ev.target.closest('[data-v]'); if (!b) return; var v = b.dataset.v; closeMenu(); if (v === 'close') openClose(tr, name, d); else if (v === 'reopen') openReopen(tr, name, d); else toast('<i class="ri-information-line"></i> Mockup: mở ' + b.textContent); };
  });
  function openClose(tr, name, d) {
    var nT = d.t.length, nI = d.i.length, waiting = d.t.filter(function (x) { return x[1] === 'Hoàn thành - Chờ duyệt'; }).length;
    var list = d.t.map(function (x) { return '<li><i class="ri-task-line"></i><span>' + esc(x[0]) + '</span><em>' + esc(x[1]) + '</em><small>' + esc(x[2]) + '</small><b>→ Huỷ</b></li>'; }).join('') + d.i.map(function (x) { return '<li><i class="ri-bug-line"></i><span>' + esc(x[0]) + '</span><em>' + esc(x[1]) + '</em><small>' + esc(x[2]) + '</small><b>→ Đã đóng</b></li>'; }).join('');
    modal(head('ri-archive-line', 'Đóng dự án nội bộ', esc(name)) +
      '<div class="mk-tdm-b">' +
        '<div class="mk-tdm-f"><label>Kết quả <span class="text-danger">*</span></label><div class="mk-cl-res">' +
          '<label><input type="radio" name="clr" value="Hoàn thành" checked><span><b><i class="ri-checkbox-circle-line"></i>Hoàn thành</b><small>Đạt mục tiêu, kết thúc dự án.</small></span></label>' +
          '<label><input type="radio" name="clr" value="Dừng giữa chừng"><span><b><i class="ri-stop-circle-line"></i>Dừng giữa chừng</b><small>Không làm tiếp (đổi kế hoạch, huỷ chủ trương…).</small></span></label></div></div>' +
        '<div class="mk-tdm-f"><label data-whyl="1">Lý do</label><textarea class="form-control form-control-sm" rows="3" data-why="1" placeholder="Kết quả đạt được / lý do dừng…"></textarea><div class="mk-td-err" data-err="why"></div></div>' +
        (nT + nI ? '<div class="mk-cl-warn"><div class="h"><i class="ri-error-warning-line"></i><div><b>' + (nT ? nT + ' nhiệm vụ chưa xong sẽ chuyển Huỷ' : '') + (nT && nI ? ' · ' : '') + (nI ? nI + ' vấn đề chưa xong sẽ chuyển Đã đóng' : '') + '</b>' +
          '<small>' + (waiting ? waiting + ' nhiệm vụ đã nộp kết quả (Hoàn thành - Chờ duyệt) cũng bị huỷ. ' : '') + 'Người làm / người phụ trách nhận thông báo. Mở lại dự án sẽ KHÔNG khôi phục các việc này.</small></div>' +
          '<button type="button" class="mk-cl-tog" data-tl="1">Xem danh sách<i class="ri-arrow-down-s-line"></i></button></div><ul class="mk-cl-list" hidden>' + list + '</ul></div>'
          : '<div class="mk-tdm-note"><i class="ri-information-line"></i>Không còn việc dở.</div>') +
        '<div class="mk-tdm-note"><i class="ri-information-line"></i>Sau khi đóng: dự án chỉ đọc với mọi người (không tạo / sửa việc, không nhắn tin), chuyển vào mục Lưu trữ; trao đổi có tin “đã đóng dự án”, mọi thành viên nhận thông báo.</div>' +
      '</div><div class="mk-tdm-ft"><button type="button" class="v2-btn v2-btn--sm v2-btn--danger" data-ok="1"><i class="ri-archive-line"></i> Đóng dự án</button><button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" data-mx="1"><i class="ri-close-line"></i> Huỷ</button></div>',
      function (e) {
        if (e.target.closest('[data-tl]')) { var l = md.querySelector('.mk-cl-list'); l.hidden = !l.hidden; e.target.closest('[data-tl]').classList.toggle('on', !l.hidden); return; }
        if (e.target.name === 'clr') { var stop = e.target.value === 'Dừng giữa chừng'; md.querySelector('[data-whyl]').innerHTML = 'Lý do' + (stop ? ' <span class="text-danger">*</span>' : ''); return; }
        if (!e.target.closest('[data-ok]')) return;
        var res = md.querySelector('[name=clr]:checked').value, why = md.querySelector('[data-why]').value.trim(), ta = md.querySelector('[data-why]'), er = md.querySelector('[data-err=why]');
        var bad = res === 'Dừng giữa chừng' && !why; ta.classList.toggle('is-invalid', bad); er.textContent = bad ? 'Bắt buộc phải nhập' : ''; if (bad) return ta.focus();
        setRow(tr, { r: res, why: why, at: '05/11/2026', by: 'Bạn' }); d.t = []; d.i = []; closeModal();
        toast('<i class="ri-archive-line"></i> Đã đóng dự án · ' + esc(res) + (nT + nI ? ' — huỷ ' + nT + ' nhiệm vụ, đóng ' + nI + ' vấn đề' : '') + '. Mọi thành viên đã nhận thông báo.');
      });
  }
  function openReopen(tr, name, d) {
    modal(head('ri-refresh-line', 'Mở lại dự án?', esc(name)) +
      '<div class="mk-tdm-b"><p class="mk-tdm-p">Dự án đã đóng ngày ' + esc(d.closed.at) + ' · <b>' + esc(d.closed.r) + '</b>' + (d.closed.why ? ' — “' + esc(d.closed.why) + '”' : '') + '.</p>' +
      '<div class="mk-tdm-note"><i class="ri-information-line"></i>Mở lại: dự án về Đang thực hiện, thành viên thao tác và nhắn tin lại được. Các việc đã tự huỷ / tự đóng khi đóng dự án KHÔNG được khôi phục — cần thì tạo lại.</div></div>' +
      '<div class="mk-tdm-ft"><button type="button" class="v2-btn v2-btn--sm v2-btn--primary" data-ok="1"><i class="ri-refresh-line"></i> Mở lại</button><button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" data-mx="1"><i class="ri-close-line"></i> Huỷ</button></div>',
      function (e) { if (!e.target.closest('[data-ok]')) return; setRow(tr, null); closeModal(); toast('<i class="ri-refresh-line"></i> Đã mở lại dự án — mọi thành viên nhận thông báo'); });
  }
})();

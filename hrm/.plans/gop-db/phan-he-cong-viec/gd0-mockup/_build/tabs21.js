// 05/11 [U] §3.12 — Tuỳ chọn tab của không gian (màn 21 Cấu hình). Cố định: Trao đổi + Nhiệm vụ. Tuỳ chọn: Tổng quan · Vấn đề · Meeting · File. Tắt = chỉ ẩn + không tạo mới, dữ liệu vẫn chạy.
(function () {
  var info = document.getElementById('st-info'); if (!info) return;
  var nav = document.querySelector('.mk-st-nav a[data-t="st-info"]');
  if (nav) nav.insertAdjacentHTML('afterend', '<a data-t="st-tabs"><i class="ri-layout-top-2-line"></i>Tab sử dụng</a>');
  var OPT = [['overview', 'ri-dashboard-line', 'Tổng quan', 'Thống kê nhanh việc, vấn đề, họp của phòng.', ''], ['issues', 'ri-bug-line', 'Vấn đề', 'Báo và xử lý vấn đề phát sinh.', '3 vấn đề đang mở'], ['meetings', 'ri-calendar-event-line', 'Meeting', 'Lịch họp và biên bản của phòng.', '2 cuộc họp sắp tới'], ['files', 'ri-folder-3-line', 'File', 'Tài liệu gom từ chat, nhiệm vụ, vấn đề, meeting.', '']];
  var on = { overview: 1, issues: 1, meetings: 1, files: 1 };
  function sw(k) { return '<label class="mk-tb-sw"><input type="checkbox" data-tab="' + k + '"' + (on[k] ? ' checked' : '') + '><span></span></label>'; }
  var html = '<section class="mk-sg" id="st-tabs"><div class="mk-sg-hd"><div class="mk-sg-t">Tab sử dụng</div><div class="mk-sg-d">Chọn các tab phòng dùng. Tắt tab chỉ ẩn đi và không tạo mới loại đó trong phòng; việc đang có vẫn chạy, bật lại là thấy đủ.</div></div>' +
    [['ri-chat-3-line', 'Trao đổi', 'Nhóm chat của phòng · tab mở đầu khi vào không gian.'], ['ri-task-line', 'Nhiệm vụ', 'Giao và theo dõi việc.']].map(function (x) { return '<div class="mk-sr"><div class="mk-sr-l"><div class="mk-sr-t"><i class="' + x[0] + ' mk-tb-ic"></i>' + x[1] + '</div><div class="mk-sr-d">' + x[2] + '</div></div><div class="mk-sr-r"><span class="mk-tb-fix"><i class="ri-lock-line"></i>Luôn bật</span></div></div>'; }).join('') +
    OPT.map(function (x) { return '<div class="mk-sr" data-row="' + x[0] + '"><div class="mk-sr-l"><div class="mk-sr-t"><i class="' + x[1] + ' mk-tb-ic"></i>' + x[2] + '</div><div class="mk-sr-d">' + x[3] + (x[4] ? ' <span class="mk-tb-cnt">' + x[4] + '</span>' : '') + '</div></div><div class="mk-sr-r">' + sw(x[0]) + '<span class="mk-tb-st" data-st="' + x[0] + '">Đang bật</span></div></div>'; }).join('') +
    '<div class="mk-sr"><div class="mk-sr-l"><div class="mk-sr-t">Dự án nội bộ của phòng</div><div class="mk-sr-d">Dự án tạo mới trong phòng được điền sẵn theo cấu hình này; Quản lý dự án đổi riêng được, đổi cấu hình phòng không kéo theo dự án đã có.</div></div><div class="mk-sr-r"><span class="mk-sr-muted">Áp cho dự án tạo sau</span></div></div></section>';
  info.insertAdjacentHTML('afterend', html);
  var md = document.createElement('div'); md.className = 'mk-tdm-wrap'; document.body.appendChild(md);
  var tw = document.createElement('div'); tw.className = 'mk-cl-toast'; document.body.appendChild(tw); var tt;
  function toast(h) { tw.innerHTML = h; tw.classList.add('on'); clearTimeout(tt); tt = setTimeout(function () { tw.classList.remove('on'); }, 3000); }
  function apply(k) { var b = document.querySelector('.tabs-root [data-key="' + k + '"]'); if (b) b.style.display = on[k] ? '' : 'none'; var s = document.querySelector('[data-st="' + k + '"]'); s.textContent = on[k] ? 'Đang bật' : 'Đã tắt'; s.classList.toggle('off', !on[k]); }
  function closeModal() { md.classList.remove('on'); md.innerHTML = ''; }
  document.getElementById('st-tabs').addEventListener('change', function (e) {
    var cb = e.target.closest('[data-tab]'); if (!cb) return; var k = cb.dataset.tab, x = OPT.filter(function (o) { return o[0] === k; })[0];
    if (cb.checked) { on[k] = 1; apply(k); return toast('<i class="ri-eye-line"></i> Đã bật tab ' + x[2] + ' — tin hệ thống báo vào Trao đổi'); }
    cb.checked = true;
    md.innerHTML = '<div class="mk-tdm-bd"></div><div class="mk-tdm mk-cl" role="dialog"><div class="mk-tdm-h mk-cl-h"><span class="mk-cl-ic"><i class="ri-eye-off-line"></i></span><div><b>Tắt tab ' + x[2] + '?</b><small>Phòng Nhân Sự Hành Chính</small></div><button type="button" class="mk-td-ic" data-mx="1"><i class="ri-close-line"></i></button></div>' +
      '<div class="mk-tdm-b"><ul class="mk-tb-list"><li><i class="ri-eye-off-line"></i>Ẩn tab ' + x[2] + ' với mọi thành viên.</li><li><i class="ri-forbid-line"></i>Không tạo mới ' + x[2].toLowerCase() + ' trong phòng này (nút +, # trong chat, tạo từ tin nhắn).</li>' +
      (x[4] ? '<li class="w"><i class="ri-information-line"></i><span><b>' + x[4] + '</b> vẫn chạy bình thường: vẫn hiện ở Việc của tôi, Phê duyệt, thẻ trong chat và thông báo.</span></li>' : '') +
      '<li><i class="ri-refresh-line"></i>Bật lại bất cứ lúc nào, dữ liệu cũ hiện đủ.</li></ul></div>' +
      '<div class="mk-tdm-ft"><button type="button" class="v2-btn v2-btn--sm v2-btn--primary" data-ok="1"><i class="ri-eye-off-line"></i> Tắt tab</button><button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" data-mx="1"><i class="ri-close-line"></i> Huỷ</button></div></div>';
    md.classList.add('on');
    md.onclick = function (ev) { if (ev.target.classList.contains('mk-tdm-bd') || ev.target.closest('[data-mx]')) return closeModal(); if (!ev.target.closest('[data-ok]')) return; on[k] = 0; cb.checked = false; apply(k); closeModal(); toast('<i class="ri-eye-off-line"></i> Đã tắt tab ' + x[2] + ' — tin hệ thống báo vào Trao đổi'); };
  });
})();

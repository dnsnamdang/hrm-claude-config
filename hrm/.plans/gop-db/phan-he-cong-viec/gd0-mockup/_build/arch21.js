// 05/11 [U] §3.11 — Lưu trữ Phòng làm việc (màn 21 Cấu hình). Theo phòng ban: không có nút, tự lưu trữ theo phòng ban. Tự chọn: Quản lý phòng đóng tay, CHẶN khi còn dự án nội bộ con đang chạy.
(function () {
  var sec = document.getElementById('st-arch'); if (!sec) return;
  var KIDS = [['Mua sắm đồng phục sơ mi 2027', 'Nguyễn Thị Hằng', '6 nhiệm vụ đang mở'], ['Tổ chức hội nghị công đoàn 2027', 'Trần Văn Minh', '5 nhiệm vụ đang mở']];
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  sec.innerHTML = '<div class="mk-sg-hd"><div class="mk-sg-t">Lưu trữ</div></div>' +
    '<div class="mk-sr" data-arch="dept"><div class="mk-sr-l"><div class="mk-sr-t">Lưu trữ phòng làm việc</div><div class="mk-sr-d">Phòng theo phòng ban <b>tự lưu trữ</b> khi phòng ban P. NSHC ngừng hoạt động và tự mở lại khi hoạt động lại — không đóng tay. Dự án nội bộ thuộc phòng vẫn chạy bình thường.</div></div><div class="mk-sr-r"><span class="mk-ar-st"><i class="ri-checkbox-circle-line"></i>Đang hoạt động · theo phòng ban</span></div></div>' +
    '<div class="mk-sr mk-ar-demo"><div class="mk-sr-l"><div class="mk-sr-t"><span class="mk-ar-tag">Mockup</span>Ca Phòng tự chọn</div><div class="mk-sr-d">Phòng tự chọn: Quản lý phòng đóng / mở lại bằng tay. Còn dự án nội bộ con đang chạy thì <b>không đóng được</b> — phải đóng từng dự án trước.</div></div><div class="mk-sr-r"><button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary mk-danger" data-arch-go="1"><i class="ri-archive-line" style="margin-right:3px"></i> Đóng phòng làm việc</button></div></div>';
  var md = document.createElement('div'); md.className = 'mk-tdm-wrap'; document.body.appendChild(md);
  var tw = document.createElement('div'); tw.className = 'mk-cl-toast'; document.body.appendChild(tw); var tt;
  function toast(h) { tw.innerHTML = h; tw.classList.add('on'); clearTimeout(tt); tt = setTimeout(function () { tw.classList.remove('on'); }, 3000); }
  function closeModal() { md.classList.remove('on'); md.innerHTML = ''; }
  sec.addEventListener('click', function (e) {
    if (!e.target.closest('[data-arch-go]')) return;
    md.innerHTML = '<div class="mk-tdm-bd"></div><div class="mk-tdm mk-cl" role="dialog"><div class="mk-tdm-h mk-cl-h"><span class="mk-cl-ic d"><i class="ri-forbid-line"></i></span><div><b>Chưa đóng được phòng làm việc</b><small>Hỗ trợ phần mềm · Phòng tự chọn</small></div><button type="button" class="mk-td-ic" data-mx="1"><i class="ri-close-line"></i></button></div>' +
      '<div class="mk-tdm-b"><p class="mk-tdm-p">Phòng còn <b>' + KIDS.length + ' dự án nội bộ đang chạy</b>. Đóng từng dự án (chọn kết quả Hoàn thành / Dừng) rồi quay lại đóng phòng.</p>' +
      '<ul class="mk-ar-list">' + KIDS.map(function (k) { return '<li><i class="ri-folders-line"></i><div><b>' + esc(k[0]) + '</b><small>Quản lý: ' + esc(k[1]) + ' · ' + esc(k[2]) + '</small></div><button type="button" class="mk-ar-go" data-kid="' + esc(k[0]) + '">Đóng dự án<i class="ri-arrow-right-s-line"></i></button></li>'; }).join('') + '</ul>' +
      '<div class="mk-tdm-note"><i class="ri-information-line"></i>Khi không còn dự án con đang chạy, nút này mở popup Đóng như dự án (Kết quả Hoàn thành / Dừng + lý do; nhiệm vụ / vấn đề còn dở của phòng tự chuyển Huỷ / Đã đóng).</div></div>' +
      '<div class="mk-tdm-ft"><button type="button" class="v2-btn v2-btn--sm v2-btn--primary" data-mx="1"><i class="ri-check-line"></i> Đã hiểu</button></div></div>';
    md.classList.add('on');
    md.onclick = function (ev) { if (ev.target.classList.contains('mk-tdm-bd') || ev.target.closest('[data-mx]')) return closeModal(); var g = ev.target.closest('[data-kid]'); if (g) { closeModal(); toast('<i class="ri-external-link-line"></i> Mở Dự án nội bộ “' + esc(g.dataset.kid) + '” → ⋮ Đóng dự án (màn 06)'); } };
  });
})();

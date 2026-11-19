// U21: Panel chi tiết Nhiệm vụ / Vấn đề — phương án thiết kế đề xuất (thay 2 popup CreateTaskModal / ImportResultModal).
// 1 panel cho mọi trạng thái · bấm thẳng vào trường để sửa (chỉ người giao, đúng canEdit) · mục trống gom vào "+ Thêm" (bỏ Đơn giản / Nâng cao)
// · Thiết lập: Lặp lại, Báo cáo tiến độ, Liên kết (05/11: bỏ Trọng số KPI — form thật không có) · Nhật ký tiến độ · đổi hạn / đề nghị gia hạn · quyền bám code thật (khao-sat-nhiem-vu.md).
(function () {
  var L = window.__MKLV; if (!L) return;
  var isI = L.isIssue, N = L.NOUN, esc = L.esc, ME = 'Bạn', NOW = 'Vừa xong';
  var NCap = N.charAt(0).toUpperCase() + N.slice(1);
  function av(n) { return '<i class="mk-lr-av mk-td-av" style="background:' + L.avc(n) + '" title="' + esc(n) + '">' + esc(L.initials(n)) + '</i>'; }
  function ext(f) { var e = (f.split('.').pop() || '').toLowerCase(); return { pdf: ['ri-file-pdf-2-line', '#dc2626'], docx: ['ri-file-word-2-line', '#2563eb'], xlsx: ['ri-file-excel-2-line', '#16a34a'], png: ['ri-image-line', '#7c3aed'], jpg: ['ri-image-line', '#7c3aed'], mp4: ['ri-video-line', '#db2777'] }[e] || ['ri-file-line', '#64748b']; }
  function fileChip(f) { var x = ext(f.n); return '<span class="mk-td-file"><i class="' + x[0] + '" style="color:' + x[1] + '"></i><span>' + esc(f.n) + '</span><small>' + esc(f.s || '') + '</small><i class="ri-download-2-line mk-td-dl" title="Tải xuống"></i></span>'; }
  var NAMES = 'Bạn|Nguyễn Thị Hằng|Trần Văn Minh|Lê Thu Trang|Phạm Quốc Huy|Đỗ Mai Anh|Vũ Hoàng Long';
  function mention(t) { return esc(t).replace(new RegExp('@(' + NAMES + ')', 'g'), '<b class="mk-td-at">@$1</b>').replace(/(ISS-\d{6}-\d{4}|TPE\.(TASK|MET)\.[A-Z]{2}\.\d\d\.\d{4})/g, '<a class="mk-td-ref" href="javascript:void(0)">$1</a>'); }
  var LINKT = { FS: 'Phải xong trước khi việc này bắt đầu', SS: 'Bắt đầu cùng lúc với việc này', FF: 'Kết thúc cùng lúc với việc này', SF: 'Bắt đầu thì việc này mới được kết thúc', RL: 'Liên quan' };
  // ---------- dữ liệu chi tiết mẫu (bám trường thật của tasks / issues) ----------
  var DETAIL = {
    'Báo giá may đồng phục 3 nhà cung cấp': { type: 'Nhiệm vụ cụ thể', hours: 12, time: '17:00', watch: ['Trần Văn Minh'], weight: 3,
      desc: 'Lấy báo giá sơ mi đồng phục từ 3 nhà cung cấp (May 10, Việt Tiến, An Phước) cho 420 nhân sự; so sánh đơn giá, thời gian giao và chính sách đổi size.',
      cl: [['Gửi yêu cầu báo giá', 1], ['Nhận báo giá May 10', 1], ['Nhận báo giá Việt Tiến', 0], ['Lập bảng so sánh 3 nhà cung cấp', 0]],
      sub: [['Liên hệ An Phước xin báo giá', 'Trần Văn Minh', 'Đang thực hiện']],
      files: [{ n: 'Yeu-cau-bao-gia.docx', s: '86 KB' }, { n: 'BG-May10.pdf', s: '1,2 MB' }, { n: 'Mau-so-mi.jpg', s: '640 KB' }],
      report: 'Hằng ngày lúc 17:00', links: [['FS', 'Chốt danh sách size sơ mi toàn công ty', 'Việc này phải xong trước khi “Chốt danh sách size” bắt đầu']],
      logs: [['02/11', 4, 50, 'Nhận báo giá May 10, đang chờ Việt Tiến.'], ['31/10', 3, 30, 'Đã gửi yêu cầu báo giá cho 3 nhà cung cấp.'], ['29/10', 2, 10, 'Soạn yêu cầu báo giá.']],
      cmts: [{ u: 'Nguyễn Thị Hằng', t: '@Bạn nhớ hỏi thêm chính sách đổi size trong 30 ngày nhé.', ago: 'Hôm qua 16:20', re: { '👍': 2 }, rep: [{ u: 'Bạn', t: 'Dạ, em đã ghi vào yêu cầu báo giá rồi ạ.', ago: 'Hôm qua 16:45' }] },
        { u: 'Bạn', t: 'Đã nhận báo giá May 10, em đính kèm ở đây.', f: 'BG-May10.pdf', ago: '2 giờ trước' },
        { u: 'Trần Văn Minh', t: 'Việt Tiến hẹn gửi báo giá trước 06/11.', ago: '1 giờ trước', re: { '👀': 1 } }],
      his: [['ri-line-chart-line', 'Bạn', 'cập nhật tiến độ 30% → 50%', '2 giờ trước'], ['ri-attachment-2', 'Bạn', 'đính kèm BG-May10.pdf', '2 giờ trước'], ['ri-contrast-2-line', 'Bạn', 'chuyển trạng thái Chờ bắt đầu → Đang thực hiện', '28/10 09:05'], ['ri-user-follow-line', 'Nguyễn Thị Hằng', 'giao cho Bạn, người duyệt Nguyễn Thị Hằng', '28/10 08:40'], ['ri-add-circle-line', 'Nguyễn Thị Hằng', 'tạo nhiệm vụ', '28/10 08:40']] },
    'Chốt danh sách size sơ mi toàn công ty': { type: 'Nhiệm vụ cụ thể', hours: 6, time: '17:00', desc: 'Tổng hợp size sơ mi của 420 nhân sự từ form khảo sát, chốt số lượng theo size để gửi nhà cung cấp.',
      cl: [['Gửi form khảo sát size', 0], ['Nhắc các phòng chưa gửi', 0], ['Chốt bảng tổng hợp', 0]], files: [{ n: 'Form-khao-sat-size.xlsx', s: '42 KB' }],
      links: [['FS', 'Báo giá may đồng phục 3 nhà cung cấp', 'Chỉ bắt đầu khi “Báo giá may đồng phục” xong']],
      cmts: [{ u: 'Nguyễn Thị Hằng', t: 'Hạn khảo sát là 10/11, @Bạn nhắc giúp các phòng nhé.', ago: 'Hôm qua 09:10' }] },
    'Đặt hội trường hội nghị': { type: 'Nhiệm vụ cụ thể', hours: 10, time: '12:00', watch: ['Nguyễn Thị Hằng', 'Lê Thu Trang'], meeting: 'TPE.MET.NB.26.0031 · Họp BTC hội nghị công đoàn', weight: 5,
      desc: 'Đặt hội trường 300 chỗ cho Hội nghị công đoàn ngày 15/01/2027, gồm âm thanh, máy chiếu, backdrop và khu đón khách.',
      cl: [['Khảo sát 3 địa điểm', 1], ['Ký hợp đồng thuê hội trường', 0]], files: [{ n: 'Bao-gia-hoi-truong.pdf', s: '820 KB' }, { n: 'So-do-ban-ghe.png', s: '310 KB' }],
      links: [['RL', 'Thiếu phòng họp cho hội nghị ngày 15/01', 'Vấn đề ISS-202611-0007']],
      cmts: [{ u: 'Trần Văn Minh', t: 'Ưu tiên địa điểm gần văn phòng, có chỗ để xe ô tô.', ago: '02/11 10:15', rep: [{ u: 'Bạn', t: 'Dạ, em đang chờ báo giá Trung tâm Hội nghị Quận.', ago: '02/11 10:40' }] },
        { u: 'Lê Thu Trang', t: '@Bạn bên vấn đề ISS-202611-0007 (thiếu phòng họp ngày 15/01) có liên quan, xem giúp nhé.', ago: '02/11 14:00' },
        { u: 'Bạn', t: 'Đã khảo sát xong 3 nơi, bảng so sánh ở file đính kèm.', f: 'Bao-gia-hoi-truong.pdf', ago: 'Hôm qua 17:05', re: { '👍': 3 }, rep: [{ u: 'Trần Văn Minh', t: 'Chọn phương án 2, em làm hợp đồng nhé.', ago: '30 phút trước' }] },
        { u: 'Nguyễn Thị Hằng', t: 'Nhớ xin hoá đơn VAT.', ago: '30 phút trước' }] },
    'Gia hạn hợp đồng vệ sinh toà nhà': { type: 'Nhiệm vụ cụ thể', hours: 4, time: '17:00', desc: 'Gia hạn hợp đồng vệ sinh với Công ty Hoàn Mỹ từ 01/11/2026 đến 31/10/2027, đàm phán giữ nguyên đơn giá.',
      files: [{ n: 'Du-thao-HD-gia-han.docx', s: '120 KB' }], repeat: 'Hằng năm vào 20/10 · không kết thúc',
      cmts: [{ u: 'Lê Thu Trang', t: 'Hợp đồng cũ hết hạn 31/10, cần ký gấp.', ago: '01/11 08:30' }, { u: 'Bạn', t: 'Bên Hoàn Mỹ hẹn gửi bản ký ngày 04/11.', ago: '3 giờ trước' }] },
    'Cập nhật nội quy văn phòng 2027': { type: 'Nhiệm vụ chung', hours: 8, time: '17:00', desc: 'Rà soát và cập nhật nội quy văn phòng áp dụng từ 01/01/2027 theo góp ý của các phòng.',
      cl: [['Tổng hợp góp ý các phòng', 1], ['Soạn bản v3', 1], ['Gửi pháp chế rà soát', 1]], files: [{ n: 'Noi-quy-VP-2027-v3.docx', s: '210 KB' }],
      res: { pct: 100, act: 10, text: 'Đã cập nhật 12 điều khoản theo góp ý các phòng; bổ sung quy định làm việc từ xa, đặt phòng họp và gửi xe.', files: [{ n: 'Noi-quy-VP-2027-v3.docx', s: '210 KB' }], by: 'Phạm Quốc Huy', at: 'Hôm qua 17:30' },
      cmts: [{ u: 'Lê Thu Trang', t: 'Bổ sung thêm phần quy định gửi xe nhé.', ago: '31/10 15:00', rep: [{ u: 'Phạm Quốc Huy', t: 'Đã bổ sung ở mục 7.', ago: '01/11 09:20' }] }, { u: 'Phạm Quốc Huy', t: 'Đã nộp bản v3, @Lê Thu Trang duyệt giúp em.', ago: 'Hôm qua 17:31' }] },
    'Kiểm kê bàn ghế tầng 2': { type: 'Nhiệm vụ cụ thể', hours: 6, time: '17:00', repeat: 'Hằng quý · ngày 28 tháng cuối quý', desc: 'Kiểm kê toàn bộ bàn ghế tầng 2, đối chiếu sổ tài sản, lập biên bản chênh lệch.',
      cl: [['Lập danh sách theo sổ', 1], ['Kiểm đếm thực tế', 1], ['Đối chiếu chênh lệch', 1], ['Lập biên bản', 1], ['Trình ký', 1]],
      res: { pct: 100, act: 7, text: 'Đã kiểm kê 186 bàn ghế; chênh lệch 6 ghế do nhập trùng, đã lập biên bản.', files: [{ n: 'Bien-ban-kiem-ke-T2.pdf', s: '560 KB' }], by: 'Đỗ Mai Anh', at: '27/09 16:00', ok: { by: 'Lê Thu Trang', at: '28/09 09:00', note: 'Đạt.' } } },
    'Máy in tầng 3 kẹt giấy liên tục': { src: 'Thành viên phòng báo', exp: 'In liên tục không kẹt giấy.', act: 'Kẹt giấy sau 5–10 trang ở khay 2, phải tắt máy mới in tiếp.', desc: 'Máy in Canon iR tầng 3 (khu kế toán) kẹt giấy liên tục từ 30/10.', time: '17:00',
      files: [{ n: 'Anh-loi-may-in.jpg', s: '480 KB' }, { n: 'Video-ket-giay.mp4', s: '6,8 MB' }],
      cmts: [{ u: 'Nguyễn Thị Hằng', t: 'Phòng kế toán cần in báo cáo cuối tháng, ưu tiên giúp.', ago: '01/11 08:10' }, { u: 'Vũ Hoàng Long', t: 'Đã đặt mua bộ cuốn giấy thay thế, dự kiến về 04/11.', ago: '1 giờ trước', rep: [{ u: 'Nguyễn Thị Hằng', t: 'OK, cảm ơn em.', ago: '1 giờ trước' }] }] },
    'Sai lệch số liệu kiểm kê bàn ghế tầng 2': { src: 'Phát hiện khi đối chiếu sổ', exp: 'Số liệu kiểm kê khớp sổ tài sản.', act: 'Thực tế ít hơn sổ 6 ghế.', desc: 'Biên bản kiểm kê tầng 2 lệch 6 ghế so với sổ tài sản.', time: '17:00',
      res: { text: 'Đối chiếu lại phiếu nhập: 6 ghế bị nhập trùng ở phiếu PN-0912. Đã điều chỉnh sổ tài sản.', cause: 'Sai nhập liệu', by: 'Lê Thu Trang', at: '29/09 10:00', files: [{ n: 'Doi-chieu-PN-0912.xlsx', s: '35 KB' }] } }
  };
  var POOL = [['Nguyễn Thị Hằng', 'Em cập nhật tiến độ giúp chị nhé.'], ['Trần Văn Minh', 'Đã xem, ổn.'], ['Bạn', 'Em đang xử lý, chiều nay báo lại ạ.'], ['Lê Thu Trang', 'Đính kèm thêm biên bản giúp mình.'], ['Đỗ Mai Anh', 'Mình đã bổ sung số liệu.'], ['Vũ Hoàng Long', 'Đã kiểm tra tại chỗ.']];
  function det(it) {
    if (it.dt) return it.dt;
    var d = JSON.parse(JSON.stringify(DETAIL[it.name] || {}));
    d.desc = d.desc != null ? d.desc : NCap + ': ' + it.name + '.';
    var m = /^(\d+)\/(\d+)$/.exec(it.ck || '');
    if (!d.cl && m) { d.cl = []; for (var i = 0; i < +m[2]; i++) d.cl.push(['Bước ' + (i + 1), i < +m[1] ? 1 : 0]); }
    d.cl = d.cl || []; d.sub = d.sub || []; d.watch = d.watch || []; d.links = d.links || []; d.logs = d.logs || [];
    d.type = d.type || 'Nhiệm vụ cụ thể'; d.time = d.time || '17:00';
    if (!d.files) { d.files = []; for (var j = 0; j < (it.x.file || 0); j++) d.files.push({ n: 'Tai-lieu-' + (j + 1) + '.pdf', s: (120 + j * 90) + ' KB' }); }
    if (!d.cmts) { d.cmts = []; for (var k = 0; k < (it.x.cmt || 0); k++) { var p = POOL[k % POOL.length]; d.cmts.push({ u: p[0], t: p[1], ago: (k + 1) + ' ngày trước' }); } }
    if (!d.his) d.his = [['ri-user-follow-line', it.cr || '—', 'giao cho ' + it.who, (it.x.start || '') + ' 08:30'], ['ri-add-circle-line', it.cr || '—', 'tạo ' + N, (it.x.start || '') + ' 08:30']];
    if (!d.res && L.done(it)) d.res = { pct: 100, act: d.hours || 4, text: 'Đã hoàn thành theo yêu cầu.', by: it.who, at: it.due.slice(0, 5) };
    it.dt = d; return d;
  }
  function cmtCount(d) { return d.cmts.reduce(function (s, c) { return s + (c.sys ? 0 : 1) + (c.rep ? c.rep.length : 0); }, 0); }
  // ---------- vai trò & quyền (bám code thật) ----------
  function role(it) { if (it.as) return it.as; return it.cr === ME ? 'cr' : it.who === ME ? 'who' : it.rv === ME ? 'rv' : 'none'; }
  var ROLES = isI ? [['who', 'Người xử lý'], ['cr', 'Người báo'], ['rv', 'Người duyệt'], ['none', 'Người xem']] : [['who', 'Người làm'], ['cr', 'Người giao'], ['rv', 'Người duyệt'], ['none', 'Người xem']];
  function setRole(it, r) { it.as = r; L.render(); paint(); }
  function canEdit(it) { return role(it) === 'cr'; }                        // Task::canEdit = người tạo
  function canWork(it) { var r = role(it); return r === 'who' || r === 'cr'; } // checklist / tệp / nhiệm vụ con
  // ---------- nhãn hành động ----------
  function actLabel(it, s) {
    if (isI) return { 'Đang xử lý': it.st === 'Đã phân công' || it.st === 'Mới ghi nhận' ? ['Nhận xử lý', 'ri-play-line'] : ['Xử lý lại', 'ri-play-line'], 'Đã xử lý xong': ['Báo đã xử lý', 'ri-check-double-line'], 'Hoàn thành': ['Xác nhận hoàn thành', 'ri-check-line'], 'Từ chối': ['Từ chối kết quả', 'ri-arrow-go-back-line', 1], 'Đã đóng': ['Đóng vấn đề', 'ri-close-circle-line', 1], 'Mở lại': ['Mở lại', 'ri-refresh-line'], 'Đã phân công': ['Phân công', 'ri-user-follow-line'] }[s] || [s, 'ri-exchange-line'];
    return { 'Chờ bắt đầu': it.st === 'Nháp' ? ['Giao việc', 'ri-send-plane-2-line'] : ['Về Chờ bắt đầu', 'ri-skip-back-line'], 'Chờ phê duyệt triển khai': ['Gửi duyệt triển khai', 'ri-shield-user-line'],
      'Đang thực hiện': it.st === 'Chờ bắt đầu' ? ['Bắt đầu', 'ri-play-line'] : it.st === 'Nháp' ? ['Giao & bắt đầu ngay', 'ri-play-line'] : ['Làm tiếp', 'ri-play-line'], 'Tạm dừng': ['Tạm dừng', 'ri-pause-line'], 'Hoàn thành - Chờ duyệt': ['Báo kết quả', 'ri-send-plane-line'],
      'Hoàn thành': it.st === 'Hoàn thành - Chờ duyệt' ? ['Duyệt kết quả', 'ri-check-line'] : ['Hoàn thành', 'ri-check-line'], 'Từ chối kết quả': ['Từ chối kết quả', 'ri-arrow-go-back-line', 1] }[s] || [s, 'ri-exchange-line'];
  }
  // ---------- khung ----------
  var bd = document.createElement('div'); bd.className = 'mk-td-bd';
  var pn = document.createElement('aside'); pn.className = 'mk-td';
  var md = document.createElement('div'); md.className = 'mk-tdm-wrap';
  document.body.appendChild(bd); document.body.appendChild(pn); document.body.appendChild(md);
  var cur = null, tab = 'detail', mode = 'view', draft = null, mn = null, need = {}, advOpen = false;
  function place() { var top = 0; [].slice.call(document.querySelectorAll('.navbar-custom')).forEach(function (n) { if (getComputedStyle(n).display !== 'none') top = Math.max(top, n.getBoundingClientRect().bottom); }); var rail = document.querySelector('.sale-cats'); pn.style.top = bd.style.top = top + 'px'; bd.style.left = (rail ? rail.getBoundingClientRect().width : 0) + 'px'; }
  function show() { place(); document.body.classList.add('mk-td-open'); }
  function close() { document.body.classList.remove('mk-td-open'); cur = null; mode = 'view'; need = {}; closeMenu(); }
  bd.addEventListener('click', function () { if (!md.classList.contains('on')) close(); });
  document.addEventListener('keydown', function (e) { if (e.key !== 'Escape') return; if (md.classList.contains('on')) return closeModal(); if (mn) return closeMenu(); if (document.body.classList.contains('mk-td-open')) close(); });
  function closeMenu() { if (mn) { mn.remove(); mn = null; } }
  function openMenu(anchor, html, onPick, cls) {
    closeMenu(); mn = document.createElement('div'); mn.className = 'mk-lpop on mk-td-menu' + (cls ? ' ' + cls : ''); mn.innerHTML = html; document.body.appendChild(mn);
    var r = anchor.getBoundingClientRect(), w = mn.offsetWidth, h = mn.offsetHeight, top = r.bottom + 4;
    if (top + h > innerHeight - 8) top = Math.max(8, r.top - h - 4);
    mn.style.left = Math.max(8, Math.min(r.left, innerWidth - w - 8)) + 'px'; mn.style.top = top + 'px';
    var me = mn;
    me.addEventListener('click', function (e) {
      if (e.target.closest('[data-x]')) return closeMenu();
      var ok = e.target.closest('[data-ok]'); if (ok) { var v = {}; me.querySelectorAll('[data-f]').forEach(function (x) { v[x.getAttribute('data-f')] = x.type === 'checkbox' ? x.checked : x.value.trim(); }); var r2 = onPick(v, ok.getAttribute('data-ok')); if (r2 !== false && mn === me) closeMenu(); return; }
      var a = e.target.closest('[data-v]'); if (a) { var val = a.getAttribute('data-v'); if (onPick(val) !== false && mn === me) closeMenu(); }
    });
    var f = mn.querySelector('input:not([type=checkbox]), textarea, select'); if (f) setTimeout(function () { f.focus(); }, 20);
    return mn;
  }
  document.addEventListener('mousedown', function (e) { if (mn && !mn.contains(e.target) && !e.target.closest('[data-menu], [data-ed], .mk-lr-due, [data-dueed]')) closeMenu(); });
  // ---------- tiện ích ngày ----------
  function iso(dm) { var m = /(\d\d)\/(\d\d)\/(\d{4})/.exec(dm || ''); return m ? m[3] + '-' + m[2] + '-' + m[1] : ''; }
  function fromIso(v) { var p = v.split('-'); return p[2] + '/' + p[1] + '/' + p[0]; }
  function addDays(n) { var d = new Date(2026, 10, 3 + n); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function setDue(it, v, time) { var p = v.split('-'); it.due = fromIso(v); it.d = new Date(+p[0], p[1] - 1, +p[2]); det(it).time = time || det(it).time; }
  // ---------- vẽ panel ----------
  function paint() {
    if (!cur) return;
    if (mode !== 'view') return paintForm();
    var it = cur, d = det(it), sc = L.SC[it.st] || '#64748b', nx = L.nexts(it), r = role(it), hi = /Cao|Khẩn cấp/.test(it.pri.t);
    var acts = nx.map(function (s) { var a = actLabel(it, s); return '<button type="button" class="mk-td-btn' + (a[2] ? ' danger' : '') + '" data-go="' + esc(s) + '"><i class="' + a[1] + '"></i>' + a[0] + '</button>'; });
    if (acts.length) acts[0] = acts[0].replace('mk-td-btn', 'mk-td-btn primary');
    if (!isI && r === 'who' && it.st === 'Đang thực hiện') acts.splice(1, 0, '<button type="button" class="mk-td-btn" data-upd="1"><i class="ri-line-chart-line"></i>Cập nhật tiến độ</button>');
    var why = !nx.length ? '<span class="mk-td-why"><i class="ri-information-line"></i>' + (it.st === 'Hoàn thành - Chờ duyệt' ? 'Chờ ' + esc(it.rv) + ' duyệt kết quả' : it.st === 'Đã xử lý xong' ? 'Chờ người duyệt xác nhận' : L.done(it) ? NCap + ' đã kết thúc' : 'Bạn chỉ có quyền xem') + '</span>' : '';
    var extB = '';
    if (it.ext) extB = r === 'cr' ? '<div class="mk-td-ext"><i class="ri-hourglass-line"></i><div><b>' + esc(it.ext.by) + ' đề nghị gia hạn</b> ' + esc(it.due) + ' → <b>' + esc(it.ext.to) + ' ' + esc(it.ext.time) + '</b><small>“' + esc(it.ext.reason) + '”</small></div><button type="button" class="mk-td-btn primary" data-extok="1">Đồng ý</button><button type="button" class="mk-td-btn danger" data-extno="1">Từ chối</button></div>'
      : '<div class="mk-td-ext wait"><i class="ri-hourglass-line"></i><div><b>Đã đề nghị gia hạn đến ' + esc(it.ext.to) + '</b><small>Chờ ' + esc(it.cr) + ' đồng ý</small></div></div>';
    var nC = cmtCount(d), nH = (it.his || []).length + d.his.length;
    pn.innerHTML =
      '<div class="mk-td-hd"><div class="mk-td-r1">' +
        '<button type="button" class="mk-td-st" data-menu="st" style="--sc:' + sc + '"' + (nx.length ? '' : ' disabled') + '><i class="' + (L.ICON[it.st] || 'ri-checkbox-blank-circle-line') + '"></i>' + esc(it.st) + (nx.length ? '<i class="ri-arrow-down-s-line"></i>' : '') + '</button>' +
        (it.x.code ? '<span class="mk-lr-code">' + esc(it.x.code) + '</span>' : '') +
        (hi ? '<span class="mk-lr-pri" style="--pc:' + it.pri.c + '"><i class="ri-flag-2-fill"></i>' + esc(it.pri.t) + '</span>' : '') +
        '<span class="mk-td-sp"></span>' +
        '<button type="button" class="mk-td-ic' + (it.follow ? ' on' : '') + '" data-follow="1" data-tip="' + (it.follow ? 'Bỏ theo dõi' : 'Theo dõi') + '"><i class="' + (it.follow ? 'ri-eye-fill' : 'ri-eye-line') + '"></i></button>' +
        '<button type="button" class="mk-td-ic" data-copy="1" data-tip="Sao chép liên kết"><i class="ri-links-line"></i></button>' +
        '<button type="button" class="mk-td-ic" data-menu="more" data-tip="Thao tác khác"><i class="ri-more-2-fill"></i></button>' +
        '<button type="button" class="mk-td-ic" data-close="1" data-tip="Đóng (Esc)"><i class="ri-close-line"></i></button></div>' +
        (canEdit(it) ? '<h3 class="mk-td-title ed" data-ed="name" title="Bấm để sửa tên">' + esc(it.name) + '<i class="ri-pencil-line"></i></h3>' : '<h3 class="mk-td-title">' + esc(it.name) + '</h3>') +
        '<div class="mk-td-crumb"><i class="ri-community-line"></i>' + esc(L.spaceName) + (it.common ? '' : ' <i class="ri-arrow-right-s-line"></i><i class="ri-folders-line"></i>' + esc(it.proj)) + (isI ? '' : '<span class="mk-td-type">' + esc(d.type) + '</span>') + '</div>' +
        '<div class="mk-td-role"><span class="mk-td-demo">Demo</span>Xem với vai trò:<span class="mk-td-seg">' + ROLES.map(function (x) { return '<button type="button" data-role="' + x[0] + '" class="' + (r === x[0] ? 'on' : '') + '">' + x[1] + '</button>'; }).join('') + '</span><span class="mk-td-perm">' + (canEdit(it) ? '<i class="ri-edit-2-line"></i>Bấm vào trường để sửa' : '<i class="ri-lock-line"></i>Chỉ ' + (isI ? 'người báo' : 'người giao') + ' sửa được thông tin') + '</span></div>' +
        extB + '<div class="mk-td-acts">' + acts.join('') + why + '</div></div>' +
      '<nav class="mk-td-tabs">' + [['detail', 'Chi tiết'], ['res', isI ? 'Kết quả xử lý' : 'Kết quả & tiến độ'], ['cmt', 'Bình luận', nC], ['his', 'Lịch sử', nH]].map(function (t) { return '<button type="button" data-tab="' + t[0] + '" class="' + (tab === t[0] ? 'on' : '') + '">' + t[1] + (t[2] ? '<em>' + t[2] + '</em>' : '') + '</button>'; }).join('') + '</nav>' +
      '<div class="mk-td-body">' + (tab === 'detail' ? tDetail(it, d) : tab === 'res' ? tRes(it, d) : tab === 'cmt' ? tCmt(it, d) : tHis(it, d)) + '</div>' +
      (tab === 'cmt' ? composer('root') : '');
  }
  // trường bấm-để-sửa
  function F(it, key, lbl, ic, val, editable) {
    var ed = editable && canEdit(it);
    return '<div class="mk-td-f' + (ed ? ' ed' : '') + (need[key] ? ' need' : '') + '"' + (ed ? ' data-ed="' + key + '" title="Bấm để sửa"' : '') + '><span><i class="' + ic + '"></i>' + lbl + '</span><div>' + val + (ed ? '<i class="ri-pencil-line mk-td-pen"></i>' : '') + '</div>' + (need[key] ? '<small class="mk-td-needm">' + need[key] + '</small>' : '') + '</div>';
  }
  function person(n) { return n && n !== '—' ? '<span class="mk-td-p">' + av(n) + esc(n) + '</span>' : '<span class="mk-td-mut">Không có</span>'; }
  function dueHtml(it, d) {
    if (!it.due) return '<span class="mk-td-mut">Chưa có hạn</span>';
    return '<span class="mk-td-due ' + L.dueCls(it) + '">' + esc(it.due) + ' ' + esc(d.time) + (L.dueSub(it) ? ' · ' + L.dueSub(it) : '') + '</span>';
  }
  function tDetail(it, d) {
    var r = role(it), h = '';
    var dueCell = '<div class="mk-td-f ed' + (need.due ? ' need' : '') + '" data-dueed="1" title="' + (canEdit(it) ? 'Bấm để đổi hạn' : r === 'who' ? 'Bấm để đề nghị gia hạn' : '') + '"><span><i class="ri-calendar-line"></i>' + (isI ? 'Hạn xử lý' : 'Hạn hoàn thành') + '</span><div>' + dueHtml(it, d) + (canEdit(it) || r === 'who' ? '<i class="ri-pencil-line mk-td-pen"></i>' : '') + '</div>' + (need.due ? '<small class="mk-td-needm">' + need.due + '</small>' : '') + '</div>';
    var f = isI ? [F(it, 'who', 'Người xử lý', 'ri-user-star-line', person(it.who), 1), F(it, 'cr', 'Người báo', 'ri-user-add-line', person(it.cr), 0), F(it, 'pri', 'Mức độ ưu tiên', 'ri-flag-2-line', '<span class="mk-td-pri" style="--pc:' + it.pri.c + '">' + esc(it.pri.t) + '</span>', 1), dueCell,
        F(it, 'src', 'Nguồn phát hiện', 'ri-radar-line', esc(d.src || 'Thành viên phòng báo'), 0), F(it, 'tags', 'Thẻ (Tags)', 'ri-price-tag-3-line', (it.x.tags || []).map(function (t) { return '<span class="mk-lr-tag">' + esc(t) + '</span>'; }).join(' ') || '<span class="mk-td-mut">—</span>', 1)]
      : [F(it, 'who', 'Người làm', 'ri-user-star-line', person(it.who), 1), F(it, 'rv', 'Người duyệt kết quả', 'ri-shield-check-line', person(it.rv), 1),
        F(it, 'start', 'Ngày bắt đầu', 'ri-calendar-2-line', esc(it.x.start ? it.x.start + '/2026' : '—'), 1), dueCell,
        F(it, 'hours', 'Số giờ được giao', 'ri-time-line', d.hours ? d.hours + ' giờ' : '<span class="mk-td-mut">—</span>', 1), F(it, 'pri', 'Mức độ ưu tiên', 'ri-flag-2-line', '<span class="mk-td-pri" style="--pc:' + it.pri.c + '">' + esc(it.pri.t) + '</span>', 1),
        F(it, 'watch', 'Người theo dõi', 'ri-eye-line', d.watch.length ? d.watch.map(function (w) { return av(w); }).join('') + '<span class="mk-td-mut">' + d.watch.length + ' người</span>' : '<span class="mk-td-mut">Chưa có</span>', 1),
        F(it, 'tags', 'Thẻ (Tags)', 'ri-price-tag-3-line', (it.x.tags || []).map(function (t) { return '<span class="mk-lr-tag">' + esc(t) + '</span>'; }).join(' ') || '<span class="mk-td-mut">—</span>', 1)];
    h += '<div class="mk-td-grid">' + f.join('') + '</div>';
    // ngữ cảnh
    var ctx = [F(it, 'proj', 'Dự án / Nhóm', 'ri-folders-line', esc(it.common ? 'Việc chung của phòng' : it.proj), 1)];
    if (!isI) ctx.push(F(it, 'type', 'Loại nhiệm vụ', 'ri-list-settings-line', esc(d.type), 1), F(it, 'meeting', 'Meeting', 'ri-calendar-event-line', d.meeting ? '<a class="mk-td-ref" href="javascript:void(0)">' + esc(d.meeting) + '</a>' : '<span class="mk-td-mut">Không gắn</span>', 1));
    h += '<div class="mk-td-ctx">' + ctx.join('') + '</div>';
    // mô tả
    h += sec('Mô tả', 'ri-file-text-line', '<div class="mk-td-descw' + (canEdit(it) ? ' ed' : '') + '"' + (canEdit(it) ? ' data-ed="desc" title="Bấm để sửa"' : '') + '><p class="mk-td-desc">' + (d.desc ? esc(d.desc) : '<span class="mk-td-mut">Chưa có mô tả</span>') + '</p></div>' +
      (isI ? '<div class="mk-td-ea"><div><b>Kết quả mong đợi</b><p>' + esc(d.exp || '—') + '</p></div><div><b>Kết quả thực tế</b><p>' + esc(d.act || '—') + '</p></div></div>' : ''));
    // checklist / nhiệm vụ con / tệp — chỉ hiện khi có, còn lại gom vào "+ Thêm"
    var adds = [];
    if (!isI) {
      if (d.cl.length || d.clOpen) { var dn = d.cl.filter(function (c) { return c[1]; }).length;
        h += sec('Checklist', 'ri-checkbox-multiple-line', (d.cl.length ? '<div class="mk-td-clp"><b style="--p:' + Math.round(dn / d.cl.length * 100) + '%"></b><span>' + dn + '/' + d.cl.length + '</span></div>' : '') +
          d.cl.map(function (c, i) { return '<label class="mk-td-cl' + (c[1] ? ' done' : '') + '"><input type="checkbox" data-cl="' + i + '"' + (c[1] ? ' checked' : '') + (r === 'who' ? '' : ' disabled') + '><span>' + esc(c[0]) + '</span></label>'; }).join('') +
          (canWork(it) ? '<input class="mk-td-in" data-cladd="1" placeholder="Nhập mục checklist và Enter">' : ''), d.cl.length ? dn + '/' + d.cl.length : '');
      } else if (canWork(it)) adds.push(['cl', 'ri-checkbox-multiple-line', 'Checklist']);
      if (d.sub.length) h += sec('Nhiệm vụ con', 'ri-node-tree', d.sub.map(function (s) { return '<div class="mk-td-sub"><i class="' + (L.ICON[s[2]] || 'ri-checkbox-blank-circle-line') + '" style="color:' + (L.SC[s[2]] || '#64748b') + '"></i><span>' + esc(s[0]) + '</span><small>' + esc(s[2]) + '</small>' + av(s[1]) + '</div>'; }).join('') + (canWork(it) ? '<button type="button" class="mk-td-add" data-subadd="1"><i class="ri-add-line"></i>Thêm nhiệm vụ con</button>' : ''), d.sub.length);
      else if (canWork(it)) adds.push(['sub', 'ri-node-tree', 'Nhiệm vụ con']);
    }
    if (d.files.length) h += sec('Tệp đính kèm', 'ri-attachment-2', '<div class="mk-td-files">' + d.files.map(fileChip).join('') + (canWork(it) ? '<button type="button" class="mk-td-add" data-up="1"><i class="ri-upload-2-line"></i>Tải lên</button>' : '') + '</div>', d.files.length);
    else if (canWork(it)) adds.push(['file', 'ri-attachment-2', 'Tệp đính kèm']);
    if (adds.length) h += '<div class="mk-td-adds"><span>Thêm vào ' + N + ':</span>' + adds.map(function (a) { return '<button type="button" class="mk-td-add" data-addsec="' + a[0] + '"><i class="' + a[1] + '"></i>' + a[2] + '</button>'; }).join('') + '</div>';
    // thiết lập (thay tab Thiết lập / Liên kết & KPI của popup cũ)
    if (!isI) {
      var setRows = [['repeat', 'ri-repeat-line', 'Lặp lại', d.repeat || 'Không lặp'], ['report', 'ri-calendar-check-line', 'Yêu cầu báo cáo tiến độ', d.report || 'Không yêu cầu'],
        ['links', 'ri-links-line', 'Liên kết nhiệm vụ', d.links.length ? d.links.length + ' liên kết' : 'Chưa có']];
      var on = setRows.filter(function (x) { return !/^(Không|Chưa|Mặc định)/.test(x[3]); }).length;
      h += '<section class="mk-td-sec mk-td-adv' + (advOpen ? ' open' : '') + '"><h6 data-adv="1"><i class="ri-settings-3-line"></i>Thiết lập<em>' + on + '/3 đang bật</em><i class="ri-arrow-down-s-line mk-td-car"></i></h6><div class="mk-td-advb">' +
        setRows.map(function (x) { return '<div class="mk-td-set' + (canEdit(it) ? ' ed' : '') + '"' + (canEdit(it) ? ' data-ed="' + x[0] + '"' : '') + '><i class="' + x[1] + '"></i><span>' + x[2] + '</span><b class="' + (/^(Không|Chưa|Mặc định)/.test(x[3]) ? 'off' : '') + '">' + esc(x[3]) + '</b>' + (canEdit(it) ? '<i class="ri-pencil-line mk-td-pen"></i>' : '') + '</div>'; }).join('') +
        (d.links.length ? '<div class="mk-td-links">' + d.links.map(function (l) { return '<div class="mk-td-link"><span class="mk-td-lt" title="' + esc(LINKT[l[0]]) + '">' + l[0] + '</span><a class="mk-td-ref" href="javascript:void(0)">' + esc(l[1]) + '</a><small>' + esc(l[2] || LINKT[l[0]]) + '</small></div>'; }).join('') + '</div>' : '') + '</div></section>';
    }
    return h;
  }
  function sec(t, ic, body, c) { return '<section class="mk-td-sec"><h6><i class="' + ic + '"></i>' + t + (c !== '' && c != null ? '<em>' + c + '</em>' : '') + '</h6>' + body + '</section>'; }
  function tRes(it, d) {
    var r = role(it), res = d.res, h = '';
    if (!res) {
      var can = isI ? (r === 'who' && /Đang xử lý|Mở lại|Từ chối/.test(it.st)) : (r === 'who' && /Đang thực hiện|Từ chối kết quả/.test(it.st));
      h += '<div class="mk-td-empty"><i class="ri-inbox-2-line"></i><b>Chưa có kết quả</b><p>' + (can ? 'Khi làm xong, bấm ' + (isI ? '“Báo đã xử lý”' : '“Báo kết quả”') + ' để gửi' + (isI ? '' : ' cho ' + esc(it.rv) + ' duyệt') + '.' : (isI ? 'Người xử lý' : 'Người làm') + ' chưa gửi kết quả.') + '</p>' +
        (can ? '<button type="button" class="mk-td-btn primary" data-go="' + (isI ? 'Đã xử lý xong' : 'Hoàn thành - Chờ duyệt') + '"><i class="ri-send-plane-line"></i>' + (isI ? 'Báo đã xử lý' : 'Nhập kết quả') + '</button>' : '') + '</div>';
    } else {
      var st = res.ok ? ['ok', 'ri-checkbox-circle-fill', 'Đã duyệt bởi ' + res.ok.by + ' · ' + res.ok.at + (res.ok.note ? ' — “' + res.ok.note + '”' : '')] : res.no ? ['no', 'ri-arrow-go-back-line', 'Bị từ chối bởi ' + res.no.by + ' · ' + res.no.at + ' — “' + res.no.note + '”'] : ['wait', 'ri-time-line', isI ? 'Chờ người duyệt xác nhận' : 'Đang chờ ' + it.rv + ' duyệt'];
      h += '<div class="mk-td-rst ' + st[0] + '"><i class="' + st[1] + '"></i>' + esc(st[2]) + '</div>';
      if (isI) h += '<div class="mk-td-grid">' + F(it, 'rby', 'Người báo đã xử lý', 'ri-user-star-line', person(res.by), 0) + F(it, 'rat', 'Thời điểm', 'ri-time-line', esc(res.at), 0) + F(it, 'rcause', 'Nhóm nguyên nhân', 'ri-git-branch-line', esc(res.cause || '—'), 0) + '</div>' + sec('Cách xử lý', 'ri-tools-line', '<p class="mk-td-desc">' + esc(res.text) + '</p>');
      else {
        var eff = res.act ? Math.round((d.hours || res.act) / res.act * 100) : null;
        h += '<div class="mk-td-kpis"><div><small>Tiến độ</small><b>' + res.pct + '%</b></div><div><small>Số giờ được giao</small><b>' + (d.hours || '—') + '</b></div><div><small>Số giờ làm thực tế</small><b>' + res.act + '</b></div><div><small>Hiệu suất</small><b class="' + (eff < 100 ? 'warn' : '') + '" title="Số giờ được giao ÷ số giờ làm thực tế">' + (eff != null ? eff + '%' : '—') + '</b></div></div>';
        h += sec('Kết quả thực hiện', 'ri-list-check-2', '<p class="mk-td-desc">' + esc(res.text) + '</p><div class="mk-td-by">' + av(res.by) + esc(res.by) + ' gửi lúc ' + esc(res.at) + '</div>');
      }
      if (res.files && res.files.length) h += sec('Tệp kết quả', 'ri-attachment-2', '<div class="mk-td-files">' + res.files.map(fileChip).join('') + '</div>');
      if (r === 'rv' && (it.st === 'Hoàn thành - Chờ duyệt' || it.st === 'Đã xử lý xong'))
        h += '<div class="mk-td-appr"><h6><i class="ri-shield-check-line"></i>Duyệt kết quả</h6><textarea class="form-control form-control-sm" rows="2" data-apnote="1" placeholder="Nhận xét (bắt buộc khi từ chối)"></textarea><div class="mk-td-apb"><button type="button" class="mk-td-btn primary" data-approve="1"><i class="ri-check-line"></i>' + (isI ? 'Xác nhận hoàn thành' : 'Duyệt kết quả') + '</button><button type="button" class="mk-td-btn danger" data-reject="1"><i class="ri-arrow-go-back-line"></i>Từ chối kết quả</button></div><div class="mk-td-err" data-aperr="1"></div></div>';
    }
    if (!isI) {
      var logs = d.logs;
      h += sec('Nhật ký tiến độ', 'ri-line-chart-line', (d.report ? '<div class="mk-td-mut mk-td-rpt"><i class="ri-calendar-check-line"></i>Yêu cầu báo cáo: ' + esc(d.report) + '</div>' : '') +
        (logs.length ? '<div class="mk-td-logs">' + logs.map(function (l) { return '<div class="mk-td-log"><span class="d">' + esc(l[0]) + '</span><span class="p"><b style="--p:' + l[2] + '%"></b>' + l[2] + '%</span><span class="h">' + l[1] + ' giờ</span><span class="n">' + esc(l[3]) + '</span></div>'; }).join('') + '</div>' : '<div class="mk-td-mut">Chưa có lần cập nhật tiến độ nào.</div>') +
        (r === 'who' && it.st === 'Đang thực hiện' ? '<button type="button" class="mk-td-add" data-upd="1"><i class="ri-add-line"></i>Cập nhật tiến độ</button>' : ''), logs.length || '');
    }
    return h;
  }
  function cmtHtml(c, path, lvl) {
    var mine = c.u === ME, re = c.re || {};
    if (c.sys) return '<div class="mk-td-sys"><i class="' + c.ic + '"></i><span><b>' + esc(c.u) + '</b> ' + mention(c.t) + '</span><small>' + esc(c.ago) + '</small></div>';
    return '<div class="mk-td-c' + (lvl ? ' rep' : '') + '" data-c="' + path + '">' + av(c.u) + '<div class="mk-td-cb"><div class="mk-td-ch"><b>' + esc(c.u) + '</b><small>' + esc(c.ago) + (c.ed ? ' · đã sửa' : '') + '</small></div>' +
      (c.editing ? '<textarea class="form-control form-control-sm" data-edtxt="' + path + '" rows="2">' + esc(c.t) + '</textarea><div class="mk-td-cact"><a data-edsave="' + path + '">Lưu</a><a data-edcancel="' + path + '">Huỷ</a></div>' : '<div class="mk-td-ct">' + mention(c.t) + '</div>') +
      (c.f ? '<div class="mk-td-files">' + fileChip({ n: c.f, s: '' }) + '</div>' : '') +
      '<div class="mk-td-cact">' + Object.keys(re).filter(function (k) { return re[k]; }).map(function (k) { return '<span class="mk-td-re' + ((c.mine || {})[k] ? ' on' : '') + '" data-re="' + path + '|' + k + '">' + k + ' ' + re[k] + '</span>'; }).join('') +
        '<a data-react="' + path + '" data-menu="re"><i class="ri-emotion-line"></i></a>' + (lvl ? '' : '<a data-reply="' + path + '">Trả lời</a>') + (mine ? '<a data-edit-c="' + path + '">Sửa</a><a class="danger" data-del-c="' + path + '">Xoá</a>' : '') + '</div>' +
      (c.replying ? composer(path) : '') + (c.rep || []).map(function (r, j) { return cmtHtml(r, path + '.' + j, 1); }).join('') + '</div></div>';
  }
  function tCmt(it, d) { return d.cmts.length ? '<div class="mk-td-cmts">' + d.cmts.map(function (c, i) { return cmtHtml(c, String(i), 0); }).join('') + '</div>' : '<div class="mk-td-empty"><i class="ri-chat-3-line"></i><b>Chưa có bình luận</b><p>Gõ @ để nhắc tên người cần trao đổi.</p></div>'; }
  function composer(path) {
    return '<div class="mk-td-comp' + (path === 'root' ? ' root' : '') + '" data-comp="' + path + '">' + (path === 'root' ? av(ME) : '') + '<div class="mk-td-compb"><textarea rows="' + (path === 'root' ? 2 : 1) + '" placeholder="' + (path === 'root' ? 'Viết bình luận… gõ @ để nhắc tên' : 'Trả lời…') + '" data-ctxt="' + path + '"></textarea>' +
      '<div class="mk-td-att" data-att="' + path + '"></div><div class="mk-td-compa"><a data-at="' + path + '" title="Nhắc tên"><i class="ri-at-line"></i></a><a data-attach="' + path + '" title="Đính kèm"><i class="ri-attachment-2"></i></a><span class="mk-td-hint">Ctrl + Enter để gửi</span><button type="button" class="v2-btn v2-btn--sm v2-btn--primary" data-send="' + path + '"><i class="ri-send-plane-2-line"></i> Gửi</button></div></div><div class="mk-td-mention" data-mention="' + path + '"></div></div>';
  }
  function tHis(it, d) {
    var all = (it.his || []).map(function (h) { return [h.ic, h.who, h.t, h.ago]; }).concat(d.his);
    return '<div class="mk-td-tl">' + all.map(function (h) { return '<div class="mk-td-tli"><i class="' + h[0] + '"></i><div><span><b>' + esc(h[1]) + '</b> ' + esc(h[2]) + '</span><small>' + esc(h[3]) + '</small></div></div>'; }).join('') + '</div>';
  }
  function cAt(d, path) { var p = path.split('.').map(Number), c = d.cmts[p[0]]; return p.length > 1 ? c.rep[p[1]] : c; }
  function sys(it, ic, t) { det(it).cmts.push({ sys: 1, ic: ic, u: ME, t: t, ago: NOW }); }
  function done2(it, msg, logIc, logT) { if (logT) L.log(it, logIc, logT); it.x.upd = NOW; L.render(); paint(); if (msg) L.toast(msg); }
  // ---------- trình sửa từng trường ----------
  var PROJ = ['Việc chung của phòng', 'Mua sắm đồng phục sơ mi 2027', 'Tổ chức hội nghị công đoàn 2027', 'Kiểm kê tài sản quý III'];
  var ITYPE = ['Vướng nghiệp vụ', 'Thiếu thông tin đầu vào', 'Yêu cầu thay đổi từ KH', 'Lỗi thiết bị', 'Khác'], ISRC = ['Thành viên phòng báo', 'Kiểm tra tại công trình', 'Khách hàng phản ánh', 'Phát hiện khi đối chiếu'], IDEPT = ['P. Hành chính', 'P. Kỹ thuật', 'P. Kế toán', 'P. Kinh doanh'];
  var PRI = isI ? [['Thấp', '#94a3b8'], ['Trung bình', '#f59e0b'], ['Cao', '#f97316'], ['Khẩn cấp', '#dc2626']] : [['Bình thường', '#94a3b8'], ['Cao', '#f97316'], ['Khẩn cấp', '#dc2626']];
  function people(sel, skip) { return L.PEOPLE.filter(function (p) { return p !== skip; }).map(function (p) { return '<a data-v="' + p + '" class="' + (p === sel ? 'on' : '') + '">' + av(p) + p + (p === sel ? '<i class="ri-check-line mk-td-ck"></i>' : '') + '</a>'; }).join(''); }
  function formPop(title, body, okText) { return '<div class="mk-lpop-h">' + title + '</div><div class="mk-lpop-form">' + body + '<div class="mk-lpop-btns"><button type="button" class="v2-btn v2-btn--sm v2-btn--primary" data-ok="1">' + (okText || 'Lưu') + '</button><button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" data-x="1">Huỷ</button></div></div>'; }
  function editField(it, key, anchor) {
    var d = det(it);
    if (key === 'name') return openMenu(anchor, formPop('Tên ' + N, '<input class="form-control form-control-sm" data-f="v" value="' + esc(it.name) + '">'), function (v) { if (!v.v) return false; var o = it.name; it.name = v.v; done2(it, '<i class="ri-edit-line"></i> Đã đổi tên', 'ri-edit-line', 'đổi tên “' + o + '” → “' + v.v + '”'); });
    if (key === 'who') return openMenu(anchor, '<div class="mk-lpop-h">' + (isI ? 'Người xử lý' : 'Người làm') + '</div>' + people(it.who), function (v) { var o = it.who; it.who = v; delete need.who; done2(it, '<i class="ri-user-shared-line"></i> Đã giao cho ' + esc(v) + (v !== ME ? ' — người mới nhận thông báo' : ''), 'ri-user-shared-line', 'giao lại ' + o + ' → ' + v); });
    if (key === 'rv') return openMenu(anchor, '<div class="mk-lpop-h">Người duyệt kết quả</div><a data-v="—" class="' + (it.rv === '—' ? 'on' : '') + '"><i class="ri-close-circle-line"></i>Không cần duyệt — làm xong là Hoàn thành</a>' + people(it.rv, ME), function (v) { var o = it.rv; it.rv = v; done2(it, '<i class="ri-shield-check-line"></i> Đã đổi người duyệt', 'ri-shield-check-line', 'đổi người duyệt ' + o + ' → ' + v); });
    if (key === 'pri') return openMenu(anchor, '<div class="mk-lpop-h">Mức độ ưu tiên</div>' + PRI.map(function (p) { return '<a data-v="' + p[0] + '"><i class="ri-flag-2-fill" style="color:' + p[1] + '"></i>' + p[0] + (p[0] === it.pri.t ? '<i class="ri-check-line mk-td-ck"></i>' : '') + '</a>'; }).join(''), function (v) { var p = PRI.filter(function (x) { return x[0] === v; })[0]; var o = it.pri.t; it.pri = { t: p[0], c: p[1] }; done2(it, '', 'ri-flag-2-line', 'đổi ưu tiên ' + o + ' → ' + v); });
    if (key === 'start') return openMenu(anchor, formPop('Ngày bắt đầu', '<input type="date" class="form-control form-control-sm" data-f="v" value="' + (it.x.start ? '2026-' + it.x.start.split('/').reverse().join('-') : addDays(0)) + '">'), function (v) { if (!v.v) return false; var p = v.v.split('-'); it.x.start = p[2] + '/' + p[1]; done2(it, '', 'ri-calendar-2-line', 'đổi ngày bắt đầu → ' + it.x.start); });
    if (key === 'hours') return openMenu(anchor, formPop('Số giờ được giao', '<input type="number" step="0.5" min="0.5" class="form-control form-control-sm" data-f="v" value="' + (d.hours || '') + '" placeholder="VD: 8.0">'), function (v) { if (!(+v.v > 0)) return false; d.hours = +v.v; delete need.hours; done2(it, '', 'ri-time-line', 'đổi số giờ được giao → ' + v.v + ' giờ'); });
    if (key === 'tags') return openMenu(anchor, formPop('Thẻ (Tags)', '<input class="form-control form-control-sm" data-f="v" value="' + esc((it.x.tags || []).join(', ')) + '" placeholder="Nhập thẻ, cách nhau bởi dấu phẩy">'), function (v) { it.x.tags = v.v ? v.v.split(',').map(function (s) { return s.trim(); }).filter(Boolean) : []; done2(it, '', 'ri-price-tag-3-line', 'cập nhật thẻ'); });
    if (key === 'watch') return openMenu(anchor, '<div class="mk-lpop-h">Người theo dõi · bấm để thêm / bỏ</div>' + L.PEOPLE.filter(function (p) { return p !== it.who; }).map(function (p) { var on = d.watch.indexOf(p) >= 0; return '<a data-v="' + p + '">' + av(p) + p + (on ? '<i class="ri-check-line mk-td-ck"></i>' : '') + '</a>'; }).join(''), function (v) { var i = d.watch.indexOf(v); if (i >= 0) d.watch.splice(i, 1); else d.watch.push(v); done2(it, '', 'ri-eye-line', (i >= 0 ? 'bỏ ' + v + ' khỏi người theo dõi' : 'thêm ' + v + ' theo dõi')); });
    if (key === 'proj') return openMenu(anchor, '<div class="mk-lpop-h">Dự án / Nhóm</div>' + PROJ.map(function (p) { return '<a data-v="' + p + '"><i class="' + (p === PROJ[0] ? 'ri-community-line' : 'ri-folders-line') + '"></i>' + p + '</a>'; }).join(''), function (v) { it.common = v === PROJ[0]; it.proj = v; done2(it, '', 'ri-folders-line', 'chuyển sang ' + v); });
    if (key === 'type') return openMenu(anchor, '<div class="mk-lpop-h">Loại nhiệm vụ</div><a data-v="Nhiệm vụ chung"><i class="ri-team-line"></i>Nhiệm vụ chung</a><a data-v="Nhiệm vụ cụ thể"><i class="ri-focus-3-line"></i>Nhiệm vụ cụ thể</a>', function (v) { d.type = v; done2(it, '', 'ri-list-settings-line', 'đổi loại → ' + v); });
    if (key === 'meeting') return openMenu(anchor, '<div class="mk-lpop-h">Gắn với meeting</div><a data-v="TPE.MET.NB.26.0031 · Họp BTC hội nghị công đoàn"><i class="ri-calendar-event-line"></i>TPE.MET.NB.26.0031 · Họp BTC hội nghị</a><a data-v="TPE.MET.NB.26.0028 · Giao ban phòng tuần 44"><i class="ri-calendar-event-line"></i>TPE.MET.NB.26.0028 · Giao ban tuần 44</a><a data-v=""><i class="ri-close-circle-line"></i>Không gắn</a>', function (v) { d.meeting = v; done2(it, '', 'ri-calendar-event-line', v ? 'gắn meeting ' + v.split(' · ')[0] : 'bỏ gắn meeting'); });
    if (key === 'desc') return openMenu(anchor, formPop('Mô tả', '<textarea class="form-control form-control-sm" rows="5" data-f="v">' + esc(d.desc || '') + '</textarea>'), function (v) { d.desc = v.v; done2(it, '', 'ri-file-text-line', 'sửa mô tả'); }, 'wide');
    if (key === 'repeat') return openMenu(anchor, formPop('Lặp lại', '<select class="form-control form-control-sm" data-f="t"><option>Không lặp</option><option>Hằng ngày</option><option>Hằng tuần</option><option>Hằng tháng</option><option>Hằng năm</option></select><div class="mk-lpop-row"><span>Mỗi</span><input type="number" min="1" class="form-control form-control-sm" data-f="n" value="1"><span>chu kỳ</span></div><select class="form-control form-control-sm" data-f="e"><option>Không kết thúc</option><option>Kết thúc sau 10 lần</option><option>Kết thúc vào 31/12/2026</option></select><small class="mk-td-mut">Hệ thống tự tạo ' + N + ' mới theo chu kỳ, giữ người làm, người duyệt, checklist.</small>'), function (v) { d.repeat = v.t === 'Không lặp' ? '' : v.t + (+v.n > 1 ? ' (mỗi ' + v.n + ')' : '') + ' · ' + v.e.toLowerCase(); advOpen = true; done2(it, '', 'ri-repeat-line', 'đặt lặp lại: ' + (d.repeat || 'không lặp')); });
    if (key === 'report') return openMenu(anchor, formPop('Yêu cầu báo cáo tiến độ', '<select class="form-control form-control-sm" data-f="t"><option>Không yêu cầu</option><option>Hằng ngày</option><option>Hằng tuần (Thứ 6)</option><option>Hằng tháng (ngày 25)</option></select><div class="mk-lpop-row"><span>Giờ gửi</span><input type="time" class="form-control form-control-sm" data-f="h" value="17:00"></div><small class="mk-td-mut">Đến giờ, người làm nhận nhắc cập nhật tiến độ; mỗi lần cập nhật ghi vào Nhật ký tiến độ.</small>'), function (v) { d.report = v.t === 'Không yêu cầu' ? '' : v.t + ' lúc ' + v.h; advOpen = true; done2(it, '', 'ri-calendar-check-line', 'đặt báo cáo tiến độ: ' + (d.report || 'không')); });
    if (key === 'links') return openMenu(anchor, formPop('Thêm liên kết nhiệm vụ', '<select class="form-control form-control-sm" data-f="t">' + Object.keys(LINKT).map(function (k) { return '<option value="' + k + '">' + k + ' — ' + LINKT[k] + '</option>'; }).join('') + '</select><select class="form-control form-control-sm" data-f="w">' + L.items.filter(function (x) { return x !== it && !x.deleted; }).map(function (x) { return '<option>' + esc(x.name) + '</option>'; }).join('') + '</select>', 'Thêm'), function (v) { d.links.push([v.t, v.w, '']); advOpen = true; done2(it, '', 'ri-links-line', 'liên kết ' + v.t + ' với “' + v.w + '”'); }, 'wide');
  }
  // ---------- hạn: người giao đổi trực tiếp · người làm đề nghị gia hạn ----------
  function bindQuick(m) { m.addEventListener('click', function (e) { var q = e.target.closest('[data-qd]'); if (q) { m.querySelector('[data-f=d]').value = q.getAttribute('data-qd'); m.querySelectorAll('[data-qd]').forEach(function (x) { x.classList.toggle('on', x === q); }); } }); }
  function dueEditor(it, anchor) {
    var d = det(it), r = role(it), cur0 = iso(it.due) || addDays(3);
    var chips = [['Hôm nay', 0], ['Ngày mai', 1], ['Thứ 6 này', 4], ['+1 tuần', 7]].map(function (c) { return '<button type="button" class="mk-td-chip" data-qd="' + addDays(c[1]) + '">' + c[0] + '</button>'; }).join('');
    if (r === 'cr') {
      bindQuick(openMenu(anchor, formPop((isI ? 'Hạn xử lý' : 'Hạn hoàn thành'), '<div class="mk-td-chips">' + chips + '</div><div class="mk-lpop-row"><input type="date" class="form-control form-control-sm" data-f="d" value="' + cur0 + '"><input type="time" class="form-control form-control-sm" data-f="t" value="' + esc(d.time) + '"></div><input class="form-control form-control-sm" data-f="why" placeholder="Lý do đổi hạn (tuỳ chọn, ghi vào lịch sử)">'), function (v) {
        if (!v.d) return false; var o = it.due; setDue(it, v.d, v.t); delete need.due; if (it.ext) delete it.ext;
        sys(it, 'ri-calendar-event-line', 'đổi hạn ' + (o ? o.slice(0, 5) : '—') + ' → ' + it.due.slice(0, 5) + ' ' + v.t + (v.why ? ': “' + v.why + '”' : ''));
        done2(it, '<i class="ri-calendar-check-line"></i> Đã đổi hạn sang ' + it.due + ' ' + v.t + (it.who !== ME ? ' — ' + esc(it.who) + ' nhận thông báo' : ''), 'ri-calendar-event-line', 'đổi hạn → ' + it.due);
      }));
      return;
    }
    if (r === 'who' && !L.settled(it)) {
      if (it.ext) return openMenu(anchor, '<div class="mk-lpop-h">Đề nghị gia hạn</div><div class="mk-lpop-note">Đã gửi đề nghị gia hạn đến <b>' + esc(it.ext.to) + '</b>, đang chờ ' + esc(it.cr) + ' đồng ý.</div><a data-v="cancel" class="danger"><i class="ri-close-line"></i>Rút đề nghị</a>', function () { delete it.ext; sys(it, 'ri-close-line', 'rút đề nghị gia hạn'); done2(it, '<i class="ri-close-line"></i> Đã rút đề nghị gia hạn'); });
      bindQuick(openMenu(anchor, formPop('Đề nghị gia hạn', '<div class="mk-lpop-note">Hạn hiện tại: <b>' + esc(it.due || '—') + ' ' + esc(d.time) + '</b>. Chỉ ' + esc(it.cr) + ' (người giao) đổi được hạn — đề nghị sẽ gửi tới ' + esc(it.cr) + '.</div><div class="mk-td-chips">' + chips + '</div><div class="mk-lpop-row"><input type="date" class="form-control form-control-sm" data-f="d" value="' + addDays(7) + '"><input type="time" class="form-control form-control-sm" data-f="t" value="' + esc(d.time) + '"></div><textarea class="form-control form-control-sm" rows="2" data-f="why" placeholder="Lý do cần thêm thời gian *"></textarea><div class="mk-td-err" data-dueerr="1"></div>', 'Gửi đề nghị'), function (v) {
        if (!v.why) { mn.querySelector('[data-dueerr]').textContent = 'Nhập lý do để người giao cân nhắc.'; mn.querySelector('[data-f=why]').classList.add('is-invalid'); return false; }
        it.ext = { to: fromIso(v.d), time: v.t, reason: v.why, by: ME };
        sys(it, 'ri-hourglass-line', 'đề nghị gia hạn ' + (it.due ? it.due.slice(0, 5) : '—') + ' → ' + it.ext.to.slice(0, 5) + ' gửi @' + it.cr + ': “' + v.why + '”');
        done2(it, '<i class="ri-hourglass-line"></i> Đã gửi đề nghị gia hạn tới ' + esc(it.cr), 'ri-hourglass-line', 'đề nghị gia hạn → ' + it.ext.to);
      }));
      return;
    }
    openMenu(anchor, '<div class="mk-lpop-h">' + (isI ? 'Hạn xử lý' : 'Hạn hoàn thành') + '</div><div class="mk-lpop-note"><b>' + esc(it.due || 'Chưa có hạn') + ' ' + esc(d.time) + '</b><br>' + (L.settled(it) ? NCap + ' đã nộp kết quả / kết thúc.' : 'Chỉ ' + esc(it.cr) + ' (người giao) đổi được hạn; người làm có thể đề nghị gia hạn.') + '</div>', function () {});
  }
  // ---------- sự kiện ----------
  pn.addEventListener('click', function (e) {
    var t = e.target, it = cur; if (!it || mode !== 'view') return; var d = det(it), a;
    if (t.closest('[data-close]')) return close();
    if ((a = t.closest('[data-tab]'))) { tab = a.getAttribute('data-tab'); return paint(); }
    if ((a = t.closest('[data-role]'))) return setRole(it, a.getAttribute('data-role'));
    if ((a = t.closest('[data-go]'))) return go(it, a.getAttribute('data-go'));
    if (t.closest('[data-upd]')) return MKTD.result(it, 'Đang thực hiện');
    if (t.closest('[data-dueed]')) return dueEditor(it, t.closest('[data-dueed]'));
    if ((a = t.closest('[data-ed]'))) return editField(it, a.getAttribute('data-ed'), a);
    if (t.closest('[data-adv]')) { advOpen = !advOpen; return paint(); }
    if ((a = t.closest('[data-addsec]'))) { var k = a.getAttribute('data-addsec'); if (k === 'cl') { d.clOpen = 1; paint(); var n = pn.querySelector('[data-cladd]'); if (n) n.focus(); return; } if (k === 'sub') { d.sub.push(['Nhiệm vụ con mới', it.who, 'Chờ bắt đầu']); return done2(it, '<i class="ri-node-tree"></i> Đã thêm nhiệm vụ con', 'ri-node-tree', 'thêm nhiệm vụ con'); } if (k === 'file') { d.files.push({ n: 'Tai-lieu-moi.pdf', s: '240 KB' }); it.x.file = d.files.length; return done2(it, '<i class="ri-upload-2-line"></i> Đã tải lên Tai-lieu-moi.pdf (mô phỏng)', 'ri-attachment-2', 'đính kèm Tai-lieu-moi.pdf'); } }
    if (t.closest('[data-extok]')) { var x = it.ext; setDue(it, iso(x.to), x.time); delete it.ext; sys(it, 'ri-calendar-check-line', 'đồng ý gia hạn đến ' + x.to + ' ' + x.time); return done2(it, '<i class="ri-calendar-check-line"></i> Đã đồng ý gia hạn — ' + esc(x.by) + ' nhận thông báo', 'ri-calendar-check-line', 'đồng ý gia hạn → ' + x.to); }
    if (t.closest('[data-extno]')) { delete it.ext; sys(it, 'ri-close-circle-line', 'không đồng ý gia hạn, giữ hạn ' + it.due); return done2(it, '<i class="ri-close-circle-line"></i> Đã từ chối đề nghị gia hạn', 'ri-close-circle-line', 'từ chối đề nghị gia hạn'); }
    if (t.closest('[data-follow]')) { L.menu(it, it.follow ? 'Bỏ theo dõi' : 'Theo dõi'); return paint(); }
    if (t.closest('[data-copy]')) return L.menu(it, 'Sao chép liên kết');
    if ((a = t.closest('[data-menu=st]'))) return openMenu(a, '<div class="mk-lpop-h">Chuyển trạng thái</div>' + L.nexts(it).map(function (s) { return '<a data-v="' + esc(s) + '"><i class="' + L.ICON[s] + '" style="color:' + L.SC[s] + '"></i>' + esc(s) + '</a>'; }).join(''), function (v) { go(it, v); });
    if ((a = t.closest('[data-menu=more]'))) {
      var me = role(it), M = [canEdit(it) ? ['Sửa toàn bộ', 'ri-edit-box-line'] : null, me === 'who' && !L.settled(it) ? ['Đề nghị gia hạn', 'ri-hourglass-line'] : null, ['Lịch sử thay đổi', 'ri-history-line'], canEdit(it) && it.st === 'Nháp' ? ['Xoá', 'ri-delete-bin-line', 'danger'] : null].filter(Boolean);
      var hint = canEdit(it) && it.st !== 'Nháp' ? '<div class="mk-lpop-note">Chỉ xoá được ' + N + ' ở trạng thái Nháp.</div>' : '';
      var btn = a;
      return openMenu(a, M.map(function (m) { return '<a class="' + (m[2] || '') + '" data-v="' + m[0] + '"><i class="' + m[1] + '"></i>' + m[0] + '</a>'; }).join('') + hint, function (v) { if (v === 'Lịch sử thay đổi') { tab = 'his'; return paint(); } if (v === 'Đề nghị gia hạn') { closeMenu(); return dueEditor(it, btn); } L.menu(it, v, btn); });
    }
    if ((a = t.closest('[data-cl]')) && t.tagName === 'INPUT') { d.cl[+a.getAttribute('data-cl')][1] = a.checked ? 1 : 0; syncCk(it); return done2(it, '', 'ri-checkbox-line', (a.checked ? 'hoàn thành' : 'bỏ hoàn thành') + ' mục checklist “' + d.cl[+a.getAttribute('data-cl')][0] + '”'); }
    if (t.closest('[data-subadd]')) { d.sub.push(['Nhiệm vụ con mới', it.who, 'Chờ bắt đầu']); return done2(it, '<i class="ri-node-tree"></i> Đã thêm nhiệm vụ con', 'ri-node-tree', 'thêm nhiệm vụ con'); }
    if (t.closest('[data-up]')) { d.files.push({ n: 'Tai-lieu-moi.pdf', s: '240 KB' }); it.x.file = d.files.length; return done2(it, '<i class="ri-upload-2-line"></i> Đã tải lên Tai-lieu-moi.pdf (mô phỏng)', 'ri-attachment-2', 'đính kèm Tai-lieu-moi.pdf'); }
    if (t.closest('[data-approve]')) { var note = (pn.querySelector('[data-apnote]') || {}).value || ''; d.res.ok = { by: ME, at: NOW, note: note }; delete d.res.no; L.setSt(it, 'Hoàn thành'); sys(it, 'ri-checkbox-circle-line', 'đã duyệt kết quả' + (note ? ': “' + note + '”' : '')); tab = 'res'; return paint(); }
    if (t.closest('[data-reject]')) { var nt = (pn.querySelector('[data-apnote]') || {}).value || ''; if (!nt.trim()) { pn.querySelector('[data-aperr]').textContent = 'Nhập nhận xét để người làm biết cần sửa gì.'; pn.querySelector('[data-apnote]').classList.add('is-invalid'); return; } d.res.no = { by: ME, at: NOW, note: nt }; L.setSt(it, isI ? 'Từ chối' : 'Từ chối kết quả'); sys(it, 'ri-arrow-go-back-line', 'đã từ chối kết quả: “' + nt + '”'); tab = 'res'; return paint(); }
    if ((a = t.closest('[data-reply]'))) { var c = cAt(d, a.getAttribute('data-reply')); c.replying = !c.replying; paint(); var ta = pn.querySelector('[data-ctxt="' + a.getAttribute('data-reply') + '"]'); if (ta) { ta.value = '@' + c.u + ' '; ta.focus(); } return; }
    if ((a = t.closest('[data-edit-c]'))) { cAt(d, a.getAttribute('data-edit-c')).editing = 1; return paint(); }
    if ((a = t.closest('[data-edcancel]'))) { cAt(d, a.getAttribute('data-edcancel')).editing = 0; return paint(); }
    if ((a = t.closest('[data-edsave]'))) { var p = a.getAttribute('data-edsave'), cc = cAt(d, p); cc.t = pn.querySelector('[data-edtxt="' + p + '"]').value; cc.editing = 0; cc.ed = 1; return paint(); }
    if ((a = t.closest('[data-del-c]'))) { var pp = a.getAttribute('data-del-c').split('.').map(Number); if (pp.length > 1) d.cmts[pp[0]].rep.splice(pp[1], 1); else d.cmts.splice(pp[0], 1); it.x.cmt = cmtCount(d); return done2(it, '<i class="ri-delete-bin-line"></i> Đã xoá bình luận'); }
    if ((a = t.closest('[data-re]'))) { var q = a.getAttribute('data-re').split('|'), c2 = cAt(d, q[0]); c2.mine = c2.mine || {}; c2.mine[q[1]] = !c2.mine[q[1]]; c2.re[q[1]] += c2.mine[q[1]] ? 1 : -1; return paint(); }
    if ((a = t.closest('[data-react]'))) return openMenu(a, '<div class="mk-td-emo">' + ['👍', '❤️', '😄', '🎉', '👀', '🙏'].map(function (x) { return '<a data-v="' + x + '">' + x + '</a>'; }).join('') + '</div>', function (v) { var c3 = cAt(d, a.getAttribute('data-react')); c3.re = c3.re || {}; c3.mine = c3.mine || {}; if (!c3.mine[v]) { c3.mine[v] = 1; c3.re[v] = (c3.re[v] || 0) + 1; } paint(); });
    if ((a = t.closest('[data-at]'))) { var ta2 = pn.querySelector('[data-ctxt="' + a.getAttribute('data-at') + '"]'); ta2.value += (ta2.value && !/\s$/.test(ta2.value) ? ' ' : '') + '@'; ta2.focus(); return mentionBox(ta2); }
    if ((a = t.closest('[data-attach]'))) { var box = pn.querySelector('[data-att="' + a.getAttribute('data-attach') + '"]'); box.setAttribute('data-f', 'Anh-chup-man-hinh.png'); box.innerHTML = fileChip({ n: 'Anh-chup-man-hinh.png', s: '180 KB' }); return; }
    if ((a = t.closest('[data-mention] a'))) { var host = a.closest('[data-mention]'), ta3 = pn.querySelector('[data-ctxt="' + host.getAttribute('data-mention') + '"]'); ta3.value = ta3.value.replace(/@[^@\s]*$/, '@' + a.getAttribute('data-p') + ' '); host.innerHTML = ''; ta3.focus(); return; }
    if ((a = t.closest('[data-send]'))) return send(a.getAttribute('data-send'));
    if (t.closest('.mk-td-ref')) return L.toast('<i class="ri-links-line"></i> Mở ' + esc(t.textContent) + ' (mô phỏng)');
    if (t.closest('.mk-td-dl')) return L.toast('<i class="ri-download-2-line"></i> Tải xuống (mô phỏng)');
  });
  // Nháp → giao việc: kiểm đủ trường bắt buộc trước (giống validate form tạo hiện tại)
  function go(it, s) {
    if (!isI && it.st === 'Nháp') {
      var d = det(it); need = {};
      if (!it.due) need.due = 'Cần đặt hạn trước khi giao';
      if (!d.hours) need.hours = 'Cần số giờ được giao';
      if (!it.who || it.who === '—') need.who = 'Chọn người làm';
      if (Object.keys(need).length) { var keep = need; if (cur !== it) MKTD.open(it, 'detail'); need = keep; tab = 'detail'; mode = 'view'; show(); paint(); L.toast('<i class="ri-error-warning-line"></i> Bổ sung ' + Object.keys(need).length + ' thông tin bắt buộc trước khi giao việc'); return; }
    }
    L.go(it, s);
  }
  pn.addEventListener('keydown', function (e) {
    var t = e.target; if (mode !== 'view') return;
    if (t.matches('[data-cladd]') && e.key === 'Enter' && t.value.trim()) { var v = t.value.trim(); det(cur).cl.push([v, 0]); syncCk(cur); done2(cur, '', 'ri-checkbox-line', 'thêm mục checklist “' + v + '”'); var n = pn.querySelector('[data-cladd]'); if (n) n.focus(); }
    if (t.matches('[data-ctxt]') && e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); send(t.getAttribute('data-ctxt')); }
  });
  pn.addEventListener('input', function (e) { if (e.target.matches('[data-ctxt]')) mentionBox(e.target); });
  function mentionBox(ta) {
    var m = /@([^@\s]*)$/.exec(ta.value), host = pn.querySelector('[data-mention="' + ta.getAttribute('data-ctxt') + '"]'); if (!host) return;
    if (!m) { host.innerHTML = ''; return; }
    var q = m[1].toLowerCase(), list = L.PEOPLE.filter(function (p) { return p !== ME && p.toLowerCase().indexOf(q) >= 0; });
    host.innerHTML = list.length ? '<div class="mk-td-mlist">' + list.map(function (p) { return '<a data-p="' + p + '">' + av(p) + p + '</a>'; }).join('') + '</div>' : '';
  }
  function send(path) {
    var it = cur, d = det(it), ta = pn.querySelector('[data-ctxt="' + path + '"]'), att = pn.querySelector('[data-att="' + path + '"]'); var v = (ta.value || '').trim(), f = att && att.getAttribute('data-f');
    if (!v && !f) { ta.classList.add('is-invalid'); ta.focus(); return; }
    var c = { u: ME, t: v, ago: NOW, f: f || '' };
    if (path === 'root') d.cmts.push(c); else { var p = cAt(d, path); (p.rep = p.rep || []).push(c); p.replying = 0; }
    it.x.cmt = cmtCount(d); var tags = (v.match(new RegExp('@(' + NAMES.replace('Bạn|', '') + ')', 'g')) || []);
    done2(it, '<i class="ri-chat-check-line"></i> Đã gửi bình luận' + (tags.length ? ' · thông báo tới ' + esc(tags.join(', ').replace(/@/g, '')) : ''), 'ri-chat-3-line', path === 'root' ? 'bình luận' : 'trả lời bình luận');
    var list = pn.querySelector('.mk-td-body'); if (list) list.scrollTop = list.scrollHeight;
  }
  function syncCk(it) { var d = det(it), dn = d.cl.filter(function (c) { return c[1]; }).length; it.ck = d.cl.length ? dn + '/' + d.cl.length : '—'; }
  // ---------- hộp thoại ----------
  function modal(html, onClick) { md.innerHTML = '<div class="mk-tdm-bd"></div><div class="mk-tdm" role="dialog">' + html + '</div>'; md.classList.add('on'); md.onclick = function (e) { if (e.target.classList.contains('mk-tdm-bd') || e.target.closest('[data-mx]')) return closeModal(); onClick(e); }; var f = md.querySelector('textarea, input:not([disabled])'); if (f) setTimeout(function () { f.focus(); }, 30); }
  function closeModal() { md.classList.remove('on'); md.innerHTML = ''; }
  function mhead(t, sub) { return '<div class="mk-tdm-h"><div><b>' + t + '</b>' + (sub ? '<small>' + sub + '</small>' : '') + '</div><button type="button" class="mk-td-ic" data-mx="1"><i class="ri-close-line"></i></button></div>'; }
  function fld(lbl, inner, req, errKey, cols) { return '<div class="mk-tdm-f' + (cols ? ' c' + cols : '') + '"><label>' + lbl + (req ? ' <span class="text-danger">*</span>' : '') + '</label>' + inner + (errKey ? '<div class="mk-td-err" data-err="' + errKey + '"></div>' : '') + '</div>'; }
  function showErr(errs, root) { root = root || md; root.querySelectorAll('[data-err]').forEach(function (e) { var k = e.getAttribute('data-err'); e.textContent = errs[k] || ''; var inp = e.parentElement.querySelector('input, textarea, select'); if (inp) inp.classList.toggle('is-invalid', !!errs[k]); }); var first = root.querySelector('.is-invalid'); if (first) first.focus(); return !Object.keys(errs).length; }
  var MKTD = window.MKTD = {
    open: function (it, t) { cur = it; tab = t || 'detail'; mode = 'view'; need = {}; det(it); show(); paint(); },
    refresh: function () { if (cur && document.body.classList.contains('mk-td-open')) paint(); },
    due: function (it, anchor) { dueEditor(it, anchor); },
    go: function (it, s) { go(it, s); },
    quick: function (name) {
      var nextNo = 151 + L.items.filter(function (x) { return x.isNew; }).length;
      var it = { tr: document.createElement('tr'), isNew: 1, a: null, name: name, x: { code: isI ? 'ISS-202611-00' + (nextNo - 140) : 'TPE.TASK.NB.26.0' + nextNo, cmt: 0, file: 0, upd: NOW }, st: isI ? 'Mới ghi nhận' : 'Nháp', cr: ME, who: ME, rv: isI ? '' : '—', due: '', d: null, ck: '—', common: true, proj: 'Việc chung của phòng', pri: { t: PRI[0][0], c: PRI[0][1] } };
      if (!isI) it.x.pct = 0;
      it.dt = { desc: '', cl: [], sub: [], watch: [], files: [], cmts: [], links: [], logs: [], type: 'Nhiệm vụ cụ thể', time: '17:00', his: [['ri-add-circle-line', ME, 'tạo nhanh ' + N + (isI ? '' : ' (Nháp)'), NOW]] };
      L.items.push(it); L.render(); L.toast('<i class="ri-draft-line"></i> Đã tạo ' + (isI ? N : 'nháp') + ' — bổ sung hạn, ' + (isI ? 'người xử lý' : 'số giờ rồi bấm Giao việc'));
      MKTD.open(it, 'detail');
    },
    result: function (it, target) {
      var d = det(it), done = target !== 'Đang thực hiện';
      if (isI) {
        modal(mhead('Báo đã xử lý vấn đề', esc(it.name)) + '<div class="mk-tdm-b">' + fld('Cách xử lý', '<textarea class="form-control form-control-sm" rows="3" data-k="text" placeholder="Mô tả cách đã xử lý…"></textarea>', 1, 'text') +
          fld('Nhóm nguyên nhân', '<select class="form-control form-control-sm" data-k="cause"><option value="">— Chọn —</option><option>Thiết bị hỏng</option><option>Sai nhập liệu</option><option>Quy trình</option><option>Nhà cung cấp</option><option>Khác</option></select>', 1, 'cause') +
          fld('Tệp đính kèm', '<div class="mk-td-files" data-rf="1"><button type="button" class="mk-td-add" data-rup="1"><i class="ri-upload-2-line"></i>Tải lên</button></div>') +
          '<div class="mk-tdm-note"><i class="ri-information-line"></i>Gửi xong, vấn đề chuyển sang <b>Đã xử lý xong</b> và chờ người duyệt xác nhận.</div></div>' +
          '<div class="mk-tdm-ft"><button type="button" class="v2-btn v2-btn--sm v2-btn--primary" data-ok="1"><i class="ri-send-plane-line"></i> Gửi kết quả</button><button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" data-mx="1">Huỷ</button></div>',
          function (e) {
            if (e.target.closest('[data-rup]')) { md.querySelector('[data-rf]').insertAdjacentHTML('afterbegin', fileChip({ n: 'Anh-sau-xu-ly.jpg', s: '350 KB' })); return; }
            if (!e.target.closest('[data-ok]')) return;
            var v = {}; md.querySelectorAll('[data-k]').forEach(function (x) { v[x.getAttribute('data-k')] = x.value.trim(); });
            var er = {}; if (!v.text) er.text = 'Nhập cách xử lý.'; if (!v.cause) er.cause = 'Chọn nhóm nguyên nhân.'; if (!showErr(er)) return;
            d.res = { text: v.text, cause: v.cause, by: ME, at: NOW, files: md.querySelectorAll('[data-rf] .mk-td-file').length ? [{ n: 'Anh-sau-xu-ly.jpg', s: '350 KB' }] : [] };
            closeModal(); L.setSt(it, target); sys(it, 'ri-check-double-line', 'đã báo xử lý xong'); cur = it; tab = 'res'; show(); paint();
          });
        return;
      }
      var cl = d.cl.map(function (c, i) { return '<label class="mk-td-cl' + (c[1] ? ' done' : '') + '"><input type="checkbox" data-rcl="' + i + '"' + (c[1] ? ' checked' : '') + '><span>' + esc(c[0]) + '</span></label>'; }).join('');
      modal(mhead(done ? 'Nhập kết quả nhiệm vụ' : 'Cập nhật tiến độ', esc(it.name)) + '<div class="mk-tdm-b"><div class="mk-tdm-row">' +
        fld('<i class="ri-time-line"></i> Số giờ được giao', '<input class="form-control form-control-sm" disabled value="' + (d.hours || '—') + '">', 0, null, 3) +
        fld(done ? 'Số giờ làm thực tế' : 'Số giờ làm lần này', '<input class="form-control form-control-sm" type="number" step="0.5" data-k="act" placeholder="VD: 6.5">', 1, 'act', 3) +
        fld('Tiến độ (%)', '<input class="form-control form-control-sm" type="number" min="0" max="100" data-k="pct" value="' + (done ? 100 : (it.x.pct || 0)) + '"' + (done ? ' disabled' : '') + '>', 1, 'pct', 3) +
        (done ? fld('Hiệu suất', '<input class="form-control form-control-sm" disabled data-eff="1" value="—">', 0, null, 3) : fld('Ngày báo cáo', '<input class="form-control form-control-sm" disabled value="03/11/2026">', 0, null, 3)) + '</div>' +
        fld(done ? 'Kết quả thực hiện' : 'Nội dung đã làm', '<textarea class="form-control form-control-sm" rows="3" data-k="text" placeholder="' + (done ? 'Nhập kết quả thực hiện…' : 'Hôm nay đã làm được gì…') + '"></textarea>', 1, 'text') +
        (cl ? fld('Checklist', '<div class="mk-tdm-cl">' + cl + '</div>', 0, 'cl') : '') +
        fld('Tệp đính kèm', '<div class="mk-td-files" data-rf="1"><button type="button" class="mk-td-add" data-rup="1"><i class="ri-upload-2-line"></i>Tải lên</button></div>') +
        '<div class="mk-tdm-note"><i class="ri-information-line"></i>' + (done ? (it.rv && it.rv !== '—' ? 'Gửi xong, nhiệm vụ chuyển sang <b>Hoàn thành - Chờ duyệt</b> và báo cho <b>' + esc(it.rv) + '</b> duyệt.' : 'Nhiệm vụ không có người duyệt nên chuyển thẳng sang <b>Hoàn thành</b>.') : 'Ghi 1 dòng vào <b>Nhật ký tiến độ</b>, nhiệm vụ vẫn ở <b>Đang thực hiện</b>.') + '</div></div>' +
        '<div class="mk-tdm-ft"><button type="button" class="v2-btn v2-btn--sm v2-btn--primary" data-ok="1"><i class="ri-send-plane-line"></i> ' + (done ? 'Gửi kết quả' : 'Lưu tiến độ') + '</button><button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" data-mx="1">Huỷ</button></div>',
        function (e) {
          if (e.target.closest('[data-rup]')) { md.querySelector('[data-rf]').insertAdjacentHTML('afterbegin', fileChip({ n: 'Ket-qua-' + (it.x.code || 'NV').slice(-4) + '.pdf', s: '420 KB' })); return; }
          if (!e.target.closest('[data-ok]')) return;
          var v = {}; md.querySelectorAll('[data-k]').forEach(function (x) { v[x.getAttribute('data-k')] = x.value.trim(); });
          var er = {}; if (!v.act || +v.act <= 0) er.act = 'Nhập số giờ (> 0).'; if (v.pct === '' || +v.pct < 0 || +v.pct > 100) er.pct = 'Tiến độ từ 0 đến 100.'; if (!v.text) er.text = done ? 'Nhập kết quả thực hiện.' : 'Nhập nội dung đã làm.';
          if (done && md.querySelectorAll('[data-rcl]').length && md.querySelectorAll('[data-rcl]:not(:checked)').length) er.cl = 'Còn mục checklist chưa xong — tick đủ trước khi báo hoàn thành.';
          if (!showErr(er)) return;
          md.querySelectorAll('[data-rcl]').forEach(function (x) { d.cl[+x.getAttribute('data-rcl')][1] = x.checked ? 1 : 0; }); syncCk(it);
          it.x.pct = +v.pct; it.x.upd = NOW;
          var files = [].slice.call(md.querySelectorAll('[data-rf] .mk-td-file > span')).map(function (s) { return { n: s.textContent, s: '420 KB' }; });
          if (done) { var tot = d.logs.reduce(function (s, l) { return s + l[1]; }, 0) + (+v.act); d.res = { pct: 100, act: d.logs.length ? tot : +v.act, text: v.text, files: files, by: ME, at: NOW }; d.logs.unshift(['03/11', +v.act, 100, 'Báo kết quả: ' + v.text]); closeModal(); L.setSt(it, target === 'Hoàn thành' ? 'Hoàn thành' : 'Hoàn thành - Chờ duyệt'); sys(it, 'ri-send-plane-line', 'đã gửi kết quả' + (it.rv && it.rv !== '—' ? ' cho @' + it.rv + ' duyệt' : '')); }
          else { d.logs.unshift(['03/11', +v.act, +v.pct, v.text]); closeModal(); sys(it, 'ri-line-chart-line', 'cập nhật tiến độ ' + v.pct + '%: ' + v.text); done2(it, '<i class="ri-line-chart-line"></i> Đã lưu tiến độ ' + v.pct + '%', 'ri-line-chart-line', 'cập nhật tiến độ ' + v.pct + '%'); }
          cur = it; tab = 'res'; show(); paint();
        });
      if (done) md.addEventListener('input', function (e) { if (!e.target.matches('[data-k=act]')) return; var a = +e.target.value, eff = md.querySelector('[data-eff]'); if (eff) eff.value = a > 0 && d.hours ? Math.round(d.hours / a * 100) + '%' : '—'; });
    },
    reason: function (it, s) {
      var T = { 'Từ chối kết quả': ['Từ chối kết quả', 'Lý do / cần sửa gì', 1], 'Từ chối': ['Từ chối kết quả xử lý', 'Lý do', 1], 'Tạm dừng': ['Tạm dừng nhiệm vụ', 'Lý do tạm dừng', 0], 'Mở lại': ['Mở lại', 'Lý do mở lại', 1] }[s];
      modal(mhead(T[0], esc(it.name)) + '<div class="mk-tdm-b">' + fld(T[1], '<textarea class="form-control form-control-sm" rows="3" data-k="r"></textarea>', T[2], 'r') + '<div class="mk-tdm-note"><i class="ri-information-line"></i>Lý do được ghi vào bình luận và gửi thông báo cho ' + (s === 'Tạm dừng' ? 'người giao' : (isI ? 'người xử lý' : 'người làm')) + '.</div></div>' +
        '<div class="mk-tdm-ft"><button type="button" class="v2-btn v2-btn--sm ' + (T[2] && s !== 'Mở lại' ? 'v2-btn--danger' : 'v2-btn--primary') + '" data-ok="1">Xác nhận</button><button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" data-mx="1">Huỷ</button></div>',
        function (e) {
          if (!e.target.closest('[data-ok]')) return; var r = md.querySelector('[data-k=r]').value.trim();
          if (!showErr(T[2] && !r ? { r: 'Nhập lý do.' } : {})) return;
          var d = det(it); if (d.res && /Từ chối/.test(s)) { d.res.no = { by: ME, at: NOW, note: r }; delete d.res.ok; }
          closeModal(); L.setSt(it, s); sys(it, L.ICON[s] || 'ri-chat-3-line', T[0].toLowerCase() + (r ? ': “' + r + '”' : '')); cur = it; show(); paint();
        });
    },
    confirmDel: function (it) {
      modal(mhead('Xoá ' + N + '?') + '<div class="mk-tdm-b"><p class="mk-tdm-p">“' + esc(it.name) + '” sẽ bị xoá khỏi danh sách. Bình luận, file và lịch sử đi kèm cũng bị xoá.</p></div><div class="mk-tdm-ft"><button type="button" class="v2-btn v2-btn--sm v2-btn--danger" data-ok="1"><i class="ri-delete-bin-line"></i> Xoá</button><button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" data-mx="1">Huỷ</button></div>',
        function (e) { if (!e.target.closest('[data-ok]')) return; it.deleted = true; closeModal(); close(); L.render(); L.toast('<i class="ri-delete-bin-line"></i> Đã xoá ' + N + ' · <a href="javascript:void(0)" class="mk-undo">Hoàn tác</a>'); var u = document.querySelector('.mk-undo'); if (u) u.addEventListener('click', function () { it.deleted = false; L.render(); L.toast('<i class="ri-arrow-go-back-line"></i> Đã khôi phục'); }); });
    },
    create: function (pre) { draft = { pre: pre || {} }; mode = 'create'; cur = {}; show(); paintForm(); },
    edit: function (it) { cur = it; draft = { it: it }; mode = 'edit'; show(); paintForm(); }
  };
  function opt(list, v) { return list.map(function (x) { return '<option' + (x === v ? ' selected' : '') + '>' + esc(x) + '</option>'; }).join(''); }
  // 05/11 — form Tạo / Sửa theo khuôn app (U27 hàng "+ Thêm", U32 chip ưu tiên tô màu, U33 giờ hạn 17:30, U34 Thiết lập trong form; web giữ Lặp lại + nút Giao & tạo tiếp riêng)
  var SPACES = [L.spaceName, 'Phòng Kỹ thuật', 'Phòng Kinh doanh'];
  function priChips(cur) { return '<input type="hidden" data-k="pri" value="' + esc(cur) + '"><div class="mk-td-prio">' + PRI.map(function (p) { return '<button type="button" data-prio="' + esc(p[0]) + '" style="--pc:' + p[1] + '" class="' + (p[0] === cur ? 'on' : '') + '">' + (p[0] === cur ? '<i class="ri-check-line"></i>' : '') + esc(p[0]) + '</button>'; }).join('') + '</div>'; }
  function setCount(f) { var n = 0; if (!f) return 0; var g = function (k) { var x = f.querySelector('[data-k=' + k + ']'); return x ? x.value.trim() : ''; };
    if (g('rv')) n++; if (g('watch')) n++; if (g('tags')) n++; if (g('report') && g('report') !== 'Không yêu cầu') n++; if (g('repeat') && g('repeat') !== 'Không lặp') n++; return n; }
  // Checklist + Nhiệm vụ con trong form — bám CreateTaskModal.vue (ô thêm + Enter, Thêm nhanh n dòng, mỗi dòng sửa / tick / xoá; nhiệm vụ con: Tên · Người làm · Hạn · Giờ hạn, bắt buộc tên + người làm + hạn)
  function clRow(c) { return '<div class="mk-fcl-i" data-cli="1"><i class="ri-draggable mk-fdrag" data-tip="Kéo để đổi thứ tự"></i><input type="checkbox" data-clk="1"' + (c[1] ? ' checked' : '') + '><input class="form-control form-control-sm' + (c[1] ? ' strike' : '') + '" data-clt="1" placeholder="Nhập nội dung..." value="' + esc(c[0]) + '"><button type="button" class="mk-fic" data-cldel="1" data-tip="Xoá"><i class="ri-delete-bin-6-line"></i></button></div>'; }
  function clBlock(cl) { return '<div class="mk-fblk"><div class="mk-fblk-h"><span class="mk-fblk-ic"><i class="ri-list-check-2"></i></span><b>Checklist</b><span class="mk-fblk-n" data-clcnt="1"></span><button type="button" class="mk-fquick" data-quick="cl"><i class="ri-flashlight-line"></i>Thêm nhanh checklist</button></div>' +
    '<div class="mk-fadd"><input class="form-control form-control-sm" data-clnew="1" placeholder="Nhập mục checklist và Enter"><button type="button" class="mk-fic bd" data-cladd="1" data-tip="Thêm"><i class="ri-add-line"></i></button></div><div class="mk-fcl-list" data-cllist="1">' + cl.map(clRow).join('') + '</div></div>'; }
  function subCells(s, nw) { var a = nw ? 'data-sn' : 'data-s'; return '<input class="form-control form-control-sm" ' + a + 't="1" placeholder="Tên nhiệm vụ con" value="' + esc(s[0] || '') + '"><select class="form-control form-control-sm" ' + a + 'w="1"><option value="">Người làm...</option>' + opt(L.PEOPLE, s[1] || '') + '</select><input type="date" class="form-control form-control-sm" ' + a + 'd="1" value="' + esc(s[3] || '') + '"><input type="time" class="form-control form-control-sm" ' + a + 'h="1" value="' + esc(s[4] || '17:30') + '">'; }
  function subRow(s) { return '<div class="mk-fsub-i" data-subi="1"><span class="mk-fsub-n"><i class="ri-node-tree"></i></span>' + subCells(s) + '<button type="button" class="mk-fic" data-subdel="1" data-tip="Xoá"><i class="ri-delete-bin-6-line"></i></button><small class="mk-fsub-err" data-suberr="1"></small></div>'; }
  function subBlock(sub, e) { return '<div class="mk-fblk"><div class="mk-fblk-h"><span class="mk-fblk-ic"><i class="ri-node-tree"></i></span><b>Nhiệm vụ con</b><span class="mk-fblk-n" data-subcnt="1"></span><button type="button" class="mk-fquick" data-quick="sub"><i class="ri-flashlight-line"></i>Thêm nhanh nhiệm vụ con</button></div>' +
    '<div class="mk-fsub-hd"><span></span><span>Tên nhiệm vụ con</span><span>Người làm</span><span>Hạn (ngày)</span><span>Giờ hạn</span><span></span></div>' +
    '<div class="mk-fsub-i add"><span class="mk-fsub-n"><i class="ri-add-line"></i></span>' + subCells([], 1) + '<button type="button" class="mk-fic bd" data-subadd="1" data-tip="Thêm"><i class="ri-add-line"></i></button></div>' +
    '<div class="mk-fsub-list" data-sublist="1">' + sub.map(subRow).join('') + '</div><small class="mk-td-mut">Khi Giao việc, mỗi dòng thành 1 nhiệm vụ riêng giao cho người làm của dòng đó; nhiệm vụ cha chỉ Hoàn thành khi các nhiệm vụ con đã xong.</small></div>'; }
  function clSync() { var r = pn.querySelectorAll('[data-cli]'), dn = pn.querySelectorAll('[data-clk]:checked').length, c = pn.querySelector('[data-clcnt]'); if (c) c.textContent = dn + '/' + r.length + ' hoàn thành'; var sc = pn.querySelector('[data-subcnt]'); if (sc) sc.textContent = pn.querySelectorAll('[data-subi]').length + ' nhiệm vụ con'; }
  function clAdd(t) { pn.querySelector('[data-cllist]').insertAdjacentHTML('beforeend', clRow([t, 0])); clSync(); }
  function subAdd() { var g = function (k) { return pn.querySelector('[data-sn' + k + ']'); }; var t = g('t').value.trim(); if (!t) { g('t').classList.add('is-invalid'); g('t').focus(); return; } g('t').classList.remove('is-invalid');
    pn.querySelector('[data-sublist]').insertAdjacentHTML('beforeend', subRow([t, g('w').value, 'Chờ bắt đầu', g('d').value, g('h').value || '17:30'])); g('t').value = ''; g('w').value = ''; g('d').value = ''; g('h').value = '17:30'; g('t').focus(); clSync(); }
  function subCheck() { var bad = 0; pn.querySelectorAll('[data-subi]').forEach(function (r) { var m = []; [['t', 'tên'], ['w', 'người làm'], ['d', 'hạn']].forEach(function (k) { var x = r.querySelector('[data-s' + k[0] + ']'), miss = !x.value.trim(); x.classList.toggle('is-invalid', miss); if (miss) m.push(k[1]); }); r.querySelector('[data-suberr]').textContent = m.length ? 'Nhập ' + m.join(', ') + '.' : ''; if (m.length) bad++; }); return bad; }
  function paintForm() {
    var e = draft.it, pre = draft.pre || {}, d = e ? det(e) : null;
    var who = e ? e.who : pre.by === 'who' ? pre.k : ME, proj = e ? (e.common ? PROJ[0] : e.proj) : pre.by === 'proj' ? pre.k : PROJ[0];
    var time = d && d.time ? d.time : '17:30';
    // 05/11 [U]: Ngày bắt đầu không bắt buộc — ẩn sau '+ Ngày bắt đầu'; để trống thì lấy ngày giao việc (giữ báo cáo lọc theo khoảng start → due)
    var hasStart = !isI && e && e.x.start;
    var dueRow = '<div class="mk-tdm-row">' +
        fld(isI ? 'Hạn xử lý' : 'Hạn hoàn thành', '<input type="date" class="form-control form-control-sm" data-k="due" value="' + (e ? iso(e.due) : '') + '">', 1, 'due', 6) +
        fld('Giờ hạn', '<input type="time" class="form-control form-control-sm" data-k="time" value="' + esc(time) + '">', 1, 'time', 6) + '</div>' +
      '<div class="mk-td-chips mk-td-chips-f"><span>Chọn nhanh hạn:</span>' + [['Hôm nay', 0], ['Ngày mai', 1], ['Thứ 6 này', 4], ['+1 tuần', 7]].map(function (c) { return '<button type="button" class="mk-td-chip" data-fqd="' + addDays(c[1]) + '">' + c[0] + '</button>'; }).join('') + (isI ? '' : '<button type="button" class="mk-td-addstart" data-addstart="1"' + (hasStart ? ' hidden' : '') + '><i class="ri-add-line"></i>Ngày bắt đầu</button>') + '<small class="mk-td-mut">Chọn ngày → giờ tự điền 17:30 (hết giờ làm việc), sửa được.</small></div>' +
      (isI ? '' : '<div class="mk-td-startrow" data-startrow="1"' + (hasStart ? '' : ' hidden') + '><div class="mk-tdm-row">' + fld('Ngày bắt đầu', '<input type="date" class="form-control form-control-sm" data-k="start" value="' + (hasStart ? '2026-' + e.x.start.split('/').reverse().join('-') : '') + '">', 0, 'start', 6) + '<div class="mk-tdm-f c6 mk-td-starthint"><small class="mk-td-mut">Dùng khi giao trước, làm sau (VD: tuần sau mới bắt đầu). Để trống: lấy ngày giao việc. Thời điểm bắt đầu thực tế tự ghi khi người làm bấm Bắt đầu.</small></div></div></div>');
    var spaceRow = '<div class="mk-tdm-row">' + fld('Không gian làm việc', '<select class="form-control form-control-sm" data-k="space">' + opt(SPACES, L.spaceName) + '</select>', 1, null, 2) + fld('Dự án / Nhóm', '<select class="form-control form-control-sm" data-k="proj">' + opt(PROJ, proj) + '</select>', 0, null, 2) + '</div>';
    var body;
    if (isI) {
      body = spaceRow + fld('Tên vấn đề', '<input class="form-control form-control-sm" data-k="name" placeholder="VD: Tủ MSB giao sai thông số dòng cắt" value="' + esc(e ? e.name : '') + '">', 1, 'name') +
        '<div class="mk-tdm-row">' + fld('Loại vấn đề', '<select class="form-control form-control-sm" data-k="itype"><option value="">— Chọn —</option>' + opt(ITYPE, e ? (det(e).itype || ITYPE[0]) : '') + '</select>', 1, 'itype', 4) + fld('Mức độ ảnh hưởng', '<select class="form-control form-control-sm" data-k="impact"><option value="">— Chọn —</option>' + opt(['Thấp', 'Trung bình', 'Cao'], e ? (det(e).impact || 'Trung bình') : '') + '</select>', 1, 'impact', 4) + fld('Nguồn phát hiện', '<select class="form-control form-control-sm" data-k="src"><option value="">— Chọn —</option>' + opt(ISRC, e ? (det(e).src || ISRC[0]) : '') + '</select>', 1, 'src', 4) + '</div>' +
        fld('Mức độ ưu tiên', priChips(e ? e.pri.t : PRI[1][0]), 1) +
        '<div class="mk-tdm-row">' + fld('Người phụ trách xử lý', '<select class="form-control form-control-sm" data-k="who"><option value="">Để trống — trưởng bộ phận phân công</option>' + opt(L.PEOPLE, e ? e.who : (pre.by === 'who' ? pre.k : '')) + '</select>', 0, 'who', 2) + fld('Phòng ban xử lý', '<select class="form-control form-control-sm" data-k="dept"><option value="">— Chọn —</option>' + opt(IDEPT, e ? (det(e).dept || '') : '') + '</select>', 0, 'dept', 2) + '</div>' +
        '<div class="mk-td-route" data-route="1"></div>' +
        '<div class="mk-tdm-row">' + fld('Người duyệt đóng', '<select class="form-control form-control-sm" data-k="rv"><option value="">Không có — báo xong là Hoàn thành</option>' + opt(L.PEOPLE.filter(function (p) { return p !== ME; }), e ? (e.rv && e.rv !== '—' ? e.rv : '') : 'Nguyễn Thị Hằng') + '</select>', 0, 'rv', 2) + fld('Người báo', '<input class="form-control form-control-sm" disabled value="' + esc(e ? e.cr : ME) + '">', 0, null, 2) + '</div>' +
        dueRow +
        fld('Mô tả', '<textarea class="form-control form-control-sm" rows="3" data-k="desc" placeholder="Mô tả hiện tượng, vị trí, ảnh hưởng…">' + esc(d ? d.desc : '') + '</textarea>', 1, 'desc') +
        fld('Thẻ (Tags)', '<input class="form-control form-control-sm" data-k="tags" placeholder="Nhập thẻ, cách nhau bởi dấu phẩy" value="' + esc(e ? (e.x.tags || []).join(', ') : '') + '">');
    } else {
      var hasCl = d && d.cl.length, hasSub = d && d.sub.length, hasF = d && d.files.length;
      var rep = d && d.report ? d.report : 'Không yêu cầu', rpt = d && d.repeat ? d.repeat : 'Không lặp';
      var setb = fld('Người duyệt kết quả', '<select class="form-control form-control-sm" data-k="rv"><option value="">Không có — làm xong là Hoàn thành</option>' + opt(L.PEOPLE.filter(function (p) { return p !== ME; }), e ? (e.rv && e.rv !== '—' ? e.rv : '') : 'Nguyễn Thị Hằng') + '</select><small class="mk-td-mut">Có người duyệt: báo kết quả xong chờ duyệt. Không có: báo xong là Hoàn thành.</small>') +
        fld('Người theo dõi', '<input class="form-control form-control-sm" data-k="watch" placeholder="Chọn người, cách nhau bởi dấu phẩy" value="' + esc(d ? d.watch.join(', ') : '') + '"><small class="mk-td-mut">Nhận thông báo mọi thay đổi, không thao tác được.</small>') +
        fld('Thẻ (Tags)', '<input class="form-control form-control-sm" data-k="tags" placeholder="Nhập thẻ, cách nhau bởi dấu phẩy" value="' + esc(e ? (e.x.tags || []).join(', ') : '') + '"><small class="mk-td-mut">Lọc và tìm nhanh trên danh sách.</small>') +
        '<div class="mk-tdm-row">' + fld('Yêu cầu báo cáo tiến độ', '<select class="form-control form-control-sm" data-k="report">' + opt(['Không yêu cầu', 'Hằng ngày', 'Hằng tuần (Thứ 6)', 'Hằng tháng (ngày 25)'], rep.replace(/ lúc .*/, '')) + '</select>', 0, null, 2) + fld('Giờ nhắc', '<input type="time" class="form-control form-control-sm" data-k="rh" value="17:00">', 0, null, 2) + '</div><small class="mk-td-mut mk-td-setd">Đến giờ, người làm nhận nhắc cập nhật tiến độ; mỗi lần cập nhật ghi vào Nhật ký tiến độ.</small>' +
        fld('Lặp lại', '<select class="form-control form-control-sm" data-k="repeat">' + opt(['Không lặp', 'Hằng ngày', 'Hằng tuần', 'Hằng tháng', 'Hằng quý', 'Hằng năm'], rpt.split(' ')[0] === 'Hằng' ? rpt.split(' ·')[0] : 'Không lặp') + '</select><small class="mk-td-mut">Đến kỳ, hệ thống tự tạo bản sao nhiệm vụ cho kỳ mới.</small>');
      body = spaceRow +
        fld('Loại nhiệm vụ', '<div class="mk-td-seg2"><label><input type="radio" name="tt" data-k="type" value="Nhiệm vụ cụ thể"' + (!d || d.type !== 'Nhiệm vụ chung' ? ' checked' : '') + '>Nhiệm vụ cụ thể</label><label><input type="radio" name="tt" data-k="type" value="Nhiệm vụ chung"' + (d && d.type === 'Nhiệm vụ chung' ? ' checked' : '') + '>Nhiệm vụ chung</label></div>', 1) +
        fld('Tên công việc', '<input class="form-control form-control-sm" data-k="name" placeholder="VD: Thiết kế popup tạo nhiệm vụ" value="' + esc(e ? e.name : '') + '">', 1, 'name') +
        '<div class="mk-tdm-row">' + fld('Người thực hiện', '<select class="form-control form-control-sm" data-k="who">' + opt(L.PEOPLE, who) + '</select>', 1, 'who', 2) + fld('Số giờ được giao', '<input type="number" step="0.5" class="form-control form-control-sm" data-k="hours" value="' + (d && d.hours || '') + '" placeholder="VD: 8.0">', 1, 'hours', 2) + '</div>' +
        (e ? '' : '<div class="mk-td-tog"><label><input type="checkbox" data-k="needap"><b>Cần duyệt triển khai</b></label><small data-togtx="1">Tắt: giao xong → <b>Chờ bắt đầu</b>, người làm bắt đầu được ngay.</small><label class="mk-td-now" data-now="1"' + (who === ME ? '' : ' hidden') + '><input type="checkbox" data-k="startnow">Bắt đầu ngay (tự giao cho mình → Đang thực hiện)</label></div>') +
        dueRow +
        '<div class="mk-tdm-row">' + fld('Mức độ ưu tiên', priChips(e ? e.pri.t : PRI[0][0]), 1, null, 2) + fld('Meeting', '<select class="form-control form-control-sm" data-k="meeting"><option value="">Không gắn</option>' + opt(['TPE.MET.NB.26.0031 · Họp BTC hội nghị công đoàn', 'TPE.MET.NB.26.0028 · Giao ban phòng tuần 44'], d ? d.meeting : '') + '</select>', 0, null, 2) + '</div>' +
        fld('Mô tả', '<textarea class="form-control form-control-sm" rows="3" data-k="desc" placeholder="Mô tả ngắn gọn yêu cầu…">' + esc(d ? d.desc : '') + '</textarea>') +
        '<div class="mk-td-fsec" data-fsec="cl"' + (hasCl ? '' : ' hidden') + '>' + clBlock(d ? d.cl : []) + '</div>' +
        '<div class="mk-td-fsec" data-fsec="sub"' + (hasSub ? '' : ' hidden') + '>' + subBlock(d ? d.sub : [], e) + '</div>' +
        '<div class="mk-td-fsec" data-fsec="file"' + (hasF ? '' : ' hidden') + '>' + fld('Tệp đính kèm', '<div class="mk-td-files" data-ffiles="1">' + (d ? d.files.map(fileChip).join('') : '') + '<button type="button" class="mk-td-add" data-fup="1"><i class="ri-upload-2-line"></i>Tải lên</button></div>') + '</div>' +
        '<div class="mk-td-addrow"><span>Thêm:</span>' + [['cl', 'ri-checkbox-multiple-line', 'Checklist', hasCl], ['sub', 'ri-node-tree', 'Nhiệm vụ con', hasSub], ['file', 'ri-attachment-2', 'Tệp', hasF]].map(function (a) { return '<button type="button" class="mk-td-add" data-addf="' + a[0] + '"' + (a[3] ? ' hidden' : '') + '><i class="' + a[1] + '"></i>' + a[2] + '</button>'; }).join('') + '</div>' +
        '<section class="mk-td-fset" data-fset="1"><h6 data-fsett="1"><i class="ri-settings-3-line"></i>Thiết lập<em data-fsetn="1"></em><small>Người duyệt kết quả · Người theo dõi · Thẻ · Báo cáo tiến độ · Lặp lại</small><i class="ri-arrow-down-s-line mk-td-car"></i></h6><div class="mk-td-fsetb">' + setb + '</div></section>';
    }
    pn.innerHTML = '<div class="mk-td-hd"><div class="mk-td-r1"><b class="mk-td-ft">' + (e ? 'Sửa ' + N : 'Thêm mới ' + N) + '</b><span class="mk-td-sp"></span><button type="button" class="mk-td-ic" data-fx="1" data-tip="Đóng"><i class="ri-close-line"></i></button></div>' +
      '<div class="mk-td-crumb"><i class="ri-community-line"></i>' + esc(L.spaceName) + '</div></div>' +
      '<div class="mk-td-body mk-td-form">' + body + '</div><div class="mk-td-fbar">' + (e ? '<button type="button" class="v2-btn v2-btn--sm v2-btn--primary" data-save="keep"><i class="ri-save-3-line"></i> Lưu thay đổi</button>' :
        (isI ? '<button type="button" class="v2-btn v2-btn--sm v2-btn--primary" data-save="assign"><i class="ri-send-plane-2-line"></i> Gửi vấn đề</button>' : '<button type="button" class="v2-btn v2-btn--sm v2-btn--primary" data-save="assign"><i class="ri-send-plane-2-line"></i> Giao việc</button><button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" data-save="next"><i class="ri-add-line"></i> Giao & tạo tiếp</button><button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" data-save="draft"><i class="ri-draft-line"></i> Lưu nháp</button>')) +
      '<button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" data-fx="1"><i class="ri-close-line"></i> Huỷ</button></div>';
    var n = pn.querySelector('[data-k=name]'); if (n) setTimeout(function () { n.focus(); }, 30);
    formSync(); clSync();
  }
  // U31b: công tắc duyệt triển khai + 'Bắt đầu ngay' · U36: báo trước trạng thái vấn đề theo người nhận
  function formSync() {
    if (mode === 'view') return;
    var w = pn.querySelector('[data-k=who]'), ap = pn.querySelector('[data-k=needap]'), tt = pn.querySelector('[data-togtx]'), nw = pn.querySelector('[data-now]'), rt = pn.querySelector('[data-route]');
    var fs = pn.querySelector('[data-fsetn]'); if (fs) fs.textContent = setCount(pn.querySelector('[data-fset]')) + '/5 đang dùng';
    if (ap && tt) tt.innerHTML = ap.checked ? 'Bật: giao xong → <b>Chờ phê duyệt triển khai</b>, duyệt xong người làm mới bắt đầu.' : 'Tắt: giao xong → <b>Chờ bắt đầu</b>, người làm bắt đầu được ngay.';
    if (nw && w) { nw.hidden = w.value !== ME; if (nw.hidden) nw.querySelector('input').checked = false; }
    if (rt && w) { var dp = pn.querySelector('[data-k=dept]').value; rt.innerHTML = w.value ? '<i class="ri-arrow-right-circle-line"></i>Gửi xong → <b>Đã phân công</b>: ' + esc(w.value) + ' nhận thông báo và bấm Nhận xử lý.' : dp ? '<i class="ri-arrow-right-circle-line"></i>Gửi xong → <b>Mới ghi nhận</b>: trưởng bộ phận ' + esc(dp) + ' nhận thông báo và phân công.' : '<i class="ri-information-line"></i>Chọn Người phụ trách hoặc Phòng ban xử lý.'; }
  }
  pn.addEventListener('change', function (ev) { if (ev.target.matches && ev.target.matches('[data-clk]')) { ev.target.nextElementSibling.classList.toggle('strike', ev.target.checked); clSync(); } if (ev.target.matches && ev.target.matches('[data-k=due]')) { var tm = pn.querySelector('[data-k=time]'); if (tm && !tm.value) tm.value = '17:30'; } formSync(); });
  pn.addEventListener('keydown', function (ev) { if (mode === 'view' || ev.key !== 'Enter') return; if (ev.target.matches('[data-clnew]')) { ev.preventDefault(); if (ev.target.value.trim()) { clAdd(ev.target.value.trim()); ev.target.value = ''; } } else if (ev.target.matches('[data-snt]')) { ev.preventDefault(); subAdd(); } });
  pn.addEventListener('input', function (ev) { if (mode !== 'view' && ev.target.closest('[data-fset]')) formSync(); });
  pn.addEventListener('click', function (ev) {
    if (mode === 'view') return;
    var pc = ev.target.closest('[data-prio]'); if (pc) { pn.querySelector('[data-k=pri]').value = pc.getAttribute('data-prio'); pn.querySelectorAll('[data-prio]').forEach(function (x) { var on = x === pc; x.classList.toggle('on', on); x.innerHTML = (on ? '<i class="ri-check-line"></i>' : '') + esc(x.getAttribute('data-prio')); }); return; }
    var af = ev.target.closest('[data-addf]'); if (af) { var k = af.getAttribute('data-addf'), sc = pn.querySelector('[data-fsec=' + k + ']'); sc.hidden = false; af.hidden = true; var f0 = sc.querySelector('[data-clnew], [data-snt], textarea'); if (f0) f0.focus(); if (k === 'file') pn.querySelector('[data-fup]').click(); return; }
    if (ev.target.closest('[data-cladd]')) { var ni = pn.querySelector('[data-clnew]'); if (ni.value.trim()) { clAdd(ni.value.trim()); ni.value = ''; } ni.focus(); return; }
    if (ev.target.closest('[data-cldel]')) { ev.target.closest('[data-cli]').remove(); clSync(); return; }
    if (ev.target.closest('[data-subadd]')) { subAdd(); return; }
    if (ev.target.closest('[data-subdel]')) { ev.target.closest('[data-subi]').remove(); clSync(); return; }
    var qk = ev.target.closest('[data-quick]'); if (qk) { var kk = qk.getAttribute('data-quick'); openMenu(qk, formPop(kk === 'cl' ? 'Thêm nhanh checklist' : 'Thêm nhanh nhiệm vụ con', '<div class="mk-lpop-row"><span>Số dòng</span><input type="number" min="1" max="20" class="form-control form-control-sm" data-f="n" value="3"></div><small class="mk-td-mut">Tạo sẵn các dòng trống để nhập liền.</small>', 'Thêm'), function (v) { var n = Math.max(1, Math.min(20, +v.n || 3)); for (var i = 0; i < n; i++) { if (kk === 'cl') pn.querySelector('[data-cllist]').insertAdjacentHTML('beforeend', clRow(['', 0])); else pn.querySelector('[data-sublist]').insertAdjacentHTML('beforeend', subRow(['', '', 'Chờ bắt đầu', '', '17:30'])); } clSync(); var f1 = pn.querySelector(kk === 'cl' ? '[data-cllist] [data-clt]:last-of-type' : '[data-sublist] [data-subi]:last-child [data-st]'); }); return; }
    if (ev.target.closest('[data-addstart]')) { pn.querySelector('[data-startrow]').hidden = false; ev.target.closest('[data-addstart]').hidden = true; pn.querySelector('[data-k=start]').focus(); return; }
    if (ev.target.closest('[data-fsett]')) { pn.querySelector('[data-fset]').classList.toggle('open'); return; }
    if (ev.target.closest('[data-fup]')) { var box = pn.querySelector('[data-ffiles]'); box.insertAdjacentHTML('afterbegin', fileChip({ n: 'Tai-lieu-' + (box.querySelectorAll('.mk-td-file').length + 1) + '.pdf', s: '240 KB' })); return; }
    var q = ev.target.closest('[data-fqd]'); if (q) { var tm = pn.querySelector('[data-k=time]'); if (tm && !tm.value) tm.value = '17:30'; pn.querySelector('[data-k=due]').value = q.getAttribute('data-fqd'); pn.querySelectorAll('[data-fqd]').forEach(function (x) { x.classList.toggle('on', x === q); }); return; }
    if (ev.target.closest('[data-fx]')) { if (mode === 'edit') { mode = 'view'; return paint(); } return close(); }
    var sv = ev.target.closest('[data-save]'); if (!sv) return; var how = sv.getAttribute('data-save');
    var v = {}; pn.querySelectorAll('[data-k]').forEach(function (x) { if (x.type === 'radio') { if (x.checked) v[x.getAttribute('data-k')] = x.value; } else if (x.type === 'checkbox') v[x.getAttribute('data-k')] = x.checked; else v[x.getAttribute('data-k')] = x.value.trim(); });
    var er = {}; if (!v.name) er.name = 'Nhập tên ' + N + '.';
    if (how !== 'draft') { if (!v.due) er.due = 'Chọn hạn.'; if (!v.time) er.time = 'Chọn giờ hạn.'; if (!isI && !(+v.hours > 0)) er.hours = 'Nhập số giờ được giao.'; if (!isI && v.start && v.due && v.start > v.due) er.due = 'Hạn phải sau ngày bắt đầu.'; }
    if (isI) { if (!v.itype) er.itype = 'Chọn loại vấn đề.'; if (!v.impact) er.impact = 'Chọn mức độ ảnh hưởng.'; if (!v.src) er.src = 'Chọn nguồn phát hiện.'; if (!v.desc) er.desc = 'Nhập mô tả.'; if (!v.who && !v.dept) er.dept = 'Chọn Phòng ban xử lý hoặc Người phụ trách.'; }
    if (!isI && pn.querySelector('[data-sublist]') && subCheck()) er.sub = 1;
    if (!showErr(er, pn)) return;
    var pr = PRI.filter(function (x) { return x[0] === v.pri; })[0] || PRI[0], it = draft.it, created = !it;
    if (!it) {
      var nextNo = 151 + L.items.filter(function (x) { return x.isNew; }).length;
      it = { tr: document.createElement('tr'), isNew: 1, a: null, x: { code: isI ? 'ISS-202611-00' + (nextNo - 140) : 'TPE.TASK.NB.26.0' + nextNo, cmt: 0, file: 0, upd: NOW }, st: isI ? (v.who ? 'Đã phân công' : 'Mới ghi nhận') : how === 'draft' ? 'Nháp' : v.startnow && v.who === ME ? 'Đang thực hiện' : v.needap ? 'Chờ phê duyệt triển khai' : 'Chờ bắt đầu', cr: ME, ck: '—' };
      if (!isI) it.x.pct = 0;
      L.items.push(it);
      it.dt = { desc: '', cl: [], sub: [], watch: [], files: [], cmts: [], links: [], logs: [], his: [['ri-add-circle-line', ME, (how === 'draft' ? 'lưu nháp ' : 'tạo và giao ') + N, NOW]] };
    } else L.log(it, 'ri-edit-line', 'sửa thông tin ' + N);
    var d = det(it);
    it.name = v.name; it.who = isI ? (v.who || (v.dept ? v.dept : '—')) : v.who; it.rv = v.rv || '—';
    if (isI) { d.itype = v.itype; d.impact = v.impact; d.src = v.src; d.dept = v.dept; }
    if (v.due) setDue(it, v.due, v.time); else { it.due = ''; it.d = null; }
    it.pri = { t: pr[0], c: pr[1] }; it.common = v.proj === PROJ[0]; it.proj = it.common ? 'Việc chung của phòng' : v.proj; it.x.tags = v.tags ? v.tags.split(',').map(function (s) { return s.trim(); }).filter(Boolean) : [];
    if (v.start) { var sp = v.start.split('-'); it.x.start = sp[2] + '/' + sp[1]; } else if (!isI && !it.x.start) { var td0 = addDays(0).split('-'); it.x.start = td0[2] + '/' + td0[1]; }
    d.desc = v.desc; d.type = v.type || d.type || 'Nhiệm vụ cụ thể'; d.meeting = v.meeting || d.meeting || ''; d.time = v.time || d.time || '17:00';
    if (!isI) { d.watch = v.watch ? v.watch.split(',').map(function (s) { return s.trim(); }).filter(Boolean) : []; d.report = v.report && v.report !== 'Không yêu cầu' ? v.report + ' lúc ' + (v.rh || '17:00') : null; d.repeat = v.repeat && v.repeat !== 'Không lặp' ? v.repeat + ' · không kết thúc' : null;
      d.sub = [].slice.call(pn.querySelectorAll('[data-subi]')).map(function (r) { var g = function (k) { return r.querySelector('[data-s' + k + ']').value.trim(); }; return [g('t'), g('w'), 'Chờ bắt đầu', g('d'), g('h')]; }).filter(function (x) { return x[0]; });
      var fb = pn.querySelector('[data-ffiles]'); if (fb) d.files = [].slice.call(fb.querySelectorAll('.mk-td-file')).map(function (x) { return { n: x.querySelector('span').textContent, s: (x.querySelector('small') || {}).textContent || '' }; });
    }
    if (!isI) { d.hours = +v.hours || null; var old = {}; d.cl.forEach(function (c) { old[c[0]] = c[1]; }); d.cl = [].slice.call(pn.querySelectorAll('[data-cli]')).map(function (r) { return [r.querySelector('[data-clt]').value.trim(), r.querySelector('[data-clk]').checked ? 1 : 0]; }).filter(function (c) { return c[0]; }); syncCk(it); }
    mode = 'view'; L.render();
    L.toast('<i class="ri-checkbox-circle-line"></i> ' + (created ? (how === 'draft' ? 'Đã lưu nháp' : isI ? 'Đã gửi ' + N + ' — ' + (v.who ? esc(v.who) + ' nhận thông báo (Đã phân công)' : 'trưởng bộ phận ' + esc(v.dept) + ' nhận thông báo (Mới ghi nhận)') : 'Đã tạo ' + N + ' — ' + it.st + (v.who !== ME ? ', ' + esc(v.who) + ' nhận thông báo' : '')) : 'Đã lưu thay đổi'));
    if (how === 'next') { draft = { pre: {} }; mode = 'create'; paintForm(); return; }
    MKTD.open(it, 'detail');
  });
  window.addEventListener('resize', function () { if (document.body.classList.contains('mk-td-open')) place(); });
})();

// 11/11 [U] Màn 34 — Thống kê sử dụng TPE SMART AGENT (quản trị). User 11/11: "có tính được token của từng user đã dùng không?" → "làm 1 và 2".
// Số liệu demo; chi phí quy đổi theo bảng giá giả định (Sonnet 5.5, 26,000 ₫/USD) — bản thật đọc bảng giá cấu hình + log lượt hỏi.
// Biểu đồ: 3 màu kết quả đã chạy validate_palette (light): #14a085 · #d97706 · #6366f1 — PASS.
(function () {
  var host = document.querySelector('.v2-styles > .container-fluid'); if (!host) return;
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  function fmt(n) { return Number(n).toLocaleString('en-US'); }
  function fmtM(n) { return (n / 1e6).toFixed(1) + 'M'; }
  var PAL = ['#f472b6', '#60a5fa', '#fbbf24', '#34d399', '#a78bfa', '#f87171', '#2dd4bf', '#fb923c', '#818cf8'];
  function avc(n) { var h = 0; for (var i = 0; i < n.length; i++) h = (h * 31 + n.charCodeAt(i)) >>> 0; return PAL[h % PAL.length]; }
  function ini(n) { var p = n.trim().split(/\s+/); return ((p[p.length - 2] ? p[p.length - 2][0] : '') + p[p.length - 1][0]).toUpperCase(); }
  function av(n) { return '<span class="aiu-av" style="background:' + avc(n) + '">' + esc(ini(n)) + '</span>'; }
  var C = { ok: '#14a085', deny: '#d97706', na: '#6366f1' }, CL = { ok: 'Trả lời', deny: 'Bị chặn do quyền', na: 'Không hỗ trợ' };
  var VPT = 275, TPT = 12100; // ₫ và token trung bình / lượt (demo)

  // ---- dữ liệu ----
  var DAYS = [[1, 'CN', 12, 1, 1], [2, 'T2', 268, 21, 9], [3, 'T3', 291, 24, 11], [4, 'T4', 305, 22, 8], [5, 'T5', 312, 26, 10], [6, 'T6', 284, 19, 7], [7, 'T7', 41, 3, 2], [8, 'CN', 18, 1, 0], [9, 'T2', 330, 27, 12], [10, 'T3', 352, 31, 10], [11, 'T4', 141, 12, 4]];
  var T = DAYS.reduce(function (a, d) { a.ok += d[2]; a.deny += d[3]; a.na += d[4]; return a; }, { ok: 0, deny: 0, na: 0 }); T.all = T.ok + T.deny + T.na;
  var BUDGET = 3000000, spent = T.all * VPT, fore = Math.round(spent / 10.4 * 30 / 1000) * 1000;
  // [tên, mã phòng, mã NV, phòng, CHỨC VỤ (hồ sơ NV), lượt, chặn, hôm nay, hạn mức theo chức vụ, lần cuối]
  var U = [
    ['Trịnh Đức Anh', 'HN_KD1', '21410550', 'Phòng Kinh doanh 1', 'Nhân viên kinh doanh', 214, 31, 44, 50, '10:28'],
    ['Đỗ Mai Anh', 'HN_NSHC', '21410101', 'Phòng Nhân sự Hành chính', 'Trưởng phòng Nhân sự Hành chính', 187, 6, 23, 100, '10:22'],
    ['Ngô Quang Vinh', 'HN_KD2', '21410588', 'Phòng Kinh doanh 2', 'Trưởng phòng kinh doanh-CNV', 171, 4, 17, 150, '10:05'],
    ['Phạm Minh Đức', 'BGD', '11010001', 'Ban giám đốc', 'Tổng Giám đốc', 158, 0, 8, 0, '09:58'],
    ['Lâm Thị Ngọc', 'HCM_KD1', '31420118', 'Phòng Kinh doanh 1 (HCM)', 'Nhân viên kinh doanh', 149, 18, 41, 50, '10:31'],
    ['Đặng Minh Khoa', 'HN_KTCN', '21410177', 'Phòng Kỹ thuật công nghệ', 'Chuyên viên kỹ thuật', 132, 9, 12, 80, '09:40'],
    ['Lê Thu Trang', 'HN_NSHC', '21410210', 'Phòng Nhân sự Hành chính', 'Nhân viên hành chính tổng hợp', 118, 14, 12, 50, '08:51'],
    ['Phạm Văn Tú', 'HN_QTTT', '21410402', 'Phòng Quản trị thông tin', 'Nhân viên quản trị Web', 104, 2, 7, 50, '10:12'],
    ['Nguyễn Thu Trang', 'HN_KD1', '21410577', 'Phòng Kinh doanh 1', 'Trợ lý Kinh doanh - Dự án', 97, 11, 9, 80, '10:02'],
    ['Hoàng Thị Lan', 'HN_KT', '21410415', 'Phòng Kế toán', 'Nhân viên Kế toán thuế', 63, 7, 3, 50, 'Hôm qua']
  ];
  var D = [['Phòng Kinh doanh 1', 38, 742, 71], ['Phòng Nhân sự Hành chính', 18, 498, 29], ['Phòng Kinh doanh 2', 31, 433, 22], ['Phòng Kỹ thuật công nghệ', 27, 377, 24], ['Phòng Kinh doanh 1 (HCM)', 22, 268, 25], ['Ban giám đốc', 4, 171, 0], ['Phòng Quản trị thông tin', 9, 79, 7], ['Phòng Kế toán', 19, 47, 9]];
  var BLK = [['Xem nhiệm vụ toàn công ty', 82, 'Hỏi việc của phòng khác'], ['Xem nhiệm vụ của phòng', 61, 'Nhân viên hỏi việc của đồng nghiệp'], ['Xem báo cáo hiệu suất toàn công ty', 31, 'Xếp hạng, so sánh giữa các phòng'], ['Xem meeting của phòng', 13, 'Lịch họp của người khác']];
  var LOGS = {
    'Trịnh Đức Anh': [['10:28', 'Khách Gaochang còn việc nào quá hạn?', 'ok', 11840], ['10:24', 'Phòng Kinh doanh 2 đang chăm khách nào ở Hải Phòng?', 'deny', 8920], ['10:11', 'Tuần sau tôi có họp gì?', 'ok', 10230], ['09:47', 'Việc của anh Vinh tới đâu rồi?', 'deny', 9010], ['09:30', 'Hôm nay tôi có việc gì?', 'ok', 12410]]
  };

  // ---- khung ----
  var root = document.createElement('div'); root.className = 'aiu'; host.insertBefore(root, host.firstChild);
  var by = 'emp';
  function kpi(ic, lb, val, sub, extra) { return '<div class="aiu-kpi"><div class="h"><i class="' + ic + '"></i>' + lb + '</div><div class="v">' + val + '</div><div class="s">' + sub + '</div>' + (extra || '') + '</div>'; }
  function render() {
    var pct = Math.round(spent / BUDGET * 100), fpct = Math.round(fore / BUDGET * 100);
    root.innerHTML =
      '<div class="mk-tb aiu-tb"><div class="aiu-sel"><i class="ri-calendar-line"></i>Tháng 11/2026<i class="ri-arrow-down-s-line"></i></div><div class="aiu-sel"><i class="ri-building-line"></i>Tân Phát<i class="ri-arrow-down-s-line"></i></div>' +
      '<span class="aiu-asof">Số liệu đến 10:31 hôm nay · cập nhật mỗi 5 phút</span>' +
      '<div class="mk-tb-right"><button type="button" class="v2-btn v2-btn--sm v2-btn--secondary v2-btn--secondary-info v2-btn--prefix-sm mr-2" data-u="quota"><div class="v2-btn__prefix--sm"><i class="ri-settings-3-line" style="font-size:13px"></i></div> Cài hạn mức</button>' +
      '<button type="button" class="v2-btn v2-btn--sm v2-btn--secondary v2-btn--secondary-info btn-icon" title="Xuất Excel" data-u="xls"><i class="ri-file-excel-2-line" style="font-size:13px;margin-right:0"></i></button></div></div>' +
      '<div class="aiu-kpis">' +
        kpi('ri-chat-smile-3-line', 'Lượt hỏi', fmt(T.all), '<b class="up"><i class="ri-arrow-up-line"></i>18%</b> so với cùng kỳ tháng 10 · 168 / 214 người đã dùng') +
        kpi('ri-flashlight-line', 'Token đã dùng', fmtM(T.all * TPT), '<b>81%</b> đọc lại từ cache (giá rẻ hơn 10 lần)') +
        kpi('ri-money-dollar-circle-line', 'Chi phí ước tính', fmt(spent) + ' ₫', 'Ngân sách tháng ' + fmt(BUDGET) + ' ₫ · dự kiến cuối tháng ≈ ' + fmt(fore) + ' ₫',
          '<div class="aiu-bud"><i style="width:' + pct + '%"></i><em style="left:' + Math.min(fpct, 100) + '%" title="Dự kiến cuối tháng ' + fpct + '%"></em></div>') +
        kpi('ri-lock-2-line', 'Bị chặn do quyền', fmt(T.deny), '<b>' + (T.deny / T.all * 100).toFixed(1) + '%</b> lượt hỏi · không đọc dữ liệu nào') +
      '</div>' +
      '<div class="aiu-row2"><section class="aiu-card aiu-chart"><div class="aiu-ch"><b>Lượt hỏi theo ngày</b><div class="aiu-leg">' + ['ok', 'deny', 'na'].map(function (k) { return '<span><i style="background:' + C[k] + '"></i>' + CL[k] + '</span>'; }).join('') + '</div></div>' + chart() + '</section>' +
      '<section class="aiu-card aiu-blk"><div class="aiu-ch"><b>Bị chặn nhiều nhất theo quyền</b></div><p class="aiu-hint">Gợi ý rà lại phân quyền: quyền nào bị hỏi nhiều mà người hỏi không có.</p>' +
        BLK.map(function (b) { return '<div class="aiu-bk"><div class="t"><b>' + esc(b[0]) + '</b><small>' + esc(b[2]) + '</small></div><span>' + b[1] + '</span><div class="tr"><i style="width:' + Math.round(b[1] / BLK[0][1] * 100) + '%"></i></div></div>'; }).join('') + '</section></div>' +
      '<section class="tp-card px-3 py-2 mk-flat aiu-tbl"><div class="aiu-tabs">' + [['emp', 'Theo nhân viên'], ['dep', 'Theo phòng ban']].map(function (t) { return '<button type="button" data-by="' + t[0] + '" class="' + (by === t[0] ? 'on' : '') + '">' + t[1] + '</button>'; }).join('') + '<small>Sắp xếp theo chi phí giảm dần</small></div>' +
      '<div class="table-shell"><div class="table-wrapper scrollbar-thin">' + (by === 'emp' ? empTable() : depTable()) + '</div></div></section>';
  }
  function chart() {
    var W = 640, H = 210, L = 34, B = 24, top = 10, mx = 400, bw = 30, gap = (W - L - 8) / DAYS.length;
    var g = '';
    [0, 100, 200, 300, 400].forEach(function (v) { var y = top + (H - top - B) * (1 - v / mx); g += '<line x1="' + L + '" x2="' + W + '" y1="' + y + '" y2="' + y + '" class="gl"/><text x="' + (L - 6) + '" y="' + (y + 3.5) + '" class="ax" text-anchor="end">' + v + '</text>'; });
    DAYS.forEach(function (d, i) {
      var x = L + 8 + i * gap + (gap - bw) / 2, base = H - B, segs = [['ok', d[2]], ['deny', d[3]], ['na', d[4]]], y = base, part = d[0] === 11;
      var tot = d[2] + d[3] + d[4];
      g += '<g class="bar' + (part ? ' part' : '') + '" data-i="' + i + '"><rect class="hit" x="' + (x - (gap - bw) / 2) + '" y="' + top + '" width="' + gap + '" height="' + (H - top - B) + '"/>';
      segs.forEach(function (s, j) {
        if (!s[1]) return; var h = (H - top - B) * s[1] / mx; y -= h; var last = segs.slice(j + 1).every(function (z) { return !z[1]; });
        var hh = Math.max(0, h - (j ? 2 : 0));
        g += last ? '<path d="' + roundTop(x, y, bw, hh, 4) + '" fill="' + C[s[0]] + '"/>' : '<rect x="' + x + '" y="' + y + '" width="' + bw + '" height="' + hh + '" fill="' + C[s[0]] + '"/>';
      });
      if (tot > 300) g += '<text x="' + (x + bw / 2) + '" y="' + (y - 5) + '" class="lb" text-anchor="middle">' + tot + '</text>';
      g += '<text x="' + (x + bw / 2) + '" y="' + (H - 8) + '" class="ax" text-anchor="middle">' + d[0] + '/11</text></g>';
    });
    return '<div class="aiu-svg"><svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Lượt hỏi theo ngày, 1–11/11/2026">' + g + '</svg><div class="aiu-tip"></div></div>' +
      '<div class="aiu-note"><i class="ri-information-line"></i>11/11 tính đến 10:31 (cột nhạt). Cuối tuần ít dùng.</div>';
  }
  function roundTop(x, y, w, h, r) { r = Math.min(r, h, w / 2); return 'M' + x + ',' + (y + h) + 'V' + (y + r) + 'Q' + x + ',' + y + ' ' + (x + r) + ',' + y + 'H' + (x + w - r) + 'Q' + (x + w) + ',' + y + ' ' + (x + w) + ',' + (y + r) + 'V' + (y + h) + 'Z'; }
  function empTable() {
    return '<table class="data-table aiu-t"><thead><tr><th class="text-center">STT</th><th>Nhân viên</th><th>Chức vụ</th><th class="text-right">Lượt hỏi</th><th class="text-right">Bị chặn</th><th class="text-right">Token</th><th class="text-right">Chi phí</th><th>Hôm nay / hạn mức</th><th>Hỏi gần nhất</th><th class="text-center">Thao tác</th></tr></thead><tbody>' +
      U.map(function (u, i) {
        var p = u[8] ? Math.round(u[7] / u[8] * 100) : 0, warn = p >= 80;
        return '<tr><td class="text-center">' + (i + 1) + '</td><td><div class="aiu-emp">' + av(u[0]) + '<span>' + esc(u[0] + ' - ' + u[1] + ' - ' + u[2]) + '</span></div></td><td>' + esc(u[4]) + '</td>' +
          '<td class="text-right num">' + fmt(u[5]) + '</td><td class="text-right num">' + (u[6] ? fmt(u[6]) + ' <small>(' + Math.round(u[6] / u[5] * 100) + '%)</small>' : '0') + '</td>' +
          '<td class="text-right num">' + fmtM(u[5] * TPT) + '</td><td class="text-right num">' + fmt(u[5] * VPT) + ' ₫</td>' +
          '<td>' + (u[8] ? '<div class="aiu-q"><div class="tr"><i class="' + (warn ? 'w' : '') + '" style="width:' + p + '%"></i></div><span class="num">' + u[7] + '/' + u[8] + '</span>' + (warn ? '<span class="mk-badge" style="--c:#F59E0B">Gần chạm</span>' : '') + '</div>' : '<span class="aiu-unl">' + u[7] + ' · không giới hạn</span>') + '</td>' +
          '<td>' + esc(u[9]) + '</td><td class="text-center"><button type="button" class="aiu-ib" data-log="' + esc(u[0]) + '" title="Xem nhật ký lượt hỏi"><i class="ri-file-list-3-line"></i></button></td></tr>';
      }).join('') + '</tbody></table>';
  }
  function depTable() {
    var tot = D.reduce(function (s, d) { return s + d[2]; }, 0);
    return '<table class="data-table aiu-t"><thead><tr><th class="text-center">STT</th><th>Phòng ban</th><th class="text-right">Người đã dùng</th><th class="text-right">Lượt hỏi</th><th class="text-right">Bị chặn</th><th class="text-right">Token</th><th class="text-right">Chi phí</th><th>Tỉ trọng chi phí</th></tr></thead><tbody>' +
      D.map(function (d, i) { var p = Math.round(d[2] / tot * 100); return '<tr><td class="text-center">' + (i + 1) + '</td><td>' + esc(d[0]) + '</td><td class="text-right num">' + d[1] + '</td><td class="text-right num">' + fmt(d[2]) + '</td><td class="text-right num">' + fmt(d[3]) + ' <small>(' + Math.round(d[3] / d[2] * 100) + '%)</small></td><td class="text-right num">' + fmtM(d[2] * TPT) + '</td><td class="text-right num">' + fmt(d[2] * VPT) + ' ₫</td><td><div class="aiu-q"><div class="tr"><i style="width:' + p + '%"></i></div><span class="num">' + p + '%</span></div></td></tr>'; }).join('') + '</tbody></table>';
  }

  // ---- tooltip biểu đồ ----
  root.addEventListener('mousemove', function (e) {
    var tip = root.querySelector('.aiu-tip'); if (!tip) return; var g = e.target.closest('.bar');
    root.querySelectorAll('.bar.hov').forEach(function (x) { if (x !== g) x.classList.remove('hov'); });
    if (!g) { tip.classList.remove('on'); return; }
    g.classList.add('hov'); var d = DAYS[+g.dataset.i], t = d[2] + d[3] + d[4], box = root.querySelector('.aiu-svg').getBoundingClientRect(), r = g.querySelector('.hit').getBoundingClientRect();
    tip.innerHTML = '<b>' + d[1] + ', ' + d[0] + '/11/2026' + (d[0] === 11 ? ' (đến 10:31)' : '') + '</b>' + [['ok', d[2]], ['deny', d[3]], ['na', d[4]]].map(function (s) { return '<div><i style="background:' + C[s[0]] + '"></i>' + CL[s[0]] + '<span>' + fmt(s[1]) + '</span></div>'; }).join('') + '<div class="t">Tổng ' + fmt(t) + ' lượt · ≈ ' + fmt(t * VPT) + ' ₫</div>';
    tip.classList.add('on'); var x = r.right - box.left + 6, tw = tip.offsetWidth; if (x + tw > box.width) x = r.left - box.left - tw - 6; tip.style.left = x + 'px'; tip.style.setProperty('--ty', '18%');
  });
  root.addEventListener('mouseleave', function () { var tip = root.querySelector('.aiu-tip'); if (tip) tip.classList.remove('on'); });

  // ---- popup ----
  var ov = document.createElement('div'); ov.className = 'aiu-ov'; document.body.appendChild(ov);
  function close() { ov.classList.remove('on'); }
  ov.addEventListener('mousedown', function (e) { if (e.target === ov) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  function showLog(n) {
    var u = U.filter(function (x) { return x[0] === n; })[0], L = LOGS[n] || LOGS['Trịnh Đức Anh'];
    ov.innerHTML = '<div class="aiu-dr"><div class="aiu-dr-hd">' + av(n) + '<div><b>Nhật ký lượt hỏi</b><small>' + esc(u[0] + ' - ' + u[1] + ' - ' + u[2]) + ' · ' + esc(u[4]) + '</small></div><button type="button" class="aiu-ib" data-u="close" title="Đóng"><i class="ri-close-line"></i></button></div>' +
      '<div class="aiu-dr-sum"><span><b>' + fmt(u[5]) + '</b>lượt tháng này</span><span><b>' + fmt(u[6]) + '</b>bị chặn</span><span><b>' + fmt(u[5] * VPT) + ' ₫</b>chi phí</span></div>' +
      '<div class="aiu-dr-bd"><div class="aiu-day">Hôm nay</div>' + L.map(function (l) {
        return '<div class="aiu-lg"><span class="tm">' + l[0] + '</span><i class="' + (l[2] === 'ok' ? 'ri-check-line' : 'ri-lock-2-line') + '" style="color:' + C[l[2]] + '"></i><div><b>' + esc(l[1]) + '</b><small>' + (l[2] === 'ok' ? 'Đã trả lời' : 'Bị chặn — thiếu quyền "Xem nhiệm vụ toàn công ty"') + ' · ' + fmt(l[3]) + ' token · ≈ ' + fmt(Math.round(l[3] / TPT * VPT)) + ' ₫</small></div></div>';
      }).join('') + '<p class="aiu-hint">Nhật ký giữ 12 tháng. Chỉ quản trị Agent xem được; nội dung câu trả lời không lưu, chỉ lưu câu hỏi + công cụ + kết quả.</p></div></div>';
    ov.classList.add('on', 'dr');
  }
  function showQuota() {
    // 11/11 [U] "Cài đặt hạn mức sử dụng sẽ theo Chức vụ trong hồ sơ nhân viên": mức chung theo NHÓM chức vụ (working_position_groups — DB local công ty 1 có 5 nhóm, 170 chức vụ)
    // + cài riêng từng chức vụ (working_positions). Thứ tự áp: chức vụ cài riêng > nhóm chức vụ > NV chưa khai chức vụ.
    var R = [['Lãnh đạo', '', 'Tổng giám đốc, Phó tổng giám đốc…', 6], ['Quản lý', '100', 'Giám đốc / Trưởng phòng, Phó phòng, Trưởng bộ phận…', 41], ['Chuyên viên', '80', 'Chuyên viên nghiệp vụ các phòng ban', 23], ['Nhân viên', '50', 'Nhân viên nghiệp vụ: NSHC, kinh doanh, kế toán…', 88], ['Nhân viên phổ thông', '10', 'Tạp vụ, bảo vệ, chăm sóc cây cảnh…', 12]];
    var O = [['Trợ lý BGĐ', 'Nhân viên', ''], ['Trưởng phòng kinh doanh-CNV', 'Quản lý', '150'], ['Trợ lý Kinh doanh - Dự án', 'Nhân viên', '80']];
    ov.innerHTML = '<div class="aiu-md aiu-md-l"><div class="aiu-md-hd"><span class="ic"><i class="ri-settings-3-line"></i></span><div><b>Cài hạn mức TPE SMART AGENT</b><small>Công ty Tân Phát · hạn mức lấy theo Chức vụ trong hồ sơ nhân viên</small></div><button type="button" class="aiu-ib" data-u="close" title="Đóng"><i class="ri-close-line"></i></button></div><div class="aiu-md-bd">' +
      '<div class="aiu-f"><label>Ngân sách mỗi tháng (₫)<em>*</em></label><input value="3,000,000"></div>' +
      '<div class="aiu-f"><label>Gửi cảnh báo khi đạt</label><div class="aiu-inl"><input value="80" style="width:70px"><span>% ngân sách, tới</span><div class="aiu-chip">Phạm Minh Đức - BGD - 11010001<i class="ri-close-line"></i></div></div></div>' +
      '<div class="aiu-f"><label>Khi hết ngân sách</label><div class="aiu-rd"><label><input type="radio" name="aiu-x" checked> Chỉ Ban giám đốc được dùng tiếp</label><label><input type="radio" name="aiu-x"> Tạm dừng Agent với mọi người</label></div></div>' +
      '<div class="aiu-f"><label>Số câu hỏi tối đa mỗi ngày theo nhóm chức vụ</label><table class="aiu-qt aiu-qg"><thead><tr><th>Nhóm chức vụ</th><th class="text-right">Số chức vụ</th><th>Câu / ngày</th></tr></thead><tbody>' + R.map(function (r) { return '<tr><td><b>' + r[0] + '</b><small>' + r[2] + '</small></td><td class="text-right num">' + r[3] + '</td><td><input value="' + r[1] + '" placeholder="Không giới hạn"></td></tr>'; }).join('') +
        '<tr><td><b>Chưa khai chức vụ</b><small>Hồ sơ nhân viên chưa có Chức vụ</small></td><td class="text-right num">—</td><td><input value="20" placeholder="Không giới hạn"></td></tr></tbody></table></div>' +
      '<div class="aiu-f"><label>Cài riêng cho chức vụ <small class="aiu-lbs">ưu tiên hơn mức của nhóm</small></label><table class="aiu-qt aiu-qo"><thead><tr><th>Chức vụ</th><th>Nhóm</th><th>Câu / ngày</th><th></th></tr></thead><tbody>' + O.map(function (o) { return '<tr><td>' + esc(o[0]) + '</td><td>' + o[1] + '</td><td><input value="' + o[2] + '" placeholder="Không giới hạn"></td><td><button type="button" class="aiu-ib" title="Bỏ cài riêng"><i class="ri-delete-bin-6-line"></i></button></td></tr>'; }).join('') + '</tbody></table>' +
        '<button type="button" class="aiu-add"><i class="ri-add-line"></i>Thêm chức vụ</button>' +
        '<small class="aiu-hint">Để trống = không giới hạn. Đổi Chức vụ trong hồ sơ nhân viên thì hạn mức đổi theo từ ngày hôm sau. Hết lượt trong ngày, Agent báo "Bạn đã dùng hết lượt hôm nay" và không gọi AI.</small></div>' +
      '</div><div class="aiu-md-ft"><button type="button" class="v2-btn v2-btn--sm v2-btn--primary v2-btn--primary-info v2-btn--prefix-sm mr-2" data-u="save"><div class="v2-btn__prefix--sm"><i class="ri-save-line" style="font-size:13px"></i></div> Lưu</button><button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary v2-btn--tertiary-info" data-u="close">Huỷ</button></div></div>';
    ov.classList.remove('dr'); ov.classList.add('on');
  }
  function toast(m) { var t = document.querySelector('.mk-p-toast'); if (!t) { t = document.createElement('div'); t.className = 'mk-p-toast'; document.body.appendChild(t); } t.innerHTML = m; t.classList.add('on'); clearTimeout(t._t); t._t = setTimeout(function () { t.classList.remove('on'); }, 2200); }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-by],[data-log],[data-u]'); if (!b || !(root.contains(b) || ov.contains(b))) return;
    if (b.dataset.by) { by = b.dataset.by; render(); return; }
    if (b.dataset.log) return showLog(b.dataset.log);
    var u = b.dataset.u;
    if (u === 'quota') showQuota(); else if (u === 'close') close();
    else if (u === 'save') { close(); toast('<i class="ri-check-line"></i> Đã lưu hạn mức TPE SMART AGENT'); }
    else if (u === 'xls') toast('<i class="ri-file-excel-2-line"></i> Xuất Excel thống kê theo ' + (by === 'emp' ? 'nhân viên' : 'phòng ban'));
  });
  render();
})();

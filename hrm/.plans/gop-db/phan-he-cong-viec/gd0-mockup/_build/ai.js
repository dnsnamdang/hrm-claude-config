// 11/11 [U] TPE SMART AGENT (tên cũ: Trợ lý ERP) — mockup DEMO giới thiệu giải pháp cho khách hàng.
// User 11/11: "mục đích để giới thiệu giải pháp cho khách hàng nên cần ấn tượng, mượt, phản hồi chính xác ·
//              thể hiện được việc phân quyền rõ ràng ai được hỏi gì, bị chặn khi quá quyền hạn".
// Claude tự chốt (thuần trình bày, ghi lại để user soát):
//  - "Xem như" (3 vai trò) là NÚT DEMO cho buổi giới thiệu, sản phẩm thật không có — bot luôn chạy theo người đăng nhập.
//  - Mỗi câu trả lời có dòng "các bước": Người hỏi → Kiểm quyền → Tra dữ liệu. Bị chặn thì dừng ở Kiểm quyền và ghi "Không đọc dữ liệu".
//  - 3 kiểu không trả lời, tách màu: 🔒 Ngoài quyền (vàng hổ phách) · ⓘ Không hỗ trợ / dữ liệu loại trừ (xám) · ? Cần làm rõ (xanh).
//    Chữ đỏ chỉ dành cho lỗi validate (CLAUDE.md) ⇒ không dùng đỏ cho câu bị chặn; đỏ chỉ ở badge trạng thái "Quá hạn".
//  - Quá quyền thì gợi ý "Hỏi trong phạm vi của tôi" thay vì cụt.
//  - Dữ liệu demo cố định (kịch bản), câu gõ tự do được khớp theo từ khoá; ngoài kịch bản thì trả lời mình làm được gì.
(function () {
  var wrap = document.querySelector('.cx-wrap'); if (!wrap) return;
  var pane = wrap.querySelector('.dm-pane'), side = wrap.querySelector('.dm-info'), ls = document.querySelector('.dm-ls'), q = document.querySelector('.dm-q input');
  if (!pane || !ls) return;
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  function nrm(s) { return String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[đĐ]/g, 'd').toLowerCase(); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function now() { var d = new Date(); return pad(d.getHours()) + ':' + pad(d.getMinutes()); }
  var PAL = ['#f472b6', '#60a5fa', '#fbbf24', '#34d399', '#a78bfa', '#f87171', '#2dd4bf', '#fb923c', '#818cf8'];
  function avc(n) { var h = 0; for (var i = 0; i < n.length; i++) h = (h * 31 + n.charCodeAt(i)) >>> 0; return PAL[h % PAL.length]; }
  function ini(n) { var p = n.trim().split(/\s+/); return ((p[p.length - 2] ? p[p.length - 2][0] : '') + p[p.length - 1][0]).toUpperCase(); }
  function av(n, sz) { return '<span class="dm-av' + (sz ? ' ' + sz : '') + '" style="background:' + avc(n) + '">' + esc(ini(n)) + '</span>'; }
  // 11/11 [U] Linh vật TPE SMART AGENT — robot nhỏ, kính mặt là hình elip xanh #2B59A7 lấy từ logo Tân Phát ETEK (hrm-client/assets/images/logo-etek.jpg),
  // đèn ăng-ten vàng, tay cầm cờ lê (công ty làm thiết bị kỹ thuật). head(): bản đầu cho avatar · full(): bản toàn thân cho màn chào.
  var TB = '#2B59A7';
  function head() {
    return '<svg class="tpa" viewBox="0 0 64 64" aria-hidden="true"><line x1="32" y1="14" x2="32" y2="7" stroke="' + TB + '" stroke-width="3" stroke-linecap="round"/><circle class="tpa-bulb" cx="32" cy="6" r="4" fill="#FBBF24"/>' +
      '<rect x="5" y="27" width="8" height="15" rx="4" fill="' + TB + '"/><rect x="51" y="27" width="8" height="15" rx="4" fill="' + TB + '"/>' +
      '<rect x="10" y="13" width="44" height="40" rx="17" fill="#fff" stroke="' + TB + '" stroke-width="2.6"/>' +
      '<ellipse cx="32" cy="31" rx="17.5" ry="10.5" fill="' + TB + '" transform="rotate(-6 32 31)"/>' +
      '<g class="tpa-eyes"><rect x="22" y="25.5" width="6" height="9" rx="3" fill="#fff"/><rect x="36" y="24.5" width="6" height="9" rx="3" fill="#fff"/></g>' +
      '<path d="M28.5 37.2q3.8 2.8 7.6 -0.6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/>' +
      '<circle cx="17" cy="44" r="2.6" fill="#F9A8D4"/><circle cx="47" cy="44" r="2.6" fill="#F9A8D4"/></svg>';
  }
  function full() {
    return '<svg class="tpa tpa-full" viewBox="0 0 120 128" aria-hidden="true"><ellipse cx="60" cy="122" rx="26" ry="4" fill="rgba(43,89,167,.16)"/>' +
      '<rect x="45" y="102" width="11" height="13" rx="4.5" fill="' + TB + '"/><rect x="64" y="102" width="11" height="13" rx="4.5" fill="' + TB + '"/>' +
      '<g class="tpa-wave"><rect x="20" y="70" width="22" height="10" rx="5" fill="#fff" stroke="' + TB + '" stroke-width="2.4"/><circle cx="20" cy="75" r="5.5" fill="' + TB + '"/></g>' +
      '<g transform="rotate(28 100 70)"><rect x="97" y="62" width="6" height="22" rx="3" fill="#94A3B8"/><circle cx="100" cy="60" r="7" fill="#94A3B8"/><rect x="97.5" y="51" width="5" height="9" rx="1" fill="#fff"/></g>' +
      '<rect x="78" y="72" width="20" height="10" rx="5" fill="#fff" stroke="' + TB + '" stroke-width="2.4"/>' +
      '<rect x="38" y="66" width="44" height="40" rx="14" fill="#fff" stroke="' + TB + '" stroke-width="2.6"/>' +
      '<ellipse cx="60" cy="86" rx="14" ry="7" fill="' + TB + '" transform="rotate(-6 60 86)"/><text x="60" y="89" text-anchor="middle" font-family="Roboto,Arial,sans-serif" font-size="8" font-weight="700" fill="#fff" letter-spacing=".5">TPE</text>' +
      '<g transform="translate(20 0) scale(1.25)">' + head().replace(/^<svg[^>]*>/, '').replace('</svg>', '') + '</g></svg>';
  }
  var BOT = '<span class="ai-av">' + head() + '</span>';

  // ---- vai trò demo ----
  var PS = {
    nv: { n: 'Lê Thu Trang', r: 'Nhân viên hành chính tổng hợp', g: 'Nhân viên', d: 'Phòng Nhân sự Hành chính', short: 'Nhân viên',
      perms: ['Xem nhiệm vụ của tôi', 'Xem meeting của tôi'], scope: 'Việc của mình + nhóm mình tham gia' },
    tp: { n: 'Đỗ Mai Anh', r: 'Trưởng phòng Nhân sự Hành chính', g: 'Quản lý', d: 'Phòng Nhân sự Hành chính', short: 'Trưởng phòng',
      perms: ['Xem nhiệm vụ của tôi', 'Xem meeting của tôi', 'Xem nhiệm vụ của phòng', 'Xem báo cáo hiệu suất của phòng'], scope: 'Phòng Nhân sự Hành chính' },
    gd: { n: 'Phạm Minh Đức', r: 'Tổng Giám đốc', g: 'Lãnh đạo', d: 'Công ty Tân Phát', short: 'Giám đốc',
      perms: ['Xem nhiệm vụ của tôi', 'Xem meeting của tôi', 'Xem nhiệm vụ của phòng', 'Xem nhiệm vụ toàn công ty', 'Xem báo cáo hiệu suất của phòng', 'Xem báo cáo hiệu suất toàn công ty'], scope: 'Toàn công ty Tân Phát' }
  };
  var who = 'tp';
  try { var sv = sessionStorage.getItem('ai-who'); if (PS[sv]) who = sv; } catch (e) {}
  function has(p) { return PS[who].perms.indexOf(p) >= 0; }

  // ---- ma trận "ai được hỏi gì" (khớp đúng logic trả lời bên dưới) ----
  var MX = [
    ['Việc / lịch họp của tôi', { nv: 'y', tp: 'y', gd: 'y' }],
    ['Việc của đồng nghiệp cùng phòng', { nv: 'n', tp: 'y', gd: 'y' }],
    ['Việc quá hạn của phòng mình', { nv: 'n', tp: 'y', gd: 'y' }],
    ['Việc của phòng khác', { nv: 'n', tp: 'n', gd: 'y' }],
    ['Xếp hạng hoàn thành toàn công ty', { nv: 'n', tp: 'p', gd: 'y' }],
    ['Lương · giá vốn · công nợ', { nv: 'x', tp: 'x', gd: 'x' }]
  ];
  var MXI = { y: '<i class="ri-check-line ai-y" title="Được hỏi"></i>', n: '<i class="ri-lock-2-line ai-n" title="Bị chặn"></i>', p: '<span class="ai-p" title="Chỉ trong phạm vi phòng mình">phòng</span>', x: '<i class="ri-forbid-line ai-x" title="Agent không truy cập dữ liệu này với bất kỳ ai"></i>' };

  // ---- dữ liệu nhiệm vụ demo ----
  var ST = { run: ['Đang thực hiện', '#2563EB'], wait: ['Hoàn thành - Chờ duyệt', '#D97706'], late: ['Quá hạn', '#DC2626'], new: ['Chờ bắt đầu', '#64748B'], done: ['Hoàn thành', '#16A34A'], watch: ['Theo dõi', '#0EA5E9'] };
  function T(code, name, st, man, due, note) { return { c: code, n: name, s: st, m: man, due: due, note: note }; }
  var TODAY = {
    nv: [T('NV-2026-01803', 'Cập nhật hồ sơ BHXH tháng 11', 'late', 'Lê Thu Trang', '09/11', 'trễ 2 ngày'), T('NV-2026-01842', 'Dự trù kinh phí hội nghị công đoàn 2027', 'wait', 'Lê Thu Trang', 'Hôm nay 10:00', 'chờ chị Đỗ Mai Anh duyệt'), T('NV-2026-01861', 'Đặt cọc hội trường tầng 5', 'new', 'Lê Thu Trang', 'Hôm nay 17:30', '')],
    tp: [T('NV-2026-01790', 'Báo cáo nhân sự tháng 10 gửi Ban giám đốc', 'late', 'Đỗ Mai Anh', '09/11', 'trễ 2 ngày'), T('NV-2026-01842', 'Duyệt dự trù kinh phí hội nghị công đoàn 2027', 'wait', 'Lê Thu Trang', 'Hôm nay 10:00', 'bạn là người duyệt'), T('NV-2026-01857', 'Ký biên bản bàn giao tài sản', 'run', 'Đỗ Mai Anh', 'Hôm nay 17:30', '')],
    gd: [T('NV-2026-01811', 'Duyệt kế hoạch kinh doanh Q1/2027', 'wait', 'Ngô Quang Vinh', 'Hôm nay 17:30', 'bạn là người duyệt'), T('NV-2026-01866', 'Chốt ngân sách hội nghị khách hàng 2027', 'run', 'Phạm Minh Đức', '13/11', '')]
  };
  var LATE_NSHC = [T('NV-2026-01790', 'Báo cáo nhân sự tháng 10 gửi Ban giám đốc', 'late', 'Đỗ Mai Anh', '09/11', 'trễ 2 ngày'), T('NV-2026-01803', 'Cập nhật hồ sơ BHXH tháng 11', 'late', 'Lê Thu Trang', '09/11', 'trễ 2 ngày'),
    T('NV-2026-01755', 'Rà soát hợp đồng lao động hết hạn Q4', 'late', 'Phạm Quốc Huy', '04/11', 'trễ 7 ngày'), T('NV-2026-01772', 'Kiểm kê tài sản văn phòng tầng 3', 'late', 'Bùi Thanh Tâm', '07/11', 'trễ 4 ngày')];
  var LATE_CO = [['Phòng Kinh doanh 1', 7], ['Phòng Kỹ thuật công nghệ', 5], ['Phòng Nhân sự Hành chính', 4], ['Phòng Kinh doanh 2', 2], ['Phòng Kế toán', 1]];
  var LATE_KD1 = [T('NV-2026-01702', 'Gửi báo giá điều chỉnh dự án GP40', 'late', 'Trịnh Đức Anh', '06/11', 'trễ 5 ngày'), T('NV-2026-01734', 'Khảo sát lại hiện trường DA010', 'late', 'Nguyễn Thu Trang', '08/11', 'trễ 3 ngày'), T('NV-2026-01748', 'Cập nhật CRM 12 khách hàng tiềm năng', 'late', 'Trịnh Đức Anh', '10/11', 'trễ 1 ngày')];
  var MEET = {
    nv: [['Thứ Hai 16/11', '08:30', 'Giao ban Phòng Nhân sự Hành chính', 'Phòng họp 3A'], ['Thứ Năm 19/11', '14:00', 'Chạy thử chương trình hội nghị công đoàn', 'Hội trường tầng 5']],
    tp: [['Thứ Hai 16/11', '08:30', 'Giao ban Phòng Nhân sự Hành chính', 'Phòng họp 3A'], ['Thứ Ba 17/11', '15:00', 'Họp Ban giám đốc — báo cáo nhân sự tháng 10', 'Phòng họp 5B'], ['Thứ Năm 19/11', '14:00', 'Chạy thử chương trình hội nghị công đoàn', 'Hội trường tầng 5']],
    gd: [['Thứ Hai 16/11', '10:00', 'Họp giao ban Ban giám đốc', 'Phòng họp 5B'], ['Thứ Ba 17/11', '15:00', 'Họp Ban giám đốc — báo cáo nhân sự tháng 10', 'Phòng họp 5B'], ['Thứ Sáu 20/11', '09:00', 'Gặp khách hàng Gaochang — dự án DA010', 'Trực tuyến']]
  };
  var TRANG = {
    'Lê Thu Trang': { d: 'HN_NSHC - 21410210', dep: 'NSHC', list: [T('NV-2026-01842', 'Dự trù kinh phí hội nghị công đoàn 2027', 'wait', 'Lê Thu Trang', 'Hôm nay 10:00', 'đã nộp 10/11'), T('NV-2026-01803', 'Cập nhật hồ sơ BHXH tháng 11', 'late', 'Lê Thu Trang', '09/11', 'trễ 2 ngày'), T('NV-2026-01861', 'Đặt cọc hội trường tầng 5', 'new', 'Lê Thu Trang', 'Hôm nay 17:30', '')] },
    'Nguyễn Thu Trang': { d: 'HN_KD1 - 21410577', dep: 'KD1', list: [T('NV-2026-01734', 'Khảo sát lại hiện trường DA010', 'late', 'Nguyễn Thu Trang', '08/11', 'trễ 3 ngày'), T('NV-2026-01759', 'Hồ sơ thầu gói 3 — dự án Gaochang', 'run', 'Nguyễn Thu Trang', '18/11', '60% checklist')] }
  };
  var RANK_CO = [['Phạm Văn Tú', 'Phòng Quản trị thông tin', 31, 97], ['Lâm Thị Ngọc', 'Phòng Kinh doanh 1 (HCM)', 28, 96], ['Nguyễn Thị Hằng', 'Phòng Nhân sự Hành chính', 26, 96], ['Đặng Minh Khoa', 'Phòng Kỹ thuật công nghệ', 24, 92], ['Ngô Quang Vinh', 'Phòng Kinh doanh 2', 22, 91]];
  var RANK_NSHC = [['Nguyễn Thị Hằng', 'Phòng Nhân sự Hành chính', 26, 96], ['Trần Văn Minh', 'Phòng Nhân sự Hành chính', 21, 90], ['Vũ Hoàng Long', 'Phòng Nhân sự Hành chính', 18, 89], ['Lê Thu Trang', 'Phòng Nhân sự Hành chính', 17, 82]];

  // ---- câu hỏi gợi ý ----
  var SUG = [
    ['today', 'ri-calendar-todo-line', 'Hôm nay tôi có việc gì cần làm?'],
    ['late', 'ri-alarm-warning-line', 'Phòng mình đang có việc nào quá hạn?'],
    ['meet', 'ri-team-line', 'Tuần sau tôi có những cuộc họp nào?'],
    ['trang', 'ri-user-search-line', 'Việc của chị Trang đang tới đâu rồi?'],
    ['kd1', 'ri-building-line', 'Phòng Kinh doanh 1 tuần này trễ bao nhiêu việc?'],
    ['rank', 'ri-trophy-line', 'Ai hoàn thành việc đúng hạn tốt nhất tháng 10 toàn công ty?'],
    ['salary', 'ri-money-dollar-circle-line', 'Lương tháng 10 của anh Trần Văn Minh là bao nhiêu?']
  ];
  function match(t) {
    var k = nrm(t);
    if (/luong|thu nhap|gia von|cong no/.test(k)) return 'salary';
    if (/trang/.test(k)) return 'trang';
    if (/xep hang|tot nhat|dung han nhat|hieu suat/.test(k)) return 'rank';
    if (/kinh doanh|kd1|kd 1|phong khac/.test(k)) return 'kd1';
    if (/qua han|tre han|cham|tre /.test(k + ' ')) return 'late';
    if (/hop|meeting|lich/.test(k)) return 'meet';
    if (/hom nay|viec gi|can lam|viec cua toi/.test(k)) return 'today';
    return null;
  }

  // ---- hội thoại ----
  var LOG = [], busy = false, open = false, panel = true, convo = [];

  function rowsHtml(list, opt) {
    opt = opt || {};
    return '<div class="ai-tasks">' + list.map(function (t, i) {
      var s = ST[t.s];
      return '<a class="ai-task" style="--d:' + (i * 70) + 'ms" title="Mở nhiệm vụ ' + esc(t.c) + '"><i class="ri-task-line ai-ti"></i><div class="ai-tt"><b>' + esc(t.n) + '</b><small>' + esc(t.c) + (opt.man !== false ? ' · ' + esc(t.m) : '') + ' · Hạn ' + esc(t.due) + (t.note ? ' · ' + esc(t.note) : '') + '</small></div><span class="mk-badge" style="--c:' + s[1] + '">' + esc(s[0]) + '</span><i class="ri-arrow-right-s-line ai-go"></i></a>';
    }).join('') + '</div>';
  }
  function barsHtml(list, unit) {
    var mx = Math.max.apply(null, list.map(function (x) { return x[1]; }));
    return '<div class="ai-bars">' + list.map(function (x, i) {
      return '<div class="ai-bar" style="--d:' + (i * 80) + 'ms"><span class="l">' + esc(x[0]) + '</span><span class="tr"><i style="--w:' + Math.round(x[1] / mx * 100) + '%"></i></span><b>' + x[1] + '</b><small>' + unit + '</small></div>';
    }).join('') + '</div>';
  }
  function rankHtml(list) {
    return '<div class="ai-rank">' + list.map(function (x, i) {
      return '<div class="ai-rk" style="--d:' + (i * 80) + 'ms"><span class="no n' + (i + 1) + '">' + (i + 1) + '</span>' + av(x[0], 's') + '<div class="tx"><b>' + esc(x[0]) + '</b><small>' + esc(x[1]) + '</small></div><div class="num"><b>' + x[3] + '%</b><small>' + x[2] + ' việc đúng hạn</small></div></div>';
    }).join('') + '</div>';
  }
  function meetHtml(list) {
    return '<div class="ai-meets">' + list.map(function (m, i) {
      var d = m[0].split(' '); return '<div class="ai-mt" style="--d:' + (i * 70) + 'ms"><div class="dt"><small>' + esc(d.slice(0, 2).join(' ')) + '</small><b>' + esc(d[2]) + '</b></div><div class="tx"><b>' + esc(m[2]) + '</b><small><i class="ri-time-line"></i>' + esc(m[1]) + ' · <i class="ri-map-pin-line"></i>' + esc(m[3]) + '</small></div></div>';
    }).join('') + '</div>';
  }

  // Mỗi câu trả lời: { steps:[[kiểu, tên, chi tiết]], kind:'ok'|'deny'|'na'|'ask', text, html, src, fu:[gợi ý tiếp] }
  function stepWho() { var p = PS[who]; return ['ok', 'Người hỏi', p.n + ' · ' + p.r + ' · ' + p.d]; }
  function deny(need, scopeMsg, alt) {
    return { kind: 'deny', steps: [stepWho(), ['no', 'Kiểm quyền', 'thiếu quyền "' + need + '"'], ['skip', 'Tra dữ liệu', 'không thực hiện — không đọc bản ghi nào']],
      need: need, scopeMsg: scopeMsg, alt: alt };
  }
  function answer(key, arg) {
    var p = PS[who];
    if (key === 'today') {
      var L = TODAY[who], late = L.filter(function (t) { return t.s === 'late'; }).length;
      return { kind: 'ok', steps: [stepWho(), ['ok', 'Kiểm quyền', 'Xem nhiệm vụ của tôi ✓'], ['tool', 'Tra nhiệm vụ của tôi', 'hạn đến hết hôm nay + đang quá hạn · ' + L.length + ' kết quả · 0,28 giây']],
        text: 'Hôm nay (Thứ Tư 11/11) bạn có **' + L.length + ' việc** cần xử lý' + (late ? ', trong đó **' + late + ' việc đã quá hạn** — nên làm việc này trước.' : '.'),
        html: rowsHtml(L), src: 'Nhiệm vụ · phạm vi: việc của ' + p.n, fu: ['late', 'meet'] };
    }
    if (key === 'late') {
      if (who === 'nv') return deny('Xem nhiệm vụ của phòng', 'Bạn chỉ xem được việc của mình và các nhóm bạn tham gia.', ['today', 'Xem việc quá hạn của tôi']);
      if (who === 'gd') return { kind: 'ok', steps: [stepWho(), ['ok', 'Kiểm quyền', 'Xem nhiệm vụ toàn công ty ✓'], ['tool', 'Thống kê việc quá hạn theo phòng', 'toàn công ty Tân Phát · 19 việc · 0,41 giây']],
        text: 'Toàn công ty đang có **19 việc quá hạn**. **Phòng Kinh doanh 1** nhiều nhất (7 việc), chủ yếu là báo giá và khảo sát dự án.', html: barsHtml(LATE_CO, 'việc'), src: 'Nhiệm vụ · phạm vi: toàn công ty Tân Phát', fu: ['kd1', 'rank'] };
      return { kind: 'ok', steps: [stepWho(), ['ok', 'Kiểm quyền', 'Xem nhiệm vụ của phòng ✓'], ['tool', 'Tra nhiệm vụ quá hạn', 'Phòng Nhân sự Hành chính · 4 kết quả · 0,31 giây']],
        text: 'Phòng Nhân sự Hành chính có **4 việc quá hạn**. Trễ lâu nhất là **Rà soát hợp đồng lao động hết hạn Q4** của anh Phạm Quốc Huy (7 ngày).', html: rowsHtml(LATE_NSHC), src: 'Nhiệm vụ · phạm vi: Phòng Nhân sự Hành chính', fu: ['trang', 'kd1'] };
    }
    if (key === 'kd1') {
      if (who === 'nv') return deny('Xem nhiệm vụ toàn công ty', 'Bạn chỉ xem được việc của mình và các nhóm bạn tham gia.', ['today', 'Xem việc của tôi']);
      if (who === 'tp') return deny('Xem nhiệm vụ toàn công ty', 'Quyền của bạn giới hạn trong Phòng Nhân sự Hành chính — Phòng Kinh doanh 1 nằm ngoài phạm vi.', ['late', 'Xem việc quá hạn của phòng tôi']);
      return { kind: 'ok', steps: [stepWho(), ['ok', 'Kiểm quyền', 'Xem nhiệm vụ toàn công ty ✓'], ['ok', 'Xác định phòng', '"Kinh doanh 1" → Phòng Kinh doanh 1 (HN_KD1)'], ['tool', 'Tra nhiệm vụ quá hạn', 'HN_KD1 · tuần 09–15/11 · 7 kết quả · 0,36 giây']],
        text: 'Tuần này Phòng Kinh doanh 1 có **7 việc trễ hạn**, tập trung ở **2 người**: anh Trịnh Đức Anh (4 việc) và chị Nguyễn Thu Trang (3 việc). 3 việc trễ lâu nhất:', html: rowsHtml(LATE_KD1), src: 'Nhiệm vụ · phạm vi: Phòng Kinh doanh 1', fu: ['rank'] };
    }
    if (key === 'meet') {
      var M = MEET[who];
      return { kind: 'ok', steps: [stepWho(), ['ok', 'Kiểm quyền', 'Xem meeting của tôi ✓'], ['ok', 'Hiểu thời gian', '"tuần sau" → 16/11 – 20/11/2026'], ['tool', 'Tra lịch meeting', M.length + ' cuộc họp · 0,22 giây']],
        text: 'Tuần sau (16 – 20/11) bạn có **' + M.length + ' cuộc họp**:', html: meetHtml(M), src: 'Meeting · phạm vi: lịch của ' + p.n, fu: ['today'] };
    }
    if (key === 'trang') {
      if (!arg) return { kind: 'ask', steps: [stepWho(), ['tool', 'Tìm nhân viên', '"Trang" → 2 người trùng tên']],
        text: 'Có **2 người tên Trang**. Bạn hỏi ai?', pick: Object.keys(TRANG) };
      var tr = TRANG[arg], self = arg === p.n;
      if (!self && who === 'nv') return deny('Xem nhiệm vụ của phòng', 'Bạn không xem được việc của đồng nghiệp, trừ việc trong nhóm bạn cùng tham gia.', ['today', 'Xem việc của tôi']);
      if (!self && who === 'tp' && tr.dep !== 'NSHC') return deny('Xem nhiệm vụ toàn công ty', 'Chị Nguyễn Thu Trang thuộc Phòng Kinh doanh 1 — ngoài phạm vi Phòng Nhân sự Hành chính của bạn.', ['trang:Lê Thu Trang', 'Hỏi về Lê Thu Trang (cùng phòng)']);
      var need = self ? 'Xem nhiệm vụ của tôi' : (tr.dep === 'NSHC' && who === 'tp' ? 'Xem nhiệm vụ của phòng' : 'Xem nhiệm vụ toàn công ty');
      return { kind: 'ok', steps: [stepWho(), ['ok', 'Xác định người', arg + ' · ' + tr.d], ['ok', 'Kiểm quyền', need + ' ✓'], ['tool', 'Tra nhiệm vụ đang mở', tr.list.length + ' kết quả · 0,27 giây']],
        text: (self ? 'Đó là bạn 🙂. Bạn' : (arg.split(' ').pop() === 'Trang' ? 'Chị ' + arg : arg)) + ' đang có **' + tr.list.length + ' việc chưa xong**' + (tr.list.some(function (t) { return t.s === 'late'; }) ? ', **1 việc đã quá hạn**.' : '.'),
        html: rowsHtml(tr.list, { man: false }), src: 'Nhiệm vụ · phạm vi: việc của ' + arg, fu: ['late'] };
    }
    if (key === 'rank') {
      if (who === 'nv') return deny('Xem báo cáo hiệu suất toàn công ty', 'Báo cáo hiệu suất chỉ mở cho quản lý.', ['today', 'Xem việc của tôi']);
      if (who === 'tp' && arg !== 'scope') return deny('Xem báo cáo hiệu suất toàn công ty', 'Bạn có quyền xem báo cáo hiệu suất trong Phòng Nhân sự Hành chính.', ['rank:scope', 'Xếp hạng trong phòng tôi']);
      var L2 = who === 'gd' ? RANK_CO : RANK_NSHC, sc = who === 'gd' ? 'toàn công ty Tân Phát' : 'Phòng Nhân sự Hành chính';
      return { kind: 'ok', steps: [stepWho(), ['ok', 'Kiểm quyền', (who === 'gd' ? 'Xem báo cáo hiệu suất toàn công ty' : 'Xem báo cáo hiệu suất của phòng') + ' ✓'], ['ok', 'Hiểu thời gian', '"tháng 10" → 01/10 – 31/10/2026'], ['tool', 'Báo cáo hoàn thành đúng hạn', sc + ' · ' + (who === 'gd' ? '214' : '18') + ' nhân viên · 0,52 giây']],
        text: 'Tháng 10, ' + (who === 'gd' ? '' : 'trong Phòng Nhân sự Hành chính, ') + '**' + L2[0][0] + '** dẫn đầu với tỉ lệ đúng hạn **' + L2[0][3] + '%** (' + L2[0][2] + ' việc). Xếp hạng theo tỉ lệ hoàn thành đúng hạn, chỉ tính người có từ 10 việc:',
        html: rankHtml(L2), src: 'Báo cáo hiệu suất · phạm vi: ' + sc, fu: who === 'gd' ? ['late'] : ['late'] };
    }
    if (key === 'salary') return { kind: 'na', steps: [stepWho(), ['no', 'Phạm vi Agent', 'dữ liệu lương nằm trong danh sách loại trừ'], ['skip', 'Tra dữ liệu', 'không thực hiện']],
      text: 'TPE SMART AGENT **không truy cập dữ liệu lương** — công ty đã loại dữ liệu lương, giá vốn, công nợ khỏi Agent cho **mọi vai trò**, kể cả Ban giám đốc. Bạn xem lương ở màn **Tính lương** như thường lệ.', src: 'Cấu hình Agent lý · danh sách dữ liệu loại trừ', fu: ['today'] };
    return { kind: 'na', steps: [stepWho(), ['skip', 'Chọn công cụ', 'không có công cụ phù hợp']],
      text: 'Bản thử nghiệm hiện trả lời được về **nhiệm vụ, lịch họp và tiến độ** trong phân hệ Công việc. Bạn thử một trong các câu dưới đây nhé.', fu: ['today', 'late', 'meet'] };
  }
  // 11/11 [U] đếm token theo lượt: demo giả định Sonnet 5.5 ($2 vào · $10 ra · cache đọc $0.20 / 1 triệu token), tỉ giá 26,000 ₫/USD — bản thật lấy từ bảng giá cấu hình.
  var PRICE = { inp: 2, cr: 0.2, out: 10, fx: 26000 };
  var QUOTA = { nv: [12, 50], tp: [23, 100], gd: [8, 0] }, SPENT = { nv: 3120, tp: 6480, gd: 2210 };
  function fmt(n) { return Number(n).toLocaleString('en-US'); }
  function usage(A) {
    var tools = A.steps.filter(function (x) { return x[0] === 'tool'; }).length, calls = A.kind === 'na' || A.kind === 'deny' ? (A.kind === 'deny' ? 2 : 1) : tools + 1;
    var cr = 8000 * calls, inp = 520 + 380 * tools + (A.kind === 'deny' ? 140 : 0), rows = (A.html || '').split('class="ai-').length - 1;
    var out = Math.round(140 + (A.text || '').length * 0.6 + rows * 9);
    var vnd = Math.round((inp * PRICE.inp + cr * PRICE.cr + out * PRICE.out) / 1e6 * PRICE.fx);
    return { calls: calls, cr: cr, inp: inp, out: out, tot: cr + inp + out, vnd: vnd, sec: (0.7 + calls * 0.45).toFixed(1) };
  }
  function useHtml(u) { return '<div class="ai-use" title="Token vào ' + fmt(u.inp) + ' · đọc từ cache ' + fmt(u.cr) + ' · token ra ' + fmt(u.out) + '"><i class="ri-flashlight-line"></i>' + fmt(u.tot) + ' token<span>·</span>' + fmt(u.cr) + ' đọc từ cache<span>·</span>' + u.calls + ' lần gọi<span>·</span>' + u.sec + ' giây<span>·</span><b>≈ ' + fmt(u.vnd) + ' ₫</b></div>'; }
  function md(s) { return esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>'); }

  // ---- giao diện ----
  function hdHtml() {
    var p = PS[who];
    return '<div class="dm-hd ai-hd">' + BOT + '<div class="dm-hd-t"><b>TPE SMART AGENT <span class="ai-tag">AI</span></b><small><i></i>Trả lời theo quyền của người hỏi</small></div>' +
      '<div class="r"><div class="ai-who" title="Nút dành cho buổi giới thiệu — sản phẩm thật luôn chạy theo người đăng nhập"><span class="lb">Xem như</span>' +
      Object.keys(PS).map(function (k) { return '<button type="button" data-ai-who="' + k + '" class="' + (k === who ? 'on' : '') + '">' + av(PS[k].n, 'xs') + PS[k].short + '</button>'; }).join('') + '</div>' +
      '<button class="dm-ib' + (panel ? ' on' : '') + '" data-ai-panel="1" title="Phân quyền của Agent"><i class="ri-shield-user-line"></i></button></div></div>';
  }
  function helloHtml() {
    var p = PS[who];
    return '<div class="ai-hello">' + '<div class="ai-orb">' + full() + '</div><h3>Xin chào ' + esc(p.n.split(' ').slice(-2).join(' ')) + ', mình là <span class="ai-name">TPE SMART AGENT</span></h3><div class="ai-slogan">Hội tụ tinh hoa - Tiên phong giải pháp</div>' +
      '<p>Hỏi mình bằng tiếng Việt về nhiệm vụ, lịch họp, tiến độ. Mình trả lời <b>trong đúng phạm vi quyền của bạn</b> — ' + esc(p.r.toLowerCase()) + ', ' + esc(p.scope) + '.</p>' +
      '<div class="ai-sug">' + SUG.map(function (s, i) { return '<button type="button" data-ai-q="' + s[0] + '" style="--d:' + (i * 50) + 'ms"><i class="' + s[1] + '"></i>' + esc(s[2]) + '</button>'; }).join('') + '</div></div>';
  }
  function build() {
    pane.innerHTML = hdHtml() + '<div class="dm-body ai-body"></div>' +
      '<div class="dm-comp ai-comp"><div class="dm-inrow"><textarea rows="1" placeholder="Hỏi TPE SMART AGENT về nhiệm vụ, lịch họp, tiến độ…  (Enter để gửi)"></textarea></div>' +
      '<div class="dm-tb"><div class="ic ai-chips"></div>' +
      '<button type="button" class="v2-btn v2-btn--sm v2-btn--primary v2-btn--primary-info v2-btn--prefix-sm" data-ai-send="1"><div class="v2-btn__prefix--sm"><i class="ri-send-plane-2-line" style="margin-right:3px"></i></div> Gửi</button></div></div>';
    var body = pane.querySelector('.ai-body');
    if (!convo.length) body.innerHTML = helloHtml(); else convo.forEach(function (h) { body.insertAdjacentHTML('beforeend', h); });
    chips(); body.scrollTop = body.scrollHeight;
    var ta = pane.querySelector('textarea');
    ta.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); e.stopPropagation(); ask(ta.value); } });
    ta.addEventListener('input', function (e) { e.stopPropagation(); ta.style.height = 'auto'; ta.style.height = Math.min(120, ta.scrollHeight) + 'px'; });
  }
  function chips(keys) {
    var c = pane.querySelector('.ai-chips'); if (!c) return;
    keys = (keys || ['today', 'late']).slice(0, 2);
    c.innerHTML = '<span class="ai-chl">Gợi ý</span>' + keys.map(function (k) { var s = SUG.filter(function (x) { return x[0] === k; })[0]; return s ? '<button type="button" data-ai-q="' + k + '"><i class="' + s[1] + '"></i><span>' + esc(s[2]) + '</span></button>' : ''; }).join('');
  }
  function sideHtml() {
    var p = PS[who];
    var log = LOG.slice(-6).reverse();
    return '<div class="dm-info-hd">Phân quyền của Agent</div><div class="dm-info-sc ai-side">' +
      '<div class="ai-me">' + av(p.n, 'm') + '<div><b>' + esc(p.n) + '</b><small>' + esc(p.r + ' · ' + p.d) + '</small></div></div>' +
      '<div class="ai-note"><i class="ri-shield-check-line"></i><span>Agent dùng <b>đúng quyền của người đang hỏi</b>. Không có tài khoản Agent riêng, không có quyền vượt cấp. Thiếu quyền ⇒ dừng trước khi đọc dữ liệu.</span></div>' +
      (function () { var Q = QUOTA[who], pct = Q[1] ? Math.round(Q[0] / Q[1] * 100) : 0; return '<div class="ai-quota"><div class="h"><span>Hôm nay đã hỏi</span><b>' + Q[0] + (Q[1] ? ' / ' + Q[1] + ' câu' : ' câu · không giới hạn') + '</b></div>' + (Q[1] ? '<div class="bar"><i style="width:' + pct + '%"></i></div>' : '') + '<div class="f"><span>Chi phí hôm nay của bạn</span><b>≈ ' + fmt(SPENT[who]) + ' ₫</b></div><div class="src"><i class="ri-id-card-line"></i>Hạn mức theo chức vụ <b>' + esc(PS[who].r) + '</b> (nhóm ' + esc(PS[who].g) + ')</div></div>'; })() +
      '<div class="ai-sec">Quyền đang có <small>' + p.perms.length + '</small></div><div class="ai-perms">' + p.perms.map(function (x) { return '<span><i class="ri-check-line"></i>' + esc(x) + '</span>'; }).join('') + '</div>' +
      '<div class="ai-sec">Ai được hỏi gì</div><table class="ai-mx"><thead><tr><th></th>' + Object.keys(PS).map(function (k) { return '<th class="' + (k === who ? 'cur' : '') + '">' + PS[k].short + '</th>'; }).join('') + '</tr></thead><tbody>' +
      MX.map(function (r) { return '<tr><td>' + esc(r[0]) + '</td>' + Object.keys(PS).map(function (k) { return '<td class="' + (k === who ? 'cur' : '') + '">' + MXI[r[1][k]] + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table>' +
      '<div class="ai-leg"><span>' + MXI.y + 'được hỏi</span><span>' + MXI.n + 'bị chặn</span><span>' + MXI.p + 'trong phòng</span><span>' + MXI.x + 'loại trừ</span></div>' +
      '<div class="ai-sec">Nhật ký lượt hỏi <small>' + LOG.length + '</small></div>' +
      (log.length ? '<div class="ai-log">' + log.map(function (l) { return '<div class="ai-lg ' + l.k + '"><i class="' + (l.k === 'ok' ? 'ri-check-line' : l.k === 'deny' ? 'ri-lock-2-line' : l.k === 'ask' ? 'ri-question-line' : 'ri-information-line') + '"></i><div><b>' + esc(l.q) + '</b><small>' + esc(l.t + ' · ' + l.w + ' · ' + l.r) + '</small><small class="tk">' + fmt(l.u.tot) + ' token · ≈ ' + fmt(l.u.vnd) + ' ₫</small></div></div>'; }).join('') + '</div>'
        : '<div class="dm-none">Chưa có lượt hỏi. Mọi lượt hỏi đều được ghi lại: ai hỏi, công cụ nào, kết quả, token, chi phí.</div>') + '<a class="ai-stat" href="34-thong-ke-tro-ly.html"><i class="ri-bar-chart-box-line"></i>Thống kê sử dụng<small>quản trị</small><i class="ri-arrow-right-s-line"></i></a></div>';
  }
  function renderSide() { if (side && open) side.innerHTML = sideHtml(); wrap.classList.toggle('dm-info-on', open && panel); }

  function push(html) { convo.push(html); var b = pane.querySelector('.ai-body'); var hello = b.querySelector('.ai-hello'); if (hello) hello.remove(); b.insertAdjacentHTML('beforeend', html); b.scrollTo({ top: b.scrollHeight, behavior: RM ? 'auto' : 'smooth' }); return b.lastElementChild; }
  function userMsg(t) {
    return '<div class="dm-row me first ai-in"><div class="dm-m"><div class="bb">' + esc(t) + '<span class="tm">' + now() + '</span></div></div></div>';
  }
  function ask(text, key, arg) {
    if (busy) return; var t = String(text || '').trim(); if (!t) return;
    var ta = pane.querySelector('textarea'); if (ta) { ta.value = ''; ta.style.height = ''; }
    key = key || match(t); busy = true;
    push(userMsg(t));
    var A = answer(key, arg);
    var el = push('<div class="ai-row ai-in">' + BOT + '<div class="ai-card"><div class="ai-steps"></div><div class="ai-think"><span class="dots"><i></i><i></i><i></i></span>Đang kiểm quyền và tra dữ liệu…</div></div></div>');
    var stEl = el.querySelector('.ai-steps'), card = el.querySelector('.ai-card'), i = 0, gap = RM ? 0 : 420;
    (function nextStep() {
      if (i < A.steps.length) {
        var s = A.steps[i++];
        stEl.insertAdjacentHTML('beforeend', '<div class="ai-st ' + s[0] + '"><i class="' + (s[0] === 'ok' ? 'ri-checkbox-circle-fill' : s[0] === 'tool' ? 'ri-database-2-fill' : s[0] === 'no' ? 'ri-lock-2-fill' : 'ri-subtract-line') + '"></i><b>' + esc(s[1]) + '</b><span>' + esc(s[2]) + '</span></div>');
        scrollEnd(); return setTimeout(nextStep, gap);
      }
      card.querySelector('.ai-think').remove(); stEl.classList.add('done');
      stEl.insertAdjacentHTML('afterbegin', '<button type="button" class="ai-st-tg" data-ai-steps="1"><i class="ri-route-line"></i>' + A.steps.length + ' bước · ' + (A.kind === 'deny' ? 'dừng ở Kiểm quyền' : A.kind === 'na' ? 'không tra dữ liệu' : (A.steps.filter(function (x) { return x[0] === 'tool'; }).length) + ' lần tra dữ liệu') + '<i class="ri-arrow-down-s-line"></i></button>');
      var out = document.createElement('div'); out.className = 'ai-out ' + A.kind; card.appendChild(out);
      if (A.kind === 'deny') {
        out.innerHTML = '<div class="ai-deny"><div class="ic"><i class="ri-lock-2-line"></i></div><div><b>Câu hỏi này vượt quá quyền của bạn</b><p>' + esc(A.scopeMsg) + '</p>' +
          '<div class="ai-need"><span>Cần quyền</span><code>' + esc(A.need) + '</code></div><div class="ai-safe"><i class="ri-shield-check-line"></i>Agent chưa đọc bất kỳ dữ liệu nào cho câu hỏi này.</div></div></div>' +
          '<div class="ai-fu">' + (A.alt ? '<button type="button" data-ai-q="' + esc(A.alt[0]) + '" class="pri"><i class="ri-arrow-right-line"></i>' + esc(A.alt[1]) + '</button>' : '') + '<button type="button" data-ai-req="1"><i class="ri-key-2-line"></i>Đề nghị cấp quyền</button></div>';
        finish(A, t); return;
      }
      var tx = document.createElement('div'); tx.className = 'ai-tx'; out.appendChild(tx);
      stream(tx, A.text, function () {
        if (A.pick) {
          out.insertAdjacentHTML('beforeend', '<div class="ai-pick">' + A.pick.map(function (n, j) { var tr = TRANG[n]; return '<button type="button" data-ai-pick="' + esc(n) + '" style="--d:' + (j * 70) + 'ms">' + av(n, 's') + '<span><b>' + esc(n) + '</b><small>' + esc(n + ' - ' + tr.d) + '</small></span><i class="ri-arrow-right-s-line"></i></button>'; }).join('') + '</div>');
        }
        if (A.html) out.insertAdjacentHTML('beforeend', A.html);
        if (A.src) out.insertAdjacentHTML('beforeend', '<div class="ai-src"><i class="ri-database-2-line"></i>Nguồn: ' + esc(A.src) + ' · dữ liệu lúc ' + now() + '</div>');
        if (A.fu && A.fu.length && A.kind !== 'ask') out.insertAdjacentHTML('beforeend', '<div class="ai-fu">' + A.fu.map(function (k) { var s = SUG.filter(function (x) { return x[0] === k; })[0]; return '<button type="button" data-ai-q="' + k + '"><i class="' + s[1] + '"></i>' + esc(s[2]) + '</button>'; }).join('') + '</div>');
        finish(A, t);
      });
    })();
  }
  function finish(A, t) {
    busy = false; var U = usage(A), outs = pane.querySelectorAll('.ai-out'); if (outs.length) outs[outs.length - 1].insertAdjacentHTML('beforeend', useHtml(U)); scrollEnd();
    QUOTA[who][0]++; SPENT[who] += U.vnd;
    var b = pane.querySelector('.ai-body'); convo[convo.length - 1] = b.lastElementChild.outerHTML.replace(' ai-in', '');
    LOG.push({ q: t, k: A.kind, t: now(), w: PS[who].short, u: U, r: A.kind === 'ok' ? 'đã trả lời' : A.kind === 'deny' ? 'chặn — thiếu "' + A.need + '"' : A.kind === 'ask' ? 'hỏi lại' : 'không hỗ trợ' });
    renderSide(); chips(A.fu && A.fu.length ? A.fu.concat(['kd1']).filter(function (v, i, a) { return a.indexOf(v) === i; }).slice(0, 3) : null);
  }
  function stream(el, text, done) {
    var words = text.split(/(\s+)/), i = 0;
    if (RM) { el.innerHTML = md(text); return done(); }
    el.classList.add('typing');
    (function tick() {
      i = Math.min(words.length, i + 2); el.innerHTML = md(words.slice(0, i).join('')) + '<span class="ai-caret"></span>';
      if (i < words.length) { scrollEnd(); return setTimeout(tick, 28); }
      el.classList.remove('typing'); el.innerHTML = md(text); setTimeout(done, 120);
    })();
  }
  function scrollEnd() { var b = pane.querySelector('.ai-body'); if (b) b.scrollTop = b.scrollHeight; }

  function setWho(k) {
    if (k === who || busy) return; who = k; try { sessionStorage.setItem('ai-who', k); } catch (e) {}
    pane.querySelector('.ai-hd').outerHTML = hdHtml();
    if (convo.length) push('<div class="ai-swap"><span>' + av(PS[k].n, 'xs') + 'Đang hỏi với tư cách <b>' + esc(PS[k].n) + '</b> · ' + esc(PS[k].r + ', ' + PS[k].scope) + '</span></div>');
    else pane.querySelector('.ai-body').innerHTML = helloHtml();
    renderSide();
  }

  // ---- mở / đóng ----
  function itemHtml() {
    var last = LOG.length ? LOG[LOG.length - 1].q : 'Hỏi về nhiệm vụ, lịch họp, tiến độ…';
    return '<div class="dm-it ai-it' + (open ? ' on' : '') + '" data-ai-open="1">' + BOT.replace('ai-av', 'ai-av l') + '<div class="dm-tx"><div class="dm-nm"><span>TPE SMART AGENT</span><span class="ai-tag">AI</span><em>' + (LOG.length ? LOG[LOG.length - 1].t : '') + '</em></div><div class="dm-last"><span>' + esc(last) + '</span></div></div></div>';
  }
  function inject() {
    var old = ls.querySelector('[data-ai-open]'); if (old) old.remove(); var ff = document.querySelector('.dm-flt .on'); if ((q && q.value.trim()) || (ff && ff.getAttribute('data-f') !== 'all')) return;
    var pz = ls.querySelector('.dm-pinz'), h = itemHtml();
    if (pz) { var sec = pz.querySelector('.dm-sec'); sec ? sec.insertAdjacentHTML('afterend', h) : pz.insertAdjacentHTML('afterbegin', h); var sm = sec && sec.querySelector('small'); if (sm && !sm.dataset.ai) { sm.textContent = (+sm.textContent || 0) + 1; sm.dataset.ai = 1; } }
    else ls.insertAdjacentHTML('afterbegin', h);
    if (open) ls.querySelectorAll('.dm-it.on:not([data-ai-open])').forEach(function (x) { x.classList.remove('on'); });
  }
  var mo = new MutationObserver(function () { if (!ls.querySelector('[data-ai-open]')) { mo.disconnect(); inject(); mo.observe(ls, { childList: true }); } });
  mo.observe(ls, { childList: true });
  function openAI() {
    open = true; wrap.classList.add('dm-on', 'ai-on'); build(); renderSide(); mo.disconnect(); inject(); mo.observe(ls, { childList: true });
    var ta = pane.querySelector('textarea'); if (ta) ta.focus();
  }
  ls.addEventListener('click', function (e) {
    if (e.target.closest('[data-ai-open]')) { e.stopPropagation(); if (!open) openAI(); return; }
    if (e.target.closest('.dm-it') && !e.target.closest('.dm-more')) { open = false; wrap.classList.remove('ai-on'); wrap.classList.remove('dm-info-on'); }
  }, true);

  pane.addEventListener('click', function (e) {
    if (!open) return;
    var t = e.target.closest('[data-ai-q],[data-ai-pick],[data-ai-who],[data-ai-panel],[data-ai-send],[data-ai-steps],[data-ai-req]'); if (!t) return;
    e.stopPropagation();
    if (t.dataset.aiWho) return setWho(t.dataset.aiWho);
    if (t.dataset.aiPanel) { panel = !panel; t.classList.toggle('on', panel); renderSide(); return; }
    if (t.dataset.aiSend) return ask(pane.querySelector('textarea').value);
    if (t.dataset.aiSteps) { t.parentElement.classList.toggle('open'); return; }
    if (t.dataset.aiReq) { var tt = document.querySelector('.mk-p-toast'); if (!tt) { tt = document.createElement('div'); tt.className = 'mk-p-toast'; document.body.appendChild(tt); } tt.innerHTML = '<i class="ri-key-2-line"></i> Mở form đề nghị cấp quyền gửi quản lý trực tiếp — làm ở giai đoạn sau'; tt.classList.add('on'); clearTimeout(tt._t); tt._t = setTimeout(function () { tt.classList.remove('on'); }, 2400); return; }
    if (t.dataset.aiPick) return ask(t.dataset.aiPick, 'trang', t.dataset.aiPick);
    var v = t.dataset.aiQ, k = v.split(':')[0], arg = v.split(':')[1];
    var s = SUG.filter(function (x) { return x[0] === k; })[0];
    var label = arg === 'scope' ? 'Xếp hạng hoàn thành đúng hạn tháng 10 trong phòng tôi' : arg ? 'Việc của ' + arg + ' đang tới đâu rồi?' : (t.textContent.trim() && t.closest('.ai-deny, .ai-fu') && !s ? t.textContent.trim() : (s ? s[2] : t.textContent.trim()));
    if (t.closest('.ai-fu') && t.classList.contains('pri') && !arg) label = t.textContent.trim();
    ask(label, k, arg);
  }, true);

  if (window.__AI_OPEN) setTimeout(openAI, 0);
})();

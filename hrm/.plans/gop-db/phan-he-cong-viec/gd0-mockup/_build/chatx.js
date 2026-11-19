// Chat Trao đổi — bản demo tương tác (GĐ0 mockup, phân hệ Công việc). Thay khối .mk-chat-wrap tĩnh.
// Demo được: @nhắc tên · # chèn nhiệm vụ/vấn đề (thành thẻ) · đính kèm (chọn / kéo thả / dán ảnh) · trả lời · cảm xúc ·
// ghim · sửa / thu hồi · tìm trong chat · tạo nhanh nhiệm vụ / vấn đề từ tin nhắn hoặc từ ô soạn ·
// nút hành động trên thẻ theo vai trò (Bắt đầu / Báo kết quả / Duyệt / Từ chối / Nhận xử lý / Báo đã xử lý / Đóng / Mở lại)
// → tin hệ thống tự báo vào nhóm theo cấu hình "Tự báo vào nhóm" · menu Mô phỏng sự kiện của người khác.
(function () {
  'use strict';
  var old = document.querySelector('.mk-chat-wrap'); if (!old) return;
  var SP = window.__CX_SPACE || 'room';
  var tb = document.querySelector('.mk-comp-bar button.v2-btn') || document.querySelector('button.v2-btn');
  var DV = ''; if (tb) [].forEach.call(tb.attributes, function (a) { if (a.name.indexOf('data-v-') === 0) DV += ' ' + a.name + '=""'; });

  // ---------- tiện ích ----------
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function nc(c) { var x = c.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[đĐ]/g, 'd').toLowerCase(); return x.length === 1 ? x : c.toLowerCase(); }
  function norm(s) { return String(s).split('').map(nc).join(''); }
  var PAL = ['#0ea5e9', '#7c3aed', '#f59e0b', '#16a34a', '#db2777', '#2563eb', '#0d9488', '#ea580c', '#9333ea', '#475569'];
  function avc(n) { var h = 0; for (var i = 0; i < n.length; i++) h = (h * 31 + n.charCodeAt(i)) >>> 0; return PAL[h % PAL.length]; }
  function ini(n) { var p = n.trim().split(/\s+/); return (p[0][0] + (p.length > 1 ? p[p.length - 1][0] : '')).toUpperCase(); }
  function av(n, cls, dot) { return '<span class="cx-av ' + (cls || '') + '" style="background:' + avc(n) + '" title="' + esc(n) + '">' + esc(ini(n)) + (dot ? '<i class="dot"></i>' : '') + '</span>'; }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function hhmm() { var d = new Date(); return pad(d.getHours()) + ':' + pad(d.getMinutes()); }
  function dmy(d) { return pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + d.getFullYear(); }
  function pdate(s) { var m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec(String(s || '').trim()); if (!m) return null; var d = new Date(+m[3], m[2] - 1, +m[1]); return d.getDate() === +m[1] && d.getMonth() === m[2] - 1 ? d : null; }
  var TODAY = new Date(); TODAY.setHours(0, 0, 0, 0);
  function fsize(b) { return b >= 1048576 ? (b / 1048576).toFixed(1) + ' MB' : Math.max(1, Math.round(b / 1024)).toLocaleString('en-US') + ' KB'; }
  function fic(n) { var e = (n.split('.').pop() || '').toLowerCase(); return ({ pdf: ['ri-file-pdf-2-line', '#dc2626', 'PDF'], doc: ['ri-file-word-2-line', '#2563eb', 'Word'], docx: ['ri-file-word-2-line', '#2563eb', 'Word'], xls: ['ri-file-excel-2-line', '#16a34a', 'Excel'], xlsx: ['ri-file-excel-2-line', '#16a34a', 'Excel'], ppt: ['ri-file-ppt-2-line', '#ea580c', 'PowerPoint'], pptx: ['ri-file-ppt-2-line', '#ea580c', 'PowerPoint'], zip: ['ri-file-zip-line', '#7c3aed', 'Nén'], rar: ['ri-file-zip-line', '#7c3aed', 'Nén'], png: ['ri-image-line', '#7c3aed', 'Ảnh'], jpg: ['ri-image-line', '#7c3aed', 'Ảnh'], jpeg: ['ri-image-line', '#7c3aed', 'Ảnh'], mp4: ['ri-video-line', '#db2777', 'Video'] })[e] || ['ri-file-line', '#64748b', 'Tệp']; }
  function isImg(n) { return /\.(png|jpe?g|gif|webp)$/i.test(n); }
  function svgImg(t, c1, c2, kind) {
    var art = kind === 'shelf' ? '<g fill="#fff" opacity=".85"><rect x="40" y="60" width="240" height="8" rx="3"/><rect x="40" y="110" width="240" height="8" rx="3"/><rect x="40" y="160" width="240" height="8" rx="3"/><rect x="56" y="30" width="34" height="30" rx="3"/><rect x="100" y="38" width="26" height="22" rx="3"/><rect x="150" y="80" width="44" height="30" rx="3"/><rect x="210" y="86" width="30" height="24" rx="3"/><rect x="70" y="130" width="60" height="30" rx="3"/><rect x="200" y="124" width="40" height="36" rx="3"/></g>'
      : '<g fill="#fff"><rect x="30" y="40" width="260" height="120" rx="8" opacity=".18"/><text x="160" y="96" text-anchor="middle" font-family="Roboto,Arial" font-size="22" font-weight="700">HỘI NGHỊ CÔNG ĐOÀN</text><text x="160" y="124" text-anchor="middle" font-family="Roboto,Arial" font-size="14">15/01/2027 · Hội trường tầng 5</text></g>';
    var s = '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="200" viewBox="0 0 320 200"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="' + c1 + '"/><stop offset="1" stop-color="' + c2 + '"/></linearGradient></defs><rect width="320" height="200" fill="url(#g)"/>' + art + '<text x="12" y="190" font-family="Roboto,Arial" font-size="11" fill="#fff" opacity=".8">' + t + '</text></svg>';
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(s);
  }
  function btn(label, icon, kind, status, attr) {
    kind = kind || 'primary'; status = status || 'info';
    return '<button' + DV + ' type="button" class="v2-btn v2-btn--sm v2-btn--prefix-sm v2-btn--' + kind + ' v2-btn--' + kind + '-' + status + '" ' + (attr || '') + '>' + (icon ? '<div class="v2-btn__prefix--sm"><i class="' + icon + '" style="margin-right:3px"></i></div>' : '') + ' ' + label + ' </button>';
  }
  function badge(t) { return '<span class="mk-badge" style="--c:' + (SC[t] || '#64748b') + '">' + esc(t) + '</span>'; }
  function toast(m) { var t = document.querySelector('.mk-p-toast'); if (!t) { t = document.createElement('div'); t.className = 'mk-p-toast'; document.body.appendChild(t); } t.innerHTML = m; t.classList.add('on'); clearTimeout(toast.t); toast.t = setTimeout(function () { t.classList.remove('on'); }, 2600); }

  // ---------- dữ liệu ----------
  var SC = { 'Nháp': '#64748B', 'Chờ phê duyệt triển khai': '#D97706', 'Chờ bắt đầu': '#0EA5E9', 'Đang thực hiện': '#2563EB', 'Tạm dừng': '#F59E0B', 'Hoàn thành - Chờ duyệt': '#D97706',
    'Từ chối kết quả': '#DC2626', 'Hoàn thành': '#16A34A', 'Hủy': '#6B7280', 'Mới ghi nhận': '#64748B', 'Đã phân công': '#0EA5E9', 'Đang xử lý': '#2563EB', 'Đã xử lý xong': '#16A34A', 'Đã đóng': '#6B7280', 'Mở lại': '#F59E0B' };
  var ME = 'Đỗ Mai Anh';
  var D = SP === 'iproj' ? {
    title: 'Tổ chức hội nghị công đoàn 2027', kin: false, total: 4, ctx: 'Nhóm trao đổi',
    sub: 'Nhóm trao đổi · hạn 20/01/2027 · chỉ thành viên xem được',
    people: [['Trần Văn Minh', 'Quản lý', 'HN_NSHC', '21410133', 1], ['Đỗ Mai Anh', 'Thành viên', 'HN_NSHC', '21410301', 1], ['Lê Thu Trang', 'Thành viên', 'HN_NSHC', '21410210', 0],
      ['Vũ Hoàng Long', 'Thành viên', 'HN_NSHC', '21410322', 1], ['Nguyễn Thị Hằng', 'Xem', 'HN_NSHC', '21410102', 1]],
    joiner: null,
    objs: {
      P150: { k: 't', code: 'TPE.TASK.NB.26.0150', n: 'Đặt hội trường hội nghị', st: 'Đang thực hiện', as: 'Vũ Hoàng Long', ap: 'Trần Văn Minh', due: '08/11/2026', pct: 40, hrs: 6 },
      P151: { k: 't', code: 'TPE.TASK.NB.26.0151', n: 'Gửi giấy mời đại biểu', st: 'Chờ bắt đầu', as: ME, ap: 'Trần Văn Minh', due: '20/12/2026', pct: 0, hrs: 8 },
      P152: { k: 't', code: 'TPE.TASK.NB.26.0152', n: 'Thiết kế backdrop, phông nền hội nghị', st: 'Đang thực hiện', as: ME, ap: 'Trần Văn Minh', due: '15/11/2026', pct: 60, hrs: 10, pr: 'Cao' },
      P153: { k: 't', code: 'TPE.TASK.NB.26.0153', n: 'Dự trù kinh phí hội nghị', st: 'Hoàn thành - Chờ duyệt', as: 'Lê Thu Trang', ap: ME, due: '05/11/2026', pct: 100, hrs: 6 },
      PI1: { k: 'i', code: 'ISS-202611-0011', n: 'Hội trường tầng 5 trùng lịch ngày 15/01', st: 'Đang xử lý', as: 'Trần Văn Minh', rp: 'Vũ Hoàng Long', due: '06/11/2026', pr: 'Cao' }
    },
    msgs: [
      { d: 'Hôm qua', w: 'Trần Văn Minh', t: '16:30', x: 'Chào cả nhóm, nhóm này chỉ gồm người trong ban tổ chức vì có dự trù kinh phí và danh sách khen thưởng. Mọi trao đổi về hội nghị để ở đây nhé.', pin: 1 },
      { d: 'Hôm qua', sys: 'member', h: '<b>Trần Văn Minh</b> đã thêm <b>Đỗ Mai Anh</b>, <b>Lê Thu Trang</b>, <b>Vũ Hoàng Long</b> vào dự án', t: '16:31' },
      { d: 'Hôm qua', w: 'Trần Văn Minh', t: '16:40', x: '@{Vũ Hoàng Long} em liên hệ đặt hội trường giúp anh nhé #{P150}', rc: { '👌': ['Vũ Hoàng Long'] } },
      { d: 'Hôm qua', sys: 'assign', o: 'P150', h: '<b>Trần Văn Minh</b> đã giao nhiệm vụ {o} cho <b>Vũ Hoàng Long</b>', t: '16:40' },
      { d: 'Hôm nay', w: 'Vũ Hoàng Long', t: '08:15', x: 'Hội trường tầng 5 bị trùng lịch 15/01 với bên Kinh doanh anh ơi, em ghi vấn đề rồi #{PI1}' },
      { d: 'Hôm nay', w: 'Lê Thu Trang', t: '08:40', x: 'Chị gửi dự trù kinh phí, @{Đỗ Mai Anh} xem và duyệt giúp chị nhé #{P153}', f: [['Du_tru_kinh_phi_HN_2027.xlsx', 57344]] },
      { d: 'Hôm nay', sys: 'submit', o: 'P153', h: '<b>Lê Thu Trang</b> đã báo hoàn thành nhiệm vụ {o} · chờ <b>Đỗ Mai Anh</b> duyệt', t: '08:41' },
      { d: 'Hôm nay', w: 'Vũ Hoàng Long', t: '09:02', x: 'Bên in gửi 2 phương án backdrop, mọi người chọn giúp em.', f: [['Backdrop_PA1.png', 412000, svgImg('Backdrop_PA1.png', '#0f766e', '#1abc9c')], ['Backdrop_PA2.png', 398000, svgImg('Backdrop_PA2.png', '#1e3a8a', '#7c3aed')]], rc: { '👍': ['Trần Văn Minh', 'Đỗ Mai Anh'] } },
      { d: 'Hôm nay', w: ME, t: '09:10', x: 'Em chọn PA2, em hoàn thiện tiếp phần chữ nhé #{P152}', seen: 4 },
      { d: 'Hôm nay', w: 'Trần Văn Minh', t: '09:20', x: '@{Đỗ Mai Anh} giấy mời gửi trước 20/12 em nhé, danh sách đại biểu anh để trong file ghim.', unread: 1 }
    ]
  } : {
    title: 'Phòng Nhân Sự Hành Chính', kin: false, total: 18, ctx: 'Nhóm trao đổi',
    sub: 'Nhóm trao đổi · 18 thành viên',
    people: [['Nguyễn Thị Hằng', 'Quản lý', 'HN_NSHC', '21410102', 1], ['Trần Văn Minh', 'Thành viên', 'HN_NSHC', '21410133', 1], ['Lê Thu Trang', 'Thành viên', 'HN_NSHC', '21410210', 0],
      ['Phạm Quốc Huy', 'Thành viên', 'HN_NSHC', '21410245', 1], ['Đỗ Mai Anh', 'Thành viên', 'HN_NSHC', '21410301', 1], ['Vũ Hoàng Long', 'Thành viên', 'HN_NSHC', '21410322', 0],
      ['Bùi Thanh Tâm', 'Thành viên', 'HN_NSHC', '21410356', 1], ['Hoàng Lan Chi', 'Thành viên', 'HN_NSHC', '21410378', 0]],
    joiner: ['Ngô Đức Thịnh', 'Thành viên', 'HN_NSHC', '21410391', 1],
    objs: {
      T118: { k: 't', code: 'TPE.TASK.NB.26.0118', n: 'Gia hạn hợp đồng vệ sinh toà nhà', st: 'Đang thực hiện', as: 'Lê Thu Trang', ap: 'Nguyễn Thị Hằng', due: '01/11/2026', pct: 70, hrs: 4, pr: 'Cao' },
      T141: { k: 't', code: 'TPE.TASK.NB.26.0141', n: 'Báo giá may đồng phục 3 nhà cung cấp', st: 'Đang thực hiện', as: ME, ap: 'Nguyễn Thị Hằng', due: '07/11/2026', pct: 50, hrs: 12 },
      T142: { k: 't', code: 'TPE.TASK.NB.26.0142', n: 'Chốt danh sách size sơ mi toàn công ty', st: 'Chờ bắt đầu', as: ME, ap: 'Nguyễn Thị Hằng', due: '14/11/2026', pct: 0, hrs: 6 },
      T127: { k: 't', code: 'TPE.TASK.NB.26.0127', n: 'Cập nhật nội quy văn phòng 2027', st: 'Hoàn thành', as: 'Lê Thu Trang', ap: 'Nguyễn Thị Hằng', due: '31/10/2026', pct: 100, hrs: 5 },
      T155: { k: 't', code: 'TPE.TASK.NB.26.0155', n: 'Kiểm kê tài sản tầng 4', st: 'Hoàn thành - Chờ duyệt', as: 'Phạm Quốc Huy', ap: ME, due: '03/11/2026', pct: 100, hrs: 8 },
      I07: { k: 'i', code: 'ISS-202611-0007', n: 'Máy chấm công tầng 3 không nhận vân tay', st: 'Đã phân công', as: 'Phạm Quốc Huy', rp: ME, due: '04/11/2026', pr: 'Cao' },
      I09: { k: 'i', code: 'ISS-202611-0009', n: 'Điều hoà phòng họp 2 kêu to', st: 'Đang xử lý', as: 'Vũ Hoàng Long', rp: 'Nguyễn Thị Hằng', due: '05/11/2026' },
      TX: { k: 't', code: 'TPE.TASK.NB.26.0149', n: 'Phỏng vấn vòng 2 ứng viên Kế toán trưởng', st: 'Đang thực hiện', as: 'Nguyễn Thị Hằng', ap: 'Nguyễn Thị Hằng', due: '10/11/2026', lock: 'Tuyển dụng Kế toán trưởng' }
    },
    msgs: [
      { d: 'Hôm qua', w: ME, t: '08:30', x: 'Em đã cập nhật danh sách tài sản tầng 2 lên thư mục chung của nhóm.' },
      { d: 'Hôm qua', w: 'Trần Văn Minh', t: '16:20', x: 'Mọi người ơi, công đoàn chốt tổ chức hội nghị ngày 15/01. Mình đã tạo nhóm trao đổi **Tổ chức hội nghị công đoàn 2027** (có hạn tới 20/01) cho ban tổ chức bàn chi tiết nhé.' },
      { d: 'Hôm qua', sys: 'member', h: '<b>Trần Văn Minh</b> đã tạo nhóm trao đổi <a>Tổ chức hội nghị công đoàn 2027</a>', t: '16:21', ic: ['ri-folders-line', '#7c3aed'] },
      { d: 'Hôm qua', w: 'Nguyễn Thị Hằng', t: '16:35', x: '@{Đỗ Mai Anh} em lo phần báo giá đồng phục nhé, thứ 6 gửi chị. #{T141}', rc: { '👍': ['Trần Văn Minh', 'Lê Thu Trang'] } },
      { d: 'Hôm qua', sys: 'assign', o: 'T141', h: '<b>Nguyễn Thị Hằng</b> đã giao nhiệm vụ {o} cho <b>Đỗ Mai Anh</b>', t: '16:35' },
      { d: 'Hôm qua', w: 'Nguyễn Thị Hằng', t: '17:02', x: 'Lịch trực lễ tân tuần 45, mọi người xem và đổi ca trực tiếp với nhau nhé.', f: [['Lich_truc_le_tan_T45.pdf', 219136]], pin: 1 },
      { d: 'Hôm nay', w: 'Nguyễn Thị Hằng', t: '08:42', x: '@{Lê Thu Trang} hợp đồng vệ sinh toà nhà hết hạn từ 31/10 rồi, bên mình gia hạn chưa chị?', made: ['T118'] },
      { d: 'Hôm nay', sys: 'assign', o: 'T118', h: '<b>Lê Thu Trang</b> đã tạo nhiệm vụ {o} từ tin nhắn của <b>Nguyễn Thị Hằng</b>', t: '08:49', card: 1 },
      { d: 'Hôm nay', w: 'Lê Thu Trang', t: '08:50', x: 'Chị đang làm rồi em, chờ bên vệ sinh gửi phụ lục giá mới.', re: 5 },
      { d: 'Hôm nay', w: 'Phạm Quốc Huy', t: '09:05', x: 'Em kiểm kê xong tầng 4 rồi, gửi bảng kê và ảnh hiện trạng. @{Đỗ Mai Anh} duyệt giúp em nhé #{T155}', f: [['Bang_ke_tai_san_tang4.xlsx', 86016], ['Anh_hien_trang_tang4.jpg', 640000, svgImg('Anh_hien_trang_tang4.jpg', '#64748b', '#0ea5e9', 'shelf')]] },
      { d: 'Hôm nay', sys: 'submit', o: 'T155', h: '<b>Phạm Quốc Huy</b> đã báo hoàn thành nhiệm vụ {o} · chờ <b>Đỗ Mai Anh</b> duyệt', t: '09:06' },
      { d: 'Hôm nay', w: ME, t: '09:12', x: 'Cảm ơn anh Huy. Máy chấm công tầng 3 không nhận vân tay từ sáng, em báo vấn đề luôn: #{I07}', seen: 6 },
      { d: 'Hôm nay', sys: 'assign', o: 'I07', h: 'Vấn đề {o} đã phân công cho <b>Phạm Quốc Huy</b>', t: '09:13' },
      { d: 'Hôm nay', w: 'Nguyễn Thị Hằng', t: '09:30', x: 'Việc phỏng vấn Kế toán trưởng chị giao ở dự án tuyển dụng rồi nhé: #{TX}' },
      { d: 'Hôm nay', sys: 'done', o: 'T127', h: 'Nhiệm vụ {o} đã <b>hoàn thành</b> · <b>Nguyễn Thị Hằng</b> duyệt', t: '09:35' },
      { d: 'Hôm nay', w: 'Vũ Hoàng Long', t: '09:41', x: 'Điều hoà phòng họp 2 kêu to quá, em đang xử lý, chiều xong. #{I09}', rc: { '🙏': ['Nguyễn Thị Hằng'] }, unread: 1 },
      { d: 'Hôm nay', w: 'Trần Văn Minh', t: '09:44', x: '@{all} 14h chiều nay họp giao ban tuần ở phòng họp 1 nhé.', pin: 1 }
    ]
  };
  var PEOPLE = D.people.map(function (p) { return { n: p[0], r: p[1], dep: p[2], code: p[3], on: p[4] }; });
  function person(n) { return PEOPLE.filter(function (p) { return p.n === n; })[0]; }
  function plabel(n) { var p = person(n); return p ? p.n + ' - ' + p.dep + ' - ' + p.code : n; }
  var OBJ = D.objs;
  var EV = [
    ['assign', 'Giao việc mới · phân công vấn đề', 'Khi việc của không gian được giao / phân công', 1],
    ['start', 'Bắt đầu thực hiện', 'Người làm bấm Bắt đầu', 0],
    ['submit', 'Báo hoàn thành – chờ duyệt', 'Người làm nộp kết quả', 1],
    ['done', 'Duyệt kết quả – Hoàn thành', 'Người duyệt chấp nhận kết quả', 1],
    ['reject', 'Từ chối kết quả', 'Người duyệt trả lại kèm lý do', 1],
    ['issue', 'Vấn đề: đã xử lý · đóng · mở lại', 'Đổi trạng thái vấn đề', 1],
    ['overdue', 'Nhắc quá hạn', 'Hệ thống gom lúc 08:00 hằng ngày', 1],
    ['due', 'Đổi hạn · đề nghị gia hạn', '', 0],
    ['member', 'Thành viên vào / rời', 'Gồm đồng bộ theo phòng ban', 1]
  ];
  var EVON = {}; EV.forEach(function (e) { EVON[e[0]] = !!e[3]; });
  var EVIC = { assign: ['ri-user-shared-line', '#2563eb'], start: ['ri-play-circle-line', '#2563eb'], submit: ['ri-flag-2-line', '#d97706'], done: ['ri-checkbox-circle-line', '#16a34a'], reject: ['ri-close-circle-line', '#dc2626'], issue: ['ri-bug-line', '#0ea5e9'], overdue: ['ri-alarm-warning-line', '#dc2626'], due: ['ri-calendar-event-line', '#d97706'], member: ['ri-team-line', '#7c3aed'], pin: ['ri-pushpin-2-line', '#d97706'] };

  var uid = 0; function nid() { return 'm' + (++uid); }
  var MSG = [];
  function parseX(x) { var segs = [], re = /@\{([^}]+)\}|#\{([^}]+)\}/g, m, last = 0; while ((m = re.exec(x))) { if (m.index > last) segs.push(x.slice(last, m.index)); segs.push(m[1] ? { m: m[1] === 'all' ? '*' : m[1] } : { r: m[2] }); last = re.lastIndex; } if (last < x.length) segs.push(x.slice(last)); return segs; }
  var idx = {};
  D.msgs.forEach(function (m, i) {
    var o = { id: nid(), d: m.d, t: m.t };
    if (m.sys) { o.sys = m.sys; o.h = m.h; o.o = m.o; o.card = m.card; o.ic = m.ic; }
    else { o.w = m.w; o.segs = parseX(m.x); o.files = (m.f || []).map(function (f) { return { n: f[0], s: f[1], url: f[2] || '' }; }); o.rc = m.rc || {}; o.pin = !!m.pin; o.made = m.made || []; o.seen = m.seen || 0; if (m.re != null) o.re = idx[m.re]; }
    idx[i] = o.id; MSG.push(o);
  });
  // ---------- trạng thái ----------
  var S = { unread: null, reply: null, edit: null, att: [], side: 'viec', vf: 'all', peek: null, q: '', hits: [], hi: -1, typing: '', below: 0, notif: 'all', pinIdx: 0, newIds: {} };
  (function () { for (var i = 0; i < D.msgs.length; i++) if (D.msgs[i].unread) { S.unread = idx[i]; break; } })();
  function byId(id) { for (var i = 0; i < MSG.length; i++) if (MSG[i].id === id) return MSG[i]; return null; }
  // 05/11 [U]: sửa / thu hồi tin của mình trong 24 giờ (giờ demo: hôm nay 09:45)
  function in24(m) { return !m.d || m.d === 'Hôm nay' || (m.d === 'Hôm qua' && m.t > '09:45'); }
  function pinned() { return MSG.filter(function (m) { return m.pin && !m.rec; }); }
  function overdue(o) { var d = pdate(o.due); return d && d < TODAY && ['Hoàn thành', 'Hoàn thành - Chờ duyệt', 'Hủy', 'Nháp', 'Đã xử lý xong', 'Đã đóng'].indexOf(o.st) < 0; } // L2 chưa chốt: đang theo mockup (đã nộp kết quả không tính quá hạn)
  function daysLeft(o) { var d = pdate(o.due); return d ? Math.round((d - TODAY) / 864e5) : null; }

  // ---------- khung ----------
  var root = document.createElement('div'); root.className = 'cx-wrap';
  var online = PEOPLE.filter(function (p) { return p.on; }).length;
  root.innerHTML =
    '<div class="cx-main">' +
      '<div class="cx-hd"><div class="cx-hd-l"><div class="cx-hd-ic"><i class="' + (D.kin ? 'ri-folder-lock-line' : 'ri-chat-3-line') + '"></i></div><div style="min-width:0"><div class="t">Trao đổi' + (D.kin ? '<i class="ri-lock-2-line" data-tip="Chỉ thành viên"></i>' : '') + '</div><div class="s">' + D.total + ' thành viên · <i class="on"></i>' + online + ' đang trực tuyến</div></div></div>' +
      '<div class="cx-hd-r"><span class="cx-demo" data-act="demo"><i class="ri-play-circle-line"></i>Mô phỏng sự kiện</span>' +
      '<button class="cx-ib" data-act="search" data-tip="Tìm trong trao đổi (Ctrl F)"><i class="ri-search-line"></i></button>' +
      '<button class="cx-ib" data-act="notif" data-tip="Thông báo của tôi"><i class="ri-notification-3-line"></i></button>' +
      '<button class="cx-ib" data-act="auto" data-tip="Tự báo vào nhóm"><i class="ri-robot-2-line"></i></button>' +
      '<button class="cx-ib on" data-act="side" data-tip="Ẩn / hiện cột bên phải"><i class="ri-layout-right-line"></i></button></div></div>' +
      '<div class="cx-pinbar" data-act="pinbar" hidden></div>' +
      '<div class="cx-search" hidden><i class="ri-search-line" style="color:#94a3b8"></i><input placeholder="Tìm theo nội dung tin nhắn, tên người gửi, tên file"><span class="n"></span><button class="cx-ib" data-act="sprev" data-tip="Kết quả trước"><i class="ri-arrow-up-s-line"></i></button><button class="cx-ib" data-act="snext" data-tip="Kết quả sau"><i class="ri-arrow-down-s-line"></i></button><button class="cx-ib" data-act="sclose" data-tip="Đóng (Esc)"><i class="ri-close-line"></i></button></div>' +
      '<div class="cx-bodyw"><div class="cx-body"></div><button class="cx-down" data-act="down"><i class="ri-arrow-down-line"></i><span></span></button><div class="cx-drop"><i class="ri-upload-cloud-2-line"></i>Thả file vào đây để gửi<small>Tối đa 50 MB mỗi file</small></div></div>' +
      '<div class="cx-typing"></div>' +
      '<div class="cx-comp"><div class="cx-ctx" hidden></div><div class="cx-atts"></div>' +
        '<div class="cx-in empty" contenteditable="true" data-ph="Nhập tin nhắn… gõ @ để nhắc tên, # để chèn nhiệm vụ / vấn đề"></div>' +
        '<div class="cx-bar"><div class="ic">' +
          '<button class="cx-ib" data-act="attach" data-tip="Đính kèm file (hoặc kéo thả / dán ảnh)"><i class="ri-attachment-2"></i></button>' +
          '<button class="cx-ib" data-act="at" data-tip="Nhắc tên">@</button>' +
          '<button class="cx-ib" data-act="hash" data-tip="Chèn nhiệm vụ / vấn đề">#</button>' +
          '<button class="cx-ib" data-act="emoji" data-tip="Biểu cảm"><i class="ri-emotion-line"></i></button>' +
          '<span class="sep"></span><span class="cx-mk" data-act="newobj"><i class="ri-add-line"></i>Tạo việc<i class="ri-arrow-down-s-line"></i></span>' +
        '</div><div class="r"><small>Enter gửi · Shift + Enter xuống dòng</small>' + btn('Gửi', 'ri-send-plane-2-line', 'primary', 'info', 'data-act="send"') + '</div></div>' +
        '<input type="file" multiple hidden class="cx-file-in"></div>' +
    '</div><div class="cx-side"></div>';
  old.parentNode.replaceChild(root, old);
  var $ = function (s) { return root.querySelector(s); };
  var body = $('.cx-body'), input = $('.cx-in'), main = $('.cx-main');

  // ---------- hiển thị tin ----------
  function hiText(s) {
    var t = esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
    if (!S.q) return t.replace(/\n/g, '<br>');
    var q = norm(S.q), raw = t, n = norm(raw), out = '', i = 0, inTag = false, k;
    // bọc <mark> trên chữ (bỏ qua thẻ html)
    for (k = 0; k < raw.length;) {
      if (raw[k] === '<') inTag = true;
      if (!inTag && n.substr(k, q.length) === q) { out += '<mark>' + raw.substr(k, q.length) + '</mark>'; k += q.length; continue; }
      if (raw[k] === '>') inTag = false;
      out += raw[k]; k++;
    }
    return out.replace(/\n/g, '<br>');
  }
  function segHtml(segs) {
    return segs.map(function (s) {
      if (typeof s === 'string') return hiText(s);
      if (s.m) { var all = s.m === '*'; return '<span class="cx-at' + (all || s.m === ME ? ' me' : '') + '">@' + esc(all ? 'Tất cả' : s.m) + '</span>'; }
      var o = OBJ[s.r]; if (!o) return '';
      return '<a class="cx-ref" data-act="peek" data-obj="' + s.r + '">#' + esc(o.lock ? o.code : o.code) + '</a>';
    }).join('');
  }
  function segText(segs) { return (segs || []).map(function (s) { return typeof s === 'string' ? s : s.m ? '@' + (s.m === '*' ? 'Tất cả' : s.m) : '#' + ((OBJ[s.r] || {}).code || ''); }).join('').replace(/\*\*/g, ''); }
  function refsOf(m) { var r = []; (m.segs || []).forEach(function (s) { if (s.r && r.indexOf(s.r) < 0) r.push(s.r); }); return r; }
  function mentionsMe(m) { return (m.segs || []).some(function (s) { return s.m === ME || s.m === '*'; }); }
  function acts(o) {
    if (o.lock) return [];
    var a = [];
    if (o.k === 't') {
      if (o.st === 'Chờ bắt đầu' && o.as === ME) a.push(['Bắt đầu', 'ri-play-line', 'start', 'primary']);
      if ((o.st === 'Đang thực hiện' || o.st === 'Từ chối kết quả') && o.as === ME) a.push(['Báo kết quả', 'ri-flag-2-line', 'submit', 'primary']);
      if (o.st === 'Hoàn thành - Chờ duyệt' && o.ap === ME) { a.push(['Duyệt', 'ri-check-line', 'approve', 'primary']); a.push(['Từ chối', 'ri-close-line', 'reject', 'primary', 'danger']); }
    } else {
      if ((o.st === 'Mới ghi nhận' || o.st === 'Đã phân công') && o.as === ME) a.push(['Nhận xử lý', 'ri-hand', 'take', 'primary']);
      if ((o.st === 'Đang xử lý' || o.st === 'Mở lại') && o.as === ME) a.push(['Báo đã xử lý', 'ri-check-double-line', 'resolve', 'primary']);
      if (o.st === 'Đã xử lý xong' && o.rp === ME) { a.push(['Đóng vấn đề', 'ri-checkbox-circle-line', 'close', 'primary']); a.push(['Mở lại', 'ri-arrow-go-back-line', 'reopen', 'secondary']); }
    }
    return a;
  }
  function actBtns(id) { return acts(OBJ[id]).map(function (a) { return btn(a[0], a[1], a[3], a[4] || 'info', 'data-act="oa" data-op="' + a[2] + '" data-obj="' + id + '"'); }).join(''); }
  function dueHtml(o) { if (!o.due) return ''; var over = overdue(o), dl = daysLeft(o), done = ['Hoàn thành', 'Đã đóng', 'Đã xử lý xong', 'Hoàn thành - Chờ duyệt'].indexOf(o.st) >= 0; return '<span class="' + (over ? 'over' : !done && dl != null && dl <= 3 ? 'soon' : '') + '"><i class="ri-calendar-line"></i> Hạn ' + o.due.slice(0, 5) + (over ? ' · quá ' + (-dl) + ' ngày' : !done && dl != null && dl <= 3 ? (dl === 0 ? ' · hôm nay' : ' · còn ' + dl + ' ngày') : '') + '</span>'; }
  function card(id) {
    var o = OBJ[id]; if (!o) return '';
    if (o.lock) return '<div class="cx-card locked"><i class="ri-lock-2-line"></i><div><b>' + (SP === 'gp' ? 'Nhiệm vụ trong không gian khác' : 'Nhiệm vụ trong nhóm trao đổi khác') + '</b><small>Bạn không phải thành viên “' + esc(o.lock) + '” nên không xem được nội dung. Thẻ được kiểm quyền theo người xem.</small></div></div>';
    var t = o.k === 't', c = SC[o.st] || '#2563eb';
    var A = acts(o), mine = (t ? o.as === ME || o.ap === ME : o.as === ME || o.rp === ME);
    return '<div class="cx-card" data-card="' + id + '" style="--c:' + c + '"><div class="cx-card-hd"><i class="' + (t ? 'ri-task-line' : 'ri-bug-line') + '" style="color:' + (t ? '#2563eb' : '#d97706') + '"></i>' + (t ? 'Nhiệm vụ' : 'Vấn đề') + '<span class="code">' + esc(o.code) + '</span>' +
      (o.pr ? '<span class="pr" style="color:' + (o.pr === 'Khẩn cấp' ? '#dc2626' : '#d97706') + '"><i class="ri-flag-fill"></i>' + o.pr + '</span>' : '') + '</div>' +
      '<a class="cx-card-n" data-act="peek" data-obj="' + id + '">' + esc(o.n) + '</a>' +
      '<div class="cx-card-r">' + badge(o.st) + '<span><i class="ri-user-line"></i> ' + esc(o.as || 'Chưa phân công') + '</span>' + dueHtml(o) +
      (t && o.pct != null ? '<span class="cx-pg"><i><b style="width:' + o.pct + '%"></b></i>' + o.pct + '%</span>' : '') + '</div>' +
      (A.length ? '<div class="cx-card-act">' + actBtns(id) + '<span class="hint">' + (t && o.ap === ME && o.st === 'Hoàn thành - Chờ duyệt' ? 'Bạn là người duyệt' : o.k === 'i' && o.rp === ME && o.st === 'Đã xử lý xong' ? 'Bạn là người báo' : 'Bạn là người làm') + '</span></div>' : '') + '</div>';
  }
  function sysHtml(m) {
    var ic = m.ic || EVIC[m.sys] || ['ri-information-line', '#64748b'];
    var h = m.h.replace('{o}', m.o && OBJ[m.o] ? '<a data-act="peek" data-obj="' + m.o + '">' + esc(OBJ[m.o].n) + '</a>' : '');
    return '<div class="cx-sys' + (m.sys === 'overdue' ? ' warn' : '') + (S.newIds[m.id] ? ' new' : '') + '" data-id="' + m.id + '"><span class="ln"><span class="ic" style="background:' + ic[1] + '"><i class="' + ic[0] + '"></i></span><span>' + h + ' <small>' + m.t + '</small></span></span>' + (m.card && m.o ? card(m.o) : '') + '</div>';
  }
  function filesHtml(m) {
    if (!m.files || !m.files.length) return '';
    return '<div class="cx-files">' + m.files.map(function (f, i) {
      if (isImg(f.n) && f.url) return '<img class="cx-img" src="' + f.url + '" alt="' + esc(f.n) + '" data-act="lb" data-id="' + m.id + '" data-i="' + i + '">';
      var x = fic(f.n); return '<div class="cx-file" data-act="dl" data-n="' + esc(f.n) + '"><i class="' + x[0] + '" style="color:' + x[1] + '"></i><div><b>' + esc(f.n) + '</b><small>' + fsize(f.s) + ' · ' + x[2] + '</small></div><i class="ri-download-2-line dl"></i></div>';
    }).join('') + '</div>';
  }
  function msgHtml(m, cont) {
    var me = m.w === ME;
    if (m.rec) return '<div class="cx-msg' + (me ? ' me' : '') + (cont ? ' cont' : '') + '" data-id="' + m.id + '">' + (me ? '' : av(m.w)) + '<div class="cx-meta"><div class="cx-who">' + (me ? '' : esc(m.w)) + '<small>' + m.t + '</small></div><div class="cx-bub recalled"><i class="ri-arrow-go-back-line"></i> Tin nhắn đã được thu hồi</div></div></div>';
    var q = m.re && byId(m.re), rc = Object.keys(m.rc || {}).filter(function (k) { return m.rc[k].length; });
    var refs = refsOf(m);
    var hit = S.q && S.hits[S.hi] === m.id;
    return '<div class="cx-msg' + (me ? ' me' : '') + (cont ? ' cont' : '') + (!me && mentionsMe(m) ? ' atme' : '') + (hit ? ' hit-cur' : '') + '" data-id="' + m.id + '">' + (me ? '' : av(m.w)) +
      '<div class="cx-meta"><div class="cx-who">' + (me ? '' : esc(m.w)) + '<small>' + m.t + '</small>' + (m.ed ? '<small>(đã sửa)</small>' : '') + (m.pin ? '<i class="ri-pushpin-2-fill" data-tip="Đã ghim"></i>' : '') + '</div>' +
      (m.segs && segText(m.segs).trim() || q ? '<div class="cx-bub">' + (q ? '<div class="cx-quote" data-act="jump" data-to="' + q.id + '"><i class="ri-reply-line"></i> <b>' + esc(q.w) + '</b>: ' + esc(q.rec ? 'Tin nhắn đã thu hồi' : segText(q.segs).slice(0, 90) || '[File]') + '</div>' : '') + segHtml(m.segs) + '</div>' : '') +
      filesHtml(m) + refs.map(card).join('') +
      (m.made.length ? m.made.map(function (id) { var o = OBJ[id]; return o ? '<div class="cx-made"><i class="ri-corner-down-right-line"></i>Đã tạo ' + (o.k === 't' ? 'nhiệm vụ' : 'vấn đề') + ' <a data-act="peek" data-obj="' + id + '">' + esc(o.code) + '</a>' + (o.st === 'Nháp' ? ' (nháp)' : '') + ' từ tin nhắn này</div>' : ''; }).join('') : '') +
      (rc.length ? '<div class="cx-rcs">' + rc.map(function (k) { var mine = m.rc[k].indexOf(ME) >= 0; return '<span class="cx-rc' + (mine ? ' mine' : '') + '" data-act="react" data-id="' + m.id + '" data-e="' + k + '" data-tip="' + esc(m.rc[k].map(function (n) { return n === ME ? 'Bạn' : n; }).join(', ')) + '">' + k + ' ' + m.rc[k].length + '</span>'; }).join('') + '</div>' : '') +
      (me && m.seen ? '<div class="cx-seen">Đã xem · ' + m.seen + '<span class="avs">' + PEOPLE.filter(function (p) { return p.n !== ME; }).slice(0, Math.min(3, m.seen)).map(function (p) { return av(p.n, 'xs'); }).join('') + '</span></div>' : '') +
      '</div>' +
      '<div class="cx-tools">' + ['👍', '❤️', '😂', '😮', '✅'].map(function (e) { return '<span class="em" data-act="react" data-id="' + m.id + '" data-e="' + e + '">' + e + '</span>'; }).join('') + '<span class="sep"></span>' +
        '<span data-act="reply" data-id="' + m.id + '" data-tip="Trả lời"><i class="ri-reply-line"></i></span>' +
        '<span data-act="mkobj" data-k="t" data-id="' + m.id + '" data-tip="Tạo nhiệm vụ từ tin này"><i class="ri-task-line"></i><span class="lb">Nhiệm vụ</span></span>' +
        '<span data-act="mkobj" data-k="i" data-id="' + m.id + '" data-tip="Tạo vấn đề từ tin này"><i class="ri-bug-line"></i><span class="lb">Vấn đề</span></span>' +
        '<span data-act="more" data-id="' + m.id + '" data-tip="Thêm"><i class="ri-more-2-fill"></i></span></div></div>';
  }
  function render(opts) {
    opts = opts || {};
    var atBottom = body.scrollHeight - body.scrollTop - body.clientHeight < 80, prevTop = body.scrollTop;
    var h = '', lastDay = '', prev = null;
    MSG.forEach(function (m) {
      if (m.d !== lastDay) { h += '<div class="cx-day"><span>' + m.d + '</span></div>'; lastDay = m.d; prev = null; }
      if (S.unread === m.id) { var n = MSG.slice(MSG.indexOf(m)).filter(function (x) { return !x.sys && x.w !== ME; }).length; h += '<div class="cx-unread">' + n + ' tin nhắn mới</div>'; prev = null; }
      if (m.sys) { h += sysHtml(m); prev = null; return; }
      var cont = prev && prev.w === m.w && !m.re && !prev.rec;
      h += msgHtml(m, cont); prev = m;
    });
    body.innerHTML = h;
    S.newIds = {};
    if (opts.bottom || (atBottom && !opts.keep)) body.scrollTop = body.scrollHeight; else body.scrollTop = prevTop;
    renderPinbar(); renderSide(); downBtn();
  }
  function downBtn() {
    var far = body.scrollHeight - body.scrollTop - body.clientHeight > 160, b = $('.cx-down');
    if (!far) S.below = 0;
    b.classList.toggle('on', far);
    b.querySelector('span').textContent = S.below ? S.below + ' tin mới' : 'Xuống cuối';
  }
  body.addEventListener('scroll', downBtn);
  function jump(id) {
    var el = body.querySelector('[data-id="' + id + '"]'); if (!el) return;
    el.scrollIntoView({ block: 'center', behavior: 'smooth' });
    el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash');
  }
  function renderPinbar() {
    var P = pinned(), b = $('.cx-pinbar');
    if (!P.length) { b.hidden = true; return; }
    if (S.pinIdx >= P.length) S.pinIdx = 0;
    var m = P[P.length - 1 - S.pinIdx];
    b.hidden = false;
    b.innerHTML = '<span class="bar"></span><i class="ri-pushpin-2-fill"></i><div class="tx"><b>' + esc(m.w === ME ? 'Bạn' : m.w) + ':</b> ' + esc(segText(m.segs) || (m.files[0] || {}).n || '') + '</div><small>' + (S.pinIdx + 1) + ' / ' + P.length + ' tin đã ghim</small><a data-act="pinall">Xem tất cả</a><span class="x" data-act="unpin" data-id="' + m.id + '" data-tip="Bỏ ghim tin này"><i class="ri-close-line"></i></span>';
    b.dataset.id = m.id;
  }

  // ---------- cột phải ----------
  function allObjIds() {
    var ids = [];
    MSG.forEach(function (m) { if (m.sys && m.o) ids.push(m.o); (m.segs || []).forEach(function (s) { if (s.r) ids.push(s.r); }); (m.made || []).forEach(function (x) { ids.push(x); }); });
    return ids.filter(function (x, i) { return ids.indexOf(x) === i && OBJ[x]; });
  }
  function allFiles() { var r = []; MSG.forEach(function (m) { if (!m.rec) (m.files || []).forEach(function (f, i) { r.push({ f: f, m: m, i: i }); }); }); return r.reverse(); }
  function renderSide() {
    var side = $('.cx-side');
    if (S.peek) return renderPeek(side);
    var ids = allObjIds(), F = allFiles(), P = pinned();
    var tabs = [['viec', 'Việc', ids.filter(function (x) { return !OBJ[x].lock; }).length], ['ghim', 'Ghim', P.length], ['file', 'File', F.length], ['tv', 'Thành viên', D.total]];
    var h = '<div class="cx-stabs">' + tabs.map(function (t) { return '<span class="' + (S.side === t[0] ? 'on' : '') + '" data-act="stab" data-t="' + t[0] + '">' + t[1] + '<small>' + t[2] + '</small></span>'; }).join('') + '</div><div class="cx-sbody">';
    if (S.side === 'viec') {
      var f = S.vf, L = ids.filter(function (x) { var o = OBJ[x]; if (o.lock) return false; if (f === 'mine') return o.as === ME || o.ap === ME || o.rp === ME; if (f === 'open') return ['Hoàn thành', 'Đã đóng', 'Hủy'].indexOf(o.st) < 0; if (f === 'act') return acts(o).length > 0; return true; });
      h += '<div class="cx-chips">' + [['all', 'Tất cả'], ['act', 'Chờ tôi'], ['mine', 'Của tôi'], ['open', 'Chưa xong']].map(function (c) { return '<span class="' + (f === c[0] ? 'on' : '') + '" data-act="vf" data-f="' + c[0] + '">' + c[1] + '</span>'; }).join('') + '</div>';
      h += L.length ? L.reverse().map(function (x) { var o = OBJ[x]; return '<div class="cx-li" data-act="peek" data-obj="' + x + '"><i class="' + (o.k === 't' ? 'ri-task-line' : 'ri-bug-line') + '" style="color:' + (o.k === 't' ? '#2563eb' : '#d97706') + '"></i><div class="nm"><div>' + esc(o.n) + '</div><div class="sub">' + badge(o.st) + '<span>' + esc(o.as || '') + '</span>' + (o.due ? '<span class="' + (overdue(o) ? 'over' : '') + '">Hạn ' + o.due.slice(0, 5) + '</span>' : '') + (acts(o).length ? '<span style="color:#0f766e;font-weight:600">● chờ bạn</span>' : '') + '</div></div></div>'; }).join('') : '<div class="cx-empty"><i class="ri-task-line"></i>Không có việc nào khớp</div>';
      h += '<div class="cx-sft">Gồm việc được nhắc (#), tạo từ tin nhắn và việc tự báo vào nhóm. Thẻ việc chỉ hiện đủ với người có quyền xem việc đó.</div>';
    } else if (S.side === 'ghim') {
      h += P.length ? P.slice().reverse().map(function (m) { return '<div class="cx-li" data-act="jump" data-to="' + m.id + '"><i class="ri-pushpin-2-fill" style="color:#d97706"></i><div class="nm"><div>' + esc(segText(m.segs) || (m.files[0] || {}).n || '') + '</div><div class="sub">' + esc(m.w === ME ? 'Bạn' : m.w) + ' · ' + m.d.toLowerCase() + ' ' + m.t + '</div></div><span class="x" data-act="unpin" data-id="' + m.id + '" data-tip="Bỏ ghim"><i class="ri-close-line"></i></span></div>'; }).join('') : '<div class="cx-empty"><i class="ri-pushpin-2-line"></i>Chưa có tin nào được ghim.<br>Rê chuột vào tin → ⋮ → Ghim tin nhắn.</div>';
      h += '<div class="cx-sft">Quản lý và Thành viên ghim / bỏ ghim được (người chỉ xem thì không); tối đa 20 tin. Tin ghim mới nhất hiện ở thanh trên cùng.</div>';
    } else if (S.side === 'file') {
      h += F.length ? F.map(function (x) { var f = x.f, ic = fic(f.n); return '<div class="cx-li" data-act="' + (isImg(f.n) && f.url ? 'lb' : 'jump') + '" data-id="' + x.m.id + '" data-i="' + x.i + '" data-to="' + x.m.id + '">' + (isImg(f.n) && f.url ? '<img src="' + f.url + '">' : '<i class="' + ic[0] + '" style="color:' + ic[1] + ';font-size:20px"></i>') + '<div class="nm"><div>' + esc(f.n) + '</div><div class="sub">' + esc(x.m.w === ME ? 'Bạn' : x.m.w) + ' · ' + fsize(f.s) + ' · ' + x.m.d.toLowerCase() + '</div></div><i class="ri-chat-forward-line x" data-act="jump" data-to="' + x.m.id + '" data-tip="Đi tới tin nhắn"></i></div>'; }).join('') : '<div class="cx-empty"><i class="ri-folder-line"></i>Chưa có file</div>';
      h += '<div class="cx-sft">File gửi trong trao đổi cũng hiện ở tab <a>File</a> của không gian (cột Nguồn = Trao đổi).</div>';
    } else {
      h += PEOPLE.map(function (p) { return '<div class="cx-li" data-act="atp" data-n="' + esc(p.n) + '">' + av(p.n, 'sm', p.on) + '<div class="nm"><div>' + esc(p.n) + (p.n === ME ? ' (bạn)' : '') + '</div><div class="sub">' + esc(p.r) + ' · ' + p.dep + ' · ' + p.code + '</div></div>' + (p.n !== ME ? '<i class="x" style="font-style:normal;font-weight:700;font-size:13px;color:#0f766e" data-tip="Nhắc tên">@</i>' : '') + '</div>'; }).join('');
      if (D.total > PEOPLE.length) h += '<div class="cx-sft">… và ' + (D.total - PEOPLE.length) + ' thành viên khác. Thêm / bớt người ở tab <a>Thành viên</a>.</div>';
    }
    side.innerHTML = h + '</div>';
  }
  function renderPeek(side) {
    var id = S.peek, o = OBJ[id];
    var t = o.k === 't';
    var tl = MSG.filter(function (m) { return (m.sys && m.o === id) || refsOf(m).indexOf(id) >= 0 || (m.made || []).indexOf(id) >= 0; });
    side.innerHTML = '<div class="cx-peek-hd"><span data-act="unpeek"><i class="ri-arrow-left-line"></i>Quay lại danh sách việc</span></div><div class="cx-sbody"><div class="cx-peek">' +
      (o.lock ? '<div class="cx-empty"><i class="ri-lock-2-line"></i>Việc thuộc nhóm trao đổi “' + esc(o.lock) + '”.<br>Bạn không phải thành viên nên không xem được.</div>' :
      '<div class="code"><i class="' + (t ? 'ri-task-line' : 'ri-bug-line') + '" style="color:' + (t ? '#2563eb' : '#d97706') + '"></i>' + (t ? 'Nhiệm vụ' : 'Vấn đề') + ' · ' + esc(o.code) + '</div><h4>' + esc(o.n) + '</h4>' +
      '<dl class="cx-kv"><dt>Trạng thái</dt><dd>' + badge(o.st) + '</dd><dt>' + (t ? 'Người thực hiện' : 'Người xử lý') + '</dt><dd>' + esc(o.as || 'Chưa phân công') + '</dd><dt>' + (t ? 'Người duyệt' : 'Người báo') + '</dt><dd>' + esc(t ? o.ap : o.rp) + '</dd>' +
      '<dt>Hạn</dt><dd>' + (o.due ? dueHtml(o) : '—') + '</dd>' + (t ? '<dt>Tiến độ</dt><dd><span class="cx-pg"><i><b style="width:' + (o.pct || 0) + '%"></b></i>' + (o.pct || 0) + '%</span></dd>' : '') +
      '<dt>Ưu tiên</dt><dd>' + (o.pr || 'Bình thường') + '</dd><dt>Không gian</dt><dd>' + esc(D.title) + '</dd></dl>' +
      '<div class="acts">' + actBtns(id) + btn('Mở chi tiết', 'ri-external-link-line', 'secondary', 'info', 'data-act="open" data-obj="' + id + '"') + '</div>' +
      '<div class="tl-t">Trong trao đổi</div><div class="cx-tl">' + (tl.length ? tl.map(function (m) { return '<div data-act="jump" data-to="' + m.id + '">' + (m.sys ? m.h.replace(/<[^>]+>/g, '').replace('{o}', '“' + o.n + '”') : esc((m.w === ME ? 'Bạn' : m.w) + ': ' + segText(m.segs).slice(0, 70))) + ' <small>' + m.d.toLowerCase() + ' ' + m.t + '</small></div>'; }).join('') : '<small>Chưa có</small>') + '</div>') +
      '</div></div>';
  }

  // ---------- thêm tin ----------
  function addMsg(m, opts) {
    opts = opts || {};
    m.id = nid(); m.d = 'Hôm nay'; m.t = m.t || hhmm();
    if (!m.sys) { m.rc = m.rc || {}; m.files = m.files || []; m.made = m.made || []; m.seen = m.seen || 0; }
    MSG.push(m); S.newIds[m.id] = 1;
    var far = body.scrollHeight - body.scrollTop - body.clientHeight > 160;
    if (far && m.w !== ME) S.below++;
    render({ bottom: m.w === ME || opts.bottom || !far, keep: far });
    return m;
  }
  function announce(ev, h, o, extra) {
    if (!EVON[ev]) { toast('<i class="ri-notification-off-line"></i> Sự kiện “' + EV.filter(function (e) { return e[0] === ev; })[0][1] + '” đang tắt — không báo vào nhóm'); return null; }
    var m = { sys: ev, h: h, o: o }; for (var k in extra || {}) m[k] = extra[k];
    return addMsg(m, { bottom: true });
  }
  function pulse(id) { setTimeout(function () { root.querySelectorAll('[data-card="' + id + '"]').forEach(function (c) { c.classList.remove('pulse'); void c.offsetWidth; c.classList.add('pulse'); }); }, 30); }
  function typing(name, ms, then) { S.typing = name; $('.cx-typing').innerHTML = '<span class="dots"><i></i><i></i><i></i></span>' + esc(name) + ' đang soạn tin…'; setTimeout(function () { S.typing = ''; $('.cx-typing').innerHTML = ''; then && then(); }, ms); }

  // ---------- popup nổi ----------
  var POP = null;
  function closePop() { if (POP) { POP.el.remove(); if (POP.onClose) POP.onClose(); POP = null; } root.querySelectorAll('.cx-tools.keep').forEach(function (t) { t.classList.remove('keep'); }); }
  function openPop(html, anchor, o) {
    closePop(); o = o || {};
    var el = document.createElement('div'); el.className = 'cx-pop ' + (o.cls || ''); el.innerHTML = html; document.body.appendChild(el);
    var r = anchor.getBoundingClientRect ? anchor.getBoundingClientRect() : anchor, w = el.offsetWidth, hh = el.offsetHeight;
    var left = o.alignRight ? r.right - w : r.left; left = Math.max(8, Math.min(left, window.innerWidth - w - 8));
    var top = o.up || r.bottom + hh + 8 > window.innerHeight ? r.top - hh - 6 : r.bottom + 6;
    el.style.left = left + 'px'; el.style.top = Math.max(8, top) + 'px';
    POP = { el: el, onClose: o.onClose, kind: o.kind };
    el.addEventListener('mousedown', function (e) { if (!e.target.closest('input')) e.preventDefault(); });
    return el;
  }
  document.addEventListener('mousedown', function (e) { if (POP && !POP.el.contains(e.target) && !e.target.closest('[data-act="more"],[data-act="demo"],[data-act="notif"],[data-act="auto"],[data-act="emoji"],[data-act="newobj"]')) closePop(); });
  window.addEventListener('resize', closePop);
  body.addEventListener('scroll', function () { if (POP && POP.kind === 'menu') closePop(); });
  function menu(anchor, items, onPick, o) {
    var el = openPop('<div class="cx-menu">' + items.map(function (it, i) { if (it === '-') return '<div class="sp"></div>'; if (it.ti) return '<div class="ti">' + it.ti + '</div>'; return '<div class="mi ' + (it.dg ? 'dg' : '') + '" data-i="' + i + '"><i class="' + it.ic + '"></i>' + it.t + (it.k ? '<small>' + it.k + '</small>' : '') + '</div>'; }).join('') + '</div>', anchor, Object.assign({ kind: 'menu' }, o || {}));
    el.addEventListener('click', function (e) { var mi = e.target.closest('.mi'); if (!mi) return; var it = items[+mi.dataset.i]; closePop(); onPick(it); });
  }

  // ---------- ô soạn: @ / # ----------
  var savedRange = null;
  document.addEventListener('selectionchange', function () { var s = getSelection(); if (s.rangeCount && input.contains(s.anchorNode)) savedRange = s.getRangeAt(0).cloneRange(); });
  function focusEnd() { input.focus(); var s = getSelection(); if (savedRange && input.contains(savedRange.startContainer)) { s.removeAllRanges(); s.addRange(savedRange); return; } var r = document.createRange(); r.selectNodeContents(input); r.collapse(false); s.removeAllRanges(); s.addRange(r); }
  function syncEmpty() { var empty = !input.textContent.replace(/ /g, ' ').trim() && !input.querySelector('[data-m],[data-r]'); input.classList.toggle('empty', empty); if (empty && input.innerHTML !== '' && !input.querySelector('[data-m],[data-r]')) input.innerHTML = ''; }
  function caretInfo() {
    var s = getSelection(); if (!s.rangeCount) return null; var r = s.getRangeAt(0); if (!r.collapsed) return null;
    var n = r.startContainer; if (n.nodeType !== 3 || !input.contains(n)) return null;
    var before = n.textContent.slice(0, r.startOffset), m = before.match(/(^|[\s ])([@#])([^\s @#]{0,30})$/); if (!m) return null;
    return { node: n, start: r.startOffset - 1 - m[3].length, end: r.startOffset, trig: m[2], q: m[3], rect: r.getBoundingClientRect() };
  }
  var AC = null; // { trig, q, items, i, tab }
  function acItems(trig, q, tab) {
    var nq = norm(q);
    if (trig === '@') {
      var L = PEOPLE.filter(function (p) { return p.n !== ME && (!nq || norm(p.n).indexOf(nq) >= 0 || p.code.indexOf(nq) >= 0); }).map(function (p) { return { m: p.n, p: p }; });
      if (!nq || 'tat ca'.indexOf(nq) === 0 || 'all'.indexOf(nq) === 0) L.unshift({ m: '*' });
      return L;
    }
    return Object.keys(OBJ).filter(function (k) { var o = OBJ[k]; if (o.lock) return false; if (tab === 't' && o.k !== 't') return false; if (tab === 'i' && o.k !== 'i') return false; return !nq || norm(o.n + ' ' + o.code).indexOf(nq) >= 0; }).map(function (k) { return { r: k }; });
  }
  function acRender() {
    var ci = caretInfo(); if (!ci) return closeAC();
    var items = acItems(ci.trig, ci.q, AC && AC.trig === '#' ? AC.tab : 'all');
    if (!AC || AC.trig !== ci.trig) AC = { trig: ci.trig, tab: 'all', i: 0 };
    AC.q = ci.q; AC.items = items; if (AC.i >= items.length) AC.i = 0;
    var h;
    if (ci.trig === '@') {
      h = '<div class="hd"><span>Nhắc tên thành viên' + (ci.q ? ' · “' + esc(ci.q) + '”' : '') + '</span><span class="kb">↑↓ chọn · Enter chèn · Esc đóng</span></div><div class="ls">' +
        (items.length ? items.map(function (it, i) { return it.m === '*' ? '<div class="it' + (i === AC.i ? ' on' : '') + '" data-i="' + i + '"><span class="cx-av sm" style="background:#1abc9c"><i class="ri-team-line"></i></span><div class="nm"><div><b>@Tất cả</b></div><small>Báo cho cả ' + D.total + ' thành viên của ' + (D.kin ? 'dự án' : 'phòng') + '</small></div></div>' : '<div class="it' + (i === AC.i ? ' on' : '') + '" data-i="' + i + '">' + av(it.p.n, 'sm', it.p.on) + '<div class="nm"><div>' + esc(it.p.n) + '</div><small>' + esc(it.p.r) + ' · ' + it.p.dep + ' · ' + it.p.code + '</small></div></div>'; }).join('') : '<div class="em">Không có thành viên khớp “' + esc(ci.q) + '”.<br>Chỉ nhắc được người trong ' + 'không gian này' + '.</div>') + '</div>';
    } else {
      h = '<div class="hd"><span class="tabs">' + [['all', 'Tất cả'], ['t', 'Nhiệm vụ'], ['i', 'Vấn đề']].map(function (t) { return '<span class="' + (AC.tab === t[0] ? 'on' : '') + '" data-tab="' + t[0] + '">' + t[1] + '</span>'; }).join('') + '</span><span class="kb">Tab đổi nhóm · Enter chèn</span></div><div class="ls">' +
        (items.length ? items.map(function (it, i) { var o = OBJ[it.r]; return '<div class="it' + (i === AC.i ? ' on' : '') + '" data-i="' + i + '"><i class="' + (o.k === 't' ? 'ri-task-line' : 'ri-bug-line') + '" style="color:' + (o.k === 't' ? '#2563eb' : '#d97706') + '"></i><div class="nm"><div>' + esc(o.n) + '</div><small>' + esc(o.code) + ' · ' + esc(o.as || '') + '</small></div>' + badge(o.st) + '</div>'; }).join('') : '<div class="em">Không tìm thấy việc khớp “' + esc(ci.q) + '”</div>') + '</div>' +
        '<div class="ft"><a data-new="t"><i class="ri-add-line"></i> Tạo nhiệm vụ mới</a><a data-new="i"><i class="ri-add-line"></i> Tạo vấn đề mới</a><span class="kb" style="margin-left:auto">Chỉ hiện việc bạn được xem</span></div>';
    }
    var el = openPop(h, { left: ci.rect.left, right: ci.rect.right, top: input.getBoundingClientRect().top, bottom: ci.rect.bottom, getBoundingClientRect: null }, { up: true, kind: 'ac', cls: '' });
    el.style.width = (ci.trig === '@' ? 340 : 440) + 'px';
    var r = input.getBoundingClientRect(); el.style.top = (r.top - el.offsetHeight - 6) + 'px';
    el.style.left = Math.max(8, Math.min(ci.rect.left - 10, window.innerWidth - el.offsetWidth - 8)) + 'px';
    el.addEventListener('click', function (e) {
      var tab = e.target.closest('[data-tab]'); if (tab) { AC.tab = tab.dataset.tab; AC.i = 0; acRender(); return; }
      var nw = e.target.closest('[data-new]'); if (nw) { var c = caretInfo(); if (c) { c.node.textContent = c.node.textContent.slice(0, c.start) + c.node.textContent.slice(c.end); } closeAC(); openQC(nw.dataset.new, null); return; }
      var it = e.target.closest('.it'); if (it) { AC.i = +it.dataset.i; acPick(); }
    });
  }
  function closeAC() { if (POP && POP.kind === 'ac') closePop(); AC = null; }
  function chipHtml(seg) {
    if (seg.m) return '<span class="cx-chip-at" contenteditable="false" data-m="' + esc(seg.m) + '">@' + esc(seg.m === '*' ? 'Tất cả' : seg.m) + '</span>';
    var o = OBJ[seg.r]; return '<span class="cx-chip-ref" contenteditable="false" data-r="' + seg.r + '"><i class="' + (o.k === 't' ? 'ri-task-line' : 'ri-bug-line') + '"></i>' + esc(o.code) + '</span>';
  }
  function acPick() {
    var ci = caretInfo(); if (!ci || !AC || !AC.items.length) return closeAC();
    var it = AC.items[AC.i];
    var n = ci.node, after = n.splitText(ci.start); after.textContent = after.textContent.slice(ci.end - ci.start);
    var tmp = document.createElement('span'); tmp.innerHTML = chipHtml(it); var chip = tmp.firstChild;
    n.parentNode.insertBefore(chip, after);
    var sp = document.createTextNode(' '); n.parentNode.insertBefore(sp, after);
    var r = document.createRange(); r.setStart(sp, 1); r.collapse(true); var s = getSelection(); s.removeAllRanges(); s.addRange(r);
    closeAC(); syncEmpty();
  }
  function insertText(t) { focusEnd(); document.execCommand('insertText', false, t); syncEmpty(); }
  input.addEventListener('input', function () { syncEmpty(); if (caretInfo()) acRender(); else closeAC(); });
  input.addEventListener('keydown', function (e) {
    if (AC && POP && POP.kind === 'ac') {
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); var n = AC.items.length || 1; AC.i = (AC.i + (e.key === 'ArrowDown' ? 1 : n - 1)) % n; acRender(); return; }
      if (e.key === 'Enter' || (e.key === 'Tab' && AC.trig === '@')) { e.preventDefault(); acPick(); return; }
      if (e.key === 'Tab' && AC.trig === '#') { e.preventDefault(); AC.tab = { all: 't', t: 'i', i: 'all' }[AC.tab]; AC.i = 0; acRender(); return; }
      if (e.key === 'Escape') { e.preventDefault(); closeAC(); return; }
    }
    if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); send(); return; }
    if (e.key === 'Escape') { if (S.edit || S.reply) { e.preventDefault(); clearCtx(); } return; }
    if (e.key === 'ArrowUp' && input.classList.contains('empty')) { var mine = MSG.filter(function (m) { return m.w === ME && !m.rec && in24(m); }).pop(); if (mine) { e.preventDefault(); startEdit(mine.id); } }
  });
  input.addEventListener('paste', function (e) {
    var cd = e.clipboardData; if (!cd) return;
    if (cd.files && cd.files.length) { e.preventDefault(); addFiles(cd.files); return; }
    e.preventDefault(); document.execCommand('insertText', false, cd.getData('text/plain'));
  });
  input.addEventListener('blur', function () { setTimeout(function () { if (POP && POP.kind === 'ac' && !POP.el.matches(':hover')) closeAC(); }, 150); });
  function serialize() {
    var segs = [];
    function push(t) { if (!t) return; if (typeof segs[segs.length - 1] === 'string') segs[segs.length - 1] += t; else segs.push(t); }
    (function walk(n) { [].forEach.call(n.childNodes, function (c) { if (c.nodeType === 3) push(c.textContent.replace(/ /g, ' ')); else if (c.dataset && c.dataset.m) segs.push({ m: c.dataset.m }); else if (c.dataset && c.dataset.r) segs.push({ r: c.dataset.r }); else if (c.nodeName === 'BR') push('\n'); else { if ((c.nodeName === 'DIV' || c.nodeName === 'P') && segs.length) push('\n'); walk(c); } }); })(input);
    if (typeof segs[0] === 'string') segs[0] = segs[0].replace(/^\s+/, ''); var l = segs.length - 1; if (typeof segs[l] === 'string') segs[l] = segs[l].replace(/\s+$/, '');
    return segs.map(function (s) { return typeof s === 'string' ? s.replace(/[ \t]{2,}/g, ' ') : s; }).filter(function (s) { return s !== ''; });
  }
  function loadSegs(segs) { input.innerHTML = segs.map(function (s) { return typeof s === 'string' ? esc(s).replace(/\n/g, '<br>') : chipHtml(s); }).join(''); syncEmpty(); }

  // ---------- trả lời / sửa ----------
  function setCtx(kind, m) {
    var c = $('.cx-ctx'); c.hidden = false; c.className = 'cx-ctx' + (kind === 'edit' ? ' edit' : '');
    c.innerHTML = '<i class="' + (kind === 'edit' ? 'ri-edit-line' : 'ri-reply-line') + '"></i><div class="tx">' + (kind === 'edit' ? '<b>Đang sửa tin nhắn</b> · Enter lưu, Esc hủy' : 'Trả lời <b>' + esc(m.w === ME ? 'chính bạn' : m.w) + '</b>: ' + esc(segText(m.segs).slice(0, 100) || '[File]')) + '</div><i class="ri-close-line x" data-act="ctxx"></i>';
  }
  function clearCtx() { if (S.edit) { input.innerHTML = ''; syncEmpty(); } S.reply = null; S.edit = null; $('.cx-ctx').hidden = true; }
  function startReply(id) { S.edit = null; S.reply = id; setCtx('reply', byId(id)); focusEnd(); }
  function startEdit(id) { var m = byId(id); S.reply = null; S.edit = id; setCtx('edit', m); loadSegs(m.segs); savedRange = null; focusEnd(); }

  // ---------- file ----------
  var fileIn = $('.cx-file-in');
  fileIn.addEventListener('change', function () { addFiles(fileIn.files); fileIn.value = ''; });
  function addFiles(list) {
    [].forEach.call(list, function (f) {
      var a = { id: 'a' + Math.random().toString(36).slice(2), n: f.name || 'anh-dan.png', s: f.size, url: /^image\//.test(f.type) ? URL.createObjectURL(f) : '', pct: 0, err: f.size > 50 * 1048576 ? 'Vượt quá 50 MB — không gửi được' : '' };
      S.att.push(a);
      if (!a.err) var tm = setInterval(function () { a.pct = Math.min(100, a.pct + 18 + Math.random() * 20); renderAtt(); if (a.pct >= 100) clearInterval(tm); }, 140);
    });
    renderAtt(); input.focus();
  }
  function renderAtt() {
    $('.cx-atts').innerHTML = S.att.map(function (a) { var x = fic(a.n); return '<div class="cx-att' + (a.err ? ' err' : '') + '">' + (a.url ? '<img src="' + a.url + '">' : '<i class="' + x[0] + '" style="color:' + x[1] + '"></i>') + '<div><b>' + esc(a.n) + '</b><small>' + (a.err || (a.pct < 100 ? 'Đang tải lên ' + Math.round(a.pct) + '%' : fsize(a.s) + ' · sẵn sàng gửi')) + '</small></div><i class="ri-close-line x" data-act="rmatt" data-id="' + a.id + '" data-tip="Bỏ file"></i>' + (a.err ? '' : '<span class="pg" style="width:' + (a.pct < 100 ? a.pct : 0) + '%"></span>') + '</div>'; }).join('');
  }
  var dragN = 0;
  main.addEventListener('dragenter', function (e) { if ([].indexOf.call(e.dataTransfer.types, 'Files') < 0) return; dragN++; main.classList.add('dragging'); });
  main.addEventListener('dragover', function (e) { if ([].indexOf.call(e.dataTransfer.types, 'Files') >= 0) e.preventDefault(); });
  main.addEventListener('dragleave', function () { if (--dragN <= 0) { dragN = 0; main.classList.remove('dragging'); } });
  main.addEventListener('drop', function (e) { e.preventDefault(); dragN = 0; main.classList.remove('dragging'); if (e.dataTransfer.files.length) addFiles(e.dataTransfer.files); });

  // ---------- gửi ----------
  function send() {
    var segs = serialize();
    var hasText = segText(segs).trim().length > 0;
    if (S.att.some(function (a) { return !a.err && a.pct < 100; })) { toast('<i class="ri-upload-cloud-2-line"></i> Đang tải file lên, gửi lại sau giây lát'); return; }
    var files = S.att.filter(function (a) { return !a.err; }).map(function (a) { return { n: a.n, s: a.s, url: a.url }; });
    if (!hasText && !files.length) return;
    if (S.edit) { var m = byId(S.edit); m.segs = segs; m.ed = 1; clearCtx(); input.innerHTML = ''; syncEmpty(); render({ keep: true }); toast('<i class="ri-edit-line"></i> Đã sửa tin nhắn'); return; }
    var msg = addMsg({ w: ME, segs: segs, files: files, re: S.reply }, { bottom: true });
    S.unread = null; S.att = []; renderAtt(); input.innerHTML = ''; syncEmpty(); clearCtx(); render({ bottom: true });
    setTimeout(function () { msg.seen = 2; render({ keep: true }); }, 1500);
    setTimeout(function () { msg.seen = Math.min(D.total - 1, 5); render({ keep: true }); }, 4000);
    var ments = segs.filter(function (s) { return s.m && s.m !== '*'; });
    if (ments.length) toast('<i class="ri-at-line"></i> Đã báo ' + ments.map(function (s) { return s.m; }).join(', ') + ' (đếm chưa đọc + đẩy app, không bật chuông)');
  }

  // ---------- modal ----------
  function modal(o) {
    var lay = document.createElement('div'); lay.className = 'cx-layer' + (o.cls ? ' ' + o.cls : '');
    lay.innerHTML = '<div class="modal fade show" style="display:block;z-index:2050" role="dialog"><div class="modal-dialog ' + (o.size || 'modal-lg') + '"><div class="modal-content shadow">' +
      (o.confirm ? '' : '<header class="modal-header"><div data-v-d092afda="" class="d-flex align-items-center v2-modal-head-left" style="min-width:0"><div data-v-d092afda="" class="v2-modal-icon mr-2" style="background:' + (o.bg || 'rgba(26,188,156,.1)') + ';color:' + (o.color || '#1abc9c') + '"><i class="' + o.icon + '" style="font-size:16px"></i></div><div data-v-d092afda="" class="v2-modal-heading" style="min-width:0"><h5 data-v-d092afda="" class="modal-title mb-0 d-flex align-items-center" style="font-size:14px;font-weight:800;gap:8px;min-width:0"><span>' + o.title + '</span></h5>' + (o.sub ? '<div class="cx-msub">' + o.sub + '</div>' : '') + '</div></div><button data-v-d092afda="" type="button" class="close" data-x="1"><span aria-hidden="true">×</span></button></header>') +
      '<div class="modal-body v2-modal-wrap"><div data-v-d092afda="" class="v2-modal-body" style="max-height:calc(100vh - 220px)">' + o.body + '</div></div><div data-v-d092afda="" class="modal-footer v2-modal-footer">' + o.foot + '</div></div></div></div><div class="modal-backdrop show" style="z-index:2040"></div>';
    document.body.appendChild(lay);
    function close() { lay.remove(); document.removeEventListener('keydown', k); }
    function k(e) { if (e.key === 'Escape' && !POP) close(); }
    document.addEventListener('keydown', k);
    lay.addEventListener('click', function (e) { if (e.target.closest('[data-x]')) close(); });
    lay.close = close;
    var f = lay.querySelector('input:not([readonly]),textarea'); if (f) setTimeout(function () { f.focus(); if (f.select && o.selectFirst) f.select(); }, 30);
    return lay;
  }
  function confirmBox(o, ok) {
    var lay = modal({ confirm: 1, size: 'modal-sm', cls: 'cx-confirm', body: '<div class="ic" style="background:' + (o.bg || '#fef2f2') + ';color:' + (o.color || '#dc2626') + '"><i class="' + o.icon + '"></i></div><h5>' + o.title + '</h5><p>' + o.text + '</p>', foot: btn(o.ok, o.okIcon, 'primary', o.status || 'danger', 'data-ok="1" class="mr-2"') + btn('Hủy', 'fas fa-arrow-left', 'tertiary', 'info', 'data-x="1"') });
    lay.querySelector('[data-ok]').addEventListener('click', function () { lay.close(); ok(); });
  }
  function lab(t, req, tip) { return '<label data-v-3e7045fc="" class="v2-label v2-label--sm"><span data-v-3e7045fc="" class="v2-label__text"> ' + t + ' ' + (req ? '<span data-v-441a3978="" class="required" data-v-3e7045fc="">*</span>' : '') + '</span>' + (tip ? ' <i class="ri-information-line" style="font-size:14px;color:#94a3b8" data-tip="' + esc(tip) + '"></i>' : '') + '</label>'; }
  function fInput(name, label, req, val, col, ph, extra) { return '<div class="' + col + ' mb-2 cx-fe" data-f="' + name + '">' + lab(label, req) + '<div class="v2-input__wrapper"><input type="text" class="v2-input v2-input--sm" name="' + name + '" value="' + esc(val || '') + '" placeholder="' + esc(ph || '') + '" ' + (extra || '') + '></div>' + (extra === 'readonly' ? '' : '') + '<div class="cx-err"></div></div>'; }
  function fDate(name, label, req, val, col) { return '<div class="' + col + ' mb-2 cx-fe" data-f="' + name + '">' + lab(label, req) + '<div class="v2-input__wrapper"><input type="text" class="v2-input v2-input--sm" name="' + name + '" value="' + esc(val || '') + '" placeholder="dd/mm/yyyy"></div><div class="cx-qd" data-for="' + name + '"><span data-d="0">Hôm nay</span><span data-d="1">Ngày mai</span><span data-d="fri">Thứ 6 này</span><span data-d="7">+1 tuần</span></div><div class="cx-err"></div></div>'; }
  function fText(name, label, req, val, col, rows) { return '<div class="' + col + ' mb-2 cx-fe" data-f="' + name + '">' + lab(label, req) + '<textarea class="form-control v2-textarea v2-textarea--sm" name="' + name + '" rows="' + (rows || 3) + '" style="resize:vertical;min-height:' + ((rows || 3) * 24 + 12) + 'px">' + esc(val || '') + '</textarea><div class="cx-err"></div></div>'; }
  function fPerson(name, label, req, val, col, help) { return '<div class="' + col + ' mb-2 cx-fe" data-f="' + name + '">' + lab(label, req) + '<div class="v2-select v2-select--sm cx-sel" data-person="' + name + '" data-val="' + esc(val || '') + '"><span class="select2 select2-container select2-container--default" style="width:100%"><span class="selection"><span class="select2-selection select2-selection--single">' + '<span class="select2-selection__rendered">' + (val ? esc(plabel(val)) : '<span class="select2-selection__placeholder">Chọn ' + label.toLowerCase() + '</span>') + '</span><span class="select2-selection__arrow"><b></b></span></span></span></span></div>' + (help ? '<div class="cx-help">' + help + '</div>' : '') + '<div class="cx-err"></div></div>'; }
  function fRadio(name, label, opts, val, col) { return '<div class="' + col + ' mb-2 cx-fe" data-f="' + name + '">' + lab(label) + '<div class="pt-1">' + opts.map(function (o, i) { var id = 'cxr' + name + i; return '<div class="custom-control custom-radio custom-control-inline"><input type="radio" class="custom-control-input" name="' + name + '" id="' + id + '" value="' + o + '"' + (o === val ? ' checked' : '') + '><label class="custom-control-label" for="' + id + '">' + o + '</label></div>'; }).join('') + '</div></div>'; }
  function wireForm(lay) {
    lay.querySelectorAll('.cx-qd span').forEach(function (s) { s.addEventListener('click', function () { var d = new Date(TODAY), v = s.dataset.d; if (v === 'fri') d.setDate(d.getDate() + ((5 - d.getDay() + 7) % 7 || 7)); else d.setDate(d.getDate() + +v); var inp = lay.querySelector('input[name="' + s.parentNode.dataset.for + '"]'); inp.value = dmy(d); inp.dispatchEvent(new Event('input')); }); });
    lay.querySelectorAll('[data-person]').forEach(function (sel) {
      sel.addEventListener('click', function () {
        var list = PEOPLE.slice();
        var el = openPop('<div style="padding:8px;border-bottom:1px solid #f1f5f9"><input class="v2-input v2-input--sm" placeholder="Gõ tên hoặc mã nhân viên" style="width:100%"></div><div class="ls"></div>', sel, { kind: 'menu' });
        el.style.width = sel.offsetWidth + 'px'; el.style.zIndex = 2100;
        var q = el.querySelector('input'), ls = el.querySelector('.ls');
        function draw() { var nq = norm(q.value); ls.innerHTML = list.filter(function (p) { return !nq || norm(p.n).indexOf(nq) >= 0 || p.code.indexOf(nq) >= 0; }).map(function (p) { return '<div class="it" data-n="' + esc(p.n) + '">' + av(p.n, 'sm', p.on) + '<div class="nm"><div>' + esc(plabel(p.n)) + (p.n === ME ? ' (bạn)' : '') + '</div><small>' + esc(p.r) + '</small></div></div>'; }).join('') || '<div class="em">Không có nhân viên khớp</div>'; }
        draw(); q.addEventListener('input', draw); setTimeout(function () { q.focus(); }, 10);
        ls.addEventListener('click', function (e) { var it = e.target.closest('.it'); if (!it) return; sel.dataset.val = it.dataset.n; sel.querySelector('.select2-selection__rendered').textContent = plabel(it.dataset.n); sel.closest('.cx-fe').classList.remove('cx-bad'); closePop(); });
      });
    });
    lay.querySelectorAll('input,textarea').forEach(function (i) { i.addEventListener('input', function () { var fe = i.closest('.cx-fe'); if (fe) fe.classList.remove('cx-bad'); }); });
  }
  function val(lay, n) { var p = lay.querySelector('[data-person="' + n + '"]'); if (p) return p.dataset.val; var r = lay.querySelector('input[name="' + n + '"]:checked'); if (r) return r.value; var e = lay.querySelector('[name="' + n + '"]'); return e ? e.value.trim() : ''; }
  function bad(lay, n, msg) { var fe = lay.querySelector('[data-f="' + n + '"]'); fe.classList.add('cx-bad'); fe.querySelector('.cx-err').textContent = msg; }
  function validate(lay, req, draft) {
    lay.querySelectorAll('.cx-fe').forEach(function (f) { f.classList.remove('cx-bad'); });
    var ok = true;
    (draft ? req.slice(0, 1) : req).forEach(function (n) { if (!val(lay, n)) { bad(lay, n, 'Bắt buộc phải nhập'); ok = false; } });
    lay.querySelectorAll('.cx-qd').forEach(function (q) { var n = q.dataset.for, v = val(lay, n); if (v && !pdate(v)) { bad(lay, n, 'Không hợp lệ'); ok = false; } });
    var s = pdate(val(lay, 'start')), d = pdate(val(lay, 'due')); if (s && d && d < s) { bad(lay, 'due', 'Hạn phải từ ngày bắt đầu trở đi'); ok = false; }
    ['hrs', 'act_hrs'].forEach(function (n) { var v = val(lay, n); if (v && !(+v > 0)) { bad(lay, n, 'Không hợp lệ'); ok = false; } });
    var p = val(lay, 'pct'); if (p && !(+p >= 0 && +p <= 100)) { bad(lay, 'pct', 'Không được lớn hơn 100.'); ok = false; }
    if (!ok) { var f = lay.querySelector('.cx-bad'); f && f.scrollIntoView({ block: 'nearest' }); }
    return ok;
  }

  // ---------- tạo nhanh nhiệm vụ / vấn đề ----------
  var seq = { t: 160, i: 12 };
  function openQC(k, srcId) {
    var src = srcId ? byId(srcId) : null, t = k === 't';
    var text = src ? segText(src.segs).replace(/@\S+(\s\S+){0,3}?\s/, '').trim() : segText(serialize()).trim();
    var firstM = src ? (src.segs.filter(function (s) { return s.m && s.m !== '*' && s.m !== src.w; })[0] || {}).m : (serialize().filter(function (s) { return s.m && s.m !== '*'; })[0] || {}).m;
    var name = (src ? segText(src.segs) : text).replace(/@(Tất cả|[A-ZĐÂĂÊÔƠƯ][^\s]*(\s[A-ZĐÂĂÊÔƠƯ][^\s,.:]*){0,3})/g, '').replace(/#\S+/g, '').replace(/\s+/g, ' ').replace(/^[\s,.:-]+|[\s,.:-]+$/g, '');
    var first = name.split(/(?<=[.?!])\s/)[0].replace(/[.!]+$/, ''); if (first.length >= 12) name = first;
    name = name.charAt(0).toUpperCase() + name.slice(1);
    if (name.length > 120) name = name.slice(0, 117) + '…';
    var srcLine = src ? '<div class="cx-src"><i class="ri-chat-quote-line"></i> Tạo từ tin nhắn của <b>' + esc(src.w === ME ? 'bạn' : src.w) + '</b> lúc ' + src.t + ' ' + src.d.toLowerCase() + ': “' + esc(segText(src.segs).slice(0, 160)) + '”' + (src.files.length ? ' · ' + src.files.length + ' file' : '') + '</div>' : '';
    var assignee = firstM || (src && src.w !== ME ? src.w : '');
    var bodyH = srcLine + '<div class="form-row">' +
      fInput('n', t ? 'Tên công việc' : 'Tiêu đề vấn đề', true, name, 'col-md-12', t ? 'Nhập tên công việc' : 'Nhập tiêu đề vấn đề') +
      (t ? fPerson('as', 'Người thực hiện', true, assignee, 'col-md-6', firstM ? 'Điền sẵn theo người được @ trong tin nhắn' : '') + fPerson('ap', 'Người duyệt kết quả', false, ME, 'col-md-6')
         : fPerson('as', 'Người xử lý', false, assignee, 'col-md-6', 'Bỏ trống: vấn đề ở trạng thái Mới ghi nhận, Quản lý phân công sau') + fPerson('rp', 'Người báo', true, src ? src.w : ME, 'col-md-6')) +
      (t ? fDate('start', 'Ngày bắt đầu', true, dmy(TODAY), 'col-md-4') + fDate('due', 'Hạn hoàn thành', true, '', 'col-md-4') + fInput('time', 'Giờ hạn', true, '17:00', 'col-md-2', 'hh:mm') + fInput('hrs', 'Số giờ được giao', true, '4', 'col-md-2')
         : fDate('due', 'Hạn xử lý', true, '', 'col-md-6') + fRadio('pr', 'Mức độ ưu tiên', ['Bình thường', 'Cao', 'Khẩn cấp'], 'Bình thường', 'col-md-6')) +
      (t ? fRadio('pr', 'Mức độ ưu tiên', ['Bình thường', 'Cao', 'Khẩn cấp'], 'Bình thường', 'col-md-6') + '<div class="col-md-6 mb-2">' + lab('Không gian làm việc') + '<div class="v2-input__wrapper"><input class="v2-input v2-input--sm" value="' + esc(D.title) + '" disabled></div></div>' : '') +
      fText('desc', 'Mô tả', false, src ? 'Từ trao đổi: “' + segText(src.segs) + '”' : '', 'col-md-12', 3) +
      (src && src.files.length ? '<div class="col-md-12 mb-2"><label class="cx-chk" data-chk="1"><i class="ri-checkbox-line"></i>Đính kèm ' + src.files.length + ' file của tin nhắn (' + esc(src.files.map(function (f) { return f.n; }).join(', ')) + ')</label></div>' : '') +
      '<div class="col-md-12"><div class="cx-help"><i class="ri-information-line"></i> ' + (t ? 'Tạo xong: thẻ nhiệm vụ gắn vào trao đổi, người thực hiện nhận thông báo; mở panel chi tiết để thêm Checklist, Người theo dõi, Lặp lại…' : 'Tạo xong: thẻ vấn đề gắn vào trao đổi, người xử lý nhận thông báo.') + '</div></div></div>';
    var lay = modal({ icon: t ? 'ri-task-line' : 'ri-bug-line', color: t ? '#1abc9c' : '#d97706', bg: t ? 'rgba(26,188,156,.1)' : 'rgba(217,119,6,.1)', title: t ? 'Tạo nhiệm vụ' : 'Tạo vấn đề', sub: (src ? 'Từ tin nhắn trong ' : 'Trong ') + esc(D.ctx.toLowerCase() + ' ' + D.title), body: bodyH, selectFirst: !name,
      foot: (t ? btn('Lưu nháp', 'ri-save-3-line', 'secondary', 'info', 'data-draft="1" class="mr-2 mb-2"') : '') + btn(t ? 'Tạo nhiệm vụ' : 'Tạo vấn đề', 'ri-save-3-line', 'primary', 'info', 'data-ok="1"') + btn('Đóng', 'fas fa-arrow-left', 'tertiary', 'info', 'data-x="1"') });
    wireForm(lay);
    var chk = lay.querySelector('[data-chk]'); if (chk) chk.addEventListener('click', function (e) { e.preventDefault(); var i = chk.querySelector('i'); i.className = i.className === 'ri-checkbox-line' ? 'ri-checkbox-blank-line' : 'ri-checkbox-line'; });
    function submit(draft) {
      var req = t ? ['n', 'as', 'start', 'due', 'time', 'hrs'] : ['n', 'rp', 'due'];
      if (!validate(lay, req, draft)) return;
      var id = (t ? 'N' : 'J') + (++seq[k]);
      var o = { k: k, code: t ? 'TPE.TASK.NB.26.0' + seq.t : 'ISS-202611-' + ('000' + seq.i).slice(-4), n: val(lay, 'n'), as: val(lay, 'as'), due: val(lay, 'due'), pr: val(lay, 'pr') === 'Bình thường' ? '' : val(lay, 'pr') };
      if (t) { o.ap = val(lay, 'ap') || ME; o.pct = 0; o.hrs = +val(lay, 'hrs') || 0; o.st = draft ? 'Nháp' : 'Chờ bắt đầu'; } // L3: trạng thái sau khi tạo (Chờ bắt đầu hay Chờ phê duyệt triển khai) — chờ user chốt
      else { o.rp = val(lay, 'rp'); o.st = o.as ? 'Đã phân công' : 'Mới ghi nhận'; }
      OBJ[id] = o; lay.close();
      if (src) src.made.push(id);
      if (draft) { render({ keep: true }); S.side = 'viec'; renderSide(); toast('<i class="ri-save-3-line"></i> Đã lưu nháp ' + o.code + ' — chỉ bạn thấy, chưa báo vào nhóm'); return; }
      var who = '<b>Bạn</b>';
      var h = who + ' đã tạo ' + (t ? 'nhiệm vụ' : 'vấn đề') + ' {o}' + (src ? ' từ tin nhắn của <b>' + esc(src.w === ME ? 'bạn' : src.w) + '</b>' : '') + (o.as ? ' · ' + (t ? 'giao' : 'phân công') + ' <b>' + esc(o.as === ME ? 'bạn' : o.as) + '</b>' : '');
      var m = announce('assign', h, id, { card: 1 });
      if (!m) { addMsg({ w: ME, segs: [{ r: id }] }, { bottom: true }); }
      render({ bottom: true }); pulse(id);
      toast('<i class="ri-checkbox-circle-line"></i> Đã tạo ' + o.code + (o.as && o.as !== ME ? ' · đã báo ' + esc(o.as) : ''));
    }
    lay.querySelector('[data-ok]').addEventListener('click', function () { submit(false); });
    var dr = lay.querySelector('[data-draft]'); if (dr) dr.addEventListener('click', function () { submit(true); });
  }

  // ---------- hành động trên thẻ ----------
  function objAct(op, id) {
    var o = OBJ[id], t = o.k === 't', name = '{o}';
    if (op === 'start') { o.st = 'Đang thực hiện'; if (EVON.start) announce('start', '<b>Bạn</b> đã bắt đầu thực hiện ' + name, id); render(); pulse(id); toast('<i class="ri-play-circle-line"></i> ' + esc(o.code) + ' → Đang thực hiện' + (EVON.start ? '' : ' · không báo vào nhóm (sự kiện “Bắt đầu thực hiện” đang tắt)')); return; }
    if (op === 'submit') {
      var lay = modal({ icon: 'ri-flag-2-line', title: 'Báo kết quả nhiệm vụ', sub: esc(o.code + ' · ' + o.n), size: 'modal-md',
        body: '<div class="form-row">' + '<div class="col-md-4 mb-2">' + lab('Số giờ được giao') + '<div class="v2-input__wrapper"><input class="v2-input v2-input--sm" value="' + (o.hrs || 0) + '" disabled></div></div>' + fInput('act_hrs', 'Số giờ làm thực tế', true, '', 'col-md-4') + fInput('pct', 'Tiến độ (%)', true, '100', 'col-md-4') + fText('res', 'Kết quả thực hiện', true, '', 'col-md-12', 3) +
          '<div class="col-md-12"><div class="cx-help"><i class="ri-information-line"></i> Gửi xong: nhiệm vụ chuyển <b>Hoàn thành - Chờ duyệt</b>, ' + esc(o.ap) + ' nhận thông báo duyệt' + (EVON.submit ? ', nhóm thấy tin “đã báo hoàn thành”.' : '. Sự kiện báo vào nhóm đang tắt.') + '</div></div></div>',
        foot: btn('Gửi kết quả', 'ri-send-plane-2-line', 'primary', 'info', 'data-ok="1" class="mr-2 mb-2"') + btn('Đóng', 'fas fa-arrow-left', 'tertiary', 'info', 'data-x="1"') });
      wireForm(lay);
      lay.querySelector('[data-ok]').addEventListener('click', function () {
        if (!validate(lay, ['act_hrs', 'pct', 'res'])) return;
        o.pct = +val(lay, 'pct'); o.st = 'Hoàn thành - Chờ duyệt'; lay.close();
        announce('submit', '<b>Bạn</b> đã báo hoàn thành nhiệm vụ ' + name + ' · chờ <b>' + esc(o.ap) + '</b> duyệt', id, { card: 1 });
        pulse(id); toast('<i class="ri-flag-2-line"></i> Đã gửi kết quả · mô phỏng: ' + esc(o.ap) + ' duyệt sau vài giây');
        setTimeout(function () { typing(o.ap, 1800, function () {
          o.st = 'Hoàn thành';
          announce('done', '<b>' + esc(o.ap) + '</b> đã duyệt kết quả · nhiệm vụ ' + name + ' <b>hoàn thành</b>', id);
          addMsg({ w: o.ap, segs: [{ m: ME }, ' cảm ơn em, kết quả rõ ràng 👍'], re: null });
          pulse(id);
        }); }, 1600);
      });
      return;
    }
    if (op === 'approve') { o.st = 'Hoàn thành'; announce('done', '<b>Bạn</b> đã duyệt kết quả · nhiệm vụ ' + name + ' <b>hoàn thành</b> · ' + esc(o.as), id); render(); pulse(id); toast('<i class="ri-checkbox-circle-line"></i> Đã duyệt ' + esc(o.code)); return; }
    if (op === 'reject') {
      var lr = modal({ icon: 'ri-close-circle-line', color: '#dc2626', bg: 'rgba(220,38,38,.1)', title: 'Từ chối kết quả', sub: esc(o.code + ' · ' + o.n), size: 'modal-md', body: '<div class="form-row">' + fText('why', 'Lý do từ chối', true, '', 'col-md-12', 3) + '</div>',
        foot: btn('Từ chối', 'ri-close-line', 'primary', 'danger', 'data-ok="1" class="mr-2 mb-2"') + btn('Đóng', 'fas fa-arrow-left', 'tertiary', 'info', 'data-x="1"') });
      wireForm(lr);
      lr.querySelector('[data-ok]').addEventListener('click', function () { if (!validate(lr, ['why'])) return; var why = val(lr, 'why'); o.st = 'Từ chối kết quả'; lr.close(); announce('reject', '<b>Bạn</b> đã từ chối kết quả nhiệm vụ ' + name + ': “' + esc(why.slice(0, 60)) + '”', id, { card: 1 }); pulse(id); });
      return;
    }
    if (op === 'take') { o.st = 'Đang xử lý'; announce('issue', '<b>Bạn</b> đã nhận xử lý vấn đề ' + name, id); render(); pulse(id); return; }
    if (op === 'resolve') { o.st = 'Đã xử lý xong'; announce('issue', '<b>Bạn</b> đã xử lý xong vấn đề ' + name + ' · chờ <b>' + esc(o.rp) + '</b> xác nhận đóng', id, { card: 1 }); pulse(id); return; }
    if (op === 'close') { o.st = 'Đã đóng'; announce('issue', '<b>Bạn</b> đã đóng vấn đề ' + name, id); render(); pulse(id); toast('<i class="ri-checkbox-circle-line"></i> Đã đóng vấn đề ' + esc(o.code)); return; }
    if (op === 'reopen') { o.st = 'Mở lại'; announce('issue', '<b>Bạn</b> đã mở lại vấn đề ' + name, id, { card: 1 }); pulse(id); return; }
  }

  // ---------- 05/11 [U]: người chỉ xem — không gửi / ghim / thả cảm xúc, có nút Xin tham gia ----------
  var ro = document.createElement('div'); ro.className = 'cx-ro'; ro.hidden = true; root.querySelector('.cx-main').appendChild(ro);
  function paintRo() { ro.innerHTML = '<i class="ri-eye-line"></i><span>Bạn chỉ có quyền xem</span>' + (S.req ? '<button type="button" class="cx-joinb wait" data-act="joincancel" data-tip="Bấm để huỷ yêu cầu"><i class="ri-time-line"></i>Đã gửi · chờ duyệt</button>' : '<button type="button" class="cx-joinb" data-act="join"><i class="ri-user-add-line"></i>Xin tham gia</button>'); }
  // 05/11 [U] §3.11 — dự án đã đóng: chỉ đọc với mọi người, dải trên ô soạn + Mở lại (Quản lý nhóm)
  function setClosed(on) { S.closed = on; S.viewer = on; root.classList.toggle('viewer', on); ro.hidden = !on; if (on) { ro.innerHTML = '<i class="ri-archive-line"></i><span><b>Dự án đã đóng ngày 05/11/2026 · Hoàn thành</b> — chỉ xem, không nhắn tin / tạo việc. Dự án đã chuyển vào mục Lưu trữ.</span><button type="button" class="cx-joinb" data-act="reopen"><i class="ri-refresh-line"></i>Mở lại</button>'; var nT = 0, nI = 0; Object.keys(OBJ).forEach(function (k) { var o = OBJ[k]; if (o.lock) return; if (o.k === 'i') { if (['Hoàn thành', 'Đã đóng'].indexOf(o.st) < 0) { o.st = 'Đã đóng'; nI++; } } else if (['Hoàn thành', 'Huỷ', 'Hủy'].indexOf(o.st) < 0) { o.st = 'Huỷ'; nT++; } }); addMsg({ sys: 'member', h: '<b>Bạn</b> đã đóng dự án · <b>Hoàn thành</b>: “Hội nghị đã tổ chức xong.”' + (nT + nI ? ' · ' + (nT ? nT + ' nhiệm vụ chưa xong chuyển Huỷ' : '') + (nT && nI ? ', ' : '') + (nI ? nI + ' vấn đề chuyển Đã đóng' : '') : '') }); } else { paintRo(); addMsg({ sys: 'member', h: '<b>Bạn</b> đã mở lại dự án' }); } }
  function setViewer(on) { S.viewer = on; S.req = false; root.classList.toggle('viewer', on); ro.hidden = !on; paintRo(); toast(on ? '<i class="ri-eye-line"></i> Đang xem như người chỉ xem' : 'Đã trở lại vai trò thành viên'); }

  // ---------- mô phỏng sự kiện của người khác ----------
  function demo(anchor) {
    var room = SP !== 'iproj';
    var items = [{ ti: 'Mô phỏng (chỉ có trong bản demo)' }];
    if (room) {
      items.push({ t: 'Phạm Quốc Huy báo đã xử lý vấn đề máy chấm công', ic: 'ri-bug-line', f: function () { var o = OBJ.I07; if (o.st === 'Đã xử lý xong' || o.st === 'Đã đóng') return toast('Vấn đề này đã xử lý rồi'); typing('Phạm Quốc Huy', 1400, function () { o.st = 'Đã xử lý xong'; announce('issue', '<b>Phạm Quốc Huy</b> đã xử lý xong vấn đề {o} · chờ <b>bạn</b> xác nhận đóng', 'I07', { card: 1 }); addMsg({ w: 'Phạm Quốc Huy', segs: ['Em thay đầu đọc vân tay rồi, chị thử lại giúp em nhé.'] }); pulse('I07'); }); } });
      items.push({ t: 'Nguyễn Thị Hằng giao việc mới cho bạn', ic: 'ri-user-shared-line', f: function () { if (OBJ.T170) return toast('Đã mô phỏng rồi'); typing('Nguyễn Thị Hằng', 1400, function () { OBJ.T170 = { k: 't', code: 'TPE.TASK.NB.26.0170', n: 'Lập kế hoạch khám sức khoẻ định kỳ 2027', st: 'Chờ bắt đầu', as: ME, ap: 'Nguyễn Thị Hằng', due: '20/11/2026', pct: 0, hrs: 8 }; addMsg({ w: 'Nguyễn Thị Hằng', segs: [{ m: ME }, ' em lên kế hoạch khám sức khoẻ năm sau giúp chị nhé '] }); announce('assign', '<b>Nguyễn Thị Hằng</b> đã giao nhiệm vụ {o} cho <b>bạn</b>', 'T170', { card: 1 }); pulse('T170'); }); } });
      items.push({ t: 'Lê Thu Trang báo hoàn thành “Gia hạn hợp đồng vệ sinh”', ic: 'ri-flag-2-line', f: function () { var o = OBJ.T118; if (o.st !== 'Đang thực hiện') return toast('Đã mô phỏng rồi'); o.st = 'Hoàn thành - Chờ duyệt'; o.pct = 100; announce('submit', '<b>Lê Thu Trang</b> đã báo hoàn thành nhiệm vụ {o} · chờ <b>Nguyễn Thị Hằng</b> duyệt', 'T118', { card: 1 }); pulse('T118'); setTimeout(function () { o.st = 'Hoàn thành'; announce('done', '<b>Nguyễn Thị Hằng</b> đã duyệt kết quả · nhiệm vụ {o} <b>hoàn thành</b>', 'T118'); pulse('T118'); }, 3500); } });
      items.push({ t: 'Hệ thống nhắc việc quá hạn (08:00)', ic: 'ri-alarm-warning-line', f: function () { var L = Object.keys(OBJ).filter(function (k) { return !OBJ[k].lock && overdue(OBJ[k]); }); if (!L.length) return toast('Không có việc quá hạn'); announce('overdue', '<b>' + L.length + ' việc quá hạn</b>: ' + L.map(function (k) { return '<a data-act="peek" data-obj="' + k + '">' + esc(OBJ[k].n) + '</a> (' + esc(OBJ[k].as) + ', quá ' + (-daysLeft(OBJ[k])) + ' ngày)'; }).join(', '), null); } });
      items.push({ t: 'Ngô Đức Thịnh vào phòng (đồng bộ phòng ban)', ic: 'ri-user-add-line', f: function () { if (person('Ngô Đức Thịnh')) return toast('Đã mô phỏng rồi'); var j = D.joiner; PEOPLE.push({ n: j[0], r: j[1], dep: j[2], code: j[3], on: j[4] }); D.total++; announce('member', '<b>Ngô Đức Thịnh</b> đã vào phòng · đồng bộ từ phòng ban Nhân Sự Hành Chính', null); } });
    } else {
      items.push({ t: S.closed ? 'Mở lại dự án (Quản lý)' : 'Quản lý đóng dự án (xem trạng thái đã đóng)', ic: 'ri-archive-line', f: function () { setClosed(!S.closed); } });
      items.push({ t: S.viewer ? 'Trở lại vai trò thành viên dự án' : 'Xem như người chỉ xem (không là thành viên dự án)', ic: 'ri-eye-line', f: function () { setViewer(!S.viewer); } });
      items.push({ t: 'Vũ Hoàng Long báo hoàn thành “Đặt hội trường”', ic: 'ri-flag-2-line', f: function () { var o = OBJ.P150; if (o.st !== 'Đang thực hiện') return toast('Đã mô phỏng rồi'); typing('Vũ Hoàng Long', 1400, function () { o.st = 'Hoàn thành - Chờ duyệt'; o.pct = 100; announce('submit', '<b>Vũ Hoàng Long</b> đã báo hoàn thành nhiệm vụ {o} · chờ <b>Trần Văn Minh</b> duyệt', 'P150', { card: 1 }); pulse('P150'); setTimeout(function () { o.st = 'Hoàn thành'; announce('done', '<b>Trần Văn Minh</b> đã duyệt kết quả · nhiệm vụ {o} <b>hoàn thành</b>', 'P150'); pulse('P150'); }, 3500); }); } });
      items.push({ t: 'Trần Văn Minh xử lý xong vấn đề trùng lịch', ic: 'ri-bug-line', f: function () { var o = OBJ.PI1; if (o.st !== 'Đang xử lý') return toast('Đã mô phỏng rồi'); o.st = 'Đã xử lý xong'; announce('issue', '<b>Trần Văn Minh</b> đã xử lý xong vấn đề {o} · chờ <b>Vũ Hoàng Long</b> xác nhận đóng', 'PI1', { card: 1 }); addMsg({ w: 'Trần Văn Minh', segs: ['Anh đổi được sang hội trường tầng 3, sức chứa 250 người.'] }); pulse('PI1'); } });
    }
    items.push('-');
    items.push({ t: 'Có người nhắn tin mới (khi bạn đang cuộn lên)', ic: 'ri-chat-new-line', f: function () { body.scrollTop = 0; var w = room ? 'Bùi Thanh Tâm' : 'Lê Thu Trang'; setTimeout(function () { typing(w, 1200, function () { addMsg({ w: w, segs: [{ m: ME }, ' chị ơi file này em cần ký trước 16h nhé'] }); }); }, 300); } });
    menu(anchor, items, function (it) { it.f(); }, { alignRight: true });
  }

  // ---------- sự kiện click ----------
  root.addEventListener('click', function (e) {
    var a = e.target.closest('[data-act]'); if (!a || !root.contains(a)) return;
    var act = a.dataset.act, id = a.dataset.id;
    switch (act) {
      case 'send': return send();
      case 'attach': return fileIn.click();
      case 'at': case 'hash': { focusEnd(); var c = caretInfo(); var s = getSelection(), r = s.rangeCount ? s.getRangeAt(0) : null, prev = r && r.startContainer.nodeType === 3 ? r.startContainer.textContent.slice(0, r.startOffset) : ''; document.execCommand('insertText', false, (prev && !/[\s ]$/.test(prev) ? ' ' : '') + (act === 'at' ? '@' : '#')); syncEmpty(); acRender(); return; }
      case 'emoji': { var rg = savedRange; var el = openPop('<div class="cx-emo">' + '👍 ❤️ 😂 😮 😢 🙏 👏 🎉 ✅ ❌ ⏰ 📌 🔥 💯 👌 🤝 😊 😅 🤔 👀 💪 🚀 📎 ☕'.split(' ').map(function (x) { return '<span>' + x + '</span>'; }).join('') + '</div>', a, { up: true }); el.addEventListener('click', function (ev) { var sp = ev.target.closest('span'); if (!sp) return; savedRange = rg; insertText(sp.textContent); closePop(); }); return; }
      case 'newobj': return menu(a, [{ t: 'Nhiệm vụ', ic: 'ri-task-line', k: 'giao việc có hạn, có duyệt', v: 't' }, { t: 'Vấn đề', ic: 'ri-bug-line', k: 'sự cố cần xử lý', v: 'i' }], function (it) { openQC(it.v, null); }, { up: true });
      case 'ctxx': return clearCtx();
      case 'rmatt': S.att = S.att.filter(function (x) { return x.id !== id; }); return renderAtt();
      case 'reply': return startReply(id);
      case 'mkobj': return openQC(a.dataset.k, id);
      case 'react': { var m = byId(id), e2 = a.dataset.e; m.rc[e2] = m.rc[e2] || []; var i = m.rc[e2].indexOf(ME); if (i >= 0) m.rc[e2].splice(i, 1); else m.rc[e2].push(ME); return render({ keep: true }); }
      case 'more': {
        var mm = byId(id), mine = mm.w === ME; a.closest('.cx-tools').classList.add('keep');
        var it = [{ t: mm.pin ? 'Bỏ ghim' : 'Ghim tin nhắn', ic: 'ri-pushpin-2-line', v: 'pin' }, { t: 'Trả lời', ic: 'ri-reply-line', v: 'reply' }, { t: 'Tạo nhiệm vụ từ tin này', ic: 'ri-task-line', v: 'mt' }, { t: 'Tạo vấn đề từ tin này', ic: 'ri-bug-line', v: 'mi' }, '-', { t: 'Sao chép nội dung', ic: 'ri-file-copy-line', v: 'copy' }, { t: 'Sao chép liên kết tin nhắn', ic: 'ri-links-line', v: 'link' }];
        if (S.viewer) it = [{ t: 'Sao chép nội dung', ic: 'ri-file-copy-line', v: 'copy' }, { t: 'Sao chép liên kết tin nhắn', ic: 'ri-links-line', v: 'link' }];
        else if (mine && in24(mm)) { it.push('-'); it.push({ t: 'Sửa', ic: 'ri-edit-line', v: 'edit', k: '↑' }); it.push({ t: 'Thu hồi', ic: 'ri-arrow-go-back-line', v: 'rec', dg: 1 }); }
        else if (mine) { it.push('-'); it.push({ ti: 'Quá 24 giờ — không sửa / thu hồi được' }); }
        return menu(a, it, function (x) {
          if (x.v === 'pin') { if (!mm.pin && pinned().length >= 20) return toast('Tối đa 20 tin ghim'); mm.pin = !mm.pin; S.pinIdx = 0; if (mm.pin) addMsg({ sys: 'pin', h: '<b>Bạn</b> đã ghim tin nhắn của <b>' + esc(mm.w === ME ? 'bạn' : mm.w) + '</b>', o: null }); else render({ keep: true }); toast('<i class="ri-pushpin-2-line"></i> ' + (mm.pin ? 'Đã ghim — mọi thành viên thấy ở thanh trên cùng' : 'Đã bỏ ghim')); }
          if (x.v === 'reply') startReply(id);
          if (x.v === 'mt') openQC('t', id);
          if (x.v === 'mi') openQC('i', id);
          if (x.v === 'copy') { try { navigator.clipboard.writeText(segText(mm.segs)); } catch (er) { } toast('<i class="ri-file-copy-line"></i> Đã sao chép nội dung'); }
          if (x.v === 'link') toast('<i class="ri-links-line"></i> Đã sao chép liên kết — mở ra sẽ nhảy tới đúng tin này');
          if (x.v === 'edit') startEdit(id);
          if (x.v === 'rec') confirmBox({ icon: 'ri-arrow-go-back-line', title: 'Thu hồi tin nhắn?', text: 'Mọi thành viên sẽ thấy “Tin nhắn đã được thu hồi”. File đính kèm của tin cũng bị gỡ khỏi trao đổi.', ok: 'Thu hồi', okIcon: 'ri-arrow-go-back-line' }, function () { mm.rec = 1; mm.pin = false; render({ keep: true }); toast('Đã thu hồi tin nhắn'); });
        }, { alignRight: !mine });
      }
      case 'peek': S.peek = a.dataset.obj; return renderSide();
      case 'unpeek': S.peek = null; return renderSide();
      case 'open': return toast('<i class="ri-external-link-line"></i> Mở panel chi tiết ' + esc(OBJ[a.dataset.obj].code) + ' (màn 03 / 19 — U20–U21)');
      case 'oa': e.stopPropagation(); return objAct(a.dataset.op, a.dataset.obj);
      case 'jump': return jump(a.dataset.to);
      case 'pinbar': { if (e.target.closest('[data-act="pinall"]')) { S.side = 'ghim'; S.peek = null; return renderSide(); } var pid = a.dataset.id; jump(pid); S.pinIdx = (S.pinIdx + 1) % Math.max(1, pinned().length); renderPinbar(); return; }
      case 'pinall': S.side = 'ghim'; S.peek = null; return renderSide();
      case 'unpin': e.stopPropagation(); if (S.viewer) return; byId(a.dataset.id).pin = false; S.pinIdx = 0; render({ keep: true }); return toast('<i class="ri-pushpin-2-line"></i> Đã bỏ ghim');
      case 'stab': S.side = a.dataset.t; return renderSide();
      case 'vf': S.vf = a.dataset.f; return renderSide();
      case 'atp': { var n = a.dataset.n; if (n === ME) return; focusEnd(); document.execCommand('insertHTML', false, chipHtml({ m: n }) + '&nbsp;'); syncEmpty(); return; }
      case 'lb': { var mg = byId(id), f = mg.files[+a.dataset.i]; var lb = document.createElement('div'); lb.className = 'cx-lb'; lb.innerHTML = '<img src="' + f.url + '"><div><span>' + esc(f.n) + ' · ' + fsize(f.s) + ' · ' + esc(mg.w === ME ? 'Bạn' : mg.w) + '</span><a data-dl="1"><i class="ri-download-2-line"></i> Tải xuống</a><a>Đóng (Esc)</a></div>'; document.body.appendChild(lb); var k = function (ev) { if (ev.key === 'Escape') { lb.remove(); document.removeEventListener('keydown', k); } }; document.addEventListener('keydown', k); lb.addEventListener('click', function (ev) { if (ev.target.closest('[data-dl]')) toast('<i class="ri-download-2-line"></i> Tải xuống ' + esc(f.n)); lb.remove(); }); return; }
      case 'dl': return toast('<i class="ri-download-2-line"></i> Tải xuống ' + esc(a.dataset.n));
      case 'down': S.below = 0; body.scrollTo({ top: body.scrollHeight, behavior: 'smooth' }); return;
      case 'side': root.classList.toggle('noside'); a.classList.toggle('on'); return;
      case 'demo': return demo(a);
      case 'join': S.req = true; paintRo(); return toast('<i class="ri-user-add-line"></i> Đã gửi yêu cầu tham gia — Quản lý nhóm <b>Trần Văn Minh</b> nhận thông báo');
      case 'reopen': setClosed(false); return toast('<i class="ri-refresh-line"></i> Đã mở lại dự án — mọi thành viên nhận thông báo');
      case 'joincancel': S.req = false; paintRo(); return toast('Đã huỷ yêu cầu tham gia');
      case 'search': return openSearch();
      case 'sclose': return closeSearch();
      case 'sprev': return stepHit(-1);
      case 'snext': return stepHit(1);
      case 'notif': {
        var opts = [['all', 'Tất cả tin nhắn', 'Đếm chưa đọc + đẩy app mọi tin'], ['ment', 'Chỉ khi được @ nhắc tên', 'Và việc giao cho tôi / tôi duyệt'], ['off', 'Tắt', 'Vẫn đếm chưa đọc, không đẩy app']];
        var pel = openPop('<div class="cx-cfg cx-radio"><div class="hd" style="padding:9px 12px"><b style="color:#1f2937;font-size:13px">Thông báo của tôi</b><span>chỉ áp cho bạn</span></div>' + opts.map(function (o) { return '<div class="row' + (S.notif === o[0] ? ' on' : '') + '" data-v="' + o[0] + '"><i class="' + (S.notif === o[0] ? 'ri-radio-button-fill' : 'ri-checkbox-blank-circle-line') + '"></i><div class="nm">' + o[1] + '<small>' + o[2] + '</small></div></div>'; }).join('') + '<div class="note"><i class="ri-information-line"></i> Tin trao đổi <b>không bật chuông thông báo</b>: chỉ hiện số chưa đọc ở nút Trao đổi, danh sách không gian và đẩy về app.</div></div>', a, { alignRight: true });
        pel.addEventListener('click', function (ev) { var r2 = ev.target.closest('.row'); if (!r2) return; S.notif = r2.dataset.v; closePop(); a.classList.toggle('on', S.notif !== 'all'); a.querySelector('i').className = S.notif === 'off' ? 'ri-notification-off-line' : 'ri-notification-3-line'; toast('<i class="ri-notification-3-line"></i> Thông báo: ' + opts.filter(function (o) { return o[0] === S.notif; })[0][1]); });
        return;
      }
      case 'auto': {
        var ael = openPop('<div class="cx-cfg"><div class="hd" style="padding:9px 12px"><b style="color:#1f2937;font-size:13px">Tự báo vào nhóm</b><span>áp cho cả ' + (D.kin ? 'dự án' : 'phòng') + '</span></div>' + EV.map(function (ev) { return '<div class="row"><div class="nm">' + ev[1] + (ev[2] ? '<small>' + ev[2] + '</small>' : '') + '</div><span class="cx-sw' + (EVON[ev[0]] ? ' on' : '') + '" data-ev="' + ev[0] + '"></span></div>'; }).join('') + '<div class="note"><i class="ri-information-line"></i> Sự kiện của nhiệm vụ / vấn đề thuộc ' + (D.kin ? 'dự án' : 'phòng') + ' này tự sinh tin hệ thống vào trao đổi. Chỉ <b>Quản lý ' + (D.kin ? 'dự án' : 'phòng') + '</b> sửa được (cũng có ở tab Cấu hình) — bản demo cho bật / tắt để thử.</div></div>', a, { alignRight: true });
        ael.addEventListener('click', function (ev) { var sw = ev.target.closest('.cx-sw'); if (!sw) return; var k2 = sw.dataset.ev; EVON[k2] = !EVON[k2]; sw.classList.toggle('on', EVON[k2]); });
        return;
      }
    }
  });

  // ---------- tìm ----------
  var sbar = $('.cx-search'), sin = sbar.querySelector('input');
  function openSearch() { sbar.hidden = false; sin.focus(); sin.select(); }
  function closeSearch() { sbar.hidden = true; S.q = ''; S.hits = []; S.hi = -1; sin.value = ''; render({ keep: true }); }
  function doSearch() {
    S.q = sin.value.trim();
    S.hits = S.q ? MSG.filter(function (m) { return !m.sys && !m.rec && norm(segText(m.segs) + ' ' + m.w + ' ' + (m.files || []).map(function (f) { return f.n; }).join(' ')).indexOf(norm(S.q)) >= 0; }).map(function (m) { return m.id; }) : [];
    S.hi = S.hits.length - 1; render({ keep: true });
    sbar.querySelector('.n').textContent = S.q ? (S.hits.length ? (S.hi + 1) + ' / ' + S.hits.length : 'Không thấy') : '';
    if (S.hi >= 0) jump(S.hits[S.hi]);
  }
  function stepHit(d) { if (!S.hits.length) return; S.hi = (S.hi + d + S.hits.length) % S.hits.length; render({ keep: true }); sbar.querySelector('.n').textContent = (S.hi + 1) + ' / ' + S.hits.length; jump(S.hits[S.hi]); }
  var st; sin.addEventListener('input', function () { clearTimeout(st); st = setTimeout(doSearch, 250); });
  sin.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); stepHit(e.shiftKey ? 1 : -1); } if (e.key === 'Escape') closeSearch(); });
  document.addEventListener('keydown', function (e) { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'f' && document.querySelector('.cx-wrap')) { e.preventDefault(); openSearch(); } });

  // ---------- khởi tạo ----------
  render({ bottom: true });
  var ue = body.querySelector('.cx-unread'); if (ue) body.scrollTop = Math.max(0, ue.offsetTop - body.clientHeight * 0.45);
  downBtn();
  window.__CX = { S: S, MSG: MSG, OBJ: OBJ, EVON: EVON, render: render };
})();

// Builds "Tạo không gian" popup on top of the real V2BaseModal of /assign/project_items
window.MKspaceModal = function (variant) {
  const m = document.querySelector('.modal.show');
  m.querySelector('.modal-title span').textContent = 'Tạo không gian';
  const ic = m.querySelector('.v2-modal-icon i'); if (ic) ic.className = 'ri-add-box-line';
  const row = m.querySelector('.form-row');
  if (!window.__mkTpl) window.__mkTpl = [...row.children].map(c => c.cloneNode(true));
  const [cInput, cSelect, cText] = window.__mkTpl;
  let rid = 0;
  const mk = (tpl, col, label, req) => { const c = tpl.cloneNode(true); c.className = col + ' mb-2'; const t = c.querySelector('.v2-label__text'); const star = (t.querySelector('.required') || cInput.querySelector('.required')).cloneNode(true); t.textContent = ' ' + label + ' '; if (req) t.appendChild(star); if (!req) { const s = c.querySelector('.required'); if (s) s.remove(); } return c; };
  const help = (c, txt) => { const d = document.createElement('div'); d.className = 'mk-help'; d.innerHTML = txt; c.appendChild(d); return c; };
  const inp = (label, req, val, ph, col = 'col-md-6') => { const c = mk(cInput, col, label, req); const i = c.querySelector('input'); i.setAttribute('placeholder', ph || ''); if (val) i.setAttribute('value', val); return c; };
  const sel = (label, req, text, col = 'col-md-6') => { const c = mk(cSelect, col, label, req); const r = c.querySelector('.select2-selection__rendered'); r.textContent = text; r.title = text; if (!text) { r.innerHTML = '<span class="select2-selection__placeholder">Chọn ' + label.toLowerCase() + '</span>'; } c.querySelectorAll('select').forEach(s => s.removeAttribute('id')); return c; };
  const multi = (label, req, chips, col = 'col-md-12', ph) => { const c = sel(label, req, ' ', col); const s = c.querySelector('.select2-selection'); s.className = 'select2-selection select2-selection--multiple'; s.style.cssText = 'min-height:32px;'; s.innerHTML = '<ul class="select2-selection__rendered">' + chips.map(x => `<li class="select2-selection__choice" title="${x}"><span class="select2-selection__choice__remove" role="presentation">×</span>${x}</li>`).join('') + (chips.length ? '' : `<li class="select2-search select2-search--inline"><span style="color:#94a3b8;font-size:12.8px;line-height:28px;padding-left:6px">${ph || 'Chọn nhân viên'}</span></li>`) + '</ul>'; return c; };
  const radio = (label, req, opts, checked, col = 'col-md-6') => { const c = mk(cText, col, label, req); c.querySelector('textarea').outerHTML = '<div class="pt-1">' + opts.map((o, i) => { rid++; return `<div class="custom-control custom-radio custom-control-inline"><input type="radio" class="custom-control-input" id="mksr${rid}" ${i === checked ? 'checked' : ''}><label class="custom-control-label" for="mksr${rid}">${o}</label></div>`; }).join('') + '</div>'; return c; };
  const txt = (label, ph, col = 'col-md-12') => { const c = mk(cText, col, label, false); c.querySelector('textarea').setAttribute('placeholder', ph); return c; };
  const ME = 'DNS Admin - HN_QTTT - 21410013';
  let items = [];
  if (variant === 'room-dept') items = [
    help(radio('Loại không gian', true, ['Phòng', 'Dự án'], 0), 'Phòng: làm việc thường trực, không có hạn kết thúc.'),
    inp('Tên phòng', true, 'Phòng Hành chính', 'VD: Phòng Hành chính, Hỗ trợ phần mềm'),
    help(radio('Nguồn thành viên', true, ['Theo phòng ban', 'Tự chọn'], 0), 'Theo phòng ban: chỉ gồm nhân sự của 1 phòng ban, tự cập nhật khi nhân sự vào / rời.'),
    help(sel('Phòng ban / Bộ phận', true, 'PHÒNG NHÂN SỰ HÀNH CHÍNH'), '<i class="ri-team-line"></i> 18 nhân sự (gồm các bộ phận bên dưới) sẽ tự vào phòng. Trưởng / phó phòng ban là Quản lý.'),
    help(multi('Quản lý thêm', false, [], 'col-md-12', 'Chọn thêm Quản lý trong số nhân sự phòng ban (không bắt buộc)'), 'Quản lý được giao việc, tạo Nhóm, cấu hình phòng và đổi vai trò thành viên.'),
    txt('Mô tả', 'Phạm vi công việc của phòng'),
  ];
  if (variant === 'room-custom') items = [
    help(radio('Loại không gian', true, ['Phòng', 'Dự án'], 0), 'Phòng: làm việc thường trực, không có hạn kết thúc.'),
    inp('Tên phòng', true, 'Hỗ trợ phần mềm', 'VD: Phòng Hành chính, Hỗ trợ phần mềm'),
    help(radio('Nguồn thành viên', true, ['Theo phòng ban', 'Tự chọn'], 1), 'Tự chọn: chọn nhân sự từ bất kỳ phòng ban nào.'),
    multi('Quản lý', true, [ME], 'col-md-6'),
    help(multi('Thành viên', false, ['Phạm Văn Tú - HN_QTTT - 21410402', 'Ngô Thị Lan - HN_QTTT - 21410415', 'Đặng Minh Khoa - HN_KTCN - 21410177', 'Bùi Thanh Hà - HN_KT - 21410260']), 'Chọn từ mọi phòng ban. Quản lý thêm / bớt người sau ở tab Thành viên.'),
    txt('Mô tả', 'Phạm vi công việc của phòng'),
  ];
  if (variant === 'project') items = [
    help(radio('Loại không gian', true, ['Phòng', 'Dự án'], 1), 'Dự án: có thời hạn, đóng lại khi hoàn thành.'),
    inp('Tên dự án', true, 'Triển khai phân hệ Công việc 2027', 'VD: Triển khai phân hệ Công việc 2027'),
    inp('Ngày bắt đầu', true, '01/11/2026', 'dd/mm/yyyy'),
    inp('Hạn kết thúc', true, '31/03/2027', 'dd/mm/yyyy'),
    help(multi('Quản lý dự án', true, [ME], 'col-md-12'), 'Người tạo mặc định là Quản lý dự án.'),
    help(multi('Thành viên', false, ['Phạm Văn Tú - HN_QTTT - 21410402', 'Nguyễn Thị Hằng - HN_NSHC - 21410105', 'Đặng Minh Khoa - HN_KTCN - 21410177', 'Trịnh Đức Anh - HN_KD1 - 21410550']), 'Chọn từ mọi phòng ban.'),
    txt('Mục tiêu / mô tả', 'Mục tiêu, phạm vi của dự án'),
  ];
  row.innerHTML = '';
  items.forEach(c => row.appendChild(c));
  [...m.querySelectorAll('.modal-footer button')].forEach(b => { if (/Tiếp tục/.test(b.textContent)) b.remove(); });
  // Lưu button label
  const save = [...m.querySelectorAll('.modal-footer button')].find(b => /Lưu|Tạo (phòng|dự án)/.test(b.textContent));
  if (save) [...save.childNodes].forEach(n => { if (n.nodeType === 3 && /Lưu|Tạo (phòng|dự án)/.test(n.textContent)) n.textContent = ' Tạo ' + (variant === 'project' ? 'dự án' : 'phòng') + ' '; });
  return row.children.length;
};

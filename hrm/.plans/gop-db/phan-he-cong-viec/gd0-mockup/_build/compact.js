// Chuyển 1 màn danh sách kiểu cũ (thẻ bộ lọc + đầu thẻ danh sách) sang thanh công cụ gọn (U11).
// Dùng trên trang mockup đã dựng (served qua http), sau đó MKR.base() để chụp lại.
// opt: { placeholder, chips:[[text, cls, title]], keep:[nhãn ô giữ lại] | null, rename:{nhãn cũ: nhãn mới},
//        afl:[[nhãn, giá trị]], cfgTitle, dropNotes:true }
window.MKcompact = function (opt) {
  opt = opt || {};
  const scope = document.querySelector('main .overflow-auto') || document.querySelector('.content-page');
  const filt = scope.querySelector('section.smart-filter-card');
  if (!filt) return 'no-filter';
  const host = filt.parentElement;
  const list = [...host.children].find(e => e.tagName === 'SECTION' && e !== filt && e.querySelector('table'));
  // --- pieces
  const qs = filt.querySelector('.quick-search');
  if (opt.placeholder) qs.querySelector('input').setAttribute('placeholder', opt.placeholder);
  const advBtn = filt.querySelector('.filter-toggle-btn');
  const cfgBtn = [...filt.querySelectorAll('button')].find(b => /Cài đặt bộ lọc/.test(b.textContent));
  const adv = filt.querySelector('.smart-advanced-filters .form-row');
  const head = list.firstElementChild; // tiêu đề + cụm nút
  const actWrap = head.querySelector('.justify-content-lg-end') || head.lastElementChild;
  const pillTpl = list.querySelector('.due-pill') || (() => { const s = document.createElement('span'); s.className = 'due-pill'; return s; })();
  // --- toolbar
  const tb = document.createElement('div'); tb.className = 'mk-tb';
  const sep = () => { const s = document.createElement('span'); s.className = 'mk-tb-sep'; return s; };
  tb.appendChild(qs);
  if (opt.chips && opt.chips.length) {
    tb.appendChild(sep());
    const chips = document.createElement('div'); chips.className = 'mk-tb-chips';
    opt.chips.forEach(([t, cl, ti]) => { const p = pillTpl.cloneNode(false); p.className = 'due-pill ' + (cl || 'st-total'); if (ti) p.title = ti; p.textContent = t; chips.appendChild(p); });
    tb.appendChild(chips);
  }
  tb.appendChild(sep());
  advBtn.classList.add('mk-filter-btn');
  [...advBtn.childNodes].forEach(n => { if (n.nodeType === 3 && n.nodeValue.trim()) n.nodeValue = ' Lọc '; });
  const ic = advBtn.querySelector('.toggle-icon, i'); if (ic) ic.className = 'ri-equalizer-line toggle-icon';
  const fc = document.createElement('span'); fc.className = 'mk-fcount'; fc.textContent = String((opt.afl || []).length || 1);
  advBtn.insertBefore(fc, [...advBtn.childNodes].find(n => n.nodeType === 8) || null);
  tb.appendChild(advBtn);
  // right: mọi nút của đầu thẻ (giữ cả menu thả kèm theo, vd "Gửi vấn đề cho")
  const right = document.createElement('div'); right.className = 'mk-tb-right'; right.style.position = 'relative';
  [...actWrap.children].forEach(el => {
    if (el.tagName === 'BUTTON') {
      el.classList.remove('mb-2', 'mr-2');
      if (/Xuất Excel/.test(el.textContent)) {
        el.title = 'Xuất Excel';
        [...el.childNodes].forEach(n => { if (n.nodeType === 3) n.nodeValue = ''; });
        el.className = el.className.replace('v2-btn--prefix-sm', '') + ' btn-icon';
        const pre = el.querySelector('.v2-btn__prefix--sm'); if (pre) { const i = pre.querySelector('i'); el.insertBefore(i, pre); pre.remove(); i.style.marginRight = '0'; }
      }
      if (el.classList.contains('btn-icon') && !el.title) el.title = 'Cấu hình cột hiển thị';
    }
    right.appendChild(el);
  });
  tb.appendChild(right);
  // --- popover
  const pop = document.createElement('div'); pop.className = 'mk-filter-pop';
  const hd = document.createElement('div'); hd.className = 'mk-fp-hd'; hd.innerHTML = '<span>' + (opt.cfgTitle || 'Lọc nâng cao') + '</span>';
  if (cfgBtn) { cfgBtn.title = 'Chọn ô lọc hiển thị, thứ tự ô, lưu bộ lọc mặc định'; hd.appendChild(cfgBtn); }
  pop.appendChild(hd);
  const row = adv ? adv.cloneNode(false) : document.createElement('div'); row.className = 'form-row';
  const fields = adv ? [...adv.children] : [];
  const lab = d => (d.querySelector('.ff__text') || d.querySelector('.v2-label__text') || d).textContent.trim();
  (opt.keep ? opt.keep.map(k => fields.find(d => lab(d) === k)).filter(Boolean) : fields).forEach(f => {
    f.className = 'col-md-6';
    const t = f.querySelector('.ff__text'); if (t && opt.rename && opt.rename[t.textContent.trim()]) { t.textContent = opt.rename[t.textContent.trim()]; const l = f.querySelector('.ff__label'); if (l) l.title = t.textContent; }
    row.appendChild(f);
  });
  pop.appendChild(row);
  const ft = document.createElement('div'); ft.className = 'mk-fp-ft';
  const prim = right.querySelector('.v2-btn--primary');
  const apply = prim.cloneNode(true); apply.removeAttribute('title');
  [...apply.childNodes].forEach(n => { if (n.nodeType === 3 && n.nodeValue.trim()) n.nodeValue = ' Áp dụng '; });
  const ai = apply.querySelector('i'); if (ai) ai.className = 'ri-check-line';
  const clear = document.createElement('button'); clear.type = 'button'; clear.className = 'v2-btn v2-btn--sm v2-btn--tertiary v2-btn--tertiary-info'; clear.textContent = 'Xoá lọc';
  [...apply.attributes].filter(a => a.name.startsWith('data-v-')).forEach(a => clear.setAttribute(a.name, ''));
  ft.append(apply, clear); pop.appendChild(ft);
  tb.appendChild(pop);
  // --- hàng điều kiện đang lọc (chỉ hiện khi body.mk-filtered)
  const afl = document.createElement('div'); afl.className = 'mk-afl';
  afl.innerHTML = (opt.afl || []).map(([k, v]) => '<span class="mk-af">' + k + ': <b>' + v + '</b><i class="ri-close-line"></i></span>').join('') + '<span class="mk-af-clear">Xoá lọc</span>';
  // --- lắp ráp
  filt.remove(); head.remove();
  const ttb = list.querySelector('.table-toolbar'); if (ttb) ttb.remove();
  // hàng left-actions cũ chứa chip đếm (V2BaseDataTable slot left-actions) — bỏ, chip đã lên thanh công cụ
  list.querySelectorAll('.due-pill').forEach(p => { const r = p.closest('.d-flex.flex-wrap.justify-content-between'); if (r && list.contains(r)) r.remove(); });
  if (opt.dropNotes !== false) list.querySelectorAll('.mk-note').forEach(n => n.remove());
  list.classList.add('mk-flat');
  host.insertBefore(afl, list); host.insertBefore(tb, afl);
  return 'ok';
};
'MKcompact ready';
// Đánh dấu dòng không khớp điều kiện mẫu (ẩn khi body.mk-filtered) + dòng tổng 2 trạng thái.
window.MKfilterRows = function (col, test) {
  const tb = document.querySelector('main tbody, .content-page tbody'); const rows = [...tb.children];
  const m = rows.filter(tr => test(tr.children[col].textContent.trim())), o = rows.filter(tr => !m.includes(tr));
  [...m, ...o].forEach((tr, i) => { tb.appendChild(tr); tr.children[0].textContent = String(i + 1); tr.classList.toggle('mk-fx', o.includes(tr)); });
  const tot = rows.length;
  const foot = document.querySelector('.mk-flat .tp-small-text') || [...document.querySelectorAll('.mk-flat *')].find(e => e.children.length === 0 && /Hiển thị|Không có/.test(e.textContent));
  if (foot) foot.innerHTML = '<span class="mk-nf">Hiển thị 1–' + tot + ' / ' + tot + '</span><span class="mk-f">Hiển thị 1–' + m.length + ' / ' + m.length + ' (đang lọc)</span>';
  return [m.length, tot, !!foot];
};

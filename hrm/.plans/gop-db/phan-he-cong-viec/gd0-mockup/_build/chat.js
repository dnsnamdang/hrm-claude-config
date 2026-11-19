window.MKbtn = function (label, icon, kind) {
  // clone a real V2BaseButton and retarget; kind: primary|secondary|tertiary
  const all = [...document.querySelectorAll('button.v2-btn')];
  const src = all.find(b => b.classList.contains('v2-btn--' + kind)) || all[0];
  const b = src.cloneNode(true);
  b.className = b.className.replace(/v2-btn--(primary|secondary|tertiary|quaternary)(-[a-z]+)?/g, '').trim() + ' v2-btn--' + kind + ' v2-btn--' + kind + '-info';
  if (!b.classList.contains('v2-btn--sm')) b.classList.add('v2-btn--sm');
  const ic = b.querySelector('i'); if (ic) ic.className = icon;
  [...b.childNodes].forEach(n => { if (n.nodeType === 3 && n.textContent.trim()) n.textContent = ' ' + label + ' '; });
  b.classList.remove('tab-btn-root', 'active');
  const lab = b.querySelector('.tab-label'); if (lab) lab.textContent = label;
  return b.outerHTML;
};
window.MKav = (txt, color) => `<div class="mk-av" style="background:${color}">${txt}</div>`;
window.MKchat = function (o) {
  const host = document.querySelector('.surface .overflow-auto') || document.querySelector('.surface');
  const send = MKbtn('Gửi', 'ri-send-plane-2-line', 'primary');
  const B = MK.badge;
  const msgs = o.messages.map(m => {
    if (m.day) return `<div class="mk-day"><span>${m.day}</span></div>`;
    if (m.sys) return `<div class="mk-sys"><i class="${m.icon || 'ri-checkbox-circle-line'}" style="color:${m.color || '#16a34a'}"></i>${m.sys}</div>`;
    return `<div class="mk-msg ${m.me ? 'me' : ''}">${m.me ? '' : MKav(m.av, m.c)}<div class="meta">
      ${m.me ? '' : `<div class="who">${m.who}<small>${m.t}</small></div>`}
      ${m.me ? `<div class="who" style="text-align:right"><small>${m.t}</small></div>` : ''}
      <div class="mk-bub">${m.quote ? `<div class="mk-quote">${m.quote}</div>` : ''}${m.html}</div>
      ${m.file ? `<div class="mk-file"><i class="ri-file-excel-2-line"></i><div><b>${m.file}</b><small>${m.size}</small></div></div>` : ''}
      ${m.card ? `<div class="mk-card" style="border-left-color:${m.card.color}"><div class="k"><i class="${m.card.icon}"></i>${m.card.kind}</div><div class="n">${m.card.name}</div><div class="r">${B(m.card.st, m.card.stc)}<span><i class="ri-user-line"></i> ${m.card.who}</span><span><i class="ri-calendar-line"></i> Hạn ${m.card.due}</span></div></div>` : ''}
      </div>${m.hover ? `<div class="mk-hover"><span><i class="ri-reply-line"></i>Trả lời</span><span><i class="ri-emotion-line"></i></span><span class="on"><i class="ri-task-line"></i>Tạo nhiệm vụ</span><span><i class="ri-bug-line"></i>Tạo vấn đề</span><span><i class="ri-more-2-fill"></i></span></div>` : ''}</div>`;
  }).join('');
  const side = (o.side || []).map(p => `<div class="mk-panel"><div class="mk-panel-hd">${p.title}<small>${p.sub || ''}</small></div>${p.items.map(i => `<div class="mk-li">${i}</div>`).join('')}</div>`).join('');
  host.innerHTML = `<div class="mk-chat-wrap"><div class="mk-chat">
    <div class="mk-chat-hd"><div><div class="t"><i class="ri-chat-3-line" style="color:#1abc9c"></i> ${o.title}</div><div class="s">${o.sub}</div></div>
      <div class="d-flex" style="gap:6px">${MKbtn('Tìm trong chat', 'ri-search-line', 'tertiary')}${MKbtn('Thông báo: Tất cả', 'ri-notification-3-line', 'tertiary')}</div></div>
    <div class="mk-chat-body">${msgs}</div>
    <div class="mk-comp"><div class="mk-comp-box">Nhập tin nhắn… gõ <b style="color:#0a7c88">@</b> để nhắc tên, <b style="color:#0a7c88">#</b> để chèn nhiệm vụ / vấn đề</div>
      <div class="mk-comp-bar"><div class="ic"><span title="Đính kèm file"><i class="ri-attachment-2"></i></span><span title="Nhắc tên">@</span><span title="Chèn nhiệm vụ / vấn đề">#</span><span title="Biểu cảm"><i class="ri-emotion-line"></i></span></div>${send}</div></div>
  </div><div class="mk-side">${side}</div></div>`;
};

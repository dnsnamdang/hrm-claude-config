// Helpers to edit a built mockup screen in the browser, then capture it back as a source body (cap/*.html).
window.MKR = {
  scope: 'header.topbar, main, .modal, .content-page .container-fluid',
  // replace substrings inside text nodes of the content area (never the navbar / notification dropdown)
  txt(pairs, scope) {
    let n = 0;
    document.querySelectorAll(scope || this.scope).forEach(root => {
      const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      let t; while ((t = w.nextNode())) {
        let v = t.nodeValue;
        pairs.forEach(([a, b]) => { if (v.includes(a)) { v = v.split(a).join(b); n++; } });
        if (v !== t.nodeValue) t.nodeValue = v;
      }
    });
    return n;
  },
  // body without modal/backdrop/class — the base layer
  base() {
    const b = document.body.cloneNode(true);
    b.querySelectorAll('.modal.show, .modal-backdrop').forEach(x => x.closest('.modal, .modal-backdrop') && x.remove());
    b.removeAttribute('class');
    return b.outerHTML;
  },
  // the open modal only (as captured originally: the outer wrapper of .modal.show)
  modal() {
    const m = document.querySelector('.modal.show');
    const outer = m.closest('[id$="___BV_modal_outer_"]') || m;
    return outer.outerHTML;
  },
};
'MKR ready';

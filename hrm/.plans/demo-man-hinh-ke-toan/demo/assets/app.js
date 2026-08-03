/* ============================================================
   Demo Kế toán HRM — logic chung: shell, tabs, toast, modal
   Shell bám cấu trúc hrm-client: logo-box + left-side-menu (trắng,
   condensed, hover hiện label) + navbar-custom (trắng) + content-page
   ============================================================ */

/* ---------- Shell ---------- */
function renderShell(activeKey, pageContentHTML) {
    var menu = [
        { icon: 'ri-dashboard-line', label: 'Tổng quan', href: '#', disabled: true },
        {
            icon: 'ri-bank-line', label: 'Khế ước vay', children: [
                { key: 'borrow', label: 'Khế ước đi vay', href: 'di-vay-danh-sach.html' },
                { key: 'lend', label: 'Khế ước cho vay', href: 'cho-vay-danh-sach.html' }
            ]
        },
        {
            icon: 'ri-book-2-line', label: 'Sổ sách kế toán', children: [
                { key: 'journal', label: 'Sổ nhật ký chung', href: 'so-nhat-ky-chung.html' },
                { key: 'cashbook', label: 'Nhật ký thu / chi tiền', href: 'nhat-ky-thu-chi.html' },
                { key: 'cashfund', label: 'Sổ quỹ tiền mặt', href: 'so-quy.html' },
                { key: 'salesinv', label: 'Bảng kê HĐ bán hàng', href: 'bang-ke-hoa-don-ban-hang.html' },
                { key: 'costvouchers', label: 'Bảng kê CT theo mã phí', href: 'bang-ke-chung-tu-ma-phi.html' },
                { key: 'ledger', label: 'Sổ Cái', href: 'so-cai.html' },
                { key: 'taccount', label: 'Sổ tổng hợp chữ T', href: 'so-tong-hop-chu-t.html' }
            ]
        },
        {
            icon: 'ri-bar-chart-box-line', label: 'Báo cáo', children: [
                { key: 'trial', label: 'Cân đối phát sinh nhiều TK', href: 'bang-can-doi-phat-sinh.html' },
                { key: 'debt', label: 'Cân đối phát sinh công nợ', href: 'bang-can-doi-cong-no.html' },
                { key: 'balance', label: 'Bảng cân đối kế toán', href: 'bang-can-doi.html' },
                { key: 'cashbalance', label: 'Báo cáo số dư tiền', href: 'bao-cao-so-du-tien.html' }
            ]
        },
        {
            icon: 'ri-git-merge-line', label: 'Thiết lập', children: [
                { key: 'posting', label: 'Cấu hình hạch toán', href: 'posting-rule-engine-v3.html' }
            ]
        }
    ];
    var items = menu.map(function (m) {
        if (!m.children) {
            var href = m.disabled ? 'javascript:void(0)' : m.href;
            return '<li><a class="' + (m.disabled ? 'disabled' : '') + '" href="' + href + '"' +
                (m.disabled ? ' title="Ngoài phạm vi demo"' : ' title="' + m.label + '"') + '>' +
                '<i class="' + m.icon + '"></i></a></li>';
        }
        var isActive = m.children.some(function (c) { return c.key === activeKey; });
        var subs = m.children.map(function (c) {
            return '<a class="' + (c.key === activeKey ? 'active' : '') + '" href="' + c.href + '">' + c.label + '</a>';
        }).join('');
        return '<li class="has-sub' + (isActive ? ' active' : '') + '">' +
            '<a href="javascript:void(0)" title="' + m.label + '"><i class="' + m.icon + '"></i></a>' +
            '<div class="submenu"><div class="sub-head">' + m.label + '</div>' + subs + '</div></li>';
    }).join('');

    /* Tiêu đề màn hình trên topbar: tên trang lấy từ <title>, nhóm menu (breadcrumb) từ MENU */
    var activeParent = null;
    menu.forEach(function (m) {
        if (m.children && m.children.some(function (c) { return c.key === activeKey; })) activeParent = m;
    });
    var pageTitle = (document.title.split('—')[0] || '').trim() || (activeParent ? activeParent.label : 'Kế toán HRM');
    var crumbLabel = activeParent ? activeParent.label : 'Kế toán';
    var crumbIcon = activeParent ? activeParent.icon : 'ri-calculator-line';

    document.body.insertAdjacentHTML('afterbegin',
        '<div class="logo-box"><a class="logo" href="index.html" title="Kế toán"><i class="ri-calculator-line"></i></a></div>' +
        '<div class="left-side-menu">' +
        '  <div id="sidebar-menu"><ul>' + items + '</ul></div>' +
        '</div>' +
        '<div class="navbar-custom">' +
        '  <div class="topbar-left">' +
        '    <button class="button-menu-mobile" title="Thu gọn menu"><i class="ri-menu-line"></i></button>' +
        '    <div class="topbar-title">' +
        '      <div class="tt-crumb"><i class="' + crumbIcon + '"></i> ' + crumbLabel + '</div>' +
        '      <div class="tt-name">' + pageTitle + '</div>' +
        '    </div>' +
        '  </div>' +
        '  <div class="topnav-right">' +
        '    <a class="nav-link" title="Toàn màn hình"><i class="ri-fullscreen-line"></i></a>' +
        '    <a class="nav-link" title="Phân hệ"><i class="ri-layout-grid-line"></i></a>' +
        '    <a class="nav-link" title="Thông báo"><i class="ri-notification-3-line"></i><span class="noti-icon-badge">3</span></a>' +
        '    <div class="user-box">' +
        '      <div class="avatar">ĐN</div>' +
        '      <div><div class="user-name">Đặng Nam</div><div class="user-role">Kế toán trưởng</div></div>' +
        '    </div>' +
        '  </div>' +
        '</div>' +
        '<div class="content-page"><div class="v2-styles container-fluid">' + pageContentHTML + '</div></div>' +
        '<div id="toast-wrap"></div>');
}

/* ---------- Sticky cột đầu (đóng băng khi cuộn ngang) ----------
   Số cột đóng băng theo từng báo cáo (id bảng). Helper đo bề rộng động
   từ hàng header đầu, set position:sticky + left cho N cột đầu của mọi hàng.
   Tự re-apply qua MutationObserver (re-render tbody/header) + resize. */
var STICKY_FREEZE = {
    ltbl: 4,        // Sổ Cái → …Diễn giải
    jtbl: 4,        // Sổ NKC → …Ngày CT (Mã/Tên đối tượng + Diễn giải cuộn cùng phần phân tích)
    cbtbl: 3,       // Nhật ký thu/chi → …Ngày CT
    cvtbl: 4,       // Bảng kê mã phí → …Diễn giải
    sitbl: 5,       // Bảng kê HĐ bán hàng → …Tên khách
    'fund-tbl': 5,  // Sổ quỹ → …Diễn giải
    btbl: 1,        // Bảng cân đối → CHỈ TIÊU
    'tbps-tbl': 2,  // Cân đối số phát sinh → Số hiệu + Tên tài khoản
    'bcps-tbl': 1,  // Cân đối phát sinh công nợ → Tài khoản / Đối tượng
    tatbl: 2,       // Sổ chữ T → Tk đối ứng, Tên tài khoản
    tbl: 2          // Danh sách khế ước → STT, Số khế ước
};
function applyStickyTable(table) {
    var n = STICKY_FREEZE[table.id];
    if (!n || !table.tHead || !table.tHead.rows.length) return;
    // reset lần trước
    table.querySelectorAll('.sticky-col').forEach(function (c) {
        c.classList.remove('sticky-col', 'sticky-col-last');
        c.style.left = ''; c.style.zIndex = '';
    });
    var hrow = table.tHead.rows[0];
    var count = Math.min(n, hrow.cells.length);
    var offs = [], acc = 0;
    for (var i = 0; i < count; i++) { offs[i] = acc; acc += hrow.cells[i].getBoundingClientRect().width; }
    if (acc <= 0) return; // bảng chưa layout (ẩn) → bỏ qua, sẽ re-apply sau
    function stickRow(row, z) {
        var col = 0;
        for (var i = 0; i < row.cells.length && col < n; i++) {
            var cell = row.cells[i], span = cell.colSpan || 1;
            if (col + span > n) break;            // ô tràn khỏi vùng đóng băng → không dính (tránh che dữ liệu)
            cell.classList.add('sticky-col');
            cell.style.left = offs[col] + 'px';
            if (z) cell.style.zIndex = z;
            if (col + span === n) cell.classList.add('sticky-col-last');
            col += span;
        }
    }
    stickRow(hrow, 8);
    Array.prototype.forEach.call(table.tBodies, function (tb) {
        Array.prototype.forEach.call(tb.rows, function (r) { stickRow(r, 3); });
    });
    if (table.tFoot) Array.prototype.forEach.call(table.tFoot.rows, function (r) { stickRow(r, 4); });
}
function refreshSticky() {
    Object.keys(STICKY_FREEZE).forEach(function (id) {
        var t = document.getElementById(id);
        if (t) applyStickyTable(t);
    });
}
(function initSticky() {
    if (window.__stickyInit) return; window.__stickyInit = true;
    var timer = null;
    function schedule() { if (timer) return; timer = setTimeout(function () { timer = null; refreshSticky(); }, 30); }
    window.addEventListener('load', schedule);
    window.addEventListener('resize', schedule);
    // Chỉ phản ứng với thay đổi cấu trúc (childList) — thay đổi class/style của ta là attribute nên không lặp
    var mo = new MutationObserver(function (muts) {
        for (var i = 0; i < muts.length; i++) { if (muts[i].type === 'childList') { schedule(); return; } }
    });
    (function start() {
        if (document.body) mo.observe(document.body, { childList: true, subtree: true });
        else setTimeout(start, 10);
    })();
})();

/* ---------- Toast ---------- */
function toast(msg, type) {
    var el = document.createElement('div');
    el.className = 'toast-item' + (type ? ' toast-' + type : '');
    el.textContent = msg;
    document.getElementById('toast-wrap').appendChild(el);
    setTimeout(function () { el.style.opacity = '0'; el.style.transition = 'opacity .3s'; }, 2600);
    setTimeout(function () { el.remove(); }, 3000);
}

/* ---------- Tabs ---------- */
function initTabs(container) {
    var root = container || document;
    root.querySelectorAll('.nav-tabs .nav-link').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var tabs = btn.closest('.nav-tabs');
            var wrap = tabs.parentElement;
            tabs.querySelectorAll('.nav-link').forEach(function (b) { b.classList.remove('active'); });
            btn.classList.add('active');
            wrap.querySelectorAll(':scope > .tab-pane').forEach(function (p) { p.classList.remove('active'); });
            wrap.querySelector('#' + btn.dataset.tab).classList.add('active');
        });
    });
}

/* ---------- Modal ---------- */
function openModal(id) { document.getElementById(id).classList.add('show'); }
function closeModal(id) { document.getElementById(id).classList.remove('show'); }

/* ---------- Query param ---------- */
function qs(name) {
    var m = new RegExp('[?&]' + name + '=([^&]*)').exec(location.search);
    return m ? decodeURIComponent(m[1]) : '';
}

/* ---------- Validate helpers (convention HRM: is-invalid + invalid-feedback) ---------- */
function setInvalid(input, invalid) {
    input.classList.toggle('is-invalid', invalid);
}
function validateRequired(form) {
    var ok = true;
    form.querySelectorAll('[data-required]').forEach(function (inp) {
        // bỏ qua field đang ẩn (vd: Ngày trả gốc đầu tiên khi Trả gốc = Cuối kỳ)
        if (!inp.offsetParent) { setInvalid(inp, false); return; }
        var bad = !String(inp.value).trim() || (inp.dataset.positive !== undefined && parseMoney(inp.value) <= 0);
        setInvalid(inp, bad);
        if (bad) ok = false;
    });
    return ok;
}

/* ---------- Input tiền: auto format nghìn ---------- */
function bindMoneyInput(inp) {
    inp.addEventListener('input', function () {
        var raw = inp.value.replace(/[^\d]/g, '');
        inp.value = raw ? fmtMoney(parseInt(raw, 10)) : '';
    });
}

/* ---------- Cài đặt bộ lọc (dùng chung các màn sổ) ----------
   - Mỗi trường lọc bọc trong div[data-ff="<id>"]; ban đầu render hết trong #<advWrap>
   - apply(): chuyển các trường "mặc định" (locked + user chọn, lưu localStorage) sang #<defaultWrap>
   - Nút ⚙️ mở modal tick chọn trường mặc định; còn lại nằm trong "Tìm kiếm nâng cao"
   - Nhóm trường: khai báo { id, label, ids: ['f-a','f-b',...] } → 1 checkbox, di chuyển cả khối */
function setupFilterSettings(cfg) {
    function fieldIds(f) { return f.ids || [f.id]; }
    function savedDefaults() {
        try { var v = JSON.parse(localStorage.getItem(cfg.storageKey)); return Array.isArray(v) ? v : null; } catch (e) { return null; }
    }
    function currentDefaults() {
        var saved = savedDefaults();
        return cfg.fields.filter(function (f) {
            if (f.locked) return true;
            return saved ? saved.indexOf(f.id) !== -1 : !!f.def;
        }).map(function (f) { return f.id; });
    }
    function apply() {
        var defs = currentDefaults();
        var defWrap = document.getElementById(cfg.defaultWrap);
        var advWrap = document.getElementById(cfg.advWrap);
        cfg.fields.forEach(function (f) {
            var target = defs.indexOf(f.id) !== -1 ? defWrap : advWrap;
            fieldIds(f).forEach(function (id) {
                var el = document.querySelector('[data-ff="' + id + '"]');
                if (el) target.appendChild(el);
            });
        });
        var toggle = document.getElementById('f-toggle');
        if (toggle) toggle.style.display = advWrap.children.length ? '' : 'none';
    }
    document.body.insertAdjacentHTML('beforeend',
        '<div class="modal-backdrop-demo" id="ffcfg-modal"><div class="modal-dialog" style="max-width:680px">' +
        '<div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-settings-3-line"></i></span>Cài đặt bộ lọc</h5>' +
        '<button type="button" class="close" onclick="closeModal(\'ffcfg-modal\')">×</button></div>' +
        '<div class="modal-body"><p class="tp-small-text" style="margin-bottom:10px">Tích chọn các trường hiển thị <b>mặc định</b> khi vào màn hình. Trường không tích sẽ nằm trong khu "Tìm kiếm nâng cao". Cài đặt được lưu theo từng màn hình.</p>' +
        '<div class="ffcfg-grid" id="ffcfg-list"></div></div>' +
        '<div class="modal-footer">' +
        '<button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="ffcfg-save"><i class="ri-save-3-line"></i> Lưu</button>' +
        '<button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="ffcfg-reset"><i class="ri-refresh-line"></i> Khôi phục mặc định</button>' +
        '<button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'ffcfg-modal\')"><i class="ri-close-line"></i> Đóng</button>' +
        '</div></div></div>');
    function renderList() {
        var defs = currentDefaults();
        document.getElementById('ffcfg-list').innerHTML = cfg.fields.map(function (f) {
            var checked = defs.indexOf(f.id) !== -1;
            return '<label class="ffcfg-item">' +
                '<input type="checkbox" data-ffcfg="' + f.id + '"' + (checked ? ' checked' : '') + (f.locked ? ' disabled' : '') + '> ' +
                f.label + (f.locked ? ' <span class="ffcfg-note">(bắt buộc)</span>' : '') + '</label>';
        }).join('');
    }
    document.getElementById(cfg.gearBtnId).addEventListener('click', function () { renderList(); openModal('ffcfg-modal'); });
    document.getElementById('ffcfg-save').addEventListener('click', function () {
        var ids = [...document.querySelectorAll('[data-ffcfg]')].filter(function (c) { return c.checked; }).map(function (c) { return c.dataset.ffcfg; });
        localStorage.setItem(cfg.storageKey, JSON.stringify(ids));
        apply();
        closeModal('ffcfg-modal');
        toast('Đã lưu cài đặt bộ lọc');
    });
    document.getElementById('ffcfg-reset').addEventListener('click', function () {
        localStorage.removeItem(cfg.storageKey);
        renderList();
        apply();
        toast('Đã khôi phục cài đặt mặc định', 'info');
    });
    apply();
}

/* ---------- Sticky các dòng tổng ở đầu tbody ----------
   Các dòng tổng/số dư đặt LIÊN TIẾP ở đầu tbody (class row-total / row-carry)
   sẽ dính ngay dưới header khi cuộn. position:sticky phải đặt trên <td> (Chrome
   không hỗ trợ sticky trên <tr>), top cộng dồn theo chiều cao từng dòng. */
function applyStickyTotals(tableSel) {
    var table = document.querySelector(tableSel);
    if (!table || !table.tHead || !table.tBodies.length) return;
    var top = table.tHead.offsetHeight;
    var rows = table.tBodies[0].rows;
    for (var i = 0; i < rows.length; i++) {
        var tr = rows[i];
        if (!(tr.classList.contains('row-total') || tr.classList.contains('row-carry'))) break;
        [...tr.cells].forEach(function (td) {
            td.style.position = 'sticky';
            td.style.top = top + 'px';
            td.style.zIndex = 4;
        });
        top += tr.offsetHeight;
    }
}

/* ---------- Sort theo cột (icon trên header, dùng chung các màn sổ) ----------
   setupColumnSort({ tableSel, headRow: hàng thead chứa th cột (mặc định 2), cols, onChange })
   - cols: mảng theo ĐÚNG thứ tự th, mỗi phần tử {key} hoặc null (cột không cho sort)
   - Click xoay vòng: tăng dần → giảm dần → bỏ sort (trả về thứ tự chuẩn của sổ)
   - onChange(state) với state = {key, dir:'asc'|'desc'} hoặc null */
function setupColumnSort(cfg) {
    var ths = document.querySelectorAll(cfg.tableSel + ' thead tr:nth-child(' + (cfg.headRow || 2) + ') th');
    var state = null;
    function refreshIcons() {
        ths.forEach(function (th) {
            var ico = th.querySelector('.sort-ico');
            if (!ico) return;
            var key = th.getAttribute('data-sort-key');
            if (state && state.key === key) {
                ico.className = 'sort-ico active ' + (state.dir === 'asc' ? 'ri-arrow-up-s-line' : 'ri-arrow-down-s-line');
                th.classList.add('sorted');
                th.title = state.dir === 'asc' ? 'Đang sắp xếp tăng dần — click để sắp giảm dần' : 'Đang sắp xếp giảm dần — click để trở về thứ tự chuẩn';
            } else {
                ico.className = 'sort-ico ri-arrow-up-down-line';
                th.classList.remove('sorted');
                th.title = 'Sắp xếp theo cột này';
            }
        });
    }
    cfg.cols.forEach(function (col, i) {
        var th = ths[i];
        if (!th || !col || !col.key) return;
        th.classList.add('th-sort');
        th.setAttribute('data-sort-key', col.key);
        th.insertAdjacentHTML('beforeend', ' <i class="sort-ico ri-arrow-up-down-line"></i>');
        th.addEventListener('click', function () {
            if (state && state.key === col.key) {
                state = state.dir === 'asc' ? { key: col.key, dir: 'desc' } : null;
            } else {
                state = { key: col.key, dir: 'asc' };
            }
            refreshIcons();
            cfg.onChange(state);
        });
    });
    refreshIcons();
}

/* ---------- Phân trang client-side (dùng chung các màn sổ) ----------
   var pager = createPager({ storageKey, containerSel, onChange });
   Trong draw():  var pageRows = pager.paginate(sortedList, filterSignature);
                  (signature đổi → tự về trang 1; đổi trang giữ nguyên bộ lọc)
   Sau khi render bảng: pager.render();
   Link sâu: pager.goToIndex(idx) rồi gọi lại draw. */
function createPager(cfg) {
    var page = 1;
    var pageSize = parseInt(localStorage.getItem(cfg.storageKey), 10);
    if (isNaN(pageSize)) pageSize = cfg.defaultSize || 25;
    var lastSig = null, total = 0, pages = 1;
    function paginate(list, sig) {
        if (sig !== undefined && sig !== lastSig) { lastSig = sig; page = 1; }
        total = list.length;
        pages = pageSize > 0 ? Math.max(1, Math.ceil(total / pageSize)) : 1;
        if (page > pages) page = pages;
        return pageSize > 0 ? list.slice((page - 1) * pageSize, page * pageSize) : list;
    }
    function render() {
        var el = document.querySelector(cfg.containerSel);
        if (!el) return;
        if (!total) { el.innerHTML = ''; return; }
        var from = pageSize > 0 ? (page - 1) * pageSize + 1 : 1;
        var to = pageSize > 0 ? Math.min(page * pageSize, total) : total;
        var nums = [];
        for (var i = 1; i <= pages; i++) {
            if (i === 1 || i === pages || Math.abs(i - page) <= 1) nums.push(i);
            else if (nums[nums.length - 1] !== '...') nums.push('...');
        }
        el.innerHTML =
            '<div>Hiển thị <b>' + from + '–' + to + '</b> / ' + total + ' dòng</div>' +
            '<div class="d-flex align-center gap-2">' +
            '  <span>Số dòng / trang:</span>' +
            '  <select class="form-control form-control-sm pager-size">' +
                 [10, 25, 50, 100, 0].map(function (n) {
                     return '<option value="' + n + '"' + (n === pageSize ? ' selected' : '') + '>' + (n || 'Tất cả') + '</option>';
                 }).join('') +
            '  </select>' +
            '  <div class="pager-btns">' +
            '    <button type="button" class="pager-btn" data-pg="prev"' + (page <= 1 ? ' disabled' : '') + ' title="Trang trước"><i class="ri-arrow-left-s-line"></i></button>' +
                 nums.map(function (n) {
                     return n === '...' ? '<span class="pager-ellipsis">…</span>'
                         : '<button type="button" class="pager-btn' + (n === page ? ' active' : '') + '" data-pg="' + n + '">' + n + '</button>';
                 }).join('') +
            '    <button type="button" class="pager-btn" data-pg="next"' + (page >= pages ? ' disabled' : '') + ' title="Trang sau"><i class="ri-arrow-right-s-line"></i></button>' +
            '  </div>' +
            '</div>';
        el.querySelector('.pager-size').addEventListener('change', function () {
            pageSize = parseInt(this.value, 10);
            localStorage.setItem(cfg.storageKey, pageSize);
            page = 1;
            cfg.onChange();
        });
        el.querySelectorAll('.pager-btn').forEach(function (b) {
            b.addEventListener('click', function () {
                var v = this.dataset.pg;
                if (v === 'prev') page--; else if (v === 'next') page++; else page = parseInt(v, 10);
                cfg.onChange();
            });
        });
    }
    function goToIndex(idx) { if (pageSize > 0 && idx >= 0) page = Math.floor(idx / pageSize) + 1; }
    return { paginate: paginate, render: render, goToIndex: goToIndex };
}

/* ---------- Cấu hình cột hiển thị (dùng chung các màn sổ) ----------
   var colCfg = setupColumnConfig({ storageKey, btnId, columns, fixedNote, onChange });
   - columns: [{key, label, cls, style, always}] — cột always bắt buộc, CỐ ĐỊNH đầu bảng
   - Cột mở rộng: tick chọn ẩn/hiện + kéo ⠿ sắp thứ tự; lưu {hidden, order} (tương thích mảng cũ)
   - colCfg.visible() → mảng cột hiển thị theo thứ tự; colCfg.isHidden(key) */
function setupColumnConfig(cfg) {
    var modalId = cfg.btnId + '-modal';
    var DEFAULT_ORDER = cfg.columns.filter(function (c) { return !c.always; }).map(function (c) { return c.key; });
    var hidden = [], order = DEFAULT_ORDER.slice();
    (function () {
        try {
            var v = JSON.parse(localStorage.getItem(cfg.storageKey));
            if (Array.isArray(v)) { hidden = v; return; }
            if (v && typeof v === 'object') {
                if (Array.isArray(v.hidden)) hidden = v.hidden;
                if (Array.isArray(v.order)) {
                    var known = v.order.filter(function (k) { return DEFAULT_ORDER.indexOf(k) !== -1; });
                    order = known.concat(DEFAULT_ORDER.filter(function (k) { return known.indexOf(k) === -1; }));
                }
            }
        } catch (e) { /* giữ mặc định */ }
    })();
    function visible() {
        var fixed = cfg.columns.filter(function (c) { return c.always; });
        var opt = order.map(function (k) {
            return cfg.columns.find(function (c) { return c.key === k; });
        }).filter(function (c) { return c && hidden.indexOf(c.key) === -1; });
        return fixed.concat(opt);
    }
    document.body.insertAdjacentHTML('beforeend',
        '<div class="modal-backdrop-demo" id="' + modalId + '"><div class="modal-dialog" style="max-width:680px">' +
        '<div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-layout-column-line"></i></span>Cấu hình cột hiển thị</h5>' +
        '<button type="button" class="close" onclick="closeModal(\'' + modalId + '\')">×</button></div>' +
        '<div class="modal-body"><p class="tp-small-text" style="margin-bottom:10px">Tích chọn cột hiển thị; kéo <i class="ri-draggable"></i> để sắp xếp thứ tự. ' +
        (cfg.fixedNote || 'Các cột chuẩn theo mẫu sổ là <b>bắt buộc</b> và cố định ở đầu bảng.') + ' Cài đặt được lưu theo từng màn hình.</p>' +
        '<div id="' + modalId + '-list"></div></div>' +
        '<div class="modal-footer">' +
        '<button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="' + modalId + '-save"><i class="ri-save-3-line"></i> Lưu</button>' +
        '<button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="' + modalId + '-reset"><i class="ri-refresh-line"></i> Khôi phục mặc định</button>' +
        '<button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'' + modalId + '\')"><i class="ri-close-line"></i> Đóng</button>' +
        '</div></div></div>');
    function renderList() {
        var fixed = cfg.columns.filter(function (c) { return c.always; });
        var optional = order.map(function (k) { return cfg.columns.find(function (c) { return c.key === k; }); });
        var fixedHTML = !fixed.length ? '' :
            '<p class="tp-label" style="margin-bottom:6px">Cột chuẩn — cố định vị trí 1–' + fixed.length + '</p>' +
            '<div class="ffcfg-grid" style="margin-bottom:14px">' +
                fixed.map(function (c) {
                    return '<label class="ffcfg-item"><input type="checkbox" checked disabled> ' +
                        c.label.replace('<br>', ' ') + ' <span class="ffcfg-note">(bắt buộc)</span></label>';
                }).join('') +
            '</div>';
        document.getElementById(modalId + '-list').innerHTML =
            fixedHTML +
            '<p class="tp-label" style="margin-bottom:6px">Cột mở rộng — tích chọn hiển thị, kéo <i class="ri-draggable"></i> để sắp xếp thứ tự</p>' +
            '<div class="colcfg-optlist" style="counter-reset:colidx ' + (cfg.counterStart != null ? cfg.counterStart : fixed.length) + '">' +
                optional.map(function (c) {
                    var checked = hidden.indexOf(c.key) === -1;
                    return '<label class="ffcfg-item colcfg-drag" draggable="true" data-key="' + c.key + '">' +
                        '<i class="ri-draggable drag-ico" title="Kéo để sắp xếp"></i>' +
                        '<input type="checkbox" data-colcfg="' + c.key + '"' + (checked ? ' checked' : '') + '> ' +
                        c.label.replace('<br>', ' ') + '</label>';
                }).join('') +
            '</div>';
        var list = document.querySelector('#' + modalId + '-list .colcfg-optlist');
        var dragEl = null;
        list.addEventListener('dragstart', function (e) {
            dragEl = e.target.closest('.colcfg-drag');
            if (dragEl) dragEl.classList.add('dragging');
        });
        list.addEventListener('dragover', function (e) {
            e.preventDefault();
            if (!dragEl) return;
            var over = e.target.closest('.colcfg-drag');
            if (over && over !== dragEl) {
                var r = over.getBoundingClientRect();
                list.insertBefore(dragEl, e.clientY < r.top + r.height / 2 ? over : over.nextElementSibling);
            }
        });
        list.addEventListener('dragend', function () {
            if (dragEl) dragEl.classList.remove('dragging');
            dragEl = null;
        });
    }
    document.getElementById(cfg.btnId).addEventListener('click', function () {
        renderList();
        openModal(modalId);
    });
    document.getElementById(modalId + '-save').addEventListener('click', function () {
        var items = [...document.querySelectorAll('#' + modalId + '-list .colcfg-drag')];
        order = items.map(function (el) { return el.dataset.key; });
        hidden = items.filter(function (el) { return !el.querySelector('input').checked; })
            .map(function (el) { return el.dataset.key; });
        localStorage.setItem(cfg.storageKey, JSON.stringify({ hidden: hidden, order: order }));
        closeModal(modalId);
        cfg.onChange();
        toast('Đã lưu cấu hình cột hiển thị');
    });
    document.getElementById(modalId + '-reset').addEventListener('click', function () {
        hidden = [];
        order = DEFAULT_ORDER.slice();
        localStorage.removeItem(cfg.storageKey);
        renderList();
        cfg.onChange();
        toast('Đã khôi phục cấu hình cột mặc định', 'info');
    });
    return { visible: visible, isHidden: function (k) { return hidden.indexOf(k) !== -1; } };
}

/* ---------- Ẩn / hiện toàn bộ khu vực bộ lọc (dùng chung) ----------
   setupFilterHide({ storageKey, btnId: 'f-hide', bodyId: 'filter-body' }) */
function setupFilterHide(cfg) {
    function apply(hiddenState) {
        document.getElementById(cfg.bodyId).style.display = hiddenState ? 'none' : '';
        document.getElementById(cfg.btnId).innerHTML = hiddenState
            ? '<i class="ri-eye-line"></i> Hiện bộ lọc'
            : '<i class="ri-eye-off-line"></i> Ẩn bộ lọc';
    }
    document.getElementById(cfg.btnId).addEventListener('click', function () {
        var hiddenState = document.getElementById(cfg.bodyId).style.display !== 'none';
        localStorage.setItem(cfg.storageKey, hiddenState ? '1' : '');
        apply(hiddenState);
    });
    apply(localStorage.getItem(cfg.storageKey) === '1');
}

/* ---------- Status pill helper ---------- */
function statusBadge(st) {
    var s = STATUSES[st] || STATUSES[0];
    return '<span class="status-pill ' + s.cls + '"><i class="' + s.icon + '"></i>' + s.label + '</span>';
}

/* ============================================================
   Demo Kế toán HRM — Bảng cân đối phát sinh công nợ (nhiều tài khoản)
   - Tổng hợp theo TỪNG TÀI KHOẢN CÔNG NỢ × TỪNG ĐỐI TƯỢNG.
   - Phát sinh (PS Nợ/Có) dẫn xuất từ JOURNAL_ROWS trong kỳ.
   - Số dư đầu kỳ (SDĐK) seed ổn định theo (TK, đối tượng) — deterministic.
   - SDCK theo tính chất TK: net = ±SDĐK + PS Nợ − PS Có → tách Nợ/Có.
   ============================================================ */
function renderDebtBalancePage() {
    function uniq(a) { return [...new Set(a.filter(Boolean))]; }
    function val(id) { var e = document.getElementById(id); return e ? e.value : ''; }
    function chk(id) { var e = document.getElementById(id); return e ? e.checked : false; }
    function pad(n) { return (n < 10 ? '0' : '') + n; }

    /* Các tài khoản công nợ (đa tài khoản) — thứ tự: tài sản (dư Nợ) trước, nợ phải trả (dư Có) sau */
    var DEBT_ACCOUNTS = [
        { acc: '131', type: 'KH' },
        { acc: '1368', type: 'NB' },
        { acc: '331', type: 'NCC' },
        { acc: '3368', type: 'NB' },
        { acc: '334', type: 'NV' }
    ].map(function (d) { return { acc: d.acc, type: d.type, name: ACC_NAMES[d.acc] || '' }; });

    var TYPE_LABEL = { KH: 'Khách hàng', NCC: 'Nhà cung cấp', NV: 'Nhân viên', NB: 'Nội bộ' };
    var companies = Object.keys(ORG);

    /* Đối tượng của 1 TK = các đối tượng từng phát sinh với TK đó (trên toàn bộ dữ liệu) */
    function objectsOf(acc) {
        return uniq(JOURNAL_ROWS.filter(function (r) { return r[JR.account] === acc && r[JR.object]; })
            .map(function (r) { return r[JR.object]; })).sort();
    }
    /* SDĐK seed ổn định theo (TK, đối tượng): ~80% đối tượng có số dư, 5–250 triệu (tròn 5tr) */
    function seedOpen(acc, obj) {
        var s = acc + '|' + obj, h = 0;
        for (var i = 0; i < s.length; i++) h = (h * 131 + s.charCodeAt(i)) >>> 0;
        if (h % 5 === 0) return 0;
        return ((h % 50) + 1) * 5000000;
    }

    function periodRange(v) {
        var LAST = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        if (v === 'y') return ['2026-01-01', '2026-12-31'];
        if (v[0] === 'q') { var q = +v[1], sm = (q - 1) * 3 + 1; return ['2026-' + pad(sm) + '-01', '2026-' + pad(sm + 2) + '-' + LAST[sm + 1]]; }
        if (v[0] === 'm') { var m = +v.slice(1); return ['2026-' + pad(m) + '-01', '2026-' + pad(m) + '-' + LAST[m - 1]]; }
        return null;
    }

    var allObjects = uniq(DEBT_ACCOUNTS.reduce(function (a, d) { return a.concat(objectsOf(d.acc)); }, [])).sort();

    renderShell('debt',
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="filter-header">' +
        '    <div class="filter-header-left"><div class="tp-icon-chip"><i class="ri-scales-3-line"></i></div>' +
        '      <p class="tp-section-title">Bộ lọc Bảng cân đối phát sinh công nợ</p></div>' +
        '    <div class="d-flex gap-2">' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-hide" title="Ẩn / hiện bộ lọc"><i class="ri-eye-off-line"></i> Ẩn bộ lọc</button>' +
        '    </div>' +
        '  </div>' +
        '  <div id="filter-body">' +
        '    <div class="quick-search-row">' +
        '      <div class="quick-search"><i class="ri-search-line"></i>' +
        '        <input class="form-control form-control-sm" id="f-search" placeholder="Tìm theo mã / tên đối tượng">' +
        '        <button type="button" class="btn-clear-quick-search" id="f-search-clear"><i class="ri-close-line"></i></button></div>' +
        '      <button type="button" class="v2-btn v2-btn--primary btn-compact" id="f-go"><i class="ri-search-line"></i> Tìm kiếm</button>' +
        '      <button type="button" class="v2-btn v2-btn--tertiary btn-compact" id="f-clear"><i class="ri-refresh-line"></i> Nhập lại</button>' +
        '    </div>' +
        '    <div class="form-row filter-grid">' +
        '      <div class="col-md-3"><label class="tp-label">Đơn vị</label><select class="form-control form-control-sm" id="f-company"><option value="">— Tất cả công ty —</option>' +
                companies.map(function (c) { return '<option value="' + c + '"' + (c === 'TPE' ? ' selected' : '') + '>' + c + ' — ' + ORG[c].name + '</option>'; }).join('') +
        '      </select></div>' +
        '      <div class="col-md-3"><label class="tp-label">Kỳ báo cáo</label><select class="form-control form-control-sm" id="f-period">' +
        '        <option value="y">Cả năm 2026</option>' +
        '        <optgroup label="Theo quý"><option value="q1">Quý I/2026</option><option value="q2">Quý II/2026</option><option value="q3">Quý III/2026</option><option value="q4">Quý IV/2026</option></optgroup>' +
        '        <optgroup label="Theo tháng">' + Array.from({ length: 12 }, function (_, i) { return '<option value="m' + (i + 1) + '"' + (i === 0 ? ' selected' : '') + '>Tháng ' + (i + 1) + '/2026</option>'; }).join('') + '</optgroup>' +
        '        <option value="custom">Tùy chọn...</option></select></div>' +
        '      <div class="col-md-3"><label class="tp-label">Từ ngày</label><input type="date" class="form-control form-control-sm" id="f-from" value="2026-01-01"></div>' +
        '      <div class="col-md-3"><label class="tp-label">Đến ngày</label><input type="date" class="form-control form-control-sm" id="f-to" value="2026-01-31"></div>' +
        '      <div class="col-md-3"><label class="tp-label">Loại đối tượng</label><select class="form-control form-control-sm" id="f-type"><option value="">— Tất cả —</option>' +
                Object.keys(TYPE_LABEL).map(function (k) { return '<option value="' + k + '">' + TYPE_LABEL[k] + '</option>'; }).join('') +
        '      </select></div>' +
        '      <div class="col-md-3"><label class="tp-label">Đối tượng</label><select class="form-control form-control-sm" id="f-object"><option value="">— Tất cả —</option>' +
                allObjects.map(function (o) { return '<option value="' + o + '">' + o + ' — ' + objName(o) + '</option>'; }).join('') +
        '      </select></div>' +
        '      <div class="col-md-6"><label class="tp-label">Tài khoản công nợ</label><div class="acc-checks">' +
                DEBT_ACCOUNTS.map(function (d) { return '<label class="acc-chk"><input type="checkbox" class="f-acc" value="' + d.acc + '" checked> ' + d.acc + ' — ' + d.name + '</label>'; }).join('') +
        '      </div></div>' +
        '    </div>' +
        '    <label class="cn-nonzero"><input type="checkbox" id="f-nonzero" checked> Chỉ hiện đối tượng còn số dư hoặc có phát sinh trong kỳ</label>' +
        '  </div>' +
        '</section>' +

        '<section class="tp-card p-3">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left"><div class="tp-icon-chip"><i class="ri-scales-3-line"></i></div>' +
        '      <div><h5>Bảng cân đối phát sinh công nợ</h5>' +
        '      <p class="tp-section-subtitle" id="bcps-sub">Tổng hợp công nợ theo tài khoản × đối tượng · Đơn vị tính: VNĐ</p></div></div>' +
        '    <div class="table-actions">' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-print"><i class="ri-printer-line"></i> In báo cáo</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-excel"><i class="ri-file-excel-2-line"></i> Xuất Excel</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-toggle-all"><i class="ri-expand-up-down-line"></i> Thu gọn / Mở tất cả</button>' +
        '    </div>' +
        '  </div>' +
        '  <div class="table-wrapper scrollbar-thin"><table class="data-table" id="bcps-tbl">' +
        '    <thead>' +
        '      <tr><th rowspan="2" style="min-width:300px">Tài khoản / Đối tượng</th>' +
        '        <th colspan="2" class="text-center th-group-org">Số dư đầu kỳ</th>' +
        '        <th colspan="2" class="text-center th-group">Số phát sinh trong kỳ</th>' +
        '        <th colspan="2" class="text-center th-group-org">Số dư cuối kỳ</th></tr>' +
        '      <tr><th class="text-right">Nợ</th><th class="text-right">Có</th><th class="text-right">Nợ</th><th class="text-right">Có</th><th class="text-right">Nợ</th><th class="text-right">Có</th></tr>' +
        '    </thead><tbody></tbody><tfoot></tfoot>' +
        '  </table></div>' +
        '  <div class="d-flex align-center gap-2 mt-2" id="bcps-summary"></div>' +
        '</section>' +

        '<div class="modal-backdrop-demo" id="print-modal"><div class="modal-dialog" style="max-width:1000px">' +
        '  <div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-printer-line"></i></span>In Bảng cân đối phát sinh công nợ</h5>' +
        '  <button type="button" class="close" onclick="closeModal(\'print-modal\')">×</button></div>' +
        '  <div class="modal-body" id="print-preview" style="max-height:70vh"></div>' +
        '  <div class="modal-footer">' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-do-print"><i class="ri-printer-line"></i> In</button>' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'print-modal\')"><i class="ri-close-line"></i> Đóng</button>' +
        '  </div>' +
        '</div></div><div id="print-area"></div>');

    var tbody = document.querySelector('#bcps-tbl tbody');
    var tfoot = document.querySelector('#bcps-tbl tfoot');
    var expandState = {};

    /* ---------- Tính toán nhóm theo bộ lọc ---------- */
    function computeGroups() {
        var company = val('f-company'), from = val('f-from'), to = val('f-to');
        var typeF = val('f-type'), objF = val('f-object');
        var search = (val('f-search') || '').toLowerCase().trim();
        var nonzero = chk('f-nonzero');
        var selAccs = Array.prototype.map.call(document.querySelectorAll('.f-acc:checked'), function (c) { return c.value; });

        var groups = [], grand = z();
        DEBT_ACCOUNTS.forEach(function (d) {
            if (selAccs.indexOf(d.acc) === -1) return;
            if (typeF && d.type !== typeF) return;
            var sub = z(), objRows = [];
            objectsOf(d.acc).forEach(function (obj) {
                if (objF && obj !== objF) return;
                if (search) { var nm = (obj + ' ' + objName(obj)).toLowerCase(); if (nm.indexOf(search) === -1) return; }
                var pno = 0, pco = 0;
                JOURNAL_ROWS.forEach(function (r) {
                    if (r[JR.account] !== d.acc || r[JR.object] !== obj) return;
                    if (company && r[JR.company] !== company) return;
                    if (from && r[JR.date] < from) return;
                    if (to && r[JR.date] > to) return;
                    pno += r[JR.debit] || 0; pco += r[JR.credit] || 0;
                });
                var signedOpen = (isDebitNature(d.acc) ? 1 : -1) * seedOpen(d.acc, obj);
                var ono = signedOpen > 0 ? signedOpen : 0, oco = signedOpen < 0 ? -signedOpen : 0;
                var net = signedOpen + pno - pco;
                var cno = net > 0 ? net : 0, cco = net < 0 ? -net : 0;
                if (nonzero && !(ono || oco || pno || pco)) return;
                var row = { obj: obj, ono: ono, oco: oco, pno: pno, pco: pco, cno: cno, cco: cco };
                objRows.push(row); add(sub, row); add(grand, row);
            });
            if (objRows.length) groups.push({ acc: d.acc, name: d.name, rows: objRows, sub: sub });
        });
        return { groups: groups, grand: grand };
    }
    function z() { return { ono: 0, oco: 0, pno: 0, pco: 0, cno: 0, cco: 0 }; }
    function add(t, r) { ['ono', 'oco', 'pno', 'pco', 'cno', 'cco'].forEach(function (k) { t[k] += r[k]; }); }
    function m(n) { return '<td class="text-right num">' + (n ? fmtMoney(n) : '') + '</td>'; }
    function cells(o) { return m(o.ono) + m(o.oco) + m(o.pno) + m(o.pco) + m(o.cno) + m(o.cco); }

    function draw() {
        var data = computeGroups();
        if (!data.groups.length) {
            tbody.innerHTML = '<tr><td colspan="7"><div class="empty-state"><div class="es-icon"><i class="ri-inbox-line"></i></div>Không có dữ liệu công nợ khớp bộ lọc.</div></td></tr>';
            tfoot.innerHTML = ''; document.getElementById('bcps-summary').innerHTML = ''; return;
        }
        var html = '', objCount = 0;
        data.groups.forEach(function (g) {
            if (expandState[g.acc] === undefined) expandState[g.acc] = true;
            var open = expandState[g.acc];
            objCount += g.rows.length;
            html += '<tr class="row-acc" data-acc="' + g.acc + '">' +
                '<td><span class="acc-caret' + (open ? ' open' : '') + '"><i class="ri-arrow-right-s-line"></i></span><b>' + g.acc + ' — ' + g.name + '</b> <span class="acc-count">(' + g.rows.length + ' đối tượng)</span></td>' +
                cells(g.sub) + '</tr>';
            g.rows.forEach(function (o) {
                html += '<tr class="row-obj acc-' + g.acc + '"' + (open ? '' : ' style="display:none"') + '>' +
                    '<td class="obj-cell">' + o.obj + ' — ' + objName(o.obj) + '</td>' + cells(o) + '</tr>';
            });
        });
        tbody.innerHTML = html;
        tfoot.innerHTML = '<tr class="row-total"><td><b>TỔNG CỘNG</b></td>' + cells(data.grand) + '</tr>';

        var g = data.grand;
        document.getElementById('bcps-summary').innerHTML =
            '<span class="tp-badge">Số TK công nợ: ' + data.groups.length + '</span>' +
            '<span class="tp-badge">Số đối tượng: ' + objCount + '</span>' +
            '<span class="tp-badge">Tổng dư Nợ cuối kỳ: ' + fmtMoney(g.cno) + '</span>' +
            '<span class="tp-badge">Tổng dư Có cuối kỳ: ' + fmtMoney(g.cco) + '</span>' +
            '<span class="small">SDCK = SDĐK ± (PS Nợ − PS Có) theo tính chất tài khoản.</span>';
    }

    /* ---------- Bản in ---------- */
    function printHTML() {
        var data = computeGroups();
        var company = val('f-company');
        var unit = company ? (company + ' — ' + ORG[company].name) : 'Toàn bộ đơn vị (hợp cộng)';
        var rows = '';
        data.groups.forEach(function (g) {
            rows += '<tr class="p-total"><td colspan="7" style="text-align:left"><b>' + g.acc + ' — ' + g.name + '</b></td></tr>';
            g.rows.forEach(function (o) {
                rows += '<tr><td>' + o.obj + ' — ' + objName(o.obj) + '</td>' +
                    pr(o.ono) + pr(o.oco) + pr(o.pno) + pr(o.pco) + pr(o.cno) + pr(o.cco) + '</tr>';
            });
            rows += '<tr class="p-total"><td style="text-align:right"><i>Cộng ' + g.acc + '</i></td>' +
                pr(g.sub.ono) + pr(g.sub.oco) + pr(g.sub.pno) + pr(g.sub.pco) + pr(g.sub.cno) + pr(g.sub.cco) + '</tr>';
        });
        var gr = data.grand;
        function pr(n) { return '<td class="pr">' + (n ? fmtMoney(n) : '') + '</td>'; }
        return '<div class="print-sheet">' +
            '<table class="p-head"><tr><td><b>Đơn vị:</b> ' + unit + '<br><b>Địa chỉ:</b> ……………………………</td>' +
            '<td style="text-align:right"><b>Mẫu số S06-DN</b><br><i>(Ban hành theo TT 99/2025/TT-BTC)</i></td></tr></table>' +
            '<div class="p-title">BẢNG CÂN ĐỐI PHÁT SINH CÔNG NỢ</div>' +
            '<div class="p-sub">Từ ngày ' + fmtDate(val('f-from')) + ' đến ngày ' + fmtDate(val('f-to')) + '</div>' +
            '<table class="p-grid" style="margin-top:8px"><thead>' +
            '<tr><th rowspan="2">Tài khoản / Đối tượng</th><th colspan="2">Số dư đầu kỳ</th><th colspan="2">Số phát sinh</th><th colspan="2">Số dư cuối kỳ</th></tr>' +
            '<tr><th>Nợ</th><th>Có</th><th>Nợ</th><th>Có</th><th>Nợ</th><th>Có</th></tr></thead><tbody>' + rows +
            '<tr class="p-total"><td style="text-align:right"><b>TỔNG CỘNG</b></td>' +
            pr(gr.ono) + pr(gr.oco) + pr(gr.pno) + pr(gr.pco) + pr(gr.cno) + pr(gr.cco) + '</tr></tbody></table>' +
            '<table class="p-sign"><tr><td>Người lập biểu<br><i>(Ký, họ tên)</i></td><td>Kế toán trưởng<br><i>(Ký, họ tên)</i></td><td>Giám đốc<br><i>(Ký, họ tên, đóng dấu)</i></td></tr></table>' +
            '</div>';
    }

    /* ---------- Sự kiện ---------- */
    tbody.addEventListener('click', function (e) {
        var tr = e.target.closest('.row-acc'); if (!tr) return;
        var acc = tr.getAttribute('data-acc');
        expandState[acc] = !expandState[acc];
        tr.querySelector('.acc-caret').classList.toggle('open', expandState[acc]);
        Array.prototype.forEach.call(document.querySelectorAll('.acc-' + acc), function (r) { r.style.display = expandState[acc] ? '' : 'none'; });
    });
    document.getElementById('btn-toggle-all').addEventListener('click', function () {
        var anyOpen = Object.keys(expandState).some(function (k) { return expandState[k]; });
        computeGroups().groups.forEach(function (g) { expandState[g.acc] = !anyOpen; });
        draw();
    });

    var fPeriod = document.getElementById('f-period'), fFrom = document.getElementById('f-from'), fTo = document.getElementById('f-to');
    fPeriod.addEventListener('change', function () {
        var rg = periodRange(fPeriod.value);
        if (rg) { fFrom.value = rg[0]; fTo.value = rg[1]; }
        draw();
    });
    [fFrom, fTo].forEach(function (el) { el.addEventListener('change', function () { fPeriod.value = 'custom'; draw(); }); });
    ['f-company', 'f-type', 'f-object'].forEach(function (id) { document.getElementById(id).addEventListener('change', draw); });
    Array.prototype.forEach.call(document.querySelectorAll('.f-acc'), function (c) { c.addEventListener('change', draw); });
    document.getElementById('f-nonzero').addEventListener('change', draw);

    var fSearch = document.getElementById('f-search'), fSearchClear = document.getElementById('f-search-clear');
    function syncClear() { fSearchClear.style.display = fSearch.value ? 'block' : 'none'; }
    fSearch.addEventListener('input', syncClear);
    fSearch.addEventListener('keydown', function (e) { if (e.key === 'Enter') draw(); });
    fSearchClear.addEventListener('click', function () { fSearch.value = ''; syncClear(); draw(); });
    document.getElementById('f-go').addEventListener('click', draw);
    document.getElementById('f-clear').addEventListener('click', function () {
        document.getElementById('f-company').value = 'TPE';
        fPeriod.value = 'm1'; fFrom.value = '2026-01-01'; fTo.value = '2026-01-31';
        document.getElementById('f-type').value = ''; document.getElementById('f-object').value = '';
        document.getElementById('f-nonzero').checked = true; fSearch.value = ''; syncClear();
        Array.prototype.forEach.call(document.querySelectorAll('.f-acc'), function (c) { c.checked = true; });
        draw();
    });
    document.getElementById('f-hide').addEventListener('click', function () {
        var b = document.getElementById('filter-body'), btn = this;
        var hidden = b.style.display === 'none';
        b.style.display = hidden ? '' : 'none';
        btn.innerHTML = hidden ? '<i class="ri-eye-off-line"></i> Ẩn bộ lọc' : '<i class="ri-eye-line"></i> Hiện bộ lọc';
    });
    document.getElementById('btn-excel').addEventListener('click', function () { toast('Đã xuất Excel (demo).', 'info'); });
    document.getElementById('btn-print').addEventListener('click', function () {
        document.getElementById('print-preview').innerHTML = printHTML(); openModal('print-modal');
    });
    document.getElementById('btn-do-print').addEventListener('click', function () {
        document.getElementById('print-area').innerHTML = printHTML(); window.print();
    });

    draw();
}

/* ============================================================
   Demo Kế toán HRM — Bảng cân đối phát sinh trên nhiều tài khoản (trial balance)
   - Mỗi tài khoản: SDĐK (Nợ/Có) · Phát sinh (Nợ/Có) · SDCK (Nợ/Có).
   - PS dẫn xuất từ JOURNAL_ROWS; SDĐK từ openingOf(); SDCK theo tính chất TK.
   - Thêm dòng Vốn CSH (411) cân số dư đầu kỳ → toàn bảng cân Nợ = Có cả 3 cặp cột.
   ============================================================ */
function renderTrialBalancePage() {
    function uniq(a) { return [...new Set(a.filter(Boolean))]; }
    function val(id) { var e = document.getElementById(id); return e ? e.value : ''; }
    function chk(id) { var e = document.getElementById(id); return e ? e.checked : false; }
    function pad(n) { return (n < 10 ? '0' : '') + n; }
    function accName(acc) { return ACC_NAMES[acc] || (acc === '411' ? 'Vốn đầu tư của chủ sở hữu' : ''); }

    var companies = Object.keys(ORG);
    var allAccounts = uniq([].concat(
        JOURNAL_ROWS.map(function (r) { return r[JR.account]; }),
        Object.keys(ACC_NAMES),
        Object.keys(OPENING).reduce(function (a, c) { return a.concat(Object.keys(OPENING[c])); }, [])
    )).sort();
    /* Danh sách tài khoản cho select lọc (gồm cả TK vốn 411 do báo cáo tự thêm) */
    var selectAccounts = uniq(allAccounts.concat(['411'])).sort();

    function openingSum(acc, company) {
        if (company) return openingOf(company, acc);
        return Object.keys(OPENING).reduce(function (s, c) { return s + openingOf(c, acc); }, 0);
    }
    function periodRange(v) {
        var LAST = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        if (v === 'y') return ['2026-01-01', '2026-12-31'];
        if (v[0] === 'q') { var q = +v[1], sm = (q - 1) * 3 + 1; return ['2026-' + pad(sm) + '-01', '2026-' + pad(sm + 2) + '-' + LAST[sm + 1]]; }
        if (v[0] === 'm') { var m = +v.slice(1); return ['2026-' + pad(m) + '-01', '2026-' + pad(m) + '-' + LAST[m - 1]]; }
        return null;
    }

    renderShell('trial',
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="filter-header">' +
        '    <div class="filter-header-left"><div class="tp-icon-chip"><i class="ri-scales-3-line"></i></div>' +
        '      <p class="tp-section-title">Bộ lọc Bảng cân đối phát sinh trên nhiều tài khoản</p></div>' +
        '    <div class="d-flex gap-2">' +
        '      <button type="button" class="v2-btn v2-btn--tertiary btn-compact" id="f-clear"><i class="ri-refresh-line"></i> Nhập lại</button>' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-hide" title="Ẩn / hiện bộ lọc"><i class="ri-eye-off-line"></i> Ẩn bộ lọc</button>' +
        '    </div>' +
        '  </div>' +
        '  <div id="filter-body">' +
        '    <div class="form-row filter-grid">' +
        '      <div class="col-md-3"><label class="tp-label">Tài khoản</label><select class="form-control form-control-sm" id="f-account"><option value="">— Tất cả tài khoản —</option>' +
                selectAccounts.map(function (a) { return '<option value="' + a + '">' + a + ' — ' + accName(a) + '</option>'; }).join('') +
        '      </select></div>' +
        '      <div class="col-md-3"><label class="tp-label">Đơn vị</label><select class="form-control form-control-sm" id="f-company"><option value="">— Tất cả công ty (hợp cộng) —</option>' +
                companies.map(function (c) { return '<option value="' + c + '"' + (c === 'TPE' ? ' selected' : '') + '>' + c + ' — ' + ORG[c].name + '</option>'; }).join('') +
        '      </select></div>' +
        '      <div class="col-md-3"><label class="tp-label">Kỳ báo cáo</label><select class="form-control form-control-sm" id="f-period">' +
        '        <option value="y">Cả năm 2026</option>' +
        '        <optgroup label="Theo quý"><option value="q1">Quý I/2026</option><option value="q2">Quý II/2026</option><option value="q3">Quý III/2026</option><option value="q4">Quý IV/2026</option></optgroup>' +
        '        <optgroup label="Theo tháng">' + Array.from({ length: 12 }, function (_, i) { return '<option value="m' + (i + 1) + '"' + (i === 0 ? ' selected' : '') + '>Tháng ' + (i + 1) + '/2026</option>'; }).join('') + '</optgroup>' +
        '        <option value="custom">Tùy chọn...</option></select></div>' +
        '      <div class="col-md-3"><label class="tp-label">Từ ngày</label><input type="date" class="form-control form-control-sm" id="f-from" value="2026-01-01"></div>' +
        '      <div class="col-md-3"><label class="tp-label">Đến ngày</label><input type="date" class="form-control form-control-sm" id="f-to" value="2026-01-31"></div>' +
        '    </div>' +
        '    <label class="cn-nonzero"><input type="checkbox" id="f-nonzero" checked> Chỉ hiện tài khoản còn số dư hoặc có phát sinh trong kỳ</label>' +
        '  </div>' +
        '</section>' +

        '<section class="tp-card p-3">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left"><div class="tp-icon-chip"><i class="ri-scales-3-line"></i></div>' +
        '      <div><h5>Bảng cân đối phát sinh trên nhiều tài khoản</h5>' +
        '      <p class="tp-section-subtitle">Tổng hợp số dư &amp; phát sinh theo từng tài khoản · Đơn vị tính: VNĐ</p></div></div>' +
        '    <div class="table-actions">' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-print"><i class="ri-printer-line"></i> In báo cáo</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-excel"><i class="ri-file-excel-2-line"></i> Xuất Excel</button>' +
        '    </div>' +
        '  </div>' +
        '  <div class="table-wrapper scrollbar-thin"><table class="data-table" id="tbps-tbl">' +
        '    <thead>' +
        '      <tr><th rowspan="2" style="min-width:80px">Số hiệu<br>TK</th><th rowspan="2" style="min-width:280px">Tên tài khoản</th>' +
        '        <th colspan="2" class="text-center th-group-org">Số dư đầu kỳ</th>' +
        '        <th colspan="2" class="text-center th-group">Số phát sinh trong kỳ</th>' +
        '        <th colspan="2" class="text-center th-group-org">Số dư cuối kỳ</th></tr>' +
        '      <tr><th class="text-right">Nợ</th><th class="text-right">Có</th><th class="text-right">Nợ</th><th class="text-right">Có</th><th class="text-right">Nợ</th><th class="text-right">Có</th></tr>' +
        '    </thead><tbody></tbody><tfoot></tfoot>' +
        '  </table></div>' +
        '  <div class="d-flex align-center gap-2 mt-2" id="tbps-summary"></div>' +
        '</section>' +

        '<div class="modal-backdrop-demo" id="print-modal"><div class="modal-dialog" style="max-width:960px">' +
        '  <div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-printer-line"></i></span>In Bảng cân đối phát sinh trên nhiều tài khoản — Mẫu số S06-DN</h5>' +
        '  <button type="button" class="close" onclick="closeModal(\'print-modal\')">×</button></div>' +
        '  <div class="modal-body" id="print-preview" style="max-height:70vh"></div>' +
        '  <div class="modal-footer">' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-do-print"><i class="ri-printer-line"></i> In</button>' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'print-modal\')"><i class="ri-close-line"></i> Đóng</button>' +
        '  </div>' +
        '</div></div><div id="print-area"></div>');

    var tbody = document.querySelector('#tbps-tbl tbody');
    var tfoot = document.querySelector('#tbps-tbl tfoot');

    function z() { return { opNo: 0, opCo: 0, psNo: 0, psCo: 0, ckNo: 0, ckCo: 0 }; }
    function add(t, r) { ['opNo', 'opCo', 'psNo', 'psCo', 'ckNo', 'ckCo'].forEach(function (k) { t[k] += r[k]; }); }

    /* Tính tất cả dòng TK (chưa lọc hiển thị) + dòng vốn 411 cân SDĐK */
    function computeAll() {
        var company = val('f-company'), from = val('f-from'), to = val('f-to');
        var rows = allAccounts.map(function (acc) {
            var op = openingSum(acc, company), deb = isDebitNature(acc);
            var psNo = 0, psCo = 0;
            JOURNAL_ROWS.forEach(function (r) {
                if (r[JR.account] !== acc) return;
                if (company && r[JR.company] !== company) return;
                if (from && r[JR.date] < from) return;
                if (to && r[JR.date] > to) return;
                psNo += r[JR.debit] || 0; psCo += r[JR.credit] || 0;
            });
            var signedOpen = (deb ? 1 : -1) * op;
            var net = signedOpen + psNo - psCo;
            return { acc: acc, opNo: deb ? op : 0, opCo: deb ? 0 : op, psNo: psNo, psCo: psCo, ckNo: net > 0 ? net : 0, ckCo: net < 0 ? -net : 0 };
        });
        /* Dòng vốn CSH 411 để tổng SDĐK cân (SDCK cũng cân vì PS luôn cân theo bút toán) */
        var sNo = 0, sCo = 0; rows.forEach(function (r) { sNo += r.opNo; sCo += r.opCo; });
        var imb = sNo - sCo;
        if (Math.abs(imb) >= 1) {
            var addNo = imb < 0 ? -imb : 0, addCo = imb > 0 ? imb : 0;
            var ex = rows.filter(function (r) { return r.acc === '411'; })[0];
            if (ex) { ex.opNo += addNo; ex.opCo += addCo; ex.ckNo += addNo; ex.ckCo += addCo; }
            else rows.push({ acc: '411', opNo: addNo, opCo: addCo, psNo: 0, psCo: 0, ckNo: addNo, ckCo: addCo });
        }
        return rows.sort(function (a, b) { return a.acc < b.acc ? -1 : 1; });
    }

    function m(n) { return '<td class="text-right num">' + (n ? fmtMoney(n) : '') + '</td>'; }
    function cells(o) { return m(o.opNo) + m(o.opCo) + m(o.psNo) + m(o.psCo) + m(o.ckNo) + m(o.ckCo); }

    function display() {
        var account = val('f-account'), nonzero = chk('f-nonzero');
        return computeAll().filter(function (r) {
            if (account && r.acc !== account) return false;
            if (nonzero && !(r.opNo || r.opCo || r.psNo || r.psCo)) return false;
            return true;
        });
    }

    function draw() {
        var rows = display();
        if (!rows.length) {
            tbody.innerHTML = '<tr><td colspan="8"><div class="empty-state"><div class="es-icon"><i class="ri-inbox-line"></i></div>Không có tài khoản khớp bộ lọc.</div></td></tr>';
            tfoot.innerHTML = ''; document.getElementById('tbps-summary').innerHTML = ''; return;
        }
        tbody.innerHTML = rows.map(function (r) {
            return '<tr><td class="text-center"><b>' + r.acc + '</b></td><td>' + accName(r.acc) + '</td>' + cells(r) + '</tr>';
        }).join('');
        var tot = z(); rows.forEach(function (r) { add(tot, r); });
        tfoot.innerHTML = '<tr class="row-total"><td class="text-center"><b>—</b></td><td><b>TỔNG CỘNG</b></td>' + cells(tot) + '</tr>';

        var balanced = tot.opNo === tot.opCo && tot.psNo === tot.psCo && tot.ckNo === tot.ckCo;
        var filtered = val('f-account') !== '';
        document.getElementById('tbps-summary').innerHTML =
            '<span class="tp-badge">Số tài khoản: ' + rows.length + '</span>' +
            '<span class="tp-small-text">Kiểm tra cân đối (Nợ = Có ở cả 3 cặp cột):</span> ' +
            (balanced ? '<span class="status-pill st-done"><i class="ri-checkbox-circle-line"></i>CÂN ĐỐI</span>'
                : (filtered ? '<span class="status-pill st-paused"><i class="ri-filter-line"></i>Đang lọc — tổng theo dòng hiển thị</span>'
                    : '<span class="status-pill st-cancel"><i class="ri-error-warning-line"></i>LỆCH</span>'));
    }

    /* ---------- Bản in ---------- */
    function printHTML() {
        var rows = display(), tot = z(); rows.forEach(function (r) { add(tot, r); });
        var company = val('f-company');
        var unit = company ? (company + ' — ' + ORG[company].name) : 'Toàn bộ đơn vị (hợp cộng)';
        function pr(n) { return '<td class="pr">' + (n ? fmtMoney(n) : '') + '</td>'; }
        var body = rows.map(function (r) {
            return '<tr><td class="pc">' + r.acc + '</td><td>' + accName(r.acc) + '</td>' +
                pr(r.opNo) + pr(r.opCo) + pr(r.psNo) + pr(r.psCo) + pr(r.ckNo) + pr(r.ckCo) + '</tr>';
        }).join('');
        return '<div class="print-sheet">' +
            '<table class="p-head"><tr><td><b>Đơn vị:</b> ' + unit + '<br><b>Địa chỉ:</b> ……………………………</td>' +
            '<td style="text-align:right"><b>Mẫu số S06-DN</b><br><i>(Ban hành theo TT 99/2025/TT-BTC)</i></td></tr></table>' +
            '<div class="p-title">BẢNG CÂN ĐỐI PHÁT SINH TRÊN NHIỀU TÀI KHOẢN</div>' +
            '<div class="p-sub">Từ ngày ' + fmtDate(val('f-from')) + ' đến ngày ' + fmtDate(val('f-to')) + '</div>' +
            '<table class="p-grid" style="margin-top:8px"><thead>' +
            '<tr><th rowspan="2">Số hiệu TK</th><th rowspan="2">Tên tài khoản</th><th colspan="2">Số dư đầu kỳ</th><th colspan="2">Số phát sinh</th><th colspan="2">Số dư cuối kỳ</th></tr>' +
            '<tr><th>Nợ</th><th>Có</th><th>Nợ</th><th>Có</th><th>Nợ</th><th>Có</th></tr></thead><tbody>' + body +
            '<tr class="p-total"><td class="pc">—</td><td><b>TỔNG CỘNG</b></td>' +
            pr(tot.opNo) + pr(tot.opCo) + pr(tot.psNo) + pr(tot.psCo) + pr(tot.ckNo) + pr(tot.ckCo) + '</tr></tbody></table>' +
            '<table class="p-sign"><tr><td>Người lập biểu<br><i>(Ký, họ tên)</i></td><td>Kế toán trưởng<br><i>(Ký, họ tên)</i></td><td>Giám đốc<br><i>(Ký, họ tên, đóng dấu)</i></td></tr></table>' +
            '</div>';
    }

    /* ---------- Sự kiện ---------- */
    var fPeriod = document.getElementById('f-period'), fFrom = document.getElementById('f-from'), fTo = document.getElementById('f-to');
    fPeriod.addEventListener('change', function () { var rg = periodRange(fPeriod.value); if (rg) { fFrom.value = rg[0]; fTo.value = rg[1]; } draw(); });
    [fFrom, fTo].forEach(function (el) { el.addEventListener('change', function () { fPeriod.value = 'custom'; draw(); }); });
    document.getElementById('f-company').addEventListener('change', draw);
    document.getElementById('f-account').addEventListener('change', draw);
    document.getElementById('f-nonzero').addEventListener('change', draw);
    document.getElementById('f-clear').addEventListener('click', function () {
        document.getElementById('f-company').value = 'TPE';
        fPeriod.value = 'm1'; fFrom.value = '2026-01-01'; fTo.value = '2026-01-31';
        document.getElementById('f-account').value = '';
        document.getElementById('f-nonzero').checked = true; draw();
    });
    document.getElementById('f-hide').addEventListener('click', function () {
        var b = document.getElementById('filter-body');
        var hidden = b.style.display === 'none';
        b.style.display = hidden ? '' : 'none';
        this.innerHTML = hidden ? '<i class="ri-eye-off-line"></i> Ẩn bộ lọc' : '<i class="ri-eye-line"></i> Hiện bộ lọc';
    });
    document.getElementById('btn-excel').addEventListener('click', function () { toast('Đã xuất Excel (demo).', 'info'); });
    document.getElementById('btn-print').addEventListener('click', function () { document.getElementById('print-preview').innerHTML = printHTML(); openModal('print-modal'); });
    document.getElementById('btn-do-print').addEventListener('click', function () { document.getElementById('print-area').innerHTML = printHTML(); window.print(); });

    draw();
}

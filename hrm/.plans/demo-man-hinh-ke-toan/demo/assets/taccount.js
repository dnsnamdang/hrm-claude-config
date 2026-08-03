/* ============================================================
   Demo Kế toán HRM — SỔ TỔNG HỢP CHỮ T CỦA MỘT TÀI KHOẢN
   Tham khảo file Excel "Sổ tổng hợp chữ T của một tài khoản - 20260525154958.xlsx"
   - Bản TỔNG HỢP theo TK đối ứng (KHÔNG phải chi tiết chứng từ):
     chọn 1 tài khoản → mỗi dòng = 1 TK đối ứng, tổng PS Nợ / PS Có giữa 2 TK.
   - SDĐK + Tổng phát sinh + SDCK (tái dùng công thức số dư như Sổ Cái để KHỚP số).
   - Hiển thị: (a) thẻ "chữ T" trực quan (Nợ trái / Có phải) + (b) bảng đúng mẫu Excel.
   - Nguồn dữ liệu demo: JOURNAL_ROWS. TK đối ứng = TK ở vế ngược lại cùng chứng từ;
     chứng từ nhiều vế → phân bổ theo tỷ lệ số tiền (tổng luôn khớp Cộng phát sinh).
   ============================================================ */

/* Số dư theo tính chất TK (giống ledger.js): dư Nợ = +Nợ−Có; dư Có = +Có−Nợ */
function taApplyBalance(acc, bal, debit, credit) {
    return isDebitNature(acc) ? bal + debit - credit : bal + credit - debit;
}
/* SDĐK = số dư đầu năm + toàn bộ PS trước "Từ ngày" (theo TK + Công ty; trống = mọi pháp nhân) */
function taOpeningBalance(acc, company, from) {
    var bal = 0;
    if (company) bal = openingOf(company, acc);
    else Object.keys(OPENING).forEach(function (c) { bal += openingOf(c, acc); });
    JOURNAL_ROWS.forEach(function (r) {
        if (r[JR.account] === acc && (!company || r[JR.company] === company) && from && r[JR.date] < from) {
            bal = taApplyBalance(acc, bal, r[JR.debit], r[JR.credit]);
        }
    });
    return bal;
}
/* Gom phát sinh của TK theo TK đối ứng trong kỳ (phân bổ tỷ lệ khi chứng từ nhiều vế) */
function taBreakdown(acc, company, from, to) {
    var map = {}, totD = 0, totC = 0;
    JOURNAL_ROWS.forEach(function (L) {
        if (L[JR.account] !== acc) return;
        if (company && L[JR.company] !== company) return;
        if (from && L[JR.date] < from) return;
        if (to && L[JR.date] > to) return;
        var isD = L[JR.debit] > 0;
        var amt = isD ? L[JR.debit] : L[JR.credit];
        if (!amt) return;
        var opp = JOURNAL_ROWS.filter(function (o) {
            return o[JR.docNo] === L[JR.docNo] && o[JR.company] === L[JR.company] &&
                o[JR.line] !== L[JR.line] && (isD ? o[JR.credit] > 0 : o[JR.debit] > 0);
        });
        var sumOpp = opp.reduce(function (s, o) { return s + (isD ? o[JR.credit] : o[JR.debit]); }, 0);
        opp.forEach(function (o) {
            var oamt = isD ? o[JR.credit] : o[JR.debit];
            var share = sumOpp > 0 ? amt * (oamt / sumOpp) : 0;
            var c = o[JR.account];
            map[c] = map[c] || { debit: 0, credit: 0 };
            if (isD) map[c].debit += share; else map[c].credit += share;
        });
        if (isD) totD += amt; else totC += amt;
    });
    return { map: map, totD: totD, totC: totC };
}

function renderTAccountPage() {
    function uniq(vals) { return [...new Set(vals.filter(Boolean))].sort(); }
    function selOptions(list, labelFn, allLabel) {
        return '<option value="">' + (allLabel || '— Tất cả —') + '</option>' + list.map(function (v) {
            return '<option value="' + v + '">' + (labelFn ? labelFn(v) : v) + '</option>';
        }).join('');
    }
    var ACCOUNTS = uniq(JOURNAL_ROWS.map(function (r) { return r[JR.account]; }));
    function accLabel(a) { return a + ' — ' + (ACC_NAMES[a] || ''); }

    renderShell('taccount',
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="filter-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-filter-3-line"></i></div>' +
        '      <p class="tp-section-title">Bộ lọc Sổ tổng hợp chữ T của một tài khoản</p>' +
        '    </div>' +
        '    <div class="d-flex gap-2">' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="ff-gear"><i class="ri-settings-3-line"></i> Cài đặt bộ lọc</button>' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-hide" title="Ẩn / hiện toàn bộ khu vực bộ lọc"><i class="ri-eye-off-line"></i> Ẩn bộ lọc</button>' +
        '    </div>' +
        '  </div>' +
        '  <div id="filter-body">' +
        '  <div class="form-row filter-grid" id="ff-default"></div>' +
        '  <div id="ff-adv">' +
        '    <div class="form-row filter-grid">' +
        '      <div class="col-md-3" data-ff="f-account"><label class="tp-label">Tài khoản <span style="color:#dc2626">*</span></label>' +
        '        <select class="form-control form-control-sm" id="f-account">' + ACCOUNTS.map(function (a) { return '<option value="' + a + '"' + (a === '131' ? ' selected' : '') + '>' + accLabel(a) + '</option>'; }).join('') + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-period"><label class="tp-label">Kỳ báo cáo</label>' +
        '        <select class="form-control form-control-sm" id="f-period">' +
        '          <option value="y">Cả năm 2026</option>' +
        '          <optgroup label="Theo quý"><option value="q1">Quý I/2026</option><option value="q2">Quý II/2026</option><option value="q3">Quý III/2026</option><option value="q4">Quý IV/2026</option></optgroup>' +
        '          <optgroup label="Theo tháng">' + Array.from({ length: 12 }, function (_, i) { return '<option value="m' + (i + 1) + '">Tháng ' + (i + 1) + '/2026</option>'; }).join('') + '</optgroup>' +
        '          <option value="custom">Tùy chọn...</option>' +
        '        </select></div>' +
        '      <div class="col-md-3" data-ff="f-from"><label class="tp-label">Từ ngày</label><input type="date" class="form-control form-control-sm" id="f-from" value="2026-01-01"></div>' +
        '      <div class="col-md-3" data-ff="f-to"><label class="tp-label">Đến ngày</label><input type="date" class="form-control form-control-sm" id="f-to" value="2026-12-31"></div>' +
        '      <div class="col-md-3" data-ff="f-company"><label class="tp-label">Đơn vị</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-company">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.company]; })), function (c) { return c + ' — ' + ORG[c].name; }, '— Tất cả công ty —') + '</select></div>' +
        '    </div>' +
        '  </div>' +
        '  <div class="quick-search-row" style="margin-top:8px">' +
        '    <div class="quick-search">' +
        '      <i class="ri-search-line"></i>' +
        '      <input class="form-control form-control-sm" id="f-search" placeholder="Tìm TK đối ứng theo số hiệu / tên tài khoản">' +
        '      <button type="button" class="btn-clear-quick-search" id="f-search-clear"><i class="ri-close-line"></i></button>' +
        '    </div>' +
        '    <button type="button" class="v2-btn v2-btn--primary btn-compact" id="f-go"><i class="ri-search-line"></i> Tìm kiếm</button>' +
        '    <button type="button" class="v2-btn v2-btn--tertiary btn-compact" id="f-clear"><i class="ri-refresh-line"></i> Nhập lại</button>' +
        '  </div>' +
        '  </div>' +
        '</section>' +

        /* ----- Sổ tổng hợp chữ T (đúng mẫu Excel) ----- */
        '<section class="tp-card p-3">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-t-box-line"></i></div>' +
        '      <div><h5 id="ta-title">Sổ tổng hợp chữ T</h5><p class="tp-section-subtitle" id="ta-sub"></p></div>' +
        '    </div>' +
        '    <div class="table-actions">' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-print"><i class="ri-printer-line"></i> In sổ</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-excel"><i class="ri-file-excel-2-line"></i> Xuất Excel</button>' +
        '    </div>' +
        '  </div>' +
        '  <div id="ta-open" style="font-size:12.5px;margin:2px 0 8px;padding:6px 12px;background:#f8fafc;border:1px solid #e5e7eb;border-radius:.4rem"></div>' +
        '  <div class="table-wrapper scrollbar-thin"><table class="data-table" id="tatbl">' +
        '    <thead>' +
        '      <tr><th rowspan="2" style="min-width:110px">Tk đối ứng</th><th rowspan="2" style="min-width:260px">Tên tài khoản</th><th colspan="2" class="text-center">Số phát sinh</th></tr>' +
        '      <tr id="tatbl-head2"><th class="text-right" data-sk="debit" style="min-width:150px">Nợ</th><th class="text-right" data-sk="credit" style="min-width:150px">Có</th></tr>' +
        '    </thead>' +
        '    <tbody></tbody><tfoot></tfoot>' +
        '  </table></div>' +
        '</section>' +

        /* ----- Modal In ----- */
        '<div class="modal-backdrop-demo" id="print-modal"><div class="modal-dialog" style="max-width:820px">' +
        '  <div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-printer-line"></i></span>In Sổ tổng hợp chữ T của một tài khoản</h5>' +
        '  <button type="button" class="close" onclick="closeModal(\'print-modal\')">×</button></div>' +
        '  <div class="modal-body" id="print-preview" style="max-height:70vh"></div>' +
        '  <div class="modal-footer">' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-do-print"><i class="ri-printer-line"></i> In</button>' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'print-modal\')"><i class="ri-close-line"></i> Đóng</button>' +
        '  </div>' +
        '</div></div>' +
        '<div id="print-area"></div>');

    function val(id) { return document.getElementById(id).value; }

    /* Kỳ → ngày */
    document.getElementById('f-period').addEventListener('change', function () {
        var range = PERIODS[this.value];
        if (range) { document.getElementById('f-from').value = range[0]; document.getElementById('f-to').value = range[1]; }
        draw();
    });
    ['f-from', 'f-to'].forEach(function (id) {
        document.getElementById(id).addEventListener('change', function () {
            document.getElementById('f-period').value = 'custom'; draw();
        });
    });

    /* Sort bảng (2 cột số) */
    var sortState = null;
    function bindSort() {
        setupColumnSort({
            tableSel: '#tatbl', headRow: 2,
            cols: [{ key: 'debit' }, { key: 'credit' }],
            onChange: function (s) { sortState = s; draw(); },
        });
    }

    function buildRows() {
        var acc = val('f-account'), company = val('f-company');
        var bd = taBreakdown(acc, company, val('f-from'), val('f-to'));
        var kw = val('f-search').toLowerCase().trim();
        var rows = Object.keys(bd.map).map(function (c) {
            return { contra: c, name: ACC_NAMES[c] || '', debit: bd.map[c].debit, credit: bd.map[c].credit };
        }).filter(function (r) {
            return !kw || (r.contra + ' ' + r.name).toLowerCase().indexOf(kw) !== -1;
        });
        rows.sort(function (a, b) { return a.contra < b.contra ? -1 : 1; });
        if (sortState) {
            var k = sortState.key, asc = sortState.dir === 'asc' ? 1 : -1;
            rows.sort(function (a, b) { return (a[k] - b[k]) * asc || (a.contra < b.contra ? -1 : 1); });
        }
        return { acc: acc, company: company, rows: rows, totD: bd.totD, totC: bd.totC };
    }

    function draw() {
        document.getElementById('f-search-clear').style.display = val('f-search') ? 'inline-flex' : 'none';
        var d = buildRows();
        var acc = d.acc, natureDebit = isDebitNature(acc);
        var sdOpen = taOpeningBalance(acc, d.company, val('f-from'));
        var sdClose = taApplyBalance(acc, sdOpen, d.totD, d.totC);
        var scope = d.company ? (d.company + ' — ' + ORG[d.company].name) : 'Toàn tập đoàn (TPE, TPSG, TPHP)';

        document.getElementById('ta-title').textContent = 'Tài khoản: ' + acc + ' — ' + (ACC_NAMES[acc] || '');
        document.getElementById('ta-sub').textContent = scope + ' · Từ ngày ' + fmtDate(val('f-from')) + ' đến ngày ' + fmtDate(val('f-to'));

        /* ----- Bảng tổng hợp chữ T (đúng mẫu Excel) ----- */
        var tbody = document.querySelector('#tatbl tbody');
        var tfoot = document.querySelector('#tatbl tfoot');
        if (!d.rows.length) {
            tbody.innerHTML = '<tr><td colspan="4"><div class="empty-state"><div class="es-icon"><i class="ri-inbox-2-line"></i></div>Tài khoản không có phát sinh trong kỳ (hoặc không khớp tìm kiếm).</div></td></tr>';
        } else {
            tbody.innerHTML = d.rows.map(function (r) {
                return '<tr><td class="text-center"><b>' + r.contra + '</b></td><td>' + (r.name || '') + '</td>' +
                    '<td class="text-right num">' + (r.debit ? fmtMoney(r.debit) : '') + '</td>' +
                    '<td class="text-right num">' + (r.credit ? fmtMoney(r.credit) : '') + '</td></tr>';
            }).join('');
        }
        document.getElementById('ta-open').innerHTML = 'Số dư ' + (natureDebit ? 'nợ' : 'có') + ' đầu kỳ: <b>' + fmtMoney(sdOpen) + '</b>';
        tfoot.innerHTML =
            '<tr class="row-total"><td colspan="2">Tổng phát sinh nợ</td>' +
            '<td class="text-right num">' + fmtMoney(d.totD) + '</td><td></td></tr>' +
            '<tr class="row-total"><td colspan="2">Tổng phát sinh có</td>' +
            '<td></td><td class="text-right num">' + fmtMoney(d.totC) + '</td></tr>' +
            '<tr class="row-group"><td colspan="2">Số dư ' + (natureDebit ? 'nợ' : 'có') + ' cuối kỳ</td>' +
            '<td class="text-right num">' + (natureDebit ? fmtMoney(sdClose) : '') + '</td><td class="text-right num">' + (!natureDebit ? fmtMoney(sdClose) : '') + '</td></tr>';
        applyStickyTotals('#tatbl');
    }

    /* Sự kiện lọc */
    document.getElementById('f-account').addEventListener('change', draw);
    document.getElementById('f-company').addEventListener('change', draw);
    setupFilterHide({ storageKey: 'demo-filter-taccount-hidden', btnId: 'f-hide', bodyId: 'filter-body' });
    document.getElementById('f-search').addEventListener('keydown', function (e) { if (e.key === 'Enter') draw(); });
    document.getElementById('f-search').addEventListener('input', function () {
        document.getElementById('f-search-clear').style.display = this.value ? 'inline-flex' : 'none';
    });
    document.getElementById('f-search-clear').addEventListener('click', function () { document.getElementById('f-search').value = ''; draw(); });
    document.getElementById('f-go').addEventListener('click', draw);
    document.getElementById('f-clear').addEventListener('click', function () {
        document.getElementById('f-search').value = '';
        document.getElementById('f-company').value = '';
        document.getElementById('f-period').value = 'y';
        document.getElementById('f-from').value = PERIODS.y[0];
        document.getElementById('f-to').value = PERIODS.y[1];
        sortState = null; draw();
    });
    document.getElementById('btn-excel').addEventListener('click', function () {
        toast('Demo: file Excel sẽ được tải xuống ở bản chính thức', 'info');
    });

    setupFilterSettings({
        storageKey: 'demo-filter-taccount', gearBtnId: 'ff-gear', defaultWrap: 'ff-default', advWrap: 'ff-adv',
        fields: [
            { id: 'f-account', label: 'Tài khoản', locked: true },
            { id: 'f-period', label: 'Kỳ báo cáo', locked: true },
            { id: 'f-from', label: 'Từ ngày', locked: true },
            { id: 'f-to', label: 'Đến ngày', locked: true },
            { id: 'f-company', label: 'Đơn vị' },
        ],
    });

    /* ----- In (mẫu Excel) ----- */
    function printSheetHTML() {
        var d = buildRows(), acc = d.acc, natureDebit = isDebitNature(acc);
        var sdOpen = taOpeningBalance(acc, d.company, val('f-from'));
        var sdClose = taApplyBalance(acc, sdOpen, d.totD, d.totC);
        var body = d.rows.map(function (r) {
            return '<tr><td class="pc">' + r.contra + '</td><td>' + (r.name || '') + '</td>' +
                '<td class="pr">' + (r.debit ? fmtMoney(r.debit) : '') + '</td>' +
                '<td class="pr">' + (r.credit ? fmtMoney(r.credit) : '') + '</td></tr>';
        }).join('');
        return '<div class="print-sheet">' +
            '<table class="p-head"><tr>' +
            '<td style="width:60%"><b>Đơn vị:</b> ' + (d.company ? ORG[d.company].name : ORG['TPE'].name) + '<br><b>Địa chỉ:</b> ……………………………</td>' +
            '<td style="text-align:center"><i style="font-size:10.5px">Mẫu sổ tổng hợp chữ T</i></td>' +
            '</tr></table>' +
            '<div class="p-title">SỔ TỔNG HỢP CHỮ T CỦA MỘT TÀI KHOẢN</div>' +
            '<div class="p-sub">Tài khoản: ' + acc + ' — ' + (ACC_NAMES[acc] || '') + '</div>' +
            '<div class="p-sub">Từ ngày ' + fmtDate(val('f-from')) + ' đến ngày ' + fmtDate(val('f-to')) + '</div>' +
            '<div class="p-unit">Đơn vị tính: VNĐ</div>' +
            '<div style="margin:6px 0;font-size:12px"><b>Số dư ' + (natureDebit ? 'nợ' : 'có') + ' đầu kỳ:</b> ' + fmtMoney(sdOpen) + '</div>' +
            '<table class="p-grid">' +
            '<thead><tr><th rowspan="2">Tk đối ứng</th><th rowspan="2" style="width:46%">Tên tài khoản</th><th colspan="2">Số phát sinh</th></tr>' +
            '<tr><th>Nợ</th><th>Có</th></tr></thead>' +
            '<tbody>' + body + '</tbody></table>' +
            '<table class="p-summary" style="width:auto;margin:8px 0;font-size:12px">' +
            '<tr><td style="text-align:left;padding:2px 24px 2px 0"><b>Tổng phát sinh nợ:</b></td><td class="pr"><b>' + fmtMoney(d.totD) + '</b></td></tr>' +
            '<tr><td style="text-align:left;padding:2px 24px 2px 0"><b>Tổng phát sinh có:</b></td><td class="pr"><b>' + fmtMoney(d.totC) + '</b></td></tr>' +
            '<tr><td style="text-align:left;padding:2px 24px 2px 0"><b>Số dư ' + (natureDebit ? 'nợ' : 'có') + ' cuối kỳ:</b></td><td class="pr"><b>' + fmtMoney(sdClose) + '</b></td></tr>' +
            '</table>' +
            '<table class="p-sign" style="margin-top:24px"><tr>' +
            '<td style="width:60%"></td>' +
            '<td><i>Ngày ... tháng ... năm ...</i><br><b>NGƯỜI GHI SỔ</b><br><i>(Ký, họ tên)</i></td>' +
            '</tr></table>' +
            '</div>';
    }
    document.getElementById('btn-print').addEventListener('click', function () {
        document.getElementById('print-preview').innerHTML = printSheetHTML();
        openModal('print-modal');
    });
    document.getElementById('btn-do-print').addEventListener('click', function () {
        document.getElementById('print-area').innerHTML = printSheetHTML();
        window.print();
    });

    bindSort();
    draw();
}

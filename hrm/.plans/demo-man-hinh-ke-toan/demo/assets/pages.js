/* ============================================================
   Demo Kế toán HRM — render 3 loại màn (danh sách / form / chi tiết)
   Markup bám V2 components của hrm-client:
   - V2BaseFilterPanel  → section.tp-card (icon chip, quick search, advanced filters)
   - V2BaseDataTable    → section.tp-card (header + actions, table.data-table, row-actions)
   - V2BaseButton       → .v2-btn .v2-btn--sm .v2-btn--primary/secondary/tertiary (+ icon prefix)
   - V2BaseIconButton   → .v2-icon-btn (table actions: Xem → Sửa → Xoá)
   kind = 'borrow' (đi vay) | 'lend' (cho vay)
   ============================================================ */

function T(kind) {
    if (kind === 'borrow') {
        return {
            kind: 'borrow', menuKey: 'borrow',
            title: 'Khế ước đi vay', subInfo: 'Khai báo khế ước vay để tính lãi vay đến hạn, theo dõi lịch thanh toán nợ gốc và lãi vay',
            partnerLabel: 'Đối tượng cho vay', pay: 'trả', Pay: 'Trả',
            listPage: 'di-vay-danh-sach.html', formPage: 'di-vay-form.html', detailPage: 'di-vay-chi-tiet.html',
            debtAccounts: ACCOUNTS_DEBT.borrow, interestAccounts: ACCOUNTS_INTEREST.borrow,
            payMethods: ['Chuyển khoản', 'Tiền mặt', 'Tiền gửi'],
            scheduleTitle: 'Lịch trả nợ gốc và lãi vay',
        };
    }
    return {
        kind: 'lend', menuKey: 'lend',
        title: 'Khế ước cho vay', subInfo: 'Khai báo khế ước cho vay để tính lãi phải thu, theo dõi lịch thu hồi nợ gốc và lãi',
        partnerLabel: 'Đối tượng vay', pay: 'thu', Pay: 'Thu',
        listPage: 'cho-vay-danh-sach.html', formPage: 'cho-vay-form.html', detailPage: 'cho-vay-chi-tiet.html',
        debtAccounts: ACCOUNTS_DEBT.lend, interestAccounts: ACCOUNTS_INTEREST.lend,
        payMethods: ['Nộp vào tài khoản', 'Tiền mặt', 'Trừ lương'],
        scheduleTitle: 'Lịch thu nợ gốc và lãi',
    };
}

/* ---------- helper: nút V2 ---------- */
function v2btn(variant, icon, label, attrs) {
    return '<button type="button" class="v2-btn v2-btn--sm v2-btn--' + variant + '" ' + (attrs || '') + '>' +
        (icon ? '<i class="' + icon + '"></i>' : '') + label + '</button>';
}

/* ============================================================
   1. MÀN DANH SÁCH
   ============================================================ */
function renderListPage(kind) {
    var t = T(kind);
    var rows = getAllRecords(kind);
    var deleted = {}; // id đã xóa trong phiên xem trang
    var collapsed = true;

    renderShell(t.menuKey,
        /* ----- FILTER PANEL (V2BaseFilterPanel) ----- */
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="filter-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-filter-3-line"></i></div>' +
        '      <p class="tp-section-title">Bộ lọc danh sách ' + t.title.toLowerCase() + '</p>' +
        '    </div>' +
        '    <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-toggle">' +
        '      <i class="ri-equalizer-line"></i> Tìm kiếm nâng cao</button>' +
        '  </div>' +
        '  <div class="quick-search">' +
        '    <i class="ri-search-line"></i>' +
        '    <input class="form-control form-control-sm" id="f-search" placeholder="Tìm theo Số khế ước, ' + t.partnerLabel + '">' +
        '    <button type="button" class="btn-clear-quick-search" id="f-search-clear"><i class="ri-close-line"></i></button>' +
        '  </div>' +
        '  <div class="advanced-filters collapsed" id="adv-filters">' +
        '    <div class="form-row filter-grid">' +
        '      <div class="col-md-3"><label class="tp-label">Trạng thái</label>' +
        '        <select class="form-control form-control-sm" id="f-status"><option value="">— Tất cả —</option>' +
                    Object.keys(STATUSES).map(function (k) { return '<option value="' + k + '">' + STATUSES[k].label + '</option>'; }).join('') +
        '        </select></div>' +
        '      <div class="col-md-3"><label class="tp-label">Ngày giải ngân từ</label>' +
        '        <input type="date" class="form-control form-control-sm" id="f-from"></div>' +
        '      <div class="col-md-3"><label class="tp-label">Ngày giải ngân đến</label>' +
        '        <input type="date" class="form-control form-control-sm" id="f-to"></div>' +
        '    </div>' +
        '  </div>' +
        '  <div class="mt-1">' +
        '    <button type="button" class="v2-btn v2-btn--primary btn-compact mr-2" id="f-go"><i class="ri-search-line"></i> Tìm kiếm</button>' +
        '    <button type="button" class="v2-btn v2-btn--tertiary btn-compact" id="f-clear"><i class="ri-refresh-line"></i> Nhập lại</button>' +
        '  </div>' +
        '</section>' +

        /* ----- DATA TABLE (V2BaseDataTable) ----- */
        '<section class="tp-card p-3">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-file-list-3-line"></i></div>' +
        '      <h5>Danh sách ' + t.title.toLowerCase() + '</h5>' +
        '    </div>' +
        '    <div class="table-actions">' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-create"><i class="ri-add-line"></i> Tạo mới</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-excel"><i class="ri-file-excel-2-line"></i> Xuất Excel</button>' +
        '    </div>' +
        '  </div>' +
        '  <div class="table-wrapper scrollbar-thin"><table class="data-table" id="tbl">' +
        '    <thead><tr>' +
        '      <th class="text-center" style="width:44px">STT</th>' +
        '      <th>Số khế ước</th><th>' + t.partnerLabel + '</th><th>Ngày giải ngân</th><th>Thời hạn</th>' +
        '      <th class="text-right">Giá trị khoản vay</th><th class="text-right">Nợ gốc đã ' + t.pay + '</th>' +
        '      <th class="text-right">Dư nợ hiện tại</th><th class="text-right">LS hiện tại</th>' +
        '      <th>Ngày ' + t.pay + ' gốc tiếp theo</th><th>Ngày ' + t.pay + ' lãi tiếp theo</th>' +
        '      <th>Trạng thái</th><th class="text-center" style="width:110px">Thao tác</th>' +
        '    </tr></thead>' +
        '    <tbody></tbody>' +
        '    <tfoot></tfoot>' +
        '  </table></div>' +
        '  <div class="tp-small-text mt-2" id="tbl-count"></div>' +
        '</section>' +
        confirmModalHTML());

    /* toggle tìm kiếm nâng cao */
    document.getElementById('f-toggle').addEventListener('click', function () {
        collapsed = !collapsed;
        document.getElementById('adv-filters').classList.toggle('collapsed', collapsed);
        this.innerHTML = collapsed ? '<i class="ri-equalizer-line"></i> Tìm kiếm nâng cao'
                                   : '<i class="ri-arrow-up-s-line"></i> Ẩn tìm kiếm nâng cao';
    });

    function applyFilter() {
        var kw = document.getElementById('f-search').value.toLowerCase().trim();
        var st = document.getElementById('f-status').value;
        var from = document.getElementById('f-from').value;
        var to = document.getElementById('f-to').value;
        return rows.filter(function (r) {
            if (deleted[r.id]) return false;
            if (kw && (r.code + ' ' + r.partner).toLowerCase().indexOf(kw) === -1) return false;
            if (st !== '' && String(r.status) !== st) return false;
            if (from && r.disburseDate < from) return false;
            if (to && r.disburseDate > to) return false;
            return true;
        });
    }

    function draw() {
        var list = applyFilter();
        var tbody = document.querySelector('#tbl tbody');
        var tfoot = document.querySelector('#tbl tfoot');
        document.getElementById('f-search-clear').style.display = document.getElementById('f-search').value ? 'inline-flex' : 'none';
        if (!list.length) {
            tbody.innerHTML = '<tr><td colspan="13"><div class="empty-state"><div class="es-icon"><i class="ri-inbox-2-line"></i></div>Không có dữ liệu phù hợp bộ lọc.</div></td></tr>';
            tfoot.innerHTML = '';
            document.getElementById('tbl-count').textContent = '';
            return;
        }
        var totalAmount = 0, totalBalance = 0;
        tbody.innerHTML = list.map(function (r, idx) {
            var s = computeStats(r);
            totalAmount += r.amount; totalBalance += s.balance;
            return '<tr class="clickable' + (r.isNew ? ' row-new' : '') + '" data-id="' + r.id + '">' +
                '<td class="text-center">' + (idx + 1) + '</td>' +
                '<td><span class="cell-title">' + r.code + '</span>' + (r.isNew ? '<span class="tp-badge">Mới</span>' : '') + '</td>' +
                '<td>' + r.partner + '</td>' +
                '<td class="num">' + fmtDate(r.disburseDate) + '</td>' +
                '<td class="num">' + r.termMonths + ' tháng</td>' +
                '<td class="text-right num">' + fmtMoney(r.amount) + '</td>' +
                '<td class="text-right num">' + fmtMoney(s.paidPrincipal) + '</td>' +
                '<td class="text-right num"><b>' + fmtMoney(s.balance) + '</b></td>' +
                '<td class="text-right num">' + r.rate.toFixed(1).replace('.', ',') + '%</td>' +
                '<td class="num">' + (s.nextPrincipalDate ? fmtDate(s.nextPrincipalDate) : '<span class="text-muted">—</span>') + '</td>' +
                '<td class="num">' + (s.nextInterestDate ? fmtDate(s.nextInterestDate) : '<span class="text-muted">—</span>') + '</td>' +
                '<td>' + statusBadge(r.status) + '</td>' +
                '<td class="text-center"><span class="row-actions">' +
                '  <button type="button" class="v2-icon-btn v2-icon-btn--sm" data-act="view" data-id="' + r.id + '" title="Xem chi tiết"><i class="ri-eye-line"></i></button>' +
                '  <button type="button" class="v2-icon-btn v2-icon-btn--sm" data-act="edit" data-id="' + r.id + '" title="Chỉnh sửa"><i class="ri-edit-line"></i></button>' +
                '  <button type="button" class="v2-icon-btn v2-icon-btn--sm v2-icon-btn--danger" data-act="del" data-id="' + r.id + '" title="Xoá"><i class="ri-delete-bin-line"></i></button>' +
                '</span></td></tr>';
        }).join('');
        tfoot.innerHTML = '<tr><td colspan="5">Tổng cộng</td>' +
            '<td class="text-right num">' + fmtMoney(totalAmount) + '</td><td></td>' +
            '<td class="text-right num">' + fmtMoney(totalBalance) + '</td><td colspan="5"></td></tr>';
        document.getElementById('tbl-count').textContent = 'Tổng ' + list.length + ' khế ước';

        tbody.querySelectorAll('tr.clickable').forEach(function (tr) {
            tr.addEventListener('click', function (e) {
                if (e.target.closest('.v2-icon-btn')) return;
                location.href = t.detailPage + '?id=' + tr.dataset.id;
            });
        });
        tbody.querySelectorAll('.v2-icon-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var id = btn.dataset.id, act = btn.dataset.act;
                if (act === 'view') location.href = t.detailPage + '?id=' + id;
                else if (act === 'edit') location.href = t.formPage + '?id=' + id;
                else if (act === 'del') askDelete(id);
            });
        });
    }

    function askDelete(id) {
        var rec = rows.filter(function (r) { return r.id === id; })[0];
        document.getElementById('cf-text').innerHTML = 'Bạn có chắc muốn xoá khế ước <b>' + rec.code + '</b>?<br><span class="tp-small-text">(Demo: chỉ ẩn khỏi danh sách trong phiên này)</span>';
        openModal('confirm-modal');
        document.getElementById('cf-ok').onclick = function () {
            deleted[id] = true;
            if (rec.isNew) {
                var arr = loadSessionRecords(kind).filter(function (r) { return r.id !== id; });
                sessionStorage.setItem('demo-ku-' + kind, JSON.stringify(arr));
            }
            closeModal('confirm-modal');
            toast('Đã xoá khế ước ' + rec.code, 'warning');
            draw();
        };
    }

    /* Filter auto-search (list-page skill): select/date đổi → lọc ngay; keyword cần Enter/nút Tìm kiếm */
    ['f-status', 'f-from', 'f-to'].forEach(function (id) {
        document.getElementById(id).addEventListener('change', draw);
    });
    document.getElementById('f-search').addEventListener('keydown', function (e) { if (e.key === 'Enter') draw(); });
    document.getElementById('f-search').addEventListener('input', function () {
        document.getElementById('f-search-clear').style.display = this.value ? 'inline-flex' : 'none';
    });
    document.getElementById('f-search-clear').addEventListener('click', function () {
        document.getElementById('f-search').value = ''; draw();
    });
    document.getElementById('f-go').addEventListener('click', draw);
    document.getElementById('f-clear').addEventListener('click', function () {
        ['f-search', 'f-status', 'f-from', 'f-to'].forEach(function (id) { document.getElementById(id).value = ''; });
        draw();
    });
    document.getElementById('btn-create').addEventListener('click', function () { location.href = t.formPage; });
    document.getElementById('btn-excel').addEventListener('click', function () {
        toast('Demo: file Excel sẽ được tải xuống ở bản chính thức', 'info');
    });
    draw();
}

function confirmModalHTML() {
    return '<div class="modal-backdrop-demo" id="confirm-modal"><div class="modal-dialog" style="max-width:420px">' +
        '<div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-error-warning-line"></i></span>Xác nhận</h5>' +
        '<button type="button" class="close" onclick="closeModal(\'confirm-modal\')">×</button></div>' +
        '<div class="modal-body" id="cf-text" style="font-size:13px;color:#374151"></div>' +
        '<div class="modal-footer">' +
        '<button type="button" class="v2-btn v2-btn--sm v2-btn--primary v2-btn--primary-danger" id="cf-ok"><i class="ri-delete-bin-line"></i> Xoá</button>' +
        '<button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'confirm-modal\')"><i class="ri-close-line"></i> Đóng</button>' +
        '</div></div></div>';
}

/* ============================================================
   2. MÀN FORM KHAI BÁO
   ============================================================ */
function renderFormPage(kind) {
    var t = T(kind);
    var editing = qs('id') ? findRecord(kind, qs('id')) : null;
    var rateRows = editing ? JSON.parse(JSON.stringify(editing.rates)) : [{ rate: '', overdueRate: '', from: '', note: '' }];

    function opt(list, selected) {
        return list.map(function (v) { return '<option' + (v === selected ? ' selected' : '') + '>' + v + '</option>'; }).join('');
    }
    function periodOpts(selected, keys) {
        // Trả gốc: đủ 4 kỳ; Trả lãi: MISA chỉ có Hàng tháng / Hàng quý / Cuối kỳ
        return (keys || Object.keys(PAY_PERIODS)).map(function (k) {
            return '<option value="' + k + '"' + (k === selected ? ' selected' : '') + '>' + PAY_PERIODS[k] + '</option>';
        }).join('');
    }
    function group(label, required, inner, err, col) {
        return '<div class="' + (col || 'col-md-3') + '"><label class="tp-label">' + label +
            (required ? ' <span class="field-required">*</span>' : '') + '</label>' + inner +
            (err ? '<div class="invalid-feedback">' + err + '</div>' : '') + '</div>';
    }

    var e = editing || {};
    renderShell(t.menuKey,
        '<form id="ku-form" novalidate>' +
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="' + (editing ? 'ri-edit-line' : 'ri-file-add-line') + '"></i></div>' +
        '      <div><h5>' + (editing ? 'Sửa khế ước ' + e.code : 'Khai báo ' + t.title.toLowerCase()) + '</h5>' +
        '      <p class="tp-section-subtitle">' + t.subInfo + '</p></div>' +
        '    </div>' +
        '    <div class="table-actions">' +
        '      <a class="v2-btn v2-btn--sm v2-btn--light" href="' + t.listPage + '"><i class="ri-arrow-left-line"></i> Quay lại danh sách</a>' +
        '    </div>' +
        '  </div>' +

        /* ----- Header form ----- */
        '<div class="form-row" style="margin-top:6px">' +
        group('Số khế ước', true, '<input class="form-control form-control-sm" id="fd-code" data-required value="' + (e.code || nextCode(kind)) + '">', 'Vui lòng nhập số khế ước') +
        group(t.partnerLabel, true, '<select class="form-control form-control-sm" id="fd-partner" data-required><option value="">— Chọn đối tượng —</option>' + opt(PARTNERS, e.partner) + '</select>', 'Vui lòng chọn đối tượng', 'col-md-4') +
        group('Hợp đồng tín dụng', false, '<select class="form-control form-control-sm" id="fd-contract">' + opt(CREDIT_CONTRACTS, e.creditContract) + '</select>') +
        '</div>' +
        '<div class="form-row">' +
        group('TK hạch toán nợ gốc', true, '<select class="form-control form-control-sm" id="fd-debt-acc">' + opt(t.debtAccounts, e.debtAccount) + '</select>') +
        group('TK hạch toán lãi vay', true, '<select class="form-control form-control-sm" id="fd-int-acc">' + opt(t.interestAccounts, e.interestAccount) + '</select>') +
        group('Mục đích vay', false, '<input class="form-control form-control-sm" id="fd-purpose" placeholder="VD: Bổ sung vốn lưu động..." value="' + (e.purpose || '') + '">', '', 'col-md-6') +
        '</div>' +

        /* ----- Tabs ----- */
        '<div class="tabs-wrap mt-2">' +
        '<ul class="nav-tabs">' +
        '  <li><button type="button" class="nav-link active" data-tab="tab-gn"><i class="ri-money-dollar-circle-line"></i>Thông tin giải ngân</button></li>' +
        '  <li><button type="button" class="nav-link" data-tab="tab-ls"><i class="ri-percent-line"></i>Lãi suất</button></li>' +
        '  <li><button type="button" class="nav-link" data-tab="tab-tn"><i class="ri-calendar-schedule-line"></i>Hình thức ' + t.pay + ' nợ</button></li>' +
        '  <li><button type="button" class="nav-link" data-tab="tab-dk"><i class="ri-attachment-2"></i>Đính kèm</button></li>' +
        '</ul>' +

        /* Tab 1: giải ngân */
        '<div class="tab-pane active" id="tab-gn"><div class="form-row">' +
        group('Loại tiền', true, '<select class="form-control form-control-sm" id="fd-currency"><option>VND</option><option>USD</option><option>EUR</option></select>') +
        group('Giá trị khoản vay', true, '<input class="form-control form-control-sm text-right" id="fd-amount" data-required data-positive value="' + (e.amount ? fmtMoney(e.amount) : '') + '" placeholder="0">', 'Giá trị khoản vay phải lớn hơn 0') +
        group('Thời hạn vay', true,
            '<div class="input-group"><input type="number" min="1" class="form-control form-control-sm text-right" id="fd-term" data-required data-positive value="' + (e.termMonths || '') + '">' +
            '<select class="form-control form-control-sm" id="fd-term-unit" style="max-width:100px"><option value="thang">Tháng</option><option value="nam">Năm</option></select></div>', 'Vui lòng nhập thời hạn vay') +
        '</div><div class="form-row">' +
        group('Ngày giải ngân', true, '<input type="date" class="form-control form-control-sm" id="fd-disburse" data-required value="' + (e.disburseDate || '') + '">', 'Vui lòng chọn ngày giải ngân') +
        group('Ngày đáo hạn <span class="tp-small-text">(tự tính)</span>', true, '<input type="date" class="form-control form-control-sm" id="fd-maturity" data-required value="' + (e.maturityDate || '') + '">', 'Vui lòng chọn ngày đáo hạn') +
        group('Phương thức giải ngân', true, '<select class="form-control form-control-sm" id="fd-disburse-method"><option>Chuyển khoản vào tài khoản DN</option><option>Chuyển khoản</option><option>Tiền mặt</option><option>Giải ngân từng lần theo HĐTD</option></select>') +
        '</div><div class="form-row">' +
        group('TK thụ hưởng', false, '<input class="form-control form-control-sm" id="fd-benef" value="' + (e.beneficiaryAccount || '') + '">') +
        group('Tên ngân hàng', false, '<input class="form-control form-control-sm" id="fd-bank" value="' + (e.bankName || '') + '">', '', 'col-md-4') +
        '</div></div>' +

        /* Tab 2: lãi suất */
        '<div class="tab-pane" id="tab-ls">' +
        '  <label class="tp-label">Loại lãi suất</label><div class="radio-row">' +
        '    <label><input type="radio" name="r-type" value="reducing"' + (e.interestType !== 'flat' ? ' checked' : '') + '> Lãi suất trên dư nợ giảm dần</label>' +
        '    <label><input type="radio" name="r-type" value="flat"' + (e.interestType === 'flat' ? ' checked' : '') + '> Lãi suất trên dư nợ gốc</label></div>' +
        '  <label class="tp-label">Cơ sở tính lãi ngày</label><div class="radio-row">' +
        '    <label><input type="radio" name="r-basis" value="365"' + (e.dayBasis !== 360 ? ' checked' : '') + '> Lãi năm/365</label>' +
        '    <label><input type="radio" name="r-basis" value="360"' + (e.dayBasis === 360 ? ' checked' : '') + '> Lãi năm/360</label></div>' +
        '  <label class="tp-label">Phương thức điều chỉnh</label><div class="radio-row">' +
        '    <label><input type="radio" name="r-adjust" value="adjustable"' + (e.rateAdjust !== 'fixed' ? ' checked' : '') + '> Có điều chỉnh</label>' +
        '    <label><input type="radio" name="r-adjust" value="fixed"' + (e.rateAdjust === 'fixed' ? ' checked' : '') + '> Cố định</label></div>' +
        '  <div class="table-wrapper"><table class="data-table table-input" id="rate-grid"><thead><tr>' +
        '    <th class="text-center" style="width:36px">#</th><th style="width:130px">Lãi suất (%) <span class="field-required">*</span></th><th style="width:150px">Lãi suất quá hạn (%)</th>' +
        '    <th style="width:150px">Hiệu lực từ <span class="field-required">*</span></th><th>Ghi chú</th><th style="width:40px"></th>' +
        '  </tr></thead><tbody></tbody></table></div>' +
        '  <div class="invalid-feedback" id="rate-error">Cần ít nhất 1 dòng lãi suất với Lãi suất (%) và Hiệu lực từ</div>' +
        '  <div class="d-flex gap-2 mt-2">' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="rate-add"><i class="ri-add-line"></i> Thêm dòng</button>' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" id="rate-clear"><i class="ri-eraser-line"></i> Xoá hết dòng</button>' +
        '  </div>' +
        '</div>' +

        /* Tab 3: hình thức trả/thu nợ — theo MISA: chọn "Cuối kỳ" thì ẩn "Ngày ... đầu tiên" */
        '<div class="tab-pane" id="tab-tn"><div class="form-row">' +
        group(t.Pay + ' gốc', true, '<select class="form-control form-control-sm" id="fd-p-period">' + periodOpts(e.principalPeriod || 'monthly') + '</select>') +
        '<div class="col-md-3" id="wrap-p-first"><label class="tp-label">Ngày ' + t.pay + ' gốc đầu tiên <span class="field-required">*</span></label>' +
        '<input type="date" class="form-control form-control-sm" id="fd-p-first" data-required value="' + (e.firstPrincipalDate || '') + '">' +
        '<div class="invalid-feedback">Vui lòng chọn ngày</div></div>' +
        '</div><div class="form-row">' +
        group(t.Pay + ' lãi', true, '<select class="form-control form-control-sm" id="fd-i-period">' + periodOpts(e.interestPeriod || 'monthly', ['monthly', 'quarterly', 'maturity']) + '</select>') +
        '<div class="col-md-3" id="wrap-i-first"><label class="tp-label">Ngày ' + t.pay + ' lãi đầu tiên <span class="field-required">*</span></label>' +
        '<input type="date" class="form-control form-control-sm" id="fd-i-first" data-required value="' + (e.firstInterestDate || '') + '">' +
        '<div class="invalid-feedback">Vui lòng chọn ngày</div></div>' +
        '</div><div class="form-row">' +
        group('Phương thức ' + t.pay + ' nợ', true, '<select class="form-control form-control-sm" id="fd-pay-method">' + opt(t.payMethods, e.payMethod) + '</select>') +
        group('Chuyển vào tài khoản', false, '<input class="form-control form-control-sm" id="fd-pay-acc" value="' + (e.payAccount || '') + '">') +
        group('Tên ngân hàng', false, '<input class="form-control form-control-sm" id="fd-pay-bank" value="' + (e.payBank || '') + '">', '', 'col-md-4') +
        '</div></div>' +

        /* Tab 4: đính kèm */
        '<div class="tab-pane" id="tab-dk">' +
        '  <div class="attach-zone" id="attach-zone"><i class="ri-attachment-2"></i> Bấm để chọn file đính kèm (hợp đồng, khế ước scan...)<br><span style="font-size:11px">Demo: file chỉ hiển thị tên, không upload</span></div>' +
        '  <input type="file" id="attach-input" multiple style="display:none">' +
        '  <ul class="attach-list" id="attach-list"></ul>' +
        '</div>' +
        '</div>' + // tabs-wrap

        /* Footer — thứ tự button-convention form page: chính → phụ → quay lại cuối */
        '<div class="d-flex justify-end gap-2 mt-3" style="border-top:1px solid #e5e7eb;padding-top:12px">' +
        '  <button type="submit" class="v2-btn v2-btn--sm v2-btn--primary"><i class="ri-save-3-line"></i> Lưu</button>' +
        '  <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-preview"><i class="ri-calendar-check-line"></i> Xem trước lịch ' + t.pay + ' nợ</button>' +
        '  <a class="v2-btn v2-btn--sm v2-btn--tertiary" href="' + t.listPage + '"><i class="ri-arrow-left-line"></i> Huỷ</a>' +
        '</div>' +
        '</section></form>' +

        /* Modal xem trước lịch */
        '<div class="modal-backdrop-demo" id="preview-modal"><div class="modal-dialog">' +
        '  <div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-calendar-check-line"></i></span>Xem trước ' + t.scheduleTitle.toLowerCase() + '</h5>' +
        '  <button type="button" class="close" onclick="closeModal(\'preview-modal\')">×</button></div>' +
        '  <div class="modal-body" id="preview-body"></div>' +
        '  <div class="modal-footer"><button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'preview-modal\')"><i class="ri-close-line"></i> Đóng</button></div>' +
        '</div></div>');

    initTabs();

    /* ----- Grid lãi suất ----- */
    function drawRates() {
        var tbody = document.querySelector('#rate-grid tbody');
        tbody.innerHTML = rateRows.map(function (r, i) {
            return '<tr>' +
                '<td class="text-center">' + (i + 1) + '</td>' +
                '<td><input class="form-control form-control-sm text-right rate-cell" data-i="' + i + '" data-f="rate" value="' + (r.rate !== '' ? String(r.rate).replace('.', ',') : '') + '"></td>' +
                '<td><input class="form-control form-control-sm text-right rate-cell" data-i="' + i + '" data-f="overdueRate" value="' + (r.overdueRate !== '' ? String(r.overdueRate).replace('.', ',') : '') + '"></td>' +
                '<td><input type="date" class="form-control form-control-sm rate-cell" data-i="' + i + '" data-f="from" value="' + (r.from || '') + '"></td>' +
                '<td><input class="form-control form-control-sm rate-cell" data-i="' + i + '" data-f="note" value="' + (r.note || '') + '"></td>' +
                '<td class="text-center"><button type="button" class="v2-icon-btn v2-icon-btn--sm v2-icon-btn--danger rate-del" data-i="' + i + '" title="Xoá dòng"><i class="ri-delete-bin-line"></i></button></td>' +
                '</tr>';
        }).join('');
        tbody.querySelectorAll('.rate-cell').forEach(function (inp) {
            inp.addEventListener('input', function () {
                rateRows[+inp.dataset.i][inp.dataset.f] = inp.value;
            });
        });
        tbody.querySelectorAll('.rate-del').forEach(function (btn) {
            btn.addEventListener('click', function () { rateRows.splice(+btn.dataset.i, 1); drawRates(); });
        });
    }
    drawRates();
    document.getElementById('rate-add').addEventListener('click', function () {
        rateRows.push({ rate: '', overdueRate: '', from: document.getElementById('fd-disburse').value || '', note: '' });
        drawRates();
    });
    document.getElementById('rate-clear').addEventListener('click', function () { rateRows = []; drawRates(); });

    /* ----- Auto tính ngày đáo hạn ----- */
    function autoMaturity() {
        var d = document.getElementById('fd-disburse').value;
        var term = parseInt(document.getElementById('fd-term').value, 10);
        var unit = document.getElementById('fd-term-unit').value;
        if (d && term > 0) document.getElementById('fd-maturity').value = addMonths(d, unit === 'nam' ? term * 12 : term);
    }
    ['fd-disburse', 'fd-term', 'fd-term-unit'].forEach(function (id) {
        document.getElementById(id).addEventListener('change', autoMaturity);
    });

    /* ----- Hình thức trả/thu nợ: chọn "Cuối kỳ" → ẩn "Ngày ... đầu tiên" (theo MISA);
       đổi kỳ / ngày giải ngân → gợi ý ngày kỳ đầu = giải ngân + 1 kỳ ----- */
    function syncPayPeriod(selId, wrapId, inpId) {
        var period = document.getElementById(selId).value;
        var wrap = document.getElementById(wrapId);
        var inp = document.getElementById(inpId);
        var isMaturity = period === 'maturity';
        wrap.style.display = isMaturity ? 'none' : '';
        if (isMaturity) { setInvalid(inp, false); return; }
        var dis = document.getElementById('fd-disburse').value;
        if (dis && (!inp.value || inp.dataset.auto === '1')) {
            inp.value = addMonths(dis, periodMonths(period));
            inp.dataset.auto = '1';
        }
    }
    function syncBothPeriods() {
        syncPayPeriod('fd-p-period', 'wrap-p-first', 'fd-p-first');
        syncPayPeriod('fd-i-period', 'wrap-i-first', 'fd-i-first');
    }
    document.getElementById('fd-p-period').addEventListener('change', syncBothPeriods);
    document.getElementById('fd-i-period').addEventListener('change', syncBothPeriods);
    document.getElementById('fd-disburse').addEventListener('change', syncBothPeriods);
    ['fd-p-first', 'fd-i-first'].forEach(function (id) {
        document.getElementById(id).addEventListener('input', function () { this.dataset.auto = '0'; }); // user sửa tay → thôi auto
    });
    syncBothPeriods(); // init (kể cả khi sửa KƯ có sẵn "Cuối kỳ")

    bindMoneyInput(document.getElementById('fd-amount'));

    /* ----- Đính kèm giả lập ----- */
    var attachZone = document.getElementById('attach-zone');
    var attachInput = document.getElementById('attach-input');
    attachZone.addEventListener('click', function () { attachInput.click(); });
    attachInput.addEventListener('change', function () {
        var list = document.getElementById('attach-list');
        Array.prototype.forEach.call(attachInput.files, function (f) {
            var li = document.createElement('li');
            li.innerHTML = '<span><i class="ri-file-3-line"></i> ' + f.name + '</span><button type="button" class="rm"><i class="ri-close-line"></i></button>';
            li.querySelector('.rm').addEventListener('click', function () { li.remove(); });
            list.appendChild(li);
        });
        attachInput.value = '';
    });

    /* ----- Thu thập dữ liệu form thành object khế ước ----- */
    function collect() {
        var term = parseInt(document.getElementById('fd-term').value, 10) || 0;
        if (document.getElementById('fd-term-unit').value === 'nam') term *= 12;
        var firstRate = rateRows.filter(function (r) { return parseFloat(String(r.rate).replace(',', '.')) > 0; })[0];
        return {
            id: editing ? editing.id : 'NEW-' + (loadSessionRecords(kind).length + 1) + '-' + kind,
            code: document.getElementById('fd-code').value.trim(),
            partner: document.getElementById('fd-partner').value,
            creditContract: document.getElementById('fd-contract').value,
            purpose: document.getElementById('fd-purpose').value.trim(),
            debtAccount: document.getElementById('fd-debt-acc').value,
            interestAccount: document.getElementById('fd-int-acc').value,
            currency: document.getElementById('fd-currency').value,
            amount: parseMoney(document.getElementById('fd-amount').value),
            termMonths: term,
            disburseDate: document.getElementById('fd-disburse').value,
            maturityDate: document.getElementById('fd-maturity').value,
            disburseMethod: document.getElementById('fd-disburse-method').value,
            beneficiaryAccount: document.getElementById('fd-benef').value.trim(),
            bankName: document.getElementById('fd-bank').value.trim(),
            interestType: document.querySelector('[name=r-type]:checked').value,
            dayBasis: +document.querySelector('[name=r-basis]:checked').value,
            rateAdjust: document.querySelector('[name=r-adjust]:checked').value,
            rates: rateRows.map(function (r) {
                return { rate: parseFloat(String(r.rate).replace(',', '.')) || 0, overdueRate: parseFloat(String(r.overdueRate).replace(',', '.')) || 0, from: r.from, note: r.note };
            }),
            rate: firstRate ? parseFloat(String(firstRate.rate).replace(',', '.')) : 0,
            principalPeriod: document.getElementById('fd-p-period').value,
            firstPrincipalDate: document.getElementById('fd-p-first').value,
            interestPeriod: document.getElementById('fd-i-period').value,
            firstInterestDate: document.getElementById('fd-i-first').value,
            payMethod: document.getElementById('fd-pay-method').value,
            payAccount: document.getElementById('fd-pay-acc').value.trim(),
            payBank: document.getElementById('fd-pay-bank').value.trim(),
            status: editing ? editing.status : 1,
            paidPeriods: editing ? editing.paidPeriods : 0,
        };
    }

    /* ----- Validate ----- */
    function validate(showTabWithError) {
        var form = document.getElementById('ku-form');
        var ok = validateRequired(form);

        // grid lãi suất ≥ 1 dòng hợp lệ
        var rateOk = rateRows.some(function (r) { return parseFloat(String(r.rate).replace(',', '.')) > 0 && r.from; });
        document.getElementById('rate-error').classList.toggle('d-block', !rateOk);
        if (!rateOk) ok = false;

        // ngày trả gốc/lãi đầu tiên >= ngày giải ngân
        var dis = document.getElementById('fd-disburse').value;
        ['fd-p-first', 'fd-i-first'].forEach(function (idInp) {
            var inp = document.getElementById(idInp);
            if (!inp.offsetParent) return; // đang ẩn (Cuối kỳ) → bỏ qua
            var err = inp.parentElement.querySelector('.invalid-feedback');
            if (inp.value && dis && inp.value < dis) {
                setInvalid(inp, true);
                err.textContent = 'Ngày ' + t.pay + ' đầu tiên không được trước ngày giải ngân (' + fmtDate(dis) + ')';
                ok = false;
            } else if (inp.value) {
                err.textContent = 'Vui lòng chọn ngày';
            }
        });

        if (!ok && showTabWithError) {
            var firstBad = form.querySelector('.is-invalid') || document.getElementById('rate-error');
            var pane = firstBad.closest('.tab-pane');
            if (pane) {
                var btn = document.querySelector('[data-tab="' + pane.id + '"]');
                if (btn && !btn.classList.contains('active')) btn.click();
            }
        }
        return ok;
    }

    /* ----- Xem trước lịch ----- */
    document.getElementById('btn-preview').addEventListener('click', function () {
        if (!validate(true)) { toast('Vui lòng nhập đủ thông tin trước khi xem lịch', 'warning'); return; }
        var ku = collect();
        document.getElementById('preview-body').innerHTML = scheduleTableHTML(ku, t, -1, false);
        openModal('preview-modal');
    });

    /* ----- Submit ----- */
    document.getElementById('ku-form').addEventListener('submit', function (ev) {
        ev.preventDefault();
        if (!validate(true)) { toast('Vui lòng kiểm tra lại các trường báo đỏ', 'warning'); return; }
        var ku = collect();
        if (editing) {
            if (editing.isNew) {
                var arr = loadSessionRecords(kind).map(function (r) { return r.id === editing.id ? ku : r; });
                sessionStorage.setItem('demo-ku-' + kind, JSON.stringify(arr));
            }
            toast('Đã cập nhật khế ước ' + ku.code + (editing.isNew ? '' : ' (demo — dữ liệu mẫu không thay đổi)'));
        } else {
            saveSessionRecord(kind, ku);
            toast('Đã lưu khế ước ' + ku.code);
        }
        setTimeout(function () { location.href = t.listPage; }, 900);
    });
}

/* ============================================================
   Bảng lịch trả/thu nợ (modal xem trước + màn chi tiết)
   paidCount: số dòng đầu đã trả (-1 = không hiển thị cột trạng thái)
   withAction: true → nút "Ghi nhận trả/thu" trên dòng chưa trả kế tiếp
   ============================================================ */
function scheduleTableHTML(ku, t, paidCount, withAction) {
    var sched = generateSchedule(ku);
    if (!sched.length) return '<div class="empty-state">Chưa đủ dữ liệu để sinh lịch</div>';
    var showStatus = paidCount >= 0;
    var balance = ku.amount;
    var tot = { p: 0, i: 0 };
    var today = todayISO();
    var rows = sched.map(function (r, idx) {
        balance -= r.principal;
        tot.p += r.principal; tot.i += r.interest;
        var typeLabel = r.principal > 0 && r.interest > 0 ? 'Gốc + Lãi' : r.principal > 0 ? 'Gốc' : 'Lãi';
        var stCell = '', actCell = '';
        if (showStatus) {
            if (idx < paidCount) stCell = '<span class="status-pill st-done"><i class="ri-checkbox-circle-line"></i>Đã ' + t.pay + '</span>';
            else if (r.date <= today) stCell = '<span class="status-pill st-paused"><i class="ri-alarm-warning-line"></i>Đến hạn</span>';
            else stCell = '<span class="status-pill st-none"><i class="ri-time-line"></i>Chưa đến hạn</span>';
        }
        if (withAction && idx === paidCount) {
            actCell = '<button type="button" class="v2-btn v2-btn--xs v2-btn--primary v2-btn--primary-success" data-pay-idx="' + idx + '"><i class="ri-check-line"></i> Ghi nhận ' + t.pay + '</button>';
        }
        return '<tr>' +
            '<td class="text-center">' + (idx + 1) + '</td>' +
            '<td class="num">' + fmtDate(r.date) + '</td>' +
            '<td>' + typeLabel + '</td>' +
            '<td class="text-right num">' + (r.principal ? fmtMoney(r.principal) : '<span class="text-muted">—</span>') + '</td>' +
            '<td class="text-right num">' + (r.interest ? fmtMoney(r.interest) : '<span class="text-muted">—</span>') + '</td>' +
            '<td class="text-right num"><b>' + fmtMoney(r.principal + r.interest) + '</b></td>' +
            '<td class="text-right num">' + fmtMoney(Math.max(balance, 0)) + '</td>' +
            (showStatus ? '<td>' + stCell + '</td>' : '') +
            (withAction ? '<td class="text-center">' + actCell + '</td>' : '') +
            '</tr>';
    }).join('');
    return '<div class="note-box"><i class="ri-information-line"></i> Lãi tính theo <b>' + (ku.interestType === 'flat' ? 'dư nợ gốc' : 'dư nợ giảm dần') + '</b>, lãi suất ' +
        String(ku.rate).replace('.', ',') + '%/năm (năm/' + ku.dayBasis + '), ' + t.pay + ' gốc <b>' + PAY_PERIODS[ku.principalPeriod] +
        '</b>, ' + t.pay + ' lãi <b>' + PAY_PERIODS[ku.interestPeriod] + '</b>. Số liệu demo làm tròn nghìn đồng.</div>' +
        '<div class="table-wrapper scrollbar-thin"><table class="data-table"><thead><tr>' +
        '<th class="text-center" style="width:44px">Kỳ</th><th>Ngày đến hạn</th><th>Loại</th><th class="text-right">Gốc phải ' + t.pay + '</th>' +
        '<th class="text-right">Lãi phải ' + t.pay + '</th><th class="text-right">Tổng</th><th class="text-right">Dư nợ sau kỳ</th>' +
        (showStatus ? '<th>Trạng thái</th>' : '') + (withAction ? '<th style="width:130px"></th>' : '') +
        '</tr></thead><tbody>' + rows + '</tbody>' +
        '<tfoot><tr><td colspan="3">Tổng cộng</td><td class="text-right num">' + fmtMoney(tot.p) + '</td>' +
        '<td class="text-right num">' + fmtMoney(tot.i) + '</td><td class="text-right num">' + fmtMoney(tot.p + tot.i) + '</td>' +
        '<td colspan="' + (1 + (showStatus ? 1 : 0) + (withAction ? 1 : 0)) + '"></td></tr></tfoot></table></div>';
}

/* ============================================================
   3. MÀN CHI TIẾT + LỊCH TRẢ/THU NỢ
   ============================================================ */
function renderDetailPage(kind) {
    var t = T(kind);
    var ku = findRecord(kind, qs('id'));

    if (!ku) {
        renderShell(t.menuKey,
            '<section class="tp-card p-3"><div class="empty-state">' +
            '<div class="es-icon"><i class="ri-search-eye-line"></i></div>' +
            '<h5 style="margin-bottom:6px;color:#0f172a">Không tìm thấy khế ước</h5>' +
            '<p class="tp-small-text">Khế ước không tồn tại hoặc đã bị xoá trong phiên demo.</p>' +
            '<a class="v2-btn v2-btn--sm v2-btn--primary mt-3" href="' + t.listPage + '" style="display:inline-flex;margin-top:12px"><i class="ri-arrow-left-line"></i> Về danh sách</a>' +
            '</div></section>');
        return;
    }

    var stats = computeStats(ku);
    var paidCount = stats.paidCount; // state trong phiên xem trang

    renderShell(t.menuKey,
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-file-text-line"></i></div>' +
        '      <div><h5>' + ku.code + ' — ' + t.title + ' &nbsp;' + statusBadge(ku.status) + '</h5>' +
        '      <p class="tp-section-subtitle">' + ku.partner + '</p></div>' +
        '    </div>' +
        '    <div class="table-actions">' +
        '      <a class="v2-btn v2-btn--sm v2-btn--secondary" href="' + t.formPage + '?id=' + ku.id + '"><i class="ri-edit-line"></i> Chỉnh sửa</a>' +
        '      <a class="v2-btn v2-btn--sm v2-btn--light" href="' + t.listPage + '"><i class="ri-arrow-left-line"></i> Quay lại danh sách</a>' +
        '    </div>' +
        '  </div>' +
        '</section>' +
        '<div class="stat-row" id="stat-row"></div>' +
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="filter-header-left mb-2">' +
        '    <div class="tp-icon-chip"><i class="ri-information-line"></i></div>' +
        '    <p class="tp-section-title">Thông tin khế ước</p>' +
        '  </div>' +
        '  <div class="info-grid">' + infoItems() + '</div>' +
        '</section>' +
        '<section class="tp-card p-3">' +
        '  <div class="filter-header-left mb-2">' +
        '    <div class="tp-icon-chip"><i class="ri-calendar-schedule-line"></i></div>' +
        '    <p class="tp-section-title">' + t.scheduleTitle + '</p>' +
        '  </div>' +
        '  <div id="schedule-wrap"></div>' +
        '</section>');

    function infoItems() {
        var items = [
            ['Số khế ước', ku.code],
            [t.partnerLabel, ku.partner],
            ['Hợp đồng tín dụng', ku.creditContract || '—'],
            ['Mục đích vay', ku.purpose || '—'],
            ['TK hạch toán nợ gốc', ku.debtAccount],
            ['TK hạch toán lãi vay', ku.interestAccount],
            ['Loại tiền', ku.currency],
            ['Thời hạn vay', ku.termMonths + ' tháng'],
            ['Ngày giải ngân', fmtDate(ku.disburseDate)],
            ['Ngày đáo hạn', fmtDate(ku.maturityDate)],
            ['Phương thức giải ngân', ku.disburseMethod || '—'],
            ['TK thụ hưởng', ku.beneficiaryAccount || '—'],
            ['Loại lãi suất', ku.interestType === 'flat' ? 'Trên dư nợ gốc' : 'Trên dư nợ giảm dần'],
            ['Cơ sở tính lãi', 'Lãi năm/' + ku.dayBasis],
            ['Lãi suất hiện tại', String(ku.rate).replace('.', ',') + '%/năm'],
            [t.Pay + ' gốc', PAY_PERIODS[ku.principalPeriod] + ' — từ ' + fmtDate(ku.firstPrincipalDate)],
            [t.Pay + ' lãi', PAY_PERIODS[ku.interestPeriod] + ' — từ ' + fmtDate(ku.firstInterestDate)],
            ['Phương thức ' + t.pay + ' nợ', ku.payMethod || '—'],
        ];
        return items.map(function (it) {
            return '<div class="info-item"><span class="k">' + it[0] + '</span><span class="v">' + it[1] + '</span></div>';
        }).join('');
    }

    function drawStats() {
        var paidP = 0, paidI = 0, totI = 0;
        stats.schedule.forEach(function (r, i) {
            totI += r.interest;
            if (i < paidCount) { paidP += r.principal; paidI += r.interest; }
        });
        document.getElementById('stat-row').innerHTML =
            '<div class="tp-card stat-card"><div class="tp-icon-chip chip-teal"><i class="ri-money-dollar-circle-line"></i></div>' +
            '  <div><div class="stat-label">Giá trị khoản vay</div><div class="stat-value">' + fmtMoney(ku.amount) + '</div><div class="stat-sub">' + ku.currency + '</div></div></div>' +
            '<div class="tp-card stat-card"><div class="tp-icon-chip"><i class="ri-checkbox-circle-line"></i></div>' +
            '  <div><div class="stat-label">Nợ gốc đã ' + t.pay + '</div><div class="stat-value">' + fmtMoney(paidP) + '</div><div class="stat-sub">' + Math.min(paidCount, stats.schedule.length) + '/' + stats.schedule.length + ' kỳ đã hoàn tất</div></div></div>' +
            '<div class="tp-card stat-card"><div class="tp-icon-chip chip-amber"><i class="ri-scales-3-line"></i></div>' +
            '  <div><div class="stat-label">Dư nợ hiện tại</div><div class="stat-value">' + fmtMoney(ku.amount - paidP) + '</div><div class="stat-sub">Cập nhật theo kỳ đã ' + t.pay + '</div></div></div>' +
            '<div class="tp-card stat-card"><div class="tp-icon-chip chip-blue"><i class="ri-percent-line"></i></div>' +
            '  <div><div class="stat-label">Lãi đã ' + t.pay + '</div><div class="stat-value">' + fmtMoney(paidI) + '</div><div class="stat-sub">Tổng lãi dự kiến: ' + fmtMoney(totI) + '</div></div></div>';
    }

    function drawSchedule() {
        var canPay = ku.status === 1 && paidCount < stats.schedule.length;
        document.getElementById('schedule-wrap').innerHTML = scheduleTableHTML(ku, t, paidCount, canPay);
        var btn = document.querySelector('[data-pay-idx]');
        if (btn) btn.addEventListener('click', function () {
            paidCount++;
            toast('Đã ghi nhận ' + t.pay + ' kỳ ' + paidCount + ' — khế ước ' + ku.code + ' (demo, chỉ trong phiên xem)');
            drawStats(); drawSchedule();
        });
    }

    drawStats();
    drawSchedule();
}

/* ============================================================
   Demo Kế toán HRM — Sổ Cái (S03b-DN TT99/2025 + mở rộng ERP)
   Nguồn cấu trúc: file Mau_So_Cai_TT99_2025.xlsx (user cung cấp)
   - Sổ theo TỪNG TÀI KHOẢN của TỪNG PHÁP NHÂN, dữ liệu dẫn xuất từ Sổ NKC (JOURNAL_ROWS)
   - Cột đặc trưng hình thức NKC: Trang NKC + STT NKC → hyperlink tham chiếu ngược Sổ NKC
   - Cột "Số dư lũy kế" (mở rộng ERP): dư Nợ (TK 1,2,6,8) = dư trước + Nợ − Có; dư Có (3,4,5,7) ngược lại
   - Dòng SỐ DƯ ĐẦU KỲ ► / CỘNG PS KỲ / SỐ DƯ CUỐI KỲ ► / CỘNG LŨY KẾ TỪ ĐẦU NĂM + kiểm tra cân đối
   - Header 1 hàng render động + Cấu hình cột (10 cột chuẩn cố định) + Phân trang client-side
   ============================================================ */

var NKC_PAGE_SIZE = 25; // Trang NKC = ceil(STT dòng / 25)

function renderLedgerPage() {
    function uniq(vals) { return [...new Set(vals.filter(Boolean))].sort(); }
    function selOptions(list, labelFn) {
        return '<option value="">— Tất cả —</option>' + list.map(function (v) {
            return '<option value="' + v + '">' + (labelFn ? labelFn(v) : v) + '</option>';
        }).join('');
    }
    var allAccounts = uniq(JOURNAL_ROWS.map(function (r) { return r[JR.account]; }));
    var ledgerCompanies = Object.keys(ORG).filter(function (c) {
        return JOURNAL_ROWS.some(function (r) { return r[JR.company] === c; }) || Object.keys(ORG[c].depts).length;
    });

    renderShell('ledger',
        /* ----- FILTER PANEL ----- */
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="filter-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-filter-3-line"></i></div>' +
        '      <p class="tp-section-title">Bộ lọc Sổ Cái</p>' +
        '    </div>' +
        '    <div class="d-flex gap-2">' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="ff-gear" title="Cài đặt trường lọc mặc định / mở rộng">' +
        '        <i class="ri-settings-3-line"></i> Cài đặt bộ lọc</button>' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-toggle">' +
        '        <i class="ri-equalizer-line"></i> Tìm kiếm nâng cao</button>' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-hide" title="Ẩn / hiện toàn bộ khu vực bộ lọc">' +
        '        <i class="ri-eye-off-line"></i> Ẩn bộ lọc</button>' +
        '    </div>' +
        '  </div>' +
        '  <div id="filter-body">' +
        /* quick search + nút Tìm kiếm / Nhập lại cùng hàng (đồng bộ Sổ NKC) */
        '  <div class="quick-search-row">' +
        '    <div class="quick-search">' +
        '      <i class="ri-search-line"></i>' +
        '      <input class="form-control form-control-sm" id="f-search" placeholder="Tìm theo Số CT, Diễn giải, TK đối ứng">' +
        '      <button type="button" class="btn-clear-quick-search" id="f-search-clear"><i class="ri-close-line"></i></button>' +
        '    </div>' +
        '    <button type="button" class="v2-btn v2-btn--primary btn-compact" id="f-go"><i class="ri-search-line"></i> Tìm kiếm</button>' +
        '    <button type="button" class="v2-btn v2-btn--tertiary btn-compact" id="f-clear"><i class="ri-refresh-line"></i> Nhập lại</button>' +
        '  </div>' +
        /* Trường MẶC ĐỊNH (setupFilterSettings sẽ kéo các trường được cấu hình vào đây) */
        '  <div class="form-row filter-grid" id="ff-default"></div>' +
        /* Trường MỞ RỘNG tùy chọn — trong "Tìm kiếm nâng cao"; toàn bộ trường render tại đây trước */
        '  <div class="advanced-filters collapsed" id="adv-filters">' +
        '    <div class="form-row filter-grid" id="ff-adv">' +
        '      <div class="col-md-3" data-ff="f-account"><label class="tp-label">Tài khoản <span class="field-required">*</span></label>' +
        '        <select class="form-control form-control-sm" id="f-account">' +
                allAccounts.map(function (a) { return '<option value="' + a + '"' + (a === '131' ? ' selected' : '') + '>' + a + ' — ' + (ACC_NAMES[a] || '') + '</option>'; }).join('') +
        '        </select></div>' +
        '      <div class="col-md-3" data-ff="f-company"><label class="tp-label">Công ty</label>' +
        '        <select class="form-control form-control-sm" id="f-company">' +
        '          <option value="">— Tất cả công ty —</option>' +
                ledgerCompanies.map(function (c) { return '<option value="' + c + '"' + (c === 'TPE' ? ' selected' : '') + '>' + c + ' — ' + ORG[c].name + '</option>'; }).join('') +
        '        </select></div>' +
        '      <div class="col-md-3" data-ff="f-period"><label class="tp-label">Kỳ báo cáo</label>' +
        '        <select class="form-control form-control-sm" id="f-period">' +
        '          <option value="y">Cả năm 2026</option>' +
        '          <optgroup label="Theo quý"><option value="q1">Quý I/2026</option><option value="q2">Quý II/2026</option><option value="q3">Quý III/2026</option><option value="q4">Quý IV/2026</option></optgroup>' +
        '          <optgroup label="Theo tháng">' + Array.from({ length: 12 }, function (_, i) { return '<option value="m' + (i + 1) + '"' + (i === 0 ? ' selected' : '') + '>Tháng ' + (i + 1) + '/2026</option>'; }).join('') + '</optgroup>' +
        '          <option value="custom">Tùy chọn...</option>' +
        '        </select></div>' +
        '      <div class="col-md-3" data-ff="f-from"><label class="tp-label">Từ ngày</label><input type="date" class="form-control form-control-sm" id="f-from" value="2026-01-01"></div>' +
        '      <div class="col-md-3" data-ff="f-to"><label class="tp-label">Đến ngày</label><input type="date" class="form-control form-control-sm" id="f-to" value="2026-01-31"></div>' +
        '      <div class="col-md-3" data-ff="f-dept"><label class="tp-label">Phòng ban</label><select class="form-control form-control-sm" id="f-dept"><option value="">— Tất cả —</option></select></div>' +
        '      <div class="col-md-3" data-ff="f-part"><label class="tp-label">Bộ phận</label><select class="form-control form-control-sm" id="f-part" disabled><option value="">— Tất cả —</option></select></div>' +
        '      <div class="col-md-3" data-ff="f-emp"><label class="tp-label">Nhân viên</label><select class="form-control form-control-sm" id="f-emp" disabled><option value="">— Tất cả —</option></select></div>' +
        '      <div class="col-md-3" data-ff="f-item"><label class="tp-label">Mã phí</label><select class="form-control form-control-sm f-adv" id="f-item">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.item]; }))) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-job"><label class="tp-label">Vụ việc</label><select class="form-control form-control-sm f-adv" id="f-job">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.job]; })), jobLabel) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-contract"><label class="tp-label">Hợp đồng</label><select class="form-control form-control-sm f-adv" id="f-contract">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.contract]; }))) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-customer"><label class="tp-label">Khách hàng</label><select class="form-control form-control-sm f-adv" id="f-customer">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.object]; })).filter(function (o) { return o.indexOf('KH-') === 0; }), objOptLabel) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-object"><label class="tp-label">Đối tượng</label><select class="form-control form-control-sm f-adv" id="f-object">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.object]; })), objOptLabel) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-goods"><label class="tp-label">Hàng hóa</label><select class="form-control form-control-sm f-adv" id="f-goods">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.goods]; }))) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-currency"><label class="tp-label">Loại tiền tệ</label><select class="form-control form-control-sm f-adv" id="f-currency">' + selOptions(uniq(JOURNAL_ROWS.map(function (r) { return r[JR.currency]; }))) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-internal"><label class="tp-label">GD nội bộ</label><select class="form-control form-control-sm f-adv" id="f-internal"><option value="">— Tất cả —</option><option value="Y">Y — Nội bộ tập đoàn</option><option value="N">N — Bên ngoài</option></select></div>' +
        '      <div class="col-md-3" data-ff="f-posted"><label class="tp-label">Đã ghi Sổ Cái</label><select class="form-control form-control-sm f-adv" id="f-posted"><option value="">— Tất cả —</option><option value="Y">Đã ghi</option><option value="N">Chưa ghi</option></select></div>' +
        '      <div class="col-md-3" data-ff="f-amt-min"><label class="tp-label">Số tiền từ</label><input class="form-control form-control-sm text-right" id="f-amt-min" placeholder="0"></div>' +
        '      <div class="col-md-3" data-ff="f-amt-max"><label class="tp-label">Số tiền đến</label><input class="form-control form-control-sm text-right" id="f-amt-max" placeholder="Không giới hạn"></div>' +
        '    </div>' +
        '  </div>' +
        '  </div>' +
        '</section>' +

        /* ----- DATA TABLE ----- */
        '<section class="tp-card p-3">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-booklet-line"></i></div>' +
        '      <div><h5 id="ledger-title">Sổ Cái</h5>' +
        '      <p class="tp-section-subtitle" id="ledger-sub">(Dùng cho hình thức kế toán Nhật ký chung) · Đơn vị tính: VNĐ</p></div>' +
        '    </div>' +
        '    <div class="table-actions">' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-print"><i class="ri-printer-line"></i> In sổ (mẫu S03b-DN)</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-excel"><i class="ri-file-excel-2-line"></i> Xuất Excel</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-cols" title="Chọn cột hiển thị trên bảng"><i class="ri-layout-column-line"></i> Cấu hình cột</button>' +
        '    </div>' +
        '  </div>' +
        '  <div id="ledger-note"></div>' +
        '  <div class="table-wrapper scrollbar-thin"><table class="data-table" id="ltbl">' +
        '    <thead><tr id="ltbl-head"></tr></thead>' +
        '    <tbody></tbody>' +
        '    <tfoot></tfoot>' +
        '  </table></div>' +
        '  <div class="table-pager" id="ltbl-pager"></div>' +
        '  <div class="d-flex align-center gap-2 mt-2" id="ltbl-summary"></div>' +
        '</section>' +

        /* ----- Modal In sổ ----- */
        '<div class="modal-backdrop-demo" id="print-modal"><div class="modal-dialog" style="max-width:1000px">' +
        '  <div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-printer-line"></i></span>In Sổ Cái — Mẫu số S03b-DN (TT 99/2025/TT-BTC)</h5>' +
        '  <button type="button" class="close" onclick="closeModal(\'print-modal\')">×</button></div>' +
        '  <div class="modal-body" id="print-preview" style="max-height:70vh"></div>' +
        '  <div class="modal-footer">' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-do-print"><i class="ri-printer-line"></i> In</button>' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'print-modal\')"><i class="ri-close-line"></i> Đóng</button>' +
        '  </div>' +
        '</div></div>' +
        '<div id="print-area"></div>');

    /* ----- Cascade PB → BP → NV theo công ty ----- */
    var fCompany = document.getElementById('f-company');
    var fDept = document.getElementById('f-dept');
    var fPart = document.getElementById('f-part');
    var fEmp = document.getElementById('f-emp');
    function fillSelect(sel, list, labelFn) {
        sel.innerHTML = '<option value="">— Tất cả —</option>' + list.map(function (v) {
            return '<option value="' + v + '">' + (labelFn ? labelFn(v) : v) + '</option>';
        }).join('');
        sel.disabled = !list.length;
    }
    function cascade(level) {
        var c = fCompany.value;
        if (level <= 0) fillSelect(fDept, c ? Object.keys(ORG[c].depts) : [], function (d) { return d + ' — ' + ORG[c].depts[d].name; });
        if (level <= 1) {
            var d1 = fDept.value;
            fillSelect(fPart, (c && d1) ? Object.keys(ORG[c].depts[d1].parts) : []);
            if (!(c && d1)) fPart.disabled = true;
        }
        if (level <= 2) {
            var d2 = fDept.value, p2 = fPart.value;
            fillSelect(fEmp, (c && d2 && p2) ? ORG[c].depts[d2].parts[p2] : [], function (e) { return e + ' — ' + (EMP_NAMES[e] || ''); });
            if (!(c && d2 && p2)) fEmp.disabled = true;
        }
    }
    fCompany.addEventListener('change', function () { cascade(0); draw(); });
    fDept.addEventListener('change', function () { cascade(1); draw(); });
    fPart.addEventListener('change', function () { cascade(2); draw(); });
    fEmp.addEventListener('change', draw);

    /* toggle nâng cao + badge */
    var collapsed = true;
    function updateAdvBadge() {
        // Không đếm các trường bắt buộc (TK/kỳ/ngày) và nhóm tổ chức — chỉ đếm điều kiện phân tích
        var n = ['f-customer', 'f-item', 'f-job', 'f-object', 'f-contract', 'f-goods', 'f-currency', 'f-internal', 'f-posted', 'f-amt-min', 'f-amt-max']
            .filter(function (id) { return String(val(id)).trim() !== ''; }).length;
        var btn = document.getElementById('f-toggle');
        btn.innerHTML = '<i class="' + (collapsed ? 'ri-equalizer-line' : 'ri-arrow-up-s-line') + '"></i> ' +
            (collapsed ? 'Tìm kiếm nâng cao' : 'Ẩn tìm kiếm nâng cao') + (n ? ' <span class="adv-count">' + n + '</span>' : '');
    }
    document.getElementById('f-toggle').addEventListener('click', function () {
        collapsed = !collapsed;
        document.getElementById('adv-filters').classList.toggle('collapsed', collapsed);
        updateAdvBadge();
    });

    /* ẩn / hiện toàn bộ khu vực bộ lọc (helper chung, lưu trạng thái theo màn) */
    setupFilterHide({ storageKey: 'demo-filter-ledger-hidden', btnId: 'f-hide', bodyId: 'filter-body' });

    /* Kỳ báo cáo ↔ Từ/Đến ngày */
    document.getElementById('f-period').addEventListener('change', function () {
        var range = PERIODS[this.value];
        if (range) { document.getElementById('f-from').value = range[0]; document.getElementById('f-to').value = range[1]; }
        draw();
    });
    ['f-from', 'f-to'].forEach(function (id) {
        document.getElementById(id).addEventListener('change', function () {
            document.getElementById('f-period').value = 'custom';
            draw();
        });
    });
    document.getElementById('f-account').addEventListener('change', draw);
    document.querySelectorAll('.f-adv').forEach(function (el) { el.addEventListener('change', draw); });
    /* quick search: Enter/nút Tìm kiếm mới lọc (đồng bộ NKC); số tiền: format nghìn + lọc ngay */
    document.getElementById('f-search').addEventListener('keydown', function (e) { if (e.key === 'Enter') draw(); });
    document.getElementById('f-search').addEventListener('input', function () {
        document.getElementById('f-search-clear').style.display = this.value ? 'inline-flex' : 'none';
    });
    document.getElementById('f-search-clear').addEventListener('click', function () {
        document.getElementById('f-search').value = ''; draw();
    });
    ['f-amt-min', 'f-amt-max'].forEach(function (id) {
        var inp = document.getElementById(id);
        bindMoneyInput(inp);
        inp.addEventListener('input', draw);
    });
    document.getElementById('f-go').addEventListener('click', draw);
    document.getElementById('f-clear').addEventListener('click', function () {
        ['f-search', 'f-dept', 'f-part', 'f-emp', 'f-customer', 'f-item', 'f-job', 'f-object', 'f-contract', 'f-goods', 'f-currency', 'f-internal', 'f-posted', 'f-amt-min', 'f-amt-max'].forEach(function (id) { document.getElementById(id).value = ''; });
        document.getElementById('f-account').value = '131';
        fCompany.value = 'TPE';
        document.getElementById('f-period').value = 'm1';
        document.getElementById('f-from').value = PERIODS.m1[0];
        document.getElementById('f-to').value = PERIODS.m1[1];
        cascade(0);
        draw();
    });
    document.getElementById('btn-excel').addEventListener('click', function () {
        toast('Demo: file Excel sẽ được tải xuống ở bản chính thức', 'info');
    });

    function val(id) { return document.getElementById(id).value; }

    /* ----- TK đối ứng: các TK ở vế bên kia trong cùng chứng từ ----- */
    function counterAccounts(row) {
        var isDebit = row[JR.debit] > 0;
        var accs = JOURNAL_ROWS.filter(function (o) {
            return o[JR.docNo] === row[JR.docNo] && o[JR.company] === row[JR.company] &&
                o[JR.line] !== row[JR.line] && (isDebit ? o[JR.credit] > 0 : o[JR.debit] > 0);
        }).map(function (o) { return o[JR.account]; });
        return [...new Set(accs)].join(', ');
    }
    function nkcPage(line) { return Math.ceil(line / NKC_PAGE_SIZE); }
    function nkcLink(line, text) {
        return '<a href="so-nhat-ky-chung.html?line=' + line + '" title="Mở Sổ Nhật ký chung đúng dòng bút toán ' + line + '" style="color:#1d4ed8;font-weight:600">' + text + '</a>';
    }

    /* ----- Lọc ----- */
    function baseRows() { // dòng của TK + công ty (trống = tất cả công ty; chưa xét ngày/chiều phân tích)
        return JOURNAL_ROWS.filter(function (r) {
            return r[JR.account] === val('f-account') && (!val('f-company') || r[JR.company] === val('f-company'));
        });
    }
    function advMatch(r) {
        if (val('f-dept') && r[JR.dept] !== val('f-dept')) return false;
        if (val('f-part') && r[JR.part] !== val('f-part')) return false;
        if (val('f-emp') && r[JR.emp] !== val('f-emp')) return false;
        if (val('f-customer') && r[JR.object] !== val('f-customer')) return false;
        if (val('f-item') && r[JR.item] !== val('f-item')) return false;
        if (val('f-job') && r[JR.job] !== val('f-job')) return false;
        if (val('f-object') && r[JR.object] !== val('f-object')) return false;
        if (val('f-contract') && r[JR.contract] !== val('f-contract')) return false;
        if (val('f-goods') && r[JR.goods] !== val('f-goods')) return false;
        if (val('f-currency') && r[JR.currency] !== val('f-currency')) return false;
        if (val('f-internal') && r[JR.internal] !== val('f-internal')) return false;
        if (val('f-posted') && (isPosted(r) ? 'Y' : 'N') !== val('f-posted')) return false;
        var amtMin = parseMoney(val('f-amt-min'));
        var amtMax = parseMoney(val('f-amt-max'));
        var amount = r[JR.debit] || r[JR.credit];
        if (amtMin > 0 && amount < amtMin) return false;
        if (amtMax > 0 && amount > amtMax) return false;
        var kw = val('f-search').toLowerCase().trim();
        if (kw && (r[JR.docNo] + ' ' + r[JR.desc] + ' ' + counterAccounts(r)).toLowerCase().indexOf(kw) === -1) return false;
        return true;
    }
    function hasAnalyticFilter() {
        return ['f-dept', 'f-part', 'f-emp', 'f-customer', 'f-item', 'f-job', 'f-object', 'f-contract', 'f-goods', 'f-currency', 'f-internal', 'f-posted', 'f-amt-min', 'f-amt-max', 'f-search']
            .some(function (id) { return String(val(id)).trim() !== ''; });
    }

    /* Số dư: dư Nợ = trước + Nợ − Có; dư Có = trước + Có − Nợ */
    function applyBalance(acc, balance, debit, credit) {
        return isDebitNature(acc) ? balance + debit - credit : balance + credit - debit;
    }
    /* Số dư đầu kỳ = số dư đầu năm + toàn bộ PS trước "Từ ngày" (theo TK + Công ty; trống = cộng mọi pháp nhân) */
    function openingBalance(acc, company, from) {
        var bal = 0;
        if (company) bal = openingOf(company, acc);
        else Object.keys(OPENING).forEach(function (c) { bal += openingOf(c, acc); });
        JOURNAL_ROWS.forEach(function (r) {
            if (r[JR.account] === acc && (!company || r[JR.company] === company) && from && r[JR.date] < from) {
                bal = applyBalance(acc, bal, r[JR.debit], r[JR.credit]);
            }
        });
        return bal;
    }

    /* ----- Cột hiển thị (header 1 hàng, render động + cấu hình ẩn/hiện) -----
       8 cột đầu = cột chuẩn mẫu S03b-DN + Số dư lũy kế (đặc trưng Sổ Cái) → bắt buộc, cố định.
       (2 cột Trang NKC / STT NKC đã bỏ khỏi bảng hiển thị theo yêu cầu; vẫn giữ ở bản in mẫu chuẩn.)
       Cột mở rộng: chiều phân tích trước, 4 cột tổ chức VỀ CUỐI. */
    var COLUMNS = [
        { key: 'date', label: 'Ngày ghi sổ', always: true },
        { key: 'docNo', label: 'Số CT', always: true },
        { key: 'docDate', label: 'Ngày CT', always: true },
        { key: 'desc', label: 'Diễn giải', style: 'min-width:220px', always: true },
        { key: 'counter', label: 'TK ĐƯ', cls: 'text-center', always: true },
        { key: 'debit', label: 'PS Nợ', cls: 'text-right', always: true },
        { key: 'credit', label: 'PS Có', cls: 'text-right', always: true },
        { key: 'balance', label: 'Số dư lũy kế', cls: 'text-right', always: true },
        { key: 'item', label: 'Mã phí' },
        { key: 'object', label: 'Mã đối tượng' },
        { key: 'objectName', label: 'Tên đối tượng', style: 'min-width:180px' },
        { key: 'job', label: 'Vụ việc', style: 'min-width:180px' },
        { key: 'contract', label: 'Hợp đồng' },
        { key: 'goods', label: 'Hàng hóa' },
        { key: 'currency', label: 'Loại tiền', cls: 'text-center' },
        { key: 'rate', label: 'Tỷ giá', cls: 'text-right' },
        { key: 'internal', label: 'GD nội bộ', cls: 'text-center' },
        { key: 'company', label: 'Công ty' },
        { key: 'dept', label: 'Phòng ban' },
        { key: 'part', label: 'Bộ phận' },
        { key: 'emp', label: 'Nhân viên' },
    ];
    /* Cấu hình cột (helper chung): 10 cột chuẩn khóa đầu bảng, cột mở rộng tick + kéo thả */
    var colCfg = setupColumnConfig({
        storageKey: 'demo-ledger-columns',
        btnId: 'btn-cols',
        columns: COLUMNS,
        fixedNote: '8 cột chuẩn theo mẫu S03b-DN (gồm Số dư lũy kế) là <b>bắt buộc</b> và cố định ở đầu bảng.',
        onChange: function () { renderHeader(); draw(); },
    });
    /* ----- Sort theo cột (click header). Không sort → thứ tự chuẩn kế toán (theo ngày ghi sổ + STT NKC).
       LƯU Ý NGHIỆP VỤ: sort chỉ đổi THỨ TỰ HIỂN THỊ các dòng — giá trị "Số dư lũy kế" của TỪNG DÒNG
       GIỮ NGUYÊN như đã tính theo trình tự thời gian trên toàn bộ phát sinh (giống NKC giữ STT dòng khi sort).
       Bản in mẫu S03b-DN LUÔN theo trình tự thời gian, không theo sort cột. */
    var sortState = null;
    var SORT_NUMERIC = { debit: 1, credit: 1, balance: 1, rate: 1 };
    /* Giá trị dùng để so sánh của 1 dòng hiển thị {r, balance} theo key cột (mapping đúng như cellHTML) */
    function sortValue(item, key) {
        switch (key) {
            case 'balance': return item.balance;                 // Số dư lũy kế đã tính sẵn của dòng
            case 'counter': return counterAccounts(item.r);      // TK đối ứng (chuỗi)
            case 'objectName': return objName(item.r[JR.object]); // Tên đối tượng (danh mục)
            default: return item.r[JR[key]];                     // các cột dữ liệu còn lại
        }
    }
    /* Sort TOÀN BỘ displayRows trước khi phân trang; tie-break theo thứ tự gốc trong danh sách
       (gắn chỉ số trước khi sort → sort ổn định, dòng bằng nhau giữ trình tự thời gian) */
    function applySort(displayRows) {
        if (!sortState) return displayRows;
        var key = sortState.key, asc = sortState.dir === 'asc' ? 1 : -1;
        var indexed = displayRows.map(function (item, i) { return { item: item, i: i }; });
        indexed.sort(function (a, b) {
            var x = sortValue(a.item, key), y = sortValue(b.item, key);
            if (SORT_NUMERIC[key]) return ((x || 0) - (y || 0)) * asc || (a.i - b.i);
            x = x == null ? '' : String(x);
            y = y == null ? '' : String(y);
            if (x === y) return a.i - b.i;
            return (x < y ? -1 : 1) * asc;
        });
        return indexed.map(function (o) { return o.item; });
    }

    function renderHeader() {
        var visCols = colCfg.visible();
        document.getElementById('ltbl-head').innerHTML = visCols.map(function (c) {
            return '<th' + (c.cls ? ' class="' + c.cls + '"' : '') + (c.style ? ' style="' + c.style + '"' : '') + '>' + c.label + '</th>';
        }).join('');
        /* Cột đang sort bị ẩn (cấu hình cột) → bỏ sort, trả về thứ tự chuẩn */
        if (sortState && !visCols.some(function (c) { return c.key === sortState.key; })) sortState = null;
        /* Re-init icon sort mỗi lần render lại header (header render động theo cấu hình cột) */
        setupColumnSort({
            tableSel: '#ltbl',
            headRow: 1,
            cols: visCols.map(function (c) { return { key: c.key }; }),
            onChange: function (s) { sortState = s; draw(); },
        });
    }
    /* Ô dữ liệu theo cột — bal = số dư lũy kế đã tính sẵn của dòng (trên TOÀN BỘ dòng trong kỳ) */
    function cellHTML(r, c, bal) {
        switch (c.key) {
            case 'date': return '<td class="num">' + fmtDate(r[JR.date]) + '</td>';
            case 'docNo': return '<td><span class="cell-title" style="font-size:12px">' + r[JR.docNo] + '</span></td>';
            case 'docDate': return '<td class="num">' + fmtDate(r[JR.docDate]) + '</td>';
            case 'desc': return '<td style="white-space:normal">' + r[JR.desc] + '</td>';
            case 'counter': return '<td class="text-center"><b>' + counterAccounts(r) + '</b></td>';
            case 'debit': return '<td class="text-right num">' + (r[JR.debit] ? fmtMoney(r[JR.debit]) : '') + '</td>';
            case 'credit': return '<td class="text-right num">' + (r[JR.credit] ? fmtMoney(r[JR.credit]) : '') + '</td>';
            case 'balance': return '<td class="text-right num"><b>' + fmtMoney(bal) + '</b></td>';
            case 'objectName': return '<td style="white-space:normal">' + objName(r[JR.object]) + '</td>';
            case 'job': return '<td>' + jobLabel(r[JR.job]) + '</td>';
            case 'currency': return '<td class="text-center">' + r[JR.currency] + '</td>';
            case 'rate': return '<td class="text-right num">' + fmtMoney(r[JR.rate]) + '</td>';
            case 'internal': return '<td class="text-center">' + (r[JR.internal] === 'Y' ? '<span class="status-pill st-paused">Y</span>' : '<span class="status-pill st-none">N</span>') + '</td>';
            case 'emp': return '<td>' + (r[JR.emp] ? '<span title="' + (EMP_NAMES[r[JR.emp]] || '') + '">' + r[JR.emp] + '</span>' : '') + '</td>';
            default: return '<td>' + r[JR[c.key]] + '</td>'; // item, object, contract, goods, company, dept, part
        }
    }

    /* ----- Phân trang (helper chung) — chỉ dòng dữ liệu bị phân trang; SDĐK/PS/SDCK tính trên full list ----- */
    var pager = createPager({ storageKey: 'demo-ledger-pagesize', containerSel: '#ltbl-pager', onChange: function () { draw(); } });
    /* Đổi bộ lọc → tự về trang 1; chuyển trang giữ nguyên bộ lọc */
    function filterSignature() {
        return ['f-search', 'f-account', 'f-company', 'f-dept', 'f-part', 'f-emp', 'f-period', 'f-from', 'f-to',
            'f-item', 'f-job', 'f-contract', 'f-customer', 'f-object', 'f-goods', 'f-currency',
            'f-internal', 'f-posted', 'f-amt-min', 'f-amt-max'].map(val).join('|') +
            '|' + JSON.stringify(sortState); // đổi sort → tự về trang 1
    }

    function draw() {
        var acc = val('f-account'), company = val('f-company');
        var from = val('f-from'), to = val('f-to');
        var nature = isDebitNature(acc) ? 'Nợ' : 'Có';
        var filtered = hasAnalyticFilter();
        document.getElementById('f-search-clear').style.display = val('f-search') ? 'inline-flex' : 'none';

        document.getElementById('ledger-title').textContent = 'Sổ Cái — TK ' + acc + ' — ' + (ACC_NAMES[acc] || '');
        document.getElementById('ledger-sub').textContent = '(Dùng cho hình thức kế toán Nhật ký chung) · ' +
            (company ? company + ' — ' + ORG[company].name : 'Toàn tập đoàn — tổng hợp ' + Object.keys(OPENING).join(', ')) + ' · Đơn vị tính: VNĐ';
        document.getElementById('ledger-note').innerHTML = filtered
            ? '<div class="note-box"><i class="ri-information-line"></i> Đang áp dụng bộ lọc phân tích — cột <b>Số dư lũy kế</b> và các dòng Số dư đầu/cuối kỳ vẫn tính trên <b>toàn bộ phát sinh của tài khoản</b> (không bị loại trừ theo bộ lọc).</div>'
            : '';

        var rows = baseRows()
            .filter(function (r) { return (!from || r[JR.date] >= from) && (!to || r[JR.date] <= to); })
            .sort(function (a, b) { return a[JR.date] === b[JR.date] ? a[JR.line] - b[JR.line] : (a[JR.date] < b[JR.date] ? -1 : 1); });

        var opening = openingBalance(acc, company, from);
        var tbody = document.querySelector('#ltbl tbody');
        var tfoot = document.querySelector('#ltbl tfoot');
        var visCols = colCfg.visible();
        var sig = filterSignature();
        /* 10 cột cố định luôn hiện → dòng đặc biệt chỉ điều chỉnh colspan phần đuôi */
        var trailTd = visCols.length > 10 ? '<td colspan="' + (visCols.length - 10) + '"></td>' : '';

        /* Số dư ghi vào cột PS Nợ / PS Có theo tính chất TK + cột Số dư lũy kế (3 cột trong nhóm cố định) */
        function balanceRow(cls, label, amount) {
            var isDebit = isDebitNature(acc);
            return '<tr class="' + cls + '"><td colspan="7"><b>' + label + '</b></td>' +
                '<td class="text-right num"><b>' + (isDebit ? fmtMoney(amount) : '') + '</b></td>' +
                '<td class="text-right num"><b>' + (!isDebit ? fmtMoney(amount) : '') + '</b></td>' +
                '<td class="text-right num"><b>' + fmtMoney(amount) + '</b></td>' +
                trailTd + '</tr>';
        }
        var openRow = balanceRow('row-carry', 'SỐ DƯ ĐẦU KỲ (' + nature + ')  ►', opening);

        /* Số dư lũy kế tính trên TOÀN BỘ dòng trong kỳ (kể cả dòng bị bộ lọc phân tích ẩn);
           chỉ dòng qua bộ lọc mới đưa vào danh sách hiển thị (bị phân trang) */
        var totD = 0, totC = 0, balance = opening;
        var displayRows = [];
        rows.forEach(function (r) {
            var shown = advMatch(r);
            balance = applyBalance(acc, balance, r[JR.debit], r[JR.credit]);
            if (shown) {
                totD += r[JR.debit]; totC += r[JR.credit];
                displayRows.push({ r: r, balance: balance });
            }
        });
        var shownCount = displayRows.length;

        // Số dư cuối kỳ + tổng PS luôn tính trên TOÀN BỘ dòng của TK trong kỳ
        var fullD = 0, fullC = 0;
        rows.forEach(function (r) { fullD += r[JR.debit]; fullC += r[JR.credit]; });
        var closing = applyBalance(acc, opening, fullD, fullC);
        // Lũy kế từ đầu năm (01/01 → Đến ngày)
        var ytdD = 0, ytdC = 0;
        baseRows().forEach(function (r) {
            if (r[JR.date] >= '2026-01-01' && (!to || r[JR.date] <= to)) { ytdD += r[JR.debit]; ytdC += r[JR.credit]; }
        });

        var totalRow = '<tr class="row-total"><td colspan="7">CỘNG SỐ PHÁT SINH KỲ' + (filtered ? ' (theo bộ lọc — ' + shownCount + '/' + rows.length + ' dòng)' : ' (' + rows.length + ' dòng)') + '</td>' +
            '<td class="text-right num">' + fmtMoney(filtered ? totD : fullD) + '</td>' +
            '<td class="text-right num">' + fmtMoney(filtered ? totC : fullC) + '</td>' +
            '<td></td>' + trailTd + '</tr>';
        var closingRow = balanceRow('row-total', 'SỐ DƯ CUỐI KỲ (' + nature + ')  ►', closing);
        var ytdRow = '<tr><td colspan="7">CỘNG LŨY KẾ TỪ ĐẦU NĂM</td>' +
            '<td class="text-right num">' + fmtMoney(ytdD) + '</td>' +
            '<td class="text-right num">' + fmtMoney(ytdC) + '</td>' +
            '<td></td>' + trailTd + '</tr>';

        /* dòng tổng đưa lên ĐẦU bảng (sticky) + giữ bản sao ở tfoot; chỉ dòng dữ liệu bị phân trang */
        if (!rows.length) {
            tbody.innerHTML = openRow + totalRow + closingRow +
                '<tr><td colspan="' + visCols.length + '"><div class="empty-state"><div class="es-icon"><i class="ri-inbox-2-line"></i></div>Không có phát sinh của TK ' + acc + ' (' + (company || 'tất cả công ty') + ') trong kỳ.</div></td></tr>';
            pager.paginate([], sig);
        } else {
            /* Sort theo cột (nếu có) trên TOÀN BỘ dòng hiển thị TRƯỚC khi phân trang.
               Chỉ đổi thứ tự dòng — "Số dư lũy kế" từng dòng giữ nguyên giá trị đã tính theo trình tự thời gian;
               các dòng SDĐK / CỘNG PS / SDCK / lũy kế năm không bị ảnh hưởng bởi sort. */
            var pageRows = pager.paginate(applySort(displayRows), sig);
            tbody.innerHTML = openRow + totalRow + closingRow + pageRows.map(function (d) {
                return '<tr>' + visCols.map(function (c) { return cellHTML(d.r, c, d.balance); }).join('') + '</tr>';
            }).join('');
        }
        tfoot.innerHTML = ''; // bỏ 3 dòng tổng cuối bảng (đã có dòng tổng ở đầu bảng)
        applyStickyTotals('#ltbl');

        var ok = closing === applyBalance(acc, opening, fullD, fullC); // luôn đúng theo công thức — hiển thị minh hoạ
        document.getElementById('ltbl-summary').innerHTML =
            '<span class="tp-small-text">Kiểm tra cân đối: SDĐK ' + (isDebitNature(acc) ? '+ PS Nợ − PS Có' : '+ PS Có − PS Nợ') + ' = SDCK → ' +
            fmtMoney(opening) + (isDebitNature(acc) ? ' + ' + fmtMoney(fullD) + ' − ' + fmtMoney(fullC) : ' + ' + fmtMoney(fullC) + ' − ' + fmtMoney(fullD)) + ' = ' + fmtMoney(closing) + '</span> ' +
            (ok ? '<span class="status-pill st-done"><i class="ri-checkbox-circle-line"></i>CÂN ĐỐI</span>' : '<span class="status-pill st-cancel">LỆCH</span>');
        updateAdvBadge();
        pager.render();
    }

    /* ----- In sổ mẫu chuẩn S03b-DN (GIỮ NGUYÊN — không theo cấu hình cột/phân trang) ----- */
    function printSheetHTML() {
        var acc = val('f-account'), company = val('f-company');
        var from = val('f-from'), to = val('f-to');
        var nature = isDebitNature(acc) ? 'Nợ' : 'Có';
        var rows = baseRows()
            .filter(function (r) { return advMatch(r) && (!from || r[JR.date] >= from) && (!to || r[JR.date] <= to); })
            .sort(function (a, b) { return a[JR.date] === b[JR.date] ? a[JR.line] - b[JR.line] : (a[JR.date] < b[JR.date] ? -1 : 1); });
        var opening = openingBalance(acc, company, from);
        var balance = opening, totD = 0, totC = 0;
        var body = rows.map(function (r) {
            balance = applyBalance(acc, balance, r[JR.debit], r[JR.credit]);
            totD += r[JR.debit]; totC += r[JR.credit];
            return '<tr>' +
                '<td class="pc">' + fmtDate(r[JR.date]) + '</td>' +
                '<td class="pc">' + r[JR.docNo] + '</td>' +
                '<td class="pc">' + fmtDate(r[JR.docDate]) + '</td>' +
                '<td>' + r[JR.desc] + '</td>' +
                '<td class="pc">' + nkcPage(r[JR.line]) + '</td>' +
                '<td class="pc">' + r[JR.line] + '</td>' +
                '<td class="pc">' + counterAccounts(r) + '</td>' +
                '<td class="pr">' + (r[JR.debit] ? fmtMoney(r[JR.debit]) : '') + '</td>' +
                '<td class="pr">' + (r[JR.credit] ? fmtMoney(r[JR.credit]) : '') + '</td>' +
                '<td class="pr">' + fmtMoney(balance) + '</td>' +
                '</tr>';
        }).join('');
        var ytdD = 0, ytdC = 0;
        baseRows().forEach(function (r) {
            if (r[JR.date] >= '2026-01-01' && (!to || r[JR.date] <= to)) { ytdD += r[JR.debit]; ytdC += r[JR.credit]; }
        });
        return '<div class="print-sheet">' +
            '<table class="p-head"><tr>' +
            '<td style="width:55%"><b>Đơn vị:</b> ' + (company ? ORG[company].name : 'TẬP ĐOÀN TÂN PHÁT (tổng hợp ' + Object.keys(OPENING).join(', ') + ')') + '<br><b>Địa chỉ:</b> ……………………………</td>' +
            '<td style="text-align:center"><b>Mẫu số S03b - DN</b><br><i style="font-size:10.5px">(Ban hành theo Thông tư số 99/2025/TT-BTC<br>ngày 17/10/2025 của Bộ Tài chính)</i></td>' +
            '</tr></table>' +
            '<div class="p-title">SỔ CÁI</div>' +
            '<div class="p-sub"><i>(Dùng cho hình thức kế toán Nhật ký chung)</i></div>' +
            '<div class="p-sub">Năm: 2026' + (from || to ? ' (Từ ' + fmtDate(from) + ' đến ' + fmtDate(to) + ')' : '') + '</div>' +
            '<div class="p-sub">Tên tài khoản: <b>' + (ACC_NAMES[acc] || '') + '</b> &nbsp;·&nbsp; Số hiệu: <b>' + acc + '</b></div>' +
            '<div class="p-unit">Đơn vị tính: VNĐ</div>' +
            '<table class="p-grid">' +
            '<thead>' +
            '<tr><th rowspan="2">Ngày, tháng<br>ghi sổ</th><th colspan="2">Chứng từ</th><th rowspan="2" style="width:24%">Diễn giải</th>' +
            '<th colspan="2">Nhật ký chung</th><th rowspan="2">Số hiệu<br>TK đối ứng</th><th colspan="2">Số phát sinh</th><th rowspan="2">Số dư</th></tr>' +
            '<tr><th>Số hiệu</th><th>Ngày, tháng</th><th>Trang<br>số</th><th>STT<br>dòng</th><th>Nợ</th><th>Có</th></tr>' +
            '<tr class="p-abc"><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>G</th><th>H</th><th>1</th><th>2</th><th>3</th></tr>' +
            '</thead><tbody>' +
            '<tr><td colspan="7" style="text-align:left"><b>Số dư đầu kỳ (' + nature + ')</b></td><td></td><td></td><td class="pr"><b>' + fmtMoney(opening) + '</b></td></tr>' +
            body +
            '<tr class="p-total"><td colspan="7" style="text-align:left"><b>Cộng số phát sinh kỳ</b></td>' +
            '<td class="pr"><b>' + fmtMoney(totD) + '</b></td><td class="pr"><b>' + fmtMoney(totC) + '</b></td><td></td></tr>' +
            '<tr class="p-total"><td colspan="7" style="text-align:left"><b>Số dư cuối kỳ (' + nature + ')</b></td><td></td><td></td><td class="pr"><b>' + fmtMoney(balance) + '</b></td></tr>' +
            '<tr class="p-total"><td colspan="7" style="text-align:left"><b>Cộng lũy kế từ đầu năm</b></td>' +
            '<td class="pr"><b>' + fmtMoney(ytdD) + '</b></td><td class="pr"><b>' + fmtMoney(ytdC) + '</b></td><td></td></tr>' +
            '</tbody></table>' +
            '<div class="p-note">- Sổ này có …. trang, đánh số từ trang số 01 đến trang ….<br>- Ngày mở sổ: ……………</div>' +
            '<table class="p-sign"><tr>' +
            '<td><b>Người ghi sổ</b><br><i>(Ký, họ tên)</i></td>' +
            '<td><b>Kế toán trưởng</b><br><i>(Ký, họ tên)</i></td>' +
            '<td><i>Ngày ... tháng ... năm ...</i><br><b>Người đại diện theo pháp luật</b><br><i>(Ký, họ tên, đóng dấu)</i></td>' +
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

    /* Cài đặt bộ lọc: mặc định = bắt buộc (TK sổ / kỳ / từ–đến ngày); mọi trường khác vào "Tìm kiếm nâng cao".
       Nhóm tổ chức = 1 checkbox di chuyển cả khối Công ty – Phòng ban – Bộ phận. */
    setupFilterSettings({
        storageKey: 'demo-filter-ledger',
        gearBtnId: 'ff-gear',
        defaultWrap: 'ff-default',
        advWrap: 'ff-adv',
        fields: [
            { id: 'f-account', label: 'Tài khoản', locked: true },
            { id: 'f-period', label: 'Kỳ báo cáo', locked: true },
            { id: 'f-from', label: 'Từ ngày', locked: true },
            { id: 'f-to', label: 'Đến ngày', locked: true },
            { id: 'grp-org', label: 'Công ty – Phòng ban – Bộ phận', ids: ['f-company', 'f-dept', 'f-part'] },
            { id: 'f-emp', label: 'Nhân viên' },
            { id: 'f-customer', label: 'Khách hàng' },
            { id: 'f-item', label: 'Mã phí' },
            { id: 'f-job', label: 'Vụ việc' },
            { id: 'f-object', label: 'Đối tượng' },
            { id: 'f-contract', label: 'Hợp đồng' },
            { id: 'f-goods', label: 'Hàng hóa' },
            { id: 'f-currency', label: 'Loại tiền tệ' },
            { id: 'f-internal', label: 'GD nội bộ' },
            { id: 'f-posted', label: 'Đã ghi Sổ Cái' },
            { id: 'f-amt-min', label: 'Số tiền từ' },
            { id: 'f-amt-max', label: 'Số tiền đến' },
        ],
    });

    renderHeader();
    cascade(0);
    draw();
}

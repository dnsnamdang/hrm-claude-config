/* ============================================================
   Demo Kế toán HRM — BẢNG KÊ CHỨNG TỪ THEO MÃ PHÍ
   Tham khảo Fast Accounting Online rpt_gldtbkb (03.50.15)
   — file Excel mẫu: "Bảng kê chứng từ theo mã phí - 20260526174249.xlsx"
   — ảnh khảo sát: tham-khao/fast-bkct-maphi-filter.png / fast-bkct-maphi-report.png
   - NGUỒN DỮ LIỆU: các dòng bút toán trong JOURNAL_ROWS có gắn Mã phí (COST_CODES).
     Mỗi nghiệp vụ hiện ĐỦ 2 VẾ (leg Nợ + leg Có) → tổng nhóm Nợ = Có.
   - NHÓM theo Mã phí: dòng header nhóm "<Mã> — <Tên>" + tổng nhóm (Nợ/Có),
     các dòng chứng từ, xếp theo mã phí.
   - Cột chuẩn Fast (khóa): Ngày ct · Mã ct · Số ct · Diễn giải · Tài khoản ·
     Tk đối ứng · PS Nợ · PS Có + cột mở rộng cấu hình được.
   ============================================================ */

var CV_DOC_TYPES = { 'PC': 'Phiếu chi', 'PKT': 'Phiếu kế toán' };
/* Mã chứng từ (loại ct) suy từ tiền tố số chứng từ */
function cvDocType(docNo) {
    if (/^PC/.test(docNo)) return 'PC';
    return 'PKT'; // PKT-*, BL-* (phân bổ lương), PB-* (phân bổ khấu hao)
}
/* TK đối ứng: các TK ở vế bên kia trong cùng chứng từ (cùng công ty) */
function cvContra(row) {
    var isDebit = row[JR.debit] > 0;
    var accs = JOURNAL_ROWS.filter(function (o) {
        return o[JR.docNo] === row[JR.docNo] && o[JR.company] === row[JR.company] &&
            o[JR.line] !== row[JR.line] && (isDebit ? o[JR.credit] > 0 : o[JR.debit] > 0);
    }).map(function (o) { return o[JR.account]; });
    return [...new Set(accs)].join(', ');
}

function renderCostVouchersPage() {
    function selOptions(list, labelFn) {
        return '<option value="">— Tất cả —</option>' + list.map(function (v) {
            return '<option value="' + v + '">' + (labelFn ? labelFn(v) : v) + '</option>';
        }).join('');
    }
    /* Chỉ xét các dòng có gắn mã phí (thuộc COST_CODES) */
    var COST_ROWS = JOURNAL_ROWS.filter(function (r) { return isCostCode(r[JR.item]); });
    function uniq(fn) { return [...new Set(COST_ROWS.map(fn).filter(Boolean))].sort(); }

    renderShell('costvouchers',
        /* ----- FILTER (theo dialog "Điều kiện lọc" của Fast) ----- */
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="filter-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-filter-3-line"></i></div>' +
        '      <p class="tp-section-title">Bộ lọc Bảng kê chứng từ theo mã phí</p>' +
        '    </div>' +
        '    <div class="d-flex gap-2">' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="ff-gear"><i class="ri-settings-3-line"></i> Cài đặt bộ lọc</button>' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-toggle"><i class="ri-equalizer-line"></i> Tìm kiếm nâng cao</button>' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-hide" title="Ẩn / hiện toàn bộ khu vực bộ lọc"><i class="ri-eye-off-line"></i> Ẩn bộ lọc</button>' +
        '    </div>' +
        '  </div>' +
        '  <div id="filter-body">' +
        '  <div class="quick-search-row">' +
        '    <div class="quick-search">' +
        '      <i class="ri-search-line"></i>' +
        '      <input class="form-control form-control-sm" id="f-search" placeholder="Tìm theo Số ct, Diễn giải, Tài khoản, Mã phí, Tên khách">' +
        '      <button type="button" class="btn-clear-quick-search" id="f-search-clear"><i class="ri-close-line"></i></button>' +
        '    </div>' +
        '    <button type="button" class="v2-btn v2-btn--primary btn-compact" id="f-go"><i class="ri-search-line"></i> Tìm kiếm</button>' +
        '    <button type="button" class="v2-btn v2-btn--tertiary btn-compact" id="f-clear"><i class="ri-refresh-line"></i> Nhập lại</button>' +
        '  </div>' +
        '  <div class="form-row filter-grid" id="ff-default"></div>' +
        '  <div class="advanced-filters collapsed" id="adv-filters">' +
        '    <div class="form-row filter-grid" id="ff-adv">' +
        '      <div class="col-md-3" data-ff="f-period"><label class="tp-label">Kỳ báo cáo</label>' +
        '        <select class="form-control form-control-sm" id="f-period">' +
        '          <option value="y">Cả năm 2026</option>' +
        '          <optgroup label="Theo quý"><option value="q1">Quý I/2026</option><option value="q2">Quý II/2026</option><option value="q3">Quý III/2026</option><option value="q4">Quý IV/2026</option></optgroup>' +
        '          <optgroup label="Theo tháng">' + Array.from({ length: 12 }, function (_, i) { return '<option value="m' + (i + 1) + '">Tháng ' + (i + 1) + '/2026</option>'; }).join('') + '</optgroup>' +
        '          <option value="custom">Tùy chọn...</option>' +
        '        </select></div>' +
        '      <div class="col-md-3" data-ff="f-from"><label class="tp-label">Từ ngày</label><input type="date" class="form-control form-control-sm" id="f-from" value="2026-01-01"></div>' +
        '      <div class="col-md-3" data-ff="f-to"><label class="tp-label">Đến ngày</label><input type="date" class="form-control form-control-sm" id="f-to" value="2026-12-31"></div>' +
        '      <div class="col-md-3" data-ff="f-item"><label class="tp-label">Mã phí</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-item">' + selOptions(uniq(function (r) { return r[JR.item]; }), costCodeLabel) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-side"><label class="tp-label">Ghi nợ/có</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-side"><option value="">* — Tất cả</option><option value="1">1 — Chỉ vế Nợ</option><option value="2">2 — Chỉ vế Có</option></select></div>' +
        '      <div class="col-md-3" data-ff="f-account"><label class="tp-label">Tài khoản</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-account">' + selOptions(uniq(function (r) { return r[JR.account]; }), function (a) { return a + ' — ' + (ACC_NAMES[a] || ''); }) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-contra"><label class="tp-label">TK đối ứng</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-contra">' + selOptions(uniq(function (r) { return r[JR.account]; }), function (a) { return a + ' — ' + (ACC_NAMES[a] || ''); }) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-company"><label class="tp-label">Đơn vị</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-company">' + selOptions(uniq(function (r) { return r[JR.company]; }), function (c) { return c + ' — ' + ORG[c].name; }) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-template"><label class="tp-label">Mẫu báo cáo</label>' +
        '        <select class="form-control form-control-sm" id="f-template"><option value="std">Mẫu chuẩn</option><option value="fx">Mẫu ngoại tệ</option></select></div>' +
        '    </div>' +
        '  </div>' +
        '  </div>' +
        '</section>' +

        /* ----- BẢNG ----- */
        '<section class="tp-card p-3">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-price-tag-3-line"></i></div>' +
        '      <div><h5>Bảng kê chứng từ theo mã phí</h5>' +
        '      <p class="tp-section-subtitle" id="cv-subtitle">Nhóm theo Mã phí · mỗi nghiệp vụ hiện 2 vế (Nợ/Có) · Đơn vị tính: VNĐ</p></div>' +
        '    </div>' +
        '    <div class="table-actions">' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-print"><i class="ri-printer-line"></i> In bảng kê</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-excel"><i class="ri-file-excel-2-line"></i> Xuất Excel</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-cols" title="Chọn cột hiển thị trên bảng"><i class="ri-layout-column-line"></i> Cấu hình cột</button>' +
        '    </div>' +
        '  </div>' +
        '  <div class="note-box"><i class="ri-information-line"></i> <b>Ghi chú nghiệp vụ &amp; triển khai (cho đội phát triển):</b>' +
        '    <ul style="margin:6px 0 0;padding-left:18px">' +
        '      <li><b>Nguồn dữ liệu:</b> lấy TẤT CẢ dòng hạch toán (chi tiết bút toán) trong kỳ <b>có gắn Mã phí</b> (trường <code>ma_phi</code> ≠ rỗng), thuộc chứng từ <b>đã duyệt / đã ghi sổ</b>. Mỗi dòng sổ = 1 dòng bảng kê. Demo lấy từ <code>JOURNAL_ROWS</code> (lọc <code>isCostCode(item)</code>).</li>' +
        '      <li><b>Nhóm theo Mã phí:</b> gom các dòng cùng mã phí thành 1 nhóm; dòng tiêu đề nhóm hiện <code>&lt;Mã phí&gt; — &lt;Tên&gt;</code> + <b>tổng PS Nợ / PS Có của nhóm</b>. Thứ tự nhóm: theo mã phí.</li>' +
        '      <li><b>Hiện đủ 2 vế:</b> mỗi nghiệp vụ xuất hiện thành 2 dòng — 1 dòng ghi <b>Nợ</b> (số tiền ở cột PS Nợ) và 1 dòng ghi <b>Có</b> (cột PS Có). Nhờ vậy tổng nhóm & tổng cộng luôn có <b>PS Nợ = PS Có</b> (cân đối).</li>' +
        '      <li><b>TK đối ứng:</b> là các tài khoản ở <b>vế ngược lại</b> trong cùng <b>Số chứng từ + Đơn vị</b> (nhiều TK thì ghép bằng dấu phẩy). Không lưu sẵn — tính động từ các dòng cùng chứng từ.</li>' +
        '      <li><b>Danh mục mã phí:</b> mã phí khai báo ở màn <i>Danh mục mã phí</i>, được gắn vào dòng hạch toán khi lập/hạch toán chứng từ.</li>' +
        '      <li><b>Bộ lọc:</b> Kỳ (bắt buộc) · Mã phí · <b>Ghi nợ/có</b> (1 = chỉ vế Nợ, 2 = chỉ vế Có, * = cả hai) · Tài khoản · TK đối ứng · Đơn vị · <b>Mẫu báo cáo</b> (Mẫu chuẩn / Mẫu ngoại tệ — mẫu ngoại tệ hiện thêm cột Mã nt, Tỷ giá, PS Nợ/Có nguyên tệ).</li>' +
        '      <li><b>Liên kết:</b> cột <b>Số CT NKC</b> mở đúng dòng bút toán trên Sổ nhật ký chung (<code>?line=</code>). <b>In</b> theo mẫu bảng kê Fast (nhóm mã phí + Tổng cộng + chữ ký Người lập / Kế toán trưởng / Giám đốc).</li>' +
        '    </ul></div>' +
        '  <div class="table-wrapper scrollbar-thin"><table class="data-table" id="cvtbl">' +
        '    <thead><tr id="cvtbl-head"></tr></thead>' +
        '    <tbody></tbody><tfoot></tfoot>' +
        '  </table></div>' +
        '  <div class="table-pager" id="cvtbl-pager"></div>' +
        '  <div class="d-flex align-center gap-2 mt-2" id="cvtbl-summary"></div>' +
        '</section>' +

        /* ----- Modal In ----- */
        '<div class="modal-backdrop-demo" id="print-modal"><div class="modal-dialog" style="max-width:1000px">' +
        '  <div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-printer-line"></i></span>In Bảng kê chứng từ theo mã phí</h5>' +
        '  <button type="button" class="close" onclick="closeModal(\'print-modal\')">×</button></div>' +
        '  <div class="modal-body" id="print-preview" style="max-height:70vh"></div>' +
        '  <div class="modal-footer">' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-do-print"><i class="ri-printer-line"></i> In</button>' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'print-modal\')"><i class="ri-close-line"></i> Đóng</button>' +
        '  </div>' +
        '</div></div>' +
        '<div id="print-area"></div>');

    /* ----- Kỳ báo cáo → khoảng ngày ----- */
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

    /* ----- Lọc ----- */
    function val(id) { return document.getElementById(id).value; }
    function filtered() {
        var kw = val('f-search').toLowerCase().trim();
        return COST_ROWS.filter(function (r) {
            if (val('f-from') && r[JR.date] < val('f-from')) return false;
            if (val('f-to') && r[JR.date] > val('f-to')) return false;
            if (val('f-item') && r[JR.item] !== val('f-item')) return false;
            if (val('f-side') === '1' && !(r[JR.debit] > 0)) return false;
            if (val('f-side') === '2' && !(r[JR.credit] > 0)) return false;
            if (val('f-account') && r[JR.account] !== val('f-account')) return false;
            if (val('f-contra') && cvContra(r).split(', ').indexOf(val('f-contra')) === -1) return false;
            if (val('f-company') && r[JR.company] !== val('f-company')) return false;
            if (kw && (r[JR.docNo] + ' ' + r[JR.desc] + ' ' + r[JR.account] + ' ' + r[JR.item] + ' ' + costCodeName(r[JR.item]) + ' ' + r[JR.object] + ' ' + objName(r[JR.object])).toLowerCase().indexOf(kw) === -1) return false;
            return true;
        });
    }

    /* ----- Cột: 8 cột chuẩn Fast khóa + cột mở rộng cấu hình được ----- */
    var COLUMNS = [
        { key: 'date', label: 'Ngày ct', cls: 'num', always: true },
        { key: 'type', label: 'Mã ct', cls: 'text-center', always: true },
        { key: 'no', label: 'Số ct', cls: 'text-center', always: true },
        { key: 'desc', label: 'Diễn giải', style: 'min-width:240px', always: true },
        { key: 'account', label: 'Tài khoản', cls: 'text-center', always: true },
        { key: 'contra', label: 'Tk đối ứng', cls: 'text-center', always: true },
        { key: 'debit', label: 'PS Nợ', cls: 'text-right', always: true },
        { key: 'credit', label: 'PS Có', cls: 'text-right', always: true },
        { key: 'buyer', label: 'Mã khách', cls: 'text-center' },
        { key: 'buyerName', label: 'Tên khách hàng', style: 'min-width:200px' },
        { key: 'emp', label: 'Nhân viên' },
        { key: 'company', label: 'Đơn vị', cls: 'text-center' },
        { key: 'item', label: 'Mã phí', cls: 'text-center' },
        { key: 'currency', label: 'Mã nt', cls: 'text-center' },
        { key: 'rate', label: 'Tỷ giá', cls: 'text-right' },
        { key: 'debitFx', label: 'PS Nợ nt', cls: 'text-right' },
        { key: 'creditFx', label: 'PS Có nt', cls: 'text-right' },
        { key: 'nkcDoc', label: 'Số CT NKC', cls: 'text-center' },
    ];
    var colCfg = setupColumnConfig({
        storageKey: 'demo-costvouchers-columns',
        btnId: 'btn-cols',
        columns: COLUMNS,
        fixedNote: '8 cột chuẩn của bảng kê (theo mẫu Fast) là <b>bắt buộc</b> và cố định ở đầu bảng.',
        onChange: function () { renderHeader(); draw(); },
    });

    /* ----- Sort trong từng nhóm (giữ cấu trúc nhóm mã phí) ----- */
    var sortState = null;
    var SORT_NUMERIC = { debit: 1, credit: 1, rate: 1, debitFx: 1, creditFx: 1 };
    function cellValue(r, key) {
        switch (key) {
            case 'date': return r[JR.docDate];
            case 'type': return cvDocType(r[JR.docNo]);
            case 'no': return r[JR.docNo];
            case 'desc': return r[JR.desc];
            case 'account': return r[JR.account];
            case 'contra': return cvContra(r);
            case 'debit': return r[JR.debit];
            case 'credit': return r[JR.credit];
            case 'buyer': return r[JR.object];
            case 'buyerName': return objName(r[JR.object]);
            case 'emp': return r[JR.emp];
            case 'company': return r[JR.company];
            case 'item': return r[JR.item];
            case 'currency': return r[JR.currency];
            case 'rate': return r[JR.rate];
            case 'debitFx': return r[JR.debit] / (r[JR.rate] || 1);
            case 'creditFx': return r[JR.credit] / (r[JR.rate] || 1);
            case 'nkcDoc': return r[JR.line];
            default: return '';
        }
    }
    function sortRows(rows) {
        if (!sortState) return rows;
        var key = sortState.key, asc = sortState.dir === 'asc' ? 1 : -1;
        return rows.slice().sort(function (a, b) {
            var x = cellValue(a, key), y = cellValue(b, key);
            if (SORT_NUMERIC[key]) return (x - y) * asc || a[JR.line] - b[JR.line];
            if (x === y) return a[JR.line] - b[JR.line];
            return (x < y ? -1 : 1) * asc;
        });
    }

    /* Cột ngoại tệ chỉ hiện ở "Mẫu ngoại tệ" (Mẫu chuẩn ẩn — tránh trùng số VND) */
    var FX_COLS = { currency: 1, rate: 1, debitFx: 1, creditFx: 1 };
    function effectiveCols() {
        var cols = colCfg.visible();
        if (val('f-template') !== 'fx') cols = cols.filter(function (c) { return !FX_COLS[c.key]; });
        return cols;
    }

    function renderHeader() {
        var visCols = effectiveCols();
        document.getElementById('cvtbl-head').innerHTML = visCols.map(function (c) {
            return '<th' + (c.cls ? ' class="' + c.cls + '"' : '') + (c.style ? ' style="' + c.style + '"' : '') + '>' + c.label + '</th>';
        }).join('');
        if (sortState && !visCols.some(function (c) { return c.key === sortState.key; })) sortState = null;
        setupColumnSort({
            tableSel: '#cvtbl', headRow: 1,
            cols: visCols.map(function (c) { return { key: c.key }; }),
            onChange: function (s) { sortState = s; draw(); },
        });
    }

    function cellHTML(r, c) {
        switch (c.key) {
            case 'date': return '<td class="num">' + fmtDate(r[JR.docDate]) + '</td>';
            case 'type': return '<td class="text-center"><span title="' + CV_DOC_TYPES[cvDocType(r[JR.docNo])] + '"><b>' + cvDocType(r[JR.docNo]) + '</b></span></td>';
            case 'no': return '<td class="text-center"><span class="cell-title" style="font-size:12px">' + r[JR.docNo] + '</span></td>';
            case 'desc': return '<td style="white-space:normal">' + r[JR.desc] + '</td>';
            case 'account': return '<td class="text-center"><b title="' + (ACC_NAMES[r[JR.account]] || '') + '">' + r[JR.account] + '</b></td>';
            case 'contra': return '<td class="text-center">' + cvContra(r) + '</td>';
            case 'debit': return '<td class="text-right num">' + (r[JR.debit] ? fmtMoney(r[JR.debit]) : '') + '</td>';
            case 'credit': return '<td class="text-right num">' + (r[JR.credit] ? fmtMoney(r[JR.credit]) : '') + '</td>';
            case 'buyer': return '<td class="text-center">' + (r[JR.object] || '') + '</td>';
            case 'buyerName': return '<td style="white-space:normal">' + objName(r[JR.object]) + '</td>';
            case 'emp': return '<td>' + (r[JR.emp] ? '<span title="' + (EMP_NAMES[r[JR.emp]] || '') + '">' + r[JR.emp] + '</span>' : '') + '</td>';
            case 'company': return '<td class="text-center">' + r[JR.company] + '</td>';
            case 'item': return '<td class="text-center"><span title="' + costCodeName(r[JR.item]) + '">' + r[JR.item] + '</span></td>';
            case 'currency': return '<td class="text-center">' + r[JR.currency] + '</td>';
            case 'rate': return '<td class="text-right num">' + (r[JR.rate] > 1 ? numberWithSep(r[JR.rate]) : '') + '</td>';
            case 'debitFx': return '<td class="text-right num">' + (r[JR.debit] ? fmtMoney(r[JR.debit] / (r[JR.rate] || 1)) : '') + '</td>';
            case 'creditFx': return '<td class="text-right num">' + (r[JR.credit] ? fmtMoney(r[JR.credit] / (r[JR.rate] || 1)) : '') + '</td>';
            case 'nkcDoc': return '<td class="text-center"><a href="so-nhat-ky-chung.html?line=' + r[JR.line] + '" title="Mở Sổ Nhật ký chung đúng dòng bút toán" style="color:#1d4ed8;font-weight:600">' + r[JR.docNo] + '</a></td>';
            default: return '<td></td>';
        }
    }
    function numberWithSep(n) { return (typeof numberWithCommas === 'function') ? numberWithCommas(n) : fmtMoney(n); }

    /* ----- Nhóm theo mã phí (xếp theo mã phí) ----- */
    function buildGroups(list) {
        var byCode = {};
        list.forEach(function (r) { (byCode[r[JR.item]] = byCode[r[JR.item]] || []).push(r); });
        return Object.keys(byCode).sort(function (a, b) {
            return a < b ? -1 : 1;
        }).map(function (code) {
            var rows = sortRows(byCode[code]);
            var n = 0, c = 0; byCode[code].forEach(function (r) { n += r[JR.debit]; c += r[JR.credit]; });
            return { code: code, rows: rows, totN: n, totC: c, count: countDocs(byCode[code]) };
        });
    }
    function countDocs(rows) { return new Set(rows.map(function (r) { return r[JR.docNo] + '@' + r[JR.company]; })).size; }

    /* Dòng tổng (grand total / group header) — số PS Nợ/Có thẳng cột */
    function amountRowHTML(visCols, labelHTML, totN, totC, cls) {
        var di = visCols.findIndex(function (c) { return c.key === 'debit'; });
        var span = di < 0 ? visCols.length : di;
        var html = '<tr class="' + cls + '"><td colspan="' + span + '">' + labelHTML + '</td>';
        visCols.slice(span).forEach(function (c) {
            if (c.key === 'debit') html += '<td class="text-right num">' + (totN ? fmtMoney(totN) : '') + '</td>';
            else if (c.key === 'credit') html += '<td class="text-right num">' + (totC ? fmtMoney(totC) : '') + '</td>';
            else html += '<td></td>';
        });
        return html + '</tr>';
    }

    /* ----- Phân trang (helper chung) — flat qua các item nhóm/dòng ----- */
    var pager = createPager({ storageKey: 'demo-costvouchers-pagesize', defaultSize: 50, containerSel: '#cvtbl-pager', onChange: function () { draw(); } });
    function filterSignature() {
        return ['f-search', 'f-from', 'f-to', 'f-item', 'f-side', 'f-account', 'f-contra', 'f-company', 'f-template']
            .map(val).join('|') + '|' + JSON.stringify(sortState);
    }

    var collapsed = true;
    function updateAdvBadge() {
        var n = ['f-item', 'f-side', 'f-account', 'f-contra', 'f-company']
            .filter(function (id) { return String(val(id)).trim() !== ''; }).length;
        var btn = document.getElementById('f-toggle');
        var label = collapsed ? 'Tìm kiếm nâng cao' : 'Ẩn tìm kiếm nâng cao';
        var icon = collapsed ? 'ri-equalizer-line' : 'ri-arrow-up-s-line';
        btn.innerHTML = '<i class="' + icon + '"></i> ' + label + (n ? ' <span class="adv-count">' + n + '</span>' : '');
    }

    function draw() {
        var list = filtered();
        var visCols = effectiveCols();
        var tbody = document.querySelector('#cvtbl tbody');
        var tfoot = document.querySelector('#cvtbl tfoot');
        document.getElementById('f-search-clear').style.display = val('f-search') ? 'inline-flex' : 'none';
        document.getElementById('cv-subtitle').textContent = (val('f-template') === 'fx' ? 'Mẫu ngoại tệ' : 'Mẫu chuẩn') +
            ' · Nhóm theo Mã phí · mỗi nghiệp vụ hiện 2 vế (Nợ/Có) · Đơn vị tính: VNĐ';
        var sig = filterSignature();
        if (!list.length) {
            tbody.innerHTML = '<tr><td colspan="' + visCols.length + '"><div class="empty-state"><div class="es-icon"><i class="ri-inbox-2-line"></i></div>Không có chứng từ mã phí phù hợp bộ lọc.</div></td></tr>';
            tfoot.innerHTML = ''; document.getElementById('cvtbl-summary').innerHTML = '';
            pager.paginate([], sig); pager.render(); updateAdvBadge(); return;
        }
        /* Tổng cộng toàn báo cáo (trên TOÀN BỘ list lọc) */
        var gN = 0, gC = 0; list.forEach(function (r) { gN += r[JR.debit]; gC += r[JR.credit]; });
        var nDocs = countDocs(list), nCodes = new Set(list.map(function (r) { return r[JR.item]; })).size;
        var grandRow = amountRowHTML(visCols, 'TỔNG CỘNG — ' + nDocs + ' chứng từ · ' + nCodes + ' mã phí', gN, gC, 'row-total');

        /* Flat display items: [group header, ...rows] cho từng nhóm; phân trang trên mảng này */
        var groups = buildGroups(list);
        var items = [];
        groups.forEach(function (g) {
            items.push({ t: 'gh', g: g });
            g.rows.forEach(function (r) { items.push({ t: 'd', r: r }); });
        });
        var pageItems = pager.paginate(items, sig);
        tbody.innerHTML = grandRow + pageItems.map(function (it) {
            if (it.t === 'gh') {
                var g = it.g;
                var label = '<i class="ri-price-tag-3-line" style="color:#7c3aed"></i> <b>' + g.code + '</b> — ' + costCodeName(g.code) +
                    ' <span class="tp-small-text">(' + g.count + ' chứng từ)</span>';
                return amountRowHTML(visCols, label, g.totN, g.totC, 'row-group');
            }
            return '<tr>' + visCols.map(function (c) { return cellHTML(it.r, c); }).join('') + '</tr>';
        }).join('');
        tfoot.innerHTML = grandRow;

        document.getElementById('cvtbl-summary').innerHTML =
            '<span class="tp-small-text">Đối chiếu: mỗi nghiệp vụ hiện đủ 2 vế → Tổng PS Nợ = Tổng PS Có = ' + fmtMoney(gN) + '</span> ' +
            '<span class="status-pill ' + (gN === gC ? 'st-done' : 'st-paused') + '"><i class="ri-checkbox-circle-line"></i>' + (gN === gC ? 'CÂN ĐỐI' : 'LỆCH') + '</span>';
        updateAdvBadge();
        applyStickyTotals('#cvtbl');
        pager.render();
    }

    /* ----- Sự kiện lọc ----- */
    document.getElementById('f-toggle').addEventListener('click', function () {
        collapsed = !collapsed;
        document.getElementById('adv-filters').classList.toggle('collapsed', collapsed);
        updateAdvBadge();
    });
    setupFilterHide({ storageKey: 'demo-filter-costvouchers-hidden', btnId: 'f-hide', bodyId: 'filter-body' });
    document.querySelectorAll('.f-adv').forEach(function (el) { el.addEventListener('change', draw); });
    document.getElementById('f-template').addEventListener('change', function () { renderHeader(); draw(); });
    document.getElementById('f-search').addEventListener('keydown', function (e) { if (e.key === 'Enter') draw(); });
    document.getElementById('f-search').addEventListener('input', function () {
        document.getElementById('f-search-clear').style.display = this.value ? 'inline-flex' : 'none';
    });
    document.getElementById('f-search-clear').addEventListener('click', function () { document.getElementById('f-search').value = ''; draw(); });
    document.getElementById('f-go').addEventListener('click', draw);
    document.getElementById('f-clear').addEventListener('click', function () {
        ['f-search', 'f-item', 'f-side', 'f-account', 'f-contra', 'f-company'].forEach(function (id) { document.getElementById(id).value = ''; });
        document.getElementById('f-template').value = 'std';
        document.getElementById('f-period').value = 'y';
        document.getElementById('f-from').value = PERIODS.y[0];
        document.getElementById('f-to').value = PERIODS.y[1];
        draw();
    });
    document.getElementById('btn-excel').addEventListener('click', function () {
        toast('Demo: file Excel sẽ được tải xuống ở bản chính thức', 'info');
    });

    /* Cài đặt bộ lọc: mặc định = trường bắt buộc (Kỳ/Từ/Đến) */
    setupFilterSettings({
        storageKey: 'demo-filter-costvouchers',
        gearBtnId: 'ff-gear', defaultWrap: 'ff-default', advWrap: 'ff-adv',
        fields: [
            { id: 'f-period', label: 'Kỳ báo cáo', locked: true },
            { id: 'f-from', label: 'Từ ngày', locked: true },
            { id: 'f-to', label: 'Đến ngày', locked: true },
            { id: 'f-item', label: 'Mã phí' },
            { id: 'f-side', label: 'Ghi nợ/có' },
            { id: 'f-account', label: 'Tài khoản' },
            { id: 'f-contra', label: 'TK đối ứng' },
            { id: 'f-company', label: 'Đơn vị' },
            { id: 'f-template', label: 'Mẫu báo cáo' },
        ],
    });

    /* ----- In bảng kê (bố cục theo bản in Excel mẫu) ----- */
    function printSheetHTML() {
        var list = filtered();
        var company = val('f-company');
        var groups = buildGroups(list);
        var gN = 0, gC = 0;
        var body = groups.map(function (g) {
            var head = '<tr class="p-group"><td colspan="5"><b>' + g.code + ' — ' + costCodeName(g.code) + '</b></td>' +
                '<td class="pr"><b>' + fmtMoney(g.totN) + '</b></td><td class="pr"><b>' + fmtMoney(g.totC) + '</b></td></tr>';
            var rows = g.rows.map(function (r) {
                gN += r[JR.debit]; gC += r[JR.credit];
                return '<tr><td class="pc">' + fmtDate(r[JR.docDate]) + '</td>' +
                    '<td class="pc">' + cvDocType(r[JR.docNo]) + '</td>' +
                    '<td class="pc">' + r[JR.docNo] + '</td>' +
                    '<td>' + r[JR.desc] + '</td>' +
                    '<td class="pc">' + r[JR.account] + '</td>' +
                    '<td class="pc">' + cvContra(r) + '</td>' +
                    '<td class="pr">' + (r[JR.debit] ? fmtMoney(r[JR.debit]) : '') + '</td>' +
                    '<td class="pr">' + (r[JR.credit] ? fmtMoney(r[JR.credit]) : '') + '</td></tr>';
            }).join('');
            return head + rows;
        }).join('');
        return '<div class="print-sheet">' +
            '<table class="p-head"><tr>' +
            '<td style="width:60%"><b>Đơn vị:</b> ' + (company ? ORG[company].name : ORG['TPE'].name) + '<br><b>Địa chỉ:</b> ……………………………</td>' +
            '<td style="text-align:center"><i style="font-size:10.5px">Bảng kê chứng từ theo mã phí</i></td>' +
            '</tr></table>' +
            '<div class="p-title">BẢNG KÊ CHỨNG TỪ THEO MÃ PHÍ</div>' +
            '<div class="p-sub">Từ ngày ' + fmtDate(val('f-from')) + ' đến ngày ' + fmtDate(val('f-to')) + '</div>' +
            '<div class="p-unit">Đơn vị tính: VNĐ</div>' +
            '<table class="p-grid">' +
            '<thead><tr><th>Ngày ct</th><th>Mã ct</th><th>Số ct</th><th style="width:34%">Diễn giải</th><th>Tài khoản</th><th>Tk đối ứng</th><th>Phát sinh nợ</th><th>Phát sinh có</th></tr></thead>' +
            '<tbody>' + body +
            '<tr class="p-total"><td colspan="6" style="text-align:left"><b>Tổng cộng</b></td>' +
            '<td class="pr"><b>' + fmtMoney(gN) + '</b></td><td class="pr"><b>' + fmtMoney(gC) + '</b></td></tr>' +
            '</tbody></table>' +
            '<div class="p-note">- Bảng kê nhóm theo Mã phí; mỗi nghiệp vụ hiện đủ 2 vế (Nợ/Có) → Tổng phát sinh Nợ = Tổng phát sinh Có.<br>- Số liệu đối chiếu khớp Sổ nhật ký chung cùng kỳ.</div>' +
            '<table class="p-sign"><tr>' +
            '<td><b>Người lập</b><br><i>(Ký, họ tên)</i></td>' +
            '<td><b>Kế toán trưởng</b><br><i>(Ký, họ tên)</i></td>' +
            '<td><i>Ngày ... tháng ... năm ...</i><br><b>Giám đốc</b><br><i>(Ký, họ tên, đóng dấu)</i></td>' +
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

    renderHeader();
    draw();
}

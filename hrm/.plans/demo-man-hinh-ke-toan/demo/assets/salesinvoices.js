/* ============================================================
   Demo Kế toán HRM — BẢNG KÊ HÓA ĐƠN BÁN HÀNG, DỊCH VỤ
   Tham khảo báo cáo Fast Accounting Online rpt_sobk1t (07.20.02)
   — ảnh khảo sát: tham-khao/fast-bang-ke-hdbh-*.png
   - NGUỒN DỮ LIỆU (theo ERP): Phiếu XUẤT HÀNG (PXH — bán hàng hóa)
     + Phiếu HẠCH TOÁN DỊCH VỤ (DV — doanh thu dịch vụ). Mỗi dòng = 1 phiếu.
   - Cột theo mẫu chuẩn Fast: Ngày ct · Mã ct · Số ct · (Số xác thực) · Mã khách ·
     Tên khách · Tiền · Thuế · Chiết khấu · Phải thu · Diễn giải · Tài khoản ·
     NV bán hàng · Vụ việc — Phải thu = Tiền − Chiết khấu + Thuế
   - Các phiếu trùng nghiệp vụ với Sổ NKC có cột "Số CT NKC" link ?line= (tìm dòng động)
   - Dòng Tổng cộng ở ĐẦU bảng (sticky, giống Fast) + bản sao ở tfoot
   ============================================================ */

/* [loại ct, số ct, ngày ct, số xác thực, mã khách, diễn giải, tiền, thuế, chiết khấu,
    TK nợ, NV bán hàng, vụ việc, hợp đồng, số CT NKC, company, GD nội bộ] */
var SI_ROWS = [
    ['PXH', 'PXH-0001', '2026-01-10', 'FA26-000101', 'KH-Y', 'Xuất bán thiết bị nâng hạ TP-001', 100000000, 10000000, 0, '131', 'NV-005', 'VV-001', 'HĐ-B101', 'HD-101', 'TPE', 'N'],
    ['PXH', 'PXH-0002', '2026-01-12', 'FA26-000102', 'KH-JP', 'Xuất khẩu thiết bị cân chỉnh (thuế suất 0%)', 150000000, 0, 0, '131', 'NV-006', '', 'HĐ-EX01', '', 'TPE', 'N'],
    ['PXH', 'PXH-0003', '2026-01-15', 'FA26-000103', 'TPSG', 'Xuất bán hàng nội bộ tập đoàn TP-002', 200000000, 20000000, 0, '1368', 'NV-006', '', 'HĐ-IC01', 'HD-201', 'TPE', 'Y'],
    ['DV', 'DV-0001', '2026-01-18', 'FA26-000104', 'KH-D', 'Dịch vụ đào tạo nghiệp vụ (không chịu thuế GTGT)', 30000000, 0, 0, '131', 'NV-010', '', '', '', 'TPE', 'N'],
    ['PXH', 'PXH-0004', '2026-01-20', 'FA26-000105', 'KH-X', 'Xuất bán thành phẩm TP-001 (đợt 2)', 120000000, 12000000, 0, '131', 'NV-005', 'VV-001', 'HĐ-B115', 'HD-115', 'TPE', 'N'],
    ['DV', 'DV-0002', '2026-01-25', 'FA26-000106', 'KH-A', 'Cung cấp nước sạch phục vụ sản xuất (5%)', 40000000, 2000000, 0, '131', 'NV-006', '', '', '', 'TPE', 'N'],
    ['DV', 'DV-0003', '2026-01-28', 'FA26-000107', 'KH-B', 'Dịch vụ vận tải hàng hóa (8%)', 60000000, 4800000, 0, '131', 'NV-010', 'VV-001', '', '', 'TPE', 'N'],
    ['PXH', 'PXH-0005', '2026-02-05', 'FA26-000108', 'KH-Y', 'Xuất bán thành phẩm TP-001 (đơn tháng 2)', 150000000, 15000000, 0, '131', 'NV-005', 'VV-001', 'HĐ-B130', 'HD-130', 'TPE', 'N'],
    ['PXH', 'PXH-0006', '2026-02-08', 'FA26-000109', 'KH-C', 'Xuất bán thiết bị kiểm định khí thải (CK 10%)', 50000000, 4500000, 5000000, '131', 'NV-006', '', '', '', 'TPE', 'N'],
    ['DV', 'DV-0005', '2026-02-20', 'FA26-000110', 'KH-D', 'Dịch vụ bảo trì thiết bị định kỳ', 25000000, 2500000, 0, '131', 'NV-010', '', '', '', 'TPE', 'N'],
    ['PXH', 'PXH-0009', '2026-03-10', 'FA26-000111', 'KH-Y', 'Xuất bán thành phẩm TP-002 (đơn tháng 3)', 200000000, 20000000, 0, '131', 'NV-005', 'VV-001', 'HĐ-B150', 'HD-150', 'TPE', 'N'],
    ['PXH', 'PXH-B001', '2026-01-22', 'FB26-000201', 'KH-W', 'Xuất bán hàng hóa HH-005', 80000000, 8000000, 0, '131', 'NV-105', 'VV-B01', 'HĐ-B055', 'HD-B55', 'TPSG', 'N'],
    ['PXH', 'PXH-B002', '2026-02-08', 'FB26-000202', 'KH-W', 'Xuất bán hàng hóa HH-005 (đơn tháng 2)', 100000000, 10000000, 0, '131', 'NV-105', 'VV-B01', 'HĐ-B060', 'HD-B60', 'TPSG', 'N'],
    ['DV', 'DV-H001', '2026-02-12', 'FH26-000301', 'KH-H', 'Dịch vụ lắp đặt xưởng', 50000000, 5000000, 0, '131', 'NV-201', '', 'HĐ-B201', 'HD-H01', 'TPHP', 'N'],
];
var SI = { type: 0, no: 1, date: 2, verify: 3, buyer: 4, desc: 5, amount: 6, vat: 7, discount: 8, account: 9, emp: 10, job: 11, contract: 12, nkcDoc: 13, company: 14, internal: 15 };

var SI_TYPES = { 'PXH': 'Phiếu xuất hàng', 'DV': 'Phiếu hạch toán dịch vụ' };
/* Người mua ngoài danh mục chung (khách nước ngoài) */
var SI_EXTRA_NAMES = { 'KH-JP': 'Sakura Trading Co., Ltd (Nhật Bản)' };
function siBuyerName(code) { return objName(code) || SI_EXTRA_NAMES[code] || ''; }
/* Phải thu = Tiền − Chiết khấu + Thuế (theo Fast) */
function siReceivable(r) { return r[SI.amount] - r[SI.discount] + r[SI.vat]; }
/* Tìm STT dòng NKC theo Số CT (dòng ghi Nợ đầu tiên) — link chéo sang Sổ NKC */
function siNkcLine(docNo) {
    if (!docNo) return 0;
    var hit = JOURNAL_ROWS.find(function (r) { return r[JR.docNo] === docNo && r[JR.debit] > 0; });
    return hit ? hit[JR.line] : 0;
}

function renderSalesInvoicesPage() {
    function selOptions(list, labelFn) {
        return '<option value="">— Tất cả —</option>' + list.map(function (v) {
            return '<option value="' + v + '">' + (labelFn ? labelFn(v) : v) + '</option>';
        }).join('');
    }
    function uniq(fn) { return [...new Set(SI_ROWS.map(fn).filter(Boolean))].sort(); }

    renderShell('salesinv',
        /* ----- FILTER (theo dialog điều kiện lọc của Fast) ----- */
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="filter-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-filter-3-line"></i></div>' +
        '      <p class="tp-section-title">Bộ lọc Bảng kê hóa đơn bán hàng, dịch vụ</p>' +
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
        '      <input class="form-control form-control-sm" id="f-search" placeholder="Tìm theo Số ct, Số xác thực, Mã/Tên khách, Diễn giải">' +
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
        '      <div class="col-md-3" data-ff="f-company"><label class="tp-label">Đơn vị</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-company">' + selOptions(uniq(function (r) { return r[SI.company]; }), function (c) { return c + ' — ' + ORG[c].name; }) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-type"><label class="tp-label">Loại chứng từ</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-type">' + selOptions(Object.keys(SI_TYPES), function (k) { return k + ' — ' + SI_TYPES[k]; }) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-buyer"><label class="tp-label">Khách hàng</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-buyer">' + selOptions(uniq(function (r) { return r[SI.buyer]; }), function (c) { var n = siBuyerName(c); return n ? c + ' — ' + n : c; }) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-emp"><label class="tp-label">Nhân viên bán hàng</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-emp">' + selOptions(uniq(function (r) { return r[SI.emp]; }), function (e) { return e + ' — ' + (EMP_NAMES[e] || ''); }) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-account"><label class="tp-label">Tài khoản</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-account">' + selOptions(uniq(function (r) { return r[SI.account]; })) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-job"><label class="tp-label">Mã vụ việc</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-job">' + selOptions(uniq(function (r) { return r[SI.job]; }), jobLabel) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-contract"><label class="tp-label">Mã hợp đồng</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-contract">' + selOptions(uniq(function (r) { return r[SI.contract]; })) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-internal"><label class="tp-label">GD nội bộ</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-internal"><option value="">— Tất cả —</option><option value="Y">Y — Nội bộ tập đoàn</option><option value="N">N — Bên ngoài</option></select></div>' +
        '    </div>' +
        '  </div>' +
        '  </div>' +
        '</section>' +

        /* ----- BẢNG ----- */
        '<section class="tp-card p-3">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-bill-line"></i></div>' +
        '      <div><h5>Bảng kê hóa đơn bán hàng, dịch vụ</h5>' +
        '      <p class="tp-section-subtitle">Nguồn: Phiếu xuất hàng + Phiếu hạch toán dịch vụ (ERP) · Phải thu = Tiền − Chiết khấu + Thuế · Đơn vị tính: VNĐ</p></div>' +
        '    </div>' +
        '    <div class="table-actions">' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-print"><i class="ri-printer-line"></i> In bảng kê</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-excel"><i class="ri-file-excel-2-line"></i> Xuất Excel</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-cols" title="Chọn cột hiển thị trên bảng"><i class="ri-layout-column-line"></i> Cấu hình cột</button>' +
        '    </div>' +
        '  </div>' +
        '  <div class="table-wrapper scrollbar-thin"><table class="data-table" id="sitbl">' +
        '    <thead><tr id="sitbl-head"></tr></thead>' +
        '    <tbody></tbody><tfoot></tfoot>' +
        '  </table></div>' +
        '  <div class="table-pager" id="sitbl-pager"></div>' +
        '  <div class="d-flex align-center gap-2 mt-2" id="sitbl-summary"></div>' +
        '</section>' +

        /* ----- Modal In ----- */
        '<div class="modal-backdrop-demo" id="print-modal"><div class="modal-dialog" style="max-width:1000px">' +
        '  <div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-printer-line"></i></span>In Bảng kê hóa đơn bán hàng, dịch vụ</h5>' +
        '  <button type="button" class="close" onclick="closeModal(\'print-modal\')">×</button></div>' +
        '  <div class="modal-body" id="print-preview" style="max-height:70vh"></div>' +
        '  <div class="modal-footer">' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-do-print"><i class="ri-printer-line"></i> In</button>' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'print-modal\')"><i class="ri-close-line"></i> Đóng</button>' +
        '  </div>' +
        '</div></div>' +
        '<div id="print-area"></div>');

    /* ----- Kỳ báo cáo → khoảng ngày (dùng PERIODS của journal.js) ----- */
    document.getElementById('f-period').addEventListener('change', function () {
        var range = PERIODS[this.value];
        if (range) {
            document.getElementById('f-from').value = range[0];
            document.getElementById('f-to').value = range[1];
        }
        draw();
    });
    ['f-from', 'f-to'].forEach(function (id) {
        document.getElementById(id).addEventListener('change', function () {
            document.getElementById('f-period').value = 'custom';
            draw();
        });
    });

    /* ----- Lọc ----- */
    function val(id) { return document.getElementById(id).value; }
    function filtered() {
        var kw = val('f-search').toLowerCase().trim();
        return SI_ROWS.filter(function (r) {
            if (val('f-from') && r[SI.date] < val('f-from')) return false;
            if (val('f-to') && r[SI.date] > val('f-to')) return false;
            if (val('f-company') && r[SI.company] !== val('f-company')) return false;
            if (val('f-type') && r[SI.type] !== val('f-type')) return false;
            if (val('f-buyer') && r[SI.buyer] !== val('f-buyer')) return false;
            if (val('f-emp') && r[SI.emp] !== val('f-emp')) return false;
            if (val('f-account') && r[SI.account] !== val('f-account')) return false;
            if (val('f-job') && r[SI.job] !== val('f-job')) return false;
            if (val('f-contract') && r[SI.contract] !== val('f-contract')) return false;
            if (val('f-internal') && r[SI.internal] !== val('f-internal')) return false;
            if (kw && (r[SI.no] + ' ' + r[SI.verify] + ' ' + r[SI.buyer] + ' ' + siBuyerName(r[SI.buyer]) + ' ' + r[SI.desc]).toLowerCase().indexOf(kw) === -1) return false;
            return true;
        });
    }

    /* ----- Cột hiển thị: 9 cột chuẩn mẫu Fast khóa, cột mở rộng cấu hình được ----- */
    var COLUMNS = [
        { key: 'date', label: 'Ngày ct', always: true },
        { key: 'type', label: 'Mã ct', cls: 'text-center', always: true },
        { key: 'no', label: 'Số ct', cls: 'text-center', always: true },
        { key: 'buyer', label: 'Mã khách', always: true },
        { key: 'buyerName', label: 'Tên khách', style: 'min-width:200px', always: true },
        { key: 'amount', label: 'Tiền', cls: 'text-right', always: true },
        { key: 'vat', label: 'Thuế', cls: 'text-right', always: true },
        { key: 'discount', label: 'Chiết khấu', cls: 'text-right', always: true },
        { key: 'receivable', label: 'Phải thu', cls: 'text-right', always: true },
        { key: 'verify', label: 'Số xác thực', cls: 'text-center' },
        { key: 'desc', label: 'Diễn giải', style: 'min-width:230px' },
        { key: 'account', label: 'Tài khoản', cls: 'text-center' },
        { key: 'emp', label: 'NV bán hàng' },
        { key: 'job', label: 'Vụ việc', style: 'min-width:180px' },
        { key: 'contract', label: 'Hợp đồng' },
        { key: 'nkcDoc', label: 'Số CT NKC', cls: 'text-center' },
        { key: 'company', label: 'Đơn vị' },
        { key: 'internal', label: 'GD nội bộ', cls: 'text-center' },
    ];
    var colCfg = setupColumnConfig({
        storageKey: 'demo-salesinv-columns',
        btnId: 'btn-cols',
        columns: COLUMNS,
        fixedNote: '9 cột chuẩn của bảng kê (theo mẫu Fast) là <b>bắt buộc</b> và cố định ở đầu bảng.',
        onChange: function () { renderHeader(); draw(); },
    });

    /* ----- Sort theo cột (giá trị bằng nhau giữ thứ tự chuẩn theo ngày ct) ----- */
    var sortState = null;
    var SORT_NUMERIC = { amount: 1, vat: 1, discount: 1, receivable: 1 };
    function sortValue(item, key) {
        var r = item.r;
        switch (key) {
            case 'buyerName': return siBuyerName(r[SI.buyer]);
            case 'receivable': return siReceivable(r);
            default: return r[SI[key]];
        }
    }
    function applySort(wrapped) {
        if (!sortState) return wrapped;
        var key = sortState.key, asc = sortState.dir === 'asc' ? 1 : -1;
        return wrapped.slice().sort(function (a, b) {
            var x = sortValue(a, key), y = sortValue(b, key);
            if (SORT_NUMERIC[key]) return (x - y) * asc || a.stt - b.stt;
            if (x === y) return a.stt - b.stt;
            return (x < y ? -1 : 1) * asc;
        });
    }
    function renderHeader() {
        var visCols = colCfg.visible();
        document.getElementById('sitbl-head').innerHTML = visCols.map(function (c) {
            return '<th' + (c.cls ? ' class="' + c.cls + '"' : '') + (c.style ? ' style="' + c.style + '"' : '') + '>' + c.label + '</th>';
        }).join('');
        if (sortState && !visCols.some(function (c) { return c.key === sortState.key; })) sortState = null;
        setupColumnSort({
            tableSel: '#sitbl',
            headRow: 1,
            cols: visCols.map(function (c) { return { key: c.key }; }),
            onChange: function (s) { sortState = s; draw(); },
        });
    }

    function cellHTML(item, c) {
        var r = item.r;
        switch (c.key) {
            case 'date': return '<td class="num">' + fmtDate(r[SI.date]) + '</td>';
            case 'type': return '<td class="text-center"><span title="' + SI_TYPES[r[SI.type]] + '"><b>' + r[SI.type] + '</b></span></td>';
            case 'no': return '<td class="text-center"><span class="cell-title" style="font-size:12px">' + r[SI.no] + '</span></td>';
            case 'buyerName': return '<td style="white-space:normal">' + siBuyerName(r[SI.buyer]) + '</td>';
            case 'amount': return '<td class="text-right num">' + fmtMoney(r[SI.amount]) + '</td>';
            case 'vat': return '<td class="text-right num">' + (r[SI.vat] ? fmtMoney(r[SI.vat]) : '') + '</td>';
            case 'discount': return '<td class="text-right num">' + (r[SI.discount] ? fmtMoney(r[SI.discount]) : '') + '</td>';
            case 'receivable': return '<td class="text-right num" style="font-weight:700">' + fmtMoney(siReceivable(r)) + '</td>';
            case 'verify': return '<td class="text-center num">' + r[SI.verify] + '</td>';
            case 'desc': return '<td style="white-space:normal">' + r[SI.desc] + '</td>';
            case 'account': return '<td class="text-center"><b>' + r[SI.account] + '</b></td>';
            case 'emp': return '<td>' + (r[SI.emp] ? '<span title="' + (EMP_NAMES[r[SI.emp]] || '') + '">' + r[SI.emp] + '</span>' : '') + '</td>';
            case 'job': return '<td>' + jobLabel(r[SI.job]) + '</td>';
            case 'nkcDoc':
                if (!r[SI.nkcDoc]) return '<td class="text-center"></td>';
                var line = siNkcLine(r[SI.nkcDoc]);
                return '<td class="text-center">' + (line
                    ? '<a href="so-nhat-ky-chung.html?line=' + line + '" title="Mở Sổ NKC đúng dòng bút toán" style="color:#1d4ed8;font-weight:600">' + r[SI.nkcDoc] + '</a>'
                    : r[SI.nkcDoc]) + '</td>';
            case 'internal': return '<td class="text-center">' + (r[SI.internal] === 'Y' ? '<span class="status-pill st-paused">Y</span>' : '<span class="status-pill st-none">N</span>') + '</td>';
            default: return '<td>' + r[SI[c.key]] + '</td>'; // buyer, contract, company
        }
    }

    /* ----- Phân trang (helper chung) ----- */
    var pager = createPager({ storageKey: 'demo-salesinv-pagesize', containerSel: '#sitbl-pager', onChange: function () { draw(); } });
    function filterSignature() {
        return ['f-search', 'f-from', 'f-to', 'f-company', 'f-type', 'f-buyer', 'f-emp', 'f-account', 'f-job', 'f-contract', 'f-internal']
            .map(val).join('|') + '|' + JSON.stringify(sortState);
    }

    /* Badge đếm filter nâng cao */
    function updateAdvBadge() {
        var n = ['f-company', 'f-type', 'f-buyer', 'f-emp', 'f-account', 'f-job', 'f-contract', 'f-internal']
            .filter(function (id) { return String(val(id)).trim() !== ''; }).length;
        var btn = document.getElementById('f-toggle');
        var label = collapsed ? 'Tìm kiếm nâng cao' : 'Ẩn tìm kiếm nâng cao';
        var icon = collapsed ? 'ri-equalizer-line' : 'ri-arrow-up-s-line';
        btn.innerHTML = '<i class="' + icon + '"></i> ' + label + (n ? ' <span class="adv-count">' + n + '</span>' : '');
    }

    /* Dòng tổng render theo cột hiển thị → số luôn thẳng cột Tiền/Thuế/CK/Phải thu.
       Label chiếm 5 cột đầu (Ngày ct, Mã ct, Số ct, Mã khách, Tên khách — luôn hiện) */
    function totalRowHTML(visCols, label, t) {
        var html = '<tr class="row-total"><td colspan="5">' + label + '</td>';
        visCols.slice(5).forEach(function (c) {
            if (c.key === 'amount') html += '<td class="text-right num">' + fmtMoney(t.amount) + '</td>';
            else if (c.key === 'vat') html += '<td class="text-right num">' + fmtMoney(t.vat) + '</td>';
            else if (c.key === 'discount') html += '<td class="text-right num">' + fmtMoney(t.discount) + '</td>';
            else if (c.key === 'receivable') html += '<td class="text-right num">' + fmtMoney(t.amount - t.discount + t.vat) + '</td>';
            else html += '<td></td>';
        });
        return html + '</tr>';
    }

    function draw() {
        var list = filtered();
        var visCols = colCfg.visible();
        var tbody = document.querySelector('#sitbl tbody');
        var tfoot = document.querySelector('#sitbl tfoot');
        document.getElementById('f-search-clear').style.display = val('f-search') ? 'inline-flex' : 'none';
        var sig = filterSignature();
        if (!list.length) {
            tbody.innerHTML = '<tr><td colspan="' + visCols.length + '"><div class="empty-state"><div class="es-icon"><i class="ri-inbox-2-line"></i></div>Không có chứng từ phù hợp bộ lọc.</div></td></tr>';
            tfoot.innerHTML = '';
            document.getElementById('sitbl-summary').innerHTML = '';
            pager.paginate([], sig);
            pager.render();
            return;
        }
        /* Tổng cộng trên TOÀN BỘ danh sách lọc (như dòng "Tổng cộng" đầu bảng của Fast) */
        var tot = { amount: 0, vat: 0, discount: 0 };
        var nPxh = 0, nDv = 0;
        list.forEach(function (r) {
            tot.amount += r[SI.amount]; tot.vat += r[SI.vat]; tot.discount += r[SI.discount];
            if (r[SI.type] === 'PXH') nPxh++; else nDv++;
        });
        var totalRow = totalRowHTML(visCols, 'Tổng cộng — ' + list.length + ' chứng từ (' + nPxh + ' phiếu xuất hàng · ' + nDv + ' phiếu dịch vụ)', tot);

        /* STT không hiển thị nhưng dùng làm tie-break giữ thứ tự chuẩn theo ngày ct */
        var wrapped = list.map(function (r, i) { return { r: r, stt: i + 1 }; });
        var pageRows = pager.paginate(applySort(wrapped), sig);
        tbody.innerHTML = totalRow + pageRows.map(function (item) {
            return '<tr>' + visCols.map(function (c) { return cellHTML(item, c); }).join('') + '</tr>';
        }).join('');
        tfoot.innerHTML = totalRow;

        document.getElementById('sitbl-summary').innerHTML =
            '<span class="tp-small-text">Đối chiếu doanh thu: Tiền hàng + dịch vụ ' + fmtMoney(tot.amount) + ' · Thuế GTGT đầu ra ' + fmtMoney(tot.vat) + '</span> ' +
            '<span class="status-pill st-done"><i class="ri-checkbox-circle-line"></i>KHỚP SỔ NKC (TK 511 / 3331)</span>';
        updateAdvBadge();
        applyStickyTotals('#sitbl');
        pager.render();
    }

    /* filter auto-search */
    var collapsed = true;
    document.getElementById('f-toggle').addEventListener('click', function () {
        collapsed = !collapsed;
        document.getElementById('adv-filters').classList.toggle('collapsed', collapsed);
        updateAdvBadge();
    });
    setupFilterHide({ storageKey: 'demo-filter-salesinv-hidden', btnId: 'f-hide', bodyId: 'filter-body' });
    document.querySelectorAll('.f-adv').forEach(function (el) { el.addEventListener('change', draw); });
    document.getElementById('f-search').addEventListener('keydown', function (e) { if (e.key === 'Enter') draw(); });
    document.getElementById('f-search').addEventListener('input', function () {
        document.getElementById('f-search-clear').style.display = this.value ? 'inline-flex' : 'none';
    });
    document.getElementById('f-search-clear').addEventListener('click', function () {
        document.getElementById('f-search').value = ''; draw();
    });
    document.getElementById('f-go').addEventListener('click', draw);
    document.getElementById('f-clear').addEventListener('click', function () {
        ['f-search', 'f-company', 'f-type', 'f-buyer', 'f-emp', 'f-account', 'f-job', 'f-contract', 'f-internal'].forEach(function (id) { document.getElementById(id).value = ''; });
        document.getElementById('f-period').value = 'y';
        document.getElementById('f-from').value = PERIODS.y[0];
        document.getElementById('f-to').value = PERIODS.y[1];
        draw();
    });
    document.getElementById('btn-excel').addEventListener('click', function () {
        toast('Demo: file Excel sẽ được tải xuống ở bản chính thức', 'info');
    });

    /* Cài đặt bộ lọc (helper chung): mặc định = trường bắt buộc */
    setupFilterSettings({
        storageKey: 'demo-filter-salesinv',
        gearBtnId: 'ff-gear',
        defaultWrap: 'ff-default',
        advWrap: 'ff-adv',
        fields: [
            { id: 'f-period', label: 'Kỳ báo cáo', locked: true },
            { id: 'f-from', label: 'Từ ngày', locked: true },
            { id: 'f-to', label: 'Đến ngày', locked: true },
            { id: 'f-company', label: 'Đơn vị' },
            { id: 'f-type', label: 'Loại chứng từ' },
            { id: 'f-buyer', label: 'Khách hàng' },
            { id: 'f-emp', label: 'Nhân viên bán hàng' },
            { id: 'f-account', label: 'Tài khoản' },
            { id: 'f-job', label: 'Mã vụ việc' },
            { id: 'f-contract', label: 'Mã hợp đồng' },
            { id: 'f-internal', label: 'GD nội bộ' },
        ],
    });

    /* ----- In bảng kê (bố cục theo bản in Fast) ----- */
    function printSheetHTML() {
        var list = filtered();
        var company = val('f-company');
        var tot = { amount: 0, vat: 0, discount: 0 };
        var body = list.map(function (r, i) {
            tot.amount += r[SI.amount]; tot.vat += r[SI.vat]; tot.discount += r[SI.discount];
            return '<tr><td class="pc">' + (i + 1) + '</td>' +
                '<td class="pc">' + fmtDate(r[SI.date]) + '</td>' +
                '<td class="pc">' + r[SI.type] + '</td>' +
                '<td class="pc">' + r[SI.no] + '</td>' +
                '<td>' + siBuyerName(r[SI.buyer]) + '</td>' +
                '<td>' + r[SI.desc] + '</td>' +
                '<td class="pr">' + fmtMoney(r[SI.amount]) + '</td>' +
                '<td class="pr">' + (r[SI.vat] ? fmtMoney(r[SI.vat]) : '') + '</td>' +
                '<td class="pr">' + (r[SI.discount] ? fmtMoney(r[SI.discount]) : '') + '</td>' +
                '<td class="pr">' + fmtMoney(siReceivable(r)) + '</td></tr>';
        }).join('');
        return '<div class="print-sheet">' +
            '<table class="p-head"><tr>' +
            '<td style="width:55%"><b>Đơn vị:</b> ' + (company ? ORG[company].name : ORG['TPE'].name) + '<br><b>Địa chỉ:</b> ……………………………</td>' +
            '<td style="text-align:center"><i style="font-size:10.5px">Nguồn: Phiếu xuất hàng + Phiếu hạch toán dịch vụ (ERP)</i></td>' +
            '</tr></table>' +
            '<div class="p-title">BẢNG KÊ HÓA ĐƠN BÁN HÀNG, DỊCH VỤ</div>' +
            '<div class="p-sub">Từ ngày ' + fmtDate(val('f-from')) + ' đến ngày ' + fmtDate(val('f-to')) + '</div>' +
            '<div class="p-unit">Đơn vị tính: VNĐ</div>' +
            '<table class="p-grid">' +
            '<thead><tr><th>STT</th><th>Ngày ct</th><th>Mã ct</th><th>Số ct</th><th style="width:20%">Tên khách hàng</th><th style="width:20%">Diễn giải</th><th>Tiền</th><th>Thuế</th><th>Chiết khấu</th><th>Phải thu</th></tr></thead>' +
            '<tbody>' + body +
            '<tr class="p-total"><td colspan="6" style="text-align:left"><b>Tổng cộng</b></td>' +
            '<td class="pr"><b>' + fmtMoney(tot.amount) + '</b></td><td class="pr"><b>' + fmtMoney(tot.vat) + '</b></td>' +
            '<td class="pr"><b>' + fmtMoney(tot.discount) + '</b></td><td class="pr"><b>' + fmtMoney(tot.amount - tot.discount + tot.vat) + '</b></td></tr>' +
            '</tbody></table>' +
            '<div class="p-note">- Phải thu = Tiền − Chiết khấu + Thuế.<br>- Số liệu đối chiếu khớp Sổ nhật ký chung (TK 511, 3331) cùng kỳ.</div>' +
            '<table class="p-sign"><tr>' +
            '<td><b>Người lập biểu</b><br><i>(Ký, họ tên)</i></td>' +
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

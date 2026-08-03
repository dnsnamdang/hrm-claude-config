/* ============================================================
   Demo Kế toán HRM — Sổ nhật ký THU TIỀN (S03a1-DN) & CHI TIỀN (S03a2-DN)
   Nguồn cấu trúc: file Mau_So_Nhat_Ky_Thu_Chi_TT99_2025.xlsx (user cung cấp)
   - Nhật ký đặc biệt: 1 dòng = 1 nghiệp vụ (1 Nợ - nhiều Có / 1 Có - nhiều Nợ)
   - Cột TK đối ứng cột-hóa sẵn: Thu (Có 131/511/3331 + TK khác), Chi (Nợ 331/152-156/133/6xx + TK khác)
   - Cân đối ngang từng dòng: Số tiền = tổng các cột TK đối ứng
   - Đối chiếu dòng tiền: SDCK quỹ = SDĐK + Tổng Thu (S03a1) − Tổng Chi (S03a2)
   ============================================================ */

var CASH_ACCOUNTS = { '1111': 'Tiền mặt VNĐ', '1121': 'TGNH VNĐ', '1122': 'TGNH ngoại tệ' };
/* Số dư quỹ + TGNH đầu kỳ theo công ty (đối chiếu dòng tiền) */
var CASH_OPENING = { 'TPE': 850000000, 'TPSG': 420000000 };

/* THU: [date, docNo, docDate, desc, cashAcc, amount, c131, c511, c3331, otherAcc, otherAmt,
        company, dept, part, emp, item, object, contract, goods, currency, rate, internal] */
var CB_RECEIPTS = [
    ['2026-01-05', 'PT-01', '2026-01-05', 'Thu tiền bán hàng KH-A', '1111', 66000000, 0, 60000000, 6000000, '', 0, 'TPE', 'PB-KD', 'BP-KD01', 'NV-005', 'KM-DT', 'KH-A', 'HĐ-B001', 'TP-001', 'VND', 1, 'N'],
    ['2026-01-08', 'GBC-01', '2026-01-08', 'Thu tiền KH-B qua NH VCB', '1121', 220000000, 220000000, 0, 0, '', 0, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'KH-B', 'HĐ-B002', '', 'VND', 1, 'N'],
    ['2026-01-12', 'PT-02', '2026-01-12', 'Thu hoàn tạm ứng còn dư NV-005', '1111', 3000000, 0, 0, 0, '141', 3000000, 'TPE', 'PB-KT', 'BP-KT01', 'NV-005', '', 'NV-005', '', '', 'VND', 1, 'N'],
    ['2026-01-15', 'GBC-02', '2026-01-15', 'Thu lãi tiền gửi NH TCB', '1122', 2000000, 0, 0, 0, '515', 2000000, 'TPE', 'PB-KT', 'BP-KT01', 'NV-020', 'KM-DTTC', 'NH-TCB', '', '', 'VND', 1, 'N'],
    ['2026-01-20', 'PT-03', '2026-01-20', 'Thu tiền cho thuê VP tầng 3', '1111', 55000000, 0, 50000000, 5000000, '', 0, 'TPE', 'PB-KD', 'BP-KD02', 'NV-006', 'KM-DT', 'KH-D', 'HĐ-CT001', '', 'VND', 1, 'N'],
    ['2026-01-25', 'GBC-03', '2026-01-25', 'Thu thanh toán HĐ từ KH-C', '1121', 165000000, 165000000, 0, 0, '', 0, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'KH-C', 'HĐ-B003', '', 'VND', 1, 'N'],
    ['2026-01-28', 'GBC-04', '2026-01-28', 'Thu vốn góp bổ sung từ cổ đông', '1121', 500000000, 0, 0, 0, '411', 500000000, 'TPE', 'PB-KT', 'BP-KT01', 'NV-010', '', 'CĐ-01', '', '', 'VND', 1, 'N'],
    ['2026-01-30', 'GBC-05', '2026-01-30', 'Thu TPSG thanh toán công nợ nội bộ (HĐ-IC01)', '1121', 220000000, 0, 0, 0, '1368', 220000000, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'TPSG', 'HĐ-IC01', '', 'VND', 1, 'Y'],
    ['2026-01-24', 'PT-B01', '2026-01-24', 'Thu tiền bán hàng KH-W', '1111', 33000000, 0, 30000000, 3000000, '', 0, 'TPSG', 'PB-KD', 'BP-KD01', 'NV-105', 'KM-DT', 'KH-W', 'HĐ-B055', 'HH-005', 'VND', 1, 'N'],
];
/* CHI: [date, docNo, docDate, desc, cashAcc, amount, n331, n152156, n133, n6xx, otherAcc, otherAmt,
        company, dept, part, emp, item, object, contract, goods, currency, rate, internal] */
var CB_PAYMENTS = [
    ['2026-01-06', 'PC-01', '2026-01-06', 'Chi mua NVL trực tiếp NCC-X', '1111', 55000000, 0, 50000000, 5000000, 0, '', 0, 'TPE', 'PB-MUA', 'BP-MUA01', 'NV-001', 'KM-NVL', 'NCC-X', 'HĐ-M001', 'NVL-001', 'VND', 1, 'N'],
    ['2026-01-10', 'UNC-01', '2026-01-10', 'Chi trả NCC-Y qua NH', '1121', 88000000, 88000000, 0, 0, 0, '', 0, 'TPE', 'PB-KT', 'BP-KT02', 'NV-020', '', 'NCC-Y', 'HĐ-M002', '', 'VND', 1, 'N'],
    ['2026-01-15', 'PC-02', '2026-01-15', 'Tạm ứng công tác NV-010', '1111', 20000000, 0, 0, 0, 0, '141', 20000000, 'TPE', 'PB-KT', 'BP-KT01', 'NV-010', '', 'NV-010', '', '', 'VND', 1, 'N'],
    ['2026-01-20', 'UNC-02', '2026-01-20', 'Chi lương NV tháng 01/2026', '1121', 80000000, 0, 0, 0, 0, '334', 80000000, 'TPE', 'PB-HCNS', 'BP-HCNS01', 'NV-010', 'KM-LN', '', '', '', 'VND', 1, 'N'],
    ['2026-01-25', 'PC-03', '2026-01-25', 'Mua CCDC văn phòng', '1111', 8800000, 0, 0, 800000, 0, '153', 8000000, 'TPE', 'PB-HCNS', 'BP-HCNS01', 'NV-010', 'KM-CCDC', 'NCC-CCDC', 'HĐ-M003', 'CCDC-001', 'VND', 1, 'N'],
    ['2026-01-28', 'UNC-03', '2026-01-28', 'Chi phí điện thoại tháng 01', '1121', 3300000, 0, 0, 300000, 3000000, '', 0, 'TPE', 'PB-HCNS', 'BP-HCNS01', 'NV-010', 'KM-DVMN', 'NCC-VNPT', '', '', 'VND', 1, 'N'],
    ['2026-01-30', 'UNC-04', '2026-01-30', 'Trả nợ vay ngắn hạn NH VCB', '1121', 100000000, 0, 0, 0, 0, '341', 100000000, 'TPE', 'PB-KT', 'BP-KT01', 'NV-020', '', 'NH-VCB', '', '', 'VND', 1, 'N'],
    ['2026-01-30', 'UNC-B01', '2026-01-30', 'Chi trả công nợ nội bộ TPE (HĐ-IC01)', '1121', 220000000, 0, 0, 0, 0, '3368', 220000000, 'TPSG', 'PB-MUA', 'BP-MUA01', 'NV-101', '', 'TPE', 'HĐ-IC01', '', 'VND', 1, 'Y'],
    ['2026-01-26', 'PC-B01', '2026-01-26', 'Chi mua hàng hóa NCC-Z', '1111', 22000000, 0, 20000000, 2000000, 0, '', 0, 'TPSG', 'PB-MUA', 'BP-MUA01', 'NV-101', 'KM-HH', 'NCC-Z', 'HĐ-IM01', 'HH-005', 'VND', 1, 'N'],
];
var CB = { date: 0, docNo: 1, docDate: 2, desc: 3, cashAcc: 4, amount: 5 }; // 6.. cột đối ứng tùy sổ; đuôi chung:
function cbTail(r) { var n = r.length; return { company: r[n - 11], dept: r[n - 10], part: r[n - 9], emp: r[n - 8], item: r[n - 7], object: r[n - 6], contract: r[n - 5], goods: r[n - 4], currency: r[n - 3], rate: r[n - 2], internal: r[n - 1] }; }

function renderCashbookPage() {
    var MODE = { // cấu hình 2 sổ
        thu: {
            title: 'Sổ nhật ký thu tiền', form: 'S03a1-DN', rows: CB_RECEIPTS,
            cashLabel: 'Ghi Nợ TK (tiền)', side: 'Có', cols: [
                { key: 6, label: 'Có TK 131' }, { key: 7, label: 'Có TK 511' }, { key: 8, label: 'Có TK 3331' },
            ], otherAcc: 9, otherAmt: 10, docHint: 'PT, GBC',
            checkLabel: 'Số tiền = Tổng ghi Có các TK',
        },
        chi: {
            title: 'Sổ nhật ký chi tiền', form: 'S03a2-DN', rows: CB_PAYMENTS,
            cashLabel: 'Ghi Có TK (tiền)', side: 'Nợ', cols: [
                { key: 6, label: 'Nợ TK 331' }, { key: 7, label: 'Nợ TK 152, 156' }, { key: 8, label: 'Nợ TK 133' }, { key: 9, label: 'Nợ TK 6xx' },
            ], otherAcc: 10, otherAmt: 11, docHint: 'PC, UNC, GBN',
            checkLabel: 'Số tiền = Tổng ghi Nợ các TK',
        },
    };
    var active = 'thu';

    function selOptions(list, labelFn) {
        return '<option value="">— Tất cả —</option>' + list.map(function (v) {
            return '<option value="' + v + '">' + (labelFn ? labelFn(v) : v) + '</option>';
        }).join('');
    }
    function uniqBoth(fn) {
        var vals = CB_RECEIPTS.map(fn).concat(CB_PAYMENTS.map(fn));
        return [...new Set(vals.filter(Boolean))].sort();
    }

    renderShell('cashbook',
        /* ----- FILTER ----- */
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="filter-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-filter-3-line"></i></div>' +
        '      <p class="tp-section-title">Bộ lọc Nhật ký thu / chi tiền</p>' +
        '    </div>' +
        '    <div class="d-flex gap-2">' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="ff-gear"><i class="ri-settings-3-line"></i> Cài đặt bộ lọc</button>' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-toggle"><i class="ri-equalizer-line"></i> Tìm kiếm nâng cao</button>' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-hide" title="Ẩn / hiện toàn bộ khu vực bộ lọc"><i class="ri-eye-off-line"></i> Ẩn bộ lọc</button>' +
        '    </div>' +
        '  </div>' +
        '  <div id="filter-body">' +
        /* Ô tìm nhanh + nút Tìm kiếm / Nhập lại cùng hàng (pattern chuẩn journal.js) */
        '  <div class="quick-search-row">' +
        '    <div class="quick-search">' +
        '      <i class="ri-search-line"></i>' +
        '      <input class="form-control form-control-sm" id="f-search" placeholder="Tìm theo Số CT, Diễn giải, TK đối ứng">' +
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
        '          <optgroup label="Theo tháng">' + Array.from({ length: 12 }, function (_, i) { return '<option value="m' + (i + 1) + '"' + (i === 0 ? ' selected' : '') + '>Tháng ' + (i + 1) + '/2026</option>'; }).join('') + '</optgroup>' +
        '          <option value="custom">Tùy chọn...</option>' +
        '        </select></div>' +
        '      <div class="col-md-3" data-ff="f-from"><label class="tp-label">Từ ngày</label><input type="date" class="form-control form-control-sm" id="f-from" value="2026-01-01"></div>' +
        '      <div class="col-md-3" data-ff="f-to"><label class="tp-label">Đến ngày</label><input type="date" class="form-control form-control-sm" id="f-to" value="2026-01-31"></div>' +
        '      <div class="col-md-3" data-ff="f-company"><label class="tp-label">Công ty</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-company"><option value="">— Tất cả —</option>' +
                ['TPE', 'TPSG'].map(function (c) { return '<option value="' + c + '"' + (c === 'TPE' ? ' selected' : '') + '>' + c + ' — ' + ORG[c].name + '</option>'; }).join('') +
        '        </select></div>' +
        '      <div class="col-md-3" data-ff="f-cash"><label class="tp-label">TK tiền</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-cash">' + selOptions(Object.keys(CASH_ACCOUNTS), function (a) { return a + ' — ' + CASH_ACCOUNTS[a]; }) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-object"><label class="tp-label">Đối tượng</label><select class="form-control form-control-sm f-adv" id="f-object">' + selOptions(uniqBoth(function (r) { return cbTail(r).object; }), objOptLabel) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-item"><label class="tp-label">Mã phí</label><select class="form-control form-control-sm f-adv" id="f-item">' + selOptions(uniqBoth(function (r) { return cbTail(r).item; })) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-contract"><label class="tp-label">Hợp đồng</label><select class="form-control form-control-sm f-adv" id="f-contract">' + selOptions(uniqBoth(function (r) { return cbTail(r).contract; })) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-dept"><label class="tp-label">Phòng ban</label><select class="form-control form-control-sm f-adv" id="f-dept">' + selOptions(uniqBoth(function (r) { return cbTail(r).dept; })) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-internal"><label class="tp-label">GD nội bộ</label><select class="form-control form-control-sm f-adv" id="f-internal"><option value="">— Tất cả —</option><option value="Y">Y — Nội bộ tập đoàn</option><option value="N">N — Bên ngoài</option></select></div>' +
        '    </div>' +
        '  </div>' +
        '  </div>' + // đóng #filter-body
        '</section>' +

        /* ----- BẢNG (2 tab) ----- */
        '<section class="tp-card p-3">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-exchange-dollar-line"></i></div>' +
        '      <div><h5 id="cb-title">Sổ nhật ký thu tiền</h5>' +
        '      <p class="tp-section-subtitle" id="cb-sub">Mẫu S03a1-DN · Đơn vị tính: VNĐ</p></div>' +
        '    </div>' +
        '    <div class="table-actions">' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-print"><i class="ri-printer-line"></i> In sổ</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-excel"><i class="ri-file-excel-2-line"></i> Xuất Excel</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-cols" title="Chọn cột hiển thị trên bảng"><i class="ri-layout-column-line"></i> Cấu hình cột</button>' +
        '    </div>' +
        '  </div>' +
        '  <ul class="nav-tabs">' +
        '    <li><button type="button" class="nav-link active" data-cb="thu"><i class="ri-download-2-line"></i>Sổ NK thu tiền (S03a1-DN)</button></li>' +
        '    <li><button type="button" class="nav-link" data-cb="chi"><i class="ri-upload-2-line"></i>Sổ NK chi tiền (S03a2-DN)</button></li>' +
        '  </ul>' +
        '  <div class="note-box"><i class="ri-information-line"></i> Nhật ký đặc biệt: <b>1 dòng = 1 nghiệp vụ</b> (thu: 1 Nợ TK tiền – nhiều Có; chi: 1 Có TK tiền – nhiều Nợ), nghiệp vụ đã ghi ở đây <b>không ghi lại vào Sổ NKC</b>. Cân đối ngang: Số tiền = tổng các cột TK đối ứng.</div>' +
        '  <div class="table-wrapper scrollbar-thin"><table class="data-table" id="cbtbl"><thead></thead><tbody></tbody><tfoot></tfoot></table></div>' +
        '  <div class="table-pager" id="cbtbl-pager"></div>' +
        '  <div class="d-flex align-center gap-2 mt-2" id="cbtbl-summary"></div>' +
        '</section>' +

        /* ----- Modal In ----- */
        '<div class="modal-backdrop-demo" id="print-modal"><div class="modal-dialog" style="max-width:1000px">' +
        '  <div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-printer-line"></i></span><span id="print-title-label">In sổ</span></h5>' +
        '  <button type="button" class="close" onclick="closeModal(\'print-modal\')">×</button></div>' +
        '  <div class="modal-body" id="print-preview" style="max-height:70vh"></div>' +
        '  <div class="modal-footer">' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-do-print"><i class="ri-printer-line"></i> In</button>' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'print-modal\')"><i class="ri-close-line"></i> Đóng</button>' +
        '  </div>' +
        '</div></div>' +
        '<div id="print-area"></div>');

    function val(id) { return document.getElementById(id).value; }
    function match(r, m) {
        var t = cbTail(r);
        if (val('f-company') && t.company !== val('f-company')) return false;
        if (val('f-from') && r[CB.date] < val('f-from')) return false;
        if (val('f-to') && r[CB.date] > val('f-to')) return false;
        if (val('f-cash') && r[CB.cashAcc] !== val('f-cash')) return false;
        if (val('f-object') && t.object !== val('f-object')) return false;
        if (val('f-item') && t.item !== val('f-item')) return false;
        if (val('f-contract') && t.contract !== val('f-contract')) return false;
        if (val('f-dept') && t.dept !== val('f-dept')) return false;
        if (val('f-internal') && t.internal !== val('f-internal')) return false;
        var kw = val('f-search').toLowerCase().trim();
        if (kw) {
            var accs = m.cols.map(function (c) { return r[c.key] > 0 ? c.label : ''; }).join(' ') + ' ' + r[m.otherAcc];
            if ((r[CB.docNo] + ' ' + r[CB.desc] + ' ' + r[CB.cashAcc] + ' ' + accs).toLowerCase().indexOf(kw) === -1) return false;
        }
        return true;
    }
    function filtered(mode) {
        var m = MODE[mode];
        return m.rows.filter(function (r) { return match(r, m); })
            .sort(function (a, b) { return a[CB.date] < b[CB.date] ? -1 : 1; });
    }

    /* ----- Sort theo cột (click icon trên header) -----
       Không sort → thứ tự chuẩn của sổ (theo Ngày ghi sổ). Sort áp lên TOÀN BỘ
       danh sách lọc trước khi phân trang. Các dòng SDĐK / Cộng phát sinh / SDCK
       đối chiếu + pill CÂN ĐỐI + bản in mẫu S03a1/S03a2 KHÔNG theo sort. */
    var sortState = null;
    function applySort(list) {
        if (!sortState) return list;
        var m = MODE[active];
        var key = sortState.key, asc = sortState.dir === 'asc' ? 1 : -1;
        /* Giá trị so sánh theo key của cột:
           - 6 cột cố định → chỉ số trong CB (amount so sánh số)
           - cột TK đối ứng động → key = chỉ số cột trong m.cols (dạng chuỗi số) → so sánh số
           - TK khác: otherAcc (chuỗi số hiệu) / otherAmt (số tiền)
           - cột mở rộng → lấy qua cbTail(r) (rate so sánh số) */
        function sortVal(r) {
            if (CB.hasOwnProperty(key)) return r[CB[key]];
            if (/^\d+$/.test(key)) return r[parseInt(key, 10)];
            if (key === 'otherAcc') return r[m.otherAcc];
            if (key === 'otherAmt') return r[m.otherAmt];
            if (key === 'objectName') return objName(cbTail(r).object);
            return cbTail(r)[key];
        }
        var numeric = key === 'amount' || key === 'otherAmt' || key === 'rate' || /^\d+$/.test(key);
        /* Gắn chỉ số gốc để tie-break: giá trị bằng nhau giữ nguyên thứ tự chuẩn của sổ */
        return list.map(function (r, i) { return { r: r, i: i }; })
            .sort(function (a, b) {
                var x = sortVal(a.r), y = sortVal(b.r);
                if (numeric) return (x - y) * asc || a.i - b.i;
                if (x === y) return a.i - b.i;
                return (x < y ? -1 : 1) * asc;
            })
            .map(function (o) { return o.r; });
    }

    /* Đối chiếu dòng tiền (thay 4 thẻ tổng quan cũ — đưa vào bảng):
       tổng THU/CHI tính trên CẢ 2 sổ S03a1 + S03a2, không phụ thuộc tab đang mở */
    function cashReconRows(tailTd) {
        var thu = 0, chi = 0;
        filtered('thu').forEach(function (r) { thu += r[CB.amount]; });
        filtered('chi').forEach(function (r) { chi += r[CB.amount]; });
        var openTotal = 0;
        if (val('f-company')) openTotal = CASH_OPENING[val('f-company')] || 0;
        else Object.keys(CASH_OPENING).forEach(function (c) { openTotal += CASH_OPENING[c]; });
        var scope = val('f-company') || 'Toàn tập đoàn';
        return {
            open: '<tr class="row-carry"><td colspan="7"><i>Số dư quỹ + TGNH đầu kỳ — ' + scope + '</i></td>' +
                '<td class="text-right num"><i>' + fmtMoney(openTotal) + '</i></td>' + tailTd + '</tr>',
            close: '<tr class="row-carry"><td colspan="7"><i>Số dư cuối kỳ đối chiếu quỹ + TGNH = SDĐK + Tổng thu (' + fmtMoney(thu) + ') − Tổng chi (' + fmtMoney(chi) + ')</i></td>' +
                '<td class="text-right num"><i>' + fmtMoney(openTotal + thu - chi) + '</i></td>' + tailTd + '</tr>',
        };
    }

    /* Ô dữ liệu cho cột MỞ RỘNG (tổ chức + chiều phân tích) — theo cấu hình cột */
    function extCellHTML(t, c) {
        switch (c.key) {
            case 'emp': return '<td>' + (t.emp ? '<span title="' + (EMP_NAMES[t.emp] || '') + '">' + t.emp + '</span>' : '') + '</td>';
            case 'currency': return '<td class="text-center">' + t.currency + '</td>';
            case 'rate': return '<td class="text-right num">' + fmtMoney(t.rate) + '</td>';
            case 'internal': return '<td class="text-center">' + (t.internal === 'Y' ? '<span class="status-pill st-paused">Y</span>' : '<span class="status-pill st-none">N</span>') + '</td>';
            default: return '<td>' + t[c.key] + '</td>'; // company, dept, part, item, object, contract, goods
        }
    }

    /* ----- Render THEAD + gắn icon sort — TÁCH KHỎI draw() -----
       Thead chỉ phụ thuộc TAB đang mở + CẤU HÌNH CỘT (không phụ thuộc dữ liệu)
       → chỉ gọi khi: lần đầu vào màn, đổi tab, đổi cấu hình cột. Nhờ vậy mỗi lần
       draw() (đổi trang / gõ lọc / click sort) icon sort KHÔNG bị vẽ lại từ đầu,
       trạng thái active của icon (state nội bộ setupColumnSort) luôn khớp sortState. */
    function renderHead() {
        var m = MODE[active];
        var extCols = colCfg.visible();
        /* Header 1 HÀNG: cột chuẩn mẫu S03a1/S03a2 (đổi động theo tab) + cột mở rộng theo cấu hình.
           Tên cột TK đối ứng đã mang đủ ngữ nghĩa Ghi Nợ/Ghi Có ("Có TK 131", "Nợ TK 331"...);
           cột "TK khác" ghép thêm chiều Nợ/Có của tab hiện tại. */
        document.querySelector('#cbtbl thead').innerHTML = '<tr>' +
            '<th>Ngày ghi sổ</th><th>Số CT</th><th>Ngày CT</th>' +
            '<th>Mã đối tượng</th><th style="min-width:170px">Tên đối tượng</th>' +
            '<th style="min-width:220px">Diễn giải</th>' +
            '<th class="text-center">' + m.cashLabel + '</th><th class="text-right">Số tiền</th>' +
            m.cols.map(function (c) { return '<th class="text-right">' + c.label + '</th>'; }).join('') +
            '<th class="text-center">' + m.side + ' TK khác<br>(số hiệu)</th><th class="text-right">' + m.side + ' TK khác<br>(số tiền)</th>' +
            extCols.map(function (c) { return '<th' + (c.cls ? ' class="' + c.cls + '"' : '') + '>' + c.label + '</th>'; }).join('') +
            '</tr>';
        /* Key ổn định cho từng th, theo ĐÚNG thứ tự: 6 cột cố định → key thật trong CB;
           cột TK đối ứng động → chính key (chỉ số) của m.cols, ép chuỗi để so khớp
           data-sort-key; TK khác → 'otherAcc'/'otherAmt'; cột mở rộng → key ext. */
        var sortCols = [
            { key: 'date' }, { key: 'docNo' }, { key: 'docDate' },
            { key: 'object' }, { key: 'objectName' },
            { key: 'desc' }, { key: 'cashAcc' }, { key: 'amount' },
        ].concat(m.cols.map(function (c) { return { key: String(c.key) }; }))
            .concat([{ key: 'otherAcc' }, { key: 'otherAmt' }])
            .concat(extCols.map(function (c) { return { key: c.key }; }));
        /* Đổi tab / ẩn cột đang sort → key không còn trong bộ cột mới → bỏ sort */
        if (sortState && !sortCols.some(function (c) { return c.key === sortState.key; })) sortState = null;
        setupColumnSort({
            tableSel: '#cbtbl',
            headRow: 1,
            cols: sortCols,
            onChange: function (s) { sortState = s; draw(); },
        });
    }

    function draw() {
        var m = MODE[active];
        var list = filtered(active);
        document.getElementById('cb-title').textContent = m.title + (val('f-company') ? ' — ' + val('f-company') : ' — Toàn tập đoàn');
        document.getElementById('cb-sub').textContent = 'Mẫu ' + m.form + ' (TT 99/2025/TT-BTC) · Chứng từ: ' + m.docHint + ' · Đơn vị tính: VNĐ';

        /* Thead đã render ở renderHead() — draw() chỉ vẽ tbody/tfoot */
        var nOpp = m.cols.length;
        var extCols = colCfg.visible();
        var fixedCount = 8 + nOpp + 2; // ngày, số CT, ngày CT, mã + tên đối tượng, diễn giải, TK tiền, số tiền + cột đối ứng + TK khác (số hiệu/số tiền)
        var colCount = fixedCount + extCols.length;

        /* Tổng + kiểm tra cân đối ngang: tính trên TOÀN BỘ danh sách lọc của tab (không phụ thuộc trang) */
        var tot = { amount: 0, other: 0 };
        var totCols = m.cols.map(function () { return 0; });
        var allBalanced = true;
        list.forEach(function (r) {
            m.cols.forEach(function (c, i) { totCols[i] += r[c.key]; });
            tot.amount += r[CB.amount]; tot.other += r[m.otherAmt];
            var oppSum = r[m.otherAmt];
            m.cols.forEach(function (c) { oppSum += r[c.key]; });
            if (oppSum !== r[CB.amount]) allBalanced = false;
        });
        var trailTd = extCols.length ? '<td colspan="' + extCols.length + '"></td>' : '';
        var totalRow = '<tr class="row-total"><td colspan="7">Cộng số phát sinh (' + list.length + ' nghiệp vụ)</td>' +
            '<td class="text-right num">' + fmtMoney(tot.amount) + '</td>' +
            totCols.map(function (v) { return '<td class="text-right num">' + fmtMoney(v) + '</td>'; }).join('') +
            '<td></td><td class="text-right num">' + fmtMoney(tot.other) + '</td>' + trailTd + '</tr>';

        /* CHỈ dòng dữ liệu phân trang; sort TOÀN BỘ danh sách lọc trước khi cắt trang.
           Đổi tab / bộ lọc / sort → signature đổi → tự về trang 1 */
        var pageRows = pager.paginate(applySort(list), filterSignature());
        var body = pageRows.map(function (r) {
            var t = cbTail(r);
            var oppSum = r[m.otherAmt];
            m.cols.forEach(function (c) { oppSum += r[c.key]; });
            var balanced = oppSum === r[CB.amount];
            return '<tr' + (balanced ? '' : ' style="background:#fef2f2"') + '>' +
                '<td class="num">' + fmtDate(r[CB.date]) + '</td>' +
                '<td><span class="cell-title" style="font-size:12px">' + r[CB.docNo] + '</span></td>' +
                '<td class="num">' + fmtDate(r[CB.docDate]) + '</td>' +
                '<td>' + t.object + '</td>' +
                '<td style="white-space:normal">' + objName(t.object) + '</td>' +
                '<td style="white-space:normal">' + r[CB.desc] + '</td>' +
                '<td class="text-center"><b>' + r[CB.cashAcc] + '</b></td>' +
                '<td class="text-right num" style="font-weight:700">' + fmtMoney(r[CB.amount]) + '</td>' +
                m.cols.map(function (c) { return '<td class="text-right num">' + (r[c.key] ? fmtMoney(r[c.key]) : '') + '</td>'; }).join('') +
                '<td class="text-center"><b>' + r[m.otherAcc] + '</b></td>' +
                '<td class="text-right num">' + (r[m.otherAmt] ? fmtMoney(r[m.otherAmt]) : '') + '</td>' +
                extCols.map(function (c) { return extCellHTML(t, c); }).join('') +
                '</tr>';
        }).join('');
        /* SDĐK + dòng tổng ở ĐẦU bảng (sticky); tfoot: bản sao dòng tổng + SDCK đối chiếu */
        var tailAfterAmount = '<td colspan="' + (nOpp + 2 + extCols.length) + '"></td>';
        var recon = cashReconRows(tailAfterAmount);
        document.querySelector('#cbtbl tbody').innerHTML = recon.open + totalRow + (list.length ? body
            : '<tr><td colspan="' + colCount + '"><div class="empty-state"><div class="es-icon"><i class="ri-inbox-2-line"></i></div>Không có nghiệp vụ ' + (active === 'thu' ? 'thu' : 'chi') + ' tiền trong kỳ.</div></td></tr>');
        document.querySelector('#cbtbl tfoot').innerHTML = totalRow + recon.close;
        applyStickyTotals('#cbtbl');
        pager.render();

        var sumOpp = totCols.reduce(function (a, b) { return a + b; }, 0) + tot.other;
        document.getElementById('cbtbl-summary').innerHTML =
            '<span class="tp-small-text">Kiểm tra: ' + m.checkLabel + ' → ' + fmtMoney(tot.amount) + ' = ' + fmtMoney(sumOpp) + '</span> ' +
            (allBalanced && tot.amount === sumOpp
                ? '<span class="status-pill st-done"><i class="ri-checkbox-circle-line"></i>CÂN ĐỐI</span>'
                : '<span class="status-pill st-cancel"><i class="ri-error-warning-line"></i>LỆCH</span>');
    }

    /* tabs thu/chi */
    document.querySelectorAll('[data-cb]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.querySelectorAll('[data-cb]').forEach(function (b) { b.classList.remove('active'); });
            btn.classList.add('active');
            active = btn.dataset.cb;
            renderHead(); // bộ cột đổi theo tab; sort trên key không còn tồn tại sẽ tự reset
            draw();
        });
    });

    /* filter events */
    var collapsed = true;
    document.getElementById('f-toggle').addEventListener('click', function () {
        collapsed = !collapsed;
        document.getElementById('adv-filters').classList.toggle('collapsed', collapsed);
        this.innerHTML = '<i class="' + (collapsed ? 'ri-equalizer-line' : 'ri-arrow-up-s-line') + '"></i> ' + (collapsed ? 'Tìm kiếm nâng cao' : 'Ẩn tìm kiếm nâng cao');
    });

    /* ẩn / hiện toàn bộ khu vực bộ lọc (helper chung, lưu trạng thái theo màn) */
    setupFilterHide({ storageKey: 'demo-filter-cashbook-hidden', btnId: 'f-hide', bodyId: 'filter-body' });
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
    document.querySelectorAll('.f-adv').forEach(function (el) { el.addEventListener('change', draw); });
    document.getElementById('f-search').addEventListener('keydown', function (e) { if (e.key === 'Enter') draw(); });
    document.getElementById('f-search').addEventListener('input', function () {
        document.getElementById('f-search-clear').style.display = this.value ? 'inline-flex' : 'none';
    });
    document.getElementById('f-search-clear').addEventListener('click', function () { document.getElementById('f-search').value = ''; draw(); });
    document.getElementById('f-go').addEventListener('click', draw);
    document.getElementById('f-clear').addEventListener('click', function () {
        ['f-search', 'f-cash', 'f-object', 'f-item', 'f-contract', 'f-dept', 'f-internal'].forEach(function (id) { document.getElementById(id).value = ''; });
        document.getElementById('f-company').value = 'TPE';
        document.getElementById('f-period').value = 'm1';
        document.getElementById('f-from').value = PERIODS.m1[0];
        document.getElementById('f-to').value = PERIODS.m1[1];
        draw();
    });
    document.getElementById('btn-excel').addEventListener('click', function () {
        toast('Demo: file Excel sẽ được tải xuống ở bản chính thức', 'info');
    });

    /* ----- In mẫu chuẩn S03a1/S03a2 ----- */
    function printSheetHTML() {
        var m = MODE[active];
        var list = filtered(active);
        var tot = { amount: 0, other: 0 };
        var totCols = m.cols.map(function () { return 0; });
        var body = list.map(function (r) {
            m.cols.forEach(function (c, i) { totCols[i] += r[c.key]; });
            tot.amount += r[CB.amount]; tot.other += r[m.otherAmt];
            return '<tr>' +
                '<td class="pc">' + fmtDate(r[CB.date]) + '</td>' +
                '<td class="pc">' + r[CB.docNo] + '</td>' +
                '<td class="pc">' + fmtDate(r[CB.docDate]) + '</td>' +
                '<td>' + r[CB.desc] + '</td>' +
                '<td class="pc">' + r[CB.cashAcc] + '</td>' +
                '<td class="pr">' + fmtMoney(r[CB.amount]) + '</td>' +
                m.cols.map(function (c) { return '<td class="pr">' + (r[c.key] ? fmtMoney(r[c.key]) : '') + '</td>'; }).join('') +
                '<td class="pc">' + r[m.otherAcc] + '</td>' +
                '<td class="pr">' + (r[m.otherAmt] ? fmtMoney(r[m.otherAmt]) : '') + '</td>' +
                '</tr>';
        }).join('');
        var company = val('f-company');
        return '<div class="print-sheet">' +
            '<table class="p-head"><tr>' +
            '<td style="width:55%"><b>Đơn vị:</b> ' + (company ? ORG[company].name : ORG['TPE'].name) + '<br><b>Địa chỉ:</b> ……………………………</td>' +
            '<td style="text-align:center"><b>Mẫu số ' + m.form.replace('-DN', ' - DN') + '</b><br><i style="font-size:10.5px">(Ban hành theo Thông tư số 99/2025/TT-BTC<br>ngày 17/10/2025 của Bộ Tài chính)</i></td>' +
            '</tr></table>' +
            '<div class="p-title">' + m.title.toUpperCase() + '</div>' +
            '<div class="p-sub">Năm: 2026' + (val('f-from') || val('f-to') ? ' (Từ ' + fmtDate(val('f-from')) + ' đến ' + fmtDate(val('f-to')) + ')' : '') + '</div>' +
            '<div class="p-unit">Đơn vị tính: VNĐ</div>' +
            '<table class="p-grid">' +
            '<thead><tr><th rowspan="2">Ngày, tháng<br>ghi sổ</th><th colspan="2">Chứng từ</th><th rowspan="2" style="width:22%">Diễn giải</th>' +
            '<th rowspan="2">' + (active === 'thu' ? 'Ghi Nợ<br>TK…' : 'Ghi Có<br>TK…') + '</th><th rowspan="2">Số tiền</th>' +
            '<th colspan="' + (m.cols.length + 2) + '">Ghi ' + m.side + ' các tài khoản</th></tr>' +
            '<tr><th>Số hiệu</th><th>Ngày, tháng</th>' +
            m.cols.map(function (c) { return '<th>' + c.label.replace('Có ', '').replace('Nợ ', '') + '</th>'; }).join('') +
            '<th>TK khác<br>(số hiệu)</th><th>TK khác<br>(số tiền)</th></tr>' +
            '</thead><tbody>' + body +
            '<tr class="p-total"><td colspan="5" style="text-align:left"><b>Cộng số phát sinh</b></td>' +
            '<td class="pr"><b>' + fmtMoney(tot.amount) + '</b></td>' +
            totCols.map(function (v) { return '<td class="pr"><b>' + fmtMoney(v) + '</b></td>'; }).join('') +
            '<td></td><td class="pr"><b>' + fmtMoney(tot.other) + '</b></td></tr>' +
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
        document.getElementById('print-title-label').textContent = 'In ' + MODE[active].title + ' — Mẫu số ' + MODE[active].form + ' (TT 99/2025/TT-BTC)';
        document.getElementById('print-preview').innerHTML = printSheetHTML();
        openModal('print-modal');
    });
    document.getElementById('btn-do-print').addEventListener('click', function () {
        document.getElementById('print-area').innerHTML = printSheetHTML();
        window.print();
    });

    /* Cài đặt bộ lọc — quy tắc "mặc định = bắt buộc": chỉ kỳ/ngày locked,
       mọi trường khác (kể cả Công ty/TK tiền) nằm ở "Tìm kiếm nâng cao" trừ khi user tự cấu hình */
    setupFilterSettings({
        storageKey: 'demo-filter-cashbook',
        gearBtnId: 'ff-gear',
        defaultWrap: 'ff-default',
        advWrap: 'ff-adv',
        fields: [
            { id: 'f-period', label: 'Kỳ báo cáo', locked: true },
            { id: 'f-from', label: 'Từ ngày', locked: true },
            { id: 'f-to', label: 'Đến ngày', locked: true },
            { id: 'grp-org', label: 'Công ty – Phòng ban', ids: ['f-company', 'f-dept'] },
            { id: 'f-cash', label: 'TK tiền' },
            { id: 'f-object', label: 'Đối tượng' },
            { id: 'f-item', label: 'Mã phí' },
            { id: 'f-contract', label: 'Hợp đồng' },
            { id: 'f-internal', label: 'GD nội bộ' },
        ],
    });

    /* ----- Cấu hình cột (helper chung) — cột chuẩn của mẫu đổi động theo tab nên
       KHÔNG đưa vào modal; chỉ các cột TĨNH tổ chức + chiều phân tích là cột mở rộng ----- */
    var EXT_COLUMNS = [
        { key: 'company', label: 'Công ty' },
        { key: 'dept', label: 'Phòng ban' },
        { key: 'part', label: 'Bộ phận' },
        { key: 'emp', label: 'Nhân viên' },
        { key: 'item', label: 'Mã phí' },
        { key: 'contract', label: 'Hợp đồng' },
        { key: 'currency', label: 'Loại tiền', cls: 'text-center' },
        { key: 'rate', label: 'Tỷ giá', cls: 'text-right' },
        { key: 'internal', label: 'GD nội bộ', cls: 'text-center' },
    ];
    var colCfg = setupColumnConfig({
        storageKey: 'demo-cashbook-columns',
        btnId: 'btn-cols',
        columns: EXT_COLUMNS, // không có cột always → modal chỉ hiện danh sách cột mở rộng
        counterStart: 0,
        fixedNote: 'Các cột chuẩn theo mẫu S03a1/S03a2 (ngày, chứng từ, diễn giải, các cột tài khoản đối ứng) là <b>bắt buộc</b>.',
        onChange: function () { renderHead(); draw(); }, // đổi cột → render lại thead; ẩn cột đang sort sẽ tự reset
    });

    /* ----- Phân trang (helper chung): chỉ dòng dữ liệu; tổng/thẻ đối chiếu tính trên toàn bộ danh sách lọc ----- */
    var pager = createPager({ storageKey: 'demo-cashbook-pagesize', containerSel: '#cbtbl-pager', onChange: draw });
    /* Signature gồm TAB đang mở + mọi giá trị lọc + sortState → đổi tab/bộ lọc/sort tự về trang 1 */
    function filterSignature() {
        return active + '|' + ['f-search', 'f-company', 'f-dept', 'f-from', 'f-to', 'f-cash',
            'f-object', 'f-item', 'f-contract', 'f-internal'].map(val).join('|') +
            '|' + JSON.stringify(sortState);
    }

    renderHead();
    draw();
}

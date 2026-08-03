/* ============================================================
   Demo Kế toán HRM — Bảng cân đối kế toán hợp nhất (B01-DN TT99/2025 + ERP đa pháp nhân)
   Nguồn cấu trúc: file Mau_Bang_Can_Doi_Ke_Toan_TT99_2025.xlsx (user cung cấp)
   - Cột: chỉ tiêu B01-DN + từng pháp nhân → Cộng dồn → Loại trừ NB → HỢP NHẤT → so sánh đầu năm
   - Chỉ tiêu nội bộ ⭐ (133, 213, 252, 316, 411) loại trừ khi hợp nhất
   - Kiểm tra cân đối: TỔNG TÀI SẢN (270) = TỔNG NGUỒN VỐN (440) ở TẤT CẢ các cột
   - Số liệu minh họa theo sheet VD, map 3 pháp nhân thật: TPE (mẹ) / TPSG (con) / TPHP (chi nhánh)
   ============================================================ */

var BS_COMPANIES = ['TPE', 'TPSG', 'TPHP'];
var BS_ROLES = { 'TPE': 'Công ty mẹ', 'TPSG': 'Công ty con (TPE nắm 100%)', 'TPHP': 'Chi nhánh trực thuộc TPE' };

/* [stt, label, code, tm, level, star, [TPE, TPSG, TPHP], elim, opening]
   level: 0=section, 1=A/B/C/D, 2=I/II, 3=chỉ tiêu, 4=chi tiết, 9=TỔNG CỘNG
   Đơn vị: TRIỆU ĐỒNG. Số liệu theo sheet "VD_BCĐKT có dữ liệu". */
var BS_ROWS = [
    ['', 'PHẦN TÀI SẢN', '', '', 0, false, null, 0, null],
    ['', 'A. TÀI SẢN NGẮN HẠN', '100', '', 1, false, [465000, 160000, 50000], -60000, 554500],
    ['', 'I. Tiền và các khoản tương đương tiền', '110', 'V.01', 2, false, [50000, 30000, 20000], 0, 90000],
    [1, '1. Tiền', '111', '', 3, false, [50000, 30000, 20000], 0, 90000],
    ['', 'III. Các khoản phải thu ngắn hạn', '130', 'V.03', 2, false, [260000, 50000, 30000], -60000, 250000],
    [2, '1. Phải thu ngắn hạn của khách hàng', '131', '', 3, false, [200000, 50000, 30000], 0, 250000],
    [3, '3. Phải thu nội bộ ngắn hạn', '133', '', 3, true, [60000, 0, 0], -60000, 0],
    ['', 'IV. Hàng tồn kho', '140', 'V.04', 2, false, [150000, 80000, 0], 0, 210000],
    [4, '1. Hàng tồn kho', '141', '', 3, false, [150000, 80000, 0], 0, 210000],
    ['', 'V. Tài sản ngắn hạn khác', '150', '', 2, false, [5000, 0, 0], 0, 4500],
    [5, '2. Thuế GTGT được khấu trừ', '152', '', 3, false, [5000, 0, 0], 0, 4500],
    ['', 'B. TÀI SẢN DÀI HẠN', '200', '', 1, false, [650000, 100000, 60000], -150000, 630000],
    ['', 'I. Các khoản phải thu dài hạn', '210', 'V.05', 2, false, [50000, 0, 0], -50000, 0],
    [6, '2. Vốn kinh doanh ở đơn vị trực thuộc', '213', '', 3, true, [50000, 0, 0], -50000, 0],
    ['', 'II. Tài sản cố định', '220', 'V.06', 2, false, [500000, 100000, 60000], 0, 630000],
    ['', '1. Tài sản cố định hữu hình', '221', '', 3, false, [500000, 100000, 60000], 0, 630000],
    [7, '- Nguyên giá', '222', '', 4, false, [800000, 150000, 80000], 0, 950000],
    [8, '- Giá trị hao mòn lũy kế (*)', '223', '', 4, false, [-300000, -50000, -20000], 0, -320000],
    ['', 'V. Đầu tư tài chính dài hạn', '250', 'V.07', 2, false, [100000, 0, 0], -100000, 0],
    [9, '1. Đầu tư vào công ty con', '252', '', 3, true, [100000, 0, 0], -100000, 0],
    ['', 'TỔNG CỘNG TÀI SẢN', '270', '', 9, false, [1115000, 260000, 110000], -210000, 1184500],
    ['', 'PHẦN NGUỒN VỐN', '', '', 0, false, null, 0, null],
    ['', 'C. NỢ PHẢI TRẢ', '300', '', 1, false, [230000, 110000, 30000], -60000, 303000],
    ['', 'I. Nợ ngắn hạn', '310', 'V.08', 2, false, [130000, 110000, 30000], -60000, 193000],
    [10, '1. Phải trả người bán ngắn hạn', '311', '', 3, false, [80000, 40000, 30000], 0, 140000],
    [11, '4. Phải trả người lao động', '314', '', 3, false, [20000, 0, 0], 0, 18000],
    [12, '6. Phải trả nội bộ ngắn hạn', '316', '', 3, true, [0, 60000, 0], -60000, 0],
    [13, '8. Vay và nợ thuê tài chính ngắn hạn', '320', '', 3, false, [30000, 10000, 0], 0, 35000],
    ['', 'II. Nợ dài hạn', '330', 'V.09', 2, false, [100000, 0, 0], 0, 110000],
    [14, '8. Vay và nợ thuê tài chính dài hạn', '338', '', 3, false, [100000, 0, 0], 0, 110000],
    ['', 'D. VỐN CHỦ SỞ HỮU', '400', '', 1, false, [885000, 150000, 80000], -150000, 881500],
    ['', 'I. Vốn chủ sở hữu', '410', 'V.10', 2, false, [885000, 150000, 80000], -150000, 881500],
    [15, '1. Vốn góp của chủ sở hữu', '411', '', 3, true, [700000, 100000, 50000], -150000, 700000],
    [16, '11. Lợi nhuận sau thuế chưa phân phối', '421', '', 3, false, [185000, 50000, 30000], 0, 181500],
    ['', 'TỔNG CỘNG NGUỒN VỐN', '440', '', 9, false, [1115000, 260000, 110000], -210000, 1184500],
];
var BR = { stt: 0, label: 1, code: 2, tm: 3, level: 4, star: 5, vals: 6, elim: 7, opening: 8 };

function bsSum(r) { return r[BR.vals] ? r[BR.vals].reduce(function (a, b) { return a + b; }, 0) : 0; }
function bsConsol(r) { return bsSum(r) + r[BR.elim]; }
function fmtMoneySigned(n) { return n < 0 ? '(' + fmtMoney(-n) + ')' : fmtMoney(n); }
function fmtPct(n) { return (n * 100).toFixed(1).replace('.', ',') + '%'; }

function renderBalancePage() {
    var collapsedRows = {}; // code cấp cha đang thu gọn

    renderShell('balance',
        /* ----- FILTER / TÙY CHỌN HIỂN THỊ ----- */
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="filter-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-filter-3-line"></i></div>' +
        '      <p class="tp-section-title">Tham số báo cáo</p>' +
        '    </div>' +
        '    <div class="d-flex gap-2">' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-hide" title="Ẩn / hiện khu vực tham số">' +
        '        <i class="ri-eye-off-line"></i> Ẩn bộ lọc</button>' +
        '    </div>' +
        '  </div>' +
        '  <div id="filter-body">' +
        '  <div class="form-row filter-grid">' +
        '    <div class="col-md-3"><label class="tp-label">Kỳ báo cáo</label>' +
        '      <select class="form-control form-control-sm" id="f-asof"><option value="2026-12-31">Tại ngày 31/12/2026</option></select></div>' +
        '    <div class="col-md-3"><label class="tp-label">Phạm vi</label>' +
        '      <select class="form-control form-control-sm" id="f-scope">' +
        '        <option value="group">Hợp nhất tập đoàn (3 pháp nhân)</option>' +
                BS_COMPANIES.map(function (c) { return '<option value="' + c + '">' + c + ' — ' + ORG[c].name + '</option>'; }).join('') +
        '      </select></div>' +
        '  </div>' +
        '  </div>' +
        '</section>' +

        /* ----- BẢNG ----- */
        '<section class="tp-card p-3">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-scales-3-line"></i></div>' +
        '      <div><h5 id="bs-title">Bảng cân đối kế toán hợp nhất</h5>' +
        '      <p class="tp-section-subtitle" id="bs-sub">Mẫu B01-DN (TT 99/2025/TT-BTC) · Tại ngày 31/12/2026 · Đơn vị tính: Triệu đồng</p></div>' +
        '    </div>' +
        '    <div class="table-actions">' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-print"><i class="ri-printer-line"></i> In báo cáo (mẫu B01-DN)</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-excel"><i class="ri-file-excel-2-line"></i> Xuất Excel</button>' +
        '    </div>' +
        '  </div>' +
        '  <div class="note-box" id="bs-note"><i class="ri-information-line"></i> Số liệu hợp nhất tập đoàn đã <b>loại trừ giao dịch nội bộ</b> giữa các pháp nhân (phải thu/phải trả nội bộ, vốn góp vào đơn vị trực thuộc...). Bấm vào dòng nhóm (A/B/C/D, I/II...) để thu gọn/mở rộng.</div>' +
        '  <div class="table-wrapper scrollbar-thin"><table class="data-table" id="btbl">' +
        '    <thead></thead><tbody></tbody>' +
        '  </table></div>' +
        '  <div class="d-flex align-center gap-2 mt-2" id="btbl-summary"></div>' +
        '</section>' +

        /* ----- Modal In ----- */
        '<div class="modal-backdrop-demo" id="print-modal"><div class="modal-dialog" style="max-width:880px">' +
        '  <div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-printer-line"></i></span>In Bảng cân đối kế toán — Mẫu số B01-DN (TT 99/2025/TT-BTC)</h5>' +
        '  <button type="button" class="close" onclick="closeModal(\'print-modal\')">×</button></div>' +
        '  <div class="modal-body" id="print-preview" style="max-height:70vh"></div>' +
        '  <div class="modal-footer">' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-do-print"><i class="ri-printer-line"></i> In</button>' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'print-modal\')"><i class="ri-close-line"></i> Đóng</button>' +
        '  </div>' +
        '</div></div>' +
        '<div id="print-area"></div>');

    function scope() { return document.getElementById('f-scope').value; }

    /* Dòng có phải con của dòng nhóm đang thu gọn? */
    function isHiddenByCollapse(idx) {
        var r = BS_ROWS[idx];
        for (var i = idx - 1; i >= 0; i--) {
            var p = BS_ROWS[i];
            if (p[BR.level] !== 0 && p[BR.level] !== 9 && p[BR.level] < r[BR.level]) {
                if (collapsedRows[p[BR.code]]) return true;
                if (p[BR.level] === 1) break;
            }
            if (p[BR.level] === 0) break;
        }
        return false;
    }
    function hasChildren(idx) {
        var r = BS_ROWS[idx];
        var nxt = BS_ROWS[idx + 1];
        return nxt && nxt[BR.level] > r[BR.level] && nxt[BR.level] !== 9;
    }

    function draw() {
        var sc = scope();
        var isGroup = sc === 'group';
        var ci = BS_COMPANIES.indexOf(sc); // index pháp nhân khi xem riêng
        function cur(r) { return isGroup ? bsConsol(r) : r[BR.vals][ci]; }

        document.getElementById('bs-title').textContent = isGroup
            ? 'Bảng cân đối kế toán hợp nhất — Tập đoàn Tân Phát'
            : 'Bảng cân đối kế toán — ' + sc + ' (' + BS_ROLES[sc] + ')';
        document.getElementById('bs-sub').textContent = 'Mẫu B01-DN (TT 99/2025/TT-BTC) · Tại ngày 31/12/2026 · Đơn vị tính: Triệu đồng';
        document.getElementById('bs-note').style.display = isGroup ? '' : 'none';

        /* ---- thead: đúng 5 cột mẫu chuẩn B01-DN ---- */
        document.querySelector('#btbl thead').innerHTML = '<tr>' +
            '<th style="min-width:320px">CHỈ TIÊU</th>' +
            '<th class="text-center" style="width:70px">Mã số</th>' +
            '<th class="text-center" style="width:90px">Thuyết minh</th>' +
            '<th class="text-right" style="width:150px">Số cuối năm</th>' +
            '<th class="text-right" style="width:150px">Số đầu năm</th>' +
            '</tr>';
        var colCount = 5;

        /* ---- tbody: Số cuối năm = hợp nhất (đã loại trừ GD nội bộ) hoặc số của pháp nhân đang xem ---- */
        var html = BS_ROWS.map(function (r, idx) {
            if (r[BR.level] === 0) {
                return '<tr class="bs-section"><td colspan="' + colCount + '">' + r[BR.label] + '</td></tr>';
            }
            if (isHiddenByCollapse(idx)) return '';
            var lv = r[BR.level];
            var cls = lv === 9 ? 'row-total' : lv === 1 ? 'bs-l1' : lv === 2 ? 'bs-l2' : '';
            var pad = lv === 3 ? 22 : lv === 4 ? 38 : lv === 2 ? 10 : 0;
            var caret = (lv === 1 || lv === 2) && hasChildren(idx)
                ? '<i class="' + (collapsedRows[r[BR.code]] ? 'ri-arrow-right-s-line' : 'ri-arrow-down-s-line') + '" style="vertical-align:-2px"></i> ' : '';
            function num(v) {
                return '<td class="text-right num"' + (v < 0 ? ' style="color:#b91c1c"' : '') + '>' + fmtMoneySigned(v) + '</td>';
            }
            return '<tr class="' + cls + (caret ? ' bs-toggle' : '') + '" data-code="' + r[BR.code] + '">' +
                '<td style="white-space:normal;padding-left:' + (8 + pad) + 'px">' + caret + r[BR.label] + '</td>' +
                '<td class="text-center"><b>' + r[BR.code] + '</b></td>' +
                '<td class="text-center">' + r[BR.tm] + '</td>' +
                num(cur(r)) +
                num(r[BR.opening] || 0) +
                '</tr>';
        }).join('');
        document.querySelector('#btbl tbody').innerHTML = html;

        /* thu gọn/mở rộng */
        document.querySelectorAll('#btbl tbody tr.bs-toggle').forEach(function (tr) {
            tr.addEventListener('click', function () {
                var code = tr.dataset.code;
                collapsedRows[code] = !collapsedRows[code];
                draw();
            });
        });

        /* ---- kiểm tra cân đối: Tổng TÀI SẢN (270) = Tổng NGUỒN VỐN (440) ---- */
        var ts = BS_ROWS.filter(function (r) { return r[BR.code] === '270'; })[0];
        var nv = BS_ROWS.filter(function (r) { return r[BR.code] === '440'; })[0];
        var checks = [
            ['Số cuối năm', cur(ts) === cur(nv)],
            ['Số đầu năm', ts[BR.opening] === nv[BR.opening]],
        ];
        document.getElementById('btbl-summary').innerHTML =
            '<span class="tp-small-text">Kiểm tra cân đối (Tổng TÀI SẢN 270 = Tổng NGUỒN VỐN 440):</span> ' +
            checks.map(function (ch) {
                return '<span class="status-pill ' + (ch[1] ? 'st-done' : 'st-cancel') + '">' + (ch[1] ? '✓' : '✗') + ' ' + ch[0] + '</span>';
            }).join(' ');
    }

    document.getElementById('f-scope').addEventListener('change', draw);
    /* ẩn / hiện khu tham số báo cáo (helper chung, lưu theo màn) */
    setupFilterHide({ storageKey: 'demo-filter-balance-hidden', btnId: 'f-hide', bodyId: 'filter-body' });
    document.getElementById('btn-excel').addEventListener('click', function () {
        toast('Demo: file Excel sẽ được tải xuống ở bản chính thức', 'info');
    });

    /* ----- In mẫu chuẩn B01-DN ----- */
    function printSheetHTML() {
        var sc = scope();
        var isGroup = sc === 'group';
        var ci = BS_COMPANIES.indexOf(sc);
        var body = BS_ROWS.map(function (r) {
            if (r[BR.level] === 0) return '<tr><td colspan="5" style="font-weight:700;text-align:center">' + r[BR.label] + '</td></tr>';
            if (r[BR.level] === 4) return ''; // mẫu chuẩn không in dòng chi tiết "- Nguyên giá..."
            var bold = r[BR.level] <= 1 || r[BR.level] === 9;
            var current = isGroup ? bsConsol(r) : r[BR.vals][ci];
            return '<tr' + (r[BR.level] === 9 ? ' class="p-total"' : '') + '>' +
                '<td style="padding-left:' + (6 + (r[BR.level] >= 3 ? 22 : r[BR.level] === 2 ? 12 : 0)) + 'px">' + (bold ? '<b>' + r[BR.label] + '</b>' : r[BR.label]) + '</td>' +
                '<td class="pc">' + r[BR.code] + '</td>' +
                '<td class="pc">' + r[BR.tm] + '</td>' +
                '<td class="pr">' + (bold ? '<b>' + fmtMoneySigned(current) + '</b>' : fmtMoneySigned(current)) + '</td>' +
                '<td class="pr">' + (bold ? '<b>' + fmtMoneySigned(r[BR.opening] || 0) + '</b>' : fmtMoneySigned(r[BR.opening] || 0)) + '</td>' +
                '</tr>';
        }).join('');
        return '<div class="print-sheet">' +
            '<table class="p-head"><tr>' +
            '<td style="width:55%"><b>Đơn vị:</b> ' + (isGroup ? 'TẬP ĐOÀN TÂN PHÁT (hợp nhất TPE, TPSG, TPHP)' : ORG[sc].name) + '<br><b>Địa chỉ:</b> ……………………………</td>' +
            '<td style="text-align:center"><b>Mẫu số B01 - DN</b><br><i style="font-size:10.5px">(Ban hành theo Thông tư số 99/2025/TT-BTC<br>ngày 17/10/2025 của Bộ Tài chính)</i></td>' +
            '</tr></table>' +
            '<div class="p-title">BẢNG CÂN ĐỐI KẾ TOÁN' + (isGroup ? ' HỢP NHẤT' : '') + '</div>' +
            '<div class="p-sub">Tại ngày 31 tháng 12 năm 2026</div>' +
            '<div class="p-unit">Đơn vị tính: Triệu đồng</div>' +
            '<table class="p-grid">' +
            '<thead><tr><th style="width:44%">CHỈ TIÊU</th><th>Mã số</th><th>Thuyết<br>minh</th><th>Số cuối năm</th><th>Số đầu năm</th></tr>' +
            '<tr class="p-abc"><th>A</th><th>B</th><th>C</th><th>1</th><th>2</th></tr></thead>' +
            '<tbody>' + body + '</tbody></table>' +
            '<table class="p-sign"><tr>' +
            '<td><b>Người lập biểu</b><br><i>(Ký, họ tên)</i></td>' +
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

    draw();
}

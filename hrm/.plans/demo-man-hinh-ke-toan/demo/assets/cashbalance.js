/* ============================================================
   Demo Kế toán HRM — Báo cáo số dư tại quỹ và các ngân hàng
   Nguồn cấu trúc: file Mau_BC_So_Du_Tien.xlsx (user cung cấp)
   - BÁO CÁO QUẢN TRỊ NỘI BỘ (không thuộc bộ BCTC theo TT99/2025)
   - Chi tiết theo TK tiền × pháp nhân × nguyên tệ; SDCK = SDĐK + PS Nợ − PS Có
   - Quy VND theo hệ số tỷ giá (VND=1, USD=0.025 tương đương 25.000 VND/USD, đơn vị triệu)
   - Tab Tổng hợp (pivot pháp nhân × loại TK, theo loại tiền, nhận xét) + Tab Đối chiếu SC vs Sao kê NH
   - Quy tắc kiểm soát: quỹ TM > 100tr → cảnh báo vượt hạn mức tồn quỹ nội bộ (chi tiền mặt ≥ 5tr
     cho HHDV không được khấu trừ VAT theo Luật 48/2024/QH15 + NĐ 181/2025); số dư âm → lỗi nghiêm trọng
   ============================================================ */

/* Đơn vị: TRIỆU ĐỒNG (nguyên tệ theo loại tiền).
   [company, type, place, bankAccNo, glAcc, ccy, rate, sdkNT, psNo, psCo, note] */
var CBAL_ROWS = [
    ['TPE', 'Quỹ tiền mặt', 'Trụ sở chính HN', '', '1111', 'VND', 1, 25, 1000, 995, ''],
    ['TPE', 'Quỹ tiền mặt', 'Trụ sở chính HN', '', '1112', 'USD', 0.025, 4000, 1500, 500, 'Ngoại tệ quỹ — hệ số 0.025 = 25.000 VND/USD'],
    ['TPE', 'Tiền gửi NH', 'Vietcombank - CN Hà Nội', '0011.0000.12345678', '1121-VCB', 'VND', 1, 80000, 350000, 330000, 'TK hoạt động chính'],
    ['TPE', 'Tiền gửi NH', 'BIDV - CN Hà Nội', '3100.0000.87654321', '1121-BIDV', 'VND', 1, 45000, 80000, 75000, 'TK phụ'],
    ['TPE', 'Tiền gửi NH', 'Techcombank - CN Hà Nội', '1900.5555.66666', '1121-TCB', 'VND', 1, 18000, 25000, 23000, 'TK phụ'],
    ['TPE', 'Tiền gửi NH', 'Vietcombank - CN Hà Nội', '0011.9999.12345', '1122-VCB', 'USD', 0.025, 150000, 100000, 50000, 'TK ngoại tệ NH — hệ số 0.025'],
    ['TPE', 'Tiền gửi kỳ hạn', 'Vietcombank - CN Hà Nội', '0011.7777.KH-6M', '1281-VCB', 'VND', 1, 30000, 0, 0, 'Kỳ hạn 6 tháng, đáo hạn 15/03'],
    ['TPSG', 'Quỹ tiền mặt', 'Trụ sở TPSG', '', '1111', 'VND', 1, 12, 200, 197, ''],
    ['TPSG', 'Tiền gửi NH', 'VPBank - CN HCM', '2200.0000.99999', '1121-VPB', 'VND', 1, 20000, 15000, 10000, ''],
    ['TPSG', 'Tiền gửi NH', 'ACB - CN HCM', '2000.1111.88888', '1121-ACB', 'VND', 1, 8000, 2000, 5000, ''],
    ['TPHP', 'Quỹ tiền mặt', 'Trụ sở TPHP', '', '1111', 'VND', 1, 6, 150, 148, ''],
    ['TPHP', 'Tiền gửi NH', 'Sacombank - CN Đà Nẵng', '0200.3333.77777', '1121-STB', 'VND', 1, 10000, 8000, 3000, ''],
    ['TPHP', 'Tiền gửi NH', 'ACB - CN Đà Nẵng', '2000.4444.55555', '1121-ACB', 'VND', 1, 6000, 1000, 2000, ''],
];
var CL = { company: 0, type: 1, place: 2, bankNo: 3, gl: 4, ccy: 5, rate: 6, sdk: 7, no: 8, co: 9, note: 10 };
function clSdck(r) { return r[CL.sdk] + r[CL.no] - r[CL.co]; }
function clSdckVnd(r) { return clSdck(r) * r[CL.rate]; }
function clSdkVnd(r) { return r[CL.sdk] * r[CL.rate]; }
function pctStr(x) { return (x * 100).toFixed(1).replace('.', ',') + '%'; }
/* TK kế toán hiển thị KHÔNG kèm mã ngân hàng ('1121-VCB' → '1121');
   mã NH đã có ở cột Ngân hàng / Số TK ngân hàng. Data + quick search giữ mã đầy đủ. */
function glCode(v) { return String(v).split('-')[0]; }

/* Đối chiếu Sổ Cái vs Sao kê NH: [company, glAcc, bank, sdSC, sdSaoKe, nguyên nhân & xử lý] */
var CBAL_RECON = [
    ['TPE', '1121-VCB', 'Vietcombank - CN Hà Nội', 100000, 100000, ''],
    ['TPE', '1121-BIDV', 'BIDV - CN Hà Nội', 50000, 49950, 'UNC đã ghi sổ trước, NH xử lý T+1 → chờ khớp tháng sau, KHÔNG cần điều chỉnh'],
    ['TPE', '1121-TCB', 'Techcombank - CN Hà Nội', 20000, 20000, ''],
    ['TPE', '1122-VCB', 'Vietcombank - USD', 5000, 5000, ''],
    ['TPE', '1281-VCB', 'Vietcombank - Kỳ hạn', 30000, 30000, ''],
    ['TPSG', '1121-VPB', 'VPBank - CN HCM', 25000, 25025, 'Lãi tiền gửi NH đã cộng nhưng chưa hạch toán → CẦN bổ sung bút toán ghi thu nhập (515)'],
    ['TPSG', '1121-ACB', 'ACB - CN HCM', 5000, 5000, ''],
    ['TPHP', '1121-STB', 'Sacombank - CN Đà Nẵng', 15000, 15000, ''],
    ['TPHP', '1121-ACB', 'ACB - CN Đà Nẵng', 5000, 5000, ''],
];

function renderCashBalancePage() {
    var activeTab = 'detail';

    function selOptions(list, labelFn) {
        return '<option value="">— Tất cả —</option>' + list.map(function (v) {
            return '<option value="' + v + '">' + (labelFn ? labelFn(v) : v) + '</option>';
        }).join('');
    }
    function uniq(fn) { return [...new Set(CBAL_ROWS.map(fn).filter(Boolean))].sort(); }
    function bankName(r) { return r[CL.type] === 'Quỹ tiền mặt' ? '' : r[CL.place].split(' - ')[0]; }

    renderShell('cashbalance',
        /* ----- FILTER ----- */
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="filter-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-filter-3-line"></i></div>' +
        '      <p class="tp-section-title">Bộ lọc Báo cáo số dư tiền</p>' +
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
        '      <input class="form-control form-control-sm" id="f-search" placeholder="Tìm theo TK kế toán, Số TK ngân hàng, Ngân hàng / Địa điểm quỹ">' +
        '      <button type="button" class="btn-clear-quick-search" id="f-search-clear"><i class="ri-close-line"></i></button>' +
        '    </div>' +
        '    <button type="button" class="v2-btn v2-btn--primary btn-compact" id="f-go"><i class="ri-search-line"></i> Tìm kiếm</button>' +
        '    <button type="button" class="v2-btn v2-btn--tertiary btn-compact" id="f-clear"><i class="ri-refresh-line"></i> Nhập lại</button>' +
        '  </div>' +
        '  <div class="form-row filter-grid" id="ff-default"></div>' +
        '  <div class="advanced-filters collapsed" id="adv-filters">' +
        '    <div class="form-row filter-grid" id="ff-adv">' +
        '      <div class="col-md-3" data-ff="f-period"><label class="tp-label">Kỳ báo cáo</label>' +
        '        <select class="form-control form-control-sm" id="f-period"><option value="m1">Tháng 1/2026</option></select></div>' +
        '      <div class="col-md-3" data-ff="f-company"><label class="tp-label">Công ty</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-company">' + selOptions(uniq(function (r) { return r[CL.company]; }), function (c) { return c + ' — ' + ORG[c].name; }) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-type"><label class="tp-label">Loại tài khoản</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-type">' + selOptions(uniq(function (r) { return r[CL.type]; })) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-ccy"><label class="tp-label">Loại tiền</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-ccy">' + selOptions(uniq(function (r) { return r[CL.ccy]; })) + '</select></div>' +
        '      <div class="col-md-3" data-ff="f-bank"><label class="tp-label">Ngân hàng</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-bank">' + selOptions([...new Set(CBAL_ROWS.map(bankName).filter(Boolean))].sort()) + '</select></div>' +
        '    </div>' +
        '  </div>' +
        '  </div>' + /* /#filter-body */
        '</section>' +

        /* ----- BẢNG 3 tab ----- */
        '<section class="tp-card p-3">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-safe-2-line"></i></div>' +
        '      <div><h5 id="cbal-title">Báo cáo số dư tại quỹ và các ngân hàng</h5>' +
        '      <p class="tp-section-subtitle">Báo cáo quản trị nội bộ (không thuộc bộ BCTC theo TT 99/2025) · Kỳ: Tháng 01/2026 · Ngày kết sổ: 31/01/2026 · Đơn vị: Triệu đồng, nguyên tệ theo loại tiền</p></div>' +
        '    </div>' +
        '    <div class="table-actions">' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-print"><i class="ri-printer-line"></i> In báo cáo</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-excel"><i class="ri-file-excel-2-line"></i> Xuất Excel</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-cols" title="Chọn cột hiển thị trên bảng chi tiết"><i class="ri-layout-column-line"></i> Cấu hình cột</button>' +
        '    </div>' +
        '  </div>' +
        '  <ul class="nav-tabs">' +
        '    <li><button type="button" class="nav-link active" data-cbal="detail"><i class="ri-list-check-2"></i>Chi tiết theo tài khoản</button></li>' +
        '    <li><button type="button" class="nav-link" data-cbal="summary"><i class="ri-pie-chart-2-line"></i>Tổng hợp & nhận xét</button></li>' +
        '    <li><button type="button" class="nav-link" data-cbal="recon"><i class="ri-checkbox-multiple-line"></i>Đối chiếu Sổ Cái vs Sao kê NH</button></li>' +
        '  </ul>' +
        '  <div id="cbal-body"></div>' +
        '</section>' +

        /* ----- Modal In ----- */
        '<div class="modal-backdrop-demo" id="print-modal"><div class="modal-dialog" style="max-width:1100px">' +
        '  <div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-printer-line"></i></span>In Báo cáo số dư tại quỹ và các ngân hàng</h5>' +
        '  <button type="button" class="close" onclick="closeModal(\'print-modal\')">×</button></div>' +
        '  <div class="modal-body" id="print-preview" style="max-height:70vh"></div>' +
        '  <div class="modal-footer">' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-do-print"><i class="ri-printer-line"></i> In</button>' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'print-modal\')"><i class="ri-close-line"></i> Đóng</button>' +
        '  </div>' +
        '</div></div>' +
        '<div id="print-area"></div>');

    function val(id) { return document.getElementById(id).value; }
    function filtered() {
        var kw = val('f-search').toLowerCase().trim();
        return CBAL_ROWS.filter(function (r) {
            if (val('f-company') && r[CL.company] !== val('f-company')) return false;
            if (val('f-type') && r[CL.type] !== val('f-type')) return false;
            if (val('f-ccy') && r[CL.ccy] !== val('f-ccy')) return false;
            if (val('f-bank') && bankName(r) !== val('f-bank')) return false;
            if (kw && (r[CL.gl] + ' ' + r[CL.bankNo] + ' ' + r[CL.place]).toLowerCase().indexOf(kw) === -1) return false;
            return true;
        });
    }

    /* Cơ cấu số dư (thay 4 thẻ tổng quan cũ — đưa vào tfoot bảng chi tiết):
       3 dòng "Trong đó" render theo cột hiển thị để số luôn thẳng cột SDCK quy VND / % */
    function breakdownRowsHTML(visCols, list, totSdckVnd) {
        var cash = 0, bank = 0, fx = 0;
        list.forEach(function (r) {
            var v = clSdckVnd(r);
            if (r[CL.type] === 'Quỹ tiền mặt') cash += v; else bank += v;
            if (r[CL.ccy] !== 'VND') fx += v;
        });
        var identCount = 0;
        while (identCount < visCols.length && IDENT_KEYS.indexOf(visCols[identCount].key) !== -1) identCount++;
        function row(label, v) {
            var html = '<tr class="row-carry"><td colspan="' + identCount + '"><i>' + label + '</i></td>';
            visCols.slice(identCount).forEach(function (c) {
                if (c.key === 'sdckVnd') html += '<td class="text-right num"><i>' + fmtMoney(v) + '</i></td>';
                else if (c.key === 'pct') html += '<td class="text-right num"><i>' + (totSdckVnd ? pctStr(v / totSdckVnd) : '—') + '</i></td>';
                else html += '<td></td>';
            });
            return html + '</tr>';
        }
        return row('Trong đó — Quỹ tiền mặt', cash) +
            row('Trong đó — Tiền gửi ngân hàng + kỳ hạn', bank) +
            row('Trong đó — Ngoại tệ quy VND (theo dõi rủi ro tỷ giá)', fx);
    }

    /* ---------- Tab 1: Chi tiết — cột hiển thị (header 1 hàng, nhãn nhóm gộp vào tên cột) ----------
       16 cột như bảng gốc; bỏ hàng group 6 nhóm (ĐỊNH DANH/TIỀN TỆ/SDĐK/PS KỲ/SDCK/KHÁC),
       nghĩa nhóm được gộp vào tên cột: "SDĐK nguyên tệ", "PS Nợ (thu)", "SDCK quy VND ⭐"...
       - 6 cột định danh + cột "SDCK quy VND ⭐" đặt always: true (số dư cuối kỳ quy VND là
         số liệu cốt lõi của báo cáo số dư → không cho ẩn). Theo luật helper, cột always bị
         dồn cố định lên đầu bảng → "SDCK quy VND ⭐" đứng ngay sau 6 cột định danh, các cột
         optional (SDĐK → PS → SDCK nguyên tệ → %) vẫn giữ trình tự đọc phía sau.
       - Bản in GIỮ NGUYÊN 16 cột 6 nhóm như mẫu (printSheetHTML không đổi). */
    var COLUMNS = [
        { key: 'stt', label: 'STT', cls: 'text-center', style: 'width:40px', always: true },
        { key: 'company', label: 'Công ty', always: true },
        { key: 'type', label: 'Loại TK', always: true },
        { key: 'place', label: 'Ngân hàng /<br>Địa điểm quỹ', style: 'min-width:180px', always: true },
        { key: 'bankNo', label: 'Số TK<br>ngân hàng', always: true },
        { key: 'gl', label: 'TK<br>kế toán', cls: 'text-center', always: true },
        { key: 'sdckVnd', label: 'SDCK<br>quy VND ⭐', cls: 'text-right', always: true },
        { key: 'ccy', label: 'Loại tiền', cls: 'text-center' },
        { key: 'rate', label: 'Tỷ giá<br>cuối kỳ', cls: 'text-right' },
        { key: 'sdkNT', label: 'SDĐK<br>nguyên tệ', cls: 'text-right' },
        { key: 'sdkVnd', label: 'SDĐK<br>quy VND', cls: 'text-right' },
        { key: 'psNo', label: 'PS Nợ (thu)<br>nguyên tệ', cls: 'text-right' },
        { key: 'psCo', label: 'PS Có (chi)<br>nguyên tệ', cls: 'text-right' },
        { key: 'sdckNT', label: 'SDCK<br>nguyên tệ', cls: 'text-right' },
        { key: 'pct', label: '% trên<br>tổng', cls: 'text-right' },
        { key: 'note', label: 'Ghi chú' },
    ];
    /* 6 cột định danh đầu bảng — dòng TỔNG CỘNG gộp colspan qua các cột này */
    var IDENT_KEYS = ['stt', 'company', 'type', 'place', 'bankNo', 'gl'];
    var colCfg = setupColumnConfig({
        storageKey: 'demo-cashbalance-columns',
        btnId: 'btn-cols',
        columns: COLUMNS,
        fixedNote: '6 cột định danh tài khoản + cột <b>SDCK quy VND ⭐</b> (số liệu cốt lõi của báo cáo số dư) là <b>bắt buộc</b> và cố định ở đầu bảng.',
        onChange: function () {
            /* Đổi cấu hình cột ở tab Chi tiết → rebuild thead + re-init sort (như renderHeader của journal.js) */
            if (activeTab === 'detail' && document.getElementById('cbal-tbl')) renderDetailHeader();
            draw();
        },
    });

    /* ----- Phân trang tab Chi tiết (helper chung); 2 tab còn lại không phân trang ----- */
    var pager = createPager({ storageKey: 'demo-cashbalance-pagesize', containerSel: '#cbal-pager', onChange: function () { draw(); } });
    /* Đổi bộ lọc / tab / sort → tự về trang 1; chuyển trang giữ nguyên bộ lọc */
    function filterSignature() {
        return ['f-search', 'f-period', 'f-company', 'f-type', 'f-ccy', 'f-bank'].map(val).join('|') + '|' + activeTab + '|' + JSON.stringify(sortState);
    }

    /* ----- Sort theo cột — CHỈ áp dụng cho bảng tab Chi tiết (mô phỏng journal.js) -----
       Không sort → thứ tự chuẩn của báo cáo. Bản in (printSheetHTML) LUÔN theo thứ tự chuẩn.
       Dòng TỔNG CỘNG + 3 dòng "Trong đó" tính trên toàn bộ danh sách lọc → không đổi khi sort. */
    var sortState = null;
    /* Cột số sort numeric; các cột định danh (company, type, place, bankNo, gl, ccy, note) sort chuỗi */
    var SORT_NUMERIC = { stt: 1, rate: 1, sdkNT: 1, sdkVnd: 1, psNo: 1, psCo: 1, sdckNT: 1, sdckVnd: 1, pct: 1 };
    /* Giá trị sort của 1 dòng theo key cột — dùng ĐÚNG các hàm mà cellHTML dùng để hiển thị */
    function sortVal(item, key) {
        var r = item.r;
        switch (key) {
            case 'stt': return item.stt;
            case 'company': return r[CL.company];
            case 'type': return r[CL.type];
            case 'place': return r[CL.place];
            case 'bankNo': return r[CL.bankNo];
            case 'gl': return glCode(r[CL.gl]);
            case 'ccy': return r[CL.ccy];
            case 'rate': return r[CL.rate];
            case 'sdkNT': return r[CL.sdk];
            case 'sdkVnd': return clSdkVnd(r);
            case 'psNo': return r[CL.no];
            case 'psCo': return r[CL.co];
            case 'sdckNT': return clSdck(r);
            case 'sdckVnd': return clSdckVnd(r);
            case 'pct': return clSdckVnd(r); /* % tỷ lệ thuận SDCK quy VND → sort tương đương */
            case 'note': return r[CL.note];
            default: return '';
        }
    }
    /* Sort trên TOÀN BỘ wrapped (đã đánh stt theo danh sách lọc gốc) TRƯỚC khi paginate.
       STT giữ số gốc → như NKC giữ STT dòng khi sort. Tie-break: stt (thứ tự gốc). */
    function applySort(wrapped) {
        if (!sortState) return wrapped;
        var key = sortState.key, asc = sortState.dir === 'asc' ? 1 : -1;
        return wrapped.slice().sort(function (a, b) {
            var x = sortVal(a, key), y = sortVal(b, key);
            if (SORT_NUMERIC[key]) return (x - y) * asc || a.stt - b.stt;
            if (x === y) return a.stt - b.stt;
            return (x < y ? -1 : 1) * asc;
        });
    }

    /* Render 1 ô theo key cột — item = {r, stt} (stt tính trên TOÀN BỘ danh sách lọc, liên tục qua trang) */
    function cellHTML(item, c, totSdckVnd) {
        var r = item.r;
        switch (c.key) {
            case 'stt': return '<td class="text-center">' + item.stt + '</td>';
            case 'company': return '<td><b>' + r[CL.company] + '</b></td>';
            case 'type': return '<td>' + r[CL.type] + '</td>';
            case 'place': return '<td style="white-space:normal">' + r[CL.place] + '</td>';
            case 'bankNo': return '<td class="num">' + (r[CL.bankNo] || '—') + '</td>';
            case 'gl': return '<td class="text-center"><b>' + glCode(r[CL.gl]) + '</b></td>';
            case 'ccy': return '<td class="text-center">' + r[CL.ccy] + '</td>';
            case 'rate': return '<td class="text-right num">' + String(r[CL.rate]).replace('.', ',') + '</td>';
            case 'sdkNT': return '<td class="text-right num">' + fmtMoney(r[CL.sdk]) + '</td>';
            case 'sdkVnd': return '<td class="text-right num">' + fmtMoney(clSdkVnd(r)) + '</td>';
            case 'psNo': return '<td class="text-right num">' + fmtMoney(r[CL.no]) + '</td>';
            case 'psCo': return '<td class="text-right num">' + fmtMoney(r[CL.co]) + '</td>';
            case 'sdckNT': return '<td class="text-right num" style="font-weight:700">' + fmtMoney(clSdck(r)) + '</td>';
            case 'sdckVnd': {
                /* Pill cảnh báo gắn vào cột SDCK quy VND (cột always → cảnh báo không bao giờ bị ẩn theo cấu hình cột) */
                var sdck = clSdck(r), sdckVnd = clSdckVnd(r);
                var warn = '';
                if (sdck < 0) warn = ' <span class="status-pill st-cancel" title="Số dư âm — LỖI NGHIÊM TRỌNG">⛔ ÂM</span>';
                else if (r[CL.type] === 'Quỹ tiền mặt' && sdckVnd > 100) warn = ' <span class="status-pill st-paused" title="Quỹ tiền mặt vượt hạn mức tồn quỹ nội bộ 100 triệu — gợi ý nộp bớt vào ngân hàng (chi tiền mặt ≥ 5tr cho HHDV không được khấu trừ VAT theo NĐ 181/2025)">⚠ >100tr</span>';
                return '<td class="text-right num" style="font-weight:700">' + fmtMoney(sdckVnd) + warn + '</td>';
            }
            case 'pct': return '<td class="text-right num">' + (totSdckVnd ? pctStr(clSdckVnd(r) / totSdckVnd) : '—') + '</td>';
            case 'note': return '<td class="tp-small-text" style="white-space:normal;min-width:170px">' + r[CL.note] + '</td>';
            default: return '<td></td>';
        }
    }
    /* Dòng TỔNG CỘNG render theo colCfg.visible() — từng ô theo key cột để số tổng luôn thẳng cột */
    function totalRowHTML(visCols, count, totSdkVnd, totSdckVnd) {
        var identCount = 0;
        while (identCount < visCols.length && IDENT_KEYS.indexOf(visCols[identCount].key) !== -1) identCount++;
        var html = '<tr class="row-total"><td colspan="' + identCount + '">TỔNG CỘNG (quy đổi VND) — ' + count + ' tài khoản</td>';
        visCols.slice(identCount).forEach(function (c) {
            if (c.key === 'sdkVnd') html += '<td class="text-right num">' + fmtMoney(totSdkVnd) + '</td>';
            else if (c.key === 'sdckVnd') html += '<td class="text-right num">' + fmtMoney(totSdckVnd) + '</td>';
            else if (c.key === 'pct') html += '<td class="text-right num">100%</td>';
            else html += '<td></td>'; /* nguyên tệ nhiều loại tiền → không cộng gộp (giữ logic cũ) */
        });
        return html + '</tr>';
    }

    /* ---------- Tab 1: Chi tiết ----------
       Tách 3 tầng (mô phỏng renderHeader của journal.js) để icon sort giữ trạng thái active:
       - renderDetailSkeleton(): khung tĩnh (note-box, table rỗng, pager) — chỉ dựng khi vào tab
       - renderDetailHeader():   thead + setupColumnSort — chỉ rebuild khi đổi cấu hình cột
       - drawDetail():           tbody + tfoot theo bộ lọc/sort/trang — KHÔNG động vào thead */
    function renderDetailSkeleton() {
        /* setupColumnSort không nhận trạng thái khởi tạo → khi dựng lại khung (quay về từ tab khác)
           reset sort về thứ tự chuẩn để icon trên header và dữ liệu luôn khớp nhau */
        sortState = null;
        document.getElementById('cbal-body').innerHTML =
            '<div class="note-box"><i class="ri-information-line"></i> SDCK (nguyên tệ) = SDĐK + PS Nợ − PS Có · Quy VND theo hệ số tỷ giá (VND = 1; USD = 0,025 tương đương 25.000 VND/USD, đơn vị triệu). PS Nợ lấy từ Sổ NK Thu tiền (S03a1), PS Có từ Sổ NK Chi tiền (S03a2). Quỹ tiền mặt &gt; 100 triệu → cảnh báo vượt hạn mức tồn quỹ nội bộ (gợi ý nộp NH — từ 01/07/2025 chi tiền mặt ≥ 5tr cho HHDV không được khấu trừ VAT theo Luật 48/2024 &amp; NĐ 181/2025); số dư âm → lỗi nghiêm trọng.</div>' +
            '<div class="table-wrapper scrollbar-thin"><table class="data-table" id="cbal-tbl">' +
            '<thead><tr id="cbal-head"></tr></thead>' +
            '<tbody id="cbal-tbody"></tbody>' +
            '<tfoot id="cbal-tfoot"></tfoot>' +
            '</table></div>' +
            '<div class="table-pager" id="cbal-pager"></div>' +
            '<div class="d-flex align-center gap-2 mt-2"><span class="tp-small-text">Kiểm tra liên kết: số dư báo cáo khớp tuyệt đối với Sổ Cái TK 111/112/128 cùng thời điểm</span> <span class="status-pill st-done"><i class="ri-checkbox-circle-line"></i>KHỚP SỔ CÁI</span></div>';
        renderDetailHeader();
    }
    function renderDetailHeader() {
        var visCols = colCfg.visible();
        document.getElementById('cbal-head').innerHTML = visCols.map(function (c) {
            return '<th' + (c.cls ? ' class="' + c.cls + '"' : '') + (c.style ? ' style="' + c.style + '"' : '') + '>' + c.label + '</th>';
        }).join('');
        /* Cột đang sort bị ẩn qua cấu hình cột → reset về thứ tự chuẩn */
        if (sortState && !visCols.some(function (c) { return c.key === sortState.key; })) sortState = null;
        setupColumnSort({
            tableSel: '#cbal-tbl',
            headRow: 1,
            cols: visCols.map(function (c) { return { key: c.key }; }),
            onChange: function (s) { sortState = s; drawDetail(); },
        });
    }
    function drawDetail() {
        /* Vừa chuyển từ tab khác về (cbal-body đã bị tab khác ghi đè) → dựng lại khung + thead */
        if (!document.getElementById('cbal-tbl')) renderDetailSkeleton();
        var list = filtered();
        /* Dòng TỔNG CỘNG + % trên tổng tính trên TOÀN BỘ danh sách lọc (không theo trang, không theo sort) */
        var totSdkVnd = 0, totSdckVnd = 0;
        list.forEach(function (r) { totSdkVnd += clSdkVnd(r); totSdckVnd += clSdckVnd(r); });
        var visCols = colCfg.visible();
        var totalRow = totalRowHTML(visCols, list.length, totSdkVnd, totSdckVnd);
        /* Đánh STT TRƯỚC khi sort → STT giữ số gốc theo danh sách lọc, liên tục qua trang */
        var wrapped = list.map(function (r, i) { return { r: r, stt: i + 1 }; });
        /* Sort toàn bộ danh sách rồi mới phân trang */
        var pageRows = pager.paginate(applySort(wrapped), filterSignature());
        var body = pageRows.map(function (item) {
            return '<tr>' + visCols.map(function (c) { return cellHTML(item, c, totSdckVnd); }).join('') + '</tr>';
        }).join('');
        document.getElementById('cbal-tbody').innerHTML =
            totalRow + (list.length ? body : '<tr><td colspan="' + visCols.length + '"><div class="empty-state"><div class="es-icon"><i class="ri-inbox-2-line"></i></div>Không có tài khoản phù hợp bộ lọc.</div></td></tr>');
        document.getElementById('cbal-tfoot').innerHTML = totalRow + breakdownRowsHTML(visCols, list, totSdckVnd);
        applyStickyTotals('#cbal-tbl');
        pager.render();
    }

    /* ---------- Tab 2: Tổng hợp & nhận xét ---------- */
    function drawSummary() {
        var comps = [...new Set(CBAL_ROWS.map(function (r) { return r[CL.company]; }))];
        function sumBy(c, fn) {
            var s = 0;
            CBAL_ROWS.forEach(function (r) { if (r[CL.company] === c && fn(r)) s += clSdckVnd(r); });
            return s;
        }
        var grand = 0;
        CBAL_ROWS.forEach(function (r) { grand += clSdckVnd(r); });
        var rowsA = comps.map(function (c) {
            var cashV = sumBy(c, function (r) { return r[CL.type] === 'Quỹ tiền mặt' && r[CL.ccy] === 'VND'; });
            var cashF = sumBy(c, function (r) { return r[CL.type] === 'Quỹ tiền mặt' && r[CL.ccy] !== 'VND'; });
            var bankV = sumBy(c, function (r) { return r[CL.type] === 'Tiền gửi NH' && r[CL.ccy] === 'VND'; });
            var bankF = sumBy(c, function (r) { return r[CL.type] === 'Tiền gửi NH' && r[CL.ccy] !== 'VND'; });
            var term = sumBy(c, function (r) { return r[CL.type] === 'Tiền gửi kỳ hạn'; });
            var total = cashV + cashF + bankV + bankF + term;
            return '<tr><td><b>' + c + '</b> <span class="tp-small-text">' + ORG[c].name + '</span></td>' +
                [cashV, cashF, bankV, bankF, term, total].map(function (v, i) {
                    return '<td class="text-right num"' + (i === 5 ? ' style="font-weight:700"' : '') + '>' + fmtMoney(v) + '</td>';
                }).join('') +
                '<td class="text-right num">' + pctStr(total / grand) + '</td></tr>';
        }).join('');
        var ccys = [...new Set(CBAL_ROWS.map(function (r) { return r[CL.ccy]; }))];
        var rowsB = ccys.map(function (ccy) {
            var nt = 0, vnd = 0, rate = 1;
            CBAL_ROWS.forEach(function (r) { if (r[CL.ccy] === ccy) { nt += clSdck(r); vnd += clSdckVnd(r); rate = r[CL.rate]; } });
            return '<tr><td><b>' + ccy + '</b></td><td class="text-right num">' + fmtMoney(nt) + '</td>' +
                '<td class="text-right num">' + (ccy === 'VND' ? '1' : fmtMoney(rate * 1000000)) + '</td>' +
                '<td class="text-right num" style="font-weight:700">' + fmtMoney(vnd) + '</td>' +
                '<td class="text-right num">' + pctStr(vnd / grand) + '</td></tr>';
        }).join('');
        document.getElementById('cbal-body').innerHTML =
            '<div class="filter-header-left mb-2"><div class="tp-icon-chip"><i class="ri-building-line"></i></div><p class="tp-section-title">A. Tổng hợp theo pháp nhân</p></div>' +
            '<div class="table-wrapper"><table class="data-table"><thead><tr>' +
            '<th style="min-width:220px">Pháp nhân</th><th class="text-right">Tiền mặt VND</th><th class="text-right">Tiền mặt ngoại tệ<br>(quy VND)</th><th class="text-right">TGNH VND</th><th class="text-right">TGNH ngoại tệ<br>(quy VND)</th><th class="text-right">Tiền gửi<br>kỳ hạn</th><th class="text-right">Tổng cộng<br>(triệu VND)</th><th class="text-right">% trên tổng</th>' +
            '</tr></thead><tbody>' + rowsA + '</tbody>' +
            '<tfoot><tr><td>TỔNG TẬP ĐOÀN</td><td colspan="5"></td><td class="text-right num">' + fmtMoney(grand) + '</td><td class="text-right num">100%</td></tr></tfoot></table></div>' +
            '<div class="filter-header-left mb-2 mt-3"><div class="tp-icon-chip"><i class="ri-exchange-line"></i></div><p class="tp-section-title">B. Tổng hợp theo loại tiền tệ</p></div>' +
            '<div class="table-wrapper" style="max-width:640px"><table class="data-table"><thead><tr>' +
            '<th>Loại tiền</th><th class="text-right">Số lượng nguyên tệ<br>(triệu)</th><th class="text-right">Tỷ giá TB<br>(VND)</th><th class="text-right">Quy đổi VND<br>(triệu đồng)</th><th class="text-right">% trên tổng</th>' +
            '</tr></thead><tbody>' + rowsB + '</tbody></table></div>' +
            '<div class="filter-header-left mb-2 mt-3"><div class="tp-icon-chip chip-amber"><i class="ri-lightbulb-line"></i></div><p class="tp-section-title">C. Nhận xét & cảnh báo</p></div>' +
            '<div class="note-box" style="line-height:1.9">' +
            '💰 Tổng số dư tiền tập đoàn cuối tháng 01/2026: <b>' + fmtMoney(grand) + ' triệu đồng</b> (~255,2 tỷ), tăng so với đầu kỳ.<br>' +
            '🏢 <b>TPE chiếm ~80,4%</b> tổng số dư tiền tập đoàn — công ty mẹ giữ vai trò trung tâm dòng tiền.<br>' +
            '💵 Ngoại tệ (USD) chiếm ~2,0% tổng số dư → mức thấp, ít rủi ro tỷ giá; cần theo dõi biến động.<br>' +
            '⚠ TPSG và TPHP có số dư tiền tương đối thấp so với quy mô hoạt động — cần kiểm tra tính đủ vốn lưu động.<br>' +
            '💡 30 tỷ tiền gửi kỳ hạn 6 tháng đáo hạn 15/03/2026 — cần kế hoạch tái đầu tư hoặc rút về sử dụng.<br>' +
            '🏦 Tiền tập trung tại 6 ngân hàng — phân tán rủi ro nhưng tốn chi phí quản lý nhiều tài khoản.' +
            '</div>';
    }

    /* ---------- Tab 3: Đối chiếu SC vs Sao kê ---------- */
    function drawRecon() {
        var totSC = 0, totBank = 0, matched = 0;
        var body = CBAL_RECON.map(function (r, i) {
            var diff = r[3] - r[4];
            totSC += r[3]; totBank += r[4];
            if (diff === 0) matched++;
            return '<tr' + (diff !== 0 ? ' style="background:#fffbeb"' : '') + '>' +
                '<td class="text-center">' + (i + 1) + '</td>' +
                '<td><b>' + r[0] + '</b></td>' +
                '<td class="text-center"><b>' + glCode(r[1]) + '</b></td>' +
                '<td>' + r[2] + '</td>' +
                '<td class="text-right num">' + fmtMoney(r[3]) + '</td>' +
                '<td class="text-right num">' + fmtMoney(r[4]) + '</td>' +
                '<td class="text-right num"' + (diff !== 0 ? ' style="color:#b91c1c;font-weight:700"' : '') + '>' + (diff === 0 ? '0' : (diff > 0 ? '+' : '−') + fmtMoney(Math.abs(diff))) + '</td>' +
                '<td class="text-center">' + (diff === 0 ? '<span class="status-pill st-done">✓ Khớp</span>' : '<span class="status-pill st-paused">⚠ Lệch</span>') + '</td>' +
                '<td style="white-space:normal;min-width:260px" class="tp-small-text">' + r[5] + '</td>' +
                '</tr>';
        }).join('');
        document.getElementById('cbal-body').innerHTML =
            '<div class="note-box"><i class="ri-information-line"></i> Đối chiếu tối thiểu 1 lần/tháng (tốt nhất hằng tuần với TK giao dịch nhiều). Trong ERP nên chạy tự động hằng ngày, cảnh báo khi chênh lệch &gt; 1% giá trị tài khoản. Tại ngày 31/01/2026 · Đơn vị: Triệu đồng.</div>' +
            '<div class="table-wrapper"><table class="data-table"><thead><tr>' +
            '<th class="text-center" style="width:40px">STT</th><th>Công ty</th><th class="text-center">TK kế toán</th><th style="min-width:200px">Ngân hàng</th>' +
            '<th class="text-right">SD Sổ Cái (A)</th><th class="text-right">SD Sao kê NH (B)</th><th class="text-right">Chênh lệch (A − B)</th><th class="text-center">Trạng thái</th><th>Nguyên nhân &amp; xử lý</th>' +
            '</tr></thead><tbody>' + body + '</tbody>' +
            '<tfoot><tr><td colspan="4">TỔNG CỘNG — khớp ' + matched + '/' + CBAL_RECON.length + ' tài khoản</td>' +
            '<td class="text-right num">' + fmtMoney(totSC) + '</td><td class="text-right num">' + fmtMoney(totBank) + '</td>' +
            '<td class="text-right num">' + fmtMoney(totSC - totBank) + '</td><td colspan="2"></td></tr></tfoot></table></div>' +
            '<div class="note-box" style="margin-top:12px;line-height:1.9">' +
            '✓ 9 tài khoản NH cần đối chiếu: <b>7 khớp, 2 chênh lệch</b> (~0,2% tổng số dư).<br>' +
            '📌 BIDV (−50tr): UNC đã ghi sổ trước, NH xử lý T+1 → chờ khớp tháng sau, không cần điều chỉnh.<br>' +
            '📌 VPBank (+25tr): lãi tiền gửi chưa hạch toán → cần bổ sung bút toán ghi thu nhập tài chính (515).<br>' +
            '⚡ Sau khi hạch toán bổ sung, chênh lệch còn lại thuộc timing ngân hàng — chấp nhận được.' +
            '</div>';
    }

    function draw() {
        /* Cấu hình cột chỉ áp dụng cho bảng tab Chi tiết → ẩn nút ở 2 tab còn lại */
        document.getElementById('btn-cols').style.display = activeTab === 'detail' ? '' : 'none';
        if (activeTab === 'detail') drawDetail();
        else if (activeTab === 'summary') drawSummary();
        else drawRecon();
    }

    /* tabs */
    document.querySelectorAll('[data-cbal]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.querySelectorAll('[data-cbal]').forEach(function (b) { b.classList.remove('active'); });
            btn.classList.add('active');
            activeTab = btn.dataset.cbal;
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
    document.querySelectorAll('.f-adv').forEach(function (el) { el.addEventListener('change', draw); });
    document.getElementById('f-search').addEventListener('keydown', function (e) { if (e.key === 'Enter') draw(); });
    document.getElementById('f-search').addEventListener('input', function () {
        document.getElementById('f-search-clear').style.display = this.value ? 'inline-flex' : 'none';
    });
    document.getElementById('f-search-clear').addEventListener('click', function () { document.getElementById('f-search').value = ''; draw(); });
    document.getElementById('f-go').addEventListener('click', draw);
    document.getElementById('f-clear').addEventListener('click', function () {
        ['f-search', 'f-company', 'f-type', 'f-ccy', 'f-bank'].forEach(function (id) { document.getElementById(id).value = ''; });
        draw();
    });
    document.getElementById('btn-excel').addEventListener('click', function () {
        toast('Demo: file Excel sẽ được tải xuống ở bản chính thức', 'info');
    });

    /* ----- In báo cáo (mẫu chuẩn) ----- */
    function printSheetHTML() {
        var list = filtered();
        var totSdkVnd = 0, totSdckVnd = 0;
        list.forEach(function (r) { totSdkVnd += clSdkVnd(r); totSdckVnd += clSdckVnd(r); });
        var body = list.map(function (r, i) {
            return '<tr>' +
                '<td class="pc">' + (i + 1) + '</td><td class="pc">' + r[CL.company] + '</td><td>' + r[CL.type] + '</td>' +
                '<td>' + r[CL.place] + '</td><td class="pc">' + (r[CL.bankNo] || '') + '</td><td class="pc">' + glCode(r[CL.gl]) + '</td>' +
                '<td class="pc">' + r[CL.ccy] + '</td><td class="pr">' + String(r[CL.rate]).replace('.', ',') + '</td>' +
                '<td class="pr">' + fmtMoney(r[CL.sdk]) + '</td><td class="pr">' + fmtMoney(clSdkVnd(r)) + '</td>' +
                '<td class="pr">' + fmtMoney(r[CL.no]) + '</td><td class="pr">' + fmtMoney(r[CL.co]) + '</td>' +
                '<td class="pr"><b>' + fmtMoney(clSdck(r)) + '</b></td><td class="pr"><b>' + fmtMoney(clSdckVnd(r)) + '</b></td>' +
                '<td class="pr">' + (totSdckVnd ? pctStr(clSdckVnd(r) / totSdckVnd) : '') + '</td>' +
                '<td style="font-size:10px">' + r[CL.note] + '</td>' +
                '</tr>';
        }).join('');
        var company = val('f-company');
        return '<div class="print-sheet">' +
            '<table class="p-head"><tr>' +
            '<td style="width:55%"><b>Đơn vị:</b> ' + (company ? ORG[company].name : 'TẬP ĐOÀN TÂN PHÁT (tổng hợp 3 pháp nhân)') + '<br><b>Địa chỉ:</b> ……………………………</td>' +
            '<td style="text-align:center"><b>BÁO CÁO QUẢN TRỊ NỘI BỘ</b><br><i style="font-size:10.5px">(Không thuộc bộ BCTC theo TT99/2025)</i></td>' +
            '</tr></table>' +
            '<div class="p-title">BÁO CÁO SỐ DƯ TẠI QUỸ VÀ CÁC NGÂN HÀNG</div>' +
            '<div class="p-sub">Kỳ báo cáo: Từ ngày 01/01/2026 đến ngày 31/01/2026</div>' +
            '<div class="p-unit">Đơn vị tính: Triệu đồng (VNĐ), nguyên tệ theo loại tiền tương ứng</div>' +
            '<table class="p-grid" style="font-size:10.5px">' +
            '<thead>' +
            '<tr><th colspan="6">ĐỊNH DANH TÀI KHOẢN</th><th colspan="2">TIỀN TỆ</th><th colspan="2">SỐ DƯ ĐẦU KỲ</th><th colspan="2">PHÁT SINH TRONG KỲ</th><th colspan="3">SỐ DƯ CUỐI KỲ ⭐</th><th>KHÁC</th></tr>' +
            '<tr><th>STT</th><th>Công ty</th><th>Loại</th><th>Ngân hàng /<br>Địa điểm quỹ</th><th>Số TK<br>ngân hàng</th><th>TK<br>kế toán</th>' +
            '<th>Loại<br>tiền</th><th>Tỷ giá<br>cuối kỳ</th><th>SDĐK<br>(ng.tệ)</th><th>SDĐK<br>(VND)</th><th>PS Nợ<br>(ng.tệ)</th><th>PS Có<br>(ng.tệ)</th>' +
            '<th>SDCK<br>(ng.tệ)</th><th>SDCK<br>(VND)</th><th>% trên<br>tổng</th><th>Ghi chú</th></tr>' +
            '</thead><tbody>' + body +
            '<tr class="p-total"><td colspan="9" style="text-align:left"><b>TỔNG CỘNG (quy đổi VND)</b></td>' +
            '<td class="pr"><b>' + fmtMoney(totSdkVnd) + '</b></td><td></td><td></td><td></td>' +
            '<td class="pr"><b>' + fmtMoney(totSdckVnd) + '</b></td><td class="pr"><b>100%</b></td><td></td></tr>' +
            '</tbody></table>' +
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

    /* Cài đặt bộ lọc — quy tắc "mặc định = bắt buộc": chỉ Kỳ báo cáo (locked) hiện mặc định,
       mọi trường khác (kể cả Công ty, Loại TK) nằm trong Tìm kiếm nâng cao trừ khi user tự cấu hình.
       Màn này chỉ có 1 trường tổ chức (Công ty) → KHÔNG cần gom nhóm grp-org. */
    setupFilterSettings({
        storageKey: 'demo-filter-cashbalance',
        gearBtnId: 'ff-gear',
        defaultWrap: 'ff-default',
        advWrap: 'ff-adv',
        fields: [
            { id: 'f-period', label: 'Kỳ báo cáo', locked: true },
            { id: 'f-company', label: 'Công ty' },
            { id: 'f-type', label: 'Loại tài khoản' },
            { id: 'f-ccy', label: 'Loại tiền' },
            { id: 'f-bank', label: 'Ngân hàng' },
        ],
    });

    /* Ẩn / hiện toàn bộ khu vực bộ lọc (helper chung, lưu trạng thái theo màn) */
    setupFilterHide({ storageKey: 'demo-filter-cashbalance-hidden', btnId: 'f-hide', bodyId: 'filter-body' });

    draw();
}

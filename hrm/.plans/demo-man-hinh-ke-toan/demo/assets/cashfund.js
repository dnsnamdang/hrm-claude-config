/* ============================================================
   Demo Kế toán HRM — SỔ QUỸ TIỀN MẶT (S04a-DN VND & S04b-DN ngoại tệ)
   Nguồn cấu trúc: file Mau_So_Quy_TT99_2025.xlsx (user cung cấp)
   - Sổ do THỦ QUỸ ghi (khác Sổ Cái TK 111 do kế toán ghi) — cột Tồn quỹ cập nhật realtime từng dòng
   - Sổ ngoại tệ theo dõi SONG SONG nguyên tệ + quy đổi VNĐ; cuối kỳ đánh giá tỷ giá (TK 413)
   - Nguyên tắc "3 số dư phải khớp": Sổ quỹ = Sổ Cái TK 111 = Kiểm quỹ thực tế
   - Cảnh báo chi tiền mặt: từ 01/07/2025 (Luật Thuế GTGT 48/2024/QH15 + NĐ 181/2025/NĐ-CP),
     hóa đơn mua HHDV từ 5 triệu đồng trở lên (gồm VAT) phải thanh toán KHÔNG dùng tiền mặt
     mới được khấu trừ thuế GTGT / tính chi phí được trừ
   ============================================================ */

var FUND_OPEN = { 'TPE': 25000000, 'TPSG': 12000000, 'TPHP': 6000000 }; // SDĐK quỹ VND 01/01/2026
var FUND_KEEPER = { 'TPE': 'Nguyễn Thị Hạnh', 'TPSG': 'Võ Minh Trí', 'TPHP': 'Đặng Thu Hà' };

/* Quỹ VND: [dateGS, dateCT, soPT, soPC, desc, thu, chi, tkDoiUng, company] */
var FUND_VND = [
    ['2026-01-02', '2026-01-02', 'PT-01', '', 'Thu hoàn tạm ứng NV-005 dư', 3000000, 0, '141', 'TPE'],
    ['2026-01-03', '2026-01-03', '', 'PC-01', 'Chi mua văn phòng phẩm quý 1', 0, 3500000, '6428', 'TPE'],
    ['2026-01-05', '2026-01-05', 'PT-02', '', 'Thu tiền bán hàng KH-A (đã bao gồm VAT)', 66000000, 0, '511, 3331', 'TPE'],
    ['2026-01-06', '2026-01-06', '', 'PC-02', 'Chi mua NVL nhập kho NCC-X', 0, 55000000, '152, 133', 'TPE'],
    ['2026-01-08', '2026-01-08', 'PT-03', '', 'Rút tiền NH VCB nhập quỹ', 200000000, 0, '1121', 'TPE'],
    ['2026-01-09', '2026-01-09', '', 'PC-03', 'Tạm ứng NV-001 mua NVL', 0, 20000000, '141', 'TPE'],
    ['2026-01-10', '2026-01-10', '', 'PC-04', 'Nộp tiền vào NH VCB', 0, 100000000, '1121', 'TPE'],
    ['2026-01-12', '2026-01-12', 'PT-04', '', 'Thu hoàn tạm ứng NV-020 (thừa)', 5000000, 0, '141', 'TPE'],
    ['2026-01-15', '2026-01-15', 'PT-05', '', 'Thu tiền bán hàng lẻ trong ngày', 30000000, 0, '511', 'TPE'],
    ['2026-01-15', '2026-01-15', '', 'PC-05', 'Tạm ứng NV-010 đi công tác Đà Nẵng', 0, 20000000, '141', 'TPE'],
    ['2026-01-18', '2026-01-18', 'PT-06', '', 'Rút tiền NH BIDV nhập quỹ', 250000000, 0, '1121', 'TPE'],
    ['2026-01-20', '2026-01-20', 'PT-07', '', 'Thu tiền cho thuê VP tầng 3', 55000000, 0, '511, 3331', 'TPE'],
    ['2026-01-20', '2026-01-20', '', 'PC-06', 'Chi tiền quà tết cho khách hàng VIP', 0, 30000000, '6428', 'TPE'],
    ['2026-01-22', '2026-01-22', 'PT-08', '', 'Thu tiền lãi cho vay ngắn hạn', 15000000, 0, '515', 'TPE'],
    ['2026-01-22', '2026-01-22', '', 'PC-07', 'Nộp tiền vào NH VCB', 0, 150000000, '1121', 'TPE'],
    ['2026-01-24', '2026-01-24', '', 'PC-08', 'Mua công cụ dụng cụ văn phòng', 0, 8800000, '153, 133', 'TPE'],
    ['2026-01-25', '2026-01-25', 'PT-09', '', 'Rút tiền NH TCB nhập quỹ chuẩn bị chi lương', 200000000, 0, '1121', 'TPE'],
    ['2026-01-27', '2026-01-27', '', 'PC-09', 'Nộp tiền vào NH BIDV', 0, 200000000, '1121', 'TPE'],
    ['2026-01-28', '2026-01-28', 'PT-10', '', 'Thu tiền bán hàng cửa hàng cuối kỳ', 45000000, 0, '511', 'TPE'],
    ['2026-01-28', '2026-01-28', '', 'PC-10', 'Nộp tiền vào NH TCB', 0, 150000000, '1121', 'TPE'],
    ['2026-01-30', '2026-01-30', 'PT-11', '', 'Hoàn tiền đặt cọc từ NCC-W', 131000000, 0, '331', 'TPE'],
    ['2026-01-30', '2026-01-30', '', 'PC-11', 'Chi trả nợ tiền mặt NCC-W', 0, 60000000, '331', 'TPE'],
    ['2026-01-31', '2026-01-31', '', 'PC-12', 'Nộp tiền vào NH VCB cuối kỳ', 0, 197700000, '1121', 'TPE'],
    /* TPSG (khớp tổng thu 200tr / chi 197tr → SDCK 15tr) */
    ['2026-01-09', '2026-01-09', 'PT-B01', '', 'Thu tiền bán hàng lẻ showroom', 120000000, 0, '511', 'TPSG'],
    ['2026-01-15', '2026-01-15', '', 'PC-B01', 'Tạm ứng NV-101 mua vật tư', 0, 47000000, '141', 'TPSG'],
    ['2026-01-20', '2026-01-20', 'PT-B02', '', 'Rút tiền NH VPBank nhập quỹ', 80000000, 0, '1121', 'TPSG'],
    ['2026-01-28', '2026-01-28', '', 'PC-B02', 'Nộp tiền vào NH VPBank', 0, 150000000, '1121', 'TPSG'],
    /* TPHP (khớp tổng thu 150tr / chi 148tr → SDCK 8tr) */
    ['2026-01-10', '2026-01-10', 'PT-H01', '', 'Thu tiền dịch vụ lắp đặt KH-H', 90000000, 0, '511, 3331', 'TPHP'],
    ['2026-01-18', '2026-01-18', '', 'PC-H01', 'Chi phí văn phòng + tiếp khách', 0, 28000000, '6428', 'TPHP'],
    ['2026-01-22', '2026-01-22', 'PT-H02', '', 'Rút tiền NH Sacombank nhập quỹ', 60000000, 0, '1121', 'TPHP'],
    ['2026-01-29', '2026-01-29', '', 'PC-H02', 'Nộp tiền vào NH Sacombank', 0, 120000000, '1121', 'TPHP'],
];
var FV = { dateGS: 0, dateCT: 1, pt: 2, pc: 3, desc: 4, thu: 5, chi: 6, tk: 7, company: 8 };

/* ---------- Thông tin phiếu (demo: sinh ổn định theo số chứng từ) ---------- */
var FUND_REQUESTERS = ['Nguyễn Văn Hùng — P. Kinh doanh', 'Trần Thị Mai — P. Hành chính', 'Phạm Quốc Anh — P. Kỹ thuật', 'Lê Thị Thu — P. Kế toán', 'Đỗ Minh Tuấn — Ban Giám đốc', 'Vũ Thị Lan — P. Mua hàng'];
var FUND_PREPARERS = ['Ngô Thị Hoa (KT thanh toán)', 'Bùi Văn Nam (KT thanh toán)', 'Đặng Thu Trang (KT tiền mặt)'];
var FUND_PAYERS = ['Nguyễn Văn Hùng (NV)', 'Công ty TNHH Yên Bình', 'Trần Thị Mai (NV)', 'Công ty CP Xuân Phát', 'Đỗ Minh Tuấn (NV)', 'Công ty TNHH An Bình'];
var FUND_RECEIVERS = ['Công ty CP Thiết bị Xuân Hòa', 'Nguyễn Văn Hùng (NV)', 'VNPT Hà Nội', 'Trần Thị Mai (NV)', 'Công ty TNHH Vạn Lợi', 'Đỗ Minh Tuấn (NV)'];
function fundHash(s) { s = String(s); var h = 0; for (var i = 0; i < s.length; i++) h = (h * 131 + s.charCodeAt(i)) >>> 0; return h; }
function fundCtNo(r) { return r[FV.pt] || r[FV.pc] || ''; }
function fundIsThu(r) { return !!r[FV.thu]; }
function fundPick(pool, r, salt) { return pool[fundHash(fundCtNo(r) + '|' + salt) % pool.length]; }
function fundRequester(r) { return fundPick(FUND_REQUESTERS, r, 'req'); }
function fundPreparer(r) { return fundPick(FUND_PREPARERS, r, 'prep'); }
function fundReceiver(r) { return fundPick(fundIsThu(r) ? FUND_PAYERS : FUND_RECEIVERS, r, 'recv'); }

/* Quỹ ngoại tệ USD (chỉ TPE): [dateGS, dateCT, soPT, soPC, desc, tyGia, thuUSD, chiUSD, ghiChu] */
var FUND_USD_OPEN = { usd: 4000, vnd: 100000000 };
var FUND_USD = [
    ['2026-01-05', '2026-01-05', 'PT-U01', '', 'Thu ngoại tệ từ KH-NB thanh toán trực tiếp', 25000, 1000, 0, 'Xuất khẩu'],
    ['2026-01-12', '2026-01-12', '', 'PC-U01', 'Chi công tác phí NV-002 đi Nhật Bản', 25000, 0, 500, 'Công tác 5 ngày'],
    ['2026-01-18', '2026-01-18', 'PT-U02', '', 'Thu ngoại tệ thanh toán HĐ xuất khẩu', 25000, 500, 0, 'HĐ-EX-005'],
];

function renderCashFundPage() {
    var activeTab = 'vnd';

    renderShell('cashfund',
        /* ----- FILTER ----- */
        '<section class="tp-card p-3 mb-2">' +
        '  <div class="filter-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-filter-3-line"></i></div>' +
        '      <p class="tp-section-title">Bộ lọc Sổ quỹ tiền mặt</p>' +
        '    </div>' +
        '    <div class="d-flex gap-2">' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="ff-gear"><i class="ri-settings-3-line"></i> Cài đặt bộ lọc</button>' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-toggle"><i class="ri-equalizer-line"></i> Tìm kiếm nâng cao</button>' +
        '      <button type="button" class="v2-btn v2-btn--secondary btn-compact" id="f-hide" title="Ẩn / hiện toàn bộ khu vực bộ lọc"><i class="ri-eye-off-line"></i> Ẩn bộ lọc</button>' +
        '    </div>' +
        '  </div>' +
        /* Thân bộ lọc — ẩn/hiện toàn bộ qua nút f-hide (trạng thái lưu localStorage) */
        '  <div id="filter-body">' +
        /* Ô tìm nhanh + nút Tìm kiếm / Nhập lại cùng một hàng (nút bên phải) */
        '  <div class="quick-search-row">' +
        '    <div class="quick-search">' +
        '      <i class="ri-search-line"></i>' +
        '      <input class="form-control form-control-sm" id="f-search" placeholder="Tìm theo Số phiếu, Diễn giải, TK đối ứng">' +
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
        '        <select class="form-control form-control-sm f-adv" id="f-company">' +
                Object.keys(FUND_OPEN).map(function (c) { return '<option value="' + c + '"' + (c === 'TPE' ? ' selected' : '') + '>' + c + ' — ' + ORG[c].name + '</option>'; }).join('') +
        '        </select></div>' +
        '      <div class="col-md-3" data-ff="f-kind"><label class="tp-label">Loại phiếu</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-kind"><option value="">— Tất cả —</option><option value="thu">Phiếu thu</option><option value="chi">Phiếu chi</option></select></div>' +
        '      <div class="col-md-3" data-ff="f-tk"><label class="tp-label">TK đối ứng</label>' +
        '        <select class="form-control form-control-sm f-adv" id="f-tk"><option value="">— Tất cả —</option>' +
                [...new Set(FUND_VND.map(function (r) { return r[FV.tk]; }))].sort().map(function (t) { return '<option value="' + t + '">' + t + '</option>'; }).join('') +
        '        </select></div>' +
        '    </div>' +
        '  </div>' +
        '  </div>' +
        '</section>' +

        '<section class="tp-card p-3">' +
        '  <div class="table-card-header">' +
        '    <div class="filter-header-left">' +
        '      <div class="tp-icon-chip"><i class="ri-money-dollar-box-line"></i></div>' +
        '      <div><h5 id="fund-title">Sổ quỹ tiền mặt</h5>' +
        '      <p class="tp-section-subtitle" id="fund-sub"></p></div>' +
        '    </div>' +
        '    <div class="table-actions">' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-print"><i class="ri-printer-line"></i> In sổ quỹ</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-excel"><i class="ri-file-excel-2-line"></i> Xuất Excel</button>' +
        '      <button type="button" class="v2-btn v2-btn--sm v2-btn--secondary" id="btn-cols" title="Chọn cột hiển thị trên bảng (áp dụng cho tab Sổ quỹ VNĐ)"><i class="ri-layout-column-line"></i> Cấu hình cột</button>' +
        '    </div>' +
        '  </div>' +
        '  <ul class="nav-tabs">' +
        '    <li><button type="button" class="nav-link active" data-fund="vnd"><i class="ri-cash-line"></i>Sổ quỹ VNĐ (S04a-DN)</button></li>' +
        '    <li><button type="button" class="nav-link" data-fund="usd"><i class="ri-exchange-dollar-line"></i>Sổ quỹ ngoại tệ USD (S04b-DN)</button></li>' +
        '    <li><button type="button" class="nav-link" data-fund="recon"><i class="ri-checkbox-multiple-line"></i>Đối chiếu 3 số dư & tổng hợp</button></li>' +
        '  </ul>' +
        '  <div id="fund-body"></div>' +
        '</section>' +

        '<div class="modal-backdrop-demo" id="print-modal"><div class="modal-dialog" style="max-width:960px">' +
        '  <div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-printer-line"></i></span><span id="print-title-label">In sổ quỹ</span></h5>' +
        '  <button type="button" class="close" onclick="closeModal(\'print-modal\')">×</button></div>' +
        '  <div class="modal-body" id="print-preview" style="max-height:70vh"></div>' +
        '  <div class="modal-footer">' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--primary" id="btn-do-print"><i class="ri-printer-line"></i> In</button>' +
        '    <button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'print-modal\')"><i class="ri-close-line"></i> Đóng</button>' +
        '  </div>' +
        '</div></div>' +
        '<div id="print-area"></div>');

    function val(id) { return document.getElementById(id).value; }
    function company() { return val('f-company'); }

    function vndRows() { // dòng quỹ VND theo bộ lọc (giữ nguyên thứ tự ngày để tính tồn)
        var kw = val('f-search').toLowerCase().trim();
        return FUND_VND.filter(function (r) { return r[FV.company] === company(); })
            .sort(function (a, b) { return a[FV.dateGS] < b[FV.dateGS] ? -1 : 1; })
            .filter(function (r) {
                if (val('f-kind') === 'thu' && !r[FV.thu]) return false;
                if (val('f-kind') === 'chi' && !r[FV.chi]) return false;
                if (val('f-tk') && r[FV.tk] !== val('f-tk')) return false;
                if (kw && (r[FV.pt] + ' ' + r[FV.pc] + ' ' + r[FV.desc] + ' ' + r[FV.tk]).toLowerCase().indexOf(kw) === -1) return false;
                return true;
            });
    }
    function fullVndRows() { // toàn bộ dòng của công ty (tính tồn quỹ realtime — không phụ thuộc filter phụ)
        return FUND_VND.filter(function (r) { return r[FV.company] === company(); })
            .sort(function (a, b) { return a[FV.dateGS] < b[FV.dateGS] ? -1 : 1; });
    }

    /* ---------- Cấu hình cột tab Sổ quỹ VNĐ (header 1 hàng, render động) ----------
       8 cột đầu là cột chuẩn theo mẫu S04a-DN → bắt buộc, cố định đầu bảng;
       cột kiểm soát ERP (TK đối ứng) là cột mở rộng tùy chọn.
       QUYẾT ĐỊNH: nút "Cấu hình cột" chỉ áp dụng cho bảng tab VNĐ — tab USD giữ
       nguyên bộ cột song song USD/quy VNĐ cố định (mẫu S04b không cho ẩn cột). */
    var FUND_COLUMNS = [
        { key: 'dateGS', label: 'Ngày ghi sổ', always: true },
        { key: 'dateCT', label: 'Ngày CT', always: true },
        { key: 'loai', label: 'Loại phiếu', cls: 'text-center', always: true },
        { key: 'ct', label: 'Số chứng từ', cls: 'text-center', always: true },
        { key: 'desc', label: 'Diễn giải', style: 'min-width:230px', always: true },
        { key: 'requester', label: 'Người yêu cầu', style: 'min-width:150px', always: true },
        { key: 'preparer', label: 'Người lập phiếu', style: 'min-width:160px', always: true },
        { key: 'receiver', label: 'Người nhận / nộp tiền', style: 'min-width:170px', always: true },
        { key: 'thu', label: 'Thu<br>(Nợ 111)', cls: 'text-right', always: true },
        { key: 'chi', label: 'Chi<br>(Có 111)', cls: 'text-right', always: true },
        { key: 'bal', label: 'Tồn quỹ', cls: 'text-right', always: true },
        { key: 'tk', label: 'TK đối ứng', cls: 'text-center' },
    ];
    var colCfg = setupColumnConfig({
        storageKey: 'demo-cashfund-columns',
        btnId: 'btn-cols',
        columns: FUND_COLUMNS,
        fixedNote: 'Các cột chuẩn mẫu S04a-DN + Loại phiếu, Số chứng từ và thông tin người (yêu cầu / lập / nhận–nộp) là <b>cố định</b>; chỉ <b>TK đối ứng</b> là cột tùy chọn (áp dụng cho tab Sổ quỹ VNĐ).',
        /* Đổi cấu hình cột → header tab VNĐ phải render lại (kèm gắn lại icon sort).
           Reset fundSkeleton để draw() dựng lại khung; vndSort tự reset trong renderVndSkeleton
           (bao trùm cả trường hợp cột đang sort bị ẩn). */
        onChange: function () { if (activeTab === 'vnd') fundSkeleton = null; draw(); },
    });

    /* ---------- Phân trang dùng chung 1 pager cho tab VNĐ + USD ----------
       Container #fund-pager render lại bên trong fund-body theo từng tab;
       signature gồm activeTab + mọi giá trị lọc → đổi tab / đổi lọc tự về trang 1.
       Tab "Đối chiếu & tổng hợp" KHÔNG phân trang (không render container). */
    var pager = createPager({ storageKey: 'demo-cashfund-pagesize', containerSel: '#fund-pager', onChange: function () { draw(); } });
    function filterSignature() {
        /* Nối thêm sort của tab đang xem → bấm sort đổi signature → pager tự về trang 1 */
        var sort = activeTab === 'vnd' ? vndSort : (activeTab === 'usd' ? usdSort : null);
        return activeTab + '|' + ['f-search', 'f-period', 'f-company', 'f-kind', 'f-tk'].map(val).join('|') +
            '|' + JSON.stringify(sort);
    }

    /* ---------- Sort theo cột (áp cho tab VNĐ + tab USD; tab Đối chiếu KHÔNG áp sort) ----------
       QUYẾT ĐỊNH: mỗi tab giữ 1 biến sort riêng (vndSort / usdSort), nhưng khi header của tab
       render lại (vào lại tab / đổi cấu hình cột) thì RESET về null (thứ tự chuẩn của sổ) —
       vì setupColumnSort khởi tạo chu trình click mới từ đầu mỗi lần gắn lên thead, nếu giữ
       sort cũ thì icon và vòng xoay tăng→giảm→bỏ sẽ lệch trạng thái thực. Cột sort đang bị ẩn
       qua "Cấu hình cột" cũng tự về null theo cơ chế reset này. */
    var vndSort = null;      // {key, dir:'asc'|'desc'} | null — sort tab Sổ quỹ VNĐ
    var usdSort = null;      // {key, dir:'asc'|'desc'} | null — sort tab Sổ quỹ USD
    var fundSkeleton = null; // khung bảng (thead + tbody/tfoot rỗng) đang có trong #fund-body: 'vnd' | 'usd' | null

    /* Sort danh sách dòng VNĐ theo cột — CHỈ đổi THỨ TỰ HIỂN THỊ.
       LƯU Ý NGHIỆP VỤ: cột "Tồn quỹ" của từng phiếu GIỮ NGUYÊN giá trị realtime đã tính
       lũy kế theo trình tự thời gian trên TOÀN BỘ sổ (balMap tính trên `full` TRƯỚC khi
       sort/lọc/phân trang) — sort không tính lại tồn; dòng SDĐK / CỘNG PS / SDCK không đổi. */
    var VND_SORT_NUMERIC = { thu: 1, chi: 1, bal: 1 }; // cột số; còn lại so sánh chuỗi (ngày ISO yyyy-mm-dd so chuỗi vẫn đúng)
    function applyVndSort(list, balMap) {
        if (!vndSort) return list;
        var asc = vndSort.dir === 'asc' ? 1 : -1;
        var orig = new Map(); // thứ tự chuẩn của sổ (theo ngày) để tie-break ổn định
        list.forEach(function (r, i) { orig.set(r, i); });
        function keyVal(r) { return vndSort.key === 'bal' ? balMap.get(r) : r[FV[vndSort.key]]; }
        return list.slice().sort(function (a, b) {
            var x = keyVal(a), y = keyVal(b);
            if (VND_SORT_NUMERIC[vndSort.key]) return (x - y) * asc || orig.get(a) - orig.get(b);
            if (x === y) return orig.get(a) - orig.get(b);
            return (x < y ? -1 : 1) * asc;
        });
    }

    /* Sort tab USD: sort trên mảng `lines` ĐÃ precompute tồn song song USD / quy VNĐ theo
       trình tự thời gian → sort chỉ đổi thứ tự hiển thị, tồn từng dòng giữ nguyên. */
    var USD_SORT_NUMERIC = { rate: 1, thuU: 1, chiU: 1, tonU: 1, thuV: 1, chiV: 1, tonV: 1 };
    function usdKeyVal(l, key) {
        switch (key) {
            case 'dateGS': return l.r[0];
            case 'dateCT': return l.r[1];
            case 'pt': return l.r[2];
            case 'pc': return l.r[3];
            case 'desc': return l.r[4];
            case 'rate': return l.r[5];
            case 'thuU': return l.r[6];
            case 'chiU': return l.r[7];
            case 'tonU': return l.usd;
            case 'thuV': return l.thuV;
            case 'chiV': return l.chiV;
            case 'tonV': return l.vnd;
            default: return l.r[8]; // ghi chú
        }
    }
    function applyUsdSort(lines) {
        if (!usdSort) return lines;
        var asc = usdSort.dir === 'asc' ? 1 : -1;
        return lines.slice().sort(function (a, b) {
            var x = usdKeyVal(a, usdSort.key), y = usdKeyVal(b, usdSort.key);
            if (USD_SORT_NUMERIC[usdSort.key]) return (x - y) * asc || a.idx - b.idx;
            if (x === y) return a.idx - b.idx;
            return (x < y ? -1 : 1) * asc;
        });
    }

    /* (4 thẻ tổng quan cũ đã bỏ — thông tin đưa về bảng: SDĐK/SDCK là dòng trong sổ,
       số phiếu thu/chi trong label dòng CỘNG PHÁT SINH, thủ quỹ ở subtitle bảng) */

    /* ---------- Tab 1: Sổ quỹ VND ---------- */
    /* Render 1 ô theo cấu hình cột (balMap: tồn quỹ realtime tính sẵn trên toàn bộ sổ) */
    function vndCellHTML(r, c, balMap) {
        switch (c.key) {
            case 'dateGS': return '<td class="num">' + fmtDate(r[FV.dateGS]) + '</td>';
            case 'dateCT': return '<td class="num">' + fmtDate(r[FV.dateCT]) + '</td>';
            case 'loai': return '<td class="text-center"><span class="status-pill ' + (fundIsThu(r) ? 'st-done' : 'st-cancel') + '">' + (fundIsThu(r) ? 'Phiếu thu' : 'Phiếu chi') + '</span></td>';
            case 'ct': return '<td class="text-center"><b>' + fundCtNo(r) + '</b></td>';
            case 'desc': return '<td style="white-space:normal">' + r[FV.desc] + '</td>';
            case 'requester': return '<td>' + fundRequester(r) + '</td>';
            case 'preparer': return '<td>' + fundPreparer(r) + '</td>';
            case 'receiver': return '<td>' + fundReceiver(r) + '</td>';
            case 'thu': return '<td class="text-right num">' + (r[FV.thu] ? fmtMoney(r[FV.thu]) : '') + '</td>';
            case 'chi':
                // Cảnh báo chi tiền mặt ≥ 5tr cho hóa đơn HHDV (không áp dụng: nộp/rút NH 1121, tạm ứng 141, chi lương 334)
                var warnCash = r[FV.chi] >= 5000000 && ['1121', '141', '334'].indexOf(r[FV.tk]) === -1
                    ? ' <span class="status-pill st-paused" title="Chi tiền mặt ≥ 5 triệu cho hóa đơn hàng hóa/dịch vụ — theo Luật Thuế GTGT 48/2024/QH15 & NĐ 181/2025/NĐ-CP (hiệu lực 01/07/2025) KHÔNG được khấu trừ thuế GTGT / tính chi phí được trừ. Cần thanh toán không dùng tiền mặt.">⚠ ≥5tr TM</span>' : '';
                return '<td class="text-right num">' + (r[FV.chi] ? fmtMoney(r[FV.chi]) + warnCash : '') + '</td>';
            case 'bal': return '<td class="text-right num" style="font-weight:700">' + fmtMoney(balMap.get(r)) + '</td>';
            default: return '<td class="text-center">' + r[FV.tk] + '</td>'; // tk
        }
    }
    /* Render KHUNG tab VNĐ (note-box + thead theo cấu hình cột + tbody/tfoot rỗng + pager + dòng kiểm tra).
       Tách khỏi drawVnd (như renderHeader của journal.js): chỉ gọi khi vào tab / đổi cấu hình cột
       → setupColumnSort gắn 1 lần lên thead, bấm sort chỉ vẽ lại tbody nên icon active giữ đúng. */
    function renderVndSkeleton() {
        vndSort = null; // header mới → chu trình sort của helper bắt đầu lại → về thứ tự chuẩn của sổ
        fundSkeleton = 'vnd';
        var visCols = colCfg.visible();
        document.getElementById('fund-body').innerHTML =
            '<div class="note-box"><i class="ri-information-line"></i> Sổ quỹ do <b>Thủ quỹ</b> ghi và ký chịu trách nhiệm (khác Sổ Cái TK 111 do kế toán ghi). Cột <b>Tồn quỹ</b> cập nhật realtime sau từng phiếu. <b>Từ 01/07/2025</b> (Luật Thuế GTGT 48/2024/QH15 &amp; NĐ 181/2025/NĐ-CP): hóa đơn mua hàng hóa/dịch vụ <b>từ 5 triệu đồng trở lên</b> (gồm VAT) phải thanh toán không dùng tiền mặt mới được khấu trừ thuế GTGT / tính chi phí được trừ — kể cả mua cùng NCC nhiều lần trong ngày cộng lại ≥ 5tr; phiếu chi tiền mặt vi phạm sẽ cảnh báo ⚠. Tồn dự kiến &lt; 0 → hệ thống chặn tạo phiếu chi. <b>ERP chỉ lấy các phiếu thu/chi ĐÃ ĐƯỢC DUYỆT vào sổ quỹ và báo cáo.</b></div>' +
            '<div class="table-wrapper scrollbar-thin"><table class="data-table" id="fund-tbl">' +
            /* Header 1 hàng render theo cấu hình cột (đã gộp nhóm cũ vào tên cột) */
            '<thead><tr>' + visCols.map(function (c) {
                return '<th' + (c.cls ? ' class="' + c.cls + '"' : '') + (c.style ? ' style="' + c.style + '"' : '') + '>' + c.label + '</th>';
            }).join('') + '</tr></thead>' +
            '<tbody id="fund-tbody"></tbody><tfoot id="fund-tfoot"></tfoot>' +
            '</table></div>' +
            '<div class="table-pager" id="fund-pager"></div>' +
            '<div class="d-flex align-center gap-2 mt-2" id="fund-check"></div>';
        /* Gắn icon sort cho TẤT CẢ cột đang hiện (mảng cols đúng thứ tự th) */
        setupColumnSort({
            tableSel: '#fund-tbl',
            headRow: 1,
            cols: visCols.map(function (c) { return { key: c.key }; }),
            onChange: function (s) { vndSort = s; drawVnd(); },
        });
    }
    function drawVnd() {
        var full = fullVndRows();
        var shown = vndRows();
        var filteredMode = shown.length !== full.length;
        var opening = FUND_OPEN[company()];
        // QUAN TRỌNG: tồn quỹ realtime tính lũy kế trên TOÀN BỘ dòng (map theo reference)
        // TRƯỚC khi lọc/phân trang → tồn từng dòng không đổi khi ẩn dòng hay chuyển trang
        var balMap = new Map();
        var bal = opening, totThu = 0, totChi = 0, thuCount = 0, chiCount = 0;
        full.forEach(function (r) {
            bal += r[FV.thu] - r[FV.chi]; balMap.set(r, bal);
            totThu += r[FV.thu]; totChi += r[FV.chi];
            if (r[FV.thu]) thuCount++;
            if (r[FV.chi]) chiCount++;
        });
        var closing = opening + totThu - totChi;

        var visCols = colCfg.visible();
        /* Dòng tổng: nhãn span các cột TRƯỚC "Thu"; Thu/Chi/Tồn cố định; phần sau "Tồn" span nốt.
           Tính động theo cấu hình cột (đã thêm Loại phiếu / các cột Người). */
        var keys = visCols.map(function (c) { return c.key; });
        var lead = keys.indexOf('thu');                          // số cột nhãn (trước Thu)
        var trail = visCols.length - keys.indexOf('bal') - 1;    // số cột sau Tồn quỹ
        var trailTd = trail > 0 ? '<td colspan="' + trail + '"></td>' : '';
        var openRow = '<tr class="row-carry"><td colspan="' + lead + '"><b>SỐ DƯ ĐẦU KỲ (01/01/2026)</b></td><td></td><td></td>' +
            '<td class="text-right num"><b>' + fmtMoney(opening) + '</b></td>' + trailTd + '</tr>';
        var totalRow = '<tr class="row-total"><td colspan="' + lead + '">CỘNG PHÁT SINH KỲ' + (filteredMode ? ' (toàn sổ — bộ lọc chỉ ẩn dòng hiển thị)' : ' (' + thuCount + ' phiếu thu · ' + chiCount + ' phiếu chi)') + '</td>' +
            '<td class="text-right num">' + fmtMoney(totThu) + '</td><td class="text-right num">' + fmtMoney(totChi) + '</td>' +
            '<td class="text-right num"></td>' + trailTd + '</tr>';
        var closeRow = '<tr class="row-total"><td colspan="' + lead + '">SỐ DƯ CUỐI KỲ (31/01/2026)</td><td></td><td></td>' +
            '<td class="text-right num">' + fmtMoney(closing) + '</td>' + trailTd + '</tr>';

        /* Sort TRƯỚC phân trang, SAU khi đã có tồn quỹ từng dòng (balMap) — sort chỉ đổi thứ tự
           hiển thị, tồn realtime từng phiếu và SDĐK / Cộng PS / SDCK vẫn theo toàn bộ sổ */
        var sorted = applyVndSort(shown, balMap);
        var pageRows = pager.paginate(sorted, filterSignature());
        var body = pageRows.map(function (r) {
            return '<tr>' + visCols.map(function (c) { return vndCellHTML(r, c, balMap); }).join('') + '</tr>';
        }).join('');

        /* Chỉ đổ lại tbody / tfoot / dòng kiểm tra — thead (đã gắn sort) nằm trong skeleton, không render lại */
        document.getElementById('fund-tbody').innerHTML =
            openRow + totalRow + closeRow + (shown.length ? body : '<tr><td colspan="' + visCols.length + '"><div class="empty-state"><div class="es-icon"><i class="ri-inbox-2-line"></i></div>Không có phiếu phù hợp bộ lọc.</div></td></tr>');
        document.getElementById('fund-tfoot').innerHTML = totalRow + closeRow;
        document.getElementById('fund-check').innerHTML =
            '<span class="tp-small-text">Kiểm tra: SDĐK + Cộng thu − Cộng chi = SDCK → ' +
            fmtMoney(opening) + ' + ' + fmtMoney(totThu) + ' − ' + fmtMoney(totChi) + ' = ' + fmtMoney(closing) + '</span> ' +
            '<span class="status-pill st-done"><i class="ri-checkbox-circle-line"></i>CÂN ĐỐI</span>';
        applyStickyTotals('#fund-tbl');
        pager.render();
    }

    /* ---------- Tab 2: Sổ quỹ USD ---------- */
    /* Render KHUNG tab USD (note-box + thead cố định + tbody/tfoot rỗng + pager + dòng kiểm tra) —
       như renderVndSkeleton: chỉ gọi khi vào tab (bộ cột S04b cố định, không có cấu hình cột)
       để setupColumnSort gắn 1 lần, icon active giữ đúng khi bấm sort. */
    function renderUsdSkeleton() {
        usdSort = null; // header mới → chu trình sort bắt đầu lại → về thứ tự chuẩn của sổ
        fundSkeleton = 'usd';
        document.getElementById('fund-body').innerHTML =
            '<div class="note-box"><i class="ri-information-line"></i> Sổ quỹ ngoại tệ theo dõi <b>song song</b> nguyên tệ (USD) và quy đổi VNĐ theo tỷ giá tại thời điểm phát sinh. Cuối kỳ đánh giá lại: Tồn USD × tỷ giá cuối kỳ (VD 26.000) — chênh lệch với "Tồn VNĐ" hạch toán <b>TK 413</b> (chênh lệch tỷ giá). Kiểm quỹ đột xuất: đếm USD trong két khớp với Tồn USD trên sổ.</div>' +
            '<div class="table-wrapper scrollbar-thin"><table class="data-table" id="fund-tbl">' +
            /* Header 1 hàng — nhãn nhóm cũ ("Nguyên tệ (USD)", "Quy đổi VNĐ") gộp vào tên cột */
            '<thead>' +
            '<tr><th>Ngày ghi sổ</th><th>Ngày CT</th><th class="text-center">Số PT</th><th class="text-center">Số PC</th><th style="min-width:230px">Diễn giải</th>' +
            '<th class="text-right">Tỷ giá<br>(VND/USD)</th>' +
            '<th class="text-right">Thu (USD)</th><th class="text-right">Chi (USD)</th><th class="text-right">Tồn (USD)</th>' +
            '<th class="text-right">Thu quy VNĐ</th><th class="text-right">Chi quy VNĐ</th><th class="text-right">Tồn quy VNĐ</th><th>Ghi chú</th></tr>' +
            '</thead>' +
            '<tbody id="fund-tbody"></tbody><tfoot id="fund-tfoot"></tfoot>' +
            '</table></div>' +
            '<div class="table-pager" id="fund-pager"></div>' +
            '<div class="d-flex align-center gap-2 mt-2" id="fund-check"></div>';
        /* Mảng cols đúng thứ tự 13 th của bảng S04b — tất cả cột đều sort được */
        setupColumnSort({
            tableSel: '#fund-tbl',
            headRow: 1,
            cols: [{ key: 'dateGS' }, { key: 'dateCT' }, { key: 'pt' }, { key: 'pc' }, { key: 'desc' },
                { key: 'rate' }, { key: 'thuU' }, { key: 'chiU' }, { key: 'tonU' },
                { key: 'thuV' }, { key: 'chiV' }, { key: 'tonV' }, { key: 'note' }],
            onChange: function (s) { usdSort = s; drawUsd(); },
        });
    }
    function drawUsd() {
        var usd = FUND_USD_OPEN.usd, vnd = FUND_USD_OPEN.vnd;
        var totTU = 0, totCU = 0, totTV = 0, totCV = 0;
        // Tính tồn song song USD / quy VNĐ trên TOÀN BỘ danh sách TRƯỚC khi sort/phân trang
        // → tồn từng dòng không đổi khi sort hay chuyển trang; Cộng PS / SDCK vẫn theo toàn bộ
        var lines = FUND_USD.map(function (r, i) {
            var thuV = r[6] * r[5], chiV = r[7] * r[5];
            usd += r[6] - r[7]; vnd += thuV - chiV;
            totTU += r[6]; totCU += r[7]; totTV += thuV; totCV += chiV;
            return { r: r, idx: i, thuV: thuV, chiV: chiV, usd: usd, vnd: vnd }; // idx: thứ tự gốc để tie-break khi sort
        });
        /* Sort TRƯỚC phân trang — chỉ đổi thứ tự hiển thị các dòng đã precompute */
        var pageLines = pager.paginate(applyUsdSort(lines), filterSignature());
        var body = pageLines.map(function (l) {
            var r = l.r;
            return '<tr>' +
                '<td class="num">' + fmtDate(r[0]) + '</td><td class="num">' + fmtDate(r[1]) + '</td>' +
                '<td class="text-center"><b>' + (r[2] || '') + '</b></td><td class="text-center"><b>' + (r[3] || '') + '</b></td>' +
                '<td style="white-space:normal">' + r[4] + '</td>' +
                '<td class="text-right num">' + fmtMoney(r[5]) + '</td>' +
                '<td class="text-right num">' + (r[6] ? fmtMoney(r[6]) : '') + '</td>' +
                '<td class="text-right num">' + (r[7] ? fmtMoney(r[7]) : '') + '</td>' +
                '<td class="text-right num" style="font-weight:700">' + fmtMoney(l.usd) + '</td>' +
                '<td class="text-right num">' + (l.thuV ? fmtMoney(l.thuV) : '') + '</td>' +
                '<td class="text-right num">' + (l.chiV ? fmtMoney(l.chiV) : '') + '</td>' +
                '<td class="text-right num" style="font-weight:700">' + fmtMoney(l.vnd) + '</td>' +
                '<td class="tp-small-text">' + r[8] + '</td>' +
                '</tr>';
        }).join('');
        var openRow = '<tr class="row-carry"><td colspan="5"><b>SỐ DƯ ĐẦU KỲ (01/01/2026)</b></td><td></td><td></td><td></td>' +
            '<td class="text-right num"><b>' + fmtMoney(FUND_USD_OPEN.usd) + '</b></td><td></td><td></td>' +
            '<td class="text-right num"><b>' + fmtMoney(FUND_USD_OPEN.vnd) + '</b></td><td></td></tr>';
        var totalRow = '<tr class="row-total"><td colspan="5">CỘNG PHÁT SINH KỲ</td><td></td>' +
            '<td class="text-right num">' + fmtMoney(totTU) + '</td><td class="text-right num">' + fmtMoney(totCU) + '</td><td></td>' +
            '<td class="text-right num">' + fmtMoney(totTV) + '</td><td class="text-right num">' + fmtMoney(totCV) + '</td><td></td><td></td></tr>';
        var closeRow = '<tr class="row-total"><td colspan="5">SỐ DƯ CUỐI KỲ (31/01/2026)</td><td></td><td></td><td></td>' +
            '<td class="text-right num">' + fmtMoney(usd) + '</td><td></td><td></td>' +
            '<td class="text-right num">' + fmtMoney(vnd) + '</td><td></td></tr>';
        /* Chỉ đổ lại tbody / tfoot / dòng kiểm tra — thead (đã gắn sort) nằm trong skeleton, không render lại */
        document.getElementById('fund-tbody').innerHTML = openRow + totalRow + closeRow + body;
        document.getElementById('fund-tfoot').innerHTML = totalRow + closeRow;
        document.getElementById('fund-check').innerHTML =
            '<span class="tp-small-text">SDĐK 4.000 USD → SDCK ' + fmtMoney(usd) + ' USD · Thủ quỹ ngoại tệ: Trần Văn Em</span> ' +
            '<span class="status-pill st-done"><i class="ri-checkbox-circle-line"></i>CÂN ĐỐI</span>';
        applyStickyTotals('#fund-tbl');
        pager.render();
    }

    /* ---------- Tab 3: Đối chiếu 3 số dư & tổng hợp ---------- */
    function drawRecon() {
        var daily = [
            ['02/01/2026', 25000000, 3000000, 0], ['03/01/2026', 28000000, 0, 3500000],
            ['05/01/2026', 24500000, 66000000, 0], ['06/01/2026', 90500000, 0, 55000000],
            ['08/01/2026', 35500000, 200000000, 0],
        ];
        var dailyRows = daily.map(function (d) {
            var sdck = d[1] + d[2] - d[3];
            return '<tr><td class="num">' + d[0] + '</td><td class="text-right num">' + fmtMoney(d[1]) + '</td>' +
                '<td class="text-right num">' + fmtMoney(d[2]) + '</td><td class="text-right num">' + fmtMoney(d[3]) + '</td>' +
                '<td class="text-right num" style="font-weight:700">' + fmtMoney(sdck) + '</td>' +
                '<td class="text-right num">' + fmtMoney(sdck) + '</td><td class="text-right num">0</td>' +
                '<td class="text-right num">' + fmtMoney(sdck) + '</td><td class="text-right num">0</td>' +
                '<td class="text-center"><span class="status-pill st-done">✓ Khớp</span></td></tr>';
        }).join('');
        var monthly = [
            ['TPE', 'Quỹ VND', 25000000, 1000000000, 995000000],
            ['TPE', 'Quỹ USD (quy VND)', 100000000, 37500000, 12500000],
            ['TPSG', 'Quỹ VND', 12000000, 200000000, 197000000],
            ['TPHP', 'Quỹ VND', 6000000, 150000000, 148000000],
        ];
        var mTot = { sdk: 0, thu: 0, chi: 0, sdck: 0, vnd: 0, usd: 0 };
        var monthlyRows = monthly.map(function (m) {
            var sdck = m[2] + m[3] - m[4];
            mTot.sdk += m[2]; mTot.thu += m[3]; mTot.chi += m[4]; mTot.sdck += sdck;
            if (m[1].indexOf('USD') !== -1) mTot.usd += sdck; else mTot.vnd += sdck;
            return '<tr><td><b>' + m[0] + '</b></td><td>' + m[1] + '</td>' +
                '<td class="text-right num">' + fmtMoney(m[2]) + '</td><td class="text-right num">' + fmtMoney(m[3]) + '</td>' +
                '<td class="text-right num">' + fmtMoney(m[4]) + '</td>' +
                '<td class="text-right num" style="font-weight:700">' + fmtMoney(sdck) + '</td>' +
                '<td class="text-right num">' + fmtMoney(sdck) + '</td><td class="text-right num">' + fmtMoney(sdck) + '</td>' +
                '<td class="text-right num">0</td><td class="text-center"><span class="status-pill st-done">✓ Khớp</span></td></tr>';
        }).join('');
        document.getElementById('fund-body').innerHTML =
            '<div class="note-box"><i class="ri-information-line"></i> Nguyên tắc <b>"3 số dư phải khớp"</b>: SD Sổ quỹ (thủ quỹ ghi) = SD Sổ Cái TK 111 (kế toán post) = SD Kiểm quỹ thực tế (đếm tiền trong két). Thiếu → thủ quỹ bồi thường; thừa → lập biên bản, hạch toán TK 3388. ERP chạy đối chiếu tự động hằng ngày.</div>' +
            '<div class="filter-header-left mb-2"><div class="tp-icon-chip"><i class="ri-calendar-check-line"></i></div><p class="tp-section-title">A. Đối chiếu theo ngày (TPE — quỹ VND, 5 ngày đầu tháng)</p></div>' +
            '<div class="table-wrapper"><table class="data-table"><thead><tr>' +
            '<th>Ngày</th><th class="text-right">SDĐK ngày (A)</th><th class="text-right">Tổng thu (B)</th><th class="text-right">Tổng chi (C)</th>' +
            '<th class="text-right">SDCK Sổ quỹ<br>(D = A+B−C)</th><th class="text-right">SDCK Sổ Cái (E)</th><th class="text-right">Chênh (D−E)</th>' +
            '<th class="text-right">Kiểm quỹ thực tế (F)</th><th class="text-right">Chênh (D−F)</th><th class="text-center">Trạng thái</th>' +
            '</tr></thead><tbody>' + dailyRows + '</tbody></table></div>' +
            '<div class="filter-header-left mb-2 mt-3"><div class="tp-icon-chip"><i class="ri-building-line"></i></div><p class="tp-section-title">B. Đối chiếu cả tháng 01/2026 — toàn bộ pháp nhân</p></div>' +
            '<div class="table-wrapper"><table class="data-table"><thead><tr>' +
            '<th>Pháp nhân</th><th>Loại quỹ</th><th class="text-right">SDĐK</th><th class="text-right">Tổng thu</th><th class="text-right">Tổng chi</th>' +
            '<th class="text-right">SDCK Sổ quỹ</th><th class="text-right">SDCK Sổ Cái</th><th class="text-right">Kiểm quỹ thực tế</th><th class="text-right">Chênh lệch</th><th class="text-center">Trạng thái</th>' +
            '</tr></thead><tbody>' + monthlyRows + '</tbody>' +
            /* dòng tổng gộp thông tin 3 thẻ tổng quan cũ: quỹ VNĐ + quỹ USD quy đổi = tổng tập đoàn, khớp BC số dư tiền */
            '<tfoot><tr><td colspan="2">TỔNG TẬP ĐOÀN — quỹ VNĐ ' + fmtMoney(mTot.vnd) + ' + quỹ USD quy đổi ' + fmtMoney(mTot.usd) + '</td><td class="text-right num">' + fmtMoney(mTot.sdk) + '</td>' +
            '<td class="text-right num">' + fmtMoney(mTot.thu) + '</td><td class="text-right num">' + fmtMoney(mTot.chi) + '</td>' +
            '<td class="text-right num">' + fmtMoney(mTot.sdck) + '</td><td class="text-right num">' + fmtMoney(mTot.sdck) + '</td>' +
            '<td class="text-right num">' + fmtMoney(mTot.sdck) + '</td><td class="text-right num">0</td>' +
            '<td class="text-center"><span class="status-pill st-done"><i class="ri-checkbox-circle-line"></i>Khớp BC số dư tiền</span></td></tr>' +
            '</tfoot></table></div>';
    }

    function draw() {
        var m = { vnd: ['Sổ quỹ tiền mặt VNĐ — ' + company(), 'Mẫu S04a-DN (TT 99/2025/TT-BTC) · Kỳ: Tháng 01/2026 · Thủ quỹ: ' + FUND_KEEPER[company()] + ' · Đơn vị tính: VNĐ'],
                  usd: ['Sổ quỹ tiền mặt ngoại tệ (USD) — TPE', 'Mẫu S04b-DN (TT 99/2025/TT-BTC) · Kỳ: Tháng 01/2026 · Thủ quỹ ngoại tệ: Trần Văn Em · Đơn vị: USD & VNĐ'],
                  recon: ['Đối chiếu 3 số dư & tổng hợp quỹ tập đoàn', 'Sổ quỹ = Sổ Cái TK 111 = Kiểm quỹ thực tế · Tháng 01/2026'] }[activeTab];
        document.getElementById('fund-title').textContent = m[0];
        document.getElementById('fund-sub').textContent = m[1];
        /* Khung (thead + sort) chỉ dựng lại khi đổi tab / đổi cấu hình cột;
           các lần draw khác (lọc, phân trang, bấm sort) chỉ đổ lại phần thân bảng */
        if (activeTab === 'vnd') {
            if (fundSkeleton !== 'vnd') renderVndSkeleton();
            drawVnd();
        } else if (activeTab === 'usd') {
            if (company() !== 'TPE') {
                fundSkeleton = null; // không có bảng → quay lại TPE sẽ dựng lại khung
                document.getElementById('fund-body').innerHTML =
                    '<div class="empty-state"><div class="es-icon"><i class="ri-exchange-dollar-line"></i></div>' + company() + ' không có quỹ ngoại tệ. Chỉ TPE (công ty mẹ) mở quỹ USD.</div>';
            } else {
                if (fundSkeleton !== 'usd') renderUsdSkeleton();
                drawUsd();
            }
        } else {
            fundSkeleton = null; // tab đối chiếu render toàn bộ trong drawRecon — KHÔNG áp sort
            drawRecon();
        }
    }

    document.querySelectorAll('[data-fund]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.querySelectorAll('[data-fund]').forEach(function (b) { b.classList.remove('active'); });
            btn.classList.add('active');
            activeTab = btn.dataset.fund;
            draw();
        });
    });

    var collapsed = true;
    document.getElementById('f-toggle').addEventListener('click', function () {
        collapsed = !collapsed;
        document.getElementById('adv-filters').classList.toggle('collapsed', collapsed);
        this.innerHTML = '<i class="' + (collapsed ? 'ri-equalizer-line' : 'ri-arrow-up-s-line') + '"></i> ' + (collapsed ? 'Tìm kiếm nâng cao' : 'Ẩn tìm kiếm nâng cao');
    });

    /* ẩn / hiện toàn bộ khu vực bộ lọc (helper chung, lưu trạng thái theo màn) */
    setupFilterHide({ storageKey: 'demo-filter-cashfund-hidden', btnId: 'f-hide', bodyId: 'filter-body' });
    document.querySelectorAll('.f-adv').forEach(function (el) { el.addEventListener('change', draw); });
    document.getElementById('f-search').addEventListener('keydown', function (e) { if (e.key === 'Enter') draw(); });
    document.getElementById('f-search').addEventListener('input', function () {
        document.getElementById('f-search-clear').style.display = this.value ? 'inline-flex' : 'none';
    });
    document.getElementById('f-search-clear').addEventListener('click', function () { document.getElementById('f-search').value = ''; draw(); });
    document.getElementById('f-go').addEventListener('click', draw);
    document.getElementById('f-clear').addEventListener('click', function () {
        ['f-search', 'f-kind', 'f-tk'].forEach(function (id) { document.getElementById(id).value = ''; });
        document.getElementById('f-company').value = 'TPE';
        draw();
    });
    document.getElementById('btn-excel').addEventListener('click', function () {
        toast('Demo: file Excel sẽ được tải xuống ở bản chính thức', 'info');
    });

    /* ----- In mẫu chuẩn S04a / S04b (chữ ký: Thủ quỹ · KTT · Người đại diện) ----- */
    function printSign() {
        return '<div class="p-note">- Sổ này có …. trang, đánh số từ trang số 01 đến trang ….<br>- Ngày mở sổ: ……………</div>' +
            '<table class="p-sign"><tr>' +
            '<td><b>Thủ quỹ</b><br><i>(Ký, họ tên)</i></td>' +
            '<td><b>Kế toán trưởng</b><br><i>(Ký, họ tên)</i></td>' +
            '<td><i>Ngày ... tháng ... năm ...</i><br><b>Người đại diện theo pháp luật</b><br><i>(Ký, họ tên, đóng dấu)</i></td>' +
            '</tr></table>';
    }
    function printSheetHTML() {
        if (activeTab === 'usd') {
            var usd = FUND_USD_OPEN.usd, vnd = FUND_USD_OPEN.vnd, tTU = 0, tCU = 0, tTV = 0, tCV = 0;
            var body = FUND_USD.map(function (r) {
                var tv = r[6] * r[5], cv = r[7] * r[5];
                usd += r[6] - r[7]; vnd += tv - cv; tTU += r[6]; tCU += r[7]; tTV += tv; tCV += cv;
                return '<tr><td class="pc">' + fmtDate(r[0]) + '</td><td class="pc">' + fmtDate(r[1]) + '</td>' +
                    '<td class="pc">' + (r[2] || '') + '</td><td class="pc">' + (r[3] || '') + '</td><td>' + r[4] + '</td>' +
                    '<td class="pr">' + fmtMoney(r[5]) + '</td>' +
                    '<td class="pr">' + (r[6] ? fmtMoney(r[6]) : '') + '</td><td class="pr">' + (r[7] ? fmtMoney(r[7]) : '') + '</td><td class="pr">' + fmtMoney(usd) + '</td>' +
                    '<td class="pr">' + (tv ? fmtMoney(tv) : '') + '</td><td class="pr">' + (cv ? fmtMoney(cv) : '') + '</td><td class="pr">' + fmtMoney(vnd) + '</td>' +
                    '<td>' + r[8] + '</td></tr>';
            }).join('');
            return '<div class="print-sheet">' +
                '<table class="p-head"><tr><td style="width:55%"><b>Đơn vị:</b> ' + ORG['TPE'].name + '<br><b>Địa chỉ:</b> ……………………………</td>' +
                '<td style="text-align:center"><b>Mẫu số S04b - DN</b><br><i style="font-size:10.5px">(Ban hành theo Thông tư số 99/2025/TT-BTC<br>ngày 17/10/2025 của Bộ Tài chính)</i></td></tr></table>' +
                '<div class="p-title">SỔ QUỸ TIỀN MẶT</div>' +
                '<div class="p-sub">Loại quỹ: Ngoại tệ — USD · Theo dõi cả nguyên tệ và quy đổi VNĐ</div>' +
                '<div class="p-sub">Tháng 01 năm 2026</div>' +
                '<div class="p-unit">Đơn vị tính: USD và VNĐ</div>' +
                '<table class="p-grid" style="font-size:11px"><thead>' +
                '<tr><th rowspan="2">Ngày, tháng<br>ghi sổ</th><th rowspan="2">Ngày, tháng<br>chứng từ</th><th colspan="2">Số hiệu CT</th><th rowspan="2" style="width:22%">Diễn giải</th><th rowspan="2">Tỷ giá</th><th colspan="3">Nguyên tệ (USD)</th><th colspan="3">Quy đổi VNĐ</th><th rowspan="2">Ghi chú</th></tr>' +
                '<tr><th>Thu</th><th>Chi</th><th>Thu</th><th>Chi</th><th>Tồn</th><th>Thu</th><th>Chi</th><th>Tồn</th></tr>' +
                '</thead><tbody>' +
                '<tr><td colspan="5" style="text-align:left"><b>Số dư đầu kỳ</b></td><td></td><td></td><td></td><td class="pr"><b>' + fmtMoney(FUND_USD_OPEN.usd) + '</b></td><td></td><td></td><td class="pr"><b>' + fmtMoney(FUND_USD_OPEN.vnd) + '</b></td><td></td></tr>' +
                body +
                '<tr class="p-total"><td colspan="5" style="text-align:left"><b>Cộng phát sinh trong kỳ</b></td><td></td><td class="pr"><b>' + fmtMoney(tTU) + '</b></td><td class="pr"><b>' + fmtMoney(tCU) + '</b></td><td></td><td class="pr"><b>' + fmtMoney(tTV) + '</b></td><td class="pr"><b>' + fmtMoney(tCV) + '</b></td><td></td><td></td></tr>' +
                '<tr class="p-total"><td colspan="5" style="text-align:left"><b>Số dư cuối kỳ</b></td><td></td><td></td><td></td><td class="pr"><b>' + fmtMoney(usd) + '</b></td><td></td><td></td><td class="pr"><b>' + fmtMoney(vnd) + '</b></td><td></td></tr>' +
                '</tbody></table>' + printSign() + '</div>';
        }
        // S04a VND
        var full = fullVndRows();
        var opening = FUND_OPEN[company()];
        var bal = opening, tThu = 0, tChi = 0;
        var body = full.map(function (r) {
            bal += r[FV.thu] - r[FV.chi]; tThu += r[FV.thu]; tChi += r[FV.chi];
            return '<tr><td class="pc">' + fmtDate(r[FV.dateGS]) + '</td><td class="pc">' + fmtDate(r[FV.dateCT]) + '</td>' +
                '<td class="pc">' + (r[FV.pt] || '') + '</td><td class="pc">' + (r[FV.pc] || '') + '</td><td>' + r[FV.desc] + '</td>' +
                '<td class="pr">' + (r[FV.thu] ? fmtMoney(r[FV.thu]) : '') + '</td>' +
                '<td class="pr">' + (r[FV.chi] ? fmtMoney(r[FV.chi]) : '') + '</td>' +
                '<td class="pr">' + fmtMoney(bal) + '</td></tr>';
        }).join('');
        return '<div class="print-sheet">' +
            '<table class="p-head"><tr><td style="width:55%"><b>Đơn vị:</b> ' + ORG[company()].name + '<br><b>Địa chỉ:</b> ……………………………</td>' +
            '<td style="text-align:center"><b>Mẫu số S04a - DN</b><br><i style="font-size:10.5px">(Ban hành theo Thông tư số 99/2025/TT-BTC<br>ngày 17/10/2025 của Bộ Tài chính)</i></td></tr></table>' +
            '<div class="p-title">SỔ QUỸ TIỀN MẶT</div>' +
            '<div class="p-sub">Loại quỹ: Tiền Việt Nam đồng (VNĐ) · Tháng 01 năm 2026</div>' +
            '<div class="p-unit">Đơn vị tính: VNĐ</div>' +
            '<table class="p-grid"><thead>' +
            '<tr><th rowspan="2">Ngày, tháng<br>ghi sổ</th><th rowspan="2">Ngày, tháng<br>chứng từ</th><th colspan="2">Số hiệu chứng từ</th><th rowspan="2" style="width:30%">Diễn giải</th><th colspan="3">Số tiền</th></tr>' +
            '<tr><th>Thu</th><th>Chi</th><th>Thu</th><th>Chi</th><th>Tồn</th></tr>' +
            '<tr class="p-abc"><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>1</th><th>2</th><th>3</th></tr>' +
            '</thead><tbody>' +
            '<tr><td colspan="5" style="text-align:left"><b>Số dư đầu kỳ</b></td><td></td><td></td><td class="pr"><b>' + fmtMoney(opening) + '</b></td></tr>' +
            body +
            '<tr class="p-total"><td colspan="5" style="text-align:left"><b>Cộng phát sinh trong kỳ</b></td><td class="pr"><b>' + fmtMoney(tThu) + '</b></td><td class="pr"><b>' + fmtMoney(tChi) + '</b></td><td></td></tr>' +
            '<tr class="p-total"><td colspan="5" style="text-align:left"><b>Số dư cuối kỳ</b></td><td></td><td></td><td class="pr"><b>' + fmtMoney(opening + tThu - tChi) + '</b></td></tr>' +
            '</tbody></table>' + printSign() + '</div>';
    }
    document.getElementById('btn-print').addEventListener('click', function () {
        if (activeTab === 'recon') { toast('Tab đối chiếu là báo cáo nội bộ — chọn tab Sổ quỹ VNĐ hoặc USD để in mẫu chuẩn', 'info'); return; }
        document.getElementById('print-title-label').textContent = 'In Sổ quỹ tiền mặt — Mẫu số ' + (activeTab === 'usd' ? 'S04b-DN' : 'S04a-DN') + ' (TT 99/2025/TT-BTC)';
        document.getElementById('print-preview').innerHTML = printSheetHTML();
        openModal('print-modal');
    });
    document.getElementById('btn-do-print').addEventListener('click', function () {
        document.getElementById('print-area').innerHTML = printSheetHTML();
        window.print();
    });

    setupFilterSettings({
        storageKey: 'demo-filter-cashfund',
        gearBtnId: 'ff-gear',
        defaultWrap: 'ff-default',
        advWrap: 'ff-adv',
        /* Quy tắc "mặc định = bắt buộc": chỉ trường locked hiện mặc định,
           mọi trường khác (Loại phiếu, TK đối ứng) nằm ở "Tìm kiếm nâng cao".
           Trường tổ chức chỉ có Công ty và đã locked → không cần nhóm grp-org. */
        fields: [
            { id: 'f-period', label: 'Kỳ báo cáo', locked: true },
            { id: 'f-company', label: 'Công ty', locked: true },
            { id: 'f-kind', label: 'Loại phiếu' },
            { id: 'f-tk', label: 'TK đối ứng' },
        ],
    });

    draw();
}

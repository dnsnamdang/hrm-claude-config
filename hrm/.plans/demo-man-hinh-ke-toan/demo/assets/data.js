/* ============================================================
   Demo Kế toán HRM — Dữ liệu mẫu + helpers + engine lịch trả nợ
   (Demo tĩnh: dữ liệu chỉ nằm trong file/sessionStorage)
   ============================================================ */

/* ---------- Danh mục ---------- */
var STATUSES = {
    0: { label: 'Chưa thực hiện', cls: 'st-none', icon: 'ri-time-line' },
    1: { label: 'Đang thực hiện', cls: 'st-active', icon: 'ri-loader-4-line' },
    2: { label: 'Hoàn thành', cls: 'st-done', icon: 'ri-checkbox-circle-line' },
    3: { label: 'Tạm dừng', cls: 'st-paused', icon: 'ri-pause-circle-line' },
    4: { label: 'Hủy', cls: 'st-cancel', icon: 'ri-close-circle-line' },
};

var PARTNERS = [
    'Ngân hàng TMCP Á Châu (ACB) — CN Đông Đô',
    'Ngân hàng TMCP Ngoại thương (Vietcombank) — CN Ba Đình',
    'Ngân hàng TMCP Đầu tư & Phát triển (BIDV) — CN Hà Thành',
    'Ngân hàng TMCP Kỹ thương (Techcombank) — CN Hoàn Kiếm',
    'Công ty CP Đầu tư Hoàng Minh',
    'Công ty TNHH TM Minh Long',
    'Công ty CP Vận tải Phú Thành',
    'Công ty TNHH Kỹ thuật Số Bách Khoa',
    'Nguyễn Văn Hùng (nhân viên)',
    'Trần Thị Mai (nhân viên)',
];

var CREDIT_CONTRACTS = ['', 'HĐTD-ACB-2026/015', 'HĐTD-VCB-2026/088', 'HĐTD-BIDV-2025/230', 'HĐTD-TCB-2025/112'];

var ACCOUNTS_DEBT = {
    borrow: ['3411 — Các khoản đi vay', '341 — Vay và nợ thuê tài chính', '3412 — Nợ thuê tài chính'],
    lend: ['1288 — Các khoản đầu tư khác nắm giữ đến ngày đáo hạn', '1283 — Cho vay', '138 — Phải thu khác'],
};
var ACCOUNTS_INTEREST = {
    borrow: ['635 — Chi phí tài chính', '242 — Chi phí trả trước', '241 — XDCB dở dang (vốn hoá lãi vay)'],
    lend: ['515 — Doanh thu hoạt động tài chính', '3387 — Doanh thu chưa thực hiện'],
};

var PAY_PERIODS = { monthly: 'Hàng tháng', quarterly: 'Hàng quý', semiannual: '6 tháng', maturity: 'Cuối kỳ' };

/* ---------- Format helpers ---------- */
function fmtMoney(n) {
    if (n === null || n === undefined || isNaN(n)) return '';
    return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}
function parseMoney(s) { return parseFloat(String(s).replace(/\./g, '').replace(/,/g, '.')) || 0; }
function fmtDate(iso) { // '2026-01-05' -> '05/01/2026'
    if (!iso) return '';
    var p = iso.split('-');
    return p[2] + '/' + p[1] + '/' + p[0];
}
function addMonths(iso, m) {
    var p = iso.split('-').map(Number);
    var d = new Date(p[0], p[1] - 1 + m, p[2]);
    // xử lý cuối tháng (31/01 + 1 tháng -> 28/02)
    if (d.getDate() !== p[2]) d = new Date(p[0], p[1] + m, 0);
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}
function todayISO() { return '2026-07-14'; } // mốc "hôm nay" cố định cho demo ổn định

/* ---------- Engine sinh lịch trả nợ ----------
   ku: { amount, termMonths, disburseDate, maturityDate,
         interestType: 'reducing'|'flat', rate (%/năm),
         principalPeriod, interestPeriod (key PAY_PERIODS),
         firstPrincipalDate, firstInterestDate }
   Trả về mảng kỳ: { date, principal, interest }
   Gốc chia đều theo kỳ gốc; lãi = dư_nợ(giảm dần)/gốc(flat) × rate/12 × số tháng kỳ.
------------------------------------------------- */
function periodMonths(key) { return key === 'monthly' ? 1 : key === 'quarterly' ? 3 : key === 'semiannual' ? 6 : 0; }

function generateSchedule(ku) {
    var events = {}; // dateISO -> {principal, interest}
    function push(date, field, val) {
        if (!events[date]) events[date] = { principal: 0, interest: 0 };
        events[date][field] += val;
    }
    var P = ku.amount, rate = ku.rate / 100;

    // --- các mốc trả gốc ---
    var pDates = [];
    if (ku.principalPeriod === 'maturity') {
        pDates = [ku.maturityDate];
    } else {
        var step = periodMonths(ku.principalPeriod);
        var d = ku.firstPrincipalDate;
        while (d <= ku.maturityDate) { pDates.push(d); d = addMonths(d, step); }
        if (!pDates.length || pDates[pDates.length - 1] < ku.maturityDate) pDates.push(ku.maturityDate);
    }
    var per = Math.round(P / pDates.length / 1000) * 1000;
    var remain = P;
    var principalAt = {}; // dateISO -> gốc trả kỳ đó
    pDates.forEach(function (dt, i) {
        var amt = (i === pDates.length - 1) ? remain : per;
        remain -= amt;
        principalAt[dt] = amt;
        push(dt, 'principal', amt);
    });

    // --- các mốc trả lãi ---
    var iDates = [];
    if (ku.interestPeriod === 'maturity') {
        iDates = [ku.maturityDate];
    } else {
        var istep = periodMonths(ku.interestPeriod);
        var di = ku.firstInterestDate;
        while (di <= ku.maturityDate) { iDates.push(di); di = addMonths(di, istep); }
        if (!iDates.length || iDates[iDates.length - 1] < ku.maturityDate) iDates.push(ku.maturityDate);
    }
    // lãi từng kỳ: từ mốc trước (hoặc ngày giải ngân) đến mốc này
    var prev = ku.disburseDate;
    var balance = P;
    // để tính dư nợ tại 1 thời điểm: trừ dần gốc đã đến hạn trước mốc lãi
    var pIdx = 0;
    iDates.forEach(function (dt) {
        // cập nhật dư nợ: các kỳ gốc có ngày <= prev đã trả
        while (pIdx < pDates.length && pDates[pIdx] <= prev) { balance -= principalAt[pDates[pIdx]]; pIdx++; }
        var months = monthsBetween(prev, dt);
        var base = ku.interestType === 'flat' ? P : balance;
        var interest = Math.round(base * rate / 12 * months / 1000) * 1000;
        if (interest > 0) push(dt, 'interest', interest);
        prev = dt;
    });

    return Object.keys(events).sort().map(function (dt) {
        return { date: dt, principal: events[dt].principal, interest: events[dt].interest };
    });
}
function monthsBetween(a, b) { // xấp xỉ theo tháng (demo)
    var pa = a.split('-').map(Number), pb = b.split('-').map(Number);
    var m = (pb[0] - pa[0]) * 12 + (pb[1] - pa[1]) + (pb[2] - pa[2]) / 30;
    return Math.max(m, 0);
}

/* ---------- Dữ liệu mẫu: Khế ước ĐI VAY ---------- */
var BORROW_DATA = [
    {
        id: 'DV1', code: 'KUDV-2026-00001', partner: PARTNERS[0], creditContract: 'HĐTD-ACB-2026/015',
        purpose: 'Bổ sung vốn lưu động phục vụ mua hàng hoá quý I/2026',
        debtAccount: ACCOUNTS_DEBT.borrow[0], interestAccount: ACCOUNTS_INTEREST.borrow[0],
        currency: 'VND', amount: 2000000000, termMonths: 12,
        disburseDate: '2026-01-05', maturityDate: '2027-01-05',
        disburseMethod: 'Chuyển khoản vào tài khoản DN', beneficiaryAccount: '19036 8899 8888 (Techcombank)', bankName: 'Techcombank — CN Hoàn Kiếm',
        interestType: 'reducing', dayBasis: 365, rateAdjust: 'adjustable',
        rates: [{ rate: 8.5, overdueRate: 12.75, from: '2026-01-05', note: 'LS ưu đãi 6 tháng đầu' }, { rate: 9.0, overdueRate: 13.5, from: '2026-07-05', note: 'LS thả nổi kỳ 2' }],
        rate: 9.0,
        principalPeriod: 'quarterly', firstPrincipalDate: '2026-04-05',
        interestPeriod: 'monthly', firstInterestDate: '2026-02-05',
        payMethod: 'Chuyển khoản', payAccount: '19036 8899 8888', payBank: 'Techcombank',
        status: 1, paidPeriods: 8, // số dòng lịch (gốc+lãi) đã hoàn tất
    },
    {
        id: 'DV2', code: 'KUDV-2026-00002', partner: PARTNERS[1], creditContract: 'HĐTD-VCB-2026/088',
        purpose: 'Đầu tư mở rộng kho hàng Long Biên',
        debtAccount: ACCOUNTS_DEBT.borrow[0], interestAccount: ACCOUNTS_INTEREST.borrow[0],
        currency: 'VND', amount: 5000000000, termMonths: 24,
        disburseDate: '2026-03-15', maturityDate: '2028-03-15',
        disburseMethod: 'Chuyển khoản vào tài khoản DN', beneficiaryAccount: '001100 234 5678 (Vietcombank)', bankName: 'Vietcombank — CN Ba Đình',
        interestType: 'reducing', dayBasis: 365, rateAdjust: 'fixed',
        rates: [{ rate: 9.2, overdueRate: 13.8, from: '2026-03-15', note: '' }],
        rate: 9.2,
        principalPeriod: 'quarterly', firstPrincipalDate: '2026-06-15',
        interestPeriod: 'quarterly', firstInterestDate: '2026-06-15',
        payMethod: 'Chuyển khoản', payAccount: '001100 234 5678', payBank: 'Vietcombank',
        status: 1, paidPeriods: 1,
    },
    {
        id: 'DV3', code: 'KUDV-2025-00007', partner: PARTNERS[2], creditContract: 'HĐTD-BIDV-2025/230',
        purpose: 'Vay ngắn hạn thanh toán công nợ NCC',
        debtAccount: ACCOUNTS_DEBT.borrow[0], interestAccount: ACCOUNTS_INTEREST.borrow[0],
        currency: 'VND', amount: 1200000000, termMonths: 12,
        disburseDate: '2025-06-10', maturityDate: '2026-06-10',
        disburseMethod: 'Chuyển khoản vào tài khoản DN', beneficiaryAccount: '2601 000 555 999 (BIDV)', bankName: 'BIDV — CN Hà Thành',
        interestType: 'flat', dayBasis: 360, rateAdjust: 'fixed',
        rates: [{ rate: 10, overdueRate: 15, from: '2025-06-10', note: '' }],
        rate: 10,
        principalPeriod: 'maturity', firstPrincipalDate: '2026-06-10',
        interestPeriod: 'monthly', firstInterestDate: '2025-07-10',
        payMethod: 'Chuyển khoản', payAccount: '2601 000 555 999', payBank: 'BIDV',
        status: 2, paidPeriods: 99, // hoàn thành — tất cả kỳ đã trả
    },
    {
        id: 'DV4', code: 'KUDV-2026-00003', partner: PARTNERS[4], creditContract: '',
        purpose: 'Vay vốn đối tác bổ sung dòng tiền dự án Nam Định',
        debtAccount: ACCOUNTS_DEBT.borrow[1], interestAccount: ACCOUNTS_INTEREST.borrow[0],
        currency: 'VND', amount: 800000000, termMonths: 6,
        disburseDate: '2026-07-01', maturityDate: '2027-01-01',
        disburseMethod: 'Chuyển khoản vào tài khoản DN', beneficiaryAccount: '19036 8899 8888 (Techcombank)', bankName: 'Techcombank — CN Hoàn Kiếm',
        interestType: 'flat', dayBasis: 365, rateAdjust: 'fixed',
        rates: [{ rate: 7, overdueRate: 10.5, from: '2026-07-01', note: 'Thoả thuận riêng với đối tác' }],
        rate: 7,
        principalPeriod: 'maturity', firstPrincipalDate: '2027-01-01',
        interestPeriod: 'quarterly', firstInterestDate: '2026-10-01',
        payMethod: 'Chuyển khoản', payAccount: '19036 8899 8888', payBank: 'Techcombank',
        status: 1, paidPeriods: 0,
    },
    {
        id: 'DV5', code: 'KUDV-2025-00009', partner: PARTNERS[3], creditContract: 'HĐTD-TCB-2025/112',
        purpose: 'Vay trung hạn đầu tư dây chuyền lắp ráp',
        debtAccount: ACCOUNTS_DEBT.borrow[1], interestAccount: ACCOUNTS_INTEREST.borrow[0],
        currency: 'VND', amount: 3000000000, termMonths: 36,
        disburseDate: '2025-10-20', maturityDate: '2028-10-20',
        disburseMethod: 'Chuyển khoản vào tài khoản DN', beneficiaryAccount: '19036 8899 8888 (Techcombank)', bankName: 'Techcombank — CN Hoàn Kiếm',
        interestType: 'reducing', dayBasis: 365, rateAdjust: 'adjustable',
        rates: [{ rate: 9.8, overdueRate: 14.7, from: '2025-10-20', note: '' }],
        rate: 9.8,
        principalPeriod: 'semiannual', firstPrincipalDate: '2026-04-20',
        interestPeriod: 'quarterly', firstInterestDate: '2026-01-20',
        payMethod: 'Chuyển khoản', payAccount: '19036 8899 8888', payBank: 'Techcombank',
        status: 3, paidPeriods: 2,
    },
];

/* ---------- Dữ liệu mẫu: Khế ước CHO VAY ---------- */
var LEND_DATA = [
    {
        id: 'CV1', code: 'KUCV-2026-00001', partner: PARTNERS[5], creditContract: '',
        purpose: 'Cho đối tác vay bổ sung vốn lưu động, có tài sản đảm bảo',
        debtAccount: ACCOUNTS_DEBT.lend[0], interestAccount: ACCOUNTS_INTEREST.lend[0],
        currency: 'VND', amount: 1500000000, termMonths: 12,
        disburseDate: '2026-02-10', maturityDate: '2027-02-10',
        disburseMethod: 'Chuyển khoản', beneficiaryAccount: '0451 000 786 555 (Vietcombank)', bankName: 'Vietcombank — CN Thành Công',
        interestType: 'reducing', dayBasis: 365, rateAdjust: 'fixed',
        rates: [{ rate: 11, overdueRate: 16.5, from: '2026-02-10', note: '' }],
        rate: 11,
        principalPeriod: 'quarterly', firstPrincipalDate: '2026-05-10',
        interestPeriod: 'monthly', firstInterestDate: '2026-03-10',
        payMethod: 'Nộp vào tài khoản', payAccount: '19036 8899 8888', payBank: 'Techcombank',
        status: 1, paidPeriods: 6,
    },
    {
        id: 'CV2', code: 'KUCV-2026-00002', partner: PARTNERS[8], creditContract: '',
        purpose: 'Cho nhân viên vay mua nhà theo chính sách phúc lợi',
        debtAccount: ACCOUNTS_DEBT.lend[2], interestAccount: ACCOUNTS_INTEREST.lend[0],
        currency: 'VND', amount: 200000000, termMonths: 10,
        disburseDate: '2026-04-01', maturityDate: '2027-02-01',
        disburseMethod: 'Chuyển khoản', beneficiaryAccount: '9704 2292 1234 (MB Bank)', bankName: 'MB Bank — CN Thanh Xuân',
        interestType: 'flat', dayBasis: 365, rateAdjust: 'fixed',
        rates: [{ rate: 5, overdueRate: 7.5, from: '2026-04-01', note: 'LS ưu đãi nội bộ' }],
        rate: 5,
        principalPeriod: 'monthly', firstPrincipalDate: '2026-05-01',
        interestPeriod: 'monthly', firstInterestDate: '2026-05-01',
        payMethod: 'Trừ lương', payAccount: '', payBank: '',
        status: 1, paidPeriods: 4,
    },
    {
        id: 'CV3', code: 'KUCV-2025-00003', partner: PARTNERS[6], creditContract: '',
        purpose: 'Cho vay ngắn hạn hỗ trợ đối tác vận tải',
        debtAccount: ACCOUNTS_DEBT.lend[1], interestAccount: ACCOUNTS_INTEREST.lend[0],
        currency: 'VND', amount: 900000000, termMonths: 9,
        disburseDate: '2025-08-15', maturityDate: '2026-05-15',
        disburseMethod: 'Chuyển khoản', beneficiaryAccount: '8899 777 111 (ACB)', bankName: 'ACB — CN Cầu Giấy',
        interestType: 'flat', dayBasis: 360, rateAdjust: 'fixed',
        rates: [{ rate: 10.5, overdueRate: 15.75, from: '2025-08-15', note: '' }],
        rate: 10.5,
        principalPeriod: 'maturity', firstPrincipalDate: '2026-05-15',
        interestPeriod: 'quarterly', firstInterestDate: '2025-11-15',
        payMethod: 'Nộp vào tài khoản', payAccount: '19036 8899 8888', payBank: 'Techcombank',
        status: 2, paidPeriods: 99,
    },
    {
        id: 'CV4', code: 'KUCV-2026-00004', partner: PARTNERS[7], creditContract: '',
        purpose: 'Cho vay hợp tác kinh doanh thiết bị số (chưa giải ngân)',
        debtAccount: ACCOUNTS_DEBT.lend[0], interestAccount: ACCOUNTS_INTEREST.lend[0],
        currency: 'VND', amount: 600000000, termMonths: 6,
        disburseDate: '2026-08-01', maturityDate: '2027-02-01',
        disburseMethod: 'Chuyển khoản', beneficiaryAccount: '', bankName: '',
        interestType: 'reducing', dayBasis: 365, rateAdjust: 'fixed',
        rates: [{ rate: 9, overdueRate: 13.5, from: '2026-08-01', note: '' }],
        rate: 9,
        principalPeriod: 'maturity', firstPrincipalDate: '2027-02-01',
        interestPeriod: 'monthly', firstInterestDate: '2026-09-01',
        payMethod: 'Nộp vào tài khoản', payAccount: '19036 8899 8888', payBank: 'Techcombank',
        status: 0, paidPeriods: 0,
    },
];

/* ---------- Số liệu dẫn xuất từ lịch (dùng cho danh sách + chi tiết) ---------- */
function computeStats(ku) {
    var sched = generateSchedule(ku);
    var paid = ku.paidPeriods >= sched.length ? sched.length : ku.paidPeriods;
    var s = { paidPrincipal: 0, paidInterest: 0, totalInterest: 0, nextPrincipalDate: '', nextInterestDate: '', schedule: sched, paidCount: paid };
    sched.forEach(function (row, i) {
        s.totalInterest += row.interest;
        if (i < paid) { s.paidPrincipal += row.principal; s.paidInterest += row.interest; }
        else {
            if (!s.nextPrincipalDate && row.principal > 0) s.nextPrincipalDate = row.date;
            if (!s.nextInterestDate && row.interest > 0) s.nextInterestDate = row.date;
        }
    });
    s.balance = ku.amount - s.paidPrincipal;
    return s;
}

/* ---------- sessionStorage store (bản ghi user tạo trong phiên demo) ---------- */
function loadSessionRecords(kind) { // kind: 'borrow' | 'lend'
    try { return JSON.parse(sessionStorage.getItem('demo-ku-' + kind) || '[]'); } catch (e) { return []; }
}
function saveSessionRecord(kind, rec) {
    var arr = loadSessionRecords(kind);
    arr.push(rec);
    sessionStorage.setItem('demo-ku-' + kind, JSON.stringify(arr));
}
function getAllRecords(kind) {
    var base = kind === 'borrow' ? BORROW_DATA : LEND_DATA;
    return base.concat(loadSessionRecords(kind).map(function (r) { r.isNew = true; return r; }));
}
function findRecord(kind, id) {
    return getAllRecords(kind).filter(function (r) { return r.id === id; })[0] || null;
}
function nextCode(kind) {
    var prefix = kind === 'borrow' ? 'KUDV' : 'KUCV';
    var n = 10 + loadSessionRecords(kind).length + 1;
    return prefix + '-2026-000' + (n < 10 ? '0' + n : n);
}

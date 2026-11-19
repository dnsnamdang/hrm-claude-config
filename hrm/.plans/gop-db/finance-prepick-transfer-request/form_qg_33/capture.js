// Chụp ảnh HDSD/SRS màn Yêu cầu điều chuyển hàng giữ trên DEV (headless riêng, KHÔNG bấm xác nhận ghi dữ liệu).
// Chạy: node capture.js [bước...]   (không truyền = chạy hết)
//
// ⚠️ Dev 28/10/2026 KHÔNG có phiếu điều chuyển nào (danh sách 0 phiếu, kể cả với Super Admin). Để minh họa danh
// sách / chi tiết / duyệt / từ chối / sửa / xóa / lịch sử, script BẬT TẠM 3 phiếu minh họa ngay trên trình duyệt
// (page.route trả response giả cho các API ĐỌC) — dòng hàng lấy từ hàng THẬT tài khoản test đang giữ. Không ghi gì
// xuống máy chủ; mọi hộp xác nhận đều bấm Hủy / Đóng. Màn Tạo mới + popup chọn hàng/lô là dữ liệu thật.
// Icon dùng chung với màn 31 (form_qg_31/hdsd_shots/icons) — ở đây chỉ chụp icon riêng của màn 33.
const path = require('path');
const fs = require('fs');
const { openDev, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/phieu-theo-form-quoc-gia/pw_dev.js');

const HERE = __dirname;
const SHOT = path.join(HERE, 'hdsd_shots');
const ICON = path.join(SHOT, 'icons');
const LIST_URL = DEV + '/finance/prepick-transfer-requests';
const API = 'finance/prepick-transfer-requests';
const ID_TP = 990001; // Chờ TP duyệt (minh họa)
const ID_DONE = 990002; // Đã duyệt (minh họa)
const ID_KD = 990003; // Không duyệt, của chính tài khoản test (minh họa)
const STEPS = process.argv.slice(2);
const want = (s) => !STEPS.length || STEPS.includes(s);

let page;
async function settle(ms = 1200) {
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.mouse.move(760, 8);
    await page.waitForTimeout(ms);
}
async function icon(loc, name, opt = {}) {
    const l = loc.first();
    await l.scrollIntoViewIfNeeded().catch(() => {});
    const b = await l.boundingBox();
    if (!b) return console.log('THIẾU icon', name);
    const clip = { x: b.x, y: b.y, width: opt.maxW ? Math.min(b.width, opt.maxW) : b.width, height: b.height };
    await page.screenshot({ path: path.join(ICON, name + '.png'), clip });
}
async function full(name) {
    await page.mouse.move(760, 8);
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(SHOT, name + '.png') });
}
async function elShot(loc, name) {
    await page.mouse.move(760, 8);
    await page.waitForTimeout(600);
    await loc.first().screenshot({ path: path.join(SHOT, name + '.png') });
}
const modal = () => page.locator('.modal.show .modal-content').last();
const inModal = (text) => page.locator('.modal.show').last().locator(`button:has-text("${text}")`);
const rowOf = (code) => page.locator('tr', { has: page.locator(`a:text-is("${code}")`) });

// ---------------------------------------------------------------- mock chỉ trên trình duyệt
let MOCK = {}; // path -> object (trả thẳng) | function(json) (sửa response thật)
async function installMocks() {
    await page.route('**/api/v1/' + API + '**', async (route) => {
        const req = route.request();
        if (req.method() !== 'GET') return route.continue();
        const p = new URL(req.url()).pathname.replace(/^.*\/api\/v1\//, '');
        if (!(p in MOCK)) return route.continue();
        const v = MOCK[p];
        if (typeof v === 'function') {
            const resp = await route.fetch();
            return route.fulfill({ response: resp, json: v(await resp.json()) });
        }
        return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(v) });
    });
}

const STATUS = {
    5: ['Chờ TP duyệt', 'warning', '#D97706'], 4: ['Chờ BGĐ duyệt', 'warning', '#D97706'], 2: ['Chờ KT duyệt', 'warning', '#D97706'],
    1: ['Đã duyệt', 'success', '#16A34A'], 3: ['Không duyệt', 'danger', '#DC2626'],
};

(async () => {
    fs.mkdirSync(ICON, { recursive: true });
    const o = await openDev(HERE);
    page = o.page;
    await installMocks();

    await page.goto(LIST_URL);
    await settle(3000);
    // Dữ liệu THẬT để dựng phiếu minh họa: hàng tài khoản đang giữ + lô, khách hàng, người dùng hiện tại
    const R = await page.evaluate(async (api) => {
        const g = (ep) => $nuxt.$store.dispatch('apiGetMethod', ep);
        const me = $nuxt.$store.state.current_employee || {};
        const info = $nuxt.$store.state.current_employee_info || {};
        const prods = ((await g(`${api}/products?per_page=10`)).data || {}).items || [];
        const lines = [];
        for (const p of prods) {
            const lots = ((await g(`${api}/lots?product_id=${p.product_id}&employee_id=${me.id}`)).data || {});
            const lot = (lots.items || lots || [])[0];
            if (lot) lines.push({ p, lot });
        }
        const cus = await g('assign/customers?per_page=3&page=1').catch(() => null);
        const emps = ($nuxt.$store.state.employeeOptions || []).slice(0, 40);
        return { me: { id: me.id, name: info.fullname || (me.info || {}).fullname || 'DNS Admin' }, lines, cus, emps };
    }, API);
    fs.writeFileSync(path.join(HERE, 'capture_data.json'), JSON.stringify(R, null, 1));

    const cus = ((R.cus && (R.cus.data || [])) || [])[0] || {};
    const cusName = cus.fullname || cus.name || 'CÔNG TY TNHH THƯƠNG MẠI MINH ANH';
    const cusId = cus.id || 1;
    const emp = (i, fb) => {
        const e = R.emps[i];
        return e ? { id: e.id, name: String(e.text || '').split(' - ')[0] } : fb;
    };
    const recv = emp(5, { id: 2, name: 'Trần Văn Đức' });
    const products = R.lines.map(({ p, lot }, i) => ({
        id: 500 + i, from_prepick_detail_id: lot.id || lot.prepick_detail_id, product_id: p.product_id,
        product_name: p.product_name, product_code: p.product_code, unit_id: p.unit_id, unit_name: p.unit_name,
        approve: false, qty: Math.min(5, Number(lot.qty || p.held_qty || 1)), holding_qty: Number(lot.qty || p.held_qty || 0),
        expire_date: lot.expire_date_text || lot.expire_date || '20/11/2026', from_customer_id: lot.customer_id || null, from_customer_name: lot.customer_name || null,
        contractable_id: null, contractable_code: null, contractable_type: null,
    }));
    const base = (id, code, status, extra = {}) => ({
        id, code, note: 'Chuyển hàng giữ cho khách của phòng kinh doanh khu vực', status,
        status_name: STATUS[status][0], status_type: STATUS[status][1], status_color: STATUS[status][2],
        created_at: '27/10/2026', created_at_time: '27/10/2026 09:15', creator_name: R.me.name,
        department_name: 'Phòng Công nghệ thông tin', company_name: 'CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT',
        to_employee_id: recv.id, to_employee_name: recv.name, to_employee_department: 'PHÒNG THIẾT BỊ Ô TÔ 2',
        to_customer_id: cusId, to_customer_name: cusName, to_customer_code: cus.code || '',
        attachments: [], approvals: [], is_can_edit: false, is_can_delete: false, is_can_approve: false, products, ...extra,
    });
    const D = {
        [ID_TP]: base(ID_TP, 'ĐCHG-01310', 5, { is_can_approve: true }),
        [ID_DONE]: base(ID_DONE, 'ĐCHG-01309', 1, { created_at_time: '26/10/2026 14:02', approvals: [
            { level: 'Trưởng phòng', approver_name: 'Trần Ngọc Duy', approved_time: '26/10/2026 15:10', comment: null, is_reject: false },
            { level: 'Kế toán', approver_name: 'Võ Thị Hà', approved_time: '26/10/2026 16:44', comment: 'Đã kiểm tra tồn', is_reject: false }] }),
        [ID_KD]: base(ID_KD, 'ĐCHG-01308', 3, { created_at_time: '25/10/2026 10:30', is_can_edit: true, is_can_delete: true, approvals: [
            { level: 'Trưởng phòng', approver_name: 'Trần Ngọc Duy', approved_time: '25/10/2026 11:05', comment: 'Sai khách hàng nhận, đề nghị sửa lại', is_reject: true }] }),
    };
    const listRow = (d) => ({
        id: d.id, code: d.code, created_by: R.me.id, creator_name: d.creator_name, created_at: d.created_at_time,
        updated_by: R.me.id, updater_name: d.creator_name, updated_at: d.created_at_time,
        to_employee_id: d.to_employee_id, to_employee_name: d.to_employee_name, to_employee_department: d.to_employee_department,
        to_customer_id: d.to_customer_id, to_customer_name: d.to_customer_name, to_customer_code: d.to_customer_code,
        approver_id: d.status === 1 ? 1 : null, approver_name: d.status === 1 ? 'Võ Thị Hà' : null,
        approved_time: d.status === 1 ? '26/10/2026 16:44' : null, department_name: d.department_name, note: d.note,
        comment: d.status === 3 ? 'Sai khách hàng nhận, đề nghị sửa lại' : null,
        status: d.status, status_name: d.status_name, status_type: d.status_type, status_color: d.status_color,
        is_can_edit: d.is_can_edit, is_can_delete: d.is_can_delete, is_can_approve: d.is_can_approve,
    });
    const LIST = (json) => ({ ...json, data: [D[ID_TP], D[ID_DONE], D[ID_KD]].map(listRow), total: 3, lastPage: 1, currentPage: 1 });
    const MOCK_ALL = {
        [API]: LIST,
        [`${API}/${ID_TP}`]: { code: 200, message: 'success', data: D[ID_TP] },
        [`${API}/${ID_DONE}`]: { code: 200, message: 'success', data: D[ID_DONE] },
        [`${API}/${ID_KD}`]: { code: 200, message: 'success', data: D[ID_KD] },
        [`${API}/${ID_DONE}/histories`]: { code: 200, message: 'success', data: [
            { id: 3, action: 'kt_approve', action_label: 'Kế toán duyệt', action_color: '#16a34a', actor_name: 'Võ Thị Hà', note: 'Đã kiểm tra tồn',
                created_at: '26/10/2026 16:44', changes: [{ field: 'Trạng thái', old: 'Chờ KT duyệt', new: 'Đã duyệt' }] },
            { id: 2, action: 'tp_approve', action_label: 'Trưởng phòng duyệt', action_color: '#16a34a', actor_name: 'Trần Ngọc Duy', note: null,
                created_at: '26/10/2026 15:10', changes: [{ field: 'Trạng thái', old: 'Chờ TP duyệt', new: 'Chờ KT duyệt' }] },
            { id: 1, action: 'create', action_label: 'Tạo phiếu', action_color: '#2563eb', actor_name: R.me.name, note: null,
                created_at: '26/10/2026 14:02', changes: [{ field: 'Trạng thái', old: null, new: 'Chờ TP duyệt' },
                    { field: 'Người nhận', old: null, new: recv.name }, { field: 'Khách hàng nhận', old: null, new: cusName }] },
        ] },
    };
    const gotoList = async () => {
        MOCK = MOCK_ALL;
        await page.goto(LIST_URL);
        await page.waitForSelector('text=ĐCHG-01310', { timeout: 60000 });
        await settle(2000);
    };

    if (want('list')) {
        await gotoList();
        await full('01_list');
    }

    if (want('filter')) {
        await gotoList();
        await page.click('button:has-text("Tìm kiếm nâng cao")');
        await settle(1500);
        await elShot(page.locator('.smart-filter-card'), '02_filter');
        const ff = (lb) => page.locator('.ff').filter({ has: page.locator('label.ff__label', { hasText: new RegExp('^[\\s\\u00a0]*' + lb + '[\\s\\u00a0]*$') }) });
        const map = { 'Người nhận': 'o_nguoinhan', 'Khách nhận': 'o_khachnhan', 'Tên, mã hàng': 'o_tenmahang', 'Số hợp đồng': 'o_sohopdong' };
        for (const [lb, nm] of Object.entries(map)) await icon(ff(lb), nm, { maxW: 180 });
    }

    if (want('filtercfg')) {
        await gotoList();
        await page.click('button:has-text("Cài đặt bộ lọc")');
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(1200);
        await elShot(modal(), '26_filtercfg');
        await inModal('Đóng').first().click();
    }

    if (want('colcfg')) {
        await gotoList();
        await page.locator('[title="Cấu hình cột hiển thị"]').first().click();
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(1200);
        await elShot(modal(), '25_colcfg');
        await inModal('Đóng').first().click();
    }

    if (want('export')) {
        await gotoList();
        await page.click('button:has-text("Xuất Excel")');
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(1200);
        await elShot(modal(), '20_export');
        await inModal('Đóng').first().click();
    }

    if (want('history')) {
        await gotoList();
        await rowOf('ĐCHG-01309').locator('[title="Lịch sử"]').first().click();
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(2500);
        await elShot(modal(), '16_history');
        await inModal('Đóng').first().click();
    }

    if (want('delete')) {
        await gotoList();
        await rowOf('ĐCHG-01308').locator('[title="Xóa"]').first().click();
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(800);
        await elShot(modal(), '13_delete');
        await inModal('Hủy').first().click();
    }

    if (want('detail')) {
        MOCK = MOCK_ALL;
        await page.goto(`${LIST_URL}/${ID_DONE}`);
        await page.waitForSelector('text=ĐCHG-01309', { timeout: 60000 });
        await settle(3000);
        await full('17_detail');
    }

    if (want('approve')) {
        MOCK = MOCK_ALL;
        await page.goto(`${LIST_URL}/${ID_TP}`);
        await page.waitForSelector('button:has-text("TP duyệt")', { timeout: 60000 });
        await settle(3000);
        await full('14_detail_approve');
        await icon(page.locator('button:has-text("TP duyệt")'), 'btn_duyet');
        await page.locator('button:has-text("TP duyệt")').first().click();
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(800);
        await elShot(modal(), '14_approve');
        await inModal('Hủy').first().click();
        await page.waitForTimeout(1000);
        await page.locator('button:has-text("Từ chối")').last().click();
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(800);
        await elShot(modal(), '15_reject');
        await inModal('Đóng').first().click();
    }

    if (want('edit')) {
        MOCK = MOCK_ALL;
        await page.goto(`${LIST_URL}/${ID_KD}/edit`);
        await page.waitForSelector('button:has-text("Gửi duyệt")', { timeout: 60000 });
        await settle(3500);
        await full('12_edit');
    }

    if (want('create')) {
        MOCK = {};
        await page.goto(LIST_URL + '/create');
        await page.waitForSelector('button:has-text("Thêm hàng hóa")', { timeout: 60000 });
        await settle(2500);
        await icon(page.locator('button:has-text("Thêm hàng hóa")'), 'btn_themhanghoa');
        await page.click('button:has-text("Thêm hàng hóa")');
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(2500);
        // Tích hết các dòng hàng đang giữ
        const boxes = page.locator('.modal.show tbody input[type=checkbox]');
        const n = await boxes.count();
        for (let i = 0; i < n; i++) await boxes.nth(i).check({ force: true }).catch(() => {});
        await settle(600);
        await elShot(modal(), '11_stock');
        await icon(page.locator('.modal.show button:has-text("Chọn")').last(), 'btn_chon');
        await icon(inModal('Đóng'), 'btn_dong');
        await page.locator('.modal.show button:has-text("Chọn")').last().click();
        await settle(2500);
        // Mở popup chọn lô nguồn của dòng 1 — chụp rồi đóng (không chọn)
        const lotBtn = page.locator('[title="Chọn lô hàng giữ nguồn"]').first();
        await icon(lotBtn, 'btn_chonlo');
        await icon(page.locator('[title="Chọn đơn hàng / hợp đồng"]'), 'btn_chonhopdong');
        await icon(page.locator('[title="Xóa dòng hàng hóa này khỏi phiếu"]'), 'btn_xoadong');
        await lotBtn.click();
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(2000);
        await elShot(modal(), '11_lot');
        await inModal('Đóng').first().click().catch(() => page.keyboard.press('Escape'));
        await settle(1000);
        await full('10_create');
        await icon(page.locator('button:has-text("Gửi duyệt")'), 'btn_guiduyet');
    }

    await o.browser.close();
})().catch(async (e) => {
    console.error(e);
    try { await page.screenshot({ path: path.join(HERE, 'capture_error.png') }); } catch (x) {}
    process.exit(1);
});

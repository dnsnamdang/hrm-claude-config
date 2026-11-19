// Chụp ảnh HDSD/SRS màn Yêu cầu gia hạn hàng giữ trên DEV (headless riêng, KHÔNG bấm xác nhận ghi dữ liệu).
// Chạy: node capture.js [bước...]   (không truyền = chạy hết)
// Dữ liệu dev 28/10/2026: không có phiếu Đang tạo của tài khoản test, không phiếu nào có lịch sử, tài khoản
// không giữ lô nào sắp hết hạn → các màn Sửa / nút Sửa-Xóa / Tạo mới có dòng hàng / Lịch sử được BẬT TẠM
// trên trình duyệt bằng cách sửa response API (page.route) — không ghi gì xuống máy chủ.
const path = require('path');
const fs = require('fs');
const { openDev, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/phieu-theo-form-quoc-gia/pw_dev.js');

const HERE = __dirname;
const SHOT = path.join(HERE, 'hdsd_shots');
const ICON = path.join(SHOT, 'icons');
const LIST_URL = DEV + '/finance/prepick-extend-requests';
const API = 'finance/prepick-extend-requests';
const ID_WAIT = 1984; // Chờ BGĐ duyệt — tài khoản test duyệt được
const ID_DONE = 1982; // Đã duyệt
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
    const pad = opt.pad || 0;
    const clip = { x: b.x - pad, y: b.y - pad, width: (opt.maxW ? Math.min(b.width, opt.maxW) : b.width) + 2 * pad, height: b.height + 2 * pad };
    await page.screenshot({ path: path.join(ICON, name + '.png'), clip });
}
async function full(name, opt = {}) {
    await page.mouse.move(760, 8);
    await page.waitForTimeout(600);
    const MAXH = opt.maxH || 900;
    if (opt.fullPage) {
        // Màn form dài: nới cao khung nhìn cho vừa nội dung (giữ thanh bên + footer đúng chỗ), chụp, trả lại.
        const h = await page.evaluate((m) => Math.min(m, Math.max(900, document.documentElement.scrollHeight, document.body.scrollHeight)), MAXH);
        await page.setViewportSize({ width: 1440, height: h });
        await page.waitForTimeout(1200);
        await page.mouse.move(760, 8);
        await page.screenshot({ path: path.join(SHOT, name + '.png') });
        await page.setViewportSize({ width: 1440, height: 900 });
        return;
    }
    await page.screenshot({ path: path.join(SHOT, name + '.png'), clip: opt.clip });
}
async function elShot(loc, name) {
    await page.mouse.move(760, 8);
    await page.waitForTimeout(600);
    await loc.first().screenshot({ path: path.join(SHOT, name + '.png') });
}
const modal = () => page.locator('.modal.show .modal-content').last();
const inModal = (text) => page.locator('.modal.show').last().locator(`button:has-text("${text}")`);

async function gotoList() {
    await page.goto(LIST_URL);
    await page.waitForSelector('text=PGHHG-', { timeout: 60000 });
    await settle(2500);
}
const rowOf = (code) => page.locator('tr', { has: page.locator(`a:text-is("${code}")`) });

// ---------------------------------------------------------------- mock (chỉ trên trình duyệt)
let MOCK = {};
async function installMocks() {
    await page.route('**/api/v1/' + API + '**', async (route) => {
        const req = route.request();
        const u = new URL(req.url());
        const p = u.pathname.replace(/^.*\/api\/v1\//, '');
        if (req.method() !== 'GET') return route.continue();
        for (const [k, fn] of Object.entries(MOCK)) {
            if (p === k || (k.endsWith('?') && p === k.slice(0, -1))) {
                const resp = await route.fetch();
                const json = await resp.json();
                return route.fulfill({ response: resp, json: fn(json, u) });
            }
        }
        return route.continue();
    });
}

(async () => {
    fs.mkdirSync(ICON, { recursive: true });
    const o = await openDev(HERE);
    page = o.page;
    await installMocks();

    // Dữ liệu thật để dựng mock
    await gotoList();
    const real = await page.evaluate(async ([api, a, b]) => {
        const g = (ep) => $nuxt.$store.dispatch('apiGetMethod', ep);
        return { wait: (await g(`${api}/${a}`)).data, done: (await g(`${api}/${b}`)).data };
    }, [API, ID_WAIT, ID_DONE]);

    if (want('list')) {
        await full('01_list');
        await icon(page.locator('input[placeholder="Tìm theo mã phiếu..."]'), 'o_timnhanh', { maxW: 330 });
        await icon(page.locator('button:has-text("Tìm kiếm nâng cao")'), 'btn_timkiemnangcao');
        await icon(page.locator('button:has-text("Cài đặt bộ lọc")'), 'btn_caidatboloc');
        await icon(page.locator('button:text-is("Tìm kiếm"), button:has-text("Tìm kiếm"):not(:has-text("nâng cao"))'), 'btn_timkiem');
        await icon(page.locator('button:has-text("Làm mới")'), 'btn_lammoi');
        await icon(page.locator('button:has-text("Tạo mới")'), 'btn_taomoi');
        await icon(page.locator('button[title="In danh sách theo bộ lọc đang áp"]'), 'btn_in_list');
        await icon(page.locator('button:has-text("Xuất Excel")'), 'btn_xuatexcel');
        await icon(page.locator('button[title="Cấu hình cột hiển thị"], [title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        // Cột Hành động: phiếu chờ mình duyệt (Duyệt, Từ chối + ba chấm) và phiếu đã duyệt (In, Lịch sử)
        const rw = rowOf('PGHHG-0' + ID_WAIT);
        await rw.scrollIntoViewIfNeeded();
        await icon(rw.locator('[title="Duyệt"]'), 'btn_duyet_row');
        await icon(rw.locator('[title="Từ chối"]'), 'btn_tuchoi_row');
        await icon(rw.locator('[title="Hành động khác"]'), 'btn_bacham_row');
        await rw.locator('[title="Hành động khác"]').first().click();
        await page.waitForTimeout(800);
        const menu = page.locator('.v2-row-actions__menu:visible');
        await icon(menu.locator('.v2-row-actions__item:has-text("In")'), 'item_in');
        await icon(menu.locator('.v2-row-actions__item:has-text("Lịch sử")'), 'item_lichsu');
        await page.keyboard.press('Escape');
        await page.mouse.click(700, 880);
        const rd = rowOf('PGHHG-0' + ID_DONE);
        await icon(rd.locator('[title="In"]'), 'btn_in_row');
        await icon(rd.locator('[title="Lịch sử"]'), 'btn_lichsu_row');
    }

    if (want('filter')) {
        await gotoList();
        await page.click('button:has-text("Tìm kiếm nâng cao")');
        await settle(1500);
        const card = page.locator('.smart-filter-card').first();
        await elShot(card, '02_filter');
        const ff = (lb) => page.locator('.ff').filter({ has: page.locator('label.ff__label', { hasText: new RegExp('^[\\s\\u00a0]*' + lb + '[\\s\\u00a0]*$') }) });
        const map = { 'Công ty': 'o_congty', 'Phòng ban': 'o_phongban', 'Mã phiếu': 'o_maphieu', 'Trạng thái': 'o_trangthai',
            'Người tạo': 'o_nguoitao', 'Người duyệt': 'o_nguoiduyet', 'Tên hàng hóa': 'o_tenhang', 'Mã hàng hóa': 'o_mahang', 'Ngày tạo': 'o_ngaytao' };
        for (const [lb, nm] of Object.entries(map)) await icon(ff(lb), nm, { maxW: 180 });
    }

    if (want('filtercfg')) {
        await gotoList();
        await page.click('button:has-text("Cài đặt bộ lọc")');
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(1200);
        await elShot(modal(), '26_filtercfg');
        await icon(inModal('Lưu'), 'btn_luu');
        await icon(inModal('Khôi phục'), 'btn_khoiphuc');
        await icon(inModal('Đóng'), 'btn_dong_filtercfg');
        await inModal('Đóng').first().click();
    }

    if (want('colcfg')) {
        await gotoList();
        await page.locator('[title="Cấu hình cột hiển thị"]').first().click();
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(1200);
        await elShot(modal(), '25_colcfg');
        await icon(inModal('Chọn tất cả'), 'btn_chontatca');
        await icon(inModal('Bỏ chọn hết'), 'btn_bochonhet');
        await icon(inModal('Lưu'), 'btn_luu_col');
        await icon(inModal('Đóng'), 'btn_dong_col');
        await inModal('Đóng').first().click();
    }

    if (want('export')) {
        await gotoList();
        await page.click('button:has-text("Xuất Excel")');
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(1200);
        await elShot(modal(), '20_export');
        await icon(inModal('Xuất file'), 'btn_xuatfile');
        await icon(inModal('Đóng'), 'btn_dong_export');
        await inModal('Đóng').first().click();
    }

    if (want('printlist')) {
        await gotoList();
        await page.click('button[title="In danh sách theo bộ lọc đang áp"]');
        await page.waitForSelector('.modal.show', { timeout: 30000 });
        await settle(4000);
        await elShot(modal(), '19_printlist');
        await icon(page.locator('.modal.show button:has-text("In")').last(), 'btn_in_preview');
    }

    if (want('print')) {
        await gotoList();
        await rowOf('PGHHG-0' + ID_DONE).locator('[title="In"]').first().click();
        await page.waitForSelector('.modal.show', { timeout: 30000 });
        await settle(4000);
        await elShot(modal(), '18_print');
    }

    if (want('history')) {
        // Phiếu thật chưa có dòng lịch sử nào trên dev → dựng lịch sử minh họa từ chính dữ liệu phiếu
        const d = real.done;
        const ap = d.approvals || [];
        const WAIT = { 'Trưởng phòng': 'Chờ TP duyệt', 'Ban giám đốc': 'Chờ BGĐ duyệt', 'Kế toán': 'Chờ KT duyệt' };
        const KEY = { 'Trưởng phòng': 'tp_approve', 'Ban giám đốc': 'bgd_approve', 'Kế toán': 'kt_approve' };
        const steps = ap.map((a, i) => ({
            id: 10 + i, action: KEY[a.level], action_label: a.level + ' duyệt', action_color: '#16a34a',
            actor_name: a.approver_name, department_name: null, note: a.comment, created_at: a.approved_time, created_at_raw: null,
            changes: [{ field: 'Trạng thái', old: WAIT[a.level], new: ap[i + 1] ? WAIT[ap[i + 1].level] : 'Đã duyệt' }],
        }));
        MOCK = {
            [`${API}/${ID_DONE}/histories`]: (json) => ({
                ...json,
                data: [
                    ...steps.reverse(),
                    { id: 1, action: 'create', action_label: 'Tạo phiếu', action_color: '#2563eb', actor_name: d.creator_name,
                        department_name: d.department_name, note: null, created_at: d.created_at_time, created_at_raw: null,
                        changes: [{ field: 'Trạng thái', old: null, new: 'Chờ TP duyệt' }, { field: 'Ghi chú', old: null, new: d.note }] },
                ],
            }),
        };
        await gotoList();
        await rowOf('PGHHG-0' + ID_DONE).locator('[title="Lịch sử"]').first().click();
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(2500);
        await elShot(modal(), '16_history');
        await icon(page.locator('.modal.show button:has-text("Bộ lọc"), .modal.show [title*="lọc"]'), 'btn_boloc_ls');
        await icon(inModal('Đóng'), 'btn_dong_ls');
        await inModal('Đóng').first().click();
        MOCK = {};
    }

    if (want('detail')) {
        await page.goto(`${LIST_URL}/${ID_DONE}`);
        await page.waitForSelector(`text=PGHHG-0${ID_DONE}`, { timeout: 60000 });
        await settle(3000);
        await full('17_detail', { fullPage: true });
        await icon(page.locator('button:has-text("Xem lịch sử")'), 'btn_xemlichsu');
        await icon(page.locator('.v2-footer button:has-text("In"), footer button:has-text("In"), button[title="In phiếu yêu cầu gia hạn hàng giữ"]'), 'btn_in');
        await icon(page.locator('button:has-text("Quay lại")'), 'btn_quaylai');
    }

    if (want('approve')) {
        await page.goto(`${LIST_URL}/${ID_WAIT}`);
        await page.waitForSelector(`text=PGHHG-0${ID_WAIT}`, { timeout: 60000 });
        await settle(3000);
        await full('14_detail_approve', { fullPage: true });
        await icon(page.locator('button:has-text("BGĐ duyệt")'), 'btn_duyet');
        await icon(page.locator('button:has-text("Từ chối")').last(), 'btn_tuchoi');
        // Hộp xác nhận duyệt — chụp rồi HỦY
        await page.locator('button:has-text("BGĐ duyệt")').first().click();
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(800);
        await elShot(modal(), '14_approve');
        await icon(inModal('Duyệt'), 'btn_confirm_duyet');
        await icon(inModal('Hủy'), 'btn_huy_confirm');
        await inModal('Hủy').first().click();
        await page.waitForTimeout(1000);
        // Cửa sổ Từ chối — chụp rồi ĐÓNG
        await page.locator('button:has-text("Từ chối")').last().click();
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(800);
        await elShot(modal(), '15_reject');
        await icon(inModal('Xác nhận từ chối'), 'btn_confirm_tuchoi');
        await icon(inModal('Đóng'), 'btn_dong_reject');
        await inModal('Đóng').first().click();
    }

    if (want('edit')) {
        // Bật tạm: phiếu chờ duyệt hiển thị như phiếu Đang tạo của chính mình
        MOCK = {
            [`${API}/${ID_WAIT}`]: (json) => ({ ...json, data: { ...json.data, status: 3, status_name: 'Đang tạo', status_type: 'draft',
                status_color: '#64748B', approvals: [], products: json.data.products.slice(0, 5), is_can_edit: true, is_can_delete: true, is_can_approve: false } }),
        };
        await page.goto(`${LIST_URL}/${ID_WAIT}/edit`);
        await page.waitForSelector('button:has-text("Gửi duyệt")', { timeout: 60000 });
        await settle(3000);
        await full('12_edit', { fullPage: true });
        await icon(page.locator('button:has-text("Lưu nháp")'), 'btn_luunhap');
        await icon(page.locator('button:has-text("Gửi duyệt")'), 'btn_guiduyet');
        await icon(page.locator('button:has-text("Thêm tài liệu")'), 'btn_themtailieu');
        // Màn chi tiết của phiếu đó: nút Sửa / Xóa
        await page.goto(`${LIST_URL}/${ID_WAIT}`);
        await page.waitForSelector('button:has-text("Sửa")', { timeout: 60000 });
        await settle(2500);
        await icon(page.locator('button:has-text("Sửa")'), 'btn_sua');
        await icon(page.locator('button:has-text("Xóa")'), 'btn_xoa');
        MOCK = {};
    }

    if (want('delete')) {
        // Bật tạm: dòng đầu danh sách hiển thị như phiếu Đang tạo của chính mình (có Sửa / Xóa)
        MOCK = {
            [`${API}?`]: (json) => {
                const x = json.data.find((r) => r.id === ID_WAIT);
                Object.assign(x, { status: 3, status_name: 'Đang tạo', status_type: 'draft', status_color: '#64748B',
                    is_can_edit: true, is_can_delete: true, is_can_approve: false });
                return json;
            },
        };
        await gotoList();
        const rw = rowOf('PGHHG-0' + ID_WAIT);
        await icon(rw.locator('[title="Sửa"]'), 'btn_sua_row');
        await icon(rw.locator('[title="Xóa"]'), 'btn_xoa_row');
        await rw.locator('[title="Xóa"]').first().click();
        await page.waitForSelector('.modal.show', { timeout: 20000 });
        await settle(800);
        await elShot(modal(), '13_delete');
        await icon(inModal('Xóa'), 'btn_confirm_xoa');
        await inModal('Hủy').first().click();
        MOCK = {};
    }

    if (want('create')) {
        // Tài khoản test không giữ lô nào sắp hết hạn → nạp tạm các lô của phiếu thật để minh họa bảng Chi tiết
        const lots = (real.wait.products || []).slice(0, 5).map((p) => ({ ...p, customer_name: p.customer_name || '' }));
        MOCK = {
            [`${API}/stock`]: (json) => ({ ...json, data: { ...json.data, items: lots } }),
        };
        await page.goto(LIST_URL + '/create');
        await page.waitForSelector('button:has-text("Lưu nháp")', { timeout: 60000 });
        await settle(3000);
        // Tích dòng đầu để thấy ô Số lượng / Hạn giữ mới mở khóa
        const cb = page.locator('tbody tr').first().locator('input[type=checkbox], .custom-control-label, label').first();
        await cb.click().catch(() => console.log('không tích được dòng đầu'));
        await settle(800);
        await full('10_create', { fullPage: true });
        {
            const b = await page.locator('tbody tr').first().locator('td').nth(1).boundingBox();
            await page.screenshot({ path: path.join(ICON, 'o_tick.png'), clip: { x: b.x + b.width / 2 - 12, y: b.y + b.height / 2 - 12, width: 24, height: 24 } });
        }
        await icon(page.locator('button:has-text("Lưu và tiếp tục")'), 'btn_luutieptuc');
        MOCK = {};
    }

    if (want('menu')) {
        await gotoList();
        await page.mouse.move(760, 8);
        await page.waitForTimeout(1500);
        await page.mouse.click(88, 29);
        await page.waitForTimeout(800);
        await page.click('.modal.show button:has-text("Xác nhận")'); // chỉ ghi localStorage của trình duyệt headless (bật menu mở rộng)
        await settle(1500);
        await icon(page.locator('.logo-box'), 'menu_phanhe');
        await icon(page.locator('a.cat:has-text("Hàng hoá - Dịch vụ")'), 'menu_nhom');
        await page.click('a.cat:has-text("Hàng hoá - Dịch vụ")');
        await page.waitForTimeout(1200);
        await page.hover('a.scat:has-text("Giữ hàng")');
        await page.click('a.scat:has-text("Giữ hàng")');
        await settle(1200);
        await icon(page.locator('a.scat:has-text("Giữ hàng")'), 'menu_giuhang');
        await icon(page.locator('a:has-text("Yêu cầu gia hạn hàng giữ")').last(), 'menu_muc');
        await icon(page.locator('a:has-text("Phiếu Yêu cầu điều chuyển hàng giữ")').last(), 'menu_muc_33');
        await full('00_menu');
    }

    await o.browser.close();
})().catch(async (e) => {
    console.error(e);
    try { await page.screenshot({ path: path.join(HERE, 'capture_error.png') }); } catch (x) {}
    process.exit(1);
});

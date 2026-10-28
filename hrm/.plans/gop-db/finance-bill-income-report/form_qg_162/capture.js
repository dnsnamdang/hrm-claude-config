// Chụp ảnh HDSD/SRS màn Phiếu báo có + Tổng hợp tiền về ngân hàng trên DEV (headless riêng).
// AN TOÀN: chỉ mở màn / popup / hộp xác nhận rồi bấm Hủy / Đóng. KHÔNG bấm Lưu, Duyệt, Xóa, Import.
// Tài khoản test không thấy phiếu Đang tạo nào → nút Sửa/Xóa/Duyệt được BẬT TẠM HIỂN THỊ bằng cách sửa
// cờ is_can_edit/is_can_delete/is_can_approve trong phản hồi GET (chỉ trên trình duyệt, không ghi dữ liệu).
// Chạy: node capture.js [bước ...]   (không truyền = chụp hết)
const fs = require('fs');
const path = require('path');
const { open } = require('./devlib.js');

const SHOTS = path.join(__dirname, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
fs.mkdirSync(ICONS, { recursive: true });
const LIST = '/finance/bill-income-reports';
const SUM = '/finance/bill-income-reports/summarize-money';
const ONLY = process.argv.slice(2);

function mk(page) {
    const h = {};
    h.wait = (ms) => page.waitForTimeout(ms);
    // Chuột ra góc phải dưới — KHÔNG (5,5): rê vào rail trái làm sidebar bung che màn.
    h.mouseOut = async () => {
        const vp = page.viewportSize();
        await page.mouse.move(vp.width - 5, vp.height - 5);
        await page.waitForTimeout(400);
    };
    h.clip = async (name, box, pad = 0, dir = SHOTS) => {
        const vp = page.viewportSize();
        const x = Math.max(0, box.x - pad), y = Math.max(0, box.y - pad);
        const w = Math.min(vp.width - x, box.width + 2 * pad), hh = Math.min(vp.height - y, box.height + 2 * pad);
        await page.screenshot({ path: path.join(dir, name + '.png'), clip: { x, y, width: w, height: hh } });
    };
    h.el = async (name, loc, pad = 0) => {
        await loc.scrollIntoViewIfNeeded().catch(() => {});
        const b = await loc.boundingBox();
        if (!b) throw new Error('Không thấy ' + name);
        await h.clip(name, b, pad);
    };
    h.icon = async (name, loc, pad = 2) => {
        try {
            await loc.scrollIntoViewIfNeeded().catch(() => {});
            await page.waitForTimeout(200);
            const b = await loc.boundingBox();
            if (!b) throw new Error('không thấy');
            await h.clip(name, b, pad, ICONS);
        } catch (e) {
            console.log('WARN icon', name, e.message.split('\n')[0]);
        }
    };
    h.full = async (name) => {
        await h.mouseOut();
        await page.screenshot({ path: path.join(SHOTS, name + '.png') });
    };
    h.btn = (text, scope) =>
        (scope || page).locator('button:visible, a.btn:visible').filter({ hasText: new RegExp('^\\s*' + text + '\\s*$') });
    h.modal = () => page.locator('.modal.show .modal-content').last();
    return h;
}

/** Bật tạm cờ Sửa/Xóa/Duyệt (chỉ hiển thị) cho dòng đầu danh sách / phiếu đang mở. */
async function forceFlags(page) {
    await page.route(/\/finance\/bill-income-reports(\/\d+)?(\?.*)?$/, async (route) => {
        const req = route.request();
        if (req.method() !== 'GET' || !['xhr', 'fetch'].includes(req.resourceType())) return route.continue();
        const res = await route.fetch();
        const j = await res.json().catch(() => null);
        if (!j) return route.fulfill({ response: res });
        const fix = (o) => {
            if (o && typeof o === 'object') {
                o.is_can_edit = true;
                o.is_can_delete = true;
                o.is_can_approve = true;
                o.status = 1;
                o.status_text = 'Đang tạo';
                o.status_type = 'secondary';
                o.detail_ids_need_adjust_dept = [];
            }
        };
        if (Array.isArray(j.data)) j.data.slice(0, 1).forEach(fix);
        else if (j.data) fix(j.data);
        else fix(j);
        return route.fulfill({ response: res, json: j });
    });
}

const waitList = async (page) => {
    await page.getByText('PBC', { exact: false }).first().waitFor({ timeout: 30000 });
    await page.waitForTimeout(1200);
};

const STEPS = {
    async menu(page, h, go) {
        await page.setViewportSize({ width: 1080, height: 675 });
        await go(LIST);
        await waitList(page);
        await page.mouse.move(30, 383);
        await h.wait(900);
        await page.mouse.click(100, 383);
        await h.wait(1500);
        await page.screenshot({ path: path.join(__dirname, 'probe_menu.png') });
        await h.icon('menu_phanhe', page.locator('.subsystem-name').first().locator('xpath=..'), 4);
        await h.icon('menu_nhom', page.locator('.left-side-menu a.cat', { hasText: 'Quản lý tiền' }).first(), 0);
        await h.icon('menu_thanhtoan', page.locator('.scat-nm', { hasText: 'Thanh toán tiền mặt' }).first().locator('xpath=..'), 2);
        await h.icon('menu_muc', page.locator('.row-nm', { hasText: /^\s*Phiếu báo có\s*$/ }).first().locator('xpath=..'), 2);
        await h.icon('menu_tonghop', page.locator('.row-nm', { hasText: 'Tổng hợp tiền về ngân hàng' }).first().locator('xpath=..'), 2);
    },
    async list(page, h, go) {
        await page.setViewportSize({ width: 1440, height: 900 });
        await go(LIST);
        await waitList(page);
        await h.full('01_list');
        await h.icon('btn_timkiem', h.btn('Tìm kiếm').first());
        await h.icon('btn_lammoi', h.btn('Làm mới').first());
        await h.icon('btn_timkiemnangcao', h.btn('Tìm kiếm nâng cao').first());
        await h.icon('btn_caidatboloc', h.btn('Cài đặt bộ lọc').first());
        await h.icon('btn_taomoi', h.btn('Tạo mới').first());
        await h.icon('btn_import', h.btn('Import Excel').first());
        await h.icon('btn_cauhinhcot', page.locator('button[title="Cấu hình cột hiển thị"]').first());
        await h.icon('o_timnhanh', page.locator('input[placeholder^="Tìm theo mã phiếu"]').first(), 2);
        await h.btn('Tìm kiếm nâng cao').first().click();
        await h.wait(1500);
        await h.mouseOut();
        const card = page.locator('section.smart-filter-card').first();
        await h.el('02_filter', card, 0);
        const fld = (t) =>
            card.locator('.ff').filter({ has: page.locator('label', { hasText: new RegExp('^\\s*' + t + '\\s*$') }) }).first();
        const F = [
            ['o_congty', 'Công ty'], ['o_loaithu', 'Loại thu'], ['o_trangthai', 'Trạng thái'], ['o_nguoitao', 'Người tạo'],
            ['o_nganhang', 'Ngân hàng'], ['o_taikhoan', 'Tài khoản ngân hàng'], ['o_khachhang', 'Khách hàng'],
            ['o_tenkhach', 'Tên khách hàng \\(gõ tay\\)'], ['o_ghichu', 'Ghi chú'], ['o_khongbao', 'Không báo tiền về'],
            ['o_ngayhachtoan', 'Ngày hạch toán'], ['o_ngaytao', 'Ngày tạo'],
        ];
        for (const [n, t] of F) await h.icon(n, fld(t), 1);
    },
    async colcfg(page, h, go) {
        await page.setViewportSize({ width: 1440, height: 900 });
        await go(LIST);
        await waitList(page);
        await page.locator('button[title="Cấu hình cột hiển thị"]').first().click();
        await h.wait(1500);
        let m = h.modal();
        await h.mouseOut();
        await h.el('25_colcfg', m, 0);
        await h.icon('btn_chontatca', m.locator('button', { hasText: 'Chọn tất cả' }).first());
        await h.icon('btn_bochonhet', m.locator('button', { hasText: 'Bỏ chọn hết' }).first());
        await h.icon('btn_luu_col', m.locator('button', { hasText: 'Lưu' }).last());
        await h.icon('btn_dong_col', m.locator('button', { hasText: 'Đóng' }).last());
        await m.locator('button', { hasText: 'Đóng' }).last().click();
        await h.wait(800);
        await h.btn('Cài đặt bộ lọc').first().click();
        await h.wait(1500);
        m = h.modal();
        await h.mouseOut();
        await h.el('26_filtercfg', m, 0);
        await h.icon('btn_luu', m.locator('button', { hasText: 'Lưu' }).last());
        await h.icon('btn_khoiphuc', m.locator('button', { hasText: 'Khôi phục' }).first());
        await h.icon('btn_dong_filtercfg', m.locator('button', { hasText: 'Đóng' }).last());
        await m.locator('button', { hasText: 'Đóng' }).last().click();
    },
};

module.exports = { STEPS, mk, forceFlags, waitList, SHOTS, ICONS, LIST, SUM };

if (require.main === module) {
    (async () => {
        const p2 = path.join(__dirname, 'capture2.js');
        if (fs.existsSync(p2)) Object.assign(STEPS, require(p2));
        const { browser, page, go } = await open(__dirname, { scale: 1 });
        const h = mk(page);
        for (const [k, fn] of Object.entries(STEPS)) {
            if (ONLY.length && !ONLY.includes(k)) continue;
            try {
                await fn(page, h, go);
                console.log('OK', k);
            } catch (e) {
                console.log('FAIL', k, e.message.split('\n')[0]);
            }
            await page.unrouteAll({ behavior: 'ignoreErrors' }).catch(() => {});
        }
        await browser.close();
    })().catch((e) => {
        console.error(e);
        process.exit(1);
    });
}

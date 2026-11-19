// Hàm dùng chung cho capture.js của STT 232 + 233 (CSKH — Kiểm tra bảo hành sửa chữa).
//
// ⚠️ Tài khoản chụp ảnh trên dev KHÔNG có quyền xem theo cấp nên danh sách trả RỖNG. Để chụp được
// màn danh sách, script CHẶN request danh sách ngay trong trình duyệt và trả về các phiếu THẬT lấy từ
// API chi tiết (API chi tiết tài khoản này đọc được). Không ghi gì xuống máy chủ.
// Cờ hiện nút (is_can_*) chỉ được bật tạm trên trình duyệt khi cần chụp nút Sửa / Xóa / ...
const fs = require('fs');
const path = require('path');
const { openDev, DEV } = require('../../phieu-theo-form-quoc-gia/pw_dev.js');

async function start(stateDir, shotsDir) {
    fs.mkdirSync(path.join(shotsDir, 'icons'), { recursive: true });
    const r = await openDev(stateDir);
    const { page, ctx } = r;
    await page.setViewportSize({ width: 1600, height: 900 });
    await page.goto(DEV + '/customer-care/dashboard');
    await page.waitForLoadState('networkidle').catch(() => {});
    const tok = (await page.evaluate(() => localStorage.getItem('access_token'))).replace(/^Bearer /, '');
    r.api = async (u) => {
        const res = await ctx.request.get(DEV + '/api/v1/' + u, {
            headers: { Authorization: 'Bearer ' + tok, Accept: 'application/json' },
        });
        return (await res.json()).data;
    };
    r.shotsDir = shotsDir;
    return r;
}

/** Danh sách: trả về phiếu thật (đọc từ API chi tiết) cho request danh sách của `base`. */
async function mockList(r, base, ids, patch) {
    const rows = [];
    for (const id of ids) {
        const d = await r.api(`customer-care/${base}/${id}`);
        const row = Object.assign({}, d, {
            product_names: [...new Set((d.products || []).map((p) => p.product_name || p.product_no_sale_name).filter(Boolean))],
        });
        delete row.products;
        rows.push(patch ? patch(row) : row);
    }
    r.listRows = rows;
    const rx = new RegExp(`/api/v1/customer-care/${base}\\?`);
    await r.page.route(rx, async (route) => {
        const resp = await route.fetch();
        const j = await resp.json();
        j.data = r.listRows;
        if (j.meta) Object.assign(j.meta, { total: rows.length, from: 1, to: rows.length, last_page: 1 });
        await route.fulfill({ response: resp, json: j });
    });
}

/** Bật tạm cờ hiện nút ở API chi tiết (chỉ trên trình duyệt). */
async function patchDetail(r, base, id, patch) {
    const rx = new RegExp(`/api/v1/customer-care/${base}/${id}(\\?|$)`);
    await r.page.route(rx, async (route) => {
        if (route.request().method() !== 'GET') return route.continue();
        const resp = await route.fetch();
        const j = await resp.json();
        Object.assign(j.data, patch);
        await route.fulfill({ response: resp, json: j });
    });
}

async function settle(page, ms = 2500) {
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(ms);
    await page.mouse.move(page.viewportSize().width - 3, page.viewportSize().height - 3);
    await page.waitForTimeout(300);
}

async function shot(r, name, locator, opts = {}) {
    const p = path.join(r.shotsDir, name + '.png');
    if (locator) await locator.screenshot({ path: p });
    else if (opts.full) {
        // Cả trang: nới khung nhìn bằng chiều cao nội dung (fullPage làm thanh nút ghim đáy đè giữa ảnh)
        const vp = r.page.viewportSize();
        const h = await r.page.evaluate(() => {
            const els = [...document.querySelectorAll('.container-fluid, main, .content-page, .v2-styles')];
            return Math.max(900, ...els.map((e) => e.scrollHeight + e.getBoundingClientRect().top + 90));
        });
        await r.page.setViewportSize({ width: vp.width, height: Math.min(Math.ceil(h), 3000) });
        await r.page.waitForTimeout(1200);
        await r.page.mouse.move(vp.width - 3, 5);
        await r.page.screenshot({ path: p });
        await r.page.setViewportSize(vp);
    } else await r.page.screenshot({ path: p });
    console.log('shot', name);
}

async function icon(r, locator, name) {
    try {
        await locator.first().screenshot({ path: path.join(r.shotsDir, 'icons', name + '.png') });
        console.log('icon', name);
    } catch (e) {
        console.log('ICON FAIL', name, e.message.split('\n')[0]);
    }
}

/** Nút hiển thị theo đúng chữ (bỏ nút ẩn trùng tên). */
function btn(scope, text) {
    const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const rx = text instanceof RegExp ? text : new RegExp('^\\s*' + esc(text) + '\\s*$');
    return scope.locator('button:visible, a.btn:visible').filter({ hasText: rx });
}

/** Ảnh hộp thoại: modal đang mở cuối cùng. */
function lastModal(page) {
    return page.locator('.modal.show .modal-content').last();
}

/** Icon ô lọc: phần tử nhỏ nhất chứa nhãn mà rộng >= 150px (khung ô có nhãn floating). */
async function fieldIcon(r, label, name) {
    const box = await r.page.evaluate((label) => {
        const all = [...document.querySelectorAll('label, span, div, p')].filter((e) =>
            e.offsetParent && e.childElementCount === 0 && e.textContent.trim() === label);
        for (const e of all) {
            let a = e;
            while (a && a.getBoundingClientRect().width < 150) a = a.parentElement;
            if (a) { const b = a.getBoundingClientRect(); if (b.width < 700) return { x: b.x - 2, y: b.y - 4, width: b.width + 4, height: b.height + 8 }; }
        }
        return null;
    }, label);
    if (!box) return console.log('ICON FAIL', name);
    await r.page.screenshot({ path: path.join(r.shotsDir, 'icons', name + '.png'), clip: box });
    console.log('icon', name);
}

module.exports = { fieldIcon, btn, start, mockList, patchDetail, settle, shot, icon, lastModal, DEV };

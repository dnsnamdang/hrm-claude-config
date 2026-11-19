// Chụp ảnh SRS + HDSD màn "Báo cáo hàng có thể bán theo công ty" trên DEV (dev-hrm) — khuôn danh-muc-kho/docs/warehouses/capture.js.
// Màn CHỈ ĐỌC: chỉ bấm Tìm kiếm, đổi ĐVT, mở popup, Xuất Excel (file lưu trong hdsd_shots/), mở/đóng cửa sổ cấu hình.
// KHÔNG bấm Lưu ở cửa sổ Tuỳ chỉnh cột / Cài đặt bộ lọc (chỉ Đóng).
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/danh-muc-kho/docs/_capture_login.js');

const CFG = {
    route: '/lookup/stock-companies',
    nhom: 'Tra cứu tồn kho',
    muc: 'Hàng có thể bán theo công ty',
    search: 'Tìm theo tên, mã hoặc model hàng hóa',
    keywordRead: 'ENEO-AO', // 5 mặt hàng áo ENEOS — dùng cho PHẦN Đọc báo cáo
    unitCode: 'TATE-TZ-03', // hàng có 3 ĐVT (Cái / Vỉ x25 / Hộp x100)
    incomingCode: 'ENEO-700-V5231', // popup Hàng đang về 6 chứng từ
    filters: [
        ['Tồn theo công ty', 'o_congty'],
        ['Kho', 'o_kho'],
        ['Nhóm hàng hóa', 'o_nhom'],
        ['Tính chất hàng hóa', 'o_tinhchat'],
        ['Loại hàng hóa', 'o_loai'],
        ['Thương hiệu', 'o_thuonghieu'],
        ['Hãng sản xuất', 'o_hang'],
        ['Model', 'o_model'],
        ['Hàng hóa', 'o_hanghoa'],
    ],
};
const SHOTS = path.join(__dirname, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
fs.mkdirSync(ICONS, { recursive: true });
const ONLY = process.argv.slice(2);

const away = async (page) => {
    await page.mouse.move(1435, 895);
    await page.waitForTimeout(600);
};
const shot = async (page, name) => {
    await away(page);
    await page.screenshot({ path: path.join(SHOTS, name + '.png') });
};
const shotM = async (page, name, loc = null) => {
    await away(page);
    const box = loc || page.locator('.modal.show:visible .modal-content').last();
    await box.screenshot({ path: path.join(SHOTS, name + '.png') });
};
const icon = async (loc, name) => {
    await loc.first().scrollIntoViewIfNeeded().catch(() => {});
    await loc.first().screenshot({ path: path.join(ICONS, name + '.png') });
};
const clipIcon = async (page, loc, name, pad = 0, maxX = null) => {
    const b = await loc.first().boundingBox();
    const x = b.x - pad;
    const y = b.y - pad;
    let w = b.width + 2 * pad;
    const h = b.height + 2 * pad;
    if (maxX !== null && x + w > maxX) w = maxX - x;
    await page.screenshot({ path: path.join(ICONS, name + '.png'), clip: { x, y, width: w, height: h } });
};
const modal = (page) => page.locator('.modal.show:visible').last();
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\-]/g, '\\$&');
const ff = (page, label) =>
    page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + esc(label) + '\\s*\\*?\\s*$') }) });
const timing = {};

async function waitTable(page) {
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.locator('tr.summary-row').first().waitFor({ timeout: 120000 }).catch(() => {});
    await page.waitForTimeout(1500);
}
async function go(page) {
    const t0 = Date.now();
    await page.goto(DEV + CFG.route);
    await waitTable(page);
    timing.load = Date.now() - t0;
}
async function quick(page, kw) {
    await page.locator(`input[placeholder="${CFG.search}"]`).fill(kw);
    await page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }).first().click();
    await page.waitForTimeout(1000);
    await waitTable(page);
}
async function closeModal(page, text = /^\s*Đóng\s*$/) {
    const btn = modal(page).locator('button', { hasText: text });
    if (await btn.count()) await btn.last().click();
    else await page.keyboard.press('Escape');
    await page.waitForTimeout(1000);
}
const rowOf = (page, code) => page.locator('tbody tr').filter({ hasText: code }).first();
const save = (name, text) => fs.writeFileSync(path.join(SHOTS, name), text);

const steps = {
    async menu(page) {
        await go(page);
        await page.mouse.move(40, 300);
        await page.waitForTimeout(1200);
        await clipIcon(page, page.locator('a.logo').first(), 'menu_phanhe', 12, 218);
        const cat = page.locator('a.cat', { hasText: CFG.nhom }).first();
        await clipIcon(page, cat, 'menu_nhom', 0, 218);
        await cat.click();
        await page.waitForTimeout(1500);
        const item = page.getByText(CFG.muc, { exact: true });
        let el = null;
        for (let i = 0; i < (await item.count()); i++) {
            const b = await item.nth(i).boundingBox();
            if (b && b.x > 230) {
                el = item.nth(i);
                break;
            }
        }
        await clipIcon(page, el.locator('xpath=..'), 'menu_muc', 2);
        await page.screenshot({ path: path.join(SHOTS, '00_menu.png') });
    },
    async list(page) {
        await page.goto(DEV + '/');
        await page.evaluate(() => {
            try {
                localStorage.removeItem('lookup_stock_companies');
            } catch (e) {}
        });
        await go(page);
        console.log('thời gian tải (ms):', timing.load);
        save('_timing.txt', String(timing.load));
        await shot(page, '01_report');
        await icon(page.locator(`input[placeholder="${CFG.search}"]`).locator('xpath=..'), 'o_timnhanh');
        await icon(page.locator('button', { hasText: 'Tìm kiếm nâng cao' }), 'btn_timkiemnangcao');
        await icon(page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(page.locator('button', { hasText: 'Làm mới' }), 'btn_lammoi');
        await icon(page.locator('button', { hasText: 'Cài đặt bộ lọc' }), 'btn_caidatboloc');
        await icon(page.locator('button', { hasText: 'Xuất Excel' }), 'btn_xuatexcel');
        await icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        await page.locator('button', { hasText: 'Tìm kiếm nâng cao' }).first().click();
        await page.waitForTimeout(1500);
        await shot(page, '02_filter');
        for (const [lb, nm] of CFG.filters) {
            if (await ff(page, lb).count()) await icon(ff(page, lb), nm);
            else console.log('thiếu ô lọc', lb);
        }
        save('_filter_text.txt', await page.locator('body').innerText());
    },
    async required(page) {
        await go(page);
        await page.locator('button', { hasText: 'Tìm kiếm nâng cao' }).first().click();
        await page.waitForTimeout(1200);
        const box = ff(page, 'Tồn theo công ty');
        save('_company_box.txt', await box.first().innerHTML());
        const x = box.locator('.select2-selection__clear').first();
        if (await x.count()) await x.click({ force: true });
        else console.log('không thấy nút x ô công ty');
        await page.waitForTimeout(1500);
        await page.keyboard.press('Escape');
        await page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }).first().click();
        await page.waitForTimeout(1500);
        await shot(page, '03_required');
        save('_required_text.txt', await page.locator('body').innerText());
    },
    async read(page) {
        await go(page);
        await quick(page, CFG.keywordRead);
        await shot(page, '04_read');
        save('_read_text.txt', await page.locator('section.tp-card').last().innerText());
        const th = page.locator('thead th').filter({ hasText: 'SL tồn có thể bán' }).first();
        await icon(th.locator('.report-info-tip'), 'ic_info');
        await th.locator('.report-info-tip').hover();
        await page.waitForTimeout(1200);
        const pop = page.locator('.popover:visible').last();
        if (await pop.count()) {
            const b1 = await th.boundingBox();
            const b2 = await pop.boundingBox();
            const x = Math.max(0, Math.min(b1.x, b2.x) - 10);
            const y = Math.max(0, b1.y - 10);
            const w = Math.max(b1.x + b1.width, b2.x + b2.width) - x + 10;
            const h = b2.y + b2.height - y + 10;
            await page.screenshot({ path: path.join(SHOTS, '05_tooltip.png'), clip: { x, y, width: w, height: h } });
        } else console.log('không hiện popover ⓘ');
        await away(page);
    },
    // Bảng rộng: mở khung nhìn rộng để thấy MỌI cột của 5 dòng ví dụ, chỉ chụp khối bảng.
    async readwide(page) {
        await page.setViewportSize({ width: 2300, height: 900 });
        await go(page);
        await quick(page, CFG.keywordRead);
        await away(page);
        await page.locator('section.tp-card').last().screenshot({ path: path.join(SHOTS, '04b_read_wide.png') });
        await page.setViewportSize({ width: 1440, height: 900 });
    },
    // Nửa phải của bảng (cuộn ngang hết cỡ) — ảnh PHẦN Đọc báo cáo giữ cỡ chữ đọc được.
    async readright(page) {
        await go(page);
        await quick(page, CFG.keywordRead);
        await page.locator('.table-wrapper').first().evaluate((el) => {
            el.scrollLeft = el.scrollWidth;
        });
        await page.waitForTimeout(800);
        await away(page);
        await page.locator('section.tp-card').last().screenshot({ path: path.join(SHOTS, '04c_read_right.png') });
        await page.locator('section.tp-card').last().screenshot({ path: path.join(SHOTS, '04a_read_left.png') }).catch(() => {});
        await page.locator('.table-wrapper').first().evaluate((el) => {
            el.scrollLeft = 0;
        });
        await page.waitForTimeout(500);
        await away(page);
        await page.locator('section.tp-card').last().screenshot({ path: path.join(SHOTS, '04a_read_left.png') });
    },
    async unitwide(page) {
        await page.setViewportSize({ width: 2300, height: 900 });
        await go(page);
        await quick(page, CFG.unitCode);
        const row = rowOf(page, CFG.unitCode);
        await row.locator('select.unit-select').selectOption({ index: 2 });
        await page.waitForTimeout(800);
        await away(page);
        await page.locator('section.tp-card').last().screenshot({ path: path.join(SHOTS, '06_unit_wide.png') });
        save('_unit_wide.txt', await page.locator('section.tp-card').last().innerText());
        await page.setViewportSize({ width: 1440, height: 900 });
    },
    async unit(page) {
        await go(page);
        await quick(page, CFG.unitCode);
        const row = rowOf(page, CFG.unitCode);
        const sel = row.locator('select.unit-select');
        await icon(sel, 'o_dvt');
        await shot(page, '06_unit_before');
        const opts = await sel.locator('option').allInnerTexts();
        save('_unit_opts.txt', opts.join('\n'));
        save('_unit_before.txt', await row.innerText());
        await sel.selectOption({ index: opts.length - 1 });
        await page.waitForTimeout(800);
        await shot(page, '06_unit_after');
        await away(page);
        await page.locator('section.tp-card').last().screenshot({ path: path.join(SHOTS, '06_unit_card.png') });
        save('_unit_text.txt', await page.locator('section.tp-card').last().innerText());
    },
    async incoming(page) {
        await go(page);
        await quick(page, CFG.incomingCode);
        const row = rowOf(page, CFG.incomingCode);
        const link = row.locator('a.v2-cell-link').first();
        await icon(link, 'link_tonkho');
        await link.click();
        await page.waitForTimeout(1500);
        await page.locator('.modal.show:visible tbody tr').first().waitFor({ timeout: 60000 }).catch(() => {});
        await page.waitForTimeout(1500);
        await shotM(page, '07_incoming');
        save('_incoming_text.txt', await modal(page).innerText());
        await icon(modal(page).locator('button', { hasText: /^\s*Đóng\s*$/ }), 'btn_dong_popup');
        await closeModal(page);
    },
    async export(page) {
        await go(page);
        await quick(page, CFG.keywordRead);
        await page.locator('button', { hasText: 'Xuất Excel' }).first().click();
        await page.waitForTimeout(1500);
        await shotM(page, '08_export');
        const m = modal(page);
        await icon(m.locator('button', { hasText: 'Xuất file' }), 'btn_xuatfile');
        await icon(m.locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await icon(m.locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        await icon(m.locator('button', { hasText: /^\s*Đóng\s*$/ }), 'btn_dong');
        save('_export_text.txt', await m.innerText());
        const t0 = Date.now();
        const [dl] = await Promise.all([
            page.waitForEvent('download', { timeout: 180000 }),
            m.locator('button', { hasText: 'Xuất file' }).click(),
        ]);
        await dl.saveAs(path.join(SHOTS, '_export_' + dl.suggestedFilename()));
        console.log('xuất file:', dl.suggestedFilename(), Date.now() - t0, 'ms');
        await page.waitForTimeout(1500);
    },
    async colcfg(page) {
        await go(page);
        await page.locator('button[title="Cấu hình cột hiển thị"]').first().click();
        await page.waitForTimeout(1500);
        await shotM(page, '09_colcfg');
        save('_colcfg_text.txt', await modal(page).innerText());
        await icon(modal(page).locator('button', { hasText: /^\s*Lưu\s*$/ }), 'btn_luu');
        await closeModal(page);
    },
    async filtercfg(page) {
        await go(page);
        await page.locator('button', { hasText: 'Cài đặt bộ lọc' }).first().click();
        await page.waitForTimeout(1500);
        await shotM(page, '10_filtercfg');
        save('_filtercfg_text.txt', await modal(page).innerText());
        await closeModal(page);
    },
};

(async () => {
    const { browser, page } = await open(__dirname);
    try {
        for (const [k, f] of Object.entries(steps)) {
            if (ONLY.length && !ONLY.includes(k)) continue;
            console.log('==', k);
            try {
                await f(page);
            } catch (e) {
                console.log('LỖI bước', k, e.message.split('\n')[0]);
            }
        }
    } finally {
        await browser.close();
    }
})().catch((e) => {
    console.error(e);
    process.exit(1);
});

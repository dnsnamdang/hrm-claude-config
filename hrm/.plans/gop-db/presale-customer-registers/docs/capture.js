// Chụp ảnh SRS + HDSD màn "Danh sách đăng ký khách hàng toàn công ty" trên DEV (dev-hrm) — khuôn
// lookup-stock-companies/docs/capture.js + sale-customer-debt-reports/docs/compare/capture.js.
// Màn CHỈ ĐỌC: chỉ Tìm kiếm, lọc, sắp xếp, Xuất Excel (file lưu trong hdsd_shots/), mở/đóng cửa sổ cấu hình.
// KHÔNG bấm Lưu ở cửa sổ Tuỳ chỉnh cột / Cài đặt bộ lọc (chỉ Đóng).
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/danh-muc-kho/docs/_capture_login.js');

const CFG = {
    route: '/assign/report/customer-registers',
    rail: 'Báo cáo',
    group: 'Báo cáo thị trường',
    item: 'Danh sách đăng ký khách hàng toàn công ty',
    search: 'Tìm theo khách hàng, người liên hệ, người đăng ký, số báo giá',
    lsKey: 'assign_customer_registers',
    filters: [
        ['Khách hàng đăng ký', 'o_khachhang'],
        ['Thời hạn đăng ký', 'o_thoihan'],
        ['Người đăng ký', 'o_nguoidk'],
        ['Số báo giá', 'o_sobaogia'],
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
const shotM = async (page, name) => {
    await away(page);
    await page.locator('.modal.show:visible .modal-content').last().screenshot({ path: path.join(SHOTS, name + '.png') });
};
const card = (page) => page.locator('section.tp-card').last();
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
const save = (name, text) => fs.writeFileSync(path.join(SHOTS, name), typeof text === 'string' ? text : JSON.stringify(text, null, 1));
const footer = async (page) => {
    const t = await page.locator('body').innerText();
    const m = /Hiển thị[^\n]*/.exec(t);
    return m ? m[0] : '(không có chân bảng)';
};
let lastJson = null;

async function waitTable(page) {
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.locator('tbody tr').first().waitFor({ timeout: 60000 }).catch(() => {});
    await page.waitForTimeout(1500);
}
async function go(page, clear = true) {
    if (clear) {
        await page.goto(DEV + '/');
        await page.evaluate((k) => {
            try {
                localStorage.removeItem(k);
            } catch (e) {}
        }, CFG.lsKey);
    }
    const t0 = Date.now();
    await page.goto(DEV + CFG.route);
    await waitTable(page);
    return Date.now() - t0;
}
async function quick(page, kw) {
    await page.locator(`input[placeholder="${CFG.search}"]`).fill(kw);
    await page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }).first().click();
    await page.waitForTimeout(1000);
    await waitTable(page);
}
async function adv(page) {
    await page.locator('button', { hasText: /tìm kiếm nâng cao/i }).first().click();
    await page.waitForTimeout(1200);
}
async function pickSel(page, label, text, type = null) {
    await ff(page, label).locator('.select2-selection').first().click();
    await page.waitForTimeout(500);
    if (type) await page.keyboard.type(type, { delay: 40 });
    const opt = page.locator('.select2-results__option', { hasText: text }).first();
    await opt.waitFor({ timeout: 30000 });
    await opt.click();
    await page.waitForTimeout(800);
    await waitTable(page);
}
async function closeModal(page) {
    const btn = modal(page).locator('button', { hasText: /^\s*Đóng\s*$/ });
    if (await btn.count()) await btn.last().click();
    else await page.keyboard.press('Escape');
    await page.waitForTimeout(1000);
}

const steps = {
    async menu(page) {
        await go(page);
        await page.mouse.move(40, 300);
        await page.waitForTimeout(1200);
        await clipIcon(page, page.locator('a.logo').first(), 'menu_phanhe', 12, 218);
        const cat = page.locator('a.cat', { hasText: new RegExp('^\\s*' + CFG.rail + '\\s*$') }).first();
        await clipIcon(page, cat, 'menu_nhom', 0, 218);
        await cat.click();
        await page.waitForTimeout(1500);
        const grp = page.getByText(CFG.group, { exact: true });
        for (let i = 0; i < (await grp.count()); i++) {
            const b = await grp.nth(i).boundingBox();
            if (b && b.x > 200) {
                await clipIcon(page, grp.nth(i).locator('xpath=..'), 'menu_nhomcon', 2);
                break;
            }
        }
        await page.screenshot({ path: path.join(SHOTS, '00_menu.png') });
        const item = page.getByText(CFG.item, { exact: true });
        for (let i = 0; i < (await item.count()); i++) {
            const b = await item.nth(i).boundingBox();
            if (b && b.x > 230) {
                await clipIcon(page, item.nth(i).locator('xpath=..'), 'menu_muc', 2);
                break;
            }
        }
        save('_menu_text.txt', await page.locator('body').innerText());
    },
    async list(page) {
        const ms = await go(page);
        console.log('thời gian tải (ms):', ms);
        save('_timing.txt', String(ms));
        await shot(page, '01_list');
        save('_list_footer.txt', await footer(page));
        save('_page1.json', lastJson);
        await icon(page.locator(`input[placeholder="${CFG.search}"]`).locator('xpath=..'), 'o_timnhanh');
        await icon(page.locator('button', { hasText: /tìm kiếm nâng cao/i }), 'btn_timkiemnangcao');
        await icon(page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(page.locator('button', { hasText: 'Làm mới' }), 'btn_lammoi');
        await icon(page.locator('button', { hasText: 'Cài đặt bộ lọc' }), 'btn_caidatboloc');
        await icon(page.locator('button', { hasText: 'Xuất Excel' }), 'btn_xuatexcel');
        await icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        const link = page.locator('tbody a.v2-cell-link').first();
        if (await link.count()) await icon(link, 'link_sobaogia');
        await page.evaluate(() => window.scrollTo(0, 0));
        await away(page);
        await card(page).screenshot({ path: path.join(SHOTS, '05_read.png') });
        save('_read_text.txt', await card(page).innerText());
    },
    async filter(page) {
        await go(page);
        await adv(page);
        await shot(page, '02_filter');
        for (const [lb, nm] of CFG.filters) {
            if (await ff(page, lb).count()) await icon(ff(page, lb), nm);
            else console.log('thiếu ô lọc', lb);
        }
        save('_filter_text.txt', await page.locator('body').innerText());
        const counts = { tong: await footer(page) };
        await pickSel(page, 'Thời hạn đăng ký', 'Còn hạn');
        counts.con_han = await footer(page);
        await shot(page, '03_conhan');
        await pickSel(page, 'Thời hạn đăng ký', 'Hết hạn');
        counts.het_han = await footer(page);
        save('_counts.json', counts);
        console.log(counts);
    },
    async empty(page) {
        await go(page);
        await quick(page, 'zzzkhongtontai999');
        await page.waitForTimeout(1000);
        await shot(page, '04_empty');
        save('_empty_text.txt', await card(page).innerText().catch(() => ''));
    },
    async sort(page) {
        await go(page);
        const th = page.locator('thead th', { hasText: 'Thời hạn đăng ký' }).first();
        await th.click();
        await page.waitForTimeout(1500);
        await waitTable(page);
        save('_sort1.txt', await card(page).innerText());
        await th.click();
        await page.waitForTimeout(1500);
        await waitTable(page);
        await shot(page, '06_sort');
        save('_sort2.txt', await card(page).innerText());
        await th.click();
        await page.waitForTimeout(1500);
        await waitTable(page);
        save('_sort3.txt', await card(page).innerText());
    },
    async keyword(page) {
        await go(page);
        await quick(page, 'TOYOTA');
        await shot(page, '07_keyword');
        save('_keyword.txt', await footer(page));
    },
    async export(page) {
        await go(page);
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
        save('_export_toast.txt', await page.locator('body').innerText());
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
    page.on('response', async (r) => {
        if (/api\/v1\/assign\/report\/customer-registers\?/.test(r.url())) {
            try {
                lastJson = await r.json();
            } catch (e) {}
        }
    });
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

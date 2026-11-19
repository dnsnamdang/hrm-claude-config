// Chụp ảnh SRS + HDSD màn "Báo cáo phân chia thị trường" trên DEV (dev-hrm) — khuôn lookup-stock-companies/docs/capture.js.
// Màn CHỈ ĐỌC: chỉ Tìm kiếm, mở popup, Xuất Excel (file lưu trong hdsd_shots/), xem trước In (không bấm In ra máy in),
// mở / Đóng cửa sổ cấu hình (KHÔNG bấm Lưu).
// Bộ lọc đặt sẵn qua bộ nhớ bộ lọc 10 phút của chính màn (giống người dùng lọc rồi quay lại) rồi mở màn.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/danh-muc-kho/docs/_capture_login.js');

const CFG = {
    route: '/assign/report/division-market',
    lsKey: 'assign_division_market_report',
    search: 'Tìm theo tỉnh/TP, phường/xã, phòng, nhân viên hoặc số điện thoại',
    filters: [
        ['Quốc gia', 'o_quocgia'], ['Vùng', 'o_vung'], ['Tỉnh/TP', 'o_tinh'], ['Phường/Xã', 'o_xa'],
        ['Phụ trách tất cả các hãng', 'o_phutrach'], ['Phòng phụ trách', 'o_phong'],
        ['Nhân viên phụ trách', 'o_nhanvien'], ['Hãng xe', 'o_hangxe'],
    ],
};
const BASE = { keyword: '', nation_id: '', area_ids: [], province_ids: [], ward_ids: [], in_charge: '', department_ids: [], employee_ids: [], vehicle_manufact_ids: [] };
const SHOTS = path.join(__dirname, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
fs.mkdirSync(ICONS, { recursive: true });
const ONLY = process.argv.slice(2);

const away = async (page) => { await page.mouse.move(1435, 895); await page.waitForTimeout(600); };
const shot = async (page, name) => { await away(page); await page.screenshot({ path: path.join(SHOTS, name + '.png') }); };
const modal = (page) => page.locator('.modal.show:visible').last();
const shotM = async (page, name) => { await away(page); await modal(page).locator('.modal-content').last().screenshot({ path: path.join(SHOTS, name + '.png') }); };
const icon = async (loc, name) => { await loc.first().scrollIntoViewIfNeeded().catch(() => {}); await loc.first().screenshot({ path: path.join(ICONS, name + '.png') }); };
const clipIcon = async (page, loc, name, pad = 0, maxX = null) => {
    const b = await loc.first().boundingBox();
    const x = b.x - pad, y = b.y - pad;
    let w = b.width + 2 * pad;
    const h = b.height + 2 * pad;
    if (maxX !== null && x + w > maxX) w = maxX - x;
    await page.screenshot({ path: path.join(ICONS, name + '.png'), clip: { x, y, width: w, height: h } });
};
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\-]/g, '\\$&');
const ff = (page, label) => page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + esc(label) + '\\s*\\*?\\s*$') }) });
const save = (name, text) => fs.writeFileSync(path.join(SHOTS, name), text);
const card = (page) => page.locator('section.tp-card').last();

async function waitTable(page) {
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForFunction(() => !document.querySelector('.ri-loader-4-line.rotating'), null, { timeout: 120000 }).catch(() => {});
    await page.waitForTimeout(1500);
}
// Mở màn với bộ lọc đặt sẵn (f = phần khác mặc định); f = null -> xoá bộ lọc đã nhớ.
async function go(page, f = null) {
    await page.goto(DEV + '/');
    await page.evaluate(([k, v]) => {
        try {
            if (v) localStorage.setItem(k, JSON.stringify({ filter: v, filterCollapsed: false, timestamp: Date.now() }));
            else localStorage.removeItem(k);
        } catch (e) {}
    }, [CFG.lsKey, f ? Object.assign({}, BASE, f) : null]);
    const t0 = Date.now();
    await page.goto(DEV + CFG.route);
    await waitTable(page);
    return Date.now() - t0;
}

const steps = {
    async menu(page) {
        await go(page, { keyword: 'zzz-khong-co' });
        await page.mouse.move(30, 400);
        await page.waitForTimeout(1200);
        await clipIcon(page, page.locator('a.logo').first(), 'menu_phanhe', 6, 210);
        const cat = page.locator('.left-side-menu a.cat').filter({ hasText: /^\s*Báo cáo\s*$/ }).first();
        await clipIcon(page, cat, 'menu_nhom', 0, 200);
        await cat.click();
        await page.waitForTimeout(1500);
        const scat = page.locator('a.scat').filter({ hasText: 'Báo cáo thị trường' }).first();
        await scat.click();
        await page.waitForTimeout(800);
        await clipIcon(page, scat, 'menu_nhomcon', 2);
        const item = page.getByText('Báo cáo phân chia thị trường', { exact: true });
        let el = null;
        for (let i = 0; i < (await item.count()); i++) {
            const b = await item.nth(i).boundingBox();
            if (b && b.x > 440) { el = item.nth(i); break; }
        }
        await clipIcon(page, el.locator('xpath=..'), 'menu_muc', 4);
        // mục menu nằm trong ô rộng: cắt bớt phần trắng bên phải (làm ở gen_hdsd/gen_srs bằng PIL — xem crop_menu.py)
        await page.screenshot({ path: path.join(SHOTS, '00_menu.png') });
    },
    async list(page) {
        const ms = await go(page, null);
        console.log('thời gian tải (ms):', ms);
        save('_timing.txt', String(ms));
        await shot(page, '01_report');
        save('_list_text.txt', await page.locator('body').innerText());
        await icon(page.locator(`input[placeholder="${CFG.search}"]`).locator('xpath=..'), 'o_timnhanh');
        await icon(page.locator('button', { hasText: 'tìm kiếm nâng cao' }), 'btn_timkiemnangcao');
        await icon(page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(page.locator('button', { hasText: 'Làm mới' }), 'btn_lammoi');
        await icon(page.locator('button', { hasText: 'Cài đặt bộ lọc' }), 'btn_caidatboloc');
        await icon(page.locator('button', { hasText: /^\s*In\s*$/ }), 'btn_in');
        await icon(page.locator('button', { hasText: 'Xuất Excel' }), 'btn_xuatexcel');
        await icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        for (const [lb, nm] of CFG.filters) {
            if (await ff(page, lb).count()) await icon(ff(page, lb), nm);
            else console.log('thiếu ô lọc', lb);
        }
        const pg = page.locator('.page-size-select').first().locator('xpath=../..');
        await pg.scrollIntoViewIfNeeded().catch(() => {});
        await away(page);
        await pg.screenshot({ path: path.join(SHOTS, '01b_paging.png') }).catch((e) => console.log('paging', e.message));
        save('_paging_text.txt', await pg.innerText().catch(() => ''));
    },
    async filter(page) {
        // Tỉnh Khánh Hòa + Phụ trách tất cả các hãng = Không
        const ms = await go(page, { province_ids: [6], in_charge: 2 });
        console.log('lọc (ms):', ms);
        await shot(page, '02_filter');
        save('_filter_text.txt', await card(page).innerText());
    },
    async read(page) {
        await go(page, { keyword: 'Âu Lâu' });
        await away(page);
        await card(page).screenshot({ path: path.join(SHOTS, '04_read.png') });
        save('_read_text.txt', await card(page).innerText());
        const th = page.locator('thead th').filter({ hasText: 'Phụ trách tất cả các hãng' }).first();
        save('_th_html.txt', await th.innerHTML());
        const tip = th.locator('.report-info-tip, i, svg').first();
        await icon(tip, 'ic_info');
        await tip.hover();
        await page.waitForTimeout(1200);
        const pop = page.locator('.popover:visible, .tooltip:visible').last();
        if (await pop.count()) {
            const b1 = await th.boundingBox();
            const b2 = await pop.boundingBox();
            const x = Math.max(0, Math.min(b1.x, b2.x) - 10);
            const y = Math.max(0, Math.min(b1.y, b2.y) - 10);
            const w = Math.max(b1.x + b1.width, b2.x + b2.width) - x + 10;
            const h = Math.max(b1.y + b1.height, b2.y + b2.height) - y + 10;
            await page.screenshot({ path: path.join(SHOTS, '05_tooltip.png'), clip: { x, y, width: w, height: h } });
            save('_tooltip_text.txt', await pop.innerText());
        } else console.log('không hiện popover ⓘ');
    },
    async empty(page) {
        await go(page, { keyword: 'zzzkhongtontai999' });
        await away(page);
        await card(page).screenshot({ path: path.join(SHOTS, '06_empty.png') });
    },
    async export(page) {
        await go(page, { keyword: 'Âu Lâu' });
        await page.locator('button', { hasText: 'Xuất Excel' }).first().click();
        await page.waitForTimeout(1500);
        await shotM(page, '08_export');
        const m = modal(page);
        await icon(m.locator('button', { hasText: 'Xuất file' }), 'btn_xuatfile');
        await icon(m.locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await icon(m.locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        await icon(m.locator('button', { hasText: /^\s*Đóng\s*$/ }), 'btn_dong');
        save('_export_text.txt', await m.innerText());
        const [dl] = await Promise.all([
            page.waitForEvent('download', { timeout: 180000 }),
            m.locator('button', { hasText: 'Xuất file' }).click(),
        ]);
        await dl.saveAs(path.join(SHOTS, '_export_' + dl.suggestedFilename()));
        console.log('xuất file:', dl.suggestedFilename());
        await page.waitForTimeout(1500);
    },
    async print(page) {
        await go(page, { keyword: 'Âu Lâu' });
        await page.locator('button', { hasText: /^\s*In\s*$/ }).first().click();
        await page.waitForTimeout(2000);
        await page.locator('.modal.show:visible iframe').first().waitFor({ timeout: 90000 }).catch(() => {});
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(3000);
        await shotM(page, '10_print');
        save('_print_text.txt', await modal(page).innerText());
        const b = modal(page).locator('button').filter({ hasText: /^\s*In\s*$/ });
        if (await b.count()) await icon(b, 'btn_in_popup');
        else console.log('không thấy nút In trong popup');
        await page.keyboard.press('Escape');
        await page.waitForTimeout(800);
    },
    async printlimit(page) {
        await go(page, null);
        await page.locator('button', { hasText: /^\s*In\s*$/ }).first().click();
        await page.waitForTimeout(3000);
        await page.waitForFunction(() => {
            const m = document.querySelector('.modal.show');
            return m && /vượt|Không có dữ liệu|<table/i.test(m.innerHTML) && !m.querySelector('.spinner-border');
        }, null, { timeout: 120000 }).catch(() => {});
        await page.waitForTimeout(3000);
        await shotM(page, '10b_print_limit');
        save('_printlimit_text.txt', await modal(page).innerText());
        await page.keyboard.press('Escape');
    },
    async colcfg(page) {
        await go(page, { keyword: 'Âu Lâu' });
        await page.locator('button[title="Cấu hình cột hiển thị"]').first().click();
        await page.waitForTimeout(1500);
        await shotM(page, '09_colcfg');
        save('_colcfg_text.txt', await modal(page).innerText());
        await icon(modal(page).locator('button', { hasText: /^\s*Lưu\s*$/ }), 'btn_luu');
        const d = modal(page).locator('button', { hasText: /^\s*Đóng\s*$/ });
        if (await d.count()) await d.last().click(); else await page.keyboard.press('Escape');
        await page.waitForTimeout(800);
    },
    async filtercfg(page) {
        await go(page, { keyword: 'Âu Lâu' });
        await page.locator('button', { hasText: 'Cài đặt bộ lọc' }).first().click();
        await page.waitForTimeout(1500);
        await shotM(page, '11_filtercfg');
        save('_filtercfg_text.txt', await modal(page).innerText());
        const d = modal(page).locator('button', { hasText: /^\s*Đóng\s*$/ });
        if (await d.count()) await d.last().click(); else await page.keyboard.press('Escape');
    },
};

(async () => {
    const { browser, page } = await open(__dirname);
    page.on('dialog', (d) => d.dismiss().catch(() => {}));
    try {
        for (const [k, f] of Object.entries(steps)) {
            if (ONLY.length && !ONLY.includes(k)) continue;
            console.log('==', k);
            try { await f(page); } catch (e) { console.log('LỖI bước', k, e.message.split('\n')[0]); }
        }
    } finally {
        await browser.close();
    }
})().catch((e) => { console.error(e); process.exit(1); });

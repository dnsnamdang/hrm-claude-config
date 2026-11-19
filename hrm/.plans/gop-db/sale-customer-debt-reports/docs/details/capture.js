// Chụp ảnh SRS + HDSD "BC chi tiết công nợ KH" trên DEV (dev-hrm), headless riêng.
// Màn CHỈ ĐỌC: chỉ chọn bộ lọc, bấm Tìm kiếm, mở popup chứng từ, mở cửa sổ Xuất Excel + tải file (để trong thư mục này).
// KHÔNG bấm Lưu / Xoá / Duyệt bất kỳ phiếu nào.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('../../../danh-muc-kho/docs/_capture_login.js');

const CFG = {
    route: '/sale/customer-debt-details',
    rail: 'Báo cáo',
    nhom: 'Báo cáo công nợ',
    muc: 'Chi tiết công nợ KH',
    search: 'Tìm theo số hợp đồng, mã hoặc tên khách hàng',
    start: '2026-10-01',
    end: '2026-10-31',
    // KH có đủ số ở nhiều cột trong tháng 10/2026 (dò 02/11/2026), 3 hợp đồng — dùng cho ảnh đọc báo cáo + popup
    customerCode: '89THUPTR-62',
    filters: [
        ['Thời gian', 'o_thoigian'],
        ['Khách hàng', 'o_khachhang'],
        ['Số hợp đồng', 'o_sohopdong'],
        ['Số dư cuối kỳ', 'o_soducuoiky'],
        ['Công ty', 'o_congty'],
        ['Phòng ban', 'o_phongban'],
        ['Bộ phận', 'o_bophan'],
        ['Nhân viên', 'o_nhanvien'],
    ],
};
const SHOTS = path.join(__dirname, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
fs.mkdirSync(ICONS, { recursive: true });
const ONLY = process.argv.slice(2);
const LOG = {};
const logFile = path.join(SHOTS, '_capture_log.json');
if (fs.existsSync(logFile)) Object.assign(LOG, JSON.parse(fs.readFileSync(logFile, 'utf8')));

const away = async (page) => {
    await page.mouse.move(1435, 895);
    await page.waitForTimeout(500);
};
const shot = async (page, name) => {
    await away(page);
    await page.screenshot({ path: path.join(SHOTS, name + '.png') });
};
const shotEl = async (page, loc, name) => {
    await away(page);
    await loc.screenshot({ path: path.join(SHOTS, name + '.png') });
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
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\-]/g, '\\$&');
const ff = (page, label) =>
    page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + esc(label) + '\\s*\\*?\\s*$') }) });

async function go(page) {
    await page.goto(DEV + CFG.route);
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(2000);
}
// Đặt bộ lọc qua chính component trang (giống người dùng chọn ô) rồi chờ bảng có dòng
async function setFilters(page, patch) {
    const t0 = Date.now();
    await page.evaluate((patch) => {
        let vm = null;
        for (const el of document.querySelectorAll('div')) {
            const v = el.__vue__;
            if (v && v.localStorageKey === 'sale_customer_debt_details') { vm = v; break; }
        }
        Object.keys(patch).forEach((k) => vm.$set(vm.filters, k, patch[k]));
    }, patch);
    await page.waitForTimeout(500);
    await page.locator('tr.row-contract, td:has-text("Không có dữ liệu")').first().waitFor({ timeout: 120000 });
    await page.waitForLoadState('networkidle').catch(() => {});
    const ms = Date.now() - t0;
    await page.waitForTimeout(1500);
    return ms;
}
async function customerOption(page, code) {
    return page.evaluate(async (code) => {
        const r = await window.$nuxt.$store.dispatch('apiGetMethod', { url: 'assign/customers/search', params: { q: code } });
        const it = (r.data || []).find((x) => String(x.text).includes(code)) || r.data[0];
        return { id: it.id, text: it.text };
    }, code);
}
async function withCustomer(page) {
    await go(page);
    const opt = await customerOption(page, CFG.customerCode);
    LOG.customer = opt;
    await setFilters(page, { start_date: CFG.start, end_date: CFG.end, customer_id: opt.id, customer_option: opt });
    return opt;
}
const tableBox = (page) => page.locator('section.tp-card:has(table.report-table)').first();
async function scrollTable(page, where) {
    await page.evaluate((where) => {
        const t = document.querySelector('section.tp-card table.report-table');
        let el = t.parentElement;
        while (el && el.scrollWidth <= el.clientWidth) el = el.parentElement;
        if (el) el.scrollLeft = where === 'right' ? el.scrollWidth : 0;
        document.querySelectorAll('section.tp-card *').forEach((x) => {
            if (x.scrollWidth > x.clientWidth + 5 && getComputedStyle(x).overflowX !== 'visible') x.scrollLeft = where === 'right' ? x.scrollWidth : 0;
        });
    }, where);
    await page.waitForTimeout(600);
}
// Ô số tiền bấm được của dòng hợp đồng / khách hàng theo vị trí cột (thứ tự cột trên bảng, 1-based)
const COL = { opening: 6, total_payable: 7, adjust_debt: 8, increase: 9, total_returned: 10, total_paid: 11, adjust_has: 12, decrease: 13, refund: 14, closing: 15 };

const steps = {
    async menu(page) {
        await go(page);
        await page.mouse.move(40, 300);
        await page.waitForTimeout(1200);
        await clipIcon(page, page.locator('a.logo').first(), 'menu_phanhe', 10, 218);
        const cat = page.locator('.left-side-menu .cats-list a.cat').filter({ hasText: new RegExp('^\\s*' + CFG.rail + '\\s*$') }).first();
        await clipIcon(page, cat, 'menu_nhom', 0, 200);
        await cat.click();
        await page.waitForTimeout(1500);
        const pick = async (text, min) => {
            const items = page.getByText(text, { exact: true });
            for (let i = 0; i < (await items.count()); i++) {
                const b = await items.nth(i).boundingBox();
                if (b && b.x > min && b.y > 90) return items.nth(i);
            }
            return null;
        };
        const g = await pick(CFG.nhom, 230);
        if (g) {
            await g.click();
            await page.waitForTimeout(1200);
            const g2 = await pick(CFG.nhom, 230);
            await clipIcon(page, g2.locator('xpath=..'), 'menu_nhomcon', 2, 600);
        } else console.log('không thấy nhóm', CFG.nhom);
        const it = await pick(CFG.muc, 230);
        if (it) await clipIcon(page, it.locator('xpath=..'), 'menu_muc', 2);
        else console.log('không thấy mục', CFG.muc);
        await page.screenshot({ path: path.join(SHOTS, '00_menu.png') });
    },
    async open(page) {
        await go(page);
        await shot(page, '01_open');
        await icon(page.locator(`input[placeholder="${CFG.search}"]`).locator('xpath=..'), 'o_timnhanh');
        await icon(page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(page.locator('button', { hasText: 'Làm mới' }), 'btn_lammoi');
        await icon(page.locator('button', { hasText: 'Cài đặt bộ lọc' }), 'btn_caidatboloc');
        await icon(page.locator('button', { hasText: 'Ẩn tìm kiếm nâng cao' }), 'btn_antimkiemnangcao');
        await icon(page.locator('button', { hasText: 'Xuất Excel' }), 'btn_xuatexcel');
        for (const [lb, nm] of CFG.filters) {
            if (await ff(page, lb).count()) await icon(ff(page, lb), nm);
            else console.log('thiếu ô lọc', lb);
        }
        // Tìm kiếm khi chưa chọn Thời gian -> chữ đỏ dưới ô
        await page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }).first().click();
        await page.waitForTimeout(1200);
        await shot(page, '02_required');
        LOG.required_text = await ff(page, 'Thời gian').first().innerText().catch(() => '');
        await page.locator('button', { hasText: 'Ẩn tìm kiếm nâng cao' }).first().click();
        await page.waitForTimeout(800);
        await icon(page.locator('button', { hasText: 'Tìm kiếm nâng cao' }), 'btn_timkiemnangcao');
    },
    async list(page) {
        await go(page);
        // thời gian tải khi KHÔNG lọc gì ngoài Thời gian (cả công ty) — đưa vào TC hiệu năng
        LOG.load_ms_month = await setFilters(page, { start_date: CFG.start, end_date: CFG.end });
        LOG.footer_month = await page.locator('.tp-small-text', { hasText: 'Hiển thị' }).first().innerText();
        await shot(page, '03_list');
        await icon(page.locator('ul.pagination').first(), 'phantrang');
        LOG.summary_month = await page.locator('tr.summary-row').first().innerText();
        // năm 2026
        await go(page);
        LOG.load_ms_year = await setFilters(page, { start_date: '2026-01-01', end_date: CFG.end });
        LOG.footer_year = await page.locator('.tp-small-text', { hasText: 'Hiển thị' }).first().innerText();
    },
    async customer(page) {
        await withCustomer(page);
        await scrollTable(page, 'left');
        await shot(page, '04_customer');
        await shotEl(page, tableBox(page), '05a_table_left');
        await scrollTable(page, 'right');
        await shotEl(page, tableBox(page), '05b_table_right');
        // số đọc được trên màn để làm ví dụ cộng số trong HDSD
        LOG.rows = await page.evaluate(() =>
            [...document.querySelectorAll('section.tp-card table.report-table tbody tr')].map((tr) =>
                [...tr.querySelectorAll('td')].map((td) => td.innerText.trim())
            )
        );
        await scrollTable(page, 'left');
        // ⓘ đầu cột Số dư cuối kỳ + ⓘ dòng Tổng cộng
        await scrollTable(page, 'right');
        const th = page.locator('th', { hasText: 'Số dư cuối kỳ' }).first();
        await th.locator('.report-info-tip').hover();
        await page.waitForTimeout(1200);
        await page.screenshot({ path: path.join(SHOTS, '06_tip.png') });
        await scrollTable(page, 'left');
        await page.locator('#cdd-total-info').hover();
        await page.waitForTimeout(1200);
        await page.screenshot({ path: path.join(SHOTS, '06b_tip_total.png') });
        await icon(page.locator('#cdd-total-info'), 'ic_info');
    },
    async popup(page) {
        await withCustomer(page);
        const contracts = page.locator('tr.row-contract');
        const n = await contracts.count();
        LOG.popups = [];
        const tryCol = async (col, name) => {
            for (let i = 0; i < n; i++) {
                const cell = contracts.nth(i).locator('td').nth(col - 1);
                const a = cell.locator('a.v2-cell-link');
                if (!(await a.count())) continue;
                const val = (await a.innerText()).trim();
                if (val === '0') continue;
                await a.scrollIntoViewIfNeeded();
                await a.click();
                const md = page.locator('.modal.show:visible .modal-content').last();
                await md.waitFor();
                await page.waitForLoadState('networkidle').catch(() => {});
                await page.waitForTimeout(2000);
                LOG.popups.push({ col: name, contract: (await contracts.nth(i).locator('td').nth(1).innerText()).trim(), cell: val, text: await md.innerText() });
                await shotEl(page, md, name);
                await page.locator('.modal.show:visible button', { hasText: 'Đóng' }).last().click();
                await page.waitForTimeout(1000);
                return true;
            }
            console.log('không có ô bấm được ở cột', col);
            return false;
        };
        await tryCol(COL.total_payable, '07_popup_hanghoa');
        await tryCol(COL.adjust_debt, '08_popup_dccn_tang');
        await tryCol(COL.total_returned, '08b_popup_nhaptralai');
        await tryCol(COL.adjust_has, '08c_popup_dccn_giam');
        // dòng khách hàng
        const cust = page.locator('tr.row-customer').first();
        const a = cust.locator('td').nth(COL.total_payable - 4).locator('a.v2-cell-link');
        if (await a.count()) {
            const val = (await a.innerText()).trim();
            await a.click();
            const md = page.locator('.modal.show:visible .modal-content').last();
            await md.waitFor();
            await page.waitForLoadState('networkidle').catch(() => {});
            await page.waitForTimeout(2000);
            LOG.popups.push({ col: 'customer_total_payable', cell: val, text: await md.innerText() });
            await shotEl(page, md, '09_popup_khachhang');
            await icon(page.locator('.modal.show:visible button', { hasText: 'Đóng' }).last(), 'btn_dong');
            await page.locator('.modal.show:visible button', { hasText: 'Đóng' }).last().click();
        }
    },
    async balance(page) {
        await withCustomer(page);
        await ff(page, 'Số dư cuối kỳ').first().click();
        await page.waitForTimeout(1000);
        await shot(page, '10_balance_open');
        await page.keyboard.press('Escape');
    },
    async export(page) {
        await withCustomer(page);
        await page.locator('button', { hasText: 'Xuất Excel' }).first().click();
        const md = page.locator('.modal.show:visible .modal-content').last();
        await md.waitFor();
        await page.waitForTimeout(1200);
        await shotEl(page, md, '11_export');
        LOG.export_text = await md.innerText();
        await icon(md.locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await icon(md.locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        await icon(md.locator('button', { hasText: 'Xuất file' }), 'btn_xuatfile');
        const [dl] = await Promise.all([
            page.waitForEvent('download', { timeout: 120000 }),
            md.locator('button', { hasText: 'Xuất file' }).click(),
        ]);
        const out = path.join(SHOTS, '_export_' + dl.suggestedFilename());
        await dl.saveAs(out);
        LOG.export_file = out;
    },
    async settings(page) {
        await go(page);
        await page.locator('button', { hasText: 'Cài đặt bộ lọc' }).first().click();
        const md = page.locator('.modal.show:visible .modal-content').last();
        await md.waitFor().catch(() => {});
        await page.waitForTimeout(1200);
        if (await md.count()) {
            await shotEl(page, md, '12_filter_settings');
            LOG.settings_text = await md.innerText();
        }
    },
    async nodate_export(page) {
        await go(page);
        await page.locator('button', { hasText: 'Xuất Excel' }).first().click();
        await page.waitForTimeout(400);
        LOG.export_nodate_toast = await page.locator('.toasted, .toasted-container').allInnerTexts().catch(() => []);
        await shot(page, '13_export_nodate');
    },
};

(async () => {
    const { browser, page } = await open(__dirname);
    const names = ONLY.length ? ONLY : Object.keys(steps);
    for (const nm of names) {
        console.log('==>', nm);
        try {
            await steps[nm](page);
        } catch (e) {
            console.log('LỖI bước', nm, e.message.split('\n')[0]);
        }
        fs.writeFileSync(logFile, JSON.stringify(LOG, null, 1));
    }
    await browser.close();
})().catch((e) => {
    console.error(e);
    process.exit(1);
});

// Chụp ảnh SRS + HDSD "Bảng đối chiếu công nợ 1 khách hàng" trên DEV (dev-hrm), trình duyệt headless riêng.
// Màn CHỈ ĐỌC: chỉ bấm Tìm kiếm, mở popup, Xuất Excel (file để trong thư mục này), mở xem trước bản In (KHÔNG in).
// Không bấm Lưu / Xoá / Duyệt bất kỳ phiếu nào.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/danh-muc-kho/docs/_capture_login.js');

const CFG = {
    route: '/sale/customer-debt-compare',
    rail: 'Báo cáo',
    group: 'Báo cáo công nợ',
    item: 'Đối chiếu công nợ 1 KH',
    // Bộ lọc cho ra số liệu thật (dò dữ liệu dev 02/11/2026): 10 hợp đồng, 21 chứng từ, có phiếu xuất (popup hàng hóa)
    from: '01/01/2026',
    to: '30/06/2026',
    customer: 'BÁCH LIÊN',
    customerFull: 'CÔNG TY CỔ PHẦN BÁCH LIÊN',
    productCode: 'PXH-19789',
    // KH có phiếu xuất bán hàng mượn — popup biến thể + đo thời gian tải kỳ 10 tháng
    borrowCustomer: 'TOYOTA HÀ ĐÔNG',
    borrowCustomerFull: 'CÔNG TY TNHH TOYOTA HÀ ĐÔNG',
    borrowCode: 'PXBHM-04941',
};
const SHOTS = path.join(__dirname, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
fs.mkdirSync(ICONS, { recursive: true });
const ONLY = process.argv.slice(2);
const LOG = path.join(SHOTS, '_log.txt');
const log = (...a) => {
    const s = a.join(' ');
    console.log(s);
    fs.appendFileSync(LOG, s + '\n');
};

const away = async (page) => {
    await page.mouse.move(1900, 1060);
    await page.waitForTimeout(600);
};
const shot = async (page, name) => {
    await away(page);
    await page.screenshot({ path: path.join(SHOTS, name + '.png') });
};
const shotEl = async (page, loc, name) => {
    await away(page);
    await loc.screenshot({ path: path.join(SHOTS, name + '.png') });
};
const shotM = async (page, name) => shotEl(page, page.locator('.modal.show:visible .modal-content').last(), name);
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
const ff = (page, label) =>
    page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + label + '\\s*$') }) });
const api = (page, u) =>
    page.evaluate(async (u) => {
        try {
            return await window.$nuxt.$store.dispatch('apiGetMethod', u);
        } catch (e) {
            return { err: String(e) };
        }
    }, u);

async function go(page) {
    await page.goto(DEV + CFG.route);
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(2500);
}
async function waitRows(page) {
    const t = Date.now();
    await page.waitForTimeout(300);
    await page.locator('tbody tr.row-group').first().waitFor({ timeout: 90000 });
    await page.waitForLoadState('networkidle').catch(() => {});
    const ms = Date.now() - t;
    await page.waitForTimeout(800);
    return ms;
}
async function setDates(page, from, to) {
    const a = page.locator('input[placeholder="Từ ngày"]').first();
    await a.click();
    await a.fill(from);
    await a.press('Enter');
    await page.waitForTimeout(500);
    const b = page.locator('input[placeholder="Đến ngày"]').first();
    await b.click();
    await b.fill(to);
    await b.press('Enter');
    await page.waitForTimeout(500);
    await page.mouse.click(1880, 700);
    await page.waitForTimeout(500);
}
async function pickCustomer(page, kw, full) {
    await ff(page, 'Khách hàng').locator('.select2-selection').click();
    await page.waitForTimeout(400);
    await page.keyboard.type(kw, { delay: 40 });
    const opt = page.locator('.select2-results__option', { hasText: full || kw }).first();
    await opt.waitFor({ timeout: 30000 });
    await page.waitForTimeout(500);
    await opt.click();
    await page.waitForTimeout(300);
}
async function loadMain(page) {
    await go(page);
    await setDates(page, CFG.from, CFG.to);
    await pickCustomer(page, CFG.customer, CFG.customerFull);
    return waitRows(page);
}

const steps = {
    async menu(page) {
        await page.setViewportSize({ width: 1440, height: 900 });
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
                const g = grp.nth(i).locator('xpath=..');
                await g.click();
                await page.waitForTimeout(1200);
                await clipIcon(page, g, 'menu_nhomcon', 2);
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
        await page.setViewportSize({ width: 1920, height: 1080 });
    },
    async empty(page) {
        await go(page);
        await shot(page, '01_empty');
        await icon(page.locator('input[placeholder="Tìm theo số hợp đồng hoặc số chứng từ"]').locator('xpath=..'), 'o_timnhanh');
        await icon(page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(page.locator('button', { hasText: 'Làm mới' }), 'btn_lammoi');
        await icon(page.locator('button', { hasText: 'Cài đặt bộ lọc' }), 'btn_caidatboloc');
        await icon(page.locator('button', { hasText: /tìm kiếm nâng cao/i }), 'btn_timkiemnangcao');
        await icon(page.locator('button', { hasText: /^\s*In\s*$/ }), 'btn_in');
        await icon(page.locator('button', { hasText: 'Xuất Excel' }), 'btn_xuatexcel');
        for (const [lb, nm] of [
            ['Thời gian', 'o_thoigian'],
            ['Khách hàng', 'o_khachhang'],
            ['Số hợp đồng', 'o_sohopdong'],
            ['Công ty', 'o_congty'],
            ['Phòng ban', 'o_phongban'],
            ['Bộ phận', 'o_bophan'],
            ['Nhân viên', 'o_nhanvien'],
        ]) {
            if (await ff(page, lb).count()) await icon(ff(page, lb), nm);
            else log('Không thấy ô', lb);
        }
        // Bấm Tìm kiếm khi chưa chọn gì -> chữ đỏ ô bắt buộc
        await page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }).first().click();
        await page.waitForTimeout(1200);
        await shot(page, '02_required');
        const errs = await page.locator('.ff').evaluateAll((xs) => xs.map((x) => x.innerText.trim()).filter((t) => /Vui lòng/.test(t)));
        log('Lỗi bắt buộc:', JSON.stringify(errs));
        await page.locator('button', { hasText: 'Xuất Excel' }).first().click();
        await page.waitForTimeout(800);
        const toast = await page.locator('.toasted').allTextContents();
        log('Toast thiếu điều kiện:', JSON.stringify(toast));
        await shot(page, '02b_toast');
    },
    async report(page) {
        const ms = await loadMain(page);
        log('Thời gian tải báo cáo chính (BÁCH LIÊN, 6 tháng):', ms, 'ms');
        await shot(page, '03_report');
        await shotEl(page, page.locator('section.tp-card').last(), '03b_table');
        await page.locator('#cdc-total-info').hover();
        await page.waitForTimeout(900);
        const sb = await page.locator('section.tp-card').last().boundingBox();
        await page.screenshot({ path: path.join(SHOTS, '04_total_tip.png'), clip: { x: sb.x, y: sb.y, width: 1000, height: 420 } });
        log('Tip tổng:', JSON.stringify(await page.locator('.popover').allTextContents()));
        const th = page.locator('thead th', { hasText: 'Số dư cuối kỳ' }).first();
        await th.locator('i').last().hover().catch(() => th.hover());
        await page.waitForTimeout(900);
        await page.screenshot({ path: path.join(SHOTS, '05_col_tip.png') });
        log('Tip cột:', JSON.stringify(await page.locator('.popover, .tooltip').allTextContents()));
        log('Chân bảng:', JSON.stringify(await page.locator('.tp-small-text').allTextContents()));
        const rows = await page
            .locator('tbody tr')
            .evaluateAll((trs) => trs.slice(0, 40).map((tr) => [...tr.children].map((td) => td.innerText.trim()).join(' | ')));
        fs.writeFileSync(path.join(SHOTS, '_report_rows.txt'), rows.join('\n'));
        await icon(page.locator('a.v2-cell-link', { hasText: CFG.productCode }), 'lnk_phieuxuat');
    },
    // Ảnh phóng to cho PHẦN "ĐỌC BÁO CÁO" của HDSD: cột STT + 8 cột số, từ tiêu đề tới hết hợp đồng 2
    // (cả bảng 12 cột chèn 6" thì chữ số quá nhỏ). Ghép 2 mảnh bằng make_zoom.py.
    async zoom(page) {
        await loadMain(page);
        await away(page);
        const head = await page.locator('table.report-table thead').boundingBox();
        const stt = await page.locator('table.report-table thead th').first().boundingBox();
        const ddk = await page.locator('table.report-table thead th', { hasText: 'Số dư đầu kỳ' }).first().boundingBox();
        const dck = await page.locator('table.report-table thead th', { hasText: 'Số dư cuối kỳ' }).first().boundingBox();
        const row3 = await page.locator('tbody tr').filter({ has: page.locator('td:first-child', { hasText: /^\s*3\s*$/ }) }).first().boundingBox();
        const y = head.y;
        const h = row3.y - head.y;
        await page.screenshot({ path: path.join(SHOTS, '_zoom_a.png'), clip: { x: stt.x, y, width: stt.width, height: h } });
        await page.screenshot({ path: path.join(SHOTS, '_zoom_b.png'), clip: { x: ddk.x, y, width: dck.x + dck.width - ddk.x, height: h } });
        log('zoom clip', JSON.stringify({ y, h }));
    },
    async products(page) {
        await loadMain(page);
        await page.locator('a.v2-cell-link', { hasText: CFG.productCode }).first().click();
        await page.locator('.modal.show:visible tbody tr').first().waitFor({ timeout: 30000 });
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(1200);
        await shotM(page, '06_products');
        log('Popup hàng:', JSON.stringify(await page.locator('.modal.show:visible').innerText()).slice(0, 800));
        await icon(page.locator('.modal.show:visible button', { hasText: 'Xem chi tiết phiếu' }), 'btn_xemchitietphieu');
        await icon(page.locator('.modal.show:visible button', { hasText: 'Đóng' }), 'btn_dong');
        await page.locator('.modal.show:visible button', { hasText: 'Đóng' }).last().click();
        await page.waitForTimeout(800);
    },
    async borrow(page) {
        // Biến thể popup: phiếu xuất bán hàng mượn — KH TOYOTA HÀ ĐÔNG (dò bằng _find_borrow.js 02/11/2026)
        await go(page);
        await setDates(page, '01/01/2026', '31/10/2026');
        const t0 = Date.now();
        await pickCustomer(page, CFG.borrowCustomer, CFG.borrowCustomerFull);
        const ms = await waitRows(page);
        log('Thời gian tải KH nhiều dữ liệu (01/01-31/10/2026):', ms, 'ms; tính từ lúc chọn KH:', Date.now() - t0, 'ms');
        log('Chân bảng KH nặng:', JSON.stringify(await page.locator('.tp-small-text').allTextContents()));
        await page.locator('input[placeholder="Tìm theo số hợp đồng hoặc số chứng từ"]').fill(CFG.borrowCode);
        await page.keyboard.press('Enter');
        await page.waitForTimeout(1500);
        await waitRows(page);
        await shot(page, '07_keyword');
        await page.locator('a.v2-cell-link', { hasText: CFG.borrowCode }).first().click();
        await page.locator('.modal.show:visible tbody tr').first().waitFor({ timeout: 30000 });
        await page.waitForTimeout(1200);
        await shotM(page, '08_products_borrow');
        log('Popup mượn:', JSON.stringify(await page.locator('.modal.show:visible').innerText()).slice(0, 600));
        await page.locator('.modal.show:visible button', { hasText: 'Đóng' }).last().click();
    },
    async exportx(page) {
        await loadMain(page);
        await page.locator('button', { hasText: 'Xuất Excel' }).first().click();
        await page.waitForTimeout(1200);
        await shotM(page, '09_export');
        await icon(page.locator('.modal.show:visible button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await icon(page.locator('.modal.show:visible button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        await icon(page.locator('.modal.show:visible button', { hasText: 'Xuất file' }), 'btn_xuatfile');
        const [dl] = await Promise.all([
            page.waitForEvent('download', { timeout: 60000 }),
            page.locator('.modal.show:visible button', { hasText: 'Xuất file' }).click(),
        ]);
        const out = path.join(SHOTS, dl.suggestedFilename());
        await dl.saveAs(out);
        log('Excel:', out);
    },
    async print(page) {
        await loadMain(page);
        await page.locator('button', { hasText: /^\s*In\s*$/ }).first().click();
        await page.waitForTimeout(1500);
        await page.locator('.modal.show:visible iframe, .modal.show:visible .report-print-notice').first().waitFor({ timeout: 60000 }).catch(() => {});
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(3000);
        await shotM(page, '10_print');
        await page.keyboard.press('Escape');
    },
    async reverse(page) {
        await go(page);
        await setDates(page, '30/06/2026', '01/01/2026');
        const v = await page.locator('input.mx-input').evaluateAll((xs) => xs.map((x) => x.value));
        log('Gõ ngày ngược chiều -> giá trị ô:', JSON.stringify(v));
        await shot(page, '11_reverse');
    },
};

(async () => {
    const { browser, page } = await open(__dirname);
    await page.setViewportSize({ width: 1920, height: 1080 });
    try {
        for (const [name, fn] of Object.entries(steps)) {
            if (ONLY.length && !ONLY.includes(name)) continue;
            log('== bước', name);
            try {
                await fn(page);
            } catch (e) {
                log('LỖI bước', name, e.message.split('\n')[0]);
                await page.screenshot({ path: path.join(SHOTS, '_err_' + name + '.png') });
            }
        }
    } finally {
        await browser.close();
    }
})().catch((e) => {
    console.error(e);
    process.exit(1);
});

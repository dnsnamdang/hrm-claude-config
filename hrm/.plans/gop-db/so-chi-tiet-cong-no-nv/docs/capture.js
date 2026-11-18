// Chụp ảnh SRS + HDSD "Sổ chi tiết công nợ nhân viên" trên DEV (dev-hrm), trình duyệt headless riêng.
// Màn CHỈ ĐỌC: chỉ chọn bộ lọc, Tìm kiếm, Xuất Excel (file để trong hdsd_shots), mở xem trước bản In (KHÔNG in).
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/danh-muc-kho/docs/_capture_login.js');

const CFG = {
    route: '/finance/employee-debt-details',
    rail: 'Kế toán công nợ',
    group: 'Nhân viên',
    item: 'Sổ chi tiết công nợ nhân viên',
    from: '01/01/2026',
    to: '31/10/2026',
    account: '141 - Tạm ứng',
    accountKw: '141',
    employee: 'Võ Cát Hào',
    fAccount: '131 - Phải thu của khách hàng',
    fAccountKw: '131',
    fCurrency: 'USD',
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
    page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + label + '\\s*\\*?\\s*$') }) }).first();
const QS = 'input[placeholder="Tìm theo số chứng từ hoặc số hợp đồng"]';
const BTN_TOGGLE = /tìm kiếm nâng cao/i;

async function go(page, route = CFG.route) {
    // Bộ lọc được nhớ 10 phút trên trình duyệt — xoá trước mỗi bước để các bước không dính bộ lọc của nhau
    await page.evaluate(() => {
        try {
            Object.keys(localStorage).filter((k) => /employee_debt/i.test(k)).forEach((k) => localStorage.removeItem(k));
        } catch (e) {}
    }).catch(() => {});
    await page.goto(DEV + route);
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(2500);
}
async function waitRows(page) {
    const t = Date.now();
    await page.waitForTimeout(300);
    await page.locator('tbody tr.summary-row').first().waitFor({ timeout: 120000 });
    await page.waitForLoadState('networkidle').catch(() => {});
    const ms = Date.now() - t;
    await page.waitForTimeout(1000);
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
    await page.mouse.click(1880, 1000);
    await page.waitForTimeout(500);
}
async function pick(page, label, kw, full) {
    await ff(page, label).locator('.select2-selection').first().click();
    await page.waitForTimeout(500);
    const search = page.locator('.select2-container--open .select2-search__field');
    if (await search.count()) await search.last().fill(kw);
    else await page.keyboard.type(kw, { delay: 40 });
    const opt = page.locator('.select2-container--open .select2-results__option', { hasText: full || kw }).first();
    await opt.waitFor({ timeout: 30000 });
    await page.waitForTimeout(500);
    await opt.click();
    await page.waitForTimeout(600);
}
async function loadMain(page) {
    await go(page);
    await pick(page, 'Tài khoản', CFG.accountKw, CFG.account);
    await setDates(page, CFG.from, CFG.to);
    return waitRows(page);
}
async function dumpRows(page, file) {
    const rows = await page
        .locator('table.report-table tbody tr')
        .evaluateAll((trs) => trs.slice(0, 40).map((tr) => [...tr.children].map((td) => td.innerText.trim()).join(' | ')));
    fs.writeFileSync(path.join(SHOTS, file), rows.join('\n'));
    log('Chân bảng:', JSON.stringify(await page.locator('.tp-small-text').allTextContents()));
}
async function collapse(page) {
    await page.locator('button', { hasText: BTN_TOGGLE }).first().click();
    await page.waitForTimeout(1000);
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
        await icon(page.locator(QS).locator('xpath=..'), 'o_timnhanh');
        await icon(page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(page.locator('button', { hasText: 'Làm mới' }), 'btn_lammoi');
        await icon(page.locator('button', { hasText: 'Cài đặt bộ lọc' }), 'btn_caidatboloc');
        await icon(page.locator('button', { hasText: BTN_TOGGLE }), 'btn_timkiemnangcao');
        await icon(page.locator('button', { hasText: /^\s*In\s*$/ }), 'btn_in');
        await icon(page.locator('button', { hasText: 'Xuất Excel' }), 'btn_xuatexcel');
        for (const [lb, nm] of [
            ['Công ty', 'o_congty'], ['Phòng ban', 'o_phongban'], ['Bộ phận', 'o_bophan'], ['Nhân viên', 'o_nhanvien'],
            ['Tài khoản', 'o_taikhoan'], ['Thời gian', 'o_thoigian'], ['Tài khoản đối ứng', 'o_tkdoiung'],
            ['Đơn hàng/Hợp đồng', 'o_hopdong'], ['Loại chứng từ', 'o_loaichungtu'], ['Số chứng từ', 'o_sochungtu'],
            ['Ghi chú', 'o_ghichu'], ['Loại tiền', 'o_loaitien'], ['Mẫu', 'o_mau'], ['Khách hàng', 'o_khachhang'],
            ['Chỉ tiêu', 'o_chitieu'], ['Mã vụ việc', 'o_mavuviec'], ['Số tiền', 'o_sotien'],
        ]) {
            if (await ff(page, lb).count()) await icon(ff(page, lb), nm);
            else log('Không thấy ô', lb);
        }
        await page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }).first().click();
        await page.waitForTimeout(1200);
        await shot(page, '02_required');
        const errs = await page.locator('.ff').evaluateAll((xs) => xs.map((x) => x.innerText.trim()).filter((t) => /Vui lòng/.test(t)));
        log('Lỗi bắt buộc:', JSON.stringify(errs));
        await page.locator('button', { hasText: 'Xuất Excel' }).first().click();
        await page.waitForTimeout(800);
        log('Toast thiếu điều kiện (Xuất Excel):', JSON.stringify(await page.locator('.toasted').allTextContents()));
        await page.waitForTimeout(3500);
        await page.locator('button', { hasText: /^\s*In\s*$/ }).first().click();
        await page.waitForTimeout(800);
        log('Toast thiếu điều kiện (In):', JSON.stringify(await page.locator('.toasted').allTextContents()));
    },
    async report(page) {
        const ms = await loadMain(page);
        log('Thời gian tải TK 141 01/01-31/10/2026 (không lọc thêm):', ms, 'ms');
        await shot(page, '03_report');
        await dumpRows(page, '_rows_141.txt');
        const lnk = page.locator('table.report-table tbody a.v2-cell-link').first();
        if (await lnk.count()) {
            log('Link chứng từ đầu:', await lnk.innerText());
            await icon(lnk, 'lnk_chungtu');
        }
        await collapse(page);
        await shotEl(page, page.locator('section.tp-card').last(), '03b_table');
    },
    async employee(page) {
        await loadMain(page);
        await pick(page, 'Nhân viên', CFG.employee, CFG.employee);
        await page.waitForTimeout(1000);
        await waitRows(page);
        await shot(page, '04_employee');
        await dumpRows(page, '_rows_141_nv.txt');
        await collapse(page);
        await shotEl(page, page.locator('section.tp-card').last(), '04b_employee_table');
    },
    async foreign(page) {
        await go(page);
        await pick(page, 'Tài khoản', CFG.fAccountKw, CFG.fAccount);
        await setDates(page, CFG.from, CFG.to);
        await pick(page, 'Loại tiền', CFG.fCurrency, CFG.fCurrency);
        await pick(page, 'Mẫu', 'Ngoại tệ', 'Ngoại tệ');
        await waitRows(page);
        await shot(page, '05_foreign');
        await dumpRows(page, '_rows_131_usd.txt');
        await collapse(page);
        await shotEl(page, page.locator('section.tp-card').last(), '05b_foreign_table');
    },
    async keyword(page) {
        await loadMain(page);
        await page.locator(QS).fill('HTCXK');
        await page.keyboard.press('Enter');
        await page.waitForTimeout(1500);
        await waitRows(page);
        await shot(page, '06_keyword');
        await dumpRows(page, '_rows_keyword.txt');
    },
    async exportx(page) {
        await loadMain(page);
        await pick(page, 'Nhân viên', CFG.employee, CFG.employee);
        await waitRows(page);
        const t = Date.now();
        const [dl] = await Promise.all([
            page.waitForEvent('download', { timeout: 300000 }),
            page.locator('button', { hasText: 'Xuất Excel' }).first().click(),
        ]);
        await page.waitForTimeout(300);
        await shot(page, '07_export');
        const out = path.join(SHOTS, dl.suggestedFilename());
        await dl.saveAs(out);
        log('Excel:', out, 'ms', Date.now() - t);
        log('Toast xuất:', JSON.stringify(await page.locator('.toasted').allTextContents()));
    },
    async print(page) {
        await loadMain(page);
        await pick(page, 'Nhân viên', CFG.employee, CFG.employee);
        await waitRows(page);
        await page.locator('button', { hasText: /^\s*In\s*$/ }).first().click();
        await page.waitForTimeout(1500);
        await page.locator('.modal.show:visible iframe, .modal.show:visible .report-print-notice').first().waitFor({ timeout: 60000 }).catch(() => {});
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(3000);
        await shotM(page, '08_print');
        log('Tiêu đề popup in:', JSON.stringify(await page.locator('.modal.show:visible .modal-title, .modal.show:visible h5').allTextContents()));
        await page.keyboard.press('Escape');
    },
    async printbig(page) {
        await loadMain(page);
        await page.locator('button', { hasText: /^\s*In\s*$/ }).first().click();
        await page.waitForTimeout(3000);
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(2000);
        await shotM(page, '09_print_limit');
        log('Popup in vượt trần:', JSON.stringify(await page.locator('.modal.show:visible').innerText()).slice(0, 600));
        await page.keyboard.press('Escape');
    },
    async settings(page) {
        await go(page);
        await page.locator('button', { hasText: 'Cài đặt bộ lọc' }).first().click();
        await page.waitForTimeout(1200);
        if (await page.locator('.modal.show:visible .modal-content').count()) await shotM(page, '10_filter_settings');
        else await shot(page, '10_filter_settings');
        await page.keyboard.press('Escape');
    },
    async reverse(page) {
        await go(page);
        await setDates(page, '31/10/2026', '01/01/2026');
        const v = await page.locator('input[placeholder="Từ ngày"], input[placeholder="Đến ngày"]').evaluateAll((xs) => xs.map((x) => x.value));
        log('Gõ ngày ngược chiều -> giá trị ô:', JSON.stringify(v));
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

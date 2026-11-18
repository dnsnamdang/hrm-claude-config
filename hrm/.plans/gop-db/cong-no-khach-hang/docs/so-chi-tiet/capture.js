// Chụp ảnh SRS + HDSD "Sổ chi tiết công nợ phải thu khách hàng" trên DEV (dev-hrm), trình duyệt headless riêng.
// Màn CHỈ ĐỌC: chỉ bấm Tìm kiếm, Xuất Excel (file để trong thư mục này), mở xem trước bản In (KHÔNG in), mở rồi ĐÓNG
// cửa sổ Cài đặt bộ lọc (KHÔNG bấm Lưu). Không bấm Lưu / Xoá / Duyệt bất kỳ phiếu nào.
// Tài khoản dev đã lưu "Cài đặt bộ lọc" ẩn ô Công ty… và Loại tiền => chặn đọc cấu hình đó TRÊN TRÌNH DUYỆT (route) để
// màn hiện đủ ô như người dùng chưa cài đặt (mặc định) — không ghi gì lên máy chủ.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/danh-muc-kho/docs/_capture_login.js');

const CFG = {
    route: '/finance/customer-ledger-details',
    rail: 'Kế toán công nợ',
    group: 'Khách hàng',
    item: 'Sổ chi tiết công nợ phải thu khách hàng',
    // Dò dữ liệu dev 18/11/2026 (_probe2.js): TK 131, KH id 69 (14TQUPCA-2) có 73 bút toán 01/01–31/10/2026
    q: 'account_id=21&customer_id=69&date_from=01/01/2026&date_to=31/10/2026&type_report=1',
    // KH có bút toán ngoại tệ (USD) trên TK 131
    qFx: 'account_id=21&customer_id=10929&date_from=01/01/2026&date_to=31/10/2026&type_report=2',
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
const esc = (s) => s.replace(/[/]/g, '\\/');
const ff = (page, label) =>
    page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + esc(label) + '\\s*\\*?\\s*$') }) });

async function go(page, query) {
    await page.goto(DEV + CFG.route + (query ? '?' + query : ''));
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(2500);
}
async function waitRows(page) {
    const t = Date.now();
    await page.locator('tbody tr.summary-row').first().waitFor({ timeout: 90000 });
    await page.waitForLoadState('networkidle').catch(() => {});
    const ms = Date.now() - t;
    await page.waitForTimeout(800);
    return ms;
}
async function loadMain(page, q) {
    await go(page, q || CFG.q);
    return waitRows(page);
}
const rowsText = (page) =>
    page.locator('tbody tr').evaluateAll((trs) => trs.slice(0, 20).map((tr) => [...tr.children].map((td) => td.innerText.trim()).join(' | ')));

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
        await page.setViewportSize({ width: 1920, height: 1080 });
    },
    async empty(page) {
        await go(page);
        await shot(page, '01_empty');
        log('Ô lọc:', JSON.stringify(await page.locator('.ff__text').allInnerTexts()));
        await icon(page.locator('input[placeholder="Tìm theo số chứng từ hoặc số hợp đồng"]').locator('xpath=..'), 'o_timnhanh');
        await icon(page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(page.locator('button', { hasText: 'Làm mới' }), 'btn_lammoi');
        await icon(page.locator('button', { hasText: 'Cài đặt bộ lọc' }), 'btn_caidatboloc');
        await icon(page.locator('button', { hasText: /tìm kiếm nâng cao/i }), 'btn_timkiemnangcao');
        await icon(page.locator('button', { hasText: /^\s*In\s*$/ }), 'btn_in');
        await icon(page.locator('button', { hasText: 'Xuất Excel' }), 'btn_xuatexcel');
        const fields = [
            ['Công ty', 'o_congty'], ['Phòng ban', 'o_phongban'], ['Bộ phận', 'o_bophan'], ['Nhân viên', 'o_nhanvien'],
            ['Tài khoản', 'o_taikhoan'], ['Khách hàng', 'o_khachhang'], ['Thời gian', 'o_thoigian'], ['Tài khoản đối ứng', 'o_tkdoiung'],
            ['Đơn hàng/Hợp đồng', 'o_hopdong'], ['Số chứng từ', 'o_sochungtu'], ['Loại tiền', 'o_loaitien'], ['Số tiền', 'o_sotien'],
        ];
        for (const [lb, nm] of fields) {
            if (await ff(page, lb).count()) await icon(ff(page, lb), nm);
            else log('Không thấy ô', lb);
        }
        const ti = page.locator('.ri-information-line').first();
        await ti.hover().catch(() => {});
        await page.waitForTimeout(900);
        log('Tip tiêu đề:', JSON.stringify(await page.locator('.popover, .tooltip').allInnerTexts()));
        await page.screenshot({ path: path.join(SHOTS, '01b_title_tip.png'), clip: { x: 0, y: 0, width: 1200, height: 300 } });
        await away(page);
        await page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }).first().click();
        await page.waitForTimeout(1200);
        await shot(page, '02_required');
        const errs = await page.locator('.ff').evaluateAll((xs) => xs.map((x) => x.innerText.trim()).filter((t) => /Vui lòng/.test(t)));
        log('Lỗi bắt buộc:', JSON.stringify(errs));
        await page.locator('button', { hasText: 'Xuất Excel' }).first().click();
        await page.waitForTimeout(800);
        log('Toast thiếu điều kiện:', JSON.stringify(await page.locator('.toasted').allInnerTexts()));
        await shot(page, '02b_toast');
        await page.locator('button', { hasText: 'Cài đặt bộ lọc' }).first().click();
        await page.waitForTimeout(1200);
        await shotM(page, '13_filter_setting');
        await page.locator('.modal.show:visible button', { hasText: 'Đóng' }).last().click();
    },
    async report(page) {
        const ms = await loadMain(page);
        log('Thời gian tải (KH 14TQUPCA-2, 01/01-31/10/2026, mở bằng link):', ms, 'ms');
        await shot(page, '03_report');
        await shotEl(page, page.locator('section.tp-card').last(), '03b_table');
        log('Chân bảng:', JSON.stringify(await page.locator('.tp-small-text').allInnerTexts()));
        log('Giá trị ô:', JSON.stringify(await page.locator('.ff').evaluateAll((xs) => xs.map((x) => x.innerText.replace(/\s+/g, ' ').trim()))));
        fs.writeFileSync(path.join(SHOTS, '_report_rows.txt'), (await rowsText(page)).join('\n'));
        await page.locator('.page-link[aria-label="Go to last page"]').first().click().catch((e) => log('không bấm trang cuối', e.message));
        await page.waitForTimeout(3000);
        log('Chân bảng trang cuối:', JSON.stringify(await page.locator('.tp-small-text').allInnerTexts()));
        fs.writeFileSync(path.join(SHOTS, '_report_last.txt'), (await rowsText(page)).join('\n'));
        await shot(page, '04_last_page');
    },
    async zoom(page) {
        await loadMain(page);
        await away(page);
        const tb = await page.locator('table.report-table').boundingBox();
        const r = await page.locator('tbody tr').nth(6).boundingBox();
        await page.screenshot({ path: path.join(SHOTS, '12_read_zoom.png'), clip: { x: tb.x, y: tb.y, width: tb.width, height: r.y - tb.y } });
    },
    async keyword(page) {
        await loadMain(page);
        await page.locator('input[placeholder="Tìm theo số chứng từ hoặc số hợp đồng"]').fill('PXH');
        await page.keyboard.press('Enter');
        await page.waitForTimeout(1500);
        await waitRows(page);
        log('Chân bảng tìm PXH', JSON.stringify(await page.locator('.tp-small-text').allInnerTexts()));
        fs.writeFileSync(path.join(SHOTS, '_kw_rows.txt'), (await rowsText(page)).join('\n'));
        await shot(page, '05_keyword');
    },
    async foreign(page) {
        const ms = await loadMain(page, CFG.qFx);
        log('Thời gian tải Ngoại tệ:', ms);
        fs.writeFileSync(path.join(SHOTS, '_fx_rows.txt'), (await rowsText(page)).join('\n'));
        await shot(page, '06_foreign');
    },
    async exportx(page) {
        await loadMain(page);
        const [dl] = await Promise.all([
            page.waitForEvent('download', { timeout: 120000 }),
            page.locator('button', { hasText: 'Xuất Excel' }).first().click(),
        ]);
        const out = path.join(SHOTS, dl.suggestedFilename());
        await dl.saveAs(out);
        await page.waitForTimeout(500);
        log('Excel:', out, 'toast', JSON.stringify(await page.locator('.toasted').allInnerTexts()));
        await page.screenshot({ path: path.join(SHOTS, '07_export.png') });
    },
    async print(page) {
        await loadMain(page);
        await page.locator('button', { hasText: /^\s*In\s*$/ }).first().click();
        await page.waitForTimeout(1500);
        await page.locator('.modal.show:visible iframe, .modal.show:visible .report-print-notice').first().waitFor({ timeout: 60000 }).catch(() => {});
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(3500);
        await shotM(page, '08_print');
        log('Tiêu đề cửa sổ in:', JSON.stringify(await page.locator('.modal.show:visible .modal-title, .modal.show:visible h5').allInnerTexts()));
        await page.keyboard.press('Escape');
    },
    async reverse(page) {
        await go(page);
        const a = page.locator('input[placeholder="Từ ngày"]').first();
        await a.click();
        await a.fill('31/10/2026');
        await a.press('Enter');
        await page.waitForTimeout(500);
        const b = page.locator('input[placeholder="Đến ngày"]').first();
        await b.click();
        await b.fill('01/01/2026');
        await b.press('Enter');
        await page.waitForTimeout(500);
        await page.mouse.click(1880, 900);
        log('Gõ ngày ngược chiều -> giá trị ô:', JSON.stringify(await page.locator('input.mx-input').evaluateAll((xs) => xs.map((x) => x.value))));
        await shot(page, '11_reverse');
    },
};

(async () => {
    const { browser, page } = await open(__dirname);
    await page.context().route('**/human/filter-customizations/detail*', (route) =>
        route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ message: 'ok', data: null }) }));
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

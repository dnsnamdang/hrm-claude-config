// Chụp ảnh SRS + HDSD "BC tổng hợp công nợ KH theo nhân viên" trên DEV (dev-hrm) — khuôn danh-muc-kho/docs/warehouses/capture.js.
// Màn CHỈ ĐỌC: được bấm Tìm kiếm, Xuất Excel (file tải về để trong thư mục này), mở popup rồi Đóng.
// KHÔNG bấm Lưu ở popup Cài đặt bộ lọc. Không bấm Lưu / Xóa / Duyệt phiếu nào.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('../../../danh-muc-kho/docs/_capture_login.js');

const CFG = {
    route: '/sale/customer-debt-by-employee',
    rail: 'Báo cáo',
    nhom: 'Báo cáo công nợ',
    muc: 'Tổng hợp công nợ theo NV',
    from: '01/10/2026',
    to: '31/10/2026',
    nv: 'Vương Văn Duy', // NV có nhiều HĐ, có phát sinh tăng + đã thanh toán + ngày nghiệm thu trong kỳ
    filters: [
        ['Thời gian', 'o_thoigian'], ['Khách hàng', 'o_khachhang'], ['Số hợp đồng', 'o_sohopdong'],
        ['Số dư cuối kỳ', 'o_soducuoiky'], ['Ngày nghiệm thu', 'o_ngaynghiemthu'], ['Công ty', 'o_congty'],
        ['Phòng ban', 'o_phongban'], ['Bộ phận', 'o_bophan'], ['Nhân viên', 'o_nhanvien'],
    ],
};
const SHOTS = path.join(__dirname, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
const XLS = path.join(__dirname, 'excel_tai_ve');
fs.mkdirSync(ICONS, { recursive: true });
fs.mkdirSync(XLS, { recursive: true });
const ONLY = process.argv.slice(2);
const LOG = path.join(SHOTS, '_log.txt');
const log = (...a) => { const s = a.join(' '); console.log(s); fs.appendFileSync(LOG, s + '\n'); };

const away = async (page) => { await page.mouse.move(1435, 895); await page.waitForTimeout(600); };
const shot = async (page, name) => { await away(page); await page.screenshot({ path: path.join(SHOTS, name + '.png') }); };
const shotEl = async (page, loc, name) => { await away(page); await loc.screenshot({ path: path.join(SHOTS, name + '.png') }); };
const icon = async (loc, name) => {
    await loc.first().scrollIntoViewIfNeeded().catch(() => {});
    await loc.first().screenshot({ path: path.join(ICONS, name + '.png') });
};
const clipIcon = async (page, loc, name, pad = 0, maxW = null) => {
    const b = await loc.first().boundingBox();
    let w = b.width + 2 * pad;
    if (maxW && w > maxW) w = maxW;
    await page.screenshot({ path: path.join(ICONS, name + '.png'), clip: { x: b.x - pad, y: b.y - pad, width: w, height: b.height + 2 * pad } });
};
const modal = (page) => page.locator('.modal.show:visible').last();
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\-]/g, '\\$&');
const ff = (page, label) =>
    page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + esc(label) + '\\s*$') }) }).first();
const card = (page) => page.locator('section.tp-card').filter({ has: page.locator('table.report-table') }).first();

async function go(page) {
    // bộ lọc được ghi nhớ 10 phút -> xoá trước mỗi bước để bước sau không mang bộ lọc của bước trước
    await page.evaluate(() => { try { Object.keys(localStorage).filter((k) => /customer_debt_by_employee/.test(k)).forEach((k) => localStorage.removeItem(k)); } catch (e) {} }).catch(() => {});
    await page.goto(DEV + CFG.route);
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(2500);
}
async function setDates(page, from = CFG.from, to = CFG.to) {
    const ins = ff(page, 'Thời gian').locator('input.mx-input');
    await ins.nth(0).click(); await page.keyboard.press('Control+A'); await page.keyboard.type(from, { delay: 30 }); await page.keyboard.press('Enter');
    await page.waitForTimeout(400);
    const t0 = Date.now();
    await ins.nth(1).click(); await page.keyboard.press('Control+A'); await page.keyboard.type(to, { delay: 30 }); await page.keyboard.press('Enter');
    await page.waitForTimeout(800);
    return t0;
}
async function waitRows(page, t0) {
    await page.locator('tr.row-group').first().waitFor({ timeout: 180000 });
    await page.waitForLoadState('networkidle').catch(() => {});
    const ms = Date.now() - t0;
    await page.waitForTimeout(1500);
    return ms;
}
async function pickEmployee(page, name) {
    await ff(page, 'Nhân viên').locator('.select2-selection').first().click();
    await page.waitForTimeout(500);
    await page.keyboard.type(name, { delay: 40 });
    await page.waitForTimeout(2500);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(800);
    await page.keyboard.press('Escape');
}

// Số dư cuối kỳ = Dư nợ: bỏ các HĐ đã hết nợ (toàn số 0) cho bảng đọc được
async function pickDuNo(page) {
    await ff(page, 'Số dư cuối kỳ').locator('.select2-selection').first().click();
    await page.waitForTimeout(600);
    await page.locator('.select2-results__option', { hasText: /^\s*Dư nợ\s*$/ }).first().click();
    await page.waitForTimeout(1500);
}

const steps = {
    async menu(page) {
        await go(page);
        await page.mouse.move(40, 300);
        await page.waitForTimeout(1200);
        await clipIcon(page, page.locator('.left-side-menu a.logo').first(), 'menu_phanhe', 2, 200);
        const cat = page.locator('.left-side-menu .cats-list a.cat').filter({ hasText: new RegExp('^\\s*' + CFG.rail + '\\s*$') }).first();
        await clipIcon(page, cat, 'menu_rail', 0, 150);
        await cat.click();
        await page.waitForTimeout(1500);
        const grp = page.getByText(CFG.nhom, { exact: true });
        let g = null;
        for (let i = 0; i < (await grp.count()); i++) {
            const b = await grp.nth(i).boundingBox();
            if (b && b.x > 200 && b.x < 440) { g = grp.nth(i); break; }
        }
        await g.click();
        await page.waitForTimeout(1200);
        await clipIcon(page, g.locator('xpath=ancestor::a[1]'), 'menu_nhom', 0);
        const item = page.getByText(CFG.muc, { exact: true });
        let el = null;
        for (let i = 0; i < (await item.count()); i++) {
            const b = await item.nth(i).boundingBox();
            if (b && b.x > 440) { el = item.nth(i); break; }
        }
        await clipIcon(page, el.locator('xpath=..'), 'menu_muc', 2, 260);
        await page.screenshot({ path: path.join(SHOTS, '00_menu.png') });
    },
    async empty(page) {
        await go(page);
        await shot(page, '00b_empty');
        await icon(page.locator('input[placeholder="Tìm theo số hợp đồng, mã hoặc tên khách hàng"]').locator('xpath=..'), 'o_timnhanh');
        await icon(page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(page.locator('button', { hasText: 'Làm mới' }), 'btn_lammoi');
        await icon(page.locator('button', { hasText: 'Cài đặt bộ lọc' }), 'btn_caidatboloc');
        await icon(page.locator('button', { hasText: 'Ẩn tìm kiếm nâng cao' }), 'btn_antimkiem');
        await icon(page.locator('button', { hasText: /^\s*Xuất Excel\s*$/ }), 'btn_xuatexcel');
        await icon(page.locator('button', { hasText: 'Xuất Excel mẫu in' }), 'btn_xuatexcelmauin');
        for (const [lb, nm] of CFG.filters) {
            if (await ff(page, lb).count()) await icon(ff(page, lb), nm); else log('thiếu ô lọc', lb);
        }
        await page.locator('button', { hasText: 'Ẩn tìm kiếm nâng cao' }).first().click();
        await page.waitForTimeout(1000);
        await icon(page.locator('button', { hasText: /Tìm kiếm nâng cao/ }), 'btn_timkiemnangcao');
        await shot(page, '00c_collapsed');
        await page.locator('button', { hasText: /Tìm kiếm nâng cao/ }).first().click();
        await page.waitForTimeout(800);
        // bấm Tìm kiếm khi chưa chọn Thời gian -> chữ đỏ dưới ô
        await page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }).first().click();
        await page.waitForTimeout(1200);
        await shotEl(page, page.locator('.tp-card').first(), '02b_required');
        log('chữ đỏ Thời gian:', (await ff(page, 'Thời gian').locator('xpath=..').innerText()).replace(/\s+/g, ' '));
    },
    async report(page) {
        await go(page);
        const t0 = await setDates(page);
        const ms = await waitRows(page, t0);
        log('Thời gian tải kỳ', CFG.from, '-', CFG.to, 'không lọc khác:', ms, 'ms');
        await shot(page, '01_report');
        log('chân bảng:', await page.locator('.tp-small-text').filter({ hasText: 'Hiển thị' }).first().innerText());
        const tip = page.locator('thead th').filter({ hasText: 'Số dư cuối kỳ' }).first().locator('.report-info-tip').first();
        await tip.scrollIntoViewIfNeeded();
        await tip.hover();
        await page.waitForTimeout(1500);
        await page.screenshot({ path: path.join(SHOTS, '06_tip.png') });
        await icon(page.locator('ul.pagination').first(), 'phantrang');
    },
    async longperiod(page) {
        await go(page);
        const t0 = await setDates(page, '01/01/2026', '31/10/2026');
        const ms = await waitRows(page, t0);
        log('Thời gian tải kỳ 01/01/2026 - 31/10/2026 không lọc khác:', ms, 'ms; chân bảng:',
            await page.locator('.tp-small-text').filter({ hasText: 'Hiển thị' }).first().innerText());
    },
    async filter(page) {
        await go(page);
        let t0 = await setDates(page);
        await waitRows(page, t0);
        await pickEmployee(page, CFG.nv);
        await page.waitForTimeout(3000);
        await page.waitForLoadState('networkidle').catch(() => {});
        await pickDuNo(page);
        await page.locator('tr.row-group').first().waitFor({ timeout: 120000 });
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(2000);
        await shot(page, '02_filter');
        const c = card(page);
        await c.scrollIntoViewIfNeeded();
        await shotEl(page, c, '05_table_a');
        await page.evaluate(() => {
            document.querySelectorAll('div').forEach((d) => {
                if (d.scrollWidth > d.clientWidth + 20 && d.querySelector('table.report-table')) d.scrollLeft = d.scrollWidth;
            });
        });
        await page.waitForTimeout(1000);
        await shotEl(page, c, '05_table_b');
        const rows = await page.locator('table.report-table tbody tr').allInnerTexts();
        fs.writeFileSync(path.join(SHOTS, '_rows_nv.txt'), rows.join('\n'));
    },
    async daterange(page) {
        // Đến ngày chặn ngày trước Từ ngày (ngày mờ, gõ tay cũng không nhận) -> chụp lịch Đến ngày khi Từ = 15/10/2026
        await go(page);
        const ins = ff(page, 'Thời gian').locator('input.mx-input');
        await ins.nth(0).click(); await page.keyboard.type('15/10/2026', { delay: 30 }); await page.keyboard.press('Enter');
        await page.waitForTimeout(600);
        await ins.nth(1).click();
        await page.waitForTimeout(800);
        await page.keyboard.type('01/10/2026', { delay: 30 });
        await page.waitForTimeout(800);
        await page.mouse.move(1435, 895);
        await shot(page, '02c_daterange');
        await page.keyboard.press('Enter');
        await page.waitForTimeout(800);
        log('gõ Đến ngày 01/10 khi Từ 15/10 ->', await ins.nth(0).inputValue(), '->', await ins.nth(1).inputValue());
    },
    async export(page) {
        await go(page);
        const t0 = await setDates(page);
        await waitRows(page, t0);
        // xuất cả tháng không lọc > 5 phút trên dev (ghi ở báo cáo cuối) -> lọc 1 nhân viên để có file mẫu
        await pickEmployee(page, CFG.nv);
        await page.waitForTimeout(3000);
        await page.waitForLoadState('networkidle').catch(() => {});
        await pickDuNo(page);
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.locator('button', { hasText: /^\s*Xuất Excel\s*$/ }).first().click();
        await page.waitForTimeout(1500);
        const m = modal(page);
        await shotEl(page, m.locator('.modal-content'), '03_export');
        log('popup xuất:', (await m.innerText()).replace(/\n+/g, ' | '));
        await icon(m.locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await icon(m.locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        await icon(m.locator('button', { hasText: 'Xuất file' }), 'btn_xuatfile');
        await icon(m.locator('button', { hasText: /^\s*Đóng\s*$/ }), 'btn_dong');
        let t1 = Date.now();
        const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 300000 }), m.locator('button', { hasText: 'Xuất file' }).click()]);
        await dl.saveAs(path.join(XLS, dl.suggestedFilename()));
        log('Xuất Excel:', dl.suggestedFilename(), Date.now() - t1, 'ms');
        await page.waitForTimeout(1200);
        await shot(page, '03b_export_done');
        t1 = Date.now();
        const [dl2] = await Promise.all([page.waitForEvent('download', { timeout: 300000 }), page.locator('button', { hasText: 'Xuất Excel mẫu in' }).first().click()]);
        await dl2.saveAs(path.join(XLS, dl2.suggestedFilename()));
        log('Xuất Excel mẫu in:', dl2.suggestedFilename(), Date.now() - t1, 'ms');
    },
    async settings(page) {
        await go(page);
        await page.locator('button', { hasText: 'Cài đặt bộ lọc' }).first().click();
        await page.waitForTimeout(1500);
        const m = modal(page);
        await shotEl(page, m.locator('.modal-content'), '04_settings');
        log('popup cài đặt:', (await m.innerText()).replace(/\n+/g, ' | '));
        const close = m.locator('button', { hasText: /^\s*(Đóng|Hủy)\s*$/ });
        if (await close.count()) await close.last().click(); else await page.keyboard.press('Escape');
    },
};

(async () => {
    const { browser, page } = await open(__dirname);
    const names = ONLY.length ? ONLY : Object.keys(steps);
    for (const n of names) {
        try { log('==', n); await steps[n](page); } catch (e) { log('LỖI bước', n, e.message.split('\n')[0]); }
    }
    await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });

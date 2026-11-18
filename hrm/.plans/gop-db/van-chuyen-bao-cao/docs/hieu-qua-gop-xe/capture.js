// Chụp ảnh SRS + HDSD "Báo cáo hiệu quả gộp xe vận tải" trên DEV (dev-hrm), headless riêng.
// Màn CHỈ ĐỌC: Tìm kiếm, popup danh sách, xem trước In, Xuất Excel (file để trong hdsd_shots). Không bấm Lưu cấu hình cột.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const fs = require('fs');
const path = require('path');
const C = require('./_cap_common.js').make(__dirname);
const { log, shot, shotEl, shotM, modal, icon, clipIcon, ff, pick, go, toasts } = C;

const ROUTE = '/transport/trip-gross-reports/by-vehicle';
const ITEM = 'Báo cáo hiệu quả gộp xe vận tải';
const PLATE = '37C-31738';

async function lastMonth(page) {
    await go(page, ROUTE);
    const t = Date.now();
    await pick(page, 'Kỳ', 'Tháng trước');
    log('Tải kỳ Tháng trước (ms, gồm chờ 3s):', Date.now() - t);
}

const steps = {
    async menu(page) {
        await go(page, ROUTE);
        await page.mouse.move(30, 300);
        await page.waitForTimeout(1500);
        await clipIcon(page, page.locator('a.logo').first(), 'menu_phanhe', 8, 300);
        const cat = page.locator('a.cat', { hasText: /Báo cáo vận chuyển/ }).first();
        await clipIcon(page, cat, 'menu_nhom', 0, 300);
        await cat.click();
        await page.waitForTimeout(1500);
        await page.screenshot({ path: path.join(C.SHOTS, '00_menu.png') });
        const it = page.getByText(ITEM, { exact: true });
        for (let i = 0; i < (await it.count()); i++) {
            const b = await it.nth(i).boundingBox();
            if (b && b.x > 280) {
                await clipIcon(page, it.nth(i).locator('xpath=..'), 'menu_muc', 2);
                break;
            }
        }
    },
    async open(page) {
        const t = Date.now();
        await go(page, ROUTE);
        log('Mở màn (Tháng này) ms gồm chờ 3.5s:', Date.now() - t);
        await shot(page, '01_open');
        await icon(ff(page, 'Kỳ'), 'o_ky');
        await icon(ff(page, 'Công ty'), 'o_congty');
        await icon(page.locator('.ff:visible', { hasText: 'Biển số xe' }), 'o_bienso');
        await icon(page.locator('button:visible', { hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(page.locator('button:visible', { hasText: 'Xóa lọc' }), 'btn_xoaloc');
        await icon(page.locator('button:visible', { hasText: 'In báo cáo' }), 'btn_in');
        await icon(page.locator('button:visible', { hasText: 'Xuất Excel' }), 'btn_xuatexcel');
        await icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        fs.writeFileSync(path.join(C.SHOTS, '_open.txt'), await page.locator('body').innerText());
    },
    async report(page) {
        await lastMonth(page);
        await shot(page, '03_report');
        await shot(page, '03_report_full', { fullPage: true });
        await shotEl(page, page.locator('.ptr-table').first(), '03b_table');
        await shotEl(page, page.locator('section.rsum').first(), '03c_summary');
        const rows = await page.locator('table.rsum-tb tr').evaluateAll((trs) => trs.map((tr) => [...tr.children].map((td) => td.innerText.trim().replace(/\s+/g, ' ')).join(' | ')));
        fs.writeFileSync(path.join(C.SHOTS, '_report_rows.txt'), rows.join('\n'));
        fs.writeFileSync(path.join(C.SHOTS, '_report.txt'), await page.locator('body').innerText());
        log('Chân bảng:', await page.locator('.ptr-table').innerText().then((t) => t.split('\n').slice(-6).join(' / ')));
        // tooltip cột Lãi gộp + dòng TỔNG
        const th = page.locator('thead th[data-col="gross"]').first();
        await th.locator('.info-tip, i, svg').last().hover().catch(() => th.hover());
        await page.waitForTimeout(900);
        await page.screenshot({ path: path.join(C.SHOTS, '04_tip.png') });
        log('Tip cột:', await page.locator('.popover:visible, .tooltip:visible').allTextContents());
        await icon(page.locator('.rsum-tb__level-wrap'), 'o_capbung');
        await icon(page.locator('table.rsum-tb a.v2-cell-link', { hasText: PLATE }), 'lnk_bienso');
        await icon(page.locator('.rsum-tb__sec .rsum-drill'), 'lnk_sochuyen');
        // cấp bung: Chỉ công ty
        await page.locator('.rsum-tb__level-wrap .select2-selection').first().click();
        await page.waitForTimeout(500);
        log('Ô chọn cấp:', await page.locator('.select2-results__option:visible').allTextContents());
        await page.locator('.select2-results__option:visible', { hasText: 'Chỉ công ty' }).first().click();
        await page.waitForTimeout(1200);
        await shotEl(page, page.locator('.ptr-table').first(), '03d_level1');
    },
    async tipsum(page) {
        await lastMonth(page);
        const tips = [];
        for (const sel of ['.rsum-goal', '.rsum-blk[data-block="trips"] .rsum-blk__title', '.rsum-blk[data-block="money"] .rsum-blk__title', '.rsum-blk[data-block="km"] .rsum-blk__title', '.rsum-tb__sec .rsum-tb__name', 'thead th[data-col="km_norm"]', 'thead th[data-col="km_real"]', 'thead th[data-col="km_diff"]', 'thead th[data-col="diff_pct"]', 'thead th[data-col="revenue"]', 'thead th[data-col="driver_cost"]']) {
            const el = page.locator(sel).first();
            const ic = el.locator('i, svg, .info-tip').last();
            await (await ic.count() ? ic : el).hover().catch(() => {});
            await page.waitForTimeout(800);
            tips.push(sel + ' => ' + (await page.locator('.popover:visible, .tooltip:visible').allTextContents()).join(' || '));
            await page.mouse.move(720, 897);
            await page.waitForTimeout(300);
        }
        fs.writeFileSync(path.join(C.SHOTS, '_tips.txt'), tips.join('\n'));
    },
    async drill(page) {
        await lastMonth(page);
        await page.locator('.rsum-tb__sec .rsum-drill').first().click();
        await modal(page).locator('tbody tr').first().waitFor({ timeout: 30000 });
        await page.waitForTimeout(1500);
        await shotM(page, '05_drill');
        fs.writeFileSync(path.join(C.SHOTS, '_drill.txt'), await modal(page).innerText());
        await icon(modal(page).locator('button', { hasText: 'In danh sách' }), 'btn_indanhsach');
        await icon(modal(page).locator('button', { hasText: 'Xuất Excel danh sách' }), 'btn_xuatexceldanhsach');
        await icon(modal(page).locator('button', { hasText: 'Đóng' }), 'btn_dong');
        await modal(page).locator('button', { hasText: 'Đóng' }).last().click();
        await page.waitForTimeout(800);
        // ô Chuyến lỗ ở khối tổng hợp
        await page.locator('.rsum-blk__item[data-item="loss"] .rsum-drill').first().click();
        await modal(page).locator('tbody tr').first().waitFor({ timeout: 30000 });
        await page.waitForTimeout(1500);
        await shotM(page, '05b_drill_loss');
        log('Popup chuyến lỗ:', (await modal(page).innerText()).slice(0, 300));
        await modal(page).locator('button', { hasText: 'Đóng' }).last().click();
        await page.waitForTimeout(800);
        // số chuyến của 1 xe
        const row = page.locator('tr', { has: page.locator('a.v2-cell-link', { hasText: PLATE }) }).first();
        await row.locator('.rsum-drill').first().click();
        await modal(page).locator('tbody tr').first().waitFor({ timeout: 30000 });
        await page.waitForTimeout(1500);
        await shotM(page, '05c_drill_plate');
        log('Popup 1 xe:', (await modal(page).innerText()).slice(0, 400));
        // In danh sách -> chọn cột
        await modal(page).locator('button', { hasText: 'In danh sách' }).click();
        await page.waitForTimeout(1500);
        await shotM(page, '05d_drill_print_opt');
        log('Chọn cột in danh sách:', (await modal(page).innerText()).slice(0, 500));
        await modal(page).locator('button', { hasText: /^\s*In\s*$/ }).last().click();
        await page.waitForTimeout(6000);
        await shotM(page, '05e_drill_print');
        await page.keyboard.press('Escape');
    },
    async link(page, ctx) {
        await lastMonth(page);
        const [np] = await Promise.all([ctx.waitForEvent('page'), page.locator('table.rsum-tb a.v2-cell-link', { hasText: PLATE }).first().click()]);
        await np.setViewportSize({ width: 1440, height: 900 });
        await np.waitForLoadState('networkidle').catch(() => {});
        await np.waitForTimeout(5000);
        log('Tab mới:', np.url());
        await np.mouse.move(720, 897);
        await np.screenshot({ path: path.join(C.SHOTS, '06_link.png') });
        await np.close();
    },
    async filter(page) {
        await lastMonth(page);
        await pick(page, 'Biển số xe', PLATE);
        await shot(page, '07_filter_plate');
        log('Lọc biển số:', (await page.locator('.rsum-goal').innerText()).replace(/\s+/g, ' '));
        await go(page, ROUTE);
        await pick(page, 'Kỳ', 'Tháng trước');
        await page.locator('.ff:visible', { hasText: 'Công ty' }).locator('.select2-selection').first().click();
        await page.waitForTimeout(600);
        log('DS công ty:', await page.locator('.select2-results__option:visible').allTextContents());
        await page.locator('.select2-results__option:visible').nth(1).click();
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(3000);
        await shot(page, '07b_filter_company');
        log('Lọc công ty:', (await page.locator('.rsum-goal').innerText()).replace(/\s+/g, ' '));
    },
    async custom(page) {
        await go(page, ROUTE);
        await page.locator('.ff:visible', { hasText: 'Kỳ' }).first().locator('.select2-selection').first().click();
        await page.waitForTimeout(500);
        log('Lựa chọn Kỳ:', await page.locator('.select2-results__option:visible').allTextContents());
        await page.locator('.select2-results__option:visible', { hasText: 'Tuỳ chọn' }).first().click();
        await page.waitForTimeout(1500);
        await icon(page.locator('.ff:visible', { hasText: 'Thời gian' }), 'o_thoigian');
        await page.locator('button:visible', { hasText: /^\s*Tìm kiếm\s*$/ }).first().click();
        await page.waitForTimeout(700);
        log('Toast thiếu ngày:', await toasts(page));
        await shot(page, '08_custom');
        // nhập khoảng ngày ngược / đúng
        const inp = page.locator('.ff:visible', { hasText: 'Thời gian' }).locator('input').first();
        log('Placeholder ô thời gian:', await page.locator('.ff:visible', { hasText: 'Thời gian' }).locator('input').evaluateAll((xs) => xs.map((x) => x.placeholder)));
        await inp.click();
        await page.waitForTimeout(800);
        await page.screenshot({ path: path.join(C.SHOTS, '08b_custom_cal.png') });
        await page.keyboard.press('Escape');
    },
    async print(page) {
        await lastMonth(page);
        await page.locator('button:visible', { hasText: 'In báo cáo' }).click();
        await page.waitForTimeout(1500);
        await shotM(page, '09_print_opt');
        await icon(modal(page).locator('button', { hasText: /^\s*In\s*$/ }), 'btn_in_modal');
        await icon(modal(page).locator('button', { hasText: 'Hủy' }), 'btn_huy');
        await modal(page).locator('button', { hasText: /^\s*In\s*$/ }).last().click();
        await page.waitForTimeout(8000);
        await shotM(page, '10_print');
        log('Bản in:', (await modal(page).innerText()).slice(0, 300));
        await page.keyboard.press('Escape');
        await page.waitForTimeout(1000);
        // bản Danh sách chuyến xe
        await page.locator('button:visible', { hasText: 'In báo cáo' }).click();
        await page.waitForTimeout(1500);
        await modal(page).getByText('Danh sách chuyến xe', { exact: true }).first().click();
        await page.waitForTimeout(800);
        await shotM(page, '09b_print_opt_list');
        log('Chọn cột bản danh sách:', (await modal(page).innerText()).slice(0, 600));
        await modal(page).locator('button', { hasText: /^\s*In\s*$/ }).last().click();
        await page.waitForTimeout(8000);
        await shotM(page, '10b_print_list');
        await page.keyboard.press('Escape');
    },
    async exportx(page) {
        await lastMonth(page);
        await page.locator('button:visible', { hasText: 'Xuất Excel' }).first().click();
        await page.waitForTimeout(1500);
        await shotM(page, '11_export_opt');
        const txt = await modal(page).innerText();
        log('Cửa sổ xuất:', txt.slice(0, 600));
        const btn = modal(page).locator('button', { hasText: /^\s*Xuất( Excel| file)?\s*$/ }).last();
        await icon(btn, 'btn_xuat_modal');
        const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 90000 }), btn.click()]);
        const out = path.join(C.SHOTS, dl.suggestedFilename());
        await dl.saveAs(out);
        log('Excel:', out);
        log('Toast:', await toasts(page));
    },
    async colcfg(page) {
        await go(page, ROUTE);
        await page.locator('button[title="Cấu hình cột hiển thị"]').click();
        await page.waitForTimeout(1500);
        await shotM(page, '12_colcfg');
        await icon(modal(page).locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await icon(modal(page).locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        await icon(modal(page).locator('button', { hasText: /^\s*Lưu\s*$/ }), 'btn_luu');
        await icon(modal(page).locator('button', { hasText: 'Đóng' }), 'btn_dong_cfg');
        await modal(page).locator('button', { hasText: 'Đóng' }).last().click(); // KHÔNG bấm Lưu
    },
};

C.run(steps, process.argv.slice(2)).catch((e) => {
    console.error(e);
    process.exit(1);
});

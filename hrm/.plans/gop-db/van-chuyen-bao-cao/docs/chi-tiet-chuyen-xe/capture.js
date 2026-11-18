// Chụp ảnh SRS + HDSD "Báo cáo chi tiết chuyến xe" trên DEV (dev-hrm), headless riêng.
// Màn CHỈ ĐỌC: Tìm kiếm, popup danh sách, xem trước In, Xuất Excel (file để trong hdsd_shots). Không bấm Lưu cấu hình cột.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const fs = require('fs');
const path = require('path');
const C = require('../hieu-qua-gop-xe/_cap_common.js').make(__dirname);
const { log, shot, shotEl, shotM, modal, icon, clipIcon, ff, pick, go, toasts } = C;

const ROUTE = '/transport/trip-detail-report';
const ITEM = 'Báo cáo chi tiết chuyến xe';

async function lastMonth(page) {
    await go(page, ROUTE);
    const t = Date.now();
    await pick(page, 'Kỳ', 'Tháng trước');
    log('Tải kỳ Tháng trước (ms, gồm chờ 3s):', Date.now() - t);
}
const rowsOf = (page) =>
    page.locator('table.rsum-tb tr').evaluateAll((trs) => trs.map((tr) => [...tr.children].map((td) => td.innerText.trim().replace(/\s+/g, ' ')).join(' | ')));
const field = (page, label) => page.locator('.ff:visible').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + label + '\\s*$') }) }).first();

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
        fs.writeFileSync(path.join(C.SHOTS, '_open.txt'), await page.locator('body').innerText());
        const labels = await page.locator('.ff:visible .ff__text').allTextContents();
        log('Nhãn ô lọc:', labels.map((x) => x.trim()));
        const map = {
            'Kỳ': 'o_ky', 'Xem theo': 'o_xemtheo', 'Công ty': 'o_congty', 'Phiếu hạch toán': 'o_phieuht', 'Chuyến xe': 'o_chuyenxe',
            'Tuyến đường': 'o_tuyen', 'Lái xe': 'o_laixe', 'Biển số xe': 'o_bienso', 'Phiếu nhập/xuất': 'o_phieunx',
            'Đối tượng chịu phí': 'o_doituong', 'Phòng ban': 'o_phongban', 'Bộ phận': 'o_bophan', 'Nhân viên kinh doanh': 'o_nvkd',
        };
        for (const [lb, nm] of Object.entries(map)) {
            let loc = field(page, lb);
            if (!(await loc.count())) loc = page.locator('.ff:visible', { hasText: lb }).first();
            await icon(loc, nm);
        }
        await icon(page.locator('button:visible', { hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(page.locator('button:visible', { hasText: 'Xóa lọc' }), 'btn_xoaloc');
        await icon(page.locator('button:visible', { hasText: 'In báo cáo' }), 'btn_in');
        await icon(page.locator('button:visible', { hasText: 'Xuất Excel' }), 'btn_xuatexcel');
        await icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        await icon(page.locator('button:visible', { hasText: 'Cài đặt bộ lọc' }), 'btn_caidatboloc');
        await icon(page.locator('button:visible', { hasText: /tìm kiếm nâng cao/i }), 'btn_timkiemnangcao');
        // ô Đối tượng chịu phí: lựa chọn
        await field(page, 'Đối tượng chịu phí').locator('.select2-selection').first().click().catch(() => {});
        await page.waitForTimeout(600);
        log('Đối tượng chịu phí:', await page.locator('.select2-results__option:visible').allTextContents());
        await page.keyboard.press('Escape');
        await field(page, 'Xem theo').locator('.select2-selection').first().click().catch(() => {});
        await page.waitForTimeout(600);
        log('Xem theo:', await page.locator('.select2-results__option:visible').allTextContents());
        await page.keyboard.press('Escape');
    },
    async report(page) {
        await lastMonth(page);
        await shot(page, '03_report');
        await shot(page, '03_report_full', { fullPage: true });
        await shotEl(page, page.locator('.ptr-table').first(), '03b_table');
        await shotEl(page, page.locator('section.rsum').first(), '03c_summary');
        fs.writeFileSync(path.join(C.SHOTS, '_report_rows.txt'), (await rowsOf(page)).join('\n'));
        fs.writeFileSync(path.join(C.SHOTS, '_report.txt'), await page.locator('body').innerText());
        log('Chân bảng:', await page.locator('.ptr-table').innerText().then((t) => t.split('\n').slice(-6).join(' / ')));
        await icon(page.locator('.rsum-tb__level-wrap'), 'o_capbung');
        await icon(page.locator('.rsum-tb__sec .rsum-drill'), 'lnk_sophieu');
        await page.locator('.rsum-tb__level-wrap .select2-selection').first().click();
        await page.waitForTimeout(500);
        log('Ô chọn cấp:', await page.locator('.select2-results__option:visible').allTextContents());
        await page.locator('.select2-results__option:visible', { hasText: 'Đến từng' }).first().click();
        await page.waitForTimeout(1500);
        await shot(page, '03d_level3');
        await shot(page, '03d_level3_full', { fullPage: true });
        fs.writeFileSync(path.join(C.SHOTS, '_report_rows_l3.txt'), (await rowsOf(page)).join('\n'));
        const badge = page.locator('.trp-badge').first();
        if (await badge.count()) {
            log('Nhãn ghép:', await badge.innerText(), '| title:', await badge.getAttribute('title'));
            await badge.scrollIntoViewIfNeeded();
            const tr = page.locator('tr', { has: badge }).first();
            await shotEl(page, tr, '03e_shared_row');
            await icon(badge, 'lnk_ghep');
        } else log('Không có nhãn ghép trang 1');
        await icon(page.locator('.trp-row--leaf a.v2-cell-link').first(), 'lnk_phieuht');
    },
    async trip(page) {
        await lastMonth(page);
        await pick(page, 'Xem theo', 'Chuyến xe');
        await shot(page, '04_trip');
        await shot(page, '04_trip_full', { fullPage: true });
        fs.writeFileSync(path.join(C.SHOTS, '_trip_rows.txt'), (await rowsOf(page)).join('\n'));
        log('Chân bảng (chuyến):', await page.locator('.ptr-table').innerText().then((t) => t.split('\n').slice(-6).join(' / ')));
        await page.locator('.rsum-tb__level-wrap .select2-selection').first().click();
        await page.waitForTimeout(500);
        log('Ô chọn cấp (chuyến):', await page.locator('.select2-results__option:visible').allTextContents());
        await page.keyboard.press('Escape');
    },
    async tipsum(page) {
        await lastMonth(page);
        const tips = [];
        const sels = ['.rsum-blk[data-block="trips"] .rsum-blk__title', '.rsum-blk[data-block="subject"] .rsum-blk__title', '.rsum-blk[data-block="money"] .rsum-blk__title', '.rsum-tb__sec .rsum-tb__name'];
        for (const id of ['count', 'km', 'km_additional', 'recipe_main', 'recipe_extra', 'actual_fee', 'tax', 'after_tax', 'toll', 'sale_name']) sels.push(`thead th[data-col="${id}"]`);
        for (const sel of sels) {
            const el = page.locator(sel).first();
            if (!(await el.count())) continue;
            const ic = el.locator('i, svg, .info-tip').last();
            await ((await ic.count()) ? ic : el).hover().catch(() => {});
            await page.waitForTimeout(800);
            tips.push(sel + ' => ' + (await page.locator('.popover:visible, .tooltip:visible').allTextContents()).join(' || '));
            await page.mouse.move(720, 897);
            await page.waitForTimeout(300);
        }
        const th = page.locator('thead th[data-col="after_tax"]').first();
        await th.locator('i, svg, .info-tip').last().hover().catch(() => {});
        await page.waitForTimeout(900);
        await page.screenshot({ path: path.join(C.SHOTS, '04b_tip.png') });
        // tip ô Kỳ / Xem theo / Công ty
        for (const lb of ['Kỳ', 'Xem theo', 'Công ty']) {
            await field(page, lb).locator('i, svg').first().hover().catch(() => {});
            await page.waitForTimeout(800);
            tips.push('ô ' + lb + ' => ' + (await page.locator('.popover:visible, .tooltip:visible').allTextContents()).join(' || '));
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
        // Xuất Excel danh sách (dựng ở trình duyệt, tải thẳng)
        const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 90000 }), modal(page).locator('button', { hasText: 'Xuất Excel danh sách' }).click()]);
        await dl.saveAs(path.join(C.SHOTS, dl.suggestedFilename()));
        log('Excel danh sách:', dl.suggestedFilename());
        await page.waitForTimeout(1000);
        await modal(page).locator('button', { hasText: 'Đóng' }).last().click();
        await page.waitForTimeout(800);
        const shared = page.locator('.rsum-blk__item[data-item="shared"] .rsum-drill').first();
        if (await shared.count()) {
            await shared.click();
            await modal(page).locator('tbody tr').first().waitFor({ timeout: 30000 });
            await page.waitForTimeout(1500);
            await shotM(page, '05b_drill_shared');
            log('Popup ghép:', (await modal(page).innerText()).slice(0, 300));
            await modal(page).locator('button', { hasText: 'Đóng' }).last().click();
            await page.waitForTimeout(800);
        }
        // số phiếu của 1 khách hàng (dòng nhóm đầu)
        await page.locator('tr.rsum-tb__row--d0 .rsum-drill').first().click();
        await modal(page).locator('tbody tr').first().waitFor({ timeout: 30000 });
        await page.waitForTimeout(1500);
        await shotM(page, '05c_drill_customer');
        log('Popup 1 KH:', (await modal(page).innerText()).slice(0, 400));
        await modal(page).locator('button', { hasText: 'In danh sách' }).click();
        await page.waitForTimeout(1500);
        await shotM(page, '05d_drill_print_opt');
        log('Chọn cột in danh sách:', (await modal(page).innerText()).slice(0, 600));
        await modal(page).locator('button', { hasText: /^\s*In\s*$/ }).last().click();
        await page.waitForTimeout(8000);
        await shotM(page, '05e_drill_print');
        await page.keyboard.press('Escape');
    },
    async filter(page) {
        await lastMonth(page);
        await pick(page, 'Đối tượng chịu phí', 'Nhân viên chịu');
        await page.waitForTimeout(6000);
        await shot(page, '07_filter_subject');
        log('Lọc NV chịu:', (await page.locator('.rsum-goal').innerText()).replace(/\s+/g, ' '));
        await go(page, ROUTE);
        await pick(page, 'Kỳ', 'Tháng trước');
        const inp = field(page, 'Phiếu hạch toán').locator('input').first();
        await inp.fill('03199');
        await page.waitForTimeout(1500);
        log('Gõ chưa Enter:', (await page.locator('.rsum-goal').innerText()).replace(/\s+/g, ' '));
        await inp.press('Enter');
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(3000);
        log('Lọc phiếu HT:', (await page.locator('.rsum-goal').innerText()).replace(/\s+/g, ' '));
        await shot(page, '07b_filter_doc');
        await page.locator('button:visible', { hasText: 'Xóa lọc' }).first().click();
        await page.waitForTimeout(3000);
        log('Sau Xóa lọc:', (await page.locator('.rsum-goal').innerText()).replace(/\s+/g, ' '));
    },
    async print(page) {
        await lastMonth(page);
        await page.locator('button:visible', { hasText: 'In báo cáo' }).click();
        await page.waitForTimeout(1500);
        await shotM(page, '09_print_opt');
        log('Cửa sổ in:', (await modal(page).innerText()).slice(0, 800));
        await icon(modal(page).locator('button', { hasText: /^\s*In\s*$/ }), 'btn_in_modal');
        await icon(modal(page).locator('button', { hasText: 'Hủy' }), 'btn_huy');
        await modal(page).locator('button', { hasText: /^\s*In\s*$/ }).last().click();
        await page.waitForTimeout(10000);
        await shotM(page, '10_print');
        log('Bản in:', (await modal(page).innerText()).slice(0, 300));
        await page.keyboard.press('Escape');
    },
    async exportx(page) {
        await lastMonth(page);
        const t = Date.now();
        const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 120000 }), page.locator('button:visible', { hasText: 'Xuất Excel' }).first().click()]);
        await dl.saveAs(path.join(C.SHOTS, dl.suggestedFilename()));
        log('Excel cây:', dl.suggestedFilename(), Date.now() - t, 'ms');
        log('Toast:', await toasts(page));
    },
    async wide(page) {
        await page.setViewportSize({ width: 2700, height: 1300 });
        await lastMonth(page);
        await page.locator('.rsum-tb__level-wrap .select2-selection').first().click();
        await page.waitForTimeout(500);
        await page.locator('.select2-results__option:visible', { hasText: 'Đến từng' }).first().click();
        await page.waitForTimeout(1500);
        await shotEl(page, page.locator('.ptr-table').first(), '03f_wide');
        await pick(page, 'Xem theo', 'Chuyến xe');
        await page.waitForTimeout(3000);
        await shotEl(page, page.locator('.ptr-table').first(), '04c_wide');
        await page.setViewportSize({ width: 1440, height: 900 });
    },
    async colcfg(page) {
        await go(page, ROUTE);
        await page.locator('button[title="Cấu hình cột hiển thị"]').click();
        await page.waitForTimeout(1500);
        await shotM(page, '12_colcfg');
        log('Cột (KH):', (await modal(page).innerText()).replace(/\n/g, ' | '));
        await icon(modal(page).locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await icon(modal(page).locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        await icon(modal(page).locator('button', { hasText: /^\s*Lưu\s*$/ }), 'btn_luu');
        await icon(modal(page).locator('button', { hasText: 'Đóng' }), 'btn_dong_cfg');
        await modal(page).locator('button', { hasText: 'Đóng' }).last().click(); // KHÔNG bấm Lưu
        await page.waitForTimeout(800);
        await pick(page, 'Xem theo', 'Chuyến xe');
        await page.locator('button[title="Cấu hình cột hiển thị"]').click();
        await page.waitForTimeout(1500);
        log('Cột (chuyến):', (await modal(page).innerText()).replace(/\n/g, ' | '));
        await modal(page).locator('button', { hasText: 'Đóng' }).last().click();
    },
};

C.run(steps, process.argv.slice(2)).catch((e) => {
    console.error(e);
    process.exit(1);
});

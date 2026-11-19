// Chụp ảnh SRS + HDSD cho 2 báo cáo bốc xếp (theo NCC / theo nhân viên) trên DEV — khuôn lookup-stock-companies/docs/capture.js.
// Màn CHỈ ĐỌC: chỉ đổi bộ lọc, bấm Tìm kiếm, mở popup, xem trước In (KHÔNG bấm In ra máy in), Xuất Excel (file lưu trong
// hdsd_shots/), mở / đóng cửa sổ Cấu hình cột, Cài đặt bộ lọc (KHÔNG bấm Lưu).
// Dùng: require('<đây>').run(__dirname, CFG, process.argv.slice(2))
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/danh-muc-kho/docs/_capture_login.js');

const esc = (s) => s.replace(/[.*+?^${}()|[\]\\-]/g, '\\$&');

function make(dir, CFG) {
    const SHOTS = path.join(dir, 'hdsd_shots');
    const ICONS = path.join(SHOTS, 'icons');
    fs.mkdirSync(ICONS, { recursive: true });
    const save = (name, text) => fs.writeFileSync(path.join(SHOTS, name), text);
    const away = async (page) => {
        await page.mouse.move(1435, 895);
        await page.waitForTimeout(500);
    };
    const shot = async (page, name) => {
        await away(page);
        await page.screenshot({ path: path.join(SHOTS, name + '.png') });
    };
    const modal = (page) => page.locator('.modal.show:visible').last();
    const shotM = async (page, name) => {
        await away(page);
        await modal(page).locator('.modal-content').first().screenshot({ path: path.join(SHOTS, name + '.png') });
    };
    const icon = async (loc, name) => {
        const l = loc.first();
        if (!(await l.count())) return console.log('thiếu icon', name);
        await l.scrollIntoViewIfNeeded().catch(() => {});
        await l.screenshot({ path: path.join(ICONS, name + '.png') });
    };
    const clipIcon = async (page, loc, name, pad = 0, maxX = null) => {
        const b = await loc.first().boundingBox();
        if (!b) return console.log('thiếu icon', name);
        let w = b.width + 2 * pad;
        if (maxX !== null && b.x - pad + w > maxX) w = maxX - b.x + pad;
        await page.screenshot({ path: path.join(ICONS, name + '.png'), clip: { x: b.x - pad, y: b.y - pad, width: w, height: b.height + 2 * pad } });
    };
    const ff = (page, label) =>
        page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + esc(label) + '\\s*\\*?\\s*$') }) });
    const btn = (page, text) => page.locator('button', { hasText: new RegExp('^\\s*' + esc(text) + '\\s*$') });
    const timing = {};

    async function waitTable(page) {
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.locator('.rsum-tb tbody tr').first().waitFor({ timeout: 120000 }).catch(() => {});
        await page.waitForTimeout(1500);
    }
    async function go(page) {
        const t0 = Date.now();
        await page.goto(DEV + CFG.route);
        await waitTable(page);
        timing.load = Date.now() - t0;
    }
    async function pickSelect(page, label, option) {
        const f = ff(page, label).first();
        await f.locator('.select2-selection').first().click();
        await page.waitForTimeout(700);
        await page.locator('.select2-results__option:visible', { hasText: option }).first().click();
        await page.waitForTimeout(800);
        await waitTable(page);
    }
    async function closeModal(page) {
        const m = modal(page);
        const b = m.locator('button', { hasText: /^\s*(Đóng|Hủy)\s*$/ });
        if (await b.count()) await b.last().click();
        else await page.keyboard.press('Escape');
        await page.waitForTimeout(1000);
    }
    async function tipShot(page, th, name) {
        const t = th.locator('.ptr-info').first();
        await t.hover();
        await page.waitForTimeout(1000);
        const pop = page.locator('.popover:visible').last();
        if (!(await pop.count())) return console.log('không hiện popover', name);
        const b1 = await th.boundingBox();
        const b2 = await pop.boundingBox();
        const x = Math.max(0, Math.min(b1.x, b2.x) - 10);
        const y = Math.max(0, Math.min(b1.y, b2.y) - 10);
        const w = Math.min(1440 - x, Math.max(b1.x + b1.width, b2.x + b2.width) - x + 10);
        const h = Math.max(b1.y + b1.height, b2.y + b2.height) - y + 10;
        await page.screenshot({ path: path.join(SHOTS, name + '.png'), clip: { x, y, width: w, height: h } });
        save('_' + name + '.txt', await pop.innerText());
        await away(page);
    }

    const steps = {
        async menu(page) {
            await go(page);
            await page.mouse.move(30, 300);
            await page.waitForTimeout(1500);
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
            if (el) await clipIcon(page, el.locator('xpath=..'), 'menu_muc', 2);
            else console.log('không thấy mục menu');
            await page.screenshot({ path: path.join(SHOTS, '00_menu.png') });
        },
        async list(page) {
            await go(page);
            console.log('thời gian tải (ms):', timing.load);
            save('_timing.txt', String(timing.load));
            await shot(page, '01_report');
            save('_report_text.txt', await page.locator('body').innerText());
            await icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
            await icon(btn(page, 'In báo cáo'), 'btn_inbaocao');
            await icon(btn(page, 'Xuất Excel'), 'btn_xuatexcel');
            await icon(btn(page, 'Cài đặt bộ lọc'), 'btn_caidatboloc');
            await icon(btn(page, 'Ẩn tìm kiếm nâng cao'), 'btn_antimkiem');
            await icon(btn(page, 'Tìm kiếm'), 'btn_timkiem');
            await icon(btn(page, 'Xóa lọc'), 'btn_xoaloc');
            for (const [lb, nm] of CFG.filters) {
                if (await ff(page, lb).count()) await icon(ff(page, lb), nm);
                else console.log('thiếu ô lọc', lb);
            }
            await away(page);
            await page.locator('section.rsum').first().screenshot({ path: path.join(SHOTS, '02_summary.png') });
            await icon(page.locator('tr.rsum-tb__sec .rsum-drill'), 'lnk_soluot');
            if (CFG.leaf) {
                await icon(page.locator('.rsum-tb__row--d1 a.arr-link').first(), 'lnk_phieu');
                await icon(page.locator('.rsum-tb__level-wrap'), 'o_cap');
                await icon(page.locator('button.rsum-caret').first(), 'btn_caret');
            }
            await icon(page.locator('button.rsum-toggle'), 'btn_thugon');
            await icon(page.locator('.paging, .pagination').first(), 'o_phantrang');
        },
        async custom(page) {
            await go(page);
            await pickSelect(page, 'Kỳ', 'Tuỳ chọn');
            await shot(page, '03_custom');
            await btn(page, 'Tìm kiếm').first().click();
            await page.waitForTimeout(700);
            await shot(page, '03b_custom_toast');
            save('_custom_text.txt', await page.locator('body').innerText());
            if (await ff(page, 'Thời gian').count()) await icon(ff(page, 'Thời gian'), 'o_thoigian');
        },
        async dropdown(page) {
            await go(page);
            const [lb, kw, name] = CFG.dropdown;
            const f = ff(page, lb).first();
            await f.locator('.select2-selection').first().click();
            await page.waitForTimeout(800);
            if (kw) {
                await page.locator('.select2-search__field:visible').last().fill(kw);
                await page.waitForTimeout(2500);
            }
            await shot(page, name);
            save('_' + name + '.txt', await page.locator('.select2-results:visible').last().innerText().catch(() => ''));
            await page.keyboard.press('Escape');
        },
        async read(page) {
            await go(page);
            if (CFG.readPeriod) await pickSelect(page, 'Kỳ', CFG.readPeriod);
            await away(page);
            await page.locator('.ptr-table').first().screenshot({ path: path.join(SHOTS, '05_read.png') });
            await page.locator('section.rsum').first().screenshot({ path: path.join(SHOTS, '05b_read_summary.png') });
            save('_read_text.txt', await page.locator('.arr-body').first().innerText());
            const th = page.locator('thead th').filter({ hasText: CFG.amountHead }).first();
            await tipShot(page, th, '06_tip_amount');
            const th2 = page.locator('tr.rsum-tb__sec td.rsum-tb__name').first();
            await tipShot(page, th2, '06b_tip_name');
            const blk = page.locator('.rsum-blk__title').first();
            await tipShot(page, blk, '06c_tip_block');
        },
        async level1(page) {
            if (!CFG.leaf) return;
            await go(page);
            const wrap = page.locator('.rsum-tb__level-wrap').first();
            await wrap.locator('.select2-selection').first().click();
            await page.waitForTimeout(700);
            await page.locator('.select2-results__option:visible', { hasText: 'Chỉ nhà cung cấp' }).first().click();
            await page.waitForTimeout(1200);
            await away(page);
            await page.locator('.ptr-table').first().screenshot({ path: path.join(SHOTS, '07_level1.png') });
        },
        async paging(page) {
            if (!CFG.pagingPeriod) return;
            await go(page);
            await pickSelect(page, 'Kỳ', CFG.pagingPeriod);
            await shot(page, '07_paging');
            save('_paging_text.txt', await page.locator('.arr-body').first().innerText());
        },
        async empty(page) {
            await go(page);
            if (CFG.emptyText) {
                const f = ff(page, CFG.emptyText).first();
                await f.locator('input').first().fill('ZZZ999');
                await page.keyboard.press('Enter');
            } else {
                await pickSelect(page, 'Kỳ', 'Tuần này');
            }
            await page.waitForTimeout(1500);
            await waitTable(page);
            await shot(page, '08_empty');
            save('_empty_text.txt', await page.locator('.arr-body').first().innerText());
        },
        async popup(page) {
            await go(page);
            if (CFG.popupPeriod) await pickSelect(page, 'Kỳ', CFG.popupPeriod);
            const row = CFG.popupRow
                ? page.locator('tr.rsum-tb__row--d0').filter({ hasText: CFG.popupRow }).first()
                : page.locator('tr.rsum-tb__sec').first();
            await row.locator('.rsum-drill').first().click();
            await page.waitForTimeout(1500);
            await modal(page).locator('tbody tr').first().waitFor({ timeout: 60000 }).catch(() => {});
            await page.waitForTimeout(1500);
            await shotM(page, '09_popup');
            save('_popup_text.txt', await modal(page).innerText());
            const m = modal(page);
            await icon(m.locator('button', { hasText: 'In danh sách' }), 'btn_indanhsach');
            await icon(m.locator('button', { hasText: 'Xuất Excel danh sách' }), 'btn_xuatexceldanhsach');
            await icon(m.locator('button', { hasText: /^\s*Đóng\s*$/ }), 'btn_dong');
            await icon(m.locator('input').first(), 'o_timpopup');
            // In danh sách -> popup chọn cột (chỉ xem, bấm Hủy)
            await m.locator('button', { hasText: 'In danh sách' }).first().click();
            await page.waitForTimeout(1500);
            await shotM(page, '09b_popup_print');
            save('_popup_print_text.txt', await modal(page).innerText());
            await closeModal(page);
            await page.waitForTimeout(800);
            // Xuất Excel danh sách -> tải file
            const m2 = modal(page);
            if (await m2.locator('button', { hasText: 'Xuất Excel danh sách' }).count()) {
                await m2.locator('button', { hasText: 'Xuất Excel danh sách' }).first().click();
                await page.waitForTimeout(1500);
                await shotM(page, '09c_popup_export');
                const [dl] = await Promise.all([
                    page.waitForEvent('download', { timeout: 120000 }),
                    modal(page).locator('button', { hasText: /^\s*Xuất Excel\s*$/ }).last().click(),
                ]);
                await dl.saveAs(path.join(SHOTS, '_popup_' + dl.suggestedFilename()));
                console.log('xuất popup:', dl.suggestedFilename());
            }
        },
        async print(page) {
            await go(page);
            if (CFG.printPeriod) await pickSelect(page, 'Kỳ', CFG.printPeriod);
            await btn(page, 'In báo cáo').first().click();
            await page.waitForTimeout(1500);
            await shotM(page, '10_print_opt');
            save('_print_opt_text.txt', await modal(page).innerText());
            await icon(modal(page).locator('button', { hasText: /^\s*In\s*$/ }), 'btn_in');
            await icon(modal(page).locator('button', { hasText: /^\s*Hủy\s*$/ }), 'btn_huy');
            await modal(page).locator('button', { hasText: /^\s*In\s*$/ }).last().click();
            await page.waitForTimeout(5000);
            await page.waitForLoadState('networkidle').catch(() => {});
            await page.waitForTimeout(2000);
            await shotM(page, '11_print_preview');
            save('_print_preview_text.txt', await modal(page).innerText());
            await page.keyboard.press('Escape');
            await page.waitForTimeout(800);
            // bản danh sách
            await btn(page, 'In báo cáo').first().click();
            await page.waitForTimeout(1500);
            await modal(page).locator('label', { hasText: 'In danh sách lượt bốc xếp' }).first().click().catch(() => {});
            await page.waitForTimeout(600);
            await shotM(page, '10b_print_opt_detail');
            await modal(page).locator('button', { hasText: /^\s*In\s*$/ }).last().click();
            await page.waitForTimeout(6000);
            await shotM(page, '11b_print_preview_detail');
            await page.keyboard.press('Escape');
        },
        async export(page) {
            await go(page);
            if (CFG.printPeriod) await pickSelect(page, 'Kỳ', CFG.printPeriod);
            await btn(page, 'Xuất Excel').first().click();
            await page.waitForTimeout(1500);
            await shotM(page, '12_export_opt');
            save('_export_opt_text.txt', await modal(page).innerText());
            await icon(modal(page).locator('button', { hasText: /^\s*Xuất Excel\s*$/ }), 'btn_xuatexcel_popup');
            const t0 = Date.now();
            const [dl] = await Promise.all([
                page.waitForEvent('download', { timeout: 180000 }),
                modal(page).locator('button', { hasText: /^\s*Xuất Excel\s*$/ }).last().click(),
            ]);
            await dl.saveAs(path.join(SHOTS, '_export_' + dl.suggestedFilename()));
            console.log('xuất file:', dl.suggestedFilename(), Date.now() - t0, 'ms');
            // bản danh sách
            await page.waitForTimeout(1500);
            await btn(page, 'Xuất Excel').first().click();
            await page.waitForTimeout(1500);
            await modal(page).locator('label', { hasText: 'Xuất danh sách lượt bốc xếp' }).first().click().catch(() => {});
            await page.waitForTimeout(600);
            const [dl2] = await Promise.all([
                page.waitForEvent('download', { timeout: 180000 }),
                modal(page).locator('button', { hasText: /^\s*Xuất Excel\s*$/ }).last().click(),
            ]);
            await dl2.saveAs(path.join(SHOTS, '_export_detail_' + dl2.suggestedFilename()));
            console.log('xuất file ds:', dl2.suggestedFilename());
        },
        async colcfg(page) {
            await go(page);
            await page.locator('button[title="Cấu hình cột hiển thị"]').first().click();
            await page.waitForTimeout(1500);
            await shotM(page, '13_colcfg');
            save('_colcfg_text.txt', await modal(page).innerText());
            await icon(modal(page).locator('button', { hasText: /^\s*Lưu\s*$/ }), 'btn_luu');
            await closeModal(page);
        },
        async filtercfg(page) {
            await go(page);
            await btn(page, 'Cài đặt bộ lọc').first().click();
            await page.waitForTimeout(1500);
            await shotM(page, '14_filtercfg');
            save('_filtercfg_text.txt', await modal(page).innerText());
            await closeModal(page);
        },
    };

    return { steps };
}

async function run(dir, CFG, only) {
    const { steps } = make(dir, CFG);
    const { browser, page } = await open(dir);
    try {
        for (const [k, f] of Object.entries(steps)) {
            if (only.length && !only.includes(k)) continue;
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
}

module.exports = { run };

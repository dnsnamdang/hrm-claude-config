// Chụp ảnh HDSD + SRS màn Phiếu hủy hàng giữ (STT 191) trên DEV — chỉ đọc.
// AN TOÀN: mọi request API không phải GET đều bị chặn (abort) => không ghi được dữ liệu kể cả bấm nhầm.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js
const path = require('path');
const { openDev, DEV } = require('../../phieu-theo-form-quoc-gia/pw_dev.js');

const HERE = __dirname;
const OUT = path.join(HERE, 'hdsd_shots');
const IC = path.join(OUT, 'icons');
const log = [];

(async () => {
    const { browser, page } = await openDev(HERE, { scale: 1 });
    await page.setViewportSize({ width: 1920, height: 950 });
    await page.route('**/api/**', (r) => (r.request().method() === 'GET' ? r.continue() : r.abort()));
    page.on('dialog', (d) => d.accept().catch(() => {}));
    const W = (ms) => page.waitForTimeout(ms);
    const out = (n) => path.join(OUT, n + '.png');
    // Chuột ra góc phải dưới: (5,5) rê vào sidebar làm menu bung ra che màn.
    const away = async () => { await page.mouse.move(1915, 945); await W(400); };
    const shot = async (n, opt = {}) => { await away(); await page.screenshot({ path: out(n), ...opt }); log.push(n); };
    const eshot = async (loc, n, dir = OUT) => {
        try { await loc.first().scrollIntoViewIfNeeded(); await away(); await loc.first().screenshot({ path: path.join(dir, n + '.png') }); log.push(n); }
        catch (e) { log.push(n + ':ERR ' + e.message.split('\n')[0]); }
    };
    const icon = (loc, n) => eshot(loc, n, IC);
    const clipIcon = async (loc, n, w) => {
        try { await away(); const b = await loc.first().boundingBox(); await page.screenshot({ path: path.join(IC, n + '.png'), clip: { x: b.x, y: b.y, width: Math.min(w, b.width), height: b.height } }); log.push(n); }
        catch (e) { log.push(n + ':ERR ' + e.message.split('\n')[0]); }
    };
    const btn = (text, scope = page) => scope.locator('button', { hasText: new RegExp('^\\s*' + text + '\\s*$') });
    const modal = () => page.locator('.modal.show .modal-content').last();
    const closeModal = async (text = 'Đóng|Hủy') => {
        const b = page.locator('.modal.show button').filter({ hasText: new RegExp('^\\s*(' + text + ')') });
        if (await b.count()) await b.last().click(); else await page.keyboard.press('Escape');
        await W(800);
    };
    const list = async () => {
        await page.goto(DEV + '/finance/prepick-cancels');
        await page.waitForSelector('text=PHHG-', { timeout: 90000 });
        await page.waitForLoadState('networkidle').catch(() => {});
        await W(1500);
    };

    // ---- 1. Danh sách + menu
    await list();
    await shot('01_list', { clip: { x: 0, y: 0, width: 1920, height: 800 } });
    const firstCode = (await page.locator('tbody tr').first().locator('a.v2-cell-link').first().innerText()).trim();
    log.push('phiếu đầu: ' + firstCode);
    await page.mouse.move(28, 400); await W(1000);
    await page.locator('a.cat', { hasText: 'Hàng hoá - Dịch vụ' }).first().click(); await W(1000);
    await page.locator('a, div, li, button').filter({ hasText: /^\s*Giữ hàng\s*\d*\s*$/ }).locator('visible=true').last().click(); await W(1000);
    {
        const a = page.locator('a.row[data-k="/finance/prepick-cancels"]').locator('visible=true').first();
        const b1 = await a.boundingBox(); const b2 = await a.locator('.row-nm').boundingBox();
        await page.screenshot({ path: path.join(IC, 'menu_muc.png'), clip: { x: b1.x, y: b1.y, width: b2.x + b2.width - b1.x + 10, height: b1.height } });
        log.push('menu_muc');
    }
    await page.keyboard.press('Escape');
    await list();

    // ---- 2. Bộ lọc
    await clipIcon(page.locator('input[placeholder^="Tìm theo mã phiếu"]'), 'o_timnhanh', 250);
    await btn('Tìm kiếm nâng cao').first().click(); await W(1500);
    await eshot(page.locator('.smart-filter-card, section').filter({ hasText: 'Bộ lọc danh sách' }).first(), '02_filter');
    const field = (label) => page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + label + '\\s*$') }) }).locator('visible=true');
    for (const [lb, n] of [['Trạng thái', 'o_trangthai'], ['Mã phiếu yêu cầu', 'o_maphieuyc'], ['Người yêu cầu', 'o_nguoiyeucau'], ['Người tạo', 'o_nguoitao'], ['Tên/mã hàng hóa', 'o_tenmahang'], ['Ngày tạo', 'o_ngaytao']]) {
        await clipIcon(field(lb), n, 150);
    }
    // ---- 3. Cài đặt bộ lọc / Cấu hình cột / Xuất Excel
    await btn('Cài đặt bộ lọc').first().click(); await W(1500);
    await eshot(modal(), '26_filtercfg'); await closeModal('Đóng');
    await page.locator('button[title="Cấu hình cột hiển thị"]').first().click(); await W(1500);
    await eshot(modal(), '25_colcfg'); await closeModal('Đóng');
    await btn('Xuất Excel').first().click(); await W(1500);
    await eshot(modal(), '20_export'); await closeModal('Đóng');

    // ---- 4. Lịch sử + In từ dòng
    const r1 = page.locator('tbody tr').first();
    await r1.locator('[title="Lịch sử"]').first().click(); await W(2500);
    await eshot(modal(), '16_history'); await closeModal('Đóng');
    await r1.locator('[title="In"]').first().click(); await W(4000);
    { await away(); const b = await modal().boundingBox(); await page.screenshot({ path: out('18_print'), clip: { x: b.x, y: b.y, width: b.width, height: Math.round(b.height * 0.6) } }); log.push('18_print'); } // nửa dưới tờ giấy trắng -> cắt bỏ await closeModal('Đóng'); await page.keyboard.press('Escape'); await W(500);

    // ---- 5. Màn form: khổ 1440x640
    await page.setViewportSize({ width: 1440, height: 640 });
    // 5a. Chi tiết
    await page.locator('tbody tr').first().locator('a.v2-cell-link').first().click();
    await page.waitForURL(/prepick-cancels\/\d+/, { timeout: 60000 }); await page.waitForLoadState('networkidle').catch(() => {}); await W(2500);
    await shot('17_detail');
    await icon(btn('In'), 'btn_in');
    await icon(btn('Xem lịch sử'), 'btn_xemlichsu');
    await btn('Xem lịch sử').first().click(); await W(2000);
    await eshot(page.locator('.pc-history-card').first(), '16_history_detail');

    // 5b. Lập phiếu — lối 1 (Tạo mới ở danh sách)
    await page.goto(DEV + '/finance/prepick-cancels/create');
    await page.waitForLoadState('networkidle').catch(() => {}); await W(2500);
    await shot('10_create_empty');
    const look = page.locator('button[title="Chọn phiếu yêu cầu đang chờ duyệt"]').first();
    await icon(look, 'btn_tracuu');
    await look.click(); await W(3000);
    await eshot(modal(), '11_request');
    await icon(btn('Đóng', page.locator('.modal.show')), 'btn_dong');
    await page.locator('.modal.show tbody tr a.v2-cell-link').first().click(); await W(3000);
    await shot('10_create');
    await icon(btn('Duyệt'), 'btn_duyet');
    await icon(btn('Duyệt và tiếp tục'), 'btn_duyettieptuc');
    await icon(btn('Quay lại'), 'btn_quaylai');
    await btn('Duyệt').first().click(); await W(1500);
    await eshot(modal(), '14_confirm');
    await icon(btn('Duyệt', page.locator('.modal.show')), 'btn_confirm_duyet');
    await icon(btn('Hủy', page.locator('.modal.show')), 'btn_huy_confirm');
    await closeModal('Hủy');

    console.log(log.join('\n'));
    await browser.close();
})().catch((e) => { console.error(e); console.log(log.join('\n')); process.exit(1); });

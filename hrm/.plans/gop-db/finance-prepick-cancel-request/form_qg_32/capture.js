// Chụp ảnh HDSD + SRS màn Yêu cầu hủy hàng giữ (STT 32) trên DEV — chỉ đọc.
// AN TOÀN: mọi request API không phải GET đều bị chặn (abort) => không ghi được dữ liệu kể cả bấm nhầm.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js
const path = require('path');
const { openDev, DEV } = require('../../phieu-theo-form-quoc-gia/pw_dev.js');

const HERE = __dirname;
const OUT = path.join(HERE, 'hdsd_shots');
const IC = path.join(OUT, 'icons');
const REQ_WAIT = 'PYCHHG-04628'; // phiếu Chờ duyệt (có nút Duyệt) trên dev 28/10
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
    const btn = (text, scope = page) => scope.locator('button', { hasText: new RegExp('^\\s*' + text + '\\s*$') });
    const modal = () => page.locator('.modal.show .modal-content').last();
    const closeModal = async (text = 'Đóng|Hủy') => {
        const b = page.locator('.modal.show button').filter({ hasText: new RegExp('^\\s*(' + text + ')') });
        if (await b.count()) await b.last().click(); else await page.keyboard.press('Escape');
        await W(800);
    };
    const list = async () => {
        await page.goto(DEV + '/finance/prepick-cancel-requests');
        await page.waitForSelector('text=PYCHHG-', { timeout: 90000 });
        await page.waitForLoadState('networkidle').catch(() => {});
        await W(1500);
    };
    const row = (code) => page.locator('tbody tr', { hasText: code }).first();

    // ---- 0. Ảnh phụ cho SRS: chi tiết phiếu Đã duyệt (có link phiếu hủy) + phiếu có Lý do không duyệt
    //      (`node capture.js extra` chỉ chạy phần này)
    await page.setViewportSize({ width: 1440, height: 640 });
    for (const [id, n] of [['4627', '17_detail_approved'], ['4390', '19_reason']]) {
        await page.goto(DEV + '/finance/prepick-cancel-requests/' + id);
        await page.waitForSelector('text=PYCHHG-0' + id, { timeout: 90000 }); await page.waitForLoadState('networkidle').catch(() => {}); await W(2500);
        if (n === '19_reason') await eshot(page.locator('.card').filter({ hasText: 'Lý do không duyệt' }).last(), n);
        else await shot(n);
    }
    await page.setViewportSize({ width: 1920, height: 950 });
    if (process.argv[2] === 'extra') { console.log(log.join('\n')); await browser.close(); return; }

    // ---- 1. Danh sách + menu
    await list();
    await shot('01_list', { clip: { x: 0, y: 0, width: 1920, height: 800 } });
    await page.mouse.move(28, 400); await W(1000);
    await page.locator('a.cat', { hasText: 'Hàng hoá - Dịch vụ' }).first().click(); await W(1000);
    const grp = page.locator('a, div, li, button').filter({ hasText: /^\s*Giữ hàng\s*\d*\s*$/ }).locator('visible=true');
    await icon(grp.last(), 'menu_giuhang');
    await grp.last().click(); await W(1000);
    {   // mục menu: cắt từ biểu tượng tài liệu tới hết chữ (dòng menu rất rộng)
        const a = page.locator('a.row[data-k="/finance/prepick-cancel-requests"]').locator('visible=true').first();
        const b1 = await a.boundingBox(); const b2 = await a.locator('.row-nm').boundingBox();
        await page.screenshot({ path: path.join(IC, 'menu_muc.png'), clip: { x: b1.x, y: b1.y, width: b2.x + b2.width - b1.x + 10, height: b1.height } });
        log.push('menu_muc');
    }
    await page.screenshot({ path: out('00_menu') });
    await page.keyboard.press('Escape');
    await list();

    // ---- 2. Bộ lọc
    // Ô nhập: chỉ cắt phần đầu ô (rộng 150px, ô tìm nhanh 250px) như bộ icon màn 27.
    const clipIcon = async (loc, n, w) => {
        try { await away(); const b = await loc.first().boundingBox(); await page.screenshot({ path: path.join(IC, n + '.png'), clip: { x: b.x, y: b.y, width: Math.min(w, b.width), height: b.height } }); log.push(n); }
        catch (e) { log.push(n + ':ERR ' + e.message.split('\n')[0]); }
    };
    await clipIcon(page.locator('input[placeholder^="Tìm theo mã phiếu"]'), 'o_timnhanh', 250);
    await btn('Tìm kiếm nâng cao').first().click(); await W(1500);
    await eshot(page.locator('.smart-filter-card, section').filter({ hasText: 'Bộ lọc danh sách' }).first(), '02_filter');
    const field = (label) => page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + label + '\\s*$') }) }).locator('visible=true');
    for (const [lb, n] of [['Mã phiếu', 'o_maphieu'], ['Người duyệt', 'o_nguoiduyet'], ['Tên hàng hóa', 'o_tenhang'], ['Mã hàng hóa', 'o_mahang'], ['Trạng thái', 'o_trangthai'], ['Người tạo', 'o_nguoitao'], ['Ngày tạo', 'o_ngaytao']]) {
        await clipIcon(field(lb), n, 150);
    }
    // ---- 3. Cài đặt bộ lọc / Cấu hình cột / Xuất Excel
    await btn('Cài đặt bộ lọc').first().click(); await W(1500);
    await eshot(modal(), '26_filtercfg'); await closeModal('Đóng');
    await page.locator('button[title="Cấu hình cột hiển thị"]').first().click(); await W(1500);
    await eshot(modal(), '25_colcfg'); await closeModal('Đóng');
    await btn('Xuất Excel').first().click(); await W(1500);
    await eshot(modal(), '20_export'); await closeModal('Đóng');

    // ---- 4. Nút trên dòng phiếu Chờ duyệt
    const r1 = row(REQ_WAIT);
    await icon(r1.locator('[title="Duyệt"]').first(), 'btn_duyet_row');
    // ---- 5. Lịch sử từ danh sách
    await r1.locator('[title="Lịch sử"]').first().click(); await W(2500);
    await eshot(modal(), '16_history'); await closeModal('Đóng');
    // ---- 6. In từ danh sách
    await r1.locator('[title="In"]').first().click(); await W(4000);
    { await away(); const b = await modal().boundingBox(); await page.screenshot({ path: out('18_print'), clip: { x: b.x, y: b.y, width: b.width, height: Math.round(b.height * 0.6) } }); log.push('18_print'); } // nửa dưới tờ giấy trắng -> cắt bỏ await closeModal('Đóng'); await page.keyboard.press('Escape'); await W(500);

    // ---- 7. Bật tạm Sửa/Xóa trên trình duyệt (vá JSON danh sách, không ghi dữ liệu) để chụp nút + hộp xác nhận xóa
    await page.route('**/api/v1/finance/prepick-cancel-requests?*', async (r) => {
        const res = await r.fetch(); const j = await res.json();
        (j.data || []).forEach((x) => { if (x.code === REQ_WAIT) { x.is_can_edit = true; x.is_can_delete = true; } });
        await r.fulfill({ response: res, json: j });
    });
    await list();
    await icon(row(REQ_WAIT).locator('[title="Sửa"]').first(), 'btn_sua_row');
    await icon(row(REQ_WAIT).locator('[title="Xóa"]').first(), 'btn_xoa_row');
    await eshot(row(REQ_WAIT).locator('td').last(), 'row_actions_patched');
    await row(REQ_WAIT).locator('[title="Xóa"]').first().click(); await W(1200);
    await eshot(modal(), '13_delete');
    await icon(btn('Xóa', page.locator('.modal.show')), 'btn_confirm_xoa');
    await icon(btn('Hủy', page.locator('.modal.show')), 'btn_huy_confirm');
    await closeModal('Hủy');
    await page.unroute('**/api/v1/finance/prepick-cancel-requests?*');

    // ---- 8. Tạo mới — màn form chụp khổ 1440x640 (khổ 1920 thừa nhiều khoảng trắng)
    await page.setViewportSize({ width: 1440, height: 640 });
    await page.goto(DEV + '/finance/prepick-cancel-requests/create');
    await page.waitForLoadState('networkidle').catch(() => {}); await W(2500);
    await shot('10_create_empty');
    await page.locator('.select2-selection, .select2').first().click(); await W(1200);
    await page.locator('.select2-results__option').filter({ hasText: /\S/ }).first().click(); await W(1500);
    await icon(btn('Thêm hàng hóa').first(), 'btn_themhanghoa');
    await btn('Thêm hàng hóa').first().click(); await W(3000);
    await eshot(modal(), '11_stock');
    const ck = page.locator('.modal.show tbody tr input[type=checkbox], .modal.show tbody tr .custom-control-label, .modal.show tbody tr .v2-checkbox').first();
    await ck.click().catch((e) => log.push('tick:ERR ' + e.message.split('\n')[0])); await W(600);
    await icon(page.locator('.modal.show button').filter({ hasText: /^\s*Chọn/ }), 'btn_chon');
    await icon(btn('Đóng', page.locator('.modal.show')), 'btn_dong');
    await page.locator('.modal.show button').filter({ hasText: /^\s*Chọn/ }).first().click(); await W(1500);
    await shot('10_create');
    await icon(page.locator('button[title="Xóa dòng"]').first(), 'btn_xoadong');
    for (const [t, n] of [['Lưu nháp', 'btn_luunhap'], ['Lưu và gửi duyệt', 'btn_luuguiduyet'], ['Lưu và tiếp tục', 'btn_luutieptuc'], ['Quay lại', 'btn_quaylai']]) await icon(btn(t), n);
    await btn('Lưu và gửi duyệt').first().click(); await W(1200);
    await eshot(modal(), '10_confirm_send');
    await icon(btn('Xác nhận', page.locator('.modal.show')), 'btn_confirm_xacnhan');
    await closeModal('Hủy');

    // ---- 9. Chi tiết phiếu Chờ duyệt
    const reqId = REQ_WAIT.replace(/\D/g, '').replace(/^0+/, '');
    await page.goto(DEV + '/finance/prepick-cancel-requests/' + reqId);
    await page.waitForSelector('text=' + REQ_WAIT, { timeout: 90000 }); await page.waitForLoadState('networkidle').catch(() => {}); await W(2000);
    await shot('17_detail');
    await icon(btn('Tạo phiếu hủy hàng giữ'), 'btn_taophieuhuy');
    await icon(btn('Không duyệt'), 'btn_khongduyet');
    await icon(btn('In'), 'btn_in');
    await icon(btn('Xem lịch sử'), 'btn_xemlichsu');
    await btn('Xem lịch sử').first().click(); await W(2000);
    await eshot(page.locator('.card').filter({ hasText: 'Lịch sử thay đổi' }).last(), '16_history_detail');
    await btn('Không duyệt').first().click(); await W(1200);
    await eshot(modal(), '15_reject');
    await icon(btn('Xác nhận không duyệt', page.locator('.modal.show')), 'btn_confirm_khongduyet');
    await icon(btn('Đóng', page.locator('.modal.show')), 'btn_dong_reject');
    await closeModal('Đóng');

    // ---- 10. Màn Sửa (mở để chụp, không lưu)
    await page.goto(DEV + '/finance/prepick-cancel-requests/' + reqId + '/edit');
    await page.waitForLoadState('networkidle').catch(() => {}); await W(3500);
    await shot('12_edit');

    // ---- 11. Tạo phiếu hủy hàng giữ (duyệt) — mở màn lập phiếu hủy, KHÔNG lưu
    await page.goto(DEV + '/finance/prepick-cancel-requests/' + reqId);
    await page.waitForSelector('text=' + REQ_WAIT, { timeout: 90000 }); await W(2000);
    await btn('Tạo phiếu hủy hàng giữ').first().click();
    await page.waitForURL(/prepick-cancels\/create/, { timeout: 60000 }); await page.waitForLoadState('networkidle').catch(() => {}); await W(3000);
    await shot('14_approve');
    await icon(btn('Duyệt'), 'btn_duyet');
    await btn('Duyệt').first().click(); await W(1500);
    await eshot(modal(), '14_approve_confirm');
    await icon(btn('Duyệt', page.locator('.modal.show')), 'btn_confirm_duyet');
    await closeModal('Hủy');

    console.log(log.join('\n'));
    await browser.close();
})().catch((e) => { console.error(e); console.log(log.join('\n')); process.exit(1); });

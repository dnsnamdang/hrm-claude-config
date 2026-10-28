// Chụp ảnh HDSD + SRS màn Phiếu đề nghị thanh toán trên DEV (dev-hrm.eteksofts.com).
// AN TOÀN: không bấm xác nhận Lưu / Duyệt / Từ chối / Xóa — mở hộp thoại, chụp, rồi Hủy / Đóng.
// Nút Sửa / Xóa (tài khoản dev không có phiếu nào của mình) bật TẠM bằng cách sửa JSON trả về
// trên trình duyệt (page.route) — không ghi dữ liệu.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [tên bước ...]
const path = require('path');
const { open, go } = require('./devlib');

const SHOTS = path.join(__dirname, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
const APPROVE_ID = 5174; // Chờ kế toán trưởng duyệt — có Duyệt + Chuyển duyệt BGĐ + Từ chối
const ONLY = process.argv.slice(2);

const shot = async (page, name, opt = {}) => {
    if (opt.fullPage) {
        await page.setViewportSize({ width: 1440, height: opt.h || 1300 }); await page.waitForTimeout(1200);
        await page.mouse.move(700, 8);
        await page.screenshot({ path: path.join(SHOTS, name + '.png') });
        await page.setViewportSize({ width: 1440, height: 900 }); await page.waitForTimeout(500);
        return;
    }
    await page.screenshot({ path: path.join(SHOTS, name + '.png'), ...opt });
};
const icon = async (loc, name) => {
    await loc.first().scrollIntoViewIfNeeded().catch(() => {});
    await loc.first().screenshot({ path: path.join(ICONS, name + '.png') });
};
const away = async (page) => { await page.mouse.move(700, 8); await page.waitForTimeout(500); };
const ff = (page, label) => page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^' + label + '$') }) });

async function closeModal(page) {
    const btn = page.locator('.modal.show').last().locator('button', { hasText: /^\s*(Đóng|Hủy)\s*$/ });
    if (await btn.count()) await btn.last().click();
    else await page.keyboard.press('Escape');
    await page.waitForTimeout(800);
}

const steps = {
    async menu(page) {
        await go(page, '/finance/bill-payment-requests');
        await page.mouse.move(40, 300); await page.waitForTimeout(1000);
        await page.screenshot({ path: path.join(ICONS, 'menu_phanhe.png'), clip: { x: 0, y: 0, width: 200, height: 58 } });
        const cat = (t) => page.locator('a.cat', { hasText: t }).first();
        await icon(cat('Khởi tạo'), 'menu_khoitao');
        await cat('Khởi tạo').click(); await page.waitForTimeout(1200);
        await icon(page.getByText('Khởi tạo phiếu yêu c', { exact: false }).first().locator('xpath=ancestor::*[self::a or self::button or self::li or self::div][1]'), 'menu_nhom');
        await icon(page.getByText('Đề nghị thanh toán', { exact: true }).first().locator('xpath=..'), 'menu_muc');
        await shot(page, '00_menu');
        await page.mouse.move(40, 300); await page.waitForTimeout(600);
        await icon(cat('Quản lý tiền'), 'menu_quanlytien');
        await cat('Quản lý tiền').click(); await page.waitForTimeout(1200);
        await icon(page.locator('button, a, li, div').filter({ hasText: /^\s*Đề nghị\s*\d*\s*$/ }).last(), 'menu_nhom_qlt');
        await page.mouse.move(40, 300); await page.waitForTimeout(600);
        await icon(cat('Chờ duyệt'), 'menu_choduyet');
        await cat('Chờ duyệt').click(); await page.waitForTimeout(1200);
        await icon(page.getByText('Phê duyệt - Công nợ', { exact: false }).first().locator('xpath=ancestor::*[self::a or self::button or self::li or self::div][1]'), 'menu_nhom_cd');
        await icon(page.getByText('Phiếu đề nghị thanh toán chờ duyệt', { exact: true }).first().locator('xpath=..'), 'menu_muc_cd');
    },
    async list(page) {
        await go(page, '/finance/bill-payment-requests'); await away(page);
        await shot(page, '01_list');
        await icon(page.locator('input[placeholder="Tìm theo mã phiếu..."]').locator('xpath=..'), 'o_timnhanh');
        await icon(page.locator('button', { hasText: 'Tìm kiếm nâng cao' }), 'btn_timkiemnangcao');
        await icon(page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(page.locator('button', { hasText: 'Làm mới' }), 'btn_lammoi');
        await icon(page.locator('button', { hasText: 'Cài đặt bộ lọc' }), 'btn_caidatboloc');
        await icon(page.locator('button', { hasText: 'Tạo mới' }), 'btn_taomoi');
        await icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        await page.locator('button', { hasText: 'Tìm kiếm nâng cao' }).first().click(); await page.waitForTimeout(1500); await away(page);
        await shot(page, '02_filter');
        const F = [['Công ty', 'o_congty'], ['Phòng ban', 'o_phongban'], ['Loại chi', 'o_loaichi'],
            ['Hình thức thanh toán', 'o_hinhthuc'], ['Trạng thái', 'o_trangthai'], ['Lý do chi', 'o_lydochi'],
            ['Khách hàng', 'o_khachhang'], ['Nhà cung cấp', 'o_ncc'], ['Người lập', 'o_nguoilap'],
            ['Số tiền đề nghị', 'o_sotien'], ['Ngày lập', 'o_ngaylap']];
        for (const [lb, nm] of F) await icon(ff(page, lb), nm);
    },
    async pending(page) {
        await go(page, '/finance/bill-payment-requests?mode=pending'); await away(page);
        await shot(page, '03_pending');
        const rowA = page.locator('tbody tr').filter({ has: page.locator('span[title="Duyệt"]') }).first();
        await icon(rowA.locator('span[title="Duyệt"] > *'), 'btn_duyet_row');
        const rowU = page.locator('tbody tr').filter({ has: page.locator('span[title="Tạo ủy nhiệm chi"]') }).first();
        if (await rowU.count()) await icon(rowU.locator('span[title="Tạo ủy nhiệm chi"] > *'), 'btn_taounc_row');
        const rowC = page.locator('tbody tr').filter({ has: page.locator('span[title="Tạo phiếu chi"]') }).first();
        if (await rowC.count()) await icon(rowC.locator('span[title="Tạo phiếu chi"] > *'), 'btn_taophieuchi_row');
    },
    async rowmenu(page) {
        // Bật tạm Sửa / Xóa cho 1 dòng (chỉ trên trình duyệt) để chụp nút + hộp xác nhận xóa.
        await page.route(/\/api\/v1\/finance\/bill-payment-requests\?/, async (route) => {
            const res = await route.fetch(); const j = await res.json();
            if (j.data && j.data[1]) { j.data[1].is_can_edit = true; j.data[1].is_can_delete = true; }
            await route.fulfill({ response: res, json: j });
        });
        await go(page, '/finance/bill-payment-requests'); await away(page);
        const row = page.locator('tbody tr').nth(1);
        await icon(row.locator('span[title="Sửa"] > *'), 'btn_sua_row');
        await icon(row.locator('span[title="In phiếu"] > *'), 'btn_in_row');
        const more = row.locator('.v2-row-actions button').last();
        await icon(more, 'btn_bacham_row');
        await more.click(); await page.waitForTimeout(800);
        if (!(await page.locator('.v2-row-actions__menu:visible').count())) { await more.click(); await page.waitForTimeout(800); }
        console.log('menu count', await page.locator('.v2-row-actions__menu').count());
        const menu = page.locator('.v2-row-actions__menu:visible').first();
        const it = async (t, n) => {
            const b = await menu.locator(`button[title="${t}"]`).boundingBox();
            await page.screenshot({ path: path.join(ICONS, n + '.png'), clip: b });
        };
        await it('Xuất Excel', 'item_xuatexcel');
        await it('Lịch sử', 'item_lichsu');
        await it('Xóa', 'item_xoa');
        await shot(page, '22_export');
        await menu.locator('button[title="Xóa"]').click(); await page.waitForTimeout(1000);
        await shot(page, '15_delete');
        await closeModal(page);
        await page.unroute(/\/api\/v1\/finance\/bill-payment-requests\?/);
    },
    async rowplain(page) {
        await go(page, '/finance/bill-payment-requests'); await away(page);
        const row = page.locator('tbody tr').filter({ hasNot: page.locator('span[title="Duyệt"]') }).first();
        await icon(row.locator('span[title="Xuất Excel"] > *'), 'btn_xuatexcel_row');
        await icon(row.locator('span[title="Lịch sử"] > *'), 'btn_lichsu_row');
        await row.locator('span[title="Lịch sử"] > *').click(); await page.waitForTimeout(3000); await away(page);
        await shot(page, '20_history_row');
        await closeModal(page);
    },
    async create(page) {
        await go(page, '/finance/bill-payment-requests/create'); await away(page);
        await shot(page, '10_create');
        for (const [t, n] of [['Lưu nháp', 'btn_luunhap'], ['Lưu và gửi duyệt', 'btn_luuguiduyet'], ['Lưu và tiếp tục', 'btn_luutieptuc'], ['Quay lại', 'btn_quaylai']])
            await icon(page.locator('button', { hasText: t }), n);
        const add = page.locator('a[title="Thêm dòng"]');
        if (await add.count()) await icon(add.locator('xpath=..'), 'btn_themdong');
        await icon(page.locator('button', { hasText: 'Thêm tài liệu' }), 'btn_themtailieu');
        await add.first().click(); await page.waitForTimeout(600);
        const xoa = page.locator('a[title="Xóa dòng"]');
        if (await xoa.count()) await icon(xoa.locator('xpath=..'), 'btn_xoadong');
        // Ô nhà cung cấp của dòng → cửa sổ Chọn nhà cung cấp
        await page.locator('input[placeholder*="Nhấn vào đây để chọn"]').first().click(); await page.waitForTimeout(3000);
        await shot(page, '11_supplier');
        const firstRow = page.locator('.modal.show tbody tr').first();
        await firstRow.click(); await page.waitForTimeout(1500);
        // Ô hợp đồng của dòng → cửa sổ chọn hợp đồng
        await page.locator('tbody input[placeholder*="hợp đồng"], tbody input[placeholder*="Hợp đồng"]').first().click().catch(() => {});
        await page.waitForTimeout(3000);
        if (await page.locator('.modal.show').count()) { await shot(page, '12_contract'); await closeModal(page); }
        await page.locator('button', { hasText: 'Thêm tài liệu' }).first().click(); await page.waitForTimeout(800);
        await icon(page.locator('button, label', { hasText: 'Chọn tệp' }), 'btn_chontep');
        await shot(page, '10b_create_filled');
    },
    async createck(page) {
        await go(page, '/finance/bill-payment-requests/create'); await away(page);
        const sel = async (label, text) => {
            const box = page.locator('.form-row > div').filter({ has: page.locator('label', { hasText: label }) }).first();
            await box.locator('.select2-selection').click(); await page.waitForTimeout(500);
            await page.locator('.select2-results__option', { hasText: text }).first().click(); await page.waitForTimeout(1200);
        };
        await sel('Hình thức thanh toán', 'CK');
        await away(page);
        await shot(page, '13_create_ck');
        await sel('Loại chi', 'vận chuyển');
        if (await page.locator('.modal.show').count()) { await page.locator('.modal.show button', { hasText: 'Xác nhận' }).click(); await page.waitForTimeout(1000); }
        await sel('Hình thức thanh toán', 'TM');
        await away(page);
        await icon(page.locator('button', { hasText: 'Lấy dữ liệu' }), 'btn_laydulieu');
        await shot(page, '14_delivery');
    },
    async edit(page) {
        await go(page, '/finance/bill-payment-requests/' + APPROVE_ID + '/edit'); await away(page);
        await page.waitForTimeout(7000); await away(page);
        await shot(page, '16_edit');
    },
    async detail(page) {
        await go(page, '/finance/bill-payment-requests/' + APPROVE_ID); await page.waitForTimeout(2500); await away(page);
        await shot(page, '17_detail', { fullPage: true });
        await shot(page, '17b_detail_view');
        const ft = (t) => page.locator('button', { hasText: new RegExp('^\\s*' + t + '\\s*$') });
        await icon(ft('Chuyển duyệt BGĐ'), 'btn_chuyenduyet');
        await ft('In').first().click(); await page.waitForTimeout(5000); await away(page);
        await shot(page, '21_print');
        await icon(page.locator('.modal.show button', { hasText: /^\s*In\s*$/ }), 'btn_in_preview');
        await closeModal(page);
        await icon(ft('In'), 'btn_in');
        await icon(ft('Xuất Excel'), 'btn_xuatexcel_ct');
        const xl = page.locator('button', { hasText: 'Xem lịch sử' });
        if (await xl.count()) await icon(xl, 'btn_xemlichsu');
        // Duyệt → hộp xác nhận → Hủy
        await ft('Duyệt').first().click(); await page.waitForTimeout(1200);
        await shot(page, '18_approve');
        await icon(page.locator('.modal.show button', { hasText: /^\s*Duyệt\s*$/ }), 'btn_confirm_duyet');
        await closeModal(page);
        await ft('Chuyển duyệt BGĐ').first().click(); await page.waitForTimeout(1200);
        await shot(page, '18b_forward');
        await icon(page.locator('.modal.show button', { hasText: /^\s*Chuyển duyệt\s*$/ }), 'btn_confirm_chuyenduyet');
        await closeModal(page);
        // Từ chối → cửa sổ → Đóng
        await ft('Từ chối').first().click(); await page.waitForTimeout(1200);
        await shot(page, '19_reject');
        await closeModal(page);
        // Khối lịch sử ở cuối màn chi tiết
        if (await xl.count()) {
            await xl.first().click(); await page.waitForTimeout(3000); await away(page);
            await xl.first().locator('xpath=ancestor::div[contains(@class,"card")][1]').screenshot({ path: path.join(SHOTS, '20_history.png') }).catch(() => shot(page, '20_history'));
        }
    },
    async dialogs(page) {
        // Hộp xác nhận đổi Loại chi / gửi duyệt / chưa lưu — chỉ mở rồi Hủy, không lưu gì.
        await go(page, '/finance/bill-payment-requests/create'); await away(page);
        await page.locator('a[title="Thêm dòng"]').first().click(); await page.waitForTimeout(600);
        const box = page.locator('.form-row > div').filter({ has: page.locator('label', { hasText: 'Loại chi' }) }).first();
        await box.locator('.select2-selection').click(); await page.waitForTimeout(500);
        await page.locator('.select2-results__option', { hasText: 'Chi trả lại khách hàng' }).first().click(); await page.waitForTimeout(1200);
        await away(page); await shot(page, '30_changetype');
        await closeModal(page);
        await page.locator('button', { hasText: 'Lưu và gửi duyệt' }).first().click(); await page.waitForTimeout(1200);
        await away(page); await shot(page, '31_confirm_send');
        await closeModal(page);
        await page.locator('input[placeholder="Nhập lý do chi"]').fill('Thử'); await page.waitForTimeout(400);
        await page.locator('button', { hasText: 'Quay lại' }).first().click(); await page.waitForTimeout(1200);
        await away(page); await shot(page, '32_unsaved');
        const stay = page.locator('.modal.show button', { hasText: 'Ở lại' });
        if (await stay.count()) await stay.first().click(); else await page.keyboard.press('Escape');
        await page.waitForTimeout(600);
    },
    async paybtn(page) {
        // Nút Tạo phiếu chi (phiếu TM) / Tạo ủy nhiệm chi (phiếu CK) ở màn chi tiết phiếu Chờ tạo phiếu chi — chỉ chụp nút.
        for (const [id, t, n] of [[5193, 'Tạo phiếu chi', 'btn_taophieuchi'], [5235, 'Tạo ủy nhiệm chi', 'btn_taounc']]) {
            await go(page, '/finance/bill-payment-requests/' + id); await page.waitForTimeout(2000); await away(page);
            await icon(page.locator('button', { hasText: new RegExp('^\\s*' + t + '\\s*$') }), n);
            if (n === 'btn_taounc') await shot(page, '23_waitpay');
        }
    },
    async config(page) {
        await go(page, '/finance/bill-payment-requests'); await away(page);
        await page.locator('button', { hasText: 'Cài đặt bộ lọc' }).first().click(); await page.waitForTimeout(1500);
        await shot(page, '26_filtercfg');
        await closeModal(page);
        await page.locator('button[title="Cấu hình cột hiển thị"]').first().click(); await page.waitForTimeout(1500);
        await shot(page, '25_colcfg');
        await closeModal(page);
    },
};

(async () => {
    const { browser, page } = await open();
    for (const [k, fn] of Object.entries(steps)) {
        if (ONLY.length && !ONLY.includes(k)) continue;
        try { await fn(page); console.log('OK', k); } catch (e) { console.log('FAIL', k, String(e.message).split('\n')[0]); }
    }
    await browser.close();
})().catch(e => { console.error(e); process.exit(1); });

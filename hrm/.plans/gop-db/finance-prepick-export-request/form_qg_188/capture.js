// Chụp ảnh HDSD/SRS màn Phiếu xuất giữ (STT 188) trên DEV — KHÔNG bấm xác nhận Lưu/Duyệt/Từ chối/Xóa.
// Nút Sửa/Xóa/Duyệt mà tài khoản không có phiếu đủ điều kiện -> chỉ bật tạm cờ trong JSON trả về TRÊN TRÌNH
// DUYỆT (page.route), không ghi dữ liệu.
// Chạy: node capture.js   (node v24 — xem BRIEF_AGENT.md)
const fs = require('fs');
const path = require('path');
const { openDev, DEV } = require('d:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/phieu-theo-form-quoc-gia/pw_dev.js');

const OUT = path.join(__dirname, 'hdsd_shots');
const IC = path.join(OUT, 'icons');
const LIST = '/finance/warehouse-prepick-requests';
const ID_REQ = 2739; // YCXG Chờ KT duyệt — mở màn lập phiếu (không lưu)
const ID_PXG = 2744; // PXG Đã duyệt, có lịch sử
const MOUSE = [1436, 150];

let mock = { list: false, edit: null, approve: null };

function patchDetail(j) {
    const d = j && j.data && j.data.id ? j.data : j;
    return d;
}

(async () => {
    fs.mkdirSync(IC, { recursive: true });
    const { browser, page } = await openDev(__dirname, { scale: 2 });

    await page.route(/\/api\/v1\/finance\/warehouse-prepick-requests(\?|\/\d+(\?|$))/, async (route) => {
        const url = route.request().url();
        if (route.request().method() !== 'GET') return route.continue();
        const res = await route.fetch();
        let j;
        try { j = await res.json(); } catch (e) { return route.fulfill({ response: res }); }
        const m = url.match(/warehouse-prepick-requests\/(\d+)/);
        if (!m && mock.list && Array.isArray(j.data) && j.data[0]) {
            Object.assign(j.data[0], { is_can_edit: true, is_can_delete: true });
        }
        if (m && mock.edit && Number(m[1]) === mock.edit) {
            Object.assign(patchDetail(j), { is_can_edit: true, is_can_delete: true, status: 3, status_name: 'Đang tạo', status_color: '#64748B' });
        }
        if (m && mock.approve && Number(m[1]) === mock.approve) {
            Object.assign(patchDetail(j), { is_can_approve: true, is_can_reject: true });
        }
        return route.fulfill({ response: res, json: j });
    });

    const settle = async (ms = 2500) => {
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(ms);
        await page.mouse.move(...MOUSE);
        await page.waitForTimeout(300);
    };
    const go = async (url, ms) => { await page.setViewportSize({ width: 1440, height: 900 }); await page.goto(DEV + url); await settle(ms); };
    const shot = async (name) => { await page.mouse.move(...MOUSE); await page.waitForTimeout(400); await page.screenshot({ path: path.join(OUT, name + '.png') }); console.log('shot', name); };
    // Màn dài: nới chiều cao khung nhìn cho thấy đủ nội dung (thanh nút cố định đáy vẫn nằm đáy).
    const shotTall = async (name, max = 1700) => {
        const h = await page.evaluate(() => document.documentElement.scrollHeight);
        await page.setViewportSize({ width: 1440, height: Math.min(Math.max(900, h + 40), max) });
        await page.waitForTimeout(800);
        await shot(name);
        await page.setViewportSize({ width: 1440, height: 900 });
    };
    const icon = async (loc, name) => {
        try {
            await loc.first().scrollIntoViewIfNeeded();
            await loc.first().screenshot({ path: path.join(IC, name + '.png') });
            console.log('icon', name);
        } catch (e) { console.log('MISS icon', name, e.message.split('\n')[0]); }
    };
    const btn = (txt) => page.locator('button, a', { hasText: txt }).filter({ visible: true });
    const ff = (label) => page.locator('.ff', { has: page.locator('.ff__text', { hasText: new RegExp('^' + label + '$') }) });
    const modal = () => page.locator('.modal.show .modal-content').last();
    const closeModalBtn = async (txt) => { await modal().locator('button', { hasText: txt }).last().click(); await page.waitForTimeout(800); };

    const PART = process.argv[2] || 'all';
    const foot = (txt) => page.locator('.footer button', { hasText: new RegExp('^\\s*' + txt + '\\s*$') });
    const top = async () => { await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(400); };
    const shotH = async (name, h) => { await page.setViewportSize({ width: 1440, height: h }); await page.waitForTimeout(800); await shot(name); await page.setViewportSize({ width: 1440, height: 900 }); };
    const rowOf = (code) => page.locator('table tbody tr', { hasText: code }).first();

    if (PART === 'all' || PART === 'p1') {
        await go(LIST);
        await page.locator('a.cat', { hasText: 'Hàng hoá - Dịch vụ' }).click(); await page.waitForTimeout(1200);
        await icon(page.locator('a.scat', { hasText: 'Giữ hàng' }), 'menu_giuhang');
        await page.locator('a.scat', { hasText: 'Giữ hàng' }).click(); await page.waitForTimeout(1200);
        await icon(page.locator('.navwrap').getByText('Phiếu xuất giữ', { exact: true }), 'menu_muc');

        await go(LIST);
        await shot('01_list');
        await icon(page.locator('input[placeholder*="Tìm theo"]').first(), 'o_timnhanh');
        await icon(btn('Lập từ yêu cầu'), 'btn_laptuyc');
        await icon(rowOf('PXG-0' + ID_PXG).locator('.v2-row-actions > span').nth(0), 'btn_in_row');
        await icon(rowOf('PXG-0' + ID_PXG).locator('.v2-row-actions > span').nth(1), 'btn_lichsu_row');
        await btn('Tìm kiếm nâng cao').first().click(); await settle(1500);
        await shot('02_filter');
        for (const [lb, nm] of [['Mã phiếu', 'o_maphieu'], ['Yêu cầu xuất giữ', 'o_yeucau'], ['Người yêu cầu', 'o_nguoiyeucau'],
            ['Người duyệt', 'o_nguoiduyet'], ['Khách hàng', 'o_khachhang'], ['Tên, mã hàng', 'o_tenmahang']]) {
            await icon(ff(lb), nm);
        }

        mock.list = true;
        await go(LIST);
        const row0 = page.locator('table tbody tr').first();
        await icon(row0.locator('.v2-row-actions > span').nth(0), 'btn_sua_row');
        await icon(row0.locator('.v2-row-actions > span').nth(1), 'btn_xoa_row');
        await icon(row0.locator('.v2-row-actions > span').nth(2), 'btn_bacham_row');
        await row0.locator('.v2-row-actions > span').nth(2).locator('button').click(); await page.waitForTimeout(600);
        await icon(page.locator('.v2-row-actions__menu:visible .v2-row-actions__item', { hasText: 'In' }), 'item_in');
        await icon(page.locator('.v2-row-actions__menu:visible .v2-row-actions__item', { hasText: 'Lịch sử' }), 'item_lichsu');
        await page.mouse.click(...MOUSE); await page.waitForTimeout(400);
        await row0.locator('.v2-row-actions > span').nth(1).locator('button').click(); await page.waitForTimeout(1200);
        await shot('13_delete');
        await closeModalBtn('Hủy');
        mock.list = false;

        await go(LIST);
        await btn('In').filter({ hasText: /^\s*In\s*$/ }).first().click(); await settle(3500);
        await shot('19_printlist');
        await page.keyboard.press('Escape'); await page.waitForTimeout(800);
        await go(LIST);
        await btn('Xuất Excel').first().click(); await page.waitForTimeout(1500);
        await shot('20_export');
        await closeModalBtn('Đóng');
        await page.locator('[title="Cấu hình cột hiển thị"]').first().click(); await page.waitForTimeout(1500);
        await shot('25_colcfg');
        await closeModalBtn('Đóng');
        await btn('Cài đặt bộ lọc').first().click(); await page.waitForTimeout(1500);
        await shot('26_filtercfg');
        await closeModalBtn('Đóng');
    }

    if (PART === 'all' || PART === 'p2') {
        // Màn lập phiếu từ yêu cầu Chờ KT duyệt — CHỈ mở xem, không lưu
        await go(LIST + '/create?product_prepick_request_id=' + ID_REQ, 4500);
        await shotH('10_create', 1150);
        await icon(foot('Lưu nháp'), 'btn_luunhap');
        await icon(foot('Duyệt giữ hàng'), 'btn_duyetgiuhang');
        await icon(foot('Không duyệt'), 'btn_khongduyet');
        await icon(btn('Quay lại'), 'btn_quaylai');
        await icon(page.locator('table tbody tr input[type=checkbox], table tbody tr .custom-checkbox').first(), 'o_tick');
        await top();
        await foot('Duyệt giữ hàng').click(); await page.waitForTimeout(1200);
        await shot('11_approve');
        await icon(modal().locator('.modal-footer button', { hasText: 'Duyệt giữ hàng' }), 'btn_confirm_duyetgiuhang');
        await icon(modal().locator('.modal-footer button', { hasText: 'Hủy' }), 'btn_huy_confirm');
        await closeModalBtn('Hủy');
    }

    if (PART === 'all' || PART === 'p3') {
        await go(LIST + '/' + ID_PXG, 3500);
        await shotTall('17_detail');
        await icon(foot('In'), 'btn_in');
        await icon(btn('Xem lịch sử'), 'btn_xemlichsu');
        await top();
        await foot('In').click(); await settle(3500);
        await shot('18_print');
        await page.keyboard.press('Escape'); await page.waitForTimeout(800);

        await go(LIST);
        await rowOf('PXG-0' + ID_PXG).locator('.v2-row-actions > span').nth(1).locator('button').click(); await settle(2500);
        await shot('16_history');
        await icon(modal().locator('button', { hasText: 'Bộ lọc' }), 'btn_boloc_ls');
        await icon(modal().locator('.modal-footer button', { hasText: 'Đóng' }), 'btn_dong_ls');
        await closeModalBtn('Đóng');

        mock.edit = ID_PXG;
        await go(LIST + '/' + ID_PXG, 3500);
        await icon(foot('Sửa'), 'btn_sua');
        await icon(foot('Xóa'), 'btn_xoa');
        await go(LIST + '/' + ID_PXG + '/edit', 4000);
        await shotH('12_edit', 1150);
        mock.edit = null;
    }

    if (PART === 'all' || PART === 'p4') {
        // Icon dùng chung (chụp lại trên chính màn này cho đồng bộ cỡ chữ)
        await go(LIST);
        await icon(page.locator('a.logo .subsystem-name').first(), 'menu_phanhe');
        await icon(page.locator('a.cat', { hasText: 'Hàng hoá - Dịch vụ' }), 'menu_nhom');
        await icon(btn('Tìm kiếm').filter({ hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(btn('Làm mới'), 'btn_lammoi');
        await icon(btn('Cài đặt bộ lọc'), 'btn_caidatboloc');
        await icon(btn('Xuất Excel'), 'btn_xuatexcel');
        await icon(page.locator('[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        await btn('Tìm kiếm nâng cao').first().click(); await settle(1500);
        for (const [lb, nm] of [['Công ty', 'o_congty'], ['Phòng ban', 'o_phongban'], ['Trạng thái', 'o_trangthai'],
            ['Người tạo', 'o_nguoitao'], ['Ngày tạo', 'o_ngaytao']]) await icon(ff(lb), nm);
        await btn('Xuất Excel').first().click(); await page.waitForTimeout(1500);
        await icon(modal().locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await icon(modal().locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        await icon(modal().locator('button', { hasText: 'Xuất file' }), 'btn_xuatfile');
        await icon(modal().locator('.modal-footer button', { hasText: 'Đóng' }), 'btn_dong_export');
        await closeModalBtn('Đóng');
        await page.locator('[title="Cấu hình cột hiển thị"]').first().click(); await page.waitForTimeout(1500);
        await icon(modal().locator('.modal-footer button', { hasText: 'Lưu' }), 'btn_luu_col');
        await icon(modal().locator('.modal-footer button', { hasText: 'Đóng' }), 'btn_dong_col');
        await closeModalBtn('Đóng');
        await btn('Cài đặt bộ lọc').first().click(); await page.waitForTimeout(1500);
        await icon(modal().locator('button', { hasText: /^\s*Lưu\s*$/ }), 'btn_luu');
        await icon(modal().locator('button', { hasText: 'Khôi phục mặc định' }), 'btn_khoiphuc');
        await icon(modal().locator('button', { hasText: 'Đóng' }), 'btn_dong_filtercfg');
        await closeModalBtn('Đóng');
        await btn('In').filter({ hasText: /^\s*In\s*$/ }).first().click(); await settle(3500);
        await icon(modal().locator('button', { hasText: /^\s*In\s*$/ }), 'btn_in_preview');
        await page.keyboard.press('Escape'); await page.waitForTimeout(800);
    }

    if (PART === 'p5') {
        await go(LIST);
        await btn('Tìm kiếm nâng cao').first().click(); await settle(1500);
        await shot('02_filter');
    }

    await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });

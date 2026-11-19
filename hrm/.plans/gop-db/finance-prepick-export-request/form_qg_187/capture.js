// Chụp ảnh HDSD/SRS màn Yêu cầu xuất giữ (STT 187) trên DEV — KHÔNG bấm xác nhận Lưu/Duyệt/Từ chối/Xóa.
// Nút Sửa/Xóa/Duyệt mà tài khoản không có phiếu đủ điều kiện -> chỉ bật tạm cờ trong JSON trả về TRÊN TRÌNH
// DUYỆT (page.route), không ghi dữ liệu.
// Chạy: node capture.js   (node v24 — xem BRIEF_AGENT.md)
const fs = require('fs');
const path = require('path');
const { openDev, DEV } = require('d:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/phieu-theo-form-quoc-gia/pw_dev.js');

const OUT = path.join(__dirname, 'hdsd_shots');
const IC = path.join(OUT, 'icons');
const LIST = '/finance/product-prepick-requests';
const ID_KT = 2739; // Chờ KT duyệt, loại Xuất giữ khác — nút Lập phiếu xuất giữ + Từ chối (cờ thật)
const ID_BGD = 2737; // Chờ BGĐ duyệt
const ID_HD = 2717; // Chờ KT duyệt, loại Xuất giữ HĐ hãng
const MOUSE = [1436, 150];

let mock = { list: false, edit: null, approve: null };

function patchDetail(j) {
    const d = j && j.data && j.data.id ? j.data : j;
    return d;
}

(async () => {
    fs.mkdirSync(IC, { recursive: true });
    const { browser, page } = await openDev(__dirname, { scale: 2 });

    await page.route(/\/api\/v1\/finance\/product-prepick-requests(\?|\/\d+(\?|$))/, async (route) => {
        const url = route.request().url();
        if (route.request().method() !== 'GET') return route.continue();
        const res = await route.fetch();
        let j;
        try { j = await res.json(); } catch (e) { return route.fulfill({ response: res }); }
        const m = url.match(/product-prepick-requests\/(\d+)/);
        if (!m && mock.list && Array.isArray(j.data) && j.data[0]) {
            Object.assign(j.data[0], { is_can_edit: true, is_can_delete: true });
        }
        if (m && mock.edit && Number(m[1]) === mock.edit) {
            Object.assign(patchDetail(j), { is_can_edit: true, is_can_delete: true, status: 3, status_name: 'Đang tạo', status_color: '#64748B', is_can_create_export: false, is_can_reject: false });
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
    if (PART === 'all' || PART === 'p1') {
    // ---------------- Menu
    await go(LIST);
    await page.locator('a.cat', { hasText: 'Hàng hoá - Dịch vụ' }).click(); await page.waitForTimeout(1200);
    await icon(page.locator('a.scat', { hasText: 'Giữ hàng' }), 'menu_giuhang');
    await page.locator('a.scat', { hasText: 'Giữ hàng' }).click(); await page.waitForTimeout(1200);
    await icon(page.locator('.navwrap a', { hasText: /^\s*Yêu cầu xuất giữ\s*$/ }), 'menu_muc');
    await page.keyboard.press('Escape');

    // ---------------- Danh sách + bộ lọc
    await go(LIST);
    await shot('01_list');
    await icon(page.locator('.v2-smart-filter input[type=text], input[placeholder*="Tìm theo"]').first(), 'o_timnhanh');
    await icon(btn('Tạo mới'), 'btn_taomoi');
    await icon(btn('Tìm kiếm nâng cao'), 'btn_timkiemnangcao');
    await btn('Tìm kiếm nâng cao').first().click(); await settle(1500);
    await shot('02_filter');
    for (const [lb, nm] of [['Mã phiếu', 'o_maphieu'], ['Loại yêu cầu', 'o_loaiyc'], ['Người duyệt', 'o_nguoiduyet'],
        ['Khách hàng', 'o_khachhang'], ['Tên, mã hàng', 'o_tenmahang'], ['Số hợp đồng', 'o_sohopdong']]) {
        await icon(ff(lb), nm);
    }

    // Icon dòng (bật tạm cờ Sửa/Xóa cho dòng đầu) + hộp xác nhận xóa
    mock.list = true;
    await go(LIST);
    const row0 = page.locator('table tbody tr').first();
    await icon(row0.locator('.v2-row-actions > span').nth(0), 'btn_sua_row');
    await icon(row0.locator('.v2-row-actions > span').nth(1), 'btn_xoa_row');
    await icon(row0.locator('.v2-row-actions > span').nth(2), 'btn_bacham_row');
    await row0.locator('.v2-row-actions > span').nth(2).locator('button').click(); await page.waitForTimeout(600);
    await icon(page.locator('.v2-row-actions__menu:visible .v2-row-actions__item', { hasText: 'In' }), 'item_in');
    await icon(page.locator('.v2-row-actions__menu:visible .v2-row-actions__item', { hasText: 'Lịch sử' }), 'item_lichsu');
    await page.keyboard.press('Escape'); await page.mouse.click(...MOUSE); await page.waitForTimeout(400);
    await row0.locator('.v2-row-actions > span').nth(1).locator('button').click(); await page.waitForTimeout(1200);
    await shot('13_delete');
    await icon(modal().locator('button', { hasText: 'Xóa' }), 'btn_confirm_xoa');
    await icon(modal().locator('button', { hasText: 'Hủy' }), 'btn_huy_confirm');
    await closeModalBtn('Hủy');
    mock.list = false;

    // Dòng Chờ KT duyệt: icon Lập phiếu xuất giữ / In / Lịch sử (cờ thật)
    await go(LIST + '?status=2');
    const rowKT = page.locator('table tbody tr', { hasText: 'PYCXG-0' + ID_KT }).first();
    if (await rowKT.count()) {
        await icon(rowKT.locator('.v2-row-actions > span').nth(0), 'btn_lapxg_row');
        await icon(rowKT.locator('.v2-row-actions > span').nth(1), 'btn_in_row');
        await icon(rowKT.locator('.v2-row-actions > span').nth(2), 'btn_lichsu_row');
    } else console.log('MISS row KT');

    // In danh sách + In phiếu
    await go(LIST);
    await icon(btn('In').filter({ hasText: /^\s*In\s*$/ }), 'btn_in_list');
    await btn('In').filter({ hasText: /^\s*In\s*$/ }).first().click(); await settle(3500);
    await shot('19_printlist');
    await icon(modal().locator('button', { hasText: /^\s*In\s*$/ }), 'btn_in_preview');
    await page.keyboard.press('Escape'); await page.waitForTimeout(800);

    // Xuất Excel
    await go(LIST);
    await btn('Xuất Excel').first().click(); await page.waitForTimeout(1500);
    await shot('20_export');
    await closeModalBtn('Đóng');

    // Tùy chỉnh cột / Cài đặt bộ lọc
    await page.locator('button[title="Cấu hình cột hiển thị"], [title="Cấu hình cột hiển thị"]').first().click(); await page.waitForTimeout(1500);
    await shot('25_colcfg');
    await closeModalBtn('Đóng');
    await btn('Cài đặt bộ lọc').first().click(); await page.waitForTimeout(1500);
    await shot('26_filtercfg');
    await closeModalBtn('Đóng');

    }
    const foot = (txt) => page.locator('.footer button', { hasText: new RegExp('^\\s*' + txt + '\\s*$') });
    const top = async () => { await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(400); };
    const shotH = async (name, h) => { await page.setViewportSize({ width: 1440, height: h }); await page.waitForTimeout(800); await shot(name); await page.setViewportSize({ width: 1440, height: 900 }); };
    const pickType = async (txt) => {
        await page.locator('.select2-selection').first().click(); await page.waitForTimeout(600);
        await page.locator('.select2-results__option', { hasText: txt }).first().click(); await page.waitForTimeout(1500);
    };

    if (PART === 'all' || PART === 'p2') {
        await go(LIST);
        await page.locator('a.cat', { hasText: 'Hàng hoá - Dịch vụ' }).click(); await page.waitForTimeout(1200);
        await page.locator('a.scat', { hasText: 'Giữ hàng' }).click(); await page.waitForTimeout(1200);
        await icon(page.locator('.navwrap').getByText('Yêu cầu xuất giữ', { exact: true }), 'menu_muc');

        await go(LIST + '/create', 3000);
        await shotH('10_create', 1000);
        await icon(btn('Lưu nháp'), 'btn_luunhap');
        await icon(btn('Gửi duyệt'), 'btn_guiduyet');
        await icon(btn('Lưu và tiếp tục'), 'btn_luutieptuc');
        await icon(btn('Quay lại'), 'btn_quaylai');
        let got = false;
        for (const t of ['Xuất giữ HĐ hãng', 'Xuất giữ thường', 'Xuất giữ HĐDA', 'Xuất giữ HĐDV', 'Xuất giữ khuyến mại']) {
            await go(LIST + '/create', 3000);
            await pickType(t);
            await icon(page.locator('button', { hasText: /^\s*Chọn\s*$/ }), 'btn_chon_hd');
            await page.locator('button', { hasText: /^\s*Chọn\s*$/ }).first().click(); await settle(3000);
            const n = await modal().locator('table tbody tr button').count();
            console.log('type', t, 'contract rows', n);
            if (n) {
                await shot('11_contract');
                await icon(modal().locator('table tbody tr button').first(), 'btn_chon_dong_hd');
                await modal().locator('table tbody tr button').first().click(); await settle(4000);
                await shotH('11b_create_hd', 1150);
                await icon(page.locator('table tbody tr .custom-checkbox, table tbody tr input[type=checkbox]').first(), 'o_tick');
                await icon(btn('Thêm tài liệu'), 'btn_themtailieu');
                got = true; break;
            }
            if (t === 'Xuất giữ HĐ hãng') await shot('11_contract');
            await page.keyboard.press('Escape'); await page.waitForTimeout(600);
        }
        if (!got) console.log('NO CONTRACT');
        await go(LIST + '/create', 3000);
        await pickType('Xuất giữ khác');
        await icon(btn('Thêm hàng hóa'), 'btn_themhanghoa');
        await shotH('12_create_khac', 1000);

        await go(LIST + '/' + ID_KT, 3000);
        await shotTall('17_detail');
        await icon(foot('Lập phiếu xuất giữ'), 'btn_lapxg');
        await icon(foot('Từ chối'), 'btn_tuchoi');
        await icon(foot('In'), 'btn_in');
        await icon(btn('Xem lịch sử'), 'btn_xemlichsu');
        await top();
        await foot('Từ chối').click(); await page.waitForTimeout(1500);
        await shot('15_reject');
        await icon(modal().locator('button', { hasText: 'Xác nhận từ chối' }), 'btn_confirm_tuchoi');
        await icon(modal().locator('button', { hasText: 'Đóng' }), 'btn_dong_reject');
        await closeModalBtn('Đóng');
        await top();
        await foot('In').click(); await settle(3500);
        await shot('18_print');
        await page.keyboard.press('Escape'); await page.waitForTimeout(800);
    }

    if (PART === 'all' || PART === 'p3') {
        await go(LIST);
        const rowH = page.locator('table tbody tr', { hasText: 'PYCXG-0' + ID_KT }).first();
        await rowH.locator('.v2-row-actions > span').nth(2).locator('button').click(); await settle(2500);
        await shot('16_history');
        await icon(modal().locator('button', { hasText: 'Bộ lọc' }), 'btn_boloc_ls');
        await icon(modal().locator('.modal-footer button', { hasText: 'Đóng' }), 'btn_dong_ls');
        await closeModalBtn('Đóng');

        mock.approve = ID_BGD;
        await go(LIST + '/' + ID_BGD, 3000);
        await shotTall('14_approve_detail');
        await icon(foot('BGĐ duyệt'), 'btn_bgd_duyet');
        await top();
        await foot('BGĐ duyệt').click(); await page.waitForTimeout(1200);
        await shot('14_approve');
        await icon(modal().locator('button', { hasText: /^\s*Duyệt\s*$/ }), 'btn_confirm_duyet');
        await closeModalBtn('Hủy');
        await page.route(/\/api\/v1\/finance\/product-prepick-requests\?/, async (route) => {
            const res = await route.fetch(); const j = await res.json();
            (j.data || []).forEach((x) => { if (x.id === ID_BGD) x.is_can_approve = true; });
            return route.fulfill({ response: res, json: j });
        });
        await go(LIST);
        const rowB = page.locator('table tbody tr', { hasText: 'PYCXG-0' + ID_BGD }).first();
        await icon(rowB.locator('.v2-row-actions > span').nth(0), 'btn_duyet_row');
        mock.approve = null;

        mock.edit = ID_KT;
        await go(LIST + '/' + ID_KT, 3000);
        await icon(foot('Sửa'), 'btn_sua');
        await icon(foot('Xóa'), 'btn_xoa');
        await go(LIST + '/' + ID_KT + '/edit', 3500);
        await shotTall('12_edit', 1500);
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
        // Lịch sử: phiếu PYCXG-02740 có 3 mốc (PYCXG-02739 chưa có mốc nào)
        await go(LIST);
        const rowL = page.locator('table tbody tr', { hasText: 'PYCXG-02740' }).first();
        await rowL.locator('.v2-row-actions > span').nth(1).locator('button').click(); await settle(2500);
        await shot('16_history');
        await icon(modal().locator('button', { hasText: 'Bộ lọc' }), 'btn_boloc_ls');
        await closeModalBtn('Đóng');
    }

    await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });

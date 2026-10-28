// Chụp ảnh HDSD/SRS màn 26 "Phiếu yêu cầu chuyển hàng" trên DEV (dữ liệu dùng chung).
// AN TOÀN: KHÔNG bấm xác nhận Lưu / Không duyệt / Xóa / Tạo phiếu. Mở form/hộp thoại -> chụp -> Đóng/Hủy.
// Nút Sửa/Xóa: tài khoản không có phiếu Đang tạo nên chỉ BẬT TẠM cờ is_can_edit/is_can_delete trong
// response trên trình duyệt (page.route) — không ghi dữ liệu.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [tên bước ...]
const path = require('path');
const fs = require('fs');
const { openDev, DEV } = require('../../phieu-theo-form-quoc-gia/pw_dev.js');

const HERE = __dirname;
const SHOTS = path.join(HERE, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
fs.mkdirSync(ICONS, { recursive: true });
const LIST = DEV + '/finance/product-transfer-requests';
const CHO_DUYET_ID = 8111; // PYCCH-08111 — Chờ duyệt, tài khoản có quyền Không duyệt / Tổng hợp
const CHO_DUYET_CODE = 'PYCCH-08111';
const LICH_SU_CODE = 'PYCCH-08230'; // phiếu lập trên HRM -> có lịch sử
const only = process.argv.slice(2);
const fails = [];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function settle(page, ms = 1500) {
    await page.waitForLoadState('networkidle').catch(() => {});
    await sleep(ms);
    await page.mouse.move(720, 4);
    await sleep(300);
}
async function shot(page, name, opts = {}) {
    await page.screenshot({ path: path.join(SHOTS, name + '.png'), ...opts });
    console.log('shot', name);
}
async function modalShot(page, name) {
    const m = page.locator('.modal.show .modal-content').last();
    await m.waitFor({ state: 'visible', timeout: 15000 });
    await sleep(900);
    await page.mouse.move(720, 4);
    await m.screenshot({ path: path.join(SHOTS, name + '.png') });
    console.log('modal', name);
}
async function icon(loc, name) {
    try {
        await loc.first().waitFor({ state: 'visible', timeout: 8000 });
        await loc.first().screenshot({ path: path.join(ICONS, name + '.png') });
        console.log('icon', name);
    } catch (e) {
        fails.push('icon ' + name + ': ' + e.message.split('\n')[0]);
    }
}
const btn = (scope, text) => scope.locator('button:visible').filter({ hasText: new RegExp('^\\s*' + text + '\\s*$') });
const modal = (page) => page.locator('.modal.show').last();

async function step(name, fn) {
    if (only.length && !only.includes(name)) return;
    try {
        await fn();
    } catch (e) {
        fails.push(name + ': ' + e.message.split('\n')[0]);
        console.log('FAIL', name, e.message.split('\n')[0]);
    }
}

/** Lọc danh sách theo 1 mã phiếu bằng ô tìm nhanh. */
async function gotoListCode(page, code) {
    await page.goto(LIST);
    await settle(page);
    const q = page.locator('input[placeholder^="Tìm theo mã yêu cầu"]');
    await q.fill(code);
    await btn(page, 'Tìm kiếm').click();
    await settle(page);
}

/** Bật tạm cờ Sửa/Xóa trong response (chỉ hiển thị, không ghi dữ liệu). */
async function fakeEditable(page) {
    await page.route(/\/finance\/product-transfer-requests(\?|\/\d+$|\/\d+\?)/, async (route) => {
        const rt = route.request().resourceType();
        if (route.request().method() !== 'GET' || (rt !== 'xhr' && rt !== 'fetch')) return route.continue();
        const res = await route.fetch();
        const body = await res.json();
        const patch = (r) => Object.assign(r, { is_can_edit: true, is_can_delete: true, is_can_approve: false });
        if (Array.isArray(body.data)) body.data.forEach(patch);
        else if (body.data) patch(body.data);
        route.fulfill({ response: res, json: body });
    });
}

(async () => {
    const { browser, page } = await openDev(HERE);
    page.setDefaultTimeout(20000);

    await step('menu', async () => {
        await page.goto(LIST);
        await settle(page);
        await page.mouse.move(30, 300);
        await sleep(1200);
        const side = page.locator('.left-side-menu');
        const g = side.getByText('Hàng hoá - Dịch vụ - Vận chuyển', { exact: true }).first();
        await g.hover();
        await sleep(600);
        await g.click();
        await sleep(1500);
        const xh = page.getByText('Xuất hàng', { exact: true }).first();
        await xh.click();
        await sleep(1000);
        await icon(xh.locator('xpath=ancestor-or-self::*[self::a or self::li or self::button or self::div][1]'), 'menu_xuathang');
        const cands = page.getByText('Phiếu yêu cầu chuyển hàng', { exact: true });
        let muc = null;
        for (let i = 0; i < (await cands.count()); i++) {
            const b = await cands.nth(i).boundingBox();
            if (b && b.x > 440 && b.y > 120) muc = cands.nth(i);
        }
        await muc.hover();
        await sleep(500);
        await icon(muc.locator('xpath=ancestor-or-self::*[self::a or self::li or self::button or self::div][1]'), 'menu_muc');
        await page.screenshot({ path: path.join(SHOTS, '00_menu.png') });
    });

    await step('list', async () => {
        await page.goto(LIST);
        await settle(page, 2500);
        await shot(page, '01_list');
        await icon(page.locator('input[placeholder^="Tìm theo mã yêu cầu"]').locator('xpath=..'), 'o_timnhanh');
        await icon(btn(page, 'Tìm kiếm'), 'btn_timkiem');
        await icon(btn(page, 'Làm mới'), 'btn_lammoi');
        await icon(btn(page, 'Tìm kiếm nâng cao'), 'btn_timkiemnangcao');
        await icon(btn(page, 'Cài đặt bộ lọc'), 'btn_caidatboloc');
        await icon(btn(page, 'Tạo mới'), 'btn_taomoi');
        await icon(btn(page, 'Xuất Excel'), 'btn_xuatexcel');
        await icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        await icon(page.locator('.v2-row-actions span[title="In"] button'), 'btn_in_row');
        await icon(page.locator('.v2-row-actions span[title="Lịch sử"] button'), 'btn_lichsu_row');
    });

    await step('filter', async () => {
        await page.goto(LIST);
        await settle(page);
        await btn(page, 'Tìm kiếm nâng cao').click();
        await settle(page, 1200);
        await shot(page, '02_filter');
        // Ô lọc floating: lấy khối bao nhãn
        for (const [lb, name] of [['Trạng thái', 'o_trangthai'], ['Tên/mã hàng hóa', 'o_tenmahang'], ['Người tạo', 'o_nguoitao'],
            ['Người tiếp nhận', 'o_nguoitiepnhan'], ['Ngày tạo', 'o_ngaytao']]) {
            await page.evaluate(([lb, name]) => {
                const els = [...document.querySelectorAll('label, span, div, input')].filter((e) => {
                    const own = e.tagName === 'INPUT' ? e.placeholder : [...e.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent).join('').trim();
                    return own === lb && e.getBoundingClientRect().width > 0 && e.getBoundingClientRect().y > 150 && e.getBoundingClientRect().y < 300;
                });
                let e = els[0];
                while (e && !(e.getBoundingClientRect().width >= 150 && e.getBoundingClientRect().height >= 28)) e = e.parentElement;
                if (e) e.setAttribute('data-cap', name);
            }, [lb, name]);
            await icon(page.locator(`[data-cap="${name}"]`), name);
        }
        await btn(page, 'Ẩn tìm kiếm nâng cao').click().catch(() => btn(page, 'Tìm kiếm nâng cao').click());
    });

    await step('filtercfg', async () => {
        await page.goto(LIST);
        await settle(page);
        await btn(page, 'Cài đặt bộ lọc').click();
        await modalShot(page, '26_filtercfg');
        await icon(btn(modal(page), 'Lưu'), 'btn_luu');
        await icon(btn(modal(page), 'Khôi phục mặc định'), 'btn_khoiphuc');
        await icon(btn(modal(page), 'Đóng'), 'btn_dong_filtercfg');
        await btn(modal(page), 'Đóng').click();
    });

    await step('colcfg', async () => {
        await page.goto(LIST);
        await settle(page);
        await page.locator('button[title="Cấu hình cột hiển thị"]').click();
        await modalShot(page, '25_colcfg');
        await icon(btn(modal(page), 'Chọn tất cả'), 'btn_chontatca');
        await icon(btn(modal(page), 'Bỏ chọn hết'), 'btn_bochonhet');
        await icon(btn(modal(page), 'Lưu'), 'btn_luu_col');
        await icon(btn(modal(page), 'Đóng'), 'btn_dong_col');
        await btn(modal(page), 'Đóng').click();
    });

    await step('export', async () => {
        await page.goto(LIST);
        await settle(page);
        await btn(page, 'Xuất Excel').click();
        await modalShot(page, '20_export');
        await icon(btn(modal(page), 'Xuất file'), 'btn_xuatfile');
        await icon(btn(modal(page), 'Đóng'), 'btn_dong_export');
        await btn(modal(page), 'Đóng').click();
    });

    await step('history', async () => {
        await gotoListCode(page, LICH_SU_CODE);
        await page.locator('.v2-row-actions span[title="Lịch sử"] button').first().click();
        await sleep(2500);
        await modalShot(page, '16_history');
        await icon(btn(modal(page), 'Bộ lọc'), 'btn_boloc_ls');
        await icon(btn(modal(page), 'Đóng'), 'btn_dong_ls');
        await btn(modal(page), 'Đóng').click();
    });

    await step('rowapprove', async () => {
        await gotoListCode(page, CHO_DUYET_CODE);
        await shot(page, '03_row_choduyet');
        await icon(page.locator('.v2-row-actions span[title="Tổng hợp"] button'), 'btn_tonghop_row');
        await page.locator('.v2-row-actions span[title="In"] button').first().click();
        await sleep(3000);
        await modalShot(page, '18_print');
        await icon(btn(modal(page), 'In'), 'btn_in_preview');
        await modal(page).locator('button.close').first().click();
    });

    await step('detail', async () => {
        await page.goto(`${LIST}/${CHO_DUYET_ID}`);
        await settle(page, 3000);
        await shot(page, '17_detail');
        await icon(btn(page, 'Không duyệt'), 'btn_khongduyet');
        await icon(btn(page, 'In'), 'btn_in');
        await icon(btn(page, 'Tổng hợp'), 'btn_tonghop');
        await icon(btn(page, 'Quay lại'), 'btn_quaylai');
        await icon(page.locator('.system-info-section .si-header'), 'khoi_lichsu');
        await btn(page, 'Không duyệt').click();
        await modalShot(page, '15_reject');
        await icon(btn(modal(page), 'Không duyệt'), 'btn_confirm_khongduyet');
        await icon(btn(modal(page), 'Hủy'), 'btn_huy_confirm');
        await btn(modal(page), 'Hủy').click();
        await sleep(800);
        // Tổng hợp: chỉ chuyển sang màn Tạo yêu cầu xuất hàng (KHÔNG lưu gì)
        await btn(page, 'Tổng hợp').click();
        await page.waitForURL(/product-export-requests\/create/, { timeout: 20000 });
        await settle(page, 4000);
        await shot(page, '19_summary');
    });

    await step('fake', async () => {
        await fakeEditable(page);
        await gotoListCode(page, CHO_DUYET_CODE);
        await icon(page.locator('.v2-row-actions span[title="Sửa"] button'), 'btn_sua_row');
        await icon(page.locator('.v2-row-actions span[title="Xóa"] button'), 'btn_xoa_row');
        await icon(page.locator('.v2-row-actions button[title="Hành động khác"]'), 'btn_bacham_row');
        await page.locator('.v2-row-actions button[title="Hành động khác"]').first().click();
        await sleep(600);
        await icon(page.locator('.v2-row-actions__menu:visible .v2-row-actions__item').filter({ hasText: 'Lịch sử' }), 'item_lichsu');
        await icon(page.locator('.v2-row-actions__menu:visible .v2-row-actions__item').filter({ hasText: /^\s*In\s*$/ }), 'item_in');
        await page.mouse.click(700, 120);
        await sleep(500);
        await page.locator('.v2-row-actions span[title="Xóa"] button').first().click();
        await modalShot(page, '13_delete');
        await icon(btn(modal(page), 'Xóa'), 'btn_confirm_xoa');
        await btn(modal(page), 'Hủy').click();
        await sleep(600);
        // Footer chi tiết khi phiếu sửa được (Sửa)
        await page.goto(`${LIST}/${CHO_DUYET_ID}`);
        await settle(page, 2500);
        await icon(btn(page, 'Sửa'), 'btn_sua');
        // Màn Sửa
        await page.goto(`${LIST}/${CHO_DUYET_ID}/edit`);
        await settle(page, 4000);
        await shot(page, '12_edit');
        await page.unroute(/\/finance\/product-transfer-requests/);
    });

    await step('create', async () => {
        await page.goto(LIST + '/create');
        await settle(page, 3000);
        await shot(page, '10_create_empty');
        await icon(btn(page, 'Lưu nháp'), 'btn_luunhap');
        await icon(btn(page, 'Lưu và tiếp tục'), 'btn_luutieptuc');
        await icon(btn(page, 'Lưu và gửi duyệt'), 'btn_luuguiduyet');
        await icon(page.locator('button[title="Thêm hàng hóa"]'), 'btn_themhanghoa');
        // Popup chọn hàng hóa
        await page.locator('button[title="Thêm hàng hóa"]').click();
        await sleep(3500);
        const m = page.locator('.modal-card').last();
        await m.waitFor({ state: 'visible' });
        await sleep(2500);
        await page.mouse.move(720, 4);
        await m.screenshot({ path: path.join(SHOTS, '11_product.png') });
        console.log('btns', JSON.stringify(await m.locator('button:visible').allInnerTexts()));
        const cb = m.locator('tbody input[type="checkbox"]:not([disabled])').first();
        await cb.check({ force: true });
        await sleep(700);
        console.log('btns2', JSON.stringify(await m.locator('button:visible').allInnerTexts()));
        await icon(m.locator('button:visible').filter({ hasText: /Thêm \d+ hàng/ }), 'btn_themsp');
        await icon(btn(m, 'Đóng'), 'btn_dong_sp');
        await m.locator('button:visible').filter({ hasText: /Thêm \d+ hàng/ }).first().click();
        await sleep(2500);
        await btn(m, 'Đóng').click().catch(() => m.locator('button.close').first().click());
        await sleep(1500);
        // Popup chọn khách hàng
        await icon(page.locator('.customer-picker'), 'o_khachhang');
        await page.locator('.customer-picker').first().click();
        await sleep(3500);
        await modalShot(page, '11b_customer');
        await icon(btn(modal(page), 'Đóng'), 'btn_dong_kh');
        await modal(page).locator('tbody tr').first().click();
        await sleep(1500);
        // Dòng khách hàng
        await page.locator('.detail-col--qty input').first().fill('10');
        const dt = page.locator('.detail-col--date input').first();
        await dt.click();
        await dt.fill('20/11/2026');
        await page.keyboard.press('Enter');
        await sleep(400);
        await page.locator('.detail-col--note input').first().fill('Giao cho khách trước ngày cần');
        await page.mouse.click(700, 120);
        await sleep(800);
        await icon(page.locator('button.add-row-btn'), 'btn_themkhachhang');
        await icon(page.locator('.detail-col--remove button'), 'btn_xoadong');
        await icon(page.locator('td.align-middle button').filter({ has: page.locator('.ri-delete-bin-line') }).last(), 'btn_xoahang');
        await icon(page.locator('.card').filter({ hasText: 'File đính kèm' }).locator('button').filter({ hasText: 'Thêm tài liệu' }), 'btn_themtailieu');
        await settle(page, 6000);
        await shot(page, '10_create');
    });

    await step('extra', async () => {
        // Chặn mọi lệnh GHI tới API phiếu (an toàn tuyệt đối khi bấm nút trong popup)
        await page.route(/\/finance\/product-transfer-requests/, (route) =>
            route.request().method() === 'GET' ? route.fallback() : route.abort());
        await page.goto(`${LIST}/${CHO_DUYET_ID}`);
        await settle(page, 3000);
        await btn(page, 'Không duyệt').click();
        const m = modal(page);
        await m.waitFor({ state: 'visible' });
        await btn(m, 'Không duyệt').click(); // ô ghi chú trống -> popup tự báo lỗi, KHÔNG gọi API
        await modalShot(page, '15b_reject_err');
        await btn(m, 'Hủy').click();
        await sleep(600);
        await page.unroute(/\/finance\/product-transfer-requests/);
        // Chi tiết phiếu nháp của chính mình (bật tạm cờ Sửa, tắt cờ duyệt)
        await fakeEditable(page);
        await page.goto(`${LIST}/${CHO_DUYET_ID}`);
        await settle(page, 3000);
        await shot(page, '17b_detail_draft');
        await page.unroute(/\/finance\/product-transfer-requests/);
    });

    console.log('FAILS', JSON.stringify(fails, null, 1));
    await browser.close();
})().catch((e) => {
    console.error(e);
    process.exit(1);
});

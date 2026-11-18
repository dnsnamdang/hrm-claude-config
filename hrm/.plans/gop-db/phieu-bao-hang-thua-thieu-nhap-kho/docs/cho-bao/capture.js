// Chụp ảnh SRS + HDSD màn "Phiếu nhập kho chờ báo thừa, thiếu" (STT 288) trên DEV — khuôn màn mẫu phiếu
// finance-declare-debt-beginning/docs/kh/capture.js; hàm chung ../../../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js.
// AN TOÀN (dev dùng chung): màn chỉ có xem + Xuất Excel + nút "Báo hàng thừa thiếu" (mở trang Tạo phiếu báo đã nạp sẵn
// phiếu nhập kho) — chỉ mở trang rồi Quay lại, KHÔNG bấm Lưu / Lưu và gửi.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const P = require('../../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js');

const CFG = {
    route: '/warehouse/import-discrepancies',
    nhom: 'Nhập kho',
    muc: 'Phiếu nhập kho chờ báo thừa, thiếu',
    search: 'Tìm theo mã phiếu nhập kho',
    filters: [
        ['Hàng hóa', 'o_hanghoa'],
        ['Kho hàng', 'o_khohang'],
        ['Phiếu ĐNNK', 'o_dnnk'],
        ['Loại', 'o_loai'],
        ['Nhà cung cấp', 'o_ncc'],
        ['Người đề nghị', 'o_nguoidenghi'],
        ['Ngày tạo', 'o_ngaytao'],
        ['Công ty', 'o_congty'],
    ],
    code: 'PNK-02667', // dò dev 18/11/2026: có nhà cung cấp
};
const c = P.ctx(__dirname);
const { go, btn, modal } = P;

async function scrollRight(page) {
    await page.evaluate(() => document.querySelectorAll('*').forEach((el) => {
        if (el.scrollWidth > el.clientWidth + 50 && el.querySelector && el.querySelector('table')) el.scrollLeft = el.scrollWidth;
    }));
    await page.waitForTimeout(800);
}

const steps = {
    async menu(page) {
        await P.menuIcons(page, c, CFG.nhom, CFG.muc, CFG.route);
    },
    async list(page) {
        await go(page, CFG.route);
        await c.shot(page, '01_list');
        c.save('_list_text.txt', await page.locator('table').first().innerText());
        await c.icon(page.locator(`input[placeholder="${CFG.search}"]`).locator('xpath=..'), 'o_timnhanh');
        for (const [t, n] of [['Tìm kiếm nâng cao', 'btn_timkiemnangcao'], ['Tìm kiếm', 'btn_timkiem'], ['Làm mới', 'btn_lammoi'],
            ['Cài đặt bộ lọc', 'btn_caidatboloc'], ['Xuất Excel', 'btn_xuatexcel']])
            await c.icon(btn(page, t), n);
        await c.icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        const row = P.rowOf(page, CFG.code);
        await c.icon(P.act(row, 'Báo hàng thừa thiếu'), 'btn_baohang');
        await btn(page, 'Tìm kiếm nâng cao').first().click();
        await page.waitForTimeout(2500);
        await c.shot(page, '02_filter');
        for (const [lb, nm] of CFG.filters) {
            if (await P.ff(page, lb).count()) await c.icon(P.ff(page, lb), nm);
            else console.log('  thiếu ô lọc', lb);
        }
        c.save('_filter_text.txt', await page.locator('.ff').allInnerTexts().then((a) => a.join('\n')));
        await go(page, CFG.route);
        await scrollRight(page);
        await c.shot(page, '01b_list_actions');
    },
    async filtercfg(page) {
        await go(page, CFG.route);
        await btn(page, 'Cài đặt bộ lọc').first().click();
        await page.waitForTimeout(1500);
        await c.shotM(page, '26_filtercfg');
        c.save('_filtercfg_text.txt', await modal(page).innerText());
        await P.closeModal(page, /^\s*(Đóng|Hủy)\s*$/);
    },
    async colcfg(page) {
        await go(page, CFG.route);
        await page.locator('button[title="Cấu hình cột hiển thị"]').first().click();
        await page.waitForTimeout(1500);
        await c.shotM(page, '25_colcfg');
        const m = modal(page);
        c.save('_colcfg_text.txt', await m.innerText());
        await c.icon(m.locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await c.icon(m.locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        await P.closeModal(page, /^\s*(Đóng|Hủy)\s*$/);
    },
    async export(page) {
        await go(page, CFG.route);
        await btn(page, 'Xuất Excel').first().click();
        await page.waitForTimeout(1500);
        await c.shotM(page, '20_export');
        const m = modal(page);
        await c.icon(m.locator('button', { hasText: 'Xuất file' }), 'btn_xuatfile');
        c.save('_export_text.txt', await m.innerText());
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async bao(page) {
        await go(page, CFG.route);
        await P.rowAction(page, P.rowOf(page, CFG.code), 'Báo hàng thừa thiếu');
        await page.waitForURL(/exc-shortage-imports\/create/, { timeout: 30000 });
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(3000);
        await c.shot(page, '10_create_from_queue', true);
        c.save('_create_text.txt', page.url() + '\n' + (await page.locator('.exc-form').innerText()));
        await c.icon(btn(page, 'Lưu và gửi'), 'btn_luugui');
        await c.icon(btn(page, 'Lưu'), 'btn_luu');
        await c.icon(btn(page, 'Quay lại'), 'btn_quaylai');
        await btn(page, 'Quay lại').last().click();
        await page.waitForTimeout(1500);
        const unsaved = page.locator('.modal.show:visible').filter({ hasText: 'Thông tin chưa lưu' });
        if (await unsaved.count()) await btn(unsaved, 'Thoát').last().click();
        await page.waitForTimeout(1000);
        console.log('  sau Quay lại:', page.url());
    },
};

P.run(__dirname, steps).catch((e) => {
    console.error(e);
    process.exit(1);
});

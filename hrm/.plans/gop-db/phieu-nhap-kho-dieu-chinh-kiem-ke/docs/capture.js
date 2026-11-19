// Chụp ảnh SRS + HDSD màn "Phiếu nhập kho điều chỉnh kiểm kê" (STT 287) trên DEV — chép khuôn màn mẫu
// finance-declare-debt-beginning/docs/kh/capture.js; hàm chung ở ../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js.
// AN TOÀN (dev dùng chung): KHÔNG bấm Lưu / Lưu và tiếp tục / Gửi duyệt (xác nhận) / Xóa file / Chọn tệp (upload).
//   - Form Thêm: chọn phiếu kiểm kê (chỉ ĐỌC dữ liệu nguồn) + ghi chú + file đính kèm GIẢ LẬP trên trình duyệt (gán thẳng
//     vào form, không tải file lên) -> bấm Gửi duyệt -> chụp hộp "Xác nhận gửi duyệt" -> Hủy -> Quay lại -> Thoát.
//   - Lưu khi form trống: chỉ kiểm ở trình duyệt, không gửi gì.
//   - Dev KHÔNG có phiếu "Đang tạo" (dò 18/11/2026: 1 Chờ duyệt, 1 Đang hạch toán, 52 Đã hạch toán) -> ảnh Sửa / nút Sửa
//     GIẢ LẬP: đổi trạng thái phiếu PNKĐCKK-00054 thành Đang tạo trong dữ liệu trả về trình duyệt (CFG.fakeDraft).
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const P = require('../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js');

const CFG = {
    route: '/warehouse/inventory-imports',
    nhom: 'Nhập kho',
    muc: 'Phiếu nhập kho điều chỉnh kiểm kê',
    search: 'Tìm theo số phiếu',
    filters: [
        ['Mã phiếu', 'o_maphieu'],
        ['Kho', 'o_kho'],
        ['Trạng thái', 'o_trangthai'],
        ['Người tạo', 'o_nguoitao'],
        ['Mã hàng hóa', 'o_mahang'],
        ['Tên hàng hóa', 'o_tenhang'],
        ['Ngày tạo', 'o_ngaytao'],
        ['Công ty', 'o_congty'],
        ['Phòng ban', 'o_phongban'],
    ],
    waitId: 54, waitCode: 'PNKĐCKK-00054', // Chờ duyệt (có "Tạo phiếu nhập hàng")
    doingId: 53, doingCode: 'PNKĐCKK-00053', // Đang hạch toán, lịch sử 2 mốc
    doneId: 52, doneCode: 'PNKĐCKK-00052', // Đã hạch toán
    sourceId: 1096, sourceWarehouse: 7, // phiếu kiểm kê còn lập được (TPE.KKK-01096)
    note: 'Nhập điều chỉnh hàng thừa theo kết quả kiểm kê kho tháng 11/2026',
    fakeFile: { url: 'https://tanphat.s3.cloud.cmctelecom.vn/warehouse_inventory_imports/bien-ban-kiem-ke-thang-11.pdf', name: 'bien-ban-kiem-ke-thang-11.pdf', size: 245760 },
};
const c = P.ctx(__dirname);
const { go, btn, modal } = P;

const draft = (it) => Object.assign(it, {
    status: 3, status_text: 'Đang tạo', status_color: '#64748B', is_can_edit: true, is_can_create_product_import: false,
    product_import_path: null, approver_name: null, approved_time: null,
});
/** Giả lập phiếu 54 ở trạng thái Đang tạo (chỉ trên trình duyệt). */
async function fakeDraft(page) {
    await P.fakeJson(page, /warehouse-inventory-imports\?/, (j) => {
        (j.data.items || []).forEach((it) => { if (it.id === CFG.waitId) draft(it); });
    });
    await P.fakeJson(page, new RegExp('warehouse-inventory-imports/' + CFG.waitId + '(\\?|$)'), (j) => { draft(j.data.detail); });
}
const form = (page) => page.evaluate(() => !!document.querySelector('.wii-form'));
async function fillCreate(page) {
    await page.evaluate((id) => document.querySelector('.wii-form').__vue__.onSelfInventoryInput(id), CFG.sourceId);
    await page.waitForTimeout(4000);
    // Kho mặc định (kho đầu tiên của phiếu kiểm kê) không còn hàng thừa -> chọn kho HP - Hải Phòng (chỉ đọc dữ liệu nguồn)
    await page.evaluate((w) => document.querySelector('.wii-form').__vue__.onWarehouseInput(w), CFG.sourceWarehouse);
    await page.waitForTimeout(4000);
    await page.evaluate(({ note, file }) => {
        const vm = document.querySelector('.wii-form').__vue__;
        vm.onNoteInput(note);
        vm.onAddFile(file);
        window.scrollTo(0, 0);
    }, { note: CFG.note, file: CFG.fakeFile });
    await page.waitForTimeout(1500);
}

const steps = {
    async menu(page) {
        await P.menuIcons(page, c, CFG.nhom, CFG.muc, CFG.route);
    },
    async list(page) {
        await go(page, CFG.route);
        await c.shot(page, '01_list');
        await c.icon(page.locator(`input[placeholder="${CFG.search}"]`).locator('xpath=..'), 'o_timnhanh');
        for (const [t, n] of [['Tìm kiếm nâng cao', 'btn_timkiemnangcao'], ['Tìm kiếm', 'btn_timkiem'], ['Làm mới', 'btn_lammoi'],
            ['Cài đặt bộ lọc', 'btn_caidatboloc'], ['Tạo mới', 'btn_taomoi'], ['Xuất Excel', 'btn_xuatexcel'], ['In danh sách', 'btn_indanhsach']])
            await c.icon(btn(page, t), n);
        await c.icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        c.save('_list_text.txt', await page.locator('table').first().innerText());
        await btn(page, 'Tìm kiếm nâng cao').first().click();
        await page.waitForTimeout(2500);
        await c.shot(page, '02_filter');
        for (const [lb, nm] of CFG.filters) {
            if (await P.ff(page, lb).count()) await c.icon(P.ff(page, lb), nm);
            else console.log('  thiếu ô lọc', lb);
        }
        c.save('_filter_text.txt', await page.locator('.ff').allInnerTexts().then((a) => a.join('\n')));
    },
    async rows(page) {
        await fakeDraft(page);
        await go(page, CFG.route);
        const w = P.rowOf(page, CFG.waitCode);
        await c.icon(P.act(w, 'Sửa'), 'btn_sua');
        await c.icon(P.act(w, 'In'), 'btn_in_row');
        await c.icon(P.act(w, 'Lịch sử'), 'btn_lichsu_row');
        await page.evaluate(() => document.querySelectorAll('*').forEach((el) => {
            if (el.scrollWidth > el.clientWidth + 50 && el.querySelector && el.querySelector('table')) el.scrollLeft = el.scrollWidth;
        }));
        await page.waitForTimeout(800);
        await c.shot(page, '01b_list_draft');
        await page.unrouteAll({ behavior: 'ignoreErrors' });
        await go(page, CFG.route);
        const w2 = P.rowOf(page, CFG.waitCode);
        await c.icon(P.act(w2, 'Tạo phiếu nhập hàng'), 'btn_taophieunhaphang_row');
        c.save('_rows_text.txt', await w2.innerText());
    },
    async filtercfg(page) {
        await go(page, CFG.route);
        await btn(page, 'Cài đặt bộ lọc').first().click();
        await page.waitForTimeout(1500);
        await c.shotM(page, '26_filtercfg');
        c.save('_filtercfg_text.txt', await modal(page).innerText());
        await P.closeModal(page, /^\s*(Đóng|Hủy)\s*$/);
    },
    async create(page) {
        await go(page, CFG.route + '/create', false);
        await page.waitForTimeout(3000);
        await c.shot(page, '10_create');
        c.save('_create_text.txt', await page.locator('.wii-form').innerText());
        await c.icon(btn(page, 'Lưu'), 'btn_luu');
        await c.icon(btn(page, 'Lưu và tiếp tục'), 'btn_luutieptuc');
        await c.icon(btn(page, 'Gửi duyệt'), 'btn_guiduyet');
        await c.icon(btn(page, 'Quay lại'), 'btn_quaylai');
        await c.icon(btn(page, 'Thêm tài liệu'), 'btn_themtailieu');
        // Lưu khi form trống: chỉ kiểm ở trình duyệt, không gửi gì
        await btn(page, 'Lưu').first().click();
        await page.waitForTimeout(1200);
        await page.evaluate(() => window.scrollTo(0, 0));
        await c.shot(page, '11_validate');
        await go(page, CFG.route + '/create', false);
        await page.waitForTimeout(3000);
        await fillCreate(page);
        await c.shot(page, '10b_create_filled');
        c.save('_create_filled_text.txt', await page.locator('.wii-form').innerText());
        await btn(page, 'Gửi duyệt').first().click();
        await P.confirmShot(page, c, '15_send_confirm', 'Xác nhận gửi duyệt', { 'Gửi duyệt': 'btn_confirm_guiduyet', 'Hủy': 'btn_huy_confirm' }, 'Hủy');
        await P.leaveUnsaved(page, c, '18_unsaved');
    },
    async fromsource(page) {
        await go(page, '/warehouse/self-inventories/' + CFG.sourceId, false);
        await page.waitForTimeout(4000);
        const b = btn(page, /Tạo phiếu nhập kho điều/);
        console.log('  nút ở phiếu kiểm kê:', await b.count(), await b.first().innerText().catch(() => ''));
        await c.icon(b, 'btn_tu_kiemke');
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
        await page.waitForTimeout(800);
        await c.shot(page, '09_self_inventory');
    },
    async detail(page) {
        await go(page, CFG.route + '/' + CFG.waitId, false);
        await page.waitForTimeout(3000);
        await c.shot(page, '17_detail_wait');
        c.save('_detail_text.txt', await page.locator('.wii-form').innerText());
        await c.icon(btn(page, 'Tạo phiếu nhập hàng'), 'btn_taophieunhaphang');
        await c.icon(btn(page, 'In'), 'btn_in_footer');
        await go(page, CFG.route + '/' + CFG.doneId, false);
        await page.waitForTimeout(3000);
        await c.shot(page, '17c_detail_done');
        await go(page, CFG.route + '/' + CFG.doingId, false);
        await page.waitForTimeout(3000);
        const h = page.locator('.si-header').first();
        if (await h.count()) {
            await c.icon(page.locator('.si-header-right button').last(), 'btn_xemlichsu');
            await h.click();
            await page.waitForTimeout(3000);
            await c.shot(page, '17b_detail_history', true);
        } else console.log('  không thấy khối lịch sử');
    },
    async edit(page) {
        await fakeDraft(page);
        await go(page, CFG.route + '/' + CFG.waitId + '/edit', false);
        await page.waitForTimeout(3500);
        await c.shot(page, '12_edit');
        c.save('_edit_text.txt', await page.locator('.wii-form').innerText());
        await go(page, CFG.route + '/' + CFG.waitId, false);
        await page.waitForTimeout(3000);
        await c.icon(btn(page, 'Sửa'), 'btn_sua_footer');
        await c.shot(page, '17d_detail_draft');
    },
    async history(page) {
        await go(page, CFG.route);
        await P.rowAction(page, P.rowOf(page, CFG.doingCode), 'Lịch sử');
        await page.waitForTimeout(3000);
        await c.shotM(page, '16_history');
        c.save('_history_text.txt', await modal(page).innerText());
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async printone(page) {
        await go(page, CFG.route);
        await P.rowAction(page, P.rowOf(page, CFG.doneCode), 'In');
        await page.waitForTimeout(7000);
        await c.shotM(page, '19_print');
        const m = modal(page);
        c.save('_printone_text.txt', (await m.innerText()).slice(0, 3000));
        await c.icon(btn(m, 'In'), 'btn_in');
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async print(page) {
        await go(page, CFG.route);
        await btn(page, 'In danh sách').first().click();
        await page.waitForTimeout(8000);
        await c.shotM(page, '19b_printlist');
        const m = modal(page);
        c.save('_print_text.txt', (await m.innerText()).slice(0, 3000));
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async export(page) {
        await go(page, CFG.route);
        await btn(page, 'Xuất Excel').first().click();
        await page.waitForTimeout(1500);
        await c.shotM(page, '20_export');
        const m = modal(page);
        await c.icon(m.locator('button', { hasText: 'Xuất file' }), 'btn_xuatfile');
        await c.icon(m.locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await c.icon(m.locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        c.save('_export_text.txt', await m.innerText());
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async colcfg(page) {
        await go(page, CFG.route);
        await page.locator('button[title="Cấu hình cột hiển thị"]').first().click();
        await page.waitForTimeout(1500);
        await c.shotM(page, '25_colcfg');
        c.save('_colcfg_text.txt', await modal(page).innerText());
        await P.closeModal(page, /^\s*(Đóng|Hủy)\s*$/);
    },
};

P.run(__dirname, steps).catch((e) => {
    console.error(e);
    process.exit(1);
});

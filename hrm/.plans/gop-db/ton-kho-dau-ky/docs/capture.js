// Chụp ảnh SRS + HDSD màn "Khai báo tồn kho đầu kỳ" (STT 283, phân hệ Kho) trên DEV — chép khuôn màn mẫu
// finance-declare-debt-beginning/docs/kh/capture.js, hàm chung ở ../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js.
// AN TOÀN (dev dùng chung): KHÔNG bấm Lưu / Lưu và tiếp tục / Xóa / Import. Form: điền tạm trên trình duyệt -> Quay lại -> Thoát.
//   Hộp xác nhận xóa / đổi kho: chụp -> Hủy. Import: chỉ Load lên bảng + Validate (Validate chỉ kiểm, không ghi).
//   Màn KHÔNG có trang Chi tiết, Lịch sử, In danh sách (đúng code develop 02/11/2026).
//   Bộ cột: tài khoản dev đã tự ẩn bớt cột -> trả rỗng cấu hình cột của người dùng NGAY TRÊN TRÌNH DUYỆT để thấy bộ cột mặc định.
//   Form Thêm: hàng chọn được trên dev đều đã khai -> bảng hàng điền tạm trên trình duyệt (CFG.fakeProduct) — ảnh giả lập.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const path = require('path');
const P = require('../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js');

const CFG = {
    route: '/warehouse/beginning-stocks',
    nhom: 'Tồn kho đầu kỳ', // mục rail của phân hệ Kho
    muc: 'Khai báo tồn kho đầu kỳ',
    search: 'Tìm theo mã / tên hàng',
    filters: [
        ['Mã hàng', 'o_mahang'],
        ['Kho', 'o_kho'],
        ['Vị trí', 'o_vitri'],
        ['Người tạo', 'o_nguoitao'],
        ['Công ty', 'o_congty'],
    ],
    // dò dev 02/11/2026: nhóm CHƯA giao dịch (Sửa / Xóa) và nhóm ĐÃ giao dịch (không còn nút)
    freeId: 10780, freeCode: 'BLNS-IR-EVOPYRO', freePos: 'N1-T2-KV',
    usedId: 10778, usedCode: '2Q-GSAQ',
    companyId: 1, warehouseId: 1, otherWarehouseId: 2,
    colApi: /column-customizations\/detail\?table=warehouse_beginning_stocks/,
    fakeProduct: {
        product_id: 13384, product_code: 'BLNS-IR-EVOPYRO', product_name: 'Hệ thống rô bốt sấy hồng ngoại sóng ngắn 54kw, 2x 9 bóng',
        model_name: 'EVOPYRO', units: [{ unit_id: 9, name: 'Bộ', unit_coefficient: 1 }], unit_id: 9, accounting_qty: 10,
        positions: [{ position_id: 1, position_code: 'PTT-N1-D1-K1-T1', qty: 4 }, { position_id: 2, position_code: 'N1-T2-KV', qty: 5 }],
    },
    importFile: path.join(__dirname, 'hdsd_shots', 'import_test.xlsx'),
};
const c = P.ctx(__dirname);
const { go, btn, modal } = P;
const defaultCols = (page) => P.mockJson(page, CFG.colApi, { code: 200, message: 'success', data: {} });
const rowOf = (page, code, pos) => {
    let r = page.locator('tbody tr').filter({ hasText: code });
    if (pos) r = r.filter({ hasText: pos });
    return r.first();
};
const formVm = (page, fn, arg) =>
    page.evaluate(([src, a]) => {
        const el = document.querySelector('.bs-form');
        const vm = el.__vue__;
        // eslint-disable-next-line no-new-func
        return new Function('vm', 'a', src)(vm, a);
    }, [fn, arg]);

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
        await defaultCols(page);
        await go(page, CFG.route);
        await c.shot(page, '01_list');
        await c.icon(page.locator(`input[placeholder="${CFG.search}"]`).locator('xpath=..'), 'o_timnhanh');
        for (const [t, n] of [['Tìm kiếm nâng cao', 'btn_timkiemnangcao'], ['Tìm kiếm', 'btn_timkiem'], ['Làm mới', 'btn_lammoi'],
            ['Cài đặt bộ lọc', 'btn_caidatboloc'], ['Tạo mới', 'btn_taomoi'], ['Import Excel', 'btn_import'],
            ['Xuất Excel', 'btn_xuatexcel']])
            await c.icon(btn(page, t), n);
        await c.icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        await btn(page, 'Tìm kiếm nâng cao').first().click();
        await page.waitForTimeout(2500);
        await c.shot(page, '02_filter');
        for (const [lb, nm] of CFG.filters) {
            if (await P.ff(page, lb).count()) await c.icon(P.ff(page, lb), nm);
            else console.log('  thiếu ô lọc', lb);
        }
        c.save('_filter_text.txt', await page.locator('.ff').allInnerTexts().then((a) => a.join('\n')));
        c.save('_list_text.txt', await page.locator('table').first().innerText());
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
        await defaultCols(page);
        await go(page, CFG.route);
        await page.locator('button[title="Cấu hình cột hiển thị"]').first().click();
        await page.waitForTimeout(1500);
        await c.shotM(page, '25_colcfg');
        c.save('_colcfg_text.txt', await modal(page).innerText());
        await P.closeModal(page, /^\s*(Đóng|Hủy)\s*$/);
    },
    async rows(page) {
        await defaultCols(page);
        await go(page, CFG.route);
        await scrollRight(page);
        const free = rowOf(page, CFG.freeCode, CFG.freePos);
        await free.scrollIntoViewIfNeeded();
        await c.icon(P.act(free, 'Sửa'), 'btn_sua');
        await c.icon(P.act(free, 'Xóa'), 'btn_xoa');
        const used = rowOf(page, CFG.usedCode);
        c.save('_rows_text.txt', 'free: ' + (await free.innerText()) + '\nused: ' + (await used.innerText()));
        await P.act(free, 'Xóa').first().click();
        await P.confirmShot(page, c, '13_delete', 'Xác nhận xóa', { 'Xóa': 'btn_confirm_xoa', 'Hủy': 'btn_huy_confirm' }, 'Hủy');
    },
    async create(page) {
        await go(page, CFG.route + '/create', false);
        await page.waitForTimeout(2500);
        await c.shot(page, '10_create');
        await c.icon(btn(page, 'Lưu'), 'btn_luu');
        await c.icon(btn(page, 'Lưu và tiếp tục'), 'btn_luutieptuc');
        await c.icon(btn(page, 'Quay lại'), 'btn_quaylai');
        c.save('_form_options.txt', JSON.stringify(await formVm(page, 'return { c: vm.companies, w: vm.warehouses }'), null, 1));
        // chọn Kho + Công ty (chỉ đặt giá trị trên form, như người dùng chọn)
        await formVm(page, 'vm.form = { ...vm.form, warehouse_id: a.w, company_id: a.c }', { w: CFG.warehouseId, c: CFG.companyId });
        await page.waitForTimeout(1200);
        await c.icon(btn(page, 'Chọn hàng hóa'), 'btn_chonhang');
        await btn(page, 'Chọn hàng hóa').first().click();
        await page.waitForTimeout(4000);
        await c.shotM(page, '14_picker');
        c.save('_picker_text.txt', (await modal(page).innerText()).slice(0, 3000));
        // gõ mã hàng đã khai để chụp câu chặn (bấm Thêm của popup chỉ đưa hàng vào form, không lưu gì)
        const kw = modal(page).locator('input[placeholder^="Tìm theo mã, tên hàng"]').first();
        if (await kw.count()) {
            await kw.fill(CFG.freeCode);
            await kw.press('Enter');
            await page.waitForTimeout(4000);
            const name = modal(page).locator('tbody tr').filter({ hasText: CFG.freeCode }).first().locator('td').first();
            if (await name.count()) {
                await name.click().catch(() => {});
                await page.waitForTimeout(1500);
                await c.shotM(page, '14b_picker_selected');
                const add = modal(page).locator('button', { hasText: /Thêm \(/ });
                if (await add.count() && await add.isEnabled()) {
                    await c.icon(add, 'btn_them_popup');
                    await add.click();
                    await page.waitForTimeout(3000);
                    await c.shot(page, '15_blocked');
                }
            }
        }
        if (await modal(page).count()) await P.closeModal(page, /^\s*Đóng\s*$/);
        // bảng hàng điền tạm (GIẢ LẬP): 1 hàng chia 2 vị trí, tổng 9 lệch SL tồn kế toán 10
        await formVm(page, 'vm.unsavedLastActionAt = Date.now(); vm.form.products.splice(0); vm.form.products.push(JSON.parse(JSON.stringify(a)))', CFG.fakeProduct);
        await page.waitForTimeout(1200);
        await c.shot(page, '10b_create_filled');
        // kiểm dữ liệu NGAY TRÊN FORM (hàm kiểm phía trình duyệt, không gửi gì) để thấy câu báo lệch
        await formVm(page, 'vm.validate()');
        await page.waitForTimeout(1000);
        await c.shot(page, '10c_create_mismatch');
        await c.icon(page.locator('a.add-pos', { hasText: 'Thêm vị trí' }), 'btn_themvitri');
        // popup chọn vị trí
        await page.locator('.bs-form tbody tr').first().locator('td').nth(7).locator('input, .form-control, div').first().click().catch(() => {});
        await page.waitForTimeout(3500);
        if (await modal(page).count()) {
            await c.shotM(page, '16_position_picker');
            c.save('_position_text.txt', (await modal(page).innerText()).slice(0, 2000));
            await P.closeModal(page, /^\s*(Đóng|Hủy)\s*$/);
        } else {
            await formVm(page, 'vm.openPositionPicker(0, 0)');
            await page.waitForTimeout(3500);
            await c.shotM(page, '16_position_picker');
            c.save('_position_text.txt', (await modal(page).innerText()).slice(0, 2000));
            await P.closeModal(page, /^\s*(Đóng|Hủy)\s*$/);
        }
        // đổi kho khi đã có hàng -> hộp xác nhận -> Hủy
        page.evaluate(([w]) => document.querySelector('.bs-form').__vue__.onWarehouseInput(w), [CFG.otherWarehouseId]);
        await P.confirmShot(page, c, '19_change_wh', 'Đổi công ty / kho', { 'Đồng ý': 'btn_dongy', 'Hủy': 'btn_huy_doikho' }, 'Hủy');
        await P.leaveUnsaved(page, c, '18_unsaved');
    },
    async edit(page) {
        await go(page, CFG.route + '/' + CFG.freeId + '/edit', false);
        await page.waitForTimeout(3000);
        await c.shot(page, '12_edit');
        c.save('_edit_text.txt', await page.locator('.bs-form').innerText());
        // đổi tạm 1 ô Số lượng trên trình duyệt + kiểm phía trình duyệt -> báo lệch (không bấm Lưu)
        await page.evaluate(() => {
            const vm = document.querySelector('.bs-form').__vue__;
            vm.unsavedLastActionAt = Date.now();
            vm.form.items[0].qty = 3;
            vm.validated = true;
        });
        await page.waitForTimeout(1000);
        await c.shot(page, '12b_edit_mismatch');
        await P.leaveUnsaved(page, c, '18b_unsaved_edit');
        // nhóm đã giao dịch: mở thẳng trang Sửa -> báo + về danh sách
        await go(page, CFG.route + '/' + CFG.usedId + '/edit', false);
        await page.waitForTimeout(1200);
        await c.shot(page, '12c_edit_blocked');
    },
    async export(page) {
        await defaultCols(page);
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
    async template(page) {
        await go(page, CFG.route);
        await btn(page, 'Import Excel').first().click();
        await page.waitForTimeout(1500);
        const [dl] = await Promise.all([page.waitForEvent('download'), modal(page).locator('button', { hasText: 'Tải file mẫu' }).click()]);
        await dl.saveAs(path.join(c.shots, 'template.xlsx'));
        console.log('file mẫu:', dl.suggestedFilename());
    },
    async import(page) {
        await go(page, CFG.route);
        await btn(page, 'Import Excel').first().click();
        await page.waitForTimeout(1500);
        await c.shotM(page, '21_import_open');
        const m = modal(page);
        for (const [t, n] of [['Chọn file Excel', 'btn_chonfile'], ['Tải file mẫu', 'btn_taifilemau']])
            await c.icon(m.locator('button', { hasText: t }), n);
        await m.locator('input[type=file]').setInputFiles(CFG.importFile);
        await page.waitForTimeout(1000);
        await c.icon(m.locator('button', { hasText: 'Load lên bảng' }), 'btn_load');
        await m.locator('button', { hasText: 'Load lên bảng' }).click();
        await page.waitForTimeout(2500);
        await c.shotM(page, '22_import_loaded');
        await c.icon(btn(m, 'Validate'), 'btn_validate');
        await btn(m, 'Validate').click();
        await page.waitForTimeout(8000);
        await c.shotM(page, '23_import_validated');
        c.save('_import_text.txt', await m.innerText());
        const bo = m.locator('button', { hasText: 'Bỏ dòng lỗi' });
        if (await bo.count()) await c.icon(bo, 'btn_bodongloi');
        const xv = m.locator('button', { hasText: /trạng thái validate/ });
        if (await xv.count()) await c.icon(xv, 'btn_xoavalidate');
        await c.icon(btn(m, 'Import'), 'btn_import_modal'); // KHÔNG bấm
        await m.locator('button', { hasText: /^\s*Đóng\s*$/ }).last().click();
        await page.waitForTimeout(1000);
    },
};

P.run(__dirname, steps, ['template', 'import']).catch((e) => {
    console.error(e);
    process.exit(1);
});

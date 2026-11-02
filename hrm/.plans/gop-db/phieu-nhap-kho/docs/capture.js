// Chụp ảnh SRS + HDSD màn "Phiếu nhập kho" (STT 178) trên DEV — chép khuôn màn mẫu finance-declare-debt-beginning/docs/kh/capture.js.
// AN TOÀN (dev dùng chung): KHÔNG bấm Lưu / Lưu và tiếp tục / Lưu và nhập / Lưu phiếu xếp hàng / In nhóm xếp hàng (In nhóm
//   tự LƯU nhóm trước khi in) / Nhập kho ở màn xếp hàng (cũng tự lưu) / Không duyệt / Hủy phiếu / Xuất lại / In barcode (in tem
//   có thể GHI mã lô). Form: điền thử -> Quay lại -> Thoát. Hộp xác nhận: chụp -> Đóng.
//   Bấm "Lưu" CHỈ ở form Tạo còn TRỐNG: FE tự chặn (tổng SL = 0), không gửi gì lên hệ thống.
// Phiếu dùng (dò dev 02/11/2026, tài khoản DNS Admin — Super admin + Kế toán kho):
//   PNK-11592 Đang tạo / Đang đi xếp hàng · PNK-11606 Chờ duyệt · PNK-11608 Không duyệt · PNK-11607 Đã xuất lại (có lịch sử 5 mốc)
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const P = require('../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js');

const CFG = {
    route: '/finance/warehouse-imports',
    nhom: 'Hàng hoá - Dịch vụ - Vận chuyển', // mục rail phân hệ Tài chính (nhóm con trong panel: Nhập hàng)
    muc: 'Phiếu nhập kho',
    search: 'Tìm theo Mã phiếu',
    filters: [
        ['Kho nhập', 'o_kho'],
        ['Hàng hoá', 'o_hanghoa'],
        ['Mã phiếu', 'o_maphieu'],
        ['Loại', 'o_loai'],
        ['Nhà cung cấp', 'o_ncc'],
        ['Phiếu ĐNNK', 'o_dnnk'],
        ['Người đề nghị', 'o_nguoidenghi'],
        ['Người yêu cầu', 'o_nguoiyeucau'],
        ['Người tạo', 'o_nguoitao'],
        ['Trạng thái', 'o_trangthai'],
        ['Người duyệt', 'o_nguoiduyet'],
        ['Ngày tạo', 'o_ngaytao'],
    ],
    draft: { id: 11592, code: 'PNK-11592' }, // Đang tạo, Đang đi xếp hàng
    wait: { id: 11606, code: 'PNK-11606' }, // Chờ duyệt
    deny: { id: 11608, code: 'PNK-11608' }, // Không duyệt
    rex: { id: 11607, code: 'PNK-11607' }, // Đã xuất lại
};
const c = P.ctx(__dirname);
const { go, btn, modal } = P;

/** Lọc danh sách đúng 1 phiếu bằng ô tìm nhanh. */
async function findRow(page, code) {
    await go(page, CFG.route);
    const q = page.locator(`input[placeholder="${CFG.search}"]`).first();
    await q.fill(code);
    await q.press('Enter');
    await page.waitForTimeout(3000);
    return P.rowOf(page, code);
}

/** Icon 1 hành động trên dòng (nút ngoài hoặc mục trong menu ba chấm). */
async function actIcon(page, row, title, name) {
    if (await P.act(row, title).count()) return c.icon(P.act(row, title), name);
    await row.locator('button[title="Hành động khác"]').click();
    await page.waitForTimeout(700);
    const item = page.locator('.v2-row-actions__menu:visible .v2-row-actions__item', { hasText: P.exact(title) }).first();
    const ok = await c.icon(item, name);
    await page.keyboard.press('Escape');
    await page.mouse.click(1400, 120);
    await page.waitForTimeout(500);
    return ok;
}

async function openRowAction(page, row, title) {
    if (await P.act(row, title).count()) return P.act(row, title).first().click();
    await row.locator('button[title="Hành động khác"]').click();
    await page.waitForTimeout(700);
    await page.locator('.v2-row-actions__menu:visible .v2-row-actions__item', { hasText: P.exact(title) }).first().click();
}

/** vm của WarehouseImportForm (đặt giá trị tạm trên trình duyệt như người dùng chọn — không lưu). */
const formEval = (page, fn, arg) =>
    page.evaluate(
        ([src, arg]) => {
            const find = (vm) => {
                if (vm.$options.name === 'WarehouseImportForm') return vm;
                for (const ch of vm.$children) {
                    const r = find(ch);
                    if (r) return r;
                }
                return null;
            };
            const vm = find(window.$nuxt.$root);
            // eslint-disable-next-line no-new-func
            return new Function('vm', 'arg', src)(vm, arg);
        },
        [fn, arg]
    );

async function tab(page, text) {
    await page.locator('.nav-tabs a.nav-link', { hasText: text }).first().click();
    await page.waitForTimeout(1200);
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
            ['Cài đặt bộ lọc', 'btn_caidatboloc'], ['Tạo mới', 'btn_taomoi'], ['Xuất Excel', 'btn_xuatexcel']])
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
        await go(page, CFG.route);
        await page.evaluate(() => document.querySelectorAll('*').forEach((el) => {
            if (el.scrollWidth > el.clientWidth + 50 && el.querySelector && el.querySelector('table')) el.scrollLeft = el.scrollWidth;
        }));
        await page.waitForTimeout(800);
        await c.shot(page, '01b_list_actions');
        c.save('_list_head.txt', (await page.locator('thead').first().innerText()).replace(/\s+/g, ' | '));
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
        c.save('_colcfg_text.txt', await modal(page).innerText());
        const m = modal(page);
        for (const [t, n] of [['Chọn tất cả', 'btn_chontatca_cot'], ['Bỏ chọn hết', 'btn_bochonhet_cot']])
            if (await m.locator('button', { hasText: t }).count()) await c.icon(m.locator('button', { hasText: t }), n);
        await P.closeModal(page, /^\s*(Đóng|Hủy)\s*$/);
    },
    async rows(page) {
        // Đang tạo (đang đi xếp hàng): Nhập kho, Hủy, Phiếu xếp hàng, In phiếu, Xem lịch sử
        let row = await findRow(page, CFG.draft.code);
        c.save('_rows_draft.txt', await row.innerText());
        await c.shot(page, '03_row_draft');
        for (const [t, n] of [['Nhập kho', 'btn_nhapkho'], ['Hủy', 'btn_huy'], ['Phiếu xếp hàng', 'btn_xephang'],
            ['In phiếu', 'btn_inphieu'], ['Xem lịch sử', 'btn_lichsu_row']])
            await actIcon(page, row, t, n);
        await row.locator('button[title="Hành động khác"]').click();
        await page.waitForTimeout(800);
        await c.shot(page, '03b_row_menu');
        await page.keyboard.press('Escape');
        await page.mouse.click(1400, 120);
        // Hộp Xác nhận hủy -> Đóng
        row = await findRow(page, CFG.draft.code);
        await openRowAction(page, row, 'Hủy');
        await P.confirmShot(page, c, '13_cancel', 'Xác nhận hủy', { 'Hủy phiếu': 'btn_confirm_huy', 'Đóng': 'btn_dong_confirm' }, 'Đóng');
        // Chờ duyệt: Tạo phiếu nhập hàng, Không duyệt, In barcode
        row = await findRow(page, CFG.wait.code);
        c.save('_rows_wait.txt', await row.innerText());
        for (const [t, n] of [['Tạo phiếu nhập hàng', 'btn_taophieunhaphang'], ['Không duyệt', 'btn_khongduyet'], ['In barcode', 'btn_inbarcode']])
            await actIcon(page, row, t, n);
        await openRowAction(page, row, 'Không duyệt');
        await page.waitForTimeout(800);
        await P.confirmShot(page, c, '15_deny', 'Lý do không duyệt', { 'Không duyệt': 'btn_confirm_khongduyet' }, 'Đóng');
        // Không duyệt: Tạo phiếu xuất lại · Đã xuất lại: Tạo phiếu nhập lại
        row = await findRow(page, CFG.deny.code);
        await actIcon(page, row, 'Tạo phiếu xuất lại', 'btn_xuatlai_row');
        row = await findRow(page, CFG.rex.code);
        await actIcon(page, row, 'Tạo phiếu nhập lại', 'btn_nhaplai_row');
    },
    async history(page) {
        const row = await findRow(page, CFG.rex.code);
        await openRowAction(page, row, 'Xem lịch sử');
        await page.waitForTimeout(3500);
        await c.shotM(page, '16_history');
        c.save('_history_text.txt', await modal(page).innerText());
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async export(page) {
        await go(page, CFG.route);
        await btn(page, 'Xuất Excel').first().click();
        await page.waitForTimeout(1500);
        await c.shotM(page, '20_export');
        const m = modal(page);
        await c.icon(m.locator('button', { hasText: /Xuất file|Xuất Excel/ }), 'btn_xuatfile');
        await c.icon(m.locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await c.icon(m.locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        c.save('_export_text.txt', await m.innerText());
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async create(page) {
        await go(page, CFG.route + '/create', false);
        await page.waitForTimeout(2000);
        await c.shot(page, '10_create');
        for (const [t, n] of [['Lưu', 'btn_luu'], ['Lưu và tiếp tục', 'btn_luutieptuc'], ['Quay lại', 'btn_quaylai']])
            await c.icon(btn(page, t), n);
        await c.icon(page.locator('.v2-picker-input').first(), 'o_chondnnk');
        // Form còn TRỐNG: bấm Lưu -> FE tự chặn (tổng SL = 0), không gửi gì
        await btn(page, 'Lưu').first().click();
        await page.waitForTimeout(1500);
        await c.shot(page, '11_validate');
        // Popup chọn đề nghị nhập kho -> chọn 1 dòng (chỉ nạp dữ liệu lên form)
        await page.locator('.v2-picker-input').first().click();
        await page.locator('.modal.show:visible tbody tr').first().waitFor({ timeout: 30000 });
        await page.waitForTimeout(2500);
        await c.shotM(page, '14_picker');
        c.save('_picker_text.txt', await modal(page).innerText());
        await modal(page).locator('tbody tr').first().click();
        await page.waitForTimeout(4000);
        await page.locator('input[placeholder="Nhập người giao hàng"]').fill('Nguyễn Văn Giao');
        await page.waitForTimeout(500);
        // Chọn vị trí cho dòng hàng đầu
        const pos = page.locator('.v2-picker-input', { hasText: '' }).nth(1);
        await pos.click().catch(() => {});
        await page.waitForTimeout(3000);
        if (await page.locator('.modal.show:visible tbody tr').count()) {
            await c.shotM(page, '14c_position');
            c.save('_position_text.txt', await modal(page).innerText());
            await modal(page).locator('tbody tr:not(.is-disabled)').first().click();
            await page.waitForTimeout(2000);
        }
        await page.evaluate(() => window.scrollTo(0, 0));
        await c.shot(page, '10b_create_filled');
        c.save('_create_text.txt', await page.locator('.container-fluid').first().innerText());
        if (await page.locator('.nav-tabs a.nav-link', { hasText: 'Vận chuyển' }).count()) {
            await tab(page, 'Vận chuyển');
            await formEval(page, 'vm.form.transition_type = 2; if (!vm.form.trips.length) vm.form.trips.push({ delivery_trip_id: null });');
            await page.waitForTimeout(1200);
            await page.evaluate(() => window.scrollTo(0, 0));
            await c.shot(page, '10c_create_vanchuyen');
        }
        await tab(page, 'Bốc xếp');
        await formEval(page, "vm.form.arrange_delivery.rent_type = 1; vm.form.executors.push({ employee_id: null, employee_name: '', employee_price: 0 });");
        await page.waitForTimeout(1500);
        await page.evaluate(() => window.scrollTo(0, 0));
            await c.shot(page, '10d_create_bocxep');
        await tab(page, 'Thông tin chung');
        await P.leaveUnsaved(page, c, '18_unsaved');
    },
    async arrange(page) {
        await go(page, `${CFG.route}/${CFG.draft.id}/arrange`, false);
        await page.waitForTimeout(3000);
        await c.shot(page, '30_arrange');
        c.save('_arrange_text.txt', await page.locator('.container-fluid').first().innerText());
        for (const [t, n] of [['Lưu phiếu xếp hàng', 'btn_luuxephang'], ['Nhập kho', 'btn_nhapkho_xh'], ['In', 'btn_in_nhom']])
            await c.icon(btn(page, t), n);
        await c.icon(page.locator('.arrange-add'), 'btn_themphieuxep');
    },
    async edit(page) {
        await go(page, `${CFG.route}/${CFG.draft.id}/edit`, false);
        await page.waitForTimeout(3500);
        await c.shot(page, '40_import');
        c.save('_edit_text.txt', await page.locator('.container-fluid').first().innerText());
        for (const [t, n] of [['In dự kiến', 'btn_indukien'], ['Lưu và nhập', 'btn_luuvanhap']]) await c.icon(btn(page, t), n);
        if (await page.locator('.nav-tabs a.nav-link', { hasText: 'Vận chuyển' }).count()) {
            await tab(page, 'Vận chuyển');
            await formEval(page, 'vm.form.transition_type = 2; if (!vm.form.trips.length) vm.form.trips.push({ delivery_trip_id: null });');
            await page.waitForTimeout(1500);
            await page.evaluate(() => window.scrollTo(0, 0));
            await c.shot(page, '40b_import_vanchuyen');
            await tab(page, 'Thông tin chung');
        }
        const shipper = page.locator('input[placeholder="Nhập người giao hàng"]').first();
        await shipper.click();
        await page.keyboard.press('End');
        await page.keyboard.type(' (sửa)', { delay: 80 });
        await page.waitForTimeout(800);
        await P.leaveUnsaved(page, c, '18b_unsaved_edit');
    },
    async detail(page) {
        await go(page, `${CFG.route}/${CFG.wait.id}`, false);
        await page.waitForTimeout(3000);
        await c.shot(page, '20_detail');
        c.save('_detail_text.txt', await page.locator('.container-fluid').first().innerText());
        for (const [t, n] of [['Tạo phiếu nhập hàng', 'btn_taophieunhaphang_ft'], ['Không duyệt', 'btn_khongduyet_ft'], ['In phiếu', 'btn_inphieu_ft'],
            ['In barcode', 'btn_inbarcode_ft']])
            await c.icon(btn(page, t), n);
        await tab(page, 'Bốc xếp');
        await c.shotEl(page, '20b_detail_bocxep', page.locator('.card').first());
        await tab(page, 'Thông tin chung');
        await page.locator('.si-header').first().click().catch(() => {});
        await page.waitForTimeout(3000);
        await page.locator('.si-header').first().scrollIntoViewIfNeeded().catch(() => {});
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
        await page.waitForTimeout(800);
        await c.shot(page, '20c_detail_history');
        await c.icon(page.locator('.si-header-right button').last(), 'btn_xemlichsu');
        // Không duyệt: có Lý do không duyệt + Tạo phiếu xuất lại
        await go(page, `${CFG.route}/${CFG.deny.id}`, false);
        await page.waitForTimeout(3000);
        await c.shot(page, '21_detail_deny');
        await c.icon(btn(page, 'Tạo phiếu xuất lại'), 'btn_xuatlai_ft');
        // Đang tạo — đang đi xếp hàng
        await go(page, `${CFG.route}/${CFG.draft.id}`, false);
        await page.waitForTimeout(3000);
        await c.shot(page, '22_detail_draft');
        c.save('_detail_draft.txt', await page.locator('.container-fluid').first().innerText());
    },
    async print(page) {
        await go(page, `${CFG.route}/${CFG.wait.id}`, false);
        await page.waitForTimeout(3000);
        await btn(page, 'In phiếu').first().click();
        await page.waitForTimeout(8000);
        await c.shotM(page, '19_print');
        const m = modal(page);
        c.save('_print_text.txt', (await m.innerText()).slice(0, 3000));
        for (const [t, n] of [['In', 'btn_in'], ['Đóng', 'btn_dong_in']]) if (await btn(m, t).count()) await c.icon(btn(m, t), n);
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async reexport(page) {
        await go(page, `${CFG.route}/${CFG.deny.id}/re-export`, false);
        await page.waitForTimeout(3000);
        await c.shot(page, '50_reexport');
        c.save('_reexport_text.txt', await page.locator('.container-fluid').first().innerText());
        await c.icon(btn(page, 'Xuất lại'), 'btn_xuatlai');
        await btn(page, 'Xuất lại').first().click();
        await P.confirmShot(page, c, '51_reexport_confirm', 'Xác nhận xuất lại', { 'Xuất lại': 'btn_confirm_xuatlai' }, 'Đóng');
    },
    async reimport(page) {
        await go(page, `${CFG.route}/${CFG.rex.id}/re-import`, false);
        await page.waitForTimeout(3500);
        await c.shot(page, '55_reimport');
        c.save('_reimport_text.txt', await page.locator('.container-fluid').first().innerText());
    },
    async barcode(page) {
        await go(page, `${CFG.route}/${CFG.wait.id}/barcode`, false);
        await page.waitForTimeout(3500);
        await c.shot(page, '60_barcode');
        c.save('_barcode_text.txt', await page.locator('.container-fluid').first().innerText());
        for (const [t, n] of [['In barcode + tem phụ', 'btn_bc_full'], ['In barcode', 'btn_bc'], ['In tem phụ', 'btn_bc_sub']])
            await c.icon(btn(page, t), n);
    },
    async productimport(page) {
        await go(page, `/finance/product-imports/create?warehouse_import_id=${CFG.wait.id}`, false);
        await page.waitForTimeout(5000);
        await c.shot(page, '70_create_product_import');
    },
};

P.run(__dirname, steps).catch((e) => {
    console.error(e);
    process.exit(1);
});

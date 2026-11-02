// Chụp ảnh SRS + HDSD màn "Phiếu điều chuyển hàng" (STT 204) trên DEV — chép khuôn màn mẫu
// finance-declare-debt-beginning/docs/kh/capture.js, hàm chung ở ../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js.
// AN TOÀN (dev dùng chung): KHÔNG bấm Lưu nháp / Lưu và tiếp tục / Lưu và duyệt / Xóa. Form: điền thử -> Quay lại -> Thoát.
//   Hộp xác nhận (Lưu và duyệt, Xóa phiếu, Xóa dòng hàng): chụp -> Hủy.
// GIẢ LẬP trên trình duyệt (không ghi gì vào hệ thống) — dò dev 02/11/2026:
//   - dev KHÔNG có phiếu "Đang tạo" nào tài khoản chụp nhìn thấy (384 phiếu đều Đã hạch toán) -> dòng / chi tiết / trang
//     Sửa phiếu Đang tạo là phiếu PDCH-01118 đổi tạm trạng thái trên trình duyệt (CFG.fakeDraft).
//   - lịch sử PDCH-01118 thật chỉ có 1 mốc "Tạo mới" -> lịch sử 3 mốc giả lập (CFG.mockHistory).
//   - câu báo vượt tồn dưới ô SL chuyển (lỗi máy chủ trả khi bấm lưu) đặt tạm trên form để chụp.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const P = require('../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js');

const CFG = {
    route: '/finance/product-transfers',
    nhom: 'Hàng hoá - Dịch vụ - Vận chuyển', // mục rail của phân hệ Tài chính (hubGroup)
    muc: 'Phiếu điều chuyển hàng',
    search: 'Tìm theo số phiếu...',
    filters: [
        ['Kho vật lý', 'o_khovatly'],
        ['Kho xuất', 'o_khoxuat'],
        ['Kho nhập', 'o_khonhap'],
        ['Trạng thái', 'o_trangthai'],
        ['Người tạo', 'o_nguoitao'],
        ['Mã hàng hóa', 'o_mahang'],
        ['Tên hàng hóa', 'o_tenhang'],
        ['Ngày tạo', 'o_ngaytao'],
        ['Ngày hạch toán', 'o_ngayhachtoan'],
    ],
    id: 1118, code: 'PDCH-01118', // phiếu Đã hạch toán, có lịch sử thật (Tạo mới)
    listApi: /\/api\/v1\/finance\/product-transfers\?/,
    detailApi: /\/api\/v1\/finance\/product-transfers\/1118(\?|$)/,
    historyApi: /\/api\/v1\/catalog-histories\/product_transfers\/1118(\?|$)/,
    mockHistory: [
        { id: 3, action: 'change_status', action_label: 'Thay đổi trạng thái', action_group: 'status', action_color: '#d97706',
          actor_id: 13, actor_dept_code: 'HDQT', actor_code: 'DNS01', actor_name: 'DNS Admin', department_name: 'HỘI ĐỒNG QUẢN TRỊ',
          note: null, changes: [{ field: 'Trạng thái', old: 'Đang tạo', new: 'Đã hạch toán' }],
          created_at: '30/10/2026 20:36', created_at_raw: '2026-10-30 20:36:12' },
        { id: 2, action: 'update', action_label: 'Thay đổi thông tin', action_group: 'update', action_color: '#2563eb',
          actor_id: 13, actor_dept_code: 'HDQT', actor_code: 'DNS01', actor_name: 'DNS Admin', department_name: 'HỘI ĐỒNG QUẢN TRỊ',
          note: null, changes: [{ field: 'Kho nhập', old: 'Phan Trọng Tuệ - Hàng khuyến mại', new: 'Phan Trọng Tuệ - Hàng khách gửi' },
              { field: 'Ghi chú', old: '', new: 'Chuyển hàng khách gửi' }],
          created_at: '30/10/2026 20:20', created_at_raw: '2026-10-30 20:20:05' },
        { id: 1, action: 'create', action_label: 'Tạo mới', action_group: 'create', action_color: '#16a34a',
          actor_id: 13, actor_dept_code: 'HDQT', actor_code: 'DNS01', actor_name: 'DNS Admin', department_name: 'HỘI ĐỒNG QUẢN TRỊ',
          note: null, changes: [], created_at: '30/10/2026 20:15', created_at_raw: '2026-10-30 20:15:40' },
    ],
};
const c = P.ctx(__dirname);
const { go, btn, modal } = P;
const mockHistory = (page) => P.mockJson(page, CFG.historyApi, { code: 200, message: 'success', data: CFG.mockHistory });

/** Dòng PDCH-01118 thành phiếu "Đang tạo" (chỉ trên trình duyệt). */
const asDraft = (o) => Object.assign(o, { status: 1, status_text: 'Đang tạo', status_color: '#64748B', date_accounting: null,
    is_can_edit: true, is_can_delete: true });
const fakeDraftList = (page) => P.fakeJson(page, CFG.listApi, (j) => (j.data || []).forEach((r) => r.id === CFG.id && asDraft(r)));
const fakeDraftDetail = (page) => P.fakeJson(page, CFG.detailApi, (j) => asDraft(j.data));

const formVm = (page) => page.evaluate(() => !!document.querySelector('.pt-form'));
async function vm(page, fn, arg) {
    return page.evaluate(([src, a]) => {
        const el = document.querySelector('.pt-form').parentElement;
        const find = (x) => {
            if (!x) return null;
            if (x.$options && x.$options.name === 'ProductTransferForm') return x;
            for (const ch of x.$children || []) { const r = find(ch); if (r) return r; }
            return null;
        };
        const v = find(el.__vue__) || find(window.$nuxt.$root);
        // eslint-disable-next-line no-new-func
        return new Function('vm', 'arg', src)(v, a);
    }, [fn, arg]);
}

const steps = {
    // Menu hub 3 cấp (rail -> nhóm con "Điều chuyển" -> mục): làm tại chỗ, không sửa hàm chung menuIcons.
    async menu(page) {
        await go(page, CFG.route);
        await page.mouse.move(40, 300);
        await page.waitForTimeout(1200);
        await c.clipIcon(page, page.locator('a.logo').first(), 'menu_phanhe', 12, 300);
        const cat = page.locator('a.cat', { hasText: CFG.nhom.slice(0, 14) }).first();
        await c.clipIcon(page, cat, 'menu_nhom', 0, 300);
        await cat.click();
        await page.waitForTimeout(1500);
        const sub = page.getByText('Điều chuyển', { exact: true });
        for (let i = 0; i < (await sub.count()); i++) {
            const b = await sub.nth(i).boundingBox();
            if (b && b.x > 220 && b.x < 450) {
                await sub.nth(i).click();
                await page.waitForTimeout(1200);
                await c.clipIcon(page, sub.nth(i).locator('xpath=..'), 'menu_nhom2', 2);
                break;
            }
        }
        const items = page.getByText(CFG.muc, { exact: true });
        for (let i = 0; i < (await items.count()); i++) {
            const b = await items.nth(i).boundingBox();
            if (b && b.x > 430) {
                await c.clipIcon(page, items.nth(i).locator('xpath=..'), 'menu_muc', 2);
                break;
            }
        }
        await page.screenshot({ path: require('path').join(c.shots, '00_menu.png') });
    },
    async list(page) {
        await go(page, CFG.route);
        await c.shot(page, '01_list');
        await c.icon(page.locator(`input[placeholder="${CFG.search}"]`).locator('xpath=..'), 'o_timnhanh');
        for (const [t, n] of [['Tìm kiếm nâng cao', 'btn_timkiemnangcao'], ['Tìm kiếm', 'btn_timkiem'], ['Làm mới', 'btn_lammoi'],
            ['Cài đặt bộ lọc', 'btn_caidatboloc'], ['Tạo mới', 'btn_taomoi'], ['Xuất Excel', 'btn_xuatexcel'],
            ['In danh sách', 'btn_indanhsach']])
            await c.icon(btn(page, t), n);
        await c.icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        await btn(page, 'Tìm kiếm nâng cao').first().click();
        await page.waitForTimeout(1500);
        await c.shot(page, '02_filter');
        for (const [lb, nm] of CFG.filters) {
            if (await P.ff(page, lb).count()) await c.icon(P.ff(page, lb), nm);
            else console.log('  thiếu ô lọc', lb);
        }
        c.save('_filter_text.txt', await page.locator('.ff').allInnerTexts().then((a) => a.join('\n')));
        c.save('_list_text.txt', await page.locator('table').first().innerText());
    },
    async actions(page) {
        const un = await fakeDraftList(page);
        await go(page, CFG.route);
        await c.shot(page, '01b_list_actions');
        const draft = P.rowOf(page, CFG.code);
        const done = page.locator('tbody tr').nth(1);
        c.save('_rows_text.txt', 'draft: ' + (await draft.innerText()) + '\ndone: ' + (await done.innerText()));
        await c.icon(P.act(draft, 'Sửa'), 'btn_sua');
        await c.icon(P.act(draft, 'Xóa'), 'btn_xoa');
        await c.icon(P.act(done, 'In phiếu'), 'btn_inphieu');
        await c.icon(P.act(done, 'Lịch sử'), 'btn_lichsu_row');
        await c.icon(draft.locator('button[title="Hành động khác"]'), 'btn_khac');
        await draft.locator('button[title="Hành động khác"]').click();
        await page.waitForTimeout(700);
        await c.shot(page, '01c_row_menu');
        await page.keyboard.press('Escape');
        await page.mouse.click(1400, 880);
        await page.waitForTimeout(500);
        await P.rowAction(page, draft, 'Xóa');
        await P.confirmShot(page, c, '13_delete', 'Xác nhận xóa', { 'Xóa': 'btn_confirm_xoa', 'Hủy': 'btn_huy_confirm' }, 'Hủy');
        await un();
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
        await page.waitForTimeout(2000);
        await c.shot(page, '10_create');
        c.save('_create_text.txt', await page.locator('.pt-form').innerText());
        for (const [t, n] of [['Lưu nháp', 'btn_luunhap'], ['Lưu và duyệt', 'btn_luuduyet'], ['Lưu và tiếp tục', 'btn_luutieptuc'],
            ['Quay lại', 'btn_quaylai']])
            await c.icon(btn(page, t), n);
        // Lấy 2 hàng hóa thật đã từng chuyển ở kho PTT (chỉ đọc chi tiết phiếu cũ)
        const prods = await page.evaluate(async () => {
            const g = (u) => window.$nuxt.$store.dispatch('apiGetMethod', u);
            const a = (await g('finance/product-transfers/1118')).data.products;
            const b = (await g('finance/product-transfers/1117')).data.products;
            return a.concat(b).slice(0, 2).map((p) => ({ erp_product_id: p.product_id, name: p.product_name, code: p.code, model_name: p.model_name }));
        });
        console.log('  hàng thử:', prods.map((p) => p.code).join(', '));
        // chọn kho như người dùng chọn (đặt giá trị ngay trên form của trình duyệt) — KHÔNG lưu
        await vm(page, 'vm.form.warehouse_id = 1; return vm.onChangeWarehouse();');
        await page.waitForTimeout(2000);
        await vm(page, 'vm.form.acc_warehouse_export_id = 3; vm.form.acc_warehouse_import_id = 5; return vm.onChangeExportWarehouse();');
        await page.waitForTimeout(1500);
        await c.shot(page, '10a_create_kho');
        await c.icon(btn(page, 'Thêm hàng hóa'), 'btn_themhang');
        // popup chọn hàng (chỉ mở để chụp)
        await btn(page, 'Thêm hàng hóa').first().click();
        await page.waitForTimeout(3500);
        await c.shot(page, '14_picker');
        c.save('_picker_text.txt', (await page.locator('body').innerText()).slice(0, 4000));
        const dong = page.locator('button:visible', { hasText: /^\s*(Đóng|Hủy)\s*$/ });
        if (await dong.count()) await dong.last().click(); else await page.keyboard.press('Escape');
        await page.waitForTimeout(800);
        // thêm 2 dòng hàng vào bảng form (như bấm Áp dụng trong popup), nhập SL
        await vm(page, 'return vm.onApplyProducts(arg);', prods);
        await page.waitForTimeout(4000);
        await vm(page, `vm.form.products.forEach((r, i) => { r.qty = i === 0 ? 1 : 999999; });
            if (vm.form.products[1]) vm.$set(vm.formErrors, 'products.1.qty', 'Số lượng chuyển vượt quá số lượng tồn (còn ' + (vm.form.products[1].in_stock_by_unit || 0) + ')');
            window.scrollTo(0, 0);`);
        await page.waitForTimeout(1500);
        await page.locator('.pt-form textarea').first().click();
        await page.keyboard.type('Chuyển hàng sang kho hàng khách gửi', { delay: 20 });
        await page.evaluate(() => window.scrollTo(0, 0));
        await page.waitForTimeout(800);
        await c.shot(page, '10b_create_filled');
        c.save('_create_filled_text.txt', await page.locator('.pt-form').innerText());
        await c.icon(page.locator('.pt-form button[title="Xóa dòng"]'), 'btn_xoadong');
        // xóa dòng hàng: chụp hộp -> Hủy
        await page.locator('.pt-form button[title="Xóa dòng"]').first().click();
        await P.confirmShot(page, c, '15_remove_row', 'Xác nhận xóa hàng hóa', {}, 'Hủy');
        // Lưu và duyệt: chụp hộp xác nhận -> Hủy (KHÔNG bấm Xác nhận)
        await btn(page, 'Lưu và duyệt').first().click();
        await page.waitForTimeout(1000);
        await P.confirmShot(page, c, '15b_approve_confirm', 'Xác nhận lưu và duyệt', { 'Xác nhận': 'btn_xacnhan' }, 'Hủy');
        // Hộp "Thông tin chưa lưu" KHÔNG hiện ở màn này (form tự gọi markFormSaved() lúc mở -> nghi lỗi code, đã báo).
        await btn(page, 'Quay lại').last().click();
        await page.waitForTimeout(1500);
    },
    async detail(page) {
        await mockHistory(page);
        await go(page, CFG.route + '/' + CFG.id, false);
        await page.waitForTimeout(3000);
        await c.shot(page, '17_detail');
        c.save('_detail_text.txt', await page.locator('.pt-show-page').innerText());
        await c.icon(btn(page, 'In phiếu'), 'btn_inphieu_footer');
        await c.icon(page.locator('.si-header-right button').last(), 'btn_xemlichsu');
        await page.locator('.si-header').first().click();
        await page.waitForTimeout(2500);
        await page.setViewportSize({ width: 1440, height: 1120 });
        await page.waitForTimeout(800);
        await c.shot(page, '17b_detail_history');
        await page.setViewportSize({ width: 1440, height: 900 });
        // phiếu Đang tạo (giả lập): có Sửa / In phiếu / Xóa
        const un = await fakeDraftDetail(page);
        await go(page, CFG.route + '/' + CFG.id, false);
        await page.waitForTimeout(3000);
        await c.shot(page, '17c_detail_draft');
        await c.icon(btn(page, 'Sửa'), 'btn_sua_footer');
        await c.icon(btn(page, 'Xóa'), 'btn_xoa_footer');
        await un();
    },
    async edit(page) {
        const un = await fakeDraftDetail(page);
        await go(page, CFG.route + '/' + CFG.id + '/edit', false);
        await page.waitForTimeout(5000);
        await c.shot(page, '12_edit');
        c.save('_edit_text.txt', await page.locator('.pt-form').innerText());
        await un();
    },
    async history(page) {
        await mockHistory(page);
        await go(page, CFG.route);
        await P.rowAction(page, P.rowOf(page, CFG.code), 'Lịch sử');
        await page.waitForTimeout(3000);
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
        await c.icon(m.locator('button', { hasText: 'Xuất file' }), 'btn_xuatfile');
        await c.icon(m.locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await c.icon(m.locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        c.save('_export_text.txt', await m.innerText());
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async print(page) {
        await go(page, CFG.route);
        await btn(page, 'In danh sách').first().click();
        await page.waitForTimeout(8000);
        await c.shotM(page, '19_printlist');
        const m = modal(page);
        c.save('_print_text.txt', (await m.innerText()).slice(0, 3000));
        for (const [t, n] of [['In', 'btn_in'], ['Đóng', 'btn_dong_in']]) await c.icon(btn(m, t), n);
        await P.closeModal(page, /^\s*Đóng\s*$/);
        await P.rowAction(page, P.rowOf(page, CFG.code), 'In phiếu');
        await page.waitForTimeout(6000);
        await c.shotM(page, '19b_printitem');
        c.save('_printitem_text.txt', (await modal(page).innerText()).slice(0, 3000));
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

void formVm;
P.run(__dirname, steps).catch((e) => {
    console.error(e);
    process.exit(1);
});

// Chụp ảnh SRS + HDSD màn "Khai báo đầu kỳ công nợ nhà cung cấp" (STT 168) trên DEV — chép khuôn màn mẫu ../kh/capture.js.
// Hàm chung ở ../../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js.
// AN TOÀN (dev dùng chung): KHÔNG bấm Lưu / Lưu và tiếp tục / Xóa / Import. Form: điền thử -> Quay lại -> Thoát.
//   Hộp xác nhận xóa: chụp -> Hủy. Import: chỉ Load lên bảng + Validate (Validate không ghi dữ liệu).
//   Lịch sử: dev KHÔNG có khai báo NCC nào có lịch sử (đã dò 02/11/2026) -> nội dung lịch sử GIẢ LẬP trên trình duyệt.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const path = require('path');
const P = require('../../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js');

const CFG = {
    route: '/finance/declare-debt-supplier-beginnings',
    nhom: 'Khai báo đầu kỳ',
    muc: 'Khai báo đầu kỳ công nợ nhà cung cấp',
    search: 'Tìm theo mã phiếu, số hợp đồng, mã hoặc tên nhà cung cấp',
    filters: [
        ['Nhà cung cấp', 'o_ncc'],
        ['Tài khoản', 'o_taikhoan'],
        ['Số hợp đồng', 'o_sohd'],
        ['Người lập hợp đồng', 'o_nguoilaphd'],
        ['Người tạo', 'o_nguoitao'],
        ['Người cập nhật', 'o_nguoicapnhat'],
        ['Ngày tạo', 'o_ngaytao'],
    ],
    // khai báo CHƯA phát sinh (có Sửa / Xóa) và ĐÃ phát sinh (chỉ Lịch sử) — dò dev 02/11/2026
    freeId: 1514, freeCode: 'TPE_DKNCC_01302',
    usedId: 1232, usedCode: 'TPE_DKNCC_01101',
    supplierKey: 'TCX',
    historyApi: /\/api\/v1\/catalog-histories\/declare_debt_supplier_beginnings\/\d+(\?|$)/,
    mockHistory: [
        { id: 2, action: 'update', action_label: 'Thay đổi thông tin', action_group: 'update', action_color: '#2563eb',
          actor_id: 34, actor_dept_code: 'HN_QTTT', actor_code: 'TPE0034', actor_name: 'Đào Thị Thúy', department_name: 'PHÒNG QUẢN TRỊ TÀI CHÍNH',
          note: null, changes: [{ field: 'Tỷ giá', old: '25,990.00', new: '26,453.00' }, { field: 'Công nợ', old: '3,700.00', new: '3,717.00' }],
          created_at: '16/10/2026 09:12', created_at_raw: '2026-10-16 09:12:00' },
        { id: 1, action: 'create', action_label: 'Tạo mới', action_group: 'create', action_color: '#16a34a',
          actor_id: 34, actor_dept_code: 'HN_QTTT', actor_code: 'TPE0034', actor_name: 'Đào Thị Thúy', department_name: 'PHÒNG QUẢN TRỊ TÀI CHÍNH',
          note: null, changes: [], created_at: '15/10/2026 08:50', created_at_raw: '2026-10-15 08:50:00' },
    ],
    importFile: path.join(__dirname, 'hdsd_shots', 'import_test.xlsx'),
};
const c = P.ctx(__dirname);
const { go, btn, modal } = P;
const mockHistory = (page) => P.mockJson(page, CFG.historyApi, { code: 200, message: 'success', data: CFG.mockHistory });
const quick = (page) => page.locator(`input[placeholder="${CFG.search}"]`);

async function pickSupplier(page) {
    await page.locator('.select2-selection').first().click();
    await page.waitForTimeout(500);
    await page.keyboard.type(CFG.supplierKey, { delay: 60 });
    const opt = page.locator('.select2-results__option', { hasText: CFG.supplierKey + ' - ' }).first();
    await opt.waitFor({ timeout: 20000 });
    await opt.click();
    await page.waitForTimeout(1200);
}

async function searchCode(page, code) {
    await quick(page).fill(code);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(3500);
}

const steps = {
    async menu(page) {
        await P.menuIcons(page, c, CFG.nhom, CFG.muc, CFG.route);
    },
    async list(page) {
        await go(page, CFG.route);
        await c.shot(page, '01_list');
        await c.icon(quick(page).locator('xpath=..'), 'o_timnhanh');
        for (const [t, n] of [['Tìm kiếm nâng cao', 'btn_timkiemnangcao'], ['Tìm kiếm', 'btn_timkiem'], ['Làm mới', 'btn_lammoi'],
            ['Cài đặt bộ lọc', 'btn_caidatboloc'], ['Tạo mới', 'btn_taomoi'], ['Import Excel', 'btn_import'],
            ['Xuất Excel', 'btn_xuatexcel'], ['In danh sách', 'btn_indanhsach']])
            await c.icon(btn(page, t), n);
        await c.icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        c.save('_list_head.txt', await page.locator('thead').first().innerText());
        await btn(page, 'Tìm kiếm nâng cao').first().click();
        await page.waitForTimeout(1500);
        await c.shot(page, '02_filter');
        for (const [lb, nm] of CFG.filters) {
            if (await P.ff(page, lb).count()) await c.icon(P.ff(page, lb), nm);
            else console.log('  thiếu ô lọc', lb);
        }
        c.save('_filter_text.txt', await page.locator('.ff').allInnerTexts().then((a) => a.join('\n')));
        // dòng mẫu: 1 khai báo Chưa phát sinh + 1 Đã phát sinh cùng trang (tìm theo tiền tố mã), cuộn sang cột Hành động
        await go(page, CFG.route);
        await searchCode(page, 'TPE_DKNCC_0');
        await page.evaluate(() => document.querySelectorAll('*').forEach((el) => {
            if (el.scrollWidth > el.clientWidth + 50 && el.querySelector && el.querySelector('table')) el.scrollLeft = el.scrollWidth;
        }));
        await page.waitForTimeout(800);
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
    async rows(page) {
        await go(page, CFG.route);
        await searchCode(page, CFG.freeCode);
        const free = P.rowOf(page, CFG.freeCode);
        await free.scrollIntoViewIfNeeded();
        await c.icon(P.act(free, 'Sửa'), 'btn_sua');
        await c.icon(P.act(free, 'Xóa'), 'btn_xoa');
        await c.icon(P.act(free, 'Lịch sử'), 'btn_lichsu_row');
        c.save('_rows_text.txt', 'free: ' + (await free.innerText()));
        await P.act(free, 'Xóa').first().click();
        await P.confirmShot(page, c, '13_delete', 'Xác nhận xóa', { 'Xóa': 'btn_confirm_xoa', 'Hủy': 'btn_huy_confirm' }, 'Hủy');
        await searchCode(page, CFG.usedCode);
        const used = P.rowOf(page, CFG.usedCode);
        c.save('_rows_used.txt', 'used: ' + (await used.innerText()));
    },
    async create(page) {
        await go(page, CFG.route + '/add', false);
        await page.waitForTimeout(1500);
        await c.shot(page, '10_create');
        await c.icon(btn(page, 'Chọn hợp đồng'), 'btn_chonhd');
        await c.icon(btn(page, 'Lưu'), 'btn_luu');
        await c.icon(btn(page, 'Lưu và tiếp tục'), 'btn_luutieptuc');
        await c.icon(btn(page, 'Quay lại'), 'btn_quaylai');
        // Chọn hợp đồng khi chưa chọn NCC -> báo đỏ (chỉ FE, không gửi gì)
        await btn(page, 'Chọn hợp đồng').first().click();
        await page.waitForTimeout(800);
        await c.shot(page, '11_no_supplier');
        await pickSupplier(page);
        await btn(page, 'Chọn hợp đồng').first().click();
        await page.locator('.modal.show:visible tbody tr').first().waitFor({ timeout: 30000 });
        await page.waitForTimeout(2500);
        await c.shotM(page, '14_picker');
        const m = modal(page);
        c.save('_picker_text.txt', await m.innerText());
        // bấm 2 dòng CHƯA khai báo (hợp đồng mua nước ngoài USD + hợp đồng mua trong nước) — chỉ thêm vào bảng form
        for (const want of ['Hợp đồng mua nước ngoài', 'Hợp đồng mua trong nước']) {
            const r = m.locator('tbody tr:not(.is-disabled)', { hasText: want }).first();
            if (await r.count()) {
                await r.click();
                await page.waitForTimeout(900);
            }
        }
        await page.waitForTimeout(1500);
        await c.shotM(page, '14b_picker_selected');
        // Phạm vi = HĐ nhà cung cấp khác (chỉ lọc trong cửa sổ, không ghi gì)
        try {
            await m.locator('.select2-selection').first().click();
            await page.waitForTimeout(700);
            await page.locator('.select2-results__option', { hasText: 'HĐ nhà cung cấp khác' }).first().click();
            await page.waitForTimeout(4500);
            await c.shotM(page, '14c_picker_other');
            c.save('_picker_other_text.txt', (await m.innerText()).slice(0, 2000));
        } catch (e) {
            console.log('  không chụp được phạm vi NCC khác:', e.message.split('\n')[0]);
        }
        await P.closeModal(page, /^\s*Đóng\s*$/);
        await page.waitForTimeout(800);
        // điền thử ngay trên form của trình duyệt (như người dùng chọn) — KHÔNG bấm Lưu
        await page.evaluate(() => {
            const vm = document.querySelector('.declare-debt-form').closest('.v2-styles').__vue__;
            const acc = vm.accounts.find((a) => a.identify_number === '3311');
            vm.form.items.forEach((it, i) => {
                it.account_id = acc ? acc.id : it.account_id;
                it.type_dept = 2;
                it.dept_value = i === 0 ? 10391.5 : 25000000;
            });
            window.scrollTo(0, 0);
        });
        await page.waitForTimeout(1500);
        await c.shot(page, '10b_create_filled');
        c.save('_create_text.txt', await page.locator('.declare-debt-form').innerText());
        await P.leaveUnsaved(page, c, '18_unsaved');
    },
    async detail(page) {
        await mockHistory(page);
        await go(page, CFG.route + '/' + CFG.freeId, false);
        await page.waitForTimeout(2000);
        await c.shot(page, '17_detail');
        await c.icon(btn(page, 'Sửa'), 'btn_sua_footer');
        await c.icon(btn(page, 'Xóa'), 'btn_xoa_footer');
        await c.icon(page.locator('.si-header-right button').last(), 'btn_xemlichsu');
        await page.locator('.si-header').first().click();
        await page.waitForTimeout(2500);
        await c.shot(page, '17b_detail_history', true);
        c.save('_detail_text.txt', await page.locator('.declare-debt-form').innerText());
        await go(page, CFG.route + '/' + CFG.usedId, false);
        await page.waitForTimeout(2000);
        await c.shot(page, '17c_detail_used');
    },
    async edit(page) {
        await go(page, CFG.route + '/' + CFG.freeId + '/edit', false);
        await page.waitForTimeout(2500);
        await c.shot(page, '12_edit');
        c.save('_edit_text.txt', await page.locator('.declare-debt-form').innerText());
    },
    async history(page) {
        await mockHistory(page);
        await go(page, CFG.route);
        await searchCode(page, CFG.freeCode);
        await P.rowAction(page, P.rowOf(page, CFG.freeCode), 'Lịch sử');
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
        await searchCode(page, 'TPE_DKNCC_013'); // lọc gọn để bản in không vượt 2,000 dòng
        await btn(page, 'In danh sách').first().click();
        await page.waitForTimeout(8000);
        await c.shotM(page, '19_printlist');
        const m = modal(page);
        c.save('_print_text.txt', (await m.innerText()).slice(0, 3000));
        for (const [t, n] of [['In', 'btn_in'], ['Đóng', 'btn_dong_in']]) await c.icon(btn(m, t), n);
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
        await btn(m, 'Validate').click(); // Validate chỉ kiểm, không ghi
        await page.waitForTimeout(8000);
        await c.shotM(page, '23_import_validated');
        c.save('_import_text.txt', await m.innerText());
        const bo = m.locator('button', { hasText: 'Bỏ dòng lỗi' });
        if (await bo.count()) await c.icon(bo, 'btn_bodongloi');
        const xv = m.locator('button', { hasText: /trạng thái validate/ });
        if (await xv.count()) await c.icon(xv, 'btn_xoavalidate');
        if (await bo.count()) {
            await bo.first().click(); // chỉ bỏ dòng trên bảng xem trước
            await page.waitForTimeout(1200);
            await c.icon(btn(m, 'Import'), 'btn_import_modal'); // KHÔNG bấm
        }
        await m.locator('button', { hasText: /^\s*Đóng\s*$/ }).last().click();
        await page.waitForTimeout(1000);
    },
};

P.run(__dirname, steps, ['template', 'import']).catch((e) => {
    console.error(e);
    process.exit(1);
});

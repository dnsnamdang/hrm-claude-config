// Chụp ảnh SRS + HDSD màn "Phiếu huỷ hàng giữ kế toán" (STT 202) trên DEV — chép khuôn màn mẫu
// finance-declare-debt-beginning/docs/kh/capture.js; hàm chung ở ../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js.
// AN TOÀN (dev dùng chung): KHÔNG bấm Duyệt / Lưu và tiếp tục (bấm là TRỪ TỒN HÀNG GIỮ THẬT).
//   - Form lập: chọn nhân viên + chọn hàng (chỉ nạp dữ liệu để hiển thị) + gõ số -> Quay lại -> Thoát.
//   - Hộp "Xác nhận duyệt" / "Đổi nhân viên": chụp -> Hủy.
//   - Lịch sử: dev KHÔNG có phiếu nào có lịch sử (dò 60 phiếu mới nhất 02/11/2026 — phiếu chuyển từ hệ
//     thống cũ) -> nội dung lịch sử GIẢ LẬP trên trình duyệt (CFG.mockHistory).
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const P = require('../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js');

const CFG = {
    route: '/finance/accounting-prepick-cancels',
    nhom: 'Hàng hoá - Dịch vụ - Vận chuyển', // mục rail (hubGroup); tiêu đề nhóm trong panel: Giữ hàng
    muc: 'Phiếu huỷ hàng giữ kế toán',
    search: 'Tìm theo mã phiếu...',
    filters: [
        ['Công ty', 'o_congty'],
        ['Hủy của nhân viên', 'o_nhanvien'],
        ['Người tạo', 'o_nguoitao'],
        ['Tên/mã hàng hóa', 'o_hanghoa'],
        ['Ngày tạo', 'o_ngaytao'],
    ],
    // phiếu 2 hàng hoá (dò dev 02/11/2026)
    detailId: 656, detailCode: 'KTPHHG-00656',
    // nhân viên đang giữ hàng: Lại Văn Hiệp (id 265) — hàng 4741 giữ cho 2 khách, hàng 47451 có ĐVT Túi = 100 Cái
    empId: 265, empName: 'Lại Văn Hiệp',
    prodCodes: ['SUKE-ST-RW5004', 'FUNISI-XF006'],
    historyApi: /\/api\/v1\/finance\/accounting-prepick-cancels\/\d+\/histories(\?|$)/,
    mockHistory: [
        { id: 1, action: 'create', action_label: 'Tạo mới', action_color: '#16a34a', actor_code: 'HN0147',
          actor_name: 'Trần Thị Ngọc Mai', department_name: null, actor_dept_code: 'HN_KTTV',
          note: 'Đã trừ tồn hàng giữ trên 2 lô.', changes: [], created_at: '07/10/2026 08:59', created_at_raw: '2026-10-07 08:59:00' },
    ],
};
const c = P.ctx(__dirname);
const { go, btn, modal } = P;
const mockHistory = (page) => P.mockJson(page, CFG.historyApi, { message: 'success', data: CFG.mockHistory });
const formVm = (page, fn, arg) => page.evaluate(fn, arg);

async function pickEmployee(page) {
    // chọn bằng select2 như người dùng; không được thì đặt giá trị qua form (chỉ trên trình duyệt)
    try {
        await page.locator('.apc-form .select2-selection').first().click();
        await page.waitForTimeout(600);
        await page.keyboard.type(CFG.empName, { delay: 50 });
        const opt = page.locator('.select2-results__option', { hasText: CFG.empName }).first();
        await opt.waitFor({ timeout: 15000 });
        await opt.click();
    } catch (e) {
        console.log('  select2 nhân viên lỗi, đặt qua form:', e.message.split('\n')[0]);
        await page.keyboard.press('Escape');
        await formVm(page, (id) => document.querySelector('.apc-form').__vue__.onEmployeeChange(id), CFG.empId);
    }
    await page.waitForTimeout(1500);
}

const steps = {
    // Menu hub 3 tầng: rail "Hàng hoá - Dịch vụ - Vận chuyển" -> nhóm "Giữ hàng" -> mục. Hàm chung menuIcons chỉ
    // có 2 tầng nên viết lại ở đây (không sửa lib chung).
    async menu(page) {
        await go(page, CFG.route);
        await page.mouse.move(40, 300);
        await page.waitForTimeout(1200);
        await c.clipIcon(page, page.locator('a.logo').first(), 'menu_phanhe', 12, 300);
        const cat = page.locator('a.cat', { hasText: /Hàng hoá - Dịch vụ/ }).first();
        await c.clipIcon(page, cat, 'menu_nhom', 0, 300);
        await cat.click();
        await page.waitForTimeout(1500);
        const grp = page.getByText('Giữ hàng', { exact: true });
        for (let i = 0; i < (await grp.count()); i++) {
            const b = await grp.nth(i).boundingBox();
            if (b && b.x > 220 && b.x < 440) {
                await c.clipIcon(page, grp.nth(i).locator('xpath=..'), 'menu_nhom2', 2);
                await grp.nth(i).click();
                break;
            }
        }
        await page.waitForTimeout(1500);
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
            ['Cài đặt bộ lọc', 'btn_caidatboloc'], ['Tạo mới', 'btn_taomoi'], ['In', 'btn_indanhsach'], ['Xuất Excel', 'btn_xuatexcel']])
            await c.icon(btn(page, t), n);
        await c.icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        c.save('_list_text.txt', await page.locator('table').first().innerText());
        await btn(page, 'Tìm kiếm nâng cao').first().click();
        await page.waitForTimeout(1500);
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
        const row = P.rowOf(page, CFG.detailCode);
        if (await row.count()) {
            await c.icon(P.act(row, 'In'), 'btn_in_row');
            await c.icon(P.act(row, 'Lịch sử'), 'btn_lichsu_row');
        } else {
            const r0 = page.locator('tbody tr').first();
            await c.icon(P.act(r0, 'In'), 'btn_in_row');
            await c.icon(P.act(r0, 'Lịch sử'), 'btn_lichsu_row');
        }
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
        await P.closeModal(page, /^\s*(Đóng|Hủy)\s*$/);
    },
    async create(page) {
        await go(page, CFG.route + '/create', false);
        await page.waitForTimeout(2000);
        await c.shot(page, '10_create');
        await c.icon(btn(page, 'Quay lại'), 'btn_quaylai');
        await pickEmployee(page);
        await c.shot(page, '10a_employee');
        await c.icon(btn(page, 'Thêm hàng hóa'), 'btn_themhang');
        // Cửa sổ chọn hàng: chỉ đọc dữ liệu, tích + "Chọn" chỉ đưa hàng lên bảng trên form
        await btn(page, 'Thêm hàng hóa').first().click();
        await page.locator('.modal.show:visible tbody tr').first().waitFor({ timeout: 30000 });
        await page.waitForTimeout(2500);
        await c.shotM(page, '14_picker');
        let m = modal(page);
        c.save('_picker_text.txt', await m.innerText());
        for (const code of CFG.prodCodes) {
            const inp = m.locator('input[placeholder="Nhập mã hàng hóa"]');
            await inp.fill(code);
            await inp.press('Enter');
            await page.waitForTimeout(2500);
            const row = m.locator('tbody tr', { hasText: code }).first();
            await row.locator('input[type=checkbox]').first().check({ force: true }).catch(async () => row.click());
            await page.waitForTimeout(600);
        }
        await c.shotM(page, '14b_picker_selected');
        await c.icon(m.locator('button', { hasText: /^\s*Chọn \(/ }), 'btn_chon');
        await m.locator('button', { hasText: /^\s*Chọn \(/ }).first().click();
        await page.waitForTimeout(4000);
        // Bấm Duyệt khi chưa nhập số -> chỉ báo lỗi trên form (chưa tới hộp xác nhận, không gửi gì)
        await c.icon(btn(page, 'Duyệt'), 'btn_duyet');
        await c.icon(btn(page, 'Lưu và tiếp tục'), 'btn_luutieptuc');
        await btn(page, 'Duyệt').first().click();
        await page.waitForTimeout(1200);
        await c.shot(page, '11_validate');
        // thêm khách thứ 2 cho hàng đầu, nhập số, đổi ĐVT hàng thứ 2 sang Túi (chỉ trên trình duyệt)
        const link = page.locator('.add-customer-link').first();
        if (await link.count()) {
            await c.icon(link, 'link_themkhach');
            await link.click();
            await page.waitForTimeout(800);
        }
        await formVm(page, () => {
            const vm = document.querySelector('.apc-form').__vue__;
            const p2 = vm.form.products[1];
            if (p2) {
                const tui = p2.units.find((u) => !u.is_base);
                if (tui) vm.onUnitChange(p2, p2.customers[0], 1, 0, tui.unit_id);
            }
        });
        const qty = async (name, v) => {
            const i = page.locator(`input[name="${name}"]`).first();
            if (await i.count()) { await i.fill(''); await i.type(v, { delay: 40 }); }
        };
        await qty('products.0.customers.0.qty', '2');
        await qty('products.0.customers.1.qty', '9');
        await qty('products.1.customers.0.qty', '0.5');
        await page.locator('#note, textarea[name="note"]').first().fill('Huỷ hàng giữ quá hạn theo biên bản kiểm kê').catch(() => {});
        await page.waitForTimeout(1200);
        await c.shot(page, '10c_over');
        await c.icon(page.locator('.apc-form tbody tr').first().locator('.btn-danger, button.danger, [class*=danger]').first(), 'btn_xoakhach');
        await qty('products.0.customers.1.qty', '4');
        await page.waitForTimeout(1000);
        await page.evaluate(() => window.scrollTo(0, 0));
        await c.shot(page, '10b_create_filled');
        c.save('_create_text.txt', await page.locator('.apc-form').innerText());
        // Hộp xác nhận duyệt: chụp rồi Hủy — KHÔNG bấm Duyệt
        await btn(page, 'Duyệt').first().click();
        await P.confirmShot(page, c, '13_confirm', 'Xác nhận duyệt', { 'Duyệt': 'btn_confirm_duyet', 'Hủy': 'btn_huy_confirm' }, 'Hủy');
        // Đổi nhân viên khi đã có hàng: chụp hộp hỏi rồi Hủy
        await formVm(page, () => { document.querySelector('.apc-form').__vue__.onEmployeeChange(412); });
        await page.waitForTimeout(800);
        await P.confirmShot(page, c, '15_change_emp', 'Đổi nhân viên', {}, 'Hủy');
        await P.leaveUnsaved(page, c, '18_unsaved');
    },
    async detail(page) {
        await mockHistory(page);
        await go(page, CFG.route + '/' + CFG.detailId, false);
        await page.waitForTimeout(2500);
        await c.shot(page, '17_detail');
        await c.icon(btn(page, 'In'), 'btn_in_footer');
        await c.icon(page.locator('.history-head-toggle button').last(), 'btn_xemlichsu');
        c.save('_detail_text.txt', await page.locator('.apc-form').innerText());
        await page.locator('.history-head-toggle').first().click();
        await page.waitForTimeout(2500);
        await page.locator('.history-head-toggle').first().scrollIntoViewIfNeeded(); await page.evaluate(() => window.scrollBy(0, 400)); await page.waitForTimeout(800);
        await c.shot(page, '17b_detail_history');
        await btn(page, 'In').first().click();
        await page.waitForTimeout(6000);
        await c.shotM(page, '19_print');
        c.save('_print_text.txt', (await modal(page).innerText()).slice(0, 3000));
        await c.icon(btn(modal(page), 'In'), 'btn_in');
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async history(page) {
        await mockHistory(page);
        await go(page, CFG.route);
        await P.rowAction(page, P.rowOf(page, CFG.detailCode), 'Lịch sử');
        await page.waitForTimeout(3000);
        await c.shotM(page, '16_history');
        c.save('_history_text.txt', await modal(page).innerText());
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async printlist(page) {
        await go(page, CFG.route);
        await btn(page, 'In').first().click();
        await page.waitForTimeout(10000);
        await c.shotM(page, '19b_printlist');
        c.save('_printlist_text.txt', (await modal(page).innerText()).slice(0, 2000));
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
};

P.run(__dirname, steps).catch((e) => {
    console.error(e);
    process.exit(1);
});

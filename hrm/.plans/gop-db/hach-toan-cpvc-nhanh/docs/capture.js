// Chụp ảnh SRS + HDSD màn "Danh sách cần hạch toán chi phí vận chuyển nhanh" (STT 181) trên DEV — khuôn phiếu đợt 3/4
// (chép từ finance-declare-debt-beginning/docs/kh/capture.js, hàm chung ../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js).
// AN TOÀN (dev dùng chung): chỉ tick ô trên trình duyệt, bấm "Tạo phiếu kế toán" để MỞ form (chưa ghi gì), KHÔNG bấm
//   Lưu nháp / Lưu và duyệt / Lưu và tiếp tục; rời form bằng Quay lại -> Thoát. Xuất Excel được phép (chỉ đọc).
// Dữ liệu dev dò 18/11/2026 (probe.js): 23 dòng; Chưa hạch toán: id 69 (IPC 0726 HN), 72 (GYS 0726 HCM, EURO) ...;
//   Đang tạo: id 59 (SPIN 0226 HN, TPE.PKT1126.00001); Đã duyệt: còn lại.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const path = require('path');
const P = require('../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js');

const CFG = {
    route: '/finance/fast-delivery-accountings',
    nhom: 'Hàng hoá - Dịch vụ - Vận chuyển', // mục rail phân hệ Tài chính (nhóm con trong panel: Nhập hàng)
    muc: 'Danh sách cần hạch toán chi phí vận chuyển nhanh',
    search: 'Tìm theo mã HĐ mua, phiếu nhập, khách hàng',
    filters: [
        ['Công ty', 'o_congty'],
        ['Phòng ban', 'o_phongban'],
        ['Bộ phận', 'o_bophan'],
        ['Nhân viên', 'o_nhanvien'],
        ['Ngày nhập', 'o_ngaynhap'],
        ['Trạng thái', 'o_trangthai'],
        ['Khách hàng', 'o_khachhang'],
        ['Phiếu kế toán', 'o_phieukt'],
        ['Hợp đồng', 'o_hopdong'],
        ['Người duyệt', 'o_nguoiduyet'],
    ],
    tick: ['IPC 0726 HN', 'GYS 0726 HCM'], // 2 dòng Chưa hạch toán, cùng EURO
    draftKey: 'SPIN', // có dòng Đã duyệt + dòng Đang tạo
};
const c = P.ctx(__dirname);
const { go, btn, modal } = P;

/** Dòng (ô đầu của nhóm) có mã HĐ mua = code */
const groupRow = (page, code) =>
    page.locator('tbody tr').filter({ has: page.locator('td a, td span', { hasText: P.exact(code) }) }).first();

async function tick(page) {
    for (const code of CFG.tick) {
        const row = groupRow(page, code);
        await row.scrollIntoViewIfNeeded();
        await row.locator('input[type=checkbox], .v2-checkbox, label').first().click();
        await page.waitForTimeout(500);
    }
}

async function searchKeyword(page, kw) {
    const inp = page.locator(`input[placeholder="${CFG.search}"]`).first();
    await inp.fill(kw);
    await inp.press('Enter');
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(3500);
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
            ['Cài đặt bộ lọc', 'btn_caidatboloc'], ['Tạo phiếu kế toán', 'btn_taophieukt'], ['Xuất Excel', 'btn_xuatexcel']])
            await c.icon(btn(page, t), n);
        await c.icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        c.save('_list_head.txt', (await page.locator('thead').first().innerText()).replace(/\s+/g, ' | '));
        c.save('_list_foot.txt', await page.locator('body').innerText().then((t) => t.slice(-600)));
        await btn(page, 'Tìm kiếm nâng cao').first().click();
        await page.waitForTimeout(2500);
        await c.shot(page, '02_filter');
        for (const [lb, nm] of CFG.filters) {
            if (await P.ff(page, lb).count()) await c.icon(P.ff(page, lb), nm);
            else console.log('  thiếu ô lọc', lb);
        }
        c.save('_filter_text.txt', await page.locator('.ff').allInnerTexts().then((a) => a.join('\n')));
        // ô Trạng thái mở danh sách lựa chọn
        const st = P.ff(page, 'Trạng thái');
        if (await st.count()) {
            await st.locator('.select2-selection, select, .v2-select, input').first().click().catch(() => {});
            await page.waitForTimeout(1200);
            c.save('_status_opts.txt', await page.locator('.select2-results, .dropdown-menu.show, .v2-select__menu').allInnerTexts().then((a) => a.join('\n')).catch(() => ''));
            await c.shot(page, '02b_status_options');
            await page.keyboard.press('Escape');
        }
    },
    async states(page) {
        // Dòng Đã duyệt + Đang tạo cùng hợp đồng SPIN
        await go(page, CFG.route);
        await searchKeyword(page, CFG.draftKey);
        // cuộn bảng sang phải để thấy cột Hợp đồng mua, Người tạo, Người duyệt, Trạng thái
        await page.evaluate(() => document.querySelectorAll('*').forEach((el) => {
            if (el.scrollWidth > el.clientWidth + 50 && el.querySelector && el.querySelector('table')) el.scrollLeft = el.scrollWidth;
        }));
        await page.waitForTimeout(800);
        await c.shot(page, '03_states');
        c.save('_states_text.txt', await page.locator('tbody').innerText());
        // Lọc sẵn Chưa hạch toán bằng đường link việc cần làm
        await go(page, CFG.route + '?status=0');
        await c.shot(page, '04_chua_hach_toan');
        c.save('_chua_text.txt', await page.locator('tbody').innerText());
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
        for (const [t, n] of [['Chọn tất cả', 'btn_chontatca'], ['Bỏ chọn hết', 'btn_bochonhet']])
            if (await m.locator('button', { hasText: t }).count()) await c.icon(m.locator('button', { hasText: t }), n);
        await P.closeModal(page, /^\s*(Đóng|Hủy)\s*$/);
    },
    async create(page) {
        await go(page, CFG.route + '?status=0');
        // bấm khi chưa tick -> toast
        await btn(page, 'Tạo phiếu kế toán').first().click();
        await page.waitForTimeout(900);
        await c.shot(page, '10_no_select');
        c.save('_toast.txt', await page.locator('.toasted, .toasted-container').allInnerTexts().then((a) => a.join('\n')).catch(() => ''));
        await page.waitForTimeout(4000);
        await tick(page);
        await page.waitForTimeout(800);
        await c.shot(page, '11_ticked');
        await c.icon(groupRow(page, CFG.tick[0]).locator('td').nth(6), 'o_hachtoan');
        // mở form Tạo phiếu kế toán (chỉ mở, KHÔNG lưu)
        await btn(page, 'Tạo phiếu kế toán').first().click();
        await page.waitForURL(/bill-adjust-depts\/create/, { timeout: 30000 });
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(5000);
        c.save('_form_url.txt', page.url());
        await c.shot(page, '12_bill_form');
        await c.shot(page, '12b_bill_form_full', true);
        c.save('_form_text.txt', await page.locator('body').innerText());
        for (const [t, n] of [['Lưu nháp', 'btn_luunhap'], ['Lưu và duyệt', 'btn_luuduyet'], ['Lưu và tiếp tục', 'btn_luutieptuc'],
            ['Quay lại', 'btn_quaylai']])
            await c.icon(btn(page, t), n);
        // rời form không lưu
        await btn(page, 'Quay lại').last().click();
        await page.waitForTimeout(1500);
        const box = page.locator('.modal.show:visible').filter({ hasText: 'Thông tin chưa lưu' });
        if (await box.count()) await P.confirmShot(page, c, '18_unsaved', 'Thông tin chưa lưu', { 'Thoát': 'btn_thoat', 'Ở lại': 'btn_olai' }, 'Thoát');
        await page.waitForTimeout(2000);
        c.save('_after_back.txt', page.url());
    },
    async links(page) {
        await go(page, CFG.route);
        const first = page.locator('tbody tr').first();
        const piHref = await first.locator('a.v2-cell-link').nth(0).getAttribute('href');
        const billHref = await first.locator('a.v2-cell-link').nth(1).getAttribute('href');
        const bcHref = await first.locator('a.v2-cell-link').nth(2).getAttribute('href').catch(() => null);
        c.save('_links.txt', [piHref, billHref, bcHref].join('\n'));
        await go(page, piHref, false);
        await page.waitForTimeout(3000);
        await c.shot(page, '15_pi_detail');
        await go(page, billHref, false);
        await page.waitForTimeout(3000);
        await c.shot(page, '16_bill_detail');
    },
    async export(page) {
        await go(page, CFG.route);
        await btn(page, 'Xuất Excel').first().click();
        await page.waitForTimeout(1500);
        await c.shotM(page, '20_export');
        const m = modal(page);
        await c.icon(m.locator('button', { hasText: 'Xuất file' }), 'btn_xuatfile');
        for (const [t, n] of [['Chọn tất cả', 'btn_chontatca_x'], ['Bỏ chọn hết', 'btn_bochonhet_x']])
            if (await m.locator('button', { hasText: t }).count()) await c.icon(m.locator('button', { hasText: t }), n);
        c.save('_export_text.txt', await m.innerText());
        const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 60000 }), m.locator('button', { hasText: 'Xuất file' }).first().click()]);
        await dl.saveAs(path.join(c.shots, 'export.xlsx'));
        console.log('file xuất:', dl.suggestedFilename());
        await page.waitForTimeout(1500);
    },
};

P.run(__dirname, steps).catch((e) => {
    console.error(e);
    process.exit(1);
});

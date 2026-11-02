// Chụp ảnh SRS + HDSD màn "Yêu cầu mua dịch vụ" (STT 63) trên DEV — chép khuôn finance-declare-debt-beginning/docs/kh/capture.js.
// Hàm chung: ../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js
// AN TOÀN (dev dùng chung): KHÔNG bấm Lưu nháp / Gửi duyệt / Lưu và tiếp tục / Duyệt / Duyệt giá / Từ chối / Hủy yêu cầu /
//   Yêu cầu duyệt lại giá / Xóa. Form: điền thử -> Quay lại -> Thoát. Hộp xác nhận / popup ý kiến: chụp -> Hủy.
// Dữ liệu dev (dò 02/11/2026, tài khoản DNS Admin = Super admin, id 13): 103 phiếu; KHÔNG có phiếu Đang tạo / Chờ TP duyệt /
//   Chờ KS duyệt / Hủy; phiếu Không duyệt đều của người khác; KHÔNG phiếu nào có lịch sử.
//   => GIẢ LẬP trên trình duyệt (không ghi gì vào hệ thống):
//     - 01b_list_actions: 3 dòng đầu đổi trạng thái + cờ nút (Đang tạo / Chờ TP duyệt / Đã duyệt của chính mình)
//     - 12_edit, 13_delete, 30..34: chi tiết phiếu đổi trạng thái + cờ nút
//     - 11_validate: lỗi kiểm tra trả về giả lập (yêu cầu Lưu bị chặn ngay trên trình duyệt, KHÔNG gửi lên máy chủ)
//     - 16_history, 17b_detail_history: nội dung lịch sử giả lập
//     - 10b_create_filled: điền sẵn trên trình duyệt, kèm 1 file đính kèm giả lập (không upload)
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const P = require('../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js');

const CFG = {
    route: '/finance/buy-service-requests?type=all',
    base: '/finance/buy-service-requests',
    nhom: 'Yêu cầu',
    muc: 'Yêu cầu mua dịch vụ',
    search: 'Tìm theo số phiếu',
    filters: [
        ['Công ty', 'o_congty'],
        ['Phòng ban', 'o_phongban'],
        ['Số phiếu', 'o_sophieu'],
        ['Tên dịch vụ', 'o_tendv'],
        ['Trạng thái', 'o_trangthai'],
        ['Người duyệt giá', 'o_nguoiduyetgia'],
        ['Người tạo', 'o_nguoitao'],
        ['Ngày tạo', 'o_ngaytao'],
    ],
    approvedId: 90, approvedCode: 'TPE.YCMDV.2026000090', // Đã duyệt, có ý kiến TP + KS, 2 dòng dịch vụ
    rejectedId: 10, // Không duyệt (ý kiến KS "đính kèm sai BG")
    contractId: 35, // Đang lập hợp đồng
    showApi: /\/api\/v1\/finance\/buy-service-requests\/\d+(\?|$)/,
    listApi: /\/api\/v1\/finance\/buy-service-requests\?/,
    historyApi: /\/api\/v1\/catalog-histories\/buy_service_requests\/\d+(\?|$)/,
    storeApi: /\/api\/v1\/finance\/buy-service-requests\/?(\?|$)/,
};
const actor = { actor_id: 13, actor_dept_code: 'HN_DA', actor_code: 'NV0825', actor_name: 'Bùi Huyền Diệu', department_name: 'PHÒNG QUẢN TRỊ THƯƠNG HIỆU' };
CFG.mockHistory = [
    { id: 5, action: 'change_status', action_label: 'Thay đổi trạng thái', action_group: 'status', action_color: '#d97706', ...actor,
      actor_name: 'Trần Thị Hương', department_name: 'BAN KIỂM SOÁT', note: 'Đính kèm báo giá của bên cung cấp',
      changes: [{ field: 'Trạng thái', old: 'Chờ KS duyệt', new: 'Đã duyệt' }], created_at: '28/08/2026 09:01', created_at_raw: '2026-08-28 09:01:00' },
    { id: 4, action: 'change_status', action_label: 'Thay đổi trạng thái', action_group: 'status', action_color: '#d97706', ...actor,
      actor_name: 'Đào Thị Thúy', department_name: 'PHÒNG QUẢN TRỊ THƯƠNG HIỆU', note: 'Sửa lại, chỉ để 2 mục dịch vụ',
      changes: [{ field: 'Trạng thái', old: 'Chờ TP duyệt', new: 'Chờ KS duyệt' }], created_at: '28/08/2026 08:58', created_at_raw: '2026-08-28 08:58:00' },
    { id: 3, action: 'change_status', action_label: 'Thay đổi trạng thái', action_group: 'status', action_color: '#d97706', ...actor,
      note: null, changes: [{ field: 'Trạng thái', old: 'Đang tạo', new: 'Chờ TP duyệt' }], created_at: '27/08/2026 16:40', created_at_raw: '2026-08-27 16:40:00' },
    { id: 2, action: 'update', action_label: 'Thay đổi thông tin', action_group: 'update', action_color: '#2563eb', ...actor,
      note: null, changes: [{ field: 'Thuế VAT (%)', old: '8', new: '10' }, { field: 'Ghi chú', old: 'Mua dịch vụ AI', new: 'Mua dịch vụ trực tuyến cho phòng Thương hiệu' }],
      created_at: '27/08/2026 16:38', created_at_raw: '2026-08-27 16:38:00' },
    { id: 1, action: 'create', action_label: 'Tạo mới', action_group: 'create', action_color: '#16a34a', ...actor,
      note: null, changes: [], created_at: '27/08/2026 16:30', created_at_raw: '2026-08-27 16:30:00' },
];
const c = P.ctx(__dirname);
const { go, btn, modal } = P;
const mockHistory = (page) => P.mockJson(page, CFG.historyApi, { code: 200, message: 'success', data: CFG.mockHistory });
const NOFLAG = { is_can_edit: false, is_can_delete: false, is_can_department_approve: false, is_can_ks_approve: false,
    is_can_send_ks_again: false, is_can_cancel: false, is_can_create_contract: false };
const ST = {
    1: { status: 1, status_name: 'Đang tạo', status_type: 'draft', status_color: '#64748B' },
    2: { status: 2, status_name: 'Chờ TP duyệt', status_type: 'warning', status_color: '#D97706' },
    3: { status: 3, status_name: 'Chờ KS duyệt', status_type: 'warning', status_color: '#D97706' },
    4: { status: 4, status_name: 'Đã duyệt', status_type: 'success', status_color: '#16A34A' },
};

/** Giả lập chi tiết phiếu ở trạng thái `st` với bộ cờ nút `flags` (chỉ sửa JSON trên trình duyệt). */
async function fakeDetail(page, st, flags, extra = {}) {
    return P.fakeJson(page, CFG.showApi, (j) => {
        if (!j.data) return;
        Object.assign(j.data, ST[st], NOFLAG, flags, extra);
        if (st < 3) j.data.details.forEach((r) => { r.price_approve = 0; r.amount_approve = 0; });
        if (st < 3) { j.data.approver_name = null; j.data.approved_time = null; j.data.ks_comment = null; }
        if (st < 3) { j.data.department_approver_name = null; j.data.received_time = null; j.data.comment = null; }
    });
}

async function openDetail(page, id) {
    await go(page, CFG.base + '/' + id, false);
    await page.locator('.v2-footer, footer').first().waitFor({ timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(3000);
}

/** Popup ý kiến (CommentModal) đang mở: chụp -> bấm Hủy (KHÔNG bấm nút xác nhận). */
async function commentShot(page, name, title, accept, iconName, tryEmpty = false) {
    const box = page.locator('.modal.show:visible').filter({ hasText: title }).last();
    await box.waitFor({ timeout: 10000 });
    await page.waitForTimeout(800);
    if (tryEmpty) {
        // Popup Từ chối: lý do bắt buộc — bấm khi ô trống chỉ hiện báo đỏ ngay trên trình duyệt, không gửi gì đi
        await btn(box, accept).last().click();
        await page.waitForTimeout(800);
    }
    await c.shotM(page, name, box.locator('.modal-content'));
    c.save('_' + name + '.txt', await box.innerText().catch(() => ''));
    await c.icon(btn(box, accept), iconName);
    await btn(box, 'Hủy').last().click();
    await page.waitForTimeout(1000);
}

/** Ảnh cao vừa đủ nội dung: kéo cao khung nhìn = chiều cao trang (thanh nút cố định nằm đúng đáy) rồi trả về 900. */
async function tallShot(page, name, full = false) {
    const h = await page.evaluate((full) => {
        if (full) return document.documentElement.scrollHeight + 20;
        const el = document.querySelector('.container-fluid');
        return Math.ceil((el ? el.getBoundingClientRect().bottom + window.scrollY : document.body.scrollHeight) + 90);
    }, full);
    await page.setViewportSize({ width: 1440, height: Math.max(900, Math.min(h, 2600)) });
    await page.waitForTimeout(1200);
    await c.shot(page, name);
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.waitForTimeout(500);
}

function formVm() {
    const find = (vm) => {
        if (vm.$options.name === 'BuyServiceRequestForm') return vm;
        for (const ch of vm.$children) { const r = find(ch); if (r) return r; }
        return null;
    };
    return find(window.$nuxt.$root);
}

const steps = {
    async menu(page) {
        // Hub Bán hàng có thêm cấp nhóm con (Yêu cầu => Mua dịch vụ => mục) — tự cắt icon, không dùng P.menuIcons
        await go(page, CFG.route);
        await page.mouse.move(40, 300);
        await page.waitForTimeout(1200);
        await c.clipIcon(page, page.locator('a.logo').first(), 'menu_phanhe', 12, 300);
        const cat = page.locator('a.cat', { hasText: P.exact(CFG.nhom) }).first();
        await c.clipIcon(page, cat, 'menu_nhom', 0, 300);
        await cat.click();
        await page.waitForTimeout(1500);
        const grp = page.getByText('Mua dịch vụ', { exact: true });
        for (let i = 0; i < (await grp.count()); i++) {
            const b = await grp.nth(i).boundingBox();
            if (b && b.x > 220 && b.x < 600) {
                await c.clipIcon(page, grp.nth(i).locator('xpath=..'), 'menu_nhomcon', 2);
                await grp.nth(i).click();
                break;
            }
        }
        await page.waitForTimeout(1200);
        const items = page.getByText(CFG.muc, { exact: true });
        for (let i = 0; i < (await items.count()); i++) {
            const b = await items.nth(i).boundingBox();
            if (b && b.x > 450) {
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
            ['Cài đặt bộ lọc', 'btn_caidatboloc'], ['Tạo mới', 'btn_taomoi'], ['Xuất Excel', 'btn_xuatexcel'], ['In danh sách', 'btn_indanhsach']])
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
    },
    async quicksearch(page) {
        // Kiểm ô tìm nhanh: gõ số phiếu rồi Tìm kiếm — xem danh sách có thu hẹp không (chỉ đọc)
        await go(page, CFG.route);
        await page.locator(`input[placeholder="${CFG.search}"]`).fill(CFG.approvedCode);
        await btn(page, 'Tìm kiếm').first().click();
        await page.waitForTimeout(4000);
        await c.shot(page, '03_quicksearch');
        c.save('_quicksearch.txt', await page.locator('text=/Hiển thị/').first().innerText().catch(() => ''));
    },
    async rowsfake(page) {
        // GIẢ LẬP 3 dòng đầu ở 3 trạng thái khác nhau để thấy đủ nút ở cột Hành động
        await P.fakeJson(page, CFG.listApi, (j) => {
            const d = j.data || [];
            if (d[0]) Object.assign(d[0], ST[1], NOFLAG, { is_can_edit: true, is_can_delete: true, received_time: null, approved_time: null, approver_name: null });
            if (d[1]) Object.assign(d[1], ST[2], NOFLAG, { is_can_department_approve: true, approved_time: null, received_time: null, approver_name: null });
            if (d[2]) Object.assign(d[2], ST[4], NOFLAG, { is_can_send_ks_again: true, is_can_cancel: true, is_can_create_contract: true });
        });
        await go(page, CFG.route);
        await page.evaluate(() => document.querySelectorAll('*').forEach((el) => {
            if (el.scrollWidth > el.clientWidth + 50 && el.querySelector && el.querySelector('table')) el.scrollLeft = el.scrollWidth;
        }));
        await page.waitForTimeout(800);
        await c.shot(page, '01b_list_actions');
        const rows = page.locator('tbody tr');
        await c.icon(P.act(rows.nth(0), 'Sửa'), 'btn_sua');
        await c.icon(P.act(rows.nth(0), 'Xóa'), 'btn_xoa');
        c.save('_rows_text.txt', (await rows.nth(0).innerText()) + '\n' + (await rows.nth(1).innerText()) + '\n' + (await rows.nth(2).innerText()));
        // menu "…" của dòng Đã duyệt
        const more = rows.nth(2).locator('button[title="Hành động khác"]');
        if (await more.count()) {
            await more.click();
            await page.waitForTimeout(800);
            await c.shot(page, '01c_row_menu');
            const menu = page.locator('.v2-row-actions__menu:visible');
            for (const [t, n] of [['In phiếu', 'btn_inphieu_row'], ['Lịch sử', 'btn_lichsu_row'], ['Hủy yêu cầu', 'btn_huy_row'],
                ['Yêu cầu duyệt lại giá', 'btn_duyetlai_row'], ['Lập hợp đồng mua dịch vụ', 'btn_laphd_row']])
                await c.icon(menu.locator(`button[title="${t}"]`), n);
            c.save('_rowmenu.txt', await menu.innerText().catch(() => ''));
            await page.keyboard.press('Escape');
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
    },
    async printdetail(page) {
        await openDetail(page, CFG.approvedId);
        await c.icon(btn(page, 'In phiếu'), 'btn_inphieu');
        await btn(page, 'In phiếu').first().click();
        await page.waitForTimeout(8000);
        await c.shotM(page, '19b_printdetail');
        c.save('_printdetail_text.txt', (await modal(page).innerText()).slice(0, 3000));
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async create(page) {
        await go(page, CFG.base + '/create', false);
        await page.waitForTimeout(3000);
        await c.shot(page, '10_create');
        for (const [t, n] of [['Lưu nháp', 'btn_luunhap'], ['Gửi duyệt', 'btn_guiduyet'], ['Lưu và tiếp tục', 'btn_luutieptuc'],
            ['Quay lại', 'btn_quaylai'], ['Thêm dòng', 'btn_themdong']])
            await c.icon(btn(page, t), n);
        await c.icon(page.locator('button', { hasText: /Thêm tài liệu/ }), 'btn_themtailieu');
        c.save('_create_text.txt', await page.locator('.container-fluid').first().innerText());
        // điền thử ngay trên form của trình duyệt — KHÔNG bấm Lưu nháp / Gửi duyệt
        await page.evaluate((fn) => {
            const vm = eval('(' + fn + ')')();
            const costs = vm.costOptions;
            const pick = (kw, i) => costs.find((x) => x.name.toLowerCase().includes(kw)) || costs[i];
            const a = pick('vận chuyển', 0);
            const b = pick('lắp đặt', 1);
            vm.form.note = 'Thuê vận chuyển và lắp đặt máy nén khí cho dự án nhà máy Bắc Ninh';
            vm.form.vat_percent = 8;
            vm.form.details = [
                { cost_id: a.id, cost_name: a.name, supplier_id: 999001, supplier_code: 'NCC-VT01', supplier_name: 'CÔNG TY TNHH VẬN TẢI MINH PHÁT',
                  qty: 2, price: 3500000, amount: 7000000, price_approve: 0, amount_approve: 0 },
                { cost_id: b.id, cost_name: b.name, supplier_id: 999002, supplier_code: 'NCC-LD02', supplier_name: 'CÔNG TY CP KỸ THUẬT AN BÌNH',
                  qty: 1, price: 12000000, amount: 12000000, price_approve: 0, amount_approve: 0 },
            ];
            vm.pendingFiles.push({ url: 'bao-gia-van-chuyen-lap-dat.pdf', name: 'bao-gia-van-chuyen-lap-dat.pdf', size: 245760 });
            window.scrollTo(0, 0);
        }, formVm.toString());
        await page.waitForTimeout(2000);
        await c.shot(page, '10b_create_filled');
        // Lỗi kiểm tra: CHẶN yêu cầu Lưu ngay trên trình duyệt, trả lỗi giả lập (không gì tới máy chủ)
        await page.route(CFG.storeApi, (route) => {
            if (route.request().method() !== 'POST') return route.continue();
            return route.fulfill({ status: 422, contentType: 'application/json', body: JSON.stringify({ message: 'The given data was invalid.', errors: {
                note: ['Bắt buộc phải nhập'], attachments: ['Bắt buộc phải nhập'], 'details.0.cost_id': ['Bắt buộc phải nhập'],
                'details.0.qty': ['Bắt buộc phải nhập'], 'details.0.price': ['Bắt buộc phải nhập'] } }) });
        });
        await page.evaluate((fn) => {
            const vm = eval('(' + fn + ')')();
            vm.form.note = '';
            vm.form.vat_percent = 0;
            vm.pendingFiles.splice(0);
            vm.form.details = [{ cost_id: '', cost_name: '', supplier_id: null, supplier_code: '', supplier_name: '', qty: 0, price: 0, amount: 0, price_approve: 0, amount_approve: 0 }];
            vm.touched = true;
            vm.formError = { note: ['Bắt buộc phải nhập'], attachments: ['Bắt buộc phải nhập'], 'details.0.cost_id': ['Bắt buộc phải nhập'],
                'details.0.qty': ['Bắt buộc phải nhập'], 'details.0.price': ['Bắt buộc phải nhập'] };
            window.scrollTo(0, 0);
        }, formVm.toString());
        await page.waitForTimeout(1500);
        await c.shot(page, '11_validate');
        await page.unroute(CFG.storeApi);
        // KHÔNG chụp hộp "Thông tin chưa lưu": form gọi markFormSaved() ngay khi mở nên Quay lại về thẳng danh sách
        // (đã thử gõ Ghi chú bằng bàn phím rồi bấm Quay lại — không có hộp hỏi) -> ghi vào báo cáo nghi lỗi.
        await btn(page, 'Quay lại').last().click();
        await page.waitForTimeout(1500);
    },
    async edit(page) {
        await fakeDetail(page, 1, { is_can_edit: true, is_can_delete: true }, { comment: null, ks_comment: null });
        await go(page, CFG.base + '/' + CFG.rejectedId + '/edit', false);
        await page.waitForTimeout(5000);
        await tallShot(page, '12_edit');
        c.save('_edit_text.txt', await page.locator('.container-fluid').first().innerText());
    },
    async draftdetail(page) {
        // GIẢ LẬP phiếu Đang tạo của chính mình: footer Sửa / In phiếu / Xóa; hộp Xác nhận xóa -> Hủy
        await fakeDetail(page, 1, { is_can_edit: true, is_can_delete: true }, { comment: null, ks_comment: null });
        await openDetail(page, CFG.rejectedId);
        await tallShot(page, '17d_detail_draft');
        await c.icon(btn(page, 'Sửa'), 'btn_sua_footer');
        await c.icon(btn(page, 'Xóa'), 'btn_xoa_footer');
        await btn(page, 'Xóa').last().click();
        await P.confirmShot(page, c, '13_delete', 'Xác nhận xóa', { 'Xóa': 'btn_confirm_xoa', 'Hủy': 'btn_huy_confirm' }, 'Hủy');
    },
    async tpapprove(page) {
        await fakeDetail(page, 2, { is_can_department_approve: true });
        await openDetail(page, CFG.approvedId);
        await tallShot(page, '30_detail_wait_tp');
        await c.icon(btn(page, 'Trưởng phòng duyệt'), 'btn_tpduyet');
        await c.icon(btn(page, 'Từ chối'), 'btn_tuchoi');
        await btn(page, 'Trưởng phòng duyệt').last().click();
        await commentShot(page, '31_tp_modal', 'Trưởng phòng duyệt yêu cầu mua dịch vụ', 'Duyệt', 'btn_duyet_modal');
        await btn(page, 'Từ chối').last().click();
        await commentShot(page, '32_reject_modal', 'Từ chối yêu cầu mua dịch vụ', 'Từ chối', 'btn_tuchoi_modal', true);
    },
    async ksapprove(page) {
        await fakeDetail(page, 3, { is_can_ks_approve: true }, { approver_name: null, approved_time: null, ks_comment: null });
        await openDetail(page, CFG.approvedId);
        await tallShot(page, '33_detail_wait_ks');
        await c.icon(btn(page, 'Kiểm soát duyệt giá'), 'btn_ksduyet');
        await btn(page, 'Kiểm soát duyệt giá').last().click();
        await commentShot(page, '34_ks_modal', 'Ban kiểm soát duyệt giá', 'Duyệt giá', 'btn_duyetgia_modal');
    },
    async approvedowner(page) {
        await fakeDetail(page, 4, { is_can_send_ks_again: true, is_can_cancel: true, is_can_create_contract: true });
        await openDetail(page, CFG.approvedId);
        await tallShot(page, '35_detail_approved_owner');
        await c.icon(btn(page, 'Yêu cầu duyệt lại giá'), 'btn_duyetlai');
        await c.icon(btn(page, 'Hủy yêu cầu'), 'btn_huyyc');
        await c.icon(btn(page, 'Lập hợp đồng mua dịch vụ'), 'btn_laphd');
        await btn(page, 'Hủy yêu cầu').last().click();
        await commentShot(page, '36_cancel_modal', 'Hủy yêu cầu mua dịch vụ', 'Hủy yêu cầu', 'btn_huyyc_modal');
    },
    async detail(page) {
        await mockHistory(page);
        await openDetail(page, CFG.approvedId);
        await tallShot(page, '17_detail');
        c.save('_detail_text.txt', await page.locator('.container-fluid').first().innerText());
        await c.icon(page.locator('.si-header-right button').last(), 'btn_xemlichsu');
        await page.locator('.si-header').first().click();
        await page.waitForTimeout(2500);
        await tallShot(page, '17b_detail_history', true);
        await openDetail(page, CFG.rejectedId);
        await tallShot(page, '17c_detail_rejected');
        c.save('_detail_rejected.txt', await page.locator('.container-fluid').first().innerText());
        await openDetail(page, CFG.contractId);
        await c.shot(page, '17e_detail_contract');
    },
    async history(page) {
        await mockHistory(page);
        await go(page, CFG.route);
        await P.rowAction(page, page.locator('tbody tr').first(), 'Lịch sử');
        await page.waitForTimeout(3000);
        await c.shotM(page, '16_history');
        c.save('_history_text.txt', await modal(page).innerText());
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
};

// Mỗi bước gỡ hết giả lập của bước trước (cùng 1 trang dùng cho mọi bước)
const wrapped = {};
for (const [k, f] of Object.entries(steps)) wrapped[k] = async (page) => { await page.unrouteAll({ behavior: 'ignoreErrors' }); await f(page); };
P.run(__dirname, wrapped).catch((e) => {
    console.error(e);
    process.exit(1);
});

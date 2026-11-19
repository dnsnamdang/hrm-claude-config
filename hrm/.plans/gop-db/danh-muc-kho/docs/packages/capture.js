// Chụp ảnh SRS + HDSD màn Danh mục kiện trên DEV (dev-hrm). Chép khuôn docs/warehouses/capture.js (màn mẫu đã duyệt),
// chỉ đổi khối CFG + các bước riêng của màn Kiện (không có Mã -> cột Tên kiện là cột mở chi tiết; ô nhập Thứ tự).
// AN TOÀN (dev dùng chung): KHÔNG bấm xác nhận Lưu / Xóa / Khóa / Mở khóa / Import.
//   Mở popup -> chụp -> Đóng / Hủy. Import chỉ Load lên bảng + Validate (Validate không ghi dữ liệu).
//   Ảnh Mở khóa / nút Khóa hiện thẳng: thiếu bản ghi phù hợp thì đổi TẠM cờ của 1 dòng trong JSON trả về trên trình duyệt.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
//   Không truyền bước = chạy mọi bước trừ probe/template/import/findhist.
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('../_capture_login.js');

const CFG = {
    route: '/warehouse/packages',
    nhom: 'Danh mục', // nhóm menu (a.cat) trong phân hệ Kho
    muc: 'Kiện', // mục trong panel nhóm
    search: 'Tìm theo tên kiện, người tạo',
    filters: [
        ['Trạng thái', 'o_trangthai'],
        ['Người tạo', 'o_nguoitao'],
        ['Người cập nhật', 'o_nguoicapnhat'],
        ['Ngày tạo', 'o_ngaytao'],
    ],
    // bản ghi dùng chụp Sửa / Xem / Lịch sử: bước `findhist` tự tìm bản ghi có lịch sử và ghi vào hdsd_shots/_hist_code.txt
    historyCode: 'Kiện 2',
    // Dev chưa có kiện nào có lịch sử -> giả lập TRÊN TRÌNH DUYỆT (như màn mẫu, user đã chấp nhận), không ghi gì vào hệ thống.
    mockHistory: [
        { id: 3, action: 'update', action_label: 'Thay đổi thông tin', action_group: 'update', action_color: '#2563eb',
          actor_id: 13, actor_dept_code: 'CTV_NV', actor_code: 'DNS01', actor_name: 'DNS Admin', department_name: 'PHÒNG CỘNG TÁC VIÊN_NV',
          note: null, changes: [{ field: 'Tên kiện', old: 'Kiện 20', new: 'Kiện 2' }, { field: 'Thứ tự', old: '20', new: '2' }],
          created_at: '26/10/2026 16:21', created_at_raw: '2026-10-26 16:21:00' },
        { id: 2, action: 'unlock', action_label: 'Mở khóa', action_group: 'status', action_color: '#16a34a',
          actor_id: 13, actor_dept_code: 'CTV_NV', actor_code: 'DNS01', actor_name: 'DNS Admin', department_name: 'PHÒNG CỘNG TÁC VIÊN_NV',
          note: null, changes: [{ field: 'Trạng thái', old: 'Khóa', new: 'Hoạt động' }],
          created_at: '20/10/2026 09:15', created_at_raw: '2026-10-20 09:15:00' },
        { id: 1, action: 'create', action_label: 'Tạo mới', action_group: 'create', action_color: '#16a34a',
          actor_id: 13, actor_dept_code: 'CTV_NV', actor_code: 'DNS01', actor_name: 'DNS Admin', department_name: 'PHÒNG CỘNG TÁC VIÊN_NV',
          note: null, changes: [], created_at: '01/10/2026 12:04', created_at_raw: '2026-10-01 12:04:00' },
    ],
    historyApi: /\/api\/v1\/catalog-histories\/packages\/\d+(\?|$)/,
    lockConfirmId: '#confirm-toggle-lock-packages',
    deleteConfirmId: '#confirm-delete-packages',
    apiList: /\/api\/v1\/master-data\/packages\?/,
    importFile: path.join(__dirname, 'hdsd_shots', 'import_test.xlsx'),
}
const SHOTS = path.join(__dirname, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
fs.mkdirSync(ICONS, { recursive: true });
const ONLY = process.argv.slice(2);
const HIST_FILE = path.join(SHOTS, '_hist_code.txt');
// findhist tìm được bản ghi CÓ lịch sử thật (02/11/2026: Kiện 3) -> dùng lịch sử thật, bỏ giả lập
if (fs.existsSync(HIST_FILE)) {
    CFG.historyCode = fs.readFileSync(HIST_FILE, 'utf8').trim();
    CFG.mockHistory = null;
}

const away = async (page) => {
    // (5,5) nằm trên thanh menu trái -> hover làm bung menu; đưa chuột ra góc phải dưới
    await page.mouse.move(1435, 895);
    await page.waitForTimeout(600);
};
const shot = async (page, name) => {
    await away(page);
    await page.screenshot({ path: path.join(SHOTS, name + '.png') });
};
// Ảnh popup / hộp xác nhận: chỉ chụp khung popup (chụp cả trang thì chữ trong popup quá nhỏ khi chèn 6 inch)
const shotM = async (page, name, loc = null) => {
    await away(page);
    const box = loc || page.locator('.modal.show:visible .modal-content').last();
    await box.screenshot({ path: path.join(SHOTS, name + '.png') });
};
const icon = async (loc, name) => {
    await loc.first().scrollIntoViewIfNeeded().catch(() => {});
    await loc.first().screenshot({ path: path.join(ICONS, name + '.png') });
};
const clipIcon = async (page, loc, name, pad = 0, maxX = null) => {
    const b = await loc.first().boundingBox();
    const x = b.x - pad;
    const y = b.y - pad;
    let w = b.width + 2 * pad;
    const h = b.height + 2 * pad;
    if (maxX !== null && x + w > maxX) w = maxX - x;
    await page.screenshot({ path: path.join(ICONS, name + '.png'), clip: { x, y, width: w, height: h } });
};
const modal = (page) => page.locator('.modal.show:visible').last();
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\-]/g, '\\$&');
async function go(page, url = CFG.route) {
    await page.goto(DEV + url);
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.locator('tbody tr').first().waitFor({ timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(2500);
}
async function closeModal(page, text = /^\s*(Đóng|Hủy)\s*$/) {
    const btn = modal(page).locator('button', { hasText: text });
    if (await btn.count()) await btn.last().click();
    else await page.keyboard.press('Escape');
    await page.waitForTimeout(1000);
}
const rowOf = (page, code) =>
    page
        .locator('tbody tr')
        .filter({ has: page.locator('button.v2-cell-link', { hasText: new RegExp('^\\s*' + esc(code) + '\\s*$') }) })
        .first();
const ff = (page, label) =>
    page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + esc(label) + '\\s*$') }) });
async function mockHistory(page) {
    if (!CFG.mockHistory) return;
    await page.route(CFG.historyApi, (route) =>
        route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ code: 200, message: 'success', data: CFG.mockHistory }) })
    );
}
const act = (row, title) => row.locator(`span[title="${title}"] button`);

async function searchCode(page, code) {
    await page.locator(`input[placeholder="${CFG.search}"]`).fill(code);
    await page.keyboard.press('Enter');
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(2500);
}

const steps = {
    /** Khảo sát: menu có mục Kiện, đủ nút, 1 trang dữ liệu + cờ nút từng dòng (chỉ đọc) */
    async probe(page) {
        let last = null;
        page.on('response', async (r) => {
            if (CFG.apiList.test(r.url())) last = await r.json().catch(() => null);
        });
        await go(page);
        console.log('URL', page.url());
        const btns = await page.locator('button').allInnerTexts();
        console.log('nút:', btns.map((s) => s.trim()).filter(Boolean).slice(0, 30).join(' | '));
        console.log('tiêu đề cột:', (await page.locator('thead th').allInnerTexts()).map((s) => s.trim()).join(' | '));
        if (last) {
            console.log('tổng:', last.meta && last.meta.total);
            for (const r of last.data || [])
                console.log(r.id, r.name, 'st', r.status, 'edit', r.is_can_edit, 'del', r.is_can_delete, 'lock', r.is_can_lock, 'unlock', r.is_can_unlock);
        }
        await page.mouse.move(40, 300);
        await page.waitForTimeout(1200);
        const cat = page.locator('a.cat', { hasText: CFG.nhom }).first();
        await cat.click();
        await page.waitForTimeout(1500);
        console.log('có mục Kiện:', await page.getByText(CFG.muc, { exact: true }).count());
    },
    async menu(page) {
        await go(page);
        await page.mouse.move(40, 300);
        await page.waitForTimeout(1200);
        await clipIcon(page, page.locator('a.logo').first(), 'menu_phanhe', 12, 218);
        const cat = page.locator('a.cat', { hasText: CFG.nhom }).first();
        await clipIcon(page, cat, 'menu_nhom', 0, 218);
        await cat.click();
        await page.waitForTimeout(1500);
        const item = page.getByText(CFG.muc, { exact: true });
        let el = null;
        for (let i = 0; i < (await item.count()); i++) {
            const b = await item.nth(i).boundingBox();
            if (b && b.x > 230) {
                el = item.nth(i);
                break;
            }
        }
        await clipIcon(page, el.locator('xpath=..'), 'menu_muc', 2);
        await page.screenshot({ path: path.join(SHOTS, '00_menu.png') });
    },
    async list(page) {
        await go(page);
        await shot(page, '01_list');
        await icon(page.locator(`input[placeholder="${CFG.search}"]`).locator('xpath=..'), 'o_timnhanh');
        await icon(page.locator('button', { hasText: 'Tìm kiếm nâng cao' }), 'btn_timkiemnangcao');
        await icon(page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(page.locator('button', { hasText: 'Làm mới' }), 'btn_lammoi');
        await icon(page.locator('button', { hasText: 'Cài đặt bộ lọc' }), 'btn_caidatboloc');
        await icon(page.locator('button', { hasText: 'Tạo mới' }), 'btn_taomoi');
        await icon(page.locator('button', { hasText: 'Import Excel' }), 'btn_import');
        await icon(page.locator('button', { hasText: 'Xuất Excel' }), 'btn_xuatexcel');
        await icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        await page.locator('button', { hasText: 'Tìm kiếm nâng cao' }).first().click();
        await page.waitForTimeout(1500);
        await shot(page, '02_filter');
        for (const [lb, nm] of CFG.filters) {
            if (await ff(page, lb).count()) await icon(ff(page, lb), nm);
            else console.log('thiếu ô lọc', lb);
        }
    },
    async rows(page) {
        // Dev chỉ có 3 kiện, cả 3 đã được dùng (không có nút Xóa) -> đổi TẠM cờ "xóa được" của 1 dòng trong JSON trả
        // về (chỉ trên trình duyệt) để chụp hộp xác nhận Xóa + menu ba chấm. Hộp xác nhận chỉ chụp rồi bấm Hủy.
        let faked = false;
        await page.route(CFG.apiList, async (route) => {
            const res = await route.fetch();
            const j = await res.json();
            if (j.data && j.data.length && !j.data.some((r) => r.is_can_delete)) {
                const r = j.data.find((x) => Number(x.status) === 1) || j.data[0];
                Object.assign(r, { is_can_delete: true });
                faked = true;
            }
            await route.fulfill({ response: res, json: j });
        });
        await go(page);
        console.log('đổi tạm 1 dòng thành "xóa được" (chỉ trình duyệt):', faked);
        // dòng đủ 4 nút: Sửa, Xóa + "…" (Khóa, Lịch sử)
        const full = page
            .locator('tbody tr')
            .filter({ has: page.locator('span[title="Xóa"]') })
            .filter({ has: page.locator('button[title="Hành động khác"]') })
            .first();
        await icon(act(full, 'Sửa'), 'btn_sua');
        await icon(act(full, 'Xóa'), 'btn_xoa');
        await icon(full.locator('button[title="Hành động khác"]'), 'btn_bacham_row');
        await full.locator('button[title="Hành động khác"]').click();
        await page.waitForTimeout(800);
        const menu = page.locator('.v2-row-actions__menu:visible').first();
        await icon(menu.locator('button[title="Khóa"]'), 'item_khoa');
        await icon(menu.locator('button[title="Lịch sử"]'), 'item_lichsu');
        await page.screenshot({ path: path.join(SHOTS, '03_rowmenu.png') });
        await menu.locator('button[title="Khóa"]').click();
        await page.waitForTimeout(1200);
        await shotM(page, '14_lock', page.locator(CFG.lockConfirmId + ' .modal-content'));
        const cm = page.locator(CFG.lockConfirmId);
        await icon(cm.locator('button', { hasText: /^\s*Khóa\s*$/ }), 'btn_confirm_khoa');
        await icon(cm.locator('button', { hasText: /^\s*Hủy\s*$/ }), 'btn_huy_confirm');
        fs.writeFileSync(path.join(SHOTS, '_lock_text.txt'), await cm.innerText());
        await cm.locator('button', { hasText: /^\s*Hủy\s*$/ }).click();
        await page.waitForTimeout(1000);
        await act(full, 'Xóa').first().click();
        await page.waitForTimeout(1200);
        await shotM(page, '13_delete', page.locator(CFG.deleteConfirmId + ' .modal-content'));
        const dm = page.locator(CFG.deleteConfirmId);
        await icon(dm.locator('button', { hasText: /^\s*Xóa\s*$/ }), 'btn_confirm_xoa');
        fs.writeFileSync(path.join(SHOTS, '_delete_text.txt'), await dm.innerText());
        await dm.locator('button', { hasText: /^\s*Hủy\s*$/ }).click();
        await page.waitForTimeout(1000);
        await page.unroute(CFG.apiList);
    },
    /** Dòng không có Xóa (kiện đã được dùng): Sửa, Khóa, Lịch sử hiện thẳng. Dev không có trang đầu nào như vậy
     *  thì đổi TẠM cờ "xóa được" của 1 dòng trong JSON trả về (chỉ trên trình duyệt) để cắt icon. */
    async plainrow(page) {
        let faked = false;
        await page.route(CFG.apiList, async (route) => {
            const res = await route.fetch();
            const j = await res.json();
            const has = (j.data || []).some((r) => Number(r.status) === 1 && !r.is_can_delete && r.is_can_lock);
            if (!has && j.data && j.data.length) {
                const r = j.data.find((x) => Number(x.status) === 1) || j.data[0];
                Object.assign(r, { is_can_delete: false });
                faked = true;
            }
            await route.fulfill({ response: res, json: j });
        });
        await go(page);
        console.log('đổi tạm 1 dòng thành "không xóa được" (chỉ trình duyệt):', faked);
        const plain = page
            .locator('tbody tr')
            .filter({ hasNot: page.locator('span[title="Xóa"]') })
            .filter({ has: page.locator('span[title="Khóa"]') })
            .first();
        await icon(act(plain, 'Khóa'), 'btn_khoa_row');
        await icon(act(plain, 'Lịch sử'), 'btn_lichsu_row');
        await page.unroute(CFG.apiList);
    },
    async unlock(page) {
        let faked = false;
        await page.route(CFG.apiList, async (route) => {
            const res = await route.fetch();
            const j = await res.json();
            if (j.data && j.data.length && !j.data.some((r) => Number(r.status) === 0)) {
                const r = j.data.find((x) => x.is_can_lock) || j.data[0];
                Object.assign(r, { status: 0, status_text: 'Khóa', is_can_edit: false, is_can_delete: false, is_can_unlock: true });
                faked = true;
            }
            await route.fulfill({ response: res, json: j });
        });
        await go(page);
        console.log('đổi tạm 1 dòng sang Khóa (chỉ trình duyệt):', faked);
        const row = page.locator('tbody tr').filter({ has: page.locator('span[title="Mở khóa"]') }).first();
        await icon(act(row, 'Mở khóa'), 'btn_mokhoa_row');
        await act(row, 'Mở khóa').first().click();
        await page.waitForTimeout(1200);
        await shotM(page, '15_unlock', page.locator(CFG.lockConfirmId + ' .modal-content'));
        const cm = page.locator(CFG.lockConfirmId);
        await icon(cm.locator('button', { hasText: /^\s*Mở khóa\s*$/ }), 'btn_confirm_mokhoa');
        fs.writeFileSync(path.join(SHOTS, '_unlock_text.txt'), await cm.innerText());
        await cm.locator('button', { hasText: /^\s*Hủy\s*$/ }).click();
        await page.waitForTimeout(800);
        await page.unroute(CFG.apiList);
    },
    async create(page) {
        await go(page);
        await page.locator('button', { hasText: 'Tạo mới' }).first().click();
        await page.waitForTimeout(1500);
        await shotM(page, '10_create');
        const m = modal(page);
        await icon(m.locator('button', { hasText: /^\s*Lưu\s*$/ }), 'btn_luu');
        await icon(m.locator('button', { hasText: 'Lưu & Tiếp tục' }), 'btn_luutieptuc');
        await icon(m.locator('button', { hasText: /^\s*Đóng\s*$/ }), 'btn_dong');
        // gõ Thứ tự bằng bàn phím: ô Tên kiện tự hiện "Kiện <thứ tự>" (KHÔNG bấm Lưu)
        // popup chỉ coi là "đã nhập" khi có thao tác thật (fill() không bắn phím)
        await m.locator('input[placeholder="Nhập thứ tự"]').click();
        await page.keyboard.type('7', { delay: 60 });
        await page.waitForTimeout(800);
        await shotM(page, '11_name_preview');
        // đóng khi đã nhập -> hộp "Thông tin chưa lưu"; Thoát = đóng không lưu
        await m.locator('button', { hasText: /^\s*Đóng\s*$/ }).click();
        await page.waitForTimeout(1200);
        await shotM(page, '18_unsaved', page.locator('.modal.show:visible').filter({ hasText: 'Thông tin chưa lưu' }).last().locator('.modal-content'));
        const um = page.locator('.modal.show:visible').filter({ hasText: 'Thông tin chưa lưu' }).last();
        fs.writeFileSync(path.join(SHOTS, '_unsaved_text.txt'), await um.innerText({ timeout: 5000 }).catch(() => 'KHÔNG HIỆN HỘP'));
        await icon(um.locator('button', { hasText: /^\s*Thoát\s*$/ }), 'btn_thoat');
        await icon(um.locator('button', { hasText: /^\s*Ở lại\s*$/ }), 'btn_olai');
        await um.locator('button', { hasText: /^\s*Thoát\s*$/ }).click();
        await page.waitForTimeout(1200);
    },
    /** Tìm bản ghi CÓ lịch sử (duyệt 3 trang đầu, mở Lịch sử từng dòng) -> ghi tên vào _hist_code.txt */
    async findhist(page) {
        await go(page);
        for (let p = 1; p <= 3; p++) {
            if (p > 1) {
                await page.locator('.pagination button, .pagination a, button', { hasText: new RegExp('^\\s*' + p + '\\s*$') }).last().click();
                await page.waitForTimeout(2500);
            }
            const n = await page.locator('tbody tr').count();
            for (let i = 0; i < n; i++) {
                const row = page.locator('tbody tr').nth(i);
                const code = (await row.locator('button.v2-cell-link').innerText()).trim();
                if (await act(row, 'Lịch sử').count()) await act(row, 'Lịch sử').first().click();
                else {
                    await row.locator('button[title="Hành động khác"]').click();
                    await page.waitForTimeout(500);
                    await page.locator('.v2-row-actions__menu:visible button[title="Lịch sử"]').first().click();
                }
                await page.waitForTimeout(2500);
                const txt = await modal(page).innerText();
                await closeModal(page, /^\s*Đóng\s*$/);
                if (!txt.includes('Chưa có lịch sử')) {
                    console.log('bản ghi có lịch sử:', code);
                    fs.writeFileSync(path.join(SHOTS, '_hist_code.txt'), code);
                    return;
                }
            }
        }
        console.log('KHÔNG tìm thấy bản ghi có lịch sử ở 3 trang đầu');
    },
    async edit(page) {
        await go(page);
        await searchCode(page, CFG.historyCode);
        await act(rowOf(page, CFG.historyCode), 'Sửa').first().click();
        await page.waitForTimeout(2500);
        await shotM(page, '12_edit');
        fs.writeFileSync(path.join(SHOTS, '_edit_text.txt'), await modal(page).innerText());
        await closeModal(page, /^\s*Đóng\s*$/);
    },
    async detail(page) {
        await mockHistory(page);
        await go(page);
        await searchCode(page, CFG.historyCode);
        await rowOf(page, CFG.historyCode).locator('button.v2-cell-link').first().click();
        await page.waitForTimeout(3500);
        await shotM(page, '17_detail');
        const xem = modal(page).locator('button', { hasText: 'Xem lịch sử' });
        if (await xem.count()) {
            await icon(xem, 'btn_xemlichsu');
            await xem.first().click();
            await page.waitForTimeout(2500);
            await shotM(page, '17b_detail_history');
        }
        fs.writeFileSync(path.join(SHOTS, '_detail_text.txt'), await modal(page).innerText());
        await closeModal(page, /^\s*Đóng\s*$/);
    },
    async history(page) {
        await mockHistory(page);
        await go(page);
        await searchCode(page, CFG.historyCode);
        const row = rowOf(page, CFG.historyCode);
        if (await act(row, 'Lịch sử').count()) await act(row, 'Lịch sử').first().click();
        else {
            await row.locator('button[title="Hành động khác"]').click();
            await page.waitForTimeout(600);
            await page.locator('.v2-row-actions__menu:visible button[title="Lịch sử"]').first().click();
        }
        await page.waitForTimeout(3500);
        await shotM(page, '16_history');
        fs.writeFileSync(path.join(SHOTS, '_history_text.txt'), await modal(page).innerText());
        await closeModal(page, /^\s*Đóng\s*$/);
    },
    async export(page) {
        await go(page);
        await page.locator('button', { hasText: 'Xuất Excel' }).first().click();
        await page.waitForTimeout(1500);
        await shotM(page, '20_export');
        const m = modal(page);
        await icon(m.locator('button', { hasText: 'Xuất file' }), 'btn_xuatfile');
        await icon(m.locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await icon(m.locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        fs.writeFileSync(path.join(SHOTS, '_export_text.txt'), await m.innerText());
        await closeModal(page, /^\s*Đóng\s*$/);
    },
    async colcfg(page) {
        await go(page);
        await page.locator('button[title="Cấu hình cột hiển thị"]').first().click();
        await page.waitForTimeout(1500);
        await shotM(page, '25_colcfg');
        fs.writeFileSync(path.join(SHOTS, '_colcfg_text.txt'), await modal(page).innerText());
        await closeModal(page, /^\s*Đóng\s*$/);
    },
    async template(page) {
        // File mẫu sinh ngay trên trình duyệt (không ghi dữ liệu) — dùng dựng file thử Import
        await go(page);
        await page.locator('button', { hasText: 'Import Excel' }).first().click();
        await page.waitForTimeout(1500);
        const [dl] = await Promise.all([
            page.waitForEvent('download'),
            modal(page).locator('button', { hasText: 'Tải file mẫu' }).click(),
        ]);
        await dl.saveAs(path.join(SHOTS, 'template.xlsx'));
        console.log('file mẫu:', dl.suggestedFilename());
        await closeModal(page, /^\s*Đóng\s*$/);
    },
    async import(page) {
        await go(page);
        await page.locator('button', { hasText: 'Import Excel' }).first().click();
        await page.waitForTimeout(1500);
        await shotM(page, '21_import_open');
        const m = modal(page);
        for (const [t, n] of [
            ['Chọn file Excel', 'btn_chonfile'],
            ['Tải file mẫu', 'btn_taifilemau'],
        ])
            await icon(m.locator('button', { hasText: t }), n);
        await m.locator('input[type=file]').setInputFiles(CFG.importFile);
        await page.waitForTimeout(1000);
        await icon(m.locator('button', { hasText: 'Load lên bảng' }), 'btn_load'); // cắt khi nút đã bấm được
        await m.locator('button', { hasText: 'Load lên bảng' }).click();
        await page.waitForTimeout(2500);
        await shotM(page, '22_import_loaded');
        await icon(m.locator('button', { hasText: /^\s*Validate\s*$/ }), 'btn_validate');
        await m.locator('button', { hasText: /^\s*Validate\s*$/ }).click();
        await page.waitForTimeout(6000);
        await shotM(page, '23_import_validated');
        fs.writeFileSync(path.join(SHOTS, '_import_text.txt'), await m.innerText());
        const bo = m.locator('button', { hasText: 'Bỏ dòng lỗi' });
        if (await bo.count()) await icon(bo, 'btn_bodongloi');
        const xv = m.locator('button', { hasText: /trạng thái validate/ });
        if (await xv.count()) await icon(xv, 'btn_xoavalidate');
        // Bỏ dòng lỗi (chỉ trên bảng xem trước) để nút Import sáng lên -> cắt icon, KHÔNG bấm
        if (await bo.count()) {
            await bo.first().click();
            await page.waitForTimeout(1200);
            await icon(m.locator('button', { hasText: /^\s*Import\s*$/ }), 'btn_import_modal');
        }
        // KHÔNG bấm Import — đóng popup
        await m.locator('button', { hasText: /^\s*Đóng\s*$/ }).last().click();
        await page.waitForTimeout(1000);
    },
};

(async () => {
    const { browser, page } = await open(__dirname);
    try {
        for (const [k, f] of Object.entries(steps)) {
            if (ONLY.length && !ONLY.includes(k)) continue;
            if (!ONLY.length && ['probe', 'template', 'import', 'findhist'].includes(k)) continue;
            console.log('==', k);
            try {
                await f(page);
            } catch (e) {
                console.log('LỖI bước', k, e.message.split('\n')[0]);
            }
        }
    } finally {
        await browser.close();
    }
})().catch((e) => {
    console.error(e);
    process.exit(1);
});

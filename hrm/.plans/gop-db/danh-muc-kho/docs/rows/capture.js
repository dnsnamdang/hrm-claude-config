// Chụp ảnh SRS + HDSD màn Danh mục dãy trên DEV (dev-hrm) — chép khuôn docs/warehouses/capture.js (màn mẫu đã duyệt),
// chỉ đổi khối CFG + các bước riêng của màn Dãy.
// AN TOÀN (dev dùng chung): KHÔNG bấm xác nhận Lưu / Xóa / Khóa / Mở khóa / Import.
//   Mở popup -> chụp -> Đóng / Hủy. Import chỉ Load lên bảng + Validate (Validate không ghi dữ liệu).
// Riêng màn Dãy: Mã dãy KHÔNG duy nhất (D1, D2… lặp ở mọi nhà kho) -> chọn dòng theo Mã + chữ trong dòng (tên nhà / kho).
//   Dev ĐÃ có dãy có lịch sử thật + dãy đang Khóa (02/11/2026) -> không giả lập lịch sử, không đổi tạm trạng thái.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
//   Không truyền bước = chạy mọi bước trừ template/import (import cần file thử dựng từ template).
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('../_capture_login.js');

const CFG = {
    route: '/warehouse/rows',
    nhom: 'Danh mục', // nhóm menu (a.cat) trong phân hệ Kho
    muc: 'Dãy', // mục trong panel nhóm
    search: 'Tìm theo mã, tên dãy',
    filters: [
        ['Công ty', 'o_congty'],
        ['Kho', 'o_kho'],
        ['Nhà kho', 'o_nhakho'],
        ['Trạng thái', 'o_trangthai'],
        ['Người tạo', 'o_nguoitao'],
        ['Ngày tạo', 'o_ngaytao'],
    ],
    // Dãy có lịch sử thật trên dev (4 mốc: Tạo mới, Khóa, Mở khóa, Khóa) — đang Khóa nên dùng luôn cho ảnh Mở khóa
    histRow: { code: 'D1', text: 'Kho Dự án trọng điểm' },
    // Dãy Hoạt động đã có khoang (popup Sửa: Số khoang chỉ đọc)
    editRow: { code: 'D2', text: 'Cát Bà' },
    // Dãy Hoạt động CHƯA có khoang (popup Sửa: phải nhập Số khoang + Số vị trí mỗi khoang)
    editRow0: { code: 'D1', text: 'Cát Bà', re: /Test\s*Cát Bà/ },
    mockHistory: null,
    historyApi: /\/api\/v1\/catalog-histories\/rows\/\d+(\?|$)/,
    lockConfirmId: '#confirm-toggle-lock-rows',
    deleteConfirmId: '#confirm-delete-rows',
    apiList: /\/api\/v1\/master-data\/rows\?/,
    importFile: path.join(__dirname, 'hdsd_shots', 'import_test.xlsx'),
}
const SHOTS = path.join(__dirname, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
fs.mkdirSync(ICONS, { recursive: true });
const ONLY = process.argv.slice(2);

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
/** Dòng theo Mã dãy + chữ trong dòng (Mã dãy lặp ở nhiều nhà kho) */
const rowOf = (page, spec) => {
    let loc = page
        .locator('tbody tr')
        .filter({ has: page.locator('button.v2-cell-link', { hasText: new RegExp('^\\s*' + esc(spec.code) + '\\s*$') }) })
        .filter({ hasText: spec.text });
    if (spec.re) loc = loc.filter({ hasText: spec.re });
    return loc.first();
};
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
        // công tắc 🔒 "Hiện cả kho đã khoá" trên nhãn ô Kho
        const tg = ff(page, 'Kho').locator('.lockable-filter-toggle');
        if (await tg.count()) await clipIcon(page, tg, 'btn_hienkhoa', 3);
        else console.log('không thấy công tắc 🔒 ô Kho');
    },
    async rows(page) {
        await go(page);
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
        // dòng không có Xóa: Khóa / Lịch sử hiện thẳng (dãy chưa có khoang nhưng đã dùng ở kiểm kê, vd N1-T2-KV)
        await searchCode(page, 'N1-T2-KV');
        const plain = page
            .locator('tbody tr')
            .filter({ hasNot: page.locator('span[title="Xóa"]') })
            .filter({ has: page.locator('span[title="Khóa"]') })
            .first();
        if (await plain.count()) {
            await icon(act(plain, 'Khóa'), 'btn_khoa_row');
            await icon(act(plain, 'Lịch sử'), 'btn_lichsu_row');
        } else console.log('không có dòng Khóa hiện thẳng');
    },
    async unlock(page) {
        // Dev có sẵn dãy đang Khóa (nhà kho Hoạt động -> có nút Mở khóa) — dùng dòng thật, không giả lập
        await go(page);
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
        fs.writeFileSync(path.join(SHOTS, '_create_text.txt'), await m.innerText({ timeout: 5000 }).catch(() => 'TREO'));
        // lỗi định dạng mã báo ngay khi gõ (KHÔNG bấm Lưu)
        // gõ bằng bàn phím: popup chỉ coi là "đã nhập" khi có thao tác thật (fill() không bắn phím)
        await m.locator('input[name="code"]').click();
        await page.keyboard.type('Dãy @01', { delay: 40 });
        await page.waitForTimeout(800);
        await shotM(page, '11_code_error');
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
    async edit(page) {
        for (const [spec, name] of [[CFG.editRow, '12_edit'], [CFG.editRow0, '12b_edit_nospace']]) {
            await go(page);
            const row = rowOf(page, spec);
            if (!(await row.count())) {
                console.log('không thấy dòng', JSON.stringify(spec));
                continue;
            }
            await act(row, 'Sửa').first().click();
            await page.waitForTimeout(2500);
            await shotM(page, name);
            fs.writeFileSync(path.join(SHOTS, '_' + name + '_text.txt'), await modal(page).innerText());
            await closeModal(page, /^\s*Đóng\s*$/);
        }
    },
    async detail(page) {
        await mockHistory(page);
        await go(page);
        await rowOf(page, CFG.histRow).locator('button.v2-cell-link').first().click();
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
        const row = rowOf(page, CFG.histRow);
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
            if (!ONLY.length && ['template', 'import'].includes(k)) continue;
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

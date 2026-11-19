// Các bước chụp phần thao tác (nạp vào capture.js). AN TOÀN: không bấm Lưu / Duyệt / Xóa / Import xác nhận.
const path = require('path');
const { forceFlags, waitList, SHOTS, LIST, SUM } = require('./capture.js');

const DETAIL_ID = Number(process.env.DETAIL_ID || 4804);

async function scrollTableRight(page) {
    await page.evaluate(() => {
        document.querySelectorAll('*').forEach((e) => {
            if (e.scrollWidth > e.clientWidth + 20 && getComputedStyle(e).overflowX !== 'visible') e.scrollLeft = 99999;
        });
    });
    await page.waitForTimeout(600);
}

async function pickSelect2(page, label, text) {
    const grp = page
        .locator('.form-group, [class*="col-"]')
        .filter({ has: page.locator('label', { hasText: new RegExp('^\\s*' + label) }) })
        .last();
    await grp.locator('.select2-selection').first().click();
    await page.waitForTimeout(700);
    await page.locator('.select2-results__option', { hasText: text }).first().click();
    await page.waitForTimeout(1200);
}

module.exports = {
    async rows(page, h, go) {
        await page.setViewportSize({ width: 1440, height: 900 });
        await forceFlags(page);
        await go(LIST);
        await waitList(page);
        await scrollTableRight(page);
        await h.full('01b_list_right');
        const ra = page.locator('.v2-row-actions').first();
        await h.icon('btn_sua_row', ra.locator('[title="Sửa"]').first());
        await h.icon('btn_xoa_row', ra.locator('[title="Xóa"]').first());
        await h.icon('btn_bacham_row', ra.locator('[title="Hành động khác"]').first());
        await ra.locator('[title="Hành động khác"]').first().click();
        await h.wait(800);
        const menu = page.locator('.v2-row-actions__menu:visible, [class*="row-actions"][class*="menu"]:visible').last();
        await h.icon('item_duyet', page.locator('button:visible, a:visible, li:visible, div[role=menuitem]:visible').filter({ hasText: /^\s*Duyệt\s*$/ }).last());
        await h.icon('item_lichsu', page.locator('button:visible, a:visible, li:visible, div[role=menuitem]:visible').filter({ hasText: /^\s*Lịch sử\s*$/ }).last());
        await page.locator('button:visible, a:visible, li:visible, div[role=menuitem]:visible').filter({ hasText: /^\s*Duyệt\s*$/ }).last().click();
        await h.wait(1200);
        let m = h.modal();
        await h.mouseOut();
        await h.el('14_approve', m, 0);
        await h.icon('btn_confirm_duyet', h.btn('Duyệt', m).last());
        await h.icon('btn_huy_confirm', h.btn('Hủy', m).first());
        await h.btn('Hủy', m).first().click();
        await h.wait(900);
        await ra.locator('[title="Xóa"]').first().locator('button, a').first().click();
        await h.wait(1200);
        m = h.modal();
        await h.mouseOut();
        await h.el('13_delete', m, 0);
        await h.icon('btn_confirm_xoa', h.btn('Xóa', m).last());
        await h.btn('Hủy', m).first().click();
        await h.wait(800);
    },
    async history(page, h, go) {
        await page.setViewportSize({ width: 1440, height: 900 });
        await go(LIST);
        await waitList(page);
        await page.locator('.v2-row-actions').nth(1).locator('[title="Lịch sử"]').first().locator('button, a').first().click();
        await h.wait(2500);
        const m = h.modal();
        await h.mouseOut();
        await h.el('16_history', m, 0);
        await h.icon('btn_boloc_ls', m.locator('button', { hasText: 'Bộ lọc' }).first());
        await h.icon('btn_dong_ls', m.locator('button', { hasText: 'Đóng' }).last());
    },
    async create(page, h, go) {
        await page.setViewportSize({ width: 1440, height: 1000 });
        await go(LIST + '/create');
        await page.locator('input[placeholder="Nhấn để chọn khách hàng"]').first().waitFor({ timeout: 30000 });
        await h.wait(2000);
        await h.full('10_create');
        await h.icon('btn_luu', h.btn('Lưu').first());
        await h.icon('btn_luuduyet', h.btn('Lưu và duyệt').first());
        await h.icon('btn_luutieptuc', h.btn('Lưu và tiếp tục').first());
        await h.icon('btn_quaylai', h.btn('Quay lại').first());
        await h.icon('btn_themdong', h.btn('Thêm dòng').first());
        await h.icon('btn_xoadong', page.locator('[title="Xóa dòng"]').first());
        // Hộp xác nhận Lưu và duyệt → chụp → Hủy
        await h.btn('Lưu và duyệt').first().click();
        await h.wait(1200);
        let m = h.modal();
        await h.mouseOut();
        await h.el('14b_saveapprove', m, 0);
        await h.icon('btn_confirm_xacnhan', m.locator('button').last());
        await h.btn('Hủy', m).first().click().catch(() => m.locator('button').first().click());
        await h.wait(1000);
        // Popup Chọn khách hàng (mở ngay trên form)
        await page.locator('input[placeholder="Nhấn để chọn khách hàng"]').first().click();
        await h.wait(3500);
        m = h.modal();
        await h.mouseOut();
        await h.el('11_customer', m, 0);
        // chọn 1 khách để nạp form (không lưu) — bỏ qua dòng KHÁCH KHÔNG RÕ
        await m.locator('tbody tr').nth(1).click();
        await h.wait(2000);
        await page.locator('input[placeholder="Nhấn để chọn hợp đồng"]').first().click();
        await h.wait(3500);
        m = h.modal();
        await h.mouseOut();
        await h.el('11b_contract', m, 0);
        await m.locator('button', { hasText: 'Đóng' }).last().click().catch(() => page.keyboard.press('Escape'));
        await h.wait(1000);
        await h.full('10a_create_filled');
        // Đổi loại thu → hộp xác nhận
        await pickSelect2(page, 'Loại thu', 'Thu nhà cung cấp');
        m = h.modal();
        if (await m.isVisible().catch(() => false)) {
            await h.mouseOut();
            await h.el('10e_changetype', m, 0);
            await m.locator('button').last().click();
            await h.wait(1500);
        }
        await h.full('10b_supplier');
        await page.locator('input[placeholder="Nhấn để chọn nhà cung cấp"]').first().click();
        await h.wait(3500);
        m = h.modal();
        await h.mouseOut();
        await h.el('11c_supplier', m, 0);
        await m.locator('button', { hasText: 'Đóng' }).last().click().catch(() => page.keyboard.press('Escape'));
        await h.wait(800);
        await pickSelect2(page, 'Loại thu', 'Thu khác');
        m = h.modal();
        if (await m.isVisible().catch(() => false)) {
            await m.locator('button').last().click();
            await h.wait(1500);
        }
        await h.full('10c_other');
    },
    async createright(page, h, go) {
        await page.setViewportSize({ width: 1440, height: 1000 });
        await go(LIST + '/create');
        await page.locator('input[placeholder="Nhấn để chọn khách hàng"]').first().waitFor({ timeout: 30000 });
        await h.wait(2000);
        await scrollTableRight(page);
        await h.mouseOut();
        const card = page.locator('.card, section, div').filter({ has: page.getByText('Thêm dòng') }).filter({ has: page.locator('table') }).last();
        await h.el('10d_create_right', card, 0);
    },
    async edit(page, h, go) {
        await page.setViewportSize({ width: 1440, height: 1000 });
        await forceFlags(page);
        await go(LIST + '/' + DETAIL_ID + '/edit');
        await page.getByText('PBC', { exact: false }).first().waitFor({ timeout: 30000 }).catch(() => {});
        await h.wait(3000);
        await h.full('12_edit');
    },
    async detail(page, h, go) {
        await page.setViewportSize({ width: 1440, height: 1000 });
        await go(LIST + '/' + DETAIL_ID);
        await page.getByText('Đánh dấu không báo tiền về').first().waitFor({ timeout: 30000 });
        await h.wait(2500);
        await h.full('17_detail');
        await h.icon('btn_taophieudc', h.btn('Tạo phiếu yêu cầu điều chỉnh công nợ').first());
        const card = page.locator('.card', { has: page.getByText('Đánh dấu không báo tiền về') }).first();
        await card.evaluate((e) => e.scrollIntoView({ block: 'center' }));
        await h.mouseOut();
        await h.clip('18_notreport', await card.boundingBox(), 0);
        const xb = h.btn('Xem lịch sử').first();
        await xb.evaluate((e) => e.scrollIntoView({ block: 'center' }));
        await h.mouseOut();
        await h.clip('btn_xemlichsu', await xb.boundingBox(), 2, path.join(SHOTS, 'icons'));
        await xb.click();
        await h.wait(2500);
        await h.full('17b_detail_history');
    },
    async draft(page, h, go) {
        await page.setViewportSize({ width: 1440, height: 1000 });
        await forceFlags(page);
        await go(LIST + '/' + DETAIL_ID);
        await page.getByText('PBC', { exact: false }).first().waitFor({ timeout: 30000 });
        await h.wait(3000);
        await h.full('17c_draft');
        await h.icon('btn_sua', h.btn('Sửa').first());
        await h.icon('btn_duyet', h.btn('Duyệt').first());
        await h.icon('btn_xoa', h.btn('Xóa').first());
    },
    async import(page, h, go) {
        await page.setViewportSize({ width: 1440, height: 900 });
        await go(LIST);
        await waitList(page);
        await h.btn('Import Excel').first().click();
        await h.wait(1500);
        const m = h.modal();
        await h.mouseOut();
        await h.el('30_import', m, 0);
        await h.icon('btn_chonfile', h.btn('Chọn file Excel', m).first());
        await h.icon('btn_taifilemau', h.btn('Tải file mẫu', m).first());
        await h.icon('btn_loadbang', h.btn('Load lên bảng', m).first());
        await h.icon('btn_validate', h.btn('Validate', m).first());
        await h.icon('btn_import_do', h.btn('Import', m).first());
        await h.icon('btn_dong_import', h.btn('Đóng', m).last());
        await h.icon('btn_lammoi_import', h.btn('Làm mới', m).last());
        await page.locator('.modal.show input[type=file]').last().setInputFiles(path.join(__dirname, 'import_test.xlsx'));
        await h.wait(1200);
        await h.btn('Load lên bảng', m).first().click();
        await h.wait(2500);
        await h.mouseOut();
        await h.el('31_import_loaded', m, 0);
        await h.btn('Validate', m).first().click();
        await h.wait(5000);
        await h.mouseOut();
        await h.el('32_import_validated', m, 0);
        await h.icon('btn_bodongloi', h.btn('Bỏ dòng lỗi', m).first());
        await h.btn('Đóng', m).last().click();
        await h.wait(800);
    },
    async summary(page, h, go) {
        await page.setViewportSize({ width: 1440, height: 900 });
        await go(SUM);
        await page.getByText('PBC', { exact: false }).first().waitFor({ timeout: 40000 });
        await h.wait(1500);
        await h.full('40_summary');
        await h.icon('btn_taomoidc', h.btn('Tạo mới điều chỉnh công nợ').first());
        await h.icon('btn_xuatexcel', h.btn('Xuất Excel').first());
        await h.icon('o_timnhanh_sum', page.locator('input[placeholder^="Tìm theo số báo có"]').first(), 2);
        await scrollTableRight(page);
        await h.full('40b_summary_right');
        const cb = page.locator('tbody input[type=checkbox], tbody .custom-checkbox, tbody .v2-checkbox').first();
        await h.icon('o_tick', cb, 3);
        await h.btn('Tìm kiếm nâng cao').first().click();
        await h.wait(1500);
        await h.mouseOut();
        await h.el('41_sumfilter', page.locator('section.smart-filter-card').first(), 0);
        await h.btn('Xuất Excel').first().click();
        await h.wait(1500);
        const m = h.modal();
        await h.mouseOut();
        await h.el('42_export', m, 0);
        await h.icon('btn_xuatfile', h.btn('Xuất file', m).first());
        await h.icon('btn_dong_export', h.btn('Đóng', m).last());
        await h.icon('btn_chontatca_x', h.btn('Chọn tất cả', m).first());
        await h.icon('btn_bochonhet_x', h.btn('Bỏ chọn hết', m).first());
        await h.btn('Đóng', m).last().click();
    },
};
module.exports.rowicon = async function (page, h, go) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await go(LIST);
    await waitList(page);
    await scrollTableRight(page);
    await h.mouseOut();
    await h.icon('btn_lichsu_row', page.locator('.v2-row-actions').first().locator('[title="Lịch sử"]').first());
};
module.exports.fixicons = async function (page, h, go) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await go(LIST + '/create');
    await page.locator('input[placeholder="Nhấn để chọn khách hàng"]').first().waitFor({ timeout: 30000 });
    await h.wait(1500);
    await h.btn('Lưu và duyệt').first().click();
    await h.wait(1200);
    let m = h.modal();
    await h.mouseOut();
    await h.icon('btn_confirm_xacnhan', h.btn('Xác nhận', m).first());
    await h.btn('Hủy', m).first().click();
    await h.wait(800);
    await go(LIST);
    await waitList(page);
    await h.btn('Import Excel').first().click();
    await h.wait(1500);
    m = h.modal();
    await page.locator('.modal.show input[type=file]').last().setInputFiles(path.join(__dirname, 'import_test.xlsx'));
    await h.wait(1000);
    await h.icon('btn_loadbang', h.btn('Load lên bảng', m).first());
    await h.btn('Load lên bảng', m).first().click();
    await h.wait(2000);
    await h.icon('btn_validate', h.btn('Validate', m).first());
    await h.btn('Validate', m).first().click();
    await h.wait(5000);
    await h.btn('Bỏ dòng lỗi', m).first().click();
    await h.wait(1500);
    await h.mouseOut();
    await h.icon('btn_import_do', h.btn('Import', m).first());
    await h.el('33_import_ready', m, 0);
    await h.btn('Đóng', m).last().click();
};

// Chụp ảnh HDSD + SRS cho STT 232 "Yêu cầu kiểm tra sửa chữa - bảo hành" trên DEV.
// Chạy: node capture.js [bước...]   (không truyền = chạy hết)
// AN TOÀN: chỉ mở form / hộp thoại rồi Đóng / Hủy — KHÔNG bấm Lưu / Xác nhận / Xóa / Từ chối.
const path = require('path');
const C = require('./cap_common');

const HERE = __dirname;
const SHOTS = path.join(HERE, 'hdsd_shots');
const BASE = 'warranty-repair-requests';
const LIST = '/customer-care/warranty-repair-requests?type=all';
// Phiếu thật mới nhất trên dev (đọc qua API chi tiết)
const IDS = [7079, 7078, 7076, 7075, 7074, 7073, 7072, 7071, 7070, 7069];
const ID_WAIT = 7079; // Chờ xử lý — đủ 3 nút của phòng tiếp nhận
const ID_HIST = 7075; // từng bị từ chối -> có lịch sử nhiều mốc
const ID_DRAFT = 7074; // dùng để bật tạm hiển thị Sửa / Xóa (giả lập phiếu Đang tạo của mình)
const DRAFT = { status: 1, status_text: 'Đang tạo', status_color: '#64748B', is_can_edit: true, is_can_delete: true,
    is_can_handle_request: false, is_can_transfer_department: false, is_can_reject: false };

const steps = process.argv.slice(2);
const want = (s) => !steps.length || steps.includes(s);

async function openList(r) {
    await r.page.goto(C.DEV + LIST);
    await r.page.getByText('TPE.YCSCBH.26.007079').first().waitFor({ timeout: 60000 });
    await C.settle(r.page);
}

async function closeModal(page) {
    const m = page.locator('.modal.show').last();
    const btn = C.btn(m, /^(Đóng|Hủy)$/).last();
    if (await btn.count()) await btn.click().catch(() => {});
    else await page.keyboard.press('Escape');
    await page.waitForTimeout(800);
}

(async () => {
    const r = await C.start(HERE, SHOTS);
    const { page } = r;
    await C.mockList(r, BASE, IDS);

    if (want('list')) {
        await openList(r);
        await C.shot(r, '01_list');
        await C.icon(r, page.locator('input[placeholder^="Tìm theo mã phiếu"]').locator('xpath=..'), 'o_timnhanh');
        await C.icon(r, C.btn(page, 'Tìm kiếm'), 'btn_timkiem');
        await C.icon(r, C.btn(page, 'Làm mới'), 'btn_lammoi');
        await C.icon(r, C.btn(page, 'Tìm kiếm nâng cao'), 'btn_timkiemnangcao');
        await C.icon(r, C.btn(page, 'Cài đặt bộ lọc'), 'btn_caidatboloc');
        await C.icon(r, C.btn(page, 'Tạo mới'), 'btn_taomoi');
        await C.icon(r, C.btn(page, 'Xuất Excel'), 'btn_xuatexcel');
        await C.icon(r, C.btn(page, 'In danh sách'), 'btn_in_list');
        await C.icon(r, page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        // Cột Hành động: dòng Đang tạo (bật tạm) có Sửa / Xóa; dòng Chờ xử lý có nút phòng tiếp nhận
        const rowWait = page.locator('tr', { hasText: 'TPE.YCSCBH.26.007079' });
        await C.icon(r, rowWait.locator('[title="Tạo phiếu xử lý yêu cầu"]'), 'btn_xuly_row');
        await C.icon(r, rowWait.locator('[title="Chuyển phòng tiếp nhận"]'), 'btn_chuyenphong_row');
        const rowDone = page.locator('tr', { hasText: 'TPE.YCSCBH.26.007076' });
        await C.icon(r, rowDone.locator('[title="In"]'), 'btn_in_row');
        await C.icon(r, rowDone.locator('[title="Lịch sử"]'), 'btn_lichsu_row');
        await C.icon(r, rowWait.locator('td').last(), 'cell_actions_wait');
        // Menu "Hành động khác" của dòng Chờ xử lý
        const dots = rowWait.locator('[title="Hành động khác"]');
        await C.icon(r, dots, 'btn_bacham_row');
        await dots.first().click();
        await page.waitForTimeout(800);
        const menu = page.locator('.v2-row-actions__menu:visible').last();
        await C.shot(r, '03_rowmenu', menu);
        await C.icon(r, menu.locator('.v2-row-actions__item', { hasText: 'Từ chối' }), 'item_tuchoi');
        await C.icon(r, menu.locator('.v2-row-actions__item', { hasText: /^\s*In\s*$/ }), 'item_in');
        await C.icon(r, menu.locator('.v2-row-actions__item', { hasText: 'Lịch sử' }), 'item_lichsu');
        await page.keyboard.press('Escape');
        await C.settle(page, 500);
    }

    if (want('menu')) {
        // Icon menu: rê chuột vào thanh bên để bung menu phân hệ
        await openList(r);
        await page.mouse.move(25, 400);
        await page.waitForTimeout(1500);
        await C.icon(r, page.locator(':visible').filter({ hasText: /^\s*CSKH SAU BÁN\s*$/i }).last(), 'menu_phanhe');
        const nhom = page.locator('a:visible, li:visible > div:visible, .menu-item:visible')
            .filter({ hasText: /^\s*Kiểm tra bảo hành s/ }).last();
        await C.icon(r, nhom, 'menu_nhom');
        await nhom.click().catch(() => {});
        await page.waitForTimeout(1000);
        await page.mouse.move(25, 400);
        await page.waitForTimeout(800);
        await C.icon(r, page.locator('a:visible').filter({ hasText: /^\s*Yêu cầu kiểm tra sửa chữa - bảo hành\s*$/ }).last(), 'menu_muc');
        await C.icon(r, page.locator('a:visible').filter({ hasText: /^\s*Phiếu xử lý yêu cầu\s*$/ }).last(), 'menu_muc_233');
        await page.screenshot({ path: path.join(SHOTS, '00_menu_debug.png') });
    }

    if (want('filter')) {
        await openList(r);
        await C.btn(page, 'Tìm kiếm nâng cao').click();
        await C.settle(page, 1500);
        await C.shot(r, '02_filter');
        const panel = page.locator('.v2-smart-filter-panel, .smart-filter-panel').first();
        for (const [lb, nm] of [['Trạng thái', 'o_trangthai'], ['Khách hàng', 'o_khachhang'], ['Tên thiết bị', 'o_tenthietbi'],
            ['Người yêu cầu', 'o_nguoiyeucau'], ['Tỉnh/TP', 'o_tinhtp'], ['Ngày yêu cầu', 'o_ngayyeucau']]) {
            await C.fieldIcon(r, lb, nm);
        }
    }

    if (want('cfg')) {
        await openList(r);
        await C.btn(page, 'Cài đặt bộ lọc').click();
        await page.waitForTimeout(1500);
        const m1 = C.lastModal(page);
        await C.shot(r, '26_filtercfg', m1);
        await C.icon(r, C.btn(m1, 'Lưu'), 'btn_luu');
        await C.icon(r, C.btn(m1, /Khôi phục/), 'btn_khoiphuc');
        await C.icon(r, C.btn(m1, 'Đóng'), 'btn_dong_filtercfg');
        await closeModal(page);
        await page.locator('button[title="Cấu hình cột hiển thị"]').click();
        await page.waitForTimeout(1500);
        const m2 = C.lastModal(page);
        await C.shot(r, '25_colcfg', m2);
        await C.icon(r, C.btn(m2, 'Chọn tất cả'), 'btn_chontatca');
        await C.icon(r, C.btn(m2, 'Bỏ chọn hết'), 'btn_bochonhet');
        await C.icon(r, C.btn(m2, 'Lưu'), 'btn_luu_col');
        await C.icon(r, C.btn(m2, 'Đóng'), 'btn_dong_col');
        await closeModal(page);
        await C.btn(page, 'Xuất Excel').click();
        await page.waitForTimeout(1500);
        const m3 = C.lastModal(page);
        await C.shot(r, '20_export', m3);
        await C.icon(r, C.btn(m3, /Xuất file/), 'btn_xuatfile');
        await C.icon(r, C.btn(m3, 'Đóng'), 'btn_dong_export');
        await closeModal(page);
    }

    if (want('create')) {
        await page.goto(C.DEV + '/customer-care/warranty-repair-requests/create');
        await C.settle(page, 3500);
        await C.shot(r, '10_create', null, { full: true });
        await C.icon(r, C.btn(page, 'Lưu nháp'), 'btn_luunhap');
        await C.icon(r, C.btn(page, 'Lưu và tiếp tục'), 'btn_luutieptuc');
        await C.icon(r, C.btn(page, 'Lưu và gửi'), 'btn_luugui');
        await C.icon(r, C.btn(page, 'Quay lại'), 'btn_quaylai');
        // Ô Khách hàng -> cửa sổ Chọn khách hàng (modal dùng chung)
        const kh = page.locator('input[placeholder*="khách hàng" i], .customer-picker, [title*="Chọn khách"]').first();
        await C.icon(r, kh, 'o_khachhang_form');
        await kh.click().catch(() => {});
        await page.waitForTimeout(2500);
        const mk = C.lastModal(page);
        if (await mk.count()) {
            await C.shot(r, '11_customer', mk);
            await closeModal(page);
        }
    }

    if (want('edit')) {
        await C.patchDetail(r, BASE, ID_DRAFT, DRAFT);
        await page.goto(C.DEV + `/customer-care/warranty-repair-requests/${ID_DRAFT}/edit`);
        await page.getByText('TPE.YCSCBH.26.007074').first().waitFor({ timeout: 60000 }).catch(() => {});
        await C.settle(page, 3000);
        await C.shot(r, '12_edit', null, { full: true });
        // Chi tiết với cờ bật tạm: nút Sửa / Xóa ở thanh nút
        await page.goto(C.DEV + `/customer-care/warranty-repair-requests/${ID_DRAFT}`);
        await C.settle(page, 3000);
        await C.icon(r, C.btn(page, 'Sửa'), 'btn_sua');
        await C.icon(r, C.btn(page, 'Xóa'), 'btn_xoa');
        // Hộp xác nhận xóa (bấm Hủy) — bật tạm dòng 7074 thành phiếu Đang tạo của mình
        r.listRows = r.listRows.map((x) => (x.id === ID_DRAFT ? Object.assign({}, x, DRAFT) : x));
        await openList(r);
        const rowDraft = page.locator('tr', { hasText: 'TPE.YCSCBH.26.007074' });
        await C.icon(r, rowDraft.locator('[title="Sửa"]'), 'btn_sua_row');
        await C.icon(r, rowDraft.locator('[title="Xóa"]'), 'btn_xoa_row');
        await page.locator('tr', { hasText: 'TPE.YCSCBH.26.007074' }).locator('[title="Xóa"]').first().click();
        await page.waitForTimeout(1200);
        const md = C.lastModal(page);
        await C.shot(r, '13_delete', md);
        await C.icon(r, C.btn(md, 'Xóa'), 'btn_confirm_xoa');
        await C.icon(r, C.btn(md, 'Hủy'), 'btn_huy_confirm');
        await C.btn(md, 'Hủy').click();
        await page.waitForTimeout(800);
    }

    if (want('detail')) {
        await page.goto(C.DEV + `/customer-care/warranty-repair-requests/${ID_WAIT}`);
        await page.getByText('TPE.YCSCBH.26.007079').first().waitFor({ timeout: 60000 }).catch(() => {});
        await C.settle(page, 3000);
        await C.shot(r, '17_detail');
        await C.icon(r, C.btn(page, 'Tạo phiếu xử lý yêu cầu'), 'btn_xuly');
        await C.icon(r, C.btn(page, 'Chuyển phòng tiếp nhận'), 'btn_chuyenphong');
        await C.icon(r, C.btn(page, 'Từ chối'), 'btn_tuchoi');
        await C.icon(r, C.btn(page, 'In'), 'btn_in');
        await C.icon(r, C.btn(page, 'Quay lại'), 'btn_quaylai_ct');
        const footer = page.locator('.v2-footer, footer').last();
        await C.shot(r, '21_footer_wait', footer).catch(() => {});
        // Chuyển phòng tiếp nhận (Đóng)
        await C.btn(page, 'Chuyển phòng tiếp nhận').click();
        await page.waitForTimeout(1500);
        const mt = C.lastModal(page);
        await C.shot(r, '14_transfer', mt);
        await C.icon(r, C.btn(mt, 'Xác nhận'), 'btn_confirm_chuyen');
        await C.icon(r, C.btn(mt, 'Đóng'), 'btn_dong_modal');
        await closeModal(page);
        // Từ chối (Đóng)
        await C.btn(page, 'Từ chối').click();
        await page.waitForTimeout(1500);
        const mr = C.lastModal(page);
        await C.shot(r, '15_reject', mr);
        await C.icon(r, C.btn(mr, 'Từ chối'), 'btn_confirm_tuchoi');
        await closeModal(page);
        // In phiếu
        await C.btn(page, 'In').click();
        await page.waitForTimeout(4000);
        const mp = C.lastModal(page);
        await C.shot(r, '18_print', mp);
        await C.icon(r, C.btn(mp, /^In$/), 'btn_in_preview');
        await closeModal(page);
    }

    if (want('history')) {
        await page.goto(C.DEV + `/customer-care/warranty-repair-requests/${ID_HIST}`);
        await C.settle(page, 3000);
        const xem = C.btn(page, /Xem lịch sử/);
        await C.icon(r, xem, 'btn_xemlichsu');
        await xem.first().click().catch(() => {});
        await C.settle(page, 2500);
        const sec = page.locator('text=Lịch sử').last().locator('xpath=ancestor::div[contains(@class,"card") or contains(@class,"section")][1]');
        await C.shot(r, '16b_history_detail', sec).catch(() => {});
        await openList(r);
        await page.locator('tr', { hasText: 'TPE.YCSCBH.26.007075' }).locator('[title="Hành động khác"]').first().click();
        await page.waitForTimeout(800);
        await page.locator('.v2-row-actions__menu:visible').last().locator('.v2-row-actions__item', { hasText: 'Lịch sử' }).click();
        await page.waitForTimeout(3000);
        const mh = C.lastModal(page);
        await C.shot(r, '16_history', mh);
        await C.icon(r, C.btn(mh, /Bộ lọc/), 'btn_boloc_ls');
        await C.icon(r, C.btn(mh, 'Đóng'), 'btn_dong_ls');
        await closeModal(page);
    }

    if (want('printlist')) {
        await openList(r);
        await C.btn(page, 'In danh sách').click();
        await page.waitForTimeout(5000);
        await C.shot(r, '19_printlist', C.lastModal(page));
        await closeModal(page);
    }

    await r.browser.close();
})().catch((e) => {
    console.error(e);
    process.exit(1);
});

// Chụp ảnh HDSD + SRS cho STT 233 "Phiếu xử lý yêu cầu" trên DEV.
// Chạy: node capture.js [bước...]   (không truyền = chạy hết). Hàm chung: ../../warranty-repair-request/form_qg_232/cap_common.js
// AN TOÀN: chỉ mở form / hộp thoại rồi Đóng / Hủy — KHÔNG bấm Lưu / Xác nhận / Xóa / Không duyệt.
const path = require('path');
const C = require('../../warranty-repair-request/form_qg_232/cap_common');

const HERE = __dirname;
const SHOTS = path.join(HERE, 'hdsd_shots');
const BASE = 'warranty-repair-handle-requests';
const LIST = '/customer-care/warranty-repair-handle-requests?type=all';
const IDS = [6619, 6618, 6617, 6616, 6615, 6614, 6613, 6612, 6572, 6571];
const ID = 6619;
const SRC_REQ = 7079; // phiếu yêu cầu Chờ xử lý -> mở màn Tạo phiếu xử lý (không lưu)
const DRAFT = { status: 1, status_text: 'Đang tạo', status_color: '#64748B', is_can_edit: true, is_can_delete: true,
    is_can_create_information: false, is_can_reject: false };
const WAIT = { status: 2, status_text: 'Chờ CCTT', status_color: '#D97706', is_can_edit: false, is_can_delete: false,
    is_can_create_information: true, is_can_reject: true };

const steps = process.argv.slice(2);
const want = (s) => !steps.length || steps.includes(s);

async function openList(r) {
    await r.page.goto(C.DEV + LIST);
    await r.page.getByText('TPE.PXL.2026006619').first().waitFor({ timeout: 60000 });
    await C.settle(r.page);
}

async function closeModal(page) {
    const m = page.locator('.modal.show').last();
    const b = C.btn(m, /^\s*(Đóng|Hủy)\s*$/).last();
    if (await b.count()) await b.click().catch(() => {});
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
        await C.icon(r, page.locator('input[placeholder^="Tìm theo số phiếu"]').locator('xpath=..'), 'o_timnhanh');
        await C.icon(r, C.btn(page, 'Tìm kiếm'), 'btn_timkiem');
        await C.icon(r, C.btn(page, 'Làm mới'), 'btn_lammoi');
        await C.icon(r, C.btn(page, 'Tìm kiếm nâng cao'), 'btn_timkiemnangcao');
        await C.icon(r, C.btn(page, 'Cài đặt bộ lọc'), 'btn_caidatboloc');
        await C.icon(r, C.btn(page, 'Xuất Excel'), 'btn_xuatexcel');
        await C.icon(r, C.btn(page, 'In danh sách'), 'btn_in_list');
        await C.icon(r, page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        const row = page.locator('tr', { hasText: 'TPE.PXL.2026006618' });
        await C.icon(r, row.locator('[title="In"]'), 'btn_in_row');
        await C.icon(r, row.locator('[title="Lịch sử"]'), 'btn_lichsu_row');
        const orig = r.listRows.slice();
        // Dòng Chờ CCTT (bật tạm): Tạo phiếu CCTT + menu Hành động khác (Không duyệt / In / Lịch sử)
        r.listRows = r.listRows.map((x) => (x.id === ID ? Object.assign({}, x, WAIT) : x));
        await openList(r);
        const rw = page.locator('tr', { hasText: 'TPE.PXL.2026006619' });
        await C.icon(r, rw.locator('[title="Tạo phiếu cung cấp thông tin"]'), 'btn_cctt_row');
        await C.icon(r, rw.locator('[title="Không duyệt"]'), 'btn_khongduyet_row');
        const dots = rw.locator('[title="Hành động khác"]');
        await C.icon(r, dots, 'btn_bacham_row');
        await dots.first().click();
        await page.waitForTimeout(800);
        const menu = page.locator('.v2-row-actions__menu:visible').last();
        await C.shot(r, '03_rowmenu', menu);
        await C.icon(r, menu.locator('.v2-row-actions__item', { hasText: /^\s*In\s*$/ }), 'item_in');
        await C.icon(r, menu.locator('.v2-row-actions__item', { hasText: 'Lịch sử' }), 'item_lichsu');
        // Dòng Đang tạo (bật tạm): Sửa / Xóa + hộp xác nhận xóa (bấm Hủy)
        r.listRows = r.listRows.map((x) => (x.id === ID ? Object.assign({}, x, DRAFT) : x));
        await openList(r);
        const rd = page.locator('tr', { hasText: 'TPE.PXL.2026006619' });
        await C.icon(r, rd.locator('[title="Sửa"]'), 'btn_sua_row');
        await C.icon(r, rd.locator('[title="Xóa"]'), 'btn_xoa_row');
        await rd.locator('[title="Xóa"]').first().click();
        await page.waitForTimeout(1200);
        const md = C.lastModal(page);
        await C.shot(r, '13_delete', md);
        await C.icon(r, C.btn(md, 'Xóa'), 'btn_confirm_xoa');
        await C.icon(r, C.btn(md, 'Hủy'), 'btn_huy_confirm');
        await C.btn(md, 'Hủy').click();
        await page.waitForTimeout(800);
        r.listRows = orig;
    }

    if (want('filter')) {
        await openList(r);
        await C.btn(page, 'Tìm kiếm nâng cao').click();
        await C.settle(page, 1500);
        await C.shot(r, '02_filter');
        for (const [lb, nm] of [['Trạng thái', 'o_trangthai'], ['Số phiếu yêu cầu', 'o_sophieuyc'], ['Khách hàng', 'o_khachhang'],
            ['Tên thiết bị', 'o_tenthietbi'], ['Model', 'o_model'], ['Ngày tạo', 'o_ngaytao']]) {
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
        await C.btn(page, 'In danh sách').click();
        await page.waitForTimeout(5000);
        await C.shot(r, '19_printlist', C.lastModal(page));
        await closeModal(page);
    }

    if (want('create')) {
        // Màn Tạo phiếu xử lý mở từ phiếu yêu cầu Chờ xử lý (nút "Tạo phiếu xử lý yêu cầu" của STT 232)
        await page.goto(C.DEV + `/customer-care/warranty-repair-requests/${SRC_REQ}`);
        await C.settle(page, 3000);
        await C.icon(r, C.btn(page, 'Tạo phiếu xử lý yêu cầu'), 'btn_xuly');
        await C.btn(page, 'Tạo phiếu xử lý yêu cầu').click();
        await page.waitForURL(/warranty-repair-handle-requests\/create/, { timeout: 60000 });
        await C.settle(page, 4000);
        await C.shot(r, '10_create', null, { full: true });
        await C.icon(r, C.btn(page, 'Lưu nháp'), 'btn_luunhap');
        await C.icon(r, C.btn(page, 'Lưu và gửi'), 'btn_luugui');
        await C.icon(r, C.btn(page, 'Quay lại'), 'btn_quaylai');
        const qa = page.locator('button:visible, a:visible').filter({ hasText: 'Thêm nhanh lỗi thiết bị' }).first();
        await C.icon(r, qa, 'btn_themnhanh');
        await C.icon(r, page.locator('.select2-container:visible').filter({ hasText: /Chọn nguyên nhân/ }), 'o_nguyennhan');
        await C.icon(r, page.locator('.select2-container:visible').filter({ hasText: /Chọn hành động/ }), 'o_hanhdong');
        await qa.click();
        await page.waitForTimeout(1500);
        const mq = C.lastModal(page);
        await C.shot(r, '11_quickadd', mq);
        await C.icon(r, C.btn(mq, 'Lưu'), 'btn_luu_qa');
        await C.icon(r, C.btn(mq, 'Đóng'), 'btn_dong_modal');
        await closeModal(page);
    }

    if (want('edit')) {
        await C.patchDetail(r, BASE, ID, DRAFT);
        await page.goto(C.DEV + `/customer-care/warranty-repair-handle-requests/${ID}/edit`);
        await page.getByText('TPE.PXL.2026006619').first().waitFor({ timeout: 60000 }).catch(() => {});
        await C.settle(page, 3500);
        await C.shot(r, '12_edit', null, { full: true });
        await page.goto(C.DEV + `/customer-care/warranty-repair-handle-requests/${ID}`);
        await C.settle(page, 3000);
        await C.icon(r, C.btn(page, 'Sửa'), 'btn_sua');
        await C.icon(r, C.btn(page, 'Xóa'), 'btn_xoa');
        await page.unroute(new RegExp(`/api/v1/customer-care/${BASE}/${ID}(\\?|$)`));
    }

    if (want('detail')) {
        await page.goto(C.DEV + `/customer-care/warranty-repair-handle-requests/${ID}`);
        await page.getByText('TPE.PXL.2026006619').first().waitFor({ timeout: 60000 }).catch(() => {});
        await C.settle(page, 3000);
        await C.shot(r, '17_detail');
        await C.icon(r, C.btn(page, 'In'), 'btn_in');
        await C.btn(page, 'In').click();
        await page.waitForTimeout(4000);
        await C.shot(r, '18_print', C.lastModal(page));
        await closeModal(page);
        // Chi tiết phiếu Chờ CCTT (bật tạm nút): Tạo phiếu CCTT + Không duyệt
        await C.patchDetail(r, BASE, ID, WAIT);
        await page.goto(C.DEV + `/customer-care/warranty-repair-handle-requests/${ID}`);
        await C.settle(page, 3000);
        await C.shot(r, '14_wait_detail');
        await C.icon(r, C.btn(page, 'Tạo phiếu cung cấp thông tin'), 'btn_cctt');
        await C.icon(r, C.btn(page, 'Không duyệt'), 'btn_khongduyet');
        await C.btn(page, 'Không duyệt').click();
        await page.waitForTimeout(1500);
        const mr = C.lastModal(page);
        await C.shot(r, '15_reject', mr);
        await C.icon(r, C.btn(mr, 'Không duyệt'), 'btn_confirm_khongduyet');
        await C.icon(r, C.btn(mr, 'Đóng'), 'btn_dong_reject');
        await closeModal(page);
    }

    await r.browser.close();
})().catch((e) => {
    console.error(e);
    process.exit(1);
});

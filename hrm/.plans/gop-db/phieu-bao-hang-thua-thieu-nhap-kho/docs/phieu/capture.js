// Chụp ảnh SRS + HDSD màn "Phiếu báo hàng thừa, thiếu nhập kho" (STT 289) trên DEV — khuôn màn mẫu phiếu
// finance-declare-debt-beginning/docs/kh/capture.js; hàm chung ../../../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js.
// AN TOÀN (dev dùng chung): KHÔNG bấm Lưu / Lưu và gửi / Lưu và tiếp tục / Xóa / Không duyệt (xác nhận) / Xử lý.
//   - Form Thêm: chọn PNK qua popup (chỉ đọc), Diễn giải + file đính kèm ĐIỀN TẠM trên trình duyệt (KHÔNG chọn file thật
//     vì chọn file là tải ngay lên kho lưu trữ) -> Quay lại -> Thoát.
//   - Hộp Xác nhận xóa: chụp -> Hủy. Popup Không duyệt: bấm "Không duyệt" khi ô trống (chỉ báo đỏ, không gửi) -> Hủy.
//   - Dev không có phiếu Không duyệt -> ảnh 17d_detail_rejected GIẢ LẬP (sửa dữ liệu trả về ngay trên trình duyệt).
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const P = require('../../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js');

const CFG = {
    route: '/warehouse/exc-shortage-imports',
    nhom: 'Nhập kho',
    muc: 'Phiếu báo hàng thừa, thiếu nhập kho',
    search: 'Tìm theo số phiếu',
    filters: [
        ['Phiếu nhập kho', 'o_pnk'],
        ['Yêu cầu nhập', 'o_ycn'],
        ['Hợp đồng', 'o_hopdong'],
        ['Hàng hóa', 'o_hanghoa'],
        ['Nhà cung cấp', 'o_ncc'],
        ['Trạng thái', 'o_trangthai'],
        ['Người tạo', 'o_nguoitao'],
        ['Ngày tạo', 'o_ngaytao'],
        ['Công ty', 'o_congty'],
    ],
    // dò dev 18/11/2026 (probe.js): 20 = Đang tạo của tài khoản dev (có Sửa/Xóa, có 2 mốc lịch sử), 21 = Chờ xử lý
    draftId: 20, draftCode: 'TPE_BHNK-00020',
    waitId: 21, waitCode: 'TPE_BHNK-00021',
    doneCode: 'TPE_BHNK-00019',
    detailApi: /\/api\/v1\/finance\/exc-shortage-imports\/20(\?|$)/,
};
const c = P.ctx(__dirname);
const { go, btn, modal } = P;

async function scrollRight(page) {
    await page.evaluate(() => document.querySelectorAll('*').forEach((el) => {
        if (el.scrollWidth > el.clientWidth + 50 && el.querySelector && el.querySelector('table')) el.scrollLeft = el.scrollWidth;
    }));
    await page.waitForTimeout(800);
}

const steps = {
    async menu(page) {
        await P.menuIcons(page, c, CFG.nhom, CFG.muc, CFG.route);
    },
    async list(page) {
        await go(page, CFG.route);
        await c.shot(page, '01_list');
        c.save('_list_text.txt', await page.locator('table').first().innerText());
        await c.icon(page.locator(`input[placeholder="${CFG.search}"]`).locator('xpath=..'), 'o_timnhanh');
        for (const [t, n] of [['Tìm kiếm nâng cao', 'btn_timkiemnangcao'], ['Tìm kiếm', 'btn_timkiem'], ['Làm mới', 'btn_lammoi'],
            ['Cài đặt bộ lọc', 'btn_caidatboloc'], ['Tạo mới', 'btn_taomoi'], ['Xuất Excel', 'btn_xuatexcel']])
            await c.icon(btn(page, t), n);
        await c.icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot');
        await btn(page, 'Tìm kiếm nâng cao').first().click();
        await page.waitForTimeout(2500);
        await c.shot(page, '02_filter');
        for (const [lb, nm] of CFG.filters) {
            if (await P.ff(page, lb).count()) await c.icon(P.ff(page, lb), nm);
            else console.log('  thiếu ô lọc', lb);
        }
        c.save('_filter_text.txt', await page.locator('.ff').allInnerTexts().then((a) => a.join('\n')));
        await go(page, CFG.route);
        await scrollRight(page);
        await c.shot(page, '01b_list_actions');
    },
    async rows(page) {
        await go(page, CFG.route);
        await scrollRight(page);
        const draft = P.rowOf(page, CFG.draftCode);
        const wait = P.rowOf(page, CFG.waitCode);
        await c.icon(P.act(draft, 'Sửa'), 'btn_sua');
        await c.icon(P.act(draft, 'Xóa'), 'btn_xoa');
        await c.icon(P.act(draft, 'Lịch sử'), 'btn_lichsu_row');
        await c.icon(P.act(wait, 'Xử lý'), 'btn_xuly');
        c.save('_rows_text.txt', 'draft: ' + (await draft.innerText()) + '\nwait: ' + (await wait.innerText()) +
            '\ndraft actions: ' + (await draft.locator('span[title]').evaluateAll((a) => a.map((x) => x.title)).catch(() => [])) +
            '\nwait actions: ' + (await wait.locator('span[title]').evaluateAll((a) => a.map((x) => x.title)).catch(() => [])));
        await P.rowAction(page, draft, 'Xóa');
        await P.confirmShot(page, c, '13_delete', 'Xác nhận xóa', { 'Xóa': 'btn_confirm_xoa', 'Hủy': 'btn_huy_confirm' }, 'Hủy');
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
        const m = modal(page);
        c.save('_colcfg_text.txt', await m.innerText());
        await c.icon(m.locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await c.icon(m.locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        await P.closeModal(page, /^\s*(Đóng|Hủy)\s*$/);
    },
    async export(page) {
        await go(page, CFG.route);
        await btn(page, 'Xuất Excel').first().click();
        await page.waitForTimeout(1500);
        await c.shotM(page, '20_export');
        const m = modal(page);
        await c.icon(m.locator('button', { hasText: 'Xuất file' }), 'btn_xuatfile');
        c.save('_export_text.txt', await m.innerText());
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async history(page) {
        await go(page, CFG.route);
        await P.rowAction(page, P.rowOf(page, CFG.draftCode), 'Lịch sử');
        await page.waitForTimeout(3000);
        await c.shotM(page, '16_history');
        c.save('_history_text.txt', await modal(page).innerText());
        await P.closeModal(page, /^\s*Đóng\s*$/);
    },
    async create(page) {
        await go(page, CFG.route + '/create', false);
        await page.waitForTimeout(2000);
        await c.shot(page, '10_create', true);
        c.save('_create_text.txt', await page.locator('.exc-form').innerText());
        for (const [t, n] of [['Lưu', 'btn_luu'], ['Lưu và gửi', 'btn_luugui'], ['Lưu và tiếp tục', 'btn_luutieptuc'], ['Quay lại', 'btn_quaylai'],
            ['Thêm tài liệu', 'btn_themtailieu']])
            await c.icon(btn(page, t), n);
        await c.icon(page.locator('.v2-picker-input'), 'o_chonpnk');
        // Bấm Lưu khi chưa nhập gì: kiểm tra ngay trên trình duyệt, KHÔNG gửi gì đi
        await btn(page, 'Lưu').first().click();
        await page.waitForTimeout(1200);
        await c.shot(page, '11_validate', true);
        c.save('_validate_text.txt', await page.locator('.exc-form').innerText());
        // Popup chọn phiếu nhập kho (chỉ đọc) — mở lại trang trống để không dính lỗi đỏ của bước trên
        await go(page, CFG.route + '/create', false);
        await page.waitForTimeout(2000);
        await page.locator('.v2-picker-input').first().click();
        await page.locator('.modal.show:visible tbody tr').first().waitFor({ timeout: 30000 });
        await page.waitForTimeout(2500);
        await c.shotM(page, '14_picker');
        const m = modal(page);
        c.save('_picker_text.txt', await m.innerText());
        // bấm ô Loại (không phải ô Mã phiếu — ô đó mở phiếu nhập kho ở tab mới)
        await m.locator('tbody tr').first().locator('td').nth(2).click();
        await page.waitForTimeout(3500);
        // điền tạm Diễn giải + 1 file giả (KHÔNG tải file thật lên)
        await page.evaluate(() => {
            const vm = document.querySelector('.exc-form').__vue__;
            vm.form.note = 'Hàng về thiếu so với đề nghị nhập, đề nghị phòng mua hàng làm việc với nhà cung cấp.';
            vm.pendingFiles.push({ url: 'https://tanphat.s3.cloud.cmctelecom.vn/delivery_international_general/bien-ban-kiem-dem.pdf', name: 'bien-ban-kiem-dem.pdf', size: 245760 });
            window.scrollTo(0, 0);
        });
        await page.waitForTimeout(1500);
        await c.shot(page, '10b_create_filled', true);
        c.save('_create_filled_text.txt', await page.locator('.exc-form').innerText());
        await P.leaveUnsaved(page, c, '18_unsaved');
    },
    async detail(page) {
        // Chờ xử lý: có Xử lý, Không duyệt
        await go(page, CFG.route + '/' + CFG.waitId, false);
        await page.waitForTimeout(2500);
        await c.shot(page, '17_detail', true);
        c.save('_detail_text.txt', await page.locator('.exc-form').innerText());
        await c.icon(btn(page, 'Xử lý'), 'btn_xuly_footer');
        await c.icon(btn(page, 'Không duyệt'), 'btn_khongduyet');
        await c.icon(page.locator('.si-header-right button').last(), 'btn_xemlichsu');
        // popup Không duyệt: bấm Không duyệt khi chưa nhập lý do (chỉ báo đỏ trên trình duyệt), rồi Hủy
        await btn(page, 'Không duyệt').first().click();
        await page.waitForTimeout(1500);
        await c.shotM(page, '15_reject');
        const m = modal(page);
        await btn(m, 'Không duyệt').last().click();
        await page.waitForTimeout(800);
        await c.shotM(page, '15b_reject_empty');
        c.save('_reject_text.txt', await m.innerText());
        await c.icon(btn(m, 'Không duyệt'), 'btn_khongduyet_modal');
        await c.icon(btn(m, 'Hủy'), 'btn_huy_modal');
        await btn(m, 'Hủy').last().click();
        await page.waitForTimeout(1000);
        // khối Lịch sử
        await page.locator('.si-header').first().click();
        await page.waitForTimeout(2500);
        await c.shot(page, '17b_detail_history', true);
        // Đang tạo của mình: Sửa, Xóa
        await go(page, CFG.route + '/' + CFG.draftId, false);
        await page.waitForTimeout(2500);
        await c.shot(page, '17c_detail_draft', true);
        await c.icon(btn(page, 'Sửa'), 'btn_sua_footer');
        await c.icon(btn(page, 'Xóa'), 'btn_xoa_footer');
        c.save('_detail_draft_text.txt', await page.locator('.exc-form').innerText());
    },
    async rejected(page) {
        // GIẢ LẬP phiếu Không duyệt (dev không có) — chỉ sửa dữ liệu trả về trên trình duyệt
        await P.fakeJson(page, CFG.detailApi, (j) => {
            const d = j.data.detail;
            d.status = 6;
            d.status_text = 'Không duyệt';
            d.status_type = 'danger';
            d.status_color = '#DC2626';
            d.approve_comment = 'Chưa có biên bản kiểm đếm có chữ ký nhà cung cấp, bổ sung rồi gửi lại.';
            d.approver_name = 'Nguyễn Văn Duyệt';
            d.approved_time = '17/11/2026 15:20';
        });
        await go(page, CFG.route + '/' + CFG.draftId, false);
        await page.waitForTimeout(2500);
        await c.shot(page, '17d_detail_rejected', true);
    },
    async edit(page) {
        await go(page, CFG.route + '/' + CFG.draftId + '/edit', false);
        await page.waitForTimeout(3000);
        await c.shot(page, '12_edit', true);
        c.save('_edit_text.txt', await page.locator('.exc-form').innerText());
    },
};

P.run(__dirname, steps).catch((e) => {
    console.error(e);
    process.exit(1);
});

// Chụp ảnh SRS + HDSD "BC chi phí vận chuyển theo NV kinh doanh" trên DEV (dev-hrm), trình duyệt headless riêng.
// Khuôn: danh-muc-kho/docs/warehouses/capture.js. Màn CHỈ ĐỌC: chỉ bấm Tìm kiếm, tick Xem chi tiết, mở popup Xuất Excel,
// Xuất file (file tải về để trong hdsd_shots/). KHÔNG bấm Lưu / Xóa / Duyệt ở bất kỳ màn nào.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
const fs = require('fs');
const path = require('path');
const { open, DEV } = require(path.join(__dirname, '..', '..', 'danh-muc-kho', 'docs', '_capture_login.js'));

const CFG = {
    route: '/sale/transport-cost-by-staff',
    search: 'Tìm theo mã / tên nhân viên KD, phòng ban hoặc số chuyến xe',
    filters: [
        ['Thời gian', 'o_thoigian'],
        ['Công ty', 'o_congty'],
        ['Phòng ban', 'o_phongban'],
        ['Nhân viên KD', 'o_nhanvien'],
        ['Số chuyến xe', 'o_sochuyen'],
        ['Hợp đồng', 'o_hopdong'],
        ['Yêu cầu xuất hàng', 'o_ycxh'],
        ['Đối tượng chịu phí', 'o_doituong'],
    ],
    // Kỳ có số liệu thật trên dev (dò 02/11/2026): cả năm 21 phòng / 610 chuyến; tháng 10 có 4 phòng — vừa 1 ảnh.
    kyNam: ['01/01/2026', '02/11/2026'],
    kyThang: ['01/10/2026', '02/11/2026'],
};
const SHOTS = path.join(__dirname, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
fs.mkdirSync(ICONS, { recursive: true });
const ONLY = process.argv.slice(2);
const LOG = path.join(SHOTS, '_capture_log.json');
const log = fs.existsSync(LOG) ? JSON.parse(fs.readFileSync(LOG, 'utf8')) : {};

const away = async (page) => {
    await page.mouse.move(1435, 895);
    await page.waitForTimeout(600);
};
const shot = async (page, name, opts = {}) => {
    await away(page);
    await page.screenshot({ path: path.join(SHOTS, name + '.png'), ...opts });
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
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\-]/g, '\\$&');
const ff = (page, label) =>
    page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + esc(label) + '\\s*\\*?\\s*$') }) });

async function go(page, url = CFG.route) {
    await page.goto(DEV + url);
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(2500);
}
/** Gõ khoảng ngày vào ô Thời gian rồi chờ báo cáo nạp xong (có dòng phòng ban). Trả thời gian nạp (ms). */
async function setKy(page, [from, to]) {
    const f = page.locator('input[placeholder="Từ ngày"]');
    const t = page.locator('input[placeholder="Đến ngày"]');
    await f.click();
    await f.fill(from);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(400);
    await t.click();
    await t.fill(to);
    const t0 = Date.now();
    await page.keyboard.press('Enter');
    await page.waitForTimeout(300);
    await away(page);
    await page.mouse.click(1000, 880);
    await page.locator('tr.row-dept').first().waitFor({ timeout: 60000 });
    await page.waitForLoadState('networkidle').catch(() => {});
    const ms = Date.now() - t0;
    await page.waitForTimeout(1500);
    return ms;
}

const steps = {
    async menu(page) {
        await go(page);
        await page.mouse.move(40, 300);
        await page.waitForTimeout(1200);
        await clipIcon(page, page.locator('a.logo').first(), 'menu_phanhe', 12, 218);
        const cat = page.locator('a.cat', { hasText: 'Báo cáo' }).first();
        await clipIcon(page, cat, 'menu_nhom', 0, 218);
        await cat.click();
        await page.waitForTimeout(1500);
        const pick = async (loc, minX, maxX) => {
            for (let i = 0; i < (await loc.count()); i++) {
                const b = await loc.nth(i).boundingBox();
                if (b && b.width > 0 && b.x > minX && b.x < maxX) return loc.nth(i);
            }
            return null;
        };
        const grp = await pick(page.getByText('Vận chuyển', { exact: true }), 215, 430);
        await grp.click();
        await page.waitForTimeout(1200);
        await clipIcon(page, grp.locator('xpath=..'), 'menu_nhom2', 2);
        const item = await pick(page.getByText('Chi phí vận chuyển theo nhân viên kinh doanh', { exact: true }), 430, 1400);
        await clipIcon(page, item.locator('xpath=..'), 'menu_muc', 2);
        await page.screenshot({ path: path.join(SHOTS, '00_menu_sale.png') });
    },
    async menu2(page) {
        // Đường thứ 2: phân hệ Vận chuyển => Báo cáo vận chuyển
        await go(page, '/transport/dashboard');
        await page.mouse.move(40, 300);
        await page.waitForTimeout(1200);
        await clipIcon(page, page.locator('a.logo').first(), 'menu2_phanhe', 12, 218);
        const cat = page.locator('a.cat', { hasText: 'Báo cáo vận chuyển' }).first();
        await clipIcon(page, cat, 'menu2_nhom', 0, 218);
        await cat.click();
        await page.waitForTimeout(1500);
        const item = page.getByText('Báo cáo chi phí vận chuyển theo nhân viên kinh doanh', { exact: true });
        let el = null;
        for (let i = 0; i < (await item.count()); i++) {
            const b = await item.nth(i).boundingBox();
            if (b && b.x > 230) {
                el = item.nth(i);
                break;
            }
        }
        await clipIcon(page, (el || item.last()).locator('xpath=..'), 'menu2_muc', 2);
        await page.screenshot({ path: path.join(SHOTS, '00_menu_transport.png') });
    },
    async open(page) {
        await go(page);
        await shot(page, '01_open');
        await icon(page.locator(`input[placeholder="${CFG.search}"]`).locator('xpath=..'), 'o_timnhanh');
        await icon(page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem');
        await icon(page.locator('button', { hasText: 'Làm mới' }), 'btn_lammoi');
        await icon(page.locator('button', { hasText: 'Cài đặt bộ lọc' }), 'btn_caidatboloc');
        await icon(page.locator('button', { hasText: 'tìm kiếm nâng cao' }), 'btn_antimkiem');
        await icon(page.locator('button', { hasText: 'Xuất Excel' }), 'btn_xuatexcel');
        await icon(page.locator('.custom-control, label', { hasText: 'Xem chi tiết chuyến xe' }).last(), 'chk_chitiet');
        for (const [lb, nm] of CFG.filters) {
            if (await ff(page, lb).count()) await icon(ff(page, lb), nm);
            else console.log('thiếu ô lọc', lb);
        }
        // Bấm Tìm kiếm khi chưa chọn Thời gian -> chữ đỏ dưới ô
        await page.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }).first().click();
        await page.waitForTimeout(1200);
        await shot(page, '02_required', { clip: { x: 66, y: 60, width: 1370, height: 200 } });
        log.required_text = await page.locator('.ff').first().innerText();
    },
    async report(page) {
        await go(page);
        log.load_nam_ms = await setKy(page, CFG.kyNam);
        log.footer_nam = await page.locator('.tp-small-text').first().innerText();
        log.summary_nam = await page.locator('tr.summary-row').innerText();
        await shot(page, '03_report');
        // Phân trang + chọn số dòng: cuộn xuống chân bảng
        await icon(page.locator('ul.pagination'), 'pagination');
        await page.locator('ul.pagination').first().scrollIntoViewIfNeeded();
        await page.waitForTimeout(800);
        await shot(page, '03c_footer');
        await page.evaluate(() => window.scrollTo(0, 0));
        await page.waitForTimeout(500);
        // Tooltip ⓘ cột Cước vận chuyển
        const th = page.locator('th', { hasText: 'Cước vận chuyển' }).first();
        const tip = th.locator('i, svg, span').last();
        await tip.hover();
        await page.waitForTimeout(1000);
        const b = await th.boundingBox();
        await page.screenshot({ path: path.join(SHOTS, '05_tip.png'), clip: { x: Math.max(0, b.x - 380), y: b.y - 10, width: 760, height: 330 } });
        log.tip_text = await page.locator('.tooltip, .popover, [role=tooltip]').allInnerTexts().catch(() => []);
    },
    async detail(page) {
        await go(page);
        log.load_thang_ms = await setKy(page, CFG.kyThang);
        await shot(page, '03b_thang');
        const t0 = Date.now();
        await page.locator('.custom-control, label', { hasText: 'Xem chi tiết chuyến xe' }).last().click();
        await page.locator('tr.row-trip').first().waitFor({ timeout: 60000 });
        await page.waitForLoadState('networkidle').catch(() => {});
        log.load_detail_thang_ms = Date.now() - t0;
        await page.waitForTimeout(1500);
        await shot(page, '04_detail');
        log.detail_rows = await page.locator('table.report-table tbody tr').allInnerTexts();
        const trip = page.locator('tr.row-trip').first();
        await icon(trip.locator('td').nth(8).locator('a').first(), 'link_ycxh');
        await icon(trip.locator('td').nth(9).locator('a').first(), 'link_hopdong');
        await icon(trip.locator('td').nth(10).locator('a').first(), 'link_sochuyen');
        // Cuộn ngang sang phải để thấy cột YCXH / Hợp đồng / Số chuyến xe
        await page.evaluate(() => document.querySelectorAll('.v2-table-scroll, .table-responsive, [class*="scroll"]').forEach((e) => (e.scrollLeft = 5000)));
        await page.waitForTimeout(800);
        await shot(page, '04b_detail_right');
    },
    async nodetail_nam(page) {
        // Cả năm + Xem chi tiết: đo thời gian nạp khi bật cấp chuyến (hiệu năng)
        await go(page);
        await setKy(page, CFG.kyNam);
        const t0 = Date.now();
        await page.locator('.custom-control, label', { hasText: 'Xem chi tiết chuyến xe' }).last().click();
        await page.locator('tr.row-trip').first().waitFor({ timeout: 60000 });
        await page.waitForLoadState('networkidle').catch(() => {});
        log.load_detail_nam_ms = Date.now() - t0;
    },
    async filterex(page) {
        // Lọc ví dụ: Nhân viên KD qua ô tìm nhanh (Enter)
        await go(page);
        await setKy(page, CFG.kyNam);
        await page.locator(`input[placeholder="${CFG.search}"]`).fill('Vinh');
        await page.keyboard.press('Enter');
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(2500);
        await shot(page, '02_filter');
        log.kw_vinh = await page.locator('tr.summary-row').innerText();
    },
    async export(page) {
        await go(page);
        await setKy(page, CFG.kyThang);
        await page.locator('.custom-control, label', { hasText: 'Xem chi tiết chuyến xe' }).last().click();
        await page.locator('tr.row-trip').first().waitFor({ timeout: 60000 });
        await page.waitForTimeout(1500);
        await page.locator('button', { hasText: 'Xuất Excel' }).first().click();
        await page.waitForTimeout(1500);
        const m = page.locator('.modal.show:visible .modal-content').last();
        await away(page);
        await m.screenshot({ path: path.join(SHOTS, '06_export.png') });
        await icon(m.locator('button', { hasText: 'Chọn tất cả' }), 'btn_chontatca');
        await icon(m.locator('button', { hasText: 'Bỏ chọn hết' }), 'btn_bochonhet');
        await icon(m.locator('button', { hasText: 'Xuất file' }), 'btn_xuatfile');
        await icon(m.locator('button', { hasText: /^\s*Đóng\s*$/ }), 'btn_dong');
        log.export_modal = await m.innerText();
        const [dl] = await Promise.all([
            page.waitForEvent('download', { timeout: 60000 }),
            m.locator('button', { hasText: 'Xuất file' }).click(),
        ]);
        const out = path.join(SHOTS, 'export_thang10.xlsx');
        await dl.saveAs(out);
        log.export_file = dl.suggestedFilename();
        await page.waitForTimeout(800);
        log.export_toast = await page.locator('.toasted').allInnerTexts().catch(() => []);
    },
};

(async () => {
    const { browser, page } = await open(__dirname);
    try {
        for (const [k, f] of Object.entries(steps)) {
            if (ONLY.length && !ONLY.includes(k)) continue;
            console.log('==', k);
            try {
                await f(page);
            } catch (e) {
                console.log('LỖI bước', k, e.message.split('\n')[0]);
                await page.screenshot({ path: path.join(SHOTS, '_err_' + k + '.png') }).catch(() => {});
            }
        }
    } finally {
        fs.writeFileSync(LOG, JSON.stringify(log, null, 1));
        await browser.close();
    }
})().catch((e) => {
    console.error(e);
    process.exit(1);
});

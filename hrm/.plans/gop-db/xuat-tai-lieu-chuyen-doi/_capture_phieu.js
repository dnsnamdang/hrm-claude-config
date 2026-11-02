// Bộ hàm chụp ảnh DÙNG CHUNG cho 7 PHIẾU đợt 3 (SRS + HDSD) trên dev-hrm, trình duyệt headless riêng.
// Màn mẫu: finance-declare-debt-beginning/docs/kh/capture.js. Phiếu khác: chép capture.js đó, đổi CFG + các bước riêng.
//
// AN TOÀN (dev dùng chung) — hàm ở đây KHÔNG bao giờ bấm Lưu / Lưu nháp / Gửi duyệt / Duyệt / Từ chối / Huỷ / Xoá / Import.
//   - Hộp xác nhận: confirmShot() chụp rồi bấm nút đóng (Hủy / Ở lại / Đóng).
//   - Form chưa lưu: leaveUnsaved() bấm Quay lại -> chụp hộp "Thông tin chưa lưu" -> Thoát (không lưu).
//   - Thiếu dữ liệu ở trạng thái cần chụp: fakeJson() sửa JSON trả về NGAY TRÊN TRÌNH DUYỆT (không ghi gì vào hệ thống)
//     -> GHI RÕ trong báo cáo ảnh nào giả lập.
//
// Dùng:
//   const P = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/xuat-tai-lieu-chuyen-doi/_capture_phieu.js');
//   const c = P.ctx(__dirname);           // c.shots, c.icons
//   const { browser, page } = await P.open(__dirname);
//   await P.go(page, '/finance/...'); await c.shot(page, '01_list'); ...
// Chạy bằng C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('../danh-muc-kho/docs/_capture_login.js');

const esc = (s) => String(s).replace(/[.*+?^${}()|[\]\\-]/g, '\\$&');
const exact = (s) => new RegExp('^\\s*' + esc(s) + '\\s*$');

/** Chuột ra góc phải dưới (góc trái trên là thanh menu -> hover làm bung menu). */
async function away(page) {
    await page.mouse.move(1435, 895);
    await page.waitForTimeout(600);
}

function ctx(dir) {
    const shots = path.join(dir, 'hdsd_shots');
    const icons = path.join(shots, 'icons');
    fs.mkdirSync(icons, { recursive: true });
    const c = {
        shots,
        icons,
        /** Ảnh cả màn hình (1440x900, scale 2). fullPage: chụp dài cả trang (form nhiều khối). */
        async shot(page, name, fullPage = false) {
            await away(page);
            await page.screenshot({ path: path.join(shots, name + '.png'), fullPage });
        },
        /** Ảnh chỉ khung popup / hộp xác nhận đang mở (chụp cả trang thì chữ trong popup quá nhỏ). */
        async shotM(page, name, loc = null) {
            await away(page);
            const box = loc || page.locator('.modal.show:visible .modal-content').last();
            await box.screenshot({ path: path.join(shots, name + '.png') });
        },
        /** Ảnh 1 vùng (khối form, bảng…) */
        async shotEl(page, name, loc) {
            await away(page);
            await loc.first().scrollIntoViewIfNeeded().catch(() => {});
            await loc.first().screenshot({ path: path.join(shots, name + '.png') });
        },
        /** Icon nút / ô lọc cho HDSD (sau đó chạy trim_icon.py). */
        async icon(loc, name) {
            const l = loc.first();
            if (!(await l.count())) {
                console.log('  thiếu icon', name);
                return false;
            }
            await l.scrollIntoViewIfNeeded().catch(() => {});
            await l.screenshot({ path: path.join(icons, name + '.png') });
            return true;
        },
        /** Icon cắt theo khung bao (+pad), cắt phải tại maxX (mục menu nằm trong panel rộng). */
        async clipIcon(page, loc, name, pad = 0, maxX = null) {
            const b = await loc.first().boundingBox();
            let w = b.width + 2 * pad;
            if (maxX !== null && b.x - pad + w > maxX) w = maxX - (b.x - pad);
            await page.screenshot({
                path: path.join(icons, name + '.png'),
                clip: { x: b.x - pad, y: b.y - pad, width: w, height: b.height + 2 * pad },
            });
        },
        save(name, text) {
            fs.writeFileSync(path.join(shots, name), text);
        },
    };
    return c;
}

/** Mở trang, chờ dữ liệu nạp (networkidle + có dòng bảng nếu có). */
async function go(page, url, waitRow = true) {
    await page.goto(DEV + url);
    await page.waitForLoadState('networkidle').catch(() => {});
    if (waitRow) await page.locator('tbody tr').first().waitFor({ timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(2500);
}

const modal = (page) => page.locator('.modal.show:visible').last();
const btn = (scope, text) => scope.locator('button', { hasText: typeof text === 'string' ? exact(text) : text });

/** Đóng popup đang mở bằng nút có chữ (mặc định Đóng / Hủy), không có thì Esc. */
async function closeModal(page, text = /^\s*(Đóng|Hủy)\s*$/) {
    const b = modal(page).locator('button', { hasText: text });
    if (await b.count()) await b.last().click();
    else await page.keyboard.press('Escape');
    await page.waitForTimeout(1000);
}

/**
 * Hộp xác nhận ($confirm / base-confirm-modal) đang mở có chữ `hasText`: chụp `name`, lưu nội dung `_<name>.txt`,
 * cắt icon các nút (map {chữ nút: tên icon}) rồi bấm nút ĐÓNG `closeText` (Hủy / Ở lại) — KHÔNG bấm nút xác nhận.
 */
async function confirmShot(page, c, name, hasText, iconMap = {}, closeText = 'Hủy') {
    const box = page.locator('.modal.show:visible').filter({ hasText }).last();
    await box.waitFor({ timeout: 10000 });
    await page.waitForTimeout(700);
    await c.shotM(page, name, box.locator('.modal-content'));
    c.save('_' + name + '.txt', await box.innerText().catch(() => ''));
    for (const [t, ic] of Object.entries(iconMap)) await c.icon(btn(box, t), ic);
    await btn(box, closeText).last().click();
    await page.waitForTimeout(1000);
}

/** Form đã nhập: bấm Quay lại -> chụp hộp "Thông tin chưa lưu" -> bấm Thoát (rời form, KHÔNG lưu). */
async function leaveUnsaved(page, c, name = '18_unsaved', backText = 'Quay lại') {
    await btn(page, backText).last().click();
    await page.waitForTimeout(1200);
    await confirmShot(page, c, name, 'Thông tin chưa lưu', { 'Thoát': 'btn_thoat', 'Ở lại': 'btn_olai' }, 'Thoát');
}

/**
 * Sửa JSON trả về của API khớp `re` ngay trên trình duyệt (giả lập dữ liệu để chụp, KHÔNG ghi hệ thống).
 * mutate(json) sửa tại chỗ. Trả hàm gỡ.
 */
async function fakeJson(page, re, mutate) {
    const h = async (route) => {
        const res = await route.fetch();
        const j = await res.json();
        mutate(j);
        await route.fulfill({ response: res, json: j });
    };
    await page.route(re, h);
    return () => page.unroute(re, h);
}

/** Trả thẳng JSON cố định cho API khớp `re` (vd lịch sử giả lập khi dev không có bản ghi có lịch sử). */
async function mockJson(page, re, body) {
    await page.route(re, (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(body) }));
}

/** Ô lọc của V2BaseSmartFilterPanel theo nhãn. */
const ff = (page, label) =>
    page.locator('.ff').filter({ has: page.locator('.ff__text', { hasText: exact(label) }) });

/** Dòng bảng danh sách có link mã phiếu = code (nuxt-link hoặc button v2-cell-link). */
const rowOf = (page, code) =>
    page.locator('tbody tr').filter({ has: page.locator('.v2-cell-link', { hasText: exact(code) }) }).first();

/** Nút hành động trên dòng (V2BaseRowActions: span[title] bọc button) — nút thẳng hoặc trong menu ba chấm. */
const act = (row, title) => row.locator(`span[title="${title}"] > *`);
async function rowAction(page, row, title) {
    if (await act(row, title).count()) return act(row, title).first().click();
    await row.locator('button[title="Hành động khác"]').click();
    await page.waitForTimeout(600);
    await page.locator(`.v2-row-actions__menu:visible button[title="${title}"]`).first().click();
}

/**
 * Icon menu kiểu hub (Tài chính, Kho…): menu_phanhe (logo phân hệ), menu_nhom (mục rail), menu_muc (mục trong panel).
 * Chụp kèm `00_menu.png` lúc panel đang mở.
 */
async function menuIcons(page, c, nhom, muc, route) {
    await go(page, route);
    await page.mouse.move(40, 300);
    await page.waitForTimeout(1200);
    await c.clipIcon(page, page.locator('a.logo').first(), 'menu_phanhe', 12, 300);
    const cat = page.locator('a.cat', { hasText: exact(nhom) }).first();
    await c.clipIcon(page, cat, 'menu_nhom', 0, 300);
    await cat.click();
    await page.waitForTimeout(1500);
    const items = page.getByText(muc, { exact: true });
    for (let i = 0; i < (await items.count()); i++) {
        const b = await items.nth(i).boundingBox();
        if (b && b.x > 230) {
            await c.clipIcon(page, items.nth(i).locator('xpath=..'), 'menu_muc', 2);
            break;
        }
    }
    await page.screenshot({ path: path.join(c.shots, '00_menu.png') });
}

/** Chạy các bước: `node capture.js [bước ...]`; không truyền = chạy hết trừ `skip`. Luôn đóng trình duyệt. */
async function run(dir, steps, skip = []) {
    const only = process.argv.slice(2);
    const { browser, page } = await open(dir);
    try {
        for (const [k, f] of Object.entries(steps)) {
            if (only.length && !only.includes(k)) continue;
            if (!only.length && skip.includes(k)) continue;
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
}

module.exports = {
    open, DEV, ctx, go, modal, btn, exact, esc, away, closeModal, confirmShot, leaveUnsaved, fakeJson, mockJson,
    ff, rowOf, act, rowAction, menuIcons, run,
};

// Hàm chụp dùng chung cho 2 báo cáo vận chuyển (hiệu quả gộp xe vận tải + chi tiết chuyến xe) — cùng khung TransportReportPage.
// Chỉ ĐỌC: Tìm kiếm, mở popup, Xuất Excel (file để trong thư mục mình), xem trước In. KHÔNG bấm Lưu ở cửa sổ Tuỳ chỉnh cột.
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/danh-muc-kho/docs/_capture_login.js');

function make(dir) {
    const SHOTS = path.join(dir, 'hdsd_shots');
    const ICONS = path.join(SHOTS, 'icons');
    fs.mkdirSync(ICONS, { recursive: true });
    const LOG = path.join(SHOTS, '_log.txt');
    const log = (...a) => {
        const s = a.map((x) => (typeof x === 'string' ? x : JSON.stringify(x))).join(' ');
        console.log(s);
        fs.appendFileSync(LOG, s + '\n');
    };
    const away = async (page) => {
        await page.mouse.move(720, 897);
        await page.waitForTimeout(500);
    };
    const shot = async (page, name, opts = {}) => {
        await away(page);
        await page.screenshot({ path: path.join(SHOTS, name + '.png'), ...opts });
    };
    const shotEl = async (page, loc, name) => {
        await away(page);
        await loc.screenshot({ path: path.join(SHOTS, name + '.png') });
    };
    const modal = (page) => page.locator('.modal.show:visible .modal-content').last();
    const shotM = async (page, name) => shotEl(page, modal(page), name);
    const icon = async (loc, name) => {
        try {
            await loc.first().scrollIntoViewIfNeeded().catch(() => {});
            await loc.first().screenshot({ path: path.join(ICONS, name + '.png') });
        } catch (e) {
            log('Không cắt được icon', name, e.message.split('\n')[0]);
        }
    };
    const clipIcon = async (page, loc, name, pad = 0, maxX = null) => {
        const b = await loc.first().boundingBox();
        const x = b.x - pad;
        const y = b.y - pad;
        let w = b.width + 2 * pad;
        if (maxX !== null && x + w > maxX) w = maxX - x;
        await page.screenshot({ path: path.join(ICONS, name + '.png'), clip: { x, y, width: w, height: b.height + 2 * pad } });
    };
    const ff = (page, label) =>
        page.locator('.ff:visible').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\\s*' + label + '\\s*$') }) });
    const pick = async (page, label, text) => {
        await ff(page, label).locator('.select2-selection:visible').first().click();
        await page.waitForTimeout(500);
        const opt = page.locator('.select2-results__option:visible', { hasText: text }).first();
        await opt.waitFor({ timeout: 20000 });
        await opt.click();
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(3000);
    };
    const go = async (page, route) => {
        await page.goto(DEV + route);
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(3500);
    };
    const toasts = async (page) => page.locator('.toasted').allTextContents();
    const run = async (steps, only) => {
        const { browser, page, ctx } = await open(dir);
        await page.setViewportSize({ width: 1440, height: 900 });
        try {
            for (const [name, fn] of Object.entries(steps)) {
                if (only.length && !only.includes(name)) continue;
                log('== bước', name);
                try {
                    await fn(page, ctx);
                } catch (e) {
                    log('LỖI bước', name, e.message.split('\n')[0]);
                    await page.screenshot({ path: path.join(SHOTS, '_err_' + name + '.png') }).catch(() => {});
                }
            }
        } finally {
            await browser.close();
        }
    };
    return { SHOTS, ICONS, log, away, shot, shotEl, shotM, modal, icon, clipIcon, ff, pick, go, toasts, run, DEV };
}

module.exports = { make };

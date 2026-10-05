import { chromium } from '/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/e2e/node_modules/@playwright/test/index.mjs';

// ---- Tham số CLI (Task 8) ------------------------------------------------
// node measure-popup.mjs <out.json> --url=<đường dẫn màn> [--open=<selector click để mở popup>]
//   [--sort-text=<nhãn cột CHỮ sortable>] [--sort-date=<nhãn cột NGÀY sortable, bỏ trống = không đo>]
//   [--item-label=<đơn vị dùng cho log, không bắt buộc>]
const args = process.argv.slice(2);
const OUT = args[0];
const opt = {};
for (const a of args.slice(1)) {
    const m = a.match(/^--([a-z-]+)=(.*)$/);
    if (m) opt[m[1]] = m[2];
}

const URL = opt.url || 'http://127.0.0.1:3000/assign/report/potential-customer-care';
// Selector mặc định: dòng cha đầu tiên của bảng theo dõi, ô số thứ 3 (nth 2, 0-based), nút drill
// — khớp khuôn `.rsum-tb__row--parent` dùng chung ở CẢ 3 màn báo cáo hiện có.
const OPEN_SELECTOR = opt.open || '.rsum-tb__row--parent >> nth=0';
const SORT_TEXT = opt['sort-text'] || 'Thị trường / Phường xã';
const SORT_DATE = opt['sort-date'] !== undefined ? opt['sort-date'] : 'Meeting thu thập nhu cầu';

const browser = await chromium.launch();
const page = await (await browser.newContext({
    storageState: '/tmp/care-state.json', viewport: { width: 1440, height: 900 },
})).newPage();
await page.goto(URL, { waitUntil: 'domcontentloaded' });
await page.locator('.rsum-tb__sec').first().waitFor({ timeout: 40000 });

// Mở popup từ dòng cha đầu tiên (ô số thứ 3 của bảng theo dõi — cột "Meeting KH"/"Tổng dự án"/tương đương)
await page.locator(OPEN_SELECTOR).locator('td').nth(2).locator('button.rsum-drill').click();
await page.waitForFunction(() => {
    const tr = document.querySelector('.modal.show table tbody tr');
    return tr && tr.querySelectorAll('td').length > 1;
}, { timeout: 20000 });
// Popup nào TỰ gọi API riêng (vd tkt-project-list-modal) còn cần đợi hết trạng thái "Đang tải…"
await page.waitForFunction(() => {
    const body = document.querySelector('.modal.show table tbody');
    return body && !/Đang tải/.test(body.textContent || '');
}, { timeout: 20000 });

const snap = () => page.evaluate(() => {
    const m = document.querySelector('.modal.show');
    const t = (el) => (el ? el.innerText.replace(/\s+/g, ' ').trim() : null);
    const rows = [...m.querySelectorAll('table tbody tr')];
    const dialog = m.querySelector('.modal-dialog').getBoundingClientRect();
    const wrapSel = '.care-drill-wrap, .report-drill-wrap, .v2-table-scroll__body';
    const footSel = '.care-drill-footer, .report-drill-footer, .modal-footer';
    const wrapEl = m.querySelector(wrapSel);
    const wrapStyle = wrapEl ? getComputedStyle(wrapEl) : null;
    const modalContent = m.querySelector('.modal-content');
    const footerButtons = [...m.querySelectorAll(`${footSel} button`)];
    const footerGaps = footerButtons.slice(1).map((btn, i) => {
        const prev = footerButtons[i].getBoundingClientRect();
        const cur = btn.getBoundingClientRect();
        return {
            between: `${t(footerButtons[i])} → ${t(btn)}`,
            gapPx: Math.round(cur.left - prev.right),
        };
    });

    return {
        cols: [...m.querySelectorAll('table thead th')].map((th) => t(th)),
        firstPageRowCount: rows.length,
        sttFirst: t(rows[0]?.querySelector('td')),
        sttLast: t(rows[rows.length - 1]?.querySelector('td')),
        pageTotal: t(m.querySelector('.page-total')),
        tableBottom: Math.round(wrapEl.getBoundingClientRect().bottom),
        footerTop: Math.round(m.querySelector(footSel).getBoundingClientRect().top),
        heightNormal: Math.round(dialog.height),
        // ---- 3 phép đo MỚI (Task 8, brief mục 2) — Phase 1 thiếu, không bắt được mất viền/bo góc/chặn chiều cao ----
        tableScrollBorderTopWidth: wrapStyle ? wrapStyle.borderTopWidth : null,
        tableScrollBorderRadius: wrapStyle ? wrapStyle.borderRadius : null,
        modalContentOverflow: modalContent ? getComputedStyle(modalContent).overflow : null,
        footerButtonGaps: footerGaps,
    };
});

const out = await snap();

// Sắp xếp: cột CHỮ và cột NGÀY (nếu có) -> lưu nguyên mảng giá trị sau khi bấm asc
const sortBy = async (label) => {
    const th = page.locator('.modal.show table thead th', { hasText: label }).first();
    const control = th.locator('.care-drill-sort, .report-drill-sort, .cmd-sort, .tkt-sort');
    if (!(await control.count())) {
        throw new Error(`Cột "${label}" không bấm-sắp-xếp được — đo ra thứ tự mặc định là vô nghĩa`);
    }
    await control.first().click();
    // Popup sort tại BE (vd tkt-project-list-modal) cần đợi API trả về + hết "Đang tải…", không
    // chỉ chờ 400ms cố định như popup sort client-side.
    await page.waitForFunction(() => {
        const body = document.querySelector('.modal.show table tbody');
        return body && !/Đang tải/.test(body.textContent || '');
    }, { timeout: 20000 });
    await page.waitForTimeout(400);
    const idx = (await page.locator('.modal.show table thead th').allInnerTexts())
        .findIndex((x) => x.trim().startsWith(label));
    return page.locator('.modal.show table tbody tr').evaluateAll(
        (trs, i) => trs.map((tr) => (tr.querySelectorAll('td')[i]?.textContent || '').replace(/\s+/g, ' ').trim()),
        idx,
    );
};
out.sortTextAsc = await sortBy(SORT_TEXT);
out.sortDateAsc = SORT_DATE ? await sortBy(SORT_DATE) : null;

// Phóng to toàn màn hình — CHỈ áp dụng cho popup có nút này (vỏ V2BaseReportModal). Popup dựng trên
// V2BaseModal (2 popup mới của Task 8) KHÔNG có nút này -> bỏ qua, không throw.
const zoomBtn = page.locator('.modal.show [title*="Phóng to"], .modal.show [title*="phóng to"]').first();
if (await zoomBtn.count()) {
    await zoomBtn.click();
    await page.waitForTimeout(500);
    out.heightFull = await page.evaluate(() =>
        Math.round(document.querySelector('.modal.show .modal-dialog').getBoundingClientRect().height));
} else {
    out.heightFull = null;
    out.heightFullNote = 'Popup này không có nút "Phóng to" (vỏ V2BaseModal không có tính năng này) — bỏ qua phép đo, không bịa số.';
}

const fs = await import('fs');
fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1));
await browser.close();

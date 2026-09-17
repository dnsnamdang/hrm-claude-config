import { chromium } from '/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/e2e/node_modules/@playwright/test/index.mjs';

const OUT = process.argv[2];               // đường dẫn file json để ghi
const browser = await chromium.launch();
const page = await (await browser.newContext({
    storageState: '/tmp/care-state.json', viewport: { width: 1440, height: 900 },
})).newPage();
await page.goto('http://127.0.0.1:3000/assign/report/potential-customer-care', { waitUntil: 'domcontentloaded' });
await page.locator('.rsum-tb__sec').first().waitFor({ timeout: 40000 });

// Mở popup từ dòng cha đầu tiên
await page.locator('.rsum-tb__row--parent').first().locator('td').nth(2).locator('button.rsum-drill').click();
await page.waitForFunction(() => {
    const tr = document.querySelector('.modal.show table tbody tr');
    return tr && tr.querySelectorAll('td').length > 1;
}, { timeout: 20000 });

const snap = () => page.evaluate(() => {
    const m = document.querySelector('.modal.show');
    const t = (el) => (el ? el.innerText.replace(/\s+/g, ' ').trim() : null);
    const rows = [...m.querySelectorAll('table tbody tr')];
    const dialog = m.querySelector('.modal-dialog').getBoundingClientRect();
    const wrapSel = '.care-drill-wrap, .report-drill-wrap, .v2-table-scroll__body';
    const footSel = '.care-drill-footer, .report-drill-footer, .modal-footer';
    return {
        cols: [...m.querySelectorAll('table thead th')].map((th) => t(th)),
        firstPageRowCount: rows.length,
        sttFirst: t(rows[0]?.querySelector('td')),
        sttLast: t(rows[rows.length - 1]?.querySelector('td')),
        pageTotal: t(m.querySelector('.page-total')),
        tableBottom: Math.round(m.querySelector(wrapSel).getBoundingClientRect().bottom),
        footerTop: Math.round(m.querySelector(footSel).getBoundingClientRect().top),
        heightNormal: Math.round(dialog.height),
    };
});

const out = await snap();

// Sắp xếp: cột CHỮ đầu tiên và cột NGÀY đầu tiên -> lưu nguyên mảng giá trị sau khi bấm asc
const sortBy = async (label) => {
    const th = page.locator('.modal.show table thead th', { hasText: label }).first();
    if (!(await th.count())) return null;
    await th.locator('span').first().click();
    await page.waitForTimeout(400);
    const idx = (await page.locator('.modal.show table thead th').allInnerTexts())
        .findIndex((x) => x.trim().startsWith(label));
    return page.locator('.modal.show table tbody tr').evaluateAll(
        (trs, i) => trs.map((tr) => (tr.querySelectorAll('td')[i]?.textContent || '').replace(/\s+/g, ' ').trim()),
        idx,
    );
};
out.sortTextAsc = await sortBy('Khách hàng');
out.sortDateAsc = await sortBy('Ngày meeting');

// Phóng to toàn màn hình
await page.locator('.modal.show [title*="Phóng to"], .modal.show [title*="phóng to"]').first().click();
await page.waitForTimeout(500);
out.heightFull = await page.evaluate(() =>
    Math.round(document.querySelector('.modal.show .modal-dialog').getBoundingClientRect().height));

const fs = await import('fs');
fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1));
await browser.close();

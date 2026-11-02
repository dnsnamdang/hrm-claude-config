// Dò KH có phiếu xuất bán hàng mượn trong kỳ (chỉ đọc API báo cáo) — phục vụ ảnh popup biến thể.
const { open, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/danh-muc-kho/docs/_capture_login.js');
(async () => {
    const { browser, page } = await open(__dirname);
    try {
        await page.goto(DEV + '/sale/customer-debt-compare');
        await page.waitForLoadState('networkidle').catch(() => {});
        await page.waitForTimeout(2500);
        const api = (u) => page.evaluate(async (u) => { try { return await window.$nuxt.$store.dispatch('apiGetMethod', u); } catch (e) { return { err: String(e) }; } }, u);
        const det = await api('finance/customer-debt-details?start_date=2026-01-01&end_date=2026-10-31&per_page=80&page=1');
        const custs = (det.data || []).filter((c) => c.customer_name).map((c) => [c.customer_id, c.customer_code, c.customer_name]);
        console.log('KH:', custs.length);
        for (const [id, code, name] of custs) {
            const r = await api(`finance/customer-debt-compare/export?start_date=2026-01-01&end_date=2026-10-31&customer_id=${id}`);
            const rows = (r.data && r.data.data) || [];
            const bs = rows.filter((x) => x.invoiceable_type && x.invoiceable_type.includes('BorrowSell'));
            const pi = rows.filter((x) => x.invoiceable_type && x.invoiceable_type.includes('ProductImport'));
            const bi = rows.filter((x) => x.invoiceable_type && x.invoiceable_type.includes('BillIncome'));
            if (bs.length || pi.length) console.log(id, code, name, 'rows', rows.length, 'BS', bs.map((x) => x.code).join(','), 'PI', pi.length, 'PT', bi.length);
        }
    } finally {
        await browser.close();
    }
})().catch((e) => { console.error(e); process.exit(1); });

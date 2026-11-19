// Đo thời gian lấy dữ liệu Xuất Excel (toàn bộ dòng 1 tháng, không lọc khác) — CHỈ ĐỌC, gọi đúng API mà nút Xuất Excel gọi.
const fs = require('fs');
const path = require('path');
const { open, DEV } = require('../../../danh-muc-kho/docs/_capture_login.js');
(async () => {
    const { browser, page } = await open(__dirname);
    page.setDefaultTimeout(1200000);
    await page.goto(DEV + '/sale/customer-debt-by-employee');
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.waitForTimeout(2000);
    const q = process.argv[2] || 'start_date=2026-10-01&end_date=2026-10-31';
    const r = await page.evaluate(async (q) => {
        const t0 = Date.now();
        try {
            const a = await window.$nuxt.$store.dispatch('apiGetMethod', 'finance/customer-debt-by-employee/export?' + q);
            const d = (a && a.data) || {};
            return { ms: Date.now() - t0, nv: (d.data || []).length, hd: (d.data || []).reduce((s, e) => s + e.children.length, 0) };
        } catch (e) {
            return { ms: Date.now() - t0, err: String(e && (e.message || e)), status: e && e.response && e.response.status };
        }
    }, q);
    const line = 'export ' + q + ' -> ' + JSON.stringify(r);
    console.log(line);
    fs.appendFileSync(path.join(__dirname, 'hdsd_shots', '_log.txt'), line + '\n');
    await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });

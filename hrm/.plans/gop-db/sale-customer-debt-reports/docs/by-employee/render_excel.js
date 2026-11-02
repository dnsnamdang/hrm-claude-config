// Chụp 2 trang HTML do render_excel.py dựng từ file Excel tải về -> hdsd_shots/03c_excel.png, 07_mauin.png
const path = require('path');
const { chromium } = require('C:/Users/Legion/AppData/Local/nvm/v24.6.0/node_modules/@playwright/mcp/node_modules/playwright');
(async () => {
    const b = await chromium.launch({ headless: true });
    const p = await b.newPage({ viewport: { width: 1200, height: 700 }, deviceScaleFactor: 2 });
    for (const [src, out] of [['mau1.html', '03c_excel.png'], ['mauin.html', '07_mauin.png']]) {
        await p.goto('file:///' + path.join(__dirname, 'hdsd_shots', '_excel_html', src).replace(/\\/g, '/'));
        await p.locator('.sheet').screenshot({ path: path.join(__dirname, 'hdsd_shots', out) });
    }
    await b.close();
})();

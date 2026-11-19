// Trình duyệt headless RIÊNG cho từng agent, đăng nhập sẵn dev-hrm — chụp ảnh song song nhiều màn.
// Dùng: const { openDev } = require('<đường dẫn>/pw_dev.js');
//       const { browser, page } = await openDev('<thư mục lưu phiên>');
//       await page.goto(DEV + '/finance/...'); ... await browser.close();
// Chạy bằng: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe <script>.js
const fs = require('fs');
const path = require('path');
const { chromium } = require('C:/Users/Legion/AppData/Local/nvm/v24.6.0/node_modules/@playwright/mcp/node_modules/playwright');

const DEV = 'https://dev-hrm.eteksofts.com';
const EMAIL = 'namdangit@gmail.com';
const PASS = '2025Dns@2';

async function openDev(stateDir, opts = {}) {
    const stateFile = path.join(stateDir, '.dev_state.json');
    const browser = await chromium.launch({ headless: true });
    const ctx = await browser.newContext({
        viewport: { width: 1440, height: 900 },
        deviceScaleFactor: opts.scale || 2,
        storageState: fs.existsSync(stateFile) ? stateFile : undefined,
    });
    const page = await ctx.newPage();
    await page.goto(DEV + '/');
    await page.waitForLoadState('networkidle').catch(() => {});
    if (page.url().includes('/login')) {
        await page.fill('#emailaddress, input[type=email], input[name=email]', EMAIL);
        await page.fill('#password, input[type=password]', PASS);
        await page.keyboard.press('Enter');
        await page.waitForURL(u => !String(u).includes('/login'), { timeout: 60000 });
        await page.waitForLoadState('networkidle').catch(() => {});
        fs.mkdirSync(stateDir, { recursive: true });
        await ctx.storageState({ path: stateFile });
    }
    return { browser, ctx, page, DEV };
}

module.exports = { openDev, DEV };

if (require.main === module) {
    (async () => {
        const { browser, page } = await openDev(process.argv[2] || __dirname);
        console.log('OK', page.url());
        await browser.close();
    })().catch(e => { console.error(e); process.exit(1); });
}

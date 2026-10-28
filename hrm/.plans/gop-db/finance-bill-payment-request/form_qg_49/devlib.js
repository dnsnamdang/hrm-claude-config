const fs = require('fs'), path = require('path');
const { openDev, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/phieu-theo-form-quoc-gia/pw_dev.js');
async function open() {
  const o = await openDev(__dirname);
  const { page, ctx } = o;
  await page.goto(DEV + '/finance/dashboard').catch(() => {});
  await page.waitForTimeout(3000);
  if (page.url().includes('/login')) {
    await page.fill('#emailaddress, input[type=email], input[name=email]', 'namdangit@gmail.com');
    await page.fill('#password, input[type=password]', '2025Dns@2');
    await page.keyboard.press('Enter');
    await page.waitForURL(u => !String(u).includes('/login'), { timeout: 60000 });
    await page.waitForLoadState('networkidle').catch(() => {});
    await ctx.storageState({ path: path.join(__dirname, '.dev_state.json') });
  }
  return o;
}
async function go(page, url) {
  await page.goto(DEV + url).catch(() => {});
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(2500);
}
module.exports = { open, go, DEV };

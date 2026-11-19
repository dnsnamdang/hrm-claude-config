// Bọc pw_dev.js: tự đăng nhập lại nếu bị đẩy về /login giữa chừng.
const path = require('path');
const fs = require('fs');
const { openDev, DEV } = require('D:/CompanyProject/hrm/hrm-claude-config/hrm/.plans/gop-db/phieu-theo-form-quoc-gia/pw_dev.js');
async function login(page, ctx, dir) {
  await page.waitForSelector('input[type=password]', { timeout: 30000 });
  await page.fill('#emailaddress, input[type=email], input[name=email]', 'namdangit@gmail.com');
  await page.fill('#password, input[type=password]', '2025Dns@2');
  await page.keyboard.press('Enter');
  await page.waitForURL(u => !String(u).includes('/login'), { timeout: 60000 });
  await page.waitForLoadState('networkidle').catch(() => {});
  await ctx.storageState({ path: path.join(dir, '.dev_state.json') });
}
async function open(dir, opts) {
  const o = await openDev(dir, opts);
  const { page, ctx } = o;
  o.go = async (url) => {
    for (let i = 0; i < 3; i++) {
      try { await page.goto(DEV + url); } catch (e) { }
      await page.waitForLoadState('networkidle').catch(() => {});
      await page.waitForTimeout(1500);
      if (page.url().includes('/login')) { await login(page, ctx, dir); continue; }
      return;
    }
    throw new Error('Không vào được ' + url);
  };
  return o;
}
module.exports = { open, DEV };

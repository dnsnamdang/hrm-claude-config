const fs = require('fs');
const path = require('path');
// Dùng chung cho capture.js của 7 danh mục kho: mở trình duyệt headless riêng, đăng nhập dev-hrm.
// Đăng nhập chắc chắn: pw_dev.openDev đôi khi kiểm URL trước khi trang tự chuyển về /login
const PW_DEV = path.join(__dirname, '..', '..', 'phieu-theo-form-quoc-gia', 'pw_dev.js');
const { openDev, DEV } = require(PW_DEV);
// Tài khoản dev lấy từ chính pw_dev.js (không chép mật khẩu sang file khác)
const SRC = fs.readFileSync(PW_DEV, 'utf8');
const EMAIL = /const EMAIL = '([^']+)'/.exec(SRC)[1];
const PASS = /const PASS = '([^']+)'/.exec(SRC)[1];
async function open(dir) {
  const r = await openDev(dir);
  const { page, ctx } = r;
  await page.waitForTimeout(3000);
  if (page.url().includes('/login')) {
    await page.fill('#emailaddress, input[type=email], input[name=email]', EMAIL);
    await page.fill('#password, input[type=password]', PASS);
    await page.keyboard.press('Enter');
    await page.waitForURL(u => !String(u).includes('/login'), { timeout: 60000 });
    await page.waitForLoadState('networkidle').catch(() => {});
    await ctx.storageState({ path: path.join(dir, '.dev_state.json') });
  }
  return r;
}
module.exports = { open, DEV };

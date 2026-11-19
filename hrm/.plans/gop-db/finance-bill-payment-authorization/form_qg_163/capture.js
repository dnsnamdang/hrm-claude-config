// Chụp ảnh HDSD/SRS màn Phiếu ủy nhiệm chi trên DEV (headless riêng, đăng nhập sẵn).
// AN TOÀN: chỉ mở màn / popup / hộp xác nhận rồi bấm Hủy / Đóng. KHÔNG bấm Xác nhận, Lưu, Xóa.
// Phiếu nháp không có trên dev (tài khoản chưa lập phiếu nào) → nút Sửa/Xóa được BẬT TẠM HIỂN THỊ
// bằng cách sửa cờ is_can_edit/is_can_delete trong phản hồi GET (chỉ trên trình duyệt, không ghi dữ liệu).
// Chạy: node capture.js [tên bước ...]   (không truyền = chụp hết)
const fs = require('fs');
const path = require('path');
const { open } = require('./devlib.js');

const SHOTS = path.join(__dirname, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
fs.mkdirSync(ICONS, { recursive: true });
const LIST = '/finance/bill-payment-authorizations';
const DETAIL_ID = 3278;      // phiếu Đã hạch toán, có lịch sử (lập trên HRM)
const ONLY = process.argv.slice(2);

async function rectOf(loc) { return loc.boundingBox(); }

function mk(page) {
  const h = {};
  h.wait = (ms) => page.waitForTimeout(ms);
  h.mouseOut = async () => { await page.mouse.move(700, 8); await page.waitForTimeout(300); };
  h.clip = async (name, box, pad = 0, dir = SHOTS) => {
    const vp = page.viewportSize();
    const x = Math.max(0, box.x - pad), y = Math.max(0, box.y - pad);
    const w = Math.min(vp.width - x, box.width + 2 * pad), hh = Math.min(vp.height - y, box.height + 2 * pad);
    await page.screenshot({ path: path.join(dir, name + '.png'), clip: { x, y, width: w, height: hh } });
  };
  h.el = async (name, loc, pad = 0) => { await loc.scrollIntoViewIfNeeded().catch(() => {}); const b = await rectOf(loc); if (!b) throw new Error('Không thấy ' + name); await h.clip(name, b, pad); };
  h.icon = async (name, loc, pad = 2) => { await loc.scrollIntoViewIfNeeded().catch(() => {}); await page.waitForTimeout(200); const b = await rectOf(loc); if (!b) throw new Error('Không thấy icon ' + name); await h.clip(name, b, pad, ICONS); };
  h.full = async (name) => { await h.mouseOut(); await page.screenshot({ path: path.join(SHOTS, name + '.png') }); };
  h.btn = (text) => page.locator('button:visible, a.btn:visible').filter({ hasText: new RegExp('^\\s*' + text + '\\s*$') });
  return h;
}

// Bật tạm cờ Sửa/Xóa trong phản hồi GET (chỉ hiển thị).
async function forceCanEdit(page, onlyFirst) {
  await page.route(/\/finance\/bill-payment-authorizations(\/\d+)?(\?.*)?$/, async (route) => {
    const req = route.request();
    if (req.method() !== 'GET' || !['xhr', 'fetch'].includes(req.resourceType())) return route.continue();
    const res = await route.fetch();
    let j = await res.json().catch(() => null);
    if (!j) return route.fulfill({ response: res });
    const fix = (o) => { if (o && typeof o === 'object') { o.is_can_edit = true; o.is_can_delete = true; } };
    if (Array.isArray(j.data)) { (onlyFirst ? j.data.slice(0, 1) : j.data).forEach(fix); } else if (j.data) fix(j.data); else fix(j);
    return route.fulfill({ response: res, json: j });
  });
}

async function select2Pick(page, label, optionText) {
  const grp = page.locator('.col-md-3, .col-md-4, .col-md-6, .form-group').filter({ has: page.locator('label', { hasText: new RegExp('^\\s*' + label) }) }).first();
  await grp.locator('.select2-selection').first().click();
  await page.waitForTimeout(600);
  const search = page.locator('.select2-container--open .select2-search__field');
  if (await search.count()) { await search.first().fill(optionText.slice(0, 12)); await page.waitForTimeout(1200); }
  await page.locator('.select2-results__option', { hasText: optionText }).first().click();
  await page.waitForTimeout(800);
}

const STEPS = {
  async menu(page, h, go) {
    await page.setViewportSize({ width: 1080, height: 675 });
    await go(LIST);
    await page.mouse.move(30, 383); await h.wait(900);
    await page.mouse.click(100, 383); await h.wait(1500);
    await h.icon('menu_phanhe', page.locator('.subsystem-name').first().locator('xpath=..'), 4);
    await h.icon('menu_nhom', page.locator('.left-side-menu a.cat', { hasText: 'Quản lý tiền' }).first(), 0);
    await h.icon('menu_thanhtoan', page.locator('.scat-nm', { hasText: 'Thanh toán tiền mặt' }).first().locator('xpath=..'), 2);
    await h.icon('menu_muc', page.locator('.row-nm', { hasText: 'Phiếu ủy nhiệm chi' }).first().locator('xpath=..'), 2);
  },
  async list(page, h, go) {
    await page.setViewportSize({ width: 1080, height: 675 });
    await go(LIST);
    await page.getByText('UNC', { exact: false }).first().waitFor();
    await h.wait(1500);
    await h.full('01_list');
    await h.icon('btn_timkiem', h.btn('Tìm kiếm').first());
    await h.icon('btn_lammoi', h.btn('Làm mới').first());
    await h.icon('btn_timkiemnangcao', h.btn('Tìm kiếm nâng cao').first());
    await h.icon('btn_caidatboloc', h.btn('Cài đặt bộ lọc').first());
    await h.icon('btn_taomoi', h.btn('Tạo mới').first());
    await h.icon('btn_cauhinhcot', page.locator('button[title="Cấu hình cột hiển thị"]').first());
    await h.icon('o_timnhanh', page.locator('input[placeholder^="Tìm theo mã phiếu"]').first(), 2);
    await h.icon('btn_lichsu_row', page.locator('.v2-row-actions span[title="Lịch sử"]').first());
    // Bộ lọc nâng cao
    await page.setViewportSize({ width: 1080, height: 900 });
    await h.btn('Tìm kiếm nâng cao').first().click();
    await h.wait(1500);
    await h.mouseOut();
    const card = page.locator('section.smart-filter-card').first();
    await h.el('02_filter', card, 0);
    const fld = (t) => card.locator('.ff').filter({ has: page.locator('label', { hasText: new RegExp('^\\s*' + t + '\\s*$') }) }).first();
    for (const [n, t] of [['o_maphieu', 'Mã phiếu'], ['o_madenghi', 'Mã phiếu đề nghị chi'], ['o_loaichi', 'Loại chi'], ['o_trangthai', 'Trạng thái'], ['o_nguoilap', 'Người lập'], ['o_nguoidenghi', 'Người đề nghị'], ['o_congty', 'Công ty'], ['o_phongban', 'Phòng ban'], ['o_bophan', 'Bộ phận'], ['o_ngaylap', 'Ngày lập']]) {
      try { await h.icon(n, fld(t), 1); } catch (e) { console.log('WARN', n, e.message); }
    }
  },
  async rowicons(page, h, go) {
    await page.setViewportSize({ width: 1080, height: 675 });
    await forceCanEdit(page, true);
    await go(LIST);
    await page.getByText('UNC', { exact: false }).first().waitFor();
    await h.wait(1500);
    await h.icon('btn_sua_row', page.locator('.v2-row-actions span[title="Sửa"]').first());
    await h.icon('btn_xoa_row', page.locator('.v2-row-actions span[title="Xóa"]').first());
    await page.locator('.v2-row-actions span[title="Xóa"]').first().locator('button, a').first().click();
    await h.wait(1200);
    const m = page.locator('.modal.show .modal-content').first();
    await h.mouseOut();
    await h.el('13_delete', m, 0);
    await h.icon('btn_confirm_xoa', m.locator('button', { hasText: 'Xóa' }).last());
    await h.icon('btn_huy_confirm', m.locator('button', { hasText: 'Hủy' }).first());
    await m.locator('button', { hasText: 'Hủy' }).first().click();
    await h.wait(800);
    await page.unrouteAll({ behavior: 'ignoreErrors' });
  },
  async history(page, h, go) {
    await page.setViewportSize({ width: 1080, height: 675 });
    await go(LIST + '/' + DETAIL_ID);
    await page.getByText('UNC', { exact: false }).first().waitFor();
    await h.wait(2000);
    const code = (await page.title()).split(':').pop().trim();
    console.log('history code', code);
    await go(LIST);
    await page.getByText('UNC', { exact: false }).first().waitFor();
    await page.locator('input[placeholder^="Tìm theo mã phiếu"]').first().fill(code);
    await page.keyboard.press('Enter');
    await h.wait(2500);
    await page.locator('tbody tr', { hasText: code }).first().locator('.v2-row-actions span[title="Lịch sử"]').locator('button, a').first().click();
    await h.wait(2500);
    const m = page.locator('.modal.show .modal-content').first();
    await h.mouseOut();
    await h.el('16_history', m, 0);
    try { await h.icon('btn_boloc_ls', m.locator('button', { hasText: 'Bộ lọc' }).first()); } catch (e) { console.log('WARN boloc', e.message); }
    try { await h.icon('btn_dong_ls', m.locator('button', { hasText: 'Đóng' }).last()); } catch (e) { console.log('WARN dong', e.message); }
  },
  async colcfg(page, h, go) {
    await page.setViewportSize({ width: 1080, height: 675 });
    await go(LIST);
    await page.getByText('UNC', { exact: false }).first().waitFor();
    await page.locator('button[title="Cấu hình cột hiển thị"]').first().click();
    await h.wait(1500);
    const m = page.locator('.modal.show .modal-content').first();
    await h.mouseOut();
    await h.el('25_colcfg', m, 0);
    await h.icon('btn_chontatca', m.locator('button', { hasText: 'Chọn tất cả' }).first());
    await h.icon('btn_bochonhet', m.locator('button', { hasText: 'Bỏ chọn hết' }).first());
    await h.icon('btn_luu_col', m.locator('button', { hasText: 'Lưu' }).last());
    await h.icon('btn_dong_col', m.locator('button', { hasText: 'Đóng' }).last());
    await m.locator('button', { hasText: 'Đóng' }).last().click();
    await h.wait(800);
    await h.btn('Cài đặt bộ lọc').first().click();
    await h.wait(1500);
    const f = page.locator('.modal.show .modal-content').first();
    await h.mouseOut();
    await h.el('26_filtercfg', f, 0);
    await h.icon('btn_luu', f.locator('button', { hasText: 'Lưu' }).last());
    await h.icon('btn_khoiphuc', f.locator('button', { hasText: 'Khôi phục' }).first());
    await h.icon('btn_dong_filtercfg', f.locator('button', { hasText: 'Đóng' }).last());
    await f.locator('button', { hasText: 'Đóng' }).last().click();
  },
  async create(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await go(LIST + '/create');
    await page.getByText('Nhấn vào đây', { exact: false }).first().waitFor().catch(() => {});
    await page.locator('input[placeholder^="Nhấn vào đây"]').first().waitFor();
    await h.wait(2000);
    await h.mouseOut();
    await page.screenshot({ path: path.join(SHOTS, '10_create.png'), fullPage: false });
    await h.icon('btn_luunhap', h.btn('Lưu nháp').first());
    await h.icon('btn_luuduyet', h.btn('Lưu và duyệt').first());
    await h.icon('btn_luutieptuc', h.btn('Lưu và tiếp tục').first());
    await h.icon('btn_quaylai', h.btn('Quay lại').first());
    await h.icon('o_sophieudenghi', page.locator('input[placeholder^="Nhấn vào đây"]').first(), 1);
    // Hộp xác nhận Lưu và duyệt → chụp → Hủy
    await h.btn('Lưu và duyệt').first().click();
    await h.wait(1200);
    let m = page.locator('.modal.show .modal-content').first();
    await h.mouseOut();
    await h.el('14_approve', m, 0);
    await h.icon('btn_confirm_xacnhan', m.locator('button', { hasText: 'Xác nhận' }).first());
    await m.locator('button', { hasText: 'Hủy' }).first().click();
    await h.wait(1000);
    // Popup chọn phiếu đề nghị
    await page.locator('input[placeholder^="Nhấn vào đây"]').first().click();
    await h.wait(3000);
    m = page.locator('.modal.show .modal-content').first();
    await m.getByText('DNTT', { exact: false }).first().waitFor();
    await h.wait(800);
    await h.mouseOut();
    await h.el('11_request', m, 0);
    try { await h.icon('btn_dong_req', m.locator('button', { hasText: 'Đóng' }).last()); } catch (e) { console.log('WARN', e.message); }
    // Chọn 1 dòng (chỉ nạp dữ liệu về form, không lưu)
    await m.locator('tbody tr').filter({ hasText: 'Chi trả nhà cung cấp' }).first().click().catch(async () => { await m.locator('tbody tr').first().click(); });
    await h.wait(3500);
    await h.mouseOut();
    await page.screenshot({ path: path.join(SHOTS, '10b_filled.png'), fullPage: false });
  },
  async income(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await go(LIST + '/create');
    await page.locator('input[placeholder^="Nhấn vào đây"]').first().waitFor();
    await h.wait(1500);
    await select2Pick(page, 'Loại chi', 'Chi thu nhập cho nhân viên');
    await h.wait(1500);
    await select2Pick(page, 'Phòng ban', process.env.PB || 'Phòng Kế toán');
    await h.wait(4000);
    await h.mouseOut();
    await page.screenshot({ path: path.join(SHOTS, '12_income.png'), fullPage: false });
    const tab = page.locator('a, button, li', { hasText: /^\s*Chi tiết vụ việc\s*$/ }).first();
    await tab.click();
    await h.wait(1500);
    await h.mouseOut();
    await page.screenshot({ path: path.join(SHOTS, '12b_vuviec.png'), fullPage: false });
  },
  async detail(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await go(LIST + '/' + DETAIL_ID);
    await page.getByText('UNC', { exact: false }).first().waitFor();
    await h.wait(2500);
    await h.mouseOut();
    await page.screenshot({ path: path.join(SHOTS, '17_detail.png'), fullPage: false });
    // Nút nằm sát đáy, bị footer cố định che -> cuộn ra giữa màn rồi mới cắt icon.
    await h.btn('Xem lịch sử').first().evaluate(e => e.scrollIntoView({ block: 'center' }));
    await h.mouseOut();
    const xb = await h.btn('Xem lịch sử').first().boundingBox();
    await h.clip('btn_xemlichsu', xb, 2, ICONS);
    await h.btn('Xem lịch sử').first().click();
    await h.wait(2500);
    await h.mouseOut();
    await page.screenshot({ path: path.join(SHOTS, '17b_detail_history.png'), fullPage: false });
  },
  async draft(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await forceCanEdit(page, false);
    await go(LIST + '/' + DETAIL_ID);
    await page.getByText('UNC', { exact: false }).first().waitFor();
    await h.wait(2500);
    await h.mouseOut();
    await page.screenshot({ path: path.join(SHOTS, '17c_draft.png'), fullPage: false });
    await h.icon('btn_sua', h.btn('Sửa').first());
    await h.icon('btn_xoa', h.btn('Xóa').first());
    await h.btn('Sửa').first().click();
    await h.wait(3500);
    await h.mouseOut();
    await page.screenshot({ path: path.join(SHOTS, '15_edit.png'), fullPage: false });
    await page.unrouteAll({ behavior: 'ignoreErrors' });
  },
};

(async () => {
  const { browser, page, go } = await open(__dirname, { scale: 1 });
  const h = mk(page);
  for (const [k, fn] of Object.entries(STEPS)) {
    if (ONLY.length && !ONLY.includes(k)) continue;
    try { await fn(page, h, go); console.log('OK', k); } catch (e) { console.log('FAIL', k, e.message.split('\n')[0]); }
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });

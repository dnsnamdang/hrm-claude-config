// Chụp ảnh HDSD/SRS màn Phiếu đề nghị thu tiền trên DEV (headless riêng, đăng nhập sẵn).
// AN TOÀN: chỉ mở màn / popup / hộp xác nhận rồi bấm Hủy / Đóng / Ở lại. KHÔNG bấm Xác nhận, Lưu, Xóa, Không duyệt.
// Nút Sửa/Xóa: BẬT TẠM cờ is_can_edit/is_can_delete trong phản hồi GET (chỉ trình duyệt, không ghi dữ liệu).
// Chạy: node capture.js [bước ...]
const fs = require('fs');
const path = require('path');
const { open } = require('./devlib.js');

const SHOTS = path.join(__dirname, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
fs.mkdirSync(ICONS, { recursive: true });
const LIST = '/finance/bill-income-requests';
const WAIT_ID = 2932;   // Chờ KT duyệt, có Tạo phiếu thu
const REJ_ID = 2930;    // Không duyệt, có lịch sử
const REJ_CODE = 'TPE.DNTT1026.00065';
const ONLY = process.argv.slice(2);

function mk(page) {
  const h = {};
  h.wait = (ms) => page.waitForTimeout(ms);
  h.mouseOut = async () => { await page.mouse.move(700, 8); await page.waitForTimeout(400); };
  h.clip = async (name, box, pad = 0, dir = SHOTS) => {
    const vp = page.viewportSize();
    const x = Math.max(0, box.x - pad), y = Math.max(0, box.y - pad);
    const w = Math.min(vp.width - x, box.width + 2 * pad), hh = Math.min(vp.height - y, box.height + 2 * pad);
    await page.screenshot({ path: path.join(dir, name + '.png'), clip: { x, y, width: w, height: hh } });
  };
  h.el = async (name, loc, pad = 0) => { await loc.scrollIntoViewIfNeeded().catch(() => {}); const b = await loc.boundingBox(); if (!b) throw new Error('Không thấy ' + name); await h.clip(name, b, pad); };
  h.icon = async (name, loc, pad = 2) => {
    try {
      await loc.scrollIntoViewIfNeeded({ timeout: 3000 }).catch(() => {});
      const b = await loc.boundingBox({ timeout: 4000 });
      if (!b) throw new Error('rỗng');
      await h.clip(name, b, pad, ICONS);
    } catch (e) { console.log('WARN icon', name, e.message.split('\n')[0]); }
  };
  h.full = async (name, fullPage = false) => { await h.mouseOut(); await page.screenshot({ path: path.join(SHOTS, name + '.png'), fullPage }); };
  h.btn = (text) => page.locator('button:visible, a.btn:visible').filter({ hasText: new RegExp('^\\s*' + text + '\\s*$') });
  h.modal = () => page.locator('.modal.show .modal-content').last();
  h.listReady = async () => { await page.getByText('DNTT', { exact: false }).first().waitFor({ timeout: 30000 }); await h.wait(1200); };
  return h;
}

async function forceCanEdit(page) {
  await page.route(/\/api\/v1\/finance\/bill-income-requests(\/\d+)?(\?.*)?$/, async (route) => {
    const req = route.request();
    if (req.method() !== 'GET') return route.continue();
    const res = await route.fetch();
    const j = await res.json().catch(() => null);
    if (!j) return route.fulfill({ response: res });
    const fix = (o) => { if (o && typeof o === 'object') { o.is_can_edit = true; o.is_can_delete = true; } };
    if (Array.isArray(j.data)) j.data.forEach(fix); else if (j.data) fix(j.data); else fix(j);
    return route.fulfill({ response: res, json: j });
  });
}

async function pickType(page, h, text) {
  const grp = page.locator('.col-md-3').filter({ has: page.locator('label', { hasText: /^\s*Loại thu/ }) }).first();
  await grp.locator('.select2-selection').first().click();
  await h.wait(600);
  await page.locator('.select2-results__option', { hasText: text }).first().click();
  await h.wait(1200);
}

const STEPS = {
  async menu(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await go(LIST);
    await h.listReady();
    await h.icon('menu_phanhe', page.locator('.subsystem-name').first().locator('xpath=..'), 4);
    const rail = page.locator('.left-side-menu a.cat', { hasText: /^\s*Khởi tạo\s*$/ }).first();
    await rail.hover(); await h.wait(900); await rail.click().catch(() => {}); await h.wait(1500);
    await h.icon('menu_nhom', rail, 0);
    await h.icon('menu_khoitao', page.locator('.scat-nm', { hasText: 'Khởi tạo phiếu yêu cầu' }).first().locator('xpath=..'), 2);
    await h.icon('menu_muc', page.locator('.row-nm', { hasText: /^\s*Đề nghị thu tiền\s*$/ }).first().locator('xpath=..'), 2);
    await page.screenshot({ path: path.join(SHOTS, '00_menu.png') });
    const rail2 = page.locator('.left-side-menu a.cat', { hasText: /^\s*Chờ duyệt\s*$/ }).first();
    await rail2.hover(); await h.wait(900); await rail2.click().catch(() => {}); await h.wait(1500);
    await h.icon('menu_choduyet', rail2, 0);
    await h.icon('menu_pheduyet', page.locator('.scat-nm', { hasText: 'Phê duyệt - Công nợ' }).first().locator('xpath=..'), 2);
    await h.icon('menu_muc_choduyet', page.locator('.row-nm', { hasText: 'Phiếu đề nghị thu tiền chờ duyệt' }).first().locator('xpath=..'), 2);
    await page.screenshot({ path: path.join(SHOTS, '00_menu2.png') });
  },
  async list(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await go(LIST);
    await h.listReady();
    await h.full('01_list');
    await h.icon('btn_timkiem', h.btn('Tìm kiếm').first());
    await h.icon('btn_lammoi', h.btn('Làm mới').first());
    await h.icon('btn_timkiemnangcao', h.btn('Tìm kiếm nâng cao').first());
    await h.icon('btn_caidatboloc', h.btn('Cài đặt bộ lọc').first());
    await h.icon('btn_taomoi', h.btn('Tạo mới').first());
    await h.icon('btn_cauhinhcot', page.locator('button[title="Cấu hình cột hiển thị"]').first());
    await h.icon('o_timnhanh', page.locator('input[placeholder^="Tìm theo mã phiếu"]').first(), 2);
    await h.icon('btn_lichsu_row', page.locator('.v2-row-actions [title="Lịch sử"]').first());
    await h.icon('btn_in_row', page.locator('.v2-row-actions [title="In phiếu"]').first());
    await h.icon('btn_taophieuthu_row', page.locator('.v2-row-actions [title="Tạo phiếu thu"]').first());
    await h.btn('Tìm kiếm nâng cao').first().click();
    await h.wait(1500);
    await h.mouseOut();
    const card = page.locator('section.smart-filter-card').first();
    await h.el('02_filter', card, 0);
    const fld = (t) => card.locator('div.ff').filter({ has: page.locator('.ff__text', { hasText: new RegExp('^\s*' + t + '\s*$') }) }).first();
    for (const [n, t] of [['o_congty', 'Công ty'], ['o_phongban', 'Phòng ban'], ['o_bophan', 'Bộ phận'], ['o_loaithu', 'Loại thu'], ['o_trangthai', 'Trạng thái'], ['o_hopdong', 'Số đơn hàng/hợp đồng'], ['o_khachhang', 'Khách hàng'], ['o_ncc', 'Nhà cung cấp'], ['o_nguoitao', 'Người tạo'], ['o_sotien', 'Số tiền đề nghị'], ['o_ngaytao', 'Ngày tạo']]) {
      await h.icon(n, fld(t), 1);
    }
  },
  async rowicons(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await forceCanEdit(page);
    await go(LIST);
    await h.listReady();
    await h.icon('btn_sua_row', page.locator('.v2-row-actions [title="Sửa"]').first());
    const ra = page.locator('.v2-row-actions').first();
    const dots = ra.locator('button[title="Hành động khác"]').first();
    await h.icon('btn_bacham_row', dots);
    await dots.click(); await h.wait(900);
    await h.mouseOut();
    const vis = page.locator('.dropdown-menu.show, .v2-row-actions__menu:visible, .popover:visible').last();
    console.log('MENU', (await vis.innerHTML().catch(() => 'none')).slice(0, 800));
    await h.icon('item_xoa', vis.locator('a, button, li, div', { hasText: /^\s*Xóa\s*$/ }).last());
    await h.icon('item_lichsu', vis.locator('a, button, li, div', { hasText: /^\s*Lịch sử\s*$/ }).last());
    await page.screenshot({ path: path.join(SHOTS, '05_rowmenu.png') });
    await vis.locator('a, button, li, div', { hasText: /^\s*Xóa\s*$/ }).last().click();
    await h.wait(1200);
    const m = h.modal();
    await h.mouseOut();
    await h.el('13_delete', m, 0);
    await h.icon('btn_confirm_xoa', m.locator('button', { hasText: 'Xóa' }).last());
    await m.locator('button', { hasText: 'Hủy' }).first().click();
    await h.wait(800);
    await page.unrouteAll({ behavior: 'ignoreErrors' });
  },
  async history(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await go(LIST);
    await h.listReady();
    const qs = page.locator('input[placeholder^="Tìm theo mã phiếu"]').first();
    await qs.fill(REJ_CODE); await h.btn('Tìm kiếm').first().click(); await h.wait(2500);
    await page.locator('.v2-row-actions [title="Lịch sử"] button').first().click();
    await h.wait(3000);
    const m = h.modal();
    await h.mouseOut();
    await h.el('16_history', m, 0);
    await h.icon('btn_boloc_ls', m.locator('button', { hasText: 'Bộ lọc' }).first());
    await h.icon('btn_dong_ls', m.locator('button', { hasText: 'Đóng' }).last());
    await m.locator('button', { hasText: 'Đóng' }).last().click(); await h.wait(500);
    await h.btn('Làm mới').first().click(); await h.wait(1500);
  },
  async colcfg(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await go(LIST);
    await h.listReady();
    await page.locator('button[title="Cấu hình cột hiển thị"]').first().click();
    await h.wait(1500);
    let m = h.modal();
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
    m = h.modal();
    await h.mouseOut();
    await h.el('26_filtercfg', m, 0);
    await h.icon('btn_luu', m.locator('button', { hasText: 'Lưu' }).last());
    await h.icon('btn_khoiphuc', m.locator('button', { hasText: 'Khôi phục' }).first());
    await h.icon('btn_dong_filtercfg', m.locator('button', { hasText: 'Đóng' }).last());
    await m.locator('button', { hasText: 'Đóng' }).last().click();
  },
  async pending(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await go(LIST + '/pending');
    await h.listReady();
    await h.full('21_pending');
  },
  async create(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await go(LIST + '/create');
    await page.locator('a[title="Thêm dòng"]').first().waitFor();
    await h.wait(1500);
    await h.full('10_create');
    await h.icon('btn_luunhap', h.btn('Lưu nháp').first());
    await h.icon('btn_luuguiduyet', h.btn('Lưu và gửi duyệt').first());
    await h.icon('btn_luutieptuc', h.btn('Lưu và tiếp tục').first());
    await h.icon('btn_quaylai', h.btn('Quay lại').first());
    await h.icon('btn_themdong', page.locator('a[title="Thêm dòng"]').first(), 4);
    // Hộp xác nhận lưu và gửi duyệt -> Hủy
    await h.btn('Lưu và gửi duyệt').first().click(); await h.wait(1200);
    let m = h.modal(); await h.mouseOut();
    await h.el('14_confirm_send', m, 0);
    await h.icon('btn_confirm_xacnhan', m.locator('button', { hasText: 'Xác nhận' }).first());
    await h.icon('btn_huy_confirm', m.locator('button', { hasText: 'Hủy' }).first());
    await m.locator('button', { hasText: 'Hủy' }).first().click(); await h.wait(1000);
    // Thêm dòng + chọn khách hàng
    await page.locator('a[title="Thêm dòng"]').first().click();
    await h.wait(600);
    await h.icon('btn_xoadong', page.locator('a[title="Xóa dòng"]').first(), 4);
    await h.icon('o_chonkhachhang', page.locator('input[placeholder^="Nhấn vào đây để chọn khách hàng"]').first(), 1);
    await page.locator('input[placeholder^="Nhấn vào đây để chọn khách hàng"]').first().click();
    await h.wait(3000);
    m = h.modal();
    await m.locator('input[placeholder="Nhập tên / mã khách hàng"]').fill(process.env.KH || '35TNIBTR-12');
    await m.locator('button', { hasText: 'Tìm kiếm' }).first().click();
    await h.wait(3500);
    await h.mouseOut();
    await h.el('11_customer', m, 0);
    await h.icon('btn_dong_kh', m.locator('button', { hasText: 'Đóng' }).last());
    await m.locator('tbody tr').first().click(); await h.wait(1500);
    // Chọn hợp đồng
    await h.icon('o_chonhopdong', page.locator('table.detail-table tbody tr').first().locator('td').nth(2).locator('input'), 1);
    await page.locator('table.detail-table tbody tr').first().locator('td').nth(2).locator('input').click();
    await h.wait(4000);
    m = h.modal(); await h.mouseOut();
    await h.el('12_contract', m, 0);
    await h.icon('btn_dong_hd', m.locator('button', { hasText: 'Đóng' }).last());
    const rows = m.locator('.contract-table tbody tr');
    const n = await rows.count();
    console.log('contract rows', n);
    if (n && !(await rows.first().innerText()).includes('Không có')) { await rows.first().click(); await h.wait(1500); }
    else { await m.locator('button', { hasText: 'Đóng' }).last().click(); await h.wait(600); }
    const r0 = page.locator('table.detail-table tbody tr').first();
    await r0.locator('td').nth(4).locator('input').first().fill('15000000').catch((e) => console.log('WARN amount', e.message.split('\n')[0]));
    await r0.locator('input[placeholder="Ghi chú"]').fill('Thu đợt 1').catch(() => {});
    await page.locator('input[placeholder="Nhập lý do thu"]').first().fill('Thu tiền hàng theo hợp đồng');
    await h.wait(800);
    await h.full('10b_filled');
    // Đổi loại thu khi đã có dòng -> hộp xác nhận -> Hủy
    await pickType(page, h, 'Thu nhà cung cấp');
    m = h.modal(); await h.mouseOut();
    await h.el('13b_changetype', m, 0);
    await m.locator('button', { hasText: 'Hủy' }).first().click(); await h.wait(800);
    // Cảnh báo chưa lưu -> Ở lại
    await h.btn('Quay lại').first().click(); await h.wait(1200);
    m = h.modal(); await h.mouseOut();
    await h.el('15_unsaved', m, 0);
    await m.locator('button', { hasText: 'Ở lại' }).first().click().catch(() => {}); await h.wait(600);
  },
  async supplier(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await go(LIST + '/create');
    await page.locator('a[title="Thêm dòng"]').first().waitFor();
    await h.wait(1200);
    await pickType(page, h, 'Thu nhà cung cấp');
    await page.locator('a[title="Thêm dòng"]').first().click(); await h.wait(600);
    await page.locator('input[placeholder^="Nhấn vào đây để chọn nhà cung cấp"]').first().click(); await h.wait(3500);
    const m = h.modal(); await h.mouseOut();
    await h.el('11b_supplier', m, 0);
  },
  async detail(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await go(LIST + '/' + WAIT_ID);
    await page.getByText('DNTT', { exact: false }).first().waitFor();
    await h.wait(2500);
    await h.full('17_detail');
    await h.icon('btn_taophieuthu', h.btn('Tạo phiếu thu').first());
    await h.icon('btn_in', h.btn('In phiếu').first());
    await h.icon('btn_khongduyet', h.btn('Không duyệt').first());
    await h.icon('btn_xemlichsu', h.btn('Xem lịch sử').first());
    await h.btn('Không duyệt').first().click(); await h.wait(1200);
    let m = h.modal(); await h.mouseOut();
    await h.el('15_reject', m, 0);
    await h.icon('btn_confirm_khongduyet', m.locator('button', { hasText: 'Không duyệt' }).last());
    await h.icon('btn_dong_reject', m.locator('button', { hasText: 'Đóng' }).last());
    await m.locator('button', { hasText: 'Đóng' }).last().click(); await h.wait(800);
    await h.btn('In phiếu').first().click(); await h.wait(2000); await page.getByText('Đang tải dữ liệu in').waitFor({ state: 'hidden', timeout: 60000 }).catch(() => {}); await h.wait(3000);
    m = h.modal(); await h.mouseOut();
    await h.el('18_print', m, 0);
    await h.icon('btn_in_preview', m.locator('button', { hasText: /^\s*In\s*$/ }).first());
  },
  async detailrej(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await forceCanEdit(page);
    await go(LIST + '/' + REJ_ID);
    await page.getByText('DNTT', { exact: false }).first().waitFor();
    await h.wait(2500);
    await h.icon('btn_sua', h.btn('Sửa').first());
    await h.icon('btn_xoa', h.btn('Xóa').first());
    await h.btn('Xem lịch sử').first().click(); await h.wait(3000);
    await h.full('17b_detail_history');
    await page.unrouteAll({ behavior: 'ignoreErrors' });
    await go(LIST + '/' + REJ_ID + '/edit');
    await page.locator('a[title="Thêm dòng"]').first().waitFor();
    await h.wait(2500);
    await h.full('19_edit');
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

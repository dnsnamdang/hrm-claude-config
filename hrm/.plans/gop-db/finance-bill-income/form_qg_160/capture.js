// Chụp ảnh HDSD/SRS màn Phiếu thu tiền trên DEV (headless riêng, đăng nhập sẵn).
// AN TOÀN: chỉ mở màn / popup / hộp xác nhận rồi bấm Hủy / Đóng. KHÔNG bấm Xác nhận, Lưu, Duyệt, Xóa.
// Dev không có phiếu Đang tạo / Chờ duyệt → nút Sửa/Xóa/Duyệt được BẬT TẠM HIỂN THỊ bằng cách sửa cờ
// is_can_edit / is_can_delete / is_can_approve (+ trạng thái) trong phản hồi GET (chỉ trên trình duyệt,
// không ghi dữ liệu).
// Chạy: node capture.js [tên bước ...]   (không truyền = chụp hết)
const fs = require('fs');
const path = require('path');
const { open } = require('./devlib.js');

const SHOTS = path.join(__dirname, 'hdsd_shots');
const ICONS = path.join(SHOTS, 'icons');
fs.mkdirSync(ICONS, { recursive: true });
const LIST = '/finance/bill-incomes';
const DETAIL_ID = Number(process.env.DETAIL_ID || 2836);
const ONLY = process.argv.slice(2);

function mk(page) {
  const h = {};
  h.wait = (ms) => page.waitForTimeout(ms);
  // (5,5) nằm trên thanh menu trái -> hover làm bung menu đè lên màn; đưa chuột lên giữa thanh tiêu đề.
  h.mouseOut = async () => { const vp = page.viewportSize(); await page.mouse.move(Math.round(vp.width * 0.55), 5); await page.waitForTimeout(600); };
  h.clip = async (name, box, pad = 0, dir = SHOTS) => {
    const vp = page.viewportSize();
    const x = Math.max(0, box.x - pad), y = Math.max(0, box.y - pad);
    const w = Math.min(vp.width - x, box.width + 2 * pad), hh = Math.min(vp.height - y, box.height + 2 * pad);
    await page.screenshot({ path: path.join(dir, name + '.png'), clip: { x, y, width: w, height: hh } });
  };
  h.el = async (name, loc, pad = 0) => { await loc.scrollIntoViewIfNeeded().catch(() => {}); const b = await loc.boundingBox(); if (!b) throw new Error('Không thấy ' + name); await h.clip(name, b, pad); };
  h.icon = async (name, loc, pad = 2) => { await loc.scrollIntoViewIfNeeded().catch(() => {}); const b = await loc.boundingBox(); if (!b) throw new Error('Không thấy icon ' + name); await h.clip(name, b, pad, ICONS); };
  h.full = async (name) => { await h.mouseOut(); await page.screenshot({ path: path.join(SHOTS, name + '.png') }); };
  h.page = async (name) => { await h.mouseOut(); await page.screenshot({ path: path.join(SHOTS, name + '.png'), fullPage: true }); };
  h.btn = (text) => page.locator('button:visible, a.btn:visible').filter({ hasText: new RegExp('^\\s*' + text + '\\s*$') });
  h.modal = () => page.locator('.modal.show .modal-content').last();
  return h;
}

// Bật tạm cờ trong phản hồi GET (chỉ hiển thị). flags: {is_can_edit, ..., status, status_text}
async function force(page, flags, onlyFirst) {
  await page.route(/\/api\/v1\/finance\/bill-incomes(\/\d+)?(\?.*)?$/, async (route) => {
    const req = route.request();
    if (req.method() !== 'GET') return route.continue();
    const res = await route.fetch();
    let j = await res.json().catch(() => null);
    if (!j) return route.fulfill({ response: res });
    const fix = (o) => { if (o && typeof o === 'object') Object.assign(o, flags); };
    if (Array.isArray(j.data)) { (onlyFirst ? j.data.slice(0, 1) : j.data).forEach(fix); } else if (j.data) fix(j.data); else fix(j);
    return route.fulfill({ response: res, json: j });
  });
}

async function waitList(page, h) {
  await page.locator('a.v2-cell-link', { hasText: '.PT' }).first().waitFor({ timeout: 60000 });
  await h.wait(1500);
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
    await h.icon('menu_muc', page.locator('.row-nm', { hasText: /^\s*Phiếu thu\s*$/ }).first().locator('xpath=..'), 2);
  },
  async list(page, h, go) {
    await page.setViewportSize({ width: 1080, height: 675 });
    await go(LIST);
    await waitList(page, h);
    await h.full('01_list');
    await h.icon('btn_timkiem', h.btn('Tìm kiếm').first());
    await h.icon('btn_lammoi', h.btn('Làm mới').first());
    await h.icon('btn_timkiemnangcao', h.btn('Tìm kiếm nâng cao').first());
    await h.icon('btn_caidatboloc', h.btn('Cài đặt bộ lọc').first());
    await h.icon('btn_taomoi', h.btn('Tạo mới').first());
    await h.icon('btn_cauhinhcot', page.locator('button[title="Cấu hình cột hiển thị"]').first());
    await h.icon('o_timnhanh', page.locator('input[placeholder^="Tìm theo mã phiếu"]').first(), 2);
    await h.icon('btn_in_row', page.locator('.v2-row-actions span[title="In"]').first()).catch(e => console.log('WARN in_row', e.message));
    await h.icon('btn_excel_row', page.locator('.v2-row-actions span[title="Xuất Excel"]').first()).catch(e => console.log('WARN excel_row', e.message));
    await h.icon('btn_lichsu_row', page.locator('.v2-row-actions span[title="Lịch sử"]').first()).catch(e => console.log('WARN ls_row', e.message));
    // Bộ lọc nâng cao
    await h.btn('Tìm kiếm nâng cao').first().click();
    await h.wait(1500);
    await h.mouseOut();
    const card = page.locator('section.smart-filter-card').first();
    await h.el('02_filter', card, 0);
    const fld = (t) => card.locator('.ff').filter({ has: page.locator('label.ff__label', { hasText: t }) }).first();
    for (const [n, t] of [['o_congty', 'Công ty'], ['o_madenghi', 'Mã phiếu đề nghị thu'], ['o_loaithu', 'Loại thu'], ['o_trangthai', 'Trạng thái'], ['o_nguoitao', 'Người tạo'], ['o_nguoidenghi', 'Người đề nghị'], ['o_khachhang', 'Khách hàng'], ['o_hopdong', 'Số hợp đồng'], ['o_sotien', 'Số tiền'], ['o_ngaylap', 'Ngày lập']]) {
      try { await h.icon(n, fld(t), 1); } catch (e) { console.log('WARN', n, e.message.split('\n')[0]); }
    }
  },
  async rowmenu(page, h, go) {
    await page.setViewportSize({ width: 1080, height: 675 });
    await force(page, { is_can_edit: true, is_can_delete: true, status: 1, status_text: 'Đang tạo', status_type: 'danger' }, true);
    await go(LIST);
    await waitList(page, h);
    const more = page.locator('.v2-row-actions').first().locator('button[title="Hành động khác"], span:not([title]) button').last();
    await h.icon('btn_bacham_row', more);
    await more.click(); await h.wait(800);
    const menu = page.locator('.v2-row-actions__menu:visible').first();
    for (const [n, t] of [['item_in', 'In'], ['item_excel', 'Xuất Excel'], ['item_lichsu', 'Lịch sử']]) {
      await h.icon(n, menu.locator('.v2-row-actions__item').filter({ hasText: new RegExp('^\\s*' + t + '\\s*$') }).first(), 1).catch(e => console.log('WARN', n, e.message.split('\n')[0]));
    }
    await page.keyboard.press('Escape');
    await page.unrouteAll({ behavior: 'ignoreErrors' });
  },
  async rowicons(page, h, go) {
    await page.setViewportSize({ width: 1080, height: 675 });
    await force(page, { is_can_edit: true, is_can_delete: true, status: 1, status_text: 'Đang tạo', status_type: 'danger' }, true);
    await go(LIST);
    await waitList(page, h);
    await h.icon('btn_sua_row', page.locator('.v2-row-actions span[title="Sửa"]').first());
    await h.icon('btn_xoa_row', page.locator('.v2-row-actions span[title="Xóa"]').first());
    await page.locator('.v2-row-actions span[title="Xóa"]').first().locator('button, a').first().click();
    await h.wait(1200);
    const m = h.modal();
    await h.mouseOut();
    await h.el('13_delete', m, 0);
    await h.icon('btn_confirm_xoa', m.locator('button', { hasText: 'Xóa' }).last());
    await h.icon('btn_huy_confirm', m.locator('button', { hasText: 'Hủy' }).first());
    await m.locator('button', { hasText: 'Hủy' }).first().click();
    await h.wait(800);
    await page.unrouteAll({ behavior: 'ignoreErrors' });
    // Nút Duyệt trên dòng (phiếu Chờ duyệt)
    await force(page, { is_can_approve: true, status: 2, status_text: 'Chờ duyệt', status_type: 'danger' }, true);
    await go(LIST);
    await waitList(page, h);
    await h.icon('btn_duyet_row', page.locator('.v2-row-actions span[title="Duyệt"]').first()).catch(e => console.log('WARN duyet_row', e.message));
    await page.unrouteAll({ behavior: 'ignoreErrors' });
  },
  async history(page, h, go) {
    await page.setViewportSize({ width: 1080, height: 675 });
    await go(LIST);
    await waitList(page, h);
    const n = await page.locator('.v2-row-actions span[title="Lịch sử"]').count();
    for (let i = 0; i < n; i++) {
      await page.locator('.v2-row-actions span[title="Lịch sử"]').nth(i).locator('button, a').first().click();
      await h.wait(2500);
      const m = h.modal();
      const empty = await m.getByText('Chưa có lịch sử', { exact: false }).count();
      console.log('history row', i, empty ? 'EMPTY' : 'CÓ');
      if (!empty) {
        await h.mouseOut();
        await h.el('16_history', m, 0);
        await h.icon('btn_boloc_ls', m.locator('button', { hasText: 'Bộ lọc' }).first()).catch(e => console.log('WARN boloc', e.message));
        await h.icon('btn_dong_ls', m.locator('button', { hasText: 'Đóng' }).last()).catch(e => console.log('WARN dong', e.message));
        break;
      }
      await m.locator('button', { hasText: 'Đóng' }).last().click(); await h.wait(800);
    }
  },
  async colcfg(page, h, go) {
    await page.setViewportSize({ width: 1080, height: 675 });
    await go(LIST);
    await waitList(page, h);
    await page.locator('button[title="Cấu hình cột hiển thị"]').first().click();
    await h.wait(1500);
    const m = h.modal();
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
    const f = h.modal();
    await h.mouseOut();
    await h.el('26_filtercfg', f, 0);
    await h.icon('btn_luu', f.locator('button', { hasText: 'Lưu' }).last());
    await h.icon('btn_khoiphuc', f.locator('button', { hasText: 'Khôi phục' }).first());
    await h.icon('btn_dong_filtercfg', f.locator('button', { hasText: 'Đóng' }).last());
    await f.locator('button', { hasText: 'Đóng' }).last().click();
  },
  async create(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await go(LIST + '/create');
    await page.locator('input[placeholder^="Nhấn vào đây"]').first().waitFor();
    await h.wait(2500);
    await h.page('10_create');
    await h.icon('btn_luu_form', h.btn('Lưu').first());
    await h.icon('btn_luuguiduyet', h.btn('Lưu và gửi duyệt').first());
    await h.icon('btn_luutieptuc', h.btn('Lưu và tiếp tục').first()).catch(e => console.log('WARN tieptuc', e.message));
    await h.icon('btn_quaylai', h.btn('Quay lại').first());
    await h.icon('o_sophieudenghi', page.locator('input[placeholder^="Nhấn vào đây"]').first(), 1);
    // Hộp xác nhận Lưu và gửi duyệt → chụp → Hủy
    await h.btn('Lưu và gửi duyệt').first().click();
    await h.wait(1200);
    let m = h.modal();
    await h.mouseOut();
    await h.el('14_sendapprove', m, 0);
    await h.icon('btn_confirm_xacnhan', m.locator('button', { hasText: 'Xác nhận' }).first());
    await m.locator('button', { hasText: 'Hủy' }).first().click();
    await h.wait(1000);
    // Popup chọn phiếu đề nghị thu
    await page.locator('input[placeholder^="Nhấn vào đây"]').first().click();
    await h.wait(3500);
    m = h.modal();
    await h.mouseOut();
    await h.el('11_request', m, 0);
    await h.icon('btn_dong_req', m.locator('button', { hasText: 'Đóng' }).last()).catch(e => console.log('WARN', e.message));
    const rows = await m.locator('tbody tr.tr-hover').count();
    console.log('so phieu de nghi du dieu kien:', rows);
    if (rows) {
      await m.locator('tbody tr.tr-hover').first().click();   // chỉ nạp dữ liệu về form, KHÔNG lưu
      await h.wait(3500);
      await h.page('10b_filled');
    } else {
      await m.locator('button', { hasText: 'Đóng' }).last().click();
    }
  },
  async edit(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await force(page, { is_can_edit: true, is_can_delete: true, is_can_approve: false, status: 1, status_text: 'Đang tạo', status_type: 'danger' }, false);
    await go(LIST + '/' + DETAIL_ID);
    await page.getByText('.PT', { exact: false }).first().waitFor();
    await h.wait(2500);
    await h.icon('btn_sua', h.btn('Sửa').first());
    await h.icon('btn_xoa', h.btn('Xóa').first());
    await go(LIST + '/' + DETAIL_ID + '/edit');
    await h.wait(3500);
    await h.page('12_edit');
    await page.unrouteAll({ behavior: 'ignoreErrors' });
  },
  async approve(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await force(page, { is_can_edit: false, is_can_delete: false, is_can_approve: true, status: 2, status_text: 'Chờ duyệt', status_type: 'danger' }, false);
    await go(LIST + '/' + DETAIL_ID);
    await page.getByText('.PT', { exact: false }).first().waitFor();
    await h.wait(3000);
    await h.page('15_approve');
    await h.icon('btn_duyet', h.btn('Duyệt phiếu thu').first());
    await h.icon('btn_huyphieu', h.btn('Hủy phiếu thu').first());
    await h.icon('btn_phanbo', h.btn('Phân bổ').first());
    await h.icon('o_phanbo', page.locator('input[placeholder^="Nhập tổng tiền thực nhận"]').first(), 1);
    // Hộp xác nhận duyệt → chụp → Hủy
    await h.btn('Duyệt phiếu thu').first().click();
    await h.wait(1200);
    let m = h.modal();
    await h.mouseOut();
    await h.el('15b_confirm', m, 0);
    await h.icon('btn_confirm_duyet', m.locator('button', { hasText: 'Duyệt' }).last());
    await m.locator('button', { hasText: 'Hủy' }).first().click();
    await h.wait(1000);
    // Popup hủy phiếu → chụp → Đóng
    await h.btn('Hủy phiếu thu').first().click();
    await h.wait(1500);
    m = h.modal();
    await h.mouseOut();
    await h.el('16_cancel', m, 0);
    await h.icon('btn_confirm_huy', m.locator('button', { hasText: 'Xác nhận' }).first());
    await h.icon('btn_dong_cancel', m.locator('button', { hasText: 'Đóng' }).last());
    await m.locator('button', { hasText: 'Đóng' }).last().click();
    await h.wait(800);
    await page.unrouteAll({ behavior: 'ignoreErrors' });
  },
  async detail(page, h, go) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await go(LIST + '/' + DETAIL_ID);
    await page.getByText('.PT', { exact: false }).first().waitFor();
    await h.wait(2500);
    await h.page('17_detail');
    await h.icon('btn_in', h.btn('In').first());
    await h.icon('btn_xuatexcel', h.btn('Xuất Excel').first());
    await h.icon('btn_xemlichsu', h.btn('Xem lịch sử').first()).catch(e => console.log('WARN xemls', e.message));
    await h.btn('In').first().click();
    await h.wait(4000);
    const m = h.modal();
    await h.mouseOut();
    await h.el('18_print', m, 0);
    await h.icon('btn_in_preview', m.locator('button', { hasText: /^\s*In\s*$/ }).last()).catch(e => console.log('WARN inprev', e.message));
    await h.icon('btn_dong_print', m.locator('button', { hasText: 'Đóng' }).last()).catch(e => console.log('WARN dongprint', e.message));
  },
};

(async () => {
  const { browser, page, go } = await open(__dirname, { scale: 1 });
  const h = mk(page);
  for (const [k, fn] of Object.entries(STEPS)) {
    if (ONLY.length && !ONLY.includes(k)) continue;
    try { await fn(page, h, go); console.log('OK', k); } catch (e) { console.log('FAIL', k, e.message.split('\n')[0]); }
    await page.unrouteAll({ behavior: 'ignoreErrors' }).catch(() => {});
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });

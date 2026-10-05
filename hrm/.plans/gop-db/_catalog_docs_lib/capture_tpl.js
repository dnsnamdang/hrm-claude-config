async (page) => {
  if (!page.__dlg) { page.__dlg = true; page.on('dialog', d => d.accept().catch(() => {})); }
  // Chụp ảnh chuẩn cho 1 màn danh mục (popup). Tham số thay bởi Python: __PARAMS__
  const P = __PARAMS__;
  const D = P.dir;                 // thư mục ảnh (tương đối .playwright-mcp)
  const log = [];
  const W = (ms) => page.waitForTimeout(ms);
  const shot = async (name, opts = {}) => { try { await page.screenshot({ path: D + name, ...opts }); log.push(name); } catch (e) { log.push(name + ':ERR ' + e.message.slice(0, 60)); } };
  const eshot = async (loc, name) => { try { await loc.first().screenshot({ path: D + name }); log.push(name); } catch (e) { log.push(name + ':ERR'); } };
  const closeModal = async () => {
    for (let i = 0; i < 3; i++) {
      const thoat = page.locator('.modal.show button:has-text("Thoát")');
      if (await thoat.count()) { await thoat.first().click(); await W(700); continue; }
      const dong = page.locator('.modal.show button:has-text("Đóng"), .modal.show button:has-text("Hủy")');
      if (await dong.count()) { await dong.last().click(); await W(700); continue; }
      const x = page.locator('.modal.show .close');
      if (await x.count()) { await x.first().click(); await W(700); continue; }
      break;
    }
    await page.keyboard.press('Escape'); await W(300);
  };
  const gotoList = async () => {
    await page.goto(P.base + P.route, { waitUntil: 'domcontentloaded' });
    await page.waitForSelector('tbody tr', { timeout: 90000 });
    // chờ hết dòng "Đang tải dữ liệu..." (dòng loading cũng là tbody tr)
    await page.waitForFunction(() => document.querySelectorAll('tbody tr .v2-row-actions').length > 0, null, { timeout: 90000 }).catch(() => {});
    await W(1500);
  };
  const rowWith = async (pred) => {
    const rows = page.locator('tbody tr');
    const n = await rows.count();
    for (let i = 0; i < n; i++) {
      const r = rows.nth(i);
      if (await pred(r)) return r;
    }
    return null;
  };
  const openMenuItem = async (row, text) => {
    const more = row.locator('button[title="Hành động khác"]');
    if (await more.count()) { await more.first().click(); await W(600);
      const it = page.locator('.v2-row-actions__item:visible', { hasText: text });
      if (await it.count()) { await it.first().click(); await W(1200); return true; }
      await page.keyboard.press("Escape"); await page.mouse.click(1420, 845); await W(300);
    }
    return false;
  };
  const clickAction = async (row, icon, text) => {
    const b = row.locator(`td:last-child .${icon}`);
    if (await b.count()) { await b.first().click(); await W(1200); return true; }
    return await openMenuItem(row, text);
  };

  await page.setViewportSize({ width: 1440, height: 860 });
  await gotoList();
  await shot('01_list.png');

  // icon menu: phân hệ + nhóm + mục
  if (P.menu) {
    try {
      await eshot(page.locator('text=' + P.menu.phanhe).locator('xpath=..'), '../icons/menu_phanhe.png');
      const grp = page.locator('a, div, li').filter({ hasText: new RegExp('^\\s*' + P.menu.nhom + '\\s*$') }).locator('visible=true');
      await eshot(grp, '../icons/menu_nhom.png');
      await grp.first().click(); await W(900);
      try {
        const bb = await page.locator(`text="${P.menu.muc}"`).first().boundingBox();
        await page.screenshot({ path: D + '../icons/menu_muc.png', clip: { x: bb.x - 34, y: bb.y - 8, width: bb.width + 46, height: bb.height + 16 } });
        log.push('menu_muc');
      } catch (e) { log.push('menu_muc:ERR'); }
      await shot('02_menu.png');
      await page.keyboard.press('Escape'); await page.mouse.click(1300, 820); await W(500);
    } catch (e) { log.push('menu:ERR ' + e.message.slice(0, 80)); }
    await gotoList();
  }

  // bộ lọc
  await eshot(page.locator('section.smart-filter-card, .smart-filter-card').first(), 'filter.png');
  // nút ba chấm (dòng có nhiều nút)
  const rMore = await rowWith(async r => (await r.locator('button[title="Hành động khác"]').count()) > 0);
  if (rMore) { await rMore.locator('button[title="Hành động khác"]').click(); await W(700); await shot('03_rowmenu.png'); await page.keyboard.press("Escape"); await page.mouse.click(1420, 845); await W(400); }
  else { await eshot(page.locator('tbody tr').first().locator('td:last-child'), '03_rowmenu.png'); }

  // tìm nhanh theo chữ của dòng đầu
  if (P.search) {
    const q = page.locator('input[placeholder^="' + P.search + '"]');
    if (await q.count()) { await q.first().fill(P.searchText || ''); await q.first().press('Enter'); await W(2500); await shot('04_filter_result.png'); await q.first().fill(''); await q.first().press('Enter'); await W(2000); }
  }

  // Tạo mới + lỗi
  if (P.create !== false) {
    await page.locator('button:has-text("Tạo mới")').first().click(); await W(2500);
    await shot('10_create.png');
    const save = page.locator('.modal.show button').filter({ hasText: /^\s*Lưu\s*$/ });
    if (await save.count()) { await save.first().click(); await W(2000); await shot('11_create_error.png'); }
    if (P.codeInput) {
      const ci = page.locator(`.modal.show input[placeholder="${P.codeInput}"]`);
      if (await ci.count()) { await ci.first().fill('mã sai định dạng'); await W(1200); await shot('11b_code_error.png'); }
    }
    await closeModal();
  }

  await gotoList();
  // Sửa (dòng đầu đang Hoạt động có nút sửa)
  const rEdit = await rowWith(async r => (await r.locator('td:last-child .ri-edit-line').count()) > 0);
  if (rEdit) { await rEdit.locator('td:last-child .ri-edit-line').first().click(); await W(2500); await shot('12_edit.png'); await closeModal(); }
  // Xem chi tiết
  if (P.detailCol !== undefined) {
    const link = page.locator('tbody tr').first().locator('td').nth(P.detailCol).locator('.v2-cell-link, a').first();
    if (await link.count()) { await link.click(); await W(2500); await shot('17_detail.png'); await closeModal(); }
  }
  // Xoá
  const rDel = await rowWith(async r => (await r.locator('td:last-child .ri-delete-bin-line, td:last-child .ri-delete-bin-6-line').count()) > 0);
  if (rDel) { await rDel.locator('td:last-child .ri-delete-bin-line, td:last-child .ri-delete-bin-6-line').first().click(); await W(1200); await shot('13_delete.png'); await closeModal(); }
  // Khoá thật 1 bản ghi mẫu (P.lockName) để có dòng Khóa cho ảnh Mở khóa
  if (P.lockName) {
    const rl = await rowWith(async r => (await r.innerText()).includes(P.lockName) && (await r.innerText()).includes('Hoạt động'));
    if (rl && await clickAction(rl, 'ri-lock-line', 'Khóa')) {
      const ok = page.locator('.modal.show .modal-footer button, .modal.show footer button');
      if (await ok.count()) { await ok.first().click(); await W(2500); log.push('locked ' + P.lockName); }
      await gotoList();
    }
  }
  // Khoá
  if (P.lock !== false) {
    const rAct = await rowWith(async r => (await r.innerText()).includes('Hoạt động'));
    if (rAct && await clickAction(rAct, 'ri-lock-line', 'Khóa')) { await shot('14_lock.png'); await closeModal(); }
    const rLck = await rowWith(async r => /\tKhóa\t|Khóa\s*$/.test(await r.innerText()));
    if (rLck && await clickAction(rLck, 'ri-lock-unlock-line', 'Mở khóa')) { await shot('15_unlock.png'); await closeModal(); }
  }
  // Lịch sử
  const r0 = page.locator('tbody tr').first();
  if (await clickAction(r0, 'ri-history-line', 'Lịch sử')) { await W(1500); await shot('16_history.png'); await closeModal(); }

  // Xuất Excel
  const bx = page.locator('button:has-text("Xuất Excel")');
  if (await bx.count()) { await bx.first().click(); await W(1500); await shot('20_export.png'); await closeModal(); }

  // Import
  const bi = page.locator('button:has-text("Import Excel")');
  if (await bi.count()) {
    await bi.first().click(); await W(1800); await shot('21_import_open.png');
    try {
      const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 30000 }), page.locator('.modal.show button:has-text("Tải file mẫu")').click()]);
      await dl.saveAs(D + 'mau_import.xlsx'); log.push('mau_import.xlsx');
    } catch (e) { log.push('mau:ERR'); }
    if (P.importFile) {
      await page.locator('.modal.show input[type=file]').setInputFiles(P.importFile); await W(800);
      await page.locator('.modal.show button:has-text("Load lên bảng")').click(); await W(2500); await shot('22_import_loaded.png');
      await page.locator('.modal.show button:has-text("Validate")').first().click(); await W(5000); await shot('23_import_validated.png');
    }
    await closeModal();
  }
  // Cấu hình cột
  const bc = page.locator('button[title="Cấu hình cột hiển thị"]');
  if (await bc.count()) { await bc.first().click(); await W(1200); await shot('25_colcfg.png'); await closeModal(); }
  return log;
}

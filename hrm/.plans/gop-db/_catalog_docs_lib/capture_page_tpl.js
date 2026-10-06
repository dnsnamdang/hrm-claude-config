async (page) => {
  if (!page.__dlg) { page.__dlg = true; page.on('dialog', d => d.accept().catch(() => {})); }
  // Chụp ảnh cho màn danh mục có form Thêm/Sửa/Xem là TRANG RIÊNG (không phải popup).
  const P = __PARAMS__;
  const D = P.dir, log = [];
  const W = (ms) => page.waitForTimeout(ms);
  const shot = async (n) => { try { await page.screenshot({ path: D + n }); log.push(n); } catch (e) { log.push(n + ':ERR'); } };
  const eshot = async (loc, n) => { try { await loc.first().screenshot({ path: D + n }); log.push(n); } catch (e) { log.push(n + ':ERR'); } };
  const esc = async () => { await page.keyboard.press('Escape'); await W(300); };
  const closeM = async () => { for (let i = 0; i < 3; i++) { const b = page.locator('.modal.show button').filter({ hasText: /^\s*(Hủy|Đóng|Thoát)\s*$/ }); if (await b.count()) { await b.last().click(); await W(700); } else break; } await esc(); };
  const list = async (q) => {
    await page.goto(P.base + P.route, { waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => document.querySelectorAll('tbody tr .v2-row-actions').length > 0, null, { timeout: 90000 }).catch(() => {});
    await W(1500);
    if (q) { const s = page.locator('input[placeholder^="' + P.search + '"]').first(); await s.fill(q); await s.press('Enter'); await W(3000); }
  };
  const act = async (text, icon) => {
    const rows = page.locator('tbody tr');
    for (let i = 0; i < await rows.count(); i++) {
      const r = rows.nth(i);
      const d = r.locator(`td:last-child [title="${text}"] button, td:last-child button[title="${text}"]` + (icon ? `, td:last-child .${icon}` : ''));
      if (await d.count()) { await d.first().click(); await W(1500); return true; }
      const more = r.locator('button[title="Hành động khác"]');
      if (await more.count()) { await more.first().click(); await W(600); const it = page.locator('.v2-row-actions__item:visible', { hasText: text }); if (await it.count()) { await it.first().click(); await W(1500); return true; } await esc(); }
    }
    return false;
  };
  await page.setViewportSize({ width: 1440, height: 860 });
  await list(); await shot('01_list.png');
  if (P.menu) {
    try {
      await eshot(page.locator('text=' + P.menu.phanhe).locator('xpath=..'), '../icons/menu_phanhe.png');
      if (P.menu.nhom) {
        const grp = page.locator('a, div, li').filter({ hasText: new RegExp('^\\s*' + P.menu.nhom + '\\s*$') }).locator('visible=true');
        await eshot(grp, '../icons/menu_nhom.png'); await grp.first().click(); await W(900);
      }
      const bb = await page.locator(`text="${P.menu.muc}"`).first().boundingBox();
      await page.screenshot({ path: D + '../icons/menu_muc.png', clip: { x: bb.x - 34, y: bb.y - 8, width: bb.width + 46, height: bb.height + 16 } });
      await shot('02_menu.png'); await esc();
    } catch (e) { log.push('menu:ERR'); }
    await list();
  }
  await eshot(page.locator('section.smart-filter-card, .smart-filter-card'), 'filter.png');
  const rm = page.locator('tbody tr button[title="Hành động khác"]').first();
  if (await rm.count()) { await rm.click(); await W(700); await shot('03_rowmenu.png'); await esc(); }
  else await eshot(page.locator('tbody tr').first().locator('td:last-child'), '03_rowmenu.png');
  if (P.search && P.searchText) { const s = page.locator('input[placeholder^="' + P.search + '"]').first(); await s.fill(P.searchText); await s.press('Enter'); await W(3000); await shot('04_filter_result.png'); }
  // Tạo mới (trang riêng)
  if (P.create !== false) {
    await list(); await page.locator('button:has-text("Tạo mới")').first().click(); await W(4000); await shot('10_create.png');
    const save = page.locator('button').filter({ hasText: /^\s*Lưu\s*$/ }).first();
    if (await save.count()) { await save.click(); await W(2500); await shot('11_create_error.png'); }
  }
  // Sửa / Xem
  await list();
  if (await act('Sửa', 'ri-edit-line')) { await W(3000); await shot('12_edit.png'); }
  await list();
  const link = page.locator('tbody tr').first().locator('td').nth(P.detailCol || 1).locator('.v2-cell-link, a').first();
  if (await link.count()) { await link.click(); await W(4000); await shot('17_detail.png'); }
  // Xoá (chỉ mở hộp xác nhận rồi Hủy)
  await list();
  if (await act('Xóa', 'ri-delete-bin-line')) { await shot('13_delete.png'); await closeM(); }
  // Khoá thật bản ghi mẫu rồi chụp Mở khoá
  if (P.lockSearch) {
    await list(P.lockSearch);
    if (await act('Khóa', 'ri-lock-line')) { await shot('14_lock.png');
      const ok = page.locator('.modal.show .modal-footer button, .modal.show footer button'); if (await ok.count()) { await ok.first().click(); await W(3000); log.push('locked'); } }
    await list(P.lockSearch);
    if (await act('Mở khóa', 'ri-lock-unlock-line')) { await shot('15_unlock.png'); await closeM(); }
  }
  await list();
  if (await act('Lịch sử', 'ri-history-line')) { await W(1500); await shot('16_history.png'); await closeM(); }
  await list();
  const bx = page.locator('button:has-text("Xuất Excel")'); if (await bx.count()) { await bx.first().click(); await W(1800); await shot('20_export.png'); await closeM(); }
  const bi = page.locator('button:has-text("Import Excel")');
  if (await bi.count()) { await bi.first().click(); await W(1800); await shot('21_import_open.png');
    try { const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 30000 }), page.locator('.modal.show button:has-text("Tải file mẫu")').click()]); await dl.saveAs(D + 'mau_import.xlsx'); log.push('mau'); } catch (e) { log.push('mau:ERR'); }
    await closeM(); }
  const bc = page.locator('button[title="Cấu hình cột hiển thị"]'); if (await bc.count()) { await bc.first().click(); await W(1200); await shot('25_colcfg.png'); await closeM(); }
  return log;
}

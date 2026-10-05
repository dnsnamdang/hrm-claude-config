async (page) => {
  if (!page.__dlg) { page.__dlg = true; page.on('dialog', d => d.accept().catch(() => {})); }
  // Chạy luồng Import trên màn danh mục: Load → Validate (chụp lỗi) → Bỏ dòng lỗi → Validate → Import
  const P = __PARAMS__; const D = P.dir; const log = []; const W = (ms) => page.waitForTimeout(ms);
  const shot = async (n) => { await page.screenshot({ path: D + n }); log.push(n); };
  await page.goto(P.base + P.route, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('tbody tr', { timeout: 90000 }); await page.waitForFunction(() => document.querySelectorAll('tbody tr .v2-row-actions').length > 0, null, { timeout: 90000 }).catch(() => {}); await W(1500);
  await page.locator('button:has-text("Import Excel")').first().click(); await W(1800);
  const m = page.locator('.modal.show');
  await m.locator('input[type=file]').setInputFiles(P.file); await W(800);
  await m.locator('button:has-text("Load lên bảng")').click(); await W(2500); await shot('22_import_loaded.png');
  await m.locator('button:has-text("Validate")').first().click(); await W(1500); await page.waitForFunction(() => /Validate xong:|Validate thành công/.test(document.querySelector('.modal.show')?.innerText || '') && !document.querySelector('.modal.show .spinner-border, .modal.show .loading, .modal.show [class*=spinner]'), null, { timeout: 90000 }).catch(() => {}); await W(1500); await shot('23_import_validated.png');
  log.push((await m.innerText()).slice(0, 600));
  if (P.doImport) {
    const drop = m.locator('button:has-text("Bỏ dòng lỗi")');
    if (await drop.count()) { await drop.first().click(); await W(1500); }
    await m.locator('button:has-text("Validate")').first().click(); await W(1500); await page.waitForFunction(() => /Validate xong:|Validate thành công/.test(document.querySelector('.modal.show')?.innerText || '') && !document.querySelector('.modal.show .spinner-border, .modal.show .loading, .modal.show [class*=spinner]'), null, { timeout: 90000 }).catch(() => {}); await W(1500); await shot('24_import_ok.png');
    await m.locator('button').filter({ hasText: /^\s*Import\s*$/ }).last().click(); await W(6000);
    log.push(JSON.stringify(await page.evaluate(() => document.body.innerText.match(/Import thành công[^\n]*/g))));
  }
  return log;
}

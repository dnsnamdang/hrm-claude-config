async (page) => {
  // Sửa 1 tab trong "Testcase chuyển đổi" (Google Sheet, chế độ Office).
  // P = {tab, ops:[...]}. op:
  //   {op:'expand'} / {op:'collapse'}               mở / thu tất cả nhóm hàng
  //   {op:'insert', after:R, n:N}                   chèn N hàng dưới hàng R (kế thừa định dạng + dropdown)
  //   {op:'paste', ref:'A90', tsv:'...'}            dán text/plain TSV (giữ định dạng ô, giữ xuống dòng)
  //   {op:'fmt', src:'77:77', dst:'90:90'}          chép CHỈ định dạng
  //   {op:'merge', ref:'A91:A99'}                   hợp nhất theo chiều dọc
  //   {op:'clear', refs:['K20','K21']}              xoá nội dung ô
  //   {op:'shot', name:'x.png', ref:'A85'}          chụp màn hình (sau khi nhảy tới ref)
  const P = __PARAMS__;
  const p = page.context().pages().find(x => x.url().includes('1dbKcipbtpm'));
  await p.bringToFront();
  const W = (ms) => p.waitForTimeout(ms);
  const log = [];
  const go = async (ref) => {
    const nb = p.locator('#t-name-box');
    await nb.click(); await nb.fill(ref); await nb.press('Enter'); await W(500);
  };
  const menu = async (menuSel, path) => {
    await p.locator(menuSel).click(); await W(500);
    for (let i = 0; i < path.length; i++) {
      const it = p.locator('.goog-menuitem:visible, [role=menuitem]:visible').filter({ hasText: path[i] }).first();
      if (i < path.length - 1) { await it.hover(); await W(600); } else { await it.click(); await W(800); }
    }
  };
  const okDialog = async () => {
    const ok = p.locator('.modal-dialog-buttons button:visible, [role=dialog] button:visible').filter({ hasText: /^(OK|Đồng ý)$/ });
    if (await ok.count()) { await ok.first().click(); await W(600); }
  };
  const groupMenu = async (label) => {
    const t = p.locator('.docs-sheet-row-group-control, [class*="row-group"] [role=button], [class*="grouping-control"]').first();
    let box = null;
    try { box = await t.boundingBox(); } catch (e) {}
    if (box) await p.mouse.click(box.x + box.width / 2, box.y + box.height / 2, { button: 'right' });
    else await p.mouse.click(14, 176, { button: 'right' });
    await W(600);
    const it = p.locator('.goog-menuitem:visible, [role=menuitem]:visible').filter({ hasText: label }).first();
    if (await it.count()) { await it.click(); await W(1000); log.push(label); } else { await p.keyboard.press('Escape'); log.push('groupMenu:MISS ' + label); }
  };

  const tab = p.locator('.docs-sheet-tab', { hasText: P.tab });
  await tab.first().click(); await W(2000);
  for (const o of P.ops) {
    try {
      if (o.op === 'expand') await groupMenu('Mở rộng tất cả các nhóm hàng');
      else if (o.op === 'collapse') await groupMenu('Thu gọn tất cả các nhóm hàng');
      else if (o.op === 'insert') {
        await go(`${o.after - o.n + 1}:${o.after}`);
        await menu('#docs-insert-menu', ['Hàng', new RegExp(`Chèn ${o.n} hàng xuống dưới`)]);
        log.push(`insert ${o.n} after ${o.after}`);
      } else if (o.op === 'paste') {
        await go(o.ref);
        await p.evaluate((tsv) => {
          const dt = new DataTransfer(); dt.setData('text/plain', tsv);
          document.activeElement.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
        }, o.tsv);
        await W(1500); log.push('paste ' + o.ref);
      } else if (o.op === 'fmt') {
        await go(o.src); await p.keyboard.press('Meta+C'); await W(500);
        await go(o.dst);
        await menu('#docs-edit-menu', ['Dán đặc biệt', 'Chỉ định dạng']);
        await p.keyboard.press('Escape'); log.push('fmt ' + o.src + '→' + o.dst);
      } else if (o.op === 'merge') {
        await go(o.ref);
        await menu('#docs-format-menu', ['Hợp nhất ô', 'Hợp nhất theo chiều dọc']);
        await okDialog(); log.push('merge ' + o.ref);
      } else if (o.op === 'clear') {
        for (const r of o.refs) { await go(r); await p.keyboard.press('Delete'); await W(300); }
        log.push('clear ' + o.refs.join(','));
      } else if (o.op === 'shot') {
        if (o.ref) await go(o.ref);
        await W(800); await p.screenshot({ path: '.playwright-mcp/' + o.name }); log.push('shot ' + o.name);
      }
    } catch (e) { log.push(o.op + ':ERR ' + e.message.slice(0, 120)); }
  }
  return log;
}

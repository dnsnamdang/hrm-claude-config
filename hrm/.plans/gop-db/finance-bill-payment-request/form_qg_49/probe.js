const { open, go, DEV } = require('./devlib');
(async () => {
  const { browser, page } = await open();
  const resps = [];
  page.on('response', async r => { if (r.url().includes('/bill-payment-requests')) { try { resps.push([r.url(), (await r.text())]) } catch (e) {} } });
  await go(page, '/finance/bill-payment-requests');
  for (const [u, t] of resps) { console.log(u); try { const j = JSON.parse(t); console.log(JSON.stringify(j.meta||{}).slice(0,1500)); (j.data||[]).slice(0,10).forEach(d=>console.log(d.id,d.code,d.type,d.type_payment,d.status,d.status_name,d.is_can_edit,d.is_can_delete,d.is_can_approve,d.created_by_name)); console.log('total', j.total) } catch(e){ console.log(t.slice(0,300)) } }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });

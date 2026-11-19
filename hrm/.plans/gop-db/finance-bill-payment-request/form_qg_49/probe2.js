const { open, go, DEV } = require('./devlib');
(async () => {
  const { browser, page } = await open();
  let auth = null;
  page.on('request', r => { if (r.url().includes('/api/v1/') && r.headers().authorization) auth = r.headers().authorization; });
  await go(page, '/finance/bill-payment-requests');
  const api = async (u) => (await page.request.get(DEV + '/api/v1/' + u, { headers: { authorization: auth, accept: 'application/json' } })).json();
  for (const q of ['finance/bill-payment-requests?mode=mine&per_page=50', 'finance/bill-payment-requests/pending?per_page=50', 'finance/bill-payment-requests?per_page=50&status=6', 'finance/bill-payment-requests?per_page=30&type=12']) {
    const j = await api(q); console.log('==', q, j.total);
    (j.data||[]).forEach(d=>console.log(d.id,d.code,'type',d.type,'tp',d.type_payment,'st',d.status,d.status_name,'e',d.is_can_edit,'d',d.is_can_delete,'a',d.is_can_approve,'pc',d.is_can_create_bill_payment,d.is_can_create_bill_payment_authorization,d.created_by_name));
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });

// Dò dữ liệu dev (CHỈ ĐỌC — chỉ gọi GET) cho 2 màn Chờ báo thừa thiếu (288) + Phiếu báo hàng thừa thiếu (289).
const P = require('../../../xuat-tai-lieu-chuyen-doi/_capture_phieu.js');
(async () => {
  const { browser, page } = await P.open(__dirname);
  try {
    await P.go(page, '/warehouse/import-discrepancies');
    const get = (u) => page.evaluate(async (u) => { try { return await window.$nuxt.$store.dispatch('apiGetMethod', u); } catch (e) { return { err: e?.response?.status, msg: e?.response?.data?.message }; } }, u);
    const me = await page.evaluate(() => { const u = window.$nuxt.$auth && window.$nuxt.$auth.user; return u ? JSON.stringify({ id: u.id, name: u.info && u.info.fullname, company: u.info && u.info.company_id }) : null; });
    console.log('me', me);
    const qfo = await get('finance/exc-shortage-imports/queue/filter-options');
    console.log('queue fo', JSON.stringify({ ...qfo.data, warehouses: (qfo.data?.warehouses||[]).length, suppliers: (qfo.data?.suppliers||[]).length, requesters: (qfo.data?.requesters||[]).length, companies: (qfo.data?.companies||[]).length }));
    const q = await get('finance/exc-shortage-imports/queue?per_page=200');
    console.log('queue total', q.data?.total, JSON.stringify(q.data?.meta));
    for (const it of (q.data?.items || []).slice(0, 30)) console.log(' Q', it.id, it.code, '|', it.type_name, '|', it.supplier_name, '|', it.created_at, '|', it.warehouse_import_request_code, '|', it.requester_name, '|', it.product_import_requester_name, '|', it.creator_name, '| parent', it.parent_warehouse_import_code, '| can', it.is_can_create_exc);
    const fo = await get('finance/exc-shortage-imports/filter-options');
    console.log('list fo', JSON.stringify({ ...fo.data, suppliers: (fo.data?.suppliers||[]).length, creators: (fo.data?.creators||[]).length, companies: (fo.data?.companies||[]).length }));
    const l = await get('finance/exc-shortage-imports?per_page=200');
    console.log('list total', l.data?.total, JSON.stringify(l.data?.meta));
    for (const it of (l.data?.items || [])) {
      const h = await get(`finance/exc-shortage-imports/${it.id}/histories`);
      const n = Array.isArray(h.data) ? h.data.length : -1;
      console.log(' L', it.id, it.code, '|', it.status_text, '|', it.created_at, '|', it.warehouse_import_code, '|', it.product_import_request_code, '|', it.supplier_name, '|', it.contract_code, '|', it.creator_name, '| edit', it.is_can_edit, 'rej', it.is_can_reject, 'proc', it.is_can_process, '| hist', n);
    }
    if (q.data?.items?.length) {
      const s = await get('finance/exc-shortage-imports/source/' + q.data.items[0].id);
      console.log('source', JSON.stringify(s).slice(0, 1500));
    }
    if (l.data?.items?.length) {
      const d = await get('finance/exc-shortage-imports/' + l.data.items[0].id);
      console.log('detail', JSON.stringify(d).slice(0, 2000));
    }
  } finally { await browser.close(); }
})();

"""E2E Chương trình khuyến mại trên cổng DEV — dữ liệu CT thật của dev (CT 506 'Mua 09 xô dầu CK4 tặng 02 xô', KH 18002).
E2E_ENV=dev python3 run_km_dev.py  — tạo báo giá [E2E KM DEV] qua API, chọn KM qua API (đúng payload FE toPayload),
kiểm chặn vượt mốc / SL mua > SL báo giá, rồi mở màn Sửa + Chi tiết, Lưu nháp từ giao diện."""
import os, re, sys
os.environ['E2E_ENV'] = 'dev'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'e2e-p3'))
from common import *   # e2e-p3/common.py: api / sql / check / ui_login theo dev
from playwright.sync_api import sync_playwright

CUST, CAT, CAMP, P, UNIT = 18002, 506, 5646, 50375, 75
st, r = api('GET', f'assign/quotations/promotion-categories/{CAT}?customer_id={CUST}')
check('KM: chi tiết CT 506 cho KH 18002 trả được', st == 200, r)
camp = next(c for c in r['data']['combo_campaigns'] if c['id'] == CAMP)
cp9 = next(c for c in camp['checkpoints'] if c['qty'] == 9)
G, O = cp9['groups'][0]['id'], cp9['groups'][0]['options'][0]['id']

line = {'product_type': 1, 'erp_product_id': P, 'code': 'ENEO-700-V5262', 'name': 'Dầu ENEOS DEO CK-4 15W40 (xô 18L)', 'unit_id': UNIT,
        'qty_needed': 9, 'quoted_price': 2000000, 'estimated_price': 1500000, 'vat_percent': 10, 'temp_id': 't1'}
qid = sql("select id from quotations where note='[E2E KM DEV]' order by id desc limit 1")
if qid:
    QID = int(qid[0][0])
    sql(f'update quotations set status=1, price_approval_level=null where id={QID}')
else:
    st, r = api('POST', 'assign/quotations', {'price_type_id': 1, 'customer_id': CUST, 'note': '[E2E KM DEV]', 'products': [line],
                                              'service_items': [], 'quotation_discounts': [], 'delivery_address': '[TEST] Số 1 KM, Hà Nội'})
    check('KM: tạo báo giá test có 9 xô CK4', st == 200, r)
    QID = int(sql("select id from quotations where note='[E2E KM DEV]' order by id desc limit 1")[0][0])
print('QID', QID)

def promo(buy, sel):
    return [{'combo_category_id': CAT, 'combo_campaigns': [{'combo_campaign_id': CAMP, 'products': [{'product_id': P, 'qty': buy}],
             'groups': [{'combo_group_id': G, 'options': [{'combo_option_id': O, 'select_qty': sel}]}]}], 'gifts': []}]

st, r = api('PUT', f'assign/quotations/{QID}', {'promotions': promo(9, 1)})
check('KM: mua 9 ⇒ đạt mốc 9, chọn 1 phần quà ⇒ lưu được', st == 200, r)
rows = sql(f'select count(*) from quotation_promotions where quotation_id={QID}')[0][0]
check('KM: DB có dòng quotation_promotions', int(rows) >= 1, rows)
st, r = api('PUT', f'assign/quotations/{QID}', {'promotions': promo(9, 2)})
check('KM: chọn quà vượt số phần được tặng ⇒ chặn 422', st == 422, (st, r))
st, r = api('PUT', f'assign/quotations/{QID}', {'promotions': promo(10, 1)})
check('KM: SL mua KM (10) > SL hàng trong báo giá (9) ⇒ chặn 422', st == 422, (st, r))
check('KM: lưu lỗi không làm mất KM đã lưu', sql(f'select count(*) from quotation_promotions where quotation_id={QID}')[0][0] == rows)
st, r = api('GET', f'assign/quotations/{QID}')
check('KM: chi tiết báo giá trả lại KM đã chọn', st == 200 and any(c.get('id') == CAT for c in ((r['data'].get('promotions') or {}).get('categories') or [])),
      list((r['data'] or {}).keys()))

ERR = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    page = b.new_page(viewport={'width': 1600, 'height': 1000})
    page.on('pageerror', lambda e: ERR.append(str(e)))
    ui_login(page)
    page.goto(FE + f'/assign/quotations/{QID}/edit', wait_until='domcontentloaded'); page.wait_for_timeout(20000)
    check('KM UI: màn Sửa hiện khối CT 506', page.locator(f'[data-test="qp-cat-{CAT}"]').count() == 1)
    check('KM UI: bảng tổng hợp quà có dòng', page.locator('[data-test="qp-gift-summary"] tbody tr').count() >= 1)
    with page.expect_response(lambda x: re.search(rf'/assign/quotations/{QID}$', x.url) and x.request.method == 'PUT', timeout=90000) as ri:
        page.locator('button:has-text("Lưu nháp")').last.click()
    check('KM UI: Lưu nháp từ giao diện thành công', ri.value.status == 200, ri.value.text()[:300])
    page.wait_for_timeout(3000)
    check('KM UI: lưu lại giữ nguyên KM trên DB', sql(f'select count(*) from quotation_promotions where quotation_id={QID}')[0][0] == rows)
    page.goto(FE + f'/assign/quotations/{QID}', wait_until='domcontentloaded'); page.wait_for_timeout(20000)
    check('KM UI: màn Chi tiết hiện khối CT 506', page.locator(f'[data-test="qp-cat-{CAT}"]').count() == 1)
    b.close()
check('KM UI: không lỗi JS', not ERR, ERR[:3])
summary()

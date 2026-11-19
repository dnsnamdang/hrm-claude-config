import sys
from common import *
CATS = [int(x) for x in (sys.argv[1:] or ['482', '474', '472'])]
TRIALS = 250
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context()
    p = erp_login(ctx)
    p.goto(ERP + '/admin/sale/firm-quotations/create', wait_until='domcontentloaded', timeout=180000)
    p.wait_for_function('typeof FirmQuotationCategory !== "undefined"', timeout=120000)
    p.add_script_tag(path=os.path.join(HERE, 'hqp_browser.js'))
    js = open(os.path.join(HERE, 'parity.js')).read()
    all_trials = {}
    for cid in CATS:
        erp = p.evaluate(f'''async () => (await (await fetch('/admin/sale/new_combo_categories/{cid}/getDataForUse?employee_id=13&customer_id=210', {{headers:{{'X-Requested-With':'XMLHttpRequest'}}}})).json())''')
        st, h = api('GET', f'assign/quotations/promotion-categories/{cid}?customer_id=210')
        check(f'CT {cid}: ERP + HRM đều trả chi tiết', erp.get('success') and st == 200, (erp.get('message'), st, h.get('message')))
        if st != 200 or not erp.get('success'):
            continue
        r = p.evaluate(js, {'erpData': erp['data'], 'hrmData': h['data'], 'trials': TRIALS, 'seed': cid * 7919})
        ids = r['campaignIds']
        check(f'CT {cid}: cùng danh sách mã KM (ERP {len(ids["erp"])} / HRM {len(ids["hrm"])})', ids['erp'] == ids['hrm'], ids)
        check(f'CT {cid}: cùng danh sách quà nhóm', sorted(ids['erpGifts']) == sorted(ids['hrmGifts']), ids)
        print(f'   stats {r["stats"]}')
        check(f'CT {cid}: {TRIALS} bộ số ngẫu nhiên — Q/mốc/SL chọn/max/SL tặng/hàng tặng khớp ERP', not r['mismatches'], r['mismatches'][:15])
        all_trials[cid] = {'trials': r['trials']}
    json.dump(all_trials, open(os.path.join(HERE, 'parity_trials.json'), 'w'))
    b.close()
summary()

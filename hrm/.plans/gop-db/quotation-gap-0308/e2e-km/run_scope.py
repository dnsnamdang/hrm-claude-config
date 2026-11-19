from common import *
from urllib.parse import urlencode
TOK = dict(l.split() for l in open(os.path.join(DEV_TOK_DIR if ENV == 'dev' else HERE, 'tokens.txt')))
EMPS = [13, 40, 126, 661, 328, 407]
CUSTS = [232834, 21195, 973, 87, 2440] if ENV == 'dev' else [210, 232389, 973, 87, 2440]
FILTERS = [({}, {}), ({'keyword': 'BÁN BUÔN'}, {'name': 'BÁN BUÔN'}), ({'keyword': 'mafra'}, {'name': 'mafra'}),
           ({'product_code': 'MARA-P1261'}, {'product_code': 'MARA-P1261'}), ({'product_name': 'SJ-40'}, {'product_name': 'SJ-40'}),
           ({'product_model': 'SJ 40'}, {'product_model': 'SJ 40'}), ({'product_code': 'KHONG_CO_XYZ'}, {'product_code': 'KHONG_CO_XYZ'})]
with sync_playwright() as pw:
    b = pw.chromium.launch(); ctx = b.new_context(); p = erp_login(ctx)
    p.goto(ERP + '/admin/sale/firm-quotations/create', wait_until='domcontentloaded', timeout=180000)
    erp_get = lambda path: p.evaluate('async (u) => (await (await fetch(u, {headers:{"X-Requested-With":"XMLHttpRequest"}})).json())', path)
    total = mism = 0; mm = []
    nonempty = set()
    for e in EMPS:
        for c in CUSTS:
            for hf, ef in FILTERS:
                st, h = api('GET', 'assign/quotations/promotion-categories?' + urlencode({'customer_id': c, **hf}), token=TOK[str(e)])
                er = erp_get('/admin/sale/new_combo_categories/getListDataForUse?' + urlencode({'employee_id': e, 'customer_id': c, 'type': 'active', **ef}))
                hi = sorted(x['id'] for x in h.get('data', [])); ei = sorted(x['id'] for x in er.get('data', []))
                total += 1
                if hi: nonempty.add((e, c, tuple(sorted(hi))))
                if st != 200 or hi != ei:
                    mism += 1; mm.append((e, c, hf, st, 'hrm', hi, 'erp', ei))
    check(f'Danh sách CT: {total} tổ hợp (6 NV × 5 KH × 7 bộ lọc) HRM = ERP', mism == 0, mm[:6])
    print('   các tập kết quả khác nhau:', len(set(x[2] for x in nonempty)), sorted(set(x[2] for x in nonempty)))
    # chi tiết: HRM 200 ⇔ ERP success (mọi CT đang hiệu lực, không lọc phạm vi)
    cand = [506, 504, 503, 500, 497, 486, 482, 474, 472, 470] if ENV == 'dev' else [482, 481, 480, 478, 474, 472, 463, 451, 466, 470]
    total = mism = 0; mm = []
    for e in EMPS:
        for c in CUSTS:
            for cid in cand:
                st, h = api('GET', f'assign/quotations/promotion-categories/{cid}?customer_id={c}', token=TOK[str(e)])
                er = erp_get(f'/admin/sale/new_combo_categories/{cid}/getDataForUse?employee_id={e}&customer_id={c}')
                total += 1
                ok_h = st == 200; ok_e = bool(er.get('success'))
                same_msg = ok_h or (h.get('message') == er.get('message'))
                if ok_h != ok_e or not same_msg:
                    mism += 1; mm.append((e, c, cid, st, h.get('message'), er.get('success'), er.get('message')))
    check(f'Chi tiết CT: {total} tổ hợp — HRM cho/chặn y hệt ERP (kể cả câu báo)', mism == 0, mm[:6])
    b.close()
summary()

"""E2E API Phase 3 (GAP 0308) — chạy: python3 run_api.py  (cần API :8003 + DB local_hrm_erp).
Đối chiếu số liệu API với DB thật, 2 tài khoản (đủ quyền / không quyền). Dữ liệu sửa thử được trả về như cũ ở cuối."""
from common import *

ADMIN, LIMITED = token('tok'), token('tok_cannt')
KH = IDS['KH']
Q = IDS['Q_DEMAND']          # báo giá test độc lập, Đang tạo, người lập id 13
DEM_OK, DEM_CLOSED, DEM_OTHER = IDS.get('D_OPEN', 5), IDS.get('D_CLOSED', 6), IDS['DEM_OTHER']   # 2 nhu cầu của KH test (1 đã đóng); 1 của KH khác

orig = sql(f"select coalesce(customer_demand_id,'NULL') from quotations where id={Q}")[0][0]

# ---------------------------------------------------------------- 1. Nhu cầu khách hàng (dòng 13)
st, r = api('GET', f'assign/quotations/customer-demand-options?customer_id={KH}')
ids = [x['id'] for x in r.get('data', [])]
db = [int(x[0]) for x in sql(f"select d.id from meeting_investment_demands d join meetings m on m.id=d.meeting_id where m.customer_id={KH} and d.status=1")]
check('Nhu cầu: danh sách = nhu cầu Đang theo dõi của KH (đối chiếu DB)', st == 200 and sorted(ids) == sorted(db), (ids, db))
check('Nhu cầu: không có KH → rỗng', api('GET', 'assign/quotations/customer-demand-options')[1].get('data') == [])
st, r = api('GET', f'assign/quotations/customer-demand-options?customer_id={KH}&include_id={DEM_CLOSED}')
check('Nhu cầu: nhu cầu đang chọn đã đóng vẫn có trong danh sách', DEM_CLOSED in [x['id'] for x in r['data']])
check('Nhu cầu: nhãn có nhóm ngành + giá trị định dạng en-US', any('5,000,000' in x['text'] for x in r['data']), r['data'])
st, r = api('PUT', f'assign/quotations/{Q}', {'customer_demand_id': DEM_OTHER})
check('Nhu cầu: chọn nhu cầu của KH khác bị chặn 422', st == 422, (st, r))
st, r = api('PUT', f'assign/quotations/{Q}', {'customer_demand_id': 999999})
check('Nhu cầu: id không tồn tại bị chặn 422 (lang file "Không tồn tại")', st == 422 and 'Không tồn tại' in json.dumps(r, ensure_ascii=False), r)
st, r = api('PUT', f'assign/quotations/{Q}', {'customer_demand_id': DEM_OK})
check('Nhu cầu: lưu nhu cầu đúng KH', st == 200 and sql(f'select customer_demand_id from quotations where id={Q}')[0][0] == str(DEM_OK), r)
st, r = api('GET', f'assign/quotations/{Q}')
check('Nhu cầu: chi tiết trả customer_demand kèm nhãn', (r['data'].get('customer_demand') or {}).get('id') == DEM_OK)
st, r = api('PUT', f'assign/quotations/{Q}', {'customer_demand_id': None})
check('Nhu cầu: gửi null = bỏ chọn', sql(f'select coalesce(customer_demand_id,"NULL") from quotations where id={Q}')[0][0] == 'NULL')
sql(f'update quotations set price_approval_level=null where id={Q}')
st, r = api('POST', f'assign/quotations/{Q}/submit', {})
check('Nhu cầu: KHÔNG bắt buộc (bỏ 30/10) — gửi duyệt khi trống không bị chặn vì nhu cầu', 'nhu cầu' not in str(r.get('message', '')), r)
sql(f'update quotations set status=1, price_approval_level=null where id={Q}')
api('PUT', f'assign/quotations/{Q}', {'customer_demand_id': DEM_OK})
st, r = api('POST', f'assign/quotations/{Q}/submit', {})
check('Nhu cầu: có nhu cầu thì qua bước kiểm nhu cầu', 'nhu cầu' not in str(r.get('message', '')), r)
sql(f'update quotations set status=1, price_approval_level=null where id={Q}')
st_dem = sql(f'select status from meeting_investment_demands where id={DEM_OK}')[0][0]
check('Nhu cầu: lập/gửi duyệt báo giá KHÔNG đổi trạng thái nhu cầu', st_dem == '1', st_dem)
# báo giá CÓ dự án (28/10/2026): chọn từ nhu cầu meeting của KH dự án, điền sẵn nhu cầu dự án, bắt buộc khi gửi duyệt
QP2 = IDS['Q_PROJECT']   # báo giá có dự án test
D_PRJ = IDS.get('D_PROJECT') or int(sql("select id from meeting_investment_demands where scope_name='[TEST] Cầu nâng (đã lập dự án 154)'")[0][0])
D_OPEN2 = IDS.get('D_OPEN2') or int(sql("select id from meeting_investment_demands where scope_name='[TEST] Hệ thống khí nén KH210'")[0][0])
st, r = api('GET', f"assign/quotations/customer-demand-options?customer_id={KH}&project_id={IDS['PROJECT']}")
opts = {x['id']: x for x in r['data']}
check('Nhu cầu (dự án): danh sách có nhu cầu của dự án, đánh dấu để điền sẵn', D_PRJ in opts and opts[D_PRJ]['is_project_demand'], list(opts))
check('Nhu cầu (dự án): danh sách CHỈ có nhu cầu kế thừa từ dự án (chốt 30/10)', list(opts) == [D_PRJ], list(opts))
check('Nhu cầu: nhãn có mã meeting + ngày họp (phân biệt nhiều meeting)', all(' — ' in x['text'] and '(' in x['text'] for x in r['data']), [x['text'] for x in r['data']][:2])
sql(f'update quotations set customer_demand_id=null where id={QP2}')
st, r = api('PUT', f'assign/quotations/{QP2}', {'customer_demand_id': D_OPEN2})
check('Nhu cầu (dự án): gửi nhu cầu khác ⇒ BE bỏ qua, lưu nhu cầu của dự án', st == 200 and sql(f'select customer_demand_id from quotations where id={QP2}')[0][0] == str(D_PRJ), (st, r))
st, r = api('PUT', f'assign/quotations/{QP2}', {'customer_demand_id': DEM_OTHER})
check('Nhu cầu (dự án): gửi nhu cầu của KH khác ⇒ vẫn lưu nhu cầu của dự án', st == 200 and sql(f'select customer_demand_id from quotations where id={QP2}')[0][0] == str(D_PRJ), (st, r))
st, r = api('PUT', f'assign/quotations/{QP2}', {'customer_demand_id': None})
check('Nhu cầu (dự án): gửi rỗng ⇒ vẫn giữ nhu cầu của dự án', sql(f'select customer_demand_id from quotations where id={QP2}')[0][0] == str(D_PRJ))
sql(f'update quotations set customer_demand_id={D_OPEN2} where id={QP2}')
st, r = api('GET', f'assign/quotations/{QP2}')
check('Nhu cầu (dự án): chi tiết hiện nhu cầu dự án (kể cả bản ghi cũ lưu lệch) + cờ khoá', r['data']['customer_demand_id'] == D_PRJ and r['data']['customer_demand_locked'] is True, (r['data'].get('customer_demand_id'), r['data'].get('customer_demand_locked')))
st, r = api('PUT', f'assign/quotations/{QP2}', {'note': 'e2e'})
check('Nhu cầu (dự án): lưu không gửi trường ⇒ tự sửa về nhu cầu dự án', sql(f'select customer_demand_id from quotations where id={QP2}')[0][0] == str(D_PRJ))
sql(f"update meeting_investment_demands set prospective_project_id=null where id={D_PRJ}")
st, r = api('PUT', f'assign/quotations/{QP2}', {'note': 'e2e'})
check('Nhu cầu (dự án): dự án chưa gắn nhu cầu ⇒ trống, không lỗi', st == 200 and sql(f'select coalesce(customer_demand_id,"NULL") from quotations where id={QP2}')[0][0] == 'NULL', (st, r))
st, r = api('POST', f'assign/quotations/{QP2}/submit', {})
check('Nhu cầu (dự án): KHÔNG bắt buộc — gửi duyệt khi trống không bị chặn vì nhu cầu', 'nhu cầu' not in str(r.get('message', '')), r)
sql(f'update quotations set status=1, price_approval_level=null where id={QP2}')
sql(f"update meeting_investment_demands set prospective_project_id={IDS['PROJECT']} where id={D_PRJ}")
api('PUT', f'assign/quotations/{QP2}', {'customer_demand_id': D_PRJ})
check('Nhu cầu: tài khoản không quyền vẫn đọc danh sách', api('GET', f'assign/quotations/customer-demand-options?customer_id={KH}', tok=LIMITED)[0] == 200)

# ---------------------------------------------------------------- 2. Tồn kho 3 cột (dòng 30)
st, r = api('POST', 'assign/quotations/stock-info', {'customer_id': IDS['STOCK_CUSTOMER'], 'items': [{'product_id': 20972}, {'product_id': 20973}]})
check('Tồn: API trả đủ dòng theo thứ tự', st == 200 and [x['product_id'] for x in r['data']] == [20972, 20973], r)
codes = [x['company_code'] for x in r['data'][0]['sellable_by_company']]
check('Tồn: tồn có thể bán chia theo từng công ty', len(codes) >= 1 and len(set(codes)) == len(codes), codes)
# Đang giữ = prepick người lập (token = id 13) + KH; dữ liệu giữ hàng có sẵn thuộc NV 31 ⇒ id 13 thấy 0
check('Tồn: Đang giữ của người khác không lọt sang (id 13 = 0)', r['data'][0]['prepick_qty'] == 0, r['data'][0])
st, r = api('POST', 'assign/quotations/stock-info', {'items': [{'product_id': 20972}]})
check('Tồn: chưa có khách hàng → Đang giữ = null (FE hiện "-")', r['data'][0]['prepick_qty'] is None, r)
# đổi ĐVT: số = floor(cơ bản / hệ số)
pu = sql("select pu.product_id, pu.unit_id, pu.unit_coefficient from product_units pu join recipe_products rp on rp.base_product_id=pu.product_id where pu.is_base=0 and pu.unit_coefficient>1 limit 1")
pu = pu or sql("select product_id, unit_id, unit_coefficient from product_units where is_base=0 and unit_coefficient>1 and product_id in (select product_id from accounting_stocks group by product_id having sum(qty)>50) limit 1")
pid, uid, coef = int(pu[0][0]), int(pu[0][1]), float(pu[0][2])
st, r = api('POST', 'assign/quotations/stock-info', {'items': [{'product_id': pid}, {'product_id': pid, 'unit_id': uid}]})
b, u = r['data']
ok = all(abs(x['qty'] - (int(y['qty'] / coef * 100) / 100)) < 0.011 for x, y in zip(u['sellable_by_company'], b['sellable_by_company']))
check(f'Tồn: đổi ĐVT (hệ số {coef:g}) chia đúng cho tồn có thể bán', ok, (b, u))
check('Tồn: đổi ĐVT chia đúng Có thể LR', u['join_qty'] == int(b['join_qty'] // coef), (b['join_qty'], u['join_qty']))
check('Tồn: tài khoản không quyền vẫn xem được', api('POST', 'assign/quotations/stock-info', {'items': [{'product_id': 20972}]}, tok=LIMITED)[0] == 200)

# ---------------------------------------------------------------- 3. Mẫu báo giá ERP (dòng 22/26/60)
st, r = api('GET', 'assign/quotations/template-options')
qt, dt = r['data']['quotation_templates'], r['data']['data_templates']
check('Mẫu: số Báo giá mẫu = project_quotations is_template', len(qt) == int(sql('select count(*) from project_quotations where is_template=1')[0][0]))
check('Mẫu: số Dữ liệu mẫu = quotation_templates', len(dt) == int(sql('select count(*) from quotation_templates')[0][0]))
for t in qt:
    st, r = api('GET', f"assign/quotations/quotation-templates/{t['id']}")
    d = r['data']
    tabs = int(sql(f"select count(*) from project_quotation_tabs t where t.parent_id={t['id']}")[0][0])
    prods = int(sql(f"select count(*) from project_quotation_tab_products tp join project_quotation_tabs t on t.id=tp.parent_id where t.parent_id={t['id']} and tp.product_id is not null")[0][0])
    temps = int(sql(f"select count(*) from project_quotation_tab_products tp join project_quotation_tabs t on t.id=tp.parent_id where t.parent_id={t['id']} and tp.product_id is null")[0][0])
    got = sum(len(g['products']) for g in d['groups'])
    check(f"Mẫu {t['id']}: nhóm = tab ERP, hàng ERP + hàng tạm bỏ qua khớp DB", len(d['groups']) == tabs and got == prods and d['skipped_temp'] == temps, (len(d['groups']), tabs, got, prods, d['skipped_temp'], temps))
for t in dt[:15]:
    st, r = api('GET', f"assign/quotations/data-templates/{t['id']}")
    n = int(sql(f"select count(*) from quotation_template_products where parent_id={t['id']}")[0][0])
    check(f"Dữ liệu mẫu {t['id']}: số hàng khớp DB", len(r['data']['products']) == n, (len(r['data']['products']), n))
check('Mẫu: id không tồn tại → 404', api('GET', 'assign/quotations/quotation-templates/999999')[0] == 404 and api('GET', 'assign/quotations/data-templates/999999')[0] == 404)
check('Mẫu: tài khoản không quyền vẫn đọc mẫu', api('GET', 'assign/quotations/template-options', tok=LIMITED)[0] == 200)

# ---------------------------------------------------------------- 4. Cờ công thức (tối ưu áp mẫu)
sample = [int(x[0]) for x in sql('select id from products where status=1 order by id limit 400')]
st, r = api('POST', 'assign/quotations/recipe-flags', {'ids': sample})
db = sorted(int(x[0]) for x in sql(f"select distinct base_product_id from recipe_products where base_product_id in ({','.join(map(str, sample))})"))
check('Cờ công thức: khớp recipe_products', sorted(r['data']) == db, (len(r['data']), len(db)))

# ---------------------------------------------------------------- 5. Phần mở rộng bản in (dòng 56)
st, r = api('GET', f"assign/quotations/{IDS['Q_SPECS']}/print-extras")
d = r['data']['products']
pid = next((k for k, v in d.items() if v['basic_attributes']), None)
n = int(sql(f'select count(*) from attribute_products where product_id={pid} and need_print=1')[0][0]) if pid else -1
check('In: Thông số cơ bản = attribute_products tích in', pid and len(d[pid]['basic_attributes']) == n, (pid, n))
nprod = int(sql(f'select count(distinct erp_product_id) from quotation_product_prices where quotation_id={IDS['Q_SPECS']} and erp_product_id is not null')[0][0])
check('In: đủ hàng ERP của báo giá', len(d) == nprod, (len(d), nprod))
check('In: có định mức đàm phán theo từng hàng/ĐVT', len(r['data']['negotiation']) >= 1)

# ---------------------------------------------------------------- 6. Hàng tự khai thác + lọc popup chọn hàng (dòng 58)
st, r = api('GET', 'master-data/products/form-options')
check('Loại hàng: form-options có "Hàng tự khai thác"', {'id': 'hang_tu_khai_thac', 'name': 'Hàng tự khai thác'} in r['data']['product_cates'])
base = 'master-data/products/product-picker/search?company_id=1&scope=all&include_uncataloged=1&per_page=100'
st, r = api('GET', base + '&product_cate=hang_bao_hanh&columns[]=creator_name')
ids = [x['id'] for x in r['data']]
bad = sql(f"select count(*) from products where id in ({','.join(map(str, ids))}) and not json_contains(product_cate, '\"hang_bao_hanh\"')")[0][0] if ids else '0'
check('Lọc loại hàng: mọi dòng trả về đúng loại', ids and bad == '0', (len(ids), bad))
check('Lọc loại hàng: có tên người tạo', all(x.get('creator_name') for x in r['data'][:20]))
check('Lọc loại hàng: giá trị lạ → 422', api('GET', base + '&product_cate=bogus')[0] == 422)
st, r = api('GET', base + '&per_page=20')
check('Popup chọn hàng (màn khác, không xin cột) KHÔNG trả join_qty/prepick_qty', 'join_qty' not in r['data'][0] and 'prepick_qty' not in r['data'][0])

# ---------------------------------------------------------------- 7. BOM mẫu (dòng 27/59) — quyền
st, r = api('GET', 'assign/bom-templates/options')
check('BOM mẫu: options chỉ mẫu Hoạt động', st == 200 and len(r['data']) == int(sql('select count(*) from bom_templates where status=1')[0][0]))
st, r = api('POST', 'assign/bom-templates', {'name': 'E2E không quyền', 'status': 1, 'products': [], 'services': [], 'groups': []}, tok=LIMITED)
check('BOM mẫu: không quyền tạo → 403', st == 403, (st, r))
st, r = api('GET', 'assign/bom-templates', tok=LIMITED)
check('BOM mẫu: không quyền vẫn xem danh sách', st == 200)

# ---------------------------------------------------------------- trả dữ liệu
sql(f"update quotations set customer_demand_id={orig}, price_approval_level=null where id={Q}")
summary()

"""Dựng DỮ LIỆU TEST Phase 3 trên cổng DEV (dev-hrm.eteksofts.com, DB hrm_erp_test) — chạy lại nhiều lần không trùng.
E2E_ENV=dev python3 seed_dev.py  → ghi ids_dev.json cho run_api / run_ui / run_extra. Mọi bản ghi tạo mới có tiền tố [TEST].
Danh mục (hàng hoá, mẫu ERP, bảng giá) dev giống local nên dùng chung id; chỉ khách hàng / báo giá / BOM / nhu cầu là riêng."""
import os
os.environ['E2E_ENV'] = 'dev'
from common import *

KH, KH_LABEL = 232834, 'KH232834'   # 50TPHPAN-541 — có 2 meeting + dự án 489
EMP = 13
# Dự án [TEST]: nhân bản dự án 489 của KH, Sale phụ trách = namdangit (chỉ Sale phụ trách mới lập báo giá dự án được)
if not sql("select id from prospective_projects where code='TEST-E2E-DA489'"):
    cols = [c[0] for c in sql('show columns from prospective_projects') if c[0] not in ('id', 'code', 'name', 'main_sale_employee_id')]
    cl = ','.join(f'`{c}`' for c in cols)
    sql(f"insert into prospective_projects (code,name,main_sale_employee_id,{cl}) select 'TEST-E2E-DA489','[TEST] Dự án E2E báo giá',{EMP},{cl} from prospective_projects where id=489")
PROJECT = int(sql("select id from prospective_projects where code='TEST-E2E-DA489'")[0][0])
P_STOCK = 43508
ids = dict(LOCAL_IDS)
ids.update({'KH': KH, 'KH_LABEL': KH_LABEL, 'PROJECT': PROJECT, 'MEETING_CODE': 'TPE.MET'})

# --- 1. Nhu cầu [TEST] trên meeting của KH (meeting mới nhất) — expected 5,000,000 cho nhãn định dạng en-US
mid = sql(f"select id from meetings where customer_id={KH} order by id desc limit 1")[0][0]
def demand(name, status, scope_id, project='NULL'):
    r = sql(f"select id from meeting_investment_demands where scope_name='{name}'")
    if r:
        sql(f"update meeting_investment_demands set status={status}, prospective_project_id={project} where id={r[0][0]}")
        return int(r[0][0])
    sql(f"insert into meeting_investment_demands (meeting_id,internal_business_scope_id,internal_business_scope_name,scope_id,scope_name,expected_amount,status,prospective_project_id,created_at,updated_at) values ({mid},990007,'Năng lượng',{scope_id},'{name}',5000000,{status},{project},now(),now())")
    return int(sql(f"select id from meeting_investment_demands where scope_name='{name}'")[0][0])
ids['D_OPEN'] = demand(f'[TEST] Kết cấu thép {KH_LABEL}', 1, 44)
ids['D_OPEN2'] = demand(f'[TEST] Hệ thống khí nén {KH_LABEL}', 1, 3)
ids['D_CLOSED'] = demand(f'[TEST] Trạm sạc {KH_LABEL} (đã đóng)', 3, 45)
sql("update meeting_investment_demands set scope_name='[TEST] Cầu nâng (đã lập dự án E2E)' where scope_name like '[TEST] Cầu nâng (đã lập dự án %'")
ids['D_PROJECT'] = demand('[TEST] Cầu nâng (đã lập dự án E2E)', 2, 1, PROJECT)

# --- 2. Báo giá test: tạo qua API thật, đánh dấu bằng ghi chú [E2E-DEV] <khoá>
def quotation(key, payload):
    r = sql(f"select id from quotations where note='[E2E-DEV] {key}' order by id desc limit 1")
    if r:
        qid = int(r[0][0])
    else:
        st, body = api('POST', 'assign/quotations', {'price_type_id': 1, 'note': f'[E2E-DEV] {key}', **payload})
        if st not in (200, 201):
            raise RuntimeError(f'tạo báo giá {key}: {st} {body}')
        qid = int(sql(f"select id from quotations where note='[E2E-DEV] {key}' order by id desc limit 1")[0][0])
    # đủ các ô bắt buộc khác khi Gửi duyệt (điều khoản TT, người liên hệ, giai đoạn dự án) ⇒ test chạm đúng bước kiểm nhu cầu
    phase = sql("select id from project_phases where status=1 order by id limit 1")[0][0]
    sql(f"update quotations set status=1, price_approval_level=null, customer_demand_id=null, payment_terms='[TEST] Thanh toán 100% khi giao hàng', "
        f"customer_contact_name=coalesce(nullif(customer_contact_name,''),'[TEST] Người liên hệ'), "
        f"project_phase_id=if(project_id is null, project_phase_id, coalesce(project_phase_id,{phase})) where id={qid}")
    return qid
ids['Q_DEMAND'] = quotation('Q_DEMAND', {'customer_id': KH})
ids['Q_DIRECT'] = ids['Q_EDIT'] = quotation('Q_DIRECT', {'customer_id': KH})
ids['Q_PICK'] = quotation('Q_PICK', {'customer_id': KH})
ids['Q_PROJECT'] = quotation('Q_PROJECT', {'project_id': PROJECT})

# --- 3. Đang giữ: namdangit giữ 2 cái CH-ER-BDCD cho KH (công ty 1)
if not sql(f"select id from prepick_details where employee_id={EMP} and customer_id={KH} and product_id={P_STOCK}"):
    sql(f"insert into prepick_details (employee_id,customer_id,expire_date,qty,product_id,company_id,created_at,updated_at) values ({EMP},{KH},date_add(curdate(), interval 60 day),2,{P_STOCK},1,now(),now())")

# --- 4. Hàng tạm "Hàng tự khai thác" qua API thật (cây phân loại [TEST] mã TESTP3*)
if not sql("select id from product_types where code='TESTP3T'"):
    sql("insert into product_natures (code,name,barcode_template_type,status,is_auto_parts,created_at,updated_at) values ('TESTP3N','[TEST] Tính chất',1,1,0,now(),now())")
    n = sql("select id from product_natures where code='TESTP3N'")[0][0]
    sql(f"insert into product_function_groups (code,name,product_nature_id,status,created_at,updated_at) values ('TESTP3G','[TEST] Nhóm chức năng',{n},1,now(),now())")
    g = sql("select id from product_function_groups where code='TESTP3G'")[0][0]
    sql(f"insert into product_families (code,name,product_function_group_id,status,created_at,updated_at) values ('TESTP3F','[TEST] Nhóm sản phẩm',{g},1,now(),now())")
    f = sql("select id from product_families where code='TESTP3F'")[0][0]
    sql(f"insert into product_types (code,name,product_family_id,status,created_at,updated_at) values ('TESTP3T','[TEST] Loại sản phẩm',{f},1,now(),now())")
cat = {
    'model_id': int(sql("select id from product_models where status=1 limit 1")[0][0]),
    'brand_id': int(sql("select id from brands where status=1 limit 1")[0][0]),
    'manufacture_id': int(sql("select id from manufactures where status=1 and code is not null and code<>'' limit 1")[0][0]),
    'origin_id': int(sql("select id from origins where status=1 limit 1")[0][0]),
    'product_type_id': int(sql("select id from product_types where code='TESTP3T'")[0][0]),
    'units': [{'unit_id': int(sql("select id from units where status=1 limit 1")[0][0]), 'is_base': True, 'unit_coefficient': 1}],
    'vat_percent_tax_rate_id': int(sql("select id from tax_rates where status=1 limit 1")[0][0]),
}
def temp_product(name):
    if not sql(f"select id from products where name='{name}'"):
        st, r = api('POST', 'master-data/temp-products', {'name': name, **cat})
        print('tạo hàng tạm:', name, st, (r or {}).get('message') if isinstance(r, dict) else '')
    return sql(f"select id, code, product_cate from products where name='{name}'")[0]
t1 = temp_product('[TEST] Hàng tự khai thác – bộ dụng cụ E2E')
t2 = temp_product('[TEST] Hàng tự khai thác – đã vào kinh doanh')
sql(f"update product_company_coefficients set status=3 where product_id={t2[0]} and company_id=1")
ids['TMP_NEW'], ids['TMP_KD'] = int(t1[0]), int(t2[0])

# --- 5. BOM mẫu [TEST] (nội dung giống mẫu local id 1) qua API thật
def bom_template(name, payload):
    r = sql(f"select id from bom_templates where name='{name}'")
    if r:
        return int(r[0][0])
    st, body = api('POST', 'assign/bom-templates', {'name': name, 'status': 1, **payload})
    if st not in (200, 201):
        raise RuntimeError(f'tạo BOM mẫu: {st} {body}')
    return int(sql(f"select id from bom_templates where name='{name}'")[0][0])
ids['BT_TPL'] = bom_template('[TEST] BOM mẫu khoang sửa chữa', {
    'groups': [{'key': 'g1', 'name': 'Thiết bị nâng'}],
    'products': [{'product_id': 7465, 'unit_id': 73, 'qty': 2, 'group_key': 'g1'}, {'product_id': 7466, 'unit_id': 72, 'qty': 1.5}],
    'services': [{'cost_id': 1, 'note': 'phí'}]})
ids['BT_HIST'] = bom_template('[TEST] BOM mẫu xem lịch sử', {'products': [{'product_id': 7465, 'unit_id': 73, 'qty': 1}]})
ids['BT_NAME'] = 'BOM mẫu khoang sửa chữa'

# --- 6. BOM nháp để test áp BOM mẫu: BOM nháp mới nhất của namdangit, chưa có thì dùng BOM nháp gần nhất
# BOM nháp loại thường (bom_list_type=1) của namdangit — tạo qua API thật (chỉ người tạo mới sửa được BOM)
b = sql("select id from bom_lists where name='[TEST] BOM E2E báo giá' and status=1 order by id desc limit 1")
if not b:
    st, r = api('POST', 'assign/bom-lists', {'name': '[TEST] BOM E2E báo giá', 'status': 1, 'bom_list_type': 1,
                                             'prospective_project_id': PROJECT, 'customer_id': KH})
    print('tạo BOM nháp:', st, (r or {}).get('message') if isinstance(r, dict) else '')
    b = sql("select id from bom_lists where name='[TEST] BOM E2E báo giá' and status=1 order by id desc limit 1")
ids['BOM'] = int(b[0][0])

json.dump(ids, open(os.path.join(HERE, 'ids_dev.json'), 'w'), ensure_ascii=False, indent=1)
for k, v in ids.items():
    print(f'{k:14} {v}')
print(f"\nBáo giá test: {FE}/assign/quotations/{ids['Q_DEMAND']}/edit · có dự án: {FE}/assign/quotations/{ids['Q_PROJECT']}/edit")

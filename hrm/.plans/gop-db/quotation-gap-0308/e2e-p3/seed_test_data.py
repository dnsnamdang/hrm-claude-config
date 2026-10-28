"""Tạo / làm mới bộ DỮ LIỆU TEST TAY Phase 3 trên DB local (local_hrm_erp) — chạy lại nhiều lần không trùng.
python3 seed_test_data.py  → in ra bảng dữ liệu để test theo sheet "Huong_dan_test" của file Excel.
Mọi bản ghi tạo mới đều có tiền tố [TEST]."""
from common import *

KH = 210                 # khách hàng test (THẦN CHÂU GARAGE)
EMP = 13                 # namdangit
Q_DEMAND = 219           # báo giá ĐỘC LẬP đang tạo của KH 210 — test nhu cầu, tồn, Hỏi giá, mẫu
Q_PROJECT = 92           # báo giá CÓ DỰ ÁN (dự án 154, KH 210) — test nhu cầu theo dự án
P_STOCK = 43508          # CH-ER-BDCD: có công thức lắp ráp (Có thể LR > 0)
P_LOWPRICE = 3900        # TEWI-828127: giá bán lẻ 1đ ⇒ hiện nút Hỏi giá

# --- 1. Nhu cầu meeting của KH 210: 1 Đang theo dõi (chọn được), 1 Đã đóng, 1 gắn dự án 154
mid = sql("select id from meetings where code like '%-T210' limit 1")[0][0]
def demand(name, status, scope_id, project='NULL'):
    r = sql(f"select id from meeting_investment_demands where scope_name='{name}'")
    if r:
        sql(f"update meeting_investment_demands set status={status}, prospective_project_id={project} where id={r[0][0]}")
        return int(r[0][0])
    sql(f"insert into meeting_investment_demands (meeting_id,internal_business_scope_id,internal_business_scope_name,scope_id,scope_name,expected_amount,status,prospective_project_id,created_at,updated_at) values ({mid},990007,'Năng lượng',{scope_id},'{name}',7000000,{status},{project},now(),now())")
    return int(sql(f"select id from meeting_investment_demands where scope_name='{name}'")[0][0])
D_OPEN = demand('[TEST] Kết cấu thép KH210', 1, 44)
D_OPEN2 = demand('[TEST] Hệ thống khí nén KH210', 1, 3)
D_CLOSED = demand('[TEST] Trạm sạc KH210 (đã đóng)', 3, 45)
D_PROJECT = demand('[TEST] Cầu nâng (đã lập dự án 154)', 2, 1, 154)

# --- 2. Báo giá test về trạng thái Đang tạo, chưa chọn nhu cầu
sql(f"update quotations set status=1, price_approval_level=null, customer_demand_id=null, name='[TEST] Báo giá độc lập – test GAP 0308' where id={Q_DEMAND}")
sql(f"update quotations set status=1, customer_demand_id=null where id={Q_PROJECT}")

# --- 3. Đang giữ: namdangit giữ 2 cái CH-ER-BDCD cho KH 210 (công ty 1)
if not sql(f"select id from prepick_details where employee_id={EMP} and customer_id={KH} and product_id={P_STOCK}"):
    sql(f"insert into prepick_details (employee_id,customer_id,expire_date,qty,product_id,company_id,created_at,updated_at) values ({EMP},{KH},date_add(curdate(), interval 60 day),2,{P_STOCK},1,now(),now())")

# --- 4. Hàng tạm "Hàng tự khai thác" (tạo qua API thật ⇒ đi đúng luồng gắn loại)
name = '[TEST] Hàng tự khai thác – bộ dụng cụ E2E'
tmp = sql(f"select id, code from products where name='{name}'")
if not tmp:
    model = sql("select id from product_models where status=1 limit 1")[0][0]
    brand = sql("select id from brands where status=1 limit 1")[0][0]
    manu = sql("select id from manufactures where status=1 and code is not null and code<>'' limit 1")[0][0]
    origin = sql("select id from origins where status=1 limit 1")[0][0]
    # cây phân loại [TEST] (DB local chưa có loại SP đang hoạt động) — tạo 1 lần, mã TESTP3*
    if not sql("select id from product_types where code='TESTP3T'"):
        sql("insert into product_natures (code,name,barcode_template_type,status,is_auto_parts,created_at,updated_at) values ('TESTP3N','[TEST] Tính chất',1,1,0,now(),now())")
        n = sql("select id from product_natures where code='TESTP3N'")[0][0]
        sql(f"insert into product_function_groups (code,name,product_nature_id,status,created_at,updated_at) values ('TESTP3G','[TEST] Nhóm chức năng',{n},1,now(),now())")
        g = sql("select id from product_function_groups where code='TESTP3G'")[0][0]
        sql(f"insert into product_families (code,name,product_function_group_id,status,created_at,updated_at) values ('TESTP3F','[TEST] Nhóm sản phẩm',{g},1,now(),now())")
        f = sql("select id from product_families where code='TESTP3F'")[0][0]
        sql(f"insert into product_types (code,name,product_family_id,status,created_at,updated_at) values ('TESTP3T','[TEST] Loại sản phẩm',{f},1,now(),now())")
    ptype = sql("select id from product_types where code='TESTP3T'")[0][0]
    unit = sql("select id from units where status=1 limit 1")[0][0]
    tax = sql("select id from tax_rates where status=1 limit 1")[0][0]
    st, r = api('POST', 'master-data/temp-products', {
        'name': name, 'model_id': int(model), 'brand_id': int(brand), 'manufacture_id': int(manu), 'origin_id': int(origin),
        'product_type_id': int(ptype), 'units': [{'unit_id': int(unit), 'is_base': True, 'unit_coefficient': 1}],
        'vat_percent_tax_rate_id': int(tax)})
    print('tạo hàng tạm:', st, (r or {}).get('message'))
    tmp = sql(f"select id, code from products where name='{name}'")
TMP_ID, TMP_CODE = (tmp[0] if tmp else ('?', '?'))
# Hàng tự khai thác thứ 2: giả lập đã qua PTKD duyệt + tính giá ⇒ "Đang kinh doanh" ở công ty 1 (cửa sổ chọn hàng chỉ hiện hàng
# Đang kinh doanh). Tạo qua API thật rồi chuyển trạng thái công ty 1 = 3 (bước PTKD/tính giá làm tay thì dài).
name2 = '[TEST] Hàng tự khai thác – đã vào kinh doanh'
if not sql(f"select id from products where name='{name2}'"):
    st, r = api('POST', 'master-data/temp-products', {
        'name': name2, 'model_id': int(model), 'brand_id': int(brand), 'manufacture_id': int(manu), 'origin_id': int(origin),
        'product_type_id': int(ptype), 'units': [{'unit_id': int(unit), 'is_base': True, 'unit_coefficient': 1}],
        'vat_percent_tax_rate_id': int(tax)}) if tmp and 'model' in dir() else (None, None)
    if st is None:   # hàng tạm 1 đã có sẵn ⇒ lấy lại danh mục để tạo hàng 2
        model = sql("select id from product_models where status=1 limit 1")[0][0]; brand = sql("select id from brands where status=1 limit 1")[0][0]
        manu = sql("select id from manufactures where status=1 and code is not null and code<>'' limit 1")[0][0]; origin = sql("select id from origins where status=1 limit 1")[0][0]
        ptype = sql("select id from product_types where code='TESTP3T'")[0][0]; unit = sql("select id from units where status=1 limit 1")[0][0]
        tax = sql("select id from tax_rates where status=1 limit 1")[0][0]
        st, r = api('POST', 'master-data/temp-products', {
            'name': name2, 'model_id': int(model), 'brand_id': int(brand), 'manufacture_id': int(manu), 'origin_id': int(origin),
            'product_type_id': int(ptype), 'units': [{'unit_id': int(unit), 'is_base': True, 'unit_coefficient': 1}],
            'vat_percent_tax_rate_id': int(tax)})
    print('tạo hàng tự khai thác 2:', st)
TK = sql(f"select id, code from products where name='{name2}'")[0]
sql(f"update product_company_coefficients set status=3 where product_id={TK[0]} and company_id=1")
cate = sql(f"select product_cate from products where id={TMP_ID}")[0][0] if tmp else ''

rows = [
    ('Đăng nhập', 'namdangit@gmail.com / 2025Dns@2 (đủ quyền) · cannt.kd1@tanphat.com / Test@123 (không quyền BOM mẫu)'),
    ('Báo giá độc lập test', f"BG-2026-00{Q_DEMAND} (id {Q_DEMAND}) – KH 210 THẦN CHÂU GARAGE – {FE}/assign/quotations/{Q_DEMAND}/edit"),
    ('Báo giá có dự án test', f"{sql(f'select code from quotations where id={Q_PROJECT}')[0][0]} (id {Q_PROJECT}) – dự án 154 – {FE}/assign/quotations/{Q_PROJECT}/edit"),
    ('Nhu cầu chọn được', f'"[TEST] Kết cấu thép KH210" (id {D_OPEN}), "[TEST] Hệ thống khí nén KH210" (id {D_OPEN2})'),
    ('Nhu cầu KHÔNG hiện', f'"[TEST] Trạm sạc KH210 (đã đóng)" (id {D_CLOSED}) – đã đóng'),
    ('Nhu cầu của dự án 154', f'"[TEST] Cầu nâng (đã lập dự án 154)" (id {D_PROJECT})'),
    ('Hàng test tồn kho', f'CH-ER-BDCD (id {P_STOCK}) – có công thức lắp ráp; namdangit đang giữ 2 cái cho KH 210'),
    ('Hàng test Hỏi giá', f'TEWI-828127 (id {P_LOWPRICE}) – giá bán lẻ 1đ'),
    ('Hàng tạm tự khai thác', f'{TMP_CODE} "{name}" – mới tạo (chờ PTKD duyệt), product_cate = {cate}'),
    ('Hàng tự khai thác đã KD', f'{TK[1]} "{name2}" – Đang kinh doanh ở công ty 1 ⇒ lọc ra được trong cửa sổ chọn hàng'),
    ('Báo giá có nhóm (đã duyệt)', f'BG id 24 – {FE}/assign/quotations/24 (in tách nhóm, chi tiết)'),
    ('Báo giá nhiều thông số', f'BG id 45 – {FE}/assign/quotations/45 (in bản thông số kỹ thuật)'),
    ('Báo giá nhiều mức VAT', f'BG id 6 – {FE}/assign/quotations/6 (Tổng hợp theo VAT)'),
    ('BOM test', f'BOM-2026-00030 (id 30) – {FE}/assign/bom-list/30/edit'),
    ('BOM mẫu test', f'BMM-2026-00001 "[TEST] BOM mẫu khoang sửa chữa" + mẫu id 5 "[TEST] BOM mẫu xem lịch sử" – {FE}/assign/bom-templates'),
]
for k, v in rows:
    print(f'{k:28} {v}')

# Sinh SQL dữ liệu bỏ Nhóm hàng hoá cho go-live 20/10/2026 + mô phỏng trên dump DB (chỉ đọc).
# python3 -I sinh_sql_bo_nhom.py <file17.xlsx> <bang_tra_cay.xlsx> <thư mục dump tsv> <thư mục ra>
import openpyxl,sys,collections,re,os
f17,ftra,dump,out=sys.argv[1:5]
norm=lambda s: re.sub(r'\s+',' ',str(s).strip()).casefold() if s not in (None,'') and str(s).strip() else None
clean=lambda s: re.sub(r'\s+',' ',str(s).strip()) if s is not None else ''
rd=lambda f:[l.rstrip('\n').split('\t') for l in open(os.path.join(dump,f),encoding='utf-8')]
nz=lambda v: None if v=='NULL' else v
# Bảng tra: tên Loại -> mã LSP (do file import sinh, ổn định giữa các DB)
L2C={}
for r in list(openpyxl.load_workbook(ftra,read_only=True).worksheets[0].iter_rows(values_only=True))[1:]:
    if r[6]: L2C[norm(r[7])]=clean(r[6])
assert len(L2C)==968, len(L2C)
# File 17/10: mã hàng (G) -> Loại (E); nhóm cũ (I) -> Loại
code2l=collections.defaultdict(set); g2l=collections.defaultdict(set)
for r in list(openpyxl.load_workbook(f17,read_only=True,data_only=True)['NewERP Green Power'].iter_rows(values_only=True))[1:]:
    if not any(r[1:6]): continue
    l=norm(r[4])
    if not l: continue
    assert l in L2C, r[4]
    c=clean(r[6])
    if c: code2l[c.casefold()].add(L2C[l])
    try: g2l[int(float(r[8]))].add(L2C[l])
    except: pass
map_ma={c:next(iter(v)) for c,v in code2l.items() if len(v)==1}
conflict_ma={c:v for c,v in code2l.items() if len(v)>1}
map_nhom={g:next(iter(v)) for g,v in g2l.items() if len(v)==1}
# ---------- SQL ----------
q=lambda s: "'"+s.replace("\\","\\\\").replace("'","''")+"'"
def chunks(rows,n=500):
    for i in range(0,len(rows),n): yield rows[i:i+n]
L=[]
L.append("""-- =====================================================================================
-- Dữ liệu bỏ Nhóm hàng hoá — go-live 20/10/2026 (sinh bởi sinh_sql_bo_nhom.py, KHÔNG sửa tay)
-- Chạy SAU khi đã import đủ cây 4 cấp (968 Loại mã LSP.0001–LSP.0968) và SAU migration của đợt.
-- Mỗi bước: đọc số KIỂM TRƯỚC ⇒ chạy ⇒ đọc số KIỂM SAU. Lệch xa số trong README ⇒ DỪNG.
-- Bảng phụ tiền tố zz_golive2010_* (giữ tới khi nghiệm thu xong, rồi DROP — xem cuối file).
-- =====================================================================================
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ---------- B0. Điều kiện trước (chỉ đọc) ----------
SELECT COUNT(*) AS loai_lsp_phai_968 FROM product_types WHERE code LIKE 'LSP.%';
SELECT COUNT(*) AS hang_da_co_loai_truoc FROM products WHERE product_type_id IS NOT NULL;
SELECT COUNT(*) AS thuoc_tinh_loai_truoc FROM product_type_attributes;

-- ---------- B1. Bảng phụ + sao lưu (điểm lui) ----------
DROP TABLE IF EXISTS zz_golive2010_map_ma, zz_golive2010_map_nhom;
CREATE TABLE zz_golive2010_map_ma (product_code VARCHAR(255) NOT NULL, loai_code VARCHAR(32) NOT NULL, PRIMARY KEY (product_code))
  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE zz_golive2010_map_nhom (group_id BIGINT UNSIGNED NOT NULL, loai_code VARCHAR(32) NOT NULL, PRIMARY KEY (group_id))
  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS zz_golive2010_products_bak AS
  SELECT id, product_type_id, vat_percent, vat_percent_tax_rate_id FROM products;
CREATE TABLE IF NOT EXISTS zz_golive2010_product_types_bak AS SELECT id, long_stock_days FROM product_types;
CREATE TABLE IF NOT EXISTS zz_golive2010_pta_bak AS SELECT id FROM product_type_attributes;
""")
for ch in chunks(sorted(map_ma.items())):
    L.append("INSERT INTO zz_golive2010_map_ma (product_code, loai_code) VALUES\n"+",\n".join(f"({q(c)},{q(l)})" for c,l in ch)+";")
for ch in chunks(sorted(map_nhom.items())):
    L.append("INSERT INTO zz_golive2010_map_nhom (group_id, loai_code) VALUES\n"+",\n".join(f"({g},{q(l)})" for g,l in ch)+";")
L.append(f"""SELECT COUNT(*) AS map_ma_phai_{len(map_ma)} FROM zz_golive2010_map_ma;
SELECT COUNT(*) AS map_nhom_phai_{len(map_nhom)} FROM zz_golive2010_map_nhom;
-- Mã Loại trong bảng phụ không có trên DB (rỗng = đúng; có dòng ⇒ cây chưa import đủ — DỪNG)
SELECT DISTINCT m.loai_code FROM (SELECT loai_code FROM zz_golive2010_map_ma UNION SELECT loai_code FROM zz_golive2010_map_nhom) m
  LEFT JOIN product_types t ON t.code = m.loai_code WHERE t.id IS NULL;

-- ---------- B2. Gán Loại SP — (a) theo mã hàng trong file 17/10 ----------
UPDATE products p
  JOIN zz_golive2010_map_ma m ON m.product_code = TRIM(p.code)
  JOIN product_types t ON t.code = m.loai_code
SET p.product_type_id = t.id
WHERE p.product_type_id IS NULL;

-- ---------- B3. Gán Loại SP — (b) nhóm cũ ứng đúng 1 Loại (chỉ hàng còn trống sau B2) ----------
UPDATE products p
  JOIN zz_golive2010_map_nhom m ON m.group_id = p.group_id
  JOIN product_types t ON t.code = m.loai_code
SET p.product_type_id = t.id
WHERE p.product_type_id IS NULL;

SELECT COUNT(*) AS hang_dang_dung_co_loai_sau FROM products WHERE status <> 0 AND product_type_id IS NOT NULL;

-- ---------- B4. VAT: hàng VAT NULL ⇒ chép VAT nhóm (đúng giá trị ERP đang hiện qua dự phòng nhóm) ----------
-- (i) hàng có thuế suất riêng (vat_percent_tax_rate_id) ⇒ lấy % từ CHÍNH thuế suất của hàng
UPDATE products p JOIN tax_rates r ON r.id = p.vat_percent_tax_rate_id
SET p.vat_percent = r.tax_rate
WHERE p.vat_percent IS NULL;
-- (ii) hàng không có thuế suất riêng, nhóm VAT > 0 ⇒ chép % + thuế suất của nhóm
UPDATE products p JOIN `groups` g ON g.id = p.group_id
SET p.vat_percent = g.vat_percent,
    p.vat_percent_tax_rate_id = COALESCE(p.vat_percent_tax_rate_id, g.vat_percent_tax_rate_id)
WHERE p.vat_percent IS NULL AND g.vat_percent > 0;
-- Còn lại (nhóm VAT 0) ⇒ danh sách cho nghiệp vụ (file ds-hang-vat-trong.xlsx); số còn NULL:
SELECT COUNT(*) AS hang_dang_dung_vat_null_sau FROM products WHERE status <> 0 AND vat_percent IS NULL;

-- ---------- B5. Số ngày tồn lâu theo Loại = 180 (Loại chưa khai) ----------
UPDATE product_types SET long_stock_days = 180 WHERE long_stock_days IS NULL AND code LIKE 'LSP.%';
SELECT COUNT(*) AS loai_ton_lau_180 FROM product_types WHERE long_stock_days = 180;

-- ---------- B6. Thuộc tính: nhóm ứng đúng 1 Loại ⇒ product_type_attributes (gộp hợp, bỏ trùng) ----------
INSERT IGNORE INTO product_type_attributes (product_type_id, attribute_id, created_at, updated_at)
SELECT DISTINCT t.id, ag.attribute_id, NOW(), NOW()
FROM attribute_groups ag
  JOIN zz_golive2010_map_nhom m ON m.group_id = ag.group_id
  JOIN product_types t ON t.code = m.loai_code
  JOIN attributes a ON a.id = ag.attribute_id;
SELECT COUNT(*) AS thuoc_tinh_loai_sau, COUNT(DISTINCT product_type_id) AS so_loai FROM product_type_attributes;

-- ---------- (B7 Nhóm máy: CHƯA có trong file này — cần code ERP picker + HRM form trước) ----------

-- =====================================================================================
-- LUI (chỉ khi cần): trả về đúng giá trị trước B2–B6
-- UPDATE products p JOIN zz_golive2010_products_bak b ON b.id = p.id
--   SET p.product_type_id = b.product_type_id, p.vat_percent = b.vat_percent, p.vat_percent_tax_rate_id = b.vat_percent_tax_rate_id;
-- UPDATE product_types t JOIN zz_golive2010_product_types_bak b ON b.id = t.id SET t.long_stock_days = b.long_stock_days;
-- DELETE FROM product_type_attributes WHERE id NOT IN (SELECT id FROM zz_golive2010_pta_bak);
-- (Loại import sau lúc sao lưu không có trong *_bak — UPDATE JOIN bỏ qua, đúng ý.)
-- DỌN sau nghiệm thu: DROP TABLE zz_golive2010_map_ma, zz_golive2010_map_nhom, zz_golive2010_products_bak,
--   zz_golive2010_product_types_bak, zz_golive2010_pta_bak;
-- =====================================================================================
""")
os.makedirs(out,exist_ok=True)
open(os.path.join(out,'golive_bo_nhom_2010.sql'),'w',encoding='utf-8').write("\n".join(L))
# ---------- Mô phỏng trên dump (chỉ đọc) ----------
P=[dict(id=int(a),code=b,g=nz(c),t=nz(d),st=int(e),vat=nz(f),rate=nz(h)) for a,b,c,d,e,f,h in rd('products.tsv')]
G={int(r[0]):dict(name=r[1],vat=float(r[3]),rate=nz(r[4])) for r in rd('groups_full.tsv')}
TR={int(a):b for a,b in rd('tax_rates.tsv')}
T={r[1]:int(r[0]) for r in rd('types_code.tsv')}
miss=[l for l in set(map_ma.values())|set(map_nhom.values()) if l not in T]
cnt=collections.Counter(); vat_list=[]; vat_diff=[]
for p in P:
    use=p['st']!=0; g=int(p['g']) if p['g'] else None
    if p['t'] is None:
        if p['code'].strip().casefold() in map_ma: cnt['a '+('dùng' if use else 'xoá')]+=1
        elif g in map_nhom: cnt['b '+('dùng' if use else 'xoá')]+=1
        else: cnt['trống '+('dùng' if use else 'xoá')]+=1
    if p['vat'] is None:
        if p['rate'] and int(p['rate']) in TR:
            cnt['vat(i) '+('dùng' if use else 'xoá')]+=1
            if g in G and float(TR[int(p['rate'])])!=G[g]['vat']: vat_diff.append((p['id'],p['code'],TR[int(p['rate'])],G[g]['vat']))
        elif g in G and G[g]['vat']>0: cnt['vat(ii) '+('dùng' if use else 'xoá')]+=1
        else:
            cnt['vat còn NULL '+('dùng' if use else 'xoá')]+=1
            if use: vat_list.append((p['id'],p['code'],g,G[g]['name'] if g in G else ''))
AG=[(int(a),int(b)) for a,b in rd('attr_groups.tsv')]
pta={(map_nhom[g],a) for g,a in AG if g in map_nhom}
print('Loại thiếu trên DB:',len(miss),'| map mã',len(map_ma),'(mã lệch Loại bỏ qua:',len(conflict_ma),') | map nhóm',len(map_nhom))
for k in sorted(cnt): print(' ',k,cnt[k])
print('  VAT(i) khác VAT nhóm (ERP đang hiện VAT nhóm):',len(vat_diff))
print('  thuộc tính: cặp',len(pta),'| Loại',len({t for t,_ in pta}))
wb=openpyxl.Workbook(); ws=wb.active; ws.title='VAT con trong'
ws.append(['ID hàng','Mã hàng','ID nhóm','Nhóm hàng (VAT 0)']); [ws.append(list(r)) for r in vat_list]
ws2=wb.create_sheet('VAT rieng khac nhom'); ws2.append(['ID hàng','Mã hàng','VAT theo thuế suất của hàng','VAT nhóm (ERP đang hiện)']); [ws2.append(list(r)) for r in vat_diff]
wb.save(os.path.join(out,'ds-hang-vat-trong.xlsx'))

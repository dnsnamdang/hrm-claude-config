# Sinh SQL nhập cây phân loại 4 cấp (Tính chất › Nhóm chức năng › Nhóm SP › Loại SP) từ bản dump giacty
# (cây đã nhập qua màn Import 19/10 + tick "Là phụ tùng ô tô" TCHH.0005). python3 -I sinh_sql_cay4.py <json> <out.sql>
import json,sys,collections
src,out=sys.argv[1:3]
R=json.load(open(src,encoding='utf-8'))
cnt=collections.Counter(r['cap'] for r in R); assert [cnt[i] for i in (1,2,3,4)]==[6,48,282,968], cnt
for r in R:
    if r['cap']==1 and r['auto']: r['hist']=r['hist'].replace('"is_auto_parts":"Không"','"is_auto_parts":"Có"')
q=lambda s: 'NULL' if s is None else "'"+str(s).replace("\\","\\\\").replace("'","''")+"'"
T={1:('product_natures',None),2:('product_function_groups','product_nature_id'),3:('product_families','product_function_group_id'),4:('product_types','product_family_id')}
L=["""-- =====================================================================================
-- Cây phân loại hàng hoá 4 cấp — go-live 20/10/2026 (sinh bởi sinh_sql_cay4.py, KHÔNG sửa tay)
-- Tính chất 6 (TCHH.0001–0006) › Nhóm chức năng 48 (NCN.) › Nhóm SP 282 (NSP.) › Loại SP 968 (LSP.)
-- = đúng dữ liệu đã nhập qua màn Import trên giacty 19/10 (file import-cay-1710) + TCHH.0005 "Là phụ tùng ô tô".
-- THAY CÂY CŨ (user chốt 20/10): prod đã có cây nhập 15/10 bản file cũ (6/48/270/959, mã TRÙNG dãy NCN./NSP./LSP. nhưng KHÁC tên)
--   ⇒ sao lưu (zz_golive2010_cay_cu_*), ghi lịch sử "delete", xoá cây cũ, rồi nạp cây 17/10. CHỐT CHẶN: chỉ xoá + nạp khi 0 hàng
--   và 0 thuộc tính Loại trỏ vào cây (biến @ok); không đạt ⇒ KHÔNG đổi gì (K0b in @ok = 0) — DỪNG báo dev.
-- Sau khi thay: mã đã có thì bỏ qua (chạy lại lần 2 = 0 dòng). Bản ghi mới ghi lịch sử "create" như màn Import.
-- Chạy SAU migration, TRƯỚC golive_bo_nhom_2010.sql (bước đó cần đủ 968 Loại).
-- =====================================================================================
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET @nguoi_chay = 13;   -- 13 = DNS Admin (user chốt 20/10). (tuỳ chọn) employees.id người chạy ⇒ created_by / updated_by / changed_by lịch sử

-- K0. Kiểm trước (chỉ đọc) — prod 20/10 (bản sao): 6 · 48 · 270 · 959 (cây cũ) ⇒ sẽ được thay.
SELECT (SELECT COUNT(*) FROM product_natures) AS tinh_chat, (SELECT COUNT(*) FROM product_function_groups) AS nhom_cn,
       (SELECT COUNT(*) FROM product_families) AS nhom_sp, (SELECT COUNT(*) FROM product_types) AS loai_sp;
SELECT id, code, name FROM product_natures ORDER BY id;   -- dòng rác (vd TCHH.GJGH "hjjhjh") ⇒ xoá trên màn Tính chất SAU khi chạy

DROP TABLE IF EXISTS zz_golive2010_cay4;
CREATE TABLE zz_golive2010_cay4 (cap TINYINT NOT NULL, code VARCHAR(32) NOT NULL, name VARCHAR(255) NOT NULL, parent_code VARCHAR(32) NULL,
  barcode_template_type TINYINT UNSIGNED NULL, is_auto_parts TINYINT UNSIGNED NULL, history_json TEXT NOT NULL, PRIMARY KEY (code))
  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS zz_golive2010_cay4_moc AS
  SELECT (SELECT IFNULL(MAX(id),0) FROM product_natures) AS nature_max, (SELECT IFNULL(MAX(id),0) FROM product_function_groups) AS fgroup_max,
         (SELECT IFNULL(MAX(id),0) FROM product_families) AS family_max, (SELECT IFNULL(MAX(id),0) FROM product_types) AS type_max,
         (SELECT IFNULL(MAX(id),0) FROM catalog_histories) AS history_max;
"""]
for i in range(0,len(R),300):
    L.append("INSERT INTO zz_golive2010_cay4 (cap, code, name, parent_code, barcode_template_type, is_auto_parts, history_json) VALUES\n"+
      ",\n".join(f"({r['cap']},{q(r['code'])},{q(r['name'])},{q(r['parent'])},{q(r.get('btt'))},{q(r.get('auto'))},{q(r['hist'])})" for r in R[i:i+300])+";")
L.append("""SELECT cap, COUNT(*) AS so_dong FROM zz_golive2010_cay4 GROUP BY cap ORDER BY cap;   -- 6 · 48 · 282 · 968

-- K0b. Chốt chặn thay cây: cây hiện có KHÔNG được dùng (hàng / thuộc tính Loại). Cây đã đúng bản 17/10 (chạy lần 2) ⇒ không xoá.
SET @da_dung = (SELECT COUNT(*) FROM products WHERE product_type_id IS NOT NULL) + (SELECT COUNT(*) FROM product_type_attributes);
SET @da_la_cay_moi = (SELECT COUNT(*) FROM product_types t JOIN zz_golive2010_cay4 z ON z.cap = 4 AND z.code = t.code AND z.name = t.name);
SET @ok = IF((SELECT COUNT(*) FROM product_types) = 0 OR @da_la_cay_moi = 968 OR @da_dung = 0, 1, 0);
SET @thay = IF(@ok = 1 AND @da_la_cay_moi <> 968 AND (SELECT COUNT(*) FROM product_types) > 0, 1, 0);
SELECT @da_dung AS hang_va_thuoc_tinh_dang_dung_cay_PHAI_0, @da_la_cay_moi AS loai_da_dung_ban_1710, @ok AS ok_PHAI_1, @thay AS se_thay_cay_cu;

-- R. Thay cây cũ (chỉ khi @thay = 1): sao lưu ⇒ lịch sử "delete" ⇒ xoá theo thứ tự con → cha
CREATE TABLE IF NOT EXISTS zz_golive2010_cay_cu_natures AS SELECT * FROM product_natures WHERE @thay = 1;
CREATE TABLE IF NOT EXISTS zz_golive2010_cay_cu_fgroups AS SELECT * FROM product_function_groups WHERE @thay = 1;
CREATE TABLE IF NOT EXISTS zz_golive2010_cay_cu_families AS SELECT * FROM product_families WHERE @thay = 1;
CREATE TABLE IF NOT EXISTS zz_golive2010_cay_cu_types AS SELECT * FROM product_types WHERE @thay = 1;
INSERT INTO catalog_histories (table_name, table_id, action, old_value, new_value, note, changed_by, changed_at, created_at, updated_at)
SELECT x.t, x.id, 'delete', JSON_OBJECT('code', x.code, 'name', x.name), NULL, 'Thay cây phân loại bản 17/10 (go-live 20/10)', @nguoi_chay, NOW(), NOW(), NOW()
FROM (SELECT 'product_types' t, id, code, name FROM product_types UNION ALL SELECT 'product_families', id, code, name FROM product_families
      UNION ALL SELECT 'product_function_groups', id, code, name FROM product_function_groups UNION ALL SELECT 'product_natures', id, code, name FROM product_natures) x
WHERE @thay = 1;
DELETE FROM product_types WHERE @thay = 1;
DELETE FROM product_families WHERE @thay = 1;
DELETE FROM product_function_groups WHERE @thay = 1;
DELETE FROM product_natures WHERE @thay = 1;
SELECT (SELECT COUNT(*) FROM product_types) AS loai_sau_buoc_R, (SELECT COUNT(*) FROM zz_golive2010_cay_cu_types) AS loai_cu_da_sao_luu;

-- K1. Xung đột (rỗng = đúng): tên đã có trên DB dưới MÃ KHÁC ⇒ INSERT sẽ vấp UNIQUE(name) — DỪNG, báo dev/nghiệp vụ
SELECT z.cap, z.code, z.name, x.code AS ma_tren_db FROM zz_golive2010_cay4 z
JOIN (SELECT 1 cap, code, name FROM product_natures UNION ALL SELECT 2, code, name FROM product_function_groups
      UNION ALL SELECT 3, code, name FROM product_families UNION ALL SELECT 4, code, name FROM product_types) x
  ON x.cap = z.cap AND x.name = z.name AND x.code <> z.code;
""")
for cap in (1,2,3,4):
    t,pc=T[cap]
    pt=T[cap-1][0] if cap>1 else None
    L.append(f"-- C{cap}. {t}")
    L.append(f"SET @m = (SELECT IFNULL(MAX(id),0) FROM {t});")
    if cap==1:
        L.append(f"""INSERT INTO product_natures (code, name, description, barcode_template_type, is_auto_parts, is_service_product, is_service_quotation,
  status, created_by, updated_by, created_at, updated_at)
SELECT z.code, z.name, NULL, z.barcode_template_type, z.is_auto_parts, 0, 0, 1, @nguoi_chay, @nguoi_chay, NOW(), NOW()
FROM zz_golive2010_cay4 z WHERE @ok = 1 AND z.cap = 1 AND NOT EXISTS (SELECT 1 FROM product_natures x WHERE x.code = z.code);""")
    elif cap<4:
        L.append(f"""INSERT INTO {t} (code, name, description, {pc}, status, created_by, updated_by, created_at, updated_at)
SELECT z.code, z.name, NULL, p.id, 1, @nguoi_chay, @nguoi_chay, NOW(), NOW()
FROM zz_golive2010_cay4 z JOIN {pt} p ON p.code = z.parent_code
WHERE @ok = 1 AND z.cap = {cap} AND NOT EXISTS (SELECT 1 FROM {t} x WHERE x.code = z.code);""")
    else:
        L.append(f"""INSERT INTO product_types (code, name, description, product_family_id, serial_required,
  vat_percent_tax_rate_id, long_stock_days, ingredient, warning, user_manual, barcode_template_type, status, created_by, updated_by, created_at, updated_at)
SELECT z.code, z.name, NULL, p.id, 0, NULL, NULL, NULL, NULL, NULL, NULL, 1, @nguoi_chay, @nguoi_chay, NOW(), NOW()
FROM zz_golive2010_cay4 z JOIN product_families p ON p.code = z.parent_code
WHERE @ok = 1 AND z.cap = 4 AND NOT EXISTS (SELECT 1 FROM product_types x WHERE x.code = z.code);""")
    L.append(f"""INSERT INTO catalog_histories (table_name, table_id, action, old_value, new_value, note, changed_by, changed_at, created_at, updated_at)
SELECT '{t}', x.id, 'create', NULL, z.history_json, NULL, @nguoi_chay, NOW(), NOW(), NOW()
FROM {t} x JOIN zz_golive2010_cay4 z ON z.cap = {cap} AND z.code = x.code WHERE x.id > @m;
""")
L.append("""-- K2. Kiểm sau: mỗi cấp đủ mã + ĐÚNG TÊN + đúng cha (mọi số = 0); tổng dòng phải đúng 6 · 48 · 282 · 968
SELECT
 (SELECT COUNT(*) FROM zz_golive2010_cay4 z LEFT JOIN product_natures x ON x.code = z.code WHERE z.cap = 1 AND (x.id IS NULL OR x.name <> z.name)) AS thieu_tc,
 (SELECT COUNT(*) FROM zz_golive2010_cay4 z LEFT JOIN product_function_groups x ON x.code = z.code
    LEFT JOIN product_natures p ON p.id = x.product_nature_id WHERE z.cap = 2 AND (x.id IS NULL OR x.name <> z.name OR NOT (p.code <=> z.parent_code))) AS lech_ncn,
 (SELECT COUNT(*) FROM zz_golive2010_cay4 z LEFT JOIN product_families x ON x.code = z.code
    LEFT JOIN product_function_groups p ON p.id = x.product_function_group_id WHERE z.cap = 3 AND (x.id IS NULL OR x.name <> z.name OR NOT (p.code <=> z.parent_code))) AS lech_nsp,
 (SELECT COUNT(*) FROM zz_golive2010_cay4 z LEFT JOIN product_types x ON x.code = z.code
    LEFT JOIN product_families p ON p.id = x.product_family_id WHERE z.cap = 4 AND (x.id IS NULL OR x.name <> z.name OR NOT (p.code <=> z.parent_code))) AS lech_lsp;
SELECT (SELECT COUNT(*) FROM product_natures) tc, (SELECT COUNT(*) FROM product_function_groups) ncn, (SELECT COUNT(*) FROM product_families) nsp, (SELECT COUNT(*) FROM product_types) lsp;
SELECT code, name, is_auto_parts, barcode_template_type FROM product_natures WHERE code LIKE 'TCHH.%' ORDER BY code;   -- TCHH.0005 is_auto_parts = 1

-- =====================================================================================
-- LUI (chỉ khi cần, và TRƯỚC khi chạy golive_bo_nhom_2010.sql — sau đó hàng đã trỏ Loại):
-- DELETE FROM catalog_histories WHERE id > (SELECT history_max FROM zz_golive2010_cay4_moc)
--   AND table_name IN ('product_natures','product_function_groups','product_families','product_types');
-- DELETE FROM product_types WHERE id > (SELECT type_max FROM zz_golive2010_cay4_moc);
-- DELETE FROM product_families WHERE id > (SELECT family_max FROM zz_golive2010_cay4_moc);
-- DELETE FROM product_function_groups WHERE id > (SELECT fgroup_max FROM zz_golive2010_cay4_moc);
-- DELETE FROM product_natures WHERE id > (SELECT nature_max FROM zz_golive2010_cay4_moc);
-- Khôi phục cây cũ (nếu cần): INSERT INTO product_natures SELECT * FROM zz_golive2010_cay_cu_natures; … fgroups → families → types (sau khi xoá cây mới).
-- DỌN sau nghiệm thu: DROP TABLE zz_golive2010_cay4, zz_golive2010_cay4_moc, zz_golive2010_cay_cu_natures, zz_golive2010_cay_cu_fgroups,
--   zz_golive2010_cay_cu_families, zz_golive2010_cay_cu_types;
-- =====================================================================================
""")
open(out,'w',encoding='utf-8').write("\n".join(L))
print('ok',dict(cnt))

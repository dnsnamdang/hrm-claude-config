import sys,json
d=json.load(open(sys.argv[1])); out=sys.argv[2]
def q(s): return 'NULL' if s is None else "'"+str(s).replace("\\","\\\\").replace("'","''")+"'"
TB={3:'product_families',4:'product_types'}
dm=[n for n in d['new']]
assert all(n['cap'] in (3,4) for n in dm)
L=[]
w=L.append
w("""-- =====================================================================================
-- Cập nhật danh mục 4 cấp cho hàng ETEK GREEN — 21/10/2026 (sinh bởi sinh_sql.py từ "Copy of UPDATE hàng green.xlsx", KHÔNG sửa tay)
-- Luật đã chốt với user 21/10 (chi tiết + danh sách: tong-ket-danh-muc-green-2110.xlsx):
--  1. So tên coi ',' và '-' là một (không phân biệt hoa thường/dấu như MySQL); danh mục mới đặt tên kiểu gạch ngang.
--  2. Loại SP đã có trên DB ⇒ lấy 4 cấp đang có trên DB (bỏ qua cha ghi trong file). Nhóm SP / Nhóm CN đã có ⇒ dùng cha trên DB.
--  3. Bỏ qua: model chưa có trên DB · Loại = "0" · danh mục MỚI mà file đặt dưới >1 cha (Mặt bích, Ống ruột gà, Kẹp đỡ ống, Bình - Bồn - Bể).
--  4. Mã hàng đã có Loại SP ⇒ giữ nguyên. Gán cả mã đã xoá (status 0).
--  5. Loại mới: tồn lâu 180, VAT trống, mẫu tem trống, không serial, không thuộc tính, Hoạt động. Lịch sử "create" ở catalog_histories;
--     gán Loại cho hàng KHÔNG ghi lịch sử hàng hoá (như go-live 20/10).
-- Tạo mới: %d Nhóm SP (NSP.%s–NSP.%s) · %d Loại SP (LSP.%s–LSP.%s). Gán Loại cho %d mã hàng.
-- CHỐT CHẶN: tên/mã mới đã có trên DB dưới mã/tên khác ⇒ @ok = 0 ⇒ KHÔNG ghi gì — DỪNG báo dev. Chạy lại lần 2 = 0 dòng đổi.
-- =====================================================================================
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET @nguoi_chay = 13;   -- 13 = DNS Admin
""" % (sum(n['cap']==3 for n in dm), *[f(n['code'] for n in dm if n['cap']==3)[4:] for f in (min,max)], sum(n['cap']==4 for n in dm), *[f(n['code'] for n in dm if n['cap']==4)[4:] for f in (min,max)], len(d['upd'])))
w("""-- K0. Kiểm trước (chỉ đọc) — bản sao prod hrm_erp_21_10: 6 · 48 · 282 · 968; mã cuối NSP.0282 / LSP.0968
SELECT (SELECT COUNT(*) FROM product_natures) tc, (SELECT COUNT(*) FROM product_function_groups) ncn, (SELECT COUNT(*) FROM product_families) nsp,
       (SELECT COUNT(*) FROM product_types) lsp, (SELECT MAX(code) FROM product_families) ma_nsp_cuoi, (SELECT MAX(code) FROM product_types) ma_lsp_cuoi;

CREATE TABLE IF NOT EXISTS zz_green2110_moc AS
  SELECT (SELECT IFNULL(MAX(id),0) FROM product_families) family_max, (SELECT IFNULL(MAX(id),0) FROM product_types) type_max,
         (SELECT IFNULL(MAX(id),0) FROM catalog_histories) history_max, NOW() chay_luc;

DROP TABLE IF EXISTS zz_green2110_dm;
CREATE TABLE zz_green2110_dm (cap TINYINT NOT NULL, code VARCHAR(32) NOT NULL, name VARCHAR(255) NOT NULL, parent_code VARCHAR(32) NOT NULL,
  history_json TEXT NOT NULL, PRIMARY KEY (code)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;""")
vals=[]
for n in dm:
    if n['cap']==3:
        h=json.dumps({"code":n['code'],"name":n['name'],"description":None,"status":"Hoạt động","product_function_group_id":n['pname']},ensure_ascii=False,separators=(',',':'))
    else:
        h=json.dumps({"code":n['code'],"name":n['name'],"description":None,"status":"Hoạt động","product_family_id":n['pname'],"serial_required":"Không bắt buộc","vat_percent_tax_rate_id":None,"long_stock_days":180,"ingredient":None,"warning":None,"user_manual":None,"barcode_template_type":None},ensure_ascii=False,separators=(',',':'))
    vals.append(f"({n['cap']},{q(n['code'])},{q(n['name'])},{q(n['pcode'])},{q(h)})")
w("INSERT INTO zz_green2110_dm (cap, code, name, parent_code, history_json) VALUES\n"+",\n".join(vals)+";")
w("""
DROP TABLE IF EXISTS zz_green2110_hang;
CREATE TABLE zz_green2110_hang (product_id BIGINT UNSIGNED NOT NULL, product_code VARCHAR(255) NOT NULL, loai_code VARCHAR(32) NOT NULL,
  PRIMARY KEY (product_id)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;""")
hv=[f"({u['pid']},{q(u['code'])},{q(u['path'][3][0])})" for u in d['upd']]
for i in range(0,len(hv),200): w("INSERT INTO zz_green2110_hang (product_id, product_code, loai_code) VALUES\n"+",\n".join(hv[i:i+200])+";")
w("""
-- K1. Xung đột (PHẢI rỗng): mã mới đã có trên DB với TÊN khác, hoặc tên mới đã có dưới MÃ khác ⇒ @ok = 0
SELECT z.cap, z.code, z.name, x.code ma_db, x.name ten_db FROM zz_green2110_dm z
JOIN (SELECT 3 cap, code, name FROM product_families UNION ALL SELECT 4, code, name FROM product_types) x
  ON x.cap = z.cap AND ((x.code = z.code AND x.name <> z.name) OR (x.name = z.name AND x.code <> z.code));
SET @xung_dot = (SELECT COUNT(*) FROM zz_green2110_dm z
  JOIN (SELECT 3 cap, code, name FROM product_families UNION ALL SELECT 4, code, name FROM product_types) x
    ON x.cap = z.cap AND ((x.code = z.code AND x.name <> z.name) OR (x.name = z.name AND x.code <> z.code)));
-- cha có sẵn phải tồn tại: Nhóm SP mới → Nhóm CN; Loại mới → Nhóm SP (có sẵn hoặc mới trong file)
SET @thieu_cha = (SELECT COUNT(*) FROM zz_green2110_dm z WHERE z.cap = 3 AND NOT EXISTS (SELECT 1 FROM product_function_groups g WHERE g.code = z.parent_code))
               + (SELECT COUNT(*) FROM zz_green2110_dm z WHERE z.cap = 4 AND NOT EXISTS (SELECT 1 FROM product_families f WHERE f.code = z.parent_code)
                    AND NOT EXISTS (SELECT 1 FROM zz_green2110_dm y WHERE y.cap = 3 AND y.code = z.parent_code));
-- Loại có sẵn mà hàng trỏ tới phải tồn tại
SET @thieu_loai = (SELECT COUNT(*) FROM zz_green2110_hang h WHERE NOT EXISTS (SELECT 1 FROM product_types t WHERE t.code = h.loai_code)
                    AND NOT EXISTS (SELECT 1 FROM zz_green2110_dm y WHERE y.cap = 4 AND y.code = h.loai_code));
SET @thieu_hang = (SELECT COUNT(*) FROM zz_green2110_hang h LEFT JOIN products p ON p.id = h.product_id WHERE p.id IS NULL OR p.code <> h.product_code);
SET @ok = IF(@xung_dot = 0 AND @thieu_cha = 0 AND @thieu_loai = 0 AND @thieu_hang = 0, 1, 0);
SELECT @xung_dot xung_dot_PHAI_0, @thieu_cha thieu_cha_PHAI_0, @thieu_loai thieu_loai_PHAI_0, @thieu_hang thieu_hang_PHAI_0, @ok ok_PHAI_1;
SELECT COUNT(*) hang_trong_ds, SUM(p.product_type_id IS NULL) se_gan_lan_nay, SUM(p.product_type_id IS NOT NULL) da_co_loai_bo_qua
FROM zz_green2110_hang h JOIN products p ON p.id = h.product_id;

-- Sao lưu Loại hiện tại của đúng các mã trong danh sách (giữ bản lần chạy đầu)
CREATE TABLE IF NOT EXISTS zz_green2110_products_bak AS SELECT p.id, p.product_type_id FROM products p JOIN zz_green2110_hang h ON h.product_id = p.id;

-- C3. Nhóm sản phẩm mới
SET @m = (SELECT IFNULL(MAX(id),0) FROM product_families);
INSERT INTO product_families (code, name, description, product_function_group_id, status, created_by, updated_by, created_at, updated_at)
SELECT z.code, z.name, NULL, g.id, 1, @nguoi_chay, @nguoi_chay, NOW(), NOW()
FROM zz_green2110_dm z JOIN product_function_groups g ON g.code = z.parent_code
WHERE @ok = 1 AND z.cap = 3 AND NOT EXISTS (SELECT 1 FROM product_families x WHERE x.code = z.code);
INSERT INTO catalog_histories (table_name, table_id, action, old_value, new_value, note, changed_by, changed_at, created_at, updated_at)
SELECT 'product_families', x.id, 'create', NULL, z.history_json, 'Bổ sung danh mục hàng ETEK GREEN 21/10', @nguoi_chay, NOW(), NOW(), NOW()
FROM product_families x JOIN zz_green2110_dm z ON z.cap = 3 AND z.code = x.code WHERE x.id > @m;

-- C4. Loại sản phẩm mới
SET @m = (SELECT IFNULL(MAX(id),0) FROM product_types);
INSERT INTO product_types (code, name, description, product_family_id, serial_required, vat_percent_tax_rate_id, long_stock_days,
  ingredient, warning, user_manual, barcode_template_type, status, created_by, updated_by, created_at, updated_at)
SELECT z.code, z.name, NULL, f.id, 0, NULL, 180, NULL, NULL, NULL, NULL, 1, @nguoi_chay, @nguoi_chay, NOW(), NOW()
FROM zz_green2110_dm z JOIN product_families f ON f.code = z.parent_code
WHERE @ok = 1 AND z.cap = 4 AND NOT EXISTS (SELECT 1 FROM product_types x WHERE x.code = z.code);
INSERT INTO catalog_histories (table_name, table_id, action, old_value, new_value, note, changed_by, changed_at, created_at, updated_at)
SELECT 'product_types', x.id, 'create', NULL, z.history_json, 'Bổ sung danh mục hàng ETEK GREEN 21/10', @nguoi_chay, NOW(), NOW(), NOW()
FROM product_types x JOIN zz_green2110_dm z ON z.cap = 4 AND z.code = x.code WHERE x.id > @m;

-- G. Gán Loại SP cho hàng (chỉ hàng đang trống Loại)
UPDATE products p
  JOIN zz_green2110_hang h ON h.product_id = p.id
  JOIN product_types t ON t.code = h.loai_code
SET p.product_type_id = t.id
WHERE @ok = 1 AND p.product_type_id IS NULL;
SELECT ROW_COUNT() AS hang_vua_gan;

-- K2. Kiểm sau (mọi số lệch PHẢI 0)
SELECT
 (SELECT COUNT(*) FROM zz_green2110_dm z LEFT JOIN product_families x ON x.code = z.code LEFT JOIN product_function_groups p ON p.id = x.product_function_group_id
   WHERE z.cap = 3 AND (x.id IS NULL OR x.name <> z.name OR NOT (p.code <=> z.parent_code))) lech_nsp,
 (SELECT COUNT(*) FROM zz_green2110_dm z LEFT JOIN product_types x ON x.code = z.code LEFT JOIN product_families p ON p.id = x.product_family_id
   WHERE z.cap = 4 AND (x.id IS NULL OR x.name <> z.name OR NOT (p.code <=> z.parent_code))) lech_lsp,
 (SELECT COUNT(*) FROM zz_green2110_hang h JOIN products p ON p.id = h.product_id JOIN zz_green2110_products_bak b ON b.id = p.id
   LEFT JOIN product_types t ON t.id = p.product_type_id WHERE b.product_type_id IS NULL AND NOT (t.code <=> h.loai_code)) lech_hang;
SELECT (SELECT COUNT(*) FROM product_families) nsp, (SELECT COUNT(*) FROM product_types) lsp,
       (SELECT COUNT(*) FROM catalog_histories WHERE id > (SELECT history_max FROM zz_green2110_moc)) lich_su_moi;

-- =====================================================================================
-- LUI (chỉ khi cần):
-- UPDATE products p JOIN zz_green2110_products_bak b ON b.id = p.id SET p.product_type_id = b.product_type_id;
-- DELETE FROM catalog_histories WHERE id > (SELECT history_max FROM zz_green2110_moc) AND table_name IN ('product_families','product_types')
--   AND note = 'Bổ sung danh mục hàng ETEK GREEN 21/10';
-- DELETE FROM product_types WHERE id > (SELECT type_max FROM zz_green2110_moc) AND code IN (SELECT code FROM zz_green2110_dm WHERE cap = 4);
-- DELETE FROM product_families WHERE id > (SELECT family_max FROM zz_green2110_moc) AND code IN (SELECT code FROM zz_green2110_dm WHERE cap = 3);
-- DỌN sau nghiệm thu: DROP TABLE zz_green2110_dm, zz_green2110_hang, zz_green2110_moc, zz_green2110_products_bak;
-- =====================================================================================""")
open(out,'w',encoding='utf-8').write('\n'.join(L)+'\n')
print('ok',out)

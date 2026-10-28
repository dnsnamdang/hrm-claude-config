# Sinh SQL catalog "Dịch vụ ô tô": tạo cây Chương › Mục › Tiểu mục (tìm-hoặc-tạo) + gắn hàng ↔ Tiểu mục cho công ty 1·2·3·4.
# python3 -I sinh_catalog.py <file catalog.xlsx> <mã lĩnh vực trên DB đích, vd LVCTKD.0007> <thư mục ra>
import openpyxl,sys,re,os
src,scope_code,out=sys.argv[1:4]
COMPANY_IDS=[1,2,3,4]   # user 20/10: Tân Phát · Hải Phòng · Vinh · Sài Gòn
clean=lambda s: re.sub(r'\s+',' ',str(s).strip()) if s not in (None,'') and str(s).strip() else ''
rows=[[clean(x) for x in r[:6]] for r in list(openpyxl.load_workbook(src,data_only=True).worksheets[0].iter_rows(values_only=True))[2:]]
rows=[r for r in rows if any(r)]
assert all(r[0]=='Dịch vụ ô tô' and r[1] and r[2] and r[3] for r in rows)
assert all(len(x)<=64 for r in rows for x in r[1:4])
tm=list(dict.fromkeys((r[1],r[2],r[3]) for r in rows))
links=sorted(set((r[5],r[1],r[2],r[3]) for r in rows if r[5]))
nch=len({t[0] for t in tm}); nmu=len({t[:2] for t in tm})
cids=', '.join(map(str,COMPANY_IDS))
q=lambda s: "'"+s.replace("\\","\\\\").replace("'","''")+"'"
L=[f"""-- =====================================================================================
-- Catalog kinh doanh "Dịch vụ ô tô" — go-live 20/10/2026 (sinh bởi sinh_catalog.py, KHÔNG sửa tay)
-- 1) Tạo cây Chương › Mục › Tiểu mục dưới Lĩnh vực @scope_code: TÌM-HOẶC-TẠO theo (tên, cha) — có rồi thì dùng lại,
--    không tạo trùng; bản ghi mới ghi lịch sử "create" như màn Import. Không đụng chương cũ ERP (không có lĩnh vực).
-- 2) Gắn hàng ↔ Tiểu mục cho các CÔNG TY {', '.join(map(str,COMPANY_IDS))} (1 Tân Phát · 2 Hải Phòng · 3 Vinh · 4 Sài Gòn) — MỖI công ty 1 bộ, luật như popup "Xây dựng catalog": hàng còn dùng, có dòng tại công ty,
--    không hàng tạm / ngừng KD; nhánh đang hoạt động; trùng bỏ qua.
-- Chạy SAU backfill giá theo công ty (cần product_company_coefficients). Chạy lại lần 2 an toàn (0 dòng mới).
-- Số kỳ vọng: {nch} Chương · {nmu} Mục · {len(tm)} Tiểu mục · {len(links)} dòng (mã × Tiểu mục) trong file.
-- =====================================================================================
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET @scope_code = {q(scope_code)};
SET @nguoi_chay = 13;   -- 13 = DNS Admin (user chốt 20/10). ⚠️ BẮT BUỘC: employees.id người chạy (chapters/job_groups/job_clusters.created_by NOT NULL + FK employees). NULL ⇒ không ghi gì

-- C0. Kiểm trước (chỉ đọc)
SELECT id, name, status FROM internal_business_scopes WHERE code = @scope_code;   -- phải ra "Dịch vụ ô tô", status 1 — khác ⇒ DỪNG
SET @scope_id = (SELECT id FROM internal_business_scopes WHERE code = @scope_code AND status = 1);
SET @ok = IF(@scope_id IS NOT NULL AND @nguoi_chay IS NOT NULL AND EXISTS (SELECT 1 FROM employees WHERE id = @nguoi_chay), 1, 0);
SELECT @scope_id AS scope_id_khong_duoc_null, @ok AS ok_PHAI_1;
SELECT company_id, COUNT(*) AS lien_ket_truoc FROM product_business_catalogs WHERE company_id IN ({cids}) GROUP BY company_id;
SELECT id, name FROM companies WHERE id IN ({cids}) ORDER BY id;   -- phải ra đủ 4 công ty Tân Phát

-- C1. Bảng phụ + mốc lui
DROP TABLE IF EXISTS zz_golive2010_catalog;
CREATE TABLE zz_golive2010_catalog (product_code VARCHAR(255) NULL, chuong VARCHAR(64) NOT NULL, muc VARCHAR(64) NOT NULL,
  tieu_muc VARCHAR(64) NOT NULL, KEY (product_code)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS zz_golive2010_catalog_moc AS
  SELECT (SELECT IFNULL(MAX(id),0) FROM chapters) AS chapter_max, (SELECT IFNULL(MAX(id),0) FROM job_groups) AS group_max,
         (SELECT IFNULL(MAX(id),0) FROM job_clusters) AS cluster_max, (SELECT IFNULL(MAX(id),0) FROM product_business_catalogs) AS pbc_max,
         (SELECT IFNULL(MAX(id),0) FROM catalog_histories) AS history_max;
"""]
data=[(c,m,t,None) for c,m,t in tm]+[(b,c,d,a) for a,b,c,d in links]
for i in range(0,len(data),500):
    L.append("INSERT INTO zz_golive2010_catalog (chuong, muc, tieu_muc, product_code) VALUES\n"+",\n".join(f"({q(c)},{q(m)},{q(t)},{q(a) if a else 'NULL'})" for c,m,t,a in data[i:i+500])+";")
L.append(f"""SELECT COUNT(DISTINCT chuong) AS chuong_{nch}, COUNT(DISTINCT chuong, muc) AS muc_{nmu}, COUNT(DISTINCT chuong, muc, tieu_muc) AS tieu_muc_{len(tm)},
       SUM(product_code IS NOT NULL) AS dong_hang_{len(links)} FROM zz_golive2010_catalog;

-- C2. Chương
SET @m = (SELECT IFNULL(MAX(id),0) FROM chapters);
INSERT INTO chapters (name, status, internal_business_scope_id, created_by, updated_by, created_at, updated_at)
SELECT DISTINCT z.chuong, 1, @scope_id, @nguoi_chay, @nguoi_chay, NOW(), NOW() FROM zz_golive2010_catalog z
WHERE @ok = 1 AND NOT EXISTS (SELECT 1 FROM chapters c WHERE c.internal_business_scope_id = @scope_id AND c.name = z.chuong);
INSERT INTO catalog_histories (table_name, table_id, action, old_value, new_value, note, changed_by, changed_at, created_at, updated_at)
SELECT 'chapters', c.id, 'create', NULL, JSON_OBJECT('name', c.name, 'internal_business_scope_id', s.name, 'status', 'Hoạt động'),
       NULL, @nguoi_chay, NOW(), NOW(), NOW()
FROM chapters c JOIN internal_business_scopes s ON s.id = c.internal_business_scope_id WHERE c.id > @m;

-- C3. Mục
SET @m = (SELECT IFNULL(MAX(id),0) FROM job_groups);
INSERT INTO job_groups (name, status, chapter_id, created_by, updated_by, created_at, updated_at)
SELECT DISTINCT z.muc, 1, c.id, @nguoi_chay, @nguoi_chay, NOW(), NOW() FROM zz_golive2010_catalog z
JOIN chapters c ON c.internal_business_scope_id = @scope_id AND c.name = z.chuong
WHERE @ok = 1 AND NOT EXISTS (SELECT 1 FROM job_groups g WHERE g.chapter_id = c.id AND g.name = z.muc);
INSERT INTO catalog_histories (table_name, table_id, action, old_value, new_value, note, changed_by, changed_at, created_at, updated_at)
SELECT 'job_groups', g.id, 'create', NULL, JSON_OBJECT('name', g.name, 'chapter_id', c.name, 'status', 'Hoạt động'),
       NULL, @nguoi_chay, NOW(), NOW(), NOW()
FROM job_groups g JOIN chapters c ON c.id = g.chapter_id WHERE g.id > @m;

-- C4. Tiểu mục
SET @m = (SELECT IFNULL(MAX(id),0) FROM job_clusters);
INSERT INTO job_clusters (name, status, group_id, created_by, updated_by, created_at, updated_at)
SELECT DISTINCT z.tieu_muc, 1, g.id, @nguoi_chay, @nguoi_chay, NOW(), NOW() FROM zz_golive2010_catalog z
JOIN chapters c ON c.internal_business_scope_id = @scope_id AND c.name = z.chuong
JOIN job_groups g ON g.chapter_id = c.id AND g.name = z.muc
WHERE @ok = 1 AND NOT EXISTS (SELECT 1 FROM job_clusters k WHERE k.group_id = g.id AND k.name = z.tieu_muc);
INSERT INTO catalog_histories (table_name, table_id, action, old_value, new_value, note, changed_by, changed_at, created_at, updated_at)
SELECT 'job_clusters', k.id, 'create', NULL, JSON_OBJECT('name', k.name, 'group_id', g.name, 'status', 'Hoạt động'),
       NULL, @nguoi_chay, NOW(), NOW(), NOW()
FROM job_clusters k JOIN job_groups g ON g.id = k.group_id WHERE k.id > @m;

-- Kiểm cây: đường trong file không ra Tiểu mục ĐANG HOẠT ĐỘNG (rỗng = đúng; có dòng = nhánh có sẵn đang KHOÁ ⇒ báo nghiệp vụ)
SELECT DISTINCT z.chuong, z.muc, z.tieu_muc FROM zz_golive2010_catalog z
LEFT JOIN chapters c ON c.internal_business_scope_id = @scope_id AND c.name = z.chuong AND c.status = 1
LEFT JOIN job_groups g ON g.chapter_id = c.id AND g.name = z.muc AND g.status = 1
LEFT JOIN job_clusters k ON k.group_id = g.id AND k.name = z.tieu_muc AND k.status = 1
WHERE k.id IS NULL;

-- C5. Mã hàng KHÔNG gắn được + lý do (gửi nghiệp vụ)
SELECT z.product_code, cty.id AS company_id,
  CASE WHEN p.id IS NULL THEN 'không có mã trên DB / đã xoá'
       WHEN pcs.status IS NULL THEN 'không có dòng tại công ty'
       WHEN pcs.status IN (6,7,8) THEN 'hàng tạm'
       WHEN pcs.status = 4 THEN 'ngừng kinh doanh' END AS ly_do
FROM (SELECT DISTINCT product_code FROM zz_golive2010_catalog WHERE product_code IS NOT NULL) z
CROSS JOIN companies cty
LEFT JOIN products p ON p.code = z.product_code AND p.status <> 0
LEFT JOIN product_company_coefficients pcs ON pcs.product_id = p.id AND pcs.company_id = cty.id
WHERE cty.id IN ({cids}) AND (p.id IS NULL OR pcs.status IS NULL OR pcs.status IN (4,6,7,8))
ORDER BY z.product_code, cty.id;

-- C6. Gắn hàng ↔ Tiểu mục
INSERT IGNORE INTO product_business_catalogs (product_id, company_id, job_cluster_id, created_by, updated_by, created_at, updated_at)
SELECT DISTINCT p.id, pcs.company_id, k.id, @nguoi_chay, @nguoi_chay, NOW(), NOW()
FROM zz_golive2010_catalog z
JOIN products p ON p.code = z.product_code AND p.status <> 0
JOIN product_company_coefficients pcs ON pcs.product_id = p.id AND pcs.company_id IN ({cids}) AND pcs.status NOT IN (4,6,7,8)
JOIN chapters c ON c.internal_business_scope_id = @scope_id AND c.name = z.chuong AND c.status = 1
JOIN job_groups g ON g.chapter_id = c.id AND g.name = z.muc AND g.status = 1
JOIN job_clusters k ON k.group_id = g.id AND k.name = z.tieu_muc AND k.status = 1
WHERE @ok = 1;

SELECT (SELECT COUNT(*) FROM chapters WHERE internal_business_scope_id = @scope_id) AS chuong_linh_vuc;
SELECT company_id, COUNT(*) AS lien_ket_sau, COUNT(DISTINCT product_id) AS so_hang FROM product_business_catalogs
WHERE company_id IN ({cids}) GROUP BY company_id;

-- =====================================================================================
-- LUI (chỉ khi cần) — xoá đúng những gì file này tạo (theo mốc id lúc chạy LẦN ĐẦU):
-- DELETE FROM product_business_catalogs WHERE id > (SELECT pbc_max FROM zz_golive2010_catalog_moc);
-- DELETE FROM catalog_histories WHERE id > (SELECT history_max FROM zz_golive2010_catalog_moc)
--   AND table_name IN ('chapters','job_groups','job_clusters');
-- DELETE FROM job_clusters WHERE id > (SELECT cluster_max FROM zz_golive2010_catalog_moc);
-- DELETE FROM job_groups WHERE id > (SELECT group_max FROM zz_golive2010_catalog_moc);
-- DELETE FROM chapters WHERE id > (SELECT chapter_max FROM zz_golive2010_catalog_moc);
-- (Chỉ đúng khi CHƯA ai tạo tay Chương/Mục/Tiểu mục/catalog sau lúc chạy.)
-- DỌN sau nghiệm thu: DROP TABLE zz_golive2010_catalog, zz_golive2010_catalog_moc;
-- =====================================================================================
""")
os.makedirs(out,exist_ok=True)
open(os.path.join(out,'catalog_dich_vu_o_to_2010.sql'),'w',encoding='utf-8').write("\n".join(L))
print('Chương',nch,'Mục',nmu,'Tiểu mục',len(tm),'| dòng hàng',len(links))

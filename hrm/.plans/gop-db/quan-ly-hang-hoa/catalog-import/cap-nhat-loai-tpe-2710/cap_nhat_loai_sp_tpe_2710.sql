-- =====================================================================================
-- Cập nhật phân loại 4 cấp cho hàng hoá công ty TPE (đợt 27/10) — nguồn: du_lieu_hang_hoa_cong_ty_TPE_27102026.xlsx (32 mã)
-- products chỉ lưu product_type_id; 3 cấp trên (Nhóm SP → Nhóm CN → Tính chất) suy ra theo cây
-- product_types → product_families → product_function_groups → product_natures.
-- Khớp: products.code = "Mã hàng", product_types.name = "Loại sản phẩm".
-- Mã hàng / Loại SP không có trên DB, hoặc Loại trống ⇒ BỎ QUA, liệt kê ở bước B4.
-- Chỉ ghi dòng có product_type_id khác giá trị mới. Điểm lui: bảng zz_tpe2710_products_bak.
-- =====================================================================================
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ---------- B1. Dữ liệu file ----------
DROP TEMPORARY TABLE IF EXISTS tmp_tpe2710_map;
CREATE TEMPORARY TABLE tmp_tpe2710_map (
  dong_excel INT NOT NULL,
  product_code VARCHAR(255) NOT NULL,
  loai_name VARCHAR(255) NOT NULL,
  PRIMARY KEY (product_code)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO tmp_tpe2710_map (dong_excel, product_code, loai_name) VALUES
(4,'LAPA-35626','Máy nén khí trục vít'),
(5,'LAPA-35740','Máy nén khí trục vít'),
(6,'LAPA-AMDLH43','Máy sấy khí nén'),
(7,'LAPA-99308A','Lọc khí nén'),
(8,'LAPA-99208A','Lọc khí nén'),
(9,'LAPA-99404','Lọc tách nước và dầu khí nén'),
(10,'LAPA-99104','Lọc tách nước và dầu khí nén'),
(11,'LAPA-356381:02','Máy nén khí trục vít'),
(12,'LAPA-94413:01','Máy sấy khí nén'),
(13,'LAPA-35638:01','Máy nén khí trục vít'),
(14,'LAPA-94704','Máy sấy khí nén'),
(15,'LAPA-94705','Máy sấy khí nén'),
(16,'LAPA-380201IE3','Máy nén khí trục vít'),
(17,'LAPA-35766','Máy nén khí trục vít'),
(18,'LAPA-MXP300012','Máy nén khí trục vít'),
(19,'LAPA-MXH300010INVERTER','Máy nén khí trục vít'),
(20,'LAPA-91023','PTLK máy nén khí'),
(21,'LAPA-91021','PTLK máy nén khí'),
(22,'LAPA-94412','Máy sấy khí nén'),
(23,'LAPA-37114','Máy nén khí trục vít'),
(24,'LAPA-37112','Máy nén khí trục vít'),
(25,'LAPA-99204','Lọc tách nước và dầu khí nén'),
(26,'LAPA-380201:02','Máy nén khí trục vít'),
(27,'LAPA-94413','Máy sấy khí nén'),
(28,'LAPA-371141','Máy nén khí trục vít'),
(29,'LAPA-37113','Máy nén khí trục vít'),
(30,'LAPA-38020','Máy nén khí trục vít'),
(31,'LAPA-38017','Máy nén khí trục vít'),
(32,'LAPA-37025','Máy nén khí trục vít'),
(33,'LAPA-37027','Máy nén khí trục vít'),
(34,'LAPA-89012','Máy nén khí piston'),
(35,'LAPA-53320','Máy nén khí trục vít');

-- ---------- B2. Sao lưu + kiểm trước ----------
CREATE TABLE IF NOT EXISTS zz_tpe2710_products_bak AS
  SELECT p.id, p.code, p.product_type_id, p.updated_at
  FROM products p JOIN tmp_tpe2710_map m ON m.product_code = p.code;

SELECT COUNT(*) AS se_cap_nhat
FROM products p
JOIN tmp_tpe2710_map m ON m.product_code = p.code
JOIN product_types t ON t.name = m.loai_name
WHERE m.loai_name <> '' AND NOT (p.product_type_id <=> t.id);

-- ---------- B3. Cập nhật ----------
UPDATE products p
JOIN tmp_tpe2710_map m ON m.product_code = p.code
JOIN product_types t ON t.name = m.loai_name
SET p.product_type_id = t.id, p.updated_at = NOW()
WHERE m.loai_name <> '' AND NOT (p.product_type_id <=> t.id);

SELECT ROW_COUNT() AS da_cap_nhat;

-- ---------- B4. Danh sách BỎ QUA ----------
SELECT m.dong_excel, m.product_code, m.loai_name,
       CASE
         WHEN m.loai_name = ''                 THEN 'Loại sản phẩm trống trong file'
         WHEN NOT EXISTS (SELECT 1 FROM products p WHERE p.code = m.product_code)
              AND t.id IS NULL                 THEN 'Mã hàng + Loại SP chưa có trên DB'
         WHEN NOT EXISTS (SELECT 1 FROM products p WHERE p.code = m.product_code)
                                               THEN 'Mã hàng chưa có trên DB'
         ELSE 'Loại SP chưa có trên DB'
       END AS ly_do
FROM tmp_tpe2710_map m
LEFT JOIN product_types t ON t.name = m.loai_name AND m.loai_name <> ''
WHERE m.loai_name = ''
   OR t.id IS NULL
   OR NOT EXISTS (SELECT 1 FROM products p WHERE p.code = m.product_code)
ORDER BY m.dong_excel;

-- ---------- B5. Kiểm sau: 4 cấp theo Loại trong file ----------
SELECT m.loai_name, t.code AS loai_code, f.name AS nhom_sp, g.name AS nhom_cn, n.name AS tinh_chat,
       COUNT(*) AS so_hang, SUM(p.product_type_id <=> t.id) AS da_dung_loai
FROM tmp_tpe2710_map m
JOIN products p ON p.code = m.product_code
JOIN product_types t ON t.name = m.loai_name
JOIN product_families f ON f.id = t.product_family_id
JOIN product_function_groups g ON g.id = f.product_function_group_id
JOIN product_natures n ON n.id = g.product_nature_id
GROUP BY m.loai_name, t.code, f.name, g.name, n.name
ORDER BY m.loai_name;

DROP TEMPORARY TABLE IF EXISTS tmp_tpe2710_map;

-- ---------- Rollback (chỉ khi cần) ----------
-- UPDATE products p JOIN zz_tpe2710_products_bak b ON b.id = p.id
--   SET p.product_type_id = b.product_type_id, p.updated_at = b.updated_at;
-- Nghiệm thu xong: DROP TABLE zz_tpe2710_products_bak;

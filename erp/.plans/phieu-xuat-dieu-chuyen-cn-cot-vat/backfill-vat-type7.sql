-- =============================================================================
-- task_11319 — Backfill % VAT cho phiếu xuất hàng "Xuất điều chuyển kho chi nhánh" (type = 7)
--
-- Vì sao cần: cột %VAT mới bổ sung cho type 7. Các phiếu type 7 tạo TRƯỚC bản này
-- đều có product_export_details.vat_percent = 0 (chưa bao giờ được ghi).
-- Từ bản này, màn Chi tiết + bản in của phiếu ĐÃ DUYỆT đọc VAT đã chốt trong
-- product_export_details -> phiếu cũ sẽ hiện 0 nếu không backfill.
--
-- Chạy 1 LẦN, trước/ngay sau khi deploy code task_11319.
-- Ảnh hưởng: chỉ product_export_details.vat_percent của phiếu type = 7.
-- =============================================================================

-- 0) BACKUP trước khi chạy (bắt buộc, để còn đường lùi)
CREATE TABLE product_export_details_vat_bak_11319 AS
SELECT d.id, d.vat_percent
FROM product_export_details d
JOIN product_exports p ON p.id = d.parent_id
WHERE p.type = 7;

-- 1) KIỂM TRA trước: xem sẽ đụng bao nhiêu dòng, giá trị cũ -> mới
SELECT COUNT(*) AS so_dong_se_update
FROM product_export_details d
JOIN product_exports p  ON p.id  = d.parent_id
JOIN products         pr ON pr.id = d.product_id
WHERE p.type = 7
  AND d.vat_percent <=> 0;

SELECT d.id AS detail_id, p.code AS phieu, p.status, pr.code AS ma_hang,
       d.vat_percent AS vat_cu, pr.vat_percent AS vat_moi
FROM product_export_details d
JOIN product_exports p  ON p.id  = d.parent_id
JOIN products         pr ON pr.id = d.product_id
WHERE p.type = 7
ORDER BY p.id DESC
LIMIT 50;

-- 2) BACKFILL
UPDATE product_export_details d
JOIN product_exports p  ON p.id  = d.parent_id
JOIN products         pr ON pr.id = d.product_id
SET d.vat_percent = pr.vat_percent
WHERE p.type = 7
  AND d.vat_percent <=> 0;   -- chỉ vá dòng chưa có VAT, không đè dòng đã chốt đúng

-- 3) KIỂM TRA sau: không còn dòng nào lệch danh mục
SELECT COUNT(*) AS con_lai_vat_0
FROM product_export_details d
JOIN product_exports p ON p.id = d.parent_id
WHERE p.type = 7 AND d.vat_percent <=> 0;

-- 4) ROLLBACK nếu cần (chạy khi muốn trả về như cũ)
-- UPDATE product_export_details d
-- JOIN product_export_details_vat_bak_11319 b ON b.id = d.id
-- SET d.vat_percent = b.vat_percent;

-- 5) Dọn bảng backup sau khi đã chắc chắn OK
-- DROP TABLE product_export_details_vat_bak_11319;

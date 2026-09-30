-- Backfill cancel_type cho cac dong da huy TU TRUOC (Redmine #11474)
-- Quy tac suy luan (user chot 16/09/2026):
--   dong da huy ma CUNG dong nhu cau do van con chi tiet HD/PLBS khac dang hieu luc
--   => nguoi dung da "Huy dat lai" (2); nguoc lai => "Huy khong dat" (1).

-- ============ LUONG TRONG NUOC (gom ca PLBS, dung chung bang) ============
-- 1a. Dong dat cho khach: doi chieu theo dong nhu cau (inland_order_request_new_detail_id)
UPDATE inland_buy_contract_new_product_details d
SET d.cancel_type = 2
WHERE d.status = 0 AND d.cancel_type IS NULL
  AND d.inland_order_request_new_detail_id IS NOT NULL
  AND EXISTS (
      SELECT 1 FROM (SELECT * FROM inland_buy_contract_new_product_details) x
      WHERE x.inland_order_request_new_detail_id = d.inland_order_request_new_detail_id
        AND x.id <> d.id AND x.status = 1
  );

-- 1b. Dong ton kho (khong co dong nhu cau): doi chieu theo phieu dat hang + hang hoa
UPDATE inland_buy_contract_new_product_details d
SET d.cancel_type = 2
WHERE d.status = 0 AND d.cancel_type IS NULL
  AND d.inland_order_request_new_detail_id IS NULL
  AND d.inland_order_request_new_id IS NOT NULL
  AND EXISTS (
      SELECT 1 FROM (SELECT * FROM inland_buy_contract_new_product_details) x
      WHERE x.inland_order_request_new_id = d.inland_order_request_new_id
        AND x.product_id = d.product_id
        AND x.id <> d.id AND x.status = 1
  );

-- 1c. Con lai la huy han
UPDATE inland_buy_contract_new_product_details
SET cancel_type = 1
WHERE status = 0 AND cancel_type IS NULL;

-- ============ LUONG NHAP KHAU ============
UPDATE buy_contract_product_detail2 d
SET d.cancel_type = 2
WHERE d.status = 0 AND d.cancel_type IS NULL
  AND d.order_request_detail2_id IS NOT NULL
  AND EXISTS (
      SELECT 1 FROM (SELECT * FROM buy_contract_product_detail2) x
      WHERE x.order_request_detail2_id = d.order_request_detail2_id
        AND x.id <> d.id AND x.status = 1
  );

UPDATE buy_contract_product_detail2 d
SET d.cancel_type = 2
WHERE d.status = 0 AND d.cancel_type IS NULL
  AND d.order_request_detail2_id IS NULL
  AND d.order_request2_id IS NOT NULL
  AND EXISTS (
      SELECT 1 FROM (SELECT * FROM buy_contract_product_detail2) x
      WHERE x.order_request2_id = d.order_request2_id
        AND x.product_id = d.product_id
        AND x.id <> d.id AND x.status = 1
  );

UPDATE buy_contract_product_detail2
SET cancel_type = 1
WHERE status = 0 AND cancel_type IS NULL;

-- ============ KIEM TRA ============
SELECT 'Trong nuoc' AS luong, cancel_type, COUNT(*) AS so_dong
FROM inland_buy_contract_new_product_details WHERE status = 0 GROUP BY cancel_type
UNION ALL
SELECT 'Nhap khau', cancel_type, COUNT(*)
FROM buy_contract_product_detail2 WHERE status = 0 GROUP BY cancel_type;

-- =====================================================================
-- FIX DỮ LIỆU PROD (erp_new): xóa dòng Có (type=2) THỪA của báo có (PBC)
-- bị trùng do import (StoreIncomeReportJob) — 69 báo có 1-detail nhưng >=2 Có.
-- Giữ dòng Có id NHỎ NHẤT mỗi voucher; xóa các dòng Có còn lại + ref của chúng.
-- KHÔNG đụng dòng Nợ (type=1).
--
-- ⚠️ CHẠY TRÊN PROD — BẮT BUỘC:
--   1. Backup DB (hoặc ít nhất 2 bảng dưới) TRƯỚC khi chạy.
--   2. Kế toán xác nhận các dòng Có thừa KHÔNG bị dùng để cấn trừ công nợ ở đâu.
--   3. Chạy từng STEP, đối chiếu số lượng, rồi mới COMMIT.
-- Ngày soạn: 2026-06-30
-- =====================================================================

-- ---------------------------------------------------------------------
-- STEP 1: BACKUP — tạo bảng lưu đúng 69 dòng Có thừa sẽ xóa (đồng thời là nguồn id)
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS bak_dup_co_ad_20260630;
CREATE TABLE bak_dup_co_ad_20260630 AS
SELECT a.*
FROM account_details a
WHERE a.invoiceable_type LIKE '%BillIncomeReport%' AND a.type = 2
  AND a.invoiceable_id IN (
     SELECT invoiceable_id FROM (
       SELECT ad.invoiceable_id, SUM(ad.type = 2) n_co,
              (SELECT COUNT(*) FROM bill_income_report_details d WHERE d.parent_id = ad.invoiceable_id) n_detail
       FROM account_details ad
       WHERE ad.invoiceable_type LIKE '%BillIncomeReport%'
       GROUP BY ad.invoiceable_id
       HAVING n_detail = 1 AND n_co >= 2
     ) x
  )
  AND a.id NOT IN (
     SELECT * FROM (
       SELECT MIN(id) FROM account_details
       WHERE invoiceable_type LIKE '%BillIncomeReport%' AND type = 2
       GROUP BY invoiceable_id
     ) y
  );

-- Kỳ vọng: 69 dòng
SELECT COUNT(*) AS so_co_thua_backup FROM bak_dup_co_ad_20260630;

-- ---------------------------------------------------------------------
-- STEP 2: BACKUP refs của các dòng Có thừa
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS bak_dup_co_ref_20260630;
CREATE TABLE bak_dup_co_ref_20260630 AS
SELECT r.*
FROM account_detail_refs r
WHERE r.account_detail_id IN (SELECT id FROM bak_dup_co_ad_20260630);

-- Kỳ vọng: 69 dòng
SELECT COUNT(*) AS so_ref_thua_backup FROM bak_dup_co_ref_20260630;

-- ---------------------------------------------------------------------
-- STEP 3: PREVIEW — xem lại đúng các dòng sắp xóa trước khi DELETE
-- ---------------------------------------------------------------------
SELECT id, invoiceable_code, type, account_id, money_value_exchange, created_at
FROM bak_dup_co_ad_20260630
ORDER BY invoiceable_code;

-- ---------------------------------------------------------------------
-- STEP 4: DELETE (transaction) — chạy sau khi đã đối chiếu STEP 1-3
-- ---------------------------------------------------------------------
START TRANSACTION;

DELETE FROM account_detail_refs
WHERE account_detail_id IN (SELECT id FROM bak_dup_co_ad_20260630);

DELETE FROM account_details
WHERE id IN (SELECT id FROM bak_dup_co_ad_20260630);

-- Kiểm tra: phải = 0 voucher 1-detail còn >=2 Có
SELECT COUNT(*) AS con_trung_sau_xoa FROM (
  SELECT ad.invoiceable_id, SUM(ad.type = 2) n_co,
         (SELECT COUNT(*) FROM bill_income_report_details d WHERE d.parent_id = ad.invoiceable_id) n_detail
  FROM account_details ad
  WHERE ad.invoiceable_type LIKE '%BillIncomeReport%'
  GROUP BY ad.invoiceable_id
  HAVING n_detail = 1 AND n_co >= 2
) t;

-- Nếu con_trung_sau_xoa = 0 và số dòng xóa khớp (69 + 69) -> COMMIT; ngược lại -> ROLLBACK;
-- COMMIT;
-- ROLLBACK;

-- ---------------------------------------------------------------------
-- ROLLBACK DỮ LIỆU (nếu cần khôi phục sau khi đã COMMIT):
--   INSERT INTO account_details      SELECT * FROM bak_dup_co_ad_20260630;
--   INSERT INTO account_detail_refs  SELECT * FROM bak_dup_co_ref_20260630;
-- ---------------------------------------------------------------------

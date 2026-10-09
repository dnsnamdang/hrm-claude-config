-- =====================================================================
-- Fix ngày hạch toán account_details của phiếu quyết toán năng suất quý
-- (BillProductivitySettlementQuarter) đã hạch toán SAI ngày trên prod.
--
-- Nguyên nhân: trước khi vá code, account_details lấy ngày = updated_at
-- (ngày tạo, vd 2026-07-02) thay vì date_accounting trên phiếu (2026-06-30).
--
-- Phạm vi (prod erp_new, xác minh 2026-07-02): 52 dòng / 4 phiếu (id 1-4).
--   invoiceable_date_accounting: 2026-07-02  ->  date_accounting phiếu (2026-06-30)
--
-- CHẠY TRÊN PRODUCTION — cần backup + duyệt trước.
-- =====================================================================

-- (1) KIỂM TRA trước khi chạy — số dòng sẽ đổi (kỳ vọng 52):
SELECT COUNT(*) AS so_dong_se_doi
FROM account_details ad
JOIN bill_productivity_settlement_quarters b ON ad.invoiceable_id = b.id
WHERE ad.invoiceable_type = 'App\\Model\\Accounting\\BillProductivitySettlementQuarter'
  AND DATE(ad.invoiceable_date_accounting) <> DATE(b.date_accounting);

-- (2) BACKUP giá trị hiện tại (chạy và LƯU KẾT QUẢ trước khi UPDATE để rollback được):
SELECT ad.id, ad.invoiceable_id, ad.invoiceable_date_accounting AS old_value, b.date_accounting AS new_value
FROM account_details ad
JOIN bill_productivity_settlement_quarters b ON ad.invoiceable_id = b.id
WHERE ad.invoiceable_type = 'App\\Model\\Accounting\\BillProductivitySettlementQuarter'
  AND DATE(ad.invoiceable_date_accounting) <> DATE(b.date_accounting);

-- (3) UPDATE — chạy trong transaction:
START TRANSACTION;

-- Dùng DATE(b.date_accounting) để ép giờ 00:00:00 (tránh 0000-00-00 / lệch giờ).
UPDATE account_details ad
JOIN bill_productivity_settlement_quarters b ON ad.invoiceable_id = b.id
SET ad.invoiceable_date_accounting = DATE(b.date_accounting)
WHERE ad.invoiceable_type = 'App\\Model\\Accounting\\BillProductivitySettlementQuarter'
  AND DATE(ad.invoiceable_date_accounting) <> DATE(b.date_accounting);

-- (4) KIỂM TRA sau UPDATE (trước COMMIT) — kỳ vọng 0 dòng lệch:
SELECT COUNT(*) AS con_lech
FROM account_details ad
JOIN bill_productivity_settlement_quarters b ON ad.invoiceable_id = b.id
WHERE ad.invoiceable_type = 'App\\Model\\Accounting\\BillProductivitySettlementQuarter'
  AND DATE(ad.invoiceable_date_accounting) <> DATE(b.date_accounting);

-- Nếu đúng (con_lech = 0):
-- COMMIT;
-- Nếu sai:
-- ROLLBACK;

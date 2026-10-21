-- =====================================================================================
-- Đóng YCHG CHÉO công ty còn dở (company_id <> send_company_id) — go-live 20/10/2026, user chốt "đóng bằng lệnh khi deploy".
-- Chạy SAU `php artisan price-asking:backfill-groups` (bước 8 runbook) và TRƯỚC/SAU close-stale đều được.
-- Làm Y HỆT `price-asking:close-stale` (PriceAskingStaleCloser) nhưng lọc theo phiếu chéo thay vì theo ngày:
--   nhóm còn mở (5 Chờ XNK · 1 Chờ lập YCTG · 7 Đang tính giá) ⇒ 6 Huỷ duyệt, lý do "Chuyển hệ thống", log type "Huỷ duyệt";
--   phiếu có MỌI nhóm đã đóng ⇒ 4 (nếu có nhóm Đã tính giá) / 6 Huỷ duyệt. YCTG / PTG nháp đi kèm GIỮ NGUYÊN.
-- Người lập tạo lại phiếu trên HRM nếu còn cần. Chạy lại = 0 dòng.
-- =====================================================================================
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET @nguoi_chay = 13;   -- 13 = DNS Admin (user chốt 20/10). ⚠️ BẮT BUỘC: employees.id người chạy (như --by của close-stale). Để NULL ⇒ không ghi gì.

SET @ok = IF(@nguoi_chay IS NOT NULL AND EXISTS (SELECT 1 FROM employees WHERE id = @nguoi_chay), 1, 0);
SELECT @ok AS ok_PHAI_1;

-- Danh sách phiếu chéo dở (gửi nghiệp vụ) — bản sao prod 20/10: 36
SELECT a.id, a.code, a.status, a.company_id, a.send_company_id, a.created_by, a.created_at
FROM price_asking_requests a
WHERE a.status IN (1,2,5,7,10) AND a.send_company_id IS NOT NULL AND a.company_id <> a.send_company_id ORDER BY a.id;

DROP TABLE IF EXISTS zz_golive2010_cheo_nhom;
CREATE TABLE zz_golive2010_cheo_nhom AS
  SELECT g.id, g.status, g.close_reason, g.closed_by, g.closed_at, g.updated_by, g.updated_at, g.price_asking_request_id
  FROM price_asking_request_groups g JOIN price_asking_requests a ON a.id = g.price_asking_request_id
  WHERE @ok = 1 AND a.send_company_id IS NOT NULL AND a.company_id <> a.send_company_id AND g.status IN (5,1,7);
CREATE TABLE IF NOT EXISTS zz_golive2010_cheo_phieu_bak AS
  SELECT a.id, a.status, a.updated_at FROM price_asking_requests a WHERE a.id IN (SELECT price_asking_request_id FROM zz_golive2010_cheo_nhom);
SELECT COUNT(*) AS nhom_se_dong, COUNT(DISTINCT price_asking_request_id) AS phieu FROM zz_golive2010_cheo_nhom;

UPDATE price_asking_request_groups g JOIN zz_golive2010_cheo_nhom z ON z.id = g.id
SET g.status = 6, g.close_reason = 'Chuyển hệ thống', g.closed_by = @nguoi_chay, g.closed_at = NOW(),
    g.updated_by = @nguoi_chay, g.updated_at = NOW();
INSERT INTO price_asking_request_approve_histories (price_asking_request_id, group_id, created_by, note, type, created_at, updated_at)
SELECT z.price_asking_request_id, z.id, @nguoi_chay, 'Chuyển hệ thống', 'Huỷ duyệt', NOW(), NOW() FROM zz_golive2010_cheo_nhom z;

-- Đầu phiếu: chỉ khi MỌI nhóm của phiếu đã đóng (4 · 9 · 6); NULL / còn mở ⇒ giữ nguyên
UPDATE price_asking_requests a
JOIN (SELECT g.price_asking_request_id AS rid, MAX(g.status = 4) AS co_gia,
             SUM(g.status IS NULL OR g.status NOT IN (4,9,6)) AS con_mo
      FROM price_asking_request_groups g
      WHERE g.price_asking_request_id IN (SELECT DISTINCT price_asking_request_id FROM zz_golive2010_cheo_nhom)
      GROUP BY g.price_asking_request_id) s ON s.rid = a.id
SET a.status = IF(s.co_gia = 1, 4, 6), a.updated_at = NOW()
WHERE s.con_mo = 0;

-- Kiểm: phiếu chéo còn "đang hỏi giá" (1 · 5 · 7 · 10). Còn ⇒ phiếu chưa backfill nhóm / nhóm NULL — báo dev. Phiếu 2 (Chờ PTKD) không đụng (như close-stale).
SELECT a.status, COUNT(*) AS n FROM price_asking_requests a
WHERE a.send_company_id IS NOT NULL AND a.company_id <> a.send_company_id AND a.status IN (1,2,5,7,10) GROUP BY a.status;

-- LUI: UPDATE price_asking_request_groups g JOIN zz_golive2010_cheo_nhom z ON z.id = g.id SET g.status = z.status, g.close_reason = z.close_reason,
--        g.closed_by = z.closed_by, g.closed_at = z.closed_at, g.updated_by = z.updated_by, g.updated_at = z.updated_at;
--      UPDATE price_asking_requests a JOIN zz_golive2010_cheo_phieu_bak b ON b.id = a.id SET a.status = b.status, a.updated_at = b.updated_at;
--      DELETE FROM price_asking_request_approve_histories WHERE note = 'Chuyển hệ thống' AND group_id IN (SELECT id FROM zz_golive2010_cheo_nhom);
-- DỌN: DROP TABLE zz_golive2010_cheo_nhom, zz_golive2010_cheo_phieu_bak;

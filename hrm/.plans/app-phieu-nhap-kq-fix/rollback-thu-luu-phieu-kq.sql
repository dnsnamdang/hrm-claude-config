-- =============================================================================
-- THỬ NÚT "LƯU VÀ GỬI DUYỆT" TRÊN DỮ LIỆU THẬT — CÁCH QUAY VỀ TRẠNG THÁI CŨ
-- Phiếu giao việc thử: TPE.PGV.2026014961  (wr_assign_tasks.id = 14961)
-- Chạy trên DB của ERP. Đổi @TASK_ID nếu thử phiếu khác.
-- =============================================================================
SET @TASK_ID = 14961;

-- -----------------------------------------------------------------------------
-- BƯỚC 1 — CHẠY TRƯỚC KHI BẤM. Bắt buộc.
--
-- Lưu phiếu KQ không chỉ TẠO bản ghi mới, nó còn GHI ĐÈ dữ liệu sẵn có của phiếu
-- giao việc (trạng thái phiếu, % hoàn thành và cờ hoàn thành của từng hạng mục).
-- Phần ghi đè KHÔNG thể khôi phục bằng cách xoá — phải có bản chụp trước.
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS bak_task;
DROP TABLE IF EXISTS bak_items;
DROP TABLE IF EXISTS bak_services;
DROP TABLE IF EXISTS bak_timesheets;

CREATE TABLE bak_task      AS SELECT id, status FROM wr_assign_tasks WHERE id = @TASK_ID;
CREATE TABLE bak_items     AS SELECT id, finish_percent, is_completed
                              FROM wr_assign_task_product_items  WHERE wr_assign_task_id = @TASK_ID;
CREATE TABLE bak_services  AS SELECT id, finish_percent, is_completed
                              FROM wr_assign_task_product_services WHERE wr_assign_task_id = @TASK_ID;
CREATE TABLE bak_timesheets AS SELECT id, checkin_actual, checkout_actual, time_actual
                              FROM wr_assign_task_timesheets WHERE wr_assign_task_id = @TASK_ID;

-- Kiểm tra đã chụp được (phải ra 1 dòng cho bak_task):
SELECT (SELECT COUNT(*) FROM bak_task)       AS task,
       (SELECT COUNT(*) FROM bak_items)      AS items,
       (SELECT COUNT(*) FROM bak_services)   AS services,
       (SELECT COUNT(*) FROM bak_timesheets) AS timesheets;

-- >>> Giờ mới bấm "Lưu và Gửi duyệt" trên app <<<

-- -----------------------------------------------------------------------------
-- BƯỚC 2 — SAU KHI BẤM. Xem nó đã tạo ra cái gì (chỉ đọc).
-- -----------------------------------------------------------------------------
SELECT id, code, status, created_by, created_at
FROM wr_import_results
WHERE wr_assign_task_id = @TASK_ID
ORDER BY id DESC;

-- Lấy id phiếu vừa tạo rồi điền vào đây:
SET @KQ_ID = 0;   -- <<< ĐIỀN id phiếu KQ vừa tạo. Để 0 thì các lệnh dưới không xoá gì.

-- -----------------------------------------------------------------------------
-- BƯỚC 3 — HOÀN TÁC. Chạy trong 1 transaction, xoá con trước cha.
-- -----------------------------------------------------------------------------
START TRANSACTION;

-- 3a. Bảng cháu (nối qua wr_import_result_products)
DELETE s FROM wr_import_result_product_services s
  JOIN wr_import_result_products p ON p.id = s.wr_import_result_product_id
  WHERE p.wr_import_result_id = @KQ_ID;
DELETE i FROM wr_import_result_product_items i
  JOIN wr_import_result_products p ON p.id = i.wr_import_result_product_id
  WHERE p.wr_import_result_id = @KQ_ID;
DELETE e FROM wr_import_result_product_device_errors e
  JOIN wr_import_result_products p ON p.id = e.wr_import_result_product_id
  WHERE p.wr_import_result_id = @KQ_ID;

-- 3b. Bảng con trực tiếp
DELETE FROM wr_import_result_products              WHERE wr_import_result_id = @KQ_ID;
DELETE FROM wr_import_result_items                 WHERE wr_import_result_id = @KQ_ID;
DELETE FROM wr_import_result_services              WHERE wr_import_result_id = @KQ_ID;
DELETE FROM wr_import_result_other_services        WHERE wr_import_result_id = @KQ_ID;
DELETE FROM wr_import_result_costs                 WHERE wr_import_result_id = @KQ_ID;
DELETE FROM wr_import_result_works                 WHERE wr_import_result_id = @KQ_ID;
DELETE FROM wr_import_result_executors             WHERE wr_import_result_id = @KQ_ID;
DELETE FROM wr_import_result_extend_products       WHERE wr_import_result_id = @KQ_ID;
DELETE FROM wr_import_result_galleries_constructions WHERE wr_import_result_id = @KQ_ID;
DELETE FROM wr_import_result_galleries_handovers   WHERE wr_import_result_id = @KQ_ID;

-- 3c. Phiếu
DELETE FROM wr_import_results WHERE id = @KQ_ID;

-- 3d. Trả lại phần BỊ GHI ĐÈ (đây là phần xoá không cứu được)
UPDATE wr_assign_tasks t JOIN bak_task b ON b.id = t.id
   SET t.status = b.status;
UPDATE wr_assign_task_product_items t JOIN bak_items b ON b.id = t.id
   SET t.finish_percent = b.finish_percent, t.is_completed = b.is_completed;
UPDATE wr_assign_task_product_services t JOIN bak_services b ON b.id = t.id
   SET t.finish_percent = b.finish_percent, t.is_completed = b.is_completed;
UPDATE wr_assign_task_timesheets t JOIN bak_timesheets b ON b.id = t.id
   SET t.checkin_actual = b.checkin_actual, t.checkout_actual = b.checkout_actual,
       t.time_actual = b.time_actual;

-- Kiểm tra rồi mới quyết định:
SELECT COUNT(*) AS con_lai FROM wr_import_results WHERE wr_assign_task_id = @TASK_ID;
SELECT status FROM wr_assign_tasks WHERE id = @TASK_ID;

-- Đúng như trước khi bấm  -> COMMIT;
-- Có gì lạ                -> ROLLBACK;

-- -----------------------------------------------------------------------------
-- Dọn bảng tạm sau khi đã COMMIT và xác nhận ổn:
-- DROP TABLE bak_task, bak_items, bak_services, bak_timesheets;
-- -----------------------------------------------------------------------------

-- GHI CHÚ
-- * Còn 2 bảng phụ nữa: wr_import_result_extend_product_services và
--   wr_import_result_extend_product_service_items. Chúng nối qua
--   wr_import_result_extend_products; nếu phiếu có phần "dịch vụ mở rộng" thì xoá
--   chúng TRƯỚC 3b. Phiếu 14961 không có extend_products nên tạm bỏ qua.
-- * Ảnh đã tải lên nằm trên S3, xoá bản ghi không xoá file. File mồ côi vô hại.
-- * Mã phiếu sinh theo id nên id đã dùng sẽ không quay lại — không ảnh hưởng nghiệp vụ.

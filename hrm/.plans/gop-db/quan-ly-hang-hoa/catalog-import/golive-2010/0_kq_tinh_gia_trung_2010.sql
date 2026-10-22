-- =====================================================================================
-- Dọn KQ tính giá TRÙNG (1 PTG > 1 KQ) — go-live 20/10/2026. Chạy TRƯỚC migration (bước 4 runbook):
-- migration 2026_10_11_100008 ép UNIQUE(price_calculate_id) sẽ DỪNG nếu còn trùng.
-- Bản sao prod 20/10: PTG-03422 (KQ 3364 sáng / 3378 chiều) · PTG-03425 (3367 / 3379), cùng người lập, giá 2 bản KHÁC nhau
-- ⇒ PTG đã sửa rồi trả KQ lần 2 ⇒ GIỮ KQ MỚI NHẤT (id lớn nhất), xoá bản cũ + dòng con (sản phẩm · giá · giá dự kiến).
-- Không chứng từ nào khác trỏ vào price_calculate_results (đã soát). Sao lưu zz_golive2010_kq_trung_* trước khi xoá.
-- =====================================================================================
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT r.price_calculate_id, c.code, GROUP_CONCAT(r.id ORDER BY r.id) AS cac_kq, MAX(r.id) AS giu
FROM price_calculate_results r JOIN price_calculates c ON c.id = r.price_calculate_id
GROUP BY r.price_calculate_id, c.code HAVING COUNT(*) > 1;            -- bản sao prod: 2 dòng

CREATE TABLE IF NOT EXISTS zz_golive2010_kq_trung AS
  SELECT r.* FROM price_calculate_results r
  JOIN (SELECT price_calculate_id, MAX(id) AS giu FROM price_calculate_results GROUP BY price_calculate_id HAVING COUNT(*) > 1) d
    ON d.price_calculate_id = r.price_calculate_id AND r.id <> d.giu;
CREATE TABLE IF NOT EXISTS zz_golive2010_kq_trung_sp AS
  SELECT p.* FROM price_calculate_result_products p WHERE p.parent_id IN (SELECT id FROM zz_golive2010_kq_trung);
CREATE TABLE IF NOT EXISTS zz_golive2010_kq_trung_gia AS
  SELECT g.* FROM price_calculate_result_product_prices g WHERE g.parent_id IN (SELECT id FROM zz_golive2010_kq_trung_sp);
CREATE TABLE IF NOT EXISTS zz_golive2010_kq_trung_du_kien AS
  SELECT e.* FROM price_calculate_result_product_expected_prices e WHERE e.parent_id IN (SELECT id FROM zz_golive2010_kq_trung_gia);
SELECT (SELECT COUNT(*) FROM zz_golive2010_kq_trung) kq, (SELECT COUNT(*) FROM zz_golive2010_kq_trung_sp) sp,
       (SELECT COUNT(*) FROM zz_golive2010_kq_trung_gia) gia, (SELECT COUNT(*) FROM zz_golive2010_kq_trung_du_kien) du_kien;

DELETE FROM price_calculate_result_product_expected_prices WHERE id IN (SELECT id FROM zz_golive2010_kq_trung_du_kien);
DELETE FROM price_calculate_result_product_prices WHERE id IN (SELECT id FROM zz_golive2010_kq_trung_gia);
DELETE FROM price_calculate_result_products WHERE id IN (SELECT id FROM zz_golive2010_kq_trung_sp);
DELETE FROM price_calculate_results WHERE id IN (SELECT id FROM zz_golive2010_kq_trung);

SELECT COUNT(*) AS ptg_con_trung_PHAI_0 FROM (SELECT price_calculate_id FROM price_calculate_results GROUP BY 1 HAVING COUNT(*) > 1) x;

-- LUI: INSERT INTO price_calculate_results SELECT * FROM zz_golive2010_kq_trung; rồi _sp → _gia → _du_kien vào 3 bảng con tương ứng.
-- DỌN sau nghiệm thu: DROP TABLE zz_golive2010_kq_trung, zz_golive2010_kq_trung_sp, zz_golive2010_kq_trung_gia, zz_golive2010_kq_trung_du_kien;

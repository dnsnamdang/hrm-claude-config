-- Chụp bộ giá (CHỈ ĐỌC) của các công ty kế thừa — chạy 1 lần TRƯỚC khi Lưu cài đặt, 1 lần SAU khi áp xong.
-- Mỗi dòng = 1 mã × ĐVT × loại giá tại công ty đích, kèm dòng cùng ĐVT + loại giá ở công ty tạo mã (nguồn) và luật kế thừa
-- TẠI THỜI ĐIỂM CHỤP (chép từ PriceInheritance::sql / factorSql — sửa luật ở đó thì sửa cả đây).
-- Chỉ hàng ĐANG KINH DOANH tại công ty đích (pcc.status = 3) do công ty KHÁC tạo — chỉ các dòng này mới đổi khi đổi cài đặt.
-- Cần 2 bảng đợt 2 (inherited_price_factors) ⇒ chạy SAU khi deploy đợt 2.
--
-- Cách chạy: xem README.md. Đổi danh sách mã công ty ở dòng SET bên dưới (ngăn bằng dấu phẩy, không dấu cách).
SET @cty = 'TPHP';

SELECT
    c.code AS cty, c.id AS cty_id,
    coalesce((SELECT mpm.mode FROM manufacture_price_modes mpm WHERE mpm.company_id = c.id), 1) AS mode,
    p.id AS product_id, p.code AS ma_hang, p.name AS ten_hang, m.name AS hang,
    pu.id AS product_unit_id, u.name AS dvt, pt.id AS price_type_id, pt.name AS loai_gia,
    sc.code AS cty_nguon,
    (p.manufacture_id IS NOT NULL AND (
        EXISTS (SELECT 1 FROM inherited_price_factors ipf WHERE ipf.company_id = c.id AND ipf.manufacture_id = p.manufacture_id)
        OR CASE coalesce((SELECT mpm.mode FROM manufacture_price_modes mpm WHERE mpm.company_id = c.id), 1)
            WHEN 2 THEN NOT EXISTS (SELECT 1 FROM manufacture_price_mode_items mpi WHERE mpi.company_id = c.id AND mpi.manufacture_id = p.manufacture_id)
            ELSE EXISTS (SELECT 1 FROM manufacture_price_mode_items mpi WHERE mpi.company_id = c.id AND mpi.manufacture_id = p.manufacture_id)
        END)) AS ke_thua,
    coalesce(
        (SELECT ipf.factor FROM inherited_price_factors ipf WHERE ipf.company_id = c.id AND ipf.product_id = p.id),
        (SELECT ipf.factor FROM inherited_price_factors ipf WHERE ipf.company_id = c.id AND ipf.manufacture_id = p.manufacture_id),
        1) AS he_so_k,
    d.price, d.coefficient, d.sale_max_percent,
    d.is_manual_price_online, d.is_manual_coefficient_online, d.is_manual_sale_max_percent_online,
    s.price AS src_price, s.coefficient AS src_coefficient, s.sale_max_percent AS src_sale_max_percent,
    s.is_manual_price_online AS src_is_manual_price_online, s.is_manual_coefficient_online AS src_is_manual_coefficient_online,
    s.is_manual_sale_max_percent_online AS src_is_manual_sale_max_percent_online
FROM companies c
JOIN product_company_coefficients pcc ON pcc.company_id = c.id AND pcc.status = 3
JOIN products p ON p.id = pcc.product_id AND p.company_id <> c.id
JOIN companies sc ON sc.id = p.company_id
LEFT JOIN manufactures m ON m.id = p.manufacture_id
JOIN product_units pu ON pu.product_id = p.id
LEFT JOIN units u ON u.id = pu.unit_id
JOIN product_unit_prices d ON d.product_unit_id = pu.id AND d.company_id = c.id
JOIN price_types pt ON pt.id = d.price_type_id
LEFT JOIN product_unit_prices s ON s.product_unit_id = pu.id AND s.price_type_id = d.price_type_id AND s.company_id = p.company_id
WHERE FIND_IN_SET(c.code, CONVERT(@cty USING utf8mb4) COLLATE utf8mb4_unicode_ci)
ORDER BY c.code, p.code, pu.id, pt.order, pt.id;

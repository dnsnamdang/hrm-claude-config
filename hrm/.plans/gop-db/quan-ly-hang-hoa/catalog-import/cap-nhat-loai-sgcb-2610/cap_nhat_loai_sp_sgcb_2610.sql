-- =====================================================================================
-- Cập nhật phân loại 4 cấp cho hàng SGCB — nguồn: phân loại sản phẩm SGCB.xlsx (183 mã)
-- products chỉ lưu product_type_id; 3 cấp trên (Nhóm SP → Nhóm CN → Tính chất) suy ra theo cây
-- product_types → product_families → product_function_groups → product_natures.
-- Khớp: products.code = "Mã hàng", product_types.name = "Loại sản phẩm".
-- Mã hàng / Loại SP không có trên DB, hoặc Loại trống ⇒ BỎ QUA, liệt kê ở bước B4.
-- Chỉ ghi dòng có product_type_id khác giá trị mới. Điểm lui: bảng zz_sgcb2610_products_bak.
-- =====================================================================================
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ---------- B1. Dữ liệu file ----------
DROP TEMPORARY TABLE IF EXISTS tmp_sgcb2610_map;
CREATE TEMPORARY TABLE tmp_sgcb2610_map (
  dong_excel INT NOT NULL,
  product_code VARCHAR(255) NOT NULL,
  loai_name VARCHAR(255) NOT NULL,
  PRIMARY KEY (product_code)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO tmp_sgcb2610_map (dong_excel, product_code, loai_name) VALUES
(4,'SGCB-SGGF236:01','Cuộn dây hơi tự rút'),
(5,'SGCB-SGGD355','Móc treo'),
(6,'SGCB-SGGF181-57','PTLK thiết bị mài - đánh bóng khí nén'),
(7,'SGCB-SGGD289','Giá đỡ - giá treo'),
(8,'SGCB-SGGF004:02','Cuộn dây hơi tự rút'),
(9,'SGCB-SGGD356','Móc treo'),
(10,'SGCB-SGGF004:03','Cuộn dây hơi tự rút'),
(11,'SGCB-SGFB027','Hóa chất dưỡng nhựa'),
(12,'SGCB-SGGD357','Móc treo'),
(13,'SGCB-SGGD358','Móc treo'),
(14,'SGCB-SGFB004','Hóa chất rửa xe có chạm'),
(15,'SGCB-SGGF253','Cuộn dây hơi tự rút'),
(16,'SGCB-SGFB015','Hóa chất dưỡng lốp cao su đen'),
(17,'SGCB-SGFB021','Hóa chất tẩy nhựa đường và mưa axit'),
(18,'SGCB-SGGD359','Móc treo'),
(19,'SGCB-SGGD414','Xe đẩy sửa chữa trong xưởng'),
(20,'SGCB-SGFB014','Hóa chất dưỡng nhựa'),
(21,'SGCB-SGFB032','Hóa chất tẩy nhựa đường và mưa axit'),
(22,'SGCB-SGFB026','Hóa chất dưỡng nhựa'),
(23,'SGCB-SGGD492','Khăn - găng tay lau rửa xe'),
(24,'SGCB-SGFB030','Hóa chất rửa xe có chạm'),
(25,'SGCB-SGFA024','Hóa chất rửa xe có chạm'),
(26,'SGCB-SGFB045','Hóa chất rửa xe có chạm'),
(27,'SGCB-SGGD498','Khăn - găng tay lau rửa xe'),
(28,'SGCB-SGGD499','Khăn - găng tay lau rửa xe'),
(29,'SGCB-SGGD500','Khăn - găng tay lau rửa xe'),
(30,'SGCB-SGGD497','Khăn - găng tay lau rửa xe'),
(31,'SGCB-SGGD496','Khăn - găng tay lau rửa xe'),
(32,'SGCB-SGGD501','Khăn - găng tay lau rửa xe'),
(33,'SGCB-SGGD208','Khăn - găng tay lau rửa xe'),
(34,'SGCB-SGGD441','Khăn - găng tay lau rửa xe'),
(35,'SGCB-SGGF211-TCNHTBRX','Máy thổi khí nóng'),
(36,'SGCB-SGGF027','Cuộn dây điện (rulo)'),
(37,'SGCB-SGGD395','Khăn - găng tay lau rửa xe'),
(38,'SGCB-SGGF211','Máy thổi khí nóng'),
(39,'SGCB-SGGF212','Máy thổi khí nóng'),
(40,'SGCB-SGGC023','PTLK thiết bị - máy phun áp lực'),
(41,'SGCB-SGGD135','PTLK thiết bị - máy phun áp lực'),
(42,'SGCB-SGGD071','Khăn - găng tay lau rửa xe'),
(43,'SGCB-SGGD085','Găng tay - chổi vệ sinh'),
(44,'SGCB-SGGD045','Găng tay - chổi vệ sinh'),
(45,'SGCB-SGGF016','Cuộn dây hơi tự rút'),
(46,'SGCB-SGGD046','Găng tay - chổi vệ sinh'),
(47,'SGCB-SGGD188','Găng tay - chổi vệ sinh'),
(48,'SGCB-SGGA034','Phớt đánh bóng'),
(49,'SGCB-SGGA033','Phớt đánh bóng'),
(50,'SGCB-SGGC045','Súng phun bọt tuyết'),
(51,'SGCB-SGGC043','PTLK thiết bị - máy phun áp lực'),
(52,'SGCB-SGGC044','PTLK thiết bị - máy phun áp lực'),
(53,'SGCB-SGGC032','PTLK thiết bị - máy phun áp lực'),
(54,'SGCB-SGGD189','Dụng cụ chăm sóc xe'),
(55,'SGCB-SGO094','Khăn - găng tay lau rửa xe'),
(56,'SGCB-SGGD007','Khăn - găng tay lau rửa xe'),
(57,'SGCB-SGGD074','Khăn - găng tay lau rửa xe'),
(58,'SGCB-SGGD072','Khăn - găng tay lau rửa xe'),
(59,'SGCB-SGGF081','Máy rửa hơi nước nóng'),
(60,'SGCB-SGGF089','Máy thổi khí nóng'),
(61,'SGCB-SGGD051','Phớt đánh bóng'),
(62,'SGCB-SGGF063','Đèn kiểm tra bề mặt (sơn - ...)'),
(63,'SGCB-SGGF062','Đèn kiểm tra bề mặt (sơn - ...)'),
(64,'SGCB-SGGA083','Phớt đánh bóng'),
(65,'SGCB-SGGA053','Phớt đánh bóng'),
(66,'SGCB-SGGA050','Phớt đánh bóng'),
(67,'SGCB-SGF093','Hóa chất vệ sinh - dưỡng nội thất'),
(68,'SGCB-SGGF004','Cuộn dây hơi tự rút'),
(69,'SGCB-SGGF028','Máy đánh bóng hoạt động khí nén'),
(70,'SGCB-SGGF023','Cuộn dây hơi tự rút'),
(71,'SGCB-SGGF005','Cuộn dây hơi tự rút'),
(72,'SGCB-SGGE011','Hóa chất tẩy bụi sơn'),
(73,'SGCB-SGGA184','Phớt đánh bóng'),
(74,'SGCB-SGGF181','Máy đánh bóng hoạt động điện'),
(75,'SGCB-SGGF179','Máy đánh bóng hoạt động điện'),
(76,'SGCB-SGGC099','Súng phun bọt tuyết'),
(77,'SGCB-SGGD402','PTLK thiết bị - máy phun áp lực'),
(78,'SGCB-SGGC086','Súng hơi'),
(79,'SGCB-SGGC090','PTLK thiết bị - máy phun áp lực'),
(80,'SGCB-SGGC089','PTLK thiết bị - máy phun áp lực'),
(81,'SGCB-SGGC088','Súng phun bọt tuyết'),
(82,'SGCB-SGGF007','Cuộn dây hơi tự rút'),
(83,'SGCB-SGGF216','Cuộn dây điện (rulo)'),
(84,'SGCB-SGGF214','Cuộn dây hơi tự rút'),
(85,'SGCB-SGGA187','Phớt đánh bóng'),
(86,'SGCB-SGGA185','Phớt đánh bóng'),
(87,'SGCB-SGGD294','Dụng cụ chăm sóc xe'),
(88,'SGCB-SGGD296','Dụng cụ chăm sóc xe'),
(89,'SGCB-SGGD465:01','Dụng cụ chăm sóc xe'),
(90,'SGCB-SGGA209','Phớt đánh bóng'),
(91,'SGCB-SGGA164','Phớt đánh bóng'),
(92,'SGCB-SGGA163','Phớt đánh bóng'),
(93,'SGCB-SGGA162','Phớt đánh bóng'),
(94,'SGCB-SGGF154','Máy rửa hơi nước nóng'),
(95,'SGCB-SGO403','Đầu Phun'),
(96,'SGCB-SGO412','Dụng cụ xịt - châm - tra dầu'),
(97,'SGCB-SGGD418','Hóa chất tẩy nhựa đường và mưa axit'),
(98,'SGCB-SGGD285','Dụng cụ chăm sóc xe'),
(99,'SGCB-SGGD478','Hóa chất vệ sinh lazăng'),
(100,'SGCB-SGGD477','Hóa chất rửa và dưỡng khoang máy (bảo vệ khoang máy)'),
(101,'SGCB-SGGD490','Dụng cụ xịt - châm - tra dầu'),
(102,'SGCB-SGGD489','Dụng cụ xịt - châm - tra dầu'),
(103,'SGCB-SGGD488','Dụng cụ xịt - châm - tra dầu'),
(104,'SGCB-SGGD486','Dụng cụ xịt - châm - tra dầu'),
(105,'SGCB-SGGD471','Dụng cụ xịt - châm - tra dầu'),
(106,'SGCB-SGGD316','Khăn - găng tay lau rửa xe'),
(107,'SGCB-SGGD010','Khăn - găng tay lau rửa xe'),
(108,'SGCB-SGGD311','Giá treo phụ tùng - dụng cụ'),
(109,'SGCB-SGGE003','Hóa chất tẩy bụi sơn'),
(110,'SGCB-SGFB003','Hóa chất rửa xe có chạm'),
(111,'SGCB-SGFB002','Hóa chất rửa xe không chạm'),
(112,'SGCB-SGFB001:01','Hóa chất rửa xe không chạm'),
(113,'SGCB-SGFB062','Hóa chất làm sạch và phục hồi đèn pha - kính'),
(114,'SGCB-SGFB012','Hóa chất tẩy nhựa đường và mưa axit'),
(115,'SGCB-SGFB006','Hóa chất rửa xe có chạm'),
(116,'SGCB-SGFB005','Hóa chất rửa xe không chạm'),
(117,'SGCB-SGFL002','Hóa chất phủ bóng hoàn thiện bề mặt'),
(118,'SGCB-SGPM001','Dụng cụ chăm sóc xe'),
(119,'SGCB-SGGD037','PTLK thiết bị - máy phun áp lực'),
(120,'SGCB-SGFB037','Hóa chất dưỡng lốp cao su đen'),
(121,'SGCB-SGFB036','Hóa chất dưỡng nhựa'),
(122,'SGCB-SGGD453','Khăn - găng tay lau rửa xe'),
(123,'SGCB-SGGD434','Khăn - găng tay lau rửa xe'),
(124,'SGCB-SGFB029','Hóa chất rửa xe có chạm'),
(125,'SGCB-SGFB040','Hóa chất rửa xe không chạm'),
(126,'SGCB-SGFB017','Hóa chất rửa xe có chạm'),
(127,'SGCB-SGFB016','Hóa chất rửa xe không chạm'),
(128,'SGCB-SGGF177','Đèn kiểm tra bề mặt (sơn - ...)'),
(129,'SGCB-SGFB022','Hóa chất rửa xe có chạm'),
(130,'SGCB-SGFB018','Hóa chất làm sạch đa năng'),
(131,'SGCB-SGGD498:01','Khăn - găng tay lau rửa xe'),
(132,'SGCB-SGGD497:01','Khăn - găng tay lau rửa xe'),
(133,'SGCB-SGGD496:01','Khăn - găng tay lau rửa xe'),
(134,'SGCB-SGGD461:01','Khăn - găng tay lau rửa xe'),
(135,'SGCB-SGGD462:01','Khăn - găng tay lau rửa xe'),
(136,'SGCB-SGGD463:01','Khăn - găng tay lau rửa xe'),
(137,'SGCB-SGGD464:01','Khăn - găng tay lau rửa xe'),
(138,'SGCB-SGGD492:01','Khăn - găng tay lau rửa xe'),
(139,'SGCB-SGGD493:01','Khăn - găng tay lau rửa xe'),
(140,'SGCB-SGGD494:01','Khăn - găng tay lau rửa xe'),
(141,'SGCB-SGGD495:01','Khăn - găng tay lau rửa xe'),
(142,'SGCB-SGGD421','Găng tay - chổi vệ sinh'),
(143,'SGCB-SGGD354','PTLK thiết bị làm sạch bằng hóa chất'),
(144,'SGCB-SGGD502:01','Khăn - găng tay lau rửa xe'),
(145,'SGCB-SGGD501:02','Khăn - găng tay lau rửa xe'),
(146,'SGCB-SGGD500:01','Khăn - găng tay lau rửa xe'),
(147,'SGCB-SGGD499:02','Khăn - găng tay lau rửa xe'),
(148,'SGCB-SGFB010','Hóa chất tẩy nhựa đường và mưa axit'),
(149,'SGCB-SGGF192','Máy đánh bóng hoạt động điện'),
(150,'SGCB-SGGF013','Cuộn dây hơi tự rút'),
(151,'CH-SGFA036','Hóa chất vệ sinh - dưỡng nội thất'),
(152,'SGCB-SGGF251','Cuộn dây điện (rulo)'),
(153,'SGCB-SGFB020','Hóa chất làm sạch đa năng'),
(154,'SGCB-SGFY006','Hóa chất làm sạch đa năng'),
(155,'SGCB-SGGS004','Súng xịt'),
(156,'SGCB-SGGF234','Cuộn dây điện (rulo)'),
(157,'SGCB-SGGF232','Cuộn dây hơi tự rút'),
(158,'SGCB-SGGD460:01','Khăn - găng tay lau rửa xe'),
(159,'SGCB-SGGD504:01','Khăn - găng tay lau rửa xe'),
(160,'SGCB-SGGD503:01','Khăn - găng tay lau rửa xe'),
(161,'SGCB-SGGD436','Bình bọt tuyết'),
(162,'SGCB-SGGD411','Bánh xe - càng bánh xe'),
(163,'SGCB-SGGC096','Bình bọt tuyết'),
(164,'SGCB-SGGF076','Cuộn dây điện (rulo)'),
(165,'SGCB-SGGF360','Bình bọt tuyết'),
(166,'SGCB-SGGC098','Máy hút bụi'),
(167,'SGCB-SGGF273','Máy đánh bóng hoạt động điện'),
(168,'SGCB-SGFY004','Xi đánh bóng'),
(169,'SGCB-SGFY002','Xi đánh bóng'),
(170,'SGCB-SGFB048','Hóa chất tẩy nhựa đường và mưa axit'),
(171,'SGCB-SGGD360','Hệ thống treo'),
(172,'SGCB-SGGD348','Hệ thống treo'),
(173,'SGCB-SGGF323','Máy đánh bóng hoạt động điện'),
(174,'SGCB-SGGD342','Găng tay - chổi vệ sinh'),
(175,'SGCB-SGGD439','Máy đo độ ẩm - tỷ trọng - độ nhớt'),
(176,'SGCB-SGGF194','PTLK thiết bị làm sạch bằng hóa chất'),
(177,'SGCB-SGD022','Hóa chất tẩy nhựa đường và mưa axit'),
(178,'SGCB-SGGC101','Súng xịt'),
(179,'SGCB-SGFB057','Hóa chất tẩy nhựa đường và mưa axit'),
(180,'SGCB-SGFB050','Hóa chất dưỡng nhựa'),
(181,'SGCB-SGFB051','Hóa chất dưỡng nhựa'),
(182,'SGCB-SGGF255','Bình bọt tuyết'),
(183,'SGCB-SGPM014','Dụng cụ chăm sóc xe'),
(184,'SGCB-SGPM013','Dụng cụ chăm sóc xe'),
(185,'SGCB-SGGF141','PTLK thiết bị làm sạch bằng hóa chất'),
(186,'SGCB-SGFB028','Hóa chất làm sạch đa năng');

-- ---------- B2. Sao lưu + kiểm trước ----------
CREATE TABLE IF NOT EXISTS zz_sgcb2610_products_bak AS
  SELECT p.id, p.code, p.product_type_id, p.updated_at
  FROM products p JOIN tmp_sgcb2610_map m ON m.product_code = p.code;

SELECT COUNT(*) AS se_cap_nhat
FROM products p
JOIN tmp_sgcb2610_map m ON m.product_code = p.code
JOIN product_types t ON t.name = m.loai_name
WHERE m.loai_name <> '' AND NOT (p.product_type_id <=> t.id);

-- ---------- B3. Cập nhật ----------
UPDATE products p
JOIN tmp_sgcb2610_map m ON m.product_code = p.code
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
FROM tmp_sgcb2610_map m
LEFT JOIN product_types t ON t.name = m.loai_name AND m.loai_name <> ''
WHERE m.loai_name = ''
   OR t.id IS NULL
   OR NOT EXISTS (SELECT 1 FROM products p WHERE p.code = m.product_code)
ORDER BY m.dong_excel;

-- ---------- B5. Kiểm sau: 4 cấp theo Loại trong file ----------
SELECT m.loai_name, t.code AS loai_code, f.name AS nhom_sp, g.name AS nhom_cn, n.name AS tinh_chat,
       COUNT(*) AS so_hang, SUM(p.product_type_id <=> t.id) AS da_dung_loai
FROM tmp_sgcb2610_map m
JOIN products p ON p.code = m.product_code
JOIN product_types t ON t.name = m.loai_name
JOIN product_families f ON f.id = t.product_family_id
JOIN product_function_groups g ON g.id = f.product_function_group_id
JOIN product_natures n ON n.id = g.product_nature_id
GROUP BY m.loai_name, t.code, f.name, g.name, n.name
ORDER BY m.loai_name;

DROP TEMPORARY TABLE IF EXISTS tmp_sgcb2610_map;

-- ---------- Rollback (chỉ khi cần) ----------
-- UPDATE products p JOIN zz_sgcb2610_products_bak b ON b.id = p.id
--   SET p.product_type_id = b.product_type_id, p.updated_at = b.updated_at;
-- Nghiệm thu xong: DROP TABLE zz_sgcb2610_products_bak;

-- =====================================================================================
-- Cập nhật phân loại 4 cấp cho hàng mua ngoài SG — nguồn: Hàng mua ngoài SG_update.xlsx (185 mã)
-- products chỉ lưu product_type_id; 3 cấp trên (Nhóm SP → Nhóm CN → Tính chất) suy ra theo cây
-- product_types → product_families → product_function_groups → product_natures.
-- Khớp: products.code = "Mã hàng", product_types.name = "Loại sản phẩm".
-- Mã hàng / Loại SP không có trên DB, hoặc Loại trống ⇒ BỎ QUA, liệt kê ở bước B4.
-- Chỉ ghi dòng có product_type_id khác giá trị mới. Điểm lui: bảng zz_sg2610_products_bak.
-- =====================================================================================
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ---------- B1. Dữ liệu file ----------
DROP TEMPORARY TABLE IF EXISTS tmp_sg2610_map;
CREATE TEMPORARY TABLE tmp_sg2610_map (
  dong_excel INT NOT NULL,
  product_code VARCHAR(255) NOT NULL,
  loai_name VARCHAR(255) NOT NULL,
  PRIMARY KEY (product_code)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO tmp_sg2610_map (dong_excel, product_code, loai_name) VALUES
(2,'MNSG-MN-HB-GT0113','Găng tay'),
(3,'MNSG-YT-4590:01','Bộ búa - đe'),
(4,'MNSG-MNUCD22KV','Trang bị cách điện'),
(5,'MNSG-MN-HB-LK0103','Lọc khí nén'),
(6,'MNSG-MNSG-LAPDATMNK','PTLK máy nén khí'),
(7,'MNSG-MNSG-VATTUOCAM','PTLK thiết bị đo - kiểm tra điện'),
(8,'MNSG-PT0103','Gioăng - phớt'),
(9,'MNSG-XML-T6','Đèn pin - đèn chiếu sáng di động'),
(10,'MNSG-NCTN','Vỏ - nắp - chụp bảo vệ'),
(11,'MNSG-8410MP','Bộ khẩu'),
(12,'MNSG-VT-CK0101','Cút nối'),
(13,'MNSG-KR-TG10710056','Máy cắt - mài - đánh gỉ hoạt động điện'),
(14,'MNSG-KSGAAI0702','Bộ búa - đe'),
(15,'MNSG-KR-MN-DBH','Trang phục bảo hộ'),
(16,'MNSG-QT30-3-25A','Cuộn dây điện (rulo)'),
(17,'MNSG-MN-BCC-19100','Bình chữa cháy di động'),
(18,'MNSG-KR-MN-2046A7010S-10','Đế từ'),
(19,'MNSG-1009','Đồng hồ đo điện vạn năng'),
(20,'MNSG-KD0102','Khởi động từ'),
(21,'MNSG-KD0102:01','Khởi động từ'),
(22,'MNSG-H-701R0','Trang phục bảo hộ'),
(23,'MNSG-DHDN-01','Vật tư phụ lắp đặt'),
(24,'MNSG-YT-2370','Súng bơm và đo áp suất lốp'),
(25,'MNSG-BP0205','Gioăng - phớt thủy lực'),
(26,'MNSG-VT-1310','Bộ vam - búa giật'),
(27,'MNSG-MN-39009','Dụng cụ cách điện'),
(28,'MNSG-MN-BDCDB','Gioăng - phớt'),
(29,'MNSG-HAS-DLM27ALFHAS','Lọc khí nén'),
(30,'MNSG-SRL22ME5A','Máy nén khí xoắn ốc không dầu'),
(31,'MNSG-GD580-01','Găng tay'),
(32,'MNSG-MN-BHHAN','Trang phục bảo hộ'),
(33,'MNSG-SX-VT-LL0102','Bông lọc F5'),
(34,'MNSG-MN-TPH-6510','Dây hơi khí nén'),
(35,'MNSG-MNSG-TCSPA271','Cờ lê 2 đầu mở'),
(36,'MNSG-MNSG-3781-11P','Tay vặn nhanh'),
(37,'MNSG-MNSG-402506','Khẩu đầu hoa thị - lục giác'),
(38,'MNSG-MNSG-237506M','Khẩu ngắn'),
(39,'MNSG-MNSG-THTGTS8150','Tua vít đóng'),
(40,'MNSG-MNSG-THT250FL1206','Bộ tua vít'),
(41,'MNSG-KRSG-BCB','Biển cảnh báo'),
(42,'MNSG-1025','Thiết bị hút dầu thải bằng khí nén'),
(43,'MNSG-G1055','Thiết bị camera nội soi'),
(44,'MNSG-QT20-3-15A','Cuộn dây điện (rulo)'),
(45,'MNSG-MN-SUNGGHIM','Dụng cụ - súng bắn đinh - rive'),
(46,'MNSG-ST642','Túi đồ nghề'),
(47,'MNSG-MN-TZ210MP-2','Kích cá sấu'),
(48,'MNSG-HP-BP02020:01','Bình bọt tuyết'),
(49,'MNSG-KD0101','Khởi động từ'),
(50,'MNSG-PUL-NS6510','Dây hơi khí nén'),
(51,'MNSG-MN-HB-CB0101','Cục kê - tấm chắn - bát cao su'),
(52,'MNSG-MN-VT-NT0102','Bu lông nở'),
(53,'MNSG-MN-HB-DH0401','Đồng hồ đo điện vạn năng'),
(54,'MNSG-MN-DAYDIEN','Cuộn dây điện (rulo)'),
(55,'MNSG-X0755PRO','Súng vặn ốc hoạt động điện'),
(56,'MNSG-VT0102','Vỏ - nắp - chụp bảo vệ'),
(57,'MNSG-SGMN34423-1A','Tay cân lực (Cờ lê cân lực)'),
(58,'MNSG-BT0104','Biến tần'),
(59,'MNSG-BDNMITSUBISHI','Đầu nối - khớp nối - đầu chuyển đổi - đầu nối nhanh'),
(60,'MNSG-MNSG-GIAY','Trang phục bảo hộ'),
(61,'MNSG-SX-VT-BD0306','Bóng đèn'),
(62,'MNSG-BVL51BP','Máy hút bụi'),
(63,'MNSG-APCCK1000','Dụng cụ kiểm tra áp suất bơm'),
(64,'MNSG-AK-9048','Máy hàn nhựa'),
(65,'MNSG-DB13','Dụng cụ mở chén cổ'),
(66,'MNSG-DB11','Khẩu'),
(67,'MNSG-DB10','Khẩu'),
(68,'MNSG-EG-EQ1202','Giá đỡ - giá treo'),
(69,'MNSG-EG-EQ1202:01','Giá đỡ - giá treo'),
(70,'MNSG-DI0101','Giá treo Pin'),
(71,'MNSG-BDNTOYOTA','Đầu nối - khớp nối - đầu chuyển đổi - đầu nối nhanh'),
(72,'MNSG-116330TR','Tua vít đầu hoa thị - lục giác'),
(73,'MNSG-MN-HB-ACT-200-12','Dụng cụ tháo lắp hệ thống điều hòa'),
(74,'MNSG-MN-HB-BD0402','Bóng đèn'),
(75,'MNSG-MN-VAMVF01','Khẩu'),
(76,'MNSG-145-185','Panme'),
(77,'MNSG-MN-TCL','PTLK cầu nâng 2 trụ'),
(78,'MNSG-L180MM','Bản lề - khóa - tay mở'),
(79,'MNSG-MN-M12-FIW2F12','Súng vặn ốc hoạt động điện'),
(80,'MNSG-MN-HB-JTC-4672','Bộ vam giật'),
(81,'MNSG-MN-DENCANHBAO','Đèn báo'),
(82,'MNSG-EG-DE4005','Động cơ'),
(83,'MNSG-103-140-10','Panme'),
(84,'MNSG-103-137','Panme'),
(85,'MNSG-7262-300','Dụng cụ đo cơ khí'),
(86,'MNSG-5716A','PTLK thiết bị kiểm tra động cơ'),
(87,'MNSG-ZX7-200E','Máy hàn hồ quang tay (MMA - hàn que)'),
(88,'MNSG-CMDT392-K-SL:01','PTLK thiết bị đo - kiểm tra điện'),
(89,'MNSG-CMDT392-K-SL','Vòng bi/gối đỡ'),
(90,'MNSG-HP-BP02020','Bình bọt tuyết'),
(91,'MNSG-DENCHIEUSANG','Đèn điện'),
(92,'MNSG-SIM4G-CS','PTLK trụ - cây sạc điện'),
(93,'MNSG-DAUCHUYENDOI','Đầu nối - đầu chuyển đổi'),
(94,'MNSG-SG-MN-TAMDOTRUOC','PTLK thiết bị kiểm tra góc đặt bánh xe'),
(95,'MNSG-SG-MN-TAMCHANSAU','PTLK thiết bị kiểm tra góc đặt bánh xe'),
(96,'MNSG-SG-MN-VT-ON0104','Nối ống nhựa'),
(97,'MNSG-TDT-DC120-320A','Tủ điện phân phối'),
(98,'MNSG-MAICHETRUSAC','Vỏ - nắp - chụp bảo vệ'),
(99,'MNSG-ORIONMOTORVN','Bình chữa cháy di động'),
(100,'MNSG-NCCL','Vỏ - nắp - chụp bảo vệ'),
(101,'MNSG-MN-HB-KD0301:01','Khởi động từ'),
(102,'MNSG-MN-HB-KD0301','Khởi động từ'),
(103,'MNSG-MN-TUYPVUONG','Khẩu'),
(104,'MNSG-MN-HB-CC0108:01','Xích - cáp - dây cẩu hàng'),
(105,'MNSG-MN-HB-CC0108','Cáp mềm'),
(106,'MNSG-YT-75071','Dao'),
(107,'MNSG-MN-SG08901087','Hóa chất vệ sinh lazăng'),
(108,'MNSG-MN-SGLQ-3077','Mỡ bôi trơn đặc chủng'),
(109,'MNSG-MN-SGGLM100-25C','Dụng cụ đo cơ khí'),
(110,'MNSG-MN-SGYZ-6024','Bộ vam ép'),
(111,'MNSG-MN-SGAS01027','Bộ vam ép'),
(112,'MNSG-MN-SGYT-06822','Bộ vam ép'),
(113,'MNSG-PAP-D050H','Súng xịt'),
(114,'MNSG-DCH-100100DP-2A','Kích nâng khác'),
(115,'MNSG-TAT8131-3','Súng hơi'),
(116,'MNSG-BT691012','Dụng cụ xả hơi lốp'),
(117,'MNSG-TH3250','Tay vặn chữ T'),
(118,'MNSG-633060M','Khẩu'),
(119,'MNSG-633058M','Khẩu'),
(120,'MNSG-1026-SG','Thiết bị thay dầu phanh'),
(121,'MNSG-4640','Dụng cụ siết vặn khác'),
(122,'MNSG-KR-511-723-20','Đồng hồ so'),
(123,'MNSG-MASTER2','Máy chẩn đoán xe ô tô (Thiết bị đọc lỗi ECU)'),
(124,'MNSG-TMT47503','Đồng hồ đo điện vạn năng'),
(125,'MNSG-GDC17','Bộ vam rotuyn'),
(126,'MNSG-DAOBAMATIT','Dụng cụ chà matit bằng tay (có hoặc không có hút bụi)'),
(127,'MNSG-MN-GM-70S','Dây hàn mig'),
(128,'MNSG-MN-HB-BK0301','Bộ khẩu'),
(129,'MNSG-HAD20B','Van đóng mở'),
(130,'MNSG-MN-M9503B','Máy cắt - mài - đánh gỉ hoạt động điện'),
(131,'MNSG-SG-NM0109','Bộ linh kiện điều hòa'),
(132,'MNSG-BCBKSC','Biển cảnh báo'),
(133,'MNSG-BCBTX','Biển cảnh báo'),
(134,'MNSG-THT11101-3','Dây hơi khí nén'),
(135,'MNSG-TACLI2012','Máy nén khí piston'),
(136,'MNSG-TACSD0251','Mũi khoan'),
(137,'MNSG-1021R','Đồng hồ đo điện vạn năng'),
(138,'MNSG-M18FHIWF12-502X-SET','Súng vặn ốc hoạt động điện'),
(139,'MNSG-MN-DCV1T','Xích - cáp - dây cẩu hàng'),
(140,'MNSG-MN-PDD02','Đèn pin - đèn chiếu sáng di động'),
(141,'MNSG-MN-DPCT','Đèn pin - đèn chiếu sáng di động'),
(142,'MNSG-MN-TDRLI206015','Súng vặn ốc hoạt động điện'),
(143,'MNSG-MN-DAYDIEN15M','Cuộn dây điện (rulo)'),
(144,'MNSG-MN-XICH8M','Xích - cáp - dây cẩu hàng'),
(145,'MNSG-SGMN-AEAV1214','Cờ lê 1 đầu'),
(146,'MNSG-SGMNTK-GL129','Bộ vam ép'),
(147,'MNSG-SGMN-ANKO127','Cờ lê 2 đầu mở'),
(148,'MNSG-SGMN-ANAKO124','Cờ lê 2 đầu mở'),
(149,'MNSG-MW3258751-01','Lực kế'),
(150,'MNSG-MW1580311-01','Lực kế'),
(151,'MNSG-MN-ORIONOR-3','Bình chữa cháy di động'),
(152,'MNSG-KR-500-181-30','Thước cặp'),
(153,'MNSG-MN-HB-BA0201','Ắc quy'),
(154,'MNSG-MN-HB-TC0501','Đế máy chà'),
(155,'MNSG-DAY8X12MM','Dây hơi khí nén'),
(156,'MNSG-MNSGTV1','Dụng cụ - thước đo góc'),
(157,'MNSG-QS400','Quạt công nghiệp'),
(158,'MNSG-MN-TCT','Bộ dụng cụ khác'),
(159,'MNSG-MN-HB-KD0201','Khay đựng chi tiết'),
(160,'MNSG-KRSG38M09A','Kìm - kẹp'),
(161,'MNSG-KRSG38242210','Khẩu ngắn'),
(162,'MNSG-MN-HB-MD0401','Bộ thổi khí nóng'),
(163,'MNSG-MN-HB-MN0207','Máy nén khí piston'),
(164,'MNSG-MN-HB-SBL001','Đồng hồ đo áp suất'),
(165,'MNSG-SX-VT-BD0304','Bóng đèn'),
(166,'MNSG-MIG-08','Dây hàn mig'),
(167,'MNSG-MN-HB-MNK-0103','Máy nén khí piston'),
(168,'MNSG-MN-HB-TC0208','Tay cân lực (Cờ lê cân lực)'),
(169,'MNSG-MN-MPD-5KW','Vật tư phụ lắp đặt'),
(170,'MNSG-MN-NAPGAS','Dụng cụ đo và nạp ga điều hòa'),
(171,'MNSG-TM-V-0258-120L','Máy nén khí piston'),
(172,'MNSG-MN-HB-CK0107','Cục kê - tấm chắn - bát cao su'),
(173,'MNSG-KRSGXENANGTP','Xe nâng hàng'),
(174,'MNSG-KR-TSP02501','Dụng cụ tháo lắp kính chắn gió'),
(175,'MNSG-KRSG-CCB','Biển cảnh báo'),
(176,'MNSG-KRSG-PROLOCKEYLT02','Biển cảnh báo'),
(177,'MNSG-KR-MN-ASA-264-999','Dụng cụ - thước đo góc'),
(178,'MNSG-KRSG-FLUKEVT06','Nhiệt kế đo nhiệt độ'),
(179,'MNSG-KRSG-TDCK','Khóa'),
(180,'MNSG-KRSG-OK','Khóa'),
(181,'MNSG-KRSGHDCK','Hộp nhựa'),
(182,'MNSG-KRSG-ARCVES40-M','Trang phục bảo hộ'),
(183,'MNSG-KRSGAS1000HAT-SPL','Kính - mặt nạ bảo hộ'),
(184,'MNSG-KRSG-GTV-VN-10','Trang phục bảo hộ'),
(185,'MNSG-KRSG-MIXPACDP2X200','Súng bắn keo - Bơm keo'),
(186,'MNSG-MN-HB-CS0104','Khớp nối cao su');

-- ---------- B2. Sao lưu + kiểm trước ----------
CREATE TABLE IF NOT EXISTS zz_sg2610_products_bak AS
  SELECT p.id, p.code, p.product_type_id, p.updated_at
  FROM products p JOIN tmp_sg2610_map m ON m.product_code = p.code;

SELECT COUNT(*) AS se_cap_nhat
FROM products p
JOIN tmp_sg2610_map m ON m.product_code = p.code
JOIN product_types t ON t.name = m.loai_name
WHERE m.loai_name <> '' AND NOT (p.product_type_id <=> t.id);

-- ---------- B3. Cập nhật ----------
UPDATE products p
JOIN tmp_sg2610_map m ON m.product_code = p.code
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
FROM tmp_sg2610_map m
LEFT JOIN product_types t ON t.name = m.loai_name AND m.loai_name <> ''
WHERE m.loai_name = ''
   OR t.id IS NULL
   OR NOT EXISTS (SELECT 1 FROM products p WHERE p.code = m.product_code)
ORDER BY m.dong_excel;

-- ---------- B5. Kiểm sau: 4 cấp theo Loại trong file ----------
SELECT m.loai_name, t.code AS loai_code, f.name AS nhom_sp, g.name AS nhom_cn, n.name AS tinh_chat,
       COUNT(*) AS so_hang, SUM(p.product_type_id <=> t.id) AS da_dung_loai
FROM tmp_sg2610_map m
JOIN products p ON p.code = m.product_code
JOIN product_types t ON t.name = m.loai_name
JOIN product_families f ON f.id = t.product_family_id
JOIN product_function_groups g ON g.id = f.product_function_group_id
JOIN product_natures n ON n.id = g.product_nature_id
GROUP BY m.loai_name, t.code, f.name, g.name, n.name
ORDER BY m.loai_name;

DROP TEMPORARY TABLE IF EXISTS tmp_sg2610_map;

-- ---------- Rollback (chỉ khi cần) ----------
-- UPDATE products p JOIN zz_sg2610_products_bak b ON b.id = p.id
--   SET p.product_type_id = b.product_type_id, p.updated_at = b.updated_at;
-- Nghiệm thu xong: DROP TABLE zz_sg2610_products_bak;

-- Du lieu mau cho 2 bao cao Meeting (theo nhan vien / theo du an) — thang 10/2026
SET NAMES utf8mb4;
SET @now = '2026-10-02 14:50:00';

-- M1: Hoan thanh, KH, truc tiep, du an 145
INSERT INTO meetings (code,name,meeting_type_id,is_customer_meeting,mode_id,status,completed_at,location,start_date,end_date,host_employee_id,has_prospective_project,customer_id,customer_name,content,conclusion,company_id,department_id,created_by,updated_by,created_at,updated_at)
VALUES ('TPE.MET.KH.26.0060','Khảo sát mặt bằng xưởng 2S Hyundai Sơn Đồng',1,1,1,3,'2026-10-01 11:05:00','Showroom Hyundai Sơn Đồng, Hoài Đức','2026-10-01 09:00:00','2026-10-01 11:00:00',67,1,916,'CÔNG TY CỔ PHẦN HYUNDAI PHẠM VĂN ĐỒNG',
'1. Khảo sát mặt bằng khu vực khoang dịch vụ nhanh\n2. Thống nhất danh mục thiết bị cầu nâng, máy ra vào lốp','1. Khách hàng đồng ý phương án bố trí 6 khoang\n2. Gửi báo giá sơ bộ trước ngày 10/10',1,44,67,67,@now,@now);
SET @m1 = LAST_INSERT_ID();

-- M2: Hoan thanh, KH, online, du an 138
INSERT INTO meetings (code,name,meeting_type_id,is_customer_meeting,mode_id,status,completed_at,online_link,start_date,end_date,host_employee_id,has_prospective_project,customer_id,customer_name,content,conclusion,company_id,department_id,created_by,updated_by,created_at,updated_at)
VALUES ('TPE.MET.KH.26.0061','Trao đổi cấu hình thiết bị xưởng 2S Phương Anh',1,1,2,3,'2026-10-01 15:35:00','https://meet.google.com/pya-xuong-2s','2026-10-01 14:00:00','2026-10-01 15:30:00',66,1,20617,'CÔNG TY TNHH THƯƠNG MẠI VÀ VẬN TẢI PHƯƠNG ANH',
'1. Rà soát cấu hình máy chẩn đoán và thiết bị cân chỉnh góc đặt bánh xe','1. Khách hàng chọn cấu hình tiêu chuẩn\n2. Bổ sung phương án trả góp',1,44,66,66,@now,@now);
SET @m2 = LAST_INSERT_ID();

-- M3: Hoan thanh, noi bo, truc tiep, du an 145
INSERT INTO meetings (code,name,meeting_type_id,is_customer_meeting,mode_id,status,completed_at,location,start_date,end_date,host_employee_id,has_prospective_project,content,conclusion,company_id,department_id,created_by,updated_by,created_at,updated_at)
VALUES ('TPE.MET.NB.26.0062','Họp nội bộ chốt phương án kỹ thuật dự án Hyundai Sơn Đồng',2,0,1,3,'2026-10-02 10:05:00','Phòng họp tầng 3','2026-10-02 08:30:00','2026-10-02 10:00:00',44,1,
'1. Chốt phương án kỹ thuật và tiến độ lập báo giá','1. Phòng Thiết bị ô tô 2 hỗ trợ bóc tách khối lượng\n2. Hạn hoàn thiện hồ sơ: 08/10/2026',1,5,44,44,@now,@now);
SET @m3 = LAST_INSERT_ID();

-- M4: Huy, KH, online, du an 141
INSERT INTO meetings (code,name,meeting_type_id,is_customer_meeting,mode_id,status,online_link,start_date,end_date,host_employee_id,has_prospective_project,customer_id,customer_name,content,cancel_reason,cancelled_at,cancelled_by,company_id,department_id,created_by,updated_by,created_at,updated_at)
VALUES ('TPE.MET.KH.26.0063','Tư vấn thiết bị xưởng sửa chữa Anh Phát',1,1,2,4,'https://meet.google.com/anh-phat','2026-10-01 16:00:00','2026-10-01 17:00:00',75,1,3966,'ANH PHÁT',
'1. Giới thiệu giải pháp thiết bị xưởng sửa chữa','Khách hàng bận đột xuất, xin dời lịch','2026-10-01 15:00:00',75,1,44,75,75,@now,@now);
SET @m4 = LAST_INSERT_ID();

-- M5: Chot lich (tuong lai), KH, truc tiep, du an 146
INSERT INTO meetings (code,name,meeting_type_id,is_customer_meeting,mode_id,status,location,start_date,end_date,host_employee_id,has_prospective_project,customer_id,customer_name,content,company_id,department_id,created_by,updated_by,created_at,updated_at)
VALUES ('TPE.MET.KH.26.0064','Thuyết trình giải pháp xưởng 2S Đà Nẵng',1,1,1,2,'Văn phòng 27-7 Hồng Quang, Đà Nẵng','2026-10-06 09:00:00','2026-10-06 11:30:00',76,1,18505,'CÔNG TY CỔ PHẦN 27-7 HỒNG QUANG',
'1. Thuyết trình giải pháp tổng thể xưởng 2S\n2. Trao đổi tiến độ đầu tư',1,44,76,76,@now,@now);
SET @m5 = LAST_INSERT_ID();

-- M6: Chot lich (tuong lai), Hop giao ban, truc tiep, khong du an
INSERT INTO meetings (code,name,meeting_type_id,is_customer_meeting,mode_id,status,location,start_date,end_date,host_employee_id,has_prospective_project,content,company_id,department_id,created_by,updated_by,created_at,updated_at)
VALUES ('TPE.MET.NB.26.0065','Họp giao ban tuần 41 khối kinh doanh',6,0,1,2,'Phòng họp lớn tầng 5','2026-10-08 14:00:00','2026-10-08 16:00:00',212,0,
'1. Đánh giá kết quả kinh doanh tuần 40\n2. Kế hoạch tuần 41',1,58,212,212,@now,@now);
SET @m6 = LAST_INSERT_ID();

-- M7: Hoan thanh, noi bo, online, du an 138
INSERT INTO meetings (code,name,meeting_type_id,is_customer_meeting,mode_id,status,completed_at,online_link,start_date,end_date,host_employee_id,has_prospective_project,content,conclusion,company_id,department_id,created_by,updated_by,created_at,updated_at)
VALUES ('TPE.MET.NB.26.0066','Rà soát báo giá dự án 2S Phương Anh',2,0,2,3,'2026-10-02 08:35:00','https://meet.google.com/ra-soat-bg','2026-10-02 07:30:00','2026-10-02 08:30:00',66,1,
'1. Rà soát đơn giá và tỷ suất lợi nhuận báo giá','1. Điều chỉnh giá máy cân chỉnh góc đặt bánh xe',1,44,66,66,@now,@now);
SET @m7 = LAST_INSERT_ID();

-- Thanh vien (type 1 = cong ty, type 2 = khach hang)
INSERT INTO meeting_employees (meeting_id,employee_id,name,role,phone,type,attendance_status,sort_order,created_at,updated_at) VALUES
(@m1,67,'Nguyễn Anh Tú','Nhân viên Kinh doanh','0912345601',1,1,1,@now,@now),
(@m1,24,'Nguyễn Đức Tuân','Trưởng phòng Kinh doanh','0988737896',1,1,2,@now,@now),
(@m1,NULL,'Anh Đỗ Văn Khánh','Giám đốc dịch vụ','0903111222',2,1,1,@now,@now),
(@m1,NULL,'Chị Lê Thu Hà','Trưởng phòng mua hàng','0903111333',2,1,2,@now,@now),
(@m2,66,'Nguyễn Văn Bình','Nhân viên Kinh doanh','0912345602',1,1,1,@now,@now),
(@m2,62,'Lê Thị Tuyết','Trợ lý kinh doanh','0904554959',1,1,2,@now,@now),
(@m2,44,'Nguyễn Văn Lâm','Kỹ sư giải pháp','0912345603',1,1,3,@now,@now),
(@m2,NULL,'Anh Phạm Quốc Việt','Giám đốc','0904222333',2,1,1,@now,@now),
(@m3,44,'Nguyễn Văn Lâm','Kỹ sư giải pháp','0912345603',1,1,1,@now,@now),
(@m3,83,'Hồ Thị Xuân','Nhân viên Kinh doanh','0912345604',1,1,2,@now,@now),
(@m3,139,'Phạm Minh Hiếu','Chuyên viên Kinh doanh','0982682898',1,1,3,@now,@now),
(@m3,67,'Nguyễn Anh Tú','Nhân viên Kinh doanh','0912345601',1,1,4,@now,@now),
(@m4,75,'Trần Văn Thái','Nhân viên Kinh doanh','0912345605',1,1,1,@now,@now),
(@m4,NULL,'Anh Nguyễn Văn Phát','Chủ xưởng','0905333444',2,1,1,@now,@now),
(@m5,76,'Nguyễn Thị Hường','Nhân viên Kinh doanh','0912345606',1,1,1,@now,@now),
(@m5,24,'Nguyễn Đức Tuân','Trưởng phòng Kinh doanh','0988737896',1,1,2,@now,@now),
(@m5,NULL,'Anh Trần Minh Quang','Phó Tổng Giám đốc','0906444555',2,1,1,@now,@now),
(@m5,NULL,'Anh Võ Đức Thịnh','Trưởng xưởng','0906444666',2,1,2,@now,@now),
(@m6,212,'Ngô Thị Hằng','Phó Tổng Giám đốc','0912345607',1,1,1,@now,@now),
(@m6,24,'Nguyễn Đức Tuân','Trưởng phòng Kinh doanh','0988737896',1,1,2,@now,@now),
(@m6,44,'Nguyễn Văn Lâm','Kỹ sư giải pháp','0912345603',1,1,3,@now,@now),
(@m6,62,'Lê Thị Tuyết','Trợ lý kinh doanh','0904554959',1,1,4,@now,@now),
(@m7,66,'Nguyễn Văn Bình','Nhân viên Kinh doanh','0912345602',1,1,1,@now,@now),
(@m7,68,'Nguyễn Đăng Long','Nhân viên Kinh doanh','0912345608',1,1,2,@now,@now);

-- Bien ban (meeting_reports) cho cac cuoc hop da hoan thanh
INSERT INTO meeting_reports (meeting_id,content,solution,proposer_id,proposer_name,proposer_type,executor_id,executor_name,executor_type,expected_deadline,created_at,updated_at) VALUES
(@m1,'Gửi bản vẽ bố trí 6 khoang dịch vụ nhanh','Phòng Thiết bị ô tô 3 lập bản vẽ',67,'Nguyễn Anh Tú',1,67,'Nguyễn Anh Tú',1,'2026-10-07',@now,@now),
(@m1,'Lập báo giá sơ bộ cầu nâng và máy ra vào lốp','Áp dụng bảng giá quý 4',24,'Nguyễn Đức Tuân',1,67,'Nguyễn Anh Tú',1,'2026-10-10',@now,@now),
(@m2,'Bổ sung phương án trả góp 12 tháng','Làm việc với ngân hàng đối tác',66,'Nguyễn Văn Bình',1,62,'Lê Thị Tuyết',1,'2026-10-09',@now,@now),
(@m3,'Bóc tách khối lượng thiết bị khoang sơn','Phòng Thiết bị ô tô 2 hỗ trợ',44,'Nguyễn Văn Lâm',1,83,'Hồ Thị Xuân',1,'2026-10-08',@now,@now);

-- Gan du an tien kha thi
INSERT INTO prospective_project_meetings (prospective_project_id,meeting_id,meeting_code,meeting_name,created_at,updated_at) VALUES
(145,@m1,'TPE.MET.KH.26.0060','Khảo sát mặt bằng xưởng 2S Hyundai Sơn Đồng',@now,@now),
(138,@m2,'TPE.MET.KH.26.0061','Trao đổi cấu hình thiết bị xưởng 2S Phương Anh',@now,@now),
(145,@m3,'TPE.MET.NB.26.0062','Họp nội bộ chốt phương án kỹ thuật dự án Hyundai Sơn Đồng',@now,@now),
(141,@m4,'TPE.MET.KH.26.0063','Tư vấn thiết bị xưởng sửa chữa Anh Phát',@now,@now),
(146,@m5,'TPE.MET.KH.26.0064','Thuyết trình giải pháp xưởng 2S Đà Nẵng',@now,@now),
(138,@m7,'TPE.MET.NB.26.0066','Rà soát báo giá dự án 2S Phương Anh',@now,@now);

SELECT @m1,@m2,@m3,@m4,@m5,@m6,@m7;

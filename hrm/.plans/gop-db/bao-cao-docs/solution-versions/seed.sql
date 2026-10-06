START TRANSACTION;
INSERT INTO solutions (id,request_solution_id,pm_id,prospective_project_id,code,status,has_modules,progress_percent,end_date,current_version_id,current_version_code,name,company_id,department_id,created_by,updated_by,created_at,updated_at) VALUES
(951,NULL,835,130,'HN_DA.UD.0137.2026.DA013_GP951',7,1,40,'2026-10-20',952,2,'Giải pháp trang bị xưởng thực hành ô tô – Trường Đại học Quy Nhơn',1,55,835,835,'2026-09-14 08:30:00','2026-10-01 08:30:00'),
(952,NULL,987,133,'HN_DA.UD.0129.2026.DA016_GP952',9,1,30,'2026-10-15',953,1,'Giải pháp mô hình dạy học nghề Điện tử công nghiệp – Trường CĐ Công nghệ và Nông Lâm Đông Bắc',1,51,987,987,'2026-10-01 09:00:00','2026-10-01 09:00:00');
INSERT INTO solution_versions (id,solution_id,code,description,start_date,end_date,status,completion_date,approved_at,progress_percent,created_by,updated_by,created_at,updated_at) VALUES
(951,951,'1','Phiên bản đầu theo khảo sát hiện trạng','2026-09-14','2026-09-25',11,'2026-09-25','2026-09-26 16:30:00',100,835,835,'2026-09-14 08:30:00','2026-09-26 16:30:00'),
(952,951,'2','Bổ sung danh mục đồng sơn theo góp ý của nhà trường','2026-10-01','2026-10-20',7,NULL,NULL,20,835,835,'2026-10-01 08:30:00','2026-10-01 08:30:00'),
(953,952,'1',NULL,'2026-10-01','2026-10-15',9,NULL,NULL,30,987,987,'2026-10-01 09:00:00','2026-10-01 09:00:00');
INSERT INTO solution_modules (id,solution_id,code,project_item_id,project_item_name,open,leader_id,status,current_version_id,current_version_code,approved_at,due_date,note,created_by,updated_by,company_id,department_id,part_id,created_at,updated_at,weight,progress_percent) VALUES
(951,951,'HN_DA.UD.0137.2026.DA013_GP951_HM01',1,'Xây dựng danh mục thiết bị',1,835,2,NULL,2,'2026-09-14','2026-10-20','Danh mục thiết bị chẩn đoán, cầu nâng, đồng sơn',835,835,1,55,NULL,'2026-09-14 08:30:00','2026-09-14 08:30:00',0,0),
(952,951,'HN_DA.UD.0137.2026.DA013_GP951_HM02',2,'Ốp bản vẽ móng máy',1,1142,2,NULL,2,'2026-09-14','2026-10-20','Bản vẽ bố trí, móng cầu nâng và khí nén',835,835,1,55,NULL,'2026-09-14 08:30:00','2026-09-14 08:30:00',0,0),
(953,952,'HN_DA.UD.0129.2026.DA016_GP952_HM01',1,'Xây dựng danh mục thiết bị',1,987,2,NULL,1,'2026-10-01','2026-10-15','Danh mục mô hình điện tử công nghiệp',987,987,1,51,11,'2026-10-01 09:00:00','2026-10-01 09:00:00',0,0);
INSERT INTO solution_version_members (id,solution_id,solution_version_id,solution_module_id,member_id,member_name,role,module_name,created_at,updated_at) VALUES
(951,951,951,NULL,835,'Vũ Quang Minh','PM',NULL,NOW(),NOW()),
(952,951,951,952,1142,'Trần Văn Sơn','Leader hạng mục','Ốp bản vẽ móng máy',NOW(),NOW()),
(953,951,951,951,149,'Bùi Thị Mai','Thành viên','Xây dựng danh mục thiết bị',NOW(),NOW()),
(954,951,952,NULL,835,'Vũ Quang Minh','PM',NULL,NOW(),NOW()),
(955,951,952,952,1142,'Trần Văn Sơn','Leader hạng mục','Ốp bản vẽ móng máy',NOW(),NOW()),
(956,951,952,951,781,'Đào Phúc Sơn','Thành viên','Xây dựng danh mục thiết bị',NOW(),NOW()),
(957,952,953,NULL,987,'Hà Mạnh Cường','PM',NULL,NOW(),NOW()),
(958,952,953,953,341,'Thiều Quốc Đạt','Leader hạng mục','Xây dựng danh mục thiết bị',NOW(),NOW());
INSERT INTO tasks (id,solution_id,solution_version_id,solution_version_code,solution_module_id,project_id,code,task_type,title,priority,status,progress_pct,start_date,due_date,due_time,assignee_id,created_by,updated_by,approver_id,completed_at,created_at,updated_at,mode,progress_percent,estimated_hours,weight) VALUES
(951,951,951,'1',951,130,'TPE.TASK.NB.26.0951',2,'Khảo sát hiện trạng xưởng thực hành ô tô',1,8,100,'2026-09-14','2026-09-16','17:00:00',835,835,835,835,'2026-09-16 17:00:00','2026-09-14 08:40:00','2026-09-16 17:00:00',2,100,16,0),
(952,951,951,'1',951,130,'TPE.TASK.NB.26.0952',2,'Lập danh mục thiết bị chẩn đoán, cầu nâng',1,8,100,'2026-09-15','2026-09-19','17:00:00',149,835,835,835,'2026-09-19 17:00:00','2026-09-14 08:45:00','2026-09-19 17:00:00',2,100,24,0),
(953,951,951,'1',952,130,'TPE.TASK.NB.26.0953',2,'Ốp bản vẽ bố trí cầu nâng và móng máy',1,8,100,'2026-09-18','2026-09-25','17:00:00',1142,835,835,835,'2026-09-25 17:00:00','2026-09-14 08:50:00','2026-09-25 17:00:00',2,100,32,0),
(954,951,952,'2',951,130,'TPE.TASK.NB.26.0954',2,'Bổ sung danh mục thiết bị đồng sơn theo góp ý nhà trường',2,4,20,'2026-10-01','2026-10-16','17:00:00',835,835,835,835,NULL,'2026-10-01 08:40:00','2026-10-02 08:00:00',2,20,64,0),
(955,951,952,'2',952,130,'TPE.TASK.NB.26.0955',2,'Cập nhật bản vẽ mặt bằng xưởng theo version 2',1,4,10,'2026-10-01','2026-10-20','17:00:00',1142,835,835,835,NULL,'2026-10-01 08:45:00','2026-10-02 08:00:00',2,10,72,0),
(956,951,952,'2',951,130,'TPE.TASK.NB.26.0956',2,'Lập dự toán chi phí lắp đặt thiết bị',1,3,0,'2026-10-05','2026-10-20','17:00:00',781,835,835,835,NULL,'2026-10-01 08:50:00','2026-10-01 08:50:00',2,0,40,0),
(957,951,952,'2',951,130,'TPE.TASK.NB.26.0957',2,'Chốt yêu cầu kỹ thuật bổ sung với nhà trường',3,4,50,'2026-09-29','2026-10-01','17:00:00',835,835,835,835,NULL,'2026-09-29 08:30:00','2026-09-30 17:00:00',2,50,12,0),
(958,951,952,'2',952,130,'TPE.TASK.NB.26.0958',2,'Rà soát hồ sơ giải pháp version 2 trước khi gửi duyệt',1,4,30,'2026-10-02','2026-10-02','17:00:00',148,835,835,835,NULL,'2026-10-01 09:00:00','2026-10-02 08:00:00',2,30,4,0),
(959,951,952,'2',951,130,'TPE.TASK.NB.26.0959',2,'Lập bảng so sánh cấu hình thiết bị của 3 hãng',1,3,0,'2026-10-05','2026-10-30','17:00:00',835,835,835,835,NULL,'2026-10-01 09:10:00','2026-10-01 09:10:00',2,0,96,0),
(960,951,952,'2',952,130,'TPE.TASK.NB.26.0960',2,'Bóc tách khối lượng vật tư lắp đặt khí nén',1,3,0,'2026-10-12','2026-10-28','17:00:00',1142,835,835,835,NULL,'2026-10-01 09:15:00','2026-10-01 09:15:00',2,0,48,0),
(961,952,953,'1',953,133,'TPE.TASK.NB.26.0961',2,'Xây dựng danh mục mô hình điện tử công nghiệp',1,4,25,'2026-10-01','2026-10-12','17:00:00',341,987,987,987,NULL,'2026-10-01 09:20:00','2026-10-02 08:00:00',2,25,40,0),
(962,952,953,'1',953,133,'TPE.TASK.NB.26.0962',2,'Thiết kế bản vẽ bố trí phòng thực hành điện tử',1,4,10,'2026-10-02','2026-10-15','17:00:00',987,987,987,987,NULL,'2026-10-01 09:25:00','2026-10-02 08:00:00',2,10,48,0);
INSERT INTO task_result_progress_logs (id,task_id,report_date,hours,progress_pct,note,created_at,updated_at) VALUES
(951,951,'2026-09-14',8,50,'Khảo sát khu cầu nâng, đồng sơn',NOW(),NOW()),
(952,951,'2026-09-15',9,100,'Hoàn thành biên bản khảo sát',NOW(),NOW()),
(953,952,'2026-09-15',6,25,NULL,NOW(),NOW()),
(954,952,'2026-09-16',8,60,NULL,NOW(),NOW()),
(955,952,'2026-09-17',6,85,NULL,NOW(),NOW()),
(956,952,'2026-09-18',6,100,NULL,NOW(),NOW()),
(957,953,'2026-09-21',8,30,NULL,NOW(),NOW()),
(958,953,'2026-09-22',8,60,NULL,NOW(),NOW()),
(959,953,'2026-09-23',8,85,NULL,NOW(),NOW()),
(960,953,'2026-09-24',6,100,NULL,NOW(),NOW()),
(961,954,'2026-10-01',8,10,NULL,NOW(),NOW()),
(962,954,'2026-10-02',7,20,NULL,NOW(),NOW()),
(963,955,'2026-10-01',6,10,NULL,NOW(),NOW()),
(964,957,'2026-09-30',4,50,NULL,NOW(),NOW()),
(965,961,'2026-10-01',7,15,NULL,NOW(),NOW()),
(966,961,'2026-10-02',8,25,NULL,NOW(),NOW()),
(967,962,'2026-10-02',6,10,NULL,NOW(),NOW());
COMMIT;

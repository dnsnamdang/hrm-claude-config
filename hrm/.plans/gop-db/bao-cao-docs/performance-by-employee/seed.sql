-- Dữ liệu mẫu cho SRS Báo cáo hiệu suất (theo dự án + theo giải pháp). Chỉ INSERT, không sửa dữ liệu cũ.
SET @now = '2026-10-02 08:00:00';
-- ===== 2 dự án TKT (copy cấu trúc dự án id 113) =====
DROP TEMPORARY TABLE IF EXISTS t_pp;
CREATE TEMPORARY TABLE t_pp AS SELECT * FROM prospective_projects WHERE id = 113;
UPDATE t_pp SET id = 0, code = 'HN_DA.UD.0137.2026.DA020',
  name = 'Cung cấp thiết bị thực hành điện – điện tử cho Trường CĐ Kỹ thuật Công nghiệp Bắc Giang',
  start_date = '2026-10-01', status = 4, created_at = @now, updated_at = @now;
INSERT INTO prospective_projects SELECT * FROM t_pp; SET @p1 = LAST_INSERT_ID();
UPDATE t_pp SET code = 'HN_DA.UD.0137.2026.DA021',
  name = 'Trang bị xưởng thực hành ô tô – Trường CĐ nghề Việt Xô số 1',
  start_date = '2026-10-02', status = 9;
INSERT INTO prospective_projects SELECT * FROM t_pp; SET @p2 = LAST_INSERT_ID();

-- ===== 2 yêu cầu làm giải pháp (copy id 15) =====
DROP TEMPORARY TABLE IF EXISTS t_rs;
CREATE TEMPORARY TABLE t_rs AS SELECT * FROM request_solutions WHERE id = 15;
UPDATE t_rs SET id = 0, code = 'TPE.YCP.TC.26.0091', project_key = @p1, receive_dept = 55, pm_id = 781,
  title = 'Yêu cầu lên giải pháp thiết bị thực hành điện – điện tử Trường CĐ KTCN Bắc Giang', created_at = @now, updated_at = @now;
INSERT INTO request_solutions SELECT * FROM t_rs; SET @rs1 = LAST_INSERT_ID();
UPDATE t_rs SET code = 'TPE.YCP.TC.26.0092', project_key = @p2, pm_id = 149,
  title = 'Yêu cầu lên giải pháp xưởng thực hành ô tô Trường CĐ nghề Việt Xô số 1';
INSERT INTO request_solutions SELECT * FROM t_rs; SET @rs2 = LAST_INSERT_ID();

-- ===== 2 giải pháp (copy id 24) =====
DROP TEMPORARY TABLE IF EXISTS t_s;
CREATE TEMPORARY TABLE t_s AS SELECT * FROM solutions WHERE id = 24;
UPDATE t_s SET id = 0, code = 'HN_DA.UD.0137.2026.DA020_GP01',
  name = 'Giải pháp thiết bị thực hành điện – điện tử, PLC cho Trường CĐ KTCN Bắc Giang',
  status = 7, prospective_project_id = @p1, request_solution_id = @rs1, pm_id = 781, department_id = 55,
  created_at = @now, updated_at = @now;
INSERT INTO solutions SELECT * FROM t_s; SET @s1 = LAST_INSERT_ID();
UPDATE t_s SET code = 'HN_DA.UD.0137.2026.DA021_GP01',
  name = 'Giải pháp trang bị xưởng thực hành ô tô (chẩn đoán, cầu nâng, khí nén)',
  status = 17, prospective_project_id = @p2, request_solution_id = @rs2, pm_id = 149;
INSERT INTO solutions SELECT * FROM t_s; SET @s2 = LAST_INSERT_ID();

-- ===== 4 hạng mục (copy id 3) =====
DROP TEMPORARY TABLE IF EXISTS t_m;
CREATE TEMPORARY TABLE t_m AS SELECT * FROM solution_modules WHERE id = 3;
UPDATE t_m SET id = 0, solution_id = @s1, code = 'HN_DA.UD.0137.2026.DA020_GP01_HM01', project_item_id = 1,
  project_item_name = 'Xây dựng danh mục thiết bị', leader_id = 835, due_date = '2026-10-08', created_at = @now, updated_at = @now;
INSERT INTO solution_modules SELECT * FROM t_m; SET @m1 = LAST_INSERT_ID();
UPDATE t_m SET code = 'HN_DA.UD.0137.2026.DA020_GP01_HM02', project_item_id = 2, project_item_name = 'Ốp bản vẽ móng máy', leader_id = 1142;
INSERT INTO solution_modules SELECT * FROM t_m; SET @m2 = LAST_INSERT_ID();
UPDATE t_m SET solution_id = @s2, code = 'HN_DA.UD.0137.2026.DA021_GP01_HM01', project_item_id = 1, project_item_name = 'Xây dựng danh mục thiết bị', leader_id = 781;
INSERT INTO solution_modules SELECT * FROM t_m; SET @m3 = LAST_INSERT_ID();
UPDATE t_m SET code = 'HN_DA.UD.0137.2026.DA021_GP01_HM02', project_item_id = 2, project_item_name = 'Ốp bản vẽ móng máy', leader_id = 148;
INSERT INTO solution_modules SELECT * FROM t_m; SET @m4 = LAST_INSERT_ID();

INSERT INTO solution_module_members (solution_module_id, member_id, project_role_id, project_role_name, created_at, updated_at) VALUES
 (@m1, 148, 3, 'Kỹ sư thiết kế cơ khí', @now, @now),
 (@m2, 149, 4, 'Kỹ sư thiết kế điện', @now, @now),
 (@m3, 835, 3, 'Kỹ sư thiết kế cơ khí', @now, @now),
 (@m4, 126, 6, 'Kỹ sư công trường', @now, @now);

-- ===== 10 nhiệm vụ (copy id 10) =====
DROP TEMPORARY TABLE IF EXISTS t_t;
CREATE TEMPORARY TABLE t_t AS SELECT * FROM tasks WHERE id = 10;
DROP TEMPORARY TABLE IF EXISTS t_def;
CREATE TEMPORARY TABLE t_def (n INT, code VARCHAR(50), title VARCHAR(255), st INT, asg BIGINT, prj BIGINT, sol BIGINT, mdl BIGINT,
  sd DATE, dd DATE, cmp DATETIME, est DECIMAL(8,2), act DECIMAL(8,2));
INSERT INTO t_def VALUES
 (1,'TPE.TASK.NB.26.0901','Khảo sát hiện trạng xưởng thực hành điện – điện tử',8,835,@p1,@s1,@m1,'2026-10-01','2026-10-02','2026-10-01 16:30:00',8,7),
 (2,'TPE.TASK.NB.26.0902','Lập danh mục thiết bị thực hành điện cơ bản',8,835,@p1,@s1,@m1,'2026-10-01','2026-10-02','2026-10-02 10:00:00',16,18),
 (3,'TPE.TASK.NB.26.0903','Lập danh mục thiết bị PLC và tự động hóa',4,148,@p1,@s1,@m1,'2026-10-02','2026-10-08',NULL,16,6),
 (4,'TPE.TASK.NB.26.0904','Ốp bản vẽ bố trí thiết bị phòng điện tử',8,1142,@p1,@s1,@m2,'2026-10-01','2026-10-01','2026-10-02 09:15:00',12,15),
 (5,'TPE.TASK.NB.26.0905','Bóc tách khối lượng tủ điện, máng cáp',4,149,@p1,@s1,@m2,'2026-10-01','2026-10-01',NULL,10,4),
 (6,'TPE.TASK.NB.26.0906','Xây dựng danh mục thiết bị chẩn đoán ô tô',8,781,@p2,@s2,@m3,'2026-10-02','2026-10-03','2026-10-02 11:00:00',20,16),
 (7,'TPE.TASK.NB.26.0907','Xây dựng danh mục cầu nâng, thiết bị gầm',6,835,@p2,@s2,@m3,'2026-10-02','2026-10-03','2026-10-02 15:00:00',12,12),
 (8,'TPE.TASK.NB.26.0908','Ốp bản vẽ móng cầu nâng 2 trụ',8,148,@p2,@s2,@m4,'2026-10-02','2026-10-01','2026-10-02 08:30:00',8,10),
 (9,'TPE.TASK.NB.26.0909','Khảo sát mặt bằng xưởng thực hành ô tô',8,126,@p2,@s2,@m4,'2026-10-01','2026-10-02','2026-10-01 17:00:00',6,5),
 (10,'TPE.TASK.NB.26.0910','Bản vẽ hệ thống khí nén xưởng',4,126,@p2,@s2,@m4,'2026-10-02','2026-10-09',NULL,10,3);
INSERT INTO tasks
 SELECT 0, d.sol, d.sol, t.solution_version_code, d.mdl, d.mdl, t.module_version_code, d.prj, NULL, NULL, NULL, NULL,
  d.code, t.task_type, NULL, d.title, NULL, 1, d.st, IF(d.cmp IS NULL, 40, 100), d.sd, d.dd, '17:00:00', d.asg, d.asg, d.asg, NULL,
  d.cmp, @now, COALESCE(d.cmp, @now), t.mode, NULL, d.act, IF(d.cmp IS NULL, 40, 100), NULL, d.est, NULL, d.cmp, IF(d.cmp IS NULL, NULL, d.asg), NULL, 0
 FROM t_def d CROSS JOIN t_t t ORDER BY d.n;
INSERT INTO task_result_progress_logs (task_id, report_date, hours, progress_pct, note, created_at, updated_at)
 SELECT tk.id, DATE(COALESCE(d.cmp, '2026-10-02')), d.act, IF(d.cmp IS NULL, 40, 100), 'Báo cáo tiến độ', @now, @now
 FROM t_def d JOIN tasks tk ON tk.code = d.code COLLATE utf8mb4_unicode_ci;
SELECT @p1 p1, @p2 p2, @rs1 rs1, @rs2 rs2, @s1 s1, @s2 s2, @m1 m1, @m2 m2, @m3 m3, @m4 m4;
SELECT id, code FROM tasks WHERE code LIKE 'TPE.TASK.NB.26.09%';

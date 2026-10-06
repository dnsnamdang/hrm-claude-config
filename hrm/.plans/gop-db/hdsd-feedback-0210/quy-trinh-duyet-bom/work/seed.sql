SET @pc='HN_DA.UD.0137.2026.DA091';
CREATE TEMPORARY TABLE tp AS SELECT * FROM prospective_projects WHERE id=148;
UPDATE tp SET id=0, code=@pc, name='Cung cấp thiết bị thực hành khí nén – thủy lực cho Trường CĐ Cơ giới và Thủy lợi',
 project_description='Khách hàng cần danh mục thiết bị và BOM để trình Ban giám hiệu', status=4, closed_reason_id=NULL, closed_at=NULL, closed_by=NULL,
 main_sale_employee_id=13, created_by=13, updated_by=13, created_at=NOW(), updated_at=NOW(), start_date=CURDATE(), end_date=DATE_ADD(CURDATE(), INTERVAL 60 DAY),
 customer_need_solution_date=DATE_ADD(CURDATE(), INTERVAL 30 DAY), internal_solution_close_date=DATE_ADD(CURDATE(), INTERVAL 25 DAY);
INSERT INTO prospective_projects SELECT * FROM tp;
SET @pp=LAST_INSERT_ID();
CREATE TEMPORARY TABLE ts AS SELECT * FROM solutions WHERE id=33;
UPDATE ts SET id=0, request_solution_id=NULL, pm_id=13, prospective_project_id=@pp, code=CONCAT(@pc,'_GP01'),
 name='Giải pháp thiết bị thực hành khí nén – thủy lực cho Trường CĐ Cơ giới và Thủy lợi', status=7, has_modules=1,
 end_date=DATE_ADD(CURDATE(), INTERVAL 25 DAY), current_version_id=NULL, current_version_code=1, created_by=13, updated_by=13, created_at=NOW(), updated_at=NOW();
INSERT INTO solutions SELECT * FROM ts;
SET @s=LAST_INSERT_ID();
INSERT INTO solution_versions (solution_id,code,start_date,end_date,status,progress_percent,created_by,updated_by,created_at,updated_at)
 VALUES (@s,1,CURDATE(),DATE_ADD(CURDATE(), INTERVAL 25 DAY),7,0,13,13,NOW(),NOW());
SET @sv=LAST_INSERT_ID();
UPDATE solutions SET current_version_id=@sv WHERE id=@s;
CREATE TEMPORARY TABLE tm AS SELECT * FROM solution_modules WHERE id=6;
UPDATE tm SET id=0, solution_id=@s, code=CONCAT(@pc,'_GP01_HM01'), project_item_id=1, project_item_name='Xây dựng danh mục thiết bị',
 leader_id=13, status=2, current_version_id=NULL, current_version_code=1, approved_at=CURDATE(), due_date=DATE_ADD(CURDATE(), INTERVAL 20 DAY),
 created_by=13, updated_by=13, created_at=NOW(), updated_at=NOW();
INSERT INTO solution_modules SELECT * FROM tm;
SET @m=LAST_INSERT_ID();
INSERT INTO solution_module_versions (solution_module_id,solution_version_id,code,start_date,end_date,status,weight,progress_percent,created_by,updated_by,created_at,updated_at)
 VALUES (@m,@sv,1,CURDATE(),DATE_ADD(CURDATE(), INTERVAL 20 DAY),2,0,0,13,13,NOW(),NOW());
SET @mv=LAST_INSERT_ID();
UPDATE solution_modules SET current_version_id=@mv WHERE id=@m;
SELECT @pp pp, @s s, @sv sv, @m m, @mv mv;

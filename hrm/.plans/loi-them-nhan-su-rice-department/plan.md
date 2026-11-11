# Lỗi thêm nhân sự vào phòng ban "BAN GIÁM ĐỐC" – rice_department_id null (Redmine: chưa có số) — @cuong61n

## Bối cảnh
CTCP đầu tư tập đoàn ETEK báo: thêm nhân sự vào phòng Ban giám đốc báo lỗi `1048 Column 'rice_department_id' cannot be null` (update `rice_employee_infos` id=20, department_id=119).

## Tasks
- [x] (11/11/2026) Điều tra nguyên nhân: phòng ban 119 thuộc công ty 8 (rice_company 13) nhưng dòng `rice_departments` id 111 mang rice_company_id=1/company_id=1 (tạo 31/01/2026 khi phòng ban còn thuộc công ty khác). Hook lưu nhân sự `EmployeeInfo.php` tìm theo (department_id, rice_company_id=13) → null → ghi null vào cột NOT NULL.
- [x] (11/11/2026) Rà prod (chỉ đọc) 103 phòng ban: 1 lệch công ty (119), 11 phòng ban đã khoá thiếu dòng rice_departments (48,62,63,78,89,91,97,99,101,102,104), 8 phòng ban thuộc công ty 5/6/7 chưa có rice_company. Không nhân sự nào đang trỏ phòng ban cơm sai công ty.
- [x] (11/11/2026) Sửa dữ liệu PROD: `rice_departments` id 111 → rice_company_id=13, company_id=8 (UPDATE có WHERE khớp giá trị cũ, 1 dòng, đã kiểm lại).
- [x] (11/11/2026) Sửa code `hrm-api/Modules/Human/Entities/EmployeeInfo.php` (hook saved): công ty chưa có rice_company thì thoát êm; phòng ban chưa có dòng phòng ban cơm thì tự tạo; kiểm null `department`. Đã `php -l`. Nhánh `develop`, chưa commit.
- [x] (11/11/2026) Commit e726a743c lên nhánh `gop_db` (hrm-api, chỉ 1 file) và deploy PROD bằng ~/build_tpe.sh: pull fast-forward, không có migration, route cache OK, FE không đổi nên không build. Đã kiểm file trên prod có bản mới.
- [ ] Chờ: ETEK test thêm nhân sự vào BAN GIÁM ĐỐC trên prod.

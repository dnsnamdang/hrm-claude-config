# Fix nhân sự chọn nhầm bộ phận của phòng ban khác (@namdangit) — nhánh `tpe`

- [x] BE: seeder `Modules/Human/Database/Seeders/FixEmployeeInfoPartMismatchSeeder.php` — gán lại `employee_infos.part_id` sang bộ phận trùng tên trong đúng phòng ban, hỗ trợ `SEED_DRY_RUN=1`
- [x] FE: `EmployeeInfoForm.vue` — `onSelectWorkingHistoryDepartment` gọi `getParts()` ghi đè list Bộ phận chính; `getTeams` đẩy team vào `listParts`; `mounted` gọi `getParts()` không tham số 
- [x] BE: `CreateEmployeeInfoRequest` chưa có rule `part_id` phải thuộc `department_id` 

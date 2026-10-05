# Plan — Trưởng phòng / trưởng bộ phận lệch người sau gộp DB

## Phase 1 — BE
- [x] Cast `app/Casts/EmployeeIdAsInfoIdCast.php` (cache map employees.id ⇄ employee_info_id theo request)
- [x] Gắn cast `department_lead_id` cho `Modules/Human/Entities/Department`, `Modules/Timesheet/Entities/Department`, `app/Models/Department`
- [x] Gắn cast `part_lead_id` cho `Modules/Human/Entities/Part`, `Modules/Timesheet/Entities/Part`, `app/Models/Part`
- [x] `IssueService::notifyHandlingDepartmentLead` (DB::table) quy đổi sang employee_info_id
- [x] Rà lại các chỗ đọc/ghi còn lại (CompanyService, OvertimeRequirement, Decision, CRM sync, AuthNew) chạy qua model
- [x] Rule request `CreateDepartmentRequest`/`CreatePartRequest`: trưởng đơn vị phải có tài khoản (controller bắt Exception chung nên không để cast ném 422)
- [x] Migration `2026_09_25_000003_convert_lead_ids_to_employee_id`: Etek Green (cty 9) 15 phòng + 61 bộ phận đang lưu employee_infos.id -> employees.id
- [x] Test trên DB PROD trong transaction + rollback: phòng 88/88, bộ phận 81/81 đúng; sơ đồ HN_KD1/KD2/NSHC đúng người; ghi hồ sơ 17 -> lưu 24; chặn người chưa có tài khoản
- [x] Deploy PROD 25/09 12:0x: `484ee95fd` (cast+migration, phiên khác commit hộ) + `32246d20c` (9 file) lên `gop_db`, `git pull` + `migrate` trên /var/www/tpe/hrm-api; backup cột trước migrate: scratchpad `backup_lead_ids_before_migrate.txt`
- [x] Verify PROD sau migrate: 0 giá trị lệch nghĩa; API companyStruct TPE (user 759) + Etek Green (user 1192) ra đúng trưởng phòng; log không lỗi mới
- [ ] Ghi chú: HN_TBCN trống tiêu đề do title_id=55 không tồn tại (có từ trước, không thuộc task)

## Phase 2 — Dữ liệu
- [x] Danh sách 14 phòng ERP ghi khác HRM cũ (đo lại sau fix; 10 phòng HRM cũ để trống) — gửi nghiệp vụ chốt
- [ ] Tồn đọng: `config/company_migration.php` map `department_lead_id`/`part_lead_id` = `OWNED:employee_infos` -> lần di trú công ty sau sẽ lại ghi id hồ sơ; cần bước đổi sang employees.id (hỏi user trước, service dùng chung)

## Phase 3 — Sơ đồ cơ cấu tổ chức sai sau gộp (30/09)
- [x] Đối chiếu hrm_erp_gop vs hrm_production: code companyStruct đúng, lệch do bảng ERP đè dữ liệu HRM
- [x] Migration `2026_09_30_000001_restore_hrm_org_struct_after_merge`: trả status phòng 48/81, công ty phòng 119, parent công ty 8, position 17 phòng, trưởng phòng 77/98/120/121 + bộ phận 15/17/24 theo HRM cũ; ngừng phòng ERP 113/123 (chỉ ghi khi giá trị hiện tại còn như lúc khảo sát)
- [x] Chạy thử trên DB PROD trong transaction + rollback: 30/30 dòng đổi, chạy lần 2 bỏ qua hết, sơ đồ đúng
- [x] Commit `d638629bb` + push gop_db, deploy PROD 30/09 15:24 (`git pull` + `migrate`): 30/30 ô đổi, 0 bỏ qua; so hrm_production còn 0 phòng lệch status/company/position

### Checkpoint — 2026-09-25 11:10
Vừa hoàn thành: BE cast + request rule + IssueService + migration dữ liệu, test trên PROD (rollback) đạt
Đang làm dở: không — ĐÃ DEPLOY PROD
Bước tiếp theo: nghiệp vụ chốt 14 phòng lệch người; quyết định có sửa company_migration không
Blocked: 

- [x] Sơ đồ theo công ty đang chọn: `CompanyService::companyStruct` lấy `current_company_role` thay cho `info->company` (test PROD rollback: role 9 → Etek Green, role 4 → TPSG)
- [ ] Commit + push + deploy PROD

### Checkpoint — 2026-09-30 15:25
Vừa hoàn thành: Phase 3 — trả lại cơ cấu tổ chức HRM bị ERP đè, đã deploy PROD
Đang làm dở: không
Bước tiếp theo: (tuỳ chọn) gán chức danh cho các phòng đang trống tên trưởng phòng (Phòng Kế hoạch, CN Hải Phòng, CN Vinh…)
Blocked: 

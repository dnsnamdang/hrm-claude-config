# Phase 0 — Catalog & Classification (read-only survey)

> Đo từ DB nguồn `local_hrm_green` (chỉ 1 công ty, `company_id=1`) và đích `hrm_prod_local`, ngày 2026-06-18.
> Nhiệm vụ CHỈ ĐỌC — không ghi/sửa DB. Số dòng = `COUNT(*)` thực tế.
> MySQL 8.0.42. Nguồn 609 bảng, đích 619 bảng.

## 0. Phát hiện then chốt (đọc trước khi duyệt)

1. **Nhiều bảng tổ chức có cột `company_id` nhưng để `NULL`** (không filter được theo `company_id=1`): `roles`, `titles`(67), `working_positions`(10), `working_position_ranks`(10), `working_position_groups`(5), `rank_competency`(39), `ranks`(6), `rank_groups`(6). `devices` có 74 NULL + 169 ở company 1. → Vì nguồn CHỈ có 1 công ty, các bảng này thực chất thuộc công ty 1. **Filter phải là `company_id = 1 OR company_id IS NULL`** và khi chèn set `company_id = target`. → CẦN NGƯỜI DUYỆT (xem §A).
2. **`created_by` / `updated_by` trỏ tới `employees`** (tài khoản đăng nhập), KHÔNG phải `employee_infos`. Kiểm chứng: `employee_infos.created_by` khớp `employees.id` 124/124; `departments.created_by` 14/14; `employee_salary_histories.created_by` 77/77. → dịch qua map `employees`.
3. **`employee_role_id` → `titles`** (KHÔNG phải ranks). Xác nhận bằng model `Modules/Human/Entities/EmployeeInfo.php:647` (`belongsTo(Title::class,'employee_role_id')`), data khớp titles 122/122.
4. **`direct_manager_id`: model khai `Employee::class` nhưng DATA khớp `employee_infos` 90/90** (khớp employees chỉ 80/90). → đề xuất dịch qua map `employee_infos`. CẦN DUYỆT (model vs data mâu thuẫn) — xem §A.
5. **JSON nhúng id nhân sự**: `groups.group_assistants` = `[{"id":41,"text":"EG-040-..."}]` (id 41 = `employee_infos.id`); `departments.department_assistants` = `[{"id":1,...}]`, `departments.working_position_order` (json). → các id trong JSON này KHÔNG được dịch tự động qua FK thường → **rủi ro trỏ sai nếu bỏ qua**. CẦN DUYỆT cách xử lý (dịch id trong JSON hay chấp nhận lệch). Xem §A.
6. **`files` nguồn RỖNG (0 dòng)** → không migrate files. Ảnh nhân viên là cột path string trên `employee_infos` (`image`, `face_image_url`, `id_images`, `passport_images`, `health_certification_file`) — ví dụ `/uploads/...jpg` và `https://tanphat.s3...jpg` → GIỮ NGUYÊN (chung bucket).
7. **Email đụng đích: `namdangit@gmail.com`** ở cả `employees` và `employee_infos` → D6: bỏ qua người này (+ mọi bản con).
8. **`companies.name` đụng**: đích id=7 = "CÔNG TY CỔ PHẦN GIẢI PHÁP ETEK GREEN" → D9 pre-step đổi tên id=7.
9. **`employees.rice_setting_location_id`**: 103 dòng có giá trị nhưng `rice_setting_locations` RỖNG ở nguồn → dangling FK. CẦN DUYỆT (set NULL hay giữ nguyên). Xem §A.
10. **`employees.tp_id` rỗng** (không dòng nào có giá trị) → giữ NULL.
11. **`employee_has_roles.model_type`** = `Modules\Timesheet\Entities\Employee` (giữ nguyên).
12. **`conn_infos.machine_type_id`** không có bảng `machine_types` → là hằng số (giá trị 2) → GIỮ NGUYÊN.

---

## 1. Nhóm SHARED (global — KHÔNG chèn, map id nguồn → id đích)

> CẬP NHẬT 2026-06-18: bỏ map theo `code`. Mỗi bảng có CHIẾN LƯỢC riêng, xác minh
> bằng đối soát THẬT (local_hrm_green → hrm_prod_local).

| Bảng | Strategy | Kết quả đối soát thật | Ghi chú |
|---|---|---|---|
| nations | `id_identity` | 3/3 (id+name) | id trùng IDENTITY giữa 2 DB |
| provinces | `id_identity` | 44/44 (id+name) | cha = nation_id |
| districts | `id_identity` | 712/712 (692 id+name, **20 id+name-lệch**) | đích **THIẾU cột `code`** → buộc map theo id; cha = province_id |
| wards | `id_identity` | 13463/13463 (id+name) | cha = district_id |
| banks | `name` (normalize NFC + trim + lower) | **5/12** khớp, 7 lệch tên | id 2 DB KHÁC nhau hẳn (0 khớp identity) → map theo TÊN; 7 bank còn lại khác cách viết tên (TMCP vs Thương mại Cổ phần…) → cần alias tay nếu công ty dùng |
| majors | `name` | 0/0 | RỖNG ở nguồn; vẫn để map phòng xa |
| areas | `name` | 0/0 | RỖNG ở nguồn |
| permissions | `tuple` `(name, guard_name)` | 580/580 | map identity, không chèn |
| ~~system_salary_compositions~~ | `unused` | — (không build) | **KHÔNG có cột FK `*_system_salary_composition_id` nào trỏ tới** (chỉ có cờ boolean `salary_compositions.is_system_salary_composition`) → bỏ qua, KHÔNG cảnh báo |

**Chiến lược `id_identity` (địa lý) — 3 tầng:**
1. id nguồn CÓ ở đích + name khớp → map theo id (`matched_id`).
2. id nguồn CÓ ở đích nhưng name LỆCH → vẫn map theo id (`matched_id_diff_name`). id là định danh tin cậy; name chỉ bị format lại. VD HCM: src "Quận 1".."Quận 12" (id 10–21) ↔ đích "1".."12" cùng id 10–21; và "Cư M'gar"→"Cư M gar", "Huyện Cai Lậy"→"Cai Lậy".
3. id nguồn KHÔNG có ở đích → fallback (name chuẩn hóa + parent_id ĐÍCH qua map cha đã dựng). Thực tế ETEK GREEN: 0 dòng rơi vào fallback (toàn bộ id đều có ở đích).

**Thứ tự build địa lý:** nations → provinces → districts → wards (fallback con cần map cha).

**Chuẩn hóa Unicode (NFC):** 2 DB lưu dấu tiếng Việt khác form (NFD tổ hợp vs NFC dựng sẵn) → cùng chữ khác byte. `normalizeNaturalKey` chuẩn hóa NFC trước khi so (recover bank "Ngoại Thương" ↔ "Ngoại thương").

> Không phát hiện bảng `*_types`/danh mục global khác được FK của bảng OWNED trỏ tới. Các `*_types` (insurance_types, attachment_types, reward_types...) đều CÓ `company_id` → là OWNED (xem §3 / §A).

---

## 2. Nhóm OWNED-SKIP (giao dịch theo kỳ — BỎ)

Số dòng = COUNT(*) company_id=1 (hoặc tổng):

| Bảng | Dòng | Bảng | Dòng |
|---|---|---|---|
| timesheets | 90282 | shift_detail_employee_dates | 54690 |
| overtime_assignments | 5329 | overtime_assignment_cost_allocations | 3894 |
| request_update_timesheet | 1748 | job_assignment_employees | 1032 |
| attendances | 915 | job_assignment_note_details | 783 |
| job_assignment_notes | 782 | admin_request_update_workings | 247 |
| applications | 221 | business_trip_employees | 136 |
| other_income_composition_employees | 132 | other_deduction_composition_employees | 117 |
| shift_detail_employees | 101 | other_allowance_composition_employees | 80 |
| salary_advance_employees | 63 | business_trip_working_shifts | 60 |
| business_trip_assigns | 60 | timesheet_month_summaries | 5 |
| p3_salary_employees | 8 | salary/salary_employees/salary_advances/p3_salaries | ~1-2 mỗi bảng |
| overtime_hours | 3 | operating_supports | 3 |
| employee_update_requests | 3 | assign_jobs | 2 |
| column_customizations | 2 | self_notifications | 1 |
| personal_todo_lists | 1 | overtime_requirements/...cost_allocations | 1 |

Cùng họ giao dịch (rỗng/ít, vẫn SKIP): salary_summary, salary_summary_department, salary_employee_data, distribution_*, bonus_distributions, payment_*, course_*, training_request*, evaluation_*, meeting*, project_*, prospective_*, quotations, pricing_requests, handovers, decision_* (giao dịch), insurance_register*, employee_update_requests, employee_incomes, employee_disciplines, career_progressions, capacity_frameworks, retirements, suspend/termination/appendix_labor_contracts, settlement_*, trouble_shooting_reports.

---

## 3. Nhóm OWNED-MIGRATE (cấp id mới + map) — CÓ DATA

| Bảng | Dòng | Nhóm | Filter đề xuất |
|---|---|---|---|
| companies | 1 | tổ chức (lõi) | id=1 |
| departments | 14 | tổ chức | company_id=1 |
| parts | 45 | tổ chức | company_id=1 |
| groups | 6 | tổ chức (Khối) | company_id=1 |
| titles | 67 | tổ chức | **company_id=1 OR NULL** ⚠️ |
| working_positions | 10 | tổ chức | **OR NULL** ⚠️ |
| working_position_ranks | 10 | tổ chức | **OR NULL** ⚠️ |
| working_position_groups | 5 | tổ chức | **OR NULL** ⚠️ |
| ranks | 6 | cấp bậc | **OR NULL** ⚠️ |
| rank_groups | 6 | cấp bậc | **OR NULL** ⚠️ |
| rank_competency | 39 | năng lực | **OR NULL** ⚠️ |
| competencies | 53 | năng lực | company_id=1 |
| competency_groups | 6 | năng lực | company_id=1 |
| capabilities | 1 | năng lực (khác) | company_id=1 |
| capability_groups | 4 | năng lực (khác) | company_id=1 |
| department_manpowers | 29 | định biên | company_id=1 |
| department_manpower_positions | 27 | định biên | qua cha (company_id=1) |
| department_manpower_position_ranks | 27 | định biên | qua cha |
| department_manpower_position_competencies | 157 | định biên | qua cha |
| employee_manage_departments | 16 | quản lý phòng | company_id=1 |
| employee_infos | 124 | hồ sơ NV (lõi) | company_id=1 (bỏ email đụng) |
| employee_educations | 19 | hồ sơ con | qua employee_info_id |
| employee_relationships | 11 | hồ sơ con | qua employee_info_id |
| employee_bank_accounts | 4 | hồ sơ con | qua employee_info_id |
| employee_authorized_bank_accounts | 3 | hồ sơ con | qua employee_info_id |
| employee_working_histories | 87 | hồ sơ con | qua employee_info_id |
| employee_concurrently_department_has_positions | 1 | hồ sơ con | qua employee_info_id |
| employee_info_conn_infos | 53 | hồ sơ con | qua employee_info_id |
| employee_salary_histories | 77 | số dư lương | company_id=1 |
| employee_attendances | 287 | số dư phép | company_id=1 |
| salary_compositions | 49 | config lương | company_id=1 |
| salary_templates | 1 | config lương | company_id=1 |
| salary_template_compositions | 19 | config lương con | qua salary_template_id |
| insurance_configs | 1 | config BH | company_id=1 |
| holidays | 18 | config chấm công | company_id=1 |
| leave_types | 7 | config chấm công | company_id=1 |
| working_shifts | 13 | config chấm công | company_id=1 |
| shift_details | 8 | config chấm công | company_id=1 |
| late_early_outs | 6 | config chấm công | company_id=1 |
| truncated_leaves | 5 | config chấm công | company_id=1 |
| timekeeping_exemptions | 3 | config chấm công | company_id=1 |
| overtime_regulations | 1 | quy định | company_id=1 |
| overtime_companies | 1 | quy định | company_id=1 |
| attendance_watch_regulations | 1 | quy định | company_id=1 |
| general_regulations | 1 | quy định | company_id=1 |
| labor_contracts | 5 | hợp đồng NV | company_id=1 |
| locations | 78 | máy chấm công | company_id=1 |
| location_conn_infos | 5 | máy chấm công | company_id=1 |
| conn_infos | 3 | máy chấm công | company_id=1 |
| devices | 169 (+74 NULL) | máy chấm công | **company_id=1 OR NULL?** ⚠️ |
| employees | 123 | tài khoản | qua employee_info_id (bỏ email đụng) |
| company_employees | 123 | NV↔công ty | company_id=1 |
| roles | 4 | phân quyền | **company_id IS NULL (all)** ⚠️ + đổi tên (D7) |
| company_roles | 4 | phân quyền | company_id=1 |
| role_has_permissions | 1073 | phân quyền | company_id=1 |
| employee_has_roles | 25 | phân quyền | company_id=1 |
| employee_has_permissions | 0 | phân quyền | rỗng |

RỖNG ở nguồn (vẫn để trong catalog, chèn 0 dòng): salary_generals, tax_generals, insurance_generals, salary_scales, salary_scale_ranks, punishment_rules, distribution_rules(+details), allowance_policies, deduction_policies, job_positions, payroll_roles, regulation_*, assign_configs(+con), assign_benefit_rate_configs, labor_contract_types, employee_family_allowances, employee_taxs, employee_insurances, rice_*, decision_* (config), manpower_allocations, teams, rank_details, shift_detail_dates, conn_info_users, conn_info_fingers, allowance/deduction_employee_salary_histories, files, users.

---

## A. CẦN NGƯỜI DUYỆT (quyết định trước khi chạy)

1. **Filter các bảng tổ chức có `company_id` NULL** (`roles`, `titles`, `working_positions`, `working_position_ranks`, `working_position_groups`, `ranks`, `rank_groups`, `rank_competency`): xác nhận filter = `company_id=1 OR company_id IS NULL` (vì nguồn chỉ 1 công ty)? Có rủi ro nếu có dòng "rác" không thuộc công ty. → ĐỀ XUẤT: lấy tất cả (OR NULL).

2. **`devices`**: 169 dòng company 1 + 74 dòng `company_id IS NULL`. Lấy cả 74 NULL hay chỉ 169? `devices` có `employee_info_id` → có thể lọc qua employee thuộc công ty. → CÂU HỎI: filter nào?

3. **`roles` (4 dòng, company_id NULL)**: D7 yêu cầu LUÔN tạo role mới + đổi tên (hậu tố). Xác nhận lấy cả 4 role (tất cả company_id NULL) và đổi tên ra sao (vd thêm ` (EG)`).

4. **`direct_manager_id` trên employee_infos**: model khai `Employee` nhưng data khớp `employee_infos` 90/90. → ĐỀ XUẤT dịch qua map **employee_infos**. Cần duyệt (nếu thực là employees thì 10 dòng sẽ trỏ sai).

5. **JSON nhúng id**: `groups.group_assistants`, `departments.department_assistants`, `departments.working_position_order` chứa `{"id": <employee_infos.id>}`. → Có dịch id trong JSON qua map employee_infos không? Nếu KHÔNG → trỏ nhầm nhân sự công ty khác sau migrate. → ĐỀ XUẤT: viết bước hậu xử lý dịch id trong JSON (hoặc chấp nhận lệch nếu nghiệp vụ không dùng).

6. **`employees.rice_setting_location_id`** (103 dòng có giá trị, bảng `rice_setting_locations` RỖNG → dangling): set NULL khi chèn, hay giữ nguyên id? → ĐỀ XUẤT set NULL.

7. **`departments.department_id` = 4 cho TẤT CẢ 14 dòng** (khác `parent_id` là self-ref thật). Ngữ nghĩa cột `department_id` trên chính bảng departments chưa rõ (trỏ tới departments.id=4 = phòng gốc?). → cả 2 cột (`department_id`, `parent_id`) đề xuất dịch qua map departments. Cần duyệt ngữ nghĩa.

8. **Nhóm ranh giới — ĐƯA hay BỎ?** (mặc định ĐANG xếp BỎ, chờ duyệt):
   - **CRM**: `customers`(1), `customer_scopes`(59), `scopes`(19), `industries`(117), `customer_scope_groups`(0). → là danh mục/khách hàng CRM. Đưa nếu công ty mới dùng module CRM.
   - **Training**: `missions`(50), `subjects`(6), `teachers`(10), `questions`(74), `examiners`(5), `exam_kits`(7), `training_types`(2). → danh mục đào tạo (master), không phải giao dịch. Có thể nên ĐƯA.
   - **Danh mục dùng lại**: `reward_conditions`(10), `priority_levels`(4), `insurance_types`(4), `attachment_types`(8), `reward_modes`(1). → danh mục nhỏ per-company. Có thể nên ĐƯA.
   - **`missions`**: nếu là "nhiệm vụ/sứ mệnh" cấu hình → ĐƯA; nếu là công tác (giao dịch) → BỎ. Cần xác định nghiệp vụ.

---

## B. Bản đồ FK cho bảng OWNED-MIGRATE

Ký hiệu: `OWNED:x` = dịch qua `migration_id_map` bảng x. `SHARED:x(key)` = map natural-key. `GIỮ NGUYÊN` = không phải FK hoặc set cố định. `→target` = gán company_id công ty mới. ⚠️ = chưa chắc, cần duyệt.

| Bảng | Cột | Trỏ tới |
|---|---|---|
| **companies** | company_id | (chính nó — set id mới) |
| | parent_id, parent_department_id, group_id, department_id, part_id | NULL ở nguồn → GIỮ NULL |
| | deputy_id (=7), owner_id (=91) | OWNED:employee_infos ⚠️ (chỉ 1 dòng, id nằm range employee_infos) |
| | province_id(=2), district_id(=51), ward_id(=833) | SHARED:provinces/districts/wards (code) |
| | hamlet_id | NULL → GIỮ NULL |
| | created_by, updated_by | OWNED:employees |
| **departments** | company_id | →target |
| | department_id (=4 all), parent_id | OWNED:departments (self-ref) ⚠️ ngữ nghĩa |
| | group_id | OWNED:groups (vòng) |
| | part_id | OWNED:parts |
| | department_lead_id | OWNED:employee_infos (12/12) |
| | title_id | OWNED:titles (12/14) |
| | created_by, updated_by | OWNED:employees |
| | branch_id, decision_id, department_establishment_id | NULL → GIỮ NULL |
| | department_assistants, working_position_order (JSON) | OWNED:employee_infos (id nhúng) ⚠️ |
| **parts** | company_id | →target |
| | department_id | OWNED:departments |
| | part_lead_id | OWNED:employee_infos (45/45) |
| **groups** | company_id | →target |
| | department_id | OWNED:departments (vòng) |
| | manager_info_id | OWNED:employee_infos (4/4) |
| | part_id | OWNED:parts |
| | created_by, updated_by | OWNED:employees |
| | group_assistants (JSON) | OWNED:employee_infos (id nhúng) ⚠️ |
| **teams** | part_id | OWNED:parts (rỗng) |
| **titles** | company_id | →target |
| | department_id | OWNED:departments |
| | part_id | OWNED:parts |
| | created_by, updated_by | OWNED:employees |
| **working_positions** | company_id | →target |
| | working_position_group_id | OWNED:working_position_groups |
| | created_by, updated_by | OWNED:employees |
| **working_position_ranks** | company_id | →target |
| | rank_id | OWNED:ranks |
| | working_position_id | OWNED:working_positions |
| | department_id, part_id | OWNED:departments / OWNED:parts |
| | created_by, updated_by | OWNED:employees |
| **working_position_groups** | company_id | →target |
| | rank_group_id | OWNED:rank_groups |
| | department_id, part_id | OWNED:departments / OWNED:parts |
| | created_by, updated_by | OWNED:employees |
| **ranks** | company_id | →target |
| | rank_group_id | OWNED:rank_groups |
| | department_id, part_id | OWNED:departments / OWNED:parts |
| | created_by, updated_by | OWNED:employees |
| **rank_groups** | company_id | →target |
| | competency_group_id | OWNED:competency_groups |
| **rank_competency** | company_id | →target |
| | rank_id | OWNED:ranks |
| | competency_id | OWNED:competencies |
| | department_id, part_id | OWNED:departments / OWNED:parts |
| | created_by, updated_by | OWNED:employees |
| **competencies** | company_id | →target |
| | competency_group_id | OWNED:competency_groups |
| | department_id, part_id | OWNED:departments / OWNED:parts |
| | created_by, updated_by | OWNED:employees |
| **competency_groups** | company_id | →target |
| | department_id, part_id | OWNED:departments / OWNED:parts |
| | created_by, updated_by | OWNED:employees |
| **capabilities / capability_groups** | company_id | →target |
| | department_id, part_id | OWNED:departments / OWNED:parts |
| | created_by, updated_by | OWNED:employees |
| **department_manpowers** | company_id | →target |
| | department_id, manpower_department_id | OWNED:departments ⚠️ (manpower_department_id kiểm thêm) |
| | working_position_group_id | OWNED:working_position_groups |
| | part_id | OWNED:parts |
| | decision_id, manpower_planning_id | NULL/rỗng → GIỮ NULL ⚠️ |
| | created_by, updated_by | OWNED:employees |
| **department_manpower_positions** | department_manpower_id | OWNED:department_manpowers |
| | working_position_id | OWNED:working_positions |
| | title_id | OWNED:titles |
| | company_id→target; department_id/part_id | OWNED:departments/parts |
| | created_by, updated_by | OWNED:employees |
| **department_manpower_position_ranks** | department_manpower_position_id | OWNED:department_manpower_positions |
| | rank_id | OWNED:ranks |
| | company_id→target; department_id/part_id; created_by/updated_by | như trên |
| **department_manpower_position_competencies** | department_manpower_position_id | OWNED:department_manpower_positions |
| | competency_id | OWNED:competencies |
| | company_id→target; department_id/part_id; created_by/updated_by | như trên |
| **employee_manage_departments** | company_id | →target |
| | department_id | OWNED:departments |
| | employee_id | OWNED:employees ⚠️ (cột tên employee_id — kiểm employees vs employee_infos) |
| **employee_infos** | company_id | →target |
| | department_id, part_id, team_id | OWNED:departments / OWNED:parts / OWNED:teams |
| | job_position_id | OWNED:job_positions (bảng rỗng; 1 dòng giá trị rác → GIỮ NULL?) ⚠️ |
| | company_role | OWNED:roles ⚠️ (1 dòng không khớp) |
| | employee_role_id | OWNED:titles (122/122, model-confirmed) |
| | employee_work_position_id | OWNED:working_positions (110/110) |
| | direct_manager_id | OWNED:employee_infos (90/90; model nói Employee) ⚠️ |
| | direct_manager_position_id | OWNED:working_positions (90/90) |
| | employee_concurrently_position_id | OWNED:employee_concurrently_positions (rỗng) ⚠️ |
| | bank_id | SHARED:banks(code) |
| | bank_branch_id | toàn NULL → GIỮ NULL |
| | province_id_residence/address, district_id_*, ward_id_* | SHARED:provinces/districts/wards(code) |
| | created_by, updated_by | OWNED:employees |
| | image, face_image_url, id_images, passport_images, health_certification_file | GIỮ NGUYÊN (string path) |
| **employee_educations** | employee_info_id | OWNED:employee_infos |
| **employee_relationships** | employee_info_id | OWNED:employee_infos |
| **employee_bank_accounts** | employee_info_id | OWNED:employee_infos |
| | bank_id, bank_branch_id | SHARED:banks(code) / GIỮ NGUYÊN ⚠️ |
| | province_id | SHARED:provinces(code) |
| **employee_authorized_bank_accounts** | (như employee_bank_accounts) | |
| **employee_working_histories** | employee_info_id | OWNED:employee_infos |
| | department_id, part_id | OWNED:departments / OWNED:parts |
| | employee_role_id | OWNED:titles (87) |
| | employee_work_position_id | OWNED:working_positions (29) |
| **employee_concurrently_department_has_positions** | employee_info_id | OWNED:employee_infos |
| | department_id | OWNED:departments |
| | title_id | OWNED:titles |
| | working_position_id | OWNED:working_positions |
| **employee_info_conn_infos** | employee_info_id | OWNED:employee_infos |
| | conn_info_id | OWNED:conn_infos |
| **employee_salary_histories** | company_id | →target |
| | employee_info_id | OWNED:employee_infos |
| | working_position_id | OWNED:working_positions (77) |
| | rank_id | OWNED:ranks (77) |
| | competency_id | OWNED:competencies (77) |
| | department_id, part_id | OWNED:departments / OWNED:parts |
| | job_position_id, payroll_role_id | toàn NULL → GIỮ NULL |
| | created_by, updated_by | OWNED:employees |
| **employee_attendances** | company_id | →target |
| | employee_info_id | OWNED:employee_infos |
| | department_id, part_id | OWNED:departments / OWNED:parts |
| | created_by, updated_by | OWNED:employees |
| | current_year, các cột tháng/ngày phép | GIỮ NGUYÊN (số liệu) |
| **salary_compositions** | company_id→target; department_id/part_id; created_by/updated_by | OWNED tương ứng |
| **salary_templates** | company_id→target; department_id/part_id; created_by/updated_by | OWNED tương ứng |
| **salary_template_compositions** | salary_template_id | OWNED:salary_templates |
| | salary_composition_id | OWNED:salary_compositions |
| **insurance_configs / holidays / truncated_leaves / overtime_regulations / attendance_watch_regulations / general_regulations / labor_contracts / location_conn_infos** | company_id→target; department_id/part_id; created_by/updated_by | OWNED tương ứng |
| **leave_types** | (+ group_id → OWNED:groups) | |
| **working_shifts** | company_id→target; department_id/part_id; created_by/updated_by | OWNED |
| | location_conn_info_id | OWNED:location_conn_infos |
| **shift_details** | company_id→target; department_id/part_id; created_by/updated_by | OWNED |
| | working_shift_id + monday..sunday + saturday_odd/even_working_shift_id | OWNED:working_shifts (8/8) |
| **late_early_outs** | company_id→target; department_id/part_id; created_by/updated_by | OWNED |
| | employee_id | OWNED:employees ⚠️ (kiểm employees vs employee_infos) |
| **timekeeping_exemptions** | (+ employee_id → OWNED:employees ⚠️) | |
| **overtime_companies** | company_id→target; created_by/updated_by | OWNED:employees |
| **locations** | company_id | →target (chỉ có company_id + place lat/lng) |
| **conn_infos** | company_id→target; department_id/part_id; created_by/updated_by | OWNED |
| | location_conn_info_id | OWNED:location_conn_infos |
| | machine_type_id | GIỮ NGUYÊN (không có bảng machine_types) |
| | device_name, comm_key, serial_number... | GIỮ NGUYÊN (string) |
| **devices** | company_id | →target |
| | employee_info_id | OWNED:employee_infos |
| | department_id, part_id | OWNED:departments / OWNED:parts |
| | device_id | GIỮ NGUYÊN (string mã máy) |
| | created_by, updated_by | OWNED:employees |
| **employees** | employee_info_id | OWNED:employee_infos |
| | rice_setting_location_id | dangling (bảng rỗng) → SET NULL ⚠️ |
| | tp_id | GIỮ NGUYÊN (rỗng) |
| | email, password | GIỮ NGUYÊN (bỏ dòng email đụng) |
| **company_employees** | company_id | →target |
| | employee_id | OWNED:employees |
| **roles** | company_id | →target (D7 đổi tên `name`) |
| | department_id, part_id | OWNED:departments / OWNED:parts (NULL ở nguồn?) |
| | created_by, updated_by | OWNED:employees |
| **company_roles** | company_id | →target |
| | role_id | OWNED:roles |
| **role_has_permissions** | company_id | →target |
| | role_id | OWNED:roles |
| | permission_id | SHARED:permissions(name,guard_name) |
| **employee_has_roles** | company_id | →target |
| | employee_id | OWNED:employees |
| | role_id | OWNED:roles |
| | model_type | GIỮ NGUYÊN (`Modules\Timesheet\Entities\Employee`) |

### Cột FK cần KIỂM THÊM trước khi chạy (chưa verify 100%)
- `employee_manage_departments.employee_id`, `late_early_outs.employee_id`, `timekeeping_exemptions.employee_id`: tên `employee_id` → nghi trỏ `employees`, nhưng cần verify (có thể là `employee_infos`). Module Timesheet hay dùng `employee_id` = employees.
- `companies.deputy_id` / `owner_id`: chỉ 1 dòng, đề xuất employee_infos, cần xác nhận.
- `employee_infos.direct_manager_id`: model vs data mâu thuẫn (xem §A.4).
- `department_manpowers.manpower_department_id`: nghi OWNED:departments, chưa verify.
- `employee_infos.company_role` / `job_position_id` / `employee_concurrently_position_id`: bảng đích rỗng hoặc không khớp — đề xuất GIỮ NULL nếu không map được.

---

## D. Bổ sung pivot/con bị sót (PASS 2 — 2026-06-18)

> Pass 1 quét theo cột `company_id` nên sót các bảng pivot/con KHÔNG có `company_id` nhưng thuộc công ty qua khóa cha. Pass 2 quét TOÀN BỘ bảng có `COUNT(*)>0` KHÔNG có `company_id`, loại các bảng đã phân loại, rồi phân loại phần còn lại theo khóa cha. Tất cả số dòng đếm thật + verify FK bằng JOIN.

### D.1 Quyết định trọng yếu — `missions` chuyển pending_review → OWNED
`missions` (50 dòng, `company_id=1`) là **master "Quản lý nhiệm vụ" của menu Cơ cấu tổ chức** (`Modules/Human/Entities/Mission.php`), KHÔNG phải giao dịch. Nhiều pivot định biên/phòng ban/số dư lương trỏ tới nó → **bắt buộc ĐƯA** để các pivot mới map được `mission_id`. fk-map: `company_id→TARGET`, `department_id→OWNED:departments` (45/45 khớp), `part_id→OWNED:parts`, `created_by/updated_by→OWNED:employees` (50/50 khớp).

### D.2 Bảng OWNED-MIGRATE mới thêm (ĐƯA)

| Bảng | Dòng (đưa) | Cha OWNED | fk-map | Ghi chú |
|---|---|---|---|---|
| **missions** | 50 | (master) | company_id→TARGET; department_id→OWNED:departments; part_id→OWNED:parts; created_by/updated_by→OWNED:employees | Chuyển từ pending_review |
| **department_missions** | 54 | departments | department_id→OWNED:departments; mission_id→OWNED:missions | filter parent (54/54 hợp lệ) |
| **department_manpower_missions** | 49 (/158) | department_manpowers | department_manpower_id→OWNED:department_manpowers; mission_id→OWNED:missions | ⚠️ 109/158 orphan (cha đã xóa) → filter parent tự loại |
| **department_manpower_position_missions** | 47 | department_manpower_positions | department_manpower_position_id→OWNED:department_manpower_positions; mission_id→OWNED:missions | 47/47 hợp lệ |
| **department_manpower_position_titles** | 47 | department_manpower_positions | department_manpower_position_id→OWNED:department_manpower_positions; title_id→OWNED:titles | 47/47 hợp lệ |
| **employee_salary_history_missions** | 77 | employee_salary_histories | employee_salary_history_id→OWNED:employee_salary_histories; mission_id→OWNED:missions | 77/77 hợp lệ |
| **overtime_position_restrictions** | 2 | overtime_companies | overtime_company_id→OWNED:overtime_companies; working_position_id→OWNED:working_positions; created_by/updated_by→OWNED:employees | con quy định OT |
| **conn_info_working_shifts** | 3 (/11) | conn_infos | conn_info_id→OWNED:conn_infos; working_shift_id→OWNED:working_shifts | ⚠️ 8/11 trỏ conn_info ngoài cty → filter parent loại |
| **truncated_leave_excepts** | 2 | truncated_leaves | truncated_leave_id→OWNED:truncated_leaves; employee_info_id→OWNED:employee_infos | con cắt phép |
| **capability_has_groups** | 1 | capabilities, capability_groups | capability_id→OWNED:capabilities; capability_group_id→OWNED:capability_groups | Module Training (cha đã OWNED ở pass 1) |
| **capability_levels** | 4 | capabilities | capability_id→OWNED:capabilities | code/name/order_level GIỮ NGUYÊN |

> Lưu ý: các pivot trên KHÔNG có `created_by/updated_by` (trừ overtime_position_restrictions) và KHÔNG có `company_id` → fk-map chỉ gồm 2 khóa cha. Filter luôn là `parent` (lọc qua khóa cha OWNED), orphan tự loại.

### D.3 Bảng thêm vào SKIP (cha giao dịch đã skip / hệ thống / audit-log)

| Bảng | Dòng | Lý do |
|---|---|---|
| admin_request_update_working_employee_timesheets | 1068 | con admin_request_update_working_employees (skip) |
| conn_info_overtime_assignments | 2381 | pivot overtime_assignments (skip) |
| overtime_details | 24270 | con timesheet_summaries (skip) |
| timesheet_details | 41260 | con timesheet_summaries (skip) |
| application_customer_scopes / application_industries / application_scopes | 652/262/225 | con applications (skip) |
| training_planning_subjects / _subject_times / _subject_time_courses | 1/1/1 | con training_plannings (skip) |
| training_survey_respondents | 2 | con training_surveys (skip) |
| employee_infos_logs / employee_infos_log_values / employee_history | 133/54/5 | **audit-log** thay đổi hồ sơ — lịch sử, OUT OF SCOPE (§2) |
| master_settings / print_templates / meeting_types / bom_price_approval_configs | 9/34/2/6 | cấu hình hệ thống/không gắn công ty |

> `self_notification_employees`(1)/`self_notification_recipients`(1)/`salary_data`(7) là con của bảng đã có sẵn trong skip (self_notifications, salary) — không cần thêm dòng riêng, cha skip thì con bỏ.

### D.4 Bảng thêm vào PENDING_REVIEW (ranh giới Training/CRM — đi cùng quyết định cha)

| Bảng | Dòng | Cha pending | Nhóm |
|---|---|---|---|
| industry_scopes | 118 | industries↔scopes | CRM |
| capability_subjects | 1 | capabilities↔subjects | Training (subjects còn pending) |
| question_answers | 309 | questions | Training |
| question_classifies | 74 | questions | Training |
| teacher_has_training_types | 1 | teachers↔training_types | Training |
| exam_questions | 67 | exam | Training (kiểm tra/đánh giá) |
| exam_type_objects | 6 | exam | Training |

> Nguyên tắc: con đi theo quyết định của cha. Nếu duyệt ĐƯA `subjects`/`questions`/`teachers`/`exam_kits` (Training) hay `industries`/`scopes` (CRM) thì các pivot/con tương ứng cũng phải ĐƯA (đã liệt kê sẵn fk-map ở trên trong description).

### D.5 Checklist coverage menu "Cơ cấu tổ chức"

| Thực thể | Bảng | Trạng thái | Dòng |
|---|---|---|---|
| Công ty | companies | ✅ owned | 1 |
| Khối | groups | ✅ owned | 6 |
| Phòng ban | departments | ✅ owned | 14 |
| Bộ phận | parts | ✅ owned | 45 |
| Team | teams | ✅ owned (rỗng) | 0 |
| Vị trí công việc | working_positions | ✅ owned | 10 |
| ↳ nhóm vị trí | working_position_groups | ✅ owned | 5 |
| ↳ cấp bậc vị trí | working_position_ranks | ✅ owned | 10 |
| Chức danh | titles | ✅ owned | 67 |
| Cấp bậc | ranks | ✅ owned | 6 |
| ↳ nhóm cấp bậc | rank_groups | ✅ owned | 6 |
| ↳ năng lực cấp bậc | rank_competency | ✅ owned | 39 |
| ↳ chi tiết cấp bậc | rank_details | ➖ rỗng | 0 |
| Năng lực | competencies | ✅ owned | 53 |
| ↳ nhóm năng lực | competency_groups | ✅ owned | 6 |
| **Nhiệm vụ** | **missions** | ✅ **owned (PASS 2)** | 50 |
| ↳ phòng ban ↔ nhiệm vụ | **department_missions** | ✅ **owned (PASS 2)** | 54 |
| Định biên | department_manpowers | ✅ owned | 29 |
| ↳ vị trí định biên | department_manpower_positions | ✅ owned | 27 |
| ↳ ↔ cấp bậc | department_manpower_position_ranks | ✅ owned | 27 |
| ↳ ↔ năng lực | department_manpower_position_competencies | ✅ owned | 157 |
| ↳ ↔ chức danh | **department_manpower_position_titles** | ✅ **owned (PASS 2)** | 47 |
| ↳ ↔ nhiệm vụ (vị trí) | **department_manpower_position_missions** | ✅ **owned (PASS 2)** | 47 |
| ↳ ↔ nhiệm vụ (định biên) | **department_manpower_missions** | ✅ **owned (PASS 2)** | 49/158 |
| Phân bổ định biên | manpower_allocations + manpower_department_* + mp_* | ➖ rỗng | 0 |

> ✅ Toàn bộ thực thể của menu Cơ cấu tổ chức có data đã được phủ. Các bảng rỗng (rank_details, teams, manpower_*/mp_*) vẫn nằm catalog (chèn 0 dòng) phòng xa.

---

## E. Quyết định đã chốt (2026-06-18)

> Người duyệt đã chốt 13 quyết định. Cập nhật vào `config/company_migration.php` (đã `php -l` PASS).
> `pending_review` giờ **RỖNG** — không còn gì chờ duyệt.

### E.1 Bảng chuyển nhóm

| # | Quyết định | Hành động trong config |
|---|---|---|
| 1 | **CRM → BỎ** | pending_review → **skip**: `customers`, `customer_scopes`, `customer_scope_groups`, `scopes`, `industries`, `industry_scopes` (các `application_*` đã skip sẵn — con của applications) |
| 2 | **Training → ĐƯA** | pending_review → **owned**: `training_types`, `subjects`, `teachers`, `examiners`, `questions`, `exam_kits` + con/pivot: `question_answers`, `question_classifies`, `teacher_has_training_types`, `exam_questions`, `exam_type_objects`, `capability_subjects`. (`examiner_has_training_types` = 0 dòng → KHÔNG thêm) |
| 3 | **Danh mục nhỏ → ĐƯA** | pending_review → **owned**: `reward_conditions`, `priority_levels`, `insurance_types`, `attachment_types`, `reward_modes` |
| 4 | **devices** | filter giữ `company_id=1 OR company_id IS NULL` (169 + 74 NULL = 243), chèn set `company_id=TARGET` |
| 5 | Bảng tổ chức company_id NULL | filter `company_id=1 OR company_id IS NULL` (titles, working_positions*, ranks*, roles…) — annotate CHỐT |
| 6 | `employee_infos.direct_manager_id` | OWNED:employee_infos (data 90/90) — annotate CHỐT |
| 7 | JSON nhúng id | thêm key **`json_fk`** (translate_json_ids): `groups.group_assistants`, `departments.department_assistants`, `departments.working_position_order` → `OWNED:employee_infos` |
| 8 | `employees.rice_setting_location_id` | đổi `KEEP` → **`SET_NULL`** |
| 9 | `departments.department_id` + `parent_id` | OWNED:departments — annotate CHỐT |
| 10 | Dòng mồ côi | giữ filter `parent` (department_manpower_missions 49/158, conn_info_working_shifts 3/11) |
| 11 | `companies.deputy_id`/`owner_id` | OWNED:employee_infos — annotate CHỐT |
| 12 | `bank_branch_id` | xem E.3 (giữ NULL) |
| 13 | `roles` | giữ `rename_suffix => true` (hậu tố ` (EG)`) |

### E.2 Kết quả VERIFY (JOIN dữ liệu thật)

| Cột | Kết quả JOIN | Kết luận | Trong config |
|---|---|---|---|
| `employee_manage_departments.employee_id` | employees **16/16**, employee_infos 11/16. Model `employee()=Employee` | **OWNED:employees** | giữ nguyên (đúng) |
| `late_early_outs.employee_id` | cả 2 đều 6/6 (id range trùng). Model `employee_info()=EmployeeInfo,'employee_id'`; code dùng `getEmloyeeInfoId()` | **OWNED:employee_infos** | **SỬA** (trước là employees) |
| `timekeeping_exemptions.employee_id` | employee_infos **3/3**, employees 1/3. Model `employeeInfo()=EmployeeInfo,'employee_id'` | **OWNED:employee_infos** | **SỬA** (trước là employees) |
| `department_manpowers.manpower_department_id` | **toàn bộ 29 dòng NULL** | không có giá trị cần dịch; giữ `OWNED:departments` an toàn | annotate |
| **Training FK** (subjects.training_type_id, exam_kits.capability_id/level, exam_questions.exam_id+question_id, exam_type_objects.exam_id, teacher_has_training_types, capability_subjects, question_answers.question_id, question_classifies.question_id) | **tất cả 100% khớp** | xem fk-map E.4 | đã set |
| `teachers.employee_id` / `examiners.employee_id` | cả employees & employee_infos đều khớp (10/10, 5/5; id range trùng). Model `Teacher/Examiner::employee()=Human\Employee` (table `employees`) | **OWNED:employees** | đã set |

### E.3 Kết luận `bank_branches`

- `bank_branches` **KHÔNG có `company_id`** ở cả 2 DB → là bảng **SHARED/global**.
- Cấu trúc: `id, name, bank_id, province_id` — **KHÔNG có cột `code`**; natural-key khả dĩ = `(name, bank_id)`.
- **id KHÔNG khớp giữa 2 DB**: nguồn có 3 dòng (id 2,3,4), match theo `(name,bank_id)` sang đích đều **NULL** (đích 119 dòng, không trùng).
- **NHƯNG** mọi cột `bank_branch_id` ở nguồn **toàn NULL**: employee_infos 0/124, employee_bank_accounts 0/4, employee_authorized_bank_accounts 0/3.
- **→ Kết luận: GIỮ NULL** (`KEEP`). Không cần map. Đã ghi chú trong config rằng nếu sau này có giá trị thì phải map natural-key `(name, bank_id)` (id không dùng được).

### E.4 fk-map các bảng Training mới đưa (đã set trong config)

| Bảng | filter | fk-map |
|---|---|---|
| training_types | company_id=1 | company_id→TARGET; department_id/part_id→OWNED; created_by/updated_by→OWNED:employees |
| subjects | company_id=1 | + training_type_id→OWNED:training_types (6/6) |
| teachers | company_id=1 | + employee_id→OWNED:employees (model Human\Employee); created_by/updated_by→OWNED:employees |
| examiners | company_id=1 | + employee_id→OWNED:employees |
| questions | company_id=1 | company_id→TARGET; department_id/part_id; created_by/updated_by→OWNED:employees |
| exam_kits | company_id=1 | + capability_id→OWNED:capabilities (1/1); capability_level_id→OWNED:capability_levels (1/1) |
| question_answers | parent (question_id 309/309) | question_id→OWNED:questions |
| question_classifies | parent (question_id 74/74) | question_id→OWNED:questions; **poly_fk** objectable_id: Subject→subjects(71), Capability→capabilities(3) |
| teacher_has_training_types | parent (1/1) | teacher_id→OWNED:teachers; training_type_id→OWNED:training_types |
| exam_questions | parent (67/67) | exam_id→OWNED:exam_kits; question_id→OWNED:questions |
| exam_type_objects | parent (6/6) | exam_id→OWNED:exam_kits; **poly_fk** objectable_id: Subject→subjects |
| capability_subjects | parent (1/1) | capability_id→OWNED:capabilities; subject_id→OWNED:subjects |
| reward_conditions / priority_levels / insurance_types / attachment_types / reward_modes | company_id=1 | company_id→TARGET; department_id/part_id→OWNED; created_by/updated_by→OWNED:employees |

> Lưu ý đặc biệt: `question_classifies` và `exam_type_objects` có **FK đa hình** (`objectable_type` + `objectable_id`) → Phase 3 dịch `objectable_id` qua map bảng tương ứng `objectable_type` (đã khai key `poly_fk` trong config).

### E.5 Special-handling flags đã thêm vào config

- `json_fk` (translate_json_ids): departments (department_assistants, working_position_order), groups (group_assistants).
- `poly_fk`: question_classifies, exam_type_objects.
- `SET_NULL`: employees.rice_setting_location_id.
- `rename_suffix => true`: roles (giữ nguyên).
- devices filter `OR company_id IS NULL` (giữ nguyên).

### E.6 pending_review còn lại

**RỖNG.** Toàn bộ mục ranh giới đã được quyết. Không còn bảng nào chờ duyệt.

> Ghi chú: các comment `⚠️` còn sót trong config (`job_position_id`, `company_role`, `employee_concurrently_position_id`, `decision_id`/`manpower_planning_id`) **CHỈ là ghi chú thông tin** (bảng đích rỗng / cột toàn NULL / orphan tự loại), KHÔNG phải quyết định chờ duyệt — không nằm trong 13 quyết định lần này.

---

## C. Ghi chú bổ sung
- `created_by`/`updated_by` → **employees** (xác nhận 3 bảng, 100% khớp).
- Ảnh `employee_infos`: string path (vd `/uploads/...`, `https://tanphat.s3...`) → GIỮ NGUYÊN.
- `files` nguồn = 0 dòng → không migrate.
- Email đụng: `namdangit@gmail.com` (employees + employee_infos).
- `companies.name` đụng id=7 đích.
- `employee_has_roles.model_type` = `Modules\Timesheet\Entities\Employee`.

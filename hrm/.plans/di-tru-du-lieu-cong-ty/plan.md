# Plan — Di trú dữ liệu 1 công ty (Hướng B, ánh xạ ID liền mạch)

> Spec: `docs/superpowers/specs/2026-06-17-di-tru-du-lieu-cong-ty-design.md`
> Tóm tắt: `.plans/di-tru-du-lieu-cong-ty/design.md`
> Feature CHỈ Backend (artisan command + config). Nguồn: `local_hrm_green` (cty id=1). Đích: `hrm_prod_local` (tạo cty mới).
> NGUYÊN TẮC: mọi thao tác chạy `--dry-run` trước; chạy thật chỉ trên bản copy DB rồi mới tới cửa sổ bảo trì; backup trước mỗi lần chạy thật.

---

## Phase 0 — Catalog & classification (sinh tự động + duyệt) ✅ DONE 2026-06-18

- [x] Quét `information_schema` bảng có `company_id` + COUNT(*) (259 bảng)
- [x] Quét bảng OWNED qua khóa cha (pass 2): pivot/con không có company_id (department_missions, *_manpower_missions, *_position_titles/missions, employee_salary_history_missions...)
- [x] Phân loại SHARED(9) / OWNED-MIGRATE(86) / SKIP(193)
- [x] Bản đồ FK "cột → OWNED:x / SHARED:x(key) / GIỮ NGUYÊN" + verify bằng JOIN; special: json_fk, poly_fk, set_null, rename_suffix
- [x] Xác nhận files rỗng, ảnh là cột path; bank_branches NULL→giữ NULL
- [x] Xuất `config/company_migration.php` (php -l PASS) + báo cáo `phase0-catalog.md`
- [x] Người dùng DUYỆT: CRM bỏ, Training đưa, danh mục nhỏ đưa, devices OR NULL; Nhóm 1 áp dụng mặc định; pending_review=0
- [x] Verify employee_id columns (sửa late_early_outs + timekeeping_exemptions → employee_infos)

## Phase 1 — Hạ tầng (connection + seeder + helper + backup) ✅ DONE 2026-06-18
> Service `app/Services/CompanyMigration/CompanyMigrationService.php` + `database/seeders/CompanyMigrationSeeder.php` + connection `mysql_source` + .env. 11 unit test xanh, kết nối thật 2 DB OK, `migration_id_map` tạo runtime. Helpers: allocateIds/translateFk(run_id-scoped)/computeNewIds/ensureMapTable/bumpAutoIncrement/loadCatalog/applyModuleFlags.

- [ ] Thêm connection `mysql_source` vào `config/database.php` (đọc biến `DB_*_SOURCE`)
- [ ] Thêm biến `.env`: `DB_CONNECTION_SOURCE=mysql`, `DB_HOST_SOURCE`, `DB_PORT_SOURCE`, `DB_DATABASE_SOURCE`, `DB_USERNAME_SOURCE`, `DB_PASSWORD_SOURCE` + tham số seeder: `MIGRATION_DRY_RUN`, `MIGRATION_SOURCE_COMPANY_ID`, `MIGRATION_RUN_ID`, cờ module `MIGRATE_CRM/MIGRATE_TRAINING/MIGRATE_SMALL_CATALOGS`
- [ ] Test kết nối cả 2 DB (in version + tên DB) — helper trong Service
- [ ] Tạo bảng `migration_id_map(table_name, old_id, new_id, run_id)` + index `(run_id, table_name, old_id)` (migration). LƯU Ý scope theo `run_id` (mọi DB nguồn đều có id trùng)
- [ ] Helper `allocateIds(table, oldIds[], runId) → map` (id mới = max(id) đích + rank, ghi map theo run_id) + unit test
- [ ] Helper `translateFk(table, oldId, runId) → newId` (tra map WHERE run_id) + unit test (self-ref + null + json_fk + poly_fk)
- [ ] Orchestrator 2 bước trong Service: **Bước A** cấp id mọi bảng OWNED của run → **Bước B** chèn + dịch FK. Xử lý vòng (departments↔groups↔employee_infos), special-handling (json_fk/poly_fk/set_null/rename_suffix)
- [ ] Tạo **`CompanyMigrationSeeder`** (gọi `CompanyMigrationService`) chạy `php artisan db:seed --class=CompanyMigrationSeeder`; đọc tham số .env; tôn trọng `MIGRATION_DRY_RUN` + cờ module
- [ ] Viết script/lệnh backup DB đích (`mysqldump hrm_prod_local` ra file timestamp) + hướng dẫn quy trình chạy nhiều công ty (sửa .env → seed → verify → lặp)

## Phase 2 — Shared mapping (natural-key) + đối soát ✅ DONE 2026-06-18
> buildSharedMap theo strategy: địa lý=id_identity (3 tầng: id+name→id≠name→fallback name+cha), banks=name(NFC normalize), permissions=tuple(100% khớp), majors/areas=name(rỗng), system_salary_compositions=unused. 29 test xanh. Đối soát thật: wards 13463/13463, provinces 44/44, districts 712/712 (692 id+name, 20 id≠name HCM), permissions 580/580, banks 5/12 (bank 7 MB của 1 NV miss→NULL).

- [ ] Helper `buildSharedMap(table, key)` so natural-key nguồn↔đích, trả map + danh sách KHÔNG khớp + unit test
- [ ] Dựng map cho: nations/provinces/districts/wards/banks/system_salary_compositions (theo `code`), majors/areas (theo `name` normalize)
- [ ] Dựng map `permissions` theo `(name, guard_name)` (kỳ vọng identity — cảnh báo nếu lệch)
- [ ] `--dry-run` xuất báo cáo đối soát shared: bao nhiêu khớp, liệt kê giá trị không khớp (đặc biệt majors/areas) để xử lý thủ công trước khi chạy thật

## Phase 3 — Core migration (companies → tổ chức → hồ sơ + số dư → config) ✅ DONE 2026-06-18
> Engine `runMigration(sourceCompanyId, runId, dryRun)` trong Service: 2 bước (A cấp id mọi bảng OWNED → B chèn+dịch FK). dry-run validate-only, dọn migration_id_map. DRY-RUN thật 86 bảng OWNED: 3501 dòng, companies=1/departments=14/employee_infos=123/employees=122 (đúng kỳ vọng sau loại 1 email). 710 FK OWNED không dịch được = 504 trỏ người email-đụng + 197 audit=0 + 9 dangling nguồn (0 bất ngờ). 32 SHARED miss = 29 province dangling nguồn + 3 bank. 41 unit test xanh.

- [x] Tiền-kiểm ĐỘNG: email đụng (`employees.email`+`employee_infos.email`, chuẩn hóa lower) → tập exclude (info_ids+employee_ids, đồng bộ chéo); tên cty đụng → hậu tố `(code)`/`(2)`
- [x] Chèn `companies` (id mới = target-company-id; tên đụng → hậu tố vào tên MỚI), lưu map
- [x] Chèn nhóm tổ chức (departments/parts/teams/groups/working_*/titles/ranks/rank_*/competencies/department_manpowers+con/missions/department_missions) — dịch FK đầy đủ, xử lý vòng (Bước A cấp id trước), json_fk assistants
- [x] Chèn `employee_infos` (bỏ người email đụng), FK org + shared (province/district/ward/bank), giữ cột path ảnh, bank_branch_id NULL
- [x] Chèn con hồ sơ NV (educations/relationships/bank_accounts/working_histories/concurrently/employee_manage_departments/info_conn_infos)
- [x] Chèn số dư: employee_salary_histories(+missions), employee_attendances
- [x] Chèn config có data (salary_*/insurance_configs/holidays/leave_types/working_shifts+details/late_early_outs/truncated_leaves+excepts/timekeeping_exemptions/overtime_*/regulations/labor_contracts/locations+conn_infos/devices OR-NULL/danh mục nhỏ)
- [x] Chèn Training (MIGRATE_TRAINING on): training_types/subjects/teachers/examiners/questions+answers+classifies(poly_fk)/exam_kits+questions+type_objects(poly_fk)/capability_*
- [x] CRM theo cờ (off → bỏ)
- [x] poly_fk (question_classifies/exam_type_objects), set_null (employees.rice_setting_location_id), json_fk (departments/groups assistants)
- [x] Bump `AUTO_INCREMENT` sau khi chèn mỗi bảng (chỉ chế độ thật)

## Phase 4 — Phân quyền (employees + roles + pivots) ✅ DONE 2026-06-18
> Tích hợp trong cùng engine runMigration (Bước B). Pivot composite-key KHÔNG có cột `id` (role_has_permissions/employee_has_roles/employee_has_permissions) xử lý riêng: Bước A bỏ cấp id, Bước B đọc theo filter + chèn không cột id + bỏ dòng dangling FK (permission_id NOT NULL trong PK). DRY-RUN: roles=4 (hậu tố ` (tên cty)`), role_has_permissions=906 (loại 167 trỏ permission đã xóa ở nguồn), employee_has_roles=22 (loại 3 của người email-đụng).

- [x] Chèn `employees` (bỏ dòng email đụng), dịch `employee_info_id`, lưu map employees
- [x] Chèn `roles` (tạo mới + hậu tố tên cty, idempotent appendSuffixIfNeeded), lưu map roles
- [x] Chèn `company_roles` (company_id=đích, role_id tra map)
- [x] Chèn `company_employees` (company_id=đích, employee_id tra map; loại người email-đụng)
- [x] Chèn `role_has_permissions` (id-less; company_id=đích, role_id tra map, permission_id map tuple; loại dòng permission dangling)
- [x] Chèn `employee_has_roles` (id-less; employee_id+role_id tra map; loại người email-đụng); `employee_has_permissions` (rỗng nguồn)
- [x] `employee_infos.company_role` dịch qua map roles (OWNED:roles trong fk-map; dangling id=1 nguồn → NULL)

## Phase 5 — Verify & cutover

- [x] Tạo bản copy DB đích → chạy thật trên copy (DRY_RUN=false) — ✅ ĐÃ CHẠY TRỌN VẸN (companies 8→9, employee_infos=123, ~3510 dòng, integrity sạch, id liền mạch, công ty cũ md5 khớp). Qua đó fix 4 lỗi insert dry-run không bắt: unique guard (titles/competencies...), check `<>''` (image→'-'), NOT NULL nhận NULL (created_by→0...), bump bỏ qua bảng id-less. 76 unit test xanh.
- [x] Chạy THẬT trên LOCAL `hrm_prod_local` (run_id=etekgreen) — ✅ companies 8→9, đếm DB khớp 100% kỳ vọng (NV 123, employees 122, dept 14, parts 45, groups 6, titles 67, lương 77, phép 283, quyền 906, ehr 22, company_employees 122)
- [x] Đối soát integrity trực tiếp trên DB: NV trỏ sai phòng ban=0, sai chức danh=0, lương trỏ sai NV=0, parent sai=0; id liền mạch (max employee_infos.id=1717, không nhảy 100M); công ty cũ (cty1=780 NV) nguyên vẹn; migration_id_map run etekgreen=2582 dòng
- [x] Verify nghiệp vụ qua Playwright: login API (current_company=9, hồ sơ EG-001 Ngô Cao Vinh, ảnh S3 load) + login trình duyệt (dashboard "Xin chào Ngô Cao Vinh"); admin di trú uyendtt.hr (role "Super Admin (ETEK GREEN)") xem màn Khối = đúng 6 khối ETEK GREEN (lọc theo cty9); NV thường bị chặn /human/employee (404) → phân quyền đúng
- [ ] **Test TÁI SỬ DỤNG** (chưa làm): sửa .env trỏ DB công ty thứ 2 + run_id mới → seed lại → xác nhận 2 công ty cùng tồn tại, map tách theo run_id
- [ ] Chạy thật PRODUCTION cho TỪNG công ty: backup → bảo trì → sửa .env (DB nguồn + run_id + cờ module) → seed → verify nhanh → mở lại → lặp công ty kế
- [ ] (Tùy chọn, NGOÀI scope di trú) super-admin công ty mới chỉ thấy data công ty mình ở màn "Danh sách tài khoản" — hiện app cho super-admin thấy toàn bộ (1198 tk) — cần sửa logic phân quyền app nếu muốn

## Phase 6 — Fix "Số NP còn lại" sai sau di trú (phép đã dùng trước cutover)

> Bug: màn timesheet/attendance/add (và dashboard/báo cáo phép/cắt phép) tính "đã dùng" tươi từ `timesheet_summaries.work_day_phep` — bảng này nằm SKIP (không di trú) → target=0 → NP còn lại bị thổi phồng đúng số ngày phép đã nghỉ năm nay trước cutover. Đo nguồn cty1: 2026 = **402.5 ngày / 63 NV** (TB ~6.4). Tất cả 63 NV map đủ + có dòng employee_attendances 2026 target (0 skip).
> Hướng (user chốt): bổ sung phép đã dùng năm cutover vào `employee_attendances.number_day_leave_outside` (nhãn FE "Số phép nghỉ ngoài PM" — đúng nghĩa "nghỉ ngoài phần mềm mới"). Công thức "đã dùng" = ts_target(0) + number_day_leave_outside → đúng cho TẤT CẢ màn cộng field này. KHÔNG đụng timesheet_summaries.

### BE
- [x] `CompanyMigrationService::foldPreCutoverUsedLeave(sourceCompanyId, runId, year, dryRun)` — đọc nguồn SUM(work_day_phep) năm cutover theo NV + number_day_leave_outside gốc → SET target `number_day_leave_outside = base_nguồn + used` (idempotent, recompute từ nguồn), match theo new_id+current_year+company_id. Trả báo cáo applied/skipped.
- [x] Gọi trong `runMigration` post-commit (chỉ chế độ thật) + preview số liệu nguồn cho dry-run → công ty sau tự đúng.
- [x] Command `company:fold-used-leave {--source=} {--run=} {--year=} {--dry-run}` — fix công ty đã di trú (cty9 run etekgreen year 2026).
- [x] php -l PASS + 75 unit test xanh (không regression).

### Verify
- [x] Dry-run command cty9 → đúng 63 NV / 402.5 ngày / target cty9 / 0 skip.
- [x] Chạy thật → DB: SUM(number_day_leave_outside) cty9 2026 = 402.5 (63 NV); **0 NV lệch** khi so NP còn lại TARGET vs NGUỒN trên toàn cty9 (đối chiếu cùng công thức app, clamp ≥0).
- [x] Verify API: get-total-leave-day EG-012→3.5, EG-043→9, EG-047→0, EG-007→5 (used=outside fold). KHỚP.
- [x] Verify BROWSER (Playwright, login uyendtt.hr EG-007): attendance/add "Số NP còn lại=5" (được sử dụng 9 / đã nghỉ 4); dashboard widget phép "4/9 Ngày" → fold đúng cả 2 màn.

### Checkpoint — 2026-06-20 (Phase 6 — Fix NP còn lại — DONE)
Vừa hoàn thành: Fix "Số NP còn lại" thổi phồng sau di trú. Root-cause: "đã dùng" tính tươi từ `timesheet_summaries` (SKIP, không di trú) → target=0. Giải: cộng phép đã dùng năm cutover vào `employee_attendances.number_day_leave_outside` (nhãn "Số phép nghỉ ngoài PM"). Method `foldPreCutoverUsedLeave` (idempotent, SET=base_nguồn+used) + tích hợp post-commit trong `runMigration` (công ty sau tự đúng) + command `company:fold-used-leave` (đã chạy thật cho cty9: 63 NV / 402.5 ngày). Verify: 0 NV lệch toàn cty9 (TARGET==NGUỒN), 75 test xanh. Fix đúng đồng loạt cho mọi màn cộng field này (attendance/add, dashboard, báo cáo phép, cắt phép).
Đang làm dở: (không).
Bước tiếp theo: User verify browser màn attendance/add. Khi di trú công ty mới: fold tự chạy trong runMigration; nếu đã di trú trước Phase 6 thì chạy `php artisan company:fold-used-leave --source=<id> --run=<runId> --year=<năm>`.
Blocked: (không).

## Phase 6b — Audit màn tương tự + an toàn cron recompute (2026-06-20)

> User hỏi: còn màn nào tương tự "NP còn lại" (số dư/lũy kế tính tươi từ bảng giao dịch SKIP) → audit toàn bộ Timesheet/Payroll/Dashboard.

### Kết quả audit (Explore agent rà toàn FE+BE)
- **A1 (NP còn lại — hiển thị + chặn vượt phép `NumberDayLeaveRule`)** + **C1-phép (dashboard widget phép)**: ✅ ĐÃ tự fix bởi fold Phase 6 — cả 3 đều cộng `number_day_leave_outside`.
- **B1 (overtime "Số giờ đã làm thêm trong tháng", `OvertimeAssignmentController::getInfoOverTimeEmployee`)**: nguồn `overtime_assignments` (SKIP), cửa sổ THÁNG → tự lành tháng sau cutover. Nguồn có 100 OT/25 NV tháng 6/2026. **Quyết (user): KHÔNG sửa code, cutover production đầu tháng** → tháng đó nguồn chưa có OT → target=0 đúng.
- **A2 (cron `update:attendance` → `EmployeeAttendanceService::updateData/updateDataAll`)**: recompute `employee_attendances` tươi từ `timesheet_summaries` rỗng → đạp `usable_leave_days`/`remaining_last_year` (cty9 bật `additional_for_unpaid_leave`+`has_time_to_use` → usable về ~0). Fold (`number_day_leave_outside`) thì AN TOÀN (chỉ đọc, không gán).
- C1-khác (dashboard công/giờ OT), B2 (cap tỉ lệ payment): hiển thị/rủi ro thấp, cha cũng SKIP → bỏ qua.

### BE — Guard cron recompute (A2)
- [x] Config `company_migration.leave_recompute_skip` = `[company_id_đích => năm_cutover]` (cty9=>2026). Mỗi lần di trú công ty mới THÊM 1 dòng.
- [x] Helper `EmployeeAttendanceService::shouldSkipMigratedRecompute(companyId, year)` + guard ở `updateDataAll` (continue) và `handleUpdateData` (return) → bỏ qua NV công ty di trú năm <= cutover, giữ snapshot. Năm sau cutover target đủ ts → chạy lại bình thường.
- [x] php -l PASS + 75 unit test xanh.

### Verify
- [x] Chạy thật `php artisan update:attendance` (1215 NV) — KHÔNG lỗi (7.5s). Cty9/2026 md5 BEFORE==AFTER (snapshot giữ nguyên, fold 402.5 còn nguyên); cty1 (không di trú) updated_at mới → recompute vẫn chạy cho công ty thường. Guard chọn lọc đúng.
- [x] Verify BROWSER overtime/add (EG-007): max=100 / đã làm thêm=0 / còn lại=100. EG-007 thực có 8 OT tháng 6 ở nguồn → minh chứng hạn chế đã thống nhất (overtime không di trú, mitigate cutover đầu tháng). Dashboard "số công đi làm=0" = hiển thị thuần (cosmetic, tự lành).
- Lưu ý hạn chế (chấp nhận): năm cutover, usable_leave_days không tự accrue thêm Jul–Dec (đóng băng snapshot June). Đây là đúng tinh thần "di trú snapshot số dư"; hết năm cutover sẽ tự chạy lại đúng.

### Checkpoint — 2026-06-20 (Phase 6b — Audit + guard cron — DONE)
Vừa hoàn thành: Audit toàn bộ màn cùng kiểu "NP còn lại". A1+C1-phép đã tự fix bởi fold. B1 overtime: chấp nhận (cutover đầu tháng, không sửa code). A2 cron: thêm guard config-driven (`leave_recompute_skip`) cho `updateData/updateDataAll/handleUpdateData` → `update:attendance` chạy được an toàn (verify thật: cty9 không đổi, cty thường vẫn recompute, không lỗi). 75 test xanh.
Bước tiếp theo: User verify browser. Mỗi lần di trú công ty mới → thêm `[company_id => năm_cutover]` vào config `leave_recompute_skip`.
Blocked: (không).

## Phase 6c — Audit TOÀN PROJECT (Payroll + Human + Decision + Training) — 2026-06-20

> User yêu cầu: kiểm toàn project, tự đánh giá, tự sửa màn cần thiết. Dùng 2 Explore agent (Opus) rà Payroll/tiền + Human/Decision/Training, đối chiếu DB nguồn.

### Kết luận: KHÔNG cần sửa thêm code (ngoài Phase 6/6b đã làm)
- **Payroll/lương/thuế/BHXH/tạm ứng**: AN TOÀN. Mọi số tiền/số dư tính từ bảng ĐÃ di trú (`employee_salary_histories`, `insurance_configs`) hoặc scope theo `salary_id` kỳ mới (tự chứa, không carry-forward, không opening-balance đọc bảng skip). KHÔNG có mẫu "số dư owned − giao dịch skip" nào ngoài ca phép. Báo cáo income/insurance year đọc owned → đúng. payroll_info/dashboard calcMonth/insurance-register report: chỉ thiếu lịch sử trước cutover (cosmetic, tự lành 2027).
- **Thâm niên (A1 `Helper::getCurrentSeniorityMonths` trừ suspend_labor_contracts+employee_disciplines; A2 màn tăng thâm niên mất mốc increase_seniority_employees)**: 3 bảng này **RỖNG ở nguồn** (đo thực: suspend=0/discipline=0/increase_seniority=0) → thâm niên ETEK GREEN tính từ `enter_date` (di trú) là ĐÚNG. MOOT. KHÔNG sửa.
- **Mã HĐ/phụ lục tuần tự, số khóa học, điểm thi, số lần thi, dashboard đào tạo/quyết định, prefill mã HĐ cũ, badge "sắp hết hạn HĐ"**: transient/by-design (reset theo công ty mới hoặc tự lành khi phát sinh dữ liệu đích). KHÔNG sửa.

### ⚠️ CHECKLIST TIỀN-DI-TRÚ cho công ty TƯƠNG LAI (rủi ro thâm niên — moot với ETEK vì nguồn rỗng)
Trước khi di trú công ty mới, đối soát 3 bảng ở DB nguồn:
- `suspend_labor_contracts`, `employee_disciplines` → nếu CÓ: `Helper::getCurrentSeniorityMonths` sẽ tính DƯ thâm niên (không trừ được tháng tạm hoãn/kỷ luật cũ vì bảng skip). Xử lý: nhập tay điều chỉnh hoặc seed bản ghi còn hiệu lực.
- `increase_seniority_employees` → nếu CÓ: màn Quyết định "Tăng thâm niên" mất mốc xét gần nhất → đề-xuất tăng lại toàn bộ thâm niên (cấp dư nếu duyệt nhầm). Xử lý: nhập tay "ngày xét TN gần nhất" / seed 1 mốc cutover.
- Đây là màn ĐỀ-XUẤT có người duyệt (không tự đạp `employee_salary_histories`) → rủi ro là "cấp dư khi duyệt", không hỏng số dư đã lưu. KHÔNG sửa code shared (theo CLAUDE.md).

### Verify browser (Phase 6) — DONE
- attendance/add (EG-007): NP được sử dụng 9 / đã nghỉ 4 / **còn lại 5** ✅ (khớp API+DB; "đã nghỉ" = fold).
- dashboard widget phép: 4/9 Ngày ✅. overtime/add: max 100 / đã làm 0 / còn lại 100 (EG-007 thực có 8 OT tháng 6 nguồn → minh chứng hạn chế đã thống nhất).

## Phase 6i — Fix màn /rice/personal-registration crash (non-rice user) — 2026-06-20

> User test bằng uyendtt.hr → màn /rice/personal-registration lỗi `Cannot read properties of undefined (reading 'status_regular')` + API 400 `Trying to get property 'id' of non-object`.

### Phân tích
- Root-cause: uyendtt.hr (admin HR) KHÔNG đăng ký ăn cơm → KHÔNG có rice_employee_info → `auth()->riceUser()` NULL. BE `PersonalRegistrationService::index:38` + `checkUserInvitation:103/110` truy cập `riceUser()->id` → 400 → FE registrationData rỗng → crash. **KHÔNG phải lỗi re-link** — bug có sẵn (rice = chỉ NV đăng ký; TPE cty1=338 rice/nhiều NV, cty7=3 → coverage 1 phần là bình thường).
- Re-link Phase 6h ĐÚNG: EG-001 (NV cơm thật) BE trả 200 đủ 7 ngày.

### Fix
- [x] `PersonalRegistrationService::index` guard riceUser null → `$registrations = collect()` (NV không đăng ký vẫn xem menu, không crash). `checkUserInvitation` guard null → return false. php -l PASS.
- [x] Verify API: uyendtt.hr giờ 200 (35 ngày). Browser: uyendtt.hr (non-rice) + EG-001 (rice) đều KHÔNG còn lỗi status_regular.
- [x] Browser EG-001: màn "Quản lý đăng ký cơm" render đúng (lưới 06/2026, nút + đăng ký từ 20/06) → re-link sống.

### Lưu ý
- Đặt mật khẩu tạm `Test@12345` cho EG-001 (vinhnc.cob@etekgreen.com, employee 1889) để test — CHƯA khôi phục.
- 72/122 NV cty9 KHÔNG có rice record (không đăng ký cơm — như TPE). Giờ họ xem menu OK nhưng MUỐN đăng ký thật thì cần tạo rice_employee_info (app tạo khi save NV; di trú insert thẳng nên bỏ qua). Nếu cần enroll toàn bộ → quyết định riêng.

### Bổ sung: ENROLL rice record còn thiếu + guard endpoint
- [x] Chẩn đoán: 72 NV cty9 chưa có rice → **45 thuộc phòng ĐÃ bật cơm (THIẾU THẬT** — app tạo khi save, di trú insert thẳng nên bỏ qua), 28 phòng không-cơm (đúng là không có). uyendtt.hr (phòng HCNS có rice_department) nằm trong 45 thiếu.
- [x] Command `company:enroll-rice --company= --rice-parent= [--dry-run]`: tạo rice_employee_info theo đúng logic app (EmployeeInfo.php:199-235 — chỉ phòng có rice_department + cooperation_type≠Nghiệp vụ(2)), set employee_id + rice_ssn. Chạy thật cty9: **tạo 45** (bỏ 50 đã có + 28 phòng không-cơm). Cty9 giờ 95 rice records.
- [x] Verify uyendtt.hr: rice-user-profile **200** (id=830, rice_ssn=30007), personal-registration **200**, browser hết lỗi.
- [x] Guard thêm `MasterDataService::getRiceUserProfile:86` (rice-user-profile) riceUser null → return null (28 NV phòng không-cơm không 500).

### Checkpoint — 2026-06-20 (Phase 6i — Fix rice + enroll NV thiếu — DONE)
Vừa hoàn thành: (1) Re-link 50 NV đã có rice = ĐÚNG (EG-001 render + đăng ký được). (2) Phát hiện migration THIẾU: 45 NV phòng có cơm chưa được tạo rice record (app tạo qua hook khi save, di trú bỏ qua) → command `company:enroll-rice` bù 45. (3) Guard 3 chỗ BE crash khi riceUser null (PersonalRegistrationService index + checkUserInvitation, MasterDataService getRiceUserProfile). uyendtt.hr + EG-001 + 95 rice records OK.
Bước tiếp theo: restore mật khẩu tạm uyendtt.hr + EG-001. (Quy trình cty sau: relink-rice → enroll-rice).
Blocked: (không).

## Phase 6h — Phân hệ Cơm (Rice): re-link sang tenant TPE — 2026-06-20

> User: phân hệ cơm /rice — gộp các cổng thành viên vào cổng TPE thì xử lý sao.

### Phát hiện kiến trúc (agent rà Modules/Rice)
- Cơm ĐÃ tập trung ở DB TPE: mọi entity rice_* dùng connection `mysql_tpe`. Cổng thành viên có DB HR riêng (`mysql`) nhưng ghi cơm thẳng vào DB TPE. Phân vùng theo `rice_companies.parent_id` (TPE=1, ETEK GREEN=2, POWER=3, ETEK=4 — config common.parent_company_id từ env PARENT_COMPANY_ID).
- → Cơm KHÔNG ở DB nguồn HR → di trú HR không đụng (rice_* ở skip là ĐÚNG).
- GAP: rice data ETEK GREEN (parent=2) trỏ id HR CŨ (company_id=1, employee theo local_hrm_green). Sau gộp HR→company_id=9 (parent=1): findRiceCompany(9) + riceUser() không khớp → NV gộp không truy cập được cơm.

### Xử lý (user chốt: RE-TAG sang tenant TPE)
- [x] Command `company:relink-rice --rice-parent= --new-parent= --run= --new-company= [--dry-run]`: dịch FK HR (company_id/employee_info_id/employee_id/department_id/part_id) CŨ→MỚI qua migration_id_map (DB HR) cho bảng anchored theo rice_company_id; re-tag rice_companies parent 2→1 + company_id→9 IN-PLACE (giữ id rice → lịch sử đăng ký tự link). KHÔNG đụng config chỉ-company_id (settings/menus — trùng TPE).
- [x] Chạy thật ETEK GREEN: rice_company id=2→(parent=1,company_id=9); rice_employee_infos 50 (1 DNS Admin orphan đã xóa + registrations); rice_departments 5; rice_menu_day_companies 4; rice_notifications 907. Dọn orphan.
- [x] php -l PASS.

### Verify
- [x] TPE parent=1 md5 BEFORE==AFTER (data TPE nguyên vẹn) — scope chặt chỉ parent=2/rice_company_id=2.
- [x] 50/50 NV cơm: employee_info_id + employee_id hợp lệ cty9 (findRiceCompany + riceUser resolve). 350 đăng ký giữ link. Mẫu resolve đúng tên (EG-001 Ngô Cao Vinh...).
- [x] **Config tables (user chốt: DÙNG CONFIG TPE) — TỰ ĐỘNG, KHÔNG cần thay đổi data**: phát hiện rice_settings là GLOBAL (26 key, SettingService:33 query theo `column_name` KHÔNG có company_id) + rice_menus/menu_days đều company_id=1 (CENTRAL). Menu thường = global theo ngày (PersonalRegistrationService:98-104: regular + party is_all_company → mọi NV; chỉ party theo-cty-cụ-thể cần rice_menu_day_companies). → ETEK GREEN khi còn cổng riêng VỐN đã dùng chung config trung tâm này (cùng connect mysql_tpe). Company 9 (rice_company tenant TPE) tự thừa hưởng settings + menu như 715 NV TPE. "Flagged config tables" thực chất là config TRUNG TÂM của TPE, KHÔNG phải riêng ETEK GREEN → không có gì để migrate/clean. (3 dòng rice_menu_day_companies = party quá khứ 2025, vô hại, giữ; rice_working_positions 10 được tham chiếu rice_employee_infos.rice_working_position_id → giữ.)
- [ ] Vận hành khi gộp production: gỡ domain cổng thành viên khỏi RICE_REGISTER_DOMAINS; rà USE_COMMON_CATALOG (working position mapping).

### Checkpoint — 2026-06-20 (Phase 6h — Re-link cơm — DONE core)
Vừa hoàn thành: Hiểu kiến trúc cơm (đã tập trung DB TPE, phân vùng parent_id). Command company:relink-rice re-tag ETEK GREEN (parent 2→1, company 1→9) + dịch FK HR qua map. Verify: TPE nguyên vẹn, 50 NV + 350 đăng ký link sống về cty9. Config tables (settings/menus) flag xử lý tay.
Bước tiếp theo: quyết định config tables (dùng TPE hay re-tag tay) + vận hành (RICE_REGISTER_DOMAINS, ssn dải). Tài liệu: audit-phan-he.md mục Cơm.
Blocked: (không).

## Phase 6g — Fix miễn chấm công crash + cascade loại child + AUDIT phân hệ — 2026-06-20

> User: audit toàn bộ thiết lập các phân hệ (cái nào chuyển/per-company, cái nào dùng chung đích). + API /timekeeping-exemptions lỗi "Trying to get property 'department' of non-object".

### Bug miễn chấm công (2 lỗi)
- [x] **Resource bug**: `TimekeepingExemptionResourceListResource.php:30,32,34,36` không guard null employee (dòng 24-29 có guard) → crash khi employeeInfo null. Fix: thêm `($employee && ...)`.
- [x] **Migration data bug**: dòng miễn chấm công của DNS Admin (employee_info 6 = namdangit, bị loại email-đụng) được di trú với employee_id=NULL → orphan. Root-cause: `filterExcludedRows` chỉ loại ở bảng employee_infos/employees, KHÔNG cascade sang con. Xóa orphan cty9 (id=68) + map.
- [x] **Engine fix (general)**: `selectOldIdsNonParent` + helper `personOwnerFkColumns` → loại dòng có cột CHỦ SỞ HỮU (`employee_id`/`employee_info_id` trần, KHÔNG tính lead/deputy/owner/audit) trỏ người bị loại. (Đã thu hẹp: ban đầu quá rộng làm rớt parts vì part_lead_id — sửa chỉ nhận 2 cột owner.) Verify: parts.part_lead_id của DNS Admin chỉ NULL (7 parts vẫn còn), employee_attendances/devices/company_employees 0 orphan.
- [x] php -l + 75 unit test xanh.

### AUDIT toàn phân hệ
- [x] Phân loại: 94 OWNED (per-company, đối chiếu nguồn↔đích KHỚP 100% trừ DNS Admin) / 9 SHARED (địa lý/bank/quyền/majors/areas — dùng của đích) / 185 SKIP (giao dịch + config global không company_id).
- [x] Quy tắc vàng: CÓ company_id = riêng→chuyển; KHÔNG = chung→dùng đích. Verify config-skip (master_settings/print_templates/meeting_types/bom_price_approval_configs) đều không company_id → global → skip đúng.
- [x] Tài liệu: `.plans/di-tru-du-lieu-cong-ty/audit-phan-he.md` (bảng theo 7 phân hệ + 6 gap đã xử lý).

### Checkpoint — 2026-06-20 (Phase 6g — Audit + fix miễn chấm công — DONE)
Vừa hoàn thành: Fix crash màn miễn chấm công (resource null-guard + xóa orphan DNS Admin) + engine cascade loại child theo người bị loại (personOwnerFkColumns, chỉ cột owner). Audit toàn diện: 94 owned khớp 100%, 9 shared dùng đích, 185 skip đúng (giao dịch/global). Tài liệu audit-phan-he.md. 75 test xanh.
Bước tiếp theo: (đề xuất) endpoint /timekeeping-exemptions không scope theo công ty (trả mọi cty) — nếu muốn lọc cty thì sửa controller; không phải lỗi di trú.
Blocked: (không).

## Phase 6f — Chi tiết phân ca (membership + roster tương lai) — 2026-06-20

> User: màn timesheet/timeworking/shift-detail/general phân ca chưa đưa. shift_details (mẫu, 8) đã OWNED nhưng con bị skip → phân ca rỗng + chấm công thiếu roster (TimesheetService đọc shift_detail_employee_dates). User chốt: đưa membership + roster TƯƠNG LAI (bỏ kỳ cũ).

### BE
- [x] Khai owned: `shift_detail_employees` (filter=parent) + `shift_detail_employee_dates` (filter=parent + `date_from_today=date` → chỉ roster ≥ hôm nay). Bỏ khỏi skip. (shift_detail_employee_date_employees không tồn tại nguồn; shift_detail_dates rỗng → giữ skip.)
- [x] Engine: `stepAllocateIds` thêm `$seedChosen` (nạp old_id cha đã di trú từ map run cũ — vì runMigrationForTables không có cha trong tập con) + helper `loadParentOldIdsFromMap`. `selectOldIdsParent` thêm filter `date_from_today` (chỉ ≥ hôm nay). 
- [x] **FIX BUG idempotent guard**: dry-run cũng allocate + cleanupMapForTables → XÓA NHẦM map thật của lần chạy trước. Đổi guard chặn CẢ dry-run khi đã có map (trước chỉ chặn real). (Đã phát sinh + tự repair: xóa 101 dòng shift_detail_employees mồ côi.)
- [x] php -l + 75 unit test xanh.

### Verify
- [x] Chạy thật cty9: shift_detail_employees=101, shift_detail_employee_dates=**25025** (chỉ tương lai, từ 54690 nguồn bỏ ~29k kỳ cũ). fk_null=0.
- [x] DB: roster ngày 2026-06-20→2027-06-16 (≥ hôm nay), 0 FK dangling (employee/working_shift đều thuộc cty9). 89 NV có ca mỗi ngày làm việc (21/06 CN không ca — đúng).
- [x] Guard fix: dry-run trên bảng đã migrate (shift_detail_employees + customers) đều bị CHẶN đúng.
- [x] Browser /shift-detail/general: hiện 72 NV ETEK GREEN + lưới phân ca (ô 01-17/06 trống vì roster chỉ từ 20/06 — đúng thiết kế future-only).

### Checkpoint — 2026-06-20 (Phase 6f — Phân ca — DONE)
Vừa hoàn thành: Đưa membership + roster tương lai phân ca cho cty9 (25126 dòng). Engine extend: seedChosen (cha từ map run cũ) + filter date_from_today. FIX bug guard (dry-run xóa nhầm map thật) + tự repair. Verify DB + browser OK. 75 test xanh.
Bước tiếp theo: Công ty sau tự đưa khi runMigration (2 bảng đã owned). Nếu cần cả lịch sử → bỏ directive date_from_today.
Blocked: (không).

## Phase 6e — Hạ quyền "tổng công ty" → "theo công ty" (chống xem chéo công ty) — 2026-06-20

> User: nguồn 1 công ty nên quyền "tổng công ty" = chính nó; sang đích nhiều công ty thì "tổng công ty" cho NV di trú XEM ĐƯỢC công ty khác đã tồn tại → hạ xuống "theo công ty".

### Phân tích
- Enforcement: `checkPermissionList` (app/Helper/PermissionHelper.php:133-145): `permissions[0]`="tổng công ty" → query KHÔNG lọc (xem mọi cty); `permissions[1]`="theo công ty" → lọc `company_id=current_company_role` (=9). Mỗi feature 4 cấp: tổng cty/công ty/phòng ban/bộ phận.
- Naming KHÔNG đồng nhất: "theo tổng công ty", "- tổng công ty" (gạch nối), vài quyền cũ name "Xem tất cả ..." (display "theo tổng công ty"). → dò twin bằng CHUỖI pattern, ưu tiên display_name. Đo cty9: 94 quyền top-scope distinct, 94/94 có twin "theo công ty".
- Chỉ `role_has_permissions` (employee_has_permissions không có company_id + rỗng cty9). Roles cty9: Super Admin (ETEK GREEN), Admin, Quản lý.

### BE
- [x] `CompanyMigrationService::downgradeGroupScopePermissions(companyId, dryRun)` — dựng twinMap (chuỗi pattern), với mỗi dòng role_has_permissions top-scope của cty: nếu role đã có twin → DELETE dòng top-scope; chưa có → UPDATE permission_id=twin. Idempotent. Báo cáo converted/deleted_dup/granted_unmapped.
- [x] Command `company:downgrade-permissions --company= [--dry-run]`. Tích hợp post-commit trong runMigration (config `downgrade_group_scope_on_migrate=true` mặc định BẬT). php -l + 75 test xanh.

### Verify
- [x] Chạy thật cty9: 108 dòng top-scope → 14 UPDATE + 94 xóa-trùng (role đã có twin). 0 unmapped.
- [x] DB: cty9 còn **0 quyền top-scope** (đạt). Idempotent: chạy lại = 0.
- [x] **End-to-end API**: `/human/customers` cho uyendtt.hr (Super Admin ETEK GREEN) TRƯỚC = 41643 KH (mọi cty) → SAU = **1 KH** (chỉ BVTL cty9). Xác nhận không còn xem chéo công ty.
- [x] **Verify mở rộng nhiều màn scoped** (uyendtt.hr): `/human/employee` (tài khoản) = **122** (TRƯỚC 1198 toàn hệ thống), `/human/employee-infos` (hồ sơ NS) = **123**, đều = đúng cty9. Browser /human/employee: "Tổng số 122", danh sách toàn NV EG-/etekgreen.com (không cty Tân Phát khác). → Giải quyết luôn ghi chú cũ "super-admin thấy 1198 tài khoản" (hóa ra là quyền tổng-công-ty di trú, KHÔNG phải app behavior).

### Checkpoint — 2026-06-20 (Phase 6e — Hạ quyền tổng-công-ty — DONE)
Vừa hoàn thành: Hạ mọi quyền "tổng công ты" của cty9 xuống "theo công ты" (chống NV di trú xem dữ liệu công ty khác ở đích). Method downgradeGroupScopePermissions (dò twin chuỗi pattern, idempotent) + command + tích hợp runMigration post-commit (config bật mặc định). Verify: cty9 0 top-scope còn lại; /human/customers 41643→1. 75 test xanh.
Bước tiếp theo: Công ty sau tự hạ quyền khi runMigration. Nếu công ty cần quyền toàn hệ thống → set config downgrade_group_scope_on_migrate=false.
Blocked: (không).

## Phase 6d — Đưa cụm danh mục Khách hàng / Ngành (sửa bỏ-nhầm "CRM") — 2026-06-20

> User hỏi /human/customers đã đưa qua chưa → CHƯA (bảng customers bị bỏ chung cụm "CRM"). Nhưng customers (màn Human) + customer_scopes/scopes/industries (module Giao việc/Danh mục) còn dùng → bỏ nhầm. User chốt: ĐƯA cả cụm danh mục, giữ skip workflow giao dịch.

### BE
- [x] Khai 6 bảng vào catalog `owned` (config/company_migration.php) với FK directive đầy đủ: customer_scope_groups, customer_scopes, scopes, industries, industry_scopes (pivot, filter=parent), customers (self-ref parent_id + scope FK + geo SHARED + hamlet SET_NULL + SoftDeletes). Bỏ 6 bảng khỏi `skip`.
- [x] `.env` MIGRATE_CRM=true (cờ optionalModuleTables['crm'] đã liệt kê đúng 6 bảng → bật/tắt qua cờ). Công ty sau tự đưa khi runMigration nếu cờ bật.
- [x] `CompanyMigrationService::runMigrationForTables(source, run, onlyTables[], dryRun)` — di trú BỔ SUNG tập con cho công ty ĐÃ di trú, tái dùng migration_id_map run cũ (dịch FK departments/employees/...), idempotent guard (đã có map → chặn), cleanup CHỈ scoped theo tập con (không phá map gốc) + `cleanupMapForTables`. Command `company:migrate-tables`.
- [x] php -l PASS + 75 unit test xanh.

### Verify
- [x] Dry-run + chạy thật cty9 (run etekgreen): 314 dòng (customer_scopes 59 / scopes 19 / industries 117 / industry_scopes 118 / customers 1 / groups 0). fk_null=392 = created_by/updated_by=13 (user hệ thống không di trú — hợp lệ, y main migration). department_id map đúng (4→126, 1→123).
- [x] DB integrity: counts khớp source 100%; customer.department_id thuộc cty9; industry_scopes scope_id dangling=0; id liền mạch.
- [x] Idempotent: chạy lại bị chặn đúng.
- [x] API + Browser /human/customers: "CÔNG TY BẢO VIỆT THĂNG LONG" (BVTL_ETEKGREEN) hiện đúng, geo Hà Nội/Láng Thượng (SHARED map đúng). (Mã suffix _ETEKGREEN do unique-guard tránh đụng code.)
- Lưu ý: màn hiện 41643 KH (super-admin thấy mọi cty — phân quyền sẵn có app, KHÔNG phải lỗi di trú); cty9 thực có đúng 1 KH.

### Checkpoint — 2026-06-20 (Phase 6d — Cụm danh mục KH/Ngành — DONE)
Vừa hoàn thành: Đưa lại cụm customers/customer_scopes/customer_scope_groups/scopes/industries/industry_scopes (bỏ nhầm theo "CRM"). Thêm vào catalog owned + bật MIGRATE_CRM + method runMigrationForTables + command company:migrate-tables (di trú bổ sung cho cty đã di trú, idempotent, cleanup scoped). Chạy thật cty9: 314 dòng, integrity sạch, verify API+browser /human/customers OK. 75 test xanh.
Bước tiếp theo: Công ty sau tự đưa cụm này khi runMigration (MIGRATE_CRM=true). Nếu công ty nào KHÔNG dùng → set MIGRATE_CRM=false trước khi seed.
Blocked: (không).

### Checkpoint — 2026-06-20 (Phase 6c — Audit toàn project — DONE)
Vừa hoàn thành: Audit toàn bộ project (2 agent Opus). Kết luận KHÔNG có lỗi data-correctness dai dẳng nào ngoài phép (đã fix) + cron (đã guard) + overtime (chấp nhận). Payroll an toàn 100%. Thâm niên moot (nguồn rỗng). Ghi checklist tiền-di-trú cho công ty sau. Verify browser PASS.
Bước tiếp theo: (khi sẵn sàng) chạy PRODUCTION. Mỗi công ty mới: thêm config leave_recompute_skip + chạy checklist thâm niên + fold tự chạy trong runMigration.
Blocked: (không).

---

## Checkpoint — 2026-06-18 (engine + fix review)
Vừa hoàn thành: Phase 0-4 code DONE + review đối kháng + FIX. Review tìm 4 Critical → ĐÃ FIX: C4 (bump AUTO_INCREMENT sau commit, không DDL trong transaction), C1 (cột *_id/_by chưa khai → NULL + báo cáo uncovered_fk; đổi KEEP→SET_NULL các FK dangling), C3 (bảng id-less filter=parent lọc theo cha trong query), I4 (JSON id fail→NULL, không giữ id nguồn), I2 (roles CÓ company_id→giữ TARGET). Sửa thêm directive working_position_order→OWNED:working_positions (verify id khớp working_positions). 46 unit test xanh; DRY-RUN lại: uncovered_fk RỖNG, số dòng vẫn đúng (companies=1/employee_infos=123/employees=122), migration_id_map dọn sạch, companies đích=8 (không ghi).

## Checkpoint — 2026-06-20 (CHẠY THẬT LOCAL + VERIFY UI — DONE)
Vừa hoàn thành: User chạy thật trên LOCAL thành công sau khi vòng test-trên-copy fix hết các lỗi INSERT mà dry-run không bắt được (unique guard suffix khi đụng: titles.name 6/competencies 34/priority_levels 4/attachment_types 8/ranks 2/wpg 4/roles tuple 1; check `<>''` image→'-'; NOT NULL nhận NULL: 547 giá trị ép 0/omit; bump bỏ qua bảng id-less). 76 unit test xanh. Verify trực tiếp DB hrm_prod_local: company 9 đếm khớp 100%, integrity 0 lỗi, id liền mạch (max 1717), công ty cũ nguyên vẹn. Verify UI bằng Playwright (Python, FE :3000): login OK (dashboard "Xin chào Ngô Cao Vinh"), JWT current_company=9, ảnh S3 load; admin di trú uyendtt.hr (Super Admin (ETEK GREEN)) thấy đúng 6 Khối ETEK GREEN; NV thường bị chặn màn quản trị (phân quyền đúng). Đã đặt mật khẩu tạm `Test@12345` cho uyendtt.hr@etekgreen.com (theo yêu cầu user — CHƯA khôi phục, để user login).
Đang làm dở: (không) — di trú LOCAL hoàn tất + verify toàn diện.
Bước tiếp theo: (khi user sẵn sàng) chạy PRODUCTION: backup + bật bảo trì + MIGRATION_RUN_ID mới mỗi công ty. Tái dùng cho công ty kế: sửa .env (DB_DATABASE_SOURCE + MIGRATION_RUN_ID + cờ MIGRATE_*).
Lưu ý: super-admin thấy toàn bộ tài khoản mọi công ty ở màn "Danh sách tài khoản" là phân quyền sẵn có của app (KHÔNG phải lỗi di trú); muốn lọc theo công ty thì sửa logic app riêng.
Blocked: (không).

---

## Phase 7 — Chạy lại & đánh giá theo bảng feedback TPE (2026-09-04)

- [x] Đọc bảng feedback TPE (Google Sheet "Bảng xử lý và test dữ liệu gộp cổng", sheet `HRM_Test gộp cổng ETEK, EP, EG`)
- [x] Backup `hrm_prod_6_6` trước khi chạy (1.1G)
- [x] Chạy `company:migrate-full` dry-run + ghi thật cho ETEK GREEN (`local_hrm_green` → company_id mới = 9)
- [x] Verify bằng SQL toàn bộ mục "Chờ sửa" trong bảng feedback
- [x] Viết báo cáo `danh-gia-lai-2026-09-04.md` + bảng nhận xét cột L để dán lên Sheet

### Checkpoint — 2026-09-04 (Phase 7 — test UI thật)
Vừa hoàn thành: Test bằng Playwright với 2 tài khoản (admin EG uyendtt.hr@etekgreen.com — cty 9, admin tổng namdangit — cty 1). Phát hiện 14 mục CÒN LỖI, trong đó nặng nhất: (1) config map sai bảng `working_position_group_id` → OWNED:working_position_groups (phải là rank_groups) làm màn Định biên hiện nhầm nhóm "LÃNH ĐẠO." của TPE; (2) manpower_report lỗi 500 tại DepartmentManpowerService.php:228 do global scope; (3) AttendanceService::approve() không lọc company → admin EG duyệt được 14 đơn của TPE. Xác nhận ĐÃ HẾT LỖI có bằng chứng UI: dòng 58 (quy định làm thêm), 99 (báo cáo phép), 122/123/125 (cơm). Dòng 45 tìm ra nguyên nhân: NV kiêm nhiệm đếm 2 lần, không phải lỗi di trú.
Bước tiếp theo: Sửa 7 việc engine + 4 việc app theo mục 5 của danh-gia-lai-2026-09-04.md; chờ TPE chốt việc gộp đơn/phiếu chờ duyệt (dòng 74-93).
Blocked: (không).

### Checkpoint — 2026-09-04 (Phase 7b — SỬA XONG các lỗi phát hiện)
Vừa hoàn thành: Sửa 15 mục lỗi (7 engine + 8 app), chạy lại di trú 3 lần để kiểm chứng, 75 unit test xanh.
- Engine (config/company_migration.php + CompanyMigrationService): (1) working_position_group_id -> OWNED:rank_groups + sắp lại thứ tự bảng (competency_groups > rank_groups > ranks trước working_positions/department_manpowers) → định biên 29/29 đúng nhóm; (2) normalizeBankName cho danh mục ngân hàng → bank_id NV 2/4 → 3/4; (3) absolutizeAssetPath + config source_asset_base_url → ảnh 124/125 URL đầy đủ; (4) stepFreeCompanyName (đổi tên bản ghi đích trùng, chỉ khi status=0) đặt TRƯỚC resolveCompanyName/detectUniqueGuards → công ty mới lấy tên gốc, bản cũ thành "(cũ)"; (5) labor_contracts filter thêm "OR company_id IS NULL" → 5 loại HĐ; (6) audit_fallback_employee_id → titles 67/67, industries 117/117 có Người tạo; (7) migrationConfig() an toàn ngoài container (fix 3 unit test).
- App (lỗ hổng chỉ lộ sau gộp cổng): AttendanceService::approve lọc company (EG 14 đơn TPE → 0); LocationConnInfo + ConnInfo thêm FilterByCompanyManagerScope (9→5 địa điểm, máy CC chỉ còn 3); CompanyService::getCompanies + helper listManageCompanyIdsForCurrentEmployee (EG 9→1 công ty); SelfNotificationService::index (EG 10→0 thông báo TPE); SalaryTemplateService index+getAllList; DepartmentManpowerService guard quan hệ NULL (500 → 200); CompetencyService::isUsed + RankService::isRankGroupUsed (chặn xoá danh mục đang dùng, message rõ).
- Excel bàn giao: thêm cột M "Hướng sửa & kiểm chứng", cột L cập nhật trạng thái.
Bước tiếp theo: chờ TPE chốt 3 việc — gộp đơn/phiếu chờ duyệt (dòng 74-93), thực đơn cơm cho công ty gộp (dòng 121), có bỏ ràng buộc trùng tên danh mục toàn hệ thống không (31 danh mục còn hậu tố). TPE cần gán quyền công ty mới cho quản trị TPE + cấp quyền cơm cho công ty gộp.
Blocked: (không).

### Checkpoint — 2026-09-05 (bổ sung danh mục dùng chung còn thiếu ở đích)
Vừa hoàn thành: Thêm cơ chế `insert_missing` cho danh mục SHARED (CompanyMigrationService::insertMissingSharedRows + config banks). Trước đây SHARED chỉ map theo khoá tự nhiên, ngân hàng nào chỉ cổng thành viên có (OCB, VIB) thì map ra NULL → NV mất tài khoản ngân hàng. Nay tự chèn vào danh mục đích (bỏ qua dòng đụng unique code) rồi map tiếp; buildSharedMap nhận thêm $dryRun để dry-run không ghi. Kiểm chứng: banks đích 19→21, UI hiện đủ 21 gồm OCB + VIB; tài khoản NV EG 3/4 có ngân hàng (dòng thứ 4 ở nguồn vốn bank_id=0).
Đồng thời TRẢ LẠI filter labor_contracts về 'company_id=1' — chốt dùng chung, chèn thêm chỉ gây 4 cặp trùng tên và 0 bản ghi tham chiếu.
Bước tiếp theo: cân nhắc bật insert_missing cho danh mục dùng chung khác (majors, areas) nếu công ty sau có tình huống tương tự.
Blocked: (không).

### Checkpoint — 2026-09-05 (dòng 21: lọc công ty ở NGUỒN CHUNG của mọi ô lọc)
Vừa hoàn thành: TPE phát hiện màn /timesheet/timesheet_details vẫn xổ đủ công ty dù đã sửa dòng 21. Truy ra: mọi ô lọc trên FE lấy dữ liệu từ store.companies/departments/parts/groups, nạp 1 lần từ API `users/auth/user-profile` (app/Http/Controllers/Api/AuthNewController.php) — trước đây trả TOÀN BỘ không lọc. Đã lọc cả 4 danh sách theo listManageCompanyIdsForCurrentEmployee() + luôn kèm current_company_role. Kiểm chứng UI màn Bảng công chi tiết (EG): công ty 9→1, phòng ban 75→12, bộ phận 57→42, khối 3. TPE không đổi: 5 công ty / 55 phòng ban. 75 test xanh.
Bài học: sửa gate công ty phải truy tới NGUỒN DỮ LIỆU CHUNG (user-profile), không chỉ sửa service của từng màn.
Blocked: (không).

### Checkpoint — 2026-09-05 (CHỐT với TPE: ô lọc giữ nguyên, chặn bằng phân quyền)
Vừa hoàn thành: TPE chốt KHÔNG lọc danh sách đổ vào ô lọc (công ty/phòng ban/bộ phận/khối) — ai có quyền cấp tổng công ty phải chọn được mọi công ty. Đã REVERT phần lọc ở AuthNewController::userProfile (giữ lại chú thích giải thích để sau không sửa nhầm lần nữa). GIỮ fix ở màn Danh mục công ty (CompanyService::getCompanies) vì J21 chốt Dùng riêng.
Cơ chế chặn xem chéo = hạ quyền "theo tổng công ty" -> "theo công ty" khi di trú (EG: 4 quyền). Kiểm chứng: ô lọc EG hiện đủ 6 công ty / 75 phòng ban NHƯNG Bảng công chi tiết chỉ trả 71 nhân sự, 100% company_id=9.
Bước tiếp theo: quét 211 endpoint các phân hệ Assign/Training/Decision/Rice/Payroll tìm chỗ còn trả dữ liệu công ty khác (script đã viết: scratchpad/scan.py + paths.txt).
Blocked: (không).

### Checkpoint — 2026-09-05 (ảnh: đẩy lên S3 thay vì trỏ cổng cũ)
Vừa hoàn thành: TPE yêu cầu không phụ thuộc cổng cũ (sẽ tắt). Thêm bước kéo ảnh lên S3 chung:
- CmcS3Helper::putContents() — đẩy nội dung file (không cần UploadedFile)
- CompanyMigrationService::uploadMigratedAssetsToS3() + rehostAssetValue/rehostOneAsset — duyệt image_columns_keep theo migration_id_map, bỏ qua ảnh đã ở kho chung, hỗ trợ cột JSON mảng ảnh; lấy file ưu tiên MIGRATION_SOURCE_ASSET_DIR rồi tới MIGRATION_SOURCE_ASSET_URL; lỗi thì giữ nguyên + liệt kê
- Gọi post-commit trong runMigration khi MIGRATION_UPLOAD_ASSETS_TO_S3=true + lệnh riêng company:upload-assets --run=<id> [--dir=] [--base-url=] [--dry-run]
Kiểm chứng: 162 ô ảnh EG → 147 đã ở kho chung, 5 có file nguồn đẩy lên S3 OK (tải lại HTTP 200), chạy lần 2 đẩy 0 (idempotent). Đã XOÁ toàn bộ file test khỏi bucket khách (xác nhận HTTP 403). 75 test xanh.
Bước tiếp theo: khi chạy thật, TPE cấp thư mục sao lưu uploads của cổng cũ HOẶC chạy khi cổng cũ còn sống.
Blocked: (không).

### Checkpoint — 2026-09-05 (đưa ĐƠN XIN NGHỈ còn giá trị sang cổng mới)
Vừa hoàn thành: TPE chốt đưa sang đơn đã duyệt có ngày nghỉ tương lai + đơn chờ duyệt.
- Bỏ 'attendances' khỏi skip; thêm vào owned SAU 'employees' (để map created_by), filter mới `pending_or_future:<cột trạng thái>:<cột ngày>:<chờ>:<đã duyệt>`
- FK: employee_id & substituter_id -> OWNED:employee_infos (KHÔNG phải employees — đối chiếu 962/962, 948/948), leave_type_id -> leave_types
- Thêm config cutover_date + option --cutover-date (mặc định ngày chạy lệnh)
Kiểm chứng: dựng 12 đơn giả phủ các nhánh -> ĐÚNG 12/12 (gồm 2 case biên: kết thúc đúng ngày cutover / trước 1 ngày; đơn của người bị loại; người thay thế bị loại). FK sạch 0 lệch công ty. UI: admin EG thấy 15 đơn toàn phòng ban EG. Đã xoá đơn giả khỏi DB nguồn, chạy lại sạch, xoá file ảnh test khỏi S3. 75 test xanh.
Bước tiếp theo: các loại phiếu khác (làm thêm, công tác, tra soát công) dùng cùng cơ chế filter — làm khi TPE xác nhận cần.
Blocked: (không).

### Checkpoint — 2026-09-05 (hướng B: đưa dữ liệu chấm công 2026 sang)
Vừa hoàn thành: TPE chốt hướng B. Đưa 4 bảng chấm công vào owned với mốc từ config timesheet_from_date:
- timesheet_summaries (filter 'parent' + directive mới 'date_from'), timesheets (filter 'company_id=N AND from_date:verify_date', poly_fk job_id cho workshift), timesheet_month_summaries, timesheet_month_summary_detail
- Thêm filter 'from_date:<col>' + directive 'date_from' + config timesheet_from_date + option --timesheet-from
- foldPreCutoverUsedLeave TỰ THU HẸP khoảng bù khi đã gộp chấm công (gộp trọn năm -> bù 0), tránh trừ phép 2 lần
Kiểm chứng đối chiếu nguồn: báo cáo phép khớp TỪNG THÁNG; chấm công chi tiết T3 (phép 72,5 / công 1.357,5) khớp; báo cáo tổng hợp chấm công T3 (2.130 phút, 129 lần muộn, 50,5 ngày nghỉ không lý do) khớp; 4 kỳ công khớp. Chênh lệch duy nhất = dữ liệu của DNS Admin bị loại có chủ đích (410 lần quẹt thẻ + 3 dòng kỳ công). 75 test xanh.
Lưu ý: khối lượng 25.294 -> 60.596 dòng, lệnh chạy lâu hơn.
Blocked: (không).

### Checkpoint — 2026-09-05 (phân hệ cơm: 2 lỗi nghiêm trọng)
Vừa hoàn thành: TPE báo /rice/personal-registration lỗi. Rà lại toàn bộ phân hệ cơm:
1. Entity Rice dùng connection RIÊNG 'mysql_tpe'. Sau gộp, DB cơm PHẢI = DB nhân sự; local user để lệch (hrm_prod_local vs hrm_prod_6_6) -> relink ghi 1 nơi, app đọc nơi khác -> findRiceCompany() trả null -> "Trying to get property 'id' of non-object". Đã thêm GUARD chặn ở CompanyMigrateFull + CompanyRelinkRice (in rõ 2 DB + cách sửa) và sửa .env local (đã backup .env).
2. NGHIÊM TRỌNG: translateCol trong relink giữ NGUYÊN id cũ khi không map được -> 19 hồ sơ cơm EG trỏ nhầm sang nhân sự TPE (id trùng nhau giữa 2 DB). Nay NGẮT LIÊN KẾT (cột nullable -> null, NOT NULL -> 0) + in danh sách để rà. TPE chốt "ngắt liên kết, giữ dòng".
Kiểm chứng: 125 hồ sơ nối đúng, 19 đã ngắt, 0 trỏ nhầm công ty khác, 0 bản ghi công ty khác bị đụng, 7.551 đăng ký giữ nguyên; màn cơm mở OK cả 2 tài khoản. 75 test xanh.
Còn chờ TPE: thực đơn/máy check-in cho công ty thành viên; xử lý 19 hồ sơ cơm mồ côi.
Blocked: (không).

### Checkpoint — 2026-09-07 (UAT chạy thật xong + bổ sung bảng lương/chi trả)
Vừa hoàn thành:
- Merge dong_bo_du_lieu -> tpe, push origin/tpe (4 lần: merge, fix preview bù phép, fix trùng mã ngân hàng, thêm bảng lương/chi trả)
- Fix phát sinh trên UAT: (1) preview dry-run tính bù phép không xét timesheet_from_date -> báo 528 ngày trong khi chạy thật bù 0; (2) insertMissingSharedRows đọc SAI cấu trúc detectUniqueGuards (thiếu khoá 'single') -> không kiểm unique -> lỗi Duplicate entry 'SHB'; kèm chuẩn hoá dấu gạch (– vs -) trong tên ngân hàng
- UAT chạy thật THÀNH CÔNG: 78.061 dòng, bù phép 0, company_id mới = 9, cơm 128 nối/16 ngắt, recode 128 NV, ERP đẩy đủ (16 phòng ban, 66 bộ phận, 128 hồ sơ, 127 tài khoản)
- Thêm chuỗi 5 bảng lương/chi trả (salary, salary_employees, salary_employee_data, payments, payment_employees). salary_employees.employee_id trỏ employee_infos — bẫy thứ 3 cùng kiểu. Chạy bổ sung bằng company:migrate-tables (KHÔNG cần nạp lại DB). UAT: 21 dòng, fk_null=0.
Bước tiếp theo: TPE kiểm trên giao diện UAT; xử lý ảnh bằng company:upload-assets khi có nguồn ảnh.
Blocked: (không).

### Checkpoint — 2026-09-10 (lỗi đăng nhập ERP sau gộp cổng)
Vừa hoàn thành: TPE báo tài khoản ETEK GREEN vào ERP UAT bị "lỗi đỏ, load lại là out". Chẩn đoán qua SSH (hrm.eteksofts.com:2230, erp.eteksofts.com:2231 — user erp_tpe, có sẵn SSH key):
- Loại trừ: tài khoản CÓ bên uat_erp (id 1121), JWT_SECRET 2 bên KHỚP, SSO redirect đúng, đăng nhập HRM OK
- Tái hiện bằng Playwright: vào được lần đầu, navigate lại → bị đá về HRM login
- Nguyên nhân: UserLogIn::checkTokenVersion so token_version trong JWT (HRM cấp) với employees.token_version bên ERP. HRM uyendtt=2 / namdangit=10, ERP đều =1 → lệch → logout
- Gốc: SyncEmployeeToErpJob chỉ chép email/status/password, BỎ SÓT token_version (2 luồng đổi mật khẩu EmployeeService:257 + AuthNewController:103 thì đã có sync). Lỗi có sẵn, không do gộp cổng — TPE cũng dính
- Xử lý: (A) đồng bộ tay 127 tài khoản trên UAT (backup /tmp/tv_erp_backup.csv trên server HRM) → hết văng; (B) sửa gốc: thêm token_version vào SyncEmployeeToErpJob (guard Schema::hasColumn)
- Kiểm chứng local: làm lệch 124 tài khoản → chạy company:sync-erp → 0 lệch. 75 test xanh
Bước tiếp theo: CHƯA COMMIT/PUSH — chờ user duyệt.
Blocked: (không).

### Checkpoint — 2026-09-10 (đồng bộ token_version TOÀN BỘ UAT)
Vừa hoàn thành: rà token_version trên UAT theo email cho TẤT CẢ nhân sự (không chỉ công ty 9).
- Đo trước: HRM 1.220 tài khoản / ERP 1.157, trùng email 1.147 → LỆCH 45 (toàn bộ là @tanphat.com, dạng HRM=2/3 vs ERP=1). Đây là tồn đọng cũ của lỗi SyncEmployeeToErpJob thiếu token_version, không do gộp cổng.
- Backup ERP trước khi sửa: /tmp/tv_erp_backup_all_20260910.csv (1.157 dòng) trên server hrm.eteksofts.com:2230; câu lệnh đã dùng: /tmp/fix_tv.sql (45 UPDATE, chỉ ghi đúng tài khoản lệch).
- Sau khi chạy: CÒN LỆCH = 0. Kiểm mẫu: namdangit=10, chinhnv.ptgd=3, uyendtt.hr=2 (khớp HRM).
- Chênh danh sách còn lại (KHÔNG phải lỗi): 73 tài khoản chỉ có ở HRM (cty 1:48, 4:14, 8:5, 3:4, 2:2 — KHÔNG có công ty 9, tức 124 tài khoản ETEK GREEN đã sang ERP đủ) và 10 tài khoản chỉ có ở ERP. Đều là dữ liệu cũ của Tân Phát, ngoài phạm vi gộp cổng.
- Lưu ý dữ liệu bẩn phát hiện được: HRM có 1 email bắt đầu bằng dấu nháy đơn: 'huongttt.kddau@tanphat.com — nên rà lại.
Bước tiếp theo: bản sửa gốc SyncEmployeeToErpJob.php VẪN CHƯA COMMIT/PUSH — chờ user duyệt.
Blocked: (không).

### Checkpoint — 2026-09-10 (bù dữ liệu công ty + cơ cấu tổ chức sang ERP)
Vừa hoàn thành: TPE phát hiện màn ERP /admin/companies/9/edit trống dữ liệu so với cổng nguồn erp.etekgreen.com.
Rà bằng script so từng cột chung hrm_uat <-> uat_erp cho công ty 9 (/tmp/gap.py trên server HRM UAT).
- companies: company:sync-erp chỉ mirror 12 cột, sót 9 (tax_code, website, fax, logo, header, district_id, apartment_number, deputy_name, deputy_role). Nguy hiểm nhất là logo/header -> bản in ERP mất letterhead.
- module_mappings bên ERP trống hoàn toàn cho công ty 9 (hook created() ghi bảng này nhưng engine di trú INSERT thẳng). Thêm helper mapErp() cho 5 loại, dùng updateOrInsert.
- Cơ cấu tổ chức còn 6 cột HRM CÓ mà ERP trống: departments.position, parts.part_lead_id, employee_infos.academic_level / vacation_start_date_type / created_by / bank_branch.
- deputy_name: HRM lưu bằng deputy_id (FK employee_infos), ERP lưu bằng TÊN -> tra tên. Ra "Ngô Cao Vinh", khớp cổng nguồn.
- KHÔNG chép deputy_role: id ERP trỏ danh mục khác working_positions của HRM (ERP cty 1 = 43 = "Chuyên viên Kinh doanh", sai nghĩa).
- Sửa nhánh ngân hàng của SyncEmployeeInfoToErpJob: có dòng employee_bank_accounts nhưng bank_branch_id NULL thì đừng ghi null đè cột cũ (gặp thật: hồ sơ 1737 Phạm Vũ Bích Liên).
3 commit đã đẩy origin/tpe: 224f46c48, fc58fbc33, bacfe4fbd. Đã pull + chạy company:sync-erp --company=9 trên /var/www/uat/hrm-api.
Kiểm chứng UAT: 20/20 cột companies khớp; mapping 1/16/66/128/127; so từng dòng phòng ban / bộ phận / nhân viên = KHỚP; tài khoản khớp email+status+employee_info_id (chỉ khác employees.id vì ERP tự sinh, khớp qua employee_info_id — đúng thiết kế sẵn có).
NGOÀI PHẠM VI, chờ TPE chốt: (1) điện thoại/email/địa chỉ HRM và ERP nguồn lệch nhau từ trước; (2) ~18 trường cấu hình nghiệp vụ ERP (đơn giá công, hệ số giá, hạn mức công nợ, % hoa hồng/đặt cọc, số ngày quá hạn...) chỉ có ở ERP nguồn; (3) kho hàng ETEK GREEN chưa di trú nên "Kho hàng khuyến mại" để trống.
Bước tiếp theo: TPE kiểm giao diện ERP UAT.
Blocked: (không).

### Checkpoint — 2026-09-10 (rà toàn bộ cột id khi đẩy sang ERP)
Vừa hoàn thành: TPE báo màn ERP /admin/departments trống cột Trưởng phòng. Rà bằng script so tỷ lệ "tra ra được" của công ty 1 (chuẩn) với công ty 9 cho MỌI cột *_id được đẩy sang ERP (/tmp/idaudit.py trên server HRM UAT). Tìm 3 cột hỏng + 1 do chính mình gây ra:
1. departments.department_lead_id & parts.part_lead_id — HRM lưu theo employee_infos.id, ERP hiểu là employees.id (Department::departmentLead(), Part::part_lead() đều belongsTo Employee). Cty1 31/31 và 9/9 tra được, cty9 0/15 và 0/61. Nguy hiểm: dải id chồng nhau là TRỎ NHẦM NGƯỜI im lặng. Đã dịch employee_infos.id -> employees.id của ERP, chạy SAU bước đẩy tài khoản, không tra được thì ghi 0 (không giữ id cũ).
2. departments.group_id trỏ bảng `groups` (Khối) — lệnh chưa từng đẩy sang ERP.department_groups. Thêm bước 2a. Lưu ý `groups` là từ khoá MySQL, phải bọc backtick.
3. employee_infos.created_by — mình từng ghi $model->created_by của HRM sang (cột này bên ERP là id người BÊN ERP) -> 125/128 hồ sơ trỏ id 1913 của HRM. Trả về $by + thêm bước vá dữ liệu đã ghi sai.
4. employees.created_by/updated_by bên ERP để trống -> bù $by.
5 commit đã đẩy origin/tpe (đến 5df93f070), đã pull + chạy lại trên /var/www/uat/hrm-api sau mỗi commit.
Kiểm chứng UAT (so THEO TÊN, không chỉ theo id): công ty 1/1, khối 6/6, phòng ban 16/16 (kèm thứ tự + khối + trưởng phòng), bộ phận 66/66 (kèm trưởng bộ phận), hồ sơ 128/128 (kèm ảnh, học vấn, ngày vào, CCCD), tài khoản 127/127 (kèm token_version) — TẤT CẢ KHỚP. Rà lại cột id: không còn cột nào lệch.
Lỗi có sẵn KHÔNG sửa: ERP có bảng working_positions cục bộ RỖNG (0 dòng) — công ty 1 cũng 0/579; ERP lấy chức danh qua connection 'hrm'.
CÒN TỒN: (1) hrm-client trên UAT chưa pull, thiếu 17 commit gồm e554e0e2f (ẩn nút Sửa dự án TKT) -> UAT đang lệch FE/BE; (2) chưa xem được màn /admin/departments bằng mắt vì tài khoản ETEK GREEN chưa có quyền admin bên ERP UAT.
Bước tiếp theo: TPE tải lại màn ERP kiểm tra.
Blocked: (không).

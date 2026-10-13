# Plan — Hợp nhất ERP+HRM: Gộp DB

## Phase 0 — Phân loại 49 bảng trùng (ĐANG LÀM)
- [x] Khảo sát: ERP 1234 / HRM 617 bảng / 49 trùng tên
- [x] So cấu trúc cột 49 bảng (ERP DB vs HRM migration) → appendix-49-tables.md
- [x] Phân loại sơ bộ A/B/C/D + nguyên tắc gộp chuẩn → design.md
- [x] Verify id khớp toàn bộ 49 bảng (D1-D5) — hoàn tất
- [x] Chốt per-bảng: 28 dùng-chung / 23 tách (design.md mục 11)

## Phase 1 — Script gộp
- [ ] Quy ước tên bảng tách (prefix `hrm_`)
- [ ] Script gộp idempotent (tạo schema chung, import bảng ERP, xử lý 49 trùng, union cột nhóm dùng-chung)
- [ ] Chạy STAGING trước, không đụng prod

## Phase 2 — Cutover
- [ ] Đổi DB_DATABASE app ERP → test regression toàn bộ
- [ ] Sửa code HRM cho bảng đã đổi tên
- [ ] Migrate code ERP→HRM dần (dự án riêng, nhiều tháng)

### Checkpoint — 2026-07-27
Vừa hoàn thành: khảo sát + phân loại 49 bảng trùng, design.md + appendix.
Bước tiếp: verify id khớp (cần môi trường nối HRM DB); chốt bảng dùng-chung vs tách.
Blocked: máy hiện không nối được HRM DB (host nội bộ timeout) → verify id phải làm ở nơi có kết nối.

### Checkpoint — 2026-07-27 (lưu tiến độ)
Vừa hoàn thành:
- Chốt chiến lược: GỘP DB TRƯỚC (ERP đổi connection là chạy) → migrate code ERP→HRM dần → tắt app ERP → dọn schema cuối.
- Khảo sát: ERP 1.234 bảng / HRM 617 / **49 trùng tên**.
- **Verify id khớp TOÀN BỘ 49 bảng** (dev_erp_2 ↔ dev_hrm_2, cùng server 127.0.0.1, query chéo được).
- Phân loại cuối (design.md mục 8-11): **~28 bảng gộp chung được / ~23 phải tách-remap**.
  - Dùng chung: danh mục org/địa lý/khách (customers 97% fullname, provinces/wards 100%, parts cùng bộ phận…).
  - TÁCH bắt buộc: nghiệp vụ (quotations id đụng khác hoàn toàn, job_requests, settlement_contracts, print_templates, customer_contacts) + pivot (company_employees, employee_manage_departments…) + framework (jobs/notifications/files).

Đang làm dở: chưa viết code/script gì. Đây là giai đoạn PLANNING.

Bước tiếp theo (chờ user chốt):
1. Quy ước prefix bảng tách: đề xuất `hrm_` (vd `hrm_quotations`).
2. Schema đích: gộp vào schema HRM hay tạo schema mới.
→ Sau khi chốt: viết **script gộp idempotent** (chạy STAGING trước): dồn 1.185 bảng riêng ERP + xử lý 49 trùng theo D1-D5 (union cột nhóm chung + remap id lệch: customers ~670, employee ~30 + đổi tên hrm_* nhóm tách).

Ghi chú môi trường:
- dev_erp_2 + dev_hrm_2 CÙNG server local 127.0.0.1:3306 → verify cross-DB được.
- HRM prod DB (host nội bộ) KHÔNG nối được từ máy này → verify id trên PROD phải chạy lại ở môi trường có kết nối trước khi gộp prod.

Blocked: chờ user chốt 2 quy ước (prefix + schema đích).

Tài liệu: design.md (11 mục), appendix-49-tables.md (số cột), verify-49-idmatch.txt (id khớp).

### Checkpoint — 2026-07-28 (BẮT ĐẦU GỘP STAGING)
Quyết định (tự chốt): prefix bảng tách = `hrm_`; schema đích = `erp_hrm_merged` (mới, local); base = ERP (giữ nguyên tên+cột).
Plan gộp (merge_plan.tsv): 1.216 KEEP_ERP · 581 ADD_HRM (HRM riêng) · 35 TACH_HRM (hrm_*) · 23 SHARE_HRM (hòa HRM vào bảng ERP).
- Phase A XONG: dựng cấu trúc 1.832 bảng trong erp_hrm_merged (CREATE LIKE), hòa 23 bảng thêm 102 cột HRM (union), 0 lỗi.
- Phase B ĐANG CHẠY NỀN (copy data): toàn bộ HRM (ADD/TACH/SHARE) + ERP-rows của 23 bảng hòa. (1.216 bảng thuần-ERP: staging bỏ copy data — prod thật sẽ RENAME-move tức thì.) notifications HRM 711k → mất vài phút.
Verify khớp logic sơ bộ: SHARE companies union=8, TACH hrm_company_employees=1104.
Bước tiếp: chờ Phase B xong → verify tổng (đếm bảng/dòng, kiểm bảng tách + union) → nếu OK, tài liệu hoá script gộp thành bản chạy prod (dùng RENAME-move cho KEEP_ERP).
Blocked: —
Script: $CLAUDE_JOB_DIR/tmp/merge_planA.php, merge_phaseA.php, merge_phaseB.php (+ merge_plan.tsv).

### Checkpoint — 2026-07-28 (GỘP STAGING THÀNH CÔNG)
Phase B XONG: copy 639 bảng HRM, 5.628.312 dòng, 0 lỗi.
VERIFY erp_hrm_merged: 1.832 bảng (35 hrm_* tách). companies 86 cột (ERP76+10 HRM union, 8 dòng), customers 43.520 (union), hrm_quotations 75 (báo giá HRM tách riêng — không lẫn ERP), hrm_roles 44, hrm_company_employees 1.104. quotations(ERP) structure-only (đúng thiết kế staging). Toàn bộ logic gộp ĐÚNG.
Bước tiếp:
1. Đóng gói script gộp thành bản PROD: KEEP_ERP dùng RENAME TABLE-move (tức thì) thay copy; các bước khác giữ. Idempotent.
2. Kiểm phần chưa xử lý: rows đụng-id ở nhóm SHARE dùng-chung id (companies/departments/customers) — hiện chỉ INSERT HRM rows CHƯA có id; cột HRM của rows đụng-id CHƯA được điền (cần UPDATE bổ sung nếu muốn giữ dữ liệu CRM HRM cho KH đã có ở ERP). Cân nhắc.
3. FK: bảng ERP có FK trỏ bảng đổi tên (hrm_*)? — rà FK trước prod.
4. Verify sâu vài bảng SHARE (customers: HRM-only rows có vào không).
Scripts: merge_planA/phaseA/phaseB.php + merge_plan.tsv (job tmp). Schema staging: erp_hrm_merged (local).
Blocked: —

### Checkpoint — 2026-07-28 (ĐÓNG GÓI SCRIPT PROD XONG)
Vừa hoàn thành:
- `merge_prod.php` — script gộp production idempotent (base=ERP, RENAME-move, DRY-RUN, FILL_SHARED_HRM). Nhúng sẵn 23 bảng HÒA + 35 bảng TÁCH. DRY-RUN trên local: 581 move + 35 tách + 23 hòa = 776 lệnh, 0 lỗi.
- `HUONG-DAN-GOP.md` — hướng dẫn: điều kiện (cùng server + backup), dry-run→thật, sau gộp (đổi connection + sửa code HRM bảng hrm_*), FK, rollback.
Deliverable đầy đủ trong .plans/hop-nhat-erp-hrm/: merge_prod.php, HUONG-DAN-GOP.md, xu-ly-bang-trung-PROD.xlsx, verify-58-prod.tsv, design.md, plan.md.
Bước tiếp (khi user sẵn sàng gộp thật):
1. Rà & remap thủ công vài trăm id lệch nhóm dùng-chung (employees ~21%, customers ~các id đụng khác thực thể) trước khi $DRY_RUN=false.
2. Rà FK sau gộp.
3. Cấu hình HRM: migration table→hrm_migrations, queue→hrm_jobs, notification/auth table names.
Blocked: —

---

## PHASE — Sửa code HRM chạy trên DB đã merge (2026-07-29)

**Quyết định user (2026-07-29):**
- Giữ nguyên nhóm `$KEEP_HRM` (quotations, job_requests, working_positions, transport_types, moving_norm_roads, attachment_types, assign_business_tasks, teams, moving_norm_road_types, majors, employee_incomes, areas) → giữ cấu trúc+data HRM, DROP bảng ERP. Chấp nhận vài tính năng ERP dính bảng này lỗi (sửa sau).
- Mục tiêu: CẢ 2 app (ERP + HRM) chạy được trên schema gộp. ERP chỉ đổi DB_DATABASE. HRM phải sửa code trỏ bảng đã TÁCH sang `hrm_*`.

**23 bảng TÁCH (tên cũ → hrm_):** company_employees, company_roles, customer_activity_types, customer_business_fields, customer_contact_has_bank_accounts, customer_has_bank_accounts, customer_has_vehicle_manufacts, delivery_places, employee_has_permissions, employee_has_roles, employee_manage_departments, employees, files, groups, module_mappings, nations, permissions, print_templates, role_has_permissions, roles, scopes, settlement_contract_employees, settlement_contracts.

### Tasks
- [ ] B0. Inventory: quét toàn bộ HRM (Modules/app/config/routes/seeders) mọi tham chiếu 23 bảng (model $table, DB::table, join, pivot belongsToMany, raw SQL, config/permission.php)
- [ ] B1. Sửa `config/permission.php`: roles→hrm_roles, permissions→hrm_permissions, model_has_permissions→hrm_employee_has_permissions, model_has_roles→hrm_employee_has_roles, role_has_permissions→hrm_role_has_permissions
- [ ] B2. Sửa `$table` các model (~24 model) sang hrm_*
- [ ] B3. Sửa pivot trong belongsToMany + DB::table + join + raw SQL trỏ hrm_*
- [ ] B4. Auth: đảm bảo HRM login (JWT) trỏ hrm_employees (Employee/TpEmployee model + guard)
- [ ] B5. php -l toàn bộ file sửa; boot HRM với .env DB=erp_hrm_check → smoke test login + 1 API mỗi module
- [ ] B6. Deploy checklist: worker queue tách (ERP --queue=erp, HRM --queue=hrm,rice_notifications,sync_faces); .env cả 2 app

### Checkpoint — 2026-07-29
Vừa hoàn thành: chốt hướng (giữ KEEP_HRM, sửa HRM sang hrm_*); dispatch agent inventory (B0).
Đang làm dở: chờ inventory 23 bảng → lập danh sách điểm sửa chính xác.
Bước tiếp: B1→B4 sửa code HRM.
Blocked: —

---

## PHASE — CHỐT: build test bằng CÁCH A (lớp VIEW) thay vì sửa code HRM (2026-07-29)

**Bối cảnh:** Inventory cho thấy sửa code HRM sang hrm_* là ~150 điểm/90 file, rủi ro auth/join cao, lại là công tạm (mục 14: hợp nhất thật sau này bỏ hrm_*). → User chốt dùng **Cách A: lớp VIEW**.

**Cách A — lớp view (KHÔNG sửa code HRM):**
- Schema `hrm_view` chứa 639 view 1-1: 23 bảng TÁCH → trỏ `<merged>.hrm_*`; còn lại → passthrough.
- HRM chỉ đổi `DB_DATABASE=hrm_view`. ERP giữ `DB_DATABASE=<merged>`.

### Tasks (Cách A)
- [x] A1. Verify 639 bảng HRM đều có target trong erp_hrm_check (639/639 OK)
- [x] A2. Dựng schema hrm_view + 639 view (mapping tách→hrm_*, còn lại passthrough)
- [x] A3. Smoke-test ĐỌC: count qua view = bảng đích (employees 1085, roles 44, permissions 588, customers 43520, files 25, quotations 75) — khớp 100%
- [x] A4. Smoke-test GHI: INSERT/UPDATE/DELETE + LAST_INSERT_ID qua view `nations` → xuống thẳng hrm_nations OK
- [x] A5. Smoke-test JOIN 6 view (auth+phân quyền: employees→employee_infos→employee_has_roles→roles→role_has_permissions→permissions) → "DNS Admin/Super admin/564 quyền" OK
- [x] A6. Script tái sử dụng `build_hrm_views.sh` + snapshot `hrm-view-tables.txt` (639) + `HUONG-DAN-VIEW.md`
- [ ] A7. DEPLOY server test: đưa 2 DB cùng server → merge → build view → sửa .env 2 app → worker tách queue → smoke-test app thật (login + 1 API/module)

### Checkpoint — 2026-07-29 (Cách A xong ở local)
Vừa hoàn thành: Cách A (lớp view) dựng + smoke-test đầy đủ ở local erp_hrm_check (đọc/ghi/auto-inc/JOIN chuỗi đều OK); deliverable build_hrm_views.sh + hrm-view-tables.txt + HUONG-DAN-VIEW.md.
Đang làm dở: — (chờ deploy lên server test A7).
Bước tiếp: A7 — dựng trên server test rồi boot 2 app thật; HOẶC (tuỳ user) boot HRM local trỏ hrm_view để test app ngay.
Blocked: — (cần server test có cả 2 DB cùng chỗ, hoặc quyết boot HRM local).

---

## PHASE — CHỐT LẠI: Sửa CODE HRM sang hrm_* (CÁCH B) — user đổi ý bỏ view (2026-07-29)

User thấy lớp view "lằng nhằng" → chốt **sửa code HRM đổi tên bảng sang hrm_** (bỏ Cách A view, đã DROP schema hrm_view). Làm trên nhánh HRM `gop_db`.

### Cách làm
- Inventory: 156 file có tham chiếu SQL tới 23 bảng tách + config/permission.php + 6 model bind ngầm.
- Chia lô: tôi làm app/(21)+config; 6 subagent theo module (Assign/Training/Human/Timesheet/Decision/Misc) Pass 1 (đổi tên bảng ở table/join/from/$table/pivot/exists/unique).
- Pass 2 (3 subagent): sửa TIỀN TỐ CỘT `bảng.cột` trên query Eloquent-model (FROM lấy từ $table model đã hrm_, cột viết tay chưa đổi).
- Pass 3 (tôi): thêm $table cho 6 model bind ngầm (Scope→hrm_scopes, Group×2→hrm_groups, ModuleMapping→hrm_module_mappings, SettlementContract→hrm_settlement_contracts, CompanyEmployee→hrm_company_employees) + sửa prefix theo; vá static join `::join('employees')` (grep Pass1 chỉ bắt ->join).

### QUY TẮC then chốt (đã áp)
- **KHÔNG đổi** mọi query `->connection('mysql2')` và model `Tp*` có `$connection='mysql2'` (đọc bảng ERP gốc, giữ tên cũ). **Đã hoàn tác 5 model Tp app/Models tôi lỡ đổi** (TpEmployee2/TpEmployeeData/TpCustomerBankAccount/TpCustomerContactBankAccount/TpDeliveryPlace).
- **Ngoại lệ `App\Models\TpEmployee`**: dù tên Tp nhưng `$connection` mysql2 bị COMMENT (dùng conn HRM) + là model auth JWT (`config/auth.php` provider) → giữ `hrm_employees` (bắt buộc để HRM login đúng).
- Giữ nguyên: field validation (`.*.`, message key `'employees.required'`), eager-load relation (`'employees.employee.info'`), comment.

### Kết quả & verify
- **167 file thay đổi, php -l SẠCH toàn bộ** (731+/721-).
- Rà tổng: Pattern A (tên bảng) + Pattern B (tiền tố cột) + raw SQL → residual đều là giữ đúng (Tp/mysql2/validation/relation); KHÔNG double-prefix; migration ngoài phạm vi.
- Smoke DB (erp_hrm_check): query auth+phân quyền với tên hrm_ mới chạy đúng (Super admin 564 quyền); 23/23 bảng hrm_* tồn tại.
- config/permission.php: roles→hrm_roles, permissions→hrm_permissions, model_has_permissions→hrm_employee_has_permissions, model_has_roles→hrm_employee_has_roles, role_has_permissions→hrm_role_has_permissions.
- **CHƯA commit** (nhánh gop_db).

### Checkpoint — 2026-07-29 (Cách B xong)
Vừa hoàn thành: đổi code HRM sang hrm_* cho 23 bảng tách (167 file, php -l sạch, rà tổng sạch), verify DB. Bỏ Cách A view.
Bước tiếp: DEPLOY test — HRM .env DB_DATABASE→merged schema; connection mysql2→merged schema (bảng ERP base); worker `--queue=hrm,...`; boot HRM smoke-test login + 1 API/module. (ERP chỉ đổi DB_DATABASE→merged.)
Blocked: cần server test có merged schema (hoặc boot HRM local trỏ erp_hrm_check).

### Checkpoint — 2026-07-29 (BOOT HRM local trên erp_hrm_check — THÀNH CÔNG)
Vừa hoàn thành: boot HRM local trỏ erp_hrm_check (cả DB_DATABASE + DB_DATABASE_SECOND). Verify: full framework + mọi module nạp OK; model đọc bảng hrm_* đúng count; spatie Role->permissions=86; mysql2 đọc ERP base (employees 1085/customers 43520); HTTP GET / =200; POST /api/v1/users/auth/login (route thật) = 422 "sai tài khoản" (query hrm_employees OK, log sạch không lỗi SQL). → HRM CHẠY ĐƯỢC trên DB merge.
Trạng thái .env HRM: đang trỏ erp_hrm_check (theo yêu cầu test browser). Backup gốc: hrm-api/.env.bak_gopdb. Khôi phục: cp .env.bak_gopdb .env && php artisan config:clear.
Bước tiếp: user test browser (login tài khoản thật + duyệt các module). Nếu OK → deploy server test tương tự (xem HUONG-DAN-VIEW.md phần .env/worker nhưng KHÔNG cần view — chỉ đổi DB_DATABASE 2 app + worker tách queue).
Pre-existing (không liên quan rename): route Modules/Decision/Routes/api.php `use ...DecisionController` thiếu \V1 → route:list lỗi (không ảnh hưởng boot/login).
Blocked: —

### Checkpoint — 2026-07-29 (fix login logout: notifications TÁCH)
Vừa hoàn thành: fix HRM login bị đá ra — nguyên nhân bảng notifications cấu trúc ERP≠HRM. Chốt TÁCH: notifications(ERP giữ)+hrm_notifications(HRM). HRM thêm model DatabaseNotification + override notifications() 2 model EmployeeInfo + DeleteOldNotification→hrm_notifications. merge_prod.php: notifications vào $TACH+truncate. DB check: notifications=ERP 78719 dòng, hrm_notifications=HRM rỗng. php -l sạch. Verify tinker OK.
Bước tiếp: user login lại FE (nếu server không tự nạp model mới → restart php artisan serve). Test tiếp các module; gặp Unknown column/Base table khác → báo để xử lý tương tự (kiểu trùng-tên-khác-cấu-trúc).
Blocked: —

### Checkpoint — 2026-09-25 (fix 500 khi sửa hợp đồng hãng — company_id ambiguous)
Triệu chứng: mở `admin/sale/firm-contracts/{id}/edit` (vd 28302) → 500 Server Error.
Root cause (đã repro tinker read-only trên hrm_erp_gop): `FirmContractService::getDataForEdit()`
eager-load `signer.roles` với `->where('company_id', auth()->user()->info->company_id)` KHÔNG
qualify tên bảng. Sau gộp DB, `employee_has_roles` có thêm cột `company_id` trùng với
`roles.company_id` → SQL "Column 'company_id' in where clause is ambiguous" → 500. Chỉ nổ khi
HĐ CÓ signer (đa số HĐ) → lỗi hệ thống mọi màn sửa HĐ hãng.
Fix (BE, 1 chỗ): bỏ điều kiện `->where('company_id', ...)` ở relation `signer.roles` trong
`getDataForEdit()` (dòng ~1331), khớp đúng bản đã sửa sẵn ở `prepareDataForCreate()` (dòng ~1126,
bản cũ đã comment). php -l sạch; repro `getDataForEdit(28302)` + full `edit()` flow = OK.
- [x] Fix `FirmContractService::getDataForEdit` signer.roles ambiguous company_id
CHƯA commit (nhánh gop_db). KHÔNG ghi DB server (chỉ SELECT khi repro).
Bước tiếp: user reload trình duyệt màn sửa HĐ để xác nhận; cân nhắc gom commit chung các fix gop_db.

### Checkpoint — 2026-09-25 (fix 500 màn Thẻ kho — company_id ambiguous)
Triệu chứng: mở `admin/warehouse/warehouse_reports/stockCard` → 500.
Root cause (repro tinker read-only): `AccountingWarehouse::getByWarehouseCompany` (dòng ~302/307)
select `company_id as id` + `groupBy('company_id')` KHÔNG qualify, join `companies`. Sau gộp DB,
`companies` có thêm cột `company_id` → "Column 'company_id' is ambiguous" → 500.
Fix (BE): qualify `accounting_warehouses.company_id` ở select raw + groupBy. php -l sạch; repro
stockCard render OK.
- [x] Fix AccountingWarehouse::getByWarehouseCompany qualify company_id
Cùng họ lỗi gộp-thêm-cột-trùng-tên (xem signer.roles, hasAnyPermission guard).

### Checkpoint — 2026-09-25 (drop 3 cột mồ côi company_id/department_id/part_id trên bảng companies)
Bối cảnh: user hỏi "cột company_id trong bảng companies có cần không" → xác định 3 cột
`company_id`, `department_id`, `part_id` là RÁC do gộp DB mang theo. Bảng `companies` gốc ERP
KHÔNG có; migration tạo companies bên HRM (2021_11_22_143552) cũng KHÔNG tạo. Xác minh:
NULL 100% (server hrm_erp_gop 9 dòng, local erp_new 8 dòng đều NULL), không FK, không index,
KHÔNG code nào (ERP `app/`+`resources/`+`database/`, HRM `app/`+`Modules/`) đọc/ghi
`companies.{company_id,department_id,part_id}` (mọi match đều là bảng khác/FK trỏ companies.id).
Bonus: bỏ cột này gỡ luôn bẫy hook auto-fill `company_id` của HRM `BaseModel` với model Company.
Migration (hrm-api, HRM sở hữu schema companies):
`hrm-api/database/migrations/2026_09_25_000001_drop_orphan_org_columns_from_companies_table.php`
— up() drop 3 cột (guard hasColumn); down() re-add unsignedBigInteger nullable.
- [x] Tạo migration drop 3 cột mồ côi
- [x] Chạy migrate trên LOCAL erp_new → 3 cột biến mất, companies còn 8 dòng (data nguyên vẹn)
- [ ] Chạy trên SERVER hrm_erp_gop: CHƯA — server DB write cần user xác nhận thời điểm (deploy pipeline sẽ tự migrate)
CHƯA commit (nhánh gop_db hrm-api).

### Checkpoint — 2026-09-25 (fix popup "Người ký hợp đồng" rỗng ở màn tạo/sửa HĐ hãng)
Triệu chứng: mở popup chọn Người ký hợp đồng (nút "Ký duyệt") ở màn tạo/sửa HĐ hãng → bảng
NV rỗng hoàn toàn (AJAX 500).
Root cause (repro read-only trên hrm_erp_gop): popup dùng `partials/modals/searchEmployee_v2`
(type='Ký hợp đồng') gọi `SearchController::searchEmployee`. Query chính OK (permission scope
'Duyệt hợp đồng' web guard = 43 role links). Lỗi ở eager-load `roles` (dòng ~166): khi
`role_by_company_current == "true"` (create/edit HĐ hãng đều set `let role_by_company_current=true`)
thì `->where('company_id', ...)` KHÔNG qualify. Sau gộp DB pivot `employee_has_roles` cũng có
`company_id` → "Column 'company_id' is ambiguous" → Datatables 500 → popup rỗng.
Fix (BE, 1 chỗ): qualify `->where('roles.company_id', ...)`. php -l sạch; repro TEST A (chưa
qualify) = lỗi ambiguous, TEST B (qualify roles.company_id) = OK trả rows.
- [x] Fix SearchController::searchEmployee eager-load roles qualify company_id
Ảnh hưởng chung: searchEmployee dùng cho nhiều popup (Duyệt báo giá, Duyệt HĐ, Duyệt YCĐH...) →
fix 1 chỗ có lợi cho mọi popup khi role_by_company_current=true. CHƯA commit (nhánh gop_db ERP).

### Checkpoint — 2026-09-25 (fix in HĐ trắng màn: signer_role_id chưa offset khi gộp DB)
Triệu chứng: mở `admin/customer-care/warranty_repair_contracts/7937/print` → màn trắng,
`ErrorException: Trying to get property 'name' of non-object` tại
`app/Services/PrintTemplate/WarrantyRepairServiceContractPrint.php:50`
(`Role::query()->find($object->signer_role_id)->name` — signer_role_id=60, Role::find(60)=NULL).
Root cause (điều tra read-only trên hrm_erp_gop): khi gộp DB, role ERP đã offset +100000 và
chuyển guard 'web' (dải 100001..100124), NHƯNG ReconcileAuth BỎ SÓT không offset các cột
`signer_role_id` ở 9 bảng HĐ → chúng giữ id role ERP CŨ (1..999). id cũ mất role -> in trắng
màn; id cũ trùng role HRM (guard 'api' id thấp) -> in NHẦM tên chức vụ (âm thầm).
Phạm vi: 33.821 dòng id cũ trên firm_contracts(26441), wr_service_contracts(3574),
inland_buy_contract_news(1948), inland_buy_contracts(852), buy_contract2(923),
buy_service_contracts(81), inland_buy_contract_annex2(2). Dry-run: 33.821/33.821 đều có role
đích +100000 guard web, skip=0.
Fix DATA (đã CHỌN A, đã CHẠY THẬT trên server hrm_erp_gop): `UpdateDB::fixSignerRoleIdOffsetGopDb_20260925`
— per-table UPDATE JOIN roles (r.id = signer_role_id+100000 AND guard='web') SET +100000
WHERE signer_role_id BETWEEN 1 AND 999; transaction, dry-run mặc định, verify trong TX.
- [x] Điều tra root cause + xác định phạm vi 9 bảng (read-only)
- [x] Viết method fixSignerRoleIdOffsetGopDb_20260925 (dry-run + verify), php -l sạch
- [x] Dry-run trên hrm_erp_gop: 33.821 se_doi, skip=0, con_low=0 [OK]
- [x] Chạy thật (false) COMMIT trên hrm_erp_gop: affected khớp, con_low=0 mọi bảng
- [x] Verify sau ghi: HD 7937 signer_role_id=100060 "Trưởng phòng CSKH"(web); 9 bảng orphan=0
CHƯA commit code (nhánh gop_db ERP) — user tự commit/push. Method để lại trong UpdateDB.php.
Lưu ý: chỉ vá signer_role_id; các FK roles.id khác mà ReconcileAuth bỏ sót (nếu có) chưa rà.

### Checkpoint — 2026-09-25 (fix TIẾP popup Người ký hợp đồng: "Chức vụ" rỗng + JS crash roles[0].id)
Nối tiếp checkpoint "fix popup rỗng" ở trên: bản qualify `->where('roles.company_id', ...)` đã
chữa lỗi 500 (ambiguous) nhưng LỌC SAI CỘT → popup load được NV nhưng cột "Chức vụ" rỗng hoàn
toàn; chọn NV làm người ký → JS crash `formJs.blade.php:202` `$scope.form.signer.roles[0].id`
(roles[] rỗng → roles[0] undefined).
Root cause (repro read-only hrm_erp_gop): sau gộp DB, role ERP (guard 'web') đều có
`roles.company_id = NULL` (76/76). Phạm vi công ty của việc gán role đã chuyển sang PIVOT
`employee_has_roles.company_id` (điền đúng: cty1=927, cty4=201, cty3=63, ...). Lọc theo
`roles.company_id = <cty hiện tại>` loại sạch role → roles rỗng. Đây là cùng ngữ nghĩa mà code
ERP khác đã dùng: `Employee.php:758-760` và `:1213` đều `where('employee_has_roles.company_id')`.
Fix (BE, 1 chỗ): đổi eager-load roles từ `roles.company_id` → `employee_has_roles.company_id`
(SearchController::searchEmployee ~dòng 169). Verify tinker: emp có role trả về đủ (emp#223: 2
role "111","Nhân sự hành chính"), roles[0].id có giá trị.
Fix (FE, phòng thủ): `selectValidSigner` null-safe — NV có quyền ký nhưng không có role ở cty
hiện tại → roles rỗng thì set signer_role_id=null thay vì crash (formJs.blade.php:200-207).
- [x] Điều tra: roles.company_id=NULL toàn bộ role web sau gộp; pivot company_id điền đúng
- [x] Fix BE: eager-load roles lọc theo employee_has_roles.company_id (pivot), php -l sạch
- [x] Verify read-only: eager-load trả roles non-empty theo cty
- [x] Fix FE: selectValidSigner null-safe roles[0]
CHƯA commit (nhánh gop_db ERP) — user tự commit/push.

### Checkpoint — 2026-09-25 (DROP 3 cột org mồ côi trên bảng `roles`: company_id, department_id, part_id)
Nối tiếp Ca 3 (drop 3 cột org trên `companies`). User đặt vấn đề: 3 cột `company_id`,
`department_id`, `part_id` trên bảng `roles` "hình như không cần thiết... không dùng ở cả
erp,hrm". Điều tra kỹ (read-only trên hrm_erp_gop + grep code + 2 agent Explore hrm-api/hrm-client):
- **Không code nào ĐỌC 3 cột như thuộc tính của role.** Phạm vi công ty của role đi qua PIVOT:
  `employee_has_roles.company_id`, `role_has_permissions.company_id` (ERP) và `company_roles` (HRM).
  Cột scalar trên chính bảng `roles` là dư thừa. (Chính đây là gốc của Ca 4 signer popup:
  `roles.company_id` = NULL nên phải lọc qua pivot.)
- **Dữ liệu:** `part_id` NULL 100% mọi guard (mồ côi thật). `company_id`(17)/`department_id`(13)
  chỉ còn dead-data trên role guard 'api' (HRM), không ai đọc. KHÔNG FK, KHÔNG index trên DB gộp.
- **Nguồn gốc (đã truy):** `roles.company_id` do ERP thêm 2021 (`2021_07_13_..._add_field_company_id_
  to_roles_and_permissions_table`, từng kèm FK → nhưng FK không còn trên DB gộp) — tức KHÔNG phải
  rác gộp DB như user tưởng ban đầu, nhưng vẫn vô dụng sau khi scope chuyển sang pivot.
  `department_id`+`part_id` do 2 migration blanket HRM 2024 quét mọi bảng có `created_by`
  (`2024_10_29_162738_add_part_id_to_tables`, `2024_11_05_115711_add_company_id_and_department_id_
  to_table`).
- **permissions table:** đã kiểm read-only — bảng `permissions` KHÔNG có bất kỳ cột nào trong 3
  cột trên DB gộp → không cần đụng.
User chốt Cách B: bỏ cả 3 cột bằng 1 migration ở hrm-api (khớp tiền lệ Ca 3 companies).
- [x] Điều tra read-only DB (no FK/index; part_id all NULL; company_id/department_id dead-data api-only)
- [x] Grep code ERP: chỉ dùng pivot, không đọc roles.{3 cột}
- [x] 2 agent Explore xác nhận hrm-api + hrm-client KHÔNG đọc 3 cột
- [x] Kiểm permissions table: không có 3 cột → scope hẹp về mình bảng roles
- [x] Tạo migration `HRM/hrm-api/database/migrations/2026_09_25_000002_drop_orphan_org_columns_from_roles_table.php`
      (up: dropForeignKeysIfExist qua information_schema rồi dropColumn có hasColumn guard; down: re-add nullable)
- [x] Dọn dead-code `HRM/hrm-api/Modules/Timesheet/Services/RoleService.php:112`
      (`$attributes['company_id'] = ...` — bị $fillable của Role chặn nên vô hiệu; xóa)
CHƯA chạy migration trên server (ERP .env đang trỏ hrm_erp_gop — ghi DB server cần user xác nhận
thời điểm; pipeline deploy sẽ tự migrate). CHƯA commit — user tự commit/push phía HRM.

### Checkpoint — 2026-09-25 (qualify company_id ở 17 file eager-load roles còn chưa qualify)
Kiểm tra sau khi drop 3 cột roles: KHÔNG còn `roles.company_id` qualified (chỉ comment) → không
lỗi Unknown column. NHƯNG phát hiện 17 file còn `->where('company_id', auth()->user()->info->company_id)`
CHƯA qualify trong eager-load `roles` (signer.roles/approver.roles qua pivot employee_has_roles).
Trước drop = ambiguous (bom nổ chậm, cùng họ signer/stockCard); sau drop = tự trỏ pivot (đúng) nhưng
mong manh nếu rollback. User chốt: qualify thẳng `employee_has_roles.company_id` (bền vững, khớp
ContractAccounting.php:352 đã đúng sẵn; giữ nguyên ngữ nghĩa lọc theo cty user hiện tại).
File: Contract.php, FirmContractController, FirmContractAdditionAnnexesController,
ZTFirmContractAdditionAnnexesController, ZtecDesignRequirementController(x2), InlandOrderRequestsController(x2),
ProjectContract, ServiceContract, InlandBuyContract, BuyContract2, InlandBuyContractNew,
InlandBuyContractAnnex, InlandBuyContractAnnex2, ImportRecord, FirmContractAnnexService,
ZTFirmContractAnnexService, ZTFirmContractService.
- [x] Qualify tất cả về employee_has_roles.company_id trong closure roles (28 chỗ / 17 file)
- [x] php -l sạch toàn bộ file sửa; grep xác nhận không còn company_id chưa qualify trong closure roles
CHƯA commit (nhánh gop_db ERP) — chờ user.

### Checkpoint — 2026-09-25 (in HĐ hãng: địa chỉ Bên B mất số nhà — cột scalar `hamlet` che relation)
Repro: /admin/sale/firm-contracts/28302/print?print_group=1 → Bên B (Tân Phát, company_id=1) hiện
"Địa chỉ: , Phường Thanh Liệt, Thành phố Hà Nội, Việt Nam" (dấu phẩy đầu + mất số nhà).
Root cause: accessor `Company::getAddressAttribute` (app/Model/Common/Company.php:521) ghép
apartment_number + hamlet->name + ward + province. Số nhà "Số 189 Phan Trọng Tuệ" nằm ở
hamlets.id=1433 (hệ 3 cấp cũ). Sau gộp DB, companies bị thêm CỘT scalar `hamlet` varchar(255)=NULL
(9/9 công ty NULL — mồ côi) → cột CHE relation hamlet() → `$this->hamlet` trả NULL thay vì bản ghi
hamlets → mất segment số nhà; apartment_number cũng NULL → chuỗi bắt đầu bằng ", ". Cùng họ Ca 3
(companies bị thêm cột mồ côi sau gộp). Bằng chứng: $co->hamlet=NULL nhưng
$co->hamlet()->first()->name='Số 189 Phan Trọng Tuệ'. Phạm vi: 4/9 công ty (hamlet_id set +
apartment_number NULL) mất số nhà; vài công ty khác dư dấu phẩy. KHÔNG cần sửa dữ liệu.
User chốt Hướng 1 (code-only, deploy được ngay).
- [x] Sửa `getAddressAttribute`: lấy hamlet qua relation `$this->hamlet()->first()` (bỏ qua cột che),
      array_filter bỏ phần rỗng → không dấu phẩy thừa
- [x] Sửa `getNameHamletAttribute` (line ~563) tương tự (cùng bug shadow)
- [x] php -l sạch; verify tinker read-only: company 1 = "Số 189 Phan Trọng Tuệ, Phường Thanh Liệt,
      Thành phố Hà Nội, Việt Nam"; company 3,4 cũng đủ số nhà, không dấu phẩy thừa
Đã commit+push Hướng 1: ERP gop_db `0b74aafdda`.

### Checkpoint — 2026-09-25 (Hướng 2: drop cột mồ côi `companies.hamlet` — dọn tận gốc)
Nguồn cột: migration HRM `2023_12_05_134708_add_hamlet_to_companies_table` (`$table->string('hamlet')->nullable()`).
ERP gốc chỉ có `hamlet_id` (int). Cột string mồ côi NULL 100% (local erp_new 8/8), không code nào đọc/ghi
(CompanySyncErp dùng hamlet_id; không service/controller populate). Drop = xoá tận gốc lỗi shadow relation.
Tinh chỉnh so với ghi chú cũ "mồ côi như Ca 3": cột này CÓ khai trong `$fillable` của
`Modules/Human/Entities/Company.php` (dòng cũ 334) — đã gỡ luôn.
- [x] Tạo migration hrm-api `2026_09_25_000003_drop_orphan_hamlet_column_from_companies_table.php`
      (up: hasColumn guard → dropColumn; down: re-add nullable string) theo tiền lệ Ca 3
- [x] Gỡ `'hamlet'` khỏi `$fillable` `Modules/Human/Entities/Company.php`
- [x] Chạy migrate LOCAL erp_new: has_hamlet=false, hamlet_id còn nguyên; rollback re-add OK; re-migrate OK
- [ ] CHƯA chạy trên server hrm_erp_gop (chỉ đọc DB server, ghi qua pipeline deploy / user go-ahead)
- [ ] Git HRM do user xử lý — chờ user xác nhận commit 2 file (migration + Company.php)

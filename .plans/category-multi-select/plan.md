# Plan: Category Multi-Select — Nhóm giải pháp & Ứng dụng

> 📄 **Spec chi tiết:** [`docs/superpowers/specs/2026-04-10-category-multi-select-design.md`](../../docs/superpowers/specs/2026-04-10-category-multi-select-design.md)

## Trạng thái
- Bắt đầu: 2026-04-10
- Hoàn thành: 2026-04-10
- Tiến độ: 56/56 task ✅
- Owner: @manhcuong
- **Note 2026-04-10:** mở rộng scope sau khi phát hiện 14 file FE downstream đang dùng pattern `industry.scope_id` / `application.industry_id` cho cascade. Thêm Phase 8 audit + fix.
- **Hot-fix 2026-04-10 (sau khi user chạy migration):** API `GET /assign/scopes` lỗi `industries.scope_id` không tồn tại → phát hiện loạt downstream còn tham chiếu cột đã drop (giả định cũ trong design "downstream không bị ảnh hưởng" là sai). Thêm Phase 10 — đã fix 7 file (BE 5 + FE 2). User đã backup DB, chạy migration thành công, cập nhật file Excel mẫu, smoke test xong các form downstream.

## Phase 0: Verify & Setup

### Tiền điều kiện
- [x] Task 1: Verify component multi-select — kết luận: dùng `<base-select2 :settings="{ multiple: true, allowClear: true }" />` (pattern đã có ở `ProjectPhaseForm.vue`)
- [x] Task 2: Backup DB local trước khi chạy migration

## Phase 1: DB Migration

### BE — Migration
- [x] Task 3: Tạo migration `2026_04_10_000001_convert_industries_applications_to_multi_select.php` ở `hrm-api/database/migrations/`
- [x] Task 4: Viết `up()` — tạo 4 pivot table + INSERT backfill có INNER JOIN cha + drop 4 cột FK cũ
- [x] Task 5: Viết `down()` — thêm lại cột + UPDATE backfill từ pivot dòng đầu + drop pivot
- [x] Task 6: Chạy `php artisan migrate` trên DB local có data, verify số dòng pivot khớp

## Phase 2: BE Nhóm giải pháp (Industries)

### BE — Model
- [x] Task 7: Sửa `Industries.php` — bỏ `scope_id` khỏi `$fillable`, bỏ relation `scope()`, thêm `scopes()` belongsToMany, sửa `applications()` qua pivot mới
- [x] Task 8: Sửa `isCanUnlockUpdate()` STRICT, `isCanLockUpdate()`, `isCodeEditable()`, `isCanDelete()` dùng relation mới

### BE — Request
- [x] Task 9: Sửa `IndustriesRequest` — `scope_ids` array required min:1 + each integer exists scopes,id

### BE — Service
- [x] Task 10: Sửa `IndustriesService::index()` + `getAll()` + `validateImportData()` + `importIndustries()` — filter `scope_id` qua `whereHas('scopes')`, đếm applications qua pivot `application_industries`
- [x] Task 11: Sửa `IndustriesService::updateOrCreate()` + `update()` — sync `scopes` — sau create/update gọi `$industry->scopes()->sync($request->scope_ids)`

### BE — Resource
- [x] Task 12: Sửa `IndustriesResource` (list) — trả `scopes[]`, `scope_names`, giữ các field cũ
- [x] Task 13: Sửa `DetailIndustriesResource` (show) — trả `scopes[]`
- [x] Task 14: Sửa endpoint master select `getAll` — eager load `scopes:id,name` (FE Vuex sẽ map sang `scope_ids` ở Task 35) + `show()` controller eager load `scopes` — trả thêm `scope_ids[]` cho cascade FE

## Phase 3: BE Ứng dụng (Applications)

### BE — Model
- [x] Task 15: Sửa `Applications.php` — bỏ 3 cột FK khỏi `$fillable`, bỏ 3 relation belongsTo, thêm 3 belongsToMany (`scopes`, `industries`, `customerScopes`)
- [x] Task 16: Sửa `isCanUnlockUpdate()` STRICT cho cả 2 set parent

### BE — Request
- [x] Task 17: Sửa `ApplicationsRequest` — 3 trường `*_ids` array required min:1 + each integer exists, thêm `withValidator()` validate cascade industry∈scope

### BE — Service
- [x] Task 18: Sửa `ApplicationService::index()` — 3 filter qua `whereHas`
- [x] Task 19: Sửa `ApplicationService::store()` + `update()` — bỏ set 3 cột FK, gọi 3 lệnh `sync()` sau create/update
- [x] Task 20: Bỏ block validate cascade cũ — đã thay bằng cascade check qua scopes pivot
- [x] Task 21: Sửa `ApplicationService::import()` — parser nhận array codes thay vì single, validate cascade qua từng row, sync pivot

### BE — Resource
- [x] Task 22: Sửa `ApplicationsResource` (list) — trả 3 array (`scopes`, `industries`, `customer_scopes`) + 3 trường `*_names`
- [x] Task 23: Sửa `ApplicationsDetailResource` — trả 3 array + show() controller eager load 3 relation

## Phase 4: BE — Count queries downstream

### BE — Service
- [x] Task 24: Sửa `ScopeService` — 4 chỗ count, đổi sang đếm `count(distinct ...)` qua pivot `industry_scopes` / `application_scopes`
- [x] Task 25: Sửa `CustomerScopeService` — 1 chỗ count đổi sang pivot `application_customer_scopes`

## Phase 5: FE Nhóm giải pháp

### FE — Modal
- [x] Task 26: Sửa `industry-modal.vue` — `data.scope_ids` array, V2BaseSelectInModal multi (extraSettings.multiple), submit payload, loadIndustryData map từ scopes/scope_ids

### FE — List page
- [x] Task 27: Sửa `pages/assign/solution-groups/index.vue` — bỏ sort cột Nhóm ngành (đổi key sang `scope_names`), import handler đơn giản hoá (FE chỉ gửi raw scopeCode, BE parse)

## Phase 6: FE Ứng dụng

### FE — Modal
- [x] Task 28: Sửa `application-modal.vue` — 3 binding array, 3 select multi (extraSettings.multiple)
- [x] Task 29: Cascade union `filteredIndustries` (computed) + watch `data.scope_ids` auto-cleanup `industry_ids` + toast cảnh báo
- [x] Task 30: loadApplicationData map từ scopes/industries/customer_scopes về 3 array

### FE — List page
- [x] Task 31: Sửa `pages/assign/application/index.vue` — 3 cột đổi sang `*_names`, cascade `filteredIndustries` filter dropdown qua `industry.scope_ids`

## Phase 7: Import Excel

### FE — Import
- [x] Task 32: Cập nhật label/placeholder cột import (Nhóm giải pháp + Ứng dụng) — thêm note "ngăn nhau bằng dấu phẩy"
- [x] Task 33: Sửa `importValidationRules` (Application page) — parse multi codes, kiểm tra cascade industry∈scope; `handleValidateImportData` + `handleImportApplications` đơn giản hoá (FE gửi raw, BE parse)
- [x] Task 34: Cập nhật file Excel mẫu `Mau_import_NhomGiaiPhap.xlsx` và `Mau_Import_UngDung_FN.xlsx` ở `hrm-client/static/` — thêm dòng hướng dẫn "ngăn dấu phẩy" và ví dụ multi-code

## Phase 8: Downstream FE consumers (Vuex + cascade forms)

### FE — Vuex store
- [x] Task 35: Sửa `store/optionsSelect.js` `fetchIndustries` — map `scope_ids` (array) với fallback từ `scopes` relationship
- [x] Task 36: Sửa `store/optionsSelect.js` `fetchApplications` — map 3 array với fallback từ relationship

### FE — Audit & fix cascade consumers
- [x] Task 37: `ProjectPhaseForm.vue` — cascade `industries`/`applications` đổi sang array pattern
- [x] Task 38: `V2BaseFieldCategoryApplicationFilter.vue` — cascade `industriesOptions`/`applicationsOptions` đổi sang array
- [x] Task 39: `RequestSolutionForm.vue` — **NO-OP** (chỉ lưu form data riêng, không cascade từ master)
- [x] Task 40: `FormTab.vue` — **NO-OP** (không có pattern cascade)
- [x] Task 41: `ProjectInfoSection.vue` — 3 cascade computed (industries/applications by industry/applications by customer scope) đổi sang array
- [x] Task 42: `MeetingForm.vue` — **NO-OP** (line 413 đọc `project.scope_id` từ meeting_project entity riêng)
- [x] Task 43: `MeetingProject.vue` — `filteredIndustries` + `filteredApplications` đổi sang array
- [x] Task 44: `QuestionForm.vue` — `industries` + `applications` cascade đổi sang array
- [x] Task 45: `AddQuestionQuickModal.vue` — `industries` + `applications` cascade đổi sang array
- [x] Task 46: `ProspectiveProjectsFilter.vue` — `filteredIndustries` + `filteredApplications` đổi sang array
- [x] Task 47: `solutions/index.vue` — `filteredIndustries` + `filteredApplications` đổi sang array
- [x] Task 48: `questions/index.vue` — **NO-OP** (không có pattern cascade)
- [x] Bonus: `resources/views/exports/applications.blade.php` — đổi `industry_name`/`scope_name`/`customer_scope_name` → `*_names`

## Phase 9: Test & Wrap-up

### Test
- [x] Task 49: Chạy đủ test case theo checklist trong spec §12 (BE + FE) + smoke test các form ProjectPhase / Meeting / RequestSolution / Question / etc., fix bug phát sinh, cập nhật checkpoint cuối

## Phase 10: Hot-fix downstream sau migration (2026-04-10)

### BE — Relations còn dùng FK đơn đã drop
- [x] Task 50: `Modules/Assign/Entities/Scope/Scope.php` — `industries()`/`applications()` đổi `hasMany` → `belongsToMany` qua `industry_scopes`/`application_scopes`; `isCanLockUpdate` qualify `industries.status` + đổi sang `doesntExist()`
- [x] Task 51: `Modules/Assign/Entities/CustomerScope/CustomerScope.php` — `applications()` đổi `hasMany` → `belongsToMany` qua `application_customer_scopes`; `isCanLockUpdate` qualify `applications.status`

### BE — Service đọc cột FK đã drop
- [x] Task 52: `Services/ProspectiveProjectService::autoFillFromApplication` — eager load `scopes:id`/`industries:id`/`customerScopes:id`; chỉ fill khi PP chưa có giá trị; fallback lấy phần tử đầu tiên trong pivot
- [x] Task 53: `Services/Report/SolutionsWorkSummaryByDepartmentReportService` — (a) `with('industry')` của Application không tồn tại → đổi sang `with(['industries:id','scopes:id'])`; (b) `resolveSolutionCatalogIds` fallback đọc qua pivot, hỗ trợ cả 2 trường hợp đã/chưa eager load

### BE — Resource trả field cũ
- [x] Task 54: `Transformers/SurveyQuestionsResource` — đổi `industry.scope_id` → `scope_ids[]`, `application.scope_id`/`industry_id` → `scope_ids[]`/`industry_ids[]`, lấy từ relation pivot (an toàn cả khi chưa eager load)

### FE — Vuex consumer còn map field cũ
- [x] Task 55: `store/optionsSelect.js` `fetchIndustries`/`fetchApplications` — đổi map `scope_id`/`industry_id`/`customer_scope_id` (singular) sang mảng `*_ids` từ relations BE eager-loaded
- [x] Task 56: `pages/assign/form-templates/components/FormMeta.vue` — `industryOptions`/`appOptions` cascade filter đổi sang pattern `(arr || []).map(String).includes(targetId)` (đồng bộ với 11 trang FE khác đã migrate)

### Checkpoint — 2026-04-10
Vừa hoàn thành: 7 fix downstream (5 BE + 2 FE) + smoke test thành công màn `/assign/form-templates/add` (cascade Nhóm ngành → Nhóm giải pháp → Ứng dụng).
Đang làm dở: chưa có
Bước tiếp theo: User chạy `php artisan migrate` rollback + test lại với data thật, smoke test các màn còn lại trong checklist Task 49 (CustomerScopes, SurveyQuestions, ProspectiveProject create/update, báo cáo SolutionsWorkSummary)
Blocked: Task 2 (backup DB), Task 6 (chạy migration), Task 34 (file Excel mẫu) — vẫn cần user thao tác thủ công

### Checkpoint — 2026-04-10 (FINAL)
Vừa hoàn thành: User đã hoàn tất Task 2 (backup DB), Task 6 (chạy migration thành công), Task 34 (cập nhật file Excel mẫu), Task 49 (smoke test các form downstream).
Đang làm dở: không
Bước tiếp theo: feature đóng — sẵn sàng merge
Blocked: không

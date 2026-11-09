# Giao chỉ tiêu kinh doanh (#11643 + #11651) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Người phụ trách:** @junfoke — 2026-11-06

**Goal:** Port 2 màn ERP "Phiếu giao chỉ tiêu kinh doanh theo phòng ban / theo nhân viên" sang HRM (phân hệ Bán hàng) theo bản mẫu QA, bỏ nhập chi tiết khách hàng, thêm cấp Bộ phận.

**Architecture:** BE ở `hrm-api/Modules/Finance` (cạnh DivisionMarket): Entity trỏ bảng ERP `business_target_*` + 1 bảng mới, mỗi phiếu 1 Service đọc/ghi + Controller V1; phần dùng chung (8 cột số, trạng thái, sinh số) tách helper/trait. FE `hrm-client/pages/finance/business-target-{departments,employees}` + component bảng cây `TargetTreeTable` dùng chung. ERP (TanPhatDev) chỉ sửa 2 báo cáo + ẩn menu.

**Tech Stack:** Laravel (nwidart modules), PHPUnit chạy trên DB gộp thật với `DatabaseTransactions`; Nuxt 2 / Vue 2, V2Base*; Blade + AngularJS (ERP).

**Spec:** `docs/superpowers/specs/gop-db/2026-11-06-giao-chi-tieu-kinh-doanh-design.md` (tóm tắt `design.md` cùng thư mục). Mọi mục "spec §x" bên dưới trỏ vào file này.

## Global Constraints

- **Không commit / push** (rule `CLAUDE.md` gốc) — user tự commit. Các task kết thúc bằng bước verify.
- Nhánh: `feat/giao-chi-tieu-kinh-doanh` tách từ `origin/gop_db` ở **cả 3 repo** hrm-api, hrm-client, TanPhatDev (Task 0).
- Bảng ERP: HRM ghi đủ mọi cột ERP ghi; không ghi `business_target_department_details` / `business_target_for_customers` (spec §2).
- 8 cột số: `{corporate|external}_{product|service}_{customer_number|quantity_value}`; số nguyên ≥ 0, tối đa 13 chữ số (review 06/11); ô trống lưu `NULL`.
- Trạng thái: 1 Đang tạo · 2 Chờ duyệt · 3 Đã duyệt · 5 Hủy; BE trả `status_text`, `status_color`.
- Số phiếu: `{company.code}_CTKD_{year}.{id 5 số}` / `{company.code}_CTKDNV_{year}.{id 5 số}`.
- Quyền: 8 quyền mới guard `api`, `type` 23, tên đúng bảng spec §4; thêm **cuối** `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, không id, rồi `php artisan permission:sync`.
- Câu thông báo/xác nhận: nguyên văn spec §3, §6.3, §7, §8 (toast chung theo bộ QLDA của skill `erp-to-hrm-screen`).
- UI: skill `erp-to-hrm-screen` (+ `list-page`, `form-validate`, `unsaved-changes`, `button-convention`, `print-page`, `export-excel`, `permission-seeder`, `notification-convention`, `entity-history`). Nhãn "Người tạo / Ngày tạo". Ô số 0 ở dòng chi tiết để trống.
- Test BE: `php vendor/bin/phpunit Modules/Finance/Tests/Feature/<File>.php` từ `hrm-api`; năm test `2099`, không đụng dữ liệu thật; reset cache trait quyền trong `setUp` như `BonusEndYearSettlementApproveTest`.
- Verify FE (không có eslint): parse `.vue` bằng `vue-template-compiler` + `@babel/core` (memory `project_moi_truong_dev`), rồi bấm thật Playwright (đóng browser sau khi xong).

## Review Focus

1. **Phiếu cũ ERP** (có chi tiết KH, có dòng "nhân viên mới" `employee_id` NULL + `fullname`) mở Xem ở HRM → hiện đủ 8 số, nhân viên mới hiện `fullname`; mở Sửa → dòng đó báo "Bắt buộc phải nhập" ở ô nhân viên, không crash. → test ở Task 6.
2. **Hai người lưu cùng kỳ / trạng thái đổi giữa chừng** → kiểm trùng trong transaction có `lockForUpdate`; thao tác trên phiếu đã đổi trạng thái → 409. → test ở Task 4.
3. **Một phòng nằm ở 2 khối trong cùng tỉnh** → chỉ tiêu phòng = SUM, không lấy 1 dòng. → test ở Task 6.
4. **Phòng/bộ phận đã ngừng hoạt động** trong phiếu cũ → Xem vẫn hiện tên lưu sẵn (`department_name`/`part_name`); dropdown không cho chọn mới. → test ở Task 3.
5. **Số gửi qua API sai dạng** (âm, thập phân, > 15 chữ số, chuỗi "1.234") → 422 đúng ô. → test ở Task 5.

---

## Phase 0 — Chuẩn bị

### Task 0: Tách nhánh

- [x] **Step 1:** Ở từng repo `hrm-api`, `hrm-client`, `TanPhatDev`: `git status --porcelain` phải rỗng. TanPhatDev đang có 1 file chưa commit (06/11) → **hỏi user** xử lý trước, không tự stash/discard.
- [x] **Step 2:** `git fetch origin && git switch -c feat/giao-chi-tieu-kinh-doanh origin/gop_db` ở cả 3 repo (repo chính; `gop_db` đang bị worktree giữ nên không switch sang nó).
- [x] **Step 3:** Verify: `git -C <repo> branch --show-current` ra `feat/giao-chi-tieu-kinh-doanh` cả 3.

## Phase 1 — BE nền

### Task 1: Bảng bộ phận, Entity, quyền

**Files:**
- Create: `hrm-api/Modules/Finance/Database/Migrations/2026_11_06_000001_create_business_target_department_parts_table.php`
- Create: `hrm-api/Modules/Finance/Entities/BusinessTarget/{BusinessTargetCompany,BusinessTargetDepartmentGroup,BusinessTargetAreaGroup,BusinessTargetProvince,BusinessTargetDepartment,BusinessTargetDepartmentPart,BusinessTargetForDepartment,BusinessTargetForProvince,BusinessTargetForEmployee}.php`
- Create: `hrm-api/Modules/Finance/Entities/BusinessTarget/Concerns/HasBusinessTargetStatus.php`
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (cuối file)
- Test: `hrm-api/Modules/Finance/Tests/Feature/BusinessTargetEntityTest.php`

**Interfaces:**
- Produces: Entity `extends BaseModel`, `$table` tường minh (bảng spec §2.1/§2.2; `BusinessTargetAreaGroup` → `area_groups`). Quan hệ: Company `groups()` → Group `areaGroups()`, `provinces()` → Province `departments()` → Department `parts()`; ForDepartment `provinces()` → ForProvince `employees()`.
- Trait `HasBusinessTargetStatus`: `const STATUS_CREATING=1, STATUS_PENDING=2, STATUS_APPROVED=3, STATUS_CANCELLED=5`; `statusText(): string`, `statusColor(): string`, `isLocked(): bool` (≠ Đang tạo — dùng cho `recordNotLocked`), `abstract codePrefix(): string` (`CTKD` / `CTKDNV`), `generateCode(): string`.
- Migration bảng `business_target_department_parts`: cột theo spec §2.3, decimal(16,2) cho 8 cột, index `business_target_department_id`, `business_target_company_id`.

- [x] **Step 1: Test** `BusinessTargetEntityTest`:
  - `test_new_parts_table_exists`: `Schema::hasColumns('business_target_department_parts', ['part_id','part_name','corporate_product_customer_number', …8 cột])` true.
  - `test_existing_erp_ticket_loads_tree`: lấy 1 `business_target_companies` status 3 bất kỳ → `groups.provinces.departments` load được, `->statusText() === 'Đã duyệt'`.
  - `test_generate_code_format`: phiếu tạm company TPE, year 2099, id 46 → `generateCode() === 'TPE_CTKD_2099.00046'`; bản ForDepartment → `TPE_CTKDNV_2099.00046`.
- [x] **Step 2:** Chạy → FAIL (class/bảng chưa có).
- [x] **Step 3:** Viết migration, trait, 9 Entity; thêm 8 quyền (spec §4) cuối seeder; chạy `php artisan migrate --path=Modules/Finance/Database/Migrations/2026_11_06_000001_create_business_target_department_parts_table.php` và `php artisan permission:sync --dry-run` rồi `permission:sync`.
- [x] **Step 4:** Chạy test → PASS; `permission:sync --dry-run` lần 2 báo 0 thay đổi.

### Task 2: Helper 8 cột số

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BusinessTarget/BusinessTargetNumbers.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/BusinessTargetNumbersTest.php`

**Interfaces:**
- Produces (static): `COLUMNS` (8 tên cột, thứ tự: corporate_product_customer_number, corporate_product_quantity_value, corporate_service_customer_number, corporate_service_quantity_value, external_… như trên); `BEFORE_COLUMNS` (`before_` + từng cột); `sum(iterable $rows): array` (8 key, NULL coi 0, trả int); `isEmpty(array $row): bool`; `revenue(array $row): int` (= 4 cột `*_quantity_value`); `pairErrors(array $row): array<string,string>` (key cột → câu "Bắt buộc nhập SL Khách vì đã có doanh số" / "Bắt buộc nhập doanh số vì đã có SL Khách", spec §3.7); `normalize(array $row): array` (8 key, `''`/null → null, số → int).

- [x] **Step 1: Test:** `sum` 2 dòng `[corporate_product_customer_number=>2]`+`[…=>3, external_service_quantity_value=>1000000]` → 5 và 1000000, cột còn lại 0; `revenue` dòng có 2 doanh số 100+200 → 300; `pairErrors(['corporate_product_quantity_value'=>500])` → `['corporate_product_customer_number' => 'Bắt buộc nhập SL Khách vì đã có doanh số']`; `isEmpty([])` true.
- [x] **Step 2:** Chạy → FAIL. **Step 3:** Viết class. **Step 4:** Chạy → PASS.

## Phase 2 — BE phiếu theo phòng ban (#11643)

### Task 3: Service đọc + phạm vi

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BusinessTarget/BusinessTargetDepartmentService.php` (phần đọc)
- Test: `hrm-api/Modules/Finance/Tests/Feature/BusinessTargetDepartmentScopeTest.php`

**Interfaces:**
- Consumes: Task 1, Task 2.
- Produces: `listQuery(Request $r): Builder` (lọc `q` số phiếu, `company_id`, `year`, `created_by`, `approved_by`, `status`; `type=for-approve` → status 2 + công ty mình có quyền Duyệt), `paginate(Request $r)`; `find(int $id): ?BusinessTargetCompany` áp phạm vi spec §4; `detailTree(BusinessTargetCompany $e): array` (`groups[] → {group_id, group_name, area_ids[], provinces[] → {province_id, province_name, before{8}, total{8}, departments[] → {department_id, department_name, numbers{8}, parts[] → {part_id, part_name, numbers{8}}}}}`, tên lấy từ cột lưu sẵn); `beforeYear(int $companyId, int $year, int $groupId): array<province_id, array{8}>` (phiếu năm−1 status 3 cùng công ty + khối, SUM theo tỉnh); `options(): array` (`groups` theo công ty người dùng, `areas` kèm `province_ids` từ `provinces.area_id`); `departmentOptions(int $groupId): array` (`departments.group_id`, status hoạt động); `partOptions(int $departmentId): array` (`parts.department_id`, `status=1`).
- Phạm vi: quyền "Xem … của tổng công ty" → tất cả; "… của công ty" → cùng `company_id`; còn lại → `created_by` = mình; cộng phiếu Chờ duyệt cùng công ty nếu có quyền Duyệt và phiếu `approved_by` = mình; status 1 chỉ người tạo; `company_id` null → `whereRaw('1=0')`.

- [x] **Step 1: Test** (tạo phiếu năm 2099 bằng Entity): nhân viên thường không quyền chỉ thấy phiếu mình tạo; có quyền xem công ty thấy phiếu Chờ duyệt cùng công ty nhưng **không** thấy phiếu Đang tạo của người khác; `type=for-approve` với quyền Duyệt ra đúng phiếu status 2; `beforeYear(company, 2099, group)` trả số của phiếu 2098 status 3 và bỏ qua phiếu 2098 status 1; **Review Focus 4:** phòng có `departments.status` ngừng → `detailTree` vẫn trả `department_name` lưu sẵn, `departmentOptions` không chứa phòng đó.
- [x] **Step 2:** FAIL. **Step 3:** Viết. **Step 4:** PASS.

### Task 4: Service ghi + luồng trạng thái

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/BusinessTarget/BusinessTargetDepartmentService.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/BusinessTargetDepartmentWriteTest.php`

**Interfaces:**
- Produces: `save(array $data, ?BusinessTargetCompany $e = null, bool $send = false): BusinessTargetCompany` — transaction; kiểm trùng (công ty, năm, status ≠ 5, khác id) với `lockForUpdate` → ValidationException `year` "Công ty đã có phiếu <số> (<trạng thái>) cho năm <năm>"; bỏ dòng trống; phòng có `parts` → 8 số phòng = `BusinessTargetNumbers::sum(parts)`; tỉnh = sum phòng; `before_*` tính lại bằng `beforeYear` (bỏ số client); xoá-chèn lại bảng con (kể cả parts); sinh `code`; `part_id` người tạo; nếu `$send` → như `send()`.
- `send(BusinessTargetCompany $e): void` (status 1→2; tổng `revenue` = 0 → ValidationException "Phiếu chưa có chỉ tiêu doanh số — không gửi được"; không ai có quyền Duyệt cùng công ty → ValidationException "Chưa phân quyền người duyệt"; `received_time`; thông báo người duyệt), `approve()` (2→3, `approved_by`, `approved_time`, báo người tạo), `reject(e, string $reason)` (2→1, `note`, báo người tạo), `unApprove(e)` (3→1, xoá approved_*, **chặn** khi có `business_target_for_departments` status ∈ {2,3} cùng `company_id` + `year` và `plan_department_id` ∈ các phòng của phiếu → ValidationException câu spec §3.4b), `cancel(e)` (1|2 → 5).
- Mọi chuyển trạng thái sai trạng thái nguồn → `ConflictHttpException` (409). Ghi lịch sử `CatalogHistoryService` (tạo, sửa, send, approved, rejected kèm lý do, un_approved, cancelled).

- [x] **Step 1: Test:** lưu phiếu 2099 có 1 phòng chia 2 bộ phận (3 và 4 khách hãng HH) → dòng phòng `corporate_product_customer_number` = 7, tỉnh = 7, 2 dòng trong `business_target_department_parts`; lưu lại lần 2 không nhân đôi dòng con; tạo phiếu thứ 2 cùng công ty 2099 → lỗi `year`; Hủy phiếu 1 rồi tạo lại → OK; `send` khi doanh số 0 → lỗi đúng câu; luồng send→reject(lý do)→send→approve→unApprove ra status đúng + `note`; `unApprove` khi có phiếu nhân viên 2099 status 2 của phòng trong phiếu → lỗi; **Review Focus 2:** gọi `approve` trên phiếu status 1 → 409.
- [x] **Step 2:** FAIL. **Step 3:** Viết. **Step 4:** PASS.

### Task 5: Controller, Request, routes, in, xuất

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/BusinessTargetDepartmentController.php`, `Http/Requests/BusinessTarget/BusinessTargetDepartmentRequest.php`, `Transformers/BusinessTargetResource/BusinessTargetDepartmentListResource.php`, `Resources/views/prints/business_target_department.blade.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (group mới sau `division-market-employees`), `app/ExcelExport/ExportColumnRegistry.php`, `app/Services/CatalogHistoryService.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/BusinessTargetDepartmentApiTest.php`

**Interfaces:**
- Routes prefix `/business-target-departments` theo khuôn DivisionMarket: `GET /` · `GET /options` · `GET /department-options?group_id=` · `GET /part-options?department_id=` · `GET /before-year?year=&group_id=` · `GET /export-rows` (route tĩnh trước `/{id}`) · `POST /` ($create) · `GET /{id}` · `GET /{id}/print-data` · `GET /{id}/history` · `PUT /{id}` ([$locked,$create]) · `POST /{id}/send` ($create) · `/approve` `/reject` `/un-approve` ($approve) · `/cancel` ($create). `$locked = recordNotLocked:id,…BusinessTargetCompany`.
- Request: nháp `year` required int 2000–2100, `groups` array min 1, `groups.*.area_ids` array min 1; số `nullable|integer|min:0|max:999999999999999`; khi `send=true` thêm luật spec §6.4 + `pairErrors`.
- `show` trả `detailTree` + cờ `is_can_edit/send/approve/reject/un_approve/cancel/print/export` + `status_text/status_color`.
- Bản in blade theo spec §8 (A4 ngang, chữ ký `SignerTitleHelper`).

- [x] **Step 1: Test API** (actingAs nhân viên có quyền Tạo): POST nháp → 200 + `code` dạng `…_CTKD_2099.`; **Review Focus 5:** POST số `-1`, `1.5`, `"1.234"`, `1234567890123456` → 422 đúng key; PUT phiếu status 2 → 423; GET `/{id}` người ngoài phạm vi → 404; `print-data` trả HTML chứa "PHIẾU GIAO CHỈ TIÊU KINH DOANH THEO PHÒNG BAN".
- [x] **Step 2:** FAIL. **Step 3:** Viết. **Step 4:** PASS + `php artisan route:list --path=business-target-departments` đủ route.

## Phase 3 — BE phiếu theo nhân viên (#11651)

### Task 6: Service đọc + nạp chỉ tiêu phòng

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BusinessTarget/BusinessTargetEmployeeService.php` (phần đọc)
- Test: `hrm-api/Modules/Finance/Tests/Feature/BusinessTargetEmployeeReadTest.php`

**Interfaces:**
- Consumes: Task 1–3.
- Produces: `listQuery/paginate` (thêm lọc `plan_department_id`, phạm vi như Task 3 với bộ quyền "…theo nhân viên"); `find`; `allowedDepartmentIds(int $companyId): array` — có quyền Xem công ty/tổng công ty → mọi phòng công ty, không thì `employee_manage_departments` của user (như ERP `BusinessTargetDepartmentController` ~125-136); `departmentOptions(int $year): array` = allowed ∩ phòng có chỉ tiêu trong phiếu phòng ban status 3 năm đó; `departmentTarget(int $companyId, int $year, int $departmentId): array<province_id, {province_name, numbers{8}}>` — SUM `business_target_departments` theo tỉnh từ phiếu phòng ban status 3; `detailTree(e)` (`provinces[] → {province_id, province_name, target{8} (mới nhất từ departmentTarget, tỉnh mới phát sinh được thêm), total{8}, employees[] → {employee_id, label "Tên - Mã", fullname, numbers{8}}}`); `employeeOptions(int $companyId, string $q): array`.

- [x] **Step 1: Test:** **Review Focus 3:** phiếu phòng ban 2099 status 3 có phòng X ở khối A và khối B cùng tỉnh HN (5 và 7) → `departmentTarget(…X)[HN]` = 12; phiếu phòng ban status 2 không được tính; user không quyền chỉ thấy phòng trong `employee_manage_departments`; **Review Focus 1:** phiếu nhân viên có dòng `employee_id` NULL `fullname='Nguyễn Văn Test'` → `detailTree` trả `label` = fullname, không lỗi.
- [x] **Step 2:** FAIL. **Step 3:** Viết. **Step 4:** PASS.

### Task 7: Service ghi + luồng trạng thái

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/BusinessTarget/BusinessTargetEmployeeService.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/BusinessTargetEmployeeWriteTest.php`

**Interfaces:**
- Produces: `save(array $data, ?BusinessTargetForDepartment $e = null, bool $send = false)` — `plan_department_id` ∉ `allowedDepartmentIds` → 403; trùng (công ty, phòng, năm, status ≠ 5) → lỗi `plan_department_id` "Phòng đã có phiếu <số> (<trạng thái>) cho năm <năm>"; phòng không có chỉ tiêu → lỗi "Phòng chưa có chỉ tiêu được duyệt cho năm <năm>"; nhân viên trùng trong 1 tỉnh → lỗi dòng; `before_*` tỉnh = `departmentTarget` (bỏ số client); tỉnh = sum nhân viên; **không** chặn vượt chỉ tiêu; ghi `employee_name/code` lưu sẵn, `fullname`/`type` để trống. `send/approve/reject/unApprove/cancel` như Task 4 (câu gửi 0 doanh số: "Phiếu chưa giao chỉ tiêu doanh số cho nhân viên — không gửi được"; quyền Duyệt "…theo nhân viên"; `unApprove` không có ràng buộc dây chuyền).

- [x] **Step 1: Test:** lưu phiếu 2099 cho phòng có chỉ tiêu → `before_*` tỉnh = chỉ tiêu phòng dù client gửi số khác; tổng giao vượt chỉ tiêu vẫn `send` được; phòng ngoài phạm vi → 403; trùng phiếu → lỗi; duyệt bằng user chỉ có quyền "Duyệt … theo phòng ban" → 403 (sửa lỗi ERP).
- [x] **Step 2:** FAIL. **Step 3:** Viết. **Step 4:** PASS.

### Task 8: Controller, routes, in, xuất

**Files:** như Task 5 với tên `BusinessTargetEmployee*`, blade `business_target_employee.blade.php`, prefix `/business-target-employees`; route tĩnh thêm `GET /department-options?year=`, `GET /department-target?year=&department_id=`, `GET /employee-options?q=`.
- Test: `BusinessTargetEmployeeApiTest.php` — tạo/sửa/gửi qua API; `department-target` với phòng ngoài phạm vi → 403; `print-data` chứa "PHIẾU GIAO CHỈ TIÊU KINH DOANH THEO NHÂN VIÊN" và tên nhân viên dạng "Tên - Mã".
- [x] Step 1 test → Step 2 FAIL → Step 3 viết → Step 4 PASS + `route:list`.

## Phase 4 — FE dùng chung

### Task 9: Helper, bảng cây, mixin hành động

**Files:**
- Create: `hrm-client/utils/business-target.js`, `hrm-client/components/business-target/TargetTreeTable.vue`, `hrm-client/utils/mixins/businessTargetActionsMixin.js`, `hrm-client/utils/export/businessTargetExcel.js`

**Interfaces:**
- `utils/business-target.js`: `TARGET_COLUMNS` (8 key như BE), `emptyNumbers()`, `sumNumbers(rows)`, `totalCols(numbers)` → 12 giá trị (8 + 4 tổng hãng+khác), `revenueOf(numbers)`, `overTarget(total, target)` → map cột → chênh (> 0).
- `TargetTreeTable.vue` props: `rows` (mảng phẳng `{key, level, type: 'total'|'target'|'province'|'before'|'line'|'sub', label, numbers, editable, pinned, parentKey}`), `levels` (nhãn ô "Hiển thị đến cấp"), `readonly`, `targetByKey` (tô cam, tooltip "Vượt chỉ tiêu giao <chênh>"), `errors` (key `<rowKey>.<col>`); slot `label` cho ô cây (ô chọn phòng/bộ phận/nhân viên do form cấp); emit `input(rowKey, col, value)`, `toggle(rowKey)`. Tiêu đề 3 tầng, ghim tiêu đề + dòng `pinned` + 2 cột trái, `V2BaseTableScroll`, ô số `V2BaseCurrencyInput` precision 0, ô chỉ đọc 0 → trống (dòng `total` hiện 0). Method `scrollToFirstError()`.
- Mixin: `doSend/doApprove/doReject(reason)/doUnApprove/doCancel(item)` gọi `${apiBase}/{id}/<action>` với `$confirm` câu spec §8, `$safeLoadingStart`, toast, rồi về danh sách/tải lại; `apiBase` khai ở component.

- [x] **Step 1:** Viết 4 file.
- [x] **Step 2:** Verify parse `.vue`/`.js` (Global Constraints) → "template OK / script OK".
- [x] **Step 3:** Verify logic: `node -e` import `utils/business-target.js` (babel) chạy `sumNumbers`, `totalCols` với dữ liệu Task 2 → kết quả khớp.

## Phase 5 — FE phòng ban

### Task 10: Danh sách

**Files:** Create `hrm-client/pages/finance/business-target-departments/index.vue` (bám `pages/finance/division-market-departments/index.vue` + checklist A/B/C skill).
- Cột/lọc/hành động spec §5; `localStorageKey`/`columnScreenKey` = `business-target-departments`; `?type=for-approve` đọc từ `filters.type`; Xuất Excel `ExportFieldsModal` → `export-rows`.
- [x] Step 1 viết → Step 2 parse OK → Step 3 Playwright: mở danh sách thấy 9 phiếu cũ ERP (đủ quyền xem tổng công ty), lọc Năm, sort, Cấu hình cột; chụp ảnh đặt cạnh bản mẫu.

### Task 11: Form Tạo / Sửa / Xem

**Files:** Create `pages/finance/business-target-departments/{create.vue,_id/index.vue,_id/edit.vue,components/BusinessTargetDepartmentForm.vue}` (khuôn `division-market-departments`, mixin `unsavedChangesMixin`, `saveAndContinuePageMixin`, `formValidateMixin`).
- Form dựng `rows` cho `TargetTreeTable` từ `detailTree`; Khối/Khu vực chọn nhiều; tab mỗi khối + Tổng hợp; thao tác chia/thêm/xoá bộ phận, đổi phòng, bỏ khối/vùng với câu xác nhận spec §6.3; Năm trước gọi `before-year`; nút đáy theo trạng thái spec §8; lỗi 422 map về ô + `scrollToFirstError` + chấm đỏ tab; màn Xem có `SystemInfoSection` (Lịch sử từ `/{id}/history`, skill `entity-history`), danh sách có hành động Lịch sử (`CatalogHistoryModal`). Task 14 làm y hệt cho phiếu nhân viên.
- [x] Step 1 viết → Step 2 parse OK → Step 3 Playwright luồng: tạo 2099 (2 khối, 1 vùng, 1 phòng chia 2 bộ phận) → Lưu → mở Sửa thấy đúng số → Lưu và gửi → (user có quyền Duyệt) Từ chối có lý do → Sửa → Gửi → Duyệt → Hủy duyệt → Hủy phiếu; mở 1 phiếu cũ ERP ở chế độ Xem đúng số. Chụp ảnh. Xoá phiếu test 2099 sau khi xong.

### Task 12: In + Xuất Excel 1 phiếu

**Files:** Modify `BusinessTargetDepartmentForm.vue`/`_id/index.vue` (nút In `$printPreview({url: 'finance/business-target-departments/{id}/print-data'})`), dùng `utils/export/businessTargetExcel.js` (`exportDepartmentTicket(detail)`: mỗi khối 1 sheet theo cây mở hết + sheet Tổng hợp, `addExcelSignatureBlock`).
- [x] Step 1 viết → Step 2 Playwright: In hiện popup đúng bố cục spec §8; tải Excel mở được, số khớp màn Xem.

## Phase 6 — FE nhân viên

### Task 13: Danh sách
**Files:** `pages/finance/business-target-employees/index.vue` — như Task 10, thêm lọc Phòng ban phụ thuộc Công ty.
- [x] Viết → parse OK → Playwright thấy 43 phiếu cũ (quyền tổng công ty), lọc Phòng ban.

### Task 14: Form Tạo / Sửa / Xem
**Files:** `pages/finance/business-target-employees/{create.vue,_id/index.vue,_id/edit.vue,components/BusinessTargetEmployeeForm.vue}`.
- Năm + Phòng ban (`department-options`) → `department-target` dựng dòng "Chỉ tiêu giao"; đổi Năm/Phòng có dữ liệu → hỏi spec §7; ô chọn nhân viên có tìm (`employee-options`, "Tên - Mã", mờ "Đã giao tại tỉnh này"); tô cam vượt (`targetByKey`); tab Tổng hợp theo nhân viên; In/Excel như Task 12 (`exportEmployeeTicket`).
- [x] Viết → parse OK → Playwright: dùng phiếu phòng ban 2099 đã duyệt ở Task 11 (duyệt lại nếu đã hủy) → tạo phiếu nhân viên, giao vượt thấy ô cam nhưng Gửi được; thử Hủy duyệt phiếu phòng ban → bị chặn đúng câu; mở phiếu cũ ERP có "nhân viên mới". Chụp ảnh, dọn dữ liệu 2099.

## Phase 7 — Menu

### Task 15: Gắn menu Bán hàng
**Files:** Modify `hrm-client/components/subsystem-menu/sale-hub.js:296` (`{ n: 'Theo phòng ban', link: '/finance/business-target-departments' }`, `{ n: 'Theo nhân viên', link: '/finance/business-target-employees' }`, giữ 'Phát triển sản phẩm' chuỗi trần), `:331` ('Giao chỉ tiêu chờ duyệt' → `/finance/business-target-departments?type=for-approve`; thêm mục '…theo nhân viên' nếu cấu trúc mục cho phép nhiều link, không thì giữ 1), `components/subsystem-menu/sale.js` `SALE_LINK_PERMISSIONS`.
- [x] Viết → Playwright: menu bấm vào đúng màn; mục chờ duyệt mở danh sách đã lọc.

## Phase 8 — ERP (TanPhatDev)

### Task 16: Báo cáo + ẩn menu
**Files:** Modify `TanPhatDev/app/Services/Reports/TargetBussinessDepartmentService.php` (3 chỗ đếm `business_target_department_details` → SUM `corporate_product_customer_number` / `corporate_service_customer_number` của `business_target_departments` cùng nhóm), `TargetBussinessEmployeeService.php` (tương tự với `business_target_for_employees`), view báo cáo tương ứng (ẩn link mở popup danh sách khách), `resources/views/layouts/topmenubar.blade.php:874-875, 2190-2198` (ẩn menu 2 màn + chờ duyệt; giữ menu báo cáo `:787-788`).
- [x] Step 1: Ghi lại số khách hãng của báo cáo hiện tại cho năm 2026 (phiếu cũ) trước khi sửa.
- [x] Step 2: Sửa; compile blade bằng script trong memory `project_moi_truong_dev`.
- [x] Step 3: Chạy lại báo cáo cùng tham số: số khách hãng = SUM cột đã nhập (đối chiếu bằng SQL `SELECT SUM(corporate_product_customer_number)…`); ghi nhận chênh với cách đếm cũ trong STATUS (dữ liệu cũ đếm KH không trùng ≠ SUM — báo user).
- [x] Step 4: Đăng nhập ERP local kiểm menu đã ẩn, báo cáo vẫn mở.

## Phase 9 — Nghiệm thu

### Task 17: Đối chiếu ERP + tài liệu
- [x] Chạy code ERP trên cùng DB với phiếu tạo từ HRM: `SalesDepartmentPlan::getDataTargetDepartmentEmployee`, `SalesEmployeePlan::getDataTargetEmployee`, ajax `target_business_department.getDataDepartment` → số khớp số HRM (memory "Đối chiếu số ERP ↔ HRM").
- [x] Rà checklist skill `erp-to-hrm-screen` (lệnh grep tự kiểm) cho 2 màn.
- [x] Đóng browser Playwright.
- [x] Cập nhật `plan.md` Checkpoint + `.plans/gop-db/STATUS.md` (mục Đang làm / Hoàn thành, link design/plan/spec), báo user các file để commit.

---

## Checkpoint — 2026-11-06 (cuối ngày)
- **Vừa hoàn thành:** Task 0–17. BE `Modules/Finance` (9 Entity + bảng mới `business_target_department_parts`, 2 service + trait
  luồng trạng thái, base controller + 2 controller, 2 Request, bản in A4 ngang, 8 quyền type 23) — 37 test PHPUnit xanh.
  FE: `BusinessTargetList` + `TargetTreeTable` dùng chung, 2 form, in/Excel 1 phiếu, menu sale-hub (+2 lối vào chờ duyệt).
  ERP: 4 link menu → HRM tab mới. Playwright local đi trọn luồng 2 màn; code ERP đọc đúng số HRM ghi.
- **Lệch so với plan (xem ledger Ruling):** không sửa 2 báo cáo ERP (đã SUM cột nhập sẵn); 422 `status` thay 409; nhân viên
  đã giao trong tỉnh bị loại khỏi ô chọn thay vì hiện mờ; danh sách dùng chung 1 component.
- **Review toàn nhánh (06/11):** 0 Critical, 5 Important đã sửa (gửi duyệt NV kiểm lại chỉ tiêu phòng; trần 13 chữ số;
  cache ô chọn tránh select2 dựng lại; tên sheet Excel bỏ ký tự cấm; link chờ duyệt trang chủ ERP → HRM) + 2 Minor. 39 test xanh.
- **Đang làm dở:** —
- **Bước tiếp theo:** user commit 3 repo; gán 8 quyền mới cho vai trò trên dev/prod (`permission:sync` + admin gán); QA.
- **Blocked:** —



## Ngày 06/11/2026 (@junfoke)
- [x] 06/11/2026 — Khảo sát Redmine #11651 + #11643: port sang HRM (không sửa ERP), làm #11643 theo phòng ban trước vì #11651 theo nhân viên nạp chỉ tiêu từ phiếu phòng ban Đã duyệt; user chốt làm chung 1 đợt.
- [x] 06/11/2026 — Làm chuyển đổi erp->hrm: Phiếu giao chỉ tiêu kinh doanh theo phòng ban (#11643) + theo nhân viên (#11651) — code xong 17/17 task, chưa commit (nhánh `feat/giao-chi-tieu-kinh-doanh` 3 repo). Viết design + spec + plan; user chốt Hủy duyệt → Đang tạo (không có Thu hồi), phòng của phiếu NV theo ERP. 39 test BE xanh, review toàn nhánh sửa 5 Important + 2 Minor. Chi tiết ở Checkpoint 06/11 phía trên.
- [x] 06/11/2026 (tối) — Kiểm thật lần cuối: 39/39 test BE pass; 9 test fail của module Finance (Theo dõi giữ hàng ×1, Phiếu nhập/xuất điều chỉnh kiểm kê ×8) là có sẵn — dựng bản sạch đúng commit gốc `36269786a` chạy cùng 3 file test, fail trùng tên từng cái, không do đợt này. Bấm thật trên trình duyệt local (chọn bằng chuột/bàn phím): phiếu phòng ban (Năm trước ra đúng số 2025, số 14 chữ số báo đỏ, Từ chối có lý do → gửi lại thì lý do cũ mất → Duyệt được), phiếu nhân viên (nạp chỉ tiêu phòng, giao vượt tô cam + tooltip), Hủy duyệt phòng ban bị chặn khi có phiếu NV chờ duyệt, Xuất Excel khối "Chi nhánh/Đơn vị thành viên" (trước lỗi), menu Bán hàng › Phê duyệt › Kế hoạch & chỉ tiêu. Xoá phiếu test, gỡ quyền gán tạm.

## Ngày 07/11/2026 (@junfoke)
- [x] 07/11/2026 — Theo user: file test chỉ dùng local, không đẩy lên → loại 9 file `Modules/Finance/Tests/Feature/BusinessTarget*.php` bằng `.git/info/exclude` của hrm-api (file vẫn trên đĩa để chạy).
- [x] 07/11/2026 — Phân quyền mới (Catalog + mã quyền) đã lên prod 06/11: kéo `gop_db` mới nhất về nhánh `feat/giao-chi-tieu-kinh-doanh`, chuyển quyền của 2 màn sang Catalog (`app/Support/Permissions/Catalog/sale.php`, dùng lại mã ERP + thêm `platforms` `hrm`, không khai seeder). Sao lưu `gop_db` local trước khi đụng (dump gzip) + chạy 43 migration chờ.
- [x] 07/11/2026 — Hỗ trợ user kéo DB prod `hrm_erp_gop` (đã chuyển RBAC) về local `gop_db_rbac` bằng Navicat Data Transfer: cấu hình MySQL (`max_allowed_packet` 1GB, `net_read/write_timeout` 600, `sql_mode` NO_ENGINE_SUBSTITUTION, `log_bin_trust_function_creators`), bỏ khoá ngoại/definer/transaction/lock, Continue on error. Trỏ `.env` sang DB mới.
- [x] 07/11/2026 — Xử lý lỗi migration `2026_11_06_000001_create_business_target_department_parts_table`: tên index tự sinh dài quá 64 ký tự (prod cũng sẽ lỗi) → đặt tên index ngắn. Sync Catalog (chỉ sửa `platforms` của 5 mã; prod đã có vai trò được cấp sẵn). 39/39 test pass trên DB RBAC mới; gọi API thật (nginx 8002) bằng DNS Admin (có đủ 5 mã qua vai trò thật) đúng; đang kiểm chiều người không có quyền + bấm thử trên client.

### Checkpoint — 2026-11-07 11:20
Vừa hoàn thành: merge phân quyền Catalog mới vào nhánh, sửa tên index migration, 39/39 test trên DB `gop_db_rbac`.
Đang làm dở: kiểm người không có mã quyền (danh sách trả 200 — đang xem có lọc về phiếu của chính mình không) + bấm thử client 3000.
Bước tiếp theo: xong kiểm quyền → user commit 3 repo (code vẫn chưa commit); QA.
Blocked: —

## Ngày 09/11/2026 (@junfoke)
- [x] 09/11/2026 — Kéo `gop_db` mới nhất về nhánh `feat/giao-chi-tieu-kinh-doanh` (fast-forward cả 3 repo, giữ nguyên phần đang làm, không conflict); chạy 13 migration upstream + `permission:catalog-sync` trên DB local `gop_db_rbac`. 39/39 test BusinessTarget pass.
- [x] 09/11/2026 — Bấm thật trên client 3000 + API nginx 8002 với dữ liệu prod (DNS Admin có đủ 5 mã qua vai trò thật): danh sách + chi tiết phiếu thật; trọn luồng phiếu phòng ban 2099 có cấp bộ phận (tạo → gửi → duyệt → hủy duyệt → gửi lại → duyệt), phiếu nhân viên nạp đúng chỉ tiêu phòng, chặn hủy duyệt phiếu phòng ban khi đã có phiếu NV duyệt, In (popup xem trước), Xuất Excel, 2 mục "chờ duyệt" ở menu Bán hàng hiện theo mã duyệt. Người không có mã: danh sách rỗng, xem phiếu người khác 404, tạo 403. Đã dọn dữ liệu thử 2099.

### Checkpoint — 2026-11-09
Vừa hoàn thành: cập nhật gop_db mới nhất + nghiệm thu đủ trên quyền mới với dữ liệu prod.
Đang làm dở: —
Bước tiếp theo: user commit 3 repo (file test `BusinessTarget*` chỉ để local); deploy cần chạy migration `2026_11_06_000001_create_business_target_department_parts_table` + `permission:catalog-sync` (build_tpe.sh tự chạy). Bộ test Finance còn lỗi ở màn khác chưa chuyển RBAC — ngoài phạm vi.
Blocked: —

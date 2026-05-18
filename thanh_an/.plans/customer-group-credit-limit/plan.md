# Hạn mức công nợ nhóm KH — Plan

**Người phụ trách:** @khoipv
**Trạng thái:** Code xong BE + FE, chờ user chạy migration + test browser
**Spec:** `docs/superpowers/specs/2026-05-18-customer-group-credit-limit-design.md`

## Phase 1 — BE (Task 1-5)

- [x] Task 1: Migration thêm 2 cột `max_debt_limit` (decimal 18,2 nullable) + `is_debt_limit_active` (tinyint default 0) vào `customer_groups`
  - File: `hrm-thanhan-api/database/migrations/2026_05_18_100000_add_debt_limit_to_customer_groups_table.php`
- [x] Task 2: Validation rule trong `CustomerGroupRequest` — `is_debt_limit_active` nullable|in:0,1; `max_debt_limit` nullable|numeric|min:1 + closure required_if khi toggle=1
  - File: `hrm-thanhan-api/Modules/Category/Http/Requests/CustomerGroup/CustomerGroupRequest.php`
- [x] Task 3: `CustomerGroupService` — thêm filter `is_debt_limit_active` trong `index()` + đưa 2 field vào cả update và create của `updateOrCreate()`
  - File: `hrm-thanhan-api/Modules/Category/Services/CustomerGroupService.php`
- [x] Task 4: `CustomerGroupResource` + `DetailCustomerGroupResource` — trả thêm 2 field (`max_debt_limit` float|null, `is_debt_limit_active` int)
  - File: `hrm-thanhan-api/Modules/Category/Transformers/CustomerGroupResource/CustomerGroupResource.php`
  - File: `hrm-thanhan-api/Modules/Category/Transformers/CustomerGroupResource/DetailCustomerGroupResource.php`
- [x] Task 5: `CustomerGroupController::getLogs` — map giá trị VN cho 2 cột: `is_debt_limit_active` ("Đang áp dụng" / "Không áp dụng"), `max_debt_limit` (`number_format(..., 0, ',', '.')` + " VNĐ", fallback "(trống)")
  - File: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/CustomerGroupController.php`

## Phase 2 — FE Modal (Task 6)

- [x] Task 6: `CustomerGroupModal.vue` — toggle iOS switch + input số format VND (1.000.000) + CSS scoped
  - Thêm 2 form-group SAU form-group "Trạng thái"
  - Computed `isDebtLimitActiveBool` (get/set 0↔bool) + `maxDebtLimitFormatted` (get format vi-VN, set strip non-digit → Number/null)
  - `resetModal` else: default `is_debt_limit_active: 0, max_debt_limit: null`
  - CSS scoped: `.toggle-row`, `.toggle`, `.toggle-track`, `.toggle-thumb`, `.toggle-label` (track 44×26, thumb 22×22, active #34c759)
  - Disable input khi `isShow || !isDebtLimitActiveBool` — giữ giá trị, không clear
  - File: `hrm-thanhan-client/components/modal/CustomerGroupModal.vue`

## Phase 3 — FE List (Task 7)

- [x] Task 7: `pages/category/customer_groups/index.vue`
  - Thêm `is_debt_limit_active: undefined` vào `initialStateForm`
  - Thêm `listDebtLimitStatus` (2 option: Đang áp dụng / Không áp dụng)
  - Filter dropdown Select2 mới (placeholder "Áp dụng hạn mức") trong collapse Bộ lọc
  - 2 cột mới sau `status`: `max_debt_limit` (text-right, sortable), `is_debt_limit_active` (text-center, sortable, badge xanh/xám)
  - Template `cell(max_debt_limit)`: nếu `is_debt_limit_active==1` thì format VN, ngược lại `—`
  - Template `cell(is_debt_limit_active)`: badge text
  - Method `formatMoney` (toLocaleString vi-VN) + `getDebtLimitBadge`
  - 2 entry vào array `columns` cho log: `max_debt_limit` → "Hạn mức công nợ tối đa", `is_debt_limit_active` → "Trạng thái áp dụng hạn mức"
  - File: `hrm-thanhan-client/pages/category/customer_groups/index.vue`

## Phase 4 — Test (Task 8)

- [ ] Task 8: User test end-to-end 6 case
  1. Tạo mới: toggle OFF → lưu OK; toggle ON + để trống hạn mức → toast lỗi tiếng Việt; toggle ON + nhập 500.000.000 → lưu OK
  2. Edit: mở lại → đúng giá trị + toggle ON; tắt toggle → input disable nhưng giữ 500.000.000; lưu → DB vẫn giữ giá trị cũ
  3. Edit nhóm KH cũ (chưa có data 2 cột): modal mở bình thường, toggle OFF, input rỗng, lưu OK
  4. Filter: chọn "Đang áp dụng" → lọc đúng; "Không áp dụng" → lọc đúng; Đặt lại → full list
  5. Lịch sử thay đổi: bảng log hiển thị `(trống) → 500.000.000 VNĐ`, `Không áp dụng → Đang áp dụng`
  6. Phân quyền cũ giữ nguyên (account không có quyền "Quản lý khách hàng" → ẩn nút Thêm/Sửa)

### Checkpoint — 2026-05-18
Vừa hoàn thành: Code Task 1-7 (BE migration/request/service/resource/controller log, FE modal toggle + format VND, FE list 2 cột + filter + log mapping)
Đang làm dở: User cần chạy `php artisan migrate` rồi test browser theo Task 8
Bước tiếp theo: User reload FE + test 6 case → báo lỗi nếu có
Blocked: (không có)

## Note pre-existing issues (NGOÀI scope, code reviewer flag — để dành plan cleanup riêng nếu user muốn)

Reviewer phát hiện 12 issue có sẵn trong codebase `customer_groups` (không phải code lần này gây ra):

**CRITICAL:**
- `CustomerGroupService::index()` filter `name`/`code` OR thiếu bọc closure → khi kết hợp với điều kiện khác sẽ leak record do precedence AND/OR
- `CustomerGroupService::updateOrCreate()` trả `response()->json(...)` → controller wrap lần 2 bằng `responseJson` → response bị double-wrap, status 404 bị nuốt
- `updateOrCreate()` gọi `$customerGroup->getOriginal()` TRƯỚC khi check `if ($customerGroup)` → NPE nếu id không tồn tại

**IMPORTANT:**
- `status` validation thiếu `in:0,1`
- `if (...) {} else { ... }` block rỗng → khó đọc
- Accessor `employee_update_name` / `employee_create_name` không null-safe → NPE khi employee bị xóa; thiếu eager loading → N+1

**MINOR:**
- `$guarded = []` ở model `CustomerGroup`
- `getLogs()` không paginate
- `DetailCustomerGroupResource` `created_at` format khác `updated_at` (không qua Helper)
- Soft delete check trong `unique` rule

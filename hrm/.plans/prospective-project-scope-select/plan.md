# Plan — Loại hình/Lĩnh vực KH chọn 1 + append hồ sơ KH

## Phase 1 — Chọn 1 + full catalog + 2 cấp + mapping 2 chiều (FE)

- [x] FE: Tạo component `CspSingleSelect.vue` (chế độ phẳng + 2 cấp, chọn 1, search, "Bỏ chọn")
- [x] FE: `CustomerBlock` — thay 2 `V2BaseSelect` bằng `CspSingleSelect` (Loại hình phẳng, Lĩnh vực 2 cấp)
- [x] FE: `CustomerInfoSection` — load full catalog (`getAll`) 1 lần, truyền `all-scope-groups`/`all-scopes`
- [x] FE: `businessFieldGroups` — build 2 cấp; chưa chọn Loại hình → hiện tất cả nhóm
- [x] FE: mapping 2 chiều — `onScopeChange` (chọn lĩnh vực → set loại hình cha), `onScopeGroupChange` (reset lĩnh vực nếu không tương thích)
- [x] FE: bỏ hint lọc ứng dụng + CSS `.app-hint` mồ côi ở `ProjectInfoSection`

## Phase 2 — Tick xanh "đã có trong hồ sơ KH" (AC2)

- [x] FE: `CspSingleSelect` thêm prop `marked-ids` (phẳng) + `marked-pairs` (2 cấp) → icon `ri-checkbox-circle-fill` xanh
- [x] FE: `CustomerBlock` computed `declaredGroupIds` + `declaredScopePairs` (từ `scope_group_options`/`scope_pair_options`) truyền xuống

## Phase 3 — Append Loại hình/Lĩnh vực vào hồ sơ KH khi lưu (BE, AC4)

- [x] BE: `ProspectiveProjectService::appendScopesToCustomers()` — gọi trong `store()` + `update()` sau `save()`
- [x] BE: `appendCustomerScopePair()` — insert-if-not-exists vào ERP `customer_activity_types` + `customer_business_fields` (chỉ thêm, không ghi đè); áp dụng KH trực tiếp + KH thụ hưởng cuối; try/catch + log

## Phase 4 — Sắp xếp option (yêu cầu bổ sung)

- [x] BE: `CustomerScopeGroupService::getAll` + `CustomerScopeService::getAll` đổi `orderBy('id')` → `orderBy('name')` (alpha cho TẤT CẢ màn dùng chung getAll: customer form, filter, project)
- [x] FE: `CspSingleSelect` — helper `sortByMarkedThenName` (tick xanh lên đầu, phần còn lại localeCompare 'vi'); áp dụng cho `filteredOptions` (phẳng) + `filteredGroups` (2 cấp: nhóm có tick lên trên + con có tick lên đầu, còn lại a,b,c)

## Phase 5 — Seeder dọn dữ liệu scope lệch mapping (yêu cầu bổ sung — xóa CẢ 2 trường)

- [x] BE: `CleanMismatchedCustomerScopeSeeder` (đổi từ ...BusinessFields...) — xóa CẢ 2: (1) Lĩnh vực `customer_business_fields` lệch (group NULL / cặp không thuộc master), (2) Loại hình `customer_activity_types` không còn cặp lĩnh vực hợp lệ backing; lô 500 + transaction
- [x] Phân tích tinker: business_fields đã bị xóa từ 283→16 (user đã chạy bản cũ). Hiện: business_fields 16 (0 lệch), activity_types 274 → xóa 267 / giữ 7
- [ ] CHƯA CHẠY (user tự chạy): `php artisan db:seed --class="Modules\Assign\Database\Seeders\CleanMismatchedCustomerScopeSeeder"`

## Test

- [x] AC1: chọn KH có sẵn scope → form tự điền
- [x] AC2: dropdown hiện tick xanh cạnh giá trị KH đã khai (Loại hình + Lĩnh vực) — Playwright
- [x] AC3: chọn giá trị mới (không tick xanh) → hiển thị trên form — Playwright
- [x] AC4: append vào ERP chỉ thêm, không ghi đè/trùng, giữ dữ liệu cũ — tinker (rollback)
- [x] Sort: màn dự án tick-xanh lên đầu + a,b,c (loại hình + lĩnh vực 2 cấp) — Playwright; màn tạo KH alpha qua getAll — Playwright

### Checkpoint — 2026-07-02
Vừa hoàn thành: toàn bộ Phase 1-3 + test AC1-AC4 đạt.
Đang làm dở: (không)
Bước tiếp theo: chờ review / merge.
Blocked:

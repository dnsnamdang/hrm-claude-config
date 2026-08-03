# customer-scope-single-group — Plan

@manhcuong — Đổi Lĩnh vực KH ↔ Nhóm từ n-n về 1-n, sửa toàn bộ phụ thuộc.

## Phase 1 — DB

### BE
- [x] Migration mới: thêm lại cột `customer_scopes.customer_scope_group_id` nullable
- [x] Backfill MIN(customer_scope_group_id) từ pivot cho mỗi lĩnh vực
- [x] Drop bảng pivot `customer_scope_group_members`

## Phase 2 — BE catalog Lĩnh vực KH

### BE
- [x] CustomerScope entity: `groups()` belongsToMany → `group()` belongsTo + fillable thêm cột
- [x] CustomerScopeGroup entity: `customerScopes()` belongsToMany → hasMany
- [x] CustomerScopeService: index/getAll dùng `group`; updateOrCreate/update set cột thay vì sync()
- [x] CustomerScopeRequest: `customer_scope_group_ids[]` → `customer_scope_group_id` required exists+active
- [x] CustomerScopeResource + DetailCustomerScopeResource: trả `customer_scope_group_id` + `customer_scope_group_name`
- [x] Import: validate + import chỉ nhận 1 mã nhóm, set cột thay vì sync

## Phase 3 — BE phụ thuộc

### BE
- [x] CustomerScopeGroupService.index: count subquery pivot → `where customer_scope_group_id`
- [x] Assign SaveCustomerRequest + UpdateCustomerRequest: validate scope∈group qua cột thay vì pivot
- [x] Human SaveCustomerRequest + UpdateCustomerRequest: validate scope∈group qua cột thay vì pivot
- [x] UpdateCustomerScopeGroupsSeeder: scope->groups()->sync → set cột customer_scope_group_id (1 nhóm đầu)

## Phase 4 — FE catalog

### FE
- [x] AddScopeModal.vue: select single `customer_scope_group_id` + validate inline
- [x] customer-scopes/index.vue: cột hiển thị 1 nhóm + mapping import

## Phase 5 — FE phụ thuộc

### FE
- [x] human CustomerScopeSelect.vue: scope→group 1-1 (groupId đơn), auto-fill nhóm theo lĩnh vực
- [x] assign CustomerForm.vue: filteredScopes/filteredScopeGroups/watch + mapScope sang single
- [x] customers/index.vue (filter): mapping group_ids từ single (giữ filter đa nhóm)
- [x] store/optionsSelect.js: trả customer_scope_group_id + customer_scope_group_ids=[gid] (tương thích)
- [x] prospective-projects/index.vue: KHÔNG đổi — đọc store đã trả mảng-1-phần-tử
- [x] add/_id/edit/CustomerInfoSection + meeting GeneralInfo/MeetingProject: KHÔNG đổi — vốn đọc field single của entity (customer/project tự lưu customer_scope_group_id + tra tên theo id, không qua pivot)

## Phase 6 — Verify
- [x] `php -l` 14 file BE sửa — PASS
- [x] FE: @babel/parser 6 SFC + store + vue-template-compiler 5 template — PASS
- [~] Rà soát ERP đọc pivot — FLAG: cần kiểm tra hệ ERP (TanPhatDev, ngoài 2 repo) có đọc bảng `customer_scope_group_members` qua remote DB không; nếu có sẽ hỏng sau khi drop pivot

---
## Checkpoint — 2026-06-15
Vừa hoàn thành: Toàn bộ code BE+FE đổi Lĩnh vực KH ↔ Nhóm từ n-n về 1-n.
- BE (14 file): migration revert (add cột + backfill MIN + drop pivot), 2 entity, 2 service, request catalog, 2 resource, controller show, 4 Customer request (Assign+Human), seeder. php -l PASS.
- FE (4 file đổi): AddScopeModal (select single), customer-scopes/index (cột single), CustomerScopeSelect, assign CustomerForm, customers/index filter, store. parse/template PASS.
- Đã xác minh prospective-projects + meeting KHÔNG bị ảnh hưởng (đọc field single của entity).
Đang làm dở: (không)
Bước tiếp theo: User chạy migration (`php artisan migrate`) + chạy hrm-client verify browser màn Tạo/Sửa Lĩnh vực KH (chỉ chọn 1 nhóm) + màn Khách hàng/Dự án TKT. Rà soát ERP đọc pivot.
Blocked: (không)

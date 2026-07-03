# customer-multi-scope — Plan

@manhcuong — Khách hàng ↔ Lĩnh vực KH 1-1 → n-n (HRM API + HRM Client + ERP). Giữ Nhóm đơn.
Spec: docs/superpowers/specs/2026-06-15-customer-multi-scope-design.md

## Phase 1 — DB

### BE (HRM)
- [x] Migration Human: tạo pivot `customer_customer_scopes` (customer_id, customer_scope_id, unique) + backfill từ customers.customer_scope_id + drop cột

### ERP
- [x] Migration ERP: tạo pivot `customer_customer_scopes` (FK customer_id) + backfill + drop cột customers.customer_scope_id

## Phase 2 — HRM API

### BE (Human)
- [x] Customer entity: thêm `scopes()` belongsToMany, bỏ `scope()` + fillable customer_scope_id
- [x] CustomerService: store/update sync pivot; index/show trả customer_scope_ids + names
- [x] Save/UpdateCustomerRequest: customer_scope_ids required|array|min1, mỗi id thuộc nhóm đã chọn

### BE (Assign — ghi/đọc ERP mysql2)
- [x] CustomerService: lưu sync pivot ERP; getScopeByCode trả mảng customer_scopes (bỏ field đơn); filter list qua pivot
- [x] Save/UpdateCustomerRequest (Assign): customer_scope_ids array, thuộc nhóm
- [x] CustomerDetailResource: customer_scope_ids + names, bỏ customer_scope_id đơn

## Phase 3 — HRM Client

### FE
- [x] CustomerScopeSelect.vue (human): ô Lĩnh vực multi-select trong nhóm, đổi nhóm loại lĩnh vực lệch nhóm
- [x] human CustomerForm.vue + assign CustomerForm.vue: bind customer_scope_ids, map khi sửa, payload mảng
- [x] customers/index.vue: filter Lĩnh vực gửi mảng + (BE đã lọc pivot)
- [x] prospective-projects add/_id/edit/CustomerInfoSection: chọn KH → 1 lĩnh vực auto-fill, nhiều thì dropdown chọn 1, nhóm auto

## Phase 4 — ERP (TanPhatDev)

### ERP BE
- [x] CustomerScopeReader.scopes(): đọc cột customer_scopes.customer_scope_group_id → group_ids=[gid] (FIX pivot đã drop); scopeBelongsToGroup theo cột
- [x] Customer model: helper customerScopeIds() đọc pivot; searchByFilter lọc lĩnh vực qua subquery pivot
- [x] CustomersController store/update: validate customer_scope_ids[] thuộc nhóm + sync pivot trong transaction + log history

### ERP FE (Blade/Angular)
- [x] customerForm.blade: select customer_scope_id → multiple ng-model customer_scope_ids
- [x] customerScopeJs.blade: viết lại cho mảng (scopeOptions lọc nhóm, đổi nhóm loại lĩnh vực lệch, bỏ auto-set nhóm)
- [x] classes/sale/Customer.blade submit_data: customer_scope_ids
- [x] Init customer_scope_ids:[] tại create + searchCustomerJs + searchCustomerModalProvinceJs + customermanager show_
- [x] edit.blade + customermanager: controller eager-load + map customer_scope_ids từ scopes
- [x] searchCustomer.blade (form tạo nhanh): select multiple customer_scope_ids

## Phase 5 — Verify
- [x] php -l toàn bộ file BE (HRM + ERP)
- [x] FE parse SFC + template compile (HRM client)
- [ ] Smoke: tạo/sửa KH nhiều lĩnh vực (HRM + ERP) + Dự án TKT chọn 1 từ nhiều
- [ ] Chốt thứ tự deploy: code trước → migrate HRM + ERP sau

---
## Checkpoint — 2026-06-15
Vừa hoàn thành: CODE DONE toàn bộ feature trải 3 codebase (HRM API + HRM Client + ERP).
- DB: 2 migration pivot `customer_customer_scopes` (HRM Modules/Human + ERP), backfill + drop cột customers.customer_scope_id.
- HRM API: Human (entity scopes(), service sync pivot + sync_data ERP→HRM pivot + show trả ids, 2 request array); Assign (scopeByCode trả mảng customer_scopes, show trả ids, filter pivot, syncErpScopes ghi pivot ERP, 2 request, DetailResource).
- HRM Client: CustomerScopeSelect (multi), human+assign CustomerForm (bind ids), CustomerInfoSection (1→auto-fill, nhiều→chọn 1). parse + template PASS.
- ERP: CustomerScopeReader FIX (đọc cột customer_scope_group_id thay pivot đã drop), Customer model (customerScopeIds + filter pivot), CustomersController (validate ids + sync pivot + history) + edit/show + CustomerManagerController gắn ids, blade form/scopeJs/submit_data/init×4/searchCustomer/customermanager multi-select.
- Verify: php -l 13 file (HRM+ERP) PASS; @babel/parser + vue-template-compiler 4 SFC PASS.
Đang làm dở: (không)
Bước tiếp theo: User chạy 2 migration (HRM `php artisan migrate` + ERP `php artisan migrate`) sau khi deploy code; smoke test tạo/sửa KH nhiều lĩnh vực (HRM /human/customers + ERP /sale/customers + CRM + modal) + Dự án TKT chọn 1 từ nhiều.
Blocked: (không)

### Checkpoint — 2026-06-15 (fix data)
Phát hiện khi test /assign/customers/41406/edit không hiện data: backfill pivot (lĩnh vực) ĐÚNG, nhưng dữ liệu cũ có `customers.customer_scope_group_id` lệch với nhóm THẬT của lĩnh vực (vd KH 41406 group=1 nhưng lĩnh vực 59 "Thực phẩm" thuộc group 14) → form lọc lĩnh vực theo nhóm nên không hiển thị được.
Fix: thêm migration `Modules/Human/.../2026_06_15_000003_reconcile_customer_scope_group_from_scope.php` — set lại customer_scope_group_id = nhóm catalog của lĩnh vực đầu, cho CẢ customers HRM (SQL JOIN) lẫn ERP (mysql2, PHP loop). Đã chạy: KH 41406 group 1→14, resource trả group=14 scope_ids=[59]. (Lưu ý: lỗi lúc 15:53 là do test trước khi migrate pivot — pivot tạo lúc 15:54.)

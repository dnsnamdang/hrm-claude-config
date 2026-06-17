# Plan — application-remove-customer-scope

## Phase 1 — BE gỡ customer scope khỏi Application

### BE
- [x] `Entities/Applications.php`: xóa `customerScopes()`, bỏ `$csOk` trong `isCanUnlockUpdate()`, dọn `use`
- [x] `Http/Requests/Applications/ApplicationsRequest.php`: xóa rule `customer_scope_ids` + `.*`
- [x] `Services/ApplicationService.php`: bỏ `with(customerScopes)`, filter, validate, sync/detach, import resolve
- [x] `Http/Controllers/Api/V1/ApplicationsController.php`: bỏ `load(customerScopes)`, bỏ rule `customerScopeCode` (2 chỗ)
- [x] `Transformers/ApplicationsResource/ApplicationsResource.php`: bỏ 4 field customer_scope_*
- [x] `Transformers/ApplicationsResource/DetailApplicationsResource.php`: bỏ 2 field customer_scope_*
- [x] `resources/views/exports/applications.blade.php`: bỏ 2 cột header + 2 cột body + sửa colspan (15→13, 14→12)
- [x] `php -l` các file sửa — PASS

## Phase 2 — BE downstream

### BE
- [x] `Services/ProspectiveProjectService.php` `autoFillFromApplication()`: ĐÃ được feature song song `prospective-project-customer-erp-scope` gỡ (không còn đọc customerScopes; giữ scope+industry) — không cần đụng
- [x] `Entities/CustomerScope/CustomerScope.php`: bỏ check applications trong `isCanLockUpdate()` (→ return true), xóa relation `applications()`, dọn `use Applications`
- [x] `database/seeders/QldaMasterDataSeeder.php`: bỏ đoạn `customerScopes()->syncWithoutDetaching` (dùng quan hệ đã gỡ); giữ raw DB delete (bảng vẫn tồn tại)
- [x] `php -l` các file sửa — PASS

## Phase 3 — FE gỡ customer scope khỏi màn Ứng dụng

### FE
- [x] `pages/assign/application/index.vue`: bỏ filter, cột list + template cell, computed `customerScopes`, dispatch fetch, key `filters.customer_scope_id`, payload export
- [x] `index.vue` import: bỏ cột `CustomerScopeCode` (config + validate `LVKH.XXXX` + mapping 2 chỗ + comment)
- [x] `components/modal/application-modal.vue` (form thêm/sửa/chi tiết — BỊ SÓT lần đầu, fix sau khi user báo): bỏ field select Lĩnh vực KH + error, `customer_scope_ids` trong data/reset, computed `customerScopes`, mapping load, dispatch fetch
- [x] `static/Mau_Import_UngDung_FN.xlsx` (file mẫu import tải về — BỊ SÓT, fix sau khi user báo): xóa cột "Mã lĩnh vực khách hàng" ở sheet DM_ungdung (gắn lại dropdown Trạng thái), xóa 2 sheet MAP_ungdung_lvkh + DM_linhvucKH, dọn dòng tương ứng trong HDSD_KHAIBAO. (STRICT.xlsx không dùng → bỏ qua)
- [x] Quét xác nhận FE không còn tham chiếu Lĩnh vực khách hàng — sạch (index.vue + modal + file mẫu)

## Phase 4 — Verify
- [x] BE tinker: Resource không còn `customer_scope_names`; `isCanUnlockUpdate` + `CustomerScope::isCanLockUpdate` chạy không lỗi; tạo application không customer scope PASS + pivot ghi 0 dòng (rollback)
- [ ] FE: user chạy npm dev verify AC1/AC2/AC3 trên browser (node_modules trống nên chưa lint/build được tại đây)

---

### Checkpoint — 2026-06-09 (full regression test)
Vừa hoàn thành: Toàn bộ Phase 1-4 + fix 2 chỗ bị sót (application-modal.vue form, file mẫu Mau_Import_UngDung_FN.xlsx) + tinh chỉnh layout (Trạng thái ngang Nhóm giải pháp). Test 1 lượt:
- Quét code: 0 tham chiếu LVKH ở index.vue + application-modal.vue + 8 file BE + blade export + file mẫu
- php -l 8 file BE: PASS
- File mẫu: còn 4 sheet, header DM_ungdung không còn cột LVKH
- Tinker: AC3.1 thêm mới OK (pivot 0), AC3.2 cập nhật OK (pivot 0), AC2 Resource list+detail không key customer_scope, import validate không LVKH → hợp lệ 0 lỗi
→ AC1/AC2/AC3 đạt ở mức code + DB.
Đang làm dở: —
Bước tiếp theo: user chạy hrm-client (npm dev, Node ≥14) + hard refresh → verify trực quan browser (filter list, form, file mẫu, export Excel).
Blocked: Không build/lint FE tại máy này (node_modules hrm-client trống) → chỉ còn verify mắt thường.

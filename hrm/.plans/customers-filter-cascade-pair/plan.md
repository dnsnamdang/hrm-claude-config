# Plan — Bộ lọc Loại hình/Lĩnh vực màn /assign/customers giống /assign/prospective-projects

## Phase 1 — Frontend (hrm-client) ✅
- [x] `pages/assign/customers/index.vue`: bỏ 2 ô `V2BaseSelect` multiple → 1 `CascadePairSelect` (col-md-6), `:key="cpsRemountKey"`
- [x] filters: bỏ `customer_scope_id`, thêm `customer_scope_pairs` (mảng cặp) + giữ `customer_scope_group_id` (cha chọn riêng)
- [x] computed `scopePairParentOptions` / `scopePairChildOptions` (map `group_ids` → `parent_ids`) / `selectedScopePairsParam` (CSV "gid:sid")
- [x] `onCpsParentsChange` thay `onScopeGroupsChange` + `onScopesChange`; reset bump `cpsRemountKey`
- [x] Style: `.advanced-filters{overflow:visible}` + `::v-deep .cps-label{font-weight:600}`

## Phase 2 — Backend (hrm-api) ✅
- [x] `CustomerService::index`: thêm param `customer_scope_pairs`, khớp CẶP trên `customer_business_fields` (group_id + scope_id), OR với `customer_scope_group_id` (bảng `customer_activity_types`)
- [x] Helper `toScopePairArray()` (nhận CSV "gid:sid" / mảng / mảng object), giữ nhánh cũ `customer_scope_ids` để tương thích
- [x] `php -l` sạch

## Phase 3 — Verify
- [x] Playwright (Python, 1600x950 + 1440x800): panel Loại hình + Lĩnh vực render đầy đủ, KHÔNG bị `.advanced-filters` cắt (computed overflow = visible), `elementFromPoint` trong vùng panel trả `.cps-row-label` → panel nằm TRÊN bảng dữ liệu; 226 option; 0 lỗi console
- [ ] User hard-refresh test thực tế (nghi ngờ HMR stale khi báo lỗi che)

### Checkpoint — 2026-07-29
Vừa hoàn thành: FE + BE đổi bộ lọc Loại hình/Lĩnh vực màn KH sang CascadePairSelect + lọc theo cặp (OR với loại hình chọn riêng). User đã chốt phương án "giống hoàn toàn (UI + logic OR theo cặp)" — hành vi lọc KHÁC bản cũ (trước là AND, lĩnh vực lọc rời không so cặp).
Bước tiếp theo: User kiểm tra thực tế / cho phép chạy Playwright verify.
Blocked:

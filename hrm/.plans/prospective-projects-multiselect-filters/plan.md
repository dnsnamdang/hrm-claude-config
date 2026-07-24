# Plan — Multi-select 3 bộ lọc màn Dự án tiền khả thi

Người phụ trách: @manhcuong

Màn: `/assign/prospective-projects` (Danh sách dự án tiền khả thi).
Đổi 3 filter single → multi: Loại hình + Ứng dụng = CheckboxMultiSelect; Lĩnh vực = CascadeTreeSelect (treeview). Giữ cascade 2 chiều (union theo mảng). List auto-lọc (deep watcher sẵn có).

## Phase 1 — Frontend (index.vue) ✅

### FE — state & serialize
- [x] initialStateForm: `application_id: []`, `customer_scope_group_id: []`, bỏ `customer_scope_id` thêm `customer_scope_pairs: []`; init + handleReset deep-clone (JSON) tránh share ref mảng
- [x] computed `selectedApplicationIds` / `selectedGroupIds` / `selectedScopeIds`
- [x] `buildApiFilters()`: strip `customer_scope_pairs`, thêm `customer_scope_id = selectedScopeIds`; dùng `buildQuery` (serialize `[]`) cho loadData + exportExcel
- [x] import `buildQuery`; `normalizeCatalogFilters()` chuẩn hoá localStorage cũ (scalar→array)

### FE — template
- [x] Ứng dụng → CheckboxMultiSelect (show-select-all + search)
- [x] Loại hình → CheckboxMultiSelect (show-select-all + search)
- [x] Lĩnh vực → CascadeTreeSelect (treeview cha Loại hình → con Lĩnh vực)
- [x] import + register CheckboxMultiSelect, CascadeTreeSelect
- [x] FIX UI: `.advanced-filters { overflow: visible }` (scoped, không !important) để panel dropdown/treeview không bị v2-styles overflow:hidden cắt

### FE — cascade (array-aware, giữ 2 chiều)
- [x] `hasOtherCatalogFilter` / `applicationMatchesFilters` → so khớp theo mảng
- [x] `applicationFilterOptions` / `groupFilterOptions` / `customerScopeFilterOptions` → array-aware union
- [x] `applicationFilterMulti` / `groupFilterMulti` (text→name), `treeChildOptions` (+parent_ids), `treeParentOptions` (cha của child đang hiển thị)

## Phase 2 — Backend (ProspectiveProjectService::index) ✅
- [x] 3 filter: `where` → `whereIn` chuẩn hoá `(array)` + bỏ rỗng (application_id, customer_scope_id, customer_scope_group_id)
- [x] Export reuse `index()` → tự áp dụng whereIn

## Phase 3 — Verify ✅
- [x] php -l service sạch
- [x] API thật: single app=100 (19) == array app[]=100 (19) backward compat; app[]=100,101=23 (union); csg[]/cs[] ra tập con; no filter=32
- [x] Playwright: AC1 màn tải; AC2 Loại hình multi (network `customer_scope_group_id[]=10&[]=21`) + cascade narrow; AC3 Lĩnh vực treeview tick con → chip "Cha:Con" + `customer_scope_id[]=70` auto-lọc; AC4 Ứng dụng multi dropdown search+select all (pp-3); 0 lỗi console
- [ ] User verify browser

### Checkpoint — 2026-07-14
Vừa hoàn thành: BE whereIn + FE multi-select 3 filter (CheckboxMultiSelect x2 + CascadeTreeSelect) giữ cascade union + fix overflow panel. Verify API + Playwright đủ 4 AC.

### Checkpoint 2 — 2026-07-14 (đổi theo popup)
User yêu cầu Loại hình + Lĩnh vực giống HỆT popup /assign/application → thay CheckboxMultiSelect(Loại hình) + CascadeTreeSelect(Lĩnh vực) bằng 1 `CascadePairSelect` (parent Loại hình + child Lĩnh vực, 2 ô cạnh nhau trong col-md-6, mapping cha→con tự lo qua explicitParents). Ứng dụng giữ CheckboxMultiSelect. filters bỏ `customer_scope_group_id`, chỉ còn `application_id` + `customer_scope_pairs`; API gửi `customer_scope_id[]` = child (parent chỉ là helper thu hẹp, KHÔNG lọc Loại hình đơn lẻ — user đồng ý). Cascade với Ứng dụng: `groupPairParentOptions`/`scopePairChildOptions` thu hẹp theo Ứng dụng đã chọn; `applicationFilterOptions` thu hẹp theo Lĩnh vực. VERIFY Playwright: CascadePairSelect render 2 ô + tick cha "Dệt may-giày-dép" → con chỉ hiện lĩnh vực nhóm đó → tick con "Giày dép" → chip "Cha:Con" + network `customer_scope_id[]=72`; 0 lỗi console. Giữ fix `.advanced-filters{overflow:visible}`.

### Checkpoint 3 — 2026-07-14 (Loại hình chọn riêng cũng lọc + label đậm)
User: chọn riêng Loại hình không lọc (bản chất CascadePairSelect: cha chỉ là helper, chỉ emit cặp). Fix (giữ giao diện popup): (1) CascadePairSelect thêm `watch selectedParentIds → $emit('parents-change', ...)` (BỔ SUNG, popup không nghe → không ảnh hưởng); (2) FE index.vue: `@parents-change="onCpsParentsChange"` set `filters.customer_scope_group_id` = groupsAlone (Loại hình chọn RIÊNG, loại các cha đã có con trong pairs); `:key="cpsRemountKey"` bump khi reset để xóa explicitParents nội bộ; initialStateForm + normalize giữ lại customer_scope_group_id array; cascade Ứng dụng thêm nhánh group (hasOtherCatalogFilter + applicationMatchesFilters). (3) BE ProspectiveProjectService::index: customer_scope_id + customer_scope_group_id → OR khi cả 2 (dự án khớp Lĩnh vực HOẶC thuộc Loại hình), else lọc thẳng. (4) In đậm 2 label: page-scoped `::v-deep .cps-label{font-weight:600}` (khớp V2BaseLabel). VERIFY: php -l sạch; API group14(25)∪scope94(23)=25 (OR union); Playwright label weight 600, tick "Điện-điện tử" ĐƠN LẺ → network `customer_scope_group_id[]=8` list lọc theo Loại hình (dự án KANDENKO), reset xóa chip cha, 0 lỗi console.
Bước tiếp: User hard-refresh test thực tế.

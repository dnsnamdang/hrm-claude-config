# Plan — customer-scope-filter

@dnsnamdang · 2026-06-10

Bổ sung bộ lọc Nhóm lĩnh vực KH + Lĩnh vực KH (multi-select searchable, top-down) cho danh sách KH ở **HRM** (`/assign/customers`) và **ERP** (`admin/customers`); HRM thêm filter đầy đủ thực dụng như ERP.

## Quyết định (đã chốt với user)
- 2 trường scope: **multi-select searchable**. Chọn Nhóm → Lĩnh vực chỉ hiện scope thuộc nhóm đã chọn (top-down). Bottom-up auto-fill bỏ qua ở chế độ multi (không hợp lý).
- HRM "đầy đủ thực dụng": thêm Nhóm LVKH + Lĩnh vực KH + Tỉnh/TP + Trạng thái + Khách hãng + Hãng xe + Cấp đại lý + CCCD + Mã KH. Bỏ Công ty/Phòng ban/Nhân viên (HRM đã auto scope theo quyền ERP).
- FE multi-select dùng vue-multiselect (V2BaseSelect không hỗ trợ multiple).

## Phase 1 — HRM BE (Modules/Assign, đọc ERP mysql2)
- [x] BE1: `CustomerService::index` đọc thêm filter: customer_scope_group_id[] (whereIn), customer_scope_id[] (whereIn), province_id, status, is_manufacturer, level_agent, identity_card_number, code, vehicle_manufact_id (qua customer_has_vehicle_manufacts) + helper toIdArray (nhận mảng/chuỗi comma)
- [x] BE2: php -l PASS

## Phase 2 — HRM FE (index.vue)
- [x] FE1: advanced filters: 2 multiselect scope (vue-multiselect, top-down qua filteredScopeOptions) + Tỉnh/TP + Trạng thái + Khách hãng + Hãng xe + Cấp đại lý + CCCD + Mã KH (status/is_manufacturer id chuỗi để tránh bug id=0 của V2BaseSelect)
- [x] FE2: Load options: scope groups/scopes (getAll, scope kèm group_ids), provinces, vehicle-manufacts
- [x] FE3: initialStateForm + loadData (scope join comma vì buildQueryString gộp mảng) + reset clear selected

## Phase 3 — ERP view + BE
- [x] ERP1: `Customer::searchByFilter` đọc customer_scope_group_id[] + customer_scope_id[] (whereIn cột customers)
- [x] ERP2: index.blade.php: 2 search_columns `select-multiple` (framework hỗ trợ sẵn, gửi X[]) + dependent handler top-down (delegated, không sửa class chung Datatable.blade.php)
- [x] ERP3: controller index() inject CustomerScopeReader → truyền $scopeGroups/$scopes; view dùng SCOPE_GROUPS/SCOPES (group_ids)

## Phase 4 — Verify
- [x] V1: php -l BE 2 bên PASS
- [ ] V2: user verify browser cả HRM + ERP

---
## Checkpoint
### Checkpoint — 2026-06-10 (CODE DONE)
Vừa xong: toàn bộ HRM (BE+FE) + ERP (BE+view). php -l PASS cả 2 bên.
- HRM `/assign/customers`: filter đầy đủ thực dụng + 2 scope multiselect top-down.
- ERP `admin/customers`: 2 filter scope multi (select-multiple) + dependent top-down + backend whereIn.
Bước tiếp: user verify browser. FE HRM chưa build được tại đây (node_modules trống). ERP là blade — cần view:clear nếu cache.

### Checkpoint — 2026-06-10 (bổ sung Công ty/Phòng ban/Bộ phận/Nhân viên + ô text Enter-to-search)
- HRM ô input text (Mã/MST/SĐT/CCCD/Tên đơn vị) → vào ignoredFields + @keyup.enter.native=handleSearch (chỉ search khi Enter/bấm Tìm). Select vẫn search ngay.
- HRM thêm bộ lọc Công ty/Phòng ban/Bộ phận/Nhân viên bằng `V2BaseCompanyDepartmentFilter` (khối đầu tiên như ERP), driven theo cấp quyền ERP.
  - BE `ErpPermissionHelper::customerPermissions` + 4 tier flags (is_all_company/is_company/is_department/is_part).
  - BE `CustomerService::index`: applyQuotationOrgFilter (company_id/department_id/part_id/created_by qua 4 bảng báo giá, guard hasColumn) + resolveErpEmployeeIdFromHrm (HRM employee→ERP qua employee_info_id) cho filter Nhân viên.
- php -l PASS. Lưu ý verify: id Công ty/Phòng ban/Bộ phận dùng chung HRM↔ERP (giả định org synced); Nhân viên map qua employee_info_id.

### Checkpoint — 2026-06-10 (khớp CHÍNH XÁC tập trường + thứ tự ERP)
HRM advanced filter chỉnh để đúng y ERP customer list:
- Thứ tự: Công ty → Phòng ban → Nhân viên → Quốc gia → Tỉnh/TP → Mã khách → MST/SĐT → Tên khách → CCCD → Tên đơn vị → Loại hình → Nhóm LVKH → Lĩnh vực KH → Trạng thái → Người sửa gần nhất → Khách hàng hãng → Hãng xe → Cấp đại lý.
- Bỏ "Bộ phận" (ERP customer list không có) → V2BaseCompanyDepartmentFilter :disable_part.
- Gộp MST + SĐT thành 1 ô "MST/SĐT" (BE tìm tax_code OR mobile).
- Thêm "Quốc gia" (nation_id), "Tên khách hàng" (name → fullname), "Người sửa gần nhất" (editor_id → created_by OR updated_by, map HRM→ERP).
- BE CustomerService::index: tax_code combined, +name, +nation_id, +editor_id. php -l PASS.
- Còn giữ quick-search keyword của V2BaseFilterPanel (HRM chuẩn) — không phải field ERP, có thể ẩn nếu user muốn.

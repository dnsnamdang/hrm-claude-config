# Customer Development Report — Plan

Spec: `docs/superpowers/specs/2026-05-18-customer-development-report-design.md`

## Phase 1 — Status history (nền tảng)

### BE

- [x] Migration `create_prospective_project_status_logs` (`id, prospective_project_id, status_from nullable, status_to, changed_at, changed_by nullable, timestamps`, index `(prospective_project_id, changed_at)`)
- [x] Entity `ProspectiveProjectStatusLog` ($guarded=[], cast changed_at datetime)
- [x] Relationship `ProspectiveProject::statusLogs()` (hasMany)
- [x] Model event `created` + `updating` trong `ProspectiveProject` (dùng `booted()` để không xung đột `boot()` của BaseModel)
- [x] Migration backfill: 1 row/PP với `status_from=null, status_to=status, changed_at=created_at, changed_by=created_by` (chunk 1000)
- [x] Helper `ProspectiveProject::statusAt($date)` — log gần nhất ≤ date, fallback `$this->status`

### Checkpoint — 2026-05-18

Vừa hoàn thành: Phase 1 BE — 4 file mới (2 migration + 1 entity + 1 update ProspectiveProject). Syntax pass.
Đang làm dở: Chờ user chạy migration trên môi trường dev.
Bước tiếp theo: User chạy 2 migration → kiểm tra log table có dữ liệu backfill → bắt đầu Phase 2 (BE service + controller + routes).
Blocked: —

## Phase 2 — Backend báo cáo

### BE

- [x] Service `Modules/Assign/Services/Report/CustomerDevelopmentReportService` (getReport / getFilterOptions / getCustomerList)
- [x] Query nhóm A: customers tổ chức created_at∈kỳ, JOIN PP lấy status tại `to` qua subquery log, loại 1/11/12, key (customer_id, main_sale_employee_id) + fallback chua từ users→employees
- [x] Query nhóm B: PP created_at∈kỳ, status tại `to`, loại 1/11/12, unique (customer_id, main_sale_employee_id), max status
- [x] Filter Lĩnh vực/Ngành/Ứng dụng áp cho cả 2 nhóm; chua bị tắt nếu có filter dimension
- [x] Phân quyền cấp 4 mức (tổng cty / cty / phòng ban / cá nhân) áp ở scopeEmployeeIds + applyPermissionFilter
- [x] Build org tree Cty → Phòng ban → NV
- [x] Controller `CustomerDevelopmentReportController` (index/filterOptions/customerList)
- [x] Route group `/assign/report/customer-development` 3 endpoint (filter-options đặt trước route gốc)
- [x] Modal data: enrichCustomerRows trả KH + PP gần nhất + #Meeting + #PP
- [ ] Export Excel `CustomerDevelopmentReportExport` (defer — làm sau khi UI chốt)
- [ ] Bổ sung counters #YCGP / #BG / #HĐ / GT HĐ trong customerList (defer)

### Checkpoint — 2026-05-18

Vừa hoàn thành: Phase 2 BE — Service + Controller + Routes. Syntax pass cả 3 file.
Đang làm dở: Export Excel + counters đầy đủ trong modal (defer cho khi nối FE).
Bước tiếp theo: Phase 3 FE — `/assign/report/customer-development` copy style solution-versions.
Blocked: —

## Phase 3 — Frontend

### FE

- [x] `pages/assign/report/customer-development/index.vue` copy layout từ `solution-versions/index.vue`
- [x] `constants.js`: STAGE_KEYS/STAGE_LABELS/BUCKET_OPTIONS/TIME_MODE_OPTIONS/MONTH_OPTIONS/QUARTER_OPTIONS/GROUP_LABELS
- [x] Filter panel: Thời gian (custom/tháng/quý/năm) + Cấp tổ chức + Nhóm KH + Lĩnh vực/Ngành/Ứng dụng
- [x] Table 3 cấp Cty → PB → NV (2 row header, colspan 6/6, sticky thead)
- [x] Click số → mở modal với params employee_id + group + stage
- [x] `CustomerDevelopmentDetailModal` dùng b-modal: search box + bảng KH + #Meeting + #Dự án TKT + stage pill
- [x] Deep watcher filters auto-search (oldFilters)
- [ ] Cascade scope→industry→application (defer — backend chưa expose pivot data)
- [ ] Nút In báo cáo (defer)
- [ ] Menu route + permission key trong sidebar (cần user xác nhận vị trí)

### Phase 2 — Bug fix sau test

- [x] Fix `customersWithoutPp` — `customers.created_by` map trực tiếp tới `employees.id` (không qua users.employee_info_id)
- [x] Fix `buildOrgTree` + `enrichCustomerRows` — bỏ `ei.phone` (cột không tồn tại)
- [x] Fix `getFilterOptions` — bỏ scope_id/industry_id ở select của Industries/Applications (đã chuyển pivot)

### Checkpoint — 2026-05-18 (E2E test pass)

Test đã chạy với employee_id=41 (Khúc Ngọc Nghĩa), kỳ 2025:

- companies=1, total_employees=1, total_customers=4
- dev: 0/0/4/0/0 (4 KH ở Đang làm GP)
- care: 0
- Click dev/lamgp → trả 4 KH đúng (4 customer rows)
- Filter options OK
  Bước tiếp theo: User test FE qua browser. Lưu ý cần thêm 3 permission "Xem báo cáo phát triển khách hàng theo tổng công ty/công ty/phòng ban" mới thấy được data scope rộng hơn chính mình.

## Phase 4 — Test thủ công

- [ ] Backfill chạy đúng, không miss PP
- [ ] Update status PP qua các flow hiện có → log được ghi đầy đủ
- [ ] Báo cáo kỳ quá khứ (vd 2024) trả đúng status tại ngày cuối kỳ
- [ ] Filter Lĩnh vực/Ngành/Ứng dụng hoạt động đúng 2 nhóm
- [ ] Phân quyền theo cấp: NVKD chỉ xem được dữ liệu trong cấp được phép
- [ ] Modal hiển thị đúng KH/PP theo bucket
- [ ] Xuất Excel đúng định dạng, đủ cột
- [ ] Viết test cases báo cáo QLDA_BC_10 trong Testcase \_baocao.xlsx

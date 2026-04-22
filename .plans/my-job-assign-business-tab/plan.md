# Plan — Tab "Phiếu công tác" trong "Công việc của tôi"

**Owner:** @manhcuong
**Spec:** docs/superpowers/specs/2026-04-20-my-job-assign-business-tab-design.md
**Bắt đầu:** 2026-04-20

## Phase 1 — BE endpoint + service query "của tôi"

- [x] BE Thêm 2 route `/assign/my-job/assign-business-list` (GET) và `/assign/my-job/assign-business-list/export` (GET) vào `Modules/Assign/Routes/api.php` (trong group `/assign/my-job` hiện có)
- [x] BE `MyJobController.php`: thêm method `assignBusinessList(Request $request)` trả `apiGetList(MyJobAssignBusinessResource::apiPaginate(...))`, bọc try/catch + Log::error
- [x] BE `MyJobController.php`: thêm method `exportAssignBusinesses(Request $request)` gọi `Excel::download(new MyJobAssignBusinessExport(...), 'phieu_cong_tac_cua_toi.xls')`
- [x] BE `MyJobService.php`: thêm method `getAssignBusinessList(Request $request)` — query `AssignRequest` type=PHIEU_CONG_TAC, where `created_by = me` OR `whereHas('employees', employee_id=me)`
- [x] BE `getAssignBusinessList`: ẩn nháp của người khác — `status != DANG_TAO` OR `created_by = me`
- [x] BE `getAssignBusinessList`: apply filter `keyword` (LIKE `code`), `business_type`, `status` (hỗ trợ array), `customer_id`, `contract_code`, `from_time`, `to_time`
- [x] BE `getAssignBusinessList`: apply filter `parent_code` — gộp tìm trên `parent_code` + `TpWrAssignTask.code` + `JobRequest.code` qua `assignBusinessTasks`
- [x] BE `getAssignBusinessList`: sort whitelist `['from_time','to_time','updated_at','created_at','code']`, default `updated_at desc`
- [x] BE `getAssignBusinessList`: eager load `leaderEmployee.employee.info`, `assignBusinessTasks`, `employees`

## Phase 2 — BE Resource + Export + Helper link

- [x] BE Tạo `Modules/Assign/Transformers/MyJobAssignBusinessResource/MyJobAssignBusinessResource.php` (list) với các field theo spec section 4.4
- [x] BE Tạo `Modules/Assign/Helpers/AssignBusinessHelper.php` với method static `generateJobInvoiceableLink($code, $id)` port logic từ FE cũ (xử lý `TPE.PGV.`, `TPSG.PGV.`, `PGV`, còn lại là job_request)
- [x] BE Resource: build `job_invoiceable_links` array `[{code, id, type, url}]` từ `assignBusinessTasks` dùng helper link
- [x] BE Resource: expose 11 cờ `can_*` (can_edit, can_approve, can_import_result, can_approve_result, can_create_payment_profile, can_create_payment_business_request, can_extend_time, can_end_soon, can_add_employee, can_add_wr_assign_task, can_delete)
- [x] BE Resource: map `status` → `status_text` và `status_color` theo bảng 9 trạng thái màn cũ
- [x] BE Tạo `app/ExcelExport/MyJobAssignBusinessExport.php` pattern `FromView` + blade template
- [x] BE `exportAssignBusinesses` controller: gọi `getAssignBusinessList` lấy query, `->get()` (không paginate), truyền vào Export class

## Phase 3 — BE smoke test

- [ ] BE Postman/curl test GET `/assign/my-job/assign-business-list` với JWT user đã có phiếu → trả danh sách đúng scope "của tôi"
- [ ] BE Test filter `keyword`, `status=2,3`, `business_type=1`, `parent_code=PGV`, `from_time/to_time`
- [ ] BE Test GET `/assign/my-job/assign-business-list/export` trả file xls đúng định dạng
- [ ] BE Verify `php -l` các file touch không lỗi syntax

## Phase 4 — FE wiring tab mới vào index.vue

- [x] FE `pages/assign/my-job/index.vue`: import `AssignBusinessTab` từ `./components/AssignBusinessTab.vue`
- [x] FE `index.vue`: thêm `{ key: 'assign-business', label: 'Phiếu công tác', icon: 'ri-briefcase-line' }` vào `tabs` giữa `meetings` và `approvals`
- [x] FE `index.vue`: thêm `<AssignBusinessTab v-else-if="activeTab === 'assign-business'" />` trong vùng render tab
- [x] FE `index.vue`: thêm `'assign-business'` vào `validTabs` trong `mounted()` để restore từ query param

## Phase 5 — FE component AssignBusinessTab.vue (khung + filter + table)

- [x] FE Tạo `pages/assign/my-job/components/AssignBusinessTab.vue` — copy khung template + script từ `SolutionsTab.vue` làm base
- [x] FE Định nghĩa `initialStateForm` với 8 field filter: keyword, business_type, status, customer_id, contract_code, parent_code, from_time, to_time + sort_field/sort_dir
- [x] FE Hardcode options `business_types` (2 loại) và `statuses` (6 trạng thái) trong data component
- [x] FE Template `V2BaseFilterPanel`: quick search "Số phiếu", advanced-filters grid 7 ô (V2BaseSelect + V2BaseInput + V2BaseDatePicker + live search khách hàng)
- [x] FE Port pattern live search khách hàng (customerQuery, searchCustomers, selectCustomer, handleClickOutside) từ SolutionsTab
- [x] FE Template `V2BaseDataTable`: 8 cột (STT, codeInfo, jobInvoiceable, customerInfo, leaderInfo, scheduleInfo, status, updated_at-hidden)
- [x] FE Custom cell `codeInfo` dùng `V2BaseTitleSubInfo` + dropdown ⋯ actions
- [x] FE Custom cell `jobInvoiceable` render vòng lặp `job_invoiceable_links`
- [x] FE Custom cell `customerInfo`, `leaderInfo`, `scheduleInfo`, `status` theo spec
- [x] FE Method `loadData`: gọi `apiGetMethod` với url `assign/my-job/assign-business-list${buildQueryString(apiFilters)}`

## Phase 6 — FE column customization + header actions

- [x] FE `getFields`: fetch `human/column-customizations/detail?table=my_job_assign_business`, gán `columnFields`
- [x] FE Computed `allColumns` / `defaultTableColumns` / `tableColumns` pattern giống SolutionsTab
- [x] FE Import `ColumnCustomizationModal` + truyền `:table="'my_job_assign_business'"`
- [x] FE Header action "Tạo mới" → `$router.push('/assign/assign_business/add?from=my-job&tab=assign-business')`
- [x] FE Header action "Xuất Excel": mở `ExportModal` → user chọn cột → submit gọi endpoint export, tải file
- [x] FE Header action "Cấu hình cột" → `$bvModal.show('column-customization-modal-assign-business')`

## Phase 7 — FE row actions (13 actions) + modal tái sử dụng

- [x] FE Render dropdown `⋯` với `b-dropdown` trong cell `codeInfo` — 13 action theo cờ `can_*`
- [x] FE Navigation: Xem, Sửa, Duyệt, Nhập kết quả, Duyệt kết quả, Thêm nhân viên, Thêm phiếu GV → `$router.push` kèm `?from=my-job&tab=assign-business`
- [x] FE Navigation: Lập hồ sơ TT / Lập đề nghị TT với `assign_business_id` query param
- [x] FE Import + mount `ConfirmDeleteSelected`; xóa → set `delete_id` + show modal; handler gọi `apiDeleteMethod` + reload
- [x] FE Import + mount `ConfirmCancelApprove`; từ chối → set `cancelApproveForm` + show modal; handler gọi `apiPutMethod` deny + reload
- [x] FE Gia hạn/Kết thúc sớm: pre-check `assign/extend-end-soon-request/check` → navigate create page nếu OK
- [x] FE Import + mount `ExportModal`; nối với nút Xuất Excel + `fieldsExport`

## Phase 8 — FE polish + style

- [x] FE Import `@/assets/scss/v2-styles.scss` trong `<style lang="scss">` không scoped
- [x] FE Empty state table: "Không có dữ liệu phù hợp bộ lọc."
- [x] FE Loading state dùng `loading` prop của V2BaseDataTable
- [x] FE Toast lỗi API fail: `$toasted?.global?.error?.({ message: 'Lỗi khi tải dữ liệu' })`
- [x] FE Customer dropdown responsive styles (scoped)

### Checkpoint — 2026-04-20
Vừa hoàn thành: Phase 1–2 (BE) + Phase 4–8 (FE) — code DONE
Đang làm dở: —
Bước tiếp theo: User chạy Phase 3 (BE smoke test) + Phase 9 (manual E2E)
Blocked: —

## Phase 9 — Manual test end-to-end

- [ ] QA Login user A có phiếu tạo + phiếu là thành viên → tab hiện đủ 2 nhóm
- [ ] QA Login user B không có phiếu nào → tab hiện empty state
- [ ] QA Filter từng field + kết hợp nhiều filter → data khớp expected
- [ ] QA Click "Tạo mới" → về màn add, sau tạo xong quay lại đúng tab `assign-business`
- [ ] QA Bấm 13 action theo từng kịch bản quyền → navigate/modal/delete/approve/deny đúng
- [ ] QA Xuất Excel → file tải về đầy đủ cột đã chọn, đúng scope "của tôi"
- [ ] QA Cấu hình cột: tắt/bật → save + reload giữ đúng cấu hình
- [ ] QA Phân trang + đổi per_page → meta update đúng

## Phase 10 — Testcase UI end-user

- [ ] Viết testcase UI theo góc nhìn người dùng cuối cho tab mới (định dạng bảng theo mẫu repo) — sau khi feature chạy stable. Lưu vào `docs/testcases/` hoặc thư mục testcase của module Assign theo convention đã có

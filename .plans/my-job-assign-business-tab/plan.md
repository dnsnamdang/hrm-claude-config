# Plan — Tab "Phiếu công tác" trong "Công việc của tôi"

**Owner:** @manhcuong
**Spec:** docs/superpowers/specs/2026-04-20-my-job-assign-business-tab-design.md
**Bắt đầu:** 2026-04-20

## Phase 1 — BE endpoint + service query "của tôi"

- [ ] BE Thêm 2 route `/assign/my-job/assign-business-list` (GET) và `/assign/my-job/assign-business-list/export` (GET) vào `Modules/Assign/Routes/api.php` (trong group `/assign/my-job` hiện có)
- [ ] BE `MyJobController.php`: thêm method `assignBusinessList(Request $request)` trả `apiGetList(MyJobAssignBusinessResource::apiPaginate(...))`, bọc try/catch + Log::error
- [ ] BE `MyJobController.php`: thêm method `exportAssignBusinesses(Request $request)` gọi `Excel::download(new MyJobAssignBusinessExport(...), 'phieu_cong_tac_cua_toi.xls')`
- [ ] BE `MyJobService.php`: thêm method `getAssignBusinessList(Request $request)` — query `AssignRequest` type=PHIEU_CONG_TAC, where `created_by = me` OR `whereHas('employees', employee_id=me)`
- [ ] BE `getAssignBusinessList`: ẩn nháp của người khác — `status != DANG_TAO` OR `created_by = me`
- [ ] BE `getAssignBusinessList`: apply filter `keyword` (LIKE `code`), `business_type`, `status` (hỗ trợ array), `customer_id`, `contract_code`, `from_time`, `to_time`
- [ ] BE `getAssignBusinessList`: apply filter `parent_code` — gộp tìm trên `parent_code` + `TpWrAssignTask.code` + `JobRequest.code` qua `assignBusinessTasks`
- [ ] BE `getAssignBusinessList`: sort whitelist `['from_time','to_time','updated_at','created_at','code']`, default `updated_at desc`
- [ ] BE `getAssignBusinessList`: eager load `leaderEmployee.employee.info`, `assignBusinessTasks`, `employees`

## Phase 2 — BE Resource + Export + Helper link

- [ ] BE Tạo `Modules/Assign/Transformers/MyJobAssignBusinessResource/MyJobAssignBusinessResource.php` (list) với các field theo spec section 4.4
- [ ] BE Tạo `Modules/Assign/Transformers/MyJobAssignBusinessResource/MyJobAssignBusinessDetailResource.php` (dùng khi show chi tiết từ tab nếu cần — nếu không dùng thì skip)
- [ ] BE Tạo `Modules/Assign/Helper/AssignBusinessHelper.php` với method static `generateJobInvoiceableLink($code, $id)` port logic từ FE cũ (xử lý `TPE.PGV.`, `TPSG.PGV.`, `PGV`, còn lại là job_request)
- [ ] BE Resource: build `job_invoiceable_links` array `[{code, id, type, url}]` từ `assignBusinessTasks` dùng helper link
- [ ] BE Resource: expose 11 cờ `can_*` (can_edit, can_approve, can_import_result, can_approve_result, can_create_payment_profile, can_create_payment_business_request, can_extend_time, can_end_soon, can_add_employee, can_add_wr_assign_task, can_delete)
- [ ] BE Nếu logic `can_*` đang rải rác ở Service/Transformer cũ → tách thành accessor `is_can_*` trong model `AssignRequest` để Resource tab mới tái sử dụng. Nếu đã có sẵn thì skip
- [ ] BE Resource: map `status` → `status_text` và `status_color` theo bảng 9 trạng thái màn cũ (1 Đang tạo đỏ, 2 Chờ duyệt vàng, 6 Không duyệt đỏ, 3/5/7/8/9 xanh)
- [ ] BE Tạo `app/ExcelExport/MyJobAssignBusinessExport.php` pattern như `MyJobSolutionExport` — nhận data, map cột theo `fieldsExport` màn cũ (code, business_type_name, jobInvoiceableCode, leader, customer_name, contract_code, created_by, updated_at, status)
- [ ] BE `exportAssignBusinesses` controller: gọi `getAssignBusinessList` lấy query, `->get()` (không paginate), truyền vào Export class

## Phase 3 — BE smoke test

- [ ] BE Postman/curl test GET `/assign/my-job/assign-business-list` với JWT user đã có phiếu → trả danh sách đúng scope "của tôi"
- [ ] BE Test filter `keyword`, `status=2,3`, `business_type=1`, `parent_code=PGV`, `from_time/to_time`
- [ ] BE Test GET `/assign/my-job/assign-business-list/export` trả file xls đúng định dạng
- [ ] BE Verify `php -l` các file touch không lỗi syntax

## Phase 4 — FE wiring tab mới vào index.vue

- [ ] FE `pages/assign/my-job/index.vue`: import `AssignBusinessTab` từ `./components/AssignBusinessTab.vue`
- [ ] FE `index.vue`: thêm `{ key: 'assign-business', label: 'Phiếu công tác', icon: 'ri-briefcase-line' }` vào `tabs` giữa `meetings` và `approvals`
- [ ] FE `index.vue`: thêm `<AssignBusinessTab v-else-if="activeTab === 'assign-business'" />` trong vùng render tab
- [ ] FE `index.vue`: thêm `'assign-business'` vào `validTabs` trong `mounted()` để restore từ query param

## Phase 5 — FE component AssignBusinessTab.vue (khung + filter + table)

- [ ] FE Tạo `pages/assign/my-job/components/AssignBusinessTab.vue` — copy khung template + script từ `SolutionsTab.vue` làm base
- [ ] FE Định nghĩa `initialStateForm` với 8 field filter: keyword, business_type, status, customer_id, contract_code, parent_code, from_time, to_time + sort_field/sort_dir
- [ ] FE Hardcode options `business_types` (2 loại) và `statuses` (6-8 trạng thái) trong data component (hoặc tách sang `pages/assign/my-job/components/constants.js` nếu dùng lại)
- [ ] FE Template `V2BaseFilterPanel`: quick search "Số phiếu", advanced-filters grid 8 ô (V2BaseSelect + V2BaseInput + V2BaseDatePicker + live search khách hàng)
- [ ] FE Port pattern live search khách hàng (customerQuery, searchCustomers, selectCustomer, handleClickOutside) từ SolutionsTab
- [ ] FE Template `V2BaseDataTable`: 8 cột như spec 5.2 (STT, codeInfo, jobInvoiceable, customerInfo, leaderInfo, scheduleInfo, status, updated_at-hidden)
- [ ] FE Custom cell `codeInfo` dùng `V2BaseTitleSubInfo` (title `code`, sub Loại CT + Cập nhật), click → router push `/assign/assign_business/{id}/show?from=my-job&tab=assign-business`
- [ ] FE Custom cell `jobInvoiceable` render vòng lặp `job_invoiceable_links` — mỗi link render `<a :href="item.url" target="_blank">{{ item.code }}</a>`
- [ ] FE Custom cell `customerInfo`, `leaderInfo`, `scheduleInfo`, `status` theo spec
- [ ] FE Method `loadData`: gọi `apiGetMethod` với url `assign/my-job/assign-business-list${buildQueryString(apiFilters)}`, gán `tableData` + map `pagination` meta

## Phase 6 — FE column customization + header actions

- [ ] FE `getFields`: fetch `human/column-customizations/detail?table=my_job_assign_business`, gán `columnFields`
- [ ] FE Computed `allColumns` / `defaultTableColumns` / `tableColumns` pattern giống SolutionsTab
- [ ] FE Import `ColumnCustomizationModal` + truyền `:table="'my_job_assign_business'"`
- [ ] FE Header action "Tạo mới" → `$router.push('/assign/assign_business/add?from=my-job&tab=assign-business')`
- [ ] FE Header action "Xuất Excel": giữ flow mở `ExportModal` → user chọn cột → submit gọi endpoint export với params, tải file. Copy `fieldsExport` từ màn cũ
- [ ] FE Header action "Cấu hình cột" → `$bvModal.show('column-customization-modal')`

## Phase 7 — FE row actions (13 actions) + modal tái sử dụng

- [ ] FE Method `getRowActions(item)`: build mảng 13 action, mỗi action check cờ `can_*` tương ứng từ item (action "Xem" luôn có)
- [ ] FE Render dropdown `⋯` (gear) với `b-dropdown` hoặc component tương đương — mỗi item render theo `getRowActions`
- [ ] FE Method `handleRowAction({action, item})`: switch 13 case
- [ ] FE Navigation: Xem, Sửa, Duyệt, Nhập kết quả, Duyệt kết quả, Thêm nhân viên, Thêm phiếu giao việc → `$router.push` kèm `?from=my-job&tab=assign-business`
- [ ] FE Navigation: Lập hồ sơ TT / Lập đề nghị TT → `/assign/payment_profile/create?assign_business_id={id}` / `/assign/payment_business_request/create?assign_business_id={id}`
- [ ] FE Import + mount `ConfirmDeleteSelected` modal; xóa → set `delete_id` + show modal; handler event gọi `apiDeleteMethod` `assign/assign_business/{id}` + reload
- [ ] FE Import + mount `ConfirmCancelApprove` modal; từ chối → set `form.id` + show modal; handler gọi store dispatch `denyApproveAssignBusiness`
- [ ] FE Import + mount `ExtendTimeModal`; gia hạn → pre-check `assign/extend-end-soon-request/check?type=1` → navigate create page nếu OK
- [ ] FE Import + mount `EndSoonModal`; kết thúc sớm → pre-check `type=2` → navigate create page nếu OK
- [ ] FE Import + mount `ExportModal` từ `@/components/modal/export-modal.vue`; nối với nút Xuất Excel

## Phase 8 — FE polish + style

- [ ] FE Import `@/assets/scss/v2-styles.scss` trong `<style lang="scss">` không scoped để V2Base components style đúng
- [ ] FE Kiểm tra responsive: filter grid wrap 1-2 cột trên mobile, dropdown action không tràn
- [ ] FE Empty state table: "Không có phiếu công tác nào phù hợp bộ lọc."
- [ ] FE Loading state dùng `loading` prop của V2BaseDataTable
- [ ] FE Toast lỗi API fail: `$toasted?.global?.error?.({ message: 'Lỗi khi tải dữ liệu' })`

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

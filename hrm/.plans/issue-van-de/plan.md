# Plan — Vấn đề (Issue) #11290

## Phase 1 — Đổi tên Issue → Vấn đề + Bước 1 (Bộ phận xử lý)

### BE (hrm-api, nhánh tpe)
- [x] Migration `add_handling_org_to_issues_table`: thêm `handling_department_id`, `handling_part_id` (nullable + index) — `project_id`/`solution_id` đã nullable sẵn ở DB nên không cần đổi schema
- [x] `Issue.php`: bổ sung 2 field vào `$fillable`, quan hệ `handlingDepartment()` / `handlingPart()`, accessor `scope_text`
- [x] `IssueStoreRequest` / `IssueUpdateRequest`: bỏ `required` của `project_id`/`solution_id`, `module_id` chỉ required khi có solution, thêm rule phải có ít nhất 1 trong `assignee_id` / `handling_department_id`
- [x] `IssueService::store()`: giữ `assignee_id = null` khi chỉ chọn bộ phận, bắn thông báo cho Trưởng bộ phận
- [x] `IssueService::update()`: bắn thông báo khi đổi bộ phận xử lý
- [x] `IssueService::syncIssueOrgUnits()`: thêm org của phòng ban/bộ phận xử lý
- [x] `IssueService::index()`: nhận filter `handling_department_id`, `handling_part_id`
- [x] `IssueResource` + `DetailIssueResource`: trả `handling_department_id/_name`, `handling_part_id/_name`, `scope_text`
- [x] `PermissionsTableSeeder`: đổi `display_name` + `group` của 4 quyền id 1099-1102 sang "Vấn đề" (giữ `name`)
- [x] Đổi nội dung 2 thông báo trong `IssueService` theo `notification-convention`

### FE (hrm-client, nhánh tpe)
- [x] `components/menu-sidebar.js`: menu `Issue` → `Vấn đề`
- [x] `pages/assign/issues/index.vue`: đổi nhãn, thêm cột Bộ phận xử lý, thêm 2 ô lọc
- [x] `pages/assign/issues/components/CreateIssueModal.vue`: đổi nhãn, thêm khối Bộ phận xử lý, bỏ bắt buộc Dự án/Giải pháp, sửa validate
- [x] `pages/assign/issues/components/IssueHistoryModal.vue`: đổi nhãn
- [x] `pages/assign/my-job/components/IssuesTab.vue`: đổi nhãn
- [x] `pages/assign/solutions/_id/manager.vue` + `components/manager/*`: tab `Issue` → `Vấn đề giải pháp`
- [x] `pages/assign/solution-modules/_id/manager.vue` + `components/IssueTab.vue`: tab → `Vấn đề hạng mục`
- [x] `pages/assign/prospective-projects/_id/manager.vue`: tab `Issue` → `Vấn đề giải pháp`
- [x] `pages/assign/handover/*` + `HandoverItemsTable.vue`: đổi nhãn
- [x] `pages/assign/settings/index.vue` + `DeadlineConfigHistoryModal.vue`: đổi nhãn cảnh báo sớm

## Phase 2 — Nút "Giao nhiệm vụ" ở chi tiết Vấn đề
- [ ] (chưa bắt đầu)

## Phase 3 — Báo cáo kết quả xử lý
- [ ] (chưa bắt đầu)

## Phase 4 — Tab "Vấn đề" riêng của Dự án
- [ ] (chưa bắt đầu)

## Phase 5 — Icon "Giao Vấn đề" ở Biên bản họp
- [ ] (chưa bắt đầu)

---

### Checkpoint — 2026-09-12
Vừa hoàn thành: **PHASE 1 CODE XONG** (BE + FE), đã chạy migration trên DB dev và test tạo Vấn đề
chỉ chọn phòng ban → `assignee_id` NULL, `issue_org_units` có hàng phòng ban, thông báo
`[ISSUE] Tạo mới: <b>…</b>. Giao xử lý cho PHÒNG THIẾT BỊ Ô TÔ 2.` gửi đúng `employee_info_id = 24`
(Trưởng phòng ban 5). Đã dọn dữ liệu test.
Đang làm dở: không có.
Bước tiếp theo: user kiểm thử trên giao diện (:3005) — tạo Vấn đề phòng ban, lọc theo Bộ phận xử lý,
xem cột mới ở danh sách. Sau đó làm Phase 2 (nút "Giao nhiệm vụ").
Blocked: không có.

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

- [x] 23/11/2026 — (chưa có số Redmine) — @cuong61n — Vấn đề có Người duyệt đóng mà màn người phụ trách vẫn hiện nút "Đóng vấn đề".
  Nghiệp vụ: đã chọn người duyệt thì người phụ trách không được tự đóng (bỏ qua bước duyệt). Người tạo vẫn đóng được; người duyệt không đổi.
  Kỹ thuật: `hrm-api` `Modules/Assign/Entities/Issue.php::nextStatusTransitions()` — `$canClose = $isCreator || ($isAssignee && !$this->hasApprover())`. BE chặn luôn cả API (`transitionTo`); FE web và app TPE_APP chỉ đọc `allowed_next_statuses` nên không phải sửa.
  Đã kiểm: thêm test `test_co_nguoi_duyet_thi_nguoi_phu_trach_khong_dong_duoc_nguoi_tao_van_dong` (IssueUnitAssignTest) đạt; sửa 3 test cũ trong IssueV2ApiTest đang mã hoá luật cũ (requires_cho_tung_buoc, dong_va_mo_lai_bao…, dong_van_de_tu_huy_de_nghi_cho) sang người tạo đóng. Chạy cả thư mục Tests/Feature/Issue: danh sách lỗi y hệt bản chưa sửa (~30 test lỗi có sẵn từ trước, không liên quan).
  Trạng thái: đã sửa trên worktree gop_db-api, chưa commit, chưa test trên giao diện.
- [x] 23/11/2026 — Bổ sung luật đóng: người duyệt cũng đóng được (lý do bắt buộc). Luật cuối: người tạo + người duyệt đóng được; người phụ trách chỉ đóng khi vấn đề KHÔNG có người duyệt.
  `Issue.php::nextStatusTransitions()`: `$canClose = $isCreator || $this->isApprover() || ($isAssignee && !$this->hasApprover())`. Test `test_co_nguoi_duyet_thi_nguoi_phu_trach_khong_dong_duoc_nguoi_tao_van_dong` mở rộng: người duyệt đóng được ở Đã phân công / Đang xử lý / Từ chối, thiếu lý do → 422; vấn đề không có người duyệt thì người phụ trách đóng được, người lạ không. Đạt; cả thư mục Tests/Feature/Issue giữ nguyên danh sách lỗi có sẵn. Chưa commit, chưa test giao diện.
- [x] 23/11/2026 — Đã đẩy `gop_db` (API `8e46b012d`, client `7de588616`) và deploy PROD bằng `~/build_tpe.sh`: exit 0, "Nothing to migrate", FE build xong, pm2 online, trang đăng nhập trả 200. Chưa test giao diện trên prod.

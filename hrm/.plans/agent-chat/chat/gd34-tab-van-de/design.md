# GĐ34 — Tab Vấn đề trong Nhóm trao đổi

> Tạo 17/11/2026. Phase 3 của `.plans/gop-db/phan-he-cong-viec/van-de-v2/` (design §6) — nền Vấn đề v2 đã xong
> (hrm-api / hrm-client nhánh `gop_db-van-de-v2`, chưa push). Code GĐ34 làm TIẾP trên cùng nhánh (Vấn đề v2 chưa lên gop_db).

## 1. Mục đích
Thành viên nhóm theo dõi + ghi vấn đề phát sinh ngay trong nhóm, cạnh tab Nhiệm vụ / Meeting — đồng bộ cách xem
và thao tác với tab Nhiệm vụ (danh sách gom nhóm, bấm dòng mở panel).

## 2. Đã chốt (user, lượt trước — design van-de-v2 §6)
- Nhóm thường + nhóm GP có tab Vấn đề; bật/tắt ở form tạo nhóm + Cấu hình → Tab sử dụng. **Nhóm TKT không có** (GĐ12 Q5).
- Nhóm thường: hiện vấn đề TẠO TỪ NHÓM ⇒ cột `issues.workspace_id` (nullable + index). Nhóm GP: hiện MỌI vấn đề của GP
  (như tab Nhiệm vụ nhóm KH — GĐ12 Q11).
- Bấm dòng ⇒ `IssuePanel`; "+ Vấn đề" ⇒ panel tạo điền sẵn nhóm (và GP nếu nhóm GP).
- Xem / tạo: mọi Quản lý + Thành viên nhóm (kể cả khác công ty); sửa / xử lý theo cờ Vấn đề v2.
- Ngoài phạm vi: tin hệ thống trạng thái vấn đề vào nhóm, tự nạp tab realtime, tạo vấn đề từ tin nhắn.

## 3. Claude tự chốt (bám tab Nhiệm vụ nhóm — `WorkspaceTaskRules`, `WorkspaceTaskListService`, `TaskGroupListView`)
- C1. **Luật gắn nhóm** (`WorkspaceIssueRules`, khuôn `WorkspaceTaskRules`): nhóm đóng ⇒ 423; người tạo phải là Quản lý /
  Thành viên; nhóm bật tab Vấn đề; nhóm thường ⇒ vấn đề **không** đồng thời gắn GP / Dự án (như MSG_EXCLUSIVE của nhiệm vụ);
  nhóm GP ⇒ `solution_id` = GP của nhóm (khoá, như nhóm KH). Tắt tab chỉ chặn tạo MỚI.
- C2. **Xem**: `IssueAccess::canView` thêm (c) thành viên (mọi vai trò) của nhóm có `workspace_id` = vấn đề, (c') thành viên
  nhóm GP có `solution_id` trùng. `assertWritable` 423 khi nhóm thường đã đóng (nhóm KH đóng không khoá — như TaskAccess).
- C3. **Danh sách**: API `GET assign/workspaces/{id}/issues` khuôn `WorkspaceTaskListService` — gom theo **Trạng thái /
  Người xử lý / Hạn** (bỏ "Dự án": trong 1 nhóm cùng 1 dự án), Lọc nhanh **Tất cả / Của tôi / Quá hạn / Chờ tôi duyệt đóng**,
  tìm theo mã + tiêu đề, "Xem thêm" theo nhóm. **Chỉ dạng Danh sách gom nhóm** — không làm dạng Bảng + Cấu hình cột ở đợt
  này (gọn; thêm sau nếu cần).
- C4. FE: `components/assign/issue/group-list/IssueGroupListView.vue` (+ dòng / khối nhóm riêng — component group-list của
  Nhiệm vụ gắn chặt dữ liệu task) dùng lại `TaskGroupToolbar` nếu tách được tham số, không thì copy khuôn; tab `issues` ở
  `WorkspaceView` + `WorkspaceTopicTabs` (`?panel=issues`), số đếm trên nút như tab Nhiệm vụ; ô tick Vấn đề ở
  `CreateWorkspaceModal` + `SettingsPanel` (ẩn với nhóm TKT); bỏ chặn `issues` cho nhóm GP ở 2 Request.
- C5. Panel / form: thêm ô **Nhóm** chỉ đọc khi tạo từ nhóm (dòng crumb "Nhóm: <tên>"); `IssueStoreRequest` nhận
  `workspace_id`.

## 4. Câu hỏi còn mở (user)
- Q1 (CHỐT 17/11): vấn đề tạo trong nhóm **được giao cho người / phòng ban ngoài nhóm, không giới hạn** (như tạo ở
  /assign/issues). Người ngoài xử lý được qua vai trò trên vấn đề nhưng không mở tab nhóm.

## 5. Ảnh hưởng
- Migration `2026_11_24_000001_add_workspace_id_to_issues_table` (nullable + index) — chạy `db_gop_6_11` khi user cho phép.
- `IssueAccess`, `IssueStoreRequest`, `IssueService::store`, Workspace Requests, `WorkspaceView`, `CreateWorkspaceModal`,
  `SettingsPanel`, `IssuePanel/IssueForm` (ô Nhóm). Test: PHPUnit Workspace + Issue; e2e `workspace-issues.spec.ts` mới +
  chạy lại `workspace-tasks`, `chat-core`, `workspace-kh-project`, `issue-panel-v2`.

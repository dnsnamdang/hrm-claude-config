# GĐ34 — Tab Vấn đề trong Nhóm trao đổi — Plan

> Design: `design.md` (cùng thư mục). Code tiếp trên nhánh `gop_db-van-de-v2` (hrm-api + hrm-client, wt-nhom-trao-doi).
> Khuôn: `WorkspaceTaskRules`, `WorkspaceTaskListService` + `WorkspaceTaskController`, `TaskGroupListView`, `TaskAccess` (c)(c').

## Task A — BE (hrm-api)
- [x] Migration `2026_11_24_000001_add_workspace_id_to_issues_table` (`workspace_id` unsignedBigInteger nullable + index) — chạy `db_gop_6_11` bằng `--path --force` sau khi user xem `--pretend`.
- [x] `Issue`: `workspace_id` fillable + quan hệ `workspace()`.
- [x] `WorkspaceIssueRules::validateAttach(?int $workspaceId, int $actorId, ?int $solutionId, ?int $projectId)` (C1; KHÔNG xét người phụ trách — Q1) — gọi trong `IssueService::store`; `IssueStoreRequest` nhận `workspace_id`.
- [x] `IssueAccess::canView` thêm (c) thành viên nhóm `workspace_id`, (c') thành viên nhóm GP trùng `solution_id`; `assertWritable` 423 nhóm thường đã đóng.
- [x] `WorkspaceIssueListService::list(Workspace, int $me, array $f)` + `GET assign/workspaces/{id}/issues` (C3: gom status/assignee/due, quick all/mine/overdue/waiting_my_close, q, group+page "Xem thêm"; ≤ 4 truy vấn/lượt, không N+1).
- [x] Workspace Store/UpdateRequest: bỏ chặn `issues` cho nhóm GP, giữ chặn TKT; chi tiết nhóm trả số vấn đề cho nút tab.
- [x] PHPUnit: `Tests/Feature/Workspace/WorkspaceIssueListTest.php` (thành viên thấy, người ngoài 403, nhóm GP thấy mọi vấn đề GP, nhóm đóng 423 khi tạo, tab tắt chặn tạo mới, TKT không bật được issues, đếm truy vấn không tăng theo số dòng).

## Task B — FE (hrm-client)
- [x] `components/assign/issue/group-list/IssueGroupListView.vue` (+ khối nhóm / dòng) theo C3/C4.
- [x] `WorkspaceView` + `WorkspaceTopicTabs`: tab `issues` (`?panel=issues`), số đếm; mở panel / "+ Vấn đề" ⇒ `IssuePanel.create({workspace_id, solution_id?, lock…})`; lưu ⇒ nạp lại danh sách + số đếm.
- [x] `CreateWorkspaceModal` + `SettingsPanel`: ô tick Vấn đề (ẩn nhóm TKT).
- [x] `IssueForm` / `IssuePanel`: dòng "Nhóm: <tên>" khi có `workspace_id`; gửi `workspace_id`.
- [x] Kiểm Playwright :3080 (đo DOM) — cả ngăn trượt Chat (ChatDrawer) lẫn trang nhóm.

## Task C — e2e
- [x] `HRM/e2e/tests/chat/workspace-issues.spec.ts` (API tạm như issue-panel-v2 — không push) + chạy lại workspace-tasks, chat-core, workspace-kh-project, issue-panel-v2.

### Checkpoint — 17/11/2026
Vừa hoàn thành: design (Q1 chốt) + plan.
Bước tiếp theo: hỏi user phạm vi code (2 repo nhánh gop_db-van-de-v2, migration 2026_11_24_000001).
Blocked: chưa có lệnh code.

### Checkpoint — 17/11/2026 (GĐ34 xong)
Vừa hoàn thành: Task A/B/C + fix sau soát — hrm-api `394e216e4..1492359b4` (migration 2026_11_24_000001 đã chạy db_gop_6_11; WorkspaceIssueRules, WorkspaceIssueListService + GET workspaces/{id}/issues, IssueAccess (d)(d') + isLocked, WorkspaceIssueCanceller — đóng nhóm thường ⇒ vấn đề mở tự "Đã đóng" (user chốt cách 1, khớp §3.11), closable_issue_count, chặn module_id nhóm thường, destroy 423) · hrm-client `d13eabaa0..1bc6899f6` (IssueGroupListView, tab issues, ô tick Vấn đề, dòng Nhóm trong form, popup Đóng nhóm báo số vấn đề). Cả 2 nhánh gop_db-van-de-v2 CHƯA push. Test: Issue 65, Workspace 290 (controller chạy lại), e2e workspace-issues 8/8 + workspace-tasks 12 + chat-core 8 + workspace-kh-project 7 + issue-panel-v2 11.
Quyết định khi chạy: is_locked 1 nguồn (nhóm KH đóng không khoá) · closeAll cả ở tự lưu trữ (promoteWhenManagersLeft), lịch sử ghi "Hệ thống" · thông báo đóng gộp 1/người sau commit (khuôn task canceller) · chỉ dạng danh sách gom nhóm (không Bảng).
Index `issues.solution_id`: XONG 17/11 (user cho phép + "chạy") — migration 2026_11_24_000002 đã chạy db_gop_6_11, EXPLAIN type=ref key=issues_solution_id_index, commit api sau 1492359b4.
Bình luận vấn đề nhóm đã đóng: user chốt 18/11 KHÔNG khoá. Còn chờ user: local không có nhóm GP/TKT thật (kiểm bằng dữ liệu giả + PHPUnit).
Ngoài luồng: chat-core.spec không dọn nhóm `[e2e] Nhóm chat` (56 nhóm tồn).

### Checkpoint — 17/11/2026 khuya (ĐÃ DEPLOY TPE)
prod api `5eba99ce1` · client `21a383016` (build_tpe EXIT 0, 3 migration 2026_11_23_000001 / 2026_11_24_000001 / 2026_11_24_000002 chạy xong, site 200).

- 18/11 — Hạng mục phải thuộc đúng GP: trait `Http/Requests/Issue/Concerns/ValidatesIssueModule` gắn vào IssueStore/Update/FieldUpdate Request (422 `module_id` "Hạng mục không thuộc giải pháp đã chọn."; PUT không gửi solution_id ⇒ xét GP đang lưu). PHPUnit IssueV2ApiTest 67 OK · WorkspaceIssueListTest 23 OK (sửa ca test_nhom_thuong_chan_module_id gửi kèm GP). Chưa commit.
- 18/11 — Mở rộng sang Nhiệm vụ (user "làm"): trait chuyển về `Http/Requests/Concerns/ValidatesSolutionModule` (dùng chung), gắn TaskStore/TaskUpdate/TaskFieldUpdate Request (`solution_module_id`; PUT + PATCH link không gửi solution_id ⇒ xét GP đang lưu). PHPUnit: Issue 67 · Task 34 · Workspace 290 (cần `-d memory_limit=2G`) đều OK. Prod 18/11 (đọc): 0 vấn đề gắn hạng mục, 2 nhiệm vụ gắn hạng mục đều đúng GP. Commit `ecfbf119e`, merge gop_db `52b93ae17`, ĐÃ DEPLOY TPE 18/11 (api `52b93ae17`, client không đổi `883eaed3c`, không migration, site 200). Ngoài phạm vi: nhiệm vụ sinh từ Meeting (`MeetingService`) lấy hạng mục từ liên kết meeting.

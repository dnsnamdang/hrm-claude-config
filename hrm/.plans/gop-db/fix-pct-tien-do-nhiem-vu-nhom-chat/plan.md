# Fix % tiến độ nhiệm vụ trong nhóm chat hiện 0% (chưa có số Redmine) — @cuong61n

## Phase 1 — Sửa hiển thị % hoàn thành
- [x] 21/11/2026 · Điều tra: danh sách nhiệm vụ nhóm chat đọc cột `tasks.progress_pct` (chỉ đồng bộ từ log báo cáo định kỳ), còn ô "Tiến độ" lúc nộp kết quả ghi vào `tasks.progress_percent` ⇒ việc nộp kết quả không có báo cáo định kỳ hiện 0% dù đã nhập (vd task 979: percent=100, pct=0). Màn Kết quả (`TaskResultTab.latestPct`) đọc cả 2 nguồn nên không lệch.
- [x] 21/11/2026 · BE: thêm `Task::displayProgressPct()` (pct>0 thì lấy pct, không thì lấy progress_percent); dùng ở `WorkspaceTaskItemResource` + `ChatPresenter` (thẻ nhiệm vụ trong chat); sắp xếp cột tiến độ ở `WorkspaceTaskListService` dùng cùng công thức.
- [x] 21/11/2026 · Kiểm Playwright local :3002 (nhánh gop_db): tạm gắn task 979/17/1 vào nhóm test 71 → trước sửa 0%, sau sửa 100% / 40% / 100% đúng; đã trả workspace_id về NULL. Chưa chạy bộ test PHPUnit Workspace.
- Trạng thái: sửa xong ở worktree gop_db-api, chưa commit/push.

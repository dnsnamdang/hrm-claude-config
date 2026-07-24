# Plan — Tab File đa nguồn (màn Quản lý dự án)

Phụ trách: @namdangit

## Phase 1 — Bổ sung nguồn "File kết quả thực hiện Task" vào tab File

Bug: Tab File (`/assign/solutions/{id}/manager`) chỉ lấy file từ bảng `files`
(source task/issue/HSTD GP/HSTD HM), KHÔNG lấy file kết quả thực hiện task
(lưu ở bảng riêng `task_result_attachments`). Quyết định: gộp vào nguồn **Task**.

### BE
- [x] `SolutionService::getFileListForSolution` — thêm sub-query UNION thứ 5 từ `task_result_attachments` JOIN `tasks` (theo `task_id`, `tasks.solution_id`), gán `source='task'`, map NULL cho các cột không có (created_by, attachment_type_id, attachment_type_name, status)
- [x] Xử lý filter cho sub-query mới: keyword (name/file_name/tasks.code/title/module), solution_module_id, version; bỏ qua sub-query khi filter attachment_type_id / status đang bật (bảng không có các cột này)
- [x] Người tạo file kết quả = `tasks.assignee_id` (người thực hiện/nộp kết quả) → cột "Người tạo" hiện tên; filter "Người tạo" lọc theo assignee_id

### FE
- [x] Không đổi — file kết quả hiện chung badge "Task" (đã có sẵn source='task', download bằng `file_path`)

### Verify (tinker, solution local có task result attachment)
- [x] Task có file kết quả thực hiện → hiện trong tab File với source=task, linked_code đúng, file_path = URL S3 đầy đủ
- [x] Lọc theo loại tài liệu → file kết quả bị loại đúng; lọc nguồn=Issue → không lọt vào

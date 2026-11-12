# Nhiệm vụ chung không chọn được nhiều người thực hiện (chưa có số Redmine) — @cuong61n

Nhánh `gop_db` · phản hồi từ chị Nguyễn Thị Thu Huyền (TPE).

- [x] 12/11/2026 — Điều tra: tạo nhiệm vụ chung ở form TaskPanel vẫn chỉ chọn được 1 người (ô có nút ×, không ra chip).
  Tái hiện trên local: chọn "Nhiệm vụ chung" nhưng ô vẫn là ô chọn 1 người. BE `TaskService::store` đã hỗ trợ `assignee_ids` (mỗi người 1 nhiệm vụ riêng, chung `batch_id`) nên không phải lỗi BE.
- [x] 12/11/2026 — Nguyên nhân: `components/assign/task/panel/TaskForm.vue` có 2 `V2BaseSelect` ở `v-if`/`v-else` không có `key` → Vue dùng lại instance, select2 chỉ đọc `multiple` lúc khởi tạo nên giữ nguyên kiểu chọn 1. Sửa: thêm `key="assignee-multi"` / `key="assignee-single"`.
- [x] 12/11/2026 — Test lại trên bản gop_db (client :3002, API :8003, DB local_hrm_erp) bằng Playwright:
  đổi qua lại Cụ thể ↔ Chung 2 vòng, ô đổi đúng kiểu (chung = chọn nhiều + hint, cụ thể = chọn 1); chung chọn 2 người → Giao việc → 2 nhiệm vụ (id 1056/1057) cùng `batch_id`, `task_type=1`;
  cụ thể chọn 1 người → 1 nhiệm vụ (id 1058, `task_type=2`, `batch_id` NULL); bỏ trống bấm Giao việc → báo "Bắt buộc phải nhập" ở các ô bắt buộc (BE 422).
- [x] 12/11/2026 — Cột Tag ở `/assign/tasks` hiện `[]` khi không có tag: slot `#cell-tags` chỉ ra comment nên `V2BaseDataTable` quay về render mặc định `{{ [] }}`. Sửa: thêm `<span v-else></span>` trong `pages/assign/tasks/index.vue`. Đã kiểm: 9/10 dòng không tag để trống, dòng có tag vẫn hiện chip.
- Trạng thái: đã sửa trên worktree gop_db-client (TaskForm.vue, pages/assign/tasks/index.vue), chưa commit. Chờ user xem.

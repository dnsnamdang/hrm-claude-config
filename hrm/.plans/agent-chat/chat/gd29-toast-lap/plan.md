# GĐ29 — TaskPanel / popup Vấn đề: lỗi 403/500 hiện 2 thông báo

User 17/11/2026 "làm tất cả" (mục 3 việc chờ). Nhánh client `gop_db-fix-toast-lap` (wt-nhom-trao-doi, từ origin/gop_db 12a065598). Chỉ client.
Bản sửa lấy từ worktree `wt-quyen-xem-task` (đợt vá quyền đọc #6/#17, chưa commit — phần FE độc lập với BE).

- [x] `utils/apiErrorToasted.js` (chép nguyên) — lỗi đã được plugins/axios.js báo chưa (401/403/428/500/504/mất mạng; X-Silent-Errors ⇒ chưa).
- [x] `TaskPanel.fetchDetail` + `CreateIssueModal` tải chi tiết: chỉ tự báo khi bộ chặn chưa báo; popup Vấn đề đóng khi lỗi.
- [x] `toastedByAxios` (utils/assign/workspaceTaskApi.js, GĐ2) gọi lại `apiErrorToasted` — 1 nguồn danh sách mã.
- [x] e2e task-panel-v2 ca 7 (403/500 ⇒ 1 thông báo, 404 câu riêng) PASS (trước sửa đỏ — ghi ở gd22 plan). Không chạy cả bộ: các ca khác giao việc thật cho NV 50 (push thật).
- [x] e2e workspace-tasks (dùng toastedByAxios) — xem kết quả trong STATUS.
- [x] 17/11 commit client `9ed6c1557` ⇒ gop_db ⇒ ĐÃ DEPLOY TPE (client 848e8d4eb). Khi đợt vá quyền đọc merge: bỏ phần FE trùng ở wt-quyen-xem-task (cùng nội dung ⇒ git tự gộp).

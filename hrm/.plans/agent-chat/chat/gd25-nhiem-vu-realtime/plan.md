# GĐ25 — Đổi nhiệm vụ ⇒ chat + panel Tài nguyên tự cập nhật (không tải lại trình duyệt)

User 16/11/2026: "Khi đổi trạng thái nhiệm vụ, đang cần phải load lại trình duyệt thì màn hình chat và panel tài nguyên mới cập nhật ⇒ sửa để update tự động".
Nhánh `gop_db-chat-nhiem-vu-realtime` (api từ c284cdfe5, client từ 41bc5eb0f).

Tái hiện (Playwright, script scratch taskrt.mjs): thẻ nhiệm vụ trong tin KHÔNG bao giờ đổi; panel chỉ đổi khi có tin hệ thống GĐ23
(mốc chính) — đổi sang "Từ chối triển khai" thì panel cũng đứng. Gốc: nhiệm vụ đổi thì BE không phát gì cho hội thoại nhóm.

- [x] api `Services/Chat/TaskChatSync`: `Task::booted` → `static::updated` ⇒ trường hiện trên thẻ đổi (status, title, assignee_id, due_date,
      due_time, progress_pct, workspace_id) + việc thuộc nhóm ⇒ gom theo việc, sau commit phát `ChatActivity('task.updated', conv,
      {task_id, card})` tới thành viên hội thoại nhóm (nhóm cũ khi chuyển nhóm ⇒ card moved). Bắt MỌI đường ghi. Lỗi chỉ log.
- [x] api `ChatPresenter::taskCardFor()` — cùng dữ liệu thẻ trong tin.
- [x] client `ChatPane.onTaskUpdated`: vá `card` của mọi tin cùng task_id; `ChatSidePanel.loadTasksSoon()` (gom 800ms, panel thu gọn ⇒ bỏ).
- [x] Đo lại script: Đang thực hiện / Từ chối triển khai ⇒ thẻ + panel đổi trong 5s.
- [x] PHPUnit `Workspace/TaskChatRealtimeTest` 3/3 (1 gói sau commit kèm thẻ, gom nhiều save; trường khác / việc ngoài nhóm không phát;
      chuyển nhóm ⇒ 2 nhóm, nhóm cũ moved). Workspace 241/241 · --filter Task 117/117 · Agent 279/282 (3 lỗi sort_order cũ).
- [x] e2e `chat-task-status.spec.ts` +T3 (NV 24 đang mở nhóm: NV 13 đổi Tạm dừng / Từ chối triển khai ⇒ thẻ + panel tự đổi, 0 lần tải lại): 3/3.
      Chat drawer 10 · core 8 · giao-dien 5 · bo-sung 6 · workspace-tasks 12 xanh.
- [x] 16/11 commit api 5db19c28b · client fe3ff8755, gop_db fast-forward, push 2 nhánh. ĐÃ DEPLOY TPE (EXIT 0, Nothing to migrate, site 200).

Ngoài phạm vi (chưa làm): tab Nhiệm vụ của nhóm (danh sách) chưa tự nạp lại theo task.updated; nhãn "quá hạn" đổi theo thời gian (không có sự kiện).

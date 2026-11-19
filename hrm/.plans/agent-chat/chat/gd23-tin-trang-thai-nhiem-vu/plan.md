# GĐ23 — Nhiệm vụ trong nhóm đổi trạng thái ⇒ tin hệ thống vào chat nhóm

User 16/11/2026: "Khi các Nhiệm vụ trong nhóm đổi trạng thái ⇒ cần gửi thông báo hệ thống vào nhóm tương ứng" — "làm" (không chọn danh sách
trạng thái ⇒ theo đề xuất 2 "mốc chính"). Nhánh `gop_db-chat-tin-trang-thai-nhiem-vu` (api từ 879511857, client từ 509532964).

Khuôn: như tin lịch họp GĐ9 (WorkspaceActivity ⇒ SyncWorkspaceChat ⇒ MessageService::system, meta bấm được). Tin hệ thống không push điện thoại.

- [x] api `Task::WORKSPACE_ANNOUNCE_STATUSES` = Đang thực hiện (bắt đầu / tiếp tục), Chờ duyệt kết quả, Hoàn thành, Bị từ chối kết quả,
      Tạm dừng, Huỷ — muốn thêm mốc sửa 1 chỗ.
- [x] api `TaskService::update()` (đường DUY NHẤT đổi trạng thái; updateField / gia hạn không đổi) ⇒ `announceStatusInWorkspace()`:
      có workspace_id, nhóm chưa đóng, trạng thái mới thuộc danh sách ⇒ `WorkspaceActivity('task_status_changed', {task_id, task_code,
      task_title, old_status, new_status, note ≤200})`; lỗi chỉ ghi log, không hỏng lần đổi trạng thái.
- [x] api `SyncWorkspaceChat`: task_status_changed đi đường NGẮN — không syncSpaceMembers, không conversation.updated cho cả nhóm (tin
      thường xuyên, nhóm đông); chưa có hội thoại nhóm ⇒ bỏ. Câu: "<người> đã chuyển nhiệm vụ <mã> – <tên ≤80> sang <trạng thái>
      [— Lý do: … (bị từ chối) | — Ghi chú: …]".
- [x] client `ChatMessageItem.vue`: tin meta.action=task_status_changed ⇒ viên bấm được (emit open-task ⇒ TaskPanel), icon theo trạng
      thái, nền xanh dương / xong xanh lá / từ chối-huỷ xám.
- [x] PHPUnit `Workspace/TaskStatusWorkspaceMessageTest` 3/3; Workspace 238/238; --filter Task 114/114.
- [x] e2e mới `tests/assign/chat-task-status.spec.ts` 2/2 (4 tin đúng thứ tự + ghi chú + màu/ icon đo DOM; bấm ⇒ TaskPanel đúng việc, URL giữ).
      Chat: drawer 10 · core 8 · giao-dien 5 · thong-bao-emoji 10 — xanh hết.
- [x] 16/11 commit api c284cdfe5 · client 34a946f5d, gop_db fast-forward, push 2 nhánh. ĐÃ DEPLOY TPE (EXIT 0, Nothing to migrate, site 200).

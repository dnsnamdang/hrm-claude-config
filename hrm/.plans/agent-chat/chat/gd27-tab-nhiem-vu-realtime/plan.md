# GĐ27 — Tab Nhiệm vụ của nhóm tự nạp lại (realtime)

User 16/11/2026 tối: làm việc chờ "tab Nhiệm vụ nhóm tự nạp theo task.updated" (ngoài phạm vi GĐ25). User chọn làm trên nhánh
`gop_db-chat-cot-lien-he-hep` (cùng GĐ26), chỉ client, wt-nhom-trao-doi.

Gốc: tab Nhiệm vụ (`?panel=tasks`, `TaskGroupListView`) dựng thay ChatPane (`v-else-if`) ⇒ không ai nghe `chat-event`; danh sách chỉ
nạp khi chính người xem sửa (`@changed`).

- [x] `components/chat/workspace/WorkspaceView.vue`: `created/beforeDestroy` nghe `$root 'chat-event'`; chỉ khi panel = tasks + đúng
      conversation của nhóm; sự kiện `task.updated` hoặc `message.created` kiểu system/card (việc mới / mốc) ⇒ gom 800ms ⇒
      `$refs.taskList.refresh()` (nạp danh sách + emit changed ⇒ nạp lại số trên nút Nhiệm vụ). Không đụng TaskGroupListView.
- [x] Tái hiện TRƯỚC khi sửa (Playwright, spec tạm đã xoá): NV 13 đổi Chờ bắt đầu ⇒ Tạm dừng, NV 24 đang mở tab ⇒ sau 4s dòng vẫn ở
      nhóm "Chờ bắt đầu", 0 request danh sách.
- [x] Sau sửa: dòng sang `ws-task-group-5` "Tạm dừng", 2 lần đổi sát nhau = 1 request; gửi thẻ việc mới ⇒ dòng mới hiện (1 request);
      ở tab Trao đổi đổi trạng thái ⇒ 0 request danh sách.
- [x] e2e có sẵn: workspace-tasks 12/12 · chat-task-status 3/3 · chat-drawer 10/10. Chưa thêm ca e2e mới (user chưa yêu cầu).
- [x] 16/11 commit client `97c97a86f` → origin/gop_db → ĐÃ DEPLOY TPE (cùng GĐ26 + GĐ28; prod client 12a065598).

Giới hạn: nạp lại làm nhóm đang "Xem thêm" thu về trang đầu (fetch có sẵn); BE chưa phát khi XOÁ nhiệm vụ; lỗi mạng lúc nạp nền vẫn
hiện toast của fetch.

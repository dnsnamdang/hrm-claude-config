# GĐ32 — Tin trạng thái nhiệm vụ trong nhóm: gọn + mờ (17/11/2026) @namdangit

## Vấn đề
Tin hệ thống GĐ23 dài ("<người> đã chuyển nhiệm vụ <mã> – <tên ≤80> sang <TT> — Ghi chú: …") + viên nền xanh có viền ⇒ rối khung chat.

## Quyết định đã chốt (user 17/11, "làm 2")
- Câu: "Nhiệm vụ <MÃ> đã được <Tên người> cập nhật từ: <TT cũ> → <TT mới>" — chỉ mã, BỎ tên nhiệm vụ, BỎ HẾT ghi chú / lý do.
- Tên trạng thái lấy đúng hệ thống (vd "Hoàn thành", không "Đã hoàn thành").
- Mã + tên người đậm xám #374151; 2 trạng thái chữ thường, màu theo Task::STATUS color (BE trả trong meta).
- Viên mờ: nền #f8fafc, không viền, chữ #6b7280 12.5px, icon #9ca3af; hover nền #f1f5f9 + viền #e5e7eb. Chỉ tin trạng thái nhiệm vụ (tin họp / hệ thống khác giữ nguyên).
- Tin cũ giữ nguyên câu dài (không ghi đè dữ liệu chat prod); FE thiếu meta mới ⇒ hiện body, vẫn kiểu mờ.

## Kỹ thuật
- BE `SyncWorkspaceChat`: `taskStatusMeta()` (actor_name, old/new_status_text, old/new_status_color) gửi kèm meta + `taskStatusText()`.
- FE `ChatMessageItem.vue`: `taskLine` dựng câu từ meta; testid trạng thái mới `chat-task-new-status` (KHÔNG bắt đầu bằng `chat-msg-task-` — e2e đếm viên bằng tiền tố đó).
- Kiểm: PHPUnit TaskStatusWorkspaceMessageTest, e2e chat-task-status T1 (đo DOM màu/cỡ/nền).
- ĐÃ DEPLOY TPE 17/11 cùng GĐ33 (api b796c8f86 · client 7394e4c47).

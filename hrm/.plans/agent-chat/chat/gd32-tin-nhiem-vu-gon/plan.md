# GĐ32 — Tin trạng thái nhiệm vụ trong nhóm: gọn + mờ (17/11/2026) @namdangit

Nhánh `gop_db-chat-tin-nhiem-vu-gon` (api + client, wt-nhom-trao-doi), không migration, không sửa tin cũ.

## Chốt (user 17/11, "làm 2")
- Câu: "Nhiệm vụ <MÃ> đã được <Tên người> cập nhật từ: <TT cũ> → <TT mới>" — chỉ mã (bỏ tên nhiệm vụ), BỎ HẾT ghi chú / lý do.
- Mã + tên người đậm xám #374151; 2 trạng thái chữ màu theo status color BE (không đậm).
- Viên mờ: bỏ nền xanh + viền, nền #f8fafc, chữ #6b7280 12.5px, icon xám nhỏ; hover đậm lên. Chỉ tin trạng thái nhiệm vụ.
- Tin cũ giữ nguyên câu dài (không ghi đè dữ liệu); FE thiếu meta mới ⇒ hiện body.

## Task
- [x] BE SyncWorkspaceChat: câu mới + meta actor_name, old/new_status_text, old/new_status_color
- [x] PHPUnit TaskStatusWorkspaceMessageTest theo câu mới
- [x] FE ChatMessageItem: dựng câu từ meta (đậm/màu) + CSS mờ
- [x] Playwright đo + e2e chat-task-status + chạy lại bộ chat

## Kết quả kiểm (17/11)
- PHPUnit TaskStatusWorkspaceMessageTest 3/3 (câu đúng nguyên văn, meta actor_name / old·new_status_text·color, không ghi chú); Workspace 259/259.
- e2e chat-task-status T1 viết lại: 4 câu đúng nguyên văn, không tên việc / ghi chú; đo DOM nền #f8fafc, không viền, chữ #6b7280 12.5px, icon #9ca3af, mã + tên #374151 đậm, trạng thái chữ thường màu BE (#2563EB / #F59E0B / #16A34A). 3/3.
- Chạy lại chat-core · giao-dien · bo-sung · thong-bao-emoji · gd2-polish · workspace-tasks · chat-drawer: 59/59 xanh.
- Bẫy: testid con không được bắt đầu bằng `chat-msg-task-` (e2e đếm viên bằng `[data-testid^="chat-msg-task-"]`) ⇒ đặt `chat-task-new-status`.

### Checkpoint — 17/11/2026
Vừa hoàn thành: GĐ32 code xong + kiểm, CHƯA commit (api + client nhánh gop_db-chat-tin-nhiem-vu-gon, wt-nhom-trao-doi).
Bước tiếp theo: user xem :3080 → báo commit/deploy (không migration).
Blocked:

### Checkpoint — 17/11/2026 — ĐÃ DEPLOY TPE
GĐ32 + GĐ33 lên prod: api `b796c8f86` · client `7394e4c47` (gộp origin/gop_db có develop + fix quyền hạng mục giải pháp của người khác — prod đã có sẵn phần đó). build_tpe EXIT 0, Nothing to migrate, site 200.

# Chat bổ sung — Đang soạn tin · Trực tuyến · Avatar ảnh hồ sơ · Xoá ở phía tôi

> Mở 12/11/2026 (phiên CHAT, sau khi core chat + GĐ2 + đợt Z đã merge gop_db). Spec gốc §11 "Để sau: đang soạn tin + trực tuyến".

## Chốt với user 12/11/2026
- **Xoá tin = 1:** thêm "Xoá ở phía tôi" (như Zalo): ẩn 1 tin chỉ với mình, xoá được cả tin người khác, không giới hạn
  thời gian; người khác vẫn thấy. Thu hồi giữ nguyên (tin của mình, ≤ 24h, mọi người thấy "Tin đã bị thu hồi").
- **Đang soạn = 1:** dưới khung tin "Nam đang soạn tin…" (nhóm: "Nam, Hà đang soạn tin…", > 2 người: "Nam và 2 người khác…");
  dòng hội thoại bên trái tạm thay dòng tin cuối bằng chữ nghiêng "đang soạn tin…". Tắt sau ~5 giây ngừng gõ / khi gửi.
- **Trực tuyến = làm luôn:** chấm xanh ở avatar + dòng "Đang hoạt động / Truy cập … trước" đầu khung chat 1–1.
- **Avatar (Claude tự chốt — thuần UI):** có `image` hồ sơ nhân sự ⇒ ảnh tròn; không có / ảnh lỗi ⇒ chữ cái màu như cũ;
  nhóm ghép 2×2 (ô có ảnh thì ảnh, không thì chữ).

## Thiết kế kỹ thuật
### A. Avatar (FE, BE bổ sung chỗ thiếu)
- BE: rà mọi chỗ trả người (ConversationService danh sách + `other`, ChatPresenter `sender` / members, directory, gợi ý @)
  đã có `image` chưa — thiếu thì thêm từ `EmployeeProfiles::format`.
- FE `ChatAvatar.vue`: prop `image` (+ `members[].image`); `<img @error>` ⇒ quay về chữ. Truyền `image` ở mọi chỗ gọi.

### B. Xoá ở phía tôi
- Migration `Modules/Assign/Database/Migrations/2026_11_15_000001_create_chat_message_hides_table.php`:
  `chat_message_hides(id, message_id, employee_id, created_at)` unique(message_id, employee_id), index employee_id.
- API `POST v1/assign/chat/messages/{id}/hide` (middleware read — người chỉ Xem / nhóm đóng vẫn xoá phía mình được).
- Lọc tin đã ẩn ở: lấy tin (cursor), tin ghim (dải ghim của mình), tìm tin, dòng tin cuối ở danh sách hội thoại
  (ẩn tin cuối ⇒ hiện tin trước đó chưa ẩn), xem trước trả lời (tin được trả lời bị mình ẩn ⇒ "Tin đã bị xoá").
  Số chưa đọc: tin đã ẩn không tính. Chia sẻ tin mình đã ẩn ⇒ 422.
- FE: menu ⋯ thêm "Xoá ở phía tôi" (mọi tin trừ tin hệ thống), hỏi xác nhận nhỏ (V2BaseModal), xoá khỏi danh sách tại chỗ.
- Realtime: chỉ đồng bộ các tab khác của chính mình (gói `chat` loại `hidden` gửi kênh của mình).

### C. Đang soạn tin
- API `POST v1/assign/chat/conversations/{id}/typing` (middleware send) — FE gọi tối đa 1 lần / 3 giây khi đang gõ
  (không gửi khi ô trống). BE publish Redis **trực tiếp** (không qua queue — cần nhanh) gói `{kind:'chat', type:'typing',
  conversation_id, employee_id, fullname}` tới kênh các thành viên khác còn trong hội thoại (không gửi người tắt thông báo? — vẫn gửi,
  chỉ là chữ trên màn). Throttle BE 1 lần/2 giây/người/hội thoại (Redis key TTL) chống spam.
- FE store chat: `typing[conversationId] = {employee_id: hếtHạnLúc}`; hết hạn 5 giây; nhận tin mới của người đó ⇒ xoá ngay.

### D. Trực tuyến
- `server_node/server.js`: khi socket kết nối ⇒ Redis `INCR hrm_database_chat_online:{sub}`; ngắt ⇒ `DECR`, về 0 ⇒ `DEL` +
  `SET hrm_database_chat_last_seen:{sub} = now` ; khi chuyển 0↔1 ⇒ `io.emit('presence', {employee_id, online, last_seen_at})`
  (gói nhẹ, FE chỉ dùng cho người đang hiện). Kết nối treo (node chết) ⇒ đếm lệch: đặt TTL 2 phút + FE ping 60 giây làm mới
  (`EXPIRE`) để tự hết.
- Kiểm `socket.decoded.sub` là id gì (employees.id hay users.id) trước khi dùng làm khoá — đối chiếu kênh user_notification.
- BE: `ChatPresence::of(ids)` đọc Redis (MGET) ⇒ thêm `online` + `last_seen_at` vào `other` của hội thoại 1–1, thành viên,
  directory.
- FE: chấm xanh ở ChatAvatar (prop `online`), đầu khung chat 1–1 "Đang hoạt động" / "Truy cập 5 phút trước"; nghe `presence`.
- Deploy: restart socket (`pm2 restart hrm-tpe-socket`, pm2 root).

## Task
- [x] T1 BE avatar: đủ `image` mọi chỗ trả người + PHPUnit
- [x] T2 BE xoá phía tôi: migration + API hide + lọc 6 chỗ + PHPUnit (có/không quyền, tin người khác, chưa đọc, tin cuối)
- [x] T3 BE đang soạn: API typing + throttle + publish trực tiếp + PHPUnit (người ngoài 403, người Xem 403)
- [x] T4 Socket + BE trực tuyến: server.js đếm kết nối + presence; ChatPresence; PHPUnit phần BE
- [x] T5 FE avatar ảnh (ChatAvatar + mọi chỗ gọi)
- [x] T6 FE Xoá ở phía tôi (menu ⋯ + xác nhận + đồng bộ tab)
- [x] T7 FE đang soạn (gửi throttle, hiện dưới khung + dòng hội thoại)
- [x] T8 FE trực tuyến (chấm xanh + dòng trạng thái + nghe presence)
- [x] T9 e2e: ca mới cho 4 mục (có/không quyền) + chạy lại TOÀN BỘ chat-core, chat-gd2-polish, chat-toolbar-zalo,
  workspace-tasks; đo DOM (ảnh thật naturalWidth > 0, chấm xanh toạ độ, dòng đang soạn xuất hiện/tắt ≤ 6s)

## Checkpoint — 12/11/2026 (thiết kế, chờ lệnh code)
Vừa hoàn thành: rà code (typing/presence chưa có; avatar BE có `image`, FE bỏ qua; thu hồi có, xoá từng tin chưa có); user chốt 3 câu.
Bước tiếp theo: hỏi user "làm" kèm phạm vi (nhánh mới từ origin/gop_db, worktree wt-nhom-trao-doi, 1 migration chạy db_gop_6_11).

## Checkpoint — 12/11/2026 ~22:55 (CODE XONG T1–T9, CHƯA commit)
Vừa hoàn thành: user cho phép "làm" (phạm vi: wt-nhom-trao-doi, nhánh MỚI `gop_db-chat-bo-sung` từ origin/gop_db api c106ea6e3 / client 8fc0f6648,
1 migration). Đã chạy đúng 1 migration `2026_11_15_000001_create_chat_message_hides_table` vào db_gop_6_11 (--path --force; .env worktree ghi
APP_ENV=production nhưng DB_HOST 127.0.0.1). Restart socket :8895 (PID mới 92972, log ở scratchpad phiên); :8080 php -S + :3080 nuxt dev giữ nguyên.
- BE: `ChatMessageHide` + `POST chat/messages/{id}/hide` (middleware read); lọc tin đã ẩn ở list / pins / search / chưa đọc / tin cuối (lùi về tin
  trước, `visibleLastIds` 1 query khi có) / trích dẫn (`reply_to.hidden`) / chia sẻ (422); tin hệ thống 422. `ChatPresence`: đọc Redis
  `chat_online:{id}` / `chat_last_seen:{id}` ⇒ `online` + `last_seen_ms` ở `other` (danh sách + chi tiết) và members; `POST conversations/{id}/typing`
  (middleware send, chặn 2s bằng Redis NX, publish thẳng không qua queue, không gửi chính mình); gửi tin xong xoá khoá typing (bắt được bằng e2e:
  gõ tiếp ngay sau khi gửi bị nuốt 2–3 giây).
- server.js: đếm kết nối INCR/DECR + TTL 180s, `presence_ping` làm mới, về 0 ghi last_seen; `io.emit('presence')` cho MỌI kết nối (gói chỉ id +
  online + last_seen_ms).
- FE: ChatAvatar ảnh (chỉ URL http(s), lỗi tải ⇒ chữ cái) + chấm xanh; store `presence` / `typing` (+ prune 1s); BasicSubsystem ping 50s + nghe
  `presence`; ChatPane đầu khung "Đang hoạt động / Truy cập … trước", dòng "… đang soạn tin…" cuối vùng tin, Xóa ở phía tôi (confirm chung,
  chữ "Xóa" theo button-convention); ConversationRow chấm xanh + "đang soạn tin…"; menu ⋯ luôn có "Xóa ở phía tôi" (kể cả tin đã thu hồi).
- Kiểm: PHPUnit ChatHideTypingPresenceTest 8 ca; Workspace 107/107, Task 31/31. e2e MỚI `HRM/e2e/tests/assign/chat-bo-sung.spec.ts` 6/6 (đo DOM:
  ảnh 32×32 tròn naturalWidth>0, chặn S3 ⇒ chữ cái; chấm xanh góc dưới phải 11px #22c55e; dòng đang soạn nghiêng xám dưới tin cuối, tắt khi gửi,
  tự tắt < 8s; 403 người ngoài / Xem; xóa phía tôi + trích dẫn + tải lại + B vẫn thấy; tin cuối lùi; tin thu hồi chỉ còn menu Xóa). Sửa Z3/Z4
  `chat-toolbar-zalo` (menu thêm "Xóa ở phía tôi"). Hồi quy 4 bộ chat-core + chat-gd2-polish + chat-toolbar-zalo + workspace-tasks 35/35.
  Dọn: 0 nhóm [e2e], 0 hides, notifications 660,696 không đổi.
Đang làm dở: —
Bước tiếp theo: user xem thử :3080 → commit / push / merge gop_db khi user báo.
Deploy cần: migration `2026_11_15_000001` · build client · `pm2 restart hrm-tpe-socket` (server.js đổi; pm2 root).
Ghi chú: trực tuyến chỉ tính khi đang mở app có BasicSubsystem (layout payroll dùng PayrollMenu không kết nối socket ⇒ hiện offline).
Blocked: —

## Checkpoint — 13/11/2026 (ĐÃ MERGE + PUSH gop_db)
Commit nhánh gop_db-chat-bo-sung: api 928a43ab3 · client 44c48d3b6. Merge commit lên origin/gop_db: api 337060dca · client c6ef88003
(tạo bằng commit-tree, không checkout worktree gop_db dùng chung — local gop_db ở HRM/ vẫn lùi, cần pull khi dùng). Nhánh feature cũng đã push.
Bước tiếp theo: deploy khi user báo (migration 2026_11_15_000001 · build client · pm2 restart hrm-tpe-socket).

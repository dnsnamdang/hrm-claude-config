# GĐ15 — Danh sách hội thoại: tô rõ dòng đang mở (15/11/2026) · @namdangit

Nhánh client `gop_db-chat-active-row` (wt-nhom-trao-doi, tách từ origin/gop_db 960d04154). Không đụng BE, không migration.

## Vấn đề (user 15/11)
Bấm icon chat topbar ⇒ ngăn mở sẵn hội thoại cũ nhưng danh sách trái không tô dòng đang mở; kiểu tô sáng lại quá mờ.

Tái hiện (Playwright :3080, NV 13): chọn nhóm 96 ⇒ `.cr--active` = 96; đóng + mở lại ⇒ `drawer.conversationId=96`
nhưng `activeId=null`, 0 dòng active. Gốc: `ChatDrawer.onClosed()` xoá activeId, ngăn chỉ `v-show` nên ChatPane
không dựng lại ⇒ không ai gán lại. Style GĐ8: nền #fff trên nền list #fbfcfd + viền xám 1px, vạch teal `left:-6px`.

## Task
- [x] T1 `ChatDrawer.onOpened`: gán lại `setActive(drawer.conversationId)` (trừ Agent); đang ở mục Chat ⇒ `markRead`.
- [x] T2 `ConversationRow` (dùng chung trang /assign/messages): active = nền #e6f5f1 + vạch teal 3px trong dòng + tên 600 #0f766e (PA1 — Claude khuyên, user trả "làm" không chọn số).
- [x] T3 Đo lại Playwright: chọn 96 ⇒ active 96; đóng + mở lại ⇒ active 96 (trước sửa: 0 dòng). Nền rgb(230,245,241), vạch left 0 · 3px #1abc9c, tên 600 rgb(15,118,110). Chưa commit.
- [x] T4 (user 15/11) Danh sách THU GỌN: rê chuột hiện tên NGAY — thay `title` gốc (trình duyệt trễ ~1–2s) bằng `v-b-tooltip` qua helper `collapsedTip()` (utils/chat/chatFormat.js, delay 0, bên phải, tắt khi mở rộng) ở ConversationRow + thẻ TPE SMART AGENT (ConversationList). Đo Playwright: hiện sau 74ms (dòng) / 46ms (Agent), đứng yên 2,5s, mở rộng ⇒ không tooltip, 0 lỗi console.

- [x] T5 (user 15/11, mục ngoài luồng) Tin tới lúc ngăn ĐÓNG bị đánh dấu đã đọc: ChatPane sống (v-show) vẫn nghe socket ⇒ `markRead()` chỉ chặn `document.hidden`. Tái hiện (nhóm thử NV13+NV24, tin thật qua API + giả lập gói socket đúng nhánh BasicSubsystem vì socket local không tới trình duyệt headless): ngăn đóng ⇒ 1 lần POST read, FE 0, BE 0. Sửa: `ChatPane.markRead` thêm điều kiện `activeId === Number(conversationId)`. Đo lại: ngăn mở ⇒ read 1/BE 0 · ngăn đóng ⇒ read 0/FE 1/BE 1 · mở lại ⇒ read 1/BE 0 · trang nhóm đầy đủ ⇒ read 1/BE 0. Nhóm thử 8330–8334 đã xoá.

- [x] T6 (user 15/11) e2e `chat-drawer.spec.ts` thêm N6 (mở lại ngăn vẫn tô sáng + tooltip thu gọn < 500ms, mở rộng không tooltip) · N7 (tin tới lúc ngăn đóng qua socket THẬT: 0 lần /read, BE 1; mở lại ⇒ /read, BE 0). Kết quả: 7/7 đạt 4 lượt liên tiếp. Lượt đầu N7 đỏ 1 lần (0 lần /read từ trang thử nhưng BE 0) — CHƯA rõ nguyên nhân, nghi trình duyệt thật của NV 13 (user) cùng nối socket vừa bật lại; không lặp lại.
- Môi trường: socket :8895 cũ (PID 3836, bật 07:02 trong `server_node/`) không có .env ⇒ JWT_SECRET rỗng ⇒ từ chối mọi kết nối cả ngày. Đã bật lại (user cho phép) từ `hrm-api/`: `SOCKET_PORT=8895 node server_node/server.js` (PID 37071, log scratchpad phiên ff4e2df6).

## Còn lại
- Chưa commit (4 file client + utils/chat/chatFormat.js). Chờ user báo merge / e2e `chat-drawer.spec.ts` khi được yêu cầu.

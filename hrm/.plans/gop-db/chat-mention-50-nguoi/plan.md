# Chat — gợi ý @tag hiện đủ người (nâng giới hạn 8 → 50) — @cuong61n

## Vấn đề
Gõ `@` trong chat chỉ hiện tối đa 8 dòng (gồm cả `@all`), người đứng sau (vd tên Cường) không thấy, phải gõ thêm chữ mới ra. Gốc: `slice(0, 8)` chặn trước khi hộp gợi ý kịp cuộn.

## Tasks
- [x] 19/11/2026 — Web: `hrm-client/components/chat/ChatComposer.vue` `mentionItems` đổi `slice(0, 8)` → `slice(0, 50)`; hộp gợi ý đã có `max-height: 260px` + cuộn nên người dùng kéo xuống xem hết.
- [x] 19/11/2026 — App: `TPE_APP/app/lib/ui/chat/room/widget/mention_suggest.dart` `chatMentionItems(limit)` 8 → 50 (`MentionSuggest` đã là ListView có `maxHeight`).
- [x] 19/11/2026 — Test app: `test/ui/chat/message_actions_test.dart` sửa kỳ vọng "tối đa 50" (80 thành viên → 50 dòng); cả file 30 test pass. Web chưa chạy Playwright/simulator.

## Trạng thái
Đã sửa code local, chưa commit/push. Chờ test tay (web + app).

- [x] 19/11/2026 — Đã push: web `hrm-client` nhánh `gop_db` (b621e464f), app `TPE_APP` nhánh `develop` (de63caa). Chưa build / deploy prod.

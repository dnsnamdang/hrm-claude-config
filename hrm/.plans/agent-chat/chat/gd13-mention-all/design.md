# GĐ13 — @all nhắc tất cả thành viên nhóm (như Zalo)

> 15/11/2026 · trạng thái: design ngắn, CHỜ USER DUYỆT · chưa có lệnh code

## 1. Mục đích

Trong Nhóm trao đổi, gõ `@all` để nhắc **mọi thành viên** một lần — ai cũng thấy mình được nhắc (dấu @ ở dòng hội
thoại) và nhận thông báo, khỏi phải @ từng người.

## 2. Đã chốt với user

| # | Câu hỏi | Chốt |
|---|---|---|
| A1 | Ai được @all | **Mọi thành viên được gửi tin** (không giới hạn Quản lý nhóm, không có công tắc cài đặt) |
| A2 | @all với người đã tắt thông báo nhóm | **Tôn trọng tắt thông báo**: không push / toast; vẫn thấy dấu @ khi mở app. @Tên vẫn vượt tắt thông báo như cũ |
| A3 | Cách làm | **Cờ trên tin** `chat_messages.mention_all` — 1 tin @all = 1 dấu, không ghi 1 dòng/người |

## 3. Phương án đã cân nhắc

1. **Cờ trên tin (CHỌN)** — 1 cột, nhóm 2.000 người vẫn 1 dòng; phải sửa 3 chỗ đọc mention (đếm @ danh sách hội
   thoại, job push, presenter) + FE.
2. BE mở rộng @all thành N dòng `chat_message_mentions` + cột phân biệt loại — đọc gần như giữ nguyên, nhưng N
   dòng/tin, sửa / thu hồi ghi lại N dòng ⇒ trái nguyên tắc tải 1–2 nghìn người.
3. FE gửi id mọi người — vướng `mention_ids max:200`. Loại.

## 4. Hiện trạng (đọc code wt-nhom-trao-doi 15/11)

- @ chỉ có ở hội thoại `space` (`ChatPane::mentionable`); FE gõ `@` ⇒ gợi ý ≤ 8 người (`ChatComposer::mentionItems`),
  gửi `mention_ids` (≤ 200).
- BE `MessageService::syncMentions` ghi `chat_message_mentions` (chỉ người còn trong hội thoại, bỏ chính mình); sửa tin
  xoá–ghi lại.
- Dấu @: `ConversationService` (leftJoin mentions, `COUNT(mm.id) AS mentioned`) ⇒ `ConversationRow` `cr__badge--at`.
- Push: `PushChatMessage` — người tắt thông báo bỏ qua trừ khi bị @ (tin chưa đọc); dòng "X đã nhắc đến bạn: …".
- Toast web: `PublishChatActivity` gửi `muted_ids`, FE (`chatNotifier.js`, `store/chat.js`) xét `mention_ids`.
- Hiển thị: `ChatMessageItem::html` tô nền `@Tên` của người trong `mention_ids`.

## 5. Thiết kế

**BE (hrm-api)**
- Migration: `chat_messages.mention_all` boolean default false.
- `SendMessageRequest` / `EditMessageRequest`: thêm `mention_all` boolean. Chat 1–1 (`direct`) ⇒ bỏ qua, ghi false
  (giống `syncMentions` không chặn theo loại; FE chỉ mở @ ở `space`). Người gửi phải được gửi tin (đã kiểm sẵn ở luồng gửi).
- `MessageService::send / edit`: lưu cờ; sửa tin ghi lại cờ theo nội dung mới. Thu hồi ⇒ không tính (đã lọc
  `recalled_at`).
- `ConversationService` đếm @: `mentioned` = COUNT(mm.id) + SUM(m.mention_all) trên cùng tập tin chưa đọc (đã loại tin
  của chính mình, tin ẩn, tin thu hồi) — không thêm query.
- `PushChatMessage`: người tắt thông báo vẫn chỉ được push khi có @Tên (giữ nguyên — A2). Người bật thông báo: tin mới
  nhất có `mention_all` ⇒ dòng `"X đã nhắc đến mọi người: …"`; nếu đồng thời bị @Tên ⇒ ưu tiên "đã nhắc đến bạn".
- `ChatPresenter`: trả `mention_all` (tin thu hồi ⇒ false).
- Realtime `message.created`: gói tin đã có `mention_all` qua presenter; `muted_ids` giữ nguyên.

**FE (hrm-client)**
- `ChatComposer`: gợi ý `@` thêm dòng đầu **"@all — Nhắc tất cả (N thành viên)"** (hiện khi query rỗng hoặc khớp
  `all` / `tat ca`); chọn ⇒ chèn `@all `. Khi gửi: `mention_all = body có token "@all"` (ranh giới từ). Bản nháp / sửa
  tin giữ cờ theo nội dung.
- `ChatMessageItem::html`: tin có `mention_all` ⇒ tô `@all` cùng kiểu `cm__mention`.
- Toast / âm thanh web (`chatNotifier.js` / `store/chat.js`): người KHÔNG tắt thông báo ⇒ toast "đã nhắc đến mọi
  người"; người tắt thông báo ⇒ không toast (A2).
- Placeholder ô soạn: giữ "gõ @ để nhắc tên".

**Ngoài phạm vi**: chat 1–1 (không có @); @ theo phòng ban / vai trò; app mobile (API trả sẵn `mention_all` để app dùng sau).

## 6. Kiểm

- PHPUnit (Workspace / Chat): gửi @all ⇒ cờ true; hội thoại direct ⇒ false; đếm `mentioned` cho người khác, không cho
  người gửi; tin đã đọc / thu hồi không tính; push: người tắt thông báo không nhận @all, vẫn nhận @Tên.
- Playwright đo DOM: gợi ý có dòng @all + số thành viên; tin hiện `@all` tô nền; tài khoản thứ 2 thấy dấu @ ở dòng hội
  thoại; người tắt thông báo không có toast.

## 7. Để builder tự quyết

Vị trí cột trong migration, tên khoá dịch, chi tiết regex token `@all`, style dòng gợi ý (theo `cc__mention-item`).

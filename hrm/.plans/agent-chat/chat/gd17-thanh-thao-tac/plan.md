# GĐ17 — Thanh thao tác tin chat to hơn + không đè hàng cảm xúc (15/11/2026) · @namdangit

Nhánh client `gop_db-chat-thanh-thao-tac` (wt-nhom-trao-doi, tách từ origin/gop_db 828d88245). Không BE, không migration.
Mockup 3 phương án: `mockup.html` — user chọn **B** (nút to có chữ).

## Vấn đề (user)
Rê tin của mình ⇒ thanh thao tác đè hàng cảm xúc; thanh quá nhỏ, khó bấm bằng chuột.
Tái hiện: thanh (y 710–744, z-index 5) đè hàng emoji (y 689–723) 13px; nút 28×28, icon 12px.

## Task
- [x] T1 `ChatMessageItem.vue`: nút `V2BaseIconButton.cm__act` 58×50, icon 19px + chữ (Trả lời · Chia sẻ · Nhiệm vụ · Nhắc việc · Thêm), bỏ tooltip; thanh bo 14px bóng đổ; rê nút nền #e6f5f1 chữ #0f766e.
- [x] T2 `placeActions()` viết lại: thanh nổi TRÊN mép bong bóng (tin mình canh phải, người khác canh trái), sát đầu vùng cuộn ⇒ xuống dưới (`is-below`), kẹp trong bề ngang .cm; cầu nối ::after 8px giữ hover; `.cm__like` z-index 6 > thanh 5.
- [x] T3 e2e `chat-toolbar-zalo.spec.ts`: Z1 viết lại (5 nút có chữ ≥ 44px, trên mép trái bong bóng, rê qua khe không mất) · Z1b mới (tin mình canh phải, rê 👍 ⇒ 0 điểm emoji bị che) · Z4 thêm Nhắc việc cho vai trò Xem (GĐ16 làm Z1/Z4 cũ đỏ — sót khi làm GĐ16).
- [x] T4 Đo Playwright: nút 58×50 icon 19px; tin mình/khác lệch mép 0px; emoji bị che 0/28; menu ⋯ mở; bong bóng cách đầu vùng cuộn 20px ⇒ thanh xuống dưới; 0 lỗi console. e2e: chat-toolbar-zalo 9/9 · chat-drawer 7/7 · chat-giao-dien 5/5 (cần CHAT_TOKEN_C NV 25).

- [x] T5 (15/11, user) BỎ chữ + chuyển thanh BÊN CẠNH bong bóng (PA 1): thanh có chữ nổi trên bong bóng che tin phía trên — e2e E3 bắt được (nút Thêm của tin sau chặn chip 🦄 tin trước). Nay: nút 40×40 icon 20px + tooltip; tin mình thanh bên TRÁI (chừa 👍 34px), người khác bên PHẢI, canh giữa dọc; không đủ chỗ ⇒ nổi trên / dưới như cũ. Hàng cảm xúc tin mình bung sang PHẢI (không phủ thanh — trước đó chặn nút Thêm). Đo: lệch tâm 0px, cách tin trên 25/65px, emoji bị che 0/28, menu ⋯ mở được.
- [x] T6 GĐ17b cỡ chữ (user chọn PA 1): tin + ô soạn 15px/22px (ô soạn trước 13px — luật 13.5px thua CSS V2BaseTextarea ⇒ thêm !important), tên 14px, giờ 12px, tin hệ thống 13px, DS hội thoại 14.5/13.5/12px. Lớp tô nền @ tự chép theo syncHl: khớp 100% (font 15/22, khung lệch 0, scrollHeight 82 = 82).
- [x] T7 e2e Z1/Z1b viết lại theo thanh cạnh bên (tooltip 5 nút, nút ≥ 40px, không giao hàng emoji, bấm được Thêm). Kết quả: chat-toolbar-zalo 9/9 · chat-thong-bao-emoji 10/10 · chat-drawer 7/7 · chat-giao-dien 5/5 · chat-bo-sung 6/6.

- [x] T8 GĐ17c (user 15/11) phần dưới khung soạn: placeholder 12.8 → 15px (CSS chung ép ::placeholder ⇒ !important), 5 nút công cụ 30 → 36px icon 14 → 20px, hover teal nhạt; nút Gửi cao 32 → 36 chữ 12 → 14px; dòng gợi ý 11 → 12px. Khung soạn cao 100 → 104px. e2e 5 bộ chat đạt (9 · 10 · 7 · 5 · 6).

## Còn lại
- ĐÃ lên origin/gop_db 15/11: client `87a115c9a` (nhánh gop_db-chat-thanh-thao-tac, đã push), CHƯA deploy, chỉ client.
ĐÃ DEPLOY TPE 15/11 tối: prod client 87a115c9a (gồm GĐ15+16+17), api 3fefb0545.
- e2e chat-core: ca @ sửa theo GĐ13 (dòng đầu @all ⇒ ArrowDown rồi Enter chọn B) ⇒ 8/8.

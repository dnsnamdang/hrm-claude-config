# GĐ26 — Cột hội thoại (panel liên hệ bên trái) hẹp bớt

User 16/11/2026: "giảm kích thước panel liên hệ bên trái xuống 1 chút". Nhánh client `gop_db-chat-cot-lien-he-hep` (từ fe3ff8755).

- [x] `components/chat/ConversationList.vue` `.cl`: 360px ⇒ 320px (GĐ7 từng 288 ⇒ cắt tên nhóm dài, nên không xuống thấp hơn).
- [x] Đo Playwright (trang nhóm + khung chat trượt, NV 13, 50 hội thoại): 360 ⇒ 320, không tràn ngang; tên bị "…" 0 ⇒ 2/50 (tên rất dài);
      hàng nút lọc vừa (nút cuối 307/319px); ô tìm chỉ còn 84px chữ ⇒ placeholder "Tìm nhóm, tên, mã NV" (118px) bị cắt ⇒ đổi
      "Tìm tên, mã NV" (82px; "tên" gồm tên nhóm + tên người).
- [x] e2e chat-drawer 10 · chat-giao-dien 5 · chat-core 8 xanh.
- [x] 16/11 commit client 067de626b trên nhánh `gop_db-chat-cot-lien-he-hep` (worktree wt-nhom-trao-doi) — CHƯA push, CHƯA merge gop_db, CHƯA deploy.

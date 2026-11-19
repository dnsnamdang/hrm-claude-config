# GĐ24 — Tab Thành viên nhóm chat: phân trang 20 dòng

User 16/11/2026: "Tab Thành viên nhóm chat: Làm phân trang, 1 trang 20 row mặc định" — "làm".
Cùng nhánh client `gop_db-chat-tin-trang-thai-nhiem-vu` (chờ deploy cùng GĐ23). Không đổi BE.

- [x] `components/chat/workspace/MembersPanel.vue`: phân trang TRÊN MÁY bằng `V2BasePagination` (API vẫn trả đủ — ô tìm, lọc vai trò kèm
      số đếm, popup Thêm thành viên cần cả danh sách); mặc định 20, chọn 10/20/50/100; STT liên tục; tìm / đổi vai trò / đổi nhóm ⇒ trang 1;
      thêm-bớt làm trang vượt cuối ⇒ lùi trang cuối.
- [x] e2e mới `tests/assign/chat-members-paging.spec.ts` 3/3 (nhóm 46 người: 20 dòng, "1–20 / 46", trang 2 STT 21, trang 3 còn 6; đổi 50 / 10;
      tìm ⇒ trang 1 "1–1 / 1"; trong khung chat trượt cũng 20 dòng; đo không tràn ngang).
- [x] Spec liên quan: chat-drawer 10 · chat-giao-dien 5 · workspace-tasks 12 xanh; workspace-kh-project 7 skipped (thiếu biến môi trường riêng).
- [x] 16/11 commit client 41bc5eb0f, gop_db fast-forward. ĐÃ DEPLOY TPE cùng GĐ23 (api c284cdfe5 · client 41bc5eb0f).

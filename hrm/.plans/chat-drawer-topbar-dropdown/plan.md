# Ngăn chat che dropdown topbar — @khoipv

Plan gốc của ngăn trượt chat (`.plans/agent-chat/chat/gd10-ngan-truot/plan.md`) không có trên máy này → ghi tạm ở đây.

## Fix 17/11/2026 — mở ngăn chat thì không thao tác được nút trên topbar

- [x] Điều tra: `.navbar-custom` (fixed, z-index 1001) là stacking context → dropdown Phân hệ / Chuông / Công ty / Tài khoản
      bị kẹt ở 1001, nằm SAU ngăn chat `.cdw` (z-index 1035). Bấm vẫn ăn nhưng menu bị che → tưởng không bấm được.
- [x] Sửa `hrm-client/components/chat/ChatDrawer.vue` (khối style global `body.chat-drawer-open`): nâng `.navbar-custom`
      lên `z-index: 1039 !important` — trên ngăn (1035) + rail sidebar (1038), dưới backdrop popup bootstrap (1040).
      Chỉ hiệu lực khi ngăn đang mở.
- [x] User kiểm tra trên trình duyệt (OK 17/11): mở ngăn chat → bấm Chuông / Phân hệ / Đổi công ty / Tài khoản → menu hiện trên ngăn;
      mở popup bootstrap trong ngăn → popup vẫn phủ lên topbar.

### Checkpoint — 2026-11-17
Vừa hoàn thành: nâng z-index topbar khi ngăn chat mở — user đã xác nhận menu hiện đúng
Đang làm dở: —
Bước tiếp theo: — (xong)
Blocked:

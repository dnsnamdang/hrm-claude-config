# Ngăn chat che dropdown topbar — design (tóm tắt) — @khoipv

Spec chi tiết: `docs/superpowers/specs/2026-11-17-chat-drawer-topbar-dropdown-design.md`

## Vấn đề
Mở ngăn trượt chat (icon chat trên topbar) → bấm Phân hệ / Chuông / Đổi công ty / Tài khoản trên topbar "không ăn".
Thực tế menu có mở nhưng nằm SAU ngăn chat.

## Nguyên nhân
- `.navbar-custom` `position: fixed; z-index: 1001` → tạo stacking context, mọi dropdown con bị kẹt ở tầng 1001.
- Ngăn chat `.cdw` (portal ra `<body>`) `z-index: 1035`, phủ từ `top: 60px` → che menu xổ xuống.

## Quyết định
- Chỉ sửa `hrm-client/components/chat/ChatDrawer.vue`, khối style global `body.chat-drawer-open` (đã có sẵn để nâng sidebar):
  `.navbar-custom { z-index: 1039 !important; }`
- Thang tầng khi ngăn mở: ngăn 1035 < misa 1036/1037 < sidebar rail 1038 < **topbar 1039** < backdrop popup bootstrap 1040 / modal 1050 / menu ⋯ tin 1060.
- Không đụng `BasicSubsystem.vue` / scss chung; ngăn đóng thì topbar về 1001 như cũ.

## Trạng thái
Code xong, user đã kiểm trình duyệt OK (17/11/2026). Chưa commit.

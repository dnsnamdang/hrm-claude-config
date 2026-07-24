# Plan — Fix content bị đè lên menu trái (toàn hệ thống)

@junfoke

## Phase 1 — Fix CSS layout condensed sidebar

- [x] Điều tra root cause (systematic-debugging)
- [x] Xác định commit gây lỗi qua `git blame`
- [x] Sửa `assets/scss/custom/structure/_left-menu.scss` — trả `margin-left` về biến `$leftbar-width-condensed`
- [x] Verify computed style bằng Playwright (sidebar 58px / margin-left 58px / overlap 0px)
- [x] Verify trên màn thật sau đăng nhập: `/training/training_types` (menu hết ở 58px, title H4 bắt đầu 68px → hở 10px) + ảnh chụp khớp ảnh mẫu user gửi
- [x] Verify module khác: `/assign/dashboard` OK (condensed, content-page left 58 = menu right 58)
- [ ] User kiểm tra thêm các module còn lại (payroll, timesheet, decision, CRM)

### Checkpoint — 2026-07-15

Vừa hoàn thành: Fix `body[data-sidebar-size='condensed'] .content-page { margin-left }` từ `45px` hardcode → `$leftbar-width-condensed` (58px).

Root cause: commit `901531a1` ("fix base ui v2", 2024-08-28) đổi
`margin-left: $leftbar-width-condensed !important` → `margin-left: 45px !important`,
trong khi `.left-side-menu` khi condensed vẫn rộng đúng `$leftbar-width-condensed` = 58px
(cùng file, dòng 270). Lệch 13px → content chui xuống dưới sidebar (sidebar `position: absolute`).
Vì rule gắn vào `body[data-sidebar-size='condensed']` nên **mọi màn** dùng sidebar thu gọn đều dính,
không riêng màn Quản lý loại đào tạo.

Bằng chứng pattern: các cặp width/margin khác trong cùng file đều dùng chung biến —
default `$leftbar-width` (dòng 14/22), compact `$leftbar-width-sm` (dòng 515/553),
footer condensed `left: $leftbar-width-condensed` (dòng 454). Chỉ dòng 448 lệch chuẩn.

Đang làm dở: (không)

Đã VERIFY trên màn thật (user cấp tài khoản dev): `/training/training_types` — menu kết thúc x=58,
tiêu đề "Quản lý loại đào tạo" (H4) bắt đầu x=68 → hở 10px, khớp ảnh mẫu user gửi.
`/assign/dashboard` — content-page left 58 = menu right 58, không đè.
(`/human/employees` không dùng sidebar condensed này → không ảnh hưởng.)

Bước tiếp theo: User hard-refresh (Ctrl+Shift+R) và kiểm tra nốt payroll/timesheet/decision/CRM.

Blocked: (không)

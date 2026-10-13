# Plan — Chuyển menu "Khai Quy chế – Cấu hình" sang phân hệ Bán hàng

Nhánh `gop_db` · repo `hrm-client` · @namdangit · 2026-09-21
Design: `.plans/gop-db/chuyen-menu-quy-che-cau-hinh/design.md`

## Phase 1 — Chuyển khai báo menu

- [x] Gỡ mục cấp 1 "Khai Quy chế – Cấu hình" (`/master-data/regulation-config`) khỏi
      `components/subsystem-menu/master-data.js`
- [x] Thêm screen `{ n: 'Khai Quy chế – Cấu hình', link: '/master-data/regulation-config' }` vào
      nhóm "Quy chế - Thiết lập" › item "Thiết lập" trong `components/subsystem-menu/sale-hub.js`
- [x] Verify Playwright:
      - Sidebar **Danh mục**: "Khai Quy chế" BIẾN MẤT (các mục khác Địa lý/Ngân hàng câu hỏi còn nguyên)
      - Sidebar **Bán hàng**: "Khai Quy chế – Cấu hình" hiện trong nhóm "Quy chế - Thiết lập", link đúng
      - Mở `/master-data/regulation-config` → render sidebar **BÁN HÀNG** (resolveSubsystem → sale), page title đúng
- [x] Commit/push — DONE `86b1c9587`

## Phase 2 — Đổi URL /master-data/regulation-config → /sale/regulation-config

- [x] `git mv pages/master-data/regulation-config/index.vue pages/sale/regulation-config/index.vue`
      (giữ `extends RegulationConfigScreen`, KHÔNG override subsystem → mặc định 'master-data' = đủ tab như cũ);
      xoá thư mục rỗng `pages/master-data/regulation-config/`; cập nhật comment trong page
- [x] Đổi link menu trong `sale-hub.js`: `/master-data/regulation-config` → `/sale/regulation-config`
- [x] Cập nhật comment trong `master-data.js` (URL mới) + 2 comment tham chiếu URL cũ ở
      `finance.js` và `pages/finance/regulation-config/index.vue`
- [x] KHÔNG đụng ref `master-data/regulation-config-*` trong RegulationConfigScreen.vue (đó là URL API BE)
- [x] Verify Playwright:
      - `/sale/regulation-config` → render màn (title "Khai Quy chế – Cấu hình"), sidebar **BÁN HÀNG**,
        đủ 7 nhóm tab (Chung/Báo giá–HĐ/Kỹ thuật/Chiết khấu/Tổ chức BH/Hàng hóa/Điều khoản)
      - Link menu trong nhóm "Quy chế - Thiết lập" trỏ `/sale/regulation-config` (đúng, duy nhất)
      - URL cũ `/master-data/regulation-config` → trang lỗi "Không tìm thấy trang yêu cầu"
      - (Toast "không có quyền / Lỗi khi tải cấu hình" là do phạm vi quyền user test, không phải routing)
- [x] Commit/push — DONE `6835afbbb` (đã `git pull --rebase origin gop_db` → Already up to date)

## Điều tra bug toggle "Ràng buộc lập HĐ theo loại" không đổi màu xanh trên server

- [x] Loại trừ esbuild CSS minify: compile SCSS + esbuild minify → `.tg.on .sw{background:var(--teal)}`
      và mọi biến `--teal` còn nguyên; specificity `.tg.on .sw` (0,3,0) > `.tg .sw` (0,2,0)
- [x] Xác nhận DEV chạy đúng: toggle ON = teal `rgb(15,158,140)`, OFF = xám `rgb(227,232,238)`
- [x] Verify lại trên LOCAL sau khi pull (2026-09-21): click "Dự án" → `on`, `sw` bg teal
      `rgb(15,158,140)`, knob `left:17px` ✓ → code mới nhất KHÔNG có lỗi
- [x] Kết luận: KHÔNG phải bug code. gop_db up-to-date, toggle commit `012665842` (2026-09-16) đã có.
      → Server đang chạy BẢN BUILD CŨ / CDN cache asset cũ. Cần rebuild + redeploy từ gop_db mới
      nhất và hard-refresh trình duyệt (Ctrl/Cmd+Shift+R).

### Checkpoint — 2026-09-21
Vừa hoàn thành: commit/push URL change `6835afbbb` + pull rebase (up to date) + verify toggle trên
local (đổi màu teal đúng) → xác nhận không phải bug code, nghi ngờ server chạy build cũ.
Đang làm dở: không.
Bước tiếp theo: user rebuild + redeploy server từ gop_db mới nhất, hard-refresh rồi test lại.
Blocked:

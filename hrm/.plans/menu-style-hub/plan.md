# Plan — menu-style-hub

Nhánh: `feature/menu-style-hub` (hrm-client). Không có thay đổi BE.

## Phase 1 — Nền tảng dùng chung

### FE
- [x] Tạo `components/subsystems.js` — registry 7 phân hệ HRM + ERP, chia 3 nhóm, trỏ `menu` vào mảng menu cũ
- [x] Tạo `components/subsystem-menu/hub.js` — `HUB_SUBSYSTEMS = ['assign','training']`, `deriveHubGroups`, lọc quyền, `normScreen`
- [x] Xử lý 2 mục menu Đào tạo gate theo vai trò (`roleCtx`) để rail hiện giống sidebar cũ

## Phase 2 — Sidebar kiểu hub (phần B)

### FE
- [x] Port `components/sale/SaleHubSidebar.vue` từ `gop_db`, đổi nguồn menu sang `hub.js`, nạp cờ vai trò cho Đào tạo
- [x] Port rút gọn `assets/scss/sale-theme.scss` — chỉ rail + topbar + panel menu, bỏ phần đổi style bảng/card
- [x] `layouts/default-sidebar.vue` — bật `SaleHubSidebar` cho phân hệ hub, gắn class `sale-theme`, lấy logo/tên phân hệ từ registry
- [x] `components/training-components/Sidebar.vue` — thêm prop `imgLogo` (dùng icon svg phân hệ thay icon font)

## Phase 3 — Màn chọn phân hệ + popup chuyển phân hệ (phần A, C)

### FE
- [x] Thay `layouts/system.vue` — nền navy gradient + 4 vệt sáng
- [x] Thay `pages/index.vue` — bố cục bông hoa, thêm biến thể `stage--duo` (2 nhóm → 2 cánh trái/phải) và nhị `st-s`
- [x] Port `components/SubsystemSwitcher.vue`, gắn vào `components/BasicSubsystem.vue` thay lưới card cũ

## Kiểm tra
- [x] Template 7 file `.vue` compile sạch (`vue-template-compiler`)
- [x] `sale-theme.scss` compile sạch (`node-sass`)
- [x] Giữ nguyên CRLF ở mọi file cũ bị sửa
- [ ] Chạy thật: `npm run dev` (Node 14.21.3) + rà 3 màn A/B/C — **chờ user xác nhận có test không**

### Checkpoint — 2026-08-17
Vừa hoàn thành: toàn bộ Phase 1-3, code xong trên nhánh `feature/menu-style-hub` (hrm-client).
Đang làm dở: chưa chạy thật trên trình duyệt.
Bước tiếp theo: user build FE bằng Node 14.21.3 và rà lại 3 màn; chốt bố cục bông hoa 2 cánh.
Blocked: không.

## Phase 4 — Gỡ conflict PR sang `gop_db` + vá bug rail Đào tạo

Nhánh `feature/menu-role-gate` (worktree `worktrees/menu-role-gate-client`), tách từ `origin/gop_db`.

### FE
- [x] Merge `origin/tpe-develop-assign` vào nhánh, giải quyết 7 file conflict bằng `--ours` (giữ bản gop_db) → cây kết quả giống hệt gop_db, 0 dòng đổi
- [x] Vá `hub.js::isScreenVisible` nhận `roleCtx`, xử lý 2 `isShow` dạng chuỗi của menu Đào tạo
- [x] `SaleHubSidebar.vue` nạp `roleCtx` (2 API) khi phân hệ là `training`
- [x] Ghi chú lý do `SubsystemHubOverview` không truyền `roleCtx`
- [x] Kiểm: template compile sạch, test tay `filterHubGroups` đúng 4 kịch bản vai trò
- [ ] User push nhánh + PR vào `gop_db`, sau đó đóng PR tpe-develop-assign → gop_db

### Checkpoint — 2026-08-17 (2)
Vừa hoàn thành: nhánh `feature/menu-role-gate` gồm 2 commit (merge ghi nhận lịch sử + bản vá roleCtx).
Đang làm dở: chưa push (chờ user).
Bước tiếp theo: `git push -u origin feature/menu-role-gate` rồi PR vào `gop_db`.
Blocked: không.

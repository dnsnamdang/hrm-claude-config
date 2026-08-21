# Plan — Redesign màn chọn phân hệ (style Base.vn)

## Phase 1 — Data registry (`components/subsystems.js`)
- [x] Thêm `tagline` cho 4 nhóm nghiệp vụ trong `SUBSYSTEM_GROUP_META`
- [x] Thêm `desc` cho ~24 phân hệ (theo bảng trong spec §5.2)
- [x] Thêm cờ `erpGhost: true` cho purchase / warehouse / transport

## Phase 2 — FE màn chọn phân hệ
- [x] ⚠️ VERIFY: đo codepoint `ri-*` v2.4.0 vs v4.3.0 → 26/26 LỆCH → KHÔNG dùng Remix font, chuyển sang SVG `image` tô trắng
- [x] Viết lại `pages/index.vue` (template 4 góc phần tư + dải giữa + top bar)
- [x] Style dark Base.vn (nền gradient, badge tròn, chip lõi/ERP, hexagon glow)
- [x] Xử lý badge ghost (mờ + openERP) + nút Đăng xuất inline SVG
- [x] Restyle `layouts/system.vue` (nền tối full-height, greeting vào top bar)
- [x] Responsive (>1024 / ≤1024 / ≤575)

## Phase 3 — Kiểm thử
- [x] Verify visual bằng mockup dùng chính SVG dự án (tô trắng) — render sắc nét, đúng look
- [x] ✅ User đã chạy app thật (Node 14) và xác nhận OK (2026-08-03)

## Phase 4 — Đổi bố cục sang BÔNG HOA (theo feedback user)
- [x] Nhụy tròn giữa: hexagon TP + vòng conic xoay + 3 nhị (lõi), BỎ ERP + bỏ chữ "LÕI HỆ THỐNG"
- [x] 4 cánh = 4 nhóm (panel kính mờ, mũi nhọn hướng tâm, màu riêng, tagline), bỏ số thứ tự nhóm
- [x] Mua hàng/Kho/Vận chuyển: bỏ mờ + desc riêng; click → toast "Tính năng đang phát triển" (thêm `erpLink` cho tương lai)
- [x] Hiệu ứng: glassmorphism, glow, gân nối tâm→cánh, float, hexagon pulse, ring xoay, hover
- [x] Verify desktop bằng mockup dùng SVG thật (nhiều vòng, đã duyệt concept)
- [x] Port sang pages/index.vue thật + responsive fallback (<1200 xếp dọc)

## Phase 5 — Popup chuyển phân hệ (SubsystemSwitcher) đồng bộ màn hoa
- [x] Dùng `shortLabel` (tên ngắn) + `desc` cho popup switcher
- [x] Hiện luôn Mua hàng/Kho/Vận chuyển (erpGhost, click → toast "đang phát triển"), BỎ nhóm ERP
- [x] Chia nhóm theo thứ tự Sơ đồ tổng thể, nền trắng
- [x] Đẩy dropdown ghim **sát mép phải màn hình** (`position:fixed; right:8px; top:66px` trong BasicSubsystem.vue)
- [x] Bỏ khoảng trống nhóm ít mục: đổi **grid 2 cột → multi-column** (`column-count:2` + `break-inside:avoid`) → nhóm xếp khít, không căn hàng
- [x] Icon + màu đúng màn hoa: **huy hiệu tròn màu nhóm** (svg trắng) + tiêu đề nhóm tô màu nhóm (dùng `SUBSYSTEM_GROUP_META`)
- [x] Verify bằng mockup switcher (trắng, sát phải, shortLabel, ghost, no ERP, badge màu, hết gap nội bộ)
- [x] v2 layout: mỗi nhóm **full-width**, phân hệ chia **3 cột trong nhóm** (grid) → hết mọi khoảng trống
- [x] Ghim popup **sát topbar** (`top:70px` = chiều cao topbar, `margin:0`)
- [x] Thêm **icon cho mỗi nhóm** (inline SVG kiểu Feather, tô màu nhóm) cạnh tiêu đề nhóm

### Checkpoint — 2026-08-03 (v2 — bông hoa)
Vừa hoàn thành: Port bố cục bông hoa vào pages/index.vue thật (4 cánh + nhụy 3 nhị + hexagon + conic xoay), cập nhật registry (desc 3 SX-CU, erpGhost không mờ + erpLink, toast đang phát triển), cập nhật toàn bộ tài liệu.
Đang làm dở: (không)
Bước tiếp theo: User chạy hrm-client (Node 14) đăng nhập → xem màn thật (desktop + thu nhỏ <1200); báo @junfoke về việc hiện lại Mua hàng/Kho/Vận chuyển.
Blocked: Môi trường phiên là Node 12, không chạy được Nuxt dev để test end-to-end (mới verify desktop qua mockup HTML dùng SVG thật).

## Phase 6 — Polish màn hoa + switcher (nhiều vòng feedback)
Màn hoa (`pages/index.vue` + `layouts/system.vue` + `components/subsystems.js`):
- [x] Bỏ hexagon → **điểm sáng** (spark: lõi trắng + tia chữ thập xoay + quầng + 2 sóng `ping`); nhụy thu nhỏ 344→250px
- [x] **2 vòng nhụy xoay NGƯỢC chiều** (ngoài conic 4 màu 15s + trong các cung sáng 8s reverse)
- [x] Lá **cách điệu almond** (mũi trong nhọn + mũi ngoài mềm + 2 hông cong) + **gân lá**; **viền lá = hiệu ứng ánh sáng** (gradient trắng→màu nhóm, mask-composite)
- [x] Nén chiều cao gói gọn **1 màn KHÔNG scroll** (stage 590, cánh 262); greeting **căn sát top** (`align-items:flex-start`) + gap; padding đáy 2 lá trên
- [x] Tăng tông **nền sáng**; sau đó lá về tối vừa (nền lá `0.05/0.03`), **box-shadow chỉ khi hover**
- [x] Bỏ tagline + bỏ số thứ tự nhóm; text ngắn theo mockup (`shortLabel` 9 mục + desc gọn)
- [x] **Icon nhóm** ở header cánh (dùng chung `SUBSYSTEM_GROUP_META[...].icon`); tăng tương phản chữ (`#c7d6ee`, `#b6c8e2`)

Popup switcher (`components/SubsystemSwitcher.vue` + `BasicSubsystem.vue`):
- [x] Layout cuối: mỗi nhóm full-width, phân hệ 3 cột/nhóm; icon nhóm; badge tròn màu nhóm; bỏ số thứ tự
- [x] Ghim **sát mép phải + sát topbar** (`top:66px` tuck để không hở); dùng chung icon nhóm với màn hoa

### Checkpoint — 2026-08-03 (v3 — polish) ✅ VERIFIED
Vừa hoàn thành: Toàn bộ polish màn hoa (spark, 2 vòng ngược chiều, viền ánh sáng, hình lá, fit 1 màn, icon nhóm, tương phản chữ, box-shadow hover, nền lá mờ hơn) + switcher (full-width nhóm/3 cột/icon nhóm/sát topbar-phải). Gom icon nhóm về `SUBSYSTEM_GROUP_META`.
**User đã chạy hrm-client thật và xác nhận DONE (2026-08-03).**
Đang làm dở: (không)
Bước tiếp theo: Merge/PR về `gop_db` khi sẵn sàng. ⚠️ Báo @junfoke về việc hiện lại Mua hàng/Kho/Vận chuyển (ghi đè "ẩn hẳn" của `bo-sung-menu-phan-he`).
Blocked: (không)

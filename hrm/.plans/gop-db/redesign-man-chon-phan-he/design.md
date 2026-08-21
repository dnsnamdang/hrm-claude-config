# Redesign màn chọn phân hệ (style Base.vn) — TÓM TẮT

**Nhánh:** `menu_phan_he_2026` (con `gop_db`) · **Phụ trách:** @namdangit · 2026-08-03
**Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-08-03-redesign-man-chon-phan-he-design.md`

## Mục tiêu
Đổi giao diện màn chọn phân hệ sau login (`pages/index.vue`) sang **bố cục BÔNG HOA** trên nền
xanh gradient tối: nhụy tròn ở giữa (lõi hệ thống), 4 cánh là 4 nhóm phân hệ, nhiều hiệu ứng
hiện đại. **Chỉ đổi trình bày**, registry `subsystems.js` vẫn là nguồn dữ liệu.

## Quyết định lớn (đã chốt)
1. **Bố cục bông hoa:** 4 nhóm nghiệp vụ = **4 cánh hình LÁ cách điệu** (kính mờ, mũi trong nhọn
   hướng tâm + mũi ngoài mềm + 2 hông cong + gân lá, màu riêng), xếp 4 góc; **nhụy tròn** ở giữa.
   Cánh xếp lưới cố định (HR trên-trái, VP số trên-phải, SX-CU dưới-trái, KD-TC dưới-phải).
   **Kích thước nén để vừa 1 màn, KHÔNG scroll** (stage 590px, cánh 250px, nhụy 250px, top bar sát trên).
   Tên nhóm hiển thị đơn (không số, không tagline).
2. **Nhụy (lõi):** đĩa tròn (~250px) với **2 vòng chạy NGƯỢC CHIỀU** (vòng ngoài conic 4 màu xoay
   thuận + vòng trong các cung sáng xoay ngược), **điểm sáng cách điệu** ở giữa (lõi trắng + tia
   sáng chữ thập xoay + quầng sáng pulse + sóng lan toả `ping`) + **3 nhị** = 3 phân hệ lõi (Thông
   tin NS, Danh mục, Quản trị). **KHÔNG có hexagon**, KHÔNG có ERP, KHÔNG có chữ "LÕI HỆ THỐNG".
3. **Tên nhóm:** chỉ hiển thị tên (VD NHÂN SỰ), **bỏ số thứ tự** "1./2./3./4." (strip khi hiển thị)
   và **bỏ tagline** dưới tên nhóm. (Dữ liệu `tagline` vẫn giữ trong `SUBSYSTEM_GROUP_META`,
   không render — dễ bật lại nếu cần.)
4. **Icon:** huy hiệu tròn màu theo nhóm + icon trắng. ⚠️ KHÔNG dùng `ri-*` (đã verify 26/26
   codepoint lệch giữa remixicon v2.4.0 bundled và v4.3.0 CDN → sai glyph, gotcha #4). Dùng field
   `image` (SVG có sẵn) tô trắng bằng `filter: brightness(0) invert(1)`. Nút Đăng xuất: inline SVG.
5. **Mô tả ngắn:** field `desc` cho từng phân hệ (viết sẵn trong spec).
6. **Hiệu ứng:** nền xanh **sáng**; mặt lá giữ tối vừa phải (glass mờ), **viền lá là hiệu ứng ánh
   sáng** — gradient trắng→màu nhóm chạy dọc cạnh lá (mask-composite, nửa còn lại để glow góc lộ ra);
   glassmorphism + backdrop blur, glow theo màu nhóm, gân lá, cánh trôi nổi (float), 2 vòng nhụy
   xoay ngược chiều, điểm sáng tia+quầng+sóng lan, hover nâng + sáng viền/icon.
7. **Icon nhóm:** mỗi header cánh có icon nhóm (inline SVG kiểu Feather, tô màu `--c2`) — dùng chung
   `SUBSYSTEM_GROUP_META[...].icon` với popup switcher (users/briefcase/package/trending-up, cpu=lõi).
8. **Tương phản chữ:** mô tả phân hệ `#c7d6ee`, phụ đề greeting `#b6c8e2` (sáng hơn, dễ đọc trên nền).
7. **⚠️ Mua hàng/Kho/Vận chuyển:** hiện **bình thường** (KHÔNG mờ) + tagline riêng, nằm trong
   cánh SX-CU. Là phân hệ quy hoạch bên ERP; **hiện chưa có link → click hiện toast "Tính năng
   đang phát triển"**; sau này gắn `erpLink` trỏ dashboard phân hệ bên ERP. Cờ `erpGhost` (vẫn
   `hidden` với dropdown/phân quyền) — **ghi đè có chủ đích** quyết định "ẩn hẳn" của
   `bo-sung-menu-phan-he` (@junfoke). **Cần báo lại @junfoke.**

## File tác động
- `components/subsystems.js` — thêm `tagline` (group meta), `desc` (mỗi phân hệ), `erpGhost` +
  `erpLink` (Mua hàng/Kho/Vận chuyển).
- `pages/index.vue` — viết lại template + style bố cục bông hoa (4 cánh + nhụy 3 nhị + hexagon +
  vòng conic xoay); icon dùng SVG `image` tô trắng; erpGhost click → toast "đang phát triển".
- `layouts/system.vue` — nền tối full-height, greeting trong top bar index.vue (chỉ index.vue dùng).

## Ngoài phạm vi
Không đổi logic điều hướng/permission/menu, không đổi BE/DB, không đổi topbar/sidebar sau khi vào phân hệ.

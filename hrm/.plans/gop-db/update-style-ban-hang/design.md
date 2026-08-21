# Update style phân hệ Bán hàng — theo MISA (tóm tắt)

**Nhánh:** `gop_db` · **Phụ trách:** @namdangit · 2026-08-05
**Trạng thái:** ✅ Design đã duyệt (2026-08-06)
**Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-08-05-update-style-ban-hang-design.md`

## Mục tiêu
Đổi giao diện các màn phân hệ Bán hàng (app thật `hrm-client`, `pages/assign/*`) theo **style MISA**.
Chỉ Bán hàng trước, thiết kế để **nhân rộng phân hệ khác sau**.

## Cách làm — Cách A: lớp `sale-theme` scope riêng
- **Gate 1 chỗ:** `layouts/default-sidebar.vue` thêm `:class="{ 'sale-theme': isSaleSubsystem }"` (computed đã có) → bao trùm màn Bán hàng, tắt ở phân hệ khác.
- **1 file:** `assets/scss/sale-theme.scss` — mọi override MISA dưới `.sale-theme`, tokens màu (CSS vars) ở đầu file. KHÔNG sửa component V2 dùng chung.
- **Palette baseline** (từ demo kế toán): header `#aae1e6` / chữ `#0f3d44` · hover `#d1fae5` · accent teal. Tinh chỉnh theo note.

## Working mode
Tăng dần: user note từng phần (kèm ảnh MISA) → style dưới `.sale-theme` → verify Playwright → phần tiếp.
Phase 0: setup (gate class + file scss + tokens + import).

## Nhân rộng sau
Bỏ gate (áp toàn app) hoặc bê tokens vào V2 component — không viết lại.

## Quyết định đã chốt
- Target: app thật · Style: MISA · Scope: chỉ Bán hàng (portable) · Palette nền: demo kế toán teal.

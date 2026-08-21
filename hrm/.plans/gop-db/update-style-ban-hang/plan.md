# Update style phân hệ Bán hàng (MISA) — Implementation Plan

**Goal:** Đổi giao diện các màn phân hệ Bán hàng (`hrm-client`, `pages/assign/*`) sang style MISA, scope riêng qua lớp `.sale-theme`, không đụng phân hệ khác.

**Architecture:** Gate `.sale-theme` ở `layouts/default-sidebar.vue` (computed `isSaleSubsystem` có sẵn) → mọi override MISA nằm trong 1 file `assets/scss/sale-theme.scss` dưới `.sale-theme`. KHÔNG sửa component V2 dùng chung. Tăng dần theo phần user note, verify Playwright.

**Tech Stack:** Nuxt 2 / Vue 2, SCSS, bộ component V2Base dùng chung, Playwright (verify), Node 12 + heap 8GB (dev server).

## Global Constraints
- KHÔNG sửa component V2 dùng chung (`components/V2Base*.vue`) — chỉ override CSS dưới `.sale-theme`.
- KHÔNG đổi markup/logic (chỉ CSS). Nếu 1 phần buộc đổi markup → hỏi user trước.
- KHÔNG commit/push git (quy tắc dự án).
- KHÔNG ảnh hưởng phân hệ khác — mỗi phần verify thêm 1 màn phân hệ khác giữ nguyên style.
- Palette baseline (tokens): header `#aae1e6` · chữ header `#0f3d44` · hover row `#d1fae5` · accent teal. Chỉnh theo note.
- Verify bằng Playwright trên app thật (dev server nuxt Node 12, `NODE_OPTIONS=--max-old-space-size=8192`).
- Tránh `!important` trừ khi buộc phải (theme UBold nhiều selector id) — ưu tiên tăng độ đặc hiệu bằng `.sale-theme` + class thật.

---

## Phase 0 — Setup scaffold `sale-theme` (làm 1 lần, chưa đổi giao diện)

### Task 0.1: Gate class `.sale-theme` ở layout
**Files:** Modify `layouts/default-sidebar.vue` (div gốc `.training-layout`)
- [x] Thêm `:class="{ 'sale-theme': isSaleSubsystem }"` vào div gốc layout (`isSaleSubsystem` đã có computed). ✅ dòng 2.
- [ ] Verify Playwright: vào 1 màn Bán hàng (`/assign/solutions`) → `document.querySelector('.training-layout.sale-theme')` tồn tại; vào màn phân hệ khác → KHÔNG có `.sale-theme`. ⏳ chờ dev server.

### Task 0.2: Tạo file `assets/scss/sale-theme.scss` + tokens
**Files:** Create `assets/scss/sale-theme.scss`
- [x] Tạo file với khối tokens (CSS vars) trên `.sale-theme` + bố cục comment sẵn cho các phần (bảng / filter / nút / badge / card / topbar): ✅ đã tạo.
```scss
/* ===== Style MISA — CHỈ áp cho phân hệ Bán hàng (dưới .sale-theme) =====
   Nhân rộng sau: bỏ scope .sale-theme hoặc bê tokens vào component V2. */
.sale-theme {
    /* Tokens — chỉnh 1 chỗ, là đầu mối khi nhân rộng */
    --sale-header-bg: #aae1e6;
    --sale-header-fg: #0f3d44;
    --sale-row-hover: #d1fae5;
    --sale-accent: #12a594;
    --sale-line: #e5e7eb;
}
/* ---- Bảng (V2BaseDataTable) ---- */
/* (điền khi làm phần Bảng) */
/* ---- Filter (V2BaseFilterPanel) ---- */
/* ---- Nút / Badge ---- */
/* ---- Card / Topbar ---- */
```

### Task 0.3: Import `sale-theme.scss`
**Files:** Modify `layouts/default-sidebar.vue` (`<style lang="scss">` non-scoped)
- [x] Thêm `@import '~/assets/scss/sale-theme.scss';` trong khối `<style lang="scss">` của layout — đặt **top-level** (không lồng `.training-layout`) vì `.sale-theme` khớp chính element gốc. ✅
- [ ] Verify Playwright: màn Bán hàng đọc được CSS var — `getComputedStyle(document.querySelector('.sale-theme')).getPropertyValue('--sale-header-bg')` = `#aae1e6`. Chưa có thay đổi hình ảnh (đúng — mới có tokens). ⏳ chờ dev server.

### Task 0.4: Regression check Phase 0
- [ ] Playwright: 1 màn Bán hàng + 1 màn phân hệ khác — không màn nào đổi hình ảnh; console không lỗi mới; build không lỗi. ⏳ chờ dev server.

---

## Phase 1+ — Style từng phần (cụ thể hoá khi user note)

> Mỗi phần user note (kèm ảnh MISA) → thêm 1 Task dưới đây, quy trình chuẩn:
> 1. Đọc markup + class thật của thành phần (trong `pages/assign/*` + component V2 tương ứng).
> 2. Viết override dưới `.sale-theme` trong `sale-theme.scss` (dùng tokens).
> 3. Verify Playwright: chụp so với ảnh MISA + kiểm computed style.
> 4. Regression: 1 màn phân hệ khác giữ nguyên.
> 5. User duyệt → phần tiếp.

### Backlog các phần (chờ user note ảnh MISA + chốt từng cái)
- [ ] Bảng dữ liệu (`V2BaseDataTable`): header, hover row, border, zebra, sticky, sort icon…
- [ ] Filter panel (`V2BaseFilterPanel`): nền, ô input, nút áp dụng/nhập lại, bố cục.
- [ ] Nút (`V2BaseButton` + `btn` bootstrap): primary/secondary/light, icon-btn, kích thước.
- [ ] Badge / trạng thái (`V2BaseBadge`, status pills).
- [ ] Card / section (`tp-card`, section title/subtitle).
- [ ] Topbar / breadcrumb khu vực Bán hàng (⚠️ cân nhắc đồng bộ accent teal vs rail tím — hỏi user).
- [ ] Phân trang, empty state, khoảng cách/spacing tổng thể.

*(Danh sách trên là ứng viên; chỉ làm phần nào user note, theo đúng ảnh MISA cung cấp.)*

---

### Checkpoint — 2026-08-06 (wrap up — trước khi code)
Vừa hoàn thành: brainstorm xong; **design + spec + plan đã duyệt**. Chưa viết code (Phase 0 chưa bắt đầu).
Đang làm dở: (chưa code) — plan sẵn sàng, Phase 0 (Task 0.1–0.4) là bước code đầu tiên.
Bước tiếp theo: thực thi **Phase 0** (gate `.sale-theme` ở `default-sidebar.vue` + tạo `assets/scss/sale-theme.scss` + tokens + import + verify Playwright). Sau đó **chờ user note phần đầu tiên** (ảnh MISA + tên màn/thành phần).
Blocked: (không) — chờ lệnh chạy Phase 0 / hoặc note phần đầu tiên.

Ghi chú môi trường: dev server nuxt vẫn chạy nền (Node 12, heap 8GB, port 3000) để verify Playwright khi code.

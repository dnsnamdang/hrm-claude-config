# Plan — filter-panel-inline-buttons

Người phụ trách: @khoipv

## Phase 1 — Đưa nút Tìm kiếm/Làm mới lên cùng dòng ô tìm kiếm nhanh (V2BaseFilterPanel)

Yêu cầu: mọi chỗ dùng `V2BaseFilterPanel` chuyển 2 nút "Tìm kiếm", "Làm mới" lên cùng dòng với ô input tìm kiếm nhanh — tham khảo layout popup "Thêm hàng hoá" ở `pages/assign/bom-list` (BomBuilderAddProductModal: input + nút cùng 1 hàng, nút căn phải).

### Tasks

- [x] 1. Đổi mặc định prop `inlineSearchButtons` của `V2BaseFilterPanel.vue` từ `false` → `true` (áp dụng toàn bộ 73 file đang dùng base, không cần sửa từng màn)
- [x] 2. Fallback cho màn tắt quick search (`:show-quick-search="false"` — 10 màn report): nút vẫn hiển thị ở hàng dưới khi mở panel lọc (giữ hành vi cũ, không mất nút)
- [x] 3. Chuẩn button-convention: nút "Làm mới" đổi `secondary` → `tertiary` (nhóm Reset/Phụ trợ), khai báo `size="sm"` cho các nút trong component
- [x] 4. Verify: parse + compile template SFC bằng vue-template-compiler → PASS (dev server không chạy nên chưa verify browser)

## Phase 2 — Tinh chỉnh khoảng cách theo feedback UI (user gửi screenshot)

- [x] 5. Giảm khoảng cách hàng tiêu đề ↔ hàng ô tìm kiếm trong V2BaseFilterPanel: `mb-2` (8px) → chốt 6px (qua 2 vòng feedback: 4px → 2px → user kêu sát quá → 6px)
- [x] 6. Giảm padding dọc card bộ lọc `p-3` → `px-3 py-2` + margin dưới hàng tìm kiếm `mb-2` → `mb-1`
- [x] 7. Các màn module Assign (wrapper `v2-styles min-vh-100 pt-2 > container-fluid`, ~50 màn) đang rộng hơn /assign/dashboard → thêm override trong `assets/scss/v2-styles.scss`: bỏ `pt-2` (padding-top: 0) + bỏ padding ngang 15px của container-fluid con → khớp padding layout như dashboard (5px + 5px mỗi bên)
- [x] 8. Verify: node-sass compile v2-styles.scss PASS; vue-template-compiler PASS (Phase 1). Chờ user verify browser.

### Checkpoint — 2026-07-15

Vừa hoàn thành: toàn bộ Phase 1 — sửa duy nhất `hrm-client/components/V2BaseFilterPanel.vue` (default `inlineSearchButtons=true`, fallback hàng dưới khi `showQuickSearch=false`, Làm mới → tertiary + size="sm").
Đang làm dở: (không)
Bước tiếp theo: user hard-refresh + verify browser bằng mắt 1 màn thường (vd /assign/customers) + 1 màn report (vd /assign/report/performance-by-employee).
Blocked: (không)

# Design (tóm tắt) — Menu hub cho phân hệ Quản lý công việc (assign)

- **Nhánh:** `gop_db` (client) · **Phụ trách:** @namdangit · **Ngày:** 2026-08-10
- **Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-08-10-menu-quan-ly-cong-viec-design.md`

## Mục tiêu
Đưa phân hệ **Quản lý công việc** (`assign`) sang sidebar kiểu **hub navy+teal** giống 14 phân hệ mới, giữ nguyên toàn bộ menu nghiệp vụ.

## Quyết định chính
1. **Kích hoạt hub:** thêm `'assign'` vào `HUB_SUBSYSTEMS` (`components/subsystem-menu/hub.js`) → `default-sidebar.vue` tự render `SaleHubSidebar` + `.sale-theme`.
2. **Màn lẻ cấp 1 → nút rail đi thẳng** (chốt): thêm `deriveHubNavLinks` + `hubNavLinksFor` (hub.js) và render nút `router-link.cat.cat-nav` sau "Tổng quan" trong `SaleHubSidebar.vue`. Giữ được 3 màn: Lịch làm việc của tôi (`/assign/my-todo`), Công việc của tôi (`/assign/my-job`), Cập nhật tiến độ Task (`/assign/tasks/daily-report`). KHÔNG đổi mảng `groups` → không ảnh hưởng phân hệ hub khác.
3. **6 nhóm ERP chưa có link** → hiện xám mờ (tự động, không code thêm).

## Phase 2 — Đào tạo (training)
Tái dùng nguyên hạ tầng Phase 1. `training` dùng `layout: 'default-sidebar'`, `menuItemsTraining` toàn mục có `subItems` (trừ "Tổng quan" → `/training/dashboard`, đã có nút built-in) → `hubNavLinksFor` trả `[]`. **Chỉ cần thêm `'training'` vào `HUB_SUBSYSTEMS`** (1 dòng). Verify: rail "ĐÀO TẠO" + 12 nhóm, panel bung OK.

## Ngoài phạm vi
- Trang overview `/assign/dashboard`, `/training/dashboard` render lưới tile kiểu hub (giữ nguyên, làm sau nếu cần).

## File đụng
- `components/subsystem-menu/hub.js` (assign + training + hạ tầng nav-link)
- `components/sale/SaleHubSidebar.vue` (render nút rail lẻ)

## Trạng thái
ĐÃ COMMIT + PUSH lên `gop_db` (2026-08-10). Verify Playwright 1440 đạt cho cả assign + training.

## Kiểm thử
Playwright 1440px: rail navy + 3 nút lẻ đi thẳng + nhóm mở panel + ERP xám mờ; regression check phân hệ Bán hàng không đổi.

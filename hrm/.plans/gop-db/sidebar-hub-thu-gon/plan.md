# Plan — Sidebar hub thu gọn mặc định (@namdangit)

## Phase 1 — FE (hrm-client, gop_db)
- [x] Đo hành vi sidebar MISA ActApp + sidebar hub hiện tại (Playwright)
- [x] Chốt logic 6 điểm với user
- [x] layouts/default-sidebar.vue: hubPinned/hubForceOpen, applyHubSidebar, toggleHubPin, localStorage, màn hẹp, rời hub trả trạng thái (cờ `_hubOwnsSize`)
- [x] SaleHubSidebar.vue: rail fixed khi condensed, hover/.is-held bung 220px đè nội dung, chữ nowrap + "…", bỏ tự mở rộng lúc mounted, watch open ⇒ trackRail
- [x] sale-theme.scss: content-page lùi 58px (sửa đè 3px)
- [x] SidebarMenu.vue: `:title` nút ☰
- [x] Popup xác nhận khi bấm ☰ ($confirm), đổi chú thích "Tắt/Bật thu gọn menu"
- [x] Kiểm Playwright: mặc định · hover · rời · panel giữ bung · ghim/bỏ ghim + tải lại · confirm Hủy/Xác nhận 2 chiều · ?sidebar=open · 900px · cuộn · hub ⇒ layout khác
- [x] Commit + push gop_db (client `c3b1584cd`)
- [ ] User nghiệm thu local ⇒ pull prod (không migration)
- [ ] (tuỳ chọn) chạy 5 spec e2e có bấm rail hub khi có tài khoản e2e

### Checkpoint — 23/10/2026
Vừa hoàn thành: toàn bộ Phase 1, đã push gop_db (client `c3b1584cd`; cùng đợt `2be9eefd0` bảng phiếu tính giá)
Đang làm dở: —
Bước tiếp theo: user nghiệm thu trên local ⇒ pull lên prod
Blocked: e2e không chạy được trên `hrm_erp_21_10_prod` (chưa có tài khoản e2e)

# Sidebar hub thu gọn mặc định + rê chuột bung (kiểu MISA)

**Người phụ trách:** @namdangit · **Nhánh:** `gop_db` (hrm-client) · **Trạng thái:** ĐÃ PUSH 23/10/2026 (client `c3b1584cd`), chưa pull prod
**Spec chi tiết:** `docs/superpowers/specs/gop-db/2026-10-23-sidebar-hub-thu-gon-design.md`

## Mục tiêu
Sidebar kiểu hub (`SaleHubSidebar`, các phân hệ trong `HUB_SUBSYSTEMS`) mặc định ẩn còn cột icon, rê chuột thì bung — như MISA ActApp
(`actapp.misa.vn`). Sidebar cây của phân hệ cũ KHÔNG đổi.

## Số đo MISA (Playwright, 23/10)
Rail 64px, hover bung 220px **đè** nội dung (wrapper giữ 64px, container `absolute` z 100), `width .2s cubic-bezier(.4,0,.2,1)`,
không trễ khi vào/ra; menu con flyout giữ menu bung khi chuột còn trong flyout; nút ⇥ ở đáy để đổi chế độ.

## Quyết định đã chốt (user 23/10)
1. Mặc định (chưa ghim): rail 58px, nội dung lùi 58px. Rê chuột ⇒ 220px đè nội dung; rời ⇒ thu. Đang mở panel menu con ⇒ giữ bung tới khi đóng.
2. Nút ☰ trên topbar ở màn hub = bật/tắt thu gọn. Tắt thu gọn = ghim 220px đẩy nội dung như cũ, không hover.
   **Mỗi lần bấm hỏi lại bằng popup chung** (`$confirm` → `base-confirm-modal`): "Tắt thu gọn menu" / "Bạn chắc chắn tắt chế độ thu gọn menu?"
   và "Bật thu gọn menu" / "Bạn chắc chắn bật chế độ thu gọn menu?"; Hủy giữ nguyên. Chú thích rê vào ☰ trùng tiêu đề popup.
3. Nhớ lựa chọn ở localStorage `hub-sidebar-pinned` = '1', chung MỌI phân hệ hub, giữ qua đổi màn/tải lại/đăng xuất.
4. Sang phân hệ cũ (hoặc layout khác): trả `data-sidebar-size` về mặc định — sidebar cũ không dính lựa chọn.
5. `?sidebar=open`: mở cho lần tải đó, không ghi đè lựa chọn đã lưu.
6. Màn < 992px: giữ cách cũ (☰ bật/tắt menu trượt), không thu gọn/hover.
7. Sửa kèm: theme để `.content-page` lùi 55px khi condensed trong khi rail 58px ⇒ rail đè mép trái 3px (chỉ màn hub).

## File
`layouts/default-sidebar.vue` (trạng thái + ☰ + confirm) · `components/sale/SaleHubSidebar.vue` (CSS hover/is-held, bỏ đoạn tự mở rộng lúc mounted, watch `open` ⇒ trackRail) ·
`assets/scss/sale-theme.scss` (margin 58px) · `components/training-components/SidebarMenu.vue` (`:title` nút ☰).

## Còn lại / ghi nhận
- Chưa nhìn tận mắt sidebar phân hệ cũ (tài khoản kiểm không có quyền, ra 404) — chỉ đo được `data-sidebar-size` đã trả về rỗng.
- E2E chưa chạy; 5 spec bấm `.sale-cats .cat` theo tên (internal-price-policy, master-data-hub-menu, product-catalog-ui, meeting-room, meeting-room-board) — đã thử đúng thao tác khi rail thu gọn, panel vẫn mở.
- Có từ trước, chưa sửa: màn < 992px rail hub vẫn hiện 220px trong khi nội dung không lùi (`.sale-cats { display:flex }` đè `display:none` của theme).

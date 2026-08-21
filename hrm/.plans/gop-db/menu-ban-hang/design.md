# Menu phân hệ Bán hàng — kiểu MISA (master-detail)

**Nhánh:** `menu_phan_he_2026` (con `gop_db`) · **Phụ trách:** @namdangit · 2026-08-04
**File menu hiện tại:** `hrm-client/components/subsystem-menu/sale.js` (do `bo-sung-menu-phan-he` dựng)
**Bảng cấu trúc (artifact):** https://claude.ai/code/artifact/1d3e6d03-001f-4685-9d9c-0ba7ece85418
**Mockup style (đã duyệt):** `.plans/gop-db/menu-ban-hang/menu-mockup.html`

## Mục tiêu
Thay menu Bán hàng từ **sidebar tree** hiện tại → **trang menu master-detail kiểu MISA AMIS Báo cáo**.
CHỈ áp dụng cho phân hệ Bán hàng, **không ảnh hưởng menu các phân hệ khác**.

## Cấu trúc menu (đã chốt qua khảo sát ERP Khởi tạo + Kinh doanh)
10 nhóm **cấp 1** (+ Tổng quan): Dự án TKT · Bán hàng · Bán dịch vụ · Yêu cầu · Tra cứu - Thông báo ·
Báo cáo · Kế hoạch · Danh mục · Phê Duyệt · Quy chế - Thiết lập.
- Cây tối đa **4 cấp**: Nhóm (cấp1) → Mục (cấp2) → Nhóm con (cấp3) → Màn (cấp4). Ví dụ 4 cấp: Báo cáo → Báo cáo bán hàng → Doanh số-Doanh thu/Thưởng/Thực hiện KH/… → từng báo cáo.
- Nguồn dữ liệu: chỉ lấy ERP **Khởi tạo + Kinh doanh** (không kéo menu ERP khác). Danh mục bổ sung ERP Danh mục>Dịch vụ. Đã bỏ: Báo giá mẫu, Báo giá HĐ nguyên tắc, Nha khoa, Quản lý giá-CTKM (thuộc Kế toán), Khách hàng (Danh mục).

## Style (kiểu MISA Báo cáo — đã duyệt qua mockup)
- **Layout master-detail thích ứng:**
  - Cột trái = **cấp 1** (nền trắng, icon + nhãn, active vạch teal).
  - Nhóm **nhiều con (≥5 cấp 2)** → cột giữa = **cấp 2** (nền tint, active teal đậm), click → cột phải hiện cấp 3/4.
  - Nhóm **ít con (<5 cấp 2)** → hiện thẳng: cấp 2 là section header + cấp 3 lưới (như hiện tại).
  - Cấp 3 (section) = tiêu đề teal in hoa + marker + badge số; Cấp 4 = hàng mục lưới 2 cột.
- Phân biệt rõ 4 cấp bằng style (cột trắng / cột tint / header teal / hàng mục).
- Nền trắng, accent teal (chốt màu cuối khi implement: teal MISA vs tím hệ thống).

## Tính năng (theo yêu cầu user)
- **CÓ:** Tìm kiếm (lọc màn theo tên toàn menu) · Yêu thích (sao ⭐ toggle, lưu localStorage) · Gần đây (tự ghi màn vừa mở, localStorage).
- **BỎ:** tính năng ghim riêng (dùng Yêu thích thay thế) · Ẩn/hiện mục.

## Nguyên tắc kỹ thuật
- **Icon:** bổ sung icon phù hợp cho từng nhóm/mục — dùng **inline SVG** (tránh xung đột codepoint Remix Icon, xem feature redesign-man-chon-phan-he).
- **Không đụng** `components/Sidebar.vue` (dùng chung) và menu phân hệ khác. Tạo component + route riêng cho Bán hàng.
- **Giữ `link` trên màn leaf** để `subsystems.js` (`resolveSubsystem`/`findSubsystemByLink`) vẫn map route → phân hệ Bán hàng đúng.
- Màn chưa có link (chạy ERP) → click hiện toast/mở ERP như hiện hành (`erpGhost`/xám mờ).

## ⏳ Chốt khi implement
- Màu accent (teal vs tím) · nhóm nào cần lên 4 cấp ngoài Báo cáo bán hàng · route landing của phân hệ Bán hàng.

---

## ✅ Kết quả triển khai cuối (2026-08-04) — đã verify Playwright trên app thật

Ý tưởng ban đầu (hub full-page tại `/sale/dashboard`) đã **tiến hóa** theo phản hồi user thành **menu MISA đồng nhất trên MỌI màn phân hệ Bán hàng** (không chỉ landing).

**Kiến trúc cuối:**
- **1 nguồn dữ liệu:** `components/subsystem-menu/sale-hub.js` (`saleHubGroups`, 10 nhóm, tối đa 4 cấp) → sinh ra `saleItems` qua `buildSaleTree()` trong `sale.js` (cho `resolveSubsystem`). Gắn 8 report link `/assign/report/*` + 2 erpPath vào hub. Giữ gate quyền qua `SALE_LINK_PERMISSIONS`.
- **Sidebar MISA:** `components/sale/SaleHubSidebar.vue` = cột **cats** (10 nhóm cha, icon+chữ, marker tím) cố định + panel **detail** rộng **1180px** bay ra khi click nhóm (tái dùng logic render mockup: lưới 2 cột, nav-mode cho nhóm ≥5 mục, flatten cấp4→cấp3). Chọn màn có link → `router.push` + đóng panel; erpPath → mở ERP; chưa có → toast. Có Tìm kiếm/Yêu thích/Gần đây (localStorage chung `sale_hub_fav`/`sale_hub_recent`). ESC/backdrop đóng.
- **Gate layout:** `layouts/default-sidebar.vue` — `resolveSubsystem(route).key==='sale'` → render `SaleHubSidebar` thay `SideBar`; phân hệ khác GIỮ NGUYÊN tree cũ. (KHÔNG sửa `Sidebar.vue` chung.)
- **Màn Tổng quan** `/sale/dashboard`: đổi sang layout `default-sidebar` → dùng CHUNG rail (sidebar đồng nhất). Nội dung = trang overview (hero + lưới 10 thẻ nhóm bấm mở panel qua `$root` event + Gần đây/Yêu thích). Mục cấp 1 "Tổng quan" ở đầu rail (trên Dự án TKT).
- **Thu gọn sidebar (condensed 58px):** rail chỉ còn icon; panel `left` bám mép qua `MutationObserver`+`requestAnimationFrame` (bám theo từng frame → trượt mượt, không nhảy/hở); toggle 1-click (sync `isMenuCondensed`).

**Quyết định thực tế:** accent = **tím** (theo nhóm Kinh doanh–Tài chính, đồng bộ hub) — không dùng teal của mockup. Chỉ "Báo cáo bán hàng" là 4 cấp (tree flatten về 3, panel giữ đủ 4).

**Component cũ không còn dùng:** `SaleMenuHub.vue`, `pages/sale/menu/` (rail thay thế) — giữ file, dọn sau.

**Chi tiết từng bước + verify:** xem các checkpoint trong `plan.md` (Phase 8, 9 + các checkpoint bổ sung).

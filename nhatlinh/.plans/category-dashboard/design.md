# Dashboard phân hệ Danh mục — Design (tóm tắt)

> Spec chi tiết: `docs/superpowers/specs/2026-07-03-category-dashboard-design.md`
> Người phụ trách: @manhcuong · Tạo: 2026-07-03

## Mục tiêu

Trang tổng quan phân hệ Danh mục, hướng **tổng quan + chất lượng dữ liệu**: đếm nhanh các danh mục chính, nhìn phân bố hàng hoá/NCC, và phát hiện danh mục khai báo dở dang (hàng SX chưa BOM, hàng chưa giá, chưa min_stock, KH/NCC thiếu liên hệ).

## Scope

- BE: `CategoryDashboardService` + 1 endpoint `GET /v1/category/dashboard` (sửa DashboardController stub có sẵn). Không tham số, không filter.
- FE: thay stub `pages/category/dashboard.vue` — 5 KPI card, 4 chart ApexCharts (nhóm hàng, phân loại+trạng thái donut, NCC theo nhóm, hãng SX⇄xuất xứ toggle), khối cảnh báo 4 tab (mỗi tab ≤10 dòng + count tổng).
- KHÔNG: đổi DB, scope theo cấp, filter ngày/công ty, thống kê hoạt động gần đây.

## Các quyết định lớn

1. **Permission mới 1142** "Xem dashboard danh mục" (type=8, nhóm "Danh mục chung") — thêm seeder, gắn `checkPermission` vào route; số liệu KHÔNG co giãn theo cấp (danh mục là dữ liệu chung).
2. **Cảnh báo chỉ tính bản ghi Hoạt động** (status=1); hàng SX chưa BOM = không có BOM `status=1` (ACTIVE); hàng chưa giá = không có ĐVT cơ bản `price_p0 > 0`.
3. **Menu**: mục "Tổng quan" có sẵn trong `default-menu/category.js` → thêm `isShow` quyền 1142; `/category` redirect sang dashboard khi có quyền, không quyền giữ trang welcome.
4. 1 endpoint aggregate theo pattern WhDashboardService/SaleDashboardService.

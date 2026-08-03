# Dashboard Kho — Tóm tắt

- **Ngày:** 2026-07-02 · @manhcuong
- **Phân hệ:** Quản lý kho — `Modules/Warehouse` (BE) + `pages/warehouse/dashboard` (FE)
- **Spec đầy đủ:** `docs/superpowers/specs/2026-07-02-warehouse-dashboard-design.md`

## Mục tiêu
Trang tổng quan phân hệ kho, **chỉ số lượng** (không tiền), **không scope theo cấp** (có quyền là thấy hết).

## Khối nội dung
1. **KPI chờ duyệt**: phiếu Nhập / Xuất / Chuyển `status=2` (link màn duyệt).
2. **KPI tổng quan**: số kho · mặt hàng đang có tồn · hàng đã hết.
3. **Nhập/Xuất theo thời gian**: bar 2 series, toggle **Tuần/Tháng/Quý/Năm** (chỉ type 1 nhập & 2 xuất, loại chuyển kho).
4. **Top xuất / Top nhập**: 2 bar ngang top 10, dùng chung khoảng ngày (mặc định đầu năm→nay).
5. **Cảnh báo tồn thấp**: tổng tồn toàn hệ thống < `min_stock` (mỗi hàng 1 dòng).
6. **Tồn theo kho**: mỗi kho → số mặt hàng + tổng SL.

## Quyết định lớn
- **BE**: 1 endpoint `GET /v1/warehouse/dashboard` (`WhDashboardService`), params `granularity`, `top_from`, `top_to`. Không filter chung — mỗi box tự có control.
- **Schema**: thêm `min_stock DECIMAL(18,2) NULL` vào `products` (ĐVT cơ bản) + sửa form/request/resource Category.
- **Permission**: mới `1138 — Xem dashboard kho` (type=10), gate route + menu.
- **Menu**: thêm "Tổng quan" đầu sidebar kho, route `/warehouse/dashboard`.

## Ngoài phạm vi (YAGNI)
Không export, không drill-down, không realtime/cache, không tiền, không scope cấp, không cảnh báo tồn theo từng kho, không lọc loại hàng.

## Trạng thái (2026-07-02)
CODE HOÀN THÀNH 8/8 task + final review pass (1 Critical đã fix: ProductService bỏ sót lưu min_stock — build mảng thủ công nên thêm fillable không đủ). Điều chỉnh thực tế so với plan gốc: xem §9 spec chi tiết. Còn: user migrate + seed quyền 1138 + test trình duyệt + commit.

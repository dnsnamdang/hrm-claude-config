# Plan — Hoạt động kho

> Phụ trách: @khoipv · nhánh `develop` (con của `gop_db`, cả hrm-api + hrm-client)
> Port ERP `warehouseInfo.activities` (Kho › Hoạt động kho) → HRM `/warehouse/activities`.
> Khuôn: màn chỉ đọc cùng controller ERP "Danh sách hàng mượn" (`pages/finance/borrow-stocks`), Excel theo
> `pages/warehouse/self-inventories/components/export-excel.js`, khối tổng hợp theo `self-inventory-report`.

## Quyết định (user chốt 26/10/2026)

- Quyền: KHÔNG gate quyền, y ERP. Phạm vi = kho mình là thủ kho (`warehouse_stockers`), Super Admin mọi kho.
- Realtime ERP đã chết (socket bị comment) → port ô tổng hợp + tô màu theo thời gian chờ, tự tải lại 60 giây.
- Bộ tối thiểu HRM: ô tìm nhanh mã phiếu, Cấu hình cột, Xuất Excel. Không phân trang, không lọc nâng cao.
- Cột "Phiếu đề nghị" link sang màn HRM (ĐNXK `/finance/warehouse-export-requests/{id}`, ĐNNK `/warehouse/import-requests/{id}`), tab mới.

## Phase 1 — Port màn

### BE
- [x] `WarehouseActivityService` — UNION ĐNXK + ĐNNK y `Warehouse::getActivities()` ERP, keyword, sort whitelist, summary
- [x] `WarehouseActivityController` + route `GET /v1/finance/warehouse-activities` (không checkPermission)
- [x] Đối chiếu số dòng với SQL ERP nguyên văn

### FE
- [x] `pages/warehouse/activities/index.vue` (bảng + tìm nhanh + cấu hình cột + tự tải lại 60s + tô màu dòng)
- [x] `components/ActivitySummary.vue` (Tổng phiếu nhận / Hoàn thành / Chưa xử lý)
- [x] `components/export-excel.js` (letterhead + khối ký)
- [x] Menu Kho › mục "Hoạt động kho"
- [x] Compile + gọi API kiểm

### Checkpoint — 26/10/2026
Vừa hoàn thành: BE + FE Phase 1. Số dòng khớp SQL ERP nguyên văn trên DB local (Super Admin 219 = 173 ĐNXK + 46 ĐNNK; thủ kho kho 2 = 128);
keyword + sort qua HTTP kernel 200 (~250-420ms); nhánh "Đã hoàn thành" + "Tổng thời gian xử lý" thử bằng dòng giả (DB không có phiếu xong trong ngày).
FE parse sạch (vue-template-compiler + babel), grep tự kiểm của skill sạch.
Đang làm dở: —
Bước tiếp theo: user bật dev server, mở `/warehouse/activities` bấm thật (tìm nhanh, sort, Cấu hình cột, Xuất Excel, link mã phiếu, tô màu dòng, tự tải lại 60s) → review → commit.
Blocked: dev server cổng 3000 đang tắt → chưa mở trình duyệt kiểm.

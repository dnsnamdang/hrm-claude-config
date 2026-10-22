# Biên bản xử lý hàng thừa, thiếu sau kiểm kê — Tóm tắt

> Người phụ trách: @khoipv · Nhánh: `feat/chuyen-doi-hang-hoa` (checkout từ `gop_db`) · Bắt đầu: 21/10/2026
> Nguồn ERP: `inventoryAuditReport.*` — `Warehouse\InventoryAuditReportsController` + `App\Model\Warehouse\Inventory\InventoryAuditReport`
> Menu ERP: Kế toán › Kiểm kê › Theo vị trí (link không tham số). HRM: Tài chính › Kiểm kê (`finance.js:352`, đang `erpPath`)
> Màn liên quan: Phiếu kiểm kê theo hàng hóa (`.plans/gop-db/kiem-ke-theo-hang-hoa/`)
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-21-bien-ban-xu-ly-thua-thieu-kiem-ke-design.md`

## Mục tiêu
Port màn ERP "Biên bản xử lý hàng thừa, thiếu sau kiểm kê" sang HRM: kế toán kho lấy kết quả các phiếu kiểm kê theo hàng hóa
đã Hoàn thành của 1 kho trong khoảng ngày, ghi lý do + giá xử lý + % chi phí nhân viên / công ty + NV chịu cho từng hàng
thừa / thiếu, gửi duyệt; người duyệt chốt và hệ thống ghi bút toán.

## Quyết định chính (user chốt 21/10/2026 — spec mục 2)
- Phạm vi danh sách theo quyền Xem tổng cty / cty (ERP menu chỉ cho thấy phiếu mình); người duyệt thấy thêm phiếu Chờ duyệt.
- Giữ lỗi ERP "Chi phí công ty = Chi phí nhân viên" khi lưu (bút toán 711/811 cùng số với ERP).
- 3 quyền tên y ERP (type 8) + Tạo dùng "Kế toán kho"; trait ChecksEmployeePermission, không middleware.
- Sửa ở HRM: link phiếu xuất đúng loại, chặn xem ngoài phạm vi (404), lỗi hiện đúng tab, Duyệt lỗi bút toán → rollback.
- SL / giá / phiếu xử lý BE tự lấy lại từ nguồn khi lưu (không tin client); không có Xóa (ERP đã tắt).

## Kết quả
BE `Modules/Finance` (*InventoryAuditReport*), FE `pages/finance/inventory-audit-reports`, menu Tài chính › Kiểm kê. Không migration.

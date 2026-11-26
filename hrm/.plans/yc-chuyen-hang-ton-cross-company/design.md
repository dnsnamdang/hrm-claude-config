# YC chuyển hàng — hiện tồn kho công ty khác (cross-company) — HRM

> Redmine #10783. Fix ở **CẢ 2 bên**. Nguyên nhân gốc & phân tích chung: xem bản ERP
> `ERP/.plans/yc-chuyen-hang-ton-cross-company/design.md`. File này chỉ ghi phần HRM.

## Hiện trạng HRM

Màn đã port sang **Module `Finance`**:
- BE: `Modules/Finance/Services/ProductTransferRequestService.php::stockOfProducts()` — endpoint RIÊNG
  `finance/product-transfer-requests/stock` (KHÔNG dùng chung với màn khác, khác ERP).
- Tính tồn: `Modules/Finance/Services/AccountingStockService.php::detail()` (dùng chung trong Finance).
- FE: `hrm-client/pages/finance/product-transfer-requests/components/ProductTransferRequestForm.vue`
  (`refreshStock()` GET `finance/product-transfer-requests/stock`, `displayStockText()` hiện '-' khi rỗng).

Lỗi **giống hệt ERP**: `stockOfProducts()` ép `accounting_warehouses.company_id = CurrentCompany::id()`
(dòng 1104-1106), còn dropdown `stockOptions()` liệt kê mọi kho không lọc công ty → chọn kho khác công ty
→ `$accWarehouseIds` rỗng → `AccountingStockService::detail()` fallback về kho công ty hiện tại → tồn 0 → '-'.

## Cách fix (narrow — endpoint riêng nên sửa thẳng, KHÔNG cần cờ)

Trong `stockOfProducts()`:
- Lấy accounting_warehouses theo `warehouseIds` **bỏ lọc công ty**, lấy kèm `company_id`.
- `companyId` = công ty của kho được chọn (`$accWarehouses->first()->company_id`), fallback
  `currentCompanyId()` khi kho không có acc warehouse (giữ hành vi cũ, tồn 0).
- Truyền `companyId` (đã suy từ kho) vào `detail()` → tồn/prepick/hold/khuyến mại tính đúng công ty sở hữu kho.

`AccountingStockService::detail()` **KHÔNG sửa** — đã nhận `$companyId` làm tham số, chỉ cần truyền đúng.

Kho cùng công ty với user: company suy ra = công ty user → kết quả không đổi. Chỉ khác ở kho chéo công ty.

## Quyết định đã chốt
- Hiện tồn kho công ty khác là **đúng nghiệp vụ** (user xác nhận) — khớp BC "tồn có thể bán theo công ty".
- HRM sửa thẳng `stockOfProducts` (không cần cờ vì endpoint riêng); **không** đụng `detail()` dùng chung.
- Giữ chuẩn ERP: logic nghiệp vụ bám ERP, chỉ khác điểm chèn do kiến trúc endpoint.

## Verify
- Playwright MCP `http://127.0.0.1:3000`: mở YC chuyển hàng, chọn kho SG-CSKH, thêm mã `MLER-AM101663CMUX`
  → cột "SL tồn" phải hiện số (≠ '-').

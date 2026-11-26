# Plan — YC chuyển hàng hiện tồn cross-company (HRM)

Redmine #10783. Xem `design.md`. Fix song song bên ERP (`ERP/.plans/yc-chuyen-hang-ton-cross-company/`).

## Tasks (HRM)

- [x] **T1 — BE: `stockOfProducts()` suy công ty từ kho được chọn** ✓ `ProductTransferRequestService.php:1099-1115`
  File: `Modules/Finance/Services/ProductTransferRequestService.php` (method `stockOfProducts`, ~dòng 1091-1116)
  - Thay khối dòng 1099-1108: lấy accounting_warehouses theo `warehouseIds` **bỏ `->where('company_id', ...)`**,
    `->get(['id','company_id'])`.
  - `$accWarehouseIds` = pluck id; `$companyId` = `company_id` của kho đầu tiên, fallback `currentCompanyId()`.
  - Giữ nguyên vòng lặp gọi `detail($productId, $accWarehouseIds, $companyId, $employeeId)`.
  - KHÔNG sửa `AccountingStockService::detail()`.

- [x] **T2 — Verify (Playwright MCP) ✓ 2026-11-26**
  - User DNS Admin (TPE=cty1), kho SG-CSKH (warehouse 5 → acc_wh 10, cty4), mã `MLER-AM101663CMUX` (product 7318).
  - Endpoint thật `finance/product-transfer-requests/stock?stock_query=warehouse_id-5&product_ids[]=7318`
    → **`in_stock: 1`** (đúng tồn kho SG-CSKH, khớp DB acc_wh 10 cty4 qty=1). Trước fallhiện '-'/tồn kho khác.
  - Tinker đối chiếu gốc: OLD (ép cty1) accIds=`[]`→fallback in_stock=2 (kho cty1 KHÁC) · NEW (cty4) accIds=`[10]`→in_stock=1.
  - Regression kho cùng cty (warehouse 2, cty1) → in_stock=2 đúng, không đổi.

## Checkpoint
- 2026-11-26: Fix + verify xong bên HRM. `ProductTransferRequestService::stockOfProducts()` suy `companyId`
  từ `accounting_warehouses.company_id` của kho được chọn (bỏ ép `CurrentCompany::id()`). KHÔNG sửa `detail()`.
  Chưa commit (chờ lệnh user). ERP fix song song (opt-in flag) — xem `ERP/.plans/.../plan.md`.

### Checkpoint — 2026-11-26 (wrap up cuối ngày)
Vừa hoàn thành: push hrm-api develop `2adbbe4e8` (ERP `78eb05d8f1`); Redmine #10783 = Code xong chờ test.
Đang làm dở: (không)
Bước tiếp theo: gop_db khi user yêu cầu; chờ tester.
Blocked: (không) — CHƯA gop_db.

# Plan — YC chuyển hàng hiện tồn cross-company (ERP)

Redmine #10783. Xem `design.md`. Fix song song bên HRM (`HRM/.plans/yc-chuyen-hang-ton-cross-company/`).

## Tasks (ERP)

- [x] **T1 — BE: `getStockQty` nhận cờ `stock_by_selected_warehouse`** ✓ `ProductStockService.php` (3 chỗ: cờ+skip filter, suy `$selected_company_id`, ternary `params['company_id']`). `getStockQtyForApi` (mobile) KHÔNG đổi.
  File: `app/Services/Product/ProductStockService.php` (method `getStockQty`, ~dòng 13-96)
  - Đọc cờ `$byWarehouse = (bool) $request->stock_by_selected_warehouse;`
  - Dòng 34: thêm điều kiện `&& !$byWarehouse` để KHÔNG ép `company_id = $user->info->company_id` khi cờ bật.
  - Sau khi `pluck('id')` ra `$accounting_warehouse_ids` (dòng 54): nếu `$byWarehouse` và có acc warehouse →
    suy `$selectedCompanyId = AccountingWarehouse::whereIn('id', $accounting_warehouse_ids)->value('company_id');`
  - Dòng 79 (`params['company_id']`): dùng `$byWarehouse ? $selectedCompanyId : $request->company_id`.
  - KHÔNG sửa `getAccountingStockDetail`.

- [x] **T2 — FE: form YC chuyển hàng gửi cờ** ✓ `formJs.blade.php` `$scope.updateStock` — thêm `stock_by_selected_warehouse: 1` vào object `data`.

- [x] **T3 — Verify (đọc code + dữ liệu, 2026-11-26)**
  - Controller `Warehouse\WarehouseInfosController@stockOfProducts` gọi `getStockQty` (đã confirm bằng grep) — đúng method đã sửa. `getStockQtyForApi` (mobile CRM) KHÔNG đổi.
  - Nhánh cũ không đổi: màn khác gọi `stockOfProducts` KHÔNG gửi cờ → `$by_selected_warehouse=false` → điều kiện `&& !$by_selected_warehouse` giữ nguyên `where('company_id', login)`, và `params['company_id']` ternary trả `$request->company_id` như cũ → byte-identical.
  - `php -l` OK. Logic khớp HRM (đã verify Playwright: kho khác cty hiện tồn đúng, kho cùng cty không đổi).

## Checkpoint
- 2026-11-26: Fix xong ERP (opt-in flag `stock_by_selected_warehouse`, chỉ form YC chuyển hàng gửi).
  3 edit BE + 1 edit FE. `getAccountingStockDetail` đã honor `params['company_id']` nên KHÔNG đụng.
  Verify bằng đọc code + data (ERP không chạy local tiện); HRM logic tương đương đã verify Playwright.
  Chưa commit (chờ lệnh user).

### Checkpoint — 2026-11-26 (wrap up cuối ngày)
Vừa hoàn thành: push ERP develop_02 `78eb05d8f1` (HRM song song `2adbbe4e8`); Redmine #10783 = Code xong chờ test.
Đang làm dở: (không)
Bước tiếp theo: gop_db khi user yêu cầu; chờ tester.
Blocked: (không) — CHƯA gop_db; ERP chưa kiểm màn thật (chỉ đọc code + data).

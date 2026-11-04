# Sổ chi tiết công nợ phải trả NCC — plan

Spec: `docs/superpowers/specs/gop-db/2026-11-04-so-chi-tiet-cong-no-ncc-design.md`. Nhánh `feat/so-chi-tiet-cong-no-ncc` (2 repo, từ origin/develop).

- [x] Tách phần chung (user đồng ý 04/11): trait `EmployeeDebtCommon` → `AccountDebtCommon` (`scopeColumns()`, `applyMoneyFilter()`,
      `printFilterInfo()`); lớp cha `AccountLedgerService` (dòng, ghi chú, TK đối ứng, đầu kỳ theo loại tiền, Excel, bản in);
      `ValidatesEmployeeDebtFilters` → `ValidatesAccountDebtFilters` (thêm ô bắt buộc riêng). 31 test 2 màn NV vẫn xanh.
- [x] BE `SupplierDebtDetailService` + controller + route `finance/supplier-debt-details` (`/`, `/meta`, `/suppliers`, `/export-rows`,
      `/print-list-data`) + 2 quyền cuối seeder (`permission:sync` local).
- [x] Test `SupplierDebtDetailTest` 6 ca (NCC 2 cột + đầu kỳ cùng bộ lọc, phạm vi, nhân viên, ngoại tệ từng loại tiền, 403/422, API).
- [x] FE `pages/finance/supplier-debt-details` + link menu (`isShow` 2 quyền).
- [x] Bấm thử local: mỗi thao tác 1 request; báo đỏ 3 ô; TK 331 NCC 30725 (USD, 306 dòng, ~3s) / NCC 620 (VNĐ, 1.265 dòng); In; Excel 309 dòng.

Ghi chú: menu gắn `isShow` ⇒ FE chỉ cho vào khi VAI TRÒ có quyền (store không lấy quyền gán thẳng nhân viên) — kể cả Super admin
phải được gán vào vai trò. Local đã gán tạm 2 quyền vào vai trò 18.

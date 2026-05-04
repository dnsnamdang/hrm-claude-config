# Plan: Lọc + chạy lại hạch toán phiếu báo có sai (TanPhatDev)

## Trạng thái
- Bắt đầu: 2026-04-29
- Tiến độ: ✅ Hoàn thành 2026-04-29 (3 task code + manual run + verify)

## Phase 1: UpdateDB.php — thêm 3 method

### database/seeds/UpdateDB.php
- [x] Task 1: Thêm method `findInvalidBillIncomeReports()` (sau `deleteAccountDetailOld()` ~L233): detect 4 case (null_object/invalid_type/swap/both_set), echo grouped, return array errors. Whitelist 10 class hợp đồng (Contract/InlandBuyContract*/BuyContract2/ProductExport/ServiceContract/WrServiceContract/FirmContract/ProjectContract). Ngoại lệ: parent.type=3 (Thu khác) hoặc id=10929 (KHÁCH KHÔNG RÕ).

- [x] Task 2: Thêm method `fixCustomerSupplierSwap()`: auto-swap chỉ case (c) — type=1 mà chỉ có supplier_id → move sang customer_id; type=2 mà chỉ có customer_id → move sang supplier_id. Skip khách không rõ. Return số detail đã fix.

- [x] Task 3: Thêm method `rerunBillIncomeReportAccounting($ids = [])`: foreach `BillIncomeReport::whereIn('id', $ids)` → gọi `$this->deleteAccountDetailOld($report)` + `$report->saveAccountsDetail($report->created_at)`. DB::beginTransaction wrapping.

## Phase 2: Manual run + verify

- [x] Task 4: Chạy 3 step qua tinker:
  ```
  php artisan tinker
  >>> $u = new UpdateDB();
  >>> $errors = $u->findInvalidBillIncomeReports();   // 1. inspect, ghi lại IDs
  >>> $u->fixCustomerSupplierSwap();                  // 2. auto-swap
  >>> // sửa tay null_object/invalid_type/both_set nếu cần
  >>> $ids = array_unique(array_merge($errors['null_object'], $errors['swap'], $errors['both_set'], array_column($errors['invalid_type'], 'parent_id')));
  >>> $u->rerunBillIncomeReportAccounting($ids);      // 3. re-run
  >>> $errors2 = $u->findInvalidBillIncomeReports();  // verify đã giảm
  ```
  - Kiểm tra `account_details` sau re-run: `contract_id`, `contractable_*`, `customer_id`/`supplier_id` đúng theo `details` mới.
  - Spot-check 1-2 phiếu: tổng money_value khớp với `bill_income_reports.sum_money`.

## Checkpoint
### Checkpoint — 2026-04-29
Vừa hoàn thành: 3/3 method code xong, đặt sau `deleteAccountDetailOld()` (L233) trong `database/seeds/UpdateDB.php`. Pass `php -l`. Tận dụng `BillIncomeReport`, `BillIncomeReportDetail`, `AccountDetail`, `AccountDetailRef` đã imported sẵn. Whitelist 10 class hợp đồng dùng FQCN inline.
Đang làm dở: chờ user chạy `php artisan tinker` 4 step (find → swap → fix tay → rerun → re-find verify).
Bước tiếp theo: User test + báo lại.
Blocked: không.

### Checkpoint — 2026-04-29 (close)
Vừa hoàn thành: ✅ User chạy 4 step tinker xong + verify đã giảm error. Đóng feature.
Đang làm dở: không
Bước tiếp theo: không
Blocked: không

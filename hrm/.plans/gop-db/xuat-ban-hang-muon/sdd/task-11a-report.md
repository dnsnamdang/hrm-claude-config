# Task 11a — Report: 2 endpoint nguồn "phiếu xuất mượn" + siết `canBorrowSell` (BE)

## Trạng thái: DONE

Nhánh: `gop_db`. **KHÔNG commit git** (theo yêu cầu task).

## Thay đổi

### 1. Route — `Modules/Finance/Routes/api.php`
Thêm 2 route trong group `/borrow-sell-requests`:
- `GET /contracts/{id}/export-requests` → `contractExportRequests` (ngay sau `/contracts/{id}/borrow-sell-data`)
- `GET /export-requests/{id}` → `exportRequestBorrowSellData` (trước `GET /{id}` show cuối cùng)

Full path: `GET api/v1/finance/borrow-sell-requests/contracts/{id}/export-requests`, `GET api/v1/finance/borrow-sell-requests/export-requests/{id}`.

### 2. Controller — `Modules/Finance/Http/Controllers/V1/BorrowSellRequestController.php`
Thêm 2 method mỏng (chỉ gọi service), đặt sau `contractBorrowSellData()`:
- `contractExportRequests(Request $request, $id)` → gọi `service->searchExportRequests()`
- `exportRequestBorrowSellData($id)` → gọi `service->dataForBorrowSell()`

### 3. Service — `Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestService.php`
- Thêm `use Modules\Finance\Entities\ProductImportRequest\ProductExportRequest;`
- Thêm public method `searchExportRequests(Request $request, int $contractId, string $contractableType): array` — đặt ngay sau `searchContracts()`, trước block `// Helpers`. Lọc fail-closed (AND): `created_by = self` + `type = XUAT_MUON` + `status = 5` + `borrow_status = DA_MUON` + đúng hợp đồng (`firm_contract_id` hoặc `wr_service_contract_id` theo `contractable_type`). Trả mảng phẳng `limit(50)`, không paginate (theo Ruling R-T11a-list — 1 hợp đồng chỉ có vài phiếu của 1 user).
- Thêm public method `dataForBorrowSell(int $exportRequestId): array` — gate bằng `canBorrowSell()` (throw `ValidationException` nếu fail), SELECT chi tiết `product_export_request_details` với điều kiện `need_export = true` và `base_exported_qty > borrow_returned_qty`, tính `available` bằng đúng công thức `BorrowSellRequestCalculator::availableSellQty()` khớp `syncProducts()` trong `store()`. Theo Ruling R-T11a-breakdown: KHÔNG lọc bỏ dòng `available = 0` ở BE, để FE tự chặn nhập vượt `available`.

### 4. Siết `canBorrowSell` (fail-closed)
Đổi từ OR lỏng (thiếu `type`) sang AND chặt đủ 4 điều kiện, thêm `type` vào SELECT và vào điều kiện:
```php
return ((int) $row->created_by === (int) auth()->id())
    && ((int) $row->type === self::XUAT_MUON)
    && ((int) $row->status === 5)
    && ((int) $row->borrow_status === ProductExportRequest::DA_MUON);
```
Lý do: spec §4.3#2 yêu cầu `status=5` VÀ `borrow_status=DA_MUON` (không phải OR), nguồn bắt buộc phải là phiếu XUẤT MƯỢN (`type=3`). Bản cũ (OR + thiếu type) cho phép chọn phiếu không phải xuất mượn hoặc chưa mượn — lỗ hổng nghiệp vụ. Đã grep xác nhận (mục Verify #5) chỉ 2 nơi gọi `canBorrowSell`: `store()` (dòng 52, ảnh hưởng lan có chủ đích — store cũng chặt hơn, đồng bộ) và `dataForBorrowSell()` (dòng 651, method mới của task này). Không có caller nào khác bị ảnh hưởng ngoài dự kiến.

## Verify

1. `php -l` trên cả 3 file sửa → No syntax errors detected (cả 3).
2. `composer dump-autoload -o` → chạy thành công, "Generated optimized autoload files containing 12327 classes".
3. Tinker `method_exists`:
   - `BorrowSellRequestService::searchExportRequests` → true
   - `BorrowSellRequestService::dataForBorrowSell` → true
   - `BorrowSellRequestController::contractExportRequests` → true
   - `BorrowSellRequestController::exportRequestBorrowSellData` → true
4. Route dump qua `app('router')->getRoutes()` (tránh `route:list` — crash pre-existing ở module Timesheet, không liên quan task): xác nhận có đủ 2 route mới:
   - `GET api/v1/finance/borrow-sell-requests/contracts/{id}/export-requests` → `contractExportRequests`
   - `GET api/v1/finance/borrow-sell-requests/export-requests/{id}` → `exportRequestBorrowSellData`
   Và thứ tự đúng: `export-requests/{id}` (static-first) nằm TRƯỚC `GET /{id}` (show) trong danh sách route đăng ký.
5. `grep -rn "canBorrowSell" Modules/Finance` → chỉ 3 dòng: định nghĩa (759) + 2 caller (`store()` dòng 52, `dataForBorrowSell()` dòng 651). Không caller ngoài dự kiến.

**Tóm tắt verify (1 dòng):** php -l sạch cả 3 file, autoload OK, 4/4 method_exists=true, 2 route mới lên đúng thứ tự (static trước `/{id}`), canBorrowSell chỉ 2 caller như dự kiến.

## Concerns

- Không chạy được smoke test gọi thật endpoint qua HTTP (không có session auth trong tinker) — chỉ verify method tồn tại + route đăng ký đúng, đúng theo yêu cầu Verify #3 của brief ("KHÔNG cần auth, chỉ kiểm method tồn tại").
- `searchExportRequests` giới hạn `limit(50)` không paginate — nếu về sau 1 user có nhiều hơn 50 phiếu xuất mượn cho cùng hợp đồng thì cần bổ sung paginate (đã ghi rõ trong docblock theo Ruling R-T11a-list).
- `dataForBorrowSell` trả cả dòng có `available = 0` (do `returningQty` in-flight) — chủ đích theo Ruling R-T11a-breakdown, FE phải tự chặn qua field `available`.

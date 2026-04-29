# Design: Lọc + chạy lại hạch toán phiếu báo có sai (TanPhatDev)

## Bối cảnh

Phiếu báo có (`bill_income_reports`) có 1 số bản ghi `bill_income_report_details` bị sai dữ liệu, làm `account_details` (qua `saveAccountsDetail()`) ra `contract_id`/`contractable_*` sai → ảnh hưởng báo cáo công nợ. Cần script trong `database/seeds/UpdateDB.php` để (1) detect các phiếu sai, (2) auto-swap khi `customer_id`/`supplier_id` lẫn lộn, (3) re-run hạch toán theo `BillIncomeReport::saveAccountsDetail()` hiện tại.

## Quy tắc

### 4 tiêu chí "details sai"

| # | Tiêu chí | Ngoại lệ |
|---|----------|----------|
| (a) | `objectable_id IS NULL` HOẶC `objectable_type IS NULL` | parent.type=3 (Thu khác); HOẶC `customer_id=10929` / `supplier_id=10929` (KHÁCH KHÔNG RÕ) |
| (b) | `objectable_type` không thuộc whitelist (và không NULL) | (không) |
| (c) | `customer_id`/`supplier_id` lẫn lộn theo parent.type: type=1 mà `supplier_id` set + `customer_id` null; type=2 mà `customer_id` set + `supplier_id` null | KHÁCH KHÔNG RÕ |
| (d) | Cả `customer_id` lẫn `supplier_id` cùng có giá trị | (không) |

### Whitelist `objectable_type` hợp lệ
- `App\Contract`
- `App\Model\Order\InlandBuyContract`
- `App\Model\Order\InlandBuyContract2`
- `App\Model\Order\InlandBuyContractNew`
- `App\Model\Order\BuyContract2`
- `App\Model\Warehouse\ProductExport`
- `App\Model\Sale\ServiceContract`
- `App\Model\Customers\WrServiceContract`
- `App\Model\Sale\Firm\Contract\FirmContract`
- `App\Model\Sale\ProjectContract`

### Hành vi script
- **2 method tách**: 1 method find (chỉ list, không sửa), 1 method re-run (xoá account_details cũ + chạy lại).
- **Auto-fix duy nhất case (c)**: swap `customer_id` ↔ `supplier_id` theo parent.type. Case (a)/(b)/(d) chỉ list ra để user xử lý tay (cần phán đoán nghiệp vụ).
- **Re-run hạch toán**: dùng helper sẵn có `deleteAccountDetailOld($exportable)` (UpdateDB.php L223) để xoá `account_details` + `account_detail_refs` cũ, rồi gọi `$report->saveAccountsDetail($report->created_at)` để tạo lại theo logic đúng hiện tại.

## Thay đổi

### `database/seeds/UpdateDB.php` — thêm 3 method

**1. `findInvalidBillIncomeReports()`** — detect, echo grouped output, return array IDs theo loại lỗi:
```php
public function findInvalidBillIncomeReports()
{
    $whitelist = [
        \App\Contract::class,
        \App\Model\Order\InlandBuyContract::class,
        \App\Model\Order\InlandBuyContract2::class,
        \App\Model\Order\InlandBuyContractNew::class,
        \App\Model\Order\BuyContract2::class,
        \App\Model\Warehouse\ProductExport::class,
        \App\Model\Sale\ServiceContract::class,
        \App\Model\Customers\WrServiceContract::class,
        \App\Model\Sale\Firm\Contract\FirmContract::class,
        \App\Model\Sale\ProjectContract::class,
    ];
    $known_unknown = [10929]; // KHÁCH KHÔNG RÕ id

    $details = \App\Model\IncomeExpenditure\BillIncomeReportDetail::query()
        ->with('parent')
        ->whereHas('parent')
        ->get();

    $errors = ['null_object' => [], 'invalid_type' => [], 'swap' => [], 'both_set' => []];

    foreach ($details as $d) {
        $type = $d->parent->type;
        $isUnknown = in_array($d->customer_id, $known_unknown) || in_array($d->supplier_id, $known_unknown);

        // (a) null object — bỏ qua nếu type=3 hoặc KHÁCH KHÔNG RÕ
        if ((!$d->objectable_id || !$d->objectable_type) && $type != 3 && !$isUnknown) {
            $errors['null_object'][] = $d->parent_id;
        }
        // (b) invalid type — bỏ qua nếu null (đã catch ở a)
        elseif ($d->objectable_type && !in_array($d->objectable_type, $whitelist)) {
            $errors['invalid_type'][] = ['parent_id' => $d->parent_id, 'type' => $d->objectable_type];
        }

        // (c) swap — bỏ qua nếu KHÁCH KHÔNG RÕ
        if (!$isUnknown) {
            if ($type == 1 && $d->supplier_id && !$d->customer_id) {
                $errors['swap'][] = $d->parent_id;
            } elseif ($type == 2 && $d->customer_id && !$d->supplier_id) {
                $errors['swap'][] = $d->parent_id;
            }
        }

        // (d) both set
        if ($d->customer_id && $d->supplier_id) {
            $errors['both_set'][] = $d->parent_id;
        }
    }

    foreach ($errors as $key => $list) {
        $ids = array_values(array_unique(array_map(fn($x) => is_array($x) ? $x['parent_id'] : $x, $list)));
        echo "[$key] " . count($ids) . " phiếu: " . json_encode($ids) . "\n";
    }
    return $errors;
}
```

**2. `fixCustomerSupplierSwap()`** — auto-swap case (c). Trả về số detail đã fix:
```php
public function fixCustomerSupplierSwap()
{
    $details = \App\Model\IncomeExpenditure\BillIncomeReportDetail::query()
        ->with('parent')->whereHas('parent')->get();

    $fixed = 0;
    foreach ($details as $d) {
        $type = $d->parent->type;
        if ($type == 1 && $d->supplier_id && !$d->customer_id) {
            $d->customer_id = $d->supplier_id;
            $d->supplier_id = null;
            $d->save();
            $fixed++;
        } elseif ($type == 2 && $d->customer_id && !$d->supplier_id) {
            $d->supplier_id = $d->customer_id;
            $d->customer_id = null;
            $d->save();
            $fixed++;
        }
    }
    echo "Đã swap $fixed details.\n";
    return $fixed;
}
```

**3. `rerunBillIncomeReportAccounting($ids = [])`** — xoá account_details cũ + chạy lại `saveAccountsDetail`:
```php
public function rerunBillIncomeReportAccounting($ids = [])
{
    $query = \App\Model\IncomeExpenditure\BillIncomeReport::query();
    if (!empty($ids)) $query->whereIn('id', $ids);
    $reports = $query->get();

    DB::beginTransaction();
    try {
        foreach ($reports as $report) {
            $this->deleteAccountDetailOld($report);
            $report->saveAccountsDetail($report->created_at);
        }
        DB::commit();
        echo "Đã re-run hạch toán cho " . count($reports) . " phiếu.\n";
    } catch (\Exception $e) {
        DB::rollBack();
        echo "Lỗi: " . $e->getMessage() . "\n";
        throw $e;
    }
}
```

### Cách dùng (qua tinker)
```
php artisan tinker
>>> $u = new UpdateDB();
>>> $errors = $u->findInvalidBillIncomeReports();          // 1. inspect
>>> $u->fixCustomerSupplierSwap();                          // 2. auto-swap
>>> // user sửa tay null_object/invalid_type/both_set nếu cần
>>> $ids = array_unique(array_merge($errors['null_object'], $errors['swap'], $errors['both_set'], array_column($errors['invalid_type'], 'parent_id')));
>>> $u->rerunBillIncomeReportAccounting($ids);              // 3. re-run
```

## Không thay đổi

- `BillIncomeReport::saveAccountsDetail()` — giữ nguyên (đây là logic đúng, script chỉ chạy lại)
- Helper `deleteAccountDetailOld()` đã có sẵn ở UpdateDB.php L223 — tận dụng
- Schema `bill_income_report_details` — không thêm/đổi cột
- `run()` của UpdateDB — không tự động chạy 3 method mới (user gọi tay qua tinker)

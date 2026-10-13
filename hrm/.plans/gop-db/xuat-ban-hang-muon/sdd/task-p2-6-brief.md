# Task P2-6 — Hạch toán CƯỚC VẬN CHUYỂN chuyến xe (accountingDeliveryTrip)

> Đây là YÊU CẦU của bạn. Mọi con số / chuỗi / chữ ký hàm lấy VERBATIM từ file này.
> KHÔNG đọc cả plan. KHÔNG spawn subagent. Git: chỉ `git add <path cụ thể>` + `git commit` (KHÔNG push/pull/fetch/checkout).

## Bối cảnh 1 dòng
Feature `xuat-ban-hang-muon` Phase 2 (phiếu xuất bán hàng mượn `PXBHM-`), nhánh `gop_db`, DB gộp `erp_hrm_check`. Đây là task port method RIÊNG `accountingDeliveryTrip()` của ERP `App\Model\Warehouse\BorrowSell` sang HRM: ghi bút toán CƯỚC VẬN CHUYỂN cho từng chuyến xe của các phiếu xuất kho thuộc phiếu bán hàng mượn.

## File phải sửa
- **Sửa duy nhất:** `Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php`
  - Thêm 2 const vào vùng const hiện có (sau dòng `const INVOICEABLE_BORROW_SELL = ...;`, ~dòng 60).
  - Thêm 1 method public `postDeliveryTripAccounting(BorrowSell $bs): array` + 1 helper private `buildTripCostAccounts(...)`.
  - KHÔNG đụng `getDataAccounting` / `postAccounting` / các nhánh Firm/WrService đã có. Method mới ĐỘC LẬP.
- **Tạo mới test:** `Modules/Finance/Tests/Feature/BorrowSellDeliveryTripAccountingTest.php`

## Nguồn ERP để port (App\Model\Warehouse\BorrowSell::accountingDeliveryTrip, dòng 512-554)
```php
public function accountingDeliveryTrip () {
    $works = Work::getByCode();
    $cost_debts = CostDebt::getByCode();
    $group = 1;
    $borrow_sell_request = $this->parent;                      // HRM: $bs->borrowSellRequest
    $product_export_requests = $borrow_sell_request->product_export_requests;
    $accounts = [];                                            // ⚠ ERP set 1 lần NGOÀI loop → bug double-post
    foreach ($product_export_requests as $product_export_request) {
        if ($product_export_request->is_export_direct) continue;
        $warehouse_export_request_ids = WarehouseExportRequest::query()
            ->where('product_export_request_id', $product_export_request->id)->pluck('id');
        $warehouse_export = WarehouseExport::query()
            ->whereIn('warehouse_export_request_id', $warehouse_export_request_ids)->first();
        $activity = ActivityHasDeliveryTrip::query()
            ->where('warehouse_export_id', $warehouse_export->id)->first();
        if (!$activity) continue;
        // check chuyen xe da dc hach toan
        $acs = AccountDetail::query()->where('invoiceable_id', $activity->delivery_trip_id)
            ->where('invoiceable_type', DeliveryTrip::class)->get();
        if (count($acs) == 0) continue;
        $trip = $activity->trip;
        $is_company_pay = $trip->company_pay > 0 ? true : false;
        if ($is_company_pay) {
            AccountDetail::createDataSaveDept($accounts, 6427, $activity->total_cost_transition, AccountDetail::TYPE_DEPT, [3351], [
                Employee::class => $product_export_request->created_by, 'group' => $group, CostDebt::class => $cost_debts['TVC'] ?? 0 ]);
        } else {
            AccountDetail::createDataSaveDept($accounts, 3351, $activity->total_cost_transition, AccountDetail::TYPE_DEPT, [3351], [
                Employee::class => $product_export_request->created_by, 'employee_department_id' => $product_export_request->department_id, 'group' => $group, Work::class => $works['TVC'] ?? 0 ]);
        }
        AccountDetail::createDataSaveDept($accounts, 3351, $activity->total_cost_transition, AccountDetail::TYPE_HAS, [3351], [
            Employee::class => $product_export_request->created_by, 'employee_department_id' => $product_export_request->department_id, 'group' => $group, Work::class => $works['TVC'] ?? 0 ]);
        AccountDetail::saveAccountDetail($accounts, $activity->delivery_trip_id, DeliveryTrip::class);
    }
}
```

## 3 RULING đã chốt (KHÔNG port máy móc chữ ERP — làm đúng như dưới đây)
- **T6-A (FQN check — faithful port, no-op trên data hiện tại):** giữ NGUYÊN cách check "chuyến đã được hạch toán": đếm `account_details` có `invoiceable_id = delivery_trip_id` AND `invoiceable_type = self::INVOICEABLE_DELIVERY_TRIP` (`'App\\Model\\Warehouse\\DeliveryTrip'`). Nếu 0 → `continue` (bỏ qua chuyến). Đây là port trung thực; trên DB gộp hiện tại luôn 0 (các chuyến dùng flow DeliveryTripAccounting khác) nên method sẽ KHÔNG ghi gì — ĐÚNG kỳ vọng, không được tự đổi cột check.
- **T6-B (fix double-post):** ERP set `$accounts=[]` NGOÀI loop rồi `saveAccountDetail` mỗi vòng → chuyến thứ 2 lưu lại cả bút toán chuyến 1. Đây là oversight. → Ở HRM build MẢNG MỚI `$tripAccounts = []` mỗi vòng lặp (dùng helper), save riêng từng chuyến.
- **T6-C (null guard):** ERP không guard `$warehouse_export` null (`$warehouse_export->id`). → thêm `if (!$warehouse_export) continue;`.

## Entity dùng (ĐÃ verify, dùng ĐÚNG namespace này — đừng đoán)
Thêm `use` ở đầu file service:
```php
use Modules\Assign\Entities\Warehouse\WarehouseExportRequest;
use Modules\Assign\Entities\Warehouse\WarehouseExport;
use Modules\Finance\Entities\Delivery\ActivityHasDeliveryTrip;
```
- `$bs->borrowSellRequest` → quan hệ SẴN CÓ trên `Modules\Finance\Entities\BorrowSell\BorrowSell` (belongsTo `BorrowSellRequest`, FK `borrow_sell_request_id`). Có thể null → guard `if (!$req) return [true, ''];`.
- `$req->product_export_requests` → quan hệ belongsToMany SẴN CÓ trên `BorrowSellRequest` (pivot `borrow_sell_request_has_export_requests`). Trả về `Modules\Finance\Entities\ProductImportRequest\ProductExportRequest` (read-only) — CHỈ ĐỌC `is_export_direct`, `id`, `created_by`, `department_id` nên OK.
- `WarehouseExportRequest` (Assign): cột `product_export_request_id`.
- `WarehouseExport` (Assign): cột `warehouse_export_request_id`.
- `ActivityHasDeliveryTrip` (Finance, T2 đã tạo): cột `warehouse_export_id`, `delivery_trip_id`, `total_cost_transition`; quan hệ `trip()` belongsTo `Modules\Finance\Entities\Delivery\DeliveryTrip`.
- `DeliveryTrip` (Finance): cột `company_pay` (decimal, có trong DB dù không có trong PHPDoc), `name`.
- `AccountDetail` = `Modules\Finance\Entities\Account\AccountDetail` (ĐÃ import sẵn trong file).

## Const HRM (khác ERP — dùng key thô, KHÔNG dùng ::class)
- Work TVC id = **10** (verified: works.code='TVC', id=10). ERP `$works['TVC']` → HRM hằng số `const WORK_VAN_CHUYEN = 10;`.
- CostDebt TVC: **KHÔNG tồn tại** trong DB gộp → ERP `$cost_debts['TVC'] ?? 0` = 0. HRM truyền thẳng `'cost_debt_id' => 0`.
- Thêm:
```php
const WORK_VAN_CHUYEN = 10;   // TVC — tiền vận chuyển
/** FQN model ERP cho chứng từ chuyến xe (ERP đọc lại được; đồng thời là cột check "đã hạch toán"). */
const INVOICEABLE_DELIVERY_TRIP = 'App\\Model\\Warehouse\\DeliveryTrip';
```

## saveAccountDetail HRM ≠ ERP (QUAN TRỌNG)
Chữ ký HRM: `AccountDetail::saveAccountDetail($accounts, $invoiceable_id, $invoiceable_type, $invoiceable_code, array $meta = []): array`.
`$invoiceable_code` BẮT BUỘC (cột NOT NULL). ERP dòng 552 gọi 3 args (hook tự set code). HRM PHẢI truyền:
- `$invoiceable_id` = `$activity->delivery_trip_id`
- `$invoiceable_type` = `self::INVOICEABLE_DELIVERY_TRIP`
- `$invoiceable_code` = `$trip->name` (khớp ERP AccountDetail:202 set invoiceable_code = trip->name khi type=DeliveryTrip; nếu null → dùng `''`)
- `$meta` = `['created_by' => $bs->created_by, 'invoiceable_date_accounting' => $bs->created_at ? \Carbon\Carbon::parse($bs->created_at)->format('Y-m-d') : null]` (Carbon đã import sẵn ở đầu file).

## Mã cần viết

### Helper thuần (không đụng DB — để test)
```php
/**
 * Dựng 2 vế bút toán cước vận chuyển cho 1 chuyến xe. Port ERP accountingDeliveryTrip.
 *   company_pay > 0  → Nợ 6427 (mã phí TVC=0) / Có 3351 (work TVC)
 *   company_pay <= 0 → Nợ 3351 (work TVC)     / Có 3351 (work TVC)
 * Cả 2 vế đều gắn employee_id = người lập phiếu xuất kho; vế 3351 gắn employee_department_id.
 */
private function buildTripCostAccounts(float $amount, bool $isCompanyPay, ?int $createdBy, ?int $deptId, int $group): array
{
    $accounts = [];
    if ($isCompanyPay) {
        AccountDetail::createDataSaveDept($accounts, 6427, $amount, AccountDetail::TYPE_DEPT, [3351],
            ['employee_id' => $createdBy, 'group' => $group, 'cost_debt_id' => 0]);
    } else {
        AccountDetail::createDataSaveDept($accounts, 3351, $amount, AccountDetail::TYPE_DEPT, [3351],
            ['employee_id' => $createdBy, 'employee_department_id' => $deptId, 'group' => $group,
             'work_id' => self::WORK_VAN_CHUYEN]);
    }
    AccountDetail::createDataSaveDept($accounts, 3351, $amount, AccountDetail::TYPE_HAS, [3351],
        ['employee_id' => $createdBy, 'employee_department_id' => $deptId, 'group' => $group,
         'work_id' => self::WORK_VAN_CHUYEN]);
    return $accounts;
}
```

### Method chính
```php
/**
 * Hạch toán CƯỚC VẬN CHUYỂN cho từng chuyến xe của phiếu xuất bán hàng mượn.
 * Port ERP App\Model\Warehouse\BorrowSell::accountingDeliveryTrip (dòng 512-554).
 * GHI trực tiếp account_details, mỗi chuyến 1 lần saveAccountDetail keyed theo delivery_trip_id.
 * Method ĐỘC LẬP với getDataAccounting — orchestrator (T7) gọi RIÊNG sau khi finalize phiếu
 * (ERP gọi ở BorrowSellsController@update:281).
 * @return array [bool ok, string err]
 */
public function postDeliveryTripAccounting(BorrowSell $bs): array
{
    $req = $bs->borrowSellRequest;
    if (!$req) {
        return [true, ''];
    }
    $group = 1;
    $meta = [
        'created_by' => $bs->created_by,
        'invoiceable_date_accounting' => $bs->created_at ? Carbon::parse($bs->created_at)->format('Y-m-d') : null,
    ];

    try {
        return DB::transaction(function () use ($req, $group, $meta) {
            foreach ($req->product_export_requests as $per) {
                if ($per->is_export_direct) {
                    continue;
                }
                $werIds = WarehouseExportRequest::query()
                    ->where('product_export_request_id', $per->id)->pluck('id');
                $warehouseExport = WarehouseExport::query()
                    ->whereIn('warehouse_export_request_id', $werIds)->first();
                if (!$warehouseExport) {          // Ruling T6-C: guard null
                    continue;
                }
                $activity = ActivityHasDeliveryTrip::query()
                    ->where('warehouse_export_id', $warehouseExport->id)->first();
                if (!$activity) {
                    continue;
                }
                // Ruling T6-A: chỉ hạch toán khi chuyến đã có bút toán gốc (invoiceable=DeliveryTrip)
                $tripAccounted = AccountDetail::query()
                    ->where('invoiceable_id', $activity->delivery_trip_id)
                    ->where('invoiceable_type', self::INVOICEABLE_DELIVERY_TRIP)
                    ->exists();
                if (!$tripAccounted) {
                    continue;
                }
                $trip = $activity->trip;
                $isCompanyPay = $trip && (float) $trip->company_pay > 0;

                // Ruling T6-B: build mảng MỚI mỗi chuyến → save riêng, tránh double-post
                $tripAccounts = $this->buildTripCostAccounts(
                    (float) $activity->total_cost_transition,
                    $isCompanyPay,
                    $per->created_by,
                    $per->department_id,
                    $group
                );
                [$ok, $err] = AccountDetail::saveAccountDetail(
                    $tripAccounts,
                    $activity->delivery_trip_id,
                    self::INVOICEABLE_DELIVERY_TRIP,
                    $trip->name ?? '',
                    $meta
                );
                if (!$ok) {
                    throw new \RuntimeException($err);
                }
            }
            return [true, ''];
        });
    } catch (\Throwable $e) {
        return [false, 'Lỗi hạch toán cước vận chuyển phiếu ' . $bs->code . ': ' . $e->getMessage()];
    }
}
```

## Test — `BorrowSellDeliveryTripAccountingTest.php`
2 test, dùng `DatabaseTransactions`. Test helper thuần (không cần DB fixture nặng):

```php
<?php

namespace Modules\Finance\Tests\Feature;

use Tests\TestCase;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Modules\Finance\Services\BorrowSell\BorrowSellPostingService;
use Modules\Finance\Entities\BorrowSell\BorrowSell;

class BorrowSellDeliveryTripAccountingTest extends TestCase
{
    use DatabaseTransactions;

    /** Gọi helper private buildTripCostAccounts qua reflection. */
    private function buildAccounts(float $amount, bool $isCompanyPay, ?int $createdBy, ?int $deptId, int $group): array
    {
        $svc = app(BorrowSellPostingService::class);
        $ref = new \ReflectionMethod($svc, 'buildTripCostAccounts');
        $ref->setAccessible(true);
        return $ref->invoke($svc, $amount, $isCompanyPay, $createdBy, $deptId, $group);
    }

    public function test_company_pay_debits_6427_with_cost_debt_zero_and_credits_3351()
    {
        $accounts = $this->buildAccounts(500000, true, 808, 47, 1);

        $debit = collect($accounts)->firstWhere('type', 1);
        $credit = collect($accounts)->firstWhere('type', 2);

        $this->assertSame(6427, $debit['number'], 'company_pay>0 → Nợ 6427');
        $this->assertSame(0, $debit['cost_debt_id'], 'Nợ 6427 gắn mã phí TVC=0');
        $this->assertArrayNotHasKey('work_id', $debit, 'Vế 6427 KHÔNG gắn work');
        $this->assertSame(3351, $credit['number'], 'Có 3351');
        $this->assertSame(BorrowSellPostingService::WORK_VAN_CHUYEN, $credit['work_id'], 'Có 3351 gắn work TVC=10');
        $this->assertEqualsWithDelta(500000, $debit['value'], 0.01);
        $this->assertEqualsWithDelta(
            collect($accounts)->where('type', 1)->sum('value'),
            collect($accounts)->where('type', 2)->sum('value'),
            0.01,
            'Nợ phải cân Có'
        );
    }

    public function test_not_company_pay_debits_3351_with_work_tvc()
    {
        $accounts = $this->buildAccounts(300000, false, 808, 47, 1);

        $debit = collect($accounts)->firstWhere('type', 1);
        $credit = collect($accounts)->firstWhere('type', 2);

        $this->assertSame(3351, $debit['number'], 'company_pay<=0 → Nợ 3351');
        $this->assertSame(BorrowSellPostingService::WORK_VAN_CHUYEN, $debit['work_id'], 'Nợ 3351 gắn work TVC=10');
        $this->assertSame(47, $debit['employee_department_id']);
        $this->assertSame(3351, $credit['number']);
        $this->assertSame(BorrowSellPostingService::WORK_VAN_CHUYEN, $credit['work_id']);
        $this->assertEqualsWithDelta(
            collect($accounts)->where('type', 1)->sum('value'),
            collect($accounts)->where('type', 2)->sum('value'),
            0.01,
            'Nợ phải cân Có'
        );
    }
}
```

## Lệnh test
```
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
php vendor/bin/phpunit --filter=BorrowSellDeliveryTripAccountingTest Modules/Finance/Tests/Feature/BorrowSellDeliveryTripAccountingTest.php
```
(KHÔNG dùng `php artisan test` — TTY fail.)

## Định nghĩa HOÀN THÀNH
1. Thêm 2 const + method `postDeliveryTripAccounting` + helper `buildTripCostAccounts` vào service (không đụng code cũ).
2. Thêm 3 `use` entity ở đầu file.
3. Test mới xanh (2 tests pass).
4. `git add` đúng 2 file (service + test) + `git commit` message tiếng Việt mô tả T6.
5. Ghi report vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-p2-6-report.md`.

## Report contract (ghi vào file report, trả về chat chỉ: status + commit hash + 1 dòng test + concerns)
- Xác nhận: const, method, helper, use thêm đúng chỗ; không đụng getDataAccounting/postAccounting.
- Ghi rõ đã verify các entity/cột nào tồn tại (nếu chạy query thì ghi lại).
- Nêu concern nếu có (vd: quan hệ product_export_requests trả read-only, hoặc trip->name null).
- Nhắc lại Ruling T6-A: trên DB gộp hiện tại method no-op (0 chuyến có invoiceable=DeliveryTrip) — đây KHÔNG phải lỗi.

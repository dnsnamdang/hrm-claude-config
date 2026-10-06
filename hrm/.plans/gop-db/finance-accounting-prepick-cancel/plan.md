# Phiếu huỷ hàng giữ kế toán (ERP → HRM) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

> @junfoke · nhánh `feat/finance-accounting-prepick-cancel` (từ `gop_db`, cả 2 repo) · design: `./design.md`

**Goal:** Port màn "Phiếu huỷ hàng giữ kế toán" (bảng ERP `accounting_prepick_cancels`) sang HRM
phân hệ Tài chính → Giữ hàng: danh sách, lập phiếu (= trừ tồn giữ FIFO), chi tiết, in, Excel, lịch sử.

**Architecture:** BE `Modules/Finance` theo khuôn màn `PrepickCancel` đã port (entity + service +
controller + FormRequest + Resource + blade in), mọi thao tác tồn giữ đi qua `PrepickStockService`.
Logic chuẩn hoá dòng (gộp, chặn trùng KH, quy đổi ĐVT) tách thành class thuần để unit test không cần
DB. FE Nuxt 2 bộ chuẩn V2, dùng lại popup chọn hàng + panel lịch sử của nhóm Giữ hàng.

**Tech Stack:** Laravel (hrm-api, PHPUnit), Nuxt 2 / Vue 2 (hrm-client), ExcelJS, MySQL `gop_db`.

**Spec:** `docs/superpowers/specs/gop-db/2026-09-28-finance-accounting-prepick-cancel-design.md`

## Global Constraints

- Code sửa trong worktree `hrm-api/.worktrees/gop-db` và `hrm-client/.worktrees/gop-db`, trên nhánh
  `feat/finance-accounting-prepick-cancel` tách từ `gop_db`. **Không commit / không push** (rule
  project) — bước "Commit" trong từng task thay bằng "đánh `[x]` + ghi checkpoint".
- Không đổi schema 3 bảng ERP. Bảng mới duy nhất `accounting_prepick_cancel_history`, migration ở
  `hrm-api/database/migrations/`.
- `prepick_logs.objectable_type` = `'App\Model\Warehouse\AccountingPrepickCancelDetailCustomer'`,
  `objectable_id` = id dòng `accounting_prepick_cancel_detail_customers`.
- Mã phiếu `KTPHHG-` + `generateCode(5, $id)`.
- Quyền: chỉ `Quản lý giữ hàng`, kiểm qua trait `ChecksEmployeePermission`; KHÔNG middleware
  `checkPermission` / `erpPermission`. Danh sách lọc `company_id` = công ty người đăng nhập.
- Không ghi thêm dòng vào `report_templates`. In = popup `ReportPrintPreviewModal` (skill `print-page`
  mục 0 + mục 8), KHÔNG dựng trang `/print`.
- Route tĩnh khai TRƯỚC `/{id}`.
- Số hiển thị chuẩn quốc tế `1,234,567.89`; ô rỗng để trống (không in `—`).
- Nút không dùng được thì ẨN, không disable. Vượt trần thì báo đỏ, không tự kéo số về.
- Ô số lượng chặn chữ/ký tự đặc biệt/số âm bằng `utils/number-input.js → sanitizeNumberEvent`
  (`:value` + `@input.native`), không truyền `max`.
- Thao tác xong quay về danh sách.
- Test ghi DB: sao lưu trước, chỉ phiếu tự tạo, dọn xong đối chiếu từng cột với bản sao lưu.
- Đọc skill trước khi làm phần tương ứng: `erp-to-hrm-screen`, `list-page`, `button-convention`,
  `modal-popup`, `form-validate`, `unsaved-changes`, `print-page`, `entity-history`,
  `notification-convention`, `select-and-input-state`.

## Review Focus

1. **Cùng một KH chọn 2 lần trong 1 hàng hoá** → phải 422 "Khách hàng bị chọn trùng", không trừ gì
   (Task 2 test `test_duplicate_customer_in_same_product_rejected` + Task 5 E2E bước 5).
2. **Kế toán khác công ty với NV chủ lô** → lô tra theo công ty CHỦ LÔ (tiền lệ
   `PrepickCancelService::store()`), popup / cột Có thể huỷ / trừ tồn dùng cùng công ty đó, nên số
   hiện ra = số trừ được (Task 5 E2E bước 6).
3. **ĐVT hệ số > 1, số lẻ** (vd hộp = 12 cái, huỷ 0.5 hộp) → `cancel_qty = 6`, so tồn theo ĐV cơ
   bản; cột Có thể huỷ trên form = `available / hệ số` (Task 2 test `test_cancel_qty_uses_coefficient`
   + Task 8 kiểm tay).
4. **Người khác vừa trừ tồn giữa lúc mở form và bấm Duyệt** → BE 422 từ `deductFifo`, rollback toàn
   phiếu, FE hiện lỗi dưới bảng (Task 5 E2E bước 5 — giả lập bằng cách giảm tay `prepick_details.qty`
   trước POST).
5. **Hàng hoá thiếu thương hiệu / model** → lưu được, snapshot `''` / `0` (Task 2 test
   `test_snapshot_defaults_when_brand_model_missing` + Task 5 E2E chọn 1 hàng như vậy nếu có).

---

## Bản đồ file

### hrm-api (`.worktrees/gop-db`)

| File | Trách nhiệm |
|---|---|
| Create `Modules/Finance/Entities/AccountingPrepickCancel/AccountingPrepickCancel.php` | bảng phiếu, quan hệ, `canView()`, `searchByFilter()`, `generateCode()`, `SORTABLE_COLUMNS` |
| Create `.../AccountingPrepickCancelDetail.php` | dòng hàng hoá (snapshot) |
| Create `.../AccountingPrepickCancelDetailCustomer.php` | dòng KH, hằng `ERP_TYPE` |
| Create `.../AccountingPrepickCancelHistory.php` | bảng lịch sử mới |
| Create `.../AccountingPrepickCancelLines.php` | **class thuần**: chuẩn hoá + kiểm dòng (không DB) |
| Create `Modules/Finance/Services/AccountingPrepickCancelService.php` | search/meta/show/store/stock/customers/print/export/notify |
| Create `Modules/Finance/Services/AccountingPrepickCancelHistoryService.php` | `logCreate()`, `getLogs()` |
| Create `Modules/Finance/Http/Controllers/V1/AccountingPrepickCancelController.php` | 10 action |
| Create `Modules/Finance/Http/Requests/AccountingPrepickCancel/AccountingPrepickCancelStoreRequest.php` | validate POST |
| Create `Modules/Finance/Transformers/AccountingPrepickCancelResource/AccountingPrepickCancelListResource.php` | dòng danh sách |
| Create `Modules/Finance/Resources/views/prints/accounting-prepick-cancel.blade.php` | in phiếu A4 dọc |
| Create `Modules/Finance/Resources/views/prints/accounting-prepick-cancel-list.blade.php` | in DS A4 ngang |
| Create `database/migrations/2026_09_28_000001_create_accounting_prepick_cancel_history_table.php` | bảng lịch sử |
| Create `tests/Unit/AccountingPrepickCancelLinesTest.php` | unit test class thuần |
| Modify `Modules/Finance/Services/PrepickStockService.php` | `deductFifo()` +1 tham số; +`holdingCustomersOfProduct()` |
| Modify `Modules/Finance/Services/PrepickStockReportService.php` | `hrm_path` cho map kế toán |
| Modify `Modules/Finance/Routes/api.php` | nhóm route `/accounting-prepick-cancels` |

### hrm-client (`.worktrees/gop-db`)

| File | Trách nhiệm |
|---|---|
| Create `pages/finance/accounting-prepick-cancels/index.vue` | danh sách V2 + popup in + popup lịch sử |
| Create `pages/finance/accounting-prepick-cancels/create.vue` | vỏ trang tạo (`beforeRouteLeave`) |
| Create `pages/finance/accounting-prepick-cancels/_id/index.vue` | chi tiết |
| Create `pages/finance/accounting-prepick-cancels/components/AccountingPrepickCancelForm.vue` | form tạo |
| Create `pages/finance/accounting-prepick-cancels/components/AccountingPrepickCancelDetail.vue` | màn chi tiết chỉ đọc |
| Create `pages/finance/accounting-prepick-cancels/components/export-excel.js` | ExcelJS |
| Modify `components/subsystem-menu/finance.js` | gắn `link` |

Khuôn mẫu copy (KHÔNG tự phát minh): `pages/finance/prepick-cancels/*`,
`Modules/Finance/{Entities/PrepickCancel,Services/PrepickCancel*,Http/Controllers/V1/PrepickCancelController.php}`.

---

## Task 0: Chuẩn bị nhánh + sao lưu

**Files:** không sửa code.

- [x] **Step 1: Tạo nhánh ở cả 2 worktree**

```bash
cd /d/CompanyProject/hrm/hrm-api/.worktrees/gop-db && git status --short && git pull --ff-only && git checkout -b feat/finance-accounting-prepick-cancel
cd /d/CompanyProject/hrm/hrm-client/.worktrees/gop-db && git status --short && git pull --ff-only && git checkout -b feat/finance-accounting-prepick-cancel
```

Expected: `git status` rỗng trước khi tạo nhánh. Có thay đổi dở của người khác → DỪNG, hỏi user.

> ⚠️ Worktree `.worktrees/gop-db` đang giữ `gop_db`; `checkout -b` ở đây sẽ đưa worktree sang nhánh
> mới. Nếu user muốn giữ worktree ở `gop_db`, thay bằng `git worktree add ../.worktrees/accounting-prepick-cancel -b feat/finance-accounting-prepick-cancel gop_db`
> (nhớ symlink `vendor` / `node_modules` như worktree cũ). **Hỏi user chọn cách nào trước Step 1.**

- [x] **Step 2: Đo số liệu gốc + sao lưu 5 bảng** (qua `php artisan tinker` trong hrm-api)

```php
foreach (['accounting_prepick_cancels','accounting_prepick_cancel_details','accounting_prepick_cancel_detail_customers','prepick_details','prepick_logs'] as $t) {
    DB::statement("CREATE TABLE bak_{$t}_20260928 AS SELECT * FROM {$t}");
    echo $t.': '.DB::table($t)->count().PHP_EOL;
}
echo 'SUM prepick_details.qty = '.DB::table('prepick_details')->sum('qty').PHP_EOL;
echo 'KH trùng trong 1 dòng hàng (dữ liệu ERP cũ): '.DB::table('accounting_prepick_cancel_detail_customers')
    ->select('accounting_prepick_cancel_detail_id','customer_id')->groupBy('accounting_prepick_cancel_detail_id','customer_id')
    ->havingRaw('COUNT(*) > 1')->get()->count().PHP_EOL;
```

Expected: ≈600 / 1.616 / 1.641 dòng cho 3 bảng kế toán. Ghi mọi con số vào checkpoint.

- [x] **Step 3: Ghi checkpoint Task 0** (cuối file này).

---

## Task 1: Sửa `PrepickStockService` (dùng chung) + map lịch sử giữ hàng

**Files:**
- Modify: `Modules/Finance/Services/PrepickStockService.php` (`deductFifo` :458-545, thêm hàm mới sau `holdingCustomers` :359-398)
- Modify: `Modules/Finance/Services/PrepickStockReportService.php:954-961`

**Interfaces:**
- Produces: `deductFifo(int $productId, int $employeeId, ?int $customerId, ?int $companyId, float $qty, int $prepickCancelId, string $label = '', string $objectableType = PrepickCancel::ERP_PREPICK_CANCEL_TYPE): int`
- Produces: `holdingCustomersOfProduct(int $employeeId, int $productId, ?int $companyId): array` →
  `[['customer_id'=>int,'customer_code'=>?string,'customer_name'=>string,'available_qty'=>float], ...]`

- [x] **Step 1: Thêm tham số `$objectableType`**

Trong chữ ký thêm tham số cuối và trong vòng lặp thay dòng gán cứng:

```php
        string $label = '',
        string $objectableType = PrepickCancel::ERP_PREPICK_CANCEL_TYPE
    ): int {
```

```php
            $log->objectable_id = $prepickCancelId;
            // Chuỗi lớp của ERP. Mặc định = phiếu hủy thường (PrepickCancel::ERP_PREPICK_CANCEL_TYPE);
            // màn Phiếu huỷ hàng giữ KẾ TOÁN truyền AccountingPrepickCancelDetailCustomer::ERP_TYPE
            // và `$prepickCancelId` là id DÒNG KHÁCH HÀNG (quy ước ERP, map ngược ở PrepickStockReportService).
            $log->objectable_type = $objectableType;
```

Bổ sung docblock: `@param string $objectableType chuỗi lớp ERP ghi vào prepick_logs.objectable_type`
và sửa mô tả `$prepickCancelId` → "giá trị ghi vào `prepick_logs.objectable_id`".

- [x] **Step 2: Thêm `holdingCustomersOfProduct()`** ngay sau `holdingCustomers()`

```php
    /**
     * Khách hàng đang được NV giữ MỘT hàng hoá + số CÓ THỂ HỦY của từng khách (ĐV cơ bản).
     * Dùng ở: màn Phiếu huỷ hàng giữ kế toán (dropdown KH trên từng dòng hàng).
     *
     * Vá ERP `ProductsController@getData` (:3201-3207): ERP join `prepick_details` không GROUP BY
     * (KH có nhiều lô bị lặp) và không lọc công ty (hiện KH của lô công ty khác, lúc trừ lại không
     * tìm ra lô). KH không có bản ghi `customers` (lỗ dữ liệu DB gộp) vẫn trả về, tên rỗng.
     *
     * @return array<int, array{customer_id:int, customer_code:?string, customer_name:string, available_qty:float}>
     */
    public function holdingCustomersOfProduct(int $employeeId, int $productId, ?int $companyId): array
    {
        $rows = $this->baseQuery($employeeId, null, $companyId)
            ->leftJoin('customers as c', 'c.id', '=', 'pd.customer_id')
            ->where('pd.product_id', $productId)
            ->where('pd.qty', '>', 0)
            ->whereNotNull('pd.customer_id')
            ->groupBy('pd.customer_id', 'c.code', 'c.fullname')
            ->orderBy('c.fullname')
            ->get(['pd.customer_id', 'c.code', 'c.fullname']);

        $result = [];
        foreach ($rows as $row) {
            $customerId = (int) $row->customer_id;
            $available = $this->availableQty($productId, $employeeId, $customerId, $companyId);
            if ($available <= 0) {
                continue;
            }
            $result[] = [
                'customer_id' => $customerId,
                'customer_code' => $row->code,
                'customer_name' => trim(($row->code ? $row->code . ' - ' : '') . ($row->fullname ?? '')),
                'available_qty' => $available,
            ];
        }

        return $result;
    }
```

(N+1 theo số KH của 1 hàng — thường ≤ 10; chấp nhận. Đo ở Task 5, > 30 KH thì gộp `pendingExportQty`.)

- [x] **Step 3: Gắn `hrm_path`** trong `PrepickStockReportService.php` map `AccountingPrepickCancelDetailCustomer`:

```php
            'hrm_path' => '/finance/accounting-prepick-cancels',
```

Sửa luôn comment `// ERP BỎ SÓT — 1.645 dòng log` thành `// ERP BỎ SÓT — 1.645 dòng log. HRM port 2026-09-28.`

- [x] **Step 4: Kiểm cú pháp + hồi quy chỗ gọi cũ**

```bash
php -l Modules/Finance/Services/PrepickStockService.php && php -l Modules/Finance/Services/PrepickStockReportService.php
grep -rn "deductFifo(" Modules/ | grep -v "function deductFifo"
```

Expected: `No syntax errors`; chỗ gọi hiện có (PrepickCancelService) truyền ≤ 7 tham số → không đổi hành vi.

- [x] **Step 5: Đánh `[x]`, ghi checkpoint.**

---

## Task 2: Class thuần `AccountingPrepickCancelLines` + unit test (TDD)

**Files:**
- Create: `Modules/Finance/Entities/AccountingPrepickCancel/AccountingPrepickCancelLines.php`
- Test: `tests/Unit/AccountingPrepickCancelLinesTest.php`

**Interfaces:**
- Produces: `AccountingPrepickCancelLines::normalize(array $products, array $productInfo, array $coefficients): array`
  - `$products`: payload FE `[['product_id'=>int,'customers'=>[['customer_id'=>int,'qty'=>num,'unit_id'=>int],...]],...]`
  - `$productInfo`: `product_id => ['name'=>?string,'code'=>?string,'brand_id'=>?int,'brand_name'=>?string,'model_id'=>?int,'model_name'=>?string]`
  - `$coefficients`: `"product_id:unit_id" => ['coefficient'=>float,'unit_name'=>string]` (thiếu key = ĐVT không thuộc hàng)
  - Trả `[['product_id','product_name','product_code','brand_id','brand_name','model_id','model_name','customers'=>[['customer_id','qty','unit_id','unit_name','unit_coefficient','cancel_qty'],...]],...]`
  - Ném `\InvalidArgumentException` với mảng lỗi trong `getErrors()` — dùng class con `AccountingPrepickCancelLinesException`.

- [x] **Step 1: Viết test thất bại**

```php
<?php

namespace Tests\Unit;

use Modules\Finance\Entities\AccountingPrepickCancel\AccountingPrepickCancelLines;
use Modules\Finance\Entities\AccountingPrepickCancel\AccountingPrepickCancelLinesException;
use PHPUnit\Framework\TestCase;

/**
 * Chuẩn hoá dòng Phiếu huỷ hàng giữ kế toán — không phụ thuộc DB/auth.
 * Vá ERP lỗi #4 (trùng KH), #8 (thiếu brand/model), #11 (dòng 0).
 */
class AccountingPrepickCancelLinesTest extends TestCase
{
    private function info(): array
    {
        return [
            10 => ['name' => 'Máy A', 'code' => 'MA', 'brand_id' => 3, 'brand_name' => 'Hãng X', 'model_id' => 7, 'model_name' => 'M7'],
            20 => ['name' => 'Máy B', 'code' => 'MB', 'brand_id' => null, 'brand_name' => null, 'model_id' => null, 'model_name' => null],
        ];
    }

    private function coef(): array
    {
        return [
            '10:1' => ['coefficient' => 1.0, 'unit_name' => 'Cái'],
            '10:2' => ['coefficient' => 12.0, 'unit_name' => 'Hộp'],
            '20:1' => ['coefficient' => 1.0, 'unit_name' => 'Cái'],
        ];
    }

    public function test_cancel_qty_uses_coefficient(): void
    {
        $lines = AccountingPrepickCancelLines::normalize([
            ['product_id' => 10, 'customers' => [['customer_id' => 5, 'qty' => 0.5, 'unit_id' => 2]]],
        ], $this->info(), $this->coef());

        $this->assertSame(6.0, $lines[0]['customers'][0]['cancel_qty']);
        $this->assertSame('Hộp', $lines[0]['customers'][0]['unit_name']);
        $this->assertSame(12.0, $lines[0]['customers'][0]['unit_coefficient']);
    }

    public function test_zero_rows_dropped_and_empty_product_dropped(): void
    {
        $lines = AccountingPrepickCancelLines::normalize([
            ['product_id' => 10, 'customers' => [
                ['customer_id' => 5, 'qty' => 0, 'unit_id' => 1],
                ['customer_id' => 6, 'qty' => 2, 'unit_id' => 1],
            ]],
            ['product_id' => 20, 'customers' => [['customer_id' => 5, 'qty' => 0, 'unit_id' => 1]]],
        ], $this->info(), $this->coef());

        $this->assertCount(1, $lines);
        $this->assertCount(1, $lines[0]['customers']);
        $this->assertSame(6, $lines[0]['customers'][0]['customer_id']);
    }

    public function test_all_zero_rejected(): void
    {
        try {
            AccountingPrepickCancelLines::normalize([
                ['product_id' => 10, 'customers' => [['customer_id' => 5, 'qty' => 0, 'unit_id' => 1]]],
            ], $this->info(), $this->coef());
            $this->fail('Phải ném lỗi');
        } catch (AccountingPrepickCancelLinesException $e) {
            $this->assertArrayHasKey('products', $e->getErrors());
        }
    }

    public function test_duplicate_customer_in_same_product_rejected(): void
    {
        try {
            AccountingPrepickCancelLines::normalize([
                ['product_id' => 10, 'customers' => [
                    ['customer_id' => 5, 'qty' => 1, 'unit_id' => 1],
                    ['customer_id' => 5, 'qty' => 1, 'unit_id' => 2],
                ]],
            ], $this->info(), $this->coef());
            $this->fail('Phải ném lỗi');
        } catch (AccountingPrepickCancelLinesException $e) {
            $this->assertArrayHasKey('products.0.customers.1.customer_id', $e->getErrors());
        }
    }

    public function test_same_customer_in_different_products_allowed(): void
    {
        $lines = AccountingPrepickCancelLines::normalize([
            ['product_id' => 10, 'customers' => [['customer_id' => 5, 'qty' => 1, 'unit_id' => 1]]],
            ['product_id' => 20, 'customers' => [['customer_id' => 5, 'qty' => 1, 'unit_id' => 1]]],
        ], $this->info(), $this->coef());

        $this->assertCount(2, $lines);
    }

    public function test_duplicate_product_rejected(): void
    {
        try {
            AccountingPrepickCancelLines::normalize([
                ['product_id' => 10, 'customers' => [['customer_id' => 5, 'qty' => 1, 'unit_id' => 1]]],
                ['product_id' => 10, 'customers' => [['customer_id' => 6, 'qty' => 1, 'unit_id' => 1]]],
            ], $this->info(), $this->coef());
            $this->fail('Phải ném lỗi');
        } catch (AccountingPrepickCancelLinesException $e) {
            $this->assertArrayHasKey('products.1.product_id', $e->getErrors());
        }
    }

    public function test_unit_not_belonging_to_product_rejected(): void
    {
        try {
            AccountingPrepickCancelLines::normalize([
                ['product_id' => 20, 'customers' => [['customer_id' => 5, 'qty' => 1, 'unit_id' => 2]]],
            ], $this->info(), $this->coef());
            $this->fail('Phải ném lỗi');
        } catch (AccountingPrepickCancelLinesException $e) {
            $this->assertArrayHasKey('products.0.customers.0.unit_id', $e->getErrors());
        }
    }

    public function test_snapshot_defaults_when_brand_model_missing(): void
    {
        $lines = AccountingPrepickCancelLines::normalize([
            ['product_id' => 20, 'customers' => [['customer_id' => 5, 'qty' => 1, 'unit_id' => 1]]],
        ], $this->info(), $this->coef());

        $this->assertSame('', $lines[0]['brand_name']);
        $this->assertSame(0, $lines[0]['brand_id']);
        $this->assertSame('', $lines[0]['model_name']);
        $this->assertSame(0, $lines[0]['model_id']);
    }
}
```

- [x] **Step 2: Chạy, xác nhận FAIL**

Run: `vendor/bin/phpunit tests/Unit/AccountingPrepickCancelLinesTest.php`
Expected: FAIL — `Class "...AccountingPrepickCancelLines" not found`.

- [x] **Step 3: Cài đặt**

`AccountingPrepickCancelLinesException.php` (cùng thư mục):

```php
<?php

namespace Modules\Finance\Entities\AccountingPrepickCancel;

/** Lỗi chuẩn hoá dòng phiếu — mang mảng lỗi theo key ô trên form để service đổi sang 422. */
class AccountingPrepickCancelLinesException extends \InvalidArgumentException
{
    /** @var array<string, string> */
    private $errors;

    public function __construct(array $errors)
    {
        parent::__construct(reset($errors) ?: 'Dữ liệu không hợp lệ.');
        $this->errors = $errors;
    }

    public function getErrors(): array
    {
        return $this->errors;
    }
}
```

`AccountingPrepickCancelLines.php`:

```php
<?php

namespace Modules\Finance\Entities\AccountingPrepickCancel;

/**
 * Chuẩn hoá payload lập Phiếu huỷ hàng giữ kế toán. THUẦN — không DB, không auth — để unit test.
 * Service nạp sẵn `$productInfo` + `$coefficients` rồi gọi normalize().
 *
 * Vá ERP:
 *   #4  chọn trùng KH trong 1 hàng hoá → mỗi dòng kiểm riêng với toàn bộ tồn nên tổng vượt vẫn qua.
 *   #8  hàng thiếu thương hiệu/model → `$product->brand->name` lỗi 500 (cột NOT NULL) → ''/0.
 *   #11 dòng KH qty = 0 bị bỏ nhưng dòng hàng vẫn ghi → hàng hoá rỗng KH → bỏ hẳn.
 */
class AccountingPrepickCancelLines
{
    public static function normalize(array $products, array $productInfo, array $coefficients): array
    {
        $errors = [];
        $lines = [];
        $seenProducts = [];

        foreach (array_values($products) as $pIndex => $product) {
            $productId = (int) ($product['product_id'] ?? 0);

            if (isset($seenProducts[$productId])) {
                $errors["products.$pIndex.product_id"] = 'Hàng hoá bị chọn trùng.';
                continue;
            }
            $seenProducts[$productId] = true;

            $info = $productInfo[$productId] ?? null;
            if ($info === null) {
                $errors["products.$pIndex.product_id"] = 'Hàng hoá không tồn tại.';
                continue;
            }

            $customers = [];
            $seenCustomers = [];
            foreach (array_values((array) ($product['customers'] ?? [])) as $cIndex => $row) {
                $customerId = (int) ($row['customer_id'] ?? 0);
                $key = "products.$pIndex.customers.$cIndex";

                if (isset($seenCustomers[$customerId])) {
                    $errors["$key.customer_id"] = 'Khách hàng bị chọn trùng trong cùng một hàng hoá.';
                    continue;
                }
                $seenCustomers[$customerId] = true;

                $qty = (float) ($row['qty'] ?? 0);
                if ($qty <= 0) {
                    continue;
                }

                $unitId = (int) ($row['unit_id'] ?? 0);
                $unit = $coefficients["$productId:$unitId"] ?? null;
                if ($unit === null) {
                    $errors["$key.unit_id"] = 'Đơn vị tính không thuộc hàng hoá này.';
                    continue;
                }

                $coefficient = (float) $unit['coefficient'];
                $customers[] = [
                    'customer_id' => $customerId,
                    'qty' => $qty,
                    'unit_id' => $unitId,
                    'unit_name' => (string) $unit['unit_name'],
                    'unit_coefficient' => $coefficient,
                    'cancel_qty' => round($qty * $coefficient, 2),
                ];
            }

            if (empty($customers)) {
                continue;
            }

            $lines[] = [
                'product_id' => $productId,
                'product_name' => (string) ($info['name'] ?? ''),
                'product_code' => (string) ($info['code'] ?? ''),
                'brand_id' => (int) ($info['brand_id'] ?? 0),
                'brand_name' => (string) ($info['brand_name'] ?? ''),
                'model_id' => (int) ($info['model_id'] ?? 0),
                'model_name' => (string) ($info['model_name'] ?? ''),
                'customers' => $customers,
            ];
        }

        if (!empty($errors)) {
            throw new AccountingPrepickCancelLinesException($errors);
        }

        if (empty($lines)) {
            throw new AccountingPrepickCancelLinesException([
                'products' => 'Phải có ít nhất 1 dòng Duyệt huỷ lớn hơn 0.',
            ]);
        }

        return $lines;
    }
}
```

- [x] **Step 4: Chạy, xác nhận PASS**

Run: `vendor/bin/phpunit tests/Unit/AccountingPrepickCancelLinesTest.php`
Expected: `OK (8 tests, ...)`.

- [x] **Step 5: Đánh `[x]`, ghi checkpoint.**

---

## Task 3: Entity + migration lịch sử + danh sách (BE đọc)

**Files:**
- Create: 4 entity trong `Modules/Finance/Entities/AccountingPrepickCancel/` (trừ `Lines` đã có)
- Create: `database/migrations/2026_09_28_000001_create_accounting_prepick_cancel_history_table.php`
- Create: `Modules/Finance/Transformers/AccountingPrepickCancelResource/AccountingPrepickCancelListResource.php`
- Create: `Modules/Finance/Services/AccountingPrepickCancelService.php` (phần đọc)
- Create: `Modules/Finance/Http/Controllers/V1/AccountingPrepickCancelController.php` (`index`, `show`)
- Modify: `Modules/Finance/Routes/api.php` (thêm nhóm sau nhóm `/prepick-cancels` :737-751)

**Interfaces:**
- Consumes: trait `ChecksEmployeePermission` (`currentEmployeeHasPermission`, `currentEmployeeIsSuperAdmin`, `currentCompanyId`) — copy cách dùng từ `PrepickCancel.php`.
- Produces: `AccountingPrepickCancel::PERMISSION_QUAN_LY_GIU_HANG = 'Quản lý giữ hàng'`,
  `AccountingPrepickCancel::canManage(): bool` (static — super admin hoặc có quyền),
  `canView(): bool`, `searchByFilter($request): Builder`, `generateCode(): void`,
  `AccountingPrepickCancelDetailCustomer::ERP_TYPE`,
  service `searchByFilter(Request)`, `meta(): array` (`['can_manage'=>bool]`),
  `findForShow(int $id): AccountingPrepickCancel`, `detailData(AccountingPrepickCancel): array`,
  `assertCanManage(): void` (ném `AuthorizationException` 403).

- [x] **Step 1: Entity `AccountingPrepickCancel`** — copy khung `PrepickCancel.php`, điều chỉnh:

```php
class AccountingPrepickCancel extends Model
{
    use ChecksEmployeePermission;

    protected $table = 'accounting_prepick_cancels';

    const PERMISSION_QUAN_LY_GIU_HANG = 'Quản lý giữ hàng';

    protected $fillable = ['code', 'employee_id', 'note', 'company_id', 'created_by', 'updated_by'];

    public const SORTABLE_COLUMNS = ['code' => 'code', 'createdAt' => 'created_at'];

    public function products() { return $this->hasMany(AccountingPrepickCancelDetail::class, 'accounting_prepick_cancel_id', 'id'); }
    public function employee() { return $this->belongsTo(Employee::class, 'employee_id', 'id'); }       // NV bị huỷ
    public function employee_create() { return $this->belongsTo(Employee::class, 'created_by', 'id'); }
    public function company() { return $this->belongsTo(Company::class, 'company_id', 'id'); }

    public function generateCode(): void
    {
        $this->code = 'KTPHHG-' . generateCode(5, $this->id);
        $this->save();
    }

    public static function canManage(): bool
    {
        return self::currentEmployeeIsSuperAdmin()
            || self::currentEmployeeHasPermission(self::PERMISSION_QUAN_LY_GIU_HANG);
    }

    /** Vá ERP lỗi #2 — ERP comment mất canView() ở show(). Giữ phạm vi ERP: quyền + cùng công ty. */
    public function canView(): bool
    {
        if (!self::canManage()) {
            return false;
        }
        if (self::currentEmployeeIsSuperAdmin()) {
            return true;
        }
        $companyId = self::currentCompanyId();

        return $companyId !== null && (int) $this->company_id === $companyId;
    }
    // searchByFilter / applyFilters / applySort: xem Step 2
}
```

(Viết đầy đủ docblock đầu class theo khuôn `PrepickCancel.php`: nghiệp vụ, không vòng đời, 11 lỗi ERP.)

- [x] **Step 2: `searchByFilter()`** — phạm vi ERP + bộ lọc spec §5.4:

```php
    public static function searchByFilter($request)
    {
        $query = self::query()->with(['employee.info', 'employee_create.info']);

        if (!self::currentEmployeeIsSuperAdmin()) {
            $companyId = self::currentCompanyId();
            $companyId === null ? $query->whereRaw('1 = 0') : $query->where('company_id', $companyId);
        }
        // Không port tham số ERP `?company=` — không có UI gửi, để lại là lỗ xem chéo công ty.

        if ($request->filled('keyword')) {
            $query->where('code', 'like', '%' . $request->input('keyword') . '%');
        }
        if ($request->filled('code')) {
            $query->where('code', 'like', '%' . $request->input('code') . '%');
        }
        if ($request->filled('employee_id')) {
            $query->where('employee_id', $request->input('employee_id'));
        }
        if ($request->filled('created_by')) {
            $query->where('created_by', $request->input('created_by'));
        }
        if ($request->filled('startDate')) {
            $query->whereDate('created_at', '>=', $request->input('startDate'));
        }
        if ($request->filled('endDate')) {
            // whereDate: lấy trọn ngày cuối (ERP so `<= Y-m-d` → mất phiếu trong ngày cuối).
            $query->whereDate('created_at', '<=', $request->input('endDate'));
        }
        if ($request->filled('product')) {
            $product = $request->input('product');
            $query->whereHas('products', function ($q) use ($product) {
                $q->where('product_name', 'like', '%' . $product . '%')
                    ->orWhere('product_code', 'like', '%' . $product . '%');
            });
        }

        $sortBy = $request->input('sort_by');
        $sortDir = strtolower($request->input('sort_dir', 'desc')) === 'asc' ? 'asc' : 'desc';
        if ($sortBy && isset(self::SORTABLE_COLUMNS[$sortBy])) {
            $query->orderBy(self::SORTABLE_COLUMNS[$sortBy], $sortDir);
        } else {
            $query->orderBy('created_at', 'desc');
        }

        return $query->orderBy('id', 'desc');
    }
```

- [x] **Step 3: 3 entity còn lại**

- `AccountingPrepickCancelDetail`: `$table = 'accounting_prepick_cancel_details'`, `customers()` hasMany `AccountingPrepickCancelDetailCustomer` (`accounting_prepick_cancel_detail_id`).
- `AccountingPrepickCancelDetailCustomer`: `$table = 'accounting_prepick_cancel_detail_customers'`,
  `const ERP_TYPE = 'App\Model\Warehouse\AccountingPrepickCancelDetailCustomer';`, `customer()` belongsTo `Modules\Human\Entities\Customer`.
- `AccountingPrepickCancelHistory`: copy `PrepickCancelHistory.php`, đổi `$table = 'accounting_prepick_cancel_history'`, cột `accounting_prepick_cancel_id`.

- [x] **Step 4: Migration** — copy `2026_08_15_000003_create_prepick_cancel_history_table.php`, đổi tên bảng + cột khoá `accounting_prepick_cancel_id`, tên index thủ công `apc_history_cancel_id_idx`, `apc_history_company_idx`. Chạy:

```bash
php artisan migrate --path=database/migrations/2026_09_28_000001_create_accounting_prepick_cancel_history_table.php
```

Expected: `Migrated`. Chạy `php artisan migrate:status | grep accounting_prepick` xác nhận.

- [x] **Step 5: ListResource** — copy `PrepickCancelListResource`, trả mỗi dòng:
`id`, `code`, `employeeName` (`optional($o->employee->info)->fullname`), `createdByName`, `createdAt`
(`Helper::formatDate`), `note`.

- [x] **Step 6: Service phần đọc + controller `index`/`show` + route**

Controller mở đầu mọi action bằng `$this->service->assertCanManage();`. Route:

```php
    Route::group(['prefix' => '/accounting-prepick-cancels'], function () {
        Route::get('/', [AccountingPrepickCancelController::class, 'index']);

        // Route TĨNH — PHẢI khai TRƯỚC /{id}.
        Route::get('/employees', [AccountingPrepickCancelController::class, 'employees']);
        Route::get('/stock', [AccountingPrepickCancelController::class, 'stock']);
        Route::get('/product-customers', [AccountingPrepickCancelController::class, 'productCustomers']);
        Route::get('/export', [AccountingPrepickCancelController::class, 'export']);
        Route::get('/print-list-data', [AccountingPrepickCancelController::class, 'printListData']);

        Route::post('/', [AccountingPrepickCancelController::class, 'store']);

        Route::get('/{id}/print-data', [AccountingPrepickCancelController::class, 'printData']);
        Route::get('/{id}/histories', [AccountingPrepickCancelController::class, 'histories']);
        Route::get('/{id}', [AccountingPrepickCancelController::class, 'show']);
    });
```

Các action chưa viết ở task này để stub trả `abort(501)` — Task 4/5 thay.

`detailData()` trả: `id, code, note, created_at (d/m/Y H:i), employee {id, code, name, department_name},
created_by_name, products[] {product_id, product_name, product_code, model_name, brand_name,
customers[] {customer_id, customer_name, qty, unit_name, unit_coefficient, cancel_qty}}`.

- [x] **Step 7: Verify HTTP** (token 3 loại TK — cách lấy token: mục Phân quyền "cách test" của dự án)

```bash
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/finance/accounting-prepick-cancels?per_page=5" | head -c 800
```

Expected: TK có `Quản lý giữ hàng` → `total` = `SELECT COUNT(*) FROM accounting_prepick_cancels WHERE company_id = <cty>`;
TK không quyền → 403; `/{id}` phiếu công ty khác → 403/404; lọc `endDate=<ngày có phiếu>` vẫn ra phiếu ngày đó.

- [x] **Step 8: Đánh `[x]`, ghi checkpoint.**

---

## Task 4: API phục vụ form — employees / stock / product-customers

**Files:** Modify service + controller (Task 3).

**Interfaces:**
- Consumes: `PrepickStockService::searchHoldingProducts()`, `holdingCustomersOfProduct()`, `PrepickCancelRequestService::employeeCompanyId(int): ?int` (public).
- Produces (JSON):
  - `GET /employees?keyword=` → `{data: [{id, code, name}]}` — NV đang làm việc (bám cách lọc "đang làm việc" của ERP `Employee::getEmployeeActive()`; tìm trong HRM helper đã có trước khi viết query mới: `grep -rn "getEmployeeActive\|employeesActive" Modules/ app/`), limit 50, có `keyword`.
  - `GET /stock?employee_id&name&code&page&per_page&exclude_product_ids[]` → shape y như `/prepick-cancel-requests/stock` (để `PrepickStockSearchModal` dùng nguyên).
  - `GET /product-customers?employee_id&product_id` → `{data: {customers: [...holdingCustomersOfProduct], units: [{unit_id, unit_name, unit_coefficient, is_base}]}}`.

- [x] **Step 1: `ownerCompanyId(int $employeeId): ?int`** trong service = `employeeCompanyId()` — **lô tra theo công ty CHỦ LÔ** (tiền lệ `PrepickCancelService::store()`), dùng chung cho `/stock`, `/product-customers`, `store()`.

- [x] **Step 2: `stock()`**

```php
    public function stock(Request $request)
    {
        $employeeId = (int) $request->input('employee_id');

        return $this->stock->searchHoldingProducts(
            $employeeId,
            null,
            $this->ownerCompanyId($employeeId),
            [
                'name' => $request->input('name'),
                'code' => $request->input('code'),
                'exclude_ids' => (array) $request->input('exclude_product_ids', []),
            ],
            (int) $request->input('per_page', 10)
        );
    }
```

Controller trả giống `PrepickCancelRequestController::stock` (copy cách bọc paginate).

- [x] **Step 3: `productCustomers()`** — `units` lấy từ `product_units` join `units` của hàng
(tìm hàm có sẵn trước: `grep -n "product_units" Modules/Finance/Services/PrepickStockService.php` —
`unitCoefficient()`/`baseUnits()` đọc cùng bảng; nếu chưa có hàm trả **tất cả** ĐVT thì viết private
trong service mới, KHÔNG sửa `PrepickStockService`).

- [x] **Step 4: Verify HTTP**

```bash
curl -s -H "Authorization: Bearer $TOKEN" "$API/finance/accounting-prepick-cancels/stock?employee_id=$EMP" | head -c 600
curl -s -H "Authorization: Bearer $TOKEN" "$API/finance/accounting-prepick-cancels/product-customers?employee_id=$EMP&product_id=$PID"
```

Expected: `$EMP` lấy từ `SELECT employee_id, COUNT(DISTINCT customer_id) c FROM prepick_details WHERE qty>0 GROUP BY employee_id HAVING c>1 LIMIT 1`.
`available_qty` của `/stock` = tổng `available_qty` các KH ở `/product-customers` cùng hàng; không KH nào lặp.
NV không giữ gì → `/stock` `data: []`.

- [x] **Step 5: Đánh `[x]`, ghi checkpoint.**

---

## Task 5: Lập phiếu `store()` + lịch sử + thông báo (GHI TỒN THẬT)

**Files:**
- Create: `Http/Requests/AccountingPrepickCancel/AccountingPrepickCancelStoreRequest.php`
- Create: `Services/AccountingPrepickCancelHistoryService.php`
- Modify: service + controller (`store`, `histories`)

**Interfaces:**
- Consumes: `AccountingPrepickCancelLines::normalize()`, `deductFifo(..., $objectableType)`, `ownerCompanyId()`.
- Produces: `POST /` → `{data: {id, code}, message: 'Duyệt thành công'}`; `GET /{id}/histories` → shape y `PrepickCancelHistoryService::getLogs()`.

- [x] **Step 1: FormRequest** — rule spec §5.5 (không gồm `distinct` KH — việc đó `Lines` làm để có key lỗi đúng dòng):

```php
    public function rules(): array
    {
        return [
            'employee_id' => 'required|integer|exists:employees,id',
            'note' => 'nullable|string|max:255',
            'products' => 'required|array|min:1',
            'products.*.product_id' => 'required|integer',
            'products.*.customers' => 'required|array|min:1',
            'products.*.customers.*.customer_id' => 'required|integer',
            'products.*.customers.*.qty' => 'required|numeric|min:0|max:999999',
            'products.*.customers.*.unit_id' => 'required|integer',
        ];
    }

    public function messages(): array
    {
        return [
            'employee_id.required' => 'Vui lòng chọn nhân viên.',
            'note.max' => 'Ghi chú tối đa 255 ký tự.',
            'products.required' => 'Vui lòng thêm ít nhất 1 hàng hoá.',
            'products.*.customers.required' => 'Vui lòng chọn khách hàng.',
            'products.*.customers.*.customer_id.required' => 'Vui lòng chọn khách hàng.',
            'products.*.customers.*.qty.required' => 'Vui lòng nhập số lượng duyệt huỷ.',
            'products.*.customers.*.qty.numeric' => 'Số lượng phải là số.',
            'products.*.customers.*.qty.min' => 'Số lượng không được âm.',
            'products.*.customers.*.qty.max' => 'Số lượng tối đa 999,999.',
            'products.*.customers.*.unit_id.required' => 'Vui lòng chọn đơn vị tính.',
        ];
    }
```

- [x] **Step 2: `store()`** trong service

```php
    public function store(Request $request): AccountingPrepickCancel
    {
        $this->assertCanManage();

        $employeeId = (int) $request->input('employee_id');
        $ownerCompanyId = $this->ownerCompanyId($employeeId);
        $products = (array) $request->input('products', []);
        $productIds = array_map(function ($p) { return (int) ($p['product_id'] ?? 0); }, $products);

        try {
            $lines = AccountingPrepickCancelLines::normalize(
                $products,
                $this->productInfo($productIds),     // products + brands + product_models, 1 query
                $this->unitCoefficients($productIds) // "pid:uid" => [coefficient, unit_name], 1 query
            );
        } catch (AccountingPrepickCancelLinesException $e) {
            throw ValidationException::withMessages($e->getErrors());
        }

        $object = DB::transaction(function () use ($request, $employeeId, $ownerCompanyId, $lines) {
            $object = new AccountingPrepickCancel();
            $object->code = randomString(20);
            $object->employee_id = $employeeId;
            $object->note = $request->input('note');
            // Giữ nghĩa ERP: công ty NGƯỜI LẬP (danh sách ERP + HRM lọc theo cột này).
            $object->company_id = AccountingPrepickCancel::currentCompanyId();
            $object->created_by = auth()->id();
            $object->updated_by = auth()->id();
            $object->save();
            $object->generateCode();

            $lotCount = 0;
            foreach ($lines as $line) {
                $detail = new AccountingPrepickCancelDetail();
                $detail->accounting_prepick_cancel_id = $object->id;
                foreach (['product_id', 'product_name', 'product_code', 'brand_id', 'brand_name', 'model_id', 'model_name'] as $f) {
                    $detail->{$f} = $line[$f];
                }
                $detail->save();

                foreach ($line['customers'] as $row) {
                    $dc = new AccountingPrepickCancelDetailCustomer();
                    $dc->accounting_prepick_cancel_detail_id = $detail->id;
                    $dc->product_id = $line['product_id'];
                    foreach (['customer_id', 'qty', 'unit_id', 'unit_name', 'unit_coefficient', 'cancel_qty'] as $f) {
                        $dc->{$f} = $row[$f];
                    }
                    $dc->save();

                    $lotCount += $this->stock->deductFifo(
                        $line['product_id'],
                        $employeeId,
                        $row['customer_id'],
                        $ownerCompanyId,
                        $row['cancel_qty'],
                        $dc->id,
                        $line['product_name'],
                        AccountingPrepickCancelDetailCustomer::ERP_TYPE
                    );
                }
            }

            // Lịch sử nằm TRONG transaction (bài học Redmine #11327).
            $this->history->logCreate($object->fresh(['products.customers.customer', 'employee.info']), $lotCount);

            return $object;
        });

        $this->notifyOwner($object); // NGOÀI transaction — lỗi gửi chỉ log

        return $object;
    }
```

Kiểm sau khi viết: `BaseModel`/`Model` HRM có ghi đè `created_by` không (bẫy màn trước) — entity
extends `Illuminate\Database\Eloquent\Model` như `PrepickCancel` nên không bị.

- [x] **Step 3: `notifyOwner()`** — skill `notification-convention`. Người nhận = `employee_id`;
người lập = chính NV đó → bỏ qua. Nội dung: `'[TC] Huỷ hàng giữ: ' . $code . '. ' . <tên kế toán> . ' vừa huỷ hàng giữ của bạn.'`,
`url = '/finance/accounting-prepick-cancels/' . $id`, `type = 'accountingPrepickCancel'`.
Cài bằng bản `sendNotification()` private copy từ `PrepickCancelRequestService:709-764` (insert
`notifications` + Redis + `SendNotification::dispatch`, bọc `try/catch \Throwable` → `Log::error`).
⚠️ Đây là bản sao thứ 4 của hàm này (nhập thẳng / điều chuyển / yêu cầu hủy đã có) → ghi vào mục
"Đề xuất" cuối plan để user quyết gom thành helper — KHÔNG tự gom (hàm dùng chung).

- [x] **Step 4: History service** — copy `PrepickCancelHistoryService`, snapshot `{employee, note,
products: ["<tên> · <mã KH - tên KH> · <qty> <ĐVT> (= <cancel_qty> ĐV cơ bản)"]}`, note
`'Đã trừ tồn hàng giữ trên N lô.'`, `changes = []` khi `create` (Redmine #11186).

- [x] **Step 5: E2E tầng HTTP** (đã sao lưu ở Task 0)

1. Chọn `$EMP`/`$PID` có ≥ 2 KH, ≥ 2 lô cho 1 KH (query Task 4). Ghi `qty` từng lô trước.
2. POST 1 hàng × 2 KH, 1 dòng dùng ĐVT hệ số > 1 nếu hàng có → 200, trả `KTPHHG-xxxxx`.
3. Kiểm: `detail_customers.cancel_qty` đúng; lô trừ theo `expire_date` tăng dần; `prepick_logs`
   `objectable_type = 'App\Model\Warehouse\AccountingPrepickCancelDetailCustomer'`, `objectable_id` = id dòng KH;
   `accounting_prepick_cancel_history` 1 dòng; `notifications` 1 dòng cho NV.
4. `GET /{id}`, `/histories`, popup Lịch sử giữ hàng (`PrepickStockReportService`) có link `/finance/accounting-prepick-cancels/{id}`.
5. Bị chặn (mỗi ca đếm lại 5 bảng — phải KHÔNG đổi): vượt tồn · trùng KH · ĐVT không thuộc hàng ·
   toàn dòng 0 · giảm tay `prepick_details.qty` rồi POST số cũ · TK không quyền (403).
6. Kế toán công ty A lập phiếu cho NV công ty B (nếu dữ liệu có) → trừ đúng lô công ty B.
7. Hồi quy: lập 1 Phiếu hủy thường qua `POST /finance/prepick-cancels` từ 1 yêu cầu test → log ghi
   `App\Model\Warehouse\PrepickCancel`.
8. Mở ERP (dev) — phiếu HRM hiện ở danh sách + chi tiết ERP; modal Lịch sử giữ hàng ERP hiện dòng log.

- [x] **Step 6: Dọn dữ liệu test** — xoá phiếu/dòng/log/lịch sử/thông báo test, khôi phục `prepick_details.qty`
từ bản `bak_`, đối chiếu từng cột 5 bảng với bản sao lưu:

```php
foreach (['accounting_prepick_cancels','accounting_prepick_cancel_details','accounting_prepick_cancel_detail_customers','prepick_details','prepick_logs'] as $t) {
    $diff = DB::select("SELECT COUNT(*) c FROM (SELECT * FROM {$t} EXCEPT SELECT * FROM bak_{$t}_20260928) x")[0]->c
          + DB::select("SELECT COUNT(*) c FROM (SELECT * FROM bak_{$t}_20260928 EXCEPT SELECT * FROM {$t}) x")[0]->c;
    echo "$t lệch: $diff".PHP_EOL;
}
```

Expected: mọi bảng `lệch: 0` (MySQL < 8.0.31 không có `EXCEPT` → dùng `LEFT JOIN ... WHERE b.id IS NULL` theo từng cột).

- [x] **Step 7: Đánh `[x]`, ghi checkpoint.**

---

## Task 6: In + xuất Excel (BE)

**Files:** 2 blade in; service `renderPrint`, `renderPrintList`, `exportData`; controller `printData`, `printListData`, `export`.

- [x] **Step 1:** Copy `prints/prepick-cancel.blade.php` + `prints/prepick-cancel-list.blade.php` (đã dùng
`_layout.blade.php` có sẵn khối ký chuẩn #11253). Phiếu: bảng gộp dòng theo hàng hoá (rowspan = số KH),
cột STT · Tên hàng · Model · Mã · Thương hiệu · Khách hàng · SL duyệt huỷ · ĐVT; khối ký 3 người
(Người lập / Kế toán trưởng / Nhân viên giữ hàng). Danh sách: 5 cột, khai `@page { size: A4 landscape }`.
Letterhead theo công ty **của phiếu** (trait `PrintsCompanyLetterhead` / `companyHeader()` như màn cũ).
Rowspan khi sang trang: theo skill `print-page` (bảng ô gộp vỡ khi in nhiều trang).
- [x] **Step 2:** `exportData()` trả `{rows: [{code, employee_name, created_at, created_by_name}], filter_text, header}`
— copy `PrepickCancelService::exportData()` + `exportFilterText()`.
- [x] **Step 3: Verify:** `curl .../{id}/print-data` trả `data.template` HTML có `KTPHHG-`; `print-list-data`
với bộ lọc ngày có dòng "Từ ngày … đến ngày …". Render HTML xem bằng Playwright (chụp ảnh, đọc ảnh).
- [x] **Step 4: Đánh `[x]`, ghi checkpoint.**

---

## Task 7: FE danh sách + menu

**Files:** `pages/finance/accounting-prepick-cancels/index.vue`, `components/export-excel.js`, `components/subsystem-menu/finance.js`.

- [x] **Step 1:** Copy `pages/finance/prepick-cancels/index.vue`, đổi endpoint
`finance/accounting-prepick-cancels`, `columnScreenKey: 'finance_accounting_prepick_cancels'`.
- [x] **Step 2:** Cột mặc định: STT · Mã phiếu (`code`, sticky, `.v2-cell-link` → `/_id`) · Huỷ của nhân viên (`employeeName`) ·
Ngày lập (`createdAt`, sortable) · Người lập (`createdByName`). Cột ẩn: Ghi chú. Bỏ cột/bộ lọc Trạng thái, Phiếu yêu cầu, Khách hàng của màn gốc.
- [x] **Step 3:** Tìm nhanh = mã phiếu (`keyword`, deep watcher). Bộ lọc nâng cao: Hàng hoá (`product`) ·
Huỷ của nhân viên (`employee_id`, select2 nguồn `/employees`) · Người lập (`created_by`) · Khoảng ngày
(`startDate`/`endDate`). Nút Làm mới nạp lại danh sách.
- [x] **Step 4:** Toolbar: **Thêm** (→ `/create`) · Xuất Excel · In danh sách (popup `ReportPrintPreviewModal`).
Hàng: `V2BaseRowActions` In phiếu · Lịch sử (`PrepickHistoryModal` với endpoint `/{id}/histories`).
`can_manage = false` → khối "Bạn chưa có quyền Quản lý giữ hàng" thay bảng, ẩn Thêm.
- [x] **Step 5:** `export-excel.js` copy màn gốc, 5 cột STT · Mã phiếu · Huỷ của nhân viên · Ngày lập · Người lập,
tiêu đề "DANH SÁCH PHIẾU HUỶ HÀNG GIỮ KẾ TOÁN", file `danh_sach_huy_hang_giu_ke_toan.xlsx`; mã/ngày dạng chuỗi,
căn `middle` mọi ô, `numFmt '@'` cho cột có `field` (bài học #11326).
- [x] **Step 6:** Menu: `{ label: 'Phiếu huỷ hàng giữ kế toán', link: '/finance/accounting-prepick-cancels' }` + comment 1 dòng nguồn ERP.
- [x] **Step 7: Verify Playwright** (`playwright-a`, chờ ≥ 3s sau mỗi lần lọc, CHỤP ẢNH và xem): danh sách
ra đúng số phiếu Task 3; lọc từng trường; sắp xếp; cấu hình cột; Excel mở được; popup in; popup lịch sử
phiếu ERP cũ (rỗng — đúng). **`browser_close` khi xong.**
- [x] **Step 8: Đánh `[x]`, ghi checkpoint.**

---

## Task 8: FE tạo phiếu

**Files:** `create.vue`, `components/AccountingPrepickCancelForm.vue`.

- [x] **Step 1:** `create.vue` copy `prepick-cancels/create.vue` (vỏ + `beforeRouteLeave`, `unsavedChangesMixin`).
- [x] **Step 2: Khối Thông tin chung** — Nhân viên (`V2BaseSelect`/select2 nguồn `/employees?keyword=`, bắt buộc) · Ghi chú (≤255, đếm ký tự).
Đổi nhân viên khi đã có dòng → confirm "Đổi nhân viên sẽ xoá toàn bộ hàng hoá đã chọn. Tiếp tục?"; huỷ → trả lại giá trị cũ.
- [x] **Step 3: Khối Chi tiết** — state:

```js
// form.products: [{ product_id, product_name, product_code, model_name, brand_name,
//   options: [{customer_id, customer_name, available_qty}],   // từ /product-customers
//   units:   [{unit_id, unit_name, unit_coefficient, is_base}],
//   customers: [{ uid, customer_id, qty, unit_id }] }]
availableInUnit(product, row) {
    const opt = product.options.find(o => o.customer_id === row.customer_id)
    const unit = product.units.find(u => u.unit_id === row.unit_id)
    if (!opt || !unit) return null
    return opt.available_qty / (unit.unit_coefficient || 1)
},
isOver(product, row) {
    const max = this.availableInUnit(product, row)
    return max !== null && Number(row.qty) > max + 1e-9
},
customerOptions(product, row) {   // loại KH đã chọn ở dòng khác của CÙNG hàng hoá
    const used = product.customers.filter(c => c.uid !== row.uid).map(c => c.customer_id)
    return product.options.filter(o => !used.includes(o.customer_id))
},
```

Bảng gộp dòng (rowspan = số KH): STT · Tên hàng · Model · Mã hàng · Thương hiệu | Khách hàng · Có thể huỷ
(`formatNumber(availableInUnit)`) · Duyệt huỷ (input, `sanitizeNumberEvent`, báo đỏ "Vượt số có thể huỷ
(tối đa X)") · ĐVT (select `units`) · ✕ (ẩn khi còn 1 KH) | ⊖ xoá hàng. Dưới ô KH: link
"+ Thêm khách hàng" — ẩn khi `customerOptions` rỗng.
Nút ⊕ mở `PrepickStockSearchModal`: `endpoint="finance/accounting-prepick-cancels/stock"`,
`:employeeId="form.employee_id"`, `:requireCustomer="false"`, `hideExisting`,
`title="Hàng đang giữ của nhân viên"`, `subtitle="Chỉ liệt kê hàng nhân viên đã chọn còn đang giữ"`,
`emptyText="Nhân viên này hiện không giữ hàng hoá nào."` (prop có sẵn). Nút ⊕ ẨN khi chưa chọn nhân viên,
thay bằng dòng gợi ý "Chọn nhân viên trước để thêm hàng hoá".
Thêm hàng → gọi `/product-customers` → 1 dòng KH đầu tiên (`options[0]`, ĐVT `is_base`, qty rỗng).
- [x] **Step 4: Footer** `V2Footer`: **Duyệt** (validate FE: có NV, ≥ 1 dòng qty > 0, không ô nào `isOver`
→ cuộn tới ô lỗi; confirm "Duyệt phiếu sẽ trừ tồn hàng giữ ngay, không hoàn tác được. Tiếp tục?" không
`danger`) · **Quay lại**. POST payload `{employee_id, note, products: [{product_id, customers: [{customer_id, qty, unit_id}]}]}`.
Thành công → toast "Duyệt thành công" → `/finance/accounting-prepick-cancels`. 422 → gắn lỗi theo key
`products.i.customers.j.*` vào đúng ô; lỗi `products` (thiếu tồn) → hiện dưới bảng + toast `apiErrorMessage`.
- [x] **Step 5: Verify Playwright** (xem ảnh): chưa chọn NV → không có ⊕; chọn NV không giữ hàng → popup câu rỗng mới;
thêm hàng → KH đầu tự chọn; thêm KH tới hết → link ẩn; đổi ĐVT → Có thể huỷ đổi theo hệ số; gõ chữ/âm bị chặn;
vượt → báo đỏ; đổi NV → confirm; thoát khi đã nhập → cảnh báo chưa lưu. **Duyệt thật 1 phiếu** (đã sao lưu)
rồi dọn theo Task 5 Step 6. **`browser_close`.**
- [x] **Step 6: Đánh `[x]`, ghi checkpoint.**

---

## Task 9: FE chi tiết

**Files:** `_id/index.vue`, `components/AccountingPrepickCancelDetail.vue`.

- [x] **Step 1:** Copy `prepick-cancels/_id/index.vue`. Khối Thông tin chung chỉ đọc: Mã phiếu · Huỷ của nhân viên
(+ phòng ban) · Người lập · Ngày lập · Ghi chú. Bảng gộp dòng (Khách hàng · SL duyệt huỷ · ĐVT, bỏ Có thể huỷ).
Section `PrepickHistoryPanel` cuối trang. Footer: In phiếu (popup) · Quay lại.
- [x] **Step 2: Verify Playwright** 1 phiếu ERP cũ nhiều KH (rowspan đúng) + 1 phiếu HRM vừa tạo (có lịch sử).
URL phiếu công ty khác → trang báo không có quyền. **`browser_close`.**
- [x] **Step 3: Đánh `[x]`, ghi checkpoint.**

---

## Task 10: Rà soát + tài liệu

- [x] **Step 1:** Chạy skill `erp-to-hrm-screen` phần "rà lại màn đã port" + `code-reviewer` trên diff 2 repo.
- [x] **Step 2:** `vendor/bin/phpunit tests/Unit/AccountingPrepickCancelLinesTest.php` — PASS lần cuối.
- [x] **Step 3:** Cập nhật `design.md` (trạng thái), checkpoint cuối, `.plans/gop-db/STATUS.md` (ngắn gọn).
- [x] **Step 4:** Báo user: danh sách file đổi, việc user còn làm (bấm tay dev, đối chiếu 2 cổng, xoá `bak_*_20260928`, commit).

---

## Đề xuất (cần user quyết, KHÔNG tự làm)

- Hàm `sendNotification()` private đang bị copy ở 4 service nhóm Giữ hàng/Nhập thẳng → gom thành helper
  dùng chung (vd `Modules/Finance/Services/Concerns/SendsBulkNotification`). Chạm hàm dùng chung nên phải hỏi.

---

## Checkpoint — 2026-09-28

```text
Vừa hoàn thành: design.md + spec + plan.md (thiết kế user duyệt 2026-09-28).
Đang làm dở: không.
Bước tiếp theo: Task 0 — hỏi user tạo nhánh trong worktree gop-db hay worktree riêng, rồi sao lưu 5 bảng.
Blocked: không.
```

## Checkpoint — 2026-09-29

```text
Vừa hoàn thành: Task 0-10 CODE XONG + VERIFY (chưa commit — rule project).
  Worktree riêng `.worktrees/accounting-prepick-cancel` ở CẢ 2 repo, nhánh
  `feat/finance-accounting-prepick-cancel` tách từ origin/gop_db (user chọn 2026-09-28).
  BE: 4 entity + class thuần Lines (+exception) + 2 service + controller + FormRequest +
  ListResource + 2 blade in + 1 migration (đã chạy local) + 10 route; sửa PrepickStockService
  (deductFifo +$objectableType, +holdingCustomersOfProduct) và PrepickStockReportService (hrm_path).
  FE: index / create / _id + form dùng chung + export-excel + link menu.
  Test: 13 unit test Lines (TDD) xanh; suite tests/Unit 219 (2 fail sẵn MeetingRoom, không liên quan).
  E2E HTTP: 6 ca chặn rollback sạch, duyệt thật trừ FIFO đúng, log đúng chuỗi lớp ERP + id dòng KH,
  hồi quy phiếu hủy thường OK. Playwright (TK #27 có quyền): DS / chi tiết / in / tạo / Excel.
  Dọn dữ liệu test → EXCEPT 2 chiều 5 bảng với bak_*_20260928: 0 lệch.
  Final review (subagent): 0 Critical; đã sửa 3 lỗi nâng hạng (trần làm tròn xuống, cancel_qty về 0,
  403 trước validate); 10 minor hoãn — danh sách ở ledger/ báo cáo cuối.
Lệch plan có chủ ý: bỏ route /employees (dùng store employeeOptions); thêm chặn "Có thể huỷ" ở
  Lines (plan chỉ dựa deductFifo — sẽ huỷ được hàng đang chờ xuất); form dùng chung create/show;
  thêm 2 cột cập nhật (#11180); super admin thấy mọi công ty.
Đang làm dở: không.
Bước tiếp theo (user): review diff 2 worktree → commit; bấm tay trên dev; đối chiếu 2 cổng ERP/HRM
  (Task 5 bước 6 kế toán khác công ty + bước 8 modal Lịch sử giữ hàng ERP); xoá 5 bảng bak_*_20260928.
Blocked: không.
```

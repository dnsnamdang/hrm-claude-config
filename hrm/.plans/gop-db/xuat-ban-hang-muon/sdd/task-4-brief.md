# Task 4 — Calculator thuần + Unit test

**Repo:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api` (nhánh gop_db, Laravel 8, PHP 7.4). Mọi lệnh chạy trong thư mục này.

Tạo 1 class helper thuần (static, không DB, không Eloquent) + 1 Unit test. TDD: viết test fail → viết class → test pass.

## CHỈNH SỬA so với plan (BẮT BUỘC dùng bản này)
Plan ghi verify bằng `php artisan test --filter=BorrowSellRequestCalculatorTest`. **KHÔNG dùng lệnh đó** — `phpunit.xml` testsuite chỉ trỏ `./tests/Unit` + `./tests/Feature`, KHÔNG bao gồm `Modules/`, nên `--filter` sẽ báo "No tests executed" (đã kiểm chứng: test module chỉ discover khi truyền ĐƯỜNG DẪN file). Dùng lệnh có đường dẫn:
```
php artisan test Modules/Finance/Tests/Unit/BorrowSellRequestCalculatorTest.php
```
(Cảnh báo `TTY mode requires /dev/tty` khi chạy non-interactive là vô hại, bỏ qua.)

## Bước 1 — Viết test FAIL trước
Tạo `Modules/Finance/Tests/Unit/BorrowSellRequestCalculatorTest.php` (base class `Tests\TestCase` đã xác nhận tồn tại; các test module khác trong thư mục này cùng namespace `Modules\Finance\Tests\Unit`):

```php
<?php
namespace Modules\Finance\Tests\Unit;

use Tests\TestCase;
use Modules\Finance\Services\BorrowSellRequest\BorrowSellRequestCalculator;

class BorrowSellRequestCalculatorTest extends TestCase
{
    /** @test */
    public function available_qty_divides_by_coefficient()
    {
        // (100 - 20 - 10) / 2 = 35
        $this->assertEquals(35.0, BorrowSellRequestCalculator::availableSellQty(100, 20, 10, 2));
    }

    /** @test */
    public function qty_exceeded_uses_floor_when_coefficient_not_one()
    {
        // available 3.5, coefficient 2 -> floor(3.5)=3; xin 4 -> vượt
        $this->assertTrue(BorrowSellRequestCalculator::isQtyExceeded(3.5, 2, 4));
        $this->assertFalse(BorrowSellRequestCalculator::isQtyExceeded(3.5, 2, 3));
        // coefficient 1 -> so trực tiếp
        $this->assertTrue(BorrowSellRequestCalculator::isQtyExceeded(3.5, 1, 4));
        $this->assertFalse(BorrowSellRequestCalculator::isQtyExceeded(3.5, 1, 3.5));
    }

    /** @test */
    public function over_limit_debt_only_when_limit_set_and_exceeded()
    {
        $this->assertFalse(BorrowSellRequestCalculator::isOverLimitDebt(null, 1000, 5000));   // không khai hạn mức
        $this->assertFalse(BorrowSellRequestCalculator::isOverLimitDebt(0, 1000, 5000));       // hạn mức 0 = không chặn
        $this->assertFalse(BorrowSellRequestCalculator::isOverLimitDebt(10000, 4000, 5000));   // 9000 <= 10000
        $this->assertTrue(BorrowSellRequestCalculator::isOverLimitDebt(10000, 6000, 5000));    // 11000 > 10000
    }
}
```

## Bước 2 — Chạy test, xác nhận FAIL
```
php artisan test Modules/Finance/Tests/Unit/BorrowSellRequestCalculatorTest.php
```
Kỳ vọng: FAIL với "Class ...BorrowSellRequestCalculator not found" (class chưa tạo). DÁN output vào report.

## Bước 3 — Viết calculator (port công thức ERP store dòng 377-378 + checkLimit dòng 611)
Tạo `Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestCalculator.php`:

```php
<?php
namespace Modules\Finance\Services\BorrowSellRequest;

class BorrowSellRequestCalculator
{
    public static function availableSellQty(float $baseExportedQty, float $borrowReturnedQty, float $returningQty, float $unitCoefficient): float
    {
        $coef = $unitCoefficient ?: 1;
        return ($baseExportedQty - $borrowReturnedQty - $returningQty) / $coef;
    }

    public static function isQtyExceeded(float $available, float $unitCoefficient, float $requestedQty): bool
    {
        if ($unitCoefficient != 1) {
            return floor($available) < $requestedQty;
        }
        return $available < $requestedQty;
    }

    public static function isOverLimitDebt(?float $limitExportDebt, float $currentDebt, float $requestAmountAfterVat): bool
    {
        if (!$limitExportDebt) {
            return false;
        }
        return ($currentDebt + $requestAmountAfterVat) > $limitExportDebt;
    }
}
```

## Bước 4 — Chạy test, xác nhận PASS
```
php artisan test Modules/Finance/Tests/Unit/BorrowSellRequestCalculatorTest.php
```
Kỳ vọng: PASS (3 test / 9 assertion). DÁN output vào report.

## KHÔNG làm
- KHÔNG commit, KHÔNG push, KHÔNG dispatch subagent, KHÔNG sửa file khác (chỉ 2 file trên).
- KHÔNG thêm method ngoài 3 method trên. KHÔNG đọc vendor/.
- KHÔNG sửa phpunit.xml.

## Report
Ghi `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-4-report.md`: 2 đường dẫn file, output Bước 2 (FAIL) + Bước 4 (PASS).
Trả về (ngắn, KHÔNG dán code): STATUS, 1 dòng "test 3/3 pass" hay lỗi, concerns nếu có.

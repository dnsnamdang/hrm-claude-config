# Task 4 review package (2 new untracked files)

## Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestCalculator.php
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

## Modules/Finance/Tests/Unit/BorrowSellRequestCalculatorTest.php
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

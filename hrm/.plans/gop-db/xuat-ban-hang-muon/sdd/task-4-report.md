# Task 4 — Report

## Files tạo
1. `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api/Modules/Finance/Tests/Unit/BorrowSellRequestCalculatorTest.php`
2. `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api/Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestCalculator.php`

## Bước 2 — Test FAIL (class chưa tồn tại)

```
  FAIL Modules\Finance\Tests\Unit\BorrowSellRequestCalculatorTest

  ⨯ available qty divides by coefficient
  ⨯ qty exceeded uses floor when coefficient not one
  ⨯ over limit debt only when limit set and exceeded

  ---

  • Modules\Finance\Tests\Unit\BorrowSellRequestCalculatorTest > available qty divides by coefficient
  PHPUnit\Framework\ExceptionWrapper

  Class 'Modules\Finance\Services\BorrowSellRequest\BorrowSellRequestCalculator' not found

  Tests:  3 failed
  Time:   1.76s
```

## Bước 4 — Test PASS (class đã tồn tại)

```
  PASS Modules\Finance\Tests\Unit\BorrowSellRequestCalculatorTest

  ✓ available qty divides by coefficient
  ✓ qty exceeded uses floor when coefficient not one
  ✓ over limit debt only when limit set and exceeded

  Tests:  3 passed
  Time:   1.30s
```

## Kết quả

- **STATUS**: DONE
- **Test result**: 3 test / 9 assertion pass
- **Concerns**: Không có

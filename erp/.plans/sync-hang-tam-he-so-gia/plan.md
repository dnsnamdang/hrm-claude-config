# Sửa hệ số/giá các loại giá khi đồng bộ hàng tạm HRM → ERP — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Khi đồng bộ hàng tạm từ báo giá HRM, tạo đủ dòng giá cho MỌI loại giá với hệ số/giá công thức/định mức đúng (Bán lẻ tính theo giá nhập–giá bán; loại khác = 1/1/1), để SP sau duyệt không còn 0/0/0.

**Architecture:** Sửa duy nhất `TmpProductRequestSyncService::createFromHrm()`. Tách phần tính hệ số Bán lẻ thành 1 helper tĩnh thuần (test được), rồi thay khối tạo-1-dòng-giá bằng vòng lặp qua tất cả `price_types`. Không đụng luồng duyệt (`approve()`/`CreateProductService`) vì giá chảy từ tmp prices → form → product thật.

**Tech Stack:** PHP 7.4, Laravel 6, MySQL, PHPUnit (tests/Unit có sẵn).

## Global Constraints

- KHÔNG commit/push git khi user chưa yêu cầu (CLAUDE.md). Các bước "Commit" bên dưới chỉ chạy khi user đồng ý.
- KHÔNG đọc/sửa `vendor/`, `node_modules/`.
- Branch: `sync_quotation`.
- `coefficient` là `decimal(5,2)` → tối đa 999.99, 2 số lẻ.
- Mapping field HRM: `estimated_price` = giá nhập; `quoted_price` = giá bán (trước chiết khấu).
- Loại giá Bán lẻ: `price_type_id = 1` (hằng `TmpProductRequestSyncService::PRICE_TYPE_RETAIL`).
- File code: `app/Services/Sale/TmpProductRequestSyncService.php`.

---

## File Structure

- **Modify** `app/Services/Sale/TmpProductRequestSyncService.php`
  - Thêm `use App\Model\Product\PriceType;`
  - Thêm helper `public static function computeRetailCoefficient($sellPrice, $importPrice): float`
  - Thay khối tạo giá (hiện dòng 64–70) trong `createFromHrm()` bằng vòng lặp qua mọi loại giá.
- **Create (test)** `tests/Unit/TmpProductRetailCoefficientTest.php` — test helper thuần (không cần DB/app boot).

---

### Task 1: Helper `computeRetailCoefficient` + Unit test

**Files:**
- Modify: `app/Services/Sale/TmpProductRequestSyncService.php` (thêm method tĩnh, sau hằng `PRICE_TYPE_RETAIL`)
- Test: `tests/Unit/TmpProductRetailCoefficientTest.php`

**Interfaces:**
- Produces: `TmpProductRequestSyncService::computeRetailCoefficient($sellPrice, $importPrice): float`
  — trả hệ số Bán lẻ = `round(sell/import, 2)`, cap 999.99; `import <= 0` → `1.0`.

- [x] **Step 1: Viết test thất bại** — tạo `tests/Unit/TmpProductRetailCoefficientTest.php`:

```php
<?php

namespace Tests\Unit;

use App\Services\Sale\TmpProductRequestSyncService;
use PHPUnit\Framework\TestCase;

class TmpProductRetailCoefficientTest extends TestCase
{
    public function test_he_so_binh_thuong()
    {
        // 10 / 5 = 2
        $this->assertSame(2.0, TmpProductRequestSyncService::computeRetailCoefficient(10, 5));
    }

    public function test_lam_tron_2_so_le()
    {
        // 10 / 3 = 3.333... -> 3.33
        $this->assertSame(3.33, TmpProductRequestSyncService::computeRetailCoefficient(10, 3));
    }

    public function test_gia_nhap_0_tra_ve_1()
    {
        $this->assertSame(1.0, TmpProductRequestSyncService::computeRetailCoefficient(10, 0));
    }

    public function test_gia_nhap_am_coi_nhu_0()
    {
        $this->assertSame(1.0, TmpProductRequestSyncService::computeRetailCoefficient(10, -5));
    }

    public function test_cap_999_99()
    {
        // 1.000.000 / 1 = 1.000.000 -> cap 999.99
        $this->assertSame(999.99, TmpProductRequestSyncService::computeRetailCoefficient(1000000, 1));
    }
}
```

- [x] **Step 2: Chạy test cho chắc nó FAIL**

Run: `php vendor/bin/phpunit tests/Unit/TmpProductRetailCoefficientTest.php`
Expected: FAIL — `Call to undefined method ...::computeRetailCoefficient()`.

- [x] **Step 3: Thêm helper vào service**

Trong `app/Services/Sale/TmpProductRequestSyncService.php`, ngay sau dòng `const PRICE_TYPE_RETAIL = 1; // Bán lẻ` (dòng 19), thêm:

```php

    /**
     * Hệ số Bán lẻ = giá bán / giá nhập, làm tròn 2 số lẻ, cap 999.99.
     * Giá nhập <= 0 → hệ số = 1 (tránh chia 0).
     */
    public static function computeRetailCoefficient($sellPrice, $importPrice): float
    {
        $sellPrice = (float) $sellPrice;
        $importPrice = (float) $importPrice;
        if ($importPrice <= 0) {
            return 1.0;
        }
        $coefficient = round($sellPrice / $importPrice, 2);
        return $coefficient > 999.99 ? 999.99 : $coefficient;
    }
```

- [x] **Step 4: Lint + chạy test cho PASS**

Run: `php -l app/Services/Sale/TmpProductRequestSyncService.php && php vendor/bin/phpunit tests/Unit/TmpProductRetailCoefficientTest.php`
Expected: `No syntax errors detected` + `OK (5 tests)`.

- [ ] **Step 5: Commit** (chỉ khi user yêu cầu)

```bash
git add app/Services/Sale/TmpProductRequestSyncService.php tests/Unit/TmpProductRetailCoefficientTest.php
git commit -m "feat(sync-hang-tam): helper tính hệ số Bán lẻ theo giá nhập/giá bán"
```

---

### Task 2: Tạo đủ dòng giá mọi loại giá trong `createFromHrm()`

**Files:**
- Modify: `app/Services/Sale/TmpProductRequestSyncService.php` (import `PriceType`; thay khối dòng 64–70)

**Interfaces:**
- Consumes: `self::computeRetailCoefficient($sellPrice, $importPrice)` (Task 1); `App\Model\Product\PriceType`.

- [x] **Step 1: Thêm import PriceType**

Trong khối `use` đầu file (sau `use App\Model\Product\TmpProductUnitPrice;`, dòng 11), thêm:

```php
use App\Model\Product\PriceType;
```

- [x] **Step 2: Thay khối tạo 1 dòng giá bằng vòng lặp mọi loại giá**

Thay nguyên khối hiện tại (dòng 64–70):

```php
                $price = new TmpProductUnitPrice();
                $price->tmp_product_unit_id = $unit->id;
                $price->price_type_id = self::PRICE_TYPE_RETAIL;
                $price->price = $item['quoted_price'] ?? 0;
                $price->coefficient = 1;
                $price->sale_max_percent = 0;
                $price->save();
```

bằng:

```php
                // Tạo giá cho MỌI loại giá:
                // - Bán lẻ: giá công thức = giá bán (quoted_price); hệ số = giá bán / giá nhập (cap 999.99, giá nhập=0 -> 1); định mức = 0
                // - Loại khác: giá công thức = 1; hệ số = 1; định mức = 1
                $sellPrice = $item['quoted_price'] ?? 0;
                $importPrice = $item['estimated_price'] ?? 0;
                $retailCoefficient = self::computeRetailCoefficient($sellPrice, $importPrice);

                foreach (PriceType::query()->pluck('id') as $priceTypeId) {
                    $isRetail = (int) $priceTypeId === self::PRICE_TYPE_RETAIL;

                    $price = new TmpProductUnitPrice();
                    $price->tmp_product_unit_id = $unit->id;
                    $price->price_type_id = $priceTypeId;
                    $price->price = $isRetail ? $sellPrice : 1;
                    $price->coefficient = $isRetail ? $retailCoefficient : 1;
                    $price->sale_max_percent = $isRetail ? 0 : 1;
                    $price->save();
                }
```

- [x] **Step 3: Lint**

Run: `php -l app/Services/Sale/TmpProductRequestSyncService.php`
Expected: `No syntax errors detected`.

- [ ] **Step 4: Kiểm thử thủ công (E2E)**

Trên dev: đồng bộ 1 báo giá HRM (có dòng giá nhập + giá bán) sang ERP → mở hàng tạm vừa tạo (trạng thái "Đang tạo"):
- Loại **Bán lẻ**: hệ số = giá bán / giá nhập (vd giá bán 10, giá nhập 5 → 2.00), giá công thức = giá bán, định mức = 0.
- Các loại **khác**: hệ số = 1, giá công thức = 1, định mức = 1.
- Duyệt hàng tạm → SP thật KHÔNG còn loại giá 0/0/0.

- [ ] **Step 5: Commit** (chỉ khi user yêu cầu)

```bash
git add app/Services/Sale/TmpProductRequestSyncService.php
git commit -m "feat(sync-hang-tam): tạo đủ loại giá khi đồng bộ hàng tạm (Bán lẻ theo giá nhập/bán, loại khác=1/1/1)"
```

---

## Self-Review

1. **Spec coverage:**
   - Bán lẻ hệ số = giá bán/giá nhập, công thức = giá bán → Task 1 (helper) + Task 2 (retail branch). ✅
   - Loại khác = 1/1/1 (hệ số/công thức/định mức) → Task 2 (else branch: price=1, coefficient=1, sale_max=1). ✅
   - Giá nhập=0 → hệ số=1 → Task 1 (`importPrice <= 0` → 1.0) + test. ✅
   - Cap 999.99, làm tròn 2 số lẻ → Task 1 + test. ✅
   - Tạo cho mọi loại giá (query price_types) → Task 2 (`PriceType::query()->pluck('id')`). ✅
   - Không đụng approve/CreateProductService → không có task nào sửa. ✅
2. **Placeholder scan:** không có TBD/TODO; mọi step có code/command cụ thể. ✅
3. **Type consistency:** `computeRetailCoefficient($sellPrice, $importPrice): float` dùng nhất quán giữa Task 1 (định nghĩa) và Task 2 (gọi). ✅

### Checkpoint — 2026-06-30
Vừa hoàn thành: Task 1 + Task 2. `TmpProductRequestSyncService`: thêm helper `computeRetailCoefficient` + vòng lặp tạo mọi loại giá (Bán lẻ=giá bán/giá nhập, công thức=giá bán, định mức=0; loại khác=1/1/1). Unit test 5/5 pass, php -l sạch.
Đang làm dở: không.
Bước tiếp theo: USER test E2E trên dev (đồng bộ báo giá HRM → kiểm hệ số Bán lẻ + loại khác 1/1/1 → duyệt hết 0/0/0) → rồi commit.
Blocked:

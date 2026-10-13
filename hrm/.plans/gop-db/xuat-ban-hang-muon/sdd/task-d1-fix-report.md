# Task D1 — Fix report

**Status:** DONE

**File sửa (duy nhất):** `hrm-api/Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestService.php`

## Tóm tắt diff

1. **Thêm `computeAmounts(Request $request, bool $isFirm): array`** (private, đặt ngay trước `isOverLimit`, cùng khối "Over-limit / debt") — port nguyên văn công thức ERP `BorrowSellRequestProduct` từ brief §1/§2a: loop `(array) $request->products`, skip product không có `details`, `price` ép 0 khi `!$isFirm` (WrService), `qty` = tổng `qty` các `details` (không nhân `unit_coefficient`), trả mảng 6 khóa `sum_amount_after_extra`, `sum_amount_after_extra_vat`, `sum_amount_after_extra_after_vat`, `sum_amount_allocated`, `sum_amount_allocated_after_vat`, `vat_cost_allocated`. Copy verbatim từ brief, không chỉnh sửa.

2. **Đổi chữ ký `isOverLimit`**: `isOverLimit(Request $request, int $customerId): bool` → `isOverLimit(int $customerId, float $requestAmountAfterVat): bool`. Giữ nguyên toàn bộ logic lấy `$companyId`, `$limit` (từ `declare_limit_debts.limit_debt_export`), `$currentDebt` (`getDebtCustomerByEmployee`) — chỉ thay tham số amount cuối từ `(float) $request->input('sum_amount_after_extra_after_vat', 0)` sang tham số truyền vào `$requestAmountAfterVat`.

3. **`store()`**:
   - Trước dòng quyết định escalation: thêm `$amounts = $this->computeAmounts($request, $isFirm);`
   - Đổi lời gọi: `$overLimit = $this->isOverLimit((int) $contract->customer_id, $amounts['sum_amount_after_extra_after_vat']);`
   - Thêm `$amounts` vào `use (...)` của `DB::transaction(function () use ($request, $contract, $isFirm, $status, $amounts) {...})`.
   - 7 dòng persist snapshot (dòng ~93-99): `vat_percent` GIỮ NGUYÊN đọc từ `$request->input('vat_percent')`; 6 dòng còn lại (`vat_cost_allocated`, `sum_amount_allocated`, `sum_amount_allocated_after_vat`, `sum_amount_after_extra`, `sum_amount_after_extra_vat`, `sum_amount_after_extra_after_vat`) đổi sang đọc từ `$amounts[...]`.

Không đụng `BorrowSellRequestCalculator`, FormRequest, Entity, hay bất kỳ file FE nào. Không đổi thứ tự các bước khác trong `store()` (assertDiffPrice, transaction, syncProducts, notify). Không catch `Exception` chung, không thêm `?->`/property promotion/union type (PHP 7.4 an toàn).

## Verify

- `php -l Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestService.php` → **No syntax errors detected**.
- `vendor/bin/phpunit Modules/Finance/Tests/Unit/BorrowSellRequestCalculatorTest.php` → **OK (3 tests, 9 assertions)**.

## Rà tay theo brief §4

Đọc `BorrowSellRequestCalculator::isOverLimitDebt`:
```php
public static function isOverLimitDebt(?float $limitExportDebt, float $currentDebt, float $requestAmountAfterVat): bool
{
    if (!$limitExportDebt) {
        return false;
    }
    return ($currentDebt + $requestAmountAfterVat) > $limitExportDebt;
}
```

**(a) Kịch bản spec §5** — limit=100tr, currentDebt=90tr, 1 SP firm: `extra_price`=0, `price`=1.000.000, tổng `qty` (details)=30, `vat_percent`=0.
- `computeAmounts`: `price=1.000.000` (isFirm=true) → `priceAfterExtra=0+1.000.000=1.000.000` → `amountAfterExtra=1.000.000×30=30.000.000` → `amountAfterExtraVat=30.000.000×0/100=0` → `sum_amount_after_extra_after_vat = 30.000.000 + 0 = 30tr`.
- `isOverLimit(customerId, 30tr)`: `limit=100tr`, `currentDebt=90tr` → `isOverLimitDebt(100tr, 90tr, 30tr)` = `(90tr+30tr=120tr) > 100tr` = **true** → `status = CHO_TP_DUYET (10)`. Khớp brief. ✔

**(b) KH chưa khai hạn mức** — `$limit` = `DB::table('declare_limit_debts')->...->value('limit_debt_export')` = `null` khi không có bản ghi → `isOverLimit` truyền `$limit === null ? null : (float) $limit` = `null` vào `isOverLimitDebt`. Trong Calculator, `!$limitExportDebt` (null là falsy) → trả `false` ngay, bất kể `$requestAmountAfterVat` bao nhiêu → `status = CHO_KE_TOAN_KHO (2)`. Không escalate nhầm. ✔

**(c) WrService (type 2, `$isFirm=false`)** — `computeAmounts` ép `$price = $isFirm ? (float)(...) : 0.0` → luôn 0 khi WrService, bất kể payload gửi `price` gì. Vậy `priceAfterExtra = extra_price + 0 = extra_price`, `amountAfterExtra = extra_price × qty`, cộng dồn theo vat: `sum_amount_after_extra_after_vat = Σ extra_price×qty×(1+vat_percent/100)` — đúng công thức ERP nêu trong brief. ✔

**(d) `$amounts` trong `use(...)` + 7 cột persist** — dòng 72: `DB::transaction(function () use ($request, $contract, $isFirm, $status, $amounts) {` — có `$amounts`. Dòng 93-99: `vat_percent` từ `$request->input('vat_percent')` (giữ nguyên, không nằm trong `$amounts`); 6 dòng còn lại đọc đúng 6 khóa tương ứng của `$amounts`. ✔

## Rulings / assumptions

- Không có ruling nào cần suy đoán — brief cho code verbatim cho `computeAmounts` và mô tả rõ ràng cách sửa `isOverLimit`/`store()`; đã đối chiếu đúng code hiện trạng (dòng số có lệch nhẹ so với brief do comment sẵn có trong file nhưng logic/thứ tự khớp) trước khi sửa.
- Giữ nguyên toàn bộ logic lấy `$companyId`/`$limit`/`$currentDebt` trong `isOverLimit` — không đổi cách tính, chỉ đổi nguồn amount và chữ ký như brief yêu cầu.

## Concerns

- Không có concern chặn merge. Một điểm lưu ý không thuộc phạm vi task này: `computeAmounts` chỉ được gọi 1 lần trong `store()` trước `assertDiffPrice`/transaction — nếu sau này có thêm luồng update/edit phiếu dùng lại amount tính toán thì cần gọi lại `computeAmounts` tương tự (không tái sử dụng biến cache), nhưng hiện tại `store()` là luồng duy nhất cần sửa theo brief nên không cần thay đổi gì thêm.

# Fix D1 — Escalation vượt hạn mức không kích hoạt (BE tính giá trị phiếu server-side)

> Đây là requirements của bạn. Sửa **DUY NHẤT 1 file**: `hrm-api/Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestService.php`. KHÔNG đụng file khác. Stack: Laravel 8 / PHP 7.4 (KHÔNG constructor property promotion, KHÔNG `?->`, KHÔNG union type). Nhánh `gop_db`.

## 0. Bối cảnh & lỗi (đọc kỹ)
Phiếu Yêu cầu xuất bán hàng mượn (PYCXBHM) khi tạo phải quyết định trạng thái theo **hạn mức công nợ KH** (spec §5):
- `công nợ hiện tại KH (TK 131)` **+ giá trị phiếu đang lập** > `limit_export_debt` → status `CHO_TP_DUYET` (10), notify Trưởng phòng.
- ngược lại → status `CHO_KE_TOAN_KHO` (2).

**Defect hiện tại:** `isOverLimit()` lấy giá trị phiếu từ `$request->input('sum_amount_after_extra_after_vat', 0)`, nhưng **FE KHÔNG BAO GIỜ gửi field này** → luôn = 0 → điều kiện co lại thành `currentDebt > limit`, bỏ mất "+ giá trị phiếu đang lập". Hệ quả: phiếu chính gây vượt hạn mức lại đi thẳng KT kho, escalation TP→BGD (trọng tâm Phase 1) không kích hoạt.

Ngoài ra 7 cột snapshot `sum_amount_*` (dòng ~92-98) đang persist NULL vì cũng đọc từ `$request->input(...)` mà FE không gửi.

**Nguyên tắc bảo mật (CLAUDE.md):** escalation là ranh giới phân quyền → **fail-closed, KHÔNG tin tiền do FE gửi**. Bắt buộc **BE tự tính** giá trị phiếu từ các dòng sản phẩm trong payload.

## 1. Công thức (port NGUYÊN VĂN từ ERP — ground truth)
Từ class JS ERP `BorrowSellRequestProduct` (đã verify). Với **mỗi** phần tử trong `$request->products`:

```
price          = isFirm ? (float)(product['price'] ?? 0) : 0.0     // WrService (type 2): price LUÔN = 0
extra_price    = (float)(product['extra_price'] ?? 0)
allocated_price= (float)(product['allocated_price'] ?? 0)
vat_percent    = (float)(product['vat_percent'] ?? 0)
qty            = Σ over product['details']  của (float)(detail['qty'] ?? 0)   // đơn vị phiếu, KHÔNG nhân unit_coefficient

price_after_extra                 = extra_price + price
total_amount_after_extra          = price_after_extra * qty
total_amount_after_extra_vat      = total_amount_after_extra * vat_percent / 100
total_amount_after_extra_after_vat= total_amount_after_extra + total_amount_after_extra_vat
total_amount_allocated            = allocated_price * qty
vat_cost_allocated_line           = total_amount_allocated * vat_percent / 100
total_amount_allocated_after_vat  = total_amount_allocated + vat_cost_allocated_line
```

Tổng phiếu (cộng dồn qua tất cả product):
```
sum_amount_after_extra            = Σ total_amount_after_extra
sum_amount_after_extra_vat        = Σ total_amount_after_extra_vat
sum_amount_after_extra_after_vat  = Σ total_amount_after_extra_after_vat   // == sum_amount_after_extra + sum_amount_after_extra_vat
sum_amount_allocated              = Σ total_amount_allocated
sum_amount_allocated_after_vat    = Σ total_amount_allocated_after_vat
vat_cost_allocated                = Σ vat_cost_allocated_line
```

> Lưu ý: chỉ tính các product có `details` (giống `syncProducts` bỏ qua product thiếu `details`). Dùng `(array)` guard cho `$request->products` và `product['details']`.

## 2. Việc cần làm (chính xác)

### 2a. Thêm private helper tính tổng
Thêm method mới (đặt gần `isOverLimit`):
```php
/**
 * Tính giá trị phiếu server-side từ dòng SP trong payload (port công thức ERP
 * BorrowSellRequestProduct). KHÔNG tin số tiền FE gửi (fail-closed cho escalation).
 * Trả mảng 6 cột snapshot để vừa quyết định escalation vừa persist.
 */
private function computeAmounts(Request $request, bool $isFirm): array
{
    $sumAfterExtra = 0.0;
    $sumAfterExtraVat = 0.0;
    $sumAllocated = 0.0;
    $sumAllocatedAfterVat = 0.0;
    $vatCostAllocated = 0.0;

    foreach ((array) $request->products as $product) {
        if (!isset($product['details'])) {
            continue;
        }
        $price = $isFirm ? (float) ($product['price'] ?? 0) : 0.0;
        $extraPrice = (float) ($product['extra_price'] ?? 0);
        $allocatedPrice = (float) ($product['allocated_price'] ?? 0);
        $vatPercent = (float) ($product['vat_percent'] ?? 0);

        $qty = 0.0;
        foreach ((array) $product['details'] as $detail) {
            $qty += (float) ($detail['qty'] ?? 0);
        }

        $priceAfterExtra = $extraPrice + $price;
        $amountAfterExtra = $priceAfterExtra * $qty;
        $amountAfterExtraVat = $amountAfterExtra * $vatPercent / 100;
        $amountAllocated = $allocatedPrice * $qty;
        $vatAllocatedLine = $amountAllocated * $vatPercent / 100;

        $sumAfterExtra += $amountAfterExtra;
        $sumAfterExtraVat += $amountAfterExtraVat;
        $sumAllocated += $amountAllocated;
        $sumAllocatedAfterVat += $amountAllocated + $vatAllocatedLine;
        $vatCostAllocated += $vatAllocatedLine;
    }

    return [
        'sum_amount_after_extra' => $sumAfterExtra,
        'sum_amount_after_extra_vat' => $sumAfterExtraVat,
        'sum_amount_after_extra_after_vat' => $sumAfterExtra + $sumAfterExtraVat,
        'sum_amount_allocated' => $sumAllocated,
        'sum_amount_allocated_after_vat' => $sumAllocatedAfterVat,
        'vat_cost_allocated' => $vatCostAllocated,
    ];
}
```

### 2b. Đổi chữ ký + thân `isOverLimit` — nhận amount, KHÔNG đọc request input
Hiện tại (khoảng dòng 302-316) `isOverLimit(Request $request, int $customerId): bool` đọc `$request->input('sum_amount_after_extra_after_vat', 0)`. Đổi thành nhận thẳng số tiền:
```php
private function isOverLimit(int $customerId, float $requestAmountAfterVat): bool
{
    $currentDebt = $this->getDebtCustomerByEmployee($customerId);
    $limit = /* GIỮ NGUYÊN cách lấy limit hiện có trong hàm (declare_limit_debts / limit_export_debt theo company) */;
    return BorrowSellRequestCalculator::isOverLimitDebt($limit, $currentDebt, $requestAmountAfterVat);
}
```
- **GIỮ NGUYÊN** toàn bộ cách lấy `$limit`/`$currentDebt`/company scope đang có trong hàm — CHỈ bỏ tham số `Request $request` và thay nguồn amount bằng tham số `$requestAmountAfterVat`. Đọc code hiện tại của hàm trước khi sửa, đừng đoán cách lấy limit.
- Nếu `getDebtCustomerByEmployee` đang nhận thêm tham số nào khác thì giữ nguyên.

### 2c. `store()` — tính 1 lần, dùng cho cả escalation lẫn persist
Trong `store()`:
1. Ngay trước dòng quyết định escalation (hiện: `$overLimit = $this->isOverLimit($request, (int) $contract->customer_id);`), thêm:
   ```php
   $amounts = $this->computeAmounts($request, $isFirm);
   ```
2. Sửa lời gọi:
   ```php
   $overLimit = $this->isOverLimit((int) $contract->customer_id, $amounts['sum_amount_after_extra_after_vat']);
   ```
3. `$amounts` phải vào được closure `DB::transaction(function () use (...) {` → thêm `$amounts` vào danh sách `use (...)`.
4. Thay 7 dòng persist snapshot (hiện đọc `$request->input(...)`, khoảng dòng 92-98) bằng giá trị từ `$amounts`:
   ```php
   $object->vat_percent = $request->input('vat_percent');   // GIỮ NGUYÊN dòng vat_percent (không nằm trong $amounts)
   $object->vat_cost_allocated = $amounts['vat_cost_allocated'];
   $object->sum_amount_allocated = $amounts['sum_amount_allocated'];
   $object->sum_amount_allocated_after_vat = $amounts['sum_amount_allocated_after_vat'];
   $object->sum_amount_after_extra = $amounts['sum_amount_after_extra'];
   $object->sum_amount_after_extra_vat = $amounts['sum_amount_after_extra_vat'];
   $object->sum_amount_after_extra_after_vat = $amounts['sum_amount_after_extra_after_vat'];
   ```
   - `vat_percent` GIỮ đọc từ request input như cũ (là % của tab, không phải tổng tiền). Nếu dòng `vat_cost_allocated` cũ đọc request input thì thay như trên.

## 3. Ràng buộc
- **CHỈ** sửa `BorrowSellRequestService.php`. KHÔNG sửa Calculator (đã đúng), FormRequest, Entity, FE.
- PHP 7.4: không dùng `?->`, không property promotion, không union type. Dùng `(float)`, `(array)`, `?? 0`.
- Không đổi thứ tự các bước khác trong `store()` (assertDiffPrice, transaction, syncProducts, notify).
- Không catch chung `Exception`; giữ nguyên các `throw ValidationException`.
- KHÔNG commit/push. KHÔNG dispatch subagent. KHÔNG đọc `vendor/`, `node_modules/`.

## 4. Verify (ghi vào report)
- `php -l Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestService.php` → No syntax errors.
- Chạy lại unit test Calculator (không đổi nhưng xác nhận không vỡ): `vendor/bin/phpunit Modules/Finance/Tests/Unit/BorrowSellRequestCalculatorTest.php` → OK.
- Rà tay & ghi report:
  (a) Kịch bản spec §5: limit=100tr, currentDebt=90tr, phiếu 30tr (1 SP: extra_price 0, price 1.000.000, qty 30, vat 0) → `sum_amount_after_extra_after_vat`=30tr → `isOverLimitDebt(100tr, 90tr, 30tr)` = (120tr>100tr)=true → status 10 (CHO_TP_DUYET). Trace bằng đọc code, ghi rõ.
  (b) KH chưa khai hạn mức (`limit`=null) → `isOverLimitDebt` trả false → status 2 (không escalate nhầm). ✔
  (c) WrService: `price` bị ép 0, amount = Σ extra_price×qty×(1+vat/100) — đúng ERP.
  (d) Xác nhận `$amounts` đã có trong `use(...)` của closure và 7 cột persist đúng.

## 5. Report
Ghi report đầy đủ vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-d1-fix-report.md` (status, diff tóm tắt, verify, rulings/assumptions nếu có, concerns). Trả về controller: status + 1 dòng test summary + concerns.
